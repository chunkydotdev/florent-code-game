#!/usr/bin/env python3
"""REMOTE PER-SHARD CANCEL — the stop path `auto_gate.py --apply` was missing.

Magnus, 2026-08-17 (s48), verbatim: *"I don't want you to stop and manage cores
myself, can this be automated?"* — asked after the builder HAND-STOPPED
KLADLADDER on worker@work-server-1 (42% at n=3,121) because `auto_gate.py` was
REPORT-ONLY for every remote shard. This module is that hand sequence, with the
guards the hand did not have.

═══════════════════════════════════════════════════════════════════════════════
WHY THERE WAS NO REMOTE STOP, AND WHY THERE CAN BE ONE NOW
═══════════════════════════════════════════════════════════════════════════════
`auto_gate.py`'s header said, correctly at the time: THERE IS NO PER-SHARD
CANCEL PRIMITIVE ON A WORKER. `orchestrate.sh stop` writes a GLOBAL STOP file
and halts the whole host; `kill` kills the worker. Neither advances to the next
shard, and `stop` + `start` was worse than either, because `cmd_start` does
`rm -f STOP` and a SLEEPING (curfewed) worker then wakes into a world with no
STOP file and double-subscribes the box — `--tle 10` is WALL-CLOCK, so that
silently corrupts every row BOTH workers produce.

TWO THINGS CHANGED.
  1. `orchestrate.sh cancel <host> <SHARD> <reason>` now exists: it writes a
     `results/<SHARD>.COMPLETE` marker whose TEXT says `CANCELLED at <n> rows`,
     never `reached n/TARGET`. `worker.sh:254` reads that marker at shard START
     and SKIPS the shard. Rows are KEPT. That is the per-shard primitive.
  2. The double-subscription hazard is not inherent to STOP — it is what
     happens when you `start` a host WITHOUT VERIFYING THE OLD WORKER DIED. So
     the cycle here does not assume the halt: it POLLS `status` until the
     host's own worker count reads 0, and refuses to relaunch otherwise.

⇒ THE COMPOSITION, and every step is an EXISTING one-way primitive:
     verify(flagged shard IS the running one, fresh heartbeat)
     -> stop      (global STOP; the worker halts at a BATCH boundary, so every
                   in-flight game finishes and its rows are appended)
     -> poll status until `worker: 0`, bounded          [G-R5]
     -> cancel    (the skip marker; rows kept)          [G-R6]
     -> start     (WORKERS from host_capacity.tsv; cmd_start removes STOP)
     -> verify from worker.out's own `WORKER up` line   [G-R7]
   Net effect: a per-shard cancel that keeps rows, restarts nothing from zero,
   and never edits a state backwards.

⛔ WHY `stop` AND NOT `kill`, WHICH IS WHAT THE OLD MANUAL RECIPE SAID.
`pkill -f tools/vps/worker.sh` matches the worker SHELL only. Its up-to
WORKERS*8 in-flight `fcode run` children keep running, keep burning cores, and
write into a $TMPD nobody will ever append — the batch's rows are LOST, and a
`start` issued on top of those orphans oversubscribes the box, which is the
SALTREF2 wall-clock condition. STOP halts at the batch boundary with every
child reaped and every row appended. `kill` is still the right tool for a
worker that will not halt; it is the wrong tool for a cancel-and-continue.

═══════════════════════════════════════════════════════════════════════════════
⛔ THE INCIDENT THIS MUST NOT REPRODUCE (scratchpad/fleet_queue.tsv header)
═══════════════════════════════════════════════════════════════════════════════
On 2026-08-11 `overnight_watch.sh` RESTARTED NINE COMPLETED SHARDS FROM ZERO
because a dead run and an archived run looked identical to it. The rules that
came out of it and that this module obeys:
  * STATE TRANSITIONS ARE ONE-WAY. Nothing here removes or rewrites a row, a
    `.COMPLETE` marker, a heartbeat or a worklist line.
  * THE ONLY WRITES ON THE HOST are the STOP file (and its removal by
    `cmd_start`) and the per-shard CANCELLED marker.
  * A SHARD THAT DIES IS LOGGED AND LEFT. When a step cannot be VERIFIED, this
    stops and says so; it never "repairs" anything.

DIRECTION OF FAILURE, taken from `orchestrate.sh`'s own curfew reasoning:
WRONG-TOWARD-SLEEPING COSTS US CORES, WRONG-TOWARD-RUNNING COSTS US ROWS. So
every unverified step here fails toward a stopped host — idle cores and a loud
line — never toward a relaunch we could not confirm.

═══════════════════════════════════════════════════════════════════════════════
THE GUARDS. Each is exercised in BOTH directions by --selftest.
═══════════════════════════════════════════════════════════════════════════════
G-R0 HOST KNOWN      — the host string must appear in scratchpad/vps/hosts.txt
                       AND carry a capacity row. The results mirror holds BOTH
                       `work-server-1` and `worker@work-server-1` for the same
                       box; only the dispatchable form may be acted on, because
                       the other one has no ssh user and would reach a
                       different account.
G-R1 STATUS READABLE — no parseable `worker:` count means BLIND, and BLIND is
                       not stopped.
G-R1b SOMEBODY ELSE'S — a STOP file with a live worker means a human is already
     STOP               halting this host. Our cycle ends in `start`, which
                       removes STOP, so acting would revoke their stop. Refuse.
G-R2 FRESH           — the flagged shard's own heartbeat on the HOST must be
                       <= 600s old. A stale heartbeat may already be dead; we
                       do not act on it, we log it for a human.
G-R3 IS THE RUNNING  — worker.sh runs its worklist SERIALLY, so exactly one
     ONE               shard is running per host. If the flagged shard is NOT
                       it, halting the host would interrupt ANOTHER shard's
                       rows for a queued one. We refuse the cycle and instead
                       POISON the flagged shard with its skip marker, which is
                       cheaper, safer, and needs no halt.
G-R4 CURFEW          — inside the blackout, `worker.sh` sleeps in curfew_wait()
                       BEFORE its STOP test, so STOP is a documented NO-OP and
                       the bounded wait could only time out. Refuse; the cores
                       are asleep anyway, so nothing is being wasted.
G-R5 HALT VERIFIED   — relaunch only after the host's OWN worker count reads 0.
                       On timeout: LEAVE STOP IN PLACE, write no marker, do not
                       relaunch. Idle cores, loud line, nothing corrupted.
G-R6 MARKER VERIFIED — the cancel must print a marker containing `CANCELLED`.
                       If it did not take, relaunching would RESUME the very
                       shard we meant to kill, so we do not relaunch.
G-R8 RELAUNCH HOLD   — ⭐ NEW s48. Before the relaunch (and ONLY the relaunch),
                       an operator-settable HOLD marker is re-read. If one is
                       present the worker is NOT restarted: the shard stays
                       cancelled with its rows, the host stays stopped, and the
                       refusal is shouted. See THE RELAUNCH RACE below.
G-R7 RELAUNCH        — verified off the worker's OWN `WORKER up` line in
     VERIFIED          worker.out (which `cmd_start` truncates), never off an
                       exit code: on this platform an exit code is not a health
                       signal. If it cannot be read, say so loudly and leave
                       the host stopped.

═══════════════════════════════════════════════════════════════════════════════
⛔ THE RELAUNCH RACE, AND THE HOLD MARKER THAT CLOSES HALF OF IT (s48 debt 23)
═══════════════════════════════════════════════════════════════════════════════
THE INCIDENT, 2026-08-17: the stop -> poison -> RELAUNCH cycle picks up the next
serial worklist row IMMEDIATELY, and on that day the relaunch landed inside the
window between a SIBLING shard's clause firing and the operator decision that
the sibling's prereg REQUIRED before anything further was launched. SEALSENTA
went up on its own, ran 240 games, and had to be cancelled and disclosed on its
own results row. Nothing in this module was wrong; the cycle simply had no way
to be told "not yet".

⇒ THE HOLD MARKER. A file under `scratchpad/fleet_hold/` whose NAME is either
  the dispatchable host string (`worker@work-server-1`) or the literal `ALL`.
  Its CONTENTS are free text and are quoted verbatim into the refusal, so the
  operator's reason travels with the refusal instead of living in someone's
  head. Set it BEFORE (or during) a cancel:
      mkdir -p scratchpad/fleet_hold
      echo 'SEALSENT sibling clause fired; decision pending' \
          > scratchpad/fleet_hold/worker@work-server-1
  and clear it with `rm` when the decision is made.

⛔ IT GATES THE RELAUNCH, NOT THE CANCEL, AND THAT ASYMMETRY IS THE DESIGN.
  Stopping a shard the gate has already condemned costs nothing and keeps its
  rows; LAUNCHING the next row is the irreversible half (240 games and a
  disclosure). So with a HOLD set the cycle still stops, still writes the skip
  marker, and then leaves the host DOWN — idle cores and a loud line, which is
  this module's standing direction of failure. Restarting is then a human
  action taken with the decision already made.

⛔ IT IS RE-READ AT THE RELAUNCH INSTANT, not only at plan time. The halt poll
  can take up to 900s, and the SEALSENTA window was minutes wide — an operator
  who sets the marker WHILE the host is halting must still be obeyed. plan_cancel
  reports the marker it can see for the DRY-RUN's benefit; run_plan's read
  immediately before `start` is the load-bearing one.

⛔ BLIND RESOLVES TO HELD, the same way `in_curfew` resolves BLIND to CURFEWED.
  An unreadable hold directory means we cannot tell, and the cheap error is a
  stopped host.

⚠ THE OTHER HALF IS NOT BUILT: automatically detecting that the NEXT worklist
  row's prereg carries a FIRED SIBLING-CLAUSE. See the PROPOSED-NOT-BUILT note
  above `relaunch_hold` for why that detection is riskier than the defect.

USAGE
    tools/remote_cancel.py --selftest
    tools/remote_cancel.py --host worker@work-server-1 --shard KLADLADDER \\
        --reason "auto_gate TREND-FLOOR@2700"          # DRY-RUN by default
    tools/remote_cancel.py ... --apply                 # actually do it
It is normally driven by `tools/auto_gate.py --apply`, not by hand.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0. Gated on
# `__main__` because this module is IMPORTED by auto_gate.py — ungated it would
# fire during that import and make the PARENT exit 0 mid-run.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

# ONE authority for the allocation, imported rather than copied: a second copy
# is the one nobody tests, and this exact number has been wrong three times
# (scratchpad/vps/host_capacity.tsv's own header).
from fleet_dispatch import host_capacity, hosts_list  # noqa: E402

ORCH = REPO / "tools/vps/orchestrate.sh"
WORKER_SH = REPO / "tools/vps/worker.sh"

FRESH_S = 600          # heartbeat freshness, same 600s `orchestrate status` prints
# ⛔ THE BOUND IS ALSO A BUDGET, because the caller is a LOOP. auto_gate runs
# as `while true; do auto_gate --apply; sleep 600; done`, so this cycle blocks
# the LOCAL stopper for as long as it waits — 900+120s worst case, under two
# ticks. A ws1 batch is WORKERS*8 = 80 games and its heartbeat moves every few
# minutes, so 900s is many batches of headroom. Past it we stop waiting rather
# than stop the world: STOP stays on the host, the host halts on its own and
# goes IDLE, and a human reads the loud line. Idle cores, no corrupted rows.
HALT_WAIT_S = 900
HALT_POLL_S = 30
UP_WAIT_S = 120        # how long a relaunched worker gets to print `WORKER up`
UP_POLL_S = 10
LIVE_STATES = ("RUNNING", "STARTING")

# G-R8. One directory, two accepted names: the dispatchable host string, and the
# literal ALL for a fleet-wide hold. Absent directory == no hold (the normal
# state), so nothing has to be created for the tool to keep working.
HOLD_DIR = REPO / "scratchpad/fleet_hold"
HOLD_ALL = "ALL"


# ═════════════════════════════════════════════════════════════════════════════
# TRANSPORT — one indirection, so the selftest exercises the real logic
# ═════════════════════════════════════════════════════════════════════════════
def orch_runner(argv: list[str], timeout_s: int = 180) -> tuple[int, str, str]:
    """Run `orchestrate.sh <argv...>`. Returns (rc, stdout, stderr).

    ⛔ THE RC IS RETURNED BUT NEVER GATED ON by this module — every decision
    below reads a LOAD-BEARING FIELD out of stdout instead (`worker: N`, the
    marker text, the `WORKER up` line). That is this repo's standing rule and
    it is not cosmetic here: ssh prints post-quantum warnings on stderr and
    `orchestrate status` exits 0 whether or not the host answered usefully.
    """
    try:
        p = subprocess.run(["bash", str(ORCH)] + argv, capture_output=True,
                           text=True, timeout=timeout_s)
        return p.returncode, p.stdout or "", p.stderr or ""
    except subprocess.TimeoutExpired:
        return 124, "", f"TIMEOUT after {timeout_s}s: orchestrate.sh {' '.join(argv)}"
    except OSError as e:
        return 125, "", f"cannot execute orchestrate.sh: {e}"


# ═════════════════════════════════════════════════════════════════════════════
# STATUS PARSING
# ═════════════════════════════════════════════════════════════════════════════
@dataclass
class ShardStat:
    rows: int
    target: int
    age_s: int
    status: str


@dataclass
class Status:
    ok: bool
    why: str = ""
    host_utc: str | None = None
    worker_count: int | None = None
    runners: int | None = None
    stop_present: bool = False
    shards: dict[str, ShardStat] = field(default_factory=dict)


_RE_UTC = re.compile(r"\butc:\s*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)")
_RE_WORKER = re.compile(r"\bworker:\s*(\d+)")
_RE_RUNNERS = re.compile(r"\brunners:\s*(\d+)")
_RE_ROW = re.compile(r"^(\S+)\s+(\d+)\s+(\d+)\s+(\d+)s\s+(\S+)")


def parse_status(out: str | None) -> Status:
    """Parse `orchestrate.sh status <host>` stdout.

    ⛔ BLIND IS NOT IDLE. A missing `worker:` line is not "no workers" — it is
    "we could not see", and every caller must treat it as a refusal. That is
    the same failure `orchestrate.sh` itself hit when a bad pgrep could never
    return 0: a guard that cannot report the passing state is not a guard, and
    one that reports the passing state when it saw NOTHING is worse.
    """
    if not out or not out.strip():
        return Status(False, why="no status output at all (host unreachable?)")
    m = _RE_WORKER.search(out)
    if not m:
        return Status(False, why="no `worker: N` line in the status output — BLIND")
    st = Status(True, worker_count=int(m.group(1)))
    mr = _RE_RUNNERS.search(out)
    st.runners = int(mr.group(1)) if mr else None
    mu = _RE_UTC.search(out)
    st.host_utc = mu.group(1) if mu else None
    st.stop_present = "STOP FILE PRESENT" in out
    for line in out.splitlines():
        mrow = _RE_ROW.match(line.strip())
        if not mrow:
            continue
        st.shards[mrow.group(1)] = ShardStat(int(mrow.group(2)), int(mrow.group(3)),
                                             int(mrow.group(4)), mrow.group(5))
    return st


def live_shards(st: Status, fresh_s: int = FRESH_S) -> list[str]:
    """Shards whose heartbeat says RUNNING/STARTING AND is fresh.

    worker.sh is SERIAL — one shard at a time per host — so this list is
    normally 0 or 1 long. More than one means two workers are on the box, which
    is the double-subscription condition, and the caller must refuse.
    """
    return sorted(k for k, v in st.shards.items()
                  if v.status in LIVE_STATES and v.age_s <= fresh_s)


# ═════════════════════════════════════════════════════════════════════════════
# CURFEW — read from the two files that own it, never re-stated here
# ═════════════════════════════════════════════════════════════════════════════
def curfew_window(path: Path | None = None) -> tuple[int, int] | None:
    """(start_hhmm, end_hhmm) parsed out of worker.sh's own test. None = BLIND.

    Duplicating the literals would put the blackout in two places, and this
    repo's marks/gate_watch pair already demonstrates the fix: read the
    authority, alarm when it moves.
    """
    try:
        src = (path or WORKER_SH).read_text()
    except OSError:
        return None
    m = re.search(r'\[\s*"\$hm"\s*-ge\s*(\d{3,4})\s*\]\s*\|\|\s*\[\s*"\$hm"\s*-lt\s*(\d{3,4})\s*\]', src)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def no_curfew_hosts(path: Path | None = None) -> set[str] | None:
    """Hosts orchestrate.sh has EXPLICITLY cleared to run around the clock.

    ⚠ Phrased as the EXEMPTION, exactly as orchestrate.sh phrases it: anything
    not listed defaults to CURFEW=on. Unparseable returns None, and the caller
    treats None as "assume curfew" — wrong-toward-sleeping costs cores, and the
    other error costs somebody else their machine at midnight.
    """
    try:
        src = (path or ORCH).read_text()
    except OSError:
        return None
    m = re.search(r"^NO_CURFEW_HOSTS=\$\{NO_CURFEW_HOSTS:-([^}]*)\}", src, re.M)
    if not m:
        return None
    return {h for h in m.group(1).split() if h}


def in_curfew(host: str, host_utc: str | None,
              window: tuple[int, int] | None,
              exempt: set[str] | None) -> tuple[bool, str]:
    """(is_curfewed, why). BLIND on either input resolves to CURFEWED."""
    bare = host.split("@")[-1]
    if exempt is None:
        return True, "cannot parse NO_CURFEW_HOSTS from orchestrate.sh — assuming CURFEW"
    if bare in exempt:
        return False, f"{bare} is on orchestrate.sh's round-the-clock list"
    if window is None:
        return True, "cannot parse the curfew window from worker.sh — assuming CURFEW"
    if not host_utc:
        return True, "no `utc:` line in the host's status — assuming CURFEW"
    try:
        hm = int(host_utc[11:13] + host_utc[14:16])
    except (ValueError, IndexError):
        return True, f"unparseable host clock {host_utc!r} — assuming CURFEW"
    lo, hi = window
    inside = hm >= lo or hm < hi
    return inside, (f"host clock {hm:04d} {'INSIDE' if inside else 'outside'} "
                    f"the {lo:04d}-{hi:04d} blackout")


# ═════════════════════════════════════════════════════════════════════════════
# G-R8 RELAUNCH HOLD — the operator's "not yet"
# ═════════════════════════════════════════════════════════════════════════════
# ⚠⚠ PROPOSED-NOT-BUILT, DELIBERATELY: AUTOMATIC FIRED-SIBLING-CLAUSE DETECTION.
# The other half of debt 23 was to read the NEXT worklist row, resolve it to a
# prereg, decide whether that prereg carries a FIRED sibling clause, and POISON
# the row instead of launching it. It is not built, and the reason is that its
# failure mode is WORSE THAN THE DEFECT:
#   * NO SIBLING FIELD EXISTS. Neither the worklist (5 positional fields, and a
#     6th lands inside $SL — see BARS.tsv's own header) nor BARS.tsv nor the
#     heartbeat carries a sibling relation. It would have to be inferred by
#     grepping docs/prereg/*.md, i.e. exactly the "derived by grep" mechanism
#     BARS.tsv exists to avoid.
#   * THE INPUT IS A STALE LOCAL MIRROR. This module learns nothing about
#     worklist ORDER from the host; it would read
#     scratchpad/overnight-remote/<host>/worklist.txt, a pull whose freshness is
#     not verified here. Deciding what to poison off a stale mirror is the
#     `overnight_watch.sh` shape that restarted nine completed shards.
#   * ITS ERROR IS ONE-WAY AND SILENT. A poison writes a `.COMPLETE` skip marker
#     on the host. A FALSE poison therefore RETIRES A LEGITIMATE SHARD FOREVER,
#     with no rows and no alarm — strictly worse than the defect it closes,
#     which cost 240 games that were cancelled and disclosed. A HOLD only ever
#     errs toward idle cores.
# The exact diff, if it is ever wanted, is recorded in the s48 WRAP-FIX report.
# The HOLD marker below is the half whose worst case is cheap.
def relaunch_hold(host: str, hold_dir: Path | None = None) -> tuple[bool, str]:
    """(is_held, why). BLIND resolves to HELD.

    Checked immediately before `start`, never before the cancel: see the module
    header. A marker for ANOTHER host must not hold this one, which is why the
    lookup is by exact filename and not by any substring match.
    """
    d = HOLD_DIR if hold_dir is None else hold_dir
    try:
        if not d.exists():
            return False, f"no hold directory at {d} — nothing is holding relaunches"
        if not d.is_dir():
            return True, (f"⛔ {d} EXISTS BUT IS NOT A DIRECTORY — the hold check is "
                          f"BLIND, and blind resolves to HELD")
        for name in (host, HOLD_ALL):
            p = d / name
            if p.exists():
                txt = " ".join(p.read_text(errors="replace").split())[:300]
                scope = ("FLEET-WIDE" if name == HOLD_ALL else f"host {host}")
                return True, (f"HOLD marker {p} ({scope}) says: "
                              f"{txt or '(the marker file is empty)'}")
    except OSError as e:
        return True, (f"⛔ cannot read the hold directory {d} ({e.__class__.__name__}: "
                      f"{e}) — BLIND, and blind resolves to HELD")
    return False, f"no hold marker for {host} (or {HOLD_ALL}) in {d}"


# ═════════════════════════════════════════════════════════════════════════════
# THE PLAN — read-only. Nothing here mutates the host.
# ═════════════════════════════════════════════════════════════════════════════
@dataclass
class Plan:
    verdict: str          # "STOP-CYCLE" | "SKIP-POISONED" | "REFUSE"
    reason: str
    host: str
    shard: str
    cores: int | None = None
    status: Status | None = None
    lines: list[str] = field(default_factory=list)


def plan_cancel(host: str, shard: str, *, runner=orch_runner,
                fresh_s: int = FRESH_S, capacity=host_capacity,
                hosts=hosts_list, window=None, exempt=None,
                hold_dir: Path | None = None) -> Plan:
    """Decide WHAT to do. Runs `status` only; changes nothing.

    ⚠ The G-R8 hold is REPORTED here (so a DRY-RUN discloses it) but ENFORCED in
    run_plan, which re-reads it at the relaunch instant. A hold seen at plan
    time is not the decision; the one seen ~900s later is.
    """
    log: list[str] = []

    def refuse(msg):
        return Plan("REFUSE", msg, host, shard, lines=log)

    # ---- G-R0: the host must be one we dispatch to ------------------------
    known = [h for h in hosts() if h == host]
    cores = capacity(host)
    if not known:
        return refuse(f"⛔ G-R0 HOST NOT DISPATCHABLE: {host!r} is not a line in "
                      f"scratchpad/vps/hosts.txt. The results mirror carries both "
                      f"`work-server-1` and `worker@work-server-1` for one box and only "
                      f"the user-qualified form reaches the right account.")
    if not cores:
        return refuse(f"⛔ G-R0 NO CAPACITY ROW for {host!r} in "
                      f"scratchpad/vps/host_capacity.tsv — WORKERS must be sized against "
                      f"our allocation and never against nproc, so a relaunch is refused.")
    log.append(f"G-R0 host {host} dispatchable, allocation {cores} cores")

    rc, out, err = runner(["status", host])
    st = parse_status(out)
    if not st.ok:
        return refuse(f"⛔ G-R1 STATUS UNREADABLE ({st.why}; rc={rc} "
                      f"stderr={err.strip()[:120]!r}) — BLIND is not stopped.")
    log.append(f"G-R1 status readable: worker={st.worker_count} runners={st.runners} "
               f"stop_file={st.stop_present} host_utc={st.host_utc} "
               f"shards_seen={len(st.shards)}")

    seen = st.shards.get(shard)
    live = live_shards(st, fresh_s)

    # ---- worker already down: nothing to halt -----------------------------
    if st.worker_count == 0:
        if seen is None and shard not in live:
            return refuse(f"⛔ {shard} is not known on {host} (no heartbeat row) and no "
                          f"worker is running — nothing to do here.")
        return Plan("SKIP-POISONED",
                    f"no worker process on {host}; the shard is not running, so the skip "
                    f"marker alone retires it (no halt, no relaunch — starting the host is "
                    f"the dispatcher's decision, not the canceller's)",
                    host, shard, cores, st, log)

    if st.worker_count is None or st.worker_count < 0:
        return refuse("⛔ G-R1 worker count unreadable — BLIND is not stopped.")

    # ---- G-R1b: SOMEONE ELSE IS ALREADY STOPPING THIS HOST -----------------
    # A STOP file with a worker still alive means a human (or another tool)
    # asked this host to halt and it has not reached its batch boundary yet.
    # Our cycle ENDS in `start`, and `cmd_start` does `rm -f STOP` — so
    # proceeding would silently revoke somebody's deliberate stop and restart a
    # box they wanted down. This is exactly the state ws1 was left in by the
    # hand-stop that prompted this tool. Refuse and let their halt finish.
    # (With NO worker alive the STOP file is just a stopped host: the poison
    # path above touches nothing and starts nothing, so it stays allowed.)
    if st.stop_present:
        return refuse(f"⛔ G-R1b: {host} already has a STOP file AND {st.worker_count} live "
                      f"worker(s) — somebody is halting this host right now. Our cycle ends "
                      f"in `start`, which removes STOP, so acting would revoke their stop. "
                      f"Refusing; re-evaluate on the next tick.")

    # ---- G-R3: is the flagged shard the RUNNING one? ----------------------
    if len(live) > 1:
        return refuse(f"⛔ TWO LIVE SHARDS on {host} ({', '.join(live)}). worker.sh is "
                      f"SERIAL, so this means two workers share the box — the "
                      f"double-subscription condition. Refusing every action; this needs "
                      f"a human and a `kill`.")
    if shard not in live:
        if seen is not None and seen.status in LIVE_STATES:
            # It CLAIMS to be running and its heartbeat is stale: G-R2's case.
            return refuse(f"⛔ G-R2 STALE: {shard} reads {seen.status} on {host} but its "
                          f"heartbeat is {seen.age_s}s old (> {fresh_s}s). BLIND IS NOT "
                          f"STOPPED — it may already be dead. Logged for a human; "
                          f"currently live shard: {live or 'none'}.")
        return Plan("SKIP-POISONED",
                    f"⚠ G-R3: {shard} is NOT the running shard on {host} "
                    f"(running: {live or 'none'}; {shard} reads "
                    f"{seen.status if seen else 'no heartbeat'}). Another shard's rows are "
                    f"never interrupted for this one. Writing the skip marker instead, so "
                    f"the worker never resumes it.",
                    host, shard, cores, st, log)

    # ---- G-R2: freshness of the shard we are about to halt for ------------
    if seen is None or seen.age_s > fresh_s:
        return refuse(f"⛔ G-R2 STALE/absent heartbeat for {shard} — refusing.")
    log.append(f"G-R2 {shard} heartbeat {seen.age_s}s old (<= {fresh_s}s) — fresh")
    log.append(f"G-R3 {shard} IS the running shard on {host} "
               f"({seen.rows}/{seen.target} rows, status {seen.status})")

    # ---- G-R4: curfew ------------------------------------------------------
    curfewed, why = in_curfew(host, st.host_utc,
                              window if window is not None else curfew_window(),
                              exempt if exempt is not None else no_curfew_hosts())
    if curfewed:
        return refuse(f"⛔ G-R4 CURFEW: {why}. worker.sh calls curfew_wait() BEFORE its "
                      f"STOP test, so STOP is a documented NO-OP inside the blackout and "
                      f"the bounded wait could only time out. The cores are asleep anyway.")
    log.append(f"G-R4 curfew: {why}")

    # ---- G-R8: report the hold now; run_plan re-reads it before `start` -----
    held, hwhy = relaunch_hold(host, hold_dir)
    log.append(f"G-R8 relaunch hold at plan time: {'HELD' if held else 'clear'} — {hwhy}")
    tail = (f"stop -> verify halt -> cancel -> ⛔ NO RELAUNCH (G-R8 hold is set: "
            f"{hwhy}); the host is left stopped"
            if held else
            f"stop -> verify halt -> cancel -> relaunch at WORKERS={cores}")
    return Plan("STOP-CYCLE",
                f"{shard} is the live shard on {host} at {seen.rows}/{seen.target}; "
                + tail, host, shard, cores, st, log)


# ═════════════════════════════════════════════════════════════════════════════
# EXECUTION — the only writes on the host are STOP and the skip marker
# ═════════════════════════════════════════════════════════════════════════════
def _cancel_marker(runner, host: str, shard: str, reason: str,
                   queued: bool) -> tuple[bool, str]:
    argv = ["cancel", host, shard, reason]
    if queued:
        argv.append("--queued")
    rc, out, err = runner(argv)
    text = (out + err).strip()
    ok = ("CANCELLED" in out) or ("already marked" in out)
    return ok, text


def run_plan(plan: Plan, reason: str, *, runner=orch_runner, sleep=time.sleep,
             halt_wait_s: int = HALT_WAIT_S, halt_poll_s: int = HALT_POLL_S,
             up_wait_s: int = UP_WAIT_S, up_poll_s: int = UP_POLL_S,
             clock=time.time, hold_dir: Path | None = None) -> tuple[bool, list[str]]:
    """Execute a plan. Returns (ok, log lines). Never raises on a host fault."""
    log = list(plan.lines)

    if plan.verdict == "REFUSE":
        log.append(plan.reason)
        return False, log

    # ---------------------------------------------------------------- poison
    if plan.verdict == "SKIP-POISONED":
        log.append(f"SKIP-POISONED {plan.shard}: {plan.reason}")
        ok, text = _cancel_marker(runner, plan.host, plan.shard, reason, queued=True)
        log.append("  cancel output: " + " | ".join(text.splitlines()[-3:]))
        if not ok:
            log.append(f"⛔ MARKER NOT CONFIRMED for {plan.shard} on {plan.host}. Nothing "
                       f"else was touched; the host is unchanged. A human should read the "
                       f"refusal above.")
            return False, log
        log.append(f"✔ {plan.shard} will be SKIPPED when the worker reaches its worklist "
                   f"row. Rows KEPT. No worker was halted.")
        return True, log

    # ------------------------------------------------------------ stop cycle
    log.append(f"STOP-CYCLE {plan.shard} on {plan.host}: {plan.reason}")
    rc, out, err = runner(["stop", plan.host])
    log.append("  stop: " + " | ".join((out + err).strip().splitlines()[-2:]))

    # G-R5: wait for the host's OWN worker count to read 0.
    t0 = clock()
    halted = False
    last = "no status read"
    while clock() - t0 < halt_wait_s:
        sleep(halt_poll_s)
        _rc, sout, _serr = runner(["status", plan.host])
        st = parse_status(sout)
        if not st.ok:
            last = f"status BLIND ({st.why})"
            log.append(f"  wait {clock() - t0:.0f}s: {last}")
            continue
        cur = live_shards(st)
        last = f"worker={st.worker_count} live={cur or 'none'}"
        log.append(f"  wait {clock() - t0:.0f}s: {last}")
        if st.worker_count == 0:
            halted = True
            break
    if not halted:
        log.append(
            f"⛔⛔ G-R5 HALT NOT VERIFIED after {halt_wait_s}s ({last}). THE STOP FILE IS "
            f"LEFT IN PLACE ON PURPOSE: the worker will halt at its next batch boundary "
            f"and the host will go IDLE. No marker was written and nothing was "
            f"relaunched, so {plan.shard} resumes if a human starts the host — which is "
            f"the correct direction (wrong-toward-sleeping costs cores; "
            f"wrong-toward-running costs rows). MANUAL ATTENTION: "
            f"tools/vps/orchestrate.sh status {plan.host}")
        return False, log
    log.append(f"  G-R5 halt VERIFIED: worker count 0 on {plan.host} "
               f"(rows for the in-flight batch were appended before it exited)")

    # G-R6: the skip marker.
    ok, text = _cancel_marker(runner, plan.host, plan.shard, reason, queued=False)
    log.append("  cancel output: " + " | ".join(text.splitlines()[-3:]))
    if not ok:
        log.append(
            f"⛔⛔ G-R6 MARKER NOT CONFIRMED for {plan.shard}. NOT RELAUNCHING: a restart "
            f"now would RESUME the shard we just stopped. STOP is left in place and the "
            f"host stays idle until a human looks.")
        return False, log
    log.append(f"  G-R6 skip marker CONFIRMED — {plan.shard} keeps its rows and will be "
               f"skipped, not resumed")

    # ---- G-R8: THE LAST THING BEFORE THE IRREVERSIBLE HALF ------------------
    # ⛔ RE-READ HERE, NOT AT PLAN TIME. Everything above this line can take up
    # to halt_wait_s (900s default) and the operator's decision window is
    # minutes wide — a marker set WHILE the host was halting must still be
    # obeyed, which is exactly the SEALSENTA shape this guard exists for.
    held, hwhy = relaunch_hold(plan.host, hold_dir)
    if held:
        log.append(
            f"⛔⛔ G-R8 RELAUNCH HELD — NOT STARTING {plan.host}. {hwhy}\n"
            f"      {plan.shard} IS CANCELLED and its rows are KEPT; the skip marker is "
            f"written. What did NOT happen is the RELAUNCH, so the NEXT worklist row was "
            f"NOT launched — which is the entire point of the marker (s48 debt 23: a "
            f"relaunch inside a sibling's decision window burned 240 games on SEALSENTA).\n"
            f"      THE HOST IS LEFT STOPPED: idle cores, the cheap error. When the "
            f"decision is made, clear the marker and start it by hand:\n"
            f"        rm {(HOLD_DIR if hold_dir is None else hold_dir)}/{plan.host}   "
            f"# (or .../{HOLD_ALL})\n"
            f"        tools/vps/orchestrate.sh start {plan.host} {plan.cores}")
        return False, log
    log.append(f"  G-R8 relaunch hold: clear — {hwhy}")

    # Relaunch. cmd_start removes STOP itself; the old worker is verified gone.
    rc, out, err = runner(["start", plan.host, str(plan.cores)])
    log.append("  start: " + " | ".join((out + err).strip().splitlines()[-3:]))

    # G-R7: verified off the worker's OWN log, never off an exit code.
    t1 = clock()
    up = False
    tail = ""
    while clock() - t1 < up_wait_s:
        sleep(up_poll_s)
        _rc, lout, _lerr = runner(["logs", plan.host, "60"])
        tail = lout
        if "WORKER up" in lout:
            up = True
            break
        log.append(f"  relaunch wait {clock() - t1:.0f}s: no `WORKER up` line yet")
    if not up:
        refusals = [ln for ln in tail.splitlines() if "REFUS" in ln or "⛔" in ln]
        log.append(
            f"⛔⛔ G-R7 RELAUNCH NOT VERIFIED on {plan.host}: no `WORKER up` line in "
            f"worker.out within {up_wait_s}s. THE HOST IS LEFT STOPPED — idle cores, "
            f"which is the cheap error. The shard is cancelled (marker written, rows "
            f"kept). MANUAL ATTENTION: tools/vps/orchestrate.sh logs {plan.host}"
            + (("  ||  worker.out says: " + " | ".join(refusals[:3])) if refusals else ""))
        return False, log
    picked = [ln for ln in tail.splitlines() if re.search(r"\bSHARD \S+ ", ln)]
    log.append(f"  G-R7 relaunch VERIFIED from worker.out's own `WORKER up` line"
               + (f"; it picked up: {picked[-1].strip()[:110]}" if picked else
                  "; no SHARD line yet (it is still gating)"))
    log.append(f"✔ {plan.shard} CANCELLED on {plan.host}; rows kept; the worker is back "
               f"up and continues with the next unfinished worklist row.")
    return True, log


def cancel_remote_shard(host: str, shard: str, reason: str, *, apply: bool,
                        runner=orch_runner, hold_dir: Path | None = None,
                        **kw) -> tuple[bool, str, list[str]]:
    """plan + (optionally) execute. Returns (ok, verdict, log lines).

    `hold_dir` goes to BOTH halves on purpose: plan_cancel so the DRY-RUN
    discloses a hold, run_plan so it is re-read at the relaunch instant.
    """
    plan = plan_cancel(host, shard, runner=runner, hold_dir=hold_dir)
    if not apply:
        return (plan.verdict != "REFUSE"), plan.verdict, \
            plan.lines + [f"DRY-RUN — would {plan.verdict}: {plan.reason}"]
    ok, log = run_plan(plan, reason, runner=runner, hold_dir=hold_dir, **kw)
    return ok, plan.verdict, log


# ═════════════════════════════════════════════════════════════════════════════
# SELFTEST — every guard in BOTH directions, against a simulated host
# ═════════════════════════════════════════════════════════════════════════════
class FakeHost:
    """A worker host that answers `orchestrate.sh` the way a real one does.

    ⛔ IT IS NOT A MOCK THAT AGREES WITH ME. The status text it emits is the
    literal format string from `orchestrate.sh cmd_status` (`%-14s %8s %8s
    %9ss %s`), and its `cancel` refuses under the same conditions the shell
    does, so the parser under test faces the real shape. `orchestrate.sh
    --local-sim` exercises the SHELL against a local directory; this exercises
    THIS module against the shell's OUTPUT. Both are needed and neither is the
    other.
    """

    def __init__(self, *, workers=1, shards=None, utc="2026-08-17T10:00:00Z",
                 stop_file=False, cancel_ok=True, halt_after=1, start_ok=True,
                 status_blind=False):
        self.workers = workers
        self.shards = shards or {}
        self.utc = utc
        self.stop_file = stop_file
        self.cancel_ok = cancel_ok
        self.halt_after = halt_after       # polls before the worker exits
        self.start_ok = start_ok
        self.status_blind = status_blind
        self.calls: list[str] = []
        self.stopped = False
        self.markers: list[str] = []
        self._polls = 0
        self.worker_out = ""

    def __call__(self, argv, timeout_s=180):
        self.calls.append(" ".join(argv))
        cmd = argv[0]
        if cmd == "status":
            if self.status_blind:
                return 0, "host: sim   utc: %s   NPROC: 16\n(unreachable)\n" % self.utc, ""
            if self.stopped:
                self._polls += 1
                if self._polls >= self.halt_after:
                    self.workers = 0
            lines = [f"host: sim   utc: {self.utc}   NPROC: 16",
                     "load: 0.10 0.20 0.30",
                     f"runners: {0 if self.workers == 0 else 8}   worker: {self.workers}"]
            if self.stop_file or self.stopped:
                lines.append("*** STOP FILE PRESENT ***")
            lines.append("%-14s %8s %8s %10s %s" % ("SHARD", "ROWS", "TARGET", "HB_AGE", "STATUS"))
            for sid, (rows, target, age, stt) in self.shards.items():
                lines.append("%-14s %8s %8s %9ss %s" % (sid, rows, target, age, stt))
            return 0, "\n".join(lines) + "\n", ""
        if cmd == "stop":
            self.stopped = True
            return 0, "STOP written — the worker halts at the next batch boundary\n", ""
        if cmd == "cancel":
            shard = argv[2]
            if self.workers != 0 and "--queued" not in argv:
                return 3, "⛔ REFUSING: 1 worker(s) still alive.\n", ""
            if not self.cancel_ok:
                return 4, "⛔ REFUSING: unknown shard\n", ""
            self.markers.append(shard)
            return 0, (f"cancelled {shard} at 3404 rows; marker written:\n"
                       f"   2026-08-17T10:00:00Z {shard} CANCELLED at 3404 rows by: "
                       f"auto_gate -- rows KEPT, this is NOT a completed run\n"), ""
        if cmd == "start":
            self.stopped = False
            self.workers = 1 if self.start_ok else 0
            self.worker_out = ("2026-08-17T10:05:00Z WORKER up. host=sim ncpu=16 workers=10\n"
                               "2026-08-17T10:05:01Z SHARD NEXTONE  a vs b  target=5400\n"
                               if self.start_ok else
                               "2026-08-17T10:05:00Z ⛔ REFUSING: ENGINE PIN MISMATCH\n")
            return 0, "STARTED on sim (nohup).\n", ""
        if cmd == "logs":
            return 0, self.worker_out or "(no worker.out)\n", ""
        return 2, "", f"unknown subcommand {cmd}"


def selftest() -> int:
    fails: list[str] = []

    def chk(label, got, want):
        if got == want:
            print(f"  PASS  {label:<76} -> {got}")
        else:
            print(f"  FAIL  {label:<76} -> {got} (want {want})")
            fails.append(label)

    def vclock():
        """A VIRTUAL clock for the bounded waits.

        ⛔ NOT A CONVENIENCE. With the real clock and a no-op sleep, the
        halt-timeout cell SPINS — and the first cut of this selftest passed
        that cell for the wrong reason: a million status polls in 90 real
        seconds reached the fixture's `halt_after` and the worker "halted".
        The test that was supposed to prove the timeout proved the opposite and
        said PASS. Time advances by the poll interval, once per sleep.
        """
        now = [0.0]
        return (lambda: now[0]), (lambda s: now.__setitem__(0, now[0] + s))

    HOSTS = lambda: ["local", "worker@work-server-1", "worker@work-server-2"]  # noqa: E731
    CAP = lambda h: {"worker@work-server-1": 10, "worker@work-server-2": 6}.get(h)  # noqa: E731
    # ⛔ EVERY cell that reaches the relaunch passes an explicitly ABSENT hold
    # directory. Without this the selftest would read the LIVE
    # scratchpad/fleet_hold, and an operator who legitimately set a marker would
    # make the "full cycle succeeds" cell FAIL for a reason that has nothing to
    # do with the code. A test whose verdict depends on live operator state is
    # not a test. The hold cells below supply their own fixture directories.
    NOHOLD = Path("/nonexistent/remote_cancel-selftest-no-hold-dir")
    OUTSIDE = "2026-08-17T10:00:00Z"   # outside 2055-0400
    INSIDE = "2026-08-17T22:10:00Z"    # inside it
    WIN = (2055, 400)
    EXEMPT = {"work-server-2"}

    print("── parse_status: the real cmd_status shape, and BLIND both ways ────────")
    fh = FakeHost(shards={"KLAD": (3404, 5400, 12, "RUNNING"),
                          "OLD": (5400, 5400, 99999, "COMPLETE")})
    st = parse_status(fh(["status", "h"])[1])
    chk("status parses the worker count", st.worker_count, 1)
    chk("...and the shard table", (st.shards["KLAD"].rows, st.shards["KLAD"].age_s), (3404, 12))
    chk("...and the header row is NOT read as a shard", "SHARD" in st.shards, False)
    chk("...and STOP-file absence", st.stop_present, False)
    chk("a STOP file is seen when present",
        parse_status(FakeHost(stop_file=True)(["status", "h"])[1]).stop_present, True)
    chk("⛔ output with no `worker:` line is BLIND, not idle",
        parse_status("host: x   utc: 2026-01-01T00:00:00Z").ok, False)
    chk("...and empty output is BLIND too", parse_status("").ok, False)
    chk("live_shards finds the fresh RUNNING one", live_shards(st), ["KLAD"])
    chk("...and does NOT count a stale RUNNING heartbeat",
        live_shards(parse_status(FakeHost(shards={"K": (10, 20, 40000, "RUNNING")})(
            ["status", "h"])[1])), [])

    print("\n── G-R0 HOST KNOWN, both verdicts ──────────────────────────────────────")
    p = plan_cancel("work-server-1", "KLAD", runner=fh, capacity=CAP, hosts=HOSTS)
    chk("⛔ the unqualified mirror name is REFUSED", p.verdict, "REFUSE")
    chk("...naming G-R0", "G-R0" in p.reason, True)
    chk("a host with no capacity row is REFUSED",
        plan_cancel("worker@work-server-9", "KLAD", runner=fh,
                    capacity=CAP, hosts=lambda: ["worker@work-server-9"]).verdict, "REFUSE")
    p = plan_cancel("worker@work-server-1", "KLAD", runner=fh, capacity=CAP, hosts=HOSTS,
                    window=WIN, exempt=EXEMPT)
    chk("...and the dispatchable host PASSES G-R0", p.verdict, "STOP-CYCLE")
    chk("...carrying the allocation, not nproc", p.cores, 10)

    print("\n── G-R1 STATUS READABLE, both verdicts ─────────────────────────────────")
    chk("⛔ a blind status REFUSES",
        plan_cancel("worker@work-server-1", "KLAD", runner=FakeHost(status_blind=True),
                    capacity=CAP, hosts=HOSTS, window=WIN, exempt=EXEMPT).verdict, "REFUSE")
    chk("...and a readable one does not", p.verdict, "STOP-CYCLE")

    print("\n── G-R1b A HUMAN'S STOP IS NOT OVERRIDDEN, both verdicts ───────────────")
    hstop = FakeHost(stop_file=True, shards={"KLAD": (3404, 5400, 12, "RUNNING")})
    ph = plan_cancel("worker@work-server-1", "KLAD", runner=hstop, capacity=CAP,
                     hosts=HOSTS, window=WIN, exempt=EXEMPT)
    chk("⛔ STOP file + a live worker REFUSES (their halt, not ours)", ph.verdict, "REFUSE")
    chk("...naming G-R1b", "G-R1b" in ph.reason, True)
    hstop0 = FakeHost(workers=0, stop_file=True,
                      shards={"KLAD": (3404, 5400, 900, "STOPPED")})
    chk("...while STOP + NO worker still poisons (nothing is started)",
        plan_cancel("worker@work-server-1", "KLAD", runner=hstop0, capacity=CAP,
                    hosts=HOSTS, window=WIN, exempt=EXEMPT).verdict, "SKIP-POISONED")
    chk("...and no STOP file with a live worker proceeds", p.verdict, "STOP-CYCLE")

    print("\n── G-R2 FRESHNESS: BLIND is not stopped, both verdicts ─────────────────")
    stale = FakeHost(shards={"KLAD": (3404, 5400, 4000, "RUNNING")})
    ps = plan_cancel("worker@work-server-1", "KLAD", runner=stale, capacity=CAP,
                     hosts=HOSTS, window=WIN, exempt=EXEMPT)
    chk("⛔ a shard claiming RUNNING on a 4000s heartbeat is REFUSED", ps.verdict, "REFUSE")
    chk("...naming G-R2 and saying BLIND IS NOT STOPPED",
        "G-R2" in ps.reason and "BLIND IS NOT STOPPED" in ps.reason, True)
    chk("...while a 12s heartbeat proceeds", p.verdict, "STOP-CYCLE")

    print("\n── G-R3 ONLY THE RUNNING SHARD IS HALTED, both verdicts ────────────────")
    two = FakeHost(shards={"KLAD": (3404, 5400, 12, "RUNNING"),
                           "OTHER": (900, 5400, 30, "STOPPED")})
    po = plan_cancel("worker@work-server-1", "OTHER", runner=two, capacity=CAP,
                     hosts=HOSTS, window=WIN, exempt=EXEMPT)
    chk("a NOT-running flagged shard is POISONED, never halted", po.verdict, "SKIP-POISONED")
    chk("...and says which shard is actually running", "KLAD" in po.reason, True)
    chk("...while the running one gets the stop cycle",
        plan_cancel("worker@work-server-1", "KLAD", runner=two, capacity=CAP,
                    hosts=HOSTS, window=WIN, exempt=EXEMPT).verdict, "STOP-CYCLE")
    dbl = FakeHost(shards={"A": (1, 2, 5, "RUNNING"), "B": (1, 2, 5, "RUNNING")})
    chk("⛔ TWO live shards (double-subscription) refuses everything",
        plan_cancel("worker@work-server-1", "A", runner=dbl, capacity=CAP,
                    hosts=HOSTS, window=WIN, exempt=EXEMPT).verdict, "REFUSE")

    print("\n── G-R4 CURFEW, both verdicts and both hosts ───────────────────────────")
    chk("curfew window is parsed out of worker.sh itself", curfew_window(), (2055, 400))
    chk("...and the exemption list out of orchestrate.sh", "work-server-2" in
        (no_curfew_hosts() or set()), True)
    chk("ws1 at 22:10 is INSIDE the blackout", in_curfew("worker@work-server-1",
        INSIDE, WIN, EXEMPT)[0], True)
    chk("ws1 at 10:00 is OUTSIDE it", in_curfew("worker@work-server-1",
        OUTSIDE, WIN, EXEMPT)[0], False)
    chk("ws2 is exempt even at 22:10", in_curfew("worker@work-server-2",
        INSIDE, WIN, EXEMPT)[0], False)
    chk("⛔ an unparseable exemption list assumes CURFEW",
        in_curfew("worker@work-server-1", OUTSIDE, WIN, None)[0], True)
    chk("⛔ an unparseable window assumes CURFEW",
        in_curfew("worker@work-server-1", OUTSIDE, None, EXEMPT)[0], True)
    chk("⛔ no host clock assumes CURFEW",
        in_curfew("worker@work-server-1", None, WIN, EXEMPT)[0], True)
    night = FakeHost(utc=INSIDE, shards={"KLAD": (3404, 5400, 12, "RUNNING")})
    chk("a curfewed host REFUSES the cycle",
        plan_cancel("worker@work-server-1", "KLAD", runner=night, capacity=CAP,
                    hosts=HOSTS, window=WIN, exempt=EXEMPT).verdict, "REFUSE")
    chk("...and the exempt host at the same instant does NOT",
        plan_cancel("worker@work-server-2", "KLAD", runner=night, capacity=CAP,
                    hosts=HOSTS, window=WIN, exempt=EXEMPT).verdict, "STOP-CYCLE")

    print("\n── worker already down: poison only, no halt, no start ─────────────────")
    down = FakeHost(workers=0, shards={"KLAD": (3404, 5400, 900, "STOPPED")})
    pd = plan_cancel("worker@work-server-1", "KLAD", runner=down, capacity=CAP,
                     hosts=HOSTS, window=WIN, exempt=EXEMPT)
    chk("an idle host poisons rather than cycles", pd.verdict, "SKIP-POISONED")
    _c, _s = vclock()
    ok, log = run_plan(pd, "test", runner=down, sleep=_s, clock=_c)
    chk("...and it succeeds", ok, True)
    chk("...writing exactly one marker", down.markers, ["KLAD"])
    chk("⛔ ...and NEVER calls stop or start",
        any(c.startswith(("stop", "start")) for c in down.calls), False)

    print("\n── G-R5 HALT VERIFIED, both verdicts ───────────────────────────────────")
    good = FakeHost(shards={"KLAD": (3404, 5400, 12, "RUNNING")}, halt_after=2)
    pg = plan_cancel("worker@work-server-1", "KLAD", runner=good, capacity=CAP,
                     hosts=HOSTS, window=WIN, exempt=EXEMPT)
    _c, _s = vclock()
    ok, good_log = run_plan(pg, "auto_gate TREND-FLOOR@2700", runner=good,
                            sleep=_s, clock=_c, halt_wait_s=300, halt_poll_s=30,
                            up_wait_s=60, up_poll_s=10, hold_dir=NOHOLD)
    log = good_log
    chk("the full cycle succeeds when every step verifies", ok, True)
    chk("...the order is stop -> status* -> cancel -> start -> logs",
        [c.split()[0] for c in good.calls],
        ["status", "stop", "status", "status", "cancel", "start", "logs"])
    chk("...the marker was written", good.markers, ["KLAD"])
    chk("...and the log ends on the ✔ line", log[-1].startswith("✔"), True)
    never = FakeHost(shards={"KLAD": (3404, 5400, 12, "RUNNING")}, halt_after=10 ** 6)
    pn = plan_cancel("worker@work-server-1", "KLAD", runner=never, capacity=CAP,
                     hosts=HOSTS, window=WIN, exempt=EXEMPT)
    _c, _s = vclock()
    ok, log = run_plan(pn, "r", runner=never, sleep=_s, clock=_c,
                       halt_wait_s=90, halt_poll_s=30)
    chk("⛔ a worker that never halts FAILS the cycle", ok, False)
    chk("...writes NO marker", never.markers, [])
    chk("...never starts the host", any(c.startswith("start") for c in never.calls), False)
    chk("...and says the STOP file is left in place",
        "STOP FILE IS LEFT IN PLACE" in log[-1], True)

    print("\n── G-R6 MARKER VERIFIED, both verdicts ─────────────────────────────────")
    nomark = FakeHost(shards={"KLAD": (3404, 5400, 12, "RUNNING")}, halt_after=1,
                      cancel_ok=False)
    pm = plan_cancel("worker@work-server-1", "KLAD", runner=nomark, capacity=CAP,
                     hosts=HOSTS, window=WIN, exempt=EXEMPT)
    _c, _s = vclock()
    ok, log = run_plan(pm, "r", runner=nomark, sleep=_s, clock=_c,
                       halt_wait_s=90, halt_poll_s=30)
    chk("⛔ an unconfirmed marker FAILS", ok, False)
    chk("...and REFUSES to relaunch (which would resume the shard)",
        any(c.startswith("start") for c in nomark.calls), False)
    chk("...while a confirmed marker did relaunch",
        any(c.startswith("start") for c in good.calls), True)

    print("\n── G-R7 RELAUNCH VERIFIED off worker.out, both verdicts ────────────────")
    noup = FakeHost(shards={"KLAD": (3404, 5400, 12, "RUNNING")}, halt_after=1,
                    start_ok=False)
    pu = plan_cancel("worker@work-server-1", "KLAD", runner=noup, capacity=CAP,
                     hosts=HOSTS, window=WIN, exempt=EXEMPT)
    _c, _s = vclock()
    ok, log = run_plan(pu, "r", runner=noup, sleep=_s, clock=_c, halt_wait_s=90,
                       halt_poll_s=30, up_wait_s=30, up_poll_s=10, hold_dir=NOHOLD)
    chk("⛔ no `WORKER up` line => the cycle FAILS", ok, False)
    chk("...the marker still stands (rows kept, shard retired)", noup.markers, ["KLAD"])
    chk("...the host is left STOPPED, loudly", "LEFT STOPPED" in log[-1], True)
    chk("...and the worker's own refusal is quoted", "ENGINE PIN MISMATCH" in log[-1], True)
    chk("...while the verified relaunch NAMED the shard the worker picked up",
        any("NEXTONE" in ln for ln in good_log), True)

    print("\n── G-R8 RELAUNCH HOLD, both verdicts (s48 debt 23) ─────────────────────")
    import tempfile
    hroot = Path(tempfile.mkdtemp(prefix="remote_cancel_hold_"))
    empty_dir = hroot / "empty"
    empty_dir.mkdir()
    set_dir = hroot / "set"
    set_dir.mkdir()
    (set_dir / "worker@work-server-1").write_text(
        "SEALSENT sibling clause fired 07:1x; operator decision pending\n")
    all_dir = hroot / "all"
    all_dir.mkdir()
    (all_dir / HOLD_ALL).write_text("fleet frozen for the wrap\n")
    notdir = hroot / "notadir"
    notdir.write_text("someone made this a FILE\n")

    chk("no hold directory at all           => NOT held",
        relaunch_hold("worker@work-server-1", hroot / "does-not-exist")[0], False)
    chk("an EMPTY hold directory            => NOT held",
        relaunch_hold("worker@work-server-1", empty_dir)[0], False)
    chk("a marker named for THIS host       => HELD",
        relaunch_hold("worker@work-server-1", set_dir)[0], True)
    chk("...and it quotes the operator's own reason",
        "decision pending" in relaunch_hold("worker@work-server-1", set_dir)[1], True)
    # ⛔ THE CELL THAT KEEPS THE MARKER FROM BEING A FLEET-WIDE STOP BY ACCIDENT.
    chk("⛔ a marker for ws1 does NOT hold ws2",
        relaunch_hold("worker@work-server-2", set_dir)[0], False)
    chk(f"a marker named {HOLD_ALL} holds every host",
        (relaunch_hold("worker@work-server-1", all_dir)[0],
         relaunch_hold("worker@work-server-2", all_dir)[0]), (True, True))
    chk("⛔ a hold path that is a FILE, not a directory => BLIND resolves to HELD",
        relaunch_hold("worker@work-server-1", notdir)[0], True)

    # ...and now through the WHOLE cycle, which is where it has to bite.
    held_host = FakeHost(shards={"KLAD": (3404, 5400, 12, "RUNNING")}, halt_after=2)
    ph8 = plan_cancel("worker@work-server-1", "KLAD", runner=held_host, capacity=CAP,
                      hosts=HOSTS, window=WIN, exempt=EXEMPT, hold_dir=set_dir)
    chk("the PLAN still says STOP-CYCLE (the cancel is not gated)", ph8.verdict,
        "STOP-CYCLE")
    chk("...but its reason already announces there will be no relaunch",
        "NO RELAUNCH" in ph8.reason, True)
    _c, _s = vclock()
    ok8, log8 = run_plan(ph8, "auto_gate TREND-FLOOR@2700", runner=held_host, sleep=_s,
                         clock=_c, halt_wait_s=300, halt_poll_s=30, up_wait_s=60,
                         up_poll_s=10, hold_dir=set_dir)
    chk("⛔ HOLD set => the cycle does NOT report success", ok8, False)
    chk("⛔ ...and NEVER calls start",
        any(c.startswith("start") for c in held_host.calls), False)
    chk("...while the shard IS cancelled and its rows kept", held_host.markers, ["KLAD"])
    chk("...the refusal names G-R8 and says the host is left stopped",
        ("G-R8" in log8[-1] and "LEFT STOPPED" in log8[-1].upper()), True)
    chk("...and prints the exact rm + start the operator needs",
        ("rm " in log8[-1] and "orchestrate.sh start" in log8[-1]), True)

    # THE OTHER VERDICT, same fixture, marker the ONLY difference.
    free_host = FakeHost(shards={"KLAD": (3404, 5400, 12, "RUNNING")}, halt_after=2)
    pf8 = plan_cancel("worker@work-server-1", "KLAD", runner=free_host, capacity=CAP,
                      hosts=HOSTS, window=WIN, exempt=EXEMPT, hold_dir=empty_dir)
    _c, _s = vclock()
    okf, logf = run_plan(pf8, "auto_gate TREND-FLOOR@2700", runner=free_host, sleep=_s,
                         clock=_c, halt_wait_s=300, halt_poll_s=30, up_wait_s=60,
                         up_poll_s=10, hold_dir=empty_dir)
    chk("NO hold, identical fixture => the cycle succeeds", okf, True)
    chk("...and DOES relaunch", any(c.startswith("start") for c in free_host.calls), True)
    chk("...picking up the next worklist row",
        any("NEXTONE" in ln for ln in logf), True)

    # ⛔ THE MARKER SET DURING THE HALT WAIT — the actual SEALSENTA window. The
    # plan is made while the directory is clear; the marker appears mid-poll.
    late_dir = hroot / "late"
    late_dir.mkdir()
    late_host = FakeHost(shards={"KLAD": (3404, 5400, 12, "RUNNING")}, halt_after=3)
    pl8 = plan_cancel("worker@work-server-1", "KLAD", runner=late_host, capacity=CAP,
                      hosts=HOSTS, window=WIN, exempt=EXEMPT, hold_dir=late_dir)
    chk("plan made with a CLEAR directory reads clear",
        "NO RELAUNCH" in pl8.reason, False)
    _now = [0.0]

    def _late_sleep(s):
        _now[0] += s
        if _now[0] >= 60:                      # operator sets it mid-halt-poll
            (late_dir / "worker@work-server-1").write_text("hold, decision pending\n")

    okl, logl = run_plan(pl8, "r", runner=late_host, sleep=_late_sleep,
                         clock=lambda: _now[0], halt_wait_s=300, halt_poll_s=30,
                         up_wait_s=60, up_poll_s=10, hold_dir=late_dir)
    chk("⛔ a marker set DURING the halt wait still blocks the relaunch", okl, False)
    chk("...no start was issued", any(c.startswith("start") for c in late_host.calls),
        False)

    print("\n── the transport gates on the FIELD, never on the exit code ────────────")
    chk("a cancel that exits 0 but prints no marker is NOT confirmed",
        _cancel_marker(lambda a, timeout_s=0: (0, "nothing happened\n", ""),
                       "h", "S", "r", False)[0], False)
    chk("...and one that exits nonzero but printed the marker IS",
        _cancel_marker(lambda a, timeout_s=0: (7, "X CANCELLED at 10 rows\n", ""),
                       "h", "S", "r", False)[0], True)

    print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAILED'} "
          f"(G-R0 host known · G-R1 status readable · G-R2 stale-vs-fresh · "
          f"G-R3 running-vs-queued · G-R4 curfew in/out/exempt · G-R5 halt "
          f"verified/timeout · G-R6 marker confirmed/not · G-R7 relaunch "
          f"verified/not · G-R1b a human's STOP is not overridden · G-R8 relaunch "
          f"hold set/clear/other-host/ALL/blind and set-mid-halt — each in BOTH "
          f"directions)")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--host")
    ap.add_argument("--shard")
    ap.add_argument("--reason", default="manual remote_cancel invocation")
    ap.add_argument("--apply", action="store_true",
                    help="actually do it. Default is a DRY-RUN plan.")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.host and a.shard):
        ap.error("--host and --shard are required (or --selftest)")
    ok, verdict, log = cancel_remote_shard(a.host, a.shard, a.reason, apply=a.apply)
    for ln in log:
        print(ln)
    print(f"{'OK' if ok else '⛔ NOT DONE'}  verdict={verdict}  "
          f"mode={'APPLY' if a.apply else 'DRY-RUN'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
