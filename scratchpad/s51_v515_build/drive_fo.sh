#!/bin/bash
# FLAG-OFF BEHAVIOURAL CONTROL, in-session and concurrent: the v515 tree with
# LOKI_FS_V515 = False against an UNMODIFIED COPY of the parent tree, same
# seeds, same session, same PAR.  This removes the cross-session confound that
# made the earlier flag-off comparison (v515 flagoff 46/90 vs the v514 build's
# banked 36-39/90 on identical seeds) unreadable.
set -e
cd /Users/junghard/Projects/Work/florent-code-game
S=scratchpad/s51_v515_build
export PAR=4
for blk in A:7400 B:7500 C:7600 D:7700 E:7800 F:7900 G:8200 H:8300 I:8400; do
  L=${blk%%:*}; SEED=${blk##*:}
  .venv/bin/python $S/run_grid.py $S/arms/parent514 parent514${L} \
    $S/grid/parent514${L}.tsv 6 $SEED - > $S/grid/parent514${L}.log 2>&1
done
echo FODONE > $S/grid/fo.run
