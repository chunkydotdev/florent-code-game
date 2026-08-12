#!/bin/zsh
# SIDE-LANE PRE-ARM WATCH — s31, 2026-08-11.
#
# WHY THIS EXISTS. `ship_watch`'s slot rule ARMS only after the holder's 8th
# match (`slot_rule.ARM_AFTER = 8`). v112 shipped at 13:14Z with k=2, so for
# roughly 1.4 hours the newest ship has NO automatic stop-loss -- and it is a
# ship whose leg direction reverses on a leave-one-out. This watches the gap.
# It is DELETED when ship_watch reports armed=True; it is not a second alarm.
#
# DESIGN, each clause paid for by a prior incident:
#  * EMITS ON STATE CHANGE, not every poll -- a monitor that prints every cycle
#    trains its reader to ignore it.
#  * ANNOUNCES ITS OWN BLINDNESS. `elo_history.tsv` stalled 10x in 6,693 min
#    (5.1% of its life, longest 50 min). A healthy line and a blind line were
#    byte-identical during the 08-10 outage, so silence here is NOT safe:
#    past STALE_MIN it says so rather than going quiet (CLAUDE.md).
#  * REPORTS THE AGE OF THE NEWEST ROW on every line it emits.
#  * `elo_history.tsv` stamps LOCAL CEST with NO zone marker; converted here.
#
# Modes: WATCH_ONCE=1 single pass · WATCH_TAPE=<path> override (selftest breaks it)

TAPE=${WATCH_TAPE:-/Users/junghard/Projects/Work/florent-code-game/elo_history.tsv}
FLOOR=${WATCH_FLOOR:-1630}      # ~-36 from v112's 1666 activation: beyond 2 bad matches
STALE_MIN=${WATCH_STALE_MIN:-12}
SLEEP=${WATCH_SLEEP:-120}
STATE=""

_now_utc_epoch() { date -u +%s }

_pass() {
  if [[ ! -r "$TAPE" ]]; then
    if [[ "$STATE" != BLIND ]]; then
      echo "PREARM-WATCH BLIND $(date -u '+%Y-%m-%dT%H:%M:%SZ') — cannot read ${TAPE}; v112 is NOT being watched"
      STATE=BLIND
    fi
    return
  fi
  local row ts rating ver age_min now rowepoch
  row=$(tail -1 "$TAPE")
  ts=$(print -r -- "$row" | cut -f1)
  rating=$(print -r -- "$row" | cut -f2)
  ver=$(print -r -- "$row" | cut -f4)
  # tape is LOCAL CEST, unmarked -> parse as local, compare in epoch
  rowepoch=$(date -j -f '%Y-%m-%dT%H:%M' "$ts" +%s 2>/dev/null) || rowepoch=""
  now=$(_now_utc_epoch)
  if [[ -z "$rowepoch" ]]; then
    if [[ "$STATE" != BADROW ]]; then
      echo "PREARM-WATCH BLIND $(date -u '+%Y-%m-%dT%H:%M:%SZ') — newest row unparseable ('${ts}'); v112 is NOT being watched"
      STATE=BADROW
    fi
    return
  fi
  age_min=$(( (now - rowepoch) / 60 ))

  if (( age_min > STALE_MIN )); then
    if [[ "$STATE" != STALE ]]; then
      echo "PREARM-WATCH STALE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — newest tape row is ${age_min} min old (> ${STALE_MIN}); REFUSING A VERDICT on v112"
      STATE=STALE
    fi
    return
  fi

  if (( rating < FLOOR )); then
    if [[ "$STATE" != BREACH ]]; then
      echo "⛔ PREARM-WATCH BREACH $(date -u '+%Y-%m-%dT%H:%M:%SZ') — ${ver} rating ${rating} < floor ${FLOOR}, tape age ${age_min} min. ship_watch is UNARMED until the holder's 8th match; a rollback decision is a HUMAN one right now."
      STATE=BREACH
    fi
    return
  fi

  if [[ "$STATE" != OK ]]; then
    echo "PREARM-WATCH OK $(date -u '+%Y-%m-%dT%H:%M:%SZ') — ${ver} rating ${rating} >= floor ${FLOOR}, tape age ${age_min} min"
    STATE=OK
  fi
}

if [[ -n "$WATCH_ONCE" ]]; then _pass; exit 0; fi
echo "PREARM-WATCH ARMED $(date -u '+%Y-%m-%dT%H:%M:%SZ') — tape ${TAPE}, floor ${FLOOR}, stale>${STALE_MIN}min, cadence ${SLEEP}s"
while true; do _pass; sleep "$SLEEP"; done
