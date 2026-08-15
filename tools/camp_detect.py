#!/usr/bin/env python3
"""CHRONIC-CAMP DETECTOR — the PRECONDITION arm B's falsifier is conditional on.

⛔ WHY. `PREREG-triarm-live-2026-08-13` arm B reads: *"in any game where an
enemy camp latches `under` >100 rounds WITH OUR BELT CUT, the bank must NOT
sit pinned <=12 Ti for 50+ consecutive rounds"*. **The bar is CONDITIONAL.**
`tools/bank_trace.py` measures the consequent; nothing measured the
antecedent, so the unconditional pin lengths evaluate a bar nobody
registered. Builder, on being handed that caveat: *"without camp-detection
the falsifier is unevaluable and I type nothing against it."*

**GEOMETRY MIRRORS THE TREE, NOT A GUESS** (`bots/_v197mapcode/main.py:181-182`):
`under` latches on an enemy GUNNER or SENTINEL at d² <= 64, or an enemy
BUILDER_BOT at d² <= 16, from our core. This detector uses the turret half —
the chronic case the income lock needs — and reports the builder half
separately rather than merging them.

**BOTH HALVES REQUIRED** (builder's spec): a camp alone does not trigger the
income lock; the belt must also be cut inside the same span.

Surfaces: `corpus/events.tsv` only — BUILD rows carry `d2_enemy` (distance²
from the building team's placement to the OPPOSING core), so an ENEMY turret's
`d2_enemy` is its distance to OUR core. Camp span = its BUILD round to its
same-tile DEATH (or game end). Belt cut = a DEATH of one of OUR conveyors
inside that span.

Output per game: whether the precondition FIRED, its span, and why not if not.
A cell where it never fires is **UNINFORMATIVE BY PRECONDITION** — which is a
result, not a pass.
"""
from __future__ import annotations
import argparse, csv, sys
from collections import defaultdict
from pathlib import Path

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

ROOT = Path(__file__).resolve().parent.parent
csv.field_size_limit(10 ** 9)
CAMP_D2_TURRET = 64      # main.py:181 — gunner/sentinel
CAMP_D2_BUILDER = 16     # main.py:182 — builder bot (reported, not merged)
MIN_CAMP_ROUNDS = 100    # prereg: ">100 rounds"


def scan(corpus: Path, files: dict[str, str], min_rounds: int = MIN_CAMP_ROUNDS):
    """files: {replay filename: OUR team id as string '0'/'1'}.

    -> {file: {"fired": bool, "spans": [(start, end, kind)],
               "belt_cuts_in_span": int, "longest_camp": int,
               "builder_camp_rounds": int, "last_round": int}}
    """
    builds = defaultdict(list)     # file -> enemy turret camps
    deaths = defaultdict(list)     # file -> (rnd, x, y, kind, team)
    our_belt_deaths = defaultdict(list)
    bcamp = defaultdict(list)
    last_rnd = defaultdict(int)
    for r in csv.DictReader(open(corpus / "events.tsv"), delimiter="\t"):
        f = r["file"]
        if f not in files:
            continue
        ours = files[f]
        rnd = int(r["rnd"])
        last_rnd[f] = max(last_rnd[f], rnd)
        enemy = r["team"] != ours
        if r["ev"] == "BUILD":
            if not enemy:
                continue
            d2 = int(r["d2_enemy"] or 10 ** 9)   # enemy's build -> OUR core
            if r["kind"] in ("gunner", "sentinel") and d2 <= CAMP_D2_TURRET:
                builds[f].append((rnd, r["x"], r["y"], r["kind"]))
            elif r["kind"] == "builder_bot" and d2 <= CAMP_D2_BUILDER:
                bcamp[f].append(rnd)
        else:                                     # DEATH
            if enemy:
                deaths[f].append((rnd, r["x"], r["y"]))
            elif r["kind"] == "conveyor":
                our_belt_deaths[f].append(rnd)

    out = {}
    for f in files:
        dl, used, spans = sorted(deaths[f]), set(), []
        for rnd, x, y, kind in sorted(builds[f]):
            end = last_rnd[f]
            for i, (dr, dx, dy) in enumerate(dl):
                if i in used or (dx, dy) != (x, y) or dr < rnd:
                    continue
                end, _ = dr, used.add(i)
                break
            if end - rnd >= min_rounds:
                spans.append((rnd, end, kind))
        cuts = 0
        for s, e, _k in spans:
            cuts += sum(1 for c in our_belt_deaths[f] if s <= c <= e)
        out[f] = {
            "fired": bool(spans) and cuts > 0,
            "spans": spans,
            "longest_camp": max((e - s for s, e, _ in spans), default=0),
            "belt_cuts_in_span": cuts,
            "builder_camp_events": len(bcamp[f]),
            "last_round": last_rnd[f],
            "why_not": ("" if (spans and cuts) else
                        "no turret camp >=%d rnds at d2<=%d" % (min_rounds, CAMP_D2_TURRET)
                        if not spans else "camp present but NO belt cut inside it"),
        }
    return out


def selftest() -> int:
    """Both-ways, on a fixture written to disk and read by the REAL scanner."""
    import tempfile
    d = Path(tempfile.mkdtemp())
    hdr = "file\tev\trnd\tteam\tkind\tx\ty\td2_own\td2_enemy\tmw\tmh\n"

    def row(f, ev, rnd, team, kind, x=1, y=1, d2e=9):
        return f"{f}\t{ev}\t{rnd}\t{team}\t{kind}\t{x}\t{y}\t0\t{d2e}\t20\t20\n"

    # g1: enemy sentinel camps r10->r300 at d2=9 AND our conveyor dies inside
    # g2: same camp, NO belt cut            -> must NOT fire
    # g3: camp too SHORT (r10->r50)          -> must NOT fire
    # g4: camp far away (d2=400)             -> must NOT fire
    body = (row("g1", "BUILD", 10, "1", "sentinel")
            + row("g1", "DEATH", 300, "1", "sentinel")
            + row("g1", "DEATH", 120, "0", "conveyor")
            + row("g2", "BUILD", 10, "1", "sentinel")
            + row("g2", "DEATH", 300, "1", "sentinel")
            + row("g3", "BUILD", 10, "1", "sentinel")
            + row("g3", "DEATH", 50, "1", "sentinel")
            + row("g3", "DEATH", 20, "0", "conveyor")
            + row("g4", "BUILD", 10, "1", "sentinel", d2e=400)
            + row("g4", "DEATH", 300, "1", "sentinel", d2e=400)
            + row("g4", "DEATH", 120, "0", "conveyor"))
    (d / "events.tsv").write_text(hdr + body)
    files = {f: "0" for f in ("g1", "g2", "g3", "g4")}
    r = scan(d, files)
    assert r["g1"]["fired"], "the positive case did not fire"
    assert r["g1"]["longest_camp"] == 290 and r["g1"]["belt_cuts_in_span"] == 1
    assert not r["g2"]["fired"] and "NO belt cut" in r["g2"]["why_not"], r["g2"]
    assert not r["g3"]["fired"] and "turret camp" in r["g3"]["why_not"], r["g3"]
    assert not r["g4"]["fired"], "a camp 400 away from our core fired"
    # ⭐ the cell that catches a sign/team error: OUR OWN turret near THEIR core
    # must never count as a camp on us
    (d / "events.tsv").write_text(
        hdr + row("g5", "BUILD", 10, "0", "sentinel") +
        row("g5", "DEATH", 300, "0", "sentinel") +
        row("g5", "DEATH", 120, "0", "conveyor"))
    r5 = scan(d, {"g5": "0"})
    assert not r5["g5"]["fired"], "our own forward turret counted as an enemy camp"
    print("selftest PASS (camp+cut fires; camp-without-cut does not; short camp "
          "does not; distant camp does not; OUR OWN turret never counts)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=str(ROOT / "corpus"))
    ap.add_argument("--min-rounds", type=int, default=MIN_CAMP_ROUNDS)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("files", nargs="*", help="replayfile=ourteam pairs, e.g. x.replay26=0")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    files = dict(p.split("=") for p in args.files)
    for f, r in scan(Path(args.corpus), files, args.min_rounds).items():
        print(f"{f[:24]}  fired={r['fired']}  longest_camp={r['longest_camp']} "
              f"cuts_in_span={r['belt_cuts_in_span']}"
              + (f"  ({r['why_not']})" if not r["fired"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
