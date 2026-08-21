#!/bin/zsh
# v601 local battery.  ⛔ FIXTURE RULE (tape30 autopsy §0.4): both bots are
# DETERMINISTIC and the maps are fixed, so the SEED only perturbs
# resource-move ordering -- every *_s11/_s12 pair in the tape was
# byte-identical.  Vary the MAP and the SEAT, never the seed.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
FC=.venv/bin/fcode
OPP=scratchpad/s54_fidtape/opp_v542wave_noiseoff
CAND=${1:?candidate tree}
OUT=${2:?output dir}
rm -rf $CAND/__pycache__ $OPP/__pycache__
mkdir -p $OUT
# 6 DIFFERENT pool maps; seats alternate so both are represented.
# 3 of the 6 (fimbulwinter, holmgang, paths) built ZERO harvesters in the tape.
MAPS=(fimbulwinter holmgang paths icefloe midgard yggdrasil)
SEATS=(A B A B A B)
i=1
for M in $MAPS; do
  S=$SEATS[$i]
  if [[ $S == A ]]; then P1=$CAND; P2=$OPP; else P1=$OPP; P2=$CAND; fi
  timeout 300 $FC run $P1 $P2 maps/$M.map26 --seed 7 --tle 10 \
      --replay $OUT/${M}_seat${S}.replay26 > $OUT/${M}_seat${S}.log 2>&1
  echo "$M seat$S exit=$?"
  i=$((i+1))
done
echo BATTERY DONE $(ls $OUT/*.replay26 2>/dev/null | wc -l | tr -d ' ')/6
