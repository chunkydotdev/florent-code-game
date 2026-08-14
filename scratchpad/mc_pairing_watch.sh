#!/bin/zsh
# One-shot: exit when a ladder pairing created after 07:30:00Z today appears.
# The exit wakes the builder, who types the v125 activation (watcher never acts).
cd /Users/junghard/Projects/Work/florent-code-game
while true; do
  new=$(.venv/bin/fcode match list --mine --type ladder --json --limit 3 2>/dev/null | \
    .venv/bin/python -c "
import json,sys
try: ms=json.load(sys.stdin)['matches']
except Exception: ms=[]
hits=[m['createdAt'] for m in ms if m.get('createdAt','') > '2026-08-14T07:50:00']
print(hits[0] if hits else '')")
  if [[ -n $new ]]; then
    echo "PAIRING SEEN: createdAt=$new — v135's one ladder match is paired. Roll back to v125 NOW (clear air ~16 min)."
    exit 0
  fi
  sleep 20
done
