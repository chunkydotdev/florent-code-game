#!/usr/bin/env zsh
# DOSE — does the plank we built ACTUALLY FIRE? Measure it before reading a rate.
#
#   tools/dose.sh <treatment_dir> <control_dir> <tag> [games] [map]
#   tools/dose.sh bots/_v178salt bots/_v169launchlate160 SALT 3
#   tools/dose.sh bots/_v187saltidle_f bots/_v169launchlate160 'SALT|S48' 8 nordkap
#
# ===== WHY THIS EXISTS =====
# Magnus, 2026-08-13: *"we cant see if a play we think we built actually happens
# … we can use [legs] to verify something we built actually happens, and then run
# the local games to see if they make a difference."*
#
# He is right about the workflow and the mechanism is worth stating exactly,
# because it is the opposite of what everyone assumes:
#
#   * A bot's `print()` goes INTO THE REPLAY. `tools/overnight.sh:102` runs every
#     local game with `--replay /dev/null`, so **our local batteries are
#     dose-blind BY OUR OWN CONFIGURATION, not by a platform limit.**
#   * `stderr` DOES reach the console locally (an engine probe emitted 1,984
#     lines that way), so instrumentation is possible — we simply never kept it.
#   * On the PLATFORM the reverse holds: our stdout is stripped from downloaded
#     replays (measured 30,664 of 30,664 empty), while ENGINE-side entity events
#     survive into the corpus.
#
# ⇒ Locally, keeping the replay is free and answers the question in ~15 s/game.
#
# ===== THE TWO FALSE ZEROS THIS EXISTS TO PREVENT, both real, both mine =====
# 1. A dose check over five arms read **0 for every one of them, including the
#    PARENT** — because the replay went to /dev/null. The grep could not have
#    returned anything else. Caught only because zero-for-the-parent was not
#    plausible; had the parent been excluded it would have published.
# 2. A dose check read **0 for one arm alone** — because that arm sets
#    `LOKI_SALT_LOG = False`. **The instrument was reading its own switch.**
#    With logging forced on: 2,571 funnel events over 8 games.
#
# ⇒ THIS SCRIPT REFUSES A BARE ZERO. If the treatment emits nothing it says
#   UNPROVEN and tells you the two things that produce a structural zero, rather
#   than reporting "dose 0" as though it were a measurement. **A check that has
#   never produced the other verdict has not been seen to check.**
#
# ===== WHAT A DOSE IS FOR =====
# A currency reading on an UNDOSED arm is not a null — it is a NON-EXPERIMENT.
# And a LOW-dose arm's rate is confounded with its dose: `_v191saltbaronly` read
# 46.89% at n=868 and doses **2.7 events/game against 19-79 for its siblings**,
# low BY CONSTRUCTION, so no n makes that number a mechanism verdict.
set -u
TREAT=${1:?treatment bot dir}
CTRL=${2:?control bot dir}
TAG=${3:?grep pattern for the log tag, e.g. SALT}
GAMES=${4:-3}
MAP=${5:-antler}

cd ${0:A:h:h} || exit 1
FC=.venv/bin/fcode
TMP=$(mktemp -d) || exit 1
trap 'rm -rf $TMP' EXIT

[[ -d $TREAT ]] || { print "FATAL: $TREAT is not a directory"; exit 2 }
[[ -d $CTRL  ]] || { print "FATAL: $CTRL is not a directory";  exit 2 }
[[ -f maps/$MAP.map26 ]] || { print "FATAL: maps/$MAP.map26 not found"; exit 2 }

# ---- THE LOG-FLAG PRE-CHECK. Defect 2 above, made impossible to repeat. ------
# A `*_LOG = False` in the treatment guarantees a zero that says nothing about
# behaviour. Report it BEFORE running, not as a puzzle afterwards.
offflags=$(grep -hE '^[A-Z_]*LOG[A-Z_]* *= *False' $TREAT/*.py 2>/dev/null)
if [[ -n $offflags ]]; then
  print "⚠ LOG FLAGS OFF IN THE TREATMENT — a zero below would be THIS, not behaviour:"
  print -r -- "$offflags" | sed 's/^/    /'
  print "  (flip them in a probe COPY and re-run; never edit the measured arm)"
fi

print "DOSE: $TREAT vs $CTRL   tag=/$TAG/   games=$GAMES   map=$MAP"
total=0; empty=0
for i in $(seq 1 $GAMES); do
  seed=$(( 990000 + i ))
  R=$TMP/g$i.replay
  $FC run $TREAT $CTRL maps/$MAP.map26 --seed $seed --tle 10 --replay $R >/dev/null 2>&1
  if [[ ! -s $R ]]; then
    print "  game $i seed=$seed  ⚠ NO REPLAY WRITTEN — cannot count"
    empty=$(( empty + 1 )); continue
  fi
  n=$(strings $R 2>/dev/null | grep -cE "$TAG" || true)
  total=$(( total + n ))
  print "  game $i seed=$seed  events=$n"
done

ran=$(( GAMES - empty ))
if (( ran == 0 )); then
  print "RESULT: BLIND — no replay was written at all. Nothing measured."
  exit 3
fi

avg=$(awk -v t=$total -v g=$ran 'BEGIN{printf "%.1f", t/g}')
print "TOTAL: $total events over $ran game(s) = $avg/game"

# ---- REFUSE A BARE ZERO -----------------------------------------------------
if (( total == 0 )); then
  print ""
  print "⛔ RESULT: UNPROVEN, **NOT** 'dose 0'."
  print "   A zero here has three structural sources before it has a behavioural one:"
  print "     1. the tag /$TAG/ does not match what the bot actually prints"
  print "     2. a *_LOG flag is False in the treatment (see the pre-check above)"
  print "     3. the plank's gate never opened on THIS map/seed set — try more maps"
  print "   Rule out all three before reading this as 'the plank does not fire'."
  exit 4
fi
print ""
print "✅ DOSED. The arm's rate may now be read as a rate rather than a non-experiment."
print "   ⚠ A LOW dose is still confounded with the mechanism: compare this /game"
print "     figure against the arm's SIBLINGS before calling any rate a verdict."
