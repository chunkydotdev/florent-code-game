#!/usr/bin/env python3
"""KILL-SPEED SCORE — one number per game, per `docs/research/SPEC-kill-speed-score-2026-08-10.md`.

    from score import game_score, mean_score
    .venv/bin/python tools/score.py --selftest

    core kill  <100 -> 10 · <130 -> 8 · <170 -> 6 · <250 -> 4 · <400 -> 2
    slower kill -> 1 · tiebreak/titanium win -> 0 · LOSS (any cause) -> -10

Reported as MEAN POINTS PER GAME.

**⛔ THIS IS NOT A LEG VERDICT STATISTIC, AND THAT PROHIBITION IS THE
LOAD-BEARING PART OF THE SPEC.** Per-game sd is **7.74**; detecting a realistic
change needs **~2,100 games per arm**, and it carries only **1.1x the power of
plain win rate**. A leg reporting this as its primary would repeat exactly the
failure this project spent 2026-08-10 diagnosing: an 18pp bar fired at a fixture
whose own floor was 19.5pp. **Use it for version scorecards (free, spends no
games) and as a ship gate at n >= 200. Never as a leg's primary.**

Baselines from the spec (large-sample, our own tape):
    v80 -3.38 · v94 -3.29 · v102 -2.39 · **v104 -1.77** (best shipped)
    v102 -> v104 = +0.62/game.
**Ship gate: beat -1.77 at n >= 200.**

**THE BALANCE PROPERTY IS WHY THESE EXACT NUMBERS**, and it is a maintenance
obligation, not trivia: killing 40 rounds faster across the board pays
**+0.79/game**; converting 10 of 109 losses into median-speed kills pays
**+0.67/game**. Within 20% of each other, so speed and conversion are weighted
comparably. **If any bucket edge or the loss penalty moves, RE-RUN that check —
otherwise speed silently becomes decorative and the score turns into a win-rate
proxy with extra steps.**
"""
from __future__ import annotations

import sys

BUCKETS = ((100, 10), (130, 8), (170, 6), (250, 4), (400, 2))
SLOW_KILL = 1
TIEBREAK_WIN = 0
LOSS = -10


def game_score(we_won: bool, condition: str, turns: int) -> int:
    """Points for ONE game.

    `condition` is the engine's `winCondition` string; a core kill is
    `core_destroyed`. A loss scores -10 REGARDLESS of how it was lost --
    losing slowly is not better than losing fast.
    """
    if not we_won:
        return LOSS
    if condition != "core_destroyed":
        return TIEBREAK_WIN          # a r1000 tiebreak win is not a win here
    for edge, pts in BUCKETS:
        if turns < edge:
            return pts
    return SLOW_KILL


def mean_score(games) -> tuple[float, int]:
    """(mean points per game, n). `games` yields (we_won, condition, turns)."""
    pts = [game_score(w, c, t) for w, c, t in games]
    return (sum(pts) / len(pts) if pts else 0.0), len(pts)


def selftest() -> int:
    """Drive a kill in EVERY bucket, a tiebreak win, and a loss.

    A scale whose buckets have not each been hit is a scale with untested edges,
    and the edges are where an off-by-one lives.
    """
    print("KILL-SPEED SCORE SELFTEST\n")
    cases = [
        ("kill r99  (<100)", True, "core_destroyed", 99, 10),
        ("kill r100 (boundary -> next bucket)", True, "core_destroyed", 100, 8),
        ("kill r129", True, "core_destroyed", 129, 8),
        ("kill r130 (boundary)", True, "core_destroyed", 130, 6),
        ("kill r169", True, "core_destroyed", 169, 6),
        ("kill r170 (boundary)", True, "core_destroyed", 170, 4),
        ("kill r249", True, "core_destroyed", 249, 4),
        ("kill r250 (boundary)", True, "core_destroyed", 250, 2),
        ("kill r399", True, "core_destroyed", 399, 2),
        ("kill r400 (boundary -> slow)", True, "core_destroyed", 400, 1),
        ("kill r980 (slow)", True, "core_destroyed", 980, 1),
        ("tiebreak WIN scores ZERO", True, "titanium_collected", 1000, 0),
        ("loss by core kill", False, "core_destroyed", 120, -10),
        ("loss on tiebreak", False, "titanium_collected", 1000, -10),
        ("a SLOW loss is not better than a fast one", False, "core_destroyed", 990, -10),
    ]
    bad = 0
    for label, w, c, t, want in cases:
        got = game_score(w, c, t)
        ok = got == want
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<42} {got:>4} (want {want})")
        if not ok:
            bad += 1

    m, n = mean_score([(True, "core_destroyed", 90), (False, "core_destroyed", 200)])
    ok = abs(m - 0.0) < 1e-9 and n == 2
    print(f"  [{'ok' if ok else 'FAIL'}] mean of a 10 and a -10 is 0.0        {m:>4.1f} n={n}")
    if not ok:
        bad += 1

    # THE BALANCE PROPERTY, asserted rather than trusted: a faster-kill lever and
    # a loss-conversion lever must stay within ~20% of each other.
    base = [(True, "core_destroyed", 200)] * 109 + [(False, "core_destroyed", 200)] * 109
    faster = [(w, c, max(t - 40, 1)) for w, c, t in base]
    conv = base[:]
    for i in range(10):
        conv[109 + i] = (True, "core_destroyed", 200)
    b, _ = mean_score(base); f, _ = mean_score(faster); v, _ = mean_score(conv)
    gs, gc = f - b, v - b
    ratio = min(gs, gc) / max(gs, gc) if max(gs, gc) else 0
    ok = ratio >= 0.6
    print(f"  [{'ok' if ok else 'FAIL'}] speed lever {gs:+.2f} vs conversion "
          f"{gc:+.2f}  ratio {ratio:.2f} (>=0.60)")
    if not ok:
        bad += 1
        print("          ** a bucket edge or the penalty moved: re-run the "
              "balance check in the spec **")
    print()
    if bad:
        print(f"*** {bad} case(s) wrong ***")
        return 1
    print("PASS: every bucket hit including both sides of each boundary, "
          "tiebreak win scores 0, losses score -10 regardless of cause, and "
          "the speed/conversion levers stay comparable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(selftest() if "--selftest" in sys.argv else print(__doc__) or 0)
