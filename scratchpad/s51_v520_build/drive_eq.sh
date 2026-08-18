#!/bin/bash
# BYTE-IDENTITY: does `LOKI_FS_V520 = False` play the parent's games EXACTLY?
# ⛔ A WIN-RATE COMPARISON CANNOT SETTLE A NULL AT ANY n THIS FIXTURE CAN
# AFFORD (v518 finding 2 caught a 4.6pp separation at n=810/arm on
# byte-identical play).  So the question is asked directly: run both trees on
# the same seeds with the randomness switched off -- OURS **AND THE
# OPPONENT'S** (v518 measured that disabling our salt alone pins nothing; the
# opponent carries the identical re-roll at `_v488beltbreak2/main.py:445`) --
# and diff the replay bytes.
# THE NEGATIVE CONTROL IS THE WHOLE POINT: the same tree run twice must produce
# identical replays before "identical" means anything.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v520_build
mkdir -p "$B/eq"
rm -rf "$B/arms/eq_opp" "$B/arms/eq_parent" "$B/arms/eq_off"
cp -R bots/_v488beltbreak2 "$B/arms/eq_opp"; chmod -R u+w "$B/arms/eq_opp"
echo "" >> "$B/arms/eq_opp/doctrine.py"; echo "NOISE_ON = False" >> "$B/arms/eq_opp/doctrine.py"
cp -R "$B/arms/parent" "$B/arms/eq_parent"; chmod -R u+w "$B/arms/eq_parent"
echo "" >> "$B/arms/eq_parent/doctrine.py"; echo "NOISE_ON = False" >> "$B/arms/eq_parent/doctrine.py"
cp -R bots/_v520pincer "$B/arms/eq_off"; chmod -R u+w "$B/arms/eq_off"
{ echo ""; echo "LOKI_FS_V520 = False"; echo "NOISE_ON = False"; } >> "$B/arms/eq_off/doctrine.py"
rm -rf "$B"/arms/eq_*/__pycache__

id_n=0; id_d=0; t_n=0; t_d=0
for m in atoll drakkarfjord glacierkeep midgard nordkap yulerune; do
  for seat in A B; do
    for arm in p1 p2 off; do
      case $arm in
        p1|p2) T="$B/arms/eq_parent";;
        off)   T="$B/arms/eq_off";;
      esac
      if [ "$seat" = A ]; then F="$T"; S="$B/arms/eq_opp"; else F="$B/arms/eq_opp"; S="$T"; fi
      .venv/bin/fcode run "$F" "$S" "maps/$m.map26" --seed 7 --tle 10 \
          --replay "$B/eq/${m}_${seat}_${arm}.replay26" >/dev/null 2>&1
    done
    a=$(md5 -q "$B/eq/${m}_${seat}_p1.replay26")
    b=$(md5 -q "$B/eq/${m}_${seat}_p2.replay26")
    c=$(md5 -q "$B/eq/${m}_${seat}_off.replay26")
    if [ "$a" = "$b" ]; then id_n=$((id_n+1)); else id_d=$((id_d+1)); fi
    if [ "$a" = "$c" ]; then t_n=$((t_n+1)); else t_d=$((t_d+1)); fi
    echo "$m $seat control=$([ "$a" = "$b" ] && echo SAME || echo DIFF) test=$([ "$a" = "$c" ] && echo SAME || echo DIFF)"
  done
done
echo "NEGATIVE CONTROL  parent vs parent : identical $id_n / differing $id_d"
echo "TEST              parent vs FLAGOFF: identical $t_n / differing $t_d"
