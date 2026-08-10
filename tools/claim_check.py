#!/usr/bin/env python3
"""CLAIM CHECK — every "mutation-tested" claim must point at ITS OWN record.

    .venv/bin/python tools/claim_check.py            # scan tools/
    .venv/bin/python tools/claim_check.py --selftest

WHY THIS EXISTS. On 2026-08-10 the builder wrote "mutation-tested" into a
comment or a commit message **three times** without committing the record:

  1. `panel2_cal.sh` header claimed both branches tested; the artifact had been
     deleted and no leg doc existed yet.
  2. `a49f87e` claimed the deficit-first count predicate was mutation-tested
     against the CLI banner split; the three cases had been run and none written.
  3. `panel3_cal.sh` header cited **PANEL-2's** 13:06:51Z run — a third copy of
     the same guard inheriting a citation instead of carrying a test.

**In all three the code was correct and the evidence was absent. All three were
caught by another lane; none by the author.** The failure is specific and
repeatable: *run the check, watch it pass, treat the passing as the artefact.*

**A claim whose evidence a reader cannot locate is a claim, not a test** — which
is the same standard this repo applies to instruments ("an instrument never
observed to fail is a claim"), turned on the people writing them.

WHAT IT CHECKS. For every file under `tools/` asserting it was mutation-tested /
both-branches-tested / selftested-to-both-verdicts, there must exist a record in
`docs/legs/` or `docs/research/` that **names that file**. Citing a sibling's
record does not count — that is exactly defect 3.

WHAT IT DOES NOT CHECK. That the record is honest, or that the test was any
good. It closes the gap between "I ran it" and "someone else can find it", which
is the gap that actually opened three times.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN = [ROOT / "tools"]
RECORD_DIRS = [ROOT / "docs" / "legs", ROOT / "docs" / "research"]

CLAIM = re.compile(
    r"mutation[- ]test|both branches (?:are |were )?(?:mutation[- ])?test|"
    r"driven to both verdicts|selftested to both",
    re.I,
)

_OVERRIDE: dict = {}


def records() -> dict[str, str]:
    """{path: text} for every candidate record document."""
    if "records" in _OVERRIDE:
        return _OVERRIDE["records"]
    out = {}
    for d in RECORD_DIRS:
        if not d.exists():
            continue
        for f in d.rglob("*.md"):
            try:
                out[str(f)] = f.read_text(errors="replace")
            except OSError:
                continue
    return out


def claimants() -> dict[str, str]:
    """{filename: text} for every tools/ file making a tested-claim.

    The CLAIM filter is applied to INJECTED fixtures too. First version returned
    the override dict unfiltered, so a fixture that makes no claim was still
    treated as a claimant and the "must stay silent" case failed -- the test
    bypassed the very predicate it was testing.
    """
    if "claimants" in _OVERRIDE:
        return {k: v for k, v in _OVERRIDE["claimants"].items()
                if CLAIM.search(v)}
    out = {}
    for d in SCAN:
        for f in sorted(d.rglob("*")):
            if f.suffix not in (".py", ".sh") or not f.is_file():
                continue
            if f.name == "claim_check.py":
                continue                     # this file describes the defect
            try:
                t = f.read_text(errors="replace")
            except OSError:
                continue
            if CLAIM.search(t):
                out[f.name] = t
    return out


def check() -> list[str]:
    recs = records()
    bad = []
    for name, _text in sorted(claimants().items()):  # noqa: B007
        # A record must NAME this file, ON A WORD BOUNDARY. Plain substring
        # matching passed `runner.sh` against a record that only named
        # `other_runner.sh` -- the sibling-citation case is EXACTLY defect 3,
        # so a checker that cannot see it is worse than none.
        pat = re.compile(r"(?<![\w.-])" + re.escape(name))
        hit = [p for p, t in recs.items() if pat.search(t)]
        if not hit:
            bad.append(f"{name}: claims a mutation test, NO record in "
                       f"docs/legs or docs/research names it")
        # RULE 2 — THE ONE THAT CATCHES DEFECT 3, AND RULE 1 CANNOT.
        # Rule 1 asks "does SOME record name this file". Once a correct record
        # exists, a header still citing a SIBLING's document passes rule 1
        # forever. That is exactly what happened: the first version of this
        # checker passed its own selftest and then MISSED the historical
        # panel3 header, because by then a good LEG-panel3 doc existed.
        # So: if the file CITES a specific document, that document must name
        # this file. A citation is a promise about where the evidence is.
        for cited in re.findall(r"docs/[\w/.-]+\.md", _text):
            body = next((t for pth, t in recs.items() if pth.endswith(cited)), None)
            if body is None:
                continue                     # missing doc is rule 1's business
            if not re.search(r"(?<![\w.-])" + re.escape(name), body):
                bad.append(f"{name}: cites {cited} for its mutation test, but "
                           f"that document never names {name} -- a sibling's "
                           f"record is not this file's evidence")
    return bad


def selftest() -> int:
    """Drive both verdicts: a claim with a record, and one without."""
    print("CLAIM CHECK SELFTEST\n")
    bad = 0
    cases = [
        ("claim + record naming it", {"runner.sh": "both branches mutation-tested"},
         {"docs/legs/LEG-x.md": "abort branch of runner.sh run at 12:00Z"}, 0),
        ("claim + record naming a SIBLING only",
         {"runner.sh": "both branches mutation-tested"},
         {"docs/legs/LEG-x.md": "abort branch of other_runner.sh run at 12:00Z"}, 1),
        ("claim + NO records at all",
         {"runner.sh": "mutation-tested"}, {}, 1),
        ("no claim at all -> must stay silent",
         {"runner.sh": "just a normal script"},
         {"docs/legs/LEG-x.md": "unrelated"}, 0),
        # THE HISTORICAL CASE: a good record for this file EXISTS, and the
        # header still cites a sibling's document. Rule 1 passes; rule 2 must
        # fire. This is the case the first version of the checker missed.
        ("record exists BUT header cites a sibling doc",
         {"runner.sh": "mutation-tested: see docs/legs/LEG-other.md"},
         {"docs/legs/LEG-mine.md": "abort branch of runner.sh at 12:00Z",
          "docs/legs/LEG-other.md": "abort branch of other_runner.sh"}, 1),
    ]
    for label, cl, rc, want in cases:
        _OVERRIDE.clear()
        _OVERRIDE.update({"claimants": cl, "records": rc})
        got = len(check())
        ok = got == want
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<40} flagged={got} want={want}")
        if not ok:
            bad += 1
    _OVERRIDE.clear()
    print()
    if bad:
        print(f"*** {bad} case(s) wrong -- the check is not checking ***")
        return 1
    print("PASS: flags a claim with no record and a claim citing only a "
          "sibling; silent when the record names the file, and when no claim "
          "is made.")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    bad = check()
    n = len(claimants())
    print(f"CLAIM CHECK — {n} file(s) in tools/ assert a mutation test\n")
    for b in bad:
        print(f"  *** {b}")
    if bad:
        print(f"\n{len(bad)} unbacked claim(s). Either commit the record "
              f"(the record IS the test) or drop the claim.")
        return 1
    print("  every tested-claim points at a record that names its own file")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
