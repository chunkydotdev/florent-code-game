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
WORK=${1:-scratchpad/corefill_work.txt}
OUT=${OUT:-scratchpad/overnight}
STATE=${STATE:-scratchpad/corefill_started}
NOW=$(date -u +%s)

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
print -r -- "load $(uptime | sed 's/.*averages: *//')   shards $(ps ax -o command= | grep -c '[o]vernight.sh ')   worklist $WORK"
[[ -f scratchpad/COREFILL_STOP ]] && print -r -- "*** PAUSED — scratchpad/COREFILL_STOP present ***"
ps ax -o command= | grep -q '[c]orefill.sh' || print -r -- "*** THE FILLER ITSELF IS NOT RUNNING — nothing new will be launched ***"
print -r -- ""
printf "%-11s %-9s %7s %6s %8s %9s   %s\n" SHARD STATE ROWS PCT HB_AGE ETA RESULT

tot_rows=0
while read -r SH TR CT TG SL; do
  [[ -z ${SH:-} || $SH == \#* ]] && continue
  tsv=$OUT/${SH}.tsv
  rows=0; [[ -f $tsv ]] && rows=$(( $(wc -l < $tsv) - 1 )); (( rows < 0 )) && rows=0
  tot_rows=$(( tot_rows + rows ))
  alive=$(ps ax -o command= | grep -c "[o]vernight.sh $SH ")
  hb=$OUT/${SH}.heartbeat
  age="-"; agesec=999999
  if [[ -f $hb ]]; then agesec=$(( NOW - $(stat -f %m $hb) )); age="${agesec}s"; fi

  if   [[ -f $OUT/${SH}.COMPLETE ]];            then st="DONE"
  elif grep -q cancelled $STATE/$SH 2>/dev/null; then st="CANCELLED"
  elif (( alive > 0 )) && (( agesec > 600 ));   then st="STALLED"      # alive but frozen
  elif (( alive > 0 ));                          then st="running"
  elif [[ -f $STATE/$SH ]];                      then st="DEAD"        # started, no process
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
  if (( rows >= 400 )); then
    res=$(awk -F'\t' -v pool="$LIVE_MAPS" 'BEGIN{
        blind = (pool == "") ? 1 : 0
        split(pool, a, " "); for (i in a) P[a[i]] = 1
      }
      NR>1{n++; if($7=="T") w++; if(!blind && !($4 in P)) ret++} END{
        if(n>0){p=w/n; b=1.96*sqrt(0.25/n)*100;
        printf "%.2f%%  band +-%.2fpp  (n=%d)", p*100, b, n;
        if (blind) printf "  RETIRED:BLIND";
        else if (ret>0) printf "  RETIRED %.0f%%", 100*ret/n}}' $tsv 2>/dev/null)
  elif (( rows > 0 )); then
    res="n=$rows — under 400 rows, NO RATE PRINTED (band would be wider than any effect we chase)"
  fi
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
