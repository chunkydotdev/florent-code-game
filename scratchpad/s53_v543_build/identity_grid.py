#!/usr/bin/env python3
"""v543 INSTRUMENT #3 -- THE DYNAMIC FLAG-OFF IDENTITY GRID.

THE CLAIM UNDER TEST, stated so it can fail: with `FS_V543_BURST = False`,
`bots/_v543burst` produces BYTE-IDENTICAL GAMES to the frozen parent
`bots/_v542wave` on the same (opponent, map, seed, seat).

WHY BYTE-IDENTICAL IS EVEN AVAILABLE, and why the whole grid is worthless
without it: a rated game is a pure function of (opponent, versions, map, seat)
ONLY once decision noise is off.  `NOISE_ON` ships TRUE in every tree here, so
every arm -- INCLUDING BOTH OPPONENTS -- is built as a scratch copy with
`NOISE_ON = False` appended at doctrine.py's EOF (the house arm-construction
pattern).  The repo trees are never edited.

THREE CONTROLS, because a grid of zeros proves nothing on its own:
  C1 DETERMINISM.  The same cell run twice must give the same replay md5.
     If it does not, every comparison below is noise.
  C2 DISCRIMINATION.  A DIFFERENT bot on the same cell must give a DIFFERENT
     md5.  If it does not, md5-of-replay is not sensitive to behaviour and a
     zero-difference result is vacuous.
  C3 NON-VACUITY.  The SAME tree with the plank ON must differ from the parent
     in at least one cell -- otherwise "flag off is identical" is trivially
     true because the plank does nothing at all.

Usage:
  identity_grid.py --arms P0 TOFF TON TDOSE --opps OPP1 OPP2 \
      --maps atoll ... --seeds 3 7 --jobs 8 --out OUT.tsv
  identity_grid.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

if __name__ == "__main__":
    import sys as _hg
    if "-h" in _hg.argv[1:] or "--help" in _hg.argv[1:]:
        print(__doc__)
        raise SystemExit(0)

ROOT = Path(__file__).resolve().parent.parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"
ARMS = ROOT / "scratchpad" / "s53_v543_build" / "arms"


def one(job):
    arm, opp, mp, seed, seat, keep_err = job
    a, b = (arm, opp) if seat == "A" else (opp, arm)
    with tempfile.TemporaryDirectory() as td:
        rep = Path(td) / "r.rep"
        cmd = ["nice", "-n", "19", str(FCODE), "run",
               str(ARMS / a), str(ARMS / b), str(ROOT / "maps" / f"{mp}.map26"),
               "--seed", str(seed), "--tle", "10", "--json",
               "--replay", str(rep)]
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        if not rep.exists():
            return {"arm": arm, "opp": opp, "map": mp, "seed": seed,
                    "seat": seat, "md5": "NOREPLAY", "turns": -1,
                    "cond": "NOREPLAY", "err": ""}
        h = hashlib.md5(rep.read_bytes()).hexdigest()
    res = {}
    for line in reversed(p.stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                res = json.loads(line)
                break
            except json.JSONDecodeError:
                continue
    return {"arm": arm, "opp": opp, "map": mp, "seed": seed, "seat": seat,
            "md5": h, "turns": res.get("turns", -1),
            "cond": res.get("win_condition", "?"),
            "winner": res.get("winner", "?"),
            "tb": p.stderr.count("Traceback"),
            "err": p.stderr if keep_err else ""}


def selftest() -> int:
    """The comparator itself, driven both ways on bytes we control."""
    ok = True
    a = hashlib.md5(b"same").hexdigest()
    b = hashlib.md5(b"same").hexdigest()
    c = hashlib.md5(b"different").hexdigest()
    for label, cond in (("identical bytes compare EQUAL", a == b),
                        ("differing bytes compare UNEQUAL", a != c)):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")
        ok = ok and cond
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+")
    ap.add_argument("--opps", nargs="+")
    ap.add_argument("--maps", nargs="+")
    ap.add_argument("--seeds", nargs="+", type=int)
    ap.add_argument("--seats", nargs="+", default=["A", "B"])
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--out", required=False)
    ap.add_argument("--keep-err", action="store_true",
                    help="retain bot stderr (for the PAIR tape scan)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    for need in ("arms", "opps", "maps", "seeds"):
        if not getattr(a, need):
            ap.error(f"--{need} is required")

    jobs = [(arm, opp, mp, sd, st, a.keep_err)
            for arm, opp, mp, sd, st in itertools.product(
                a.arms, a.opps, a.maps, a.seeds, a.seats)]
    print(f"{len(jobs)} games on {a.jobs} workers", file=sys.stderr)
    rows = []
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for i, r in enumerate(ex.map(one, jobs), 1):
            rows.append(r)
            if i % 25 == 0:
                print(f"  {i}/{len(jobs)}", file=sys.stderr)

    if a.out:
        with open(a.out, "w") as fh:
            fh.write("arm\topp\tmap\tseed\tseat\tmd5\tturns\tcond\twinner\ttb\n")
            for r in rows:
                fh.write("\t".join(str(r[k]) for k in
                                   ("arm", "opp", "map", "seed", "seat", "md5",
                                    "turns", "cond", "winner", "tb")) + "\n")
        if a.keep_err:
            errdir = Path(a.out).with_suffix(".err.d")
            errdir.mkdir(exist_ok=True)
            for r in rows:
                if r["err"]:
                    (errdir / f"{r['arm']}_{r['opp']}_{r['map']}_"
                              f"{r['seed']}_{r['seat']}.err").write_text(r["err"])

    # --- the comparison, per cell, against the FIRST arm as control ---
    ctrl = a.arms[0]
    key = lambda r: (r["opp"], r["map"], r["seed"], r["seat"])  # noqa: E731
    base = {key(r): r for r in rows if r["arm"] == ctrl}
    print(f"\nCONTROL ARM = {ctrl}   cells = {len(base)}")
    print(f"tracebacks across ALL games: {sum(r['tb'] for r in rows)}")
    print(f"NOREPLAY cells: {sum(1 for r in rows if r['md5'] == 'NOREPLAY')}")
    for arm in a.arms[1:]:
        diff = same = 0
        examples = []
        for r in rows:
            if r["arm"] != arm:
                continue
            b = base.get(key(r))
            if b is None:
                continue
            if b["md5"] == r["md5"]:
                same += 1
            else:
                diff += 1
                if len(examples) < 3:
                    examples.append(
                        f"{key(r)} turns {b['turns']}->{r['turns']}")
        print(f"  {arm:6s} vs {ctrl}:  differ {diff:4d} / {same + diff:4d}"
              f"   identical {same}")
        for e in examples:
            print(f"        e.g. {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
