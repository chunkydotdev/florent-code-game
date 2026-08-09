---
tactic: The raider that plants a turret BEFORE it arrives — a documented counter to interception
source: https://battlecode.org/assets/files/postmortem-2020-confused.pdf
origin: Battlecode 2020 / confused ("We also placed 2nd in the high school bracket, and ended up 6th in the scrimmage servers"), describing their opponent Kryptonite
evidence: documented
transfers: partial — as a PREMORTEM against our own launcher doctrine, not a tactic to adopt
---

WHAT IT IS — confused built, in 2020, almost exactly the defence this library is
currently proposing: a grab-capable unit held at home to pick up and remove the
enemy's incoming raider before it could act. **It was beaten by a build order,
not by a fight.**

> "Kryptonite responded by implementing building net guns even before they
> reached the HQ, preventing our drones from picking them up."

and the figure caption in the same document:

> "While we have defensive drones in place, their miner preemptively builds a net
> gun, nullifying our defense."

They also record the tempo, which is the part that should worry us: "they
submitted their change right before the deadline so we didn't have any time to
respond."

WHY IT MIGHT TRANSFER — **[[launcher-defensive-interception]] is the same
defence**: hold a displacement unit at home and remove the raider before it
plants. The BC2020 counter is available here in a near-identical form, and one
rule makes it *stronger* against us than it was against confused:

**`can_launch` requires the target builder bot to be ADJACENT.** The launcher's
r²=26 is its vision/throw radius, not its reach — the pickup is adjacency-gated.
So a launcher doing its job must stand within one tile of the raider, which is
deep inside a gunner's r²=13 kill zone. A raider that plants its gunner *first*,
then works next to it, forces our launcher to enter that zone to function.

The arithmetic once it does: **launcher 30 HP; gunner 7 dmg, reload 1 → ~9 rounds
and 20 Ti of ammo to kill it, with no reply of any kind** — a launcher cannot
fire on a building, it can only throw builder bots.

And the geometry says this is not hypothetical. The **median planted-gunner
distance to our core is d² = 20 (p25 13, p75 29)** — a launcher sited tight to the
core does not cover the band where plants actually land, and a launcher sited to
cover that band is standing in it.

WHAT WOULD KILL IT — honestly, timing:

- It costs the opponent a build-order change they have **no reason to make until
  our launcher costs them games.** This is a premortem about the *second*
  matchup, not the first, and pre-emptively engineering around it would be
  paying now for a counter that does not exist yet.
- The escape geometry does exist. Nothing forces the launcher to sit in a lane;
  a gunner's coverage is a **facing line**, not a disc, and we can read that
  turret's facing directly. A launcher one tile off the lane is untouchable by
  that gunner without a 10 Ti rotate.
- If the opponent's raider *must* be adjacent to one of our buildings to attack
  it, the launcher's adjacency comes free — which is the original argument in
  [[launcher-defensive-interception]] and it is unaffected by this file.

BUILDER HOOK — **a siting constraint and one counter, both cheap:**

1. Prefer launcher tiles that cover the measured plant band (**d² 13–29**, the
   p25–p75 of plant distance to our core) while **not lying on the facing line of
   any enemy gunner already planted there.**
2. Instrument: count games in which our launcher **dies to a gunner before
   making a single grab.** If that number is materially non-zero once launchers
   ship, the premortem has arrived and the siting rule earns its complexity. If
   it stays near zero, this file is a filed hazard and nothing more.

The open prerequisite from [[launcher-defensive-interception]] still gates this
file too and is unchanged: **is `can_launch` adjacency 4-way or 8-way?** An
8-way pickup buys a diagonal standoff that a 4-way one does not.

Related: [[launcher-defensive-interception]] · [[displace-dont-kill]] ·
[[escorted-forward-plant]]
