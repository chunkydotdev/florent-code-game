#!/bin/bash
# s51 EVICTION AUTOPSY grid.  Defect-presence read, not an effect size.
# 5 siege-active maps x 3 seeds x 2 seats.  heart is DELIBERATELY EXCLUDED:
# its signature (28,20,(7,9),(19,9)) is in FS_MAP_SKIP, so the plank never
# runs there and the map cannot answer this question.
cd /Users/junghard/Projects/Work/florent-code-game
ARM="${1:-v513_log}"
D=scratchpad/s51_evict_autopsy/logs
mkdir -p $D
for M in midgard glacierkeep nordkap atoll drakkarfjord; do
  for S in 1 2 3; do
    echo "$ARM $M $S A"
    echo "$ARM $M $S B"
  done
done | xargs -P 5 -n 4 bash -c '
  cd /Users/junghard/Projects/Work/florent-code-game
  D=scratchpad/s51_evict_autopsy/logs
  if [ "$3" = "A" ]; then A="scratchpad/s51_evict_autopsy/$0"; B="scratchpad/s51_evict_autopsy/base";
  else A="scratchpad/s51_evict_autopsy/base"; B="scratchpad/s51_evict_autopsy/$0"; fi
  timeout 1500 .venv/bin/fcode run "$A" "$B" "maps/$1.map26" \
    --tle 10 --seed "$2" --replay "$D/$0-$1-s$2-$3.replay26" \
    > "$D/$0-$1-s$2-$3.out" 2> "$D/$0-$1-s$2-$3.err"
'
echo "GRID DONE $ARM"
