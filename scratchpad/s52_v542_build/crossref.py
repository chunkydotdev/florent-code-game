#!/usr/bin/env python3
r"""crossref.py — THE MERGE'S OWN STATIC QUESTION: DO THE PLANKS TOUCH?

    crossref.py <tree> [--selftest]

⛔ WHAT THIS ASKS, AND WHY NO PLANK BUILD COULD ASK IT.  Each plank's own
flag-off audit proves ONE family is dominated by ONE master.  A MERGE has a
question none of them has: **does plank A's code read plank B's flags, or call
plank B's methods?**  If it does, "plank A off" is not an ablation of A — it
silently moves B too, and every per-plank ablation table in the report is
measuring something other than what it names.

FOUR SCANS, each reported with its own population so a zero is readable:

  X1  CROSS-FAMILY FLAG READS.  For each plank, every read of ITS flag names
      is attributed to the enclosing function.  A read of plank A's flag inside
      a `_vA_*` method is expected; inside a `_vB_*` method it is COUPLING.
  X2  CROSS-FAMILY CALLS.  Every call to a `_vA_*` method from inside a
      `_vB_*` method.
  X3  SHARED CALL SITES.  Functions that call into MORE THAN ONE family — the
      places two planks compete for the same round.  ⭐ These are NOT defects;
      they are the merge's INTERACTION SURFACE and the report must enumerate
      them by name.  A silent one is the defect.
  X4  SHARED PER-UNIT STATE.  Instance attributes (`self.X`) written by one
      family and read by another.

  ⚠ X3 AND X4 ARE EXPECTED TO BE NON-EMPTY.  This tool does not return a
  verdict on them; it returns the LIST, so the report can carry it and the
  reader can check that each entry was reasoned about.  X1 and X2 are the ones
  whose only acceptable value is empty.

SELFTEST (`--selftest`) drives every scan to BOTH verdicts on synthetic
sources — a scan that has only ever printed an empty list has not been seen to
scan.
"""
import argparse
import ast
import sys
from pathlib import Path

FAMILIES = {
    "v538": {"prefix": "_v538_",
             "flags": {"LOKI_FS_V538", "FS_V538_CLAIM_GATE", "FS_V538_LOG"}},
    "v539": {"prefix": "_v539_",
             "flags": {"LOKI_FS_V539", "FS_V539_REEST", "FS_V539_MIN_RND",
                       "FS_V539_DROUGHT", "FS_V539_LIFELINE_RNDS",
                       "FS_V539_MAX_RNDS", "FS_V539_MAX_EPISODES",
                       "FS_V539_DRAFT", "FS_V539_SEAT3_HOLD",
                       "FS_V539_LIFELINE", "FS_V539_RESERVE_FLOOR",
                       "FS_V539_HONEST_SLOT", "FS_V539_LOG",
                       "FS_ECO_BIT_FAMINE", "FS_ECO_FAM_RND_SHIFT",
                       "FS_ECO_FAM_RND_MASK"}},
    "v541": {"prefix": "_v541_",
             "flags": {"FS_V541_COREPECK", "FS_V541_COREFIRST",
                       "FS_V541_IDLEPECK", "FS_V541_FINISH_ON",
                       "FS_V541_FINISH_HP", "FS_V541_LOG",
                       "FS_V541_TI_FLOOR", "FS_V541_KEEP_SENT",
                       "FS_V541_AMMO_AWARE", "FS_V541_AMMO_MIN",
                       "FS_V541_MAX_PECKS", "FS_V541_RAID_ON",
                       "FS_V541_NEED_SENTINEL"}},
}
FILES = ("doctrine.py", "eco.py", "main.py", "raid.py", "siege.py")


def _enclosing(tree):
    """node -> name of the enclosing FunctionDef, or None (module level)."""
    out = {}

    def walk(node, fn):
        for ch in ast.iter_child_nodes(node):
            nf = ch.name if isinstance(
                ch, (ast.FunctionDef, ast.AsyncFunctionDef)) else fn
            out[ch] = nf
            walk(ch, nf)
    out[tree] = None
    walk(tree, None)
    return out


def _fam_of(name, key="prefix"):
    if not name:
        return None
    for f, d in FAMILIES.items():
        if name.startswith(d["prefix"]):
            return f
    return None


def scan_src(src, fname, res):
    tree = ast.parse(src)
    enc = _enclosing(tree)
    for node in ast.walk(tree):
        efn = enc.get(node)
        efam = _fam_of(efn)
        # X1 flag reads
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            for fam, d in FAMILIES.items():
                if node.id in d["flags"]:
                    res["reads"].append((fam, fname, node.lineno, efn, efam))
        # X2/X3 calls into a family
        if isinstance(node, ast.Call):
            f = node.func
            nm = f.attr if isinstance(f, ast.Attribute) else (
                f.id if isinstance(f, ast.Name) else None)
            cfam = _fam_of(nm)
            if cfam:
                res["calls"].append((cfam, fname, node.lineno, nm, efn, efam))
        # X4 self.<attr> reads/writes
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) \
                and node.value.id == "self":
            kind = "w" if isinstance(node.ctx, ast.Store) else "r"
            res["attrs"].append((fname, node.lineno, node.attr, kind, efn, efam))
    return res


def scan_tree(tree_dir, verbose=True):
    res = {"reads": [], "calls": [], "attrs": []}
    for f in FILES:
        p = Path(tree_dir) / f
        if not p.exists():
            continue
        scan_src(p.read_text(), f, res)

    # X1: a read of family F's flag inside a method of family G != F
    x1 = [r for r in res["reads"] if r[4] is not None and r[4] != r[0]]
    # X2: a call into family F from inside a method of family G != F
    x2 = [c for c in res["calls"] if c[5] is not None and c[5] != c[0]]
    # X3: call sites (enclosing fn) reaching more than one family
    bysite = {}
    for cfam, fn, ln, nm, efn, efam in res["calls"]:
        bysite.setdefault((fn, efn), set()).add(cfam)
    x3 = sorted((k, sorted(v)) for k, v in bysite.items() if len(v) > 1)
    # X4: self attrs touched by more than one family
    byattr = {}
    for fn, ln, a, kind, efn, efam in res["attrs"]:
        if efam:
            byattr.setdefault(a, set()).add(efam)
    x4 = sorted((a, sorted(v)) for a, v in byattr.items() if len(v) > 1)

    if verbose:
        print("POPULATION  %d flag reads · %d family calls · %d self-attr sites"
              % (len(res["reads"]), len(res["calls"]), len(res["attrs"])))
        for fam in FAMILIES:
            n = sum(1 for r in res["reads"] if r[0] == fam)
            c = sum(1 for x in res["calls"] if x[0] == fam)
            print("            %s: %3d flag reads, %3d calls" % (fam, n, c))
        print("\nX1 CROSS-FAMILY FLAG READS (must be empty): %d" % len(x1))
        for fam, f, ln, efn, efam in x1:
            print("   %s flag read inside %s method %s  (%s:%d)"
                  % (fam, efam, efn, f, ln))
        print("X2 CROSS-FAMILY CALLS (must be empty): %d" % len(x2))
        for cfam, f, ln, nm, efn, efam in x2:
            print("   %s() called from %s method %s  (%s:%d)"
                  % (nm, efam, efn, f, ln))
        print("\nX3 SHARED CALL SITES — THE INTERACTION SURFACE "
              "(enumerated, not judged): %d" % len(x3))
        for (f, efn), fams in x3:
            print("   %s :: %s  ->  %s" % (f, efn, ", ".join(fams)))
        print("X4 SHARED PER-UNIT STATE (enumerated, not judged): %d" % len(x4))
        for a, fams in x4:
            print("   self.%s  <->  %s" % (a, ", ".join(fams)))
        print("\nRESULT: %s" % ("PASS (X1=0, X2=0)" if not x1 and not x2
                                else "COUPLING FOUND"))
    return x1, x2, x3, x4


# ---------------------------------------------------------------------------
def selftest():
    fails = []

    def chk(tag, cond):
        print("  %-62s %s" % (tag, "ok" if cond else "!!! WRONG VERDICT"))
        if not cond:
            fails.append(tag)

    def run(src):
        res = {"reads": [], "calls": [], "attrs": []}
        scan_src(src, "t.py", res)
        # replicate the reduction
        x1 = [r for r in res["reads"] if r[4] is not None and r[4] != r[0]]
        x2 = [c for c in res["calls"] if c[5] is not None and c[5] != c[0]]
        bysite = {}
        for cfam, fn, ln, nm, efn, efam in res["calls"]:
            bysite.setdefault((fn, efn), set()).add(cfam)
        x3 = [k for k, v in bysite.items() if len(v) > 1]
        byattr = {}
        for fn, ln, a, kind, efn, efam in res["attrs"]:
            if efam:
                byattr.setdefault(a, set()).add(efam)
        x4 = [a for a, v in byattr.items() if len(v) > 1]
        return x1, x2, x3, x4

    print("SELFTEST crossref.py — every scan, both verdicts")

    CLEAN = (
        "class C:\n"
        "    def _v538_a(self):\n"
        "        self.p538 = 1\n"
        "        return FS_V538_CLAIM_GATE\n"
        "    def _v541_b(self):\n"
        "        self.p541 = 2\n"
        "        return FS_V541_COREPECK and self._v541_c()\n"
        "    def _v541_c(self):\n"
        "        return FS_V541_LOG\n"
    )
    x1, x2, x3, x4 = run(CLEAN)
    chk("CLEAN: X1 empty", not x1)
    chk("CLEAN: X2 empty", not x2)
    chk("CLEAN: X3 empty", not x3)
    chk("CLEAN: X4 empty", not x4)
    # and the population is NOT zero -- otherwise the zeros above are vacuous
    res = {"reads": [], "calls": [], "attrs": []}
    scan_src(CLEAN, "t.py", res)
    chk("CLEAN: population non-empty (zeros are not vacuous)",
        len(res["reads"]) == 3 and len(res["calls"]) == 1)

    DIRTY1 = CLEAN.replace("return FS_V541_LOG",
                           "return FS_V539_DRAFT")          # v539 flag in v541
    x1, _, _, _ = run(DIRTY1)
    chk("X1 fires on a v539 flag read inside a _v541_ method", len(x1) == 1)

    DIRTY2 = CLEAN.replace("return FS_V541_LOG",
                           "return self._v539_famine()")    # v539 call in v541
    _, x2, _, _ = run(DIRTY2)
    chk("X2 fires on a _v539_ call inside a _v541_ method", len(x2) == 1)

    DIRTY3 = (CLEAN + "    def plain(self):\n"
                      "        return self._v538_a() or self._v541_b()\n")
    _, _, x3, _ = run(DIRTY3)
    chk("X3 fires on a plain fn calling two families", len(x3) == 1)

    DIRTY4 = CLEAN.replace("self.p541 = 2", "self.p538 = 2")
    _, _, _, x4 = run(DIRTY4)
    chk("X4 fires on self.p538 touched by v538 and v541", x4 == ["p538"])

    # module-level read must NOT be attributed to a family (efam is None)
    MOD = "FS_V541_LOG\n" + CLEAN
    x1m, _, _, _ = run(MOD)
    chk("module-level flag read is not counted as coupling", not x1m)

    print("SELFTEST %s (%d wrong verdicts)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.tree:
        ap.error("tree required")
    x1, x2, _, _ = scan_tree(a.tree)
    sys.exit(0 if not x1 and not x2 else 1)
