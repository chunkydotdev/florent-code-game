#!/bin/bash
# THE STANDDOWN ASSERTION, n=24 per cell, with BOTH v522 instruments ON:
# on a CRIPPLE map (yulerune, midgard) or the GATED map (archipelago) no v522
# clause may fire in ANY game.  Per-game counts, so one leaking game cannot
# hide in a mean.  nordkap is the POSITIVE CONTROL -- the assertion must be
# seen to produce the other verdict.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v523_build
export SEEDS=201,202,203,204,205,206,207,208,209,210,211,212
export PAR=4
mkdir -p "$B/modeassert"
for m in yulerune midgard archipelago nordkap; do
  export MAPS=$m
  [ "$m" = archipelago ] && export OPP=bots/_v468kladturbo || export OPP=bots/_v488beltbreak2
  .venv/bin/python "$B/run_grid.py" "$B/arms/mF" \
     "$B/modeassert/$m.tsv" "$B/modeassert/rep$m" "$B/modeassert/log$m" \
     > "$B/modeassert/$m.log" 2>&1
  echo "MODEASSERT $m done $(date -u +%H:%M:%SZ)"
done
echo "MODEASSERT DONE"
