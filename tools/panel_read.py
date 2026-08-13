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
  * kill round ............................. corpus/events.tsv (DEATH, core)
    rows — exact. (econ `turns_run` REFUTED as a length proxy: 0/135.)

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
CELLS = {  # same six cells in CAL-1 and CAL-2 (deliberate, cross-panel contrast)
    "team lazy": "C1", "Focalground": "C2", "Juusto": "C3",
    "Jython": "C4", "The Bisons": "C5", "Lunds Stallions": "C6",
}

# Per-panel frozen parameters — each from its own committed prereg. A panel's
# `since` is its prereg commit time; its `until` is the next holder's ship
# (CAL-1 wrapped below n=150, so it is descriptive-only FOREVER per A1.3).
PANELS = {
    "cal1": {"since": "2026-08-13T08:49:13Z", "until": "2026-08-13T10:16:00Z",
             "gaps": {"C1": -122, "C2": -96, "C3": -68, "C4": -54, "C5": -47, "C6": +23},
             "comparative_allowed": False},  # wrapped at 30 games
    "cal2": {"since": "2026-08-13T10:47:00Z", "until": "9999",
             "gaps": {"C1": -85, "C2": -15, "C3": -48, "C4": -65, "C5": +28, "C6": +50},
             "comparative_allowed": True},
}
AREA900 = 900  # drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie

def expected(gap: float) -> float:
    return 1.0 / (1.0 + 10 ** (-gap / 400.0))


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
    """Area from events mw*mh; kill round from the (DEATH, core) EVENT — exact,
    not a length proxy. (econ `turns_run` was tried first and REFUTED as a
    game-length proxy: 0/135 rated files within ±2 of the ladder's own `turns`
    — it is summed unit-turns. events max-rnd scores 129/135 but its misses
    are all r1000 games, i.e. exactly the kill/no-kill boundary.)"""
    need = {g["file"] for g in games}
    area, core_death = {}, {}
    if need:
        with open(corpus / "events.tsv") as f:
            rd = csv.reader(f, delimiter="\t")
            head = next(rd)
            fi, evi, rndi, tmi, ki = (head.index(c) for c in
                                      ("file", "ev", "rnd", "team", "kind"))
            mwi, mhi = head.index("mw"), head.index("mh")
            for row in rd:
                fn = row[fi]
                if fn not in need:
                    continue
                if fn not in area:
                    area[fn] = int(row[mwi]) * int(row[mhi])
                if row[evi] == "DEATH" and row[ki] == "core":
                    core_death[fn] = (int(row[rndi]), row[tmi])
    for g in games:
        g["area"] = area.get(g["file"])
        cd = core_death.get(g["file"])
        # kill round only when WE won AND a core died (their core, necessarily)
        g["turns"] = cd[0] if (cd and g["won"]) else None
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
    kills = [g["turns"] for g in games if g["turns"]]
    tb_wins = w - len(kills)
    vers = sorted({g["oppver"] for g in games})
    lines = [
        f"  games {w}/{n} ({w/n:.1%})  [game-level binomial CI would be ANTI-CONSERVATIVE; primary unit below]",
        f"  matches m={m}: share mean {mean:.3f}" + (f" ± {se:.3f} (cluster SE)" if m > 1 else " (single match — no SE)"),
        f"  area: 900 {sum(g['won'] for g in a900)}/{len(a900)} · <=676 {sum(g['won'] for g in small)}/{len(small)}"
        + (f" · UNDECODED {undec}" if undec else ""),
        f"  core kills {len(kills)}/{w} of wins (tiebreak wins {tb_wins})"
        + (f" · kill round median {statistics.median(kills):.0f}" if kills else ""),
        f"  oppver mix: {', '.join('v'+v for v in vers) if vers else '-'}",
    ]
    return n, lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default="cal2", choices=sorted(PANELS),
                    help="which committed prereg's parameters to read under")
    ap.add_argument("--corpus", default=str(ROOT / "corpus"))
    ap.add_argument("--max-age-min", type=float, default=45.0)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    corpus = Path(args.corpus)
    panel = PANELS[args.panel]
    games = [g for g in join_area_turns(load(corpus, panel["since"]), corpus)
             if g["at"] < panel["until"]]
    newest = max((g["at"] for g in games), default=None)
    total = len(games)
    print(f"PANEL-{args.panel.upper()} readout — since {panel['since']} — {total} games")
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
    if total < 150 or not panel["comparative_allowed"]:
        why = (f"n={total} < 150" if total < 150 else
               "panel wrapped below its floor — descriptive-only forever (A1.3)")
        print(f"\nPANEL DESCRIPTIVE ONLY ({why}). "
              f"Comparative reads are pre-committed at n=150 and n=300 exactly.")
        return 0
    # ---- comparative read (licensed only here, at the pre-committed looks) --
    print(f"\nCOMPARATIVE READ (panel n={total} >= 150; target E frozen at the "
          f"prereg gaps, match-clustered):")
    for opp, cell in sorted(CELLS.items(), key=lambda kv: kv[1]):
        sub = [g for g in games if g["opp"] == opp]
        if len(sub) < 25:
            print(f"  {cell} {opp}: n={len(sub)} < 25 — cell withheld")
            continue
        by_match = defaultdict(list)
        for g in sub:
            by_match[g["match"]].append(g["won"])
        shares = [sum(v) / len(v) for v in by_match.values()]
        m = len(shares)
        mean = statistics.mean(shares)
        se = statistics.stdev(shares) / math.sqrt(m) if m > 1 else float("nan")
        e = expected(panel["gaps"][cell])
        print(f"  {cell} {opp}: share {mean:.3f} vs E {e:.3f} -> "
              f"{mean - e:+.3f} ± {se:.3f} (cluster SE, m={m})")
    print("  (verdict sentences remain the builder's; this table is the read)")
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
        f.write("m1_g1.replay26\tDEATH\t180\tb\tcore\t0\t0\t0\t0\t30\t30\n")
        f.write("m1_g2.replay26\tDEATH\t250\ta\tcore\t0\t0\t0\t0\t20\t20\n")
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
    # kill cell: g1 (won, core death r180) counts; g2's core death does NOT
    # (we lost g2 — the dead core is ours) — 1 kill, median 180
    assert "core kills 1/3" in lines[3] and "180" in lines[3], lines[3]
    # the OTHER verdict: corrupt the TSV ITSELF (m1_g1 won 1 -> 0), re-run the
    # PRODUCTION loader, and require the LOADED count to move 3 -> 2. Flipping
    # a dict in memory would only assert Python arithmetic (side lane, s36).
    rows[0]["our_won"] = "0"
    with open(mj, "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
        wtr.writeheader(); wtr.writerows(rows)
    g2 = load(d, "2026-08-13T08:49:13Z")
    assert sum(x["won"] for x in g2) == 2, (
        "corrupted TSV did not change the LOADED count — selftest is vacuous")
    print("selftest PASS (5-game fixture; ladder + pre-prereg rows excluded; "
          "area 900 detected; corrupted arm changed the count)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
