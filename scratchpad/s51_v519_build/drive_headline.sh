#!/bin/bash
# v519 HEADLINE: interleaved CONCURRENT blocks, THREE arms on the SAME seeds.
# ⛔ CONCURRENT PER BLOCK (v515 finding 1: --seed does not pin a game).
# ARMS: parent (_v518fastsent frozen copy, floor 60) / v519 FIRED (both changes)
#       / msoff (v519 with MODESWITCH off -- isolates change 2, and doubles as a
#       second read of parent behaviour because change 1 is dose-zero).
# MAPS: the standard 5-map siege grid PLUS yulerune, the second registered
# cripple cell -- a MODESWITCH headline that omits half its treated population
# would measure the change on one map.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v519_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export PAR=2
BLOCKS="${BLOCKS:-13}"
for i in $(seq 1 "$BLOCKS"); do
  s1=$((i*3-2)); s2=$((i*3-1)); s3=$((i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/grid/b$i"
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent" \
      "$B/grid/b$i/parent.tsv" "$B/grid/b$i/repparent" "$B/grid/b$i/logparent" \
      > "$B/grid/b$i/parent.log" 2>&1 &
  P1=$!
  .venv/bin/python "$B/run_grid.py" bots/_v519cripple \
      "$B/grid/b$i/v519.tsv" "$B/grid/b$i/repv519" "$B/grid/b$i/logv519" \
      > "$B/grid/b$i/v519.log" 2>&1 &
  P2=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/msoff" \
      "$B/grid/b$i/msoff.tsv" "$B/grid/b$i/repmsoff" "$B/grid/b$i/logmsoff" \
      > "$B/grid/b$i/msoff.log" 2>&1 &
  P3=$!
  echo "$P1 $P2 $P3" >> "$B/PIDS"
  wait $P1 $P2 $P3
  echo "BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
