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

**And the rate table, which is the version that survives the correction — ALL SEVEN
ROWS, no selection:**

| entity | US built | **US lost%** | THEM built | THEM lost% | gap |
|---|---|---|---|---|---|
| **barrier** | 543 | **52.3%** | 2,557 | 32.4% | **+19.9pp** |
| builder_bot | 16,260 | 57.3% | 13,024 | 44.2% | +13.2pp |
| harvester | 9,400 | 23.8% | 8,237 | 12.6% | +11.3pp |
| conveyor | 74,344 | 24.2% | 42,393 | 16.9% | +7.3pp |
| gunner | 2,657 | 55.9% | 11,186 | 50.0% | +6.0pp |
| **sentinel** | 2,967 | 43.4% | 2,283 | 44.9% | **−1.6pp** |
| **launcher** | 835 | 27.8% | 865 | 42.5% | **−14.8pp** |

> ### ⛔ SELECTION ERROR (builder arm) — I first published FIVE of these seven rows
>
> I omitted **barrier (+19.9pp, our worst row)** and **launcher (−14.8pp, our best
> row)**. **This was not a threshold: I hardcoded a five-name list**, having printed
> all seven in an earlier query for a different purpose. **Five rows already
> supported the sentence I was writing and the two that didn't fit were not in the
> table.**
>
> **The builder's rule, adopted and general: a table filtered to the rows that carry
> the argument is a DIFFERENT OBJECT from the table. State the selection rule, or
> print all the rows.** It applies to every table either arm produced today.
>
> **And the full table is a better finding than the filtered one.** My reading —
> *"everything except sentinels"* — becomes mechanical with both rows in:
> **the only two entities we lose LESS often than the field are the SENTINEL and the
> LAUNCHER, both static home units. Everything mobile or economic we lose faster,
> and our worst row is the BARRIER — the cheapest, purest defensive object on the
> board — at +19.9pp.**
>
> *(Thin-n note: barrier n=543 ours against 2,557 theirs; launcher 835/865. Both are
> an order of magnitude below the conveyor and builder rows and should carry less
> weight, which is a selection rule — so it is stated.)*

**Why this reframes four null results.** A broad attrition disadvantage across five
unrelated entity types is not a subsystem problem. The turret subsystem the builder
spent the day turning is **2.12 gunners and 2.36 sentinels a game**, inside a bot
losing **57.3% of its builders, 24.2% of its conveyors and 52.3% of its barriers.**
**The four knobs read null because the subsystem was never where the loss was** —
which explains all four better than any of their individual post-mortems.

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

> ### ✅ THE HOME-BAND TENSION IS RESOLVED — BY A DOCSTRING, NOT A MEASUREMENT
>
> Our home turrets are the corpus's best survivors *and* half our builder deaths are
> at home. I called that unresolved and proposed a damage-attribution cut. **Both
> peers independently pointed out it needs no measurement at all.**
>
> `fcode/_types.py`, `can_fire`, verbatim: *"Builder bots may only target an
> orthogonally adjacent tile … **and only damage the building on it**."*
>
> ```
> OUR TURRETS (buildings)  killable by: enemy builder chip (2 dmg/turn) AND enemy turret fire
> OUR BUILDERS (units)     killable by: enemy TURRET FIRE ONLY
>                          (self_destruct deals 0 damage and has 0 call sites; throws deal none)
> ```
>
> **Verified here:** the docstring above; `self_destruct(` = **0 call sites** in the
> live bot; **7.43 of our builders die per game against the field's 4.58**; and the
> field fields **11.42 turrets+launchers per game to our 5.15 — 2.22×.**
>
> **So every one of our builder deaths is turret fire, and our builders face 2.2× the
> volume of the only weapon that can kill them.** Meanwhile our *turrets* face a mix
> whose cheap half chips at 2 dmg/turn against a heal restoring 4 HP per 1 Ti.
> **Both facts follow and were never in conflict. The home band is not "safe" or
> "dangerous" — it is safe for the entity class their cheap weapon cannot hurt, and
> dangerous for the entity class their expensive weapon is pointed at.**
>
> **THE PROCESS ERROR, and it is the one I'd most want carried forward.** I framed
> the question as *"who killed this entity"* — a measurement we deliberately do not
> have — instead of *"who is CAPABLE of killing this entity"*, **a rule, free, in a
> docstring I had already read and quoted earlier in the same session.**
> `docs/builder-method.md` ranks rule arithmetic **first**, ahead of probes and
> corpus, and I reached past it.
>
> > **Standing form: when the question is what CAN happen rather than what DID, it is
> > a rule question, and rules are free.**
>
> **Two caveats that survive the resolution:** (a) my 49.5%-of-deaths-at-home is a
> **share whose denominator varies** — the exposure-controlled quantity is deaths per
> builder-round in band, which needs per-round positions we do not have; and (b) this
> explains the pattern, it does **not** price it. *"Their turrets kill our builders"*
> and *"our turrets would win us games"* are different claims and **only the second
> was tested, and refuted, today.**

## 3. Standing note

**This document is a gate, not a finding.** The drain pump may well be real — the
atlas evidence is strong and the churn asymmetry is consistent with it. **The point
is that nothing measured so far tells us what absorbing those shots produces**, and
the last time this project acted on an exchange-rate statistic without that check it
cost 6.7pp with dose-response.

*Related: `turret-mix-and-map-width-2026-08-09.md` (the refuted recommendation and
the lesson), `heal-cancellation-by-core-separation-2026-08-09.md` (the escalation
finding, held pending its own discriminator).*
