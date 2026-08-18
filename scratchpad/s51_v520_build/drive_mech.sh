#!/bin/bash
# v520 MECHANISM ARMS.  n=36 each (6 maps x 3 seeds x 2 seats), every
# instrument ON.  ⛔ THE WIN COLUMN OF A MECHANISM ARM IS NOT READ -- the
# instruments cost CPU and the arms are n=36.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v520_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export SEEDS=101,102,103
export PAR=3
INST="FS_V520_SPLIT_LOG = True|FS_V520_TERM_LOG = True|FS_V520_ARC_LOG = True|FS_V520_PRES_LOG = True|FS_V520_APPT_LOG = True|FS_V519_GF_LOG = True|FS_LOG = True"
IFS='|' read -r -a I <<< "$INST"

mk () { bash "$B/mkarm.sh" "$@" >/dev/null; }
mk mF   "${I[@]}"
mk mP   "${I[@]}" "FS_V520_PINCER = False"
mk mR   "${I[@]}" "FS_V520_PRESENCE = False"
mk mG   "${I[@]}" "FS_V520_GUNNEAR = False"
mk mS   "${I[@]}" "FS_V520_SPLIT = False"
mk mT   "${I[@]}" "FS_V520_TERMSITE = False"
mk mA   "${I[@]}" "FS_V520_ARC_SEAL = False"
mk mOff "${I[@]}" "LOKI_FS_V520 = False"

for a in mF mP mR mG mS mT mA mOff; do
  mkdir -p "$B/mech/$a"
  .venv/bin/python "$B/run_grid.py" "$B/arms/$a" \
      "$B/mech/$a.tsv" "$B/mech/$a/rep" "$B/mech/$a/log" \
      > "$B/mech/$a.log" 2>&1
  echo "MECH $a done $(date -u +%H:%M:%SZ)"
done
echo "MECH DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
