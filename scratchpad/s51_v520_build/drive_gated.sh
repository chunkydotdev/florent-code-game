#!/bin/bash
# GATED CONTROL -- archipelago, whose signature is in FS_MAP_SKIP, so `_fs_gate`
# refuses the whole ferry-siege plank and all three v520 changes are
# STRUCTURALLY UNREACHABLE (no ferry, no crew appointment, no ring turn, no
# GUNFIRST call site).  A movement here is fixture, by construction, and v519
# measured exactly that: +5.6pp on a board where nothing could execute.
# Control is `_v468kladturbo`, the same opponent v519's gated leg used.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v520_build
export OPP=bots/_v468kladturbo
export MAPS=archipelago
export PAR=2
mkdir -p "$B/gated"
for draw in 1 2; do
  if [ "$draw" = 1 ]; then export SEEDS=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18
  else export SEEDS=19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36; fi
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent" \
      "$B/gated/parent$draw.tsv" "$B/gated/rep_p$draw" "$B/gated/log_p$draw" \
      > "$B/gated/parent$draw.log" 2>&1 &
  P1=$!
  .venv/bin/python "$B/run_grid.py" bots/_v520pincer \
      "$B/gated/v520$draw.tsv" "$B/gated/rep_v$draw" "$B/gated/log_v$draw" \
      > "$B/gated/v520$draw.log" 2>&1 &
  P2=$!
  wait $P1 $P2
  echo "GATED draw $draw done $(date -u +%H:%M:%SZ)"
done
echo "GATED DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
