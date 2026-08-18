#!/bin/bash
# REPLACEMENT LATENCY -- v513's forced-death method, reused verbatim.
# The SEALER self-destructs at r60 with the game otherwise untouched; the
# latency is (first round a body of ours is back at the ring) - 60.
# ⛔ BOTH ARMS CARRY THE PROBE, which is what makes them comparable: `pKon` is
# the fired configuration, `pKoff` is the SAME TREE with the pincer off, i.e.
# one body -- the parent's shape, measured on the parent's own chassis rather
# than quoted.  v513's own number (10 of 14 replaced, MEDIAN 90 rounds, 0
# inside Magnus's ~15-round cap) is the historical anchor and is quoted, not
# re-derived.
# `pKoffP` additionally turns PRESENCE off, so the FUNDING half of change 2 can
# be separated from the two-body half.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v520_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export SEEDS=201,202,203,204
export PAR=3
P="FS_V520_PROBE_KILL_RND = 60|FS_LOG = True|FS_V520_PRES_LOG = True"
IFS='|' read -r -a I <<< "$P"
bash "$B/mkarm.sh" pKon    "${I[@]}" >/dev/null
bash "$B/mkarm.sh" pKoff   "${I[@]}" "FS_V520_PINCER = False" >/dev/null
bash "$B/mkarm.sh" pKoffP  "${I[@]}" "FS_V520_PINCER = False" "FS_V520_PRESENCE = False" >/dev/null
bash "$B/mkarm.sh" pKonP   "${I[@]}" "FS_V520_PRESENCE = False" >/dev/null
for a in pKon pKoff pKoffP pKonP; do
  mkdir -p "$B/lat/$a"
  .venv/bin/python "$B/run_grid.py" "$B/arms/$a" \
      "$B/lat/$a.tsv" "$B/lat/$a/rep" "$B/lat/$a/log" > "$B/lat/$a.log" 2>&1
  echo "LAT $a done $(date -u +%H:%M:%SZ)"
done
echo "LAT DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
