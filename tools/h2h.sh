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
# ⭐ THE NULL IS A STANDING ASSET, NOT A PER-LEG ARTEFACT. Build it ONCE at full
# power and every later screen is measured against a settled bar instead of
# re-litigating one. The 64-game null (32/64 = 50.0%) is committed; a 4,096-game
# null is running for the same reason. **A treatment run belongs to its plank and
# dies with it; the null belongs to the harness and outlives every plank.**
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
typeset -A MW MN
for S in ${=SEEDS}; do
  for M in ${=MAPS}; do
    for ORD in A B; do
      if [[ $ORD == A ]]; then OUT=$($FC run $BOT $CTRL maps/$M.map26 --seed $S 2>&1)
      else                     OUT=$($FC run $CTRL $BOT maps/$M.map26 --seed $S 2>&1); fi
      L=$(print -r -- "$OUT" | grep -i "Winner:" | head -1)
      [[ -z $L ]] && { print -r -- "  !! no winner line: $M seed $S seat $ORD"; continue; }
      N=$((N+1))
      if [[ $ORD == A ]]; then NA=$((NA+1)); else NB=$((NB+1)); fi
      MN[$M]=$(( ${MN[$M]:-0} + 1 ))
      case "$L" in *"$B"*) W=$((W+1)); MW[$M]=$(( ${MW[$M]:-0} + 1 )); [[ $ORD == A ]] && WA=$((WA+1)) || WB=$((WB+1))
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
# PER-MAP, because a pooled 8-map rate can be "harmful on short maps, neutral on
# long" and read identically to "harmful everywhere". The rush was measured at
# -35.4pp on SHORT maps (p=0.0005) and NULL on long ones in 2026-08-09's paired
# battery -- so a pooled number hides the only fact that would change its status.
# Free: the split is already in the games we just played.
print -n "  per map: "
for m in ${=MAPS}; do print -n "$m ${MW[$m]:-0}/${MN[$m]:-0}  "; done
print ""
# GATE ON THIS LINE, NEVER ON $? -- the natural `h2h.sh ... | tail` makes $? the
# pipe's, which is always 0. Repo standing rule.
# ⛔ POWER WARNING, AND IT IS NOT DECORATION. At n=24 the smallest count that
# separates from a 50% null at p<0.05 is 7/24 -- so 10/24 (41%) and 14/24 (58%)
# are BOTH indistinguishable from doing nothing. Measured the hard way on
# 2026-08-11: LOKI_FWD_GUN_CAP 3->6 read 14/24 = 58% and was reported as "the
# first thing above the null"; at n=64 it read 32/64 = EXACTLY 50%. The null
# control itself read 44% at n=36 and 50.0% at n=64. **Two false signals from
# the same instrument in one hour, both from small n.**
if (( N < 64 )); then
  print ""
  print "  ⚠ UNDERPOWERED: n=$N. Against a 50% null only an extreme count separates"
  print "    at p<0.05 (at n=24 that is <=7 or >=17). ANYTHING BETWEEN IS NOISE —"
  print "    do not rank it, do not call it positive. Re-run at n>=64 before quoting."
fi
print "H2H_RESULT: $B $W/$N"
