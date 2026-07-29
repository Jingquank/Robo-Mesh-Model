#!/usr/bin/env bash
# Headless DCC verification of Robo-Mesh-Model exports.
#
#   verify/run_checks.sh <binary.fbx> <model.glb> [name-prefix]
#
# Export the files from the tool first (serve the repo root, e.g.
# `python3 -m http.server`, open index.html, use the Download buttons).
# Requires Blender; override the binary with BLENDER=/path/to/blender.
set -euo pipefail

BLENDER="${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
if [ ! -x "$BLENDER" ]; then
  echo "Blender not found at $BLENDER (set BLENDER=...)" >&2
  exit 2
fi
if [ $# -lt 2 ]; then
  echo "usage: $0 <binary.fbx> <model.glb> [name-prefix]" >&2
  exit 2
fi

exec "$BLENDER" -b --factory-startup --python "$(dirname "$0")/blender_check.py" -- "$@"
