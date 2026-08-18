#!/bin/bash
# BYTE-IDENTITY (v518 finding 2's method, reused): with OUR salt AND THE
# OPPONENT'S salt disabled the fixture is deterministic, so the flag-off tree
# and the parent can be compared on the REPLAY BYTES instead of on a win rate.
# ⛔ THE NEGATIVE CONTROL IS THE INSTRUMENT: the same tree run twice must
# produce identical replays before "identical" means anything (v518's first
# attempt read 1/30 identical on the control and would have inverted the
# verdict).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v519_build
export OPP=$B/arms/eq_opp
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export SEEDS=1
export PAR=3
.venv/bin/python "$B/run_grid.py" "$B/arms/eqparent" "$B/eq/parentA.tsv" "$B/eq/repparentA" "$B/eq/logparentA" >/dev/null 2>&1
.venv/bin/python "$B/run_grid.py" "$B/arms/eqparent" "$B/eq/parentB.tsv" "$B/eq/repparentB" "$B/eq/logparentB" >/dev/null 2>&1
.venv/bin/python "$B/run_grid.py" "$B/arms/eqflagoff" "$B/eq/flagoff.tsv" "$B/eq/repflagoff" "$B/eq/logflagoff" >/dev/null 2>&1
echo "== NEGATIVE CONTROL: parent run twice =="
same=0; diff_=0
for f in "$B"/eq/repparentA/*.replay26; do
  t=$(basename "$f")
  if cmp -s "$f" "$B/eq/repparentB/$t"; then same=$((same+1)); else diff_=$((diff_+1)); fi
done
echo "identical $same / differing $diff_"
echo "== TEST: parent vs FLAG-OFF =="
same=0; diff_=0
for f in "$B"/eq/repparentA/*.replay26; do
  t=$(basename "$f")
  if cmp -s "$f" "$B/eq/repflagoff/$t"; then same=$((same+1)); else diff_=$((diff_+1)); fi
done
echo "identical $same / differing $diff_"
