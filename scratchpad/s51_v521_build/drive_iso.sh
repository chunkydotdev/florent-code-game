#!/bin/bash
# v521 SINGLE-FLAG ISOLATION -- FIVE arms in the SAME blocks on the SAME seeds.
# Run because the composite SURPRISED (k<=200 -7.04pp OUTSIDE at n=1080/arm
# against a known-zero arm at +1.39pp).  Seeds 501-552, disjoint from the
# headline.  Each arm is the FULL tree with exactly one change group left on.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v521_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export PAR=2
# LADDER-ONLY: the three sync reorders, no magazine reserve, no phase change,
# no gate fix.
SRC=bots/_v521sync "$B/mkarm.sh" iLADDER \
  "FS_V521_COLLARFIRST = False" "FS_V521_PHASE_HONEST = False" \
  "FS_V521_GATEFIX = False" >/dev/null
# MAGAZINE-ONLY: the collar reserve + the honest phase, no ladder reorder, no
# gate fix.  (PHASE_HONEST rides with it because 1d is unreachable without it --
# measured, not assumed: 0 of 12 deterministic games changed with 1d alone.)
SRC=bots/_v521sync "$B/mkarm.sh" iMAG \
  "FS_V521_NEAR_CLOSE = False" "FS_V521_HOLD = False" "FS_V521_BUYIN = False" \
  "FS_V521_GATEFIX = False" >/dev/null
# GATEFIX-ONLY: fired-config correction (ii) alone.
SRC=bots/_v521sync "$B/mkarm.sh" iGATE \
  "FS_V521_NEAR_CLOSE = False" "FS_V521_HOLD = False" "FS_V521_BUYIN = False" \
  "FS_V521_COLLARFIRST = False" "FS_V521_PHASE_HONEST = False" >/dev/null

for i in $(seq 1 13); do
  s1=$((500+i*3-2)); s2=$((500+i*3-1)); s3=$((500+i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/iso/b$i"
  for arm in pinceronly iLADDER iMAG iGATE; do
    T="$B/arms/$arm"
    .venv/bin/python "$B/run_grid.py" "$T" \
        "$B/iso/b$i/$arm.tsv" "$B/iso/b$i/rep$arm" "$B/iso/b$i/log$arm" \
        > "$B/iso/b$i/$arm.log" 2>&1 &
    echo "$! iso-b$i-$arm" >> "$B/PIDS"
  done
  wait
  echo "ISO BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "ISO DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
