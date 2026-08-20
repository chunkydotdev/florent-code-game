#!/bin/bash
# v530 DOSE / MECHANISM battery.  8 maps x 3 seeds x 2 seats = 48 games/arm,
# NOISE_ON=True, --tle 10, stderr KEPT.  The question is only "does each plank
# fire, and does its own ablation drive the counter to the other verdict" --
# magnitudes, not constants (NOISE_ON re-rolls the spawn salt per process).
#
# ARMS, and every one of them is the SAME TREE with one sub-flag moved, so the
# tape comes from one instrument:
#   inst_v530     all three planks on, log on          <- the dose
#   inst_nomouth  P1 off                               <- MOUTH must go to 0
#   inst_nocorner P2 off                               <- CORNER must go to 0
#   inst_nodoor   P3 off                               <- DOORKILL must go to 0
#   inst_ring     P1b ON (it is OFF in the fired tree) <- RING must go NONZERO
#   inst_flagoff  master off                           <- ALL must go to 0
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v530_build
MAPS="atoll drakkarfjord glacierkeep nordkap yulerune icefloe auroraveil antler"
SEEDS="5301 5302 5303"
OPP=${OPP:-bots/_v488beltbreak2}
for arm in inst_v530 inst_nomouth inst_nocorner inst_nodoor inst_ring inst_flagoff; do
  mkdir -p $B/dose/$arm
  for m in $MAPS; do
    for s in $SEEDS; do
      for seat in A B; do
        if [ $seat = A ]; then P1=$B/$arm; P2=$OPP; else P1=$OPP; P2=$B/$arm; fi
        .venv/bin/fcode run $P1 $P2 maps/$m.map26 --seed $s --tle 10 \
          > $B/dose/$arm/${m}_${s}_${seat}.out \
          2> $B/dose/$arm/${m}_${s}_${seat}.err &
        while [ "$(jobs -rp | wc -l)" -ge 4 ]; do wait -n; done
      done
    done
  done
  wait
  echo "DOSE $arm done $(date -u +%H:%M:%SZ)"
done
echo "DOSE ALL DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
