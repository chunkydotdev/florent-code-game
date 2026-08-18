#!/bin/bash
# v516 HEADLINE: interleaved concurrent blocks, both arms on the SAME seeds.
# ⛔ CONCURRENT PER BLOCK, not arm-after-arm: `--seed` does not pin a game (the
# spawn salt is re-rolled from OS entropy per match, v515 finding 1), so the
# only thing a shared seed buys is the MAP and the pairing; running the arms
# adjacent in time is what keeps machine load from separating them.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v516_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap
export PAR=2                      # 2 arms x PAR 2 = 4 concurrent games
BLOCKS="${BLOCKS:-15}"
for i in $(seq 1 "$BLOCKS"); do
  s1=$((i*3-2)); s2=$((i*3-1)); s3=$((i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/grid/b$i"
  .venv/bin/python "$B/run_grid.py" bots/_v516teardown \
      "$B/grid/b$i/v516.tsv" "$B/grid/b$i/rep516" "$B/grid/b$i/log516" \
      > "$B/grid/b$i/v516.log" 2>&1 &
  P1=$!
  .venv/bin/python "$B/run_grid.py" scratchpad/s51_v516_build/arms/parent515 \
      "$B/grid/b$i/v515.tsv" "$B/grid/b$i/rep515" "$B/grid/b$i/log515" \
      > "$B/grid/b$i/v515.log" 2>&1 &
  P2=$!
  echo "$P1 $P2" >> "$B/PIDS"
  wait $P1 $P2
  echo "BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
