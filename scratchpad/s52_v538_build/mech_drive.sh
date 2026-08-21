#!/bin/bash
# s52 v538 MECHANISM TEST vs the LIVE holder tree bots/_x3r0v169mjolnir.
# THREE arms INTERLEAVED (run_battery.py puts all arms of one cell adjacent, so
# they share the same wall-clock slice -- v518 finding 2 measured a 4.6pp FALSE
# POSITIVE from pooling non-time-adjacent local fixtures), in blocks of 5 seeds
# so the tape is also spread across time rather than run arm-block by arm-block.
#   archipelago : the DECISIVE cell.  v537's full-pool screen read 8/60 there
#       against v536's 35/60.  PREDICTION: v538 recovers toward v536.
#   yulerune, glacierkeep : the FALSIFIER cells.  Both RUN the siege, so the
#       gate must not touch them; v537's socket gains there must HOLD.
# 3 maps x 30 seeds x 2 seats x 3 arms = 540 games.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
export PAR=4
export OUT=scratchpad/s52_v538_build/mech
export OPP=$PWD/bots/_x3r0v169mjolnir
export ARMS="v538refine=bots/_v538refine,v537socket=bots/_v537socket,v536trust=bots/_v536trustport"
export MAPS=archipelago,yulerune,glacierkeep
echo "MECH START $(date -u +%Y-%m-%dT%H:%M:%SZ)"
for i in 1 2 3 4 5 6; do
  a=$(( (i-1)*5 + 1 )); b=$(( i*5 ))
  # ⛔ NOT `seq -s,` -- BSD seq APPENDS the separator after the last element
  # (verified: `seq -s, 1 5` emits `1,2,3,4,5,`), which run_battery.py parses
  # as an empty seed and dies on int(''). The first run of this script did
  # exactly that and reported all six blocks "done" in under a second.
  export SEEDS=$(python3 -c "print(','.join(str(x) for x in range($a, $b+1)))")
  .venv/bin/python3 scratchpad/s51_v5301_build/run_battery.py
  echo "  MECH BLOCK $i (seeds $a-$b) done $(date -u +%H:%M:%SZ)"
done
echo "MECH DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
