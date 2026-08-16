#!/usr/bin/env zsh
# WATCHDOG — the thing that watches the watchers, with no session involved.
#
#   zsh tools/watchdog.sh            # one pass; restart MISSING+AUTO rows
#   zsh tools/watchdog.sh --dry-run  # report only, change nothing
#   zsh tools/watchdog.sh --selftest # drive both verdicts
#
# Installed as a launchd agent (see tools/watchdog.plist) so it runs every 10
# minutes whether or not anyone is logged in, whether or not Claude Code is
# running, and whether or not a session ended badly.
#
# ===== WHY THIS EXISTS =====
# `corefill_forever.sh` supervises `corefill.sh`. NOTHING SUPERVISED
# `corefill_forever.sh`. On 2026-08-15 it was found DEAD FOR 22 HOURS: it paused
# on `COREFILL_STOP`, the session that would have removed the pause ended, and
# no process anywhere was responsible for noticing. The live runner carried a
# 12-hour deadline, so the box was set to stop launching at ~03:40Z with 55
# items unstarted and eight cores idle.
#
# ⭐ AND THE HARNESS CANNOT DO THIS FOR US. Every daemon here is a detached
# `PPID 1` process started from a shell. Claude Code starts them and then has no
# relationship with them -- no supervision, no restart, no notification on
# death. A `SessionStart` hook only helps when a session starts; the outage
# above happened overnight, with no session at all. **A supervisor whose only
# watchdog is "somebody opens a session tomorrow" is not supervised.**
#
# ===== WHAT IT WILL AND WILL NOT DO =====
#   WILL   relaunch a row that `fleet_health.py` reports MISSING **and** marks
#          AUTO -- i.e. one where a WRONG restart cannot destroy work.
#   WILL   log every action, and every refusal, with a UTC timestamp.
#   WON'T  ever kill anything. A DUPLICATE is reported and left alone; deciding
#          which of two live daemons dies is a judgement about what else is
#          already talking to them.
#   WON'T  touch shard runners, `corefill.sh`, `auto_gate`, or `holder_watch`.
#          On 2026-08-11 `overnight_watch.sh` restarted NINE COMPLETED shards
#          from zero because a finished-and-archived run and a never-started run
#          were byte-identical to it. That is the blast radius this file refuses
#          to have.
#   WON'T  act when BLIND. If the process table cannot be read, "missing" is
#          UNKNOWN, not TRUE, and starting a second copy of everything is the
#          worst available move.
#   WON'T  act while `scratchpad/COREFILL_STOP` exists. A deliberate pause must
#          not be undone by automation -- otherwise the pause button is a lie.
set -u
cd ${0:A:h:h} || exit 1

DRY=0; [[ "${1:-}" == "--dry-run" ]] && DRY=1
LOG=${WATCHDOG_LOG:-scratchpad/watchdog.log}
PY=${WATCHDOG_PY:-.venv/bin/python}
# TEST SEAM. The decision paths below (BLIND / 0-actionable / restart-and-confirm)
# cannot be driven from the real fleet without killing live daemons, and a
# watchdog whose branches have never been executed is the thing it exists to
# prevent. Tests point this at a fixture; production must leave it alone.
FH=${WATCHDOG_FH:-"$PY tools/fleet_health.py --json"}
mkdir -p "$(dirname $LOG)"

say() { print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" >> $LOG }

# ---- refuse to undo a deliberate pause -------------------------------------
if [[ -f scratchpad/COREFILL_STOP ]]; then
  say "PAUSED (scratchpad/COREFILL_STOP present) -- taking no action this pass."
  exit 0
fi

J=$(eval "$FH" 2>>$LOG)
RC=$?

if [[ -z $J ]]; then
  say "REFUSING: fleet_health produced no output (rc=$RC). Cannot act on nothing."
  exit 2
fi

BLIND=$(print -r -- "$J" | $PY -c 'import json,sys; print(json.load(sys.stdin)["blind"])')
if [[ $BLIND == "True" ]]; then
  say "REFUSING: BLIND -- process table unreadable. 'Missing' is UNKNOWN, not TRUE."
  exit 2
fi

# ---- act ONLY on MISSING + AUTO --------------------------------------------
# Emits one TAB-separated line per actionable row: label \t fix-command
ACTIONS=$(print -r -- "$J" | $PY -c '
import json, sys
d = json.load(sys.stdin)
for r in d["rows"]:
    if r["state"] == "MISSING" and r["auto"]:
        print(r["label"] + "\t" + r["fix"])
')

# Report duplicates without touching them, so the log is a complete picture.
# NOTE: plain concatenation, no f-strings. Nested double quotes inside a
# single-quoted `-c` payload are a quoting trap and the first draft of this
# block died on exactly that -- silently, with the watchdog still exiting 0.
print -r -- "$J" | $PY -c '
import json, sys
d = json.load(sys.stdin)
for r in d["rows"]:
    label, pids = r["label"], r["pids"]
    if r["state"] == "DUPLICATE":
        exp = r["expected"] or 1
        extra = " ".join(str(p) for p in pids[exp:])
        print("DUPLICATE (NOT killed, by policy): " + label
              + " pids=" + ",".join(str(p) for p in pids)
              + " -> a human runs: kill " + extra)
    elif r["state"] == "MISSING" and not r["auto"]:
        print("MISSING but NOT auto-restartable (human decides): " + label
              + " -- " + r["fix"])
' | while IFS= read -r line; do say "$line"; done

# ⛔ THE WATCHDOG STATES ITS OWN DECISION, ALWAYS.
# On 2026-08-15 two launchd-driven passes took NO ACTION while the supervisor
# was MISSING, and the log was byte-identical to a healthy pass -- it recorded
# only the duplicates. The cause was never reproduced. **That is precisely the
# defect class this repo names most often: a silent no-op is indistinguishable
# from a working pass.** Whatever the cause was, it is now self-diagnosing --
# every pass says how many rows it judged actionable and why it stopped.
# `grep -c` EXITS 1 ON ZERO MATCHES — it fails exactly when the answer
# is CLEAN. Harmless today (no `set -e` here), fatal the moment anyone
# adds one: measured, `set -e; n=$(grep -c zzz f)` ABORTS the script
# while `echo "$(grep -c zzz f)"` does not. `|| true` keeps the count
# (grep still prints 0) and drops the status. TEST ON THE COUNT, NEVER $?.
NACT=$(print -r -- "$ACTIONS" | grep -c '[^[:space:]]' || true)
if [[ -z $ACTIONS || $NACT -eq 0 ]]; then
  say "PASS COMPLETE: 0 actionable row(s) (MISSING+AUTO). Nothing to restart."
  exit 0
fi
say "PASS: $NACT actionable row(s) (MISSING+AUTO) -- restarting them now."

n=0
print -r -- "$ACTIONS" | while IFS=$'\t' read -r LABEL FIX; do
  [[ -z ${LABEL:-} ]] && continue
  n=$(( n + 1 ))
  if (( DRY )); then
    say "DRY-RUN would restart: $LABEL  ->  $FIX"
    continue
  fi
  say "RESTARTING (MISSING + AUTO): $LABEL"
  say "  cmd: $FIX"
  eval "$FIX" >/dev/null 2>>$LOG
  sleep 3
  # CONFIRM, never assume. `eval` succeeding says the shell forked, not that the
  # daemon came up -- this repo's standing rule is that alive-in-ps is the
  # evidence and an exit code is not.
  AFTER=$(print -r -- "$(eval "$FH" 2>/dev/null)" | $PY -c "
import json,sys
d=json.load(sys.stdin)
print(next((r['found'] for r in d['rows'] if r['label']=='''$LABEL'''), -1))
" 2>/dev/null)
  if [[ ${AFTER:-0} -ge 1 ]]; then
    say "  CONFIRMED alive ($LABEL found=$AFTER)"
  else
    say "  ⚠ RESTART DID NOT TAKE ($LABEL found=${AFTER:-?}) -- will retry next pass"
  fi
done

exit 0
