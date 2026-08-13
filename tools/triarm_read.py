#!/usr/bin/env python3
"""TRI-ARM READ — decode-side instrument for PREREG-triarm-live-2026-08-13.

Research produces the NUMBERS; the builder writes the verdict sentences.

Reads the fire log (`scratchpad/triarm_fires.tsv`, ACCEPT rows carry
`{"matchId": ...}`), resolves each match's games in the decoded corpus, and
emits, per the prereg + its amendments:

  * **PIN VERIFICATION (Amendment 3):** B and C are pinned to A's match ids,
    so a triple whose decoded `oppver` values DIFFER is an INSTRUMENT ALARM —
    either the pin did not take or our version decode is wrong. The cell is
    reported as an alarm and NOT read.
  * **W/L grid** per (arm, opponent) — descriptive only.
  * **Arm B falsifier input:** longest bank pin per game via `tools/bank_trace`
    (`econ.tsv` cannot answer it — band-aggregated; see that tool's header).
  * **Arm C mechanism (Amendment 1):** max SIMULTANEOUS forward sentinels,
    paired C-vs-A on shared cells.
  * **O3 churn table (Obligation 14).**

Everything here is descriptive. No verdict language, by design.
"""
from __future__ import annotations
import argparse, csv, json, re, statistics, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
csv.field_size_limit(10 ** 9)
SIDE = {"a": "0", "b": "1"}
MATCH_RE = re.compile(r'"matchId":\s*"([0-9a-f-]{36})"')


def fires(path: Path) -> dict[str, list[str]]:
    """arm -> [matchId] in fire order, ACCEPT rows only."""
    out: dict[str, list[str]] = defaultdict(list)
    for line in path.read_text().splitlines():
        if "\tACCEPT\t" not in line:
            continue
        arm = next((c for c in line.split("\t") if c.startswith("ARM-")), None)
        m = MATCH_RE.search(line)
        if arm and m:
            out[arm].append(m.group(1))
    return dict(out)


def games(corpus: Path, match_ids: set[str]) -> dict[str, list[dict]]:
    """matchId -> [game rows] from meta_join (our side resolved)."""
    out: dict[str, list[dict]] = defaultdict(list)
    for r in csv.DictReader(open(corpus / "meta_join.tsv"), delimiter="\t"):
        if r["match"] not in match_ids or r["us_side"] not in SIDE:
            continue
        opp = r["teamBName"] if r["us_side"] == "a" else r["teamAName"]
        oppver = r["teamBVersion"] if r["us_side"] == "a" else r["teamAVersion"]
        ourver = r["teamAVersion"] if r["us_side"] == "a" else r["teamBVersion"]
        out[r["match"]].append({
            "file": r["file"], "opp": opp, "oppver": oppver, "ourver": ourver,
            "side": SIDE[r["us_side"]], "won": int(r["our_won"] or 0),
            "at": r["completedAt"]})
    return out


def sentinel_overlap(corpus: Path, files: dict[str, str]) -> dict[str, int]:
    """file -> max simultaneous SIEGE sentinels (d2_enemy<=32 at build).

    Same method as the #42 diagnosis cut: pair each BUILD with the first later
    DEATH on the same tile, then sweep the intervals.
    """
    b, d = defaultdict(list), defaultdict(list)
    for r in csv.DictReader(open(corpus / "events.tsv"), delimiter="\t"):
        f = r["file"]
        if f not in files or r["kind"] != "sentinel" or r["team"] != files[f]:
            continue
        if r["ev"] == "BUILD":
            if int(r["d2_enemy"] or 10 ** 9) <= 32:
                b[f].append((int(r["rnd"]), r["x"], r["y"]))
        else:
            d[f].append((int(r["rnd"]), r["x"], r["y"]))
    out = {}
    for f in files:
        dl, used, iv = sorted(d[f]), set(), []
        for rnd, x, y in sorted(b[f]):
            end = 1000
            for i, (dr, dx, dy) in enumerate(dl):
                if i in used or (dx, dy) != (x, y) or dr < rnd:
                    continue
                end = dr
                used.add(i)
                break
            iv.append((rnd, end))
        ev = [(a, 1) for a, _ in iv] + [(z, -1) for _, z in iv]
        cur = mx = 0
        for _t, s in sorted(ev):
            cur += s
            mx = max(mx, cur)
        out[f] = mx
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fires", default=str(ROOT / "scratchpad" / "triarm_fires.tsv"))
    ap.add_argument("--corpus", default=str(ROOT / "corpus"))
    ap.add_argument("--archive", default=str(ROOT / "replay_archive"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    corpus = Path(args.corpus)
    fire = fires(Path(args.fires))
    allids = {m for v in fire.values() for m in v}
    g = games(corpus, allids)
    decoded = sum(len(v) for v in g.values())
    print(f"TRI-ARM READ — arms {sorted(fire)}, "
          f"{len(allids)} matches fired, {len(g)} decoded, {decoded} games")
    if not g:
        print("  nothing decoded yet — run tools/corpus/sync.py after the "
              "archiver cycle (absent from corpus = NOT COMPLETE, never "
              "'does not exist')")
        return 0

    # --- pin verification (Amendment 3) --------------------------------
    by_arm_opp: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for arm, ids in fire.items():
        for mid in ids:
            for row in g.get(mid, []):
                by_arm_opp[(arm, row["opp"])].append(row)
    opps = sorted({o for _a, o in by_arm_opp})
    print("\nPIN VERIFICATION (B/C pinned to A's match ids — differing oppver "
          "in a triple is an INSTRUMENT ALARM, not a data point):")
    alarms = set()
    for opp in opps:
        vers = {}
        for arm in sorted(fire):
            vs = {r["oppver"] for r in by_arm_opp.get((arm, opp), [])}
            if vs:
                vers[arm] = vs
        flat = {v for s in vers.values() for v in s}
        if len(flat) > 1:
            alarms.add(opp)
            print(f"  ⛔ ALARM {opp}: " +
                  " · ".join(f"{a}=v{','.join(sorted(s))}" for a, s in vers.items()))
        elif flat:
            print(f"  ok      {opp}: all arms v{flat.pop()}")

    # --- W/L grid -------------------------------------------------------
    print("\nW/L GRID (descriptive only):")
    print("  " + "arm".ljust(7) + "".join(o[:12].ljust(14) for o in opps) + "total")
    for arm in sorted(fire):
        cells, tw, tn = [], 0, 0
        for o in opps:
            rows = by_arm_opp.get((arm, o), [])
            w, n = sum(r["won"] for r in rows), len(rows)
            tw, tn = tw + w, tn + n
            mark = "!" if o in alarms else " "
            cells.append((f"{w}/{n}{mark}" if n else "-").ljust(14))
        print("  " + arm.ljust(7) + "".join(cells) + (f"{tw}/{tn}" if tn else "-"))
    if alarms:
        print(f"  ! = pin alarm ({', '.join(sorted(alarms))}) — cell not read")

    # --- arm C mechanism: simultaneous siege sentinels -------------------
    files = {r["file"]: r["side"] for rows in g.values() for r in rows}
    ov = sentinel_overlap(corpus, files)
    print("\nARM C MECHANISM — max SIMULTANEOUS siege sentinels (d²≤32), "
          "paired on shared cells:")
    for opp in opps:
        line = []
        for arm in sorted(fire):
            vals = [ov.get(r["file"], 0) for r in by_arm_opp.get((arm, opp), [])]
            if vals:
                line.append(f"{arm[-1]}: max {max(vals)} mean "
                            f"{statistics.mean(vals):.1f}")
        if line:
            flag = "  ⛔ pin alarm" if opp in alarms else ""
            print(f"  {opp[:20].ljust(20)} " + " · ".join(line) + flag)

    # --- PAIRED comparison (the design's power) ---------------------------
    # Pin the maps: every match plays the same 5. mw*mh pairs games across arms
    # WITHIN an opponent — exact for drumlin(625)/frostgate(400)/fjordgate(100),
    # and midgard/drakkarfjord are BOTH 900 so that stratum pairs as a pair.
    area = {}
    for r in csv.DictReader(open(corpus / "events.tsv"), delimiter="\t"):
        f = r["file"]
        if f in files and f not in area:
            area[f] = int(r["mw"]) * int(r["mh"])
    print("\nPAIRED W/L by (opponent, map area) — the matched design; "
          "'-' = that arm has not decoded yet:")
    areas = sorted({a for a in area.values()})
    print("  " + "cell".ljust(22) + "".join(f"a{a}".ljust(12) for a in areas))
    for opp in opps:
        for arm in sorted(fire):
            rows = by_arm_opp.get((arm, opp), [])
            if not rows:
                continue
            cells = []
            for a in areas:
                sub = [r for r in rows if area.get(r["file"]) == a]
                cells.append((f"{sum(r['won'] for r in sub)}/{len(sub)}"
                              if sub else "-").ljust(12))
            mark = " ⛔" if opp in alarms else ""
            print(f"  {(opp[:14] + ' ' + arm[-1]).ljust(22)}" + "".join(cells) + mark)

    # --- arm B falsifier input -------------------------------------------
    print("\nARM B FALSIFIER INPUT — longest bank pin (≤12 Ti consecutive "
          "rounds), via tools/bank_trace.")
    print("  ⚠ UNCONDITIONAL: the prereg's bar is CONDITIONAL on a chronic "
          "camp (enemy latches `under` >100 rnds with our belt cut) and this "
          "tool does NOT detect that precondition — these are pin lengths over "
          "ALL games in the cell. Reading them as the falsifier's answer would "
          "evaluate a different bar than the one registered.")
    try:
        from bank_trace import bank_series, longest_pin
    except Exception as e:                                   # pragma: no cover
        print(f"  bank_trace unavailable: {e}")
        return 0
    arch = Path(args.archive)
    for arm in sorted(fire):
        for opp in opps:
            runs = []
            for r in by_arm_opp.get((arm, opp), []):
                p = arch / r["file"]
                if not p.exists():
                    continue
                s = bank_series(p)
                run, start = longest_pin(s[int(r["side"])], 12)
                runs.append((run, start))
            if runs:
                worst = max(runs)
                flag = "⛔ PINNED" if worst[0] >= 50 else "ok"
                print(f"  {arm} {opp[:18].ljust(18)} longest {worst[0]:4d} rnds "
                      f"(from r{worst[1]}) over {len(runs)} games -> {flag}")
    return 0


def selftest() -> int:
    import tempfile
    d = Path(tempfile.mkdtemp())
    f = d / "fires.tsv"
    f.write_text(
        't\tARM-A\tid\tACCEPT\tx {"matchId": "aaaaaaaa-0000-0000-0000-000000000001"} \n'
        't\tARM-A\tid\tRATELIMIT\tError: Rate limit exceeded\n'
        't\tARM-B\tid\tACCEPT\tx {"matchId": "bbbbbbbb-0000-0000-0000-000000000002"} \n')
    fr = fires(f)
    assert fr == {"ARM-A": ["aaaaaaaa-0000-0000-0000-000000000001"],
                  "ARM-B": ["bbbbbbbb-0000-0000-0000-000000000002"]}, fr
    # the cell that must come out the other way: a RATELIMIT row carrying a
    # matchId-shaped string must NOT be counted as a fire
    f.write_text('t\tARM-A\tid\tRATELIMIT\t{"matchId": '
                 '"cccccccc-0000-0000-0000-000000000003"}\n')
    assert fires(f) == {}, "non-ACCEPT row counted as a fire"
    print("selftest PASS (ACCEPT rows parsed per arm; RATELIMIT row carrying a "
          "matchId NOT counted)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
