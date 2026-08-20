#!/bin/bash
# v528 HEADLINE: 3 arms, the SAME 8-map panel v526/v527 used (deviating would
# make the cross-build comparison invalid), arms INTERLEAVED per cell (v518
# finding 2: pooling non-time-adjacent local fixtures produced a 4.6pp FALSE
# POSITIVE on byte-identical play).
#   v528    = bots/_v528eco as fired
#   parent  = _v526transit configured RDV-ONLY (FS_V526_TEMPO=False)
#   flagoff = bots/_v528eco with LOKI_FS_V528=False -- the KNOWN-ZERO arm.
#             Proved byte-identical to `parent` by byte_identity.py, so any
#             flagoff-vs-parent gap in the table below is INSTRUMENT SPREAD and
#             is the only honest yardstick for the v528-vs-parent gap.
# PAR=3: the sibling v527 battery reached HEADLINE DONE at 04:19:20Z and
# corefill is DRAINED (scratchpad/COREFILL_WORKLIST_DRAINED), so the box is
# between batteries.  Re-checked each block.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v528_build
export OUT=$B/head
export ARMS="v528=bots/_v528eco,parent=$B/parent_arm,flagoff=$B/flagoff_arm"
export MAPS=atoll,drakkarfjord,glacierkeep,nordkap,yulerune,antler,fjordgate,midgard
export PAR=3
for i in $(seq 1 15); do
  a=$((i*2-1)); b=$((i*2))
  export SEEDS="$a,$b"
  .venv/bin/python3 $B/run_battery.py
  echo "HEAD BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
