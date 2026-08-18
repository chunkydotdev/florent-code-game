#!/bin/bash
# v523 HEADLINE: interleaved CONCURRENT blocks, THREE arms on the SAME seeds.
# ⛔ CONCURRENT PER BLOCK (v515 finding 1: --seed does not pin a game).
# ARMS:
#   parent   -- `bots/_v521sync` with FS_V521_SYNC and FS_V521_COLLARFIRST
#               turned off AT THEIR DEFINITION SITES.  The v521 verdict's
#               "NEXT PARENT" = v520-pincer-only + leak fix + PHASE_HONEST, and
#               an INDEPENDENTLY CONSTRUCTED tree rather than a copy of the
#               treatment with a flag appended.
#   v523     -- `bots/_v523eyes` as fired.
#   flagoff  -- `LOKI_FS_V523 = False`, the KNOWN-ZERO control, proved
#               byte-identical to `parent` on 12 of 12 games with a negative
#               control (drive_eq.sh).
# MAPS: the standard 5-map siege grid PLUS yulerune (second cripple cell).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v523_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export PAR=4
BLOCKS="${BLOCKS:-30}"
for i in $(seq 1 "$BLOCKS"); do
  s1=$((i*3-2)); s2=$((i*3-1)); s3=$((i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/grid/b$i"
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent" \
      "$B/grid/b$i/parent.tsv" "$B/grid/b$i/repparent" "$B/grid/b$i/logparent" \
      > "$B/grid/b$i/parent.log" 2>&1 &
  P1=$!
  .venv/bin/python "$B/run_grid.py" bots/_v523eyes \
      "$B/grid/b$i/v523.tsv" "$B/grid/b$i/repv523" "$B/grid/b$i/logv523" \
      > "$B/grid/b$i/v523.log" 2>&1 &
  P2=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/flagoff" \
      "$B/grid/b$i/flagoff.tsv" "$B/grid/b$i/repflagoff" "$B/grid/b$i/logflagoff" \
      > "$B/grid/b$i/flagoff.log" 2>&1 &
  P3=$!
  echo "$P1 $P2 $P3" >> "$B/PIDS"
  wait $P1 $P2 $P3
  echo "BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
