#!/usr/bin/env zsh
set -u
cd /Users/junghard/Projects/Work/florent-code-game
FC=.venv/bin/fcode
OUT=/Users/junghard/Projects/Work/florent-code-game/scratchpad/collarmedic_dose_probe
REPLAYS=$OUT/replays
RESULTS=$OUT/results.tsv
: > $RESULTS
print -r -- "arm\tmap\tseed\twinner\tend_turn\tCMEDIC\tCHAIN\tCORE\tADJ\tBUDDY\tCOLLARHOLD\ttotal_heallog\thas_exception" >> $RESULTS

maps=(fjordgate hive midgard drakkarfjord)
seeds=(2001 2002 2003)

for arm in TREAT CTRL; do
  if [[ $arm == TREAT ]]; then
    BOTDIR=bots/_v232collarmedic
  else
    BOTDIR=bots/_v232collarmedic_off
  fi
  for map in $maps; do
    for seed in $seeds; do
      R=$REPLAYS/${arm}_${map}_${seed}.replay
      LOG=$REPLAYS/${arm}_${map}_${seed}.stdout
      $FC run $BOTDIR bots/_probe_creeper maps/$map.map26 --seed $seed --tle 10 --replay $R > $LOG 2>&1
      winner=$(grep -oE "Winner: \S+" $LOG | head -1 | sed 's/Winner: //')
      [[ -z $winner ]] && winner="NONE/ERROR"
      end_turn=$(grep -oE "turn [0-9]+\)" $LOG | head -1 | grep -oE "[0-9]+")
      [[ -z $end_turn ]] && end_turn="NA"
      cmedic=$(strings $R 2>/dev/null | grep -c "HEALLOG52 CMEDIC")
      chain=$(strings $R 2>/dev/null | grep -c "HEALLOG52 CHAIN")
      core=$(strings $R 2>/dev/null | grep -c "HEALLOG52 CORE")
      adj=$(strings $R 2>/dev/null | grep -c "HEALLOG52 ADJ")
      buddy=$(strings $R 2>/dev/null | grep -c "HEALLOG52 BUDDY")
      collarhold=$(strings $R 2>/dev/null | grep -c "HEALLOG52 COLLARHOLD")
      total=$(( cmedic + chain + core + adj + buddy + collarhold ))
      hasexc="no"
      if grep -qiE "traceback|exception" $LOG; then hasexc="yes-stdout"; fi
      if strings $R 2>/dev/null | grep -qiE "traceback \(most recent"; then hasexc="yes-replay"; fi
      print -r -- "$arm\t$map\t$seed\t$winner\t$end_turn\t$cmedic\t$chain\t$core\t$adj\t$buddy\t$collarhold\t$total\t$hasexc" >> $RESULTS
    done
  done
done
print "DONE"
