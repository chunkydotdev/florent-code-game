# DECODE — DOES *OUR* PLAY CAUSE FLOTTE'S BUILDER TLEs? (QUEUE #98, causal step)

**PROVENANCE**
* **Agent:** fresh opus decode-only subagent, no inherited session context beyond the
  commissioning brief. Commissioned by **research s52, 2026-08-20**.
* **Clock:** `date -u` = **2026-08-20T10:00:44Z**; repo HEAD `13c1f3c6df9b` (2026-08-20T11:58:57+02:00).
* **Inputs, exactly:** `QUEUE.md` row **#98**;
  `docs/research/REPLAY-STUDY-flotte-v55-2026-08-20.md` (piece E and its §0 controls);
  `tools/replay_schema.md`; `tools/replay_census.py` (parser primitives `fields`,
  `read_pos`, `parse_entity`); `tools/tle_census.py` (the `BotOutput.tled` resolution rule,
  re-used verbatim); `corpus/join.tsv`; `corpus/meta_join.tsv`; `replay_archive/*.replay26`.
* **No games run, no bots edited, no platform calls.** Archive decode only.
* **Decoder** (session scratchpad, not committed): per-replay round-level reconstruction
  emitting one row per **Flotte builder-bot unit-round the engine actually ran** with
  **round-START** dose features (round-start state is what `run()` sees), plus one row per
  game-round. Surfaces:
  * **US surface** — the **40 rated** games vs Flotte at their v54/v55 (`join.tsv`,
    `opp ~ /Flotte/`, `oppver ∈ {54,55}`; all 40 present in the archive).
    **32,434 Flotte builder unit-rounds.**
  * **TP surface** — **365** archived Flotte v54/v55 games against **non-us** opponents
    (`meta_join.tsv`, 15 opponents with ≥5 games). **367,565 Flotte builder unit-rounds.**
    *(`meta_join` is used here for a POPULATION, not a rated win-rate denominator — the
    standing prohibition governs the latter.)*

---

## VERDICT

> ## **ARTIFACT** — on the dose the study proposed.
> ## **CAUSAL, but small and via a DIFFERENT dose** — our TURRETS in a Flotte builder's vision.

**The study's piece E claim — "the rate tracks *our* build volume" — is REFUTED as a causal
claim on every within-game estimator and on the between-opponent panel.** Its MEASURED
numbers all reproduce exactly (see §6); it is the arrow that fails.

**What actually produces the 1,931 TLEs is a LATCH, not a dose.** 98.0% of them are the
*persistence* of **21** builder units that enter a permanent timeout state and then time out
for most of the rest of the game. The question "what raises their TLE count" is therefore
the question "what fires a latch", and the answer is dominated by **their own clock and
their own economy**, with **one small channel we control**.

| | estimator | n | verdict |
|---|---|---|---|
| **Strongest control FOR artifact** | Between-opponent panel: Flotte's TLE rate vs opponent build volume across **15** third-party opponents (≥5 games each) | 365 games / 367,565 builder-rounds | **r = +0.086.** Besvikomat builds **94.8**/game → **0.0000** TLE rate; sporks **114.2** → **0.0000**; Erebus **38.5** → 0.0363. The dose ordering the study inferred from a 2-point comparison **does not exist across 15 points.** |
| **Strongest control FOR causal** | Discrete-time latch hazard, **(game × round) fixed effects**, covariates `vis_turret` + `vis_focus` + `near_theircore`, SE clustered by game | US: 21 events / 28,371 at-risk builder-rounds; TP: 100 events / 340,992 | `vis_turret` **+1.23e-3 (t +3.11)** US and **+1.63e-4 (t +2.90)** TP, both surviving the strictest FE and both conditioning variables, and surviving dropping the r102 events. |

---

## 1. THE OBJECT IS A LATCH, NOT A RATE — and this reframes everything (MEASURED)

| fact | US surface (40 rated games) | TP surface (365 games) |
|---|---|---|
| TLE'd builder unit-rounds | **1,931** (reproduces the study's 993 + 938 exactly) | 13,214 |
| mean TLEs/game | 48.3 | 36.2 |
| **median TLEs/game** | **0** | **0** |
| games with **zero** TLEs | **23 of 40 (58%)** | 265 of 365 (73%) |
| top-5 games' share of all TLEs | **62.3%** | 36.8% |
| builder units with ≥10 TLEs ("latched") | **21 of 160 (13.1%)** | 100 of 1,512 (6.6%) |
| **share of ALL TLEs held by those units** | **98.0%** | 98.5% |
| once latched, share of that unit's remaining rounds that also TLE | median **0.827** | median **0.972** |
| `moved` share, 30 rounds before latch → during TLE rounds | **0.686 → 0.064** | 0.627 → 0.040 |
| TLE'd rounds per latch | mean 90, median 69 | mean 130, median 57 |

**⇒ "48.3 TLEs/game" is a mean over a distribution whose median is 0.** The per-game rate
quantises: post-r102 TLE rate per game is either **exactly 0.0000** or lands near **0.25**
(observed: .2455 .2500 .2500 .2500 .2561 .2640 .2830 .3018 .3107 .3353 .4792) — i.e. **one
of their four builders timing out every round.** Flotte hard-caps at four builders and never
replaces them (study piece B), so a latch is **25% of their builder capacity, frozen for the
rest of the game.**

**⇒ The residual hazard, once persistence is removed, is flat and tiny.** Excluding each
unit's own post-latch rounds, r≥102 TLE rate by dose bin runs **0.0000–0.0024 across every
bin of both `vis_focus` and `vis_other`, on both surfaces** — no gradient in either.

---

## 2. THE DOMINANT TRIGGER IS THEIR OWN CLOCK AT ROUND 102 (MEASURED)

Per-round TLE rate steps at **exactly r102**, on both surfaces, with nothing on our side
changing at that round:

```
TP:  r99 .005  r100 .003  r101 .005 |  r102 .043  r103 .043  r104 .044 ...   (8.6x step)
US:  r99 .020  r100 .027  r101 .034 |  r102 .075  r103 .082  r104 .082 ...   (2.2x step)
```
**44 of 100 third-party latches fire at round 102 exactly** (53 of 100 in r100–105); the
next most common round has 4. This is a scheduled behaviour change inside Flotte's own code
and is **exogenous to the opponent** — it is the same round against Erebus, Torsko, 0033,
DinooniD, Banminary, Pantheon and Focalground (per-opponent median latch round = 102 for
seven of the ten opponents with ≥3 latches).

---

## 3. THE ESTIMATORS, AND WHAT EACH ONE SAYS

Every estimator below is **within-game**, so game LENGTH — the study's named confound —
cannot enter. Dose definitions, all computed at round start from that builder's own
position with **builder vision r² = 20**:

* `vis_other` — **our** entities (all types) in that builder's vision
* `vis_other_units` / `vis_turret` / `vis_bot` — our units / our turrets / our builder bots in vision
* `vis_focus` — **their own** entities in vision
* `near_builds` — our build events **this round inside that builder's vision**
* `far_builds` (placebo) — our build events this round **>d²100 from every** Flotte builder
* `jump` — that builder displaced by d²>2 in one round (launcher throw / engine displacement)
* `cum_builds`, `other_alive`, `focus_alive` — game-level counters

### 3.1 ESTIMATOR A — within (game, round) FE, across their four builders, outcome = `tled`
Removes game, map, version, round number, their global economy — everything shared by the
round. Cluster-robust SE by game.

| surface | `vis_other` | `vis_focus` | `vis_all` |
|---|---|---|---|
| US (n=30,913 / 40 games) | **−0.0086 (t −2.85)** | +0.0032 (t +1.70) | −0.0039 (t −1.34) |
| TP (n=332,251 / 365 games) | **−0.0024 (t −3.37)** | +0.0025 (t +2.65) | −0.0002 (t −0.20) |

Same with **`exec_us`** (the continuous compute measure, far more power) as the outcome:
`vis_other` **−82 µs/entity (t −2.65)** US and **−23 µs (t −3.54)** TP; `vis_focus`
**+47 µs (t +2.31)** US and **+32 µs (t +3.75)** TP. Jointly (both regressors), `vis_other`
stays negative (US t −2.26) and `vis_focus` stays positive (TP exec_us t +2.17).

**⇒ Their builder's per-turn compute rises with THEIR OWN entity density in vision and does
not rise with ours.** The mechanism hypothesis in the brief ("TLEs spike when their
builder's visible-entity count rises, so we can stand things in their vision cheaply") is
**directly falsified for OUR entities and confirmed for THEIRS.**

### 3.2 ESTIMATOR B — game-round panel, within (game, 25-round bucket) FE, outcome = TLE count

| x | US | TP |
|---|---|---|
| `other_builds` (our builds this round) | +0.0044 (t +1.10) | **−0.0021 (t −2.32)** |
| `ob_prev5` (our builds, previous 5 rounds — the **lead-lag** term) | −0.0051 (t −1.61) | −0.0013 (t −1.98) |
| `near_builds` prev5 | −0.0007 (t −0.17) | −0.0018 (t −1.96) |
| **`far_builds` prev5 (PLACEBO)** | −0.0011 (t −0.28) | −0.0009 (t −1.01) |
| `focus_alive` (their own entity count) | **+0.0024 (t +2.29)** | **+0.0005 (t +4.44)** |
| `other_alive` (our entity count) | −0.0001 (t −0.07) | +0.0006 (t +2.79) |
| joint `ob_prev5` + `focus_alive` | −0.0045 (t −1.48) / **+0.0020 (t +2.22)** | −0.0013 (t −1.95) / **+0.0005 (t +4.37)** |

**⇒ The lead-lag runs the WRONG WAY.** Our build volume in the preceding 5 rounds does not
predict a rise in their TLEs at fixed round-stratum; the point estimate is negative on both
surfaces. **The placebo reads null**, as required — but so does the real dose, so the
placebo is confirming the instrument's calibration, not a finding.

### 3.3 ESTIMATOR C — MATCHED CASE-CONTROL on the latch event (the primary causal estimator)

**Design:** for each latch, the risk set is every Flotte builder alive and **not yet
latched** in that exact game-round. Ask: is the builder that latched the one with the higher
dose? Reported as the **normalised rank of the case within its matched set** (null = 0.500),
SE clustered by game. This is the conditional-logit-equivalent of a hazard model with
(game × round) fixed effects, and it is the strongest thing the archive supports.

| dose | US: rank [95% CI], t | TP: rank [95% CI], t |
|---|---|---|
| `vis_focus` **(theirs)** | **0.817 [0.712, 0.923] t +5.88** | **0.643 [0.581, 0.705] t +4.54** |
| `near_theircore` (d²≤36 of THEIR core) | **0.758 [0.684, 0.832] t +6.80** | **0.590 [0.539, 0.641] t +3.44** |
| **`vis_turret` (OUR turrets)** | **0.647 [0.587, 0.706] t +4.84** | **0.570 [0.522, 0.618] t +2.88** |
| `vis_bot` (our builder bots) | 0.671 [0.569, 0.772] t +3.29 | 0.542 [0.488, 0.596] t +1.51 |
| **`vis_other` (ALL our entities)** | **0.468 [0.333, 0.604] t −0.46** | **0.472 [0.408, 0.536] t −0.87** |
| **`near_builds` (our builds in its vision)** | **0.468 [0.404, 0.532] t −0.97** | **0.516 [0.481, 0.551] t +0.88** |
| `near_ourcore` (d²≤36 of OUR core) | **0.433 [0.382, 0.484] t −2.59** | **0.431 [0.391, 0.470] t −3.43** |

**⇒ The builder that latches is their HOME builder, standing in the thickest patch of their
own buildings.** At the latch round the median distance to **their own** core is d²=**10**;
**95% (US) / 79% (TP) are within d²36 of their own core**, against a 59% baseline over all
builder-rounds. Their **raider** — the one in our base eating our harvesters (study piece C)
— is *significantly less* likely to latch on both surfaces.

**⇒ `vis_other` and `near_builds` are informative nulls, not underpowered ones.** On TP the
`vis_other` CI is **[0.408, 0.536]**, which **excludes** an effect anywhere near the
`vis_focus` effect (0.643) measured on the same 100 events by the same machinery.

### 3.4 ESTIMATOR D — discrete-time latch hazard with (game × round) FE

Baseline latch hazard: **7.16e-4/builder-round** (US, 21 events / 29,334 at-risk) and
**2.88e-4** (TP, 100 / 347,182).

| model (FE = game × round, SE clustered by game) | US | TP |
|---|---|---|
| `vis_turret` + `vis_focus` + `near_theircore` | **`vis_turret` +1.255e-3 (t +3.19)**; `vis_focus` +4.2e-5 (t +1.25); `near_theircore` +1.02e-3 (t +1.99) | **`vis_turret` +1.659e-4 (t +2.93)**; `vis_focus` +2.90e-5 (t +3.46); `near_theircore` −6.8e-5 (t −0.81) |
| `vis_turret` + `vis_bot` + `vis_focus` + `vis_other` (FE = game × 25rd) | turret +9.74e-4 (t +1.99); bot +3.80e-4 (t +2.08); focus +8.83e-5 (t +2.27); **`vis_other` −2.85e-5 (t −0.83)** | turret +1.92e-4 (t +3.07); bot +5.29e-5 (t +1.48); focus +2.65e-5 (t +3.52); **`vis_other` −5.05e-6 (t −0.78)** |
| `cum_builds` (our cumulative builds) — FE = round-bucket only | +3.15e-5 (t +3.47) | +3.75e-6 (t +2.73) |
| `cum_builds` — **FE = game × 25rd** | +1.38e-4 (**t +1.24**) | **−5.35e-5 (t −5.11)** |

**⇒ `cum_builds` is the study's dose, and it is positive ONLY when games are compared to
each other and dies (US) or inverts (TP) the moment the comparison is moved inside a game.**
That is the signature of a length/trajectory confound, not a dose.

**ROBUSTNESS of `vis_turret` (FE = game × round, with `vis_focus`):**

| subset | US | TP |
|---|---|---|
| all | +1.234e-3 (t +3.11), 21 ev | +1.633e-4 (t +2.90), 100 ev |
| r<102 only | +1.496e-3 (t +2.14), 13 ev | +2.881e-4 (t +2.38), 22 ev |
| r≥102 only | +9.748e-4 (t +1.79), 8 ev | +1.621e-4 (t +2.40), 78 ev |
| **drop all r102 events** (removes their clock) | **+1.235e-3 (t +3.05)**, 18 ev | **+1.504e-4 (t +2.92)**, 56 ev |

Crude, un-modelled form, **home builders only** (d²≤13 of their own core), latch hazard by
our turrets in vision — TP: `0 → 3.58e-4` (36 ev/100,688), `1 → 3.64e-4`, `2 → 3.68e-4`,
**`≥3 → 1.95e-3` (6 ev/3,071, 5.4× baseline)**. US: `0 → 4.76e-4` (4 ev/8,410),
`1 → 2.61e-3` (6 ev/2,303), `2 → 1.68e-3` (1 ev/595), `3 → 0` (0 ev/80).
**⚠ The crude TP form suggests a THRESHOLD at ≥3 turrets, not the linearity the regression
assumes.** With 6 and 1 events in the top cells this is not settled; the linear coefficient
is the conservative reading and the threshold is the optimistic one.

---

## 4. THE CONTROLS, AND WHICH ONES CAME OUT THE OTHER WAY

**(a) Rounds with our units entirely outside their builders' vision.** Required by the
brief: if proximity drives it, this must be lower. It is **not** — the raw TLE rate by
`vis_other` bin is **non-monotone and DECREASING at the top** on both surfaces
(US `0 → .0405`, `1-2 → .0989`, `10-14 → .0932`, `15-19 → .0038`, `20-29 → .0000`;
TP `0 → .0292`, `1-2 → .0566`, `20-29 → .0151`, `30+ → .0000`). The top exposure bins are
the *cleanest*. **Control comes out against the dose hypothesis.**

**(b) Placebo dose — our builds >d²100 from every Flotte builder.** `fb_prev5` predicts
their TLE count at t **−0.28** (US) / **−1.01** (TP). **Reads null, as a placebo must.**
But `near_builds` — the real, in-vision version — also reads null (t −0.97 / +0.88), so
the placebo here certifies the instrument rather than isolating a mechanism.

**(c) Third-party playstyles.** Flotte v54/v55 against 15 opponents with ≥5 games:

| opponent | games | builder-rds | TLEs | **TLE rate** | latches/unit | **opp builds/game** |
|---|---|---|---|---|---|---|
| lingling_40h | 5 | 3,972 | 438 | .1103 | .100 | 45.4 |
| Pantheon | 5 | 11,177 | 1,205 | .1078 | .111 | 145.8 |
| 0033 | 15 | 22,576 | 1,268 | .0562 | **.161** | 91.9 |
| DinooniD | 20 | 25,308 | 1,301 | .0514 | .087 | 69.3 |
| team lazy | 5 | 17,705 | 742 | .0419 | .043 | 128.4 |
| HTTP 418 | 25 | 29,110 | 1,195 | .0411 | .113 | 82.5 |
| Focalground | 15 | 17,498 | 693 | .0396 | .050 | 82.1 |
| Erebus | 175 | 140,841 | 5,117 | .0363 | .056 | 38.5 |
| Juusto | 5 | 6,954 | 244 | .0351 | .150 | 58.2 |
| Banminary | 20 | 13,070 | 256 | .0196 | .048 | 46.5 |
| kladde chatte tville | 10 | 16,912 | 257 | .0152 | .062 | 82.9 |
| Torsko | 45 | 37,500 | 441 | .0118 | .059 | 92.1 |
| Dino | 10 | 12,436 | 57 | .0046 | .025 | 68.7 |
| **Besvikomat** | 5 | 7,374 | **0** | **.0000** | .000 | **94.8** |
| **sporks** | 5 | 5,132 | **0** | **.0000** | .000 | **114.2** |
| *(**us**, for placement)* | *40* | *32,434* | *1,931* | *.0595* | *.131* | *64.3* |

**r(opp builds/game, TLE rate) = +0.086; r(opp builds/game, latches/unit) = −0.104;
r(our-entities-in-their-vision, TLE rate) = −0.396.** *(n = 15 opponents.)*
**⇒ This is the control the study did not have.** Its dose inference rested on **two**
points (us 61.9 builds → 48.3 TLEs vs Erebus 35.4 → 29.2). At 15 points the relation is
gone. Two opponents building **more than us** induce **zero** TLEs in ~12,500 builder-rounds.

**(d) Instrument positive control — can a proximity-to-us column ever fire?** Same matched
case-control machinery, same columns, but outcome = **their builder DYING mid-game**.
TP (107 events, 72 game clusters): `vis_other_units` rank **0.632 (t +3.99)**,
`vis_focus` 0.628 (t +3.57), and `vis_other` **0.495 (t −0.15)**.
**⇒ The proximity columns are live and discriminating** — our *units* predict their builder's
death (they die where our turrets are) while our *entities-at-large* do not. A column that
reads 0.632 on death and 0.533 on latch is measuring, not blind.

**(e) Displacement / kidnap.** Only **40** displacement events on Flotte builders across the
40 rated games (29 across 365 TP games). **1 of 21 latches** (US) and **0 of 100** (TP) was
preceded by a displacement within 5 rounds. The FE estimate on `jump` is null
(US t −0.34, 154 rows). **⇒ Not a channel at the dose we currently apply — and the dose is
so small that this is a non-test, not a refutation.**

---

## 5. THE NATURAL EXPERIMENT (our v159→v162 against their frozen v54/v55)

| their ver | our ver | games | builder-rds | TLEs | rate | **post-r102 rate** | our builds/game | our entities in their vision (per builder-round) |
|---|---|---|---|---|---|---|---|---|
| v54 | v159 | 5 | 3,421 | 151 | .0441 | .0854 | 68.0 | 8.89 |
| v54 | **v160** | 5 | 4,021 | **8** | **.0020** | **.0000** | 53.4 | 7.20 |
| v54 | v161 | 10 | 8,062 | 834 | .1034 | **.1973** | 69.4 | 7.00 |
| v55 | v161 | 5 | 3,303 | 83 | .0251 | .0501 | 51.8 | 6.31 |
| v55 | v162 | 15 | 13,627 | 855 | .0627 | .0946 | 64.9 | 8.28 |

**⇒ The cells do not order by our proximity dose.** The two highest-exposure cells (8.89 and
8.28 entities-in-vision) sit at post-r102 rates of .085 and .095, **below** the 7.00-exposure
cell's **.197**. Our build volume orders better (Spearman ρ = 0.8 over 5 cells) but with
**n = 5 cells** and each cell confounded with game length, their economy and their own
version, this is not evidence — and the 15-opponent panel in §4(c), which is the same
comparison at 3× the resolution, reads **r = +0.086**.
**⇒ The v160 zero (0 latches in 2,031 post-r102 builder-rounds) is the single most
dose-shaped number in this study and it is 5 games.** Not bankable.

---

## 6. WHAT THIS REFUTES / AMENDS IN THE STUDY'S PIECE E

**Reproduced exactly, no correction needed:** 993 (v54) + 938 (v55) = **1,931** TLE'd
unit-rounds over 40 games; **100% builder bots**; **0 for us**; game-level
r(our builds, their TLEs) = **0.571** here vs the study's 0.589 (build-event definition
differs slightly — I count `placeEntity` by the other team); r(turns, TLEs) = 0.446 exactly
as reported.

**⛔ REFUTED — "AND THE RATE TRACKS *OUR* BUILD VOLUME" (the piece's headline).** Every
within-game estimator is null or negative (§3.1–3.4) and the between-opponent panel is flat
(§4c). The piece's own hedge — *"⚠ EYEBALL on the CAUSAL step"* — was correct, and the causal
step does not survive.

**⛔ REFUTED — the piece's CONTROL.** It reads: *"the direction must be able to invert and
does not — the same decoder reads 0 TLEs for our units in all 215 games."* That establishes
the TLE column is not constant; it does **not** establish that the *dose relation* cannot
invert. **It can and does: Besvikomat (94.8 builds/game) and sporks (114.2) both produce
0.0000**, against our 64.3 → 0.0595. **A control on the outcome column is not a control on
the correlation.**

**⚠ AMENDED — "~48 TIMES A GAME".** True as a mean; the **median is 0**, **23 of 40 games
(58%) have zero**, and **top-5 games hold 62.3%**. The per-game distribution is
zero-inflated and the mean is not a description of a typical game.

**⚠ AMENDED — the length normalisation was insufficient, and mechanically so.** The
length-normalised 0.330/0.331 the piece reports treats TLEs as a per-round rate; but
**TLE count ≈ Σ over latches of (turns − latch_round)** — a post-latch accumulator whose
length is the *residual game*, which is itself a function of total turns.
**Measured: r(Σ(turns − latch_round), TLE count) = 0.879 US / 0.887 TP, R² = 0.77 / 0.79.**
Three-quarters of the game-level variance the correlation was computed on is a single
latch event times the game's remaining length.

**⚠ AMENDED — the mechanism guess.** The piece proposes *"a per-turn scan over nearby
entities/tiles… exactly what a 10ms budget punishes"* and the brief operationalises it as
"visible-entity count". **Half right:** the scan is real and it is over **THEIR OWN**
entities (`vis_focus`: +47 µs/entity US, +32 µs TP on `exec_us`, within (game,round) FE).
**Our entities do not enter it** (−82 µs / −23 µs, i.e. the wrong sign). **We cannot buy
their compute by standing cheap things in their vision.**

---

## 7. THE ONE CHANNEL WE CONTROL — SIZE, AND WHAT IT IS WORTH

**Dose definition with the largest within-game effect: `vis_turret` — the count of OUR
turrets (gunner/sentinel/launcher) inside a Flotte builder's vision (r²≤20), measured at
round start, on their HOME builder.**

**Effect on the latch hazard** (FE = game × round, `vis_focus` and `near_theircore`
controlled, SE clustered by game):
* **US: +1.26e-3 latches per (turret × builder-round)**, against a baseline hazard of
  7.16e-4 — **~2.7× the baseline per turret.** 21 events, 40 games.
* **TP: +1.66e-4**, baseline 2.88e-4 — **~1.6× per turret.** 100 events, 365 games.

**Converted to the brief's requested unit — TLE'd builder-rounds per unit of dose** (hazard
× TLE'd rounds per latch, 92 US / 132 TP):
* **US: 0.113 TLE'd builder-rounds per (turret × builder-round of exposure)** —
  i.e. **100 builder-rounds of one extra turret in vision buys ≈ 11 frozen builder-rounds.**
* **TP: 0.022** — ≈ 2 per 100. **The US figure is 5× the TP figure and rests on 21 events;
  treat the TP figure as the conservative estimate.**

**Current exposure, and why the channel is untouched:** across our 40 rated games Flotte
builders spend **32.7%** of their rounds with ≥1 of our turrets in vision (mean
`vis_turret` = **0.381**), and only **0.55%** with ≥3. The third-party average is **higher**
than ours (mean 0.505, ≥3 in 3.66% of rounds). **We are currently below the field on the one
dose that works.**

⚠ **WHAT I CANNOT SEPARATE, and it matters for arm design.** Within (game, round) I compare
their four builders, so reverse causation and game-state selection are excluded, and
`vis_focus` + `near_theircore` absorb "this is the home builder in a dense base". What
remains is two readings of the same coefficient: **(i)** their per-turn code runs an
expensive branch when a hostile turret is *in sensing range* (threat evaluation,
line-of-fire, retreat pathing), or **(ii)** their builder is *under fire and repairing*,
and the repair branch is what costs. **Both are "our play causes it" and both imply the same
arm**, but they price differently — (i) is bought with a cheap turret merely *present*,
(ii) requires ammo and actual shooting. The archive cannot tell them apart, because we never
place a forward turret and then decline to fire it.

---

## 8. WHAT A WEAPON ARM WOULD HAVE TO DO — and the honest prior

The arm is **not** "build more stuff near them" (§3, refuted) and **not** "throw their
builders" (§4e, non-channel at current dose). It is: **place a turret so that Flotte's HOME
builders sit inside its vision radius, early, and keep it alive.** Concretely, that means a
forward gunner/sentinel planted at d²≈20–36 of THEIR core rather than the current siege
standoff of d²25–41 (study piece F), aimed at maximising `vis_turret` for the builders
working their base — with the ≥3 threshold as the aggressive target, since the crude TP form
puts the jump there (1.95e-3 vs 3.6e-4). The discriminating pre-registration is **turret
placed and NOT fired vs turret placed and fired**, which separates reading (i) from reading
(ii) and is the only thing the archive cannot answer. **Falsifier: Flotte's latch count per
game does not rise vs a matched control arm.**

**⚠ AND THE PRIOR IS NOT GOOD, so it should be written into the prereg before the leg, not
after.** At the conservative (TP) effect size, moving their home builders from 0.4 to 2.0
turrets-in-vision for 100 builder-rounds buys **≈ 0.03 extra latches/game**; at the
optimistic (US) size, **≈ 0.20/game** — a one-in-five chance of freezing one of their four
builders. **That is a rounding error against the cost of a forward turret that dies** (our
sentinels already die 45 times per 40 games, piece F), and against the fact that the same
forward turret is being bought anyway for the kill. **The arm's case is that it is a free
rider on a turret we already want to place, chosen for WHERE it stands rather than for
whether it exists** — never as a plank funded on its own. Under `PROGRAMME.md` the bar is
`DEFENCE_ADMISSION_BAR`-adjacent: a forward turret placed for compute denial that does not
also open the lane to their core is r300-risking, and this decode does not come close to
justifying that trade.

---

## 9. WHAT WOULD CHANGE THE VERDICT

1. **Their code changing at r102.** The whole latch mass keys off a round constant in a
   frozen v54/v55. A Flotte version that moves or removes it invalidates §2 and most of §1.
   Re-run this decode against any new Flotte version before spending a leg.
2. **A high-dose displacement test.** 40 throws across 40 games is too few to say anything;
   §4(e) is a non-test. If an arm ever throws their builders at volume, re-read it.
3. **The ≥3-turret threshold.** 6 events (TP) and 1 (US) in the top cells. A leg that
   deliberately parks 3+ turrets in a home builder's vision would resolve linear-vs-threshold
   in one window.
4. **The v160 cell.** 0 latches in 2,031 post-r102 builder-rounds across 5 games is the one
   number in this decode that a dose story fits and an artifact story does not explain.
   `git log` on our v159→v160→v161 bot diff, read against `vis_turret` per version, is a
   free next step and is **not** done here.

---

## LEDGER ROW

```
2026-08-20  DECODE  QUEUE#98  flotte-TLE-dose  ARTIFACT(build-volume dose) / CAUSAL(turret-in-vision dose, small)
  estimator: matched case-control on 21(US)/100(TP) latch events + discrete-time hazard, (game x round) FE, game-clustered SE
  surfaces: 40 rated games / 32,434 builder-rounds (us) + 365 archived games / 367,565 builder-rounds (15 third-party opponents)
  refutes: REPLAY-STUDY-flotte-v55-2026-08-20.md piece E causal claim + its stated control
  winning dose: vis_turret, +1.26e-3 (US) / +1.66e-4 (TP) latch-hazard per turret-builder-round = 0.113 / 0.022 TLE'd builder-rounds per unit dose
```
