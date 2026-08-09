# There is no precursor to an in-base nest. Their builders are always in our base.

**Research arm, session 24, 2026-08-09.** Closes the question opened by
`in-base-plant-survival-tail-2026-08-09.md` §5: **can a response to nest formation be
anticipatory, or is it stuck inside the reaction window?** Answer: **anticipatory is
dead.** But the window is about **twice as wide** as I told the builder, and that
correction is the more useful half of this document.

**Version tag:** live **v91** = `bots/_v100hf`, tree `4558be91`. **Corpus only, zero
replay downloads.** Decoder: a ~340-line extension of the preserved
`docs/research/scripts/side-lane-2026-08-09/bb_decode.py` — 1,325 attributed replays →
**6,407 plants / 53,914 episodes / 401,560 zone-rounds, 0 errors, 11 s**.

**Validated before use.** The 6,407 plants are an **exact multiset match** with
`corpus/events.tsv` on `(file, round, kind, x, y)` — symmetric difference **0** — and
**0 plants had no orthogonally adjacent enemy builder**, which is a real positional
check because a build *requires* orthogonal adjacency.

---

## 1. THE ANSWER: no usable precursor, and the reason is structural

**An enemy builder is inside our core's vision in 62.0% of all rounds played**
(401,560 of 647,620 over 1,296 games — **56.5% even in r0–50**). Their presence in our
base is the **normal state of the game**, not an event. Nothing built on "an enemy
builder is here" can be a trigger.

| trigger (round grain — the grain an in-bot rule lives at) | fires on | P(in-band plant within 10 rounds) | **false positive** |
| --- | ---: | ---: | ---: |
| *baseline, no trigger* | 100% of rounds | **7.7%** | — |
| ≥1 enemy builder in d²≤36 | 62.0% | 10.7% | **89.3%** |
| ≥2 enemy builders | 36.1% | 12.3% | **87.7%** |
| ≥3 enemy builders | 19.2% | 12.7% | 87.3% |
| some builder loitering ≥5 rounds | 56.4% | 10.3% | 89.7% |
| some builder loitering ≥20 rounds | 47.0% | 9.3% | **90.7%** |

**Best case is 1.65× a 7.7% base rate while firing in a fifth of all rounds.
Loiter-based triggers are WORSE than raw presence.**

The episode grain agrees: of **53,914** enemy-builder visits into d²≤36 (41.6 per
game, median length 3 rounds), visits lasting ≥10 rounds plant a turret only **22.4%**
of the time and **build nothing at all 67.6% of the time**. Even visits of ≥100 rounds
build nothing **43.3%** of the time.

## 2. **THE LABEL CORRECTION, AND IT RETRACTS MY OWN HEADLINE**

The naive nest label — *"≥2 enemy turrets within d²≤8 within 30 rounds"* — counts a
**same-tile REBUILD** of the seed as a second turret. This corpus contains one gunner
rebuilt **158 times on one tile in a single game**, so this is not a rare contaminant:
**569 of 1,660 "nests" (34%) were the seed's own tile being rebuilt.**

**I re-derived it independently from `corpus/events.tsv` rather than accepting the
correction on trust**, over all 6,407 plants:

| next turret within d²≤8 of the seed | share of seeds | median lag |
| --- | ---: | ---: |
| **same-tile rebuild** | 16.0% (1,023) | 11 rounds |
| **distinct tile — the only thing that is a nest** | **55.7% (3,567)** | **22 rounds** (p25 5, p10 2) |
| neither | 33.3% (2,135) | — |
| *pooled, as I originally published it* | *71.6% (4,590)* | ***17 rounds*** |

**My published "median gap … is 12 rounds" is superseded. Use ~22.** The independent
analysis reports **23** under a stricter definition (distinct tile, within 30 rounds,
seed still alive) and a corrected nest rate of **25.3% (834/3,295)** against 50.4%
under the contaminated label. **Two derivations with different filters agree on the
direction and the median.**

**This widens the reaction budget rather than narrowing it** — the correction happens
to be in our favour, and it would have been just as wrong if it were not. **The hard
tail must be quoted with it: 19.6% of distinct-tile second turrets land within 3
rounds, 35.8% within 10.**

## 3. The contrasts, with the corrected label

**Loiter is a real, large effect pointing the OPPOSITE way to the hypothesis.**
Consecutive rounds the planting builder had already spent in d²≤36 before building:

| | NEST-seed (n=834) | LONE-seed (n=2,461) |
| --- | ---: | ---: |
| median | **5** | **14** |
| loiter ≥10 | 34.5% | **56.7%** (−22.2pp, z=−11.06) |
| loiter ≥50 | 12.5% | 29.8% |

Within-replay **MH-OR 0.605** over 275 informative replays, and it holds in **every**
stratum tested: all four round bands, games won and lost, hot-tile-deduplicated,
unique-attribution-only, and both seats. **A long loiter is the signature of a
resident late-game grinder planting a lone turret — not of a nest.** Under the
contaminated label the sign was the other way (12 vs 9); **the correction flipped it.**

**Approach separates nothing before arrival.** Entry distance identical (median d²=29
both groups); arrival by launcher throw identical (8.6% vs 8.3%, z=0.31). All
separation appears *after* the bot is already in the zone, and all of it is **less**
warning: nest builders are younger (median age 33 vs 78 rounds), move more in the
preceding 10 rounds (8 vs 6), and close distance faster (median d² drop 16 vs 3).
**Profile: a fresh bot walks in and plants immediately.**

**Multiplicity is a flat null, mildly inverted.** Distinct enemy builders in d²≤36 at
t−1: nest mean 2.0, lone 2.1, median 2 in both. P(nest) by builder count runs
27.3% / 26.2% / 29.9% / **16.2%** / 23.4% / 28.2% for 0–5+; for *fast* nests it
inverts cleanly (1 builder 23.6% → 3 builders 11.6%). **"A second builder arrived" is
not a precursor.**

**Visibility is total and useless.** The d²≤32 band lies entirely inside the core's own
vision (r²=36), so **3,295/3,295 seed tiles are core-visible by construction**, and
the planting builder itself stood in core vision in **94.1% of 6,397 plants**.
**Approximation limits, stated:** circular radius from the core's NW corner, no
line-of-sight or occlusion, never checked against the engine's own vision routine, and
it ignores whether the unit was alive and running `run()` at that instant. **It
supports "the geometry permits sensing", not "our bot sensed it".**

## 4. The only thing that predicts a nest is the clock — and it is a constant

Seeds planted **r0–50 nest 38.8%** (n=1,040) → r51–150 21.6% (n=782) → r151–300 22.2%
(n=703) → **r301+ 13.8%** (n=770). That is a prior available at round 0, not a signal.

Measured time budget: median **5 rounds** from the first enemy builder entering our
core's vision to the first in-band plant of the game (n=1,148; p10=1, p25=2).

## 5. What this means for a build

1. **Anticipation is refuted.** Every trigger tested carries an ~87–91% false-positive
   rate against a 7.7% base rate. **A rule that fires in a fifth of all rounds to
   catch a 12.7% event is not a trigger, it is a tax.**
2. **The response must be reactive, and it has ~22 rounds, not 12.** That is a
   materially easier constraint than the one I handed over.
3. **But 19.6% of second turrets land within 3 rounds.** A reactive rule tuned to the
   median will miss the fast fifth entirely, and the fast fifth is where nests form.
4. **Do not gate anything on loiter.** It is a real signal pointing the wrong way — it
   identifies the resident grinder that plants **alone**.
5. **The early game is where nesting happens** (38.8% at r0–50 against 13.8% at r301+),
   which is the same window where DODGE's transit share is largest (48.0% of forward
   deaths at r≤100). **Two independent lines now point at the opening.**

## 6. Limits and confounds

* **Enemy titanium/ammo at seed time is not decoded** (`updatePlayers`), and is not
  observable in-game either — so the real driver of *"can they afford a second
  turret"* is out of reach on both counts.
* **Intent is not observable.** Nothing here separates a planned nest from two
  independent plants that happened to land near each other.
* **Loiter is confounded with game phase and length** — long loiters come from long
  games, which are late-phase, where nest rate is structurally low. Stratifying by
  round band leaves the inversion intact in all four bands, so it is not purely this,
  **but the magnitude is not clean.**
* **"They nest because they're winning" vs "they win because they nest" is not
  separable.** Nest rate is 25.0% in games we lost (n=2,038) against 25.8% in games we
  won (n=1,257) — a null, so nesting is at least not a simple losing-marker.
* **Opponent range is enormous**: 4.7% (I Stone, n=128) to 68.2% (Team 48, n=170), with
  Leviathan at 20.1% (n=541). Our games only.
* **Seat/band contamination persists** (d² to the NW corner); reported split, and the
  loiter effect is seat-independent (−17.3pp / −16.3pp).
* **`destroy()` vs kill remains indistinguishable**; it affects only the
  "seed still alive" coexistence test.
* **Planter attribution is ambiguous for 10.0% of plants** (≥2 orthogonally adjacent
  enemy builders). The result holds in the unique-attribution subset (n=2,963,
  z=−9.18).
* **The 5.9% of plants built from outside d²≤36 have no episode row**, so the negative
  control slightly under-covers them.
* **Kill attribution linked to plant identity is still the open item** from the
  survival doc and was not touched. It remains the one thing that would turn
  *"survives"* into *"costs us X builders"*.
