#!/bin/bash
set -u
B=/Users/junghard/Projects/Work/florent-code-game/scratchpad/s51_v518_build
while pgrep -f drive_headline.sh > /dev/null; do sleep 10; done
$B/drive_gated.sh   > $B/gated_drive.log 2>&1
$B/drive_flagoff.sh > $B/fo_drive.log 2>&1
echo "CHAIN DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
