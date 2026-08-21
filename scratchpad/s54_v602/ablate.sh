#!/bin/zsh
# v602 per-fix ablation: one flag off per arm, 3 games each + the shared control.
# ⛔ FIXTURE RULE (tape30/tape601 autopsies): both bots are DETERMINISTIC and the
# maps are fixed, so the SEED is inert -- vary MAP and SEAT, never the seed.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
FC=.venv/bin/fcode
OPP=scratchpad/s54_fidtape/opp_v542wave_noiseoff
BASE=scratchpad/s54_v602
MAPS=(fimbulwinter glacierkeep holmgang)
SEATS=(A A B)
for ARM in control cagefirst_off danger_off cycle_off sense_off; do
  TREE=$BASE/arm_$ARM
  rm -rf $TREE && cp -r bots/_v602skalman $TREE && rm -rf $TREE/__pycache__
  case $ARM in
    cagefirst_off) sed -i '' 's/^SK_CAGE_FIRST = True/SK_CAGE_FIRST = False/' $TREE/sk_maps.py ;;
    danger_off)    sed -i '' 's/^SK_DANGER_NAV = True/SK_DANGER_NAV = False/'  $TREE/sk_maps.py ;;
    cycle_off)     sed -i '' 's/^SK_CYCLE_BREAK = True/SK_CYCLE_BREAK = False/' $TREE/sk_maps.py ;;
    sense_off)     sed -i '' 's/^SK_SENSE_NAV = True/SK_SENSE_NAV = False/'   $TREE/sk_maps.py ;;
  esac
  # ⛔ VERIFY THE FLIP BY IMPORT, not by reading the assignment.
  .venv/bin/python -c "
import sys; sys.path.insert(0, '$TREE')
import sk_maps
print('$ARM effective:', sk_maps.SK_CAGE_FIRST, sk_maps.SK_DANGER_NAV,
      sk_maps.SK_CYCLE_BREAK, sk_maps.SK_SENSE_NAV)"
  OUT=$BASE/rep_$ARM
  rm -rf $OUT && mkdir -p $OUT
  i=1
  for M in $MAPS; do
    S=$SEATS[$i]
    if [[ $S == A ]]; then P1=$TREE; P2=$OPP; else P1=$OPP; P2=$TREE; fi
    timeout 300 $FC run $P1 $P2 maps/$M.map26 --seed 7 --tle 10 \
        --replay $OUT/${M}_seat${S}.replay26 > $OUT/${M}_seat${S}.log 2>&1
    echo "  $ARM $M seat$S exit=$?"
    i=$((i+1))
  done
done
echo ABLATION DONE
