#!/bin/bash
# BYTE-IDENTITY: does `LOKI_FS_V521 = False` play the v520-PINCER-ONLY baseline's
# games EXACTLY?
#
# ⛔ A WIN-RATE COMPARISON CANNOT SETTLE A NULL AT ANY n THIS FIXTURE CAN AFFORD
# (v518 finding 2 caught a 4.6pp separation at n=810/arm on byte-identical
# play).  So the question is asked directly: both trees on the same seeds with
# the randomness switched off -- OURS **AND THE OPPONENT'S** (v518 measured that
# disabling our salt alone pins nothing) -- and the replay bytes diffed.
#
# ⭐ THE TEST IS STRONGER HERE THAN IN v520, and it is worth saying why: the
# baseline is not a copy of the treatment tree with a flag appended.  It is
# `bots/_v520pincer` with FS_V520_PRESENCE / FS_V520_GUNNEAR turned off AT THEIR
# DEFINITION SITES -- an independently constructed tree.  So this test asks
# whether TWO SEPARATELY BUILT TREES play the same 12 games byte for byte, which
# also certifies fired-config correction (i).
#
# THREE ARMS, and the controls are what make "identical" mean anything:
#   NEGATIVE CONTROL  baseline vs baseline (same tree, two runs)  -> must MATCH
#   TEST              baseline vs v521 FLAG-OFF                   -> must MATCH
#   POSITIVE CONTROL  baseline vs v521 FIRED                      -> must DIFFER
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v521_build
mkdir -p "$B/eq"
rm -rf "$B/arms/eq_opp" "$B/arms/eq_base" "$B/arms/eq_off" "$B/arms/eq_fired"
cp -R bots/_v488beltbreak2 "$B/arms/eq_opp"; chmod -R u+w "$B/arms/eq_opp"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/eq_opp/doctrine.py"
cp -R "$B/arms/pinceronly" "$B/arms/eq_base"; chmod -R u+w "$B/arms/eq_base"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/eq_base/doctrine.py"
cp -R bots/_v521sync "$B/arms/eq_off"; chmod -R u+w "$B/arms/eq_off"
{ echo ""; echo "LOKI_FS_V521 = False"; echo "NOISE_ON = False"; } >> "$B/arms/eq_off/doctrine.py"
cp -R bots/_v521sync "$B/arms/eq_fired"; chmod -R u+w "$B/arms/eq_fired"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/eq_fired/doctrine.py"
rm -rf "$B"/arms/eq_*/__pycache__

id_n=0; id_d=0; t_n=0; t_d=0; f_n=0; f_d=0
for m in atoll drakkarfjord glacierkeep midgard nordkap yulerune; do
  for seat in A B; do
    for arm in p1 p2 off fired; do
      case $arm in
        p1|p2) T="$B/arms/eq_base";;
        off)   T="$B/arms/eq_off";;
        fired) T="$B/arms/eq_fired";;
      esac
      if [ "$seat" = A ]; then F="$T"; S="$B/arms/eq_opp"; else F="$B/arms/eq_opp"; S="$T"; fi
      .venv/bin/fcode run "$F" "$S" "maps/$m.map26" --seed 7 --tle 10 \
          --replay "$B/eq/${m}_${seat}_${arm}.replay26" >/dev/null 2>&1
    done
    a=$(md5 -q "$B/eq/${m}_${seat}_p1.replay26")
    b=$(md5 -q "$B/eq/${m}_${seat}_p2.replay26")
    c=$(md5 -q "$B/eq/${m}_${seat}_off.replay26")
    d=$(md5 -q "$B/eq/${m}_${seat}_fired.replay26")
    if [ "$a" = "$b" ]; then id_n=$((id_n+1)); else id_d=$((id_d+1)); fi
    if [ "$a" = "$c" ]; then t_n=$((t_n+1)); else t_d=$((t_d+1)); fi
    if [ "$a" = "$d" ]; then f_n=$((f_n+1)); else f_d=$((f_d+1)); fi
    echo "$m $seat control=$([ "$a" = "$b" ] && echo SAME || echo DIFF) test=$([ "$a" = "$c" ] && echo SAME || echo DIFF) posctl=$([ "$a" = "$d" ] && echo SAME || echo DIFF)"
  done
done
echo "NEGATIVE CONTROL  baseline vs baseline : identical $id_n / differing $id_d   (want 12/0)"
echo "TEST              baseline vs FLAG-OFF : identical $t_n / differing $t_d   (want 12/0)"
echo "POSITIVE CONTROL  baseline vs v521 FIRED: identical $f_n / differing $f_d   (want 0/12)"
