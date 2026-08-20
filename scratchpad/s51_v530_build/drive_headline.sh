#!/bin/bash
# v530 HEADLINE.  TWO BATTERIES, SEQUENTIAL, PAR=4 THROUGHOUT.
#
# ⛔ ARMS ARE INTERLEAVED PER CELL by run_battery.py -- v518 finding 2 measured
# a 4.6pp FALSE POSITIVE at n=810/arm on byte-identical play from pooling
# non-time-adjacent local fixtures.
#
# BATTERY A -- opponent `bots/_v488beltbreak2` (the incumbent holder, the same
# opponent v526/v527/v528/v529 used; deviating would void the cross-build
# comparison).  8-map panel, 15 blocks x 2 seeds x 2 seats = 480/arm.
#   v530     bots/_v530home     all three planks live
#   parent   parent_arm         `_v529merge` unchanged
#   flagoff  flagoff_arm        LOKI_FS_V530=False -- proved byte-identical to
#                               parent on 20/20 cells, so every flagoff-vs-
#                               parent number is FIXTURE SPREAD and is the only
#                               honest yardstick for the other four
#   nomouth  nomouth            P1 off   (the primary's own ablation)
#   nocorner nocorner           P2 off
#   nodoor   nodoor             P3 off
#   ring     ring               FS_V530_RING=True -- P1b, THE CANDIDATE.  It
#                               ships OFF in the fired tree so the mouth read
#                               cannot be contaminated by it; this arm is the
#                               increment that decides its fired state.
#
# BATTERY B -- opponent `bots/_x3r0v165mjolnirB`, THE RING-CLAIMER.  This is the
# fixture the crater defect fires on: the s51 autopsy measured it standing on
# one of OUR 8 core-ring sockets at r7.2 against our belt head at r80.6, and
# `titanium_collected` at r100 = 0 in 60/60 icefloe games.  CRATER-OVERSAMPLED
# panel: 5 belt-fail maps + 3 sweep controls.  4 arms x 480.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v530_build

export PAR=4

echo "BATTERY A START $(date -u +%Y-%m-%dT%H:%M:%SZ)"
export OUT=$B/headA
export OPP=$PWD/bots/_v488beltbreak2
export ARMS="v530=bots/_v530home,parent=$B/parent_arm,flagoff=$B/flagoff_arm,nomouth=$B/nomouth,nocorner=$B/nocorner,nodoor=$B/nodoor,ring=$B/ring"
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
export ARMS="v530=bots/_v530home,parent=$B/parent_arm,flagoff=$B/flagoff_arm,nomouth=$B/nomouth,ring=$B/ring"
export MAPS=icefloe,auroraveil,glacierkeep,yulerune,drakkarfjord,ragnarok,royale,nordkap
for i in $(seq 1 15); do
  a=$((i*2-1)); b=$((i*2))
  export SEEDS="$a,$b"
  .venv/bin/python3 $B/run_battery.py
  echo "  B BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE ALL DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
