# CtrlAltDefeat v116 first read — 2026-08-07

**Version tags (rule 2):** target = **CtrlAltDefeat v116** (team id
`74e43df6-bad7-474b-8e37-0ea44a2c80f1`), opponent = **OpenSverige v68
chokewall** (`379a5d80-…`). Match **`27435b40-4b15-40e2-a1a8-8dbfae29b9c9`**,
ladder, created 19:52:43Z, completed **2026-08-07T19:56:59Z**, **CAD 5-0**.
CAD is **team A in all five games**. Elo: CAD 1629.4→1634.0 (+13.2, 845 rated),
us 1567.9→1545.4 (−13.2, 291 rated).

**Decode method:** local archive only, no downloads. Full-timeline decoder
`docs/research/2026-08-07-fanout/toolkit/replay_lib.py` run under
`.venv/bin/python` (3.13). All five replays pass every self-check —
`delivery×10 == titaniumCollected`, `ammo converted − spent == final`, no
unknown top/turn/update/entity fields, no recycled ids, HP in bounds,
**519/369/355/598/430 = 2271/2271 damage events attributed**. Turret counts
deduped by entity id (`placeEntity` re-emits on gunner rotation, per
docs/tooling.md); rotations reported separately. Launcher throws detected as
`moveBuilderBot` with `d²(frm,to) > 1` and attributed to the launcher alive
and adjacent to the pre-throw tile that round. Scratch parsers lived in the
session scratchpad, not the repo.

> **DECODE-METHOD CORRECTION (feeds back into docs/tooling.md):** the tooling
> note says attribute a throw to the launcher *orthogonally* adjacent to the
> pre-throw tile. That is too tight — **launcher pickup includes diagonals**.
> Measured here: CAD's r3/r4 throws in g2/g3/g5 and our own launcher's throws
> in g4/g5 all have the launcher at **d² = 2** (diagonal) from the bot's
> pre-throw tile. Using `d² ≤ 1` returns `NONE` for 6 of the 14 throws in this
> match. Use **`d² ≤ 2`**. With that fix, thrower attribution is unambiguous
> for 14/14 throws here (never more than one candidate launcher in range).

---

## VERDICT BLOCK

### V1 — Loss-mode class: **SAME CLASS as the family read. No new capability.**

CAD v116 beat v68 with exactly the mechanism
`docs/research/kings-college-classification-2026-08-07.md` §4 names:
**launcher-insertion → forward turret battery inside our core ring**, with
counter-turrets killing our forward turrets. Every element of the family
signature is present in **5 of 5 games**:

| Family signature (v107/KCM era) | v116, 5 games |
| --- | --- |
| `convert_ammo(8)` on r0, r1, r2 | **5/5** |
| Launcher built r1 on a core-adjacent tile | **5/5** |
| Launcher **destroyed by its own team at r6** | **5/5** |
| 1–3 of its own builders thrown at r2–r4 | **5/5** (1, 3, 3, 1, 3 throws) |
| 0 splitters | **5/5** |
| Thrown raider plants the first forward turret r3–r5 | 4/5 (g4 is the wide-map exception, first fwd r158) |
| 4th conversion = variable surplus lump | **5/5** (16+104, 172, 186, 16, 101) |
| CAD's own launcher never touches an enemy bot | **5/5** — 12/12 CAD throws move CAD's own builders |

Scoreboard: **4 core-destroyed (g2 r200, g3 r369, g4 r383, g5 r599) + 1
round-1000 titanium tiebreak (g1, 7230 vs 410)**. First blood on our core:
**r4, r4, r4, r159, r14**. **Our core reached 0 in four of five games; CAD's
core was never taken below 410 HP and took 0 damage in three of five.**

The ferry-loop ownership inversion recorded in the pre-mortem's re-check
**holds in the v116 era**: the only two post-r6 throws in the whole match
(g4 r217, g5 r91) are **our** launcher throwing a **CAD** raider away. CAD's
launcher is dead by r6 in every game and is structurally incapable of it. Do
not re-invert this.

### V2 — Opening constants: **the "map-keyed, opponent-independent" asset SURVIVES.**

Two independent tests, both pass.

**(a) Internal consistency (this match, n=5).** All five games are on
*different* maps, so no within-match replication is possible — but the
*structural* constants above reproduce 5/5, and the raider-landing tiles are
deterministic functions of the map (each game's r2–r4 throw destinations are
fixed tiles, not a spread).

**(b) Cross-era, same-map, byte-for-byte.** This is the strong test. Four of
the five v116 maps have an archived **CAD v107** game on the *identical* map
(matched by SHA-1 fingerprint over dims + wall set + ore set + core positions,
not by map name):

| v116 game | map | v107 comparandum | seat | Opening rows compared | Result |
| --- | --- | --- | --- | --- | --- |
| g1 | 14×18, 18 walls | `ad2b9a46` g1 (v107 vs SmartFridge v30) | **same seat A** | launcher tile, both builder-spawn tiles, r2 throw src+dst, first turret round/type/tile | **BYTE-IDENTICAL** |
| g2 | 28×20, 22 walls | `ad2b9a46` g2 (v107 vs SmartFridge v30) | **same seat A** | launcher tile, spawn tiles, **all three** r2/r3/r4 throws src+dst | **BYTE-IDENTICAL** — *except the r3 turret (see D1)* |
| g4 | 24×24, 164 walls | `9d2b38bb` g2 (v107 vs our v68) | mirrored (B) | r2 throw src+dst under 180° rotation | **EXACT under rotation**; launcher tile is the mirror-alternative (7,6) vs (6,7) |
| g5 | 16×16, 50 walls | `b10cce55` g2 (v107 vs Lunds v42) | mirrored (B) | launcher tile, r2/r3/r4 throw **destinations**, first turret type+tile, all under 180° rotation | **EXACT under rotation** (throw *sources* differ; destinations identical) |
| g3 | 28×20, 122 walls | none (CAD never played it) | — | — | KCM v1/v7 rows exist on this map and differ from CAD's — see D2 |

**Opponent-independence is confirmed a second way:** the v107 comparanda on
g1's and g2's maps were played against **Powered by SmartFridge v30**, g5's
against **Lunds Stallions v42** — three different opponents, and CAD produces
the same tiles it produced against us. The property holds across the version
bump.

**Verdict: the map-keyed, opponent-independent opening table is REAL, still
true in v116, and safe to freeze as anti-CAD constants.** The rows that
survive byte-for-byte are the **launcher round + tile, the builder spawn
tiles, and the r2–r4 throw destinations**. The one row that **moved** is the
r3 forward-turret type/tile on one map (D1). Throw *source* tiles (which
builder gets picked up) are **not** stable and must not be frozen.

### V3 — ERA-STABILITY CAVEAT (read before spending anything on this)

**This read is a single-match, n=5 sample of an era that may not survive the
night.** CAD went **v107 → v115 → v116 within roughly one hour** on
2026-08-07 (sibling Lunds v42→v45, KCM 7→1→…). The match decoded here
completed **19:56:59Z**; by the time this is acted on, CAD may be on v117+.
Everything below is stamped **"v116, single-match sample, 2026-08-07
~19:45–19:57Z"** and inherits the standing constants rule: **check their live
version before relying on any row.** The *structural* invariants (r1
launcher / r6 self-destroy / 8-8-8 ammo / r2–r4 own-builder throws) have now
survived v107→v116 unchanged and are the safest thing to build on; the
*per-map tile* rows are the perishable part.

---

## Q1 — Per-game loss modes

Common to all five: CAD's kill mechanism is **turrets planted inside or on the
edge of our core ring, kept alive, firing continuously**. CAD converted
1444 / 1040 / 552 / 1542 / 2174 ammo; we converted **44 / 531 / 522 / 98 /
244** and fired **2 / 102 / 52 / 11 / 22** shots against their **286 / 166 /
129 / 342 / 287**. The C5 finding from the KCM read ("just convert ammo")
reproduces exactly.

### g1 — 14×18, 1000 rounds, **lost on titanium tiebreak 410 vs 7230**

- Opening as the table: launcher (8,7) r1, throw r2 `(8,6)→(6,11)` landing
  **d²=1 from our core footprint**, launcher destroyed r6.
- That raider planted **gunner (7,11) r3** and **sentinel (6,10) r4** — d²=1
  and d²=4 from our core. **First blood r4.** Sentinel #12 survived the entire
  1000 rounds and dealt **900 of the 1299 damage** taken by our core.
- Our core never died: min **360 HP @ r15**, and our heal line put **1299 HP**
  back — an exact offset. We survived 14 CAD forward turrets by healing.
- **We lost on economy.** Our last delivery was **r199**; we finished with 78
  conveyors alive of which **31 wired to core (40%)**, **0 harvesters**, 410 Ti
  delivered. CAD ran **6 conveyors, 6/6 wired, 3 harvesters, 7230 Ti**.
  This is the v68 delivery-freeze defect, not a CAD mechanism.
- We fired **2 shots in 1000 rounds** (44 ammo converted).
- Our three forward turrets (#28 r18, #78 r44, launcher #91 r52) were all
  killed by the **same** CAD gunner #63 at (7,10), built r36.
- CAD's core took **zero damage all game.**

### g2 — 28×20 (22 walls), core destroyed **r200**

- Three throws r2/r3/r4 → `(15,10)`, `(15,11)`, `(11,7)`. The first raider
  planted **sentinel (15,9) on r3** (d²=16 from our core) and **gunner (16,9)
  r5** (d²=9). **First blood r4.**
- Sentinel #10 lived the whole game and dealt **1062 of 1643**; gunner #283
  (17,7), planted r132 at d²=8, added **476**. Nine forward turrets total.
- Our core fell to 404 by r25, was healed back to 500, then collapsed:
  cumulative damage hit 100 by r13, 400 by r115, and the core died r200 at
  minimum-alive 8 HP. 1139 heal delivered and still lost.
- Our three sentinels (#16/#19/#22, r7–r10) sat at d²=82–148 from CAD's core —
  **out of range of anything that mattered** — and fired 14/3/2 shots. Our one
  effective unit was gunner #179 (13,11) r100, 83 shots, answered by a CAD
  counter-gunner at **d²=1** eight rounds later.
- CAD core: **0 damage.**

### g3 — 28×20 (122 walls), core destroyed **r369**

- Three throws r2/r3/r4 → `(15,9)`, `(15,10)`, `(13,14)`; gunner (16,9) r3.
  First blood r4 (28 dmg), then that gunner died r8 and **nothing happened for
  ~300 rounds**.
- **Our economy was zero the whole game: 0 titanium delivered, 0 conveyors, 1
  harvester.** CAD ran 33/33 wired conveyors and 8 harvesters for 1870 Ti.
- The kill is a late stack: CAD planted gunners at **(19,8) r304 d²=1**,
  **(18,8) r348 d²=2**, **(18,9) r355 d²=1**, **(23,9) r359 d²=9**. Cumulative
  core damage: 100 by r315, 500 by r359, dead r369. **65 rounds from first
  serious contact to kill.**
- Our three sentinels (r6/r7/r9) survived the entire game at d²=81–101 from
  CAD's core and fired 10/4/38 shots into nothing. **We never damaged CAD's
  core.**

### g4 — 24×24 (164 walls), core destroyed **r383**

- Wide map, mid-map staging: one throw r2 `(6,6)→(10,10)`, **d²=128 from our
  core** — worthless to deny (pre-mortem K3 reproduces).
- CAD played **economy first**: first turret r56 (home, (6,6)), first *forward*
  turret **r158** (17,19) at d²=1. **First blood r159.**
- Then it stacked: gunners (17,19) r158, (20,19) r166, (20,18) r181, (21,18)
  r301, (20,21) r361 and **sentinel (22,22) r348** — six turrets on our core
  footprint. Damage 100 by r170, 500 by r219, dead r383 despite 1447 heal.
- We did land damage on CAD's core here (104 total, min 410 @r62) — our best
  game of the five, and still not a threat.
- Counter-turret evidence: our sentinel #88 (8,8) r49 → CAD gunner (6,6) r56 at
  d²=8 → dead r62 (**life 13**). Our gunner #126 (2,7) r73 → dead r76
  (**life 3**) to a pre-existing gunner at (2,6). Our gunner #209 (12,16) r115
  → CAD gunner (12,17) r119 at **d²=1** → dead r121 (**life 6**).

### g5 — 16×16 (50 walls), core destroyed **r599**

- Throws r2/r3 both to `(5,7)`, r4 to `(4,0)`. **Sentinel (10,11) r13**, d²=25
  from our core → **first blood r14**.
- We killed that sentinel at r32. **CAD rebuilt a sentinel on the exact same
  tile (10,11) at r382** — and that one dealt **1914 of the 2150** damage that
  killed us. Damage 100 by r24, 200 by r387, 500 by r419, dead r599.
- Note the **builder-bot core attacks**: CAD builders #104 and #395 sitting at
  (13,15)/(13,14) plinked 74 damage into our core directly. Small, but it is a
  mechanism cad_probe does not model.
- Our economy: last delivery **r166**, 62 conveyors alive with **9 wired
  (15%)**, 0 harvesters, 470 Ti vs CAD's 4340 off 17 conveyors (17/17 wired).
- Counter-turret: our sentinel #102 (5,5) r42 was answered by a CAD gunner at
  **(5,4), d²=1, built r41 — one round BEFORE ours** — dead r53 (life 11).

### The one-line predictor still holds

KCM's §3.3 predictor transfers: **count CAD turrets planted within d²≤36 of
our core.** Counts here: **14, 9, 8, 7, 4** — we lost all five. Our own
counter-count inside d²≤36 of *their* core across the whole match: **two**
(g4 #126, g5 #102), both dead within 11 rounds.

---

## Q2 — Opening-constants survival, row by row

Notation: seat A = CAD's seat in this match. Map symmetry verified from the
tile grid, not assumed.

### Rows that survive **byte-for-byte** (same map, same seat, v107 → v116)

**14×18 / 18 walls / cores (6,4)–(6,12) / reflect-horizontal `y→17−y`**
`ad2b9a46` g1 (CAD **v107** vs SmartFridge v30, 17:09:41Z) vs `27435b40` g1
(CAD **v116** vs us, 19:56:59Z):

| Row | v107 | v116 | |
| --- | --- | --- | --- |
| r0 spawn | (8,6) | (8,6) | ✅ |
| r1 spawn | (5,3) | (5,3) | ✅ |
| r1 launcher | (8,7) | (8,7) | ✅ |
| r2 throw | (8,6)→(6,11) | (8,6)→(6,11) | ✅ |
| r3 first turret | gunner (7,11) | gunner (7,11) SW | ✅ |
| launcher destroyed | r6 | r6 | ✅ |
| ammo r0/r1/r2 | 8 / 8 / **32** | 8 / 8 / **8** | ⚠️ see D3 |

**28×20 / 22 walls / cores (7,9)–(19,9) / reflect-vertical `x→27−x`**
`ad2b9a46` g2 (v107) vs `27435b40` g2 (v116):

| Row | v107 | v116 | |
| --- | --- | --- | --- |
| r0 / r1 / r4 spawns | (9,11) / (9,8) / (9,10) | (9,11) / (9,8) / (9,10) | ✅ |
| r1 launcher | (10,11) | (10,11) | ✅ |
| r2 throw | (9,11)→(15,10) | (9,11)→(15,10) | ✅ |
| r3 throw | (9,10)→(15,11) | (9,10)→(15,11) | ✅ |
| r4 throw | (9,10)→(11,7) | (9,10)→(11,7) | ✅ |
| launcher destroyed | r6 | r6 | ✅ |
| ammo r0/r1/r2 | 8 / 8 / 8 | 8 / 8 / 8 | ✅ |
| **r3 first turret** | **gunner (16,10)** | **sentinel (15,9) E** | ❌ **MOVED — D1** |

**16×16 / 50 walls / cores (0,0)–(14,14) / 180° rotation `(x,y)→(15−x,15−y)`**
`b10cce55` g2 (CAD **v107**, seat B, vs Lunds v42, 14:04:48Z) mirrored into
seat A, vs `27435b40` g5 (v116, seat A):

| Row | v107 (mirrored) | v116 | |
| --- | --- | --- | --- |
| r1 launcher | (2,3) | (2,3) | ✅ |
| r2 throw dst | (5,7) | (5,7) | ✅ |
| r3 throw dst | (5,7) | (5,7) | ✅ |
| r4 throw dst | (4,0) | (4,0) | ✅ |
| first turret | sentinel (10,11) **r16** | sentinel (10,11) **r13** | ✅ tile+type, round −3 |
| launcher destroyed | r6 | r6 | ✅ |
| throw *sources* | (2,2) / (1,2) / (2,2) | (2,2) / (2,2) / (1,2) | ❌ not stable |

**24×24 / 164 walls / cores (4,4)–(18,18) / 180° rotation `(x,y)→(23−x,23−y)`**
`9d2b38bb` g2 (CAD **v107**, seat B, vs our v68) mirrored, vs `27435b40` g4:

| Row | v107 (mirrored) | v116 | |
| --- | --- | --- | --- |
| r0 spawn | (6,6) | (6,6) | ✅ |
| r2 throw | (6,6)→(10,10) | (6,6)→(10,10) | ✅ |
| r1 launcher | (6,7) | (7,6) | ⚠️ mirror-alternative, see D4 |
| launcher destroyed | r6 | r6 | ✅ |
| ammo r0/r1/r2 | 8 / 8 / 8 | 8 / 8 / 8 | ✅ |
| first fwd turret | r13 sentinel | r56 home gunner / r158 fwd | ⚠️ **seat effect, not a version delta — D5** |

### Rows that moved / are unstable

- **D1 — the r3 forward-turret row moved on the 28×20/22 map.** Same map, same
  seat, same round, same raider landing tile `(15,10)`: v107 built **gunner
  (16,10)** (east of the raider), v116 built **sentinel (15,9)** (north).
  Different type *and* tile. **UNCERTAIN** whether this is a code change: the
  v107 comparandum is a 43-round loss to a different opponent, so a
  threat-reactive turret choice cannot be excluded. Note that v116 *does* still
  use the east-of-raider gunner on the neighbouring 28×20/122 map (g3, r3
  gunner (16,9) E). **Do not freeze the r3 turret type/tile.**
- **D2 — CAD ≠ KCM on this map family.** On the 28×20/22 map, KCM v1/v7 plant
  the launcher at (9,12) and throw to (14,11)/(14,11)/(12,11); CAD v107 *and*
  v116 both use (10,11) and (15,10)/(15,11)/(11,7). **v116 tracks the CAD
  lineage, not the KCM one** — so the KCM classification's table is a sibling
  table, not a substitute. (On the 14×18 and 16×16 maps the two tables happen
  to coincide exactly.)
- **D3 — ammo r2 is 8 in v116 5/5, but was not perfectly invariant in v107.**
  Across the 25 archived v107 games, `8/8/8` appears **20/25**; exceptions are
  `8/8/32` twice (`ad2b9a46` g1, `b10cce55` g5) and a `48/…` opener three
  times (`cdbd5b52` g3 on 14×18, `cdbd5b52` g5 and `ad2b9a46` g5 on 25×15).
  The **only two v107 games with no launcher at all** are the two `cdbd5b52`
  48-openers — a small-map/no-launcher branch that mirrors KCM's documented
  10×10 `convert_ammo(48)` branch. v116 is 8/8/8 in 5/5 with a launcher in
  5/5, and none of its maps hit that branch. Not enough to call a change.
- **D4 — the launcher tile has two variants on diagonal-core maps.** On 24×24,
  the builder spawns at (6,6) and the launcher goes on **either (7,6) or
  (6,7)** — both orthogonal neighbours, both in range of the same throw
  destination. v116 used (7,6); v107 (mirrored) and KCM v1 used (6,7). Freeze
  the **throw destination**, treat the launcher tile as a 2-way set on these
  maps.
- **D5 — seat, not version, explains the 24×24 slowness.** Family bots in
  **seat A** on that map (KCM v1 `b3656fe7` g1 r26, `9a32a859` g4 r24; CAD v116
  r56) all build their first turret at *home* and go forward at r38–r158;
  family bots in **seat B** (CAD v107 `9d2b38bb` g2, KCM v1 `c821193d` g4) go
  forward at r13–r45. v116's r56/r158 is inside the seat-A envelope. Do not
  read this as a v116 change.

---

## Q3 — STAGED RE-FREEZE TABLE (for `bots/cad_probe`)

> **ERA STAMP: CtrlAltDefeat v116, single-match sample (n=5 games, one
> opponent), match `27435b40-4b15-40e2-a1a8-8dbfae29b9c9`, 2026-08-07
> ~19:45–19:57Z. Decoded by replay_lib from the local archive. Cross-era
> confirmations are tagged with their own match id + version.**
> Maps are keyed by a SHA-1 fingerprint over `WxH | sorted walls | sorted ore
> | core positions` (first 12 hex) — map *names* are not in `.replay26`.

### A. Structural invariants — freeze these (highest confidence)

Confirmed **5/5 in v116** and **23/25 in v107** (the 2 v107 exceptions built no
launcher at all):

```
r0   convert_ammo(8);  core spawns builder #1 on the ring tile toward the enemy
r1   convert_ammo(8);  core spawns builder #2;
     builder #1 builds a LAUNCHER on an orthogonal neighbour of its own tile
     (enemy-facing side), and stands in the pickup ring
r2   convert_ammo(8);  launcher THROWS builder #1 toward the enemy
r3   (if a 2nd/3rd raider exists) further throw(s); first forward turret often
     built this round by raider #1
r4   final throw; then a single VARIABLE SURPLUS conversion
     (v116 observed: 16, 172, 186, 16, 101 — "convert what's left", not a
      fixed 24; KCM's fixed-24 is a KCM-only trait)
r6   the LAUNCHER IS DESTROYED BY ITS OWN TEAM.  5/5.  No exceptions.
     -> CAD's launcher NEVER throws an enemy bot, in any of 30 decoded games.
r5+  raiders walk / plant; 0 splitters ever; economy runs in parallel
```

### B. Per-map opening rows, CAD **seat A** as played (v116)

| # | Map key (`WxH`, walls, ore, cores A–B) | fp | Symmetry | r0/r1 spawns | r1 launcher | Throws r2 / r3 / r4 (dst, d² to our core) | First turret | Cross-era confirmation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | 14×18, 18w, 12ore, (6,4)–(6,12) | `c37217c25b77` | reflect `y→17−y` | (8,6) / (5,3) | **(8,7)** | **(6,11)** d²=1 / — / — | r3 gunner (7,11) SW; r4 sentinel (6,10) S | **CAD v107 `ad2b9a46` g1 — byte-identical**; KCM v1 `02943fbd` g3 identical |
| M2 | 28×20, 22w, 32ore, (7,9)–(19,9) | `7f69d0c8737a` | reflect `x→27−x` | (9,11) / (9,8) | **(10,11)** | **(15,10)** d²=16 / **(15,11)** d²=17 / **(11,7)** d²=68 | r3 sentinel (15,9) E; r5 gunner (16,9) E | **CAD v107 `ad2b9a46` g2 — throws byte-identical; r3 turret MOVED (D1)**. KCM uses a *different* table here (D2) |
| M3 | 28×20, 122w, 28ore, (7,9)–(19,9) | `d9f149435677` | reflect `x→27−x` | (9,10) / (9,9) (+r2 (9,11), r3 (9,10)) | **(10,10)** | **(15,9)** d²=16 / **(15,10)** d²=16 / **(13,14)** d²=52 | r3 gunner (16,9) E | no CAD comparandum; KCM v1 `02943fbd` g5 uses (9,11)/(14,10)/(14,10)/(13,14) — sibling table |
| M4 | 24×24, 164w, 36ore, (4,4)–(18,18) | `c31d24506c87` | 180° `(23−x,23−y)` | (6,6) / (3,3) | **(7,6)** *or* (6,7) — D4 | **(10,10)** d²=128 (mid-map staging) / — / — | r56 gunner (6,6) SE (home); **r158** gunner (17,19) d²=1 | **CAD v107 `9d2b38bb` g2 — throw exact under rotation**; KCM v1 ×2 identical |
| M5 | 16×16, 50w, 14ore, (0,0)–(14,14) | `28aa1260bfce` | 180° `(15−x,15−y)` | (2,2) / (2,1) (+r4 (1,2)) | **(2,3)** | **(5,7)** d²=130 / **(5,7)** d²=130 / **(4,0)** d²=296 | r13 sentinel (10,11) SE, d²=25 | **CAD v107 `b10cce55` g2 — launcher, all 3 throw dsts, first turret tile+type all exact under rotation** |

**Mirrored seat-B rows** (apply the map's symmetry above to every tile). Where
a CAD seat-B observation exists it confirms the mirror: M5 seat B = launcher
(13,12), throws (10,8)/(10,8)/(11,15), first turret sentinel (5,4)
[`b10cce55` g2, CAD v107 — and KCM v7 `4a36151e` g4 identical]. M4 seat B =
launcher (17,16) or (16,17), throw (13,13) [`9d2b38bb` g2 / `c821193d` g4].

### C. Do **not** freeze these

- **Throw source tiles** (which builder is picked up) — varies between v107 and
  v116 on the same map (M5).
- **The r3 forward-turret type/tile** — moved on M2 (D1); UNCERTAIN cause.
- **The 4th ammo conversion amount** — variable surplus, 16–186 in v116.
- **The ferry/long-game throw tile** — pre-mortem K1 stands, and per the
  re-check that loop is *the defender's*, not CAD's. Confirmed again here.

### D. Two cheap `cad_probe` calibration deltas this read supports

1. **The forward turret is kept alive and rebuilt on the same tile.** g5: CAD's
   sentinel at (10,11) is killed r32 and **re-planted on the identical tile at
   r382**, where it does 1914 damage. `cad_probe` plants and replaces raiders;
   a "re-plant the killed turret on its exact old tile" rule is a one-line add
   that reproduces the actual win condition.
2. **Builder-bot core attacks.** g5: CAD builders sitting at (13,15)/(13,14)
   put 74 damage directly into our core. Not currently modelled.

---

## Q4 — Churn signal: what did v107→v116 change?

**Nothing visible in the opening, and nothing statistically separable
elsewhere at n=5.** Across the 25 archived v107 games vs these 5 v116 games,
the per-game means are: gunners 11.2→10.0, sentinels 1.1→1.2, harvesters
4.8→7.4, conveyors 27.8→30.2, splitters 0.0→0.0, builders 11.5→10.6, barriers
1.0→**2.2**, shots 207→242; launcher-at-r1-destroyed-at-r6 23/25 → **5/5**;
ammo `8/8/8` 20/25 → **5/5**. The only candidates are (i) a mild barrier
uptick and (ii) the M2 r3 turret type/tile swap (D1) — both inside the noise
of a 5-game sample against a single opponent, and the v107 comparanda on the
two clean maps were 43- and 71-round losses to a stronger opponent, which
confounds every volume statistic. **Read for the A/B-testing hypothesis: if
the family is A/B-testing against the field, v116 is not testing the opening
— the opening is the shared, frozen asset across CAD v107/v116 and KCM v1/v7,
and the churn is happening somewhere the first 30 rounds do not show.** The
practical consequence is favourable to us: the constants are the *stable*
part of a fast-moving family.

---

## Q5 — Our side (v68 chokewall), brief

**No ancestral pave/launcher crash fired in any of the five games** — 0 TLE
rounds, 0 stdout/diagnostic lines, and **0 units died at full HP** (the
engine-kill / self-destruct signature) on our side in all five games; every
one of our losses is ordinary damage. What *did* cost us is the known
**delivery freeze plus dispatch dead-ends**: last delivery r199 (g1) and r166
(g5) with the game running to r1000/r599, **0 harvesters alive at the end of
g1 and g5**, chain-wiredness of **31/78, 10/24, 0/0, 7/40, 9/62** against
CAD's **6/6, 19/19, 33/33, 32/40, 17/17**, and **zero titanium delivered in
all of g3**. One concrete new dispatch failure worth a ticket: **g4 builder #8
immured itself** — at r163 it built a harvester onto (16,11), its only
non-wall neighbour, and then sat at (16,10) alive at 40/40 HP with **no move
and no action for the remaining 221 rounds**; it never called `destroy()` on
its own harvester to free itself. Everything else on our side (2–102 shots per
game against CAD's 129–342, sentinels parked 82–148 d² from the enemy core
where they can hit nothing, forward turrets living 3–13 rounds) reproduces the
already-documented v67/v68 picture.
