#!/usr/bin/env python3
"""SIDE-LANE CERTIFICATION, PART 2 — CAN A CHECK BE SATISFIED SPURIOUSLY?

Part 1 (`prereg_cert_s41.py`) drove all 31 checks to FAIL on corrupted REAL
prereg text: every check CAN fire. **That is only half of a certification.**

⛔ THE OTHER HALF, and it is the half this repo keeps paying for: a guard that
fires when its token is DELETED has been shown to detect ABSENCE. It has NOT
been shown to detect a token that is PRESENT AND EMPTY, PRESENT AND UNPARSEABLE,
or MENTIONED IN PROSE. Standing note (s29, four instances): *"a check only checks
once something forces it to produce an answer it could get wrong."* Deletion is
the comfortable corruption — it is the one the author reaches for, and it is the
one a real defective prereg will NOT look like, because nobody omits a field
after a checker starts demanding it. **They will type the field and leave it
empty.**

Each hypothesis below is a SPECIFIC defective document that a real author could
plausibly commit. The question for each: does `PREREG_CHECK` come out OK?
An OK verdict on any of them is a hole, reported with the line that produces it.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import prereg_check as PC

CARRIER_PATH = ROOT / "docs/research/PREREG-SPAWNPOCKET-2026-08-14.md"
sys.path.insert(0, str(ROOT / "scratchpad"))
from prereg_cert_s41 import REGISTRATION_BLOCK, DIFF


def verdict(text, label):
    _rows, fails, warns = PC.run_checks(text, label, diff_paths=DIFF, quiet=True)
    return ("FAIL" if fails else "OK"), {x[0] for x in fails}, warns


HYPOTHESES = [
    ("H1  EMPTY VALUES",
     "every declaration present, every value EMPTY — the shape a real author "
     "produces the day a checker starts demanding fields",
     lambda t: t.replace("ESTIMATOR: pooled game share, games-level, unweighted", "ESTIMATOR:")
                .replace("PRE-STATE: the predicted-change set is NOT already in the target state at lock",
                         "PRE-STATE:")
                .replace("CUT-SHORT: below 900 games this screen publishes descriptive tallies "
                         "only and takes NO comparative look", "CUT-SHORT:")),

    ("H2  PLACEHOLDER VALUES",
     "every declaration present, values are TBD / unknown / see below",
     lambda t: t.replace("ESTIMATOR: pooled game share, games-level, unweighted",
                         "ESTIMATOR: TBD")
                .replace("PRE-STATE: the predicted-change set is NOT already in the target state at lock",
                         "PRE-STATE: see below")
                .replace("CUT-SHORT: below 900 games this screen publishes descriptive tallies "
                         "only and takes NO comparative look", "CUT-SHORT: TBD")),

    ("H3  UNPARSEABLE n DISABLES THE ARITHMETIC",
     "PLANNED n present but not a number — presence passes and every "
     "resolvability check silently goes `not computed`. This is optional "
     "stopping walking back in through a door the presence layer holds open.",
     lambda t: t.replace("PLANNED n: 2700 games", "PLANNED n: fixed at fire time")
                .replace("BOUNDARY: 540 accepts = 2700 games",
                         "BOUNDARY: fixed at fire time")),

    ("H4  PROSE QUOTING THE OBLIGATION TEMPLATE",
     "the document QUOTES Obligation 13's own template sentence instead of "
     "declaring it — the same class as the false positive the author already "
     "found on this very carrier's PRIMARY SEGMENT prose",
     lambda t: t.replace(
         "**MECHANISM METRIC READS: eco.py:934. TREATMENT DIFF TOUCHES: eco.py. INTERSECTION: yes.**",
         "Obligation 13 asks every prereg to carry a line of the form "
         "`MECHANISM METRIC READS: <file:line>. TREATMENT DIFF TOUCHES: <paths>. "
         "INTERSECTION: <yes/no>.` and we should adopt it next session.")),

    ("H5  A NEGATED DECLARATION",
     "the fields are declared and each says the obligation was NOT met",
     lambda t: t.replace("PROVENANCE: docs/research/DESIGN-64-spawnpocket-2026-08-14.md · "
                         "corpus/ladder_games.tsv · bots/_v223sealrepair/eco.py",
                         "PROVENANCE: not recorded for this leg")
                .replace("DOSE: pocket-entries 37.0/game vs flag-off 0.0/game (n=24 probe shards)",
                         "DOSE: no probe was run vs no control (n=0)")),

    ("H6  BAR AND BASE RATE IN DIFFERENT UNITS",
     "BAR written as a proportion (0.52) against a BASE RATE in points (50.0) — "
     "the 0..1 heuristic the tool documents as unreachable in practice",
     lambda t: t.replace("BAR: ≥52.0", "BAR: ≥0.52")),

    ("H7  A REFERENCE THAT CANNOT GROW, DECLARED AS PROSE",
     "REFERENCE n names a retired sample in words, not digits, so the floor "
     "check reports n/a instead of computing CAL-7's own failure",
     lambda t: t.replace("REFERENCE n: none",
                         "REFERENCE n: the retired v125 six-cell rated reference, which cannot grow")),
]


def main() -> int:
    carrier = CARRIER_PATH.read_text() + REGISTRATION_BLOCK
    base, base_fails, _ = verdict(carrier, "<carrier>")
    print("SIDE-LANE CERTIFICATION PART 2 — SPURIOUS SATISFACTION")
    print(f"carrier baseline: PREREG_CHECK: {base}\n")
    if base != "OK":
        print(f"CERT2: FAIL — carrier does not pass ({base_fails})")
        return 1

    holes = []
    for name, why, fn in HYPOTHESES:
        v, fails, warns = verdict(fn(carrier), name)
        hole = (v == "OK")
        holes.append((name, hole))
        print(f"[{'HOLE' if hole else 'held'}] {name}")
        print(f"       {why}")
        print(f"       PREREG_CHECK: {v}"
              + ("" if v == "OK" else f"  (caught by: {', '.join(sorted(fails))})"))
        if hole and warns:
            print(f"       (WARN emitted, but a WARN is not a gate: {warns[0][:88]})")
        print()

    n = sum(1 for _, h in holes if h)
    print(f"RESULT  {n} of {len(holes)} defective documents pass PREREG_CHECK: OK")
    print(f"\nCERT2: {'HOLES FOUND' if n else 'NO HOLES'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
