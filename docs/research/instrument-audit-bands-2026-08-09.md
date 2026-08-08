# Instrument audit: the strong/weak split has look-ahead bias, and the locked bands sit on a fault line

**Research arm, session 20, 2026-08-09 00:1x CEST.** Live **v80 "Eir 9b"**
(`bots/_v89sh`), ladder 1579 @ 447 rank #28. Queue item 2 (instrument audit
sweep). **Zero downloads.** Audits my *own* central finding from
`kill-game-split-2026-08-08.md`, which the builder has locked as the scoring
bands for its v86 pre-registration.

---

## 1. `teamARating` / `teamBRating` is CURRENT rating, not rating at match time

Tested by asking whether a team's rating ever varies across matches played at
different times:

```
team                     matches   distinct ratings
OpenSverige                  100          1  (1573)
Lunds Stallions               10          1  (1619)
Kings College Munich           9          1  (1648)
Ouroboros                      8          1  (1569)
... 15 of 16 teams with >=3 matches: a SINGLE distinct rating
```

**The decisive case is our own.** Our rating is a single value, 1573, across all
100 cached matches — over a window in which we are *known* to have moved from
1593 down to 1537.7 and back to 1579. A field that records at-match rating could
not be constant there.

So the API reports a *live* rating on every historical match row. Classifying
500 historical games by it asks "how strong is this opponent **now**", not "how
strong were they **when we played**". For a question about historical
performance that is **look-ahead bias**.

## 2. Half the corpus is within one night's drift of the boundary

```
games within +/-60 Elo of the 1550 line:  255/500 = 51% of the corpus
```

For scale: **our own rating moved 41 points in 7 matches tonight.** A 60-point
band is well inside normal overnight drift, so the band membership of half the
corpus is not stable.

## 3. What survives the audit, and what does not

Recomputing the headline at every plausible threshold:

```
threshold   n strong   win%   killgame    n weak   win%   killgame
    1500        490   48.4%     44.1%         10   60.0%    66.7%
    1525        400   42.0%     37.3%        100   75.0%    72.0%
    1550        350   38.9%     33.1%        150   71.3%    68.7%
    1575        275   39.3%     34.6%        225   60.0%    59.4%
    1600        240   39.6%     35.0%        260   56.9%    56.7%
```

**SURVIVES — the strong-band result.** 42.0 / 38.9 / 39.3 / 39.6% across
1525–1600, kill-game 33–37%. "We win roughly 39–40% against strong opposition,
and about a third of our kill games" is robust to where the line is drawn.

**DOES NOT SURVIVE — the weak-band result and therefore the contrast.** The weak
band slides **75.0% → 71.3% → 60.0% → 56.9%** across the same thresholds, an
18-point swing driven purely by threshold choice. The headline contrast
(38.9 vs 71.3) is the most favourable framing available, not a stable fact.
**Quote the strong band; treat the weak band as threshold-dependent.**

## 4. The specific hazard in the locked bands

The two largest opponents nearest the line pull in **opposite** directions:

```
Ouroboros         1569   (+19 from the line)   n=40   our win 12%
OopsGotYourElo    1557   ( +7 from the line)   n=35   our win 66%
```

**75 games sit within 20 Elo of the boundary, and their win rates differ by 54
points.** If Ouroboros drifts below 1550 the weak band acquires 40 games at 12%
and collapses; if OopsGotYourElo drifts below, it gains 35 games at 66% and
inflates. Either move is a normal night's drift, and they move independently.

That is the worst available configuration for a threshold instrument, and the
pre-registration is currently scored on it.

## 5. Recommendation

**Score the pre-registration on opponent IDENTITY, not on a rating threshold.**
The builder already did this instinctively for the v86 rollback — the
load-bearing table there was per-opponent (Askar +9.05→−6.01, Leviathan, KCM,
Ouroboros), not band-based, and that table is unaffected by everything above.
Identity is stable; the threshold is not.

Concretely: name the weak cohort as a fixed list of teams (Askar City, Team 48,
Memtrace, Leviathan, opensverige - plan B) and the strong cohort likewise,
fixed at registration time. Then drift cannot silently re-score the prediction.

**This does not overturn the finding that our performance is
strength-conditional** — the strong band is robust, and the per-opponent
kill-game records (Ouroboros 2/22, KCM 7/33, Lunds 11/41 against Askar 20/25,
Banminary 18/24) are identity-based and carry the same conclusion without any
threshold at all.

## 6. Also audited this tick — no finding

- **`tools/ceiling.py`**: clean after the 2026-08-08 fix. `kill_rate` is
  unconditioned, `censored_median` is correct, and `kills_only_median` is
  explicitly labelled a collider in-code. **`conversion` (kills/wins) does
  condition on winning**, so its denominator is a different population of games
  for bots with different win rates. I simulated it looking for an inversion and
  **did not find one** — the effect is attenuation, not sign reversal, and in the
  builder's v76-vs-v84 comparison the bias runs *against* v76, which still won on
  the metric. **The builder's conclusion is conservative, not overstated.**
  Recommendation is only: report `kill_rate` as primary (which the tool's own
  comments already say), and never let `conversion` be a leg's verdict metric.
- I set out to find a second collider in `ceiling.py` and did not. Recording the
  null so the next sweep does not re-run it.
