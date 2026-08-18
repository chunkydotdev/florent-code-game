#!/bin/bash
# GATED CONTROL -- archipelago vs `_v468kladturbo`, TWO DRAWS of 36, pooled 72.
# ⛔ THIS LEG IS NOT NULL-BY-CONSTRUCTION AND THAT IS THE POINT.  archipelago's
# signature is in FS_MAP_SKIP so the ferry, the crew appointment, the ring turn
# and the sync state are all unreachable -- but v520 open item 7 measured TWO
# `fs_crew_on()` read sites OUTSIDE the map gate, so the parent still spends
# seat 3 as a raider on a board the plank refuses.  v521 change 0 closes them.
# ⇒ the leg MEASURES THE FIX, and the falsifier is stated: seat-3 raider spend
# must go to zero and the result must stay inside the baseline's gated band.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v521_build
export OPP=bots/_v468kladturbo
export MAPS=archipelago
export PAR=4
for d in 1 2; do
  if [ "$d" = 1 ]; then export SEEDS=101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118; else export SEEDS=119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136; fi
  for arm in base v521; do
    T=$B/arms/pinceronly; [ "$arm" = v521 ] && T=bots/_v521sync
    mkdir -p "$B/gated/d$d"
    .venv/bin/python "$B/run_grid.py" "$T" \
        "$B/gated/d$d/$arm.tsv" "$B/gated/d$d/rep$arm" "$B/gated/d$d/log$arm" \
        > "$B/gated/d$d/$arm.log" 2>&1 &
    echo "$! gated-d$d-$arm" >> "$B/PIDS"
  done
  wait
  echo "GATED DRAW $d done $(date -u +%H:%M:%SZ)"
done
echo "GATED DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
