#!/usr/bin/env python3
"""PREREG CHECK — the pre-registration checklist as a tool that exits 1.

    .venv/bin/python tools/prereg_check.py docs/research/PREREG-CAL8-2026-08-14.md
    .venv/bin/python tools/prereg_check.py --amendment <locked.md> <amended.md>
    .venv/bin/python tools/prereg_check.py --selftest

GATE ON THE LAST LINE (`PREREG_CHECK: OK|FAIL`), NEVER ON `$?` -- the natural way
anyone runs a long report is `prereg_check.py FILE | tail`, which makes `$?` the
status of `tail`. The exit code is still set, for callers that want it.

WHY THIS EXISTS. Every obligation this tool enforces was written into prose,
inside a doc nobody boots, and then broken by its own author:

  * OBLIGATION 13 (name the file:line your mechanism metric reads) was written
    on 2026-08-11 after LOKI-18 spent 25 unrated games on a bar that read 100%
    in BOTH arms -- the metric sat behind a guard in a file that was
    byte-identical between them. None of s40's preregs carry the line.
  * OBLIGATION 15 (declare map dependence) was written on 2026-08-14 because
    NONE of that day's six preregs declared a segment, and a plank worth +6pp on
    5 of 15 maps pools to +0.67pp -- a pooled screen does not measure a
    conditional plank weakly, it measures it as ZERO.
  * CAL-7's P1 registered a +-8pp bar against a reference of n=155 that CANNOT
    GROW. The floor of its own design is +-9.1pp. **No panel length could ever
    have resolved it**, and that was found after four preregs and five
    amendments.
  * CAL-8's stop boundary was counted over ATTEMPT lines instead of ACCEPTS
    (2026-08-14). One arithmetic identity -- games = 5 x accepts -- separates
    the two, and nothing was checking it.

The measured half-life of a prose rule in this repo is about one session. The
durable surfaces are booted files and tools that exit non-zero. This is the
second kind.

TWO LAYERS, AND THE SECOND IS WHY A PRESENCE CHECK ALONE IS NOT ENOUGH:
  (a) PRESENCE -- one machine-checkable token per obligation. A missing token is
      a NAMED failure, quoting the obligation and the incident.
  (b) ARITHMETIC -- recompute what is cheap: the accepts/games identity, the
      DEFF-corrected half-width at the planned n, the reference-side resolution
      floor at n=infinity, the segment-value ceiling product, and the Obligation
      13 intersection against a REAL git diff.

⛔ WHAT THIS TOOL DOES NOT CHECK, DELIBERATELY: whether the hypothesis is
interesting, whether the bar is the right bar, whether the falsifier would
actually falsify. Those are judgement and belong to research. This checks that
the DECLARATIONS EXIST and that the ARITHMETIC CLOSES. A green run is a floor,
never a blessing.

Token vocabulary: docs/research/SPEC-prereg-check-2026-08-14.md. Research owns
the vocabulary; this file owns the enforcement.
"""
from __future__ import annotations

import argparse
import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# DESIGN EFFECTS. Source: CLAUDE.md, "GAMES ARE NOT INDEPENDENT" -- measured on
# our own tape, 965 rated / 947 unrated 5-game matches.
#
# ⛔ THE KEY IS (SURFACE, SURVIVING CLUSTERS), NOT (SURFACE) ALONE, and that is
# CLAUDE.md's own procedure: name every cluster the data has (MATCH, OPPONENT),
# state for each whether YOUR stratum can hold more than one member, and the
# applicable DEFF is over the clusters that SURVIVE. A lookup table keyed only
# on the surface is exactly what lets someone drop the correction by deciding
# their cut "looks like" one of the cases.
#
# `local` is 0.98 at every cluster key ON PURPOSE: local corefill/arena screens
# are balanced-by-construction and read pair-weighted DEFF = 0.98 (rho=-0.020,
# 124 shards, s39 audit). Applying the platform constants there would widen
# local intervals 24-35% for correlation that is not present.
DEFF = {
    ("rated",   "match+opponent"): 1.529,   # pooled: both clusters live
    ("rated",   "match"):          1.366,   # within-opponent: opponent cluster removed
    ("rated",   "opponent"):       1.07,    # per-map: match cluster dead, opponent measured
    ("rated",   "none"):           1.0,
    ("unrated", "match+opponent"): 1.833,
    ("unrated", "match"):          1.434,
    ("unrated", "opponent"):       1.07,
    ("unrated", "none"):           1.0,
    ("local",   "match+opponent"): 0.98,
    ("local",   "match"):          0.98,
    ("local",   "opponent"):       0.98,
    ("local",   "none"):           0.98,
}

CLUSTER_SYNONYM = {
    "pooled": "match+opponent", "both": "match+opponent",
    "match+opponent": "match+opponent", "match and opponent": "match+opponent",
    "within-opponent": "match", "within opponent": "match", "match": "match",
    "per-map": "opponent", "opponent": "opponent", "map": "opponent",
    "none": "none", "naive": "none", "independent": "none",
}

Z95 = 1.96
GAMES_PER_ACCEPT = 5          # platform fact: an accepted challenge is 5 games

# The vocabulary. Longest-first is NOT needed (each pattern demands the colon
# immediately after the key, so `BASE RATE` cannot match inside `BASE RATE
# SOURCE:`), but the list is the single place the vocabulary is declared.
KNOWN_KEYS = [
    "STATUS", "TARGET BAND", "PINNED", "SURFACE", "CLUSTER UNIT", "ESTIMATOR",
    "PLANNED n", "BOUNDARY", "CUT-SHORT", "BAR", "BASE RATE", "BAR SOURCE",
    "BASE RATE SOURCE", "REFERENCE n", "REFERENCE SURFACE",
    "REFERENCE CLUSTER UNIT", "MECHANISM METRIC READS", "TREATMENT DIFF TOUCHES",
    "TREATMENT DIFF REFS", "INTERSECTION", "GATE RESOLUTION", "PRE-STATE",
    "MAP SEGMENT", "PRIMARY SEGMENT", "EXPECTED DIRECTION",
    "SEGMENT VALUE CEILING", "CELLS", "CELL VERSION CHURN", "FALSIFIER",
    "PROVENANCE", "DOSE",
]


# ---------------------------------------------------------------------------
# PARSING
# ---------------------------------------------------------------------------
def key_pattern(key: str) -> re.Pattern:
    """A DECLARATION of `key`, not a mention of it.

    ⛔ THE ANCHOR IS THE WHOLE DESIGN OF THIS FUNCTION, and it was added after a
    false positive on a REAL prereg. PREREG-SPAWNPOCKET contains the prose
    sentence *"The report's registration line proposes **one primary segment:
    pocket maps {...}**"* -- a bare substring search read that as a second
    PRIMARY SEGMENT declaration and FAILED the document on Obligation 15b, which
    it actually satisfies. **A checker that cannot tell a declaration from a
    sentence about declarations will fail exactly the documents that discuss
    their own obligations most carefully.**

    So a declaration must begin a line (after at most a short run of markdown or
    emoji: `* `, `- `, `> `, `⛔ `) OR begin a bold run (`**KEY:`). That second
    form is not a concession -- it is live house style: PREREG-SPAWNPOCKET writes
    `**PRIMARY MECHANISM: the PAVE half (b).** **EXPECTED DIRECTION: POSITIVE.**`
    with two declarations on one line.

    An optional short parenthetical before the colon is allowed --
    `MAP SEGMENT (primary):` is live usage in PREREG-TINYECO62.
    """
    return re.compile(
        # line start | a bold run | a sentence boundary. The third is required by
        # Obligation 13's own single-line form:
        #   `MECHANISM METRIC READS: <f:l>. TREATMENT DIFF TOUCHES: <p>. INTERSECTION: <y/n>.`
        r"(?:^[^A-Za-z0-9\n]{0,8}|\*\*|[.·;]\s+)\s*"
        + re.escape(key).replace(r"\ ", r"\s+")
        # ⛔ `[ \t]*` and NOT `\s*` after the colon (side-lane cert, 2026-08-14):
        # `\s*` matches the newline, so an EMPTY declaration captured the NEXT
        # LINE as its value — an empty `SURFACE:` above a CLUSTER UNIT line
        # passed the SURFACE malformed-value guard on its neighbour's text.
        + r"\s*(?:\([^)\n]{0,40}\))?\s*:[ \t]*([^\n]*)",
        re.IGNORECASE | re.MULTILINE)


def field(text: str, key: str) -> str | None:
    """Value of the first DECLARATION of `key`, or None."""
    m = key_pattern(key).search(text)
    if not m:
        return None
    return m.group(1).replace("**", "").replace("`", "").strip()


def parse_fields(text: str) -> dict[str, str]:
    out = {}
    for k in KNOWN_KEYS:
        v = field(text, k)
        if v is not None:
            out[k] = v
    return out


def first_number(s: str | None) -> float | None:
    """First quantity in a value, normalised to PERCENTAGE POINTS.

    Handles the three spellings this repo actually types, in the order they
    appear in the string:
        `>=52.0`, `56.8%`   -> 52.0, 56.8
        `3/10`              -> 30.0     (the bar-null incident's own spelling)
        `0.52`              -> 52.0     (a proportion, not half a point)
    ⚠ THE 0..1 RULE IS A HEURISTIC AND IT IS STATED HERE RATHER THAN HIDDEN: a
    bar of "0.5pp" cannot be expressed. No prereg in docs/research/ has ever
    written one, and a bar under 1pp is below every fixture's resolution anyway,
    so the ambiguity is not reachable in practice.
    """
    if not s:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)|(\d+(?:[.,]\d+)?)", s)
    if not m:
        return None
    if m.group(1):
        num, den = float(m.group(1)), float(m.group(2))
        return 100.0 * num / den if den else None
    v = float(m.group(3).replace(",", ""))
    return v * 100.0 if 0.0 < v <= 1.0 else v


def raw_number(s: str | None) -> float | None:
    """First float, VERBATIM -- no proportion/percent normalisation.

    Used by the DOSE check, where the two sides are compared to EACH OTHER and
    normalising one of them would be the only way to make two different numbers
    look equal."""
    if not s:
        return None
    m = re.search(r"-?\d+(?:\.\d+)?", s.replace(",", ""))
    return float(m.group(0)) if m else None


def int_before(s: str | None, word: str) -> int | None:
    """The integer immediately preceding `word` (commas tolerated)."""
    if not s:
        return None
    m = re.search(r"([\d,]+)\s*" + word, s, re.IGNORECASE)
    return int(m.group(1).replace(",", "")) if m else None


# ---------------------------------------------------------------------------
# ARITHMETIC
# ---------------------------------------------------------------------------
def half_width(p: float, terms: list[tuple[float, int]]) -> float:
    """95% half-width in PERCENTAGE POINTS, CLAUDE.md's two forms in one.

        ONE SAMPLE          terms = [(DEFF, n)]
        TWO-FIXTURE         terms = [(DEFF_a, n_a), (DEFF_b, n_b)]
        REFERENCE FLOOR     terms = [(DEFF_ref, n_ref)]   -- the n_panel -> inf limit

    The floor is the same expression with the growable term dropped, which is
    why it is not a separate function: **a reference sample that cannot grow
    contributes a constant to the variance, and no amount of the other fixture
    removes it.** That constant is what killed CAL-7's P1.
    """
    pp = p / 100.0
    var = pp * (1.0 - pp) * sum(d / n for d, n in terms if n)
    return 100.0 * Z95 * math.sqrt(var) if var > 0 else 0.0


def deff_for(surface: str | None, cluster: str | None) -> tuple[float, str]:
    """(DEFF, note). Unknown keys fall back to the most CONSERVATIVE constant on
    that surface, and say so -- an unparseable declaration must never silently
    become naive n."""
    s = (surface or "").strip().lower()
    s = "rated" if "rated" in s and "unrated" not in s else ("unrated" if "unrated" in s
                                                             else ("local" if "local" in s else ""))
    # The declared value is a token followed by prose in every real prereg
    # (`match — one opponent per arm, so ...`). Take the token, not the sentence:
    # requiring a bare value would make the field unwritable in the house style
    # and the correction would be dropped rather than the style changed.
    head = re.split(r"[—–\-,;(]", (cluster or "").strip().lower(), maxsplit=1)[0].strip()
    c = CLUSTER_SYNONYM.get(head, CLUSTER_SYNONYM.get((cluster or "").strip().lower()))
    if c is None:
        # `within-opponent` and `match+opponent` contain the split characters, so
        # they are matched by containment after the token split fails.
        for k in ("match+opponent", "within-opponent", "within opponent", "per-map"):
            if k in (cluster or "").lower():
                c = CLUSTER_SYNONYM[k]
                break
    if not s:
        return 1.833, "SURFACE unreadable -- using the LARGEST platform DEFF (1.833)"
    if c is None:
        worst = max(v for (ss, _cc), v in DEFF.items() if ss == s)
        return worst, f"CLUSTER UNIT unreadable -- using the largest {s} DEFF ({worst})"
    return DEFF[(s, c)], ""


# ---------------------------------------------------------------------------
# PRESENCE RULES — one per obligation, each carrying the incident it closes.
#
# `keys`  : satisfied when ANY of these fields is present.
# `pat`   : satisfied when this regex matches anywhere (for headings, not fields).
# `when`  : optional predicate over the parsed fields; the rule is SKIPPED when
#           it returns False. A conditional rule prints `n/a` with its reason,
#           because a rule that silently disappears is a rule nobody audits.
# ---------------------------------------------------------------------------
def _seg_value(f: dict) -> str:
    return (f.get("MAP SEGMENT") or f.get("PRIMARY SEGMENT") or "").lower()


def _named_segment(f: dict) -> bool:
    v = _seg_value(f)
    return bool(v) and not v.startswith("none")


RULES = [
    dict(id="LOCK", keys=["STATUS"], ob="two-clock lock standard (obligations doc, addendum 16:3x)",
         why="a document that does not assert it predates its own fixture is not a "
             "pre-registration; the 15:46 prereg is the template (git author time vs "
             "platform createdAt, 2m33s apart)",
         extra=lambda v: "before" in v.lower(),
         extra_why="STATUS: must contain the word BEFORE (committed BEFORE what, exactly)"),
    dict(id="TARGET_BAND", keys=["TARGET BAND"], ob="CLAUDE.md target-value gate",
         why="the machinery inspects the EXPERIMENT and never asks whether the QUESTION "
             "is worth answering; s28 passed every check in this repo aimed at teams "
             "550-860 points below us, where a 5-0 pays under 1.2 rating points",
         extra=lambda v: v.strip().upper().startswith("N/A") and len(v) > 12
                         or all(w in v.lower() for w in ("gap", "pays", "reachable")),
         extra_why="must be `TARGET BAND: <opponents>, gaps <a..b>, win pays <x..y>, "
                   "reachable YES/NO` (run tools/target_value.py), or `N/A - <reason>` "
                   "for a leg with zero rated exposure"),
    dict(id="PINNED", keys=["PINNED"], ob="CLAUDE.md opponent-pinning design rule",
         why="PIN TREATMENT LEGS, NEVER PIN CALIBRATION PANELS -- churn is noise in a "
             "leg and signal in a panel, so the choice must be declared, not inferred"),
    dict(id="SURFACE", keys=["SURFACE"], ob="CLAUDE.md DEFF scope procedure",
         why="the design effect is a property of the surface (rated 1.529 / unrated "
             "1.833 / local 0.98); an undeclared surface means no interval in the "
             "document can be checked",
         extra=lambda v: any(w in v.lower() for w in ("rated", "unrated", "local")),
         extra_why="SURFACE: must be one of rated / unrated / local"),
    dict(id="CLUSTER_UNIT", keys=["CLUSTER UNIT"],
         ob="CLAUDE.md cluster-enumeration procedure + side-lane check 4",
         why="'name every cluster this data has, state whether YOUR stratum can hold "
             "more than one member' -- the applicable DEFF is over the clusters that "
             "SURVIVE, and a per-map bar carrying 1.53 is over-corrected exactly as "
             "wrongly as a pooled bar carrying 1.00"),
    dict(id="ESTIMATOR", keys=["ESTIMATOR"], ob="side-lane check 4",
         why="s28 ring-hold: FOUR estimators sat within 0.010 of one bar and flipped "
             "MEET/MISS among themselves -- an unnamed estimator is a free choice made "
             "after the data"),
    dict(id="PLANNED_N", keys=["PLANNED n"], ob="side-lane check 5",
         why="an unfixed n permits optional stopping (s28 LOKI-16b); the planned n is "
             "also the only input the resolvability arithmetic below can use"),
    dict(id="CUT_SHORT", keys=["CUT-SHORT"], ob="side-lane check 5",
         why="CAL-6 stopped at 75 and CAL-7 at 110, both on holder changes, and neither "
             "had pre-committed what a short leg may claim -- CAL-8's n>=75 floor is "
             "the live example of this clause doing work"),
    dict(id="BOUNDARY", keys=["BOUNDARY"], ob="CAL-8 stop-boundary incident, 2026-08-14",
         why="the boundary was counted over ATTEMPT lines instead of ACCEPTS; declaring "
             "it in BOTH units is what makes the miscount visible (see BOUNDARY_UNITS "
             "below, which recomputes it)"),
    dict(id="BAR", keys=["BAR"], ob="the iteration mill (docs/builder-method.md S0-S8)",
         why="a leg with no bar cannot fail, and a leg that cannot fail is not an "
             "experiment"),
    dict(id="BASE_RATE", keys=["BASE RATE"], ob="side-lane check 1 (bar-null assertion)",
         why="a 3/10 bar was once tested against a 29.6% base rate -- the bar was the "
             "status quo wearing a treatment's clothes. The comparator must be written "
             "down before the arithmetic can assert bar != base rate"),
    dict(id="SOURCES", keys=["BAR SOURCE"], also=["BASE RATE SOURCE"],
         ob="side-lane check 1 + CLAUDE.md 'numbers carry subjects'",
         why="copy the denominator, the population and the clock along with the number; "
             "an unsourced base rate is the half of the comparison nobody audits"),
    dict(id="OB13", keys=["MECHANISM METRIC READS"], also=["TREATMENT DIFF TOUCHES", "INTERSECTION"],
         ob="OBLIGATION 13",
         why="LOKI-18 spent 25 unrated games on a bar reading 100% in BOTH arms: the "
             "metric sat downstream of a guard in raid.py, which was byte-identical "
             "between the arms, while the diff was one hunk in main.py:560. "
             "`MECHANISM METRIC READS: <file:line>. TREATMENT DIFF TOUCHES: <paths>. "
             "INTERSECTION: <yes/no>.`"),
    dict(id="OB12_GATE", keys=["GATE RESOLUTION"], ob="OBLIGATION 12",
         why="A GATE IS A BAR AND MUST BE SIZED LIKE ONE. LOKI-19's Amendment 1b had "
             "10-point-wide branches answered by 19 events, with a lower bound astride "
             "a branch boundary -- it could not resolve the question it was built to "
             "decide, and nothing required it to say so in advance"),
    dict(id="OB12_DEFAULT", pat=r"UNRESOLVED", ob="OBLIGATION 12, the pre-committed default",
         why="AN UNRESOLVED GATE DEFAULTS TO THE RESTRICTION, NEVER THE PERMISSION -- "
             "granting the permissive branch on an estimate that cannot distinguish "
             "delivery from non-delivery is precisely a flatter"),
    dict(id="OB7_PRESTATE", keys=["PRE-STATE"], ob="OBLIGATION 7",
         why="the 15:46 conversion prereg predicted change on three cells ALREADY in "
             "the target state at lock and excluded the two that moved -- 2/2 on "
             "excluded maps, 0/3 on named ones. A prereg predicting change on cells "
             "already changed cannot fail honestly"),
    dict(id="OB15A_SEGMENT", keys=["MAP SEGMENT", "PRIMARY SEGMENT"], ob="OBLIGATION 15a",
         why="none of s40's six preregs declared a segment; a plank worth +6pp on 5 of "
             "15 maps pools to +0.67pp, so a pooled screen measures a conditional plank "
             "as ZERO and the road closes"),
    dict(id="OB15A_DIRECTION", keys=["EXPECTED DIRECTION"], ob="OBLIGATION 15a",
         when=_named_segment,
         why="THE EXPECTED DIRECTION IS NOT OPTIONAL -- a segment declared without a "
             "predicted sign is unfalsifiable: whichever way it lands it 'confirms' the "
             "mechanism",
         na="MAP SEGMENT is `none expected`, so there is no sign to predict"),
    dict(id="OB15B_ONE_PRIMARY", pat=None, ob="OBLIGATION 15b",
         why="EXACTLY ONE PRIMARY SEGMENT. Declaring K segments gives K chances to "
             "rescue a failed arm -- textbook subgroup fishing, and how a 51-bar is "
             "defeated by anyone patient enough to enumerate",
         custom="one_primary"),
    dict(id="SEGMENT_CEILING", keys=["SEGMENT VALUE CEILING"], ob="D1 delta (segment-value ceiling)",
         when=_named_segment,
         why="a segment's pooled value is bounded by `pairing share x on-segment "
             "effect`; SPAWNPOCKET's primary is ~14% of pairings, so the ceiling has to "
             "be written down before a live confirmation is expected",
         na="no named segment, so there is no pairing share to bound"),
    dict(id="OB14_CHURN", keys=["CELL VERSION CHURN"], ob="OBLIGATION 14",
         when=lambda f: "CELLS" in f,
         # A CONDITIONAL RULE CANNOT BE CORRUPTED BY DELETION -- deleting its token
         # from a doc that never triggered it leaves the rule n/a, which is a PASS.
         # Its forced-fail fixture must first TRIGGER the condition.
         corrupt=lambda t: t.replace("## FALSIFIER", "**CELLS: D1 0033 · D2 LingLing40**"
                                                     "\n\n## FALSIFIER"),
         why="D13 selected the cell it could not measure -- SmartFridge was the most "
             "mid-range opponent on the board and ran TEN versions in 24h, producing "
             "five independent defects in one day. A high-churn cell is REPORTABLE BUT "
             "NOT POOLABLE, and the count is free off league_matches.tsv",
         na="no CELLS: line, so this is not a panel"),
    dict(id="FALSIFIER", pat=r"(?im)^[^A-Za-z0-9]*#*\s*\**\s*FALSIFIER|FALSIFIER\s*:",
         ob="the iteration mill",
         why="a pre-registration without a falsifier is a plan, not an experiment"),
    dict(id="PROVENANCE", keys=["PROVENANCE"],
         ob="drafting rule, 2026-08-14 (both lane charters): every prereg is drafted "
            "by a fresh opus subagent with NO inherited session context beyond named "
            "inputs",
         why="the no-inherited-context claim is unauditable unless the inputs are on the "
             "page. A drafting agent that quietly read the result tape produces a "
             "document indistinguishable from a blind one -- the PROVENANCE line is the "
             "only thing that separates them after the fact",
         extra=lambda v: len(v.strip()) >= 5,
         extra_why="PROVENANCE: must list the input files verbatim (paths), not a "
                   "description of them"),
    dict(id="DOSE", keys=["DOSE"],
         ob="dose-probe gate (Magnus, 2026-08-14): a probe is a DESIGN PHASE that gates "
            "the screen",
         why="an arm reaches a screen only after a probe shows its mechanism FIRES, and "
             "the probe carries BOTH verdicts -- treatment dose against a flag-off or "
             "mutation control returning to baseline. SPAWNPOCKET's half (a) was killed "
             "by exactly this clause before a screen row existed: the spawn chooser was "
             "never the entry mechanism, and 37/37 was false. "
             "⚠ Required only on the dose-fires path; a premise-refuted probe writes no "
             "prereg at all"),
]


def check_presence(text: str, f: dict) -> tuple[list, list]:
    """-> (rows, fails). rows are (verdict, id, token, detail) for the report."""
    rows, fails = [], []
    for r in RULES:
        rid = r["id"]
        if r.get("when") and not r["when"](f):
            rows.append(("n/a ", rid, r.get("keys", [""])[0] if r.get("keys") else "-",
                         r.get("na", "condition not met")))
            continue
        if r.get("custom") == "one_primary":
            # OBLIGATION 15b, and it is checkable because a primary segment is a
            # DECLARATION: count the declarations, not the maps.
            n = len(key_pattern("PRIMARY SEGMENT").findall(text))
            n += len(re.findall(r"MAP SEGMENT\s*\(\s*primary\s*\)\s*:", text, re.I))
            if n > 1:
                rows.append(("FAIL", rid, "PRIMARY SEGMENT:", f"{n} primary-segment declarations"))
                fails.append((rid, r["ob"], r["why"], f"{n} primary segments declared; 15b allows ONE"))
            else:
                rows.append(("ok  ", rid, "PRIMARY SEGMENT:", f"{n} declared (<=1)"))
            continue
        if r.get("pat"):
            ok = bool(re.search(r["pat"], text, re.IGNORECASE))
            rows.append((("ok  " if ok else "FAIL"), rid, r["pat"][:28], "" if ok else "absent"))
            if not ok:
                fails.append((rid, r["ob"], r["why"], "token absent"))
            continue
        keys = r["keys"]
        got = next((k for k in keys if k in f), None)
        missing_also = [k for k in r.get("also", []) if k not in f]
        token = " | ".join(keys) + ("" if not r.get("also") else " + " + " + ".join(r["also"]))
        if got is None:
            rows.append(("FAIL", rid, token, "absent"))
            fails.append((rid, r["ob"], r["why"], f"none of {keys} present"))
            continue
        if missing_also:
            rows.append(("FAIL", rid, token, f"missing {missing_also}"))
            fails.append((rid, r["ob"], r["why"], f"companion token(s) missing: {missing_also}"))
            continue
        if r.get("extra") and not r["extra"](f[got]):
            rows.append(("FAIL", rid, token, "malformed value"))
            fails.append((rid, r["ob"], r.get("extra_why", r["why"]), f"value: {f[got][:70]!r}"))
            continue
        rows.append(("ok  ", rid, token, f[got][:58]))
    return rows, fails


# ---------------------------------------------------------------------------
# ARITHMETIC CHECKS
# ---------------------------------------------------------------------------
def check_arithmetic(f: dict, diff_paths=None) -> tuple[list, list, list]:
    """-> (lines, fails, warns). Recompute where cheap; WARN where a live query
    would be needed. A check that cannot compute says so LOUDLY -- 'not computed'
    and 'computed clean' must never render identically."""
    lines, fails, warns = [], [], []

    # --- 1. BOUNDARY: accepts AND games, and games = 5 x accepts. -----------
    # THE DIRECT FIX for CAL-8's 2026-08-14 stop, which counted a boundary over
    # ATTEMPT lines instead of ACCEPTS. Declaring one unit hides the error;
    # declaring both makes it an identity a machine can check.
    bd = f.get("BOUNDARY")
    acc, gms = int_before(bd, "accepts?"), int_before(bd, "games?")
    if bd is None:
        lines.append("BOUNDARY_UNITS   not computed -- no BOUNDARY: line")
    elif acc is None or gms is None:
        lines.append(f"BOUNDARY_UNITS   FAIL  need BOTH units, got accepts={acc} games={gms}")
        fails.append(("BOUNDARY_UNITS", "CAL-8 incident",
                      "the boundary must be declared in BOTH accepts and games; one unit "
                      "alone cannot reveal a count taken over attempt lines",
                      f"BOUNDARY: {bd!r}"))
    elif gms != GAMES_PER_ACCEPT * acc:
        lines.append(f"BOUNDARY_UNITS   FAIL  {acc} accepts x 5 = {GAMES_PER_ACCEPT*acc}, "
                     f"declared {gms} games")
        fails.append(("BOUNDARY_UNITS", "CAL-8 incident",
                      "games = 5 x accepts is a platform identity; a mismatch means the "
                      "boundary was counted over the wrong lines",
                      f"{acc} accepts vs {gms} games"))
    else:
        lines.append(f"BOUNDARY_UNITS   ok    {acc} accepts = {gms} games (5x)")

    n_plan = int_before(f.get("PLANNED n"), "games?") or first_number(f.get("PLANNED n"))
    n_plan = int(n_plan) if n_plan else None
    if n_plan and gms and n_plan != gms:
        lines.append(f"BOUNDARY_VS_N    FAIL  PLANNED n={n_plan} games but BOUNDARY says {gms}")
        fails.append(("BOUNDARY_VS_N", "CAL-8 incident",
                      "the planned n and the stop boundary are the same number in the "
                      "same unit, or one of them is not the one the bar was sized on",
                      f"{n_plan} vs {gms}"))
    elif n_plan and gms:
        lines.append(f"BOUNDARY_VS_N    ok    PLANNED n = BOUNDARY games = {gms}")

    if f.get("PLANNED n") and "game" not in f["PLANNED n"].lower():
        warns.append("PLANNED n does not name its unit. Every bar this project quotes is "
                     "in GAMES (5 per accepted match); an n in MATCHES is 5x smaller than "
                     "it reads.")

    # --- 2. RESOLVABILITY: is the declared margin larger than the interval? --
    # CAL-7's P1 failure, generalised. `bar` and `base rate` are the two ends of
    # the comparison; the distance between them is what the fixture must be able
    # to see. If the half-width at the planned n exceeds that distance, the leg
    # is unresolvable BEFORE it fires.
    bar, base = first_number(f.get("BAR")), first_number(f.get("BASE RATE"))
    deff, note = deff_for(f.get("SURFACE"), f.get("CLUSTER UNIT"))
    if note:
        warns.append(note)
    n_ref = int_before(f.get("REFERENCE n"), r"\b") or first_number(f.get("REFERENCE n"))
    ref_txt = (f.get("REFERENCE n") or "").strip().lower()
    if ref_txt.startswith("none") or ref_txt.startswith("n/a"):
        n_ref = None
    n_ref = int(n_ref) if n_ref else None
    deff_ref, _ = deff_for(f.get("REFERENCE SURFACE") or f.get("SURFACE"),
                           f.get("REFERENCE CLUSTER UNIT") or f.get("CLUSTER UNIT"))

    if bar is None or base is None or not n_plan:
        lines.append("BAR_RESOLVABLE   not computed -- need BAR, BASE RATE and PLANNED n")
    else:
        margin = abs(bar - base)
        pbar = (bar + base) / 2.0
        terms = [(deff, n_plan)] + ([(deff_ref, n_ref)] if n_ref else [])
        hw = half_width(pbar, terms)
        shape = ("two-fixture" if n_ref else "one-sample")
        lines.append(f"BAR_RESOLVABLE   {'ok  ' if margin >= hw else 'FAIL'}  "
                     f"margin |{bar:.1f}-{base:.1f}| = {margin:.1f}pp vs half-width "
                     f"+-{hw:.1f}pp  ({shape}, DEFF {deff}"
                     + (f" / ref {deff_ref} @ n={n_ref}" if n_ref else "") + f", n={n_plan})")
        if margin < hw:
            fails.append(("BAR_RESOLVABLE", "CAL-7 P1 / CLAUDE.md DEFF block",
                          "the bar sits INSIDE the interval the fixture can produce at the "
                          "planned n -- the leg cannot distinguish its own branches, and "
                          "no verdict it returns is a measurement",
                          f"margin {margin:.1f}pp < half-width {hw:.1f}pp"))
        # --- 3. BAR-NULL: the bar must not BE the comparator. ---------------
        if margin < 1e-9:
            fails.append(("BAR_NULL", "side-lane check 1",
                          "the bar equals the comparator base rate: the treatment is "
                          "registered to beat the status quo by nothing",
                          f"BAR {bar} == BASE RATE {base}"))
            lines.append("BAR_NULL         FAIL  bar == base rate")
        else:
            lines.append(f"BAR_NULL         ok    bar {bar:.1f} != base rate {base:.1f}")

        # --- 4. REFERENCE FLOOR at panel n = infinity. ----------------------
        # side-lane check 3. A reference that CANNOT GROW contributes a constant
        # to the variance; the panel term goes to zero and that constant does
        # not. CAL-7's +-8pp bar sat under a +-9.1pp floor from a retired
        # reference of n=155, so NO panel length could ever have resolved it --
        # a fact available in closed form on the day the prereg was written.
        if n_ref:
            floor = half_width(pbar, [(deff_ref, n_ref)])
            lines.append(f"REFERENCE_FLOOR  {'ok  ' if margin >= floor else 'FAIL'}  "
                         f"floor at panel n=inf is +-{floor:.1f}pp "
                         f"(reference n={n_ref}, DEFF {deff_ref}); margin {margin:.1f}pp")
            if margin < floor:
                fails.append(("REFERENCE_FLOOR", "side-lane check 3 (CAL-7 P1)",
                              "the bar is below the resolution FLOOR set by a reference "
                              "sample that cannot grow -- unresolvable BY CONSTRUCTION, "
                              "at any n. Lengthening the leg buys nothing",
                              f"margin {margin:.1f}pp < floor {floor:.1f}pp"))
        else:
            lines.append("REFERENCE_FLOOR  n/a   no fixed reference declared "
                         "(REFERENCE n: none)")

    # --- 5. SEGMENT VALUE CEILING: recompute the product. -------------------
    sv = f.get("SEGMENT VALUE CEILING")
    if sv is None:
        lines.append("SEGMENT_CEILING  not computed -- no SEGMENT VALUE CEILING: line")
    else:
        nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)", sv.replace(",", ""))]
        if len(nums) < 3:
            lines.append(f"SEGMENT_CEILING  FAIL  need `<share>% x <effect>pp = <pooled>pp`")
            fails.append(("SEGMENT_CEILING", "D1 delta",
                          "the ceiling must be written as an arithmetic statement so it "
                          "can be recomputed, not as a claim",
                          f"SEGMENT VALUE CEILING: {sv!r}"))
        else:
            share, eff, claimed = nums[0], nums[1], nums[2]
            calc = share / 100.0 * eff
            ok = abs(calc - claimed) <= 0.05
            lines.append(f"SEGMENT_CEILING  {'ok  ' if ok else 'FAIL'}  "
                         f"{share}% x {eff}pp = {calc:.2f}pp, declared {claimed}pp")
            if not ok:
                fails.append(("SEGMENT_CEILING", "D1 delta",
                              "the declared pooled ceiling does not equal pairing share x "
                              "on-segment effect",
                              f"{share}% x {eff} = {calc:.2f}, declared {claimed}"))
            elif calc < 1.0:
                warns.append(f"SEGMENT CEILING {calc:.2f}pp pooled is below anything this "
                             f"project's pooled bars resolve -- say in the prereg that the "
                             f"confirmation is on-segment, never pooled.")

    # --- 6. DOSE: the probe must carry BOTH verdicts. ----------------------
    # A dose line quoting ONE number has not shown the mechanism fires -- it has
    # shown that a counter incremented. The flag-off / mutation arm returning to
    # control level is the half that makes the first half mean anything, and it
    # is the same rule CLAUDE.md applies to every instrument: a guard that has
    # never produced the other verdict has not been seen to check.
    # WHETHER THE DOSE IS SUFFICIENT IS JUDGEMENT and is deliberately not checked.
    dose = f.get("DOSE")
    if dose is None:
        lines.append("DOSE_BOTH_VERDICTS not computed -- no DOSE: line")
    else:
        halves = re.split(r"\bvs\.?\b|\bversus\b|→|->", dose, flags=re.IGNORECASE)
        lo = raw_number(halves[0]) if halves else None
        hi = raw_number(halves[1]) if len(halves) > 1 else None
        if len(halves) < 2 or lo is None or hi is None:
            lines.append(f"DOSE_BOTH_VERDICTS FAIL  one value only: {dose[:60]!r}")
            fails.append(("DOSE_BOTH_VERDICTS", "dose-probe gate",
                          "the DOSE line names a treatment value with no control value. "
                          "`DOSE: <metric> <treatment> vs flag-off <control> (n=...)` -- "
                          "one number is a counter reading, not a demonstration that the "
                          "mechanism fires", f"DOSE: {dose[:70]!r}"))
        elif abs(lo - hi) < 1e-9:
            lines.append(f"DOSE_BOTH_VERDICTS FAIL  treatment {lo} == control {hi}")
            fails.append(("DOSE_BOTH_VERDICTS", "dose-probe gate",
                          "the treatment and flag-off values are IDENTICAL: the probe did "
                          "not separate the arms, so the mechanism has not been shown to "
                          "fire and the screen is not gated open",
                          f"{lo} vs {hi}"))
        else:
            lines.append(f"DOSE_BOTH_VERDICTS ok    treatment {lo} vs control {hi}")
            if not re.search(r"\bn\s*=", dose, re.IGNORECASE):
                warns.append("DOSE line carries no `n=` -- a dose ratio without its "
                             "denominator is a number without a subject.")

    # --- 7. OBLIGATION 13, COMPUTED. ---------------------------------------
    inter = (f.get("INTERSECTION") or "").strip().lower()
    reads = f.get("MECHANISM METRIC READS") or ""
    m = re.match(r"([\w./\-]+\.py)(?::(\d+))?", reads.strip())
    metric_file = m.group(1) if m else None
    if inter.startswith("no"):
        # Declared INERT. The obligation is explicit: the leg may not be fired.
        lines.append("OB13_INTERSECTION FAIL  declared INTERSECTION: no")
        fails.append(("OB13_INTERSECTION", "OBLIGATION 13",
                      "the prereg declares the mechanism metric does NOT read a file the "
                      "treatment diff touches. The bar is INERT and the leg may not be "
                      "fired on it", f"INTERSECTION: {inter!r}"))
    elif metric_file is None:
        lines.append("OB13_INTERSECTION not computed -- MECHANISM METRIC READS has no "
                     "<file>.py:<line>")
        if reads:
            warns.append("MECHANISM METRIC READS does not name a <file>.py:<line>. "
                         "An unnameable read path is not a measured one -- that is the "
                         "finding, per Obligation 13.")
    else:
        paths = diff_paths if diff_paths is not None else git_diff_paths(f.get("TREATMENT DIFF REFS"))
        if not paths:
            lines.append(f"OB13_INTERSECTION WARN  metric file {metric_file}; no computable "
                         f"diff (tree clean or refs unavailable)")
            warns.append("Obligation 13 intersection DECLARED but NOT COMPUTED: no diff "
                         "was available. A prereg committed before the arm tree exists is "
                         "the legitimate case; re-run this check once the tree lands.")
        else:
            hit = [p for p in paths if p.endswith(metric_file) or metric_file.endswith(p)]
            lines.append(f"OB13_INTERSECTION {'ok  ' if hit else 'FAIL'}  metric file "
                         f"{metric_file} {'IS' if hit else 'is NOT'} in the {len(paths)}-path diff")
            if not hit:
                fails.append(("OB13_INTERSECTION", "OBLIGATION 13, computed",
                              "the file the mechanism metric reads is NOT in the actual "
                              "treatment diff -- this is LOKI-18 exactly: the metric reads "
                              "100% in both arms and 25 games measure nothing",
                              f"{metric_file} not in {paths[:6]}"))
            declared = [p.strip() for p in re.split(r"[,\s]+", f.get("TREATMENT DIFF TOUCHES") or "")
                        if p.strip().endswith(".py")]
            stray = [d for d in declared if not any(p.endswith(d) or d.endswith(p) for p in paths)]
            if stray:
                warns.append(f"TREATMENT DIFF TOUCHES names path(s) absent from the real "
                             f"diff: {stray}. Declared and actual disagree.")
    return lines, fails, warns


def git_diff_paths(refs: str | None) -> list[str] | None:
    """Changed .py paths, from the named refs or the working tree.

    ⛔ AN EMPTY DIFF IS 'NOT COMPUTABLE', NOT 'EMPTY INTERSECTION'. Two of the
    three s40 preregs say in their own STATUS line that they are committed
    BEFORE the arm tree exists -- which is the CORRECT order -- and a clean tree
    is what that looks like from here. FAILing them would punish the one habit
    this whole checklist is built to enforce.
    """
    cmd = ["git", "diff", "--name-only"]
    if refs and refs.strip().lower() not in ("none", "n/a", ""):
        cmd += refs.strip().split()
    else:
        cmd += ["HEAD"]
    try:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=60)
    except Exception:
        return None
    paths = [p for p in r.stdout.split() if p.endswith(".py")]
    return paths or None


# ---------------------------------------------------------------------------
# AMENDMENT MODE — side-lane check 6.
# ---------------------------------------------------------------------------
BAR_LINE_PAT = re.compile(
    r"(BAR|BASE RATE|PLANNED n|BOUNDARY|TARGET BAND|GATE RESOLUTION|EXPECTED DIRECTION"
    r"|MAP SEGMENT|PRIMARY SEGMENT|SEGMENT VALUE CEILING|CUT-SHORT|ESTIMATOR"
    r"|CLUSTER UNIT|SURFACE|REFERENCE n)\s*(?:\([^)\n]{0,40}\))?\s*:", re.IGNORECASE)


def _norm(line: str) -> str:
    return re.sub(r"\s+", " ", line.replace("**", "").replace("`", "")).strip()


def check_amendment(locked: Path, amended: Path) -> int:
    """An amendment may only ADD a constraint. Loosening, retargeting or
    reinterpreting an existing bar is a NEW PREREG.

    ⛔ TIMESTAMPS PROVE **WHEN**, NEVER **WHAT** (s28). Two honest clocks certify
    an amendment that quietly widened a bar exactly as cleanly as one that added
    a constraint. The DIFF CLASS is the enforcement, and it is the only one:
    every bar/branch line present in the locked file must still be present,
    byte-for-byte after whitespace normalisation, in the amended one.
    """
    a, b = locked.read_text(), amended.read_text()
    old = [_norm(l) for l in a.splitlines() if BAR_LINE_PAT.search(l)]
    new = {_norm(l) for l in b.splitlines() if BAR_LINE_PAT.search(l)}
    print(f"AMENDMENT CHECK\n  locked : {locked}\n  amended: {amended}")
    print(f"  bar/branch lines in locked: {len(old)}   in amended: {len(new)}")
    gone = [l for l in old if l not in new]
    added = sorted(new - set(old))
    for l in added:
        print(f"  ADD   {l[:110]}")
    for l in gone:
        print(f"  *** EDITED-OR-REMOVED  {l[:110]}")
    if gone:
        print(f"\nFAIL  {len(gone)} locked bar/branch line(s) were EDITED or REMOVED. "
              f"An amendment is ADD-ONLY; changing a registered bar is a NEW PREREG "
              f"with its own lock, not an addendum to this one.")
        print("\nPREREG_CHECK: FAIL")
        return 1
    # ⛔ COVERAGE GUARD (side-lane finding 3, 2026-08-14): this mode diffs only
    # TOKENISED bar lines. On a prose prereg (all 81 pre-migration documents) it
    # matched 3 of the 12 lines naming the decision boundary of SCREEN-v140vs145
    # and printed ADD-ONLY: OK while an amendment changed the decision rule.
    # A guard that cannot see its subject says so instead of passing.
    comparator = re.compile(r"[<>≥≤]=?\s*\d|(?:->|→)\s*(?:reactivate|v?\d)", re.IGNORECASE)
    untok = [l for l in b.splitlines()
             if comparator.search(l) and not BAR_LINE_PAT.search(l)]
    if not old or len(untok) > len(old):
        print(f"  tokenised bar lines: {len(old)}   decision-shaped untokenised lines: {len(untok)}")
        print(f"\nAMENDMENT CHECK: NOT APPLICABLE — the tokenised diff class sees too "
              f"little of this document to certify ADD-ONLY ({len(old)} tokenised vs "
              f"{len(untok)} decision-shaped prose lines). Migrate the registration "
              f"block or certify the amendment by hand; do not read this as a pass.")
        print("\nPREREG_CHECK: NOT_APPLICABLE")
        return 2
    print(f"\nADD-ONLY: OK ({len(added)} line(s) added, 0 edited)")
    print("\nPREREG_CHECK: OK")
    return 0


# ---------------------------------------------------------------------------
# REPORT
# ---------------------------------------------------------------------------
def run_checks(text: str, label: str, diff_paths=None, quiet=False) -> tuple[list, list, list]:
    f = parse_fields(text)
    rows, fails = check_presence(text, f)
    alines, afails, warns = check_arithmetic(f, diff_paths=diff_paths)
    fails = fails + afails
    if not quiet:
        print(f"PREREG CHECK  {label}")
        print(f"  {len(text.splitlines())} lines, {len(f)} vocabulary field(s) parsed\n")
        print("PRESENCE")
        for verdict, rid, token, detail in rows:
            print(f"  [{verdict}] {rid:<18} {token[:44]:<46} {detail[:52]}")
        print("\nARITHMETIC")
        for l in alines:
            print(f"  {l}")
        if warns:
            print()
            for w in warns:
                print(f"WARN  {w}")
        if fails:
            print()
            for rid, ob, why, detail in fails:
                print(f"FAIL  {rid}   [{ob}]")
                print(f"        {detail}")
                print(f"        WHY: {why}")
    return rows, fails, warns


def check_file(path: Path) -> int:
    _rows, fails, _warns = run_checks(path.read_text(), str(path))
    print()
    if fails:
        print(f"{len(fails)} obligation(s) unmet. A prereg is not locked until this "
              f"line reads OK.")
    else:
        print("Every machine-checkable obligation is declared and every recomputed "
              "quantity closes.\n⚠ THIS IS A FLOOR, NOT A BLESSING: the hypothesis, the "
              "choice of bar and the content of the falsifier are judgement and are NOT "
              "checked here.")
    print(f"\nPREREG_CHECK: {'FAIL' if fails else 'OK'}")
    return 1 if fails else 0


# ---------------------------------------------------------------------------
# SELFTEST
#
# ⛔ EVERY GUARD IS DRIVEN TO **BOTH** VERDICTS. A check that has never produced
# the other answer has not been seen to check (CLAUDE.md, instruments rule). The
# fixtures below are readable prereg text on purpose -- the side lane's
# independent forced-fail certification mutates REAL prereg text, and a fixture
# built by string generation cannot be corrupted the same way.
# ---------------------------------------------------------------------------
COMPLETE = """\
# PREREG — SYNTHETIC COMPLETE FIXTURE (selftest only, not a real leg)

**STATUS: committed BEFORE any challenge is issued** (two-clock standard).
**PROVENANCE: docs/research/HOME-LOCK-MECHANISM-2026-08-14.md · corpus/ladder_games.tsv · bots/_v223sealrepair/eco.py**

## REGISTRATION BLOCK
**TARGET BAND: 0033, gaps +81..+81, win pays 19.7..19.7, reachable YES**
**PINNED: YES — treatment leg, `fcode match unrated <team> --match <past_id>`**
**SURFACE: unrated**
**CLUSTER UNIT: match — one opponent per arm, so the opponent cluster is removed**
**ESTIMATOR: pooled game share, games-level, unweighted**
**DOSE: seal-refusals 7.4/game vs flag-off 0.0/game (n=12+12 probe shards)**
**PLANNED n: 150 games**
**BOUNDARY: 30 accepts = 150 games**
**CUT-SHORT: below 75 games this leg publishes descriptive tallies only and takes NO comparative look**
**BAR: 60.0**
**BASE RATE: 50.0**
**BAR SOURCE: pre-registered treatment bar, this document**
**BASE RATE SOURCE: corpus/ladder_games.tsv, ourver >= 125, n = 415 games, cut 2026-08-14**
**REFERENCE n: none**
**MECHANISM METRIC READS: eco.py:934. TREATMENT DIFF TOUCHES: eco.py, main.py. INTERSECTION: yes.**
**GATE RESOLUTION: the dose gate discriminates its branches at n >= 60 events; UNRESOLVED ⇒ the RESTRICTION (no ship)**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock — all six cells verified below the bar at lock time**
**MAP SEGMENT: {midgard, fjordgate} — pave-sealing is a long-approach terrain effect**
**EXPECTED DIRECTION: POSITIVE on-segment, ~ZERO off-segment**
**SEGMENT VALUE CEILING: 25.0% pairing share x 6.0pp on-segment = 1.50pp pooled**

## FALSIFIER
If the dose moves and the on-segment share does not clear 60.0, the row closes.
"""

# The reference-floor fixture: CAL-7's P1 reconstructed. A +-8pp bar against a
# reference of n=155 that cannot grow.
CAL7_FLOOR = COMPLETE.replace("**BAR: 60.0**", "**BAR: 64.8**") \
                     .replace("**BASE RATE: 50.0**", "**BASE RATE: 56.8**") \
                     .replace("**REFERENCE n: none**",
                              "**REFERENCE n: 155 (v125 six-cell rated reference, RETIRED — cannot grow)**\n"
                              "**REFERENCE SURFACE: rated**\n**REFERENCE CLUSTER UNIT: match**") \
                     .replace("**PLANNED n: 150 games**", "**PLANNED n: 3000 games**") \
                     .replace("**BOUNDARY: 30 accepts = 150 games**",
                              "**BOUNDARY: 600 accepts = 3000 games**")


def _strip_rule(text: str, rule: dict) -> str:
    """Delete the line(s) carrying a rule's token -- the minimal corruption."""
    pats = []
    for k in list(rule.get("keys", [])) + list(rule.get("also", [])):
        pats.append(key_pattern(k))
    if rule.get("pat"):
        pats.append(re.compile(rule["pat"], re.IGNORECASE))
    out = [l for l in text.splitlines() if not any(p.search(l) for p in pats)]
    return "\n".join(out)


def selftest() -> int:
    bad = 0
    print("PREREG CHECK SELFTEST — every guard driven to BOTH verdicts\n")

    # --- the complete fixture must PASS -------------------------------------
    _r, fails, _w = run_checks(COMPLETE, "<COMPLETE fixture>", diff_paths=["eco.py", "main.py"],
                               quiet=True)
    ok = not fails
    print(f"  [{'ok' if ok else 'FAIL'}] COMPLETE fixture PASSES "
          f"({len(fails)} failure(s){': ' + ', '.join(x[0] for x in fails) if fails else ''})")
    bad += 0 if ok else 1

    # --- one corruption per PRESENCE rule, each naming ITS OWN rule ----------
    print("\n  PRESENCE — one minimal corruption per rule; each must FAIL naming that rule:")
    for rule in RULES:
        rid = rule["id"]
        if rule.get("corrupt"):
            txt = rule["corrupt"](COMPLETE)
        elif rule.get("custom") == "one_primary":
            # the other verdict for 15b is a SECOND primary declaration, not a deletion
            txt = COMPLETE.replace("**MAP SEGMENT: {midgard, fjordgate}",
                                   "**PRIMARY SEGMENT: {midgard}**\n**PRIMARY SEGMENT: {valkyrie}**\n"
                                   "**MAP SEGMENT: {midgard, fjordgate}")
        else:
            txt = _strip_rule(COMPLETE, rule)
        _r, fails, _w = run_checks(txt, f"<no {rid}>", diff_paths=["eco.py", "main.py"], quiet=True)
        named = [x for x in fails if x[0] == rid]
        ok = bool(named)
        print(f"  [{'ok' if ok else 'FAIL'}] {rid:<18} -> "
              f"{'FAIL ' + rid if ok else 'NOT NAMED (got ' + ','.join(x[0] for x in fails) + ')'}")
        bad += 0 if ok else 1

    # --- conditional rules must go n/a when their condition is absent -------
    # A rule that is ALWAYS active has not been seen to be conditional, and a
    # rule that is NEVER active is decoration. Both branches, explicitly.
    print("\n  CONDITIONALS — the skip branch must also be exercised:")
    no_seg = COMPLETE.replace("**MAP SEGMENT: {midgard, fjordgate} — pave-sealing is a "
                              "long-approach terrain effect**",
                              "**MAP SEGMENT: none expected — the trigger is opponent "
                              "heal-staffing, not terrain**")
    no_seg = _strip_rule(no_seg, dict(keys=["EXPECTED DIRECTION", "SEGMENT VALUE CEILING"]))
    _r, fails, _w = run_checks(no_seg, "<none expected>", diff_paths=["eco.py"], quiet=True)
    hit = [x[0] for x in fails if x[0] in ("OB15A_DIRECTION", "SEGMENT_CEILING")]
    ok = not hit
    print(f"  [{'ok' if ok else 'FAIL'}] `MAP SEGMENT: none expected` skips DIRECTION and "
          f"CEILING  {'' if ok else hit}")
    bad += 0 if ok else 1
    with_cells = COMPLETE.replace("## FALSIFIER", "**CELLS: D1 0033 · D2 LingLing40**\n\n## FALSIFIER")
    _r, fails, _w = run_checks(with_cells, "<panel with CELLS>", diff_paths=["eco.py"], quiet=True)
    ok = any(x[0] == "OB14_CHURN" for x in fails)
    print(f"  [{'ok' if ok else 'FAIL'}] a `CELLS:` line ACTIVATES the Obligation-14 churn rule")
    bad += 0 if ok else 1

    # --- ARITHMETIC, both verdicts per check --------------------------------
    print("\n  ARITHMETIC — each check driven to FAIL and to OK:")
    cases = [
        ("BOUNDARY_UNITS", "30 accepts = 30 games (the CAL-8 attempt/accept miscount)",
         COMPLETE.replace("BOUNDARY: 30 accepts = 150 games", "BOUNDARY: 30 accepts = 30 games")
                 .replace("PLANNED n: 150 games", "PLANNED n: 30 games"), True),
        ("BOUNDARY_UNITS", "30 accepts = 150 games", COMPLETE, False),
        ("BOUNDARY_VS_N", "PLANNED n disagrees with the boundary",
         COMPLETE.replace("PLANNED n: 150 games", "PLANNED n: 120 games"), True),
        ("BAR_RESOLVABLE", "bar 58.0 vs base 50.0 at n=150 unrated (half-width ~9.6pp)",
         COMPLETE.replace("**BAR: 60.0**", "**BAR: 58.0**"), True),
        ("BAR_RESOLVABLE", "bar 60.0 vs base 50.0 at n=150 (margin 10.0pp)", COMPLETE, False),
        ("BAR_NULL", "bar == base rate",
         COMPLETE.replace("**BAR: 60.0**", "**BAR: 50.0**"), True),
        ("REFERENCE_FLOOR", "CAL-7 P1 rebuilt: +-8pp bar, retired reference n=155",
         CAL7_FLOOR, True),
        ("REFERENCE_FLOOR", "same bar against a reference of n=2000",
         CAL7_FLOOR.replace("REFERENCE n: 155", "REFERENCE n: 2000"), False),
        ("SEGMENT_CEILING", "25% x 6.0pp declared as 3.00pp",
         COMPLETE.replace("= 1.50pp pooled", "= 3.00pp pooled"), True),
        ("OB13_INTERSECTION", "declared INTERSECTION: no",
         COMPLETE.replace("INTERSECTION: yes.", "INTERSECTION: no."), True),
        ("DOSE_BOTH_VERDICTS", "a dose line quoting ONE number",
         COMPLETE.replace("**DOSE: seal-refusals 7.4/game vs flag-off 0.0/game "
                          "(n=12+12 probe shards)**",
                          "**DOSE: seal-refusals 7.4/game (n=12 probe shards)**"), True),
        ("DOSE_BOTH_VERDICTS", "treatment and flag-off IDENTICAL",
         COMPLETE.replace("vs flag-off 0.0/game", "vs flag-off 7.4/game"), True),
        ("DOSE_BOTH_VERDICTS", "7.4 vs flag-off 0.0", COMPLETE, False),
    ]
    for rid, label, txt, want_fail in cases:
        _r, fails, _w = run_checks(txt, f"<{rid}>", diff_paths=["eco.py", "main.py"], quiet=True)
        got = any(x[0] == rid for x in fails)
        ok = got == want_fail
        print(f"  [{'ok' if ok else 'FAIL'}] {rid:<18} {'FAIL' if want_fail else 'OK  '} "
              f"expected -> {'FAIL' if got else 'OK'}   {label}")
        bad += 0 if ok else 1

    # OB13 computed against a REAL diff list, both ways. The declared-yes case
    # must still FAIL when the metric's file is not in the actual diff -- that
    # is LOKI-18, and it is the whole reason the check is computed and not
    # merely read off the page.
    for label, paths, want_fail in (
            ("metric file IS in the diff", ["eco.py", "main.py"], False),
            ("metric file is NOT in the diff (LOKI-18)", ["main.py", "doctrine.py"], True),
            ("no computable diff -> WARN, never FAIL", None, False)):
        _r, fails, warns = run_checks(COMPLETE, "<ob13>", diff_paths=paths, quiet=True)
        got = any(x[0] == "OB13_INTERSECTION" for x in fails)
        ok = got == want_fail
        if paths is None:
            ok = ok and any("NOT COMPUTED" in w for w in warns)
        print(f"  [{'ok' if ok else 'FAIL'}] OB13_INTERSECTION computed: {label} -> "
              f"{'FAIL' if got else 'OK'}")
        bad += 0 if ok else 1

    # --- AMENDMENT MODE, both verdicts --------------------------------------
    print("\n  AMENDMENT — ADD-ONLY enforced, driven both ways:")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        locked = Path(td) / "locked.md"
        locked.write_text(COMPLETE)
        add_only = Path(td) / "add.md"
        add_only.write_text(COMPLETE + "\n**AMENDMENT A1: n>=75 floor added.**\n"
                                       "**CUT-SHORT: below 75 games, descriptive only (unchanged).**\n")
        widened = Path(td) / "widened.md"
        widened.write_text(COMPLETE.replace("**BAR: 60.0**", "**BAR: 52.0**"))
        import io, contextlib
        for lbl, p, want in (("append-only amendment", add_only, 0),
                             ("a quietly WIDENED bar", widened, 1)):
            with contextlib.redirect_stdout(io.StringIO()):
                rc = check_amendment(locked, p)
            ok = rc == want
            print(f"  [{'ok' if ok else 'FAIL'}] {lbl:<28} -> "
                  f"{'FAIL (edited)' if rc else 'OK (add-only)'}")
            bad += 0 if ok else 1

    # --- closed-form arithmetic reproduces PUBLISHED numbers ----------------
    # ⛔ THE CELL THAT MAKES THE FORMULAS AUDITABLE. Each target below was
    # computed independently by a prereg author and printed in a committed
    # document; if this tool reproduces all four, its half-width function is the
    # same function the documents were written with.
    print("\n  FORMULA — reproduces four half-widths already published in docs/research/:")
    checks = [
        ("CAL-8 panel n=75 vs ref n=155", 56.8, [(1.434, 75), (1.366, 155)], 16.2),
        ("CAL-8 panel n=300 vs ref n=155", 56.8, [(1.434, 300), (1.366, 155)], 11.3),
        ("CAL-8 floor at panel n=inf", 56.8, [(1.366, 155)], 9.1),
        ("EVICT58 25 games, unrated within-opponent", 50.0, [(1.434, 25)], 23.5),
        ("SPAWNPOCKET 2,700 local rows @ DEFF 0.98", 50.0, [(0.98, 2700)], 1.9),
    ]
    for label, p, terms, want in checks:
        got = half_width(p, terms)
        ok = abs(got - want) <= 0.05
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<44} +-{got:.1f}pp (published +-{want}pp)")
        bad += 0 if ok else 1

    # --- and finally: REPORT on the real CAL-8, do not assert ---------------
    print("\n" + "=" * 78)
    print("REAL PREREG READOUT (reported, NOT asserted — current practice is the "
          "measurement here, not the target)")
    print("=" * 78)
    for name in ("PREREG-CAL8-2026-08-14.md", "PREREG-SPAWNPOCKET-2026-08-14.md",
                 "PREREG-LEG-EVICT58-2026-08-14.md"):
        p = ROOT / "docs/research" / name
        if not p.exists():
            print(f"\n  {name}: NOT FOUND")
            continue
        rows, fails, _w = run_checks(p.read_text(), name, diff_paths=None, quiet=True)
        okn = sum(1 for r in rows if r[0].strip() == "ok")
        nan = sum(1 for r in rows if r[0].strip() == "n/a")
        print(f"\n  {name}")
        print(f"    presence {okn} ok / {nan} n-a / {len(rows)-okn-nan} FAIL; "
              f"{len(fails)} total failure(s)")
        print(f"    MISSING: {', '.join(x[0] for x in fails) or '(none)'}")

    print()
    print(f"PREREG_SELFTEST: {'PASS' if not bad else 'FAIL'}"
          + ("" if not bad else f"  ({bad} case(s) wrong)"))
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="validate ONE pre-registration document")
    ap.add_argument("path", nargs="?", help="path to a PREREG-*.md")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--amendment", nargs=2, metavar=("LOCKED", "AMENDED"),
                    help="ADD-ONLY enforcement: the amended file may only ADD "
                         "bar/branch lines, never edit or remove one")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.amendment:
        return check_amendment(Path(a.amendment[0]), Path(a.amendment[1]))
    if not a.path:
        print(__doc__)
        return 2
    p = Path(a.path)
    if not p.exists():
        print(f"REFUSING: {p} does not exist.\n\nPREREG_CHECK: FAIL")
        return 1
    return check_file(p)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
