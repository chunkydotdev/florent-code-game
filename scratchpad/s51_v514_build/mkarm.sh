#!/bin/bash
# Build a v514 verification arm: a COPY of bots/_v514ferrycrew with flag
# overrides APPENDED to doctrine.py (later assignment wins under `import *`).
# The canonical tree is never mutated.
set -e
cd /Users/junghard/Projects/Work/florent-code-game
NAME="$1"; shift
D=scratchpad/s51_v514_build/arms/$NAME
rm -rf "$D"; mkdir -p scratchpad/s51_v514_build/arms
cp -R bots/_v514ferrycrew "$D"
rm -rf "$D/__pycache__"
{
  echo ""
  echo "# --- ARM OVERRIDE: $NAME ---"
  for kv in "$@"; do echo "$kv"; done
} >> "$D/doctrine.py"
echo "built $D"
