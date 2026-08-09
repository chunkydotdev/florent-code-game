---
tactic: The worker pull (workers as emergency combatants) — the standard RTS answer to "when does a worker stop mining"
source: https://liquipedia.net/starcraft/SCV
origin: RTS theory, StarCraft Brood War (Liquipedia community wiki, "SCV"); contrast case from Battlecode 2020 / confused
evidence: documented
transfers: no
---

WHAT IT IS — in every mainstream RTS, the canonical answer to "when does a worker
stop mining and start doing defence" is **it stops mining and starts shooting.**
The worker is a weak but real combat unit, and pulling six or eight of them is
the cheapest emergency army in the game. Liquipedia states the underlying reason
in one line:

> "The SCV has 50% more total HP than the drone or probe and deals 47% more
> damage per second, making it a superior fighter in large numbers."

This is why the RTS literature on worker-time allocation is mostly about *combat*
allocation, and why SCV repair is a comparatively small sub-doctrine sitting
alongside it. The same article's §Competitive Usage lists repair, scouting,
proxy-building, drawing fire, mineral-walking units across patches and
body-blocking as parallel uses of the same body, with combat value assumed
throughout. *(Paraphrase of the section's contents, not a quotation.)*

WHY IT DOES NOT TRANSFER — **our builder bot has exactly zero combat capability
against anything that can be pulled against it.** The ruleset is explicit: a
builder's attack does "2 dmg to the **building** on an orthogonally adjacent
tile". Builder bots cannot damage enemy builder bots at all — this is the fact
that already underwrites the 2.2:1 defender's edge in
[`heal-arithmetic`](../heal-arithmetic-2026-08-09.md), and it kills this tactic
from the other direction as well:

- Fifty builders cannot kill one enemy builder. There is no "in large numbers"
  effect to reach.
- Against an incursion of enemy **builders** — which is what an attack on us
  actually looks like, since only builders are mobile — a worker pull produces
  literally no damage. The only counter is a turret.
- Our builders also cannot draw fire usefully: a builder body absorbs turret
  shots, but at 40 HP and 30 Ti × (+20% scale) it is a poor ablative compared to
  a barrier at 30 HP and 3 Ti × (+1%) — the point already made in sweep 7's
  barrier-screen finding.

**The single narrow exception:** a builder *can* attack enemy **buildings**, so
"pull builders onto a planted enemy gunner in our base" is a real move. But that
is the removal race already priced in [[sustained-plant-removal-race]] and
[[standoff-removal-outranging]], not a worker pull — it is a demolition detail,
it cannot defend anything, and it is exactly the action the enemy's healers
cancel at 4 HP/Ti against our 1.00 HP/Ti.

WHY FILING IT MATTERS — because it changes the reading of our own measurement.
The field's builders die next to their own turrets at lift **5.04** in their home
band and 42.2% of their forward builder deaths are there. In an RTS that shape
would be ambiguous between "they pulled workers to fight" and "they were
repairing". **Here it cannot be the first.** Our rules leave exactly one thing a
worker standing at a turret can be doing: keeping it alive. That is what makes
[[worker-fortified-turret-cell]] the forced interpretation rather than one of
two, and it is the reason this negative is worth a file.

It also warns off a specific class of import. Any source describing worker-time
allocation in a game where **workers can attack units** — which is nearly all RTS
writing, and much of the Battlecode corpus (BC2020 miners built net guns but
landscapers buried units; BC2022 builders could not fight but soldiers could) —
is describing a decision we do not get to make. The Battlecode 2020 team
*confused* reached the sharpest version of the RTS conclusion:

> "We also noticed that in a battle of rush vs. rush, it was mostly better to not
> defend, since defense meant that you couldn't spend more on offense."

That is a real result about a **shared** resource pool feeding both offence and
defence. It is not a result about worker time, and importing it as one would be
a category error.

BUILDER HOOK — none, deliberately. The only actionable content is a filter on
future sweeps: **a source that assumes workers can trade damage with enemy
workers is not describing our economy/defence split**, and its allocation rules
should be discarded rather than adapted.

Related: [[worker-fortified-turret-cell]] · [[sustained-plant-removal-race]] ·
[heal arithmetic](../heal-arithmetic-2026-08-09.md)
