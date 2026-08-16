#!/usr/bin/env python3
"""STACK — compose N planks into one bot tree, by real merge, not file-picking.

    .venv/bin/python tools/stack.py --out bots/_v280foo bodyaware rnd1 spawnlock
    .venv/bin/python tools/stack.py --list
    .venv/bin/python tools/stack.py --selftest

WHY THIS EXISTS (s44, 2026-08-15). Magnus: *"good shards should be ran as
combinations of eachother"* and *"It could probably be a combination of more than
two shards too."* Composing by hand does not scale past two and it goes wrong in
ways that are invisible afterwards. Both failure modes below are ones I actually
committed this session, an hour apart:

⛔ 1. FILE-PICKING SILENTLY DROPS A PLANK. Two planks that both edit `raid.py`
   cannot be combined by copying one of them in. I built `_v272pinthree` that way
   and it had **ZERO references to `LOKI_PINAIM_ON` in the file that must consume
   it** — a no-op wearing a pin's name, which would have measured nothing and
   been reported as a pin test. This tool merges 3-way against the common base
   and then VERIFIES every toggle is both declared and consumed.

⛔ 2. A LINE-BASED CONSTANT MERGE SPLITS MULTI-LINE STATEMENTS. Merging
   `doctrine.py` by grepping `^NAME =` broke `LOKI_BB_SHIELD_TYPES = (` across
   lines and produced a file that did not parse. Declarations are extracted as
   WHOLE STATEMENTS via `ast.get_source_segment`.

HOW IT MERGES. For code files (`main.py`, `raid.py`, `eco.py`): `git merge-file`
3-way against the base, applied cumulatively. For `doctrine.py`, which is a
declaration file every plank appends to and where 3-way conflicts constantly:
take the base, then append each plank's NEW top-level assignments — a name
already defined by the base or an earlier plank is NEVER redefined, and a
collision is REPORTED rather than silently resolved.

⚠ WHAT IT DOES NOT DO. It does not know whether two planks are semantically
compatible. A clean textual merge of two planks that fight each other is still a
clean merge — `bodyaware x rnd1` merged perfectly and came out SUB-ADDITIVE. This
buys you a tree that is what it claims to be; only a battery says whether it is
any good.
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
BASE = ROOT / "bots" / "_v223sealrepair"
FILES = ("main.py", "raid.py", "eco.py", "doctrine.py")
CODE = ("main.py", "raid.py", "eco.py")

# ⛔⛔ THE ANCESTOR TRAP, AND WHY THESE SENTINELS EXIST (s45, 2026-08-15).
# `compose` merges with `git merge-file <out/f> <BASE/f> <tree/f>` — BASE is
# the MERGE ANCESTOR as well as the "ours" seed. That is correct ONLY for a
# plank genuinely forked from BASE. Point it at a plank forked EARLIER (the six
# v197-based arms rebased this session) and git is told that the whole
# BASE-minus-fork chassis delta is a change THE PLANK DELETED — so it resolves
# toward REVERTING SHIP WORK, silently, into a tree that still parses and still
# runs. `PLANKS` declares the fork point implicitly and a declaration can be
# wrong; a sentinel that VANISHED is evidence.
#
# WHY EACH ONE, chosen by reading what v223 actually added over v197:
#  1. LOKI_SEAL_TI_FLOOR = 0 — a RETUNED constant (12 -> 0). The failure mode
#     most likely to pass every other check: the old value is valid Python,
#     parses, declares, and is consumed. Nothing but its VALUE distinguishes
#     the reverted tree. This is the one that nearly went in this session —
#     two arms insert doctrine DIRECTLY above this line.
#  2. LOKI_L4_REPAIR_ON — an ADDED declaration. A wrong-ancestor merge reads
#     chassis additions as plank deletions; a vanished declaration under a
#     surviving use site is a NameError, and on this engine an uncaught
#     exception PERMANENTLY DESTROYS the unit for the rest of the match.
#  3. def _l4_repair (eco.py) — the IMPLEMENTATION of the same plank, in a
#     different file. doctrine.py and eco.py merge by different code paths, so
#     the declaration and the body can be lost INDEPENDENTLY; losing only the
#     body is an AttributeError at the call site.
#  4. the glacierkeep MAP_CODES row — a retuned DATA payload one line deep
#     inside a 15-row tuple literal, i.e. the region where a line-based merge
#     is likeliest to take the wrong side, and the only sentinel whose loss is
#     invisible in behaviour: the bot plays on, navigating a stale map.
CHASSIS_SENTINELS = (
    ("doctrine.py", "LOKI_SEAL_TI_FLOOR = 0"),
    ("doctrine.py", "LOKI_L4_REPAIR_ON"),
    ("eco.py", "def _l4_repair"),
    ("doctrine.py", "JAABAAASAACSCSAACSAACSCSAACAAAJAAB"),  # glacierkeep row
)


def missing_sentinels(tree: Path, only_file: str | None = None) -> list[tuple[str, str]]:
    """Sentinels absent from `tree`. `only_file` narrows to one merged file."""
    out = []
    for f, needle in CHASSIS_SENTINELS:
        if only_file and f != only_file:
            continue
        p = tree / f
        if not p.exists() or needle not in p.read_text():
            out.append((f, needle))
    return out

# plank -> (tree, the toggles that must end up declared AND consumed)
PLANKS = {
    "bodyaware":  ("_v242bodyaware",  []),                       # eco.py only, no toggle
    "rnd1":       ("_v259rnd1",       ["LOKI_HOMEEARLY_ON"]),
    "spawnlock":  ("_v252spawnlock",  ["LOKI_SPAWNLOCK_ON"]),
    "bodyblock":  ("_v262bodyblock",  ["LOKI_BODYBLOCK_ON", "LOKI_BB_PECK_ON"]),
    "catapult":   ("_v253catapult",   ["LOKI_CATAPULT_ON"]),
    "collarseal": ("_v254collarseal", ["LOKI_COLLARSEAL_ON"]),
    "pinaim":     ("_v251pinaim",     ["LOKI_PINAIM_ON"]),
    "sentshell":  ("_v273sentshell",  ["LOKI_SENTSHELL_ON"]),
    "sentban":    ("_v330sentban",    ["LOKI_SENTBAN_ON"]),
}


def top_assigns(path: Path) -> dict[str, str]:
    """name -> whole source statement, module level only."""
    src = path.read_text()
    out: dict[str, str] = {}
    for n in ast.parse(src).body:
        if isinstance(n, (ast.Assign, ast.AnnAssign)):
            tgts = [n.target] if isinstance(n, ast.AnnAssign) else n.targets
            for t in tgts:
                if isinstance(t, ast.Name):
                    out[t.id] = ast.get_source_segment(src, n)
    return out


def compose(planks: list[str], out: Path, quiet=False) -> int:
    def say(*a):
        if not quiet:
            print(*a)
    for p in planks:
        if p not in PLANKS:
            print(f"⛔ unknown plank {p!r}; known: {', '.join(sorted(PLANKS))}")
            return 2
    # A sentinel absent from BASE could never fire — that is a guard that
    # validates everything, this repo's most-repeated defect. Check it first.
    absent = missing_sentinels(BASE)
    if absent:
        print(f"⛔⛔ CONFIG ERROR: {len(absent)} CHASSIS_SENTINELS are not in "
              f"BASE ({BASE.name}) at all, so they can never detect anything:")
        for f, n in absent:
            print(f"      {f}: {n!r}")
        print("      BASE has moved. Re-pick the sentinels from the new "
              "chassis delta before composing anything.")
        return 8

    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(BASE, out, ignore=shutil.ignore_patterns("__pycache__"))

    # --- code files: cumulative 3-way merge against the base -----------------
    for f in CODE:
        for p in planks:
            tree = ROOT / "bots" / PLANKS[p][0]
            if (tree / f).read_bytes() == (BASE / f).read_bytes():
                continue                       # this plank does not touch this file
            r = subprocess.run(["git", "merge-file", str(out / f),
                                str(BASE / f), str(tree / f)],
                               capture_output=True)
            if r.returncode != 0:
                print(f"⛔ CONFLICT merging {p} into {f} — refusing to guess. "
                      f"Compose these two by hand or drop one.")
                shutil.rmtree(out)
                return 3
            # ⛔ WRONG-ANCESTOR DETECTOR. Checked per plank per file so the
            # message can NAME the plank that did it, not just the symptom.
            lost = missing_sentinels(out, only_file=f)
            if lost:
                print(f"⛔⛔ {p} DROPPED CHASSIS WORK from {f} — REFUSING.")
                for lf, n in lost:
                    print(f"      lost sentinel in {lf}: {n!r}")
                print(f"      LIKELY CAUSE: {p!r} is NOT forked from "
                      f"{BASE.name}. `compose` passes BASE as the merge "
                      f"ANCESTOR, so a plank forked earlier reads as having "
                      f"DELETED everything the chassis added since its fork, "
                      f"and the merge reverts ship work.")
                print(f"      FIX: rebase the plank first — "
                      f"tools/rebase_arm.py --base <its real fork> "
                      f"--onto bots/{BASE.name} --arm bots/{PLANKS[p][0]} "
                      f"--out <new tree>")
                shutil.rmtree(out)
                return 6
        say(f"  {f:<12} merged")

    # --- doctrine.py: append NEW declarations, never redefine ----------------
    base_d = top_assigns(BASE / "doctrine.py")
    cur = (out / "doctrine.py").read_text()
    have = dict(base_d)
    added, collisions = [], []
    for p in planks:
        pd = top_assigns(ROOT / "bots" / PLANKS[p][0] / "doctrine.py")
        for k, v in pd.items():
            if k in base_d and v != base_d[k]:
                collisions.append((p, k))       # plank RETUNES a base constant
                continue
            if k in base_d or k in have and k not in base_d:
                continue
            if k not in have:
                have[k] = v
                added.append((p, k, v))
    if added:
        cur += ("\n# ---- composed by tools/stack.py from: " + ", ".join(planks) +
                "\n# Whole statements via ast; nothing already defined is redefined. ----\n"
                + "\n".join(v for _, _, v in added) + "\n")
        (out / "doctrine.py").write_text(cur)
    say(f"  doctrine.py  +{len(added)} declarations")
    if collisions:
        print("  ⚠ RETUNED BASE CONSTANTS NOT APPLIED (a plank changes a value the "
              "base already sets; compose by hand if you need it):")
        for p, k in collisions:
            print(f"      {p} -> {k}")

    # --- verification: parses, and every toggle declared AND consumed --------
    for f in FILES:
        try:
            ast.parse((out / f).read_text())
        except SyntaxError as e:
            print(f"⛔ {f} does not parse after merge: {e}")
            return 4
    code_src = "\n".join((out / f).read_text() for f in CODE)
    doc_src = (out / "doctrine.py").read_text()
    bad = 0
    for p in planks:
        for tog in PLANKS[p][1]:
            decl = f"\n{tog} " in "\n" + doc_src or doc_src.startswith(tog + " ")
            used = tog in code_src
            if not (decl and used):
                print(f"⛔ {p}: toggle {tog} declared={decl} consumed={used} "
                      f"— THIS IS THE NO-OP FAILURE MODE, refusing")
                bad = 1
    marks = sum((out / f).read_text().count("<<<<<<<") for f in FILES)
    if marks:
        print(f"⛔ {marks} conflict markers left in the tree"); bad = 1
    if bad:
        shutil.rmtree(out)
        return 5
    # Backstop: the per-file check above covers CODE merges; doctrine.py is
    # built by appending to a copy of BASE and so should never lose anything,
    # but "should never" is what a backstop is for.
    lost = missing_sentinels(out)
    if lost:
        print("⛔⛔ CHASSIS WORK MISSING FROM THE FINAL TREE — REFUSING:")
        for lf, n in lost:
            print(f"      lost sentinel in {lf}: {n!r}")
        shutil.rmtree(out)
        return 6
    say(f"✅ {out}  ({len(planks)} planks: {', '.join(planks)})  verified: parses, "
        f"every toggle declared AND consumed, 0 conflict markers, "
        f"{len(CHASSIS_SENTINELS)} chassis sentinels intact")
    return 0


def _synth(name: str, mutate) -> str:
    """Materialise a synthetic plank tree off the base; register it in PLANKS."""
    d = ROOT / "bots" / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(BASE, d, ignore=shutil.ignore_patterns("__pycache__"))
    toggles = mutate(d)
    PLANKS[name] = (name, toggles)
    return name


def selftest() -> int:
    """Drive the cells that can actually BITE, not only the one that cannot.

    ⛔ The first version of this drove (a) a real compose and (b) an unknown plank
    name. The side lane pointed out that (b) is the cell that CANNOT hurt you — a
    typo fails loudly on first use — while the two paths the docstring CLAIMS
    (conflict refusal, inert-toggle refusal) were asserted and never exercised.
    An inert toggle is the dangerous one: compose returns 0, the arm runs,
    reconciles, reports a clean 32/32 and MEASURES NOTHING — it reads as a null
    rather than as a defect. Every downstream caveat assumes the arm differs from
    its control.
    """
    fail = 0
    tmp = ROOT / "bots" / "_zzstacktest"

    rc = compose(["bodyaware", "rnd1"], tmp, quiet=True)
    print(f"  1 real compose(bodyaware,rnd1)        rc={rc}  want 0")
    if rc != 0:
        fail = 1
    else:
        eco_ok = (tmp / "eco.py").read_bytes() == (ROOT / "bots/_v242bodyaware/eco.py").read_bytes()
        print(f"      eco.py byte-identical to source:  {eco_ok}  want True")
        fail |= (not eco_ok)
    if tmp.exists():
        shutil.rmtree(tmp)

    rc = compose(["bodyaware", "nosuchplank"], tmp, quiet=True)
    print(f"  2 unknown plank name                  rc={rc}  want 2")
    fail |= (rc != 2)
    if tmp.exists():
        shutil.rmtree(tmp)

    # --- 3. CONFLICT MUST BE REFUSED, NOT GUESSED --------------------------
    # Two synthetic planks rewriting the SAME line of raid.py in different ways.
    def _confA(d):
        p = d / "raid.py"; L = p.read_text().splitlines()
        L[0] = "# SYNTHETIC CONFLICT ARM A"; p.write_text("\n".join(L)); return []
    def _confB(d):
        p = d / "raid.py"; L = p.read_text().splitlines()
        L[0] = "# SYNTHETIC CONFLICT ARM B"; p.write_text("\n".join(L)); return []
    a, b = _synth("_zzconfa", _confA), _synth("_zzconfb", _confB)
    rc = compose([a, b], tmp, quiet=True)
    print(f"  3 two planks conflicting in raid.py   rc={rc}  want 3 (REFUSED)")
    fail |= (rc != 3)
    if tmp.exists():
        shutil.rmtree(tmp)

    # --- 4. A DECLARED-BUT-UNCONSUMED TOGGLE MUST BE REFUSED ---------------
    # This is the silent one: it would compose, run, and measure nothing.
    def _inert(d):
        p = d / "doctrine.py"
        p.write_text(p.read_text() + "\nLOKI_ZZ_INERT_ON = True\n")
        return ["LOKI_ZZ_INERT_ON"]          # declared, never referenced in code
    c = _synth("_zzinert", _inert)
    rc = compose([c], tmp, quiet=True)
    print(f"  4 toggle declared but NEVER consumed  rc={rc}  want 5 (REFUSED)")
    fail |= (rc != 5)
    if tmp.exists():
        shutil.rmtree(tmp)

    # --- 5. WRONG-ANCESTOR MERGE MUST BE REFUSED, WITH THE SENTINEL NAMED ---
    # ⛔ THIS IS THE ONE THAT REVERTS SHIP WORK AND LOOKS FINE AFTERWARDS.
    # The plank is `_v197mapcode` itself — the real pre-v223 chassis, not a toy.
    # Registering it as a plank is exactly the mistake the guard is for: its
    # eco.py is v197's, so merge-file(ours=BASE, base=BASE, theirs=v197) takes
    # theirs wholesale and `def _l4_repair` disappears. Both verdicts are
    # driven: case 1 above is a genuine v223-forked plank that must PASS the
    # same check on the same file.
    PLANKS["_zzoldchassis"] = ("_v197mapcode", [])
    rc = compose(["_zzoldchassis"], tmp, quiet=True)
    print(f"  5 plank forked BEFORE the chassis          rc={rc}  want 6 (REFUSED)")
    fail |= (rc != 6)
    if tmp.exists():
        shutil.rmtree(tmp)
    PLANKS.pop("_zzoldchassis", None)

    # --- 6. A SENTINEL MISSING FROM BASE MUST BE A LOUD CONFIG ERROR --------
    # An alarm that cannot fire is worse than no alarm. Point one sentinel at a
    # string BASE does not contain and the tool must refuse to compose at all
    # rather than pass everything.
    global CHASSIS_SENTINELS
    saved = CHASSIS_SENTINELS
    CHASSIS_SENTINELS = saved + (("doctrine.py", "ZZ_NOT_IN_ANY_CHASSIS_ZZ"),)
    rc = compose(["bodyaware"], tmp, quiet=True)
    print(f"  6 sentinel absent from BASE (cannot fire)  rc={rc}  want 8 (CONFIG)")
    fail |= (rc != 8)
    CHASSIS_SENTINELS = saved
    if tmp.exists():
        shutil.rmtree(tmp)

    for n in ("_zzconfa", "_zzconfb", "_zzinert"):
        PLANKS.pop(n, None)
        if (ROOT / "bots" / n).exists():
            shutil.rmtree(ROOT / "bots" / n)

    print("SELFTEST PASS (compose / unknown / CONFLICT / INERT-TOGGLE / "
          "WRONG-ANCESTOR / DEAD-SENTINEL all discriminated)"
          if not fail else "SELFTEST FAIL")
    return fail


def batch(spec: Path, prefix: str, start: int) -> int:
    """Compose every combination in a file, and ASSERT built == requested.

    ⛔⛔ THIS EXISTS TO DELETE A SHELL LOOP, NOT TO BE CONVENIENT. Composing in a
    zsh `for c in "a b" "c d"; do ... $c ...` loop has now failed THREE TIMES
    TODAY across two people, and every time it ANSWERED rather than crashed:
      * a holder arg went empty and printed ABORT on all three cells  -> looked like a passing guard
      * a composition loop built ZERO of six                          -> looked like a loop that ran
      * a hash loop processed one 18-name blob and printed "1"        -> looked like 18 identical trees
    zsh does not word-split unquoted variables, so the failure is always a
    plausible-looking result. The habit that catches it is asserting the COUNT
    BUILT against the COUNT REQUESTED — the same requested-vs-returned
    reconciliation that mech_battery got this morning, applied to composition.
    Doing it in python removes the splitting hazard entirely rather than relying
    on remembering `${=c}`.
    """
    lines = [l.strip() for l in spec.read_text().splitlines()
             if l.strip() and not l.startswith("#")]
    built, refused = [], []
    for i, line in enumerate(lines):
        planks = line.split()
        out = ROOT / "bots" / f"_v{start + i}{prefix}{len(planks)}"
        rc = compose(planks, out, quiet=True)
        (built if rc == 0 else refused).append((out.name, line, rc))
    print(f"requested {len(lines)}   built {len(built)}   refused {len(refused)}")
    for n, line, _ in built:
        print(f"  ✅ {n:<16} {line}")
    for n, line, rc in refused:
        print(f"  ⛔ {n:<16} {line}   (rc={rc})")
    if len(built) + len(refused) != len(lines):
        print(f"⛔⛔ ACCOUNTING FAILURE: {len(built)}+{len(refused)} != {len(lines)} "
              f"requested. The loop did not process every row.")
        return 9
    return 0 if built else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("planks", nargs="*")
    ap.add_argument("--out")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--batch", help="file of combinations, one per line")
    ap.add_argument("--prefix", default="b")
    ap.add_argument("--start", type=int, default=300)
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.batch:
        return batch(Path(a.batch), a.prefix, a.start)
    if a.list or not a.planks:
        print("planks:", ", ".join(sorted(PLANKS)))
        return 0
    if not a.out:
        print("⛔ --out required")
        return 2
    return compose(a.planks, Path(a.out))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
