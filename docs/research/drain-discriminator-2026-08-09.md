# Drain-pump discriminator: REFUTED — the surviving effect is our own pipeline uptime (side lane deliverable)

**Side research lane, 2026-08-09. Closes the bait-siting family (multistep
P-B / atlas drain gate). 598 games vs the 7 atlas-confirmed building-shooters;
reconciliation rx_shot vs rx_tgt 1,066/1,066. Commissioned by the research arm
before any build — their production-not-persistence check, second save today.**


**Read-only research arm, 2026-08-09.** Commissioned before a build decision.
Corpus: 2,735 attributed replays -> **598 games vs the 7 atlas-confirmed
building-shooters** in which exactly one side is us (OpenSverige / "opensverige
- plan B"), the game ran >= 50 rounds, and the opponent fired >= 20 shots.

## Verdicts up front

| cut | verdict |
| --- | --- |
| **CUT 1 — absorbed-share vs outcome, within shooting-level strata** | **positive but NOT diagnostic.** +0.20 win rate [+0.13, +0.26], survives every control. The same instrument scores *empty*-share at **-0.26** and *core*-share at **-0.18**, so what it measures is "our material was standing in their firing lines", not "their ammo was wasted". |
| **CUT 2 — the economy channel** | **NULL, and well-powered.** Their ti_coll/round moves **-0.21 Ti/rd [-1.04, +0.65]** on a base of 9.56 — the data exclude any drain bigger than ~11% of their income. Their ammo tax is flat (p=0.65). They do **not** shoot more per round when we offer more absorbable surface (p=0.25). |
| **Build-relevant sub-cut (added)** | at fixed absorbed volume, **cheapness of the absorber does not pay** (+0.016 [-0.035, +0.072], p=0.68); **keeping the absorber healed does** (+0.070 [+0.011, +0.127], p=0.045). |

**Net: the drain-pump story as stated is refuted. The correlate it rests on is
real, but it lives entirely on OUR side of the ledger.**

## Provenance and schema

* Attribution: `attrib2.tsv` (teamA == replay team 0, atlas-reconciled 495/495)
  x `games.tsv` (winner, rounds) x `corpus/league_matches.tsv` (pre-match rating).
* Shots: `rx/rx_shot.tsv` — per (file, shooter team, shooter kind), the class of
  tile each `fireTurret` `to` landed on. Total shots = sum over all classes.
* **Healed-absorber flag: AVAILABLE and USED.** `rx/rx_tgt.tsv` carries
  `nshots_healed` per target building (shots falling within +/-2 rounds of a heal
  on that tile). The **primary treatment is `abs_nch` = healed non-core-building
  shots / their total shots**, exactly the variable guard (iii) asked for. The
  coarser `abs_nc` is reported alongside and behaves the same.
* Reconciliation: `rx_shot` non-core totals vs `rx_tgt` non-core totals agree in
  **1,066 of 1,066** rows. 0 dropped.
* Economy: `tl.tsv` -> max `ti_coll` per (file, team) (the column is a per-round
  snapshot that reads 0 in rounds with no `updatePlayers`, so max, not last).
* Ammo ledger: 4 Ti/gunner shot, 10 Ti/sentinel shot, 0 for launchers.
* Trap 5 honoured: shot counts come from `rx_shot`, never `econ.tsv`.

## The field, before any cut

| opponent | n | our win | their shots/rd | abs_nc | **abs_nch** | abs_cheap | cheap share of absorbers | healed share of absorbers |
|---|---|---|---|---|---|---|---|---|
| Ouroboros | 85 | 0.153 | 1.00 | 0.392 | 0.200 | 0.330 | 0.820 | 0.416 |
| Powerpuff Girls | 80 | 0.362 | 0.64 | 0.425 | 0.248 | 0.324 | 0.707 | 0.491 |
| OopsGotYourElo | 66 | 0.591 | 0.41 | 0.389 | 0.258 | 0.218 | 0.442 | 0.519 |
| Leviathan | 82 | 0.549 | 0.54 | 0.356 | 0.181 | 0.133 | 0.341 | 0.393 |
| Lunds Stallions | 115 | 0.287 | 0.87 | 0.233 | 0.107 | 0.152 | 0.574 | 0.368 |
| Kings College Munich | 95 | 0.253 | 0.66 | 0.265 | 0.152 | 0.172 | 0.539 | 0.451 |
| CtrlAltDefeat | 75 | 0.333 | 0.61 | 0.250 | 0.144 | 0.159 | 0.586 | 0.423 |
| **all** | **598** | **0.348** | 0.67 | 0.313 | 0.174 | 0.204 | 0.577 | 0.427 |

### The confound that had to be killed first

`abs_nch` correlates **+0.377** with game length (within-opponent median +0.372),
and `abs_nc` correlates **-0.463** with the share of their fire that reached our
core. Absorbed-share is partly just *"we did not die early"* — 288 of 598 games
end with our core destroyed. Every headline number below therefore carries a
length control, and the strongest specification (C) throws away every truncated
game.

## CUT 1 — absorbed-share vs our win rate, within shooting-level strata

Strata = **opponent x tercile of their shots/round** (the dominance control),
optionally further split at the stratum median of game length and/or our own
economy. Within each stratum, games split at the stratum median of the treatment.
Pooled by Mantel-Haenszel weights (`n_lo*n_hi/n`); p from 4,000 within-cell
label permutations; CIs from a 1,500-draw within-cell bootstrap.

### A. As commissioned — control = shots/round tercile only

Full per-cell table for the primary treatment (21 cells, n=598):

| opponent | shots/rd tercile | n lo | n hi | treat lo | treat hi | win lo | win hi | **delta** |
|---|---|---|---|---|---|---|---|---|
| Ouroboros | T1 (0.32) | 15 | 14 | 0.056 | 0.213 | 0.200 | 0.429 | +0.229 |
| Ouroboros | T2 (0.86) | 14 | 14 | 0.051 | 0.525 | 0.071 | 0.214 | +0.143 |
| Ouroboros | T3 (1.82) | 14 | 14 | 0.062 | 0.303 | 0.000 | 0.000 | +0.000 |
| Powerpuff Girls | T1 (0.19) | 14 | 14 | 0.096 | 0.362 | 0.357 | 0.857 | +0.500 |
| Powerpuff Girls | T2 (0.53) | 13 | 13 | 0.067 | 0.378 | 0.000 | 0.538 | +0.538 |
| Powerpuff Girls | T3 (1.19) | 13 | 13 | 0.087 | 0.501 | 0.000 | 0.385 | +0.385 |
| OopsGotYourElo | T1 (0.06) | 12 | 11 | 0.074 | 0.412 | 0.667 | 0.818 | +0.152 |
| OopsGotYourElo | T2 (0.31) | 11 | 11 | 0.060 | 0.472 | 0.455 | 0.909 | +0.455 |
| OopsGotYourElo | T3 (0.85) | 11 | 10 | 0.003 | 0.574 | 0.091 | 0.600 | +0.509 |
| Leviathan | T1 (0.24) | 14 | 14 | 0.016 | 0.252 | 0.571 | 0.929 | +0.357 |
| Leviathan | T2 (0.51) | 14 | 13 | 0.063 | 0.532 | 0.357 | 0.538 | +0.181 |
| Leviathan | T3 (0.88) | 14 | 13 | 0.013 | 0.238 | 0.500 | 0.385 | **-0.115** |
| Lunds Stallions | T1 (0.42) | 20 | 19 | 0.016 | 0.255 | 0.550 | 0.579 | +0.029 |
| Lunds Stallions | T2 (0.85) | 19 | 19 | 0.016 | 0.127 | 0.158 | 0.158 | +0.000 |
| Lunds Stallions | T3 (1.34) | 19 | 19 | 0.023 | 0.207 | 0.053 | 0.211 | +0.158 |
| Kings College Munich | T1 (0.29) | 16 | 16 | 0.044 | 0.250 | 0.125 | 0.625 | +0.500 |
| Kings College Munich | T2 (0.65) | 16 | 16 | 0.043 | 0.298 | 0.062 | 0.500 | +0.438 |
| Kings College Munich | T3 (1.04) | 16 | 15 | 0.023 | 0.264 | 0.062 | 0.133 | +0.071 |
| CtrlAltDefeat | T1 (0.24) | 13 | 13 | 0.041 | 0.206 | 0.462 | 0.846 | +0.385 |
| CtrlAltDefeat | T2 (0.57) | 13 | 12 | 0.029 | 0.318 | 0.077 | 0.333 | +0.256 |
| CtrlAltDefeat | T3 (1.02) | 12 | 12 | 0.006 | 0.277 | 0.000 | 0.250 | +0.250 |

**Pooled: +0.245, p < 0.001.** 19 of 21 cells non-negative. Every opponent's
pooled sign is positive.

### The full specification ladder

| # | treatment | strata (opponent x ...) | cells | n | **win delta** | p |
|---|---|---|---|---|---|---|
| A | `abs_nch` | shots/rd | 21 | 598 | **+0.245** | 0.000 |
| A | `abs_nc` | shots/rd | 21 | 598 | +0.231 | 0.000 |
| A | `abs_cheaph` | shots/rd | 21 | 598 | +0.153 | 0.000 |
| A | `abs_cheap` | shots/rd | 21 | 598 | +0.171 | 0.000 |
| B | `abs_nch` | shots/rd, **length** | 36 | 598 | **+0.199** [+0.134, +0.259] | 0.000 |
| B | `abs_nc` | shots/rd, length | 36 | 598 | +0.179 | 0.000 |
| B | `abs_cheaph` | shots/rd, length | 36 | 598 | +0.139 | 0.000 |
| B | `abs_cheap` | shots/rd, length | 36 | 598 | +0.146 | 0.000 |
| C | `abs_nch` | shots/rd, **r=1000 games only** | 20 | 221 | +0.193 | 0.003 |
| C | `abs_cheap` | shots/rd, r=1000 only | 20 | 221 | +0.247 | 0.000 |
| D | `abs_nchx` (core shots out of the denominator) | shots/rd, length | 36 | 598 | +0.159 | 0.000 |
| F | `abs_nch` | shots/rd, **OUR ti/rd** | 42 | 598 | +0.153 | 0.000 |
| F | `abs_nch` | shots/rd, **OUR builds/rd** | 42 | 598 | +0.170 | 0.000 |
| F | `abs_nch` | shots/rd, length, OUR ti/rd | 69 | 577 | **+0.142** [+0.084, +0.199] | 0.000 |

Logit with opponent fixed effects, coefficient per SD of `abs_nch`:

| model | coef | z |
|---|---|---|
| `abs_nch` | +0.732 | +6.96 |
| + shots/rd | +0.856 | +7.45 |
| + length | +0.846 | +6.95 |
| + our ti/rd | +0.718 | +5.82 |
| + our builds/rd | +0.712 | +5.78 |
| + their turret builds + their rating | +0.839 | +6.23 |

The association is real and it is not the length confound, not our economy, not
their turret count, not their rating.

### Why this cut still cannot certify the drain claim

Run the **same** instrument on the other places their shots can land:

| treatment (same strata: opponent x shots/rd x length) | win delta | p |
|---|---|---|
| `abs_nch` — healed non-core buildings | **+0.199** | 0.000 |
| `abs_ncx` — non-core buildings, core shots removed from denominator | +0.119 | 0.001 |
| `abs_core` — **our core** | **-0.178** | 0.000 |
| `abs_emptyx` — **empty tiles** (their shot hit nothing at all) | **-0.257** | 0.000 |

A shot into an empty tile is the purest possible "wasted enemy ammo" — it costs
us literally nothing, not even a barrier. Under the drain-pump logic it should be
our **best** outcome. It is our **worst**. The ranking buildings > core > empty
is not a ranking of how much of their ammo was wasted; it is a ranking of **how
much of our material was alive and standing in their firing lines**. `abs_nch`
is a presence-and-survival marker wearing a drain costume.

**CUT 1 verdict: positive association, drain-consistent, but non-diagnostic —
the instrument cannot separate "we baited them" from "we were still alive and
forward". Not evidence for the build.**

## CUT 2 — the economy channel (the cut that can actually falsify)

Ammo is bought 1:1 from titanium. A genuine drain must show up as **less economy
for them**. Same strata, outcome = their ti_coll per round.

| # | treatment | strata | n | **THEIR ti/rd delta** | p | 95% CI |
|---|---|---|---|---|---|---|
| A | `abs_nch` | shots/rd | 598 | -0.22 | 0.646 | [-1.09, +0.67] |
| B | `abs_nch` | shots/rd, length | 598 | -0.21 | 0.650 | [-1.04, +0.65] |
| B | `abs_nc` | shots/rd, length | 598 | +0.08 | 0.865 | — |
| B | `abs_cheaph` | shots/rd, length | 598 | +0.48 | 0.319 | [-0.35, +1.35] |
| B | `abs_cheap` | shots/rd, length | 598 | +0.16 | 0.735 | — |
| C | `abs_nch` | shots/rd, r=1000 only | 221 | -1.04 | 0.271 | — |
| D | `abs_ncx` | shots/rd, length | 598 | +0.12 | 0.794 | — |

**Base rate: their ti_coll/rd = 9.56. The 95% CI [-1.04, +0.65] excludes any
drain effect larger than about 11% of their income, and the point estimate is
2%.** This is a powered null, not an underpowered shrug. Four of seven point
estimates have the *wrong* sign.

### The symmetric check the commission asked for

| outcome | delta (hi - lo absorbed-share) | 95% CI | base | as % of base |
|---|---|---|---|---|
| **THEIR** ti_coll/rd | **-0.21** | [-1.04, +0.65] | 9.56 | -2% |
| **OUR** ti_coll/rd | **+3.22** | [+2.44, +4.05] | 8.70 | **+37%** |

The commission asked whether our heal upkeep costs us as much as the drain costs
them. The answer is neither: **there is no measurable cost to them at all, and
the entire association sits on our side** — an 18x asymmetry. Heal upkeep is not
eating our gain; our gain *is* our own economy surviving, and the enemy's ammo
bill is a bystander.

### Three further economy-side probes, all against the claim

| question | measure | result |
|---|---|---|
| Do they **overspend** ammo when we offer bait? | their ammo Ti/rd | **-0.23** [-0.38, -0.07], p=0.003 — they spend *less*, not more |
| Do they **shoot more** when we offer bait? | their shots/rd | -0.016, p=0.246 — flat |
| Does their **ammo tax** rise (ammo Ti / ti collected)? | e_ammo / e_ti_coll | +0.079, p=0.649 — flat |

Their total shot *count* does rise with absorbed-share (+63 shots, p<0.001) —
but that is purely the length confound: per round it is flat. **Presenting more
absorbable surface does not induce a single extra shot per round.**

### Volume ledger — the ceiling on the prize

| opponent | n | their ammo Ti/rd | **drain Ti/rd** (healed non-core absorption, in titanium) | as % of their income | their ti/rd | our ti/rd |
|---|---|---|---|---|---|---|
| Ouroboros | 85 | 4.01 | 0.85 | 6.3% | 13.53 | 6.95 |
| Powerpuff Girls | 80 | 3.35 | 0.70 | 5.8% | 11.93 | 9.00 |
| OopsGotYourElo | 66 | 1.63 | 0.42 | 3.8% | 11.23 | 14.69 |
| Leviathan | 82 | 2.79 | 0.36 | 6.6% | 5.43 | 8.11 |
| Lunds Stallions | 115 | 4.01 | 0.38 | 4.7% | 8.05 | 6.73 |
| Kings College Munich | 95 | 3.42 | 0.41 | 4.2% | 9.67 | 8.98 |
| CtrlAltDefeat | 75 | 3.26 | 0.35 | 4.5% | 7.76 | 8.40 |
| **all** | **598** | **3.30** | **0.49** | **5.1%** | 9.56 | 8.70 |

Even if every drained titanium were pure profit, the whole pump is worth
**0.49 Ti/round — 5.1% of their income, 15% of their ammo bill**. That is the
ceiling on a mechanism the economy data says is not firing at all.

**CUT 2 verdict: NULL — decisively, and with the power to say so.**

## Guards

### (i) Length control

`abs_nch` vs game length: r = **+0.377** pooled (within-opponent +0.012..+0.568,
median +0.372). Handled three ways — median-split on length inside every
stratum (B), restriction to the 226 games that ran the full 1,000 rounds (C),
and length as a logit covariate. The win effect drops from +0.245 to +0.199 and
holds; the economy null does not move.

### (ii) Reverse causation — is high absorbed-share just "fewer valuable enemy targets"?

| pair | pooled r | within-opponent (min..max, median) | reading |
|---|---|---|---|
| `abs_nch` vs their turret builds | +0.135 | -0.029..+0.291, med **+0.223** | high absorption goes with **more** enemy turrets, not fewer — rules the story out |
| `abs_nch` vs their pre-match rating | -0.139 | -0.371..+0.286, med **-0.007** | ~zero within opponent; the pooled figure is composition across opponents |
| `abs_nch` vs their shots/rd | -0.032 | -0.098..+0.148, med -0.005 | the dominance control is orthogonal to the treatment, as intended |
| `abs_nch` vs our version | +0.008 | -0.144..+0.325, med +0.141 | not a bot-version artefact (23 of our versions in the window) |
| `abs_nch` vs **our** ti/rd | +0.386 | +0.309..+0.453, med +0.326 | **this is the live alternative explanation** |
| `abs_nch` vs their ti/rd | +0.041 | -0.215..+0.172, med -0.065 | nothing on their side |

The one live confound is our own economy, and it is controlled explicitly in
spec F: the win effect survives at +0.142 [+0.084, +0.199]. The reverse cut also
holds — our ti/rd predicts wins at +0.091 (p=0.008) *within* absorbed-share
strata. Both are real; neither is drain.

### (iii) Healed vs unhealed absorbers

The flag exists per target building (`rx_tgt.nshots_healed`, +/-2-round heal
window) so the **preferred healed-absorber treatment was used throughout**;
`abs_nc` is the coarse fallback and is reported next to it everywhere. Healed
absorption is consistently the stronger predictor of the two, which is the one
piece of the original claim that survives — see below.

## The one build-relevant thing that did survive

Hold the absorbed **volume** fixed (stratify on `abs_nc` as well) and vary only
the **composition** of what absorbed:

| treatment | strata | cells | n | win delta | p | 95% CI |
|---|---|---|---|---|---|---|
| **cheap** share of absorbers (conveyor/splitter/barrier) | opponent x shots/rd x absorbed-share | 42 | 598 | +0.056 | 0.104 | — |
| **cheap** share of absorbers | + length | 68 | 587 | **+0.016** | **0.676** | [-0.035, +0.072] |
| **healed** share of absorbers | opponent x shots/rd x absorbed-share | 42 | 598 | +0.100 | 0.003 | — |
| **healed** share of absorbers | + length | 64 | 561 | **+0.070** | **0.045** | [+0.011, +0.127] |

And on the economy, at fixed absorbed volume:

| treatment | THEIR ti/rd | p | OUR ti/rd | p |
|---|---|---|---|---|
| cheap share of absorbers | +0.43 | 0.352 | +0.85 | 0.049 |
| healed share of absorbers | +0.24 | 0.594 | **+1.69** | **0.000** |

**Cheapness of the absorber buys nothing** — the confidence interval brackets
zero tightly. **Keeping absorbers healed buys +7 points of win rate**, and it
does so by adding **+1.69 Ti/rd to OUR economy**, with their economy untouched.

That is not a drain pump. It is **uptime on our own pipeline**: healing a
conveyor keeps titanium flowing, and the enemy shot it ate is incidental. The
correct restatement is *"heal what you already built"* — not *"build cheap
buildings so the enemy shoots them"*.

## What a build decision should take from this

1. **Do not build bait.** The specific claim — cheap buildings placed to absorb
   enemy fire — has a measured effect of +0.016 win rate [-0.035, +0.072] at
   fixed absorbed volume, and no detectable effect on the enemy economy at all.
2. **The drain is a rounding error even at its theoretical maximum**: 0.49 Ti/rd,
   5.1% of their income. Nothing built for it can repay its own cost scale.
3. **The surviving effect is healing, and its channel is our own throughput**,
   not their ammo bill. Any build that follows from this evidence should be
   priced against *our* ti_coll/round, and measured there.
4. **Forward material presence is what the outcome instrument was really
   tracking.** If a build wants to chase the +0.20, it should chase "our
   buildings alive and forward", with the empty-share result (-0.26) as the
   reminder that the point is contesting ground, not donating targets.

## Files

* `drain-cut/build.py` -> `drain-cut/games_us.tsv` (1,066 attributed games, 598 vs majors)
* `drain-cut/analyse.py` -> `drain-cut/tables.md` (specs A-E, all per-cell)
* `drain-cut/mediate.py` -> `drain-cut/mediation.md` (specs F-I, logit, guards, ledger)
* `drain-cut/compose.py`, `drain-cut/ci.py` (composition cuts, bootstrap CIs)
* `drain-cut/tl_final.tsv`, `drain-cut/tl_bld.tsv` (tl.tsv rollups)
