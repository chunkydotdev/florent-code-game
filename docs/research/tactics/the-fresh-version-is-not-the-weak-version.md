---
tactic: targeting a rival's freshly-shipped, "un-debugged" version
source: tools/corpus/version_drift.py over corpus/league_matches.tsv (35,642 league matches, 2026-08-01..2026-08-11)
origin: measured in-repo (research arm, sweep 22, 2026-08-11)
evidence: documented
transfers: no
---

**⛔ D12 RELABEL (side-lane flag, 2026-08-11, adopted): this road is at the BOTTOM OF THE QUEUE, NOT CLOSED.** The finding rests on archive statistics with a BEHAVIOURAL premise — how opponents' versions perform — which is exactly the evidence class D12 forbids retiring a road with, and **no leg has ever been aimed at a freshly-shipped version or an excursion window.** The statistics stand; the claim they support is *"unpromising, queue it last"*, not *"closed"*. D12's own remedy: archive evidence sends a road to the bottom of the queue, never off it.
WHAT IT IS — The intuitive offensive read on opponent non-stationarity: a rival who has
just shipped is running code that has had less testing than the version it replaced, so
the window right after their deploy is the moment to attack them. **Measured league-wide,
this is false in the mean and it is the sweep's cleanest measured negative.**

Fresh versions are, if anything, **stronger** than the shipper's own average. Outcome is
`eloDelta`, which is already opponent-strength-adjusted; teams are demeaned against their
own overall rate:

| version age | n | demeaned eloDelta | t | SD |
|---|---|---|---|---|
| first match on a new version | 2,807 | **+0.182** | +1.07 (null) | **9.030** |
| matches 2–3 | 3,847 | +0.462 | +3.22 | 8.887 |
| matches 4–6 | 4,017 | +0.358 | +2.63 | 8.645 |
| matches 7–11 | 4,918 | +0.351 | +2.88 | 8.543 |
| matches 12+ | 55,581 | −0.098 | −2.86 | 8.084 |

**THE NAIVE CHANGEPOINT TEST NEARLY PRODUCED A FALSE FINDING IN THE OPPOSITE DIRECTION,
and the reason is the same selection trap this whole sweep is about.** Teams ship
*precisely when they are losing*: the pre-ship 5-match window averages **−0.625** eloDelta
against a control window's +0.260. So the raw post-ship gain (+1.25/match) is mostly
regression to the mean. Matching each real changepoint to a same-team non-changepoint with
an equal pre-window (real −0.378 vs control −0.375) leaves a **difference-in-differences of
+0.524 ± 0.107, t = +4.89 — still positive.** A ship makes a team better, not worse.

The honest reading is not "shipping is magic": it is that **the newest version of an
active team is on average their best version so far.** That is progress, and it is the
same fact as the −8.0pp in `block-on-opponent-version-not-opponent-id.md` seen from the
other side.

**THE ONE THING THAT IS TRUE ABOUT A FRESH VERSION IS VARIANCE, NOT MEAN.** The SD column
above falls monotonically with version age — 9.030 on the first match down to 8.084 at
12+. There *is* an "un-debugged" signature and it is dispersion. Caveat that must travel
with it: these buckets pool across opponents, so the SD is not opponent-matched and part
of the spread is rating-gap variety rather than erratic play.

WHY IT MIGHT TRANSFER — it does not, and that is the point of filing it. The road is
closed in the direction everyone would try first. Two further reasons it stays closed
even if the mean had gone the other way:
* **We cannot choose our rated pairings.** Ladder matches are paired on the platform's
  clock, not by us. Knowing a rival is in a fragile window buys nothing on the rated
  ladder, where the rating actually moves.
* **In unrated legs the effect is worse than useless**: an opponent on a fresh version is
  a **noisier measuring instrument** (SD 9.03 vs 8.08) with **no compensating weakness in
  the mean**. If anything this argues for selecting cells whose opponent version has
  already been stable for a while — more games on the version we will face, and less
  dispersion per game.

WHAT WOULD KILL IT — i.e. what would reopen the road: a cut restricted to the *first
match* on a new version shows +0.182 at t = +1.07, which is a genuine null rather than a
measured positive. If someone can isolate a sub-population where the first-match effect
IS negative — say, only versions that are themselves rolled back within the hour (the
prototype excursions in `the-rollback-signature-marks-a-rivals-prototype-window.md`) —
that is a different and untested question. This file refutes the general claim, not that
one. Note also that everything here is **league-wide third-party** behaviour, which is
the right population and not an echo loop, but it is 10 days of one league.

BUILDER HOOK — none, and deliberately so. **Do not spend a leg on "attack them right
after they ship".** The reusable half is the instrument: `tools/corpus/version_drift.py`
section 3 re-runs this in seconds, and the matched-control pattern in it (match on the
pre-window before comparing post-windows) is the fix for any future cut where the subject
chose its own treatment time.
