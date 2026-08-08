# CAD PROBE RE-FREEZE SPEC — CtrlAltDefeat v117 (2026-08-08)

**Target:** CtrlAltDefeat **v117** (team `74e43df6-bad7-474b-8e37-0ea44a2c80f1`), the
current stable-ish era. **Instrument under review:** `bots/cad_probe/` (1,449 lines,
frozen against the v107 era). **Deliverable purpose:** enough of a behavioural *and*
execution specification for a builder-arm worker to rebuild the probe as a faithful
current-era sparring instrument — or to decide not to.

**Provenance.** Read-only. 15 archived CtrlAltDefeat matches / **75 games** decoded from
`replay_archive/` with `docs/research/2026-08-07-fanout/toolkit/replay_lib.py` under
`.venv/bin/python`. No games run, nothing downloaded, no bot file touched. Scratch
scripts in `…/scratchpad/cad_spec/{extract,an…}.py` (not committed). CAD's engine seat
is stamped directly from `meta.json` per `docs/research/bo5-seat-assignment-2026-08-08.md`
(meta `teamAName` == engine `TEAM_A`, always; seat fixed for the whole Bo5).

| Era | Matches | Games | CAD seat split | CAD game record |
|---|---:|---:|---|---|
| **v117 (PRIMARY)** | 8 | **40** | A: 3 matches/15 games · B: 5/25 | 22–18 (55.0%) |
| — of which vs our anchors v69–v75 | 6 | **30** | A: 15 · B: 15 | **18–12 (60.0%)** |
| v116 (adjacent) | 2 | 10 | A: 2/10 | 9–1 (90.0%) |
| v107 (probe-source) | 5 | 25 | A: 1/5 · B: 4/20 | 14–11 (56.0%) |

v117 matches: `0803bd92` (vs our v69, 3–2) · `2b05487d` (v72, 3–2) · `c6383349` (v72,
3–2) · `3e8bd0bf` (v72, 3–2) · `8704178a` (v74, 4–1) · `8d0e02c1` (v75 "Eir 8", **2–3**,
08:00Z) · `922be463` (Team 48 v16, 2–3) · `37e6ccf9` (SmartFridge v33, 2–3).

---

## 1. VERDICT

### 1.1 What v117 IS, in one paragraph

CtrlAltDefeat v117 is a **launcher-insertion siege bot with a two-tier turret economy and
a hand-to-mouth ammunition line**. Rounds 0–6 are a frozen, map-and-seat-keyed script:
`convert_ammo(8)` on r0/r1/r2, a launcher built by builder #1 on r1, up to four throws of
its *own* builders on r2–r5 toward a ranked list of tiles near our core, one variable
surplus conversion on r4 (median 172, range 15–256), and the **launcher self-destroyed at
r6 in 35/35 launcher games, age exactly 5, with zero damage events**. From r3 onward the
raiders plant a turret battery whose two tiers do completely different jobs: **~1 sentinel
per game, sited at d²≤32 of our core footprint (43/45 sentinels), which does the killing**
— median 14 shots, 288 damage, 234 of it into our core, and **96% of all CAD sentinels
deal core damage** — and **~11.5 gunners per game whose median core damage is 0** (only
17% ever touch a core) which act as a screen and, critically, as the **counter-turret
layer**: 95.6% of the damage that kills our forward turrets comes from CAD gunners.
Behind that, a real economy (median 5.5 harvesters, 25 conveyors, 2,860 Ti collected, 0
splitters ever) funds a **112-conversions-per-game ammunition trickle** in which 79% of
conversions are ≤12 Ti and 41% exactly equal that round's shot cost — CAD banks almost
nothing and spends **~21% of every game with less than one gunner shot in the bank**.
That trickle is the hinge: **all 18 of CAD's wins against our anchors are `core_destroyed`;
it won 0 of the 9 games that reached r1000**, losing every one on the titanium tiebreak.

### 1.2 What the v107-source probe gets wrong about v117 — RANKED

The single most important framing point: **the probe's largest errors are era-independent.**
`bots/cad_probe/main.py` is not a transcription of v107; it is an independently written
geometric siege bot that shares CAD's silhouette. Bumping its constants to v117 numbers
would not close the gap.

| # | Divergence | Wild v117 (measured) | `cad_probe` (source-cited) | Why it matters |
|---|---|---|---|---|
| **P1** | **No counter-turret. There is no code path in which an enemy entity's position produces a build site.** `_locate` accepts `EntityType.CORE` only (main.py:413–414); every build site is `pos.add(d)` off the acting builder (696/788/832/1018/1090); every score references `self.enemy` (the core) or `self.home`. | **100%** of our turrets planted within d²≤36 of CAD's core get a CAD turret planted within d²≤13 (n=80, 80/80); median latency **15.5 r**; **76% killed**, median lifespan **16.5 r**; at d²≤13 it is **84% killed / median life 8 r**. Beyond d²≤36 CAD does essentially nothing (11–19% killed, median life 237–377 r). | none | This is the CAD-analogue of ouro-v2's D1. It is the *reason* our forward turrets do not stay up on the ladder, and the probe teaches the opposite lesson. |
| **P2** | **Turret mix and plant order inverted.** `_plant_turret` (766–821) iterates `(SENTINEL, GUNNER)` in that fixed order — sentinel always first, gunner only as fallback (784/808–809). | **gunner : sentinel = 11.5 : 1 per game.** Sentinels are the core-killers (96% deal core damage, med 234); gunners are the screen (17% deal any, med 0). | sentinel-first | Wrong shape end to end: a probe that leads with sentinels presents an instrument our bots learn to answer with the wrong counter. |
| **P3** | **No home / own-side turret layer.** `_forward_work` is the only planting path and returns early unless `self.delivered` **and** `core_dist_sq(pos, enemy) <= PLANT_BAND_SQ(45)` (723–726). No home turret, no home barrier, no reaction to being attacked (no `get_hp(self)` call exists). | **66% of CAD's turrets (312/486) are nearer its own core than ours**; median **4 gunners/game at d²>36 of our core**. Home-band turrets: n=367, median life 71 r, median 4 shots. | none | Removes CAD's entire defensive picket. A probe with no home layer is trivially raidable — the opposite of the wild matchup. |
| **P4** | **Monotone production caps; nothing is ever rebuilt.** `SLOT_TURRETS`/`SLOT_BARRIERS`/`SLOT_HARVESTERS` only increment (735/742/1032), so a killed turret permanently consumes budget against `TURRET_TARGET = 11`. No `destroy()`, no rebuild path anywhere. | CAD **re-plants on the exact tile of a dead own turret 281 times over 40 games (25/40 games)**; near-core tile re-plants 63; one tile re-used **13 times** in `2b05487d` g4 (independently recorded in v72-bleed L5). Turret plants/100 r do not decay to zero: 8.0 (r0–50) → 4.0 (50–100) → 4.17 (100–200) → 2.9 (200–400) → 1.48 (400+). | hard ceiling of 11, never replenished | The probe's late game empties out; the wild's does not. Seven of nine v72-era CAD losses had their top killer planted after r130, two after r400. |
| **P5** | **Ammunition shape inverted — the probe never starves.** `_convert` (505–529): three flat `convert_ammo(10)` in the opening, then top-up to `AMMO_CEILING = 70` out of every surplus, every round. | **8/8/8** then one surplus lump on r4 (median 172; observed 15–256), then a trickle: **112 conversion events/game, 79% ≤12 Ti, 41% exactly equal to that round's shot cost**; balance median 8–25 Ti mid-game, **94 rounds/game (21%) with ammo < 4 while a turret is alive**. | never starves; holds a 70 bank | This is the invariant that makes CAD *lose long games*. A probe that never starves is systematically too strong late and too weak early — i.e. it fails to present the exact regime our tiebreak line has to beat. |
| **P6** | **Launcher lifecycle wrong.** Probe builds the launcher from a builder and **never destroys it** (`grep destroy` returns only the docstring); it keeps throwing every raider that queues, unbounded. | launcher born **r1**, dead **r6**, **damage events 0**, in 35/35 launcher games. Throws only on r2/r3/r4/r5, ≤4 per game, **0 cross-team throws in 40/40 games**. | permanent ferry | The permanent launcher is a mechanism CAD does not have and our bots would learn to exploit or fear wrongly. |
| **P7** | **No opening table.** Probe's only hardcoded table is `CORE_PAIRS` (223–240), which yields only the enemy core position; launcher tile, throw target and first turret are all derived geometrically. | opening r0–r5 is **byte-stable within (map, seat) in 10/14 v117 buckets with ≥2 games**, and byte-stable across **v107 → v116 → v117** on every paired bucket checked. | geometric | The opening is the single most reproducible thing about CAD, and the probe reproduces none of it. |
| **P8** | **No builder attacks.** Probe's builders never call the attack action. | CAD builders attack **30×/game** and deal **1,746 damage into our harvesters + 881 into our conveyors** (vs only 174 into our core). This is an economy-denial line. | none | Our economy-under-pressure behaviour is never exercised by the probe. |
| **P9** | **Upkeep is un-modulated.** Probe heals behind a flat 6-Ti (raider) / 40-Ti (home) floor. | CAD heals **4.3 actions/100 r when quiet, 20.0/100 r under siege** (core damaged in the last 10 rounds) — a **4.7× siege response**. Heal HP lands mostly on its own **core (2,605)** and **builders (1,621)**. | flat floor | |
| **P10** | **No small-map branch.** | On **10×10 maps CAD builds no launcher** (4 of 5 v117 10×10 games) and instead plants gunners straight off the core ring at r1–r3 with an `8/8/24/44/…` ladder. **CAD is 0–5 on 10×10.** | none | A cheap, real, exploitable branch the probe cannot present. |

### 1.3 Era-delta verdict, and BUILD vs KEEP

**The era-delta v107 → v117 is real and roughly a doubling of mid-game scale — but it is
the smaller of the two gaps.** On the 14 map+seat buckets present in both eras (22 v107 vs
24 v117 games), the opening is unchanged and everything after r10 is 1.4×–4.3× bigger
(§2). Meanwhile the probe-vs-CAD gap (§1.2) contains four mechanisms CAD has had in
*both* eras and the probe has in neither.

**Recommendation: BUILD — but do not call it an era re-freeze, and do not scope it as
one.** Naming it "v107 → v117" misdiagnoses the work: a constants bump (gunner count,
conveyor count, plant rate) would leave P1/P2/P3/P4 untouched and would not move the
predictive gap. The build to commission is a **re-spec around four execution-layer
mechanisms** — counter-turret (P1), two-tier turret economy (P2/P3), replant-and-persist
production (P4), and the starving ammunition trickle (P5) — with the v117 opening table
(P7) as cheap, high-confidence scaffolding on top.

**The evidence that "keep with era caveats" is not available:** the frozen probe already
fails the predictive gate defined in §6. Our v73–v75 line scores **60.0 – 66.7%** against
`cad_probe` (`results.tsv`: `_v85hs-gate` cad 66.7/66.7; `_v85hsb-bar` cad 61.7 v 60.0;
`_v86m1-acceptance` cad 61.7/63.3) against a **wild 40.0% [Wilson 24.6, 57.7]** — the
probe scores sit *above the upper bound of the wild interval*. Behavioural-fidelity-only
acceptance is refuted by the ouro-v2 gap decomposition and would be refuted here too:
the probe already reproduces CAD's *establishment count* (C1b gate: "cad_probe est
~7/game"; wild v117 forward turrets median 8) and is still 20–27 points too easy.

**Scoping honesty.** CAD-family is our #2 Elo bleed (−88.0 net, 17.4% stake,
`elo-weighted-battery-2026-08-08.md`). If the builder arm cannot fund the full re-spec,
the highest-value single plank is **P1 (counter-turret)** — it is the mechanism that makes
our home-ring and forward-turret work testable at all, and it is measurable in isolation
by acceptance item E1 (§6.3).

---

## 2. ERA-DELTA TABLE v107 → v116 → v117

Medians. The **PAIRED** columns are restricted to the 14 (map fingerprint, CAD seat)
buckets that occur in both the v107 and v117 corpora — this controls for map mix, which
otherwise dominates every volume statistic. v116 is shown unpaired (n=10, one opponent,
favourable maps) and should be read as a texture, not a level.

| Item | v107 paired (22 g) | v116 (10 g) | v117 paired (24 g) | v117 anchors (30 g) | Delta |
|---|---:|---:|---:|---:|---|
| Game length (rounds) | 343 | 307.5 | 468 | 408.5 | +36% |
| **OPENING** | | | | | |
| `convert_ammo` r0/r1/r2 = 8/8/8 | 80% | 100% | — | 90% | **unchanged** |
| Launcher born r1 / dead r6 / 0 dmg events | 23/25 | 10/10 | — | **35/35 of launcher games** | **unchanged** |
| Throws per game (own builders only) | 3 | 3 | 3 | 3 | unchanged |
| Throws at r5 (4th throw) | 1/23 games | 1/10 | — | **12/40** | **new-ish** |
| Cross-team throws (CAD throwing *our* bot) | 0 | 0 | 0 | **0/40** | unchanged |
| r4 surplus lump | present | 16–186 | — | median 172, range 15–256 | grew |
| Splitters, ever | 0 | 0 | 0 | **0** | unchanged |
| **TEMPO** | | | | | |
| First forward turret (d²≤36 of our core) | **r10** | r3 | **r3** | r3 | **−7 rounds** |
| First blood on our core | **r11** | r9 | **r5** | r4 | **−6 rounds** |
| **TURRETS** | | | | | |
| Gunners built | 8 | 9.5 | **14** | 11.5 | +40–75% |
| Sentinels built | 1 | 1 | 1.5 | 1 | ~ |
| Forward turrets (d²≤36) | 5.5 | 7.5 | 7 | 8 | +27% |
| Gunner rotations | 3 | 17.5 | **7** | 7 | ×2.3 |
| Shots fired | 142 | 183.5 | **267.5** | 204.5 | +88% |
| Turret re-plants on an exact dead-turret tile | 0.5 | 0 | 1 | 2 | ~ |
| Turrets nearer OWN core than ours | 62% | 35% | **66%** | 64% | unchanged |
| **ECONOMY** | | | | | |
| Harvesters built | 2.5 | 8.5 | **5.5** | 5.5 | ×2.2 |
| Conveyors built | 6 | 36 | **26** | 25 | **×4.3** |
| Barriers built | 0 | 2.5 | **1.5** | 0 | new, small |
| Ti collected | 2,785 | 3,185 | 3,385 | 2,860 | +22% |
| **BUILDERS / UPKEEP** | | | | | |
| Builders spawned | 9.5 | 9.5 | **15.5** | 13.5 | +63% |
| Builders lost | 3.5 | 3 | 2.5 | 4.5 | ~ |
| Builder heal actions | 38 | 36.5 | **57.5** | 34 | +51% |
| Builder attack actions | 14 | 64 | **30** | 30 | ×2.1 |
| **AMMO** | | | | | |
| Conversion events | 84 | 102.5 | **148** | 102 | +76% |
| Ti converted | 862.5 | 1,123 | **1,341** | 1,203 | +56% |
| Share of conversions ≤12 Ti | 78% | 76% | — | **79%** | unchanged |
| Rounds ammo-starved (<4 with a turret alive) | 35.5 | 17 | **72.5** | 94 | ×2 |
| **OUTCOME** | | | | | |
| Damage into our core | 530.5 | 1,068.5 | **1,232** | 885.5 | ×2.3 |
| Damage into CAD's core | 271 | 0 | 267 | 180.5 | ~ |

**Subsystems added between v107 and v117:** none that is structurally new. Barriers appear
(median 0–1.5) and the 4th throw at r5 becomes common. **Subsystems removed:** none.
**The v107 → v117 change is a scale-up, not a redesign** — the same machine, run roughly
twice as hard, arriving on our doorstep 7 rounds earlier.

---

## 3. BEHAVIOURAL SPEC (v117)

Every conditional clause carries an **[AUDIT]** tag. Each tagged clause becomes its own
line in the builder's code audit — this is the ouro-v2 lesson: the dropped "except…" that
the audit never itemised cost 40 points of win rate.

### 3.1 Opening — rounds 0 to 6

```
r0   convert_ammo(8)                                          [AUDIT: exactly 8, not 10]
     core spawns builder #1 on the ring tile toward the enemy
r1   convert_ammo(8)
     core spawns builder #2
     builder #1 builds a LAUNCHER on an orthogonal neighbour of its own tile,
       enemy-facing, and stands in the pickup ring
r2   convert_ammo(8)
     launcher throws builder #1 toward the enemy
r3   throw #2 (if a second raider is in the pickup ring); first forward turret
       is usually planted this round by raider #1
r4   throw #3; then ONE variable surplus conversion (median 172, range 15-256)
r5   throw #4 in 12/40 games                                  [AUDIT: only if a raider queued]
r6   the launcher is DESTROYED BY ITS OWN TEAM, age exactly 5, 0 damage events
```

- **[AUDIT] Only CAD's own builders are ever thrown.** 0 cross-team throws in 40/40 v117
  games (and 0 in 25/25 v107 games). The long-game repeat-throw "ferry loop" belongs to
  the *defender*, not CAD — already established in `cad-ferry-premortem-2026-08-07.md`
  §Re-check, reconfirmed here.
- **[AUDIT] The launcher is destroyed unconditionally at r6**, whether or not raiders
  remain queued. It has no post-r6 behaviour of any kind.
- **[AUDIT] Small-map branch: on 10×10 maps CAD builds NO launcher.** 4 of the 5 v117
  10×10 games (`0803bd92` g5, `2b05487d` g2, `3e8bd0bf` g2, `37e6ccf9` g5) and one 25×15
  game (`922be463` g1) skip the launcher entirely and plant gunners/sentinels directly off
  the core ring from r1, on an `8/8/24/44/8/48`-style conversion ladder. **CAD is 0–5 in
  no-launcher games.** The one 10×10 game that *did* build a launcher (`8d0e02c1` g1) was
  also lost. Reproduce the branch; it is a real, cheap weakness.

### 3.2 Per-map opening rows — stability, and what NOT to freeze

Maps keyed by SHA-1 over `WxH | sorted walls | sorted ore | core positions` (first 12 hex);
map names are not in `.replay26`. Of the 14 v117 (map, seat) buckets with ≥2 games,
**10 have a single byte-identical opening signature** (converts, spawn tiles, launcher
tile, throw rounds+destinations). The 4 unstable buckets each have a named cause:

| Bucket | Games | Cause of instability |
|---|---|---|
| `111babdf65ea` seat A (10×10) | 2 | launcher vs no-launcher branch fired differently |
| `22444bc0bd08` seat B (25×15) | 2 | launcher vs no-launcher branch |
| `f84ee6e4ec7d` seat B (14×18) | 2 | r2 throw destination (8,5) vs (6,6) — both at d²=1 of our core |
| `94a66ad202f2` seat A (21×8) | 3 | r2 throw destination varies across all three games |

**FREEZE these rows** (byte-stable within bucket, and stable across v107→v116→v117 on
every paired bucket checked): the **builder spawn tiles**, the **launcher tile**, the
**launcher's r1 build / r6 destruction**, the **conversion ladder 8/8/8**, and the
**set of throw destinations**.

**DO NOT FREEZE:** throw *source* tiles (which builder gets picked up — varies); the
r3 forward-turret **type and tile** (see 3.3); the r4 surplus amount.

**Throw-destination mechanism — RESOLVED [AUDIT].** `v72-bleed-cad-family` §Q3 left this
as UNCERTAIN ("*a plausible explanation is that the target must be bot-passable and one of
our own builders occupied the preferred tile — not verified*"). **Verified here.** On the
21×8 seat-A bucket the preferred r2 destination is `(12,5)`:

| Game | `(12,5)` at r2 | CAD's r2 throw | CAD's r3 throw |
|---|---|---|---|
| `3e8bd0bf` g3 (vs v72) | EMPTY | **(12,5)** | (11,3) |
| `8704178a` g2 (vs v74) | **our builder standing on it** | (11,3) | (11,4) |
| `8d0e02c1` g2 (vs v75) | **our builder standing on it** | (11,3) | **(12,5)** — taken once free |

So CAD carries a **ranked list of destination tiles and skips any that is not passable**,
taking the next one; it re-acquires the preferred tile on a later throw once it clears.
**This also answers the ferry pre-mortem's K2 open question ("does a barrier deny or
displace?") from the archive alone: it DISPLACES.** A barrier on a throw tile buys one
tile of displacement, not a denial. K2 no longer requires an instrumented unrated
challenge.

### 3.3 Turret siting and type selection — the two-tier rule

Composition per game (v117 anchors, medians): **1 sentinel at d²≤32 of our core · 3.5
gunners at d²≤13 of our core · 4 gunners at d²>36 (home/mid picket)**.

| Band (d² to OUR core footprint) | n | gunner | sentinel | sentinel share | median core dmg | median life |
|---|---:|---:|---:|---:|---:|---:|
| ≤13 | 131 | 114 | 17 | 13% | **70** | 33 |
| 13 < d² ≤ 32 | 129 | 103 | 26 | 20% | 0 | 39 |
| 32 < d² ≤ 36 | 20 | 20 | 0 | 0% | 0 | 109.5 |
| 36 < d² ≤ 100 | 145 | 145 | 0 | 0% | 0 | 138 |
| > 100 | 61 | 59 | 2 | 3% | 0 | 225 |

- **[AUDIT] Every sentinel is built where its ray reaches our core: 43 of 45 CAD sentinels
  sit at d²≤32 of our core footprint.** Two exceptions in 30 games.
- **[AUDIT] Gunners that matter sit at d²≤13; gunners outside that band never damage the
  core.** 114 of 123 forward gunners are at d²≤13; median core damage for gunners overall
  is **0**, and only **17%** of gunners ever deal any core damage at all.
- **Type-selection rule, CORRECTED.** `v72-bleed-cad-family` L6 states the first forward
  turret is a gunner when the *landing tile* is d²≤13 of our core and a sentinel when
  13<d²≤32, at 14/15. **REFUTED at n=27 on the full v117 corpus: 8/13 (62%) where the
  rule applies.** All five misses are d²=16 landings that produced a **gunner at d²=9** —
  the raider walked one tile closer before planting. The correct statement is a *site*
  rule, not a *landing* rule, and it is exactly what a `can_fire_from` gate produces:
  > **[AUDIT] Plant the turret whose ray actually reaches a core footprint tile from the
  > site the raider is standing next to: gunner if the site is d²≤13 with clear
  > line-of-fire, otherwise sentinel if the site is d²≤32 (ignores obstacles).** This is
  > also why heavy-wall maps produce sentinels at short range (`2b05487d` g5, sentinel at
  > d²=5) — a gunner's ray would be blocked there.

### 3.4 Targeting priorities

CAD turret damage by target kind (v117 anchors, 58,056 points total):

| target | share |
|---|---:|
| core | **53.4%** |
| builder_bot | 21.2% |
| conveyor | 18.0% |
| sentinel | 3.1% |
| gunner | 1.9% |
| harvester / launcher / barrier | 2.4% |

- **[AUDIT] Core first, always** — but note the *composition*: the core share is carried by
  sentinels (47% of core damage from ~1 sentinel/game) while gunners spend their fire on
  builders and conveyors.
- **Top-3-shooter share of core damage = 0.98 (median, n=28 games with core damage).** The
  kill is 1–3 turrets, not a barrage.
- Builder attacks are an **economy-denial line, not core plinking** [AUDIT]: 1,746 damage
  into our harvesters and 881 into our conveyors, against only 174 into our core. This
  re-ranks the v116 read's calibration note D2 ("builder-bot core attacks, 74 damage,
  small") — the mechanism is real but it is aimed at our *economy*.

### 3.5 Retreat, rebuild, persistence

- **[AUDIT] No retreat exists.** Raiders do not flee, do not read own HP, and do not
  disengage; they die where they stand (4.5 builders lost/game).
- **[AUDIT] Killed turrets are re-planted on the exact tile.** 281 same-tile re-plants over
  40 games, 25/40 games; near-core re-plants 63; max re-uses of a single near-core tile in
  one game = **13** (`2b05487d` g4, confirming v72-bleed L5). Median gap 119 rounds — this
  is a *persistent* loop, not an immediate rebuild.
- **[AUDIT] Economy is rebuilt too, but weakly**: median 1.5 harvester/conveyor rebuilds on
  a dead tile per game, 17/30 games.
- **[AUDIT] Arming must persist to r1000.** CAD's top killer is planted after r130 in 7 of
  9 v72-era losses and after r400 in 2 — turret plants/100 r never fall below 1.48.

### 3.6 Seat conditionality

**No material seat-conditional behaviour detected.** CAD's per-seat records against our
anchors are identical (9–6 on seat A, 9–6 on seat B; our win rate 40.0% on both). Opening
rows mirror cleanly under each map's symmetry. Per-seat execution medians (v117, all 40):
seat A — 12 gunners / 19 conveyors / first fwd r3 / 86 starved rounds; seat B — 10 / 26 /
r3 / 82. The residual differences are confounded with map and opponent mix at these n.
**The acceptance battery is still specified as both-seats** (§6) — not because CAD is
seat-sensitive, but because the *probe* may be: ouro-v2 passed pooled and failed seat B
26.7% / 3.3%.

---

## 4. EXECUTION SPEC — the layer behaviour tables under-constrain

These four items are first-class spec requirements with wild reference numbers, and each
maps to an acceptance item in §6.3.

### 4.1 Production parallelism

CAD runs **3–4 concurrent building streams**, not a queue of one.

| measure | wild v117 (anchors, n=30) |
|---|---|
| Max distinct builders placing a building inside a 10-round window | **median 3** (distribution: 1×1, 2×4, **3×15**, 4×8, 5×1, 6×1) |
| Same, 20-round window | median 3.5 (2×4, 3×11, 4×8, 5×6, 6×1) |
| Builders alive at r25 / 50 / 100 / 200 / 400 | 4 / 4 / 4 / 6 / 7.5 |
| Builders spawned over the game | 13.5 (lost 4.5) |
| Spawn rounds, builders #1–#6 | r0, r1, r4, r5, **r56**, r120 |
| Rounds with ≥2 CAD builders acting | 17.5 (of 106.5 rounds with any builder action) |

**Plants per 100 rounds by phase** (all buildings / turrets only / economy only):

| phase | all | turret | economy |
|---|---:|---:|---:|
| r0–50 | **27.0** | **8.0** | 18.0 |
| r50–100 | 14.0 | 4.0 | 10.0 |
| r100–200 | 16.5 | **4.17** | 9.5 |
| r200–400 | 6.0 | **2.9** | 0.0 |
| r400+ | 1.67 | **1.48** | 0.0 |

**[AUDIT] The economy stops at ~r200 and the turret line does not.** Economy plants fall to
**0.00/100 r** from r200 onward while turrets hold 2.9 then 1.48. A probe that ties turret
production to a global counter or a single builder index will fail this profile the way
ouro-v2 did (1.5/100 r against a wild 7.5). **The frozen `cad_probe` has no serialized
index** (verified: no `idx`, no `target == idx` gate; the plant gates at main.py:733–734 /
739–740 / 1013 are pure count caps, read-modify-write and racy, allowing 3 raiders + 4 home
builders to act concurrently) — so P4's ceiling, not serialization, is the probe's
production defect. That is a genuinely different failure from ouro-v2's and must be
audited as such.

### 4.2 Counter-turret behaviour — CAD's answer to our standoff turrets

**This is the mechanism the behaviour tables miss and it is the most load-bearing item in
the spec.**

| Our turret's band (d² to CAD core) | n | killed | median life | got a CAD turret at d²≤13 | median latency | median shots it got off |
|---|---:|---:|---:|---:|---:|---:|
| ≤13 | 45 | **84%** | **8 r** | **100%** | 24 r | 4 |
| ≤36 | 35 | 66% | 29 r | **100%** | 8.5 r | 11 |
| ≤64 | 16 | 19% | **377 r** | 69% | 58 r | 5 |
| ≤100 | 15 | 13% | 264 r | 80% | 151.5 r | 19 |
| >100 | 37 | 11% | 237 r | 89% | 110.5 r | 10 |

Restricted to our **forward** turrets (d²≤36 of CAD's core): **n=80, 76% killed, median
lifespan 16.5 rounds, 80/80 got a CAD turret planted within d²≤13**, median latency
**15.5 rounds**. Sentinels specifically: at d²≤36, **76% killed, median life 27 rounds**.

**Who does the killing.** Of the 2,576 damage points delivered into our forward turrets:
**gunner 2,464 (95.6%)**, sentinel 54, builder attack 58. The answer is a **gunner
counter-plant**, in 75 of 76 measured pairs.

**Quality of the answer [AUDIT].** Of the 76 counter-plants: **34% are aimed at our turret
at plant time**, and **32% ever deliver damage to it themselves**. The rest are pressure
from an adjacent tile that our turret's own defenders have to answer. CAD's counter is
*sited* precisely (100% coverage at d²≤13) but only *aimed* a third of the time — the
probe must reproduce both halves; over-aiming would make the instrument harsher than the
wild, which is its own calibration failure.

**[AUDIT] The counter is DISTANCE-GATED and does not extend past d²≈36 of CAD's own core.**
Our turrets beyond that band survive (11–19% killed, median life 237–377 rounds) and the
"counter" hits recorded there are incidental (median latency 110–151 rounds). A probe that
chases every enemy turret across the map is *wrong* and will over-punish standoff play.

### 4.3 Upkeep under siege

| measure | wild v117 (anchors) |
|---|---|
| Builder heal actions per 100 rounds, **quiet** | **4.27** |
| Builder heal actions per 100 rounds, **under siege** (own core damaged in the last 10 rounds) | **19.99** — a **4.7× response** |
| Heal actions per game | 34 (our line: 214 — we out-heal CAD ~6×) |
| First heal round | r29.5 |
| Heal HP by target | core **2,605** · builder_bot 1,621 · gunner 686 · conveyor 322 · harvester 168 |
| Own harvesters lost / conveyors lost per game | 0 / 2 |

**[AUDIT] The siege response is conditional on own-core damage, not on building damage in
general** — heal HP into gunners/conveyors/harvesters is a fifth of what goes into the core
and builders.

### 4.4 Ammunition economy — the trickle, and the starvation that loses long games

| measure | wild v117 (anchors) |
|---|---|
| Ti converted per game | **1,203** (opponent-side, ours: comparable) |
| Conversion **events** per game | **102** |
| Share of conversions ≤12 Ti | **79%** |
| Most common conversion amounts | 4 (n=1,116), 10 (659), 8 (534), 20 (251), 12 (187) — i.e. one gunner shot, one sentinel shot, the opening 8 |
| Conversions exactly equal to that round's shot cost | **41%** (1,434 / 3,460) |
| Conversions ≥ that round's shot cost, when a shot happened | **84%** |
| Ammo balance at r25 / 50 / 100 / 200 / 400 | 75 / 9.5 / 8 / 25 / 0.5 |
| **Rounds ammo-starved** (<4 Ti of ammo with a turret alive) | **94/game = 21.2% of rounds** |
| Titanium *balance* held at r25 / 100 / 400 | 21.5 / 71 / 205 |

**[AUDIT] CAD converts on demand, not on a ceiling.** The r4 surplus lump (median 172) is
the one exception; after that it converts roughly one shot's worth at a time. It runs
itself dry.

**Why this is a first-class spec item.** The starvation is the *mediator* of CAD's
win/loss split:

| | CAD WIN (n=18) | CAD LOSS (n=12) |
|---|---:|---:|
| rounds ammo-starved | **41.5** | **358.5** |
| conveyors built | 37.5 | 10.5 |
| harvesters built | 8.5 | 3.5 |
| our Ti collected | 1,630 | **11,330** |
| damage into our core | 1,355.5 | 461.5 |
| game length | 297 | **1000** |
| win condition | 18/18 `core_destroyed` | 9/12 `titanium_collected` |

**CAD won 0 of the 9 anchor games that reached r1000.** A probe that banks ammo and never
starves converts CAD's losing regime into a winning one and hands our tiebreak line an
easy pass it will not get on the ladder.

---

## 5. DEFECTS TO PRESERVE

The probe must reproduce these; they are where our wins come from and a "cleaned-up" probe
would delete our own measured counter-play.

| # | Defect | Evidence | [AUDIT] clause |
|---|---|---|---|
| **D1** | **No answer to a turret outside d²≈36 of its own core.** | Our turrets at 36<d²≤64: 19% killed, median life 377 r. At d²>100: 11% killed, 237 r. | [AUDIT] The counter-plant search must be **gated on the enemy turret being within ~d²36 of CAD's own core**, and must do nothing outside it. |
| **D2** | **Ammunition starvation, 21% of rounds.** | 94 starved rounds/game median; 358.5 in losses. | [AUDIT] Conversion must be demand-driven and must **not** hold a bank; no ceiling top-up. |
| **D3** | **Economy plants stop dead at r200.** | economy plants/100 r: 9.5 (r100–200) → **0.00** (r200–400) → **0.00** (r400+). | [AUDIT] Economy building must **cease** past ~r200 even when titanium is available. |
| **D4** | **Loses every 10×10 game (0–5), and skips the launcher there.** | 4/5 v117 10×10 games have no launcher; all 5 lost. | [AUDIT] Small-map branch fires **only** on the smallest maps; do not generalise it. |
| **D5** | **Launcher never touches an enemy bot** — no defensive ferry, no disposal of our raiders. | 0 cross-team throws in 40/40 v117 and 25/25 v107 games. | [AUDIT] `can_launch` must be attempted **only** on own-team builders. |
| **D6** | **Counter-plants are only aimed 34% of the time.** | 26/76 aimed at plant; 24/76 ever deal damage themselves. | [AUDIT] Do **not** add a directed rotate-to-reacquire; CAD's rotation rate is 7/game, not per-threat. |
| **D7** | **Gunners are near-useless offensively.** | median core damage 0; only 17% of gunners ever deal any core damage. | [AUDIT] Gunner siting must be governed by the same range gate CAD uses, not by a "get close to the core" objective. |
| **D8** | **Builders die forward and are not replaced quickly.** | 4.5 builders lost/game; the 5th builder spawns at median **r56**, the 6th at r120. | [AUDIT] Core spawn must **not** backfill losses on demand. |
| **D9** | **No home barriers, essentially no barriers at all.** | 0 barriers median in anchors, 1.5 in the paired v117 set. | |
| **D10** | **Zero splitters, ever.** | 0 in 75/75 games across all three eras. | |

---

## 6. ACCEPTANCE GATE

### 6.1 The wild reference number

**Our anchor binaries won 12 of 30 games against CtrlAltDefeat v117 on the ladder:
40.0%, Wilson-95 [24.6, 57.7].** Match level: **1 of 6 = 17%** (reproducing the
Elo-battery's 15.4% CAD-family match rate at n=13). Seat-symmetric: 6/15 = 40.0% on each
of CAD's two seats.

| anchor | on disk | games | our wins | rate | Wilson-95 | CAD seat |
|---|---|---:|---:|---:|---|---|
| v69 | `bots/opp_v69` | 5 | 2 | 40.0% | [11.8, 76.9] | B |
| v72 | `bots/opp_v72` | **15** | 6 | 40.0% | [19.8, 64.3] | A + B |
| v74 | `bots/opp_v74` | 5 | 1 | 20.0% | [3.6, 62.4] | A |
| v75 "Eir 8" | `bots/_v85hsd` | 5 | 3 | 60.0% | [23.1, 88.2] | A |
| **pooled** | | **30** | **12** | **40.0%** | **[24.6, 57.7]** | 15 / 15 |

`bots/_v84g` (v73) has no archived CAD v117 pairing — include it in the battery for
continuity with prior legs, but it carries no wild reference and **must not be used to
adjudicate the gate**.

### 6.2 The predictive gate (primary — behavioural fidelity alone is NOT acceptance)

> **G1 — CONTAINMENT.** Run `bots/opp_v69`, `bots/opp_v72`, `bots/opp_v74` and
> `bots/_v85hsd` against the rebuilt probe, **both seats, ≥60 games per anchor** (≥240
> games pooled), matched noise settings. The **pooled anchor win rate's Wilson-95 interval
> must contain 40.0%**, and its point estimate must fall in **[30.0, 50.0]**.
>
> **G2 — NO SEAT COLLAPSE.** Neither seat's pooled rate may fall outside **[20, 60]**.
> (ouro-v2 passed pooled and split 26.7 / 3.3 by seat; that failure mode is specifically
> being gated against.)
>
> **G3 — WIN-CONDITION SHAPE.** Of the probe's own wins, **≥80% must be `core_destroyed`**
> (wild: 18/18 = 100%), and the probe must win **≤15%** of games that reach r1000 (wild:
> **0 of 9**). A probe that wins tiebreaks is not CAD.

**The frozen `cad_probe` fails G1 today.** Our v73–v75 line scores 60.0–66.7% against it
(`results.tsv`: `_v85hs-gate` 66.7; `_v85hsb-bar` 61.7 vs baseline 60.0; `_v86m1-acceptance`
61.7/63.3) — **60.0 and 66.7 both sit above the wild upper bound of 57.7.** This is
recorded as a pre-registered refutation, not a post-hoc one: the gate is defined from the
ladder data, not from the probe's score.

**Stated confounds.** (i) The wild reference is 30 ladder games across 15 map draws with
one seat per match; the probe battery is a local deterministic arena with chosen seats and
seeds — map mix and seed amplification differ, so containment is the right test and a
point-estimate match is not required. (ii) The v74 and v75 rows are n=5 each and their
intervals span most of the range; the gate is deliberately specified on the **pooled**
rate. (iii) Anchors are snapshots; the ladder games were played against those versions
live, so anchor drift is possible but bounded — the anchors' own opening traces in the
archive are the check.

### 6.3 Execution acceptance items (the ouro-v3 adaptation)

These are measured **off the rebuilt probe's own replays**, and each is a hard gate. They
exist because ouro-v2 achieved behavioural fidelity on every table and still lost 61
points to two unspecified execution mechanisms.

> **E1 — COUNTER-TURRET (the CAD analogue of ouro's D1).** Of the anchors' gunners and
> sentinels planted within **d²≤36 of the probe's core**: **≥70% killed** (wild 76%),
> **median lifespan ≤30 rounds** (wild 16.5), and **≥90% must have a probe *gunner*
> planted within d²≤13 of them within 40 rounds** (wild 100% at median latency 15.5 r).
> **Ceiling clause [AUDIT]:** anchors' turrets at **d²>64 of the probe's core must survive
> at ≥70%** with **median lifespan ≥200 rounds** (wild: 19%/13%/11% killed, 237–377 r).
> Over-answering fails this item as surely as under-answering.
>
> **E2 — PRODUCTION PARALLELISM AND PERSISTENCE (the CAD analogue of ouro's D2).** Turret
> plants per 100 rounds must hit **≥6.5 (r0–50), ≥3.5 (r50–100), ≥3.5 (r100–200), ≥2.2
> (r200–400), ≥1.0 (r400+)** (wild 8.0 / 4.0 / 4.17 / 2.9 / 1.48, allowing ~−20%). At
> least **3 distinct builders must place a building inside one 10-round window in ≥50% of
> games** (wild median 3, ≥3 in 25/30 games). **Persistence clause [AUDIT]:** in games
> reaching r400, **≥1 turret must be planted on the exact tile of a previously destroyed
> own turret** (wild: 281 re-plants over 40 games, 25/40 games).
>
> **E3 — AMMUNITION TRICKLE AND STARVATION (CAD-specific; no ouro analogue).** ≥**80**
> conversion events per game with **≥70% of them ≤12 Ti** (wild 102 events, 79%), and
> **≥15% of rounds ammo-starved** — ammo < 4 with a turret alive (wild 21.2%, median 94
> rounds). **A probe that never starves fails E3 even if it passes G1**, because it would
> be passing for the wrong reason: it would be trading CAD's real late-game collapse for
> artificial late-game strength.

### 6.4 Behavioural spot-checks (necessary, not sufficient)

Cheap, deterministic, and all measurable in the first 10 rounds of one replay per map:

| # | Check | Wild target |
|---|---|---|
| B1 | Conversion ladder r0/r1/r2 | 8 / 8 / 8 (35/40 games) |
| B2 | Launcher born r1, destroyed by own team r6, 0 damage events | 35/35 launcher games |
| B3 | Throws: ≤4, on r2–r5, own builders only | 0 cross-team throws in 40/40 |
| B4 | Opening signature byte-stable within (map, seat) | 10/14 buckets |
| B5 | First forward turret round | median r3 |
| B6 | Gunner : sentinel ratio per game | 11.5 : 1 |
| B7 | Sentinels sited at d²≤32 of enemy core | 43/45 = 96% |
| B8 | Sentinel share of enemy-core damage | 47% from ~1 sentinel/game |
| B9 | Top-3-shooter share of enemy-core damage | 0.98 median |
| B10 | Splitters built | 0, ever |
| B11 | Economy: harvesters / conveyors built | 5.5 / 25 |
| B12 | Builder attacks per game, targeted at economy | 30/game; 1,746 dmg to harvesters, 881 to conveyors, 174 to core |
| B13 | Siege heal response | 20.0 heals/100 r under siege vs 4.27 quiet |
| B14 | 10×10 no-launcher branch | fires on 4/5 10×10 games |

---

## 7. SELF-CHECKS

**Parsing validation.**

| check | result |
|---|---|
| Games parsed | **75/75** (40 v117 + 10 v116 + 25 v107); all five replays present for all 15 matches |
| `replay_lib.check_all()` failures | **0 across all 75 games** |
| `delivery × 10 == titaniumCollected` | pass, 75/75 |
| `ammo converted − spent == final engine ammo` | pass, 75/75 |
| Unknown top/turn/update/entity fields | 0 |
| Recycled entity ids | 0 |
| HP within bounds; winner consistent with dead cores | pass, 75/75 |
| Damage events attributed | **33,618 / 33,618 (100%)** |
| CAD seat stamped from `meta.json` | 75/75; corroborated behaviourally by the opening trace on every paired map+seat bucket |
| Launcher-throw attribution | `moveBuilderBot` with d²(frm,to) > 1, thrower = launcher alive at **d²≤2** (the diagonal-pickup correction from the v116 read), unambiguous on all throws |
| Turret counts deduped by entity id | rotations routed to `entity_updates`, never counted as builds (v117 rotations: median 7/game) |
| Games excluded | **none** |

**Claims contradicted or revised, counted explicitly — 5 contradicted, 3 confirmed, 2 retired.**

*CONTRADICTED / REVISED:*
1. **`v72-bleed-cad-family` L6** — "the first forward turret is a gunner when the raider's
   *landing tile* is d²≤13 of our core and a sentinel when 13<d²≤32, 14/15."
   **REFUTED at n=27** (8/13 = 62% where the rule applies). All five misses are d²=16
   landings that produced a gunner at d²=9. **Replaced by the site rule (§3.3).**
2. **`cad-v116-first-read` V2** — "the map-keyed, opponent-independent opening table is
   REAL … and safe to freeze as anti-CAD constants." **PARTIALLY REVISED**: byte-stable
   within (map, seat) in **10/14** v117 buckets; throw destinations are conditional on
   tile passability (§3.2) and the launcher/no-launcher split is map-size conditional. The
   launcher tile, spawn tiles and conversion ladder survive as frozen rows; throw
   destinations survive only as a *ranked set*.
3. **`cad-v116-first-read` D1** — "the r3 forward-turret row moved on M2; **UNCERTAIN**
   whether this is a code change." **Cause identified** as a line-of-fire site rule, not a
   version change or a threat reaction (§3.3). `v72-bleed`'s "freeze it" reading is
   likewise superseded — the *rule* is stable, the *tile* is not.
4. **`cad-v116-first-read` calibration delta 2** — "builder-bot core attacks … small, but a
   mechanism cad_probe does not model." **RE-RANKED**: builder attacks are 10× larger
   against our *economy* (1,746 + 881) than against our core (174). The under-modelled
   mechanism is economy denial, not core plinking.
5. **`elo-weighted-battery` §5** — "cad_probe … over-confident by 46.3 pts (61.7% probe vs
   15.4% wild)." **CONFIRMED but re-expressed on comparable units**: game-level the gap is
   **20–27 points** (60.0–66.7% probe vs 40.0% [24.6, 57.7] wild); the 46.3-point framing
   compares a game rate against a *match* rate. Both framings put the probe outside the
   wild interval; the game-level one is the gateable statistic.

*CONFIRMED:*
6. **`v72-bleed` L5 re-plants** — CAD v117 re-uses tiles. Confirmed on 40 games: 281
   same-tile re-plants, 25/40 games, 1.52 near-core plants/100 r (v72-bleed measured 1.72
   on 15 games).
7. **`cad-ferry-premortem` re-check** — CAD's launcher never throws an enemy bot.
   Confirmed 0/40 in v117 (and 0/25 in v107).
8. **`cad-v116-first-read` D3 small-map branch** — "not enough to call a change."
   **Confirmed and localised**: it is a **10×10** branch in v117 (4/5 games), plus one
   25×15 instance, and CAD is 0–5 in it.

*RETIRED:*
9. **`cad-ferry-premortem` K2** — "deny-vs-displace is untestable without an instrumented
   unrated challenge." **RESOLVED from the archive: it DISPLACES.** CAD skips a
   non-passable destination and takes the next tile in its ranked list, re-acquiring the
   preferred tile on a later throw once free (§3.2, 3 games, direct occupancy evidence).
   The pre-mortem's PARK verdict is unaffected — displacement is worth ~nothing — but the
   open question is closed.
10. **"CAD wins by turret mass inside our core ring."** Retired as a *mass* claim. The
    kill is **1 sentinel** (median 234 core damage, 96% of sentinels deal core damage) plus
    a screen of gunners whose median core damage is **0**. Top-3-shooter share 0.98.

**Per-claim n, for every load-bearing number.**

| claim | n |
|---|---|
| Wild rate 40.0% [24.6, 57.7] | 30 games, 6 matches, both seats |
| Launcher r1→r6, 0 damage | 35 launcher games (of 40) |
| 0 cross-team throws | 40 games |
| Counter-turret 100% coverage / 15.5 r latency | 80 of our forward turrets |
| Our forward-turret survival 76% killed / 16.5 r | 80 turrets |
| Standoff survival at d²>64 | 68 turrets (16 + 15 + 37) |
| Counter-plant aimed 34% / damages 32% | 76 pairs |
| Gunner : sentinel 11.5 : 1 | 486 turrets, 30 games |
| Sentinels at d²≤32 of enemy core: 43/45 | 45 sentinels |
| Ammo trickle 102 events, 79% ≤12 Ti | 3,460 conversion rounds, 30 games |
| Ammo-starved 21.2% of rounds | 30 games |
| Plants/100 r by phase | 30 games |
| Concurrency median 3 in a 10-round window | 30 games |
| Siege heal 20.0 vs quiet 4.27 per 100 r | 30 games |
| Re-plants 281 / 25 of 40 games | 40 games |
| Era-delta (paired) | 14 buckets, 22 v107 vs 24 v117 games |
| Opening stability 10/14 | 14 buckets with ≥2 v117 games |
| Type-selection rule 8/13 | 27 first-forward-turret observations, 13 in-range |
| Throw displacement | 3 games, one bucket — **smallest n in this document; flagged** |
| 10×10 branch 0–5 | 5 games |

**Stated limitations.** (i) The v117 corpus is 8 matches over ~11 hours on 2026-08-07/08;
the family moves versions fast (v107→v115→v116→v117 with a brief v117→v107 rollback at
~09:14 local that reverted within ~10 minutes). **Check CAD's live version before
commissioning.** (ii) Three of the eight v117 matches are against non-OpenSverige
opponents (Team 48 v16, SmartFridge v33), included for behavioural rows and excluded from
the wild rate. (iii) Per-map v117 cells are n=1–3 and are shown for shape, never for
significance. (iv) The throw-displacement mechanism rests on one map bucket; it is
consistent with `can_launch`'s passability requirement but a second bucket would harden
it. (v) v116 numbers come from two matches against one opponent on favourable maps and are
not a reliable era level — the era-delta is drawn on the paired v107/v117 comparison.

---

## 8. THE FOUR NUMBERS

1. **Wild 40.0% [24.6, 57.7] vs probe 60.0–66.7%.** Our anchors beat CtrlAltDefeat v117 in
   12 of 30 ladder games and 1 of 6 matches; they beat `cad_probe` in 60–67% of arena
   games. The instrument is 20–27 points too easy and already fails the §6.2 gate.
2. **Counter-turret: 100% coverage, 15.5-round latency, 76% killed, 16.5-round lifespan**
   for our turrets inside d²≤36 of CAD's core — against **zero** such code path in the
   probe. Beyond d²≤64 CAD does nothing (11–19% killed, 237–377 rounds). The gate is
   two-sided.
3. **11.5 gunners : 1 sentinel, and the sentinel does the killing** — 96% of CAD sentinels
   deal core damage (median 234); only 17% of gunners deal any (median 0). The probe plants
   sentinel-first.
4. **94 ammo-starved rounds per game (21%), 358.5 in the games CAD loses, and CAD has won
   0 of 9 games that reached r1000.** The probe holds a 70-ammo bank and never starves —
   it cannot present the regime that decides half of this matchup.
