#!/bin/bash
# v526 HEADLINE: 3 arms, 8-map panel, PAR=2 STRICT, arms interleaved per cell.
# arms: v526 (as fired) · parent (bots/_v525flip, the true parent) ·
#       flagoff (bots/_v526transit with LOKI_FS_V526=False -- byte-identical
#       to the parent on 18/18, so a KNOWN-ZERO arm)
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v526_build
export OUT=$B/head
export ARMS="v526=bots/_v526transit,parent=bots/_v525flip,flagoff=$B/flagoff_arm"
export MAPS=atoll,drakkarfjord,glacierkeep,nordkap,yulerune,antler,fjordgate,midgard
export PAR=2
for i in $(seq 1 10); do
  a=$((i*3-2)); b=$((i*3-1)); c=$((i*3))
  export SEEDS="$a,$b,$c"
  .venv/bin/python3 $B/run_battery.py
  echo "HEAD BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
