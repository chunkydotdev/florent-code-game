#!/bin/zsh
# FAN-OUT RUNNER — several experiments accumulating in parallel, one window each.
#
# Magnus, 2026-08-10: "are we waiting for something before we start fanning out
# 3 or more experiments in the unrated games?"  No. Nothing was blocking it; the
# legs had been run serially out of habit from when windows felt scarce.
#
# WHY A ROTATION AND NOT TRUE PARALLELISM: only ONE submission can be active at
# a time, so arms cannot run simultaneously — but they do not need to. The rate
# limit allows one 5-match window per 10 minutes, so the windows are the scarce
# unit and they can be dealt out round-robin. Each arm accrues 25 games per
# cycle; a 4-arm cycle is ~40 min and puts every arm at n=100 in ~2.7 hours.
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
        for id in $ids; do for t in 1 2 3; do
          r=$(.venv/bin/fcode match unrated "$id" $MAPS --json 2>&1)
          case "$r" in *matchId*) echo "$id $r" >> $1; n=$((n+1)); break;; *) sleep 25;; esac
        done; done; echo "$(date -u +%H:%M:%SZ) $2: fired $n/5"; }

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
    sleep 620
  done
  echo "=== cycle $cycle done: $(for a in $ARMS; do o=${a##*:}; echo -n "$(basename $o)=$(grep -c matchId $o 2>/dev/null || echo 0) "; done)"
done
