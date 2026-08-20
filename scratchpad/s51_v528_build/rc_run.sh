#!/bin/bash
# v528 MECHANISM CELL.  Two mandates read off ONE set of tapes:
#   M4 -- mid-map stalls on the wall-heavy 30x30 class, the exact fixture v526
#         used to root-cause the defect (valkyrie/glacierkeep/drakkarfjord/
#         ragnarok x 3 seeds x 2 seats = 24 games per arm).
#   M5 -- the CONN regret tape (chosen-vs-best-available connection length per
#         harvester decision), which the shipped tree emits behind FS_V528_LOG.
# ARMS, and the last one is the point:
#   inst_off   the parent (LOKI_FS_V528=False), instrumented
#   inst_walk  WALK only -- attributes the stall delta to the ONE predicate
#   inst_v528  as fired
#   inst_mut   MUTANT: the body predicate INVERTED, so the override re-targets
#              ONLY occupied ore.  Must stall MORE than the parent -- without it
#              "0 stalls" would also be produced by a scanner that cannot see.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v528_build
mkdir -p $B/rc
PAR=${PAR:-2}
run() {
  A=$1; M=$2; S=$3; SEAT=$4
  T=${A}_${M}_s${S}_${SEAT}
  if [ "$SEAT" = "A" ]; then P1=$B/$A; P2=bots/_v488beltbreak2
  else P1=bots/_v488beltbreak2; P2=$B/$A; fi
  .venv/bin/fcode run $P1 $P2 maps/$M.map26 --seed $S --tle 10 \
      > $B/rc/$T.out 2> $B/rc/$T.err
}
i=0
for M in valkyrie glacierkeep drakkarfjord ragnarok; do
  for S in 1 2 3; do
    for SEAT in A B; do
      for A in inst_off inst_walk inst_v528 inst_mut; do
        run $A $M $S $SEAT &
        i=$((i+1))
        if [ $((i % PAR)) -eq 0 ]; then wait; fi
      done
    done
  done
done
wait
echo "RC DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)  games=$i"
