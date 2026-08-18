#!/bin/bash
# FS_CREW_CONVERT measurement, s51 2026-08-18.
# CARRIER = fired v515 config, unchanged (verified safe, no slot collision).
# CREWCONV = fired config with FS_CREW_ON/FS_CREW_CONVERT flipped True AT
#   THEIR OWN DEFINITION SITES (doctrine.py:2741, doctrine.py:2755) in the
#   copied tree -- NOT via mkarm.sh append -- so FERRY_HOME_ON (doctrine.py:
#   3011-3012) and every other downstream derived default evaluate with the
#   intended values at import.  Readback confirmed clean before this script
#   was written: FERRY_HOME_ON=False, COLLISION=False
#   (scratchpad/s51_crewconv/check_slots_rebuilt.out).
#
# 5 siege maps x 6 reps/block x 15 blocks = 450 games/arm, both arms
# interleaved within each block/seed (the v515 report's method: same-block
# interleaving is the variance control -- drive_headline.sh/drive_final.sh
# convention, reused here unchanged).
set -e
cd /Users/junghard/Projects/Work/florent-code-game
S=scratchpad/s51_v515_build
O=scratchpad/s51_crewconv
export PAR=4
for blk in A:9400 B:9500 C:9600 D:9700 E:9800 F:9900 G:10000 H:10100 I:10200 \
           J:10300 K:10400 L:10500 M:10600 N:10700 O:10800; do
  L=${blk%%:*}; SEED=${blk##*:}
  for arm in CARRIER CREWCONV; do
    .venv/bin/python $S/run_grid.py $S/arms/$arm ${arm}${L} \
      $O/grid/${arm}${L}.tsv 6 $SEED - > $O/grid/${arm}${L}.log 2>&1
  done
  echo "block $L done"
done
echo MEASUREDONE > $O/grid/measure.run
