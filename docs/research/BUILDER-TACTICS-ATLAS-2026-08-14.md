# BUILDER-BODY TACTICS ATLAS — 2026-08-14

**Commissioned by Magnus, direct, this session:** *"you can probably do a lot
more with builders than meets the eye — anything in the researcher's library
that matches these tactics?"* **Scope: every use of a builder BODY that is not
build/harvest labour** — bodies as blockers, bait, shields, saboteurs, victims,
deniers, medics, swarms.

**WHAT THIS FILE IS.** A survey of what the knowledge base already contains,
organised by MECHANISM FAMILY, with an honest status per tactic. It closes no
road and opens none; it is a map of where the evidence already is, so a prereg
can be written in minutes instead of a session. **Nothing here is committed and
nothing here is a verdict.**

**HOW TO READ THE STATUSES.**
* **SHIPPED** — in the live tree (`bots/_v223sealrepair`, v140) today.
* **QUEUED (#n)** — a QUEUE.md row with a GREP stamp.
* **REFUTED-WITH-SCOPE** — something died, and the entry says *exactly what*.
  **The distinction this atlas insists on: mechanism-false vs application-dead
  vs price-wrong.** EVICT58 died **against a back-sitting turret bot whose
  builders never enter a pickup envelope**; the eviction mechanism is
  field-proven at 22-33 throws/game *against us*. Those are different facts and
  only the first is a closure.
* **MEASURED-BUT-UNEXPLOITED** — the number exists, nobody built on it. **This
  is the richest category in the file and it is where the cross-breeding
  section draws from.**
* **UNEXPLORED** — no dose, no measurement, no arm.

**THREE STANDING RULES THAT GOVERN EVERY ROW BELOW** (`CLAUDE.md`):
1. **A road closes only on live-game evidence** — arena batteries, corpus cuts
   and engine reads may *prioritise*, never *retire*. Carve-out: a rules-level
   impossibility read off the engine is the game's own definition.
2. **`R1000_IS_DEFEAT: yes`** — economy is instrumental; a tactic whose only
   channel is `titanium_collected` is at best a correctness fix.
3. **`DEFENCE_ADMISSION_BAR: kill_round_non_regression`** — a defensive body
   plank carries a kill-round bar beside its survival bar.

---

## §0. THE ENGINE PRIMER — the nine facts that generate every tactic here

Everything downstream is a recombination of these. All engine-read or
engine-probed, none inferred from opponent behaviour.

| # | fact | source |
|---|---|---|
| 1 | **A body costs 30 Ti and +20% GLOBAL additive scale; the contribution is REMOVED on destruction, SAME-ROUND.** `_probe_refund`: `SCALE 205.000 -> 204.000` with the cost getters moving *inside the same `run()` call*. Culling one surplus builder at scale 2.0 takes a sentinel **60 -> 54**, and the discount is global for that window. **The Ti is NOT refunded — only the scale.** | `docs/coordination.md:20220`; `bots/_probe_refund` |
| 2 | **BODIES CANNOT DAMAGE BODIES.** Builder attack targets BUILDINGS only — `can_fire = False` on an adjacent enemy builder, **every occurrence**. ⇒ **only turret fire and the launcher can remove a body.** "Fifty builders cannot kill one enemy builder." | `docs/prereg/DOSE-feeder45-2026-08-13.md:98`; `tactics/worker-pull-does-not-exist-here.md` |
| 3 | **A body BLOCKS three different things.** (a) **spawns** — 0 spawns in **2,405,604** body ring-tile-rounds; enemy-body class **394,970 tile-rounds, 0 spawns**; (b) **construction** — a tile holding a builder reads `is_tile_empty = True` but `can_build_barrier = False`; (c) **a gunner's ray** — `can_fire` flips True->False with a body in the lane. **A conveyor/splitter blocks NONE of them: 40.1% of 31,913 spawns (12,784) landed on one.** | `loki-arsenal-pricing-2026-08-09.md:121-145`; `bots/_probe_prison`; `turret-line-blocking-2026-08-09.md` |
| 4 | **A sentinel's line passes THROUGH bodies and barriers for full 18 damage, and pass-through friendlies take 0.** ⇒ blockades blank gunners only. `get_attackable_tiles()` returns the target in **both** cases — our own siting code scores coverage a gunner cannot deliver. | `turret-line-blocking-2026-08-09.md`; `tactics/the-blockade-blanks-your-own-guns.md` |
| 5 | **Launch: pickup d²≤2 (full 8-neighbourhood), throw 1≤d²≤26 from the launcher, 0 ammo, cooldown +=1, position-only mutation, NO team check, NO vision guard.** Landing legality is `is_tile_passable`, not `is_tile_empty` — **33.5% of throws land on a conveyor/splitter of either team; 0% on turret/harvester/barrier/core/another bot.** | `engine-source-crash-and-launcher-2026-08-10.md`; `post-throw-tile-dwell-2026-08-09.md` |
| 6 | ⭐ **TURN ORDER IS ENTITY-ID ASCENDING, AND IDS COME FROM ONE GLOBAL CREATION COUNTER** (26,078 consecutive pairs, 0 inversions; 8,802 cross-team pairs, 0 inversions). With **`launcher_id > victim_id`** (equivalently `victim_id < ct.get_id()` — the victim has ALREADY acted this round), **P(victim still on the landing tile ≥1 round) = 99.64%** (N=6,177) against **6.2%** when the launcher moves first (us-only enemy throws: dwell=0 given `L<V` = 93.8%, N≈5,886; ⛔ the previous comparator "1.83%" was mis-sourced — 1.83% is the ALL-THROWS dwell=0 rate on the `L>V`/GOOD side, `:409-410`, corrected s51 2026-08-18 per the side-lane re-drive D2). **48.79% of the enemy bots we currently throw are on the losing side of the comparison.** ⛔ **INEQUALITY CORRECTED 2026-08-17 (s50 wrap): this cell read `launcher_id < victim_id` for the 99.64% side — INVERTED against its own source** (`post-throw-tile-dwell-2026-08-09.md:409-410`: `launcher_id < victim_id` is the **84.14%-dwell-0**/escape case; *the parenthetical here previously said "L<V is the 1.83%/escape case" — itself inverted, fixed s51*) **and against §9.3 of this same file, which had it right.** A cell copied straight out would have filtered targets backwards and bought the worse half. ⚠ **CAVEAT, same source :437 — the filter buys ONE round, not persistence: `P(≥1)=99.64%` but `≥2 = 3.24%`, `≥3 = 1.39%`, `≥7 = 0.71%`.** Any payload needing the victim parked for several rounds is not bought by this filter (see the §9.3 ceiling line). | `post-throw-tile-dwell-2026-08-09.md:404,409-410,437,454,496` |
| 7 | **Heal is the best titanium-to-HP channel in the game: 1 Ti -> +4 HP to ALL friendlies on the tile.** Stack ceiling is **exactly 2** (a builder bot + one of conveyor / splitter / allied core) = **8.00 HP/Ti**, against the best damage source at **1.80** (sentinel), gunner 1.75, builder attack **1.00**. ⇒ **4.4:1 stacked, 2.2:1 bare, in the defender's favour.** | `heal-arithmetic-2026-08-09.md:14-60` |
| 8 | **An uncaught exception from `run()` destroys that unit permanently** (`0x1ac5c` -> `Game::destroy_entity`); `SystemExit`/`KeyboardInterrupt` are the only exemptions. **A CPU timeout does NOT** — it is soft. | `engine-source-crash-and-launcher-2026-08-10.md` |
| 9 | **Population headroom: `MAX_TEAM_UNITS = 50`. We run `MAX_BUILDERS = 5` live and `LOKI_MAX_BUILDERS = 11` lifetime spawns.** | `bots/_v223sealrepair/doctrine.py:28,1196` |

**⛔ AND THE ONE FACT THAT PRICES THE WHOLE FILE, because it is easy to read
backwards:** fact 2 + fact 7 together mean **a body is a defensive object and an
obstacle, never a duellist.** Every offensive body tactic in this atlas
therefore routes through one of exactly three verbs — **occupy a tile, absorb
fire, or be moved by a launcher** — plus the one economic verb (attack a
BUILDING at 1.00 HP/Ti, the worst rate in the game).

---

## §1. WHAT WE ALREADY SHIP — the body inventory of v140

Read this before pre-registering anything. **The cheapest possible null is a
leg that tests a feature we already ship** (`SIX-ROADS-STATUS`, and it has
already happened twice).

| behaviour | where | status/number |
|---|---|---|
| **Ring parking (body denial at the enemy core)** | `raid.py:728 _raid_station` — 12 ring tiles, deterministic seat by raid slot | **emergent, live: a body on the enemy 12-ring in 0.586 of rounds (game-mean) / 0.636 (round-weighted) over 165 games, ~2.3 simultaneous, arriving ~r22.** ⚠ the widely-quoted **68.8%** is UNREPRODUCIBLE (lost 480-game local battery) |
| **Seat-seal barriers** | `raid.py:250-280`, `LOKI_BARRIER_SEAL_ON`, `LOKI_SEAL_TI_FLOOR` **now 0** (was 12, shipped in v140) | **ablation −10pp — our single biggest measured asset.** Seals the 8 tiles that are simultaneously heal seats, delivery tiles and 8 of 12 spawn tiles |
| **SALT (barrier the tile a dead conveyor vacated)** | `LOKI_SALTIDLE_ON`, `LOKI_SALT_BLOCK_ON`, cap `LOKI_SALT_MAX_PER_UNIT = 4` | shipped v178 (#29) |
| **EXILE (throw an enemy builder away)** | `raid.py:895-932` — any adjacent enemy builder, thrown to the reachable site **farthest from OUR core** | shipped; **corpus: 351,260 EXILE events.** No victim scoring, no border selector, no role preference |
| **FERRY / INSERT (throw our own raider forward)** | `raid.py:934-958`, `LOKI_FERRY_ON` | shipped (v112 ferry-first); **151,407 INSERT events** |
| **Buddy heal + opportunistic repair** | `raid.py` buddy heal at `LOKI_BUDDY_HEAL_GAP = 8`; `eco.py:325-343 _heal_adjacent` | shipped but **UNSTAFFED — a builder must already happen to stand beside the damaged thing** (#52) |
| **Defensive siphon** | `SIPHON_WIRE_ON` (wire our orphan harvesters), `SIPHON_DENY_ON` (peck enemy taps on ours) | shipped — **the OFFENSIVE half is absent** (#37) |
| ⛔ **ALL builder melee is OFF** | `LOKI_QUIET_ON = True` — *"no core peck, no siphon hit, no counterbattery"* | **this single flag disables belt-cutting, core-pecking and barrier-clearing by bodies.** Any economic-warfare plank below must either flip it or route around it |
| ⛔ **`destroy()` is never called** | `ct.destroy(` / `ct.can_destroy(` appear **0 times in the whole live tree**; all 11 textual hits are comments | #60 — and `main.py:256` is the comment where we wrote the mechanism down |
| ⛔ **No forward launcher, by explicit design** | `main.py:615-617`: *"One Launcher, near home… ours is ~97% defensive"* | #58's premise |

---

## §2. LAUNCHER-MEDIATED — the body as an object someone else moves

*The only family where a body can be relocated against its owner's will. `can_launch` has no team check and no vision guard; this is the guard asymmetry the whole Loki line was named for.*

### 2.1 Kidnap-to-border crash induction
**Mechanism.** Throw an enemy builder to a legal map-border tile; their own code queries an off-map neighbour, raises, and the engine permanently destroys that unit (fact 8).
**STATUS: REFUTED FOR CLIMBING, SCOPE-EXACT — the mechanism is NOT false; the reachable band is immune.** LOKI-14 fired 15 matches / 75 games: **150 border throws -> 0 undamaged removals; interior placebo 0/164**. The four measured carriers (`vjg` 450.71, `Troupe` 146.43, `S` 105.06, `Ship Happens` 111.55 undamaged removals per 10k border builder-rounds, against **0.000 off-border**, hazard ratio >=17,432x) were all **550-860 rating points below us**; LOKI-14b was withdrawn on its own Amendment 8 — **zero border-gated carriers among the 23 teams at or above our rating; 4 events / 400,852 border builder-rounds = 0.100/10k, >=460x below the weakest carrier.** Confirmed independently on the admissible band: **1 event on 110 border landings (0.91%) vs the same teams' 0.74% not-thrown baseline, Clopper-Pearson UB 4.24%.** The one concentrated cell (team `S`, 3/3) **pays 0.52 rating points for a 5-0**.
**EVIDENCE.** `crash-induction-targeting-2026-08-10.md`; `CRASH-CHANNEL-border-vs-interior-2026-08-12.md`; `PREREG-loki14-crash-induction-2026-08-10.md`.
**STILL OPEN AND CHEAP: QUEUE #17** — the LOCAL both-ways drive vs `bots/_probe_oov_raw` / `_probe_oov_guard`. The weapon is already built (`bots/_v131loki14/raid.py:618`, arms `"B"`=border / `"I"`=interior). **No submission, no rated cost.** #38 (crash at 900-area scale) is blocked on it.
**COUNTER-TECH.** Six teams at exactly 0 across **722,545** border builder-rounds (UB 0.0415/10k). We are immune ourselves by a blanket `try/except` at `main.py:116` — **0 crash candidates across 1,855 games against opponents' 2,451**. League-wide `r(rating, crashes suffered/game) = -0.029, n=67` — **crashing does not predict weakness**, which is why the carriers are all far below us.

### 2.2 Kidnap-to-interior (position desync)
**Mechanism.** Displace a bot off its cached plan; their stale state raises on the next query. Same approved class, different trigger (the class ruling covers *positions, plural and unqualified*).
**STATUS: MEASURED, WEAKLY POSITIVE, NEVER LEGGED.** Naive estimator read -0.080pp and was **retracted for immortal-time bias**; the risk-set-matched correction reads **THROWN 17/3,844 = 0.442% vs CONTROL 13/7,341 = 0.177%, +0.265pp, CI [+0.034,+0.496], z=2.25, 2.50x** — on 17 and 13 events, and `no_damage_removal` conflates crash with `self_destruct()`. Structural ceiling that survives: **2.62%** (360 of 13,743 enemy-builder removals are no-damage at all). `SPEC-kidnap-victim-fate-2026-08-11.md`.

### 2.3 The EXILE loop — serial workforce denial, already shipped by accident
**Mechanism.** A home launcher throws whichever enemy builder enters d²<=2 to the site farthest from our core, forever, for 0 ammo.
**STATUS: SHIPPED (emergent) + QUEUED #51 (aiming it).** Priced off replay `483b5bcd` g1: **259 EXILE throws r47-998 at ~3.7-round cadence, serial victims (89/84/66/20 throws across 4 enemy builder ids), denial rate 100.0% — 0 victim actions in all 259 inter-throw intervals** (5-round rail: a 4-tile throw against a 4-step walk-back). **But marginal value in that game was ZERO** — all 8 enemy builders idled anyway and they out-collected us 14,630:4,270. Diagnosis: **geometry + ammo, not victim choice** (the modal landing pad sat d²=16 from our own sentinel, which faced 180° away; ammo 24 for r100-900 against 30 needed for three sentinel shots).
**THE UNEXPLOITED HALF, and it is one line of code:** fact 6 — filtering to `victim_id < ct.get_id()` takes P(dwell>=1) from **6.2%** to **99.64%** (us-only comparators; the earlier "from 1.83%" mis-read the other side's dwell=0 rate as this side's dwell≥1 — corrected s51), and **48.79% of the bots we throw today are on the wrong side of it.** Ids are a global creation counter, so **a late-built launcher is favourably ordered by construction.** Not implemented anywhere in the tree.
**Ceiling on any ray/kill variant:** **96.4% of enemy victims are off the landing tile within 1 round**; P(on tile >=7 rounds) = 0.61% ⇒ **a kill happens about 1 throw in 200**. `post-throw-tile-dwell-2026-08-09.md` (97,999 throws).
**Related arm:** `AIMTHROW` / `_v222aimthrow` (sort exile destinations onto a friendly sentinel ray + ammo floor 30) — **screened, DEFERRED, no verdict**: GATE-2700 50.55 at 0.05sigma, latest 50.09/50.06 at n~3,933 under a 51 bar.

### 2.4 Forward eviction launcher (throw their medics off the core)
**Mechanism.** Station a launcher at THEIR core in the kill window; pick up the heal/repair staff parked on the ring and throw them away for 0 ammo. **This is the only tool that can remove a healer besides turret fire** (fact 2).
**STATUS: REFUTED AS DESIGNED, TODAY, AND THE SCOPE IS THE WHOLE POINT (QUEUE #58).** Pinned live leg vs **0033** (5 matches / 25 games, `oppver`=v57 x5, `ourver`=v144 x5, pin alarm clean, 36-second prototype exposure, zero rated leakage): **P1 bar >1.0 evictions/game; MEASURED 0.04 — one eviction in 25 games, a 25x miss.** ⭐ **Attribution splits cleanly: launchers BUILT/game 1.240 vs v140's 0.341 = 3.6x — THE PLANT WORKS, THE THROW STARVES.** The binding constraint is **pickup opportunity**: 0033's core kill is 100% turret fire and `batk_core = 0 in 246/246 archived games, every era — they do not send builders forward, so a forward launcher near their core has nothing to pick up.**
⛔ **WHAT IS NOT REFUTED:** the eviction mechanism. **Three opponents run it against US at scale — Jython 32.9 throws of our builders/game (125 games), Focalground 24.7 (55), LingLing40 22.1 (85), 8,274 total.** The failure is **opponent-shaped**. A HOME-side eviction launcher against opponents whose builders *do* come forward is a different question and this leg says nothing about it.
**Prior dose census, and it is why LOKI-21 never got a prereg:** of **34,269 seat-resolved EXILE throws by us**, the ejected builder's d² to **its own** core is median 265, p25 90, and **only 1.8% land inside their heal ring (d²<=8)**.

### 2.5 Home-side / approach-triggered eviction launcher
**STATUS: QUEUED #47, and its own live leg already CLOSED at net -1** (`CLOSED-BY-LEG-INDEX-2026-08-14.md`, leg MC, 8/20 vs 9/20 against a >=+4 bar) — **re-opening needs a named design change, not another leg.** What is established and reusable: detection fires (SIEGE45 15/16); the approach-triggered dose bar was MET 10/16 (frostgate 6/8 at 41-152 evictions/game); with a launcher pre-existing, **205 evictions, all r<160, 0 ammo, best case midgard 993003 — 18 evictions and the enemy ladder NEVER FORMED (0 plants)**. The price it must beat: **standing launcher premium -6.34pp** (LAUNCH0 52.77 +/- 1.33 vs BOTH0 46.43, n=5,408/arm; earlier is monotonically worse).

### 2.6 Ferry / INSERT our own body forward
**STATUS: SHIPPED (v112 ferry-first), verdict NO INFORMATION.** Treatment 13 INSERT / 25 games, win 7/25 = 28.0% vs 37.0% expected = -0.94sigma; the alarm was a comparator artefact (`LOKI27-COMPARATOR-2026-08-11.md`: matched to the leg's 3 opponents, INSERT +4% flat, **EXILE +140%** — both prereg readings invert).
**Standing negative on late ferrying:** median raider life after a forward throw **collapses 43 -> 6 rounds at exactly r150**; own-bot throws die on the landing tile at **5.43% vs 0.03% for enemy victims**. ⇒ **ferrying is the dangerous direction; exiling is the free one.**

### 2.7 RETREAT — pull our own raider OUT with our launcher
**STATUS: UNEXPLORED, and genuinely so — no doc even proposes it.** The decoder already classifies the verb (`tools/corpus/replay_throws.py:140`) and **the field has done it 56,139 times. We have done it zero times.**

### 2.8 The launcher rail (two launchers relay a body in one round)
**Mechanism.** A lower-id launcher throws into a higher-id launcher's d²<=2 ring before that one acts (fact 6), doubling reach in a single round.
**STATUS: MEASURED, USED ON US, JUDGED DOMINATED FOR OFFENCE.** 695 multi-throw bot-rounds over 97 games (689 double, 6 triple), **192/192 own-team chains ascending-id, 0 exceptions**; **enemy pairs railed OUR builders 173 times across 20 games** (Memtrace 147), median displacement 10.0 tiles. The offensive rail costs 78-108 Ti and 3-4 unit-cap slots; **the defensive rail-aware exposure guard was flagged worth building and never was.** Juusto's v11 does the constructive version: **109 multi-hop relays in 75/110 games, median 3 hops / 7 rounds / d² 530->17, 2.52 tiles per round against a walker's 1.0.**

### 2.9 Rent, don't own — demolish the launcher after the throw
**Mechanism.** `destroy()` is free, no cooldown, unlimited per turn, allied buildings only — and **the scale contribution comes back the same round** (fact 1). A launcher kept permanently is what the -6.34pp premium measures; a launcher demolished two rounds after use pays the Ti and **none** of the standing inflation.
**STATUS: QUEUED #60, never tried by us, and the field already runs it.** **Juusto built 403 launchers in 110 games and demolished 402 of them at an age of exactly 2 rounds** (p25 = median = p75 = 2), 3-round cadence, **+132 Elo in 11.7 h**. Our tree calls `destroy()` **zero times**.

---

## §3. BODY-DENIAL — the body as a tile occupant

### 3.0 The mechanical question first: BODY vs BARRIER
Both block `can_spawn`; they differ in price, mobility and removal cost — not in blocking power.

| occupant | ring tile-rounds | spawns per 1k |
|---|---:|---:|
| EMPTY | 5,801,262 | 3.297 |
| conveyor / splitter (either team) | 6,560,018 | **1.95 / 1.86 — DOES NOT BLOCK** |
| **enemy builder body** | **394,970** | **0.000** |
| own builder body | 2,010,634 | 0.000 |
| own / enemy barrier | 201,139 / 12,064 | 0.000 |

Zero-spawn classes pooled: **4,006,984 tile-rounds, 0 spawns.** Only 8 of 14 occupant classes block, and **40.1% of all spawns (12,784/31,913) land on a conveyor** — so "12 tiles occupied" is not a lock. Prices: **barrier 3 Ti / +1% / 30 HP / immobile** vs **body 30 Ti / +20% / 40 HP / mobile**; twelve barriers ~36 Ti + 12%, twelve bodies 360 Ti and roughly triples our own builder price. Removal asymmetry: `destroy()` is allied-only, so **they must peck: 15 builder-turns and 30 Ti to clear a 3 Ti barrier (10:1 in Ti, 15:1 in turns)**, or 5 gunner shots = 20 ammo.

### 3.1 Enemy-core seat seal (our body walks in, our barrier stays)
**STATUS: SHIPPED, and it is our single biggest measured asset — ablation -10pp.** `raid.py:250-280`. The 8 seats it seals are simultaneously the enemy's heal-adjacency tiles, their conveyor delivery tiles, and 8 of 12 spawn tiles. **Open deepening: #52 (staff the heal), #53 (constants never swept).**
**COUNTER-TECH:** pecking. The field pecks our buildings **85.5x/game on average, 19 of 20 opponents with n>=15 non-zero** (Coreflood 196.9, Big O 192.9, Jython 138.9, Juusto 129.4, 0033 101.8, team lazy 96.0; **Leviathan the only zero**).

### 3.2 Ring parking / retention
**STATUS: SHIPPED (emergent); the open margin is RETENTION, not presence.** `_raid_station` walks the body OFF a corner exactly when that corner becomes pure body-denial. LOKI-16b cleared at **+0.164 [+0.073, +0.253]** on `hold_pinned`.
⛔ **DO NOT SIZE A RING PLANK ON CORE-DEATH HAZARD.** The ~2x association replicates (x2.86 over 16.0M core-rounds) and **fails five controls — a core's OWN healers on its OWN ring reproduce x2.02, and same-force-different-tile reads below 1.0 in 44 of 56 cells.** Rules-level and unaffected: **0 spawns in 2,405,604 body ring-tile-rounds.**
⚠ **Instrument warning:** `tools/ring_retention.py` is retired/wrong (66.4% of its "bodies" are buildings, sign-flips); use `tools/ring_read.py tile_episodes`.

### 3.3 The full spawn lock
**STATUS: REFUTED AS STATED, UNTESTED AS A HOSTILE DOSE.** What died: *"partial occupancy is a lock"* (conveyors do not block) and the confounded source table (teams walling **themselves** in). What was never done: a hostile 12/12. **The most bodies any team has ever had on an enemy ring is 6 of 12, four times in 2,710 sides.**
**COUNTER-TECH, and it is decisive:** the defender **steps off** — a parked body makes the tile unspawnable **for its owner too** (`_probe_prison` §4, our own builder arm's words: *"parking IS a complete defence against spawn-lock"*). Unpriced live: our probe victim never moved.
**Second-order fact worth keeping:** a tile holding a builder reads `is_tile_empty = True` but `can_build_barrier = False` ⇒ **bodies and barriers compete for the same tile; a barrier cannot follow a body onto one.**

### 3.4 Self-inflicted denial (we lock our own bodies in)
**STATUS: QUEUED #64 SPAWNPOCKET (prereg committed), #63, #54.** 925 locked bots over 529 games; **11.58% of our builder-rounds locked, 39.9% of locked bots never acted**; class-P sealed pockets 99 bots — **37 terrain (valkyrie 100%), 62 sealed by our own conveyors** (midgard 30, fjordgate 10). Ours-vs-theirs lock rate **11.4% vs 4.7% pooled; midgard 35.6% vs 10.9% (3.3x)**. ⛔ Amendment A1 killed the spawn half: every valkyrie spawn candidate reads region >=40 — **pockets are ENTERED, not spawned into.** Two detect-and-repick arms are already dead (OSCLOCK **48.53**, OSCLOCK2 **46.49**) ⛔ *(CORRECTED s43: this cell read "OSCLOCK 46.39, OSCLOCK2 46.39/46.49" — 46.39 is OSCLOCK2's GATE-1800 number duplicated onto OSCLOCK, which never read it at any checkpoint. One measurement was appearing as two independent confirmations, in TWO documents.)*; **any successor must change NAVIGATION or DESTINATION, not detection.**

### 3.5 Body-blocking an enemy gunner's lane
**STATUS: QUEUED #10, UNEXPLORED IN BOTH DIRECTIONS.** Engine-measured: a gunner is blocked by any body or building in the line (`can_fire` True->False); **a sentinel passes through, full 18 damage, and pass-through friendlies take 0.** ⛔ `get_attackable_tiles()` returns the target in **both** cases — our own siting code scores coverage a gunner cannot deliver. Blocked only on a decoder choice (`tools/loki9_facing.py` computes exact-ray collinearity, not a 45-degree tolerance). **A validated replay case shows a gunner killing its own builder (13 hits, 56 damage).**

### 3.6 Turret-plant-tile pre-occupation
**STATUS: REFUTED, EXACT SCOPE — per-tile enumeration only.** Held-out cover 70.4% against a random-in-band null of 66.6% (+3.8pp); restricted to tiles we never build on, the lift is **negative at every threshold (-3.0pp)**; **97.2% of enemy plant tiles are tiles we build on too.** ⭐ **The BODY-parking variant was never tested — only placed buildings.**

### 3.7 Chokepoint / corridor walls
**STATUS: OPPONENT-SIDE ONLY; does not bind us.** x3r0's v68 chokewall: gate off on **12/14 maps**, and with barriers planted **+0 rounds detour on every current-pool seat**. Our `_bfs_direction` adds every visible barrier of either team to `blocked` and routes around; `LOKI_QUIET_ON` means we could not clear one anyway.

---

## §4. ECONOMIC WARFARE WITH BODIES

⚠ **Under `R1000_IS_DEFEAT` these pay only as TEMPO or as DENIAL-OF-DEFENCE. A plank whose only channel is `titanium_collected` is off-currency.**

### 4.1 The two things that get confused
**(a) The REFUTED siphon — pushing stacks INTO their core is a GIFT.** `distribute_resources` reads the **core's own** team byte and bumps **their** `titanium_stored` and `titanium_collected`; `can_accept_from` returns 1 unconditionally. **No poison path exists. CLOSED, stays closed.**
**(b) The STILL-OPEN team-blind tap.** `output_targets` gives a harvester all four orthogonal neighbours **team-blind**, one edge per source per round, LRU-ordered. Constructed probe: **sole enemy acceptor -> 49 of 49 stacks banked by the enemy; one acceptor per team -> 99/98 strict alternation over 800 rounds, zero exceptions.** Wild corpus: **4.41% of every stack we mine is banked by an enemy core** (1,812/41,055), 81% through exactly this shape, worst game 58.5%. And build legality is answered: **we already plant a conveyor orthogonally adjacent to an enemy harvester 283 times across 183 of 1,586 games, incidentally.**
**STATUS: QUEUED #37 (offensive arm absent; we ship only the defensive WIRE/DENY).** ⚠ **Mostly off-currency** — the r1000-insurance channel is ~6% of games and **we are sink-constrained, not income-constrained (median 7,052 Ti banked at game end, net -391 on `ENEMY_CORE` flow).** It survives as a **denial** lever against core-tank teams: halving a harvester's output defunds a 4 HP/Ti heal wall **without destroying anything** (and so without the scale rebate below).

### 4.2 Belt-cutting + SALT
**Mechanism.** 20 HP conveyor = **10 pecks = 10 builder-turns + 20 Ti**; then a 3 Ti / 30 HP barrier on the corpse costs them **15 pecks = 30 Ti + 15 builder-turns** to clear.
**STATUS: SHIPPED as the one carve-out to `LOKI_QUIET_ON`.** SALT screened **61.00% at n=5,408, z=+16.2** (null 49.56), replicated 60.56; kill share 57.6% vs 35.8%. Live leg: mechanism **20/20 corpse-salts at median latency 1 round** — but **tempo FAILED: 13 kills at median r179 against a pooled r129, MW p=0.008**. The idle-gated revival's median kill round **210 -> 218 remains UNRESOLVED against `DEFENCE_ADMISSION_BAR`.**
**COUNTER-TECH.** The field **repairs 40.5% of cut conveyors at median latency 4 rounds** (n=27,871) — a bare cut is a loan, which is exactly why the salt barrier is load-bearing. **Leviathan heals belts in place (127 conveyor heals vs our 79 cuts in one game) ⇒ belt-cutting is CONFIRMED DEAD against healers.** Same-tile restore rates: Coreflood 12%, team lazy 39%, LingLing40 60% (15 of them in one game).
**Our own mirror, and it was our biggest leak:** we are cut at the field rate (14.4% vs 15.0%) but **repaired 6.8% against the field's 40.5% — a ~6x deficit**, fixed s40 as `LOKI_L4_REPAIR_ON` (SEALREPAIR 59.26 at n=5,400). We **inflict 2.1% where the field inflicts 15.0%.**
⛔ **UNPRICED HAZARD ON EVERY CUT: destroying an enemy building LOWERS THEIR COST SCALE.** Every conveyor cut hands back +1% and every harvester kill +5%. **Costed nowhere, including salt's own prereg.**

### 4.3 Ore-tile denial
**Mechanism.** Harvesters build only on ore; a 3 Ti barrier makes `can_build_harvester` fail. **A parked body is strictly worse** — it makes the tile unspawnable for its owner too and cannot be left behind.
**STATUS: the tile bind is MEASURED AND STRONG; the economy bind is UNRESOLVED.** 3,430 rated games: a barriered our-side ore tile receives our harvester at **0.28x** the same-game control rate when barriered r<=60 (re-derivation: **0.106x, n=389 vs 1,853, z=-15.78, paired t=-21.98 over 199 games**), decaying to ~1.0x past r150, and **85.8% of 1,929 barriers stand to game end**. The **-20pp win association is a MARKER** (collapses to +0.8pp conditioning on harvester deaths by r150). Historically we built it: `_v70sb` halved kladde's collection **8,880 -> 4,120** — **parked, not refuted.**
**QUEUED #7 (offence) / #49 (defence, cut landed) / #39 (opening-book pre-emption).** ⭐ **The carve-out both primaries preserved and nobody has ever measured: barrier an ore tile a FORWARD GUN ALREADY COVERS.** Also unmeasured: the **>=50%-coverage tail** (17.3% of games, 8 at 100%).
**COUNTER-TECH: essentially none — 85.8% are never cleared.** Our own counter is accidental and bad: the harvester planner silently drops a barriered tile from its candidate set rather than contesting it. Prevalence against us: **19.8% of rated games** (team lazy 80%, I Stone 70%, Focalground 55%, Jython 40%).

### 4.4 The medic arithmetic — and a correction to our own source
| channel | cost -> effect | HP per Ti |
|---|---|---|
| fresh barrier | 3 Ti -> 30 HP | **10.00** |
| builder heal | 1 Ti -> +4 HP, all friendlies on the tile | **4.00** (8.00 on a 2-entity stack) |
| sentinel | 10 ammo -> 18 dmg | 1.80 |
| gunner | 4 ammo -> 7 dmg | 1.75 |
| builder attack | 2 Ti -> 2 dmg, **buildings only** | **1.00** |

⛔ **THERE IS NO 8:1 EXCHANGE AGAINST A BARE BARRIER. The true ratios are 4.0:1 against builder pecks and 2.22:1 against the best damage source; 8.00 HP/Ti is the AoE CEILING on a stacked tile (exactly 2 entities: a builder + one of conveyor/splitter/allied core), i.e. 4.4:1 over a sentinel.** **Our own `eco.py:328` comment says "eight to one on titanium" and QUEUE #52 quotes it as the plank's justification** — the plank is still right, its headline number is 2x optimistic against the case it names. **Fix the comment before the prereg quotes it again.**
**Staffing arithmetic:** one medic offsets exactly **two** attacking builders (4 HP/turn vs 2 dmg/turn) *and* the pecker forfeits its move while the healer does not; **4 healers on a 2x2 footprint = +16 HP/round = exact standoff with the theoretical maximum 8-tile peck rate; a 5th makes the core unkillable by builders.** Ceiling 8 seats = **32 HP/round, 2.1x the highest siege DPS ever measured against us (23.22)**. **What caps it is BODIES, not titanium** — terminal living builders 4.19 (us) / 4.06 (league), observed max healers ever 7, and the 12th builder alone costs 30 x 1.2^11 = **223 Ti.**
**Cancellation has an exploitable shape:** at 1 attacker we cancel 57-66% (field 32-36%); **at 3+ attackers we invert to 27-33% while the broad field does not scale back (no-us 34.6%, top tier 31.5%)** ⇒ **multi-shooter concentration beats most of the ladder's heal response. Measured, correlational, never legged.**
**STATUS: reactive core-heal SHIPPED (`MEDIC_TI_FLOOR=20`, `MEDIC_MIN_RND=150`, 164 heal sites); COLLAR MEDIC QUEUED #52 and PROMOTED tonight by Magnus** (commit `85c149d`, 2026-08-14 19:50:53 +0200) **because its stated blocker was wrong about the field** — self-play coverage is 0 by construction (`LOKI_QUIET_ON` means we never peck), but **the live customer is 19 of 20 opponents at 85.5 pecks/game.** ⚠ Not yet established that those pecks land on the barriers this plank heals — `batk`-by-target is the first cut.

### 4.5 Anti-medic (removing THEIR healers)
**Engine constraint first: bodies cannot touch bodies, so only a turret or a launcher can remove a healer.**
**STATUS: dose-refuted twice, mechanism intact.** LOKI-21 died pre-prereg on the corpus dose (1.8% of our 34,269 exile throws land inside their heal ring); EVICT58 died live on 0.04 evictions/game vs a >1.0 bar (§2.4). **The targets are real and measured:** team lazy **92.3% of heals on their own core (803/870), up to 9 simultaneous healers parked on the 8-ring for consecutive rounds**; Coreflood 89.8% (1,783/1,985); Leviathan won a game on **1,056 core heals with zero harvesters**. **The arithmetic that makes this the highest-value target class: their 4 HP/Ti heal against our 1.8 dmg/Ti sentinel = a 2.2x titanium deficit — one sentinel structurally cannot kill a core-tank** (net core damage in our four Leviathan losses: 0/0/14/0 HP of 2000).

---

## §5. SWARM / MASS / DISPOSABILITY

### 5.1 Suicide-body rush
**REFUTED BY RULE, permanently.** `self_destruct()` deals **0 damage** — and the ancestor league's changelog says why in as many words: *"Removing builder self-destruct damage nerfs rushes."* `mechanic-bans-2026-08-09.md`. Do not re-derive.

### 5.2 Cheap-builder swarm / mass rush
**REFUTED BY RULE + ARITHMETIC.** Builder base went 10 -> 50 -> 30 Ti upstream with *"more expensive builders and a global unit cap… reduce spam"*; here the **+20% additive scale makes the 20th builder cost 958 Ti.** The field agrees the cap is irrelevant: **median 8-9 units alive at r250, 0.0% of teams reach 45**; live builders at r100/r200 — us 4.57/5.16, them 4.44/5.20. **The builder kill-wave is not merely absent, it is INVERTED: spawns FALL into the kill window everywhere except us.**
⇒ **"Swarm" in this engine can only mean 6-12 bodies, never 40.** Any TINY-SWARM row must be priced against `958 Ti at n=20` and against our own spawn budget shape (cap 5 -> 13 -> 18; **34.7% of games end at exactly 5 builders**).

### 5.3 Disposable bodies and the scale refund — the fact, and the three planks it has already killed
**THE FACT IS REAL AND MULTIPLY-SOURCED.** (i) Disassembly: `get_scale_percent@0x11fb8`, *"its contribution removed when that team's building is destroyed"*. (ii) **Replay fit over LIVE entities: 5,050/5,051 = 99.98% of clean single-build rounds; the `--corrupt=live` arm (do NOT decrement on death) collapses the fit to 50.66%** — that negative control is what makes the death-decrement a measurement rather than a reading. (iii) Timing: `_probe_refund` shows **SCALE 205.000 -> 204.000 inside one `run()` call** ⇒ demolish-then-build at the lower price in the same turn, and the discount is **global** for that window.
⛔ **AND IT HAS KILLED THREE PLANKS ON MAGNITUDE, not on mechanism** (QUEUE #27 family): `LOKI-2` destroy/scale-prune **REFUTED** (median 2 prunes against a 300-590% scale) -> `LOKI-43 LAUNCHRENT` **WITHDRAWN** (~12pp scale, ~24 Ti, **14x short**) -> **`LOKI-48 IDLE CULL` BUILT, FIRED, REAL NEGATIVE: 33.5% at n=3,774** (`bots/_v176idlecull`, `IDLE_CULL_RNDS=12/MIN_RND=120/FLOOR=6`), against an informative band of 48.67-51.33. Break-even on builder churn needs **400-580 Ti built while the body is dead**.
⛔ **TWO ASYMMETRIES THAT REVERSE THE INTUITION.** (a) **`destroy()` cannot reach a builder — units are not buildings; only `self_destruct()` can**, and the direct probe *"does `get_builder_bot_cost()` drop after `self_destruct()`?"* **has been queued three times and never run.** (b) **Killing THEIR builder REBATES THEM 20%** — *"killing is a rebate; imprisoning is not… never kill a capped opponent's builder, you are freeing their slot."*
⇒ **The surviving member of the family is #60 RENT-DON'T-OWN, and it survives on the field's evidence rather than ours** (Juusto 402/403 launchers demolished at age exactly 2, +132 Elo in 11.7 h). **Its prereg owes an answer to LAUNCHRENT's 14x-short arithmetic** — the two rows disagree and neither cites the other.

### 5.4 Body-forward as a weapon
**REFUTED, EXACT SCOPE.** Builder melee is **2 Ti -> 2 dmg, buildings only, 1.00 HP/Ti — the weakest positive trade in the game**, and it is **3.0% of top-tier kill damage** (median builder attacks on a dying core: **0** in every population; gunner 57.6%, sentinel 39.4%). But the same channel is **59.82% economic / 81.4% non-core of all 2,372,822 archived builder-attack events** ⇒ **bodies are demolition tools and couriers, never payloads.**

### 5.5 ⛔ ~~The immunity theorem~~ — **REFUTED s50, 2026-08-17, by direct engine probe. The premise is false.**
**⛔ THE PREMISE — "Builders may stand on their own core (`is_tile_passable` admits … allied core)" — IS FALSE: probed 1,996/1,996 core-footprint tiles IMPASSABLE to the owner's own builders** (`docs/research/PROBE-DOSSIER-ferry-siege-2026-08-17.md`; the 2026-08-08 corpus read said the same and this section overrode it). Healers therefore stand on the **12 ring tiles**, never the footprint — and ring seats can be DENIED by barriers and eviction, which is exactly the Jython seal measured the same day (heals driven to 0.0000/round under a full 8-orthogonal seal, `REPLAY-STUDY-jython-v157-wider-2026-08-17.md`). **There is no mathematical unkillability; a sealed core cannot be body-healed at all.**
~~Two healers on a 1x1 repair 8 HP/round … a fifth makes the core mathematically unkillable by builders.~~ *(original text struck; kept for provenance)*
⇒ **Downstream users of this section — §5.2/TINY-SWARM's "proof of futility" (line ~351/~359) and any plan that priced body-mass against "a healed core" — lose this premise.** What survives independently: bodies still cannot attack bodies, and heal-throughput vs turret DPS is measured elsewhere (`AUTOPSY-erebus-v143-fastrush-2026-08-17.md`: heal law = min(adjacent bodies, bank), gunner-grade grind loses 2.29:1, sentinel-grade wins).

#### 5.5a ADDENDUM 2026-08-17 (s50 wrap, routed from the build report) — ⭐ **P6: AN ENEMY BODY BLOCKS A BARRIER BUILD, so sealing a body-held ring seat requires EVICTION FIRST**
`can_build_barrier` on a seat that holds an **enemy** builder body, with no building on it and the barrier affordable: **FALSE 40/40**. Empty-seat control on the same games: **TRUE 383/383**. 1,438 adjacency readings across 8 games — **both verdicts driven, and the control is what makes the 40/40 mean anything.** (`docs/research/BUILD-REPORT-v512ringladder-2026-08-17.md` §P6; recorded in-tree at `siege.py:494`.)
**Relation to fact 3(b) in §1:** that cell already said a tile holding a builder reads `is_tile_empty = True` while `can_build_barrier = False`, off `bots/_probe_prison`. P6 is the **enemy-body** case measured **in live games with an empty-seat control** — so fact 3(b) is now team-blind on evidence rather than by assumption.
⇒ **Eviction is a PRECONDITION of sealing, not an alternative to it.** Magnus's rung order — evict at rung 2, *before* the clears at rung 3 — is **engine-correct**, and a rung-1 seal attempt failing on a body-held tile falls through to rung 2 by design rather than by accident.
⚠ **AND IT RE-PRICES EVERY SEAL ESTIMATE IN THIS FILE: all "barriers needed" figures are OPTIMISTIC by the body-held share of the ring**, because each body-held seat costs an eviction (a launcher throw and its cooldown) before the 3 Ti barrier is even legal.
**This is the constructive complement of the struck theorem above:** §5.5 died because bodies *cannot* stand on the core footprint and the 12 ring seats are deniable — P6 says what denying an *occupied* seat actually costs. It also sharpens the §5.5 tension the ringladder build measured: **the sentinel that wins games pulls defender bodies onto the ring, where by P6 they block the very barriers the seal wants.**

---

## §6. BAIT, AMBUSH AND ABSORPTION

### 6.1 Bodies as bait — refuted; BUILDINGS as bait — measured and good
**Exchange rates: a 3 Ti barrier costs them ~17 Ti of ammo = 5.6:1. A 30 Ti builder costs them ~22 Ti = 0.74:1** (restated elsewhere as 0.8:1). ⇒ **bodies are bad bait and buildings are good bait**, which is the opposite of the RTS intuition. The drain-pump/ammo-bait plank as a whole is a **powered null** (their income -2%, whole-pump ceiling 0.49 Ti/round = 5.1%; the empty-tile placebo predicted our *worst* outcomes at -0.257). **Interceptor-saturation bait is DEAD** — the minimum inter-throw gap is 1 round for every throwing opponent.
⭐ **THE SURVIVOR, AND IT IS ALREADY MEASURED POSITIVE: heal OUR OWN absorber — +1.69 Ti/round, +7pp, p=0.045.**

### 6.2 ⭐ Persistence blindness — the field cannot tell that a target is not dying
**97.9-99.4% of shots on a heavily-absorbing building fall within +/-2 rounds of a heal on it — they never re-target when HP stops dropping.** Worst single case on record: **one Ouroboros gunner put 677 shots into a single healed 3-Ti conveyor** (= **2,708 Ti of ammo**, against a league median Ti->ammo conversion of **616-758 per game**). Powerpuff 634, OopsGotYourElo 531, Leviathan 446, Lunds 428, KCM 427.
**STATUS: MEASURED-BUT-UNEXPLOITED — we have never deliberately sited an absorber.** **Dead against** Memtrace, Team 48, Askar, Banminary, The Bisons, gsxWins, Focalground (max absorb 7-19 shots).

### 6.3 Rebuild ambush
**QUEUED #13, never built.** Of **15,958** of our turret-destructions, **22.6% produce a rebuild on the exact tile within 25 rounds** (33.8% at d²<=2, 42.5% at d²<=8); conditional on any rebuild, 35.2% land on the rubble. **Our opponents rebuild in place more than the top tier does (22.6% vs 13.0%) — this is worth more to us than to them.** Siege-turret rebuild latency is far faster than belt rebuild: **Coreflood median 2 rounds on the identical tile; LingLing40 [1,1,1,1,1,2,2,5,9,10,12,38,69]** ⇒ **every turret we kill is refunded before our next action.**
**THE DESIGN FORK, and only one branch is cheap:** killing the returning builder with **melee costs the raider its move round** (`_raid_act` returning True ends the turn; `_v150cbturret` read 45.2%, core kills 0.82x) — **a PRE-PLACED turret covering the rubble is free.** And note fact 2: **melee cannot kill the rebuilder at all** — only the turret branch is even legal.

### 6.4 Feeder targeting
**QUEUED #45, iteration 1 read out: MECHANISM WORKS, EXPOSURE-STARVED (FEEDER45 fired in 1 of 16 games; off-branch 0/4).** The target class is measured and large: **LingLing40 v40 — 80 siege turrets, median d²=5 from our core, 58 of 80 gunners, rebuild latency 1-2 rounds**; team lazy v222 — 48 turrets, same shape. **The turret is renewable; the 40 HP feeder is not.**
⛔ **The two engine facts this iteration banked are what constrain every successor: builder melee cannot target an enemy builder bot, and class attributes do not share across units. ⇒ the only anti-feeder tools are TURRET FIRE and LAUNCHER EVICTION.** The turret-side arm already read null: **HEALERFIRST `_v174healerfirst` 50.80% at n=5,408** — dose-confirmed (30 vs 19 builder kills) but our own sentinel losses rose 18 vs 13. `get_gunner_target()` offers no target choice, so feeder-first can only ever govern **sentinels**.

### 6.5 Feints, decoys, sacrifice-prep
**CLOSED BY SURVEY, cheaply.** A machine-grep of **123,745 words across 22 Battlecode postmortems** returns **0 hits** for `decoy`/`feint`/`deceiv`/`bluff`/`mislead`/`disguis`/`fake`. Our own corpus adds a null: **winner-side loss curves are monotone and peak AFTER first contact — nobody spends anything up front.** ⇒ do not spend a leg on deception-of-the-bot as a primary mechanism.

---

## §7. CRASH-CLASS — bodies as victims

**Standing permission and its one limit** (`CLAUDE.md`): crash-induction was asked of the organisers and is **APPROVED as a class**; the approval's wording is *"positions, plural and unqualified"*, so **a new TRIGGER needs no new question — a new MECHANISM would.** Build and fire without asking.

| trigger | status | the number |
|---|---|---|
| **map-border throw** | **REFUTED for the reachable band** (§2.1) | 150 border throws -> 0 removals; band-wide 1/110 = 0.91% vs a 0.74% baseline, UB 4.24%; the only carriers are 550-860 points below us and a 5-0 there pays **0.52 rating** |
| **interior displacement** | **MEASURED, weakly positive, never legged** (§2.2) | +0.265pp [+0.034,+0.496], z=2.25, on 17 vs 13 events |
| **barriers planted inside their base** (their pathing raises) | **QUEUED #43, unfired** | **6/6 no-damage builder removals, ALL theirs, ALL in the one game we planted barriers inside their base**, 5 of 6 at r81-111 at d²1-5 from their core; one bot spawned r98 and vanished r99 without ever moving |
| **CPU-timeout induction** | ⛔ **HELD ON NORMS** — Magnus owes the organisers a question first. Do NOT merge it with the measurement half. | headroom is measured and real (Kvarnholmen **23.4% of unit-turns TLE'd**; Erebus 0.77% and **in our band at 1824**; ours 107 of 23.3M = 0.0005%) |

**THE FIELD IS FRAGILE AND WE ARE NOT.** Across 1,855 of our archived games: **opponents 2,451 unexplained unit removals, us 0** — ours is 0 because `run()` is wrapped in one blanket `try/except` at `main.py:116`. League-wide **11,239 candidates over 10,199 files (28.7% of files)**; **the field's bodies die undamaged at 10.35% (2,636 of 25,466) and ours at 0 of 539.** But `r(rating, crashes suffered/game) = -0.029, n=67`: **fragility does not predict weakness**, which is exactly why the border road failed upward. ⚠ `crash_census` is **structurally blind to Juusto** (their build->throw->demolish recycle has the same wire signature) and cannot separate a crash from `self_destruct()`.

---

## §8. FIELD COUNTER-TECH — who guards what

| guard | who has it (number) | who does not |
|---|---|---|
| **throws our adjacent bodies away** | Memtrace **92.7% of 9,426 adjacency episodes, median latency 0**; Lunds 98.6% of 1,760; Focalground 87.4%; OopsGotYourElo 74.7% | **zero enemy throws, every version: Ouroboros, KCM, CtrlAltDefeat, Powerpuff, Leviathan, Orizon, Team 48, Banminary, 0033, I Stone, The Bisons, farming_200s** |
| **rotates a gunner onto an approaching body** | Banminary 155.6 rot/1k gunner-rounds; Lunds 18.4; Ouroboros 17.7; 0033 8.5 (96.8% with our bot near vs 69.3% baseline) | **hard zeros: Memtrace (all versions), Team 48, OopsGotYourElo, The Bisons, gsxWins, Focalground** |
| **heals under attack** | Ouroboros 79.3% of first-damage events answered within d²<=4 (median 8 rounds); OopsGotYourElo 79.2%; Powerpuff 73.8%; Lunds 70.5% | **The Bisons 0.0% on 116 triggers**; farming_200s 9.5%; Team 48 17.3% (median latency 70.5) |
| **repairs a cut belt** | field **40.5% same-tile at median 4 rounds** (n=27,871); **Leviathan heals in place — 127 conveyor heals vs our 79 cuts** | Coreflood 12% |
| **rebuilds a killed siege turret** | Coreflood median **2 rounds** on the identical tile; LingLing40 1-2; Juusto 1,1,2,2,6…; Leviathan replaces 61.9% within 20 rounds at d²<=25 | gsxWins / Focalground 0.0% |
| **counter-attacks our forward turret with melee** | Coreflood 6 of 28 cases; team lazy answers with a **counter-gunner built at d²=1 in 31 of 52 pairs** | **Juusto 1 of 23** (turret fire only) |
| **clears a barrier on its ore** | essentially nobody — **85.8% of 1,929 barriers stand to game end** | — |
| **survives a border throw** | 6 teams at 0 across 722,545 border builder-rounds; Bisons 0/426 games, 0033 0/371, LingLing40 0/15 — **"guarded" and "never triggered" are not separable here** | the four low-band carriers (vjg, Troupe, S, Ship Happens) |

**REACTION LATENCY / BLINDNESS WINDOWS a body tactic can ride** — team lazy: first *shot* at our forward turret +2 rounds, first defensive *build* **+9 rounds**, and **zero home defence before our first intrusion in 10/10 games**. Juusto: home-defence reaction median **5 rounds**. LingLing40: any post-intrusion defensive build in only **4 of 15 games**. Displacement recovery: a thrown builder is back in launcher range in **median 6 rounds** (p10 4, p90 17). **0033 is script-blind: 100% identical first 4 builds, 99% first 8, 87% first 14 across 368 games** (opponents' control 47%).

**OPPONENT BODY DOCTRINE, for target selection** — **20 of 20 teams above us use builder melee** (median 90% of games) against 57.2% below; five doctrines: belt raid (0033 74%, sporks 70%, kladde 68%), core peck (Jython 39.6%), counter-battery (Pantheon 70.1%), **breaching our barriers (Erebus 93.7%)**, harvester kill (Flotte 53.9%). **Juusto v11 is the field's most developed body doctrine: 395 INSERT throws of their own builders and 0 EXILE, 109 multi-hop relays (median 3 hops / 7 rounds / d² 530->17, 2.52 tiles per round), landing a builder that plants 717 barriers of which 98.7% sit at d²<=5 of the defender core, at median r32 against our own ring-seal at median r51.** They run our plank **19 rounds earlier and 40% heavier.**
**Band note (`target_value` is stale on exactly the teams worth targeting, #56 — recompute at fire time):** Juusto 1883.3 vs us 1744.3, gap +139, **a 5-0 pays +22.08**; The Bisons band-admissible; 0033 ~1850 and our worst matchup (30.0% h2h in the v43+ era).

---

## §9. ⭐ CROSS-BREEDING — combinations nobody has assembled

**The method: two shipped or field-proven mechanisms whose PRECONDITIONS overlap and whose EFFECTS multiply. Each entry states the composition logic, not just the pairing.**

### 9.1 THE TWELVE-SEAT CLOSURE — seat-seal (shipped) + launcher eviction, aimed at the core-tank class
**The mechanism logic, and it is a geometric argument nobody has written down.** To heal a core a builder must stand on a tile orthogonally adjacent to a core footprint tile. There are exactly **twelve** such tiles: the **8 ring seats** and the **4 core footprint tiles themselves** (a builder on one core tile is orthogonally adjacent to the next, and `is_tile_passable` admits a bot onto its **allied** core).
* **We already seal the 8 ring seats** — that is the -10pp asset (§3.1).
* **We can never occupy the other 4** — an enemy core is not passable to us.
* **A launcher is the ONLY tool in the game that can clear those 4 seats** (fact 2: bodies cannot touch bodies; turret fire onto a core-footprint tile hits the core, not selectively the healer).
⇒ **the two mechanisms are complements, not alternatives, and together they close all twelve.**
**Why it survives #58's refutation:** #58 died on **pickup opportunity against 0033, a bot that never sends builders forward (`batk_core` = 0 in 246/246 games)**. The core-tank class is the exact inverse: **team lazy parks up to 9 simultaneous healers with 92.3% of heals on its own core (803/870); Coreflood 89.8% (1,783/1,985); Leviathan won a game on 1,056 core heals with zero harvesters.** **The envelope is populated by construction there.** And the infrastructure is already live-validated: **#58's conditional plant fired at 1.240 launchers/game vs 0.341 = 3.6x.**
**What it is worth:** their wall is 4 HP/Ti against our best 1.8 dmg/Ti — **a 2.2x titanium deficit that one sentinel structurally cannot beat** (net core damage in four Leviathan losses: 0/0/14/0 of 2000). **Each evicted healer removes 4 HP/round for 0 ammo**, and the eviction is repeatable at the launcher's 1-round cadence.
**Cost: a DOSE PROBE first** (local, free): evictions/game against `_probe_camper` / `_probe_repairer`, which have parked healers by construction. Then a pinned live arm.

### 9.2 THE RING DUMP — one-line destination change on a mechanism we already fire 351,260 times
**Composition logic:** today EXILE throws the victim to the site **farthest from OUR core** — a destination chosen to protect us, not to hurt them. But **a body on a spawn-ring tile blocks a spawn 1:1, and it does so for its OWN owner too: 2,010,634 own-body ring tile-rounds, 0 spawns.** ⇒ **throwing THEIR builder onto THEIR OWN ring turns their unit into our blocker, at 0 ammo, with no unit of ours committed.** It composes with the seal because **the seal already holds up to 8 of the 12 tiles** — the throw supplies the tiles a barrier cannot reach (a barrier cannot be built on a tile a body stands on, and cannot follow a body).
**This is the assembly of the full 12/12 lock out of two shipped parts. Nobody has ever reached it: the most bodies any team has had on an enemy ring is 6 of 12, four times in 2,710 sides.** ⚠ The lock's own honest ceiling: **the core needs exactly one free tile**, and the defender's counter is to step off (which costs that builder its action or its move — itself a denial).
**Prerequisite it shares with 9.1:** the launcher must be within throw range of their ring ⇒ **the same forward launcher.** ⇒ **9.1 and 9.2 are one deployment with two payloads and should be dosed together.**

### 9.3 THE ID-ORDER FILTER — one integer comparison that multiplies every throw plank
**Composition logic:** every payload above (ring dump, jail, gunner-lane blind, AIMTHROW's ray) needs the victim to **still be on the landing tile when the effect is evaluated**. Turn order is entity-id ascending; **with `launcher_id > victim_id` (the victim has already acted) the victim is still there next round 99.64% of the time, against 6.2% otherwise** *(inequality + comparator corrected s51 2026-08-18: this sentence carried the same inversion fact 6's s50 fix removed, in the same sentence as its own correct code form)* **— and 48.79% of the bots we throw today are on the wrong side of it.** Ids come from one global creation counter (0 inversions in 26,078 pairs), so **a late-built launcher is favourably ordered by construction**, and the filter itself is `if victim_id < ct.get_id()`.
⇒ **This is not a plank, it is a multiplier on the whole family, and it is the cheapest item in this atlas.**

### 9.4 THE AMMO-SINK COLLAR — #52 (belt-medic dispatch) x ammo-drain x persistence blindness
**Composition logic, three measured facts that have never been put in one place:**
1. **Buildings are good bait and bodies are bad bait** — a 3 Ti barrier costs them ~17 Ti of ammo, **5.6:1**.
2. **They cannot tell it is not dying: 97.9-99.4% of shots on a heavily-absorbing building fall within +/-2 rounds of a heal on it, and one gunner spent 677 shots (2,708 Ti of ammo) on a single healed 3-Ti conveyor** — against a league median conversion of 616-758 Ti/game. **Ammo has no passive income; every point is titanium deleted from their bank.**
3. **Healing our own absorber is already measured positive: +1.69 Ti/round, +7pp, p=0.045** — and #52 exists precisely because **our seal barriers die unattended whenever no builder happens to stand beside them**, while the field pecks our buildings **85.5x/game (19 of 20 opponents non-zero)**.
⇒ **#52 staffed, plus a siting rule that prefers a seal tile inside an enemy gunner's ray, converts our biggest asset from a thing that dies into a thing that eats their ammunition.** ⚠ Dead against the seven teams that do not over-shoot (Memtrace, Team 48, Bisons, gsxWins, Focalground…). ⛔ And **fix the "eight to one" comment first (§4.4)** — the plank's headline is 2x optimistic against the case it names.

### 9.5 EXILE-INTO-JAIL — imprison rather than displace, because killing is a rebate
**Composition logic:** *"Killing is a rebate; imprisoning is not."* Destroying their builder **returns their 20% scale contribution and frees a unit-cap slot**; a body sealed into a 4-barrier cell (12 Ti) keeps **both** liabilities on their books and costs them **~30 Ti and 15 builder-turns** to peck out — the same 10:1 / 15:1 asymmetry that makes the seal work. **With the id-order filter (9.3) the victim is on the tile when the cell closes.**
⛔ **ONE UNVERIFIED BOOLEAN GATES IT:** whether `can_launch` accepts a fully enclosed but passable destination (the tactics note flags it; `is_tile_passable` is about the tile, not its neighbours, so the expected answer is yes). **A second boolean is worth the same probe: `is_tile_empty` returns True on a tile holding a builder — can a 3 Ti barrier therefore be built ON a 30 Ti enemy body?** (`_probe_prison` says no for the *friendly* case and the enemy case is formally untested.) **Both are one local probe game, and the second one, if true, is a 10:1 exchange with no scale rebate.**

### 9.6 RUNNERS-UP, with their honest ceilings
* **Interceptor body-block on the long approach (#63's segment).** A parked body is a wall **no builder can remove** (fact 2) and costs 0 Ti and 0 actions to hold. It composes with #63 because the long-approach maps are where a corridor step is worth the most — and **#63's own finding is that our builders lock at 3.3x theirs on midgard**, i.e. we are currently the ones being intercepted by terrain. ⚠ **Ceiling: true chokepoints are rare — x3r0's chokewall census found the gate off on 12 of 14 maps and +0 rounds of detour on every current-pool seat.** Corridor-width cut first; it is free.
* **Kidnap into our own GUNNER ray, for #45's feeders.** Turret fire hits whatever is on the tile including our own units (a validated replay shows a gunner killing its own builder, 13 hits / 56 damage), and #45 established that **only turret fire and launcher eviction can touch a feeder.** ⚠ **Ceiling: 6 gunner shots (24 ammo) kill a 40 HP body while 96.4% of victims leave within 1 round — so this is chip-and-deny, not a kill, and AIMTHROW's sentinel-ray version already read 50.09-50.55.** The untried cell is the **gunner** ray **with** the id filter.
* **Panic-build inflation** — bait them into a defensive turret build to add **+20% to THEIR scale** (the exact inverse of #60). Listed in `multistep-plans` P-D, never costed. Note it fights the rebate asymmetry: we want them to BUILD, never to LOSE buildings.

### ⭐ THE RANKING — top 5 unexplored, by (mechanism-backed) x (composes with shipped) x (cheap to dose)

| # | idea | mechanism backing | composes with | cost | **probe or arm** |
|---|---|---|---|---|---|
| **1** | **RING DUMP + TWELVE-SEAT CLOSURE** (9.1 + 9.2, one forward launcher, two payloads) | rules-level on both halves: 0 spawns in 2.4M body ring tile-rounds; only a launcher can clear an on-core heal seat; #58's plant live-validated at 3.6x | seat-seal (-10pp, shipped), EXILE (shipped, 351k events), #47/#58 plant code | destination sort + a target-class gate | **PROBE first** (local dose vs `_probe_camper`/`_probe_repairer`), **then a pinned live arm** vs the core-tank class |
| **2** | **ID-ORDER THROW FILTER** (9.3) | 99.64% vs 6.2% dwell (us-only; corrected s51), N=6,177; ids are one global counter, 0 inversions in 26,078 pairs | every throw plank incl. shipped EXILE and the deferred AIMTHROW | **one integer comparison** | **PROBE only** — decodable off `throws.tsv` with no games at all |
| **3** | **AMMO-SINK COLLAR** (9.4) | 5.6:1 barrier bait; 677 shots / 2,708 Ti into one healed 3-Ti conveyor; heal-our-absorber +1.69 Ti/rd p=0.045 | #52 (promoted tonight), seal barriers (shipped), `_heal_adjacent` (shipped) | a stay condition + a siting preference | **PROBE then SCREEN** — self-play is blind by construction (`LOKI_QUIET_ON`), so the value read needs a peck-capable fixture |
| **4** | **EXILE-INTO-JAIL** (9.5) | *killing is a rebate, imprisoning is not*; 10:1 Ti and 15:1 turns to clear a barrier | EXILE (shipped), SALT barrier machinery (shipped), id filter | 12 Ti per cell | **PROBE only** — two booleans in one local game |
| **5** | **INTERCEPTOR ON THE LONG APPROACH** (9.6) | bodies are unkillable by bodies; #63's 3.3x lock ratio; 0 Ti / 0 actions to hold | #63, #54 nav work, raid station picker | a station-scoring term | **PROBE** (free corpus cut for corridor width) **then a small arm** |

**Deliberately NOT ranked, and why** — anything requiring a body **swarm** (§5.2: the 20th builder costs 958 Ti and the immunity theorem gives a proof of futility against a healed core), anything whose only channel is `titanium_collected` (§4.1: we are sink-constrained at a median 7,052 Ti banked), and **another border-crash leg** (§2.1: the band is measured immune; #17's local drive is the only cheap cell left).

---

## §10. TONIGHT'S FOUR ROUTED CANDIDATES — where each lands in this atlas

| candidate | atlas section | honest prior |
|---|---|---|
| **TINY-SWARM** | §5.2, §5.5 | ⛔ **The weakest of the four.** The upstream league nerfed exactly this (builder 10->50->30 Ti + a global cap, *"reduce spam"*), the 20th body costs 958 Ti, the field's own spawn curve **falls** into the kill window, and the immunity theorem gives a proof of futility against a healed core. **If it is built, it must be 6-12 bodies with a named non-melee job (occupy, absorb, block) — never a rush.** |
| **BLOCKER ECONOMICS** | §3.0 | **Strong and already half-answered:** barrier 3 Ti/+1%/30 HP/immobile vs body 30 Ti/+20%/40 HP/mobile; clearing a barrier costs 10:1 in Ti and 15:1 in builder-turns; **a conveyor blocks nothing (40.1% of spawns land on one)** and a body blocks everything except a barrier being built on it. The open cell is **which of the two to spend per tile class**, and §9.2 says the answer is *both, because they reach different tiles*. |
| **BELT-MEDIC DISPATCH (#52)** | §4.4, §9.4 | **Promoted tonight by Magnus** (`85c149d`, 2026-08-14 19:50:53 +0200) on the correct ground that its stated blocker was wrong about the field (**85.5 pecks/game, 19 of 20 opponents**). ⛔ **Two riders: the "8:1" in our own comment is 4:1 against the case it names (§4.4), and `batk`-by-target has not yet shown those pecks land on the barriers this plank heals.** |
| **INTERCEPTOR** | §9.6 | **Mechanically the cleanest idea in the set** (a body is an unkillable wall) **and the most terrain-limited** (gate off on 12 of 14 maps, +0 rounds of detour on every current-pool seat). **Run the free corridor-width cut before writing a prereg.** |

---

## §11. SOURCE INDEX (all paths relative to the repo root)

**Engine reads / probes** — `docs/research/engine-source-crash-and-launcher-2026-08-10.md` · `docs/research/engine-guard-matrix-exploit-hunt-2026-08-10.md` · `docs/research/turret-line-blocking-2026-08-09.md` · `docs/research/post-throw-tile-dwell-2026-08-09.md` · `docs/research/heal-arithmetic-2026-08-09.md` · `docs/research/exchange-rates-2026-08-09.md` · `docs/coordination.md:16350-16440` (`_probe_prison`/`_probe_jail`/`_probe_victim`), `:20220` (`_probe_refund`) · `bots/_probe_*`.
**Censuses / cuts** — `crash-census-2026-08-10.md` · `crash-induction-targeting-2026-08-10.md` · `CRASH-CHANNEL-border-vs-interior-2026-08-12.md` · `SPEC-kidnap-victim-fate-2026-08-11.md` · `loki-arsenal-pricing-2026-08-09.md` · `RING-HAZARD-VERIFICATION-2026-08-11.md` · `HOME-LOCK-MECHANISM-2026-08-14.md` · `denial-book-2026-08-07.md` · `opponent-reaction-atlas-2026-08-09.md` · `SCOUT-field-mechanism-census-2026-08-11.md` · `enemy-launcher-asymmetry-2026-08-09.md` · `exploit-triage-feasibility-2026-08-08.md`.
**Books / profiles** — `BOOK-0033-2026-08-14.md` · `BOOK-bisons-v8-2026-08-14.md` · `BOOK-juusto-2026-08-14.md` · `BOOK-worst-maps-2026-08-14.md` · `OPP-{juusto,lingling40,coreflood,team-lazy,leviathan}-*-2026-08-13.md` · `OPP-SEGMENT-MAP-2026-08-14.md`.
**Legs / preregs** — `PREREG-LEG-EVICT58-2026-08-14.md` (+ the 17:2xZ dose block in `docs/coordination.md`) · `docs/prereg/DOSE-feeder45-2026-08-13.md` · `docs/prereg/DOSE-siegelaunch45-2026-08-13.md` · `docs/prereg/SCREEN-aimthrow-2026-08-14.md` · `CLOSED-BY-LEG-INDEX-2026-08-14.md` · `AUDIT-the-six-refuted-roads-2026-08-10.md` · `SIX-ROADS-STATUS-2026-08-13.md`.
**Cross-league library** — `docs/research/tactics/` (38 body-relevant notes read for this atlas; the load-bearing ones are `minimum-cost-blockading-body`, `the-consumable-blocker-versus-the-permanent-one`, `body-blocking-was-patched-out-elsewhere`, `blind-their-gun-with-their-own-body`, `the-blockade-blanks-your-own-guns`, `score-the-throw-destination`, `throw-into-prebuilt-cell`, `worker-fortified-turret-cell`, `ammo-drain-baiting`, `ore-tile-denial`, `worker-pull-does-not-exist-here`, `retreat-and-return-under-the-counter-unit`) · `mechanic-bans-2026-08-09.md`.
**Live tree** — `bots/_v223sealrepair/{main,eco,raid,doctrine}.py` (v140).

**⚠ INSTRUMENT WARNINGS CARRIED FORWARD:** `tools/ring_retention.py` is retired/wrong (66.4% of its "bodies" are buildings) — use `tools/ring_read.py tile_episodes`. `crash_census` cannot separate a crash from `self_destruct()` and is structurally blind to Juusto's build->throw->demolish recycle. `econ.tsv` v1 was corrupt for v55+-era decodes; the v2 rebuild (40,367 files, 0 decode errors) is the surface for any economic cut. `target_value.py` prices off a cached rating and is stale on exactly the teams worth targeting (#56).
