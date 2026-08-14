#!/bin/zsh
# EVICT58 live leg — submit-hold fire script (prereg 9168ac15).
# Usage: zsh scratchpad/fire_evict58_leg.sh <PIN_MATCH_ID>
# Sequence: verify holder v140 -> submit_clean --leg (prototype live, held on
# sentinel, 300s failsafe restore) -> 5 pinned challenges (retry on rate-limit
# once each) -> sentinel -> verify v140 restored. Aborts loudly at every step.
set -e
cd /Users/junghard/Projects/Work/florent-code-game
PIN=$1
[[ -n $PIN ]] || { echo "ABORT: no pin match id"; exit 2 }
T0033=74ae65ff-96ae-4da5-a43e-692eb6fee38f
live=$(.venv/bin/fcode status 2>/dev/null | grep "Active bot:")
echo "$live" | grep -q "v140" || { echo "ABORT: holder not v140: $live"; exit 1 }
# PRE-FLIGHT (research's ask after the 16:42/43 unattributed fires): count
# unrated accepts in the rolling 20-min window BEFORE the submit — if ANY
# slot is spent, abort with the prototype never having gone live.
recent=$(.venv/bin/fcode match list --mine --type unrated --json --limit 12 2>/dev/null | .venv/bin/python -c "
import json,sys,datetime
now = datetime.datetime.now(datetime.timezone.utc)
n = 0
d = json.load(sys.stdin)
rows = d.get('matches', []) if isinstance(d, dict) else d
for m in rows:
    if not isinstance(m, dict): continue
    ts = m.get('createdAt','')
    try:
        t = datetime.datetime.fromisoformat(ts.replace('Z','+00:00'))
        if (now - t).total_seconds() < 1200: n += 1
    except Exception: pass
print(n)")
[[ "$recent" == "0" ]] || { echo "ABORT PRE-FLIGHT: $recent unrated accepts inside the rolling window — budget not clean, prototype NOT submitted"; exit 3 }
echo "[$(date -u +%H:%M:%SZ)] pre-flight clean (0 accepts in window)"
rm -f scratchpad/LEG_FIRES_DONE
echo "[$(date -u +%H:%M:%SZ)] submitting EVICT58 (leg-hold)"
.venv/bin/python tools/submit_clean.py bots/_v233evict58 --name 'Loki rc9.1' --leg > scratchpad/leg_evict58_submit.log 2>&1 &
SUBPID=$!
sleep 12
newlive=$(.venv/bin/fcode status 2>/dev/null | grep "Active bot:")
echo "$newlive" | grep -q "rc9.1\|Loki rc9" || { echo "WARN: active line reads: $newlive (continuing — name may render differently)"; }
acc=0
for i in 1 2 3 4 5; do
  r=$(.venv/bin/fcode match unrated "$T0033" --match "$PIN" --json 2>&1)
  if echo "$r" | grep -q "matchId"; then
    acc=$((acc+1)); echo "[$(date -u +%H:%M:%SZ)] accept $acc/5"
  elif echo "$r" | grep -q "Rate limit"; then
    echo "[$(date -u +%H:%M:%SZ)] rate-limited at $acc — waiting 65s once"; sleep 65
    r=$(.venv/bin/fcode match unrated "$T0033" --match "$PIN" --json 2>&1)
    echo "$r" | grep -q "matchId" && { acc=$((acc+1)); echo "accept $acc/5 (retry)"; } || echo "retry failed: $(echo "$r" | head -c 120)"
  else
    echo "fire $i error: $(echo "$r" | head -c 160)"
  fi
  sleep 3
done
echo "[$(date -u +%H:%M:%SZ)] $acc accepts — releasing hold"
touch scratchpad/LEG_FIRES_DONE
wait $SUBPID 2>/dev/null || true
sleep 3
fin=$(.venv/bin/fcode status 2>/dev/null | grep "Active bot:")
echo "$fin" | grep -q "v140" && echo "[$(date -u +%H:%M:%SZ)] HOLDER RESTORED: $fin" || { echo "⛔ HOLDER NOT RESTORED: $fin — manual: .venv/bin/fcode submission activate 140"; exit 1 }
