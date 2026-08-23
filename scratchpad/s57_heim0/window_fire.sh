#!/bin/zsh
# GENERALIZED ZERO-LEAK WINDOW — usage:
#   [NOWAIT=1] window_fire.sh <tree> <legname> <opp1_id[:pin1]> [opp2_id[:pin2]] [opp3_id[:pin3]]
# GAME CONTEXT: in-game Florent Code League; unrated windows per THE FINAL
# STANDING ORDER (PROGRAMME tail — standing GO, zero-leak procedure mandatory).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
H=scratchpad/s57_heim0
TREE=${1:?tree}; LEGNAME=${2:?legname}; shift 2
# 0. clear-air wait (x1:10 cadence) unless NOWAIT=1 (legal >=5.5min air)
while [ "${NOWAIT:-0}" != "1" ]; do
  M=$(date -u +%M); S=$(date -u +%S)
  if [ $((10#$M % 10)) -eq 1 ] && [ $((10#$S)) -ge 12 ] && [ $((10#$S)) -le 40 ]; then break; fi
  sleep 3
done
TS=$(date -u +%Y%m%dT%H%M%SZ)
echo "== WINDOW $LEGNAME OPENS $(date -u +%FT%TZ) tree=$TREE =="
# teammate-traffic lull check (the ninth gate): abort if unrated created <8 min ago by us
# (best-effort textual check; a busy teammate session shows recent UR rows)
# 1. holder live (GATE 6) — with the empty-read abort (the 23:11 incident:
# a degraded status read returned NOTHING, the window opened anyway, and the
# restore had no target; a window may NEVER open without a recorded holder)
.venv/bin/fcode status 2>&1 | grep "Active bot" | tee $H/w_${TS}_holder.txt
if [ ! -s $H/w_${TS}_holder.txt ]; then
  echo "⛔ HOLDER READ EMPTY (degraded platform) — ABORTING WINDOW, nothing submitted"
  exit 3
fi
# 2. tree identity
.venv/bin/python tools/treehash.py $TREE | tee $H/w_${TS}_treehash.txt
# 3-4. submit as LEG (300s structural hold)
rm -f scratchpad/LEG_FIRES_DONE
.venv/bin/python tools/submit_clean.py $TREE --name "$LEGNAME" --leg > $H/w_${TS}_submit.log 2>&1 &
SUBPID=$!
VP=""
for i in $(seq 1 30); do
  sleep 3
  L=$(.venv/bin/fcode status 2>&1 | grep "Active bot")
  case "$L" in *"$LEGNAME"*) VP=$(echo "$L" | grep -oE 'v[0-9]+' | head -1); break;; esac
done
if [ -z "$VP" ]; then
  echo "⛔ ACTIVATION NOT OBSERVED — sentinel + abort"
  touch scratchpad/LEG_FIRES_DONE; wait $SUBPID; exit 1
fi
echo "== PROTOTYPE LIVE AS $VP =="
# 5. fire all cells (direct engine calls; pins optional as opp:pin)
for CELL in "$@"; do
  OPP=${CELL%%:*}; PIN=${CELL#*:}
  if [ "$PIN" = "$CELL" ]; then
    .venv/bin/fcode match unrated "$OPP" 2>&1 | grep -E "Match ID|Error" | tee -a $H/w_${TS}_cells.log
  else
    .venv/bin/fcode match unrated "$OPP" --match "$PIN" 2>&1 | grep -E "Match ID|Error" | tee -a $H/w_${TS}_cells.log
  fi
done
# 6. release + restore
touch scratchpad/LEG_FIRES_DONE
wait $SUBPID
AFTER=$(.venv/bin/fcode status 2>&1 | grep "Active bot")
echo "RESTORE READS: $AFTER"
echo "EXPECTED:      $(cat $H/w_${TS}_holder.txt)"
if [ "$AFTER" = "$(cat $H/w_${TS}_holder.txt)" ]; then
  echo "✅ RESTORE CONFIRMED"
else
  echo "⛔ RESTORE MISMATCH — CHECK NOW"
  { echo "RESTORE MISMATCH $(date -u +%FT%TZ) window=$LEGNAME"
    echo "EXPECTED: $(cat $H/w_${TS}_holder.txt)"
    echo "READS:    $AFTER"; } > corpus/RESTORE_MISMATCH
  echo "== WINDOW $LEGNAME DONE-WITH-MISMATCH $(date -u +%FT%TZ) =="
  exit 2
fi
echo "== WINDOW $LEGNAME DONE $(date -u +%FT%TZ) — match ids in $H/w_${TS}_cells.log =="
