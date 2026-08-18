#!/bin/bash
# ⛔ MANDATE STEP 0, RUN BEFORE ANYTHING ELSE: does the PARENT-AS-CONFIGURED
# (v521 tree with FS_V521_SYNC / FS_V521_COLLARFIRST off at their definition
# sites) reproduce a v520-PINCER-ONLY + LEAKFIX reference?
#
# It is NOT expected to be byte-identical and the mandate says so: PHASE_HONEST
# (v521 clause 1e) is retained in the parent config and it CHANGES A PUBLISHED
# CHANNEL -- FS_PH_KILL_OPEN is published whenever a turret is live and the
# collar reads open THIS round, instead of only when it has never closed.  The
# reference arm is the same tree with PHASE_HONEST additionally False, so this
# leg isolates 1e and nothing else.
#
#   NEG   v520ref vs v520ref  -> must MATCH   (determinism control)
#   TEST  v520ref vs parent   -> the 1e dose, reported not asserted
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v523_build
mkdir -p "$B/base"
rm -rf "$B/arms/b_opp" "$B/arms/b_ref" "$B/arms/b_par"
cp -R bots/_v488beltbreak2 "$B/arms/b_opp"; chmod -R u+w "$B/arms/b_opp"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/b_opp/doctrine.py"
cp -R "$B/arms/v520ref" "$B/arms/b_ref"; chmod -R u+w "$B/arms/b_ref"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/b_ref/doctrine.py"
cp -R "$B/arms/parent" "$B/arms/b_par"; chmod -R u+w "$B/arms/b_par"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/b_par/doctrine.py"
rm -rf "$B"/arms/b_*/__pycache__

n_n=0; n_d=0; t_n=0; t_d=0
for m in atoll drakkarfjord glacierkeep midgard nordkap yulerune; do
  for seat in A B; do
    for arm in r1 r2 par; do
      case $arm in
        r1|r2) T="$B/arms/b_ref";;
        par)   T="$B/arms/b_par";;
      esac
      if [ "$seat" = A ]; then F="$T"; S="$B/arms/b_opp"; else F="$B/arms/b_opp"; S="$T"; fi
      .venv/bin/fcode run "$F" "$S" "maps/$m.map26" --seed 7 --tle 10 \
          --replay "$B/base/${m}_${seat}_${arm}.replay26" >/dev/null 2>&1
    done
    a=$(md5 -q "$B/base/${m}_${seat}_r1.replay26")
    b=$(md5 -q "$B/base/${m}_${seat}_r2.replay26")
    c=$(md5 -q "$B/base/${m}_${seat}_par.replay26")
    [ "$a" = "$b" ] && n_n=$((n_n+1)) || n_d=$((n_d+1))
    [ "$a" = "$c" ] && t_n=$((t_n+1)) || t_d=$((t_d+1))
    echo "$m $seat neg=$([ "$a" = "$b" ] && echo SAME || echo DIFF) test=$([ "$a" = "$c" ] && echo SAME || echo DIFF)"
  done
done
echo "NEG   v520ref vs v520ref : identical $n_n / differing $n_d   (want 12/0)"
echo "TEST  v520ref vs parent  : identical $t_n / differing $t_d   (PHASE_HONEST dose)"
