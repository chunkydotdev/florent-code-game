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
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATIC = Path(__file__).resolve().parent / "static"
PORT = int(os.environ.get("PORT", "8787"))

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


def collect_shard_text() -> dict:
    with _shard_lock:
        c = dict(_shard_cache)
    if c["at"] is None:
        return {"ok": False, "pending": True,
                "note": "corefill_status.sh has not completed its first run yet"}
    return {"ok": c["error"] is None, "text": c["text"], "error": c["error"],
            "at": iso(c["at"]), "age_min": round(age_min(c["at"]), 1),
            "cadence_min": SHARD_REFRESH_SEC / 60.0}


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
         "/game": "game.html", "/lingo": "lingo.html"}
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
        path = self.path.split("?", 1)[0]
        if path == "/api/status":
            body = json.dumps(build_status(), indent=1).encode()
            return self._send(200, body, "application/json; charset=utf-8")
        name = PAGES.get(path) or path.lstrip("/")
        target = (STATIC / name).resolve()
        if not str(target).startswith(str(STATIC)) or not target.is_file():
            return self._send(404, b"not found", "text/plain; charset=utf-8")
        ctype = TYPES.get(target.suffix, "application/octet-stream")
        return self._send(200, target.read_bytes(), ctype)


def main() -> int:
    threading.Thread(target=_shard_worker, daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"CORE DASHBOARD  http://127.0.0.1:{PORT}")
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
