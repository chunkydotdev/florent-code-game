#!/usr/bin/env zsh
# COREFILL_FOREVER — supervise corefill so its own SUCCESS stops being a defect.
#
#   nohup zsh tools/corefill_forever.sh scratchpad/corefill_work.txt 8 > scratchpad/corefill_forever.log 2>&1 &
#
# ===== WHY THIS EXISTS =====
# Magnus, 2026-08-13 (s35), on being shown the morning's idle cores:
# *"There's a 12 hour deadline?"*
#
# Yes — and the deadline was never the bug. `corefill.sh` has TWO terminal
# exits and BOTH leave every core idle with nothing to re-arm them:
#
#   1. `DEADLINE reached (Nh). Launching nothing further` -> break
#   2. `ALL WORK STARTED AND ALL SHARDS FINISHED. exiting.` -> break
#
# Measured last night: exit (1) fired at 2026-08-13T01:52:15Z and the box sat
# idle until 04:36:04Z. The side lane's `cores_idle` monitor counted **14
# consecutive idle polls (~70 min)** before a human looked.
#
# ⭐ AND RAISING THE DEADLINE WOULD NOT HAVE SAVED IT. Thirteen shards were
# queued; once they finished, exit (2) fires regardless of how much deadline is
# left. `ALWAYS_BE_RUNNING: yes` is a PROGRAMME field, and corefill's normal
# successful termination violates it BY DESIGN. That is a structural defect, not
# a tuning mistake, and it is why the fix is a supervisor rather than a bigger
# number.
#
# ===== WHY RESTARTING THE RUNNER IS SAFE, WHEN RESTARTING A SHARD IS NOT =====
# `corefill.sh` guard 1 is "LAUNCH ONCE, NEVER RELAUNCH", enforced by a
# `.started` marker written BEFORE each launch and never removed. That marker is
# exactly what makes THIS script safe: a relaunched runner re-reads the worklist
# and skips every shard that already has a marker. The 18:40:13Z incident that
# guard was written for — nine COMPLETED shards restarted from zero because their
# outputs had been archived away — cannot recur through this path, because we
# never touch markers or output. We restart the SUPERVISOR, never the WORK.
#
# ===== WHAT IT DELIBERATELY DOES NOT DO =====
# ⛔ IT DOES NOT PICK WORK FROM `QUEUE.md`. It would be one line to make it
# auto-start the top queue row, and that line would be wrong: the side lane
# demonstrated on 2026-08-13 that our two queue parsers DISAGREE about which row
# is top — `queue_check.py` counts 19/20 rows under a `GREP:` admission gate
# while `cores_idle.py` returns `rows[0]` with no gate, and `QUEUE.md`'s own fire
# order declares positional order superseded anyway. Auto-firing a row that two
# instruments cannot agree on is worse than idling, because it burns cores on
# work nobody chose. So when the worklist drains, this ALARMS and keeps polling —
# an ADD to the worklist is picked up within POLL_S and everything resumes.
# ⇒ THE WHOLE OPERATOR INTERFACE IS: append a line to the worklist.
set -u
WORK=${1:?worklist file}
MAX_SHARDS=${2:-8}
POLL_S=${POLL_S:-120}
STATE=${STATE:-scratchpad/corefill_started}
ALARM=${ALARM:-scratchpad/COREFILL_WORKLIST_DRAINED}
# TEST SEAM. The drained-and-idle alarm can only fire when NOTHING is running,
# which on this box is the one state we refuse to be in — so without a seam the
# alarm branch could never be driven to its firing verdict, and an alarm that has
# never fired has not been seen to work. Tests override this pattern to one that
# matches no process. Production must leave it alone.
SHARD_PAT=${SHARD_PAT:-'[o]vernight.sh '}

cd ${0:A:h:h} || exit 1
say() { print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" }

[[ -f $WORK ]] || { say "FATAL: worklist $WORK does not exist"; exit 2 }
say "COREFILL_FOREVER up. work=$WORK max_shards=$MAX_SHARDS poll=${POLL_S}s"
say "policy: restart the RUNNER on any exit; never touch a shard marker or its rows."

while true; do
  # --- honour the same pause file corefill does, so one flag stops everything ---
  if [[ -f scratchpad/COREFILL_STOP ]]; then
    say "PAUSED (scratchpad/COREFILL_STOP present) -- not supervising until it is removed."
    sleep $POLL_S; continue
  fi

  # --- guard: BLIND IS NOT DOWN. If the process table cannot be read we must
  #     not conclude "corefill is dead" and start a second one. This repo's
  #     most-repeated defect is an alarm that cannot tell it is blind. ---
  pt=$(ps ax -o command= 2>/dev/null)
  if [[ -z $pt ]]; then
    say "BLIND: cannot read process table -- refusing to (re)launch this cycle"
    sleep $POLL_S; continue
  fi

  if print -r -- "$pt" | grep -q "[c]orefill.sh $WORK"; then
    sleep $POLL_S; continue                       # runner alive, nothing to do
  fi

  # --- runner is down. Is there anything left to run? ---
  remaining=0
  while read -r SH _rest; do
    [[ -z ${SH:-} || $SH == \#* ]] && continue
    [[ -f $STATE/$SH ]] || remaining=$(( remaining + 1 ))
  done < $WORK

  if (( remaining == 0 )); then
    running=$(print -r -- "$pt" | grep -c "$SHARD_PAT")
    if (( running == 0 )); then
      if [[ ! -f $ALARM ]]; then
        say "*** WORKLIST DRAINED AND NOTHING RUNNING -- ALWAYS_BE_RUNNING VIOLATED ***"
        say "*** Cores are idle and this script will NOT invent work. ADD a line to $WORK. ***"
        print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ) worklist drained, cores idle" > $ALARM
      fi
    fi
    sleep $POLL_S; continue
  fi
  rm -f $ALARM

  say "RUNNER DOWN with $remaining unstarted item(s) -- relaunching corefill (deadline 0 = none)"
  # ⛔ STDOUT GOES TO /dev/null ON PURPOSE. corefill.sh's own say() already
  # `tee -a`s into scratchpad/corefill.log, so redirecting stdout there too
  # wrote EVERY LINE TWICE (measured 2026-08-15: 5,133 "hold:" lines, each a
  # duplicate, and TWO identical `COREFILL up` banners at 15:40:28Z for ONE
  # runner). A doubled banner reads as a doubled RUNNER, which is the single
  # most alarming thing this log can falsely say. stderr is still captured --
  # it carries real subprocess failures and is not produced by say().
  nohup zsh tools/corefill.sh $WORK $MAX_SHARDS 0 >/dev/null 2>> scratchpad/corefill.log &
  sleep 10
  if print -r -- "$(ps ax -o command= 2>/dev/null)" | grep -q "[c]orefill.sh $WORK"; then
    say "relaunch CONFIRMED alive"
  else
    say "⚠ relaunch did NOT come up -- will retry next poll"
  fi
  sleep $POLL_S
done
