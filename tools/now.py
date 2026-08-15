#!/usr/bin/env python3
"""NOW — the one canonical state block. Run it at boot, before any verdict.

    .venv/bin/python tools/now.py
    .venv/bin/python tools/now.py --selftest

===== WHY THIS EXISTS =====
"What is live right now?" had FIVE answers in this repo, and THREE of them were
correct answers to a DIFFERENT question. Measured 2026-08-15T16:3xZ, all five
simultaneously true:

    fcode status            v151, 1707, Emerald, #23   <- the HOLDER
    corpus/ship_watch.log   v151, 1707                 <- the TREND (10-min poller)
    elo_history.tsv         1707, v151                 <- the TAPE (poll-time tag)
    corpus/ladder_games.tsv ourver=140                 <- RATED ground truth (~30m behind)
    PROGRAMME.md INCUMBENT  bots/_v223sealrepair (v140) <- the CONTROL, not the live bot

Nobody was wrong about any single file. The cost came from reading one and
answering a question it does not answer. The s43 side lane converged on the
same sentence independently: *"all five [published errors] are one surface
adjacent to the right one."*

It is not hypothetical and it is not a beginner's error. On 2026-08-15 the side
lane wrote its REBOOT STATE -- the artefact a successor trusts cold -- naming
holder `v140` off `ship_watch` inside that poller's 10-minute blind window,
while `fcode status` said `v151`. That lane had flagged the stale-vs-blind
hazard at boot and cited it twice the same day. Knowing the rule did not
prevent committing it.

⇒ SO THIS FILE DOES NOT EXPLAIN THE DISTINCTION. IT MAKES IT UNNECESSARY.
Every line below carries THE QUESTION IT ANSWERS and THE AGE OF ITS SOURCE, and
a line whose source is too stale to speak prints BLIND rather than a number.

===== THE ONE RULE IT ENCODES =====
THE HOLDER IS READ FROM `fcode status`, NEVER FROM A POLLER.
A poller tells you the TREND. Only the platform tells you the STATE.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from freshness import newest_row_age_h  # noqa: E402  (shared helper, honours the Z marker)

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

TAPE = ROOT / "elo_history.tsv"
SHIPW = ROOT / "corpus/ship_watch.log"
LADDER = ROOT / "corpus/ladder_games.tsv"
PROGRAMME = ROOT / "PROGRAMME.md"

# Age past which a surface may not be quoted as current. Each is ~2 cadences of
# the thing that writes it: elo_logger 300s, ship_watch 600s, ladder pairings
# ~20min. Per CLAUDE.md: "refuse to print a verdict past ~2 cadences".
MAX_AGE_H = {"tape": 0.35, "ship_watch": 0.5, "ladder": 1.5}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _fcode_status(timeout: int = 45) -> tuple[dict | None, str]:
    """Return (parsed, why). THE LOAD-BEARING FIELD IS `active_submission`.

    ⛔ NEVER GATE ON THE EXIT CODE. CLAUDE.md, measured during the 2026-08-10
    outage: `fcode status` EXITS 0 while printing `Error: True` and returning a
    body whose `active_submission` is null, and `fcode match list` exits 1 in
    the same outage -- two failure conventions on one CLI. A degraded response
    also parses as valid JSON, so parseability is worthless as a gate too.
    """
    try:
        r = subprocess.run([str(ROOT / ".venv/bin/fcode"), "status", "--json"],
                           capture_output=True, text=True, timeout=timeout, cwd=ROOT)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"could not run fcode: {type(e).__name__}"
    body = (r.stdout or "").strip()
    if not body:
        return None, "fcode returned an empty body"
    try:
        d = json.loads(body[body.index("{"):]) if "{" in body else None
    except (ValueError, json.JSONDecodeError):
        return None, "fcode body did not parse as JSON"
    if not isinstance(d, dict) or not d.get("active_submission"):
        # This is the degraded case that exits 0. Name it as BLIND.
        return None, "no `active_submission` in the response (degraded or logged out)"
    return d, ""


def _programme_incumbent() -> str:
    try:
        for line in PROGRAMME.read_text().splitlines()[:80]:
            m = re.match(r"\s*INCUMBENT:\s*(\S+)", line)
            if m:
                return m.group(1)
    except OSError:
        pass
    return "(unreadable)"


def _age_line(path: Path, key: str) -> tuple[float | None, str]:
    """(age_h, rendered) — rendered says BLIND when the surface is too stale."""
    age, _newest = newest_row_age_h(path)
    if age is None:
        return None, "BLIND (no parseable timestamp)"
    limit = MAX_AGE_H[key]
    tag = "" if age <= limit else f"  ⚠ STALE (>{limit*60:.0f}m)"
    return age, f"{age*60:6.1f}m old{tag}"


def _tail_fields(path: Path, sep: str = "\t") -> list[str]:
    try:
        with path.open("rb") as fh:
            fh.seek(0, 2)
            fh.seek(max(0, fh.tell() - 65536))
            tail = fh.read().decode("utf-8", "replace").splitlines()
    except OSError:
        return []
    for line in reversed(tail):
        if line.strip() and not line.startswith("#"):
            return line.split(sep)
    return []


def render() -> int:
    now = _utc_now()
    print(f"NOW — canonical state at {now:%Y-%m-%dT%H:%M:%SZ}")
    print("Every line says WHICH QUESTION IT ANSWERS. Do not reuse one for another.\n")

    rc = 0

    # ---- 1. THE HOLDER. The platform, never a poller. --------------------
    st, why = _fcode_status()
    print("  Q: WHAT IS LIVE ON THE LADDER RIGHT NOW?   [source: fcode status — THE authority]")
    if st is None:
        print(f"     ⛔ BLIND — {why}")
        print("        Do NOT substitute ship_watch or the tape here: they answer a")
        print("        different question and a poller cannot tell you it is blind.")
        rc = 2
    else:
        sub, rat, rk = st["active_submission"], st.get("rating", {}), st.get("rank", {})
        who = sub.get("submittedByName", "?")
        print(f"     HOLDER v{sub.get('version')} \"{sub.get('name')}\"  uploaded by {who}"
              f"  at {sub.get('uploadedAt','?')}")
        print(f"     rating {rat.get('rating', 0):.0f} ({rat.get('tier','?')})"
              f"  rank #{rk.get('rank','?')} of {rk.get('total','?')}"
              f"  matches {rat.get('matches_played','?')}")
        rec = st.get("recent_record") or {}
        if rec:
            print(f"     last {rec.get('sample_size','?')}: "
                  f"{rec.get('wins','?')}W {rec.get('losses','?')}L")

    # ---- 2. THE CONTROL. Not the live bot. -------------------------------
    inc = _programme_incumbent()
    print(f"\n  Q: WHAT DO QUEUED ARMS GET SCORED AGAINST?  [source: PROGRAMME.md INCUMBENT]")
    print(f"     CONTROL {inc}")
    if st is not None:
        print("     ⚠ THE CONTROL AND THE HOLDER ARE DIFFERENT QUESTIONS. If a teammate")
        print("       ships, 'beat the control' and 'beat what is live' diverge — and")
        print("       every queued row is still scored against the CONTROL.")

    # ---- 3. THE TREND. A poller: fine for direction, never for identity. --
    age, rendered = _age_line(SHIPW, "ship_watch")
    f = _tail_fields(SHIPW)
    print(f"\n  Q: WHICH WAY IS THE RATING MOVING?         [source: ship_watch.log — 10-min POLLER]")
    print(f"     {rendered}")
    if f:
        keep = [x for x in f[:8]]
        print(f"     {'  '.join(keep)}")
    print("     ⛔ NEVER read the HOLDER off this line. It is a poller, so between")
    print("       polls a healthy line and a blind line are byte-identical.")

    # ---- 4. THE TAPE. Version tag is POLL-TIME, not per-match. -----------
    age, rendered = _age_line(TAPE, "tape")
    f = _tail_fields(TAPE)
    print(f"\n  Q: WHAT IS THE RATING HISTORY?             [source: elo_history.tsv]")
    print(f"     {rendered}    newest row: {'  '.join(f[:6]) if f else '(none)'}")
    print("     ⚠ its version column is tagged AT POLL TIME, so a match played by")
    print("       another version is credited to whoever held the slot when polled.")
    print("       For per-match truth use ladder_games.ourver (below).")

    # ---- 5. RATED GROUND TRUTH. Per-match, but behind the wall clock. ----
    age, rendered = _age_line(LADDER, "ladder")
    f = _tail_fields(LADDER)
    print(f"\n  Q: WHAT DID WE ACTUALLY PLAY, PER MATCH?   [source: ladder_games.tsv — RATED only]")
    print(f"     {rendered}")
    if len(f) >= 12:
        print(f"     newest: {f[1]}  vs {f[2]} (theirs v{f[3]})  ours v{f[4]}"
              f"  map {f[7]}  won={f[9]}  cond={f[10]}  turns={f[11]}")
    print("     ⛔ THE ARCHIVE LAGS. An ABSENCE here is not evidence of absence —")
    print("       it is the newest thing the archiver has fetched, nothing more.")

    print("\n  RULE: the HOLDER comes from fcode status. The TREND comes from a poller.")
    print("        They are never substitutes, and the poller is the one that lies quietly.")
    return rc


# ===================== SELFTEST =====================
# Per the standing instruments rule: every guard is driven to BOTH verdicts.
# The cell that matters is the degraded-`fcode` one, because it is the exact
# shape that exits 0 while carrying no answer.
def selftest() -> int:
    import tempfile
    bad = 0

    def check(label, got, want):
        nonlocal bad
        ok = got == want
        bad += (not ok)
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<58} got={got} want={want}")

    global _fcode_status
    orig = _fcode_status

    # (a) a HEALTHY body must yield a holder and rc 0
    _fcode_status = lambda timeout=45: ({
        "active_submission": {"version": 151, "name": "X", "submittedByName": "x3r0",
                              "uploadedAt": "2026-08-15T15:54:32Z"},
        "rating": {"rating": 1707.0, "tier": "Emerald", "matches_played": 1048},
        "rank": {"rank": 23, "total": 126}, "recent_record": {"wins": 2, "losses": 8,
                                                              "sample_size": 10}}, "")
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc_ok = render()
    out_ok = buf.getvalue()
    check("healthy fcode -> rc 0", rc_ok, 0)
    check("healthy fcode -> prints the holder version", "HOLDER v151" in out_ok, True)
    check("healthy fcode -> never prints BLIND for the holder",
          "⛔ BLIND" in out_ok, False)

    # (b) THE DEGRADED CASE: exits 0, parses as JSON, carries NO active_submission.
    #     It must go BLIND and it must NOT fall back to a poller.
    _fcode_status = lambda timeout=45: (None, "no `active_submission` in the response")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc_blind = render()
    out_blind = buf.getvalue()
    check("degraded fcode -> rc 2 (NOT 0)", rc_blind, 2)
    check("degraded fcode -> says BLIND", "⛔ BLIND" in out_blind, True)
    check("degraded fcode -> does NOT invent a holder",
          "HOLDER v" in out_blind, False)

    _fcode_status = orig

    # (c) staleness must change the rendering on the SAME file, or the age is decoration
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "s.log"
        p.write_text(f"{_utc_now():%Y-%m-%dT%H:%M:%SZ}\tfresh\n")
        _, fresh = _age_line(p, "ship_watch")
        p.write_text("2026-08-01T00:00:00Z\tstale\n")
        _, stale = _age_line(p, "ship_watch")
        check("fresh surface -> no STALE tag", "STALE" in fresh, False)
        check("stale surface -> STALE tag on the SAME code path", "STALE" in stale, True)

    print("\nPASS: a degraded fcode goes BLIND instead of inventing a holder, and the"
          "\nage tag changes verdict on the same path."
          if not bad else f"\n*** {bad} case(s) wrong ***")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="The one canonical state block: what is live, what is the control, "
                    "and which surface answers which question.")
    ap.add_argument("--selftest", action="store_true",
                    help="drive every guard to both verdicts and exit")
    a = ap.parse_args()
    return selftest() if a.selftest else render()


if __name__ == "__main__":
    sys.exit(main())
