#!/usr/bin/env python3
"""Ladder-side SPRT for the slot: a stop-loss with a statable error rate.

WHY. workflow-analysis/v3 measured the fixed-threshold swap rule's residual
defect: re-testing every match with no multiplicity correction drives
P(fire) -> 1 on long tenures regardless of quality. The recalibrated -21
threshold (ship-gate.md amendment 2026-08-09) fixes the operating point, not
the multiplicity. The domain-native fix v3 names is a sequential test with
explicit bounds (fishtest's SPRT); `tools/sprt.py` does it for local legs.
This is the ladder-side version, run over `elo_history.tsv` holder runs.

MODEL. Per-match ladder Elo increment ~ N(mu, sd=9.25) (v3: 302 increments,
mean +0.82, sd 9.25). SPRT between H_bleed: mu = MU0 and H_ok: mu = 0. The
Gaussian log-likelihood ratio is linear in the increments, so only the
holder's cumulative (net, k) matter:

    LLR_ok_over_bleed = (0 - MU0)/sd^2 * (net - k * MU0/2)

LLR <= -log((1-beta)/alpha)  -> accept BLEEDING (slot free)
LLR >= +log((1-beta)/alpha)  -> accept OK (test terminates; holder cleared)

Because the statistic is a function of (net, k) only, spreading a multi-match
tape gap evenly across its matches is EXACT for the test (v3's variance
caveat applies to estimating sd, which we do not do here — sd is fixed at
the measured 9.25).

USAGE
    .venv/bin/python tools/slot_sprt.py --backtest          # all holder runs
    .venv/bin/python tools/slot_sprt.py --backtest --grid   # calibration grid
    .venv/bin/python tools/slot_sprt.py --check NET K       # one live readout

STATUS: ADVISORY. The slot RULE is net5 <= -21 in ship-gate.md +
elo_logger.py, one statement, doc+tool together. This tool must validate
against live tenures before any promotion, which would be its own
doc+tool commit.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SD = 9.25            # per-match Elo increment sd (v3, 302 increments)
MU0 = -10.0          # H_bleed: bleeding rate in Elo/match (v3's suggested bound)
ALPHA = 0.15         # = beta; log((1-b)/a) bound. 0.15 chosen by backtest —
                     # 0.05 misses the v79 true positive (see --grid).

# ===== THE SLOW BOUND (Magnus, 2026-08-09 s26 — "go with your recommended
# Path", the PAIR, added as a second bound and NOT a replacement) =====
#
# WHY A SECOND BOUND EXISTS. MU0 = -10 answers "is this collapsing?" and is
# blind to a slow bleed. Measured: the -21 rolling-5 rule trips only at
# <= -4.2 Elo/match (5r <= -21), and this SPRT at MU0 = -10 needs worse than
# -5/match, so a STEADY -4.0/match decline trips NOTHING, EVER — 240 Elo over
# 60 matches, silent on every instrument we own. That hole was found the day a
# "recovery" was reported off net5 improving while the rating fell: net5 is a
# five-match SLOPE and it RELAXES as a bad result ages out of the window.
#
# WHY -4 RATHER THAN A TIGHTER -10. Tightening MU0 makes this test fire LESS,
# not more — MU0 enters the statistic itself (llr ∝ net - k*MU0/2), not just
# the bound. Backtested over all 47 holder runs on the tape:
#
#     MU0    BLEED on real history                     slow bleed   v79 collapse
#     -10    8  incl. v53(net +43), v94(net +13)       missed       CAUGHT
#      -6    6  incl. v53(+43), v72(+16), v91(+3)      -4 only      CAUGHT
#      -4    0                                          CAUGHT      missed
#
# So the two are COMPLEMENTARY, NOT ORDERED: -10 catches the sharp short
# collapse and misses the slow bleed; -4 does the reverse and costs ZERO false
# positives on our entire recorded history. Hence both, reported separately.
# Note in passing that the live -10 setting fires on four holders that ended
# NET POSITIVE (v53 at +43 over 45 matches) — that is on the record as a
# suspected false-positive rate, not silently accepted.
MU0_SLOW = -4.0

BOUNDS = (("fast", MU0), ("slow", MU0_SLOW))


def run_both(rows, alpha: float = ALPHA):
    """Both bounds over the same holder run. Returns {name: verdict}.

    Reported SEPARATELY and never merged into one word: they answer different
    questions, and collapsing them would hide which one fired."""
    return {name: run_sprt(rows, mu0, alpha)[0] for name, mu0 in BOUNDS}


def llr(net: float, k: int, mu0: float = MU0) -> float:
    return (0.0 - mu0) / (SD * SD) * (net - k * mu0 / 2.0)


def bound(alpha: float = ALPHA) -> float:
    return math.log((1.0 - alpha) / alpha)


def holder_runs():
    """Yield (ver, rows) where rows = [(ts, rating, matches), ...] for each
    maximal consecutive same-version span of the tape."""
    runs, cur_ver, cur = [], None, []
    for line in (ROOT / "elo_history.tsv").read_text().splitlines()[1:]:
        p = line.split("\t")
        if len(p) < 4 or not p[2].isdigit():
            continue
        ts, rating, matches, ver = p[0], float(p[1]), int(p[2]), p[3]
        if ver != cur_ver:
            if cur:
                runs.append((cur_ver, cur))
            cur_ver, cur = ver, []
        cur.append((ts, rating, matches))
    if cur:
        runs.append((cur_ver, cur))
    return runs


def run_sprt(rows, mu0: float, alpha: float):
    """Walk one holder run with RESTART-ON-OK: each OK acceptance clears the
    holder *so far* and restarts the test from that row, so a holder that
    degrades later is still caught (v56 cleared at k=3 then bled -38 — the
    no-restart design misses it). Composite false-positive rate grows ~alpha
    per completed segment — statable, unlike per-poll re-testing.

    Returns (verdict, events, k_total, net_total) where events is a list of
    (kind, k_into_run, net_of_segment); verdict = 'BLEED' if any segment
    accepted bleed, else 'OK' if any cleared, else 'open'."""
    b = bound(alpha)
    _, r0, m0 = rows[0]
    seg_r, seg_m = r0, m0
    events = []
    fired = False
    for ts, rating, matches in rows[1:]:
        k, net = matches - seg_m, rating - seg_r
        if k <= 0 or fired:
            continue
        s = llr(net, k, mu0)
        if s <= -b:
            events.append(("BLEED", matches - m0, net))
            fired = True          # advisory latches; holder change resets
        elif s >= b:
            events.append(("OK", matches - m0, net))
            seg_r, seg_m = rating, matches
    kt, nt = rows[-1][2] - m0, rows[-1][1] - r0
    verdict = ("BLEED" if fired
               else "OK" if events else "open")
    return verdict, events, kt, nt


def backtest(mu0: float, alpha: float, verbose: bool = True):
    fired = cleared = openn = 0
    for ver, rows in holder_runs():
        v, events, kt, nt = run_sprt(rows, mu0, alpha)
        if kt < 1:
            continue
        fired += v == "BLEED"
        cleared += v == "OK"
        openn += v == "open"
        if verbose and kt >= 3:
            ev = "  ".join(f"{kind}@k={k}(net{net:+.0f})" for kind, k, net in events)
            print(f"  {rows[0][0][:16]}  {ver:<8} k={kt:<3} net={nt:+5.0f}  {v:<5} {ev}")
    return fired, cleared, openn


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backtest", action="store_true")
    ap.add_argument("--grid", action="store_true")
    ap.add_argument("--check", nargs=2, type=float, metavar=("NET", "K"))
    ap.add_argument("--mu0", type=float, default=MU0)
    ap.add_argument("--alpha", type=float, default=ALPHA)
    a = ap.parse_args()

    if a.check:
        net, k = a.check
        s = llr(net, int(k), a.mu0)
        b = bound(a.alpha)
        state = "BLEED (slot free)" if s <= -b else "OK (cleared)" if s >= b else "open"
        print(f"llr {s:+.3f} vs ±{b:.3f} -> {state}   (net {net:+.0f} over {int(k)} matches)")
        return 0

    if a.grid:
        print("calibration grid (fired/cleared/open across all holder runs):")
        for mu0 in (-6.0, -8.0, -10.0):
            for alpha in (0.05, 0.10, 0.15, 0.20):
                f, c, o = backtest(mu0, alpha, verbose=False)
                print(f"  mu0={mu0:+.0f} alpha={alpha:.2f}  BLEED={f:<3} OK={c:<3} open={o}")
        return 0

    if a.backtest:
        print(f"backtest: mu0={a.mu0} alpha={a.alpha} bound=±{bound(a.alpha):.3f} sd={SD}")
        f, c, o = backtest(a.mu0, a.alpha)
        print(f"totals: BLEED={f} OK={c} open={o}")
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
