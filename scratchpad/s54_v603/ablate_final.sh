#!/bin/zsh
# v603 FINAL per-flag ablation, on the FINAL chassis (FIX 6 included).
# ⛔ RE-RUN, NOT REUSED: the v602 build report measured a flag whose ablation
# went NULL once the chassis around it was fixed, so an ablation taken on an
# earlier chassis is not evidence about the shipped one.
# ⛔ EVERY FLIP IS VERIFIED BY IMPORT, never by reading the assignment.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
BASE=scratchpad/s54_v603
for ARM in nestpair_off trunknear_off evict_off collar_off ceil_on \
           lapadj_off idleact_off spawnexit_off routegate_on homedef_on; do
  TREE=$BASE/farm_$ARM
  rm -rf $TREE && cp -r bots/_v603skalman $TREE && rm -rf $TREE/__pycache__
  case $ARM in
    nestpair_off)   sed -i '' 's/^SK_NEST_PAIR = True/SK_NEST_PAIR = False/'         $TREE/sk_maps.py ;;
    trunknear_off)  sed -i '' 's/^SK_TRUNK_NEAR = True/SK_TRUNK_NEAR = False/'       $TREE/sk_maps.py ;;
    evict_off)      sed -i '' 's/^SK_EVICT_ARMED = True/SK_EVICT_ARMED = False/'     $TREE/sk_maps.py ;;
    collar_off)     sed -i '' 's/^SK_COLLAR_GUNS = True/SK_COLLAR_GUNS = False/'     $TREE/sk_maps.py ;;
    ceil_on)        sed -i '' 's/^SK_CAGE_CEIL = False/SK_CAGE_CEIL = True/'         $TREE/sk_maps.py ;;
    routegate_on)   sed -i '' 's/^SK_COLLAR_ROUTE_GATE = False/SK_COLLAR_ROUTE_GATE = True/' $TREE/sk_maps.py ;;
    homedef_on)     sed -i '' 's/^SK_HOMEDEF_SKIP_BARRIER = True/SK_HOMEDEF_SKIP_BARRIER = False/' $TREE/sk_maps.py ;;
    lapadj_off)     sed -i '' 's/^SK_LAP_ADJ_SEAL = True/SK_LAP_ADJ_SEAL = False/'   $TREE/sk_maps.py ;;
    idleact_off)    sed -i '' 's/^SK_IDLE_ACT = True/SK_IDLE_ACT = False/'           $TREE/sk_maps.py ;;
    spawnexit_off)  sed -i '' 's/^SK_SPAWN_EXIT = True/SK_SPAWN_EXIT = False/'       $TREE/sk_maps.py ;;
  esac
  .venv/bin/python -c "
import sys; sys.path.insert(0, '$TREE')
import sk_maps
print('$ARM effective:', sk_maps.SK_NEST_PAIR, sk_maps.SK_TRUNK_NEAR,
      sk_maps.SK_EVICT_ARMED, sk_maps.SK_COLLAR_GUNS, sk_maps.SK_CAGE_CEIL,
      sk_maps.SK_LAP_ADJ_SEAL, sk_maps.SK_IDLE_ACT, sk_maps.SK_SPAWN_EXIT,
      sk_maps.SK_COLLAR_ROUTE_GATE, sk_maps.SK_HOMEDEF_SKIP_BARRIER)"
  ./$BASE/tape.sh $TREE $BASE/ftape_$ARM | tail -2
done
echo FINAL ABLATION DONE
