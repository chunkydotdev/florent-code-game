#!/bin/zsh
cd /Users/junghard/Projects/Work/florent-code-game
for i in $(seq 1 180); do
  out=$(.venv/bin/python tools/leg_read.py --file scratchpad/loki13_ids.txt 2>&1)
  if echo "$out" | grep -q "(n=25 games)" && ! echo "$out" | grep -q "NOT YET COMPLETE"; then
    echo "$(date -u +%H:%M:%SZ) LEG COMPLETE AND FULLY READABLE"
    echo "$out" > scratchpad/loki13_result.txt
    echo "$out"
    exit 0
  fi
  sleep 30
done
echo "$(date -u +%H:%M:%SZ) never reached a complete readable state in 90 min"
