#!/bin/zsh
# SIDE-LANE ALL-COMMITS DRIFT WATCH — s30 instance, 2026-08-11.
#
# Emits one line per NEW commit in the repo (any lane, including this one), for
# audit against the D1-D18 checklist in
# docs/research/PROGRAMME-drift-watch-2026-08-09.md.
#
# DESIGN NOTES, each one a standing note this repo paid for:
#  * The loop calls _pass(); the selftest calls _pass(). There is no second copy
#    of the computation in the test (s29 green-selftest sweep: "the test builds
#    its own copy of the computation instead of calling the production function").
#  * BLINDNESS IS ANNOUNCED, NOT SILENT. If the repo is unreadable the watch
#    prints DRIFT-WATCH BLIND rather than going quiet -- a monitor whose healthy
#    line and blind line are identical is the ship_watch failure (CLAUDE.md).
#  * Every emitted line carries its own clock in UTC with an explicit Z.
#
# Modes:
#   DRIFT_ONCE=1   run a single pass and exit (this is what the selftest drives)
#   DRIFT_SEED=<rev>  start from this rev instead of HEAD
#   DRIFT_REPO=<path> repo to watch (the selftest breaks this on purpose)

REPO=${DRIFT_REPO:-/Users/junghard/Projects/Work/florent-code-game}
SLEEP=${DRIFT_SLEEP:-45}
LAST=${DRIFT_SEED:-}
BLIND_SINCE=""

_now() { date -u '+%Y-%m-%dT%H:%M:%SZ' }

# _pass: emit every commit after $LAST, advance $LAST. Returns 1 if blind.
_pass() {
  local head new
  head=$(git -C "$REPO" rev-parse HEAD 2>/dev/null)
  if [[ -z "$head" ]]; then
    # Blind: announce on entry and every 10 min thereafter, never silently.
    local n=$(date -u +%s)
    if [[ -z "$BLIND_SINCE" ]] || (( n - BLIND_SINCE >= 600 )); then
      echo "DRIFT-WATCH BLIND $(_now) — cannot read git HEAD at ${REPO}; commits are NOT being audited"
      BLIND_SINCE=$n
    fi
    return 1
  fi
  if [[ -n "$BLIND_SINCE" ]]; then
    echo "DRIFT-WATCH RECOVERED $(_now) — git readable again at ${REPO}"
    BLIND_SINCE=""
  fi
  if [[ -z "$LAST" ]]; then LAST=$head; return 0; fi
  if [[ "$LAST" != "$head" ]]; then
    # TZ=UTC is LOAD-BEARING: --date=format-local renders in the AMBIENT zone,
    # so without it this prints CEST wall-clock under a `Z` suffix -- the exact
    # defect this lane flags in elo_history.tsv and ship_watch.log. Caught s30
    # on the watch's own first live event (08:07:45Z for a 06:07:45Z commit).
    new=$(TZ=UTC git -C "$REPO" log --reverse --format='COMMIT %h %an %ad %s' --date=format-local:'%Y-%m-%dT%H:%M:%SZ' "${LAST}..${head}" 2>/dev/null)
    [[ -n "$new" ]] && print -r -- "$new"
    LAST=$head
  fi
  return 0
}

if [[ -n "$DRIFT_ONCE" ]]; then
  # Propagate _pass's blind/ok status. The EMITTED LINE is still the
  # load-bearing field (CLAUDE.md: exit code is not a health signal on this
  # platform); the code is a convenience for scripted callers, not the gate.
  _pass
  exit $?
fi

echo "DRIFT-WATCH ARMED $(_now) — repo ${REPO}, cadence ${SLEEP}s, base $(git -C "$REPO" rev-parse --short HEAD 2>/dev/null || echo UNREADABLE)"
while true; do
  _pass
  sleep "$SLEEP"
done
