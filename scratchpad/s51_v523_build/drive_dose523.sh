#!/bin/bash
# v523 DETERMINISTIC DOSE TEST -- STORE-BLIND, and the store-blind form is
# MANDATORY here rather than an improvement.
#
# ⛔⛔ THE v522 INSTRUMENT FINDING: `.replay26` SERIALISES THE TEAM'S PRIVATE
# COMMS STORE.  A clause that only writes a different number into a store slot
# scores a FULL DOSE on a replay-byte diff -- proved on v522 at 167 differing
# bytes across 5 games, every one a varint differing by exactly
# `1 << FS_PHASE_SHIFT`, files identical in length and not one game event
# changed.  v523 publishes TWO new words (a merged FS_PH_SEALED and the
# ARC-CLOSED code), so run against a plain baseline this test would be
# measuring the channel, not the behaviour.
#
#   NAIVE  parent    vs FIRED  -- reported, NOT the gate.  Channel + behaviour.
#   ⭐ BLIND storeonly vs FIRED -- THE GATE.  `FS_V523_STORE_ONLY` publishes
#      every v523 word the fired build publishes and lets NO consumer act on
#      it, so every difference here is behaviour.
#
# ⛔ AND THE DENOMINATOR IS NOT 36.  v522 measured `--seed` INERT on noise-off
# games in 11 of 12 (map, seat) cells across seeds 7/11/23 -- same winner, same
# turn, byte-identical stderr tape -- while the replay FILES still differed
# because the seed itself is serialised.  So 36 cells are ~12-14 DISTINCT
# GAMES and every count below is reported both ways.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v523_build
mkdir -p "$B/dose"
rm -rf "$B/arms/d_opp" "$B/arms/d_base" "$B/arms/d_store" "$B/arms/d_fired"
cp -R bots/_v488beltbreak2 "$B/arms/d_opp"; chmod -R u+w "$B/arms/d_opp"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/d_opp/doctrine.py"
cp -R "$B/arms/parent" "$B/arms/d_base"; chmod -R u+w "$B/arms/d_base"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/d_base/doctrine.py"
cp -R bots/_v523eyes "$B/arms/d_store"; chmod -R u+w "$B/arms/d_store"
{ echo ""; echo "FS_V523_STORE_ONLY = True"; echo "NOISE_ON = False"; } >> "$B/arms/d_store/doctrine.py"
cp -R bots/_v523eyes "$B/arms/d_fired"; chmod -R u+w "$B/arms/d_fired"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/d_fired/doctrine.py"
rm -rf "$B"/arms/d_*/__pycache__

echo "map seat seed naive blind"
for m in atoll drakkarfjord glacierkeep midgard nordkap yulerune; do
  for seed in 7 11 23; do
    for seat in A B; do
      for arm in base store fired; do
        T="$B/arms/d_$arm"
        if [ "$seat" = A ]; then F="$T"; S="$B/arms/d_opp"; else F="$B/arms/d_opp"; S="$T"; fi
        .venv/bin/fcode run "$F" "$S" "maps/$m.map26" --seed $seed --tle 10 \
            --replay "$B/dose/${m}_${seed}_${seat}_${arm}.replay26" >/dev/null 2>&1
      done
      a=$(md5 -q "$B/dose/${m}_${seed}_${seat}_base.replay26")
      s=$(md5 -q "$B/dose/${m}_${seed}_${seat}_store.replay26")
      f=$(md5 -q "$B/dose/${m}_${seed}_${seat}_fired.replay26")
      echo "$m $seat $seed $([ "$a" = "$f" ] && echo same || echo CHANGED) $([ "$s" = "$f" ] && echo same || echo CHANGED)"
    done
  done
done
echo "DOSE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
