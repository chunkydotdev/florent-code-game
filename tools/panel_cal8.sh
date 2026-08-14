#!/bin/zsh
# PANEL-CAL-8 runner — CAL-8 (P4-primary redesign). Prereg docs/research/PREREG-CAL8-2026-08-14.md (7fa94cb3, 15:33:08Z, pre-leg). Copy of panel_cal7.sh; BOUNDARY=30 accepts = the n=150 look (or stop with n>=75 per the prereg). Fire only after the 15:58:51Z stability gate. Original header follows.
# (coordination 2026-08-14T13:07:32Z), prereg
# docs/research/PREREG-CAL7-2026-08-14.md (committed 966882f4, 13:06:25Z,
# pre-leg; amendment A1 add-only, blind to CAL-7 data).
#
# Copy of tools/panel_cal1.sh's mechanics (cyclic persisted pointer, holder
# assert PER FIRE, rate-limit waits and retries the SAME cell, boundary stop
# in the runner not in a session watcher). ⛔ Discipline attaches to the COPY:
# run `--selftest` on THIS file before arming (s28 side-lane rule — a mutation
# test done on the original does not cover the copy).
#
# CAL-7 differences from the cal1 template, all per the prereg:
#   * Cells D1-D6 re-selected for CURRENT-ERA RATED OVERLAP (≥5 matches at
#     ourver>=125), spanning our observed rated share so a fixture bias shows
#     as a slope: 0033 · LingLing40 · Juusto · Jython · Big O · team lazy.
#     Leviathan DROPPED (floor-pinned 3/65 across three panels — no
#     information); HTTP 418 and farming_200s rotated out.
#   * Boundary = 60 accepts (n=300 games, the single comparative look).
#     The n=150 interim (30 accepts) is DESCRIPTIVE ONLY and is a read, not a
#     stop — the runner keeps firing through it.
#   * INCUMBENT=140 (v140 "Loki v10", bots/_v223sealrepair).
cd /Users/junghard/Projects/Work/florent-code-game || exit 2

CELLS=(
  74ae65ff-96ae-4da5-a43e-692eb6fee38f  # D1 0033        (era-rated 23.3%, -39.4, = CAL C5)
  86d0b484-783c-47dc-99d9-6ed9af2794f8  # D2 LingLing40  (40.0%, NEW; "leak" narrative retracted in A1)
  32087804-2dde-4265-acb2-b6ec9039fbee  # D3 Juusto      (52.5%, = CAL C2; price at league_matches newest, NOT the band cache)
  8cf9b751-00d3-484a-b0ed-e3073ae1d46f  # D4 Jython      (56.7%, NEW)
  f3362833-2d7a-4636-9a3c-e4f10fcebdc1  # D5 Big O       (60.0%, NEW)
  648d1d5b-5443-4257-a0aa-7048661b612d  # D6 team lazy   (74.3%, = CAL C1)
)
NAMES=(D1-0033 D2-LingLing40 D3-Juusto D4-Jython D5-BigO D6-teamlazy)

INCUMBENT=${INCUMBENT:-140}     # overridable ONLY for the abort-branch selftest
PTR=${PTR:-scratchpad/panel_cal8_pointer.txt}
OUT=${OUT:-scratchpad/panel_cal8_fires.tsv}
STOP=scratchpad/PANEL_CAL8_STOP
BOUNDARY=${BOUNDARY:-30}        # accepts; 60 x 5 games = n=300, the ONE comparative look
# Window arithmetic inherited from cal1 (side lane s36 fix): rolling 20-min
# limit, rejected attempts count. FIRE_GAP*4 + POST_SLEEP >= 1200s.
FIRE_GAP=${FIRE_GAP:-250}       # s between accepted fires
BACKOFF=${BACKOFF:-305}         # s after a rate-limit rejection, same cell
WINDOWS=${1:-999}               # run until boundary/stop by default

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
  # cell table integrity: 6 ids, 6 names, ids unique (a duplicated id would
  # silently double one cell's share of the panel)
  [[ ${#CELLS[@]} -eq 6 && ${#NAMES[@]} -eq 6 ]]          || { echo "FAIL cell/name count"; fail=1; }
  [[ $(printf '%s\n' "${CELLS[@]}" | sort -u | wc -l | tr -d ' ') -eq 6 ]] || { echo "FAIL duplicate cell id"; fail=1; }
  (( fail == 0 )) && echo "SELFTEST PASS (3 classifier verdicts + abort branch + cell table)"
  exit $fail
fi

[[ -f $PTR ]] || echo 0 > $PTR

# ARMED-VALUE ECHO (side lane s40): the boundary decides ~45min vs ~1h45m of
# the shared unrated budget, and an env override is invisible from outside the
# process (macOS ps eww shows no env). The armed value is OBSERVABLE in the
# log and the fires tape from launch, not first at the stop row 75 games later.
printf '%s\tARMED\tboundary\tBOUNDARY=%s PTR=%s accepts_so_far=%s\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BOUNDARY" "$(cat $PTR)" \
  "$(awk -F'\t' '$3=="ACCEPT"' $OUT 2>/dev/null | wc -l | tr -d ' ')" | tee -a $OUT

for w in $(seq 1 $WINDOWS); do
  if [[ -f $STOP ]]; then
    echo "$(date -u +%H:%M:%SZ) PANEL-CAL-8: STOP file present, yielding." | tee -a $OUT
    exit 0
  fi
  n=0
  while (( n < 5 )); do
    [[ -f $STOP ]] && { echo "$(date -u +%H:%M:%SZ) PANEL-CAL-8: STOP mid-window after $n fires." | tee -a $OUT; exit 0; }
    # Holder verified PER FIRE, not per window (side lane s36: a mid-window
    # rotation would otherwise get up to 4 fires at the wrong holder).
    live="$(holder)"
    if [[ "$live" != v${INCUMBENT}* ]]; then
      printf '%s\tABORT\tholder\texpected v%s saw "%s"\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$INCUMBENT" "$live" >> $OUT
      echo "$(date -u +%H:%M:%SZ) PANEL-CAL-8 ABORT: holder is '$live', not v$INCUMBENT. Firing nothing."
      exit 1
    fi
    accepts=$(awk -F'\t' '$3=="ACCEPT"' $OUT | wc -l | tr -d ' ')
    if (( accepts >= BOUNDARY )); then
      echo "$(date -u +%H:%M:%SZ) PANEL BOUNDARY: $accepts accepts >= $BOUNDARY — the n=300 look boundary. Stopping."
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
  echo "$(date -u +%H:%M:%SZ) PANEL-CAL-8: window $w complete (5 accepted), pointer at $(cat $PTR)."
  sleep 280  # 4*FIRE_GAP + 280 = 1280s > 1200s rolling window (side lane fix)
done
