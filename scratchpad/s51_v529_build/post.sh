#!/bin/bash
# Everything that must wait for the headline battery to release the 4 workers.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v529_build
bash $B/dose.sh          > $B/dose.log 2>&1
bash $B/standdown.sh     > $B/standdown.log 2>&1
.venv/bin/python3 $B/byteid_supp.py > $B/byteid_supp.log 2>&1
echo "POST DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
