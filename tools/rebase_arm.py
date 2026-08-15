#!/usr/bin/env python3
"""REBASE an arm built on one chassis onto a newer chassis, by real 3-way merge.

    .venv/bin/python tools/rebase_arm.py --base bots/_v197mapcode \
        --onto bots/_v223sealrepair --arm bots/_v200siegelaunch \
        --out bots/_v320siegelaunch --toggle LOKI_SIEGE_LAUNCHER

WHY THIS EXISTS (s45, 2026-08-15). Six arms were built as single-diff planks on
top of `_v197mapcode` and their preregs register `_v197mapcode` as control. The
live queue scored them against `_v223sealrepair`, the incumbent. PROGRAMME.md's
"when a ship lands, EVERY CONTROL MOVES WITH IT" made moving the CONTROL right;
what never happened is re-basing the TREATMENT. `v197+plank` vs `v223` measures
the plank MINUS 243 lines of intervening chassis development and cannot
attribute.

⛔ WHY NOT `tools/stack.py`. stack.py composes planks that are ALREADY on the
current chassis: it hardcodes `BASE = bots/_v223sealrepair` and passes that same
path as BOTH the "ours" seed AND the merge ANCESTOR (`git merge-file out BASE
tree`). For these six arms the true common ancestor is `_v197mapcode`, so
stack.py would tell git that the 243-line v197->v223 chassis delta is a change
the ARM DELETED — it would either conflict spuriously or resolve by reverting
chassis work. Its declared-and-consumed toggle check is the part worth keeping
and is reproduced verbatim in `verify()` below, with the same `ast`-based
counting (grep counts docstring prose; a prior agent was misled by exactly that).

WHAT IT DOES NOT DO. It does not know whether a plank is semantically redundant
against the new chassis. A merge can apply perfectly and still be a no-op in
behaviour because the new chassis reached the same effect another way. That is a
READING task and it is done per arm in the report, not here. The one mechanical
half of it IS enforced: the output must DIFFER from the chassis (`--assert-differs`),
which catches the textual case where the merge absorbed the plank entirely.
"""
from __future__ import annotations

import argparse
import ast
import shutil
import subprocess
import sys
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
FILES = ("main.py", "raid.py", "eco.py", "doctrine.py")
CODE = ("main.py", "raid.py", "eco.py")


def count_toggle(tree_dir: Path, toggle: str, files=CODE) -> int:
    """Executable `ast.Name` references to `toggle` across `files`.

    Uses the AST so a mention inside a docstring, a comment or a string CANNOT
    be counted — that is the whole reason this is not a grep, and the reason a
    prior agent read a plank as live when only its prose survived.
    """
    n = 0
    for f in files:
        p = tree_dir / f
        if not p.exists():
            continue
        for node in ast.walk(ast.parse(p.read_text())):
            if isinstance(node, ast.Name) and node.id == toggle:
                n += 1
    return n


def declared(tree_dir: Path, toggle: str) -> bool:
    """`toggle` assigned at module level in doctrine.py (ast, not grep)."""
    src = (tree_dir / "doctrine.py").read_text()
    for node in ast.parse(src).body:
        tgts = ([node.target] if isinstance(node, ast.AnnAssign)
                else node.targets if isinstance(node, ast.Assign) else [])
        for t in tgts:
            if isinstance(t, ast.Name) and t.id == toggle:
                return True
    return False


def rebase(base: Path, onto: Path, arm: Path, out: Path,
           toggles: list[str]) -> tuple[int, dict]:
    """3-way merge per file: ancestor=base, ours=onto, theirs=arm.

    Returns (rc, report). rc 0 clean, 3 conflict, 4 parse fail, 5 verify fail,
    6 no-op vs chassis, 7 a file exists in one tree and not another.
    """
    rep: dict = {"files": {}, "toggles": {}, "conflicts": [], "missing": []}

    # --- file-presence reconciliation: never let a file silently vanish ------
    def pyfiles(d: Path) -> set[str]:
        return {p.name for p in d.glob("*.py")}
    allf = pyfiles(base) | pyfiles(onto) | pyfiles(arm)
    for f in sorted(allf):
        where = [d.name for d in (base, onto, arm) if (d / f).exists()]
        if len(where) != 3:
            rep["missing"].append((f, where))
    if rep["missing"]:
        return 7, rep

    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(onto, out, ignore=shutil.ignore_patterns("__pycache__"))

    for f in sorted(allf):
        if (arm / f).read_bytes() == (base / f).read_bytes():
            rep["files"][f] = "untouched-by-arm"
            continue
        if (onto / f).read_bytes() == (base / f).read_bytes():
            # chassis did not move this file: the arm side IS the answer
            shutil.copyfile(arm / f, out / f)
            rep["files"][f] = "arm-only (chassis identical to base)"
            continue
        r = subprocess.run(["git", "merge-file", "-p",
                            str(onto / f), str(base / f), str(arm / f)],
                           capture_output=True)
        if r.returncode != 0:
            rep["files"][f] = f"CONFLICT ({r.returncode} hunk(s))"
            rep["conflicts"].append((f, r.stdout.decode("utf-8", "replace")))
            shutil.rmtree(out)
            return 3, rep
        (out / f).write_bytes(r.stdout)
        rep["files"][f] = "3-way merged clean"

    # --- 1. parses ----------------------------------------------------------
    for p in sorted(out.glob("*.py")):
        try:
            ast.parse(p.read_text())
        except SyntaxError as e:
            rep["parse_error"] = f"{p.name}: {e}"
            return 4, rep
    rep["parses"] = True

    # --- 2. every toggle DECLARED and CONSUMED (stack.py's check, by ast) ----
    bad = False
    for t in toggles:
        d, c = declared(out, t), count_toggle(out, t)
        rep["toggles"][t] = (d, c)
        if not (d and c > 0):
            bad = True
    if bad:
        return 5, rep

    # --- 3. must DIFFER from the chassis ------------------------------------
    diffs = [f for f in sorted(allf)
             if (out / f).read_bytes() != (onto / f).read_bytes()]
    rep["differs_in"] = diffs
    if not diffs:
        return 6, rep
    # conflict markers, belt and braces
    marks = sum((out / f).read_text().count("<<<<<<<") for f in allf)
    if marks:
        rep["markers"] = marks
        return 5, rep
    return 0, rep


def selftest() -> int:
    """Drive every guard to BOTH verdicts on synthetic trees.

    ⛔ The guards that can actually hurt here are 3 (conflict), 5 (inert toggle)
    and 6 (merged to a no-op). All three RETURN A PLAUSIBLE TREE when they fail
    open: a mis-merged arm still parses, an inert toggle still runs, and an arm
    byte-identical to its control still reconciles a clean 32/32 and reads as a
    NULL rather than as a defect. A check that has never produced the other
    verdict has not been seen to check.
    """
    import tempfile
    fail = 0

    def mk(d: Path, doctrine: str, eco: str):
        d.mkdir(parents=True, exist_ok=True)
        (d / "doctrine.py").write_text(doctrine)
        (d / "eco.py").write_text(eco)
        (d / "main.py").write_text("X = 1\n")
        (d / "raid.py").write_text("Y = 1\n")

    def case(label, rc, want):
        nonlocal fail
        ok = rc == want
        print(f"  {label:<46} rc={rc}  want {want}  {'ok' if ok else '⛔ FAIL'}")
        if not ok:
            fail = 1

    with tempfile.TemporaryDirectory() as td:
        T = Path(td)
        L = "\n".join(f"L{i} = {i}" for i in range(1, 41)) + "\n"

        # ---- 1. clean rebase: chassis and arm move DIFFERENT regions -------
        mk(T / "base", L, "A = 0\n" + L)
        mk(T / "onto", L.replace("L2 = 2", "L2 = 222"), "A = 0\n" + L)
        mk(T / "arm", L + "TOG = True\n", "A = 0\n" + L + "if TOG:\n    pass\n")
        rc, rep = rebase(T / "base", T / "onto", T / "arm", T / "o1", ["TOG"])
        case("1 clean rebase, disjoint regions", rc, 0)
        if rc == 0:
            keep = "L2 = 222" in (T / "o1" / "doctrine.py").read_text()
            print(f"      chassis edit SURVIVED the rebase: {keep}  want True")
            fail |= (not keep)

        # ---- 2. CONFLICT: both sides rewrite the same line -----------------
        mk(T / "arm2", L.replace("L2 = 2", "L2 = 999") + "TOG = True\n",
           "A = 0\n" + L + "if TOG:\n    pass\n")
        rc, _ = rebase(T / "base", T / "onto", T / "arm2", T / "o2", ["TOG"])
        case("2 same-line conflict must be REFUSED", rc, 3)

        # ---- 3. INERT TOGGLE: declared in doctrine, never executed --------
        mk(T / "arm3", L + "TOG = True\n", "A = 0\n" + L)
        rc, _ = rebase(T / "base", T / "onto", T / "arm3", T / "o3", ["TOG"])
        case("3 toggle declared but NEVER consumed", rc, 5)

        # ---- 3b. the grep trap: the ONLY mention is a docstring ------------
        mk(T / "arm3b", L + "TOG = True\n",
           'A = 0\n' + L + '\ndef f():\n    """mentions TOG in prose only."""\n')
        rc, _ = rebase(T / "base", T / "onto", T / "arm3b", T / "o3b", ["TOG"])
        case("3b toggle only in a DOCSTRING (grep trap)", rc, 5)

        # ---- 4. NO-OP: the arm's change is already in the chassis ----------
        armsrc = L + "TOG = True\n"
        mk(T / "arm4", armsrc, "A = 0\n" + L + "if TOG:\n    pass\n")
        mk(T / "onto4", armsrc, "A = 0\n" + L + "if TOG:\n    pass\n")
        rc, _ = rebase(T / "base", T / "onto4", T / "arm4", T / "o4", ["TOG"])
        case("4 arm absorbed by chassis -> no-op REFUSED", rc, 6)

        # ---- 5. a file present in one tree and not another ----------------
        mk(T / "arm5", L + "TOG = True\n", "A = 0\n" + L + "if TOG:\n    pass\n")
        (T / "arm5" / "extra.py").write_text("Z = 1\n")
        rc, rep = rebase(T / "base", T / "onto", T / "arm5", T / "o5", ["TOG"])
        case("5 file in arm only must be REFUSED", rc, 7)
        if rc == 7:
            print(f"      named it: {rep['missing']}")

    print("SELFTEST PASS (clean / conflict / inert / docstring-trap / no-op / "
          "missing-file all discriminated)" if not fail else "SELFTEST FAIL")
    return fail


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base")
    ap.add_argument("--onto")
    ap.add_argument("--arm")
    ap.add_argument("--out")
    ap.add_argument("--toggle", action="append", default=[])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.base and a.onto and a.arm and a.out):
        print("⛔ --base --onto --arm --out all required")
        return 2
    rc, rep = rebase(Path(a.base), Path(a.onto), Path(a.arm), Path(a.out),
                     a.toggle)
    print(f"--- {a.arm} -> {a.out}   rc={rc}")
    for f, s in sorted(rep["files"].items()):
        print(f"    {f:<12} {s}")
    for f, w in rep["missing"]:
        print(f"    ⛔ {f} present only in {w}")
    for t, (d, c) in sorted(rep["toggles"].items()):
        flag = "" if (d and c) else "   ⛔ NO-OP"
        print(f"    toggle {t:<24} declared={d} executable_refs={c}{flag}")
    if "differs_in" in rep:
        print(f"    differs from chassis in: {rep['differs_in'] or '⛔ NOTHING'}")
    for f, body in rep["conflicts"]:
        print(f"    ⛔ CONFLICT in {f}; conflicting region:")
        keep = False
        for line in body.splitlines():
            if line.startswith("<<<<<<<"):
                keep = True
            if keep:
                print("      " + line)
            if line.startswith(">>>>>>>"):
                keep = False
    if "parse_error" in rep:
        print(f"    ⛔ {rep['parse_error']}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
