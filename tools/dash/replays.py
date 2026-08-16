#!/usr/bin/env python3
"""REPLAYS — the list behind /replays and the on-demand viewer behind /replay.

Wired in per Magnus, 2026-08-16: *"We have a dashboard, can you plug the
viewer in there?"* This module does two jobs and reuses one implementation
for each:

1. **The list.** `replay_archive/` holds one `.replay26` per game and one
   `<match_id>.meta.json` per MATCH (team names/versions/score — see
   tools/replay_view.py's `load_meta` for the exact shape). This file
   indexes that directory (background thread, `REFRESH_SEC` cadence — a
   full scan+parse of ~62k files takes ~2.5s measured 2026-08-16, too slow
   to do inline on a page load) and joins games under their match.

2. **The viewer.** `/replay?match=<id>&game=<n>` serves the SAME HTML
   `tools/replay_view.py generate_html()` writes for the CLI — imported, not
   re-derived — cached under `tools/replay_view.py`'s own default output
   dir (`scratchpad/replay_view/`) so the CLI and the dashboard share one
   cache and one on-disk name (`<match>_game_<n>.html`). Never written into
   `replay_archive/` — that directory is the archiver's, not this box's.

⛔ THIS PAGE, LIKE THE VIEWER IT SERVES, IS NOT AN INSTRUMENT. It lists and
draws replays for a human to click through; it computes no rate, no verdict,
and win/loss counts shown here are per-row facts (this game's winner), never
aggregated into anything that looks like a result. See replay_view.py's own
docstring for the longer version of this rule.

WHAT THIS DOES NOT DO, ON PURPOSE:
  * No win-rate, no aggregation across matches — `tools/dash/matches.py`
    already owns "our match history" with its team-identity and
    origin-tagging machinery; this page is a plain file browser over
    `replay_archive/`, agnostic to which side is "us". Team A/B is exactly
    what the replay and its meta.json say, nothing resolved onto "our_side".
  * No map NAME. The `.replay26` schema (tools/replay_schema.md) has no name
    field on `Map` — only width/height/rows/cores — so "map" here is the
    dimensions read straight off the replay, not a join against
    `corpus/league_maps.tsv` (a different, differently-scoped surface; CLAUDE.md's
    two-corpus-surface rule is about exactly this kind of silent scope
    mismatch).
  * No eager per-game decode. Winner/win_condition/turns for the rows a page
    actually shows are read with `replay_view.peek_outcome` — a cheap
    top-level-only read, NOT the full per-round walk `generate_html` does —
    and only for the (small) page of rows actually returned, cached by
    (path, mtime) so a 15s poll re-reads nothing.
"""
from __future__ import annotations

import json
import os
import re
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "replay_archive"

sys.path.insert(0, str(ROOT / "tools"))
import replay_view  # noqa: E402  (generate_html, peek_outcome, DEFAULT_OUT_DIR — the one implementation)

GAME_RE = re.compile(r"^([0-9a-fA-F-]{36})_game_(\d+)\.replay26$")
META_RE = re.compile(r"^([0-9a-fA-F-]{36})\.meta\.json$")

DEFAULT_LIMIT = 100
MAX_LIMIT = 2000


# ------------------------------------------------------------- leg ledger
# scratchpad/arm_fieldcal_<ARM>_<CELL>.txt (18+ files, may grow) are the leg's
# accept ledgers. Each line is `<team-uuid> <CLI-upgrade-noise>{"matchId":
# "<uuid>"}` — the noise before the JSON is not fixed-format (e.g. a version
# bump message), so match ids are pulled with a regex on the JSON key, never
# by splitting the line. Disclosure only: this map is used to ANNOTATE rows
# and the viewer, never to gate or hide anything (see docstring below and
# CLAUDE.md's disclose-not-prohibit instruction for this feature).
LEG_DIR = ROOT / "scratchpad"
LEG_FILE_RE = re.compile(r"^arm_fieldcal_(A|B)_(.+)\.txt$")
LEG_MATCHID_RE = re.compile(r'"matchId"\s*:\s*"([0-9a-fA-F-]{36})"')

_leg_cache: dict[str, dict] = {}
_leg_sig: tuple | None = None
_leg_lock = threading.Lock()


def _leg_ledger_files() -> list[Path]:
    try:
        return sorted(LEG_DIR.glob("arm_fieldcal_*.txt"))
    except Exception:
        return []


def _leg_ledger_signature(files: list[Path]) -> tuple:
    # Directory listing (names) + max mtime — cheap (dozens of small files)
    # and enough to notice both new ledger files and appended lines in
    # existing ones. Rebuilt lazily on each call against this signature
    # rather than pinned to REFRESH_SEC, so a freshly-appended accept shows
    # up on the very next page load instead of waiting out the replay
    # index's own cadence.
    names = tuple(f.name for f in files)
    mtimes = []
    for f in files:
        try:
            mtimes.append(f.stat().st_mtime)
        except Exception:
            pass
    return (names, max(mtimes) if mtimes else 0.0)


def _build_leg_index() -> dict[str, dict]:
    mapping: dict[str, dict] = {}
    for f in _leg_ledger_files():
        m = LEG_FILE_RE.match(f.name)
        if not m:
            continue
        arm, cell = m.group(1), m.group(2)
        try:
            text = f.read_text(errors="replace")
        except Exception:
            continue
        for mid in LEG_MATCHID_RE.findall(text):
            mapping[mid] = {"arm": arm, "cell": cell}
    return mapping


def leg_index() -> dict[str, dict]:
    """{match_id: {"arm": "A"|"B", "cell": <cell>}} — signature-cached."""
    global _leg_sig
    files = _leg_ledger_files()
    sig = _leg_ledger_signature(files)
    with _leg_lock:
        if sig == _leg_sig:
            return dict(_leg_cache)
    mapping = _build_leg_index()
    with _leg_lock:
        _leg_cache.clear()
        _leg_cache.update(mapping)
        _leg_sig = sig
    return dict(_leg_cache)


def leg_accept_for(match_id: str) -> dict | None:
    return leg_index().get(match_id)


LEG_DISCLOSURE_TMPL = (
    "⚠ LEG ACCEPT — LEG-fieldcal arm {arm}, cell {cell}, post-clock2. "
    "Viewing is allowed and useful; what it costs is ABSTENTION-BASED "
    "blindness: from this viewing on, amendments to this leg must be "
    "STRUCTURALLY blind or authored by someone who did not view. "
    "(Side-lane ruling e51babce.)"
)


def leg_disclosure_text(arm: str, cell: str) -> str:
    return LEG_DISCLOSURE_TMPL.format(arm=arm, cell=cell)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def age_min(then: datetime | None) -> float | None:
    if then is None:
        return None
    return (now_utc() - then).total_seconds() / 60.0


def parse_iso(s: str | None) -> datetime | None:
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(s).astimezone(timezone.utc)
    except ValueError:
        return None


# ------------------------------------------------------------- directory index
# A full scandir + json-parse of replay_archive/ (~62k entries, ~10.4k of them
# meta.json) measured at ~2.5s on 2026-08-16 — fine on a REFRESH_SEC background
# cadence, too slow to pay on every page load. Same shape as serve.py's shard
# cache: a lock-protected dict, a daemon thread, and the page reports the
# cache's own AGE rather than pretending the read is live.
REFRESH_SEC = 60
_index_cache = {"matches": {}, "at": None, "error": None, "building_ms": None}
_index_lock = threading.Lock()


def _build_index() -> None:
    t0 = time.time()
    matches: dict[str, dict] = {}
    try:
        with os.scandir(ARCHIVE) as it:
            for e in it:
                gm = GAME_RE.match(e.name)
                if gm:
                    mid, gi = gm.group(1), int(gm.group(2))
                    m = matches.setdefault(mid, {"games": {}, "meta": None,
                                                  "meta_error": None, "meta_mtime": None})
                    try:
                        st = e.stat()
                        m["games"][gi] = {"path": e.path, "mtime": st.st_mtime}
                    except Exception as ex:
                        m["games"][gi] = {"path": e.path, "mtime": None,
                                          "stat_error": f"{type(ex).__name__}: {ex}"}
                    continue
                mm = META_RE.match(e.name)
                if mm:
                    mid = mm.group(1)
                    m = matches.setdefault(mid, {"games": {}, "meta": None,
                                                  "meta_error": None, "meta_mtime": None})
                    try:
                        m["meta"] = json.loads(Path(e.path).read_text())
                        m["meta_mtime"] = e.stat().st_mtime
                    except Exception as ex:
                        m["meta_error"] = f"{type(ex).__name__}: {ex}"
    except Exception as e:
        with _index_lock:
            _index_cache.update(error=f"{type(e).__name__}: {e}", at=now_utc())
        return
    with _index_lock:
        _index_cache.update(matches=matches, at=now_utc(), error=None,
                            building_ms=round((time.time() - t0) * 1000))


def _index_worker() -> None:
    while True:
        _build_index()
        time.sleep(REFRESH_SEC)


# Started at import time, mirroring serve.py's `_shard_worker` — this fires
# the moment `import replays` runs in serve.py, so the SERVE PROCESS MUST BE
# RESTARTED to pick this module up at all; a hot page reload alone will not.
threading.Thread(target=_index_worker, daemon=True).start()


def index_status() -> dict:
    with _index_lock:
        c = dict(_index_cache)
    if c["at"] is None:
        return {"ok": False, "pending": True, "n_matches": 0,
                "note": f"first scan of {ARCHIVE.name}/ has not completed yet "
                        f"(~2.5s for ~62k files, measured 2026-08-16)"}
    return {"ok": c["error"] is None, "error": c["error"],
            "n_matches": len(c["matches"]), "at": iso(c["at"]),
            "age_min": round(age_min(c["at"]), 1), "cadence_min": REFRESH_SEC / 60.0,
            "build_ms": c["building_ms"]}


def _snapshot() -> dict:
    with _index_lock:
        return dict(_index_cache["matches"])


# --------------------------------------------------------------- peek cache
# One replay_view.peek_outcome() per (path, mtime) — cheap on its own
# (top-level fields + the map only, no per-round walk) but still real file
# I/O, and the same ~100 newest rows get re-requested every poll. Soft-capped
# so a long-running dashboard does not grow this without bound as the archive
# scrolls forward.
_peek_cache: dict[tuple[str, float], dict] = {}
_peek_lock = threading.Lock()
_PEEK_CAP = 20000


def _peek(path: str, mtime: float | None) -> dict:
    key = (path, mtime)
    with _peek_lock:
        hit = _peek_cache.get(key)
    if hit is not None:
        return hit
    try:
        val = replay_view.peek_outcome(Path(path))
        val["ok"] = True
    except Exception as e:
        val = {"ok": False, "error": f"{type(e).__name__}: {e}"}
    with _peek_lock:
        if len(_peek_cache) > _PEEK_CAP:
            for k in list(_peek_cache)[: _PEEK_CAP // 2]:
                _peek_cache.pop(k, None)
        _peek_cache[key] = val
    return val


# ------------------------------------------------------------------ row build

def _sort_key(mid: str, rec: dict) -> tuple:
    meta = rec.get("meta")
    if meta and meta.get("completedAt"):
        t = parse_iso(meta.get("completedAt"))
        if t:
            return (1, t)
    newest_game_mtime = max((g.get("mtime") or 0) for g in rec["games"].values()) \
        if rec["games"] else 0
    if newest_game_mtime:
        return (1, datetime.fromtimestamp(newest_game_mtime, tz=timezone.utc))
    if rec.get("meta_mtime"):
        return (1, datetime.fromtimestamp(rec["meta_mtime"], tz=timezone.utc))
    return (0, datetime.fromtimestamp(0, tz=timezone.utc))


def _row(mid: str, rec: dict, with_peek: bool) -> dict:
    meta = rec.get("meta")
    games = []
    for n in sorted(rec["games"]):
        g = rec["games"][n]
        gr = {"n": n, "exists": True, "peek": None}
        if with_peek and g.get("path") and g.get("mtime") is not None:
            gr["peek"] = _peek(g["path"], g["mtime"])
        games.append(gr)
    sk = _sort_key(mid, rec)
    row = {
        "id": mid,
        "meta_ok": meta is not None,
        "meta_error": rec.get("meta_error"),
        "teamAName": (meta or {}).get("teamAName"),
        "teamAVersion": (meta or {}).get("teamAVersion"),
        "teamBName": (meta or {}).get("teamBName"),
        "teamBVersion": (meta or {}).get("teamBVersion"),
        "scoreA": (meta or {}).get("scoreA"),
        "scoreB": (meta or {}).get("scoreB"),
        "triggeredBy": (meta or {}).get("triggeredBy"),
        "status": (meta or {}).get("status"),
        "completedAt": (meta or {}).get("completedAt"),
        "createdAt": (meta or {}).get("createdAt"),
        "sort_at": iso(sk[1]),
        "sort_source": "meta.completedAt" if (meta and meta.get("completedAt"))
                       else "newest game file mtime" if rec["games"]
                       else "meta.json file mtime" if rec.get("meta_mtime") else None,
        "n_games": len(rec["games"]),
        "games": games,
        "leg_accept": leg_accept_for(mid),
    }
    return row


def collect_replay_list(limit: int = DEFAULT_LIMIT, q: str = "") -> dict:
    status = index_status()
    matches = _snapshot()
    q = (q or "").strip().lower()

    def matches_q(mid: str, rec: dict) -> bool:
        if not q:
            return True
        if mid.lower().startswith(q):
            return True
        meta = rec.get("meta") or {}
        # Term-aware: split on whitespace; a `vNNN` term matches a team's
        # VERSION (meta stores bare ints), anything else substring-matches the
        # team NAME — and ALL terms must land on the SAME team, so
        # "opensverige v140" cannot pass by pairing our name with the
        # opponent's version. (Magnus, 2026-08-16: "how can I filter on v140
        # games so I can watch those?")
        terms = q.split()

        def team_hit(term: str, name, ver) -> bool:
            if len(term) > 1 and term[0] == "v" and term[1:].isdigit():
                return str(ver) == term[1:]
            return term in str(name or "").lower()

        for nk, vk in (("teamAName", "teamAVersion"),
                       ("teamBName", "teamBVersion")):
            if all(team_hit(t, meta.get(nk), meta.get(vk)) for t in terms):
                return True
        return False

    filtered = [(mid, rec) for mid, rec in matches.items() if matches_q(mid, rec)]
    filtered.sort(key=lambda kv: _sort_key(*kv), reverse=True)

    lim = max(1, min(MAX_LIMIT, limit))
    page = filtered[:lim]
    # Peeks (real file reads) only for the page actually returned, never for
    # the full filtered set — see module docstring.
    rows = [_row(mid, rec, with_peek=True) for mid, rec in page]

    return {
        "served_at": iso(now_utc()),
        "index": status,
        "n_total": len(matches),
        "n_matching": len(filtered),
        "n_shown": len(rows),
        "limit": lim,
        "q": q,
        "rows": rows,
        "archive": str(ARCHIVE.relative_to(ROOT)),
    }


# --------------------------------------------------------------- viewer route

MATCH_ID_RE = re.compile(r"^[0-9a-fA-F-]{36}$")


def resolve_game_path(match_id: str, game_n: int) -> Path | None:
    """The one replay file for this (match, game), from the live index.

    Falls back to a direct filename check if the background index has not
    completed its first scan yet, or has not caught a very recent archiver
    write — the index is a cache, not the ground truth, and a page load
    should not 404 just because the cache is a few seconds behind disk.
    """
    matches = _snapshot()
    rec = matches.get(match_id)
    if rec:
        g = rec["games"].get(game_n)
        if g and g.get("path"):
            p = Path(g["path"])
            if p.exists():
                return p
    direct = ARCHIVE / f"{match_id}_game_{game_n}.replay26"
    return direct if direct.exists() else None


def _esc_html(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def _inject_leg_banner(html: str, match_id: str) -> str:
    """Stamp the leg-accept disclosure ABOVE the board, computed fresh on
    every serve from the CURRENT leg ledger — never baked into the on-disk
    cache file (`get_or_build_view`'s out_path is the same file the CLI
    writes and reads via `tools/replay_view.py`; polluting it would (a) leak
    a dashboard-only banner into the CLI's own output and (b) go stale the
    moment a match is added to a ledger after the file was cached, since the
    cache's freshness check is keyed on the REPLAY's mtime, not the ledger's).
    Disclosure only — returns `html` unchanged for anything not in the
    ledger, and never refuses to render.
    """
    leg = leg_accept_for(match_id)
    if not leg:
        return html
    text = leg_disclosure_text(leg["arm"], leg["cell"])
    banner = (
        '<div id="legAcceptBanner" style="position:sticky;top:0;z-index:9999;'
        'background:#4a2a00;color:#ffd479;border-bottom:2px solid #ffb84d;'
        'font:600 13px/1.5 -apple-system,Segoe UI,sans-serif;padding:10px 16px;">'
        + _esc_html(text) + "</div>"
    )
    if "<body>" in html:
        return html.replace("<body>", "<body>\n" + banner, 1)
    return banner + html  # defensive fallback if generate_html's shape ever changes


def get_or_build_view(match_id: str, game_n: int) -> tuple[bytes | None, str | None]:
    """(html_bytes, None) or (None, error). Cache dir = replay_view's own
    DEFAULT_OUT_DIR (scratchpad/replay_view/), shared with the CLI, keyed on
    the exact same filename the CLI writes (`<match>_game_<n>.html`) — so a
    replay already viewed via the CLI is already warm here, and vice versa.
    NEVER cached inside replay_archive/ (that tree belongs to the archiver).

    The leg-accept banner (see `_inject_leg_banner`) is layered on AFTER the
    cache read/write, not written into the cached file itself — the cache is
    shared with the CLI and keyed on the replay's own mtime, neither of which
    should carry or gate a dashboard-only, ledger-driven disclosure.
    """
    if not MATCH_ID_RE.match(match_id or ""):
        return None, "bad match id"
    if not isinstance(game_n, int) or not (1 <= game_n <= 50):
        return None, "bad game number"
    replay_path = resolve_game_path(match_id, game_n)
    if replay_path is None:
        return None, (f"no replay file for match {match_id} game {game_n} in "
                      f"{ARCHIVE.relative_to(ROOT)}/ — it may not be archived yet")

    out_path = replay_view.DEFAULT_OUT_DIR / f"{replay_path.stem}.html"
    try:
        replay_mtime = replay_path.stat().st_mtime
        meta_path = replay_path.with_name(f"{match_id}.meta.json")
        meta_mtime = meta_path.stat().st_mtime if meta_path.exists() else 0
        newest_source = max(replay_mtime, meta_mtime)
        if out_path.exists() and out_path.stat().st_mtime >= newest_source:
            html = out_path.read_text()
            return _inject_leg_banner(html, match_id).encode(), None
    except Exception:
        pass  # fall through and (re)generate

    try:
        html = replay_view.generate_html(replay_path)
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html)  # cached WITHOUT the banner — see docstring
    except Exception:
        pass  # serve it anyway even if the cache write failed
    return _inject_leg_banner(html, match_id).encode(), None


if __name__ == "__main__":                                    # tiny smoke read
    _build_index()  # synchronous, for the smoke read only — the real server
                    # uses the background thread started at import time above.
    d = collect_replay_list(5)
    print(json.dumps({k: v for k, v in d.items() if k != "rows"}, indent=1))
    for r in d["rows"]:
        print(r["id"][:8], r["sort_at"], r["teamAName"], r["teamBName"],
              r["scoreA"], r["scoreB"], "games:", [g["n"] for g in r["games"]])
