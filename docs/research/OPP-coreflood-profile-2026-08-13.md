# OPPONENT PROFILE — Coreflood v83 (15 games, tri-arm leg 2026-08-13)

**Provenance:** unrated tri-arm leg fired ~14:40Z (`scratchpad/triarm_fires.tsv`).
Matches `a33654a2` (ARM-A, our v125), `16f73264` (ARM-B, our v126),
`1a5e31e9` (ARM-C, our v127) — **their version pinned at v83 in all three**
(`corpus/meta_join.tsv`), 5 games each = **15 games**. We won **9/15**.
Map pool is byte-identical across all 15 tri-arm matches (terrain SHA1 per game
index: g1/g2 30x30 `60e11efa`/`5ede4adb`, g3 25x25 `99d1b5f3`, g4 20x20
`12f9036e`, g5 10x10 `5ff3ef96`), so cross-arm and cross-opponent comparisons
are map-controlled. Scripts: `scratchpad/opp-profiles-2026-08-13/`
(`prof.py`, `agg.py`, `deep.py`, `checks.py`), built on
`docs/research/lazy-profile-scripts-2026-08-13/lazy_profile.py` primitives.
**LIMIT: 15 games, one pinned build, all against our v125–v127. Nothing here
generalises to "Coreflood always".**

## Facts (MEASURED unless marked)
1. **Strongest economy of the three profiled.** First harvester median r5
   (range r3–r10, 15/15 games), **99 harvesters over 15 games, 0 destroyed**
   — but *we* never attacked one (our detector counted 30 of OUR OWN harvester
   deaths in the same 15 games, so the zero is real and is OUR behaviour, not
   their defence). 1,175 conveyors, **0 splitters in 15/15**, 4 barriers total.
   ti_collected reaches 19,060 (`1a5e31e9`g2).
2. **They are the only one of the three that harvests the far-ore map.** On g2
   (`5ede4adb`, nearest ore d²=80–100 from core) they build 5–11 harvesters at
   d²=80–530, 3/3 games; Juusto and LingLing40 build **zero** there, 3/3 each.
3. **Kill mechanism = a siege turret parked in our core's face.** 53 turrets
   built at d²≤26 of OUR core across 15 games, **median d²=10** (27 of 53 at
   d²≤10, none at d²≤2). **29 of their turrets ever shot our core footprint —
   15 gunner, 14 sentinel, median d²=13**; the top shooter in a game lands
   56–134 shots from d²=5–17. Our core died 5/15 at
   r135/175/271/306/557.
4. **They rebuild the siege on the IDENTICAL tile.** `16f73264`g1: five gunners
   then three sentinels all at `(27,23)`, d²=10 from our core, r74→r134;
   replacement latency after a siege turret dies: **1,1,1,1,2,11,17,17,93**
   (median 2 rounds).
5. **Defence is reactive, not pre-built.** Home defence (turret/barrier at
   d²≤60 of own core) exists before our first intrusion in only **5/15 games**.
   Median latency from our first intrusion to their first home-defence build:
   **0 rounds** (n=12, range 0–20) — i.e. they usually already have something
   near home when we arrive, and otherwise respond same-round.
6. **Core-tank healing.** 1,783 of 1,985 builder heals (89.8%) land on their own
   core footprint; 174 on econ tiles, 19 on turret tiles. **Cut belt is not
   repaired: 7 same-tile conveyor rebuilds out of 59 cuts.**
7. **⭐ THEY TIME OUT, AND ONLY ON 30x30.** tled turns per game: 5/15 games
   non-zero (37, 4, 97, 216, 28) — **all five are 30x30**; 0/9 on ≤25x25.
   cpu_max exceeds the 10,000µs budget in 6/15 games (max **11,459µs**). We had
   **0 tled in 15/15** with our max at 8,816µs (`checks.py` output).
8. **Turret facing is corrected by demolition, not `rotate()`.** 6 no-damage
   removals: gunner born r58 removed r59, sentinels born r190/r212 removed
   r193/r213, plus a barrier and 4 long-lived builder bots
   (born r2/r3/r3/r101, removed r202/r279/r355/r934). **Team ammo was 4–50 at
   every one of those rounds**, so the 0-ammo `can_fire` self-kill is ruled out
   as the mechanism. Crash vs `self_destruct` is undecidable on the wire.
9. **Only one of the three that builds launchers** (7 across 15 games, first
   at r190). Turret mix overall: 57 gunner / 54 sentinel / 7 launcher; 45 turret
   deaths, only 3 no-damage — **turrets are not disposable-by-design here**,
   median turret life 5.5 rounds because we shoot them.
10. **Counter-play against our forward turrets is weak but real:** their builders
    attacked 6 of our 28 forward turrets (when they commit, they finish: 15–20
    attacks = a kill). Median rounds from our forward turret being built to
    their first shot at it: **12** (n=9).

## Exploitable habits (ranked)
1. **Deny the d²≤10 ring around our own core.** 53 siege turrets, median d²=10,
   and they re-seat on the same tile within 1–2 rounds. 3 Ti barriers on that
   ring by ~r40 are the cheapest counter. ⚠ DEFENSIVE plank —
   `DEFENCE_ADMISSION_BAR` (kill-round non-regression) applies.
2. **CPU-pressure road, live evidence.** They already burn 11.4ms on 30x30 and
   lose 216 turns in one game. INFERENCE: adding units/entities on 30x30 pushes
   them further over the budget and truncated turns cost them actions. This is
   the CPU-denial road with a measured opponent at the ceiling.
3. **Belt cutting is *relatively* effective here (7/59 restored) but pays only
   via `titanium_collected` — OFF-CURRENCY.** Do not spend a leg on it.
4. **Volume, not sequence, against the 89.8% core-tank** — same arithmetic as
   team lazy and Leviathan; two simultaneous forward sentinels or none.
5. **(Lead)** 4 long-lived builder bots vanishing with no damage; ammo ruled out.
