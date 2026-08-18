#!/bin/bash
# 5 instrumented root-cause games (M6 tempo + M4 walker), PAR=2.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v526_build
ARM="${ARM:-$B/probe_rc}"
OUT="${OUT:-$B/rc}"
mkdir -p "$OUT"
run () { # map seed seat
  m=$1; s=$2; seat=$3
  if [ "$seat" = "A" ]; then A=$ARM; Bo=bots/_v488beltbreak2; else A=bots/_v488beltbreak2; Bo=$ARM; fi
  .venv/bin/fcode run "$A" "$Bo" "maps/$m.map26" --seed "$s" --tle 10 \
     --replay "$OUT/${m}_s${s}_${seat}.replay26" \
     > "$OUT/${m}_s${s}_${seat}.out" 2> "$OUT/${m}_s${s}_${seat}.err"
  echo "done $m $s $seat $(date -u +%H:%M:%SZ)"
}
run drakkarfjord 1 A & run glacierkeep 1 A & wait
run midgard 1 A & run nordkap 1 A & wait
run drakkarfjord 2 B & wait
