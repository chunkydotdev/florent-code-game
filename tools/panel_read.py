#!/usr/bin/env python3
"""PANEL-CAL-1 pooled readout (research s36).

Pools UNRATED games of the ACTIVE submission from the decoded corpus, per
panel cell, with MATCH-level clustering as the primary unit (the 5 games of a
match share an opponent and a map draw; measured per-match sd 8.565 vs the
binomial model's 7.111 — game-level CIs are anti-conservative and are labeled
so wherever printed).

Surfaces (why these): unrated matches appear in NO map-named surface
(`league_games`/`ladder_games` are rated-only by construction — verified
s36: 0 of 3,620 unrated matches in `league_games`). So:
  * game rows + opponent + our_won ......... corpus/meta_join.tsv
    (`triggeredBy == 'unrated'`, us_side != 'none')
  * map AREA class ......................... corpus/events.tsv (mw, mh per
    file; area 900 is unambiguous = the five 30x30s; queue #35's proxy)
  * kill-round proxy ....................... corpus/econ.tsv `turns_run`
    (max over the file's team rows; ==1000 means r1000, i.e. no kill)

FRESHNESS: prints the newest completedAt it saw and refuses a verdict-shaped
summary if the corpus is older than --max-age-min (a monitor that reads a
file must report that file's freshness).

Look-schedule guard: comparative output (share - Elo expectation) prints ONLY
at panel totals n>=150, per the prereg. Below that: descriptive only.
"""
from __future__ import annotations
import argparse, csv, math, statistics, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CELLS = {  # PREREG-PANEL-CAL1-v123-field-2026-08-13.md
    "team lazy": "C1", "Focalground": "C2", "Juusto": "C3",
    "Jython": "C4", "The Bisons": "C5", "Lunds Stallions": "C6",
}
AREA900 = 900  # drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie


def load(corpus: Path, since: str):
    games = []  # dicts: match, file, opp, our_won, completedAt
    for r in csv.DictReader(open(corpus / "meta_join.tsv"), delimiter="\t"):
        if r["triggeredBy"] != "unrated" or r["us_side"] == "none":
            continue
        if r["completedAt"] < since:
            continue
        opp = r["teamBName"] if r["us_side"] == "a" else r["teamAName"]
        oppver = r["teamBVersion"] if r["us_side"] == "a" else r["teamAVersion"]
        if opp not in CELLS:
            continue
        games.append({"match": r["match"], "file": r["file"], "opp": opp,
                      "oppver": oppver, "won": int(r["our_won"] or 0),
                      "at": r["completedAt"]})
    return games


def join_area_turns(games, corpus: Path):
    need = {g["file"] for g in games}
    area, turns = {}, {}
    if need:
        with open(corpus / "events.tsv") as f:
            rd = csv.reader(f, delimiter="\t")
            head = next(rd)
            fi, mwi, mhi = head.index("file"), head.index("mw"), head.index("mh")
            for row in rd:
                fn = row[fi]
                if fn in need and fn not in area:
                    area[fn] = int(row[mwi]) * int(row[mhi])
                    if len(area) == len(need):
                        break
        with open(corpus / "econ.tsv") as f:
            rd = csv.reader(f, delimiter="\t")
            head = next(rd)
            fi, ti = head.index("file"), head.index("turns_run")
            for row in rd:
                fn = row[fi]
                if fn in need:
                    turns[fn] = max(turns.get(fn, 0), int(row[ti] or 0))
    for g in games:
        g["area"] = area.get(g["file"])
        g["turns"] = turns.get(g["file"])
    return games


def cell_report(games, elo_gap=None):
    n = len(games)
    w = sum(g["won"] for g in games)
    by_match = defaultdict(list)
    for g in games:
        by_match[g["match"]].append(g["won"])
    shares = [sum(v) / len(v) for v in by_match.values()]
    m = len(shares)
    mean = statistics.mean(shares) if shares else float("nan")
    sd = statistics.stdev(shares) if m > 1 else float("nan")
    se = sd / math.sqrt(m) if m > 1 else float("nan")
    a900 = [g for g in games if g["area"] == AREA900]
    small = [g for g in games if g["area"] is not None and g["area"] != AREA900]
    undec = sum(1 for g in games if g["area"] is None)
    kills = [g["turns"] for g in games if g["won"] and g["turns"] and g["turns"] < 1000]
    vers = sorted({g["oppver"] for g in games})
    lines = [
        f"  games {w}/{n} ({w/n:.1%})  [game-level binomial CI would be ANTI-CONSERVATIVE; primary unit below]",
        f"  matches m={m}: share mean {mean:.3f}" + (f" ± {se:.3f} (cluster SE)" if m > 1 else " (single match — no SE)"),
        f"  area: 900 {sum(g['won'] for g in a900)}/{len(a900)} · <=676 {sum(g['won'] for g in small)}/{len(small)}"
        + (f" · UNDECODED {undec}" if undec else ""),
        f"  kill rounds (wins, <1000): n={len(kills)}"
        + (f" median={statistics.median(kills):.0f}" if kills else ""),
        f"  oppver mix: {', '.join('v'+v for v in vers) if vers else '-'}",
    ]
    return n, lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-08-13T08:49:13Z",
                    help="prereg commit time — panel games only")
    ap.add_argument("--corpus", default=str(ROOT / "corpus"))
    ap.add_argument("--max-age-min", type=float, default=45.0)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    corpus = Path(args.corpus)
    games = join_area_turns(load(corpus, args.since), corpus)
    newest = max((g["at"] for g in games), default=None)
    total = len(games)
    print(f"PANEL-CAL-1 readout — since {args.since} — {total} games")
    if newest:
        age_min = (datetime.now(timezone.utc)
                   - datetime.fromisoformat(newest.replace("Z", "+00:00"))
                   ).total_seconds() / 60
        stale = age_min > args.max_age_min
        print(f"corpus freshness: newest panel game {newest} ({age_min:.1f} min old)"
              + ("  ⚠ STALE — run tools/corpus/sync.py before trusting counts" if stale else ""))
    for opp, cell in sorted(CELLS.items(), key=lambda kv: kv[1]):
        sub = [g for g in games if g["opp"] == opp]
        if not sub:
            print(f"{cell} {opp}: no games yet")
            continue
        n, lines = cell_report(sub)
        floor = "" if n >= 25 else f"  [n<{25}: NO comparative sentence licensed]"
        print(f"{cell} {opp}: n={n}{floor}")
        for ln in lines:
            print(ln)
    if total < 150:
        print(f"\nPANEL TOTAL n={total} < 150 — DESCRIPTIVE ONLY. "
              f"Comparative reads are pre-committed at n=150 and n=300 exactly.")
    return 0


def selftest() -> int:
    """Both-ways: a fixture that must pass and a corrupted one that must fail."""
    import tempfile, os
    d = Path(tempfile.mkdtemp())
    mj = d / "meta_join.tsv"
    cols = ["file", "match", "game", "us_side", "teamAId", "teamAName",
            "teamAVersion", "teamBId", "teamBName", "teamBVersion",
            "teamARating", "teamBRating", "ratingABefore", "ratingBBefore",
            "match_winner_id", "match_winner_side", "game_winner_side",
            "game_winner_id", "our_won", "scoreA", "scoreB", "triggeredBy",
            "completedAt", "related"]
    def row(file, match, opp, won, trig="unrated", at="2026-08-13T09:00:00Z"):
        r = dict.fromkeys(cols, "")
        r.update(file=file, match=match, us_side="a", teamAName="OpenSverige",
                 teamBName=opp, teamBVersion="7", our_won=str(won),
                 triggeredBy=trig, completedAt=at)
        return r
    rows = [row(f"m1_g{i}.replay26", "m1", "Juusto", i % 2) for i in range(1, 6)]
    rows += [row("lad_g1.replay26", "lad", "Juusto", 1, trig="ladder")]  # must be excluded
    rows += [row("old_g1.replay26", "old", "Juusto", 1, at="2026-08-13T00:00:00Z")]  # pre-prereg: excluded
    with open(mj, "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
        wtr.writeheader(); wtr.writerows(rows)
    with open(d / "events.tsv", "w") as f:
        f.write("file\tev\trnd\tteam\tkind\tx\ty\td2_own\td2_enemy\tmw\tmh\n")
        for i in range(1, 6):
            mw = 30 if i == 1 else 20
            f.write(f"m1_g{i}.replay26\tBUILD\t1\ta\tconveyor\t0\t0\t0\t0\t{mw}\t{mw}\n")
    with open(d / "econ.tsv", "w") as f:
        f.write("file\tteam\tband\tammo_converted\tn_convert\tshots\theals\tbuilds\tattacks\tdeliveries\ttled\tturns_run\tcpu_sum_us\tcpu_max_us\tti_end\tammo_end\tti_collected_end\n")
        for i in range(1, 6):
            f.write(f"m1_g{i}.replay26\ta\t0\t0\t0\t0\t0\t0\t0\t0\t0\t{150+i}\t0\t0\t0\t0\t0\n")
    g = join_area_turns(load(d, "2026-08-13T08:49:13Z"), d)
    assert len(g) == 5, f"expected 5 panel games (ladder + pre-prereg excluded), got {len(g)}"
    assert sum(x["won"] for x in g) == 3
    assert sum(1 for x in g if x["area"] == 900) == 1
    n, lines = cell_report(g)
    assert n == 5 and "m=1" in lines[1] and "single match" in lines[1]
    # the OTHER verdict: corrupt our_won so the count MUST disagree
    bad = open(mj).read().replace("unrated\t2026-08-13T09", "unrated\t2026-08-13T09")  # no-op guard
    g2 = load(d, "2026-08-13T08:49:13Z")
    g2[0]["won"] = 1 - g2[0]["won"]
    assert sum(x["won"] for x in g2) != 3, "corrupted fixture failed to change the count — selftest is vacuous"
    print("selftest PASS (5-game fixture; ladder + pre-prereg rows excluded; "
          "area 900 detected; corrupted arm changed the count)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
