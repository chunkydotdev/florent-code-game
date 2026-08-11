#!/bin/zsh
cd /Users/junghard/Projects/Work/florent-code-game
LOG=scratchpad/loki19_treat_w1.log; : > $LOG
log(){ echo "$(date -u +%H:%M:%SZ) $*" >> $LOG; }
holder(){ .venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //'; }
# Wait until just past the derived pairing boundary (:52:59Z), giving ~19 min clear air.
while true; do
  M=$(date -u +%M); S=$(date -u +%S)
  if [ $((10#$M % 20)) -eq 13 ] && [ $((10#$S)) -ge 10 ]; then break; fi
  sleep 5
done
log "boundary passed, starting"
H=$(holder); log "holder before: $H"
case "$H" in v104*) ;; *) log "ABORT: expected v104, saw '$H'"; exit 1;; esac
.venv/bin/fcode submission activate 108 >> $LOG 2>&1
sleep 2
H=$(holder); log "holder after activate: $H"
case "$H" in v108*) ;; *) log "ABORT: activate failed, holder '$H' -- restoring"; .venv/bin/fcode submission activate 104 >> $LOG 2>&1; exit 1;; esac
CELLS=(eceb8455-7cb3-442b-ba40-c6597c16b446 b2deaacd-08ad-4c14-b97b-b4f382d82ea3 7fd91e77-812c-44da-bce7-457be94d2548 25288fdb-f3a0-4ae2-964f-2fd7eb9b11d7 b538e523-2250-4c1d-b718-e73b77ebad55)
n=0
for id in "${CELLS[@]}"; do
  R=$(.venv/bin/fcode match unrated "$id" --json 2>&1 | tr -d '\n')
  echo "$id $R" >> scratchpad/arm_loki19_treat_w1.txt
  case "$R" in *matchId*) n=$((n+1)); log "fired $n/5 vs ${id:0:8}";; *) log "REJECTED ${id:0:8}";; esac
  sleep 2
done
log "TREATMENT WINDOW 1: $n/5 accepted"
.venv/bin/fcode submission activate 104 >> $LOG 2>&1
sleep 2
H=$(holder); log "holder after rollback: $H"
case "$H" in v104*) log "ROLLBACK CONFIRMED";; *) log "*** ROLLBACK NOT CONFIRMED: '$H' -- LADDER RUNNING WRONG BOT ***";; esac
