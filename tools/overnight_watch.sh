#!/usr/bin/env zsh
# OVERNIGHT WATCHDOG — restarts dead shards. NO LLM. Zero tokens.
#
#   tools/overnight_watch.sh <spec_file>
#   spec file lines:  <shard_id> <treatment> <control> <target> <seed_lo>
#
# ⛔ WHY A SHELL LOOP AND NOT AN AGENT. Magnus offered "a sonnet agent that makes
# sure it works well but doesn't steal too many tokens". The failures this has to
# catch are ASSERTION-SHAPED: a shard died, a heartbeat went stale, a null arm
# came back degenerate. None of those needs judgment; all of them need a restart
# or an alert. An agent polling every 5 min for 6 h is ~72 wake-ups to print
# "still fine". **HEALTHY NIGHT = ZERO LLM INVOCATIONS.**
#
# ⛔ AND THE FAILURE IT EXISTS FOR: a run that dies at hour one is
# INDISTINGUISHABLE from one that is working, if nobody reports liveness. That is
# this repo's signature defect -- ship_watch printed healthy lines off a tape
# seven minutes stale, and a healthy line and a blind line were byte-identical.
#
# GATES ON THE HEARTBEAT FILE'S CONTENT AND AGE, NEVER ON AN EXIT CODE.
#
# ⛔⛔ THIRD FAILURE, s32 2026-08-11 18:40:13Z, AND IT COST NOTHING ONLY BY LUCK.
# A run FINISHED, its outputs were ARCHIVED to another directory by a launcher,
# and THIS WATCHDOG -- still polling the old spec -- saw no `.COMPLETE` and no
# heartbeat for any of the nine shards, read `prog=none`, and RESTARTED ALL NINE
# FROM ZERO within one second. 14 shards then ran on 10 cores for three minutes.
#
# **A COMPLETED-AND-ARCHIVED RUN AND A NEVER-STARTED RUN WERE BYTE-IDENTICAL TO
# IT.** That is this file's own docstring defect for the THIRD time: first a
# guard that could not fire (`&&` vs `||`), then a hung shard printing "ok", now
# a watchdog that cannot tell "my files were taken away" from "my shard died".
#
# ⛔ AND NOTE WHICH CHECK MISSED IT: the s31 F13 audit asked "does anything
# create the COMPLETE marker?" and answered YES, empirically, correctly. Nobody
# asked what happens when the marker is REMOVED while the watchdog still lives.
# The claim was right, the refutation of it was wrong, and the failure came
# through a door neither covered.
#
# THE GUARD BELOW: progress is MONOTONIC. A shard's row count can only rise. If
# it FALLS -- or the .tsv vanishes -- that is EXTERNAL INTERFERENCE, not a dead
# shard, and a restart would destroy work rather than resume it. REFUSE and
# ALERT. Restarting is only ever correct when progress STALLED, never when it
# went BACKWARDS.
# Belt as well as braces: a launcher that archives a finished run MUST STOP THIS
# WATCHDOG FIRST. That is the actual ordering bug; this guard is what makes the
# ordering bug survivable instead of destructive.
set -u
SPEC=${1:?spec file}
# ⛔ `${OUT:-...}` NOT a bare assignment, s32. This was hardcoded, so an
# `OUT=... zsh tools/watchdog.sh` invocation SILENTLY WROTE TO THE LIVE DIRECTORY.
# Measured the hard way: a throwaway watchdog fixture, believed isolated by that
# exact env var, instead ran against the live run -- created `FX.*` files beside
# five live shards, appended to their ALERT and watch.log, and launched a stray
# shard. Harmless only by luck (its bots did not exist, so every game recorded
# NOWINNER). **The trap had ALREADY been found in the sibling script an hour
# earlier and worked around in the launcher rather than fixed at the source --
# so the workaround protected the launcher and left the next caller exposed.**
# Fixing the source is what makes a test fixture possible at all: a guard that
# cannot be exercised in isolation cannot be driven to both verdicts.
OUT=${OUT:-scratchpad/overnight}
ALERT=$OUT/ALERT
STALE_S=${STALE_S:-240}      # heartbeat older than this = dead
MAX_RESTARTS=${MAX_RESTARTS:-3}
POLL_S=${POLL_S:-120}
mkdir -p $OUT
typeset -A RESTARTS
typeset -A MAXROWS      # high-water row count per shard; progress is MONOTONIC

say(){ print -r -- "$(date -u +%H:%M:%SZ) $*" | tee -a $OUT/watch.log }

say "WATCHDOG up. spec=$SPEC stale=${STALE_S}s poll=${POLL_S}s max_restarts=$MAX_RESTARTS"

# ⛔ STARTUP REFUSAL, s32 -- and it closes the hole the monotonicity guard CANNOT.
# MAXROWS is PER-PROCESS state, so on the FIRST poll hwm is 0 for every shard and
# `rows < hwm` can never be true. ⇒ point a FRESH watchdog at a spec whose run has
# already completed and been archived, and it sees rows=0, hwm=0, no fall, falls
# through to the death check, and RESTARTS THE WORLD -- the s31 incident verbatim,
# minus the coincidence that saved the diagnosis (that watchdog had been alive two
# hours and therefore HAD a high-water mark).
# That path is not contrived: it is the natural response to the incident itself
# ("I should start a watchdog"), or a crash restart, or a successor reading the
# runbook. **The guard catches "I was already watching"; it cannot catch "I was
# pointed at an archived run."**
# A launched shard ALWAYS leaves its .tsv behind, so "spec names shards, directory
# has none" is NEVER a supervisable state -- it is an archived run or a wrong
# --dir/OUT. A watchdog that begins by finding nothing to watch must SAY SO AND
# EXIT, not restart the world. Stateless, one check, and it also catches a
# mistyped spec path. (Side lane, who opened the diff rather than the subject.)
found=0; listed=0
while read -r SH _rest; do
  [[ -z ${SH:-} || $SH == \#* ]] && continue
  listed=$(( listed + 1 ))
  [[ -f $OUT/${SH}.tsv ]] && found=$(( found + 1 ))
done < $SPEC
if (( listed > 0 && found == 0 )); then
  say "*** REFUSING TO START: $SPEC names $listed shard(s) and $OUT contains NO .tsv for any of them. ***"
  say "*** That is an ARCHIVED/finished run or a wrong OUT -- not a supervisable state. ***"
  say "*** Restarting here would relaunch every shard FROM ZERO. Exiting instead. ***"
  print -r -- "$(date -u +%H:%M:%SZ) WATCHDOG REFUSED TO START: $listed shards in spec, 0 .tsv in $OUT" >> $ALERT
  exit 3
fi
say "startup check: $found/$listed shards have a .tsv in $OUT -- supervisable"

while true; do
  alldone=1
  while read -r SH TR CT TG SL; do
    [[ -z ${SH:-} || $SH == \#* ]] && continue
    HB=$OUT/${SH}.heartbeat
    if [[ -f $OUT/${SH}.COMPLETE ]]; then continue; fi
    alldone=0
    now=$(date -u +%s)
    if [[ -f $HB ]]; then
      hbts=$(stat -f %m $HB)
      age=$(( now - hbts ))
      prog=$(awk -F'\t' '{print $2"/"$3}' $HB)
    else
      age=999999; prog="none"
    fi
    # --- MONOTONICITY GUARD (s32). Must run BEFORE any restart decision. ---
    rows=0
    [[ -f $OUT/${SH}.tsv ]] && rows=$(( $(wc -l < $OUT/${SH}.tsv) - 1 ))
    (( rows < 0 )) && rows=0
    hwm=${MAXROWS[$SH]:-0}
    if (( rows < hwm )); then
      say "*** $SH PROGRESS WENT BACKWARDS ($hwm -> $rows rows) -- NOT a dead shard. ***"
      say "*** Files were moved, truncated or deleted underneath me. REFUSING to restart. ***"
      print -r -- "$(date -u +%H:%M:%SZ) $SH EXTERNAL INTERFERENCE: rows $hwm -> $rows, refused restart" >> $ALERT
      continue
    fi
    MAXROWS[$SH]=$rows

    # `grep -c` EXITS 1 ON ZERO MATCHES — it fails exactly when the answer
    # is CLEAN. Harmless today (no `set -e` here), fatal the moment anyone
    # adds one: measured, `set -e; n=$(grep -c zzz f)` ABORTS the script
    # while `echo "$(grep -c zzz f)"` does not. `|| true` keeps the count
    # (grep still prints 0) and drops the status. TEST ON THE COUNT, NEVER $?.
    alive=$(ps ax -o command= | grep -c "[o]vernight.sh $SH " || true)
    # ⛔⛔ `||` NOT `&&`. The first version required BOTH "process gone" AND
    # "heartbeat stale", so A HUNG SHARD -- live process, frozen heartbeat --
    # could NEVER trigger it. Simulated: `shard3 ok 3000/7222 hb_age=14000s
    # procs=1`, i.e. a shard frozen 3.9 HOURS printing the word "ok". That is
    # verbatim the ship_watch defect this file's own docstring says it exists to
    # prevent, reproduced in the fix for it. (Side lane audit, s31.)
    if (( age > STALE_S )); then
      if (( alive > 0 )); then
        say "*** $SH HUNG (live proc, heartbeat ${age}s stale, $prog) -- killing ***"
        pkill -f "overnight.sh $SH " 2>/dev/null
        sleep 2
        alive=0
      fi
    fi
    if (( alive == 0 && age > STALE_S )); then
      r=${RESTARTS[$SH]:-0}
      if (( r >= MAX_RESTARTS )); then
        say "*** $SH DEAD, restarts exhausted ($r) at $prog -- LEAVING DOWN ***"
        print -r -- "$(date -u +%H:%M:%SZ) $SH dead, restarts exhausted at $prog" >> $ALERT
      else
        RESTARTS[$SH]=$((r+1))
        say "*** $SH dead (age ${age}s, $prog) -- RESTART $((r+1))/$MAX_RESTARTS ***"
        print -r -- "$(date -u +%H:%M:%SZ) $SH restarted ($((r+1))) at $prog" >> $ALERT
        nohup tools/overnight.sh $SH $TR $CT $TG $SL >> $OUT/${SH}.log 2>&1 &
      fi
    else
      say "$SH ok  $prog  hb_age=${age}s  procs=$alive"
    fi
  done < $SPEC
  (( alldone )) && { say "ALL SHARDS COMPLETE"; break; }
  sleep $POLL_S
done
