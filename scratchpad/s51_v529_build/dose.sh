#!/bin/bash
# v529 DOSE + M2-SIGNATURE battery.  v527's own design (§5e/§5f): 8 maps x 3
# seeds, NOISE_ON=True, `--tle 10`, stderr kept -- x 2 seats = 48 games/arm.
#   dose_v529    the union (both tapes)
#   dose_527     `_v527collar` as fired (+ SEALNT tape)
#   dose_528     `_v528eco`    as fired (+ both tapes)
#   dose_parent  RDV-only parent (+ SEALNT tape) -- the M2 reference row
#   dose_ctl527  union, BUNKER/PSURV/SEALPATH off -- v527 counters must go to 0
#   dose_ctl528  union, CONNCOST off             -- regret must go nonzero
# ⚠ NOISE_ON=True re-rolls the spawn salt per PROCESS, so these counts are
# MAGNITUDES, not constants (v527 read BUNKER FIRE 5/3/2 on three runs of the
# same cells).  Reported as such.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v529_build
O=$B/dose
mkdir -p $O
FC=.venv/bin/fcode
OPP=bots/_v488beltbreak2
N=0
for mp in atoll drakkarfjord glacierkeep nordkap yulerune antler fjordgate midgard; do
  for sd in 301 302 303; do
    for seat in A B; do
      for arm in dose_v529 dose_527 dose_528 dose_parent dose_ctl527 dose_ctl528; do
        tag="${arm}_${mp}_s${sd}_${seat}"
        if [ "$seat" = "A" ]; then A=$B/$arm; Bo=$OPP; else A=$OPP; Bo=$B/$arm; fi
        $FC run $A $Bo maps/$mp.map26 --seed $sd --tle 10 \
            --replay $O/$tag.replay26 > $O/$tag.out 2> $O/$tag.err &
        N=$((N+1))
        if [ $((N % 4)) -eq 0 ]; then wait; fi
      done
    done
  done
done
wait
echo "DOSE DONE $N games $(date -u +%Y-%m-%dT%H:%M:%SZ)"
