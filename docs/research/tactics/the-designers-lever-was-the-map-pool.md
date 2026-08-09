---
tactic: (D) WHEN ORGANISERS WANTED MORE (OR LESS) DECISIVE GAMES, THE INSTRUMENT THEY REACHED FOR WAS THE TOURNAMENT MAP POOL — three teams, three seasons, same observation
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
origin: Battlecode 2020 / The High Ground and Confused; Battlecode 2025 / The Kragle
evidence: documented
transfers: partial
---
WHAT IT IS — Across three independent postmortems in two seasons five years
apart, competitors report the organisers steering the offence/defence balance —
and therefore whether games end in a kill — **through map selection**, without
touching a single unit stat.

The High Ground, on the same season in both directions:

> *"was weighted toward small and easily pathable “rush-friendly” maps"*

Referent: the subject of that clause is *"the early map pool"*, three words
earlier in the same sentence (a figure caption interrupts the sentence in the PDF
text, which is why the two halves are quoted separately here). And then, at the
tournament:

> *"the devs indirectly nerfed rush through large and hard-to-path maps in the
> seeding tournament"*

Confused, independently, on the same tournament:

> *"Teh devs had put pretty anti-rush maps as well."*

The Kragle, five seasons later, states it as a standing pattern rather than an
incident:

> *"Teh Devs have historically shown favoritism to teams that prioritize
> economy-based gameplans (as opposed to rush/attack based gameplans) by making
> maps in the finals tournament larger and slower."*

**The word to notice in The High Ground's sentence is "indirectly".** The
organisers did not nerf rushing; they changed where it was played. And the effect
was decisive at tournament scale — the same passage records that *"Some very
strong rush teams were knocked out pretty early"*.

The Kragle also records the direction the designers push when they *do* touch
stats, and it is the opposite of ours:

> *"We believe this would add an extra dimension to any meta, since every
> Battlecode meta usually devolves into “always attack.”"*

Referent: "this" is static defence being allowed to be strong — the sentence
before argues the RTS counter to static defence is to disengage and out-economise.
The claim being made is that Battlecode metas collapse into universal aggression,
which is the mirror image of our league, where the arithmetic collapses into
universal defence.

WHY IT MIGHT TRANSFER — Not as a lever — we do not choose maps. It transfers as a
**confound and a measurement instruction.** If the decisiveness of a game is
substantially set by its map, then our core-kill incidence is a mixture over the
map distribution we happen to draw, and a bot change that raises incidence on
open maps can be invisible in the aggregate. The library already holds
[`a-hundred-elo-of-map-distribution`](a-hundred-elo-of-map-distribution.md) and
[`map-size-decides-whether-the-rush-is-legal`](map-size-decides-whether-the-rush-is-legal.md);
this adds the specific claim that **kill incidence, not just rush legality, is a
map property** — and it is sourced to organisers using it deliberately.

The two map axes the sources name are exactly the two we can measure from the
corpus without any bot change: **size** ("small" vs "larger and slower") and
**pathability** ("easily pathable" vs "hard-to-path"). Our maps run 8x8 to 30x30
with WALL tiles, so both axes exist here.

WHAT WOULD KILL IT — Battlecode maps are 20x20 to 64x64 and hand-authored per
tournament by a dev team with an aesthetic agenda; ours are 8x8 to 30x30 and
drawn by the league. If our map pool has little variance on size or wall density,
the mechanism is real but has no room to act, and the confound is not worth
controlling for. That is checkable in the corpus in one query.

A second and more interesting failure mode: the *direction* is not fixed. The
same instrument was used in BC2020 to suppress rushing and in BC2020's early
ladder to encourage it. So "map explains incidence" is not the same as "bigger
maps mean fewer kills" — the sign has to be measured here, not imported.

BUILDER HOOK — none in the bot. A corpus cut: core-kill incidence by map area and
by wall-tile fraction, for us and for the field separately. If incidence is
strongly map-graded, every subsequent incidence A/B must be blocked on map class
or it will measure the draw rather than the change — and that is the same defect
sweep 15 named when it warned that a paired differential whose variance lives on
the other side of the subtraction is an opponent thermometer.
