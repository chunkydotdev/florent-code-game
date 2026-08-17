#!/bin/zsh
# s48 BUILDER demo battery: one arm against the base, on rotating maps, both
# seats, with a BASE-vs-BASE control run on the SAME map and seed.
#
# WHY THE CONTROL RUN.  Comparing the arm's seat against the base's seat inside
# ONE game is not a comparison: measured base-vs-base on yulerune seed 1, seat A
# oscillated on 18.4% of its moves and seat B on 41.3% with identical code, so
# the seat effect is larger than anything a plank is expected to move. The
# control gives each treatment cell a same-seat, same-map, same-seed reference.
#
# Usage: zsh scratchpad/s48_demo_battery.sh <arm> [maps...]
set -u
ARM=${1:?arm bot dir name}
shift
BASE=_v468kladturbo
if (( $# )); then MAPS=($@); else MAPS=(yulerune icefloe drumlin eider); fi
SEEDS=(11 22)
PY=.venv/bin/python

for m in $MAPS; do
  for s in $SEEDS; do
    echo "### control $m seed=$s (base vs base)"
    $PY scratchpad/s48_eco_demo.py $BASE $BASE maps/$m.map26 --seed $s \
        --replay /tmp/s48_ctl_${m}_${s}.replay26 2>&1 | grep -v '^Update'
    echo "### treat  $m seed=$s (arm seat A)"
    $PY scratchpad/s48_eco_demo.py $ARM $BASE maps/$m.map26 --seed $s \
        --replay /tmp/s48_trA_${m}_${s}.replay26 2>&1 | grep -v '^Update'
    echo "### treat  $m seed=$s (arm seat B)"
    $PY scratchpad/s48_eco_demo.py $BASE $ARM maps/$m.map26 --seed $s \
        --replay /tmp/s48_trB_${m}_${s}.replay26 2>&1 | grep -v '^Update'
  done
done
