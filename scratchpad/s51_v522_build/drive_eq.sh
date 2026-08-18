#!/bin/bash
# v522 BYTE-IDENTITY, and it asks FOUR questions rather than v521's three.
#
#   NEG   parent vs parent (same tree, two runs)      -> must MATCH  (12/12)
#   TEST  parent vs v522 FLAG-OFF                     -> must MATCH  (12/12)
#   CHAN  parent vs v522 PHASE_ONLY mutant            -> must MATCH  (12/12)
#         ⭐ THE CHANNEL-SUBSTITUTION CONTROL.  PHASE_ONLY publishes
#         FS_PH_KILL_NEAR = 6 in exactly the rounds the fired build does and
#         NEVER raises the floor.  A MATCH turns "the new phase code is
#         behaviourally inert at all nine existing consumers" from an
#         enumeration into a measurement.  A DIFF means the enumeration is
#         wrong and the build stops.
#   POS   parent vs v522 FIRED                        -> must DIFFER
#
# Randomness off on BOTH sides (v518: disabling our salt alone pins nothing).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v522_build
mkdir -p "$B/eq"
rm -rf "$B/arms/eq_opp" "$B/arms/eq_base" "$B/arms/eq_off" "$B/arms/eq_fired" "$B/arms/eq_chan"
cp -R bots/_v488beltbreak2 "$B/arms/eq_opp"; chmod -R u+w "$B/arms/eq_opp"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/eq_opp/doctrine.py"
cp -R "$B/arms/parent" "$B/arms/eq_base"; chmod -R u+w "$B/arms/eq_base"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/eq_base/doctrine.py"
cp -R bots/_v522floor "$B/arms/eq_off"; chmod -R u+w "$B/arms/eq_off"
{ echo ""; echo "LOKI_FS_V522 = False"; echo "NOISE_ON = False"; } >> "$B/arms/eq_off/doctrine.py"
cp -R bots/_v522floor "$B/arms/eq_chan"; chmod -R u+w "$B/arms/eq_chan"
{ echo ""; echo "FS_V522_PHASE_ONLY = True"; echo "NOISE_ON = False"; } >> "$B/arms/eq_chan/doctrine.py"
cp -R bots/_v522floor "$B/arms/eq_fired"; chmod -R u+w "$B/arms/eq_fired"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/eq_fired/doctrine.py"
rm -rf "$B"/arms/eq_*/__pycache__

id_n=0; id_d=0; t_n=0; t_d=0; c_n=0; c_d=0; f_n=0; f_d=0
for m in atoll drakkarfjord glacierkeep midgard nordkap yulerune; do
  for seat in A B; do
    for arm in p1 p2 off chan fired; do
      case $arm in
        p1|p2) T="$B/arms/eq_base";;
        off)   T="$B/arms/eq_off";;
        chan)  T="$B/arms/eq_chan";;
        fired) T="$B/arms/eq_fired";;
      esac
      if [ "$seat" = A ]; then F="$T"; S="$B/arms/eq_opp"; else F="$B/arms/eq_opp"; S="$T"; fi
      .venv/bin/fcode run "$F" "$S" "maps/$m.map26" --seed 7 --tle 10 \
          --replay "$B/eq/${m}_${seat}_${arm}.replay26" >/dev/null 2>&1
    done
    a=$(md5 -q "$B/eq/${m}_${seat}_p1.replay26")
    b=$(md5 -q "$B/eq/${m}_${seat}_p2.replay26")
    c=$(md5 -q "$B/eq/${m}_${seat}_off.replay26")
    e=$(md5 -q "$B/eq/${m}_${seat}_chan.replay26")
    d=$(md5 -q "$B/eq/${m}_${seat}_fired.replay26")
    [ "$a" = "$b" ] && id_n=$((id_n+1)) || id_d=$((id_d+1))
    [ "$a" = "$c" ] && t_n=$((t_n+1))  || t_d=$((t_d+1))
    [ "$a" = "$e" ] && c_n=$((c_n+1))  || c_d=$((c_d+1))
    [ "$a" = "$d" ] && f_n=$((f_n+1))  || f_d=$((f_d+1))
    echo "$m $seat neg=$([ "$a" = "$b" ] && echo SAME || echo DIFF) test=$([ "$a" = "$c" ] && echo SAME || echo DIFF) chan=$([ "$a" = "$e" ] && echo SAME || echo DIFF) pos=$([ "$a" = "$d" ] && echo SAME || echo DIFF)"
  done
done
echo "NEG   parent vs parent      : identical $id_n / differing $id_d   (want 12/0)"
echo "TEST  parent vs FLAG-OFF    : identical $t_n / differing $t_d   (want 12/0)"
echo "CHAN  parent vs PHASE_ONLY  : identical $c_n / differing $c_d   (want 12/0)"
echo "POS   parent vs v522 FIRED  : identical $f_n / differing $f_d   (want 0/12)"
