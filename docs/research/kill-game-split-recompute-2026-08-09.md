# Kill-game split, recomputed unbiased — and why the original is not reproducible

**Research arm, session 21, 2026-08-09.** Builder item (ii). Live **v87 "Eir 9c
hivethaw"** (`ecb88707`, md5 `9e85cae5`). Audits
`kill-game-split-2026-08-08.md`, which is mine.

**Corpus: 482 complete ladder matches / 2,410 games**, our v1–87, pulled with
482 paced `fcode match info --json` calls (482/482 clean, ~0.15s pacing).
**ZERO replay downloads.** Cache: `scratchpad/matchinfo.jsonl`.

Run under **three** classifiers so the choice is visible rather than assumed:

| | classifier | status |
|---|---|---|
| **X** | `teamARating`/`teamBRating` — current rating, live join | what the original doc used |
| **A** | `ratingBefore` at the match | unbiased, per-match |
| **B** | mean `ratingBefore` per (opponent name, opponent **version**) | recommended — see `strength-classifier-falsifier-2026-08-09.md` |

> ## CORRECTION, 2026-08-09 (same session, before anything was built on this)
>
> **The column labelled B in this document is actually C (per-name).**
> `fcode match info --json` returns the opponent's version as `null` — a trap
> already recorded in HANDOVER's tooling section — so every key built from that
> payload was `(opponent, None)`. I argued for B over C and then computed C
> under B's label.
>
> Rebuilt with the version joined from `match list` (482/482 non-null, 132
> binaries vs 52 names). **The conclusions below are unaffected; the numbers
> move by under 1pp:**
>
> ```
> same 500 games, thr 1550        STRONG    WEAK     kill-game win% S/W
> B per-(opp,VERSION) [true]       44.6%   66.7%       40.9% / 62.3%
> C per-name  [printed below as B] 45.4%   66.7%       41.9% / 61.4%
> ```
>
> Corrected standing figures: split **~45% / ~67%**, kill-game mixture
> **~41% / ~62%**. Full detail in `kill-timing-doctrine-2026-08-09.md` §0.
>
> **§4's "non-monotone at the top" caveat also has a cause now**: with the
> correct join the 1650+ cell is 120 games / 24 matches / 8 binaries, and
> **Banminary v41 alone carries the apparent advantage** — drop it and the cell
> reads 44.3%. See `kill-timing-doctrine-2026-08-09.md` §4.

---

## 1. The headline is not the bias. It is that the original cannot be reproduced.

I reconstructed the original doc's exact corpus — the 100 matches preceding
`ourBefore ≈ 1593 @ 429`, our v72–83, `2026-08-08T02:37Z .. 19:04Z`. The
reconstruction is confirmed by an independent quantity the classifier cannot
touch:

```
                        this recompute      original doc
our WINS / LOSSES          243 / 257          243 / 257     <- exact
kill-decided games            365                354
we won of those          164 = 44.9%        158 = 44.6%
grind (r1000) share          27.0%              29%
our win% in the grind    79/135 = 58.5%    85/146 = 58.2%
```

Same games. Now run the doc's **own field, X**, on them today:

```
band          this recompute (X, today)      as the doc reported it
1650+         n= 75   35% win                n= 70   36% win
1550-1649     n=320   52% win                n=280   40% win
<1550         n=105   47% win                n=150   71% win
STRONG>=1550  n=395   49.1%                  n=350   38.9%
WEAK  <1550   n=105   46.7%                  n=150   71.3%
```

**The doc's central result does not come back — with the doc's own field, on the
doc's own games.** X gives STRONG 49.1% / WEAK 46.7% today, a gap of **−2.4pp**,
where the doc reported **+32.4pp**.

Nothing was mis-run. `teamXRating` is a **live join**: it returns each team's
rating *as of the moment you ask*. The doc was computed against a snapshot of
current ratings from 2026-08-08 22:3x that no longer exists, and 45 games
changed band between then and now.

> **A live-join classifier does not merely bias a result. It makes the result
> irreproducible.** A successor re-running it gets different numbers and has no
> way to tell whether the original was wrong or the field moved underneath it.
> This is a stronger reason to abandon `teamXRating` than the look-ahead bias
> already recorded in `at-match-rating-2026-08-09.md`.

## 2. The split survives unbiased, with a materially narrower spread

Same 500 games, threshold 1550:

```
classifier                 band       n     win%    kill-game win%   r1000 share
X current (doc's field)  STRONG     395    49.1%        44.4%           30.4%
                         WEAK       105    46.7%        46.7%           14.3%
A at-match               STRONG     385    42.9%        39.8%           26.2%
                         WEAK       115    67.8%        63.0%           29.6%
B per-binary mean        STRONG     425    45.4%        41.9%           27.5%
                         WEAK        75    66.7%        61.4%           24.0%
```

**The finding is real and the doc's direction was right. Its magnitude was
inflated.**

```
                     STRONG    WEAK     gap
doc (X, snapshot)     38.9%   71.3%   +32.4pp
A at-match            42.9%   67.8%   +24.9pp
B per-binary          45.4%   66.7%   +21.3pp   <- the number to carry
```

**The correct standing figure is ~45% vs ~67%, a gap near +21pp — not +32pp.**

### On the full corpus (2,410 games) the same pattern holds

```
              STRONG                        WEAK
B  n=1150  43.0% win, 40.4% in kill    n=1260  58.5% win, 59.0% in kill
A  n=1060  42.8% win, 40.2% in kill    n=1350  57.6% win, 57.8% in kill
X  n=1300  49.1% win, 46.5% in kill    n=1110  53.4% win, 51.0% in kill
```

Restricted to our v ≥ 53 (n=1,650 games), the biased field flattens the split
almost to nothing — **STRONG 49.2% / WEAK 51.2%, a 2.0pp gap, versus 43.4% /
63.0% (19.6pp) under B.** The instrument was hiding the finding in the recent
era and inflating it in the older window. It is wrong in both directions,
which is what an unreliable classifier looks like.

## 3. The doc's two corrections to the s19 wrap — one survives narrowed, one survives intact

**(a) "The 44% core-kill rate is a mixture, 69% weak / 33% strong." SURVIVES,
NARROWED.** The 44% is confirmed independently (164/365 = 44.9% here vs 158/354
= 44.6% in the doc — this quantity does not depend on the classifier). The
mixture is real but tighter:

```
kill-game win%      doc (X)    A at-match    B per-binary
STRONG                33%         39.8%         41.9%
WEAK                  69%         63.0%         61.4%
```

The doc's conclusion stands as written — *there is no single 44% to optimise,
there are two regimes* — but the regimes are **42% and 61%**, not 33% and 69%.

**(b) "The top band resolves before the grind, so the tiebreak edge cannot be
spent against them." SURVIVES INTACT.** r1000 share by band, unbiased:

```
band          A at-match   B per-binary      (doc: 13% / 36% / 23%)
1650+            14%           13%
1550-1649        27%           29%
<1550            30%           24%
```

The 1650+ band resolves before the grind at 13–14% under both unbiased
classifiers — the doc said 13%. **This is the doc's best-supported claim and it
needed no correction.**

**The grind pocket itself is untouched:** 58.5% here vs 58.2% in the doc. It
never depended on the classifier. The standing caveat from
`grind-pocket-audit-2026-08-09.md` — *the 58.2% is unbiased but "therefore
losing a grind is a cost" is unsupported* — is unaffected by anything here.

## 4. One thing that got worse, not better

Under both unbiased classifiers the win-rate ordering is **not monotone at the
top**:

```
              1650+    1550-1649    <1550
A at-match     46%        43%        68%      (n=35 / 350 / 115)
B per-binary   40%        46%        67%      (n=30 / 395 /  75)
```

The 1650+ cell is 30–35 games and sits above or level with the band below it.
**Do not read a gradient into the top band from this corpus** — it is thin, and
this is the same thinness that collapses the 1600 threshold in
`strength-classifier-falsifier-2026-08-09.md` §3. The defensible statement is
binary — *at or above ~1550 we win ~45%, below it ~67%* — not a monotone ladder
of difficulty.

## 5. Standing consequences

1. **`teamARating`/`teamBRating` must not be used for any historical
   classification, ever.** Not for bias — for reproducibility. Results computed
   on it cannot be recovered later. `tools/ladder_census.py:16` still reads it
   (not changed here; tools are not the research arm's to edit).
2. **Carry ~45% / ~67%, gap ~+21pp** as the strength split, not 38.9% / 71.3%.
3. **Carry 42% / 61%** as the kill-game mixture, not 33% / 69%.
4. The r1000-share claim and the 58.2% grind figure need no revision.
5. Any figure quoted from `kill-game-split-2026-08-08.md` that is not in this
   list should be re-derived before use — the whole §3 table was built on X.
