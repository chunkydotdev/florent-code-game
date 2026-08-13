#!/bin/zsh
# MAPCODE leg executor — PREREG-mapcode-live-2026-08-13.md AMENDMENT 1 sequence.
# Run ONLY on an observed pairing (the watcher's PAIRING OBSERVED line).
cd /Users/junghard/Projects/Work/florent-code-game || exit 2
set -u
TARGET=648d1d5b-5443-4257-a0aa-7048661b612d   # team lazy (prereg TARGET BAND)
LOG=scratchpad/leg_mapcode_fires.tsv

# The incumbent, read LIVE at script start (never hardcoded — D28). Used only
# by the dead-process branches below: if submit_clean dies between the platform
# activation and its own restore, ITS 300s fail-safe died with it, so the
# executor restores. (Side lane s36, second executor audit.)
HOLDER_PRE=$(.venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //')
[[ -z "$HOLDER_PRE" ]] && { echo "cannot read the live holder — NOT submitting"; exit 1; }

restore_if_displaced() {
  live=$(.venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //')
  if [[ "$live" != "$HOLDER_PRE" ]]; then
    ver=$(echo "$HOLDER_PRE" | grep -o '[0-9]\+' | head -1)
    echo "DEAD-PROCESS RESTORE: live='$live' != pre='$HOLDER_PRE' — activating v$ver"
    .venv/bin/fcode submission activate "$ver"
    .venv/bin/fcode status 2>/dev/null | grep "Active bot"
  fi
}

rm -f scratchpad/LEG_FIRES_DONE
.venv/bin/python tools/submit_clean.py bots/_v197mapcode --name "Loki rc7.1" --leg \
    > scratchpad/leg_submit.log 2>&1 &
SUBMIT_PID=$!

# wait for the LIVE line (max 90s) — fire NOTHING before it
for i in $(seq 1 45); do
  grep -q "LEG MODE: .* IS LIVE" scratchpad/leg_submit.log && break
  kill -0 $SUBMIT_PID 2>/dev/null || { echo "SUBMIT DIED pre-LIVE; see leg_submit.log"; restore_if_displaced; exit 1; }
  sleep 2
done
grep -q "LEG MODE: .* IS LIVE" scratchpad/leg_submit.log || { echo "NO LIVE LINE in 90s — sentinel + verify"; touch scratchpad/LEG_FIRES_DONE; sleep 8; restore_if_displaced; exit 1; }
echo "$(date -u +%H:%M:%SZ) PROTOTYPE LIVE — firing 5"

n=0
for i in 1 2 3 4 5; do
  r=$(.venv/bin/fcode match unrated "$TARGET" --json 2>&1)
  case "$r" in
    *matchId*) v=ACCEPT; n=$((n+1));;
    *"Rate limit"*) v=RATELIMIT;;
    *) v=ERROR;;
  esac
  printf '%s\tfire%d\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$i" "$v" "$(echo "$r" | tr '\n' ' ' | head -c 200)" >> $LOG
  [[ $v == RATELIMIT ]] && break   # do NOT wait out a window with the prototype live
done

touch scratchpad/LEG_FIRES_DONE
wait $SUBMIT_PID
echo "$(date -u +%H:%M:%SZ) leg done: $n/5 accepted. submit_clean tail:"
tail -6 scratchpad/leg_submit.log
.venv/bin/fcode status 2>/dev/null | grep "Active bot"
