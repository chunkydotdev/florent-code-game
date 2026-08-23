#!/bin/zsh
# nb1build mutctl RETRY on DENSE cells (multi-tube per the battery study):
# the aurA/helA cells never consult pair spacing (single-tube games) — the
# X1+tight=0 DIFF must be driven where a second plant actually happens.
# GAME CONTEXT: local in-game fixture runs, Florent Code League.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
FC=.venv/bin/fcode
H=scratchpad/s57_heim0
OUT=$H/nb1build_mut2
rm -rf $OUT; mkdir -p $OUT
F1=scratchpad/s54_fidtape/opp_v542wave_noiseoff
F3=scratchpad/s54_fidtape/opp_sleipnir2_noiseoff
run() {
  local TREE=$1 TAG=$2 M=$3 S=$4 OPP=$5 SEED=$6 REF=$7 EXP=$8
  rm -rf $TREE/__pycache__ $OPP/__pycache__
  local P1 P2
  if [[ $S == A ]]; then P1=$TREE; P2=$OPP; else P1=$OPP; P2=$TREE; fi
  timeout 600 $FC run $P1 $P2 maps/$M.map26 --seed $SEED --tle 10 \
     --replay $OUT/${TAG}.replay26 > $OUT/${TAG}.log 2> $OUT/${TAG}.err
  local A=$(md5 -q $OUT/${TAG}.replay26)
  local B=$(md5 -q $H/$REF/${M}_seat${S}.replay26)
  local V; if [[ $A == $B ]]; then V=SAME; else V=DIFF; fi
  if [[ $V == $EXP ]]; then echo "  ok   $TAG  $V (expected $EXP)"
  else echo "  FAIL $TAG  $V (expected $EXP)"; fi
}
echo "X1 + tight=0 on DENSE cells -- expect DIFF on at least one"
run $H/nb1build_mutX1_off x1off_f1_fimA fimbulwinter A $F1 7 t_b4_f1 DIFF
run $H/nb1build_mutX1_off x1off_f1_holB holmgang     B $F1 7 t_b4_f1 DIFF
run $H/nb1build_mutX1_off x1off_f3_ygyA yggdrasil    A $F3 7 t_b4_f3 DIFF
echo "X1 + tight=1 on the same dense cells -- expect SAME"
run $H/nb1build_mutX1_on  x1on_f1_fimA  fimbulwinter A $F1 7 t_b4_f1 SAME
run $H/nb1build_mutX1_on  x1on_f3_ygyA  yggdrasil    A $F3 7 t_b4_f3 SAME
