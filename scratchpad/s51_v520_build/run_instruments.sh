#!/bin/bash
# Run the three replay-side instruments across every COMPLETE block of the
# headline grid, one output TSV per arm.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v520_build
mkdir -p "$B/out"
for a in parent v520 flagoff; do
  for tool in seatrate termcov nobody; do
    : > "$B/${tool}_$a.tsv"
  done
  for b in "$B"/grid/b*/; do
    i=$(basename "$b")
    n=$(wc -l < "$b/$a.tsv" 2>/dev/null | tr -d ' ')
    [ "$n" = "37" ] || continue
    for tool in seatrate termcov nobody; do
      .venv/bin/python "$B/$tool.py" "$b$a.tsv" "$b/rep$a" \
          "$B/out/${tool}_${i}_${a}.tsv" "$a" >/dev/null 2>&1 || continue
      if [ ! -s "$B/${tool}_$a.tsv" ]; then
        cat "$B/out/${tool}_${i}_${a}.tsv" >> "$B/${tool}_$a.tsv"
      else
        tail -n +2 "$B/out/${tool}_${i}_${a}.tsv" >> "$B/${tool}_$a.tsv"
      fi
    done
  done
  for tool in seatrate termcov nobody; do
    echo "$tool $a rows: $(wc -l < "$B/${tool}_$a.tsv" | tr -d ' ')"
  done
done
