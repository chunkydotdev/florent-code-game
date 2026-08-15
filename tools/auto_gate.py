#!/usr/bin/env python3
"""auto_gate.py — STOP arithmetically-dead shards without waking a human.

Magnus, 2026-08-15, verbatim: *"There needs to be a mechanism that stops shards
at the different marks we've set, then you dont need to wake up and do it
manually, the core can then just pick up the next automatically"*

Today `tools/monitors/gate_watch.sh` WAKES the builder at each mark and the
builder types the decision. This replaces the typing for the DEAD cases only.
It does not replace gate_watch: gate_watch still wakes for everything that is
NOT arithmetically dead, and that is the majority of crossings. Run both.

═══════════════════════════════════════════════════════════════════════════════
THE STOPPING RULE — PINNED BY MAGNUS, NOT SUBSTITUTABLE
═══════════════════════════════════════════════════════════════════════════════
    n < 400                 -> NEVER stop. Too early for any rule.
    n >= 400   CATASTROPHE  -> STOP if the 95% CI UPPER bound < 45.0%
    n >= 1000  at each mark -> STOP if the 95% CI UPPER bound < the shard's BAR
    otherwise               -> CONTINUE

⛔ NEVER STOP ON "UNRESOLVED". A CI that straddles the bar CONTINUES.
Research measured that an `UNRESOLVED => DROP` gate kills ~82% of arms whose
TRUE effect is +1.5pp, against 85.3% survival under the point rule. An
auto-stopper on the wrong rule destroys real effects at machine speed, which is
precisely the risk of automating this at all. The rule above stops an arm only
when the OPTIMISTIC edge of its own data cannot reach its bar — futility by
EXCLUSION, never by failure-to-resolve.

INTERVAL: 1.96*sqrt(p(1-p)/n), NAIVE. Local fixtures measure pair-weighted
DEFF 0.98 (s39 audit, 124 shards), so naive is correct and marginally
conservative here. ⛔ Do NOT apply the platform DEFF constants (1.529 rated /
1.833 unrated) to local shards: that widens intervals 24-35% for correlation
that is not there, and a wider interval makes this stopper stop LESS — the
flattering direction, which is the one an automated killer must never drift in.

═══════════════════════════════════════════════════════════════════════════════
RELATIONSHIP TO THE REGISTERED MANUAL GATES (read this before changing either)
═══════════════════════════════════════════════════════════════════════════════
`docs/prereg/RULE-futility-gates-2026-08-13.md` registers POINT-estimate gates:
GATE-1000 drops if share < 48.0; GATE-2700 drops if share <= 50.5. This tool's
rule is a DIFFERENT, CI-based rule, and the two do not nest cleanly:

  * At n=2700 with BAR 51.33 this tool stops only below ~49.4% — STRICTLY MORE
    CONSERVATIVE than the registered 50.5 point gate. Everything it stops there,
    a human applying the registered rule would also have stopped.
  * ⚠ At n=1000 with BAR 51.33 this tool stops below ~48.23%, which is LOOSER
    than the registered 48.0 point gate in the window [48.00, 48.23). An arm at
    48.1% is auto-stopped here and would have SURVIVED the registered gate.
    That window is 0.23pp wide and it is a real divergence, disclosed rather
    than smoothed. It exists because Magnus pinned the CI rule directly.

⇒ This tool never claims to implement RULE-futility-gates. It implements the
  rule pinned in its own header, and the marks come from gate_watch.

═══════════════════════════════════════════════════════════════════════════════
GUARDS (each one is driven to BOTH verdicts by --selftest)
═══════════════════════════════════════════════════════════════════════════════
G1 NO BAR, NO STOP      — a shard with no registered bar is never stopped by
                          the bar rule. Only CATASTROPHE, which needs no bar,
                          may apply to it.
G2 NEVER BELOW n=400    — no rule reaches a shard under 400 rows, ever.
G3 BLIND IS NOT DEAD    — an unreadable or STALE tape means DO NOTHING. Every
                          printed line carries the tape's age and its source, so
                          a healthy line and a blind line are never byte-identical.
G4 STOP ONCE            — a shard already cancelled is never re-cancelled, and
                          the cancellation is recorded in this tool's own ledger
                          BEFORE the action, so a restart cannot double-write
                          the results tape.
G5 NEVER STOP A NULL    — a byte-identical A/A pair is detected STRUCTURALLY by
                          comparing the two trees (the same md5 rule
                          `orchestrate.sh gen` and `overnight_read.py` use), NOT
                          by name. A naming convention rots; an md5 does not. A
                          null exists to sit at 50% and must run to completion.
G6 ABLATION CARVE-OUT   — a shard registered with direction `le` is never
                          auto-stopped at all, catastrophe included. See
                          docs/prereg/BARS.tsv for why.

═══════════════════════════════════════════════════════════════════════════════
HOW IT STOPS
═══════════════════════════════════════════════════════════════════════════════
LOCAL : `touch scratchpad/corefill_cancel/<SHARD>`. That is corefill.sh's own
        documented CANCEL interface (corefill.sh:50-58, :113-123): the shard is
        killed at the next poll, its rows are KEPT, its `.started` marker gets a
        `cancelled <ts>` line, and the SAME loop iteration goes on to launch the
        next unstarted worklist item. "The core picks up the next automatically"
        is already true — this only supplies the touch.
        ⛔ REQUIRES A LIVE REAPER. If no `corefill.sh` process is running, the
        cancel file has nobody to act on it AND nothing will launch the next
        item. We REFUSE to apply in that case rather than leave a dud flag.
REMOTE: ⛔ REPORT ONLY. THERE IS NO PER-SHARD CANCEL PRIMITIVE ON A WORKER.
        `orchestrate.sh` offers `stop` (writes a global STOP file — worker.sh
        run_shard returns 10 and the shard loop BREAKS, halting the whole host,
        not advancing to the next shard) and `kill` (whole worker). `stop` is
        additionally a NO-OP during curfew, because worker.sh calls
        curfew_wait() BEFORE its STOP test. And `stop` + `start` is worse than
        either: cmd_start does `rm -f STOP`, so a sleeping worker wakes into a
        world with no STOP file and double-subscribes the box, which silently
        corrupts every row both workers produce (`--tle 10` is wall-clock).
        ⇒ We print the decision and the exact manual sequence. We never execute
        it. Inventing a compound remote cancel is exactly the "do not invent a
        second mechanism" failure.

ROWS ARE ALWAYS KEPT. Nothing here deletes data. A stopped shard is readable and
under-powered; `tools/overnight_read.py` already pools partial shards and prints
the shortfall.

═══════════════════════════════════════════════════════════════════════════════
EVERY STOP WRITES A results.tsv ROW TYPED `cancellation`, NEVER `verdict`
═══════════════════════════════════════════════════════════════════════════════
Established 2026-08-15 by the SEALQ disclosure (results.tsv `sealq-STOP-
DISCLOSURE`): OPERATIONAL CANCELLATION AND VERDICT ARE DIFFERENT OBJECTS.
Killing a losing arm to free a core is obviously right and needs no defence;
TYPING it as a verdict is what imports the optional-stopping question. Precedent
to imitate: SEALFLOOR6 went out as FUTILITY-ALONE.

USAGE
    tools/auto_gate.py                 # --dry-run is the DEFAULT. Changes nothing.
    tools/auto_gate.py --apply         # actually cancel (local shards only)
    tools/auto_gate.py --selftest      # synthetic fixtures, every guard both ways
"""

from __future__ import annotations

import argparse
import calendar
import math
import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

# The structural null test. Imported, never re-implemented: a second copy is the
# one nobody tests (D24(e)), and this predicate decides whether we may kill a
# calibration cell.
from overnight_read import trees_identical  # noqa: E402

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

# ─────────────────────────────────────────────────────────────────────────────
# THE MARKS. ⛔ ONE SET, AND IT IS gate_watch's.
# Read off tools/monitors/gate_watch.sh:64-81 — the elif chain there tests
# n >= target (FINAL), n >= 2700, n >= 1000, n >= 400 (catastrophe), in that
# order, so the effective mark is the HIGHEST boundary crossed. Replicated here
# because parsing a shell elif chain is more fragile than duplicating four
# integers — but the duplicate is checked: marks_agree_with_gate_watch() greps
# that file for these literals and ALARMS if any is missing, so drift is caught
# rather than assumed away.
# ─────────────────────────────────────────────────────────────────────────────
MARK_CATASTROPHE = 400
MARK_MID = 1000
MARK_HALF = 2700
CATASTROPHE_CI_HI = 45.0  # pinned by Magnus

# THE TREND FLOOR. Pinned by Magnus 2026-08-15, verbatim: "the share needs to be
# above 51% at 1000 and at 2700 n otherwise it's no use to us, more than to maybe
# test combinations with." Checked against the PREFIX share at each mark, so the
# rule looks exactly twice however often this tool runs (see Tape.wins_at_mid).
TREND_FLOOR = 51.0
Z95 = 1.96                # pinned: naive normal interval, DEFF 0.98 => no inflation

DEFAULT_WORKLIST = REPO / "scratchpad/corefill_work.txt"
DEFAULT_TSVDIR = REPO / "scratchpad/overnight"
DEFAULT_REMOTE_ROOT = REPO / "scratchpad/overnight-remote"
DEFAULT_BARS = REPO / "docs/prereg/BARS.tsv"
DEFAULT_CANCEL_DIR = REPO / "scratchpad/corefill_cancel"
DEFAULT_STARTED_DIR = REPO / "scratchpad/corefill_started"
DEFAULT_LEDGER = REPO / "scratchpad/auto_gate_cancelled.tsv"
DEFAULT_RESULTS = REPO / "results.tsv"
DEFAULT_STALE_S = 900  # 15 min. A live local shard writes rows continuously; a
                       # remote worker stamps its heartbeat every batch.

RUNNER_PAT = r"[o]vernight[a-z0-9_]*\.sh"   # tools/lib/runner_pat.sh — one definition
REAPER_PAT = r"[c]orefill\.sh"


# ═════════════════════════════════════════════════════════════════════════════
# ARITHMETIC
# ═════════════════════════════════════════════════════════════════════════════
def ci95(wins: int, n: int) -> tuple[float, float, float]:
    """Naive 95% interval on the share, in PERCENTAGE POINTS.

    1.96*sqrt(p(1-p)/n). No design effect: local fixtures measure pair-weighted
    DEFF 0.98 (s39, 124 shards), so naive is correct and marginally
    conservative. Widening here would make the stopper stop LESS, which is the
    flattering direction for an automated killer.
    """
    if n <= 0:
        raise ValueError("ci95 needs n > 0")
    p = wins / n
    half = Z95 * math.sqrt(p * (1.0 - p) / n)
    return (100.0 * p, 100.0 * max(0.0, p - half), 100.0 * min(1.0, p + half))


def mark_for(n: int, target: int) -> str:
    """The HIGHEST mark this row count has crossed. Mirrors gate_watch's elif order."""
    if target and n >= target:
        return "FINAL"
    if n >= MARK_HALF:
        return "2700"
    if n >= MARK_MID:
        return "1000"
    if n >= MARK_CATASTROPHE:
        return "400"
    return "PRE-400"


# ═════════════════════════════════════════════════════════════════════════════
# INPUTS
# ═════════════════════════════════════════════════════════════════════════════
@dataclass
class Bar:
    value: float
    direction: str  # "ge" | "le"
    source: str


def load_bars(path: Path) -> dict[str, Bar]:
    bars: dict[str, Bar] = {}
    if not path.is_file():
        return bars
    for line in path.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        f = line.split("\t")
        if len(f) < 3:
            continue
        shard, val, direction = f[0].strip(), f[1].strip(), f[2].strip().lower()
        if direction not in ("ge", "le"):
            continue
        try:
            v = float(val)
        except ValueError:
            continue
        # ⛔⛔ PLAUSIBILITY BOUND ON THE BAR ITSELF. Added s44 the moment --apply
        # was armed, because that is when BARS.tsv became a DESTRUCTIVE input:
        # under --dry-run a wrong bar produced a wrong REPORT; under --apply it
        # cancels shards, once each, autonomously, every ten minutes.
        # Every other guard in this tool protects the SHARD FROM THE RULE. None of
        # them protects the shard from a WRONG BAR — a malformed row is dropped,
        # but a well-formed wrong NUMBER passes G1..G5 untouched, because nothing
        # here can know what the bar should be.
        # This does not make a bar correct. It rejects the class a typo produces:
        # a bar outside [30, 70] is not a game-share bar on this fixture (our
        # whole measured range today is 25.5-54.9), so it is a slipped decimal or
        # a percent/fraction mixup, and acting on it would cancel arms wholesale.
        # A citation is the real control and it is a human reading the file; this
        # is the cheap arithmetic backstop for when the registry grows past the
        # five hand-cited rows it has today.
        if not (30.0 <= v <= 70.0):
            print(f"⛔ BARS.tsv: refusing bar {v} for {shard} — outside the "
                  f"plausible [30,70] band. A typo'd bar under --apply cancels "
                  f"real arms. Fix the row or state why it is right.", file=sys.stderr)
            continue
        bars[shard] = Bar(v, direction, f[3].strip() if len(f) > 3 else "?")
    return bars


@dataclass
class Tape:
    """A shard TSV, read. `ok=False` means BLIND — never means dead."""
    ok: bool
    n: int = 0
    wins: int = 0
    mtime: float = 0.0
    why: str = ""
    # PREFIX wins at exactly the first MARK_MID / MARK_HALF rows. These exist so
    # the trend rule looks EXACTLY TWICE regardless of how often this tool runs.
    # ⛔ Using the CURRENT share instead would make the rule re-evaluate on every
    # 10-minute tick from n=1000 to n=5400 — ~400 looks at a random walk that
    # crosses 51% constantly. That is optional stopping, and it would kill true
    # winners at many times the rate the two-look design was priced at.
    # A prefix is deterministic and idempotent: same tape, same verdict, forever.
    # ⛔ DEFAULT None, NOT 0 — and the selftest is what forced this. A Tape built
    # any way other than read_tape() (a fixture, a future caller) would carry 0
    # here, and 0 wins over 1000 games reads as 0.00% — BELOW ANY FLOOR, so every
    # such shard would be STOPPED. That is a default that fails in the KILLING
    # direction, the one this file's docstring says an automated canceller must
    # never drift in. None means BLIND, and blind never stops.
    wins_at_mid: int | None = None
    wins_at_half: int | None = None


def read_tape(path: Path) -> Tape:
    """Count rows and treatment wins.

    ⛔ ROW COUNT IS `lines-not-starting-with-#` MINUS THE HEADER, not `wc -l - 1`.
    overnight.sh writes a `# FIXTURE` comment line ABOVE the column header
    (overnight.sh:100), so `wc -l - 1` overcounts every LOCAL tape by exactly 1.
    gate_watch.sh:56 does exactly that and is off by one on every local shard.
    Verified against the heartbeat, which the runner computes with
    `grep -vc '^#'`: BODYAWR heartbeat said 10753 where `wc -l - 1` said 10754.
    Remote tapes (worker.sh) have no FIXTURE line, so the same code is correct
    for both without a branch.
    """
    try:
        raw = path.read_bytes().decode("utf-8", "replace")
        mtime = path.stat().st_mtime
    except OSError as e:
        return Tape(False, why=f"unreadable: {e.__class__.__name__}")
    lines = [ln for ln in raw.splitlines() if ln and not ln.startswith("#")]
    if not lines:
        return Tape(False, why="empty tape (no non-comment lines)")
    if not lines[0].startswith("ts\t"):
        # An unparseable tape is BLIND, not a shard at n=0. Refusing here is what
        # stops a schema change from reading as a catastrophic arm.
        return Tape(False, why="first non-comment line is not the 'ts\\t...' header")
    n, wins = 0, 0
    w_mid, w_half = None, None
    for ln in lines[1:]:
        f = ln.split("\t")
        if len(f) < 7:
            continue
        n += 1
        if f[6] == "T":
            wins += 1
        if n == MARK_MID:
            w_mid = wins
        if n == MARK_HALF:
            w_half = wins
    if n <= 0:
        return Tape(False, mtime=mtime, why="header only, zero data rows")
    return Tape(True, n=n, wins=wins, mtime=mtime,
                wins_at_mid=w_mid, wins_at_half=w_half)


@dataclass
class Shard:
    id: str
    surface: str          # "local" | "remote"
    host: str             # "" for local
    tsv: Path
    treat: str
    ctrl: str
    target: int
    tape: Tape
    age_s: float          # freshness of the SHARD'S OWN PROGRESS, not of our copy
    age_src: str          # what the age was measured from
    live: bool
    status: str = ""      # remote heartbeat status, or local process state
    notes: list[str] = field(default_factory=list)


def _procs() -> str | None:
    try:
        out = subprocess.run(["ps", "ax", "-o", "command="],
                             capture_output=True, text=True, timeout=20)
    except Exception:
        return None
    if out.returncode != 0 and not out.stdout:
        return None
    return out.stdout


def running_shards(ps_out: str | None) -> set[str] | None:
    """Shard ids with a live runner. None means BLIND (ps unreadable).

    corefill.sh guard 2: `ps` failing means BLIND, not IDLE. Same rule here, and
    it fails toward doing nothing.
    """
    if ps_out is None:
        return None
    pat = re.compile(RUNNER_PAT + r"\s+(\S+)")
    return {m.group(1) for m in pat.finditer(ps_out)}


def reaper_alive(ps_out: str | None) -> bool | None:
    if ps_out is None:
        return None
    return re.search(REAPER_PAT, ps_out) is not None


def parse_worklist(path: Path) -> dict[str, tuple[str, str, int, int]]:
    spec: dict[str, tuple[str, str, int, int]] = {}
    if not path.is_file():
        return spec
    for line in path.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        f = s.split()
        if len(f) < 5:
            continue
        try:
            spec[f[0]] = (f[1], f[2], int(f[3]), int(f[4]))
        except ValueError:
            continue
    return spec


def scan_local(worklist: Path, tsvdir: Path, ps_out: str | None, now: float) -> list[Shard]:
    spec = parse_worklist(worklist)
    live = running_shards(ps_out)
    out: list[Shard] = []
    for sid, (tr, ct, target, _seed) in spec.items():
        tsv = tsvdir / f"{sid}.tsv"
        if not tsv.exists():
            continue
        tape = read_tape(tsv)
        try:
            mt = tsv.stat().st_mtime
        except OSError:
            mt = 0.0
        is_live = (sid in live) if live is not None else False
        notes = []
        if live is None:
            notes.append("ps unreadable -> liveness BLIND, treated as not-live")
        out.append(Shard(sid, "local", "", tsv, tr, ct, target, tape,
                         now - mt if mt else float("inf"), "tsv mtime",
                         is_live, "RUNNER" if is_live else "no runner", notes))
    return out


def _read_heartbeat(hb: Path) -> tuple[float | None, str]:
    """(epoch of the WORKER'S OWN stamp, status). Not our pull time.

    ⛔ THE PULL MTIME IS THE WRONG CLOCK for a remote shard: rsync refreshes it
    even when the worker has been frozen for an hour. worker.sh stamps its own
    UTC into field 1 and its state into field 5 — that is the clock that can
    tell a working host from a dead one, and CURFEW from either (worker.sh
    documents SALTREF2 freezing at a curfew boundary with a heartbeat still
    reading RUNNING, where a dead worker and a sleeping worker were
    byte-identical in CONTENT and only the mtime discriminated).
    """
    try:
        f = hb.read_text().strip().split("\t")
    except OSError:
        return None, "?"
    if len(f) < 5:
        return None, "?"
    # ⛔ calendar.timegm, NOT time.mktime()-time.timezone. The first cut used
    # mktime minus time.timezone and read every remote heartbeat as EXACTLY ONE
    # HOUR STALE — `time.timezone` is the NON-DST offset (CET, -3600) while this
    # box is on CEST (-7200) in August, so mktime's DST guess and the constant
    # disagreed by 3600s. Live consequence, observed before the fix: LNCHRND1's
    # heartbeat stamped 09:44:14Z was reported as age 3832s against a 900s stale
    # threshold, i.e. a HEALTHY remote shard was declared BLIND. An off-by-an-hour
    # clock in a freshness guard fails toward silence, which is the direction that
    # looks safe and is not: the shard it blinds is the one nobody then looks at.
    # timegm treats the struct as UTC by construction — no DST term exists.
    try:
        epoch = calendar.timegm(time.strptime(f[0], "%Y-%m-%dT%H:%M:%SZ"))
    except ValueError:
        epoch = None
    return epoch, f[4].strip()


def scan_remote(remote_root: Path, now: float) -> list[Shard]:
    found: dict[str, Shard] = {}
    if not remote_root.is_dir():
        return []
    for hostdir in sorted(p for p in remote_root.iterdir() if p.is_dir()):
        spec = parse_worklist(hostdir / "worklist.txt")
        for tsv in sorted(hostdir.glob("*.tsv")):
            sid = tsv.stem
            tr, ct, target, _ = spec.get(sid, ("", "", 0, 0))
            tape = read_tape(tsv)
            hb_epoch, status = _read_heartbeat(hostdir / f"{sid}.heartbeat")
            complete = (hostdir / f"{sid}.COMPLETE").exists()
            if hb_epoch is not None:
                age, src = now - hb_epoch, "remote heartbeat stamp"
            else:
                try:
                    age, src = now - tsv.stat().st_mtime, "pull mtime (NO heartbeat)"
                except OSError:
                    age, src = float("inf"), "no clock at all"
            is_live = (status == "RUNNING") and not complete
            sh = Shard(sid, "remote", hostdir.name, tsv, tr, ct, target, tape,
                       age, src, is_live, status or "?")
            if not spec:
                sh.notes.append("no worklist.txt on this pull -> trees unknown")
            prev = found.get(sid)
            # Same host is pulled under two keys (work-server-1 and
            # worker@work-server-1). Keep the FRESHEST and say so, rather than
            # reporting one shard twice and inviting a double decision.
            if prev is None or sh.age_s < prev.age_s:
                if prev is not None:
                    sh.notes.append(f"duplicate pull of this shard also at {prev.host} "
                                    f"(age {prev.age_s:.0f}s) — freshest kept")
                found[sid] = sh
            else:
                prev.notes.append(f"duplicate pull at {sh.host} (age {sh.age_s:.0f}s) — ignored")
    return list(found.values())


# ═════════════════════════════════════════════════════════════════════════════
# THE LEDGER — guard 4
# ═════════════════════════════════════════════════════════════════════════════
def ledger_claimed(ledger: Path) -> set[str]:
    if not ledger.is_file():
        return set()
    out = set()
    for line in ledger.read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        f = line.split("\t")
        if len(f) >= 2:
            out.add(f[1])
    return out


def already_cancelled(sid: str, ledger: Path, started_dir: Path,
                      cancel_dir: Path, results: Path) -> str | None:
    """Four independent reasons a shard must not be cancelled again.

    Independent on purpose: this tool's own ledger can be deleted, corefill's
    marker can be rotated, and a human cancel leaves no ledger row at all. Any
    one of them firing is enough.
    """
    if sid in ledger_claimed(ledger):
        return "this tool's ledger already claims it"
    m = started_dir / sid
    if m.is_file():
        try:
            if "cancelled" in m.read_text():
                return f"corefill marker {m.name} already reads 'cancelled'"
        except OSError:
            pass
    if (cancel_dir / sid).exists():
        return "a cancel flag is already pending for it"
    if results.is_file():
        try:
            pref = f"{sid.lower()}-autostop-"
            for line in results.read_text(errors="replace").splitlines():
                if line.lower().startswith(pref):
                    return "results.tsv already carries an autostop row for it"
        except OSError:
            pass
    return None


# ═════════════════════════════════════════════════════════════════════════════
# THE DECISION
# ═════════════════════════════════════════════════════════════════════════════
@dataclass
class Decision:
    action: str    # "STOP" | "CONTINUE" | "NOACTION"
    clause: str
    detail: str
    mark: str = ""
    share: float = 0.0
    lo: float = 0.0
    hi: float = 0.0
    bar: Bar | None = None
    computed: bool = False   # were share/lo/hi actually derived? A blind line must
                             # never print a 0.00% that looks like a measurement.


def decide(sh: Shard, bars: dict[str, Bar], stale_s: float,
           cancelled_reason: str | None = None) -> Decision:
    """The whole rule, in the order the guards must fire.

    ORDER IS LOAD-BEARING.
      * NOT-LIVE is first: a shard with no runner has nothing to stop, so no
        other question about it needs answering (and the archive holds ~140 of
        them — evaluating those is noise, not safety).
      * G3 (blind) comes next, because an unread tape cannot support any
        verdict and everything below this line reads numbers off it.
      * G5 (null) and G6 (ablation) precede the catastrophe clause because
        catastrophe needs no bar and would otherwise kill exactly the two cell
        types that are SUPPOSED to sit away from the bar.
    """
    if not sh.live:
        return Decision("NOACTION", "NOT-LIVE",
                        f"no live runner (status={sh.status}) — nothing to stop")

    # ---- G3: BLIND IS NOT DEAD ---------------------------------------------
    if not sh.tape.ok:
        return Decision("NOACTION", "BLIND-UNREADABLE",
                        f"tape not readable ({sh.tape.why}) — an unreadable shard is "
                        f"BLIND, not dead; no rule may fire on it")
    if sh.age_s > stale_s:
        return Decision("NOACTION", "BLIND-STALE",
                        f"⚠ LIVE RUNNER BUT THE TAPE IS {sh.age_s:.0f}s OLD (> {stale_s:.0f}s), "
                        f"measured from {sh.age_src} — refusing to decide off a stale "
                        f"surface. This is BLIND, not dead, and it wants a human eye.")

    share, lo, hi = ci95(sh.tape.wins, sh.tape.n)
    mark = mark_for(sh.tape.n, sh.target)
    bar = bars.get(sh.id)

    def d(action, clause, detail):
        return Decision(action, clause, detail, mark, share, lo, hi, bar, True)

    if mark == "FINAL":
        return d("NOACTION", "AT-TARGET",
                 f"n={sh.tape.n} >= target {sh.target}; the shard is finishing, "
                 f"there is nothing left to free")
    if cancelled_reason:
        return d("NOACTION", "ALREADY-STOPPED", cancelled_reason)

    # ---- G5: NEVER STOP A NULL / CALIBRATION CELL --------------------------
    if sh.treat and sh.ctrl and trees_identical(str(REPO / sh.treat) if not
                                                os.path.isabs(sh.treat) else sh.treat,
                                                str(REPO / sh.ctrl) if not
                                                os.path.isabs(sh.ctrl) else sh.ctrl):
        return d("CONTINUE", "NULL-CELL",
                 f"treatment tree is BYTE-IDENTICAL to control ({sh.treat} == {sh.ctrl}) "
                 f"— a null exists to sit at 50% and must run to completion. "
                 f"Detected structurally by md5, never by name.")

    # ---- G6: ABLATION CARVE-OUT --------------------------------------------
    if bar is not None and bar.direction == "le":
        return d("CONTINUE", "ABLATION-INVERTED",
                 f"registered with an INVERTED bar (<= {bar.value:.2f}, {bar.source}): a low "
                 f"share is this arm's hypothesis SUCCEEDING. Auto-stop is disabled for it "
                 f"entirely, catastrophe included.")

    # ---- G2: NEVER BELOW n=400 ---------------------------------------------
    if sh.tape.n < MARK_CATASTROPHE:
        return d("CONTINUE", "PRE-400",
                 f"n={sh.tape.n} < {MARK_CATASTROPHE}; too early for any rule")

    # ---- CATASTROPHE (needs no bar) ----------------------------------------
    if hi < CATASTROPHE_CI_HI:
        return d("STOP", "CATASTROPHE",
                 f"n>={MARK_CATASTROPHE} and the 95% CI UPPER bound {hi:.2f} < "
                 f"{CATASTROPHE_CI_HI:.1f} — the optimistic edge of its own data is "
                 f"still catastrophic")

    # ---- TREND FLOOR — the primary stop rule (Magnus, 2026-08-15) -----------
    # "the share needs to be above 51% at 1000 and at 2700 n otherwise it's no
    # use to us, more than to maybe test combinations with."
    #
    # ⭐ THIS SUPERSEDES THE CI-BASED FUTILITY RULE BELOW AS THE PRIMARY GATE,
    # and it is a DIFFERENT QUESTION. Futility-by-exclusion asked "can this arm
    # still REACH the bar?" and so protected anything unresolved. The trend
    # floor asks "is this arm WORTH THE COMPUTE?" — an arm reading 50.5% is
    # unresolved AND uninteresting, and we were paying full price for its
    # precision. Priced before adoption, false-drop of a TRUE effect:
    #     +1.33pp (at bar) 63.0%   +2pp 37.3%   +3pp 11.9%
    #     +4pp 2.9%        +5pp 0.6%            +7pp 0.0%
    # Tuned for the hunt actually underway (a 65% shard is +15pp: survives with
    # certainty). What it kills hard is the at-the-bar class, which is the class
    # the directive above declares uninteresting.
    #
    # ⛔ WHY DROPPING AN ARM HERE LOSES NO INFORMATION, which is the whole
    # reason the rate above is affordable: CANCELLING KEEPS THE ROWS. A shard
    # stopped at 2700 still has a 2,700-game screen on the tape — ample to pick
    # it for a COMBINATION arm. We stop buying precision on an arm we would not
    # ship alone; we do not stop knowing what it measured.
    #
    # ⭐ AND IT NEEDS NO REGISTERED BAR — deliberately. The side lane's
    # 2026-08-15 objection was that BARS.tsv coverage is a PRACTICE, not a
    # MECHANISM (grep: no queueing path writes a bar row; coverage 202/206 and
    # decaying with attention). Under the old design an unregistered arm got NO
    # RULE AT ALL, so the coverage gap was also an enforcement gap. Under this
    # one an unregistered arm gets the SAFE HOUSE DEFAULT, and the registry
    # shrinks to carrying only EXCEPTIONS — a set small enough to audit by eye.
    if sh.tape.n >= MARK_MID:
        src = "registered" if bar is not None else "DEFAULT (no bar row)"
        for mk, w in ((MARK_MID, sh.tape.wins_at_mid),
                      (MARK_HALF, sh.tape.wins_at_half)):
            if sh.tape.n < mk or w is None:
                continue  # w is None => prefix unknown => BLIND => never stop
            pfx = 100.0 * w / mk
            if pfx < TREND_FLOOR:
                return d("STOP", f"TREND-FLOOR@{mk}",
                         f"share over the FIRST {mk} games was {pfx:.2f}% < the "
                         f"{TREND_FLOOR:.1f}% house floor [{src}] — not futile, "
                         f"but not worth further compute on its own. Rows are "
                         f"KEPT: it remains available as a combination input.")

    # ---- G1: NO BAR, NO STOP (the CI rule only) -----------------------------
    if bar is None:
        return d("CONTINUE", "NO-BAR-REGISTERED",
                 f"cleared the {TREND_FLOOR:.1f}% trend floor; no row in the bar "
                 f"registry, so the CI bar rule cannot also be applied. Register "
                 f"it in docs/prereg/BARS.tsv with a prereg citation.")

    if mark in ("1000", "2700"):
        # ⛔⛔ MARGIN ADDED s44 AFTER THE RULE STOPPED A SHARD ON 0.0087pp.
        # SPAWNLKL was cancelled at n=3646 with CI upper 51.3213 against a bar of
        # 51.3300 — a margin of ONE HUNDREDTH OF A POINT, which ONE GAME would have
        # flipped. A futility stop decided by one game out of 3,646 is not futility,
        # it is noise wearing futility's clothes, and this repo has already banked
        # two knife-edge readings today (0.02pp, 0.10pp) that had to disclaim
        # themselves as coin flips. An AUTOMATED canceller making that call every
        # ten minutes across ~180 registered arms would do it repeatedly and
        # silently, and each time it would free a core by discarding an arm that
        # was merely unresolved.
        # The margin is HALF A HALF-WIDTH: the bar must be excluded by a
        # meaningful fraction of the interval's own scale, not by a rounding
        # artefact. At n=5400 that is ~0.67pp. Scale-free, so it stays correct at
        # every n rather than being a magic constant.
        margin = 0.5 * (hi - lo) / 2.0
        if hi < bar.value - margin:
            return d("STOP", f"FUTILITY-BAR@{mark}",
                     f"95% CI UPPER bound {hi:.2f} < BAR {bar.value:.2f} - margin "
                     f"{margin:.2f} ({bar.source}) — the OPTIMISTIC edge of its own "
                     f"data cannot reach the bar, by more than half a half-width. "
                     f"Futility by EXCLUSION, not by failure-to-resolve.")
        if hi < bar.value:
            return d("CONTINUE", f"WITHIN-MARGIN@{mark}",
                     f"CI upper {hi:.2f} is below BAR {bar.value:.2f} but by only "
                     f"{bar.value - hi:.3f}pp, inside the {margin:.2f}pp margin — "
                     f"a stop this close is decided by noise, not by futility. "
                     f"CONTINUING deliberately.")
        return d("CONTINUE", f"NOT-EXCLUDED@{mark}",
                 f"95% CI [{lo:.2f},{hi:.2f}] upper bound {hi:.2f} >= BAR {bar.value:.2f} — "
                 f"the interval still reaches the bar. UNRESOLVED CONTINUES.")

    return d("CONTINUE", "BETWEEN-MARKS",
             f"n={sh.tape.n} is past {MARK_CATASTROPHE} but short of {MARK_MID}; only the "
             f"catastrophe rule applies here and it did not fire")


# ═════════════════════════════════════════════════════════════════════════════
# THE ACTION
# ═════════════════════════════════════════════════════════════════════════════
def _rel(p: Path) -> str:
    """Repo-relative if it is under the repo, absolute otherwise. Never raises."""
    try:
        return str(Path(p).resolve().relative_to(REPO))
    except (ValueError, OSError):
        return str(p)


def results_row(sh: Shard, dec: Decision, ts: str) -> str:
    barstr = (f"{dec.bar.value:.2f} ({dec.bar.direction}, {dec.bar.source})"
              if dec.bar else "NONE — catastrophe rule needs no bar")
    desc = (
        f"AUTO-STOP {sh.id} at MARK-{dec.mark} n={sh.tape.n} on {ts} by tools/auto_gate.py "
        f"--apply. SHARE {dec.share:.2f}% [{dec.lo:.2f},{dec.hi:.2f}] (95%, naive "
        f"1.96*sqrt(p(1-p)/n), DEFF 0.98 local so no inflation). BAR: {barstr}. "
        f"RULE CLAUSE FIRED: {dec.clause} — {dec.detail} "
        f"⛔ THIS IS NOT A VERDICT AND MUST NOT BE READ AS ONE. It is an OPERATIONAL "
        f"CANCELLATION to free a core, typed `cancellation` per the SEALQ disclosure "
        f"(operational cancellation and verdict are different objects; killing a losing "
        f"arm needs no defence, TYPING it as a verdict imports the optional-stopping "
        f"question). Precedent: SEALFLOOR6 went out as FUTILITY-ALONE. "
        f"ROWS ARE KEPT at {_rel(sh.tsv)} "
        f"and remain readable; overnight_read.py pools partial shards and prints the "
        f"shortfall. Registered target was n={sh.target}, so this arm is UNDER-POWERED "
        f"by construction — no exclusion claim is licensed by it. Stopped by rule, not "
        f"by operator discretion: the rule is pinned in tools/auto_gate.py's header."
    )
    return "\t".join([f"{sh.id.lower()}-autostop-{dec.mark.lower()}",
                      f"{dec.share / 100:.4f}", f"{dec.lo / 100:.4f}",
                      f"{dec.hi / 100:.4f}", str(sh.tape.n), "cancellation", desc])


def apply_stop(sh: Shard, dec: Decision, *, cancel_dir: Path, ledger: Path,
               results: Path, ts: str) -> tuple[bool, str]:
    """Local stop. Ledger BEFORE the action, deliberately.

    If we crash between the claim and the touch, the shard keeps running and a
    human handles it exactly as today. If we crashed the other way round we
    could double-write the shared results tape. Fail toward not-stopping.
    """
    if sh.surface != "local":
        return False, ("REMOTE — no per-shard cancel primitive exists on a worker; "
                       "reported only, never executed")
    try:
        cancel_dir.mkdir(parents=True, exist_ok=True)
        ledger.parent.mkdir(parents=True, exist_ok=True)
        if not ledger.exists():
            ledger.write_text("#ts\tshard\tphase\tmark\tn\tshare\tci_lo\tci_hi\tclause\n")
        with ledger.open("a") as fh:
            fh.write("\t".join([ts, sh.id, "CLAIM", dec.mark, str(sh.tape.n),
                                f"{dec.share:.2f}", f"{dec.lo:.2f}", f"{dec.hi:.2f}",
                                dec.clause]) + "\n")
        (cancel_dir / sh.id).write_text(
            f"auto_gate {ts} {dec.clause} n={sh.tape.n} share={dec.share:.2f} "
            f"ci=[{dec.lo:.2f},{dec.hi:.2f}]\n")
        # Gate on the LOAD-BEARING FILE, never on a return code.
        if not (cancel_dir / sh.id).exists():
            return False, "cancel flag did not appear on disk after write"
        with results.open("a") as fh:
            fh.write(results_row(sh, dec, ts) + "\n")
        with ledger.open("a") as fh:
            fh.write("\t".join([ts, sh.id, "DONE", dec.mark, str(sh.tape.n),
                                f"{dec.share:.2f}", f"{dec.lo:.2f}", f"{dec.hi:.2f}",
                                dec.clause]) + "\n")
        return True, f"cancel flag written to {cancel_dir / sh.id}; results.tsv row appended"
    except OSError as e:
        return False, f"apply failed: {e}"


REMOTE_MANUAL = """\
  # ⛔ NO PER-SHARD CANCEL EXISTS ON A WORKER. Sequence, in this order only:
  tools/vps/orchestrate.sh kill {host}          # verify it prints 'workers remaining: 0'
  ssh {host} 'cd fcode-worker && touch results/{shard}.COMPLETE'   # so it is SKIPPED, not resumed
  tools/vps/orchestrate.sh start {host} <WORKERS>   # picks up the next shard in its worklist
  # ⚠ NEVER `stop` then `start`: cmd_start does `rm -f STOP`, so a curfewed worker
  #   wakes with no STOP file and double-subscribes the box (--tle 10 is wall-clock,
  #   so that silently corrupts every row BOTH workers produce)."""


# ═════════════════════════════════════════════════════════════════════════════
# DRIFT CHECK ON THE MARKS
# ═════════════════════════════════════════════════════════════════════════════
def marks_agree_with_gate_watch(path: Path | None = None) -> tuple[bool, str]:
    """The four integers above are a DUPLICATE of gate_watch's boundaries.

    A duplicate that nothing checks is the one that rots (D24(e)). This greps the
    authority for each literal and alarms if any has moved.
    """
    path = path or (REPO / "tools/monitors/gate_watch.sh")
    try:
        src = path.read_text()
    except OSError as e:
        return False, f"cannot read {path}: {e}"
    missing = [str(m) for m in (MARK_CATASTROPHE, MARK_MID, MARK_HALF)
               if not re.search(rf"n >= {m}\b", src)]
    if missing:
        return False, (f"gate_watch.sh no longer tests `n >= ` for: {', '.join(missing)} "
                       f"— the marks have DRIFTED apart. Fix before trusting this tool.")
    return True, f"marks {MARK_CATASTROPHE}/{MARK_MID}/{MARK_HALF} all still tested in {path.name}"


# ═════════════════════════════════════════════════════════════════════════════
# REPORT
# ═════════════════════════════════════════════════════════════════════════════
def fmt(sh: Shard, dec: Decision) -> str:
    """⛔ EVERY LINE CARRIES THE TAPE'S AGE AND ITS CLOCK.

    A healthy line and a blind line must not be byte-identical (`ship_watch`
    printed `rating=1599 armed=True RULE=held` off seven-minute-stale rows).
    """
    icon = {"STOP": "⛔ STOP    ", "CONTINUE": "   CONTINUE",
            "NOACTION": "   ---     "}[dec.action]
    if dec.computed:
        barstr = (f"bar={dec.bar.value:.2f}{dec.bar.direction}" if dec.bar else "bar=NONE")
        body = (f"n={sh.tape.n}/{sh.target or '?'} mark={dec.mark} "
                f"share={dec.share:.2f}% ci=[{dec.lo:.2f},{dec.hi:.2f}] {barstr} ")
    elif sh.tape.ok:
        # ⛔ NO share/ci PRINTED. An uncomputed 0.00% is indistinguishable from a
        # measured 0.00%, and this is precisely the line that must not read healthy.
        body = f"n={sh.tape.n}/{sh.target or '?'} share=NOT-COMPUTED "
    else:
        body = "n=UNREADABLE share=NOT-COMPUTED "
    age = (f"age={sh.age_s:.0f}s({sh.age_src})" if sh.age_s != float("inf")
           else "age=UNKNOWN(no clock)")
    return (f"{icon} {sh.id:<12} {sh.surface:<6}{('/' + sh.host) if sh.host else '':<26} "
            f"{body}{age}\n"
            f"              {dec.clause}: {dec.detail}"
            + ("".join(f"\n              ⚠ {x}" for x in sh.notes)))


def run(args) -> int:
    now = time.time()
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
    ps_out = _procs()

    ok, msg = marks_agree_with_gate_watch()
    print(f"auto_gate {ts}   mode={'APPLY' if args.apply else 'DRY-RUN (changes nothing)'}")
    print(f"  marks: {'OK' if ok else '⛔ DRIFT'} — {msg}")
    if not ok:
        print("  ⛔ REFUSING TO ACT: this tool's marks no longer match gate_watch's.")
        return 2

    bars = load_bars(Path(args.bars))
    print(f"  bars : {len(bars)} registered in {_rel(Path(args.bars))} "
          f"({', '.join(sorted(bars)) or 'none'})")

    reap = reaper_alive(ps_out)
    print(f"  reaper: corefill.sh {'RUNNING' if reap else ('BLIND (ps unreadable)' if reap is None else 'NOT RUNNING')}"
          + ("" if reap else "  ⛔ local --apply is REFUSED: a cancel flag with no reaper "
                             "neither kills the shard nor launches the next item"))
    print()

    shards = scan_local(Path(args.worklist), Path(args.tsvdir), ps_out, now)
    shards += scan_remote(Path(args.remote_root), now)
    shards.sort(key=lambda s: (s.surface, s.id))

    stops, n_live = [], 0
    for sh in shards:
        reason = already_cancelled(sh.id, Path(args.ledger), Path(args.started_dir),
                                   Path(args.cancel_dir), Path(args.results))
        dec = decide(sh, bars, args.stale_s, reason)
        if dec.action == "NOACTION" and dec.clause == "NOT-LIVE" and not args.all:
            continue
        n_live += 1
        print(fmt(sh, dec))
        if dec.action == "STOP":
            stops.append((sh, dec))
        print()

    print(f"── {n_live} live shard(s) evaluated; {len(stops)} would be STOPPED ──")
    if not stops:
        print("   Nothing is arithmetically dead. No shard would be touched.")
        return 0

    for sh, dec in stops:
        print(f"\n⛔ {sh.id} ({sh.surface}{'/' + sh.host if sh.host else ''})  {dec.clause}")
        if sh.surface == "remote":
            print(REMOTE_MANUAL.format(host=sh.host.split("/")[-1], shard=sh.id))
            print("  ⇒ REPORTED ONLY. --apply will not execute this.")
            continue
        print(f"  would: touch {_rel(Path(args.cancel_dir))}/{sh.id}")
        print(f"  row  : {results_row(sh, dec, ts)[:160]}...")
        if args.apply:
            if not reap:
                print("  ⛔ REFUSED: no live corefill.sh reaper.")
                continue
            done, why = apply_stop(sh, dec, cancel_dir=Path(args.cancel_dir),
                                   ledger=Path(args.ledger), results=Path(args.results),
                                   ts=ts)
            print(f"  {'APPLIED' if done else '⛔ NOT APPLIED'}: {why}")
    if not args.apply:
        print("\n(dry-run: nothing was changed. Re-run with --apply to cancel the above.)")
    return 0


# ═════════════════════════════════════════════════════════════════════════════
# SELFTEST — every guard driven to BOTH verdicts, on the SHIPPED functions
# ═════════════════════════════════════════════════════════════════════════════
def selftest() -> int:
    fails: list[str] = []

    def chk(label, got, want):
        if got == want:
            print(f"  PASS  {label:<74} -> {got}")
        else:
            print(f"  FAIL  {label:<74} -> {got} (want {want})")
            fails.append(label)

    tmp = Path(tempfile.mkdtemp(prefix="autogate_"))
    (tmp / "tsv").mkdir()
    (tmp / "state").mkdir()
    (tmp / "cancel").mkdir()

    # Two byte-identical trees (a NULL pair) and one that differs. Structural,
    # exactly like orchestrate.sh gen finds its null pair.
    for name, body in (("treeA", "x = 1\n"), ("treeB", "x = 1\n"), ("treeC", "x = 2\n")):
        (tmp / name).mkdir()
        (tmp / name / "main.py").write_text(body)
    assert trees_identical(str(tmp / "treeA"), str(tmp / "treeB"))
    assert not trees_identical(str(tmp / "treeA"), str(tmp / "treeC"))

    def tape(n, wins):
        return Tape(True, n=n, wins=wins, mtime=time.time())

    def shard(sid, n, wins, target=5400, treat="treeC", ctrl="treeA",
              age=1.0, live=True, ok=True):
        t = tape(n, wins) if ok else Tape(False, why="synthetic blind")
        return Shard(sid, "local", "", tmp / f"{sid}.tsv", str(tmp / treat),
                     str(tmp / ctrl), target, t, age, "tsv mtime", live, "RUNNER")

    BARS = {"REAL": Bar(51.33, "ge", "fixture"), "ABL": Bar(48.67, "le", "fixture"),
            "NULLY": Bar(51.33, "ge", "fixture"), "EDGE": Bar(51.33, "ge", "fixture")}

    print("\n── G0: the arithmetic itself (naive interval, no DEFF) ─────────────────")
    # ⛔ The expected constants below were computed INDEPENDENTLY of this module,
    # in Decimal at 30 digits, before being written here — not copied out of a
    # run. A test that echoes the implementation validates nothing.
    #   1.96*sqrt(0.25/1000)*100      = 3.09903210696501174535891567355
    #   wins=482/1000 -> ci_hi 51.2970 (< bar 51.33)   wins=483 -> 51.3972 (>=)
    #   wins=419/1000 -> ci_hi 44.9581 (< 45.0)        wins=420 -> 45.0591 (>=)
    s, lo, hi = ci95(500, 1000)
    chk("ci95(500,1000) half-width == 1.96*sqrt(.25/1000) = 3.0990pp",
        f"{hi - s:.4f}", "3.0990")
    chk("ci95 is symmetric about the point estimate", f"{s - lo:.6f}", f"{hi - s:.6f}")

    print("\n── G-EDGE: the cell that BITES — now at BAR MINUS MARGIN, not at BAR ──")
    # ⛔ THIS CELL WAS REWRITTEN s44 AND IT CAUGHT THE REWRITE. It used to test one
    # game either side of the BAR (482/483 of 1000). The rule now requires the bar
    # to be excluded by HALF A HALF-WIDTH, because the old form cancelled SPAWNLKL
    # on a margin of 0.0087pp — one game out of 3,646. So the live edge moved, and
    # the selftest FAILED on its own stale cell, which is exactly what it is for.
    # New edge: with bar 51.33 and margin = half a half-width, the flip sits far
    # below. Find it by search rather than by a hand-computed constant, so the cell
    # cannot rot the next time the rule moves.
    lo_w = None
    for w in range(300, 520):
        if decide(shard("EDGE", 1000, w), BARS, DEFAULT_STALE_S).action == "STOP":
            lo_w = w
    hi_w = lo_w + 1
    d_lo = decide(shard("EDGE", 1000, lo_w), BARS, DEFAULT_STALE_S)
    d_hi = decide(shard("EDGE", 1000, hi_w), BARS, DEFAULT_STALE_S)
    chk(f"n=1000 wins={lo_w} ci_hi={d_lo.hi:.3f} below bar-margin => STOP",
        d_lo.action, "STOP")
    chk(f"n=1000 wins={hi_w} ci_hi={d_hi.hi:.3f} inside margin  => CONTINUE",
        d_hi.action, "CONTINUE")
    chk("...the two differ by exactly ONE game", str(hi_w - lo_w), "1")
    # and the margin band itself must be reachable: a shard BELOW the bar but
    # INSIDE the margin continues, citing the new clause.
    d_mid = decide(shard("EDGE", 1000, 482), BARS, DEFAULT_STALE_S)
    chk("482/1000 (below bar, inside margin) now CONTINUES", d_mid.action, "CONTINUE")
    chk("...citing WITHIN-MARGIN, the clause that did not exist before",
        d_mid.clause, "WITHIN-MARGIN@1000")

    print("\n── G2: never below n=400 (399 vs 400, at a share that is 0%) ───────────")
    chk("n=399 wins=0  (CI upper 0.00, would be catastrophic) => CONTINUE",
        decide(shard("NOBAR9", 399, 0), BARS, DEFAULT_STALE_S).action, "CONTINUE")
    chk("...and the clause names the floor, not the arithmetic",
        decide(shard("NOBAR9", 399, 0), BARS, DEFAULT_STALE_S).clause, "PRE-400")
    chk("n=400 wins=0  => STOP", decide(shard("NOBAR9", 400, 0), BARS, DEFAULT_STALE_S).action, "STOP")
    chk("...on the catastrophe clause, which needs NO bar",
        decide(shard("NOBAR9", 400, 0), BARS, DEFAULT_STALE_S).clause, "CATASTROPHE")

    print("\n── G-CATA: the catastrophe boundary, CI upper just under vs over 45.0 ──")
    # n=1000: hi<45 needs wins around 419 (hi 44.99) vs 420 (hi 45.09).
    chk(f"n=1000 wins=419 ci_hi={ci95(419,1000)[2]:.3f} < 45.0 => STOP",
        decide(shard("NOBAR9", 1000, 419), BARS, DEFAULT_STALE_S).action, "STOP")
    chk(f"n=1000 wins=420 ci_hi={ci95(420,1000)[2]:.3f} >= 45.0 => CONTINUE (no bar)",
        decide(shard("NOBAR9", 1000, 420), BARS, DEFAULT_STALE_S).action, "CONTINUE")

    print("\n── G1: no registered bar => the BAR rule cannot stop it ────────────────")
    # 46.0% at n=2700: CI [44.12,47.88]. Upper 47.88 is BELOW bar 51.33 (a real
    # arm here STOPS) but ABOVE the 45.0 catastrophe line. So the ONLY thing
    # separating these two cells is whether a bar is registered.
    chk("n=2700 share 46.0% WITH bar 51.33 (ci_hi 47.88 < bar)      => STOP",
        decide(shard("REAL", 2700, 1242), BARS, DEFAULT_STALE_S).action, "STOP")
    chk("n=2700 share 46.0% with NO bar, same numbers               => CONTINUE",
        decide(shard("UNREG", 2700, 1242), BARS, DEFAULT_STALE_S).action, "CONTINUE")
    chk("...and it says WHY it could not stop",
        decide(shard("UNREG", 2700, 1242), BARS, DEFAULT_STALE_S).clause, "NO-BAR-REGISTERED")

    print("\n── G5: a NULL pair never stops; a REAL arm at the SAME share does ──────")
    # Same n, same wins, same bar. The ONLY difference is tree identity.
    null_arm = shard("NULLY", 2700, 1242, treat="treeA", ctrl="treeB")
    real_arm = shard("REAL", 2700, 1242, treat="treeC", ctrl="treeA")
    chk("byte-identical A/A pair at 46.0%, n=2700, bar 51.33        => CONTINUE",
        decide(null_arm, BARS, DEFAULT_STALE_S).action, "CONTINUE")
    chk("...on the structural clause, not a name check",
        decide(null_arm, BARS, DEFAULT_STALE_S).clause, "NULL-CELL")
    chk("NON-identical arm, IDENTICAL numbers and bar               => STOP",
        decide(real_arm, BARS, DEFAULT_STALE_S).action, "STOP")
    # And drive it where a NAME check would get it wrong, both ways.
    chk("a null NOT named *NULL* is still protected (name would miss it)",
        decide(shard("SHIPGATE", 2700, 1242, treat="treeA", ctrl="treeB"),
               {"SHIPGATE": Bar(51.33, "ge", "f")}, DEFAULT_STALE_S).clause, "NULL-CELL")
    chk("a NON-null NAMED 'NULLISH' is NOT protected (name would spare it)",
        decide(shard("NULLISH", 2700, 1242, treat="treeC", ctrl="treeA"),
               {"NULLISH": Bar(51.33, "ge", "f")}, DEFAULT_STALE_S).action, "STOP")
    # A null at a catastrophic share must ALSO survive.
    chk("a NULL reading 0% at n=1000 (catastrophe territory)        => CONTINUE",
        decide(shard("NULLY", 1000, 0, treat="treeA", ctrl="treeB"),
               BARS, DEFAULT_STALE_S).action, "CONTINUE")

    print("\n── G6: an ABLATION (le) bar is never auto-stopped, catastrophe included ─")
    chk("ablation at 30% n=2700 (its hypothesis SUCCEEDING)         => CONTINUE",
        decide(shard("ABL", 2700, 810), BARS, DEFAULT_STALE_S).action, "CONTINUE")
    chk("...clause names the inversion", decide(shard("ABL", 2700, 810), BARS,
        DEFAULT_STALE_S).clause, "ABLATION-INVERTED")
    chk("the SAME numbers on a normal `ge` bar                      => STOP",
        decide(shard("REAL", 2700, 810), BARS, DEFAULT_STALE_S).action, "STOP")

    print("\n── G3: BLIND is not DEAD — stale vs fresh, unreadable vs readable ──────")
    dead_numbers = dict(n=2700, wins=1242)   # would STOP if fresh and readable
    chk("fresh tape (age 1s), stoppable numbers                     => STOP",
        decide(shard("REAL", age=1.0, **dead_numbers), BARS, DEFAULT_STALE_S).action, "STOP")
    chk("STALE tape (age 901s), identical numbers                   => NOACTION",
        decide(shard("REAL", age=901.0, **dead_numbers), BARS, DEFAULT_STALE_S).action, "NOACTION")
    chk("...clause says BLIND-STALE, not dead",
        decide(shard("REAL", age=901.0, **dead_numbers), BARS, DEFAULT_STALE_S).clause,
        "BLIND-STALE")
    chk("UNREADABLE tape, would-be-stoppable                        => NOACTION",
        decide(shard("REAL", ok=False, **dead_numbers), BARS, DEFAULT_STALE_S).action, "NOACTION")
    # And the printed lines must not be byte-identical (the ship_watch defect).
    a = fmt(shard("REAL", age=1.0, **dead_numbers),
            decide(shard("REAL", age=1.0, **dead_numbers), BARS, DEFAULT_STALE_S))
    b = fmt(shard("REAL", age=901.0, **dead_numbers),
            decide(shard("REAL", age=901.0, **dead_numbers), BARS, DEFAULT_STALE_S))
    chk("a healthy line and a blind line are NOT byte-identical", a != b, True)
    chk("both lines carry an age= field", ("age=" in a) and ("age=" in b), True)
    chk("the healthy line prints a share", "share=46.00%" in a, True)
    chk("the blind line prints NO share (an uncomputed 0.00% would read as measured)",
        ("share=NOT-COMPUTED" in b) and ("%" not in b.split("\n")[0].split("age=")[0]
                                         .replace("share=NOT-COMPUTED", "")), True)
    # ORDERING: not-live must win over stale, or the archive (~140 finished
    # shards, all stale by definition) drowns the live ones in BLIND alarms.
    chk("NOT-live AND stale                                         => NOT-LIVE",
        decide(shard("REAL", age=99999.0, live=False, **dead_numbers),
               BARS, DEFAULT_STALE_S).clause, "NOT-LIVE")
    chk("LIVE and stale (the case that genuinely wants an eye)      => BLIND-STALE",
        decide(shard("REAL", age=99999.0, live=True, **dead_numbers),
               BARS, DEFAULT_STALE_S).clause, "BLIND-STALE")

    print("\n── read_tape: real file shapes, both surfaces + the malformed cases ────")
    hdr = "ts\tshard\tgame\tmap\tseed\tseat\twinner\tcond\tturns"
    rows = "\n".join(f"2026-08-15T00:00:00Z\tS\t{i}\tm\t1\tA\t{'T' if i % 2 else 'C'}\tx\t9"
                     for i in range(10))
    loc = tmp / "tsv" / "LOCALSHAPE.tsv"
    loc.write_text("# FIXTURE\tshard=S\ttreatment=a\tcontrol=b\n" + hdr + "\n" + rows + "\n")
    rem = tmp / "tsv" / "REMOTESHAPE.tsv"
    rem.write_text(hdr + "\n" + rows + "\n")
    chk("LOCAL tape with a # FIXTURE line counts 10 rows (not 11)", read_tape(loc).n, 10)
    chk("REMOTE tape with no FIXTURE line counts the same 10", read_tape(rem).n, 10)
    chk("...and both agree on wins", (read_tape(loc).wins, read_tape(rem).wins), (5, 5))
    bad = tmp / "tsv" / "BAD.tsv"
    bad.write_text("garbage,not,a,tape\n1,2,3\n")
    chk("a tape whose header is not 'ts\\t...' reads BLIND, not n=0", read_tape(bad).ok, False)
    chk("a header-only tape reads BLIND, not a 0-row arm",
        read_tape_str(tmp, hdr).ok, False)

    print("\n── G4: STOP ONCE — each of the four independent detectors, both ways ───")
    led = tmp / "ledger.tsv"
    res = tmp / "results.tsv"
    started = tmp / "state"
    cancel = tmp / "cancel"
    chk("clean slate: nothing claims ONCE",
        already_cancelled("ONCE", led, started, cancel, res), None)
    led.write_text("#h\n2026-08-15T00:00:00Z\tONCE\tCLAIM\t2700\t2700\t46.00\t44.12\t47.88\tX\n")
    chk("ledger detector fires",
        already_cancelled("ONCE", led, started, cancel, res) is not None, True)
    chk("...and does NOT fire for a different shard",
        already_cancelled("OTHER", led, started, cancel, res), None)
    (started / "M2").write_text("2026-08-15T00:00:00Z\ncancelled 2026-08-15T01:00:00Z\n")
    chk("corefill-marker detector fires", already_cancelled(
        "M2", led, started, cancel, res) is not None, True)
    (started / "M3").write_text("2026-08-15T00:00:00Z\n")   # started, NOT cancelled
    chk("...and a merely-STARTED marker does NOT fire",
        already_cancelled("M3", led, started, cancel, res), None)
    (cancel / "M4").write_text("pending\n")
    chk("pending-flag detector fires", already_cancelled(
        "M4", led, started, cancel, res) is not None, True)
    res.write_text("commit\tw\tl\th\tn\tstatus\tdesc\nm5-autostop-2700\t0.46\t\t\t2700\tcancellation\tx\n")
    chk("results.tsv detector fires (case-insensitive)",
        already_cancelled("M5", led, started, cancel, res) is not None, True)
    chk("...and does not fire on an unrelated row",
        already_cancelled("M6", led, started, cancel, res), None)
    # end-to-end: a shard the ledger claims must decide NOACTION even at a dead share
    chk("an already-claimed shard with stoppable numbers            => NOACTION",
        decide(shard("ONCE", 2700, 1242), BARS, DEFAULT_STALE_S,
               already_cancelled("ONCE", led, started, cancel, res)).action, "NOACTION")

    print("\n── the results row: typed `cancellation`, never `verdict` ──────────────")
    sh_ = shard("REAL", 2700, 1242)
    row = results_row(sh_, decide(sh_, BARS, DEFAULT_STALE_S), "2026-08-15T00:00:00Z")
    f = row.split("\t")
    chk("row has exactly 7 fields (results.tsv schema)", len(f), 7)
    chk("status field is 'cancellation'", f[5], "cancellation")
    chk("status field is NOT 'verdict'", f[5] != "verdict", True)
    chk("description carries the mark", "MARK-2700" in f[6], True)
    chk("description carries n", "n=2700" in f[6], True)
    chk("description carries the share", "46.00%" in f[6], True)
    chk("description carries the CI", "[44.12,47.88]" in f[6], True)
    chk("description carries the BAR", "51.33" in f[6], True)
    chk("description carries the rule clause", "FUTILITY-BAR@2700" in f[6], True)
    chk("description says rows are KEPT", "ROWS ARE KEPT" in f[6], True)
    chk("description disclaims being a verdict", "NOT A VERDICT" in f[6], True)

    print("\n── apply_stop: local writes the flag; remote is REFUSED ────────────────")
    led2, res2, can2 = tmp / "l2.tsv", tmp / "r2.tsv", tmp / "c2"
    res2.write_text("commit\tw\tl\th\tn\tstatus\tdesc\n")
    done, why = apply_stop(sh_, decide(sh_, BARS, DEFAULT_STALE_S), cancel_dir=can2,
                           ledger=led2, results=res2, ts="2026-08-15T00:00:00Z")
    chk("local apply reports success", done, True)
    chk("...the cancel flag EXISTS on disk (the load-bearing file)",
        (can2 / "REAL").exists(), True)
    chk("...the results row landed and is typed cancellation",
        res2.read_text().strip().splitlines()[-1].split("\t")[5], "cancellation")
    chk("...the ledger carries CLAIM before DONE",
        [l.split("\t")[2] for l in led2.read_text().splitlines() if not l.startswith("#")],
        ["CLAIM", "DONE"])
    chk("...and a re-run is now blocked by the ledger",
        already_cancelled("REAL", led2, started, can2, res2) is not None, True)
    remote_sh = Shard("RSH", "remote", "worker@h", tmp / "x.tsv", "", "", 5400,
                      tape(2700, 1242), 1.0, "remote heartbeat stamp", True, "RUNNING")
    done_r, why_r = apply_stop(remote_sh, decide(remote_sh, BARS, DEFAULT_STALE_S),
                               cancel_dir=can2, ledger=led2, results=res2,
                               ts="2026-08-15T00:00:00Z")
    chk("remote apply is REFUSED", done_r, False)
    chk("...for the stated reason (no per-shard primitive)", "no per-shard" in why_r, True)

    print("\n── liveness / freshness plumbing, both ways ────────────────────────────")
    chk("running_shards finds a runner in a ps line",
        "BODYAWR" in (running_shards(
            "zsh tools/overnight.sh BODYAWR bots/_a bots/_b 10800 336000") or set()), True)
    chk("...and does NOT match a monitor process",
        running_shards("python tools/monitors/replay_archiver.py"), set())
    chk("ps unreadable => running_shards is None (BLIND, not empty)",
        running_shards(None), None)
    chk("reaper_alive true on a corefill line",
        reaper_alive("zsh tools/corefill.sh scratchpad/corefill_work.txt 3 12"), True)
    chk("reaper_alive false with no corefill line", reaper_alive("zsh tools/overnight.sh X"), False)
    chk("reaper_alive BLIND when ps is unreadable", reaper_alive(None), None)
    chk("a shard with no live runner                                => NOACTION",
        decide(shard("REAL", 2700, 1242, live=False), BARS, DEFAULT_STALE_S).action, "NOACTION")
    chk("a shard already at target                                  => NOACTION",
        decide(shard("REAL", 5400, 2484, target=5400), BARS, DEFAULT_STALE_S).clause, "AT-TARGET")

    print("\n── heartbeat clock: the remote's OWN stamp, not our pull mtime ─────────")
    hb = tmp / "H.heartbeat"
    hb.write_text("2026-08-15T09:33:34Z\t4640\t5400\tLNCHRND1\tRUNNING\n")
    e, st = _read_heartbeat(hb)
    chk("heartbeat status parsed", st, "RUNNING")
    chk("heartbeat epoch parsed", e is not None, True)
    # ⛔ THE REGRESSION THAT SHIPPED AND WAS CAUGHT ON LIVE DATA. The first cut
    # used time.mktime()-time.timezone and was one DST hour out, declaring a
    # 4-minute-old remote heartbeat 3832s STALE. Pinned here against an epoch
    # computed OUTSIDE this module (POSIX definition: 1970-01-01T00:00:00Z == 0)
    # and against a same-instant round trip, so no timezone can move it again.
    hb.write_text("1970-01-01T00:00:00Z\t0\t1\tEPOCH\tRUNNING\n")
    chk("⛔ epoch anchor: 1970-01-01T00:00:00Z parses to exactly 0",
        _read_heartbeat(hb)[0], 0)
    hb.write_text("2026-08-15T09:33:34Z\t0\t1\tX\tRUNNING\n")
    chk("...and 2026-08-15T09:33:34Z to the value gmtime round-trips",
        time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(_read_heartbeat(hb)[0])),
        "2026-08-15T09:33:34Z")
    now_utc = time.time()
    hb.write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_utc))
                  + "\t0\t1\tNOW\tRUNNING\n")
    age_now = now_utc - _read_heartbeat(hb)[0]
    chk("⛔ a heartbeat stamped NOW reads age < 2s, not one DST hour",
        abs(age_now) < 2, True)
    chk("...and is therefore NOT declared stale (the live LNCHRND1 failure)",
        age_now <= DEFAULT_STALE_S, True)
    hb.write_text("2026-08-14T20:55:00Z\t1740\t5400\tSALTREF2\tCURFEW\n")
    chk("a CURFEW heartbeat is readable as CURFEW (asleep != dead)",
        _read_heartbeat(hb)[1], "CURFEW")
    chk("a truncated heartbeat yields no clock", _read_heartbeat(tmp / "nope.heartbeat"),
        (None, "?"))

    print("\n── marks: the duplicate is CHECKED against gate_watch, both ways ───────")
    ok, msg = marks_agree_with_gate_watch()
    chk("live gate_watch.sh still tests all three marks", ok, True)
    fake = tmp / "fake_gate_watch.sh"
    fake.write_text("if (( n >= 1000 )); then :; fi\n")   # 400 and 2700 removed
    ok2, msg2 = marks_agree_with_gate_watch(fake)
    chk("a gate_watch missing 400/2700 is DETECTED as drift", ok2, False)
    chk("...and the alarm names the missing marks", "400" in msg2 and "2700" in msg2, True)

    print("\n── bar registry parsing ────────────────────────────────────────────────")
    live_bars = load_bars(DEFAULT_BARS)
    chk("the shipped registry parses", len(live_bars) > 0, True)
    chk("BODYAWR reads 51.93 ge", (live_bars.get("BODYAWR").value,
                                   live_bars.get("BODYAWR").direction), (51.93, "ge"))
    chk("GUNAXABL reads 48.67 le (ablation)", (live_bars.get("GUNAXABL").value,
                                               live_bars.get("GUNAXABL").direction),
        (48.67, "le"))
    chk("a live-but-unregistered shard is genuinely absent",
        "LNCHERLY" in live_bars, False)
    junk = tmp / "junk_bars.tsv"
    junk.write_text("#c\nOK\t51.33\tge\tsrc\nBADDIR\t51.33\tsideways\tsrc\n"
                    "BADNUM\tnotanumber\tge\tsrc\nSHORT\t51.33\n")
    jb = load_bars(junk)
    chk("a malformed bar registry drops bad rows and keeps good ones",
        sorted(jb), ["OK"])

    # ── PLAUSIBILITY BOUND ON THE BAR ─────────────────────────────────────
    # Driven, not asserted. A malformed row was already covered above; this is
    # the WELL-FORMED WRONG NUMBER, which is the class that passes every other
    # guard because none of them can know what the bar should be. Under --apply
    # a typo'd bar cancels real arms every ten minutes.
    imp = tmp / "implausible_bars.tsv"
    imp.write_text("#c\nSLIP\t5193\tge\ttypo: 51.93 with a slipped decimal\n"
                   "FRAC\t0.5193\tge\tfraction not percent\n"
                   "HIGH\t95.0\tge\timplausible on this fixture\n"
                   "GOOD\t51.93\tge\tplausible\n")
    ib = load_bars(imp)
    chk("bar 5193 (slipped decimal) is REFUSED", "SLIP" in ib, False)
    chk("bar 0.5193 (fraction) is REFUSED", "FRAC" in ib, False)
    chk("bar 95.0 (implausible) is REFUSED", "HIGH" in ib, False)
    chk("bar 51.93 (plausible) is KEPT — the bound is not refusing everything",
        "GOOD" in ib, True)
    # ⭐ and the DIRECTION of the refusal: a rejected bar must leave the shard
    # UNSTOPPABLE, never stoppable on a wrong number.
    slip_sh = shard("SLIP", 2700, 1200)   # reuse the fixture factory, do not hand-build a Shard
    chk("a shard whose bar was REFUSED is unstoppable, not stoppable",
        decide(slip_sh, ib, DEFAULT_STALE_S).action, "CONTINUE")

    # ── TREND FLOOR (Magnus 2026-08-15) ───────────────────────────────────
    # Driven through read_tape() on REAL files, because the prefix counters only
    # exist there — a fixture Tape carries None and is deliberately unstoppable.
    print("\n── trend floor: the PREFIX share at each mark, exactly two looks ────────")
    tdir = tmp / "trend"
    tdir.mkdir(parents=True, exist_ok=True)

    def trend_shard(sid, spec, bars_key=None, treat="treeC", ctrl="treeA"):
        """spec: list of (count, 'T'|'C') written in order. Real file, real reader."""
        p = tdir / f"{sid}.tsv"
        rows = ["ts\ta\tb\tc\td\te\tres"]
        for cnt, ch in spec:
            rows += [f"0\t1\t2\t3\t4\t5\t{ch}"] * cnt
        p.write_text("\n".join(rows) + "\n")
        t = read_tape(p)
        return Shard(bars_key or sid, "local", "", p, str(tmp / treat),
                     str(tmp / ctrl), 5400, t, 1.0, "tsv mtime", True, "RUNNER")

    TB = dict(BARS)
    # one game either side of the floor at mark 1000 — 51.0% is NOT below 51.0
    s_below = trend_shard("TB_LOW",  [(509, "T"), (491, "C")], "REAL")
    s_at    = trend_shard("TB_AT",   [(510, "T"), (490, "C")], "REAL")
    chk("prefix@1000 50.90% (one game under the floor)  => STOP",
        decide(s_below, TB, DEFAULT_STALE_S).action, "STOP")
    chk("prefix@1000 51.00% (exactly AT the floor)      => CONTINUE",
        decide(s_at, TB, DEFAULT_STALE_S).action, "CONTINUE")
    chk("...and the stop names the mark it fired at",
        decide(s_below, TB, DEFAULT_STALE_S).clause, f"TREND-FLOOR@{MARK_MID}")

    # the SECOND mark bites independently: clears 1000, fails 2700
    s_m2 = trend_shard("TB_M2", [(510, "T"), (490, "C"), (865, "T"), (835, "C")], "REAL")
    chk(f"clears {MARK_MID} (51.00%) but prefix@{MARK_HALF} 50.93% => STOP at the 2nd mark",
        decide(s_m2, TB, DEFAULT_STALE_S).clause, f"TREND-FLOOR@{MARK_HALF}")

    # ⛔ THE OPTIONAL-STOPPING GUARD, and it is the reason prefixes exist at all.
    # Both cells below have a CURRENT share that points the opposite way from the
    # prefix. If either verdict follows the current share, this tool is taking
    # ~400 looks at a random walk instead of two, and the false-drop rate it was
    # priced at is fiction.
    s_lowpfx_highnow = trend_shard("TB_A", [(400, "T"), (600, "C"), (3400, "T"), (600, "C")], "REAL")
    s_highpfx_lownow = trend_shard("TB_B", [(600, "T"), (400, "C"), (600, "T"), (3400, "C")], "REAL")
    chk("bad prefix, GREAT current share (now 66.7%)   => STOP anyway",
        decide(s_lowpfx_highnow, TB, DEFAULT_STALE_S).action, "STOP")
    chk("good prefix, AWFUL current share (now 26.7%)  => not stopped by the floor",
        decide(s_highpfx_lownow, TB, DEFAULT_STALE_S).clause.startswith("TREND-FLOOR"), False)

    # too early: the mark is not reached, so the rule cannot look
    s_early = trend_shard("TB_EARLY", [(100, "T"), (899, "C")], "REAL")
    chk(f"n=999 at 10.0% — below {MARK_MID}, floor CANNOT look yet",
        decide(s_early, TB, DEFAULT_STALE_S).clause.startswith("TREND-FLOOR"), False)

    # ⭐ THE COVERAGE-GAP CLOSURE: an UNREGISTERED shard is now stoppable by the
    # house default. Under the old design it got no rule at all, so a gap in
    # BARS.tsv was also a gap in enforcement (side lane, 2026-08-15).
    s_nobar = trend_shard("TB_UNREG", [(480, "T"), (520, "C")], "NOT_IN_REGISTRY")
    dn = decide(s_nobar, TB, DEFAULT_STALE_S)
    chk("an UNREGISTERED shard at 48.0% is STOPPED by the house default",
        dn.action, "STOP")
    chk("...and the reason says the bar was a DEFAULT, not a registered row",
        "DEFAULT (no bar row)" in dn.detail, True)

    # exemption ORDER: an ablation must survive a low prefix (low IS its success)
    s_abl = trend_shard("TB_ABL", [(300, "T"), (700, "C")], "ABL")
    chk("an ABLATION (le bar) at 30.0% is NOT stopped by the floor",
        decide(s_abl, TB, DEFAULT_STALE_S).clause.startswith("TREND-FLOOR"), False)

    # a fixture Tape carries None prefixes => BLIND => never stopped by the floor
    chk("a Tape with UNKNOWN prefixes is unstoppable by the floor (blind != dead)",
        decide(shard("REAL", 2700, 100), TB, DEFAULT_STALE_S).clause.startswith("TREND-FLOOR"),
        False)

    # ── KILL SWITCH ───────────────────────────────────────────────────────
    # THE ONLY GUARD WHOSE FAILURE MODE IS "the person trying to stop the damage
    # cannot". A pause file that does not work fails exactly when someone needs
    # it — at 3am, on a wrong bar, by a successor who read the header and trusted
    # it. Driven end-to-end through the SHIPPED entry point, in a subprocess,
    # because that is the thing an operator actually invokes.
    stop_f = REPO / "scratchpad" / "AUTOGATE_STOP"
    pre_existing = stop_f.is_file()
    try:
        stop_f.touch()
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--apply"],
                           capture_output=True, text=True, cwd=str(REPO), timeout=120)
        chk("STOP file present -> exits 0", r.returncode, 0)
        chk("STOP file present -> says PAUSED", "PAUSED" in r.stdout, True)
        chk("STOP file present -> evaluates NOTHING",
            "live shard(s) evaluated" in r.stdout, False)
        stop_f.unlink()
        r2 = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--dry-run"],
                            capture_output=True, text=True, cwd=str(REPO), timeout=180)
        chk("STOP file absent -> resumes and evaluates",
            "live shard(s) evaluated" in r2.stdout, True)
        chk("paused output and running output are NOT byte-identical",
            r.stdout.strip() == r2.stdout.strip(), False)
    finally:
        if pre_existing:
            stop_f.touch()
        elif stop_f.is_file():
            stop_f.unlink()

    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    print()
    if fails:
        print(f"SELFTEST FAIL — {len(fails)} check(s): " + "; ".join(fails))
        return 1
    print("SELFTEST PASS — every guard driven to BOTH verdicts on the shipped functions "
          "(G1 bar/no-bar at identical numbers · G2 n=399/400 · G3 fresh/stale + "
          "readable/unreadable + non-identical lines · G4 four detectors each ± · "
          "G5 null/real at identical numbers, incl. the two cells a NAME check gets "
          "wrong · G6 ablation/normal · edge cell one game either side of the bar · "
          "catastrophe one game either side of 45.0 · marks drift ± · KILL SWITCH halts/resumes end-to-end through the shipped entry point · BAR PLAUSIBILITY refuses slipped-decimal/fraction/implausible and keeps a good one, leaving a refused shard UNSTOPPABLE)")
    return 0


def read_tape_str(tmp: Path, hdr: str) -> Tape:
    p = tmp / "tsv" / "HDRONLY.tsv"
    p.write_text(hdr + "\n")
    return read_tape(p)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true",
                    help="actually cancel (local shards only). Default is --dry-run.")
    # `--dry-run` is explicit-default, and if BOTH are passed the SAFE one wins.
    # A flag pair where the destructive member silently outranks the safe member
    # is a footgun in a tool whose whole job is killing things.
    ap.add_argument("--dry-run", action="store_true",
                    help="print decisions, change nothing (DEFAULT; overrides --apply)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--all", action="store_true",
                    help="also print shards with no live runner")
    ap.add_argument("--worklist", default=str(DEFAULT_WORKLIST))
    ap.add_argument("--tsvdir", default=str(DEFAULT_TSVDIR))
    ap.add_argument("--remote-root", default=str(DEFAULT_REMOTE_ROOT))
    ap.add_argument("--bars", default=str(DEFAULT_BARS))
    ap.add_argument("--cancel-dir", default=str(DEFAULT_CANCEL_DIR))
    ap.add_argument("--started-dir", default=str(DEFAULT_STARTED_DIR))
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    ap.add_argument("--results", default=str(DEFAULT_RESULTS))
    ap.add_argument("--stale-s", type=float, default=DEFAULT_STALE_S)
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    # ⛔⛔ KILL SWITCH. Added s44 immediately after --apply was armed.
    # An autonomous CANCELLER whose only stop is "know and kill the pid" is not
    # stoppable by anyone who did not start it. Its sibling automation has had
    # this since it was written — `corefill.sh:124` checks scratchpad/COREFILL_STOP
    # and any lane can pause it with a `touch`, from a line documented in its own
    # header. Same idiom, same directory, so a successor who finds a wrong bar at
    # 3am halts this the way they would halt corefill, without reading source.
    # ⚠ Deliberately checked in main() and not once at import: the loop re-invokes
    # python each cycle, so the file is read every 600s and the pause takes effect
    # on the next tick rather than requiring a restart.
    stop_file = REPO / "scratchpad" / "AUTOGATE_STOP"
    if stop_file.is_file():
        print(f"PAUSED — {stop_file} is present. Evaluating nothing, cancelling "
              f"nothing. Delete the file to resume.")
        return 0

    if args.dry_run and args.apply:
        print("⚠ both --dry-run and --apply given; DRY-RUN WINS. Nothing will be changed.")
        args.apply = False
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
