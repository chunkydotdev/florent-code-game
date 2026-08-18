#!/bin/bash
# v518 MECHANISM ARMS.  One arm at a time, PAR=4 inside; every instrument on in
# every arm so the tables are read off the same volume of trace.
# ⛔ THE INSTRUMENTED ARMS ARE NOT THE HEADLINE ARMS.  GAP518 runs a PROBED
# sentinel purchase scan every ring round; local CPU is unmeasurable
# (get_cpu_time_elapsed reads 0 under `fcode run`) but the platform TLE is real,
# so behaviour under logs is not asserted identical to behaviour without them.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v518_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap
export PAR=4
run () { local n="$1"; export SEEDS="1,2,3"; mkdir -p "$B/mech/$n"
  .venv/bin/python "$B/run_grid.py" "$B/arms/$n" "$B/mech/$n/res.tsv" \
      "$B/mech/$n/rep" "$B/mech/$n/log" > "$B/mech/$n/run.log" 2>&1
  echo "ARM $n done $(date -u +%H:%M:%SZ)"; }
for a in mF mE mR mOff mFloor30 mFloor0; do run "$a"; done
echo "MECH DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
