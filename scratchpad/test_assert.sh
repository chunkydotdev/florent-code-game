#!/bin/zsh
cd /Users/junghard/Projects/Work/florent-code-game
holder(){ .venv/bin/fcode status 2>/dev/null | grep "Active bot" | sed 's/.*Active bot: //'; }
INCUMBENT=104
# exact guard copied from tools/fanout.sh fire()
check(){ local want="${1:-$INCUMBENT}"; local live="$(holder)"
  if [[ "$live" != v${want}* ]]; then echo "ABORT (expected v$want, holder '$live')"; return 1
  else echo "PROCEED (expected v$want, holder '$live')"; return 0; fi }
echo "--- must PROCEED (correct expectation) ---"; check 104
echo "--- must ABORT (wrong expectation, the real bug's shape) ---"; check 102
echo "--- must ABORT (nonexistent version) ---"; check 999
