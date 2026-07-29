# Robo-Mesh-Model

A single-file, no-build HTML tool that procedurally generates a sleek,
compact humanoid robotics platform — Unitree-flavored proportions, exposed
articulated joints, dexterous hands, expressive sensor head — rigged and
exported as FBX / GLB entirely client-side.

![](https://img.shields.io/badge/three.js-r185-blue) ![](https://img.shields.io/badge/FBX-7.4%20ASCII%20%2B%20binary-green)

## Run

```sh
python3 -m http.server        # from the repo root
open http://localhost:8000    # (any static server works; file:// does not)
```

## What you get

- **Character** — compact humanoid research-robot concept, ~146 cm,
  6,396 triangles. White composite shell panels, dark anodized actuator
  discs exposed at every major joint (shoulders, elbows, wrists, waist,
  hips, knees, ankles), shin struts, battery pack, and a wrap-around
  sensor visor. Three materials, no textures, no logos. T-pose bind,
  Y-up, centimeter units.
- **Rig** — full 52-joint Mixamo-compatible skeleton including complete
  five-finger chains (3 joints per finger per hand). Identity rest
  rotations, pure translation offsets, single Hips root — retargets in
  Unreal IK Retargeter, Maya HumanIK, MotionBuilder, and Mixamo without
  fixing. Rigid skinning (one bone per vertex at weight 1.0). Optional
  `mixamorig:` name prefix at export time.
- **Viewer** — white studio scene with soft shadows, orbit controls, and
  an **athletic stance** display pose (viewer-only; every export rebuilds
  the character in bind pose). Toggles for wireframe, skeleton helper,
  and joint labels; joint/triangle/height readouts; collapsible hierarchy
  tree with finger chains folded.

## Exports

| Button | Format | Notes |
|---|---|---|
| FBX (ASCII 7.4) | hand-written writer | primary; human-readable |
| FBX (binary 7.4) | same document tree, binary serializer | use this for Blender < 4.5 (its importer rejects ASCII FBX) |
| GLB | `GLTFExporter` | meters, per glTF spec |

Both FBX flavors carry the full skeleton, bind pose, rigid skin weights,
and per-polygon material assignment across the three material slots
(`UnitScaleFactor = 1`, i.e. centimeters, Y-up). The page re-imports its
own output with three.js loaders on load — the badge in the panel shows
the round-trip result.

## Verify against a real DCC

```sh
verify/run_checks.sh path/to/robo-mesh-binary.fbx path/to/robo-mesh.glb
```

Runs headless Blender (override with `BLENDER=…`) and asserts bone names
and parent map (all 52 joints), rigid weights, triangle count, material
slot usage, mesh-to-armature anchoring, and world height for both files.
Optional args: name prefix (e.g. `mixamorig:`) and expected triangle count.
