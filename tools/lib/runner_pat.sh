# runner_pat.sh — THE one definition of "what a shard-runner process looks
# like". Three tools broke independently on this today (status liveness,
# status badge digits, filler cancel/count) — each held its own copy, each
# missed a variant runner. D24(e): the second implementation is the one
# nobody tests. Source this; never inline the pattern again.
#
#   RUNNER_PAT        grep form ([o] self-exclusion trick for ps|grep)
#   RUNNER_PAT_PKILL  pkill -f form (no self-exclusion needed)
#
# Callers append "<SHARD> " (trailing space) to scope to one shard.
RUNNER_PAT='[o]vernight[a-z0-9_]*\.sh'
RUNNER_PAT_PKILL='overnight[a-z0-9_]*\.sh'

runner_pat_selftest() {
  local fail=0
  for good in "zsh tools/overnight.sh FOO bots/_a bots/_b 5400 1" \
              "zsh tools/overnight_pool26.sh BAR bots/_a bots/_b 5400 1" \
              "zsh tools/overnight_mapfix.sh BAZ bots/_a bots/_b 2160 1" \
              "zsh tools/overnight_zz9.sh SYN bots/_a bots/_b 100 1"; do
    echo "$good" | grep -q "$RUNNER_PAT" || { echo "FAIL match: $good"; fail=1; }
  done
  for bad in "python tools/monitors/replay_archiver.py" \
             ".venv/bin/python tools/monitors/cores_idle.py" \
             "vim overnight.txt"; do
    echo "$bad" | grep -q "$RUNNER_PAT" && { echo "FAIL non-match: $bad"; fail=1; }
  done
  # kill-path both ways: a REAL synthetic runner must be seen, killed, gone.
  local tmp=$(mktemp -d)/overnight_zz9.sh
  printf '#!/bin/zsh\nsleep 60\n' > "$tmp"; chmod +x "$tmp"
  zsh "$tmp" SYNTEST a b 1 1 & local pid=$!
  sleep 1
  ps ax -o command= | grep -q "$RUNNER_PAT SYNTEST " || { echo "FAIL: synthetic runner not seen"; fail=1; }
  pkill -f "$RUNNER_PAT_PKILL SYNTEST " 2>/dev/null
  sleep 1
  ps ax -o command= | grep -q "$RUNNER_PAT SYNTEST " && { echo "FAIL: synthetic runner survived pkill"; fail=1; }
  kill $pid 2>/dev/null
  (( fail == 0 )) && echo "RUNNER_PAT SELFTEST PASS (4 match + 3 non-match + kill path both ways)"
  return $fail
}
