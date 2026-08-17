# loki_leap — the merged leap build

Base: `bots/loki_turbo7` **with the CB counter-battery planks turned off**, which makes it
behaviourally a `loki_turbo4` (ladder v152) equivalent plus the archetype detector and PLANK SAP.
On top of that: three of the four measured leap planks (`analysis/leap_design.md`), merged by hand
from their forks, with two fixes to the collar that its own measurement demanded and one new arm.

Every rationale block lives at the end of `doctrine.py`, next to the constants it justifies. This
file is the merge record: what came in, what was resolved, what is off, and what is still risky.

## 1. What was merged, and what was not

| plank | fork | verdict | what shipped here |
|---|---|---|---|
| P1 REPAIR | `bots/loki_repair` | **keep all** | every flag at fork default. `doctrine.py` block, `eco.py` (`_l4_repair` tail + the `_rep_*` family), `main.py` (`__init__` fields, the `_builder` hook above the role split). `raid.py` untouched by this plank. |
| P2 COLLAR | `bots/loki_collar` | **keep, two fixes + one new arm** | `COLLAR_ON`, `COLLAR_SQUAT_ON`, `COLLAR_SPREAD_ON` on. Budget rebuilt (§4); `COLLAR_SURGE_ON` added (§5). |
| P3 SIEGE | `bots/loki_siege` | **keep three arms of four** | `SIEGE_SITE_ON`, `SIEGE_MASS_ON`, `AMMO_JIT_ON` on. `SCREEN_ON` **off** — measured wrong-direction: forward-sentinel survival fell 95.5 % → 91.4 % and the screen gunner fired 0.17 times a game. |
| P4 SIPHON | `bots/loki_siphon` | **not merged** | parked: mechanism correct, 39.7 Ti/game is too thin to pay for the scale. Its one load-bearing discovery — that `_arch_note` zeroed slot 13's high bits — is carried here as the single canonical `_arch_note` (§3). |

`bots/loki_siege_off` (the flag-off copy of the siege fork) played no part in the merge.

## 2. The CB planks, shipped OFF

`loki_turbo6` = `loki_turbo4` + these six flags, and `loki_turbo7` = `turbo6` + detector + SAP. The
ladder read that difference the wrong way round — v152 (`turbo4`) **+63.8 Elo over 57 matches**,
v153 (`turbo6`) **−39.8 over 4** — and locally `turbo4` beats the `turbo6`/`turbo7` line ~60 % head
to head. A weak ladder sample and a strong local one pointing the same way is enough to put them
down and measure the leap planks on a `turbo4`-equivalent base.

**Flags flipped `True` → `False` (all in the LOKI-BEARING block of `doctrine.py`):**

```
CB_LIVE_TARGET_ON   CB_MOBILE_GUNNER_ON   CB_BEARING_GATE_ON
CB_HUNT_MOVE_ON     CB_DRY_MAG_ON         CB_RANK_THREAT_ON
```

This is exactly the revert the T5 verdict block in `doctrine.py` already prescribes, and each flag
is independently toggleable — verified against the call sites in `main.py` (`_cb_scan` 
`_home_gun_bears`, `_try_counterbattery`, `_t5_bearing_hunt`, the two threat latches, the dry-magazine
arm in `_core`). Two related constants are **dead while these are off** and are deliberately left at
their `turbo6` values so that flipping the six back on restores `turbo6` exactly:

* `CB_TARGET_BUILDERS_ON` — feeds `CB_RANK_ACTIVE`, which `_cb_scan` only reads on the
  `CB_LIVE_TARGET_ON` path;
* `CB_SMALL_MAP_CAP_ON` — already `False`, and read only inside `if CB_BEARING_GATE_ON:`.

`CB_OVER_HEAL_ON` is **not** one of the six. It predates them (it is in `turbo4`) and stays on.

Unchanged from `turbo7` by policy: `ARCH_ON` and `SAP_ON` stay **on** (panel-neutral at n=1350,
PRESSURE-gated). Every `T5_*` flag stays off, as `turbo4`/`turbo6` ship them.

## 3. Conflict resolutions

**`main.py` `__init__`** — three forks add a per-unit block at the same anchor (after the SAP
block). All three are present, in plank order REPAIR → SIEGE → COLLAR, none dropped. `col_carry`
from the first cut of the budget fix is gone with it (§4).

**`main.py` `_arch_note`** — the collar fork and the siege fork each wrote their *own* fix for the
same defect the siphon fork discovered: the detector rebuilt slot 13 from four fields and dropped
everything above bit 25. **One canonical implementation survives**, the siege fork's:

```python
nv = (v & ARCH_KEEP_HI) | (s5 << 21) | (s2 << 20) | (it << 10) | pr
```

`ARCH_KEEP_HI = 0xFC000000` preserves bits 26–31 as a block, which is a superset of both forks'
masks. It contributes 0 while no high bit is set, so the word written with the leap flags down is
bit-identical to `turbo7`'s.

**`raid.py` `_raid_act`** — the collar inserts step 0 and the siege inserts step 3c, at different
anchors; both applied. The merged ladder is:

```
0.  COLLAR: crit-tend > (surge: tend) > brick/reseal > tend > squat-support
1.  parent PECK from a seat
2.  parent SEAL a free seat
3.  FORWARD SENTINEL  (site-fixed: in-band + ranked)
3b. T5 nest gunner    (flag off)
3c. SIEGE SCREEN      (flag off)
4.  parent BUDDY HEAL … and the rest of the parent ladder unchanged
```

This is the priority the plank DOCTRINE.md files document: crit-tend/collar > brick/reseal >
parent peck > forward-sentinel > screen > parent ladder. Above the raid, `main.py._builder` keeps
emergency core heal > SAP > REPAIR tick > role split.

**`raid.py` `_raid_station`** — collar-only; the parent's two corner cases (`+12` finished, `−6`
still open) are kept verbatim and the collar adds a third (a corner carrying a hurt brick is a TEND
station). Untouched by the siege fork.

**`raid.py` `_try_forward_sentinel`** — siege-only, fixed in place. Untouched by the collar fork.

## 4. COLLAR FIX 1 — the budget, and what the measurement actually meant

`results/leap/loki_collar.md` recorded a mean of 13.5 and a max of 46 titanium a game against a
claimed 40 cap and called it a read-modify-write race. **It is worse than that, and the merged
build's own replays say so.** `tools/leap_store_audit.py` on `loki_leap` vs `mimic_istone` (royale):
seven bricks at 7 Ti each — 49 titanium spent — and the slot-13 budget field read **zero on every
round of the game**. Every increment was lost.

The mechanism is structural, not incidental. Store writes are buffered a round, so every writer in
round *N* reads the same round *N−1* word. `_arch_note` is called by the Core, by every builder and
from `eco.py`, and against an opponent that keeps a body near us its S3 stamp changes every round —
so it writes slot 13 every round, and whichever unit moves **last** wins, with a word built from the
stale read. The collar's increment survived only when the collar's writer happened to be the last
unit of the team to move. The fork was not measuring an overrun; it was measuring a broken counter.

**The rule this establishes.** A field that is RE-DERIVED every round (the siege HP band, the raid
heartbeat, the detector's own stamps) tolerates a lost write — the next round repairs it. A field
that ACCUMULATES cannot. An accumulating field may only live in a slot whose writers it can
enumerate.

**So the counter moved out of slot 13** into `SLOT_RAID_LIVE` (15), whose only writers in the whole
tree are the two raid heartbeats in `_raid` — and the collar's publish is folded into those, so slot
15 still takes exactly one write per raider per round from one place (`_raid_beat`).

* bits 0–9 — the heartbeat, `round + 1 ≤ 1001`, unchanged. `_foothold_live` now masks it.
* bits 10–27 — three six-bit **lanes**, one per `raid_slot % 3`. A lane holds **that body's own
  cumulative spend**, republished whole every round, so a lost write costs one round of latency and
  repairs itself.

The gate is a **pessimistic reservation**: a body may spend only what it can CONFIRM fits at
`observed + COLLAR_RACE_MARGIN`. Its own lane comes from `self.col_spent` (exact, current); the
other lanes come from the store and are at most one round stale, which is precisely what the margin
reserves against.

```
COLLAR_TI_BUDGET   32      (was 40)      COLLAR_RACE_MARGIN  6
```

Measured ceilings on the shipped build (`tools/leap_store_audit.py`): peak team spend **26 Ti**
without the surge and **58 Ti** with it — both exactly the arithmetic maximum
(`budget − margin − barrier_cost`, then one last barrier), so the cap binds rather than being
approached. Non-surge worst case therefore lands under the 40 the plank was measured claiming.

## 5. COLLAR FIX 2 — `COLLAR_SURGE_ON`, the terminal window

New, not measured in the collar fork; added on the SIEGE fork's evidence, which is about how *both*
arms end their games: the raid grinds the enemy Core to a median of 14 HP and then **stalls** there.
Two planks arrive at the same wall and the wall is healing. So while the enemy Core is below
`SIEGE_MASS3_HP` (400) — the **same signal from the same source** as `SIEGE_MASS_ON`'s third-tube
trigger, `_sge_core_band` in `raid.py`, slot 13 bits 26–27 — two things change:

1. **the budget doubles** (`COLLAR_SURGE_MULT` = 2);
2. **ordinary TEND is promoted above BRICK** inside `_collar_act`. Breadth of denial while there is
   time, depth of it when there is not: a brick that falls re-opens a seat worth +4 HP per titanium
   every round, and holding it costs 1 Ti against 3–7 for a fresh one.

**What is NOT gated on the surge, because it was already true:** collar tend/brick already outranks
the parent's Core peck unconditionally — `_collar_act` is step 0 of `_raid_act` and the peck is step
1, in the collar fork as measured and in this merge unchanged. There is no reorder to gate. Recorded
so a later reader does not "fix" it.

`_sge_core_band` is memoised on the round: the siege fork called it once per established raider per
turn and the collar's budget path asks the same question up to three more times.

## 6. Comm store audit

| slot | field | writers | notes |
|---|---|---|---|
| 8 `SLOT_FWD_GUN` | forward sentinel count | `raid._t5_note_fwd_build` | collar reads it in `_collar_live`; no new writer |
| 9 `SLOT_HEAL_BUDGET` / `SLOT_ARCHETYPE` | bits 0–15 bleed beacon, 16–17 archetype, 18–27 stamp | **Core only** (`main._core`) | collar and siege **read only**. Bits 28–31 still free |
| 10/11 `SLOT_FERRY_*` | ferry request | raid layer | untouched |
| 12 `SLOT_RAID_N` | raid seat issuer | `main._builder` | untouched; the collar's lane index is `raid_slot % 3` |
| 13 `SLOT_ARCH_SEEN` | bits 0–25 detector, 26–27 **legacy** siege HP band | `_arch_note` (any unit) and `_sge_core_band` (any unit with eyes) | the band copy here is a HINT since FIX B (§11): still written on a transition, still read, but only when slot 15 says UNKNOWN. Bits 28–31 remain the reserved merge budget for `bots/loki_macro` |
| 15 `SLOT_RAID_LIVE` | bits 0–9 heartbeat, 10–27 collar lanes, **28–29 siege enemy-Core HP band** | `raid._raid_beat` **only** — one write per raider per round | bits 30–31 free |

Verified: exactly one `_arch_note`; no writer collisions; the collar field and the band no longer
share a slot; `SLOT_T5_BATT` (also slot 13) is written only under `T5_BATTERY_GATE_ON`, which is
`False`. Slot 15's lane read masks to `COLLAR_LANE_BITS * COLLAR_LANES` bits so the band above the
lanes is refreshed rather than carried round; `_collar_spent` masks each lane to six bits and
`_foothold_live` masks the heartbeat to ten, so neither sees the band.

## 7. Inertness

With `REPAIR_ON = COLLAR_ON = SIEGE_SITE_ON = SIEGE_MASS_ON = AMMO_JIT_ON = False`
(`bots/leap_inert`, stamped by `tools/leap_variant.py`): **zero** `REP`/`COL`/`SGE` markers over two
games, no store writes above bit 25, and `_raid_beat` writes `rnd + 1` exactly as the parent does.
The `ARCH` markers that remain are `turbo7`'s own detector, which stays on by policy.

## 8. Evidence from the smoke set

Single games — noise on win rate, proof on "did it fire and did it raise". `tools/leap_smoke.py`.

| game | result | our tracebacks | markers seen |
|---|---|---|---|
| vs `starter`, antler/A | **win**, r54 | 0 | `ARCH PRESSURE`, `REP rebuild` |
| vs `mimic_0033`, nordkap/A | loss, r246 | 0 | `ARCH PRESSURE`, `COL brick`, `REP heal/rebuild/walk`, `SGE jit` |
| vs `mimic_0033`, antler/B | **win** (r1000) | 0 | `COL brick`, `REP rebuild`, `SGE jit/site/mass2 disc=1` |
| vs `mimic_istone`, royale/B | **win**, r83 | 0 | `COL brick ×7`, `REP rebuild`, `SGE jit/site` |
| vs `mimic_istone`, synth_d 30×30/B | r1000 loss | 0 | **`ARCH MACRO_WEAK r=140`, `COL squat`**, `COL brick/tend`, `SGE jit/site/mass2` |
| vs `mimic_istone`, synth_b 24×24/B | **win** (r1000) | 0 | `SGE mass3 disc=1` (third tube on the assault clock), `COL tend`, `REP rebuild` |
| `leap_inert` vs `mimic_istone` / `mimic_0033` | — | 0 | **none** (bar `ARCH`) |

The `Position out of bounds` tracebacks that appear in some `starter` games are `starter`'s own
known bug — reproduced at the same rate in `starter` vs `starter` (`bots/starter/main.py:391`,
`is_tile_empty(next_pos)`), and `loki_turbo7` draws them on the same cell.

`SGE site` distances observed: 2.92, 3.54, 4.30, 4.53, 4.95, 5.52 — every one inside the measured
[2.5, 5.7] band.

## 9. Frozen ablation variants

Stamped by `tools/leap_variant.py`, full copies, differing only in the named doctrine lines, so the
Measure phase never edits a bot directory:

| dir | difference |
|---|---|
| `bots/leap_nocollar` | `COLLAR_ON = False` |
| `bots/leap_norepair` | `REPAIR_ON = False` |
| `bots/leap_nosiege` | `SIEGE_SITE_ON = SIEGE_SITE_FALLBACK = SIEGE_MASS_ON = AMMO_JIT_ON = False` |
| `bots/leap_inert` | those plus `COLLAR_ON`, `COLLAR_SURGE_ON`, `SIEGE_BAND_SAFE_ON`, `SIEGE_BAND_ALLSEE_ON`, `REPAIR_ON` — the inertness control |

`leap_nosiege` deliberately **keeps** `SIEGE_BAND_SAFE_ON` and `SIEGE_BAND_ALLSEE_ON` on. They are
named `SIEGE_*` but the field they carry has two consumers and one of them is `COLLAR_SURGE_ON`,
which this leg keeps; turning them off would ablate half the collar inside the siege leg. With
`SIEGE_MASS_ON` down and the collar up, `_sge_band_armed()` is still True and the band still
publishes — for the collar. With the collar down as well (`leap_inert`) nothing derives, publishes
or reads it and slot 15 is the parent's plain heartbeat.

The control leg for §11's two fixes is not kept in `bots/`; it is one command, and it reproduces the
pre-fix build exactly because both fixes are flag-reachable:

```
python tools/leap_variant.py leap_prefix SIEGE_SITE_FALLBACK=False SIEGE_BAND_SAFE_ON=False SIEGE_BAND_ALLSEE_ON=False
```

## 10. Residual risks

1. **The lane ledger under-counts in three cases**, all in the overspend direction: more than three
   collar bodies share lanes (two bodies in one lane show as the later writer's figure, not their
   sum); a raider that dies takes its lane's history with it and a replacement re-issues from zero;
   and other bodies' spends are one round stale. The measured collar crew is 1–3 bodies and
   `COLLAR_RACE_MARGIN` reserves against the last of the three. `lane went backwards` in
   `tools/leap_store_audit.py` counts cases 1–2 directly: 0 in three of four audited games, 1 in the
   fourth.
2. ~~**The siege HP band still shares slot 13 with the detector**~~ — **fixed, §11 FIX B.** The
   authoritative copy is slot 15 bits 28–29, republished every round by the sole writer of that
   slot. Measured before/after in §11. What survives of this risk: the band is only ever published
   by a body that is *established at the ring*, so a game in which no raider ever gets eyes on a
   Core tile still reads UNKNOWN, and UNKNOWN behaves as HIGH for both consumers.
3. **`COLLAR_SURGE_ON` doubles a budget in the phase where titanium also buys the third tube.** If
   sentinels-per-game falls while collar spend rises, this is why. Pre-registered.
4. **The surge latch can be stale.** A Core seen at 399 that heals to 500 leaves blind raiders
   surging until a body with eyes republishes. FIX B shortens this from "until the next transition
   lands" to one round; it costs titanium, never a refusal.
5. **Turning `T5_BATTERY_GATE_ON` back on** re-binds slot 13 as `SLOT_T5_BATT` and blows away the
   detector and the band's legacy hint. Since FIX B the band itself is in slot 15 and safe from it,
   as the collar already was.
6. **CPU is unmeasured on this build.** `exec_time_us` is not populated in local replays on Windows
   and the TLE is only enforced on Linux (`tools/README.md`), so the offline micro-bench is still
   owed. The merge adds bounded per-round work only: the band is memoised per round, the screen (the
   one unbounded ray search) is off, and `_rep_watch`'s scan is the one genuinely new per-round loop.
7. **Every plank was measured alone against `loki_turbo7`.** None was measured on a `turbo4`-
   equivalent base, and none was measured beside the others. This build's A/B is the first test of
   both of those assumptions at once.
8. **Run-to-run variance on this harness is larger than the effects being measured.** The same bot
   on the same 30 cells, same seeds, same opponent produced 2.40 and 3.17 sentinels a game in two
   consecutive runs. `_cpu_exhausted` reads wall-clock, so the tree is not deterministic under a
   fixed seed. Any sentinel-count claim below rests on the marker counters (which count decisions,
   not outcomes) rather than on a between-run difference in `sent/g`.

## 11. Changelog — 2026-08-16, the two measured defects of the merge

Both fixes are reachable by flag, so the pre-fix build is a stamped variant rather than a hand
revert (§9). No other behaviour was touched.

### FIX A — the siting band was a veto, now it is a preference

`raid._try_forward_sentinel` skipped every out-of-band post with a bare `continue`, so a raider
whose four cardinals were all outside [2.5, 5.7] built nothing where the parent would have built.
The post loop now evaluates out-of-band posts too, keeps the parent's first-come admissible pick in
`par`, and builds it **only if no in-band post was admissible anywhere** — logging
`SGE fallback (x,y) d=…` instead of `SGE site`. The scan stops at the first out-of-band candidate,
so the added cost is the parent's own scan and no more. `SIEGE_SITE_FALLBACK`, doctrine.py §1b.

Invariant, which now holds by construction: the parent builds iff *some* (post, facing) passes
`can_fire_from` + `can_build_sentinel`; this arm builds iff some in-band one does (ranked) **or**
some out-of-band one does (first-come) — the same condition. Forward-sentinel builds with
`SIEGE_SITE_ON` are therefore `site + fallback` and can never be fewer than the parent's.

Evidence, `tools/loki_siege_mechanism.py` vs `mimic_ph`, 15 maps × 2 sides:

| run | build | site/g | **fallbk/g** | in-band % | sent/g | control `loki_turbo4` sent/g |
|---|---|---|---|---|---|---|
| n=30 | fixed | 1.47 | **0.33** | 63.9 | 2.40 | — |
| n=30 | pre-fix | 1.77 | 0.00 | 75.3 | 2.43 | — |
| n=30 | fixed | 1.50 | **0.47** | 48.4 | 3.17 | 2.93 |
| n=60 | fixed | 1.28 | **0.63** | 45.7 | 2.88 | 3.12 |
| n=60 | pre-fix | 1.72 | 0.00 | 69.5 | 2.52 | 2.73 |

`fallbk/g` is the direct count of the decisions the veto used to refuse: **0.33–0.63 tubes a game**,
stable across four independent runs. `sent/g` against the `turbo4` control is **not** stable
(risk 8) and neither confirms nor refutes the count — read the fallback column, not that one. The
cost lands exactly where it was pre-registered: in-band share falls, because a fallback tube is
out of band by definition (both observed in the smoke set stood at d = 6.36, the 5-step diagonal).

### FIX B — the HP band's published copy was transition-latched in a contended slot

The band drives `SIEGE_MASS_ON`'s third tube and `COLLAR_SURGE_ON`. Its publish was one write per
*transition* into slot 13, which `_arch_note` overwrites from a stale read every round against a
busy opponent — so the transition was simply lost, and lost until the next one. Three changes:

* the authoritative copy is **slot 15 bits 28–29**, written by `_raid_beat` (the slot's only
  writer) in the same word as the heartbeat, **every round**. A raider with eyes publishes what it
  sees; a blind one republishes what it read, so it can never erase a seeing body's answer.
* slot 13 bits 26–27 are **kept, unchanged and still transition-latched**, for backward compat —
  read only when slot 15 says UNKNOWN. Deliberately not made per-round: slot 13's real writer is
  the detector, and a per-round band write from a stale read would stomp *its* evidence.
* the re-derive broadens from established raiders to **every body with a Core tile in vision**
  (`main._builder`, gated on builder vision r² = 20).

Evidence, `tools/leap_store_audit.py`, vs `mimic_0033`, seed 1, side A — the enemy Core fell below
400 in all six games:

| map | build | first < 400 | slot-15 band | slot-13 band |
|---|---|---|---|---|
| nordkap | pre-fix | r140 | — | **no transition** |
| royale | pre-fix | r146 | — | LOW at r147 |
| antler | pre-fix | r30 | — | **no transition** |
| nordkap | fixed | r127 | **LOW at r128** | LOW at r128 |
| royale | fixed | r174 | **LOW at r175** | LOW at r175 |
| antler | fixed | r27 | **LOW at r28** | LOW at r28 |

1 of 3 before, **3 of 3 after**, each landing the round after the Core crosses 400. `COL surge`
(a new edge-triggered marker, added because the surge previously had *no* replay evidence at all —
which is how this defect survived) now fires in **6 of 6** smoke games, including the `synth_d`
game whose enemy Core bottoms out at 388. `SGE mass3` appears in 2 of 6.

### Verification

`py_compile` clean on all four modules of `loki_leap` and of each variant. Smoke suite (§8 fixture,
6 games): **0 our-side tracebacks**, markers `SGE site / fallback / mass2 / mass3 / jit`,
`COL brick / tend / surge`, `REP heal / rebuild / walk / lost`, `ARCH PRESSURE / DEFAULT`. The
`Position out of bounds` process-level traceback in the `starter` game is `starter`'s own bug (§8).
`leap_inert` re-verified: **no markers at all**, every collar lane 0 and both band fields 0 for a
whole game.


---

# 12. `bots/loki_leap3` — THE TERMINAL WEAPONS FORK (2026-08-17)

Fresh fork of `bots/loki_leap` (deployed v156). `bots/loki_leap` and
`bots/loki_leap2` and every mimic are FROZEN and untouched; everything below is
new code in a new directory, all of it behind `TW_*` flags that default ON in
this fork and leave the tree bit-identical to `loki_leap` when down.

Brief: `analysis/heal_wall_diagnosis.md` (144 games, `loki_leap` v156 vs
`mimic_istones`, 18 maps ≥ 20×20, both sides, seeds 1–4). Its finding, in one
line: **damage/round == heal/round to two decimals in 42 of 46 stalls**, at
3.1 HP/r and at 23.4 HP/r alike. The wall is a servo that matches whatever we
bring, up to a ceiling of `4 × manned seats`, and its bank never empties. H3
prices the damage lever out (a fourth tube is 20 Ti/round against 7.29 Ti/round
of stall income, 68 % of which is already ammunition). So both weapons here buy
SEATS. Neither buys damage. W2 (a fourth tube) is refuted and deliberately not
shipped — there is no flag for it.

## 12.1 What was implemented

| | W3 LAUNCHER PLUCK (rank 1) | W1 GUNNER-ON-HEALERS (rank 2) |
|---|---|---|
| flag | `TW_ON` + `TW_PLUCK_ON` | `TW_ON` + `TW_GUN_ON` |
| building | Launcher on a ring **CORNER** | Gunner on a corner / 1–3 tiles out, **never a seat** |
| what it buys | −8 HP/r of their heal per launcher, **0 Ti/round** | −4 HP/r sustained (−8 if they counter-heal), 4 Ti/r |
| cap | `TW_LAUNCH_CAP = 4`, one per corner | `TW_GUN_CAP = 1` |
| ladder | `_raid_act` step **3d**, above the gunner | `_raid_act` step **3d**, below the launcher |
| ledger | the **live census** (`_tw_census`), no store field | the same census |

* **W3 site rule.** Corners only. A corner holds exactly two heal seats inside
  the launcher's `d² ≤ 2` pickup disc, is not itself a seat (so it is outside
  `mimic_istones._fouled_seats`, which scans seats only), and does not consume a
  tile a 3-Ti brick could hold. Four corners cover all eight seats.
* **W3 progression.** First launcher as soon as the gate opens; the second only
  after the census has stood `TW_LAUNCH_AGE` (= `SIEGE_MASS2_AGE` = 20) rounds,
  which is the survivorship rule tube 2 already uses; third and fourth on the
  same rule while their Core is above `TW_LAUNCH_HP_FLOOR` (100).
* **W3 throw rule.** Enemy builder bots only (the pickup is **team-blind** and
  our own squatters sit on the two seats the corner covers), a body on one of
  their seats preferred, thrown to the **farthest** legal tile from THEIR Core
  inside `d² ≤ 26`, never inside `TW_THROW_MIN_DSQ` of their Core (a free seat is
  a *legal* throw target — dropping a warden from one seat onto another is a
  gift) and never within `TW_THROW_CLEAR_DSQ` of one of our own buildings.
* **The ratchet.** A plucked seat is free the same round and the collar already
  polls `can_build_barrier` on every adjacent seat every round, so no new code
  path — only budget. `_collar_budget` gains `TW_COLLAR_BONUS` (24 Ti) while one
  of our launchers stands at their ring. Turn order supplies the timing for
  free: raiders are spawned early and act *before* a launcher built at r ≥ 60.
* **W1 siting.** Ray is 3 tiles cardinal, 2 diagonal, stops at the nearest
  occupant, blocked by walls. A corner facing **along** the ring covers the two
  seats on that side (the 2-seat post, ranked first); the same corner facing the
  footprint **diagonal** puts a Core tile first with nothing able to stand
  between — 7 HP/r of unblockable Core damage. Facings whose first ray tile
  holds one of OUR buildings or bodies are refused (`_turret` will not fire on
  our own team, so such a gunner is simply mute). The engine's own
  `can_fire_from` has the last word, and the post must have a live target now.
  Re-aiming is the parent's `ROTATE_DISCIPLINE_ON` arm, unchanged.
* **W1 ammunition.** Slot 15 **bit 30** carries "a TW gunner stands at their
  ring", written by `_raid_beat` (that slot's only writer) on the same
  re-derive-or-republish discipline as the HP band in bits 28–29. The Core adds
  `TW_GUN_BURN` to the JIT burn term when the bit is set. "After the tubes" is
  enforced at the BUILD (step 3d, `TW_GUN_MIN_TUBES ≥ 1`, the tube's bank
  floor), never inside a conversion — the ammunition pool is global and
  undifferentiated and has no notion of priority.

## 12.2 The gate — six terms, both weapons, all required

```
TW_ON and
    archetype in (MACRO, MACRO_WEAK)        # slot 9 bits 16-17, Core-only writer
and no enemy turret EVER seen by this body  # latch, stricter than "d<=8 of their Core"
and this body established at the ring       # dsq_core <= LOKI_ESTABLISH_DSQ
and the raid heartbeat is live              # slot 15 bits 0-9
and an enemy Core footprint tile in vision
and their manned seats >= TW_MIN_MANNED (3) # max-latched
and round >= TW_MIN_RND (60)
```

Verified: vs `mimic_0033` (a turret opponent) on two cells, **zero** TW markers;
`bots/leap3_inert` (`TW_ON=TW_PLUCK_ON=TW_GUN_ON=False`) vs `mimic_istones`,
**zero** TW markers over a full 1000-round game.

## 12.3 Two constants the diagnosis got wrong, and how they were measured

The brief prescribed `bank ≥ launcher_cost + LOKI_FWD_TI_FLOOR` and said the
launcher costs "~20–30 Ti once". Shipped exactly like that, **the rank-1 weapon
never fired**: 6 games vs `mimic_istones` on the stall cells produced 0
`TW launch` markers.

`TW_LOG_WHY` (probe grade, default off; `bots/probe_pluck` stamps it on) prints
the refusal. Two causes, both measured:

| refusal | count / game | what the numbers said |
|---|---|---|
| `w=bank` | 48–101 sampled rounds | **c = 57, 60, 61, 72, 74, 88** against a bank whose median in that window is 12–56 Ti. "20–30" is the BASE cost; the price is `floor(20 × scale)` and the scale at the gate round (r140–360) is 3–4.4×. With the 40 floor the arm demanded 97–128 Ti. |
| `w=site` | 3–36 sampled rounds | ti = **150, 123, 112, 109** against c = 88, 74, 72, 60 — the bank was there and the arm still refused. A builder builds on an **orthogonally adjacent** tile and every corner is **diagonal** to every other corner, so a raider parked on a corner (which is where `COLLAR_BRICK_BONUS` puts it) can never lay this building. |

Fixes, both flagged and both documented at their constants:

* `TW_LAUNCH_TI_FLOOR = SIEGE_MASS_TI_FLOOR` (6), not `LOKI_FWD_TI_FLOOR` (40).
  It is the tree's own measured "bank kept after a purchase made at the ring in
  the terminal phase", and it is safe here for two reasons the 40 was not: this
  arm cannot open before r60, by which round every forward Sentinel that will
  ever be built has been (first tube r23 median, cap 3); and a launcher has
  **zero** running cost, whereas the 40 exists to leave a tube's 5 Ti/round of
  ammunition affordable.
* `TW_LAUNCH_WALK_ON` — a walk-to of exactly the shape `T5_NEST_WALK_ON` already
  gives the Sentinel nest: while the gate is open, the bank affords one and none
  stands, this raider's station becomes a tile beside a **free** corner. It
  yields the moment any of those stops being true.

## 12.4 Residual risks, pre-registered

1. **`TW_LAUNCH_TI_FLOOR` is a deviation from the brief**, argued from a
   measurement the brief did not have. If forward Sentinels per game fall in the
   A/B, this is the first thing to look at.
2. **The walk-to pulls a body off the collar.** Bounded by the same four
   conditions that open it, but a raider walking to a corner is a raider not
   tending a brick. `COL tend` / `COL brick` per game is the counter-check.
3. **The corner launcher is bot-impassable and takes a collar TEND station.**
   `_raid_station` skips it (it tests `is_tile_passable`), so the cost is a
   rescan, not a stall — but four launchers would remove all four tender posts.
4. **Two mechanisms key off `mimic_istones`' exact code** and neither is
   verified against the real I Stone (the diagnosis's own caveat 1):
   `_fouled_seats` scanning seats only (so a corner building is never pecked by
   the uncollar arm), and a thrown warden holding its wall slot while it walks
   back (so no replacement joins).
5. **The manned-seat term is MAX-latched**, so once a body has seen three manned
   seats the weapon stays armed for that body's life. Deliberate — the wall mans
   up and stays manned (H1), and the dips are the ones we cause — but it means
   the gate cannot re-close on seat count alone.
6. **`TW_COLLAR_BONUS` raises a cap in the phase that also buys ammunition.**
   Same shape as `COLLAR_SURGE_ON`'s risk 3 and recorded for the same reason.
7. **CPU is unmeasured**, as for the whole tree (`exec_time_us` is not populated
   on Windows). The weapons add: one bounded census per raider per round
   (memoised), eight `is_in_vision` probes behind the gate (memoised), and one
   `get_nearby_entities` scan per launcher per round. The launcher's throw-site
   list is built once per (position, anchor) pair and never rebuilt.

## 12.5 Tools

| tool | what it does |
|---|---|
| `tools/loki_leap3_mechanism.py` | per game: their heal HP during the siege, manned-seat-rounds, healer kills, plucks, tubes at terminal, their Core min HP, rounds-to-kill after the first tube, win/stall/loss |
| `tools/leap3_smoke.py` | the verification batch: 6 fixture cells + 2 gate legs (`mimic_0033`) + `starter` + the inert control |
| `tools/leap3_pluck_probe.py` | the one estimated parameter — RE-SEAT LATENCY after a throw, from `bots/probe_pluck` (`TW_PLUCK_LOG_ALL`) |
| `tools/leap3_ab.py` | parent vs fork on the stall cells, judged on **cells flipped** (diagnosis caveat 3) |
| `bots/leap3_inert` | `TW_ON = TW_PLUCK_ON = TW_GUN_ON = False` — the inertness control |
| `bots/probe_pluck` | `TW_PLUCK_LOG_ALL = True`, `TW_LOG_WHY = True` — the probe |

## 12.6 What it actually did — measured

`tools/leap3_ab.py`, 10 stall cells x seeds 1-3, `loki_leap` vs `loki_leap3`,
both vs `mimic_istones`, 30 games each; `tools/loki_leap3_mechanism.py` on both
sets of replays. Judged on cells flipped (diagnosis caveat 3), and read with
DOCTRINE.md risk 8 in mind — this harness is not deterministic under a fixed
seed.

| stall class (n=19 each) | `loki_leap` | `loki_leap3` |
|---|---|---|
| their ceiling, `4 x manned seats`, HP/r | 20.05 | **19.38** |
| their manned seats | 5.01 | **4.84** |
| **their heal actually landed, HP/r** | 9.58 | **6.53** |
| **seats WE hold** | 0.98 | **1.60** |
| our tubes at terminal | 2 | **1** |
| kills / wins, all 30 | 11 / 18 | 11 / 17 |
| cells improved / unchanged / regressed | — | 2 / 6 / 2 |

**The mechanism works and the trade is a wash.** The weapon does exactly what it
was designed to do — their landed heal falls a third, the seats we hold rise
63 %, and in the extreme case (`synth_f_royale_moved_B_s3`, 1 904 plucks) their
manned seats fall to **0.50** and their ceiling to **1.98 HP/r**, i.e. the wall
stops existing — and the game is still a stall, because in that game we had one
tube and it arrived at r677. **Our tubes at terminal fell 2 -> 1 in stalls and
3 -> 2 in kills**: the launcher and the gunner are bought out of the same bank
the tubes are, so seats were bought and damage was sold, one for one. That is
risk 12.4/1 landing exactly where it was pre-registered.

Read against the diagnosis this is a confirmation, not a refutation: section 3
already says the servo is only binding *given enough damage*, and its own
postscript says the third weapon slot "is not a weapon: the ECO plank"
(tc@r100 < 400 -> 11 % kills; >= 400 -> 82 %). Removing the ceiling does not
help while our damage is one tube.

## 12.7 The probe — re-seat latency, measured at last

`tools/leap3_pluck_probe.py --replays 'results/leap3/ab/loki_leap3_*.replay26'`
detects throws GEOMETRICALLY (a body of theirs that stood on one of their seats
inside `d^2 <= 2` of one of our launchers last round and is more than one step
away this round — nothing else in the engine moves a body more than one tile),
so it does not depend on the rate-limited marker. 15 games, 127 seat-throws:

* **re-seat latency: median 4.0 rounds**, mean 7.3, p90 13 (from the 94-sample
  game; the diagnosis estimated 3-5 from geometry, so the estimate was right);
* **25.2 % of thrown seats are never re-seated by them at all**;
* **17.3 % are taken by US first** — that is the ratchet, working.

One thing the probe found that the diagnosis did not predict: the *shipped*
pluck counter reaches 254-1 904 a game while seat-throws number 1-96. The
corner launcher's two covered seats are usually held by our own brick or
squatter within a few rounds, after which it spends its free action throwing
whatever else wanders into the 8-neighbourhood. That is not worthless (it keeps
reinforcements off the ring) but it is not the -8 HP/round mechanism, and any
future tuning of W3 should count seat-throws, not throws.

# 14. `bots/loki_leap5` — THE PER-WEAPON RESERVATION (2026-08-17)

Fresh fork of `bots/loki_leap3`. `loki_leap` (v156), `loki_leap2`, `loki_leap3`,
`loki_leap4` and every mimic are FROZEN and untouched; everything here is new
code in a new directory behind one flag (`TW_RESERVE_ON`) that leaves the tree
identical to `loki_leap3` when down, apart from `TW_LAUNCH_CAP`.

**Brief: the wave-4 measure agent's recommendation, and it is a correction to
wave 4, not to wave 3.** Three measurements have to be honoured at once:

| | leap3 (wave 3, n=108) | leap4 (wave 4, n=108) |
|---|---|---|
| istones cell | **+4.1pp** (65.9 vs 61.9) | wash |
| games with any weapon | **44 / 108** | 10 / 108 |
| launcher builds / plucks | **57 / 3 712** | 8 / 347 |
| our fwd Sentinels at terminal | 2.17 (vs 2.53 baseline) | 2.44 (vs 2.48 control) |

leap3's gain came from the terminal weapons and its only cost was a small tube
tax. Wave 4's `TW_TUBES_FIRST` put a **global** budget order in front of both
weapons — 2 tubes standing AND ten rounds of their ammunition still affordable
after the buy — and protected the tubes by **cancelling 77-91 % of the thing it
was protecting**. That is not a fix; that is a deletion with a receipt.

## 14.1 The change — one flag, three call sites, and a caller-side split

The order was **right about the second weapon and wrong about the first**,
because the two are not the same purchase:

* **Launcher #1 is the cheap half.** `floor(20 x scale)` **once** — measured
  c=57-88 at the rounds this gate opens — and **zero per round**, for -8 HP/r
  off a ceiling *observed* at 20.05 HP/r in the stall class. It cannot starve a
  tube's ammunition because it consumes no ammunition, and `TW_LAUNCH_TI_FLOOR`
  already holds a tube's own bank floor intact at the moment of the buy.
  Requiring two standing tubes and a 100-Ti magazine reserve of it is what
  emptied the fixture: in the income-poor stall cells those two conditions are
  exactly what is missing, and those are the cells the weapon exists for.
* **Launcher #2 and the gunner are the expensive half.** #2 buys the same
  -8 HP/r for a second scaled price out of the same bank; the gunner buys it for
  a scaled price **plus `TW_GUN_BURN` = 4 ammo/round drawn from the conversion
  pipe the tubes drink from** (H3). These are the bills that land twenty rounds
  later as a conversion the Core declines — the leak 12.6 measured.

So the reservation is **per weapon**. The arithmetic is wave 4's, unchanged
(`_tw_reserve`, ported from `_tw_tubes_first`); what moved is **who calls it**:

| arm | leap3 | leap4 (`TW_TUBES_FIRST`) | leap5 (`TW_RESERVE_ON`) |
|---|---|---|---|
| launcher #1 (`n=0`) | free | gated | **free** |
| launcher #2 (`n>=1`) | free | gated | **gated** |
| `_tw_launch_walk` | free | gated | **gated on the same `n`** |
| gunner | free | gated | **gated**, `burn_extra=TW_GUN_BURN` |

`_tw_reserve_gated(n)` is the whole split: `n` is the launcher census *before*
this build — the same `n` the cap and the survivorship clock already use — so
build `n+1` is gated exactly when `n >= TW_RESERVE_FREE_LAUNCHERS` (1).

The gate itself, unchanged from 13.3: **(a)** `TW_RESERVE_MIN_TUBES` (2) forward
Sentinels **standing** (live census `_tw_tubes`, store as fallback, a body that
cannot count refuses); **(b)** `bank - cost >= max(0, TW_RESERVE_RNDS *
(SIEGE_JIT_SENT_BURN * tubes + own_burn) - ammo)`, i.e. 100 Ti at the binding
two-tube case. Cost: nothing per round; both terms run after every cheaper
refusal in each arm has already returned.

`TW_LAUNCH_CAP` stays at wave 4's **2** (launchers 1-2 are the measured half;
3-4 were sized off the diagnosis's 32 HP/r *theoretical* ceiling against 20.05
observed). `TW_GUN_CAP` stays 1. New marker `TW resv` (one line per body, the
first RELEASE of a gated weapon) plus `TW why w=tubes` / `w=pipe` (probe grade).
**Unlike wave 4's `TW tfirst`, the absence of `TW resv` is not a failure** —
launcher #1 never reaches the test. Read it beside `TW launch`: `TW launch`
present and `TW resv` absent is the cheap half firing and the expensive half
correctly refused, which is the fork working as designed.

## 14.2 Smoke — `tools/leap5_smoke.py`, seed 2

Sixteen games, `results/leap5/smoke.{json,log}`. Every fixture leg was run
against `loki_leap3` **in the same batch and on the same board**, because the
harness is not deterministic under a fixed seed (risk 8) and a leg without its
own control is an anecdote.

| leg | result |
|---|---|
| six stall cells vs `mimic_istones` | leap5 **2/6** wins, leap3 3/6; `TW launch` in **4/6** games (leap3 3/6), 542 plucks (leap3 46) |
| two vs `mimic_0033` | **WIN, WIN**; leap5 TW markers clean |
| vs `starter` | WIN, t=89, `core_destroyed` |
| flags-off `bots/leap5_inert` | **zero TW markers** |
| our tracebacks, all 16 games | **0** |

`TW resv` fired **0/6** here: the gated half was refused in every game while the
free half fired in four, which is the fork doing exactly what it says.

**One marker caveat, pre-existing and NOT ours.** The 0033 leg prints
`TW gunkill` once. `_tw_note_gun_shot` is gated on `TW_ON and TW_GUN_ON` and on
a gunner of ours standing within `TW_CENSUS_DSQ` of their Core — **not** on the
gunner being a *TW* gunner — so any home/CB gunner that finishes a builder bot
near their ring borrows the marker. The leg was re-run with `loki_leap3` as a
control (`gate3` in `tools/leap5_smoke.py`) and **leap3 prints the same line on
the same board**. It is an instrument artefact of leap3's marker vocabulary,
not a leak of this plank; the archetype gate itself (`TW gate`) is silent on
both.

## 14.3 The 60-game paired read — `tools/leap5_pool.py`

Six games prove a plank fires; a tube census is a median. So the full
section-12.6 instrument was run: the ten stall cells x seeds 1-6, leap5 AND
leap3 in the same invocation, 60 games each
(`results/leap5/full.json`, `full2.json`).

| | `loki_leap5` | `loki_leap3` | wave-4 `loki_leap4` |
|---|---|---|---|
| **our fwd Sentinels at terminal** | **2.25** | 2.15 | 2.44 |
| paired tubes delta | **+0.10** (24 up / 17 down) | — | -0.05 |
| games with any weapon | **34 / 60** | 28 / 60 | 10 / 108 |
| launcher builds / plucks | 38 / **4 516** | 47 / 3 319 | 8 / 347 |
| gunner builds | **0** | 15 | 5 |
| **wins** | **30 / 60** | **41 / 60** | — |
| cells improved / unchanged / regressed | **0 / 4 / 6** | — | — |

**Both mechanism targets were hit and the outcome column went the wrong way.**

* The tube tax is **gone**: 2.25 against leap3's own 2.15 on the same boards
  (its wave-3 figure was 2.17, so the instrument is calibrated), paired +0.10.
* The mechanism is **alive**, which is the whole difference from wave 4: 34/60
  games armed and 4 516 plucks, against leap4's 10/108 and 347.
* And leap5 wins **30/60 against leap3's 41/60**, with **no cell improved and
  six regressed** — concentrated in `synth_f_royale_moved_A` (1/6 vs 5/6) and
  `synth_d_30x30_vertical_A` (0/6 vs 3/6).

**The noise floor, measured rather than assumed** (`tools/leap5_noise.py`).
leap5 and leap3 differ only on paths a weapon build attempt reaches, so in a
game where **neither** arm ever built one the two directories are the same bot:

```
NEITHER arm built a weapon  n=16  leap5  9 wins  leap3 10 wins   <- noise floor
at least one arm armed      n=44  leap5 21 wins  leap3 31 wins
```

One game of drift where the bots are identical, ten where they are not. **The
regression is the plank, not the harness.** Verdict: **REJECT as configured.**

## 14.4 Which half? — the ablation, `tools/leap5_arms.py`

Two frozen variants, stamped with `tools/leap_variant.py --src loki_leap5` and
run **in one invocation with each other** on the same ten cells x seeds 1-3
(`results/leap5/abl.json`), because only a within-invocation delta means
anything on this instrument (RESUME, wave-5 method note):

* `bots/leap5_cap4` — `TW_LAUNCH_CAP=4`, i.e. wave 4's cap import withdrawn;
* `bots/leap5_gunfree` — `TW_RESERVE_GUN=False`, i.e. the gunner back on
  leap3's conditions and only launcher #2 reserved.

| arm (30 shared cells) | wins | kills | tubes@term | w/weapon | launch | gun | plucks |
|---|---|---|---|---|---|---|---|
| `loki_leap3` (reference) | **22/30** | 17 | 2.13 | 15 | 25 | 9 | 2 458 |
| `leap5_cap4` | 19/30 | 13 | 2.23 | 16 | 19 | 2 | 930 |
| `leap5_gunfree` | 19/30 | 12 | 1.97 | 11 | 11 | 6 | 1 459 |
| `loki_leap5` (shipped config) | **15/30** | 14 | **2.40** | 19 | 22 | **0** | 2 608 |

**Neither half is the culprit on its own, and the pair is worse than either.**
Both ablations land on 19/30 — indistinguishable from each other, each about
half way back to leap3 — so the loss is not "the cap import" and not "the
gunner went to zero"; it is both, and the two are roughly additive. Read with
`kills`: leap5 keeps the plucking (2 608, the most of any arm) and loses the
**kills** (14 against leap3's 17) while holding the most tubes (2.40). That is
the wave-3 lesson restated from the other side — *the ceiling is not the
binding constraint* — and it is now measured twice: taxing the tubes to buy
seats was a wash (12.6), and protecting the tubes at the cost of the gunner and
of launchers 3-4 is worse than a wash.

The one number worth carrying forward: in leap3's own 60 games the class that
built a **gunner** won 77 % (n=13) against 67 % for launcher-only (n=15) and
66 % for no weapon at all (n=32). The gunner is the half that was paying, and
`TW_RESERVE_GUN` prices it out — `TW_GUN_TI_FLOOR` (40) **plus** a reservation
of `10 x (5 x 2 + 4)` = **140 Ti**, which the stall class never holds.

## 14.5 Verdict and residual risks

**REJECT as configured.** `loki_leap3` remains the best fork and the reference.
The flag is left **ON** rather than flipped down, because this directory *is*
the measured configuration and flipping it would make `bots/loki_leap5` no
longer the thing section 14 reports; `TW_RESERVE_ON=False` restores leap3
behaviour apart from `TW_LAUNCH_CAP`, and `bots/leap5_inert` is the flags-off
control that verified it (zero TW markers).

Risks that stood, and one that did not:

1. **Pre-registered risk (doctrine.py, `TW_RESERVE_ON`): the freed launcher #1
   re-imports the tube tax.** It did **not** — tubes 2.25 vs 2.15, paired
   +0.10. The split was real; the launcher is genuinely the cheap half.
2. **Unstated and it bit: `TW_RESERVE_GUN` is not a small extra term, it is a
   deletion.** 15 gunner builds -> 0 in 60 games. Any future use of this gate
   must price the gunner separately from launcher #2 or exempt it, and must
   carry `gun_builds` as a ship blocker the way wave 4 should have carried
   `launch_builds`.
3. **`TW_LAUNCH_CAP` 4 -> 2 was carried in unmeasured**, on wave 4's reasoning
   rather than its own evidence, and it cost about as much as the gunner gate
   did. It is a second change in a fork billed as one; 14.4 is the only place
   it has ever been measured on its own, and it reads negative.
4. **Instrument, unchanged from every previous wave**: a (map, side) cell is
   nearly deterministic and the effective n of this fixture is the **cell**
   count (10), not the game count. The 0/4/6 cell split and the measured noise
   floor (14.3) are why the verdict is stated at all; a 30-game win column on
   its own would not carry it.

# 15. `bots/loki_leap6` — THE SLEIPNIR PORT: SAMESTOP + BODYAWARE (2026-08-17)

Fresh copy of `bots/loki_leap5` carrying **two of Moonfarm's planks** out of
`bots/mate_sleipnir` (v155): **SAMESTOP (QUEUE #50)** and **BODYAWARE (#63)**.
Everything else in this tree is `loki_leap5` byte-for-byte. `loki_leap`,
`loki_leap2..5`, `mate_sleipnir`, `mate_v154` and every mimic are FROZEN and
were not touched; `bots/loki_leap6/raid.py` is `diff`-identical to leap5's.

Executed exactly to the six-step table in `analysis/team_bot_recommendation.md`
§3b, which was itself verified line-by-line before the port. The three
identity claims that made this a copy rather than a merge were re-verified
here before any edit, on the actual files:

| function in `eco.py` | turbo4 vs leap5 | leap6 vs mate_sleipnir |
|---|---|---|
| `_bfs_direction` | **byte-identical** (160 lines) | identical + the gate below |
| `_link_path` | **byte-identical** (145) | **byte-identical** |
| `_wire_on_build` | **byte-identical** (8) | **byte-identical** |
| `_samestop_plan/_stand_pref/_arm/_fire` | n/a | **byte-identical** (all four) |
| `_expand` | 1 line differs (leap5's `ARCH_BLEED_MASK` store read) | +22, the two hooks only |

## 15.1 What was changed, per §3b

1. **`_bfs_direction` -> Sleipnir's two-pass version, verbatim** (160 -> 194
   lines), carrying Sleipnir's own `HAND-MERGED BLOCK` header comment intact.
2. **`_wire_on_build` -> Sleipnir's** (8 -> 14), adding the `_samestop_arm(ct,
   bp, plan)` call and the `plan` local it shares with `self.link_queue`.
3. **The four `_samestop_*` methods pasted verbatim** (+106), in Sleipnir's own
   position: after `_wire_tick`, before `_build_next_link`.
4. **Two `_expand` hooks**, the only hand-placed lines in the port. Both hook
   *bodies* were sliced out of Sleipnir's `_expand` programmatically rather
   than retyped, so the inserted text is verbatim; only the anchor placement
   was chosen by hand, and both anchors are unchanged from turbo4:
   * `if self.samestop_pending is not None and self._samestop_fire(ct): return`
     as the FIRST statement under `if ct.get_action_cooldown() == 0:` — before
     any move, and before the `_build_next_link` line;
   * the ore stand-tile preference immediately before the closing
     `self._nav(ct, pave=allow_pave)`.
5. **`main.py`: the three per-unit attrs** (`samestop_pending`,
   `samestop_plan_key`, `samestop_plan_cache`) with Sleipnir's comment, in
   Sleipnir's position (after `hs_seek_seat`). This is the ONLY change to
   `main.py`; `diff` against leap5 is those 8 lines and nothing else.
6. **`doctrine.py`: `LOKI_SAMESTOP_ON = True`, `LOKI_SAMESTOP_LOG = False`**
   plus Sleipnir's doc block verbatim, and Sleipnir's two `composed by` /
   `hand-merged by` marker lines **carried over intact, not rewritten** —
   §4a of the recommendation records that `tools/dash/serve.py`
   (`_COMPOSED_FROM_RE`) and `tools/auto_gate.py` (`combo_of`) on the
   teammate's side require that phrasing verbatim. A third marker line for
   leap6 is added ABOVE them rather than editing either.

`LOKI_SAMESTOP_LOG` is **False** here on purpose (Sleipnir ships it True): it
prints one line per same-stop build. `bots/leap6_log` is the probe tree that
carries it True, so this directory never has to be edited to instrument it.

## 15.2 The one deviation from Sleipnir: `LOKI_BODYAWARE_ON`

**Sleipnir ships BODYAWARE ungated and unflagged** — checked, there is no
`LOKI_BODYAWARE_ON` anywhere in `bots/mate_sleipnir/`, and the plank is fused
with SAMESTOP into one bot, which is exactly why §3b asks for the ablation
("nobody has ever measured which of the two carries the gain"). So leap6 adds
the flag. It is the **only** functional deviation from the Sleipnir source in
the whole port, and it is one condition on one line:

```
elif et == EntityType.BUILDER_BOT and LOKI_BODYAWARE_ON:
```

That branch is the plank's sole entry point, and gating it there — rather than
skipping pass 0 — is what makes flag-off *exactly* the parent instead of an
approximation of it. With the flag down: `bodies` stays empty, so pass 0 stamps
nothing extra into `st`; `if _pass == 1 and not bodies: break` exits before
pass 1 does any work; and both `continue`s fall through to the same
`p.cardinal_direction_to(target)` the parent returned from those points.
`BUILDER_BOT` is **not** in `BFS_BLOCKING_TYPES`, so falling down the `elif`
chain leaves bodies unblocked, as in leap5. Claim, not argument — see 15.4.

## 15.3 Store slots and the AST sandbox

* **Zero store-slot traffic added.** `read_store` 10 and `write_store` 4 in
  `eco.py`, identical counts to leap5, and no `store` reference exists anywhere
  in the ported block. leap5's slot-15 sole-writer lanes (`COLLAR_SPENT_SLOT`)
  are untouched, as §3b predicted.
* **`bare except` 0, `try/finally` 0** across all four files, by `ast` walk, in
  leap6 exactly as in leap5. The ported code uses `except Exception` only.

## 15.4 Smoke — `tools/leap6_smoke.py`, seed 2, 12 games + 5 legs

Six big-map cells vs `mimic_istones`, leap6 and leap5 paired on the SAME cells:

| cell | loki_leap6 | loki_leap5 |
|---|---|---|
| auroraveil A | **STALL** t=1000 | win t=167 |
| auroraveil B | win t=128 | win t=152 |
| glacierkeep A | win t=460 | win t=341 |
| glacierkeep B | win t=324 | **STALL** t=1000 |
| midgard A | win t=184 | win t=393 |
| midgard B | win t=444 | win t=85 |
| **totals** | **5/6 wins, 1/6 stalls** | **5/6 wins, 1/6 stalls** |

Read this as "nothing exploded", not as a result: n=6 cells, the two stalls are
on *different* cells, and §4b's own warning is that a (map, side) cell is
nearly deterministic and run-to-run drift is the size of any effect this size.
It does not clear, and is not meant to clear, §3b's pre-registered bar.

Other legs, all clean: `mimic_0033` nordkap A **win** t=185 and antler B **win**
t=231; `starter` midgard A **win** t=154. **Zero tracebacks out of
`bots/loki_leap6/` on any leg** (and zero out of the opponents).

**The plank fires, at Sleipnir's own rate.** `mate_sleipnir` already ships
`LOKI_SAMESTOP_LOG = True`, so the reference count was free
(`tools/leap6_ss_rate.py`, same six cells, seed 2):

| cell | `leap6_log` SS50 | `mate_sleipnir` SS50 |
|---|---|---|
| auroraveil A / B | 1 / 7 | 1 / 4 |
| glacierkeep A | 4 | 4 |
| midgard A / B | 7 / 7 | 5 / 6 |
| nordkap A | 9 | 4 |
| **total** | **35 over 6 games, 6/6 games >= 1** | **24 over 6, 6/6 >= 1** |

Different bots, so this is an order-of-magnitude check, not an equality test —
but a hook that had landed in the wrong place would read ~0 against 24, and it
reads 35. The single marker in the first smoke probe was the *cell*, not the
port: auroraveil A is a 1000-turn stall for both trees.

**Flag-off identity, the ablation contract.** `bots/leap6_off` (both new flags
down) vs `mimic_istones` on midgard A seed 2, against `loki_leap5` on the same
cell: turns 393 = 393, `core_destroyed` = `core_destroyed`, and the per-round
trajectory hash (our units/buildings/core-HP and theirs, every state)
**`c569801425cc` == `c569801425cc`**. Bit-for-bit the same game. The gate is
exact, not approximately exact.

### 15.4a Each flag is individually live — and one accidental drift measurement

A second, independent invocation on the same cell (midgard A, seed 2, vs
`mimic_istones`), all five trees run inside ONE invocation so the load is
shared:

| tree | turns | trajectory hash | vs leap5 |
|---|---|---|---|
| `loki_leap5` | 285 | `db5bf56c950d` | — |
| `leap6_off` | 285 | `db5bf56c950d` | **identical** |
| `leap6_ss` (SAMESTOP only) | 240 | `142d149fe34e` | differs |
| `leap6_ba` (BODYAWARE only) | 195 | `12836b009ac5` | differs |
| `loki_leap6` (both) | 151 | `5baad4ae991e` | differs |

Two things fall out:

1. **Both flags are live, and each on its own.** `leap6_ss` and `leap6_ba` each
   diverge from the parent, so neither ablation arm is a no-op — the ablation
   in 15.6 can actually separate the planks. And `leap6_off` reproduces the
   parent exactly for the **second** time, in a different invocation, which is
   the claim 15.2 rests on.
2. **Do not read the turn counts as a result.** `loki_leap5` on this exact
   cell read **393 turns / hash `c569801425cc`** in the 15.4 invocation and
   **285 / `db5bf56c950d`** here. Identical bot, identical map, side, seed and
   opponent — the difference is machine load across invocations (parallel game
   count differed), i.e. §4b's "run-to-run drift is the size of the effect",
   reproduced by accident. Only paired, same-invocation deltas are quotable
   from this fixture, which is exactly why `leap6_off` == `loki_leap5` is
   stated as a within-invocation identity and never as a turn count.

## 15.5 CPU — `tools/wave5_cpu.py`, `CPU_BOTS=loki_leap5,loki_leap6`

nordkap, 150 timed rounds/scenario. (The tool's hardcoded column labels say
"turbo4/leap"; here they are leap5/leap6.)

| scenario | leap5 p95 | leap6 p95 | median ratio |
|---|---|---|---|
| core | 12.2 us | 12.4 us | 1.01x |
| home | 166.6 us | 186.2 us | 0.95x |
| ring | 38.1 us | 51.8 us | 1.03x |
| ring$ | 88.4 us | 67.4 us | 0.99x |
| turret | 5.7 us | 5.7 us | 1.00x |

**Worst p95: leap6 186.2 us = 1.86 % of the 10 000 us budget** (leap5 1.67 %),
ratio 1.12x. §3b's guard was < 5 %; it holds with room. The second BFS pass
does not double anything, because pass 1 only runs when pass 0 exhausts —
measured, as §3b insisted, not assumed. `ok` on every scenario for both bots
(no BROKEN rows, controller-call counts equal: 46 / 251-252 / 125 / 153 / 27).

## 15.6 The variants built alongside

All are full copies of `bots/loki_leap6` differing from it by **exactly one
line** of `doctrine.py` (`diff -r` verified), and all `py_compile` clean:

| dir | change | question it answers |
|---|---|---|
| `bots/leap6_ss` | `LOKI_BODYAWARE_ON = False` | does SAMESTOP carry the gain alone? |
| `bots/leap6_ba` | `LOKI_SAMESTOP_ON = False` | does BODYAWARE? |
| `bots/leap6_nocol` | `COLLAR_ON = False` | §3c: the v156 collar *degrades* seat denial — Sleipnir holds 4.06 seat buildings at r100 with no collar at all, v156 scores 2.55. This tests whether leap6 is better off dropping our own plank. |
| `bots/leap6_off` | both new flags `False` | the flag-off control; used for the 15.4 identity check |
| `bots/leap6_log` | `LOKI_SAMESTOP_LOG = True` | instrumentation probe only — never field this |

## 15.7 What has NOT been done, and the standing risks

1. **§3b's pre-registered bar has not been run.** That is the 45-map / 3-rep /
   mirror-control panel plus the 13-big-map additivity test (leap6 must beat
   BOTH parents' stall rates — under 8/52 and under 2/52 — or the two planks
   are redundant, not additive). Nothing in 15.4 substitutes for it, and the
   honest reading of 15.4 is "no signal at this n".
2. **`tools/crashtest.py loki_leap6 mimic_istones --synth` (42/42) has not been
   run** — the other §3b guard.
3. **Attribution and slot risk are unchanged (§4a).** leap6 is our bot carrying
   two of Moonfarm's planks. `fcode submission upload` AUTO-ACTIVATES and would
   displace Moonfarm's live v155 mid-run; that needs Moonfarm's agreement and
   the user's approval, separately. Nothing here was uploaded, and no
   `fcode submission` command of any kind was run.
4. **The `_expand` hooks are the only hand-placed lines**, so they are the only
   place a future leap5-side change can silently collide. Both anchors
   (`if ct.get_action_cooldown() == 0:` + the `_build_next_link` line, and the
   trailing `self._nav(ct, pave=allow_pave)`) were unique in the file at port
   time; a rebase must re-check that.
5. **Aug 20 rotation**: leap6 inherits leap5's map knowledge the same way
   (`eco.py known_map_for` + 3 MAP codes, no `maplib.py`), so
   `ROTATION_AUG20.md` step 4 does not apply to it — but steps 2, 3 and 5 do,
   for leap6 and every mimic in its panel.
