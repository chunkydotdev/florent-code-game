#!/bin/bash
# v521 PER-CHANGE VERIFICATION -- every mutant driven, zero-vs-nonzero.
# 9 arms x 36 games (6 maps x 3 seeds x 2 seats), EVERY INSTRUMENT ON, vs
# `_v488beltbreak2`.  ⛔ The WIN column of a mechanism arm is not read.
# Each sub-flag must drive its OWN instrument to exactly zero and leave the
# others standing; `mOff`'s columns are empty BY CONSTRUCTION (the logs are
# gated on the master) and are therefore VOID, not zero.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v521_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export SEEDS=61,62,63
export PAR=4
LOGS=("FS_V521_SYNC_LOG = True" "FS_V521_RUNG_LOG = True" "FS_V521_MAG_LOG = True" "FS_V521_GATEFIX_LOG = True")

mk () { NAME=$1; shift; SRC=bots/_v521sync "$B/mkarm.sh" "$NAME" "${LOGS[@]}" "$@" >/dev/null; }
mk mF
mk mSYNC   "FS_V521_SYNC = False"
mk mNEAR   "FS_V521_NEAR_CLOSE = False"
mk mHOLD   "FS_V521_HOLD = False"
mk mBUY    "FS_V521_BUYIN = False"
mk mCOLLAR "FS_V521_COLLARFIRST = False"
mk mPHASE  "FS_V521_PHASE_HONEST = False"
mk mGATE   "FS_V521_GATEFIX = False"
mk mOff    "LOKI_FS_V521 = False"

for a in mF mSYNC mNEAR mHOLD mBUY mCOLLAR mPHASE mGATE mOff; do
  mkdir -p "$B/mech/$a"
  .venv/bin/python "$B/run_grid.py" "$B/arms/$a" \
      "$B/mech/$a/res.tsv" "$B/mech/$a/rep" "$B/mech/$a/log" \
      > "$B/mech/$a/run.log" 2>&1 &
  echo "$! $a" >> "$B/PIDS"
done
wait
echo "MECH DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
