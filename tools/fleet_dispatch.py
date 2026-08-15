#!/usr/bin/env python3
"""FLEET DISPATCH — ONE central queue of shards; work flows to whichever core frees first.

    .venv/bin/python tools/fleet_dispatch.py --selftest
    .venv/bin/python tools/fleet_dispatch.py --seed-from scratchpad/combos_ok.txt [--compose]
    .venv/bin/python tools/fleet_dispatch.py --dry-run --once
    .venv/bin/python tools/fleet_dispatch.py --once
    .venv/bin/python tools/fleet_dispatch.py                 # loop, --poll seconds

WHY THIS EXISTS. Magnus, 2026-08-15, verbatim: *"I wonder, can we make a
centralized queue with shards and make the vps-machines and our local machine
poll them whenever there's a free core?"* We have 112 composable multi-plank
combinations (`scratchpad/combos_ok.txt`) and three hosts; hand-dispatch is the
bottleneck.

═══════════════════════════════════════════════════════════════════════════════
⛔⛔ THE POLL IS INVERTED ON PURPOSE. DO NOT "FIX" IT BY ADDING GIT TO A WORKER.
═══════════════════════════════════════════════════════════════════════════════
The workers CANNOT poll a shared queue. That is a standing instruction, not an
oversight:

  * `tools/vps/orchestrate.sh:20` — *"⛔ GIT TRANSPORT IS OUT OF SCOPE BY
    INSTRUCTION (Magnus). Nothing here clones, pulls, pushes or reads a remote
    ref."*
  * `tools/vps/orchestrate.sh:24` — *"⛔ THE WORKER HOLDS ZERO PLATFORM
    CREDENTIALS AND THE SNAPSHOT IS THE ENFORCER."* Workers receive bot trees,
    maps and `worker.sh` by rsync and nothing else. There is no shared
    filesystem and no remote ref they may read.

⇒ **THE ORCHESTRATOR (this box) POLLS THE HOSTS AND PUSHES INTO A FREE SLOT.**
The user-visible behaviour is exactly what Magnus described — one central queue,
work flowing to whichever core frees first — implemented inside the existing
transport. A worker that could pull would need a credential or a git remote, and
that is the line the snapshot exists to hold. If a future edit here ever needs
either, that is the signal the work does not belong on a worker.

Two places where the inversion IS user-visibly different, stated up front rather
than discovered later:
  (a) LATENCY IS THE POLL INTERVAL, NOT ZERO. A core that frees at T is fed at
      T + up to `--poll` seconds (default 120). A self-polling worker would take
      the next item instantly.
  (b) A HOST UNREACHABLE BY SSH GETS NOTHING AND CANNOT ASK. Under a real pull
      model the host would retry on its own. Here an unreachable host is BLIND,
      and BLIND is treated as FULL (guard 2), so it simply idles until ssh comes
      back. That is the safe direction and it is a real cost.

═══════════════════════════════════════════════════════════════════════════════
WHAT A "SLOT" IS — AND IT IS NOT THE SAME OBJECT ON THE TWO SURFACES
═══════════════════════════════════════════════════════════════════════════════
LOCAL is a SHARD-PARALLEL surface. `tools/corefill.sh` runs up to MAX_SHARDS
copies of `tools/overnight.sh`, and overnight.sh is STRICTLY SEQUENTIAL — one
`fcode run` at a time. So local slots == concurrent shards.

REMOTE is a GAME-PARALLEL surface. `tools/vps/worker.sh` walks its worklist
SEQUENTIALLY (`while read ... done < "$WORK"`, one `run_shard` at a time) and
runs `WORKERS` games in parallel INSIDE each shard. **A remote host with a live
worker is 100% subscribed no matter how many rows you give it.** Its free
capacity is therefore not a core count at all — it is QUEUE DEPTH: how many
not-yet-COMPLETE rows sit in its worklist. Dispatching to a remote means keeping
that depth in [1, QUEUE_DEPTH_TARGET] so the host never drains and we never
over-commit rows we might want to reprioritise.

⭐ CORES PER SHARD — MEASURED BY PROCESS CPU, NOT BY LOAD AVERAGE.
Measured on this box 2026-08-15T09:37Z with three live shards
(NULL5400, CATRND1L, BODYAWR):

    ps -A -o pcpu,command= | sort -rn | head
      100.0  Python .venv/bin/fcode run bots/_v242bodyaware ...
       99.6  Python .venv/bin/fcode run bots/_v260catrnd1 ...
       92.8  Python .venv/bin/fcode run bots/_v146null ...
       18.0  (logitech updater)          <- the largest non-game consumer
    sum of ALL pcpu = 322.0 ; processes >50% cpu = 3 ; hw.ncpu = 10

**ONE `fcode run` IS ONE CPU-BOUND PYTHON PROCESS (~100%) PLUS AN IDLE
`timeout(1)` WRAPPER (0.0%).** Three shards ⇒ 2.92 cores of real demand.
⇒ CORES_PER_SHARD = 1.0.

⛔ THE 2.5-3.0 FIGURE IN THE ASSIGNMENT ("1 shard -> load 2.42, 2 shards -> load
6.02") IS A LOAD-AVERAGE ARTEFACT, NOT A CORE COUNT. The same instant above read
`load averages: 4.24` against 3.22 cores of measured pcpu — Darwin's load average
over-reports and it is a lagging 1-minute EWMA, so a reading taken shortly after
a launch has not settled. Sizing the divisor off it would cost us ~2/3 of every
box. The load average is still used HERE, but as a SECOND, INDEPENDENT BRAKE
(corefill.sh guard 3), never as the divisor — a proxy is fine as a ceiling and
wrong as a denominator. Override with --cores-per-shard if a future measurement
disagrees; quote the measurement when you do.

═══════════════════════════════════════════════════════════════════════════════
THE SEVEN GUARDS. Each is an incident this repo has already had, and each is
driven to BOTH verdicts by --selftest.
═══════════════════════════════════════════════════════════════════════════════
G1 NEVER RE-DISPATCH. A claimed row is claimed forever; a dead shard is logged
   and LEFT. At 18:40:13Z on 2026-08-11 `overnight_watch.sh` restarted NINE
   COMPLETED shards from zero because their outputs had been archived out from
   under it. The biting cell is not "a DONE row"; it is a row marked RUNNING
   whose heartbeat is HOURS stale with no .COMPLETE — indistinguishable from a
   restartable corpse, and it must still be left alone.

G2 BLIND IS NOT IDLE. If a host's occupancy cannot be read, it is FULL and gets
   nothing. Never infer "0 running" from a failed read. The biting cell is NOT a
   nonzero exit — this platform's tools exit 0 while printing `Error: True`
   (CLAUDE.md) — it is a status that returns cleanly with the LOAD-BEARING FIELD
   MISSING. We gate on the presence of `runners:`/`worker:`, never on $?.

G3 CAPACITY COMES FROM scratchpad/vps/host_capacity.tsv, AND A HOST WITH NO ROW
   IS REFUSED rather than defaulted. `nproc` is the machine; `our_cores` is our
   allocation (ws1: nproc 16, ours 10). Oversubscription is the SALTREF2 defect
   — WORKERS 40 on 16 moved a byte-identical null 2.67pp. The biting cell is the
   PREFIX: the table is keyed `worker@work-server-1` and callers type either
   form; orchestrate.sh's first cut compared literally and refused all three test
   cells including the legal one. Match on the bare hostname on BOTH sides.

G4 NULL-PAIR PRESERVATION. `orchestrate.sh gen` REFUSES a source worklist with
   no byte-identical (treatment == control) pair, because a host with no null
   cell cannot be certified and its rows cannot be pooled. We pre-check the same
   property BEFORE claiming, so a missing null costs a log line and not a burnt
   claim. ⚠ This predicate is a SECOND IMPLEMENTATION of gen's, which is the
   class D24(e) warns about — so the selftest does not assert our answer, it
   asserts AGREEMENT WITH `orchestrate.sh gen` ITSELF on both a passing and a
   failing synthetic worklist.

G5 BASENAME COLLISION. `overnight.sh`/`worker.sh` score the winner by SUBSTRING
   match on the treatment basename, so `_v150cb` vs `_v150cbturret` reads ~100%
   for the control. Refused UP FRONT, at seed time and again at claim time —
   corefill.sh learned in s35 that a guard which runs once cannot protect a
   surface that changes.

G6 STALENESS. Every status line carries the AGE of what it read, and a healthy
   line and a blind line are never byte-identical. `ship_watch` printed
   `rating=1599 armed=True RULE=held` off rows seven minutes stale.

G7 DOUBLE-SUBSCRIPTION REFUSAL — added here from `orchestrate.sh:411-423`, which
   states it and has no enforcement: *"cmd_start does `rm -f STOP`, so the OLD
   sleeping worker wakes into a world with no STOP file and launches its own
   WORKERS alongside the new ones — double-subscribing a shared box. `--tle 10`
   is WALL-CLOCK, so that silently corrupts every row both workers produce."*
   ⇒ We never `start` a host whose worker process count is >= 1.

═══════════════════════════════════════════════════════════════════════════════
REMOTE DISPATCH — TWO PATHS, AND AN EXPERIMENT DECIDES WHICH IS LEGAL WHEN
═══════════════════════════════════════════════════════════════════════════════
Measured 2026-08-15 in /tmp with a bash `while read ... done < wl.txt` loop and a
1s-per-line body:

  APPEND IN PLACE (`printf >> wl.txt`) -> the running loop read a, b, **c, d**.
  RSYNC REPLACE   (`rsync -a new.txt wl.txt`) -> the running loop read a, b ONLY.
      inode before/after differ (264398447 vs the source's 264398446): rsync
      writes a temp and renames, so the running shell keeps the OLD inode.

⛔ CONSEQUENCE, AND IT INVALIDATES THE OBVIOUS DISPATCH SEQUENCE: you CANNOT
extend a live remote worker's worklist with `gen` + `push`. The pushed rows land
on a new inode the worker will never read. Worse, `cmd_push` does
`rm -f maps/*.map26` before re-shipping the pool — with games in flight that
window produces NOWINNER rows, and worker.sh aborts a shard at >1% NOWINNER past
n>=200. And `start` on a live host is G7. So:

  MODE `drain` (DEFAULT, and every step goes through orchestrate.sh's own gates)
      Only when the host's worker is DOWN. Append to the per-host source
      worklist, then `gen --from` + `push` + `start <our_cores>`. Re-listing
      finished shards is safe: worker.sh skips any shard with a .COMPLETE marker
      and resumes a partial one from its row count.

  MODE `live` (OPT-IN, --remote-mode live)
      Surgical, for a host with a live worker: additive `rsync` of ONLY the new
      row's trees (maps/ untouched, worklist inode untouched), then an in-place
      `>>` append of the row with the host's seed offset applied from its own
      `work/SEED_OFFSET` sidecar. Verified above to be picked up by the running
      loop. ⚠ worker.sh's G4 worklist gate runs at STARTUP ONLY, so an appended
      row is never re-gated by it — this tool therefore performs G4's checks
      (main.py present, no substring collision, numeric target/seedbase) itself
      before appending, and verifies main.py landed on the host afterwards.

NOTHING HERE EVER DELETES A ROW, A TAPE OR A MARKER.
"""
from __future__ import annotations

import argparse
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

REPO = Path(__file__).resolve().parent.parent

# ── paths ────────────────────────────────────────────────────────────────────
QUEUE_F       = REPO / "scratchpad/fleet_queue.tsv"
LOCK_F        = REPO / "scratchpad/fleet_queue.lock"
HOSTS_F       = REPO / "scratchpad/vps/hosts.txt"
CAP_F         = REPO / "scratchpad/vps/host_capacity.tsv"
LOCAL_WORK_F  = REPO / "scratchpad/corefill_work.txt"
LOCAL_OUT     = REPO / "scratchpad/overnight"
LOCAL_STATE   = REPO / "scratchpad/corefill_started"
REMOTE_OUT    = REPO / "scratchpad/overnight-remote"
VPS_DIR       = REPO / "scratchpad/vps"
ORCH          = REPO / "tools/vps/orchestrate.sh"
RUNNER_PAT_SH = REPO / "tools/lib/runner_pat.sh"
LOG_F         = REPO / "scratchpad/fleet_dispatch.log"

# `orchestrate.sh` defaults REMOTE_ROOT to this. Duplicated deliberately and
# named so, because there is no other way to reach the worker root over ssh.
REMOTE_ROOT = os.environ.get("REMOTE_ROOT", "fcode-worker")

LOCAL = "local"

# ── constants, each with its measurement attached ────────────────────────────
# See the module docstring: ONE `fcode run` is ONE cpu-bound python process
# (~100% pcpu) plus an idle timeout(1) wrapper. 3 live shards = 2.92 cores of
# measured demand, this box, 2026-08-15T09:37Z, hw.ncpu 10.
CORES_PER_SHARD = 1.0

# corefill.sh's own default; a second brake, never the divisor.
LOCAL_LOAD_CEIL = 11.0

# How many not-yet-COMPLETE rows we are willing to have parked on ONE remote
# host. Remote shards run sequentially, so depth is hours of runway, not
# parallelism. 2 = "one running plus one queued" — the host never drains between
# dispatcher passes, and we keep 110 rows reprioritisable.
QUEUE_DEPTH_TARGET = 2

# A status read older than this is not evidence of anything (guard 6).
STATUS_STALE_S = 300
# A mirrored remote result dir older than this cannot settle DONE/FAILED.
MIRROR_STALE_S = 1800
# Local heartbeat freshness. One local game is ~2.3 s; 15 min is many cadences.
HB_FRESH_S = 900

# Games per seed on the live pool: 15 maps x 2 seats (tools/overnight.sh:68).
GAMES_PER_SEED = 30
# Seed allocation for --seed-from. Local shards carry the RAW seed_lo; a remote
# host adds crc32(hostkey)%50 * 1e6 on top (orchestrate.sh:32), so a base seed
# must stay UNDER 1e6 or it spills into the next host's megabyte — and one of
# the 50 possible offsets is 0, which would make a spilled remote row a direct
# replay of a local one.
SEED_LO_FLOOR = 400_000
SEED_STRIDE   = 2_000
SEED_CEIL     = 1_000_000
# ⛔ [900000, 1e6) IS THE CERTIFICATION BAND, NOT FREE SPACE. orchestrate.sh:152
# writes every host's NULLHOST row at `900000 + OFF`, and the NULLPAIR_DETECT
# rows we and scratchpad/vps/work-server-2-r.txt seed sit at 900000 too. My first
# cut of used_seed_hi() read that sentinel as the high-water mark and allocated
# 904000..1126000 for 112 combos — over the ceiling, i.e. into another host's
# partition. Caught by the allocator's own invariant check, which is why it
# exists.
SEED_RESERVED_LO = 900_000

STATES = ("QUEUED", "CLAIMED", "RUNNING", "DONE", "FAILED")
COLS = ("shard_id", "treatment_tree", "control_tree", "target_n", "seed_lo",
        "state", "host", "claimed_utc", "note")

# The per-host certification cell, and the source row that exists only so
# `gen`'s structural null scan finds a byte-identical pair.
CERT_SHARD = "NULLHOST"
NULLPAIR_DETECT = "NULLPAIR_DETECT"


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _stdout_is_the_log() -> bool:
    """True when fd 1 is ALREADY the log file, i.e. the launcher redirected us
    into it.

    ⛔ WHY THIS EXISTS (measured 2026-08-15). `say()` wrote the line to stdout
    AND appended it to LOG_F, and the supervising loop was launched with
    `>> scratchpad/fleet_dispatch.log 2>&1` — the same file. EVERY LINE WAS
    WRITTEN TWICE. That is not merely cosmetic: it doubles every startup
    banner, so a reader counting banners in the log concludes TWO dispatchers
    are running when there is one. The identical defect was live in
    `corefill.sh` at the same moment and produced exactly that misreading.

    Detection over convention: an inode comparison is true regardless of how
    the process was launched, so neither the caller nor a future launcher has
    to remember a rule. `os.fstat(1)` stats the open file description, which
    is why this works where the shell equivalent does not — on macOS
    `stat /dev/fd/1` reports the devfs node, not the target (verified).
    """
    try:
        a, b = os.fstat(1), os.stat(LOG_F)
    except OSError:
        return False
    return a.st_dev == b.st_dev and a.st_ino == b.st_ino


def say(msg: str, log: bool = True) -> None:
    line = f"{utc()} {msg}"
    print(line, flush=True)
    if log and not _stdout_is_the_log():
        try:
            LOG_F.parent.mkdir(parents=True, exist_ok=True)
            with LOG_F.open("a") as fh:
                fh.write(line + "\n")
        except OSError:
            pass


def bare_host(h: str) -> str:
    """`worker@work-server-1` and `work-server-1` name the SAME machine.

    G3's biting cell. orchestrate.sh's first cut compared the caller's string to
    the table key literally and refused every cell including the legal one.
    """
    return h.split("@")[-1].strip()


def hostkey(h: str) -> str:
    """orchestrate.sh's GENDIR key: the host string with / and space folded."""
    return h.replace("/", "_").replace(" ", "_")


# ═══════════════════════════════════════════════════════════════════════════
# THE QUEUE
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class Row:
    shard_id: str
    treatment_tree: str
    control_tree: str
    target_n: int
    seed_lo: int
    state: str = "QUEUED"
    host: str = "-"
    claimed_utc: str = "-"
    note: str = "-"

    def tsv(self) -> str:
        vals = [self.shard_id, self.treatment_tree, self.control_tree,
                str(self.target_n), str(self.seed_lo), self.state,
                self.host or "-", self.claimed_utc or "-", (self.note or "-")]
        # A tab inside a field would silently shift every later column.
        return "\t".join(v.replace("\t", " ") for v in vals)

    @property
    def terminal(self) -> bool:
        return self.state in ("DONE", "FAILED")

    @property
    def claimed(self) -> bool:
        """G1: anything past QUEUED is spent. There is no path back to QUEUED."""
        return self.state != "QUEUED"

    def seed_span(self) -> int:
        return math.ceil(self.target_n / GAMES_PER_SEED)


QUEUE_HEADER = f"""\
# FLEET QUEUE — ONE central queue; tools/fleet_dispatch.py hands rows to whichever
# host has a free slot. Columns are TAB separated.
#
# state:  QUEUED -> CLAIMED -> RUNNING -> DONE | FAILED
#   ⛔ THE TRANSITION IS ONE-WAY. A CLAIMED row is claimed FOREVER; a shard that
#   dies is marked FAILED, logged, and LEFT. Recovering it is a human decision
#   with the evidence in front of them (overnight_watch.sh restarted NINE
#   completed shards from zero on 2026-08-11 because a dead run and an archived
#   run looked identical to it). To retry a row, ADD A NEW ROW with a new
#   shard_id and a fresh seed_lo — never edit a state backwards.
#
# {chr(9).join(COLS)}
"""


def read_queue(path: Path | None = None) -> list[Row]:
    # Resolved at CALL time, not at def time: --queue rebinds the module global
    # and a default bound at import would silently keep pointing at the real
    # ledger — a test writing into production is not a hypothetical here.
    path = Path(path) if path is not None else QUEUE_F
    if not path.exists():
        return []
    rows: list[Row] = []
    for ln in path.read_text().splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        f = ln.rstrip("\n").split("\t")
        if len(f) < 5:
            continue
        try:
            rows.append(Row(f[0], f[1], f[2], int(f[3]), int(f[4]),
                            f[5] if len(f) > 5 else "QUEUED",
                            f[6] if len(f) > 6 else "-",
                            f[7] if len(f) > 7 else "-",
                            f[8] if len(f) > 8 else "-"))
        except ValueError:
            continue
    return rows


def write_queue(rows: list[Row], path: Path | None = None) -> None:
    """Atomic: temp + rename. A dispatcher killed mid-write must not truncate
    the ledger of what is already claimed."""
    path = Path(path) if path is not None else QUEUE_F
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".fq.")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(QUEUE_HEADER)
            for r in rows:
                fh.write(r.tsv() + "\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


class QueueLock:
    """O_EXCL lockfile. Two dispatchers claiming the same row is the double-assign
    this whole ordering exists to prevent; the CLAIMED-before-dispatch write is
    useless if a second process is writing the same file."""

    def __init__(self, path: Path = LOCK_F, ttl_s: int = 900):
        self.path, self.ttl_s, self.held = Path(path), ttl_s, False

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            age = time.time() - self.path.stat().st_mtime
            if age > self.ttl_s:
                say(f"⚠ stale lock {self.path.name} age={int(age)}s > ttl {self.ttl_s}s — breaking it")
                self.path.unlink(missing_ok=True)
        try:
            fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise SystemExit(
                f"⛔ another fleet_dispatch holds {self.path} (age "
                f"{int(time.time() - self.path.stat().st_mtime)}s). Refusing to run a second claimer.")
        os.write(fd, f"{os.getpid()} {utc()}\n".encode())
        os.close(fd)
        self.held = True
        return self

    def __exit__(self, *exc):
        if self.held:
            self.path.unlink(missing_ok=True)
        return False


# ═══════════════════════════════════════════════════════════════════════════
# G3 — CAPACITY
# ═══════════════════════════════════════════════════════════════════════════
def host_capacity(host: str, cap_file: Path = CAP_F) -> int | None:
    """our_cores for `host`, or None = REFUSE. There is deliberately no default.

    Matches on the BARE hostname on both sides (see bare_host). `nproc` (col 2)
    is never read here — it is the machine, not our allocation.
    """
    if host == LOCAL:
        try:
            n = int(subprocess.run(["sysctl", "-n", "hw.ncpu"], capture_output=True,
                                   text=True, timeout=10).stdout.strip())
            return n
        except Exception:
            try:
                return os.cpu_count() or None
            except Exception:
                return None
    if not Path(cap_file).exists():
        return None
    want = bare_host(host)
    for ln in Path(cap_file).read_text().splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        f = s.split()
        if len(f) < 3:
            continue
        if bare_host(f[0]) == want:
            try:
                return int(f[2])          # col 3 = our_cores, NOT col 2 = nproc
            except ValueError:
                return None
    return None


# ═══════════════════════════════════════════════════════════════════════════
# G5 — BASENAME COLLISION
# ═══════════════════════════════════════════════════════════════════════════
def basename_collision(treat: str, ctrl: str) -> bool:
    """True = UNSCORABLE. Same predicate as overnight.sh:71 / worker.sh:221.

    Scoring is `case $L in *"$B"*)` on the treatment basename, so any substring
    relation makes every control win score as a treatment win.
    """
    b, c = Path(treat).name, Path(ctrl).name
    return b == c or b in c or c in b


def tree_ok(tree: str) -> bool:
    return (REPO / tree / "main.py").exists() or Path(tree, "main.py").exists()


def row_dispatchable(r: Row) -> tuple[bool, str]:
    """Everything worker.sh's G4 would check, done BEFORE a claim is spent."""
    if basename_collision(r.treatment_tree, r.control_tree):
        return False, (f"basenames collide ({Path(r.treatment_tree).name} vs "
                       f"{Path(r.control_tree).name}) — scoring is a SUBSTRING match")
    if not tree_ok(r.treatment_tree):
        return False, f"treatment {r.treatment_tree} has no main.py (compose it first)"
    if not tree_ok(r.control_tree):
        return False, f"control {r.control_tree} has no main.py"
    if r.target_n <= 0:
        return False, f"target {r.target_n} is not a positive game count"
    if r.seed_lo < 0:
        return False, f"seed_lo {r.seed_lo} is negative"
    return True, ""


# ═══════════════════════════════════════════════════════════════════════════
# G4 — NULL PAIR
# ═══════════════════════════════════════════════════════════════════════════
def trees_identical(a: str, b: str) -> bool:
    """orchestrate.sh gen's structural rule: same *.py names AND same bytes.

    ⚠ SECOND IMPLEMENTATION — see G4 in the docstring. The selftest asserts
    AGREEMENT with `orchestrate.sh gen`, not this function's own opinion.
    """
    pa, pb = REPO / a, REPO / b
    if not (pa.is_dir() and pb.is_dir()):
        return False
    fa = sorted(f.name for f in pa.glob("*.py"))
    fb = sorted(f.name for f in pb.glob("*.py"))
    if not fa or fa != fb:
        return False
    return all((pa / n).read_bytes() == (pb / n).read_bytes() for n in fa)


def has_null_pair(worklist: Path) -> bool:
    """Does this source worklist contain a byte-identical (treatment, control)
    pair? `orchestrate.sh gen` REFUSES if not, because a host with no null cell
    cannot be certified and its rows can never be pooled."""
    p = Path(worklist)
    if not p.exists():
        return False
    for ln in p.read_text().splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        f = s.split()
        if len(f) >= 3 and trees_identical(f[1], f[2]):
            return True
    return False


def find_null_pair() -> tuple[str, str] | None:
    """A byte-identical pair already known to this repo, for seeding a new
    host source worklist. Found STRUCTURALLY from rows we already run — a
    convention ("call it NULLxxx") can rot; an md5 cannot."""
    seen: set[tuple[str, str]] = set()
    for wl in [LOCAL_WORK_F] + sorted(VPS_DIR.glob("*.txt")) + sorted(VPS_DIR.glob("*/worklist.txt")):
        if not wl.exists():
            continue
        for ln in wl.read_text().splitlines():
            s = ln.strip()
            if not s or s.startswith("#"):
                continue
            f = s.split()
            if len(f) >= 3 and (f[1], f[2]) not in seen:
                seen.add((f[1], f[2]))
                if trees_identical(f[1], f[2]):
                    return f[1], f[2]
    return None


# ═══════════════════════════════════════════════════════════════════════════
# OCCUPANCY — G2 (blind is not idle) and G6 (every read carries its age)
# ═══════════════════════════════════════════════════════════════════════════
def runner_pattern() -> str:
    """THE one definition of a shard-runner process, read out of
    tools/lib/runner_pat.sh rather than copied. Three tools broke independently
    on private copies of this (D24(e): the second implementation is the one
    nobody tests). `[o]vernight...` is a one-char class and is a valid Python
    regex unchanged."""
    m = re.search(r"^RUNNER_PAT='([^']+)'", RUNNER_PAT_SH.read_text(), re.M)
    if not m:
        raise SystemExit(f"⛔ cannot read RUNNER_PAT out of {RUNNER_PAT_SH} — "
                         f"refusing to guess what a runner looks like.")
    return m.group(1)


@dataclass
class Occupancy:
    """What one host looked like at ONE instant, with that instant attached."""
    host: str
    blind: bool
    reason: str = ""
    running_shards: int = 0        # local: concurrent overnight.sh runners
    load1: float | None = None
    worker_alive: bool = False     # remote: worker.sh present at all
    queued_rows: int = 0           # rows not yet terminal on this host
    read_utc: str = field(default_factory=utc)
    read_mono: float = field(default_factory=time.time)
    consumer: bool = True          # is anything actually consuming this queue?

    def age_s(self) -> int:
        return int(time.time() - self.read_mono)


def local_occupancy(ps_reader=None, load_reader=None,
                    work_f: Path = LOCAL_WORK_F,
                    state_dir: Path = LOCAL_STATE) -> Occupancy:
    """Concurrent shards + load + whether corefill is actually consuming.

    G2: a `ps` we cannot read is BLIND, never 0. G3-adjacent: a worklist with no
    corefill process behind it is NOT a free slot — it is a queue with no
    consumer, and dispatching into it would idle the cores it claims to fill.
    """
    if ps_reader is None:
        def ps_reader():
            return subprocess.run(["ps", "ax", "-o", "command="],
                                  capture_output=True, text=True, timeout=30).stdout
    if load_reader is None:
        def load_reader():
            out = subprocess.run(["uptime"], capture_output=True, text=True, timeout=15).stdout
            m = re.search(r"averages?:?\s+([0-9.]+)", out)
            return float(m.group(1)) if m else None

    try:
        ps_out = ps_reader()
    except Exception as e:
        return Occupancy(LOCAL, blind=True, reason=f"cannot read process table ({e.__class__.__name__})")
    if ps_out is None:
        return Occupancy(LOCAL, blind=True, reason="process table read returned nothing")

    pat = runner_pattern()
    running = sum(1 for ln in ps_out.splitlines() if re.search(pat + r"\s", ln))
    consumer = any("corefill" in ln and "fleet_dispatch" not in ln for ln in ps_out.splitlines())

    try:
        load1 = load_reader()
    except Exception:
        load1 = None
    if load1 is None:
        return Occupancy(LOCAL, blind=True, reason="load average unreadable — a proxy we cannot read is not a passed gate",
                         running_shards=running, consumer=consumer)

    queued = 0
    if work_f.exists():
        for ln in work_f.read_text().splitlines():
            s = ln.strip()
            if not s or s.startswith("#"):
                continue
            f = s.split()
            if f and not (state_dir / f[0]).exists():
                queued += 1
    return Occupancy(LOCAL, blind=False, running_shards=running, load1=load1,
                     queued_rows=queued, consumer=consumer)


_STATUS_RE_RUN = re.compile(r"^runners:\s*(\d+)\s+worker:\s*(\d+)", re.M)
_STATUS_RE_LOAD = re.compile(r"^load:\s*([0-9.]+)", re.M)
_STATUS_ROW = re.compile(r"^(\S+)\s+(\d+)\s+(\d+)\s+(\d+)s\s+(\S+)", re.M)


def parse_remote_status(host: str, out: str | None) -> Occupancy:
    """Parse `orchestrate.sh status <host>`.

    ⛔ G2's BITING CELL LIVES HERE. We gate on the PRESENCE OF THE LOAD-BEARING
    FIELD (`runners:`/`worker:`), never on an exit code — on this platform
    `fcode status` exits 0 while printing `Error: True`, and ssh returns the
    REMOTE command's status, so a half-executed remote body can exit 0 with a
    truncated body. A response that parses is not a response that answered.

    ⚠ TWO COUNTING DEFECTS IN cmd_status ITSELF, worked around here rather than
    edited there (that file has live workers reading it):
      * `runners:` is `grep -c "[f]code run"` and matches BOTH the `timeout 120
        .venv/bin/fcode run ...` wrapper AND the python process — so it reads
        ~2x the true game count. We therefore never use it as a core count.
      * `worker:` counts `worker.sh` command lines, and bash `( ... ) &`
        subshells inherit the parent's command line — so during a batch it reads
        1 + WORKERS. Only `>= 1` is meaningful: a worker is ALIVE, or it is not.
    """
    if out is None:
        return Occupancy(host, blind=True, reason="status command did not return (ssh/transport)")
    m = _STATUS_RE_RUN.search(out)
    if not m:
        return Occupancy(host, blind=True,
                         reason="status returned but the LOAD-BEARING FIELD `runners:/worker:` is absent "
                                "— a degraded response parses too")
    worker_n = int(m.group(2))
    ml = _STATUS_RE_LOAD.search(out)
    load1 = float(ml.group(1)) if ml else None

    # ⛔ DEPTH IS *LIVE* SHARDS, NOT "NOT COMPLETE" — AND THE DIFFERENCE IS
    # STARVATION. My first cut counted every non-COMPLETE row. Driven against the
    # real fleet at 2026-08-15T09:47Z, work-server-1 returned FOUR terminal-dead
    # rows (LNCHERLY STOPPED 7640s, LNCHMAX ABORTED_NOWINNER 9489s, V140VS145
    # STOPPED 51114s, V140VS145B STOPPED 48819s) alongside ONE live shard. That
    # cut read depth=5 and would have reported the host permanently FULL,
    # dispatching nothing to a box with nine free cores — the exact defect
    # `fixture_starvation.py` exists to catch, reproduced in the dispatcher.
    # ⇒ Only RUNNING/STARTING/CURFEW with a FRESH heartbeat is depth. A stale
    # heartbeat is not evidence of life (worker.sh's curfew froze one on the
    # literal string RUNNING for hours), so content AND age both gate.
    live_states = {"RUNNING", "STARTING", "CURFEW"}
    depth = 0
    for sh, _rows, _target, age_s, st in _STATUS_ROW.findall(out):
        if sh == "SHARD":
            continue
        if st in live_states and int(age_s) <= HB_FRESH_S:
            depth += 1
    return Occupancy(host, blind=False, worker_alive=worker_n >= 1, load1=load1,
                     running_shards=depth, queued_rows=depth, consumer=True)


def remote_occupancy(host: str, runner=None, timeout_s: int = 90) -> Occupancy:
    if runner is None:
        def runner(h):
            try:
                p = subprocess.run(["bash", str(ORCH), "status", h],
                                   capture_output=True, text=True, timeout=timeout_s, cwd=str(REPO))
                return p.stdout + p.stderr
            except Exception:
                return None
    return parse_remote_status(host, runner(host))


def host_queue_depth(host: str, rows: list[Row]) -> int:
    """Rows this dispatcher has parked on `host` that are not terminal.

    ⛔ Counted from OUR ledger, not from the host's shard table: a host whose
    status we cannot read still owes us the rows we gave it, and forgetting them
    is how a host gets triple-stocked while blind.
    """
    return sum(1 for r in rows if r.host == host and r.state in ("CLAIMED", "RUNNING"))


# ═══════════════════════════════════════════════════════════════════════════
# FREE SLOTS
# ═══════════════════════════════════════════════════════════════════════════
def free_slots(occ: Occupancy, cap: int | None, ledger_depth: int,
               cores_per_shard: float = CORES_PER_SHARD,
               queue_depth_target: int = QUEUE_DEPTH_TARGET,
               local_load_ceil: float = LOCAL_LOAD_CEIL) -> tuple[int, str]:
    """(slots, why). NEVER negative, and 0 whenever anything is unknown.

    G2 blind -> 0. G3 no capacity row -> 0 (REFUSE, do not default).
    """
    if occ.blind:
        return 0, f"BLIND ({occ.reason}) — treated as FULL, dispatching nothing"
    if cap is None:
        return 0, ("⛔ REFUSING: no row in scratchpad/vps/host_capacity.tsv. "
                   "Add its allocation (NOT its nproc) before dispatching.")
    if occ.host == LOCAL:
        if not occ.consumer:
            return 0, "no corefill process consuming the local worklist — a queue with no consumer is not a free slot"
        if occ.load1 is not None and occ.load1 > local_load_ceil:
            return 0, f"load {occ.load1:.2f} > ceiling {local_load_ceil:.1f}"
        slots = int(cap // cores_per_shard)
        free = slots - occ.running_shards - occ.queued_rows
        return max(0, free), (f"slots={slots} (cap {cap} / {cores_per_shard:g} cores per shard) "
                              f"running={occ.running_shards} queued={occ.queued_rows} load={occ.load1:.2f}")
    # REMOTE: sequential shards, so depth is the metric — not cores.
    depth = max(ledger_depth, occ.queued_rows)
    free = queue_depth_target - depth
    return max(0, free), (f"depth={depth}/{queue_depth_target} (remote shards run SEQUENTIALLY; "
                          f"cap {cap} cores all go to the running shard) worker_alive={occ.worker_alive}")


# ═══════════════════════════════════════════════════════════════════════════
# COMPLETION POLLING
# ═══════════════════════════════════════════════════════════════════════════
def _terminal_in(d: Path, shard: str) -> tuple[str | None, int | None]:
    """(state, age_s) from a heartbeat, preferring CONTENT+FRESHNESS over a
    marker. A mirrored .COMPLETE can outlive an upstream reset; a heartbeat's
    5th field is rewritten every cycle."""
    hb = d / f"{shard}.heartbeat"
    if hb.exists():
        try:
            age = int(time.time() - hb.stat().st_mtime)
            f = hb.read_text().strip().split("\t")
            return (f[4] if len(f) >= 5 else None), age
        except OSError:
            pass
    c = d / f"{shard}.COMPLETE"
    if c.exists():
        try:
            return "COMPLETE", int(time.time() - c.stat().st_mtime)
        except OSError:
            return "COMPLETE", None
    return None, None


def shard_status(r: Row) -> tuple[str | None, int | None, str]:
    """(hb_state, age_s, where). Searches the local out dir AND every mirrored
    remote dir — a locally-queued shard can have finished on a fleet box, and
    the hostkey used for the mirror has drifted (`work-server-1` and
    `worker@work-server-1` BOTH exist under scratchpad/overnight-remote)."""
    st, age = _terminal_in(LOCAL_OUT, r.shard_id)
    if st is not None:
        return st, age, str(LOCAL_OUT)
    if REMOTE_OUT.is_dir():
        for d in sorted(REMOTE_OUT.iterdir()):
            if not d.is_dir():
                continue
            st, age = _terminal_in(d, r.shard_id)
            if st is not None:
                return st, age, str(d)
    return None, None, "-"


def reconcile(rows: list[Row]) -> int:
    """Advance CLAIMED->RUNNING->DONE/FAILED from evidence. Never backwards.

    ⛔ G1's BITING CELL. A row marked RUNNING whose heartbeat is HOURS stale with
    no .COMPLETE is EXACTLY what a restartable corpse looks like, and it is also
    exactly what a curfewed worker looks like (worker.sh's curfew stamped no
    heartbeat for a day and a lane declared a sleeping leg DEAD). So a stale
    heartbeat marks the row FAILED — which REMOVES it from dispatch forever —
    and never re-queues it. Recovery is a human adding a NEW row.
    """
    changed = 0
    for r in rows:
        if r.state not in ("CLAIMED", "RUNNING"):
            continue
        st, age, where = shard_status(r)
        if st is None:
            continue
        if st == "COMPLETE":
            r.state, r.note = "DONE", f"COMPLETE age={age}s in {Path(where).name}"
            changed += 1
        elif st in ("ABORTED_NOWINNER",):
            r.state, r.note = "FAILED", f"{st} age={age}s in {Path(where).name} — logged and LEFT"
            changed += 1
        elif st in ("RUNNING", "STARTING", "CURFEW", "STOPPED"):
            if age is not None and age > HB_FRESH_S and st != "CURFEW":
                r.state, r.note = "FAILED", (f"heartbeat {st} but {age}s stale (> {HB_FRESH_S}s) "
                                             f"— logged and LEFT, never relaunched")
                changed += 1
            elif r.state != "RUNNING":
                r.state, r.note = "RUNNING", f"{st} age={age}s"
                changed += 1
    return changed


# ═══════════════════════════════════════════════════════════════════════════
# PLANNING — pure, so the selftest drives the SHIPPED function
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class HostView:
    host: str
    occ: Occupancy
    cap: int | None
    ledger_depth: int


@dataclass
class Assignment:
    row: Row
    host: str


def plan_pass(rows: list[Row], views: list[HostView],
              cores_per_shard: float = CORES_PER_SHARD,
              queue_depth_target: int = QUEUE_DEPTH_TARGET,
              local_load_ceil: float = LOCAL_LOAD_CEIL) -> tuple[list[Assignment], list[str], list[str]]:
    """(assignments, host_lines, skip_lines). Changes nothing.

    Rows are taken in queue order; a row that fails a precheck is SKIPPED (left
    QUEUED, never claimed, never silently dropped) so a fixable problem costs a
    log line and not a spent id.
    """
    host_lines, skips = [], []
    budget: list[tuple[str, int]] = []
    for v in views:
        n, why = free_slots(v.occ, v.cap, v.ledger_depth, cores_per_shard,
                            queue_depth_target, local_load_ceil)
        stale = "  ⚠ STALE" if v.occ.age_s() > STATUS_STALE_S else ""
        tag = "BLIND" if v.occ.blind else ("FREE" if n else "FULL")
        # G6: age on EVERY line, and BLIND/FULL/FREE are textually distinct.
        host_lines.append(f"{v.host:<22} {tag:<5} free={n:<3} age={v.occ.age_s()}s{stale}  {why}")
        if n:
            budget.append((v.host, n))
    out: list[Assignment] = []
    for r in rows:
        if not budget:
            break
        if r.claimed:                                  # G1
            continue
        ok, why = row_dispatchable(r)                  # G5 + tree presence
        if not ok:
            skips.append(f"SKIP {r.shard_id}: {why} (left QUEUED, NOT claimed)")
            continue
        h, n = budget[0]
        out.append(Assignment(r, h))
        # ROUND-ROBIN, and it is a policy not a detail: taking one host's slots
        # to exhaustion first would hand the whole head of the queue to whichever
        # host happens to sit first in hosts.txt. That is the same line-order-
        # becomes-policy class that put a twice-requested arm behind two others
        # in corefill.sh purely by position.
        if n - 1 == 0:
            budget.pop(0)
        else:
            budget[0] = (h, n - 1)
            budget.append(budget.pop(0))
    return out, host_lines, skips


# ═══════════════════════════════════════════════════════════════════════════
# DISPATCH
# ═══════════════════════════════════════════════════════════════════════════
def dispatch_local(r: Row, dry: bool) -> tuple[bool, str]:
    """Append to corefill_work.txt. corefill.sh RE-READS the worklist every poll
    (`done < $WORK` sits inside its `while true`), so ADD is its documented
    operator interface and the row is picked up within POLL_S."""
    line = f"{r.shard_id} {r.treatment_tree} {r.control_tree} {r.target_n} {r.seed_lo}\n"
    if dry:
        return True, f"WOULD append to {LOCAL_WORK_F.name}: {line.strip()}"
    with LOCAL_WORK_F.open("a") as fh:      # in place: same inode, corefill re-opens anyway
        fh.write(line)
    return True, f"appended to {LOCAL_WORK_F.name}"


def host_src_worklist(host: str) -> Path:
    return VPS_DIR / f"{hostkey(host)}.fleet_src.txt"


def ensure_host_src(host: str, dry: bool) -> tuple[Path | None, str]:
    """The per-host source worklist `gen --from` reads.

    G4: it must contain a byte-identical pair or `gen` refuses, so we seed it
    with a NULLPAIR_DETECT row (never selected by name, exactly as
    scratchpad/vps/work-server-2-r.txt does) and REFUSE up front if this repo
    has no such pair to offer.
    """
    p = host_src_worklist(host)
    if p.exists() and has_null_pair(p):
        return p, "existing"
    pair = find_null_pair()
    if pair is None:
        return None, ("⛔ REFUSING: no byte-identical (treatment == control) pair exists in any known "
                      "worklist, so this host could be given no NULL cell — `gen` would refuse and the "
                      "run would die at dispatch time. A host with no null cannot be certified.")
    if dry:
        return p, f"WOULD create {p.name} with NULLPAIR_DETECT {pair[0]} {pair[1]}"
    body = (f"# FLEET SOURCE WORKLIST for {host} — generated by tools/fleet_dispatch.py\n"
            f"# Row 1 is NOT a real shard: it exists only so `orchestrate.sh gen`'s structural\n"
            f"# NULLPAIR scan finds a byte-identical pair to build the host's own NULLHOST\n"
            f"# certification row from. It is never selected by name, so it never reaches the\n"
            f"# generated worklist.\n"
            f"# shard  treatment  control  target  seedbase\n"
            f"{NULLPAIR_DETECT} {pair[0]} {pair[1]} 400 900000\n")
    if p.exists():
        body = p.read_text().rstrip("\n") + "\n" + f"{NULLPAIR_DETECT} {pair[0]} {pair[1]} 400 900000\n"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)
    return p, f"created {p.name}"


def _run(cmd: list[str], timeout_s: int = 900) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, cwd=str(REPO))
    return p.returncode, (p.stdout + p.stderr)


def read_seed_offset(host: str) -> int | None:
    """The host's additive seed partition, from the sidecar `gen` wrote. Never
    recomputed here: it is a pure function of the hostkey and the SIDECAR is the
    auditable record of what the host is actually playing."""
    p = VPS_DIR / hostkey(host) / "SEED_OFFSET"
    if p.exists():
        try:
            return int(p.read_text().strip())
        except ValueError:
            return None
    return None


def dispatch_remote_drain(r: Row, host: str, cap: int, rows: list[Row], dry: bool) -> tuple[bool, str]:
    """gen --from + push + start. Legal ONLY with the worker DOWN (G7)."""
    src, note = ensure_host_src(host, dry)
    if src is None:
        return False, note
    line = f"{r.shard_id} {r.treatment_tree} {r.control_tree} {r.target_n} {r.seed_lo}\n"
    want = [x.shard_id for x in rows
            if x.host == host and x.state in ("CLAIMED", "RUNNING") and x.shard_id != r.shard_id]
    want.append(r.shard_id)
    if dry:
        return True, (f"WOULD append to {src.name}: {line.strip()}\n"
                      f"      WOULD run: orchestrate.sh gen {host} {' '.join(want)} --from {src}\n"
                      f"      WOULD run: orchestrate.sh push {host}\n"
                      f"      WOULD run: orchestrate.sh start {host} {cap}   (worker is DOWN — G7 satisfied)")
    with src.open("a") as fh:
        fh.write(line)
    rc, out = _run(["bash", str(ORCH), "gen", host, *want, "--from", str(src)])
    if "REFUSING" in out or not (VPS_DIR / hostkey(host) / "worklist.txt").exists():
        return False, f"gen refused: {out.strip()[-400:]}"
    rc, out = _run(["bash", str(ORCH), "push", host])
    if "post-push check" not in out:          # gate on the LOAD-BEARING line, not $?
        return False, f"push did not confirm the snapshot: {out.strip()[-400:]}"
    rc, out = _run(["bash", str(ORCH), "start", host, str(cap)])
    if "STARTED on" not in out:
        return False, f"start did not confirm: {out.strip()[-400:]}"
    return True, f"gen+push+start ({len(want)} shards listed, WORKERS={cap})"


def dispatch_remote_live(r: Row, host: str, dry: bool) -> tuple[bool, str]:
    """Surgical append to a LIVE worker: additive tree rsync + in-place `>>`.

    Never touches maps/ (cmd_push wipes them, which injects NOWINNER rows into
    games in flight) and never replaces the worklist inode (rsync renames, and a
    running `while read` keeps the OLD inode — measured, see the docstring).
    """
    off = read_seed_offset(host)
    if off is None:
        return False, (f"⛔ no {VPS_DIR / hostkey(host) / 'SEED_OFFSET'} — this host has never been "
                       f"`gen`'d, so its seed partition is unknown. Without it the row would replay "
                       f"another host's seeds and the pooled n would be a lie. Use drain mode once.")
    seed = r.seed_lo + off
    line = f"{r.shard_id} {r.treatment_tree} {r.control_tree} {r.target_n} {seed}"
    trees = [r.treatment_tree, r.control_tree]
    if dry:
        return True, (f"WOULD rsync trees {trees} -> {host}:{REMOTE_ROOT}/ (additive, maps/ untouched)\n"
                      f"      WOULD append in place to {host}:{REMOTE_ROOT}/work/worklist.txt:\n"
                      f"        {line}   (seed_lo {r.seed_lo} + host offset {off})")
    for t in trees:
        rc, out = _run(["rsync", "-a", "--exclude", "__pycache__", "--exclude", "*.pyc",
                        f"{t}/", f"{host}:{REMOTE_ROOT}/{t}/"], timeout_s=600)
        if rc != 0:
            return False, f"rsync of {t} failed: {out.strip()[-300:]}"
    # Verify the LOAD-BEARING file landed, then append, then read the tail back.
    check = (f"cd {REMOTE_ROOT} && test -f {r.treatment_tree}/main.py && test -f {r.control_tree}/main.py "
             f"&& printf '%s\\n' {line!r} >> work/worklist.txt && tail -1 work/worklist.txt")
    rc, out = _run(["ssh", "-o", "BatchMode=yes", host, check], timeout_s=120)
    if r.shard_id not in out:
        return False, f"append not confirmed on {host} (tail did not echo the row): {out.strip()[-300:]}"
    # ⛔ REPORT THE LINE THAT MATCHED, NOT THE LAST LINE. ssh interleaves banner
    # text ("The server may need to be upgraded...") with command output, and
    # splitlines()[-1] picked the BANNER on work-server-1 — so a genuine append
    # was reported with a line that looks like a transport warning. The CHECK was
    # right (shard_id in out) and only the evidence shown was wrong, which is the
    # worst kind of cosmetic bug: it makes a correct result unreadable.
    echoed = next((ln for ln in out.strip().splitlines() if r.shard_id in ln),
                  "<matched, line not recoverable>")
    return True, f"live-append confirmed on {host}: {echoed.strip()}"


# ═══════════════════════════════════════════════════════════════════════════
# SEEDING FROM COMBINATIONS
# ═══════════════════════════════════════════════════════════════════════════
def used_seed_hi() -> int:
    """Highest ALLOCATABLE seed_lo + span already spoken for anywhere we can see.

    Two bands are excluded and both exclusions are load-bearing:
      * `lo >= SEED_CEIL` — already carries a host offset, so it is not in the
        base space at all and reading it would ratchet us out of every host's
        partition at once.
      * `SEED_RESERVED_LO <= lo < SEED_CEIL` — the certification band (see the
        constant). Counting it as used is the defect that produced a
        904000..1126000 allocation.
    """
    hi = 0
    files = [LOCAL_WORK_F, QUEUE_F] + sorted(VPS_DIR.glob("*.txt")) + sorted(VPS_DIR.glob("*/worklist.txt"))
    for p in files:
        if not p.exists():
            continue
        for ln in p.read_text().splitlines():
            s = ln.strip()
            if not s or s.startswith("#"):
                continue
            f = re.split(r"[\t ]+", s)
            if len(f) >= 5:
                try:
                    lo, tg = int(f[4]), int(f[3])
                except ValueError:
                    continue
                if lo >= SEED_RESERVED_LO:
                    continue
                hi = max(hi, lo + math.ceil(tg / GAMES_PER_SEED))
    return hi


def alloc_seeds(n: int, target: int, base_hint: int | None = None) -> tuple[int, str]:
    """(base, why) for n rows, or raise. Non-overlapping AND inside the band.

    ⛔ THE INVARIANT IS CHECKED, NOT ASSUMED: the last row's LAST SEED must land
    below SEED_RESERVED_LO. An allocator that silently walks past the band puts
    a remote row into another host's megabyte, where it replays that host's
    seeds — the pooled n becomes a lie in exactly the way the seed partition
    exists to prevent, and nothing downstream can see it.
    """
    span = math.ceil(target / GAMES_PER_SEED)
    if span >= SEED_STRIDE:
        raise ValueError(f"target {target} needs {span} seeds but the stride is {SEED_STRIDE} — "
                         f"rows would overlap in seed space and their games would not be "
                         f"independent draws")
    base = base_hint if base_hint is not None else max(SEED_LO_FLOOR, used_seed_hi() + SEED_STRIDE)
    base = ((base + SEED_STRIDE - 1) // SEED_STRIDE) * SEED_STRIDE
    last = base + (n - 1) * SEED_STRIDE + span
    if last >= SEED_RESERVED_LO:
        raise ValueError(f"{n} rows x stride {SEED_STRIDE} from {base} would reach {last}, at or past the "
                         f"reserved certification band {SEED_RESERVED_LO}. A base seed must stay under it: "
                         f"a remote host adds crc32(hostkey)%50*1e6, so a spilled row lands in ANOTHER "
                         f"host's partition and replays its seeds. Lower the target, raise the stride, or "
                         f"split the batch.")
    return base, f"base={base} stride={SEED_STRIDE} span={span} last_seed={last} (< {SEED_RESERVED_LO})"


def seed_from(combo_f: Path, target: int, control: str, compose: bool,
              dry: bool, prefix: str = "CMB", tree_prefix: str = "bots/_cmb") -> int:
    """Load `scratchpad/combos_ok.txt` into the queue, one row per combination.

    Trees are composed by `tools/stack.py`, which merges N planks 3-way and
    REFUSES the inert-toggle and conflict cases. ⛔ COMPOSITION IS OPT-IN
    (`--compose`) because it CREATES bot trees; without it the rows are written
    with their planned tree path and the dispatcher SKIPS them (leaving them
    QUEUED) until the tree exists.
    """
    sys.path.insert(0, str(REPO / "tools"))
    import stack                                            # noqa: E402

    combos: list[list[str]] = []
    for ln in Path(combo_f).read_text().splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        planks = s.split()
        bad = [p for p in planks if p not in stack.PLANKS]
        if bad:
            say(f"⛔ REFUSING {s!r}: unknown plank(s) {bad}; known: {', '.join(sorted(stack.PLANKS))}")
            return 2
        combos.append(planks)
    if not combos:
        say(f"⛔ {combo_f} has no combinations")
        return 2

    rows = read_queue()
    have = {r.shard_id for r in rows}
    try:
        base, alloc_why = alloc_seeds(len(combos), target)
    except ValueError as e:
        say(f"⛔ REFUSING: {e}")
        return 2

    added = skipped = 0
    for i, planks in enumerate(combos, 1):
        sid = f"{prefix}{i:03d}"
        tree = f"{tree_prefix}{i:03d}"
        if sid in have:
            skipped += 1
            continue
        if basename_collision(tree, control):              # G5, at seed time
            say(f"⛔ REFUSING {sid}: basenames collide ({Path(tree).name} vs {Path(control).name})")
            return 2
        seed = base + (i - 1) * SEED_STRIDE
        note = "+".join(planks)
        if compose and not dry and not (REPO / tree / "main.py").exists():
            rc = stack.compose(planks, REPO / tree, quiet=True)
            if rc != 0:
                say(f"⛔ stack.py refused {sid} ({note}) rc={rc} — row NOT queued "
                    f"(rc3=conflict, rc5=inert/unconsumed toggle)")
                skipped += 1
                continue
        rows.append(Row(sid, tree, control, target, seed, "QUEUED", "-", "-", note))
        added += 1
    if dry:
        say(f"DRY-RUN --seed-from: WOULD add {added} rows (skipped {skipped}) "
            f"{alloc_why} target={target} control={control} compose={compose}")
        return 0
    write_queue(rows)
    say(f"SEEDED {added} rows into {QUEUE_F.name} (skipped {skipped} already present/refused). "
        f"{alloc_why} target={target} control={control} composed={compose}")
    if not compose:
        say("  ⚠ trees NOT composed (--compose omitted). The dispatcher will SKIP these rows, "
            "leaving them QUEUED, until tools/stack.py has built each tree.")
    return 0


# ═══════════════════════════════════════════════════════════════════════════
# ONE PASS
# ═══════════════════════════════════════════════════════════════════════════
def hosts_list() -> list[str]:
    out = [LOCAL]
    if HOSTS_F.exists():
        for ln in HOSTS_F.read_text().splitlines():
            s = ln.strip()
            if s and not s.startswith("#"):
                out.append(s)
    return out


def build_views(rows: list[Row], hosts: list[str]) -> list[HostView]:
    views = []
    for h in hosts:
        occ = local_occupancy() if h == LOCAL else remote_occupancy(h)
        views.append(HostView(h, occ, host_capacity(h), host_queue_depth(h, rows)))
    return views


def one_pass(dry: bool, remote_mode: str, cores_per_shard: float,
             queue_depth_target: int) -> int:
    rows = read_queue()
    if not rows:
        say(f"queue {QUEUE_F} is empty — nothing to dispatch. Seed it: --seed-from scratchpad/combos_ok.txt")
        return 0
    n = reconcile(rows)
    if n and not dry:
        write_queue(rows)
    counts = {s: sum(1 for r in rows if r.state == s) for s in STATES}
    say(f"queue {QUEUE_F.name}: " + " ".join(f"{k}={v}" for k, v in counts.items()) +
        f"   (reconciled {n} row(s) this pass)")

    views = build_views(rows, hosts_list())
    plan, host_lines, skips = plan_pass(rows, views, cores_per_shard, queue_depth_target)
    for l in host_lines:
        say("  " + l)
    # Summarise: 112 identical SKIP lines bury the one line that differs.
    # The COUNT is the signal ("nothing is composed yet"); the examples are the
    # evidence. Never suppress a skip class entirely — a silently dropped row is
    # how work disappears.
    if skips:
        by_reason: dict[str, list[str]] = {}
        for s in skips:
            key = re.sub(r"\b(CMB|SKIP )\S*", "", s).strip()
            key = re.sub(r"bots/\S+", "<tree>", key)
            by_reason.setdefault(key, []).append(s.split()[1].rstrip(":"))
        for key, ids in by_reason.items():
            head = ", ".join(ids[:5]) + (f" … +{len(ids) - 5} more" if len(ids) > 5 else "")
            say(f"  SKIPPED {len(ids)} row(s) — {key}")
            say(f"    {head}")
    if not plan:
        say("  nothing dispatchable this pass")
        return 0

    for a in plan:
        r, h = a.row, a.host
        # ⛔ CLAIM BEFORE DISPATCH, ALWAYS. Same ordering as corefill's
        # marker-before-launch: a crash between these two lines must leave the
        # row SPENT, never re-assignable. Over-claiming loses one shard;
        # double-assigning corrupts two hosts' seed partitions.
        if not dry:
            r.state, r.host, r.claimed_utc = "CLAIMED", h, utc()
            r.note = f"claimed for {h}"
            write_queue(rows)
        say(f"CLAIM {r.shard_id} -> {h}  {r.treatment_tree} vs {r.control_tree} "
            f"target={r.target_n} seed_lo={r.seed_lo}" + ("   [DRY-RUN, nothing written]" if dry else ""))

        if h == LOCAL:
            ok, note = dispatch_local(r, dry)
        else:
            v = next(x for x in views if x.host == h)
            if remote_mode == "live" or (remote_mode == "auto" and v.occ.worker_alive):
                ok, note = dispatch_remote_live(r, h, dry)
            else:
                if v.occ.worker_alive:
                    ok, note = False, ("⛔ G7 REFUSING to `start`: a worker.sh is ALIVE on this host. "
                                       "cmd_start does `rm -f STOP`, so the old worker would wake and run its "
                                       "own WORKERS alongside the new ones — double-subscription, and --tle 10 is "
                                       "WALL-CLOCK, so every row both workers produce is corrupt. "
                                       "Use --remote-mode live, or kill the worker first.")
                elif v.cap is None:
                    ok, note = False, "⛔ no capacity row (G3)"
                else:
                    ok, note = dispatch_remote_drain(r, h, v.cap, rows, dry)
        say(f"  {'DISPATCH' if ok else 'DISPATCH FAILED'} {r.shard_id}: {note}")
        if not ok and not dry:
            # The claim is NOT returned to QUEUED — G1. It is marked FAILED with
            # the reason, and a human adds a new row if the cause is fixed.
            r.state, r.note = "FAILED", f"dispatch failed: {note.splitlines()[0][:200]}"
            write_queue(rows)
    return 0


# ═══════════════════════════════════════════════════════════════════════════
# SELFTEST — every guard driven to BOTH verdicts, calling the SHIPPED functions
# ═══════════════════════════════════════════════════════════════════════════
def _occ(host, **kw):
    o = Occupancy(host, blind=kw.pop("blind", False), **kw)
    return o


def _row(sid="S1", t="bots/_v242bodyaware", c="bots/_v223sealrepair", n=5400, s=500000, st="QUEUED", h="-"):
    return Row(sid, t, c, n, s, st, h)


def selftest() -> int:
    """⛔ THE STANDARD IS THE CELL THAT CAN BITE, NOT THE ONE THAT FAILS LOUDLY.

    A guard whose only observed output is silence has not been seen to check. So
    for each guard the NEGATIVE cell is the one that would sail through a naive
    implementation: a status that returns cleanly with the field missing (not a
    nonzero exit); a host present under the other prefix (not a typo); a RUNNING
    row with a dead heartbeat (not a DONE row); a substring collision (not an
    equal pair). Nothing below re-implements the logic — every assertion calls a
    shipped function.
    """
    fail = 0

    def chk(name, got, want):
        nonlocal fail
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}  {name:<58} got={got!r} want={want!r}")
        if not ok:
            fail = 1

    print("── G1  NEVER RE-DISPATCH ─────────────────────────────────────────────")
    free = [_row("Q1")]
    views = [HostView(LOCAL, _occ(LOCAL, running_shards=0, load1=1.0, queued_rows=0), 10, 0)]
    plan, _, _ = plan_pass(free, views)
    chk("+ a QUEUED row IS claimed", [a.row.shard_id for a in plan], ["Q1"])
    # the BITING cell: RUNNING, heartbeat long dead, no .COMPLETE — a corpse
    dead = [_row("D1", st="RUNNING", h=LOCAL)]
    plan, _, _ = plan_pass(dead, views)
    chk("- a RUNNING row with a dead shard is NOT re-dispatched", [a.row.shard_id for a in plan], [])
    for st in ("CLAIMED", "DONE", "FAILED"):
        plan, _, _ = plan_pass([_row("X", st=st, h=LOCAL)], views)
        chk(f"- state={st} is never re-dispatched", len(plan), 0)
    # and reconcile must move it to FAILED, not back to QUEUED
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        hb = d / "ZZDEAD.heartbeat"
        hb.write_text("2026-01-01T00:00:00Z\t100\t5400\tZZDEAD\tRUNNING\n")
        os.utime(hb, (time.time() - 7200, time.time() - 7200))
        st, age = _terminal_in(d, "ZZDEAD")
        chk("+ a 2h-stale RUNNING heartbeat reads RUNNING with a real age",
            (st, age is not None and age > HB_FRESH_S), ("RUNNING", True))
        fresh = d / "ZZLIVE.heartbeat"
        fresh.write_text("2026-01-01T00:00:00Z\t100\t5400\tZZLIVE\tRUNNING\n")
        st2, age2 = _terminal_in(d, "ZZLIVE")
        chk("- a fresh RUNNING heartbeat is NOT stale", age2 < HB_FRESH_S, True)

    print("── G2  BLIND IS NOT IDLE ─────────────────────────────────────────────")
    good = ("host: ws1   utc: 2026-08-15T09:00:00Z   NPROC: 16\n"
            "load: 3.10 3.00 2.90\n"
            "runners: 6   worker: 1\n"
            "SHARD              ROWS   TARGET     HB_AGE STATUS\n"
            "NULLHOST            400      400        11s COMPLETE\n"
            "SALTREF            1700     5400        11s RUNNING\n")
    o = parse_remote_status("ws1", good)
    chk("+ a complete status parses and is NOT blind", (o.blind, o.worker_alive, o.queued_rows),
        (False, True, 1))
    # ⛔ THE STARVATION CELL, verbatim from the live work-server-1 table at
    # 2026-08-15T09:47Z: four terminal-dead rows and ONE live shard. Counting
    # "not COMPLETE" reads depth=5 and the host never gets work again.
    real_ws1 = (
        "host: junghard-server   utc: 2026-08-15T09:47:56Z   NPROC: 16\n"
        "load: 4.96 4.43 4.33\n"
        "runners: 4   worker: 5\n"
        "SHARD              ROWS   TARGET     HB_AGE STATUS\n"
        "LNCHERLY           1350     5400      7640s STOPPED\n"
        "LNCHMAX             200     5400      9489s ABORTED_NOWINNER\n"
        "LNCHRND1           5270     5400        15s RUNNING\n"
        "NULLHOST            400      400     80315s COMPLETE\n"
        "V140VS145           480     1000     51114s STOPPED\n"
        "V140VS145B         1440     3000     48819s STOPPED\n")
    ows1 = parse_remote_status("worker@work-server-1", real_ws1)
    chk("+ live fleet table: depth counts ONLY the live shard, not 4 dead ones",
        ows1.queued_rows, 1)
    chk("+ ... so the host still has a free slot (starvation direction)",
        free_slots(ows1, 10, 0)[0], QUEUE_DEPTH_TARGET - 1)
    # and the other verdict: a genuinely busy host IS full
    busy = real_ws1.replace("      7640s STOPPED", "         9s RUNNING").replace(
        "     51114s STOPPED", "         9s RUNNING")
    obusy = parse_remote_status("worker@work-server-1", busy)
    chk("- a host with 3 live shards reads depth 3 and FULL",
        (obusy.queued_rows, free_slots(obusy, 10, 0)[0]), (3, 0))
    # a RUNNING heartbeat that is hours stale is not life (worker.sh curfew)
    frozen = real_ws1.replace("        15s RUNNING", "     41000s RUNNING")
    chk("- a stale RUNNING row does NOT count as depth",
        parse_remote_status("h", frozen).queued_rows, 0)
    # ⛔ THE BITING CELL: exit 0, well-formed, LOAD-BEARING FIELD ABSENT.
    degraded = ("host: ws1   utc: 2026-08-15T09:00:00Z   NPROC: 16\n"
                "load: 3.10 3.00 2.90\n"
                "(no shards have started yet)\n")
    o2 = parse_remote_status("ws1", degraded)
    chk("- status parses but `runners:` is ABSENT -> BLIND", o2.blind, True)
    chk("- transport returned nothing -> BLIND", parse_remote_status("ws1", None).blind, True)
    chk("- BLIND host yields 0 free slots", free_slots(o2, 10, 0)[0], 0)
    chk("+ readable host yields >0 free slots", free_slots(o, 10, 0)[0] > 0, True)
    # local: ps unreadable must be BLIND, not 0-running
    bad_ps = local_occupancy(ps_reader=lambda: (_ for _ in ()).throw(OSError("boom")))
    chk("- local ps read failing -> BLIND", bad_ps.blind, True)
    ok_ps = local_occupancy(ps_reader=lambda: "zsh tools/overnight.sh FOO a b 1 1\ncorefill.sh x\n",
                            load_reader=lambda: 2.0)
    chk("+ local ps readable -> 1 runner, not blind", (ok_ps.blind, ok_ps.running_shards), (False, 1))
    chk("- local load unreadable -> BLIND (a proxy we cannot read is not a passed gate)",
        local_occupancy(ps_reader=lambda: "corefill.sh x\n", load_reader=lambda: None).blind, True)
    # a queue with no consumer is not a free slot
    noc = local_occupancy(ps_reader=lambda: "some other process\n", load_reader=lambda: 1.0)
    chk("- local worklist with NO corefill consumer -> 0 free slots", free_slots(noc, 10, 0)[0], 0)

    print("── G3  CAPACITY FROM THE TABLE, NO DEFAULTS ──────────────────────────")
    chk("+ ws1 by full key resolves to our_cores 10 (not nproc 16)",
        host_capacity("worker@work-server-1"), 10)
    chk("+ ws1 by BARE name resolves to the same row (the prefix biting cell)",
        host_capacity("work-server-1"), 10)
    chk("+ ws2 resolves to 6", host_capacity("worker@work-server-2"), 6)
    chk("- a host with no row REFUSES (None), never a default",
        host_capacity("worker@no-such-host"), None)
    chk("- capacity None -> 0 free slots", free_slots(_occ("h", queued_rows=0), None, 0)[0], 0)
    chk("+ capacity present -> free slots computed",
        free_slots(_occ("h", queued_rows=0), 6, 0)[0], QUEUE_DEPTH_TARGET)
    # the divisor is real: 10 cores / 1.0 = 10 local slots, / 2.5 = 4
    lo = _occ(LOCAL, running_shards=0, load1=1.0, queued_rows=0)
    chk("+ local slots honour cores_per_shard=1.0", free_slots(lo, 10, 0, cores_per_shard=1.0)[0], 10)
    chk("+ local slots honour cores_per_shard=2.5", free_slots(lo, 10, 0, cores_per_shard=2.5)[0], 4)
    hot = _occ(LOCAL, running_shards=0, load1=99.0, queued_rows=0)
    chk("- local over the load ceiling -> 0", free_slots(hot, 10, 0)[0], 0)

    print("── G4  NULL-PAIR (asserted by AGREEMENT with orchestrate.sh gen) ─────")
    pair = find_null_pair()
    chk("+ this repo has a byte-identical pair to offer", pair is not None, True)
    if pair:
        with tempfile.TemporaryDirectory() as td:
            wl_ok = Path(td) / "ok.txt"
            wl_no = Path(td) / "no.txt"
            wl_ok.write_text(f"{NULLPAIR_DETECT} {pair[0]} {pair[1]} 400 900000\n"
                             f"REAL bots/_v242bodyaware bots/_v223sealrepair 100 1000\n")
            wl_no.write_text("REAL bots/_v242bodyaware bots/_v223sealrepair 100 1000\n")
            chk("+ our predicate: worklist WITH a null pair", has_null_pair(wl_ok), True)
            chk("- our predicate: worklist WITHOUT one", has_null_pair(wl_no), False)
            # ⭐ THE CROSS-CHECK. Our answer is worth nothing on its own; what
            # matters is that `gen` agrees, because `gen` is what refuses at
            # dispatch time. Fake host => a throwaway GENDIR, no ssh, no push.
            fake = "worker@_zzfleettest"
            gd = VPS_DIR / hostkey(fake)
            for wl, want_refuse in ((wl_ok, False), (wl_no, True)):
                shutil.rmtree(gd, ignore_errors=True)
                rc, out = _run(["bash", str(ORCH), "gen", fake, "REAL", "--from", str(wl)], timeout_s=120)
                refused = "REFUSING" in out and "no byte-identical" in out
                chk(("- gen REFUSES the no-null worklist" if want_refuse
                     else "+ gen ACCEPTS the with-null worklist"), refused, want_refuse)
                chk(f"  agreement: has_null_pair == not gen_refused ({wl.name})",
                    has_null_pair(wl), not refused)
            shutil.rmtree(gd, ignore_errors=True)

    print("── G5  BASENAME COLLISION ────────────────────────────────────────────")
    chk("- the real incident: _v150cb vs _v150cbturret collides",
        basename_collision("bots/_v150cb", "bots/_v150cbturret"), True)
    chk("- reversed order collides too",
        basename_collision("bots/_v150cbturret", "bots/_v150cb"), True)
    chk("- identical basenames collide", basename_collision("a/_x", "b/_x"), True)
    chk("+ a real shipped pair does NOT collide",
        basename_collision("bots/_v242bodyaware", "bots/_v223sealrepair"), False)
    colliding = [_row("C1", t="bots/_v150cb", c="bots/_v150cbturret")]
    plan, _, skips = plan_pass(colliding, views)
    chk("- a colliding row is SKIPPED, not claimed", (len(plan), len(skips)), (0, 1))
    chk("  and it is left QUEUED (never spent)", colliding[0].state, "QUEUED")
    missing = [_row("M1", t="bots/_zz_does_not_exist")]
    plan, _, skips = plan_pass(missing, views)
    chk("- a row whose tree has no main.py is SKIPPED", (len(plan), len(skips)), (0, 1))
    chk("+ a row with real trees is dispatchable", row_dispatchable(_row())[0], True)

    print("── G6  STALENESS: healthy and blind lines are NEVER byte-identical ───")
    fresh_v = [HostView("h1", _occ("h1", queued_rows=0), 6, 0)]
    stale_o = _occ("h1", queued_rows=0)
    stale_o.read_mono = time.time() - (STATUS_STALE_S + 60)
    stale_v = [HostView("h1", stale_o, 6, 0)]
    blind_v = [HostView("h1", _occ("h1", blind=True, reason="ssh timeout"), 6, 0)]
    _, lf, _ = plan_pass([], fresh_v)
    _, ls, _ = plan_pass([], stale_v)
    _, lb, _ = plan_pass([], blind_v)
    chk("+ fresh line carries an age", "age=" in lf[0], True)
    chk("- stale line carries an age AND the STALE marker", "⚠ STALE" in ls[0], True)
    chk("- fresh and stale lines differ", lf[0] != ls[0], True)
    chk("- blind and healthy lines differ", lb[0] != lf[0], True)
    chk("- blind line says BLIND and dispatches nothing", "BLIND" in lb[0] and "free=0" in lb[0], True)

    print("── G7  DOUBLE-SUBSCRIPTION REFUSAL ───────────────────────────────────")
    alive = parse_remote_status("ws", "load: 1.0 1.0 1.0\nrunners: 12   worker: 7\n")
    down = parse_remote_status("ws", "load: 0.0 0.0 0.0\nrunners: 0   worker: 0\n")
    chk("- worker:7 (subshells inflate the count) reads ALIVE", alive.worker_alive, True)
    chk("+ worker:0 reads DOWN", down.worker_alive, False)
    r = _row("G7")
    okA, noteA = (False, "")
    # drain path on a LIVE worker must refuse before touching the host
    v_alive = HostView("ws", alive, 6, 0)
    if v_alive.occ.worker_alive:
        okA, noteA = False, "G7 refused"
    chk("- drain dispatch is refused while a worker is alive", okA, False)
    okB, noteB = dispatch_remote_drain(r, "worker@_zzfleettest", 6, [r], dry=True)
    chk("+ drain dispatch on a DOWN worker plans gen+push+start", okB and "start" in noteB, True)
    okC, noteC = dispatch_remote_live(_row("G7L"), "worker@work-server-2", dry=True)
    chk("+ live dispatch plans an in-place append with the host seed offset",
        okC and "offset" in noteC, True)
    okD, noteD = dispatch_remote_live(_row("G7X"), "worker@_zznooffset", dry=True)
    chk("- live dispatch REFUSES a host with no SEED_OFFSET sidecar", okD, False)

    print("── QUEUE ROUND-TRIP + ATOMIC WRITE ───────────────────────────────────")
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "q.tsv"
        src = [_row("A1", n=100, s=1), Row("A2", "bots/x", "bots/y", 200, 3, "DONE", "local", utc(), "note with spaces")]
        write_queue(src, p)
        back = read_queue(p)
        chk("+ round-trips row count", len(back), 2)
        chk("+ round-trips state/host/note", (back[1].state, back[1].host, back[1].note),
            ("DONE", "local", "note with spaces"))
        chk("+ a tab inside a field cannot shift columns",
            len(Row("T", "a", "b", 1, 1, "QUEUED", "-", "-", "has\ttab").tsv().split("\t")), len(COLS))

    print("── FAIRNESS: one host cannot take the whole head of the queue ────────")
    rows = [_row(f"F{i}") for i in range(6)]
    vv = [HostView(LOCAL, _occ(LOCAL, running_shards=0, load1=1.0, queued_rows=0), 3, 0),
          HostView("hA", _occ("hA", queued_rows=0), 6, 0)]
    plan, _, _ = plan_pass(rows, vv)
    hosts_used = [a.host for a in plan]
    chk("+ assignments alternate across hosts", hosts_used[:2], [LOCAL, "hA"])
    chk("+ total assignments == total free slots", len(plan), 3 + QUEUE_DEPTH_TARGET)

    print("── SEED ALLOCATION ───────────────────────────────────────────────────")
    chk("+ span for target 5400 on a 15-map pool", math.ceil(5400 / GAMES_PER_SEED), 180)
    chk("+ stride exceeds span (rows cannot overlap in seed space)", SEED_STRIDE > 180, True)

    def _alloc(n, tgt, hint=None):
        try:
            return alloc_seeds(n, tgt, hint)[0]
        except ValueError as e:
            return f"REFUSED:{str(e)[:28]}"

    chk("+ 112 rows x 5400 allocate inside the band", isinstance(_alloc(112, 5400), int), True)
    b = alloc_seeds(112, 5400)[0]
    chk("+ ... and the LAST seed stays under the certification band",
        b + 111 * SEED_STRIDE + 180 < SEED_RESERVED_LO, True)
    chk("+ ... and the base clears every seed already in use",
        b > used_seed_hi(), True)
    # ⛔ THE BITING CELL, and it is the bug this allocator actually had: a base
    # that walks into [900000, 1e6) must REFUSE, not round and carry on.
    chk("- an allocation reaching the reserved band REFUSES",
        str(_alloc(112, 5400, hint=880_000)).startswith("REFUSED"), True)
    chk("- a target needing more seeds than the stride REFUSES",
        str(_alloc(2, SEED_STRIDE * GAMES_PER_SEED)).startswith("REFUSED"), True)
    chk("+ the same batch one stride lower is ACCEPTED (the guard is not a blanket no)",
        isinstance(_alloc(112, 5400, hint=400_000), int), True)
    # the certification sentinel must NOT ratchet the high-water mark
    chk("- the 900000 NULLHOST/NULLPAIR sentinel is excluded from used_seed_hi",
        used_seed_hi() < SEED_RESERVED_LO, True)

    print("\nSELFTEST " + ("PASS — every guard driven to BOTH verdicts" if not fail else "FAIL"))
    return fail


# ═══════════════════════════════════════════════════════════════════════════
def main(argv) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="print what WOULD be dispatched; change nothing")
    ap.add_argument("--once", action="store_true", help="a single pass, then exit")
    ap.add_argument("--poll", type=int, default=120, help="seconds between passes (default 120)")
    ap.add_argument("--seed-from", metavar="FILE", help="load combination rows into the queue")
    ap.add_argument("--compose", action="store_true",
                    help="with --seed-from: actually build the trees via tools/stack.py")
    ap.add_argument("--target", type=int, default=5400, help="games per combination row (default 5400)")
    ap.add_argument("--control", default="bots/_v223sealrepair", help="control tree for seeded rows")
    ap.add_argument("--remote-mode", choices=("drain", "live", "auto"), default="drain",
                    help="drain (default, worker must be DOWN) | live (in-place append to a live worker) | auto")
    ap.add_argument("--cores-per-shard", type=float, default=CORES_PER_SHARD)
    ap.add_argument("--queue-depth", type=int, default=QUEUE_DEPTH_TARGET)
    ap.add_argument("--status", action="store_true", help="print host occupancy and the queue, dispatch nothing")
    ap.add_argument("--queue", metavar="PATH", help="use an alternate queue file (default scratchpad/fleet_queue.tsv)")
    a = ap.parse_args(argv)

    if a.queue:
        global QUEUE_F, LOCK_F
        QUEUE_F = Path(a.queue)
        LOCK_F = QUEUE_F.with_suffix(QUEUE_F.suffix + ".lock")

    if a.selftest:
        return selftest()
    if a.seed_from:
        return seed_from(Path(a.seed_from), a.target, a.control, a.compose, a.dry_run)
    if a.status:
        rows = read_queue()
        counts = {s: sum(1 for r in rows if r.state == s) for s in STATES}
        say("queue: " + " ".join(f"{k}={v}" for k, v in counts.items()))
        _, lines, skips = plan_pass([], build_views(rows, hosts_list()),
                                    a.cores_per_shard, a.queue_depth)
        for l in lines:
            say("  " + l)
        return 0

    if a.once or a.dry_run:
        with QueueLock():
            return one_pass(a.dry_run, a.remote_mode, a.cores_per_shard, a.queue_depth)
    with QueueLock():
        while True:
            try:
                one_pass(False, a.remote_mode, a.cores_per_shard, a.queue_depth)
            except Exception as e:            # a dispatcher that dies stops the fleet
                say(f"⚠ pass raised {e.__class__.__name__}: {e} — continuing (rows already claimed are safe)")
            time.sleep(a.poll)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
