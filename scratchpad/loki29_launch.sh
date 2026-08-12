#!/bin/zsh
# LOKI-29 launcher. ALWAYS_BE_RUNNING: fires the moment the s31 overnight drains
# so the cores never sit idle between batteries.
# overnight.sh hardcodes OUT=scratchpad/overnight (line 44), so the s31 outputs
# are ARCHIVED first rather than mixed with the new shards.
cd /Users/junghard/Projects/Work/florent-code-game
while [[ $(ps aux | grep -c '[o]vernight.sh') -gt 0 ]]; do sleep 20; done
sleep 15
mkdir -p scratchpad/overnight_s31
mv scratchpad/overnight/* scratchpad/overnight_s31/ 2>/dev/null
date -u > scratchpad/overnight_s31/ARCHIVED_AT
grep -v '^#' scratchpad/loki29_spec.txt | while read -r SH T C N S; do
  [[ -z "$SH" ]] && continue
  nohup zsh tools/overnight.sh "$SH" "$T" "$C" "$N" "$S" \
      >> scratchpad/loki29_$SH.launch.log 2>&1 &
  sleep 3
done
date -u > scratchpad/LOKI29_LAUNCHED
