---
tactic: WHAT SEPARATES A CONVERTER FROM A GRINDER — a standing unit allocation to the win condition, run unconditionally on the game state
source: https://battlecode.org/assets/files/postmortem-2024-cout-for-clout.pdf
origin: Battlecode 2024 / cout for clout; independently Battlecode 2023 / don't @ me
evidence: documented
transfers: yes
---
WHAT IT IS — Two teams in two different seasons, with two different win
conditions, independently answer question (B) the same way: they carve off a
**fixed allocation** of units and code whose only job is the win condition, and
they run it **regardless of whether the game state says they are winning**.

cout for clout (BC2024, capture-the-flag):

> *"Flag Sniping We allocate 3 ducks to be snipers, whose sole purpose is to
> harass the opponent / sneak their flag out."*

don't @ me (BC2023, capture-75%-of-islands, with a 2000-round anchors/resources
tiebreak) states the same policy as a deliberate *insurance* decision, and states
the failure it insures against:

> *"Teams that didn’t properly implement island capturing could lose a match even
> if they had a dominating economy and unit advantage."*

> *"we made sure to implement mechanics for capturing islands even if we were
> falling behind economically - it could help us eke out a win in otherwise
> hopeless scenarios"*

Referent check: "island capturing" is BC2023's *primary* win condition (control
75% of sky islands ends the game immediately), stated three sentences earlier in
the same section — so this is a quote about pursuing the KILL-equivalent
condition, not about a score.

And the same postmortem records what the ladder looked like *before* anybody did
this — which is the closest thing the field has to a measured decisiveness rate:

> *"In early rounds of development, such as sprint 1, most games were settled by
> tie-breakers, due both to the fact that most teams neglected to implement
> island capturing mechanics, and the fact that anchoring islands was not as
> powerful as it would become through later patches."*

**So the incidence of decisive games rose over one season, and the stated first
cause is that teams wrote the win-condition code at all.** The second cause is an
organiser buff, which belongs to question (D).

WHY IT MIGHT TRANSFER — Our measurement is that 74.4% of the core kills we *do*
land arrive inside r250; speed is not our constraint, incidence is. That is the
exact shape of don't @ me's sprint-1 ladder: not bots that were too slow at the
win condition, but bots with **no dedicated path to it**. Our bot's damage
assets are produced by the same loop that produces economy and defence, and
compete with them for the same titanium, so the win condition is only ever
attempted with the *residual*. A standing allocation makes it a first claim
instead.

The unconditional clause is the load-bearing half and it is the one that is
counter-intuitive here. Our library's own arithmetic says an attack we cannot
finish is a 2.2:1 donation, which argues for attacking *only* when ahead. don't @
me argue the opposite and give the reason: the win condition is worth pursuing
from **behind**, because it is the only branch on which a losing position can
still win. Both can be true — the resolution is that the allocation should be
**standing but cheap**, not a commitment of the whole bank.

WHAT WOULD KILL IT — Three ducks out of a BC2024 duck population is a rounding
error; three units out of ours is not. We are capped at **50 living units
including the core**, our only mobile unit costs 30 Ti at **+20% scale per
builder**, and every builder pulled off economy stops delivering titanium —
which is our **first tiebreak key**. So a standing allocation is charged twice
here: once in titanium and once in the fallback we are currently winning 57.2% of.
It would be defeated outright by a measurement showing that the marginal builder
is worth more on conveyor duty than on the core; the library has not made that
measurement, and it should be made before this is built.

There is also a live counter-example in our own corpus: the library's
`late-game-doctrine` note measured that **2.34% of forward throws at r200+ ever
land a single attack on the enemy core**. A standing offensive allocation run on
that road is a standing loss. This tactic is only worth anything if the allocated
units are pointed at the *clearance* phase (see
[`the-crunch-is-a-rate-race-not-a-damage-race`](the-crunch-is-a-rate-race-not-a-damage-race.md))
rather than at the core itself.

BUILDER HOOK — The smallest test is a **reserved store slot, not reserved units**:
dedicate one of the 16 comms slots to a "win-condition claim" — the id of the
enemy-core tile being worked and a count of our units committed to it — and have
the core's builder-spawn decision read that slot before it reads economy demand.
That makes the win condition a first claim on the *next* builder without paying
for a standing squad, and it is measurable as a change in core-kill incidence
with no change in build totals.
