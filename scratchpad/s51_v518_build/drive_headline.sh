#!/bin/bash
# v518 HEADLINE: interleaved CONCURRENT blocks, FOUR arms on the SAME seeds.
# ⛔ CONCURRENT PER BLOCK, not arm-after-arm: `--seed` does not pin a game (the
# spawn salt is re-rolled from OS entropy per match, v515 finding 1), so a
# shared seed buys the MAP and the pairing only; running the arms adjacent in
# time is what keeps machine load from separating them.
# THE FOUR ARMS: parent (_v517twin, frozen copy) / f60 (v518 as shipped) /
# f45 / f30 -- i.e. the three-point FS_SENT_RND_FLOOR dose-response against the
# parent, with every other v518 change held on in all three v518 arms.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v518_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap
export PAR=2                      # 4 arms x PAR 2 = 8 concurrent games
BLOCKS="${BLOCKS:-15}"
for i in $(seq 1 "$BLOCKS"); do
  s1=$((i*3-2)); s2=$((i*3-1)); s3=$((i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/grid/b$i"
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent" \
      "$B/grid/b$i/parent.tsv" "$B/grid/b$i/repparent" "$B/grid/b$i/logparent" \
      > "$B/grid/b$i/parent.log" 2>&1 &
  P1=$!
  .venv/bin/python "$B/run_grid.py" bots/_v518fastsent \
      "$B/grid/b$i/f60.tsv" "$B/grid/b$i/repf60" "$B/grid/b$i/logf60" \
      > "$B/grid/b$i/f60.log" 2>&1 &
  P2=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/f45" \
      "$B/grid/b$i/f45.tsv" "$B/grid/b$i/repf45" "$B/grid/b$i/logf45" \
      > "$B/grid/b$i/f45.log" 2>&1 &
  P3=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/f30" \
      "$B/grid/b$i/f30.tsv" "$B/grid/b$i/repf30" "$B/grid/b$i/logf30" \
      > "$B/grid/b$i/f30.log" 2>&1 &
  P4=$!
  echo "$P1 $P2 $P3 $P4" >> "$B/PIDS"
  wait $P1 $P2 $P3 $P4
  echo "BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
