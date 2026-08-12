#!/bin/zsh
cd /Users/junghard/Projects/Work/florent-code-game
OUT=scratchpad/loki13_ids.txt; : > $OUT
ALERT=corpus/HOLDER_ALERT
holder() { .venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //'; }
# GATE: the load-bearing field is active_submission. `fcode status` prints the
# "Active bot:" line ONLY when it is non-null, so grepping that line IS the
# predicate -- not exit code (status exits 0 while printing "Error: True" to
# stdout) and not JSON parseability (a degraded body parses fine with
# active_submission=None). Verified empirically during the 07:14 outage.
ok=0
for i in $(seq 1 120); do
  v=$(holder)
  if [ -n "$v" ]; then ok=$((ok+1)); else ok=0; fi
  [ "$ok" -ge 3 ] && { echo "$(date -u +%H:%M:%SZ) GATE OPEN after 3 consecutive holder reads: $v"; break; }
  sleep 20
done
if [ "$ok" -lt 3 ]; then echo "$(date -u +%H:%M:%SZ) PLATFORM NEVER STABILISED -- NOT ACTIVATING. v102 remains live."; exit 0; fi
echo "$(date -u +%H:%M:%SZ) activate v104"
.venv/bin/fcode submission activate 104 >/dev/null 2>&1
echo "  holder now: $(holder)"
for id in f670dfed-dfee-421b-8c01-a67b8a278ce3 bfbb9a68-b37a-4a61-b0ea-d36369c8f65a 26286680-d861-4f9e-9073-a6201bd48d3b ebd8d82a-7365-4ccb-af0b-defea3a1ac4d 74e43df6-bad7-474b-8e37-0ea44a2c80f1; do
  for t in 1 2 3; do
    r=$(.venv/bin/fcode match unrated "$id" --map fjordgate --map jackpot --map atoll --map saga --map snowflake --json 2>&1)
    case "$r" in *matchId*) echo "$id $r" >> $OUT; break ;; *) sleep 20 ;; esac
  done
done
echo "$(date -u +%H:%M:%SZ) rollback begins ($(grep -c matchId $OUT) challenges accepted)"
# PERSISTENT: ~20 minutes of retries. If the holder field goes null AFTER we
# activated, this is the branch where "v102 stays live" would otherwise stop
# being true -- so it does NOT give up quietly, it raises a file.
for t in $(seq 1 200); do
  .venv/bin/fcode submission activate 102 >/dev/null 2>&1
  sleep 5
  v=$(holder)
  case "$v" in
    v102*) echo "$(date -u +%H:%M:%SZ) ROLLBACK VERIFIED: $v"; rm -f $ALERT; exit 0 ;;
    "")    [ $((t % 12)) -eq 0 ] && echo "$(date -u +%H:%M:%SZ) t=$t holder UNREADABLE, still retrying" ;;
    *)     echo "$(date -u +%H:%M:%SZ) t=$t holder=$v NOT v102, retrying" ;;
  esac
done
printf '%s ROLLBACK NEVER VERIFIED after 200 attempts. Holder unknown; v104 may be live.\nRun: .venv/bin/fcode submission activate 102 && .venv/bin/fcode status\n' "$(date -u +%H:%M:%SZ)" > $ALERT
echo "RAISED $ALERT"
