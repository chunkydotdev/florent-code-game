#!/bin/bash
# Everything after the headline: mechanism arms (stderr captured, no replays),
# the gated archipelago read, and the flag-off behavioural grid.
set -e
cd /Users/junghard/Projects/Work/florent-code-game
S=scratchpad/s51_v515_build
export PAR=4

# --- mechanism: 5 siege maps x 3 reps = 15 games/arm, stderr kept ------------
export NOREPLAY=1
for arm in m_door m_dooron m_gate m_gate0 m_reach m_reachoff; do
  .venv/bin/python $S/run_grid.py $S/arms/$arm $arm \
    $S/grid/$arm.tsv 3 7400 $S/logs/$arm > $S/grid/$arm.log 2>&1
  echo "done $arm"
done
unset NOREPLAY

# --- gated read: archipelago (the plank never runs), vs _v468kladturbo -------
export MAPS=archipelago
export OPP=/Users/junghard/Projects/Work/florent-code-game/bots/_v468kladturbo
for arm in v515 p514nd; do
  .venv/bin/python $S/run_grid.py $S/arms/$arm gk_$arm \
    $S/grid/gk_$arm.tsv 36 8100 - > $S/grid/gk_$arm.log 2>&1
  echo "done gk_$arm"
done
unset MAPS OPP

# --- flag-off behavioural, n=60 on the parent's own block A+B seeds ----------
for blk in A:7400 B:7500; do
  L=${blk%%:*}; SEED=${blk##*:}
  .venv/bin/python $S/run_grid.py $S/arms/flagoff flagoff$L \
    $S/grid/flagoff$L.tsv 6 $SEED - > $S/grid/flagoff$L.log 2>&1
  echo "done flagoff$L"
done
echo RESTDONE > $S/grid/rest.run

# --- HEADLINE RE-DRAW, fresh seeds, both arms concurrent ---------------------
# The one-draw law: the block above is ONE draw of a fixture whose measured
# same-config swing is up to 10 games in 30.  This is the second draw.
for blk in D:7700 E:7800 F:7900; do
  L=${blk%%:*}; SEED=${blk##*:}
  for arm in v515 p514nd; do
    .venv/bin/python $S/run_grid.py $S/arms/$arm ${arm}${L} \
      $S/grid/${arm}${L}.tsv 6 $SEED - > $S/grid/${arm}${L}.log 2>&1
    echo "done ${arm}${L}"
  done
done
echo REDRAWDONE > $S/grid/redraw.run
