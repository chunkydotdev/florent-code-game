---
tactic: The cost scale does NOT price out a cheap decoy — but the builder-turn does
source: docs/reference/official-docs.md:1353,1424 (cost model) + bots/_probe_scale engine probe, s26, recorded in CLAUDE.md and docs/research/gunner-vs-sentinel-pricing-2026-08-09.md
origin: RESEARCH ARM INFERENCE (sweep 20A, 2026-08-10) — arithmetic on this repo's own measured cost model; no external competitor used a decoy (see the survey file)
evidence: inference
transfers: partial
---
WHAT IT IS — **A price check I ran because I expected it to kill the whole sweep, and it did not
kill the thing I thought it would.** Our engine has a mechanic no comparable league has
([`nobody-else-has-a-rising-build-cost`](nobody-else-has-a-rising-build-cost.md)): one global
additive cost factor, raised by *every* build, inflating *every* future build of *every* type.
The obvious objection to any decoy is therefore "a fake structure permanently taxes the real
rush". **Worked through against the measured model, that objection is close to false, and a
different one is true instead.**

The model is `cost = floor(scale × base_cost)`, scale additive from 1.0, and the increments are
wildly unequal: conveyor / splitter / **barrier +1%**, harvester +5%, launcher +10%, builder bot
/ gunner / sentinel **+20%**. Two consequences fall straight out of the `floor()`:

**1. Cheap decoy material is nearly free to build.** Barrier base cost is 3. From scale 1.0,
`floor((1 + 0.01i) × 3)` stays at **3** until `(1+0.01i)×3 ≥ 4`, i.e. **the first 34 barriers
each cost 3 Ti**. Five barriers cost 15 Ti flat.

**2. The inflation those five barriers impose on the real attack is ~1 Ti per turret.** Five
barriers put scale at 1.05. A sentinel (base 30) goes `floor(1.00×30) = 30` → `floor(1.05×30) =
31`. Three sentinels: **+3 Ti total.** A five-barrier decoy therefore costs about **18 Ti
all-in**, against a 500 Ti opening bank — under 4%.

**3. And the tax is refunded when the decoy dies.** The rules state destruction removes the
build's contribution to the scale. **A decoy that the enemy shoots gives our scale back.** A
decoy that is *ignored* keeps taxing us; a decoy that *works* is free. That inverts the usual
risk profile of a bluff, where being called is the expensive outcome.

**Material choice dominates everything else.** The same five bodies made of builder bots
(+20% each) would put scale at 2.0 and take a sentinel from 30 to 60 Ti. **Decoys must be built
from the +1% class — barrier, conveyor, splitter — and never from anything else.** This sharpens
the caveat already noted in [`ammo-drain-baiting`](ammo-drain-baiting.md) (*"barrier spam raises
OUR prices too, at +1% each"*), which is correct as stated but reads as a bigger objection than
the arithmetic supports.

WHY IT MIGHT TRANSFER — **because the real price is somewhere else, and it is a price the
programme actually cares about.** A barrier can only be built by a builder bot standing on an
**orthogonally adjacent** tile, and for a builder bot **acting and moving are mutually exclusive
in a round**. So one decoy tile costs **one builder-turn**, which is one round that builder did
not spend advancing on the enemy core. Against a target of a dead enemy core inside **250
rounds**, with the handful of builders our openings field, builder-turns — not titanium — are the
scarce resource. **The correct question is never "can we afford the decoy" (we can, trivially) but
"is one round of one builder's advance worth whatever the decoy buys".**

That reframing is what makes this file worth keeping even though its headline is negative: it
moves the decoy question out of the economy column and into the tempo column, where the
programme's currencies (core_kill_share, time_to_core_kill) can actually adjudicate it.

WHAT WOULD KILL IT — **the thing this file cannot supply: any evidence that an opponent reacts to
a structure at all.** The 22-postmortem survey found **zero** competitors who built a decoy
([`nobody-in-twenty-two-postmortems-built-a-decoy`](nobody-in-twenty-two-postmortems-built-a-decoy.md)),
so there is no external precedent that a bot's target selection or dispatch can be pulled by a
cheap building. If our opponents' builders and turrets simply engage whatever is nearest, a
barrier draws exactly as much attention as a wall and the decoy is 15 Ti and five builder-turns
donated. **Two further killers:** (i) the +1% tax is refunded on destruction only if the rule as
written holds under *enemy* destruction as well as our own `destroy()` — that distinction is not
separately probed anywhere in this repo and should not be assumed; (ii) `floor()` makes the
5-barrier arithmetic above scale-dependent — at a live scale already near a rounding boundary the
same five barriers can cost more, so the "18 Ti all-in" figure is a **round-0 figure**, not a
constant.

**Overlap note:** [`manner-pylon-and-what-the-rules-permit`](manner-pylon-and-what-the-rules-permit.md)
already establishes that a barrier is *"3 Ti at +1% scale"* and already specifies a
provocation read. **This file is not that plank; it is the price sheet under it** — the
`floor()` arithmetic, the +1 Ti-per-sentinel inflation figure, the destruction refund, and the
rule that decoy material must come from the +1% class. Read them together; do not run two
separate legs.

BUILDER HOOK — **do not build a decoy yet; measure the reaction first, from data we already
own.** `docs/research/opponent-reaction-atlas-2026-08-09.md` decoded 2,735 attributed replays of
the opponent side. The question to put to it costs no games: **when one of our non-threatening
structures (barrier / conveyor) appears inside an opponent's sensing range, does anything in
their behaviour change within the next ~5 rounds — a builder diverting, a turret rotating, a shot
spent?** If the answer is no across the five teams that hold our rating deficit, the decoy line
is closed for this field and this file becomes a `transfers: no`. If some team's builders divert,
the decoy becomes a tempo trade with a measured denominator, and the first leg is *one* barrier
placed on the approach by a builder already walking past it — the
[`the-trigger-rides-on-a-unit-already-going-there`](the-trigger-rides-on-a-unit-already-going-there.md)
construction, which reduces the builder-turn price to the single round the build itself costs.
