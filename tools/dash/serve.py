#!/usr/bin/env python3
"""
CORE DASHBOARD — what is running locally, plus a game reference and a lingo
dictionary. Commissioned by Magnus, 2026-08-13.

    .venv/bin/python tools/dash/serve.py          # then open http://127.0.0.1:8787
    PORT=9000 .venv/bin/python tools/dash/serve.py

⛔ FOUR THINGS THIS DOES THAT A NAIVE DASHBOARD WOULD NOT, EACH ONE A DEFECT THIS
   REPO HAS ALREADY SHIPPED:

1. **EVERY NUMBER CARRIES ITS AGE.** `ship_watch` once printed
   `rating=1599 armed=True RULE=held` off rows seven minutes stale, and a HEALTHY
   line and a BLIND line were byte-identical. Nothing here renders without a
   freshness stamp, and anything past its cadence is marked STALE in the UI.
2. **BLIND IS A STATE, NOT A ZERO.** If `ps` fails or a file is unreadable the
   section reports BLIND. It never reports "0 running", because an alarm that
   cannot tell it is blind is this repo's most-repeated defect.
3. **IT DOES NOT RE-IMPLEMENT THE SHARD TABLE.** `tools/corefill_status.sh` is
   the production computation (STALLED vs DEAD, the <400-row rate refusal, the
   band beside every rate). This shells out to it and shows its output verbatim.
   Re-deriving it here would be the "test builds its own copy of the computation"
   defect, in production — exactly what `cores_idle` was flagged for this morning.
4. **NO NETWORK, NO `fcode`, READ-ONLY.** The holder and rating come from the
   LOCAL elo tape with its age shown, not from a live CLI call. This process
   cannot submit, activate, or spend a rate-limited call. It only reads files
   and `ps`.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATIC = Path(__file__).resolve().parent / "static"
PORT = int(os.environ.get("PORT", "8787"))

# The match history lives in its own module: it reads different files, on a
# different cadence, and keeping it out of here keeps this file's diff to the
# routes below. See tools/dash/matches.py for what it is and is not allowed to do.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import matches                                                    # noqa: E402

OVERNIGHT = ROOT / "scratchpad" / "overnight"
STARTED = ROOT / "scratchpad" / "corefill_started"
WORKLIST = Path(os.environ.get("COREFILL_WORK",
                               str(ROOT / "scratchpad" / "corefill_work.txt")))

# ---------------------------------------------------------------- map rotation
# ⛔ THE MAP POOL ROTATED MID-DAY 2026-08-13 AND HALF OF EVERY OLDER SHARD IS ON
# GEOMETRY THAT NO LONGER EXISTS. `tools/overnight.sh` was re-pointed from an
# 8-map array at the pool's own rotation; FOUR of those eight -- atoll, heart,
# hive, meander -- are gone from the live pool, and the live pool added a 30x30
# size class we had never played. Pooling a pre-rotation shard with a live-pool
# one is comparing two different games, so the detail view LABELS the map set.
#
# ⛔⛔ AND THE POOL ITSELF IS **PARSED FROM `tools/overnight.sh`**, NEVER LISTED
# HERE. That file's `MAPS=(...)` line is what actually decides which maps a shard
# plays, and `tools/corefill_status.sh` already parses that same line for its
# `RETIRED n%` column. A hardcoded copy in this file would be a THIRD definition
# of the live pool, drifting silently the next time the organisers rotate --
# which is the exact defect class this dashboard was flagged for. If the parse
# fails we report BLIND rather than falling back to a stale literal.
#
# ⭐ AND THE PER-SHARD LABEL IS READ OFF EACH SHARD'S OWN ROWS, NOT GUESSED FROM
# A CLOCK. `<SHARD>.tsv` carries a `map` column (header: ts shard game map seed
# seat winner cond turns), so the map set is a MEASUREMENT. Launch time is only
# the fallback, used when a shard's rows name nothing but maps common to both
# sets -- and it is labelled as an inference when it is one. A wrong label here
# is worse than "unknown", so "unknown" is a first-class verdict.
POOL_SRC = ROOT / "tools" / "overnight.sh"
# Boundary = the commit that re-pointed tools/overnight.sh (git: f1b5700,
# 2026-08-13T10:18:54+02:00 == 08:18:54Z). Cited, not hand-written.
ROTATION_COMMIT = "f1b5700"
ROTATION_AT = datetime(2026, 8, 13, 8, 18, 54, tzinfo=timezone.utc)


def map_pools() -> dict:
    """Live pool + the pool it replaced, both parsed out of `tools/overnight.sh`.

    live : the `MAPS=(...)` array -- THE line the runner iterates, and the same
           line `tools/corefill_status.sh` parses for its RETIRED column.
    prev : the `# The old set was (...)` comment beside it. A comment is a weaker
           anchor than an array, so its failure is contained: without it the
           pre/live split still works (anything outside the live pool is retired
           geometry) and only the MIXED verdict becomes unavailable, which the
           page then says out loud instead of guessing.
    """
    out = {"live": frozenset(), "prev": frozenset(), "blind": None,
           "prev_blind": None, "src": str(POOL_SRC.relative_to(ROOT))}
    try:
        text = POOL_SRC.read_text(errors="replace")
    except Exception as e:
        out["blind"] = f"cannot read {out['src']}: {type(e).__name__}: {e}"
        return out
    m = re.search(r"^MAPS=\((.*)\)\s*$", text, re.M)
    if not m:
        out["blind"] = f"no `MAPS=(...)` line in {out['src']} — live pool UNKNOWN"
    else:
        out["live"] = frozenset(m.group(1).split())
    p = re.search(r"old set was \(([^)]*)\)", text)
    if not p:
        out["prev_blind"] = (f"no `The old set was (...)` note in {out['src']} — "
                             f"cannot tell a straddling shard from a pre-rotation one")
    else:
        out["prev"] = frozenset(p.group(1).split())
    return out

# corefill_status.sh takes ~3.5 s, so it runs on a timer in the background and the
# page shows the CACHED text WITH ITS AGE. A slow truth beats a fast guess, and an
# undated cache is the thing this file exists to avoid.
SHARD_REFRESH_SEC = 45
_shard_cache = {"text": None, "at": None, "error": None}
_shard_lock = threading.Lock()


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def age_min(then: datetime | None) -> float | None:
    if then is None:
        return None
    return (now_utc() - then).total_seconds() / 60.0


def parse_ts(s: str) -> datetime | None:
    """Parse the stamp shapes this repo writes. Returns None, never raises.

    ⛔ THE ZONES ARE NOT UNIFORM AND THE DIFFERENCE IS TWO HOURS.
    Monitor logs (`ship_watch`, `cores_idle`, the shard heartbeats) end in `Z` and
    are genuinely UTC. **`elo_history.tsv` writes LOCAL wall-clock with NO marker**
    — `09:32` there is `07:32Z`. Reading it as UTC produced a NEGATIVE age on this
    dashboard's first run, which is the only reason it was caught: a negative age
    is impossible, and an impossible value is the cheapest alarm there is. A
    plausible-but-wrong offset would have shipped silently.
    """
    s = (s or "").strip()
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    # No `Z` ⇒ local wall-clock. `.astimezone()` on a naive datetime assumes the
    # system zone, which is what wrote it.
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M").astimezone(timezone.utc)
    except ValueError:
        return None


def ps_lines() -> list[str] | None:
    """All process command lines, or None meaning BLIND (never an empty list)."""
    try:
        out = subprocess.run(["ps", "ax", "-o", "command="],
                             capture_output=True, text=True, timeout=10)
        if out.returncode != 0:
            return None
        return out.stdout.splitlines()
    except Exception:
        return None


def tail_lines(p: Path, n: int = 400) -> list[str]:
    try:
        return p.read_text(errors="replace").splitlines()[-n:]
    except Exception:
        return []


# ---------------------------------------------------------------- collectors


def collect_load() -> dict:
    try:
        one, five, fifteen = os.getloadavg()
        return {"ok": True, "one": round(one, 2), "five": round(five, 2),
                "fifteen": round(fifteen, 2)}
    except Exception as e:
        return {"ok": False, "blind": f"getloadavg failed: {e}"}


def collect_procs(lines: list[str] | None) -> dict:
    """Live game processes and the monitor fleet. BLIND if ps failed."""
    if lines is None:
        return {"ok": False, "blind": "ps failed — process state UNKNOWN, "
                                      "this is NOT 'nothing running'"}
    games = [l for l in lines if re.search(r"\bfcode\b.*\brun\b", l)]
    watchers = {
        "keeper": r"corpus/keeper\.py",
        "cores_idle": r"monitors/cores_idle\.py",
        "ship_watch": r"monitors/ship_watch\.py",
        "breakin_watch": r"monitors/breakin_watch\.py",
        "elo_logger": r"monitors/elo_logger\.py",
        "match_watcher": r"monitors/match_watcher\.py",
        "opp_watcher": r"monitors/opp_watcher\.py",
        "replay_archiver": r"monitors/replay_archiver\.py",
    }
    mon = {name: any(re.search(pat, l) for l in lines) for name, pat in watchers.items()}
    corefill = any("corefill" in l for l in lines)
    return {"ok": True, "games": len(games), "monitors": mon,
            "monitors_up": sum(1 for v in mon.values() if v),
            "monitors_total": len(mon), "corefill": corefill}


def collect_holder() -> dict:
    """Holder + rating from the LOCAL elo tape. Never a live CLI call.

    ⭐ THE AGE COMES FROM `tools/freshness.newest_row_age_h(..., assume_local=True)`,
    NOT from a parser written here. `elo_history.tsv` stores LOCAL wall-clock with no
    marker, and this dashboard's first version read it as UTC and reported a NEGATIVE
    age. That is not a new discovery — `freshness.py` already carries the
    `assume_local` flag and its own comment records the identical symptom
    ("tape read -2.0h old as UTC and 0.0h with assume_local=True"). The repo solved
    this before; a third implementation of a solved problem is the defect, so this
    calls the existing one.
    """
    tape = ROOT / "elo_history.tsv"
    age_h, newest = None, None
    try:
        import sys
        if str(ROOT / "tools") not in sys.path:
            sys.path.insert(0, str(ROOT / "tools"))
        import freshness
        age_h, newest = freshness.newest_row_age_h(tape, assume_local=True)
    except Exception as e:
        return {"ok": False, "blind": f"freshness helper unavailable: {e}"}

    for line in reversed(tail_lines(tape, 5)):
        parts = line.split("\t")
        if len(parts) >= 4 and parts[1].strip().isdigit():
            return {"ok": True, "rating": int(parts[1]), "matches": parts[2].strip(),
                    "version": parts[3].strip(),
                    "at": iso(newest.astimezone(timezone.utc)) if newest else None,
                    "age_min": round(age_h * 60.0, 1) if age_h is not None else None,
                    "cadence_min": 5.0}
    return {"ok": False, "blind": "elo_history.tsv unreadable or has no parsable row"}


def collect_cores_idle() -> dict:
    """The idle alarm's own latest verdict, with its age."""
    rows = tail_lines(ROOT / "corpus" / "cores_idle.log", 5)
    if not rows:
        return {"ok": False, "blind": "cores_idle.log unreadable"}
    last = rows[-1]
    ts = parse_ts(last.split("\t")[0])
    alerting = "CORES IDLE" in last
    m = re.search(r"consec_idle=(\d+)", last)
    return {"ok": True, "line": last.strip(), "alerting": alerting,
            "consec_idle": int(m.group(1)) if m else None,
            "at": iso(ts) if ts else None,
            "age_min": round(age_min(ts), 1) if ts else None,
            "cadence_min": 5.0,
            "alert_file": (ROOT / "corpus" / "CORES_IDLE_ALERT").exists()}


def collect_ship_watch() -> dict:
    rows = tail_lines(ROOT / "corpus" / "ship_watch.log", 5)
    for line in reversed(rows):
        if "\t" not in line:
            continue
        ts = parse_ts(line.split("\t")[0])
        fields = dict(re.findall(r"(\w+)=([^\s\t]+)", line))
        return {"ok": True, "at": iso(ts) if ts else None,
                "age_min": round(age_min(ts), 1) if ts else None,
                "cadence_min": 10.0, "fields": fields}
    return {"ok": False, "blind": "ship_watch.log unreadable or empty"}


def collect_queue() -> dict:
    """Unblocked count from `queue_check.py` — the production admission gate.

    ⛔ A FIRST VERSION COUNTED `| N |` ROWS HERE AND REPORTED 4 WHERE THE GATE SAYS
    21. The queue's admission rule (a row counts only with a `GREP:` naming what was
    checked in the incumbent) is not reconstructible from table shape, and guessing
    at it is the same defect this lane flagged in `cores_idle` this morning: a second
    copy of a computation, disagreeing with the first. Call the gate instead.
    """
    p = ROOT / "QUEUE.md"
    if not p.exists():
        return {"ok": False, "blind": "QUEUE.md not found"}
    mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
    out = {"ok": True, "at": iso(mtime), "age_min": round(age_min(mtime), 1),
           "unblocked": None, "floor": None}
    try:
        r = subprocess.run([str(ROOT / ".venv" / "bin" / "python"),
                            str(ROOT / "tools" / "queue_check.py")],
                           cwd=str(ROOT), capture_output=True, text=True, timeout=60)
        m = re.search(r"unblocked items:\s*(\d+)\s*\(floor\s*(\d+)\)", r.stdout)
        if m:
            out["unblocked"], out["floor"] = int(m.group(1)), int(m.group(2))
        else:
            out["gate_unreadable"] = "queue_check produced no 'unblocked items' line"
    except Exception as e:
        out["gate_unreadable"] = f"{type(e).__name__}: {e}"
    return out


def collect_shard_summary(ps: list[str] | None) -> dict:
    """At-a-glance tally. The AUTHORITATIVE table is corefill_status.sh's text.

    ⛔ THIS MIRRORS `corefill_status.sh`'s STATE LADDER EXACTLY, in its order, on
    purpose. A first version invented its own and reported 13 STALLED where the
    production tool sees DONE and DEAD — because it conflated *alive but frozen*
    with *no process at all*, and aged the heartbeat by the timestamp INSIDE the
    file rather than by its mtime. Two copies of one computation that disagree is
    exactly the defect this lane flagged in `cores_idle` this morning; where a
    tally must exist, it copies the ladder rather than improvising one.

        .COMPLETE          -> DONE
        state has cancelled-> CANCELLED
        alive and >600s    -> STALLED   (frozen)
        alive              -> running
        state file exists  -> DEAD      (started, no process)
        otherwise          -> queued
    """
    d = ROOT / "scratchpad" / "overnight"
    state_dir = ROOT / "scratchpad" / "corefill_started"
    if ps is None:
        return {"ok": False, "blind": "ps failed — shard liveness UNKNOWN, "
                                      "which is not the same as 'none running'"}
    try:
        names = sorted({p.name.split(".")[0] for p in d.glob("*.heartbeat")}
                       | {p.name for p in state_dir.glob("*")} if state_dir.exists()
                       else {p.name.split(".")[0] for p in d.glob("*.heartbeat")})
    except Exception:
        return {"ok": False, "blind": "overnight/state dir unreadable"}

    buckets: dict[str, list] = {k: [] for k in
                                ("running", "STALLED", "DONE", "CANCELLED", "DEAD", "queued")}
    for sh in names:
        hb = d / f"{sh}.heartbeat"
        agesec, done_n, target_n = None, None, None
        if hb.exists():
            try:
                agesec = time.time() - hb.stat().st_mtime          # mtime, as corefill does
                parts = hb.read_text(errors="replace").strip().split("\t")
                if len(parts) >= 3:
                    done_n, target_n = parts[1], parts[2]
            except Exception:
                pass
        alive = any(f"overnight.sh {sh} " in l for l in ps)
        sf = state_dir / sh
        cancelled = False
        try:
            cancelled = sf.exists() and "cancelled" in sf.read_text(errors="replace")
        except Exception:
            pass

        if (d / f"{sh}.COMPLETE").exists():          st = "DONE"
        elif cancelled:                              st = "CANCELLED"
        elif alive and agesec is not None and agesec > 600: st = "STALLED"
        elif alive:                                  st = "running"
        elif sf.exists():                            st = "DEAD"
        else:                                        st = "queued"

        buckets[st].append({"shard": sh, "state": st, "done": done_n,
                            "target": target_n,
                            "age_min": round(agesec / 60.0, 1) if agesec is not None else None})

    for v in buckets.values():
        v.sort(key=lambda r: r["shard"])
    return {"ok": True,
            "running": buckets["running"], "stalled": buckets["STALLED"],
            "n_running": len(buckets["running"]), "n_stalled": len(buckets["STALLED"]),
            "n_done": len(buckets["DONE"]), "n_cancelled": len(buckets["CANCELLED"]),
            "n_dead": len(buckets["DEAD"]), "n_queued": len(buckets["queued"]),
            "n_total": len(names)}


def _refresh_shard_text() -> None:
    script = ROOT / "tools" / "corefill_status.sh"
    if not script.exists():
        with _shard_lock:
            _shard_cache.update(text=None, at=now_utc(),
                                error="tools/corefill_status.sh not found")
        return
    try:
        out = subprocess.run(["zsh", str(script)], cwd=str(ROOT),
                             capture_output=True, text=True, timeout=120)
        with _shard_lock:
            _shard_cache.update(text=out.stdout or out.stderr, at=now_utc(), error=None)
    except Exception as e:
        with _shard_lock:
            _shard_cache.update(text=None, at=now_utc(), error=f"{type(e).__name__}: {e}")


def _shard_worker() -> None:
    while True:
        _refresh_shard_text()
        time.sleep(SHARD_REFRESH_SEC)


ROW_RE = re.compile(r"^(\S+)\s+(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.*)$")


NON_ROW_FIRST_WORDS = {"SHARD", "COREFILL", "CANCEL", "load", "total",
                       "ADD", "PAUSE", "FULL", "***", "^"}


def parse_shard_table(text: str | None) -> list[dict]:
    """`corefill_status.sh`'s own table, IN ITS OWN ORDER, field for field.

    ⛔ THIS IS THE ONLY PLACE SHARD STATE / ROWS / PCT / HB_AGE / ETA / RATE / BAND
    ENTER THIS PROCESS, AND NOTHING RECOMPUTES ANY OF THEM. The arithmetic is
    trivial; the JUDGEMENT wrapped around it is not — the tool distinguishes
    STALLED (alive but frozen) from DEAD (started, no process), and it REFUSES to
    print a rate under 400 rows because the band there is wider than any effect we
    chase. A second copy of that ladder is precisely the defect this dashboard was
    flagged for on 2026-08-13 (it reported 13 STALLED where the tool sees DONE and
    DEAD). Parsing inherits every refusal instead of re-deriving it.

    `tools/dash/shard_diffcheck.py` re-parses the same text with a DIFFERENT
    implementation (column slicing, not this regex) and fails on any disagreement.
    """
    out: list[dict] = []
    for line in (text or "").splitlines():
        m = ROW_RE.match(line)
        if not m or m.group(1) in NON_ROW_FIRST_WORDS:
            continue
        shard, state, rows, pct, hb, eta, result = m.groups()
        rec = {"shard": shard, "state": state, "rows": int(rows), "pct": pct,
               "hb_age": hb, "eta": eta, "result_raw": result.strip(),
               "rate": None, "band": None, "n": None, "refused": False}
        if "NO RATE PRINTED" in result:
            rec["refused"] = True
        else:
            r = re.search(r"([\d.]+)%", result)
            b = re.search(r"band \+-([\d.]+)pp", result)
            if r:
                rec["rate"] = float(r.group(1))
            if b:
                rec["band"] = float(b.group(1))
        nn = re.search(r"n=(\d+)", result)
        if nn:
            rec["n"] = int(nn.group(1))
        # RETIRED% — the tool's own count of rows played on maps that have left the
        # live pool. Parsed, never recomputed; `None` means the tool did not
        # measure it (no rate printed at all), which is not the same as zero.
        rec["retired_blind"] = "RETIRED:BLIND" in result
        if rec["rate"] is None or rec["refused"]:
            rec["retired_pct"] = None
        elif rec["retired_blind"]:
            rec["retired_pct"] = None
        else:
            rp = re.search(r"RETIRED (\d+)%", result)
            rec["retired_pct"] = int(rp.group(1)) if rp else 0
        # separated = the whole interval sits off 50, i.e. it is saying something
        if rec["rate"] is not None and rec["band"] is not None:
            lo, hi = rec["rate"] - rec["band"], rec["rate"] + rec["band"]
            rec["lo"], rec["hi"] = round(lo, 2), round(hi, 2)
            rec["separated"] = lo > 50.0 or hi < 50.0
        out.append(rec)
    return out


def parse_shard_rows(text: str | None) -> dict:
    """Same rows, keyed by shard. Kept for the cores page; one parse, two shapes."""
    return {r["shard"]: r for r in parse_shard_table(text)}


def collect_shard_text() -> dict:
    with _shard_lock:
        c = dict(_shard_cache)
    if c["at"] is None:
        return {"ok": False, "pending": True, "rows": {},
                "note": "corefill_status.sh has not completed its first run yet"}
    return {"ok": c["error"] is None, "text": c["text"], "error": c["error"],
            "rows": parse_shard_rows(c["text"]),
            "at": iso(c["at"]), "age_min": round(age_min(c["at"]), 1),
            "cadence_min": SHARD_REFRESH_SEC / 60.0}


# ------------------------------------------------------------------ shards view


def load_worklist(path: Path = WORKLIST) -> dict:
    """The worklist that DEFINES each shard: its own line, verbatim, plus context.

    Format (`tools/corefill.sh`): `<shard> <treatment> <control> <target> <seed_lo>`.
    The `#` block immediately above a group is carried along because it is what the
    operator actually wrote about why those shards exist — verbatim, attributed to
    the file, never paraphrased into a claim this page invented.
    """
    out = {"ok": False, "path": str(path), "shards": {}, "order": [],
           "at": None, "age_min": None}
    try:
        text = path.read_text(errors="replace")
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    except Exception as e:
        out["blind"] = f"worklist unreadable: {type(e).__name__}: {e}"
        return out
    out["ok"] = True
    out["at"] = iso(mtime)
    out["age_min"] = round(age_min(mtime), 1)
    block: list[str] = []
    pending: list[str] = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if not s:
            continue
        if s.startswith("#"):
            pending.append(s)
            continue
        parts = s.split()
        if pending:
            block, pending = pending, []
        sh = parts[0]
        rec = {"line": s, "lineno": lineno, "treatment": None, "control": None,
               "target": None, "seed_lo": None, "comment_block": list(block)}
        if len(parts) >= 3:
            rec["treatment"], rec["control"] = parts[1], parts[2]
        if len(parts) >= 4:
            rec["target"] = parts[3]
        if len(parts) >= 5:
            rec["seed_lo"] = parts[4]
        if rec["treatment"] and rec["control"]:
            rec["tests"] = (f"{rec['treatment']} (arm) against {rec['control']} "
                            f"(control)")
            if rec["target"]:
                rec["tests"] += f", target {rec['target']} games"
            if rec["seed_lo"]:
                rec["tests"] += f" from seed {rec['seed_lo']}"
            rec["tests"] += "."
        else:
            rec["tests"] = None      # not derivable ⇒ omitted, never invented
        out["shards"][sh] = rec
        out["order"].append(sh)
    return out


# A worklist comment block is written for a GROUP of shard lines, not for one row
# (the three calibration cells share one block, and the file header is the block
# for the very first line). So a caption lifted from it is about the batch unless
# it happens to name the shard.
SEPARATOR_RE = re.compile(r"^#\s*(?:[-=*_~]{3,}|)\s*$")
# A new caption inside a block starts with a bare SHARDNAME: or a numbered range
# ("1-3 FIRST AND THEY ARE NOT NEGOTIABLE:"). Everything else on the following
# lines is the same sentence, hard-wrapped by hand at ~78 columns.
NEW_CAPTION_RE = re.compile(r"^(?:[A-Z][A-Z0-9_]{2,}\s*:|\d+[-–]\d+\s)")
NOTE_MAX_CHARS = 240


def _paragraph(lines: list[str], i: int) -> str:
    """The picked line PLUS its hand-wrapped continuations, joined verbatim.

    ⛔ WITHOUT THIS THE CAPTION IS A FRAGMENT. The worklist is wrapped by hand at
    ~78 columns, so `NEG125`'s own line ends "…as known-worse treatment vs v197 —
    the", and showing one line showed that. Joining adjacent lines is still pure
    selection — no word is added — and it stops at the next caption so one
    shard's note cannot annex the next shard's.
    """
    parts = [lines[i].lstrip("#").strip()]
    for l in lines[i + 1:]:
        t = l.lstrip("#").strip()
        if not t or NEW_CAPTION_RE.match(t):
            break
        parts.append(t)
    # A leading rule ("--- THE ATTRIBUTION ARMS. …") is punctuation the operator
    # used to separate batches, not a word. Dropping it leaves the sentence.
    text = re.sub(r"^[-=*_~\s]+", "", " ".join(p for p in parts if p))
    if len(text) > NOTE_MAX_CHARS:
        cut = text.rfind(" ", 0, NOTE_MAX_CHARS)
        text = text[:cut if cut > 0 else NOTE_MAX_CHARS].rstrip(" ,;-") + " …"
    return text


def worklist_note(shard: str, block: list[str]) -> dict | None:
    """One line of the operator's OWN prose to caption this shard in the list.

    ⛔ SELECTION, NEVER SUMMARY. Every character returned is copied verbatim out
    of `corefill_work.txt` with its leading `#` stripped. This page is forbidden
    from inventing an explanation of what an arm tests, and the worklist comment
    IS the richest explanation that exists, so the job is to CHOOSE a line, not
    to write one.

    Preference order, and why it is reported rather than hidden: a comment block
    sits above a GROUP of shard lines, so a line NAMING this shard is about this
    shard while the first prose line of a block is about the batch. `shard_named`
    tells the reader which of the two they got — a batch caption presented as a
    per-shard one would be a claim nobody made.
    """
    lines = [l for l in (block or []) if not SEPARATOR_RE.match(l)]
    if not lines:
        return None
    idx = next((i for i, l in enumerate(lines) if shard in l), None)
    text = _paragraph(lines, idx if idx is not None else 0)
    if not text:
        return None
    return {"text": text, "shard_named": idx is not None,
            "block_lines": len(block or [])}


def shard_map_set(shard: str) -> dict:
    """Which map pool this shard actually played, decided FROM ITS OWN ROWS.

    `label` is one of "live pool", "pre-rotation (<k> of <n> maps retired)",
    "MIXED", "unknown" — and `why` always names the evidence. "unknown" is a
    first-class verdict: a wrong label is worse than no label.
    """
    pools = map_pools()
    live, prev = pools["live"], pools["prev"]
    retired_pool = prev - live                       # e.g. atoll heart hive meander
    live_only_pool = live - prev                     # what the rotation added
    if retired_pool and prev:
        pre_label = (f"pre-rotation ({len(retired_pool)} of {len(prev)} "
                     f"maps retired)")
    else:
        pre_label = "pre-rotation (plays maps retired from the live pool)"

    p = OVERNIGHT / f"{shard}.tsv"
    res = {"label": "unknown", "why": "", "source": None, "maps": [],
           "retired_seen": [], "live_only_seen": [], "n_maps": 0,
           "first_row_at": None, "pool_src": pools["src"],
           "pool_blind": pools["blind"], "prev_pool_blind": pools["prev_blind"],
           "live_pool": sorted(live), "prev_pool": sorted(prev),
           "rotation_at": iso(ROTATION_AT), "rotation_commit": ROTATION_COMMIT}

    if pools["blind"]:
        res["why"] = ("LIVE POOL BLIND — " + pools["blind"]
                      + ". No map set can be labelled without it.")
        return res
    if not p.exists():
        res["why"] = f"no {p.name} — nothing to read a map column out of"
        return res
    try:
        raw = p.read_text(errors="replace").splitlines()
    except Exception as e:
        res["why"] = f"tsv unreadable: {type(e).__name__}: {e}"
        return res
    if not raw:
        res["why"] = "tsv is empty"
        return res
    header = raw[0].split("\t")
    if "map" not in header:                       # checked, never assumed
        res["why"] = ("tsv header has no `map` column (header: "
                      + " ".join(header) + ")")
        return res
    mi = header.index("map")
    ti = header.index("ts") if "ts" in header else None
    seen: set[str] = set()
    first_ts = None
    for row in raw[1:]:
        f = row.split("\t")
        if len(f) <= mi:
            continue
        seen.add(f[mi])
        if first_ts is None and ti is not None and len(f) > ti:
            first_ts = f[ti]
    res["maps"] = sorted(seen)
    res["n_maps"] = len(seen)
    res["first_row_at"] = first_ts
    if not seen:
        res["why"] = "tsv has a header but no data rows"
        return res
    res["source"] = "its own tsv rows"
    retired = sorted(seen - live)          # SAME definition corefill_status uses
    live_only = sorted(seen & live_only_pool)
    res["retired_seen"], res["live_only_seen"] = retired, live_only

    if retired and live_only:
        res["label"] = "MIXED"
        res["why"] = (f"rows name BOTH maps outside the live pool "
                      f"({', '.join(retired)}) and maps the rotation ADDED "
                      f"({', '.join(live_only)}) — this shard straddles the "
                      f"rotation and must not be pooled as either")
    elif retired:
        res["label"] = pre_label
        res["why"] = (f"rows name {len(retired)} map(s) that are NOT in the live "
                      f"pool: {', '.join(retired)} — {len(seen)} distinct maps in "
                      f"this tsv")
        if pools["prev_blind"]:
            res["why"] += (" · MIXED cannot be ruled out: " + pools["prev_blind"])
    elif live_only:
        res["label"] = "live pool"
        res["why"] = (f"every map in its rows is in the live pool, and "
                      f"{len(live_only)} of them exist only post-rotation "
                      f"({', '.join(live_only)}) — {len(seen)} distinct maps")
    else:
        # Every map it played survives in both pools. The rows cannot decide;
        # fall back to the clock and SAY SO — an inference, not a measurement.
        res["source"] = "launch time (rows are inconclusive)"
        t = parse_ts(first_ts or "")
        common = ", ".join(sorted(seen))
        if t is None:
            res["why"] = (f"rows name only maps that survive in both pools "
                          f"({common}) and the first row carries no parsable "
                          f"timestamp — UNDECIDED")
        elif t < ROTATION_AT:
            res["label"] = pre_label
            res["why"] = (f"INFERRED from launch time {first_ts} < rotation "
                          f"{iso(ROTATION_AT)} ({ROTATION_COMMIT}); its rows name "
                          f"only maps that survive in both pools ({common})")
        else:
            res["label"] = "live pool"
            res["why"] = (f"INFERRED from launch time {first_ts} >= rotation "
                          f"{iso(ROTATION_AT)} ({ROTATION_COMMIT}); its rows name "
                          f"only maps that survive in both pools ({common})")
    return res


def _file_facts(p: Path) -> dict:
    try:
        rel = str(p.relative_to(ROOT))
    except Exception:
        rel = str(p)
    try:
        st = p.stat()
    except Exception:
        return {"exists": False, "path": rel}
    m = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
    return {"exists": True, "path": rel, "bytes": st.st_size,
            "at": iso(m), "age_min": round(age_min(m), 1)}


def collect_shard_list() -> dict:
    """Every local battery shard: the tool's rows, plus artefacts it does not cover.

    ⛔ TWO POPULATIONS, NAMED SEPARATELY, BECAUSE THEY ARE NOT THE SAME SET.
    `corefill_status.sh` iterates the WORKLIST. Seven shards on disk have artefacts
    and no worklist line (their lines were replaced by later batches), so the
    authority reports NOTHING for them — and this page therefore prints no state,
    no rows and no rate for them either. Inventing those numbers here is exactly
    the re-implementation this file is forbidden to do, so they get their own
    section and their raw artefacts, nothing more.
    """
    st = collect_shard_text()
    wl = load_worklist()
    rows = parse_shard_table(st.get("text")) if st.get("text") else []
    known = {r["shard"] for r in rows}
    for r in rows:
        w = wl["shards"].get(r["shard"], {})
        r["tests"] = w.get("tests")
        r["worklist_line"] = w.get("line")
        # ⭐ The worklist's OWN prose, carried to the list view. Before this the
        # list rendered seven columns of numbers and no word about what any arm
        # tested — `tests` was in this payload and shown nowhere, so answering
        # "what is this one?" cost 79 page loads. Passthrough only: no field
        # below is computed, scored or paraphrased here.
        r["worklist_lineno"] = w.get("lineno")
        r["treatment"], r["control"] = w.get("treatment"), w.get("control")
        # ⭐ WHAT OPPONENT EACH SHARD RUNS AGAINST, AND WHETHER EITHER TREE IS A
        # BOT WE ACTUALLY SUBMITTED. The worklist names two directories and stops
        # there, so "is this arm being measured against the bot on the ladder?"
        # was unanswerable from this page. `matches.tree_label` is the ONE
        # implementation (ledger + PROGRAMME.md INCUMBENT); an unledgered tree
        # comes back with `versions: []` and renders as its bare path.
        r["treatment_ver"] = matches.tree_label(r["treatment"])
        r["control_ver"] = matches.tree_label(r["control"])
        r["target"], r["seed_lo"] = w.get("target"), w.get("seed_lo")
        r["comment_block"] = w.get("comment_block") or []
        r["note"] = worklist_note(r["shard"], w.get("comment_block") or [])
    orphans = []
    try:
        on_disk = sorted({p.name.split(".")[0] for p in OVERNIGHT.glob("*.heartbeat")}
                         | {p.name for p in STARTED.glob("*")})
    except Exception as e:
        on_disk = []
        orphans_blind = f"{type(e).__name__}: {e}"
    else:
        orphans_blind = None
    for sh in on_disk:
        if sh in known:
            continue
        hb = OVERNIGHT / f"{sh}.heartbeat"
        line = ""
        try:
            line = hb.read_text(errors="replace").strip()
        except Exception:
            pass
        orphans.append({"shard": sh, "heartbeat_line": line,
                        "heartbeat": _file_facts(hb)})
    return {"ok": st.get("ok", False), "pending": st.get("pending", False),
            "error": st.get("error"), "note": st.get("note"),
            # TWO CLOCKS, AND THEY ARE NOT THE SAME ONE. `served_at` is when this
            # reply was built; `at` is when corefill_status.sh last ran. A page
            # that shows only the first looks live while quoting a capture that
            # may be minutes old — the ship_watch defect, in a browser.
            "served_at": iso(now_utc()),
            "at": st.get("at"), "age_min": st.get("age_min"),
            "cadence_min": st.get("cadence_min"),
            "source": "tools/corefill_status.sh (verbatim output, parsed)",
            "worklist": {"path": wl["path"], "ok": wl["ok"], "at": wl.get("at"),
                         "age_min": wl.get("age_min"), "blind": wl.get("blind"),
                         "n": len(wl["order"])},
            "rows": rows, "n_rows": len(rows),
            "orphans": orphans, "n_orphans": len(orphans),
            "orphans_blind": orphans_blind,
            "text": st.get("text")}


def collect_shard_detail(shard: str) -> dict:
    """One shard. Status fields come from the tool; everything else is an artefact."""
    st = collect_shard_text()
    wl = load_worklist()
    rows = parse_shard_rows(st.get("text")) if st.get("text") else {}
    row = rows.get(shard)
    hb = OVERNIGHT / f"{shard}.heartbeat"
    lg = OVERNIGHT / f"{shard}.launch.log"
    tsv = OVERNIGHT / f"{shard}.tsv"
    done = OVERNIGHT / f"{shard}.COMPLETE"
    marker = STARTED / shard
    hb_line, done_line, marker_text = "", "", ""
    try:
        hb_line = hb.read_text(errors="replace").strip()
    except Exception:
        pass
    try:
        done_line = done.read_text(errors="replace").strip()
    except Exception:
        pass
    try:
        marker_text = marker.read_text(errors="replace").strip()
    except Exception:
        pass
    w = wl["shards"].get(shard)
    exists = bool(row or w or hb.exists() or tsv.exists() or marker.exists())
    return {
        "shard": shard,
        "exists": exists,
        "served_at": iso(now_utc()),
        # --- the authority ---------------------------------------------------
        "status": row,
        "status_source": "tools/corefill_status.sh",
        "status_at": st.get("at"), "status_age_min": st.get("age_min"),
        "status_cadence_min": st.get("cadence_min"),
        "status_pending": st.get("pending", False),
        "status_error": st.get("error"),
        "in_worklist": w is not None,
        "covered_by_status_tool": row is not None,
        # --- what defines it -------------------------------------------------
        "worklist": w, "worklist_path": wl["path"],
        "tests": (w or {}).get("tests"),
        # Same one implementation as the list view — see collect_shard_list.
        "treatment_ver": matches.tree_label((w or {}).get("treatment")),
        "control_ver": matches.tree_label((w or {}).get("control")),
        "note": worklist_note(shard, (w or {}).get("comment_block") or []),
        # --- artefacts -------------------------------------------------------
        "maps": shard_map_set(shard),
        "heartbeat": {**_file_facts(hb), "line": hb_line},
        "launch_log": {**_file_facts(lg), "tail": tail_lines(lg, 40)},
        "started_marker": {**_file_facts(marker), "text": marker_text},
        "complete_marker": {**_file_facts(done), "line": done_line},
        "tsv": _file_facts(tsv),
    }


def build_status() -> dict:
    lines = ps_lines()
    return {
        "served_at": iso(now_utc()),
        "repo": str(ROOT),
        "load": collect_load(),
        "procs": collect_procs(lines),
        "shards": collect_shard_summary(lines),
        "shard_text": collect_shard_text(),
        "holder": collect_holder(),
        "cores_idle": collect_cores_idle(),
        "ship_watch": collect_ship_watch(),
        "queue": collect_queue(),
    }


# ------------------------------------------------------------------- server

PAGES = {"/": "cores.html", "/cores": "cores.html",
         "/game": "game.html", "/lingo": "lingo.html",
         "/shards": "shards.html", "/shard": "shard.html",
         "/matches": "matches.html", "/match": "match.html"}
TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".js": "application/javascript; charset=utf-8"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):          # keep the terminal usable
        pass

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path, _, qs = self.path.partition("?")
        query = urllib.parse.parse_qs(qs)
        if path == "/api/status":
            body = json.dumps(build_status(), indent=1).encode()
            return self._send(200, body, "application/json; charset=utf-8")
        if path == "/api/matches":
            n = (query.get("limit") or ["100"])[0]
            lim = int(n) if n.isdigit() and 0 < int(n) <= 20000 else 100
            body = json.dumps(matches.collect_match_list(lim), indent=1).encode()
            return self._send(200, body, "application/json; charset=utf-8")
        if path == "/api/match":
            mid = (query.get("id") or [""])[0]
            # Platform match ids are uuids: no separators beyond `-`, no traversal.
            if not re.fullmatch(r"[0-9a-fA-F-]{8,64}", mid or ""):
                return self._send(400, json.dumps(
                    {"error": "bad or missing ?id= (expected a match uuid)"}).encode(),
                    "application/json; charset=utf-8")
            body = json.dumps(matches.collect_match_detail(mid), indent=1).encode()
            return self._send(200, body, "application/json; charset=utf-8")
        if path == "/api/shards":
            body = json.dumps(collect_shard_list(), indent=1).encode()
            return self._send(200, body, "application/json; charset=utf-8")
        if path == "/api/shard":
            sid = (query.get("id") or [""])[0]
            # Shard ids are worklist tokens: no separators, no traversal.
            if not re.fullmatch(r"[A-Za-z0-9_.\-]{1,64}", sid or ""):
                return self._send(400, json.dumps(
                    {"error": "bad or missing ?id="}).encode(),
                    "application/json; charset=utf-8")
            body = json.dumps(collect_shard_detail(sid), indent=1).encode()
            return self._send(200, body, "application/json; charset=utf-8")
        name = PAGES.get(path) or path.lstrip("/")
        target = (STATIC / name).resolve()
        if not str(target).startswith(str(STATIC)) or not target.is_file():
            return self._send(404, b"not found", "text/plain; charset=utf-8")
        ctype = TYPES.get(target.suffix, "application/octet-stream")
        return self._send(200, target.read_bytes(), ctype)


def main() -> int:
    # `tools/overnight_read.map_area_class` — the ONE implementation of the
    # CQ/STD/GRAND boundaries, which the match view reuses — resolves
    # `maps/<name>.map26` relative to the process cwd. Started from anywhere else
    # it returns UNK for every map, i.e. a whole column that silently means
    # nothing. Asserting the cwd is cheaper than a second copy of the boundaries,
    # and `matches.cwd_ok()` reports the condition on the page either way.
    os.chdir(ROOT)
    threading.Thread(target=_shard_worker, daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"CORE DASHBOARD  http://127.0.0.1:{PORT}")
    print(f"  shards  : http://127.0.0.1:{PORT}/shards")
    print(f"  matches : http://127.0.0.1:{PORT}/matches")
    print(f"  repo    : {ROOT}")
    print(f"  binds   : 127.0.0.1 only (not reachable from the network)")
    print(f"  reads   : files + `ps`. No fcode, no network, no writes.")
    print(f"  shard table refreshes every {SHARD_REFRESH_SEC}s via corefill_status.sh")
    print("  Ctrl-C to stop.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
