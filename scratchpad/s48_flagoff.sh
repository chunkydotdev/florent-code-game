#!/bin/zsh
# s48 BUILDER flag-off equivalence: is <arm> with its plank flag OFF the same
# bot as the base, move for move?
#
# THE METHOD, and it needs a precondition this repo already documents
# (tools/det.py): the engine is NOT reproducible as shipped. Base vs base on
# one (map, seed) gave turns 226 / 287 / 358 over three runs. Two causes, both
# removable: NOISE_ON (doctrine.py:474 -- `random.Random().randrange(97)`, an
# UNSEEDED per-unit salt, deliberate decision noise) and CPU-kill timing. With
# NOISE_ON=False and --tle 0 the same pairing returns byte-identical replays,
# so the comparison below is on replay SHA-256, not on a summary.
#
# ⛔ AND THE INSTRUMENT IS DRIVEN TO THE OTHER VERDICT ON EVERY CELL. The same
# harness runs the arm with its flag ON; those hashes MUST differ from the
# base. A hash comparison that has only ever printed MATCH has not been seen to
# check anything -- if the arm's flag were unwired, or the plank never reached,
# flag-off equivalence would pass for the wrong reason and this is the only
# line that catches it.
#
# Usage: zsh scratchpad/s48_flagoff.sh <arm_dir_name> <FLAG_NAME>
set -u
ARM=${1:?arm bot dir name}
FLAG=${2:?doctrine flag name, e.g. LOKI_ECOMMIT_ON}
BASE=_v468kladturbo
OPP=opp_v63
MAPS=(yulerune icefloe drumlin eider)
SEEDS=(11 22)
FC=.venv/bin/fcode

mk() {  # mk <src> <dst> <flagvalue|->
  rm -rf bots/$2; cp -r bots/$1 bots/$2; rm -rf bots/$2/__pycache__
  sed -i '' 's/^NOISE_ON = True/NOISE_ON = False/' bots/$2/doctrine.py
  if [[ $3 != '-' ]]; then
    sed -i '' "s/^${FLAG} = .*\$/${FLAG} = $3/" bots/$2/doctrine.py
  fi
}
mk $BASE  _s48det_base -
mk $ARM   _s48det_off  False
mk $ARM   _s48det_on   True

same=0; diff=0; onsame=0; ondiff=0
for m in $MAPS; do
  for s in $SEEDS; do
    for seat in A B; do
      for v in base off on; do
        if [[ $seat == A ]]; then a=_s48det_$v; b=$OPP; else a=$OPP; b=_s48det_$v; fi
        $FC run $a $b maps/$m.map26 --seed $s --tle 0 --json \
            --replay /tmp/fo_${v}.replay26 >/dev/null 2>&1
      done
      hb=$(shasum -a 256 /tmp/fo_base.replay26 | cut -d' ' -f1)
      ho=$(shasum -a 256 /tmp/fo_off.replay26  | cut -d' ' -f1)
      hn=$(shasum -a 256 /tmp/fo_on.replay26   | cut -d' ' -f1)
      if [[ $hb == $ho ]]; then r1=MATCH; ((same++)); else r1=DIFFER; ((diff++)); fi
      if [[ $hb == $hn ]]; then r2=match; ((onsame++)); else r2=differ; ((ondiff++)); fi
      echo "$m s$s seat$seat  flagoff-vs-base=$r1  flagon-vs-base=$r2"
    done
  done
done
echo
echo "FLAG OFF == BASE : $same match / $diff differ   (want: all match)"
echo "FLAG ON  != BASE : $ondiff differ / $onsame match  (POSITIVE CONTROL; want: all differ)"
rm -rf bots/_s48det_base bots/_s48det_off bots/_s48det_on
