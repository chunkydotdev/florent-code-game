#!/bin/zsh
# v603 FULL TAPE -- the SAME fixture as the tape602 autopsy: 15 pool maps x both
# seats = 30 games vs the NOISE_OFF `_v542wave` copy.  ⛔ FIXTURE RULE: both bots
# are DETERMINISTIC and the maps are fixed, so the SEED is inert -- vary MAP and
# SEAT, never the seed.
#   usage: tape.sh <candidate-tree> <out-dir>
set -u
cd /Users/junghard/Projects/Work/florent-code-game
FC=.venv/bin/fcode
OPP=scratchpad/s54_fidtape/opp_v542wave_noiseoff
CAND=${1:?candidate tree}
OUT=${2:?output dir}
rm -rf $CAND/__pycache__ $OPP/__pycache__
rm -rf $OUT && mkdir -p $OUT
MAPS=(auroraveil bifrost fimbulwinter glacierkeep helheim holmgang icefloe \
      jotunheim longhouse midgard paths skald stavkirke valkyrie yggdrasil)
for M in $MAPS; do
  for S in A B; do
    if [[ $S == A ]]; then P1=$CAND; P2=$OPP; else P1=$OPP; P2=$CAND; fi
    timeout 600 $FC run $P1 $P2 maps/$M.map26 --seed 7 --tle 10 \
        --replay $OUT/${M}_seat${S}.replay26 > $OUT/${M}_seat${S}.log 2>&1
    [[ $? -eq 0 ]] || echo "  !! $M seat$S exit=$?"
  done
done
echo "TAPE DONE $(ls $OUT/*.replay26 2>/dev/null | wc -l | tr -d ' ')/30  -> $OUT"
grep -l -i "Traceback" $OUT/*.log 2>/dev/null && echo "!! TRACEBACKS ABOVE" || echo "0 tracebacks"
