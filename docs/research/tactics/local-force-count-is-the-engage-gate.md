---
tactic: Four leagues converged on the same engage gate — the sign of (allies within r) minus (enemies within r), with r itself the tuned parameter
source: https://raw.githubusercontent.com/TheDuck314/halite2018/master/README.md
origin: Halite III TheDuck314 (6th); Halite II reCurse (1st); Halite III mlomb; Battlecode 2025 The Kragle
evidence: documented
transfers: partial
---

## WHAT IT IS

Independent top finishers in three different games reduce *"should I fight here"* to **one
signed integer**: the local count of my units minus the local count of theirs, inside a radius.

**Halite III, TheDuck314 (6th):**

> *"My general principle for 2p combat was that we should like collisions when we have a local
> numbers advantage"*

> *"I initial started with a radius much smaller than 8 but got big self-play improvements by
> expanding the radius to 8."*

**Referent check.** The score is defined in the same paragraph as, for each square occupied by
or adjacent to an enemy, `(allied ships within radius 8) - (enemy ships within radius 8)`; the
sign of that score is the whole decision — positive means accept collisions and ram, negative
means retreat. **The radius, not the threshold, was the parameter that mattered.**

**Halite II, reCurse (1st) — the same gate, but on the *economy* decision, with deliberately
asymmetric radii:**

> *"Once at destination, count undocked allied ships in a radius of 25"* … the source then
> reads, with `allyCount`/`enemyCount` marked as inline code:
> **`If allyCount > enemyCount, docking is authorized.`**

> *"Otherwise, hold position if the closest enemy has a distance over min(80, 20 + round) and
> does not have a docked ship."*

**Referent check.** *"docking"* is committing a ship to the economy — the opposite decision
from engaging. The radii are **25 for allies and 85 for enemies**, i.e. the count is
deliberately pessimistic: you must be locally superior by a wide margin before you are allowed
to stop fighting and start earning. And the fallback threshold **widens with the round number**
(`min(80, 20 + round)`), so the bot is paranoid early and relaxes later.

**Battlecode 2025, The Kragle**, listing what XSquare's near-universally-copied micro does:

> *"pushing an engagement when a robot senses it has many allies"*

**Halite III, mlomb** reduces it to a named scalar field with **two** thresholds separating
*permitted* from *preferred* (`friendliness_can_attack` below `friendliness_should_attack`).
*(Field name and mechanism verified present on the page; the threshold-pair reading is the
sweep's paraphrase of the page's parameter list, not a quotation.)*

## WHY IT MIGHT TRANSFER

The convergence is the argument: four teams, four rulesets, one gate. And our own arithmetic
says the gate matters *more* here than there, because our defender's edge is 2.2:1 (4.4:1 on a
stacked tile) — sub-threshold aggression is not merely wasted, it is a donation.

What is available cheaply in our engine:

- `get_nearby_units(dist_sq)` returns ids; `get_team(id)` classifies them. A signed count
  inside a chosen `dist_sq` is a few lines and one loop bounded by the vision radius.
- **The radius is the parameter TheDuck314 says matters**, and ours are fixed by the engine:
  builder r²=20, core r²=36, gunner r²=13, sentinel r²=32, launcher r²=26. So the tuning knob
  is *which unit's vision you evaluate the count from*, not the radius itself.
- reCurse's asymmetry has a direct analogue: count **our healers** in the tight ring
  (orthogonal adjacency, where `can_heal` actually works — d² ∈ {1,2,4,5}) against **their
  turrets** in the wide ring (up to sentinel r²=32, which ignores obstacles). Those are the two
  radii that actually govern the exchange here, and they are genuinely asymmetric for a
  physical reason rather than as a tuning choice.

`transfers: partial`, and the reason is the unit that does the counting.

## WHAT WOULD KILL IT

- **Counting bodies is the wrong denominator here.** In all four sources the counted units are
  *damage*. Ours are not: a builder bot deals 2 damage for 2 Ti and **cannot target enemy
  builder bots at all**. Ten of our builders next to one enemy gunner is a local numbers
  advantage of +10 and a losing fight. The transferable quantity is not unit count but
  **HP/round of healing versus HP/round of damage on the contested tile** — which the library
  has already priced, and which no source expresses as a count.
- **Our damage is immobile.** A signed count that says "retreat" cannot be acted on by a
  turret. The gate can only inform *placement* (see
  `initiation-is-a-placement-decision-not-a-fire-decision.md`) and *builder movement*.
- **Vision asymmetry.** A gunner (r²=13) counting enemies sees a smaller world than a sentinel
  (r²=32) does; the same rule evaluated by different unit types gives different answers, and
  our comms cost one round of latency to reconcile.
- TheDuck314's radius finding rests on **self-play** improvements — see
  `self-play-inflates-the-effect-by-about-2x.md` for what that instrument systematically
  overstates.

## BUILDER HOOK

Smallest test: before a builder commits to a forward seat, compute
`heal_capacity = 4 × (our builders on tiles orthogonally adjacent to the seat)` against
`incoming = Σ damage of enemy turrets whose get_attackable_tiles_from covers the seat`
(gunner 7/round, sentinel 18 every 2 rounds = 9/round). Refuse the seat when
`incoming > heal_capacity`. That is the four-league gate translated into our currency instead
of theirs, it uses only existing getters, and it is a `can_*`-style predicate that can be
logged for a battery before it is allowed to change any behaviour.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/TheDuck314/halite2018/master/README.md
- https://web.archive.org/web/20250912062821/https://recursive.cc/blog/halite-ii-post-mortem.html
- https://mlomb.dev/blog/halite-iii-postmortem
- https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
