#!/usr/bin/env zsh
# C63 PROBE RUNNER (scratchpad, local only).
#   run_c63.sh <worker_idx> <n_workers> <games_per_map_per_seat> <seed_lo>
# Instrumented tree plays the incumbent; only the instrumented side emits.
# Per game: reduce stderr to the LAST line per unit id, tag with map/seat/seed.
set -u
SP=${SP:?}
REPO=/Users/junghard/Projects/Work/florent-code-game
FC=$REPO/.venv/bin/fcode
INSTR=$SP/_c63instr2
CTRL=$REPO/bots/_v223sealrepair
W=${1:?}; NW=${2:?}; G=${3:?}; SEEDLO=${4:?}
MAPS=(midgard ragnarok valkyrie glacierkeep)
OUT=$SP/c63b_rows_w${W}.tsv
: > $OUT
i=0
for M in $MAPS; do
  for (( k=0; k<G; k++ )); do
    for ORD in A B; do
      i=$(( i + 1 ))
      (( k % NW != W )) && continue
      SEED=$(( SEEDLO + k ))
      TMP=$SP/.raw_w${W}.txt
      if [[ $ORD == A ]]; then
        timeout 300 $FC run $INSTR $CTRL $REPO/maps/$M.map26 --seed $SEED --tle 10 --replay /dev/null > $SP/.res_w${W}.txt 2> $TMP
      else
        timeout 300 $FC run $CTRL $INSTR $REPO/maps/$M.map26 --seed $SEED --tle 10 --replay /dev/null > $SP/.res_w${W}.txt 2> $TMP
      fi
      WL=$(grep -i "Winner:" $SP/.res_w${W}.txt | head -1)
      TURNS=${WL##*turn }; TURNS=${TURNS%%[!0-9]*}
      case "$WL" in *_c63instr2*) WIN=INSTR;; *) WIN=CTRL;; esac
      awk -v m=$M -v ord=$ORD -v sd=$SEED -v gid="w${W}_${i}" -v tn="${TURNS:--}" -v win="${WIN:--}" '
        $1=="C63" { key=$3; line[key]=$0 }
        END { for (k in line) { print gid"\t"m"\t"ord"\t"sd"\t"tn"\t"win"\t"line[k] } }
      ' $TMP >> $OUT
      print -r -- "$(date -u +%H:%M:%S) w$W $M $ORD seed=$SEED turns=${TURNS:--} win=${WIN:--} units=$(grep -c '^C63	' $TMP)"
      rm -f $TMP
    done
  done
done
print "WORKER $W DONE"
