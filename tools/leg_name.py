#!/usr/bin/env python3
"""LEG NAME ALLOCATION — one registry, so two planks cannot share a LOKI number.

WHY THIS EXISTS (s33, 2026-08-12). Two collisions were created within ten minutes
of each other, both between an s32 plank and an s33 plank:

    LOKI-30  PREREG-loki30-gunaxis-live (LOCKED, +3 amendments)
             vs  bots/_v157gunborder, bots/_v158blankborder   (border-first exile)
    LOKI-31  bots/_v153gunaxtb:565
             vs  bots/_v159surch30, bots/_v159surch90         (non-strike surcharge)

**A PREREG'S IDENTITY IS ITS LEG NAME** -- that is how the prereg-of-record is
located when a result is filed. A locked prereg cannot move, so the new plank
must, and it must move BEFORE results are written under the wrong name. After a
5,408-game readout is filed under "LOKI-30" a rename stops being a rename and
becomes an archive correction (D21).

⛔ AND IT IS NOT CARELESSNESS -- THERE WAS NO CANONICAL LIST. s32's allocations
existed only as COMMENTS INSIDE BOT TREES (`_v153gunaxtb/raid.py:565`,
`_v154gunferry/doctrine.py`), and `docs/prereg/` held only the two legs that
reached a prereg. So "what is the next free LOKI number?" was answerable only by
a repo-wide grep nobody was told to run, and picking "one past the last one I
personally worked on" collides BY CONSTRUCTION across a session boundary. Both
collisions are exactly that. A script, not a convention: attention-level rules
failed under time pressure all day; script-level ones held.

    Diagnosis and this design: the side lane. Built by research.

USAGE
    leg_name.py --next                      # lowest free number, from repo + registry
    leg_name.py --claim 33 --plank "border-first exile" [--tree bots/_v157gunborder ...]
    leg_name.py --audit                     # numbers in the repo that the registry disagrees with
    leg_name.py --selftest                  # driven three ways

⭐ THE THREE-WAY SELFTEST IS THE POINT, AND THE THIRD CELL IS THE LOAD-BEARING ONE.
A guard that refuses a legitimate STACKED ARM gets removed from the path -- which
is exactly how `gate.py` ended up bypassed by `h2h.sh`. So:
    free number            -> CLAIM SUCCEEDS
    bound to OTHER plank   -> CLAIM REFUSED      (the collision this exists for)
    bound to SAME plank    -> CLAIM SUCCEEDS     (arms/stacks: _v151null under LOKI-29)
Without the third cell the guard is unusable and gets deleted; without the second
it is decorative. Both failure modes have precedent in this repo.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs" / "prereg" / "LEG-REGISTRY.md"
SCAN_DIRS = ("bots", "docs/prereg", "docs/legs", "scratchpad")
LOKI_RE = re.compile(r"LOKI[-\s]?(\d{1,3})\b")
ROW_RE = re.compile(r"^\|\s*(\d{1,3})\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*$")

HEADER = """# LEG NAME REGISTRY — the allocation authority for `LOKI-<n>`

**One number, one plank.** Arms and stacks of the SAME plank share a number; two
different planks may not. Created s33 2026-08-12 after two collisions in ten
minutes — see `tools/leg_name.py` for the incident.

**Claim a number with the script, never by hand:**
`.venv/bin/python tools/leg_name.py --claim <n> --plank "<name>" --tree <dir> ...`

| n | plank | trees | prereg |
|---|---|---|---|
"""


def norm(plank: str) -> str:
    """Plank identity for comparison. Case/space/punctuation-insensitive."""
    return re.sub(r"[^a-z0-9]+", "", plank.lower())


def load_registry(path: Path = REGISTRY):
    """-> {n: {'plank':str, 'trees':str, 'prereg':str}}. Missing file = empty."""
    out = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        n, plank, trees, prereg = m.groups()
        out[int(n)] = {"plank": plank.strip(), "trees": trees.strip(), "prereg": prereg.strip()}
    return out


def scan_repo(root: Path = ROOT):
    """-> {n: set(paths)} for every LOKI-<n> mentioned in the tracked scan dirs."""
    found = {}
    for d in SCAN_DIRS:
        base = root / d
        if not base.exists():
            continue
        paths = [base] if base.is_file() else list(base.rglob("*"))
        for p in paths:
            if not p.is_file() or p.suffix not in (".py", ".md", ".txt", ""):
                continue
            try:
                text = p.read_text(errors="ignore")
            except OSError:
                continue
            for m in LOKI_RE.finditer(text):
                found.setdefault(int(m.group(1)), set()).add(str(p.relative_to(root)))
    return found


def next_free(registry, repo) -> int:
    used = set(registry) | set(repo)
    return (max(used) + 1) if used else 1


def claim(n: int, plank: str, trees, path: Path = REGISTRY):
    """-> (ok: bool, message: str). Refuses only a DIFFERENT plank on the same n."""
    reg = load_registry(path)
    if n in reg:
        if norm(reg[n]["plank"]) == norm(plank):
            return True, (f"LOKI-{n} already bound to this same plank "
                          f"({reg[n]['plank']!r}) — OK, this is an arm/stack.")
        return False, (f"⛔ REFUSED: LOKI-{n} is already bound to a DIFFERENT plank\n"
                       f"    bound:    {reg[n]['plank']}\n"
                       f"    you sent: {plank}\n"
                       f"    Pick another number (--next) or rename the other plank.")
    row = f"| {n} | {plank} | {', '.join(trees) if trees else ''} |  |\n"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(HEADER + row)
    else:
        path.write_text(path.read_text().rstrip("\n") + "\n" + row)
    return True, f"LOKI-{n} claimed for {plank!r}."


def audit(registry, repo):
    """Numbers the repo uses that the registry does not know, or knows differently."""
    problems = []
    for n, paths in sorted(repo.items()):
        if n not in registry:
            problems.append((n, "NOT IN REGISTRY", sorted(paths)))
            continue
        known = {t.strip() for t in registry[n]["trees"].split(",") if t.strip()}
        extra = {p for p in paths if not any(p.startswith(k) for k in known)} if known else set()
        if extra:
            problems.append((n, "PATHS NOT LISTED IN REGISTRY", sorted(extra)))
    return problems


def selftest() -> int:
    import tempfile
    fails = []

    def check(name, cond, detail=""):
        print(f"  [{'ok' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
        if not cond:
            fails.append(name)

    with tempfile.TemporaryDirectory() as td:
        reg = Path(td) / "LEG-REGISTRY.md"

        # 1. FREE NUMBER -> SUCCEEDS.
        ok, msg = claim(33, "border-first exile", ["bots/_v157gunborder"], reg)
        check("a FREE number claims cleanly", ok, msg.split("\n")[0])

        # 2. BOUND TO A DIFFERENT PLANK -> REFUSED. The collision this exists for.
        ok2, msg2 = claim(33, "gunaxis live three-arm", ["bots/_vXXX"], reg)
        check("a number bound to a DIFFERENT plank is REFUSED", not ok2)
        check("...and the refusal names both planks", "border-first exile" in msg2
              and "gunaxis live three-arm" in msg2)

        # 3. ⭐ BOUND TO THE SAME PLANK -> SUCCEEDS. Stacked arms must not trip it,
        # or the guard becomes unusable and gets removed from the path.
        ok3, msg3 = claim(33, "Border-First  Exile", ["bots/_v158blankborder"], reg)
        check("a STACKED ARM of the SAME plank is ACCEPTED", ok3, msg3.split("—")[0].strip())

        # 4. The refusal must not have written a row.
        after = load_registry(reg)
        check("a refused claim does NOT mutate the registry", len(after) == 1,
              f"{len(after)} row(s)")

        # 5. --next skips everything used, in registry OR repo.
        check("next_free clears the registry", next_free(after, {}) == 34,
              f"got {next_free(after, {})}")
        check("next_free clears repo-only numbers too", next_free(after, {40: {"x"}}) == 41,
              f"got {next_free(after, {40: {'x'}})}")

        # 6. Registry round-trips (a parser that cannot read its own output is a trap).
        check("registry round-trips through the parser",
              load_registry(reg)[33]["plank"] == "border-first exile")

        # 7. Empty/missing registry is not an error.
        check("a missing registry reads as empty, not a crash",
              load_registry(Path(td) / "nope.md") == {})

    print()
    if fails:
        print(f"SELFTEST FAILED: {len(fails)}: {', '.join(fails)}")
        return 1
    print("SELFTEST PASSED — driven THREE ways: free claims, different-plank refuses,\n"
          "same-plank (stacked arm) accepts. The third cell is what keeps the guard usable.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--next", action="store_true")
    ap.add_argument("--claim", type=int)
    ap.add_argument("--plank")
    ap.add_argument("--tree", action="append", default=[])
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    registry, repo = load_registry(), scan_repo()

    if a.next:
        print(next_free(registry, repo))
        return 0
    if a.audit:
        probs = audit(registry, repo)
        if not probs:
            print(f"AUDIT OK — {len(repo)} LOKI numbers in the repo, all reconciled.")
            return 0
        print(f"AUDIT — {len(probs)} number(s) the registry does not account for:")
        for n, why, paths in probs:
            print(f"  LOKI-{n}: {why}")
            for p in paths[:6]:
                print(f"      {p}")
        return 1
    if a.claim is not None:
        if not a.plank:
            print("--claim needs --plank")
            return 64
        ok, msg = claim(a.claim, a.plank, a.tree)
        print(msg)
        return 0 if ok else 1
    print(__doc__)
    return 64


if __name__ == "__main__":
    sys.exit(main())
