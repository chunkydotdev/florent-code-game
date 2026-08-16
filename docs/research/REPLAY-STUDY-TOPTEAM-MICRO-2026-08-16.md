# REPLAY STUDY: top-team micro-mechanics — 52 decoded losses (2026-08-16, builder s47)

PROVENANCE: opus subagent commissioned by the builder on Magnus's watch-the-
games directive (study 3 of 3; siblings: REPLAY-STUDY-0033-2026-08-16.md,
midgard study pending). Sample: 52 rated LOSSES (cond=core_destroyed),
2026-08-13T11:53Z -> 2026-08-16T13:13Z, our v125-v152, opponents HTTP 418 (8),
lingling_40h (8), kladde (8), gsxWins (7), Erebus (6), diverge (6),
LingLing40 (5), Leviathan (4). Decoding via replay_census primitives; every
resolver was driven to the OTHER verdict on the same code path before its
numbers were trusted. Agent report verbatim below.

## Piece 1 — BUILDER-ATTACK TARGET: OURS IS A SINGLETON
US: 2,422 of 2,422 builder attacks (100.0%) on enemy CONVEYORS — zero
harvesters, turrets, barriers, core, across 52 games/7 opponents. OPP: 2,963
attacks — conveyor 45.8%, barrier 32.9%, harvester 11.3%, sentinel 6.3%,
gunner 2.7%, core 1.0%. They walk builders up and chew the TURRET killing
their core (gsxWins 44d603b5_g3 midgard: 40 attacks on our sentinel from
r134); kladde chews harvesters at the source (42e6b05a_g2: 97 attacks on one
harvester). Ti arithmetic: conveyor = pay ~20 Ti to erase 3 Ti; harvester =
30 HP/20 Ti and must be rebuilt ON ORE; gunner = what actually kills cores.
⇒ Piece: raider adjacent-scan target priority: turret-shooting-our-core >
harvester > core > conveyor. Six lines, no new state.

## Piece 2 — THE REPAIR RACE: THEY ANSWER A PECK, WE DON'T
Opponents heal the attacked building within 2 rounds for 72.3% of attacks
(1,653/2,286); we answer 26.3% — 12.9% dropping the Erebus-barrier artifact.
Per team: Leviathan 90.5, LingLing40 81.5, Erebus 76.5, gsxWins 67.0, kladde
59.9, lingling 58.0, HTTP418 51.6, diverge 0. Heal is +4 HP/1 Ti vs attack
2 dmg/2 Ti — an answering defender wins 4:1 in titanium, which makes our
conveyor-pecking free income for them.
⇒ Two halves: (a) never peck a tile a live enemy builder is orthogonally
adjacent to (pick unreachable target or kill the healer); (b) standing
heal-answer on our forward structures.

## Piece 3 — TURRET TILE BLACKLIST: WE REBUILD INTO PROVEN KILL-TILES
US: 110/251 turrets (43.8%) built on a tile where one of ours already died.
OPP: 26/402 (6.5%). Forward turrets (d²<=64): ours die 87.6% (163/186, mean
life 25r); theirs 29.3% (84/287, mean life 69r). Anchor: kladde 42e6b05a_g2
midgard — our sentinel rebuilt at (4,9) at r219/226/233/240, dead in 5-7
rounds each, ~280 Ti into one tile. ⚠ Worst on drumlin (83% reuse, mean life
5 rounds) and drakkarfjord (68%) — NOT the midgard/fjordgate/frostgate
cluster. NOT the excluded forward-placement question: the claim is only
about REUSE of a tile that has already killed one of ours.
⇒ Piece: comms-store dead-tile set consulted before any turret build. One
slot, one membership test. (Mirror-composes with #76's enemy-rebuild-farming:
same mechanism, opposite sign.)

## Piece 4 — SPAWN ON THE ENEMY-FACING SIDE OF THE CORE
Median 80% of opponent builder spawns land on the enemy-facing half of the
core ring; ours 30%. Free (pure candidate-tile ordering). Value scales with
core separation — midgard d²=1152 (~34 tiles), 2-3 wasted moves per builder.
⚠ Collides with reserved heal seats (eco.py heal_seats): the piece is "order
REMAINING candidates by d² to enemy core", never "abandon the seats".
Map flag: midgard/drakkarfjord/drumlin/valkyrie; low value on fjordgate.

## Piece 5 — JUST-IN-TIME AMMO (4-of-7 habit, NOT universal)
Median ammo balance: OPP 10 vs US 24; rounds holding >=30: 22.9% vs 39.0%.
kladde runs it at ~5-6 vs our 40-46. Counter-examples stated: gsxWins (58)
and Leviathan (100) bank HARDER than us. Mechanism: convert_ammo costs no
cooldown and works same-turn, so pre-banking has no upside — banked ammo is
titanium that cannot buy anything. ⇒ convert shots_wanted × cost each round
at the core; three lines.

## Piece 6 — THE PIT: fixed dump tile + re-throw-on-return
lingling_40h: 63 throws, 25 on a single victim, top destination reused 19x,
median re-throw gap 4 rounds (27/56 gaps <=3). Anchor 6f8fcf68_g3 fjordgate:
our builder thrown to (0,0) at r129/131/133/135/137 — every 2 rounds, the
launcher's exact cooldown; the victim never gets a productive turn again.
diverge: one destination for all 18 throws. New vs our exile plank: the
DESTINATION IS A GAME-CONSTANT and the standing order is "re-throw whoever
is adjacent" — one 20-Ti launcher = a permanent 0-ammo lock on one enemy
builder. Our launcher exists in 2 of 52 games (median first build r214!) vs
their 16 of 52 (median r25.5).

## Roads CHECKED AND CLOSED in this study — do not re-derive
Barriers as turret armour (kladde 4/34 adjacent — falsified). Gunner rotate()
as second-gunner substitute (we rotate MORE: 2.19x vs 1.55x/gunner). Core
body-blocking (0 absorbed shots in 52 games, anyone). Splitters (0 built in
104 team-games). Self-demolition to shed scale (0 events both sides,
this sample — note 0033 study measured 53 for 0033; team-specific).
Launcher as own-builder transport (0 by any opponent HERE — only we do it;
research's Jython 11.3% ferry lead is a different team, not contradicted).
Cost-scale discipline (they run HIGHER scale — not their edge). Terminus-vs-
midline belt cutting (no differential except kladde cutting at source).
Core-heal latency: ours 8-13 rounds from first damage to first heal vs their
1-4; 6 of the first 20 games took >=500 core damage with ZERO core heals.

## Agent's ranking (composability x build cost)
1 target-priority > 3 tile-blacklist > 2 repair-race > 4 spawn-bearing >
5 JIT-ammo > 6 pit. Pieces 1, 2b, 3 compose directly into raider/seal
doctrine, each a single predicate; 4 and 5 are ordering changes, no state.
