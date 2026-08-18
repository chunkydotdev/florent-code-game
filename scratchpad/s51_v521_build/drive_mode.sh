#!/bin/bash
# MODE-SELECTOR BATTERY (coordinator request, s51): the two standdown mechanisms
# are DIFFERENT CODE and must both be verified.
#   CRIPPLE  yulerune, midgard   (FS_V519_CRIPPLE_MAPS + FS_V519_MODESWITCH)
#   GATED    archipelago         (FS_MAP_SKIP)
#   CONTROL  nordkap             (neither -- the POSITIVE control, where the
#                                 assertion MUST fire)
# THREE arms per cell: v521 FIRED, the v520-PINCER-ONLY baseline, and the PURE
# CHASSIS (LOKI_FERRY_SIEGE_ON = False, which doctrine.py states reproduces
# `_v488beltbreak2` exactly).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v521_build
export OPP=bots/_v488beltbreak2
export SEEDS=201,202,203,204,205,206,207,208,209,210,211,212
export PAR=2
for m in yulerune midgard archipelago nordkap; do
  export MAPS=$m
  [ "$m" = archipelago ] && export OPP=bots/_v468kladturbo || export OPP=bots/_v488beltbreak2
  for arm in v521 pinceronly chassis; do
    T="$B/arms/$arm"; [ "$arm" = v521 ] && T=bots/_v521sync
    mkdir -p "$B/mode/$m"
    .venv/bin/python "$B/run_grid.py" "$T" \
       "$B/mode/$m/$arm.tsv" "$B/mode/$m/rep$arm" "$B/mode/$m/log$arm" \
       > "$B/mode/$m/$arm.log" 2>&1 &
    echo "$! mode-$m-$arm" >> "$B/PIDS"
  done
  wait
  echo "MODE $m done $(date -u +%H:%M:%SZ)"
done
echo "MODE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
