#!/bin/bash
# v523 SINGLE-FLAG ISOLATION, WITH A BYTE-IDENTICAL KNOWN-ZERO ARM FROM THE
# START.  v522's leg 1 had no control, all three of its treatment arms beat the
# baseline on every column, and its one "OUTSIDE" reading (+6.41 pp) reversed
# sign (-1.71 pp) in a second draw that DID have one.  That lesson is applied
# here rather than re-learned: the known-zero arm is in leg 1.
#
# ARMS (5, same blocks, same seeds, seeds disjoint from the headline):
#   parent    the definition-site baseline
#   parentB   THE SAME TREE, second copy -- KNOWN-ZERO
#   iSALT     v523 with ONLY change 1 on (CREWREAD + COREFUND off)
#   iCREW     v523 with ONLY change 2 on (SALTEYES + COREFUND off)
#   iFLOORFUND  ⭐ change 3 ON ITS ONLY LIVE PATH: the v522 magazine floor
#             turned back ON (FS_V522_FLOOR = True) with the CORRECTED funding
#             predicate.  Change 3 is otherwise INERT in the fired config,
#             because the site it fixes sits inside a block the v522 verdict
#             ships behind FS_V522_FLOOR = False -- this arm is the honest way
#             to measure it rather than claiming it in the composite.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v523_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export PAR=4
SRC=bots/_v523eyes "$B/mkarm.sh" iSALT \
    "FS_V523_CREWREAD = False" "FS_V523_COREFUND = False" >/dev/null
SRC=bots/_v523eyes "$B/mkarm.sh" iCREW \
    "FS_V523_SALTEYES = False" "FS_V523_COREFUND = False" >/dev/null
SRC=bots/_v523eyes "$B/mkarm.sh" iFLOORFUND \
    "FS_V522_FLOOR = True" >/dev/null
BLOCKS="${IBLOCKS:-13}"
for i in $(seq 1 "$BLOCKS"); do
  s1=$((800+i*3-2)); s2=$((800+i*3-1)); s3=$((800+i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/iso/b$i"
  for a in parent parentB iSALT iCREW iFLOORFUND; do
    .venv/bin/python "$B/run_grid.py" "$B/arms/$a" \
        "$B/iso/b$i/$a.tsv" "$B/iso/b$i/rep$a" "$B/iso/b$i/log$a" \
        > "$B/iso/b$i/$a.log" 2>&1 &
    echo "$! iso-$a-b$i" >> "$B/PIDS"
  done
  wait
  echo "IBLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "ISO DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
