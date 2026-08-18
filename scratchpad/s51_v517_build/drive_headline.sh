#!/bin/bash
# v517 HEADLINE: interleaved CONCURRENT blocks, three arms on the SAME seeds.
# ⛔ CONCURRENT PER BLOCK, not arm-after-arm: `--seed` does not pin a game (the
# spawn salt is re-rolled from OS entropy per match, v515 finding 1), so a
# shared seed buys the MAP and the pairing only; running the arms adjacent in
# time is what keeps machine load from separating them.
# THIRD ARM = the FLAG-OFF tree, which is provably the parent on every path and
# is therefore the draw control the v516 gated leg showed we need.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v517_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap
export PAR=2                      # 3 arms x PAR 2 = 6 concurrent games
BLOCKS="${BLOCKS:-15}"
for i in $(seq 1 "$BLOCKS"); do
  s1=$((i*3-2)); s2=$((i*3-1)); s3=$((i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/grid/b$i"
  .venv/bin/python "$B/run_grid.py" bots/_v517twin \
      "$B/grid/b$i/v517.tsv" "$B/grid/b$i/rep517" "$B/grid/b$i/log517" \
      > "$B/grid/b$i/v517.log" 2>&1 &
  P1=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent516" \
      "$B/grid/b$i/v516.tsv" "$B/grid/b$i/rep516" "$B/grid/b$i/log516" \
      > "$B/grid/b$i/v516.log" 2>&1 &
  P2=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/flagoff" \
      "$B/grid/b$i/fo.tsv" "$B/grid/b$i/repfo" "$B/grid/b$i/logfo" \
      > "$B/grid/b$i/fo.log" 2>&1 &
  P3=$!
  echo "$P1 $P2 $P3" >> "$B/PIDS"
  wait $P1 $P2 $P3
  echo "BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
