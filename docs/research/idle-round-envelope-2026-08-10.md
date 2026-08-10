# The idle-round envelope — an upper bound on silent turn-loss

**Research arm, session 29, decoded 2026-08-10. Read-only cut. No bot, arena, prereg,
coordination or INDEX file touched.**

Companion to `undamaged-builder-deaths-2026-08-10.md`, which closed the *unit*-loss half
of the exception question (0/539) and left the *turn*-loss half open with the sentence this
cut is aimed at: **"a unit burning turns on a repeating out-of-vision query looks, in the
replay, exactly like a unit that decided to idle."** That is still true. What follows is
the envelope around it.

---

## 0. THE BOUND, IN SIX LINES

**50.80% of our eligible unit-rounds pass with no action.** 277,278 idle of 545,847
eligible unit-rounds, over 3,665 of our units in 260 v102 ladder games (52 matches).
Tightened with the exact hard gates the engine itself enforces (ammo, unit cap, titanium
floor): **48.97%**.

**That is a LOOSE envelope and the pre-stated reading applies verbatim: it does not
demonstrate exceptions, and it is too loose to reassure.** Half our unit-rounds are
consistent with a swallowed `GameError`. They are equally consistent with a bot that has
been told to hold station.

**The bound tightens by more than an order of magnitude on the one sub-class where a
totally-broken unit would have to live.** A builder that *never once acted* across ≥50
eligible rounds: **1 of 1,516 (0.066%)**, carrying **51 of 82,462 idle builder-rounds
(0.06%)**. Field: **2.52%** of long-lived builders and 13.1% of their idle rounds.

**The rate MOVED.** Our builder-bot idle rate sat in an 11.4–21.6% band across thirteen
earlier shipped versions (v65–v94, median ≈14%) and reads **25.78% on v102** — the highest
of the fourteen, +12.9pp on the immediately preceding measured version. That is the
"different kind of evidence" the brief pre-named. **It is also exactly what LOKI-8's own
documented `hold station` / `launchwait` / navigation-stall behaviour would produce**, and
this cut cannot split those.

**⚠ The pre-committed limit binds. The bound came back loose. The answer is a stderr
counter in the bot — builder's lane — not a cleverer decode.** §8 says what I would NOT do.

---

## 1. THE ELIGIBILITY DEFINITION, AND WHY IT IS THE ONE

Everything rests on this. Stated first, defended second.

> A `(unit, round)` pair is **ELIGIBLE** iff
> **(a)** the engine emitted a `botOutput` carrying that unit's id in that round, **and**
> **(b)** the unit's simulated **action** cooldown was 0 at round start — or, for a builder
> bot, its action cooldown *or* its move cooldown was 0.
>
> It **ACTED** iff that round emitted, for that id, a `setActionCooldown` or a
> `setMoveCooldown` — or, for a core, a `coreConvertAmmo` for its team.
>
> **IDLE := ELIGIBLE and not ACTED.**

### (a) `botOutput` is the aliveness/turn test, not a computed one

`BotOutput` is emitted at the END of a unit's turn (brief), and — measured, not assumed —
**exactly once per unit per round**: 0 duplicate emissions in 5,985 games. It therefore
*is* the engine's own record of "run() was called for this unit this round", and using it
disposes of three of the brief's traps mechanically rather than by filter:

| trap | how the `botOutput` denominator handles it | measured |
| --- | --- | --- |
| a unit created MID-ROUND does not act that round | the engine emits **no** `botOutput` for a unit on its birth round | **0** newborn `botOutput`s in 5,985 games |
| a unit killed earlier in the round loses its turn | no turn ⇒ no `botOutput` | (a unit seen with both a `botOutput` and a `removeEntity` in one round ran first and died after — correctly counted) |
| buildings do not run `run()` | conveyors/splitters/harvesters/barriers never emit `botOutput` | **0** building `botOutput`s in 5,985 games |

**A computed denominator ("alive at round start") would have imported all three.** This one
cannot: the engine wrote it.

### (b) the cooldown gate, and why it barely bites — which is the point

Cooldowns are simulated: seeded from `PlaceEntity` (`BuilderBot.actionCooldown` /
`Core.actionCooldown`), updated on every `SetActionCooldown` / `SetMoveCooldown`,
decremented by 1 at end of round.

The emitted values are a closed alphabet — **builder 1, gunner 1, sentinel 2, launcher 1,
core 1** — so after the end-of-round decrement *every unit type except the sentinel is
eligible again the very next round*. The gate is therefore near-vacuous for builders and
that is not a defect: **it means the builder denominator is essentially "every round the
builder was alive and ran", which is the widest honest denominator and so the most
conservative upper bound.** Where it does bite (sentinels, reload 2) it removes exactly the
rounds the unit provably could not act in.

**Self-check, and it is the load-bearing one:** the simulation is contradicted if a unit
acts on a round it was predicted to be on cooldown. **0 violations in 5,985 games**
(62,225,279 eligible unit-rounds).

### Why the cooldown *markers* and not the action updates

Counting `builderBuild`/`builderHeal`/`builderAttack`/`moveBuilderBot`/`fireTurret`
directly is wrong three ways, and each one was found in the tape, not reasoned about:

1. **`FireTurret` carries no id** — only `from`/`to`. Turret shots are attributable only
   via position → turret, or via the turret's `setActionCooldown`.
2. **`rotate()` emits a `placeEntity` RE-EMIT and no action update at all** — but it does
   set the action cooldown. Counting `placeEntity` would have walked straight into the
   28,775-re-emit trap; counting `setActionCooldown` picks rotations up for free and never
   reads a re-emit (first-id-wins, TRAP 3).
3. **`moveBuilderBot` is NOT proof of a self-move.** A **launcher throw relocates a builder
   and emits `moveBuilderBot` with no `setMoveCooldown`.** Verified arithmetically on the
   calibration game: `moves(741) − setMoveCooldown(721) = launcher setActionCooldown(20)`,
   exactly. Crediting a thrown body with an action would have deflated the idle rate on
   precisely the units LOKI-8 throws. **This trap is not in the brief.**

### The three actions that leave NO marker — named, not hidden

`destroy()`, `self_destruct()` and `write_store()` consume no cooldown and emit nothing
attributable to an actor. A unit doing only those reads as IDLE.

- `destroy()` / `self_destruct()`: **the shipped v102 tree has zero call sites for
  `self_destruct()`, `destroy()` or `resign()`** across `main.py`, `doctrine.py`, `eco.py`,
  `raid.py` (grep re-run this session, independently reproducing
  `undamaged-builder-deaths-2026-08-10.md` §4). **Not a confound on our arm. It is a
  confound on the FIELD arm and inflates the field's rate by an unknown amount.**
- **`write_store()` is a real, unbounded confound on our own arm and I cannot size it.**
  LOKI-8 writes the comms store in the builder path (`SLOT_ROLE_N`, `SLOT_RAID_N`,
  `SLOT_ENEMY_CORE`). A round spent sensing and writing a slot is a round that did real
  work and reads as idle here. **This is the single largest reason the envelope is an
  upper bound and not an estimate.**

### The gated variant

A second, strictly tighter denominator additionally requires the hard resource gates the
engine enforces: **gunner/sentinel** need team ammo ≥ 4/10 at their turn; **core** needs
team titanium ≥ 30 (the *unscaled* builder cost — a strict necessary condition, so
conservative) and live unit count < 50. It moves the number by <2pp, which is itself the
finding: **our idle rounds are overwhelmingly not resource-blocked.**

---

## 2. THE BOUND AND ITS CONTROLS

**Subject: our units' eligible rounds. Unit: one (unit, round) pair. Fixture: LADDER, no
downloads, no arena.**

| arm | population | games | units | **eligible unit-rounds** | **idle** | **rate** | gated | standardised¹ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **US v102** | our side, v102 | **260** | **3,665** | **545,847** | **277,278** | **50.80%** | 48.97% | 50.80% |
| OPP, *same 260 games* | opponents | 260 | 3,679 | 734,405 | 403,800 | 54.98% | 52.44% | 48.97% |
| **US Eir (v71–81)** | our side, Eir era | **745** | **15,116** | **3,825,361** | **1,630,926** | **42.63%** | 41.07% | **44.94%** |
| OPP, Eir games | opponents then | 745 | 17,064 | 4,490,628 | 2,599,872 | 57.90% | 55.31% | 50.39% |
| **FIELD control** | third-party ladder, both sides | **4,980** | **160,537** | **52,629,038** | **28,174,061** | **53.53%** | 49.48% | **53.15%** |

¹ direct standardisation: that arm's per-(type × round-band) rates applied to **US v102's
own type × band mix**, so the column is free of composition differences. Coverage 100% of
the reference denominator in every row.

**Ours vs the field: 50.80% against 53.15% standardised.** We idle slightly *less* than the
field on a like-for-like mix. **Ours vs Eir: 50.80% against 44.94% standardised — a real
+5.9pp move that is not explained by unit mix.**

**Per-game.** Mean **1,066** idle unit-rounds per game, median 542 (median game 177 rounds,
min 59, max 1,000). **Concentration tail: top-1 game 5.55%, top-3 12.07%, top-5 17.23%,
top-10% of games 43.76%** — spread, not one pathological match.

---

## 3. BY UNIT TYPE AND ROUND BAND

**US v102** — 260 games, 3,665 units, 545,847 eligible unit-rounds:

| kind | units | eligible | idle | **rate** | gated | % of denom | r0–49 | r50–149 | r150–299 | r300+ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| core | 260 | 66,462 | 51,318 | 77.21% | 75.30% | 12.2% | 76.17% | 74.40% | 72.19% | 85.55% |
| **builder bot** | **1,840** | **319,839** | **82,462** | **25.78%** | 25.78% | **58.6%** | 13.13% | 26.27% | 28.91% | 32.92% |
| gunner | 213 | 32,295 | 29,492 | 91.32% | 91.46% | 5.9% | 59.78% | 82.53% | 91.79% | 97.30% |
| sentinel | 987 | 60,732 | 49,610 | 81.69% | 81.44% | 11.1% | 71.35% | 70.28% | 81.39% | 90.67% |
| launcher | 365 | 66,519 | 64,396 | 96.81% | 96.81% | 12.2% | 96.88% | 94.87% | 97.38% | 97.79% |
| **ALL** | **3,665** | **545,847** | **277,278** | **50.80%** | 48.97% | 100% | 33.01% | 45.93% | 55.41% | 62.59% |

**FIELD control** — 4,980 games, 160,537 units:

| kind | units | eligible | idle | rate | r0–49 | r50–149 | r150–299 | r300+ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| core | 9,960 | 5,419,454 | 4,496,903 | 82.98% | 75.34% | 79.52% | 81.25% | 85.82% |
| builder bot | 84,183 | 32,469,282 | 10,404,658 | **32.04%** | 21.33% | 29.41% | 31.22% | 34.03% |
| gunner | 49,719 | 11,179,455 | 10,033,854 | 89.75% | 65.73% | 80.22% | 86.94% | 92.99% |
| sentinel | 13,025 | 2,696,123 | 2,441,698 | 90.56% | 66.05% | 82.30% | 87.93% | 93.67% |
| launcher | 3,650 | 864,724 | 796,948 | 92.16% | 92.43% | 93.37% | 92.05% | 91.81% |
| ALL | 160,537 | 52,629,038 | 28,174,061 | 53.53% | 36.79% | 48.38% | 52.53% | 56.50% |

**US Eir (v71–81)** — 745 games, 15,116 units: core 79.85%, **builder bot 14.85%**
(10,426 units, 2,371,323 eligible), gunner 83.14%, sentinel 93.58%, launcher 96.87%;
ALL 42.63%. By band the Eir **builder** row is essentially FLAT — 14.91 / 16.88 / 16.66 /
13.93% — where v102's climbs 13.13 → 32.92%.

**Read the turret and launcher rows before reading anything into the headline.** A gunner
with nothing in its firing line and a launcher with no adjacent body have nothing to do;
90%+ is the correct answer for those classes and it is what the field reads too. **The
headline 50.80% is dominated by classes whose idleness is structural.** The only row worth
arguing about is the builder bot, which is 58.6% of the denominator and the class that runs
the code paths a `GameError` would come from.

---

## 4. THE MOVE — our own version trajectory, builder bots only

Our side, ladder only, plan-B matches excluded, per shipped platform version with ≥40
archived games. **The builder column is composition-free by construction (one type).**

| ver | games | ALL idle | core | **builder** | gunner | sentinel | launcher | builders | never-acted (e≥50) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 65 | 45 | 44.03% | 79.34% | 14.53% | 90.60% | 84.78% | 99.33% | 407 | 0/329 (0.00%) |
| 68 | 95 | 38.85% | 83.36% | 11.38% | 68.58% | 90.76% | 95.07% | 904 | 1/744 (0.13%) |
| 69 | 45 | 37.94% | 81.32% | 16.83% | 61.85% | 86.91% | 98.17% | 412 | 0/336 (0.00%) |
| 70 | 40 | 41.83% | 82.18% | 21.58% | 71.28% | 93.18% | 95.62% | 430 | 8/371 (2.16%) |
| 72 | 135 | 40.95% | 77.99% | 15.18% | 66.06% | 92.97% | 94.67% | 1,255 | 2/1,035 (0.19%) |
| 74 | 70 | 42.14% | 71.53% | 16.39% | 66.35% | 90.94% | 96.94% | 673 | 3/555 (0.54%) |
| 75 | 70 | 42.07% | 80.11% | 12.84% | 88.05% | 94.02% | 98.38% | 1,136 | 0/779 (0.00%) |
| 76 | 40 | 46.82% | 75.44% | 13.42% | 63.43% | 97.64% | 94.76% | 438 | 0/315 (0.00%) |
| 80 | 295 | 42.34% | 81.85% | 15.36% | 88.61% | 93.80% | 97.24% | 4,853 | 15/3,328 (0.45%) |
| 90 | 80 | 45.55% | 86.00% | 15.47% | 92.20% | 95.27% | 97.36% | 1,540 | 0/951 (0.00%) |
| 91 | 75 | 35.03% | 78.28% | 11.91% | 79.79% | 91.73% | 98.52% | 1,226 | 0/752 (0.00%) |
| 92 | 75 | 36.42% | 80.41% | 13.72% | 85.10% | 87.94% | 97.83% | 936 | 2/770 (0.26%) |
| 94 | 140 | 39.90% | 83.08% | 12.89% | 88.99% | 93.83% | 97.55% | 1,539 | 0/1,349 (0.00%) |
| **102** | **260** | **50.80%** | 77.21% | **25.78%** | 91.32% | **81.69%** | 96.81% | **1,840** | **1/1,516 (0.07%)** |

**v102's builder idle rate is the highest of the fourteen, by 4.2pp over the next highest
(v70) and by 12.9pp over v94, the version it replaced.** The ALL column is likewise the
highest. This is a **rate that moved when a version shipped**, and per the pre-stated
interpretation that is a stronger class of evidence than a rate that has always been high.

**It is also, on its face, what LOKI-8 was designed to do.** The shipped tree carries
explicit hold-in-place behaviour that v94 Eir did not have: raiders that
`hold` a foothold, an interceptor that "still holds station", a `launchwait` role that
parks a builder beside a launcher, a navigation-stall path that pauses a raider, and a
first-run `if self.core is None: return`. Eir was a heal line — a builder with a friendly
entity beside it always has something to do, which is why its builder row is flat at ~15%
across every round band. **The move is real; the attribution is not available from the
tape.**

Note also **sentinel idle FELL** (93.58% Eir → 81.69% v102) while builder idle rose. A
uniform "v102 loses turns" story does not fit that; a "v102 is a different bot" story does.

---

## 5. PROVING THE CONTROL FIRES — four ways

### 5.1 Suppress a known action class and watch the rate move (METHOD RULE 1)

Same 260 games, same denominator (545,847), only the action attribution corrupted:

| arm | US idle | Δ vs clean | what it proves |
| --- | ---: | ---: | --- |
| **clean** | **50.80%** | — | |
| `none_act` — credit nothing | **100.00%** | +49.20 | the classifier can reach **every** row in the denominator; there is no structurally unreachable subset |
| `all_act` — credit everything | **0.00%** | −50.80 | and can clear every row |
| `suppress_move` — drop `setMoveCooldown` | 81.71% | **+30.91** | builder movement is visible and is the largest single action class |
| `suppress_heal` — drop the heal-round cooldowns | 60.55% | **+9.75** | heals are visible and separable |
| `suppress_build` | 53.63% | +2.83 | builds are visible |
| `suppress_fire` — drop turret cooldowns | 53.35% | +2.55 | turret shots are visible |
| `suppress_convert` — drop `coreConvertAmmo` | 53.23% | +2.43 | the core's non-cooldown action is visible |

**Every action class moves the rate on its own.** A constant column is excluded in both
directions.

### 5.2 The instrument resolves REAL turn-loss — the TLE calibration

**TLE is the one turn-loss mechanism that is visible in the tape, and it has the same
signature as a swallowed exception: `run()` called, no action, unit survives.** So it is the
positive control for the whole question.

| arm | idle builder unit-rounds | **of which TLE** | share |
| --- | ---: | ---: | ---: |
| **US v102** | 82,462 | **0** | **0.0000%** |
| OPP, same 260 games | 108,762 | 2,772 | 2.61% |
| US Eir v71–81 | 352,143 | 27 | 0.008% |
| **FIELD** | 10,404,658 | **776,454** | **7.46%** |

**The classifier finds 776,454 real turn-losses in the field arm.** It is not blind to the
category it is bounding. And **our side carries 0 TLE turn-losses in 545,847 eligible
unit-rounds** — reproducing the sibling cut's "0 TLE events in 235 games" on an independent
denominator and a larger population.

### 5.3 An exact conservation check on the action model

The team ammunition balance was reconstructed from the update stream — start 0, `+amount`
on every `coreConvertAmmo`, `−4/−10` on every `FireTurret` resolved to its turret by
position — and compared to the engine's own `Player.ammo` at the end of every round.

**0 mismatches in 6,309,310 team-rounds across 5,985 games. 0 `FireTurret` events that
failed to resolve to a turret.** This is not a smoke test: it means every shot is
attributed to the right turret, every conversion is caught, and — because `rotate()` sets a
cooldown but spends no ammo — that **rotations are correctly separated from shots**. An
earlier draft that charged ammo per gunner `setActionCooldown` mismatched on 2.03% of
team-rounds; that residual **was** the rotations.

### 5.4 The controls come out different from us

Standardised on our own mix: **US v102 50.80%, FIELD 53.15%, US Eir 44.94%, opponents in
our own games 48.97%.** Per type the arms differ far more (our sentinel 81.69% vs Eir's
93.58%; our launcher fleet 365 units vs the field's 3,650 across 19× the games). **The arms
are not the same number.**

---

## 6. THE TIGHT SUB-BOUND — where a totally-broken unit would have to live

A per-unit rate is a statement about one unit. **1,840 of our builders ran at least one
eligible round; 1,516 ran ≥50.** Distribution of per-unit idle rate over those 1,516
(81,687 idle rounds; the other 775 idle rounds sit on 324 short-lived builders):

| per-unit idle rate | units | % of units | idle rounds | % of subset's builder idle |
| --- | ---: | ---: | ---: | ---: |
| exactly 0% | 373 | 24.6% | 186 | 0.2% |
| <5% | 303 | 20.0% | 1,727 | 2.1% |
| 5–10% | 224 | 14.8% | 2,765 | 3.4% |
| 10–25% | 189 | 12.5% | 5,315 | 6.5% |
| 25–50% | 121 | 8.0% | 7,653 | 9.4% |
| 50–75% | 138 | 9.1% | 14,153 | 17.3% |
| 75–95% | 138 | 9.1% | 33,059 | 40.5% |
| 95–99.9% | 29 | 1.9% | 16,778 | 20.5% |
| **exactly 100%** | **1** | **0.07%** | **51** | **0.06%** |

**The median builder idles 5.10% of its eligible rounds.** The pooled 25.78% is carried by
a minority: **168 units (11.08%) at ≥75% idle carry 61.07% of that subset's idle rounds.**
Concentration over units: top-10 11.75%, top-1% 17.44%, top-10% 63.72%.

**"Never acted once, over ≥50 eligible rounds" is the shape of a unit whose `run()` raises
on an unconditional path** — the `reported_error` latch is per-`Player` instance, i.e. per
unit, so such a unit crashes every round for the rest of its life and never acts again.

| arm | builders with ≥50 eligible rounds | **never acted** | share |
| --- | ---: | ---: | ---: |
| **US v102** | 1,516 | **1** | **0.066%** |
| US Eir v71–81 | 7,315 | 20 | 0.27% |
| **FIELD** | 70,137 | **1,770** | **2.52%** |

**Bounded: at most 1 of our 1,516 long-lived builders, and at most 51 of 82,462 idle
builder-rounds (0.06%), can be an always-crashing unit.** The field is 38× that rate, so
the category exists and the instrument sees it. **This retires the "a whole unit is
permanently dead in the water" worry. It does not touch the conditional-path worry**, which
is the one the sibling cut actually raised.

**A soft, non-load-bearing corroboration.** Our idle builder-rounds are CHEAP:
**mean 251µs, 95.2% under 400µs**, against 955µs (55.4% under 400µs) on our acted rounds.
Eir's idle rounds averaged 942µs and the field's 1,446µs. A cheap early return is what a
decision-to-idle looks like; an exception thrown deep in `_dispatch` after the sensing loops
would cost at least as much as reaching that depth. **This does NOT exclude an exception
raised early** — and `_builder()` raises earliest in exactly the sensing loop that reads
neighbours — so it is a hint, not a bound, and nothing above depends on it.

---

## 7. WHAT THIS BOUND CANNOT EXCLUDE

Stated so a later reader cannot re-read the number as more than it is.

1. **It cannot separate deliberate idling from exception turn-loss. At all.** That was
   pre-stated and it is what happened. Half our unit-rounds are inside the envelope.
2. **`write_store()`-only rounds are counted as idle** and I cannot size them. LOKI-8 writes
   the store in the builder path. This alone could account for an unknown slice of the
   25.78%.
3. **The v102 builder move (+12.9pp on v94) has an obvious benign candidate** — LOKI-8's
   documented hold/park/launchwait/nav-stall behaviour, absent from Eir — and I have no
   instrument that separates it from a swallowed `GameError` on a conditional path.
   **Do not read §4 as evidence of a bug. Read it as: the thing that would have to be
   explained is 12.9pp of one class on one version.**
4. **`destroy()` and `self_destruct()` leave no attributable marker.** Zero call sites in
   v102 so our arm is clean; **the FIELD arm's 53.53% is inflated by an unknown amount** and
   the field row should not be quoted as a field *behaviour* number.
5. **The cooldown simulation seeds turrets at 0** (the schema carries no cooldown field for
   gunner/sentinel/launcher). 0 violations across 62.2M unit-rounds says the seed is never
   contradicted, but it is not directly confirmed.
6. **Ammo/titanium gating is a lower bound on "could not act".** The core gate uses the
   *unscaled* 30 Ti cost and ignores whether a spawn tile was free; both make the gated
   denominator too large, i.e. the gated rate is still an upper bound.
7. **The OPP arm's per-unit tail was not retained** (only its aggregates). The per-unit
   never-acted comparison is US vs Eir vs FIELD only.
8. **Engine parity.** Everything here is decoded from platform tapes, so §5's controls are
   platform-side. No local fixture was used and none is claimed.
9. **Not measured, deliberately** (a measurement the question does not turn on imports its
   own population): per-opponent breakdown; per-map breakdown; idle rate vs win; the
   composition of the 168 high-idle builders by position or role; anything about Elo.

---

## 8. THE PRE-COMMITTED LIMIT — what I am NOT proposing

**The bound came back loose. Per the brief's own pre-commitment, the answer is a stderr
counter in the bot, and that is builder's lane, not mine.**

Concretely, and stated once so it can be picked up or dropped without me re-deriving it:
the existing handler at `bots/_v124loki8/main.py:116` already latches `reported_error`; a
counter incremented in that `except` block, surfaced through an unused comms-store slot,
would turn the entire 277,278-round envelope into an exact number. It costs nothing per
round. **Route it through `print()`, not stderr**: `BotOutput.stdout` is carried in the
replay (`tools/replay_schema.md`) and the traceback's stderr is not — which is the whole
reason this cut exists. One line at a latched threshold, or a periodic count, and the
envelope collapses to a measurement on the ladder itself rather than in a local fixture.

**That is the whole recommendation. I am not proposing another decode.** Specifically I am
NOT proposing: exec-time-mode fitting to separate crash-returns from decision-returns
(§6's hint is where that ends); position-tracking the 168 high-idle builders to test the
parking hypothesis; or a per-role idle census. Each of those would produce a number and none
of them would separate the two causes, because **the tape does not contain the
discriminator** — `undamaged-builder-deaths-2026-08-10.md` §4 established that by
byte-comparing two replays that differ in one source line.

---

## Appendix — reproducing this

Scripts are session-scratch and die with the session: `idle2.py` (~300 lines against
`tools/replay_census.fields`; per-round cooldown simulation, action attribution, ammo
ledger, per-unit and per-game accumulators, and the seven corruption modes), plus
`rep2.py` / `tail.py` / `hist.py` / `tle.py` reporters.

**Frozen populations** (`replay_archive/*.meta.json`, `triggeredBy == ladder`, team id
`379a5d80-…`, `opensverige - plan B` (`b7cafd9f-…`) excluded from **both** arms; seat and
version from `.meta.json`, never from `winnerSide` — TRAP 7; `econ.tsv` never touched —
TRAP 8):

| file | sha256 (16) | games | matches |
| --- | --- | ---: | ---: |
| `pop_v102.tsv` | `f56cbe26b3a3dd28` | 260 | 52 |
| `pop_eir.tsv` | `4966ca902db5f87c` | 745 | 149 |
| `pop_field.tsv` | `34ab0ef13a71fdbd` | 4,980 | 996 |

**Decode completeness: 5,985/5,985 files, 0 errors, plus 7 corruption arms × 260 games.**
An incomplete run would have had no number.

**A live-archive caveat, because it bit mid-session.** The keeper is running and the archive
grew during this cut: the v102 population went 250 → 260 games between the first and final
enumeration. The headline moved 50.93% → 50.80% and the builder row 25.97% → 25.78%. All
tables above are the 260-game freeze; the earlier figures are recorded here only to show the
number is not fragile to that drift.

**Load-bearing decisions, in the order they would break the result:**

1. **`botOutput` is the denominator, not a computed aliveness test.** Verified 1-per-unit
   per-round, 0 for newborns, 0 for buildings. This is what disposes of the brief's
   denominator traps mechanically.
2. **`setActionCooldown` / `setMoveCooldown` are the action markers**, not the action
   updates — because `FireTurret` carries no id and `rotate()` emits only a `placeEntity`
   re-emit.
3. **`moveBuilderBot` alone is NOT an action.** Launcher throws emit it with no
   `setMoveCooldown`; the arithmetic identity `moves − setMoveCooldown = launcher
   setActionCooldown` was checked before the classifier was trusted.
4. **Cooldown simulation validated by 0 act-while-on-cooldown violations in 63.0M
   unit-rounds.**
5. **Ammo ledger reconstructs the engine's own `Player.ammo` exactly, 0/6,305,512
   team-rounds** — which is what proved rotations are separable from shots.
6. **`suppress_*` arms were run before the headline was written.** A rate with no proof that
   each action class can move it is a constant column.
7. **proto3 omits default values, and `Team.TEAM_A == 0`.** `coreConvertAmmo` for team A
   carries no team field; an early draft dropped every team-A conversion and over-counted
   our core's idle rounds by 5,649. Entity ids start at 1 (cores) / 3 (placed), so no id is
   ever omitted — checked.
