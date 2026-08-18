#!/bin/bash
# v522 SINGLE-FLAG ISOLATION -- FOUR ARMS IN THE SAME BLOCKS ON THE SAME SEEDS.
# Seeds 501+ are DISJOINT from the headline's 1-90.
#   parent    -- the v521-verdict parent (baseline)
#   iCOREFUND -- v522 with the Core's funding re-check back ON: the isolation
#                arm for reachability correction (1)
#   iCREW     -- v522 with the crew-slot read OFF: correction (2)
#   iNOPHASE  -- THE PARENT with FS_V521_PHASE_HONEST OFF.  ⭐ v521 kept 1e on
#                a SEPARABILITY ARGUMENT and never isolated it -- `iMAG` bundled
#                1d and 1e and carried the whole -9.83 pp.  This is the arm that
#                asks whether the retained half costs anything.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v522_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export PAR=4
BLOCKS="${BLOCKS:-13}"
"$B/mkarm.sh" iCOREFUND "FS_V522_CORE_FUND = True" >/dev/null
"$B/mkarm.sh" iCREW     "FS_V522_CREW_READ = False" >/dev/null
SRC=bots/_v521sync "$B/mkarm.sh" iNOPHASE "FS_V521_SYNC = False" \
    "FS_V521_COLLARFIRST = False" "FS_V521_PHASE_HONEST = False" >/dev/null
for i in $(seq 1 "$BLOCKS"); do
  s1=$((500+i*3-2)); s2=$((500+i*3-1)); s3=$((500+i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/iso/b$i"
  for a in parent iCOREFUND iCREW iNOPHASE; do
    .venv/bin/python "$B/run_grid.py" "$B/arms/$a" \
        "$B/iso/b$i/$a.tsv" "$B/iso/b$i/rep$a" "$B/iso/b$i/log$a" \
        > "$B/iso/b$i/$a.log" 2>&1 &
    echo "$! iso-$a-b$i" >> "$B/PIDS"
  done
  wait
  echo "ISO BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "ISO DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
