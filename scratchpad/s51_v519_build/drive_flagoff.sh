#!/bin/bash
# FLAG-OFF BEHAVIOURAL: two INTERLEAVED fixtures (both arms inside the same
# block), flag-off vs a frozen copy of the parent.  n=180 each per fixture.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v519_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export PAR=2
FX="$1"; shift
BASE="$1"; shift
for i in 1 2 3 4 5; do
  s1=$((BASE+i*3-3)); s2=$((BASE+i*3-2)); s3=$((BASE+i*3-1))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/$FX/b$i"
  .venv/bin/python "$B/run_grid.py" "$B/arms/flagoff" "$B/$FX/b$i/flagoff.tsv" "$B/$FX/b$i/repflagoff" "$B/$FX/b$i/logflagoff" >/dev/null 2>&1 &
  P1=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent" "$B/$FX/b$i/parent.tsv" "$B/$FX/b$i/repparent" "$B/$FX/b$i/logparent" >/dev/null 2>&1 &
  P2=$!
  echo "$P1 $P2" >> "$B/PIDS"
  wait $P1 $P2
done
echo "$FX DONE $(date -u +%H:%M:%SZ)"
