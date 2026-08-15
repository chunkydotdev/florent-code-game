#!/usr/bin/env bash
# VPS ORCHESTRATOR — runs on THIS box. ssh/rsync only. No git anywhere.
#
#   tools/vps/orchestrate.sh gen    <host> [SHARD ...]   [--from F] [--null-target N] [--target N]
#   tools/vps/orchestrate.sh push   <host>
#   tools/vps/orchestrate.sh pull   <host>
#   tools/vps/orchestrate.sh status <host>
#   tools/vps/orchestrate.sh setup  <host> [--execute]
#   tools/vps/orchestrate.sh start  <host> [WORKERS]
#   tools/vps/orchestrate.sh stop   <host>
#
#   --local-sim <dir>   replace the transport: the "host" becomes a local
#                       directory, `ssh` becomes `bash -c`, `rsync -e ssh
#                       host:path` becomes plain local `rsync`. EVERYTHING ELSE
#                       — the snapshot contents, the remote command strings, the
#                       gates, the seed offset — is byte-identical. This is how
#                       the whole system is acceptance-tested BEFORE a server
#                       exists (see docs/vps-workers.md).
#
# ⛔ GIT TRANSPORT IS OUT OF SCOPE BY INSTRUCTION (Magnus). Nothing here clones,
#    pulls, pushes or reads a remote ref. The snapshot is an rsync of named
#    paths and nothing else.
#
# ⛔ THE WORKER HOLDS ZERO PLATFORM CREDENTIALS AND THE SNAPSHOT IS THE ENFORCER.
#    We ship: the bot trees named in the worklist, maps/ (pool only), worker.sh,
#    tools/ENGINE_PIN, the generated worklist + manifests. We do NOT ship docs/,
#    corpus/, replay_archive/, scratchpad/, elo_history.tsv, ladder_games.tsv,
#    fcode.toml, .git, or any tool that speaks to the platform. `fcode run` is
#    fully offline; nothing else runs there.
#
# ⭐ SEED PARTITION. Every host gets a stable additive offset:
#       offset = crc32(hostname) % 50 * 1_000_000
#    added to each row's seedbase. Two hosts running "the same shard" therefore
#    play DIFFERENT seeds and their rows are independent draws that pool. Without
#    it they would replay each other's games and the pooled n would be a lie —
#    the same class of defect as counting a duplicated restart prefix as new
#    data. The offset is written to a SIDECAR (work/SEED_OFFSET, and a copy at
#    scratchpad/vps/<host>/SEED_OFFSET) so it is auditable after the fact and
#    stable across regenerations: it is a pure function of the host string.
set -u

REPO=$(cd "$(dirname "$0")/../.." && pwd)
cd "$REPO"

REMOTE_ROOT=${REMOTE_ROOT:-fcode-worker}
LOCAL_ROOT=${LOCAL_ROOT:-scratchpad/vps}
PULL_ROOT=${PULL_ROOT:-scratchpad/overnight-remote}
SRC_WORKLIST=${SRC_WORKLIST:-scratchpad/corefill_work.txt}
PY=${PY:-.venv/bin/python}
SIM=""

say() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }
die() { say "$*"; exit "${2:-1}"; }

# ---------------------------------------------------------------------------
# TRANSPORT ABSTRACTION — one place, so --local-sim exercises the real logic
# ---------------------------------------------------------------------------
r_exec() {   # r_exec "<shell command, run in the worker root>"
  if [ -n "$SIM" ]; then ( cd "$SIM" && bash -c "$1" )
  else ssh -o BatchMode=yes "$HOST" "mkdir -p '$REMOTE_ROOT' && cd '$REMOTE_ROOT' && $1"; fi
}
# ⛔ COUNTING WORKERS WITHOUT COUNTING OURSELVES.
# `pgrep -fc 'tools/vps/worker.sh'` is what this file used, and it is WRONG over
# ssh: the remote shell's own argv CONTAINS that string (it is in the command we
# just sent), so pgrep matches the payload and the count is never 0. Measured
# 2026-08-15 on a host with the worker CONFIRMED dead (`status` said
# `runners: 0  worker: 0`): this returned **2**. cmd_kill printed that number
# under the instruction "Verify 'workers remaining: 0'" — an operator following
# its own documentation could never see the value it demands, so the check could
# only ever refuse. A guard that cannot return the passing verdict is not a
# guard. Same class as the local `pgrep` self-match that reported 12 watchers.
# ⛔ AND MY FIRST FIX FOR IT WAS ALSO WRONG, which is why this is a shared
# constant now. I replaced pgrep with `grep -F "bash tools/vps/worker.sh"` plus a
# $$/$PPID exclusion — and it STILL read 2 on the dead host, because the pattern
# is itself part of the payload being searched. Excluding PIDs cannot help: the
# text matches whatever process carries it.
# The working form is the one cmd_status has used all along — the BRACKET TRICK.
# `[w]orker.sh` as a regex matches the string `worker.sh`, but the payload
# carries the literal characters `[w]orker.sh`, which that regex does NOT match.
# Self-match is broken by construction rather than by filtering after the fact.
# Verified both ways live: dead host -> 0, host with a live worker -> nonzero.
WCOUNT_CMD='ps ax -o command= 2>/dev/null | grep -c "[w]orker.sh" || true'

r_exec_home() {  # r_exec_home "<shell command, run in the remote HOME>"
  if [ -n "$SIM" ]; then ( cd "$(dirname "$SIM")" && bash -c "$1" )
  else ssh -o BatchMode=yes "$HOST" "$1"; fi
}
r_dest() {  # where rsync should put things
  if [ -n "$SIM" ]; then printf '%s/' "$SIM"; else printf '%s:%s/' "$HOST" "$REMOTE_ROOT"; fi
}
r_src() {   # r_src <relative path on the worker>
  if [ -n "$SIM" ]; then printf '%s/%s' "$SIM" "$1"; else printf '%s:%s/%s' "$HOST" "$REMOTE_ROOT" "$1"; fi
}
# One rsync wrapper. Written as a branch rather than an array so the file stays
# bash-3.2 clean (`"${arr[@]}"` on an empty array is an unbound-variable error
# under `set -u` there, and /bin/bash on this orchestrator IS 3.2).
rs() {
  if [ -n "${RSYNC_E:-}" ]; then rsync -a -e "$RSYNC_E" "$@"; else rsync -a "$@"; fi
}

# ---------------------------------------------------------------------------
# arg parsing
# ---------------------------------------------------------------------------
CMD=${1:-}; shift 2>/dev/null || true
HOST=${1:-}; shift 2>/dev/null || true
[ -n "$CMD" ] || die "usage: $0 {gen|push|pull|status|setup|start|stop} <host> [...]  (see the header)" 2
[ -n "$HOST" ] || die "⛔ no host. Format: user@1.2.3.4, or an ssh-config alias (Host vps1)." 2

ARGS=(); NULL_TARGET=400; TARGET=""; EXECUTE=0; FROM="$SRC_WORKLIST"
while [ $# -gt 0 ]; do
  case "$1" in
    --local-sim) mkdir -p "$2"; SIM=$(cd "$2" && pwd); shift 2;;
    --null-target) NULL_TARGET=$2; shift 2;;
    --target) TARGET=$2; shift 2;;
    --from) FROM=$2; shift 2;;
    --execute) EXECUTE=1; shift;;
    *) ARGS[${#ARGS[@]}]=$1; shift;;
  esac
done
# A host string that is a path is a foot-gun; keep the SEED-OFFSET key clean.
HOSTKEY=$(printf '%s' "$HOST" | tr '/ ' '__')
GENDIR=$LOCAL_ROOT/$HOSTKEY
[ -n "$SIM" ] && say "LOCAL-SIM MODE — transport is cp/rsync into $SIM; the ssh/rsync-over-network path is NOT exercised by this run."

seed_offset() {   # crc32(host) % 50 * 1e6 — stable, auditable, pure
  "$PY" - "$1" <<'EOF'
import sys, zlib
print((zlib.crc32(sys.argv[1].encode()) % 50) * 1000000)
EOF
}

# ---------------------------------------------------------------------------
# gen — build the per-host worklist with the seed partition applied
# ---------------------------------------------------------------------------
cmd_gen() {
  [ -f "$FROM" ] || die "⛔ no source worklist at $FROM" 2
  mkdir -p "$GENDIR"
  OFF=$(seed_offset "$HOSTKEY")
  [ -n "$OFF" ] || die "⛔ could not compute the seed offset (is $PY present?)" 2

  # THE NULL PAIR IS FOUND STRUCTURALLY, NOT BY NAME — the same rule
  # overnight_read.py uses: a null cell is one whose treatment tree is
  # BYTE-IDENTICAL to its control. A convention ("call it NULLxxx") can rot; an
  # md5 cannot. If the source worklist has no such pair we REFUSE rather than
  # invent one, because a host with no null is a host whose rows cannot be
  # certified and therefore cannot be pooled.
  NULLPAIR=$("$PY" - "$FROM" <<'EOF'
import sys, pathlib
def ident(a, b):
    pa, pb = pathlib.Path(a), pathlib.Path(b)
    if not (pa.is_dir() and pb.is_dir()): return False
    fa = sorted(f.name for f in pa.glob("*.py")); fb = sorted(f.name for f in pb.glob("*.py"))
    return bool(fa) and fa == fb and all((pa/n).read_bytes() == (pb/n).read_bytes() for n in fa)
for line in pathlib.Path(sys.argv[1]).read_text().splitlines():
    if line.lstrip().startswith("#") or not line.strip(): continue
    f = line.split()
    if len(f) >= 3 and ident(f[1], f[2]):
        print(f[1], f[2]); break
EOF
)
  [ -n "$NULLPAIR" ] || die "⛔ REFUSING: no byte-identical (treatment == control) pair anywhere in $FROM, so there is no NULL cell to give this host. A host with no null cannot be certified and its rows cannot be pooled. Add a null row and re-run." 2

  OUTW=$GENDIR/worklist.txt
  {
    echo "# GENERATED by tools/vps/orchestrate.sh gen for host: $HOST"
    echo "# generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)   source: $FROM"
    echo "# SEED OFFSET APPLIED TO EVERY ROW: +$OFF   (crc32('$HOSTKEY') % 50 * 1e6)"
    echo "# ⇒ this host plays DIFFERENT seeds from every other host and from this box,"
    echo "#   so its rows are independent draws that POOL rather than replays that do not."
    echo "# NULLHOST is first and is byte-identical tree vs itself: it is the per-host"
    echo "#   certification cell (45-55% at n>=400) and the worker refuses to run"
    echo "#   anything else until it completes."
    echo "# shard  treatment  control  target  seedbase"
    echo "NULLHOST $NULLPAIR $NULL_TARGET $(( 900000 + OFF ))"
  } > "$OUTW"

  want=" ${ARGS[*]:-} "
  n=0
  while read -r SH TR CT TG SL; do
    case "${SH:-}" in ''|'#'*) continue;; esac
    if [ "${#ARGS[@]}" -gt 0 ]; then case "$want" in *" $SH "*) :;; *) continue;; esac; fi
    [ "$SH" = NULLHOST ] && continue
    T2=${TARGET:-$TG}
    echo "$SH $TR $CT $T2 $(( SL + OFF ))" >> "$OUTW"
    n=$(( n + 1 ))
  done < "$FROM"
  # `gen <host> NULLHOST` is a legal CERT-ONLY worklist (a new host's first run);
  # the die below guards the no-args and typo cases, not that one.
  if [ "$n" -eq 0 ] && [ "$want" != " NULLHOST " ]; then
    die "⛔ no shards selected from $FROM (asked for: ${ARGS[*]:-<all>}) — nothing to run. (For a certification-only worklist, ask for exactly NULLHOST.)" 2
  fi

  # MAP POOL: parsed from overnight.sh's own MAPS= line. ONE source; this is a
  # generated copy that ships, never a second hand-maintained list.
  sed -n 's/^MAPS=(\(.*\))$/\1/p' tools/overnight.sh | tr ' ' '\n' | grep -v '^$' > "$GENDIR/MAPS.list"
  [ -s "$GENDIR/MAPS.list" ] || die "⛔ could not parse MAPS= out of tools/overnight.sh — REFUSING to ship a blind pool." 2

  printf '%s\n' "$OFF" > "$GENDIR/SEED_OFFSET"
  {
    echo "host: $HOST"
    echo "hostkey: $HOSTKEY"
    echo "seed_offset: $OFF"
    echo "formula: crc32(hostkey) % 50 * 1000000"
    echo "generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "source_worklist: $FROM"
    echo "engine_pin: $(grep -v '^#' tools/ENGINE_PIN | tr -d '[:space:]')"
    echo "maps: $(tr '\n' ' ' < "$GENDIR/MAPS.list")"
    echo "shards: NULLHOST $(awk '!/^#/ && NF>=5 && $1!="NULLHOST"{printf "%s ", $1}' "$OUTW")"
  } > "$GENDIR/SEED_OFFSET.sidecar"

  say "GEN $HOST → $OUTW"
  say "  seed offset +$OFF   shards: $(( n + 1 )) (incl. NULLHOST)   maps: $(wc -l < "$GENDIR/MAPS.list" | tr -d ' ')"
  say "  sidecar: $GENDIR/SEED_OFFSET.sidecar"
}

# ---------------------------------------------------------------------------
# push — MINIMAL snapshot. Named paths only.
# ---------------------------------------------------------------------------
cmd_push() {
  W=$GENDIR/worklist.txt
  [ -f "$W" ] || die "⛔ no generated worklist for $HOST. Run: $0 gen $HOST [SHARD ...]" 2
  DEST=$(r_dest)
  # ⛔ maps/ IS WIPED AND RE-SHIPPED, NOT MERGED. The worker's G3 gate demands
  # set-EQUALITY with the pool manifest, and a merge would leave last week's
  # retired geometry sitting there — the exact failure the gate exists to catch,
  # created by the tool that installs the gate.
  r_exec "mkdir -p work results tools/vps bots maps && rm -f maps/*.map26" \
    || die "⛔ cannot reach the worker root on $HOST. Check: ssh $HOST true" 2

  # 1. the worker + the pin
  rs tools/vps/worker.sh "${DEST}tools/vps/"
  rs tools/ENGINE_PIN    "${DEST}tools/"
  # 2. the work definition
  rs "$W" "${DEST}work/worklist.txt"
  rs "$GENDIR/MAPS.list" "$GENDIR/SEED_OFFSET" "$GENDIR/SEED_OFFSET.sidecar" "${DEST}work/"
  # 3. ONLY the maps in the pool (not maps/invented, not retired geometry)
  nm=0
  while read -r m; do
    [ -f "maps/$m.map26" ] || die "⛔ pool names $m but maps/$m.map26 does not exist here — REFUSING to ship a snapshot the worker's own gate would reject." 2
    rs "maps/$m.map26" "${DEST}maps/"
    nm=$(( nm + 1 ))
  done < "$GENDIR/MAPS.list"
  # 4. ONLY the bot trees named in the worklist. __pycache__ excluded: it is
  #    stale, arch-specific and pure weight.
  TREES=$(awk '!/^#/ && NF>=5 {print $2; print $3}' "$W" | sort -u)
  nt=0
  for t in $TREES; do
    [ -f "$t/main.py" ] || die "⛔ worklist names $t but $t/main.py does not exist." 2
    rs --exclude '__pycache__' --exclude '*.pyc' "$t/" "${DEST}$t/"
    nt=$(( nt + 1 ))
  done
  say "PUSH $HOST ← worker.sh + ENGINE_PIN + worklist + $nm maps + $nt bot trees"
  say "  NOT shipped: docs/ corpus/ replay_archive/ scratchpad/ elo_history.tsv .git fcode.toml — the worker holds no credentials and no analysis surface."
  r_exec "test -f tools/vps/worker.sh && test -f work/worklist.txt && test -f tools/ENGINE_PIN" \
    || die "⛔ POST-PUSH CHECK FAILED — the snapshot is not on $HOST. (rsync exit codes lie less than most, but the presence of the LOAD-BEARING FILE is what we gate on.)" 2
  say "  post-push check: worker.sh, worklist.txt and ENGINE_PIN are present on the host"
}

# ---------------------------------------------------------------------------
# pull — results back, into the reader's remote surface
# ---------------------------------------------------------------------------
cmd_pull() {
  DST=$PULL_ROOT/$HOSTKEY
  mkdir -p "$DST"
  rs "$(r_src results)/" "$DST/" || die "⛔ pull failed from $HOST" 2
  # The worklist comes back WITH the results, so the host is self-describing:
  # the reader resolves each shard's treatment/control (and identifies the null
  # STRUCTURALLY) without needing this box's worklist to still match.
  rs "$(r_src work/worklist.txt)" "$DST/worklist.txt" 2>/dev/null || say "  ⚠ no remote worklist to pull — the reader will not be able to name this host's contrasts"
  rs "$(r_src work/SEED_OFFSET.sidecar)" "$DST/SEED_OFFSET.sidecar" 2>/dev/null || true
  say "PULL $HOST → $DST"
  for f in "$DST"/*.tsv; do
    [ -f "$f" ] || continue
    printf '   %-14s rows=%s\n' "$(basename "$f" .tsv)" "$(( $(wc -l < "$f") - 1 ))"
  done
  say "  read it:  $PY tools/overnight_read.py --include-remote"
}

# ---------------------------------------------------------------------------
# status — rows, heartbeat AGE, load. Never a bare number.
# ---------------------------------------------------------------------------
cmd_status() {
  # ⛔ EVERY NUMBER CARRIES ITS AGE. `ship_watch` once printed a healthy line off
  # a seven-minute-stale tape and a HEALTHY line and a BLIND line were
  # byte-identical. A heartbeat older than ~10 min with no worker process is
  # DEAD, not "in progress".
  r_exec '
    echo "host: $(hostname)   utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)   NPROC: $(nproc 2>/dev/null || echo UNKNOWN)"
    if [ -r /proc/loadavg ]; then echo "load: $(cut -d" " -f1-3 /proc/loadavg)"; else echo "load: $(uptime | sed "s/.*averages*: *//")"; fi
    echo "runners: $(ps ax -o command= 2>/dev/null | grep -c "[f]code run")   worker: $(ps ax -o command= 2>/dev/null | grep -c "[w]orker.sh")"
    [ -f STOP ] && echo "*** STOP FILE PRESENT ***"
    now=$(date -u +%s)
    printf "%-14s %8s %8s %10s %s\n" SHARD ROWS TARGET HB_AGE STATUS
    for f in results/*.heartbeat; do
      [ -f "$f" ] || continue
      sh=$(basename "$f" .heartbeat)
      rows=$(( $(wc -l < "results/$sh.tsv" 2>/dev/null || echo 1) - 1 ))
      mt=$(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f" 2>/dev/null || echo 0)
      age=$(( now - mt ))
      st=$(awk -F"\t" "{print \$5}" "$f")
      tg=$(awk -F"\t" "{print \$3}" "$f")
      [ "$age" -gt 600 ] && st="$st  ⚠ STALE(${age}s) — a frozen heartbeat is BLIND, not healthy"
      printf "%-14s %8s %8s %9ss %s\n" "$sh" "$rows" "$tg" "$age" "$st"
    done
    ls results/*.heartbeat >/dev/null 2>&1 || echo "(no shards have started yet)"
  '
}

# ---------------------------------------------------------------------------
# setup — PRINT by default. --execute to run.
# ---------------------------------------------------------------------------
cmd_setup() {
  PIN=$(grep -v '^#' tools/ENGINE_PIN | tr -d '[:space:]')
  SCRIPT="set -e
mkdir -p '$REMOTE_ROOT'/work '$REMOTE_ROOT'/results '$REMOTE_ROOT'/tools/vps
cd '$REMOTE_ROOT'
command -v rsync >/dev/null 2>&1 || { echo '⛔ rsync missing — needs root once: apt-get install rsync'; exit 5; }
# fcode ships compiled cp312/cp313 manylinux wheels ONLY — a 3.9 box reads
# 'from versions: none' (work-server-1, 2026-08-14). If system python is too
# old, bootstrap a standalone CPython via uv: rootless, no admin round-trip.
PYOK=\$(python3 -c 'import sys; print(1 if sys.version_info >= (3,12) else 0)' 2>/dev/null || echo 0)
if [ \"\$PYOK\" = 1 ]; then
  [ -x .venv/bin/pip ] || { rm -rf .venv; python3 -m venv .venv || true; }  # gate on the LOAD-BEARING file — a dir from a failed create is not a venv
fi
if ! { [ -x .venv/bin/pip ] && .venv/bin/python -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 1)' 2>/dev/null; }; then
  # python too old (work-server-1: 3.9) OR venv module crippled (work-server-2,
  # 2026-08-14: 3.12 present but python3.12-venv/ensurepip absent) — either way
  # the rootless uv bootstrap is the fallback; gate stays the LOAD-BEARING file.
  export PATH=\"\$HOME/.local/bin:\$PATH\"
  command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh -s -- -q
  uv python install 3.12 -q
  rm -rf .venv; uv venv -q --seed --python 3.12 .venv
fi
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet 'fcode==$PIN'
echo \"python: \$(python3 --version)\"
echo \"fcode : \$(.venv/bin/fcode --version)\"
echo \"cores : \$(nproc)\"
echo \"PIN   : $PIN\"
.venv/bin/fcode --version | grep -q ' $PIN\$' && echo 'ENGINE PIN OK' || { echo '⛔ ENGINE PIN MISMATCH after install'; exit 4; }"

  if [ "$EXECUTE" -eq 0 ]; then
    cat <<EOF
── SETUP (PRINT-ONLY. add --execute to actually run it on $HOST) ──────────────
Idempotent: safe to re-run. Installs python3+venv only if missing, then pins
fcode to tools/ENGINE_PIN ($PIN). It does NOT copy any credential — there is
nothing to copy: \`fcode run\` is offline.

ssh $HOST '<<the script below>>'

$SCRIPT
───────────────────────────────────────────────────────────────────────────────
Then:  $0 gen $HOST <SHARD...> && $0 push $HOST && $0 start $HOST
EOF
    return 0
  fi
  # ⛔ REFUSE IN SIM. `setup --execute` runs `apt-get` and builds a venv; pointed
  # at a local simulation directory it would run those against THIS machine.
  # A mode that silently does something different is worse than one that refuses.
  [ -n "$SIM" ] && die "⛔ REFUSING: setup --execute is meaningless under --local-sim (it would apt-get and build a venv on THIS box). The print-only form is what the sim can check." 2
  say "SETUP --execute on $HOST"
  r_exec_home "$SCRIPT"
}

# ---------------------------------------------------------------------------
# start / stop
# ---------------------------------------------------------------------------
# ⛔ THE CURFEW IS PER-HOST AND IT WAS NOT. `worker.sh`'s blackout was written for
# work-server-1, whose owners need that box 23:00-06:00 CET (Magnus, 2026-08-14)
# -- but the check is unconditional and names no host, so it applied to EVERY
# fleet box. Measured consequence, same day: work-server-2 was stocked with two
# 5400-game shards, passed all four gates, skipped its already-passed NULLHOST,
# and then went straight to `curfew: sleeping` -- **six cores idle until 04:00Z
# on a box with no curfew on record**, at the moment the principal had said
# "use local and work-server-2 cores". A rule copied from one host to all hosts
# is not a stricter rule, it is a wrong one.
# ⇒ NO_CURFEW_HOSTS names the hosts EXPLICITLY CLEARED to run around the clock.
# **Anything not on that list defaults to CURFEW=on.** The two errors are not
# symmetric: wrong-toward-SLEEPING costs us cores, wrong-toward-RUNNING costs
# somebody else their machine at midnight. So the default is the expensive one,
# and clearing a host is a deliberate act with a name attached.
# ⚠ The list is phrased as the EXEMPTION, not the rule, on purpose. A first cut
# here used `CURFEW_HOSTS` (hosts that HAVE one) and its unlisted default came
# out OFF -- while the comment above it claimed ON. Prose contradicting the code
# beside it, in a block written to fix exactly that class. Caught by driving the
# selector on a third, unlisted hostname before touching any box.
NO_CURFEW_HOSTS=${NO_CURFEW_HOSTS:-work-server-2}
cmd_start() {
  W=${ARGS[0]:-}
  # ⛔⛔ SIZE WORKERS AGAINST OUR ALLOCATION, NEVER AGAINST nproc. `nproc` reports
  # the MACHINE; on work-server-1 it says 16 while our user may use 10. Sizing off
  # it puts a shard at 1.6x oversubscribed — the SALTREF2 condition, which moved a
  # byte-identical null 2.67pp and is why the original SALTREF null did not
  # replicate. Added s44 after I started a host-term NULL on a 6-core box at
  # WORKERS=10 (1.67x) because I had assumed a core count I never measured.
  CAP_F="scratchpad/vps/host_capacity.tsv"
  if [ -n "$W" ] && [ -r "$CAP_F" ]; then
    # ⛔ MATCH ON THE BARE HOSTNAME. $HOST is whatever the caller typed —
    # "work-server-1" or "worker@work-server-1" — while the table is keyed with
    # the user prefix. My first cut compared them literally and REFUSED ALL THREE
    # test cells including the legal one: a guard that refuses everything, which
    # is the exact class flagged in this repo hours earlier. Strip the prefix on
    # both sides so the comparison is on the thing that identifies the machine.
    _hb=${HOST#*@}
    CORES=$(awk -v h="$_hb" '$1 !~ /^#/ { k=$1; sub(/^.*@/,"",k); if (k==h) { print $3; exit } }' "$CAP_F")
    if [ -z "$CORES" ]; then
      say "⛔ REFUSING: $HOST has no row in $CAP_F. Add its allocation (NOT its nproc) before starting."
      exit 2
    fi
    if [ "$W" -gt "$CORES" ]; then
      say "⛔ REFUSING: WORKERS=$W exceeds our allocation of $CORES cores on $HOST (oversubscription is the SALTREF2 defect)."
      say "   Pass WORKERS <= $CORES, or correct $CAP_F if the allocation actually changed."
      exit 2
    fi
    say "capacity check: WORKERS=$W <= our allocation $CORES on $HOST — OK"
  fi
  WK=""
  [ -n "$W" ] && WK="WORKERS=$W "
  # ⛔⛔ LOAD_CEIL MUST BE SIZED ON OUR ALLOCATION, NOT ON THE BOX'S nproc.
  # `worker.sh` defaults it to NCPU + NCPU/4, and NCPU there is `nproc` — THE
  # MACHINE. On work-server-1 that is 16, so the ceiling defaulted to 20 while
  # OUR SLICE IS 10: the worker would happily keep launching until the box was
  # at twice our allocation. That is precisely the nproc-vs-allocation confusion
  # `host_capacity.tsv` was created to end — it was enforced on WORKERS (with a
  # hard refusal, above) and silently NOT on the ceiling, so the guard covered
  # the launch count and not the thing the launch count is guarding against.
  # Measured 2026-08-15 on ws1: `WORKER up. ncpu=16 workers=10 load_ceil=20`.
  # No damage had occurred (0 NOWINNER in 57,139 rows) — this closes it before
  # a noisy neighbour makes it matter, since `--tle 10` is WALL-CLOCK and
  # oversubscription corrupts rows rather than merely slowing them.
  if [ -n "$CORES" ]; then
    WK="${WK}LOAD_CEIL=$(( CORES + CORES / 4 )) "
    say "load ceiling for $HOST: $(( CORES + CORES / 4 )) (allocation $CORES + 25%), NOT nproc-derived"
  fi
  CF="on"
  case " $NO_CURFEW_HOSTS " in
    *" ${HOST#*@} "*) CF="off";;
  esac
  say "curfew for ${HOST#*@}: $CF   (round-the-clock hosts: $NO_CURFEW_HOSTS; everything else curfews by default)"
  WK="${WK}CURFEW=$CF "
  r_exec "rm -f STOP; ${WK}nohup bash tools/vps/worker.sh > worker.out 2>&1 & echo \"started pid \$!\""
  say "STARTED on $HOST (nohup). Watch: $0 status $HOST"
  say "  tmux alternative:  ssh $HOST 'tmux new -d -s fcw \"cd $REMOTE_ROOT && ${WK}bash tools/vps/worker.sh\"'"
}
cmd_stop() {
  r_exec "touch STOP; echo 'STOP written — the worker halts at the next batch boundary and KEEPS its rows'"
  say "STOP requested on $HOST. It halts at a batch boundary; partial rows are kept and remain readable."
}
# ⛔ `stop` CANNOT REACH A CURFEWED WORKER, AND THAT IS WHY THIS EXISTS.
# `worker.sh` calls curfew_wait() BEFORE its STOP check, and curfew_wait sleeps
# in a 300s loop. So a worker inside the blackout never reaches the STOP test:
# `stop` is silently a no-op until the window ends. Measured 2026-08-14 —
# work-server-2 sat curfewed with 6 idle cores and two stocked shards, and
# `stop` could not have freed it before 04:00Z.
# ⚠ AND `stop` + `start` IS NOT A SUBSTITUTE, it is worse: cmd_start does
# `rm -f STOP`, so the OLD sleeping worker wakes into a world with no STOP file
# and launches its own WORKERS alongside the new ones — double-subscribing a
# shared box. `--tle 10` is WALL-CLOCK, so that silently corrupts every row both
# workers produce. Killing the process is the only correct sequence.
# Rows are never touched: the worker holds no state a SIGTERM can lose, and
# nothing in this pipeline deletes results.
cmd_kill() {
  r_exec "pkill -f 'tools/vps/worker.sh' 2>/dev/null; sleep 1; n=\$($WCOUNT_CMD); echo \"workers remaining: \$n\"; ls results/*.tsv 2>/dev/null | wc -l | xargs echo 'result tapes still present:'"
  say "KILL sent to $HOST. Verify 'workers remaining: 0' above — a nonzero count means it did NOT die and you must not start another."
}

case "$CMD" in
  gen)    cmd_gen;;
  push)   cmd_push;;
  pull)   cmd_pull;;
  status) cmd_status;;
  setup)  cmd_setup;;
  start)  cmd_start;;
  log)    r_exec "tail -n \${LOGN:-40} worker.log worker.out 2>/dev/null || echo 'no worker.log/worker.out yet'";;
  # reset-done <host> <SHARD> — remove ONLY the .COMPLETE marker so a raised
  # TARGET can extend a finished shard (rows/heartbeat kept; A5-extension case).
  reset-done)
    SH=${ARGS[0]:?reset-done needs a SHARD name}
    r_exec "if [ -f results/$SH.COMPLETE ]; then rm results/$SH.COMPLETE && echo \"removed results/$SH.COMPLETE (rows kept: \$(wc -l < results/$SH.tsv))\"; else echo \"no results/$SH.COMPLETE on this host\"; fi";;
  # cancel <host> <SHARD> <reason> — THE PER-SHARD REMOTE CANCEL, and it exists
  # because there was none. `stop`/`kill` halt the WHOLE worker; the only
  # per-shard lever was the `.COMPLETE` marker, which the worker checks at shard
  # START (worker.sh:249). That gap is why `auto_gate.py --apply` refuses remote
  # shards outright — so the auto-stopper could not act on 2 of our 3 hosts, and
  # every remote stop was a human doing this sequence by hand.
  #
  # ⛔ THE MARKER SAYS "CANCELLED", NEVER "reached n/TARGET". worker.sh:350
  # writes the latter and it CERTIFIES A COMPLETED RUN. Hand-writing that form
  # for a shard stopped at 4620/5400 would put a false completion certificate on
  # the tape, and every downstream reader that trusts `.COMPLETE` would count a
  # cancelled arm as a finished one. Rows are KEPT either way — what differs is
  # what the marker CLAIMS about them.
  cancel)
    SH=${ARGS[0]:?cancel needs a SHARD name}
    RSN=${ARGS[1]:-unspecified}
    # G1: refuse while the worker lives. The marker is only read at shard start,
    # so cancelling a RUNNING shard silently does nothing — the caller would get
    # a success message and no effect. `kill` first, deliberately.
    # G2: refuse an unknown shard name. A typo would otherwise write a marker
    # that suppresses a shard nobody meant to touch, and leave no trace.
    r_exec "
      n=\$($WCOUNT_CMD)
      if [ \"\$n\" -ne 0 ]; then
        echo \"⛔ REFUSING: \$n worker(s) still alive. The .COMPLETE marker is read at shard START only,\"
        echo \"   so cancelling now would report success and change nothing. Run 'kill $HOST' first.\"
        exit 3
      fi
      # G2: the shard must be KNOWN to this host — either it has run (a tape) or
      # it is parked in the worklist waiting to run. ⛔ THE WORKLIST HALF WAS
      # MISSING and the guard was too strict because of it: cancelling an
      # UNSTARTED but QUEUED shard is exactly the case you need when a row is
      # withdrawn before its turn comes up, and the tape-only test refused it
      # while offering no alternative. Still refuses a genuine typo, which is
      # the thing G2 exists for.
      if [ ! -f results/$SH.tsv ] && ! grep -q \"^$SH[[:space:]]\" work/worklist.txt 2>/dev/null; then
        echo \"⛔ REFUSING: $SH is unknown here — no results/$SH.tsv and no worklist row.\"
        ls results/*.tsv 2>/dev/null | head -10 | sed 's/^/   ran: /'
        grep -v '^#' work/worklist.txt 2>/dev/null | awk '{print \$1}' | head -10 | sed 's/^/   queued: /'
        exit 4
      fi
      if [ -f results/$SH.COMPLETE ]; then
        echo \"already marked: \$(cat results/$SH.COMPLETE)\"; exit 0
      fi
      rows=\$(grep -vc '^#' results/$SH.tsv 2>/dev/null || echo 0)
      printf '%s %s CANCELLED at %s rows by: %s -- rows KEPT, this is NOT a completed run\n' \
        \"\$(date -u +%Y-%m-%dT%H:%M:%SZ)\" '$SH' \"\$rows\" '$RSN' > results/$SH.COMPLETE
      echo \"cancelled $SH at \$rows rows; marker written:\"; sed 's/^/   /' results/$SH.COMPLETE
    "
    rc=$?
    [ "$rc" -eq 0 ] && say "$SH will be SKIPPED on the next start of $HOST; its rows remain readable." \
                    || say "cancel did NOT take on $HOST (rc=$rc) — read the refusal above."
    exit $rc;;
  stop)   cmd_stop;;
  kill)   cmd_kill;;
  *) die "unknown subcommand '$CMD'. one of: gen push pull status setup start stop kill" 2;;
esac
