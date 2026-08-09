#!/usr/bin/env python3
"""The GOVERNING slot rule, as ONE importable statement.

WHY THIS FILE EXISTS. The rule — "rolling last-5 net <= -21, armed after the
holder's 8th match, frees the slot" — was implemented inline in
`tools/monitors/elo_logger.py` and nowhere else. `tools/monitors/ship_watch.py`,
the only alarm that writes a file into the repo, implemented something ELSE (a
single fixed-baseline SPRT with no restart) while HANDOVER described it as the
stop-loss. Two implementations, one name, and the durable one was the wrong one.

The repo has learned this exact lesson twice already in `ship_watch`'s own
docstring: "CONSTANTS AND THE TEST ITSELF ARE IMPORTED, NEVER RE-DERIVED." That
line was written about MU0 and ALPHA. It applies to the SEGMENTATION and to the
RULE just as hard, and this file is where the rule now lives so there is
nothing left to re-derive.

THE RULE (Magnus+x3r0 2026-08-08, threshold recalibrated 2026-08-09 —
ship-gate.md amendment 2 changes with `SWAP_THRESHOLD` or not at all):

  * the window prices ONLY the current holder's matches — tape rows are
    filtered by the live version tag, so a holder change resets it naturally;
  * it ARMS only after the holder's 8th match;
  * while armed, `net5 <= -21` FREES the slot. It never forces a swap.

-21 is -1 sd of the rolling-5 sum (per-match sd 9.25, workflow-analysis v3).
The superseded `<=0` threshold sat at 0 sd of a 20.7-sd quantity and fired on a
coin flip (50.4% on a neutral holder at match 8).

WHAT THIS FILE DELIBERATELY DOES NOT DO. It does not decide. `slot_free` is a
permission, not an instruction — the slot rule is a stop-loss and a wake, never
an n=8 evaluation of the bot (auto-memory: slot-swap-rule).
"""
from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent
TAPE = ROOT / "elo_history.tsv"

SWAP_THRESHOLD = -21
ARM_AFTER = 8
WINDOW = 5


class SlotState(NamedTuple):
    version: str          # holder tag as it appears on the tape, e.g. "v102"
    holder_start: int     # matches_played at the holder's first tape row
    k: int                # matches under this holder
    rating: float         # latest rating
    matches: int          # latest matches_played
    base5: float | None   # rating 5 matches ago (None until the window fills)
    net5: float | None    # rating - base5
    armed: bool           # k >= ARM_AFTER
    slot_free: bool       # armed and net5 <= SWAP_THRESHOLD
    rows: list            # [(ts, rating, matches), ...] for this holder


def holder_rows(tape: Path | str = TAPE, version: str | None = None):
    """Rows for one holder, oldest first. `version` defaults to the tape's last
    tag — i.e. whoever is live right now."""
    parsed = []
    for line in Path(tape).read_text().splitlines()[1:]:
        p = line.split("\t")
        if len(p) >= 4 and p[2].isdigit():
            parsed.append((p[0], float(p[1]), int(p[2]), p[3]))
    if not parsed:
        return None, []
    tag = version or parsed[-1][3]
    return tag, [(ts, r, m) for ts, r, m, v in parsed if v == tag]


def evaluate(tape: Path | str = TAPE, version: str | None = None) -> SlotState | None:
    """The rule, computed exactly as `elo_logger` computes it."""
    tag, rows = holder_rows(tape, version)
    if not rows:
        return None
    _, rating, matches = rows[-1]
    holder_start = min(m for _, _, m in rows)

    # base = the most recent row at least WINDOW matches back. Rows are appended
    # in time order, so the last qualifying row is the newest one.
    base5 = None
    for _, r, m in rows:
        if m <= matches - WINDOW:
            base5 = r
    net5 = None if base5 is None else rating - base5
    armed = (matches - holder_start) >= ARM_AFTER
    slot_free = bool(armed and net5 is not None and net5 <= SWAP_THRESHOLD)

    return SlotState(version=tag, holder_start=holder_start,
                     k=matches - holder_start, rating=rating, matches=matches,
                     base5=base5, net5=net5, armed=armed, slot_free=slot_free,
                     rows=rows)


if __name__ == "__main__":
    st = evaluate()
    if st is None:
        raise SystemExit("no tape rows")
    n5 = "n/a" if st.net5 is None else f"{st.net5:+.1f}"
    print(f"{st.version}  k={st.k}  rating={st.rating:.1f}  net5={n5}  "
          f"armed={st.armed}  slot_free={st.slot_free}  "
          f"(threshold {SWAP_THRESHOLD}, arms after {ARM_AFTER})")
