#!/usr/bin/env python3
"""THE ONE PARSE OF PROGRAMME.md's machine-readable block.

⛔ WHY THIS FILE EXISTS (s47 wrap debt 12, 2026-08-16). Three tools read the
same fields out of PROGRAMME.md and TWO OF THEM DISAGREED ABOUT WHICH LINE WINS:

    tools/gate.py                     `^\\s{4}([A-Z_0-9]+):` , dict() -> LAST wins,
                                      and an UNINDENTED line is not a field at all
    tools/slot_rule.stop_loss_active  line.strip().startswith(...) -> FIRST wins,
                                      indented or not
    tools/monitors/elo_logger._stop_loss_active   a hand copy of slot_rule's

Reproduced on a constructed file (an unindented prose copy above the block):

    SLOT_STOP_LOSS: off          <- prose, unindented
        LINE: x
        SLOT_STOP_LOSS: on       <- the real field

    slot_rule.stop_loss_active() -> False  (read the prose)
    gate-style fields            -> {'SLOT_STOP_LOSS': 'on'}  (read the field)

Two live tools, one file, opposite answers, no error from either. PROGRAMME.md
has produced exactly this failure before (s31: `R1000_IS_DEFEAT` sat inside the
block headed "the fields below are parsed" and was never parsed, because the
name pattern excluded digits). A duplicated field is not hypothetical here.

THE RULE, and it is gate.py's, adopted wholesale:
  * A FIELD IS AN INDENTED LINE. Exactly four leading spaces, `NAME: value`,
    NAME in [A-Z_0-9]. Prose anywhere in the document is prose — a sentence
    that happens to contain `SLOT_STOP_LOSS: off` cannot change a live rule.
  * LAST OCCURRENCE WINS, because `dict(pairs)` already did and gate.py is the
    tool that WARNs about duplicates. One resolution, one warning, one place.

⚠ DIRECTION OF THE CHANGE, stated because a stop-loss switch must never be
moved quietly: the live PROGRAMME.md carries `    SLOT_STOP_LOSS: off` — four
spaces, one occurrence, line 29 — so this parse returns `off` (retired), which
is what all three tools returned before. Verified against the live file, not
argued from the code. The change is only in what an ADDED prose copy would do.

An unreadable PROGRAMME.md is not this module's business: each caller decides
its own failure direction (slot_loss callers fail toward ACTIVE, the alarm).
"""

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0. `__main__`-gated
# because slot_rule / gate / elo_logger IMPORT this module.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

import re

# Four spaces exactly, and DIGITS ARE IN THE NAME CLASS. `[A-Z_]+` was the
# original and it silently dropped `R1000_IS_DEFEAT` (s31). Do not narrow it.
FIELD_RE = re.compile(r"^\s{4}([A-Z_0-9]+):\s*(.+?)\s*$", re.M)

# Deliberately PERMISSIVE — a different character class from FIELD_RE, so a
# name FIELD_RE cannot parse still shows up in the declared count and the
# mismatch is visible. Matching classes would make that guard unable to fire.
DECLARED_RE = re.compile(r"^\s{4}[^\s:]+:\s", re.M)


def pairs(raw: str) -> list[tuple[str, str]]:
    """Every indented field line, IN ORDER, duplicates kept."""
    return FIELD_RE.findall(raw)


def declared(raw: str) -> int:
    """How many indented field lines exist, including unparseable names."""
    return len(DECLARED_RE.findall(raw))


def duplicates(raw: str) -> list[str]:
    """Field names appearing more than once in the indented block."""
    ps = pairs(raw)
    names = [k for k, _ in ps]
    return sorted({k for k in names if names.count(k) > 1})


def fields(raw: str) -> dict[str, str]:
    """The resolved field map. LAST occurrence wins."""
    return dict(pairs(raw))


def field(raw: str, name: str, default: str | None = None) -> str | None:
    return fields(raw).get(name, default)


def stop_loss_active_from_text(raw: str) -> bool:
    """`SLOT_STOP_LOSS: off` -> False. Absent -> True (active).

    Absent means ACTIVE on purpose: the field postdates every other deployment
    of this rule, and a stop-loss that goes quiet when its switch is missing
    fails in the direction that costs rating.
    """
    v = fields(raw).get("SLOT_STOP_LOSS", "")
    return not v.strip().lower().startswith("off")
