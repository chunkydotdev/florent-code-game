#!/bin/bash
# v530.1 DOSE.  The MECHANISM check for the fix, not a currency read.
# 8 maps x 3 seeds x 2 seats = 48 games/arm, NOISE_ON=True, --tle 10, stderr
# KEPT.  ⚠ NOISE_ON=True re-rolls the spawn salt per process, so these are
# MAGNITUDES, not constants.
#
# TWO ARMS, the SAME TREE with ONE FLAG moved:
#   inst_v530  = _v530home  + FS_V530_LOG   -- mouth chains armed on EVERY eco
#                                              seat, which is the defect
#   inst_v531  = _v531fix   + FS_V530_LOG   -- the same tapes; the claim is that
#                                              non-designated seats no longer
#                                              arm EARLY, not that they never arm
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v5301_build
MAPS="atoll drakkarfjord glacierkeep nordkap yulerune icefloe auroraveil antler"
SEEDS="5311 5312 5313"
OPP=${OPP:-bots/_v488beltbreak2}
for arm in inst_v530 inst_v531; do
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
