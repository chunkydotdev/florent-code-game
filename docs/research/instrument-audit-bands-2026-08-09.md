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

---

# ADDENDUM (01:1x) — the drift is no longer hypothetical. It already happened.

Section 4 named two opponents as the specific hazard: Ouroboros and
OopsGotYourElo, sitting within 20 Elo of the line. I then compared the ratings in
my two API pulls of the same night — **22:25 and 00:05, 100 minutes apart** —
against the same 500 games.

```
team                    22:25    00:05   drift   band change
Askar City               1510     1552     +41   *** WEAK  -> STRONG
Focalground              1698     1730     +32
The Bisons               1495     1527     +32
Banminary                1646     1623     -24
Lunds Stallions          1619     1600     -19
Powerpuff Girls          1593     1612     +19
OopsGotYourElo           1557     1544     -14   *** STRONG -> WEAK
Kings College Munich     1648     1637     -11
```

**Two teams crossed the 1550 line in 100 minutes, in opposite directions** — and
one of them (OopsGotYourElo) is a team this document had already flagged by name
as the hazard. The other, Askar City, is the largest single contributor to the
weak cohort (n=30, 83% win) and is the team the builder's whole pre-registration
was framed around as "the weak farm".

## The same 500 games, scored 100 minutes apart

```
ratings as of 22:25   STRONG n=350 win 38.9% killgame 33.1%   WEAK n=150 win 71.3% killgame 68.7%
ratings as of 00:05   STRONG n=345 win 40.0% killgame 36.8%   WEAK n=155 win 67.7% killgame 65.6%
```

**No new games were played. The headline moved 1.1pp on the strong side and
3.6pp on the weak side purely from opponents' ratings drifting.**

The shift is modest rather than catastrophic only because Askar (30 games,
crossing up) and OopsGotYourElo (35 games, crossing down) partly cancel. That
cancellation is luck, not a property of the instrument.

**This converts section 4 from a warning into a measurement**, and it retro-
justifies the builder's amendment: freezing cohorts by name at n=6 stops exactly
this. Their frozen roster reproduces the 1550 rule against the *00:05* ratings
(all 19 teams agree), so it froze the post-drift state cleanly.

# ADDENDUM 2 (01:1x) — a correction to the v86 window on the tape

Reconstructed both windows from `eloDelta` keyed on version, newest-first:

```
=== v86: n=5  net -27.20 ===
   20:27:06  Leviathan               +0.87   running   +0.87
   20:36:32  Askar City              -6.01   running   -5.14
   20:47:25  Kings College Munich   -13.76   running  -18.90
   20:56:32  Ouroboros              -15.95   running  -34.85   <- the tape's number
   21:05:47  Banminary               +7.65   running  -27.20   <- and then this landed
```

**The tape carries v86 as n=4, net −34.85. The complete window is n=5, net
−27.20.** The fifth match (Banminary, +7.65, v86's best result) completed at
21:05:47, twelve minutes before v80's first re-activation match at 21:17:58 —
so it belongs to the v86 window.

−34.85 is exactly the running total after four matches. The rollback was decided
on a window that had one more result in it.

**What this does and does not change.** It does not reverse the rollback: the
builder stated explicitly that it rolled back on cost ("bleeding ~9/match")
and on the opponent-controlled table (worse on all four), *not* on the trigger
settling anything. Both of those still hold. **But the tape's magnitude figure
is wrong, and the claim that the swap-rule threshold "tripped" needs
recomputing at m=5 against −27.20** — a smaller magnitude against a threshold
that grows with m. Whether it still trips is the builder's to determine; the
rule is theirs.

**The v80 window, by contrast, checks out exactly.** The builder's n=6 / +33.54
is correct, and my "n=7, 13 to go" was wrong: v80 has two separate lives
(17:18–17:35 at −8.82, then 21:17 onward at +33.54), and only the re-activation
era counts. Their "a version label is not a window" is right and is the same
defect class as this queue's rule 6.
