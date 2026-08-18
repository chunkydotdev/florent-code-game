#!/usr/bin/env python3
"""FAILURE REEL — the list behind /reel and the local-replay viewer behind /reel_view.

Commissioned by Magnus, 2026-08-18: *"the failure reel must show up on a new page
in the dashboard so I can watch the replays later."* A build report names its
worst losses in prose and then they are gone; this makes them a durable,
watchable surface.

TWO JOBS, ONE REUSED IMPLEMENTATION EACH:

1. **The list.** `corpus/failure_reel.tsv` is an APPEND-ONLY manifest that BUILD
   AGENTS write (columns and the append convention are documented in that file's
   own `#` header — it is the authority, not this docstring). This module parses
   it, groups rows by `build` newest-first, and stamps every row with the age of
   its `ts` AND the age of the replay file it points at.

2. **The viewer.** `/reel_view?path=<repo-relative .replay26>` serves the SAME
   HTML `tools/replay_view.py generate_html()` writes for the CLI — imported, not
   re-derived, exactly as `tools/dash/replays.py` does for `/replay`. The reel's
   replays are LOCAL grid games (`<map>_s<seed>_<seat>.replay26`), which have no
   `<match>.meta.json`; `generate_html` already tolerates that (`load_meta`
   returns `(None, None)` for a non-match filename and `render_html` reads meta
   through `(meta or {})`), so no meta-less mode had to be added and no meta is
   SYNTHESISED. The manifest's build/arm/seat/cause instead ride in an injected
   banner above the board — the same `_inject_leg_banner` idiom `replays.py`
   uses, and for the same reason: it is dashboard-only context that must not be
   baked into the cache file the CLI shares.

⛔ THE HOUSE RULES, AND WHAT THEY COST HERE (see tools/dash/serve.py's docstring):

* **EVERY NUMBER CARRIES ITS AGE.** Each row reports `ts_age_min` (how old the
  banked observation is) and `replay_age_min` (how old the artefact is), and the
  page shows the manifest file's own mtime age. **But this file has NO CADENCE**
  — it is appended when a build finishes, not on a clock — so an old row is
  HISTORY, not STALENESS. Marking a three-day-old reel row STALE would be a
  false alarm, so ages here are DISCLOSURE and the page says so out loud. The
  one thing that IS alarmed: a row whose `ts` will not parse reports NO STAMP.
* **BLIND IS A STATE, NOT A ZERO.** A missing or unreadable manifest returns
  `source.ok = False` with the error, and the page renders BLIND. It never
  renders "0 failures", because "we banked nothing" and "we cannot read what we
  banked" are opposite facts.
* **NO RE-IMPLEMENTATION.** The narrative and the cause class are read off the
  manifest verbatim; nothing here re-derives a class, a rate or a verdict from
  the replays. This module does not even call `replay_view.peek_outcome` (which
  `replays.py` legitimately uses to label an un-narrated archive) — the outcome
  of a reel row is what the build agent wrote down, and a second, differently
  derived outcome beside it would be exactly the "two definitions" defect.
* **READ-ONLY, NO NETWORK.** Reads the manifest and the replay files; writes
  ONLY into `scratchpad/replay_view/` (rendered HTML cache). **Never into
  `replay_archive/`** — that tree belongs to the archiver.

⛔ SECURITY — `?path=` IS ATTACKER-SHAPED INPUT AND IS VALIDATED AS SUCH.
Unlike `/replay`, whose `?match=` is a uuid matched against a fixed regex and
joined to one fixed directory, `/reel_view` takes a PATH. `resolve_reel_path`
requires all of: non-empty, no NUL, not absolute, suffix exactly `.replay26`,
and — after `Path.resolve()`, so `..` segments and symlinks are collapsed FIRST
— still inside `ROOT`. A path that fails any of these is refused with a reason
and no filesystem read of the target ever happens. A path that passes but does
not exist is reported MISSING, which is a different answer from refused.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT / "tools"))
import replay_view  # noqa: E402  (generate_html, DEFAULT_OUT_DIR — the one implementation)

# Overridable so the BLIND path is testable against a second instance without
# touching the real manifest — same idiom as serve.py's COREFILL_WORK.
MANIFEST = Path(os.environ.get("FAILURE_REEL",
                               str(ROOT / "corpus" / "failure_reel.tsv")))

COLUMNS = ("ts", "build", "replay_path", "map", "seat", "arm",
           "cause_class", "narrative")
SUFFIX = ".replay26"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _age_min(then: datetime | None) -> float | None:
    if then is None:
        return None
    return (_now() - then).total_seconds() / 60.0


def _parse_ts(s: str) -> datetime | None:
    """Accept the documented `%Y-%m-%dT%H:%M:%SZ` and the wider ISO forms
    `datetime.fromisoformat` handles. Returns None rather than raising, so an
    unparseable stamp becomes a NO STAMP badge instead of a blind page."""
    s = (s or "").strip()
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


# ------------------------------------------------------------ path validation

def resolve_reel_path(rel: str) -> tuple[Path | None, str | None]:
    """(absolute Path inside ROOT, None) or (None, refusal reason).

    ⛔ Every branch here is a REFUSAL, not a sanitisation: nothing is stripped or
    rewritten to make a bad path good, because a rewriter is where traversal bugs
    live. `resolve()` runs BEFORE the containment test so `..` and symlinks are
    already collapsed when containment is decided. Existence is deliberately NOT
    checked here — a valid-but-absent path is MISSING (a manifest fact) and a
    refused path is a bad request; the caller must be able to tell them apart.
    """
    if not rel or not rel.strip():
        return None, "missing ?path="
    if "\x00" in rel:
        return None, "refused: NUL byte in path"
    p = Path(rel)
    if p.is_absolute():
        return None, "refused: absolute paths are not accepted — give a repo-relative path"
    if p.suffix != SUFFIX:
        return None, f"refused: path must end in {SUFFIX}"
    try:
        cand = (ROOT / p).resolve()
    except (OSError, RuntimeError) as e:
        return None, f"refused: unresolvable path ({type(e).__name__})"
    try:
        cand.relative_to(ROOT)
    except ValueError:
        return None, "refused: resolves outside the repo root"
    if cand.suffix != SUFFIX:                      # belt and braces after resolve()
        return None, f"refused: path must end in {SUFFIX}"
    return cand, None


# ------------------------------------------------------------------ the list

def _row_file_facts(rel: str) -> dict:
    """Existence + age of the replay a row points at. A row whose path is
    REFUSED is reported as refused, not as missing — the manifest carrying an
    unservable path is a different defect from the file having been deleted."""
    abspath, err = resolve_reel_path(rel)
    if err:
        return {"exists": False, "state": "REFUSED", "note": err,
                "bytes": None, "replay_age_min": None, "replay_mtime": None}
    try:
        st = abspath.stat()
    except FileNotFoundError:
        return {"exists": False, "state": "MISSING",
                "note": "no such file on disk (the row is kept — it is a banked observation)",
                "bytes": None, "replay_age_min": None, "replay_mtime": None}
    except OSError as e:
        return {"exists": False, "state": "UNREADABLE", "note": f"{type(e).__name__}: {e}",
                "bytes": None, "replay_age_min": None, "replay_mtime": None}
    mt = datetime.fromtimestamp(st.st_mtime, timezone.utc)
    return {"exists": True, "state": "OK", "note": "",
            "bytes": st.st_size, "replay_mtime": _iso(mt),
            "replay_age_min": _age_min(mt)}


def collect_reel() -> dict:
    """The whole page payload. Never raises; a failure becomes `source.ok=False`."""
    out: dict = {
        "served_at": _iso(_now()),
        "manifest": str(MANIFEST) if not str(MANIFEST).startswith(str(ROOT))
                    else str(MANIFEST.relative_to(ROOT)),
        "columns": list(COLUMNS),
        # There is no refresh cadence for an append-only ledger. Said explicitly
        # so the page does not have to invent one to draw a freshness badge.
        "cadence_min": None,
        "cadence_note": ("append-only ledger, written when a build finishes — it has NO "
                         "cadence, so an old row is HISTORY, not staleness. Ages below are "
                         "disclosure, not an alarm."),
        "source": {"ok": False, "error": None, "mtime": None, "age_min": None},
        "builds": [], "n_rows": 0, "n_malformed": 0, "n_missing": 0,
        "malformed": [],
    }
    try:
        st = MANIFEST.stat()
        text = MANIFEST.read_text(errors="replace")
    except Exception as e:
        out["source"]["error"] = f"cannot read {out['manifest']}: {type(e).__name__}: {e}"
        return out
    mt = datetime.fromtimestamp(st.st_mtime, timezone.utc)
    out["source"].update({"ok": True, "mtime": _iso(mt), "age_min": _age_min(mt),
                          "bytes": st.st_size})

    rows: list[dict] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != len(COLUMNS):
            out["malformed"].append({"line": lineno, "n_fields": len(parts),
                                     "expected": len(COLUMNS), "raw": line[:400]})
            continue
        r = dict(zip(COLUMNS, parts))
        r["line"] = lineno
        ts = _parse_ts(r["ts"])
        r["ts_ok"] = ts is not None
        r["ts_age_min"] = _age_min(ts)
        r["ts_sort"] = ts.timestamp() if ts else 0.0
        r.update(_row_file_facts(r["replay_path"]))
        r["watch_url"] = "/reel_view?path=" + _quote(r["replay_path"])
        rows.append(r)

    out["n_rows"] = len(rows)
    out["n_malformed"] = len(out["malformed"])
    out["n_missing"] = sum(1 for r in rows if not r["exists"])

    groups: dict[str, list[dict]] = {}
    for r in rows:
        groups.setdefault(r["build"], []).append(r)
    builds = []
    for build, rs in groups.items():
        rs.sort(key=lambda r: (-r["ts_sort"], r["line"]))
        newest = max((r for r in rs if r["ts_ok"]), key=lambda r: r["ts_sort"], default=None)
        builds.append({
            "build": build, "n": len(rs),
            "n_missing": sum(1 for r in rs if not r["exists"]),
            "newest_ts": newest["ts"] if newest else None,
            "newest_age_min": newest["ts_age_min"] if newest else None,
            "arms": sorted({r["arm"] for r in rs}),
            "causes": sorted({r["cause_class"] for r in rs}),
            "rows": rs,
        })
    builds.sort(key=lambda b: (-(b["rows"][0]["ts_sort"]), b["build"]))
    out["builds"] = builds
    return out


def _quote(s: str) -> str:
    import urllib.parse
    return urllib.parse.quote(s, safe="")


# ----------------------------------------------------------------- the viewer

def _esc_html(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def manifest_row_for(rel: str) -> dict | None:
    """The FIRST manifest row whose `replay_path` is this one, for the banner.
    Read fresh on every serve (never cached with the HTML) for the same reason
    replays.py re-reads its leg ledger: the manifest can grow after a render."""
    try:
        text = MANIFEST.read_text(errors="replace")
    except Exception:
        return None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != len(COLUMNS):
            continue
        r = dict(zip(COLUMNS, parts))
        if r["replay_path"] == rel:
            return r
    return None


def _inject_reel_banner(html: str, rel: str) -> str:
    """Stamp the manifest's own words above the board.

    ⭐ WHY A BANNER AND NOT A SYNTHESISED `meta` DICT: the meta panel is where the
    viewer states WHO PLAYED, and the manifest knows only OUR arm and OUR seat —
    it carries no opponent label. Filling `teamAName`/`teamBName` from it would
    put a half-invented matchup into the field a reader trusts for identity.
    The banner says exactly what we know and names the seat that was ours; Team
    A/B in the viewer stay whatever the replay itself says.
    """
    r = manifest_row_for(rel)
    if not r:
        head = (f"FAILURE REEL — local replay <code>{_esc_html(rel)}</code>. "
                "No manifest row matches this path, so no build/cause context is "
                "available; nothing below is annotated.")
    else:
        head = (
            f"FAILURE REEL — build <b>{_esc_html(r['build'])}</b> · arm "
            f"<b>{_esc_html(r['arm'])}</b> · map <b>{_esc_html(r['map'])}</b> · "
            f"WE PLAYED SEAT <b>{_esc_html(r['seat'])}</b> · cause "
            f"<b>{_esc_html(r['cause_class'])}</b> · banked {_esc_html(r['ts'])}"
            f"<div style=\"font-weight:400;margin-top:6px;max-width:100ch\">"
            f"{_esc_html(r['narrative'])}</div>"
            f"<div style=\"font-weight:400;margin-top:6px;opacity:.8\">"
            f"This is a LOCAL grid replay with no <code>meta.json</code>, so the "
            f"viewer's team names are blank — seat <b>{_esc_html(r['seat'])}</b> "
            f"above is which side was ours.</div>"
        )
    banner = (
        '<div id="reelBanner" style="position:sticky;top:0;z-index:9999;'
        'background:#2a1030;color:#f0c8ff;border-bottom:2px solid #c07ae0;'
        'font:600 13px/1.5 -apple-system,Segoe UI,sans-serif;padding:10px 16px;">'
        + head + "</div>"
    )
    if "<body>" in html:
        return html.replace("<body>", "<body>\n" + banner, 1)
    return banner + html  # defensive fallback if generate_html's shape ever changes


def _cache_path(rel: str) -> Path:
    """`scratchpad/replay_view/reel_<sha1[:16]>.html` — replay_view's OWN output
    dir, shared with the CLI and with /replay, but a DISTINCT name scheme so a
    reel render can never collide with or overwrite a `<match>_game_<n>.html`
    the CLI wrote. Hashed because the key is a path with separators in it."""
    h = hashlib.sha1(rel.encode()).hexdigest()[:16]
    return replay_view.DEFAULT_OUT_DIR / f"reel_{h}.html"


def get_or_build_reel_view(rel: str) -> tuple[bytes | None, str | None]:
    """(html_bytes, None) or (None, error). See `resolve_reel_path` for the
    refusal rules — this function does no path arithmetic of its own."""
    abspath, err = resolve_reel_path(rel)
    if err:
        return None, err
    try:
        replay_mtime = abspath.stat().st_mtime
    except FileNotFoundError:
        return None, (f"MISSING: {rel} is a valid repo path but no such file exists — "
                      "the manifest row is kept, the artefact is gone")
    except OSError as e:
        return None, f"unreadable: {type(e).__name__}: {e}"

    out_path = _cache_path(rel)
    try:
        if out_path.exists() and out_path.stat().st_mtime >= replay_mtime:
            return _inject_reel_banner(out_path.read_text(), rel).encode(), None
    except Exception:
        pass  # fall through and (re)generate

    try:
        html = replay_view.generate_html(abspath)
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html)     # cached WITHOUT the banner — see _inject_reel_banner
    except Exception:
        pass  # serve it anyway even if the cache write failed
    return _inject_reel_banner(html, rel).encode(), None


if __name__ == "__main__":                                    # tiny smoke read
    d = collect_reel()
    print(json.dumps({k: v for k, v in d.items() if k != "builds"}, indent=1))
    for b in d["builds"]:
        print(b["build"], b["n"], "rows,", b["n_missing"], "missing, newest",
              b["newest_ts"], b["causes"])
        for r in b["rows"]:
            print("   ", r["state"], r["map"], r["seat"], r["cause_class"],
                  r["replay_path"])
