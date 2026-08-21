#!/bin/bash
# s52 v538 IDENTITY + DOSE, NOISE_OFF ON EVERY BOT INCLUDING THE OPPONENT.
#   REFUSING boards (archipelago, midgard): v538_off MUST differ from par_off
#     -- that is the DOSE.
#   RUNNING boards (glacierkeep, yulerune, nordkap): v538_off MUST be
#     row-identical to par_off -- the gate touches nothing there.
#   flagoff_off / masteroff_off MUST be row-identical to par_off EVERYWHERE.
#   par_twin is the fixture's own determinism control.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s52_v538_build
export PAR=4
export OUT=$B/ident
export OPP=$PWD/$B/arms/opp_off
export ARMS="par_off=$B/arms/par_off,par_twin=$B/arms/par_twin,v538_off=$B/arms/v538_off,flagoff_off=$B/arms/flagoff_off,masteroff_off=$B/arms/masteroff_off"
export MAPS=archipelago,midgard,glacierkeep,yulerune,nordkap
export SEEDS=1,2,3,4,5
echo "IDENT START $(date -u +%Y-%m-%dT%H:%M:%SZ)"
.venv/bin/python3 scratchpad/s51_v5301_build/run_battery.py
echo "IDENT DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
