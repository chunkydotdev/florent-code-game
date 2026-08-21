#!/bin/zsh
# mkmerge.sh <destdir> <base> <side1> [<side2> ...]
#
# THREE-WAY MERGE of N plank trees onto one common base, file by file.
#
# ⛔ WHY THREE-WAY AND NOT `cp THE-ONE-THAT-CHANGED`.  v529merge could take
# whole files from one sibling because each file had at most ONE editor.  Here
# doctrine.py has THREE, main.py has THREE and siege.py has THREE.  A per-file
# copy would silently drop two planks.  `git merge-file` is used for the four
# code files because it CONFLICTS LOUDLY on an overlap instead of picking a
# side — a merge that cannot fail has not been seen to merge.
#
# ⛔ doctrine.py IS RESOLVED SEPARATELY AND ON PURPOSE.  All three planks append
# their constant block at the file's END, at the identical anchor, so
# `git merge-file` conflicts on every pair (both-added-at-EOF has no trailing
# context to order by).  `doctrine_union.py` resolves it and PROVES the
# resolution (P1-P7, self-tested both ways) instead of concatenating and
# hoping.
#
# ⛔ MODE-444 HAZARD (mkarm.sh's lesson): `cp -R` preserves read-only modes and
# a previous run may have left one behind, so chmod BEFORE the first write.
set -e
DEST=$1; BASE=$2; shift 2
SIDES=("$@")
[ -e "$DEST" ] && chmod -R u+w "$DEST"
rm -rf "$DEST"; cp -R "$BASE" "$DEST"; chmod -R u+w "$DEST"
rm -rf "$DEST/__pycache__"

# --- doctrine.py: the proven append-union -----------------------------------
DARGS=()
for SIDE in "${SIDES[@]}"; do
  cmp -s "$BASE/doctrine.py" "$SIDE/doctrine.py" || DARGS+=(--side "$SIDE/doctrine.py")
done
if (( ${#DARGS} )); then
  .venv/bin/python3 scratchpad/s52_v542_build/doctrine_union.py \
      --base "$BASE/doctrine.py" "${DARGS[@]}" --out "$DEST/doctrine.py"
fi

# --- the four code files: git merge-file ------------------------------------
for SIDE in "${SIDES[@]}"; do
  for f in eco main raid siege; do
    if cmp -s "$BASE/$f.py" "$SIDE/$f.py"; then continue; fi
    if git merge-file -L merged -L base -L "$SIDE" \
         "$DEST/$f.py" "$BASE/$f.py" "$SIDE/$f.py"; then
      print -r -- "MERGE ok        $DEST/$f.py  <- $SIDE"
    else
      print -r -- "MERGE CONFLICT  $DEST/$f.py  <- $SIDE"
    fi
  done
done

# ⛔ EXIT CODE IS NOT THE HEALTH SIGNAL — assert on the ARTEFACT.  A conflict
# marker left in a .py is a syntax error at import in most shapes but not all,
# so grep for it explicitly and refuse the tree.
if grep -REn '^(<<<<<<<|=======|>>>>>>>)' "$DEST"/*.py; then
  print -r -- "REFUSED: conflict markers present in $DEST"
  exit 2
fi
for f in doctrine eco main raid siege; do
  .venv/bin/python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$DEST/$f.py"
  printf "MD5 %s %s %s\n" "$DEST" "$f" "$(md5 -q $DEST/$f.py)"
done
print -r -- "MERGE TREE OK $DEST"
