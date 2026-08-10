#!/bin/zsh
# PANEL-2 CALIBRATION RUNNER — the instrument leg, not a plank leg.
#
# Prereg: docs/prereg/PREREG-panel2-calibration-2026-08-10.md (committed before
# this arm fired its first match; the arm had fired 0 at the s27 wrap).
#
# WHY THIS IS SEPARATE FROM tools/fanout.sh: fanout rotates arms that ACTIVATE
# experimental submissions, and HANDOVER forbids running that unattended after
# two rollback failures left a non-incumbent live. THIS arm activates NOTHING —
# it plays the live incumbent v104 against a new opponent set — so it carries
# zero rated exposure and zero holder risk. It still ASSERTS the holder before
# every challenge (s27 D28: an arm that activates nothing must still assert what
# is active, or it fires into whatever the previous arm left behind).
cd /Users/junghard/Projects/Work/florent-code-game
PANEL2=(f61d19c1-600e-457b-861b-dbeb6b3d8691 48340ad8-701f-4a40-850d-1f3f3d56d8ca 0774b1b2-df40-4cf2-915e-5d5a6133a13a bfbb9a68-b37a-4a61-b0ea-d36369c8f65a ebd8d82a-7365-4ccb-af0b-defea3a1ac4d)
MAPS=(--map fjordgate --map jackpot --map atoll --map saga --map snowflake)
INCUMBENT=104
OUT=scratchpad/arm_panel2.txt
CYCLES=${1:-5}

holder(){ .venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //'; }

for cycle in $(seq 1 $CYCLES); do
  live="$(holder)"
  if [[ "$live" != v${INCUMBENT}* ]]; then
    printf '%s panel2 aborted: holder v%s expected, saw "%s"\n' "$(date -u +%H:%M:%SZ)" "$INCUMBENT" "$live" >> corpus/FANOUT_ABORT
    echo "$(date -u +%H:%M:%SZ) PANEL2: ABORT -- expected v$INCUMBENT, holder is '$live'. Firing nothing."
    exit 1
  fi
  n=0
  for id in $PANEL2; do for t in 1 2 3; do
    r=$(.venv/bin/fcode match unrated "$id" $MAPS --json 2>&1)
    case "$r" in *matchId*) echo "$id $r" >> $OUT; n=$((n+1)); break;; *) sleep 25;; esac
  done; done
  echo "$(date -u +%H:%M:%SZ) PANEL2 cycle $cycle: fired $n/5 (total $(grep -c matchId $OUT))"
  [[ $cycle -lt $CYCLES ]] && sleep 620
done
echo "$(date -u +%H:%M:%SZ) PANEL2: done, $(grep -c matchId $OUT) challenges banked"
