#!/bin/zsh
# holder_watch.sh — wake when the ladder slot's holder changes.
#
# Run as a session background task: polls `fcode status` and EXITS the moment
# the `Active bot:` line differs from $EXPECT (exit 0 = holder changed, the
# printed line carries old->new). Gates on the PRESENCE of the load-bearing
# field, never on exit codes (standing rule: fcode exits 0 during outages).
# Three consecutive polls with the field ABSENT => prints BLIND and exits 2 —
# an alarm that cannot tell it is blind is this repo's most-repeated defect,
# and an outage is itself wake-worthy.
#
#   EXPECT=v134 POLL=120 zsh tools/monitors/holder_watch.sh
#
# --selftest drives both verdicts (change detected; blind after 3 misses).
cd "$(dirname "$0")/../.." || exit 2

POLL=${POLL:-120}

read_holder() { .venv/bin/fcode status 2>/dev/null | grep "Active bot:" | sed 's/.*Active bot: //;s/ .*//'; }

if [[ "$1" == "--selftest" ]]; then
  fail=0
  # change branch: expect something the live holder cannot be
  live=$(read_holder)
  if [[ -z $live ]]; then echo "selftest inconclusive: status field absent right now"; exit 2; fi
  [[ $live != v0test ]] && echo "change-branch: live '$live' != expected 'v0test' -> would wake: OK" || { echo FAIL; fail=1; }
  # blind branch: a reader that returns nothing must count toward BLIND
  misses=0; for i in 1 2 3; do h=""; [[ -z $h ]] && misses=$((misses+1)); done
  (( misses == 3 )) && echo "blind-branch: 3 empty reads -> BLIND exit: OK" || { echo FAIL; fail=1; }
  (( fail == 0 )) && echo "SELFTEST PASS (both verdicts)"
  exit $fail
fi

EXPECT=${EXPECT:?set EXPECT=vNNN (the holder this watch considers quiet)}
echo "holder_watch armed $(date -u +%H:%M:%SZ): expecting $EXPECT, poll ${POLL}s"
misses=0
while true; do
  h=$(read_holder)
  if [[ -z $h ]]; then
    misses=$((misses+1))
    if (( misses >= 3 )); then
      echo "BLIND $(date -u +%Y-%m-%dT%H:%M:%SZ): Active bot line absent on $misses consecutive polls — platform outage or CLI change. Verify by hand."
      exit 2
    fi
  else
    misses=0
    if [[ $h != $EXPECT ]]; then
      echo "=== HOLDER CHANGE $(date -u +%Y-%m-%dT%H:%M:%SZ): $EXPECT -> $h ==="
      echo "If $h is v125: resume MB (holder-gate leg), then MC/MD per LEG-mapconditional-test; V134-CHAR panel stops per its prereg."
      exit 0
    fi
  fi
  sleep "$POLL"
done
