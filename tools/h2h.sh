#!/usr/bin/env zsh
# HEAD-TO-HEAD vs the previous line iteration. `tools/h2h.sh <botdir> [seeds] [maps]`
#
# WHY THIS EXISTS (Magnus, 2026-08-11): "A good new bot should be showing signs
# early in head to head games." And: "Loki is a type of bot that can be run
# against itself to find improvements."
#
# ⛔ IT EXISTS BECAUSE I HAD DRIFTED OFF LOCAL GAMES ENTIRELY. Both dose checks
# I ran on 2026-08-11 used `bots/_det_opp_v63` -- one of OUR OWN PROBES, the
# fixture `PROGRAMME.md` says lies in a known direction (five probes share a
# `best_core or best_any` short-circuit; ZERO of our forward turrets died in 480
# arena games against 46.9% on the ladder). I read "prototypes go at live teams,
# not at our own probes" as "do not run local games", which is not what it says.
#
# **THE RIGHT LOCAL FIXTURE WAS ALWAYS IN THE PROGRAMME: `COMPARE_AGAINST:
# previous_line_iteration`. v104 is a real, current, competent bot and it does
# NOT have the probe defect.** Self-play against it is free, instant, unlimited,
# and needs no rate-limit slot.
#
# FIRST USE, and it paid for itself immediately: LOKI-22 (the rush flag flipped
# back on) went **16 wins / 64 games = 25%** across 8 maps x both seats x 4
# seeds -- reproducing a 2026-08-09 arena refutation on a fixture without the
# probe bias, and saving the live window I was about to spend on it.
#
# ⚠ WHAT IT IS AND IS NOT. This is a PRIORITISATION instrument, not a D12
# closure: deterministic, self-play, and self-play is not the field.
# `FIXTURE_OF_RECORD: live_unrated` is unchanged. A plank that dies here is
# demoted, not retired; a plank that lives here has earned a live window.
# BOTH SEATS ARE ALWAYS PLAYED -- a one-seat result is a seat measurement.
set -u
BOT=${1:?usage: h2h.sh <botdir> [seeds] [maps]}
CTRL=${CTRL:-bots/_v130loki13}
SEEDS=${2:-"7 11 23 41"}
MAPS=${3:-"antler atoll drumlin fjordgate heart hive meander nordkap"}
FC=.venv/bin/fcode
B=$(basename $BOT)
C=$(basename $CTRL)
# ⛔ IDENTICAL BASENAMES ARE UNSCORABLE. `fcode` names the winner by basename, so
# a bot run against itself matches the treatment pattern in EVERY game and reads
# 100%. The self-check caught exactly that on this file's first run. The honest
# null is a RENAMED COPY of the control, which is byte-identical in behaviour and
# distinguishable on the wire.
if [[ $B == $C ]]; then
  print "REFUSING: treatment and control share the basename '$B'."
  print "  fcode reports the winner by basename, so every game would score as a"
  print "  treatment win. Copy the control to a new directory name for a null run."
  print "H2H_RESULT: UNSCORABLE 0/0"
  exit 2
fi
W=0; N=0; KILLW=0; KILLL=0; R1000=0
WA=0; NA=0; WB=0; NB=0
for S in ${=SEEDS}; do
  for M in ${=MAPS}; do
    for ORD in A B; do
      if [[ $ORD == A ]]; then OUT=$($FC run $BOT $CTRL maps/$M.map26 --seed $S 2>&1)
      else                     OUT=$($FC run $CTRL $BOT maps/$M.map26 --seed $S 2>&1); fi
      L=$(print -r -- "$OUT" | grep -i "Winner:" | head -1)
      [[ -z $L ]] && { print -r -- "  !! no winner line: $M seed $S seat $ORD"; continue; }
      N=$((N+1))
      if [[ $ORD == A ]]; then NA=$((NA+1)); else NB=$((NB+1)); fi
      case "$L" in *"$B"*) W=$((W+1)); [[ $ORD == A ]] && WA=$((WA+1)) || WB=$((WB+1))
                          [[ $L == *"Core destroyed"* ]] && KILLW=$((KILLW+1));;
                   *)                 [[ $L == *"Core destroyed"* ]] && KILLL=$((KILLL+1));; esac
      [[ $L == *"turn 1000"* ]] && R1000=$((R1000+1))
    done
  done
done
print ""
print "H2H  $B  vs  $C"
print "  games $N   (both seats always played)"
print "  WINS  $W = $(( N ? 100*W/N : 0 ))%"
print "  core kills FOR $KILLW   AGAINST $KILLL   r1000 (a DEFEAT either way) $R1000"
# PER-SEAT, because a pooled rate hides a seat effect and the NULL control read
# 44% rather than 50% on 60 games. If a byte-identical copy wins far more from
# one seat than the other, the engine or the harness is asymmetric and every
# screen verdict is measured against a bent ruler.
print "  seat A (treatment first)  $WA/$NA     seat B (treatment second)  $WB/$NB"
# GATE ON THIS LINE, NEVER ON $? -- the natural `h2h.sh ... | tail` makes $? the
# pipe's, which is always 0. Repo standing rule.
print "H2H_RESULT: $B $W/$N"
