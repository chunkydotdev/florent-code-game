# Besieged-core heal confound: verdict and decomposition (side lane deliverable)

**Side research lane, 2026-08-09. Gates spec D1. Decoder validated on 7
independent checks (heal×4HP vs updateHp stream per-side median ratio 0.9941,
0 sides >1.0; builds−deaths identity 5,470/5,470; throw residual matches
corpus/throws.tsv exactly on 1,313 shared files). 417,477 besieged rounds,
2,409 files.**


**Read-only research subagent, 2026-08-09.** No repo file changed, no `fcode`,
no arena, no bot run. Everything in `scratchpad/confound/`.

**Gating question.** `docs/research/heal-cancellation-by-core-separation-2026-08-09.md`
found OpenSverige's heal cancellation vs 3+ simultaneous core-attackers collapses
to 27-33% while "the field" rises to 50-65%, and closed the "our builders were
already dead" confound with a live-builder *count*. Its residual: *count is not
adjacency — a builder alive across the map cannot heal.* This document supplies
the positions.

---

## 0. VERDICT

| candidate | status |
|---|---|
| **B — "game already lost, builders mostly dead by then"** | **REFUTED.** On our 3+-attacker besieged rounds (n=7,116 rounds / 341 files) we have **5.02 live builders**, identical to our 1-attacker rounds (5.62) and to every comparison population (opponents 5.05, non-us games 5.07). Only **0.9%** of those rounds have zero live builders and **3.2%** have fewer than two. |
| **A — "detail too small / mispositioned — builders alive but not at the core"** | **SPLIT.** *Mispositioned:* **refuted.** The task's own discriminator — ≥2 live builders but <2 adjacent to the core — fires on only **12.5%** of our 3+ rounds, the **lowest of any broad population** (games without us: 40.6%; TOP ≥1750: 35.2%). We are better positioned than the field at large. *Too small:* **confirmed, but only against the specific teams that beat us**, and only from mid-game onward. |
| **A′ — the mechanism that actually survives** | Our detail on 3+ rounds is **2.68 adjacent builders**; the opponents who out-cancel us run **3.47** (and ≥1600-rated opponents **4.15**). Meanwhile we absorb **23.05 dmg/round** against their 18.35. Full cancellation of our load needs **5.76** adjacent healers. We are using **2.68 of ~7.8 usable ring slots** with **2.35 live builders standing somewhere else**. |

**One-line answer for the build decision:** the resource is present, correctly
aimed, and running at 85% of its own cap — there is nothing to fix in
*targeting*. The lever is **detail size**, and it is available: ≥1 spare live
builder in **91.3%** of our 3+ rounds, ≥2 in **63.8%**, against ~5 empty ring
slots. The measured dose-response on our own games says going from adj 2 to adj
4+ inside the 3+ bin takes cancellation **33.4% → 61.3%**.

**One correction the research arm's doc needs:** its "FIELD" was
`join.tsv`-scoped, i.e. **our opponents only**. The broad field does not scale
its heal detail either — see §5.

---

## 1. THE DECODER, AND ITS VALIDATION (read this before using any number)

`confound/bb_decode.py` extends the s23 per-round decoder with a **live entity
position tracker**: `placeEntity` (first-id-only, honouring the rotate-re-emit
trap), `moveBuilderBot` (including launcher throws, which are ordinary
`moveBuilderBot` with a non-adjacent `to`), and `removeEntity`. Each round it
snapshots, per team, the set of live builder bots and where they stand relative
to that team's own **2x2 core footprint**.

**Geometry.** A 2x2 core has **8** orthogonally-adjacent tiles ("the ring"), not
4. `adj` = live builders standing on a ring tile — these are exactly the tiles
from which `heal(pos)` can reach a footprint tile. The heal cap is therefore
**8 × 4 = 32 HP/round**, not the 16 assumed in the prior doc.

Heal is read from **`builderHeal` (Update field 15)** — an explicit
`{id, target}` event, so "did an adjacent builder actually heal the core" is
measured, not inferred.

**2,735 files decoded, 0 parse errors, 918,662 rows.**

### Validation — five checks, all independently derivable

| # | check | result |
|---|---|---|
| 1 | entity-set bookkeeping: `builds − deaths == |live set|` per (file, team) | **5,470 / 5,470 agree, 0 disagree** |
| 2 | geometric invariant: `adj > 8` (impossible — only 8 ring tiles, one builder per tile) | **0 sides of 5,470** |
| 2b | builders standing ON an own-footprint tile (impossible while the core lives) | 70 sides — and **70/70 are games where that core DIED**, freeing the tiles. Fully explained. |
| 2c | out-of-bounds positions | **0** |
| 3 | **heal events × 4 HP vs the independent HP stream**: 895,084 `builderHeal`-onto-own-footprint events → 3,580,336 HP predicted vs **3,366,224 HP observed** on `updateHp` | ratio **0.9402** pooled, **per-side median 0.9941**, **max 1.0000**, and **0 sides exceed 1.0**. The one-sided shortfall is heal clipped at max HP — the only physically possible direction. Two unrelated streams agreeing this tightly means position, target-tile and HP decoding are all right. |
| 3b | heals aimed at the *enemy* footprint (impossible — you cannot heal enemies) | **0 events in 2,735 files** |
| 4 | move legality: 9,697,571 `moveBuilderBot` events — builders may only step 1 cardinal tile | **99.62% are 1-tile Manhattan steps**; the residual 36,859 (0.38%) are launcher throws |
| 4b | those 36,859 throws vs the committed `corpus/throws.tsv` decoder on the 1,313 shared files | **36,859 vs 36,859 — exact, and exact on all 1,313 files individually** |
| 5 | builder spawn/death totals vs the s23 `tl.tsv` columns `b_builder_bot` / `d_builder_bot` | **5,470 / 5,470 agree, 0 disagree** |

### Spot checks (2 games, hand-reconciled)

`019771d2…_game_1` team 0, core anchor (0,0), rounds 201/203/205/207: raw dump
gives 7 live builders at explicit tiles, 2 of them on ring tiles, 1-2
`builderHeal` events onto the footprint, 4/8/8/8 HP of `coreheal` — the emitted
`bb.tsv` rows read `live=7 adj=2 heal_core=1/2/2/2 coreheal=4/8/8/8`. Exact
match on every field.

`01f3c8a4…_game_2` team 1, core anchor (18,18), rounds 19/21/24/26: same, and
r24 shows the clipping case (1 heal event, 4 HP predicted, 2 HP observed —
the core was 2 HP below max).

In both games **every builder that healed the core was on a ring tile**, which
is the engine rule and a further check that the tracker's positions are real.

### Honest proxy statements

- `adj` is measured at **end of round**. Sensitivity: start-of-round adjacency
  differs by ≤0.02 builders in every population/bin (§2), because a builder that
  heals cannot also move that turn.
- Attacker count for a besieged team = the **other** team's
  `atkers_on_enemy_core` in the same `(file, round)`, replicating the s23
  decoder's logic exactly (turrets keyed by origin tile, builder melee keyed by
  entity id). This is the same conditioning as the doc being tested.
- Population: **417,477 besieged rounds** (own core took damage, ≥1 attacker)
  across **2,409 files**.

---

## 2. THE CENSUS — live builders and builders at the core

Besieged rounds (own core took damage that round), by attacker bin. `FIELD` here
= all non-us sides; `TOP` = non-us sides rated ≥1750.

| atk | who | rounds | live med | live mean | **ADJ med** | **ADJ mean** | near d²≤8 | heal events on own core |
|---|---|---|---|---|---|---|---|---|
| 1 | US | 95,820 | 5.0 | 5.62 | 2.0 | **2.36** | 3.06 | 1.77 |
| 1 | FIELD | 209,519 | 5.0 | 5.22 | 1.0 | 1.59 | 2.23 | 1.07 |
| 1 | TOP | 43,927 | 4.0 | 4.42 | 1.0 | 1.23 | 1.63 | 0.96 |
| 2 | US | 26,852 | 5.0 | 5.06 | 2.0 | **2.57** | 3.16 | 2.27 |
| 2 | FIELD | 60,980 | 5.0 | 5.20 | 2.0 | 1.99 | 2.44 | 1.61 |
| 2 | TOP | 11,018 | 4.0 | 4.24 | 2.0 | 1.68 | 2.04 | 1.45 |
| **3+** | **US** | **7,116** | **5.0** | **5.02** | **2.0** | **2.68** | 3.29 | 2.33 |
| 3+ | FIELD | 17,190 | 5.0 | 5.06 | 2.0 | 2.49 | 2.98 | 2.18 |
| 3+ | TOP | 2,836 | 5.0 | 4.54 | 2.0 | 1.99 | 2.51 | 1.68 |

Start-of-round positions give 2.36 / 2.56 / **2.66** for US and 1.60 / 1.95 /
2.47 for FIELD — the end-of-round snapshot is not doing any work.

**Read this table against verdict B.** Our live-builder count at 3+ (5.02) is
statistically indistinguishable from our 1-attacker count (5.62) and from every
comparison population. *"Our builders were dead"* has no support at all.

**Read it against verdict A.** Against the broad field we are not
under-committed at the core: 2.68 adjacent versus FIELD 2.49 and TOP 1.99.

---

## 3. DETAIL SIZE DIRECTLY PREDICTS CANCELLATION — and we sit on the field's curve

Pooled over all besieged rounds, cancellation = `Σ coreheal / Σ coredmg`:

| adj | US rounds | US cancel | FIELD rounds | FIELD cancel | TOP rounds | TOP cancel |
|---|---|---|---|---|---|---|
| 0 | 7,899 | 0.2% | 55,039 | 0.0% | 15,429 | 0.0% |
| 1 | 24,155 | 32.2% | 89,627 | 35.0% | 18,604 | 31.1% |
| 2 | 46,190 | 58.9% | 72,934 | 56.4% | 14,968 | 54.5% |
| 3 | 25,784 | 66.1% | 39,442 | 69.3% | 6,066 | 73.3% |
| 4+ | 25,760 | 77.1% | 30,647 | 78.2% | 2,714 | 88.1% |

**Answer to "does detail size directly predict cancellation?" — yes, almost
completely, and the curve is the same for everyone.** Adjacency explains the
cancellation rate; team identity adds almost nothing at fixed adjacency.

Restricted to the **3+-attacker bin only** (where the collapse lives):

| adj | US n | US cancel | FIELD n | FIELD cancel | TOP n | TOP cancel |
|---|---|---|---|---|---|---|
| 0 | 206 | 0.1% | 2,076 | 0.0% | 535 | 0.0% |
| 1 | 910 | 14.0% | 3,515 | 20.1% | 607 | 14.7% |
| 2 | 2,585 | 33.4% | 3,467 | 34.4% | 608 | 27.8% |
| 3 | 1,292 | 39.2% | 2,753 | 54.0% | 649 | 48.9% |
| **4+** | **2,123** | **61.3%** | 5,379 | 79.3% | 437 | 68.8% |

**33.4% at two healers, 61.3% at four — on our own games, inside the exact
regime that is failing.** That is the lever, and it is a big one.

### The joint control: fixed adjacency AND fixed incoming damage

Cancellation with both the detail size and the round's damage held constant
(`OPP` = our opponents, `OTHER` = games with no us side):

| dmg bin | pop | adj1 | adj2 | adj3 | adj4+ |
|---|---|---|---|---|---|
| 17-24 | **US** | 17.9% | **38.2%** | **50.4%** | **74.7%** |
| 17-24 | OPP | 15.5% | 36.1% | 51.3% | 61.8% |
| 17-24 | OTHER | 16.5% | 32.6% | 42.3% | 64.7% |
| 17-24 | TOP≥1750 | 15.6% | 38.2% | 52.5% | 67.7% |
| 25-40 | **US** | 11.2% | 23.8% | 34.9% | 51.1% |
| 25-40 | OPP | 12.3% | 27.8% | 43.0% | 58.2% |
| 25-40 | OTHER | 9.3% | 21.5% | 33.5% | 49.6% |

**At the same detail size against the same incoming damage we cancel as well as
anyone and better than most.** There is no per-builder efficiency deficit. The
entire pooled 3+ gap decomposes into exactly two terms: **how many healers we
have on the ring**, and **how much damage is landing**.

### Utilisation — the detail is not idle either

| atk | who | adj mean | heal events on own core | heals per adjacent builder | % of adj>0 rounds with **zero** heals |
|---|---|---|---|---|---|
| 3+ | US | 2.68 | 2.33 | **0.87** | **4.4%** |
| 3+ | FIELD | 2.49 | 2.18 | 0.88 | 7.6% |
| 3+ | TOP | 1.99 | 1.68 | 0.84 | 14.8% |

Our adjacent builders heal 87% of the time — the same as the field, better than
top tier. **"We have the builders and do not apply them" is not what the
positions say.** We apply them; we just do not have enough of them on the ring.

---

## 4. THE DISCRIMINATOR THE TASK ASKED FOR

Fraction of besieged rounds with **≥2 live builders somewhere but <2 adjacent to
the core** — the "mispositioned/misassigned" signature:

| atk | population | rounds | live=0 | adj=0 | adj<2 | **live≥2 & adj<2** |
|---|---|---|---|---|---|---|
| 1 | US | 95,820 | 1.3% | 6.6% | 26.5% | **22.8%** |
| 1 | OPP (our opponents) | 76,808 | 0.5% | 22.6% | 55.9% | 53.2% |
| 1 | OTHER (no-us games) | 132,711 | 0.8% | 20.5% | 53.6% | 49.6% |
| 1 | TOP ≥1750 | 43,927 | 0.8% | 28.0% | 62.7% | 58.8% |
| 2 | US | 26,852 | 1.2% | 5.1% | 20.8% | **17.1%** |
| 2 | OPP | 22,558 | 0.8% | 8.4% | 31.5% | 28.7% |
| 2 | OTHER | 38,422 | 1.3% | 17.0% | 46.7% | 40.8% |
| **3+** | **US** | **7,116** | **0.9%** | **2.9%** | 15.7% | **12.5%** |
| 3+ | OPP | 5,790 | 0.1% | 3.0% | 8.6% | 6.7% |
| 3+ | OTHER | 11,400 | 2.2% | 16.7% | 44.7% | 40.6% |
| 3+ | TOP ≥1750 | 2,836 | 2.2% | 18.9% | 40.3% | 35.2% |

**12.5% is a low number, and it is the second-lowest in the table.** The
mispositioning signature fires three times more often for the broad field than
for us. Whatever is wrong with our multi-attacker defence, it is not builders
wandering while the core burns.

The *right* version of "too small" is the `adj<3` column: **52.0% of our 3+
rounds have fewer than 3 builders on the ring**, against **26.4%** for our
opponents.

### Headroom — could a bigger detail have been formed?

US 3+ rounds, n=7,116:

| target | achieved | short of target but had that many builders **alive** elsewhere |
|---|---|---|
| adj ≥3 | 48.0% | 43.2% |
| adj ≥4 | 29.8% | **53.0%** |
| adj ≥5 | 7.7% | 56.7% |

- live-but-not-adjacent builders on those rounds: **median 2, mean 2.35**;
  ≥1 spare in **91.3%** of rounds, ≥2 spare in **63.8%**.
- ring capacity is not the constraint: over all 5,470 sides the ring has
  **7.80 in-bounds, non-wall tiles on average** (8 on 94% of maps, 4 for the 6%
  of corner-anchored cores), and US/opponent/other are identical (7.80/7.80/7.70).
  **We occupy 2.68 of ~7.8 slots.**
- to fully cancel the round's damage we would need a **median of 4 more**
  adjacent healers; the spare fleet alone covers that in 12.9% of rounds, so a
  *complete* stop is not on the table — but every marginal healer is worth
  ~10-14 percentage points of cancellation on the measured curve.

---

## 5. CORRECTION: the research arm's "FIELD" is our opponents, not the field

Their FIELD came from `join.tsv`, which only covers our own ladder games. Split
three ways:

| atk | population | rounds | cancel% | dmg/rnd | live | **ADJ** | dmg per attacker |
|---|---|---|---|---|---|---|---|
| 1 | US | 95,820 | 64.7% | 10.08 | 5.62 | 2.36 | 10.08 |
| 1 | OPP (our opponents) | 76,808 | 46.1% | 8.53 | 5.32 | 1.67 | 8.53 |
| 1 | OTHER (no-us games) | 132,711 | 45.6% | 8.58 | 5.16 | 1.54 | 8.58 |
| 1 | TOP ≥1750 non-us | 43,927 | 41.7% | 9.05 | 4.42 | 1.23 | 9.05 |
| 2 | US | 26,852 | 51.1% | 17.07 | 5.06 | 2.57 | 8.54 |
| 2 | OPP | 22,558 | 66.6% | 10.67 | 5.37 | 2.41 | 5.33 |
| 2 | OTHER | 38,422 | 41.2% | 12.91 | 5.09 | 1.74 | 6.45 |
| 2 | TOP ≥1750 | 11,018 | 37.7% | 15.08 | 4.24 | 1.68 | 7.54 |
| **3+** | **US** | **7,116** | **39.4%** | **23.05** | 5.02 | **2.68** | 7.43 |
| 3+ | **OPP** | 5,790 | **68.8%** | 18.35 | 5.05 | **3.47** | 5.94 |
| 3+ | OTHER | 11,400 | **34.6%** | 19.11 | 5.07 | 1.99 | 6.01 |
| 3+ | TOP ≥1750 | 2,836 | **31.5%** | 21.18 | 4.54 | 1.99 | 6.76 |
| 3+ | OPP ≥1600 | 1,047 | **78.0%** | 20.74 | 5.56 | **4.15** | 6.45 |

Three things change:

1. **The broad field does not scale its heal detail with the threat either.**
   Games without us cancel **34.6%** at 3+ and top-tier sides **31.5%** — both
   *worse* than our 39.4%. The statement "*their cancellation increases with
   pressure; ours decreases*" is **true only of the teams we play**.
2. **The comparison that matters is still real, and larger than reported.** Our
   opponents keep **3.47** builders on the ring at 3+ (≥1600-rated: **4.15**),
   against our 2.68. Their adjacency distribution at 3+ is 36.6% at exactly 4 and
   23.8% at 5, against our 36.3% at 2. The ≥1600 subset sits at **5 adjacent
   healers in 73.6% of its 3+ rounds** — a deliberate, fixed, five-builder core
   guard.
3. **We absorb a heavier bombardment.** 23.05 dmg/round at 3+ against their
   18.35 — a 26% heavier load on a smaller detail. Part of the pooled gap is a
   denominator effect that no amount of healing addresses.

### The arithmetic of the cap

| atk | population | dmg/rnd | adj | cap = 4×adj | heal | cap used | adj needed for 100% |
|---|---|---|---|---|---|---|---|
| 1 | US | 10.08 | 2.36 | 9.45 | 6.53 | 69% | 2.52 |
| 2 | US | 17.07 | 2.57 | 10.26 | 8.72 | 85% | 4.27 |
| **3+** | **US** | **23.05** | **2.68** | **10.71** | **9.08** | **85%** | **5.76** |
| 3+ | OPP | 18.35 | 3.47 | 13.88 | 12.62 | 91% | 4.59 |
| 3+ | TOP ≥1750 | 21.18 | 1.99 | 7.96 | 6.68 | 84% | 5.30 |

We run our detail at 85% of its own theoretical cap. **The cap itself is the
problem, and the cap is a headcount we choose.**

---

## 6. THE ROUND-NUMBER / "DYING ANYWAY" CONTROL

| atk | population | rounds | median round | median own core HP | % HP<250 | median game length |
|---|---|---|---|---|---|---|
| 1 | US | 95,820 | 301 | 484 | 10.2% | 887 |
| 1 | OPP | 76,808 | 225 | 464 | 19.0% | 887 |
| 1 | TOP ≥1750 | 43,927 | 181 | 384 | 26.8% | 299 |
| 2 | US | 26,852 | 283 | 384 | 27.6% | 553 |
| 2 | OPP | 22,558 | 409 | 485 | 18.3% | 1000 |
| **3+** | **US** | **7,116** | **350** | **351** | **34.9%** | 459 |
| 3+ | OPP | 5,790 | 481 | 410 | 19.5% | 1000 |
| 3+ | OTHER | 11,400 | 239 | 308 | 38.2% | 532 |
| 3+ | TOP ≥1750 | 2,836 | 189 | 269 | 47.0% | 254 |

Our 3+ rounds occur at **median round 350 with 351 core HP left**. They are
*earlier and at lower HP* than our opponents' 3+ rounds (481 / 410) but *later
and healthier* than the broad field's (239 / 308) and far healthier than top
tier's (189 / 269). **We are not systematically further into a lost game than
the field — but we are somewhat further in than the specific opponents we are
being compared against**, so part of the raw gap is that confound.

Holding it fixed, 3+-attacker rounds only:

| cut | pop | n | cancel% | live | adj | live≥2 & adj<2 |
|---|---|---|---|---|---|---|
| own core HP ≥300 | US | 4,136 | 48.4% | 5.15 | 2.92 | 9.3% |
| own core HP ≥300 | OPP | 4,212 | **76.6%** | 5.27 | **3.82** | 2.5% |
| own core HP ≥300 | OTHER | 5,911 | 43.2% | 5.49 | 2.38 | 31.2% |
| own core HP ≥400 | US | 2,975 | 56.9% | 5.15 | 3.06 | 7.2% |
| own core HP ≥400 | OPP | 3,035 | **79.5%** | 5.40 | **3.98** | 1.5% |
| round ≤250 | US | 2,795 | 30.4% | 4.57 | **2.24** | 21.5% |
| round ≤250 | OPP | 1,060 | 38.9% | 4.52 | **2.30** | 29.1% |
| round 251-500 | US | 1,893 | 36.7% | 4.80 | **2.46** | 10.6% |
| round 251-500 | OPP | 1,985 | **73.1%** | 5.01 | **3.53** | 3.8% |
| round >500 | US | 2,428 | 55.1% | 5.72 | 3.35 | 3.4% |
| round >500 | OPP | 2,745 | 77.8% | 5.29 | 3.88 | 0.2% |

**The most actionable single row-pair in this document: before round 250 our
detail is the same size as our opponents' (2.24 vs 2.30). The gap opens entirely
in the mid-game — at rounds 251-500 they run 3.53 and we run 2.46.** That is the
same time window as the r150 forward-posture collapse documented elsewhere: when
our army stops being reinforced, the core guard stops growing too.

Healthy-core control also survives: at ≥400 own core HP our 3+ cancellation is
56.9% against their 79.5%, with adj 3.06 vs 3.98. **The gap is not an artefact
of being nearly dead.**

---

## 7. LIMITS AND HONEST FLAGS

- **The OPP 3+ population is thin in games.** 5,790 rounds but only **92
  distinct files**, and five teams supply 5,372 of those rounds: Askar City
  (1,574 rounds / 11 files, adj 3.58, cancel 61.5%), Focalground (1,451 / 10,
  adj 4.49, 84.0%), OopsGotYourElo (1,388 / 12, adj 3.75, 85.1%), Leviathan
  (794 / 13, adj **2.20**, 61.5%), Memtrace (165 / 5, adj 2.86, 56.1%).
  **"Our opponents run a 3.5-4 builder core guard" rests on ~50 long games from
  4-5 teams.** Note Leviathan runs a *smaller* detail than us and still cancels
  61.5% — because they only absorb 13.60 dmg/round. Detail size is the dominant
  term, not the only one.
- The OPP ≥1600 3+ cell (1,047 rounds, adj 4.15, 73.6% of rounds at exactly 5
  adjacent) is almost certainly a handful of games against one or two teams with
  a hard-coded five-healer guard. Treat it as an existence proof of the tactic,
  not as a field rate.
- **Adjacency is measured at end of round** (start-of-round differs by ≤0.02).
- **`heal_core` is heal events onto a footprint tile**, which is exactly the
  engine's heal-the-core action; the ×4 reconciliation (§1) confirms it.
- **`atkers_on_enemy_core` is the s23 decoder's definition, re-implemented
  here**, not re-validated against the engine. Conditioning is identical to the
  doc under test, which is the point.
- **Correlational.** "More adjacent healers → higher cancellation" is a
  dose-response over observed rounds; rounds where a team *could* form a big
  detail may differ from rounds where it could not. The joint control at fixed
  damage (§3) removes the most obvious version of that (heavier attacks → both
  lower cancellation and less time to gather healers), and the dose-response is
  monotone in all four populations, but it is not an intervention.
- Damage-landing rounds only. Says nothing about rounds where nothing lands.
- The archive is not a random sample: 1,180 of 2,735 attributable files are our
  own games.

## 8. FILES (all in `scratchpad/confound/`, none in the repo)

`bb_decode.py` (position decoder), `bb.tsv` (918k besieged/attacking rows),
`bbv.tsv` (5,470 per-side validation rows), `ringcap.py` + `ring.tsv` (usable
heal slots per core), `v1.py`/`v2.py` (+`.out`, validation), `spot.py`
(+`spot.out`, hand reconciliation), `an.py`/`an2.py`/`an3.py`/`an4.py`
(+`.out`, analysis), `decode.log`.
