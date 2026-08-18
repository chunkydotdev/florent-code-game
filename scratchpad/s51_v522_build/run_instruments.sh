#!/bin/bash
# Replay-side instruments over the whole headline grid, per arm.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v522_build
TOOL=$1; OUTPFX=$2
for arm in parent v522 flagoff; do
  : > "$B/${OUTPFX}_$arm.tsv"
  first=1
  for b in $(ls -d $B/grid/b* | sort -t b -k3 -n); do
    [ -f "$b/$arm.tsv" ] || continue
    .venv/bin/python "$B/$TOOL" "$b/$arm.tsv" "$b/rep$arm" "/tmp/_i_$$.tsv" "$arm" >/dev/null 2>>"$B/${OUTPFX}_$arm.err"
    if [ $first = 1 ]; then cat /tmp/_i_$$.tsv >> "$B/${OUTPFX}_$arm.tsv"; first=0
    else tail -n +2 /tmp/_i_$$.tsv >> "$B/${OUTPFX}_$arm.tsv"; fi
  done
  echo "$arm: $(( $(wc -l < "$B/${OUTPFX}_$arm.tsv") - 1 )) rows"
done
rm -f /tmp/_i_$$.tsv
