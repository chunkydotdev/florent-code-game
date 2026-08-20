#!/bin/bash
# v529 COMPOSITION BATTERY: FIVE concurrent arms, n=480 each, the SAME 8-map
# panel v526/v527/v528 used (deviating would make the cross-build comparison
# invalid), arms INTERLEAVED per cell (v518 finding 2: pooling non-time-adjacent
# local fixtures produced a 4.6pp FALSE POSITIVE on byte-identical play).
#
#   v529     bots/_v529merge            the UNION, both masters True
#   v527     bots/_v527collar           v527 delta alone, as fired
#   v528     bots/_v528eco              v528 delta alone, as fired
#   parent   base_arm                   `_v526transit` configured RDV-ONLY
#   flagoff  flagoff_arm                the UNION with BOTH masters False --
#            proved byte-identical to `parent` on 16/16 cells by
#            byte_identity.py, so every flagoff-vs-parent number is FIXTURE
#            SPREAD and is the only honest yardstick for the other three.
#
# THE QUESTION: does union ~= v527delta + v528delta, or is it subadditive /
# interacting (the v515 signature: composite BELOW the best single arm).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v529_build
export OUT=$B/head
export ARMS="v529=bots/_v529merge,v527=bots/_v527collar,v528=bots/_v528eco,parent=$B/base_arm,flagoff=$B/flagoff_arm"
export MAPS=atoll,drakkarfjord,glacierkeep,nordkap,yulerune,antler,fjordgate,midgard
export PAR=4
for i in $(seq 1 15); do
  a=$((i*2-1)); b=$((i*2))
  export SEEDS="$a,$b"
  .venv/bin/python3 $B/run_battery.py
  echo "HEAD BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "HEADLINE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
