# How The Bisons kill a core in 49–92 turns — and what of it is stealable

**Research arm, 2026-08-10 06:23 CEST (`date`), repo at `1ff1acc`.**
Read-only cut. Source: the already-decoded corpus (`corpus/*.tsv`) plus map headers
re-read from `replay_archive/` for core positions. No downloads, no arena, no bot edits.
Scratch scripts live in the session scratchpad, not the repo.

---

## ⚠ READ BEFORE USING THE DOSE FINDING — **THIS IS A CLAIM ABOUT THE FIELD, AND OUR OWN CONVERSION RATE IS NOT MERELY UNMEASURED, IT IS UNMEASURABLE FROM THIS CUT**

Added 2026-08-10 (research lead, prompted by the side lane), **in the header rather
than the limits section, because it decides how the finding may be used.**

1. **We contribute essentially nothing to the treated arm.** We reach the gate
   **4 times in 2,508 team-sides (0.2%)**, so of the **804** treated observations
   almost none are ours. **The r45 dose finding describes the FIELD. It cannot
   describe us**, and no amount of further corpus work changes that — the
   observations do not exist.
2. **The pooled effect is a MIXTURE over a 6× spread, and the placebo does not
   protect against that.** Conversion at the same gate runs **Albert And Einstein
   11.1% · Bisons 47.5% · Cookie 69.2%**. The powered placebo (out-of-range
   sentinels, 5.2% → 3.4%, p=0.84) rules out *"the gate is spurious"*. **It does
   not rule out *"the gate means different things to different bots"*.**
   **`p=1.9e-12` is driven by n=17,235/804: it says the association is real. It
   does NOT say that 23.1% describes any particular team, including us.**
3. **Under D12 this closes nothing** (Magnus, 2026-08-10: *"test everything in
   unrated games before we refute them"*). It is archive-sourced **and**
   heterogeneous — doubly in *prioritise hard, close nothing* territory.
   **That is not a demotion: it is the strongest argument in the queue for FIRING
   the arrival leg rather than analysing further, because our own conversion rate
   is precisely the number no corpus cut can produce.**
4. **The two-bar prereg structure already absorbs this** — ARRIVAL (mechanism: 2+
   forward in-range sentinels **standing**, not merely built, at r45) scored
   separately from CONVERSION (currency: kill by r100). **A per-killer
   decomposition of the pooled effect would not change that structure, which is
   why it was declined rather than run** (a measurement you do not need imports
   its own population).

---

## The answer in six lines

1. **The falsifier passes.** The corpus independently reproduces 74 / 66 / 99 / 92 / 49
   for the five baseline games, exactly, and the fast-kill distribution is real far beyond
   those five: **28.7% of all 195 archived Bisons games end with the Bisons killing the
   enemy core inside 100 rounds** (us: 6.2% of 2,513).
2. **The mechanism is a forward sentinel battery.** They walk builders to the enemy core and
   plant **sentinels 2–5 tiles from the nearest enemy core tile**, median first one at r30,
   median kill at r69. Median d² from that sentinel to their OWN core is **208**; to the
   enemy core, **16**.
3. **100% of the core damage is turret fire.** Over 195 games their builder-attack total is
   **88 swings** (0.45/game) against **26.1/game** for their opponents in the *same replay
   files*; in their 41 third-party fast kills, **0 of 41 games contain a single melee swing
   on the enemy core**.
4. **What they refuse is as sharp as what they buy:** 0 launchers, 0 barriers, 0 splitters,
   0 throws, 0 heals across all 195 games, and **half the field's conveyors**. The whole
   global additive cost-scale budget goes to builders → sentinels → ammo (428 Ti converted
   by r150).
5. **It is not map-, seat- or opponent-conditioned.** Fast kills on **15 of 15 distinct
   maps**, against **14 of 21 distinct opponents**, in both seats, flat across map-area
   buckets. **Pre-registered branch B is rejected.**
6. **Landed on branch A, with one correction to the brief and one to my own prior:** the
   causal variable is the *count of forward in-range sentinels standing by r45*, **not** the
   geometry of their placement, and the Bisons opening is **not deterministic** — 41 of 41
   fast kills have distinct build sequences.

---

## 1. The falsifier check, first, before anything else

The four turn counts came from the builder's addendum. I reproduced them from the tape
without using the relayed platform numbers as input.

**Instrument.** Per replay: the round of the `removeEntity` on a Core id (`corpus/events.tsv`,
`ev=DEATH kind=core`), and the team index it belonged to. Rounds are 0-based
(`tools/replay_schema.md`), so `turns = max_round + 1`. This deliberately does **not**
descend from `winnerSide` — the TRAP 7 family — it is the in-replay core death.

**Result — match `28537dae`, OpenSverige v102 (seat A) vs The Bisons v4:**

| game | corpus `maxrnd+1` | corpus loser (team idx) | platform `turnsPlayed` | platform winner |
| --- | --- | --- | --- | --- |
| 1 | **74** | 0 (= us, side a) | 74 | THEM |
| 2 | **66** | 0 (= us) | 66 | THEM |
| 3 | **99** | 1 (= them) | 99 | US |
| 4 | **92** | 0 (= us) | 92 | THEM |
| 5 | **49** | 0 (= us) | 49 | THEM |

Five of five exact, on both turn count and winner. **FALSIFIER PASSES.**

**And the instrument was shown to be able to disagree.** Across all 7,289 metadata-matched
games where a single core died, the replay-derived losing team index agrees with the
metadata's `game_winner_side` in **7,288** and **disagrees in 1**; two further games
(`96d26726…_game_3`, `b7040beb…_game_3`) have **both** cores removed in the same round and
are excluded rather than guessed. A check that returns one dissent and two abstentions out
of 7,291 is a check; it is not a constant column.

**The lead is beyond five games.** The archive holds **195 Bisons game-rows**, and the
fast-kill property survives at that n (§3).

---

## 2. Populations, named once, and never pooled afterwards

| tag | population | n | clock / span | used for |
| --- | --- | --- | --- | --- |
| **P-3P** | Bisons vs **third parties** (no OpenSverige) | **140 games**, 21 distinct opponents, 15 distinct maps | Bisons v1–v4 | the mechanism |
| **P-102** | Bisons **v4** vs OpenSverige **v102** | **20 games** | one bot of ours | "their property or our hole?" |
| **P-BIS** | all Bisons games | 195 | v1:20 v2:75 v3:40 v4:60 | version span |
| **P-FIELD** | every non-Bisons game in `meta_join` | 9,839 games = 19,678 team-sides | whole archive | the baseline |
| **P-US** | OpenSverige team-sides | 2,513 | v80–v102 mixed | our own gap |

Fixture for every row below: `corpus/events.tsv` + `corpus/build_agg.tsv` +
`corpus/econ.tsv` + core positions parsed from the replay map headers. Unit is a
**team-side of one game** unless stated.

---

## 3. The table

### 3a. Speed — do they actually kill fast?

| subject | population | n | median kill turn | ≤100 turns |
| --- | --- | --- | --- | --- |
| Bisons core-kill **wins** | P-BIS | 77 | **77** | **72.7%** |
| Bisons core-kill wins | P-3P | 55 | 76 | 74.5% |
| Field core-kill wins | P-FIELD | 7,105 | 215 | **13.5%** |
| **OpenSverige** core-kill wins | P-US | 861 | 162 | 18.1% |
| Bisons **deaths** by core kill | P-3P | 73 | 109 | **47.9%** |

Unconditional, over *all* of a team's games — the number that matches the programme's
`core_kill_share × time_to_core_kill`:

| team | games | win rate | games ending in that team's ≤100 core kill |
| --- | --- | --- | --- |
| SingleCore | 90 | 43.3% | 28.9% |
| **The Bisons** | **195** | **40.5%** | **28.7%** |
| Cookie | 210 | 61.9% | 27.6% |
| Banminary | 290 | 33.4% | 25.9% |
| **OpenSverige** | **2,513** | **47.2%** | **6.2%** |

**Read the second row honestly: their win rate is 40.5%, below ours.** They are not a
better team; they are a *faster* team, and the programme's currency is speed, not win rate
(`PROGRAMME.md: WIN_RATE_IS_VERDICT: no`). They also *die* inside 100 rounds in 48% of their
third-party losses. The archetype is a coin-flip race, and both edges of it are sharp.

### 3b. What they build — Bisons vs field vs us, rounds 0–59, games ≥60 rounds long

Window fixed at r0–59 so game length cannot inflate anyone's counts.

| build | Bisons (P-3P, 114 sides) | field (19,380 sides) | us (2,504 sides) |
| --- | --- | --- | --- |
| builder bots | 4.32 | 5.08 | 5.28 |
| conveyors | **8.40** | 16.63 | **19.00** |
| harvesters | 2.41 | 3.17 | 3.41 |
| gunners | 0.78 | 1.54 | 0.47 |
| **sentinels** | **1.94** | 0.62 | 1.18 |
| launchers | **0.00** (0 of 195 games) | 0.34 | 0.57 |
| barriers | **0.00** (0 of 195 games) | 0.84 | 0.65 |
| splitters | 0.00 | 0.01 | 0.00 |

Whole-game totals, P-BIS, with the **same-file opponent as control**:

| refusal | Bisons total, 195 games | opponents in the **same 195 files** |
| --- | --- | --- |
| builder attacks (`batk`) | **88** (0.45/game) | 5,090 (26.1/game, max 404) |
| launchers built | **0** | 75 |
| barriers built | **0** | 361 |
| launcher throws (`throws.tsv`) | **0** | 519 |
| heals (`econ`, r0-150) | **0.0/game** | — (us: 94.7/game) |
| ammo converted (r0-150) | **448 Ti** in 18.8 calls | us: 284 Ti in 32.2 calls |

### 3c. Where the sentinel goes — computed to the NEAREST occupied core tile

The core is 2×2 and the engine's predicates work on tiles, so every distance below is
d² from the build tile to the **nearest of the four occupied enemy-core tiles**, never to
the anchor. This matters: on the anchor definition 85% of their fast-kill sentinels look
in-range; on the nearest-tile definition it is **142 of 142 = 100%**.

| subject (P-3P fast-kill games, 142 sentinel builds) | value |
| --- | --- |
| median d² to nearest **enemy** core tile | **16** (4 tiles) |
| median d² to nearest **own** core tile | **208** |
| distinct nearest-tile d² values observed | **only {4, 9, 16, 25}** — i.e. exactly 2, 3, 4 or 5 tiles |
| within sentinel range (r²=32) | **100%** |
| orthogonally aligned with a core tile (dx=0 or dy=0) | **142/142 = 100%** |

Field control on the same measurement (all non-Bisons forward in-range sentinels,
n=14,423): **56.6% orthogonal, 16.9% diagonal, 26.5% aligned with nothing.** Us
(n=2,601): 40.4% / 34.4% / 25.2%. The Bisons' 100%-orthogonal, 0%-diagonal, 0%-unaligned
split is a hard invariant of their code, not a tendency.

### 3d. The arithmetic check the brief asked for

A 500 HP core is 250 builder swings, 72 gunner shots, or **28 sentinel shots**.

- Their melee contribution in fast kills: **0 swings on the core in 41 of 41 games** → 0 HP.
- Their gunners in fast kills: 0.41/game, mostly at home (median d²_own 10).
- Turret shots fired per fast-kill game: **47.1 mean / 36 median** (`build_agg metric=shot`;
  `econ.shots` is the known-dead column, TRAP 5, and was not used).
- Window: median first forward sentinel r30 → median kill r69 = **39 rounds**, ≈19 volleys
  per sentinel at reload 2, across a mean 2.93 in-range sentinels → **~57 shots available**,
  28 needed.
- Ammo: 28 sentinel shots × 10 = 280 ammo, against **428 Ti converted** by r150.

Every leg closes. The kill is sentinel fire and nothing else, and the budget they refuse
(launchers, barriers, heals, half the conveyors, all melee) is exactly the size of the ammo
bill under a single global additive cost scale.

---

## 4. Mechanism vs marker

This is the part the brief was right to demand, and it is where my own expectation broke.

**The predictor is measured strictly before the outcome window.** Count the team's forward,
in-range sentinels standing **by round 45**, restricted to games still alive at r45, and ask
whether that team kills the enemy core **by round 100**. Temporal precedence holds by
construction; a consequence-of-winning cannot enter.

Forward = nearer to the enemy core than to its own. In-range = nearest-tile d² ≤ 32.

| forward in-range sentinels by r45 | P-3P (Bisons) | P-FIELD-wide (all teams) | P-US |
| --- | --- | --- | --- |
| 0 | 10/60 = **16.7%** | 612/17,235 = **3.6%** | 109/2,055 = 5.3% |
| 1 | 3/18 = 16.7% | 227/1,797 = 12.6% | 47/451 = 10.4% |
| 2+ | 27/56 = **48.2%** | 186/804 = **23.1%** | **0/2** |

Bisons 0 vs 2+: Fisher **p = 3.2e-04**. Field-wide, within the stratum that has no
off-axis sentinels at all, 0 vs 2+: **p = 1.9e-12**.

**Placebo, and it is null.** The same count restricted to sentinels **out of range**
(d² > 32) of the enemy core:

| out-of-range sentinels by r45 | P-3P | P-FIELD |
| --- | --- | --- |
| 0 | 29/95 = 30.5% | 823/15,934 = 5.2% |
| 1+ | 11/39 = 28.2% | 170/2,974 = 5.7%; 2+: 32/928 = **3.4%** |

Fisher p = 0.84. **"Sentinels" is not the variable. "Sentinels that can already see the
core" is.**

### Where I was wrong, and it changes the plank

**My prior, written before I ran the stratification:** the 100%-orthogonal alignment would
turn out to be the causal ingredient — a sentinel fires a single-tile-wide line, so being
on-axis with a core tile is what lets it hit. **It is not.** Stratifying the field-wide
predictor into line-aligned (orthogonal *or* diagonal — sentinels may face all 8 directions)
against aligned-with-nothing:

| count by r45 | line-aligned | aligned with nothing |
| --- | --- | --- |
| 0 | 523/16,277 = 3.2% | 904/18,825 = 4.8% |
| 1 | 280/2,568 = 10.9% | 99/925 = 10.7% |
| 2+ | 222/991 = **22.4%** | 22/86 = **25.6%** |

Both dimensions predict, at the same slope, and both survive stratification on the other
(p = 1.9e-12 and p = 2.3e-07). **The causal variable is the DOSE — how many sentinels are
standing in range of their core by r45 — not the geometry.** Alignment is a Bisons
fingerprint (100% vs field 56.6%) and a good way to *identify* their bot; it is not the
lever. A plank built on "align the sentinel" would be building the marker.

### And the plank is necessary-ish, not sufficient

Reach-rate versus conversion, per team, on the same instrument (team-sides of games alive
at r45):

| team | reaches 2+ by r45 | converts that into a ≤100 core kill |
| --- | --- | --- |
| Banminary | 78.6% (209/266) | 23.4% |
| Albert And Einstein | **61.9%** (117/189) | **11.1%** |
| gsxWins | 63.3% | 19.5% |
| Big O | 55.9% | 35.8% |
| **The Bisons** | **42.3%** (80/189) | **47.5%** |
| Cookie | 29.1% | **69.2%** |
| SingleCore | 42.5% | 56.8% |
| **OpenSverige** | **0.2% (4/2,508)** | **0/4** |

Albert And Einstein reach the position half again as often as the Bisons and convert it a
quarter as well. So the position is a gate, not a guarantee, and something else — most
plausibly the ammo discipline (428 Ti banked, in 16 large conversions rather than 33 small
ones) and the refusal to spend the scale factor on anything else — separates a 47%
converter from an 11% one. **I did not isolate that second factor and I am not claiming it.**

The one number that is unambiguous: **we have reached two forward in-range sentinels by
r45 four times in 2,508 team-sides.**

---

## 5. The within-Bisons contrast (the design the brief preferred)

All three cells are Bisons, P-3P, so opponent quality and our own bot are out of the picture.

| | fast kill ≤100 | slow kill >100 | loss / no kill |
| --- | --- | --- | --- |
| n | 41 | 14 | 83 |
| median turns | 70 | 132 | 112 |
| in-range sentinels/game | 2.93 | 4.93 | **1.53** |
| games with ≥1 | **90.2%** | 85.7% | **55.4%** |
| gunners/game | 0.41 | 0.93 | **1.71** |
| builder bots/game | 3.93 | 4.14 | **7.39** |
| builder bots **lost**/game | 0.24 | — | **3.70** |
| conveyors/game | 10.0 | 12.4 | 8.3 |
| builder attacks/game | 0.0 | 0.0 | 0.0 |

Raw sentinel counts are confounded by game length (slow wins last twice as long and have
more), which is exactly why the r45 time-matched predictor in §4 is the load-bearing test
and this table is context. What *is* clean here: their losses run **longer** than their fast
wins yet contain **half** the forward sentinels, twice the builder bots, four times the
gunners, and 15× the builder-bot deaths. **Their bot has two modes**, and the losing mode is
the one where the builders die on the way out and it falls back to gunners at home.

**The within-Bisons version contrast is the strongest control available and it is a natural
experiment they ran on themselves:**

| their version | n | forward in-range sentinels/game | gunners/game | share of ALL games that are their ≤100 kill |
| --- | --- | --- | --- | --- |
| **v1** | 20 | **0.00** | **5.50** | **0%** |
| v2 | 75 | 2.93 | 1.51 | 20% |
| v3 | 40 | 1.65 | 0.33 | 30% |
| **v4** (latest in archive) | 60 | 2.35 | 0.57 | **48%** |

**v1 is a pure gunner bot with zero forward sentinels and zero fast kills in 20 games.** The
same team then switched, and the fast-kill rate went 0% → 20% → 30% → 48%. The mechanism is
**present and strongest in their latest version**, so this is a live plank, not a historical
note. Everything in §3c/§4 rests on v2–v4; v1 is the negative control.

---

## 6. Is the 49-turn kill a Bisons property or a v102 vulnerability?

The brief asked me to check this explicitly and to say so loudly if the framing was wrong.
**It is mostly a Bisons property, but I cannot rule out a v102 component and I will not
pretend otherwise.**

| their version × our version | n | they ≤100-kill us | we ≤100-kill them |
| --- | --- | --- | --- |
| v2 × us-v80 | 15 | 7% | **53%** |
| v2 × us-v87 | 5 | 0% | 40% |
| v2 × us-v91 | 5 | 0% | 40% |
| v2 × us-v92 | 5 | 20% | 40% |
| v3 × us-v92 | 5 | 20% | **80%** |
| **v4 × us-v102** | **20** | **60%** | 20% |
| — v4 baseline vs third parties | 40 | **42%** | — |

- 60% (12/20) against our v102 versus **42% (17/40) against third parties with the same v4**.
  Fisher **p = 0.275**. The MDE for that comparison is **36pp** and the observed gap is
  **18pp**: **underpowered, verdict inconclusive.** Most of the 60% is explained by v4 alone.
- **But the direction of the whole matchup flipped**, and that is a finding the brief did not
  anticipate: against their v2/v3 *we* were the fast killer (40–80% of games), and against
  their v4 we are the victim (20% vs 60%). Both bots changed between those rows, so **this is
  unattributable from the tape** — it is equally consistent with "v4 got good" and "v102 got
  soft", and the archive contains no v102-vs-v2 games to break the tie.

---

## 7. Determinism — I tested it, and it is NOT there

The lead's parallel cut suggested fast killers are deterministic (identical build order,
identical kill round). **For the Bisons specifically that is false, and I want the
disagreement on the record.**

- Across their 41 third-party fast kills: **41 distinct first-40-build (round, kind)
  signatures out of 41 games.** Largest identical cluster: 1.
- First-**20**-build signatures: 36 distinct out of 41; largest cluster 4.
- Kill rounds spread continuously from 38 to 99 with no value occurring more than 3 times.
- Holding the map fixed does not rescue it: on their most common map size (25×25, n=12),
  **7 distinct signatures and 11 distinct kill rounds**; 16×16 (n=6): 6 signatures, 5 kill
  rounds.

What *is* tight is the **timing envelope**, not the sequence: build #1 lands at r0 in 41 of
41 games (IQR 0–0), build #6 at median r4 (IQR 3–6), build #10 at median r8 (IQR 7–9). So
the opening is **fast and rigidly paced, but reactive in placement** — consistent with a bot
that pathfinds to ore and to the enemy core rather than replaying a script. A builder should
implement it as a policy, not as a canned opening.

---

## 8. Branch B, checked and rejected

The brief called map/seat conditioning the most likely branch. It is not supported.

| conditioning variable | result (P-3P, 140 games) |
| --- | --- |
| map **area** ≤300 / 301–600 / >600 | 32% / 21% / 38% fast kills — no trend |
| map **identity** (md5 of the map tile bytes) | 15 distinct maps; **fast kills on 15 of 15** |
| seat | seat a 30/80 = 38%; seat b 11/60 = 18% — real asymmetry, but present in both |
| opponent | **14 of 21** distinct third-party opponents fast-killed |

The seat asymmetry is the only live conditioning and it halves the rate rather than
abolishing it. Note the seat here is derived from the in-replay core-death team index, not
from `ladder_games.seat` (TRAP 7) and not from `join.our_team`.

---

## 9. Controls — every one, and that both verdicts fired

| control | positive | negative — the case where it MUST come out the other way | fired? |
| --- | --- | --- | --- |
| core-death instrument | 7,288/7,289 agree with metadata winner | 1 disagreement + 2 double-core-death abstentions → not constant | ✅ |
| `batk` = 0 for Bisons | 191/195 Bisons sides = 0 | **same 195 files**, opponent side: 26.1/game, max 404, non-zero in 39% | ✅ |
| launchers/barriers = 0 | Bisons 0 and 0 | same files, opponents 75 and 361 | ✅ |
| throws = 0 | 0 Bisons throws | **519 opponent throws in the same files** → the instrument had coverage | ✅ |
| in-range-sentinel predictor | 3.6% → 23.1% field-wide, p = 1.9e-12 | **placebo:** out-of-range sentinels 5.2% → 3.4%, p = 0.84 | ✅ |
| alignment as mechanism | line-aligned 3.2% → 22.4% | **aligned-with-nothing also 4.8% → 25.6%** → hypothesis refuted, not confirmed | ✅ |
| version presence | v2–v4 have it | **v1: 0 forward sentinels, 0 fast kills in 20 games** | ✅ |
| nearest-tile vs anchor distance | nearest-tile: 142/142 in range | anchor: 120/142 = 85% → the two definitions genuinely disagree | ✅ |
| map conditioning | — | fast kills on 15/15 maps, 14/21 opponents → cannot be a matchup | ✅ |

`econ.shots` and `econ.deliveries` (TRAPS 5 and 8, both identically zero) were not used
anywhere. Shot counts come from `build_agg` with `metric='shot'`.

---

## 10. Power

| test | n | MDE (α=.05, 80%) | observed | verdict |
| --- | --- | --- | --- | --- |
| Bisons ≤100-kill rate vs field | 140 vs 19,678 | 8.2pp on a 13.5% base | +15.2pp | detected |
| r45 dose, within Bisons (0 vs 2+) | 60 vs 56 | 23.6pp on a 16.7% base | +31.5pp | detected, p=3.2e-04 |
| r45 dose, field-wide | 17,235 vs 804 | ~2pp | +19.5pp | detected, p=1.9e-12 |
| placebo (out-of-range) | 95 vs 39 | 23.6pp | −2.3pp | **null, and powered enough to exclude an effect of the size the real one has** |
| **v102 vulnerability** | 20 vs 40 | **36pp on a 42% base** | +18pp | **UNDERPOWERED — no verdict** |
| alignment as the lever | 991 vs 86 | ~13pp | −3.2pp | null; the aligned/unaligned slopes are indistinguishable |

The one null I report — alignment is not the lever — is powered against an effect of the
size that the dose effect itself has (+19pp); it is not powered against a small alignment
bonus on top of dose, and I do not claim one is absent.

---

## 11. What I could not see

- **Turret facing.** `Entity.gunner/sentinel.direction` exists in the replay schema but is
  not carried into any corpus table. Alignment is my proxy for "can this sentinel's line
  reach the core", and it is a proxy, not the predicate.
- **Damage attribution per shot.** Deliberately absent from the corpus (the v72 bleed decode
  mis-credited 5,359 vs 1,598). I inferred the sentinel-only kill from the *residual*: melee
  is 0, gunners are 0.41/game and at home, and the shot budget covers 500 HP. I did not watch
  a shot land on a core.
- **Which sentinel fired, and whether the core was the target** of any specific shot.
- **Map names** for third-party games (`meta_join` has no map column). I used md5 of the map
  tile bytes, which gives identity but not the organisers' name.
- **Per-round ammo and titanium balances** — in `updatePlayers`, not extracted.
- **Their source.** Everything here is behaviour, not code.
- One oddity I can see but not explain: the Bisons **time out constantly** — 70.5 TLEd unit-turns
  per game in r0–150 (fast-kill games: 29.9), against 1.15 for field fast-killers and 0.01 for
  us. Whatever their pathing does, it is expensive, and they ship it anyway.

## 12. What I deliberately did not measure

- **How the Bisons defend.** `PLAY_DEFENCE: never` — off-programme, and their losing mode is
  only characterised here as context for the within-Bisons contrast.
- **Their economy as a scoring channel.** `R1000_IS_DEFEAT: yes` demotes `titanium_collected`;
  I measured their conveyor/harvester counts only as *what they refuse to buy*.
- **The other fast killers** (Cookie 69% conversion, SingleCore 57%, Banminary, Big O). The
  reach/convert table in §4 names them because they falsify sufficiency, but characterising
  their mechanisms is the lead's parallel cut, not this one.
- **Anything about our own bot's code.** Read-only lane; our numbers here are tape only.

---

## 13. What a builder would implement — the smallest version

Branch **A**. Priced in `core_kill_share` and `time_to_core_kill`, as the programme requires.

> **Plank: get two sentinels standing within sentinel range of the enemy core by round 45.**
>
> Concretely, and nothing more than this:
> 1. From r0, spawn ~4 builder bots and send **at least two of them straight at the enemy
>    core** (its position is known from the map's symmetry). Do not stop to build economy en
>    route.
> 2. On arrival, build a **sentinel** on any tile whose d² to the **nearest of the four
>    occupied enemy-core tiles** is **≤ 32** — the Bisons live at exactly 2–5 tiles — facing
>    the core. Use `can_fire_from(pos, dir, SENTINEL, core_tile)` to pick the tile; that is
>    the engine's own predicate and it removes the whole alignment question.
> 3. **Build a second one.** The dose is the mechanism: 1 forward sentinel by r45 buys 12.6%,
>    two buys 23.1% (field-wide, n=19,836). One is barely better than none.
> 4. Convert titanium to ammo in **large lumps** — budget ≥ 280 (28 shots × 10), the Bisons
>    bank 428 — and keep the sentinels supplied over the ~39-round firing window.
> 5. **Do not buy:** launchers, barriers, splitters, heals, or any builder-melee line, and cut
>    conveyors to roughly half of what we build now (they run 8.4 by r60 against our 19.0).
>    Under one global additive cost scale, every one of those purchases raises the price of
>    the sentinels and the ammo, and the Bisons refuse all of them.
>
> **Falsifier for the leg:** if two forward in-range sentinels stand by r45 and the ≤100-round
> core-kill share does not clear ~20% against live unrated opponents, the dose reading is
> wrong and the difference lies in the conversion factor (§4), not the position.
>
> **The gap this closes:** we currently reach that position in **4 of 2,508 team-sides
> (0.2%)**. The Bisons reach it in 42.3% and convert 47.5% of the time. This is not a
> refinement of something we do badly; it is something we have never done.

**What must NOT be implemented from this document:** the 100%-orthogonal placement rule.
It is their fingerprint, it identifies their bot on the tape, and §4 shows it does not carry
the effect.
