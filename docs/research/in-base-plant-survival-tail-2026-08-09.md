# The in-base plant tail: it is the FAR SUPPORTED nests, and we remove worse than the field

**Research arm, session 24, 2026-08-09.** Follow-up to
`gunner-plant-tiles-are-not-enumerable-2026-08-09.md` §5, which flagged the
never-removed tail as a lead. **The lead was right about where to look and wrong
about both the size and the sign, and this document corrects my own §5 in place.**

**Version tag:** live **v91** = `bots/_v100hf`, tree `4558be91`.
**Corpus only** (`events.tsv` 830,886 rows → 1,325 attributed replays), **zero replay
downloads**. Reproduces my published plant counts exactly: **6,407** enemy plants in
our band, **2,610** ours in theirs, 58.6% / 41.4% / median-14 headline all recovered.

**Pairing validity, checked before use.** `events.tsv` carries no entity id, so
BUILD→DEATH was paired FIFO on `(file, team, kind, x, y)`. This is sound for
buildings — they cannot co-occupy a tile, so builds and deaths must alternate — and
it verifies: **0 of 1,419 consecutive same-tile plants had overlapping lifetimes.**

---

## 1. THE CONFOUND — the 41.4% is about 40% censoring artifact

Survivors had a median **80 rounds of game left** after being planted; the removed
had **324** (n=2,653 / 3,754). **57.5% of "survivors" — 1,525 plants, 23.8% of the
whole population — had under 100 rounds of game left.** Restricting to plants built
before r500 changes nothing (41.3%, n=5,617): the confound is not *"built late on the
clock"*, it is *"built late in **this** game"*, and most games end well before r1000.

**Censored survival, which is the honest number:**

| horizon | still alive | at risk |
| --- | ---: | ---: |
| +50 rounds | **47.8%** | 5,341 |
| +100 | **34.5%** | 4,276 |
| +200 | **25.2%** | 3,179 |
| +400 | **20.9%** | 1,938 |

**The tail is ~25%, not 41.4%.** Still large, still the whole problem. Everything
below is *alive at +200 rounds among plants with ≥200 rounds of game left*
(n=3,179 over 675 games).

## 2. **AND MY §5 CLAIM WAS WRONG: WE REMOVE WORSE THAN THE FIELD**

I published *"our average removal is not obviously worse than the field's"* off the
raw 58.6%/65.1% split. **It does not survive the censoring fix.**

| comparison | survival at +200 | n |
| --- | ---: | ---: |
| **THEM** planted in **our** band | **25.2%** | 3,179 |
| **US** planted in **their** band | **20.3%** | 1,590 |

**+4.9pp, z = 3.77, p = 1.6e-4.** And the clean design — **same replay, both sides**,
which differences out map, seat, game length and opponent simultaneously — gives
**Mantel–Haenszel odds ratio 1.31 over 482 informative replays.** The gap holds at
every horizon: **+8.6pp at T=25, falling to +4.9pp at T=200.**

**Modestly, consistently, we are worse at clearing an enemy turret out of our base
than our opponents are at clearing ours out of theirs.**

## 3. THE DISCRIMINATORS, RANKED

Adjusted logistic (L2, n=3,179, 25 terms, **opponent fixed effects**, coefficients per
1 SD), cross-checked against Mantel–Haenszel **stratified by replay**.

| # | discriminator | adjusted b (OR) | within-game MH-OR | verdict |
| ---: | --- | ---: | ---: | --- |
| 1 | **Opponent** | FE range 2.40 log-odds (≈OR 11) | — | real, but **partly IS #5/#6** |
| 2 | We won that game | −0.610 (0.54) | — | **endogenous, not a lever** |
| 3 | Seat | +0.456 (1.58) | — | **contaminated — see §6** |
| 4 | Our `batk` rate in the game | −0.405 (0.67) | — | survives win/loss stratification |
| 5 | **Friendly turrets already within d²≤8** | +0.402 (1.50) | **2.13** | **real, causally clean** |
| 6 | **Distance from our core (d²)** | +0.256 (1.29) | **2.60** | **real, causally clean** |
| 7 | Round built (residual) | +0.204 (1.23) | 3.57 | real *after* censoring control |
| 8 | Our buildings within d²≤8 | −0.139 (0.87) | 1.57 (sign flips) | weak/unstable |
| 9 | Turret type (sentinel) | +0.091 (1.10) | — | **NULL — see §4** |
| 10 | Other enemy *non-turret* buildings nearby | +0.025 (1.03) | — | **NULL once turrets are in** |

### The two clean ones interact multiplicatively, and they are not the same variable

Survival at +200, n=3,179:

| friendly turrets ≤d²8 ↓ / distance → | near ≤8 | mid 9–17 | far 18–32 |
| --- | ---: | ---: | ---: |
| **0** | **10.8%** (n=719) | 18.5% (n=568) | 24.1% (n=597) |
| **1** | 17.5% (n=240) | 23.3% (n=249) | 37.2% (n=266) |
| **2+** | 34.0% (n=103) | 46.9% (n=213) | **62.9%** (n=224) |

**A 6× spread, both margins monotone.** And it inverts the intuition my own plant
document was carrying: **the plants pressed against our core DIE** — we have builders
there — **and the ones that live to r1000 are on the outer rim of the band with a
covering turret beside them.**

### Opponent is real but is substantially the geometry wearing a name

Per-game mean survival: **Powerpuff Girls 67.2%** (59 games / 243 plants),
**Ouroboros 48.2%** (72 / 377), **Lunds Stallions 37.9%** (93 / 346) at the top;
**Leviathan 5.0%** (45 / 501), CtrlAltDefeat 14.3% (65 / 295), Orizon 17.6% (16 / 99)
at the bottom. **This is exactly the three teams the attribution doc named as hurting
us most at home** — independent corroboration on a different statistic.

But it is not independent of #5/#6: mean friendly-turrets-nearby is **1.72 for
Powerpuff against 0.34 for Leviathan**, and mean d² is **20.4 against 11.3**. **The
opponent effect is substantially "which opponents build far, supported nests."**

**Map is separable from opponent** — every major opponent is met on 10–15 maps with
the top map only 11–24% of their games; map carries a **+25pp** marginal spread
(hive 52.1% n=169 → atoll 28.0% n=375 at T=100) that survives *within* opponent
(Lunds Stallions: antler 59.4% n=32 vs snowflake 12.9% n=31).

### "Did we actually try" is a real discriminator, not just a win proxy

Stratified by result: among games we **won**, `batk`/round <0.2 → 20.7% survival
(n=382) vs ≥0.2 → **11.9%** (n=804); among games we **lost**, 44.0% (n=877) vs
**21.6%** (n=1,116). **Same direction in both strata.** Still endogenous to game
length and opponent aggression, so the magnitude is not causal.

### The harm linkage, which is why the tail matters

Our builder-bot deaths inside our own band, by number of enemy plants surviving 200+
rounds in that game:

| surviving plants | 0 | 1 | 2 | 3 | 4 | 5+ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| our home builder deaths | **2.3** | 5.3 | 9.4 | 11.9 | 22.7 | 21.9 |
| games | 326 | 161 | 89 | 35 | 21 | 43 |

**Pearson r = 0.518 over 675 games.** **Direction of causation is not established by
this** — a game where we are losing produces both.

## 4. THE NULLS, with power stated

* **Turret type is NULL.** Gunner 25.9% (n=2,633) vs sentinel 22.2% (n=546),
  **−3.7pp, 95% CI [−7.6, +0.2]pp**, adjusted OR 1.10. **MDE at 80% power is 5.5pp**,
  so this rules out effects larger than that and nothing smaller. **Report as null
  with the power attached, not as "sentinels die slightly more".**
* **Non-turret enemy buildings nearby are NULL** once neighbouring *turrets* are in
  the model (b = +0.025). The marginal *"≥3 enemy buildings nearby → +29pp"* is the
  turret count in disguise. **It is covering fire, not clutter.**
* **Our own bot version shows no trend** (v64 32.4%, v70 7.1%, v80 35.5%, v90 40.5%,
  v91 13.0%, n=60–766 each). Bounces 7–40% with no monotonicity, and the opponent mix
  changes with ladder rating. **Uninterpretable, not "we got worse".**

## 5. THE ONE SENTENCE — **AND IT IS RETRACTED; SEE THE CORRECTION UNDER IT**

> **CORRECTION, same day, by the author. THE "12 ROUNDS" FIGURE BELOW IS
> CONTAMINATED AND THE TRUE WINDOW IS ROUGHLY TWICE AS WIDE.** The follow-up
> precursor analysis found that the nest label counted a **same-tile REBUILD** of the
> seed as "a second turret" — and this corpus contains one gunner rebuilt **158 times
> on a single tile in one game**, so that is not a rare contaminant.
>
> **I re-derived it myself from `corpus/events.tsv` rather than accepting the
> correction on trust**, over all 6,407 enemy plants inside our band:
>
> | next turret within d²≤8 of the seed | share of seeds | median lag |
> | --- | ---: | ---: |
> | **same-tile rebuild** | 16.0% (1,023) | 11 rounds |
> | **distinct tile** — the only thing that is actually a nest | **55.7% (3,567)** | **22 rounds** (p25 5, p10 2) |
> | neither | 33.3% (2,135) | — |
> | *pooled, as originally published* | *71.6% (4,590)* | *17 rounds* |
>
> **Use ~22 rounds, not 12.** The pooled cut mixed a fast rebuild-in-place with a
> genuine second emplacement and reported the blend. **This makes the reaction budget
> WIDER than I told the builder, not narrower** — the correction is in our favour, and
> it would have been just as wrong if it had not been. The hard tail is real and
> should be quoted alongside it: **19.6% of distinct-tile second turrets land within
> 3 rounds, 35.8% within 10.**
>
> The independent analysis reports 25.3% (834/3,295) as the corrected nest rate under
> a stricter definition (distinct tile, within 30 rounds, **seed still alive**),
> against 50.4% under the contaminated label. My looser re-derivation and its stricter
> one agree on the direction and on the median; **the sentence below should be read as
> superseded, not adjusted.**



**The surviving tail is not the plants next to our core — it is the far-rim plants
that already have a covering friendly turret (62.9% survive 200+ rounds, n=224,
against 10.8% for a lone plant next to our core, n=719) — and the median gap from a
lone seed plant to the second turret beside it is 12 rounds (n=2,431, 45.1% inside 10
rounds), so any removal we build must fire within about a dozen rounds of the FIRST
turret or it is fighting a nest instead of a plant.**

**The caveat that must travel with it: in 57.7% of those 2,431 cases the seed was
already dead when the second turret arrived.** Killing the seed does **not** prevent
the second plant; it only prevents the pair existing simultaneously. **The lever is
speed against nest FORMATION, not seed denial.**

## 6. LIMITS — including two that apply retroactively to my earlier documents

* **A `DEATH` row cannot separate "we killed it" from "they destroyed it
  themselves"** (`destroy()` is free, unlimited, and emits the same `removeEntity`).
  Every "removal" number here is really **disappearance**. The `batk` correlation is
  the only evidence our action is involved, and it is correlational.
* **Kills are not attributable at this grain.** I cannot say a surviving plant
  produced 45 kills — only the game-level dose-response in §3. Linking plant identity
  to the kill-attribution decoder is the one thing that would turn *"survives"* into
  *"costs us X builders"*.
* **THE BAND IS NOT THE SAME PHYSICAL REGION FOR BOTH SEATS, AND THIS CONTAMINATES
  EVERY d²-BASED CUT IN THIS PROJECT — including mine and the attribution doc's.**
  `d2` is measured to the **NW corner** of the 2×2 core. Team index 0 is always the
  NW-ish core (mean normalised position 0.26, 0.38), team 1 the SE core (0.69, 0.64),
  so **on the threat-facing diagonal the same physical proximity maps to a d² about
  one tile larger for seat 0.** The seat effect survives distance bucketing (far:
  23.8% seat 0 n=512 vs 45.6% seat 1 n=575), but **"we defend worse from seat 0" and
  "the band is a different place from seat 0" are not separable from this column.**
  The attribution doc's own sensitivity check (measuring from the nearest footprint
  tile instead of the NW corner) moved its shares by 6pp and is the same issue.
* **Plants are not independent.** 6,407 plants sit on 4,988 (game, tile) keys, and
  **19 hot keys carry 590 plants (9.2%)** — one Leviathan gunner was rebuilt **158
  times on tile (12,3) in a single game.** De-duplicating to the first plant per
  (game, tile) moves the baseline from 25.2% to **30.5%** (n=2,404) and **leaves every
  discriminator intact** (near 20.6% / far 40.5%; 0-turret 22.8% / 2+-turret 54.7%).
* **Clustering is a snapshot at plant time only** — whether support arrived or was
  lost afterwards was not tracked.

## Provenance

Analysis by a research-arm subagent (`opus`), scripts in the session scratchpad
(`tail/mkplants2.py`, `a1_confound.py`, `a2_discrim.py`, `a3_disentangle.py`,
`a4_model.py`, `a5_residual.py`, `a6_seat_ver.py`, `a7_validate.py`). **The plant
counts, the 58.6/41.4 split and the median-14 headline were required to reproduce my
published figures before anything new was accepted, and they did.** The scripts die
with the session; the method is fully stated above and the inputs are committed.
**The censoring correction and the removal-gap sign change are corrections to my own
prior deliverable and are marked there in place.**
