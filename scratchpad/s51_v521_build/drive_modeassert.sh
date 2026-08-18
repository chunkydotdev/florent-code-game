#!/bin/bash
# THE ASSERTION ITSELF, at n=24 per cell, with EVERY v521 INSTRUMENT ON:
# on a cripple or gated map, no siege-path clause may fire.  Per-game counts,
# so a single leaking game cannot hide in a mean.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v521_build
export SEEDS=201,202,203,204,205,206,207,208,209,210,211,212
export PAR=4
mkdir -p "$B/modeassert"
for m in yulerune midgard archipelago nordkap; do
  export MAPS=$m
  [ "$m" = archipelago ] && export OPP=bots/_v468kladturbo || export OPP=bots/_v488beltbreak2
  .venv/bin/python "$B/run_grid.py" "$B/arms/instg" \
     "$B/modeassert/$m.tsv" "$B/modeassert/rep$m" "$B/modeassert/log$m" \
     > "$B/modeassert/$m.log" 2>&1
  echo "MODEASSERT $m done $(date -u +%H:%M:%SZ)"
done
