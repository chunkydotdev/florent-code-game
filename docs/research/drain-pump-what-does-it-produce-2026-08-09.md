# The drain pump: what it costs them is measured; what it produces for us is not

**Research arm, session 23, 2026-08-09.** Corpus only. Zero downloads, zero arena.
**Version tag:** live **v91 "Eir 9c hivethaw (rollback from v90)"** = `bots/_v100hf`,
1530 @ 508, rank #35. Corpus join 1,255 rows, 100.0000% reconciled.

Written **before** the drain pump becomes a build, because it is structurally the
same kind of claim as the siting finding that cost a −6.7pp plank four hours ago.

---

## 0. The claim, and why it needs a check

The third lane's reaction atlas measured that the drain is **already happening
inadvertently**: 97.9-99.4% of opponent shots on our heavily-absorbing buildings
overlap heals, and **one Ouroboros gunner put 677 shots ≈ 2,708 Ti into a single
healed 3 Ti conveyor.**

**Independent corroboration from building churn** (1,255 games, my decode):

| | US built | US died | US loss% | THEM built | THEM died | THEM loss% |
|---|---|---|---|---|---|---|
| conveyor | 59.2 | **14.3** | **24.2%** | 33.8 | 5.7 | 16.9% |
| harvester | 7.5 | 1.8 | 23.8% | 6.6 | 0.8 | 12.6% |
| gunner | 2.1 | 1.2 | 55.9% | 8.9 | **4.5** | 50.0% |

Titanium value lost per game at base cost: **US 360 Ti** (223 of it *builder bots*,
43 conveyors) against **THEM 293 Ti** (137 builders, **89 gunners**).

> ### ⛔ CORRECTION (builder arm, same hour) — my reading of that composition was wrong
>
> I wrote *"we absorb into cheap things; they lose expensive ones"*, on 89 Ti of their
> gunners against 24 Ti of ours. **The field loses 89 Ti of gunners because it BUILDS
> 8.91 gunners a game to our 2.12.** Loss *rates*: **theirs 50.0%, ours 55.9% — they
> lose a SMALLER fraction, not a larger one.**
>
> **The 89-vs-24 gap is a production difference wearing a loss-composition costume.**
> It is not evidence that we successfully bait expensive things; it is the
> turret-count gap again, and that is refuted on three knobs. **Same error class as
> four others today: a ratio between two quantities where only one of them varies.**
>
> **What survives:** the conveyor asymmetry is a genuine *rate* difference (24.2% vs
> 16.9%), so we really do lose a larger share of our cheap buildings. **What does
> not:** any claim that the field's losses are skewed expensive relative to ours.

**And the rate table, which is the version that survives the correction:**

| entity | US built | **US lost%** | THEM built | THEM lost% | rate gap |
|---|---|---|---|---|---|
| **builder_bot** | 16,260 | **57.3%** | 13,024 | 44.2% | **+13.2pp** |
| harvester | 9,400 | 23.8% | 8,237 | 12.6% | **+11.3pp** |
| conveyor | 74,344 | 24.2% | 42,393 | 16.9% | +7.3pp |
| gunner | 2,657 | 55.9% | 11,186 | 50.0% | +6.0pp |
| **sentinel** | 2,967 | 43.4% | 2,283 | 44.9% | **−1.6pp** |

**We lose a higher fraction of everything we build except sentinels.** That is a
broad attrition disadvantage, not a subsystem one — and **the single entity where we
are at parity is the sentinel**, which is also the one that sits at home and whose
line passes through friendlies.

**But "2,708 Ti of their shots went into a 3 Ti object" is an EXCHANGE-RATE
statistic. It says what they spend. It does not say what we get.** That is exactly
the shape of *"our forward turrets survive at 19%"* — true, clean, and silent on
purpose. **The lesson from that episode is now standing: before recommending
something, measure what it PRODUCES, not what it costs the other side.**

## 1. The obvious test is confounded, and I am not offering it as evidence

Enemy shots per round against our win rate, length-controlled, 1,255 games:

| their shots/round | median | **our win%** |
|---|---|---|
| Q1 | 0.06 | **80.9%** |
| Q2 | 0.28 | 62.2% |
| Q3 | 0.49 | 48.6% |
| Q4 | 0.77 | 31.1% |
| Q5 | 1.24 | **25.1%** |

Monotone and steep against us. If enemy ammo were scarce and draining it were
profit, the slope should point the other way.

**It does not refute the drain pump.** Enemy shot count is an **opponent-strength
proxy** — a winning opponent shoots more because it has more turrets and more
targets. **The causation almost certainly runs backwards.** This is the
opponent-thermometer error already catalogued twice today
(`middle-game-hazard-and-economy-2026-08-09.md` §3), and calling this table a
refutation would be committing it a third time.

**What it does establish is narrower and still useful: the naive prediction fails,
so the obvious test cannot discriminate, and the drain pump must not be built on
the exchange-rate number alone.**

## 2. The two cuts that would discriminate

**Neither is runnable from our corpus — shot *targets* are not decoded here; they are
in the third lane's `rx` decode.** Both have been requested.

1. **Hold total enemy shots roughly constant; vary the SHARE absorbed by cheap
   healed buildings.** If, at a fixed level of enemy shooting, a higher
   absorbed-share predicts a better outcome for us, the drain is real and worth
   siting for. If the share does not move the outcome, those shots were going to be
   wasted anyway and baiting them buys nothing.

2. **Cheaper, and a cleaner causal chain: does the opponent's TITANIUM DELIVERED
   fall when their absorbed-share is high?** Ammo is bought 1:1 from titanium, so a
   genuine drain should show up as *less economy for them*, measured independently
   of the fight. **This routes around the dominance confound entirely**, because
   delivery is not a function of who is winning the exchange in the way shot count
   is.

## 2b. The largest un-examined line: builder bots

The builder arm opened it and it is worth recording where it sits.
**Builder-bot deaths are 222.9 Ti/game = 62% of ALL our losses**, at a loss rate of
**57.3% against the field's 44.2% (+13.2pp)** — and builder bots are joint
most-scale-expensive (+20% each), so every death is 30 Ti of replacement **plus** a
permanently steeper cost curve.

**A first cut on "what do those deaths buy" — where they die, relative to their own
core:**

| band | US | US % | THEM | THEM % |
|---|---|---|---|---|
| home d²≤8 | 1,877 | **20.1%** | 1,020 | 17.7% |
| near 9-32 | 2,737 | **29.4%** | 910 | 15.8% |
| mid 33-120 | 3,111 | 33.4% | 1,687 | 29.3% |
| far >120 | 1,600 | **17.2%** | 2,134 | **37.1%** |

**49.5% of our builder deaths are within d²≤32 of our own core, against 33.5% for the
field. Only 17.2% of ours die far from home, against 37.1% of theirs.**
Death rounds are near-identical (median 308 vs 319), so this is not a timing artifact.

**Our builders die at home. Theirs die away.**

**What this establishes and what it does not.** It constrains *what our dying builders
were not doing*: a builder that dies at d²≤32 of our own core was not projecting.
**It does not establish that those deaths were unproductive** — a builder healing a
besieged core and dying there is earning it exactly as a forward gun does. **This is
still a cost statistic.** Recorded as the largest un-examined line in the ledger,
**not as a queue item**, per the standing lesson.

## 3. Standing note

**This document is a gate, not a finding.** The drain pump may well be real — the
atlas evidence is strong and the churn asymmetry is consistent with it. **The point
is that nothing measured so far tells us what absorbing those shots produces**, and
the last time this project acted on an exchange-rate statistic without that check it
cost 6.7pp with dose-response.

*Related: `turret-mix-and-map-width-2026-08-09.md` (the refuted recommendation and
the lesson), `heal-cancellation-by-core-separation-2026-08-09.md` (the escalation
finding, held pending its own discriminator).*
