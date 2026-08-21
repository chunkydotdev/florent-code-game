#!/usr/bin/env python3
"""CONTROL-TREE PIN — refuse to launch a shard whose control moved under it.

WHY THIS EXISTS, and it is not a hypothetical: the incumbent tree is the CONTROL
for every queued row. It was edited in the working tree TWICE on 2026-08-15 while
31 rows referenced it and 8 shards were writing. The second time was 90 minutes
after I committed the rule forbidding it, in a commit of my own, and it was
caught by another lane sampling arms by hand rather than by any tool.

⛔ THE FAILURE IS SILENT AND DIRECTIONAL. Nothing errors. Every shard keeps
writing rows. The rows now measure `plank + (control_after - control_before)`,
and because a cleanup makes the control CHEAPER while treatments still pay the
cost, the delta runs the SAME WAY for every arm -- against the treatment. Under a
WALL-CLOCK `--tle 10` that is a behavioural handicap, not a timing wobble. Worse,
it compounds with the auto-stopper: an arm reading low because its control got
faster is indistinguishable from an arm whose plank is dead, and the canceller
kills the real ones.

⛔ WHY A RULE WAS NOT ENOUGH, stated plainly because the rule was mine: I wrote
it, cited it twice, and enforced it on myself once. It did not fire the second
time. The lesson this repo keeps re-learning is that the mechanism holds and the
attention does not -- so this is a tool that exits nonzero, not a paragraph.

WHAT IT PINS. The md5 of the control tree's *.py contents (sorted by name, name
and bytes both folded in, so a rename is a change). NOT mtime -- a checkout or an
rsync moves mtime without changing content, and we would alarm on noise.

USAGE
  control_pin.py --pin                 record the current control hash
  control_pin.py --check               exit 1 if it moved; prints old/new
  control_pin.py --check --shard NAME  same, and names the shard being gated
  control_pin.py --selftest            drives every guard to BOTH verdicts

⛔ EXIT CODE IS THE INTERFACE HERE, deliberately, and that is a departure from
this repo's standing "exit code is not a health signal" rule. That rule is about
`fcode`, whose CLI exits 0 while printing `Error: True`. This tool is ours, its
exit code is the ONLY thing a shell guard can cheaply consume, and its selftest
drives both verdicts -- so the code means what it says here.
"""
from __future__ import annotations

import argparse
import hashlib
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
PIN_FILE = ROOT / "scratchpad" / "CONTROL_PIN"
PROGRAMME = ROOT / "PROGRAMME.md"


def incumbent() -> Path | None:
    """Read the control tree from PROGRAMME.md rather than hardcoding it.

    Hardcoding is how tools/stack.py acquired its ancestor bug: it pinned
    `_v223sealrepair` as BOTH the merge seed AND the ancestor, so an arm forked
    from an older chassis merged as though the intervening development were a
    deletion the arm had made. A tool that reads the authority cannot drift from
    it silently.
    """
    try:
        for ln in PROGRAMME.read_text().splitlines():
            s = ln.strip()
            if s.upper().startswith("INCUMBENT:"):
                v = s.split(":", 1)[1].strip().strip("`")
                if not v:
                    return None
                p = ROOT / v if not v.startswith("/") else Path(v)
                return p if p.is_dir() else None
    except OSError:
        return None
    return None


def previous_incumbent() -> Path | None:
    """Read PREVIOUS_INCUMBENT from PROGRAMME.md (same rules as incumbent()).

    ⛔ ADDED 2026-08-21 (s52, Magnus: "Fix it now") — THE SHIP THAT SEPARATED
    control FROM incumbent. Every guard below was built while control ==
    incumbent held for every row in history; the v174 ship legitimately broke
    it (V537POOL's registered control is the PREVIOUS incumbent, required for
    cross-tape subtraction). A row against the previous incumbent is the
    TRANSITION class, not the flattering-old-control class this tool exists
    to refuse.
    """
    try:
        for ln in PROGRAMME.read_text().splitlines():
            s = ln.strip()
            if s.upper().startswith("PREVIOUS_INCUMBENT:"):
                v = s.split(":", 1)[1].strip().strip("`")
                if not v:
                    return None
                p = ROOT / v if not v.startswith("/") else Path(v)
                return p if p.is_dir() else None
    except OSError:
        return None
    return None


def baseline() -> Path | None:
    """Read BASELINE from PROGRAMME.md (same rules as incumbent()).

    ⛔ ADDED 2026-08-21 (s52, Magnus: "fix them") — the THIRD control class.
    His baseline directive moved the pricing denominator to a teammate's tree
    (`BASELINE:` field, the BASELINE MOVED block); an anchor row scored against
    it is the directive executing, not an off-programme drift. Older-than-all-
    three still refuses — the flattering class stays shut.
    """
    try:
        for ln in PROGRAMME.read_text().splitlines():
            s = ln.strip()
            if s.upper().startswith("BASELINE:"):
                v = s.split(":", 1)[1].strip().strip("`")
                if not v:
                    return None
                p = ROOT / v if not v.startswith("/") else Path(v)
                return p if p.is_dir() else None
    except OSError:
        return None
    return None


def row_control(shard: str) -> Path | None:
    """Resolve THE ROW'S OWN control from the worklist, by shard name.

    The row is the registration (the prereg pins treatment AND control by
    name); INCUMBENT is a pointer that ships move. Resolution order at
    check time: the row's word, then the pointer as fallback.
    """
    wl = ROOT / "scratchpad" / "corefill_work.txt"
    try:
        for ln in wl.read_text(errors="replace").splitlines():
            if not ln.strip() or ln.lstrip().startswith("#"):
                continue
            f = ln.split("\t") if "\t" in ln else ln.split()
            if len(f) >= 3 and f[0].strip() == shard:
                v = f[2].strip()
                p = ROOT / v if not v.startswith("/") else Path(v)
                return p if p.is_dir() else None
    except OSError:
        return None
    return None


def tree_hash(tree: Path) -> str | None:
    """md5 over sorted (name, bytes) of every *.py in the tree.

    Returns None if the tree cannot be read. ⛔ None is BLIND, never "empty" --
    an unreadable tree must not hash to the same value as a tree with no files,
    or a permissions failure would read as "unchanged" forever.
    """
    try:
        files = sorted(p for p in tree.glob("*.py") if p.is_file())
        if not files:
            return None
        h = hashlib.md5()
        for f in files:
            h.update(f.name.encode())
            h.update(b"\0")
            h.update(f.read_bytes())
            h.update(b"\0")
        return h.hexdigest()
    except OSError:
        return None


def read_pins() -> dict[str, str]:
    """{tree(rel): hash} — one line per pinned tree. Backward compatible with
    the single-line format (hash tree)."""
    try:
        lines = PIN_FILE.read_text().splitlines()
    except OSError:
        return {}
    out: dict[str, str] = {}
    for ln in lines:
        parts = ln.split()
        if len(parts) >= 2:
            out[parts[1]] = parts[0]
    return out


def write_pin(tree_rel: str, h: str) -> None:
    pins = read_pins()
    pins[tree_rel] = h
    PIN_FILE.parent.mkdir(parents=True, exist_ok=True)
    PIN_FILE.write_text("".join(f"{v} {k}\n" for k, v in sorted(pins.items())))


def cmd_pin(tree: str | None = None) -> int:
    if tree:
        t = ROOT / tree if not tree.startswith("/") else Path(tree)
        if not t.is_dir():
            print(f"⛔ REFUSING to pin: {tree} is not a directory.")
            return 2
    else:
        t = incumbent()
        if t is None:
            print("⛔ REFUSING to pin: PROGRAMME.md has no readable INCUMBENT tree.")
            return 2
    h = tree_hash(t)
    if h is None:
        print(f"⛔ REFUSING to pin: cannot hash {t} (unreadable, or no .py files).")
        return 2
    rel = str(t.relative_to(ROOT)) if t.is_relative_to(ROOT) else str(t)
    write_pin(rel, h)
    print(f"pinned {rel} = {h}")
    return 0


def cmd_audit(paths: list[str]) -> int:
    """Refuse any worklist row whose CONTROL is not the current incumbent.

    ⛔ MAGNUS, 2026-08-15, verbatim: "Everything needs to beat 140, nothing else
    matters." v140 is `bots/_v223sealrepair` per corpus/version_trees.tsv:70.

    WHY THIS IS A GUARD AND NOT A CONVENTION. A row against an older control
    still produces a clean-looking number, and that number LOOKS BETTER --
    strictly, because it is scored against a weaker bot. Today's board had
    SALTIDLE2 at 64.57% (vs v116), SALT at 61.00% (vs v116) and MAPCODE at
    73.27% (vs another arm's TREATMENT) sitting above every honest v140 read,
    which tops out at 55.4%. **The off-programme rows sort to the TOP of the
    leaderboard**, so the failure is not merely silent -- it is actively
    flattering, and it is what a tired reader will quote.

    ⇒ The check is one line of arithmetic and the reason it is worth a tool is
    that the wrong answer is the attractive one.
    """
    inc = incumbent()
    if inc is None:
        print("⛔ REFUSE: PROGRAMME.md has no readable INCUMBENT — cannot audit controls.")
        return 1
    want = str(inc.relative_to(ROOT)) if inc.is_relative_to(ROOT) else str(inc)
    prev = previous_incumbent()
    base = baseline()
    accepted = {want}
    if base is not None:
        accepted.add(str(base.relative_to(ROOT)) if base.is_relative_to(ROOT) else str(base))
    if prev is not None:
        # transition class (see previous_incumbent's docstring): rows locked
        # when their control WAS the incumbent, overtaken by a ship. Anything
        # OLDER than previous still refuses — the flattering class stays shut.
        accepted.add(str(prev.relative_to(ROOT)) if prev.is_relative_to(ROOT) else str(prev))
    started_dir = ROOT / "scratchpad" / "corefill_started"
    bad = 0
    total = 0
    for path in paths:
        p = Path(path)
        if not p.is_file():
            print(f"⛔ REFUSE: {path} unreadable — BLIND, not clean.")
            return 1
        tsv = p.suffix == ".tsv"
        for ln in p.read_text(errors="replace").splitlines():
            if not ln.strip() or ln.lstrip().startswith("#"):
                continue
            f = ln.split("\t") if tsv else ln.split()
            if len(f) < 3:
                continue
            if tsv and len(f) >= 6 and f[5] in ("WITHDRAWN", "DONE", "FAILED"):
                continue
            shard, treat, ctl = f[0].strip(), f[1].strip(), f[2].strip()
            # ⛔ ONLY ROWS THAT WILL STILL RUN. corefill_work.txt is append-only
            # and keeps every row ever launched, so auditing all of it reports
            # ~121 historical rows forever. AN ALARM THAT CANNOT GO GREEN IS AN
            # ALARM NOBODY READS -- the same failure as a check that never
            # fires, arrived at from the opposite side. History is a fact about
            # what we already measured; it cannot be fixed and must not nag.
            if (started_dir / shard).exists():
                continue
            # NULL CELLS ARE EXEMPT, STRUCTURALLY (treatment path == control
            # path), never by name. A null measures the FIXTURE's noise floor,
            # not a plank, so "does it beat v140" is not a question it asks.
            # Detected by identity because a naming convention rots.
            if treat == ctl:
                continue
            total += 1
            if ctl not in accepted:
                bad += 1
                print(f"⛔ {p.name}: {shard} scored against {ctl}, not any of {sorted(accepted)}")
    if bad:
        print(f"\n⛔ {bad} of {total} live row(s) scored against none of the accepted "
              f"controls (incumbent / previous incumbent / BASELINE). A row against an "
              f"OLDER control reads HIGH and is off-programme.")
        return 1
    print(f"control audit OK: all {total} live row(s) scored against {sorted(accepted)}")
    return 0


def cmd_check(shard: str | None) -> int:
    who = f" for shard {shard}" if shard else ""
    t = row_control(shard) if shard else None
    if t is None:
        t = incumbent()   # fallback: no row found (or no shard named)
    if t is None:
        print(f"⛔ REFUSE{who}: no row control and no readable INCUMBENT — BLIND, not OK.")
        return 1
    now = tree_hash(t)
    if now is None:
        print(f"⛔ REFUSE{who}: cannot hash the control tree {t} — BLIND, not OK.")
        return 1
    rel = str(t.relative_to(ROOT)) if t.is_relative_to(ROOT) else str(t)
    pins = read_pins()
    pin = (pins[rel], rel) if rel in pins else None
    if pin is None:
        # ⛔ NO PIN IS A REFUSAL, NOT A PASS. The whole point is to fail closed:
        # an absent pin is exactly what a fresh checkout or a deleted scratchpad
        # looks like, and treating it as "fine" restores the silent failure.
        print(f"⛔ REFUSE{who}: no pin recorded for {rel}. Run `control_pin.py --pin "
              f"--tree {rel}` deliberately, after confirming it is the control the "
              f"row means.")
        return 1
    want, wtree = pin
    if now != want:
        print(f"⛔ REFUSE{who}: CONTROL TREE MOVED.")
        print(f"   tree:   {t.relative_to(ROOT)}   (pinned as {wtree})")
        print(f"   pinned: {want}")
        print(f"   now:    {now}")
        print("   Rows collected after this point measure plank + control-delta, and the")
        print("   delta runs the SAME direction for every arm. Re-base the arms, or revert")
        print("   the control, then `--pin` again. Do not just re-pin to silence this.")
        return 1
    print(f"control pin OK{who}: {t.relative_to(ROOT)} = {now}")
    return 0


def selftest() -> int:
    import shutil
    import tempfile
    global ROOT, PIN_FILE, PROGRAMME
    fails: list[str] = []

    def chk(label, got, want):
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}  {label:<64} -> {got!r}")
        if not ok:
            fails.append(f"{label} (got {got!r}, want {want!r})")

    tmp = Path(tempfile.mkdtemp(prefix="cpin_"))
    real = (ROOT, PIN_FILE, PROGRAMME)
    try:
        ROOT = tmp
        PIN_FILE = tmp / "scratchpad" / "CONTROL_PIN"
        PROGRAMME = tmp / "PROGRAMME.md"
        ctrl = tmp / "bots" / "_ctrl"
        ctrl.mkdir(parents=True)
        (ctrl / "main.py").write_text("A = 1\n")
        (ctrl / "eco.py").write_text("B = 2\n")
        PROGRAMME.write_text("INCUMBENT: bots/_ctrl\n")

        print("\n── the pin/check cycle, both verdicts ─────────────────────────")
        chk("no pin recorded yet => REFUSE (fails CLOSED, not open)", cmd_check(None), 1)
        chk("pinning succeeds", cmd_pin(), 0)
        chk("unchanged tree => PASS", cmd_check(None), 0)

        # ⛔ THE CELL THIS TOOL EXISTS FOR: a one-line edit to the control.
        (ctrl / "eco.py").write_text("B = 3\n")
        chk("control edited (one line) => REFUSE", cmd_check(None), 1)
        chk("...and the shard name is carried into the refusal",
            cmd_check("MIX280mix4"), 1)
        (ctrl / "eco.py").write_text("B = 2\n")
        chk("reverting the edit restores PASS (not a one-way latch)", cmd_check(None), 0)

        print("\n── content, not mtime ─────────────────────────────────────────")
        import os
        import time
        os.utime(ctrl / "eco.py", (time.time() + 5000, time.time() + 5000))
        chk("mtime bumped, bytes identical => still PASS (rsync/checkout safe)",
            cmd_check(None), 0)

        print("\n── a RENAME is a change ───────────────────────────────────────")
        (ctrl / "eco.py").rename(ctrl / "eco2.py")
        chk("file renamed, bytes identical => REFUSE", cmd_check(None), 1)
        (ctrl / "eco2.py").rename(ctrl / "eco.py")
        chk("renamed back => PASS", cmd_check(None), 0)

        print("\n── blind is never OK ──────────────────────────────────────────")
        PROGRAMME.write_text("INCUMBENT:\n")
        chk("PROGRAMME names no incumbent => REFUSE (blind, not fine)", cmd_check(None), 1)
        PROGRAMME.write_text("INCUMBENT: bots/_ctrl\n")
        for f in ctrl.glob("*.py"):
            f.unlink()
        chk("control tree has no .py files => REFUSE, not 'unchanged'", cmd_check(None), 1)
        chk("...and --pin REFUSES to pin an unhashable tree", cmd_pin(), 2)

        print("\n── --audit: the control must BE the incumbent ──────────────────")
        # ⛔ THE CELL THAT MATTERS: an off-programme row reads HIGH, so this
        # guard must fire on the flattering case, not just the obvious one.
        wl = tmp / "wl.txt"
        wl.write_text("# comment\n"
                      "GOODSHARD bots/_arm bots/_ctrl 5400 1000\n")
        chk("all rows against the incumbent => PASS", cmd_audit([str(wl)]), 0)
        wl.write_text("GOODSHARD bots/_arm bots/_ctrl 5400 1000\n"
                      "OLDSHARD  bots/_arm bots/_v116old 5400 2000\n")
        chk("one row against an OLDER control => REFUSE", cmd_audit([str(wl)]), 1)
        # a TSV worklist, where terminal states are exempt
        tsv = tmp / "q.tsv"
        tsv.write_text("A\tbots/_arm\tbots/_v116old\t5400\t1\tWITHDRAWN\t-\t-\t-\n")
        chk("a WITHDRAWN row against an old control is EXEMPT (not live)",
            cmd_audit([str(tsv)]), 0)
        tsv.write_text("A\tbots/_arm\tbots/_v116old\t5400\t1\tQUEUED\t-\t-\t-\n")
        chk("...the SAME row QUEUED => REFUSE", cmd_audit([str(tsv)]), 1)
        chk("an unreadable worklist => REFUSE (blind, not clean)",
            cmd_audit([str(tmp / "nope.txt")]), 1)

        print("\n── the SHIP-SEPARATION class (control != incumbent; 2026-08-21) ──")
        # restore a hashable control first
        (ctrl / "main.py").write_text("A = 1\n")
        (ctrl / "eco.py").write_text("B = 2\n")
        prevt = tmp / "bots" / "_prev"
        prevt.mkdir(parents=True)
        (prevt / "main.py").write_text("P = 1\n")
        PROGRAMME.write_text("INCUMBENT: bots/_ctrl\nPREVIOUS_INCUMBENT: bots/_prev\n")
        wl2 = tmp / "scratchpad" / "corefill_work.txt"
        wl2.parent.mkdir(parents=True, exist_ok=True)
        wl2.write_text("ROWSHARD\tbots/_arm\tbots/_prev\t5400\t1\n")
        cmd_pin()
        chk("row control (prev) UNPINNED => REFUSE (fails closed)",
            cmd_check("ROWSHARD"), 1)
        chk("pinning the row's own tree by name succeeds", cmd_pin("bots/_prev"), 0)
        chk("row control resolved FROM THE ROW, pinned => PASS",
            cmd_check("ROWSHARD"), 0)
        (prevt / "main.py").write_text("P = 2\n")
        chk("row's control edited => REFUSE (the guard still bites the right tree)",
            cmd_check("ROWSHARD"), 1)
        (prevt / "main.py").write_text("P = 1\n")
        chk("...reverted => PASS", cmd_check("ROWSHARD"), 0)
        chk("unknown shard falls back to INCUMBENT => PASS",
            cmd_check("NOSUCHROW"), 0)
        wlp = tmp / "wlp.txt"
        wlp.write_text("TRANS bots/_arm bots/_prev 5400 1\n")
        chk("audit: a row against the PREVIOUS incumbent => PASS (transition class)",
            cmd_audit([str(wlp)]), 0)
        wlp.write_text("TRANS bots/_arm bots/_prev 5400 1\n"
                       "OLD2 bots/_arm bots/_v99ancient 5400 2\n")
        chk("audit: OLDER-than-previous still => REFUSE (flattery stays shut)",
            cmd_audit([str(wlp)]), 1)
        PROGRAMME.write_text("INCUMBENT: bots/_ctrl\n")
        wlp.write_text("TRANS bots/_arm bots/_prev 5400 1\n")
        chk("audit: NO previous field declared => prev-row REFUSES (no silent widening)",
            cmd_audit([str(wlp)]), 1)

        # ── the BASELINE class (2026-08-21, the third control) ──────────────
        baset = tmp / "bots" / "_base"
        baset.mkdir(parents=True)
        (baset / "main.py").write_text("Z = 1\n")
        PROGRAMME.write_text("INCUMBENT: bots/_ctrl\nBASELINE: bots/_base\n")
        wlb = tmp / "wlb.txt"
        wlb.write_text("ANCH bots/_arm bots/_base 5400 1\n")
        chk("audit: a row against the BASELINE => PASS (the directive's class)",
            cmd_audit([str(wlb)]), 0)
        PROGRAMME.write_text("INCUMBENT: bots/_ctrl\n")
        chk("audit: NO baseline field declared => base-row REFUSES (no silent widening)",
            cmd_audit([str(wlb)]), 1)
        PROGRAMME.write_text("INCUMBENT: bots/_ctrl\nBASELINE: bots/_base\n")
        wlb.write_text("ANCH bots/_arm bots/_base 5400 1\n"
                       "OLD3 bots/_arm bots/_v50relic 5400 2\n")
        chk("audit: baseline accepted while OLDER-than-all-three still REFUSES",
            cmd_audit([str(wlb)]), 1)
        wl2.unlink()

        print("\n── the added-file case (a plank dropped in beside the control) ─")
        (ctrl / "main.py").write_text("A = 1\n")
        (ctrl / "eco.py").write_text("B = 2\n")
        cmd_pin()
        (ctrl / "extra.py").write_text("C = 3\n")
        chk("a NEW .py appearing in the control => REFUSE", cmd_check(None), 1)
    finally:
        ROOT, PIN_FILE, PROGRAMME = real
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if fails:
        print(f"SELFTEST FAIL — {len(fails)}: " + "; ".join(fails))
        return 1
    print("SELFTEST PASS — every guard driven to BOTH verdicts: pin/check cycle, "
          "one-line edit caught, revert un-catches it, mtime-only ignored, rename "
          "caught, missing-pin REFUSES, blind incumbent REFUSES, empty tree REFUSES "
          "rather than reading as unchanged, new file caught; SHIP-SEPARATION: row-resolved control both verdicts, unpinned-row fails closed, previous-incumbent transition accepted while older refuses and absent-field refuses")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pin", action="store_true", help="record the current control hash")
    ap.add_argument("--tree", metavar="PATH",
                    help="pin THIS tree (default: the PROGRAMME incumbent)")
    ap.add_argument("--check", action="store_true", help="exit 1 if the control moved")
    ap.add_argument("--shard", metavar="NAME", help="name the shard being gated, for the message")
    ap.add_argument("--audit", nargs="+", metavar="WORKLIST",
                    help="refuse any live row whose control is not the incumbent")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.audit:
        return cmd_audit(a.audit)
    if a.pin:
        return cmd_pin(a.tree)
    if a.check:
        return cmd_check(a.shard)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
