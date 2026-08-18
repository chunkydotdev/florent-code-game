#!/bin/bash
# GATED ALARM FOLLOW-UP.  The first draw read v516 22/36 against parent 29/36 on
# archipelago -- a leg every v516 branch is structurally unable to reach (the
# board's signature is in FS_MAP_SKIP, so `_fs_gate` refuses and all three
# changes sit behind it).  The control that separates "leak" from "draw" is the
# FLAG-OFF arm, which is the v516 tree with LOKI_FS_V516 = False: if it lands
# with v516 rather than with the parent, the movement is the draw.
# Second draw of both principals on FRESH seeds for the same reason.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v516_build
export OPP=bots/_v468kladturbo
export MAPS=archipelago
export PAR=4
export SEEDS=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18
mkdir -p "$B/gated/flagoff"
.venv/bin/python "$B/run_grid.py" "$B/arms/flagoff" "$B/gated/flagoff/res.tsv" \
    "$B/gated/flagoff/rep" "$B/gated/flagoff/log" > "$B/gated/flagoff/run.log" 2>&1
echo "GATED flagoff done $(date -u +%H:%M:%SZ)"
export SEEDS=19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36
for arm in bots/_v516teardown "$B/arms/parent515" "$B/arms/flagoff"; do
  n="d2_$(basename "$arm")"
  mkdir -p "$B/gated/$n"
  .venv/bin/python "$B/run_grid.py" "$arm" "$B/gated/$n/res.tsv" \
      "$B/gated/$n/rep" "$B/gated/$n/log" > "$B/gated/$n/run.log" 2>&1
  echo "GATED $n done $(date -u +%H:%M:%SZ)"
done
echo "GATED2 DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
