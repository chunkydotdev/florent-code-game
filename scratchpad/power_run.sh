#!/bin/zsh
# Continuous window runner. Magnus 2026-08-10: "You are free to use unrated
# games as much as you want, it's a free tool meant to be used."
# Binding constraint is now ONLY the platform: 5 matches / 10 min.
# Goal: LOKI-13 treatment n=25 -> 100, control n=50 -> 100.
cd /Users/junghard/Projects/Work/florent-code-game
PANEL=(f670dfed-dfee-421b-8c01-a67b8a278ce3 bfbb9a68-b37a-4a61-b0ea-d36369c8f65a 26286680-d861-4f9e-9073-a6201bd48d3b ebd8d82a-7365-4ccb-af0b-defea3a1ac4d 74e43df6-bad7-474b-8e37-0ea44a2c80f1)
MAPS=(--map fjordgate --map jackpot --map atoll --map saga --map snowflake)
holder() { .venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //'; }
fire() {  # $1 = output file
  local n=0
  for id in $PANEL; do
    for t in 1 2 3 4; do
      r=$(.venv/bin/fcode match unrated "$id" $MAPS --json 2>&1)
      case "$r" in *matchId*) echo "$id $r" >> $1; n=$((n+1)); break ;; *) sleep 25 ;; esac
    done
  done
  echo "$(date -u +%H:%M:%SZ) fired $n/5 -> $1"
}
gate() {  # wait for 3 consecutive reads with a live active_submission field
  local ok=0
  for i in $(seq 1 60); do
    [[ -n "$(holder)" ]] && ok=$((ok+1)) || ok=0
    [[ $ok -ge 3 ]] && return 0
    sleep 15
  done
  return 1
}
rollback() {
  for t in $(seq 1 200); do
    .venv/bin/fcode submission activate 102 >/dev/null 2>&1; sleep 5
    case "$(holder)" in v102*) echo "$(date -u +%H:%M:%SZ) ROLLBACK VERIFIED"; return 0 ;; esac
  done
  printf '%s ROLLBACK NEVER VERIFIED. Run: .venv/bin/fcode submission activate 102\n' "$(date -u +%H:%M:%SZ)" > corpus/HOLDER_ALERT
  return 1
}
# PLAN: C T T C T  -> control 50+50=100, treatment 25+75=100
for round in C T T C T; do
  if [[ $round == C ]]; then
    echo "=== $(date -u +%H:%M:%SZ) CONTROL window (v102 live, no activation) ==="
    fire scratchpad/control_extra_ids.txt
  else
    echo "=== $(date -u +%H:%M:%SZ) TREATMENT window ==="
    gate || { echo "gate never opened; skipping treatment window, v102 stays live"; sleep 600; continue; }
    .venv/bin/fcode submission activate 104 >/dev/null 2>&1
    fire scratchpad/loki13_extra_ids.txt
    rollback
  fi
  sleep 620
done
echo "=== $(date -u +%H:%M:%SZ) POWER RUN COMPLETE ==="
echo "control extra: $(grep -c matchId scratchpad/control_extra_ids.txt 2>/dev/null || echo 0) matches"
echo "treat   extra: $(grep -c matchId scratchpad/loki13_extra_ids.txt 2>/dev/null || echo 0) matches"
holder
