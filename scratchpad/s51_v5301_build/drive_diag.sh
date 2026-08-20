#!/bin/bash
# v530.1 DIAGNOSTIC BATTERY (battery A panel and opponent, 480/arm).
#
# ⛔ THIS IS NOT THE HEADLINE AND ITS ROWS ARE NOT POOLED WITH IT.  It exists
# because the headline answers "is the bootstrap defect fixed" (yes) and
# "is the DEFENCE_ADMISSION bar restored" (no, not fully), and the builder's
# next decision needs the SPLIT.  Five arms, interleaved per cell, so every
# number below is a WITHIN-BATTERY comparison:
#
#   parent    _v529merge                    -- the base
#   flagoff   LOKI_FS_V530=False            -- the known zero (byte-identical
#                                              to parent, 10/10 + control)
#   v531fix   as fired
#   nomouth   _v531fix + FS_V530_MOUTH=False -- P1 OFF, P2+P3 still on.  This
#                                              is how much of the residual is
#                                              NOT the mouth at all.
#   cap6      _v531fix + V530_MOUTH_MAX_LINKS=6 -- §11.3 of the v530 report,
#                                              tested for free.  NOT a shipped
#                                              default; the fired tree keeps 16.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v5301_build

export PAR=4
export OUT=$B/diagA
export OPP=$PWD/bots/_v488beltbreak2
export ARMS="parent=$B/parent_arm,flagoff=$B/flagoff_arm,v531fix=bots/_v531fix,nomouth=$B/nomouth_arm,cap6=$B/cap6_arm"
export MAPS=atoll,drakkarfjord,glacierkeep,nordkap,yulerune,antler,fjordgate,midgard

echo "DIAG START $(date -u +%Y-%m-%dT%H:%M:%SZ)"
for i in $(seq 1 15); do
  a=$((i*2-1)); b=$((i*2))
  export SEEDS="$a,$b"
  .venv/bin/python3 $B/run_battery.py
  echo "  DIAG BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "DIAG DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
