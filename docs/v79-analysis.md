# v79_lsq_eco+tall_park (x3r0) vs v55 "v70-medic-surge" — mechanism analysis

Read-only analysis, 2026-08-07. Sources: `bots/opp_v56/main.py` (v79, 2034 lines),
`bots/_v70cm/main.py` (v55, 2559 lines), diff = 1572 lines
(`SCRATCH/v55_v79.diff`). Replays: `SCRATCH/replays/v79/v79_{atoll,heart,jackpot,meander}.replay26`
(A = v55, B = v79, all four B wins).

Both files fork from the same ancestor. **Byte-identical in both**: `_link_path`,
`_build_next_link`, `_step_off_link`, `_pick`, `_bfs_direction`, `_nav`, `_move`,
`_launcher`, `_launchwait`, `_offer_launch`, `_home_defend` (bar one inserted call),
`_rank2_hold`, `_try_siege_build`, `_note_friendly_launcher`, `_sync_harvesters`,
`_try_build_launcher`, the whole map/terrain decoder. Every divergence is in
**economy/ammo policy, population, defensive reflexes, map-keyed denial, and
target-priority tables**. Navigation and pathing are not in play at all.

## Map identification (decoded from the shared MAP_CODES table)

Wall counts decoded from `MAP_ALPHABET`/`MAP_CODES`, cross-checked against the
wall-density census in v55's `MELEE_FIRST_MAX_WALL_FRAC` comment (exact match):

| map | dims | area | anchors | walls | wall% |
| --- | --- | --- | --- | --- | --- |
| fjordgate | 10x10 | 100 | (2,2)/(6,6) | 10 | 10.0 |
| moonrise | 21x8 | 168 | (5,3)/(14,3) | 24 | 14.3 |
| antler | 14x18 | 252 | (6,4)/(6,12) | 18 | 7.1 |
| jackpot | 16x16 | 256 | (0,0)/(14,14) | 50 | 19.5 |
| lighthouse | 16x16 | 256 | (3,3)/(11,11) | 63 | 24.6 |
| atoll | 18x18 | 324 | (2,14)/(14,2) | 18 | 5.6 |
| **meander** | **25x15** | **375** | **(11,3)/(11,10)** | 8 | 2.1 |
| nordkap | 20x26 | 520 | (9,6)/(9,18) | 73 | 14.0 |
| eider | 28x20 | 560 | (7,9)/(19,9) | 22 | 3.9 |
| **heart** | **28x20** | **560** | **(7,9)/(19,9)** | **122** | **21.8** |
| drumlin | 25x25 | 625 | (5,5)/(18,18) | 4 | 0.6 |
| hive | 25x25 | 625 | (2,20)/(21,3) | 34 | 5.4 |
| saga | 24x24 | 576 | (4,4)/(18,18) | 164 | 28.5 |
| snowflake | 26x26 | 676 | (5,5)/(19,19) | 70 | 10.4 |
| archipelago | 26x26 | 676 | (5,5)/(19,19) | 207 | 30.6 |

x3r0 never names a map. Every special case is an **area/aspect/anchor predicate**,
so translating one requires this table. eider and heart share dims *and* anchors; he
discriminates them with `sum(row.count("#")) >< 80` (heart 122, eider 22).

**meander's cores are 7 tiles apart (anchor dsq = 49).** The Core's UNDER sensor is
`turret within dsq<=64`, so on meander both teams are effectively **permanently
UNDER from the first forward gun onward**. That single fact drives most of the
meander divergence below.

---

# 1. MECHANISM INVENTORY

## 1a. The two named levers (the v78 → v79 overnight promote)

Both are one-line predicate widenings; **neither touches any of the four swept maps.**

**`lsq_eco_under`** — `_plan_siege`, v79 L825-828:
```python
_wide = 500 <= self.mw * self.mh <= 560 and self.mw > self.mh      # eider + heart
_lsq  = 600 <= self.mw * self.mh < 650  and self.mw == self.mh      # drumlin + hive
eco_need = 1 if (area <= 120 or ((_wide or _lsq) and read_store(SLOT_UNDER))) else ECO_NEED
if self.forward_guns >= 1 and read_store(SLOT_HARVESTERS) < eco_need: return False
```
v55 L1522-equivalent is the unconditional `< ECO_NEED` (3). Effect: on 25x25
(drumlin/hive) **while UNDER**, the siege engineer may plant its 2nd/3rd forward gun
after **one** harvester instead of three. `_wide` (eider/heart) was already there in
v78 — the new lever is only the `_lsq` disjunct.

**`tall_park_under`** — `_saboteur`, v79 L1024-1026:
```python
elif self.forward_guns >= 1 and read_store(SLOT_HARVESTERS) < (
        1 if (area <= 120 or (500 <= area <= 560 and self.mw < self.mh and read_store(SLOT_UNDER)))
        else ECO_NEED):
    self.tgt = p          # park in place instead of advancing on the enemy Core
```
"park" = the `self.tgt = p` branch. On **nordkap** (20x26, the only `w<h` map in the
500-560 band) while UNDER, the saboteur stops parking at 1 harvester instead of 3 and
walks on the enemy Core sooner. Note the asymmetry: this site carries the *tall*
disjunct, `_plan_siege` carries the *wide/lsq* disjunct — a tuner artifact, not a
principle.

So the docstring lever is a **hive/drumlin + nordkap** patch. It is aimed squarely at
maps **we** sweep or split. It is not the explanation for atoll/heart/jackpot/meander.

## 1b. v79 mechanisms our line does NOT have

| # | Mechanism | Where | Gate / constants | Pool maps affected |
| --- | --- | --- | --- | --- |
| **V1** | **Step off an ore tile on wall-dense maps** | `_expand`, v79 L1438-1454 | `sum(walls) >= 80` ∧ standing on `ORE_TITANIUM` ∧ no building on it ∧ move cooldown 0 → step to a cardinal non-ore, non-wall tile | **heart(122), saga(164), archipelago(207)** |
| **V2** | **Counterbattery has no economy gate** | `_try_counterbattery`, v79 L1056 | v55 has `if HOME_GUN>=1 and HARVESTERS<ECO_NEED: return False` (v55 L1522); **v79 deleted it** | all — decisive on close-anchor maps (**meander**, moonrise) |
| **V3** | **melee-first unconditional** | `_saboteur`, v79 L977 | v79: always `_sabotage_prio` before siege repair. v55 gates on `melee_first` = walls < 1.5% ⇒ **drumlin/hive-B only**; every other map is repair-first | all 4 swept maps |
| **V4** | **BARRIER promoted in both target tables** | `_sabotage_prio` v79 L767-770; `_turret` v79 L1874-1888 | builder melee: `GUNNER/SENTINEL 0, BARRIER 1, CORE 2, HARVESTER 3, ...`; turret fire: `..., BARRIER 4, LAUNCHER 5, HARVESTER 6, CONVEYOR 7`. v55 ranks BARRIER **last (5 / 7)** | all — matters most where the enemy walls in (jackpot corner) |
| **V5** | **Rush-tile denial (hardcoded bunker tiles)** | `_rush_deny_tiles` L1121-1149, `_try_rush_deny` L1151, `_defend` L1193-1260 | 7 (dims, anchor) entries: nordkap-B(9,18), moonrise-A(5,3), moonrise-B(14,3), **jackpot-A(0,0)**, **jackpot-B(14,14)**, **meander-A(11,3)**, heart/eider-B(19,9). Melee an enemy building on the tile → else build a Barrier on it → else heal our Barrier there. Plus a `bunker_station` the defender parks on. | jackpot, meander, heart/eider, nordkap, moonrise |
| **V6** | **`always_bunker`** | `_defend` L1198-1201 | meander-A(11,3) and heart/eider-B(19,9) run the bunker from round 0; all others wait for UNDER | meander, heart |
| **V7** | **`_deny_threat_tile`** | L1040-1054, called from `_home_defend` L724 and `_defend` L1279 | UNDER ∧ cooldown 0 ∧ orthogonally adjacent to `SLOT_THREAT` → fire on it. Cheap, map-agnostic | all |
| **V8** | **Scaled threat sensing (`gun_sense`/`b_sense`)** | `_builder` L499-511 | area>=650 square → 100/36; `_midsq_far` (256-band square, anchor sum >= (w+h)//2) or `_tiny_near` → 81/25; else 64/16 (= v55 fixed) | **jackpot-B, lighthouse-B**, fjordgate-A, snowflake, archipelago |
| **V9** | **UNDER latch decays after 50 rounds, not 35** | `_core` L334 | `rnd - SLOT_ATK_RND < 50` (v55: `< 35`) | all |
| **V10** | **Ammo magazine scales with home guns** | `_core` L358-359 | `if weapons: ammo_target = max(ammo_target, min(48, 4*weapons))`; plus `32 if under` (v55: `24 if under`) | all |
| **V11** | **Tiny-arena Ti floor protects the opening harvester** | `_core` L362-363 | `if harv < 1 and area <= 120: ti_floor = max(ti_floor, harvester_cost + 4)` | fjordgate |
| **V12** | **Early role-2/role-3 → saboteur flips** | `_builder` L560-598 | 5 extra map-keyed flips on top of the shared "role_3 at 4 harvesters/r12": tiny(1 harv, r6); **256-square (2 harv, r8)**; 252-nonsquare/antler (2 harv, r8); nordkap-B (2 harv, r10); eider-B (1 harv, r8, walls<80) | fjordgate, **jackpot**, lighthouse, antler, nordkap, eider |
| **V13** | **`keep_artillery_forward` widened** | `_builder` L658-666 | adds `tiny_arena`, `square_band` (**jackpot/lighthouse**), `large_square` (drumlin/hive/snowflake/archipelago) to v55's list; plus a release valve on the 252 band when UNDER ∧ no home gun | jackpot, lighthouse, drumlin, hive, snowflake, archipelago, fjordgate |
| **V14** | **`sq25_freeze`** | `_expand` L1365-1370 | generalises `hive_freeze` to any 25x25 (drumlin too) at `HOME_GUN>=2 ∧ r>=42`: expanders stop entirely | drumlin, hive |
| **V15** | **Melee/heal-under-fire branches in `_expand`** | `_expand` L1376-1417 | area>600, or tiny-arena near/far anchor bands, within core dsq<=36 → smash an adjacent enemy turret; then `UNDER ∧ HOME_GUN>=1 ∧ area>120 ∧ dsq<=16` → heal core | large maps mostly |
| **V16** | **First siege gun is a Gunner on tiny arenas** | `_plan_siege` L839-843 | `not tiny_arena` added to the PRIMARY_SENTINEL test — 20 Ti gunner instead of 30 Ti sentinel | fjordgate |
| **V17** | **First builder spawns on the enemy-facing edge** | `_core` L383-388 | v55 deleted this as a dead branch ("**activating it measured 41%**"). In v79 it is *also* dead: `SLOT_ENEMY_CORE` is written and read in the same round-0 Core turn and store writes are buffered, so `ec` is always the unpack of 0 | none (dead) |
| **V18** | Role assignment: `role_n >= 4` → **defend** | `_builder` L465 | v55: `n==4` defend, `n>=5` expand. Moot in v79 — see below, it never spawns a 6th builder | none in practice |

## 1c. Our mechanisms v79 does NOT have

| # | Mechanism | Where (v55) | Notes |
| --- | --- | --- | --- |
| **O1** | **Builder respawn-on-death** | `_core` L625-655, consts L27-55 | `REPLACEMENT_MAX=8, REPLACE_TI_FLOOR=250, REPLACE_MIN_RND=60`. **v79 has none of this: `self.n` is a lifetime counter and `spawn_cap` is 5, so v79 spawns exactly 5 builders per match, ever.** A dead v79 builder is never replaced. |
| **O2** | **Late labor surge** | `_core` L639-642, `_eco_cap` L1330 | `SURGE_TI_FLOOR=1500, SURGE_MIN_RND=300, SURGE_EXTRA=5, SURGE_ECO_CAP=24`. v79's harvester ceiling is a hard `ECO_CAP=18`. |
| **O3** | **Universal adjacent heal** | `_builder` L954-957 | Any builder of any role, adjacent to the Core, under UNDER, heals it *before* any melee/sabotage branch. **v79 has no equivalent** — it has three narrow, gated heal sites instead (`_expand` L1409-1417 needs `HOME_GUN>=1 ∧ area>120 ∧ dsq<=16`; `_defend` after sabotage/deny/counterbattery; `_home_defend` fourth in its chain). |
| **O4** | **Multi-healer convergence** | `_expand` L1846-1872 | role_n 2 and >=5 walk home when `UNDER ∧ _core_shelled`; proximity-bounded by builder vision r²=20. |
| **O5** | **`_core_shelled` + heal-beats-sabotage ordering** | L1349-1368, `_defend` L1613-1631 | Direct observation off the Core's HP bar, not the loose proximity flag. v79 orders `_sabotage_prio → _deny_threat_tile → _try_counterbattery → _heal_core`; **we put the heal first when the Core is provably losing HP.** |
| **O6** | **Turret-hunting under siege** | `_hunt_turret` L1370-1512 | `HUNT_DESIGNATE_DSQ=8, HUNT_MIN_HEALERS=2, HUNT_FINISH_HP=8, HUNT_MIN_RND=120`, id-ballot with `HUNT_DEFER_BASE/SPREAD` deadlock breaker. v79's `_deny_threat_tile` is a 15-line stub of this: single tile, must already be adjacent, no walk-in, no ballot, no healer floor. |
| **O7** | **Saboteur interception** | `_intercept` L1963, `_find_intruder` L1897, `_guard_target` L1942, `_heal_adjacent` L1922 | `INTRUDER_CORE_DSQ=20, INTRUDER_FORGET_RNDS=8`; role_n==1 chases enemy builders working in our half beyond the Core recall radius. **No v79 equivalent at all.** |
| **O8** | **Chain medic** | `_expand` L1789-1811 | `MEDIC_TI_FLOOR=20, MEDIC_MIN_RND=150, MEDIC_TYPES=(CONVEYOR, SPLITTER, HARVESTER)`. Heal-in-passing on damaged economy buildings — the anti-relay-churn fix (+1% team-wide scale per rebuilt conveyor). |
| **O9** | **Defend-role succession** | `_builder` L821-841, `SLOT_DEFEND_BEAT` (slot 13) | role_n==2 promotes to defend when the heartbeat goes stale >6 rounds after r10. |
| **O10** | **Defender comes home** | `_defend` L1676-1687 | `shelled ∧ role_n==4` → walk to the Core, outranking threat-chase and link-finishing. |
| **O11** | **`melee_first` map gate** | L71, `_builder` L765-769 | Deliberately *narrows* v79's V3 to wall-free maps. Not an absence — a measured restriction. |
| **O12** | **Counterbattery economy gate** | `_try_counterbattery` L1522 | Deliberately *added*; v79 lacks it (V2). Same shape as O11 — our line trades early turrets for economy. |
| **O13** | **Launch give-up / stall bounds** | `LAUNCH_GIVEUP_RND=180`, `LAUNCH_STALL_RNDS=36` | v79 uses a bare `rnd >= 180`, no stall bound. |
| **O14** | **`_try_build_launcher` call site restored** | `_defend` L1650-1653 | v79 never calls `_try_build_launcher` from `_defend`; its launcher subsystem is effectively dormant unless a launcher already exists. **This is a live bug in v79, not a design choice** — `_launchwait`, `_offer_launch`, `SLOT_DROPPED` and the whole insertion machinery are dead weight in his file. |

## 1d. Store-slot map (collision check)

Slots 0-12, 14, 15 are **identical in both files**. The only difference is slot 13:
v55 `SLOT_DEFEND_BEAT` (live), v79 `SLOT_HOME_SENT` — **declared and never read or
written anywhere in v79**. There is **no store collision** between the two files. A
merge in either direction is store-safe.

---

# 2. PER-SWEEP CAUSE (replays)

Replay method notes: `placeEntity` is re-emitted on `rotate()`, so raw gunner build
counts overstate badly (heart B 34 raw = 6 builds + 28 rotations; meander B 102 raw =
7 + 95). All counts below are deduped by entity id. Team 0 = A = v55 verified on all
four (jackpot `removeEntity` on core id=1, team=0, pos=(0,0) at r189; `winner=1`).

## 2.0 The three cross-map causes that dwarf everything else

These show up on **all four** maps and are not per-map at all. Two of the three are
**our own mechanisms misfiring**, not his mechanisms working.

### C1 — The repair-escort stalemate (our `_intercept` → `_guard_target` →
`_heal_adjacent`, v55 L1922-2018). **This is the single largest line item.**

| map | tile | what it is | B attacks | A heals | A Ti burnt |
| --- | --- | --- | --- | --- | --- |
| atoll | (4,10) | A's own **sentinel** | 819 (r181→999) | 819 | 819 |
| heart | (10,8) | A's own **3-Ti conveyor** | 717 (r263→999) | 708 | 708 |
| meander | (9,11) | A's own **3-Ti conveyor**, 1 tile from B's gunner | 453 gunner shots (r547→999) | 905 | 905 |

The docstring's claim is correct and irrelevant: "parked between the raider and what
it is chipping, the interceptor out-repairs it two-to-one on HP and eight-to-one on
titanium, so the harvester never dies." It does. What it also does is **remove one
builder's entire action budget for 450-820 consecutive rounds**, and A's total heal
spend runs **1223 / 1086 / 1147 Ti** per map ≈ 20% of A's whole match income. `_intercept`
has **no stalemate disengage** — it releases only when the intruder dies, leaves our
half, or goes unseen for `INTRUDER_FORGET_RNDS=8`. A raider that never leaves is a
permanent lock. B triggers it for 2 Ti/round with one builder, or **free** with a gunner
it was building anyway.

The meander case additionally **refutes the chain medic's premise on turret fire**:
`MEDIC_*` was sized against builder melee (2 dmg/rd < 4 HP/rd heal). A gunner is
7 dmg on reload 1 ≈ 3.5/rd sustained, and *two* gunners or a sentinel outrun the heal
outright. A held a conveyor at (9,11) — **inside the enemy gunner's kill zone, 50 dsq
from its own core** — alive for 453 rounds at 905 Ti and it never delivered anything.

### C2 — Harvesters built but never wired. `_link_path`/`_build_next_link` are
**byte-identical** in both files, so this is not a pathing difference — it is a
labour-allocation difference.

| | atoll | heart | jackpot | meander |
| --- | --- | --- | --- | --- |
| A harvesters alive @r1000 | 5 | 5 | 3 (@r189) | **7** |
| A **directed-connected** | **2** | **2** | 2 | **1** |
| B harvesters / connected | 2 / **2** | 9 / **7** | 3 / 2 | 5 / **3** |
| A delivery rate r300-999 | **5.00 Ti/rd** | **5.00** | — | **7.50** |
| B delivery rate | 5.00 | **15.00** | — | **12.50** |

**A's delivery is pinned at exactly two harvesters' throughput for 700 rounds on atoll
and heart while owning five.** heart's #389 (10,19) and #844 (5,15) never shipped a
single stack. A laid *more* conveyors than B on heart (48 built vs 52, 40 alive vs 36)
and **18 of A's 40 surviving relays connect to nothing.**

Mechanism: A spawns **17-18 builders on every long map** (5 base + `REPLACEMENT_MAX=8`
+ `SURGE_EXTRA=5` — the cap is saturated) against B's **exactly 5, at r0-r4, never
again**. Extra hands + `SURGE_ECO_CAP=24` produce extra *harvester starts*, then those
hands get claimed by heal/escort/converge reflexes before the link queue finishes.
**On atoll, A's 12 builders deliver 5.00 Ti/rd; B's 4 builders deliver 5.00 Ti/rd.**
The late labor surge produced zero throughput in all four games and cost
**+340-360% builder-bot cost scale** (and meander **+201% conveyor scale** off 201
conveyor builds with 86 deaths — same three tiles rebuilt 27/14/7 times).

### C3 — Ammo starvation with a full bank. **This is the cheapest fix on the list.**

| | atoll | heart | meander |
| --- | --- | --- | --- |
| A ammo balance, flat for 700+ rd | **16** | 24 | 24 |
| A Ti converted, whole match | **122** | — | 338 |
| B Ti converted | **798** | — | **3938** |
| A shots fired / 1000 rd | **13** | 90 | **50** (last at r299) |
| B shots fired | 75 | 121 | **804** |
| A bank at r999 | 2782 | 3031 | 2858 |

Arithmetic: A's `ammo_target` is `24 if under else AMMO_FLOOR=16` and **`under` was
usually False**. On atoll B's harasser sat at core-dsq ≈ 20-25, outside the
builder trigger (`d <= 16`), and never touched the Core, so `last_hp` never dropped and
the 35-round latch expired. A therefore held **16 ammo = one sentinel shot**, refilled
10 Ti at a time: 122 Ti ÷ 10 ≈ 12 refills ≈ the 13 shots observed. **A fired 13 shots in
1000 rounds while holding 2782 Ti.** v79 holds `max(32-if-under, min(48, 4 × home_guns))`
(V10) — with 12 turrets on atoll that is 48, unconditional on UNDER — plus the 50-round
latch (V9). B fired 75.

## 2.1 jackpot — B core-kill at r189: **one sentinel, and both of our hunt gates**

```
r18  A sentinel (10,10)  — thrown forward into B's half, dead r24
r19  B sentinel (13,13)  dB= 2   <- B's FIRST turret is a home counterbattery
r29  B sentinel (15,13)  dB= 1
r30  A gunner   (11,14)  dB= 9   — A's second turret, also deep in B's half
r37  B sentinel ( 5, 5)  dA=32   <- THE KILLER, facing NORTHWEST
```
- (5,5)→(1,1) is `dsq = 32` = **exactly `SENTINEL_ATTACK_RADIUS_SQ`, on a clean
  diagonal**, and sentinel shots ignore obstacles. It fires **60 times, every one at
  tile (1,1)**, r38→r189. Ledger on A's core: **−1080 (60×18) vs +580 healed (145
  builder heals)** → 0 HP at r189. **`builder_attack` on A's core footprint: 0 events,
  entire match.** It was 100% turret fire.
- **A had a builder standing at (5,4) — orthogonally adjacent to the killer — for the
  whole r130-189 window and issued zero `builder_attack` after r99.** 20 pecks (40 Ti)
  would have removed a 40-HP sentinel.

Why our hunt never fired, precisely — **two independent gates, both blocking**:
1. **Band.** `_hunt_turret` L1427: `self.core.distance_squared(bp) > INTRUDER_CORE_DSQ(20)`
   measured from the **anchor**. (0,0)→(5,5) = **50 > 20** → excluded. `bots/_v70cg`'s
   parked `HUNT_BAND_DSQ = 41` measured to the **nearest footprint tile** gives
   (1,1)→(5,5) = **32 ≤ 41 → in band**. **This replay is direct, independent validation
   of the `_v70cg` band widening.**
2. **Healer floor.** Even in-band, L1481: `if healers < HUNT_MIN_HEALERS(2) and hp > HUNT_FINISH_HP(8): continue`.
   A's four builders sat frozen at (1,2), (2,3)/(3,3), (5,4), (7,4) — **exactly one**
   was adjacent to the core. **A 2×2 core in the map corner has only 4 orthogonally
   adjacent in-bounds tiles versus 8 for an interior core, so `HUNT_MIN_HEALERS = 2`
   is structurally ~2× harder to satisfy on jackpot-A than anywhere else.** This is a
   new gap; the band widening alone would not have saved this game.

The decoy: **B built 20 barriers on its own doorstep** (V5 rush-deny), rebuilding
(12,14) **17 times** and healing it **126 times** — ~190 Ti total. A's forward gunner at
(11,14) burned **128 of its 154 shots (512 ammo ≈ 512 Ti)** on those barriers while its
own core was being drilled. B's 66 shots: **60 into A's core**. B's turret doctrine is
home-first (dsq 1-2 at r19/r29), ours is forward-first — and neither of A's two turrets
was within dsq 160 of the killer.

**Named mechanisms:** V5 (rush-deny barrier wall as ammo sink), V2+V12 (home
counterbattery at r19 with only 2 harvesters — our ECO gate would have refused it),
V8 (`_midsq_far` gives jackpot-B gun_sense 81 vs our 64).

## 2.2 heart — 2.5× economy blowout: **the ore-parking bug**

Separation at **r184**; B permanently ≥100 ahead from **r208**.

| | A | B |
| --- | --- | --- |
| harvesters @r100 / @r400 | 3 / 5 | **6 / 9** |
| 5th harvester built | **r392** | **r57** |
| directed-connected at end | 2 of 5 | 7 of 9 |
| rate r300-999 | 5.00 Ti/rd | **15.00** |

**Builder-rounds spent standing on an `ORE_TITANIUM` tile:**

| map | A | B |
| --- | --- | --- |
| **heart** | **416 / 9559 = 4.35%** | 20 / 2606 = 0.77% |
| atoll | 78 / 7846 = 0.99% | 297 / 4203 = **7.07%** |
| jackpot | 8 / 818 | 2 / 940 |
| meander | 184 / 5065 = 3.63% | 181 / 3388 = 5.34% |

**404 of A's 416 heart ore-rounds are one tile: (5,18), occupied continuously r160→r998.**
A built a *conveyor* on (5,18) at r159 and then parked a builder on it for 838 rounds.
No harvester was ever built there by anyone; its neighbours (5,19)/(4,18)/(6,18) are all
EMPTY, so it was buildable from three sides. **A left 14 of heart's 28 ore tiles with no
harvester, ever** — (5,18), (12,5), (15,5), (11,1), (16,1) among them.

This is **V1** exactly: `build_harvester` needs an **orthogonally adjacent** ore tile,
so a builder standing *on* an isolated ore cell can never build there. On an open map our
approach-onto-ore behaviour is harmless (ore comes in clusters, the neighbour is also
ore). Heart has 122 walls (21.8%), ore is fragmented, and the behaviour becomes a
permanent park. x3r0's fix — step off to a cardinal non-ore, non-wall tile when
`sum(walls) >= 80` — is targeted at exactly this and fires on heart / saga / archipelago
only. **The asymmetry is real but the diagnosis must stay honest: the numbers do not
generalise.** On atoll it is **B** that squats on ore 7× more than A. Heart is the case.

Secondary: the C1 escort loop on (10,8) froze one more A builder for **737 rounds**.
Barriers: B built exactly 2 (r8 (18,8), r124 (16,10)); (16,10) was placed on the tile A
had put a gunner at r94. **V6** (`always_bunker` for heart-B (19,9)) is present but did
almost nothing here — heart is won by V1 and C1/C2, not by denial.

## 2.3 meander — B by 9010 vs 5660

**Cores are 7 tiles apart (anchor dsq 49).** The Core UNDER sensor is `turret dsq ≤ 64`,
so both teams are UNDER essentially from the first forward gun.

- B is shooting into A's base from **r7-r9**: sentinel (11,8) at dA=16, gunner (12,6) at
  **dA=4**. B ends with 4 turrets alive at every checkpoint.
- **A's turret count at r700 and r1000: zero.** All 3 sentinels and 2 gunners died
  r40-r276; A's last shot is **r299**. B fires **804 shots** — **545 of them into A's
  conveyors**.
- A rebuilds under fire instead of relocating: **201 conveyors built, 86 killed**, the
  same three tiles rebuilt 27/14/7 times → **+201% conveyor scale on everything**
  (v79: 72 built, 3 lost, +72%). A spawns 18 builders (+360% builder scale) and loses
  **13** of them; B spawns 5 and loses 2.
- The C1 loop at (9,11): **905 heals, 905 Ti, 453 rounds, one builder** — on a 3-Ti
  conveyor inside a gunner's kill zone.
- One thing A did right: A's launcher at (9,4) threw the same B builder to (4,5)
  **157 times** across r226-999, neutralising it for 774 rounds at **zero ammo cost**.
  **B has no launcher to answer with, on any of the four maps** (see O14).

**Named mechanisms:** V2 (no counterbattery ECO gate — decisive here: A's gate
`HOME_GUN>=1 ∧ HARVESTERS<3` binds through the whole window when B's r7/r9 guns arrive,
and A's 3rd harvester is not up until **r130**), V9/V10 (B converts 3938 Ti to ammo, A
converts 338), V3 (melee-first, which our `MELEE_FIRST_MAX_WALL_FRAC=0.015` denies
meander at 2.1% by 0.6 points). Note V5/V6's meander entries are keyed to
**(11,3) = the A seat**, so B won this replay with **none** of its meander denial code
active — and the battery says meander is bot-decided (seat A 16/32), so it wins from
both seats. The meander loss is C1/C2/C3 + V2, not the rush-deny table.

## 2.4 atoll — B by 190 Ti (19 stacks), the thinnest of the four

- A ends with **5 harvesters**, B with **2**, and both deliver **5.00 Ti/rd** from r100
  to r999 (A at 40% efficiency, B at 100%).
- B's whole margin is **contested-centre raiding**: B built **18 harvesters and lost 16**,
  all on centre tiles (9,8)/(9,9), dying every ~15 rounds r315-465. Each still shipped
  its **free stack on build**, so B farmed 10 Ti per 20-Ti harvester repeatedly (harvester
  scale reached +90%). A killed them — 264 builder attacks on B harvesters r200-500 —
  which is the one thing A did well here.
- **A's harvesters were never attacked, on any of the four maps.**
- The margin is 190 Ti; **the C1 loop on (4,10) cost A 819 Ti and one builder for 819
  rounds.** A's total combat burn 2365 Ti vs B's 1964. A ended with 12 builders producing
  5 Ti/round.
- A fired **13 shots in 1000 rounds** (C3).

**Named mechanisms:** mostly C1/C2/C3 rather than anything of his. His actives here are
V9+V10 (798 Ti converted, 75 shots) and V3. Atoll's 190-Ti margin means **any one of
C1/C2/C3 being fixed probably flips this map.**

---

# 3. BORROW LIST, RANKED

Ranking is (expected map coverage × independence from our machinery) ÷ risk. "Diff"
is estimated lines changed in `bots/_v70cm/main.py`.

### Tier 0 — fix our own machinery first (these are worth more than anything of his)

| # | Change | Evidence | Diff | Risk |
| --- | --- | --- | --- | --- |
| **B0a** | **Stalemate disengage for `_intercept`'s repair escort.** If the guarded building's HP has not net-improved over N rounds (or if the attacker is a turret rather than a builder), release the chase and clear state exactly as the existing cold-trail branch does. Reuse the `hunt_defer` no-progress idiom already in `_hunt_turret` (`HUNT_DEFER_BASE/SPREAD`) — same shape, already reviewed. | C1: 819/708/905-round locks, ~20% of match income per map, one builder each | ~25 | **Low.** Purely a release condition on an existing branch; the escort's win case (a raider that gives up) is untouched. Ablate on flotte_probe — the escort was shipped in v53 *for* flotte, so verify it still holds there. |
| **B0b** | **Do not medic/escort a building under turret fire.** `MEDIC_*` was sized against 2 dmg/rd melee; a gunner is ~3.5/rd and a sentinel ~9/rd. Add "no enemy GUNNER/SENTINEL in vision with the target in its attackable tiles" to the medic and escort predicates, and prefer `destroy()` + relocate the link. | meander (9,11): 905 Ti, 453 rounds, never delivered | ~20 | **Medium.** `destroy()` is free and cooldown-free, but relocating a link means recomputing `_link_path`, which is the one place chains break (C2). Consider shipping the "don't heal it" half alone first. |
| **B0c** | **Hunt band → `_v70cg`'s `HUNT_BAND_DSQ = 41` measured to the nearest core-footprint tile**, *and* relax `HUNT_MIN_HEALERS` when the core footprint has fewer than 8 in-bounds orthogonal neighbours (corner/edge cores). | jackpot: killer at anchor-dsq 50 / footprint-dsq 32; only 1 of 4 adjacent tiles ever manned | ~10 | **Low-medium.** The band half is already written and ablation-tested in `_v70cg`; the healer-floor half is new. `HUNT_MIN_RND=120` stays — the early-hunt waiver is REFUTED (eider 8/16→0/16) and jackpot's killer was still alive at r120. |
| **B0d** | **Cap the labor surge on measured throughput, not bank.** `SURGE_TI_FLOOR=1500 ∧ SURGE_MIN_RND=300` currently saturates to 18 spawns and buys nothing: 12 builders deliver the same 5.00 Ti/rd as 4. Gate `SURGE_EXTRA` on delivered-Ti-per-round rising, or on unwired harvesters == 0. | C2, all four maps; +340-360% builder scale | ~15 | **Medium.** The surge was measured POSITIVE vs kladde_probe on eider. This is a narrowing, not a removal — must re-run the eider/kladde leg. |

### Tier 1 — his mechanisms, high value, low collision

| # | Borrow | Explains | Diff | Composition risk |
| --- | --- | --- | --- | --- |
| **B1** | **V10 + V9: ammo magazine scales with home guns** (`if weapons: ammo_target = max(ammo_target, min(48, 4*weapons))`; `32 if under`; UNDER latch 35→50) | **atoll, meander** directly (13 and 50 shots per 1000 rounds); helps everywhere | **4** | **Low.** No store, no role, no ordering. **Caveat (important):** two ammo-buffer raises were refuted in this repo (AMMO_BUFFER 20→50 at 45.3%; threat-timed conversion at 46.1%) — but both raised a *fixed* floor. V10 scales with turrets **owned**, i.e. with realised demand, and A's failure mode here is the opposite one (turrets dry at 16 ammo with 2782 Ti banked). Test the three sub-levers separately; `4*weapons` alone is the cleanest. |
| **B2** | **V1: step off an isolated ore tile on wall-dense maps** (`sum(walls) >= 80`) | **heart** (14 of 28 ore tiles never mined; one builder parked 838 rounds); also saga, archipelago | ~18 | **Low.** Lives in `_expand`'s move phase. Must sit **after** the multi-healer convergence block (which returns) and **before** the `link_queue` move branch, so a shelled core still outranks ore. No store, no role. Ablate on saga (we hold 25/32 — protect it) and archipelago. |
| **B3** | **V7: `_deny_threat_tile`** — under UNDER, a builder already **orthogonally adjacent** to `SLOT_THREAT` fires on it | jackpot's (5,4) builder that did nothing for 90 rounds; the cad "67-round dead window" | ~15 | **Low, if ordered correctly.** Place it **below** the universal adjacent heal (O3/O5's "heal beats sabotage" ordering is measured and must hold) and **below** `_hunt_turret`. Then it only ever consumes a turn the heal could not use. It has no round floor, but it also never walks anywhere, so it cannot trigger the "pre-r120 hunting loses economy races" trap — that trap is about *pursuit*, not about a free adjacent peck. |
| **B4** | **V2, narrowed: waive the counterbattery ECO gate on close-anchor maps.** Not a removal — condition `if HOME_GUN>=1 and HARVESTERS<ECO_NEED` on `core.distance_squared(enemy_core) > ~100`. | **meander** (anchor dsq 49, B guns at dA=4 by r9, our 3rd harvester at r130); moonrise | **3** | **Medium.** The gate exists precisely because close-anchor maps generate opening threat noise ("three fixed-facing Sentinels aimed at transient spawn tiles"). The narrowing points the waiver *at* the maps the gate was written for, so this must be ablated on meander + moonrise + fjordgate specifically, not pooled. |

### Tier 2 — cheap, plausible, needs its own ablation

| # | Borrow | Explains | Diff | Composition risk |
| --- | --- | --- | --- | --- |
| **B5** | **V3: raise `MELEE_FIRST_MAX_WALL_FRAC` 0.015 → ~0.06** (adds meander 2.1%, eider 3.9%, hive 5.4%, atoll 5.6%) | atoll, meander | **1** | **Medium.** One constant, but hive is a 32/32 sweep for us and 5.4% sits just inside the new band. Ablate per-map, not pooled; consider 0.03 (meander + eider only) as the conservative step. |
| **B6** | **V4 (turret table only): BARRIER 4, above HARVESTER/CONVEYOR.** A gunner's shot is blocked by obstacles, so a barrier in the line must die before anything behind it can be hit. | jackpot (A burned 512 ammo on decoy barriers — this does not fix that, but it fixes the general case) | **6** | **Low.** Pure table. **Do NOT take the builder-melee half** (`BARRIER 1, CORE 2`): we win most games by core kill, and demoting CORE below BARRIER in the saboteur's melee order works against that. |
| **B7** | **V5's *concept*, not its table: pre-emptive tile denial.** Derive the shelling tiles (positions from which an enemy sentinel/gunner can hit our core footprint) at match start from the decoded map, and have the defender barrier/park them. | jackpot (B's 20 barriers ate 512 of A's ammo), meander, heart, nordkap, moonrise | ~60-90 | **High effort, low collision.** His hardcoded table is 7 (dims, anchor) entries tuned against Coreflood/Lorem/Pantheon — teams we may never draw, and it grows per map forever. A derived version is a class fix and composes with the defender's existing bunker/station machinery. Treat as its own project, not a port. |
| **B8** | **V8: scaled `gun_sense`/`b_sense`** | jackpot-B, lighthouse-B, snowflake, archipelago | ~12 | **Medium.** Widening the UNDER sensor cascades into ammo conversion (B1), `keep_artillery_forward`, `_expand`'s heal gate and convergence. Take it **after** B1 lands, so the two effects can be separated. |

### Do not borrow

- **V12 (role-2 → saboteur on the 256 band).** Direct collision: `role_n == 2` is **both**
  our defend-successor seat (O9, `SLOT_DEFEND_BEAT`) and one of our two multi-healer
  convergence seats (O4). Flipping it to saboteur on jackpot/lighthouse deletes both.
  If the jackpot second-attacker idea is wanted, lower the **role_n == 3** threshold on
  the 256 band instead (it already flips at 4 harvesters / r12) — role 3 is free.
- **V13 `keep_artillery_forward` widening** — adding `square_band`/`large_square`
  suppresses the near-core melee recall on jackpot/lighthouse/hive/drumlin/snowflake/
  archipelago. We sweep hive 32/32 and hold saga/lighthouse majorities *with* the recall.
- **V14 `sq25_freeze`** — targets hive (we sweep 32/32) and drumlin (seat-decided). No upside.
- **V11 / V16** — fjordgate-only; we already sweep it 32/32.
- **V17 (enemy-facing first-builder spawn)** — dead in both files (buffered store read in
  the same round-0 turn) and **measured 41% when activated**. Tell x3r0.
- **V18 (`role_n >= 4` → defend)** — collides head-on with O1: our 6th+ builders are
  replacements and must be generic expanders.

### Store-slot safety

Slots 0-12, 14, 15 are identical in both files. Slot 13 is `SLOT_DEFEND_BEAT` for us and
`SLOT_HOME_SENT` for him — **declared and never used anywhere in v79**. **Every borrow
above is store-safe in both directions.** No merge needs a slot renumber.

---

# 4. WHAT x3r0 SHOULD BORROW FROM US (the cad_probe gap: his 43.3% vs our 65.0%)

The CtrlAltDefeat insertion script (decoded from the 0-5 ladder loss e40a6c01,
`SCRATCH/cad_insertion_diagnosis.md`): Launcher at **r1**, 2-3 builders thrown at our
core by **r2**, one sentry planted at core-dsq **10-41** by median **r11**, first core hit
**r12**, core dead median **r361**. It is a long, patient chip siege delivered by units
that arrive early and keep arriving.

From v79's source, five specific reasons it bleeds — in descending order of how cheap
they are for him to fix:

1. **He never builds a Launcher.** `_try_build_launcher` (L426) is defined and **never
   called from anywhere**. We restored the `_defend` call site in v55 L1650-1653; his
   file kept the v63 deletion. Consequences: `_launchwait`, `_offer_launch`,
   `SLOT_LAUNCHED_ID`, `SLOT_DROPPED` and the whole insertion/exile subsystem are dead
   weight in his 2034 lines. **The replays confirm it: B built zero launchers on all four
   maps.** Against CAD this is the biggest single loss — our launcher exile ejects the
   first raider wave in every one of the 5 games. And the meander replay shows what it is
   worth even against *him*: our launcher at (9,4) neutralised one of his builders for
   **774 rounds with 157 throws at zero ammo cost**, and he had no answer. **Fix: ~3 lines**
   (`if harv >= ECO_NEED and self._try_build_launcher(ct): return` in `_defend`).
2. **No universal adjacent heal.** Ours (v55 L954-957) fires for **any builder of any
   role** standing next to the core under UNDER, ahead of every melee branch. His three
   heal sites are all narrow: `_expand` L1409-1417 needs `UNDER ∧ HOME_GUN>=1 ∧ area>120
   ∧ dsq<=16`; `_defend` puts `_heal_core` **behind** `_sabotage_prio → _deny_threat_tile
   → _try_counterbattery`; `_home_defend` puts it fourth. Against a chip sentry the heal
   is the correct action and he reaches it last. Measured on our side: 0, 0, 82 core heals
   across three replays before the reflex, and the 82 was the game we survived.
3. **No `_core_shelled`, so no heal-beats-sabotage ordering and no convergence.** He
   cannot distinguish "an enemy is loitering" (`SLOT_UNDER`) from "the core is being
   shot" (core HP < max). Ours reads it straight off the HP bar (L1349-1368) and drives
   both the `_defend` ordering and **multi-healer convergence** (O4): role_n 2 and >=5
   walk home when the core is provably bleeding, turning +4 HP/rd into +8..+12 against a
   sentinel's −9. He has exactly one healer, ever.
4. **Five builders per match, full stop.** `self.n` is a lifetime counter and
   `spawn_cap = 5`; a dead v79 builder is never replaced. Confirmed in every replay: B
   spawned exactly 5, at r0/r1/r2/r3/r4, and never again. CAD kills builders on purpose.
   Once his five are gone he is a set of buildings. Our O1 (`REPLACEMENT_MAX=8`,
   `REPLACE_TI_FLOOR=250`, `REPLACE_MIN_RND=60`) is deliberately shaped so the opening and
   the +20%/builder cost curve are **bit-for-bit untouched** — that shape is the part worth
   copying, because the naive version (`_v69bc`, raising the standing cap) measured **−13 pts**.
5. **`_deny_threat_tile` cannot walk.** It requires the builder to be **already
   orthogonally adjacent** to the single `SLOT_THREAT` cell. CAD's sentry sits at core-dsq
   10-41 — usually adjacent to nobody. Only his single role_n==4 defender navigates to the
   threat. Our `_hunt_turret` walks in, holds, and arbitrates ownership by id ballot with a
   no-progress override — and note our own honest caveat: even ours has the band and
   healer-floor gaps documented in B0c above.

Also worth passing on, as straight bug reports rather than trades:
- **V17 is dead and was measured bad.** `_core` L383-388 sorts the first builder's spawn
  toward the enemy core using `ct.read_store(SLOT_ENEMY_CORE)` — but the Core writes that
  slot four lines earlier in the same round-0 turn, and store writes are buffered, so `ec`
  is always `unpack_pos(0)`. We removed it; **activating it measured 41%**.
- **The `eco_need` lever is applied asymmetrically.** `_plan_siege` (L825-828) carries the
  `_wide ∨ _lsq` disjunct; `_saboteur` (L1024-1026) carries the `tall` disjunct. Neither
  site carries both. If that is deliberate it deserves a comment; if not, it is a tuner
  artifact that leaves half the lever unapplied on each map class.
- **`SLOT_HOME_SENT` (slot 13) is declared and never used** — free slot.

## What a merge would look like

The two files are the same skeleton with **identical navigation, pathing, link-building,
ore-picking, and launcher code**, and **no store-slot collision**. A merged bot is a real
option rather than a rewrite. The clean split of assets:

- **His:** wall-dense ore handling (V1), ammo magazine sizing (V9/V10), ungated home
  counterbattery on close-anchor maps (V2), tile-denial doctrine (V5/V6), melee-first (V3).
- **Ours:** launcher subsystem (O14 + exile), universal heal (O3), `_core_shelled` +
  convergence (O4/O5), turret hunting (O6), builder respawn (O1), chain medic (O8),
  defend succession (O9).
- **Contested / needs a decision:** population policy (his 5 disciplined vs our 18
  saturated — the replays say ours currently buys nothing, see C2/B0d), and role_n == 2's
  job (his second attacker vs our defend-successor + healer).
