#!/usr/bin/env python3
"""ONE ROW PER INVOCATION for the tools that carry escape flags.

⛔ WHY EVERY INVOCATION AND NOT EVERY ESCAPE — the correction that produced this
file's shape. The first spec said "append a row when an escape flag is taken".
**That tape yields a COUNT and has no DENOMINATOR**, and the question it was
minted to answer is a RATE: *how often is the gate bypassed?* A session that ran
the gate ten times and escaped twice is BYTE-IDENTICAL, on a numerator-only tape,
to one that ran it twice and escaped twice. So:

    EVERY invocation writes a row, and `escapes` is EMPTY in most of them.
    Escaped rows are the NUMERATOR; ALL rows are the DENOMINATOR.

⛔ AND NO `prereg_path` COLUMN. `gate.py` guards a BATTERY -- its argv is
`--plank/--control/--parent/--opponents/--maps` and it never sees a prereg path.
A column that is empty in every row validates anything; this repo has the scar
(`ladder_games.tsv.oppver` was the literal string `'None'` in 4,375 of 4,375
rows and nothing noticed for four days). The BATTERY IDENTITY is what `gate.py`
actually knows, so that is what goes in `subject`.

⛔ AND IT LIVES AT THE REPO ROOT, TRACKED, NOT UNDER `corpus/`.
First cut wrote it to `corpus/tool_invocations.tsv`, which `corpus/.gitignore:2`
(`*.tsv`) IGNORES. That is correct for everything else in `corpus/` -- those
tapes are DECODED DATA and a fresh clone can regenerate them. **An escape is a
one-shot governance EVENT: nobody can re-derive who bypassed which gate, when,
and for what stated reason.** A bypass-rate tape that cannot leave the machine
that recorded it answers the question only for whoever is already sitting there,
which is the one person who does not need to ask. So it follows the
`elo_history.tsv` pattern -- repo root, tracked, append-only, travels.

Read the rate with:
    awk -F'\\t' 'NR>1 && $2=="gate.py"{n++; if($6!="") e++} END{print e"/"n}' \\
        gate_invocations.tsv

Path override: $TOOL_INVOCATION_TAPE (the probe uses it so a forced-fail run
never lands on the real tape).
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TAPE = ROOT / "gate_invocations.tsv"

COLUMNS = ("ts", "tool", "user", "host", "mode", "escapes", "setter", "reasons", "subject")


def tape_path() -> Path:
    return Path(os.environ.get("TOOL_INVOCATION_TAPE") or DEFAULT_TAPE)


def _clean(v: object) -> str:
    """Tabs and newlines are the record separators; a value carrying one would
    silently shift every column to its right."""
    return " ".join(str(v).split()) if v is not None else ""


def record(tool: str, subject: str, escapes: dict[str, str] | None = None,
           setter: str = "argv", mode: str = "") -> Path | None:
    """Append ONE row. Returns the tape path, or None if the write failed.

    `escapes` maps flag name -> reason string. An EMPTY mapping is the normal
    case and still writes a row -- that is the whole design (see the module
    docstring). Never raises: a tape that cannot be written must not take down
    the gate it is observing, but it says so on stderr rather than pretending.
    """
    escapes = escapes or {}
    row = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": tool,
        "user": os.environ.get("USER") or os.environ.get("LOGNAME") or "?",
        "host": os.uname().nodename,
        "mode": mode,
        "escapes": ",".join(sorted(escapes)),
        # WHO set it. Today every escape on both tools is typed on the command
        # line; the column exists so an env- or config-set escape cannot arrive
        # later and be indistinguishable from a typed one.
        "setter": setter if escapes else "",
        "reasons": " | ".join(f"{k}={escapes[k]}" for k in sorted(escapes)),
        "subject": subject,
    }
    p = tape_path()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        new = not p.exists() or p.stat().st_size == 0
        with p.open("a") as fh:
            if new:
                fh.write("\t".join(COLUMNS) + "\n")
            fh.write("\t".join(_clean(row[c]) for c in COLUMNS) + "\n")
        return p
    except Exception as exc:                                       # noqa: BLE001
        print(f"WARN  invocation tape not written ({p}): {exc}", file=sys.stderr)
        return None


def rate(tool: str | None = None) -> tuple[int, int]:
    """(escaped rows, total rows) -- the numerator AND its denominator."""
    p = tape_path()
    if not p.exists():
        return (0, 0)
    esc = tot = 0
    for i, line in enumerate(p.read_text().splitlines()):
        if i == 0 or not line.strip():
            continue
        f = line.split("\t")
        if len(f) < len(COLUMNS):
            continue
        if tool and f[1] != tool:
            continue
        tot += 1
        if f[5]:
            esc += 1
    return (esc, tot)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else None
    e, n = rate(which)
    print(f"{tape_path()}\nescaped {e} / {n} invocation(s)"
          + (f"  ({100.0*e/n:.1f}% bypass rate)" if n else "  (no rows)"))
