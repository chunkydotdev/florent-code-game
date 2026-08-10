#!/bin/zsh
# LOKI-14b LEG RUNNER — carrier-targeted border-throw crash induction.
#
# Prereg: docs/prereg/PREREG-loki14b-carrier-targeted-2026-08-10.md
#   body      ce12795  2026-08-10T15:29:57+02:00   (the bars)
#   amend 1   6463741  2026-08-10T15:38:30+02:00   (carrier admission rule)
#
#   .venv/bin/zsh tools/loki14b_leg.sh <cycles> <carrier_id> [carrier_id ...]
#
# CARRIERS ARE PASSED IN, NEVER HARDCODED. Amendment 1 admits them by a
# pre-committed per-carrier threshold, and fewer than TWO admitted means the leg
# does not fire -- so the admitted set is an INPUT decided by that rule, and this
# script refuses to run with fewer than two.
#
# ===== HOW THIS DIFFERS FROM tools/panel2_cal.sh, AND WHY =====
# panel2_cal.sh activates NOTHING (it calibrates the live incumbent), so when it
# is rate-limited it can afford to WAIT 330s and retry the same cell.
#
# THIS LEG RUNS A PROTOTYPE LIVE. Every second v107 holds the slot is rated
# exposure and a scouting window for anyone sampling our submission, so the
# prereg says "activate only in the instant before firing". Therefore:
#
#   ** ON A RATE-LIMIT REJECTION THIS RUNNER DOES NOT WAIT. IT ROLLS BACK
#      IMMEDIATELY, SLEEPS OUT THE WINDOW WITH THE INCUMBENT LIVE, AND
#      RE-ACTIVATES FOR THE NEXT WINDOW. **
#
# The cost of that choice is dropped challenges, and a drop that always lands on
# the same cell biases the panel (s28: panel2's cycle 1 starved exactly the two
# retained controls). So the drop is made UNBIASED the way fanout.sh now does it:
# DEFICIT-FIRST ORDERING off the arm's own outfile -- fewest banked fires first.
#
# ===== HOLDER DISCIPLINE (s27 D26 + D28) =====
# * Assert the holder BEFORE every challenge. An arm that fires into the wrong
#   bot contaminates a denominator silently -- that already cost us 10 games.
# * Gate on the "Active bot:" FIELD, never on the exit code. `fcode status`
#   exits 0 while printing `Error: True` with a null active_submission.
# * A rollback that cannot be VERIFIED writes corpus/HOLDER_ALERT and stops.
cd /Users/junghard/Projects/Work/florent-code-game
MAPS=(--map fjordgate --map jackpot --map atoll --map saga --map snowflake)
TREAT=${TREAT:-107}             # v107 = bots/_v131loki14, byte-identical to LOKI-14
INCUMBENT=${INCUMBENT:-104}
OUT=${OUT:-scratchpad/arm_loki14b.txt}
WINDOW=${WINDOW:-1230}          # 20-minute rate-limit window + margin

CYCLES=${1:-5}; shift
CARRIERS=("$@")

if (( ${#CARRIERS} < 2 )); then
  echo "REFUSING TO FIRE: ${#CARRIERS} carrier(s) given, Amendment 1 requires >= 2."
  echo "A one-cell fixture cannot support this leg's conclusion. Re-register instead."
  exit 2
fi

holder(){ .venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //'; }

assert_holder(){   # $1 = expected version int
  local live="$(holder)"
  if [[ "$live" != v${1}* ]]; then
    printf '%s loki14b: expected v%s, holder is "%s"\n' "$(date -u +%H:%M:%SZ)" "$1" "$live" >> corpus/FANOUT_ABORT
    echo "$(date -u +%H:%M:%SZ) ABORT -- expected v$1, holder is '$live'. Firing nothing."
    return 1
  fi
  return 0
}

rollback(){
  for t in $(seq 1 60); do
    .venv/bin/fcode submission activate $INCUMBENT >/dev/null 2>&1
    sleep 4
    case "$(holder)" in v${INCUMBENT}*) echo "$(date -u +%H:%M:%SZ) rolled back to v$INCUMBENT, VERIFIED"; return 0;; esac
  done
  printf '%s ROLLBACK TO v%s NEVER VERIFIED\n' "$(date -u +%H:%M:%SZ)" "$INCUMBENT" > corpus/HOLDER_ALERT
  echo "$(date -u +%H:%M:%SZ) ** ROLLBACK UNVERIFIED -- corpus/HOLDER_ALERT written **"
  return 1
}

for cycle in $(seq 1 $CYCLES); do
  # Deficit-first: fewest banked challenges fires first, so a rate-limit drop
  # cannot keep landing on the same carrier.
  ids=(${CARRIERS})
  if [[ -s "$OUT" ]]; then
    ids=(${(f)"$(for id in $ids; do printf '%s %s\n' "$(grep -c "^$id " $OUT)" "$id"; done | sort -n | cut -d' ' -f2)"})
  fi

  .venv/bin/fcode submission activate $TREAT >/dev/null 2>&1
  sleep 4
  if ! assert_holder $TREAT; then rollback; exit 1; fi
  echo "$(date -u +%H:%M:%SZ) cycle $cycle: v$TREAT LIVE, firing ${#ids} carriers"

  n=0
  for id in $ids; do
    assert_holder $TREAT || break          # holder must hold for EVERY challenge
    r=$(.venv/bin/fcode match unrated "$id" $MAPS --json 2>&1)
    case "$r" in
      *matchId*)     echo "$id $r" >> $OUT; n=$((n+1));;
      *Rate\ limit*) echo "$(date -u +%H:%M:%SZ) rate-limited on ${id:0:8} -- NOT waiting with v$TREAT live; deferring to next window"; break;;
      *)             echo "$(date -u +%H:%M:%SZ) error on ${id:0:8}: $(echo $r | tail -1)";;
    esac
  done

  rollback || exit 1
  echo "$(date -u +%H:%M:%SZ) cycle $cycle: fired $n/${#ids} (total $(grep -c matchId $OUT 2>/dev/null || echo 0))"
  # BUDGET-DRIVEN PACING (s28). A flat $WINDOW sleep left ~40% of the rolling
  # 20-minute allowance idle -- measured on panel3 before the same fix. The
  # rollback above has already run, so this waits with the INCUMBENT live.
  if [[ $cycle -lt $CYCLES ]]; then
    w=$(.venv/bin/python tools/rate_budget.py --wait 2>/dev/null || echo $WINDOW)
    [[ "$w" =~ ^[0-9]+$ ]] || w=$WINDOW
    # ⚠ THE METER LAGS THE PLATFORM. Challenges we just fired take time to
    # appear in `match list`, so rate_budget -- which reads that list -- can
    # report "a slot is free NOW" seconds after we spent four. Observed at
    # 20:15:04Z: meter said 20s, the next cycle activated v106, was rejected,
    # and rolled back. That is a pointless activation and pointless prototype
    # exposure, caused by trusting a lower bound as if it were exact.
    # If we fired anything this cycle, floor the wait at one slot-interval per
    # challenge (20 min / 5 slots = 240s each), capped at a full window.
    # A RATE-LIMIT REJECTION IS HARD EVIDENCE THE METER IS WRONG, and rejected
    # attempts THEMSELVES count against the limit -- so spinning on a stale
    # "free now" actively spends the budget it is waiting for, and pays a
    # pointless prototype activation each time round. If we fired fewer than we
    # asked for, the budget is provably gone: wait a real interval.
    local floor=0
    if (( n > 0 )); then floor=$(( 240 * n )); fi
    if (( n < ${#ids} )); then (( floor < 330 )) && floor=330; fi
    (( floor > WINDOW )) && floor=$WINDOW
    (( w < floor )) && w=$floor
    (( w < 20 )) && w=20
    echo "$(date -u +%H:%M:%SZ) meter says wait ${w}s (incumbent live)"
    sleep $w
  fi
done
echo "$(date -u +%H:%M:%SZ) LOKI-14b: done, $(grep -c matchId $OUT) challenges banked; holder $(holder)"
