#!/bin/zsh
# E1/E2 readout: rdiff every cell, ctrl-vs-id (want 30/30 identical) and
# ctrl-vs-on (want >=8/30 DIVERGENT).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
S=scratchpad/s57_v630
for F in f1 f2; do
  for PAIR in id on; do
    same=0; diff=0; missing=0
    for R in $S/t_ctrl_$F/*.replay26; do
      B=$S/t_${PAIR}_$F/$(basename $R)
      if [[ ! -s $B ]]; then missing=$((missing+1)); continue; fi
      if .venv/bin/python tools/rdiff.py $R $B 2>/dev/null | grep -q "NO behavioral divergence"; then
        same=$((same+1))
      else
        diff=$((diff+1))
      fi
    done
    echo "$F ctrl-vs-$PAIR: identical=$same divergent=$diff missing=$missing"
  done
done
