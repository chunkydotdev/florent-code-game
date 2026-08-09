# The look-ahead bias is removable: `ratingBefore` is the at-match rating

**Research arm, session 21, 2026-08-09 ~05:5x CEST.** Live at time of writing:
**v87 "Eir 9c hivethaw"** (`bots/_v100hf`, md5 `9e85cae5`, submission `ecb88707`,
activated 03:48:58Z), ladder **1523.998226 @ 481, rank #36/113**. Corpus: 300
completed ladder matches, `2026-08-07T01:54Z .. 2026-08-09T03:45Z`, pulled from
`fcode match list --mine --type ladder --limit 100 --json` × 3 pages.
**ZERO replay downloads. Free metadata only.**

This document **corrects `instrument-audit-bands-2026-08-09.md` §1**, which is
mine, and suspends its §3.

---

## 1. What I got wrong

`instrument-audit-bands` §1 established that `teamARating`/`teamBRating` is a
live join — one value per team regardless of when the match was played — and
concluded:

> *"A field that records at-match rating could not be constant there."*

That sentence is true and I then treated it as proof that **no such field
exists**. It does. `ratingABefore` / `ratingBBefore` sit in the same
`match list --json` row, and they are the at-match ratings for **both** teams.

We had already been using `ratingBefore` for **our own** rating-chain
reconciliation — `elo-weighted-battery-2026-08-08.md` (zero-mismatch chain
across 354 consecutive matches) and `v80-production-read-2026-08-08.md` (11/11
exact transitions). **Nobody turned it around onto the opponent's side of the
row.** The fix was in hand for a day while both arms worked around the bias by
freezing cohorts by name.

## 2. The decisive test

Same 300 rows. Count distinct values per team for each field:

```
team                  n    distinct teamXRating   distinct ratingXBefore   before range
OpenSverige (us)    300            1 (1524)                243             1521 .. 1625
Lunds Stallions      29            1                        29             1504 .. 1637
Ouroboros            23            1                        23             1555 .. 1620
Team 48              22            1                        22             1538 .. 1647
Powerpuff Girls      22            1                        20             1534 .. 1607
Leviathan            17            1                        17             1494 .. 1686
Kings College Mun.   19            1                        18             1540 .. 1633
Memtrace             16            1                        16             1503 .. 1574
Orizon               11            1                        11             1457 .. 1538
```

`teamXRating` is constant per team. `ratingXBefore` moves essentially every row
and spans **133–192 Elo** for the teams we play most. It is known before the
match resolves, so classifying on it carries **no look-ahead**.

**Misclassification rate of the biased field at the 1550 line: 84/300 = 28.0%.**

## 3. The strength split survives — and is cleaner unbiased

Match-level win rate, all 300 matches, all our versions:

```
   thr |         AT-MATCH (unbiased)          |          CURRENT (biased)
       |   nS   winS    nW   winW      gap    |   nS   winS    nW   winW      gap
  1500 |  283  48.1%    17  82.4%   +34.3%    |  275  48.0%    25  72.0%   +24.0%
  1525 |  244  45.1%    56  71.4%   +26.3%    |  245  45.3%    55  70.9%   +25.6%
  1550 |  194  40.2%   106  67.9%   +27.7%    |  212  40.6%    88  72.7%   +32.2%
  1575 |  147  34.0%   153  65.4%   +31.3%    |  143  49.7%   157  50.3%    +0.7%
  1600 |   90  41.1%   210  53.8%   +12.7%    |  102  59.8%   198  44.9%   -14.9%
```

**Unbiased:** the gap is **+26 to +34pp and stable across 1500–1575**, and the
strong-band win rate falls monotonically 48.1 → 45.1 → 40.2 → 34.0%. That is
what a real strength gradient looks like.

**Biased:** the gap **collapses to +0.7pp at 1575 and inverts to −14.9pp at
1600** — i.e. it reports that we beat the strongest teams 59.8% of the time.
The high-threshold instability we have been treating as a genuine robustness
limit on this finding is a bias artifact.

**The central finding of the project gets STRONGER, not weaker.** "We farm weak
opposition and are dismantled by strong opposition" holds at n=300 with an
unbiased classifier, gap ≈ +28pp at the 1550 line.

### Suspended, not refuted

`instrument-audit-bands` §3's threshold table (the "SURVIVES" verdict) used the
biased field. It is **game-level** and this table is **match-level**, so it is
not directly contradicted — but its robustness claim is **unverified until
re-run on `ratingBefore`**. Treat it as suspended. Same for the 500-game cut in
`kill-game-split-2026-08-08.md`: the win-rate half almost certainly survives
(§3 above), the kill-game half needs recomputing.

## 4. What gets weaker: the prospective confirmation

The v80 window's cohorts were frozen **by name** at n=6 — the workaround this
document makes unnecessary. Re-scoring v80's second life with at-match rating:

```
                 at-match UNBIASED (thr 1550)      name-frozen (s20 wrap)
WINDOW       STRONG n=12  -0.53  W 5/12 41.7%     STRONG n=10  -11.98
             WEAK   n= 8 +22.91  W 5/8  62.5%     WEAK   n= 9  +32.84
POST-WINDOW  STRONG n= 5 -47.25  W 0/5   0.0%     STRONG n= 7  -70.13
             WEAK   n=15  +3.52  W 8/15 53.3%     WEAK   n= 8  +21.52
FULL LIFE-2  STRONG n=17 -47.78  W 5/17 29.4%
             WEAK   n=23 +26.43  W 13/23 56.5%
```

**Direction survives everywhere. Magnitude in the window does not** — STRONG net
goes −11.98 → −0.53, essentially flat. The window's entire edge was the WEAK
cohort. **The prospective result is a direction confirmation, not a magnitude
one, and the name-freeze inflated it.**

### Why the name-freeze inflates: the Lunds case

Four v80 matches, one opponent name, both bands:

```
#3  21:35Z  Lunds v44  4-1  +11.95   oppBefore 1599.7   STRONG
#16 23:46Z  Lunds v44  2-3   -3.63   oppBefore 1547.5   weak
#24 01:08Z  Lunds v44  1-4  -12.02   oppBefore 1504.4   weak
#36 03:07Z  Lunds v44  1-4  -10.86   oppBefore 1514.3   weak
```

A name-freeze books all four to STRONG — Lunds' current rating is 1557.9 and
they read as a top team. Three were played against a **1504–1548** Lunds.
**That is not losing to strong opposition; it is losing to a mid-table opponent,
mislabelled**, and the loss is then charged to the STRONG cohort. Lunds held
v44 throughout, so this is pure rating drift, not an opponent ship.

## 5. Standing guidance

1. **Classify opponents by `ratingBefore`, never by `teamXRating`.** The latter
   is only valid for "how strong is this team right now".
2. **A team name is not a strength band.** Names drift across the line within a
   single night; `Lunds Stallions` spans 1504–1637 in our own corpus.
3. **Fix the threshold before the window opens, not after.** `ratingBefore`
   removes the look-ahead but re-introduces one degree of freedom (where the
   line goes). Pre-register the number; do not sweep it and then report the
   best cut.
4. `tools/ladder_census.py:16` reads `teamARating`/`teamBRating`. Any strength
   banding it produces inherits the bias. It has **not** been changed by this
   document — bots and tools are not the research arm's to edit.

## 6. Provenance

- All figures: `fcode match list --mine --type ladder --json`, 3 paginated
  pages, 300 complete matches. No `match info` calls, no replay downloads.
- Rating chain verified contiguous over v80's second life (39/39 transitions
  exact), so the corpus has no gaps in that range.
- Live version at time of writing v87 `ecb88707`; the corpus predates it and
  contains **zero** v87 matches. Nothing here is a read on the live slot.
