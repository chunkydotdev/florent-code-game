#!/bin/zsh
# THE FULL LEG — one command, all eight rollback-procedure steps.
# GAME CONTEXT: in-game Florent Code League; unrated mechanism probe per
# docs/research/PREREG-LIVE-ROBUSTNESS-v632heim-2026-08-23.md (ratified,
# Magnus window opened in-session "Go go!").
set -u
cd /Users/junghard/Projects/Work/florent-code-game
H=scratchpad/s57_heim0
# 0. wait for the NEXT x1:10 ladder tick (re-derived cadence), fire just after.
# NOWAIT=1 skips the wait — legal only when >=5.5 min of clear air remain.
while [ "${NOWAIT:-0}" != "1" ]; do
  M=$(date -u +%M); S=$(date -u +%S)
  if [ $((10#$M % 10)) -eq 1 ] && [ $((10#$S)) -ge 12 ] && [ $((10#$S)) -le 40 ]; then break; fi
  sleep 3
done
echo "== TICK PASSED $(date -u +%FT%TZ) — window opens =="
# 1. holder, live, verbatim (GATE 6)
.venv/bin/fcode status 2>&1 | grep "Active bot" | tee $H/leg_holder_before.txt
# 2. tree identity
.venv/bin/python tools/treehash.py bots/_v632heim | tee $H/leg_treehash.txt
# 3-4. submit as LEG (holds the slot; auto-restores on sentinel or 300s timeout)
rm -f scratchpad/LEG_FIRES_DONE
.venv/bin/python tools/submit_clean.py bots/_v632heim --name 'Skalman rc632.1' --leg > $H/leg_submit.log 2>&1 &
SUBPID=$!
# wait for activation, read V_P off the live line (never the submit echo)
VP=""
for i in $(seq 1 30); do
  sleep 3
  L=$(.venv/bin/fcode status 2>&1 | grep "Active bot")
  case "$L" in *"Skalman rc632"*) VP=$(echo "$L" | grep -oE 'v[0-9]+' | head -1); break;; esac
done
if [ -z "$VP" ]; then
  echo "⛔ ACTIVATION NOT OBSERVED — touching sentinel, aborting"
  touch scratchpad/LEG_FIRES_DONE; wait $SUBPID; exit 1
fi
echo "== PROTOTYPE LIVE AS $VP $(date -u +%FT%TZ) =="
# 5. cell 1: gsxWins, pinned to their v87 match (direct engine call —
# unrated_run.sh carries a stale hardcoded incumbent v177 and self-aborts;
# route-around per the no-tool-fix rule, defect wrap-listed)
.venv/bin/fcode match unrated ebd8d82a-7365-4ccb-af0b-defea3a1ac4d --match 1073e100-fd1d-4baf-a7d0-a33eed7d2ba4 2>&1 | tee $H/leg_cell_gsx.log | tail -4
# 6. cell 2: Jython, pinned to their v266 match
.venv/bin/fcode match unrated 8cf9b751-00d3-484a-b0ed-e3073ae1d46f --match 7f9f7202-5e6b-4d2e-b268-1e0706865ae2 2>&1 | tee $H/leg_cell_jyt.log | tail -4
# brief completion poll so the readout can find both match ids
sleep 25
.venv/bin/fcode match list --mine 2>/dev/null | head -8 | tee $H/leg_window_matches.txt
# 7. release the hold
touch scratchpad/LEG_FIRES_DONE
wait $SUBPID
# 8. confirm restore on the same line (never on exit codes)
AFTER=$(.venv/bin/fcode status 2>&1 | grep "Active bot")
echo "RESTORE READS: $AFTER"
echo "EXPECTED:      $(cat $H/leg_holder_before.txt)"
if [ "$AFTER" = "$(cat $H/leg_holder_before.txt)" ]; then
  echo "✅ RESTORE CONFIRMED"
else
  echo "⛔ RESTORE MISMATCH — check immediately: .venv/bin/fcode status"
fi
echo "== LEG DONE $(date -u +%FT%TZ) — audit next: fcode match list --mine --type ladder =="
