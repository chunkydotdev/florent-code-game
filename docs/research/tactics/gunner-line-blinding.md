---
tactic: Blind the planted gunner instead of killing it — a 3 Ti barrier in its firing lane
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf (the blocking meta it belongs to); engine probe in ../turret-line-blocking-2026-08-09.md
origin: Battlecode 2020 blocking/obstacle doctrine; the specific application is inference by tactics sweep 9 (this agent)
evidence: inference — by tactics sweep 9, resting on a documented engine probe and a documented analogue
transfers: partial
---

WHAT IT IS — **an enemy turret planted in your base is a geometry problem before
it is a damage problem.** A gunner is a facing turret whose straight-line shot is
blocked by buildings (measured, s23 — the GUNNER was the *positive control* of
that probe and `can_fire_from` flipped **True → False** with a barrier in the
line, while the sentinel under test passed straight through). So the cheapest
answer to a planted gunner is not
damage — it is **an object in the lane**. The cheapest legal object in this game
is a **barrier: 3 Ti, 30 HP, +1% scale**, the smallest scaling increment there is.

**Denial by occupancy is a first-class, officially-documented mechanic in
Screeps**, which is the nearest thing to a source for the general form. On
ramparts, docs.screeps.com/defense.html:

> "They behave like walls for hostile creeps by blocking their movements, while
> your creeps can freely pass through them."

and the community wiki's honest caveat, which applies here too:

> "Often its best to think of walls and ramparts as a delay to allow you to
> create a defensive force of creeps, than as impenetrable defenses."

*(wiki.screepspl.us/index.php/Combat — community wiki.)* A barrier in a gunner's
lane is a delay bought at 3 Ti, not a wall.

The doctrinal ancestor is Battlecode 2020's whole obstacle meta, where the
winner routed around Net Guns by treating covered cells as impassable
([[turret-threat-field]]) and where structures were routinely used to deny
movement rather than to fight. **The specific "put a wall in front of the turret
so it cannot shoot" application is my inference, not a quoted tactic — do not
attribute it to any team.**

WHY IT MIGHT TRANSFER — the exchange rates are lopsided in a way nothing else in
this library is. A 3 Ti barrier in the lane forces the opponent to pick one of
three answers, **all of them losing**:

| their answer | what it costs them | exchange vs our 3 Ti |
|---|---|---:|
| `rotate()` the gunner to a new facing | **10 Ti + 1 action cooldown**, gunner-only | **3.3 : 1** in our favour, and repeatable — each new facing takes a new barrier |
| builder-attack the barrier (2 dmg / 2 Ti = **1.00 HP/Ti**) | 30 Ti and **15 builder-turns** unhealed; against our 4.00 HP/Ti heal it is a **4 : 1** attrition loss | **10 : 1** |
| shoot it with their own gunner (7 dmg / 4 ammo = 1.75 HP/Ti) | 30 HP needs **5 shots = 20 Ti of ammo**, from a pool with no passive income | **6.7 : 1** |

and crucially **`destroy()` is allied-only** (verified in the engine type stubs,
per [[spawn-smothering]]), so there is no cheap removal route at all.

It also answers the *measured* failure rather than a hypothetical one:

- The killer is short-range and gunner-shaped: **83.8% of our home turret deaths**,
  and the three worst opponents do it "with gunners, essentially never with
  sentinels".
- **It needs no tile table.** `gunner-plant-tiles-are-not-enumerable-2026-08-09.md`
  refutes the pre-placed ≥5-kill table (+3.8pp held-out at best, **−3.0pp** at
  shippable sizes). Blinding is *reactive*: it keys on a turret already standing,
  whose position and facing are both directly readable.
- It attacks the **41.4% survive-to-end tail** without paying the removal race
  that [[sustained-plant-removal-race]] prices as unwinnable when the plant is
  escorted. A blinded gunner does not need to die; it needs to stop shooting.

WHAT WOULD KILL IT — five things, and the first two are the real risk:

1. **A legal empty tile may not exist in the lane.** Build requires an
   orthogonally adjacent, *empty* tile, and 97.2% of tiles the enemy plants on
   are tiles we also build on — the lane is likely to be our own conveyor run.
   We cannot build over our own conveyor, and destroying it to make room hands
   them the tile.
2. **Our builder has to survive the placement.** It must stand orthogonally
   adjacent to the target tile, which may itself be inside d²≤13 of the gunner.
   The place to stand is *off* the lane and *beside* it.
3. **Sentinels are immune** — probed: 18 damage landed straight through our own
   builder bot *and* our own barrier. This tactic is worth exactly the gunner
   share of the problem, and worth nothing against the 7.7% sentinel-outrange
   share. It would also stop working entirely against an opponent who switched
   turret type, which two of the field (Banminary 93.8%, Memtrace 70.6% sentinel
   share) already have.
4. **The probe tested the wrong ownership pair.** It showed a **friendly** barrier
   blocking a **friendly** gunner. What this tactic needs is **our** barrier
   blocking **their** gunner. Same rule by symmetry, almost certainly — but it is
   an assumption, and it is the cheapest thing on this page to check.
5. **Friendly fire is real and lanes are shared.** The attribution doc has a
   verified case of a team-0 gunner killing its own builder on the target tile.
   We are the gunner-heavy side too (41,921 gunner builds vs 13,298 sentinel), so
   every barrier we plant to blind theirs also blanks one of our own lanes.

BUILDER HOOK — **one rule, no map, no table, no store slot:**

> If a builder can see an enemy **gunner** (it can: vision 20 > their reach 13)
> and some tile orthogonally adjacent to the builder is empty **and** lies in
> `get_attackable_tiles_from(gunner_pos, gunner_dir, GUNNER)`, build a barrier
> there.

**Prerequisite probe, one local game, before anything is built:** place a
barrier belonging to the *other* team in a gunner's line and confirm
`can_fire_from` goes True → False from that side. That is the mirror of the s23
probe and it is the single assumption the whole file rests on.

Second, cheaper measurement worth taking at the same time: how often does a
planted enemy gunner's facing line actually contain a tile we could legally
build on? If the answer is "rarely, because it is our own conveyor", kill
condition 1 fires and this file is dead — and that is a two-hour corpus query,
not a battery.

Related: [[turret-threat-field]] · [[sustained-plant-removal-race]] ·
[[retake-the-vacated-tile]] · [[spawn-smothering]] ·
[turret line blocking probe](../turret-line-blocking-2026-08-09.md)
