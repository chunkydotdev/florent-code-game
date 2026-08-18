#!/bin/bash
# v520 SINGLE-FLAG ISOLATION GRID.  FOUR arms in the same blocks on the same
# seeds: parent / pincer-only / presence-only / gunnear-only.
# ⛔ RUN REGARDLESS OF THE COMPOSITE'S SIGN.  The mandate makes the per-change
# attribution the deliverable either way; running it only when the composite
# disappoints is a selection rule on the analysis.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v520_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export PAR=2
BLOCKS="${BLOCKS:-13}"
OFF=${OFF:-500}
bash "$B/mkarm.sh" iPIN  "FS_V520_PRESENCE = False" "FS_V520_GUNNEAR = False" >/dev/null
bash "$B/mkarm.sh" iPRES "FS_V520_PINCER = False"   "FS_V520_GUNNEAR = False" >/dev/null
bash "$B/mkarm.sh" iGUN  "FS_V520_PINCER = False"   "FS_V520_PRESENCE = False" >/dev/null
for i in $(seq 1 "$BLOCKS"); do
  s1=$((OFF+i*3-2)); s2=$((OFF+i*3-1)); s3=$((OFF+i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/iso/b$i"
  for a in parent iPIN iPRES iGUN; do
    .venv/bin/python "$B/run_grid.py" "$B/arms/$a" \
        "$B/iso/b$i/$a.tsv" "$B/iso/b$i/rep$a" "$B/iso/b$i/log$a" \
        > "$B/iso/b$i/$a.log" 2>&1 &
  done
  wait
  echo "ISO BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "ISO DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
