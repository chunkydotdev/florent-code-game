#!/bin/zsh
# gate_watch.sh — DURABLE corefill gate/finals watch. Pays the D2 instrument
# debt from s37 (the session-tied watcher died with its session and AMMO0 ran
# through both futility gates unwatched, ~4,400 games wasted).
#
# WHAT IT DOES: for every shard in the worklist, compares the shard TSV's row
# count against the gate boundaries (1000 / 2700 / final target from the
# worklist's n column) and the typed-gate ledger scratchpad/gate_watch_state.txt
# (lines `SHARD:1000`, `SHARD:2700`, `SHARD:DONE`). The moment a boundary is
# crossed that has no ledger entry, it PRINTS the numbers and EXITS — run it as
# a session background task and the exit IS the wake. The watcher never
# decides; the builder types the gate (RULE-futility-gates-2026-08-13).
#
# s37 FALLTHROUGH FIX ENCODED: a shard past 2700 with no 1000 entry wakes for
# GATE-2700 ONLY (never a spurious GATE-1000); typing the 2700 gate records
# BOTH lines in the ledger.
#
# BLIND RULE: unreadable worklist/TSV dir => prints BLIND and exits 2 rather
# than reporting quiet health. Every wake line carries the TSV's age (the
# freshness rule: a healthy line and a blind line must not be byte-identical).
#
# MODES:  --check      single pass, print any due gates, exit 0 (3 if due)
#         --selftest   fixture drive, both verdicts per guard
#         (default)    loop every $POLL s until a gate is due, print, exit 0
cd "$(dirname "$0")/../.." || exit 2

WORK=${WORK:-scratchpad/corefill_work.txt}
TSVDIR=${TSVDIR:-scratchpad/overnight}
STATE=${STATE:-scratchpad/gate_watch_state.txt}
POLL=${POLL:-120}

scan() {  # prints one line per due gate; returns 0 if none due, 3 if any
  [[ -r $WORK && -d $TSVDIR ]] || { echo "BLIND: worklist or TSV dir unreadable ($WORK / $TSVDIR)"; return 2; }
  local due=0
  grep -v '^#' "$WORK" | while read -r shard tree ctrl target seed rest; do
    [[ -n $shard && $target == <-> ]] || continue
    local tsv="$TSVDIR/$shard.tsv"
    [[ -f $tsv ]] || continue
    local n= wins= age= gate=""
    n=$(( $(wc -l < "$tsv") - 1 ))
    (( n < 1 )) && continue
    if (( n >= target )) && ! grep -q "^$shard:DONE$" "$STATE" 2>/dev/null; then
      gate="FINAL"
    elif (( n >= 2700 )) && ! grep -q "^$shard:2700$" "$STATE" 2>/dev/null; then
      gate="GATE-2700"   # covers a missing 1000 too — never a spurious GATE-1000 (s37 fix)
    elif (( n >= 1000 )) && (( n < 2700 )) && ! grep -q "^$shard:1000$" "$STATE" 2>/dev/null; then
      gate="GATE-1000"
    elif (( n >= 400 )) && (( n < 1000 )) && ! grep -q "^$shard:400$" "$STATE" 2>/dev/null; then
      # CATASTROPHE GATE (s39, Magnus: "any reason we continue it across 1000
      # ... when it's so far below 50%?"). NOAPPROACH ran to 2,264 rows at
      # 18.55% because nothing looked before 1000. Wake ONLY when the share
      # reads under 42 at n in [400,1000) — the typed bar is <40 (a true-50%
      # arm crosses it with p ~ 3e-5 even before correlation inflation, so the
      # extra look spends ~no alpha); 42 wakes the builder ahead of the bar.
      # The watcher still never decides: it wakes, the builder types.
      local w4=$(awk -F'\t' 'NR>1 && $7=="T"' "$tsv" | wc -l | tr -d ' ')
      if (( 100 * w4 < 42 * n )); then
        gate="GATE-400-CATA"
      fi
    fi
    if [[ -n $gate ]]; then
      wins=$(awk -F'\t' 'NR>1 && $7=="T"' "$tsv" | wc -l | tr -d ' ')
      age=$(( $(date +%s) - $(stat -f %m "$tsv") ))
      printf 'DUE %-12s %-9s n=%d/%d  T-share=%s%%  tsv_age=%ds\n' \
        "$shard" "$gate" "$n" "$target" \
        "$(awk -v w="$wins" -v n="$n" 'BEGIN{printf "%.2f", 100*w/n}')" "$age"
      echo DUE >> "${SCAN_FLAG:-/dev/null}"
    fi
  done
  [[ -s ${SCAN_FLAG:-/dev/null} ]] && return 3 || return 0
}

if [[ "$1" == "--selftest" ]]; then
  FIX=$(mktemp -d); fail=0
  mkfixture() {  # $1 shard, $2 rows, tsv with $2 data rows, T winner on evens
    { echo "ts\tshard\tgame\tmap\tseed\tseat\twinner\tcond\tturns"
      for i in $(seq 1 $2); do
        if (( i % 2 == 0 )); then w=T; else w=C; fi
        echo "2026-08-14T00:00:00Z\t$1\t$i\tm\t1\tA\t$w\tx\t100"
      done } > "$FIX/tsv/$1.tsv"
  }
  mkfixture_lo() {  # $1 shard, $2 rows: T wins only every 10th row (10% share)
    { echo "ts\tshard\tgame\tmap\tseed\tseat\twinner\tcond\tturns"
      for i in $(seq 1 $2); do
        if (( i % 10 == 0 )); then w=T; else w=C; fi
        echo "2026-08-14T00:00:00Z\t$1\t$i\tm\t1\tA\t$w\tx\t100"
      done } > "$FIX/tsv/$1.tsv"
  }
  mkdir -p "$FIX/tsv"; : > "$FIX/state"
  {
    echo "QUIETSHARD  bots/_a  bots/_b  5400  1"
    echo "EARLYSHARD  bots/_a  bots/_b  5400  1"
    echo "MIDSHARD    bots/_a  bots/_b  5400  1"
    echo "GRANDDADDY  bots/_a  bots/_b  5400  1"
    echo "FINALSHARD  bots/_a  bots/_b  5400  1"
    echo "TYPEDSHARD  bots/_a  bots/_b  5400  1"
    echo "CATASHARD   bots/_a  bots/_b  5400  1"
    echo "TYPEDCATA   bots/_a  bots/_b  5400  1"
  } > "$FIX/work"
  mkfixture QUIETSHARD 999            # 50% inside [400,1000) -> silent (healthy band)
  mkfixture EARLYSHARD 1001           # -> GATE-1000
  mkfixture MIDSHARD 2750             # 1000 typed -> GATE-2700
  mkfixture GRANDDADDY 2750           # NOTHING typed -> GATE-2700 only, no spurious 1000
  mkfixture FINALSHARD 5400           # 1000+2700 typed -> FINAL
  mkfixture TYPEDSHARD 5400           # all typed -> silent
  mkfixture_lo CATASHARD 450          # 10% share at n=450 -> GATE-400-CATA
  mkfixture_lo TYPEDCATA 450          # same but :400 typed -> silent
  printf 'MIDSHARD:1000\nFINALSHARD:1000\nFINALSHARD:2700\nTYPEDSHARD:1000\nTYPEDSHARD:2700\nTYPEDSHARD:DONE\nTYPEDCATA:400\n' > "$FIX/state"
  out=$(WORK="$FIX/work" TSVDIR="$FIX/tsv" STATE="$FIX/state" SCAN_FLAG="$FIX/flag" zsh "$0" --check)
  echo "$out"
  echo "$out" | grep -q "QUIETSHARD"                        && { echo "FAIL: quiet shard woke"; fail=1; }
  echo "$out" | grep -q "EARLYSHARD  *GATE-1000"            || { echo "FAIL: GATE-1000 did not fire"; fail=1; }
  echo "$out" | grep -q "MIDSHARD  *GATE-2700"              || { echo "FAIL: GATE-2700 did not fire"; fail=1; }
  echo "$out" | grep -q "GRANDDADDY  *GATE-2700"            || { echo "FAIL: grandfathered 2700 did not fire"; fail=1; }
  echo "$out" | grep -q "GRANDDADDY  *GATE-1000"            && { echo "FAIL: spurious GATE-1000 (s37 bug)"; fail=1; }
  echo "$out" | grep -q "FINALSHARD  *FINAL"                || { echo "FAIL: FINAL did not fire"; fail=1; }
  echo "$out" | grep -q "TYPEDSHARD"                        && { echo "FAIL: fully-typed shard woke"; fail=1; }
  echo "$out" | grep -q "CATASHARD  *GATE-400-CATA"         || { echo "FAIL: catastrophe gate did not fire at 10%/450"; fail=1; }
  echo "$out" | grep -q "QUIETSHARD"                        && { echo "FAIL: healthy 50% shard in [400,1000) woke"; fail=1; }
  echo "$out" | grep -q "TYPEDCATA"                         && { echo "FAIL: typed :400 shard woke again"; fail=1; }
  # blind branch: point at a missing dir
  bout=$(WORK="$FIX/work" TSVDIR="$FIX/nodir" STATE="$FIX/state" zsh "$0" --check)
  echo "$bout" | grep -q "BLIND"                            || { echo "FAIL: blind branch silent"; fail=1; }
  # D4 re-arm line, both directions: the WAKE path leads with it; --check does not carry it
  wout=$(WORK="$FIX/work" TSVDIR="$FIX/tsv" STATE="$FIX/state" POLL=1 zsh "$0")
  echo "$wout" | sed -n 2p | grep -q "^RE-ARM FIRST"        || { echo "FAIL: wake does not lead with the re-arm line (D4)"; fail=1; }
  echo "$out" | grep -q "RE-ARM"                            && { echo "FAIL: --check output carries the re-arm line"; fail=1; }
  # T-share arithmetic: 5400 rows, T on evens = exactly 50.00
  echo "$out" | grep "FINALSHARD" | grep -q "T-share=50.00" || { echo "FAIL: share arithmetic"; fail=1; }
  rm -rf "$FIX"
  (( fail == 0 )) && echo "SELFTEST PASS (8 wake/quiet verdicts incl. catastrophe both ways + blind + share + D4 re-arm line both ways)" || echo "SELFTEST FAIL"
  exit $fail
fi

if [[ "$1" == "--check" ]]; then
  SCAN_FLAG=${SCAN_FLAG:-$(mktemp)} ; export SCAN_FLAG
  scan; rc=$?
  [[ -s $SCAN_FLAG ]] && rc=3
  rm -f "$SCAN_FLAG" 2>/dev/null
  exit $rc
fi

echo "gate_watch armed $(date -u +%H:%M:%SZ): poll ${POLL}s, worklist $WORK, ledger $STATE"
while true; do
  SCAN_FLAG=$(mktemp); export SCAN_FLAG
  out=$(scan); rc=$?
  if (( rc == 2 )); then echo "$out"; rm -f "$SCAN_FLAG"; exit 2; fi
  if [[ -s $SCAN_FLAG ]]; then
    # D4 (s38 retro): the manual re-arm step failed under ship-flow once — the
    # wake itself must carry the re-arm as its FIRST line. (A nohup'd successor
    # cannot wake a harness session, so self-respawn is not an option here.)
    echo "RE-ARM FIRST: relaunch 'zsh tools/monitors/gate_watch.sh' as a background task BEFORE typing any gate below (D4)"
    echo "=== GATE WAKE $(date -u +%Y-%m-%dT%H:%M:%SZ) — builder types the decision, watcher never decides ==="
    echo "$out"
    rm -f "$SCAN_FLAG"; exit 0
  fi
  rm -f "$SCAN_FLAG"
  sleep "$POLL"
done
