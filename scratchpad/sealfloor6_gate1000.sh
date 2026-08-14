#!/usr/bin/env bash
# MECHANICAL GATE-1000 CAPTURE for SEALFLOOR6.
# The prereg (SCREEN-sealfloor6-2026-08-14.md:225) says the gate is "read ONCE
# at first crossing; the builder types the decision, the watcher never decides".
# This watcher takes the reading AT THE ROW COUNT so the moment of observation
# is not a choice anyone made. It computes, it does not decide.
TSV=scratchpad/overnight/SEALFLOOR6.tsv
OUT=scratchpad/SEALFLOOR6_GATE1000.txt
while true; do
  n=$(( $(wc -l < "$TSV") - 1 ))
  if [ "$n" -ge 1000 ]; then
    {
      echo "GATE-1000 MECHANICAL CAPTURE"
      echo "captured_at   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
      echo "trigger       first polled observation with rows >= 1000"
      awk -F'\t' 'NR>1{
          rows++
          if($7=="T") t++
          else if($7=="C") c++
          else other[$7]++
        } END {
          dec = t + c
          printf "rows          %d\n", rows
          printf "T (treat)     %d\n", t
          printf "C (control)   %d\n", c
          printf "decisive      %d   (rows - NOWINNER)\n", dec
          for (k in other) printf "non-decisive  %s = %d\n", k, other[k]
          printf "SHARE         %.4f%%   (estimator: T / (rows - NOWINNER))\n", 100*t/dec
          printf "GATE          n>=1000, drop if share < 48.0%%  (<= 479 of 1000)\n"
          printf "VERDICT       %s\n", (100*t/dec < 48.0) ? "FUTILITY-EARLY (drop)" : "SURVIVES GATE-1000"
        }' "$TSV"
    } > "$OUT"
    exit 0
  fi
  sleep 10
done
