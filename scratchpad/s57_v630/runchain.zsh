#!/bin/zsh
# s57 v630 tube-guard verification chain -- SEQUENTIAL per the v620 load
# discipline (tape.sh already runs 5 games concurrently; stacking tapes turns
# TLE noise into behaviour change).  Order: fresh control tapes (v628compose),
# flags-off identity tapes (v630 tree as committed), flag-ON smoke tapes.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
S=scratchpad/s57_v630
T=scratchpad/s54_v620/tape.sh
for F in f1 f2; do
  $T $F bots/_v628compose   $S/t_ctrl_$F  >> $S/runchain.log 2>&1
  echo "ctrl $F done $(date -u +%H:%M:%SZ)"
  $T $F bots/_v630tubeguard $S/t_id_$F    >> $S/runchain.log 2>&1
  echo "id $F done $(date -u +%H:%M:%SZ)"
  $T $F $S/arm_on           $S/t_on_$F    >> $S/runchain.log 2>&1
  echo "on $F done $(date -u +%H:%M:%SZ)"
done
echo "CHAIN COMPLETE $(date -u +%H:%M:%SZ)"
