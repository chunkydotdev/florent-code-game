#!/bin/bash
# v521 HEADLINE: interleaved CONCURRENT blocks, THREE arms on the SAME seeds.
# ⛔ CONCURRENT PER BLOCK (v515 finding 1: --seed does not pin a game).
# ARMS:
#   pinceronly -- `bots/_v520pincer` with FS_V520_PRESENCE / FS_V520_GUNNEAR
#                 turned off AT THEIR DEFINITION SITES.  This is the mandate's
#                 concurrent baseline and it is a fired-config CORRECTION of the
#                 parent, not a new tree.
#   v521       -- `bots/_v521sync` as fired.
#   flagoff    -- `LOKI_FS_V521 = False`, the KNOWN-ZERO control, proved
#                 byte-identical to `pinceronly` on 12 of 12 games with a
#                 negative AND a positive control (drive_eq.sh).
# MAPS: the standard 5-map siege grid PLUS yulerune (the second registered
# cripple cell, carried forward from v519/v520).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v521_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export PAR=4
BLOCKS="${BLOCKS:-30}"
for i in $(seq 1 "$BLOCKS"); do
  s1=$((i*3-2)); s2=$((i*3-1)); s3=$((i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/grid/b$i"
  .venv/bin/python "$B/run_grid.py" "$B/arms/pinceronly" \
      "$B/grid/b$i/pinceronly.tsv" "$B/grid/b$i/reppinceronly" "$B/grid/b$i/logpinceronly" \
      > "$B/grid/b$i/pinceronly.log" 2>&1 &
  P1=$!
  .venv/bin/python "$B/run_grid.py" bots/_v521sync \
      "$B/grid/b$i/v521.tsv" "$B/grid/b$i/repv521" "$B/grid/b$i/logv521" \
      > "$B/grid/b$i/v521.log" 2>&1 &
  P2=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/flagoff" \
      "$B/grid/b$i/flagoff.tsv" "$B/grid/b$i/repflagoff" "$B/grid/b$i/logflagoff" \
      > "$B/grid/b$i/flagoff.log" 2>&1 &
  P3=$!
  echo "$P1 $P2 $P3" >> "$B/PIDS"
  wait $P1 $P2 $P3
  echo "BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
