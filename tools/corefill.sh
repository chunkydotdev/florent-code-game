#!/usr/bin/env zsh
# COREFILL — keep every core busy for a long unattended span. NO LLM. ZERO TOKENS.
#
#   tools/corefill.sh <worklist> [max_shards] [deadline_hours]
#   tools/corefill.sh scratchpad/corefill_work.txt 8 8
#
# Worklist lines (same 5 fields overnight.sh takes), blank/# ignored:
#   <shard_id> <treatment_dir> <control_dir> <target_games> <seed_lo>
#
# WHY THIS EXISTS. Magnus, 2026-08-11: *"can we set up a script that runs them
# continuously for 7-8 hours … if there's a core free it will automatically be
# assigned from a list of bots we want to test?"* — during a span where tokens
# are scarce and cores are not. `ALWAYS_BE_RUNNING` says idle cores are a defect;
# this is the instrument that makes that true without a human in the loop.
#
# ===== THE FOUR GUARDS, EACH ONE AN INCIDENT FROM 2026-08-11 =====
#
# 1. ⛔ IT LAUNCHES. IT NEVER RE-LAUNCHES.
#    At 18:40:13Z `overnight_watch.sh` restarted NINE COMPLETED shards from zero
#    because their outputs had been archived out from under it — a
#    completed-and-archived run and a never-started run were byte-identical to
#    it. A filler that "notices a dead shard and restarts it" is one bad
#    predicate away from destroying a night's work. So: an item is started AT
#    MOST ONCE, tracked by a `.started` marker that is written BEFORE the launch
#    and never removed. A shard that dies is LOGGED AND LEFT. Recovering it is a
#    human decision with the evidence in front of them.
#
# 2. ⛔ `ps` FAILING MEANS BLIND, NOT IDLE.
#    If the process count cannot be read, this refuses to launch rather than
#    assuming zero and flooding the box. An alarm that cannot tell it is blind is
#    this repo's most-repeated defect; so is a filler that reads "no shards
#    running" off a broken pipe.
#
# 3. ⛔ IT GATES ON THE LOAD AVERAGE AS WELL AS THE SHARD COUNT.
#    Shard count is a proxy for core use and it drifts: one `overnight.sh` can
#    hold more than one `fcode run` at a time. If 1-minute load is already above
#    LOAD_CEIL, it waits regardless of how few shards it counts.
#
# 4. ⛔ BASENAME COLLISIONS ARE UNSCORABLE AND ARE REFUSED HERE, NOT DOWNSTREAM.
#    `overnight.sh` scores by SUBSTRING match on the basename, so `_v150cb` vs
#    `_v150cbturret` reads ~100% for the control. It refuses such a pair — but it
#    refuses at launch time, hours in, in a log nobody is reading. This checks the
#    WHOLE worklist up front and refuses to start at all.
#
# ===== LIVE CONTROL — the worklist is RE-READ EVERY POLL =====
#   ADD     : append a line to the worklist. It is picked up within POLL_S.
#   REMOVE  : delete an UNSTARTED line. Started shards are unaffected by edits
#             (deleting a running item's line does NOT stop it -- see CANCEL).
#   CANCEL  : `touch scratchpad/corefill_cancel/<SHARD>` -> that shard is killed
#             at the next poll and marked cancelled. Its rows are KEPT.
#   PAUSE   : `touch scratchpad/COREFILL_STOP` -> launches nothing further;
#             running shards continue. Delete the file to resume.
#   STATUS  : tools/corefill_status.sh
#
# ⛔ CANCEL KILLS, IT DOES NOT REWIND. A cancelled shard's partial rows stay on
# disk and are real games -- `overnight_read.py` pools partial shards and prints
# the shortfall, so a cancelled shard is readable, just under-powered. Nothing
# here ever deletes data.
set -u
source "$(dirname "$0")/lib/runner_pat.sh"
WORK=${1:?worklist file}
MAX_SHARDS=${2:-8}
DEADLINE_H=${3:-8}
OUT=${OUT:-scratchpad/overnight}
POLL_S=${POLL_S:-60}
LOAD_CEIL=${LOAD_CEIL:-11.0}
LOG=${LOG:-scratchpad/corefill.log}
STATE=${STATE:-scratchpad/corefill_started}

mkdir -p $OUT $STATE
# DEADLINE_H=0 means NO DEADLINE. Added 2026-08-13 (s35) after Magnus asked
# "there's a 12 hour deadline?" — the answer being that the deadline is a
# TERMINAL state with nothing to re-arm it, so corefill's own SUCCESSFUL exit
# produces an `ALWAYS_BE_RUNNING: yes` violation by design. Use with
# tools/corefill_forever.sh, which supervises this and is what actually closes
# the loop. A bare 0 here without the supervisor still exits on "ALL WORK
# STARTED AND ALL SHARDS FINISHED" — that is the OTHER terminal exit, and
# raising the deadline never addressed it.
if (( DEADLINE_H == 0 )); then
  DEADLINE=9999999999
else
  DEADLINE=$(( $(date +%s) + DEADLINE_H * 3600 ))
fi

say(){ print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a $LOG }

# ---- guard 5: ONE RUNNER PER WORKLIST -------------------------------------
# ⛔ ADDED 2026-08-15. Guards 1-4 all protect a SHARD from being started twice;
# nothing protected the WORKLIST from being *served* twice. Two runners on one
# worklist each enforce MAX_SHARDS independently, so the box silently runs
# 2 x MAX_SHARDS -- and `--tle 10` is WALL-CLOCK, so oversubscription does not
# merely slow the batch, it corrupts every row both runners produce.
#
# This is not hypothetical bookkeeping: the `.started` marker makes a double
# launch look HARMLESS in the log (the second runner skips started shards and
# reports the same "hold:" lines), which is exactly why it needed a refusal
# rather than a note. Blind is not idle -- if the process table cannot be read
# we REFUSE rather than assume we are alone, same rule as guard 2.
# PID-keyed, not pattern-keyed: $WORK is a PATH and contains `.`, which is a
# regex metacharacter -- a pattern match could over-match and produce a FALSE
# REFUSAL, and a filler that refuses to start is the very outage this file
# exists to prevent.
#
# ⛔ TWO DISCRIMINATORS, AND THE FIRST DRAFT OF THIS GUARD NEEDED BOTH. Written
# with the substring test alone it REFUSED ON A FRESH WORKLIST during its own
# both-verdicts test: the invoking shell's argv contained the literal strings
# `corefill.sh` and the worklist path (they were in the test's own echo lines),
# so the guard matched its own PARENT. A guard that has only ever been watched
# to fire has not been watched to PASS.
#   (a) ANCESTRY  -- never count a process we are descended from.
#   (b) ARGV SHAPE -- require a word ENDING in `corefill.sh` immediately
#       FOLLOWED by the worklist, i.e. an actual invocation, not a mention
#       inside some other command's quoted string.
pt=$(ps ax -o pid=,command= 2>/dev/null)
if [[ -z $pt ]]; then
  say "REFUSING TO LAUNCH: cannot read the process table, so 'am I the only runner?' is UNKNOWN, not NO."
  exit 3
fi
# (a) collect our ancestor pids
typeset -A _anc
_p=$$
while [[ -n $_p && $_p != 0 && $_p != 1 ]]; do
  _anc[$_p]=1
  _p=$(ps -o ppid= -p $_p 2>/dev/null | tr -d ' ')
done
others=0
while read -r _pid _cmd; do
  [[ -n ${_anc[$_pid]:-} ]] && continue                       # (a)
  _hit=0                                                       # (b)
  _words=(${=_cmd})
  for _i in {1..$#_words}; do
    [[ ${_words[$_i]} == *corefill.sh ]] || continue
    (( _i < $#_words )) && [[ ${_words[$_i+1]} == $WORK ]] && _hit=1
  done
  (( _hit )) || continue
  others=$(( others + 1 ))
  say "  already serving this worklist: pid $_pid -- $_cmd"
done <<< "$pt"
if (( others > 0 )); then
  say "REFUSING TO LAUNCH: $others other corefill.sh already serving $WORK."
  say "  Two runners each enforce MAX_SHARDS separately -> 2x oversubscription -> --tle 10 is wall-clock -> corrupted rows."
  say "  Kill the other runner first, or point this one at a different worklist."
  exit 3
fi

# ---- guard 4: validate the WHOLE worklist before starting anything ----------
bad=0; n=0
while read -r SH TR CT TG SL; do
  [[ -z ${SH:-} || $SH == \#* ]] && continue
  n=$(( n + 1 ))
  [[ -f $TR/main.py ]] || { say "REFUSE: $SH treatment $TR has no main.py"; bad=1; }
  [[ -f $CT/main.py ]] || { say "REFUSE: $SH control   $CT has no main.py"; bad=1; }
  B=${TR:t}; C=${CT:t}
  if [[ $B == $C || $B == *$C* || $C == *$B* ]]; then
    say "REFUSE: $SH basenames collide ($B vs $C) -- overnight.sh scores by SUBSTRING, so every control win would score as a treatment win"
    bad=1
  fi
done < $WORK
(( bad )) && { say "*** WORKLIST INVALID -- nothing started ***"; exit 2 }
(( n == 0 )) && { say "*** WORKLIST EMPTY -- nothing to do ***"; exit 2 }
say "COREFILL up. work=$WORK items=$n max_shards=$MAX_SHARDS deadline=${DEADLINE_H}h out=$OUT load_ceil=$LOAD_CEIL"
say "policy: LAUNCH ONCE, NEVER RELAUNCH. a dead shard is logged and left."

while true; do
  now=$(date +%s)
  if (( now >= DEADLINE )); then
    say "DEADLINE reached (${DEADLINE_H}h). Launching nothing further; running shards continue."
    break
  fi

  # ---- live control: cancel + pause, checked before any launch decision ----
  if [[ -d scratchpad/corefill_cancel ]]; then
    for cf in scratchpad/corefill_cancel/*(N); do
      csh=${cf:t}
      if ps ax -o command= 2>/dev/null | grep -q "$RUNNER_PAT $csh "; then
        say "CANCEL $csh -- killing on request. Partial rows are KEPT and remain readable."
        pkill -f "$RUNNER_PAT_PKILL $csh " 2>/dev/null
      fi
      print -r -- "cancelled $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $STATE/$csh
      rm -f $cf
    done
  fi
  if [[ -f scratchpad/COREFILL_STOP ]]; then
    say "PAUSED (scratchpad/COREFILL_STOP present). Running shards continue; launching nothing."
    sleep $POLL_S; continue
  fi

  # ---- guard 2: blind is not idle -----------------------------------------
  # `grep -c` EXITS 1 ON ZERO MATCHES — it fails exactly when the answer
  # is CLEAN. Harmless today (no `set -e` here), fatal the moment anyone
  # adds one: measured, `set -e; n=$(grep -c zzz f)` ABORTS the script
  # while `echo "$(grep -c zzz f)"` does not. `|| true` keeps the count
  # (grep still prints 0) and drops the status. TEST ON THE COUNT, NEVER $?.
  running=$(ps ax -o command= 2>/dev/null | grep -c "$RUNNER_PAT " || true)
  if [[ -z $running ]]; then
    say "BLIND: cannot read process table -- refusing to launch this cycle"
    sleep $POLL_S; continue
  fi

  # ---- guard 3: load ceiling ----------------------------------------------
  load1=$(uptime | sed 's/.*averages: *//' | awk '{print $1}' | tr -d ',')
  over=$(awk -v a="$load1" -v b="$LOAD_CEIL" 'BEGIN{print (a>b)?1:0}')

  # ---- guard 5: THE CONTROL TREE HAS NOT MOVED -----------------------------
  # ⛔ ADDED 2026-08-15 AFTER THREE FORKS IN ONE AFTERNOON. The incumbent is the
  # CONTROL for every queued row. It was edited in the working tree three times
  # while shards referencing it were running -- twice by me, the second time 90
  # minutes after I committed the rule forbidding it, and every occurrence was
  # caught by another lane sampling trees BY HAND rather than by any tool.
  #
  # THE FAILURE IS SILENT AND DIRECTIONAL: nothing errors, every shard keeps
  # writing, and the rows quietly measure `plank + (control_after - before)`.
  # Because the edit made the control CHEAPER while treatments still paid, the
  # delta ran the SAME WAY for every arm. Under a WALL-CLOCK --tle 10 that is a
  # behavioural handicap, and it compounds with the auto-stopper: an arm reading
  # low because its control got faster is indistinguishable from a dead plank,
  # so the canceller kills the real ones.
  #
  # ⭐ WHY A GUARD AND NOT A RULE: a control md5 was pinned for exactly this on
  # the FIRST occurrence and NOTHING CONSUMED IT. The rule was written, cited
  # twice, and self-enforced once -- and did not fire the second time. The
  # mechanism holds; the attention does not.
  #
  # Fails CLOSED: an absent pin, an unreadable tree, or a PROGRAMME.md with no
  # INCUMDENT all REFUSE, because each is exactly what the silent case looks
  # like. Re-pin deliberately (`control_pin.py --pin`) after re-basing or
  # reverting -- never to silence this.
  # ⛔ THE INTERPRETER IS PART OF THE GUARD. If .venv/bin/python is missing, the
  # check cannot run -- and a guard that cannot run must REFUSE, not skip. A
  # missing interpreter is indistinguishable from a passing check to any
  # `if ! cmd` test, which is precisely how a guard becomes decorative.
  CPIN_PY=${CPIN_PY:-.venv/bin/python}
  if [[ ! -x $CPIN_PY ]]; then
    say "REFUSING TO LAUNCH: $CPIN_PY not executable — the control-pin guard cannot run, so it refuses."
    sleep $POLL_S; continue
  fi
  if ! $CPIN_PY tools/control_pin.py --check >/dev/null 2>&1; then
    say "REFUSING TO LAUNCH: control tree moved (or is unverifiable). Details:"
    $CPIN_PY tools/control_pin.py --check 2>&1 | sed 's/^/    /'
    sleep $POLL_S; continue
  fi

  # ---- guard 6: EVERY LIVE ROW IS SCORED AGAINST THE INCUMBENT -------------
  # ⛔ MAGNUS, 2026-08-15: "Everything needs to beat 140, nothing else matters."
  # v140 == bots/_v223sealrepair (corpus/version_trees.tsv:70).
  #
  # ⭐ WHY A GUARD RATHER THAN A CONVENTION: A ROW AGAINST AN OLDER CONTROL
  # SORTS TO THE TOP OF THE LEADERBOARD. It is scored against a weaker bot, so
  # it reads HIGH -- today's board had SALTIDLE2 at 64.57% (vs v116), SALT at
  # 61.00% (vs v116) and MAPCODE at 73.27% (vs another ARM's treatment) sitting
  # above every honest v140 read, which tops out at 55.4%. I quoted three of
  # them to Magnus as leaders before he asked what they were measured against.
  # The failure is not merely silent, it is FLATTERING -- which is why it needs
  # a check and not a habit.
  #
  # Scoped to rows that will still RUN (a .started marker exempts history, which
  # cannot be fixed and must not nag) and nulls are exempt STRUCTURALLY
  # (treatment path == control path), never by name.
  if ! $CPIN_PY tools/control_pin.py --audit "$WORK" >/dev/null 2>&1; then
    say "REFUSING TO LAUNCH: a live row is not scored against the incumbent. Details:"
    $CPIN_PY tools/control_pin.py --audit "$WORK" 2>&1 | sed 's/^/    /'
    sleep $POLL_S; continue
  fi

  launched=0
  if (( running < MAX_SHARDS )) && (( over == 0 )); then
    while read -r SH TR CT TG SL; do
      [[ -z ${SH:-} || $SH == \#* ]] && continue
      # ---- guard 1: at most once, marker written BEFORE the launch ---------
      [[ -f $STATE/$SH ]] && continue
      # ---- guard 4b: RE-CHECK THE COLLISION AT LAUNCH, NOT ONLY AT STARTUP --
      # ⛔ ADDED 2026-08-13 (s35) BY WALKING INTO IT. Guard 4's docstring says it
      # "checks the WHOLE worklist up front and refuses to start at all" -- true
      # of the worklist AS IT WAS AT STARTUP. The worklist is RE-READ EVERY POLL
      # and ADD is now the entire operator interface, so a line appended later
      # NEVER met that check. I appended `SALTNULL _v178salt_null vs _v178salt`,
      # corefill launched it, and `overnight.sh` refused it at 05:11:09Z --
      # burning a shard slot and a `.started` marker (which is never removed, so
      # the id is spent) to discover something the up-front check already knew
      # how to detect. **A guard that runs once cannot protect a surface that
      # changes.** Same predicate as overnight.sh:71, deliberately duplicated
      # here so the refusal happens BEFORE the marker is written.
      _b=${TR:t}; _c=${CT:t}
      if [[ $_b == $_c || $_b == *$_c* || $_c == *$_b* ]]; then
        say "REFUSING $SH: basenames collide ('$_b' vs '$_c') -- unscorable, NOT started (no marker written)"
        continue
      fi
      print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > $STATE/$SH
      say "LAUNCH $SH  $TR vs $CT  target=$TG seed_lo=$SL   (running was $running, load $load1)"
      # WORKERS is the fleet width this shard shares the box with; it lands in
      # the shard tape's FIXTURE header, where a later reader needs it to judge
      # whether a shard was CPU-starved. A bare `overnight.sh` invocation
      # defaults it to 1, which is true of a bare invocation.
      WORKERS=$MAX_SHARDS nohup zsh tools/overnight.sh $SH $TR $CT $TG $SL >> $OUT/${SH}.launch.log 2>&1 &
      launched=1
      break
    done < $WORK
  fi

  if (( launched == 0 )); then
    remaining=0
    while read -r SH _r; do
      [[ -z ${SH:-} || $SH == \#* ]] && continue
      [[ -f $STATE/$SH ]] || remaining=$(( remaining + 1 ))
    done < $WORK
    if (( remaining == 0 )) && (( running == 0 )); then
      say "ALL WORK STARTED AND ALL SHARDS FINISHED. exiting."
      break
    fi
    say "hold: running=$running/$MAX_SHARDS load=$load1 unstarted=$remaining"
  fi
  sleep $POLL_S
done
say "COREFILL done."
# ⛔⛔ EXPLICIT TERMINATOR. THIS IS NOT DECORATION — IT CLOSES A MEASURED DEFECT.
#
# WHAT HAPPENED (2026-08-17T04:30:22Z, corefill.log:8266-8269). The runner
# printed `ALL WORK STARTED AND ALL SHARDS FINISHED. exiting.` then
# `COREFILL done.` and then TWO SHELL ERRORS:
#     tools/corefill.sh:310: command not found: SH:-
#     tools/corefill.sh:310: = not found
# It was read as "a broken ${SH:-...} expansion on a live fleet script". IT IS
# NOT. There is no such bug in this file, and the SAME code path ran clean five
# minutes later (04:35:41Z) off the SAME script.
#
# THE ACTUAL CAUSE IS THAT THIS FILE WAS REWRITTEN IN PLACE WHILE IT WAS
# RUNNING. That instance started 2026-08-16T08:17:45Z (corefill.log:7016). Commit
# cdceff02 edited this file at 2026-08-16T20:19:48Z — TWELVE HOURS INTO THE RUN —
# adding 6 lines and removing 1. The pre-cdceff02 file was 309 lines and its LAST
# line was `say "COREFILL done."`. zsh keeps an open fd with a byte offset; when
# the `while` loop finally broke, the shell went back to the file for the next
# command, found the file had GROWN under it, and executed fragments of the new
# bytes. The reported line number, 310, is EXACTLY one past the old EOF —
# `SH:-` and `=` are mid-token fragments, not a real expansion.
#
# REPRODUCED (WRAP-FIX s48) with a 260-line stand-in: grow it in place mid-run
# and it prints its trailers and then `t3.zsh:261: === not found`, rc 1 — the
# same shape at the same offset-past-old-EOF. With this `exit 0` present, the
# identical experiment is CLEAN, rc 0. Both verdicts driven.
#
# ⚠ NOTE THE INODE RULE, because it is what decides whether an edit is dangerous:
# only a SAME-INODE rewrite (`cat new > file`, in-place truncate) reaches a
# running shell. An editor that writes a temp file and renames gives the new
# content a NEW inode, and the running shell keeps reading the old, unlinked one
# — verified here by comparing `lsof -p <pid>` against `stat -f %i`.
#
# SCOPE OF THIS FIX, stated honestly: `exit 0` closes the TAIL case (reading past
# the old EOF) and nothing else. A mid-loop offset shift is still possible in
# principle; the real immunity is to parse the whole file before executing any of
# it (wrap the body in `main() { ... }; main "$@"`), which is a large restructure
# of a script that is live on the fleet right now and was NOT done here.
# The observed occurrence was harmless — it fired after the last statement, and
# corefill_forever.sh relaunched 18 s later at 04:30:40Z and read the new file
# correctly — so this CANNOT prevent relaunch when real work arrives. Cosmetic
# in that instance; the class is not, which is why the terminator goes in.
exit 0
