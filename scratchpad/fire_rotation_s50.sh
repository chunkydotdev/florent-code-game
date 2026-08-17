#!/bin/zsh
# BUILDER s50 fire-order runner — remaining rotation round 1 (research's 17:24Z fire order).
# One unrated 5-game HOLDER leg per ~21-min window (rate limit: 5/20min, shared).
# Cell 1 (Erebus) fired manually 17:27:20Z. This fires cells 2-5.
# Guard per standing rule: gate on the PRESENCE of the 'Active bot:' line == v159,
# never on exit code. If the holder is not v159, SKIP the cell and log — never fire
# a panel cell whose subject has changed.
cd /Users/junghard/Projects/Work/florent-code-game || exit 1
FC=.venv/bin/fcode
LOG=/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/82720aae-f502-4b10-9dd5-ad5f55d16b94/scratchpad/fire_rotation_s50.log
echo "$(date -u +%FT%TZ) runner start pid=$$" >> "$LOG"

typeset -A CELLS
ORDER=(gsxWins TheBisons teamlazy lingling40h)
CELLS[gsxWins]=ebd8d82a-7365-4ccb-af0b-defea3a1ac4d
CELLS[TheBisons]=f670dfed-dfee-421b-8c01-a67b8a278ce3
CELLS[teamlazy]=648d1d5b-5443-4257-a0aa-7048661b612d
CELLS[lingling40h]=86d0b484-783c-47dc-99d9-6ed9af2794f8

# Cell 1 fired at 17:27:20Z. First window opens 20:00 later; fire at +21:00 margin.
NEXT=$(( $(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "2026-08-17T17:27:20Z" +%s) + 1260 ))

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
  # ⛔ -m1 | head -1 IS NOT BELT-AND-BRACES. `fcode match unrated` prints MORE THAN
  # ONE uuid (the team id we passed is echoed alongside the match id), so a bare
  # `grep -o` captured a MULTI-LINE $mid and `$FC match info "$mid"` was handed
  # garbage. Round 2 of this same rotation already carried the fixed pattern
  # (scratchpad/fire_rotation2_s50.sh:32) — this copy is the one that gets
  # copy-pasted next, so the fix lands here too. -m1 stops grep at the first
  # MATCHING LINE; head -1 also handles several uuids on ONE line. Both needed.
  # ⚠ RESIDUAL, stated rather than papered over: this takes the FIRST uuid, so it
  # is right only while the match id is the first one printed. That held for every
  # cell of both rounds (round 1 log 17:48/18:10/18:33/18:55Z, round 2 log — each
  # captured id resolved on `match info`). If `fcode` ever prints the team id
  # first, this captures the WRONG uuid SILENTLY; the `match info` echo below is
  # the check that catches it, so keep it.
  mid=$(echo "$out" | grep -o -m1 '[0-9a-f]\{8\}-[0-9a-f-]\{27\}' | head -1)
  echo "$(date -u +%FT%TZ) FIRED $name match=$mid raw=${out//$'\n'/ | }" >> "$LOG"
  if [[ -n "$mid" ]]; then
    sleep 90
    $FC match info "$mid" 2>&1 | grep -v "Update available" >> "$LOG"
  else
    echo "$(date -u +%FT%TZ) NO-MATCH-ID for $name — leaving cell unfired, will NOT retry (window may be exhausted); operator re-fires" >> "$LOG"
  fi
  NEXT=$(( $(date +%s) + 1260 ))
done
echo "$(date -u +%FT%TZ) runner done — rotation round 1 complete" >> "$LOG"
