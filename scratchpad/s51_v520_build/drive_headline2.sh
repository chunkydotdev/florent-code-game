#!/bin/bash
# v520 HEADLINE: interleaved CONCURRENT blocks, THREE arms on the SAME seeds.
# ⛔ CONCURRENT PER BLOCK (v515 finding 1: --seed does not pin a game).
# ARMS: parent (_v519cripple frozen copy) / v520 FIRED (all three changes) /
#       flagoff (LOKI_FS_V520 = False) -- the KNOWN-ZERO control, in the SAME
#       blocks, because v519 open item 2 measured this grid's same-config
#       false-positive floor at ~4.7-5.6pp three independent ways and any
#       claim under ~6pp needs a control arm rather than an interval.
# MAPS: the standard 5-map siege grid PLUS yulerune (the second registered
# cripple cell, carried forward from v519's headline).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v520_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export PAR=2
BLOCKS="${BLOCKS:-13}"
for i in $(seq "${START:-1}" "$BLOCKS"); do
  s1=$((i*3-2)); s2=$((i*3-1)); s3=$((i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/grid/b$i"
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent" \
      "$B/grid/b$i/parent.tsv" "$B/grid/b$i/repparent" "$B/grid/b$i/logparent" \
      > "$B/grid/b$i/parent.log" 2>&1 &
  P1=$!
  .venv/bin/python "$B/run_grid.py" bots/_v520pincer \
      "$B/grid/b$i/v520.tsv" "$B/grid/b$i/repv520" "$B/grid/b$i/logv520" \
      > "$B/grid/b$i/v520.log" 2>&1 &
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
