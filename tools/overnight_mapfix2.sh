#!/usr/bin/env zsh
# OVERNIGHT SHARD RUNNER — heartbeat, completion marker, and assertions.
#
#   tools/overnight.sh <shard_id> <treatment_dir> <control_dir> <target_games> <seed_lo>
#
# ⛔ EVERY PIECE OF THIS IS A NAMED FAILURE, NOT A PRECAUTION.
#
# 1. HEARTBEAT, overwritten every game: `ts games_done TARGET_N shard_id`.
#    **TARGET_N IS WRITTEN BEFORE THE FIRST GAME**, so a partial run can never
#    read as complete. This repo's rule: silent truncation reads as "covered
#    everything".
#
# 2. COMPLETION MARKER, written ONLY on reaching TARGET_N. The morning read-out
#    MUST REFUSE to pool a shard with no marker. A shard that died at hour one
#    and a shard that finished are otherwise byte-identical in their logs --
#    which is the same failure as ship_watch printing healthy lines off a stale
#    tape.
#
# 3. NO LLM DURING THE RUN. Magnus asked for "a sonnet agent that makes sure it
#    works well but doesn't steal too many tokens"; the honest answer is that
#    overnight failures here are ASSERTION-SHAPED, not judgment-shaped. A dead
#    shard needs a restart, not a thought. Healthy night = zero LLM calls.
#
# 4. SEAT-BALANCED BY CONSTRUCTION -- both seats every seed x map, same as
#    h2h.sh. Seat is worth 7.6pp on BYTE-IDENTICAL arms, ~2.5x the largest arm
#    effect ever screened here, so an unbalanced cut measures SEAT.
#
# 5. RESULTS APPENDED PER GAME as a TSV row, not aggregated in memory. A run
#    killed at hour five keeps five hours of games.
#
# NOISE_ON IS DELIBERATELY LEFT TRUE (gate.py would FAIL it): at n>=7,000 we do
# not need pairing's variance reduction and we want THE BEHAVIOUR WE SHIP.
# Recorded as an explicit override in docs/PLAN-overnight-2026-08-11.md, not a
# bypass.
set -u
T=$'\t'      # REAL tab. `print -r` does NOT interpret \t in zsh, and a
            # literal backslash-t makes every row unparseable in the morning.
SHARD=${1:?shard_id}
TREAT=${2:?treatment dir}
CTRL=${3:?control dir}
TARGET=${4:?target games}
SEEDLO=${5:-1}

# ⛔ `${OUT:-...}` NOT a bare assignment, s32. This was hardcoded, so an
# `OUT=... zsh tools/runner.sh` invocation SILENTLY WROTE TO THE LIVE DIRECTORY.
# Measured the hard way: a throwaway watchdog fixture, believed isolated by that
# exact env var, instead ran against the live run -- created `FX.*` files beside
# five live shards, appended to their ALERT and watch.log, and launched a stray
# shard. Harmless only by luck (its bots did not exist, so every game recorded
# NOWINNER). **The trap had ALREADY been found in the sibling script an hour
# earlier and worked around in the launcher rather than fixed at the source --
# so the workaround protected the launcher and left the next caller exposed.**
# Fixing the source is what makes a test fixture possible at all: a guard that
# cannot be exercised in isolation cannot be driven to both verdicts.
OUT=${OUT:-scratchpad/overnight}
mkdir -p $OUT
HB=$OUT/${SHARD}.heartbeat
ROWS=$OUT/${SHARD}.tsv
DONEF=$OUT/${SHARD}.COMPLETE
FC=.venv/bin/fcode
# ⛔ RE-POINTED 2026-08-13 AT THE LIVE 15-MAP POOL (organisers rotated it today).
# The old set was (antler atoll drumlin fjordgate heart hive meander nordkap) and
# FOUR of those eight -- atoll, heart, hive, meander -- are NO LONGER IN THE POOL,
# so half of every battery result predating this line is on retired geometry.
# The pool also added a size class we had never played: five 30x30 maps (area 900)
# against a previous maximum of 625. Targets should be multiples of 30 (15 maps x
# 2 seats) for exact map/seat balance; the old multiples of 16 no longer balance.
MAPS=(valkyrie glacierkeep)
MAPDIR=${MAPDIR:-maps}  # MAPFIX variant 2026-08-14: POST-PATCH geometry from an isolated dir so maps/ stays frozen mid-shard
B=$(basename $TREAT); C=$(basename $CTRL)

# IDENTICAL BASENAMES ARE UNSCORABLE -- fcode names the winner by basename, so a
# bot run against itself matches the treatment pattern in EVERY game and reads
# 100%. The honest null is a RENAMED copy.
# ⛔ SUBSTRING, NOT EQUALITY. Scoring is `case "$L" in *"$B"*`, so
# `_v150cb` vs `_v150cbturret` passes an equality guard and then EVERY control
# win scores as a treatment win -- reading ~100%. Both colliding names exist in
# bots/ today and a 9-arm batch is exactly where prefix variants get made.
if [[ $B == $C || $B == *$C* || $C == *$B* ]]; then
  print "REFUSING: basenames collide ('$B' vs '$C') -- substring match makes this unscorable."
  exit 2
fi

rm -f $DONEF
print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ)${T}0${T}$TARGET${T}$SHARD${T}STARTING" > $HB
[[ -f $ROWS ]] || print -r -- "ts${T}shard${T}game${T}map${T}seed${T}seat${T}winner${T}cond${T}turns" > $ROWS

# ⛔ RESUME, DO NOT RESTART FROM ZERO. The watchdog restarts a dead shard; the
# first version reset n=0 and APPENDED, so a restart at 3,000 left 10,300 rows
# skewed to low seeds while the marker still read 7300/7300. Nothing compared
# wc -l to n. Now the row count IS the progress.
nowin=0
existing=$(( $(wc -l < $ROWS) - 1 ))
(( existing < 0 )) && existing=0
n=$existing
seed=$(( SEEDLO + n / 4 ))  # 2 maps x 2 seats per cycle
(( n > 0 )) && print "RESUMING $SHARD at $n/$TARGET (seed $seed)"
while (( n < TARGET )); do
  for M in $MAPS; do
    for ORD in A B; do
      (( n >= TARGET )) && break
      # ⛔ --tle 10 IS NOT OPTIONAL. The default is 0 = NO CPU LIMIT, and the
      # platform enforces 10ms. Measured 2026-08-11: _v145bestfit wins 6/6 with
      # the limit OFF and loses 5/6 with it ON -- so a run without --tle
      # measures a chassis that does not exist. `docs/tooling.md:18` already
      # said this and both h2h.sh and this file ignored it.
      # --replay /dev/null: nine shards otherwise share ONE default replay path
      # (disk is at 95%), which is the unclosed root cause behind D65.
      # timeout: without --tle a hung bot blocks the substitution forever.
      if [[ $ORD == A ]]; then OUTP=$(timeout 120 $FC run $TREAT $CTRL $MAPDIR/$M.map26 --seed $seed --tle 10 --replay /dev/null 2>&1)
      else                     OUTP=$(timeout 120 $FC run $CTRL $TREAT $MAPDIR/$M.map26 --seed $seed --tle 10 --replay /dev/null 2>&1); fi
      L=$(print -r -- "$OUTP" | grep -i "Winner:" | head -1)
      if [[ -z $L ]]; then
        print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ)${T}$SHARD${T}$n${T}$M${T}$seed${T}$ORD${T}NOWINNER${T}-${T}-" >> $ROWS
        nowin=$((nowin+1))
        n=$((n+1))
        # ⛔ A COMPLETE MARKER MUST CERTIFY GAMES PLAYED, NOT LOOP ITERATIONS.
        # A NOWINNER row increments n, so a broken bot or a missing map would
        # burn the whole target in minutes and still write COMPLETE.
        if (( n >= 200 && nowin * 100 > n )); then
          print "ABORT $SHARD: $nowin/$n NOWINNER (>1%) -- fixture is broken."
          print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ)${T}$n${T}$TARGET${T}$SHARD${T}ABORTED_NOWINNER" > $HB
          exit 3
        fi
        continue
      fi
      TN=${L##*turn }; TN=${TN%%[!0-9]*}
      COND="core_destroyed"; [[ $L == *"tiebreak"* ]] && COND="tiebreak"
      case "$L" in *"$B"*) WIN=T;; *) WIN=C;; esac
      print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ)${T}$SHARD${T}$n${T}$M${T}$seed${T}$ORD${T}$WIN${T}$COND${T}${TN:--}" >> $ROWS
      n=$((n+1))
      print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ)${T}$n${T}$TARGET${T}$SHARD${T}RUNNING" > $HB
    done
  done
  seed=$((seed+1))
done

# COMPLETION MARKER -- only here, only on reaching TARGET.
print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ)${T}$n${T}$TARGET${T}$SHARD${T}COMPLETE" > $HB
print -r -- "$(date -u +%Y-%m-%dT%H:%M:%SZ) $SHARD reached $n/$TARGET" > $DONEF
print "SHARD $SHARD COMPLETE $n/$TARGET"
