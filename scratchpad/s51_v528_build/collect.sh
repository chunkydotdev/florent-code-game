#!/bin/bash
# Dump every measured number this build reports, in one pass, so the report is
# assembled from ONE artefact rather than from scrollback.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v528_build
echo "=================== COLLECTED $(date -u +%Y-%m-%dT%H:%M:%SZ) ==================="
echo; echo "########## TREE FREEZE ##########"; cat $B/TREE_FROZEN.md5
echo; echo "PARENT FREEZE:"; cat $B/PARENT_FREEZE.md5
echo; echo "########## FILE DISCIPLINE ##########"
for f in doctrine.py eco.py main.py raid.py siege.py; do
  if cmp -s bots/_v528eco/$f $B/parent_arm/$f; then echo "  $f IDENTICAL to parent"
  else echo "  $f DIFFERS  ($(diff <(cat $B/parent_arm/$f) <(cat bots/_v528eco/$f) | grep -c '^[<>]') changed lines)"; fi
done
echo; echo "########## AST SCAN ##########"
.venv/bin/python $B/flagoff_ast.py bots/_v528eco/doctrine.py bots/_v528eco/eco.py bots/_v528eco/main.py bots/_v528eco/raid.py bots/_v528eco/siege.py 2>&1 | grep -E "GUARD|REAL-CASE|TOTAL|RESULT"
echo; echo "########## BYTE IDENTITY ##########"; cat $B/byte_identity.log
echo; echo "########## CPU BENCH ##########"; .venv/bin/python $B/cpubench.py 2>&1
echo; echo "########## DELIV SELFTEST ##########"
.venv/bin/python $B/deliv.py --selftest $B/probe/rep/*.replay26 2>&1
echo; echo "########## HEADLINE SELFTEST ##########"; .venv/bin/python $B/headline.py --selftest
echo; echo "########## STALLSCAN SELFTEST ##########"; .venv/bin/python $B/stallscan2.py --selftest
echo; echo "########## HEADLINE ##########"
echo "rows: $(wc -l < $B/head/results.tsv)"
.venv/bin/python $B/headline.py $B/head/results.tsv --rep $B/head/rep 2>&1
echo; echo "########## FAILURE REEL ##########"; .venv/bin/python $B/reel.py $B/head v528 2>&1
echo; echo "########## M5 REGRET (rc cell) ##########"
.venv/bin/python $B/connread.py $B/rc/*.err 2>&1
echo; echo "########## M5 REGRET, POOLED PER ARM ##########"
for A in inst_off inst_walk inst_v528 inst_mut; do
  echo -n "$A  PICK: "
  cat $B/rc/${A}_*.err 2>/dev/null | grep "^V528 PICK " | awk '{reg=$14; ra=$24; nb=$22; n++; s+=reg; sa+=ra; if(reg>0)p++; if(reg>mx)mx=reg; if(nb>0)b++} END{if(n)printf "picks=%d mean_reg=%.3f reg>0=%d max=%d mean_regall=%.3f picks_with_banned_cand=%d\n", n,s/n,p,mx,sa/n,b; else print "NO TAPE"}'
  echo -n "$A  BUILD: "
  cat $B/rc/${A}_*.err 2>/dev/null | grep "^V528 CONN " | awk '{r=$12; n++; s+=r; if(r>0)p++} END{if(n)printf "decisions=%d mean_regret=%.3f regret>0=%d\n", n,s/n,p; else print "NO TAPE"}'
  echo -n "$A  WIRE defers: "; cat $B/rc/${A}_*.err 2>/dev/null | grep -c "V528 WIRE defer"
done
echo; echo "########## M4 STALLS ##########"
.venv/bin/python $B/stallscan2.py $B/rc/*.err 2>&1 | head -40
echo; echo "########## TRACEBACKS ##########"
echo "headline results.tsv tracebacks column sum: $(awk -F'\t' 'NR>1{s+=$10} END{print s+0}' $B/head/results.tsv)"
echo "rc cell tracebacks: $(cat $B/rc/*.err 2>/dev/null | grep -c Traceback)"
echo "byte_check tracebacks: $(cat $B/byte_check/*.err 2>/dev/null | grep -c Traceback)"
