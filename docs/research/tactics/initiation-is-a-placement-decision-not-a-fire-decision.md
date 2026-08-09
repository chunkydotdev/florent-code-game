---
tactic: The field does not gate FIRING at all — the entire engagement decision is expressed as movement (for us, placement)
source: https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf
origin: Battlecode 2025 The Kragle, describing XSquare's micro — the open-sourced combat code most top teams copied
evidence: documented
transfers: partial
---

## WHAT IT IS

The sweep question was *"what governed the decision to initiate the first engagement?"*.
The most-copied combat code in Battlecode answers it by **not having a firing gate at
all**. The Kragle, explaining why nearly every top team adopted XSquare's micro:

> *"The conditions to initiate micro are usually whether your robot can see enemy robots."*

> *"decision making for who and when to attack is usually straightforward (target the lowest
> hp enemy possible, attack whenever possible)"*

**Referent check.** "micro" is defined two paragraphs earlier as *"fine-controlling singular
robots, mostly to optimize robot-to-robot combat"*; the sentence before the second quote
reads *"Note that this micro only involves movement and not the actual attacking."* So the
claim is explicit: the whole apparatus is a **movement** decision, evaluated over the 9
options (8 neighbours plus stay), scored by a heuristic:

> *"The heuristic information stores all factors that make a tile appealing/dangerous to
> move to (ie: number of nearby enemies, distance to closest enemy, etc)."*

and the one commit-side term in that heuristic is a local force ratio:

> *"pushing an engagement when a robot senses it has many allies"*

## WHY IT MIGHT TRANSFER

It reframes our own measurement. `US_shot_w50` — the best runtime-readable discriminator we
have (AUC 0.64-0.68, Holm p 1.5e-07) — is downstream of **where our turrets already are**,
not of a decision to pull a trigger. Our turrets are immovable and `can_fire`/`fire` is free
of any strategic content: with ammo and a target in the pattern, firing is always correct.

So in our ruleset the field's "movement" variable maps onto exactly one thing: **the tile a
builder chooses to build a turret on.** That is our engagement-initiation decision, and it
is made once per turret, permanently, at build time. This has a sharp consequence for the
programme:

- **You cannot retreat a decision to engage.** Sweep 14's failure catalogue lists
  *"retreat-and-return-under-the-counter-unit"* as a live tactic elsewhere; here the
  committed unit is a building. The heuristic must therefore be evaluated *before* the
  build, and it must be conservative in a way theirs need not be.
- **Our engine exposes the hypothetical form as a first-class predicate.**
  `can_fire_from(position, direction, turret_type, target)` and
  `get_attackable_tiles_from(position, direction, turret_type)` let a builder score a
  candidate seat exactly as XSquare's `MicroInfo` scores a candidate tile — *without
  building anything*. That is the mechanism, already present in the API.
- **The "many allies" term has a documented analogue on our side.** Sweep 10 measured the
  field's turret-adjacent worker cell (32.3%, lift 5.04) and `worker-fortified-turret-cell`
  explains why it closes harder here — builder attacks cannot touch builder bots. A forward
  turret with builders on its orthogonal tiles *is* our "many allies" term.

`transfers: partial` and not `yes`, because the half of XSquare's design that does the work
— reversible per-round repositioning under a threat field — has **no analogue for an
immovable turret**. What transfers is the *shape*: score seats with a runtime field, do not
gate the shot. `runtime-density-siting.md` and `turret-threat-field.md` (sweep 9) are the
same idea arriving from the siting side; this file is the statement that the field considers
the *firing* side settled.

## WHAT WOULD KILL IT

- **Our shots cost a scarce, convertible currency.** Gunners spend 4 ammo, sentinels 10,
  from a pool with **no passive income** that competes 1:1 with build titanium. "Attack
  whenever possible" is not free here the way it was for them, and our library already
  records that we *under*-convert relative to the field. A blanket fire-always rule is a
  spending decision disguised as a tactical one.
- **Their movement decision is per-round and reversible; ours is a permanent 20-30 Ti
  commitment inside the enemy kill zone.** The analogy is structural, not mechanical, and
  should not be pushed into "score tiles the way XSquare does" without the retreat term
  being replaced by something.
- It says nothing about **when to make first contact strategically** — it is an argument
  that the tactical layer is not where that decision lives. Taken alone it is a negative
  result for (A).

## BUILDER HOOK

None new. The existing hook is `_bfs_direction`'s `blocked` set at `_v100hf/main.py:4525`,
which sweep 9 already identified as half of BC2020's winning mechanism (turret tiles are
blocked, but with **no range or line-of-fire term**). The transferable step is to build the
seat-scoring side from `can_fire_from` / `get_attackable_tiles_from` rather than from a
fitted table — and to leave `fire()` ungated except by ammo policy.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
