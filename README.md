# Robo-Mesh-Model

A single-file, no-build HTML tool that procedurally generates a stylized
humanoid mocap dummy and exports it as FBX / GLB — entirely client-side.

![](https://img.shields.io/badge/three.js-r185-blue) ![](https://img.shields.io/badge/FBX-7.4%20ASCII%20%2B%20binary-green)

## Run

```sh
python3 -m http.server        # from the repo root
open http://localhost:8000    # (any static server works; file:// does not)
```

## What you get

- **Character** — minimal capsule/rounded-box humanoid, toy-robot proportions,
  2,944 triangles, one flat gray material, no textures. T-pose, Y-up,
  centimeter units, ~172 cm tall.
- **Rig** — 26 joints with Mixamo-compatible names (`Hips`,
  `Spine/Spine1/Spine2`, `Neck`, `Head`, `Shoulder→Arm→ForeArm→Hand` +
  thumb/index, `UpLeg→Leg→Foot→ToeBase`). Identity rest rotations, pure
  translation offsets, single root — retargets in Unreal IK Retargeter,
  Maya HumanIK, MotionBuilder, and Mixamo without fixing. Mesh is rigidly
  skinned (one bone per vertex, weight 1.0). Optional `mixamorig:` name
  prefix at export time.
- **Viewer** — orbit controls, grid, three-point lighting; toggles for
  wireframe, skeleton helper, and joint-name labels; joint/triangle/height
  readouts and a collapsible hierarchy tree.

## Exports

| Button | Format | Notes |
|---|---|---|
| FBX (ASCII 7.4) | hand-written writer | primary; human-readable |
| FBX (binary 7.4) | same document tree, binary serializer | use this for Blender < 4.5 (its importer rejects ASCII FBX) |
| GLB | `GLTFExporter` | meters, per glTF spec |

Both FBX flavors carry the full skeleton, bind pose, and skin weights
(`UnitScaleFactor = 1`, i.e. centimeters, Y-up). The page re-imports its own
output with three.js loaders on load — the badge in the panel shows the
round-trip result.

## Verify against a real DCC

```sh
verify/run_checks.sh path/to/robo-mocap-dummy-binary.fbx path/to/robo-mocap-dummy.glb
```

Runs headless Blender (override with `BLENDER=…`) and asserts bone names,
parent map, rigid weights, triangle count, and world height for both files.
