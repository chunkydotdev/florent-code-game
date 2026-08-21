#!/bin/zsh
# s54 fidelity-fixture recipe (the step ablate4.sh assumes): the NOISE_OFF opponent copy.
# Canonical bots/ trees are NEVER edited; the single modification to the copy is the sed below.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
BASE=scratchpad/s54_fidtape
rm -rf $BASE/opp_v542wave_noiseoff
cp -r bots/_v542wave $BASE/opp_v542wave_noiseoff
sed -i '' 's/^NOISE_ON = True/NOISE_ON = False/' $BASE/opp_v542wave_noiseoff/doctrine.py
# Verify by IMPORT, not by reading the assignment (the arm-append override hazard):
.venv/bin/python -c "
import sys; sys.path.insert(0, '$BASE/opp_v542wave_noiseoff')
import doctrine; assert doctrine.NOISE_ON is False, 'NOISE_ON flip did not take'
print('fixture ok: effective NOISE_ON = False')"
