---
tactic: Generality and robustness carry you to the top of the mid-field and then stop paying
source: https://battlecode.org/assets/files/postmortem-2023-dont-at-me.pdf
origin: Battlecode 2023 / don't @ me — a low-seeded team that upset the 8th seed in two consecutive tournaments
evidence: documented
transfers: partial
---
WHAT IT IS — **This is the sweep's cleanest answer to "is the top tier different in KIND or in
DEGREE", and it is answered by the one team best placed to know: a team whose upsets came from
generality, reporting where generality ran out.**

> *"we focused almost entirely on generality and robustness, which got us towards the finals"*
> … *"at the highest elo, generality and robustness starts to take a back seat to legitimate
> higher-level strategy"* … *"We didn’t have enough time to pivot our designs out towards
> having more specific strategies for specific map states."*

(The referent of *"which got us towards the finals"* is their own generality-and-robustness
focus, stated in the same sentence; the contrast drawn is between that focus and *"more
specific strategies for specific map states"*, which is what they say the highest-Elo teams
had.)

So the answer is **different in kind, in a named direction**: the mid-field ceiling is a bot
that does one sound thing everywhere, and the top tier's extra ingredient is *conditioning on
the situation*. Robustness is the floor, not the ladder.

WHY IT MIGHT TRANSFER — **It speaks directly to today's measurement.** We measured our
defensive shape as *more of the same* as the mid-field's — collar occupancy 67.3% against a
third-party field average of 53.2%. don't @ me's account says that is precisely the axis that
saturates: doing the field's thing harder is what gets a team *to* the mid-field ceiling, and
past that point the return comes from **branching on state**. That claim also lands on top of a
gap sweep 15 already named from a different direction: *"The one qualification — an opening
unconditional on MAP GEOMETRY — is a documented failure mode, and our own width gradient is
it."* Two independent sweeps, two independent sources, same missing ingredient — **conditional
behaviour**, not more of the current behaviour.

WHAT WOULD KILL IT — **The sentence is a self-assessment of a shortfall, not a measurement of
what the top teams actually did.** don't @ me infer the top tier's ingredient from losing to
them; they never open a top bot and confirm it. And "specific strategies for specific map
states" is their game's vocabulary — Battlecode 2023 had wells, islands, clouds and currents
generating map states that our engine has no analogue for. Our map varies in **size, symmetry,
ore layout and passability** and little else, so the space of "map states" we could condition on
is far smaller, and it is entirely possible that we exhaust it in one branch. Also note the
direct tension with [`the-top-tier-is-parity-plus-one-gimmick`](the-top-tier-is-parity-plus-one-gimmick.md),
where the BC2025 winner says the general game plan was the *same* for all top teams — these two
sources genuinely disagree about how much of the top tier is shared, and both are filed.

BUILDER HOOK — Ask the corpus a question before writing any branch: **does our win rate against
the 1900+ band vary with a map property we currently ignore** (width, ore count, core-to-core
distance)? INDEX already records that our own width gradient is an unconditional-opening failure
mode. If the gradient against strong opponents is steeper than against weak ones, that is the
"specific strategies for specific map states" gap made concrete, and the smallest plank is one
geometry branch — not a general capability.
