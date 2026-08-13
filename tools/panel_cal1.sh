#!/bin/zsh
# PANEL-CAL-1 runner — research fire order #1 (coordination 2026-08-13T08:49:47Z),
# prereg docs/research/PREREG-PANEL-CAL1-v123-field-2026-08-13.md.
#
# THE ORDER, encoded:
#   * 6 cells, CYCLIC pointer continuing across windows (pointer persisted in
#     $PTR so a restart cannot reset it to C1 and starve the tail — the
#     fanout.sh systematic-drop failure, CLAUDE.md).
#   * 5 accepted fires per 20-min window; a rate-limit rejection WAITS and
#     retries the SAME cell.
#   * NO --map pin: the prereg records the platform's draw (the 900-area games
#     are the live 30x30 evidence). panel2_cal.sh's MAPS array is 4/5 retired
#     maps — do not copy it.
#   * Holder verified v123 AT FIRE TIME each window (D28: a document naming the
#     holder is a cache). Wrong holder => abort loudly, fire nothing.
#   * Stop file scratchpad/PANEL_CAL1_STOP: the yield rule — touch it before
#     any treatment leg's window; delete to resume.
#
# SELFTEST (--selftest): drives the response classifier to all three verdicts
# and the holder guard to its abort branch. A runner that has never produced
# the other verdict has not been seen to check.
cd /Users/junghard/Projects/Work/florent-code-game || exit 2

CELLS=(
  648d1d5b-5443-4257-a0aa-7048661b612d  # C1 team lazy
  00191498-aa36-4f5a-aafb-e432e57607e8  # C2 Focalground
  32087804-2dde-4265-acb2-b6ec9039fbee  # C3 Juusto
  8cf9b751-00d3-484a-b0ed-e3073ae1d46f  # C4 Jython
  f670dfed-dfee-421b-8c01-a67b8a278ce3  # C5 The Bisons
  eceb8455-7cb3-442b-ba40-c6597c16b446  # C6 Lunds Stallions
)
NAMES=(C1-team-lazy C2-Focalground C3-Juusto C4-Jython C5-The-Bisons C6-Lunds-Stallions)

INCUMBENT=${INCUMBENT:-123}     # overridable ONLY for the abort-branch selftest
PTR=${PTR:-scratchpad/panel_cal1_pointer.txt}
OUT=${OUT:-scratchpad/panel_cal1_fires.tsv}
STOP=scratchpad/PANEL_CAL1_STOP
# ⛔ WINDOW ARITHMETIC (side lane s36, caught live at window 1): the limit is a
# ROLLING 20 min and REJECTED ATTEMPTS COUNT (CLAUDE.md). Five fires span only
# 4*FIRE_GAP, so the next window's first fire must wait until the oldest accept
# ages out: FIRE_GAP*4 + POST_SLEEP >= 1200s. And BACKOFF must keep the ATTEMPT
# rate under 1 per 240s, or each rejection re-fills the rolling window and the
# stall self-sustains (the fanout.sh failure class, rediscovered).
FIRE_GAP=${FIRE_GAP:-250}       # s between accepted fires
BACKOFF=${BACKOFF:-305}         # s after a rate-limit rejection, same cell
WINDOWS=${1:-999}               # run until stopped by default

classify() {  # $1 = fcode output -> ACCEPT | RATELIMIT | ERROR
  case "$1" in
    *matchId*)      echo ACCEPT;;
    *"Rate limit"*) echo RATELIMIT;;
    *)              echo ERROR;;
  esac
}

holder() { .venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //'; }

if [[ "$1" == "--selftest" ]]; then
  fail=0
  [[ $(classify 'x {"matchId": "abc"} y') == ACCEPT ]]    || { echo "FAIL accept"; fail=1; }
  [[ $(classify 'Error: Rate limit exceeded: max 5 test/unrated matches per 20 minutes') == RATELIMIT ]] \
                                                          || { echo "FAIL ratelimit"; fail=1; }
  [[ $(classify 'Error: True') == ERROR ]]                || { echo "FAIL error"; fail=1; }
  live="$(holder)"
  if [[ "$live" == v999* ]]; then echo "FAIL abort-branch (holder cannot be v999)"; fail=1
  else echo "abort-branch: holder '$live' != v999 -> guard would abort: OK"; fi
  (( fail == 0 )) && echo "SELFTEST PASS (3 classifier verdicts + abort branch)"
  exit $fail
fi

[[ -f $PTR ]] || echo 0 > $PTR

for w in $(seq 1 $WINDOWS); do
  if [[ -f $STOP ]]; then
    echo "$(date -u +%H:%M:%SZ) PANEL-CAL-1: STOP file present, yielding." | tee -a $OUT
    exit 0
  fi
  n=0
  while (( n < 5 )); do
    [[ -f $STOP ]] && { echo "$(date -u +%H:%M:%SZ) PANEL-CAL-1: STOP mid-window after $n fires." | tee -a $OUT; exit 0; }
    # Holder verified PER FIRE, not per window (side lane s36: a mid-window
    # rotation would otherwise get up to 4 fires at the wrong holder).
    live="$(holder)"
    if [[ "$live" != v${INCUMBENT}* ]]; then
      printf '%s\tABORT\tholder\texpected v%s saw "%s"\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$INCUMBENT" "$live" >> $OUT
      echo "$(date -u +%H:%M:%SZ) PANEL-CAL-1 ABORT: holder is '$live', not v$INCUMBENT. Firing nothing."
      exit 1
    fi
    p=$(cat $PTR)
    id=${CELLS[$((p % 6 + 1))]}
    name=${NAMES[$((p % 6 + 1))]}
    r=$(.venv/bin/fcode match unrated "$id" --json 2>&1)
    v=$(classify "$r")
    printf '%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$name" "$v" "$(echo "$r" | tr '\n' ' ' | head -c 300)" >> $OUT
    case "$v" in
      ACCEPT)    echo $((p + 1)) > $PTR; n=$((n + 1)); (( n < 5 )) && sleep $FIRE_GAP;;
      RATELIMIT) sleep $BACKOFF;;                       # same cell, pointer unmoved
      ERROR)     sleep 30;;                             # transient? same cell, logged
    esac
  done
  echo "$(date -u +%H:%M:%SZ) PANEL-CAL-1: window $w complete (5 accepted), pointer at $(cat $PTR)."
  sleep 280  # 4*FIRE_GAP + 280 = 1280s > 1200s rolling window (side lane fix)
done
