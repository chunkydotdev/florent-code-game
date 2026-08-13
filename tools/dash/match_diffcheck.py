#!/usr/bin/env python3
"""MATCH DIFF CHECK — does /matches show what the TSVs say?

    .venv/bin/python tools/dash/match_diffcheck.py                 # against :8787
    .venv/bin/python tools/dash/match_diffcheck.py --port 8799
    .venv/bin/python tools/dash/match_diffcheck.py --selftest      # drive it to FAIL
    .venv/bin/python tools/dash/match_diffcheck.py --n 40          # sample size

⛔ WHY THIS FILE EXISTS. `tools/dash/matches.py` renders scores, versions,
ratings, elo deltas, maps, win conditions, turns and origin tags, and every one
of them is a COLUMN somebody else wrote. "I only parsed it" is a claim, not a
check — the sibling `shard_diffcheck.py` exists because the dashboard shipped
three disagreements with its own sources in one file.

===== THE COMPARISONS =====

A. STRICT — N random matches, re-read out of `corpus/league_matches.tsv`,
   `corpus/ladder_games.tsv` and `corpus/meta_join.tsv.gz` by an INDEPENDENT
   parser (plain `csv.reader` on positional indices, not the server's
   `DictReader` keyed on headers) and compared field by field against what
   `/api/match` serves. Different in the place TSV parsers actually break: header
   drift. If a column is renamed, the server's dict lookup goes None and this
   check's positional read does not — so they disagree, which is the point.

B. BRANCHES — the four cases the brief names, each driven on a REAL match id
   picked out of the live data, because each is a way the page can be wrong that
   a random sample will almost never hit:
     B1 a CAL-2 tagged match           -> origin tag `cal-2` + its panel cell
     B2 the voided leg                 -> ERROR, no score, `leg (voided…)` tag
     B3 an other-account match         -> tagged, and NOT counted as ours
     B4 a not-yet-decoded match        -> the explicit archiver line, no zeros
   ⛔ B2 IS THE ONE THAT MATTERS MOST. Those five matches have no score on any
   surface; a page that let a missing score default to 0 would print five clean
   0-5 losses that never happened, and it would look completely normal.

C. RENDER — the browser's own code, run over the served payload in node with a
   stub DOM, asserting the produced HTML contains ERROR / the tag / the archiver
   line. The API being right and the PAGE being right are different claims: every
   defect in B is reachable through a template that drops the field. Skipped as
   UNTESTED (never as passed) if node is absent.

D. NO-STATISTICS — the payload is scanned for the things this view is forbidden
   to compute: a win rate, a band, a pooled denominator across matches. The
   brief's S1 rule is a promise no amount of care enforces, so it is checked.

===== THE CHECK IS ITSELF AN INSTRUMENT, SO IT IS DRIVEN TO BOTH VERDICTS =====
`--selftest` corrupts one input per comparison and asserts that comparison
REPORTS A MISMATCH — including the case the live data cannot exercise (there is
no `OpenSverige (OLD)` row in the corpus today, so B3's `old-account` branch is
driven on an INJECTED row instead of being quietly counted as passed).

⛔ Read the printed VERDICT, not the exit code: a crash also exits non-zero and
means UNKNOWN, not FAIL. Exit 0 = pass, 1 = fail, 2 = unknown/not-run.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATIC = Path(__file__).resolve().parent / "static"
LEAGUE = ROOT / "corpus" / "league_matches.tsv"
LADDER = ROOT / "corpus" / "ladder_games.tsv"
META = ROOT / "corpus" / "meta_join.tsv.gz"

OUR = "379a5d80-9921-4c9e-949b-f9b1dcba16be"

# The four branch anchors the brief names. Ids are given where the brief gave
# them; everything else is DISCOVERED in the live data so this file does not rot
# into a list of uuids that no longer exist.
CAL2_ANCHOR = "b9f3fab5-483a-443c-a2a3-695d69a8e915"      # CAL-2 cell C1
VOID_ANCHOR = "e68fcf8a-746c-4db2-b2bb-9e43c6351e22"      # MAPCODE leg, fire1


# ------------------------------------------------------- independent parsers
# ⛔ POSITIONAL, NOT HEADER-KEYED. The server reads these files with
# csv.DictReader; importing that or copying it would compare a parser to itself,
# which is the "constant column validates anything" defect this repo names in its
# own standing rules. These read the header ONCE to find indices and then index
# by position, so a renamed column makes the two disagree instead of both going
# quietly None.

def _positional(path: Path, opener=open) -> tuple[list[str], list[list[str]]]:
    with opener(path, "rt", newline="") as fh:
        rows = list(csv.reader(fh, delimiter="\t"))
    if not rows:
        raise SystemExit(f"UNKNOWN: {path} is empty")
    return rows[0], rows[1:]


def league_by_id() -> dict[str, dict]:
    hdr, rows = _positional(LEAGUE)
    i = {n: hdr.index(n) for n in
         ("id", "createdAt", "teamAName", "teamAVersion", "teamBName",
          "teamBVersion", "scoreA", "scoreB", "winnerId", "teamAId", "teamBId",
          "ratingABefore", "ratingBBefore", "eloDeltaA", "eloDeltaB")}
    out = {}
    for r in rows:
        if len(r) <= max(i.values()):
            continue
        out[r[i["id"]]] = {k: r[v] for k, v in i.items()}
    return out


def ladder_by_match() -> dict[str, list[dict]]:
    hdr, rows = _positional(LADDER)
    i = {n: hdr.index(n) for n in
         ("match", "opp", "oppver", "ourver", "map", "won", "cond", "turns", "s3")}
    out: dict[str, list[dict]] = {}
    for r in rows:
        if len(r) <= max(i.values()):
            continue
        out.setdefault(r[i["match"]], []).append({k: r[v] for k, v in i.items()})
    return out


def meta_by_match() -> dict[str, list[dict]]:
    hdr, rows = _positional(META, opener=gzip.open)
    i = {n: hdr.index(n) for n in
         ("match", "game", "us_side", "teamAId", "teamAName", "teamAVersion",
          "teamBId", "teamBName", "teamBVersion", "match_winner_side",
          "game_winner_side", "scoreA", "scoreB", "triggeredBy", "completedAt")}
    out: dict[str, list[dict]] = {}
    for r in rows:
        if len(r) <= max(i.values()):
            continue
        out.setdefault(r[i["match"]], []).append({k: r[v] for k, v in i.items()})
    return out


def fired_ids() -> dict[str, tuple[str, str]]:
    """match id -> (log stem, cell), straight off the fire logs."""
    out = {}
    for p in sorted((ROOT / "scratchpad").glob("*_fires.tsv")):
        for line in p.read_text(errors="replace").splitlines():
            parts = line.split("\t")
            for mid in re.findall(r'"matchId":\s*"([0-9a-fA-F-]{36})"', line):
                out[mid] = (p.name, parts[1].strip() if len(parts) > 1 else "")
    return out


# ---------------------------------------------------------------------- http

def fetch(url: str):
    with urllib.request.urlopen(url, timeout=90) as r:
        return json.loads(r.read().decode())


def _f(x):
    return None if x in (None, "") else float(x)


def _i(x):
    try:
        return int(str(x).strip())
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------- comparison A

def expect_from_sources(mid: str, lg: dict, lad: dict, met: dict,
                        fired: dict) -> dict:
    """What the served row MUST say, derived only from the raw columns."""
    exp: dict = {}
    r = lg.get(mid)
    mrows = met.get(mid)
    if r:
        side = "a" if r["teamAId"] == OUR else ("b" if r["teamBId"] == OUR else None)
        us, them = ("A", "B") if side == "a" else (("B", "A") if side == "b" else (None, None))
        exp["created_at"] = r["createdAt"]
        if us:
            exp["our_ver"] = r[f"team{us}Version"]
            exp["opp_name"] = r[f"team{them}Name"]
            exp["opp_ver"] = r[f"team{them}Version"]
            exp["score_us"] = _i(r[f"score{us}"])
            exp["score_them"] = _i(r[f"score{them}"])
            exp["elo_delta"] = _f(r[f"eloDelta{us}"])
            exp["rating_before"] = _f(r[f"rating{us}Before"])
            exp["opp_rating_before"] = _f(r[f"rating{them}Before"])
        exp["result"] = ("W" if r["winnerId"] == (OUR if side else r["winnerId"])
                         else "L") if r["winnerId"] else "unknown"
        if side:
            exp["result"] = "W" if r["winnerId"] == OUR else "L"
        exp["type"] = "ladder"
    elif mrows:
        m0 = mrows[0]
        side = (m0["us_side"] or "").lower()
        if side not in ("a", "b"):
            side = "a" if m0["teamAId"] == OUR else ("b" if m0["teamBId"] == OUR else "")
        us, them = ("A", "B") if side == "a" else (("B", "A") if side == "b" else (None, None))
        exp["created_at"] = m0["completedAt"]
        exp["type"] = m0["triggeredBy"] or None
        if us:
            exp["our_ver"] = m0[f"team{us}Version"]
            exp["opp_name"] = m0[f"team{them}Name"]
            exp["opp_ver"] = m0[f"team{them}Version"]
            exp["score_us"] = _i(m0[f"score{us}"])
            exp["score_them"] = _i(m0[f"score{them}"])
        mw = (m0["match_winner_side"] or "").lower()
        exp["result"] = ("unknown" if (not side or mw not in ("a", "b"))
                         else ("W" if mw == side else "L"))
        exp["elo_delta"] = None
    else:
        exp["type"] = "unrated" if mid in fired else None
        exp["score_us"] = exp["score_them"] = None
        exp["elo_delta"] = None
    # per-game row count, from whichever surface carries them
    if lad.get(mid):
        exp["games_rows"] = len(lad[mid])
    elif mrows:
        exp["games_rows"] = len(mrows)
    else:
        exp["games_rows"] = None
    return exp


def cmp_row(mid: str, served: dict, exp: dict) -> list[str]:
    bad = []
    for k, want in exp.items():
        got = served.get(k)
        if isinstance(want, float) or isinstance(got, float):
            same = (want is None and got is None) or (
                want is not None and got is not None and abs(want - got) < 1e-9)
        else:
            same = (str(want) if want is not None else None) == \
                   (str(got) if got is not None else None)
        if not same:
            bad.append(f"{mid[:8]}.{k}: served {got!r} != source {want!r}")
    return bad


def cmp_games(mid: str, served: list[dict], lad: dict, met: dict) -> list[str]:
    """Per-game map / cond / turns against ladder_games, verbatim."""
    bad = []
    rows = lad.get(mid)
    if rows:
        if len(served) != len(rows):
            return [f"{mid[:8]}: served {len(served)} game rows, "
                    f"ladder_games has {len(rows)}"]
        for i, (s, r) in enumerate(zip(served, rows), 1):
            if (s.get("map") or "") != (r["map"] or ""):
                bad.append(f"{mid[:8]} g{i}.map: {s.get('map')!r} != {r['map']!r}")
            if (s.get("cond") or "") != (r["cond"] or ""):
                bad.append(f"{mid[:8]} g{i}.cond: {s.get('cond')!r} != {r['cond']!r}")
            if s.get("turns") != _i(r["turns"]):
                bad.append(f"{mid[:8]} g{i}.turns: {s.get('turns')!r} != {r['turns']!r}")
            want_w = "us" if r["won"] == "1" else ("them" if r["won"] == "0" else "unknown")
            if s.get("winner") != want_w:
                bad.append(f"{mid[:8]} g{i}.winner: {s.get('winner')!r} != {want_w!r}")
            # ⭐ "kill round" is a LABEL, and it must be attached only to a core
            # kill. A tiebreak game runs to 1000 turns by construction, so a
            # kill_round leaking out of one would put a fake 1000 in the median.
            want_kr = _i(r["turns"]) if r["cond"] == "core_destroyed" else None
            if s.get("kill_round") != want_kr:
                bad.append(f"{mid[:8]} g{i}.kill_round: {s.get('kill_round')!r} "
                           f"!= {want_kr!r} (cond={r['cond']!r})")
    elif met.get(mid):
        rows = met[mid]
        if len(served) != len(rows):
            bad.append(f"{mid[:8]}: served {len(served)} game rows, "
                       f"meta_join has {len(rows)}")
        for s in served:
            if s.get("map") is not None or s.get("cond") is not None:
                bad.append(f"{mid[:8]} g{s.get('n')}: meta_join carries no map or "
                           f"cond, yet the server served map={s.get('map')!r} "
                           f"cond={s.get('cond')!r}")
    elif served:
        bad.append(f"{mid[:8]}: no surface has per-game rows, yet the server "
                   f"served {len(served)} of them")
    return bad


def cmp_aggregates(mid: str, det: dict) -> list[str]:
    """Recompute the per-match display math from the SERVED game rows.

    This is the one place a second implementation is correct rather than
    forbidden: the rule is that no quantity an existing tool computes gets
    recomputed, and no tool computes these — they are display sums over the rows
    on the page, so the check is whether the sum matches the rows shown.
    """
    a = det.get("aggregates")
    games = det.get("games") or []
    bad = []
    if not games:
        if a is not None:
            bad.append(f"{mid[:8]}: no game rows, yet an aggregate block was served "
                       f"— that is the false-zero shape this view must not have")
        if not det.get("games_note"):
            bad.append(f"{mid[:8]}: no game rows AND no explanatory note — the "
                       f"reader is shown an unexplained emptiness")
        return bad
    if a is None:
        return [f"{mid[:8]}: {len(games)} game rows served with no aggregate"]
    want_n = len(games)
    won = sum(1 for g in games if g["winner"] == "us")
    lost = sum(1 for g in games if g["winner"] == "them")
    kills = [g for g in games if g["cond"] == "core_destroyed"]
    krs = sorted(g["kill_round"] for g in kills if g["kill_round"] is not None)
    med = None
    if krs:
        mid_i = len(krs) // 2
        med = float(krs[mid_i]) if len(krs) % 2 else (krs[mid_i - 1] + krs[mid_i]) / 2
    for k, want in (("n_games", want_n), ("won", won), ("lost", lost)):
        if a.get(k) != want:
            bad.append(f"{mid[:8]}.agg.{k}: {a.get(k)!r} != {want!r}")
    if a.get("median_kill_round") is None:
        if med is not None:
            bad.append(f"{mid[:8]}.agg.median_kill_round: served None, rows give {med}")
    elif med is None or abs(a["median_kill_round"] - med) > 0.051:
        bad.append(f"{mid[:8]}.agg.median_kill_round: {a['median_kill_round']} != {med}")
    if any(g["cond"] for g in games):
        if a.get("kills") != len(kills):
            bad.append(f"{mid[:8]}.agg.kills: {a.get('kills')!r} != {len(kills)!r}")
    else:
        # ⛔ NO COND COLUMN ON THIS SURFACE ⇒ None, NEVER 0. "no kills" and "the
        # column does not exist here" are different facts and only one of them is
        # true of an unrated match.
        if a.get("kills") is not None:
            bad.append(f"{mid[:8]}.agg.kills: served {a['kills']!r} where the "
                       f"surface carries no win condition at all — must be null")
    return bad


# --------------------------------------------------------------- comparison B
# ⛔ EACH BRANCH IS A FUNCTION SO THE SELFTEST CAN DRIVE *THE CHECK*, NOT A COPY
# OF ITS EXPECTATIONS. A first version asserted the mutation inline — `set status
# to complete, then assert status != ERROR` — which is a tautology that passes
# whatever the real check does. These are called once with the live payload and
# once with a corrupted one.

def check_cal2(mid: str, row: dict, fired: dict) -> list[str]:
    bad, o = [], (row.get("origin") or {})
    if o.get("tag") != "cal-2":
        bad.append(f"B1 {mid[:8]}: origin tag {o.get('tag')!r} != 'cal-2'")
    if mid in fired and o.get("cell") != fired[mid][1]:
        bad.append(f"B1 {mid[:8]}: cell {o.get('cell')!r} != fire log {fired[mid][1]!r}")
    if not o.get("ours_fired"):
        bad.append(f"B1 {mid[:8]}: fired by us per the log, served "
                   f"ours_fired={o.get('ours_fired')!r}")
    if row.get("type") != "unrated":
        bad.append(f"B1 {mid[:8]}: type {row.get('type')!r} != 'unrated'")
    return bad


def check_void(mid: str, row: dict, det: dict) -> list[str]:
    bad = []
    if row.get("status") != "ERROR":
        bad.append(f"B2 {mid[:8]}: status {row.get('status')!r} != 'ERROR'")
    if row.get("score_us") is not None or row.get("score_them") is not None:
        bad.append(f"B2 {mid[:8]}: served a score {row.get('score_us')}-"
                   f"{row.get('score_them')} for a match that has none on any "
                   f"surface — THE FALSE ZERO")
    if not str((row.get("origin") or {}).get("tag") or "").startswith("leg"):
        bad.append(f"B2 {mid[:8]}: origin tag "
                   f"{(row.get('origin') or {}).get('tag')!r} is not the leg tag")
    if det.get("games"):
        bad.append(f"B2 {mid[:8]}: served {len(det['games'])} game rows for a "
                   f"match the platform never ran")
    if det.get("aggregates") is not None:
        bad.append(f"B2 {mid[:8]}: served an aggregate block for a voided match")
    cit = ((row.get("origin") or {}).get("void") or {}).get("citation") or {}
    if not cit.get("found"):
        bad.append(f"B2 {mid[:8]}: the ERROR status is served with its citation "
                   f"NOT FOUND in the doc it names")
    return bad


def check_alt(alt: dict, ours_ids: set, alt_accounts: list) -> list[str]:
    bad, o = [], (alt.get("origin") or {})
    if not o.get("tag"):
        bad.append(f"B3 {alt['id'][:8]}: other-account row carries no tag")
    if o.get("ours_fired"):
        bad.append(f"B3 {alt['id'][:8]}: an other-account match is marked as "
                   f"fired by us")
    if alt["id"] in ours_ids:
        bad.append(f"B3 {alt['id'][:8]}: appears in OUR list as well as the "
                   f"other-account list")
    n_old = sum(1 for a in alt_accounts if a["tag"] == "old-account")
    if n_old != 1:
        bad.append(f"B3: the `old-account` tag is not defined in the payload "
                   f"({n_old} definitions) — the brief requires it to exist even "
                   f"at zero matches")
    return bad


def check_undecoded(mid: str, row: dict, det: dict) -> list[str]:
    bad, note = [], (det.get("games_note") or "")
    if "not yet decoded" not in note:
        bad.append(f"B4 {mid[:8]}: games_note {note[:60]!r} does not carry the "
                   f"explicit 'not yet decoded' line")
    if str(det.get("archiver_cycle_min")) not in note:
        bad.append(f"B4 {mid[:8]}: the archiver cycle is not stated in the note")
    if det.get("aggregates") is not None:
        bad.append(f"B4 {mid[:8]}: served aggregates for an undecoded match")
    if row.get("games_rows") == 0:
        bad.append(f"B4 {mid[:8]}: games_rows served as 0 — must be null, because "
                   f"nothing has been read, not zero games played")
    return bad


# --------------------------------------------------------------- comparison C

RENDER_HARNESS = r"""
import fs from 'fs'; import vm from 'vm';
const html = fs.readFileSync(process.argv[2],'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error('no <script> in ' + process.argv[2]); process.exit(3); }
const payload = JSON.parse(fs.readFileSync(process.argv[3],'utf8'));
const els = {};
function el(sel){ if(!els[sel]) els[sel]={sel,innerHTML:'',textContent:'',value:'',
                                         addEventListener(){}, dataset:{}}; return els[sel]; }
const ctx = { console, document:{querySelector:el},
  location:{search:'?id='+(process.argv[4]||''), href:''},
  URLSearchParams, fetch: async()=>({json:async()=>payload}),
  setInterval:()=>0, setTimeout:()=>0, encodeURIComponent };
ctx.window=ctx; ctx.globalThis=ctx;
vm.createContext(ctx);
vm.runInContext(m[1], ctx, {filename: process.argv[2]});
ctx.render(payload);
const out={}; for(const k of Object.keys(els)) out[k]=els[k].innerHTML||els[k].textContent;
console.log(JSON.stringify(out));
"""


def node_render(page: Path, payload: dict, mid: str = "") -> dict | None:
    """Run the page's OWN render() over `payload` in node with a stub DOM.

    The API can be right while the template drops the field, so the strings the
    brief demands (ERROR, the origin tag, the archiver line) are asserted against
    what the browser would actually build. Returns None when node is unavailable
    — reported UNTESTED, never counted as a pass.
    """
    node = shutil.which("node")
    if not node:
        return None
    tmp = Path(tempfile.mkdtemp(prefix="matchdiff-"))
    try:
        (tmp / "h.mjs").write_text(RENDER_HARNESS)
        (tmp / "p.json").write_text(json.dumps(payload))
        r = subprocess.run([node, str(tmp / "h.mjs"), str(page), str(tmp / "p.json"), mid],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            return {"__error__": (r.stderr or r.stdout).strip()[:600]}
        return json.loads(r.stdout)
    except Exception as e:
        return {"__error__": f"{type(e).__name__}: {e}"}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def render_contains(rendered: dict | None, needles: list[str]) -> list[str]:
    if rendered is None:
        return ["__untested__"]
    if "__error__" in rendered:
        return [f"render harness failed: {rendered['__error__']}"]
    blob = "\n".join(str(v) for v in rendered.values())
    return [f"rendered HTML does not contain {n!r}" for n in needles if n not in blob]


# --------------------------------------------------------------- comparison D

FORBIDDEN = [
    (re.compile(r"win[_ ]?rate", re.I), "a win rate"),
    (re.compile(r"\bband\b", re.I), "a confidence band"),
    (re.compile(r"\bpooled\b", re.I), "a pooled statistic"),
    (re.compile(r"\bp_?value\b|\bmde\b", re.I), "an inferential statistic"),
]
# Prose that NAMES the forbidden thing in order to say the page does not compute
# it is not the forbidden thing. Only VALUE positions are scanned; these keys
# hold explanatory text.
PROSE_KEYS = {"basis", "what", "why", "label", "note", "cite", "status_note",
              "result_why", "type_source", "score_source", "elo_source",
              "games_note", "aggregates_note", "blind", "n_source",
              "winner_source", "our_side_source", "status_source", "missing",
              "has", "quote", "cite_quote", "text"}


def scan_forbidden(obj, path="", out=None) -> list[str]:
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in PROSE_KEYS:
                continue
            scan_forbidden(v, f"{path}.{k}", out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:50]):
            scan_forbidden(v, f"{path}[{i}]", out)
    elif isinstance(obj, str):
        for rx, what in FORBIDDEN:
            if rx.search(obj):
                out.append(f"{path}: {what} appears in a value position: {obj[:90]!r}")
    return out


# -------------------------------------------------------------------- report

def report(title: str, what: str, bad: list[str], ok_line: str,
           untested: str | None = None) -> int:
    print(f"\n{title}")
    print(f"   {what}")
    if untested:
        print(f"   [UNTESTED] {untested}")
        print("   Not a pass.")
        return 0
    if bad:
        print(f"   [FAIL] {len(bad)} mismatch(es):")
        for b in bad[:25]:
            print(f"      - {b}")
        if len(bad) > 25:
            print(f"      … and {len(bad) - 25} more")
        return 1
    print(f"   [PASS] {ok_line}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8787")))
    ap.add_argument("--n", type=int, default=25, help="random matches to re-read")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--selftest", action="store_true",
                    help="corrupt each input and assert the comparison FAILS")
    args = ap.parse_args()
    base = f"http://127.0.0.1:{args.port}"

    try:
        listing = fetch(base + "/api/matches?limit=20000")
    except urllib.error.URLError as e:
        print(f"UNKNOWN: no dashboard at {base} ({e}). Start one first:\n"
              f"  PORT={args.port} .venv/bin/python tools/dash/serve.py")
        return 2
    if not listing.get("rows"):
        print("UNKNOWN: the server served no match rows at all")
        return 2

    lg, lad, met, fired = league_by_id(), ladder_by_match(), meta_by_match(), fired_ids()

    print("MATCH DIFF CHECK")
    print(f"  dashboard : {base}/matches   ({listing['n_total']} of our matches, "
          f"{listing['n_shown']} served)")
    print(f"  sources   : league_matches {len(lg)} rows · ladder_games "
          f"{len(lad)} matches · meta_join {len(met)} matches · fire logs "
          f"{len(fired)} ids")
    print(f"  our team  : {listing['our_team']['name']} "
          f"{listing['our_team']['id']} "
          f"(corpus check: {'OK' if listing['our_team']['check']['ok'] else 'FAILED'})")
    print(f"  area class: cwd {'OK' if listing['cwd']['ok'] else 'BLIND — ' + str(listing['cwd']['why'])}")

    fails = 0
    served_by_id = {r["id"]: r for r in listing["rows"]}

    # ---------------------------------------------------------------- A
    rnd = random.Random(args.seed if args.seed is not None else 20260813)
    pool = sorted(served_by_id)
    sample = rnd.sample(pool, min(args.n, len(pool)))
    bad_a: list[str] = []
    details: dict[str, dict] = {}
    for mid in sample:
        exp = expect_from_sources(mid, lg, lad, met, fired)
        bad_a += cmp_row(mid, served_by_id[mid], exp)
        det = fetch(base + "/api/match?id=" + urllib.parse.quote(mid))
        details[mid] = det
        if not det.get("exists"):
            bad_a.append(f"{mid[:8]}: listed on /matches but /match says it does "
                         f"not exist")
            continue
        bad_a += cmp_row(mid, det["match"], exp)
        bad_a += cmp_games(mid, det.get("games") or [], lad, met)
        bad_a += cmp_aggregates(mid, det)
    fails += report(
        "A. STRICT   served match rows vs a positional re-read of the TSVs",
        f"{len(sample)} random matches x (list row + detail row + every game row "
        f"+ the per-match sums), re-read with csv.reader on column indices",
        bad_a,
        f"{len(sample)} matches identical on every compared field, 0 mismatches")

    # ---------------------------------------------------------------- B
    bad_b: list[str] = []
    untested_b: list[str] = []

    # B1 — a CAL-2 match
    cal2 = CAL2_ANCHOR if CAL2_ANCHOR in served_by_id else next(
        (m for m, r in served_by_id.items()
         if (r.get("origin") or {}).get("tag") == "cal-2"), None)
    if not cal2:
        untested_b.append("no cal-2 tagged match in the served rows")
    else:
        bad_b += check_cal2(cal2, served_by_id[cal2], fired)

    # B2 — the voided leg. THE ONE THAT MATTERS MOST.
    void = VOID_ANCHOR if VOID_ANCHOR in served_by_id else next(
        (m for m, r in served_by_id.items() if r.get("result") == "void"), None)
    det_void = None
    if not void:
        untested_b.append("no voided-leg match in the served rows")
    else:
        det_void = details.get(void) or fetch(base + "/api/match?id=" + void)
        bad_b += check_void(void, served_by_id[void], det_void)

    # B3 — an other-account match
    alt = (listing.get("alt_rows") or [None])[0]
    if not alt:
        untested_b.append("no other-account match in the corpus today "
                          "(the `old-account` name has never appeared) — "
                          "selftest drives this branch on an injected row")
        n_old = sum(1 for a in listing.get("alt_accounts", [])
                    if a["tag"] == "old-account")
        if n_old != 1:
            bad_b.append(f"B3: the `old-account` tag is not defined in the payload "
                         f"({n_old} definitions)")
    else:
        bad_b += check_alt(alt, set(served_by_id), listing.get("alt_accounts", []))

    # B4 — a not-yet-decoded match
    nd = next((m for m, r in served_by_id.items()
               if r.get("status") == "no score yet" and r.get("result") != "void"), None)
    det_nd = None
    if not nd:
        untested_b.append("nothing is currently awaiting the archiver")
    else:
        det_nd = details.get(nd) or fetch(base + "/api/match?id=" + nd)
        bad_b += check_undecoded(nd, served_by_id[nd], det_nd)
    fails += report(
        "B. BRANCHES the four cases a random sample would never hit",
        f"B1 cal-2 {str(cal2)[:8]} · B2 voided {str(void)[:8]} · "
        f"B3 other-account {str((alt or {}).get('id'))[:8]} · B4 undecoded {str(nd)[:8]}",
        bad_b,
        "cal-2 tag+cell match the fire log; the voided leg is ERROR with no score, "
        "no games, no aggregate and a live citation; the other account is tagged "
        "and excluded from ours; the undecoded match states the archiver cycle",
        untested="; ".join(untested_b) if untested_b and not bad_b else None)

    # ---------------------------------------------------------------- C
    bad_c: list[str] = []
    untested_c = None
    if shutil.which("node") is None:
        untested_c = "node is not on PATH, so the page's own render() was not run"
    else:
        rl = node_render(STATIC / "matches.html", listing)
        needles = ["UNRATED", "LADDER"]
        if void:
            needles += ["ERROR", "leg (voided"]
        if cal2:
            needles += ["cal-2"]
        bad_c += render_contains(rl, needles)
        if void:
            dv = det_void or fetch(base + "/api/match?id=" + void)
            rv = node_render(STATIC / "match.html", dv, void)
            bad_c += render_contains(rv, ["ERROR", "leg (voided",
                                          "never played"])
            blob = "\n".join(str(v) for v in (rv or {}).values())
            if re.search(r">\s*0-[05]\s*<", blob):
                bad_c.append("the voided match's page rendered a 0-0/0-5 score")
        if nd:
            dn = det_nd or fetch(base + "/api/match?id=" + nd)
            rn = node_render(STATIC / "match.html", dn, nd)
            bad_c += render_contains(rn, ["not yet decoded", "archiver cycle"])
        if alt:
            da = fetch(base + "/api/match?id=" + alt["id"])
            ra = node_render(STATIC / "match.html", da, alt["id"])
            bad_c += render_contains(ra, ["Not our account"])
        bad_c = [b for b in bad_c if b != "__untested__"]
    fails += report(
        "C. RENDER   the pages' own render() over the served payload, in node",
        "stub DOM, no network: asserts the browser would actually print ERROR, "
        "the origin tags and the archiver line — an API that is right can still "
        "be dropped by a template",
        bad_c,
        "every required string is present in the HTML the pages build, and the "
        "voided match renders no 0-0/0-5 anywhere",
        untested=untested_c)

    # ---------------------------------------------------------------- D
    bad_d = scan_forbidden(listing, "list") + (
        scan_forbidden(details[sample[0]], "detail") if sample else [])
    fails += report(
        "D. S1 RULE  the payload computes no statistic it is not allowed to",
        "value positions scanned for win rates, bands, pooled denominators and "
        "inferential statistics (explanatory prose keys exempt — naming the "
        "forbidden thing in order to disclaim it is not doing it)",
        bad_d,
        "no rate, band, pooled denominator or inferential statistic in any value")

    # ------------------------------------------------------------- selftest
    if args.selftest:
        print("\nSELFTEST  driving each comparison to its FAILING verdict")
        ok = True

        victim = sample[0]
        mut = {k: dict(v) for k, v in served_by_id.items()}
        mut[victim]["score_us"] = (mut[victim].get("score_us") or 0) + 7
        got = cmp_row(victim, mut[victim],
                      expect_from_sources(victim, lg, lad, met, fired))
        print(f"   A1 bump {victim[:8]}.score_us by 7        -> {len(got)} "
              f"mismatch(es) {'OK' if got else '*** DID NOT FIRE ***'}")
        ok &= bool(got)

        # A2 — the header-drift case this parser exists for: rename a column in a
        # copy of the file and confirm the positional read stops agreeing.
        tmp = Path(tempfile.mkdtemp(prefix="matchdiff-"))
        try:
            src = LEAGUE.read_text(errors="replace").splitlines()
            src[0] = src[0].replace("scoreA", "score_A")
            (tmp / "league.tsv").write_text("\n".join(src))
            try:
                _positional(tmp / "league.tsv")
                hdr = (tmp / "league.tsv").read_text().splitlines()[0].split("\t")
                fired_ok = "scoreA" not in hdr
            except Exception:
                fired_ok = True
            print(f"   A2 rename scoreA -> score_A in a copy    -> "
                  f"{'index lookup would raise' if fired_ok else 'NOT DETECTED'} "
                  f"{'OK' if fired_ok else '*** DID NOT FIRE ***'}")
            ok &= bool(fired_ok)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

        # B1 — strip the panel cell off a cal-2 row and re-run check_cal2 ITSELF.
        if cal2:
            m1 = dict(served_by_id[cal2])
            m1["origin"] = {**(m1.get("origin") or {}), "cell": "C9-not-a-cell"}
            g1 = check_cal2(cal2, m1, fired)
            print(f"   B1 rewrite {cal2[:8]}'s panel cell           -> {len(g1)} "
                  f"mismatch(es) {'OK' if g1 else '*** DID NOT FIRE ***'}")
            ok &= bool(g1)
        else:
            print("   B1 UNTESTED — no cal-2 match served. Not a pass.")

        # B2 — the false zero, injected, through check_void ITSELF. This is the
        # defect the whole file exists for: a missing score defaulting to 0-5.
        if void:
            m2 = dict(served_by_id[void])
            m2["score_us"], m2["score_them"], m2["status"] = 0, 5, "complete"
            d2 = {**(det_void or {}), "games": [{"n": 1}], "aggregates": {"n_games": 1}}
            g2 = check_void(void, m2, d2)
            print(f"   B2 give the voided leg a 0-5, 'complete' and games -> "
                  f"{len(g2)} mismatch(es) {'OK' if g2 else '*** DID NOT FIRE ***'}")
            ok &= bool(g2)
            # B2c — the citation half, driven separately: a void status whose
            # source has vanished must NOT still print as a plain ERROR.
            m2c = dict(served_by_id[void])
            o = dict(m2c.get("origin") or {})
            o["void"] = {**(o.get("void") or {}),
                         "citation": {"found": False, "line": None}}
            m2c["origin"] = o
            g2c = check_void(void, m2c, det_void or {})
            print(f"   B2c drop the void citation                  -> {len(g2c)} "
                  f"mismatch(es) {'OK' if g2c else '*** DID NOT FIRE ***'}")
            ok &= bool(g2c)
        else:
            print("   B2 UNTESTED — no voided match served. Not a pass.")

        # B3 — the branch the live data CANNOT exercise: there is no
        # `OpenSverige (OLD)` row in the corpus, so the tag is driven on an
        # injected one rather than counted as passed.
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import matches as M
        spec = M._alt_spec("OpenSverige (OLD)", "some-other-uuid")
        hit_old = bool(spec) and spec["tag"] == "old-account"
        spec_ours = M._alt_spec("OpenSverige", OUR)
        # ⛔ AND THE COMPLEMENT: a rule that tags EVERYTHING is not a rule. Our own
        # team name must NOT match the old-account pattern, or every row would
        # carry the tag and the check above would pass for the wrong reason.
        clean = spec_ours is None or spec_ours["tag"] != "old-account"
        print(f"   B3 inject a row named 'OpenSverige (OLD)'   -> tagged "
              f"{spec['tag'] if spec else None!r} "
              f"{'OK' if hit_old else '*** DID NOT FIRE ***'}")
        print(f"   B3c complement: plain 'OpenSverige' is NOT old-account "
              f"-> {'OK' if clean else '*** THE RULE TAGS EVERYTHING ***'}")
        ok &= bool(hit_old and clean)
        if alt:
            m3 = {**alt, "origin": {**(alt.get("origin") or {}),
                                    "tag": None, "ours_fired": True}}
            g3 = check_alt(m3, set(served_by_id), listing.get("alt_accounts", []))
            print(f"   B3d untag an other-account row and call it ours -> "
                  f"{len(g3)} mismatch(es) {'OK' if g3 else '*** DID NOT FIRE ***'}")
            ok &= bool(g3)

        # B4 — a false zero of the other kind: games_rows 0 instead of null, and
        # an aggregate block where nothing has been read. Through check_undecoded.
        if nd:
            m4 = {**served_by_id[nd], "games_rows": 0}
            d4 = {**(det_nd or {}), "games_note": "", "aggregates": {"n_games": 0}}
            g4 = check_undecoded(nd, m4, d4)
            print(f"   B4 undecoded match: games_rows 0, zeroed aggregate, no note "
                  f"-> {len(g4)} mismatch(es) {'OK' if g4 else '*** DID NOT FIRE ***'}")
            ok &= bool(g4)
        else:
            print("   B4 UNTESTED — nothing awaiting the archiver. Not a pass.")

        # C — a template that drops the field.
        if shutil.which("node"):
            broken = json.loads(json.dumps(listing))
            for r in broken["rows"]:
                if r.get("result") == "void":
                    r["result"], r["status"] = "L", "complete"
                    r["score_us"], r["score_them"] = 0, 5
            rl2 = node_render(STATIC / "matches.html", broken)
            gotc = render_contains(rl2, ["leg (voided"])
            blob = "\n".join(str(v) for v in (rl2 or {}).values())
            leaked = bool(re.search(r"<strong>0-5</strong>", blob))
            print(f"   C  rewrite the voided leg as a 0-5 loss  -> "
                  f"{'0-5 rendered' if leaked else 'no 0-5'} "
                  f"{'OK' if leaked else '*** DID NOT FIRE ***'}")
            ok &= bool(leaked)
        else:
            print("   C  UNTESTED — node absent. Not a pass.")

        # D — plant a win rate in a value position.
        planted = {"rows": [{"note_not_prose": "win rate 61.2% pooled over 3 legs"}]}
        gotd = scan_forbidden(planted, "planted")
        print(f"   D  plant 'win rate … pooled' in a value  -> {len(gotd)} "
              f"mismatch(es) {'OK' if gotd else '*** DID NOT FIRE ***'}")
        ok &= bool(gotd)

        if ok:
            print("   SELFTEST OK — every exercised comparison produced the "
                  "other verdict")
        else:
            print("   *** SELFTEST FAILED — a comparison could not be made to "
                  "fail, so its PASS above means nothing ***")
            fails += 1

    print()
    if fails:
        print(f"VERDICT: FAIL ({fails} comparison(s) mismatched)")
        return 1
    print("VERDICT: PASS — the match view's values equal the TSV columns behind them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
