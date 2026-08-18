#!/bin/bash
# v526 ATTRIBUTION: which of M6/M3 carries the headline regression.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v526_build
export OUT=$B/attrib
export ARMS="parent=bots/_v525flip,v526=bots/_v526transit,tempo=$B/arm_tempo_only,rdv=$B/arm_rdv_only"
export MAPS=atoll,drakkarfjord,glacierkeep,nordkap,yulerune,antler,fjordgate,midgard
export PAR=2
for i in $(seq 1 5); do
  a=$((100+i*3-2)); b=$((100+i*3-1)); c=$((100+i*3))
  export SEEDS="$a,$b,$c"
  .venv/bin/python3 $B/run_battery.py
  echo "ATTRIB BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "ATTRIB DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
