#!/bin/zsh
# FAN-OUT RUNNER — several experiments accumulating in parallel, one window each.
#
# Magnus, 2026-08-10: "are we waiting for something before we start fanning out
# 3 or more experiments in the unrated games?"  No. Nothing was blocking it; the
# legs had been run serially out of habit from when windows felt scarce.
#
# WHY A ROTATION AND NOT TRUE PARALLELISM: only ONE submission can be active at
# a time, so arms cannot run simultaneously — but they do not need to. The rate
# limit allows one 5-match window per 20 MINUTES (corrected s28 2026-08-10 off
# the CLI's own message; this said 10 and slept 620s), so the windows are the
# scarce unit and they can be dealt out round-robin. Each arm accrues 25 games
# per cycle; at the true cadence a 6-arm cycle is ~2h.
#
# ⚠ STILL DEFECTIVE, DO NOT RESTART UNATTENDED WITHOUT FIXING fire():
# fire() retries a rejected challenge 3x at 25s and then GIVES UP, printing
# "fired 3/5". Under a window it cannot outwait that drop is systematic and
# always lands on the TAIL of the id list, starving the same cells every time.
# tools/panel2_cal.sh shows the fix: wait out the window, retry the same cell,
# and rotate the starting cell so a residual drop cannot bias one opponent.
#
# THE INCUMBENT IS NOW v104 "Loki v2" and it is the CONTROL — its windows cost
# no activation at all, which is why it is dealt first in every cycle.
#
# Every non-incumbent window is: activate -> fire 5 -> roll back and VERIFY.
# Never longer than it takes to fire, because an activation window is also a
# scouting window for anyone sampling our live submission.
cd /Users/junghard/Projects/Work/florent-code-game
PANEL=(f670dfed-dfee-421b-8c01-a67b8a278ce3 bfbb9a68-b37a-4a61-b0ea-d36369c8f65a 26286680-d861-4f9e-9073-a6201bd48d3b ebd8d82a-7365-4ccb-af0b-defea3a1ac4d 74e43df6-bad7-474b-8e37-0ea44a2c80f1)
MAPS=(--map fjordgate --map jackpot --map atoll --map saga --map snowflake)
INCUMBENT=104
holder(){ .venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //'; }
gate(){ local ok=0; for i in $(seq 1 40); do [[ -n "$(holder)" ]] && ok=$((ok+1)) || ok=0; [[ $ok -ge 2 ]] && return 0; sleep 15; done; return 1; }
back(){ for t in $(seq 1 60); do .venv/bin/fcode submission activate $INCUMBENT >/dev/null 2>&1; sleep 4
          case "$(holder)" in v$INCUMBENT*) return 0;; esac; done
        printf '%s ROLLBACK TO v%s NEVER VERIFIED\n' "$(date -u +%H:%M:%SZ)" "$INCUMBENT" > corpus/HOLDER_ALERT; return 1; }
PANEL2=(f61d19c1-600e-457b-861b-dbeb6b3d8691 48340ad8-701f-4a40-850d-1f3f3d56d8ca 0774b1b2-df40-4cf2-915e-5d5a6133a13a bfbb9a68-b37a-4a61-b0ea-d36369c8f65a ebd8d82a-7365-4ccb-af0b-defea3a1ac4d)
# fire() VERIFIES THE HOLDER BEFORE EVERY CHALLENGE.
# 2026-08-10: a CONFIRM-v102 window failed to roll back, and the next arm --
# CONTROL, which activates nothing and therefore checked nothing -- fired its
# challenges into a live v102. Two matches (10 games) entered the CONTROL arm
# played by the WRONG BOT, i.e. the denominator every other arm is measured
# against was silently contaminated by the arm that had just run.
# An arm that does not activate must still ASSERT what is active. $3 = expected
# version int; empty means "the incumbent".
fire(){ local n=0; local ids; ids=($PANEL)
        [[ "$2" == PANEL2* ]] && ids=($PANEL2)
        local want="${3:-$INCUMBENT}"
        local live="$(holder)"
        if [[ "$live" != v${want}* ]]; then
          echo "$(date -u +%H:%M:%SZ) $2: ABORT -- expected v$want, holder is '$live'. Firing nothing."
          printf '%s fanout arm %s aborted: holder v%s expected, saw %s\n' "$(date -u +%H:%M:%SZ)" "$2" "$want" "$live" >> corpus/FANOUT_ABORT
          return 1
        fi
        # DEFICIT-FIRST ORDERING (s28). The rate limit is 5 per 20 MINUTES, not
        # 10 (measured off the CLI 2026-08-10), so an arm can be rejected partway
        # through its window. The old loop retried 3x at 25s, gave up, printed
        # "fired 3/5" and moved on -- and because it always walked $ids in the
        # same order, the drop was SYSTEMATIC: it landed on the SAME cells every
        # time, starving them while the rest filled.
        #
        # WHICH cells: NOT a fixed end of the list. This comment first claimed
        # "always the TAIL"; research then claimed "always the HEAD"; both are
        # over-general and the primaries settle it. DROP POSITION IS WHERE THE
        # RATE-LIMIT WINDOW BOUNDARY FALLS IN THE ID LIST, set by the budget the
        # arm inherits -- a fresh/partial budget starves the TAIL (panel2 cycle 1
        # dropped cells 4 and 5, which were exactly the two RETAINED controls, so
        # the panel starved its own linkage), an exhausted budget from a restart
        # starves the HEAD (v104 control cycles 3 and 4 lost cells {1,2,3} and
        # {1,2}). THE ROTATION FIX IS DIRECTION-AGNOSTIC AND SURVIVES BOTH.
        # Also, from the same audit: two of the four apparent deficits are
        # RESTART TRUNCATION, not drops (a final partial cycle when the runner
        # was stopped), and loki14/loki16/v102confirm are perfectly uniform with
        # zero drops -- only the CONTROL arm is composition-skewed, and I Stone,
        # one of the two cells that can move, is the under-represented one.
        #
        # WHY NOT panel2_cal.sh's FIX (wait out the window, retry the same cell):
        # that runner activates NOTHING. A fanout arm has a PROTOTYPE LIVE while
        # it fires, so waiting 5+ minutes mid-window extends rated and scouting
        # exposure -- the header's "never longer than it takes to fire" is a
        # safety property, not an efficiency one. So this arm does not wait; it
        # makes the drop UNBIASED instead, by firing the cells it owes first.
        #
        # The deficit is read from the arm's OWN outfile -- fewest banked first
        # -- so it is self-healing and needs no state file to drift out of sync.
        #
        # COUNT ON "^$id ", NOT ON matchId. The fcode CLI now prints an
        # "Update available: 2.3.6 -> 2.3.7" banner, so a record lands as TWO
        # lines: "<id> Update available..." then "{"matchId": ...}". A predicate
        # of "^$id .*matchId" therefore matches NOTHING and returns a constant 0
        # for every cell -- an ordering that looks like it works and never
        # reorders. Only the *matchId* branch appends, so one line starting with
        # the id IS one banked challenge. (Caught by inspecting the outfile
        # before trusting the count; the same banner already inflated two
        # recorded n's via `wc -l`.)
        if [[ -s "$1" ]]; then
          ids=(${(f)"$(for id in $ids; do
                        printf '%s %s\n' "$(grep -c "^$id " $1)" "$id"
                      done | sort -n | cut -d' ' -f2)"})
        fi
        for id in $ids; do for t in 1 2 3; do
          r=$(.venv/bin/fcode match unrated "$id" $MAPS --json 2>&1)
          case "$r" in
            *matchId*)     echo "$id $r" >> $1; n=$((n+1)); break;;
            *Rate\ limit*) echo "$(date -u +%H:%M:%SZ) $2: rate-limited on ${id:0:8}, deferring to next window"; break;;
            *)             sleep 25;;
          esac
        done; done
        if [[ $n -lt 5 ]]; then
          echo "$(date -u +%H:%M:%SZ) $2: fired $n/5 -- ${#ids} cells owed, deficit-first next window"
        else
          echo "$(date -u +%H:%M:%SZ) $2: fired $n/5"
        fi; }

# ARM TABLE:  label:version:outfile   ("-" version = incumbent, no activation)
ARMS=(
  "CONTROL-v104:-:scratchpad/arm_v104.txt"
  "LOKI15-quota:105:scratchpad/arm_loki15.txt"
  "CONFIRM-v102:102:scratchpad/arm_v102confirm.txt"
  "LOKI16-ringhold:106:scratchpad/arm_loki16.txt"
  "LOKI14-kidnap:107:scratchpad/arm_loki14.txt"
  "PANEL2-CAL:-:scratchpad/arm_panel2.txt"
)
# PANEL-2 CALIBRATION uses a DIFFERENT opponent set — see fire() below.
for cycle in $(seq 1 12); do
  for a in $ARMS; do
    label=${a%%:*}; rest=${a#*:}; ver=${rest%%:*}; out=${rest#*:}
    if [[ "$ver" == "-" ]]; then
      # An incumbent arm activates nothing -- so it must ASSERT the incumbent.
      fire $out "$label" "$INCUMBENT" || back
    else
      gate || { echo "$(date -u +%H:%M:%SZ) gate shut, skipping $label"; sleep 600; continue; }
      .venv/bin/fcode submission activate $ver >/dev/null 2>&1
      fire $out "$label" "$ver"
      back || echo "$(date -u +%H:%M:%SZ) ** $label rollback unverified **"
    fi
    sleep 1230   # 20-min rate-limit window + margin (s28 correction)
  done
  echo "=== cycle $cycle done: $(for a in $ARMS; do o=${a##*:}; echo -n "$(basename $o)=$(grep -c matchId $o 2>/dev/null || echo 0) "; done)"
done
