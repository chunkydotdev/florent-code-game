#!/bin/zsh
# TRI-ARM executor — PREREG-triarm-live-2026-08-13.md. One invocation per arm:
#   zsh scratchpad/triarm_leg.sh A            # control: active bot, no submit
#   zsh scratchpad/triarm_leg.sh B            # UNDERECO via --leg hold
#   zsh scratchpad/triarm_leg.sh C            # TWORAID via --leg hold
# Fires 5 matches (one per opponent) with the pinned 5-map list.
cd /Users/junghard/Projects/Work/florent-code-game || exit 2
set -u
ARM=${1:?A|B|C}
OPPS=(
  648d1d5b-5443-4257-a0aa-7048661b612d  # O1 team lazy
  26286680-d861-4f9e-9073-a6201bd48d3b  # O2 Leviathan
  86d0b484-783c-47dc-99d9-6ed9af2794f8  # O3 LingLing40
  32087804-2dde-4265-acb2-b6ec9039fbee  # O4 Juusto
  ea0d33c8-ca2b-497a-9be0-1837379eab1e  # O5 Coreflood
)
MAPS=(--map midgard --map drakkarfjord --map drumlin --map frostgate --map fjordgate)
LOG=scratchpad/triarm_fires.tsv

case $ARM in
  A) TREE=""; NAME="";;
  B) TREE=bots/_v201undereco; NAME="Loki rc8.1";;
  C) TREE=bots/_v203tworaid;  NAME="Loki rc8.2";;
  *) echo "bad arm"; exit 2;;
esac

fire_five() {
  local n=0
  for id in $OPPS; do
    r=$(.venv/bin/fcode match unrated "$id" $MAPS --json 2>&1)
    case "$r" in
      *matchId*) v=ACCEPT; n=$((n+1));;
      *"Rate limit"*) v=RATELIMIT;;
      *) v=ERROR;;
    esac
    printf '%s\tARM-%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$ARM" "$id" "$v" \
      "$(echo "$r" | tr '\n' ' ' | head -c 200)" >> $LOG
    [[ $v == RATELIMIT ]] && { echo "RATELIMIT at fire $((n+1)) — aborting burst (do NOT hold a prototype through a window)"; return 1; }
  done
  echo "$(date -u +%H:%M:%SZ) ARM-$ARM: $n/5 accepted"
  return 0
}

if [[ $ARM == A ]]; then
  live=$(.venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //')
  [[ "$live" == v125* ]] || { echo "control arm expects v125 live, saw '$live' — NOT firing"; exit 1; }
  fire_five; exit $?
fi

# B/C: prototype via --leg hold
HOLDER_PRE=$(.venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //')
[[ -z "$HOLDER_PRE" ]] && { echo "cannot read holder — NOT submitting"; exit 1; }
restore_if_displaced() {
  live=$(.venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //')
  if [[ "$live" != "$HOLDER_PRE" ]]; then
    ver=$(echo "$HOLDER_PRE" | grep -o '[0-9]\+' | head -1)
    echo "DEAD-PROCESS RESTORE: activating v$ver"
    .venv/bin/fcode submission activate "$ver"
    .venv/bin/fcode status 2>/dev/null | grep "Active bot"
  fi
}
rm -f scratchpad/LEG_FIRES_DONE
.venv/bin/python tools/submit_clean.py "$TREE" --name "$NAME" --leg \
    > scratchpad/triarm_submit_$ARM.log 2>&1 &
SUBMIT_PID=$!
for i in $(seq 1 45); do
  grep -q "LEG MODE: .* IS LIVE" scratchpad/triarm_submit_$ARM.log && break
  kill -0 $SUBMIT_PID 2>/dev/null || { echo "SUBMIT DIED pre-LIVE"; restore_if_displaced; exit 1; }
  sleep 2
done
grep -q "LEG MODE: .* IS LIVE" scratchpad/triarm_submit_$ARM.log || { echo "NO LIVE LINE in 90s"; touch scratchpad/LEG_FIRES_DONE; sleep 8; restore_if_displaced; exit 1; }
echo "$(date -u +%H:%M:%SZ) ARM-$ARM prototype LIVE — firing"
fire_five
touch scratchpad/LEG_FIRES_DONE
wait $SUBMIT_PID
tail -4 scratchpad/triarm_submit_$ARM.log
.venv/bin/fcode status 2>/dev/null | grep "Active bot"
