---
tactic: Park the scout where its presence also denies economy — the reconnaissance stops being a cost
source: https://battlecode.org/assets/files/postmortem-2019-smite.pdf
origin: Battlecode 2019, smite (finalist)
evidence: documented
transfers: partial
---

## WHAT IT IS

smite added scouting late, and states its necessity in terms that match our situation exactly:

> *"One of the features we’d always planned on implementing but never had gone around to was
> scouting."*

> *"Scouting is essential in a game like this, where responding to the enemy is key. There is
> no dominant strategy but rather counters for every approach."*

> *"instead of tuning to be more defensive against rush bots like DOS, we decided to send one
> prophet scout on 1 v 1 maps to the enemy castle"*

**Referent check.** *"a game like this"* is Battlecode 2019; DOS is a named opponent running
*"a very aggressive, sustained preacher attack strategy"*. The choice being made is explicit:
**one scout instead of a global defensive tuning** — reconnaissance bought in place of a
posture change.

The scout was a **tripwire** with a defined reaction, not an explorer:

> *"if it ever saw a preacher rush, it would immediately scream back to the castle, which would
> produce 3 more prophet scouts who could effectively kite and out maneuver preachers in the
> middle of the field"*

And the two sentences that make this file worth writing — the cost accounting:

> *"At best, it saved us the game, and at worst, it was almost no loss."*

> *"pilgrims couldn’t actually mine any tiles in front of the castle which were in the
> prophet’s attack range until it was killed, giving us valuable economic suppression"*

**Referent check.** *"pilgrims"* are the **enemy's** economic units and *"the castle"* is the
enemy castle — the scout is parked outside the enemy base. *"the prophet's attack range"* is
the scout's own threat radius. The scout is not merely cheap; **its position denies the
opponent's mining**, so the reconnaissance runs at a *negative* net cost while it lives.

## WHY IT MIGHT TRANSFER

The brief names the objection this file answers: *our only mobile unit is also our only builder,
so every scouting round is a build round forgone*, and acting/moving exclusivity means a scout
that acts does not move. smite's answer is not "make the scout cheaper" but **"make the scout's
position do a second job"**.

Our engine has exactly one unit that denies tiles by existing, and it is not the builder:

- A **gunner** (20 Ti, r²=13, 7 damage, 4 ammo/shot) or **sentinel** (30 Ti, r²=32, 18 damage,
  10 ammo/shot, **line ignores obstacles**) placed toward the enemy half both **sees** and
  **threatens**. `get_attackable_tiles()` is its denial footprint, and the sentinel's is
  unblockable by intervening bodies.
- Harvesters can only be built on ore. A turret whose attack pattern covers an enemy ore tile
  makes building there expensive in a way that costs us nothing per round except ammo we choose
  to spend — and `ore-tile-denial.md` already records the denial half of this idea from another
  direction.
- The **builder that places it** goes home. The persistent forward presence is a building, not a
  unit-turn, so it does not consume the scarce resource (builder rounds) every round the way a
  patrolling scout would.

That reframes the cost problem: **the recurring cost of a forward scout is builder rounds; the
cost of a forward turret is a one-off titanium payment plus its own survival.** Our library has
already measured the survival side hard — sweep 5's turret-survival flip, and the ablative
barrier screen at ~8× HP/Ti which is **sentinel-only** because a barrier ring blinds a gunner
and does not blind a sentinel.

## WHAT WOULD KILL IT

- **`THE FORWARD ROAD IS CLOSED` on three instruments**, and this is a forward placement. This
  file does not reopen it. What it changes is the *justification*: a forward turret proposed as
  **a sensor and a tax** is a different object from a forward turret proposed as **damage**, and
  the instruments that closed the road measured the latter (2.34% of forward throws at r200+
  ever land a single attack on the enemy core).
- **smite's prophet could retreat and re-aim; our turret cannot.** A scout that dies has cost
  one unit; a turret that dies has cost titanium *and* raised our own scale permanently for that
  category (+20% gunner/sentinel), which is a cost the sources never pay.
- **The denial is only as good as the ammo behind it.** With no passive ammo income and 1:1
  conversion competing with build spending, a forward gunner that cannot afford to fire denies
  nothing — an opponent can simply walk through an unloaded threat. smite's prophet was always
  loaded.
- **`get_nearby_buildings` from a turret is still vision-limited** (gunner r²=13). As a *sensor*
  a sentinel (r²=32) is nearly twice a builder's r²=20 and much better sited, but a gunner is
  worse than the builder we would have sent.

## BUILDER HOOK

Smallest test: place **one** sentinel at the furthest forward seat that our own measured turret
survival still supports, and treat it as an instrument rather than a weapon — log, per round,
(a) how many enemy buildings it can see, and (b) how many enemy ore tiles fall inside
`get_attackable_tiles()`. That is a two-number report that decides whether the "sensor and tax"
framing has any content on our map pool, before anyone spends a plank on acting on it.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2019-smite.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
