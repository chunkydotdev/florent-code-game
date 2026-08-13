#!/usr/bin/env python3
"""CORES IDLE WATCH — the machine has 10 cores and nothing is using them.

WHY THIS EXISTS, AND IT IS A MAGNUS CATCH NOT A DESIGN
------------------------------------------------------
2026-08-11 (s31), Magnus, twice in ten minutes:
  *"anything running locally?"*
  *"do we not monitor the local runs? if nothing is running we're losing time
    we could use to figure out the next Loki version"*
  *"If we are not running locally we should grab items from the queue and run
    them, the researcher has a monitor that makes them put more items in the
    queue if it is running out."*

**HE HAD TO ASK. There was no instrument.** We monitor the ladder (elo_logger),
our matches (match_watcher), the field (opp_watcher), the archive
(replay_archiver), the slot (ship_watch) and the corpus (keeper) — **six monitors,
all pointed at the PLATFORM, and not one pointed at whether our own machine is
doing anything.** At 13:53Z the load average had drained 14.67 -> 1.57 with zero
`fcode run` processes and a full queue sitting unread.

**THE ASYMMETRY THAT MADE IT INVISIBLE:** every other monitor watches a thing
that CHANGES and alarms on a bad value. Idle cores are not a bad value — they are
the ABSENCE of a value, and absence is what this repo's monitors have repeatedly
failed to see (`ship_watch` printing healthy lines off a stale tape; a screen
that cannot fire; a guard whose declared-count used the same broken pattern).
**An alarm that cannot tell it is blind, and an alarm for a thing that is simply
not happening, are the same failure.**

WHAT IT DOES
------------
Counts running `fcode run` processes. If FEWER THAN `EXPECTED_GAMES` (default 1)
for two consecutive polls, it prints an ALERT naming the top unblocked item in
`QUEUE.md` — the queue is the answer to "what should be running", so the alarm
carries its own remedy.

⛔ THIS PARAGRAPH SAID "If ZERO" UNTIL 2026-08-12 (s33) AND THE CODE HAD SAID
`n < expected` SINCE s31. A stale docstring beside live code is not cosmetic:
the side lane published a wrong conclusion off THIS SENTENCE in s32 — one of
four errors that session, all of them "inferred from an artefact instead of
opening the primary", and a docstring is the artefact that most looks like the
primary. Fixed here on Magnus's "fix your findings", together with the alert
wording below, which had the same gap: `games=2/5` printed "*** CORES IDLE ***"
while a runner was alive, so a reader had to caveat the alarm before quoting it.
⚠ `PROGRAMME.md:60-62` still describes the retired `n == 0` predicate. That file
is edited only on Magnus's explicit directive, so it is FLAGGED, not fixed.

⛔ IT GATES ON THE PROCESS COUNT, NEVER ON AN EXIT CODE, and it reports the AGE
of what it read — both standing repo rules (`fcode status` exits 0 while printing
`Error: True`; a monitor that reads a file must report that file's freshness).

Usage:  cores_idle.py            # one poll, prints a line
        cores_idle.py --selftest # forced-answer cells
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
STATE = Path(os.environ.get("STATE_DIR", ROOT / "corpus")) / "cores_idle_state.json"
QUEUE = ROOT / "QUEUE.md"
ALERT = ROOT / "corpus" / "CORES_IDLE_ALERT"


def running_games() -> int:
    """Count live local games. Process count, not an exit code."""
    try:
        out = subprocess.run(["ps", "ax", "-o", "command="],
                             capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return -1                       # UNKNOWN, never silently 0
    n = 0
    for line in out.splitlines():
        if "fcode" in line and re.search(r"\bfcode\b.*\brun\b", line):
            n += 1
    return n


def _fire_order_numbers(text: str) -> list[str]:
    """Row numbers in the order `QUEUE.md`'s own FIRE ORDER block ranks them.

    ⛔ THE FILE DECLARES ITS LINE ORDER VOID AND THIS READER USED TO IGNORE THAT:
    *"THIS BLOCK SUPERSEDES POSITIONAL ORDER IN THE SECTIONS BELOW."* Returns []
    when no fire-order block is present, which the caller treats as "fall back to
    admission order AND SAY SO" — never as "positional order is correct".
    """
    out, seen, in_block = [], set(), False
    for line in text.splitlines():
        if "FIRE ORDER" in line and line.lstrip().startswith("#"):
            in_block = True
            continue
        if in_block and line.startswith("## ") and "FIRE ORDER" not in line:
            break                       # next top-level section ends the block
        if not in_block:
            continue
        for num in re.findall(r"`?#(\d+)`?", line):
            if num not in seen:
                seen.add(num)
                out.append(num)
    return out


def next_queue_item():
    """The next row a builder should actually START — admitted AND top-ranked.

    ⛔ REWRITTEN 2026-08-13 (s35). THIS FUNCTION HAD TWO INDEPENDENT DEFECTS AND
    BOTH POINTED THE SAME WAY: it handed a 3am builder a row that could not be
    built.

    1. IT RE-IMPLEMENTED THE ADMISSION GATE, AND DISAGREED WITH IT. It skipped
       only `~~`/`WITHDRAWN`/`SHIPPED`, while `queue_check.unblocked()` also
       requires a substantive `GREP:` cell (the incumbent check) and rejects
       `STATUS:` tokens and unmet-grep markers. Measured on live data at s35 boot:
       `queue_check` counted 19 rows and **the row THIS function returned was not
       among them.** That is the s29 green-selftest signature — a second copy of
       the computation — here in PRODUCTION rather than in a test. Fixed by
       CALLING `queue_check.unblocked()` instead of imitating it.
    2. IT READ POSITIONAL ORDER OUT OF A FILE THAT DECLARES POSITIONAL ORDER
       SUPERSEDED. `rows[0]` is whatever sits highest in the markdown.

    ⭐ AND (2) IS A CLASS, NOT AN INCIDENT — three instances in this repo:
    this function; `corefill.sh`, where an arm Magnus asked for twice sat queued
    behind two others purely by LINE POSITION; and `fanout.sh`, whose retry
    exhaustion always drops the TAIL of the id list (CLAUDE.md prescribes
    rotating the start cell; `panel2_cal.sh` does, `fanout.sh` still does not).
    **In all three the file has no field expressing intent, so line order BECOMES
    the policy and is then edited by people who do not know that.** The tell is a
    reader taking `[0]` over a human-maintained list. Class named by the side
    lane; instances 1 and 2 fixed, 3 left as CLAUDE.md already prescribes it.

    Returns (label_or_None, age_min).
    """
    if not QUEUE.exists():
        return None, None
    age_min = (time.time() - QUEUE.stat().st_mtime) / 60.0
    text = QUEUE.read_text()

    try:                                # call the REAL gate, never a copy of it
        sys.path.insert(0, str(ROOT / "tools"))
        import queue_check              # noqa: E402
        admitted = queue_check.unblocked(queue_check.parse(text))
        labels = [queue_check.label(row) for _sec, row in admitted]
    except Exception as exc:            # BLIND, not empty — say which
        return f"(BLIND: queue_check unavailable: {exc})", age_min

    if not labels:
        return None, age_min

    def numof(lbl: str):
        m = re.match(r"\s*#?(\d+)", lbl)
        return m.group(1) if m else None

    by_num = {}
    for lbl in labels:
        n = numof(lbl)
        if n is not None:
            by_num.setdefault(n, lbl)

    for n in _fire_order_numbers(text):     # ranked order wins
        if n in by_num:
            return by_num[n], age_min

    # No fire-order row is admitted. Fall back, but SAY it is a fallback —
    # a silent fallback here is how positional order became policy in the
    # first place.
    return f"{labels[0]}  [no ranked row admitted; admission order]", age_min


def main() -> int:
    n = running_games()
    prev = {}
    if STATE.exists():
        try:
            prev = json.loads(STATE.read_text())
        except Exception:
            prev = {}
    # ⛔ EXPECTED, NOT ZERO. The first version's predicate was `n == 0`, so
    # 8 of 9 shards dying overnight would read `OK` and DELETE the alert file --
    # an idleness alarm blind to 89% idleness. (Side lane audit, s31.)
    expected = int(os.environ.get("EXPECTED_GAMES", "1"))
    consec = prev.get("consec_idle", 0)
    if n < expected:
        consec += 1
    else:
        consec = 0
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"consec_idle": consec, "last_n": n,
                                 "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                     time.gmtime())}))
    item, age = next_queue_item()
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if n < 0:
        print(f"{stamp}\tgames=UNKNOWN\tCORES=BLIND (ps failed) — not reporting idle")
        return 0
    qs = f"queue_age_min={age:.1f}" if age is not None else "queue=MISSING"
    short = f"games={n}/{expected}"
    if consec >= 2:
        # `CORES IDLE` is kept VERBATIM for n == 0 because PROGRAMME.md quotes
        # that literal string; the shortfall case gets its own honest wording
        # rather than borrowing a word that is not true of it.
        _what = ("CORES IDLE" if classify(n, expected) == "idle"
                 else f"CORES UNDER-USED ({n} of {expected})")
        msg = (f"{stamp}\t{short}\tconsec_idle={consec}\t{qs}\t"
               f"*** {_what} — NEXT QUEUE ITEM: {item or 'QUEUE EMPTY'} ***")
        print(msg)
        with ALERT.open("a") as fh:
            fh.write(msg + "\n")
    else:
        print(f"{stamp}\t{short}\tconsec_idle={consec}\t{qs}\tOK")
        if n > 0 and ALERT.exists():
            ALERT.unlink()                # cleared by work actually starting
    return 0


def classify(n: int, expected: int) -> str:
    """The predicate, as a PURE function so the selftest can drive it.

    It was inline, which is why `--selftest` had no cell for it and could not
    have caught the docstring drift above. Returns 'blind' | 'idle' | 'under'
    | 'ok'. 'idle' and 'under' both count toward `consec_idle`; they differ only
    in what the alarm CALLS itself, and that difference is the s33 fix.
    """
    if n < 0:
        return "blind"
    if n == 0:
        return "idle"
    return "under" if n < expected else "ok"


def selftest() -> bool:
    ok = True

    def cell(name, got, want, forced):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  [{'ok' if good else 'FAIL'}] {name:<44} got={got} want={want}")
        print(f"         forced by: {forced}")

    # ⛔ THE CELL THAT MATTERS: a ps failure must NOT read as "idle". An alarm
    # that cannot tell it is BLIND is the ship_watch failure in a new instrument.
    real = running_games()
    cell("counts live fcode run processes", real >= 0, True,
         "a negative return means ps failed; the caller must treat that as "
         "BLIND, never as zero games")

    # The queue parser must find a real row, or the alarm's remedy is empty.
    item, age = next_queue_item()
    cell("reads a queue item", item is not None, True,
         "the alarm names the next plank; if the parser returns None the alarm "
         "fires with no remedy and is just noise")

    # ⛔ THE CELL THIS REPLACED ASSERTED ON THE FIXTURE, NOT THE PARSER: it
    # checked that QUEUE.md *contains* "~~" and never that the parser SKIPPED
    # such a row, so it would have passed with the filter deleted. That is the
    # fourth instance in one session of an assertion that did not test its own
    # claim (effective_n's ceiling cell, overnight_read's nowin, queue_check's
    # three marker cells). The parser is exercised above by "reads a queue item";
    # what is added here is the predicate, which had NO cell at all -- which is
    # why the docstring could say `n == 0` for a session while the code said
    # `n < expected` and --selftest stayed green.
    cell("predicate: 0 of 5 is IDLE", classify(0, 5), "idle",
         "the original predicate; must still fire")
    cell("predicate: 2 of 5 is UNDER-USED, not idle", classify(2, 5), "under",
         "the s31 fix -- 8 of 9 shards dying read OK under `n == 0` and DELETED "
         "the alert file, an idleness alarm blind to 89% idleness")
    cell("predicate: 5 of 5 is OK", classify(5, 5), "ok",
         "the alarm must be able to return the OTHER verdict, or it validates "
         "everything")
    cell("predicate: 12 of 5 is OK (over-subscribed is not a fault)",
         classify(12, 5), "ok", "observed live at 04:38Z")
    cell("predicate: a ps failure is BLIND, never idle", classify(-1, 5),
         "blind", "an alarm that cannot tell it is blind is this repo's "
         "most-repeated defect")
    cell("wording: only the n==0 case may call itself CORES IDLE",
         classify(2, 5) == "idle", False,
         "`games=2/5` printed `*** CORES IDLE ***` with a runner alive, so the "
         "side lane had to caveat the alarm before it could be quoted at boot")
    print("\nCORES_IDLE_SELFTEST: " + ("PASS" if ok else "FAIL"))
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    sys.exit(main())
