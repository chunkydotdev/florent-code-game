#!/bin/bash
# v517 MECHANISM ARMS.  One arm at a time, PAR=4 inside; logs on in every arm
# so the instrument tables are read off the same volume of trace.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v517_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap
export PAR=4
run () { local n="$1"; local s="$2"; export SEEDS="$s"; mkdir -p "$B/mech/$n"
  .venv/bin/python "$B/run_grid.py" "$B/arms/$n" "$B/mech/$n/res.tsv" \
      "$B/mech/$n/rep" "$B/mech/$n/log" > "$B/mech/$n/run.log" 2>&1
  echo "ARM $n done $(date -u +%H:%M:%SZ)"; }
for a in m1_fired m1_off m2_off m2b_off; do run "$a" "1,2,3"; done
echo "MECH DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
