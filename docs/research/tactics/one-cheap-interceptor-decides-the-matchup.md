---
tactic: FAILURE MODE — a single cheap mobile interceptor, built early, kills the whole rush meta
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf
origin: Battlecode 2020 / Java Best Waifu (finalists) — the team that broke the BC2020 rush meta; corroborated by confused and The High Ground
evidence: documented
transfers: yes
---
WHAT IT IS — BC2020 had a rush meta that *worked*. It was ended by one team
building one cheap mobile unit early. Their own account:

> *"rush bots have a hard time trying to get their rush Miner close to our HQ
> because we started building Drones really early"*

confused, from the losing side, name the same cause and it is worth reading as
the field's verdict rather than one team's opinion:
> *"The key to their success was their early drone"*
Referent: "their" = Java Best Waifu, who *"rose up and took the first place in the
scrimmage ladder"* while *"not a rush bot like virtually every other top team"*.

And here is the sentence that should be pinned above the Loki plank, because it
reduces an entire matchup to one coin:
> *"Our games against Kryptonite depended almost uniquely if our initial drone was
> able to repel or capture their rush miner or not."*

The mechanism is **displacement, not damage** — The High Ground record winning the
games where they *"pick up and drown their rushing"* miner.

WHY IT MATTERS HERE — Because we have that unit, and so does the field. The
**launcher** is 20 Ti base, +10% scale (the cheapest scaling tier of any combat
building), needs **no ammo at all**, is **facing-independent** with vision/attack
r²=26, and *"picks up an adjacent builder bot from either team and throws it to a
passable tile."* Against a Loki strike that depends on one or two builder bots
reaching the enemy core, a single defensive launcher is close to a hard counter,
and it costs the defender roughly the price of one harvester.

Our own library already documents the field converging on exactly this use:
`launcher-defensive-interception.md` and sweep 12's finding that BC2020's field
*"converged on grabbing the enemy's unit defensively, never on ferrying their own
forward."* **That is the same finding arriving from the other direction: the
counter to our plank is a tactic our own research already says the field
prefers.**

Three aggravating factors specific to us:
1. Our strike builder cannot fight back. Builder attacks cannot target builder
   bots, and a launcher is a *building*, so the only answer is to destroy the
   launcher itself — 30 HP at 2 dmg per 2 Ti = **30 Ti of attacks**, more than the
   launcher cost, while standing adjacent to it.
2. The throw destination is chosen by *them*: "any passable tile" in r²=26 means a
   rejected builder can be put ~5 tiles back, wiping ~5-10 rounds of approach at
   zero ammo cost, repeatedly.
3. It is cheap enough to be incidental. A defender does not need to predict a
   rush to own one.

WHAT WOULD KILL THE COUNTER (i.e. what we would need) — The launcher must be
**orthogonally adjacent** to the bot it lifts. So the counter to the counter is
approach geometry: never route the strike builder through a tile adjacent to a
live enemy launcher, and treat launcher-adjacency as a hard block rather than a
cost. That is the same routing edit `retreat-and-return-under-the-counter-unit`
asks for, and it is currently absent — `_bfs_direction` blocks turret tiles with
no range or line-of-fire term.

BUILDER HOOK — Corpus query first, and it is nearly decisive for the programme:
**how many enemy launchers are alive at r100/r150/r200 in our ladder games, and
what fraction of our forward builder deaths/displacements are attributable to
them?** If the field already fields launchers at home by r150, the plank must be
designed around them from the first iteration rather than discovering them in a
battery.
