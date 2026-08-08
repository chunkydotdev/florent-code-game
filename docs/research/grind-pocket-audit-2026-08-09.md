# The 58% grind edge: unbiased as a number, unsupported as an argument

**Research arm, session 20, 2026-08-09 01:3x CEST.** Live **v80 "Eir 9b"**,
window n=6/20. Queue item 2, continued. **Zero downloads.**

Audits **my own claim** — the one the builder called "the correction that
changes a decision" and put in the HANDOVER top block:

> "Grind games are 29% of our games, net +24 (85W/61L, 58.2%), the only
> population where we are above water. So 'raise core-kill rate' is NOT
> unconditionally good: pushed naively it trades away our one profitable
> regime."

The builder flagged `pair.py`'s r1000-conditioned line as smelling like the
turns-to-kill collider. It led here.

---

## 1. The statistic is NOT a collider

Conditioning on reaching r1000 conditions on neither side having closed, which
is a selected subpopulation. But selection alone does not bias the *conditional
win rate*. Simulated across lethality levels with a **true tiebreak edge fixed at
58% by construction**:

```
our lethality   overall win   kill rate   r1000 share   win IN r1000
      0.20          46.0%       19.9%        45.0%         58.0%
      0.30          50.4%       30.1%        34.9%         58.1%
      0.40          54.5%       40.0%        25.0%         57.8%
      0.50          58.8%       50.1%        14.9%         58.1%
      0.60          62.9%       60.1%         5.0%         57.5%
```

The measured value tracks the truth at every lethality. **`pair.py`'s r1000 line
is clean and so is our 58.2%.** Recording that so the sweep is not re-run.

## 2. But the argument built on it does not follow

The claim is not "we win 58% of grinds" (true) — it is "**therefore** losing
grinds is a cost". That requires knowing what a marginal grind game *would
otherwise have been*, and the 58% cannot see it. Two regimes, identical
tiebreak edge:

```
REGIME A — pushing is SAFE (a marginal grind would have been a kill-WIN)
                    kill rate   r1000   win in r1000   OVERALL
  grind-steered         20.1%   45.1%          57.9%     46.1%
  baseline              39.8%   25.1%          58.1%     54.4%
  close-steered         59.9%    5.0%          57.8%     62.8%
        -> closing wins. Protecting the grind pocket COSTS us.

REGIME B — pushing is RISKY (60% of pushed games backfire into losses)
  grind-steered          8.0%   44.9%          57.9%     34.0%
  baseline              15.9%   25.1%          58.0%     30.5%
  close-steered         23.9%    5.0%          58.5%     26.8%
        -> grinding wins. Protecting the pocket is CORRECT.
```

**The 58% is identical in both regimes and in every single row.** It cannot
distinguish them. The deciding quantity is the **backfire rate** — how often
pressing for a kill converts a game we would have drawn out into one we lose —
and **no instrument this project owns has ever measured it.**

**So my claim was not wrong; it was unsupported.** It silently assumed Regime B.
A reader could equally have assumed Regime A and reached the opposite decision
from the same number. That is the defect, and it sat in the top block.

## 3. Which regime our data actually points to

Scored on the builder's **frozen named roster**, not a drifting threshold:

```
cohort            n     KILL-GAME win      GRIND win        gap
STRONG (named)  340     36.6% (n=254)     50.0% (n=86)    +13.4%
WEAK   (named)  155     65.6% (n=96)      71.2% (n=59)     +5.6%
ALL             495     44.6% (n=350)     58.6% (n=145)   +14.0%
```

**In every cohort our grind win rate exceeds our kill-game win rate**, and the
gap is widest exactly where it matters — +13.4 points against strong opposition.
That is suggestive evidence for **Regime B**, which is the regime my original
claim assumed.

**It is not proof.** These are two conditional populations compared to each
other, not a marginal counterfactual; steering changes which games land in which
bucket, and none of these numbers can see that. But it is the best available
evidence and it does not favour the alternative.

## 4. This may be the mechanism behind the local/ladder split

The builder's batteries said the lethal lineage (v76/v86) beats the grindy one
decisively — Regime A. The ladder said v86 lost. **Backfire rate is a candidate
reconciliation: it should scale with opponent strength.** Against `kladde_probe`
and `ouroboros_probe`, which we beat 87–93%, nothing punishes an over-push, so
pushing looks free. Against KCM and Ouroboros it is not free — and those are the
two opponents that killed v86.

That is a sharper version of the builder's (c) reading: **local arena fails for
magnitude against a dominated pool specifically because the dominated pool has
a near-zero backfire rate.**

## 5. The measurement that would settle it

**An arena leg with a lethality dial, scored on OVERALL WIN RATE, against
opponents that can punish** — not conversion, not r1000 share, not grind win
rate, all of which are flat across both regimes above. Overall win rate is the
only column in the tables that separates them.

The opponent pool is the load-bearing part: run it against a dominated probe and
it will report Regime A no matter which regime is true.

## 6. Caveats

- Sections 1–2 are simulations, not measurements. They establish what a
  statistic *can* support, not what is true here.
- Section 3's cohorts are the builder's frozen roster as of 2026-08-09 00:2x;
  the counts differ slightly from earlier threshold-based figures for that
  reason, and 5 of 500 games fall off-roster and are excluded.
- "Backfire rate" is my coinage for this document; it is not an established
  project term and nothing currently measures it.
