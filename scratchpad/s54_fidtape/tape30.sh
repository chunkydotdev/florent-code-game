#!/bin/zsh
# s54 SKALMAN v1 phase-1 fidelity tape: canonical bots/_v600skalman1 (seat A) vs the
# NOISE_OFF _v542wave copy, 15 rotated-pool maps x seeds 11,12, replays saved.
# Gate: CLEARED 2026-08-21 ~17:35Z with --allow-self-play typed (fidelity, not field).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
FC=.venv/bin/fcode
BASE=scratchpad/s54_fidtape
OPP=$BASE/opp_v542wave_noiseoff
OUT=$BASE/replays_tape30
mkdir -p $OUT
POOL=(auroraveil bifrost fimbulwinter glacierkeep helheim holmgang icefloe jotunheim longhouse midgard paths skald stavkirke valkyrie yggdrasil)
run_one() {
  local M=$1 S=$2
  local R=$OUT/${M}_s${S}.replay26
  timeout 240 $FC run bots/_v600skalman1 $OPP maps/$M.map26 --seed $S --tle 10 --replay $R \
    > $BASE/tape30_${M}_s${S}.log 2>&1
  echo "$M s$S exit=$? replay=$([ -s $R ] && echo ok || echo MISSING)"
}
# 5-way parallelism, PIDs recorded (kill-by-PID rule)
i=0
for M in $POOL; do for S in 11 12; do
  run_one $M $S &
  echo $! >> $BASE/tape30.pids
  i=$((i+1))
  if (( i % 5 == 0 )); then wait; fi
done; done
wait
echo TAPE30 DONE $(ls $OUT | wc -l | tr -d ' ')/30 replays
