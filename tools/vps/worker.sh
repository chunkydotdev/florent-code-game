#!/usr/bin/env bash
# VPS BATTERY WORKER — runs ON the server. Zero platform credentials, ever.
#
#   bash tools/vps/worker.sh [worklist]            # default work/worklist.txt
#   WORKERS=46 LOAD_CEIL=60 bash tools/vps/worker.sh
#
# It plays LOCAL `fcode run` games only. `fcode run` is fully offline — it never
# reaches the platform — so this host needs no token, no `fcode.toml` auth, no
# ladder access. Everything that talks to the platform (submit, unrated legs,
# match list, elo tape) stays on the orchestrating box. If a future edit here
# ever needs a credential, that is the signal that the work does not belong on a
# worker.
#
# ══════════════════════════════════════════════════════════════════════════════
# ⛔⛔ THIS FILE DUPLICATES tools/overnight.sh's ROW SCHEMA AND CYCLING. SAY SO.
# ══════════════════════════════════════════════════════════════════════════════
# `overnight.sh` is zsh and STRICTLY SEQUENTIAL — one `fcode run` at a time, no
# parallelism anywhere in it. A 48-vCPU worker exists precisely to run ~46 games
# at once inside ONE shard, which is not a parameter of that script but a
# different loop shape. Two further blockers: the target is Linux (zsh is not
# installed by default) and `for M in $MAPS` is zsh word-splitting that bash does
# not do.
#
# ⇒ The 9-column row schema, the map x seat x seed cycling ORDER, the substring
#   winner scoring, the NOWINNER abort, the heartbeat format and the COMPLETE
#   marker are REPLICATED HERE, deliberately, byte-for-byte in behaviour.
#   `tools/overnight_read.py` and `tools/corefill_status.sh` parse both without
#   knowing which produced a file — that is the contract, and it is the thing
#   that breaks first if either side drifts.
#
#   ⚠ THE COMPANION NOTE IN tools/overnight.sh IS **NOT YET WRITTEN**, and the
#   reason is itself a finding: at the time this was built, SEVEN live shards
#   were executing `zsh tools/overnight.sh` (5,400 games each). A running shell
#   reads its script from a file OFFSET; editing that file underneath it can
#   feed a live shard garbage. **Paste the note (docs/vps-workers.md, section
#   "PENDING: the overnight.sh companion note") the next time
#   `ps ax | grep '[o]vernight.sh'` is empty.** Until then this file carries the
#   whole warning, which is the correct place for it anyway: the duplicate is
#   the thing that can rot.
#
# ⭐ ONE DELIBERATE DIVERGENCE, AND IT IS A FIX, NOT A DRIFT.
#   overnight.sh resumes with `seed = SEEDLO + n / 16`. Its MAPS array holds
#   FIFTEEN maps x 2 seats = **30 games per seed**, so `/16` has been wrong since
#   the 2026-08-13 rotation: a resume at n=300 jumps to seed+18 instead of
#   seed+10. It never duplicates and never loses rows (it only skips forward
#   through seed space), which is why nothing has caught it — but a worker that
#   resumes must be exact, so here the index IS the position:
#       per_seed = 2 * NMAPS ; seed = SEEDBASE + idx/per_seed
#       map      = MAPS[(idx % per_seed) / 2] ; seat = A if idx even else B
#   Resume = "start at idx = existing row count". Nothing is inferred.
#
# ══════════════════════════════════════════════════════════════════════════════
# THE FOUR REFUSAL GATES. Each refuses LOUDLY and exits non-zero.
# ══════════════════════════════════════════════════════════════════════════════
# G1 VENV       — no .venv/bin/fcode ⇒ print the exact setup commands, exit 3.
# G2 ENGINE PIN — fcode version != tools/ENGINE_PIN ⇒ exit 4. Two engine
#                 versions are two fixtures wearing one name, and the rows are
#                 byte-identical, so nothing downstream can ever notice.
# G3 MAP POOL   — the set of maps/*.map26 must EQUAL work/MAPS.list (generated
#                 on the orchestrator from overnight.sh's own MAPS= line, so
#                 there is still ONE source). A worker holding a retired map, or
#                 missing a live one, silently plays different geometry ⇒ exit 5.
# G4 WORKLIST   — every tree must exist with main.py, and basenames must not
#                 collide by SUBSTRING (scoring is `case $L in *"$B"*`, so
#                 `_v150cb` vs `_v150cbturret` reads ~100% for the control).
#
# ⛔ AND NULLHOST-FIRST, WHICH IS NOT A GATE BUT AN ORDERING.
#   The first shard this host runs is always NULLHOST — a byte-identical tree
#   against itself — until `results/NULLHOST.COMPLETE` exists. On DIFFERENT
#   HARDWARE the null is the only thing that can catch a bent ruler, and the
#   specific mechanism is WALL-CLOCK TLE PARITY: `--tle 10` is a 10ms budget per
#   unit per turn, and a faster or slower core changes WHICH TURNS TIME OUT.
#   A host whose null does not read ~50% is not measuring our game.
#   The reader (`overnight_read.py --include-remote`) enforces 45-55% at n>=400
#   and EXCLUDES an uncertified host from every pooled rate.
#
# STOP: `touch STOP` in the worker root. Checked before every batch and between
# shards. Partial rows are KEPT — nothing here ever deletes data.
set -u

WORK=${1:-work/worklist.txt}
OUT=${OUT:-results}
STOPF=${STOPF:-STOP}
# CURFEW — the host is shared: its owners need the full box 23:00-06:00 CET
# (Magnus, 2026-08-14) = 21:00-04:00 UTC, enforced HERE because a rule that
# lives in a session's memory has a recorded violation in its future. UTC
# arithmetic so the box's TZ setting is irrelevant. The worker SLEEPS through
# the window at batch boundaries (zero CPU, rows kept) and self-resumes —
# nobody has to be awake at 06:00 CET. Override for tests: CURFEW=off.
CURFEW=${CURFEW:-on}
# ⛔ THE HEARTBEAT MUST SAY CURFEW, AND THIS COST AN HOUR OF ANOTHER LANE'S TIME.
# The first cut of curfew_wait slept without touching $HB. Every other terminal
# path stamps its state -- STARTING (:233), STOPPED (:248), RUNNING (:315),
# ABORTED_NOWINNER (:320), COMPLETE (:326) -- and curfew alone did not. So a
# curfewed worker's heartbeat kept its LAST written state, the literal string
# `RUNNING`, forever.
# WHAT THAT PRODUCED, 2026-08-14: SALTREF2 froze at 1740/5400 at 20:55:34Z (the
# curfew boundary, exactly) with a heartbeat reading RUNNING. The side lane
# correctly observed a 41-minute-stale file, three independent confirmations,
# and no .COMPLETE marker where 7 of 7 finished shards on that host have one --
# and concluded the leg was DEAD. It was asleep. **A DEAD WORKER AND A SLEEPING
# WORKER WERE BYTE-IDENTICAL IN HEARTBEAT CONTENT; only the mtime discriminated,
# and nothing read it.** That is this repo's signature defect (`ship_watch`
# printing a healthy line off stale rows) reproduced in the fixture layer.
# ⇒ Stamp CURFEW on entry and RUNNING is restored by the caller on resume. A
# consumer can now distinguish asleep / dead / working from CONTENT, and should
# STILL check freshness -- content alone was never enough.
curfew_wait() {
  [ "$CURFEW" = off ] && return 0
  stamped=
  while :; do
    hm=$(date -u +%H%M)
    # window [2055, 2400) u [0000, 0400): start 5 min early so a running batch
    # never straddles 21:00.
    if [ "$hm" -ge 2055 ] || [ "$hm" -lt 0400 ]; then
      if [ -z "$stamped" ] && [ -n "${HB:-}" ]; then
        printf '%s%s%s%s%s%s%s%s%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$T" "${n:-0}" \
          "$T" "${TARGET:-0}" "$T" "${SHARD:-?}" "$T" CURFEW > "$HB"
        stamped=1
      fi
      printf '%s curfew: sleeping (UTC %s inside 20:55-04:00 blackout)\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$hm"
      sleep 300
    else
      return 0
    fi
  done
}
FC=${FC:-.venv/bin/fcode}
PINF=${PINF:-tools/ENGINE_PIN}
POOLF=${POOLF:-work/MAPS.list}
LOG=${LOG:-worker.log}
T=$(printf '\t')

# Portable core count: nproc (Linux) / sysctl (macOS, because this file is
# ACCEPTANCE-TESTED on the mac orchestrator before any server exists).
ncpu() {
  if command -v nproc >/dev/null 2>&1; then nproc
  elif command -v sysctl >/dev/null 2>&1; then sysctl -n hw.ncpu
  else echo 4; fi
}
NCPU=$(ncpu)
WORKERS=${WORKERS:-$(( NCPU - 2 ))}
# How many games between drains. The drain is where rows are flushed and the
# heartbeat/abort checks run, so this trades straggler tax against how often
# those fire. 8 puts the tax at ~1/8 of its old value while still flushing
# every ~8*WORKERS games (80 on ws1, 48 on ws2).
POOL_BATCH_MULT=${POOL_BATCH_MULT:-8}
[ "$WORKERS" -lt 1 ] && WORKERS=1
# Ceiling is generous on purpose: `fcode run` is one busy CPU per game, so a
# healthy 48-vCPU box at WORKERS=46 sits near 46. The ceiling catches a box that
# is ALSO doing something else, not our own intended load.
LOAD_CEIL=${LOAD_CEIL:-$(( NCPU + NCPU / 4 ))}

say() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" | tee -a "$LOG"; }
die() { say "$*"; exit "${2:-1}"; }

load1() {
  if [ -r /proc/loadavg ]; then cut -d' ' -f1 /proc/loadavg
  elif command -v uptime >/dev/null 2>&1; then
    uptime | sed 's/.*averages*: *//' | awk '{print $1}' | tr -d ','
  else echo 0; fi
}

# ---------------------------------------------------------------- G1: venv ---
if [ ! -x "$FC" ]; then
  cat <<EOF
⛔ REFUSING: no fcode at $FC — this worker has no engine.

Run these on THIS host, from $(pwd):

  sudo apt-get update
  sudo apt-get install -y python3 python3-venv python3-pip rsync
  python3 -m venv .venv
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install "fcode==\$(grep -v '^#' tools/ENGINE_PIN | tr -d '[:space:]')"
  .venv/bin/fcode --version     # must print exactly that version

Or, from the orchestrating box:  tools/vps/orchestrate.sh setup <host> --execute
EOF
  exit 3
fi

# ----------------------------------------------------------- G2: engine pin ---
[ -f "$PINF" ] || die "⛔ REFUSING: no engine pin at $PINF. A worker with no pin cannot know it is playing our game." 4
PIN=$(grep -v '^#' "$PINF" | tr -d '[:space:]')
[ -n "$PIN" ] || die "⛔ REFUSING: $PINF is empty/comment-only — the pin is unreadable, which is not the same as satisfied." 4
# Parse the version line SPECIFICALLY. `fcode` prints an "Update available:
# 2.3.6 -> 2.3.7" nag on some subcommands and a loose semver grep would happily
# match the version we are refusing.
HAVE=$("$FC" --version 2>/dev/null | sed -n 's/^fcode, version \([0-9][0-9.]*\).*/\1/p' | head -1)
[ -n "$HAVE" ] || die "⛔ REFUSING: could not parse a version out of \`$FC --version\`. BLIND is not PASSED." 4
if [ "$HAVE" != "$PIN" ]; then
  say "⛔ REFUSING: ENGINE PIN MISMATCH — this host has fcode $HAVE, the pin is $PIN."
  say "   Two engine versions are two fixtures wearing one name, and the rows are"
  say "   byte-identical, so nothing downstream can notice. Fix the host, not the pin:"
  say "     $FC --version ; .venv/bin/pip install 'fcode==$PIN'"
  exit 4
fi

# ------------------------------------------------------------ G3: map pool ---
[ -f "$POOLF" ] || die "⛔ REFUSING: no map pool manifest at $POOLF — cannot verify this host plays the live geometry." 5
POOL=$(tr ' ' '\n' < "$POOLF" | grep -v '^[[:space:]]*$' | sed 's/[[:space:]]//g' | sort)
HAVEMAPS=$(ls maps/*.map26 2>/dev/null | sed 's|.*/||; s|\.map26$||' | sort)
if [ "$POOL" != "$HAVEMAPS" ]; then
  say "⛔ REFUSING: maps/ does not match the shipped pool ($POOLF)."
  say "   only in the manifest : $(comm -23 <(printf '%s\n' "$POOL") <(printf '%s\n' "$HAVEMAPS") | tr '\n' ' ')"
  say "   only in maps/        : $(comm -13 <(printf '%s\n' "$POOL") <(printf '%s\n' "$HAVEMAPS") | tr '\n' ' ')"
  say "   A worker missing a live map, or holding a retired one, plays different"
  say "   geometry and says nothing about it. Re-push: orchestrate.sh push <host>"
  exit 5
fi
MAPS=()
for m in $HAVEMAPS; do MAPS[${#MAPS[@]}]=$m; done
NMAPS=${#MAPS[@]}
[ "$NMAPS" -gt 0 ] || die "⛔ REFUSING: empty map pool." 5

# ------------------------------------------------------------- G4: worklist ---
[ -f "$WORK" ] || die "⛔ REFUSING: no worklist at $WORK." 2
bad=0; nrows=0; has_null=0
while read -r SH TR CT TG SL; do
  case "${SH:-}" in ''|'#'*) continue;; esac
  nrows=$(( nrows + 1 ))
  [ -f "$TR/main.py" ] || { say "REFUSE: $SH treatment $TR has no main.py"; bad=1; }
  [ -f "$CT/main.py" ] || { say "REFUSE: $SH control   $CT has no main.py"; bad=1; }
  B=$(basename "$TR"); C=$(basename "$CT")
  case "$B" in *"$C"*) say "REFUSE: $SH basenames collide ($B vs $C) — scoring is a SUBSTRING match, so every control win would score as a treatment win"; bad=1;; esac
  case "$C" in *"$B"*) say "REFUSE: $SH basenames collide ($B vs $C) — scoring is a SUBSTRING match, so every control win would score as a treatment win"; bad=1;; esac
  case "$TG" in ''|*[!0-9]*) say "REFUSE: $SH target '$TG' is not a number"; bad=1;; esac
  case "$SL" in ''|*[!0-9]*) say "REFUSE: $SH seedbase '$SL' is not a number"; bad=1;; esac
  [ "$SH" = NULLHOST ] && has_null=1
done < "$WORK"
[ "$bad" -eq 0 ] || die "*** WORKLIST INVALID — nothing started ***" 2
[ "$nrows" -gt 0 ] || die "*** WORKLIST EMPTY — nothing to do ***" 2
if [ "$has_null" -eq 0 ]; then
  say "⛔ REFUSING: this worklist has NO NULLHOST row."
  say "   Without a per-host null cell nothing downstream can tell whether this"
  say "   hardware measures our game — and the reader will exclude every row this"
  say "   host produces. Regenerate: orchestrate.sh gen <host> ..."
  exit 6
fi

mkdir -p "$OUT"
say "WORKER up. host=$(hostname) ncpu=$NCPU workers=$WORKERS load_ceil=$LOAD_CEIL engine=$HAVE(pin $PIN) maps=$NMAPS work=$WORK out=$OUT"

# ══════════════════════════════════════════════════════════════════════════════
# ONE SHARD
# ══════════════════════════════════════════════════════════════════════════════
run_shard() {
  SHARD=$1; TREAT=$2; CTRL=$3; TARGET=$4; SEEDBASE=$5
  ROWS=$OUT/${SHARD}.tsv
  HB=$OUT/${SHARD}.heartbeat
  DONEF=$OUT/${SHARD}.COMPLETE

  [ -f "$DONEF" ] && { say "SKIP $SHARD — already COMPLETE"; return 0; }
  B=$(basename "$TREAT")

  # HEADER + TARGET-BEFORE-FIRST-GAME. A partial run must never read as complete.
  [ -f "$ROWS" ] || printf 'ts%sshard%sgame%smap%sseed%sseat%swinner%scond%sturns\n' \
      "$T" "$T" "$T" "$T" "$T" "$T" "$T" "$T" > "$ROWS"
  n=$(( $(wc -l < "$ROWS") - 1 )); [ "$n" -lt 0 ] && n=0
  printf '%s%s%s%s%s%s%s%s%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$T" "$n" "$T" "$TARGET" "$T" "$SHARD" "$T" STARTING > "$HB"
  [ "$n" -gt 0 ] && say "RESUMING $SHARD at $n/$TARGET"
  say "SHARD $SHARD  $B vs $(basename "$CTRL")  target=$TARGET seedbase=$SEEDBASE"

  # NOWINNER tally is recomputed from the ROWS, not carried in memory — a resumed
  # shard must inherit the abort evidence, not start it over.
  nowin=$(awk -F"$T" 'NR>1 && $7=="NOWINNER"{c++} END{print c+0}' "$ROWS")
  per_seed=$(( 2 * NMAPS ))
  TMPD=$(mktemp -d "${TMPDIR:-/tmp}/fcw.XXXXXX") || die "cannot mktemp" 1
  # shellcheck disable=SC2064
  trap "rm -rf '$TMPD'" EXIT

  while [ "$n" -lt "$TARGET" ]; do
    curfew_wait
    if [ -f "$STOPF" ]; then
      printf '%s%s%s%s%s%s%s%s%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$T" "$n" "$T" "$TARGET" "$T" "$SHARD" "$T" STOPPED > "$HB"
      say "STOP file present — $SHARD halted at $n/$TARGET. Rows are KEPT."
      rm -rf "$TMPD"; trap - EXIT
      return 10
    fi
    L1=$(load1)
    if awk -v a="$L1" -v b="$LOAD_CEIL" 'BEGIN{exit !(a>b)}'; then
      say "hold: load $L1 > ceiling $LOAD_CEIL — waiting 30s ($SHARD at $n/$TARGET)"
      sleep 30
      continue
    fi

    rm -f "$TMPD"/*
    # ⭐⭐ ROLLING POOL, NOT A FIXED BATCH (2026-08-15). This loop used to launch
    # exactly WORKERS games and then `wait` for ALL of them. A batch therefore
    # cost max(duration), while the useful work is sum(duration)/N = mean --
    # and game length here is wildly skewed (measured on 104,145 remote rows:
    # mean 301 turns, median 220, p90 617, max 1000).
    #
    # MEASURED STRAGGLER TAX, by resampling that real distribution:
    #     WORKERS=6   mean/max = 0.513  ->  49% of capacity lost
    #     WORKERS=10  mean/max = 0.423  ->  58% of capacity lost
    # ⇒ ws1 at WORKERS=10 was burning MORE of its allocation on the barrier than
    # ws2 at WORKERS=6, which is exactly why a 10-core host was out-produced by
    # a 6-core one (2,769 vs 2,402 rows/h -- 87%, where hardware alone predicted
    # ws1 ahead). The anomaly and the tax are the same fact.
    #
    # So: keep WORKERS games IN FLIGHT and start a replacement as each finishes,
    # instead of draining to zero every N games. The barrier now happens once per
    # POOL_BATCH games rather than once per WORKERS games.
    #
    # ⛔ WHAT IS DELIBERATELY UNCHANGED, because these are the invariants that
    # make the rows trustworthy:
    #   * every game still writes its OWN file in $TMPD, keyed by index. No game
    #     ever appends to $ROWS -- that is still done once, by this loop, after
    #     the drain. Interleaved `>>` from N parallel games is unparseable and
    #     invisible until the morning read-out.
    #   * STOP and LOAD_CEIL are still checked BEFORE every launch, so the
    #     operator's kill switch and the oversubscription guard respond at the
    #     same granularity as before (per game, not per batch).
    #   * the heartbeat, the row count and the NOWINNER abort still run on the
    #     drained batch, from the ROW COUNT, which is the only truth.
    batch=$(( WORKERS * POOL_BATCH_MULT ))
    [ "$batch" -lt "$WORKERS" ] && batch=$WORKERS
    [ $(( n + batch )) -gt "$TARGET" ] && batch=$(( TARGET - n ))
    i=0
    inflight=0
    pool_halt=0
    while [ "$i" -lt "$batch" ] || [ "$inflight" -gt 0 ]; do
      # --- top the pool up to WORKERS, checking the guards before each launch --
      while [ "$inflight" -lt "$WORKERS" ] && [ "$i" -lt "$batch" ] && [ "$pool_halt" -eq 0 ]; do
        if [ -f "$STOPF" ]; then pool_halt=1; break; fi
        # THROTTLE THE LOAD PROBE. `load1` shells out (uptime|sed|awk on non-Linux)
        # and calling it before EVERY launch cost 0.43s per 40 games when measured
        # -- overhead I added with the pool and did not notice until an A/B came
        # out the WRONG WAY. Load average is a 1-minute mean; sampling it more
        # than once a second cannot tell you anything the previous sample did not.
        _nowsec=$(date +%s)
        if [ "$_nowsec" != "${_last_load_probe:-}" ]; then
          _last_load_probe=$_nowsec
          L1=$(load1)
        fi
        if awk -v a="${L1:-0}" -v b="$LOAD_CEIL" 'BEGIN{exit !(a>b)}'; then
          # Do not launch into an over-loaded box. Let the pool drain a slot and
          # re-check; `--tle 10` is WALL-CLOCK, so oversubscription corrupts rows
          # rather than merely slowing them (the SALTREF2 defect).
          break
        fi
      idx=$(( n + i ))
      ( # ---- ONE GAME. Same cycling ORDER as overnight.sh: seed { map { A,B } }
        k=$(( idx % per_seed ))
        seed=$(( SEEDBASE + idx / per_seed ))
        M=${MAPS[$(( k / 2 ))]}
        if [ $(( k % 2 )) -eq 0 ]; then ORD=A; else ORD=B; fi
        # --tle 10 IS NOT OPTIONAL: the default is 0 = NO CPU LIMIT and the
        # platform enforces 10ms. A run without it measures a chassis that does
        # not exist. --replay /dev/null: dozens of parallel games otherwise share
        # ONE default replay path.
        # ⛔ `</dev/null` IS LOAD-BEARING, NOT TIDINESS. These game-runners are
        # spawned from inside `while read ... done < "$WORK"`, so they inherit
        # the WORKLIST as stdin. Any child that read a byte would silently eat
        # rows out of the schedule and the shard would just... skip work.
        if [ "$ORD" = A ]; then
          OUTP=$($TIMEOUT "$FC" run "$TREAT" "$CTRL" "maps/$M.map26" --seed "$seed" --tle 10 --replay /dev/null 2>&1 </dev/null)
        else
          OUTP=$($TIMEOUT "$FC" run "$CTRL" "$TREAT" "maps/$M.map26" --seed "$seed" --tle 10 --replay /dev/null 2>&1 </dev/null)
        fi
        L=$(printf '%s\n' "$OUTP" | grep -i "Winner:" | head -1)
        TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        if [ -z "$L" ]; then
          printf '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s\n' "$TS" "$T" "$SHARD" "$T" "$idx" "$T" "$M" "$T" "$seed" "$T" "$ORD" "$T" NOWINNER "$T" - "$T" - \
            > "$TMPD/$(printf '%012d' "$idx")"
          exit 0
        fi
        TN=${L##*turn }; TN=${TN%%[!0-9]*}; [ -z "$TN" ] && TN=-
        COND=core_destroyed
        case "$L" in *tiebreak*) COND=tiebreak;; esac
        case "$L" in *"$B"*) WIN=T;; *) WIN=C;; esac
        printf '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s\n' "$TS" "$T" "$SHARD" "$T" "$idx" "$T" "$M" "$T" "$seed" "$T" "$ORD" "$T" "$WIN" "$T" "$COND" "$T" "$TN" \
          > "$TMPD/$(printf '%012d' "$idx")"
      ) &
        i=$(( i + 1 ))
        inflight=$(( inflight + 1 ))
      done
      if [ "$inflight" -eq 0 ]; then
        # Nothing running and nothing launchable: either halted, or the load
        # ceiling is holding us off. Sleep rather than spin.
        [ "$pool_halt" -eq 1 ] && break
        [ "$i" -ge "$batch" ] && break
        sleep 5
        continue
      fi
      # `wait -n` returns as soon as ONE job finishes -- that is the whole point.
      # bash >= 4.3; the shebang is bash and both hosts run bash 5.
      wait -n 2>/dev/null || wait
      inflight=$(( inflight - 1 ))
    done
    wait

    # ⛔ APPEND IN INDEX ORDER, AFTER THE BATCH — never let N parallel games
    # `>>` the same file. Interleaved partial lines would be unparseable and the
    # corruption is invisible until the morning read-out.
    got=0
    for f in $(ls "$TMPD" 2>/dev/null | sort); do
      cat "$TMPD/$f" >> "$ROWS"
      got=$(( got + 1 ))
    done
    if [ "$got" -ne "$batch" ]; then
      say "⚠ $SHARD batch produced $got/$batch rows — a game-runner died without writing. Continuing from the ROW COUNT, which is the only truth."
    fi
    n=$(( $(wc -l < "$ROWS") - 1 ))
    nowin=$(awk -F"$T" 'NR>1 && $7=="NOWINNER"{c++} END{print c+0}' "$ROWS")
    printf '%s%s%s%s%s%s%s%s%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$T" "$n" "$T" "$TARGET" "$T" "$SHARD" "$T" RUNNING > "$HB"

    # A COMPLETE MARKER MUST CERTIFY GAMES PLAYED, NOT LOOP ITERATIONS.
    if [ "$n" -ge 200 ] && [ $(( nowin * 100 )) -gt "$n" ]; then
      say "ABORT $SHARD: $nowin/$n NOWINNER (>1%) — fixture is broken."
      printf '%s%s%s%s%s%s%s%s%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$T" "$n" "$T" "$TARGET" "$T" "$SHARD" "$T" ABORTED_NOWINNER > "$HB"
      rm -rf "$TMPD"; trap - EXIT
      return 3
    fi
  done

  printf '%s%s%s%s%s%s%s%s%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$T" "$n" "$T" "$TARGET" "$T" "$SHARD" "$T" COMPLETE > "$HB"
  printf '%s %s reached %s/%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$SHARD" "$n" "$TARGET" > "$DONEF"
  say "SHARD $SHARD COMPLETE $n/$TARGET"
  rm -rf "$TMPD"; trap - EXIT
  return 0
}

# `timeout` is coreutils (present on any Linux); on a mac without it we run bare
# rather than refuse — but SAY SO, because without --tle a hung bot blocks the
# substitution forever and this is the guard that would have caught it.
if command -v timeout >/dev/null 2>&1; then TIMEOUT="timeout 120"
elif command -v gtimeout >/dev/null 2>&1; then TIMEOUT="gtimeout 120"
else TIMEOUT=""; say "⚠ no timeout(1) on this host — games run unbounded. Install coreutils."; fi

# ══════════════════════════════════════════════════════════════════════════════
# NULLHOST FIRST, THEN THE WORKLIST IN ORDER
# ══════════════════════════════════════════════════════════════════════════════
rc_any=0
run_by_id() {
  want=$1
  while read -r SH TR CT TG SL; do
    case "${SH:-}" in ''|'#'*) continue;; esac
    [ "$SH" = "$want" ] || continue
    run_shard "$SH" "$TR" "$CT" "$TG" "$SL"
    return $?
  done < "$WORK"
  return 127
}

if [ ! -f "$OUT/NULLHOST.COMPLETE" ]; then
  say "NULLHOST-FIRST: no completed $OUT/NULLHOST.tsv on this host — running the null cell before anything else."
  say "  (On different hardware the null is the only instrument that can catch a bent"
  say "   ruler. --tle 10 is a WALL-CLOCK budget, so a faster/slower core changes which"
  say "   turns time out. A host whose null is not ~50% is not measuring our game.)"
  run_by_id NULLHOST; rc=$?
  if [ "$rc" -eq 10 ]; then say "stopped during NULLHOST"; exit 0; fi
  if [ "$rc" -ne 0 ]; then die "⛔ NULLHOST did not complete (rc=$rc). REFUSING to run any other shard: every row this host produced would be uncertifiable." 7; fi
  NT=$(awk 'END{print NR-1}' "$OUT/NULLHOST.tsv")
  if [ "$NT" -lt 400 ]; then
    say "⚠ NULLHOST target is $NT rows — UNDER THE 400-ROW CERTIFICATION FLOOR."
    say "   The reader will NOT certify this host at n<400 and will exclude its rows"
    say "   from every pooled rate. This is fine for a smoke test and wrong for a run."
  fi
fi

while read -r SH TR CT TG SL; do
  case "${SH:-}" in ''|'#'*) continue;; esac
  [ "$SH" = NULLHOST ] && continue
  curfew_wait
  if [ -f "$STOPF" ]; then say "STOP file present — launching no further shards."; break; fi
  run_shard "$SH" "$TR" "$CT" "$TG" "$SL"; rc=$?
  [ "$rc" -eq 10 ] && { say "STOP during $SH — halting."; break; }
  [ "$rc" -ne 0 ] && rc_any=$rc
done < "$WORK"

say "WORKER done. (a shard that failed is LOGGED AND LEFT — nothing here relaunches anything)"
exit "$rc_any"
