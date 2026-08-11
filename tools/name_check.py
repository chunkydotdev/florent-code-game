#!/usr/bin/env python3
"""NAME CHECK — does every identifier a document NAMES actually exist?

    .venv/bin/python tools/name_check.py docs/research/SOME-DOC.md [...]
    .venv/bin/python tools/name_check.py --selftest
    .venv/bin/python tools/name_check.py --changed        # docs changed vs origin/main

WHY THIS EXISTS — s29, 2026-08-11, and it is one incident not a category.

`hold_any` and `hold_pinned` were coined by the research arm inside
`docs/research/ADJUDICATION-ring-occupancy-decoders-2026-08-11.md`, in a section
headed "RECOMMENDED AGREED DEFINITION", instructing readers to "name it
`hold_any` or `hold_pinned`".

**`ring_read.py` implements NEITHER under those names.** It computes
`tile_episodes` (== hold_pinned) and `bot_episodes` (same bot, ANY tile — a third
thing). `hold_any` as the document defined it is computed nowhere.

The name then travelled through THREE LANES and TWO DOCUMENTS and became the
deciding call of an amendment. Nobody checked. The falsifying evidence was inside
the coining document itself -- its own RELAY fixture records the tool returning
0.500 where `hold_any` would be 1.000.

THE RULE THIS ENFORCES, from the s29 wrap (D54):
    A name introduced in a document must cite the file and line that implements
    it, or be marked PROPOSED.

WHY A TOOL AND NOT A D-RULE. Measured at the s29 wrap:
    * 36 D-rules recorded in docs/coordination.md
    * 2 of them name a tool that enforces them
    * D30 ("an audit of the evidence is not an audit of the codebase") was
      violated by its own author twice the afternoon it was written, and again
      the next session.
Prose rules decay. The rules that changed behaviour on 2026-08-11 were the ones
that ran as a command: audit_trigger.py, target_value.py, gate.py.

SCOPE, STATED SO THE OUTPUT IS NOT OVER-READ. This is a LINTER, not an oracle.
It reports identifiers that look like code and are not found in the tree. It
cannot know whether a name is meant as code. Expect false positives; they are
cheap (add PROPOSED, or cite the file). A FALSE NEGATIVE is the expensive one,
so the matcher is deliberately broad.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEARCH_DIRS = ("tools", "bots", "corpus")

# An identifier that LOOKS like code: snake_case with an underscore, or dotted
# module-ish, or a *.py filename. Deliberately broad -- see SCOPE above.
IDENT = re.compile(r"^[a-z_][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)?$")

# Markers that exempt a name: the author has flagged it as not-yet-implemented.
EXEMPT = re.compile(r"PROPOSED|NOT IMPLEMENTED|does not exist|implemented nowhere"
                    r"|names nothing|coined here|NOT computed", re.I)

# Names that are language/stdlib/API vocabulary, not this repo's code.
STOPWORDS = {
    # python / shell
    "true", "false", "none", "null", "self", "int", "str", "float", "bool",
    "dict", "list", "set", "print", "open", "date", "sort_keys",
    # engine API (documented in CLAUDE.md, not in our tree)
    "run", "can_move", "move", "build", "can_build", "fire", "can_fire",
    "rotate", "can_rotate", "heal", "can_heal", "destroy", "can_destroy",
    "spawn_builder", "can_spawn", "convert_ammo", "can_convert_ammo",
    "self_destruct", "resign", "read_store", "write_store", "launch",
    "can_launch", "get_id", "get_hp", "get_team", "get_position",
    "delta", "opposite", "rotate_left", "rotate_right", "is_cardinal",
    "add", "distance_squared", "direction_to", "cardinal_direction_to",
}


def repo_corpus() -> str:
    """Every byte of our own source, concatenated once. Slow-ish, simple, correct."""
    buf = []
    for d in SEARCH_DIRS:
        p = ROOT / d
        if not p.is_dir():
            continue
        for f in p.rglob("*"):
            if f.suffix in (".py", ".sh", ".tsv", ".json", ".md") and f.is_file():
                try:
                    buf.append(f.read_text(errors="ignore"))
                except OSError:
                    pass
    return "\n".join(buf)


def is_defined(name: str, corpus: str) -> bool:
    """Does `name` appear in a DEFINING position, not merely mentioned?

    ⛔ THIS IS THE WHOLE TOOL, AND THE FIRST VERSION GOT IT WRONG.

    v1 asked "does the name appear anywhere in our source?" It passed its own
    selftest and then returned CLEAN on the exact document that motivated it --
    because `hold_any` DOES appear in `tools/ring_read.py`, inside a docstring
    that exists to say the name means nothing. **A mention satisfied a test for
    existence.** The tool reproduced, in its own resolver, the failure it was
    built to catch.

    So resolution requires a definition site: a def/class, an assignment, a dict
    key, or a real file on disk. A name that lives only in prose does not count,
    which is precisely the `hold_any` case.
    """
    if (ROOT / name).is_file():
        return True
    esc = re.escape(name)
    patterns = (
        rf"^\s*(?:def|class)\s+{esc}\b",          # def name / class name
        rf"^\s*{esc}\s*(?::[^=\n]*)?=[^=]",        # name = ... / name: T = ...
        rf"['\"]{esc}['\"]\s*:",                   # "name": dict key
        rf"^\s*{esc}\s*=",                         # bare assignment
        rf"--{esc}\b",                             # a CLI flag
    )
    return any(re.search(p, corpus, re.M) for p in patterns)


def check_text(text: str, corpus: str) -> list[tuple[int, str]]:
    """Return [(line_no, name)] for backticked code-ish names with no definition site."""
    missing: list[tuple[int, str]] = []
    seen: set[str] = set()
    for i, line in enumerate(text.splitlines(), 1):
        if EXEMPT.search(line):
            continue
        for name in re.findall(r"`([^`\n]{2,60})`", line):
            name = name.strip()
            if name.lower() in STOPWORDS or name in seen:
                continue
            if not (IDENT.match(name) or name.endswith(".py")):
                continue
            if is_defined(name, corpus):
                continue
            seen.add(name)
            missing.append((i, name))
    return missing


def selftest() -> int:
    """Drive the checker to BOTH verdicts. A check that has only ever passed
    has not been seen to check (repo standard, and the reason `hold_any`
    survived three lanes)."""
    corpus = "def tile_episodes(): pass\nbot_episodes = 1\n"
    fails = 0

    # 1. NEGATIVE case: a name that does not exist MUST be flagged.
    bad = "Name it `hold_any` or `hold_pinned` when reading the series.\n"
    got = check_text(bad, corpus)
    names = {n for _, n in got}
    if names != {"hold_any", "hold_pinned"}:
        print(f"  FAIL negative: expected both coinages flagged, got {sorted(names)}")
        fails += 1
    else:
        print("  ok  negative: unimplemented coinages are flagged")

    # 2. POSITIVE case: a name that DOES exist must NOT be flagged.
    good = "The tool computes `tile_episodes` and `bot_episodes`.\n"
    if check_text(good, corpus):
        print(f"  FAIL positive: real names flagged: {check_text(good, corpus)}")
        fails += 1
    else:
        print("  ok  positive: implemented names pass clean")

    # 3. EXEMPTION works.
    exempt = "`hold_any` is PROPOSED and implemented nowhere yet.\n"
    if check_text(exempt, corpus):
        print("  FAIL exemption: PROPOSED line was still flagged")
        fails += 1
    else:
        print("  ok  exemption: PROPOSED suppresses the flag")

    # 4. MUTATION: break the corpus and the positive case must FLIP to failing.
    #    Without this, a corpus that silently matched everything would pass 1-3.
    if not check_text(good, corpus=""):
        print("  FAIL mutation: empty corpus still passed real names "
              "-- the matcher is not actually consulting the corpus")
        fails += 1
    else:
        print("  ok  mutation: emptying the corpus flips the positive case to FAIL")

    # 5. ⛔ THE CASE THAT FOOLED v1 OF THIS TOOL, and the reason `is_defined` exists.
    #    A name MENTIONED in a docstring -- here, one that exists purely to say the
    #    name means nothing -- must NOT count as a definition. v1 asked "does it
    #    appear anywhere?", passed tests 1-4, and returned CLEAN on the real
    #    document. This cell is that document, minimised.
    mention_only = (
        '"""THE TWO SERIES ARE NOT `hold_any` AND `hold_pinned`.\n'
        '`hold_any` is not computed by this file at all."""\n'
        'per_bot_tile = {}\n'
        'out = {"tile_episodes": 1}\n'
    )
    got5 = {n for _, n in check_text("Name it `hold_any`.\n", mention_only)}
    if got5 != {"hold_any"}:
        print(f"  FAIL mention-only: a docstring MENTION satisfied existence -- "
              f"this is the v1 bug, got {sorted(got5)}")
        fails += 1
    else:
        print("  ok  mention-only: a name that only appears in prose is still FLAGGED")
    if check_text("The series is `tile_episodes`.\n", mention_only):
        print("  FAIL mention-only: a real dict-key definition was flagged")
        fails += 1
    else:
        print("  ok  mention-only: a real definition site still resolves")

    print("SELFTEST:", "PASS" if not fails else f"FAIL ({fails})")
    return 1 if fails else 0


def changed_docs() -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            cwd=ROOT, capture_output=True, text=True, timeout=20).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    return [ROOT / p for p in out.split()
            if p.endswith(".md") and (ROOT / p).is_file()]


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()

    paths = changed_docs() if "--changed" in argv else [Path(a) for a in argv if a.endswith(".md")]
    if not paths:
        print(__doc__.strip().split("\n\n")[0])
        print("\nno documents given. Use --changed, or pass .md paths, or --selftest.")
        return 0

    corpus = repo_corpus()
    total = 0
    for p in paths:
        if not p.is_file():
            continue
        hits = check_text(p.read_text(errors="ignore"), corpus)
        if not hits:
            continue
        rel = p.relative_to(ROOT) if p.is_absolute() and ROOT in p.parents else p
        print(f"\n{rel}")
        for line_no, name in hits:
            print(f"  :{line_no}  `{name}` — not found in {'/, '.join(SEARCH_DIRS)}/")
        total += len(hits)

    if total:
        print(f"\n{total} name(s) introduced with no implementation found.")
        print("Cite the file:line that implements each, or mark it PROPOSED.")
        print("(Linter, not an oracle — false positives are cheap and expected.)")
    else:
        print(f"clean — every code-ish name in {len(paths)} document(s) resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
