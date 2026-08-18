#!/bin/bash
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v526_build
ARM=$B/probe_rc
OUT=$B/rc3
mkdir -p "$OUT"
run () {
  m=$1; s=$2; seat=$3
  if [ "$seat" = "A" ]; then A=$ARM; Bo=bots/_v488beltbreak2; else A=bots/_v488beltbreak2; Bo=$ARM; fi
  .venv/bin/fcode run "$A" "$Bo" "maps/$m.map26" --seed "$s" --tle 10 \
     --replay "$OUT/${m}_s${s}_${seat}.replay26" \
     > "$OUT/${m}_s${s}_${seat}.out" 2> "$OUT/${m}_s${s}_${seat}.err"
}
for m in valkyrie glacierkeep drakkarfjord ragnarok; do
  for s in 1 2 3; do
    run $m $s A & run $m $s B & wait
  done
  echo "map $m done $(date -u +%H:%M:%SZ)"
done
