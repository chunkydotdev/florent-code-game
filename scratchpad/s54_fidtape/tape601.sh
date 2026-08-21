#!/bin/zsh
# s54 v601 fidelity tape: bots/_v601skalman vs NOISE_OFF _v542wave copy,
# 15 pool maps x BOTH SEATS = 30 distinct games (seed fixed 11 — the seed axis is inert
# for a deterministic pair; seat is the second axis per the corrected fixture rule).
# Gate: the 17:35Z CLEARED run covers the fixture (same control/opponent/self-play escape);
# plank tree bots/_v601skalman is on-line (_v[2-9]??* matches).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
FC=.venv/bin/fcode
BASE=scratchpad/s54_fidtape
OPP=$BASE/opp_v542wave_noiseoff
OUT=$BASE/replays_tape601
mkdir -p $OUT
POOL=(auroraveil bifrost fimbulwinter glacierkeep helheim holmgang icefloe jotunheim longhouse midgard paths skald stavkirke valkyrie yggdrasil)
run_one() {
  local M=$1 SEAT=$2
  local R=$OUT/${M}_${SEAT}.replay26
  if [[ $SEAT == A ]]; then
    timeout 240 $FC run bots/_v601skalman $OPP maps/$M.map26 --seed 11 --tle 10 --replay $R > $BASE/tape601_${M}_${SEAT}.log 2>&1
  else
    timeout 240 $FC run $OPP bots/_v601skalman maps/$M.map26 --seed 11 --tle 10 --replay $R > $BASE/tape601_${M}_${SEAT}.log 2>&1
  fi
  echo "$M $SEAT exit=$? replay=$([ -s $R ] && echo ok || echo MISSING)"
}
i=0
for M in $POOL; do for SEAT in A B; do
  run_one $M $SEAT &
  echo $! >> $BASE/tape601.pids
  i=$((i+1))
  if (( i % 5 == 0 )); then wait; fi
done; done
wait
echo TAPE601 DONE $(ls $OUT | wc -l | tr -d ' ')/30 replays
