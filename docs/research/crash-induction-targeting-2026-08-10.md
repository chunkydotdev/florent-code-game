# Is the undamaged-removal carrier list a crash-induction target list? — the adversary-proximity cut

**Research arm, session 30, decoded 2026-08-10 (`date -u` at start of decode:
`2026-08-10T04:05:34Z`; repo head at write time `b0728b3`). Read-only cut. No bot, arena,
prereg, submission or coordination file touched — corpus/replay reads and local analysis
only.**

Sibling to `undamaged-builder-deaths-2026-08-10.md` (which produced the carrier list) and
`idle-round-envelope-2026-08-10.md` (which established that turn-loss is invisible).

---

## 0. THE ANSWER IN SIX LINES

**The pre-registered branch that landed is "correlates only with own-state" — the carrier
list is RETIRED as a crash-induction instrument. Do not build the trigger.**

**The number that decided it: for the four teams carrying 2,401 of the field's 2,665
undamaged mid-game builder removals (90.1%), the per-round hazard of an undamaged removal is
224.06 per 10,000 builder-rounds on a MAP-BORDER tile and 0 in 2,334,017 non-border
builder-rounds — including 0 in 296,387 rounds spent in orthogonal/diagonal contact with an
enemy unit.** Rule of three puts the non-border hazard below 0.0129/10k, a ratio of ≥17,000×.

**The brief's dichotomy is incomplete and this is the highest-value thing in the document:
the gate is neither adversary-state nor the recycling covariates the brief named. It is
MAP-BOUNDARY state** — `x==0 or y==0 or x==W-1 or y==H-1`, a covariate that is a property of
the map and the unit's own path, and that an adversary can reach only through a launcher
throw the corpus has never once recorded against these teams.

**One carrier does land on the adversary branch and it is named, not promoted: `Cookie`**
(119 events, 4.5% of the field category, one team, 210 games). **It is not a target list —
its hazard next to the enemy core is 6.13 per 10,000 builder-rounds over 117,491 such
rounds, i.e. one event per 1,632 rounds spent adjacent to the enemy core.** §7 names the
fixture that would decide it.

**And the falsifier came out clean: the classifier is not broken.** 94.90% of the 2,665
undamaged removals carry NO HP event at all in their entire life; 97.75% read exactly
`spawn_hp`. For `vjg` alone: 96.57% and 99.01%.

---

## 1. THE FALSIFIER CHECK — RUN FIRST, REPORTED FIRST

**Question:** do `vjg`'s "undamaged" removals in fact carry preceding negative HP deltas? If
so, the classifier is broken and both this cut and §1 of the parent fall.

**Answer: no. The classifier holds.**

Independent re-decode, not a reuse of the parent's script: per builder bot, spawn HP from
`PlaceEntity`, then the FULL signed `UpdateHp` ledger over the whole game (defeating the S1
ordering trap), `delta` decoded as a sign-extended 64-bit varint (TRAP 2), a build being the
FIRST `placeEntity` carrying an id (TRAP 3).

**Population: `pop_field.tsv`, sha256 `2fed2b0db2bd5bf9` — 5,140 games / 1,028 matches / 70
teams; `triggeredBy == ladder`, neither side us (`379a5d80-…`), neither side
`opensverige - plan B` (`b7cafd9f-…`). Decode completeness 5,140/5,140 files, 0 errors.**

| check, on **undamaged mid-game builder removals** | ALL (n=2,665) | `vjg` only (n=1,517) |
| --- | ---: | ---: |
| any negative HP delta anywhere in the unit's life | 136 (**5.10%**) | 52 (**3.43%**) |
| any positive delta (a heal) anywhere in its life | 92 (3.45%) | 44 (2.90%) |
| **NO HP event at all, whole life** | **2,529 (94.90%)** | **1,465 (96.57%)** |
| `hp_at_removal == spawn_hp` | 2,605 (**97.75%**) | 1,502 (**99.01%**) |

**And the complement group comes out the other way, which is the point.** Damage-killed
mid-game removals (n=23,786): **100.00%** carry at least one negative delta, and the modal
reconstructed HP at removal is **−2** (14,729 of them) — a 40 HP builder taking six gunner
shots of −7. `vjg`'s own 58 damage-killed removals: 100.00%, same shape.

**Third check on the decode itself:** the field-wide builder delta alphabet is
`{−18: 23,364, −7: 142,659, +1: 666, +2: 1,977, +3: 8,200, +4: 50,077}` — sentinel, gunner,
and clamped heals; **no −2, and no ~1.8e19 values**, independently reproducing the parent's
alphabet and confirming the sign-extension is right. Read unsigned, every negative would
appear as ~1.8e19 and the census would invert.

**One correction to how the parent's category should be read.** "Undamaged" means *removed
holding positive HP*, not *never touched*: **5.10% of the category took damage earlier in
life and was healed back above zero.** Nothing in the parent depends on this, but a reader
who takes "undamaged" to mean "never in contact" will over-read it.

**Census reproduction.** On my larger population the parent's per-team structure reproduces:
2,665 undamaged of 26,451 mid-game builder removals (**10.08%**, parent: 10.35% on 4,870
games), 13 distinct teams with ≥1, top-1 team 56.9%, top-3 80.9%, **46 teams with ≥200
mid-game removals of which 36 sit at exactly zero (78%)**.

---

## 2. THE TABLE — the discriminator, per carrier

**Subject: builder-bot removals and builder-bot ROUNDS of one named team.
Unit: one removal, and one (builder, round) pair. Population: that team's third-party ladder
games inside `pop_field.tsv`. Fixture: LADDER TAPES ONLY, no downloads, no arena, no local
engine run.**

Two statistics, both computed **within the same team** (never across teams or eras):

- **AUC** = Mann-Whitney common-language effect size comparing that team's **undamaged**
  removals (U) against that team's **damage-killed** removals (D), tie-corrected, two-sided
  normal approximation. 0.5 = no separation.
- **hazard** = undamaged removals per 10,000 of that team's builder-rounds, stratified at
  ROUND START by adversary contact and by map border.

| team | games | U | D | `d2_e_unit` AUC (U vs D) | enemy in vision at U | **hazard on border /10k** | **hazard off border /10k** | verdict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| **vjg** | 225 | 1,517 | 58 | **0.942** (p<1e-4) | 29.6% | **450.71** | **0.000** (0 / 560,750) | boundary-gated |
| **Troupe** | 240 | 345 | 66 | **0.834** (p<1e-4) | 19.4% | **146.43** | **0.000** (0 / 688,735) | boundary-gated |
| **S** | 210 | 293 | 36 | **0.771** (p<1e-4) | 25.9% | **105.06** | **0.000** (0 / 642,562) | boundary-gated |
| **Ship Happens** | 160 | 246 | 34 | **0.810** (p<1e-4) | 23.2% | **111.55** | **0.000** (0 / 441,970) | boundary-gated |
| **Cookie** | 210 | 119 | 117 | 0.488 (ns, p=0.73) | **99.2%** | 4.95 | 2.982 | **adversary-locked** |
| Ouroboros | 90 | 56 | 252 | 0.817 (p<1e-4) | 60.7% | 10.98 | 2.788 | own-state / mixed |
| not adgato | 175 | 23 | 411 | 0.776 (p<1e-4) | 100% | 1.08 | 0.931 | **underpowered** |
| LingLing40 | 100 | 5 | 372 | — | — | 0.00 | 0.395 | **underpowered** |
| I Stone | 115 | 4 | 660 | — | — | 0.00 | 0.124 | **underpowered** |
| farming_200s | 110 | 1 | 446 | — | — | 0.00 | 0.052 | **underpowered** |

AUC>0.5 means U is FARTHER from the nearest enemy
unit than D.

**The four boundary carriers pooled: 2,401 undamaged removals in 107,159 border
builder-rounds (224.06/10k) against 0 in 2,334,017 non-border builder-rounds.** Rule of
three, 95% upper bound on the non-border hazard: **0.0129/10k**. Hazard-ratio lower bound
**≥17,432×**.

**Every one of the 2,401 was standing on a border tile.** 1,517/1,517 `vjg`, 345/345
`Troupe`, 293/293 `S`, 246/246 `Ship Happens`.

### The adversary gradient, conditional on the gate

Pooled over those four teams:

| stratum (nearest enemy UNIT at round start) | **on border** | | **off border** | |
| --- | ---: | ---: | ---: | ---: |
| | rounds | hazard/10k | rounds | hazard/10k |
| contact, d²≤2 | 4,683 | 330.98 | 296,387 | **0.00** |
| in vision, d²≤20 | 9,453 | 401.99 | 556,966 | **0.00** |
| far, d²>20 | 93,023 | 200.60 | 1,480,664 | **0.00** |

**Read the two columns against each other.** Off the border, adversary contact does nothing
— the hazard is 0 in all three strata, including a third of a million rounds in melee
contact. On the border, adversary proximity modulates the hazard by at most 2× and
**non-monotonically** (contact 331 < vision 402 > far 201), which is not the shape of an
adversary-triggered code path and is not a usable trigger. **The gate is the boundary; the
adversary is a second-order, non-monotone modulation of it.**

---

## 3. THE DISCRIMINATOR, AND BOTH ITS CONTROLS

The discriminator has three parts and each carries its own controls.

### 3.1 Within-team unpaired: U vs D on adversary covariates

Computed per team on 12 adversary-state and 14 own-state covariates measured at ROUND START
of the removal round (`d2_e_unit`, `d2_e_mobile`, `d2_e_turret`, `d2_e_any`, `d2_e_core`,
`n_e_vis`, enemy shots landing within d²≤8 that round, enemy `builderAttack` within d²≤2,
whether the unit was ever damaged; and age, round, `d2_o_core`, adjacency to own buildings,
own live unit count, own builder count, builds completed, rounds since its own last build,
distance to map edge, standing on ore, tile rebuilt within 3 rounds, team spawned a
replacement within 5 rounds).

### 3.2 Within-unit paired: the removal round against a round from the SAME builder's own life

For every removed builder a second round was drawn **uniformly from its own life**
(`spawn+1 … removal−1`, deterministic per-file seed) and the identical covariates computed
there. Sign test on the paired differences. **This is the background the "close to an enemy"
claim has to beat, and it holds the map, the game, the opponent, the team and the unit
constant by construction.**

### 3.3 Per-round hazard, stratified

§2's table. The removal-only cuts answer "where were they when they died"; this answers
"given that a builder is standing HERE, what is its per-round chance of leaving the game
undamaged", which is the only form in which the question is actionable.

---

### POSITIVE CONTROL — the discriminator must find adversary causation where it is certain

A **damage-killed** builder was, by construction, in reach of an enemy weapon. If the
instrument cannot see that, it cannot see anything.

`vjg`, damage-killed removals vs their own mid-life baseline rounds (sign test, discordant
pairs only):

| covariate | pairs | median at death | median at baseline | frac lower at death | p |
| --- | ---: | ---: | ---: | ---: | ---: |
| `d2_e_unit` | 41 | **2** | 8.5 | 0.951 | 1.9e-08 |
| `d2_e_any` | 42 | **1** | 5 | 0.905 | 3.5e-07 |
| `d2_e_turret` | 51 | **4** | 31.5 | 0.922 | 4.1e-09 |
| `n_e_vis` | 51 | **13** | 3 | 0.137 (i.e. HIGHER at death) | 4.6e-07 |
| `e_shot_near` | 50 | 1 | 0 | **0.000** (higher at death in all 50) | 4.2e-12 |
| `e_shot_at` | 33 | 1 | 0 | **0.000** | 2.5e-08 |

**It fires, hard, on n=41–51.** The same control fires for every carrier with ≥20
damage-killed removals.

**A second positive control, and it is the more important one because it fires on the
UNDAMAGED arm:** `Cookie`'s undamaged removals come out **adversary-locked** —
`d2_e_unit` median 1 at removal vs 10 at its own baseline, 79 of 102 discordant pairs
closer, **p = 5.2e-08**; `d2_e_core` median 4 vs 37, p = 6.3e-11; enemy in vision at 99.2%
of removals. **So the discriminator is demonstrably capable of returning "adversary" on the
very group whose null is being reported for the other four teams.** A null returned by an
instrument that has never returned the alternative on that arm is worthless; this one has.

### NEGATIVE CONTROL — the discriminator must NOT fire where nothing is there

Four, all run before the headline was written:

1. **A pure random-noise column.** A U(0,1) draw attached to every row.
   `vjg` unpaired AUC **0.515, p=0.71**; paired frac-lower **0.503, p=0.84**.
   `Cookie` unpaired AUC 0.507, p=0.86; paired 0.513, p=0.86.
2. **Label permutation** (200 shuffles of the U/D labels within team). `vjg`: observed
   `d2_e_unit` AUC 0.942 against a permutation |ΔAUC| 95th percentile of 0.0763,
   **p_perm = 0.000**; observed noise AUC 0.515, **p_perm = 0.735**. The permutation null is
   centred on 0.5 and the real covariate sits far outside it.
3. **The complement-group rate, which is the rule TRAP 8 left behind.** Six teams at exactly
   zero undamaged removals accumulate **722,545 border builder-rounds with 0 undamaged
   removals** (95% UB 0.0415/10k). **The border is not lethal per se** — it is lethal only
   for these four teams' code. A constant column would have shown the same hazard everywhere.
4. **The border instrument returns the other verdict where it must.** `Cookie`'s undamaged
   removals are **106 of 119 on NON-border tiles**; `Ouroboros` 44 of 56. The border flag is
   not a tautology of "undamaged removal".

**A control I had chosen and had to discard, reported because discarding it is data.** I had
pre-selected `round % 2` as a null covariate. It is not null: `vjg`'s undamaged removals fall
on even rounds 927:590 (paired vs baseline p = 1.4e-10). **A team whose voluntary-exit events
have a round-parity signature is running a scheduled policy, not a random fault** — so the
covariate failed as a control and succeeded as evidence. It is replaced above by the random
noise column, which has no such structure.

---

## 4. THE ALTERNATIVE EXPLANATIONS THE BRIEF NAMED — measured, and mostly dead

**1. The 50-unit cap (the brief flagged this as the strong alternative). DEAD.**
`GameConstants.MAX_TEAM_UNITS` is 50. Across **every** carrier, the number of undamaged
removals occurring with the team at ≥45 live units is **0 (0.00%)**. `vjg`'s median live unit
count at an undamaged removal is **6** (p90 8, max 12). These teams are nowhere near the cap.
Slot-freeing is not what this is.

**2. "Recycle right after it finished building". WEAK.** Only **0.1%** of `vjg`'s undamaged
removals occur within 1 round of that builder's own last build (`vjg` damage-killed: 12.1%);
**13.1% of them never built anything at all**, and for `Cookie` that figure is **79.8%**. The
`since_build` covariate does not separate U from D for `vjg` (AUC 0.497, p = 0.95).

**3. Tile-clearing (remove the body so a building can go on that tile). WEAK.** The removed
builder's tile is built on within 3 rounds in **6.3%** of `vjg`'s undamaged removals, 4.9%
`Troupe`, 2.4% `S`, 1.6% `Ship Happens`, 2.5% `Cookie`.

**4. Immediate replacement. WEAK.** The team spawns a new builder within 5 rounds of an
undamaged removal in 8.2% (`vjg`) / 4.3% (`Troupe`) / 4.1% (`S`) / 1.6% (`Ship Happens`) of
cases.

**5. Cost-scale management is NOT excluded and I could not measure it.** Every live builder
bot adds +20% to the one global additive cost factor, so retiring a builder is worth real
titanium. That is a coherent motive for a deliberate policy and nothing here rules it out;
it also does not explain why the retirement is 100% boundary-locked.

**6. Launched off the map / thrown to death. EXCLUDED.** `thrown` (a `moveBuilderBot` of more
than one tile in the removal round) is **0 across all 2,401 boundary-carrier undamaged
removals** and 0 for `Cookie` and `Ouroboros`.

**7. A fact that cuts AGAINST calling it clean recycling, reported because it is
inconvenient:** `vjg` undamaged-removes its **last surviving builder bot 101 times (6.7% of
its 1,517)**, leaving the team holding only its core. `Troupe` 4, `S` 9, `Ship Happens` 9.
A pure recycler should not do that. **I am not claiming this is a crash — §5 says the tape
cannot tell — only that the "obviously deliberate" reading is not free either.**

---

## 5. WHAT THIS CUT CANNOT SEE

1. **It cannot tell a crash from `self_destruct()`. At all.** That was settled by the parent
   (`undamaged-builder-deaths-2026-08-10.md` §4) by byte-comparing two replays that differ in
   one source line: **identical, 1000/1000 turns, 0 differing bytes**, with the traceback
   never reaching the tape. **This cut therefore characterises the CONDITIONS under which the
   category fires, never the call that fires it.** Every sentence above should be read that
   way.
2. **Turn-loss is invisible and this speaks only to the UNIT-loss channel.** A team at zero
   undamaged removals may be raising and swallowing exceptions on every round behind a
   blanket `try/except`, which converts unit-loss into turn-loss and leaves no trace
   (`idle-round-envelope-2026-08-10.md`). **Nothing here prices crash-induction overall.**
   The 36 zero-teams are not "crash-free"; they are "not losing units to it".
3. **An observational hazard is not an interventional effect.** The 224/10k border hazard is
   conditional on the builder having *walked* to the border. If it goes there **because** the
   bot has already decided to retire it, the arrow runs the other way and putting a builder
   there by force does nothing. This cut cannot break that.
4. **Inducibility is untested and the corpus contains no natural experiment.** A launcher
   picks up a builder from **either** team, so a throw is the one way an adversary can place
   an enemy builder on a chosen tile. Across the 940 archived games involving these six
   teams, **there is not one hostile throw of a `vjg`, `Troupe`, `S`, `Ship Happens` or
   `Cookie` builder.** The only hostile throws found were **153 against `Ouroboros`, of which
   15 landed on a border tile, and 0 of those 15 produced a removal within 3 rounds** (95%
   upper bound 20%, and `Ouroboros` is not one of the boundary-gated teams anyway).
5. **The archive is not a random sample of the field** (corpus-howto TRAP 4). Per-team
   coverage runs 90–260 games. Every rate above is "in these games", and the games are the
   ones our archiver happened to hold.
6. **Enemy-core distance uses the core's seeded position for the whole game**, so a
   destroyed core still contributes; mid-game removals are the only rows measured, so this
   is small, but it is not zero.

---

## 6. POWER — what each null could and could not have detected

**The boundary result is not a null and needs no power argument: 0 in 2,334,017
builder-rounds against 2,401 in 107,159.** The nulls that do need one:

| test | population | statistic | minimum detectable effect @80% power, α=0.05 two-sided |
| --- | --- | --- | ---: |
| U vs D, `vjg` | 1,517 vs 58 | AUC | **\|AUC−0.5\| ≥ 0.108** |
| U vs D, `Troupe` | 345 vs 66 | AUC | 0.109 |
| U vs D, `S` | 293 vs 36 | AUC | 0.143 |
| U vs D, `Ship Happens` | 246 vs 34 | AUC | 0.148 |
| U vs D, `Cookie` | 119 vs 117 | AUC | 0.106 |
| U vs D, `Ouroboros` | 56 vs 252 | AUC | 0.120 |
| U vs D, `not adgato` | 23 vs 411 | AUC | 0.174 |
| paired, `vjg` U | 1,413 pairs | frac-lower | **±0.037** |
| paired, `Cookie` U | 102 pairs | frac-lower | ±0.139 |
| paired, `Ouroboros` U | 53 pairs | frac-lower | ±0.192 |
| paired, `not adgato` U | 16 pairs | frac-lower | ±0.350 |
| hazard, four carriers off border | 2,334,017 rounds, 0 events | rule of three | **≤1.29e-6 per builder-round** |

**Three teams are NOT classified above and must not be read as null results:** `LingLing40`
(5 events), `I Stone` (4), `farming_200s` (1), and `not adgato` (23, paired MDE ±0.350 —
which cannot distinguish a coin from a 4:1 effect). **`Ouroboros`'s paired adversary null
(frac-lower 0.585, p=0.27, MDE ±0.192) is genuinely underpowered and I am calling it
"mixed", not "own-state".**

`Cookie` is the one place where power matters in the other direction: its adversary result is
significant at n=102–118 pairs and is **not** underpowered, but it rests on **one team, 210
games, 42 matches**, and per §5.1 it does not distinguish a crash from a raider that
self-destructs on arrival.

---

## 7. WHAT I DELIBERATELY DID NOT MEASURE, AND THE FIXTURE THAT WOULD DECIDE THE REMAINDER

**Not measured, on purpose** (a measurement the question does not turn on imports its own
population and its own denominators):

- **Any association with winning, Elo, or game outcome.** The question is whether a trigger
  exists, not whether it pays; pulling outcome in would have imported a second population.
- **Per-map and per-opponent breakdowns** of the boundary hazard. The pooled gate is
  categorical (0 vs 224/10k); slicing it 70 ways buys nothing and burns power.
- **Our own side.** The parent already closed it at 0/539 and this cut adds no information
  there.
- **Non-builder undamaged removals** (turrets, launchers, cores) for any team. `destroy()` is
  legal on buildings, so the discriminator is materially weaker for them and would need its
  own controls.
- **The identity of `Cookie`'s events beyond their conditions.** Nothing in the tape can go
  further (§5.1).

**The one fixture that would decide the remainder, stated once so it can be picked up or
dropped without re-deriving it.** The open question is no longer "which teams crash" — it is
**"can a builder be forced into the trigger state, and does the removal follow?"** That is a
one-arm UNRATED leg and it is builder's lane, not mine:

> Against `vjg` (highest hazard, 450.71/10k, and 225 archived games of prior), build a single
> launcher within reach of a lane their builders use, and throw one of THEIR builders onto a
> border tile. Pre-register the bar before the leg: **≥3 of 10 successful throws-to-border
> followed by an undamaged removal within 3 rounds** (their observed unconditional rate is
> 947 of 3,194 border entries removed on the very first border round, 29.6%). **Falsifier: 0
> of 10.** One leg settles a question 5,140 archived games cannot, because the archive
> contains zero instances of the intervention.

Until that leg runs, **the carrier list is a list of teams with an unusual internal policy,
not a list of teams we can kill units on.** It should not be quoted as a target list.

---

## Appendix — reproducing this

Scripts are session-scratch and die with the session, per the standing note that a fresh
analyst regenerates them in ~10 minutes: `pop.py` (population freeze), `stageA.py` (whole-game
HP ledger, one row per builder removal — the falsifier), `stageB.py` (35 covariates at round
start for every removal plus a uniformly-sampled round from the same builder's own life),
`stageC.py` (border-run occupancy and survival), `stageD.py` / `stageD2.py` (per-round hazard
stratified by adversary contact / enemy-core distance and by border), `stageE.py` (the
launcher-throw natural experiment), `stats.py` (tie-corrected Mann-Whitney, sign test, MDE),
`repA.py` / `repC.py` (reporters). Stdlib only — this venv has no numpy or scipy.

**Frozen population:** `pop_field.tsv`, sha256 `2fed2b0db2bd5bf9`, **5,140 games / 1,028
matches / 70 teams**. Decode completeness: **5,140/5,140 for stages A–C, 2,380/2,380 for
stage D, 1,295/1,295 for stage D2, 940/940 for stage E — 0 errors in every stage.** An
incomplete run would have had no number.

**Load-bearing decisions, in the order they would break the result:**

1. **The falsifier was run and reported before the main cut.** Had `vjg`'s rows carried
   preceding negative deltas, nothing below §1 would exist.
2. **`UpdateHp.delta` decoded as a sign-extended 64-bit varint** (TRAP 2), confirmed by the
   delta alphabet containing no ~1.8e19 values and no −2.
3. **Covariates are evaluated at ROUND START, before the round's updates are applied** —
   which is what the S1 `FireTurret`-after-`removeEntity` ordering trap requires
   (`tools/replay_schema.md`).
4. **The map parse was validated, not assumed**: 303 sampled files, `len(rows) == H` and
   every row length `== W` in **303/303**. `d_edge` is the whole result, so a wrong `W`/`H`
   would have manufactured it. An earlier version of that check was itself wrong (it read the
   `TileRow` submessage as raw packed varints and reported 303/303 BAD); the check was fixed
   and re-run rather than the finding being trusted.
5. **The comparison is always within one team** — U against that team's own D, and each
   removal against the same *unit's* own earlier round. No cross-team or cross-era contrast
   carries any claim here.
6. **The `-1` "no such entity" sentinel was recoded to +∞ before any distance statistic.**
   Left as −1 it sorts as the closest possible enemy and inverted `d2_e_turret` (AUC read
   0.290 instead of 0.993 for `vjg`). Caught because a "no enemy turret exists" row cannot be
   the nearest enemy turret.
7. **The complement-group hazard was computed before the border result was written up**
   (six zero-teams, 722,545 border builder-rounds, 0 events) — the rule TRAP 8 left behind.
8. **Rotation `placeEntity` re-emits suppressed, first-id-wins** (TRAP 3);
   `ladder_games.tsv:seat` and `econ.tsv:deliveries` never touched (TRAPs 7, 8); team
   identity taken from `replay_archive/*.meta.json`, never from `winnerSide`.
