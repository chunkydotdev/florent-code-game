# BUILD REPORT — `bots/_v510ferrysiege` (self-ferry siege raider), s50 2026-08-17

*Banked by the builder s50 from the opus build agent's final report. Magnus's one plank for the
day. Chassis `_v488beltbreak2` (holder v159) + one new module (`siege.py`, 1,333 lines,
`SiegeMixin`) + five hook sites. Master flag `LOKI_FERRY_SIEGE_ON` @ doctrine.py:2152; flag OFF
writes not one bit of the new store layout. Demo replays: `demos/DEMO-midgard-ferrysiege.replay26`
(seed 21, most legible, loss r545) and `demos/DEMO-midgard-ferrysiege-WIN.replay26` (seed 22,
win r409). Spec inputs: PROBE-DOSSIER-ferry-siege + both Jython studies + eviction-geometry +
field-siege-response + Juusto (all docs/research/, same day).*

## Subsystem anchors (siege.py unless noted)
store codec/heartbeat :92-136 · map gate `_fs_gate` :144 / `_fs_active` :181 · geometry+backside
target :191-250 (`_fs_ring12`, `_fs_wall`, `_fs_target`, `_fs_park_seat`) · ring census +
diagonal deferral :286-380 · raider state machine `_fs_turn` :391 / degrade :460 · ferry
:474-551 (`_fs_build_ferry`, `_fs_hop_step`) · ring turn/seal :582-791 (`_fs_seal_ok`,
`_fs_try_seal`, `_fs_stand_target`) · eviction :840-947,:1239 (`_fs_observe_healers`,
`_fs_try_evict_launcher`) · sentinel :963-1016 (`_fs_sentinel_ok`, `_fs_gun_axis`,
`_fs_try_sentinel`) · launcher turn :1095-1156 (`self_destruct()` at :1086/:1091 — last
statement) · indicators :1319,:1327.
Hooks: main.py:41,62 (mixin) · :174-197 state · :442-448 FS magazine (after T4 burn cap) ·
:469-486 siege ti_floor · :521-542 3-builder opening + raider replacement (min() only — can
never raise the incumbent spawn curve) · :551-554 collar reserve on spawn gate · :751-766 role
dispatch · raid.py:139-145,:174,:191,:1235 (launcher hook ABOVE the `self.core is None` early
return — load-bearing, surprise 1) · eco.py:377-386 collar reserve · doctrine.py:2085-2377.

**Store: no free slot exists (probed: index 16 out of range). `SLOT_FS = SLOT_RAID_LIVE` (15)
shared via bitfield** (bits 0-10 beat, 11-13 phase, 14-29 raider id+1); chassis's reader/writers
adapted mask-preserving.

## Extended vs added
Extended: forward-sentinel path (SLOT_FWD_GUN funds it), chassis nav/BFS (already treats
BARRIER blocked — solved the probe's 995-round self-walling), `_eco_spendable`, spawn gate,
`_launcher_turn`, exile/stale-position guard, heal_seats/core_corners helpers. Added new:
raider state machine (replaces `_raid` for THE ONE FS raider only — different discipline over
the same tiles as the chassis's opportunistic ungated collar), disposable launcher chain,
backside targeting, eviction launchers, diagonal deferral (no launcher capability existed to
inherit — LAUNCHER_MIN_RND=160).

## Verification
**V1 midgard demo vs incumbent:** 3-builder opening ✓ · arrival r13 (seed 21) at 2-round hop
cadence ✓ · launcher self-destructs ✓ · eviction launcher at cov 9, **119 throws** ✓ · collar
7/8 orthogonals ✓ · 4 aligned sentinels ✓. ⛔ **Orthogonal-8 never closed; no game ended by
sentinel-on-sealed-core. Seed 21 = loss r545.**
**V2 gates:** fjordgate (dim branch) and antler (core-dsq branch) both play PURE incumbent (0 FS
lines/hops/launchers); both branches driven both ways; 11/13 maps pass.
**V3 flag-OFF:** 8 maps, every reported quantity identical to inc-vs-inc (label-only diff);
full det-equivalence deferred to prereg.
**V4 both-ways per guard:** team filter 0 own-throws vs mutant 16/19 own (84% — Jython §4.1
reproduced) · never-ferry gate 0 ring-sited ferry throws vs mutant 3 (own sealer flung) ·
binary-seal wait first-barrier r8 @ 218 Ti banked vs mutant r54 @ 19 Ti · self-destruct scale
174% / sentinel 52 Ti vs persist-mutant 229-252% / 68-75 Ti (+44%) · bounds guard: mutant
raises GameError on atoll AND midgard (is_in_vision-as-bounds); static audit: all 15 risky call
sites behind explicit bounds/wall-filter/try (usually two of three).
**V5 numbers (1 game/map, seed 7):** arrival heart/nordkap r5 · atoll/drumlin/royale/yulerune
r7 · saga r9 · glacierkeep/ragnarok r11 · **jackpot r12 (dossier said never)** · midgard r15.
Ferry exactly 2.00 rounds/hop on 10/11 maps (midgard 2.20, jackpot 3.00). Collar best 7/8
(glacierkeep, nordkap); **0/13 games closed the 8**. Evictions 0-126/game. Sentinels 1-2 live,
up to 12 built (replacement churn ≈ field's 8-round median life). Ammo 83-296. CPU max 334 µs
builder / 191 core / 55 sentinel (~30× headroom; process_time local — get_cpu_time_elapsed is
a stub under fcode run). Our econ materially down vs incumbent (midgard 530 vs 920 mined) —
the plank buys 3-9 launchers + 280-300 ammo at chassis scale 1.7-2.5.

## Deviations from spec (agent's, with reasons — all ratified by the builder)
1. Sentinel siting = MAX standoff + gunner-axis penalty (delta-3 supersedes "prefer close";
   Jython's d²=9 median is a survivorship cut). 2. Sentinel does NOT wait for a complete seal
   (orth==0 gate vs a pecking defender = never bought = r1000 stall; now: bank covers turret +
   all owed barriers, or jump-queue at FS_SENTINEL_RND=30). 3. Seal-first sentinel-second within
   a round. 4. Second eviction launcher default-on (delta-1). 5. Replacement: 2 core-spawn cap
   but UNCAPPED role-conversion of existing builders on stale heartbeat. 6. FS_CLEAR_RING_ON
   ignores LOKI_QUIET_ON for the single case of an enemy BUILDING on a needed ring tile
   (surplus-gated). 7. Store slot shared (none free). 8. Diagonals deferred to kill window, NW
   excepted.

## Surprises (verbatim in substance)
1. **A launcher cannot see our own core** past the second ferry link (r²=26) and the incumbent's
   launcher path early-returns on `self.core is None` — ferry died r4 until the hook moved above
   it; anchors now from `enemy_core_for`'s involution.
2. **Two independently-computed reserves over one bank deadlock** (core's siege reserve vs
   raider's seal gate — each generous, together a lock; a full match passed with zero barriers).
3. An unconditional repair step froze a raider 60 rounds (heal consumed action, action blocked
   move; five never-visited ring tiles stayed open).
4. "Already in place" is a trap when the seat is squatted (adjacent raider answered stand-target
   with "here"; can_build refused every round; died there).
5. The no-route watchdog killed a siege at 7/8 sealed (walking a closed curve's outside crosses
   FS_RING_DSQ; 30 such rounds read as "no route").
6. **is_in_vision-as-bounds also fails on MIDGARD** (cores at (2,2)/(26,26) near borders) — the
   exposed set is wider than the dossier recorded.
7. **jackpot is reachable** (r12) — corrects the dossier's "never".
8. **The plank loses to our own incumbent on midgard** — mechanisms all fire; the orthogonal-8
   never closes, heal denial (the engine of the plank) never engages, their counter-attack
   decides (our core r137-r545). Seed-1 long dumps landed ~4 tiles = the short-dump regime
   (58.7% return) — ≥6-tile sites were terrain-unavailable at those placements.

## Fixture caveat for the prereg (agent's, adopted)
The local fixture is our own strongly-defensive holder — the class of fixture the dossier
explicitly prices as lying for collar planks (five prior collar planks failed locally on
fixture admission; Jython's 0.650 share is vs the LADDER). Binding constraint measured locally
= BANK at chassis scale 1.7-2.5, not mechanism. Eviction geometry observational vs un-thrown
defenders; the partially-sealed sub-case — the state 13/13 local games sat in — is unmeasured.
