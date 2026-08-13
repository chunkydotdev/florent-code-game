# OPPONENT PROFILE — team lazy (10 games, 2026-08-13, HP-verified attribution)

**Provenance:** opus subagent spawned by builder s36 (Magnus's ask), replays
`1ef56244-*` (M1: their v212 seat A vs our v123, we won 3-2, ~08:54Z) and
`b9f3fab5-*` (M2: their v212 seat B vs our v125, we won 3-2, ~10:24Z). Their
v213 first pairs 10:52:59Z — **both matches are the identical opponent build**,
so every cross-match difference is map draw + our bot. The autopsy self-check
reconciles attributed core damage against UpdateHp deltas **20/20 core-sides,
0 mismatches**. Scripts preserved in `lazy-profile-scripts-2026-08-13/`
(built on tools/replay_census.py primitives; replays in local replay_archive/).

## The profile in eight facts
1. **Opening: deterministic in TILE, jittery in ORDER.** First harvester on one
   of the 3 nearest ore tiles to their core 9/10; the controlled pair (same
   14x18 map, opposite cores, M1g4/M2g2) matches 10/16 first builds under
   reflection while rounds jitter (r3 vs r8). Pre-emptable by tile, not round.
   Zero splitters (0/292 relay builds), zero launchers, in 10/10 games.
2. **The kill is ONE mechanism: a point-blank sentinel.** 12/12 turret tiles
   that ever shot our core sit at d²≤5 from our core NW; 11/12 sentinels.
   Their builder reaches d²≤8 then builds 1-6 rounds later (5/7). **The kill is
   SLOW — fastest r157** (vs our r115-r532), because:
3. **The core-tank is their real defence.** 92.3% of all their heals (803/870)
   target their own core, up to 9 simultaneous healer bots; they out-healed 93%
   of incoming in M2g4 (survived) vs ≤66% in every game their core died.
4. **They repair nothing but the core.** 56 harvesters built, 0 lost; cut belt
   tiles restored 14/36 (39%), 61% never. They replace belts, never repair.
5. **Defence is purely reactive and gunner-only.** Zero home defence before our
   first intrusion (10/10). Reaction to our forward turret: first SHOT median
   +2 rounds; first defensive BUILD median +9. **30/31 of our forward-turret
   deaths involve gunner fire, 0 sentinel**; counter-gunner at d²=1 in 31/52
   pairs; our forward turret's median life: 10 rounds. They rebuild their siege
   sentinel on the IDENTICAL tile (M2g4: (2,1)/(3,1) ×5).
6. **NOT broken on 900s** (n=3): harvesters r4/r4/r12, builders cross the map,
   siege lands r43-74. What degrades is turret timing (first turret r43-63 vs
   r9-40 small). We won 2/3 there with our two fastest kills (r115, r189). The
   "farm them on 900s" lead survives; the "pre-fix-broken" version is refuted.
7. **CPU:** they run cool (max 6,701µs of 10,000). **Self-audit: OUR execmax
   hit 8,757µs on 30x30s — WE sit closer to the TLE ceiling than they do.**
8. **Crash-surface lead:** 6 no-damage unit removals in the corpus, ALL their
   builders, ALL in the one game we planted barriers inside their base
   (5 of 6 at r81-111, tiles at d²=1-5 from their core; one bot spawned r98,
   vanished r99 having never moved). Crash vs self_destruct undecidable on the
   wire; a two-arm unrated leg would settle it. Approved class if real.

## Exploitable habits (ranked, with plank shapes)
1. **Deny the ~8-tile siege ring** around our own core with 3 Ti barriers by
   ~r40 — they rebuild on identical tiles and never heal turrets; their only
   counter is 2 dmg/2 Ti builder attacks vs 30 HP + our 4 HP/1 Ti heal.
   ⚠ DEFENSIVE plank: carries DEFENCE_ADMISSION_BAR (kill-round non-regression).
2. **Sentinel range asymmetry:** our sentinel r²=32 ignores obstacles; their
   counter-gunner r²=13 doesn't and gets built NEXT DOOR reactively. Site
   forward sentinels at d²14-32, or barrier the adjacent tiles — force the
   +3..+29-round new-build latency. Metric: forward-sentinel median life
   (currently 10 rounds) and shots-landed-per-sentinel.
3. **Beat the core-tank with VOLUME, not sequence:** in M2g4 we built 21
   sequential forward sentinels and NEVER had two firing simultaneously —
   12 HP/round beats two healers (8 HP/round + our other damage), 6 does not.
   Also: their healers park on the core 8-ring for consecutive rounds — a
   launcher throw (0 ammo, no team check) evicts one free. ⛔ Do NOT spend a
   leg cutting their belt: pays only via titanium_collected, off-currency.
4. **(Lead)** the barrier-in-base/vanishing-builders correlation above.

**Churn caveat:** they ship multiple versions/day (v197→v213 in 48h). Habits
here are structural (tile determinism, core-tank, gunner-only CB) and likelier
to survive churn than any constant; re-profile after their next big rating move.
