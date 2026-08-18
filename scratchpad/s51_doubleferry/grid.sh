#!/bin/bash
# s51 DOUBLE-FERRY timing probe grid.  An ARRIVAL read, not an effect size.
# 5 siege-active maps x 3 seeds x 2 seats = 30 games vs _v488beltbreak2.
# heart is excluded by construction: its signature (28,20,(7,9),(19,9)) is in
# FS_MAP_SKIP, so the plank never runs there and the map cannot answer this.
cd /Users/junghard/Projects/Work/florent-code-game
ARM="${1:-v513_dblferry}"
D=scratchpad/s51_doubleferry/logs
mkdir -p $D
for M in midgard glacierkeep nordkap atoll drakkarfjord; do
  for S in 1 2 3; do
    echo "$ARM $M $S A"
    echo "$ARM $M $S B"
  done
done | xargs -P 5 -n 4 bash -c '
  cd /Users/junghard/Projects/Work/florent-code-game
  D=scratchpad/s51_doubleferry/logs
  if [ "$3" = "A" ]; then A="scratchpad/s51_doubleferry/$0"; B="scratchpad/s51_doubleferry/base";
  else A="scratchpad/s51_doubleferry/base"; B="scratchpad/s51_doubleferry/$0"; fi
  timeout 1500 .venv/bin/fcode run "$A" "$B" "maps/$1.map26" \
    --tle 10 --seed "$2" --replay "$D/$1-s$2-$3.replay26" \
    > "$D/$1-s$2-$3.out" 2> "$D/$1-s$2-$3.err"
'
echo "GRID DONE $ARM"
