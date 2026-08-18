#!/bin/bash
# v523 BYTE-IDENTITY, four questions.
#
#   NEG   parent vs parent (same tree, two runs)     -> must MATCH  (12/12)
#         The negative control.  Without it a 12/12 "TEST" proves only that
#         the fixture is deterministic, not that the flag is inert.
#   TEST  parent vs v523 FLAG-OFF (LOKI_FS_V523=False) -> must MATCH (12/12)
#   STORE parent vs v523 STORE_ONLY                  -> DIFF EXPECTED, and the
#         differences must be STORE BYTES ONLY.  ⭐ THIS IS THE v522 INSTRUMENT
#         FINDING TURNED INTO A CONTROL: `.replay26` serialises the private
#         comms store, so an arm that publishes every v523 word and lets no
#         consumer act on it MUST differ from the parent in the replay bytes
#         while playing an identical game.  If it came out IDENTICAL the
#         dose baseline would be publishing nothing and the dose test below
#         would be measuring against the wrong thing.
#   POS   parent vs v523 FIRED                       -> must DIFFER
#
# Randomness off on BOTH sides (v518: disabling our salt alone pins nothing).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v523_build
mkdir -p "$B/eq"
rm -rf "$B/arms/eq_opp" "$B/arms/eq_base" "$B/arms/eq_off" "$B/arms/eq_fired" "$B/arms/eq_store"
cp -R bots/_v488beltbreak2 "$B/arms/eq_opp"; chmod -R u+w "$B/arms/eq_opp"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/eq_opp/doctrine.py"
cp -R "$B/arms/parent" "$B/arms/eq_base"; chmod -R u+w "$B/arms/eq_base"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/eq_base/doctrine.py"
cp -R bots/_v523eyes "$B/arms/eq_off"; chmod -R u+w "$B/arms/eq_off"
{ echo ""; echo "LOKI_FS_V523 = False"; echo "NOISE_ON = False"; } >> "$B/arms/eq_off/doctrine.py"
cp -R bots/_v523eyes "$B/arms/eq_store"; chmod -R u+w "$B/arms/eq_store"
{ echo ""; echo "FS_V523_STORE_ONLY = True"; echo "NOISE_ON = False"; } >> "$B/arms/eq_store/doctrine.py"
cp -R bots/_v523eyes "$B/arms/eq_fired"; chmod -R u+w "$B/arms/eq_fired"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/eq_fired/doctrine.py"
rm -rf "$B"/arms/eq_*/__pycache__

id_n=0; id_d=0; t_n=0; t_d=0; s_n=0; s_d=0; f_n=0; f_d=0
for m in atoll drakkarfjord glacierkeep midgard nordkap yulerune; do
  for seat in A B; do
    for arm in p1 p2 off store fired; do
      case $arm in
        p1|p2) T="$B/arms/eq_base";;
        off)   T="$B/arms/eq_off";;
        store) T="$B/arms/eq_store";;
        fired) T="$B/arms/eq_fired";;
      esac
      if [ "$seat" = A ]; then F="$T"; S="$B/arms/eq_opp"; else F="$B/arms/eq_opp"; S="$T"; fi
      .venv/bin/fcode run "$F" "$S" "maps/$m.map26" --seed 7 --tle 10 \
          --replay "$B/eq/${m}_${seat}_${arm}.replay26" >/dev/null 2>&1
    done
    a=$(md5 -q "$B/eq/${m}_${seat}_p1.replay26")
    b=$(md5 -q "$B/eq/${m}_${seat}_p2.replay26")
    c=$(md5 -q "$B/eq/${m}_${seat}_off.replay26")
    e=$(md5 -q "$B/eq/${m}_${seat}_store.replay26")
    d=$(md5 -q "$B/eq/${m}_${seat}_fired.replay26")
    [ "$a" = "$b" ] && id_n=$((id_n+1)) || id_d=$((id_d+1))
    [ "$a" = "$c" ] && t_n=$((t_n+1))  || t_d=$((t_d+1))
    [ "$a" = "$e" ] && s_n=$((s_n+1))  || s_d=$((s_d+1))
    [ "$a" = "$d" ] && f_n=$((f_n+1))  || f_d=$((f_d+1))
    echo "$m $seat neg=$([ "$a" = "$b" ] && echo SAME || echo DIFF) test=$([ "$a" = "$c" ] && echo SAME || echo DIFF) store=$([ "$a" = "$e" ] && echo SAME || echo DIFF) pos=$([ "$a" = "$d" ] && echo SAME || echo DIFF)"
  done
done
echo "NEG   parent vs parent        : identical $id_n / differing $id_d   (want 12/0)"
echo "TEST  parent vs v523 FLAG-OFF : identical $t_n / differing $t_d   (want 12/0)"
echo "STORE parent vs v523 STORE_ONLY: identical $s_n / differing $s_d   (DIFF expected, store bytes)"
echo "POS   parent vs v523 FIRED    : identical $f_n / differing $f_d   (want some DIFF)"
