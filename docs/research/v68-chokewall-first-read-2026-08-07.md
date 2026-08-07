# v68 "chokewall" first read (x3r0 upload, live 19:12)

**Status: COMPLETE ~20:25 — code half (agent A) + replay half (agent B,
tiebreak-led) + synthesis.** Commissioned by builder ASK post-v68
activation; priority raised after 6c stage-2 bar-not-met (46.0/480 vs this
bot, half the decided games tiebreak grinds). Replay corpus: ALL 7 v68-era
matches (teamXVersion==68 authoritative), 35 games — ladder 10-5 (+10.6
Elo → 1589.35 over 3 match wins), x3r0's unrated self-probe burst 3-17.
Parser cross-validated against tools/replay_census.py (exact agreement).

Version tags (rule 2): live = **v68 "chokewall"** (`bots/opp_v68/main.py`,
md5 04811b4a3f065f861e74ab626db559df — verified against the builder's
activation stamp; the 3502-vs-3684 line-count discrepancy the agent flagged
is a measurement artifact of my brief — `grep -c .` skips ~182 blank lines —
NOT an incomplete copy). Dirs code-read (agent A, read-only): opp_v68,
opp_v67, _v74e4/_v74e4b8/_v74e4b8v2, _v75e5, _v76e51, _v72e2, _v70mh,
_v77e6/_v78e6b/_v79e6c, opp_v49/50/56/58/63. All line refs = opp_v68/main.py
unless tagged.

## Headline

1. **v68 is a ~300-line additive evolution of wave_ghost — NOT the announced
   v8 + I/J/H graft.** Diff to opp_v67: 299 lines, every hunk additive except
   one 2-line restructure (:2643-2657). Diff to x3r0's own lineage
   (opp_v56/58/63): ~2,800, unchanged. **None of our pieces I/J/H are
   present** (evidence below). The graft conversation with x3r0 has a clean
   factual basis: his fork still lacks everything he said he'd graft.
2. **No endgame switch exists — the latest behavior change in the file is
   r300.** No r900/960/1000 gate, no MAX_TURNS reference, no rounds-left
   arithmetic (grepped). From r300 to r1000 — 70% of a tiebreak game — v68's
   policy is static. **Any late-game lever we ship (piece H, late surge,
   late link repair) is uncontested.** This is the highest-leverage finding
   for the 6d cycle.
3. **The eponymous chokewall feature is measurably near-dead capital.** The
   agent simulated the planner offline on all 14 current-pool maps, both
   seats: gate (≥80 embedded walls) is OFF on 12 maps; fires on archipelago
   + saga only; and re-running shortest-path WITH the planted barriers:
   **+0 rounds detour on every current-pool seat** (3-6 Ti spent). The only
   +4-detour seat is a 25x15 layout not in the current pool. The width
   heuristic is local (single-BFS-path neighbors) and cannot see parallel
   corridors — it walls the path it found while traffic uses the alternative.
4. **Every measured wave_ghost signature carries over bit-for-bit** (the
   snipe code falls outside all diff hunks): PRIMARY_SENTINEL (:433), first
   forward turret = sentinel, snipe dsq 18-32 (ranges (5,4), :1760), snipe
   window r4-30, 1-gunner rarity. The choke window (r30-140, role_n==1) opens
   after the snipe window closes on a different role — no interaction. **Our
   v67-era decode (wave-ghost-first-read) still applies in full**; the only
   new production signature is one mid-map barrier r30-140 on archipelago/
   saga plus the role-1 builder's walk there.

## Graft check (I/J/H all ABSENT)

- **I (rotation discipline): ABSENT.** v68 retains the exact anti-pattern I
  fixes: bare nearest-bearing rotate in `_turret`'s idle tail (:3555-3565),
  no latch/hysteresis constants anywhere. Contrast _v76e51/main.py:389-439.
- **J (defender counterbattery): ABSENT.** `_try_counterbattery` (:2368) and
  `hive_freeze` (:2626-2632) are the shared _v74e4 BASE (present
  _v74e4:1977/:2218); the J additions (CB_OVER_HEAL, `_live_home_gun`,
  `_cb_over_heal`, freeze return-value change) are all missing.
- **H (endgame switch): ABSENT** — see headline 2.

Provenance oddity on the record: v68's own docstring claims descent from
`_v70mh` "bit-for-bit" (:12-13, OUR internal dir name) AND "bit-for-bit v8"
(:23) in the same header. Also `bots/opp_v56/58/63` meta.json files carry OUR
`florent-v63` deploy metadata — do not lean on those dirs for authorship
claims without re-verification (agent flag, UNCERTAIN).

## Endgame/tiebreak paths (the 6d-relevant detail)

- Round-threshold inventory (complete): r8/12 saboteur flips, r40/42
  harvester tests, r60 replacement spawns, r70 launchwait, r120 HUNT_MIN,
  **r140 CHOKE_MAX (choke stops)**, r150 MEDIC_MIN, r180 launcher give-up,
  **r300 SURGE_MIN — last switch in the file**.
- **Tiebreak #1/#2 engine is real**: LATE LABOR SURGE (:258-275, :883-884,
  :1936-1946) at rnd≥300 AND ti≥1500 → spawn budget +5, eco cap 18→24.
  Harvester building has no round cutoff (:2554). MEDIC protects
  conveyor/splitter/harvester (:236, chain medic :2680-2730). x3r0 has been
  explicitly tuning against 1000-round Ti races (comments :40, :242, :1964).
- **Never dumps ammo; hard caps.** Conversion targets: AMMO_FLOOR 16;
  general ceiling 72 under attack / 48 not; 24 Ti/round max conversion;
  256 only on exact hive anchors (2,20)/(21,3), 32 on atoll (:819-855,
  :824-831). **Stored-Ti tiebreak #3 never zeroed** — and their own comment
  records finishing with "8,957 Ti UNSPENT" (:259-260): v68 finishes rich in
  the bank but converts none of it into anything that scores #1.
- Barrier spend late: choke path hard-stopped r140 (≤9 Ti lifetime); screen
  barriers (:2289-2345) have no cutoff but are triple-gated (under-attack +
  visible enemy GUNNER only + 12-round stale-threat suppression) — small,
  threat-driven, not a drain.

## Mechanism (chokewall loop, for completeness)

Map-decode-time BFS from enemy-core neighbors to own (:1074-1213), walk the
middle third from the enemy side, take the first tile with corridor width
≤ CHOKE_WIDTH_MAX 2; wall = tile + lateral neighbors, cap 3 tiles, no ore,
no core-adjacent (:1152-1164). Only role_n==1, idle-time only (:2643-2657),
window r30-140, ≤9 Ti (:126-133, :3007-3092). See headline 3: +0 detour on
the whole current pool.

## Exploitable weaknesses (ranked; candidate levers)

1. **Uncontested endgame** (headline 2): piece H / late-surge / late-repair
   levers land unopposed after r300. Highest leverage for 6d.
2. **Ammo ceiling low + static**: outside hive anchors it never holds >72
   (48 quiet), converts ≤24 Ti/round — cannot burst against a sustained
   multi-turret push; ammo-starved before Ti-starved.
3. **Map-recognition dependency is total**: `_plan_siege` returns if
   `map_grid is None` (:1740-1741) — on any map not in MAP_CODES, x3r0's
   entire forward game turns off. A pool rotation blinds him wholesale.
4. **Hardcoded seat tuples everywhere** (hive magazine, nordkap/snowflake
   caps, chase_battery): silent no-ops off the exact anchors.
5. **Razor-thin gates**: ORE_STEPOFF_MIN_WALLS=80 with maps at 70/74/80
   exactly; terrain changes flip features.
6. **Interceptor diversion**: role-1 off economy r30-140 (archipelago walk
   ~19 tiles each way); unreachable site burns the builder for the full
   window (:3088-3091).
7. **OUR-SIDE CHECK — RESOLVED by builder (~20:15): our nav ROUTES AROUND,
   never pecks.** `_v79e6c` `_bfs_direction` (:3581-3634, identical across
   the 5.1→6c lineage) adds every visible barrier (either team, :3600-3604)
   to `blocked` before pathing; a barrier target's goal set becomes its
   passable neighbors; no blocked→attack-the-blocker logic exists (movement
   frustration → greedy cardinal step). Barriers are only ever fired at via
   the generic adjacent-fire fallback (:3790-3811) at priority 7 of 8 —
   last-resort idle pecks. Nuance: barriers OUTSIDE vision aren't in
   `blocked` (only get_nearby_entities scanned), so a long route can plan
   through an unseen barrier and re-route on first contact — small one-time
   detour, still never a peck. **Net chokewall-vs-our-nav exposure ≈ nil on
   the current pool**; the inherited snipe is the only live threat.

CPU and exception safety: not levers (decode+choke ≈450 µs vs 10 ms budget;
run() catches all, one-shot traceback, no unit-kill vector). Note
`get_cpu_time_elapsed()` reads 0 in local arena — offline CPU measurements
of this bot are meaningless (matches the tooling doc's TLE trap).

## Production read (replay half — all 35 v68-era games)

**Clock behavior**: median win r97; 11/13 wins are core kills before r140.
Ladder kills fast (1/15 games reach r1000); against the strong unrated
burst (sporks/Jython/not-adgato/Pivot) it grinds — 10/20 to r1000. The
6c arena bar's ~50% tiebreak rate matches the strong-opponent regime, not
the ladder regime (opponent class mix, not a harness artifact).

**Tiebreak behavior — THE lead finding, production-measured over all 11
r1000 games: every single one resolved at chain step 1, titanium
DELIVERED.** Stored-Ti (step 3) was never reached; harvesters-alive (step
2) never reached. Implications:
- Dump-stored-Ti plays are WASTED vs v68; so is starving its stored Ti.
- **The live lever is delivered titanium**: v68 delivers ~250 Ti/100
  rounds healthy and ZERO in ~45% of its long games — 9 of its 11 grinds
  LOST on delivered Ti, several by 5-15x. Keeping a working chain alive to
  r1000 beats it.
- **Delivery-freeze defect (biggest recoverable loss source)**: in 5/11
  games its delivered Ti froze permanently at r59-350 (649-940 dead
  rounds) — conveyor network disconnected from core and never re-attached
  (measured: 95 conveyors alive at r999, 1/95 wired to core, 0 harvesters,
  while it kept laying conveyor). Harvester count flat r700→r999 in 10/11.
- Confirms the code half exactly: zero barriers after r800 (latest
  anywhere: r154), zero ammo conversion after r800 in 10/11 (drip only,
  never dumps), no late build-out. **Survive past ~r150 with core intact
  and v68 has no second plan.**

**Small-map collapse (loss mode 1, unchanged from v67)**: by map area,
4-9 on ≤256 tiles (10x10: 2-4; 21x8: 0-2) vs 9-13 above. On short maps
the sentinel goes defensive near its own core, snipe never fires (0 shots
on enemy core in 3/6 ladder losses), no plan B.

**Snipe carryover confirmed in production**: forward sentinel at dsq 18-32
in 30/35 games, established by r30 in 23/35 (v67 archive: 43/50, 34/50 —
same); first core hit r9-46 in 11/15 ladder games; 22-51 hits per kill
(≈28 shots × 18 dmg = 500 HP checks out).

**Barrier attribution (reconciles A vs B)**: the barriers seen in
production (19 total/35 games; core plugs + 3-tile lane walls marching
out from OWN core at dsq_own 4→9→16, not terrain-aware, IDENTICAL pattern
present in v67, rate 0.40→0.54/g = noise) are the OLD defensive
`_try_screen`/plug code, NOT the new choke planner. No mid-map choke
plant was observed in the archived set — consistent with the code half's
2-of-14-maps gate + idle-only trigger. "Chokewall" the name describes
nearly nothing that happens in production.

**TLE note (resolved by synthesis)**: 0 CPU timeouts in 35 v68 games vs
14 TLE-rounds across 3 v67 games — BUT the CPU self-guard is byte-
identical in both (v67:409-721 / v68:443-767, checked directly) and the
diff is additive, so this is NOT a v68 code fix; attribute to platform
variance until contradicted. v68's substantive content really is just the
near-dead choke feature.

**Baseline correction (flagged to wave-ghost-first-read)**: that read's
"1 gunner in 25 games" reproduces only under a gunner-BY-R30 definition
(v67 archive: 3/50 by-r30; total gunners 0.94/g across 20/50 games). v68:
6/35 by-r30 (~3x, small n), total flat at 0.86/g. Definition, not a v68
signal; the wave-ghost deliverable should be read with this footnote.

Anomalies: zero tracebacks/stdout both sides all 35 games; parser
validated (core_deliv×10 == titaniumCollected everywhere checked).

## Open questions

- **Delivery-freeze mechanism** (5/11 games): pathfinding bug or missing
  chain-connectivity check in opp_v68's conveyor targeting? Worth a
  targeted code look — it's the single largest exploitable defect found.
- **Small-map defensive-sentinel gate**: what distance rule makes the
  forward placement fail when cores are close? (Code look, opp_v68
  `_plan_siege` candidate selection on small grids.)
- Which 26x26/24x24 archived games were archipelago/saga (replays carry
  dims, not names) — determines whether the choke planner EVER fired in
  production. Low priority given +0 detour either way.
- Which arena is the 25x15 (0,0)/(0,13) layout (the only real-detour
  seat)? If rotated out, chokewall is 100% dead on the pool.
- opp_v56/58/63 dir provenance (our meta.json inside — stale copy risk).
- Cost-scale form (additive 1+0.2n vs multiplicative 1.2^n per builder
  bot) — how hard the r300 surge drains v68's bank.
- Ladder-vs-arena regime gap: fold the strong-opponent tiebreak regime
  into gate-battery weighting? (Builder's call; data above supports it.)
