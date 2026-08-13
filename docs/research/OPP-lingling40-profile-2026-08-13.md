# OPPONENT PROFILE — LingLing40 v40 (15 games, tri-arm leg 2026-08-13)

**Provenance:** unrated tri-arm leg fired ~14:40Z (`scratchpad/triarm_fires.tsv`).
Matches `446bb6a3` (ARM-A, our v125), `ee551d6f` (ARM-B, our v126),
`85408103` (ARM-C, our v127) — **their version pinned at v40 in all three**
(`corpus/meta_join.tsv`), 5 games each = **15 games**. We won **4/15 — the
worst of the five tri-arm cells.** Map pool byte-identical across all 15
tri-arm matches (terrain SHA1 per game index), so the comparison is
map-controlled. Scripts: `scratchpad/opp-profiles-2026-08-13/` (`prof.py`,
`agg.py`, `deep.py`, `checks.py`), on
`docs/research/lazy-profile-scripts-2026-08-13/` primitives.
**LIMIT: 15 games, one pinned build, all against our v125–v127.**

## Facts (MEASURED unless marked)
1. **They kill us, fast and repeatedly. Our core died in 11/15 games** at
   r85/92/93/100/115/141/169/237/250/524/858 (median **r141**); their core died
   in 3/15 (r253/358/420); 1 game reached r1000. **Our core takes its first
   damage at median r23** (range r5–r133) — earlier than either other profiled
   opponent (Coreflood median r46, Juusto r44).
2. **⭐ THE MECHANISM IS A CREEPING POINT-BLANK GUNNER LADDER.** 80 turrets
   built at d²≤26 of OUR core, **median d²=5**, with **45 of 80 at d²≤5 and 14
   at d²≤2**; **70 of their turrets ever shot our core footprint — 52 gunner,
   18 sentinel, median d²=5**. The pattern is a sentinel anchor at d²=18–25
   first, then gunners
   walking in tile by tile: `446bb6a3`g3 `(7,7)→(7,4)→(6,4)→(5,4)→(4,4)→(4,5)`
   over r128–r146; `85408103`g1 `(3,4)→(2,4)→(1,4)→(1,3)→(1,2)→(1,1)` over
   r89–r112. Single-tile shot counts reach **386, 210, 163, 152, 126** — a
   7-dmg gunner firing every other round from the doorstep.
3. **Replacement is near-instant.** Latency from a siege turret's death to the
   next siege turret build: `446bb6a3`g1 `[1,1,1,1,1,2,2,5,9,10,12,38,69]`,
   g3 `[1,2,3,6,11,13,16,17,18,18,22,25,25]`. Killing one gunner buys 1–2 rounds.
4. **Gunner-heavy mix, and turrets are consumable in practice, not by design:**
   60 gunners / 24 sentinels / **0 launchers**; 47 turret deaths, **0 no-damage
   self-removals** (median turret life 8 rounds — we kill them).
5. **Opening:** first harvester median r7.5 (r3–r11) in 12/15 games, 3–4
   harvesters per game, 44 built and 0 destroyed by us. **4 builder bots by r30
   in 15/15 games — the flattest builder curve of the three.** 0 splitters,
   52 barriers.
6. **They will not walk for ore either.** On the far-ore 30x30 `5ede4adb`
   (nearest ore d²=80–100): **0 harvesters and 0 conveyors in 3/3 games.** They
   still killed our core on it once (r858) and drew one r1000. Coreflood
   harvests that map 3/3.
7. **Home defence is essentially absent: pre-built defence within d²≤60 of their
   own core before our first intrusion in 1/15 games**, and only 4/15 games
   produced any defensive build after our intrusion at all (latencies
   0, 1, 2, 406). **INFERENCE: their titanium goes forward, unconditionally.**
8. **Healing is core-tank when it happens:** 1,852 of 2,547 builder heals
   (72.7%) on their own core, 442 econ, 261 turret; but heal volume is bimodal —
   4/15 games under 10 heals, 3/15 over 240. **Belt repair is real but rare:
   15 same-tile conveyor rebuilds of 25 cuts, 15 of which are one game
   (`ee551d6f`g5, 16 cuts / 15 rebuilds).**
9. **CPU: spiky, not broken.** cpu_max 590–10,513µs; **2/15 games exceed the
   10,000µs budget** (10,513 and 10,506) and total tled is 3 turns across 15
   games. Not the Coreflood pattern (386 tled turns), not the Juusto flatline.
   Our own cpu_max in the same games: up to 8,831µs, 0 tled.
10. **We barely contested them.** We built only 11 forward turrets in 15 games
    (vs 28 vs Coreflood, 23 vs Juusto) because games ended early; **only 2 of
    those 11 were ever shot at.** Both numbers are JOINT and mostly describe
    OUR bot's short life on these maps, not their answer.

## Exploitable habits (ranked)
1. **The gunner ladder walks a fixed corridor into our core.** 39 of 80 siege
   turrets at d²≤5. A 3 Ti barrier ring at d²≤5–8 by ~r40 denies the build tile
   outright (walls block building), and gunner shots are obstacle-blocked
   (unlike sentinel). ⚠ DEFENSIVE plank — carries `DEFENCE_ADMISSION_BAR`.
2. **Their builders escort the ladder and are unguarded.** INFERENCE (from the
   1/15 pre-defence figure and the 1–2 round rebuild latency): the ladder is a
   single builder rebuilding in place. A launcher throw (0 ammo, no team check,
   pickup d²≤2) that evicts that bot resets the whole ladder — and it is the
   only mechanism in this profile that attacks the *cause* rather than the
   turret.
3. **Their home is empty.** 1/15 games with any pre-built home defence,
   median 0 harvester defence, 0 launchers. **INFERENCE: a race is winnable
   against them if we survive to r141 — the median round our core dies —
   which is exactly the r150–250 window `PLAY_DEFENCE` was amended for.**
4. **Do not spend a leg on their economy:** 3–4 harvesters, ti_collected
   500–5,030, and they win anyway. Their damage is not economy-financed at the
   margin (INFERENCE from ammo_end 0–13 in 15/15 games — they run ammo-starved
   and still out-shoot us).
5. **⛔ No crash lead: 0 no-damage unit removals in 15/15.** Positive control:
   the same detector in the same run found 6 for Coreflood; LP's
   splitter/launcher detectors fire non-zero elsewhere in the corpus. Real zero.
