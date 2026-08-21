#!/usr/bin/env python3
"""v541 INSTRUMENT #3 -- THE REMOTE DOSE PROXY (and the identity certificate).

⛔ THE PROBLEM THIS SOLVES, AND WHY THE OBVIOUS INSTRUMENT DOES NOT EXIST.
The dose we want is "builder-attack HP into the enemy core per game" -- the
quantity the field measures at ZERO in 25 of 25 rated games.  Reading it needs
a replay decode, and this build is under a HARD ZERO-local-fcode constraint
until V537POOL reaches 5400 rows.  `tools/remote_battery.py` returns the
run_grid TAPE, not the replays, so no HP ledger is available remotely either.
⇒ **THE EXACT DOSE COUNT IS DEFERRED to a post-V537POOL local decode, and this
file does NOT pretend to substitute for it.**

WHAT IT MEASURES INSTEAD, and the claim is bounded to exactly this:
**DID THE FLAG CHANGE THE GAME AT ALL?**  The battery runs both arms NOISE_OFF
on the SAME (map, seed, seat) cells, against the same opponent, on the same
host -- and `tools/remote_battery.py --selftest` reports that configuration
determinististic: local/ws1/ws2 all 0/12 rows differing, with a NOISE_ON
control at 11-12/12.  So under NOISE_OFF two identical trees produce identical
tapes, and **every differing row is a board on which the flag changed play.**

  * DIVERGENCE > 0  ==  the dose reached the board.  (Necessary, not
    sufficient, for "the verb fired": a changed tape proves behaviour changed,
    and with a single-verb diff the verb is the only candidate.)
  * DIVERGENCE == 0 ==  ZERO DOSE.  The plank did nothing on this fixture and
    any outcome comparison over it is a comparison of one bot with itself.
    ⭐ THIS IS THE READING THAT MATTERS MOST -- it is the one that makes a null
    interpretable, and it is the reading `_v519_gunfirst` needed and did not
    have when it shipped at "0 plants in 356 attempts".

  * SAME FILE, OTHER JOB -- THE FLAG-OFF IDENTITY CERTIFICATE.  Run against
    (flag-off arm, frozen parent) the REQUIRED answer is the opposite one:
    0 differing rows out of N, on all 11 columns.  One reader, two uses, and
    the two uses demand opposite verdicts -- which is why the selftest drives
    it both ways rather than only proving it can find a difference.

    .venv/bin/python scratchpad/s52_v541_build/diverge.py --selftest
    .venv/bin/python scratchpad/s52_v541_build/diverge.py A.tsv B.tsv
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

HDR = ("tag map seed seat ours winner cond turn tracebacks "
       "ours_mined opp_mined").split()
# columns compared for the OUTCOME divergence read.  `tag/map/seed/seat` are
# the JOIN KEY, not a signal.
#
# ⛔⛔ `winner` IS DELIBERATELY EXCLUDED, AND FINDING OUT WHY IS THE REASON THIS
# COMMENT EXISTS.  run_grid writes the WINNING ARM'S DIRECTORY NAME into that
# column, so on every row where BOTH arms won, `winner` reads `_v541quiet` in
# one tape and `parent` in the other -- a guaranteed difference that says
# nothing whatever about behaviour.  The first read of the v541 grid scored
# `winner=123/180` and that number was ~63 parts arm-name and ~60 parts real
# outcome flip.  **A COLUMN THAT DIFFERS BY CONSTRUCTION VALIDATES ANYTHING**,
# which is the same defect class as a constant column certifying anything.
# `ours` (US/OPP/NONE) carries the outcome with no arm identity in it, so the
# information is not lost -- only the contamination.
CMP = ("ours", "cond", "turn", "ours_mined", "opp_mined")


def read(path):
    rows = {}
    dupes = 0
    for line in Path(path).read_text().splitlines():
        f = line.rstrip("\n").split("\t")
        if not f or f[0] == "tag" or len(f) < len(HDR):
            continue
        r = dict(zip(HDR, f))
        if r["tag"] in rows:
            dupes += 1
        rows[r["tag"]] = r
    return rows, dupes


def compare(a_path, b_path, cols=CMP):
    A, adup = read(a_path)
    B, bdup = read(b_path)
    keys = sorted(set(A) & set(B))
    only_a = sorted(set(A) - set(B))
    only_b = sorted(set(B) - set(A))
    diffs = []
    percol = {c: 0 for c in cols}
    for k in keys:
        d = [c for c in cols if A[k][c] != B[k][c]]
        if d:
            diffs.append((k, d, {c: (A[k][c], B[k][c]) for c in d}))
            for c in d:
                percol[c] += 1
    return {
        "n_joined": len(keys), "n_diff": len(diffs), "diffs": diffs,
        "percol": percol, "only_a": only_a, "only_b": only_b,
        "dupes": adup + bdup,
    }


def render(name_a, name_b, res, show=8):
    n, d = res["n_joined"], res["n_diff"]
    pct = 100.0 * d / max(1, n)
    print(f"DIVERGENCE  {name_a}  vs  {name_b}")
    print(f"  joined rows          {n}")
    if res["only_a"] or res["only_b"]:
        print(f"  ⚠ UNJOINED           {len(res['only_a'])} only in A, "
              f"{len(res['only_b'])} only in B "
              "-- an unjoined row is NOT evidence either way")
    if res["dupes"]:
        print(f"  ⚠ DUPLICATE TAGS     {res['dupes']} "
              "-- the join key is not unique; do not read this cell")
    print(f"  rows differing       {d}/{n}  ({pct:.1f}%)")
    print("  by column            "
          + "  ".join(f"{c}={res['percol'][c]}" for c in CMP))
    for k, cols, vals in res["diffs"][:show]:
        print(f"    {k:26s} " + "  ".join(
            f"{c}:{vals[c][0]}->{vals[c][1]}" for c in cols))
    if d > show:
        print(f"    ... and {d - show} more")
    return d


# ---------------------------------------------------------------------------
# SELFTEST -- driven to BOTH verdicts, per column
# ---------------------------------------------------------------------------

def _tape(rows):
    fh = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
    fh.write("\t".join(HDR) + "\n")
    for r in rows:
        fh.write("\t".join(str(r[c]) for c in HDR) + "\n")
    fh.close()
    return fh.name


def _row(tag, **kw):
    base = dict(tag=tag, map="atoll", seed=1, seat="A", ours="US",
                winner="us", cond="Core destroyed", turn=150, tracebacks=0,
                ours_mined=100, opp_mined=200)
    base.update(kw)
    return base


def selftest():
    fails = []

    def chk(cond, msg):
        print(("  ok    " if cond else "  FAIL  ") + msg)
        if not cond:
            fails.append(msg)

    base = [_row(f"m_s{i}_A") for i in range(6)]

    print("[1] IDENTICAL TAPES -> 0 divergence (the identity verdict)")
    a, b = _tape(base), _tape(list(base))
    r = compare(a, b)
    chk(r["n_joined"] == 6 and r["n_diff"] == 0,
        f"joined={r['n_joined']} diff={r['n_diff']} (expect 6 / 0)")

    print("[2] EVERY COMPARED COLUMN, DRIVEN ON ITS OWN (the other verdict)")
    for col, newval in (("ours", "OPP"),
                        ("cond", "Round limit"), ("turn", 999),
                        ("ours_mined", 111), ("opp_mined", 222)):
        mut = [dict(x) for x in base]
        mut[0][col] = newval
        r = compare(a, _tape(mut))
        ok = r["n_diff"] == 1 and r["percol"][col] == 1
        chk(ok, f"a change in `{col}` alone is seen: diff={r['n_diff']} "
                f"percol[{col}]={r['percol'][col]} (expect 1 / 1)")

    print("[3] AN IGNORED COLUMN IS IGNORED (the guard's other side)")
    mut = [dict(x) for x in base]
    mut[0]["tracebacks"] = 7
    r = compare(a, _tape(mut))
    chk(r["n_diff"] == 0,
        "`tracebacks` is not in CMP, so it does not register as divergence "
        "-- it is read separately by summarise.py")
    mut = [dict(x) for x in base]
    for row in mut:
        row["winner"] = "the_other_arm_name"
    r = compare(a, _tape(mut))
    chk(r["n_diff"] == 0,
        "⭐ `winner` DIFFERING ON EVERY ROW registers as ZERO divergence -- "
        "the arm-name contamination is excluded, and this case is the guard "
        "for the defect that produced a false 123/180 on the first read")

    print("[4] UNJOINED ROWS ARE REPORTED, NOT COUNTED AS AGREEMENT")
    r = compare(a, _tape(base[:3]))
    chk(r["n_joined"] == 3 and len(r["only_a"]) == 3 and r["n_diff"] == 0,
        f"joined={r['n_joined']} only_a={len(r['only_a'])} "
        "(a short tape must shrink the denominator, not pad it)")

    print("[5] DUPLICATE TAGS ARE FLAGGED")
    r = compare(_tape(base + [base[0]]), b)
    chk(r["dupes"] >= 1, f"dupes={r['dupes']} (expect >=1)")

    print()
    if fails:
        print(f"SELFTEST FAILED: {len(fails)}")
        for f in fails:
            print("  - " + f)
        return 1
    print(f"SELFTEST PASSED -- identity and divergence both produced, "
          f"all {len(CMP)} compared columns driven individually")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a", nargs="?")
    ap.add_argument("b", nargs="?")
    ap.add_argument("--show", type=int, default=8)
    ap.add_argument("--expect", choices=("same", "differ"),
                    help="assert the verdict and set the exit code")
    ap.add_argument("--selftest", action="store_true")
    x = ap.parse_args()
    if x.selftest:
        return selftest()
    if not (x.a and x.b):
        ap.error("give two tapes, or --selftest")
    res = compare(x.a, x.b)
    d = render(Path(x.a).stem, Path(x.b).stem, res, x.show)
    if x.expect == "same":
        print("VERDICT:", "IDENTICAL — flag-off certificate holds"
              if d == 0 else f"⛔ {d} ROWS DIFFER — identity BROKEN")
        return 0 if d == 0 else 1
    if x.expect == "differ":
        print("VERDICT:", f"DOSE REACHED THE BOARD on {d} rows"
              if d else "⛔ ZERO DOSE — the flag changed nothing on this "
                        "fixture; no outcome read over it is interpretable")
        return 0 if d else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
