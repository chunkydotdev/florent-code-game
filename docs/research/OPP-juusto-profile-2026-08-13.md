# OPPONENT PROFILE — Juusto v7 (15 games, tri-arm leg 2026-08-13)

**Provenance:** unrated tri-arm leg fired ~14:40Z (`scratchpad/triarm_fires.tsv`).
Matches `c2e36a20` (ARM-A, our v125), `e0beff8d` (ARM-B, our v126),
`2cf0df8e` (ARM-C, our v127) — **their version pinned at v7 in all three**
(`corpus/meta_join.tsv`), 5 games each = **15 games**. We won **6/15**.
Map pool byte-identical across all 15 tri-arm matches (terrain SHA1 per game
index), so cross-arm/cross-opponent comparisons are map-controlled. Scripts:
`scratchpad/opp-profiles-2026-08-13/` (`prof.py`, `agg.py`, `deep.py`,
`checks.py`), built on `docs/research/lazy-profile-scripts-2026-08-13/`.
**LIMIT: 15 games, one pinned build, all against our v125–v127.**

## Facts (MEASURED unless marked)
1. **Opening is a metronome: first harvester r6 in 8 of 12 games** that build one
   at all (values 6,6,6,6,6,6,6,6,8,8,10,10), always at d²=10–20 from their own
   core. Builder spawns: 4–5 by r30 in 15/15, then almost none (4–10 total).
2. **They will not walk for ore.** On the far-ore 30x30 map `5ede4adb` (nearest
   ore d²=80–100) they build **0 harvesters in 3/3 games** and 5–62 conveyors
   that feed nothing. Coreflood harvests that map 3/3. *(Same blind spot as
   LingLing40 — see that profile.)*
3. **Sentinel stand-off, not a face-camp.** 42 sentinels vs 12 gunners, **0
   launchers**, 15 turret deaths, 0 self-removals. 44 turrets built at d²≤26 of
   our core, **median d²=16** (4 tiles), the clustered mode being 16–18. Their
   first turret is a FORWARD turret in **14/15 games** — median r22, and the
   round they first touch our core is median r44.
4. **Kill mechanism: one sentinel doing all the work.** Only **15 of their
   turrets ever shot our core footprint across 15 games — 14 sentinel, 1
   gunner, median d²=16** — and 5/15 games produced none at all, so ~1.5
   shooters per contested game (46, 86, 55, 23, 50, 28 shots from d²=16–18 are
   the single-tile totals). Our core died 7/15 at r76/113/126/167/188/193/199 (median
   r167); their core died 5/15 at r100/135/200/220/304; 3 games reached r1000.
5. **They also use builder attacks on our core**: 103/86/95/36/15 attacks in
   5/15 games (2 Ti → 2 dmg each), i.e. a bot parked on our footprint.
6. **Barriers are their defensive primitive** (39 across 15 games, 11/15 games);
   pre-built home defence before our first intrusion in only 3/15. Median
   reaction latency from our intrusion to their first home-defence build:
   **5 rounds** (n=9, range 1–123).
7. **Healing is turret-first, not core-first — the inverse of every other team
   profiled.** 1,147 of 1,534 builder heals (74.8%) land on their own turret
   tiles, 220 on the core, 165 on econ. **1,113 of those are ONE sentinel at
   `(5,6)` in `2cf0df8e`g5 healed for 1,000 rounds.** Excluding that game:
   34/412 turret, 220/412 core — so the mode is *core*-heal and the turret-heal
   number is one outlier game, not a habit. (Stated both ways deliberately.)
8. **⭐ AMMO HOARDING, and it is enormous.** `2cf0df8e`g1: they collected
   12,110 Ti, converted ~12,139 into ammo across 721 conversions, fired **48
   shots (480 ammo)** and finished with **11,939 ammo unspent** — cross-checked
   against `corpus/econ.tsv` (`ammo_end=11939`, `ti_collected_end=12110`,
   `ti_end=330`), two independent decoders agreeing. Milder but same sign in
   `e0beff8d`g1 (520 unspent) and `c2e36a20`g1/g5 (289/238). INFERENCE: their
   convert rule is balance-triggered with no cap, so a long game converts the
   whole economy into an unusable reserve.
9. **CPU: the coolest team of the three. cpu_max 1,385–2,444µs of 10,000; tled
   0 in 15/15.** No CPU road here. (Our own max in the same games: 8,831µs.)
10. **Zero counter-play against our forward turrets by builder attack in 22 of
    23 cases.** They answer with turret fire only: median rounds from our
    forward turret's build to their first shot at it **6.8** (n=8); our forward
    turret's median life against them **17 rounds** (n=9) — the longest of the
    three profiled opponents. That number is JOINT (our siting, their answer).

## Exploitable habits (ranked)
1. **Out-range or blind the d²=16 stand-off sentinel.** Their siege sits at 4
   tiles; sentinel line shots ignore obstacles, so barriers do not block it —
   but the tile is *predictable* and 40 HP. A pre-placed counter-sentinel
   covering that ring, or a launcher throw on the builder that seats it, is the
   shape. Replacement latency after a siege turret dies: 1,1,2,2,6,7,37,50,58.
2. **Deny the far-ore map by denying nothing at all** — on `5ede4adb` they have
   no income line for 1,000 rounds. INFERENCE: any plank that lengthens a game
   on that map class is nearly free against them; conversely they cannot be
   starved there because they are already starving.
3. **The ammo hoard is a titanium sink we should not interrupt.** 12,110 Ti
   collected, ~480 spent as ammo. INFERENCE: pressuring their *income* is
   pointless; pressuring their *builder count* (4–5, then flat) is not.
4. **They never counter-attack a forward turret with builders (1/23).** Our
   forward sentinel lives 17 rounds median here vs 5–14 elsewhere — siting a
   second simultaneous forward sentinel is cheaper against Juusto than against
   any other profiled team.
5. **⛔ No CPU road, no crash lead:** 0 tled and **0 no-damage unit removals in
   15/15**. Positive control: the same detector in the same run found 6
   no-damage removals for Coreflood, and LP's splitter/launcher/harvester-death
   detectors all fire non-zero elsewhere in this corpus. The zeros are real.
