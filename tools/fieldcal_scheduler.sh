#!/bin/zsh
# FIELDCAL SCHEDULER — drives LEG-fieldcal-2026-08-16 (docs/prereg/LEG-fieldcal-2026-08-16.md).
#
#   tools/fieldcal_scheduler.sh              # run (resumes from scratchpad/fieldcal_state.tsv)
#   tools/fieldcal_scheduler.sh --selftest   # prove every branch, touches no network
#
# WHAT THIS IS. `tools/unrated_run.sh` (§9.4.1-2 of the prereg) is the ONLY runner
# with a pin path, but at one cell per invocation it cannot alternate arms, rotate
# a starting cell across 10 opponents, or gate on account-wide spend -- those are
# explicitly SCHEDULER duties (§9.4.2, §9.6a, §9.6b). This file is that scheduler.
# It calls unrated_run.sh, never `fcode` directly.
#
# THE DESIGN, exactly as ratified (§10.2/10.3 BETWEEN-WINDOWS ruling):
#   - 20 (arm, cell) pairs, target 12 accepts each = 240 accepts = 1,200 games.
#   - One ROUND = one 20-minute window = one arm. Round k (0-based): arm = A if
#     (k mod 2)==0 else B; start cell = (k/2) mod 10 (integer division, so each
#     arm's OWN rotation advances every time that arm fires -- not every round).
#   - Within a round: up to 5 accepts (the window budget), walking cells from the
#     round's start cell in rotation order. ONE unrated_run.sh invocation per
#     cell, target = min(accepts remaining this round, 12 - already banked for
#     that arm+cell). A cell already at 12/12 is skipped, not fired.
#   - Before EVERY invocation: gate on `tools/rate_budget.py` (account-wide,
#     sees teammates' spend too -- §9.6a). A nonzero wait SLEEPS AND RE-CHECKS
#     THE SAME CELL. It never advances the cell -- that would recreate the
#     `fanout.sh` starvation class through a different door (§9.6b).
#
# ⛔ MAIN vs RESTORE_TO, VERIFIED AGAINST unrated_run.sh RATHER THAN GUESSED.
# unrated_run.sh:250 captures RESTORE_TO from the LIVE holder immediately before
# every upload -- that is fully internal and automatic, and this scheduler never
# touches it. MAIN is different: it is ONLY the pre-flight "is this a foreign
# holder" comparison (unrated_run.sh:254-261), derived by DEFAULT from
# PROGRAMME.md's INCUMBENT (registered today as v140/_v223sealrepair) via
# corpus/version_trees.tsv. Read live at build time: `corpus/version_trees.tsv`
# line 86 has v152 as `bots/_x3r0v152 (teammate, STAGED from platform artifact)`,
# i.e. the PRE-LEG HOLDER (per the leg's own design note) is v152 -- NOT the
# registered INCUMBENT v140. Left to its own default, unrated_run.sh's guard
# would therefore ABORT every single invocation of THIS leg (actual holder v152
# != derived MAIN v140), for BOTH arms. So FIELDCAL_MAIN defaults to 152 here and
# is passed as `MAIN=` on every call. If the real holder has since changed
# legitimately, override with `FIELDCAL_MAIN=<n>` -- a wrong value fails SAFE
# (unrated_run.sh aborts and fires nothing) rather than silently clobbering an
# unexpected holder.
#
# THE OUTFILE CONTRACT. unrated_run.sh computes its own outfile name internally
# (`scratchpad/arm_unrated_v${VER}_${STAMP}.txt`) and there is no override for
# it -- `tools/rate_budget.py` globs exactly `scratchpad/arm_*.txt` to attribute
# spend (its own guard 2), so this scheduler must NOT rename or move that file
# out of the glob. Instead it reads the exact path off the runner's own printed
# `outfile=...` line (guard 2's own citation) and APPENDS a copy into
# `scratchpad/arm_fieldcal_<arm>_<label>.txt` (itself `arm_*.txt`, so the meter
# stays able to see it too) for this leg's own per-cell bookkeeping. Each row in
# that file is `<team_id> <json blob, no newlines>`; an accepted row contains
# `"matchId"` and `"createdAt"`, a rejected row does not.
#
# WINDOW COMPOSITION, STATED SO IT IS NOT MISTAKEN FOR A BUG. unrated_run.sh
# paces itself internally (its own guard 5/7a, `rate_budget.py` + its local
# ledger) and backs off a full window on a zero-accept cycle; it loops until its
# own WANT is reached, however many windows that takes. This scheduler's
# pre-invocation gate (§9.6a) is a SEPARATE, required layer -- it sees
# account-wide spend (teammates included) before we even try to activate a
# prototype, so we do not activate INTO a window we can already see is spent.
# In the common uncontested case both checks agree and the second one is a
# no-op (near-zero-cost re-read); under contention the runner's OWN internal
# wait is what actually absorbs the extra delay, correctly, and can carry a
# round past its nominal 20 minutes. The 16h/600-per-arm figure is therefore a
# FLOOR, never a promise (prereg §9.6a) -- this scheduler does not paper over
# that, it composes with it.
#
# THE -40 ELO HALT (§10.5b) IS EVALUATED BEFORE EVERY ROUND, ONCE CLOCK2 IS
# KNOWN, off corpus/ladder_games.tsv (never elo_history.tsv, which tags by
# POLL-time version -- CLAUDE.md's standing rule). No `eloDelta` column exists
# on that tape; delta is reconstructed per match as `32 * (S - E)` from
# ourbef/oppbef/won, exactly `tools/ship_ledger.py`'s verified model (residual
# 0.000000 there). ⛔ BLIND IS ABSOLUTE-AGE, NOT CLOCK2-RELATIVE (side-lane
# correction, 2026-08-16, driven live: the archive was 76 min behind and an
# earlier draft of this gate read that as "clear" purely because the FILTERED
# subset was empty). The newest row's age is measured over the WHOLE tape,
# unfiltered, and if it exceeds ~2 pairing cadences (default 40 min) the read is
# BLIND REGARDLESS OF WHAT THE FILTERED SUM COMPUTES TO -- a stale-but-nonempty
# tape must read BLIND exactly like a stale-and-empty one, never "clear from
# emptiness". Three consecutive BLIND reads stop the scheduler for a human.
#
# HALT FILE: scratchpad/FIELDCAL_HALT, checked before every invocation and
# again after any budget wait. unrated_run.sh restores the pre-upload holder
# ITSELF at the end of every firing cycle and on SIGINT/SIGTERM (its own trap) --
# this scheduler never duplicates that logic, it only refrains from calling the
# runner again once HALT is seen. Between scheduler invocations the ladder is
# therefore always at rest on the pre-leg holder; the one gap this scheduler
# cannot close is a HALT file dropped WHILE unrated_run.sh is already running --
# send it SIGTERM/SIGINT directly (or the whole process group) to invoke its own
# trap-based restore immediately.
#
# STATE: scratchpad/fieldcal_state.tsv, rewritten atomically (tmp + mv) after
# every accept, every clock2 capture, and every elo-gate read. This file IS the
# two-session handover (prereg §10.4) -- a successor reads it and resumes.
set -u
cd /Users/junghard/Projects/Work/florent-code-game

# ===========================================================================
# THE CELL TABLE — registered in docs/prereg/LEG-fieldcal-2026-08-16.md §1/§10.
# Every id is validated present-and-well-formed (36-char UUID) at startup; a
# bad one is a REFUSAL, not a warning (see validate_ids/startup below).
# ===========================================================================
typeset -a CELL_ORDER
CELL_ORDER=(Juusto not_adgato Erebus kladde gsxWins 0033 lingling_40h HTTP_418 The_Bisons farming_200s)

typeset -A CELL_TEAM CELL_PIN
CELL_TEAM[Juusto]=32087804-2dde-4265-acb2-b6ec9039fbee
CELL_PIN[Juusto]=246843da-fd15-435a-ab03-d61ff7a68ceb
CELL_TEAM[not_adgato]=fb0e7053-f8f3-4cc8-a38f-1856a518c7d2
CELL_PIN[not_adgato]=fbebd601-2c89-4f73-adab-faf980b1368f
CELL_TEAM[Erebus]=9810ba35-66a9-4af3-9a2f-06651aef4109
CELL_PIN[Erebus]=1017fe8c-ba37-49e6-9a6d-55166562e782
# ⛔⛔ BUILDER-FILLS. kladde's team id is TRUNCATED in the source instruction
# (`c7571c87-f960-4c88-a13d-XXXX`) and this agent runs no platform commands, so
# it cannot be recovered here. The placeholder below is DELIBERATELY not a
# well-formed UUID -- validate_ids() below REFUSES to run (exit 2) while it
# stands. Fill it from `.venv/bin/fcode team search kladde` before firing.
CELL_TEAM[kladde]="c7571c87-f960-4c88-a13d-14340bb3200f"  # filled by the builder from live `fcode team search kladde --json` (teamId), 2026-08-16 ~06:2xZ
CELL_PIN[kladde]=5b1ad1be-8d85-4dc6-9edc-db6ff01ef90a
CELL_TEAM[gsxWins]=ebd8d82a-7365-4ccb-af0b-defea3a1ac4d
CELL_PIN[gsxWins]=2398e4c4-1879-40c1-bbfc-b826a370a75e
CELL_TEAM[0033]=74ae65ff-96ae-4da5-a43e-692eb6fee38f
CELL_PIN[0033]=997b672e-f9f3-4114-ba3c-63fbd8db0e34
CELL_TEAM[lingling_40h]=86d0b484-783c-47dc-99d9-6ed9af2794f8
CELL_PIN[lingling_40h]=22da9159-8db9-4946-b9db-867b016fa919
CELL_TEAM[HTTP_418]=12fdece5-48c9-4913-9533-6d95b73e22ab
CELL_PIN[HTTP_418]=0370222d-f731-4a02-ae6b-815d88822f8b
CELL_TEAM[The_Bisons]=f670dfed-dfee-421b-8c01-a67b8a278ce3
CELL_PIN[The_Bisons]=17366fbc-36f0-4613-85c0-98ece3f0aaef
CELL_TEAM[farming_200s]=25288fdb-f3a0-4ae2-964f-2fd7eb9b11d7
CELL_PIN[farming_200s]=1b720a8c-443f-42a4-a882-9a31ac7aa2c6

# ARMS — §2 of the prereg. A = control v140 (_v223sealrepair), B = treatment
# v154 (_v242bodyaware, "Loki rc10.1").
typeset -A ARM_VER ARM_TREE
ARM_VER[A]=140;  ARM_TREE[A]=bots/_v223sealrepair
ARM_VER[B]=154;  ARM_TREE[B]=bots/_v242bodyaware

GAMES_PER=5     # a challenge is 5 games -- mirrors unrated_run.sh's own GAMES_PER

# ===========================================================================
# Overridable configuration. Real defaults for a live leg; --selftest replaces
# every one of these with an isolated fixture so it touches neither the repo's
# scratchpad/ nor the network.
# ===========================================================================
FIELDCAL_MAIN=${FIELDCAL_MAIN:-152}    # pre-leg holder, see header note above
RUNNER_CMD=${RUNNER_CMD:-tools/unrated_run.sh}
BUDGET_CMD=${BUDGET_CMD:-".venv/bin/python tools/rate_budget.py --wait"}
PYTHON_BIN=${PYTHON_BIN:-.venv/bin/python}
LADDER_TSV=${LADDER_TSV:-corpus/ladder_games.tsv}
SCRATCH_DIR=${SCRATCH_DIR:-scratchpad}   # base dir for the per-cell consolidated outfiles
STATE_FILE=${STATE_FILE:-scratchpad/fieldcal_state.tsv}
HALT_FILE=${HALT_FILE:-scratchpad/FIELDCAL_HALT}
LOG_FILE=${LOG_FILE:-scratchpad/fieldcal_scheduler.log}
STALE_MIN=${STALE_MIN:-40}             # ~2 pairing cadences; absolute-age BLIND bar
# PLATFORM FALLBACK for the elo gate (side-lane design, 2026-08-16 07:0xZ): the
# archive is a CACHE of the platform, and its HEALTHY lag (30-min archiver cycle
# + match completion) routinely exceeds STALE_MIN — so a stale cache falls back
# to a LIVE platform read instead of going blind. BLIND (and the 3-strike human
# stop) survives only when BOTH surfaces fail. Same population, same per-match
# semantics (arm-played ladder matches since clock2); the wire's own
# eloDelta{A,B} field is read directly (authoritative, 677/677 agreement per
# CLAUDE.md) — never reconstructed; sides keyed on teamId, NEVER on team name
# (names change and truncate; two id-vs-name incidents today alone).
OUR_TEAM_ID=${OUR_TEAM_ID:-379a5d80-9921-4c9e-949b-f9b1dcba16be}  # OpenSverige, live `fcode team search` 2026-08-16T06:5xZ
PLATFORM_LIST_CMD=${PLATFORM_LIST_CMD:-.venv/bin/fcode match list --mine --type ladder --json --limit 60}
NOW_OVERRIDE=${NOW_OVERRIDE:-}         # ISO8601Z; testing only

# Mutable leg state (populated by load_state).
typeset -g ROUND_NUM=0
typeset -g CLOCK2=""
typeset -g BLIND_STREAK=0
typeset -gA COUNTS
typeset -g FATAL=0
typeset -g LAST_OUTFILE=""
typeset -ga SLEPT               # selftest introspection: recorded sleep durations

say(){ print -r -- "$(date -u +%H:%M:%SZ) $*" | tee -a "$LOG_FILE"; }

# ---------------------------------------------------------------------------
# 36-char UUID check. "36-char" is enforced structurally by the regex, not by
# a separate length test.
# ---------------------------------------------------------------------------
uuid_ok(){ [[ "$1" =~ ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$ ]]; }

# validate_ids(): args are "label|team_id|pin_id" triples. Prints every bad
# entry (label + which field) and returns nonzero if ANY are bad. A malformed
# id is a REFUSAL at the caller, never a warning that is merely logged.
validate_ids(){
  local -a triples; triples=("$@")
  local bad=0 t label team pin
  for t in $triples; do
    label=${t%%|*}
    local rest=${t#*|}
    team=${rest%%|*}
    pin=${rest#*|}
    if ! uuid_ok "$team"; then say "  REFUSAL: cell '$label' team id is not a well-formed 36-char UUID: '$team'"; bad=1; fi
    if ! uuid_ok "$pin";  then say "  REFUSAL: cell '$label' pin id is not a well-formed 36-char UUID: '$pin'";  bad=1; fi
  done
  return $bad
}

halt_file_present(){ [[ -f "$HALT_FILE" ]]; }

do_sleep(){
  local s=$1
  if [[ -n ${FIELDCAL_TEST_NOSLEEP:-} ]]; then
    SLEPT+=("$s")
  else
    sleep "$s"
  fi
}

budget_wait(){
  local w
  w=$(${=BUDGET_CMD} 2>/dev/null)
  [[ "$w" =~ ^[0-9]+$ ]] || w=1200   # non-numeric/blind -> assume the full window
  print -r -- "$w"
}

# ===========================================================================
# STATE — atomic rewrite, resumable. This file IS the two-session handover.
# ===========================================================================
load_state(){
  ROUND_NUM=0; CLOCK2=""; BLIND_STREAK=0
  typeset -gA COUNTS
  local arm label
  for arm in A B; do for label in $CELL_ORDER; do COUNTS[$arm,$label]=0; done; done
  [[ -f "$STATE_FILE" ]] || return 0
  local k a b c
  while IFS=$'\t' read -r k a b c; do
    case "$k" in
      ROUND) ROUND_NUM=$a ;;
      CLOCK2) CLOCK2=$a ;;
      BLIND_STREAK) BLIND_STREAK=$a ;;
      COUNT) COUNTS[$a,$b]=$c ;;
    esac
  done < "$STATE_FILE"
}

persist_state(){
  local tmp="${STATE_FILE}.tmp.$$"
  {
    printf 'ROUND\t%s\n' "$ROUND_NUM"
    printf 'CLOCK2\t%s\n' "${CLOCK2:-}"
    printf 'BLIND_STREAK\t%s\n' "${BLIND_STREAK:-0}"
    local arm label
    for arm in A B; do
      for label in $CELL_ORDER; do
        printf 'COUNT\t%s\t%s\t%s\n' "$arm" "$label" "${COUNTS[$arm,$label]:-0}"
      done
    done
  } > "$tmp"
  mv -f "$tmp" "$STATE_FILE"
}

all_cells_done(){
  local arm label
  for arm in A B; do
    for label in $CELL_ORDER; do
      (( ${COUNTS[$arm,$label]:-0} < 12 )) && return 1
    done
  done
  return 0
}

# ===========================================================================
# THE RUNNER CALL AND ITS OUTFILE
# ===========================================================================
count_accepted(){ grep -c '"matchId"' "$1" 2>/dev/null; }
count_rejected(){
  local total accepted
  total=$(wc -l < "$1" 2>/dev/null); total=${total:-0}
  accepted=$(count_accepted "$1")
  print -r -- $(( total - accepted ))
}

# maybe_capture_clock2: only ever fires ONCE for the whole leg (§1 clock2).
# ⛔ REWRITTEN 06:3xZ AFTER THE FIRST LIVE WINDOW: the challenge-create response
# carries ONLY {"matchId": ...} — measured on five real accepts, zero createdAt
# fields — and `fcode match info` returns createdAt: None (the same thin-fields
# defect CLAUDE.md records for opponent versions). The AUTHORITY is
# `fcode match list --mine --type unrated`, which carried createdAt for all
# five. So: extract the matchId from the outfile, resolve createdAt by list.
_created_at_of(){  # $1 = match uuid -> prints createdAt or nothing
  .venv/bin/fcode match list --mine --type unrated --json --limit 50 2>/dev/null \
    | .venv/bin/python -c "
import json,sys
try: d=json.load(sys.stdin)
except Exception: sys.exit(0)
ms=d if isinstance(d,list) else d.get('matches',d.get('data',[]))
print(next((m.get('createdAt','') or '' for m in ms if m.get('id')==sys.argv[1]), ''))" "$1"
}
maybe_capture_clock2(){
  local outfile=$1
  [[ -n "${CLOCK2:-}" ]] && return 0
  [[ -f "$outfile" ]] || return 0
  local line mid createdat
  line=$(grep -m1 '"matchId"' "$outfile") || return 0
  mid=$(print -r -- "$line" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | tail -1)
  [[ -z "$mid" ]] && return 0
  createdat=$(_created_at_of "$mid")
  [[ -z "$createdat" ]] && { say "  clock2: matchId $mid not yet resolvable via match list — retrying at next accept"; return 0; }
  CLOCK2="$createdat"
  say "  ****** CLOCK 2 CAPTURED: first accepted challenge $mid createdAt = $CLOCK2 ******"
  persist_state
}
# backfill_clock2: on (re)start with accepts already banked but CLOCK2 empty
# (the 06:25Z window banked five accepts under the broken extractor), resolve
# the EARLIEST createdAt across every existing outfile's first accept.
backfill_clock2(){
  [[ -n "${CLOCK2:-}" ]] && return 0
  local f line mid c best=""
  for f in ${SCRATCH_DIR}/arm_fieldcal_*.txt(N); do
    line=$(grep -m1 '"matchId"' "$f") || continue
    mid=$(print -r -- "$line" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | tail -1)
    [[ -z "$mid" ]] && continue
    c=$(_created_at_of "$mid")
    [[ -z "$c" ]] && continue
    if [[ -z "$best" || "$c" < "$best" ]]; then best="$c"; fi
  done
  [[ -z "$best" ]] && return 0
  CLOCK2="$best"
  say "  ****** CLOCK 2 BACKFILLED at startup: earliest banked accept createdAt = $CLOCK2 ******"
  persist_state
}

# invoke_runner: fires exactly one unrated_run.sh call for one (arm,cell).
# Sets LAST_OUTFILE on success; sets FATAL=1 and returns 1 on ANY abnormal
# exit or an unreadable outfile line -- unrated_run.sh's nonzero exits are all
# genuine abort states (foreign holder, activate/rollback failure, final
# holder mismatch), never mere budget contention (which it absorbs itself).
invoke_runner(){
  local ver=$1 games=$2 team=$3 pin=$4 arm=$5 label=$6
  FATAL=0
  local consolidated="${SCRATCH_DIR}/arm_fieldcal_${arm}_${label}.txt"
  local capture rc
  # ⛔ HEARTBEAT WRAPPER (side lane, 06:4xZ): the runner waits out rate windows
  # INTERNALLY, so a synchronous capture left the scheduler silent for up to a
  # full window — a live-and-waiting scheduler and a dead one produced
  # identical output (§9.5's freshness rule, applied to our own liveness).
  # The child runs in background; a liveness line prints every ~120s.
  local _hb_tmp="${SCRATCH_DIR}/.fieldcal_invoke_$$.out"
  PIN="$pin" MAIN="$FIELDCAL_MAIN" ${=RUNNER_CMD} "$ver" "$games" "$team" > "$_hb_tmp" 2>&1 &
  local _hb_pid=$! _hb_w=0
  while kill -0 $_hb_pid 2>/dev/null; do
    sleep 15; _hb_w=$((_hb_w+15))
    if (( _hb_w % 120 == 0 )); then
      say "  … arm=$arm cell=$label invocation running ${_hb_w}s (child $_hb_pid alive — a silent stretch is the runner waiting out the rate window, not a hang)"
    fi
  done
  wait $_hb_pid; rc=$?
  capture=$(<"$_hb_tmp"); rm -f "$_hb_tmp"
  print -r -- "$capture" >> "$LOG_FILE"
  if (( rc != 0 )) || [[ "$capture" == *ABORT* ]] || [[ "$capture" == *"ROLLBACK FAILED"* ]]; then
    say "  *** RUNNER FATAL arm=$arm cell=$label ver=$ver exit=$rc — stopping the scheduler."
    print -r -- "$capture" | tail -8 | while IFS= read -r l; do say "      $l"; done
    FATAL=1
    return 1
  fi
  local outfile
  outfile=$(print -r -- "$capture" | grep -o 'outfile=[^ ]*' | head -1 | cut -d= -f2)
  if [[ -z "$outfile" || ! -f "$outfile" ]]; then
    say "  *** RUNNER for arm=$arm cell=$label reported no readable outfile — cannot verify accepts or clock2. Stopping."
    FATAL=1
    return 1
  fi
  cat "$outfile" >> "$consolidated"
  LAST_OUTFILE=$outfile
  return 0
}

# ===========================================================================
# THE -40 ELO HALT (§10.5b), evaluated before every round once CLOCK2 exists.
# ===========================================================================
# leak_check: after every flip, read the platform (id-keyed, complete rows,
# createdAt >= clock2) and HALT if ANY rated ladder pairing was played by an
# ARM version rather than the holder. Session-independent replacement for the
# side lane's manual per-flip verification. An unreadable platform logs
# LEAK-UNKNOWN and does NOT halt (persistent blindness is the elo gate's job).
leak_check(){
  [[ -z "${CLOCK2:-}" ]] && return 0
  local versions_csv="${ARM_VER[A]},${ARM_VER[B]}"
  local _lk_json="${SCRATCH_DIR}/.fieldcal_leak_$$.json" lline
  ${=PLATFORM_LIST_CMD} > "$_lk_json" 2>/dev/null
  lline=$("$PYTHON_BIN" - "$_lk_json" "$CLOCK2" "$OUR_TEAM_ID" "$versions_csv" <<'PY'
import json, sys
from datetime import datetime
json_path, clock2, our_id, versions_csv = sys.argv[1:5]
versions = set(v.strip() for v in versions_csv.split(","))
def p(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)
try:
    with open(json_path) as fh:
        d = json.load(fh)
except Exception:
    print("LEAK unknown=1 n=0"); raise SystemExit(0)
ms = d if isinstance(d, list) else d.get("matches", d.get("data", []))
if not isinstance(ms, list):
    print("LEAK unknown=1 n=0"); raise SystemExit(0)
since = p(clock2)
leaks = []
for m in ms:
    if m.get("triggeredBy") != "ladder" or m.get("status") != "complete":
        continue
    ca = m.get("createdAt") or ""
    try:
        if p(ca) < since:
            continue
    except Exception:
        continue
    if m.get("teamAId") == our_id:
        side = "A"
    elif m.get("teamBId") == our_id:
        side = "B"
    else:
        continue
    if str(m.get(f"team{side}Version", "")).strip() in versions:
        leaks.append(f"{m.get('id','?')[:8]}@{ca}")
print(f"LEAK unknown=0 n={len(leaks)}" + (" ids=" + ",".join(leaks) if leaks else ""))
PY
)
  rm -f "$_lk_json"
  # ⛔ token-parse, never substring: "unknown=0" CONTAINS "n=0", so a substring
  # check for the count matched the WRONG token and passed a real leak
  # (caught by selftest cell h2 — the cell earned its keep before first fire).
  local _lk_unknown=0 _lk_n=0 tok
  for tok in ${(s: :)lline}; do
    case $tok in
      unknown=*) _lk_unknown=${tok#unknown=} ;;
      n=*) _lk_n=${tok#n=} ;;
    esac
  done
  if [[ "$_lk_unknown" == "1" ]]; then
    say "  LEAK CHECK: platform unreadable — LEAK-UNKNOWN (not a pass; the elo gate owns persistent blindness)."
    return 0
  fi
  if [[ "$_lk_n" == "0" ]]; then
    say "  LEAK CHECK: clean — no rated pairing played by an arm since clock2."
    return 0
  fi
  say "  *** LEAK DETECTED: rated pairing(s) played by an ARM version — $lline"
  : > "$HALT_FILE"
  say "  HALT file created: $HALT_FILE"
  return 1
}

elo_round_gate(){
  if [[ -z "${CLOCK2:-}" ]]; then
    say "ELO GATE: clock2 not yet set (no accept banked) — gate not yet active."
    return 0
  fi
  local versions_csv="${ARM_VER[A]},${ARM_VER[B]}"
  local line
  line=$("$PYTHON_BIN" - "$LADDER_TSV" "$CLOCK2" "$STALE_MIN" "${NOW_OVERRIDE:-}" "$versions_csv" <<'PY'
import sys, csv
from datetime import datetime, timezone

ladder_path, since_iso, stale_min_s, now_override, versions_csv = sys.argv[1:6]
stale_min = float(stale_min_s)
versions = set(v.strip() for v in versions_csv.split(","))

def parse_iso(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)

now = parse_iso(now_override) if now_override else datetime.now(timezone.utc)
since_dt = parse_iso(since_iso)

try:
    with open(ladder_path, newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
except OSError:
    rows = []

if not rows:
    print("ELO_GATE blind=1 reason=NO_ROWS age_min=NA sum=0.00 n=0 n_incomplete=0 newest=NA")
    raise SystemExit(0)

# Newest row over the WHOLE tape, UNFILTERED -- staleness must not be
# confused by an empty filtered subset (a stale-but-nonempty tape and a
# stale-and-empty tape must read identically BLIND; a fresh-and-empty tape
# is the only legitimate "clear" empty read).
newest = None
for r in rows:
    c = r.get("created")
    if not c:
        continue
    try:
        d = parse_iso(c)
    except ValueError:
        continue
    if newest is None or d > newest:
        newest = d

if newest is None:
    print("ELO_GATE blind=1 reason=NO_TIMESTAMPS age_min=NA sum=0.00 n=0 n_incomplete=0 newest=NA")
    raise SystemExit(0)

age_min = (now - newest).total_seconds() / 60.0

grouped = {}
order = []
for r in rows:
    mid = r.get("match")
    if not mid:
        continue
    if mid not in grouped:
        grouped[mid] = []
        order.append(mid)
    grouped[mid].append(r)

total = 0.0
n_matches = 0
n_incomplete = 0
for mid in order:
    games = grouped[mid]
    first = games[0]
    c = first.get("created")
    if not c:
        continue
    try:
        cd = parse_iso(c)
    except ValueError:
        continue
    if cd < since_dt:
        continue
    ourver = str(first.get("ourver", "")).strip()
    if ourver not in versions:
        continue
    n = len(games)
    if n != 5:
        n_incomplete += 1
        continue
    won = sum(1 for g in games if g.get("won") == "1")
    try:
        ourbef = float(first["ourbef"]); oppbef = float(first["oppbef"])
    except (KeyError, ValueError, TypeError):
        n_incomplete += 1
        continue
    E = 1.0 / (1.0 + 10 ** ((oppbef - ourbef) / 400.0))
    S = won / 5.0
    delta = 32 * (S - E)
    total += delta
    n_matches += 1

# BLIND IS ABSOLUTE-AGE, NOT CLOCK2-RELATIVE: a stale archive is BLIND
# regardless of what the (possibly empty) filtered sum computes to.
blind = age_min > stale_min
reason = "STALE_ARCHIVE" if blind else "OK"
newest_s = newest.strftime("%Y-%m-%dT%H:%M:%SZ")
print(f"ELO_GATE blind={1 if blind else 0} reason={reason} age_min={age_min:.2f} "
      f"sum={total:.2f} n={n_matches} n_incomplete={n_incomplete} newest={newest_s}")
PY
)
  say "  $line"
  local blind=0 sum=0 age=NA reason=NA tok
  for tok in ${(s: :)line}; do
    case $tok in
      blind=*) blind=${tok#blind=} ;;
      sum=*) sum=${tok#sum=} ;;
      age_min=*) age=${tok#age_min=} ;;
      reason=*) reason=${tok#reason=} ;;
    esac
  done
  if [[ "$blind" == "1" ]]; then
    # Archive stale -> LIVE PLATFORM READ before any blindness is declared.
    # ⛔ Data goes via a TEMP FILE, not a pipe: `python -` takes its SCRIPT from
    # stdin (the heredoc), so piping the JSON in as well silently hands the
    # parser an empty stream — found by the selftest's g4 cell, which is the
    # reason fixture-driven cells exist.
    local pline _pf_json="${SCRATCH_DIR}/.fieldcal_platform_$$.json"
    ${=PLATFORM_LIST_CMD} > "$_pf_json" 2>/dev/null
    pline=$("$PYTHON_BIN" - "$_pf_json" "$CLOCK2" "$OUR_TEAM_ID" "$versions_csv" <<'PY'
import json, sys
from datetime import datetime
json_path, clock2, our_id, versions_csv = sys.argv[1:5]
versions = set(v.strip() for v in versions_csv.split(","))
def p(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)
try:
    with open(json_path) as fh:
        d = json.load(fh)
except Exception:
    print("PFALL ok=0 reason=UNPARSEABLE"); raise SystemExit(0)
ms = d if isinstance(d, list) else d.get("matches", d.get("data", []))
if not isinstance(ms, list) or not ms:
    print("PFALL ok=0 reason=EMPTY_LIST"); raise SystemExit(0)
since = p(clock2)
tot = 0.0; n = 0; ninc = 0
for m in ms:
    if m.get("triggeredBy") != "ladder":
        continue
    ca = m.get("createdAt") or ""
    try:
        if p(ca) < since:
            continue
    except Exception:
        continue
    if m.get("status") != "complete":
        ninc += 1; continue
    if m.get("teamAId") == our_id:
        side = "A"
    elif m.get("teamBId") == our_id:
        side = "B"
    else:
        continue
    if str(m.get(f"team{side}Version", "")).strip() not in versions:
        continue
    dlt = m.get(f"eloDelta{side}")
    if dlt is None:
        ninc += 1; continue
    tot += float(dlt); n += 1
print(f"PFALL ok=1 sum={tot:.2f} n={n} n_incomplete={ninc}")
PY
)
    rm -f "$_pf_json"
    say "  $pline"
    if [[ "$pline" == *"ok=1"* ]]; then
      local psum=0
      for tok in ${(s: :)pline}; do case $tok in sum=*) psum=${tok#sum=} ;; esac; done
      BLIND_STREAK=0
      persist_state
      say "  ELO GATE: archive stale (age=${age}min) -> LIVE PLATFORM READ sum=${psum} (source=platform eloDelta, id-keyed, complete-only) — verdict from the authority, not the cache."
      if awk -v s="$psum" 'BEGIN{exit !(s<=-40)}'; then
        say "  *** -40 ELO HALT (platform read): cumulative net = ${psum} (<= -40)."
        : > "$HALT_FILE"
        say "  HALT file created: $HALT_FILE"
        return 1
      fi
      return 0
    fi
    BLIND_STREAK=$(( ${BLIND_STREAK:-0} + 1 ))
    say "  ELO GATE: BLIND (age=${age}min > ${STALE_MIN}min, archive reason=$reason, platform fallback failed: ${pline}) — BOTH surfaces unreadable. streak=${BLIND_STREAK}/3"
    persist_state
    if (( BLIND_STREAK >= 3 )); then
      say "  *** 3 CONSECUTIVE DOUBLE-BLIND ELO READS. STOPPING FOR A HUMAN. ***"
      return 2
    fi
    return 0
  fi
  BLIND_STREAK=0
  persist_state
  if awk -v s="$sum" 'BEGIN{exit !(s<=-40)}'; then
    say "  *** -40 ELO HALT: cumulative net Elo since clock2=$CLOCK2 for ourver in {${ARM_VER[A]},${ARM_VER[B]}} = ${sum} (<= -40)."
    : > "$HALT_FILE"
    say "  HALT file created: $HALT_FILE"
    return 1
  fi
  say "  ELO GATE: clear (sum=${sum}, age=${age}min <= ${STALE_MIN}min)."
  return 0
}

# ===========================================================================
# ONE ROUND = ONE WINDOW = ONE ARM.
# ===========================================================================
run_round(){
  local round=$1 arm start_idx pos idx label banked target budget_remaining=5 w games ver team pin accepted rejected
  if (( round % 2 == 0 )); then arm=A; else arm=B; fi
  start_idx=$(( (round / 2) % 10 ))
  say "ROUND $round: arm=$arm (v${ARM_VER[$arm]}) start_cell=${CELL_ORDER[start_idx+1]} (idx $start_idx)"
  # AMEND1 CATCH-UP RULE (docs/prereg/AMENDMENT-LEG-fieldcal-catchup-2026-08-16.md
  # §1, ratified 868e3312, side-lane cert 6faa684f): the round's FIRST cell is the
  # lowest-index ZERO-ACCEPT cell for this arm, if one exists; the ordinary
  # rotation then resumes from start_idx. A prepend to the SAME walk — every gate
  # below (HALT, rate budget same-cell retry, leak check, 12/12 skip) binds
  # unchanged, so the rule chooses WHICH cell fires first, never WHETHER (§1.3).
  # Selection predicate is `== 0`: structurally blind — a cell with no games has
  # no results to prefer (§3).
  local -a visit
  visit=()
  local catchup_idx=-1 ci clbl
  for (( ci=0; ci<10; ci++ )); do
    clbl=${CELL_ORDER[ci+1]}
    if (( ${COUNTS[$arm,$clbl]:-0} == 0 )); then catchup_idx=$ci; break; fi
  done
  if (( catchup_idx >= 0 && catchup_idx != start_idx )); then
    # No line when the zero cell IS the scheduled cell: no reorder happened,
    # and a spurious CATCHUP line would make the tape lie about firing order.
    say "  CATCHUP $arm/${CELL_ORDER[catchup_idx+1]}   (scheduled start was $arm/${CELL_ORDER[start_idx+1]}, idx $start_idx)"
    visit+=($catchup_idx)
  fi
  for (( pos=0; pos<10; pos++ )); do visit+=($(( (start_idx + pos) % 10 ))); done
  for idx in $visit; do
    (( budget_remaining > 0 )) || break
    label=${CELL_ORDER[idx+1]}
    if halt_file_present; then
      say "  HALT file present — stopping cleanly, no further invocations this round."
      say "  ⚠ STOP NOTE: arm B trails A by one round STRUCTURALLY (lost round 3 + parity) — an early stop shorts B on every possible stop; CUT-SHORT shortfall is ASYMMETRIC. See scratchpad/fieldcal_amend1_effective.txt."
      return 0
    fi
    banked=${COUNTS[$arm,$label]:-0}
    if (( banked >= 12 )); then
      say "  cell $label already 12/12 for arm $arm — skip"
      continue
    fi
    target=$budget_remaining
    (( (12-banked) < target )) && target=$((12-banked))

    # Gate on the account-wide meter BEFORE this invocation. A nonzero wait
    # sleeps and RE-CHECKS THE SAME CELL — never advances (§9.6b).
    while true; do
      w=$(budget_wait)
      (( w <= 0 )) && break
      say "  rate budget: wait ${w}s before firing $arm/$label (target ${target} accept(s)) — same-cell retry, never advances"
      do_sleep "$w"
      if halt_file_present; then
        say "  HALT file present during budget wait — stopping cleanly."
      say "  ⚠ STOP NOTE: arm B trails A by one round STRUCTURALLY (lost round 3 + parity) — an early stop shorts B on every possible stop; CUT-SHORT shortfall is ASYMMETRIC. See scratchpad/fieldcal_amend1_effective.txt."
        return 0
      fi
    done

    games=$(( target * GAMES_PER ))
    ver=${ARM_VER[$arm]}
    team=${CELL_TEAM[$label]}
    pin=${CELL_PIN[$label]}
    say "  firing arm=$arm cell=$label ver=$ver target_accepts=$target games=$games team=${team:0:8} pin=${pin:0:8}"
    invoke_runner "$ver" "$games" "$team" "$pin" "$arm" "$label"
    if (( FATAL )); then return 1; fi

    accepted=$(count_accepted "$LAST_OUTFILE")
    rejected=$(count_rejected "$LAST_OUTFILE")
    COUNTS[$arm,$label]=$(( banked + accepted ))
    say "  cell $label: +${accepted} accept(s), +${rejected} reject(s) — now ${COUNTS[$arm,$label]}/12 for arm $arm"
    maybe_capture_clock2 "$LAST_OUTFILE"
    persist_state
    # Per-flip leak check (side-lane mechanisation, 2026-08-16 07:3xZ): the leg
    # verifies ITSELF that no rated pairing has been played by an ARM. One leak
    # means gap-landing failed and continuing would repeat it -> HALT.
    if ! leak_check; then
      say "*** LEAK CHECK FAILED — halting the leg. ***"
      return 1
    fi
    budget_remaining=$(( budget_remaining - accepted ))
  done
  return 0
}

# ===========================================================================
# MAIN LOOP
# ===========================================================================
main_loop(){
  while true; do
    if halt_file_present; then
      say "HALT file present at round boundary — stopping cleanly."
      say "  ⚠ STOP NOTE: arm B trails A by one round STRUCTURALLY (lost round 3 + parity) — an early stop shorts B on every possible stop; CUT-SHORT shortfall is ASYMMETRIC. See scratchpad/fieldcal_amend1_effective.txt."
      return 0
    fi
    if all_cells_done; then
      say "LEG COMPLETE: all 20 (arm,cell) pairs at 12/12 accepts (240 accepts, 1,200 games)."
      return 0
    fi
    elo_round_gate
    local gate_rc=$?
    if (( gate_rc == 1 )); then return 0; fi   # -40 halt tripped, HALT file created
    if (( gate_rc == 2 )); then return 3; fi   # 3x BLIND — ask a human

    run_round "$ROUND_NUM"
    if (( FATAL )); then return 4; fi

    ROUND_NUM=$((ROUND_NUM+1))
    persist_state
  done
}

# ===========================================================================
# STARTUP VALIDATION — a bad id REFUSES, it does not warn.
# ===========================================================================
startup_validate(){
  local -a triples
  triples=()
  local label
  for label in $CELL_ORDER; do
    triples+=("${label}|${CELL_TEAM[$label]}|${CELL_PIN[$label]}")
  done
  validate_ids $triples
}

# ===========================================================================
# SELFTEST — every cell isolated, no network, own temp dir, cleans up after.
# ===========================================================================
selftest(){
  print "FIELDCAL SCHEDULER SELFTEST"
  print ""
  local bad=0
  ok(){ print "  [ok] $1"; }
  fail(){ print "  [FAIL] $1"; bad=1; }

  local TDIR
  TDIR=$(mktemp -d "${TMPDIR:-/tmp}/fieldcal_selftest.XXXXXX")
  trap "rm -rf '$TDIR'" EXIT
  # ⛔ ISOLATION, ENFORCED BEFORE ANY OTHER CELL RUNS: every writable path this
  # script touches (log, halt file, state file, per-cell consolidated outfiles)
  # is redirected into TDIR here, first, so that even the very first `say` call
  # below (inside the (f) startup-validation cell) cannot land in the repo's
  # real scratchpad/. A prior version of this file redirected these only
  # per-test-cell and leaked scratchpad/fieldcal_scheduler.log plus two
  # scratchpad/arm_fieldcal_*.txt files on its first run -- caught by checking
  # `git status` after running --selftest, not by inspection.
  LOG_FILE="$TDIR/sched.log"
  HALT_FILE="$TDIR/HALT_absent"
  STATE_FILE="$TDIR/state_default.tsv"
  SCRATCH_DIR="$TDIR"

  # --- (a) rotation: rounds 0..5 -> arms A,B,A,B,A,B and start cells 0,0,1,1,2,2
  local r arm start_idx exp_arms exp_starts got_arms got_starts
  exp_arms=(A B A B A B)
  exp_starts=(0 0 1 1 2 2)
  got_arms=(); got_starts=()
  for r in 0 1 2 3 4 5; do
    if (( r % 2 == 0 )); then arm=A; else arm=B; fi
    start_idx=$(( (r / 2) % 10 ))
    got_arms+=("$arm"); got_starts+=("$start_idx")
  done
  if [[ "${got_arms[*]}" == "${exp_arms[*]}" && "${got_starts[*]}" == "${exp_starts[*]}" ]]; then
    ok "rotation: rounds 0..5 -> arms ${got_arms[*]}, starts ${got_starts[*]}"
  else
    fail "rotation: got arms=${got_arms[*]} starts=${got_starts[*]}, want arms=${exp_arms[*]} starts=${exp_starts[*]}"
  fi

  # --- (f) startup validation on the REAL shipped table. HISTORY: until the
  # builder filled kladde's team id (2026-08-16 ~06:2xZ) this cell asserted the
  # REFUSAL (placeholder id); the fill flipped it, correctly — a cell asserting
  # a temporary data state must flip when the data completes. Refusal coverage
  # lives in the synthetic malformed-triple cell below, which is fixture-driven
  # and cannot rot with the table. (The original cell also read rc from the
  # [[ ]] test instead of the validator — fixed here.)
  local out rc
  out=$(startup_validate 2>&1); rc=$?
  if [[ $rc -eq 0 ]]; then
    ok "startup validation: the REAL shipped table VALIDATES (all 10 ids filled, well-formed)"
  else
    fail "startup validation: complete real table should validate; rc=$rc out=$out"
  fi
  local -a good_triples
  good_triples=("x|32087804-2dde-4265-adcd-ab6ec9039fbe|246843da-fd15-435a-ab03-d61ff7a68ceb")
  if validate_ids $good_triples; then
    ok "validate_ids: a well-formed synthetic triple PASSES (checker is not vacuous)"
  else
    fail "validate_ids: a well-formed synthetic triple was rejected"
  fi
  local -a bad_triples
  bad_triples=("y|not-a-uuid|246843da-fd15-435a-ab03-d61ff7a68ceb")
  if ! validate_ids $bad_triples; then
    ok "validate_ids: a malformed synthetic triple FAILS"
  else
    fail "validate_ids: a malformed synthetic triple was accepted"
  fi

  # --- shared fixture setup for (b)/(c)/(e): a stub RUNNER_CMD that always
  # accepts exactly (games/5) challenges and logs every call it received.
  local calllog="$TDIR/calls.log"
  : > "$calllog"
  local stub_runner="$TDIR/stub_runner.sh"
  cat > "$stub_runner" <<STUB
#!/bin/zsh
ver=\$1; games=\$2; team=\$3
echo "\$ver \$games \$team \$PIN" >> "$calllog"
n=\$(( games / 5 ))
stamp="\$(date -u +%Y%m%dT%H%M%S)_\$\$_\$RANDOM"
out="$TDIR/arm_unrated_v\${ver}_\${stamp}.txt"
: > "\$out"
i=0
while (( i < n )); do
  i=\$((i+1))
  echo "\$team {\"matchId\": \"fake-\$RANDOM-\$i\", \"createdAt\": \"2026-08-16T00:0\${i}:00Z\"}" >> "\$out"
done
echo "outfile=\$out"
exit 0
STUB
  chmod +x "$stub_runner"

  local stub_budget_always_free="$TDIR/budget_free.sh"
  cat > "$stub_budget_always_free" <<'STUB'
#!/bin/zsh
echo 0
STUB
  chmod +x "$stub_budget_always_free"

  # --- (b) a full-cell skip: pre-fill Juusto's arm-A count to 12/12, run one
  # round (round 0 -> arm A, start cell Juusto). Expect Juusto NOT invoked and
  # not_adgato IS invoked and gains an accept.
  LOG_FILE="$TDIR/sched.log"; HALT_FILE="$TDIR/HALT_absent"
  RUNNER_CMD="$stub_runner"; BUDGET_CMD="$stub_budget_always_free"
  # ⛔ NO NETWORK IN A SELFTEST: the elo gate's platform fallback would call the
  # real fcode on every stale-archive cell (it did, and reset the streak cell
  # with a LIVE read). Default the sandbox to a FAILING platform so blind-path
  # cells exercise blindness; g4/g5 override per-cell with JSON fixtures.
  PLATFORM_LIST_CMD="echo selftest-no-network"
  FIELDCAL_TEST_NOSLEEP=1
  load_state_fixture(){ ROUND_NUM=0; CLOCK2=""; BLIND_STREAK=0; typeset -gA COUNTS; local a l; for a in A B; do for l in $CELL_ORDER; do COUNTS[$a,$l]=0; done; done; }
  load_state_fixture
  COUNTS[A,Juusto]=12
  STATE_FILE="$TDIR/state_b.tsv"
  : > "$calllog"
  FATAL=0
  run_round 0 >/dev/null
  if grep -q "kladde\|Juusto" "$calllog" 2>/dev/null; then
    # team id substring check is unreliable across ids; check by absence of
    # Juusto's team id prefix instead.
    :
  fi
  if grep -q "${CELL_TEAM[Juusto]}" "$calllog"; then
    fail "full-cell skip: Juusto (12/12) WAS invoked — skip did not fire"
  else
    ok "full-cell skip: Juusto (12/12) was not invoked"
  fi
  if grep -q "${CELL_TEAM[not_adgato]}" "$calllog" && (( ${COUNTS[A,not_adgato]:-0} > 0 )); then
    ok "full-cell skip: rotation moved on to not_adgato and it gained an accept (${COUNTS[A,not_adgato]})"
  else
    fail "full-cell skip: not_adgato was not fired or gained no accept"
  fi

  # --- (c) budget-refusal causes SAME-cell retry, not advance.
  local stub_budget_once="$TDIR/budget_once.sh"
  local ctrfile="$TDIR/budget_ctr"
  echo 0 > "$ctrfile"
  cat > "$stub_budget_once" <<STUB
#!/bin/zsh
n=\$(cat "$ctrfile")
n=\$((n+1))
echo \$n > "$ctrfile"
if [ "\$n" -eq 1 ]; then echo 3; else echo 0; fi
STUB
  chmod +x "$stub_budget_once"
  load_state_fixture
  STATE_FILE="$TDIR/state_c.tsv"
  BUDGET_CMD="$stub_budget_once"
  : > "$calllog"
  SLEPT=()
  FATAL=0
  run_round 0 >/dev/null
  local first_call_id
  first_call_id=$(head -1 "$calllog" | awk '{print $3}')
  if [[ "${#SLEPT[@]}" -ge 1 && "${SLEPT[1]}" == "3" ]]; then
    ok "budget-refusal: waited exactly the reported 3s before firing"
  else
    fail "budget-refusal: expected one recorded sleep of 3s, got SLEPT=(${SLEPT[*]})"
  fi
  if [[ "$first_call_id" == "${CELL_TEAM[Juusto]}" ]]; then
    ok "budget-refusal: the cell that fired after the wait is the SAME cell (Juusto), not advanced"
  else
    fail "budget-refusal: expected Juusto to fire after the wait, got team=$first_call_id"
  fi
  BUDGET_CMD="$stub_budget_always_free"

  # --- (e) HALT file stops before any invocation.
  load_state_fixture
  STATE_FILE="$TDIR/state_e.tsv"
  HALT_FILE="$TDIR/HALT_present"
  : > "$HALT_FILE"
  : > "$calllog"
  FATAL=0
  run_round 0 >/dev/null
  if [[ ! -s "$calllog" ]]; then
    ok "HALT file: present -> zero invocations before the round even starts"
  else
    fail "HALT file: an invocation happened despite HALT being present ($(wc -l < "$calllog") call(s))"
  fi
  rm -f "$HALT_FILE"
  HALT_FILE="$TDIR/HALT_absent"

  # --- (d) state resume reproduces counts.
  load_state_fixture
  STATE_FILE="$TDIR/state_d.tsv"
  COUNTS[A,Juusto]=7; COUNTS[B,farming_200s]=3
  CLOCK2="2026-08-16T05:32:59Z"
  ROUND_NUM=4
  BLIND_STREAK=1
  persist_state
  load_state
  if [[ "${COUNTS[A,Juusto]:-0}" == "7" && "${COUNTS[B,farming_200s]:-0}" == "3" \
        && "$CLOCK2" == "2026-08-16T05:32:59Z" && "$ROUND_NUM" == "4" && "$BLIND_STREAK" == "1" ]]; then
    ok "state resume: reloaded counts/clock2/round/blind_streak match what was persisted"
  else
    fail "state resume: reloaded state does not match (Juusto=${COUNTS[A,Juusto]:-?} farming=${COUNTS[B,farming_200s]:-?} clock2=$CLOCK2 round=$ROUND_NUM streak=$BLIND_STREAK)"
  fi

  # --- (i) AMEND1 catch-up rule — the five owed cells (amendment §4; each can
  # return the other verdict, and i2/i3 are the dormancy/no-spurious-line pair
  # that make i1 mean something).
  local first_call_id2
  # i1: zero-accept cell OUT of rotation order fires FIRST, with a CATCHUP line.
  load_state_fixture
  STATE_FILE="$TDIR/state_i1.tsv"; LOG_FILE="$TDIR/sched_i1.log"
  for l in $CELL_ORDER; do COUNTS[A,$l]=12; done
  COUNTS[A,0033]=0   # idx 5; round 0 schedules idx 0 (Juusto)
  : > "$calllog"; FATAL=0
  run_round 0 >/dev/null
  first_call_id2=$(head -1 "$calllog" | awk '{print $3}')
  if [[ "$first_call_id2" == "${CELL_TEAM[0033]}" ]] && grep -q "CATCHUP A/0033" "$LOG_FILE"; then
    ok "amend1 i1: out-of-order zero-accept cell (0033) fired FIRST, CATCHUP line emitted"
  else
    fail "amend1 i1: expected 0033 first with a CATCHUP line (got team=$first_call_id2, log=$(grep -c CATCHUP "$LOG_FILE" 2>/dev/null) CATCHUP line(s))"
  fi
  # i2: no zero-accept cells -> rule DORMANT: no CATCHUP line, scheduled cell first.
  load_state_fixture
  STATE_FILE="$TDIR/state_i2.tsv"; LOG_FILE="$TDIR/sched_i2.log"
  for l in $CELL_ORDER; do COUNTS[A,$l]=1; done
  : > "$calllog"; FATAL=0
  run_round 0 >/dev/null
  first_call_id2=$(head -1 "$calllog" | awk '{print $3}')
  if [[ "$first_call_id2" == "${CELL_TEAM[Juusto]}" ]] && ! grep -q "CATCHUP" "$LOG_FILE"; then
    ok "amend1 i2: no zero cells -> dormant (no CATCHUP line, scheduled Juusto fired first)"
  else
    fail "amend1 i2: expected dormant rule (got team=$first_call_id2, CATCHUP lines=$(grep -c CATCHUP "$LOG_FILE" 2>/dev/null))"
  fi
  # i3: the zero-accept cell IS the scheduled cell -> no reorder, NO spurious line.
  load_state_fixture
  STATE_FILE="$TDIR/state_i3.tsv"; LOG_FILE="$TDIR/sched_i3.log"
  for l in $CELL_ORDER; do COUNTS[A,$l]=12; done
  COUNTS[A,Juusto]=0   # idx 0 == round 0's scheduled start
  : > "$calllog"; FATAL=0
  run_round 0 >/dev/null
  first_call_id2=$(head -1 "$calllog" | awk '{print $3}')
  if [[ "$first_call_id2" == "${CELL_TEAM[Juusto]}" ]] && ! grep -q "CATCHUP" "$LOG_FILE"; then
    ok "amend1 i3: zero cell IS the scheduled cell -> fired first with NO spurious CATCHUP line"
  else
    fail "amend1 i3: expected Juusto first and zero CATCHUP lines (got team=$first_call_id2, lines=$(grep -c CATCHUP "$LOG_FILE" 2>/dev/null))"
  fi
  # i4: budget refusal with a catch-up cell selected -> wait binds on the
  # CATCH-UP cell, same-cell retry, never advances (§1 exclusion 3).
  load_state_fixture
  STATE_FILE="$TDIR/state_i4.tsv"; LOG_FILE="$TDIR/sched_i4.log"
  for l in $CELL_ORDER; do COUNTS[A,$l]=12; done
  COUNTS[A,0033]=0
  echo 0 > "$ctrfile"
  BUDGET_CMD="$stub_budget_once"
  : > "$calllog"; SLEPT=(); FATAL=0
  run_round 0 >/dev/null
  first_call_id2=$(head -1 "$calllog" | awk '{print $3}')
  if [[ "${#SLEPT[@]}" -ge 1 && "${SLEPT[1]}" == "3" && "$first_call_id2" == "${CELL_TEAM[0033]}" ]]; then
    ok "amend1 i4: budget wait bound to the CATCH-UP cell (waited 3s, then 0033 fired, not advanced)"
  else
    fail "amend1 i4: expected 3s wait then 0033 (got SLEPT=(${SLEPT[*]}) team=$first_call_id2)"
  fi
  BUDGET_CMD="$stub_budget_always_free"
  # i5: HALT present with a catch-up cell selected -> ZERO invocations.
  load_state_fixture
  STATE_FILE="$TDIR/state_i5.tsv"; LOG_FILE="$TDIR/sched_i5.log"
  for l in $CELL_ORDER; do COUNTS[A,$l]=12; done
  COUNTS[A,0033]=0
  HALT_FILE="$TDIR/HALT_present_i5"
  : > "$HALT_FILE"
  : > "$calllog"; FATAL=0
  run_round 0 >/dev/null
  if [[ ! -s "$calllog" ]]; then
    ok "amend1 i5: HALT outranks the catch-up rule — zero invocations"
  else
    fail "amend1 i5: catch-up fired despite HALT ($(wc -l < "$calllog") call(s))"
  fi
  rm -f "$HALT_FILE"
  HALT_FILE="$TDIR/HALT_absent"
  LOG_FILE="$TDIR/sched.log"

  # --- (g) the -40 Elo gate: fixture ladder tapes.
  # Build a minimal ladder_games.tsv-shaped fixture. One complete 5-game match
  # per row-group, ourbef/oppbef chosen so E~0.5 and S from won-count controls
  # the sign/magnitude of delta = 32*(S-E).
  gen_match(){
    # args: match_id created ourver won_of_5
    local mid=$1 created=$2 ourver=$3 won=$4
    local g
    for g in 1 2 3 4 5; do
      local w=0
      (( g <= won )) && w=1
      printf '%s\t%s\t%s\t9\t%s\t1500\t1500\t testmap\ta\t%s\tcore_destroyed\t150\ts3\n' \
        "$mid" "$created" "OppX" "$ourver" "$w"
    done
  }
  local header='match	created	opp	oppver	ourver	ourbef	oppbef	map	winner_seat	won	cond	turns	s3'

  # g1: FRESH tape (newest row ~5 min before NOW_OVERRIDE), net well past -40.
  # E=0.5 always (ourbef==oppbef==1500); pick won-counts so mean S far below E.
  local now_iso="2026-08-16T12:00:00Z"
  local since_iso="2026-08-16T11:00:00Z"
  {
    print -r -- "$header"
    gen_match m1 "2026-08-16T11:10:00Z" 140 0   # S=0.0 delta=32*(0-.5)=-16
    gen_match m2 "2026-08-16T11:20:00Z" 154 0   # -16
    gen_match m3 "2026-08-16T11:55:00Z" 140 1   # S=0.2 delta=32*(.2-.5)=-9.6  total -41.6
  } > "$TDIR/ladder_neg41.tsv"
  local line41
  CLOCK2="$since_iso"; NOW_OVERRIDE="$now_iso"; LADDER_TSV="$TDIR/ladder_neg41.tsv"; STALE_MIN=40
  BLIND_STREAK=0; HALT_FILE="$TDIR/HALT_g1"
  elo_round_gate >/dev/null
  local rc41=$?
  if [[ $rc41 -eq 1 && -f "$HALT_FILE" ]]; then
    ok "elo gate: net -41.6 (fresh tape) -> HALT created"
  else
    fail "elo gate: net -41.6 expected HALT, got rc=$rc41 halt_exists=$([[ -f $HALT_FILE ]] && echo yes || echo no)"
  fi

  # g2: FRESH tape, net -39 (must NOT halt). Same E=0.5.
  {
    print -r -- "$header"
    gen_match m1 "2026-08-16T11:10:00Z" 140 0   # -16
    gen_match m2 "2026-08-16T11:20:00Z" 154 1   # S=.2 -9.6
    gen_match m3 "2026-08-16T11:55:00Z" 140 2   # S=.4 32*(.4-.5)=-3.2  ... adjust to land at -39
  } > "$TDIR/ladder_neg39.tsv"
  # recompute exactly: want -16 + -9.6 + X = -39 => X = -13.4 => S=.5-13.4/32=0.08125 -> not a clean /5 fraction.
  # Use a simpler exact composition instead: two matches only, -16 + -23 is too much;
  # build precisely: m1 S=0 (-16), m2 S=1/5=.2 (-9.6) => -25.6; m3 S=3/5=.6 delta=32*(.6-.5)=+3.2 => total -22.4 (not -39 either)
  # Simplify: just assert rc==0 (no halt) for a hand-verified -39.0 fixture below instead of chaining comments as data.
  {
    print -r -- "$header"
    gen_match m1 "2026-08-16T11:10:00Z" 140 0   # S=0   delta=-16.0
    gen_match m2 "2026-08-16T11:20:00Z" 154 0   # S=0   delta=-16.0
    gen_match m3 "2026-08-16T11:55:00Z" 140 3   # S=0.6 delta=32*(0.6-0.5)=+3.2
  } > "$TDIR/ladder_neg39.tsv"
  # total = -16 -16 +3.2 = -28.8 ; not -39. Compute a fixture that lands exactly
  # on -39.00 with integer won-counts (S in {0,.2,.4,.6,.8,1}, delta in
  # {-16,-9.6,-3.2,3.2,9.6,16} at E=0.5): -16 + -16 + -3.2 -3.8?? use three matches:
  # -16 + -9.6 + -13.4 impossible (not on grid). Use FOUR matches instead:
  # -16 -9.6 -9.6 -3.2 = -38.4 (close). Try -16 -16 -3.2 -3.2 = -38.4. Try
  # -16 -9.6 -9.6 -3.2 -0? use -16 -9.6 -9.6 -3.2 -0.6?? not on grid either.
  # Simplify to TWO matches at S=0 and S=1 mixed isn't needed -- just pick
  # counts on the grid summing exactly to -39.0: -16 -16 -9.6 +2.6?? no.
  # Grid step is 3.2 (32*0.1) since S steps by 0.2 -> delta steps by 6.4? Actually
  # 32*0.2=6.4 per S-step, so grid values are {-16,-9.6,-3.2,3.2,9.6,16} step 6.4.
  # Sum of k grid values landing exactly on -39.0: -16-16-9.6+... try
  # -16-16-9.6+2.6 no. Try five matches: -16-16-9.6-9.6+12.2 no.
  # -16*2 + -9.6*1 + 3.2*? : -16-16-9.6=-41.6 (that's g1's number). Add +2.6 not on grid.
  # Use -16 -9.6 -9.6 -3.2 -0.6?? still off-grid. Instead of forcing -39.0 exactly,
  # register -39.0 via UNEQUAL ourbef/oppbef so E != 0.5, giving a free real-valued
  # dial. Redo g2 with a single match tuned exactly to -39.0 at S=0 (worst case):
  # delta = 32*(0-E) = -39.0 => E = 39/32 = 1.21875 -- impossible (E<=1). So a
  # single S=0 match cannot reach -39 alone (max magnitude at S=0 is -32*E<=  -32*1=-32
  # only if E=1, i.e. oppbef << ourbef). Use TWO S=0 matches with E=0.6 each:
  # delta=32*(0-0.6)=-19.2 each, total -38.4. Close but let's just SOLVE exactly:
  # want total=-39.0 over 2 matches, S=0 both, oppbef-ourbef=d for both (E depends on d).
  # -39.0 = 2 * 32 * (0 - E) => E = 39/64 = 0.609375
  # E = 1/(1+10^((oppbef-ourbef)/400)) = 0.609375 => 10^((oppbef-ourbef)/400) = (1/0.609375)-1 = 0.640977...
  # (oppbef-ourbef)/400 = log10(0.640977) = -0.19314  => oppbef-ourbef = -77.257
  # i.e. ourbef = oppbef + 77.257. Use ourbef=1577.26 oppbef=1500.00 (approx).
  {
    print -r -- "$header"
    printf 'm1\t2026-08-16T11:10:00Z\tOppX\t9\t140\t1577.26\t1500.00\ttestmap\ta\t0\tcore_destroyed\t150\ts3\n'
    printf 'm1\t2026-08-16T11:10:00Z\tOppX\t9\t140\t1577.26\t1500.00\ttestmap\ta\t0\tcore_destroyed\t150\ts3\n'
    printf 'm1\t2026-08-16T11:10:00Z\tOppX\t9\t140\t1577.26\t1500.00\ttestmap\ta\t0\tcore_destroyed\t150\ts3\n'
    printf 'm1\t2026-08-16T11:10:00Z\tOppX\t9\t140\t1577.26\t1500.00\ttestmap\ta\t0\tcore_destroyed\t150\ts3\n'
    printf 'm1\t2026-08-16T11:10:00Z\tOppX\t9\t140\t1577.26\t1500.00\ttestmap\ta\t0\tcore_destroyed\t150\ts3\n'
    printf 'm2\t2026-08-16T11:20:00Z\tOppX\t9\t154\t1577.26\t1500.00\ttestmap\ta\t0\tcore_destroyed\t150\ts3\n'
    printf 'm2\t2026-08-16T11:20:00Z\tOppX\t9\t154\t1577.26\t1500.00\ttestmap\ta\t0\tcore_destroyed\t150\ts3\n'
    printf 'm2\t2026-08-16T11:20:00Z\tOppX\t9\t154\t1577.26\t1500.00\ttestmap\ta\t0\tcore_destroyed\t150\ts3\n'
    printf 'm2\t2026-08-16T11:20:00Z\tOppX\t9\t154\t1577.26\t1500.00\ttestmap\ta\t0\tcore_destroyed\t150\ts3\n'
    printf 'm2\t2026-08-16T11:20:00Z\tOppX\t9\t154\t1577.26\t1500.00\ttestmap\ta\t0\tcore_destroyed\t150\ts3\n'
  } > "$TDIR/ladder_neg39.tsv"
  CLOCK2="$since_iso"; NOW_OVERRIDE="$now_iso"; LADDER_TSV="$TDIR/ladder_neg39.tsv"
  BLIND_STREAK=0; HALT_FILE="$TDIR/HALT_g2"
  local out39
  out39=$(elo_round_gate)
  local rc39=$?
  if [[ $rc39 -eq 0 && ! -f "$HALT_FILE" ]] && print -r -- "$out39" | grep -q 'sum=-39\.0'; then
    ok "elo gate: net -39.0 (fresh tape) -> no HALT (sum printed in the read)"
  else
    fail "elo gate: net -39.0 expected no-HALT with sum~-39.0, got rc=$rc39 out=$(print -r -- $out39 | tail -1)"
  fi

  # g3: STALE tape (newest row 76 min old) with a LARGE negative sum available
  # if it were read -- must return BLIND, not a verdict, per the coordinator's
  # correction. now=12:00, newest row=10:44 (76 min old).
  {
    print -r -- "$header"
    gen_match m1 "2026-08-16T10:44:00Z" 140 0   # would be -16 if read
    gen_match m2 "2026-08-16T10:44:00Z" 154 0   # would be -16
    gen_match m3 "2026-08-16T10:44:00Z" 140 0   # would be -16 -> total -48 if it were read
  } > "$TDIR/ladder_stale76.tsv"
  CLOCK2="2026-08-16T10:00:00Z"; NOW_OVERRIDE="$now_iso"; LADDER_TSV="$TDIR/ladder_stale76.tsv"
  BLIND_STREAK=0; HALT_FILE="$TDIR/HALT_g3"
  local out76 rc76
  out76=$(elo_round_gate)
  rc76=$?
  if [[ $rc76 -eq 0 && ! -f "$HALT_FILE" ]] && print -r -- "$out76" | grep -q 'blind=1' && print -r -- "$out76" | grep -q 'age_min=76\.00'; then
    ok "elo gate: 76-min-old newest row -> BLIND with age printed, NOT a verdict (despite a would-be -48 sum)"
  else
    fail "elo gate: expected BLIND age_min=76.00, got rc=$rc76 out=$(print -r -- $out76 | tail -1)"
  fi

  # g4: 3 consecutive BLIND reads -> stop-for-human (rc=2 on the 3rd).
  BLIND_STREAK=0
  elo_round_gate >/dev/null; local s1=$BLIND_STREAK
  local rc2a; elo_round_gate >/dev/null; rc2a=$?; local s2=$BLIND_STREAK
  local rc2b; elo_round_gate >/dev/null; rc2b=$?; local s3=$BLIND_STREAK
  if [[ "$s1" == "1" && "$s2" == "2" && "$s3" == "3" && "$rc2b" == "2" ]]; then
    ok "elo gate: 3 consecutive BLIND reads -> streak 1,2,3 and rc=2 (stop for a human) on the 3rd"
  else
    fail "elo gate: expected streak 1,2,3 and rc=2 on 3rd BLIND, got streak=($s1,$s2,$s3) rc3=$rc2b"
  fi
  # a subsequent CLEAR (fresh, in-band) read resets the streak.
  CLOCK2="$since_iso"; NOW_OVERRIDE="$now_iso"; LADDER_TSV="$TDIR/ladder_neg39.tsv"
  elo_round_gate >/dev/null
  if [[ "$BLIND_STREAK" == "0" ]]; then
    ok "elo gate: a subsequent non-BLIND read resets the streak to 0"
  else
    fail "elo gate: streak did not reset after a clear read (streak=$BLIND_STREAK)"
  fi

  # --- (g4-g6) PLATFORM FALLBACK cells (side-lane design, 07:1xZ). Stale
  # archive must fall back to a live platform read; BLIND survives only when
  # BOTH surfaces fail. The g4 fixture drives every filter: version (152
  # excluded — the halt is ARM-ATTRIBUTED, the window total is not the
  # registered quantity), status, triggeredBy, and the clock2 boundary.
  local PJ="$TDIR/plat.json"
  cat > "$PJ" <<'PJEOF'
[
 {"triggeredBy":"ladder","status":"complete","createdAt":"2026-08-16T11:30:00Z","teamAId":"OURID","teamBId":"x","teamAVersion":"140","eloDeltaA":-20.0,"eloDeltaB":20.0},
 {"triggeredBy":"ladder","status":"complete","createdAt":"2026-08-16T11:35:00Z","teamAId":"x","teamBId":"OURID","teamBVersion":"152","eloDeltaB":-30.0,"eloDeltaA":30.0},
 {"triggeredBy":"ladder","status":"created","createdAt":"2026-08-16T11:40:00Z","teamAId":"OURID","teamBId":"x","teamAVersion":"154"},
 {"triggeredBy":"unrated","status":"complete","createdAt":"2026-08-16T11:41:00Z","teamAId":"OURID","teamBId":"x","teamAVersion":"140","eloDeltaA":-99.0},
 {"triggeredBy":"ladder","status":"complete","createdAt":"2026-08-16T09:00:00Z","teamAId":"OURID","teamBId":"x","teamAVersion":"140","eloDeltaA":-99.0},
 {"triggeredBy":"ladder","status":"complete","createdAt":"2026-08-16T11:50:00Z","teamAId":"x","teamBId":"OURID","teamBVersion":"154","eloDeltaB":5.0,"eloDeltaA":-5.0}
]
PJEOF
  sed -i '' "s/OURID/$OUR_TEAM_ID/g" "$PJ" 2>/dev/null || sed -i "s/OURID/$OUR_TEAM_ID/g" "$PJ"
  # g4: stale archive + healthy platform -> live verdict sum=-15 (only rows 1
  # and 6 count: -20 +5; the v152, incomplete, unrated and pre-clock2 rows are
  # all excluded), streak resets, no halt.
  CLOCK2="2026-08-16T10:00:00Z"; NOW_OVERRIDE="$now_iso"; LADDER_TSV="$TDIR/ladder_stale76.tsv"
  BLIND_STREAK=2; HALT_FILE="$TDIR/HALT_g4"; STATE_FILE="$TDIR/state_g4"; PLATFORM_LIST_CMD="cat $PJ"
  local outg4 rcg4 stg4
  outg4=$(elo_round_gate); rcg4=$?
  # ⛔ the gate ran in a $() SUBSHELL, so the shell var is unchanged — the
  # PERSISTED state file is the honest surface for the streak assert.
  stg4=$(awk -F'\t' '$1=="BLIND_STREAK"{print $2}' "$STATE_FILE" 2>/dev/null)
  if [[ $rcg4 -eq 0 && ! -f "$HALT_FILE" && "$stg4" == "0" ]] \
     && print -r -- "$outg4" | grep -q "LIVE PLATFORM READ" \
     && print -r -- "$outg4" | grep -q "sum=-15.00"; then
    ok "elo gate g4: stale archive -> LIVE platform read sum=-15.00 (v152/incomplete/unrated/pre-clock2 all excluded), persisted streak reset, no halt"
  else
    fail "elo gate g4: expected live read sum=-15.00 rc=0 persisted-streak=0, got rc=$rcg4 streak=$stg4 out=$(print -r -- $outg4 | tail -1)"
  fi
  # g5: stale archive + platform showing arm-attributed -41.5 -> HALT.
  cat > "$TDIR/plat41.json" <<PJ2
[
 {"triggeredBy":"ladder","status":"complete","createdAt":"2026-08-16T11:30:00Z","teamAId":"$OUR_TEAM_ID","teamBId":"x","teamAVersion":"140","eloDeltaA":-25.0},
 {"triggeredBy":"ladder","status":"complete","createdAt":"2026-08-16T11:40:00Z","teamAId":"$OUR_TEAM_ID","teamBId":"x","teamAVersion":"154","eloDeltaA":-16.5}
]
PJ2
  BLIND_STREAK=0; HALT_FILE="$TDIR/HALT_g5"; PLATFORM_LIST_CMD="cat $TDIR/plat41.json"
  local outg5 rcg5
  outg5=$(elo_round_gate); rcg5=$?
  if [[ $rcg5 -eq 1 && -f "$HALT_FILE" ]] && print -r -- "$outg5" | grep -q -- "-40 ELO HALT (platform read)"; then
    ok "elo gate g5: stale archive + platform arm-net -41.5 -> HALT created via the fallback"
  else
    fail "elo gate g5: expected platform-read HALT rc=1, got rc=$rcg5 halt=$([[ -f $TDIR/HALT_g5 ]] && echo yes || echo no)"
  fi
  # g6: BOTH surfaces fail -> double-blind, streak increments.
  BLIND_STREAK=0; HALT_FILE="$TDIR/HALT_g6"; STATE_FILE="$TDIR/state_g6"; PLATFORM_LIST_CMD="echo not-json"
  local outg6 rcg6 stg6
  outg6=$(elo_round_gate); rcg6=$?
  stg6=$(awk -F'\t' '$1=="BLIND_STREAK"{print $2}' "$STATE_FILE" 2>/dev/null)
  if [[ $rcg6 -eq 0 && "$stg6" == "1" && ! -f "$HALT_FILE" ]] \
     && print -r -- "$outg6" | grep -q "BOTH surfaces unreadable"; then
    ok "elo gate g6: archive stale AND platform unreadable -> double-blind, persisted streak=1, no verdict"
  else
    fail "elo gate g6: expected double-blind persisted-streak=1 rc=0, got rc=$rcg6 streak=$stg6"
  fi
  # --- (h1-h3) LEAK CHECK cells, both ways.
  CLOCK2="2026-08-16T10:00:00Z"
  cat > "$TDIR/leak_clean.json" <<PJ3
[
 {"triggeredBy":"ladder","status":"complete","createdAt":"2026-08-16T11:00:00Z","teamAId":"$OUR_TEAM_ID","teamBId":"x","teamAVersion":"152","eloDeltaA":-3.0},
 {"triggeredBy":"ladder","status":"complete","createdAt":"2026-08-16T09:00:00Z","teamAId":"$OUR_TEAM_ID","teamBId":"x","teamAVersion":"140","eloDeltaA":-3.0}
]
PJ3
  HALT_FILE="$TDIR/HALT_h1"; PLATFORM_LIST_CMD="cat $TDIR/leak_clean.json"
  local outh1 rch1
  outh1=$(leak_check); rch1=$?
  if [[ $rch1 -eq 0 && ! -f "$HALT_FILE" ]] && print -r -- "$outh1" | grep -q "clean"; then
    ok "leak check h1: holder-only pairings (and a pre-clock2 arm row) -> clean, no halt"
  else
    fail "leak check h1: expected clean rc=0, got rc=$rch1 out=$(print -r -- $outh1 | tail -1)"
  fi
  cat > "$TDIR/leak_bad.json" <<PJ4
[
 {"triggeredBy":"ladder","status":"complete","createdAt":"2026-08-16T11:00:00Z","teamAId":"$OUR_TEAM_ID","teamBId":"x","teamAVersion":"140","eloDeltaA":-3.0,"id":"deadbeef-0000-0000-0000-000000000000"}
]
PJ4
  HALT_FILE="$TDIR/HALT_h2"; PLATFORM_LIST_CMD="cat $TDIR/leak_bad.json"
  local outh2 rch2
  outh2=$(leak_check); rch2=$?
  if [[ $rch2 -eq 1 && -f "$HALT_FILE" ]] && print -r -- "$outh2" | grep -q "LEAK DETECTED"; then
    ok "leak check h2: a rated pairing played by an ARM (v140, post-clock2) -> LEAK DETECTED, HALT created"
  else
    fail "leak check h2: expected leak halt rc=1, got rc=$rch2 halt=$([[ -f $TDIR/HALT_h2 ]] && echo yes || echo no)"
  fi
  HALT_FILE="$TDIR/HALT_h3"; PLATFORM_LIST_CMD="echo not-json"
  local outh3 rch3
  outh3=$(leak_check); rch3=$?
  if [[ $rch3 -eq 0 && ! -f "$HALT_FILE" ]] && print -r -- "$outh3" | grep -q "LEAK-UNKNOWN"; then
    ok "leak check h3: platform unreadable -> LEAK-UNKNOWN (logged, no halt, not a pass)"
  else
    fail "leak check h3: expected unknown rc=0 no-halt, got rc=$rch3"
  fi
  PLATFORM_LIST_CMD=".venv/bin/fcode match list --mine --type ladder --json --limit 60"

  print ""
  if (( bad )); then
    print "*** one or more selftest cells FAILED ***"
    return 1
  fi
  print "PASS: all selftest cells passed."
  return 0
}

# ===========================================================================
# CLI
# ===========================================================================
if [[ "${1:-}" == "--selftest" ]]; then
  selftest
  exit $?
fi
if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  print "usage: tools/fieldcal_scheduler.sh [--selftest]"
  print "  drives LEG-fieldcal-2026-08-16 (docs/prereg/LEG-fieldcal-2026-08-16.md)."
  print "  resumes from \$STATE_FILE (default scratchpad/fieldcal_state.tsv)."
  print "  see the header comment in this file for the full contract."
  exit 0
fi

# APPEND, never truncate: the 07:40:13Z relaunch wiped rounds 1-4 of the leg's
# narrative (halts, gate readings, accepts) — data survived in the state file +
# our_matches.tsv, but the debugging history did not. A restart marks a seam.
print -r -- "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) scheduler (re)start pid=$$ =====" >> "$LOG_FILE" 2>/dev/null || true
say "FIELDCAL SCHEDULER starting. MAIN(pre-leg holder)=$FIELDCAL_MAIN  runner=$RUNNER_CMD  ladder=$LADDER_TSV  AMEND1=868e3312(catch-up, effective r9) — regime boundary in-log, not only sidecar (side-lane D2 rider)"
if ! startup_validate; then
  say "REFUSAL: one or more cell ids failed validation (see above). Fix the table in tools/fieldcal_scheduler.sh before firing. Exiting."
  exit 2
fi
load_state
say "resumed at round=$ROUND_NUM clock2='${CLOCK2:-<unset>}' blind_streak=$BLIND_STREAK"
# AMEND1 EFFECTIVE BOUNDARY (side-lane cert condition D2): rounds before this
# stamp bought accepts under the pure rotation, rounds from it under the
# catch-up rule. Stamped ONCE, to a sidecar the log truncation cannot eat.
AMEND1_MARK=${AMEND1_MARK:-scratchpad/fieldcal_amend1_effective.txt}
if [[ ! -f "$AMEND1_MARK" ]]; then
  print -r -- "AMEND1 catch-up rule EFFECTIVE from round=$ROUND_NUM restart=$(date -u +%Y-%m-%dT%H:%M:%SZ) amendment_commit=868e3312" > "$AMEND1_MARK"
  say "$(cat "$AMEND1_MARK")"
fi
backfill_clock2
main_loop
rc=$?
say "FIELDCAL SCHEDULER exiting rc=$rc round=$ROUND_NUM"
exit $rc
