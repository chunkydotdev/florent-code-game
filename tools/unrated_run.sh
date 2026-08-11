#!/bin/zsh
# UNRATED RUN — queue N unrated games for a prototype, protect the ladder, report
# every game, exit clean when N is reached.
#
#   tools/unrated_run.sh <version> <games> [opponent_id ...]
#   tools/unrated_run.sh 108 50
#   tools/unrated_run.sh 108 25 eceb8455-... b2deaacd-...
#
# Spec, Magnus 2026-08-11: "take the number of games we want to play and the id of
# the bot we want to run, switch back to the main bot after runs are queued so the
# ladder isn't damaged, report back every game that is run with progress, exit
# cleanly when the amount of games you want has been done."
#
# IMPLEMENTS: D45 (own ledger is authority for own spend), D46 (submitting IS
# shipping), D44 (a claim needs a record -- see docs/legs/LEG-unrated-run-abort-
# guard-2026-08-11.md), D50 (verify exit codes without a pipe).
#
# ===== EVERY GUARD BELOW IS AN INCIDENT, NOT A PRECAUTION =====
#
# 1. SUBMITTING IS SHIPPING. `fcode submit` AUTO-ACTIVATES what it uploads. This
#    runner therefore takes an ALREADY-SUBMITTED version number and never submits.
#    (s29: a submit put an unmeasured prototype on the rated ladder instantly.)
#
# 2. THE OUTFILE MUST BE `scratchpad/arm_*.txt`. `tools/rate_budget.py` attributes
#    our spend by globbing exactly that — the platform supplies no actor field, so
#    the glob IS the contract. (s29: a hand-rolled runner wrote `loki19_ctrl_w1.txt`,
#    the meter could not attribute five challenges, reported "a slot is free NOW"
#    into a spent window, and the next window came back 0/5 rejected.)
#
# 3. GATE ON THE `Active bot:` LINE, NEVER ON `$?`. `fcode status` exits 0 while
#    printing `Error: True`, and `fcode match list` exits 1 on a healthy list.
#
# 4. THE LADDER PAIRS ON A CLOCK. Pairings land on a fixed second-of-20-minutes
#    (observed `:12:59`/`:32:59`/`:52:59`, 55 of 60 matches). The prototype is live
#    for ~20 seconds, so firing just after a pairing gives ~19 minutes of clear
#    air. THE OFFSET IS DERIVED FROM RECENT ROWS, NEVER HARDCODED — it has shifted
#    at least once inside an 18-hour span.
#    ⚠ AND WHEN THE PAIRING CLOCK CANNOT BE READ, THIS WAITS `GUARD_S` RATHER THAN
#    PROCEEDING. It used to return 0 — i.e. fail OPEN on the one guard whose
#    failure mode IS the incident it was built for. Blocking forever on a flaky
#    API is its own failure, so the unreadable case takes a BOUNDED conservative
#    wait instead of either extreme. The trade is stated rather than implied:
#    worst case we wait GUARD_S too long; the alternative worst case is a
#    prototype live across a pairing at roughly −8 Elo.
#
# 5. REJECTED ATTEMPTS COUNT AGAINST THE RATE LIMIT and create no match, so they
#    are invisible to the meter. The meter is a LOWER bound.
#
# 7. ⛔ THE METER LAGS REALITY BY ~25 SECONDS AND THIS RUNNER SPUN ON IT.
#    `fcode match list` does not show a match the instant it is created, so a
#    back-to-back run reads a window that is already spent as FREE.
#    MEASURED 2026-08-11 05:21Z, this runner's first prototype outing: a control
#    window fired 5 challenges at 05:21:03-13; the treatment run started at
#    05:21:35, the meter reported a free slot, and the runner ACTIVATED v108 and
#    burned 5 rejections. It then looped and did it twice more —
#    **3 activations, 15 rejections, ZERO games** — because a zero-accept cycle
#    retried immediately against the same stale reading.
#    ⇒ TWO FIXES, BOTH BELOW: (a) THE RUNNER KEEPS ITS OWN LEDGER and is the
#      authority on its own attempts — it knows what it fired and when, including
#      rejections, which the meter can never see; the effective wait is
#      max(meter, own ledger). (b) a cycle that accepts NOTHING backs off a full
#      window instead of retrying at once.
#    The meter stays in the loop because it sees OTHER lanes' spend, which the
#    ledger cannot. Neither is sufficient alone.
#
# 6. ROLLBACK IS VERIFIED, RETRIED, AND ITS FAILURE IS LOUD. Two prior sessions
#    left a non-incumbent live.
#
# ===== THE ABORT BRANCH, MUTATION-TESTED ON THIS FILE AND NOT INHERITED =====
# This runner is the FOURTH copy of the holder-assertion guard. The house rule
# (night_collector.sh's own header) is that a copied guard carries a copied
# CITATION and not a copied TEST, and `tools/claim_check.py` stays silent here
# because this file makes no claim to check -- silence from a checker whose
# predicate was never triggered is not evidence.
#
#   2026-08-11 05:04:39Z   MAIN=999 zsh tools/unrated_run.sh 108 10
#     -> "ABORT: expected incumbent v999, holder is 'v104 (Loki v2)'. Firing nothing."
#     -> exit 1 (checked WITHOUT a pipe: `$?` behind `| tail` is tail's status,
#        which reads 0 and is the exact trap this repo logged against `fcode`)
#     -> scratchpad/arm_unrated_v108_*.txt created and EMPTY: zero challenges fired
#   RE-RUN 2026-08-11 05:08:42Z   after the guard-2/4/5 hardening touched this path
#     -> ABORT, exit 1, arm file EMPTY. Same result. (The rule is "re-run after
#        any edit to the holder logic"; this is that rule applied to its own file
#        rather than asserted about it.)
#   Also verified the same run: the pairing helper returns -1 on unreadable input
#   (bounded wait, guard 4) and 281s on a healthy read, landing on the observed
#   :12:59 pairing -- so it is derived, not assumed, in both directions.
#
#   Re-run it after any edit to the holder logic. It is the guard standing
#   between us and another prototype on the rated ladder.
set -u
cd /Users/junghard/Projects/Work/florent-code-game

VER=${1:?usage: unrated_run.sh <version> <games> [opponent_id ...]}
WANT=${2:?usage: unrated_run.sh <version> <games> [opponent_id ...]}
shift 2
CELLS=("$@")
if [ ${#CELLS[@]} -eq 0 ]; then
  # PANEL-3 admitted cells + Landers. Named here so a bare invocation is
  # reproducible rather than depending on what the caller remembered.
  CELLS=(eceb8455-7cb3-442b-ba40-c6597c16b446   # Lunds Stallions
         b2deaacd-08ad-4c14-b97b-b4f382d82ea3   # Askar City
         7fd91e77-812c-44da-bce7-457be94d2548   # Powered by SmartFridge
         25288fdb-f3a0-4ae2-964f-2fd7eb9b11d7   # farming_200s
         b538e523-2250-4c1d-b718-e73b77ebad55)  # Landers
fi

# ⛔ MOVED 104 -> 112 on 2026-08-11 (s32). PROGRAMME.md:169 ALREADY ASSERTED THIS
# HAD MOVED -- *"h2h.sh/dose.py defaults and unrated_run.sh's MAIN all moved on
# 2026-08-11"* -- and h2h.sh:38 and dose.py:89 DID move at 13:2xZ when v112
# shipped. This one did not. The programme stated a fact about the tree that was
# false for five hours, on the same line every lane cites as the authority for
# moving controls.
# NOT COSMETIC, though it failed safe: line ~177 aborts unless the holder is
# v$MAIN, so with the holder at v112 and MAIN at 104 the runner REFUSES TO FIRE.
# The standing obligation is that a leg is always ready; the next unrated leg
# would have died at pre-flight instead of rolling the ladder back to v104.
# A guard that refuses everything is the failure this repo logged twice today.
MAIN=${MAIN:-114}                # the incumbent to return the ladder to
GAMES_PER=5                      # a challenge is 5 games
GUARD_S=${GUARD_S:-150}          # keep this clear of the next pairing
WINDOW_S=${WINDOW_S:-1230}       # the rate window + margin, for a zero-accept backoff
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT=scratchpad/arm_unrated_v${VER}_${STAMP}.txt      # MUST match arm_*.txt (guard 2)
LOG=scratchpad/unrated_run_v${VER}_${STAMP}.log
: > "$OUT"; : > "$LOG"

say(){ print -r -- "$(date -u +%H:%M:%SZ) $*" | tee -a "$LOG"; }
holder(){ .venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //'; }

# --- guard 6: restore the incumbent, verify, and shout if it did not take ------
restore(){
  local tries=0 h
  while [ $tries -lt 4 ]; do
    .venv/bin/fcode submission activate "$MAIN" >/dev/null 2>&1
    sleep 2
    h=$(holder)
    case "$h" in
      v${MAIN}*) say "rollback confirmed: holder=$h"; return 0 ;;
    esac
    tries=$((tries+1)); say "rollback attempt $tries did not take (holder='$h'), retrying"
    sleep 3
  done
  say "*** ROLLBACK FAILED after 4 tries. HOLDER='$h'. THE LADDER IS RUNNING THE"
  say "*** WRONG BOT. Fix by hand NOW: .venv/bin/fcode submission activate $MAIN"
  print -r -- "$(date -u +%H:%M:%SZ) rollback failed, holder=$h" >> corpus/HOLDER_ALERT
  return 1
}
trap 'say "interrupted — restoring incumbent"; restore; exit 130' INT TERM

# --- guard 4: seconds until safely past the next pairing -----------------------
# Derives the offset from the last few ladder pairings instead of assuming it.
secs_to_safe_gap(){
  .venv/bin/fcode match list --mine --type ladder --json --limit 8 2>/dev/null \
  | .venv/bin/python -c '
import json,sys,re
from datetime import datetime,timezone,timedelta
try:
    d=json.load(sys.stdin)
except Exception:
    print(-1); raise SystemExit         # unreadable -> caller applies a bounded wait
rows=d if isinstance(d,list) else d.get("matches",d.get("data",[]))
ts=[]
for m in rows:
    c=m.get("createdAt")
    if c:
        try: ts.append(datetime.fromisoformat(c.replace("Z","+00:00")))
        except ValueError: pass
if len(ts)<3: print(-1); raise SystemExit   # too little history to derive a period
ts.sort(reverse=True)
last=ts[0]
# period from consecutive gaps, snapped to the nearest minute; falls back to 1200
gaps=[(ts[i]-ts[i+1]).total_seconds() for i in range(min(4,len(ts)-1))]
gaps=[g for g in gaps if 300<=g<=3600]
period=min(gaps) if gaps else 1200
now=datetime.now(timezone.utc)
nxt=last
while nxt<=now: nxt=nxt+timedelta(seconds=period)
print(int((nxt-now).total_seconds()))
' 2>/dev/null || echo -1
}

say "UNRATED RUN  version=v$VER  target=$WANT games  incumbent=v$MAIN"
say "cells=${#CELLS[@]}  outfile=$OUT   (arm_*.txt so rate_budget can attribute it)"

h=$(holder)
case "$h" in
  v${MAIN}*) say "holder before: $h" ;;
  *) say "ABORT: expected incumbent v$MAIN, holder is '$h'. Firing nothing."; exit 1 ;;
esac

# --- guard 7a: our own spend ledger, in epoch seconds, attempts not matches ----
# PERSISTED TO A SHARED FILE, and that is not a detail: an in-memory ledger dies
# with the process, so a FRESH invocation starts blind to what the previous one
# spent. Rejections are the case that makes this bite -- they count against the
# limit but create no match, so they are invisible to the meter AND to a new
# process. After the 05:21Z spin, 15 rejections sat in the window and NOTHING
# could see them. The file is shared, so a second runner in another lane inherits
# them too.
LEDGER=${LEDGER:-scratchpad/.rate_ledger}

# --- guard 7c: THE MATCH-INITIATIVE LEDGER (Magnus's ask, s30) -----------------
# `.rate_ledger` above is 25 lines of bare unix timestamps -- it knows we spent
# budget and NOTHING about on what. `fcode match list --mine` mixes matches WE
# created with matches opponents created against US, `triggeredBy` is the match
# TYPE not the actor, and sourceMatchAId/BId are null: NOTHING ON THE PLATFORM
# RECORDS WHO PRESSED THE BUTTON. s28's meter read `7 of 5` because two of the
# seven were an opponent challenging us, and that was caught ONLY because 7-of-5
# is arithmetically impossible -- ONE foreign challenge reads a plausible 5/5 and
# silently stalls this runner.
# REFUSE BEFORE FIRING IF THE LEDGER IS BLIND. An unrecorded match is the exact
# defect being fixed, so firing unrecorded is not a degraded mode, it is the bug.
if ! .venv/bin/python tools/match_ledger.py preflight; then
  say "ABORT: match ledger is BLIND. Firing nothing — an unrecorded match is the"
  say "       defect this ledger exists to fix, so we do not fire without it."
  exit 1
fi
ARM_TAG=${ARM_TAG:-unrated_v${VER}_${STAMP}}
typeset -a ATTEMPTS
[ -f "$LEDGER" ] && ATTEMPTS=($(tail -50 "$LEDGER"))
note_attempt(){ local ts=$(date -u +%s); ATTEMPTS+=($ts); print -r -- $ts >> "$LEDGER"; }
local_wait(){
  local now cutoff n oldest
  now=$(date -u +%s); cutoff=$((now - 1200)); n=0; oldest=0
  for ts in $ATTEMPTS; do
    if [ "$ts" -ge $cutoff ]; then
      n=$((n+1)); [ $oldest -eq 0 ] && oldest=$ts
    fi
  done
  if [ $n -ge 5 ]; then echo $(( oldest + 1200 - now + 5 )); else echo 0; fi
}

done_games=0; fired=0; rejected=0; ci=0; cycle=0
while [ $done_games -lt $WANT ]; do
  cycle=$((cycle+1))

  # guard 5: pace off the meter, which is a LOWER bound
  w=$(.venv/bin/python tools/rate_budget.py --wait 2>/dev/null || echo 1200)
  # `--wait` ALWAYS exits 0, so the `||` fallback only catches a crash, never bad
  # output. If that path ever prints anything besides the bare integer -- a
  # warning line, a blank -- `w` goes multi-line and `-gt` errors. Safe today
  # only because `--wait` returns before anything is printed, which is a property
  # of rate_budget's current control flow and NOT a contract; that file changed
  # twice in the hour before this was written. Same guard as night_collector.sh.
  [[ "$w" =~ ^[0-9]+$ ]] || { say "rate meter returned non-numeric output — assuming a full window"; w=1200; }
  # guard 7a: the meter lags ~25s, so take the max of it and our own ledger.
  lw=$(local_wait)
  if [ "$lw" -gt "$w" ]; then
    say "own ledger says wait ${lw}s (meter said ${w}s — it lags ~25s); taking the ledger"
    w=$lw
  fi
  if [ "${w:-0}" -gt 0 ]; then
    say "rate: waiting ${w}s for a slot"
    sleep "$w"
  fi

  # guard 4: do not hold the prototype live across a pairing
  g=$(secs_to_safe_gap)
  [[ "$g" =~ ^-?[0-9]+$ ]] || g=-1
  if [ "$g" -lt 0 ]; then
    say "pairing clock UNREADABLE — waiting ${GUARD_S}s (bounded, fail-safer; see guard 4)"
    sleep $GUARD_S
  elif [ "$g" -lt $GUARD_S ]; then
    say "pairing in ${g}s — waiting past it before activating"
    sleep $((g+15))
  fi

  remaining=$(( (WANT - done_games + GAMES_PER - 1) / GAMES_PER ))
  n_this=$(( remaining < 5 ? remaining : 5 ))

  h=$(holder)
  case "$h" in v${MAIN}*) ;; *) say "ABORT mid-run: holder='$h' not v$MAIN"; restore; exit 1;; esac

  .venv/bin/fcode submission activate "$VER" >/dev/null 2>&1
  sleep 2
  h=$(holder)
  case "$h" in
    v${VER}*) say "cycle $cycle: activated $h — firing $n_this challenge(s)" ;;
    *) say "cycle $cycle: ACTIVATE FAILED (holder='$h') — restoring, no challenges fired"
       restore; exit 1 ;;
  esac

  got=0
  for i in $(seq 1 $n_this); do
    id=${CELLS[$(( ci % ${#CELLS[@]} + 1 ))]}   # zsh arrays are 1-based
    ci=$((ci+1))                                 # rotate so drops don't bias one cell
    r=$(.venv/bin/fcode match unrated "$id" --json 2>&1 | tr -d '\n')
    note_attempt                   # guard 7a: EVERY attempt, accepted or not, persisted
    print -r -- "$id $r" >> "$OUT"
    # guard 7c: stamp our initiative at the moment the CLI returns. Rejections
    # get a row too (match_id=REJECTED) because they consume the rate window; a
    # success-only ledger under-counts in the direction that matters. The tool
    # gates on the presence of `matchId` in the body, NEVER on $? -- this CLI
    # exits 0 while printing `Error: True`.
    print -r -- "$r" | .venv/bin/python tools/match_ledger.py record \
      --type unrated --opponent-id "$id" --opponent-name "$id" \
      --our-version "v$VER" --arm-tag "$ARM_TAG" --runner unrated_run.sh >/dev/null
    case "$r" in
      *matchId*)
        got=$((got+1)); fired=$((fired+1))
        done_games=$((done_games + GAMES_PER))
        say "  queued ${id:0:8}  +${GAMES_PER} games   PROGRESS ${done_games}/${WANT}"
        ;;
      *)
        rejected=$((rejected+1))
        say "  REJECTED ${id:0:8} (counts against the limit even though no match exists)"
        ;;
    esac
    sleep 2
  done

  # guard 1/6: the prototype goes back in the box the moment queuing is done
  restore || exit 1
  say "cycle $cycle: queued $got/$n_this   total ${done_games}/${WANT} games"

  [ $done_games -ge $WANT ] && break
  if [ $got -eq 0 ]; then
    # guard 7b: a zero-accept cycle means the window was spent despite what the
    # meter said. Retrying at once re-activates the prototype and burns five more
    # rejections, which is exactly what happened at 05:21-05:22Z.
    say "NOTHING accepted this cycle — the window was spent. Backing off ${WINDOW_S}s before retrying."
    sleep $WINDOW_S
  fi
done

say "DONE: ${done_games}/${WANT} games queued in $cycle cycle(s); $fired accepted, $rejected rejected"
h=$(holder); say "final holder: $h"
case "$h" in
  v${MAIN}*) say "ladder is on the incumbent. clean exit."; exit 0 ;;
  *) say "*** FINAL HOLDER IS NOT v$MAIN ***"; exit 1 ;;
esac
