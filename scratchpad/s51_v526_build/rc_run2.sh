#!/bin/bash
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v526_build
ARM=$B/probe_rc
OUT=$B/rc2
mkdir -p "$OUT"
run () {
  m=$1; s=$2; seat=$3
  if [ "$seat" = "A" ]; then A=$ARM; Bo=bots/_v488beltbreak2; else A=bots/_v488beltbreak2; Bo=$ARM; fi
  .venv/bin/fcode run "$A" "$Bo" "maps/$m.map26" --seed "$s" --tle 10 \
     --replay "$OUT/${m}_s${s}_${seat}.replay26" \
     > "$OUT/${m}_s${s}_${seat}.out" 2> "$OUT/${m}_s${s}_${seat}.err"
  echo "done $m $s $seat"
}
run drakkarfjord 2 B & run glacierkeep 1 A & wait
run midgard 1 A & run valkyrie 1 A & wait
