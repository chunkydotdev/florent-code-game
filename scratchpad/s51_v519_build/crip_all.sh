#!/bin/bash
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v519_build
N="${N:-13}"
for a in parent v519 msoff; do
  out="$B/crip_$a.tsv"; : > "$out"; first=1
  for i in $(seq 1 "$N"); do
    [ -f "$B/grid/b$i/$a.tsv" ] || continue
    .venv/bin/python "$B/crip.py" "$B/grid/b$i/$a.tsv" "$B/grid/b$i/rep$a" "$B/crip_tmp.tsv" "$a" 2>>"$B/crip.err" || continue
    if [ $first = 1 ]; then cat "$B/crip_tmp.tsv" >> "$out"; first=0
    else tail -n +2 "$B/crip_tmp.tsv" >> "$out"; fi
  done
  echo "$a: $(( $(wc -l < "$out") - 1 )) rows"
done
