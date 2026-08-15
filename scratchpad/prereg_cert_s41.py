#!/usr/bin/env python3
"""SIDE-LANE INDEPENDENT FORCED-FAIL CERTIFICATION of tools/prereg_check.py.

Obligation inherited from the s40 side-lane wrap (a98c81f item 2): the
certification was OFFERED, ACCEPTED and UNRUN because the draft landed after the
wrap. Retro v1.10 books an offered-and-never-performed certification as this
lane's own Q8 failure mode.

⛔ WHY THIS IS NOT THE AUTHOR'S SELFTEST RUN AGAIN. The tool's own selftest
(50 cells, green) corrupts a SYNTHETIC fixture the tool's author wrote, and the
tool's docstring says so at line 806: *"the side lane's independent forced-fail
certification mutates REAL prereg text, and a fixture built by string generation
cannot be corrupted the same way."* A verification that shares the failure mode
of the thing it verifies is not a verification (drift-watch standing note, four
instances s26). The author's fixture cannot exercise:
  * house-style prose that MENTIONS a token without DECLARING it,
  * a declaration whose value is EMPTY,
  * real spellings of BOUNDARY / BAR / DOSE that the synthetic fixture normalises
    away by construction.

THE STANDARD (meta_attrib template, the repo's positive standard):
  * every check driven to its FAILING verdict,
  * on CORRUPTED REAL PREREG TEXT,
  * each corruption aimed at a DIFFERENT check,
  * calling the PRODUCTION function, never a re-implementation,
  * and COLLATERAL RECORDED — a corruption that trips five checks has not shown
    the sixth has teeth.

Run:  .venv/bin/python scratchpad/prereg_cert_s41.py
Gate on the last line (CERT: OK|FAIL), never on $? (CLAUDE.md).
"""
from __future__ import annotations

import contextlib
import io
import re
import pathlib
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import prereg_check as PC            # THE PRODUCTION MODULE. No second copy.

CARRIER_PATH = ROOT / "docs/research/PREREG-SPAWNPOCKET-2026-08-14.md"

# TAPE MODE has its own entry point (`PC.check_tape`), its own carrier and its
# own three checks, so it gets a REAL SHARD TAPE rather than prereg prose. This
# one is git-tracked and passes clean today (CELL 0T asserts it), which is what
# makes each mutation below attributable.
TAPE_PATH = ROOT / "scratchpad/overnight/CRASHS.tsv"

# OB13's untracked-arm gap is a property of GIT STATE, not of the text: the
# check fires when a path the prereg NAMES exists on disk and `git ls-files`
# cannot see it. The harness MANUFACTURES that precondition in a temp tree it
# creates and removes itself -- a cell that fired only because somebody had left
# a bot tree uncommitted today would stop certifying the day they committed it,
# silently, which is the failure mode this whole file exists to catch.
PROBE_ARM = ROOT / "scratchpad/.cert_untracked_arm_probe"

# The ~15-line REGISTRATION BLOCK the builder specced as the migration. It is
# appended to REAL prereg prose, so every corruption below runs against a
# document that is real text plus this block -- not against a generated string.
# Values are SPAWNPOCKET's own where the document already carries them.
# The OBLIGATION 17 line (METRIC WINDOW / GATING CONSTANTS / MECHANISM CAN OCCUR)
# is SPAWNPOCKET's own fact too: the pave guard the metric reads is unconditional
# on round, so the window is the whole game and no gate binds it. It is declared
# CLEAN in the carrier ON PURPOSE -- CELL 0 then certifies the line itself is not
# a defect, and every OB17 corruption below is a minimal mutation of a line the
# baseline has already passed.
REGISTRATION_BLOCK = """

## REGISTRATION BLOCK (side-lane certification carrier — NOT a live registration)

**TARGET BAND: N/A - local screen, zero rated exposure, no opponent is challenged**
**PINNED: N/A - local corefill screen, no platform opponent to pin**
**SURFACE: local**
**CLUSTER UNIT: none - balanced-by-construction local shards, pair-weighted DEFF 0.98**
**ESTIMATOR: pooled game share, games-level, unweighted**
**PLANNED n: 2700 games**
**BOUNDARY: 2700 games**
**CUT-SHORT: below 900 games this screen publishes descriptive tallies only and takes NO comparative look**
**BASE RATE: 50.0**
**BAR SOURCE: pre-registered treatment bar, this document**
**BASE RATE SOURCE: local corefill balanced screen, 50/50 by construction, n = 2,700 rows**
**REFERENCE n: none**
**MECHANISM METRIC READS: eco.py:934. TREATMENT DIFF TOUCHES: eco.py. INTERSECTION: yes.**
**METRIC WINDOW: r0-r1000, every round of every shard game. GATING CONSTANTS: none - the pave guard is unconditional on round. MECHANISM CAN OCCUR IN WINDOW: yes.**
**GATE RESOLUTION: the pocket gate discriminates its branches at n >= 900 rows; UNRESOLVED means the RESTRICTION (no ship)**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock**
**SEGMENT VALUE CEILING: 14.0% pairing share x 6.0pp on-segment = 0.84pp pooled**
**PROVENANCE: docs/research/DESIGN-64-spawnpocket-2026-08-14.md · corpus/ladder_games.tsv · bots/_v223sealrepair/eco.py**
**DOSE: pocket-entries 37.0/game vs flag-off 0.0/game (n=24 probe shards)**
"""

DIFF = ["eco.py"]                      # a fixed diff list, so OB13 is computable


def run(text, label, diff_paths=None, fire=False):
    """PRODUCTION path. Returns (set of failing check ids, warns).

    `diff_paths=None` means the harness's fixed DIFF; a cell that needs the
    OTHER world -- an arm tree that yields NO diff at all -- passes an explicit
    empty list, which is the condition the tool's cannot-compute branch reads.
    """
    _rows, fails, warns = PC.run_checks(
        text, label, quiet=True, fire=fire,
        diff_paths=DIFF if diff_paths is None else diff_paths)
    return {x[0] for x in fails}, warns


def run_tape(text):
    """PRODUCTION path for TAPE MODE. Returns the set of failing check ids.

    `PC.check_tape` takes a PATH, prints its verdicts and returns an exit code,
    so the ids are read off ITS OWN STDOUT rather than re-derived here -- the
    same rule as everywhere else in this file: call the production function,
    never a second copy of it.
    """
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "tape.tsv"
        p.write_text(text)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            PC.check_tape(p)
    return {m.group(1) for m in
            (re.match(r"FAIL\s+([A-Z0-9_]+)", l) for l in buf.getvalue().splitlines())
            if m}


# ---------------------------------------------------------------------------
# CORRUPTIONS — one per check, each aimed at a DIFFERENT check, each a mutation
# of the carrier's REAL text or of the registration block appended to it.
# `want` is the id that MUST appear in the failure set.
# ---------------------------------------------------------------------------
def _sub(old, new):
    def f(t):
        assert old in t, f"corruption anchor absent from carrier: {old!r}"
        return t.replace(old, new, 1)
    return f


def _drop_line(substr):
    def f(t):
        keep = [l for l in t.splitlines() if substr not in l]
        assert len(keep) < len(t.splitlines()), f"nothing to drop for {substr!r}"
        return "\n".join(keep)
    return f


def _mode(fn, **kw):
    """Run the corrupted text under a NON-DEFAULT INVOCATION.

    ⛔ FOR FOUR CELLS THE INVOCATION **IS** PART OF THE CORRUPTION, and no
    mutation of the text alone can reach them. THREE are mode-gated -- the tool
    escalates a WARN to a FAIL under `--fire`, which is a real production mode
    (`check_file(path, fire=True)`, the CLI flag) and is exactly the moment the
    defect becomes fatal. TWO are diff-gated: they read the world where the arm
    tree yields NO diff, which the harness's fixed DIFF list forecloses by
    construction. (OB13_NOT_COMPUTED is both.) Everything still goes through the
    same production call, and each of the four is shown to fire ONLY under its
    own invocation: the printed `[invocation: ...]` tag is the other verdict.
    """
    return lambda t: (fn(t), kw)


def _same(t):
    """No text mutation -- the cell's whole corruption is its invocation."""
    return t


def _as_panel(t):
    """The carrier RE-REGISTERED AS A PANEL LEG, and NOT a corruption.

    ⛔ WHY A SECOND BASE FORM EXISTS AT ALL: the POOL ERA family is UNREACHABLE
    from this carrier as written. SPEC-pool-era §6 exempts LOCAL surfaces (our
    own fixture config, measured), so a local screen cannot drive those three
    checks to ANY verdict -- pass or fail. Flipping the surface alone would
    trip BOUNDARY_UNITS and BAR_RESOLVABLE as collateral, and a cell whose
    target id is buried in three other failures certifies nothing, so the flip
    carries the arithmetic it makes necessary: a boundary in both units (5x),
    a bar the unrated DEFF can resolve at n=2,700 (+-2.3pp), and the panel
    spellings of the fields whose values named the local fixture. CELL 0b
    certifies THIS form passes clean, exactly as CELL 0 does for the carrier.
    """
    return (t.replace("SURFACE: local", "SURFACE: unrated")
             .replace("TARGET BAND: N/A - local screen, zero rated exposure, no opponent "
                      "is challenged",
                      "TARGET BAND: 0033 +120, The Bisons +41, gaps +41..+120, win pays "
                      "17.89..21.30, reachable YES")
             .replace("PINNED: N/A - local corefill screen, no platform opponent to pin",
                      "PINNED: NO - calibration panel, churn is signal not noise")
             .replace("CLUSTER UNIT: none - balanced-by-construction local shards, "
                      "pair-weighted DEFF 0.98",
                      "CLUSTER UNIT: match - one opponent per accepted match")
             .replace("BOUNDARY: 2700 games", "BOUNDARY: 540 accepts = 2700 games")
             .replace("BAR: ≥52.0", "BAR: ≥55.0")
             .replace("BASE RATE SOURCE: local corefill balanced screen, 50/50 by "
                      "construction, n = 2,700 rows",
                      "BASE RATE SOURCE: our own share against these five cells, "
                      "corpus/meta_join non-ladder, n = 2,700 games")
             + "\n**POOL ERA: 2026-08-13T07:12:59Z..now**\n")


def _panel(fn):
    """Apply a corruption to the PANEL form rather than the local carrier."""
    return lambda t: fn(_as_panel(t))


CORRUPTIONS = [
    # --- PRESENCE, each a different deletion or malformation -----------------
    ("LOCK",              "STATUS line deleted entirely",
     _drop_line("STATUS:")),
    ("LOCK",              "STATUS present but does not say BEFORE (malformed value)",
     _sub("STATUS: committed BEFORE", "STATUS: committed AFTER")),
    ("TARGET_BAND",       "TARGET BAND deleted",              _drop_line("TARGET BAND:")),
    ("TARGET_BAND",       "TARGET BAND present but bare `N/A` with no reason",
     _sub("TARGET BAND: N/A - local screen, zero rated exposure, no opponent is challenged",
          "TARGET BAND: N/A")),
    ("PINNED",            "PINNED deleted",                   _drop_line("PINNED:")),
    ("SURFACE",           "SURFACE deleted",                  _drop_line("SURFACE:")),
    ("SURFACE",           "SURFACE names a surface that does not exist",
     _sub("SURFACE: local", "SURFACE: arena")),
    ("CLUSTER_UNIT",      "CLUSTER UNIT deleted",             _drop_line("CLUSTER UNIT:")),
    ("ESTIMATOR",         "ESTIMATOR deleted",                _drop_line("ESTIMATOR:")),
    ("PLANNED_N",         "PLANNED n deleted",                _drop_line("PLANNED n:")),
    ("CUT_SHORT",         "CUT-SHORT deleted",                _drop_line("CUT-SHORT:")),
    ("BOUNDARY",          "BOUNDARY deleted",                 _drop_line("BOUNDARY:")),
    ("BAR",               "the carrier's own real BAR line deleted",
     _drop_line("BAR:")),
    ("BASE_RATE",         "BASE RATE deleted",                _drop_line("BASE RATE:")),
    ("SOURCES",           "BASE RATE SOURCE deleted, BAR SOURCE kept (companion-token half)",
     _drop_line("BASE RATE SOURCE:")),
    ("OB13",              "TREATMENT DIFF TOUCHES + INTERSECTION removed from the OB13 line",
     _sub("MECHANISM METRIC READS: eco.py:934. TREATMENT DIFF TOUCHES: eco.py. INTERSECTION: yes.",
          "MECHANISM METRIC READS: eco.py:934.")),
    ("OB12_GATE",         "GATE RESOLUTION deleted",          _drop_line("GATE RESOLUTION:")),
    ("OB12_DEFAULT",      "every occurrence of UNRESOLVED removed (the pre-committed default)",
     lambda t: t.replace("UNRESOLVED", "undecided").replace("UNRESOLVABLE", "undecidable")),
    ("OB7_PRESTATE",      "PRE-STATE deleted",                _drop_line("PRE-STATE:")),
    ("OB15A_SEGMENT",     "both segment declarations deleted",
     lambda t: "\n".join(l for l in t.splitlines()
                         if "MAP SEGMENT" not in l and "PRIMARY SEGMENT" not in l)),
    ("OB15A_DIRECTION",   "EXPECTED DIRECTION deleted while a named segment stands",
     _drop_line("EXPECTED DIRECTION:")),
    ("OB15B_ONE_PRIMARY", "a SECOND primary segment declared (subgroup fishing)",
     lambda t: t + "\n**PRIMARY SEGMENT: {valkyrie, ragnarok}**\n"),
    ("SEGMENT_CEILING",   "SEGMENT VALUE CEILING deleted while a named segment stands",
     _drop_line("SEGMENT VALUE CEILING:")),
    ("OB14_CHURN",        "a CELLS: line ACTIVATES the conditional rule, churn undeclared",
     lambda t: t + "\n**CELLS: D1 0033 · D2 LingLing40 · D3 Juusto**\n"),
    ("FALSIFIER",         "every FALSIFIER heading and token removed",
     lambda t: t.replace("FALSIFIER", "closing note").replace("falsifier", "closing note")),
    ("PROVENANCE",        "PROVENANCE deleted",               _drop_line("PROVENANCE:")),
    ("PROVENANCE",        "PROVENANCE present but describes its inputs instead of naming them",
     _sub("PROVENANCE: docs/research/DESIGN-64-spawnpocket-2026-08-14.md · corpus/ladder_games.tsv · bots/_v223sealrepair/eco.py",
          "PROVENANCE: n/a")),
    ("DOSE",              "DOSE deleted",                     _drop_line("DOSE:")),

    # --- ARITHMETIC, each a different identity broken ------------------------
    # ⛔ THE ACCEPTS/GAMES IDENTITY IS A **PANEL** FAILURE MODE (CAL-8), so it is driven
    # on a PANEL surface. The tool exempts local surfaces because a local shard has no
    # accept/attempt distinction to get wrong (1 row = 1 game) — correct, and my earlier
    # fixture declared "540 accepts" under `SURFACE: local`, which is a panel template
    # wearing a local surface and is not a document anyone would write. THE FIXTURE WAS
    # WRONG, NOT THE TOOL; recorded rather than quietly re-pointed.
    ("BOUNDARY_UNITS",    "PANEL surface, boundary counted over ATTEMPTS (540 accepts as 540 games)",
     lambda t: t.replace("SURFACE: local", "SURFACE: unrated")
                .replace("CLUSTER UNIT: none - balanced-by-construction local shards, pair-weighted DEFF 0.98",
                         "CLUSTER UNIT: match - one opponent per arm")
                .replace("BOUNDARY: 2700 games", "BOUNDARY: 540 accepts = 540 games")),
    ("BOUNDARY_UNITS",    "PANEL surface, BOUNDARY missing a unit entirely",
     lambda t: t.replace("SURFACE: local", "SURFACE: unrated")
                .replace("BOUNDARY: 2700 games", "BOUNDARY: 540 accepts")),
    ("BOUNDARY_VS_N",     "PLANNED n and BOUNDARY disagree",
     _sub("PLANNED n: 2700 games", "PLANNED n: 2000 games")),
    ("CUT_SHORT_FLOOR",   "cut-short floor raised ABOVE the leg's own PLANNED n (unreachable)",
     _sub("below 900 games", "below 3000 games")),
    ("BAR_RESOLVABLE",    "bar moved inside the half-width the fixture can produce",
     _sub("BAR: ≥52.0", "BAR: ≥50.9")),
    ("BAR_NULL",          "the bar IS the comparator base rate",
     _sub("BAR: ≥52.0", "BAR: ≥50.0")),
    ("REFERENCE_FLOOR",   "a retired reference of n=155 under a 2.0pp margin (CAL-7 P1)",
     lambda t: t.replace("REFERENCE n: none",
                         "REFERENCE n: 155 (retired v125 six-cell reference, cannot grow)\n"
                         "**REFERENCE SURFACE: rated**\n**REFERENCE CLUSTER UNIT: match**")),
    ("SEGMENT_CEILING",   "the declared ceiling does not equal share x effect",
     _sub("14.0% pairing share x 6.0pp on-segment = 0.84pp pooled",
          "14.0% pairing share x 6.0pp on-segment = 4.20pp pooled")),
    ("DOSE_BOTH_VERDICTS", "a dose line quoting ONE number (a counter reading)",
     _sub("DOSE: pocket-entries 37.0/game vs flag-off 0.0/game (n=24 probe shards)",
          "DOSE: pocket-entries 37.0/game (n=24 probe shards)")),
    ("DOSE_BOTH_VERDICTS", "treatment and flag-off IDENTICAL (the probe separated nothing)",
     _sub("vs flag-off 0.0/game", "vs flag-off 37.0/game")),
    ("OB13_INTERSECTION", "the metric's file is NOT in the real diff (LOKI-18 exactly)",
     _sub("MECHANISM METRIC READS: eco.py:934", "MECHANISM METRIC READS: raid.py:415")),
    ("OB13_INTERSECTION", "the prereg declares its own bar INERT",
     _sub("INTERSECTION: yes.", "INTERSECTION: no.")),

    # --- OB13, THE TWO CANNOT-COMPUTE BRANCHES. Both need the world where the
    # diff is EMPTY, which the fixed DIFF list above forecloses -- so both pass
    # `diff_paths=[]`. They are DIFFERENT facts and the tool separates them: an
    # arm tree that is ABSENT (locked before it was built, legitimate, FAILs
    # only under --fire) versus one that is PRESENT and invisible to git.
    ("OB13_NOT_COMPUTED", "no diff exists to intersect, at FIRE time (tree named, none untracked)",
     _mode(_same, diff_paths=[], fire=True)),
    ("OB13_UNTRACKED_ARM", "TREATMENT TREE names an arm that EXISTS on disk and git cannot see",
     _mode(lambda t: t + f"\n**TREATMENT TREE: {PROBE_ARM.relative_to(ROOT)}/eco.py**\n",
           diff_paths=[])),

    # --- OBLIGATION 17 (routed), each a minimal mutation of the ONE clean OB17
    # line CELL 0 has already passed, so no cell can trip its id by inventing a
    # block the baseline never certified.
    ("METRIC_WINDOW_PRESENT", "METRIC WINDOW deleted, at FIRE time (WARN at lock, FAIL fired)",
     _mode(_drop_line("METRIC WINDOW:"), fire=True)),
    ("METRIC_WINDOW_PARSE", "the window is a placeholder and names no round",
     _sub("METRIC WINDOW: r0-r1000, every round of every shard game.",
          "METRIC WINDOW: TBD, the shard runner decides.")),
    ("METRIC_WINDOW_DECLARED_INERT", "the prereg declares its own mechanism CANNOT occur in the window",
     _sub("MECHANISM CAN OCCUR IN WINDOW: yes.",
          "MECHANISM CAN OCCUR IN WINDOW: no - the pave path is gated off before r120.")),
    ("METRIC_WINDOW_INERT", "window r0-r75 against the tree's own HUNT_MIN_RND=120 (#67 exactly)",
     lambda t: t.replace("METRIC WINDOW: r0-r1000, every round of every shard game.",
                         "METRIC WINDOW: r0-r75, the opening only.")
                .replace("GATING CONSTANTS: none - the pave guard is unconditional on round",
                         "GATING CONSTANTS: HUNT_MIN_RND=120")),
    ("METRIC_WINDOW_GATE_STALE", "a GATING CONSTANTS value the tree contradicts (declared 999, tree 120)",
     _sub("GATING CONSTANTS: none - the pave guard is unconditional on round",
          "GATING CONSTANTS: HUNT_MIN_RND=999")),
    ("METRIC_WINDOW_NOT_COMPUTED", "PROVENANCE points at a tree that is not on disk, at FIRE time",
     _mode(_sub("bots/_v223sealrepair/eco.py", "bots/_v999ghost/eco.py"), fire=True)),

    # --- POOL ERA, on the PANEL form (see _as_panel: SPEC §6 exempts LOCAL, so
    # these three are unreachable from the carrier's own surface).
    ("POOL_ERA_PRESENT",  "POOL ERA deleted while a base rate and a ceiling carry shares",
     _panel(_drop_line("POOL ERA:"))),
    ("POOL_ERA_NONEMPTY", "POOL ERA typed and left EMPTY (empty is absent, no exceptions)",
     _panel(_sub("POOL ERA: 2026-08-13T07:12:59Z..now", "POOL ERA:"))),
    ("POOL_ERA_SINGLE",   "the window spans the derived 2026-08-13 rotation, unjustified",
     _panel(_sub("POOL ERA: 2026-08-13T07:12:59Z..now",
                 "POOL ERA: 2026-08-05T19:42:43Z..2026-08-15T00:00:00Z"))),
]


# ---------------------------------------------------------------------------
# TAPE MODE — a SECOND entry point (`PC.check_tape`), a SECOND real carrier.
# Its three checks read a shard result TAPE, not prereg prose, and they can only
# be driven from a tape; the corruptions are minimal mutations of a real, clean,
# git-tracked leg tape.
# ---------------------------------------------------------------------------
TAPE_CORRUPTIONS = [
    ("TAPE_FIXTURE_HEADER", "the header's required `start=` field removed",
     _sub("\tstart=2026-08-14T21:22:05Z", "")),
    ("TAPE_START_PARSES",   "start= carries a human clock instead of an ISO UTC stamp",
     _sub("start=2026-08-14T21:22:05Z", "start=last night just after nine")),
    ("TAPE_ROW_SCHEMA",     "the `cond` column dropped from the row header",
     _sub("ts\tshard\tgame\tmap\tseed\tseat\twinner\tcond\tturns",
          "ts\tshard\tgame\tmap\tseed\tseat\twinner\tturns")),
]


def main() -> int:
    carrier = CARRIER_PATH.read_text() + REGISTRATION_BLOCK
    tape = TAPE_PATH.read_text()
    bad = 0

    print("SIDE-LANE FORCED-FAIL CERTIFICATION — tools/prereg_check.py")
    print(f"carrier: {CARRIER_PATH.relative_to(ROOT)} (REAL, "
          f"{len(CARRIER_PATH.read_text().splitlines())} lines) + a "
          f"{len(REGISTRATION_BLOCK.strip().splitlines())}-line registration block")
    print(f"tape carrier: {TAPE_PATH.relative_to(ROOT)} (REAL, "
          f"{len(tape.splitlines())} lines, git-tracked)\n")

    # --- CELL 0. The carrier must PASS, or every FAIL below is unattributable.
    base_fails, base_warns = run(carrier, "<carrier>")
    ok = not base_fails
    print(f"[{'ok ' if ok else 'BAD'}] CELL 0  carrier passes clean "
          f"({len(base_fails)} failure(s){': ' + ', '.join(sorted(base_fails)) if base_fails else ''})")
    if base_warns:
        for w in base_warns:
            print(f"        carrier WARN: {w[:100]}")
    bad += 0 if ok else 1
    if not ok:
        print("\nCERT: FAIL  — the carrier does not pass, so no corruption is attributable.")
        return 1

    # --- CELL 0b. The PANEL form of the carrier must ALSO pass clean, for the
    # same reason: the POOL ERA cells corrupt that form, so if the re-
    # registration itself failed anything, their target ids would be firing
    # inside a document that was already broken.
    panel_fails, _pw = run(_as_panel(carrier), "<panel carrier>")
    ok = not panel_fails
    print(f"[{'ok ' if ok else 'BAD'}] CELL 0b panel form of the carrier passes clean "
          f"({len(panel_fails)} failure(s){': ' + ', '.join(sorted(panel_fails)) if panel_fails else ''})")
    bad += 0 if ok else 1

    # --- CELL 0T. Same contract for TAPE MODE's own carrier.
    tape_fails = run_tape(tape)
    ok = not tape_fails
    print(f"[{'ok ' if ok else 'BAD'}] CELL 0T real shard tape passes clean "
          f"({len(tape_fails)} failure(s){': ' + ', '.join(sorted(tape_fails)) if tape_fails else ''})")
    bad += 0 if ok else 1

    # --- CELLS 1..N. One corruption per check, collateral recorded. ----------
    print(f"\nFORCED FAILURES — {len(CORRUPTIONS) + len(TAPE_CORRUPTIONS)} corruptions "
          f"of REAL text, each aimed at a DIFFERENT check:")
    seen = set()
    for want, label, fn in CORRUPTIONS:
        try:
            out = fn(carrier)
        except AssertionError as e:
            print(f"[BAD] {want:<19} CORRUPTION DID NOT APPLY: {e}")
            bad += 1
            continue
        # A cell whose corruption includes its INVOCATION returns (text, kwargs).
        txt, kw = out if isinstance(out, tuple) else (out, {})
        fails, _w = run(txt, f"<{want}>", **kw)
        hit = want in fails
        collateral = sorted(fails - {want})
        # ⛔ A MODE-GATED CELL OWES THE OTHER VERDICT, and it is cheap: run the
        # SAME text under the DEFAULT invocation. If the id fires there too then
        # the mutation, not the mode, is doing the work and the cell has not
        # certified the escalation it claims to certify.
        note = ""
        if kw:
            ctrl, _cw = run(txt, f"<{want}:default>")
            if want in ctrl:
                hit = False
                note = "   *** ALSO FIRES UNDER THE DEFAULT INVOCATION ***"
            else:
                note = f"   [invocation: {kw}; silent under the default]"
        bad += 0 if hit else 1
        seen.add(want)
        print(f"[{'ok ' if hit else 'BAD'}] {want:<19} {label[:66]}")
        print(f"      {'names its own rule' if hit else '*** DID NOT FIRE ***'}"
              f"   collateral: {collateral if collateral else 'none'}{note}")

    for want, label, fn in TAPE_CORRUPTIONS:
        try:
            txt = fn(tape)
        except AssertionError as e:
            print(f"[BAD] {want:<19} CORRUPTION DID NOT APPLY: {e}")
            bad += 1
            continue
        fails = run_tape(txt)
        hit = want in fails
        collateral = sorted(fails - {want})
        bad += 0 if hit else 1
        seen.add(want)
        print(f"[{'ok ' if hit else 'BAD'}] {want:<19} {label[:66]}")
        print(f"      {'names its own rule' if hit else '*** DID NOT FIRE ***'}"
              f"   collateral: {collateral if collateral else 'none'}   [tape mode]")

    # --- COVERAGE. A check with no corruption has not been certified. --------
    # ⛔ FIXED 2026-08-15 (s42), reported by the builder, verified by me.
    # WAS: {r["id"] for r in PC.RULES} | <a hand-maintained set>.
    # PC.RULES holds only the PRESENCE rules; every ARITHMETIC and OBLIGATION
    # check is emitted inline via fails.append((...)) and is INVISIBLE to it.
    # So the denominator could not grow when the tool did, and this harness
    # printed "uncovered: none" while OB17's five ids were wholly uncovered.
    # A denominator that cannot grow reports COMPLETE by construction -- D33 in
    # the instrument that certifies the instruments. It ran four times tonight.
    # NOW: derive from BOTH declaration styles in the tool's own source.
    _src = pathlib.Path(PC.__file__).read_text()
    all_ids = ({r["id"] for r in PC.RULES}
               | set(re.findall(r'fails\.append\(\(\s*"([A-Z0-9_]+)"', _src))
               | set(re.findall(r'dict\(id="([A-Z0-9_]+)"', _src)))
    uncovered = sorted(all_ids - seen)
    print(f"\nCOVERAGE  {len(seen)}/{len(all_ids)} checks driven to FAIL on real text; "
          f"uncovered: {uncovered if uncovered else 'none'}")
    bad += len(uncovered)

    print(f"\nCERT: {'OK' if not bad else 'FAIL'}"
          + ("" if not bad else f"  ({bad} cell(s) wrong)"))
    return 1 if bad else 0


def _with_probe_arm(fn):
    """Create, then ALWAYS remove, the untracked arm tree OB13's gap needs.

    It is written under `scratchpad/` rather than `bots/` so that a killed run
    leaves an obviously-named scratch directory and never a bot tree somebody
    might mistake for an arm. `git ls-files` sees nothing here by construction,
    which is the precondition -- and the cell asserts it by FIRING, not by this
    function claiming it.
    """
    PROBE_ARM.mkdir(parents=True, exist_ok=True)
    (PROBE_ARM / "eco.py").write_text(
        "# transient probe tree written by scratchpad/prereg_cert_s41.py\n")
    try:
        return fn()
    finally:
        shutil.rmtree(PROBE_ARM, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(_with_probe_arm(main))
