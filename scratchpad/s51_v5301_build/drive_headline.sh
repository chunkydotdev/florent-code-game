#!/bin/bash
# v530.1 HEADLINE.  THE TWO v530 BATTERIES RE-RUN, SAME OPPONENTS, SAME PANELS,
# SAME n=480/arm, SAME BLOCK STRUCTURE AND SAME SEEDS -- deviating would void
# the cross-build comparison this whole build exists to make.
#
# ⛔ ARMS ARE INTERLEAVED PER CELL by run_battery.py -- v518 finding 2 measured
# a 4.6pp FALSE POSITIVE at n=810/arm on byte-identical play from pooling
# non-time-adjacent local fixtures.
#
# FOUR ARMS, BOTH BATTERIES:
#   parent    _v529merge unchanged            -- the base of every comparison
#   flagoff   _v531fix with LOKI_FS_V530=False -- THE KNOWN ZERO.  Proved
#             byte-identical to parent on 10/10 cells with a negative control
#             (BYTEID_OUT.txt B3/B4), so every flagoff-vs-parent number is
#             FIXTURE SPREAD and is the only honest yardstick for the others.
#   v530      _v530home as fired              -- the arm whose defect this
#             build fixes; carried so the delta is ATTRIBUTABLE rather than
#             compared across two batteries run on different days.
#   v531fix   bots/_v531fix as fired
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v5301_build

export PAR=4
export ARMS="parent=$B/parent_arm,flagoff=$B/flagoff_arm,v530=$B/v530_arm,v531fix=bots/_v531fix"

echo "BATTERY A START $(date -u +%Y-%m-%dT%H:%M:%SZ)"
export OUT=$B/headA
export OPP=$PWD/bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,nordkap,yulerune,antler,fjordgate,midgard
for i in $(seq 1 15); do
  a=$((i*2-1)); b=$((i*2))
  export SEEDS="$a,$b"
  .venv/bin/python3 $B/run_battery.py
  echo "  A BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "BATTERY A DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "BATTERY B START $(date -u +%Y-%m-%dT%H:%M:%SZ)"
export OUT=$B/headB
export OPP=$PWD/bots/_x3r0v165mjolnirB
export MAPS=icefloe,auroraveil,glacierkeep,yulerune,drakkarfjord,ragnarok,royale,nordkap
for i in $(seq 1 15); do
  a=$((i*2-1)); b=$((i*2))
  export SEEDS="$a,$b"
  .venv/bin/python3 $B/run_battery.py
  echo "  B BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE ALL DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
