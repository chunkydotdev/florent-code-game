#!/bin/bash
# v527 M2 SIGNATURE BATTERY: [sealed & no-turret] rounds, both arms,
# instrumented copies, interleaved per cell.  PAR=4.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v527_build
mkdir -p $B/sealnt/v527 $B/sealnt/parent
MAPS="atoll drakkarfjord glacierkeep nordkap yulerune antler fjordgate midgard"
N=0
for s in 41 42 43 44 45 46; do
  for m in $MAPS; do
    for arm in v527 parent; do
      .venv/bin/fcode run $B/inst_$arm bots/_v488beltbreak2 \
        maps/$m.map26 --seed $s --tle 10 --replay /dev/null \
        2>$B/sealnt/$arm/${m}_s${s}.err >/dev/null &
      N=$((N+1))
      if [ $((N % 4)) -eq 0 ]; then wait; fi
    done
  done
done
wait
echo "SEALNT DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
