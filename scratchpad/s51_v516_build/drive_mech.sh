#!/bin/bash
# v516 MECHANISM ARMS + FLAG-OFF.  One arm at a time, PAR=4 inside.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v516_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap
export PAR=4
run () {  # name seeds
  local n="$1"; local s="$2"
  export SEEDS="$s"
  mkdir -p "$B/mech/$n"
  .venv/bin/python "$B/run_grid.py" "$B/arms/$n" \
      "$B/mech/$n/res.tsv" "$B/mech/$n/rep" "$B/mech/$n/log" \
      > "$B/mech/$n/run.log" 2>&1
  echo "ARM $n done $(date -u +%H:%M:%SZ)"
}
for a in m1_fired m1_off m1_holdoff m3_fired m3_off m2_fired m2_off; do
  run "$a" "1,2,3"
done
# flag-off behavioural: 60 games each, master flag off vs an untouched copy of
# the parent, SAME seeds.  A structural diff is not enough (v515 finding 3).
run flagoff "1,2,3,4,5,6"
run parent515 "1,2,3,4,5,6"
echo "MECH DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
