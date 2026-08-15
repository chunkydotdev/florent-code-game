#!/usr/bin/env python3
"""INERT CHECK — mechanised form of D42: can anything in the DIFF move the
mechanism metric a prereg is about to fire a window on?

    .venv/bin/python tools/inert_check.py docs/prereg/SOME-PREREG.md
    .venv/bin/python tools/inert_check.py docs/prereg/SOME-PREREG.md \
        --treat bots/_vNNplank --control bots/_v130loki13
    .venv/bin/python tools/inert_check.py --metric-reads "a.py:10,b.py" \
        --diff-touches "a.py"
    .venv/bin/python tools/inert_check.py --selftest

D42 (docs/coordination.md:30707, written `38bc735` 2026-08-11T04:08:40Z, ABOUT
LOKI-17/18, naming `raid.py`'s `can_fire_from` guard as the reason the metric
was inert): *"Before pre-registering a mechanism metric, ask what in the DIFF
can change it. If the answer is nothing, the leg spends a window to learn
nothing."* At `21269a6` (06:45:18Z) -- 2h37m later -- D42's own author
pre-registered LOKI-18 Amendment 1 with a bar reading exactly that guard, on a
diff that touches only `main.py:560` with `raid.py` byte-identical, and fired
25 unrated games on it. Full account:
`docs/legs/LEG-loki18-void-and-the-live-closure-2026-08-11.md` sec.4 item 2.
**A rule its own author cannot hold for one working session is a note, not a
rule.** This file is the enforcement, not a restatement.

===== THE MACHINE-READABLE BLOCK A PREREG MUST DECLARE =====
    MECHANISM METRIC READS: <path>:<line>[, <path>:<line> ...]
    TREATMENT DIFF TOUCHES: <path>[, <path> ...]

`<path>` in METRIC READS is repo-root-relative (e.g.
`bots/_v135loki18/raid.py:433`) because it must resolve to a concrete file on
disk -- that is the whole point, an unresolvable read path is not a measured
one. `<path>` in DIFF TOUCHES is bot-tree-relative (e.g. `main.py`,
`sub/dir/file.py`) because that is what a directory diff between a treatment
tree and a control tree naturally produces, and it is also how these preregs
already write it in prose ("one hunk in main.py:560"). Both conventions are
normalised to the same bot-tree-relative key before the intersection test
(`_normalize_for_match`), so a full repo path and a bare filename that name the
same file inside the same tree correctly meet.

===== WHAT THE TOOL DOES, DELIBERATELY SIMPLE =====
1. Parses the block out of a prereg file (or accepts it via
   `--metric-reads`/`--diff-touches` for a prereg that predates the block --
   both LOKI-18 and LOKI-19's preregs do, since D42 postdates them).
2. Optionally RECOMPUTES `TREATMENT DIFF TOUCHES` itself from two bot-tree
   directories (`--treat DIR --control DIR`), byte-diffing every tracked file
   (excluding `__pycache__`/`.pyc`/`.DS_Store`, which are build artefacts, not
   diff), so a declared value is VERIFIED rather than trusted. Declared vs.
   computed disagreement is itself a failure (MALFORMED) -- it means the
   prereg's own account of its diff cannot be relied on, independent of
   whether the metric turns out inert.
3. Asserts the FILE-LEVEL intersection of (normalised) read paths and
   (normalised, preferring computed-if-available) diff-touch paths is
   non-empty. Empty -> INERT -> the leg may not be fired on this bar.
4. A missing block, an unresolvable read path, or a declared/computed
   mismatch is MALFORMED -- these are cases where the prereg cannot be
   trusted to answer the question at all, which this file treats as a
   distinct, worse failure than "resolves cleanly but is inert".

FILE-LEVEL, NOT LINE-LEVEL, AND SAID HERE SO IT ISN'T RE-LITIGATED: a
line-exact match would be defeated by any refactor that moves the guard a few
lines without changing what it does, which is a false INERT for a metric that
is still live. The failure this tool exists to catch is "the diff does not
touch this FILE at all" -- exactly the LOKI-18 shape (mechanism in `raid.py`,
diff in `main.py`, zero overlap at any granularity). A declared line number is
still parsed and printed, because it narrows the report for a human, but it
never gates the verdict.

Verdict token, printed once, gate on this and never on `$?` (this repo's
standing rule -- a pipe/tee makes `$?` the pipe's, per `plank_status.py`'s
docstring):

    INERT_CHECK: PASS | INERT | MALFORMED

Exit 0 on PASS, exit 1 on INERT or MALFORMED.

===== SELFTEST, BOTH ACCEPTANCE CELLS, FROM REAL FILES ON DISK =====
Run: `.venv/bin/python tools/inert_check.py --selftest`

Neither acceptance prereg contains the block yet (both predate D42's
mechanisation), so the selftest constructs the two-line block from the facts
recorded in the brief and D42's own leg doc, and feeds it to the SAME parser
production calls use (`parse_block`) -- it does not hand-roll a second parser
for the test. Where a real bot-tree diff is available on disk the selftest
also exercises the `--treat`/`--control` recomputation path, not only the
declared path, so the verification half of the tool is covered by the
positive/negative cells too, not only by the dedicated mismatch cell.

  NEGATIVE (must read INERT): docs/prereg/PREREG-loki18-forward-sentinel-aims-
  at-core-2026-08-10.md's bar 1 reads `raid.py`'s `can_fire_from` guard
  (`bots/_v135loki18/raid.py:433` -- the brief's approximate line 423 did not
  match the file on disk; verified against source, see below) and its
  treatment diff against `bots/_v130loki13` touches `main.py` only
  (`diff -rq bots/_v130loki13 bots/_v135loki18`, `__pycache__` excluded as a
  build artefact). raid.py != main.py -> empty intersection -> INERT. This is
  the LOKI-18 Amendment-1 shape exactly.

  POSITIVE (must read PASS): docs/prereg/PREREG-loki19-core-peck-2026-08-11
  .md's 5a dose bar counts builder attacks produced by the gate at
  `bots/_v136loki19/raid.py:256`, and its diff against `bots/_v130loki13`
  touches `raid.py` and `doctrine.py` (`main.py`/`eco.py` byte-identical,
  verified: `diff -rq bots/_v130loki13 bots/_v136loki19` reports only raid.py
  and doctrine.py differing, pycache aside). raid.py is in both sets ->
  non-empty intersection -> PASS.

  A checker that answers INERT to everything looks correct on the negative
  cell alone -- that is the exact failure mode this repo keeps rediscovering
  (most recently a ring decoder whose selftest passed while testing the wrong
  property). The positive cell is not optional.

Plus three more cells:
  MALFORMED_NO_BLOCK   -- the real loki18 prereg file, read AS-IS (no flags,
                          no injected block): it has no block on disk today,
                          so the file-parsing path must return MALFORMED, not
                          silently pass or silently read INERT.
  MALFORMED_BAD_PATH    -- a declared read path naming a file that does not
                          exist on disk must not resolve, must not PASS.
  MALFORMED_DIFF_MISMATCH -- a declared TREATMENT DIFF TOUCHES that disagrees
                          with the --treat/--control-computed set (loki18's
                          real diff, declared wrong as `raid.py` instead of
                          `main.py`) must fail, not silently trust the
                          declaration.

===== MUTATION TEST OF THE SELFTEST ITSELF =====
Recipe (run against a SCRATCH COPY, never against tools/):

    d=$(mktemp -d); mkdir -p "$d/tools"
    cp tools/inert_check.py "$d/tools/"
    python3 - "$d/tools/inert_check.py" <<'PY'
    import sys
    src = open(sys.argv[1]).read()
    # (apply one of the two edits below, see MUTATION A / MUTATION B)
    open(sys.argv[1], "w").write(src)
    PY
    INERT_CHECK_REPO_ROOT=/Users/junghard/Projects/Work/florent-code-game \
      .venv/bin/python "$d/tools/inert_check.py" --selftest

(`INERT_CHECK_REPO_ROOT` points the scratch copy back at the real repo's
fixtures, so the selftest fails on the MUTATION, not on missing files --
otherwise `Path(__file__).resolve().parent.parent` from the scratch copy
would resolve to the scratch dir itself.)

MUTATION A -- axis: widen the intersection test so it can never be empty
(the exact class D42 itself failed on: a gate that cannot say no).
  Change:  `hit = reads_norm & touches_norm`
  To:      `hit = reads_norm | touches_norm`
  (union is empty only when BOTH sets are empty, so any non-trivial reads or
  touches makes the gate report non-inert unconditionally.)
  OBSERVED (run 2026-08-11, scratch copy): the NEGATIVE cell -- which must
  read INERT -- read PASS instead. `INERT_CHECK_SELFTEST: FAIL`, reporting
  `NEGATIVE_loki18: expected INERT, got PASS`.

MUTATION B -- axis: a missing block passes silently instead of failing closed.
  Change (the `reads is None or (declared_touches is None and not
  can_compute)` guard and its `return _malformed(...)`):
      if reads is None or (declared_touches is None and not can_compute):
          ... return _malformed(lines)
  To (swallow both instead of refusing to check):
      if reads is None:
          reads = []
      if declared_touches is None and not can_compute:
          declared_touches = []
  OBSERVED (run 2026-08-11, scratch copy): the MALFORMED_NO_BLOCK cell --
  which must read MALFORMED -- read INERT instead (empty reads intersect
  empty touches -> `reads_norm & touches_norm` is empty, which the mutated
  code path reached without ever flagging the missing block).
  `INERT_CHECK_SELFTEST: FAIL`, reporting
  `MALFORMED_NO_BLOCK: expected MALFORMED, got INERT`.

Both mutations were confirmed to flip `INERT_CHECK_SELFTEST` from PASS to
FAIL, and the unmutated file (this one) reads PASS on the same five cells
immediately before and after each scratch run.

===== WHAT THE BRIEF GOT WRONG WHEN IT MET THE CODE =====
The brief's line number for the negative cell's guard ("around line 423,
verify") is off by ten: the live `can_fire_from` call inside
`_try_forward_sentinel` in `bots/_v135loki18/raid.py` is at line 433, not 423
(line 423 falls inside the function's docstring/early-return prose, not on
the guard). Verified by reading the file directly; the selftest uses 433.
Everything else in the brief (both diff claims, the loki19 gate line, the
byte-identity of main.py/eco.py between v136loki19 and v130loki13) checked out
exactly as stated.
"""
from __future__ import annotations

import argparse
import os
import re
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

# Repo root, overridable via INERT_CHECK_REPO_ROOT. The override exists so a
# MUTATED SCRATCH COPY of this file (see the mutation-test recipe below) can
# still resolve the real repo's prereg docs and bot trees for --selftest --
# without it, `Path(__file__).resolve().parent.parent` from a scratch copy
# would point at the scratch dir, and the selftest would fail on missing
# fixtures rather than on the mutation being tested.
ROOT = (Path(os.environ["INERT_CHECK_REPO_ROOT"]).resolve()
        if os.environ.get("INERT_CHECK_REPO_ROOT")
        else Path(__file__).resolve().parent.parent)

READS_LABEL = "MECHANISM METRIC READS:"
TOUCHES_LABEL = "TREATMENT DIFF TOUCHES:"

_READS_RE = re.compile(r"^\s*" + re.escape(READS_LABEL) + r"\s*(.+?)\s*$", re.M)
_TOUCHES_RE = re.compile(r"^\s*" + re.escape(TOUCHES_LABEL) + r"\s*(.+?)\s*$", re.M)

# Build artefacts to ignore when diffing two bot trees -- not source, never
# part of a "diff touches" claim.
_IGNORE_NAMES = {".DS_Store"}
_IGNORE_SUFFIXES = {".pyc"}
_IGNORE_DIR_PARTS = {"__pycache__"}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_reads_entry(entry: str) -> tuple[str, int | None]:
    """'path:line' or bare 'path' -> (path, line_or_None)."""
    m = re.match(r"^(.*):(\d+)$", entry)
    if m:
        return m.group(1).strip(), int(m.group(2))
    return entry.strip(), None


def parse_block(text: str):
    """Extract the machine-readable block from prereg markdown.

    Returns (reads, touches) where reads is a list of (path, line_or_None)
    and touches is a list of path strings -- or (None, None) if EITHER
    labelled line is absent. Both lines are required: a block that declares
    reads but not touches (or vice versa) is exactly the kind of half-claim
    this tool exists to refuse, not infer around.
    """
    rm = _READS_RE.search(text)
    tm = _TOUCHES_RE.search(text)
    if rm is None or tm is None:
        return None, None
    reads = [parse_reads_entry(e) for e in rm.group(1).split(",") if e.strip()]
    touches = [e.strip() for e in tm.group(1).split(",") if e.strip()]
    return reads, touches


# ---------------------------------------------------------------------------
# Diff recomputation
# ---------------------------------------------------------------------------

def _walk_tree(d: Path) -> dict[str, bytes]:
    out = {}
    for p in d.rglob("*"):
        if p.is_dir():
            continue
        if _IGNORE_DIR_PARTS & set(p.relative_to(d).parts[:-1]):
            continue
        if p.name in _IGNORE_NAMES or p.suffix in _IGNORE_SUFFIXES:
            continue
        out[p.relative_to(d).as_posix()] = p.read_bytes()
    return out


def compute_diff_touches(treat_dir: Path, control_dir: Path) -> list[str]:
    """Bot-tree-relative paths of every file that differs (by content or by
    presence) between treat_dir and control_dir. Excludes __pycache__/.pyc/
    .DS_Store -- build artefacts, not treatment."""
    t = _walk_tree(treat_dir)
    c = _walk_tree(control_dir)
    touched = {rel for rel in (t.keys() | c.keys()) if t.get(rel) != c.get(rel)}
    return sorted(touched)


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

def _normalize_for_match(path_str: str) -> str:
    """Reduce a path to its position WITHIN a bot tree, so a repo-root path
    (bots/_v135loki18/raid.py, as METRIC READS must be to resolve to a real
    file) and a bot-tree-relative path (raid.py, as a directory diff or
    prereg prose naturally writes it) name the same key for the file-level
    intersection test. Anything not under bots/ is left as-is."""
    parts = Path(path_str).as_posix().split("/")
    if len(parts) >= 3 and parts[0] == "bots":
        return "/".join(parts[2:])
    return "/".join(parts)


# ---------------------------------------------------------------------------
# Core check
# ---------------------------------------------------------------------------

class Result:
    def __init__(self, verdict, lines):
        self.verdict = verdict  # "PASS" | "INERT" | "MALFORMED"
        self.lines = lines


def _malformed(lines):
    return Result("MALFORMED", lines)


def run_check(prereg_path: Path | None, *, metric_reads_arg: str | None = None,
              diff_touches_arg: str | None = None, treat_dir: Path | None = None,
              control_dir: Path | None = None, cwd: Path = ROOT) -> Result:
    lines = []

    # --- resolve METRIC READS ------------------------------------------------
    block_reads = block_touches = None
    if prereg_path is not None:
        text = Path(prereg_path).read_text()
        block_reads, block_touches = parse_block(text)

    if metric_reads_arg is not None:
        reads = [parse_reads_entry(e) for e in metric_reads_arg.split(",") if e.strip()]
        reads_source = "--metric-reads flag"
    elif block_reads is not None:
        reads = block_reads
        reads_source = f"block in {prereg_path}"
    else:
        reads = None
        reads_source = None

    # --- resolve declared TREATMENT DIFF TOUCHES -----------------------------
    if diff_touches_arg is not None:
        declared_touches = [e.strip() for e in diff_touches_arg.split(",") if e.strip()]
        touches_source = "--diff-touches flag"
    elif block_touches is not None:
        declared_touches = block_touches
        touches_source = f"block in {prereg_path}"
    else:
        declared_touches = None
        touches_source = None

    # A declared touches value can be skipped ONLY if --treat/--control is
    # present to compute one instead -- otherwise there is no touches source
    # at all and that is unrecoverable (MALFORMED), same as missing reads.
    can_compute = treat_dir is not None and control_dir is not None
    if reads is None or (declared_touches is None and not can_compute):
        missing = []
        if reads is None:
            missing.append(READS_LABEL)
        if declared_touches is None:
            missing.append(TOUCHES_LABEL)
        lines.append("MALFORMED: machine-readable block missing or incomplete.")
        lines.append(f"  missing: {', '.join(missing)}")
        lines.append("  (no --metric-reads/--diff-touches/--treat+--control "
                      "override supplied either)")
        if prereg_path is not None:
            lines.append(f"  file: {prereg_path}")
        return _malformed(lines)

    lines.append(f"METRIC READS source: {reads_source}")
    for p, ln in reads:
        lines.append(f"  {p}" + (f":{ln}" if ln is not None else ""))
    if declared_touches is not None:
        lines.append(f"DECLARED DIFF TOUCHES source: {touches_source}")
        for p in declared_touches:
            lines.append(f"  {p}")
    else:
        lines.append("DECLARED DIFF TOUCHES source: none (relying entirely "
                      "on --treat/--control computation)")

    # --- resolve every read path to a real file ------------------------------
    unresolved = []
    for p, ln in reads:
        fp = (cwd / p) if not Path(p).is_absolute() else Path(p)
        if not fp.is_file():
            unresolved.append((p, ln))
    if unresolved:
        lines.append("MALFORMED: a METRIC READS path does not resolve to an "
                      "existing file -- an unnameable read path is not a "
                      "measured one.")
        for p, ln in unresolved:
            lines.append(f"  cannot resolve: {p}" + (f":{ln}" if ln is not None else ""))
        return _malformed(lines)

    # --- optionally recompute TOUCHES and cross-check ------------------------
    touches_used = declared_touches
    touches_used_source = f"declared ({touches_source})" if declared_touches is not None else None
    if can_compute:
        computed_touches = compute_diff_touches(Path(treat_dir), Path(control_dir))
        lines.append(f"COMPUTED DIFF TOUCHES ({treat_dir} vs {control_dir}):")
        for p in computed_touches:
            lines.append(f"  {p}")
        if declared_touches is not None:
            declared_norm = {_normalize_for_match(p) for p in declared_touches}
            computed_norm = {_normalize_for_match(p) for p in computed_touches}
            declared_only = sorted(declared_norm - computed_norm)
            computed_only = sorted(computed_norm - declared_norm)
            if declared_only or computed_only:
                lines.append("MALFORMED: declared TREATMENT DIFF TOUCHES "
                              "disagrees with the computed diff.")
                if declared_only:
                    lines.append(f"  declared but NOT in the computed diff: "
                                  f"{', '.join(declared_only)}")
                if computed_only:
                    lines.append(f"  in the computed diff but NOT declared: "
                                  f"{', '.join(computed_only)}")
                return _malformed(lines)
            touches_used_source = "computed (--treat/--control, verified == declared)"
        else:
            touches_used_source = "computed (--treat/--control; no declared " \
                                   "value existed to verify against)"
        touches_used = computed_touches

    lines.append(f"TOUCHES used for the intersection test: {touches_used_source}")

    # --- the actual gate -------------------------------------------------------
    reads_norm = {_normalize_for_match(p) for p, _ in reads}
    touches_norm = {_normalize_for_match(p) for p in touches_used}
    hit = reads_norm & touches_norm

    if not hit:
        lines.append("INERT: no file named in METRIC READS is touched by the "
                      "treatment diff. Nothing in the diff can move this "
                      "metric -- the leg may not be fired on this bar (D42).")
        lines.append(f"  reads (normalised):   {sorted(reads_norm)}")
        lines.append(f"  touches (normalised): {sorted(touches_norm)}")
        return Result("INERT", lines)

    lines.append(f"PASS: intersection = {sorted(hit)}")
    return Result("PASS", lines)


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

def _repo_path(*parts) -> Path:
    return ROOT.joinpath(*parts)


def selftest() -> int:
    cells = []

    # NEGATIVE -- must read INERT.
    r = run_check(
        _repo_path("docs", "prereg",
                   "PREREG-loki18-forward-sentinel-aims-at-core-2026-08-10.md"),
        metric_reads_arg="bots/_v135loki18/raid.py:433",
        diff_touches_arg="main.py",
        treat_dir=_repo_path("bots", "_v135loki18"),
        control_dir=_repo_path("bots", "_v130loki13"),
    )
    cells.append(("NEGATIVE_loki18", "INERT", r))

    # POSITIVE -- must read PASS.
    r = run_check(
        _repo_path("docs", "prereg", "PREREG-loki19-core-peck-2026-08-11.md"),
        metric_reads_arg="bots/_v136loki19/raid.py:256",
        diff_touches_arg="raid.py, doctrine.py",
        treat_dir=_repo_path("bots", "_v136loki19"),
        control_dir=_repo_path("bots", "_v130loki13"),
    )
    cells.append(("POSITIVE_loki19", "PASS", r))

    # MALFORMED: no block on disk, no override flags -- the real file as-is.
    r = run_check(
        _repo_path("docs", "prereg",
                   "PREREG-loki18-forward-sentinel-aims-at-core-2026-08-10.md"),
    )
    cells.append(("MALFORMED_NO_BLOCK", "MALFORMED", r))

    # MALFORMED: a read path naming a file that does not exist.
    r = run_check(
        _repo_path("docs", "prereg",
                   "PREREG-loki18-forward-sentinel-aims-at-core-2026-08-10.md"),
        metric_reads_arg="bots/_v135loki18/does_not_exist.py:1",
        diff_touches_arg="main.py",
    )
    cells.append(("MALFORMED_BAD_PATH", "MALFORMED", r))

    # MALFORMED: declared touches disagrees with computed (real loki18 diff
    # is main.py only; declare raid.py instead -- wrong on purpose).
    r = run_check(
        _repo_path("docs", "prereg",
                   "PREREG-loki18-forward-sentinel-aims-at-core-2026-08-10.md"),
        metric_reads_arg="bots/_v135loki18/raid.py:433",
        diff_touches_arg="raid.py",
        treat_dir=_repo_path("bots", "_v135loki18"),
        control_dir=_repo_path("bots", "_v130loki13"),
    )
    cells.append(("MALFORMED_DIFF_MISMATCH", "MALFORMED", r))

    n_ok = n_fail = 0
    fails = []
    for name, expected, result in cells:
        ok = result.verdict == expected
        n_ok, n_fail = n_ok + ok, n_fail + (not ok)
        print(f"\n=== CELL {name}  (expect {expected}, got {result.verdict}) "
              f"{'ok' if ok else 'FAIL'} ===")
        for ln in result.lines:
            print(f"  {ln}")
        if not ok:
            fails.append(f"{name}: expected {expected}, got {result.verdict}")

    print(f"\n  {n_ok} cells passed, {n_fail} failed, over {len(cells)} cells")
    for f in fails:
        print(f"    FAILED: {f}")
    print(f"\nINERT_CHECK_SELFTEST: {'PASS' if n_fail == 0 else 'FAIL'}")
    return 1 if n_fail else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="D42 mechanised: is a prereg's mechanism metric inert "
                     "against its own treatment diff?")
    ap.add_argument("prereg", nargs="?", type=Path,
                     help="prereg markdown file (optional if both "
                          "--metric-reads and --diff-touches are given)")
    ap.add_argument("--metric-reads",
                     help="override/supply 'path:line,path:line,...' "
                          "instead of parsing the file's block")
    ap.add_argument("--diff-touches",
                     help="override/supply 'path,path,...' instead of "
                          "parsing the file's block")
    ap.add_argument("--treat", type=Path,
                     help="treatment bot-tree dir; with --control, "
                          "recomputes and verifies TREATMENT DIFF TOUCHES")
    ap.add_argument("--control", type=Path,
                     help="control bot-tree dir, paired with --treat")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    if args.prereg is None and (args.metric_reads is None or args.diff_touches is None):
        ap.error("supply a prereg file, or both --metric-reads and --diff-touches")

    if bool(args.treat) != bool(args.control):
        ap.error("--treat and --control must be given together")

    result = run_check(
        args.prereg,
        metric_reads_arg=args.metric_reads,
        diff_touches_arg=args.diff_touches,
        treat_dir=args.treat,
        control_dir=args.control,
    )
    for ln in result.lines:
        print(ln)
    print(f"\nINERT_CHECK: {result.verdict}")
    return 0 if result.verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
