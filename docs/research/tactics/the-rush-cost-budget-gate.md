---
tactic: The "rush cost" — a virtual surcharge on all non-rush spending before round 250, with an abort signal keyed to the forward building
source: https://battlecode.org/assets/files/postmortem-2020-confused.pdf
origin: Battlecode 2020 / confused (2nd place, high-school bracket)
evidence: documented
transfers: yes
---
WHAT IT IS — The single most directly buildable thing this sweep found, and it
names our own round number. confused observed that in mirror aggression,
defending is self-defeating:

> *"in a battle of rush vs. rush, it was mostly better to not defend, since
> defense meant that you couldn't spend more on offense."*

They then encoded that as a **budget priority, not a boolean mode**:

> *"we implemented a rush cost: if it's still before round 250 and the rush isn't
> over"* … *"then everything non-rush gets an additional rush cost of 250. This
> meant that we would always prioritize offense over defense."*

The abort condition is a **signal from the field unit about the forward
building**, not a timer:

> *"our rush miner signals that the rush is over when our design school is
> destroyed"*

And their target priority was deliberately NOT the base:

> *"prioritizing killing the enemy design school rather than the enemy HQ"*
> — because *"the design school can't do anything for 10 turns after it spawns"*,
> so killing the enemy's forward *production* suppressed the units that would
> contest theirs.

WHY IT MIGHT TRANSFER — Three separate pieces, all cheap:

1. **The surcharge shape.** A virtual cost added to every non-offensive build,
   evaluated against `get_global_resources()`, gives a smooth priority ordering
   instead of a mode flag that thrashes (see `defence-recall-oscillation`). It
   is arithmetic in the existing build-decision path, not a new state machine.
2. **The abort keyed to an artefact, not a clock.** Our store is 16 buffered ints
   with last-writer-wins; a single slot holding "forward plant alive / dead",
   written by whichever unit can see it, is exactly the idiom that survives our
   store semantics — no counter, no read-increment-write (which
   `store-semantics-2026-08-09.md` shows collapses silently).
3. **Kill the enemy's forward production, not their core.** Our analogue of a
   design school is an enemy **forward turret** or their nearest **harvester
   cluster**: the thing that feeds the defence rather than the defence itself.

WHAT WOULD KILL IT — Their premise is *"in a battle of rush vs. rush"*. Our
measured field **does not rush** (12% of top-tier kills by r100, median kill
r296). Against a defender who never attacks us, "prioritize offense over defense"
is not a symmetric trade — it is a unilateral drawdown, and our heal arithmetic
says an under-threshold offensive is a 2.2:1 donation. The surcharge is therefore
only safe if it is gated on evidence of enemy aggression, or on the Kragle
contested-opening trigger, rather than run unconditionally.

Second killer: their forward building spawned units at the target. **We cannot
build a builder-bot source forward** — only the core spawns builders, ≤1/turn,
on its own 12-tile ring. Our forward plant produces damage, not bodies, so the
"suppress their production" half has a much weaker analogue.

BUILDER HOOK — Smallest test: one store slot `SLOT_STRIKE_ALIVE`, one integer
constant `NON_STRIKE_SURCHARGE`, applied in the existing affordability check for
conveyors/harvesters/barriers while `get_current_round() < 250` and the slot is
non-zero. Zero new units. Measure on core-kill share and time-to-core-kill per
PROGRAMME, against LOKI-(N-1).
