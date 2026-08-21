#!/bin/zsh
# v601 per-plank ablation: one flag flipped per arm, 3 games, same 3 maps/seats
# as the control subset.  Canonical bots/ trees are NEVER edited -- each arm is a
# scratchpad COPY with exactly one sed, and the flip is verified BY IMPORT
# (reading the assignment back would not catch an append-time override).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
FC=.venv/bin/fcode
OPP=scratchpad/s54_fidtape/opp_v542wave_noiseoff
BASE=scratchpad/s54_v601
MAPS=(midgard icefloe yggdrasil)
SEATS=(A B B)

arm() {
  local NAME=$1 FLAG=$2
  local DIR=$BASE/arm_$NAME
  rm -rf $DIR $BASE/rep_$NAME
  cp -r bots/_v601skalman $DIR
  rm -rf $DIR/__pycache__
  sed -i '' "s/^$FLAG = True/$FLAG = False/" $DIR/sk_maps.py
  .venv/bin/python -c "
import sys; sys.path.insert(0, '$DIR')
import sk_maps
assert sk_maps.$FLAG is False, '$FLAG flip did not take'
for f in ('SK_HARV_ESCALATE','SK_BELT_COVER','SK_TARGET_PRIO','SK_ORE_SENSE'):
    if f != '$FLAG':
        assert getattr(sk_maps, f) is True, f + ' should still be True'
print('  arm $NAME ok: $FLAG=False, the other three True')" || exit 1
  mkdir -p $BASE/rep_$NAME
  local i=1
  for M in $MAPS; do
    local S=$SEATS[$i]
    if [[ $S == A ]]; then P1=$DIR; P2=$OPP; else P1=$OPP; P2=$DIR; fi
    timeout 300 $FC run $P1 $P2 maps/$M.map26 --seed 7 --tle 10 \
        --replay $BASE/rep_$NAME/${M}_seat${S}.replay26 \
        > $BASE/rep_$NAME/${M}_seat${S}.log 2>&1
    echo "  $NAME $M seat$S exit=$?"
    i=$((i+1))
  done
}

arm harv_off SK_HARV_ESCALATE
arm cover_off SK_BELT_COVER
arm prio_off SK_TARGET_PRIO
arm ore_off SK_ORE_SENSE
echo ABLATE3 DONE
