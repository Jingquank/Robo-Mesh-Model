# Robo-Mesh-Model

A single-file, no-build HTML tool that procedurally generates an **ivory
ball-jointed mannequin android** — rebuilt in code from a reference plate
(elongated artist-figure proportions, exposed ball joints, brass hinge
hardware, articulated five-finger hands) — rigged and exported as FBX / GLB
entirely client-side.

![](https://img.shields.io/badge/three.js-r185-blue) ![](https://img.shields.io/badge/FBX-7.4%20ASCII%20%2B%20binary-green)

## Run

```sh
python3 -m http.server        # from the repo root
open http://localhost:8000    # (any static server works; file:// does not)
```

## What you get

- **Character** — 175 cm ivory mannequin android, 8,980 triangles, built to a
  measured proportion table from the reference image (9.3 head-units, crotch
  at 49% of height, arm chain 39.5°/43.3°). Warm ivory satin shells with
  clamshell seam lines, layered chest/belly/pelvis panels (briefs with W top
  edge and V crotch), double-petal shoulder pauldrons, exposed ball joints at
  elbows/knees/ankles with brass pin discs, brass wrist pins + knuckle rows +
  finger hinge rings, featureless egg head with an incised face-plate oval,
  bootie feet with toe-cap panel breaks. Three materials, no textures.
  T-pose bind, Y-up, centimeter units.
- **Rig** — full 52-joint Mixamo-compatible skeleton including complete
  five-finger chains (3 joints per finger per hand). Identity rest
  rotations, pure translation offsets, single Hips root — retargets in
  Unreal IK Retargeter, Maya HumanIK, MotionBuilder, and Mixamo without
  fixing. Rigid skinning (one bone per vertex at weight 1.0). Optional
  `mixamorig:` name prefix at export time.
- **Viewer** — studio scene matching the reference plate (blue-gray cove,
  warm key, soft shadow) with orbit controls and the **reference A-pose**
  display pose (viewer-only; every export rebuilds the character in bind
  pose). Toggles for wireframe, skeleton helper, and joint labels;
  joint/triangle/height readouts; collapsible hierarchy tree.

### URL parameters

| Param | Effect |
|---|---|
| `?stage=1..5` | rebuild at a sculpt stage: 1 blockout, 2 structure, 3 +seams/hardware, 4 +materials, 5 final plate |
| `?review=front\|tq\|profile\|hands\|head` | fixed reference-matched camera, panel hidden |
| `?explode=1.6` | named-parts explode view with click-to-identify (parts scale apart about the model centre; seams ride their shells) |

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
verify/run_checks.sh path/to/mannequin-binary.fbx path/to/mannequin.glb
```

Runs headless Blender (override with `BLENDER=…`) and asserts bone names
and parent map (all 52 joints), rigid weights, triangle count, material
slot usage, mesh-to-armature anchoring, and world height for both files.
Optional args: name prefix (e.g. `mixamorig:`) and expected triangle count.
Current build: **40/40 assertions pass**.

## Provenance

`spec/mannequin-sculpt-spec.json` is the machine-validated sculpt
specification the model was built against — measured component dimensions,
materials with reference-extracted PBR evidence, per-pass acceptance
criteria, and the full review history of the staged build (blockout →
proportion lock → structure → features → materials → lighting →
interaction → optimization).
