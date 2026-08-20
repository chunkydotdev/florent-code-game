#!/bin/bash
# v529 STANDDOWN, in the two forms the union needs.
#
# (a) MAP STANDDOWN, v527 side.  archipelago is GATED and midgard is CRIPPLE:
#     the ferry-siege never opens, so ZERO v527 siege clauses may be reached.
#     `sd_v529` is the union with FS_V527_LOG=True and both tapes, so a clause
#     that fired would print.  ⚠ This assertion CAN fail -- the same tape reads
#     thousands of clause lines on atoll/drakkarfjord/glacierkeep (spot battery,
#     3,554 BUNKER lines in 12 games), which is what stops it being an
#     assertion that cannot fail.
#
# (b) SUB-FLAG STANDDOWN, both sides.  `eq_sub` = the union with BOTH masters
#     TRUE and every sub-flag of BOTH lineages False.  It must be byte-identical
#     to the parent.  If it is not, a master is doing something on its own and
#     none of the per-plank ablations mean what they say.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v529_build
O=$B/standdown
mkdir -p $O
FC=.venv/bin/fcode
OPP=bots/_v488beltbreak2

echo "=== (a) MAP STANDDOWN: 0 v527 clauses on gated boards ==="
for mp in archipelago midgard; do
  for sd in 401 402 403; do
    for seat in A B; do
      tag="sd_${mp}_s${sd}_${seat}"
      if [ "$seat" = "A" ]; then A=$B/sd_v529; Bo=$OPP; else A=$OPP; Bo=$B/sd_v529; fi
      $FC run $A $Bo maps/$mp.map26 --seed $sd --tle 10 \
          --replay $O/$tag.replay26 > $O/$tag.out 2> $O/$tag.err
    done
  done
  n=$(cat $O/sd_${mp}_*.err | grep -cE "^V527 (BUNKER|PSURV|LASTSEAT|TFIRST|SELFCUT|SWITCH|DEFHIT)")
  b=$(cat $O/sd_${mp}_*.err | grep -c "V527 BUNKER")
  p=$(cat $O/sd_${mp}_*.err | grep -c "V527 PSURV")
  tb=$(cat $O/sd_${mp}_*.err | grep -c "Traceback")
  printf "%-14s games 6   V527 clauses reached = %-4s BUNKER = %-4s PSURV = %-4s tb %s\n" $mp $n $b $p $tb
done

echo
echo "=== (b) SUB-FLAG STANDDOWN: masters ON, every sub-flag OFF == parent ==="
same=0; tot=0
for mp in atoll drakkarfjord glacierkeep nordkap yulerune; do
  for seat in A B; do
    for arm in eq_sub eq_parent; do
      tag="sub_${mp}_${seat}_${arm}"
      if [ "$seat" = "A" ]; then A=$B/$arm; Bo=$B/eq_opp; else A=$B/eq_opp; Bo=$B/$arm; fi
      $FC run $A $Bo maps/$mp.map26 --seed 529820 --tle 0 \
          --replay $O/$tag.replay26 --json > $O/$tag.out 2> $O/$tag.err
    done
    tot=$((tot+1))
    if cmp -s $O/sub_${mp}_${seat}_eq_sub.replay26 $O/sub_${mp}_${seat}_eq_parent.replay26; then
      same=$((same+1)); r=IDENTICAL; else r="DIFFERS(FAIL)"; fi
    printf "  %-14s seat%s  %s\n" $mp $seat $r
  done
done
echo "  -> $same/$tot IDENTICAL"
echo "STANDDOWN DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
