---
tactic: Import a hazard into the enemy base (cow delivery) — REFUTED for our ruleset
source: https://battlecode.org/assets/files/postmortem-2020-confused.pdf
origin: Battlecode 2020 — confused (implemented it), The High Ground (4th, lost a series to it)
evidence: documented (the tactic) / documented (our refutation, from our own rules)
transfers: no
---

WHAT IT IS — **the purest "poison their base" tactic any comparable league has
produced.** Battlecode 2020 had a neutral unit that emitted a debuff field:

> *"Cow: A neutral unit that produced a significant amount of pollution within a
> certain radius by farting."*

Pollution shrank vision and slowed actions. Delivery drones could pick up any
adjacent unit, including neutrals, so teams carried cows into the enemy base and
dropped them there. confused shipped it:

> *"we implemented sending cows over to the enemy HQ, and also drowning enemy
> units by picking up a nearby unit, travelling to the nearest water location and
> drowning them"*

**And it decided a final-tournament series.** The High Ground, the 1 seed, chose
not to implement it and named the omission as the cause of their loss:

> *"still didn’t drown cows or drop cows off near the enemy team like some
> others"*

> *"with 2 of their victories being on maps with very many cows"*

> *"there were so many cows near our HQ we failed to get our initial wall up"*

**This is the whole family working exactly as Magnus described it — nothing was
killed, a liability was simply moved into the opponent's base — and it beat the
top seed.**

WHY IT DOES NOT TRANSFER — **the mechanism has no counterpart in our engine, and
the nearest thing we do have runs backwards.** Four checks, all negative:

1. **There is no neutral entity.** Every entity in our game belongs to team A or
   team B. There is nothing on the map that harms whoever is nearest.
2. **There is no persistent debuff.** No pollution, no vision reduction, no
   cooldown penalty, no terrain the enemy can be made to stand in. Vision radii
   are constants per entity type; cooldowns are set by actions taken, not by
   surroundings.
3. **The one thing we *can* push into their base is titanium — and it helps
   them.** Our rules explicitly allow it: *"Resources can still be pushed onto an
   opposing team's conveyor network or core."* But their core accepts it as
   income, and **cumulative titanium delivered to core is tiebreak key #1**. So
   the only importable object in this game is a **gift**, not a poison. Anyone
   reading the "push onto their network" clause as an exploit has the sign
   backwards.
4. **The thing we *can* move — an enemy builder bot, via the launcher — is
   already theirs.** Dropping their own unit in their own base is not importing a
   hazard; it is a repositioning, and it is covered by
   [[blind-their-gun-with-their-own-body]] and [[score-the-throw-destination]].

**Recorded as a dead road so nobody re-derives it.** "Poison their economy" is
the most natural-sounding item on the dirty-tricks list and it is the one our
ruleset most completely forbids. The transferable residue of BC2020's cow work is
**not** the poisoning — it is the *delivery verb*, and that half is already
mined: the drone's pick-up-and-place signature is our launcher, and the field's
converged use of it was **defensive interception**, not import
([[launcher-defensive-interception]], [[displace-dont-kill]]).

WHAT WOULD REVIVE IT — one engine fact would flip this file, and it is worth a
single probe because it is cheap:

- **Does titanium pushed into an enemy core credit *their* delivery total, or
  ours?** If the engine credits delivery to the *pushing* team, then feeding an
  enemy core is a tiebreak-key attack rather than a gift, and this file becomes
  live under a different name. Our reading of the rules says it credits them, but
  we have **not measured it**, and the tiebreak is the key we win 57.2% of
  r1000 games on.

BUILDER HOOK — none for the tactic. **One probe for the revival condition:** a
local game where we route a stack into the enemy core and read both teams'
delivered-titanium counters. If it credits them, close this file permanently.

Related: [[launcher-defensive-interception]] · [[displace-dont-kill]] ·
[[ore-tile-denial]] · [sweep 3](2026-08-09-sweep-3.md)
