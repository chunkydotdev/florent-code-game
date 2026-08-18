#!/bin/bash
# Build a v522 verification arm: a COPY of $SRC (default bots/_v522floor)
# with flag overrides APPENDED to doctrine.py (later assignment wins under
# `import *`).  Canonical trees are never mutated.
set -e
cd /Users/junghard/Projects/Work/florent-code-game
SRC="${SRC:-bots/_v522floor}"
NAME="$1"; shift
D=scratchpad/s51_v522_build/arms/$NAME
rm -rf "$D"; mkdir -p scratchpad/s51_v522_build/arms
cp -R "$SRC" "$D"
chmod -R u+w "$D"
rm -rf "$D/__pycache__"
{
  echo ""
  echo "# --- ARM OVERRIDE: $NAME (src $SRC) ---"
  for kv in "$@"; do echo "$kv"; done
} >> "$D/doctrine.py"
echo "built $D from $SRC"
