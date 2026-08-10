#!/bin/zsh
# PANEL-2 CALIBRATION RUNNER — the instrument leg, not a plank leg.
#
# Prereg: docs/prereg/PREREG-panel2-calibration-2026-08-10.md (committed 14:27:30
# CEST, ~35 min before this arm's first match; the arm had fired 0 at the s27 wrap).
#
# WHY THIS IS SEPARATE FROM tools/fanout.sh: fanout rotates arms that ACTIVATE
# experimental submissions, and HANDOVER forbids running that unattended after
# two rollback failures left a non-incumbent live. THIS arm activates NOTHING —
# it plays the live incumbent v104 against a new opponent set — so it carries
# zero rated exposure and zero holder risk. It still ASSERTS the holder before
# every challenge (s27 D28: an arm that activates nothing must still assert what
# is active, or it fires into whatever the previous arm left behind).
# Both branches of that guard are mutation-tested ON THIS FILE, not inherited:
#   docs/legs/LEG-panel3-calibration-2026-08-10.md (abort branch run at
#   15:46:09Z with INCUMBENT=999 -> ABORT, FANOUT_ABORT written, exit 1, zero
#   challenges fired; pass and rate-limit branches exercised live at 15:43-15:44Z).
# The header of this file previously cited PANEL-2's 13:06:51Z run -- a THIRD
# copy of the guard inheriting a citation instead of carrying a test. Side-lane
# flag, and correct: discipline attaches to labels, not function.
#
# ===== THE RATE LIMIT IS 20 MINUTES, MEASURED ON THE CLI 2026-08-10 15:0x =====
#   "Error: Rate limit exceeded: max 5 test/unrated matches per 20 minutes"
# CLAUDE.md and fanout.sh both encode 10 MINUTES (fanout sleeps 620s). Under a
# 20-minute window a 620s cadence fires ~half its challenges and the old fire()
# reports "fired 3/5" and moves on — a SILENT, SYSTEMATIC drop that always lands
# on the TAIL of the id list, i.e. the same cells starve every window.
# Two consequences are built into this runner:
#   1. A rate-limit rejection WAITS FOR THE WINDOW and retries the same cell,
#      rather than burning three 25s retries and abandoning it.
#   2. The starting cell ROTATES each cycle, so any residual drop cannot keep
#      landing on the same cell and biasing the panel it is trying to measure.
cd /Users/junghard/Projects/Work/florent-code-game
# PANEL-3: the REACHABLE band (us-80..us+125), per
# docs/prereg/PREREG-panel3-reachable-band-2026-08-10.md. Ids resolved from
# corpus/league_matches.tsv, each name to exactly one id.
#   SmartFridge +5 · 0033 +111 · Askar City +18 · farming_200s +35
#   Lunds Stallions -30 · The Bisons +32 (re-derives D22's floor verdict)
PANEL2=(7fd91e77-812c-44da-bce7-457be94d2548 74ae65ff-96ae-4da5-a43e-692eb6fee38f b2deaacd-08ad-4c14-b97b-b4f382d82ea3 25288fdb-f3a0-4ae2-964f-2fd7eb9b11d7 eceb8455-7cb3-442b-ba40-c6597c16b446 f670dfed-dfee-421b-8c01-a67b8a278ce3)
MAPS=(--map fjordgate --map jackpot --map atoll --map saga --map snowflake)
# Overridable ONLY so the abort branch can be mutation-tested (set to a version
# that is not live -> the guard must abort without firing). s28 side-lane flag:
# this file is a COPY of fanout.sh's D28 fix, and the mutation test done on the
# original does not cover the copy. Discipline attaches to labels, not function.
INCUMBENT=${INCUMBENT:-104}
OUT=${OUT:-scratchpad/arm_panel3.txt}
CYCLES=${1:-5}
WINDOW=${WINDOW:-1230}          # seconds; 20-min limit + margin
BACKOFF=${BACKOFF:-330}         # seconds to wait after a rate-limit rejection

holder(){ .venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //'; }

for cycle in $(seq 1 $CYCLES); do
  live="$(holder)"
  if [[ "$live" != v${INCUMBENT}* ]]; then
    printf '%s panel3 aborted: holder v%s expected, saw "%s"\n' "$(date -u +%H:%M:%SZ)" "$INCUMBENT" "$live" >> corpus/FANOUT_ABORT
    echo "$(date -u +%H:%M:%SZ) PANEL3: ABORT -- expected v$INCUMBENT, holder is '$live'. Firing nothing."
    exit 1
  fi
  n=0
  # Rotate the starting cell so a dropped challenge cannot keep hitting the
  # same opponent. Cycle k starts at cell (k-1 mod 5).
  for k in $(seq 0 $(( ${#PANEL2} - 1 ))); do
    idx=$(( ((cycle - 1 + k + ${START:-0}) % ${#PANEL2}) + 1 ))
    id=${PANEL2[$idx]}
    for t in 1 2 3 4 5 6; do
      r=$(.venv/bin/fcode match unrated "$id" $MAPS --json 2>&1)
      case "$r" in
        *matchId*)          echo "$id $r" >> $OUT; n=$((n+1)); break;;
        *Rate\ limit*)      echo "$(date -u +%H:%M:%SZ) PANEL3: rate-limited on ${id:0:8}, waiting ${BACKOFF}s (attempt $t)"; sleep $BACKOFF;;
        *)                  echo "$(date -u +%H:%M:%SZ) PANEL3: error on ${id:0:8}: $(echo $r | tail -1)"; sleep 25;;
      esac
    done
  done
  echo "$(date -u +%H:%M:%SZ) PANEL3 cycle $cycle: fired $n/${#PANEL2} (total $(grep -c matchId $OUT))"
  [[ $cycle -lt $CYCLES ]] && sleep $WINDOW
done
echo "$(date -u +%H:%M:%SZ) PANEL3: done, $(grep -c matchId $OUT) challenges banked"
