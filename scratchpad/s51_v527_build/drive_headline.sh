#!/bin/bash
# v527 HEADLINE: 3 arms, 8-map panel, PAR=4 (both full-pool shards COMPLETE),
# arms INTERLEAVED per cell (v518 finding 2: pooling non-time-adjacent local
# fixtures produced a 4.6pp FALSE POSITIVE on byte-identical play).
#   v527    = bots/_v527collar as fired
#   parent  = the RDV-ONLY parent (v526transit with FS_V526_TEMPO=False)
#   flagoff = bots/_v527collar with LOKI_FS_V527=False -- proved byte-identical
#             to `parent` on 18/18 deterministic cells, so a KNOWN-ZERO arm
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v527_build
export OUT=$B/head
export ARMS="v527=bots/_v527collar,parent=$B/parent_arm,flagoff=$B/flagoff_arm"
export MAPS=atoll,drakkarfjord,glacierkeep,nordkap,yulerune,antler,fjordgate,midgard
export PAR=4
for i in $(seq 1 14); do
  a=$((i*2-1)); b=$((i*2))
  export SEEDS="$a,$b"
  .venv/bin/python3 $B/run_battery.py
  echo "HEAD BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
