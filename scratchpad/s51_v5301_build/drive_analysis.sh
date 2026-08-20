#!/bin/bash
# v530.1 ANALYSIS.  Every reader is the one the v530 report used, unchanged,
# so the two builds' numbers are comparable line for line.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v5301_build
R=scratchpad/s51_route
P=.venv/bin/python3

echo "ANALYSIS START $(date -u +%Y-%m-%dT%H:%M:%SZ)"

$P $R/routetape.py --batch $B/headA/results.tsv $B/headA/rep --out $B/raceA.tsv \
    > $B/raceA.log 2>&1
echo "  raceA done $(date -u +%H:%M:%SZ)"
$P $R/routetape.py --batch $B/headB/results.tsv $B/headB/rep --out $B/raceB.tsv \
    > $B/raceB.log 2>&1
echo "  raceB done $(date -u +%H:%M:%SZ)"

$P $B/raceread.py --selftest   > $B/RACEA_OUT.txt 2>&1
$P $B/raceread.py $B/raceA.tsv >> $B/RACEA_OUT.txt 2>&1
$P $B/raceread.py --selftest   > $B/RACEB_OUT.txt 2>&1
$P $B/raceread.py $B/raceB.tsv >> $B/RACEB_OUT.txt 2>&1

$P $B/headline.py --selftest > $B/HEADA_OUT.txt 2>&1
$P $B/headline.py $B/headA/results.tsv --rep $B/headA/rep >> $B/HEADA_OUT.txt 2>&1
echo "  headA done $(date -u +%H:%M:%SZ)"
$P $B/headline.py --selftest > $B/HEADB_OUT.txt 2>&1
$P $B/headline.py $B/headB/results.tsv --rep $B/headB/rep >> $B/HEADB_OUT.txt 2>&1
echo "  headB done $(date -u +%H:%M:%SZ)"

$P $B/harvread.py --selftest > $B/HARV_OUT.txt 2>&1
echo "=== BATTERY A (opp _v488beltbreak2) ===" >> $B/HARV_OUT.txt
$P $B/harvread.py $B/headA/rep >> $B/HARV_OUT.txt 2>&1
echo "=== BATTERY B (opp _x3r0v165mjolnirB) ===" >> $B/HARV_OUT.txt
$P $B/harvread.py $B/headB/rep >> $B/HARV_OUT.txt 2>&1
echo "  harv done $(date -u +%H:%M:%SZ)"

$P $B/harv_xcheck.py $B/raceA.tsv $B/headA/rep --limit 400 > $B/XCHECK2_OUT.txt 2>&1
$P $B/harv_xcheck.py $B/raceA.tsv $B/headA/rep --limit 400 --mutate 25 \
    >> $B/XCHECK2_OUT.txt 2>&1

$P $B/reel.py $B/headA v531fix > $B/REELA_OUT.txt 2>&1
$P $B/reel.py $B/headB v531fix > $B/REELB_OUT.txt 2>&1
echo "ANALYSIS DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
