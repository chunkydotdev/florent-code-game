# `bots/loki_leap18` -- WAVE 22 INTEGRATION BUILD (five arms, all masters ON)

**This tree is `bots/loki_leap16` (the wave-19 head, `PLAN.md` §1.2 else-branch) plus the five
wave-22 arm diffs, each behind its own master flag.** It is the PLAN §3.3.6 **stage-3
integration** build: the measurement that catches arms cancelling each other.

| flag | arm | module | state |
|---|---|---|---|
| `OPEN_ON`   | A1 INTEGRATED OPENING            | `opening.py` | **True** |
| `RING_ON`   | A6 RING-CLAIM + EVICT-AND-REPLACE | `ring.py`    | **True** |
| `GD_ON`     | A2 GUN DISCIPLINE                 | (in `main.py`/`raid.py`) | **True** |
| `SIPHON_ON` | A4 OFFENSIVE SIPHON TAP           | `sip.py`     | **True** |
| `END_ON`    | A5 TITANIUM-TIEBREAK ENDGAME      | (in `main.py`/`eco.py`/`raid.py`) | **True** |

`CB_READY_ON` (arm A3, COUNTER-BATTERY) **is not in this tree at all** -- KILLED by
`PLAN.md` AMENDMENT 2026-08-18 §A1 on `results/wave22/cb_verdict.md`.

**All five arm `*_LOG` flags are False** (`OPEN_LOG`, `RING_LOG`, `GD_LOG`, `SIPHON_LOG`,
`END_LOG`) per PLAN §1.5. The **base lineage** `*_LOG` flags are left at their `loki_leap16`
/ `leap15_kfix` (v161) values, unchanged: altering them would be an un-flagged behavioural
change outside any arm and would stop `bots/loki_leap18_off` restoring `loki_leap16`.

Twins:

* `bots/loki_leap18_off` -- all five masters `False`. Inertness leg; restores `loki_leap16`
  modulo unreachable blocks.
* `bots/loki_leap18_dbg` -- all five masters `True` **and** all five arm `*_LOG` flags `True`.
  Marker-firing check only; **never** a verdict cell.

## Conflicts resolved during integration (apply order: open -> ring -> gd -> sip -> end)

1. **`main.py` class bases / imports** -- each arm added its own mixin. Merged to
   `class Player(EcoMixin, RaidMixin, OpenMixin, RingMixin, SipMixin)`. Verified: the three
   mixins share **no method name** with each other or with the 261 base methods, so the MRO
   order carries no behaviour.
2. **`main.py` action rank point (A1 prefill/trunk vs A6 refill/evict)** -- both arms ranked an
   own-socket action immediately after `_wire_tick`. **A1 runs first**, on a deadline argument:
   the prefill's registered bar is "= 2 @r10 on >= 2 faces" occupied by r3 (`PREFILL_RND`), so a
   round lost fails a bar outright, while A6's refill window is 5 rounds and its evict is a
   20-round peck campaign. The pre-emption window is empty in practice (A1 can only claim the
   turn r0-r3; A6 needs an enemy building already standing on our socket, first recorded r7).
   Composition is by design: `RING_FLOOR_OWN` is an **absolute** census of own buildings on own
   sockets, so A1's two prefill conveyors **are** two ring claims and A6's untriggered floor is
   already satisfied -- A6 lays nothing further until its own trigger fires.
3. **`main.py` `_sh_pick_seat` body ban (A1 vs A6)** -- the same wave-20 M3 finding shipped
   twice with different scope. **Both vetoes applied**: A6 `_ring_station_ok` (all 8 sockets,
   SOFT -- stands down with no filled alternative), A1 `_op_seat_filled` (the 2 prefill sockets
   only, HARD). Cannot strand the caller: `_sh_pick_seat` already returns `None` legally, and
   A1's hard half covers only 2 of 8 sockets so A6's soft fallback keeps the other 6.
4. **`main.py` dangling `CB_RESERVE` (A1)** -- the amendment's named must-fix. `_op_reserve` is
   **deleted** (not zeroed, so no later edit can re-arm a reserve for a dead arm) and the
   cap-lift gate is now **`bank >= builder cost`**. `CB_RESERVE_EXTRA` survives in `doctrine.py`
   as the record and is read by nothing.
5. **`doctrine.py` `SIP_RESERVE_ON` (A4)** -- the *second* dangling `CB_RESERVE` reference. Its
   comment instructs a stage-3 integrator to flip it `True` "where A3 exists". A3 does not
   exist. **Stays `False`**; the ruling is recorded at the constant.
6. **`main.py` A4 SIPHON vs A5 END_QUIT** -- a real conflict. A5 ARM 1 retires the forward tree
   with one test at the top of `_raid`, but A4's hook sits **above** the role split, so an
   un-gated tapper would stand in the enemy ore field for the last 300 rounds. **A5 outranks**:
   the tap hook is gated on `not (END_ON and END_QUIT_ON and self._end_fired(ct))`. Cost is
   near zero -- a *completed* tap is a building and keeps yielding with no body present (83 of
   112 corpus taps outlived their builder); only an incomplete chain is abandoned, and that
   delivers nothing either way. The gate can only make A4 smaller, never larger.
7. **`doctrine.py`** -- all five arm blocks are pure appends with **zero** symbol collisions
   against each other or the base. Concatenated in apply order.
8. **Comm** -- zero new slots. A1 writes only slots 4/5/8, which already have those writers;
   A6 and A4 are zero-comm; A5 takes bit 28 of slot 9, guarded on `not SG_ON` (`SG_ON` is
   `False` here). `eco.py` and `raid.py` merged with no conflicts in any arm.

---

# WAVE 22, ARM A1 -- THE INTEGRATED OPENING (`OPEN_ON` = True)

This tree is `bots/loki_leap16` (the wave-19 head) plus ONE new flag and its module,
`opening.py`. Ticket: `analysis/wave22/PLAN.md` 2.1. Design: `analysis/wave22/OPENING.md`.
Every wave-20 master (`SR_*`, `EF_*`, `AB_*`, `RFC_*`) is absent, per `results/wave20/DECISION.md` 6(b).

* `bots/leap18_open` -- `OPEN_ON = True`, `OPEN_LOG = True` (arm A1).
* `bots/leap18_open_off` -- the inertness twin: byte-identical apart from those two flags.

The whole rationale, constant by constant, is the `WAVE 22, ARM A1` block at the end of
`doctrine.py`; the mechanism is documented in the `opening.py` module docstring. `A2_ECO`
is present as a flag and is **False and unimplemented here** -- it is `bots/leap18_a2eco`,
its own arm and its own A/B (PLAN W6 / F7.4). Nothing in this tree spends the
counter-battery reserve; arm A3 (`CB_READY_ON`) is a separate build.

`OPEN_LOG` prints `OP band=`, `OP prefill`, `OP capliftr=`, `OP feeder`, `OP pair`. It is
measurement scaffolding and **must be False in any build that reaches a verdict cell**
(PLAN 1.5).

---

# WAVE 22, TRACK 3 -- PLANK RING: RING-CLAIM + EVICT-AND-REPLACE (`RING_ON` = True)

This tree is `bots/loki_leap16` (the wave-19 head, `PLAN.md` 1.2 else-branch) plus ONE new flag
and its module, `ring.py`. Evidence: `analysis/wave22/0033_losses.md` §1 (the mechanism) and §3.1
(the arm it registers). Engine argument: `analysis/wave22/OPENING.md` §4, contradiction X2.
Every wave-20 master (`SR_*`, `EF_*`, `AB_*`, `RFC_*`) is absent, per `results/wave20/DECISION.md` 6(b).

* `bots/leap18_ring` -- `RING_ON = True`, `RING_LOG = True`.
* `bots/leap18_ring_off` -- the inertness twin: byte-identical apart from those two flags.

**The loss this answers.** RING-SEAT FORFEITURE. Median 3.8 of our 8 core sockets empty every
turn, ~1.6 more held by one of our own BODIES (260 body-turns/game), 65 distinct enemy buildings
on our sockets over 15 ladder games of which we cleared **3 (4.6 %)**, 5 still standing there at
the end of the median game. 0033 leaves 0.3 sockets free and clears 34 % of the bricks on its own.

**The three arms, one flag.**

| arm | what it does | the bound that keeps it honest |
|---|---|---|
| 1 RING-CLAIM | our own CONVEYORS onto our free sockets, cheapest-first, when an enemy non-builder is forward of the midline or an enemy building lands within 4.0 of our core; plus an unconditional floor of 2 beyond the standing count by r20 | chain guard, `_eco_spendable` + `RING_TI_FLOOR`, `RING_MAX_PER_UNIT`, and a census-based team ledger |
| 2 EVICT-AND-REPLACE | at most 2 adjacent bodies peck a brick off one of our 8 sockets, and our conveyor goes back on the tile the round it dies | the peck **refuses itself** unless the 3 Ti retake is funded -- clear+retake only, never clear |
| 3 BODY BAN | SEATHOLD stations on FILLED sockets only | SOFT: with no filled seat available the parent's choice stands, so the ban can never hand the seat over faster |

**Conveyors and only conveyors, on our own sockets.** OPENING.md §4 settles X2 from the engine
(§G passable = empty/ore/conveyors+splitters of either team; §N.10 stacks pass under bodies; §N.9
heal is strictly `d^2 == 1`) and from a 60-game measurement (772 of 2 332 own-socket core heals came
from a body standing on its own conveyor; **0** from a body on its own barrier, harvester or turret,
all three impassable). A socket carrying our conveyor is a delivery terminus, a tile the enemy can
never build on, and a live heal seat, all at once. Nothing in this tree places a barrier, a
harvester or a turret on one of our eight sockets.

**No new comm slot** (PLAN 1.5): the eviction cap is an id ballot among the bodies orthogonally
adjacent to the target, the claim ledger is censused off the buildings that are standing, and the
refill intent lives on the unit that pecked. Every occupancy test is `get_tile_building_id` /
`get_tile_builder_bot_id`, never `is_tile_empty` (P0-B). Sandbox: no bare `except`, no
`try`/`finally`, a typed fallback on every `ct.*` call.

`RING_LOG` prints `RING claim`, `RING evict`, `RING refill`. It is measurement scaffolding and
**must be False in any build that reaches a verdict cell** (PLAN 1.5).

Falsifiers are pre-registered in `analysis/wave22/ring.md` and were written before the arm ran.

---

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

---

# 16. PLANK SOCKET-GUARD — loki_leap7, 2026-08-17

`bots/loki_leap7` is `bots/loki_leap6` plus one plank in five separately-flagged
arms. Everything below is gated on `SG_ON`; with it `False` the tree is leap6.

## 16.0 The attack, in one paragraph

`analysis/launcher_meta.md` (fresh corpus, 505 games, all opponents ≥1800)
identifies exactly one mechanism behind our current ladder losses, and both
Juusto v13 (v155 10–15) and gsxWins v53 (v155 2–13) run it. A builder of theirs
reaches our base by turn ~14 — Juusto ferries it (build launcher → throw its own
builder r²≤26 → self-destruct, which refunds the +10 % scale; 325 launchers, 321
throws, **100 % own bots, 100 % recycled**, median 2 rounds alive, 5.7 tiles a
hop), gsxWins walks it in behind a turn-9 gunner. It then plants **3-Ti
barriers** on the eight tiles orthogonally adjacent to our 2×2 Core — the
**sockets** — which per `engine_mechanics` §B are the only tiles a conveyor can
deliver into the Core from, and it kills the one conveyor we have plugged in.
Because a conveyor whose output tile is empty ground **holds its stack forever
and blocks everything upstream**, killing that one tile does not slow our
economy, it stops it.

| ours vs Juusto | 10 wins | 15 losses |
|---|---|---|
| feeder conveyors on sockets | **2.25** | **0.45** |
| enemy buildings on sockets (mean / max) | 2.43 / 3.5 | **4.78 / 6.4** |
| rounds with ZERO feeder | 15.6 % | **72.4 %** |
| core deliveries | 131.6 | 22.9 |
| our Ti→ammo | **619** | **89** |

Ti→ammo separates the results perfectly at ~300: **0/15 below, 10/10 above**.

## 16.1 What was implemented

| arm | flag | where | mechanism |
|---|---|---|---|
| 1a face-diverse trunk | `SG_TWO_FEEDERS` | `eco._link_path`, `eco.delivery_seats` | the incumbent flood re-run against the Core's requested socket/face; accepted only within `SG_FEED2_DETOUR` extra links |
| 1b harvester stub | `SG_STUB_ON` | `eco._sg_rebuild` | one conveyor on a free socket a harvester of ours already touches = a whole second line |
| 2 self-fill | `SG_SELF_FILL` | `eco._sg_fill` | our own 3-Ti bricks on the two sockets of the face nearest THEIR Core |
| 3 feeder rebuild | `SG_FEEDER_REBUILD` | `main._core`, `eco._sg_rebuild(_walk)` | Core censuses its own eight sockets, publishes a 4-bit request; builders answer it as the top economy priority |
| 4 corner launcher | `SG_CORNER_LAUNCHER` | `main._try_build_launcher`, `main._sg_launch_walk`, `raid._launcher_turn` | ONE launcher on a ring **diagonal corner** under S3, evicting every round |
| 5 ring turret | `SG_RING_TURRET` | `main._sg_ring_gun` | one gunner one tile OUTSIDE the ring under S3 |

**A conveyor cannot fork.** It has one output tile and accepts from its other
three sides (`engine_mechanics` §B), so the "spur off the trunk" the brief asks
for cannot receive anything without re-facing a trunk link — which breaks the
line it forked from — or a splitter, which nothing in this tree builds and
nobody in 280 games has built. Face diversity is therefore bought the only two
ways the engine allows: **route the second whole chain** to an unfed face (1a,
zero titanium) and **one-tile stub off an existing harvester** (1b, 3 Ti).

**The store.** One field, no new traffic: slot 9 (`SLOT_HEAL_BUDGET`) bits
28–31, free since the merge and **Core-written only**, which is what DOCTRINE §6
records. The Core already writes that word every round. Four bits, three
meanings — `0` stand down, `1–8` an **actionable** socket index+1 (one of our
belts already points into it, or one of our harvesters already touches it;
a body may walk to it and build on it), `9–12` a **face index+9 routing hint**
(no body walks to it, no body builds on it). That split is not decoration: see
16.3. Bits 0–15 stay the bleed beacon, 16–27 the archetype; the three cannot
collide. **`bare except` 0, `try/finally` 0** across all four files, by `ast`
walk.

**The launcher is leap5's mechanism, re-sited.** leap5 built 73 launchers across
155 ladder sides, **0 before turn 100** (median turn 255), median 8.3 tiles from
our own Core — outside the r²≤2 pickup disc of anything that mattered — for **8
throws total**. `_launcher_turn`'s exile code is unchanged; what changed is the
tile (a ring corner, orthogonally adjacent to two sockets), the clock
(`SG_LAUNCH_MIN_RND` 10 instead of `LAUNCHER_MIN_RND` 160), the trigger (the
detector's S3 stamp, slot 13 bits 10–19, already written by every unit that sees
an enemy builder within d≤8 of our Core), and two refusals on the landing tile
(never within `SG_THROW_CLEAR_DSQ` of one of our own buildings — a body dropped
beside our feeder simply pecks it instead — and never back inside
`SG_THROW_MIN_DSQ` of our own Core).

## 16.2 Markers and the mechanism tool

`SG launch` / `SG evict` / `SG gun` / `SG fill` / `SG rebuild` / `SG feeder2`,
all under `SG_LOG` (local replays only — the platform strips stdout).
`tools/sg_mechanism.py` decodes, per game: live feeders over time (a conveyor on
a socket **facing a footprint tile**; any other facing delivers nothing and is
not counted), faces fed, rounds with zero feeder, enemy buildings on our
sockets, our own bricks, Ti→ammo and the ≥300 verdict, evictions, and enemy
builder-rounds spent on our 12-tile ring.

## 16.3 Three defects this batch found and fixed — all of them self-inflicted

These are the reason the arms are as narrow as they are. Each was measured, not
anticipated.

1. **Self-fill bricked our own trunk's terminus.** nordkap seed 2: the arm laid
   bricks on sockets 2, 5 and 6 at turns 9/17/18 while the trunk was still three
   conveyors short of the ring; the chain then had nowhere to terminate and the
   game finished with **0 titanium delivered** and the feeder count never
   leaving zero. Fix: the arm cannot open until at least one feeder is **live**,
   never touches a socket one of our belts points into or one of our harvesters
   touches, and never takes the last free socket of an unfed face.
2. **The routing hint biased the FIRST chain.** glacierkeep is 9 conveyors from
   the nearest ore (r² = 89). Biasing chain #1 onto a chosen face cost enough
   extra links that the bank hit 2 Ti at turn 31 with the line still
   unconnected — **23 conveyors laid, 0 delivered, 0/2 games**, against leap6's
   15 conveyors, connected turn 61, 2/2. Fix: the hint (values 9–12) is
   published **only once a feeder is live**, so arm 1a can only ever see the
   *second* chain, and `SG_FEED2_DETOUR` dropped 6 → 3.
3. **The ring turret was bought before the line that pays for it.** Same map:
   a gunner at turn 17 is 30 Ti plus +10 % on every conveyor still to be laid.
   Fix: `_sg_ring_gun` runs the socket census with its own eyes (the defender
   stands at home) and refuses while we hold no live feeder.

A fourth, narrower one: the first cut let a body **walk** to any requested
socket, and in the opening every face is unfed, so the request never cleared and
bodies oscillated between the doorstep and the ore. That is what the
actionable/hint split in 16.1 exists for, on top of a per-request walk budget
(`SG_REBUILD_WALK_RNDS` 12) and a per-body lifetime cap
(`SG_REBUILD_WALK_CAP` 36).

## 16.4 Smoke — `tools/leap7_smoke.py`, seed 2

**`NOISE_ON` is `True` in this tree**: the Core re-rolls its spawn dispersion
from OS entropy every match, so the same bot on the same map and seed is **not
reproducible** — repeated leap6 runs on one cell ranged from 40 to 5300
titanium collected. Nothing below is a measurement; single cells are noise and
only the batch aggregate is worth reading.

12 leap7 games + 12 paired leap6 controls + 1 inertness leg, 2 repeats per
cell. **0 tracebacks out of either tree**, and `bots/leap7_off` emitted **zero**
`SG` markers.

| leg | leap7 | leap6 |
|---|---|---|
| vs `mimic_0033`, 4 cells x2 | **8/8 wins**, Ti collected 1912 | 6/8, 929 |
| vs `mimic_istones`, 2 cells x2 | 3/4 wins, Ti collected 4092 | 3/4, 2172 |
| per cell (leap7 \| leap6) | antler_B 2/2\|2/2, glacierkeep_B 2/2\|1/2, midgard_A 2/2\|1/2, nordkap_A 2/2\|2/2, auroraveil_A 1/2\|1/2, midgard_B 2/2\|2/2 | |

Every arm fires: `SG launch` 8 (7/12 games), `SG evict` 138 (3/12),
`SG gun` 3 (3/12), `SG fill` 3 (3/12), `SG rebuild` 1 (1/12).
**`SG feeder2` fires 0 times, and that is structural, not a bug** — arm 1b
needs a harvester of ours orthogonally adjacent to a socket, and
`engine_mechanics` §A records that *none of the 15 competition maps has ore
orthogonally adjacent to a core footprint*; only an antler-shaped map (nearest
ore r²=4) can ever satisfy it. Arm 1b is close to dead code on the real map
pool and arm 1a carries face diversity alone.

### The chain, decoded — `tools/sg_mechanism.py`, same 24 games

This is the part worth reading: it measures the mechanism rather than the
scoreboard, and it moves in the right direction on every axis.

| | leap7 | leap6 |
|---|---|---|
| live feeders, mean over rounds | **2.45** | 2.25 |
| faces fed (max), mean | **2.33** | 1.92 |
| rounds with ZERO feeder | **14.0 %** | 15.0 % |
| enemy buildings on our sockets (max) | **1.17** | 2.00 |
| our own bricks on sockets | 0.25 | 0 |
| Ti→ammo | **2019** | 1102 |
| Ti→ammo ≥ 300 | **12/12** | 11/12 |
| evictions | **11.5** | 0 |
| enemy builder-rounds on our 12-tile ring | **19.6** | 80.4 |

The eviction arm is doing exactly what `launcher_meta` §4.1 predicted: enemy
builder-rounds on our own ring fall **80.4 → 19.6**, and enemy buildings on our
sockets fall **2.00 → 1.17**, for 20 Ti once and zero ammunition.

## 16.5 The honest read, and what the fixture cannot tell us

**The local mimics do not run the attack.** Across the batch, enemy buildings on
our sockets peak at ~1.6 for leap7 and ~1.8 for leap6 — against Juusto the
losing figure is 4.78 mean / 6.4 max. So this fixture can detect the plank's
**cost** and cannot detect its **benefit**. Every number in 16.4 should be read
as a cost measurement.

### Ablation — 12 games each vs `mimic_0033`, 4 cells x3

| tree | wins | Ti collected |
|---|---|---|
| `loki_leap7` | 9/12 (75 %) | 1136 |
| `leap7_nogun` (`SG_RING_TURRET=False`) | 10/12 (83 %) | 1152 |
| `leap7_nofill` (`SG_SELF_FILL=False`) | 7/12 (58 %) | 1184 |
| `loki_leap6` | 8/12 (67 %) | 1344 |

**There is no separation at this n and it would be dishonest to claim one** —
the same three trees on an earlier build of the fill arm ranked
nofill 10/12 > nogun 9/12 > leap7 7/12, i.e. exactly reversed. What the two runs
agree on is that nothing here is catastrophic any more, which was not true
before 16.3.

## 16.6 Ablation variants

| tree | flag | question |
|---|---|---|
| `bots/leap7_off` | `SG_ON = False` | the inertness control — must emit zero `SG` markers |
| `bots/leap7_nofill` | `SG_SELF_FILL = False` | is arm 2 a net cost outside the socket meta? |
| `bots/leap7_nogun` | `SG_RING_TURRET = False` | is arm 5 the home-defence refutation all over again? |

`tools/leap7_variant.py NAME FLAG=VALUE …` stamps any other combination.

## 16.7 Standing risks, pre-registered

1. **Arms 2 and 5 are the ones to kill first.** Home defence has measured
   negative in this tree before — `T5_HOME_GUNNER_ON` is `False` in `doctrine.py`
   for that reason — and the fixture above says so again. They are separately
   flagged and separately ablatable precisely so a real measurement can remove
   one without touching the other four.
2. **No panel run.** The 45-map / 3-rep / mirror-control panel has not been run,
   and neither has `tools/crashtest.py loki_leap7 mimic_istones --synth`.
3. **The fixture is wrong for this plank.** Confirming the benefit needs an
   opponent that actually seals sockets. The cheapest honest next step is a
   *mimic of Juusto's kill chain* (ferry a builder in by turn 14, barrier the
   sockets, kill the feeder) rather than more games against mimics that do not.
4. **Spawn tiles.** Bricks, the corner launcher and (indirectly) the turret all
   consume ring tiles, and the 12-tile ring is also the spawn ring.
   `SG_FILL_FREE_MIN`, `SG_FILL_ENEMY_FACE_ONLY` and `SG_GUN_OFF_RING` bound
   this to at most 2 bricks + 1 corner, but nothing measures spawn refusals yet.
   A conveyor does **not** cost a heal seat (conveyors are bot-passable); a
   brick does.
5. **Slot 9's top nibble is now taken.** Anything that later wants those four
   bits must read 16.1 first. The Core remains the only writer.
6. **Nothing was uploaded.** No `fcode submission` command of any kind was run.
   v155 remains live and v157 (Odin) remains standing.

---

# 17. PLANK CAGE — loki_leap7, 2026-08-17

`bots/loki_leap7` = loki_leap6 + PLANK SOCKET-GUARD (§16) + **PLANK CAGE**.
Master flag `CAGE_ON`; `bots/leap7_nocage` is the inertness control.

## 17.0 The bet, in one paragraph

`analysis/meta_2000.md` (505 fresh ladder games / 1010 game-sides) says the #1
bot does not out-economise anyone — it **out-transports** them. It ferries a
builder onto the enemy core's 12-tile spawn ring by round 7 with a chain of
launchers, bricks all twelve tiles, teleports itself around the ring with more
launchers to keep the bricks up, and only then starts shooting a core that can
neither spawn nor heal. Seal depth is the largest single win-correlate in the
corpus (0–3 sealed → 27 %; 12/12 → 93 %, heal ratio 0.00), and *ordering* is a
second, separable one (seal before first damage → 93 %, n=70). We already win
**83 %** of the games where we reach seal ≥ 10 — statistically the same as
Jython's 85 % — we simply reach it in 34 % of games against their 91 %, and we
hold it a median of **zero** turns against their 77. This plank is the four
mechanisms that close that gap, taken as one package: `CAGE_FERRY` (the
launcher ladder), `CAGE_SEAL` (ring12 instead of the eight seats),
`CAGE_BEFORE_SIEGE` (hold fire until the cage exists) and `CAGE_EVICT` /
`CAGE_HOP` (the launcher parked at their ring).

## 17.1 What was implemented

| arm | where | what it does |
|---|---|---|
| `CAGE_FERRY` | `_cg_ferry_try` (rider), `_cg_ferry_launch` (launcher), `_launcher_turn` | raid slot 0 builds a launcher on an adjacent tile, stands still one round, is thrown r²≤26 toward their core, and the launcher `self_destruct()`s — refunding its +10 % scale — unless another of our builders is inside its pickup disc, in which case it is kept as a relay |
| `CAGE_SEAL` | `_collar_act`, `_collar_budget`, `_cg_corner_ok`, `_cg_outer_station` | the collar's target set widens from the 8 heal seats to all 12 ring tiles and its cap from 32 → 45 Ti; a diagonal corner is only bought once ring8 ≥ 6 and one corner is kept free while we hold no launcher at their ring |
| `CAGE_BEFORE_SIEGE` | `_cg_beat_bit` (publish), `_cg_hold` (consume), `_raid_act` step 1, `_raid_peck`, `main._turret` | while the seal is under `CAGE_SEAL_GATE` (9) nothing we own fires at their **core** — not the forward sentinels, not a raider's peck. Every other target stays legal, and sentinels are still built and sited as before |
| `CAGE_EVICT` / `CAGE_HOP` | `_tw_launcher`, `_cg_hop`, `_cg_gate` | the pluck's victim set widens from their 8 seats to all 12 ring tiles; when there is nobody to evict the same free action throws one of **ours** from a finished ring station to one that still needs a brick |

Two gates were **replaced, not extended**, and both are deliberate:

* **`_cg_gate` replaces `_tw_gate` for the launcher only.** TW's six-term gate
  (r ≥ 60, a MACRO/MACRO\_WEAK archetype, no enemy turret ever seen, ≥ 3 of
  their seats manned) was written for a defensive plucker. It is what kept
  launchers out of 85 % of our games. The cage's gate is four terms — the flag,
  r ≥ `CAGE_LAUNCH_MIN_RND` (20), establishment, a live foothold. **The gunner
  keeps all six**: it burns 4 ammo a round and this plank buys nothing needing
  it.
* **`TW_RESERVE_ON` is waived while the cage is short of its gate.** The
  reservation demands two forward sentinels standing before a gated weapon is
  bought; this plank's whole thesis is that the tubes come *after* the cage, so
  inside that window the reservation is a test the design guarantees will fail.

## 17.2 The store — one bit, and the first build got it wrong

The obvious home for ARMED/OPEN/DISARM was slot 13 bits 28–30, above the HP
band, on the reasoning that slot 13's two writers already preserve that field
(`_arch_note` masks with `ARCH_KEEP_HI`, `_sge_core_band` rewrites only 26–27).
**Measured, first smoke game (nordkap seed 2): the OPEN latch was set at r25 and
re-set on 58 consecutive rounds — it never once survived.** `_arch_note`
preserves the high bits it *read*, and it reads the start-of-round snapshot, so
any builder reporting detector evidence later in the same round wins the
last-write and erases the latch. This is FIX B's defect in a fresh field, the
third time this lineage has walked into it.

The published state is therefore **one bit, slot 15 bit 31**, assembled by
`_raid_beat` — the sole writer of that word in the tree, which republishes it
whole every round. `bots/probe_store31` was written to check the "sign safety"
reservation on bit 31 that has sat in `doctrine.py` untested since the
beginning: `0x80000000`, `0x800003FF` and `0xFFFFFFFF` all survive a write/read
cycle byte-identical. The store is a genuine u32 and the reservation was
superstition.

OPEN and DISARM are then **per-unit latches**, which they can be because each is
a function of something already published: OPEN from this body's own ring census
(or from the bit going 1 → 0), DISARM from the enemy-core HP band in slot 15
bits 28–29.

One inversion from FIX B is load-bearing and is commented at the call site: **a
blind established raider publishes the HOLD, it does not republish what it
read.** The band can republish because its zero state means "nobody has looked";
this bit's zero state means "shoot", which must never be arrived at by accident.

## 17.3 Three defects this batch found, all measured

1. **The ferry spent the trunk chain's opening bank.** glacierkeep side B seed
   2: three hops at r2/r4/r6 took the bank **470 → 105 by t7** against leap6's
   294. The 9-conveyor trunk never connected, `titanium_collected` stayed at
   **0 for 1000 rounds**, and the game was lost on the tiebreak while holding an
   11/12 seal for **949 turns** — Jython's `73867571_g4` failure mode,
   reproduced exactly, on the same map that produced SOCKET-GUARD defect
   §16.3 #2. Fix: `CAGE_FERRY_TI_FLOOR` 4 → **220**, dropping to 120 where the
   nearest ore is within d² ≤ 16 of our own core (antler 4, midgard 9,
   nordkap 9 are near; auroraveil 29, drakkarfjord 58, glacierkeep 65 are not).
   In practice: three hops on a short trunk, two on a long one. Re-run:
   glacierkeep **won in 191 turns**, no stall anywhere in the batch.
2. **The ferry rider silently stopped being the rider.** `raid_slot` is not a
   constant — `_raid`'s navigation-stall handler increments it to rotate the
   station assignment — so one bumped wall disqualified the rider forever and
   capped the ladder at one hop a game. Fix: the seat is latched on the body's
   first raid turn (`cg_seat`).
3. **A raider joining a raid already in progress restarted the hold.** midgard
   seed 2: a body that reached the ring at r120, long after the team opened at
   r58, re-held our guns from r135 to r155 because its own census was short of
   the gate. Fix: a live heartbeat stamped *before* this body's first published
   round means a teammate was established first and is not holding — the joiner
   inherits OPEN (`w=join`).

A fourth, cheaper one: `_cg_hop`'s declined scans (a 12-tile census plus an
88-tile site walk) ran every round on a unit whose whole job is one free throw.
`CAGE_HOP_RETRY` throttles the scan separately from the hop.

## 17.4 Smoke — `tools/cage_smoke.py`, seed 2

**`NOISE_ON` is `True` in this tree.** The same leap6 control on the same cell
between the two batches ran 92 → 191 turns on antler and collected 420 → 1630
titanium; on nordkap 158 → 206 turns and 1970 → 2460. Nothing below is a
measurement, single cells are noise, and the win column at n=6 cannot rank two
trees. What the batch is for is the *chain*.

6 cage games + 6 paired leap6 controls + 2 inertness legs. **0 tracebacks out of
either tree, 0 TLEs, and `bots/leap7_nocage` emitted zero `CG` markers.**

### The chain — `tools/cage_mechanism.py`, same 14 games

Medians. `lead` = (first turn we damaged their core) − (first turn the seal
reached 9); positive is the winning order. `-999` is the sentinel for "we shot
their core and never sealed at all", which is why the `baseis` cell reads −588.

| | leap7+cage vs 0033 (n=4) | leap6 vs 0033 (n=4) | leap7+cage vs istones (n=2) | leap6 vs istones (n=2) |
|---|--:|--:|--:|--:|
| first raider **at their ring** | **12.5** | 25.0 | **25.5** | 45 |
| seal max / ring8 max | 11 / 8 | 11 / 8 | 11 / 7.5 | 5.5 / 3.5 |
| **turns held at seal ≥ 10** | **65.5** | 27.0 | **70.0** | 6.0 |
| **turns held at 12/12** | **19** | 0 | **22.5** | 0 |
| **seal-before-first-shot lead** | **+16** | −25 | **+2** | −588 |
| **enemy heal ratio** | **0.10** | 0.33 | **0.00** | 0.78 |
| kill round | **142** | 198.5 | **161.5** | 230.5 |
| wins | 3/4 | 4/4 | 2/2 | 2/2 |

Every axis `meta_2000.md` names moves the right way, and the two that the corpus
says are causal move furthest: **the ordering flips from −25 to +16** and the
**enemy heal ratio falls from 0.33/0.78 to 0.10/0.00**. Turns held at 12/12 goes
from 0 — the number §7 of `meta_2000.md` calls our actual problem — to 19–22.5.

Marker census over the six cage games: `CG lift` 7 (5/6 games), `CG ferry` 7
(5/6), `CG sd` 5 (4/6), `CG relay` 2 (2/6), `CG seal` 518 (6/6), `CG hold` 5
(3/6), `CG open` 12 (6/6), `CG evict` 30 (3/6), `CG hop` 18 (4/6). `CG off`
fired 3 times in one game of the **pre-fix** batch (the glacierkeep stall) and
zero times after — the finisher guard is exercised, but only by the defect it
was written for.

The pre-registered bars, and how they read: markers fire on every arm **yes**;
a raider at their ring before turn 30 **yes, in 5 of 6 games** (turns 6, 8, 17,
17, 31); seal ≥ 9 **yes, 12/12 in three games**; flags-off inert **yes**;
wins not obviously collapsing **3/4 and 2/2 against 4/4 and 2/2** — one loss,
nordkap, where the seal peaked at 10 and the heal ratio stayed at 0.74.

## 17.5 The honest read

* **The win column is not evidence.** n=6, and the noise floor on this fixture
  is wider than any difference in it. The mechanism table is the evidence, and
  it measures that the machine works, not that it wins.
* **Titanium collected falls sharply** (680/410 against 1672/1500). Part is real
  — the cage costs ~45 Ti of barriers and 1–3 launchers, and it ends games
  ~60 rounds sooner, so there is less time to collect. Part may be the ferry
  still leaning on the opening bank even at the new floor. `auroraveil_A` was
  won in 205 turns on **0 titanium collected**, which is a win and a warning:
  that game is one failed kill away from a tiebreak loss.
* **The local mimics do not defend a ring.** `mimic_0033` and `mimic_istones`
  neither ferry nor re-brick, so this fixture measures the plank's *cost*
  faithfully and its *benefit* optimistically.

## 17.6 Ablation variants

| tree | flag | question |
|---|---|---|
| `bots/leap7_nocage` | `CAGE_ON = False` | the inertness control — must emit zero `CG` markers |
| `bots/leap7_cgwhy` | `CAGE_LOG_WHY = True` | why the ferry declined, per round (`CG why r=N w=…`) |

`tools/leap7_variant.py NAME FLAG=VALUE …` stamps any other combination; the
arms that most need their own leg are `CAGE_FERRY=False` (is the ladder worth
its bank?) and `CAGE_BEFORE_SIEGE=False` (is the ordering worth the withheld
damage?).

## 17.7 Standing risks, pre-registered

1. **The ferry versus the opening economy is still the sharpest edge.** The
   fix is a bank floor calibrated on one map from one seed. A floor that is too
   high makes the arm dead code on long maps; too low reproduces §17.3 #1.
   The cheapest honest next step is a `CAGE_FERRY=False` leg over the 45-map
   panel, not more games on six cells.
2. **Holding fire is a real cost against a bot that rushes us.** The hold lapses
   on the clock (`CAGE_SEQ_TIMEOUT` 220), on a dead foothold, and on the
   finisher guard — but between r10 and r60 it does mean our forward sentinels
   shoot belts instead of the core. Nothing in this batch isolates that cost.
3. **CPU is unmeasured.** `_cg_seal` adds ~40 engine calls per established
   raider per round and `_cg_hop` adds a bounded scan on each forward launcher.
   No TLEs appeared locally, but `get_cpu_time_elapsed()` returns 0 on this
   build (`engine_mechanics` §I), so local CPU measurement is broken and this is
   a claim about the absence of evidence.
4. **Spawn tiles, again.** This plank deliberately bricks all twelve, including
   the four diagonals — that is the mechanism. `CAGE_RING8_FLOOR` and
   `CAGE_CORNER_KEEP` bound the order and keep one corner for the launcher, but
   a fully sealed ring is also a ring our own raiders cannot stand on;
   `CAGE_OUTER_STATION` is what keeps them working from the shell and it is
   exercised but not separately measured.
5. **Slot 15 is now full.** Bits 0–9 heartbeat, 10–27 collar lanes, 28–29 HP
   band, 30 TW gunner, 31 cage hold. Anything that later wants a published field
   must take a slot from something else or pack into slot 13 — and §17.2 is the
   record of what happens if it assumes slot 13 can hold a latch.
6. **No panel run, no arena, nothing uploaded.** The 45-map panel has not been
   run, `tools/crashtest.py` has not been run, and **no `fcode submission`
   command of any kind was issued**. v155 remains live and v157 (Odin) remains
   standing.

---

# 18. PLANK PAIRS — forward sentinels deploy in twos, never in ones

## 18.0 The bet, in one paragraph

`analysis/meta_pipeline_diff.md` (505 fresh ladder games / 1 010 game-sides /
2 230 sentinels) ranks every lever it can measure, and the biggest one is not an
economy number or a placement number. It is a *count*: **peak sentinels alive
within 6 tiles of the enemy core at the same moment.** At ≥ 2 we win **82.3 %**;
at 1 we win **33.3 %** — a **+48.9 pp** split, and the top-5 agree at +51.9
(87.1 vs 35.2). It is also the one metric whose *median* sits on the wrong side
of the split for us: our median peak is **1**. The shape of the failure is not
poverty — conditional on winning we already reach 2 on **62.2 %** of sides,
*ahead* of the top-5's 56.4 % — it is that our losing half never gets a second
tube up at all, so a lone turret absorbs the entire response and dies having
landed a median **6** core shots against a pair's **14 each**. 14 + 14 = 28 =
ceil(500/18) = exactly one core. **A tube that stands alone is not half a kill;
it is a donation** — 68 % of our core-hitting sentinels die, against the top-5's
27 % and Jython's 22 %. This plank makes the pair the unit of deployment.

## 18.1 What was implemented

| arm | where | what it does |
|---|---|---|
| 1 · the discount, immediate | `raid._sge_mass_ok` | tube 2's bank floor drops from `LOKI_FWD_TI_FLOOR` (40) to `SIEGE_MASS_TI_FLOOR` (6) the round tube 1 is **sited**, not after `SIEGE_MASS2_AGE` (20) rounds of survivorship |
| 2 · the hold | `raid._pr_hold`, `main._hold_core_fire` | a tube that is alone does not fire at their **core**; every other target stays legal |
| 3 · the reserve | `main._sge_jit`, `raid._pr_core_hold` | while a tube is held the ammo pipe's spend floor rises to a sentinel + `PAIR_JIT_MARGIN`, so the bank climbs to fund tube 2 instead of buying a magazine nothing is firing |
| 4 · the release | `PAIR_RELEASE_RNDS` = 30 | if tube 2 has not arrived 30 rounds after tube 1 could first have shot, tube 1 opens anyway and latches open for good |

Three of the four are **rewires of machinery that already existed** (the
`SIEGE_MASS` discount from leap3/5, the JIT pipe, the marker path). The only new
code is the hold itself, `_pr_near`, and the doctrine block behind them.

**Arm 1 is the inversion, and it is worth stating plainly.** `SIEGE_MASS2_AGE`
was written as a *survivorship* test — "if the first tube is being answered on
arrival, a second body will just die with it". The fresh corpus says that is
backwards: the reason the first tube is answered on arrival is *that it is
alone*. Waiting 20 rounds to find out whether a solo tube survives is how the
solo tube stops surviving. The gate is still a **discount and never a veto** —
the floor only ever moves down — so a looser age here cannot refuse a tube the
parent would have bought.

## 18.2 The shared open-fire moment

`CAGE_BEFORE_SIEGE` (§17) and this plank ask the same question — *may this body
damage their core yet?* — so they are **OR'd**: fire opens only when **both** are
satisfied. `main._hold_core_fire` is the single place that resolves it, and the
three turret sites plus the two raider peck sites all go through it.

They are deliberately **not merged into one bit**. CAGE's hold is a *team* fact
(the ring census, published in slot 15 bit 31 and refreshed by the sole writer of
that word); PAIRS' hold is a *per-body* fact (this tube's own clock against a
team census of tubes). Folding a per-body latch into a shared word is precisely
the race that cost this tree two rebuilds — FIX B, and §17.2's slot-13 story.

CAGE is asked **first** on purpose: while it holds, the PR clock must not start,
because a tube that may not shoot for cage reasons has not yet "become able to
shoot", which is what arm 4's 30 rounds counts.

## 18.3 The store — nothing new, and that is the design

Slot 15 is full (§17.7 #5). Slot 13's high bits are the field `_arch_note` loses
races in. **PLANK PAIRS adds no shared state at all.** The pair census is already
published as `SLOT_FWD_GUN` (slot **8**), whose only writer is
`_t5_note_fwd_build` and which under `LOKI2B_LIVE_CAP_ON` carries the *live*
count of forward tubes — so it falls back to 1 when a tube dies, which is exactly
the re-hold a body that has not yet opened should see. The clock and the open
latch are per-unit.

Two deliberate asymmetries:

* **The latch is one-way.** Once a body has opened — by pair or by release — it
  never re-holds, even if the census falls back to 1. The measured lever is
  **peak** sentinels within 6, not concurrent ones, and a tube that re-mutes
  itself on its partner's death stops being the 14-shot half of 28.
* **The clock starts on the first ask, not on a build round.** A body is only
  asked when their core is actually in a line it could fire down, so the first
  ask *is* the round it became able to shoot — no store field is needed to carry
  a build round, and a home gunner never starts a clock at all.

The 6-tile predicate is `sge_centre_q4 <= PAIR_CENTRE_Q4` (144 = (6·2)² in the
quarter-scale centre metric the SIEGE band already uses) and is **raider-side
only**, for the marker and the census. The turret-side gate reads the published
count instead: a tube must never hold its fire forever because fog hid its
partner.

## 18.4 Smoke — `tools/pair_smoke.py`, seed 2, 8 legs

4 plank cells (midgard/A + nordkap/B vs `mimic_ph`, glacierkeep/A + antler/B vs
`mimic_0033`), 2 inertness cells (`bots/leap7_nopair`, `PAIR_ON=False`), 2
baseline cells vs `starter`.

| check | result |
|---|---|
| tracebacks out of `bots/loki_leap7` | **0** on all 8 legs |
| `PR pair` / `PR hold` / `PR release-solo` on the 4 plank cells | **4 / 5 / 2** — every arm fires |
| flags-off PR markers | **0** |
| flags-off other planks still alive (CG/SGE markers) | **58** and **90** |
| vs `starter` | **2 / 2 wins**, both `core_destroyed`, t=158 and t=95 |
| plank cells won | 4 / 4 |

Repeated on **seed 5** (`--seed 5`, same 8 legs): `PR pair` / `PR hold` /
`PR release-solo` = 3 / 1 / 1, flags-off still 0 PR markers against 81 and 197
CG/SGE markers, 0 tracebacks out of `bots/loki_leap7`, 2 / 2 vs `starter` both
`core_destroyed`, 3 / 4 plank cells won. The earliest pair observed was
`PR pair (9,8)+(9,7)` at **t10** on antler.

> **The first run of this file read every arm as dead, and the bug was in the
> tool.** The engine captures each unit's stdout *into the replay stream*; the
> process stdout carries only the JSON result and tracebacks. Grepping the
> subprocess output returns zero markers for a perfectly live plank. The lesson
> is recorded in the file: markers are read with `replay_parser`, never off
> `subprocess.run`.

## 18.5 The chain — `tools/pair_mechanism.py`, same 8 replays

Measured **off the board**, not off our markers, so a plank that believes it
paired and did not reads as a failure. `--near 6.0`, Euclidean to the 2×2 centre
— the corpus metric verbatim.

| | 4 plank cells | 2 flags-off cells |
|---|--:|--:|
| peak sentinels within 6, median | **2.0** | 1.5 |
| % of sides reaching ≥ 2 | **75 %** | 50 % |
| % reaching ≥ 3 | 25 % | 0 % |
| pair lag (turns, tube 1 → tube 2 in band), median | 21 | 11 |
| near sentinels built / died | 9 / **0** | 3 / 0 |
| **solo deaths** | **0** | 0 |
| bands (jammed / kill / diagonal / unreachable) | 0 / 8 / 1 / **0** | 0 / 3 / 0 / 0 |
| median distance to their core centre | **2.92** | 3.54 |
| lead = first core damage − first turn at peak 2 | **+1** | **−500** (shot before ever pairing) |
| first `PR release-solo`, median | r83.5 | — |

Two things are worth pointing at, and one thing is worth refusing to say.

* **The ordering flipped sign.** The flags-off cells put damage on their core
  before a pair ever existed (−500 is this tool's sentinel value for "we shot
  and never paired", the same convention `cage_mechanism.py` uses for the seal).
  The plank cells damaged the core *one turn after* the pair stood.
* **Median distance to their core centre is 2.92** — Jython's number to two
  decimals — with **zero** sentinels in the jammed (<2.5) or unreachable (>6.4)
  bands across all nine.
* **n = 4 versus n = 2 on partly different maps and opponents is not an A/B.**
  `NOISE_ON` re-rolls the core's spawn dispersion from OS entropy every match.
  Nothing in §18.5 ranks the plank against its own control; it shows the
  instruments are live and the mechanism runs end to end.

## 18.6 Standing risks, pre-registered

1. **The hold can cost a kill we would otherwise have closed.** A tube that
   holds for up to 30 rounds against a core already under 400 is 30 rounds of
   damage not dealt. The release exists for exactly this, and `CAGE_FINISH_HP`
   already disarms the cage in that window — but PAIRS has **no** terminal-band
   waiver of its own, and adding one is the first thing to try if the plank
   measures negative.
2. **Arm 3 starves the magazine of a tube that is legitimately busy.** A held
   tube still shoots belts and turrets, and the reserve raises the *spend* floor
   while it does. The magazine target (`SIEGE_JIT_MIN`, 16) is untouched and the
   reserve is suspended under attack, but a long hold against a rich opponent is
   a tube firing on 16 ammo.
3. **`SLOT_FWD_GUN` is the gate, and it counts tubes near the core — not tubes
   within 6.** `LOKI2B_CENSUS_DSQ` is 50 (≈ 7.1 tiles to the footprint), looser
   than the corpus's 6.0 to the centre. A pair that satisfies the gate can in
   principle be one tube in band and one just outside it. Tightening this needs
   either a second published field (there is none free) or a turret-side vision
   scan, which §18.3 argues against.
4. **The release clock is per-body, so two tubes built 25 rounds apart can open
   at different moments.** That is intended — each tube answers for itself — but
   it means "the pair opened fire" is never a single team-wide instant, and any
   later plank that wants one must publish it.
5. **CPU is unmeasured, again.** `_pr_hold` is one store read memoised on the
   round and `_pr_near` runs only on a forward-sentinel build, so the added cost
   is small by inspection — but `get_cpu_time_elapsed()` returns 0 on this build
   (`engine_mechanics` §I), so that remains a claim about the absence of
   evidence.
6. **No panel run, no arena, nothing uploaded.** The 45-map panel has not been
   run, `tools/crashtest.py` has not been run, and **no `fcode submission`
   command of any kind was issued**. v155 remains live and v157 (Odin) remains
   standing.

# 19. PLANK FIN + PLANK RATCHET — loki_leap8, wave 10, 2026-08-17

## 19.0 The two holes wave 9 named

`results/wave9/*.md` is the first batch in this line where the cage **machinery
works** — first raider at their ring r16.5–21 (vs leap6's 25–28), seal ≥ 10 in
45–49 % of games (vs 20–26 %), held ≥ 10 turns in 42–45 % (vs 15–20 %). And it
converted nothing: net −1.9 pp against leap6. Two named failures:

1. **the 12/12 window (15–22 % of games) converts ~nothing** — we reach the
   position Jython wins 85 % from and then keep grinding at the same cadence;
2. **vs `mimic_istones` the enemy heal ratio never moved off 0.91** — ring8
   topped out at 6 of 8, because *their healers pre-occupy the seats* and
   `can_build_barrier` is `False` on an occupied tile. We were sealing the
   empty half of their ring and calling it a cage.

FIN answers (1); RATCHET answers (2). They are one build because neither pays
alone: the ratchet manufactures the window the finisher spends.

## 19.1 What was implemented

| arm | where | what it does |
|---|---|---|
| FIN a · ammo surge | `main._sge_jit` | inside the window the magazine target rises to `FIN_AMMO_TARGET` (60), the bank floor drops to `FIN_TI_FLOAT` (20) and PAIRS' arm-3 reserve is suspended |
| FIN b · escort peck | `raid._fin_peck`, step 3e of `_raid_act` | an escort orthogonally adjacent to a Core tile with **no seal work pending** fires: 2 dmg / 2 Ti, zero cost scale |
| FIN c · tube priority | `raid._sge_mass_ok` | tube 3's discount arms on the window instead of waiting for the HP band to fall under `SIEGE_MASS3_HP` |
| RAT 1 · aimed pluck | `raid._tw_launcher` | victims ranked *seated healer our bricker is already beside* → *seated healer* → *anything else*, replacing CAGE arm 4's flat ring12 preference |
| RAT 2 · stage first | `raid._raid_station` | a station orthogonally beside a seated enemy builder inside one of **our** launchers' r²≤2 pickup disc is worth `RAT_STAGE_BONUS` (14) |
| RAT 3 · take the vacancy | `raid._collar_act` | seats we watched one of theirs sit on inside `RAT_WATCH_RNDS` go to the **front** of the brick list, and the collar's titanium budget cannot refuse one |

Both planks are one master flag each; `bots/leap8_off` (`FIN_ON = RAT_ON =
False`) emitted **zero** FIN/RAT markers and matches leap7_soft branch for
branch — every added test short-circuits on the flag.

## 19.2 Two defects this batch found, both in machinery that predates it

**(i) THE CAGE CENSUS COUNTS THEIR BODIES AS SEAL.** `_cg_seal` resolves a ring
tile through `is_tile_passable`, and `analysis/engine_mechanics.md` N.6
measures that predicate as `False` **under a builder bot of either team**. So
one of *their* healers sitting on one of *their* heal seats reads to us as a
sealed tile. Measured on the first wave-10 probe (`loki_leap8` vs
`mimic_istones`, synth_d, seed 2): the bot's own census said **10 of 12** while
the board said **4–8**, their seat occupancy meaned **6.45 of 8**, and the enemy
heal ratio was **1.000** — all 13,924 points we landed were healed back. The
first build of FIN opened its window on that phantom and spent **833 pecks /
1,666 Ti** inside it.

Fixed by a **second count taken in the same pass** (`cg_strict_val`, exposed as
`_fin_seal`): held only by terrain, by a building of either team, or by one of
**our** bodies — the definition `tools/fin_mechanism.py` measures from the
board. `_cg_seal`'s own answer is deliberately **left alone**: it gates the CAGE
hold, and tightening that would hold our fire far longer against exactly the
opponents wave 8 measured the hold-fire stretch on. **This is a live defect in
leap7_soft and every ancestor with `CAGE_ON`, and it is the best available
explanation for "the cage is built and the heal ratio does not move".**

**(ii) THE WINDOW WAS GATED ON THE WRONG HALF OF THE RING.** A ring12 census of
10 can be four corners and six seats — and each of the two seats still open is
worth +4 HP per titanium to their Core, which beats everything the window buys.
Measured, sab_05 seed 2: strict seal ≥ 10 all game, **100 % of our damage landed
inside the window**, 833 pecks spent, **heal ratio 1.000**. ring12 is the
**spawn** seal; ring8 is the **heal** seal, and FIN's premise is a statement
about ring8 only. `FIN_SEAT_GATE` (7) / `FIN_SEAT_DROP` (6) were added and both
terms must hold. `analysis/meta_2000.md` had already flagged "spawn-seal !=
heal-seal" as a failure mode to design against; this is where it bites.

## 19.3 One flag retuned on evidence

`RAT_CAP_N` 20 → **8**. S5 is what our own bodies *saw at once* near their Core,
not their army size. Max enemy builders within r² ≤ 20 of their Core, measured
off the wave-10 replays: `mimic_istones` 10 / 11 / 39, `mimic_0033` 5 / 5,
`mimic_juusto` 4 / 4. At 20 the ratchet fired in 1 of 8 istones games; 8 is the
detector's **own** threshold for "many builders near their Core"
(`ARCH_S5_MANY`, which the corpus set) and it separates the fixtures with room
on both sides. The archetype half of the gate is unchanged but nearly inert in
practice — `ARCH_R_MACRO` is 140 and most of these games are decided earlier.

## 19.4 Smoke — `tools/leap8_smoke.py`, seed 2, 25 games + two re-runs

Every candidate leg is paired with `bots/leap7_soft` on the same map, side and
seed. `NOISE_ON` re-rolls the Core's spawn dispersion every match, so **none of
these numbers is a measurement** — the batch exists to show the arms fire, the
gates hold and nothing crashes.

**No tracebacks, no TLEs, 25/25 games completed.**

vs `mimic_istones`, 4 big maps × 2 sides (`tools/fin_mechanism.py`, medians):

| | leap7_soft | loki_leap8 |
|---|---|---|
| games won | 5/8 | **6/8** |
| ring8 sealed, max | 6.5 | 6.5 (7.0 on the run before the seat gate; one game 8) |
| ring8 sealed, mean | 5.09 | **5.41** |
| enemy heal ratio | 0.98 | 0.98 |
| **window kill share** | **0.00** | **0.06** (0.60 on the pre-seat-gate run) |
| seats closed by ratchet | 0 | 0.25/game (fires in 2 of 8) |
| median kill round | 162.5 | 630.5 |
| tiebreak stalls | 4/8 | 4/8 |
| titanium spent on pecks | 0 | 79/game |

vs `mimic_juusto` (nordkap, 2 sides): FIN fires — `FIN open` ×9, `FIN peck`
×343, `FIN surge` ×2 across the non-istones legs; heal ratio 0.208 / 0.789;
1W 1L.

vs `mimic_0033` (midgard, 2 sides): **`RAT_CAP_ONLY` holds** — `RAT pluck` 0,
`RAT ratchet` 0, exactly as designed (their near-core builder census is 5, well
under `RAT_CAP_N`). FIN is *not* archetype-gated and did fire (302 pecks in the
B-side game, which was lost); leap7_soft won that cell in the first run.

`bots/leap8_off` (`FIN_ON = RAT_ON = False`): **zero FIN/RAT markers**, won its
cell, no behavioural difference found.

## 19.5 The honest read

**FIN's plumbing works and its premise is under-served.** Damage now lands
inside the window (kill share 0.00 → 0.06, and 0.60 before the seat gate was
added), the surge and tube-3 arms fire, and the peck is cheap. But the enemy
heal ratio vs istones **did not move** (0.98), and the reason is arithmetic: at
7 of 8 seats held, one open seat heals +4 HP per titanium and out-earns two or
three escort pecks. The window's premise — "their heal is ~0" — is only true at
**8 of 8**, and we get there in a minority of games.

**RATCHET works per event and is rate-limited by launchers, not by logic.** Of
the plucks it aims, roughly half convert into a brick on the vacated seat, which
is the mechanism doing exactly what it was built to do. But a launcher sits on a
ring **corner** and only two of the eight seats fall inside its r² ≤ 2 pickup
disc, and the fixture builds **one** launcher per game — so the ceiling is ~2
reachable seats, and the observed rate is 0.25 seats closed per game. **The
binding constraint on the heal wall is launcher COUNT and launcher SITING, not
the eviction logic.** That is the wave-11 lever.

**The kill round stretched** (median 162.5 → 630.5 on the istones cells) with
stalls unchanged at 4/8. On n = 8 with `NOISE_ON` this is not adjudicable —
leap7_soft's own kill rounds on the same cells run 57 / 162 / 163 / 971 — but it
is the pre-registered failure mode of both planks and it is the first thing the
A/B must check.

## 19.6 Ablation variants, stamped and unmeasured

`bots/leap8_off` (both master flags down, the inertness control),
`bots/leap8_nofin`, `bots/leap8_norat`, `bots/leap8_nopeck` (`FIN_PECK_ON`
only — the arm carrying the stretch risk), `bots/leap8_seat8`
(`FIN_SEAT_GATE = 8`, the "heal is actually zero" endpoint §19.5 argues for).

## 19.7 Standing risks, pre-registered

1. **The peck is a step not taken.** `LOKI_QUIET_ON` was a measured win because
   acting and moving are mutually exclusive and this line wins on arrival. If
   median kill round rises in the A/B, `leap8_nopeck` is the first arm to try.
2. **The surge is titanium not banked, and stored titanium is tiebreak #3.** A
   cage with no finisher that now also empties the bank loses tiebreaks it used
   to win. Stalls were 4/8 on both arms here; that number is the one to watch.
3. **`FIN_SEAT_GATE = 7` is one seat too loose** by the arithmetic in §19.5, and
   `leap8_seat8` exists to test it. The counter-argument is that at 8/8 the
   window is so rare the plank is inert.
4. **The ratchet's rate is bounded by the launcher, not by the ratchet.** Two
   reachable seats per launcher, one launcher per game. Raising `TW_LAUNCH_CAP`
   or siting a second launcher on the opposite corner is the wave-11 lever, and
   it is a scaled purchase at the moment the raid is most exposed.
5. **`_cg_seal`'s defect (§19.2 (i)) is still live** everywhere except FIN's own
   consumer. The CAGE hold gate still opens on a ring full of their healers.
   Fixing it is a behaviour change to a frozen plank and needs its own arm.
6. **The archetype half of `RAT_CAP_ONLY` is nearly inert** (`ARCH_R_MACRO` =
   140). The gate is carried by S5 alone in practice.
7. **CPU is unmeasured.** `exec_time_us` is 0 on this build, as in wave 9. By
   inspection the added cost is one extra `get_tile_builder_bot_id` per
   impassable ring tile (`_cg_seal`, no extra pass), ≤ 4 tile reads per peck
   attempt, and ≤ 48 per raid-station rescan while the ratchet gate is open.
8. **No panel run, no arena, nothing uploaded.** The 45-map panel has not been
   run, `tools/crashtest.py` has not been run, and **no `fcode submission`
   command of any kind was issued.** v155 remains live.

# 20. THE WAVE-10 MEASUREMENT, ACTED ON — loki_leap9, wave 11, 2026-08-17

## 20.0 What wave 10 named, and what this batch does about it

`results/wave10/leap8_vs_leap6.md` is a **negative** A/B — leap8 −5.0 pp on the
panel, −8.1 pp/game vs `mimic_juusto` (p = 0.0013), −5.6 pp vs `mimic_0033`
(p = 0.0135) — and §19 named four causes rather than guessing. This batch is
those four, and nothing else:

| fix | the wave-10 finding | what changed |
|---|---|---|
| 1 · STRICT SEAL EVERYWHERE | §19.2 (i) / §19.7 risk 5: the loose census counts THEIR bodies as seal, and it still gated the CAGE hold and the corner spend | every **gate** reads `_cg_census` (strict); the loose count survives only as the free-corner scouting term |
| 2 · PECK_MACRO_ONLY | the peck was FIN's only un-gated arm, and vs juusto it fired 519× on the way to −8.1 pp | `_fin_peck` takes the detector's verdict (slot 9) and fires on MACRO / MACRO_WEAK only |
| 3 · LAUNCHER CAPACITY | §19.5: "the binding constraint on the heal wall is launcher COUNT and launcher SITING, not the eviction logic" (0.107 ratchets/game) | (a) ferry relays convert instead of self-destructing when sited in pickup range of the ring; (b) `CAGE_EVICT_CAP` = 2 with the 20-round survivorship clock waived and the second sited on the opposite corner; (c) the stationing bonus follows the evictor, not the cap read |
| 4 · SURGE TRIM | §19.7 risk 2: tube 3 in-window is a scaled purchase out of a bank the surge has just emptied | `FIN_TUBE3_ON` → **False**, flag kept for the ablation |

One flag each: `CAGE_STRICT_SEAL`, `FIN_PECK_MACRO_ONLY`, `CAGE_FERRY_CONVERT` /
`CAGE_EVICT_AGE` / `CAGE_EVICT_SPREAD` / `RAT_STAGE_ANY_EVICTOR`,
`FIN_TUBE3_ON`. `bots/leap9_off` emits **zero** FIN/RAT/convert markers and won
its cell.

## 20.1 Measurement — paired, `bots/loki_leap8` on the same cells and seed

`tools/leap9_smoke.py` (27 games, seed 2) is the gate check; `tools/leap9_rate.py`
(10 big maps × 2 sides × 2 arms) is the rate batch, because the ratchet is a
RATE and 8 cells cannot separate 0.107 from 0.25. `NOISE_ON` throughout:
**none of this is an A/B**; the 45-map panel is.

vs `mimic_istones`, seed 3, n = 20 per arm (`tools/fin_mechanism.py`):

| | loki_leap8 | loki_leap9 |
|---|---|---|
| games won | 12/20 | **14/20** |
| enemy heal ratio (median) | 0.99 | **0.71** |
| games at heal ratio < 0.5 | 3/20 | **7/20** |
| their seat occupancy (mean) | 4.545 | **3.562** |
| window kill share (median) | 0.05 | **0.31** |
| kill round (median) | 227 | **171** |
| tiebreak stalls | 11/20 | **7/20** |
| titanium spent on pecks | 148.9 | **9.4** |
| `RAT ratchet` per game | 0.00 | 0.05 |
| `CG evictor2` per game | 0.00 | 0.15 |
| `CG convert` per game | — | **0.00** |

**The heal wall moved for the first time in this line.** Waves 3–10 could not
shift `mimic_istones` off a heal ratio of 0.91–0.98; it is 0.71 here and below
0.5 in seven games of twenty. Their seat occupancy fell a full seat. The kill
round FELL rather than rose, which was the pre-registered failure mode of both
wave-10 planks.

vs `mimic_juusto`, seed 4, n = 20 per arm — the cell fix 2 exists for:
16/20 vs 17/20, kill round 133 vs 134, stalls 2 vs 3, peck titanium **2.0 vs
65.6**. The 519 pecks are gone and nothing measurable went with them, but this
batch cannot resolve the wave-10 −8.1 pp either: that was 270 games on the
45-map panel against `loki_leap6`, and this is 20 games against leap8.

vs `mimic_0033`, seed 5, n = 20 per arm — the OTHER wave-10 regression cell
(−5.6 pp, p = 0.0135), and the one most exposed to fix 3(c) taking the
stationing bonus outside `RAT_CAP_ONLY`:

| | loki_leap8 | loki_leap9 |
|---|---|---|
| games won | 16/20 | **19/20** |
| tiebreak stalls | 5/20 | **0/20** |
| titanium spent on pecks | 89.3 | **0.0** |
| enemy heal ratio (median) | 0.18 | 0.14 |
| kill round (median) | 107 | 124 |

The ratchet stayed effectively silent there (`RAT ratchet` 0.05/game, one brick
in twenty games) — `RAT_CAP_ONLY` still holds, as designed.

## 20.2 The gate checks, which are the point of the batch

* **FIX 2 passes exactly.** `FIN peck` vs `mimic_juusto` = **0** (leap8: 519)
  and vs `mimic_0033` = **0** (leap8: 94). The detector reads juusto as
  PRESSURE/DEFAULT (first call r57), 0033 as PRESSURE (r48), istones as
  MACRO/MACRO_WEAK — **first call r141**.
* **`ARCH_R_MACRO` = 140 is now doing more work than it was set for.** The peck
  survives only vs istones and only after r141, which is why peck titanium is
  9.4/game rather than 0. With the median kill round at 171, FIN arm (b) is
  close to inert. That is an argument for `FIN_PECK_ON = False` outright;
  `bots/leap9_peckany` is the other end of the same ablation.
* **FIX 1 opens the window MORE, not less.** `FIN open` reaches 47 markers on
  the istones smoke legs against leap8's 7, and ring8-max median rose 6.5 → 7.5,
  because the strict census also gates `_cg_corner_ok` — so titanium stops being
  spent on SPAWN corners while HEAL seats are still open. Finisher guard (ii)
  was written for exactly that and the loose census was defeating it.
* **`CG hold` roughly tripled** (1.60/game vs 0.55) and the kill round still
  fell. The wave-8 hold-fire stretch did not reproduce.

## 20.3 One arm is inert, and the measurement says why

**`CAGE_FERRY_CONVERT` (fix 3(a)) never fires — 0 in 67 games.** Measured off
the `CG sd` / `CG relay` markers: the distance from a disposed ferry relay to
the NEAREST enemy ring tile is **d² = 49 minimum, 289 median, 970 maximum**.
A launcher's pickup disc is d² ≤ 2. The cause is structural and it is in the
ferry's own constants — `CAGE_FERRY_STOP_DSQ` = 40 stops the rider building
once it is inside d² ≤ 40 of their Core, so the last relay is always ~7+ tiles
short of the ring and the rider walks the rest. **The conversion predicate is
correct and unreachable.** It is kept, flagged, and free (one cached-geometry
test per throw); making it reachable means moving the ferry's stop distance,
which is a different plank and a different measurement.

The capacity gain in 20.1 is therefore carried entirely by **3(b)** (second
evictor, survivorship waived, sited on the opposite corner — `CG evictor2`
fires 0.15/game) and **3(c)** (the stationing bonus following the evictor).

## 20.4 The ratchet bar was NOT met, and the reason is a gate, not the logic

Pre-registered bar: "`RAT ratchet` rises materially above 0.107/game."
Measured **0.05/game** (leap8 on the same 20 cells: 0.00; on the smoke's 8
cells, leap9 0.125 vs leap8 0.25). It did not rise.

The reason is in the same census: **`RAT pluck` fell 9.30 → 0.35/game while
`TW pluck` held at 9.15 vs 9.75 and `CG evict` at 49.9 vs 47.8.** The evictions
did not stop; they stopped being *counted as ratchet plucks*, because
`_rat_live` (RAT_CAP_ONLY) opens on MACRO — earliest r141 — or on an S5 census
of 8, and **leap9's median kill round is now 171**. The ratchet's own gate now
opens after the games it was built for are decided; leap8 banked its plucks in
1000-round stalls leap9 no longer plays.

That is the wave-12 lever and it is one question: does the ratchet need the
archetype half of `RAT_CAP_ONLY` at all, given S5 is the term that actually
proxies "at the unit cap"? It was NOT widened here — `RAT_CAP_ONLY` is the
guard that keeps the ratchet silent vs `mimic_0033`, and 0033 is a measured
regression cell (−5.6 pp, wave 10).

## 20.5 Ablation variants, stamped and unmeasured

`bots/leap9_off` (the inertness control), `bots/leap9_loose`
(`CAGE_STRICT_SEAL = False` — fix 1 alone reverted), `bots/leap9_noev`
(fix 3 reverted), `bots/leap9_peckany` (`FIN_PECK_MACRO_ONLY = False` — fix 2
alone reverted).

## 20.6 Standing risks, pre-registered

1. **`RAT ratchet` did not rise** (20.4). If the panel confirms the heal-wall
   gain, the ratchet counter is measuring the wrong thing and the arm wants
   re-gating or retiring, not tuning.
2. **The peck is nearly inert** (20.2). If `leap9_peckany` matches leap9 on
   istones, arm (b) costs an action for nothing and `FIN_PECK_ON` should go to
   False.
3. **`_tw_launch_walk` no longer early-returns on "already in place".** The
   standing tile is scored at walk distance 0 instead, identical whenever the
   spread rank is flat — i.e. in every case the parent had — but it is a
   rewrite of a hot path and the first thing to check if raiders start
   shuffling between corners.
4. **The strict seal delays the corner spend**, so more of their SPAWN tiles
   stay usable for longer. ring12-max is the number to watch on the panel;
   ring8 is what the trade buys.
5. **A second evictor is a second scaled purchase** at the moment the raid is
   most exposed, with the survivorship clock waived. It fires 0.15/game, so
   both the bill and the evidence are small.
6. **vs juusto, ring8-max fell 8.0 → 6.0 and window kill share 0.59 → 0.0**
   while wins and kill round held. Their heal ratio is 0.0 on that fixture
   either way, so the window buys nothing there — but it is an unexplained
   difference and it is on the cell wave 10 lost.
7. **CPU unmeasured.** By inspection: one extra `_cg_gate` call per launcher
   decision, one 12-tile geometry scan per ferry throw, and one
   `get_nearby_buildings` walk per corner candidate while a second evictor is
   being sited (≤ 4 corners, and only while the cage gate is open).
8. **n = 20 per arm, `NOISE_ON`, one seed per batch. Not adjudicable.** The
   45-map panel against `loki_leap6` is the bar and it has not been run.
9. **Nothing uploaded.** No `fcode submission` command of any kind was issued.
   v155 remains live.


---

# 21. THE EVICTOR GATE, AND THE RATCHET RETIRED — loki_leap10, wave 12, 2026-08-17

## 21.0 What wave 11 measured, and the two things this batch does about it

`results/wave11/leap9_vs_leap6.md` split the paired A/B on one predicate — did a
launcher of ours ever stand inside its own `d^2 <= 2` pickup disc of one of
THEIR ring tiles (an **evictor**, standing) — and the two halves went opposite
ways:

| cells | vs `loki_leap6` | enemy heal ratio |
|---|---|---|
| an evictor stood | **+4.4 pp** | **0.562** |
| no evictor stood | **−9.0 pp** (p = .081) | — |

The same package, priced twice. Where the evictor stands the cage does what it
was designed to do: the seat cannot be re-manned, their heal falls by nearly
half, and the hold-fire that bought the seal is repaid. Where none stands, the
expensive arms are a pure bill — we hold our guns off their Core waiting for a
seal nobody will finish, surge the bank into a window opened on a ring their
healers walk back onto, and buy diagonal corners beside a Core that heals
faster than we shoot it.

The same measurement killed the ratchet: **the launcher-to-bricker handoff
converts at 2.9 %**. The arm was given two waves and a capacity fix and the
conversion did not move.

| change | what it is |
|---|---|
| 1 · **RATCHET OFF** | `RAT_ON = False`, permanently. Every branch stays in the tree, one flag from live, and nothing may turn it back on without a NEW measurement of the **handoff** — not of the eviction count. |
| 2 · **THE EVICTOR GATE** | `CAGE_EVGATE_ON`. Hold-fire, the FIN window and the diagonal-corner spend run ONLY while an evictor is established. Before that, and for good if none arrives by `CAGE_EVGATE_DEADLINE` (80), the bot plays the ordinary leap6-style attack. |
| 3 · **ESTABLISHMENT EFFORT** | `CAGE_EST_RETRY`, `bots/leap10_est` only. The arrived ferry rider buys the evictor post itself; a sited relay converts on SITED alone; one budget of 3 launcher builds per body covers every arm. |

## 21.1 Where the gate is wired, and why nowhere else

Two of the three expensive arms are already **team-wide published facts with
exactly one publisher each**, and that publisher is a raider standing at their
ring — the one body that can see whether a launcher of ours is on it:

| arm | publisher | field |
|---|---|---|
| hold-fire | `_cg_beat_bit` | slot 15 bit 31 (sole writer `_raid_beat`) |
| FIN window | `_fin_publish` | slot 13 bits 28–29 (eyed raiders only) |

So the gate is applied **at the publish**, and every blind consumer — the
Core's ammunition JIT, a turret across the map, a tube-siting raider —
inherits it with **no new store field and no second source of truth**. The two
first-hand readers that bypass the store (`_fin_live`'s own-eyes branch,
`_cg_corner_ok`) take the gate directly, and both are by construction bodies
with eyes on the ring.

`_cg_ev_seen` is the census (one `get_nearby_buildings` pass, round-memoised,
`_cg_evict_sited` for the geometry — the wave-11 accessor, unchanged).
`_cg_evgate` is the three-state predicate: SEEN → open; seen within
`CAGE_EVGATE_HYST` (15) → still open, because an evictor shot and rebuilt is
the normal case and flapping the one-way `cg_open` latch is worse than either
state; never seen past the deadline → dead for the game.

**Not gated, deliberately:** the ferry and the launcher themselves (they are how
establishment HAPPENS — gating them on establishment is a deadlock); a barrier
laid on a ring **seat** by an escort already standing beside it (3 Ti, no walk,
no scaled purchase — the collar's target set is untouched); and the seal census
and its markers, because the gate's own decisions are read off them.

## 21.2 Smoke — `tools/leap10_smoke.py`, 27 games, seed 2

`NOISE_ON` throughout. **This is an evidence check, not a measurement.**

**The gate is bimodal, and it is exact.** Every leg is classified by whether a
`CG evictor` marker ever fired; the expensive arms are counted as
`CG hold` + `CG open` + `FIN open` + `FIN peck` + `FIN surge`. `CG open` is the
sharpest instrument here — it can only be printed from inside `_cg_beat_bit`,
past the gate test, so its presence *is* the hold-fire arm having run.

| bot | evictor legs | expensive markers | no-evictor legs | expensive markers |
|---|---|---|---|---|
| `loki_leap10` | 9 | 125 | 4 | **0** |
| `leap10_est` | 7 | 103 | 6 | **0** |
| `leap10_off` (control, gate off) | 0 | 0 | 1 | **3** |

Zero leaks in 13 gated no-evictor legs across two forks. The control's three
markers on a leg with no evictor are the −9.0 pp population, still being paid
for, which is the whole point of the batch.

**The ratchet is gone:** `RAT` markers, whole batch = **0**. **Flags off:**
`leap10_off` emits zero `CG evictor` / `CG evgate` / `CG post` markers and the
cage still runs (86 markers), which is `loki_leap9` with the ratchet off.
**Zero tracebacks in 27 games.**

## 21.3 Establishment effort did NOT raise the rate, and the smoke says why

| | `loki_leap10` | `leap10_est` |
|---|---|---|
| legs with an evictor | **9/13** | 7/13 |
| `CG post` | 0 | 2 |
| first `CG evictor` round, `nordkap` A/B | r35 / r33 | **r5 / r7** |
| istones `TW launch` / `CG evict` | 9 / 656 | 6 / 27 |

Two runs, same direction (run 1: 8/13 vs 5/13; run 2: 9/13 vs 7/13). The arm
works where it fires — on `nordkap` it establishes at **r5–r7 against r33–r35**,
which is a different game, not a better one by a margin. But `CAGE_EST_RESERVE`
holds one of the three builds back for the post, and on the big maps the build
it holds back is **the third hop, which is what carries the rider to the ring at
all**: istones launches 9 → 6 and evictions 656 → 27.

The reserve is therefore a **trade between short and long trunks**, not an
improvement, and it is left as a flag rather than a guess:
`bots/leap10_noresv` (`CAGE_EST_RESERVE = False`) is the ablation and the panel
decides. This is the honest read — **the 50 % establishment rate was not
raised by this batch.**

## 21.4 Ablation variants, stamped

`bots/leap10_off` (`CAGE_EVGATE_ON = False` — the inertness control, and the
un-gated −9.0 pp behaviour for comparison), `bots/leap10_est`
(`CAGE_EST_RETRY = True`), `bots/leap10_noresv` (`CAGE_EST_RETRY = True`,
`CAGE_EST_RESERVE = False`).

## 21.5 Standing risks, pre-registered

1. **The gate is read from ONE body's eyes.** A raider whose view of the ring is
   blocked reads "no evictor" and publishes SHUT while one stands. That false
   negative degrades to leap6, which is the fallback by design — but flickering
   `CG evgate` markers on cells where `CG convert` fired would indict the
   census, not the plank.
2. **The gate can only make the cage RARER.** If wave 11's evictor split was
   selection (good games grow evictors) rather than causation, this batch buys
   nothing and costs the cells where the cage was winning without one. That is
   the single question the 45-map panel has to answer.
3. **`CAGE_SEQ_TIMEOUT` no longer carries the hold-fire risk alone.** A late
   establishment (r70) opens a hold-fire window at r70 that leap9 would have
   opened at r20 and released at r150. **Median kill round is the watch.**
4. **`CG convert` fired ZERO times in 27 games**, both forks, as it did in
   wave 11 (0.00/game). Wave-11 FIX 3(a) and wave-12 establishment effort (2)
   are both effectively inert: the ferry chain's last launcher is essentially
   never sited on the ring. Establishment comes from arm 4, not the ferry.
5. **`CG hold` never printed, in any game of any batch since wave 8.** The
   hold-fire arm is instrumented through `CG open` only. If the panel makes
   hold-fire the suspect, the marker needs fixing before the arm is judged.
6. **The deadline latch is per-body.** A raider that spawns at r120 into a live
   evictor still runs the cage, because `_cg_ev_seen` is asked before the
   deadline. Bounded by `CAGE_SEQ_TIMEOUT` (150), and deliberate — but it means
   the "cage abandoned" state is a property of a body, not of the team.
7. **CPU, unmeasured.** By inspection: one `get_nearby_buildings` pass per
   raider per round while the gate is undecided, round-memoised, with a
   `dsq_core > TW_CENSUS_DSQ` reject in front of the 12-tile walk.
8. **27 games, `NOISE_ON`, one seed. Not adjudicable.** The 45-map panel against
   `loki_leap6` is the bar and it has not been run.
9. **Nothing uploaded.** No `fcode submission` command of any kind was issued.

# 22. THE CHAIN BILL — loki_leap11, wave 13, 2026-08-17

`bots/loki_leap11` is `bots/leap10_est` promoted to master (its 67 % / turn-36
establishment numbers were validated at n=270, and §21.3's smoke "REGRESSION"
verdict is struck) plus **arm D, the chain deadline**.

## 22.0 What wave 12 asked for, and what its own corpus says

The wave-12 verdict named a residual: in games that never establish an evictor
the bot still paid `CG ferry` ≈ 1.09 and `CG lift` ≈ 1.26 per game **with all
three expensive arms shut**, and read that as the ferry chain being REBUILT to
game end after the gate had already given up. Arm D is the fix that follows
from that reading — a body that has not established by `CAGE_EVGATE_DEADLINE`
(80) stops rebuilding the chain.

**The premise was checked against the corpus it came from before a line was
written. It does not hold.** 540 games of `leap10_est`
(`results/wave12/replays_est/cand_vs_opp_mimic_{istones,juusto}`), every leg
split on whether a `CG evictor` marker ever fired by r80:

| | vs `mimic_istones` | vs `mimic_juusto` |
|---|---|---|
| legs | 270 | 270 |
| established by r80 | 154 (**57.0 %**) | 128 (**47.4 %**) |
| **the no-evictor half** | **n = 116** | **n = 142** |
| `CG lift`, r ≤ 80 | 1.319 /game | 1.380 /game |
| `CG lift`, r > 80 | **0.000** | **0.000** |
| `CG ferry`, r ≤ 80 | 1.172 /game | 1.204 /game |
| `CG ferry`, r > 80 | **0.000** | **0.000** |
| `CG post`, `CG sd`, `CG relay`, r > 80 | **0, 0, 0** | **0, 0, 0** |
| legs with ANY post-r80 lift or ferry | **0 / 116** | **0 / 142** |

Zero events, zero legs, both opponents, both halves. The reason is two
constants that were already equal: `CAGE_FERRY_MAX_RND` is 80 and
`CAGE_EVGATE_DEADLINE` is 80, so the ferry's own `clock` refusal has been
declining every build arm D would decline since wave 8, and `CAGE_FERRY_STALE`
(4) expires every claim arm D would refuse to serve.

**The residual bill is real, and it is EARLY.** Every titanium a doomed game
spends on transport is spent at r ≤ 80 — inside the attempt window, which is
the window the plank is required to protect. The same split says the failing
half spends *more* on transport than the winning half and collects nothing:
**1.32–1.38 lifts/game against 1.09–1.16**, ~1.2 throws against ~1.06, and
`CG evict` 0.25–0.27 against 5.2–15.9. That is the −9.0 pp population, and a
deadline at r80 cannot reach one titanium of it.

## 22.1 What arm D is, given that

It ships as an **invariant, not a saving**. The two constants are equal today
by intention and a comment; nothing enforced it, and the next person to move
`CAGE_FERRY_MAX_RND` — the obvious knob if the chain is ever asked to run
longer — would silently reopen exactly the leak wave 12 was worried about.
Arm D makes the gate own the rule.

| call site | what it refuses | reachable today |
|---|---|---|
| `_cg_ferry_try`, above the post and the cap | a new lift, a new post, a new hop, for a body past the deadline with no evictor ever seen | no — the `clock` refusal fires first |
| `_cg_ferry_launch`, after the stale test | a throw served for a claim **stamped** after the deadline | no — `_cg_ferry_try` cannot write one |

`CG chaincut r=N w=lift|ferry` is the instrument, and it is deliberately
**not** a marker for every post-deadline refusal: it fires only where arm D
declines something the ferry's own clock would have ALLOWED. A zero count is
the proof of inertness; a non-zero count is the alarm that the constants have
drifted apart. Self-destruct is untouched, and a launcher standing with a live
claim finishes its current throw.

## 22.2 The defect this batch found in its own first draft

The obvious implementation of `_cg_chain_dead` — call `_cg_evgate`, return
`cg_ev_dead` — was written, and it is **wrong in a way no marker census would
have caught.** `cg_ev_dead` is a ONE-WAY latch and `_cg_evgate` is its only
writer. Asking the gate from the ferry path sets that latch **for a rider
still walking at r81**. Under `leap10_est` that rider's first gate call happens
when it reaches the ring, so an evictor standing there at r95 is seen by
`_cg_ev_seen` *before* the deadline branch is ever reached and the cage runs —
§21.5 risk 6, deliberate. The latching draft would have retired that body's
cage at r81 for a game it was about to win, and it would have done so silently:
the chain markers it gates are zero either way.

Shipped version reads the condition and writes none of it — `cg_ev_dead` if
already latched, else `cg_ev_first`/`_cg_ev_seen`, which can only move the
answer to NOT dead. **Arm D never retires a cage; it only declines to rebuild
a chain the gate has already retired.**

## 22.3 Smoke — `tools/leap11_smoke.py`, 13 games, seed 2

12 legs of `loki_leap11` (4 big maps × 2 sides vs `mimic_istones`, 2 cells × 2
sides vs `mimic_juusto`) plus 1 flags-off leg of `bots/leap11_off` vs
`mimic_0033`.

| check | result |
|---|---|
| crashes / non-zero exits / `permanently removed` | **0 / 13** |
| `CG chaincut`, all legs | **0** — arm D is inert, as predicted |
| post-r80 chain spend (`lift`+`ferry`+`post`+`sd`+`relay`+`convert`) | **0**, all legs |
| established by r80 | 5 / 12 |
| pre-r80 chain effort, no-evictor legs (n=7) | `CG lift` 10, `CG ferry` 10, `CG sd` 7 — attempts NOT suppressed |
| normal play past r80, no-evictor legs | `CG evict` 16, `COL surge` 9, `COL brick` 3, `TW launch` 2, `TW pluck` 3; last marker r999 |
| flags-off leg (`leap11_off`) | chain runs as `leap10_est`, `CG chaincut` 0 |

The `NORMAL` row is the one that matters for "normal play resumes": the
leap6-shared arms keep firing to game end in exactly the legs where the cage's
own chain has gone quiet, and the bot plays out to r999.

## 22.4 The wider read — `tools/leap11_rate.py`, 96 legs, seeds 2–3

Both forks on the SAME 24 cells (7 maps × 2 sides vs `mimic_istones`, 5 × 2 vs
`mimic_juusto`, 2 reps). `NOISE_ON`: legs are **not** paired and single cells
are noise — read the rates.

| | `loki_leap11` | `leap10_est` |
|---|---|---|
| legs | 48 | 48 |
| **established by r80, aggregate** | **29 / 48 (60.4 %)** | **29 / 48 (60.4 %)** |
| …vs `mimic_istones` | 13/28 (46 %) | 18/28 (64 %) |
| …vs `mimic_juusto` | 16/20 (80 %) | 11/20 (55 %) |
| `CG lift` / game, r ≤ 80 (istones, juusto) | 1.286, 1.300 | 1.286, 1.250 |
| `CG ferry` / game, r ≤ 80 | 1.107, 1.250 | 1.143, 1.150 |
| `CG post` / game, r ≤ 80 | 0.250, 0.300 | 0.357, 0.300 |
| **post-r80 chain bill, no-evictor legs** | **0** | **0** |
| `CG chaincut` | **0** | n/a |
| wins | 30 / 48 (62.5 %) | 35 / 48 (72.9 %) |

Establishment is **identical in aggregate and un-suppressed** — the per-opponent
split swings ±18 pp in opposite directions on n=20–28 legs with the spawn
dispersion re-rolled per match, which is what noise at this sample size looks
like, and the pre-r80 effort rates (the thing arm D could actually have broken)
agree to within 0.04 lifts and 0.11 posts per game. The post-r80 bill reads
**zero for `leap10_est` too**, which is the batch's headline restated: there
was nothing there to cut.

The win column is **−10.4 pp and not adjudicable** (48 unpaired legs each,
`NOISE_ON`, two-proportion p ≈ 0.25). It is recorded rather than explained
away, but no mechanism connects it to arm D: `CG chaincut` is zero across all
48 legs, which means arm D never once refused an action the shipped code would
have taken.

## 22.5 Ablation variants, stamped

`bots/leap11_off` (`CAGE_CHAIN_DEADLINE_ON = False` — the inertness control;
at the shipped constants it is expected to be indistinguishable from
`loki_leap11`, and the batch above is why). Stamped by
`tools/leap11_variant.py`, the `leap10_variant.py` pattern re-pointed at this
fork.

## 22.6 Standing risks, pre-registered

1. **ARM D BUYS NOTHING TODAY, AND THAT IS MEASURED, NOT FEARED.** 540 corpus
   games plus 96 fresh ones read a post-r80 chain bill of exactly zero for the
   parent fork. Anyone reviewing this batch for a win should stop here: the
   win is not in it. What it buys is that `CAGE_FERRY_MAX_RND` can never again
   be raised without the gate noticing.
2. **THE −9.0 pp POPULATION IS UNTOUCHED, AND THE LEVER MOVED.** The failing
   half's transport bill is paid at r ≤ 80 and it is *larger* than the winning
   half's (1.32–1.38 lifts/game vs 1.09–1.16). The reachable levers are
   therefore (a) a FAILURE predicate inside the window — a rider that has spent
   its launcher budget and is still outside `CAGE_FERRY_STOP_DSQ` at, say, r40
   is not going to arrive, and that is testable on the existing corpus before
   a line is written; or (b) the establishment RATE itself, which waves 11, 12
   and 13 have now all named and none has raised (~50–60 %).
3. **`_cg_ev_seen` is polled from one more site.** Past the deadline, for the
   rider only, round-memoised. It can only move the gate toward OPEN (it
   records sightings, never deaths), but it means `cg_ev_first` may latch a
   round or two earlier than under `leap10_est` on a body whose other gate
   consumers were not reached that turn. Marker timing, not policy — and the
   96-leg batch shows no rate difference.
4. **CPU, unmeasured.** One extra `get_nearby_buildings` pass per rider per
   round, only past r80, only while `cg_ev_first < 0`, round-memoised and
   behind the same `dsq_core > TW_CENSUS_DSQ` reject the gate already uses.
5. **The bar is unchanged and unmet.** `loki_leap11` has NOT been measured
   against `loki_leap6` on the 45-map panel, and it has not been measured
   against `mate_sleipnir` (v155), which is the user's standing bar for any
   slot proposal. Nothing here is a ship recommendation.
6. **Nothing uploaded.** No `fcode submission` command of any kind was issued.

# 23. THE SEAT WAR — `loki_leap12`, wave 15, 2026-08-17

## 23.0 What wave 14 measured, and what this batch does about it

`analysis/elite_gap.md` §3 is the whole brief. Bucketing 270 pool games by how
many of our 8 delivery/heal seats the enemy held **at round 50**:

| enemy-held seats @ r50 | n | our r100 Ti | our win rate |
|---|---|---|---|
| 0–1 | 25 | 715 | **84.0 %** |
| 2–3 | 47 | 315 | **53.2 %** |
| 4–5 | 86 | 170 | **31.4 %** |
| 6–8 | 112 | 50 | **16.1 %** |

r(seats held @ r50, our r100 Ti) = **−0.759** (n=251), *stronger* than the
whole-game peak (−0.727) — which is what says the seal is upstream of the
economy rather than a trailing symptom. Median state vs `mimic_jython`: **5 of
8 seats gone by r50**. Their titanium is flat at 380–420 whether we win or
lose. We are not out-produced; we are severed at the delivery seat.

CT-1 was the wave's highest-value counter-target and the engine leaves exactly
one denial primitive for it: **bodies**. We cannot brick our own seats (our
barrier blocks our own delivery), but a tile holding a bot cannot be built on
by anyone (`engine_mechanics.md` §N.6), a builder cannot be fired on by
another builder (§F), and a body on a seat heals the Core for 1 Ti / +4 HP
(§B). Three seated bodies is +12 HP/round, which beats two band sentinels.

## 23.1 What was implemented

Fork of `bots/loki_leap11`, nothing else changed. Two flag-gated planks, full
rationale in the block at the end of `doctrine.py`.

**PLANK SEATHOLD** (`SH_ON`, default True) — up to `SH_BODIES` (3) home-side
builders station on our own free seats when an enemy unit *or building* is seen
within d ≤ 10 of our Core before `SH_UNTIL` (120).

* *Trigger*: own eyes this round (free — `_builder`'s sensing loop already
  computes that exact distance), falling back to the shared S1/S3 stamps in
  slot 13 so a body that has seen nothing gets the team's eyes.
* *Feeder carve-out*: `delivery_seats()` names the 2 seats our own conveyors
  deliver through and SEATHOLD never stations on them. Six seats are eligible.
* *Roster*: no free store slot exists (slots 0–15 are all multiplexed), so the
  cap is an **id ballot** — claim only if (peers already on a non-feeder seat)
  + (eligible home-side peers with a lower id) < `SH_BODIES`.
* *Not idle*: LPECK → heal a Core tile → heal an adjacent own building → peck
  an adjacent enemy building, with a barrier on **our own ring12** ranked
  second only to a launcher (`_sabotage_prio` ranks barriers *last*, which is
  right for a raider in an open field and wrong for the brick on our socket).
* *Eviction*: a throw needs no API call to detect — a builder cannot displace
  more than a king move under its own power, so d² ≥ `SH_JUMP_DSQ` against its
  own last position **is** a throw. The body walks straight back (the claim
  outlives `SH_UNTIL`; giving the seat up on a clock is what the throw buys)
  and remembers the launcher within pickup range of the seat it lost.
* *Chain guard*: a body carrying a trunk chain is never claimed.

**PLANK LPECK** (`LP_ON`, default True) — any of our builders orthogonally
adjacent to an enemy LAUNCHER within d ≤ 10 of our Core pecks it above all
other sabotage, spending only the **action** and never the move.
`SAP_TARGET_TYPES` always contained LAUNCHER; what was missing is that
`SABOTAGE_PRIO` ranked it 3 (below the enemy Core and below a harvester) and
`CORE_THREAT_TYPES` never let one be nominated at all. `LP_PRIO = -1` fixes the
first. The second is fixed **without** touching `CORE_THREAT_TYPES`, which is
read by `_turret` and the SLOT_THREAT latch — widening it there would re-aim
30 Ti of Sentinel.

Markers: `SH seat (x,y)`, `SH back (x,y)`, `LP hit (x,y)`, `LP kill (x,y)`.

## 23.2 The defect this batch found in its own first draft

**AN ADJACENCY-ONLY LPECK CAN NEVER KILL A LAUNCHER, AND THE FIRST SMOKE
PROVED IT.** The first build shipped LPECK as a pure adjacency peck. `LP kill`
came back 0 on every leg. The replay scan says why, and it is not a bug:

| leg (vs `mimic_jython`) | rounds an enemy launcher is within d ≤ 10 of our Core | rounds one is ORTHOGONALLY ADJACENT to one of our bodies |
|---|---|---|
| frostgate A | 678 | **1** |
| nordkap A | 947 | **5** |
| ragnarok A | 404 | **0** |
| midgard B | 110 | **1** |

A launcher is 30 HP and a peck is 2 damage: it needs **15 adjacent rounds** to
die. Eleven adjacency-rounds across eight games is not a tuning problem, it is
a geometry problem — their launchers sit near our Core and nowhere near our
bodies. `LP_SAP_TARGET_ON` is the answer: a launcher inside `LP_NEAR_DSQ` is
nominated as a SAP target, which hands it to the one walker this lineage
already trusts (the defender, one body, seat-first, committed for
`SAP_MAX_RNDS`). `_sap` re-checks `SAP_BAND_DSQ = 64` itself, so the wider
sighting band cannot pull the defender past the measured band, and it ranks
strictly below a real turret — a Sentinel is doing 9 HP a round to the Core and
a launcher is doing none.

The `LP hit` marker exists because of this defect: without it, "the plank never
gets in reach" and "the plank fires and the launcher survives" are the same
observation.

## 23.3 THE HARNESS IS NOT DETERMINISTIC AT A FIXED SEED

This is the most important thing in the batch and it is not about the planks.
Three identical invocations, same bots, same map, same `--seed 2`:

```
fcode run loki_leap12 mimic_jython maps/nordkap.map26 --tle 10 --seed 2
  -> turns 97 / 74 / 138        (winner B all three)
fcode run loki_leap11 mimic_jython maps/nordkap.map26 --tle 10 --seed 2
  -> turns 82 / 124 / 151       (winner B all three)
```

The cause is almost certainly `--tle`: a unit that overruns its CPU budget is
truncated mid-turn, and how often that happens depends on machine load. Two
runs of the same 12-cell smoke at the same seed moved the candidate from 10/12
wins to 5/12 and the *control* from 6/12 to 7/12.

**Consequence, and it applies to every wave in this file:** a 12-cell
single-seed batch measures nothing. `tools/leap12_smoke.py` therefore takes
`--seeds` and prints the disclaimer with its own table. Any strength claim
needs `tools/ab.py`-scale n.

## 23.4 Smoke — `tools/leap12_smoke.py`, 150 legs, seeds 2–7

Six POOL cells (4 maps × `mimic_jython`, 1 × `mimic_istones`, 1 × `mimic_0033`)
× 2 sides × 6 seeds, run for **both** `loki_leap12` and `loki_leap11` so every
number below is **paired on the same (opponent, map, side, seed) cell**. Plus 6
`leap12_off` legs. **0 crashes, 0 bad legs, all 150.** Raw:
`results/wave15/smoke_6seeds.txt`, replays under `results/wave15/replays/`.

**The plank fires, and the flag-off build is inert.**

| bot | legs | markers |
|---|---|---|
| `loki_leap12` | 72 | `SH seat` 200, `SH back` 64, `LP hit` 50, **`LP kill` 0** |
| `loki_leap11` | 72 | none |
| `leap12_off` | 6 | **none** |

**The seat census moved, and it is the bar this batch was built to meet.**
`e_seal8_r50` from `tools/elite_loss_decode.py` is enemy-held seats at r50; the
column below is `8 −` that, i.e. seats still ours, so **up is good**.

| paired, n = 72 | leap12 | leap11 | delta |
|---|---|---|---|
| **our seats @ r50** | **4.89** | 4.42 | **+0.47** |
| our seats @ r100 | 4.96 | 3.40 | **+1.56** |
| our Ti @ r100 (n=60) | 222.0 | 281.7 | **−59.7** |
| our Ti @ end | 620.0 | 724.9 | −104.9 |
| wins | 39/72 | 37/72 | +2 |

Cell-level sign test on seats @ r50: **32 up, 12 down, 28 tied** — two-sided
p ≈ 0.003. The mechanism is real and it is not a seed artefact.

**Per opponent, and the split is the whole story:**

| opponent | n | our seats @r50 | our seats @r100 | our Ti @r100 | wins |
|---|---|---|---|---|---|
| `mimic_0033` | 12 | 8.00 / 8.00 | 8.00 / 8.00 | 527 / 567 | 10/12 vs 12/12 |
| `mimic_istones` | 12 | 5.50 / 4.92 | **5.58 / 0.83** | 187 / 149 | 12/12 vs 10/12 |
| `mimic_jython` | 48 | 3.96 / 3.40 | 4.04 / 2.90 | **153 / 248** | 17/48 vs 15/48 |

* Against `mimic_0033` the seats are never contested (8/8 both ways), so the
  trigger never arms and the plank is correctly inert — that is the guard leg
  working, and the −40 Ti there is the only cost it charges.
* Against `mimic_istones` it is a rout in our favour: their seal takes 7 of our
  8 seats by r100 against the control and **none** against the plank.
* Against the fixture the whole wave is aimed at, the seat metric rises as
  designed **and the economy pays for it**: r100 titanium 153 vs 248, a 38 %
  cut, which is pre-registered risk R1 landing exactly where it was predicted.

**THE HONEST READ.** Seats held is up and significant; **win rate is flat**
(17/48 vs 15/48 vs `mimic_jython`, 39/72 vs 37/72 overall). This batch has
*not* shown that holding the seats wins games — only that the plank holds the
seats, and that it currently buys them with titanium. Given §23.3, no win-rate
claim at this n would be worth anything anyway.

## 23.5 The second negative: LPECK's melee arm cannot kill a launcher

`LP kill` is **0 across all 78 candidate legs** and this is now measured twice
over, from two directions:

| | `loki_leap11` | `loki_leap12` |
|---|---|---|
| our-builder-adjacent enemy-launcher rounds (72 legs) | 80 | **132** |
| enemy launchers destroyed within d ≤ 10 of our Core | 89 | 75 |

`LP_SAP_TARGET_ON` did what it was built to do — it raised our time in melee
reach of a launcher by **65 %** — and it still is not close. 132 adjacent
rounds spread across 72 games and dozens of distinct tiles never assembles the
**15 consecutive** pecks a 30 HP launcher needs, because the launcher's owner
keeps rebuilding, self-destructing and re-siting it. The launcher deaths that
do happen near our Core (89 vs 75) are overwhelmingly *theirs* — cage
self-destructs and turret kills — and the plank did not raise them.

**Bank this:** an adjacency-only, 2-damage answer to a 30 HP building that is
never adjacent is not a mechanism, it is arithmetic. If a future wave wants the
evictor dead, the reachable levers are a **turret** sited on it (LAUNCHER is
already rank 1 in `CB_TARGET_RANK`) or `CB_*` counter-battery — not melee.
`LP_ON` still earns its place as a free re-ranking (it never costs a move, and
`LP_PRIO` correctly stops us pecking a barrier while a launcher stands beside
us), but it should not be credited with kills it cannot make.

## 23.6 Ablation variants, stamped

Stamped by `tools/leap12_variant.py` (the `leap11_variant.py` pattern
re-pointed at this fork):

* **`bots/leap12_off`** — `SH_ON = LP_ON = False`. The inertness control, and
  the smoke confirms it: zero markers on 6 legs.
* **`bots/leap12_cb`** — the six counter-battery flags ON:
  `CB_LIVE_TARGET_ON`, `CB_MOBILE_GUNNER_ON`, `CB_BEARING_GATE_ON`,
  `CB_HUNT_MOVE_ON`, `CB_DRY_MAG_ON`, `CB_RANK_THREAT_ON`. This is the clean
  solo re-test the gap table asked for: CB went off inside the confounded
  turbo6→turbo4 revert and band denial has never been refuted on its own flag,
  while the pair-band siege is 39.0 % of our cage-meta losses (CT-2). Verified
  by diff: the six flags are the *only* difference from `loki_leap12` in any
  `.py` file. **Not yet measured.**
* **`bots/leap12_eco`** — `SH_ECO_GATE_ON = True`, i.e. the roster is held at
  `SH_BODIES_EARLY = 1` until `SH_ECO_HARV = 2` harvesters exist. This is the
  arm §23.4 argues for: it targets the −95 Ti against `mimic_jython` without
  giving up the early seat. **Not yet measured.**

## 23.7 Standing risks, pre-registered

1. **THE ECONOMY COST IS REAL AND MEASURED, NOT FEARED.** −59.7 Ti at r100
   overall, −95 against `mimic_jython`. Three bodies parked from the first
   sighting is three bodies not building harvesters, and on maps where the
   first sighting precedes the first harvester it is most of the opening. The
   feeder carve-out and `SH_CHAIN_GUARD` were not enough. `bots/leap12_eco` is
   the arm; until it runs, this plank is a trade and not a gain.
2. **SEATS HELD IS NOT WINS.** The dose-response in `elite_gap.md` §3 is
   *correlational*. This batch is the first intervention on it and the win
   column did not move (39/72 vs 37/72). It remains possible that seats held
   and wins share a common cause and that forcing the former buys nothing —
   that is exactly what a full `tools/ab.py` run against `mimic_jython` is for.
3. **SEATHOLD SITS BELOW SAP**, so a defender with a besieger in band still
   walks off a seat to sap it. Deliberate (CT-2 outranks one seat), but the
   r50 census under-reads on maps where a band sentinel establishes early.
4. **THE PLANK CANNOT RETAKE A SEAT.** A bricked seat is `is_tile_passable`
   False and is not a candidate. It gets there first or not at all — so a null
   r50 result on some map is evidence the trigger is late, not that bodies do
   not deny bricks.
5. **THE ROSTER BALLOT IS VISION-LIMITED.** `_sh_claim_ok` counts peers it can
   see; builder vision is r² = 20 and the home band is d² ≤ 64, so peers on the
   far side of the Core are invisible and the cap can be exceeded transiently.
   It self-corrects as bodies converge (seats are all within d² ≈ 5 of the
   Core, well inside each other's vision), but it is not a hard cap.
6. **CPU, unmeasured.** Per home-side builder per round: one extra integer
   compare inside an existing loop, plus — only while the trigger is armed —
   one `get_nearby_units` pass and up to four `get_tile_building_id` calls.
   `--tle 10` truncation is already the dominant noise source in this harness
   (§23.3), which makes a CPU regression here hard to see and worth a
   dedicated `tools/leap_cpu.py`-style pass before any ship.
7. **NOTHING UPLOADED.** No `fcode submission` command of any kind was issued,
   and none of the four bots in this batch has been measured against
   `mate_sleipnir` (v155), which is the standing bar for any slot proposal.

---

# §24 WAVE 17 — ONE BODY AND ONE GUN (`bots/loki_leap13`)

## 24.0 What wave 14/16 measured, and what this batch does about it

Two things, and they pull in opposite directions on purpose.

**(1) `SH_BODIES` 3 → 1.** The wave-14 dose-response is the evidence: the
eco-gated arm that averages ~1.4 stationed bodies a turn (`leap12_eco`) read
**61.9 %** overall against `mate_sleipnir`, and the un-gated three-body roster
(`loki_leap12`) read 64.4 % overall but **38.9 %** on the `mimic_jython` cell
that the whole wave is aimed at — while §23.4 priced the roster at **−59.7 Ti
@ r100 overall and −95 Ti against `mimic_jython`**. Seats held is a BAND, not
a monotone: three bodies standing still collapse the economy that pays for
everything else.

**(2) PLANK RG, the reactive ring gunner.** §23.7 risk R3 is the hole this
fills: SEATHOLD *cannot retake a bricked seat*, it can only get there first.
The Jython decode says ONE early raider lays the cage from t8, and nothing we
own can touch it — **a builder cannot fire on a builder** (`engine_mechanics`
§F), so turrets are the only answer in the engine. The elite pack does exactly
this, with reactive home gunners 3:1, but at r92/r129 — after their own cage
has sealed. The kill math: 40 HP intruder, 7 dmg/round, dead in six; **their
launcher cannot evict it, because a launcher throws BUILDER BOTS and a gunner
is a building.**

## 24.1 The defect this batch found in its own first draft

**A RAY SCORED ON RING COVERAGE AIMS ONE TILE BEHIND THE TARGET, AND THE FIRST
SMOKE LEG PROVED IT.** The first build scored a facing on how many of our
twelve *ring* tiles it covered — the tiles the intruder bricks. But a build
target must be orthogonally adjacent to the builder (§G), so **the body filling
one of our ring tiles is standing on the SHELL just outside the ring and never
on the tile it is filling.**

nordkap seed 2, the first leg run: the gun went up at (7,6) facing SE, covering
ring tiles (8,7) and (9,8) — and it worked, in the sense that it shot both
bricks dead at r11–r18. The builder that laid them worked the whole sequence
from **(8,8), (9,9), (10,9), (11,9)** and was never once on the ray.

`RG_WORK_DSQ = 8` is the fix: a *work tile* is `1 ≤ dsq_core ≤ 8`, ring **plus**
shell, scored by nearness to the body we can actually see with a dominating
bonus for covering it outright. A cardinal facing reaches three tiles where a
diagonal reaches two, so the score now prefers a gun laid tangentially ALONG the
shell — the line the intruder walks. Re-running the identical leg: `RG up
(11,9) f=SOUTHWEST s=20 r=4`, and `RG kill (10,9) r=84`.

Fratricide is enforced, not hoped for (mechanics table rule 9 — *turrets hit
friendly units, including your own core and your own builders*): a facing whose
ray contains a tile of our own Core footprint, a tile holding one of our own
buildings, or a feeder seat is refused **before** the score, the check is
repeated on every rotation, and it FAILS CLOSED on an unreadable tile. The
reactive gun also refuses the incumbent "nothing in sight → swing at the enemy
Core anchor" idle rotate, which for a gun two tiles from OUR Core is a line
straight across our own ring.

## 24.2 Smoke — `tools/leap13_smoke.py`, 49 legs, seeds 2–3, **0 crashes**

Paired on the same (opponent, map, side, seed) cell against `bots/leap12_eco`.
Raw: `results/wave17/smoke.txt`, replays under `results/wave17/replays/`.

| bot | legs | markers |
|---|---|---|
| `loki_leap13` | 24 | `RG up` 25, `RG rot` 44, **`RG kill` 20**, `SH seat` 22, `LP hit` 15 |
| `leap12_eco` | 24 | `SH seat` 53, `SH back` 19, `LP hit` 23, `LP kill` 2 |
| `leap13_rgoff` | 1 | **no RG markers** (the inertness leg) |

**The plank fires and it kills.** vs `mimic_jython`: a gun up in **20/20**
games, a kill in **12/20**. **`SH_BODIES` 3 → 1 shows up as designed**: `SH
seat` markers per leg fall **−58 % / −50 % / −67 %** against the control on
jython / istones / 0033.

## 24.3 The three-arm decomposition, which is the point of the batch

`bots/leap13_rgoff` is `loki_leap13` with `RG_ON = False` and **nothing else**
(verified by diff: `eco.py`, `main.py`, `raid.py` byte-identical), so it is
change (1) alone. `tools/leap13_decomp.py`, the same 20 jython cells, all three
arms paired:

| arm | | seats @r50 | seats @r100 | Ti @r100 | Ti @end | wins |
|---|---|---|---|---|---|---|
| `leap12_eco` | SH3, no RG | **4.00** | 4.20 | 183 | 326 | 9/20 |
| `leap13_rgoff` | SH1, no RG | 3.25 | 3.35 | 167 | 433 | **12/20** |
| `loki_leap13` | SH1, RG on | 3.55 | 2.80 | **196** | **462** | 8/20 |

Paired cell sign tests on seats @ r50 (up/down/tied): rgoff vs control
**5/11/4**; candidate vs rgoff **7/9/4**. On wins (x wins & y loses / reverse):
rgoff vs control **6/3**; candidate vs rgoff **4/8**.

**THE HONEST READ, and it is three separate findings.**

1. **The `SH_BODIES` cut trades seats for wins, exactly as §23.7 risk 2
   warned.** One body holds fewer seats than three (4.00 → 3.25) and wins MORE
   (9 → 12 of 20, paired 6/3). Seats held is not wins; this is the first arm in
   the file to move the two in opposite directions and it settles that the r50
   census is a proxy, not the objective.
2. **RG does not strangle the economy.** Ti @ r100 **196 vs 183** against the
   control and **+29 against its own no-RG arm**, Ti @ end 462 vs 326.
   Pre-registered risk R1 did NOT land — the `SH_BODIES` cut pays for the gun
   with change to spare.
3. **RG's win column went the wrong way (12/20 → 8/20) and this batch cannot
   adjudicate it.** §23.3 is the reason: two runs of one identical 12-cell
   fixture moved a candidate 10/12 → 5/12 at a fixed seed, so a 4-cell swing at
   n = 20 on a single draw is inside this harness's own noise band. It is a
   WARNING, not a verdict, and it is the first thing a `tools/ab.py`-scale run
   must resolve.

**Why the gun is probably late rather than wrong.** Median `RG up` is **r11.5**
(min 5, max 23) — early, as designed — but median `RG kill` is **r90**, and the
seat census at r50 moves only +0.30. In the r10–50 window the gun is alive in
20/20 legs and fires a median of **8.5 shots over 40 alive-rounds**, four legs
firing none at all. It is engaged and mostly shooting BRICKS. The binding
constraint is the same shape as LPECK's in §23.5 — per-event the mechanism
works, the RATE inside the window that matters does not. Legs with an `RG kill`
won **7/12**; legs without won **1/8**.

## 24.4 Trigger purity, audited off the replays and not off our own logs

The trigger is **enemy BUILDER BOTS ONLY** within d ≤ 8 — own eyes tested
against `EntityType.BUILDER_BOT`, team fallback on the detector's S3 stamp
(slot 13 bits 10-19), which `_arch_note` writes from `intruder=arch_s3` and
which is set from `et == EntityType.BUILDER_BOT` and nothing else. S1/S2
(turrets) live in other bits and are deliberately not read.

Every `RG up` in the guard legs was audited against the replay state on its own
round:

| leg | `RG up` | what was actually inside d ≤ 8 |
|---|---|---|
| `mimic_0033` valkyrie AB | r39 | builder d²17, builder d²40, sentinel d²25 |
| `mimic_0033` valkyrie BA | **never** | — (silent all game) |
| `mimic_istones` glacierkeep AB | r81 | builder d²2 + 4 barriers |
| `mimic_istones` glacierkeep BA | r90 | builder d²4, builder d²53, barrier |

**No firing on a turret-only state anywhere.** But the ask's prediction that
the plank would be *silent* against both guards is **REFUTED, and it is the
fixture that was wrong, not the trigger**: the replay census says `mimic_0033`
puts an enemy builder inside d ≤ 8 for **221 rounds a game** and `mimic_istones`
for **79** — so there is a legitimate builder to answer in both, and the plank
answers it (0033: seats stay 8.00/8.00 both arms, Ti @ r100 615 vs 395;
istones: 2/2 both arms, n = 2 and worth nothing). The 0033 leg that stayed
silent is the guard leg working.

## 24.5 Ablation variants, stamped

* **`bots/leap13_rgoff`** — `RG_ON = False`. The inertness control (0 RG
  markers on its leg) AND the decomposition arm of §24.3. Verified by diff:
  that flag is the only difference in any `.py` file.

## 24.6 Standing risks, pre-registered

1. **THE WIN COLUMN.** RG is −4 cells of 20 against its own no-RG arm. Below
   this harness's resolution (§23.3), unresolved, and the ship-blocker.
2. **THE GUN IS LATE TO THE KILL.** Up at r11, killing at r90. If a wave wants
   the cage denied it needs engagement inside r10–50, and the levers are the
   ammunition JIT's home-gun budget and the site's reach over the shell — not
   more guns (`RG_MAX = 1`; a second is refuted territory in this lineage,
   `T5_HOME_GUNNER_ON` and `SG_RING_TURRET` are both shipped off).
3. **THE BUDGET IS SHARED WITH THE COUNTER-BATTERY.** `SLOT_HOME_GUN` is the
   cross-unit claim and it is monotone, so a CB home turret bought first
   suppresses RG for the match, and a gun that DIES is never replaced. Both are
   deliberate; neither is measured.
4. **FRATRICIDE IS GUARDED AT BUILD AND ROTATE TIME ONLY.** A conveyor laid
   later, or one of our own bodies walking into the ray, can still put a
   friendly in front of the barrel — the ray hits the nearest occupant and does
   not care whose it is.
5. **RE-SITING IS NOT IMPLEMENTED.** `RG_RESITE_ON` is a stub. `destroy()`
   refunds nothing, so a re-site is 30 Ti plus a fresh +20 % cost scale; the
   8-way rotate is the answer instead, and `RG rot` fires 44 times over 24 legs.
6. **CPU, unmeasured.** While the trigger is armed and the gun is not up, each
   home body runs 4 sites × 8 facings of `get_attackable_tiles_from` plus the
   ray scans. Bounded by `RG_UNTIL` and by the one-gun latch, but `--tle 10`
   truncation is already the dominant noise source here.
7. **NOTHING UPLOADED.** No `fcode submission` command of any kind was issued,
   and neither bot has been measured against `mate_sleipnir` (v155).


---

# §24b WAVE 17b — THE SECOND DELIVERY ROUTE (`bots/leap13_split`)

## 24b.0 What this batch is answering

`analysis/elite_gap.md` counter-target (3), and it is the only one of the three
nobody on the ladder has ever tried: **zero splitters in 1,010 decoded sides.**
The loss mechanism it aims at is counter-target (1)'s other half — our own eight
sockets enemy-held by r50 predicts everything (r = −0.759), and a socket is not
only a heal seat, it is the ONLY tile a conveyor can deliver into a 2×2 Core
from. A trunk therefore ends in exactly one socket, and one brick on that socket
is the whole economy: r100 titanium 80 in losses against 330 in wins.

A splitter accepts input only from the tile directly behind it, has three
outputs, and **skips dead outputs** — measured in `analysis/engine_mechanics.md`
§B, where a splitter with two of its three outputs on empty ground still
delivered to the Core on every four-round cycle. One incoming line, two delivery
sockets, no code of ours in the reroute.

## 24b.1 The geometry, which is the plank and also its binding constraint

The eight sockets are the orthogonal ring tiles. The four DIAGONAL ring tiles —
`core_corners` — are the only tiles on the board orthogonally adjacent to TWO
sockets (a corner touches the two sockets flanking it; the two sockets of one
face have no common orthogonal neighbour at all). So the fork can stand in
exactly one kind of place: a corner, back-fed from outside, with both flanking
sockets among its three outputs.

`_link_path`'s goals are the sockets and every socket is a root of its reverse
flood, so no socket can ever be the parent of a socket: **the penultimate tile
of a trunk is always either the corner beside its terminal socket or the tile
straight out from it.** Arm A is the coin toss between those two.

## 24b.2 Defect one: arm A alone is dead code in nine games out of ten

And it is a measurement, not a worry. `tools/split_geometry.py` re-runs
`_link_path`'s own flood — same blocked template, same multi-source reverse BFS
from the eight sockets, same N/E/S/W expansion order, so the same first parent
wins — over all 15 pool maps, both sides:

| sample | termini | penultimate IS a corner | coverage |
|---|---|---|---|
| three nearest ores (what an opening wires) | 87 | 8 | **9.2 %** |
| every ore on the board | 554 | 92 | 16.6 % |

The reason is structural: the flood finds the NEAREST socket, and the straight
approach to a socket is its outer tile. Coming round the corner is normally one
step longer, so the corner loses.

The same enumeration priced the fix — re-run the identical flood against the
four CORNERS as goals (sockets masked out, so the chain cannot spend the tile it
is protecting), then append the socket:

| detour, extra conveyors | coverage, near-3 ores | coverage, all ores |
|---|---|---|
| **0** | **39.1 %** | 54.7 % |
| ≤ 2 | 89.7 % | 87.9 % |
| ≤ 3 | 98.9 % | 98.4 % |

`SP_DETOUR = 0` ships as the default and it is **free in every currency a trunk
has**: the chain is the same length, so the same titanium, the same +1 % scale
ticks and the same delivery latency — only its shape changes. 4.3× the coverage
for nothing. `bots/leap13_spd2` is the 2-conveyor arm (priced against
`SG_FEED2_DETOUR`'s own 3-link precedent) for a measurement to choose.

## 24b.3 Defect two: the titanium floor priced the wrong thing

The first probe declined the only forkable terminus of a frostgate game at r28
on a 14 Ti bank — `SP_TI_FLOOR = 6` was being charged on top of the splitter's
own scaled 11 Ti. **Arm A does not START anything:** it substitutes one building
for another inside a chain `_build_next_link` has already authorised and already
gated, so the marginal spend is the 3 Ti price difference, not the 6 Ti
building. `SP_TRUNK_FLOOR = 0` is the fix; the floor stays on arms B and C,
which do start forks.

## 24b.4 Defect three: arm B was polluting arm A's coverage instrument

`SP geom` is arm A's coverage denominator — one line per trunk terminus the
router picked. Arm B re-evaluates the same corners every time a body stands
beside one, and in the first batch that inflated the denominator by a third and
made the **no-bias** arm read HIGHER in-game coverage (59.1 %) than the biased
one (47.6 %), which is impossible. Arm B now reports under `SP corner`.

## 24b.5 What was implemented

* **Arm A** — `_build_next_link` lays a SPLITTER instead of a conveyor when the
  penultimate tile is a corner and a live feeder puts both flanking sockets
  among the three outputs. Falls through to the incumbent conveyor otherwise.
* **Arm A2** — `_sp_bias_path`, the corner-goal re-flood. Structurally SG arm
  1a: the same `_sg_flood` closure, the same blocked template borrowed and put
  back byte for byte, a detour cap. Not a second router.
* **Arm B** — `_sp_fork` re-lays a fork that was shot out (20 HP), and
  `SP_CONVERT_ON` upgrades a standing corner conveyor: `destroy()` is free,
  takes no action cooldown and returns its own +1 % scale in the same round. If
  the splitter build then fails the conveyor goes straight back the same round —
  the trunk is never left severed on our own initiative.
* **Arm C** — `_sp_wire_seat` lays the conveyor on the SECOND socket. Stateless
  like `_l4_repair`: the fix destroys its own condition, so the rule cannot walk
  and needs no memory — which is also what re-wires the socket after they shoot
  it out.
* Ranked in `_expand` directly ABOVE `_l4_repair` and BELOW the planned chain: a
  fork whose second socket is empty is not a slower economy, it is the
  single-socket economy it replaced.
* `_l4_repair`'s "nothing in this tree calls build_splitter" docstring is now
  false and was corrected. The rule itself is unchanged and still refuses a
  splitter as a FEEDER — an empty output is a splitter's normal state.

## 24b.6 Smoke — `tools/split_smoke.py`, 37 legs, seed 2, **0 crashes**

Paired on the same (opponent, map, side, seed) cell against `bots/loki_leap13`.
Raw: `results/wave17b/smoke.txt`, `smoke.json`, replays alongside.

| bot | legs | markers |
|---|---|---|
| `leap13_split` | 10 | `SP fork` 4, `SP seat` 2, `SP geom` 29 |
| `leap13_spnb` | 8 | `SP fork` 5, `SP seat` 2, `SP conv` 1 |
| `leap13_spd2` | 8 | **`SP fork` 11, `SP seat` 6** |
| `loki_leap13` | 10 | — (control) |
| `leap13_spoff` | 1 | **none** (the inertness leg) |

**THE MECHANISM WORKS, and this is the part worth keeping.** Traced off the
replays, every fork that went up kept delivering: the maximum gap between
arrivals at our Core after the fork round is **4–5 rounds**, which is the
harvester's own cycle. The splitter does not stall the line, does not lose two
thirds of the stacks, and does not need the second socket to be useful.

**THE REDUNDANCY WAS OBSERVED, once.** `leap13_spd2` frostgate/A: fork at (4,11)
up at r18, both flanking sockets live from r21, socket (4,10) destroyed at r39 —
**delivery resumed at r41**, through the surviving socket, with no code of ours
involved. That is the whole plank in one event. Rate: 4 of 14 fork legs ever had
two live sockets at once, and exactly 1 socket-loss-with-fork-standing event
occurred across the batch.

**THE WIN AND ECONOMY COLUMNS CANNOT BE ADJUDICATED HERE, and the file has to
say so plainly.** Two batches of this fixture, run hours apart, gave OPPOSITE
headline signs on the same 8 jython cells (batch 1: drought −86 rounds, Ti @
r100 +191; batch 2: dry% +10 pp, Ti @ end −253). Worse, the first drought metric
scored a game that NEVER DELIVERED as zero drought, which is how a control with
`ti_end = 0` in three cells read best-in-class; the harvester-anchored
re-measurement (`dry%` = share of harvester-alive rounds with no arrival in the
trailing 12) flips the paired sign test to 5/2/1, 5/3/0 and 4/3/1 in the
plank's favour while the MEANS still say the opposite, because both are
dominated by whether a cell happened to run 106 turns or 1,000. At n = 8 cells
against a fixture whose own noise floor is 6.6 pp (§23.3), none of that is a
verdict. **The guard cell is the only clean read: `mimic_istones` glacierkeep,
both sides, candidate 1/2 wins vs control 1/2, Ti @ r100 190 vs 0 and 320 vs
170, dry% 2.8/22.2 vs 9.3/25.7 — no eco regression.**

## 24b.7 Ablation variants, stamped

Each is `bots/leap13_split` with ONE flag changed and nothing else — verified by
diff, `eco.py` / `main.py` / `raid.py` byte-identical:

* **`bots/leap13_spoff`** — `SPLIT_ON = False`. The inertness control (0 SP
  markers on its leg).
* **`bots/leap13_spnb`** — `SP_ROUTE_BIAS_ON = False`. Arm A alone, i.e. the
  9.2 %-coverage draft, for the decomposition.
* **`bots/leap13_spd2`** — `SP_DETOUR = 2`. The priced ~90 %-coverage arm, and
  the one that actually forks: 11 forks and 6 wired second sockets over 8 legs
  against the default's 4 and 2.

## 24b.8 Standing risks, pre-registered

R1–R5 are in the flag block at the end of `doctrine.py` (20 HP terminus, one
heal seat spent, the fork can be pointless, coverage is geometry not choice,
round-robin latency unprobed). Added by this batch:

1. **THE FORK DIES LIKE ANYTHING ELSE ON THE COLLAR.** nordkap/B: fork up at
   r26, terminal socket gone by r32, the splitter itself gone by r46, and
   delivery stopped at 110 collected. R1 is not hypothetical.
2. **ONE TERMINUS A GAME.** `_wire_on_build` plans a chain for the FIRST
   harvester only; later harvesters queue behind it and mostly find an acceptor
   without a fresh route. A game offers roughly one forkable decision, which is
   why the coverage rate had to be enumerated offline rather than counted off a
   smoke — and why a 37-leg batch cannot move a win column.
3. **ARM A2 CHANGES THE ROUTE, AND THE ROUTE IS THE ECONOMY.** At
   `SP_DETOUR = 0` the chain is the same length but a different set of tiles:
   different exposure to their raider, a different stand tile for SAMESTOP, a
   different socket claimed. Equal length is not equal value and this batch does
   not separate the two — `leap13_spnb` exists so a real A/B can.
4. **THE SECOND SOCKET IS WIRED ONLY 40 % OF THE TIME IT IS OPENED** (4 legs of
   14 with a fork ever reached two live sockets). Until arm C lands, a fork is a
   3 Ti-dearer conveyor. The binding constraint is the same shape as RG's and
   LPECK's: per event the mechanism works, the RATE does not.
5. **NOTHING UPLOADED.** No `fcode submission` command of any kind was issued,
   and neither bot has been measured against `mate_sleipnir` (v155).


---

# §25 WAVE 18 TRACK 1 — THE CAGE-ARRIVAL DETECTOR (`bots/loki_leap14`)

## 25.0 The brief, and the measurement that refuted its premise

The ask was to "close the 23-round gap between their cage start (r9) and our
response (r32)" — the wave-15 reading that PLANK RG's first kill lands at r32–36
against a first brick at r9. `tools/eb_probe.py` re-derived both numbers off
**ground truth in the replay** (entity streams, not our own logs), 10 legs of
`leap13_split` vs `mimic_jython`, 5 pool maps, both sides, seed 2:

| map | first enemy BUILDER in d≤8 of our Core | manhattan from THEIR Core | their first brick on our r12 | `RG up` | first `RG kill` |
|---|---|---|---|---|---|
| fjordgate | r1 | 0 / 2 | r3 | r4 | r165 / r13 |
| frostgate | r3 | 6 / 7 | r6 | r4 | r109 / — |
| nordkap | r3 | 6 / 7 | r6 | r4 | — / r304 |
| midgard | r11 | 39 / 41 | r14 | r12 / r11 | — |
| ragnarok | r11 | 39 / 41 | r15 | r15 / r12 | r77 / — |

**The gun is not late. It is blind.** `RG up` lands at r4–r15, at or *before*
their first brick on every map in the pool. The 23-round figure was a
first-**kill** statistic read as a first-**build** statistic.

`tools/eb_probe2.py` then priced the real constraint over the same 10 legs:

* **Ammunition is not it** — 16 in the bank at `RG up` on 10 legs of 10, ≥ 4
  from r2 on 10 legs of 10.
* **Aim is it** — the gun stood for 52–585 rounds and had an enemy BUILDER on
  one of its three ray tiles for **0–36 of them**, and for **zero** on 4 legs of
  10. A three-tile cardinal ray against a body that walks the collar is a coin
  toss, and the coin is landing tails.

That finding is the batch's most valuable output and it belongs to nobody's
plank: it is the wave-19 lever (risk R4).

## 25.1 The defect this batch found in its own first draft

`_eb_note` published SLOT_ARCH_SEEN bit 30 with its own `write_store`, from
inside `_builder`'s sensing loop. `_arch_note` runs three lines later, rebuilds
the whole word from **last round's** buffered read, and therefore erased the bit
every single time. The first sanity leg shows it exactly: `EB detect r=11`,
then `EB hold r=12` from a peer that could not see the classification, and the
gun deferred from r12 to **r23** — an 11-round regression caused by the plank
that was supposed to accelerate it.

This is P4 SIPHON's finding (§3) re-found: **slot 13 has one canonical writer
per round and it is `_arch_note`.** The fix is that the bit travels *into*
`_arch_note` as an argument, plus a re-assert loop — the detecting body keeps
setting it until it reads it back, because `_sge_core_band` and `_fin_publish`
write the same slot from their own stale reads and one write can still be lost.
After the fix the same leg gives `EB detect r=11` → `EB gun r=12` → `RG up r=12`,
i.e. no regression, and `EB detect` count per game falls 4 → 2 as peers adopt
the published classification instead of re-deriving it.

## 25.2 Trigger purity — the one result this batch establishes

48-leg smoke, seeds 2–3, 0 crashes, 0 non-zero exits.

| fixture | legs | legs with any `EB` marker | enemy BUILDER-rounds inside our band (median) |
|---|---|---|---|
| `mimic_jython` | 20 | **20 / 20** | 303 |
| `mimic_istones` | 2 | **0 / 2** | 420 |
| `mimic_0033` | 2 | **0 / 2** | 413 |

The guard rows are the point, and they are stated as a census rather than as
silence: the detector stood in front of **~400 enemy-builder-rounds inside its
own band per guard leg and declined every one of them**, because those bodies
walked. "Did not fire" and "had nothing to fire at" are separable observations
here, and this is the first.

First `EB detect` round vs `mimic_jython`, 20 legs: r3 ×8, r4 ×4, r6, r8, r11 ×8
— the walk-clock catches midgard/ragnarok at r11 (manhattan 39–41, 28 rounds of
flight they did not have) and the small maps go at r3–r6. `bots/leap14_off`
(EB_ON=False) is inert: zero EB markers, and every new call site in `main.py` is
EB_ON-gated by inspection.

## 25.3 The arms are NOT adjudicable, and the null arm is why

100-leg decomposition, same 20 `mimic_jython` cells, all five bots in one batch:

| arm | win % | RG first kill (ground truth) | bricks STANDING on our r12 @ r50 | seats free @ r50 | Ti @ end |
|---|---|---|---|---|---|
| `leap13_split` (control) | 40.0 | 61.0 | 7.0 | 2.5 | 215 |
| `loki_leap14` (all arms) | 30.0 | 58.5 | 6.5 (lower on 10 cells of 20) | 3.0 | 260 |
| `leap14_ebonly` (**null arm**) | 40.0 | 45 | 7.0 (lower on 8) | 3.5 | 120 |
| `leap14_nopeck` | 35.0 | 45 | 7.0 (lower on 11) | 3.5 | 280 |
| `leap14_nohold` | 25.0 | 71.0 | 8.0 (lower on 10) | 3.0 | 100 |

**Read `leap14_ebonly` first.** It carries the detector with all three arms
OFF — it prints and sets a bit and changes nothing else — so it is a
behaviourally null arm, and *every column it moves is that column's noise
floor*. It moves the ground-truth first kill by **−16 rounds** and the seats
column by **+1.0**. Those are larger than anything the real arms produce.
The control itself came in at **50.0 %** on the identical 20 cells in the first
run and **40.0 %** in the second, which is the documented 6–10 pp cross-run
swing (§23.3) and the reason the −25 pp that run 1 showed for `loki_leap14` is
not a finding either.

So: **no arm of this plank is separable from noise at n = 20, and the honest
verdict on arms (a), (b) and (c) is "not measured", not "works" and not
"fails".** What can be said:

1. **Arm (c) fires per event.** 1,600–2,278 `EB peck` markers per 20 legs
   (80–114 a game) and 76–104 `EB kill` — roughly 4–5 enemy bricks deleted off
   our own collar per game, which the incumbent tree cannot do at all because
   `_sh_peck` is reachable only by the one stationed body and only after the
   launcher and both heals decline.
2. **One weak ordering worth a pre-registration, not a claim.** In both runs the
   two peck-OFF arms finished above the two peck-ON arms in the win column
   (40.0 / 35.0 vs 30.0 / 25.0). That is the same shape as wave 14's finding
   that per-event-correct home planks get paid for out of the build-out, and it
   is exactly what risk R2 predicted. It is also well inside a noise floor the
   null arm just measured at ±10 pp, so it is a hypothesis for a bigger batch.
3. **Arm (b) shipped inert on purpose** (`EB_SH_BODIES = SH_BODIES = 1`).
   `bots/leap14_eb2` is its arm and was not run.

## 25.4 Ablation variants, stamped

`bots/leap14_off` (EB_ON=False, the inertness ablation), `bots/leap14_ebonly`
(detector only — **the null arm, and the most useful bot in this batch**),
`bots/leap14_nohold` (EB_RG_HOLD_ON=False), `bots/leap14_nopeck`
(EB_PECK_ON=False), `bots/leap14_eb2` (EB_SH_BODIES=2, unrun).
Stamped by `tools/leap14_variant.py`; all five compile.

## 25.5 Standing risks, pre-registered

1. **THE HOLD IS THE ARM MOST LIKELY TO BE NEGATIVE.** `leap14_nohold` finished
   *below* the full bot in both runs, which reads as the hold helping — but
   `nopeck` finished above both, so the hold's apparent value may be entirely
   the peck's cost measured with the sign flipped. Unresolved.
2. **NOTHING HERE MOVED THE CELL.** The plank as shipped is 30.0 % against a
   40.0 % control on 20 paired cells. Whatever else is true, `loki_leap14` is
   **not** a ship candidate on this evidence and must not be uploaded.
3. **THE AIM PROBLEM IS UNTOUCHED** (R4). 0–36 target-rounds out of 52–585 is
   where the next batch should go, and it is a siting/rotation problem, not a
   detection one.
4. **n = 20 IS NOT ENOUGH FOR A WIN COLUMN.** The wave-16 DECISION memo's rule
   applies unchanged: the honest unit is the cell, three seeds of one cell are
   not three trials, and a claim needs a fresh-seed replication.
5. **NOTHING UPLOADED.** No `fcode submission` command of any kind was issued.
   v160 Heimdall (`bots/leap13_split`) remains the live submission and is
   untouched by this batch.


# §25b WAVE 18, TRACK 2 — THE FERRY RACE (`bots/leap14_race`)

The #1 team's raider is standing on our ring at **t13** and has laid its first
brick on it at **t14**. Ours reaches theirs at **t28-30** and lays its first
brick at **t35-40**. Everything downstream of arrival — the seal, the evictor,
the collar, the whole of §17–§24 — therefore starts twenty rounds late against
the one opponent it was written for. This plank is about those twenty rounds
and nothing else.

## 25b.1 The decode: why OUR ferry is slow

`tools/leap14_delay.py`, 4 legs (`leap14_diag` = `leap13_split` with
`CAGE_LOG_WHY` on and `CAGE_WHY_GAP` 3, vs `mimic_jython`, midgard +
drakkarfjord, both sides, seed 2). Launcher rounds and positions are read off
the **replay**, not off our markers; the refusal reasons are the bot's own.

| | rungs built | arrival d²≤40 | on the ring | first brick on the foe's ring |
|---|---|---|---|---|
| **them** | r2 r4 r6 r8 r10 r12 (six) | **r9–r11** | **r11–r13** | **r12–r15** |
| **us (`leap13_split`)** | r3 r5 (two; ONE on drakkarfjord) | r28–r30 | r37–r57 | r35–r40 |

Their rungs land at dEnemy 970 → 650 → 394 → 208 → 90 → 25. Ours stop after
two, and the rider then **walks at a measured 0.61 tiles a round** across a
31-tile crossing.

**The geometry was never the problem.** `_cg_ferry_try` already sites the rung
on the cardinally adjacent tile with the smallest d² to their Core — Jython's
"adjacent, one step ahead" exactly; `_cg_near_sites` already throws at maximum
range toward their Core (their measured d² = 25); rungs already self-destruct;
and our cadence is already theirs (r3, r5 = every two rounds). **We built the
right ladder and bought two rungs of it.** Three refusals, in the bot's words:

* `CG why r=1 w=clock ti=430 n=0` — `CAGE_FERRY_MIN_RND` is 2 and **the rider's
  first turn is round 1**. One free round given away with 430 Ti in the bank.
* `CG why r=5 w=cap ti=209 n=2` — `CAGE_EST_LAUNCH_CAP` 3 minus the one
  `CAGE_EST_RESERVE` holds back for the evictor post = **two hops a game**.
* `CG why r=4 w=bank ti=246 n=1` — `CAGE_FERRY_TI_FLOOR` 220 (drakkarfjord
  misses `CAGE_FERRY_ORE_NEAR` at d² 58). One hop, then money-blocked for the
  whole window — and the trace shows the bank that floor protected being spent
  by the economy anyway, 246 → 115 by r14.

## 25b.2 What PLANK SPRINT changes

Inside a window (`SPR_MAX_RND` 24) the rider runs Jython's ladder: start at
`SPR_MIN_RND` 1, up to `SPR_CAP` 6 rungs, on a bank floor (`SPR_TI_FLOOR` 60)
sized to the trunk's next build rather than to a war chest, under a total spend
cap (`SPR_TI_CAP`). The site choice, the throw, the disposal, the wait and the
hand-off at the ring are the parent's code **untouched** — §21.3's lesson was
that this machinery works and was starved.

Three deliberate restraints, all flag-ablatable:

1. **The sprint keeps its own books.** A sprint rung increments `spr_n`/`spr_ti`
   and *not* `cg_ferry_n`/`cg_launch_n`, so wave 12's reserved evictor post and
   the parent's own two hops are still unspent when the window closes. Wave 12
   measured what happens when transport eats the destination's budget.
2. **The hand-off does not move.** `SPR_STOP_DSQ` defaults to
   `CAGE_FERRY_STOP_DSQ`; `bots/leap14_c300` prices carrying the rider in.
3. **Two brakes on the trunk**: a total spend cap and a per-rung bank floor.

## 25b.3 The number the brief got wrong: a rung is not 20 Ti

Measured off the `SPR rung … ti=` markers: **rung 1 costs 28 and rung 2 costs
38.** The cost scale is team-wide, and our Core spawns builders #1 and #2 at
r1–r2 at **+20 % of scale each** (engine_mechanics C). The ladder prices
28, 38, 42, 44, 50 …, so Jython's six rungs are ~280 Ti of a 500 opening bank —
affordable to *it* because its economy is deliberately tiny (3 builders, ~7
conveyors, scale ~1.2–1.5 all game). At the brief's `SPR_TI_CAP` 90 this plank
buys **two** rungs — the same two the parent bought, one round earlier.
`SPR_TI_CAP` therefore ships at **180** (four rungs, ~148 Ti actually spent
before the bank floor takes over), with `bots/leap14_spr90` carrying the
brief's literal number as the ablation and `bots/leap14_spr300` showing that
above ~180 the binding constraint is the **floor**, not the cap.

## 25b.4 The smoke — `tools/leap14_smoke.py`, seeds 2 and 3, 97 legs, zero failures

Every arm runs **in the same batch on the same (map, side, seed) cells**: five
pool maps x both sides against `mimic_jython`, seed 2 (five arms) and seed 3
(three arms). `arrive` / `onring` / `brick` are read off the REPLAY, not off our
own markers; `sprTi` is the plank's own last `SPR rung ... ti=` marker.
Medians over the 20 pooled jython cells (10 for the seed-2-only arms):

| arm | `SPR_TI_CAP` | arrive | on ring | first brick | Ti coll r100 | spent | cells won |
|---|---|---|---|---|---|---|---|
| **`leap14_race`** | 180 | **13.5** | 22.5 | 21 | **180** | 106 | 7/20 |
| `leap13_split` (control) | — | 27.5 | 36.5 | 39 | 120 | 0 | 3/20 |
| `leap14_spr300` | 300 | 11.5 | 21.5 | 23 | **55** | 105 | 7/20 |
| `leap14_c300` (stop 8) | 300 | 13.5 | 23.5 | 21.5 | 70 | 104 | 6/10 |
| `leap14_spr90` | 90 (the brief's) | 23.0 | 29.0 | 29.5 | 160 | 64 | 3/10 |
| *`mimic_jython`, same games* | — | *10.0* | — | *13.0* | — | — | — |

**PAIRED per cell, `leap14_race` − `leap13_split`, pooled over both seeds
(sign test on the discordant cells):**

| column | n | median | faster / slower / tie | p |
|---|---|---|---|---|
| arrival (d² ≤ 40) | 20 | **−6.5** | 15 / 4 / 1 | **.019** |
| on the ring (d² ≤ 2) | 20 | **−6.0** | 16 / 3 / 1 | **.0044** |
| first brick on their ring | 19 | **−4.0** | 15 / 3 / 1 | **.0075** |
| cells won | 20 | 7 vs 3 | flips +5 / −1 | **.22** |

The transport claim replicates on a second seed and is significant on the
conservative unit. **The win claim does not and is not** — 5-vs-1 flips is
p = .22, and the in-run null says why: `leap14_race` and `leap14_spr300` differ
by a constant whose measured spend (106 vs 105 Ti) shows it almost never binds,
yet they swing 6/10 -> 1/10 across the two seeds. That is this fixture's noise
floor, measured in-run, and no win column of twenty cells clears it. §16 stands.

**The trunk.** Ti collected at r100 is 180 (race) against 120 (control) —
no collapse at `SPR_TI_CAP` 180. It IS dose-responsive: `leap14_spr300` spends
the same median 105 Ti but its TAIL (146-Ti legs) takes r100 collection to 55,
and `leap14_c300` to 70. That is the wave-14 failure mode arriving on schedule
and it is the reason the cap ships at 180 rather than higher. The brief's
`ti100 >= 150 in wins` bar is met on median (200) and NOT on the minimum (0).

Guards, seeds 2 and 3: `leap14_race` won all five guard legs it ran
(`mimic_istones` glacierkeep A and B on both seeds, `starter` valkyrie);
`leap13_split` lost glacierkeep/A on seed 3.

**INERTNESS.** `bots/leap14_sproff` (`SPR_ON = False`) reproduces
`leap13_split` tile for tile on the decode cells: first launcher r3, two rungs
(one on drakkarfjord), arrival r28/r29, first brick r35/r37, and **zero `SPR`
markers**. NOTE THE NAME. The batch was first run against `bots/leap14_off`,
which is **not ours** — wave 18's TRACK 1 agent claimed that name for its own
PLANK EARLYBIRD ablation and overwrote the file mid-batch, so the seed-2 and
seed-3 inertness lines in the raw logs describe whichever bot was on disk at
the time. One bots/ namespace, two agents working it: check a name before you
claim one, and re-run anything that turns on a shared path.

## 25b.5 Standing risks, pre-registered

1. **THE ECO COST IS REAL AND DOSE-RESPONSIVE.** r100 collection runs
   180 -> 55 -> 70 as the sprint budget rises (race -> spr300 -> c300), and
   `ti100` in `leap14_race`'s own wins has a **minimum of 0**. §14's verdict —
   leap12 paid for its plank out of the build-out and lost the game that way —
   is the live risk, and 20 cells do not clear it.
2. **THE BANK FLOOR IS THE REAL CONSTANT, AND IT IS UNPROBED.**
   `SPR_TI_FLOOR` 60 is what stops the ladder at 3-4 rungs; every cap arm in
   this batch varies the constant that does NOT bind. The next batch should
   sweep the floor, not the cap.
3. **ARRIVING IS NOT SEALING.** On-ring still trails arrival by ~9 rounds
   because the last six tiles are walked. `leap14_c300` buys them with rungs and
   is better on no column — a first, cheap refutation of "carry the rider all
   the way in".
4. **TWO SEEDS, TEN CELLS, ONE OPPONENT.** No `mate_sleipnir` (v155) leg, no
   45-map A/B, no fresh-draw replication of the win column. The wave-16 lesson
   about same-seed re-measurement applies to anything built on this file.
5. **NOTHING UPLOADED.** No `fcode submission` command of any kind was issued.


# §26 WAVE 19, TRACK 1 — THE TWO FIXES (`bots/loki_leap15`)

`bots/loki_leap15` = `bots/leap14_race` (PLANK SPRINT) + PLANK EARLYBIRD's
**detector and gun only** — the neutral cut, `EB_RG_HOLD_ON` / `EB_SH_ON` /
`EB_PECK_ON` all `False` — with two measured defects of the parents repaired.
Nothing else moves. `bots/leap15_off` is the inertness fork; `bots/leap15_gate`
is FIX 1 alone and `bots/leap15_aim` is FIX 2 alone.

## 26.0 The two defects, and what each fix does about them

**FIX 1, THE ECO GATE.** Wave 18 shipped the sprint funded from the BANK
(`ti >= cost + SPR_TI_FLOOR`, floor 60) and measured the bill: 42 of 78 legs
finished with ZERO titanium collected by r100 against the control's ~27, and
r100 collection ran 99 against `leap13_split`'s 146. A bank test cannot tell an
idle opening war chest from a bank that is idle *because the harvester it was
meant to buy has not been built yet* — both read 430.

The gate now prices a rung against REALIZED COLLECTION instead. There is no
`titanium_collected` reader in the API (`get_global_resources()` is the only
resource call a unit has, docs 155/206), so the meter is the rider's own:
`_spr_collect` sums the POSITIVE bank deltas between the rider's consecutive
turns. It is monotone (a watermark a rung can be priced against), it
UNDERCOUNTS (another body's spend between two of our turns hides the income
that paid for it — conservative in exactly the direction this fix wants), and
it includes the 10 Ti / 4 rounds of passive income, which is the floor of the
gate rather than a leak in it. Rung 1 and every rung before `SPR_FREE_RND` are
free; every later rung waits for `SPR_COLLECT_STEP` of meter movement since
the rung before it. `spr_mark` is written **only** on a rung that was actually
bought — a refusal that reset its own clock would be a gate that opens by
being closed.

**FIX 2, THE AIM.** `tools/eb_probe2.py` established that the reactive ring
gunner is neither late nor unarmed — `RG up` at r4 on every leg, ammunition
>= 4 from r2, the gun standing 52–443 rounds — and that it simply never has
anything on its ray: **rounds with a target 0, 0, 3, 8 … out of 500+**. Two
causes, both repaired here:

  1. *The site was chosen for one facing.* `_rg_gun` scored (site, facing)
     pairs jointly. A gunner is the only turret that can re-aim (docs 2287), so
     the property of a POST worth maximizing is the UNION of the rays it can
     ever swing to. `_rg_cover` counts DISTINCT work tiles over the four
     cardinal facings — and only over facings that pass the same rule-9
     fratricide test the build itself must pass, so it is a lower bound and can
     undersell a post but never oversell one. Coverage now outranks the opening
     facing in the site key; the intruder bonus survives as the tie-break
     between facings *of the winning post*.
  2. *The re-aim could not chase.* `_idle_rotate` is a forward tube's
     discipline: an eight-round self-imposed cooldown, a sticky previous
     target, and — the outright bug for this use — it computes ONE bearing
     (`p.direction_to(tgt)`), tests it, tries the nearest cardinal if that
     bearing was diagonal, and gives up. A courier bricking our collar sits two
     tiles out on a bearing that is neither. `_rg_chase` enumerates all eight
     legal facings, keeps the ones whose ray actually CONTAINS the body
     (`can_fire_from`), prefers a cardinal, re-runs `_rg_ray_safe`, and
     rotates. **And it never rotates at a body no ray reaches** — the diagonal
     case in the brief — because a rotate is 10 Ti *and* a round's fire
     forgone, so a chase that misses costs twice.

## 26.1 The defect the first smoke found in this batch's own first draft

The chase was written EXCLUSIVE: for the reactive ring gun, `_turret` called
`_rg_chase` and returned, so `_idle_rotate` never ran on that barrel. The
reason was budget hygiene — two arms spending 10 Ti on one turret makes
`RG_ROT_BUDGET` a number about nothing. The consequence was worse than the
disease: once the four rotations were spent the barrel was **welded** for the
remaining four hundred rounds, while the control still had the incumbent
discipline re-aiming all game. Time on target came in BELOW the control:
`tgt_rounds` median 2 vs 6, `tot_pct` 0.5 % vs 1.2 % (results/wave19/smoke.txt,
12 paired jython cells).

The budget test now sits on the OUTSIDE of the branch. While the chase has
budget it owns the turret; when it runs out it hands the turret BACK to
`_idle_rotate` rather than retiring it.

## 26.2 The smoke — `tools/leap15_smoke.py`, two draws, 74 legs, **0 crashes**

Both draws are 12 paired `mimic_jython` pool cells (midgard / nordkap /
frostgate x 2 sides x 2 seeds) plus 6 guard cells (2 istones + 2 0033 +
2 kladde) plus one flags-off leg, candidate and control run in the SAME batch
on the SAME cells. Draw A = seeds 41,42 (`results/wave19/smoke.txt`, and it is
the draw that found the welded-barrel defect above). Draw B = seeds 43,44,
after the repair (`results/wave19/smoke2.txt`). Per the wave-17 instrument
note the seed blocks were varied between runs and nothing unpaired is claimed.

`bots/leap15_off` printed **no** `EB` / `RG chase` / `SPR gate` marker in
either draw: the inertness leg is clean.

### FIX 1 — the eco gate: **fires, but does not move the column**

| jython cell | draw A cand / ctrl | draw B cand / ctrl |
|---|---|---|
| r100 collection, median | **205 / 35** | **90 / 140** |
| r100 collection, mean | 210.8 / 150 | 242.7 / 237 |
| zero-collection legs | **1 / 12** vs 4 / 12 | 4 / 12 vs 3 / 12 |
| arrival, median | 4 / 5 | 5 / 3 |
| `SPR rung` totals | 23 / 22 | 24 / 23 |
| `SPR gate` refusals | 6 | 3 |

The two draws point in opposite directions on the same column, which is the
jython fixture doing what wave 17 said it does. The marker counts say why the
gate cannot be responsible for either: **it refuses 3-6 rungs in 12 legs and
the arms buy the same number of rungs (23 vs 22, 24 vs 23)**. On these three
maps the rider ARRIVES at r3-r5, so almost every rung it ever buys is bought
inside `SPR_FREE_RND` and the gate never gets asked. FIX 1 is *implemented and
inert on this cell set*; the wave-18 zero-collection finding was measured over
78 legs on the full pool and this batch does not touch it. **Acceptance is NOT
adjudicated here** -- it needs the 45-map unit, where arrival is r13-27 and the
late rungs the gate exists to refuse are actually bought.

Arrival did not slip: median 4-5 against the control's 3-5, i.e. inside the
r12 bar on both draws.

### FIX 2 — the aim: **the kill clock moves, the aim instrument does not**

| jython cell, draw B | cand | ctrl | paired |
|---|---|---|---|
| first enemy builder dead in our band (`gt_kill`) | med 37, mean 45.9 | med 37.5, mean 63.9 | **cand earlier 6 / 6, p = 0.031** |
| kills before r20 | 3 / 12 | 2 / 12 | |
| `RG up` round | 3-17 | 4-24 | earlier (the EARLYBIRD waiver) |
| time on target, absolute | med 0, mean 2.3 | med 3.5, mean 37.8 | cand higher 2 / 12, p = 0.18 |
| time on target, r<=120, rate | med 0.0 %, mean 1.2 % | med 3.5 %, mean 9.5 % | cand higher **1 / 12, p = 0.070** |
| gun-up rounds inside r<=120 | mean 107.2 | mean 104.9 | 5 / 12, p = 1.0 |

**The two numbers disagree and the honest reading is that FIX 2 is NOT
established.** `tools/leap15_aimprobe.py` exists to ask whether the
disagreement is an artefact, and it half-answers: holding the denominator
fixed (gun-up rounds inside r<=120 are equal, 107 vs 105) the candidate's
time-on-target rate is still LOWER on 11 of 12 cells. That is not a
confound, that is the aim being worse on average -- even though the body dies
sooner on every discordant cell.

What the per-leg table (`results/wave19/aimprobe.txt`) shows is that the
control's big `tgt` numbers are single legs where a courier PARKED on an
incumbent gun's ray for 25-66 rounds and was not killed, while the candidate's
legs read 0-13. So both statements are true: the incumbent aim accumulates
target-rounds it does not convert, and the new aim converts sooner but
accumulates almost nothing. Which of the two wins a GAME is a question 12
cells cannot answer.

**The chase is also barely firing: 13 `RG chase` markers over 12 legs, about
one rotation a game against a budget of four.** So the measured aim delta is
dominated by the SITING change, not by the chase. That is the first thing the
measurement wave should separate -- `bots/leap15_nocover` is stamped for
exactly that.

### Guards

istones, 0033 and kladde are 2 cells each and adjudicate nothing; they are
here to catch a breach. None: wins 2/2, 2/2, 2/2 (draw A) and 2/2, 2/1, 2/2
(draw B), no column moving more than the fixture does. The kladde cell -- the
one the lineage has a fresh -12.2 breach on -- shows **no further slide** in
either draw (wins 2 vs 2 both times; r100 collection 585/430 and 575/660;
`rounds_up` 92-162). It is 4 cells in total and it is a smoke signal, not a
measurement.

## 26.3 Ablation variants, stamped

| bot | flags | asks |
|---|---|---|
| `bots/leap15_off` | `EB_ON` `SPR_COLLECT_ON` `RG_CHASE_ON` `RG_COVER_UNION_ON` = False | inertness == `leap14_race` |
| `bots/leap15_gate` | FIX 1 only (`EB_ON`, chase, cover off) | is the eco gate the effect? |
| `bots/leap15_aim` | FIX 2 + EB only (`SPR_COLLECT_ON` off) | is the aim package the effect? |
| `bots/leap15_nocover` | `RG_COVER_UNION_ON=False` | **siting vs chase**, the open question |
| `bots/leap15_nochase` | `RG_CHASE_ON=False` | ...from the other side |
| `bots/leap15_c15` | `SPR_COLLECT_STEP=15` | the gate's dial, if arrival slips |
| `bots/leap15_rot80` | `RG_ROT_BUDGET=80` | eight rotations instead of four |

## 26.4 Standing risks, pre-registered

  * **R1 A ROTATE IS A SHOT FORGONE.** 10 Ti and a one-round action cooldown.
    Bounded at four rotations a game, on the one gun this lineage builds.
  * **R2 COVERAGE IS NOT PROXIMITY**, and the smoke's aim column is the first
    evidence that the trade may be going the wrong way. `leap15_nocover`.
  * **R3 THE GATE IS UNTESTED WHERE IT BINDS.** It never fired in anger on
    three short-arrival maps. On the 45-map unit it will refuse real rungs and
    the arrival column is where that shows up first.
  * **R4 THE METER UNDERCOUNTS.** Spends by other bodies between the rider's
    turns hide the income that paid for them, so a busy economy can read as a
    dead one and stall the ladder. Conservative by design; `SPR_COLLECT_STEP`
    is the dial and `leap15_c15` is stamped.
  * **R5 EARLYBIRD'S GUN IS IN, ITS TEETH ARE NOT.** `EB_RG_HOLD_ON`,
    `EB_SH_ON` and `EB_PECK_ON` are all False here -- the neutral cut. Wave 18
    could not adjudicate those arms and this batch does not re-open them.

---

# WAVE 30 BELTEVICT

`bots/leap30_beltevict` = `bots/loki_leap18` (v162) + **ARM 4 BELT EVICT**
(`BELT_EVICT_ON`) + **F6** (`F6_TEAM_TEST_ON`, lifted verbatim out of
`bots/leap28_clean`). `bots/leap30_beltevict_off` is the same tree with both
flags False, i.e. v162. Built 2026-08-19; nothing submitted, nothing
activated, no existing bot touched.

## 30.1 The defect this answers

`results/wave29/EMERGENCY_BLEED.md` §2. **kladde v126 never attacks.** It drops
4-5 barriers across **our belt path** at `dsq_core` 2.2-6.4 and waits; two of
those games collected **0 Ti in 269 of 530 rounds** (`TiEnd` 0/3160, 0/240).
`RING_EVICT`'s target set is `sg_socket(self.core, i)` — the eight sockets, at
`dsq_core` 1-2 — so the apron is **outside its geometry** and `foe` is empty.
Nothing else in the tree reaches it: LPECK is launchers, SAP is the besieger
band, `EB_PECK_ON` is False, and F5 (the only belt arm ever built) refuses a
tile carrying an enemy building by construction and was killed on measurement
(`results/wave28/SCREEN_CLEAN.md`).

## 30.2 The arm, in one line each

| | |
|---|---|
| **target** | an ENEMY BUILDING on / orthogonally adjacent to one of OUR conveyor-chain tiles, `dsq_core <= BELT_EVICT_DSQ` (49 = d 7) |
| **"on" vs "beside"** | one test: a tile carrying their building cannot carry our conveyor, so "on the path" is observable only as "in the hole", i.e. adjacent to our belt on **two** sides. The census counts adjacencies and ranks `n >= 2` first |
| **chain filter** | a belt tile counts if it touches our Core footprint or another of our belt tiles. Reachability back to a harvester is **not** required — the case this exists for is the chain already broken |
| **peck** | nearest HOME body, `BELT_EVICT_MAX_PECKS` = 20 per TILE (30 HP barrier = 15 pecks), `BELT_EVICT_BODIES` = 2 via `_ring_evict_ok`'s id ballot, `BELT_EVICT_LIFE` = 40 per body |
| **never** | a raider by role, a body outside `BELT_EVICT_HOME_DSQ` (64) of our Core, or **a body on THEIR ring** (`_f0_plug`, the wave-27 plug rule, verbatim) |
| **no refill** | the tile is not one of our eight sockets and there is nothing to retake; sockets are dropped from this census and left to `RING_EVICT`, which can fund the retake |
| **walk** | `_belt_evict_walk`, on RING's **shared** `ring_walk_total` / `RING_WALK_CAP` budget — not a second one |
| **gunner** | `BELT_EVICT_GUN_BONUS` (6) per covered target in `_rg_gun`'s site/facing score, and a belt-covering facing is the FIRST key of `_gd_reaim`. A gunner ray clears a 30-HP barrier in 5 shots (`analysis/engine_mechanics.md`) and keeps doing it to the re-lay |
| **gunner, what is NOT touched** | `_rg_trigger`, `RG_MAX` (still one gun a match) and `_rg_ray_clean` — a ray holding any building of ours is still refused outright. Rule 9 fratricide is not traded for this |
| **ordering** | `_ring_refill` > `_ring_evict` > **`_belt_evict`** > everything else; the socket has the five-round refill window, so it goes first |

The gunner half is aimed at the OTHER half of the bleed: v162 builds **0 home
gunners in 58 % of games** against v161's 12 % (`EMERGENCY_BLEED` §3) because
`GD_SILENT_OFF` vetoes any post whose ray does not already contain one of
theirs. **An apron barrier is one of theirs, standing still, permanently in
reach of a post at `RG_SITE_DSQ`** — so the same census that feeds the peck
gives the veto something legal to point at.

## 30.3 STATIC PROOF — the off twin IS v162

`tools/analysis_scratch/w30_static_proof.py`, run 2026-08-19:

```
CLAIM 1  arm vs off twin
  main.py / eco.py / ring.py / raid.py / opening.py / sip.py   identical
  doctrine.py  2 differing lines, both of them flags:
      6949  F6_TEAM_TEST_ON   True | False
      7067  BELT_EVICT_ON     True | False

CLAIM 2  every added line vs bots/loki_leap18 (v162)
  main.py  +92  -3   COMMENT=46 GUARD=5  F6=15 BKEYS=15 INGUARD=1 STATE=9 REFACTOR=1
  eco.py   +84  -1   COMMENT=23 NEWDEF=57 GUARD=1 F6=2  INGUARD=1
  ring.py  +338 -4   COMMENT=45 NEWDEF=270 CAP=8 GUARD=2 F6=2 INGUARD=9 IMPORT=2
  raid.py  +11  -1   COMMENT=4  F6=7
  opening.py / sip.py  +0 -0
  TOTAL COMMENT=118 NEWDEF=327 CAP=8 GUARD=8 F6=26 BKEYS=15 INGUARD=11
        STATE=9 IMPORT=2 REFACTOR=1        (UNEXPLAINED=0)

CLAIM 3  BELT_EVICT_* read by the code: 13, undefined: none
         _ring_evict_ok(cap=None) defaults to RING_EVICT_BODIES: True
         call sites: ['cap=None (incumbent)', 'cap=BELT_EVICT_BODIES']
STATIC PROOF OK
```

Each class is inert with the flags down: **NEWDEF** = inside a method this
wave adds, and every call site of those is itself GUARD or F6; **GUARD** /
**INGUARD** = carries or is opened by `BELT_EVICT_ON` / `F6_TEAM_TEST_ON`;
**F6** = calls `_f6_ok`, which returns True for every tile when
`F6_TEAM_TEST_ON` is False; **BKEYS** = reads one of the four belt-mode locals
(`bkeys` is `frozenset()` with the arm off, so all four are False and every
branch they open is dead); **CAP** = `_ring_evict_ok`'s new `cap`, defaulting
to `RING_EVICT_BODIES`; **STATE** = a bare `self.x = <literal>` at spawn;
**REFACTOR** = the single line named in the script, `lane_own = ... ==
GD_OWN`, the incumbent test hoisted into a local. The five replaced lines are
listed with their reasons in the script output.

**ORDERING NOTE (`_gd_reaim`).** With the arm off `belt` is False on every
facing, so the new first element of the ranking key is the constant 1 on every
candidate — prepending a constant to a tuple key cannot change the order the
remaining elements induce, so the facing chosen is the incumbent's.

## 30.4 Mechanism smoke — 12 games vs `mimic_kladde125`, seed 1231

`bots/loki_leap18` (v162) in the SAME BATCH (VERDICT_25C: the local engine is
not run-to-run deterministic, so a control run at another time is not a
control). 6 maps (antler, drakkarfjord, fjordgate, midgard, nordkap,
yulerune) x both sides. Instrument
`tools/analysis_scratch/w30_belt_census.py`, rows in
`results/wave30/w30_belt_k125.json`.

| metric | leap30_beltevict | v162 |
|---|---|---|
| games / wins | 12 / 7 | 12 / 8 |
| belt-adjacent enemy buildings seen /g | 2.50 | 2.75 |
| **belt-adjacent CLEARED /g** | **1.00** | **1.67** |
| games with >= 1 cleared | 7 | 7 |
| our pecks at belt-adjacent tiles /g | 22.75 | 24.58 |
| our turret shots at belt-adjacent tiles /g | 0.42 | 1.08 |
| **home gunners built /g** | **0.75** | **0.42** |
| **games with 0 gunners** | **5 / 12** | **7 / 12** |
| Ti@100 (mean) | 393.3 | 397.5 |
| Ti end (mean) | 1173.3 | 1029.2 |
| **zero-Ti games** | **0** | **1** |
| collection stall round (mean) | 262.7 | 227.4 |
| stalled >= 60r before the end | 0 | 0 |

**The arm fires.** With `BELT_EVICT_LOG` on (4 debug games, reverted):
`antler_AB` 38 target scans / **14 belt pecks**, `nordkap_AB` 27 / **20** —
the 20 is the per-tile cap `BELT_EVICT_MAX_PECKS` being spent in full on one
40-HP building. Both `_BA` legs logged nothing at all: on that side the
opponent put nothing beside our belt, which is the refusal working.

**But the headline number did not move the way the arm predicts.** Clears came
in at 1.00/g against the control's 1.67/g on 12 games, and our incumbent
already pecks these tiles ~24 times a game through other arms — so on THIS
cell the population is small (2.5 buildings/g) and largely already answered.
Two honest reads, and the screen has to settle them:

1. **The cell is the wrong one.** `results/wave29/KLADDE126.md`: the mimic is
   built from v125 and **both of v126's new planks — the +63 % denser apron
   and the r50 home gunner — are absent from it**; the mimic passes 4 of 7
   admission bands. The apron this arm is aimed at is the one thing
   `mimic_kladde125` does not do.
2. **12 games is noise** on a 1-2 event/game metric.

**What did move, and it is the metric `EMERGENCY_BLEED` §3 calls the ladder's
strongest predictor:** zero-gunner games **7/12 -> 5/12** and gunners/game
**0.42 -> 0.75**, at `Ti@100` **-4.2** (393.3 vs 397.5, i.e. flat), zero-Ti
games 1 -> 0 and the collection stall 35 rounds later. That is the
`GD_SILENT_OFF` veto being handed a legal target, which is exactly the second
half of §30.2.

## 30.5 Gate

`--maps all --maps-dir maps_pool --both-sides --seeds 481 --workers 4`:

| cell | games | W-L | fails | tracebacks |
|---|---|---|---|---|
| `leap30_beltevict` vs `mimic_jython2` | 30 | 22-8 (73 %) | 0 | 0 |
| `leap30_beltevict` vs `mimic_kladde125` | 30 | 20-10 (67 %) | 0 | 0 |
| `leap30_beltevict_off` vs `mimic_kladde125` (crash check, 6 g) | 6 | 4-2 | 0 | 0 |

Engine time 3.3-3.7 s/game against the control's 6.1 s/game on the same cell —
the census is memoised per unit per round and bounded by
`BELT_EVICT_MAX_TILES`, and it does not show up in the budget.

**Win rates are gate output, not evidence.** No screen has been run: this
section reports that the build is admissible, not that it is better.

## 30.6 What a screen must do next

1. Screen on a cell that actually lays the apron — a `mimic_kladde126` built
   to `KLADDE126.md`'s bands, not `mimic_kladde125`.
2. Run the ablation `beltevict` vs `beltevict_off` vs `loki_leap18` in one
   batch, kill-only bars (VERDICT_28 §4), so F6 and ARM 4 are separable.
3. Watch the two guards this arm can break: `their_ring_rounds` (the plug
   rule — `_f0_plug` should hold it flat) and `Ti@100` (the walk budget is
   shared with RING, so a belt walk is a claim walk not taken).


# WAVE 31 RESTORE

`bots/leap31_restore` = v164 (`bots/leap30_beltevict`) + the RESTORE pair, two
flags, screened singly. Twins: `leap31_restore_off` (both False == v164),
`leap31_restore_A` (plank A only), `leap31_restore_B` (plank B only).
Brief and evidence: `analysis/wave31/TOP3_SYNTHESIS.md` §3,
`results/wave31/TOP3_{Clankers,O1,Pivot}.md`. Smoke: `results/wave31/SMOKE_RESTORE.md`.

## 31.1 The defect this answers

One disease, two entry wounds, both on OUR half of the board. Against Clankers,
O(1) and Pivot (15 unrated games, 0-15, all `core_destroyed` against us) our
income is amputated early and **never restored**.

**(a) THE DOOR — a deadlock.** Delivery needs one of OUR buildings on OUR
ring8. `ring.py::_ring_evict` (and `_ring_evict_walk`, and the v164 BELT_EVICT
twin) is gated by `_ring_eco_ready` -> `RING_ECO_HARV = 2`: *you may not clear
an enemy brick off your own socket until you have built two harvesters, and you
cannot deliver to build harvesters while the door is bricked.* Circular.
Harvesters built g1 r109 / g2 never / g3 r14 / g4 r101 / g5 r9; first attack on
our own ring8 g1 never / g2 never / g3 r38 / g4 r155 / g5 r39 — it tracks the
gate exactly, and g5 is the positive control (brick r39, peck r39).

**(b) THE HOLE — no dispatch.** `eco.py::_l4_repair` fills only a tile
orthogonally adjacent to the acting body, and the only dispatch,
`_rep_detour_target`, ranks `get_nearby_buildings()` filtered on damage. **A
destroyed conveyor is not a damaged building — it is an empty tile with no id**,
so no code path in v164 sends a body to a hole. Pivot g5: a body within 4
Manhattan steps of the one-wide hole on **74 of 76** unwired rounds,
`titanium_collected` frozen at 50 for 133 rounds; belt uptime 6-7 % in the two
games we died fastest.

## 31.2 The arms, in one line each

**PLANK A `RESTORE_EVICT_ON` — the GATE SPLIT.** `_ring_evict` and
`_belt_evict` route their shell gate through `_ring_evict_gate_ok`, which
returns True when the harvester shell is up (v164's own condition) and
otherwise only when `rnd >= RING_FLOOR_MIN_RND` **and our door is SHUT**
(`_ring_door_shut`). Nothing else moves: the CLAIM CEILING and all THREE WALKS
keep the shell gate byte for byte.

**PLANK B `RESTORE_HOLE_ON` — the second candidate class.**
`_rep_detour_target` gains, ranked first, a tile this body WATCHED DIE
(`self.rep_lost`) that is now empty, in vision, on the remembered trunk, within
`RESTORE_HOLE_STEPS = 6` Manhattan of a free non-raider home body; the body
walks to it and lays our conveyor back with the REMEMBERED FACING for 3 Ti.

## 31.3 STATIC PROOF — every call site and every guard

`tools/analysis_scratch/w31b_static_proof.py`, run 2026-08-19:

```
CLAIM 1  arm vs its three twins
  leap31_restore_off  (both flags False == v164)
    non-doctrine files identical: True
    doctrine.py differing line(s): 2
       7167  arm  RESTORE_EVICT_ON = True   |   off  RESTORE_EVICT_ON = False
       7235  arm  RESTORE_HOLE_ON = True    |   off  RESTORE_HOLE_ON = False
  leap31_restore_A    (plank A only)   1 differing line: RESTORE_HOLE_ON
  leap31_restore_B    (plank B only)   1 differing line: RESTORE_EVICT_ON

CLAIM 2  every added line vs bots/leap30_beltevict (v164)
  main.py      +22   -1   COMMENT=12  GUARD=2  STATE=8
  eco.py       +335  -4   COMMENT=137 NEWDEF=164 GUARD=3 OVR=8 INGUARD=10
                          DUPLICATE=10 REFACTOR=3
  ring.py      +76   -2   COMMENT=56  NEWDEF=18  GATE=2
  raid.py / opening.py / sip.py   +0 -0
  TOTAL COMMENT=205 NEWDEF=182 GUARD=5 GATE=2 OVR=8 INGUARD=10 STATE=8
        DUPLICATE=10 REFACTOR=3            (UNEXPLAINED=0)

CLAIM 3  the gate split, site by site
  _ring_want           SHELL  expected SHELL  OK      <- the CLAIM CEILING
  _ring_claim_walk     SHELL  expected SHELL  OK      <- the CLAIM WALK
  _ring_evict          SPLIT  expected SPLIT  OK      <- the EVICT PECK
  _ring_evict_walk     SHELL  expected SHELL  OK      <- the EVICT WALK
  _belt_evict          SPLIT  expected SPLIT  OK      <- the BELT twin
  _belt_evict_walk     SHELL  expected SHELL  OK      <- the BELT WALK
  _ring_evict_gate_ok == v164 expression when RESTORE_EVICT_ON is False: True
  _ring_door_shut requires BOTH a brick and an unfed ring: True
  RESTORE_* read by the code: 8, undefined: none
STATIC PROOF OK
```

**Every call site this wave touches or adds, with its guard.**

| # | file:site | what it is | guard |
|---|---|---|---|
| A1 | `ring.py::_ring_evict` | THE EVICT PECK | `_ring_evict_gate_ok(ct, rnd, RING_ECO_GATE_ON)` |
| A2 | `ring.py::_belt_evict` | THE BELT TWIN | `_ring_evict_gate_ok(ct, rnd, BELT_EVICT_ECO_GATE)` |
| A3 | `ring.py::_ring_evict_gate_ok` | new | `if not RESTORE_EVICT_ON: return False` before any new path |
| A4 | `ring.py::_ring_door_shut` | new | reached only from A3, i.e. only with the flag up |
| B1 | `eco.py::_rep_watch` | facing memory write | `if RESTORE_HOLE_ON and et == EntityType.CONVEYOR:` |
| B2 | `eco.py::_rep_tick` (chain guard) | `... and not ovr` | `ovr = _restore_override(...)`, False on the flag |
| B3 | `eco.py::_rep_tick` (adjacent lay) | the RELAY | `if RESTORE_HOLE_ON and self._restore_lay(ct, rnd)` |
| B4 | `eco.py::_rep_tick` (role gate) | `role != "expand" and not ovr` | as B2 |
| B5 | `eco.py::_rep_tick` (dispatch) | `if ovr_used: _restore_detour else: _rep_detour_target` | as B2 |
| B6 | `eco.py::_rep_detour_target` | the second candidate class | `if RESTORE_HOLE_ON:` |
| B7 | `eco.py::_restore_*` (6 methods) | new | each head guard is `if not (REPAIR_ON and RESTORE_HOLE_ON): return <typed empty>` |
| B8 | `main.py::_builder` | `_rep_watch` call | incumbent condition kept as the FIRST disjunct |
| B9 | `main.py::__init__` | 8 per-unit fields | bare `self.x = <literal>` |

## 31.4 THE GATE SPLIT — what is de-gated and what is not

v164 gated six things on `_ring_eco_ready`. The wave-31 split de-gates **two**,
and only the two PECKS:

| gated in v164 | wave 31 | why |
|---|---|---|
| CLAIM CEILING `_ring_want` | **unchanged** | doctrine's own r30 measurement priced the CLAIM: 8 socket conveyors by r30, 1 harvester vs 2, `titanium_collected@30` 0 vs 40. Plugs compete with the harvester budget. |
| CLAIM WALK `_ring_claim_walk` | **unchanged** | `RING_WALK_CAP` is 24 rounds/body: five bodies = 120 body-rounds walking home in the opening. The walk is what the measurement actually priced. |
| EVICT WALK `_ring_evict_walk` | **unchanged** | same walk budget, same argument. |
| BELT WALK `_belt_evict_walk` | **unchanged** | shares `ring_walk_total` / `RING_WALK_CAP`. |
| **EVICT PECK `_ring_evict`** | **SPLIT** | clearing an ENEMY brick off a socket we already own cannot ratchet (`RING_MAX_OWN` still binds the claim) and costs 2 Ti a peck. The two halves were gated together for convenience, not on evidence. |
| **BELT TWIN `_belt_evict`** | **SPLIT** | `_belt_evict_targets` drops our eight sockets, so this is never a second peck at the same brick — it clears the apron barrier standing IN the trunk one tile further out. |

`_ring_evict_gate_ok(ct, rnd, gate_on)` in full:

```
if not gate_on:                  return True     # v164: this arm's gate is off
if self._ring_eco_ready(ct):     return True     # v164: the shell is up
if not RESTORE_EVICT_ON:         return False    # v164, byte for byte
if rnd < RING_FLOOR_MIN_RND:     return False    # r1-r5 is the bootstrap
return self._ring_door_shut(ct)
```

**`_ring_door_shut` requires BOTH halves, and the second is the smoke's own
correction.** The first build de-gated on `foe` alone — "a brick exists". That
is not the deadlock. `TOP3_Clankers` §5 is *delivery needs one of our buildings
on our ring8*, so a bricked socket while ANOTHER socket still feeds the Core is
an ordinary nuisance. Measured (`mimic_juusto`, 30 g, seed 1411): on `foe`
alone the arm took **23.4 pre-shell pecks/game against the control's 3.7 and
paid -6.7 pp**, and `mimic_o1b` — which bricks a socket but never closes the
door — also went **-6.7 pp** where the arm is meant to be inert. With `feed`
empty required as well, the de-gate arms only in the state the plank was
registered for. Both reads inverted on the re-smoke (§31.6).

**Bound.** One 30-HP barrier ~= 11 builder pecks ~= 22 Ti + a 3 Ti refill,
about 7 rounds. Untouched: `RING_EVICT_TI_FLOOR`, the CLEAR+RETAKE funding
test, `RING_EVICT_TRY_RNDS` (20/tile/body), `RING_EVICT_LIFE` (30),
`_ring_evict_ok`'s id ballot, `BELT_EVICT_BODIES` = 2,
`BELT_EVICT_MAX_PECKS` = 20, `BELT_EVICT_LIFE`, `_f6_ok`.

**This is NOT `leap20_ringev`** (which `return`ed from `_builder` and forfeited
the build action, Ti@100 -15 %) and not `leap19_evict`'s resident evictor: no
new campaign, no new walk, no new target class.

## 31.5 THE HOLE CLASS — a watched-die remembered-trunk tile, NOT a BFS

`results/wave28/VERDICT_28.md` records what the wrong class costs: F5's belt
repair was POISON because its undirected BFS queued tiles that reconnect
nothing. The wave-31 class is defined by conjunction, and every clause is a
refusal:

1. **THIS BODY WATCHED IT DIE** — `self.rep_lost`, the death-watch memory
   `REPAIR_REBUILD_ON` / `REPAIR_GAP2_SEEN_ONLY` already keeps: our belt stood
   there when this body last looked, the tile is in its vision NOW, it is not
   there. Ungated, the audit behind `REPAIR_GAP2_SEEN_ONLY` read **0 of 23**
   relays of a destroyed tile and 23 DEAD HEADS.
2. **ON THE REMEMBERED TRUNK, WITH A REMEMBERED FACING** — `rest_face` records
   each of our conveyors' direction while it is ALIVE, so the relay points back
   DOWN the chain. No facing = not a candidate; only `EntityType.CONVEYOR`
   writes it, so a splitter tile is never a candidate.
3. **EMPTY AND IN VISION NOW** — `is_in_vision` then `is_tile_empty`. The
   valkyrie FIX-3 lesson: never queue a tile you cannot see.
4. **WITHIN 6 MANHATTAN OF A FREE NON-RAIDER HOME BODY** —
   `RESTORE_HOLE_STEPS`, `role != "raid"`, `dsq_core <= RESTORE_HOLE_HOME_DSQ`
   (64), and THE PLUG RULE below.
5. **PAVE-LEGAL, OWN HALF** — `pave_blocked` (the ore ban) and
   `LOKI_L4_OWN_HALF_ONLY`, both identical to `_l4_repair`'s.
6. **NOT BANNED** — a target not reached inside `RESTORE_HOLE_WALK_RNDS` is
   written off for `REPAIR_WALK_BAN` in the SAME `self.rep_ban` the incumbent
   detour uses.

**THE SEVERED-TRUNK OVERRIDE.** `_restore_severed` holds when NOT ONE of our
eight sockets carries a conveyor outputting into a Core tile **and every socket
tile is in this body's vision** (one socket unseen => False; builder vision is
r^2 = 20). It is SOUND in the direction that matters — no feeding socket means
no harvester anywhere is wired — and conservative in the other. When it holds,
and only for this class, two refusals lift: `REPAIR_CHAIN_GUARD` and the
`role != "expand"` gate. `ovr_used` keeps the incumbent DAMAGED class on
exactly v164's population (expanders, chain-free).

**BUDGET.** `RESTORE_HOLE_MAX` = 6 relays/body (`REPAIR_GAP2_MAX`'s number),
never before `REPAIR_MIN_RND`, `_eco_spendable` for the 3 Ti, and the
`RESTORE_HOLE_WALK_RNDS` = 12 time-box. Worst case 18 Ti of conveyor per body.

**Why 12 and not `REPAIR_WALK_RNDS` = 6.** 6 was sized to `REPAIR_DETOUR` = 4;
this class reaches to 6 and `_rep_tick` does not own every round of a body's
life, so at 6 the commitment expired — and expiry BANS the tile for 60 rounds,
i.e. the arm wrote off the holes it exists to fill. The 6-game `_dbg` run:
**30 commitments, 4 relays.** The ban (loki_cage's guard) is kept; only the
window is resized.

## 31.6 THE PLUG RULE, and the conflicts

**THE PLUG RULE (`results/wave27/VERDICT_27.md`).** `_restore_body_ok` calls
`self._f0_plug(ct, p)` verbatim, so **no body standing on THEIR ring8/ring12
ever gets a hole to walk to.** Wave 27 measured retasking such a body at -6
wins / +93 kill rounds / +23 pp of our own core dying. Plank A inherits the
same refusal through `_belt_home_ok` (unchanged) and, for `_ring_evict`,
through the adjacency requirement — a body pecking one of OUR sockets is by
construction at OUR ring.

**Conflicts, each resolved by rank rather than by a new flag.**

* **OPENING (`opening.py`)** — plank B cannot fire before `REPAIR_MIN_RND` = 20
  and plank A cannot fire before `RING_FLOOR_MIN_RND` = 6, so neither touches
  the r1-r5 harvester bootstrap or the r2 launcher. This is `MEDIC_MIN_RND`'s
  own lesson (two flipped maps on opening tempo).
* **RING (arms 1-3)** — plank A changes no target set and no budget; the claim
  ceiling, both claim paths and `_ring_refill`'s first rank are untouched, so
  CLEAR+RETAKE still beats the peck that created the opening. Plank B never
  builds on one of our eight sockets: a socket that has held our conveyor and
  lost it enters `rep_lost`, but `_ring_refill` / `_ring_claim` are ranked
  above `_rep_tick` in `_builder`, so the socket is retaken by RING, and if
  plank B does get there the tile it lays is the same conveyor with the same
  facing.
* **SEATHOLD (`SH_ON`)** — ranked ABOVE `_rep_tick` in `_builder` and
  unchanged, so a stationed body still holds its seat; plank B can only claim a
  turn SEATHOLD declined.
* **END (`END_QUIT_ON`)** — the A5 latch retires the forward tree at the top of
  `_raid`; both planks are home-band-only (`RESTORE_HOLE_HOME_DSQ`,
  `BELT_EVICT_HOME_DSQ`, and `_ring_evict`'s adjacency), so neither can keep a
  body forward past the latch.
* **CAGE / collar** — the cage lives at THEIR ring and is excluded by the PLUG
  rule and by `LOKI_L4_OWN_HALF_ONLY` / `REPAIR_OWN_HALF_ONLY`. Neither plank
  adds a peck at their core or their collar; `RING_EVICT`'s target set is still
  exactly our eight sockets and `_belt_evict`'s is still the apron inside
  `BELT_EVICT_DSQ` of OUR Core.
* **SAP, LPECK, the emergency Core heal, the melee recall** — all ranked ABOVE
  `_rep_tick` and above the ring arms; unchanged.

## 31.7 INERTNESS

With both flags False, `bots/leap31_restore_off` **is** v164:

1. `_ring_evict_gate_ok` collapses to `(not gate_on) or _ring_eco_ready(ct)`,
   which IS the expression it replaced at both call sites, and
   `_ring_door_shut` is reached on no path (CLAIM 3 checks the body text).
2. Every plank-B method's first line is
   `if not (REPAIR_ON and RESTORE_HOLE_ON): return <typed empty>`, and each of
   the six call sites is additionally behind `if RESTORE_HOLE_ON` or behind
   `ovr` / `ovr_used`, which `_restore_override` forces False.
3. `_rep_watch`'s facing write is behind `if RESTORE_HOLE_ON`; its call site in
   `main.py` keeps the incumbent condition as the first disjunct.
4. CLAIM 2 classifies all 433 added lines with **UNEXPLAINED = 0**, and every
   one of the 7 removed lines is a REPLACED line whose replacement reduces to
   the original with the flags down.
5. Measured, not only argued: `leap31_restore_off` vs `mimic_juusto`, 30 games,
   maps_pool, both sides, seed 1411 — **87 %**, against v164's **87 %** in the
   same batch (`results/wave31/w31b_offtwin_juusto.json`).

## 31.8 Gate

`--maps all --maps-dir maps_pool --both-sides --seeds 481 --workers 4`:

| cell | games | W-L | fails | tracebacks | stderr |
|---|---|---|---|---|---|
| `leap31_restore` vs `mimic_jython2` | 30 | 21-9 (70 %) | 0 | 0 | 0 |
| `leap31_restore` vs `mimic_kladde125` | 30 | 22-8 (73 %) | 0 | 0 | 0 |

Engine time mean 4.0 s / 3.2 s per game, max 7.5 s — in line with v164's own
batches on the same cells. **Win rates are gate output, not evidence.**

## 31.9 Standing risks, pre-registered

1. **Plank A can grind.** A re-laid brick is a fresh building id;
   `RING_EVICT_TRY_RNDS` is keyed on the TILE for exactly that reason, but a
   body that spends 20 rounds on one doorway is a body that built nothing. The
   `_dbg` run shows single tiles taking 9-12 consecutive pecks. Watch
   `harvesters@30` and `Ti@100`; both were flat-to-up on the re-smoke.
2. **Plank B's fill rate is low in absolute terms** (8.9 % on flotte2, 16.1 %
   on kladde125 of round-opportunities). The arm is real — relays on a lost
   tile 1.07/g vs the control's 0.60 — but the class is narrow by design and
   most opportunities are holes nobody remembers dying.
3. **Neither plank is measured on the axis that decides the top-3 games.**
   `TOP3_SYNTHESIS` §2: every fixture is faithful on economy shape and a
   strawman on the WEAPON. `mimic_pivot2` is the cell that would settle it and
   it does not exist yet.
4. **The pack cost is the ladder risk, not the top-3 upside.** Both planks are
   inert when nobody bricks or cuts us; when they do, the spend is <= 25 Ti per
   socket and 3 Ti per hole. Re-screen on the NEW pool after the Aug 20
   rotation before any ship proposal.

# WAVE 33 TUBE

`bots/leap33_tube` is **the live bot plus one top-5-proven repair, and nothing
else**: `bots/leap31_restore_B` — the ladder's **v165** — carrying wave 32's
**FIX 1 `TUBE_REPLACE_ON`**, the turret-replacement fix that was measured on the
five real top-5 opponents and fired there. `bots/leap33_tube_off` is the same
tree with `TUBE_REPLACE_ON = TUBE_REPLACE_HARV_ON = False`, which is v165's
behaviour exactly.

This is **not** a new idea. Every line of the arm is wave-32 code that has
already been read, screened and re-tested; wave 33 is the *carrier change* —
moving FIX 1 off v164 and onto the bot that is actually on the ladder — and
nothing more.

## 33.0 Why this bot exists — the evidence, in three numbers

`results/wave32/TEST_V166.md` decoded five unrated top-5 matches (25 games)
played by `bots/leap32_fix13` and compared them with v165's own 25. FIX 1 is
the only plank there that fired:

| quantity, per game | with FIX 1 | v165 | |
|---|--:|--:|---|
| **dead tail** — rounds that end with no forward tube | **48.2** (median 0) | 119.6 (median 85) | **p = .045**; ex-Pantheon 52.8 vs 149.6, **p = .019** |
| games **ending** with no tube alive | **9 / 25** | 14 / 25 | the headline defect (D3) |
| games where a tube was **never built** | **0** | 4 | max-alive `{1:11,2:6,3:6,4:2}` vs `{0:4,1:5,2:10,3:5,4:1}` |
| **our shots on their core** | 20.8 | 19.1 | p .83 pooled, but **ex-Pantheon 25.2 vs 12.6, +101 %** |
| empty episodes / refilled / refill latency | 27 / 18 / **18 r** | 44 / 34 / 31.5 r | fewer holes, filled ~1.8× faster |

The two planks that rode along in that test are **not** here:

* **FIX 3 `STICK_ON` = False.** It fires as a rate (re-lay gap 22 r → 1.5 r,
  p < .001) and converts to nothing: seats held/round 2.914 → 2.554, and the
  median life of a killed seal falls 40 r → 19 r pooled, 40 r → **5 r** on side
  A. It re-lays into the socket the enemy crew is standing on and clearing.
  Rate without currency is not a case; held at False.
* **FIX 2 `EXIT_GUARD_ON` = False.** Killed in `SCREEN_FIX13.md` — it was the
  source of *both* wave-32 costs (our core died p .013/.007, depth −0.16
  p .016); with it off those read p .716 and p 1.000.

`RESTORE_HOLE_ON` (plank B) stays **True** and `RESTORE_EVICT_ON` **False**,
exactly as v165 ships them. TEST_V166 §3 could find no signature for plank B on
the top-5 either way; it is cheap, it is already live, and wave 33 is not the
place to remove it.

## 33.1 Why this needed a splice and not a flag

The two lineages carry **disjoint dormant code**, not just different flag
values. `grep RESTORE_HOLE` in `leap32_fix13` returns 0 hits; `grep
TUBE_REPLACE|STICK` in `leap31_restore_B` returns 0 hits. Neither tree could be
turned into the other by stamping a flag, so FIX 1 had to be laid into v165 by
hand — and the splice is conflict-free because the two lineages edit **different
regions of different files**:

| module | v165 (`leap31_restore_B`) vs v164 | fix13 vs v164 | resolution |
|---|---|---|---|
| `raid.py` | **byte-identical to v164** | +225 lines, 22 hunks | take **fix13's, wholesale** — there is nothing of v165's to lose |
| `ring.py` | +76 lines @157/@464/@859 | **byte-identical to v164** | keep **v165's** |
| `eco.py` | +339 lines @2771-3258 | +84 lines @439 | both, **2 332 lines apart** |
| `main.py` | +23 lines @231/@1448 | +6 lines @258 | both, **27 lines apart** |
| `doctrine.py` | +184 lines, pure append @L7087 | +249 lines, pure append @L7087 | both tails, appended in order |
| `opening.py`, `sip.py` | identical in all three | identical | untouched |

**Zero symbol collisions**, re-derived from the built tree rather than trusted:
794 module-level names in `doctrine.py`, 90 `EcoMixin` methods, 115 `RaidMixin`
methods, 82 `Player` methods — **no duplicate at any level in any module**.

The eco and main blocks are **not** FIX 1 itself; they are what fix13's
`raid.py` *calls*. `eco.py`'s +84 are `_exit_free` / `_exit_ok` /
`_exit_refuse` (FIX 2), which fix13's raid.py calls at 12 sites and which
return the no-op on the first line under `EXIT_GUARD_ON = False`; `main.py`'s
+6 are `self.stick_n = 0` and its comment, which raid.py's STICK block reads and
which is dormant under `STICK_ON = False`. Omitting either would make the
wholesale `raid.py` raise. Taking both, with the flags off, makes them inert.

## 33.2 STATIC PROOF — every claim re-derived from the built tree

Builder and checker: `tools/analysis_scratch/w33_splice.py` (`--check` re-runs
the proof without rebuilding; exit 0 == all green). It verifies, in order:

1. **Provenance per module.** `raid.py` == `leap32_fix13`'s byte for byte;
   `ring.py`, `opening.py`, `sip.py` == v165's byte for byte; the other three
   are the spliced files at their expected lengths (`doctrine.py` 7 520,
   `eco.py` 4 322, `main.py` 4 754).
2. **The three inserted blocks are byte-exact donor text** at the ordered
   offsets: eco.py L440-523 (84), main.py L275-280 (6 — v164's L258 is v165's
   L274, because v165 inserts 16 lines at L231), doctrine.py L7272-7520 (249),
   the last differing from fix13's only at the one ordered `STICK_ON` stamp.
3. **Nothing was removed.** Every one of v165's lines still appears, in order,
   in every module except `raid.py` — where v165's copy *is* v164's and is
   replaced by design.
4. **No duplicate symbol** at module level or inside any class (see §33.1).
5. **The six flags**, read back from `doctrine.py`, each defined exactly once:
   `TUBE_REPLACE_ON=True`, `TUBE_REPLACE_HARV_ON=True`, `STICK_ON=False`,
   `EXIT_GUARD_ON=False`, `RESTORE_HOLE_ON=True`, `RESTORE_EVICT_ON=False`.
6. **The off twin differs by the flag lines and nothing else** — `doctrine.py`
   L7480 and L7484, zero differing lines in the other six modules.
7. **Inertness of the dormant code** — `_exit_ok`/`_exit_refuse` return the
   no-op on their first line under `EXIT_GUARD_ON=False`; `stick_n` initialised.
8. **Cross-module call resolution**, the splice's one real risk: every
   `self.<name>(...)` in the tree resolves to a method defined in the tree.
   **0 unresolved in `leap33_tube`, 0 in v165, 0 in fix13** — the splice
   introduces no call whose definition stayed behind in the other lineage.

`py_compile` clean on all seven modules of **both** bots.

## 33.3 What FIX 1 actually is, in this tree

Unchanged from `WAVE 32 — FIXIT` §32.1, which remains the reference. In one
paragraph: `SIEGE_MASS_ON`'s discount, which drops the bank floor from
`LOKI_FWD_TI_FLOOR` (40) to `SIEGE_MASS_TI_FLOOR` (6), is gated
`if SIEGE_MASS_ON and n >= 1`. It cheapens tube 2 and tube 3 and can never
cheapen the replacement of a dead **last** tube (`n == 0`) — which is the state
of every zero-tube round D3 measured. The repair is an `elif` beside it
(`raid.py:1272`) plus the same `elif` on the walk gate (`raid.py:1829`), so a
raider is not released to build a replacement and then refused the walk to the
nest.

`_tube_replace_ok` (`raid.py:1719`) **fails closed**: it requires `live` — the
raw `_live_fwd_guns` return — to be a literal integer `0`, and `_live_fwd_guns`
returns `None`, not zero, when the body cannot see the siege band. A raider
across the map cannot read its own blindness as "the tube is dead, buy another".
The monotone `SLOT_FWD_GUN` is used only as the EVER-EXISTED test, which is the
one question a monotone counter answers correctly.

`ti_floor` only ever moves **down**, at both sites, so
`builds(FIX1 on) >= builds(FIX1 off)` always: the arm cannot refuse a tube v165
would have bought. No store write, no slot, no reserve, no accumulator (the FUND
lesson) — the tube is funded from the bank that exists in that round or it is
not bought.

`TUBE_REPLACE_HARV_ON` is the one arm with an economic cost: it drops
`LOKI_FWD_MIN_HARV` 2 → 1 **in the replacement state only**, on the ground that
a replacement is by construction not an opening — a tube already stood, so the
economy the floor protects already existed.

## 33.4 Gate

`tools/arena.py leap33_tube {mimic_jython2, mimic_pivot2} --maps-dir maps_pool
--seeds 481 --both-sides --workers 8` — **60 games, 60 completed, 0 failed, 0
tracebacks, 0 stderr bytes** (`results/wave33/gate_tube_{jy2,pv2}.json`).
Win rates are gate output, not evidence: 18-12 vs `mimic_jython2`, 23-7 vs
`mimic_pivot2`; engine time mean 4.6 s / 4.5 s per game, max 7.5 s.

## 33.5 Screen vs the LIVE bot — **HOLD. No kill clause fires; the pooled bar is missed by 0.2 pp.**

`tools/ab.py leap33_tube leap31_restore_B --panel mimic_jython2,mimic_o1b,mimic_juusto,mimic_flotte2,mimic_pivot2
--maps-dir maps_pool --reps 3 --seeds 1551 --workers 8 --quiet --replay-dir replays/w33_screen
--out results/wave33/screen_tube.json` — **1 080 games, 649 s, 0 fails / 0 tracebacks / 0 stderr bytes.**
Seeds 1551-1553 verified unused (highest prior 1543); mirror auto; 90 games/cell paired on map·side·seed.

| cell | `leap33_tube` | v165 | Δ/game | p |
|---|--:|--:|--:|--:|
| `mimic_jython2` | 65.6 % | 63.3 % | **+2.2 pp** | .832 |
| `mimic_o1b` | 81.1 % | 83.3 % | −2.2 pp | .815 |
| `mimic_juusto` | 86.7 % | 92.2 % | **−5.6 pp** | **.062** |
| `mimic_flotte2` | 73.3 % | 77.8 % | −4.4 pp | .481 |
| `mimic_pivot2` | 75.6 % | 76.7 % | −1.1 pp | 1.000 |
| **pooled (450 pairs)** | **76.4 %** | **78.7 %** | **−2.2 pp** | **.343** |

Cell-level paired: −8 of 150 cells (−5.3 pp), p .096. h2h **47.8 %** against an in-run mirror null of **56.7 %**.

**The four pre-registered kill clauses, all clear:** worst cell `juusto` −5.6 pp p .062 misses the −8 pp magnitude
bar · our core died **20.0 % vs 18.0 %, +48/−39, p = .391** · Ti@100 294.8 vs 301.5 = **−2.2 %** · `fail_games` 0.
**The PASS-for-ladder bar (pooled ≥ −2) reads −2.2 and is MISSED by 0.2 pp → HOLD, not PASS.**

## 33.6 Mechanism — `w33_tube_census.py`, 450 paired replays → `results/wave33/census_tube.json`

FIX 1 is **live and measurable even on fixtures that barely kill tubes** (the panel kills **4.8 %** of ours; the
real top-5 kills 75 %). The pre-registered cut is the 57 of 450 pairs (12.7 %) where a tube actually died.

| quantity | `leap33_tube` | v165 | paired p |
|---|--:|--:|--:|
| **tubes alive @ r100** (all 450) | **1.504** | 1.396 | **+70/−31, p < .001** |
| ...**tube-death pairs** (57) | **1.754** | 1.333 | **+23/−2, p < .001** |
| ...`pivot2` tube-death pairs (23) | **2.130** | 1.391 | **+15/−0, p < .001** |
| zero-tube rounds after the first | **0.6 %** | 1.3 % | +7/−17, **p .064** |
| dead tail, tube-death pairs | **4.9 r** | 22.2 r | .625 (n=4 discordant) |
| **empty episodes / refills / refill latency** | **15 / 13 / 6 r** | 21 / 18 / **12.5 r** | .146 / .180 |
| tubes built /game | **2.553** | 2.464 | +111/−84, p .062 |
| games ending empty · never built | 2.9 % · 2.4 % | 3.6 % · 2.9 % | .607 · .774 |

**The one bar that reads against the arm is `rebuilt_after_death`, 13 vs 18** — and it is the exact denominator
artifact `TEST_V166` §1 already flagged: *it counts episodes that REFILLED*, and episodes fell 21 → 15. The arm
makes fewer holes and fills the ones it makes twice as fast (12.5 r → 6 r). This is reported as **NOT MET as
written**, not re-defined: the bar was pre-registered in that form and it fails in that form.

**Dormant code confirmed dormant:** FIX 3 relays 0.284 vs 0.209 (p .321) and seats/round 3.469 vs 3.451 (p .536)
— no relay rate, as with `STICK_ON` False it must be. FIX 2 self-bricked exits **570 vs 622** (p .029): the guard
is OFF (v165's 622 sits exactly at v164's own 615/622 from wave 32), and the candidate's drop is downstream of
tubes standing longer, not a refusal — a refusal would show as a *bounded* count, and none of the 14 guarded sites
can fire. Guards flat: belt .642/.668 (p .220), harvesters lost .438/.440, depth@r50 3.0/3.0, turns 290.5/285.1.

## 33.7 The off twin, empirically — as close to v165 as v165 is to itself

The static proof (§33.2 items 6-7) is the real evidence. The empirical check is bounded by engine
non-determinism and says only that: over `mimic_jython2` × 15 maps × both sides at seed 481,
**v165 run against itself reproduces only 7/30 games exactly** on (winner, turns, condition);
`leap33_tube_off` reproduces **8/30** of v165's. Win counts 12, 13 and 14 of 30 across the three runs.
The off twin is inside the engine's own reproduction noise, which is the strongest statement this harness
can make. `results/wave33/{off_twin_jy2,v165_jy2,v165_jy2_repeat}.json`.

## 33.8 Standing risks, pre-registered

1. **The pooled −2.2 pp is the ladder risk and it is not dismissible as noise just because p = .343.**
   Three of five cells are negative and the cell-level test reads p .096. If this bot goes up, the pull-back
   bar must be set on rating, not on mechanism.
2. **`mimic_juusto` −5.6 pp p .062 is the cell to watch.** It is the only cell with a one-sided run (0 favour
   the candidate, 5 favour v165). Nothing in FIX 1 predicts a juusto-specific cost; it may be the extra tube
   spend at a socket-attacking opponent. A `juusto` ablation of `TUBE_REPLACE_HARV_ON` alone would settle it.
3. **h2h 47.8 % vs a 56.7 % mirror null** is the widest own-bot gap wave 33 measured. Directive 3 makes this a
   guard, not a verdict — but it is a guard that did not clear.
4. **The case for this bot is the top-5 evidence, not this screen.** The panel kills 4.8 % of our forward tubes;
   the opponents that decide the ladder kill 75 %. This screen can say *not obviously harmful* and no more.


# 37. WAVE 37 — PLANK RANK: the counter-battery is *reached*, not re-priced

**Carrier** `bots/leap37_rank` = LIVE **v168** `bots/leap35_fix1only` + the one block at the end of
`doctrine.py` and its two call sites in `main.py`. **Twin** `bots/leap37_rank_off` = the same tree with
`RANK_ON = False`; `diff -r` between them is that one line.

## 37.1 The defect, named twice

`results/wave35/SCREEN_P1B.md` finding 1, repeated as `results/wave36/SCREEN_YARD.md` §4's recommendation.
Over **925 instrumented P1-state rounds** (a live besieger inside `HUNT_BAND_DSQ` of our Core with no home
turret answering) the CB **gate** opened 63 times — 3.3× the parent — and `_try_counterbattery` was reached
on **~3 %**. `_defend` was entered on 33 of the 925; the buy loop on 22; two gunners were bought in 30 games.
The price half of the CB family works and is worthless: the routine it funds is at the bottom of `_builder`'s
job ladder and behind a `role == "defend"` test exactly one body a match satisfies (`LOKI_DEFEND_SEAT = 4`,
never replaced when it dies). `results/wave33/TEST_V167.md` defect #2 prices the miss: `their_ge2` separates
16 % wins from 63 %, and it is Pantheon's 20/20 rule.

## 37.2 The cut

In the P1 state the **nearest eligible HOME body** runs `_try_counterbattery` — the existing routine, at its
existing prices — from a rank above the errand work that eats the turn. No price change, no new build path,
no gate change. It **spends the ACTION and never the turn** (the LPECK/RG construction), so the body still
makes its ordinary move and everything below re-tests `get_action_cooldown()` itself.

**Ranked BELOW:** the universal adjacent Core heal (P1b was killed for skipping it — this arm never does),
OPEN prefill/trunk, RING refill and RING socket evict, and THE PLUG RULE (`_f0_plug`, verbatim).
**Ranked ABOVE:** BELT evict, LPECK, RG, SAP, SEATHOLD, REPAIR, SIPHON and the whole role split.

## 37.3 The state, and the one test the defender's gate does not make

`_cb_over_heal`'s state minus the role test and minus the bank test, plus: `_enemy_type_at` must read a live
**GUNNER or SENTINEL** on the threat tile *this round* (`RANK_TURRET_ONLY_ON`). That is the brief's "enemy
forward turret" and it is the ghost filter `SLOT_THREAT` needs — the store named a tile holding no enemy at
all on 893 ladder-loss rounds. A ghost and a wandering builder both buy nothing here, so the arm cannot spend
a 30 Ti turret (and +10 % on the global cost scale, for ever) on a transient.

## 37.4 `RANK_BODIES = 1` without a comm slot

Comm writes are at best one round old, so a claim cannot cap a within-round race. The cap is an **election**:
defer to any friendly builder this body can see that is inside the home band and strictly closer to the
threat, ties on entity id. Vision is r²=20 and the band r²=41, so the residue (two bodies that cannot see
each other) is closed one layer down — the first body's turret is a building beside it and the second body's
`_live_home_gun` then shuts the state.

## 37.5 Pre-registered risks

1. **Core death is the kill clause.** This family has killed on core-death twice. The arm buys turrets in a
   state where the parent bought nothing; every Ti spent is a heal not bought later.
2. **`RANK_TURRET_ONLY_ON` may make the arm too quiet.** Wave 34's classification read a turret on ~34 % of
   CB targets; if the elevation never fires the verdict is NOTHING, not a kill.
3. **The panel under-prices sieges.** `mimic_pivot2` is the only cell with 5.7 besieger arrivals/game; the
   other four are 1.1–4.6 and measure noise around an inert arm (`SCREEN_P1B.md` §3.4).
