#!/bin/zsh
# BUILDER s50 fire-order runner ROUND 2 — research's baseline-cells order (tail, ~18:40Z):
# farming_200s -> not adgato -> The Bisons -> gsxWins. Erebus dropped (self-refreshing cell).
# Purpose: pre-treatment BASELINE cells for the ferry-siege leg shortlist, same fixture/era.
# Starts after round-1 cell 5 (lingling ~18:54Z): first fire 19:16Z, then 21-min cadence.
# Holder guard identical to round 1: fire ONLY on a healthy "Active bot: v159" line.
# New script (not a fix of the round-1 runner): match-id capture takes FIRST UUID only.
cd /Users/junghard/Projects/Work/florent-code-game || exit 1
FC=.venv/bin/fcode
LOG=/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/82720aae-f502-4b10-9dd5-ad5f55d16b94/scratchpad/fire_rotation2_s50.log
echo "$(date -u +%FT%TZ) round-2 runner start pid=$$" >> "$LOG"

typeset -A CELLS
ORDER=(farming200s notadgato TheBisons gsxWins)
CELLS[farming200s]=25288fdb-f3a0-4ae2-964f-2fd7eb9b11d7
CELLS[notadgato]=fb0e7053-f8f3-4cc8-a38f-1856a518c7d2
CELLS[TheBisons]=f670dfed-dfee-421b-8c01-a67b8a278ce3
CELLS[gsxWins]=ebd8d82a-7365-4ccb-af0b-defea3a1ac4d

NEXT=$(( $(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "2026-08-17T19:16:00Z" +%s) ))

for name in $ORDER; do
  now=$(date +%s)
  if (( NEXT > now )); then sleep $(( NEXT - now )); fi
  holder=$($FC status 2>/dev/null | grep "Active bot:")
  if [[ "$holder" != *"v159"* ]]; then
    echo "$(date -u +%FT%TZ) SKIP $name — holder line is '$holder' (need v159 present)" >> "$LOG"
    NEXT=$(( $(date +%s) + 1260 ))
    continue
  fi
  out=$($FC match unrated "${CELLS[$name]}" 2>&1 | grep -v "Update available")
  mid=$(echo "$out" | grep -o -m1 '[0-9a-f]\{8\}-[0-9a-f-]\{27\}' | head -1)
  echo "$(date -u +%FT%TZ) FIRED $name match=$mid raw=${out//$'\n'/ | }" >> "$LOG"
  if [[ -n "$mid" ]]; then
    sleep 90
    $FC match info "$mid" 2>&1 | grep -v "Update available" >> "$LOG"
  else
    echo "$(date -u +%FT%TZ) NO-MATCH-ID for $name — cell left unfired, NO retry; operator re-fires" >> "$LOG"
  fi
  NEXT=$(( $(date +%s) + 1260 ))
done
echo "$(date -u +%FT%TZ) round-2 runner done" >> "$LOG"
