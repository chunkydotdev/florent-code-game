#!/usr/bin/env python3
"""MATCH HISTORY — the list and per-match detail behind /matches and /match.

Commissioned by Magnus, 2026-08-13: *"put up the match history and tag the UR
games you've started? Add interesting stats on each match as well so I can go
through them."*

⛔ WHAT THIS FILE IS ALLOWED TO DO, AND THE FIVE THINGS IT IS NOT
================================================================

1. **PASSTHROUGH.** Every score, version, rating, elo delta, map, win condition
   and turn count below is a COLUMN in a file the keeper already writes. Nothing
   here recomputes one. The only arithmetic is per-match display math over the
   rows the detail page is already showing (how many of these 5 games ended on a
   core kill, the median of their turn counts, how many of these maps are CQ) —
   the ceiling the brief set, and deliberately below `tools/panel_read.py`, which
   owns pooled rates and bands and is pre-registered territory.

2. **NO WIN RATES ACROSS MATCHES.** Not one. The page tallies how many matches
   are ladder and how many are unrated because that is a count of ROWS SHOWN, not
   a rate; it never divides wins by games. `ladder_games.tsv` vs `meta_join` also
   fail in opposite directions on exactly that question (CLAUDE.md's two
   corpus-surface rules), so a denominator built here would be wrong in a way the
   page could not see.

3. **A MISSING NUMBER IS NEVER A ZERO.** A match whose replays have not been
   archived yet renders "not yet decoded (archiver cycle ~30 min)". A match the
   platform errored renders ERROR. Neither renders 0-5, and neither renders an
   empty aggregate table. This repo treats a false zero as its worst defect
   class, and the voided MAPCODE leg is precisely the shape that produces one:
   five matches that exist in a fire log, carry no score anywhere, and would
   otherwise show up as five clean 0-0 losses.

4. **A MATCH IS NEVER TAGGED AS OURS WITHOUT ITS ID IN A LOG.** The origin tag
   comes from an id-for-id match against `scratchpad/*_fires.tsv` (what a lane
   fired, one line per accepted challenge) or `corpus/our_matches.tsv` (what
   `unrated_run.sh` fired). Everything else unrated on our account is
   `other operator` — a teammate fires from the same team account, verified
   2026-08-13 — and that is a statement about OUR LOGS, not about them.

5. **ONE IMPLEMENTATION OF THE AREA CLASS.** `tools/overnight_read.map_area_class`
   reads each map's own `.map26` header; the CQ/STD/GRAND boundaries are not
   re-typed here. It resolves `maps/<name>.map26` RELATIVE TO THE PROCESS CWD, so
   `area_class()` below CHECKS the cwd and reports `cwd_ok: False` instead of
   quietly returning UNK for every map — a class column that is silently all-UNK
   looks like data.

WHAT THE SURFACES ACTUALLY COVER (measured 2026-08-13, not assumed)
-------------------------------------------------------------------
* `corpus/league_matches.tsv` — EVERY league match, all teams, match level, with
  ratings and elo deltas. **Ladder only:** of our 889 rows there, `meta_join`
  calls 0 anything but `ladder`. It has NO unrated match in it at all — none of
  the 28 ids in today's fire logs appear.
* `corpus/ladder_games.tsv` — per-game for our RATED matches, and it covers all
  889 (map / win condition / turns come off the platform's own match info, not
  off a decoded replay, which is why they are available long before the archive).
* `corpus/meta_join.tsv.gz` — per-game for ARCHIVED matches including unrated;
  our unrated history lives here and nowhere else. It lags the archiver's ~30 min
  cycle, so the newest fires are legitimately absent.
⇒ The list is the UNION keyed on match id, and every row says which surface each
  of its numbers came from.
"""
from __future__ import annotations

import csv
import gzip
import re
import statistics
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# The Loki ladder account. Same literal as tools/crash_census.py:109,
# tools/field_deaths.py:29, tools/leg_read.py:42 — this is the repo's team id,
# not a new one, and `assert_team_id()` below checks the corpus still knows it.
OUR_TEAM_ID = "379a5d80-9921-4c9e-949b-f9b1dcba16be"
OUR_TEAM_NAME = "OpenSverige"

# ⛔ THE BRIEF ASKED FOR AN `old-account` TAG ON A TEAM NAMED "OpenSverige (OLD)"
# AND THAT NAME OCCURS ZERO TIMES IN EITHER CORPUS SURFACE. Scanned every
# (name, id) pair in `league_matches.tsv` and `meta_join.tsv.gz`: exactly two
# teams carry an OpenSverige-ish name — ours, and `opensverige - plan B`. The
# "(OLD)" account is real (docs/coordination.md, 2026-08-13T09:1xZ: "the OLD
# account's separate window (OpenSverige (OLD) = teammate entity)") but has not
# appeared in an archived or league row yet.
#
# So the rule is written by NAME PATTERN, not by a hardcoded id list, and both
# outcomes are first class: the `old-account` tag fires the moment a "(OLD)" row
# lands, and today it fires zero times and the page says zero rather than
# implying the tag was checked and found nothing to check.
#
# ⛔⛔ AND `opensverige - plan B` IS **NOT** OURS AND IS **NOT** TAGGED
# `old-account`. Magnus, on the record (docs/coordination.md:26987): *"OpenSverige
# plan B is our friends' team, they have our code for Eir but not Loki."* Calling
# their 493 matches an old account of ours would be a fabricated claim about
# whose games these are, on a page built to answer exactly that question. They
# are a SEPARATE SCOPE, off by default, labelled with that quote.
ALT_ACCOUNTS = [
    {"id": None, "name_re": r"opensverige\s*\(old\)", "tag": "old-account",
     "label": "OpenSverige (OLD) — teammate entity firing from a separate account",
     "cite": "docs/coordination.md, 2026-08-13: "
             "'the OLD account's separate window (OpenSverige (OLD) = teammate entity)'"},
    {"id": "b7cafd9f-265f-4932-b8b2-f5ba80a6a5ba",
     "name_re": r"opensverige\s*-\s*plan\s*b", "tag": "friends-acct",
     "label": "opensverige - plan B — NOT ours",
     "cite": "Magnus, docs/coordination.md:26987: 'OpenSverige plan B is our "
             "friends' team, they have our code for Eir but not Loki, so they are "
             "building with that branch.'"},
]

# ---------------------------------------------------------------- fire logs
# Each accepted challenge writes one row: <ts>\t<cell>\t<verdict>\t<raw response>.
# The matchId is inside the raw response text, which is why it is parsed out with
# a regex rather than read from a column.
FIRE_ID_RE = re.compile(r'"matchId":\s*"([0-9a-fA-F-]{36})"')

FIRE_LOGS = [
    {"key": "cal-1", "tag": "cal-1",
     "path": ROOT / "scratchpad" / "panel_cal1_fires.tsv",
     "what": "PANEL-CAL-1 — the pinned six-cell calibration panel, FIRE ORDER #1"},
    {"key": "cal-2", "tag": "cal-2",
     "path": ROOT / "scratchpad" / "panel_cal2_fires.tsv",
     "what": "PANEL-CAL-2 — same panel, FIRE ORDER #2, incumbent v125 pinned per fire"},
    {"key": "leg-mapcode", "tag": "leg (voided: platform error)",
     "path": ROOT / "scratchpad" / "leg_mapcode_fires.tsv",
     "what": "MAPCODE leg (v124 / _v197mapcode) — five unrated matches vs team lazy",
     "void": {
         "status": "ERROR",
         "why": "all five matches errored in the PLATFORM runner after 30+ min "
                "queued — not passed, not fired: VOID",
         # ⭐ THIS CITATION IS CHECKED AT RUN TIME, NOT TRUSTED. A void status
         # hardcoded in a dashboard is a claim; `void_citation()` below greps the
         # doc for the id and the verdict and reports whether it is still there,
         # so a stale hardcode announces itself instead of outliving its evidence.
         "cite_file": "docs/coordination.md",
         "cite_id": "e68fcf8a",
         "cite_needle": "status=error",
         "cite_quote": "RESEARCH 2026-08-13T10:40:07Z — v124 LEG VOID: "
                       "`match info e68fcf8a` re-read: status=error, score 0-0",
     }},
]

# `unrated_run.sh` kept its own record of what it fired, with the arm tag. 42
# matches on 2026-08-11 — WITHOUT this they would all read `other operator`,
# which would be false about legs this repo ran itself.
OUR_MATCHES_TSV = ROOT / "corpus" / "our_matches.tsv"

LEAGUE_TSV = ROOT / "corpus" / "league_matches.tsv"
LADDER_TSV = ROOT / "corpus" / "ladder_games.tsv"
META_GZ = ROOT / "corpus" / "meta_join.tsv.gz"

# ---------------------------------------------------------- the version ledger
# ⭐ WHICH LOCAL TREE IS WHICH PLATFORM SUBMISSION. Nothing in this repo joined
# the two before 2026-08-13: `ladder_games.tsv.ourver` carries `125`, the shard
# worklist carries `bots/_v197mapcode`, and the sentence "those are the same bot"
# lived only in prose. `corpus/version_trees.tsv` is that join, seeded ONLY from
# written anchors, and this is the ONE place the dashboard reads it — the shard
# pages and the match page both call through here rather than each parsing it.
#
# ⛔ ABSENCE IS UNKNOWN, NOT UNLABELLED-BUT-GUESSABLE. A tree with no ledger row
# renders as its bare path. Inferring a version from a directory name (`_v197` ->
# "v197"?) would be a fabricated claim about what we shipped, on the page built
# to answer exactly that — and the numbers do not even coincide (`_v197mapcode`
# is submission v125).
VERSION_LEDGER = ROOT / "corpus" / "version_trees.tsv"
# `INCUMBENT` is read from PROGRAMME.md itself, per request (mtime-keyed, so a
# `submit_clean --activate` rewrite shows up on the next page load). NOT copied
# into this file: a second copy of the incumbent is the defect that left the real
# field stale across four consecutive ships.
PROGRAMME_MD = ROOT / "PROGRAMME.md"

# The archiver's own cycle. Stated on the page so `meta_join` absence reads as
# LAG rather than as "this match had no games".
ARCHIVER_CYCLE_MIN = 30

DEFAULT_LIMIT = 100
ALT_LIMIT = 25

# The tiebreak ladder, per CLAUDE.md: titanium_collected -> harvesters ->
# titanium_stored. A CLOSED set, written out so that `cond` values outside it
# (the engine also emits `error`) are counted as `other` instead of silently
# inflating the tiebreak count.
TIEBREAK_CONDS = ("titanium_collected", "harvesters", "titanium_stored")


# ------------------------------------------------------------------- helpers

def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def age_min(then: datetime | None) -> float | None:
    if then is None:
        return None
    return (now_utc() - then).total_seconds() / 60.0


def parse_iso(s: str | None) -> datetime | None:
    """Platform stamps: `2026-08-13T11:12:59.623Z` / `...:59Z` / `+00:00`.

    Returns None, never raises. Every consumer treats None as NO STAMP rather
    than as now().
    """
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    try:                                   # `2026-08-11T06:46:27.367282+00:00`
        return datetime.fromisoformat(s).astimezone(timezone.utc)
    except ValueError:
        return None


def file_facts(p: Path) -> dict:
    """Path, size and mtime — the CAPTURE clock, distinct from the newest row's.

    Both are reported everywhere because they answer different questions: the row
    stamp says how old the newest event is, the mtime says when the keeper last
    touched the file. A file rewritten 30 s ago whose newest row is 4 h old is a
    stalled feed, and only showing both makes that visible.
    """
    try:
        rel = str(p.relative_to(ROOT))
    except Exception:
        rel = str(p)
    try:
        st = p.stat()
    except Exception as e:
        return {"exists": False, "path": rel, "blind": f"{type(e).__name__}: {e}"}
    m = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
    return {"exists": True, "path": rel, "bytes": st.st_size,
            "at": iso(m), "age_min": round(age_min(m), 1)}


def _num(s: str | None) -> float | None:
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def _int(s: str | None) -> int | None:
    try:
        return int(str(s).strip())
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------- cached loaders
# The corpus files are rewritten by the keeper on its own cycle; re-parsing 41k
# league rows and 33k meta rows on every 10 s page refresh is wasteful, and a
# cache with no invalidation is the "stale but plausible" defect. Keyed on
# (mtime_ns, size), so an edit invalidates and a touch-free read does not.
_CACHE: dict[str, tuple] = {}
_LOCK = threading.Lock()


def _cached(path: Path, build):
    """(value, None) or (None, reason). Never raises, never returns a stale value."""
    try:
        st = path.stat()
        key = (st.st_mtime_ns, st.st_size)
    except Exception as e:
        with _LOCK:
            _CACHE.pop(str(path), None)
        return None, f"unreadable: {type(e).__name__}: {e}"
    with _LOCK:
        hit = _CACHE.get(str(path))
    if hit is not None and hit[0] == key:
        return hit[1], None
    try:
        val = build(path)
    except Exception as e:
        return None, f"parse failed: {type(e).__name__}: {e}"
    with _LOCK:
        _CACHE[str(path)] = (key, val)
    return val, None


def _rows(path: Path, opener=open):
    with opener(path, "rt", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def load_league() -> tuple[dict, str | None]:
    """match id -> the league row. ALL teams, so opponents' rows are here too."""
    def build(p):
        out = {}
        for r in _rows(p):
            if r.get("id"):
                out[r["id"]] = r
        return out
    return _cached(LEAGUE_TSV, build)


def load_ladder() -> tuple[dict, str | None]:
    """match id -> its per-game rows, in file order (game 1..5)."""
    def build(p):
        out: dict[str, list] = {}
        for r in _rows(p):
            out.setdefault(r["match"], []).append(r)
        return out
    return _cached(LADDER_TSV, build)


def load_meta() -> tuple[dict, str | None]:
    """match id -> its archived per-game rows."""
    def build(p):
        out: dict[str, list] = {}
        for r in _rows(p, opener=gzip.open):
            out.setdefault(r["match"], []).append(r)
        return out
    return _cached(META_GZ, build)


def load_version_ledger() -> tuple[dict, str | None]:
    """`corpus/version_trees.tsv`, indexed both ways. Passthrough, no inference.

    Returns {"by_tree": tree -> [row, ...], "by_version": version -> row, "n": k}.
    A tree may carry SEVERAL versions (`_v197mapcode` was submitted twice: v124 as
    an unrated leg, v125 as the ship), so `by_tree` is a list, newest version
    first. Comment lines (`#`) are the file's own header block and are skipped.
    """
    def build(p):
        by_tree: dict[str, list] = {}
        by_version: dict[str, dict] = {}
        hdr = None
        for raw in p.read_text(errors="replace").splitlines():
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            f = [c.strip() for c in raw.split("\t")]
            if hdr is None:
                hdr = f
                continue
            r = dict(zip(hdr, f))
            ver, tree = r.get("version", ""), r.get("tree", "")
            if not ver:
                continue
            rec = {"version": ver, "name": r.get("name") or None,
                   "tree": tree or None, "evidence": r.get("evidence") or None,
                   "recorded_at": r.get("recorded_at") or None}
            by_version[ver] = rec
            if tree:
                by_tree.setdefault(tree, []).append(rec)
        for rows in by_tree.values():
            rows.sort(key=lambda d: (_int(d["version"]) is None,
                                     -(_int(d["version"]) or 0), d["version"]))
        return {"by_tree": by_tree, "by_version": by_version,
                "n": len(by_version)}
    return _cached(VERSION_LEDGER, build)


def programme_incumbent() -> tuple[dict, str | None]:
    """PROGRAMME.md's INCUMBENT / PREVIOUS_INCUMBENT / INCUMBENT_FROZEN.

    Same four-space-indented `FIELD: value` shape `tools/gate.py:166` parses —
    that file is the enforcement authority and this is a read of the same block,
    not a second definition of what the incumbent is.
    """
    def build(p):
        fields = dict(re.findall(r"^\s{4}([A-Z_0-9]+):\s*(.+?)\s*$",
                                 p.read_text(errors="replace"), re.M))
        return {"incumbent": fields.get("INCUMBENT"),
                "previous": fields.get("PREVIOUS_INCUMBENT"),
                "frozen": fields.get("INCUMBENT_FROZEN")}
    return _cached(PROGRAMME_MD, build)


def _rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)


def tree_label(tree: str | None) -> dict | None:
    """What a bot tree IS: its platform submissions, and whether it is LIVE.

    `versions: []` means the ledger does not name this tree — rendered as the bare
    path. `incumbent` is a separate fact from a separate file (PROGRAMME.md), so an
    unledgered tree can still be flagged LIVE INCUMBENT without inventing a version.
    """
    if not tree:
        return None
    led, led_err = load_version_ledger()
    prog, prog_err = programme_incumbent()
    inc = (prog or {}).get("incumbent")
    return {
        "tree": tree,
        "versions": ((led or {}).get("by_tree", {}).get(tree) or []),
        "incumbent": bool(inc) and tree == inc,
        "ledger_path": _rel(VERSION_LEDGER),
        "ledger_blind": led_err,
        "incumbent_source": _rel(PROGRAMME_MD) + " INCUMBENT",
        "incumbent_blind": prog_err,
    }


def version_label(ver: str | None) -> dict | None:
    """The ledger row for a platform version number, or None if it names none."""
    if ver in (None, ""):
        return None
    led, _err = load_version_ledger()
    return ((led or {}).get("by_version", {}) or {}).get(str(ver).strip())


def load_fire_logs() -> dict:
    """match id -> which log fired it, which cell, and when.

    ⛔ ONE ROW OF A FIRE LOG IS NOT ONE MATCH. A rejected challenge writes a
    RATELIMIT/ERROR row with no `matchId` at all, so the ids are pulled out of the
    raw response text and rows without one are counted separately — reporting
    `fires: 13` for a log that produced 6 matches would misstate what we fired.
    """
    out = {"ids": {}, "logs": []}
    for spec in FIRE_LOGS:
        facts = file_facts(spec["path"])
        rec = {"key": spec["key"], "tag": spec["tag"], "what": spec["what"],
               "file": facts, "n_rows": 0, "n_ids": 0, "n_no_id": 0,
               "newest_fire_at": None, "newest_fire_age_min": None,
               "void": None, "blind": None}
        if spec.get("void"):
            rec["void"] = {k: v for k, v in spec["void"].items()}
            rec["void"]["citation"] = void_citation(spec["void"])
        try:
            lines = spec["path"].read_text(errors="replace").splitlines()
        except Exception as e:
            rec["blind"] = f"{type(e).__name__}: {e}"
            out["logs"].append(rec)
            continue
        newest = None
        for line in lines:
            if not line.strip():
                continue
            rec["n_rows"] += 1
            parts = line.split("\t")
            ts = parts[0].strip() if parts else ""
            cell = parts[1].strip() if len(parts) > 1 else ""
            verdict = parts[2].strip() if len(parts) > 2 else ""
            ids = FIRE_ID_RE.findall(line)
            t = parse_iso(ts)
            if t and (newest is None or t > newest):
                newest = t
            if not ids:
                rec["n_no_id"] += 1
                continue
            for mid in ids:
                rec["n_ids"] += 1
                out["ids"][mid] = {
                    "tag": spec["tag"], "key": spec["key"], "cell": cell,
                    "fired_at": ts, "verdict": verdict,
                    "log": rec["file"]["path"], "what": spec["what"],
                    "void": rec["void"],
                }
        rec["newest_fire_at"] = iso(newest) if newest else None
        rec["newest_fire_age_min"] = round(age_min(newest), 1) if newest else None
        out["logs"].append(rec)
    return out


def load_our_matches() -> dict:
    """`corpus/our_matches.tsv` — what `unrated_run.sh` recorded firing, by arm."""
    out = {"ids": {}, "file": file_facts(OUR_MATCHES_TSV), "n": 0, "blind": None,
           "newest_at": None, "newest_age_min": None}
    rows, err = _cached(OUR_MATCHES_TSV, _rows)
    if err:
        out["blind"] = err
        return out
    newest = None
    for r in rows or []:
        mid = (r.get("match_id") or "").strip()
        if not mid:
            continue
        out["n"] += 1
        t = parse_iso(r.get("created_at_utc"))
        if t and (newest is None or t > newest):
            newest = t
        out["ids"][mid] = {
            "tag": f"leg · {r.get('arm_tag') or 'untagged'}",
            "key": "our_matches",
            "cell": r.get("arm_tag") or "",
            "fired_at": r.get("created_at_utc") or "",
            "verdict": r.get("match_type") or "",
            "log": out["file"]["path"],
            "what": f"fired by {r.get('runner') or 'unknown runner'} "
                    f"(source={r.get('source') or 'unknown'}), arm "
                    f"{r.get('arm_tag') or 'untagged'}",
            "void": None,
        }
    out["newest_at"] = iso(newest) if newest else None
    out["newest_age_min"] = round(age_min(newest), 1) if newest else None
    return out


def void_citation(void: dict) -> dict:
    """Is the recorded void status still written down where it says it is?

    Greps `docs/coordination.md` for the leg's match id and checks the verdict
    string sits within a few lines of it. A hardcoded status that has outlived
    its source is exactly the kind of stale claim this dashboard exists to make
    visible, so the page prints `cited` or `CITATION NOT FOUND` rather than
    asserting the status unconditionally.
    """
    p = ROOT / void["cite_file"]
    res = {"file": void["cite_file"], "needle": void["cite_needle"],
           "id": void["cite_id"], "found": False, "line": None, "text": None,
           "blind": None}
    def build(path):
        lines = path.read_text(errors="replace").splitlines()
        return lines
    lines, err = _cached(p, build)
    if err:
        res["blind"] = err
        return res
    for i, line in enumerate(lines):
        if void["cite_id"] in line:
            window = "\n".join(lines[max(0, i - 2):i + 3])
            if void["cite_needle"] in window:
                res["found"] = True
                res["line"] = i + 1
                res["text"] = line.strip()[:220]
                return res
    return res


# ------------------------------------------------------------- the area class

_AREA_WARNED = {"cwd_ok": None}


def area_class(name: str | None) -> str | None:
    """CQ / STD / GRAND / UNK from `tools/overnight_read.map_area_class`.

    ⛔ ONE IMPLEMENTATION. The class boundaries are NOT re-typed here; the brief
    says so and the reason is that the boundaries moved once already (s36's
    three-class scheme) and a second copy would have kept the old ones.

    ⛔⛔ AND IT RESOLVES `maps/<name>.map26` AGAINST THE PROCESS CWD. Run from
    anywhere but the repo root it returns UNK for EVERY map — a column that is
    uniformly UNK looks exactly like data. `cwd_ok()` reports that condition and
    the page shows it, instead of the class column quietly meaning nothing.
    """
    if not name:
        return None
    try:
        if str(ROOT / "tools") not in sys.path:
            sys.path.insert(0, str(ROOT / "tools"))
        import overnight_read
        return overnight_read.map_area_class(name)
    except Exception:
        return "UNK"


def cwd_ok() -> dict:
    """Whether `map_area_class`'s relative `maps/` lookup can actually resolve."""
    here = Path.cwd().resolve()
    ok = (here / "maps").is_dir()
    return {"ok": bool(ok), "cwd": str(here),
            "why": None if ok else
                   f"process cwd is {here}, which has no maps/ directory — "
                   f"tools/overnight_read.map_area_class resolves "
                   f"maps/<name>.map26 relatively, so EVERY area class would "
                   f"read UNK. That is a blind column, not a measurement."}


def assert_team_id() -> dict:
    """Does the corpus still know the id this file calls ours? Cheap, and it
    would have caught a copy-paste of the wrong uuid — which produces an empty
    match history that looks like 'no matches played'."""
    league, err = load_league()
    if err:
        return {"ok": False, "blind": err}
    n = 0
    name = None
    for r in league.values():
        if r.get("teamAId") == OUR_TEAM_ID:
            n += 1
            name = r.get("teamAName")
        elif r.get("teamBId") == OUR_TEAM_ID:
            n += 1
            name = r.get("teamBName")
    return {"ok": n > 0, "id": OUR_TEAM_ID, "name_in_corpus": name,
            "n_league_matches": n,
            "blind": None if n else
                     f"{OUR_TEAM_ID} appears in 0 rows of "
                     f"{LEAGUE_TSV.name} — the team id is wrong or the file is empty"}


# ------------------------------------------------------------------ row build

def _alt_spec(team_name: str | None, team_id: str | None) -> dict | None:
    for spec in ALT_ACCOUNTS:
        if spec["id"] and team_id == spec["id"]:
            return spec
        if re.search(spec["name_re"], team_name or "", re.I):
            return spec
    return None


def _side_of(row_a_id: str, row_b_id: str, team_id: str) -> str | None:
    if row_a_id == team_id:
        return "a"
    if row_b_id == team_id:
        return "b"
    return None


def _league_row(r: dict, team_id: str) -> dict:
    """The league table's own columns, mapped onto us/them. No arithmetic."""
    side = _side_of(r.get("teamAId", ""), r.get("teamBId", ""), team_id)
    if side == "a":
        us, them = "A", "B"
    elif side == "b":
        us, them = "B", "A"
    else:
        us, them = None, None
    out = {"our_side": side}
    if us:
        out.update({
            "our_name": r.get(f"team{us}Name"), "our_ver": r.get(f"team{us}Version"),
            "opp_name": r.get(f"team{them}Name"), "opp_ver": r.get(f"team{them}Version"),
            "score_us": _int(r.get(f"score{us}")), "score_them": _int(r.get(f"score{them}")),
            "elo_delta": _num(r.get(f"eloDelta{us}")),
            "rating_before": _num(r.get(f"rating{us}Before")),
            "opp_rating_before": _num(r.get(f"rating{them}Before")),
        })
    win = (r.get("winnerId") or "").strip()
    if not win:
        out["result"] = "unknown"
        out["result_why"] = "league row carries no winnerId"
    elif win == team_id:
        out["result"] = "W"
        out["result_why"] = "league winnerId == this team's id"
    else:
        out["result"] = "L"
        out["result_why"] = "league winnerId is the other team's id"
    return out


def _meta_row(rows: list[dict], team_id: str) -> dict:
    """meta_join's match-level columns, mapped onto us/them.

    ⛔ THE KNOWN WARTS ARE HANDLED, NOT GUESSED AROUND. `us_side` is lowercase and
    EMPTY in old rows and `our_won` is unreliable in them, so `our_won` is never
    read and the result is derived from `match_winner_side` against `us_side` —
    and when `us_side` is empty the answer is "unknown", which is a verdict.
    """
    r = rows[0]
    us_side = (r.get("us_side") or "").strip().lower()
    if us_side not in ("a", "b"):
        # us_side is the wart; the ids are not, so fall back to them and SAY SO.
        by_id = _side_of(r.get("teamAId", ""), r.get("teamBId", ""), team_id)
        us_side = by_id or ""
        side_src = ("us_side column empty/none — side taken from teamAId/teamBId"
                    if by_id else "us_side empty and neither team id matches")
    else:
        side_src = "us_side column"
    if us_side == "a":
        us, them = "A", "B"
    elif us_side == "b":
        us, them = "B", "A"
    else:
        us, them = None, None
    out = {"our_side": us_side or None, "our_side_source": side_src,
           "type": (r.get("triggeredBy") or "").strip() or None,
           "completed_at": r.get("completedAt") or None}
    if us:
        out.update({
            "our_name": r.get(f"team{us}Name"), "our_ver": r.get(f"team{us}Version"),
            "opp_name": r.get(f"team{them}Name"), "opp_ver": r.get(f"team{them}Version"),
            "score_us": _int(r.get(f"score{us}")), "score_them": _int(r.get(f"score{them}")),
            "opp_rating_before": _num(r.get(f"rating{them}Before")),
        })
    mw = (r.get("match_winner_side") or "").strip().lower()
    if not us_side:
        out["result"], out["result_why"] = "unknown", (
            "our side is unknown for this match, so a winner side cannot be "
            "read as a win or a loss")
    elif mw not in ("a", "b"):
        out["result"], out["result_why"] = "unknown", (
            f"match_winner_side is {mw!r}, neither 'a' nor 'b'")
    else:
        out["result"] = "W" if mw == us_side else "L"
        out["result_why"] = f"match_winner_side={mw} vs us_side={us_side}"
    return out


def _origin(mid: str, mtype: str | None, fires: dict, ours: dict,
            alt: dict | None) -> dict:
    """Which log says we fired this — or, explicitly, that none does."""
    if alt:
        return {"tag": alt["tag"], "label": alt["label"], "cell": None,
                "fired_at": None, "source": "team identity, not a fire log",
                "cite": alt["cite"], "ours_fired": False, "void": None}
    hit = fires["ids"].get(mid) or ours["ids"].get(mid)
    if hit:
        return {"tag": hit["tag"], "label": hit["what"], "cell": hit["cell"],
                "fired_at": hit["fired_at"],
                "source": hit["log"], "cite": None, "ours_fired": True,
                "void": hit["void"]}
    if mtype == "ladder":
        return {"tag": None, "label": "ladder pairing — nobody fires these",
                "cell": None, "fired_at": None, "source": None, "cite": None,
                "ours_fired": False, "void": None}
    if mtype is None:
        return {"tag": "origin unknown", "label":
                "match type is unknown, so whether anyone here fired it is unknown",
                "cell": None, "fired_at": None, "source": None, "cite": None,
                "ours_fired": False, "void": None}
    return {"tag": "other operator",
            "label": "unrated on our account and in none of this box's fire logs "
                     "— a teammate fires from the same team account (verified "
                     "2026-08-13). This says what OUR logs contain, nothing about "
                     "theirs.",
            "cell": None, "fired_at": None, "source": None, "cite": None,
            "ours_fired": False, "void": None}


def build_row(mid: str, team_id: str, league: dict, meta: dict, ladder: dict,
              fires: dict, ours: dict, alt: dict | None) -> dict:
    lg = league.get(mid)
    mrows = meta.get(mid)
    lrows = ladder.get(mid)
    fired = fires["ids"].get(mid) or ours["ids"].get(mid)

    row = {"id": mid, "scope": "alt" if alt else "ours"}

    # --- type, and where the type came from -------------------------------
    if mrows:
        row["type"] = (mrows[0].get("triggeredBy") or "").strip() or None
        row["type_source"] = "meta_join.triggeredBy"
    elif lg:
        row["type"] = "ladder"
        row["type_source"] = ("present in league_matches.tsv, which is the league "
                              "ladder table (0 of our 889 rows there are anything "
                              "but ladder in meta_join)")
    elif fired:
        row["type"] = "unrated"
        row["type_source"] = f"fired by `fcode match unrated` per {fired['log']}"
    else:
        row["type"] = None
        row["type_source"] = "no surface names a type for this match"

    # --- identity / score / result ----------------------------------------
    if lg:
        row.update(_league_row(lg, team_id))
        row["created_at"] = lg.get("createdAt")
        row["score_source"] = "league_matches.tsv scoreA/scoreB"
        row["elo_source"] = "league_matches.tsv eloDeltaA/B + ratingABefore/BBefore"
    elif mrows:
        row.update(_meta_row(mrows, team_id))
        row["created_at"] = mrows[0].get("completedAt")
        row["created_is_completed"] = True
        row["score_source"] = "meta_join scoreA/scoreB"
        row["elo_source"] = None
    else:
        row["created_at"] = fired["fired_at"] if fired else None
        row["created_is_fired"] = True
        row["our_side"] = None
        row["score_us"] = row["score_them"] = None
        row["score_source"] = None
        row["result"] = "unknown"
        row["result_why"] = ("no league row and no archived rows — nothing "
                             "anywhere carries a score for this match")
        row["elo_source"] = None

    row.setdefault("elo_delta", None)
    row.setdefault("rating_before", None)
    row.setdefault("opp_rating_before", None)
    row.setdefault("our_name", None)
    row.setdefault("our_ver", None)
    row.setdefault("opp_name", None)
    row.setdefault("opp_ver", None)

    # ⭐ WHICH BUILD IS `ourver=125`? The corpus carries a bare integer and nothing
    # else; the ledger is the only surface that says it was named "Loki v8" and
    # built from `bots/_v197mapcode`. None when the ledger does not name it — a
    # version we cannot anchor renders as the number alone, never as a guess.
    row["our_ver_label"] = version_label(row.get("our_ver"))

    t = parse_iso(row.get("created_at"))
    row["created_age_min"] = round(age_min(t), 1) if t else None

    # --- origin tag --------------------------------------------------------
    row["origin"] = _origin(mid, row["type"], fires, ours, alt)

    # --- platform status ---------------------------------------------------
    # ⛔ THE VOIDED LEG MUST NOT RENDER AS 0-5, AND THE ONLY REASON IT CANNOT IS
    # THAT THE VOID IS CHECKED BEFORE THE SCORE. Its five matches carry no score
    # on any surface; a page that defaulted a missing score to 0 would print five
    # clean losses that never happened.
    void = row["origin"].get("void")
    if void:
        row["status"] = void["status"]
        row["status_note"] = void["why"]
        row["status_source"] = (f"{void['cite_file']}"
                                + (f":{void['citation']['line']}"
                                   if void.get("citation", {}).get("found") else
                                   " (CITATION NOT FOUND — see the sources panel)"))
        row["score_us"] = row["score_them"] = None
        row["result"] = "void"
        row["result_why"] = void["why"]
    elif row["score_us"] is None and row["score_them"] is None:
        row["status"] = "no score yet"
        row["status_note"] = (
            f"fired and accepted, but no surface carries a score yet — "
            f"meta_join lags the archiver's ~{ARCHIVER_CYCLE_MIN} min cycle")
        row["status_source"] = "absence from league_matches.tsv and meta_join"
    else:
        row["status"] = "complete"
        row["status_note"] = None
        row["status_source"] = row["score_source"]

    # --- how many per-game rows exist, and where -------------------------
    if lrows:
        row["games_rows"] = len(lrows)
        row["games_source"] = "ladder_games.tsv"
    elif mrows:
        row["games_rows"] = len(mrows)
        row["games_source"] = "meta_join.tsv.gz"
    else:
        row["games_rows"] = None       # NOT 0 — nothing has been read yet
        row["games_source"] = None
    return row


# ------------------------------------------------------------------ per-game

def _ladder_games(rows: list[dict]) -> list[dict]:
    """ladder_games.tsv rows, verbatim, plus the area class and the game number.

    The game number is parsed out of the `s3` replay filename (`<match>_game_N`),
    which is the only place it exists in this file; rows with no replay filename
    (the platform reported the game but no replay was produced) keep their file
    order and say the number is not stated rather than inventing one.
    """
    out = []
    for i, r in enumerate(rows, 1):
        m = re.search(r"_game_(\d+)\.replay26$", r.get("s3") or "")
        cond = (r.get("cond") or "").strip() or None
        turns = _int(r.get("turns"))
        won = (r.get("won") or "").strip()
        out.append({
            "n": _int(m.group(1)) if m else None,
            "n_fallback": i,
            "n_source": "s3 replay filename" if m else "file order (s3 is empty)",
            "map": r.get("map") or None,
            "area_class": area_class(r.get("map")),
            "winner": "us" if won == "1" else ("them" if won == "0" else "unknown"),
            "winner_source": "ladder_games.won",
            "winner_seat": (r.get("winner_seat") or "").strip() or None,
            "cond": cond,
            # ⛔ "kill round" ONLY when the core actually died. `turns` on a
            # tiebreak game is 1000 by construction, and labelling that a kill
            # round would put a fake 1000 into the median.
            "kill_round": turns if cond == "core_destroyed" else None,
            "turns": turns,
            "replay": (r.get("s3") or "").strip() or None,
            "source": "ladder_games.tsv",
        })
    return out


def _meta_games(rows: list[dict], us_side: str | None) -> list[dict]:
    """Archived per-game rows. Winner only — this surface carries no map/cond/turns.

    ⛔ `our_won` IS NOT READ. The repo records it as unreliable in old rows; the
    winner comes from `game_winner_side` against `us_side`, and where `us_side` is
    the empty/none wart the answer is "unknown". Guessing here would put a wrong
    W beside a real match id.
    """
    out = []
    for r in sorted(rows, key=lambda x: _int(x.get("game")) or 0):
        gw = (r.get("game_winner_side") or "").strip().lower()
        if not us_side or gw not in ("a", "b"):
            winner, why = "unknown", (
                f"game_winner_side={gw!r}, us_side={us_side!r}")
        else:
            winner, why = ("us" if gw == us_side else "them"), \
                          f"game_winner_side={gw} vs us_side={us_side}"
        out.append({
            "n": _int(r.get("game")), "n_fallback": None,
            "n_source": "meta_join.game",
            "map": None, "area_class": None,
            "winner": winner, "winner_source": why, "winner_seat": gw or None,
            "cond": None, "kill_round": None, "turns": None,
            "replay": r.get("file") or None,
            "source": "meta_join.tsv.gz",
        })
    return out


def aggregate(games: list[dict]) -> dict:
    """Display math over THESE rows only. Sums and one median. Nothing else.

    ⛔ THE CEILING IS THE BRIEF'S: simple sums and medians of the rows shown
    directly above them on the page. No rate, no band, no pooling across matches,
    no verdict. `tools/panel_read.py` owns pooled readouts and that is
    pre-registered territory; a second, unregistered pooling surface on a
    dashboard is how a number gets quoted with no prereg behind it.
    """
    n = len(games)
    kills = [g for g in games if g["cond"] == "core_destroyed"]
    known_cond = [g for g in games if g["cond"]]
    # ⛔ NOT EVERY NON-KILL IS A TIEBREAK. `cond` also takes the value `error`
    # (25 rows in ladder_games — the opponent's bot died and the game was awarded),
    # and a first version counted those five as five tiebreaks. The tiebreak
    # ladder is a NAMED, CLOSED set — titanium_collected -> harvesters ->
    # titanium_stored — so it is written out and anything else is `other`.
    ties = [g for g in known_cond if g["cond"] in TIEBREAK_CONDS]
    other = [g for g in known_cond
             if g["cond"] != "core_destroyed" and g["cond"] not in TIEBREAK_CONDS]
    krs = [g["kill_round"] for g in kills if g["kill_round"] is not None]
    classes: dict[str, int] = {}
    for g in games:
        if g["area_class"]:
            classes[g["area_class"]] = classes.get(g["area_class"], 0) + 1
    conds: dict[str, int] = {}
    for g in known_cond:
        conds[g["cond"]] = conds.get(g["cond"], 0) + 1
    won = sum(1 for g in games if g["winner"] == "us")
    lost = sum(1 for g in games if g["winner"] == "them")
    unk = sum(1 for g in games if g["winner"] == "unknown")
    return {
        "n_games": n,
        "won": won, "lost": lost, "winner_unknown": unk,
        # None, never 0, when the surface carries no win condition at all —
        # "0 kills" and "the column does not exist here" are different facts.
        "n_cond_known": len(known_cond),
        "kills": len(kills) if known_cond else None,
        "tiebreaks": len(ties) if known_cond else None,
        "other_cond": len(other) if known_cond else None,
        "cond_counts": conds or None,
        "median_kill_round": (round(statistics.median(krs), 1) if krs else None),
        "n_kill_rounds": len(krs),
        "maps_by_class": classes or None,
        "basis": (f"simple sums and one median over the {n} row(s) displayed "
                  f"above, and nothing else. No rate, no band, no pooling with "
                  f"any other match."),
    }


# ---------------------------------------------------------------- collectors

def _sources(fires: dict, ours: dict, league: dict, ladder: dict, meta: dict,
             league_err, ladder_err, meta_err) -> dict:
    def newest(rows_by_id, key, pick):
        best = None
        for v in rows_by_id.values():
            r = v[0] if isinstance(v, list) else v
            t = parse_iso(r.get(key))
            if t and (best is None or t > best):
                best = t
        return best
    lnew = newest(league, "createdAt", None) if league else None
    mnew = newest(meta, "completedAt", None) if meta else None
    dnew = newest(ladder, "created", None) if ladder else None
    def blk(path, err, n, nnew, cadence, what):
        f = file_facts(path)
        return {**f, "blind": err or f.get("blind"), "n_matches": n,
                "newest_row_at": iso(nnew) if nnew else None,
                "newest_row_age_min": round(age_min(nnew), 1) if nnew else None,
                "cadence_min": cadence, "what": what}
    return {
        "league_matches": blk(LEAGUE_TSV, league_err, len(league or {}), lnew, 20,
                              "every league match, all teams — ladder only; the "
                              "source of ratings, elo deltas and match scores"),
        "ladder_games": blk(LADDER_TSV, ladder_err, len(ladder or {}), dnew, 20,
                            "per-game rows for our RATED matches: map, win "
                            "condition, turns. Off the platform's match info, so "
                            "it does not wait for the archiver"),
        "meta_join": blk(META_GZ, meta_err, len(meta or {}), mnew,
                         ARCHIVER_CYCLE_MIN,
                         f"per-game rows for ARCHIVED matches incl. unrated. Lags "
                         f"the archiver's ~{ARCHIVER_CYCLE_MIN} min cycle — the "
                         f"newest fires are legitimately absent, which is LAG, "
                         f"not an empty match"),
        "fire_logs": fires["logs"],
        "our_matches": {**ours["file"], "n_matches": ours["n"],
                        "blind": ours["blind"],
                        "newest_row_at": ours["newest_at"],
                        "newest_row_age_min": ours["newest_age_min"],
                        "what": "what `unrated_run.sh` recorded firing, with the "
                                "arm tag it fired under"},
    }


def collect_match_list(limit: int = DEFAULT_LIMIT) -> dict:
    league, league_err = load_league()
    meta, meta_err = load_meta()
    ladder, ladder_err = load_ladder()
    league, meta, ladder = league or {}, meta or {}, ladder or {}
    fires = load_fire_logs()
    ours = load_our_matches()

    # --- the population, and it is a UNION of three surfaces ---------------
    ids_ours: set[str] = set()
    alt_of: dict[str, dict] = {}
    for mid, r in league.items():
        for nm, tid in ((r.get("teamAName"), r.get("teamAId")),
                        (r.get("teamBName"), r.get("teamBId"))):
            if tid == OUR_TEAM_ID:
                ids_ours.add(mid)
            else:
                spec = _alt_spec(nm, tid)
                if spec:
                    alt_of[mid] = spec
    for mid, rows in meta.items():
        r = rows[0]
        for nm, tid in ((r.get("teamAName"), r.get("teamAId")),
                        (r.get("teamBName"), r.get("teamBId"))):
            if tid == OUR_TEAM_ID:
                ids_ours.add(mid)
            else:
                spec = _alt_spec(nm, tid)
                if spec:
                    alt_of.setdefault(mid, spec)
    # Fired ids are OURS by construction — this box fired them — including the
    # ones no surface has yet (the voided leg has no row anywhere at all, so
    # without this it would vanish from the history entirely).
    ids_ours |= set(fires["ids"]) | set(ours["ids"])
    alt_ids = {m for m in alt_of if m not in ids_ours}

    # Every row is built ONCE. The tallies below count the full population and
    # the table shows the newest `limit` of it, so "17 cal-2" is a statement about
    # all our matches and not about the page's first screenful.
    all_mine = [build_row(m, OUR_TEAM_ID, league, meta, ladder, fires, ours, None)
                for m in sorted(ids_ours)]
    all_mine.sort(key=lambda r: (r.get("created_at") or ""), reverse=True)

    def _alt_team_id(mid: str, spec: dict) -> str:
        """The alt account's own id, read off the match rather than assumed —
        the "(OLD)" spec has no id at all, only a name pattern."""
        if spec.get("id"):
            return spec["id"]
        r = league.get(mid) or (meta.get(mid) or [{}])[0]
        for nm, tid in ((r.get("teamAName"), r.get("teamAId")),
                        (r.get("teamBName"), r.get("teamBId"))):
            if _alt_spec(nm, tid) is spec:
                return tid or ""
        return ""

    all_alt = [build_row(m, _alt_team_id(m, alt_of[m]), league, meta, ladder,
                         fires, ours, alt_of[m]) for m in sorted(alt_ids)]
    all_alt.sort(key=lambda r: (r.get("created_at") or ""), reverse=True)

    mine, n_mine = all_mine[:limit], len(all_mine)
    alt_rows, n_alt = all_alt[:min(limit, ALT_LIMIT)], len(all_alt)

    # --- tallies. COUNTS OF ROWS, never rates -----------------------------
    def tally(rows, key):
        t: dict[str, int] = {}
        for r in rows:
            k = key(r)
            if k:
                t[k] = t.get(k, 0) + 1
        return t
    by_type = tally(all_mine, lambda r: r["type"] or "type unknown")
    by_origin = tally(all_mine, lambda r: r["origin"]["tag"])
    by_origin["(ladder — nobody fires these)"] = sum(
        1 for r in all_mine if r["type"] == "ladder" and not r["origin"]["tag"])

    return {
        "served_at": iso(now_utc()),
        "our_team": {"id": OUR_TEAM_ID, "name": OUR_TEAM_NAME,
                     "check": assert_team_id()},
        "cwd": cwd_ok(),
        "limit": limit,
        "n_total": n_mine, "n_shown": len(mine),
        "n_alt_total": n_alt, "n_alt_shown": len(alt_rows),
        "by_type": by_type, "by_origin": by_origin,
        "rows": mine, "alt_rows": alt_rows,
        "alt_accounts": [{"tag": s["tag"], "label": s["label"], "cite": s["cite"],
                          "n_matches": sum(1 for m in alt_ids
                                           if alt_of[m]["tag"] == s["tag"])}
                         for s in ALT_ACCOUNTS],
        "sources": _sources(fires, ours, league, ladder, meta,
                            league_err, ladder_err, meta_err),
        "archiver_cycle_min": ARCHIVER_CYCLE_MIN,
    }


def collect_match_detail(mid: str) -> dict:
    league, league_err = load_league()
    meta, meta_err = load_meta()
    ladder, ladder_err = load_ladder()
    league, meta, ladder = league or {}, meta or {}, ladder or {}
    fires = load_fire_logs()
    ours = load_our_matches()

    lg = league.get(mid)
    mrows = meta.get(mid)
    src = lg or (mrows[0] if mrows else None)

    # Whose match is this? OURS wins outright — a match we played against a
    # sibling account is still ours, and reading it from the sibling's seat would
    # invert every W and L on the page.
    alt, team_id = None, OUR_TEAM_ID
    if src and OUR_TEAM_ID not in (src.get("teamAId"), src.get("teamBId")):
        for nm, tid in ((src.get("teamAName"), src.get("teamAId")),
                        (src.get("teamBName"), src.get("teamBId"))):
            spec = _alt_spec(nm, tid)
            if spec:
                alt, team_id = spec, (tid or "")
                break

    known = bool(lg or mrows or mid in fires["ids"] or mid in ours["ids"])
    if not known:
        return {"id": mid, "exists": False, "served_at": iso(now_utc()),
                "why": ("no row in league_matches.tsv, no archived rows in "
                        "meta_join, and no fire log on this box names it"),
                "sources": _sources(fires, ours, league, ladder, meta,
                                    league_err, ladder_err, meta_err)}

    row = build_row(mid, team_id, league, meta, ladder, fires, ours, alt)

    lrows = ladder.get(mid)
    games: list[dict] = []
    games_note = None
    if lrows:
        games = _ladder_games(lrows)
        games_source = {"file": "corpus/ladder_games.tsv",
                        "has": "map, win condition, turns, per-game winner",
                        "missing": None}
    elif mrows:
        games = _meta_games(mrows, row.get("our_side"))
        games_source = {
            "file": "corpus/meta_join.tsv.gz",
            "has": "per-game winner side",
            "missing": ("map, win condition and turns — meta_join does not carry "
                        "them, and ladder_games.tsv (which does) covers RATED "
                        "matches only. Not zero, not unknown-per-game: the "
                        "columns do not exist on this surface."),
        }
    else:
        games_source = None
        # ⛔ TWO DIFFERENT ABSENCES, AND COLLAPSING THEM WOULD BE A FALSE
        # PROMISE. "not yet decoded" says come back after the archiver's next
        # cycle; for a VOIDED match no cycle will ever produce rows, because the
        # platform runner errored and no games were played. Printing the first
        # sentence over the second would have this page tell the operator to wait
        # for data that cannot arrive.
        if row["origin"].get("void"):
            games_note = ("no games were played — the platform runner errored, so "
                          "there are no per-game rows to decode and there never "
                          "will be. This is not archiver lag.")
        else:
            games_note = (
                f"not yet decoded (archiver cycle ~{ARCHIVER_CYCLE_MIN} min). "
                f"No per-game rows exist for this match on any surface yet.")

    return {
        "id": mid, "exists": True, "served_at": iso(now_utc()),
        "cwd": cwd_ok(),
        "match": row,
        "games": games, "games_source": games_source, "games_note": games_note,
        "aggregates": aggregate(games) if games else None,
        "aggregates_note": (None if games else
                            "no per-game rows to sum — the page shows the reason "
                            "above instead of an empty table of zeros"),
        "archiver_cycle_min": ARCHIVER_CYCLE_MIN,
        "sources": _sources(fires, ours, league, ladder, meta,
                            league_err, ladder_err, meta_err),
    }


if __name__ == "__main__":                                   # tiny smoke read
    import json
    d = collect_match_list(5)
    print(json.dumps({k: v for k, v in d.items() if k != "rows"}, indent=1)[:2500])
    for r in d["rows"]:
        print(r["id"][:8], r["created_at"], r["type"], r["opp_name"],
              r["score_us"], r["score_them"], r["result"], r["origin"]["tag"])
