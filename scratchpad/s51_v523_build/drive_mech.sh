#!/bin/bash
# v523 PER-CHANGE VERIFICATION -- every mutant driven, zero-vs-nonzero.
# 8 arms x 36 games (6 maps x 3 seeds x 2 seats), ALL FOUR instruments ON, vs
# `_v488beltbreak2`.  ⛔ The WIN column of a mechanism arm is not read.
# ⭐ `mOff`'s columns are REAL ZEROES, not void: every log flag is gated on
# ITSELF rather than on the master, so the denominators still print.
# ⛔ FS_V522_MAG_LOG is forced ON in every arm because the FUND523 site lives
# inside the v522 magazine block, which ships behind FS_V522_FLOOR = False --
# without the log flag that site is not even REACHED and change 3's column
# would be a void zero rather than a measured one.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v523_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export SEEDS=61,62,63
export PAR=4
LOGS=("FS_V523_SALT_LOG = True" "FS_V523_CREW_LOG = True" \
      "FS_V523_FUND_LOG = True" "FS_V523_ARC_LOG = True" \
      "FS_V522_MAG_LOG = True")
mk () { NAME=$1; shift; SRC=bots/_v523eyes "$B/mkarm.sh" "$NAME" "${LOGS[@]}" "$@" >/dev/null; }
mk mF
mk mSALT  "FS_V523_SALTEYES = False"
mk mUNION "FS_V523_SALT_UNION = False"
mk mARC   "FS_V523_ARC_UNION = False"
mk mPHS   "FS_V523_PHASE_SEALED = False"
mk mCREW  "FS_V523_CREWREAD = False"
mk mFUND  "FS_V523_COREFUND = False"
mk mOff   "LOKI_FS_V523 = False"
for a in mF mSALT mUNION mARC mPHS mCREW mFUND mOff; do
  mkdir -p "$B/mech/$a"
  .venv/bin/python "$B/run_grid.py" "$B/arms/$a" \
      "$B/mech/$a/res.tsv" "$B/mech/$a/rep" "$B/mech/$a/log" \
      > "$B/mech/$a/run.log" 2>&1 &
  echo "$! $a" >> "$B/PIDS"
done
wait
echo "MECH DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
