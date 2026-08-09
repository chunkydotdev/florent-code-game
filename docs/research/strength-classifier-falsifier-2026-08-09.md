# The strength classifier, falsified within-opponent and rebuilt between-opponent

**Research arm, session 21, 2026-08-09.** Commissioned by the builder as item
(i) — a gate on the strong-cohort mechanism read. Live **v87 "Eir 9c hivethaw"**
(`ecb88707`, `bots/_v100hf`, md5 `9e85cae5`), activated 03:48:58Z.

Corpus: **482 complete ladder matches**, our v1–87,
`2026-08-05T19:46Z .. 2026-08-09T03:58Z`, from `fcode match list --mine --type
ladder --json` (8 paginated pages). **Zero replay downloads.**

The builder's question, verbatim:

> *Does opponent `ratingBefore` predict our match result at all, once opponent
> VERSION is held fixed?*

**Answer: no, not in the current era.** The classifier survives anyway, for a
reason that was not obvious before the test. And the test turned up a larger
confound aimed at the live v87 window.

---

## 1. A prior trap: `eloDelta` is not a performance statistic

Before any of the below, conditioning on outcome so the result cannot be a
win/loss composition effect:

```
our WINS only    n=252   corr(oppBefore, eloDelta) = +0.298   t=+4.9
our LOSSES only  n=230   corr(oppBefore, eloDelta) = +0.088   t=+1.3
```

Beating a higher-rated opponent pays more Elo, by construction. **Every
"net Elo per band" figure this project has quoted is part performance, part Elo
formula** — including `STRONG −70.13`, and including figures in my own prior
documents. It does not overturn any verdict, but net-Elo-per-band should stop
being described as a performance measurement.

**Everything below uses score margin (our games − their games, −5..+5) and win
rate.** Neither is mechanically coupled to opponent rating.

## 2. The falsifier: within a fixed opponent binary, opponent rating predicts nothing

Design: group matches into cells of **(opponent name, opponent version)** — a
fixed opponent *binary*. Demean the outcome and every regressor inside its cell
(fixed effects), then pool. Cells with n ≥ 5. Outcome = score margin.

```
                                          oppBefore effect       our-ratingBefore
FULL corpus (our v1-87)   raw              -1.58/100Elo t=-3.07
                          + time control   -0.95/100Elo t=-1.55
RECENT (our v>=53)        raw              -0.56/100Elo t=-0.94
                          + our rating+time +0.39/100Elo t=+0.52
TIGHT  (our v>=70)        raw              -0.02/100Elo t=-0.03
                          + our rating+time +1.04/100Elo t=+1.11   ub -4.97 t=-2.95
```

**The full-corpus effect is an early-era artifact.** It dies under a time
control and is entirely gone by our v53. In the tight era the point estimate is
zero, and adding controls flips its sign.

The builder's motivating observation replicates: within **Lunds Stallions v44**
— identical bytes across a 123-Elo swing — `corr(oppBefore, margin) = +0.299`,
the *wrong* sign. Within **CtrlAltDefeat v117**, +0.778. Within **Kings College
Munich v8**, −0.813. These are n = 6–14 cells scattering around zero, which is
what no-signal looks like.

**Conclusion: for a static opponent, at-match rating variation is ladder noise
about that opponent, not information about the match.** Classifying an
individual match by it adds noise.

## 3. The split survives, because it was never a within-opponent effect

Variance decomposition of `oppBefore`, era our v ≥ 53, n = 330:

```
BETWEEN opponent binaries   84.1%
WITHIN  binary (drift/noise) 15.9%
```

Only 16% of the spread is the noise §2 identifies. And the headline is
insensitive to which classifier carries it — same corpus, threshold 1550:

```
A. at-match ratingBefore (per match)        nS=209 winS=40.7% | nW=121 winW=68.6% | gap +27.9% z=+4.89
B. mean ratingBefore per (opponent, VERSION) nS=225 winS=41.8% | nW=105 winW=70.5% | gap +28.7% z=+4.86
C. mean ratingBefore per opponent NAME       nS=242 winS=42.6% | nW= 88 winW=73.9% | gap +31.3% z=+5.03
```

Threshold sensitivity, gap in win rate (weak − strong):

```
   thr    A at-match   B per-binary   C per-name
  1500       +35.3%         +25.3%       +50.3%
  1525       +26.7%         +29.9%       +27.5%
  1550       +27.9%         +28.7%       +31.3%
  1575       +31.5%         +31.1%       +27.9%
  1600       +13.6%          +4.9%        +6.1%
```

**The strength split is a between-opponent effect — which is what "strong
opponents beat us" means.** It is not noise wearing a rating label. z ≈ 4.9
under every classifier.

**Self-correction to `at-match-rating-2026-08-09.md` §3:** I claimed at-match is
"cleaner at high thresholds". It beats *current-rating* there, but not the other
unbiased classifiers — at 1600 **all three weaken** (+13.6 / +4.9 / +6.1). The
1600 band is thin, not clean.

## 4. Recommended classifier: B, per-(opponent, version) mean

B keeps the 84% that is between-opponent signal and discards the 16% that §2
shows is noise. Unlike C it still tracks opponent **ships** — Lunds v41 and v44
are different binaries, KCM v1 and v8 likewise — which is the whole reason a
name is a bad label.

**The live case that forced the issue.** v87's first match landed during this
analysis:

```
v87 #1  2026-08-09T03:58:30.114Z  vs Leviathan v35  1-4  delta -8.4049
        oppBefore = 1549.9973548107455    ->  0.0026 Elo BELOW the 1550 line
```

The first application of the pre-registered classifier is a coin-flip on the
third decimal.

```
                        Leviathan v35        knife-edge exposure (<5 Elo from line)
A at-match     1549.9974  WEAK by 0.003      25/330 = 7.6% of matches
B per-binary   1543.0     WEAK by 7.0        20/330 = 6.1%
C per-name     1590.8     STRONG by 40.8      4/330 = 1.2%
```

Whichever classifier is kept, **the tie rule must be stated explicitly and now**
— match #1 needs it.

## 5. The confound this test turned up, aimed at the live v87 window

Within a fixed opponent binary, **our own** `ratingBefore` predicts our margin
far more strongly than the opponent's does: **−4.97 margin per 100 Elo,
t = −2.95** (tight era, with time control). Within-cell sd of our own rating is
16.9 Elo, so **+1sd above our recent mean costs ≈ 0.84 games of margin out of 5,
against identical opponent code.**

Direct, without cells:

```
corr(our ratingBefore − era mean, next margin)    our v>=53: -0.224  t=-4.16  n=330
                                                  our v>=70: -0.166  t=-2.25  n=181
```

Empirically, by distance of our rating from the era mean (our v ≥ 70):

```
  vs era mean     n    mean eloDelta    mean margin
      -40        20        +2.26           +0.60
      -20        38        -0.37           -0.16
       +0        50        +0.90           +0.36
      +20        46        -1.99           -0.65
      +40        24        -2.08           -1.08
```

**Our era mean is 1580.1. The v87 window is pre-registered from 1523.998 —
56.2 Elo below it, the most favourable starting point in the corpus.** The table
puts that at roughly **+2 Elo/match, ≈ +40 Elo over an n=20 window, from
regression alone.**

### Mechanism is ambiguous and is not being claimed

Two candidates fit and this data cannot separate them:

- **(a) mean reversion** in a noisy Elo — high readings are partly luck, luck
  does not persist;
- **(b) rating lag** — our rating trails real changes in our bot, so a high
  reading is a stale one.

The within-cell design rules out **matchmaking** (same opponent, same opponent
code), and a time control does not kill the effect. That is as far as the
evidence goes.

**The operational consequence is identical under either mechanism: a window's
starting baseline is not neutral, and the v87 window's baseline is stacked in
its favour.** This is not an argument against running the window. It is an
argument for pre-registering the right null — *"v87 beats +40 over n=20"* is a
much weaker claim than *"v87 is positive over n=20"*, and only the first one is
evidence about the hive fix.

## 6. Standing guidance

1. **Never report net-Elo-per-band as performance.** Use win rate or score
   margin. (§1)
2. **Classify opponents by per-(name, version) mean `ratingBefore`**, not by the
   match's own value and not by name. (§2–§4)
3. **State the tie rule when a threshold is pre-registered.** 7.6% of matches
   fall within 5 Elo of the 1550 line under at-match classification. (§4)
4. **Record where a window's baseline sits relative to the era mean, at
   pre-registration time.** A depressed baseline inflates the window and a
   raised one deflates it, by roughly 2 Elo/match per 40 Elo of deviation in
   this era. (§5)
5. `tools/ladder_census.py:16` still reads the live-join `teamARating`. Not
   changed here — tools are not the research arm's to edit.
