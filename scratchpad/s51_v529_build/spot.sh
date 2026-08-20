#!/bin/bash
# v529 MECHANISM SPOT-CHECK: does each lineage's mechanism still FIRE inside
# the union?  Composition can silently kill a mechanism through shared instance
# state, an import-order effect, or a predicate the sibling widened.
#
# 5 arms x 12 games (3 siege maps x 2 seeds x 2 seats), stderr KEPT.
#   inst_v529    the union, both lineages live + both tapes
#   inst_527     `_v527collar` as fired + its tape        (v527 reference)
#   inst_528     `_v528eco`    as fired + its tape        (v528 reference)
#   inst_ctl527  union with BUNKER/PSURV/SEALPATH OFF     (v527 counters -> 0)
#   inst_ctl528  union with CONNCOST OFF                  (regret -> nonzero)
# The last two are the drive-to-the-other-verdict controls, IN THE UNION: a
# counter that is nonzero everywhere and a regret that is zero everywhere would
# both be constants, and a constant column validates anything.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v529_build
O=$B/spot
mkdir -p $O
FC=.venv/bin/fcode
OPP=bots/_v488beltbreak2
run_one() {
  arm=$1; mp=$2; sd=$3; seat=$4
  tag="${arm}_${mp}_s${sd}_${seat}"
  if [ "$seat" = "A" ]; then A=$B/$arm; Bo=$OPP; else A=$OPP; Bo=$B/$arm; fi
  $FC run $A $Bo maps/$mp.map26 --seed $sd --tle 10 \
      --replay $O/$tag.replay26 > $O/$tag.out 2> $O/$tag.err
}
export -f run_one
N=0
for mp in atoll drakkarfjord glacierkeep; do
  for sd in 901 902; do
    for seat in A B; do
      for arm in inst_v529 inst_527 inst_528 inst_ctl527 inst_ctl528; do
        run_one $arm $mp $sd $seat &
        N=$((N+1))
        if [ $((N % 4)) -eq 0 ]; then wait; fi
      done
    done
  done
done
wait
echo "SPOT DONE $N games $(date -u +%Y-%m-%dT%H:%M:%SZ)"
