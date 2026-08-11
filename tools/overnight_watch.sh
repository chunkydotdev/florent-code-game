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
set -u
SPEC=${1:?spec file}
OUT=scratchpad/overnight
ALERT=$OUT/ALERT
STALE_S=${STALE_S:-240}      # heartbeat older than this = dead
MAX_RESTARTS=${MAX_RESTARTS:-3}
POLL_S=${POLL_S:-120}
mkdir -p $OUT
typeset -A RESTARTS

say(){ print -r -- "$(date -u +%H:%M:%SZ) $*" | tee -a $OUT/watch.log }

say "WATCHDOG up. spec=$SPEC stale=${STALE_S}s poll=${POLL_S}s max_restarts=$MAX_RESTARTS"

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
    alive=$(ps ax -o command= | grep -c "[o]vernight.sh $SH ")
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
