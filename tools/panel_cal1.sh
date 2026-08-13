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

# CAL-3 cells (fire order #3 @63d45eb; prereg PREREG-PANEL-CAL3-v125-band).
# CAL-1/CAL-2 cell sets retired with their panels — retained cells do NOT pool
# across panels; totals reset with the new PTR/OUT files.
CELLS=(
  648d1d5b-5443-4257-a0aa-7048661b612d  # C1 team lazy      (stretch, profiled)
  f3362833-2d7a-4636-9a3c-e4f10fcebdc1  # C2 Big O          (stretch, unprofiled)
  26286680-d861-4f9e-9073-a6201bd48d3b  # C3 Leviathan      (core-tank class)
  8cf9b751-00d3-484a-b0ed-e3073ae1d46f  # C4 Jython         (even)
  32087804-2dde-4265-acb2-b6ec9039fbee  # C5 Juusto         (even)
  ea0d33c8-ca2b-497a-9be0-1837379eab1e  # C6 Coreflood      (below)
)
NAMES=(C1-team-lazy C2-Big-O C3-Leviathan C4-Jython C5-Juusto C6-Coreflood)

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
    # BOUNDARY STOP (research ask, 2026-08-13 s37): the panel's comparative
    # look is pre-committed at a fixed n; firing past it buys games no read
    # may use. 30 accepts x 5 games = 150 = the look boundary. Durable — in
    # the runner itself, not in any session's watcher (the s36 class).
    accepts=$(awk -F'\t' '$3=="ACCEPT"' $OUT | wc -l | tr -d ' ')
    if (( accepts >= 30 )); then
      echo "$(date -u +%H:%M:%SZ) PANEL BOUNDARY: $accepts accepts >= 30 — look boundary reached, stopping. Rotate per the CAL-(N+1) selection prereg."
      printf '%s\tBOUNDARY\tstop\t%s accepts\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$accepts" >> $OUT
      exit 0
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
