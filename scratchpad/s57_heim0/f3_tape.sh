#!/bin/zsh
# s57 F3 TAPE RUNNER -- VERBATIM scratchpad/s54_v620/tape.sh with ONE addition:
# the f3 fixture case.  Same maps, same seats, same seeds, same --tle, same
# concurrency, so an f1/f2 arm run through this script MUST reproduce the
# s54_v620 tape cell for cell.  (In-game league fixture work; nothing here
# runs outside the game engine.)
#   F1 = NOISE_OFF `_v542wave` copy   (INCUMBENT VERDICT SURFACE; v613 ships
#        reading 14 kills / by-r300 12 here)
#   F2 = NOISE_OFF Mjolnir copy       (TRANSFER GUARD; v613 reads 7/30)
#   F3 = NOISE_OFF Sleipnir-v2 copy   (RUSH CLASS; bots/_v488beltbreak2,
#        platform v159, corpus/version_trees.tsv:93 -- our own retired rush
#        line, added s57 as the fast-checkmate sparring partner)
# ⛔ FIXTURE RULE: both bots are DETERMINISTIC and the maps are fixed, so the
# SEED IS INERT -- vary MAP and SEAT, never the seed.
#   usage: f3_tape.sh <f1|f2|f3> <candidate-tree> <out-dir>
set -u
cd /Users/junghard/Projects/Work/florent-code-game
FC=.venv/bin/fcode
FIX=${1:?f1|f2|f3}
CAND=${2:?candidate tree}
OUT=${3:?output dir}
case $FIX in
  f1) OPP=scratchpad/s54_fidtape/opp_v542wave_noiseoff;  SEED=7 ;;
  f2) OPP=scratchpad/s54_fidtape/opp_mjolnir_noiseoff;   SEED=11 ;;
  f3) OPP=scratchpad/s54_fidtape/opp_sleipnir2_noiseoff; SEED=7 ;;
  *)  echo "unknown fixture $FIX"; exit 2 ;;
esac
rm -rf $CAND/__pycache__ $OPP/__pycache__
rm -rf $OUT && mkdir -p $OUT
MAPS=(auroraveil bifrost fimbulwinter glacierkeep helheim holmgang icefloe \
      jotunheim longhouse midgard paths skald stavkirke valkyrie yggdrasil)
i=0
for M in $MAPS; do
  for S in A B; do
    if [[ $S == A ]]; then P1=$CAND; P2=$OPP; else P1=$OPP; P2=$CAND; fi
    timeout 600 $FC run $P1 $P2 maps/$M.map26 --seed $SEED --tle 10 \
        --replay $OUT/${M}_seat${S}.replay26 > $OUT/${M}_seat${S}.log 2>&1 &
    i=$((i+1))
    (( i % 5 == 0 )) && wait
  done
done
wait
echo "TAPE $FIX DONE $(ls $OUT/*.replay26 2>/dev/null | wc -l | tr -d ' ')/30  -> $OUT"
grep -l -i "Traceback" $OUT/*.log 2>/dev/null && echo "!! TRACEBACKS ABOVE" || echo "0 tracebacks"
