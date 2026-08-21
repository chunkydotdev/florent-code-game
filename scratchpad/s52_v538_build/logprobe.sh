#!/bin/bash
# v538 build instrument #7 -- THE DIRECT ENGINE-SIDE DOSE READ, both verdicts.
# The tape is STDERR from a live game, not our own replay stdout (CLAUDE.md:
# print() is stripped from platform replays; locally stderr is real).
#   archipelago (REFUSES): v538 must print V538GATE refuse=1 and ZERO
#       "V537 SOCKET" lines, while the parent prints socket claims.
#   nordkap (RUNS):        v538 must print V538GATE refuse=0 and the SAME
#       number of socket claims as the parent.
# A one-sided probe would prove nothing; both maps are read for both arms.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s52_v538_build
for mp in archipelago nordkap; do
  for arm in logpar logv538; do
    .venv/bin/fcode run $B/arms/$arm bots/_x3r0v169mjolnir maps/$mp.map26 \
      --seed 1 --tle 10 2> $B/log_${arm}_${mp}.err > /dev/null
    g=$(grep -c "V538GATE" $B/log_${arm}_${mp}.err || true)
    r1=$(grep -m1 "V538GATE" $B/log_${arm}_${mp}.err || true)
    s=$(grep -c "V537 SOCKET" $B/log_${arm}_${mp}.err || true)
    echo "$mp $arm  V538GATE_lines=$g  first='$r1'  V537_SOCKET_claims=$s"
  done
done
