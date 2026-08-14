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

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import prereg_check as PC            # THE PRODUCTION MODULE. No second copy.

CARRIER_PATH = ROOT / "docs/research/PREREG-SPAWNPOCKET-2026-08-14.md"

# The ~15-line REGISTRATION BLOCK the builder specced as the migration. It is
# appended to REAL prereg prose, so every corruption below runs against a
# document that is real text plus this block -- not against a generated string.
# Values are SPAWNPOCKET's own where the document already carries them.
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
**GATE RESOLUTION: the pocket gate discriminates its branches at n >= 900 rows; UNRESOLVED means the RESTRICTION (no ship)**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock**
**SEGMENT VALUE CEILING: 14.0% pairing share x 6.0pp on-segment = 0.84pp pooled**
**PROVENANCE: docs/research/DESIGN-64-spawnpocket-2026-08-14.md · corpus/ladder_games.tsv · bots/_v223sealrepair/eco.py**
**DOSE: pocket-entries 37.0/game vs flag-off 0.0/game (n=24 probe shards)**
"""

DIFF = ["eco.py"]                      # a fixed diff list, so OB13 is computable


def run(text, label):
    """PRODUCTION path. Returns (set of failing check ids, warns)."""
    _rows, fails, warns = PC.run_checks(text, label, diff_paths=DIFF, quiet=True)
    return {x[0] for x in fails}, warns


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
]


def main() -> int:
    carrier = CARRIER_PATH.read_text() + REGISTRATION_BLOCK
    bad = 0

    print("SIDE-LANE FORCED-FAIL CERTIFICATION — tools/prereg_check.py")
    print(f"carrier: {CARRIER_PATH.relative_to(ROOT)} (REAL, "
          f"{len(CARRIER_PATH.read_text().splitlines())} lines) + a "
          f"{len(REGISTRATION_BLOCK.strip().splitlines())}-line registration block\n")

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

    # --- CELLS 1..N. One corruption per check, collateral recorded. ----------
    print(f"\nFORCED FAILURES — {len(CORRUPTIONS)} corruptions of REAL text, "
          f"each aimed at a DIFFERENT check:")
    seen = set()
    for want, label, fn in CORRUPTIONS:
        try:
            txt = fn(carrier)
        except AssertionError as e:
            print(f"[BAD] {want:<19} CORRUPTION DID NOT APPLY: {e}")
            bad += 1
            continue
        fails, _w = run(txt, f"<{want}>")
        hit = want in fails
        collateral = sorted(fails - {want})
        bad += 0 if hit else 1
        seen.add(want)
        print(f"[{'ok ' if hit else 'BAD'}] {want:<19} {label[:66]}")
        print(f"      {'names its own rule' if hit else '*** DID NOT FIRE ***'}"
              f"   collateral: {collateral if collateral else 'none'}")

    # --- COVERAGE. A check with no corruption has not been certified. --------
    all_ids = {r["id"] for r in PC.RULES} | {
        "BOUNDARY_UNITS", "BOUNDARY_VS_N", "BAR_RESOLVABLE", "BAR_NULL",
        "REFERENCE_FLOOR", "SEGMENT_CEILING", "DOSE_BOTH_VERDICTS", "OB13_INTERSECTION"}
    uncovered = sorted(all_ids - seen)
    print(f"\nCOVERAGE  {len(seen)}/{len(all_ids)} checks driven to FAIL on real text; "
          f"uncovered: {uncovered if uncovered else 'none'}")
    bad += len(uncovered)

    print(f"\nCERT: {'OK' if not bad else 'FAIL'}"
          + ("" if not bad else f"  ({bad} cell(s) wrong)"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
