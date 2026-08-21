#!/bin/zsh
# s54 ablation completion: SK_NEST / SK_DOOR / SK_BELT / SK_ROLES (3 games each)
# + 3-game shared control. Deterministic fixture: opp copy NOISE_OFF, fixed seeds.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
FC=.venv/bin/fcode
BASE=scratchpad/s54_fidtape
OPP=$BASE/opp_v542wave_noiseoff
for ARM in control nest_off door_off belt_off roles_off; do
  TREE=$BASE/arm_$ARM
  rm -rf $TREE && cp -r bots/_v600skalman1 $TREE
  case $ARM in
    nest_off)  sed -i '' 's/^SK_NEST = True/SK_NEST = False/'   $TREE/sk_maps.py ;;
    door_off)  sed -i '' 's/^SK_DOOR = True/SK_DOOR = False/'   $TREE/sk_maps.py ;;
    belt_off)  sed -i '' 's/^SK_BELT = True/SK_BELT = False/'   $TREE/sk_maps.py ;;
    roles_off) sed -i '' 's/^SK_ROLES = True/SK_ROLES = False/' $TREE/sk_maps.py ;;
  esac
  mkdir -p $BASE/replays_$ARM
  i=0
  for M in inv_small12 atoll midgard; do
    i=$((i+1))
    OUT=$BASE/replays_$ARM/${M}.replay26
    timeout 180 $FC run $TREE $OPP maps/$M.map26 --seed $i --tle 10 --replay $OUT \
      > $BASE/run_${ARM}_${M}.log 2>&1
    echo "$ARM $M exit=$? replay=$([ -s $OUT ] && echo ok || echo MISSING)"
  done
done
echo DONE
