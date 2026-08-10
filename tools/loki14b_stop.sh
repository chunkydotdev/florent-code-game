#!/bin/zsh
# STOP WATCHDOG for LOKI-14b. Amendment 6 pre-commits "stop after cycle 4,
# decode, extend ONLY if the throw count is under 150". The runner was launched
# with a cycle count of 6 before that amendment existed, so TEXT AND BEHAVIOUR
# DISAGREED (side-lane flag, s28). This makes behaviour match the text.
#
# It is a SCRIPT and not a reminder for the same reason Amendment 1's floor is a
# script: a pre-commitment that lives in attention is the one that fails under
# time pressure, and this one fires ~50 minutes from now.
cd /Users/junghard/Projects/Work/florent-code-game
LOG=scratchpad/loki14b_run.log
# The stop cycle is a POSITIONAL ARG, not an env var, so it is visible in `ps`.
# s28: armed first as `STOP_AFTER=5 zsh loki14b_stop.sh`, and macOS would not
# show the variable in an env dump -- so the load-bearing parameter of a
# pre-commitment could not be VERIFIED from outside the process. Same rule as
# gating on the `Active bot:` field instead of an exit code: if it matters, it
# has to be observable.
STOP_AFTER=${1:-${STOP_AFTER:-4}}
while true; do
  if grep -q "cycle ${STOP_AFTER}: fired" $LOG 2>/dev/null; then
    # NOTE FOR THE READ-OUT: the gate is on THROWS DELIVERED (>=150), never on
    # cycles. Cycles are a proxy calibrated on LOKI-14's panel at 10.0
    # throws/match; these carriers are weaker bots whose builder counts and
    # border exposure may differ in EITHER direction. Decode and check the
    # actual throw count against 150 before reading anything.
    pkill -f loki14b_leg.sh
    sleep 3
    printf '%s STOP WATCHDOG: cycle %s complete -> runner killed per PREREG amendment 6.\n' \
      "$(date -u +%H:%M:%SZ)" "$STOP_AFTER" >> $LOG
    # The runner rolls back at the END of every cycle, so the incumbent should
    # already hold. VERIFY rather than assume -- a killed runner cannot roll back.
    live=$(.venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //')
    if [[ "$live" != v104* ]]; then
      printf '%s ** HOLDER IS "%s" AFTER STOP -- re-activating v104 **\n' "$(date -u +%H:%M:%SZ)" "$live" >> $LOG
      for t in $(seq 1 30); do
        .venv/bin/fcode submission activate 104 >/dev/null 2>&1; sleep 4
        case "$(.venv/bin/fcode status 2>/dev/null | grep 'Active bot')" in *v104*) break;; esac
      done
    fi
    printf '%s holder after stop: %s\n' "$(date -u +%H:%M:%SZ)" \
      "$(.venv/bin/fcode status 2>/dev/null | grep 'Active bot' | sed 's/.*Active bot: //')" >> $LOG
    exit 0
  fi
  pgrep -f loki14b_leg.sh >/dev/null || { printf '%s STOP WATCHDOG: runner already gone.\n' "$(date -u +%H:%M:%SZ)" >> $LOG; exit 0; }
  sleep 30
done
