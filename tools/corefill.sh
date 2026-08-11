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
# READ IT WITH:  tools/corefill_read.sh   (or overnight_read.py --dir <OUT>)
set -u
WORK=${1:?worklist file}
MAX_SHARDS=${2:-8}
DEADLINE_H=${3:-8}
OUT=${OUT:-scratchpad/overnight}
POLL_S=${POLL_S:-60}
LOAD_CEIL=${LOAD_CEIL:-11.0}
LOG=${LOG:-scratchpad/corefill.log}
STATE=${STATE:-scratchpad/corefill_started}

mkdir -p $OUT $STATE
DEADLINE=$(( $(date +%s) + DEADLINE_H * 3600 ))

say(){ print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a $LOG }

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

  # ---- guard 2: blind is not idle -----------------------------------------
  running=$(ps ax -o command= 2>/dev/null | grep -c "[o]vernight.sh ")
  if [[ -z $running ]]; then
    say "BLIND: cannot read process table -- refusing to launch this cycle"
    sleep $POLL_S; continue
  fi

  # ---- guard 3: load ceiling ----------------------------------------------
  load1=$(uptime | sed 's/.*averages: *//' | awk '{print $1}' | tr -d ',')
  over=$(awk -v a="$load1" -v b="$LOAD_CEIL" 'BEGIN{print (a>b)?1:0}')

  launched=0
  if (( running < MAX_SHARDS )) && (( over == 0 )); then
    while read -r SH TR CT TG SL; do
      [[ -z ${SH:-} || $SH == \#* ]] && continue
      # ---- guard 1: at most once, marker written BEFORE the launch ---------
      [[ -f $STATE/$SH ]] && continue
      print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > $STATE/$SH
      say "LAUNCH $SH  $TR vs $CT  target=$TG seed_lo=$SL   (running was $running, load $load1)"
      nohup zsh tools/overnight.sh $SH $TR $CT $TG $SL >> $OUT/${SH}.launch.log 2>&1 &
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
