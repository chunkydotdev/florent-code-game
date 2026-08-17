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
