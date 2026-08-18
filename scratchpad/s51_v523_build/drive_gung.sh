#!/bin/bash
# ⭐ MAGNUS DIRECTIVE (s51, mid-build): TWO GUNGNIR LEGS, INTERLEAVED.
#
# v523 FIRED vs `bots/_x3r0v161gungnir` AND parent-as-configured vs the SAME
# opponent, n >= 450 each, run as CONCURRENT BLOCKS ON THE SAME SEEDS -- so the
# delta is drift-proof rather than leaning on the earlier SEPARATE-RUN 55.6%
# read (scratchpad/s51_pincer_vs_gungnir/).
#
# ⛔ THE CAVEATS TRAVEL WITH THE NUMBER AND ARE NOT OPTIONAL: Gungnir is a
# TEAMMATE'S BOT, not the field; this is a 6-map grid, which `PROGRAMME.md`
# calls explicitly non-arming; and the cripple cells (midgard, yulerune)
# measured 47% / 37% vs Gungnir in the v520 screen, so per-map movement THERE
# is an opponent-specific mode-calibration question and is reported as one.
#
# ⛔ RUN ORDER: the incumbent headline is the VERDICT SURFACE and runs first.
# This leg runs after it, and if the budget forces a choice it is this leg that
# is reported "as far as it got".
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v523_build
export OPP=bots/_x3r0v161gungnir
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export PAR=4
BLOCKS="${GBLOCKS:-13}"
for i in $(seq 1 "$BLOCKS"); do
  s1=$((400+i*3-2)); s2=$((400+i*3-1)); s3=$((400+i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/gung/b$i"
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent" \
      "$B/gung/b$i/parent.tsv" "$B/gung/b$i/repparent" "$B/gung/b$i/logparent" \
      > "$B/gung/b$i/parent.log" 2>&1 &
  P1=$!
  .venv/bin/python "$B/run_grid.py" bots/_v523eyes \
      "$B/gung/b$i/v523.tsv" "$B/gung/b$i/repv523" "$B/gung/b$i/logv523" \
      > "$B/gung/b$i/v523.log" 2>&1 &
  P2=$!
  echo "$P1 $P2" >> "$B/PIDS"
  wait $P1 $P2
  echo "GBLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "GUNG DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
