#!/bin/bash
# v522 PER-CHANGE VERIFICATION -- every mutant driven, zero-vs-nonzero.
# 7 arms x 36 games (6 maps x 3 seeds x 2 seats), BOTH instruments ON, vs
# `_v488beltbreak2`.  ⛔ The WIN column of a mechanism arm is not read.
# ⭐ `mOff`'s columns are REAL ZEROES, not void: both log flags are gated on
# themselves rather than on the master, so the denominators still print.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v522_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export SEEDS=61,62,63
export PAR=4
LOGS=("FS_V522_MAG_LOG = True" "FS_V522_PH_LOG = True")
mk () { NAME=$1; shift; SRC=bots/_v522floor "$B/mkarm.sh" "$NAME" "${LOGS[@]}" "$@" >/dev/null; }
mk mF
mk mFLOOR "FS_V522_FLOOR = False"
mk mCHAN  "FS_V522_PHASE_ONLY = True"
mk mFUND  "FS_V522_CORE_FUND = True"
mk mCREW  "FS_V522_CREW_READ = False"
mk mBIND  "FS_V522_BIND_IF = False"
mk mOff   "LOKI_FS_V522 = False"
for a in mF mFLOOR mCHAN mFUND mCREW mBIND mOff; do
  mkdir -p "$B/mech/$a"
  .venv/bin/python "$B/run_grid.py" "$B/arms/$a" \
      "$B/mech/$a/res.tsv" "$B/mech/$a/rep" "$B/mech/$a/log" \
      > "$B/mech/$a/run.log" 2>&1 &
  echo "$! $a" >> "$B/PIDS"
done
wait
echo "MECH DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
