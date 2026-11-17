"""Headless import assertions for Robo-Mesh-Model (Ivory Mannequin Android) exports.

Usage:
    blender -b --factory-startup --python verify/blender_check.py -- \
        <binary.fbx> <model.glb> [name-prefix] [expected-tris]

Verifies, for both files: armature with the 52 Mixamo-named joints (full
finger chains) and the expected parent map, a mesh where every vertex sits in
exactly one vertex group at weight 1.0, triangle count, three material slots
all in use, mesh anchored to the armature, and real-world height ~1.76 m.
ASCII FBX is intentionally not tested here — Blender < 4.5 cannot read it;
that flavor is covered by the in-page FBXLoader round-trip.
"""
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:]
FBX_PATH, GLB_PATH = argv[0], argv[1]
PREFIX = argv[2] if len(argv) > 2 else ''
EXPECTED_TRIS = int(argv[3]) if len(argv) > 3 else 8980

PARENTS = {
    'Hips': None, 'Spine': 'Hips', 'Spine1': 'Spine', 'Spine2': 'Spine1',
    'Neck': 'Spine2', 'Head': 'Neck',
}
for S in ('Left', 'Right'):
    PARENTS[S + 'Shoulder'] = 'Spine2'
    PARENTS[S + 'Arm'] = S + 'Shoulder'
    PARENTS[S + 'ForeArm'] = S + 'Arm'
    PARENTS[S + 'Hand'] = S + 'ForeArm'
    for f in ('Thumb', 'Index', 'Middle', 'Ring', 'Pinky'):
        PARENTS[S + 'Hand' + f + '1'] = S + 'Hand'
        PARENTS[S + 'Hand' + f + '2'] = S + 'Hand' + f + '1'
        PARENTS[S + 'Hand' + f + '3'] = S + 'Hand' + f + '2'
    PARENTS[S + 'UpLeg'] = 'Hips'
    PARENTS[S + 'Leg'] = S + 'UpLeg'
    PARENTS[S + 'Foot'] = S + 'Leg'
    PARENTS[S + 'ToeBase'] = S + 'Foot'
PARENTS = {PREFIX + k: (PREFIX + v if v else None) for k, v in PARENTS.items()}

EXPECTED_MATERIALS = 3

failures = []
passes = []


def check(cond, msg):
    (passes if cond else failures).append(msg)
    print(('ok   ' if cond else 'FAIL ') + msg)


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def verify(tag):
    arms = [o for o in bpy.data.objects if o.type == 'ARMATURE']
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    check(len(arms) == 1, f'{tag}: exactly one armature (got {len(arms)})')
    check(len(meshes) == 1, f'{tag}: exactly one mesh (got {len(meshes)})')
    if not arms or not meshes:
        return
    arm, mesh = arms[0], meshes[0]

    names = {b.name for b in arm.data.bones}
    check(names == set(PARENTS), f'{tag}: bone name set, {len(names)} bones '
          f'(missing {set(PARENTS) - names or "none"}, extra {names - set(PARENTS) or "none"})')
    for b in arm.data.bones:
        want = PARENTS.get(b.name)
        got = b.parent.name if b.parent else None
        if got != want:
            check(False, f'{tag}: parent of {b.name} is {got}, want {want}')
            break
    else:
        check(True, f'{tag}: parent map matches')

    deg = sum(1 for b in arm.data.bones if (b.head_local - b.tail_local).length < 1e-6)
    check(deg == 0, f'{tag}: no zero-length bones ({deg})')

    def wx(bone):
        return (arm.matrix_world @ bone.head_local.to_4d()).to_3d()

    bl = arm.data.bones
    check(wx(bl[PREFIX + 'Head']).z > wx(bl[PREFIX + 'Neck']).z, f'{tag}: Head above Neck')
    check(wx(bl[PREFIX + 'LeftArm']).x > 0.05 and wx(bl[PREFIX + 'RightArm']).x < -0.05,
          f'{tag}: left/right on +/-X')
    la, ra = wx(bl[PREFIX + 'LeftArm']), wx(bl[PREFIX + 'RightArm'])
    lh, rh = wx(bl[PREFIX + 'LeftHand']), wx(bl[PREFIX + 'RightHand'])
    check(abs(la.z - lh.z) < 1e-4 and abs(ra.z - rh.z) < 1e-4, f'{tag}: arms level (T-pose)')
    check(abs(wx(bl[PREFIX + 'Hips']).z - 0.97) < 0.02, f'{tag}: Hips at ~0.97 m')
    tip = wx(bl[PREFIX + 'LeftHandMiddle3'])
    check(tip.x > wx(bl[PREFIX + 'LeftHand']).x, f'{tag}: finger chains extend along +X')

    tris = sum(1 for p in mesh.data.polygons if len(p.vertices) == 3)
    ngons = len(mesh.data.polygons) - tris
    check(tris == EXPECTED_TRIS and ngons == 0,
          f'{tag}: {tris} triangles, {ngons} non-tris (want {EXPECTED_TRIS}, 0)')

    check(len(mesh.material_slots) == EXPECTED_MATERIALS,
          f'{tag}: {len(mesh.material_slots)} material slots (want {EXPECTED_MATERIALS})')
    used_slots = {p.material_index for p in mesh.data.polygons}
    check(used_slots == set(range(EXPECTED_MATERIALS)),
          f'{tag}: all material slots referenced by polygons ({sorted(used_slots)})')

    vg_names = {g.name for g in mesh.vertex_groups}
    check(vg_names == set(PARENTS), f'{tag}: vertex-group names == bone names')
    bad = 0
    for v in mesh.data.vertices:
        ws = [g.weight for g in v.groups if g.weight > 1e-6]
        if len(ws) != 1 or abs(ws[0] - 1.0) > 1e-4:
            bad += 1
    check(bad == 0, f'{tag}: rigid weights, one group @1.0 per vertex ({bad} bad)')

    depsgraph = bpy.context.evaluated_depsgraph_get()
    ev = mesh.evaluated_get(depsgraph)
    ws = [ev.matrix_world @ Vector(c) for c in ev.bound_box]
    height = max(v.z for v in ws) - min(v.z for v in ws)
    check(1.68 < height < 1.84, f'{tag}: height {height:.3f} m (want ~1.76)')

    # Bbox spans are translation-invariant, so also anchor the mesh to the
    # skeleton: a wrong cluster Transform displaces the mesh object itself.
    off = (mesh.matrix_world.translation - arm.matrix_world.translation).length
    check(off < 1e-5, f'{tag}: mesh anchored to armature (offset {off:.6f} m)')
    used = set()
    for p in mesh.data.polygons:
        used.update(p.vertices)
    loose = len(mesh.data.vertices) - len(used)
    check(loose == 0, f'{tag}: no loose vertices ({loose})')

    for o in (arm, mesh):
        s = o.scale
        # FBX import puts the cm->m conversion on object scale (0.01); GLB is 1.
        uniform = abs(s.x - s.y) < 1e-9 and abs(s.y - s.z) < 1e-9
        check(uniform, f'{tag}: {o.name} scale uniform ({s.x:.4f})')


clear_scene()
bpy.ops.import_scene.fbx(filepath=FBX_PATH)
verify('fbx-binary')

clear_scene()
bpy.ops.import_scene.gltf(filepath=GLB_PATH)
verify('glb')

print(f'\n{len(passes)} passed, {len(failures)} failed')
if failures:
    sys.exit(1)
