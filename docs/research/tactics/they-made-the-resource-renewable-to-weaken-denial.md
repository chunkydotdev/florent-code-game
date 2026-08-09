---
tactic: THE COUNTERWEIGHT — organisers made the contested resource RENEWABLE specifically to weaken scorched-earth denial, and the field's eventual winner had to abandon the strategy it won a sprint with
source: https://github.com/Lux-AI-Challenge/Lux-Design-2021 (ChangeLog.md v2.0.2, local raw fetch) + https://www.kaggle.com/competitions/lux-ai-2021/writeups/toad-brigade-toad-brigade-s-approach-deep-reinforc
origin: Lux AI Challenge Season 1 (2021) — organisers' changelog, and Toad Brigade (1st place) describing the effect on their own agent
evidence: documented
transfers: no
---
⚠ **MIXED TIER. The changelog half is TIER 1** (raw bytes fetched directly from the
organisers' repo). **The Toad Brigade half is TIER 2** — read through a text proxy
rather than diffed against Kaggle's original HTML; see the summary's tier caveat.
The two halves are independent sources describing the same patch from opposite
sides, which is most of why this file is worth having.

WHAT IT IS — **The designer side (TIER 1).** Under `### v2.0.2`, one line changes
wood from a finite stock into a renewable one:

> *"Wood auto regrows each turn by 1% of its current valued rounded upwards and is capped at 400."*

(`valued` is their typo and is preserved. The regrowth rate was later raised again —
v3.1.0 reads *"Wood regrowth increased to 2.5%, previously was 1%"*.)

**The competitor side (TIER 2).** Toad Brigade, 1st in Lux S1, narrating their own
agent's trajectory across the season. The two spans below are **separated in the
running text by inline markdown links**, so they are quoted separately — joining them
would silently insert link syntax into the quotation:

> *"it learned the importance of denying the opponent access to resources, and used a scorched earth strategy to consume all the available resources without heed for its own survival - a strategy which was enough to win the August sprint prize."*

> *"However, after the rules change, (where wood regrowth was added and fuel costs were reduced to weaken swarming scorched earth strategies)"*

and what it became instead — *"and protecting the renewable forests"*, then
*"Finally, by the end of the competition, the agent has become a formidable player"*.

**Read the two halves together and the sequence is complete.** A maximally
aggressive denial strategy — consume everything, ignore your own survival — was
strong enough to **win a sprint prize**. The organisers then changed the rules to
weaken it *by name*. The eventual overall winner abandoned it and won on
conservation instead. This is a decisiveness lever that existed, worked, and was
deliberately removed by the people who wrote the rules.

WHY IT DOES NOT TRANSFER — Two independent blocks, either of which is sufficient.

**First, scorched earth requires a consumable resource, and ours is not documented
to be one.** Machine-checked over the whole of `docs/reference/official-docs.md`
(80,439 characters, flattened): `deplete` **0**, `exhaust` **0**, `runs out` **0**,
`finite ore` **0**. Nothing in the organisers' reference says an ore tile can be used
up. If ore is inexhaustible, *"consume all the available resources"* is not a legal
move here — there is no scorching to do. Note this is a **documentation** negative,
not an engine probe.

**Second, the denial we can do does not kill.** See
[`the-kill-mechanism-was-starvation-not-hp`](the-kill-mechanism-was-starvation-not-hp.md).
Toad Brigade's scorched earth won because a Lux city with no fuel is *"consumed by
darkness"*. Our core has 500 HP and no upkeep.

WHAT WOULD KILL THE "NO" — An arena probe showing ore tiles deplete. That single fact
would reopen this entire family and would be one of the more consequential engine
facts the library holds, because it would give us a starvation road we currently
believe does not exist. **It has never been probed and no file here claims to have
probed it.**

**AND THE PART THAT MUST NOT BE CHERRY-PICKED, which is why this file is filed as a
counterweight rather than a curiosity.** The programme's working assumption is that
decisiveness is a thing to be increased and that a league's history will show how.
Here a league's history shows a designer *reducing* it on purpose, and the strongest
agent in that league complying and getting stronger. Alongside
[`designers-flattened-the-skill-discontinuity`](designers-flattened-the-skill-discontinuity.md),
17A's map-pool finding, and Halite II's veto (*"Survival is part of the meta"*), that
is **four leagues where the design pressure ran against decisiveness and one (BC2020)
where it ran for it.** A programme premised on the opposite should hold that ratio
somewhere visible.

BUILDER HOOK — one probe, and it is cheap: **build a harvester on an ore tile in an
isolated match, run to r1000, and count the stacks it emits.** If the count is
`floor(1000/4)` with no falloff, ore does not deplete, this family closes for good,
and a paragraph of hedging can be deleted from three files.
