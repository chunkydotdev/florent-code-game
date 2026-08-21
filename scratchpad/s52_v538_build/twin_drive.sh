#!/bin/bash
# v538 build instrument #8 -- THE SAME-BOT SWING, i.e. THIS FIXTURE'S OWN NOISE
# FLOOR at n=60/cell.
# ⛔ WHY IT EXISTS, and it is a finding not a formality: the mechanism tape read
# v538refine ABOVE v537socket on glacierkeep (+20.0pp) and yulerune (+11.7pp) --
# two boards the siege RUNS, where the gate returns claim-ON and the identity
# battery already proved the two trees row-identical under NOISE_OFF. A gate
# that cannot fire cannot have caused that. Either the shipped (NOISE_ON) arms
# simply do not reproduce at n=60, or something else moved. This measures which,
# by running TWO BYTE-IDENTICAL COPIES of the parent as separate arms on the
# identical grid.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s52_v538_build
export PAR=4
export OUT=$B/twin
export OPP=$PWD/bots/_x3r0v169mjolnir
export ARMS="twinA=$B/arms/twinA,twinB=$B/arms/twinB"
export MAPS=archipelago,yulerune,glacierkeep
echo "TWIN START $(date -u +%Y-%m-%dT%H:%M:%SZ)"
for i in 1 2 3 4 5 6; do
  a=$(( (i-1)*5 + 1 )); b=$(( i*5 ))
  export SEEDS=$(python3 -c "print(','.join(str(x) for x in range($a, $b+1)))")
  .venv/bin/python3 scratchpad/s51_v5301_build/run_battery.py
  echo "  TWIN BLOCK $i (seeds $a-$b) done $(date -u +%H:%M:%SZ)"
done
echo "TWIN DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
