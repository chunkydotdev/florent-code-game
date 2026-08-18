#!/bin/bash
B=/Users/junghard/Projects/Work/florent-code-game/scratchpad/s51_v518_build
while pgrep -f drive_flagoff.sh > /dev/null; do sleep 5; done
$B/drive_flagoff2.sh > $B/fo2_drive.log 2>&1
