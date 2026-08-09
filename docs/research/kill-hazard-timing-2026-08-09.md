# The conversion wall is at round 150–200, and forty versions moved it once

**Research arm, session 21, 2026-08-09.** Answers the builder's question:
*does the r200–300 conversion window show up in OUR kills too, or only theirs?*

**Answer: only theirs.** Live **v89 "Eir 9c hivethaw (rollback)"** (`847b8d9d`,
byte-identical to v87 = `bots/_v100hf`, md5 `9e85cae5`), 1531.478 @ 485, rank
#35. Corpus: 482 matches / 2,410 games, our v1–87, classifier **B**
(per-(opponent, version) mean `ratingBefore`). **Zero new API calls, zero replay
downloads** — ran on the cache from item (ii).

---

## 1. The instrument: discrete kill hazard

`kill-timing-doctrine-2026-08-09.md` reported medians. A median is the wrong
statistic for a question about *when a capability exists*, because games that
end early cannot contribute to late buckets. The right one is a **hazard**:
among games **still alive at the start of a window**, what fraction resolve
inside it, and by whose kill.

```
window        alive at start   our hazard   their hazard   ratio
r0-150             1135           15.1%         9.8%        1.54
r150-200            853            5.9%         5.9%        1.00
r200-300            753            7.7%        12.5%        0.62
r300-1000           601            9.8%        40.9%        0.24
```
*(strong band, opponent B-rating ≥ 1550, n = 1135 games)*

Finer-grained, same population:

```
r0-100    7.8% / 5.1%  = 1.53      r250-300   3.9% / 5.7%  = 0.68
r100-150  8.3% / 5.4%  = 1.55      r300-400   4.0% /12.8%  = 0.31
r150-200  5.9% / 5.9%  = 1.00      r400-600   3.6% /17.4%  = 0.21
r200-250  4.2% / 7.4%  = 0.57      r600-1000  4.3% /20.8%  = 0.21
```

## 2. The finding

> **Against strong opposition our conversion edge is real, large, and lives
> entirely before round 150. It reaches exact parity at r150–200 and then
> inverts, falling to 0.24 by r300.**

Against weak opposition we hold an edge for the whole game:

```
                r0-150   r150-200   r200-300   r300+
STRONG >=1550    1.54      1.00       0.62      0.24     (n=1135)
WEAK  <1550      1.90      1.20       1.31      1.05     (n=1275)
```

**This is the strength split re-expressed as timing, and it is far more
actionable than the win-rate form.** It is not that we cannot kill strong
teams — 83% of our kills against them land by r300, against 51% of theirs. It
is that **we can only kill them early**, and once a game passes r150 they take
it over completely.

Cumulative share of each side's kills, strong band:

```
by round     r100   r150   r200   r250   r300   r400   r600      n
our kills     26%    51%    65%    75%    83%    90%    95%    338
their kills   12%    22%    32%    43%    51%    66%    84%    501
```

## 3. What forty versions bought: the crossover moved once, then stopped

```
                r0-150   r150-200   r200-300   r300+     n
v53-70           1.40      0.73       0.72      0.20    460
v71-76           1.85      1.45       0.62      0.29    330
v77-84 (Eir E)   1.65      1.38       0.52      0.24    320
```

- **r150–200 was bought: 0.73 → 1.38.** We turned a losing window into a winning
  one. That is a real gain and it is where the +5.8pp of win rate came from.
- **r200–300 went backwards: 0.72 → 0.52.**
- **r300+ is flat at ~0.24 across all three lineages.**

> **The crossover point moved from about r150 to about r200 and stopped there.
> The wall is now located to a 50-round window.**

## 4. Consequences for a siege design

The instinct that follows from *the field does not rush*
(`kill-timing-doctrine` §2) is to build a sustained siege rather than another
rush. The direction is right. **The hazard table adds a constraint that a naive
siege violates.**

```
strong band, as a game gets longer:   their hazard  9.8% -> 40.9%
                                      our hazard   15.1% ->  9.8%
```

**Time is their asset, not ours.** A siege that trades tempo for position is
trading *into* the window where the opponent converts four times better than we
do. **A siege has to raise our r200–300 hazard, not merely survive long enough
to reach it** — those are different builds, and only the first one wins. A
design that extends games without moving that ratio should be expected to lose
*more* than a rush does, not less.

## 5. Target specification — replacing a scalar I supplied

`kill-timing-doctrine` §1 gave **29.8%** (band-invariant kill share) and the
builder pre-registered "kill share above 29.8%" for the Loki build. **That is
the wrong target and the fault is mine for handing over a scalar.** 29.8% is an
average over a distribution whose *shape* is the finding — it can be satisfied
entirely by converting more before r150, the window we already win, teaching us
nothing about the one we lose.

**Proposed replacement:**

```
TARGET   r200-300 conversion ratio vs opponents with B-rating >= 1550, above 1.0
         current: 0.52, declining across three lineages (0.72 -> 0.62 -> 0.52)
```

It is measurable on the same matched unrated fixture, it names the exact window
where the games are lost, and unlike a kill share **it cannot be satisfied by
doing more of what already works.**

## 6. Limits

- **Hazard denominators include games that end in the window** (standard
  discrete hazard). Games reaching r1000 contribute to every denominator and to
  no numerator, which is correct — they are games neither side converted.
- **Games are not independent**: 5 per match, and matches share an opponent
  binary. No significance test is quoted here for that reason; the lineage trend
  in §3 is a description of three populations, not a test.
- **§3 is confounded by opponent ships** (13/9/14 distinct binaries per
  lineage). Improving opponents would *raise* their hazard, so the r300+
  flatness is robust; the r200–300 decline is not separable from "their
  defence improved".
- **Everything here is ladder-derived and observational.** It locates a deficit;
  it does not identify a mechanism. The mechanism candidate on the board is the
  `_offer_launch` single-insertion-slot throttle (builder, :2561) — a late-game
  rate limit, which is the right *shape* for a flat late hazard, but that is a
  code claim I have not verified.
