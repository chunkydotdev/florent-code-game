---
tactic: Commit only to tiles where AT MOST ONE enemy weapon can bear — a no-lose engagement invariant, computed not predicted
source: https://github.com/rooklift/halite2_rush_theory
origin: Halite II / rooklift (fohristiwhirl), "Theory and Practice of Halite 2 Rushes"
evidence: documented
transfers: yes
---
WHAT IT IS — The best-documented early-aggression result in any league in this
sweep, with a measured win rate attached. The bot was unremarkable in general
play; in rushes it was dominant:

> *"it had a winrate over 85%"* … *"In Finals, the bot's score in 2 player rush
> games was"* **1279-176**.

The mechanism is a **geometric invariant**, not tempo and not prediction:

> *"certain sweet spots emerge on the map where *at most* one enemy ship can come
> into range. If we put all our ships in those sweet spots, we can't lose, but we
> might win."*

and, decisively for a bot ladder:

> *"It's worth noting that this approach uses no prediction at all. We prepare for
> what the enemy could do, not what we think he will do. Therefore, it cannot
> really be exploited."*

WHY IT MIGHT TRANSFER — **This is the strongest new idea in sweep 14, because our
engine hands us the oracle it needs as a first-class predicate.**
`can_fire_from(position, direction, turret_type, target)` is explicitly the
*hypothetical-turret* form and **ignores ammo and cooldown** — i.e. it answers
"could a turret of this type at this place, facing this way, hit this tile?"
That is exactly rooklift's *"what the enemy could do"*, already implemented,
already cheap. `get_attackable_tiles_from()` is the same oracle in set form.

Applied to a Loki strike, the invariant is: **place a forward sentinel only on a
tile that (a) bears on the enemy core and (b) is bearable-on by at most one live
enemy turret.** The exchange arithmetic then favours us structurally:

- Our sentinel: 40 HP, 18 dmg, reload 2, and its line **ignores obstacles**, so
  barriers and bodies between it and the core do nothing.
- A single enemy gunner answering it: 7 dmg/round, and its line **is** blocked by
  their own bots and buildings — so their own heal screen partially blinds it
  (`the-blockade-blanks-your-own-guns.md`, `gunner-line-blinding.md`).
- Two enemy sentinels bearing on the same tile is the case the invariant forbids;
  one is a fight we win on HP-per-titanium.

The library's standing crack is *"concentration, not more damage."* This is the
defensive twin of it: **anti-concentration on our own exposed asset.** We already
maintain turret tiles in `blocked` in `_bfs_direction` with no range or
line-of-fire term — so we have a coarse version of this and are missing the
counting.

WHAT WOULD KILL IT — (a) rooklift's own stated breaker is terrain: *"Our theory of
combat suffers from literal edge and corner cases: we will generally be backing
away from enemy ships, possibly leading to us running out of space."* Our
buildings **cannot back away at all** — a sentinel is immovable, so a tile that
satisfies the invariant at placement stops satisfying it the moment the defender
builds one more turret. The invariant must therefore be re-evaluated every round
with a `destroy()`-and-relocate response, and `destroy()` is free, uncapped and
cooldown-less, which makes that unusually cheap here.
(b) A **launcher** ignores the invariant entirely: no facing, no ammo, and it
grabs the escorting builder rather than shooting the turret.
(c) Sentinel cost scale is +20% each, so a relocation that destroys and rebuilds
loses the scale contribution on destroy but re-pays the *current* scaled price.

BUILDER HOOK — A pure scoring function, no strategy change, testable offline
against the corpus: `bearing_count(tile)` = number of live enemy turrets for which
`can_fire_from(their_pos, their_facing, their_type, tile)` is true. Then (1) add
it as a cost term to `_bfs_direction` instead of the current binary block, and
(2) refuse any forward build on a tile with `bearing_count >= 2`. Measure forward
sentinel *survival rounds* and *damage dealt before death* — the library already
flags that our forward assets die fast, and this is the first candidate mechanism
that explains why in a way we can compute.
