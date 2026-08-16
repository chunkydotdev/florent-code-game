#!/usr/bin/env zsh
# COREFILL STATUS — one command: what is running, what is queued, what it says.
#
#   tools/corefill_status.sh [worklist]
#
# ⛔ THREE THINGS THIS REPORTS THAT A NAIVE STATUS SCRIPT WOULD NOT, EACH ONE A
# DEFECT THIS PROJECT HAS SHIPPED:
#
# 1. **THE AGE OF EVERY NUMBER IT PRINTS.** `ship_watch` once printed
#    `rating=1599 armed=True RULE=held` off rows seven minutes stale, and a
#    HEALTHY line and a BLIND line were byte-identical. Every row here carries
#    its heartbeat age; a shard whose file has not moved is called STALLED, not
#    silently included in a total.
# 2. **RUNNING vs STARTED-BUT-DEAD ARE DIFFERENT STATES.** A shard with rows and
#    no process is DEAD, not "in progress". `corefill` deliberately never
#    relaunches, so a dead shard stays dead until a human looks -- which only
#    works if the status tool SAYS SO instead of showing a stalled percentage.
# 3. **IT REFUSES TO PRINT A WIN RATE UNDER ~400 ROWS.** At n=200 the 95% band
#    is about +-7pp; a number printed there reads as a result and is noise. The
#    band is printed beside every rate so nobody has to remember this.
set -u
source "$(dirname "$0")/lib/runner_pat.sh"
WORK=${1:-scratchpad/corefill_work.txt}
OUT=${OUT:-scratchpad/overnight}
STATE=${STATE:-scratchpad/corefill_started}
NOW=$(date -u +%s)
# ONE ps snapshot for the whole run. 113 worklist lines × a fresh `ps ax`
# each was ~73s wall under game load and blew the dashboard's 120s capture
# budget (side-lane measurement, 2026-08-14) — the status authority got
# slower the busier the box. The snapshot is also the freshness contract:
# every liveness answer below is as-of $NOW, stated once.
PSSNAP=$(ps ax -o command= 2>/dev/null)

# 4. **A RATE ON RETIRED GEOMETRY SAYS SO ON THE SAME LINE.** The 2026-08-13
#    map rotation retired 4 of the old 8 battery maps; a shard launched before
#    it keeps its startup array, so its rate silently spans dead maps (audit
#    M4: 165,832 rows, 49.99%, with no consumer-path caveat). The live pool is
#    parsed from tools/overnight.sh's own MAPS= line — ONE source, never a
#    second copy. If the parse fails we print RETIRED:BLIND rather than
#    nothing: an alarm that cannot tell it is blind is this repo's
#    most-repeated defect.
POOL_SRC=${POOL_SRC:-tools/overnight.sh}
LIVE_MAPS=$(sed -n 's/^MAPS=(\(.*\))$/\1/p' $POOL_SRC 2>/dev/null)
[[ -z $LIVE_MAPS ]] && print -r -- "*** LIVE POOL UNPARSEABLE from $POOL_SRC — every RETIRED%% below is BLIND ***"

print -r -- "COREFILL STATUS  $(date -u +%Y-%m-%dT%H:%M:%SZ)"
print -r -- "load $(uptime | sed 's/.*averages: *//')   shards $(print -r -- "$PSSNAP" | grep -c "$RUNNER_PAT ")   worklist $WORK"
[[ -f scratchpad/COREFILL_STOP ]] && print -r -- "*** PAUSED — scratchpad/COREFILL_STOP present ***"
print -r -- "$PSSNAP" | grep -q '[c]orefill.sh' || print -r -- "*** THE FILLER ITSELF IS NOT RUNNING — nothing new will be launched ***"
print -r -- ""
printf "%-11s %-9s %7s %6s %8s %9s   %s\n" SHARD STATE ROWS PCT HB_AGE ETA RESULT

tot_rows=0
while read -r SH TR CT TG SL; do
  [[ -z ${SH:-} || $SH == \#* ]] && continue
  tsv=$OUT/${SH}.tsv
  rows=0; [[ -f $tsv ]] && rows=$(( $(wc -l < $tsv) - 1 )); (( rows < 0 )) && rows=0
  tot_rows=$(( tot_rows + rows ))
  # `grep -c` EXITS 1 ON ZERO MATCHES — it fails exactly when the answer
  # is CLEAN. Harmless today (no `set -e` here), fatal the moment anyone
  # adds one: measured, `set -e; n=$(grep -c zzz f)` ABORTS the script
  # while `echo "$(grep -c zzz f)"` does not. `|| true` keeps the count
  # (grep still prints 0) and drops the status. TEST ON THE COUNT, NEVER $?.
  alive=$(print -r -- "$PSSNAP" | grep -c "$RUNNER_PAT $SH " || true)
  hb=$OUT/${SH}.heartbeat
  age="-"; agesec=999999
  if [[ -f $hb ]]; then agesec=$(( NOW - $(stat -f %m $hb) )); age="${agesec}s"; fi

  if   [[ -f $OUT/${SH}.COMPLETE ]];            then st="DONE"
  elif grep -q cancelled $STATE/$SH 2>/dev/null; then st="CANCELLED"
  elif (( alive > 0 )) && (( agesec > 600 ));   then st="STALLED"      # alive but frozen
  elif (( alive > 0 ));                          then st="running"
  elif [[ -f $STATE/$SH ]] && (( agesec < 600 )); then st="running?"   # no matching process but heartbeat FRESH — an unmatched runner, not a corpse
  elif rtsv=(scratchpad/overnight-remote/*/${SH}.tsv(N)) && (( ${#rtsv} > 0 )); then
    # the shard runs on a FLEET box: rows/age come from the freshest pulled
    # copy — without this clause a remote shard reads DEAD locally (caught
    # the day the first box went live, before the dashboard could lie).
    st="remote"; tsv=${rtsv[1]}
    rows=$(( $(wc -l < $tsv) - 1 )); (( rows < 0 )) && rows=0
    agesec=$(( NOW - $(stat -f %m $tsv) )); age="${agesec}s(pull)"
    # State comes from the MIRRORED HEARTBEAT's 5th field, never from a mirror
    # .COMPLETE: the pull does not delete, so a marker removed upstream (the
    # A5-extension reset-done case) persists here — a presence-marker over a
    # non-deleting mirror is unreliable by construction (side lane, s41). The
    # heartbeat is rewritten every cycle and cannot go stale that way.
    rhb=${tsv:r}.heartbeat
    if [[ -f $rhb ]]; then
      hbstate=$(awk -F'\t' '{print $5}' "$rhb" 2>/dev/null)
      [[ $hbstate == COMPLETE ]] && st="DONE"
    fi
  elif [[ -f $STATE/$SH ]];                      then st="DEAD"        # started, no process, heartbeat stale
  else                                                st="queued"
  fi

  pct="-"; eta="-"
  if (( rows > 0 )); then
    pct="$(( rows * 100 / TG ))%"
    if [[ $st == running && -f $STATE/$SH ]]; then
      t0=$(stat -f %m $STATE/$SH); el=$(( NOW - t0 ))
      if (( el > 60 && rows > 20 )); then
        rate=$(( rows * 60 / el ))                      # games/min
        (( rate > 0 )) && eta="$(( (TG - rows) / rate ))m"
      fi
    fi
  fi

  res=""
  # DONE shards never change: their awk result is cached keyed on the TSV's
  # mtime (72 of 113 lines were finished shards re-awked every 45s capture).
  cachef=$OUT/${SH}.result_cache
  if [[ $st == DONE && -f $cachef && $cachef -nt $tsv ]]; then
    res=$(cat $cachef)
  elif (( rows >= 400 )); then
    res=$(awk -F'\t' -v pool="$LIVE_MAPS" 'BEGIN{
        blind = (pool == "") ? 1 : 0
        split(pool, a, " "); for (i in a) P[a[i]] = 1
      }
      NR>1{n++; if($7=="T") w++; if(!blind && !($4 in P)) ret++} END{
        if(n>0){p=w/n; b=1.96*sqrt(0.25/n)*100;
        printf "%.2f%%  band +-%.2fpp  (n=%d)", p*100, b, n;
        if (blind) printf "  RETIRED:BLIND";
        else if (ret>0) printf "  RETIRED %.0f%%", 100*ret/n}}' $tsv 2>/dev/null)
    [[ $st == DONE && -n $res ]] && print -r -- "$res" > $cachef
  elif (( rows > 0 )); then
    res="n=$rows — under 400 rows, NO RATE PRINTED (band would be wider than any effect we chase)"
  fi
  [[ $st == remote ]] && res="@${${tsv:h:t}##*@} · $res"   # visible host tag; the durable tags are the path + the seed offset
  printf "%-11s %-9s %7d %6s %8s %9s   %s\n" "$SH" "$st" "$rows" "$pct" "$age" "$eta" "$res"
done < $WORK

print -r -- ""
print -r -- "total rows this programme: $tot_rows"
print -r -- ""
print -r -- "ADD     : append a line to $WORK (picked up within one poll)"
print -r -- "CANCEL  : touch scratchpad/corefill_cancel/<SHARD>   (kills it; rows are KEPT)"
print -r -- "PAUSE   : touch scratchpad/COREFILL_STOP             (delete to resume)"
print -r -- "FULL    : .venv/bin/python tools/overnight_read.py --dir $OUT"
print -r -- "          ^ pools partial shards, prints the shortfall, and applies the"
print -r -- "            informative band + the NULL/NEG calibration cells."
