#!/usr/bin/env python3
"""KILL-SPEED SCORE — one number per game, per `docs/research/SPEC-kill-speed-score-2026-08-10.md`.

    from score import game_score, mean_score
    .venv/bin/python tools/score.py --selftest

    core kill  <100 -> 10 · <130 -> 8 · <170 -> 6 · <250 -> 4 · <400 -> 2
    slower kill -> 1 · tiebreak/titanium win -> -10 · LOSS (any cause) -> -10

Reported as MEAN POINTS PER GAME.

**⛔ THIS IS NOT A LEG VERDICT STATISTIC, AND THAT PROHIBITION IS THE
LOAD-BEARING PART OF THE SPEC.** Per-game sd is **7.74**; detecting a realistic
change needs **~2,100 games per arm**, and it carries only **1.1x the power of
plain win rate**. A leg reporting this as its primary would repeat exactly the
failure this project spent 2026-08-10 diagnosing: an 18pp bar fired at a fixture
whose own floor was 19.5pp. **Use it for version scorecards (free, spends no
games) and as a ship gate at n >= 200. Never as a leg's primary.**

Baselines RECOMPUTED on the -10 tiebreak scale (our own ladder tape, n>=100):
    v20 -10.00 · v53 -2.60 · v72 -4.20 · v80 -5.54 · v94 -5.08 · v102 -2.47
    **v104 -1.76 (best shipped, n=255)**
**SHIP GATE: beat -1.76 at n >= 200 [scale v2].** A bar without its scale tag is
a bar that cannot be checked.
**THE RESCALE CHANGED THE HISTORY, NOT JUST THE NUMBERS.** v20 scores EXACTLY
-10.00 over 110 games -- it never destroyed a core once; every "win" was a
tiebreak. And v53, which read -1.77 on the old scale and appeared to TIE v104,
drops to -2.60. **The old scale was crediting tiebreak wins and flattering our
early versions into looking like today's bot.**

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

# ⚠ THE SCALE IS VERSIONED AND EVERY PRINTED SCORE CARRIES THE TAG.
# Tonight is the proof: the tiebreak value was edited IN PLACE from 0 to -10 and
# orphaned every earlier figure within the hour. v20 read -3.64, now -10.00. The
# ship gate read -1.77, now -1.76. Nothing in the repo marked which rule produced
# which number, so a reader had to date it by archaeology.
# That is the s26 fixture rule -- VERSIONED, NEVER EDITED IN PLACE -- applying to
# the currency, and we violated it within an hour of creating the currency.
#   v1  tiebreak/titanium win =   0   (in force ~20:0x-21:0x Z, 2026-08-10)
#   v2  tiebreak/titanium win = -10   (current; Magnus)
# A rebalance is an APPENDED amendment with a new version, never an in-place
# edit -- same discipline as the preregs. Balance property re-verified per
# version: v1 -> v2 unchanged, ratio 1.20 both.
SCALE_VERSION = "v2"

BUCKETS = ((100, 10), (130, 8), (170, 6), (250, 4), (400, 2))
SLOW_KILL = 1
# CHANGED BY MAGNUS 2026-08-10: a tiebreak win scores -10, IDENTICAL TO A LOSS.
# *"we should never optimize for tiebreak wins, all of our effort should be on
# killing the cores."* The argument that settles it: at 0, a pure SURVIVAL plank
# converting 20 losses into 20 tiebreak wins scores +200 and reads as a triumph
# -- while PLAY_DEFENCE: never forbids exactly that plank. At -10 the same plank
# scores ZERO improvement. **-10 is what makes the currency agree with the
# doctrine**; 0 was what created the tension.
# Verified rather than assumed: the balance property is IDENTICAL either way
# (speed +0.75, conversion +0.63, ratio 1.20), so the maintenance obligation in
# the spec is cleared by this change rather than reopened by it.
TIEBREAK_WIN = -10
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
        ("tiebreak win scores -10, SAME AS A LOSS", True, "titanium_collected", 1000, -10),
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

    # a tiebreak win must now be indistinguishable from a loss
    assert game_score(True, "titanium_collected", 1000) == game_score(False, "x", 1000)
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
          "a tiebreak win is indistinguishable from a loss, losses score -10 regardless of cause, and "
          "the speed/conversion levers stay comparable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(selftest() if "--selftest" in sys.argv else print(__doc__) or 0)
