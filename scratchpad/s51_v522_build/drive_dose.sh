#!/bin/bash
# ⛔⛔ THE DETERMINISTIC DOSE TEST -- v521's promoted method, run here as the
# PRE-HEADLINE GATE the mandate requires.
#
# Same seeds, randomness off on BOTH sides, parent vs treatment, replay bytes
# diffed.  It answers the one question no win column can: DOES THIS CLAUSE EVER
# CHANGE ANYTHING?  v521 ran it and measured two ladder designs at 0/18 changed
# games on the maps where their state fires -- before a headline game was
# played, and the win column would have called that a clean null at any n.
#
# GATE: the clause must change >= 1 of 18 games' bytes on the non-gated maps.
# 6 maps x 3 seeds x 2 seats = 36 cells; midgard and yulerune are the
# FS_V519_CRIPPLE_MAPS internal control, where the whole plank stands down, so
# the 18 that count are atoll / drakkarfjord / glacierkeep / nordkap ... minus
# atoll, which is in FS_MAP_SKIP.  Per-map counts are printed so the gate is
# read on the cells it applies to rather than on a pooled number.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v522_build
TRT="${TRT:-$B/arms/dose_fired}"
TAG="${TAG:-fired}"
mkdir -p "$B/dose"
rm -rf "$B/arms/dose_opp" "$B/arms/dose_base"
cp -R bots/_v488beltbreak2 "$B/arms/dose_opp"; chmod -R u+w "$B/arms/dose_opp"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/dose_opp/doctrine.py"
cp -R "$B/arms/parent" "$B/arms/dose_base"; chmod -R u+w "$B/arms/dose_base"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/dose_base/doctrine.py"
rm -rf "$B"/arms/dose_*/__pycache__

TOT=0; CHG=0
for m in atoll drakkarfjord glacierkeep midgard nordkap yulerune; do
  mc=0; mt=0
  for s in 7 11 23; do
    for seat in A B; do
      for arm in base trt; do
        case $arm in base) T="$B/arms/dose_base";; trt) T="$TRT";; esac
        if [ "$seat" = A ]; then F="$T"; S="$B/arms/dose_opp"; else F="$B/arms/dose_opp"; S="$T"; fi
        .venv/bin/fcode run "$F" "$S" "maps/$m.map26" --seed "$s" --tle 10 \
            --replay "$B/dose/${TAG}_${m}_${s}_${seat}_${arm}.replay26" >/dev/null 2>&1
      done
      a=$(md5 -q "$B/dose/${TAG}_${m}_${s}_${seat}_base.replay26")
      b=$(md5 -q "$B/dose/${TAG}_${m}_${s}_${seat}_trt.replay26")
      mt=$((mt+1)); TOT=$((TOT+1))
      if [ "$a" != "$b" ]; then mc=$((mc+1)); CHG=$((CHG+1)); fi
    done
  done
  echo "DOSE $TAG $m  changed $mc / $mt"
done
echo "DOSE $TAG TOTAL changed $CHG / $TOT"
