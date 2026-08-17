#!/bin/zsh
# s48 OPENFAST demo: first-harvester round, arm vs base, per map / seat / opponent.
#
# DETERMINISM PRECONDITION (tools/det.py, same one s48_flagoff.sh states): the
# engine is not reproducible as shipped -- NOISE_ON injects an UNSEEDED
# per-unit spawn salt, and the CPU killer is wall-clock. With NOISE_ON=False
# and --tle 0 a (bot, bot, map, seed) cell is a FUNCTION, so base and arm
# differ by the plank and by nothing else. Without this the spawn salt alone
# moves the first-harvester round by +-3, which is larger than the effect.
#
# ⛔ AND THAT PRECONDITION KILLS THE SEED AXIS: with NOISE_ON=False, seeds 11
# and 22 produced BYTE-IDENTICAL opening columns in all 32 cells of the first
# run of this harness. The seed is INERT for our own decisions, so replicating
# over seeds manufactures n without adding information. The axes that carry
# information are MAP, SEAT and OPPONENT, and this harness rotates all three.
#
# MAP SET: every map in maps/ (25), which subsumes the flag-off set and covers
# FAILURE GEOMETRY (archipelago 208 walls, saga 164, heart 122, lighthouse 64
# on a 16x16), CLOSE-ORE maps (archipelago / snowflake, nearest-ore d=2), the
# LONG-WALK stress case (drakkarfjord d=12, valkyrie d=10) and the small-map
# branch of _pick (fjordgate 10x10 -> workers=2).
set -u
BASE=_v468kladturbo
ARM=_v486openfast
OPPS=(opp_v63 opp_v78)
SEED=11
FC=.venv/bin/fcode
OUT=${1:-scratchpad/s48_demo_rows.tsv}

mk() { rm -rf bots/$2; cp -r bots/$1 bots/$2; rm -rf bots/$2/__pycache__
       sed -i '' 's/^NOISE_ON = True/NOISE_ON = False/' bots/$2/doctrine.py }
mk $BASE _s48d_base
mk $ARM  _s48d_arm

print "arm\topp\tlabel\tteam\tcore\tnear_ore\td\th1\th1_seat\th1_pos\tc1\twalk_lb\tharv25\tconv25\tharv8\tconv8\tbld8" > $OUT
ERRS=0
for f in maps/*.map26; do
  m=${f:t:r}
  for o in $OPPS; do
    for v in base arm; do
      $FC run _s48d_$v $o $f --seed $SEED --tle 0 --json \
          --replay /tmp/s48d.replay26 >/dev/null 2>/tmp/s48d_err
      grep -q "Traceback" /tmp/s48d_err && { print "TRACEBACK $v $m $o A"; ERRS=$((ERRS+1)) }
      print -n "$v\t$o\t" >> $OUT
      .venv/bin/python scratchpad/s48_open_table.py /tmp/s48d.replay26 \
          --team 0 --rounds 25 --label "$m/A" >> $OUT
      $FC run $o _s48d_$v $f --seed $SEED --tle 0 --json \
          --replay /tmp/s48d.replay26 >/dev/null 2>/tmp/s48d_err
      grep -q "Traceback" /tmp/s48d_err && { print "TRACEBACK $v $m $o B"; ERRS=$((ERRS+1)) }
      print -n "$v\t$o\t" >> $OUT
      .venv/bin/python scratchpad/s48_open_table.py /tmp/s48d.replay26 \
          --team 1 --rounds 25 --label "$m/B" >> $OUT
    done
  done
done
print "tracebacks seen: $ERRS"
rm -rf bots/_s48d_base bots/_s48d_arm
print "rows -> $OUT"
