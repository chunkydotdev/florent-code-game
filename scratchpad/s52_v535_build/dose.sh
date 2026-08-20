#!/bin/bash
# v535 DOSE / MECHANISM battery.  4 maps x 3 seeds x 2 seats = 24 games/arm.
#
# THE QUESTION, and it has to be answerable BOTH WAYS or it is not a dose:
#   * on a REFUSING board (archipelago, midgard) v535 must build ZERO corners
#     while the parent builds its usual handful;
#   * on a SIEGE-ACTIVE board (glacierkeep, ragnarok) the two arms must be
#     INDISTINGUISHABLE -- same corner count, game for game.
# The second half is the positive control: an arm that built no corners
# anywhere would pass the first half and be a different (broken) bot.
#
# ⛔ NOISE_ON = False ON BOTH ARMS, DELIBERATELY.  With the noise salt frozen a
# game is a pure function of (arms, map, seed, seat), so on the running boards
# the two arms' per-game corner counts must match EXACTLY, not merely on
# average.  The opponent is NOISE_OFF too -- the v534 lesson: a determinism
# fixture with a noisy opponent is not a determinism fixture.
#
# ⛔ LOCAL ONLY, AND THAT IS FORCED: `tools/remote_battery.py` returns no
# per-game stderr, and the corner counter IS a stderr tape (FS_V530_LOG).
# Run only once scratchpad/overnight/HOMEPOOL.tsv has its 5,400 data rows.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s52_v535_build
MAPS_REFUSE="archipelago midgard"
MAPS_RUN="glacierkeep ragnarok"
SEEDS="5351 5352 5353"
OPP=$B/arms/opp_off
for arm in dose_par dose_v535; do
  mkdir -p $B/dose/$arm
  for m in $MAPS_REFUSE $MAPS_RUN; do
    for s in $SEEDS; do
      for seat in A B; do
        if [ $seat = A ]; then P1=$B/arms/$arm; P2=$OPP; else P1=$OPP; P2=$B/arms/$arm; fi
        .venv/bin/fcode run $P1 $P2 maps/$m.map26 --seed $s --tle 10 \
          --replay $B/dose/$arm/${m}_${s}_${seat}.rep \
          > $B/dose/$arm/${m}_${s}_${seat}.out \
          2> $B/dose/$arm/${m}_${s}_${seat}.err &
        while [ "$(jobs -rp | wc -l)" -ge 3 ]; do wait -n; done
      done
    done
  done
  wait
  echo "DOSE $arm done $(date -u +%H:%M:%SZ)"
done
echo "DOSE ALL DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
