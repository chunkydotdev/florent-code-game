# Plank inventory: mining the old heads for present-then-dropped mechanisms

**Date:** 2026-08-08 · **Arm:** research (read-only; no games run, no bot edits)
**Deliverable for:** the plank-inventory ask registered at `docs/coordination.md:5665-5673`, `:5684-5685`

## Version stamp

| role | dir | ladder version | lines |
|---|---|---|---|
| **modern head** | `bots/_v91osb/` | **v79 "Eir 10"** (live; ship commit `82074d6`, md5 `6a909e72`) | 5,388 |
| old head A | `bots/_v68si/` | **v53** "v68-saboteur-escort" | 2,002 |
| old head B | `bots/_v70mh/` | **v54** "v70-respawn-convergence" | 2,195 |
| already-priced variant | `bots/_v70th/` | turret-hunting; merged into v55 `_v70cm` | 2,463 |
| s10-11 experiment fan | `bots/_v70cg _v70cm _v70ec _v70rp _v70sb _v70sm _v70st` | dev branches | 2.2-2.6k |

**Motivating datum:** tape row `field-sweep-9v` (`results.tsv:222`), 9 heads × kladde/band/cad × 30,
810 games, interleaved same-batch per instrument. Pooled /90: v77 83.3, v75 81.1, v79 80.0,
**v53 78.9, v54 77.8**, v73 77.8, v66 72.2, v64 71.1, e6e 65.6. ARC finding: the two oldest
heads outscore the entire v64→e6e middle era.

---

## 0. Two premise corrections, up front

Both matter more than any individual plank below.

### 0.1 The middle era did not SHED mechanisms. Nothing was dropped.

Verified by code, three independent ways:

1. **Function-set diff `_v70mh` → `_v91osb`: zero functions removed.** All 45 defs in the old
   head exist in the modern head; every one is same-size or larger.
2. **Removed code lines: 45 total across 13 functions**, and every one is a *replacement*
   (a bare call swapped for a gated call — e.g. `ct.get_global_resources() < cost` →
   `not self._eco_spendable(ct, cost)` at `_build_next_link`), not the deletion of a mechanism.
3. **Constants never drifted.** `MAX_BUILDERS=5, ECO_CAP=18, ECO_NEED=3, REPLACEMENT_MAX=8,
   REPLACE_TI_FLOOR=250, REPLACE_MIN_RND=60, LAUNCH_GIVEUP_RND=180, LAUNCH_STALL_RNDS=36,
   MELEE_FIRST_MAX_WALL_FRAC=0.015, INTRUDER_CORE_DSQ=20, INTRUDER_FORGET_RNDS=8` are
   byte-identical in `_v70cm` (v55), `_v76e51` (v66) and `_v91osb` (v79).

Only two module constants exist in an old head and not the modern one — `SLOT_LINKS_DONE`
and `SLOT_HOME_SENT` — and **neither is a plank** (§4).

The trough therefore is not a shedding story. The documented mechanism for lost value in that
era is **suppression, not deletion**: dispatch-order lockout (the universal adjacent heal sits
above role dispatch, so `_try_counterbattery` fired *once per game* — `docs/spitball.md:417-425`),
monotone gate ratchets (`SLOT_HOME_GUN` counts rubble as a live gun — `results.tsv:131`),
fuel-precondition circularity (`HUNT_MIN_HEALERS=2` needs a 3rd body, which needs ti≥250, which
the raid prevents — `docs/spitball.md:64-71`), and timing-window mismatch (`MEDIC_MIN_RND=150`
misses the r63-390 window where the farm actually dies — `docs/spitball.md:70-73`).

**The real shelved set is not in the old heads at all — it is the v70 experiment fan**, six dev
branches built in s10-11 and never merged forward. That is what this document inventories.

### 0.2 The ask's motivating precedent is itself refuted

The sweep note says "x3r0's v70th revival already proved one shelved plank shippable"
(`docs/coordination.md:5668`, `:5681-5682`). That claim was **retracted 23 minutes earlier in
the same file** (`:5562-5565`) and then refuted by measurement: the `_v70th` docstring is
inherited boilerplate present verbatim in all of `opp_v67, v68, v69, v72, v74, v76, v78`, and
measured distance puts v78→`_v70mh` at **1,856 changed lines (second worst of nineteen bases)**
against v78→`opp_v68` at **341** (`docs/research/v78-first-read-2026-08-08.md:22`;
`docs/coordination.md:5584-5588`).

The ARC numbers stand on their own. The "shelved plank proved shippable" support does not.
**Nothing in this document should be priced on that precedent.**

---

## 1. Ranked dropped-plank table

Rank = (evidence strength when alive) × (orthogonality to the modern head) × (plausible field
value today). Every "absent" verdict is by code, not docstring.

| # | Plank | Source | What it did | Evidence when alive | Why dropped | Revival cost | Pricing test |
|---|---|---|---|---|---|---|---|
| **1** | **Converter/spawner reserve agreement** | `_v70cg:653` | While the Core is bleeding, raise the ammo-conversion titanium floor to `builder_cost + margin` so the converter cannot drain the bank below the price of the replacement builder | Never isolated. Its *diagnosis* is measured and is now doubly on the record: the cad_probe dead-zone shape (`cad_probe` build: 0 spawns after r4 in a 405-round game) and the hive `core_destroyed@787` decode (bank pinned 2-12 Ti for 500 rounds; 0 of 270 builder attacks landed within dsq≤41 — `docs/spitball.md:64-71`) | Rode a package that failed its gate on a *different* instrument (cad_probe 63.3 vs v55's 65.0, `HANDOVER.md:561`); never separately screened | **Orthogonal, ~1 line.** No slot. Does not touch roles, deny arm, ferry, or OS | Det legs vs **kladde_probe hive** + **cad_probe**, paired against `_v91osb`; instrument = rounds-with-live-builders < POP_FLOOR while `SLOT_UNDER != 0` |
| **2** | **Ore-barrier denial** | `_v70sb/_v70sm` `_deny_ore_{tiles,ready,target,build}` | Saboteur plants a 3 Ti Barrier on an empty **enemy-side** ore tile, vetoing a Harvester there; re-denies tiles whose Harvester died. Capped 6/unit, off below 100 Ti bank, self-shutoff after 8 refusals, refuses unknown map anchors | **Measured positive on its own target:** halves kladde's hive collection **8880 → 4120** (`elo_history.tsv:99`). Supporting census: opponent rebuild latency 41-400 rounds, 2 of 14 deaths never rebuilt; 13/16 eider + 3/6 hive enemy Harvester builds land after our earliest reach; last build r845/r748 | **PARKED, not refuted** — "our farm still dies; hive residual = own-economy survival, not denial" (`elo_history.tsv:99`). Then the line jumped tracks entirely when x3r0 took the slot with v56 (`HANDOVER.md:548-555`) | **Low.** Its two infrastructure deps already ship: `core_anchor_exact()` (`_v91osb:1220`) ≡ its `known_enemy_core_for` guard, and `map_grid`/`map_ores`. Graft point in `_saboteur` (between `_try_siege_build` and `_sabotage_prio`) is unchanged. No slot. Orthogonal to the siphon deny arm — different target class | Det legs vs **kladde_probe** (its measured target) + guard vs **band_probe**; primary instrument is *enemy* delivered-Ti, not our win rate |
| **3** | **Interceptor body-block** | `_v70cg:_intercept` | Instead of chasing a raider it cannot attack, the role_n 1 interceptor stands in the **doorway** — the tile one cardinal step from the raider toward our Core. Builders are mutually impassable and thrown raiders walk their last tiles (throws reach r²≤26), so it costs 0 Ti and 0 action; falls back to the old chase if the doorway is a wall/building/behind the raider | Never independently screened. Magnus-scouted from ladder play; built against the decoded CAD insertion class (0-5 loss `e40a6c01`: Launcher r1, 2-3 thrown raiders, sentry ~r11 at core-dsq 10-41, kill median r361) | Rode the same `_v70cg` package that failed the cad_probe gate; attribution for that failure was later resolved as **seed amplification, not a knob regression** (`elo_history.tsv:112` — v55 control 16/16, every cg knob-subset 8/16; `_v70cg` kladde flat paired 81.0 vs 81.9) | **Low-medium, and it has a free trigger waiting.** Confined to `_intercept`; role numbering is unchanged across eras so role_n 1 still lands. **PLANK FT already detects exactly this raider** and writes `SLOT_UNDER = 2` — and that 2 has **zero behavioural consumers**: all seven live readers (`:2151, :2530, :2538, :2801, :3473, :3771, :4075`) are truthiness tests, and the only `== 2` reads are the writers' own no-downgrade guards. FT is a detector with no responder | Det legs vs **cad_probe** paired against `_v91osb`. **Topical:** the same sweep flagged v79's cad leg at **53.3 vs v75/77's 73-77** |
| 4 | **Ore steal** | `_v70st` `_enemy_acceptor_adjacent`, `ORE_STEAL_*` | Upgrade of #2: build *our* Harvester on their ore instead of a Barrier — same denial, plus impassable, plus it scores tiebreak #2. Guards the donation trap (never adjacent to an enemy acceptor), never writes `SLOT_HARVESTERS`, capped 3/unit at cost+150 | **Screened, mixed:** eider 8/16 held, hive **0/16** — "steal margin (cost+150) never met on hive, poverty-gated to barrier mode" (`elo_history.tsv:102`) | Parked with the denial family pending the own-farm survival fix | Medium — strictly rides on #2 being revived first; adds harvester +5% scale creep to our own rebuilds | Only after #2 prices positive; then an A/B of steal-vs-barrier on the *same* deny tiles |

---

## 2. Per-plank detail

### Plank 1 — Converter/spawner reserve agreement (highest confidence, smallest change)

**Code-level.** `_v70cg/main.py:653`, inside `_core`, immediately before the ammo conversion:

```python
if ct.get_hp() < ct.get_max_hp():
    ti_floor = max(ti_floor, ct.get_builder_bot_cost() + SIEGE_SPAWN_MARGIN)
```

The modern head's equivalent line is `ti_floor = 12 if (under or weapons) else 52`, and the one
raise that exists is explicitly *peacetime only*: `if E1_AMMO_FLOOR_ON and not under:`
(`_v91osb:1948-1953`).

**Why this is a live gap, not a superseded one.** Four facts compose:

1. `SPORKS_AMMO_ON = False` (`_v91osb:1047`), so the **legacy** branch owns ammo policy and the
   `ti_floor = 12` line is the live one.
2. `convert_ammo` runs **before** the spawn block in `_core` and re-reads `ti` after converting,
   so conversion has first claim on the bank.
3. Conversion is `amt = min(16, ammo_target - ammo, ti - ti_floor)`. It stops when the magazine
   is full — but under siege turrets are *firing* (sentinel 10/shot, gunner 4/shot), so the
   magazine is continuously below target and the drain is sustained, not one-shot.
   `hive_magazine` sets `ammo_target = 256` (`:1919`).
4. The POP_FLOOR refill spawn requires `ti >= ct.get_builder_bot_cost()` — 30 base, 74+ scaled.
   **Eir 6b's own comment concedes the refill is "bank-gated"** (`_v91osb:642`).

So under a sustained siege the converter can hold the bank at 12 Ti while the population-floor
refill — the very mechanism built to answer siege population collapse — cannot afford a body.
This is precisely the dead zone `_v70cg` named, and its comment (`_v70cg:640-651`) says it was
first surfaced by the cad_probe build: *"a converter floor below the spawner's threshold means
the bank oscillates in the dead zone between them and no builder is ever spawned again
(measured there: 0 spawns after r4 in a 405-round game)"*.

**Partial supersession — be precise about which half.** `_v70cg`'s siege plank had two halves.
The **respawn** half *did* merge: `SIEGE_RESPAWN_ON` (`_v91osb:435`) relaxes the floor to
`ti >= builder_cost + SIEGE_HEAL_RESERVE_TI` at `:2044-2047`. The **converter reserve** half did
not — and the modern head's comment at `:430-432` explicitly waves it off: *"The Core's ammo
conversion already keeps its own under-siege floor of 12 … this extends the same idea to the
builder economy paths."* But 12 < `builder_cost + 16`, so the siege respawn override it merged
is fundable only from a bank the converter is allowed to take first. The two shipped halves
disagree by construction.

**Field-transfer honesty.** Its diagnosis is not era-bound — it is arithmetic between two
constants both still live in `_v91osb`, so unlike the planks below it does not depend on the
field looking like it did in s11. But it has **never been measured in isolation**, and the
package it rode failed its gate. Do not claim a gain; the pricing test is a det leg pair.

### Plank 2 — Ore-barrier denial

**Code-level.** Four methods in `_v70sb/main.py` (`_deny_ore_tiles` :1430, `_deny_ore_ready`
:1468, `_deny_ore_build` :1476, `_deny_ore_target` :1539) plus `known_enemy_core_for`.
"Enemy side" is strictly-nearer-their-anchor by Manhattan distance to the nearest 2×2 footprint
tile, ties excluded. Bounded at `ORE_BLOCK_MAX = 6` per unit (each barrier is +1% on the same
conveyor/splitter/barrier scale our own economy spends from), `ORE_BLOCK_TI_FLOOR = 100`,
`ORE_BLOCK_FAIL_MAX = 8` self-shutoff, plus a self-trap guard requiring one other passable
cardinal neighbour. It refuses to run at all where the anchor pair is not in `CORE_PAIRS`.

**Absence verified.** The only `build_barrier` call in `_v91osb` is the map-gated hive bunker at
`(20,4)` (`:3766-3769`) — the same single site `_v70mh` has. No ore denial in any form.

**Evidence when alive.** `elo_history.tsv:99` — the mechanism *worked on its own metric*:
kladde's hive collection halved **8880 → 4120**. It was parked because a different residual
bound: our own farm still died, so denial did not convert to wins on that map.

**One blocker has since been retired.** `ORE_BLOCK_FAIL_MAX` existed only because the team had
not verified barriers can stand on ore. That was later settled from 376 cached replays — 44 of
370 surviving barriers stand on `ENV_ORE` — and the note says so explicitly: *"unparks `_v70sm`
design space"* (`docs/spitball.md:342`, `:587`;
`docs/research/2026-08-07-fanout/findings/thread6_barrier_geometry.md:30`).

**Revival cost — genuinely low.** Both infrastructure dependencies already ship in the modern
head: `core_anchor_exact()` (`:1220`) is functionally `known_enemy_core_for`'s guard, and
`map_grid`/`map_ores` are present. No store slot needed (the ledger is per-unit). The graft
point in `_saboteur` is byte-unchanged from `_v70sb`. Contention is only for the saboteur's
action budget, now shared with `_os_early` (rounds ≤ 40, role_n 0 only) and `_sabotage_prio`.

**Conflict check against modern machinery:** the deny arm (`SIPHON_DENY_ON`) targets enemy
*conveyors tapping our harvesters* — a different target class entirely, so the two are
orthogonal. PLANK HS's seat ban is Core-local and cannot collide with enemy-side ore. PLANK E2B
bans paving conveyors *onto* ore, which is a compatible doctrine, not a conflicting one.

**Field-transfer honesty — this is the weakest link.** All of this plank's evidence is
**vs-field-of-its-era**: kladde_probe as frozen in s11, plus a census of the s11 map pool. The
denial book warns that whole probe samples from our v53-59 era had to be **retired as stale**
(`docs/research/denial-adjudication-2026-08-07.md:29`, `:95`). Worse, the barrier *family* has
accumulated a consistent negative record since: barrier prophylaxis refuted by geometry
(`665be1e`), bait-barrier refuted on a Core-target confound (`fb2172d`), CAD ferry-barrier parked
by pre-mortem (`b2e0218`), and thread 6's finding that reactive deletion (~40 Ti of attacks kills
a landed sentinel) beats prophylaxis everywhere. Ore denial is a *different* mechanism from all
three — it denies an economic investment before it is made, not a turret plant — but the prior
is unfavourable and should be stated in any routing package.

### Plank 3 — Interceptor body-block

**Code-level.** `_v70cg`'s `_intercept` splits the escort path from the raider path. On the
raider path it computes `door = tp.add(tp.cardinal_direction_to(nearest_core_tile(tp, core)))`,
navigates to it rather than to the raider, and once standing on it spends the action on a
nearby target. Falls back to the old chase whenever the doorway is impassable, unreachable, or
already behind the raider.

**Absence verified.** `_v91osb`'s `_intercept` (`:4263`) has no doorway logic — it is the v53
chase form plus two later guards (PIECE S1 own-building fire guard, and the escort stalemate
ledger `escort_watch`/`escort_ban`).

**Why it ranks 3 despite having the weakest standalone evidence.** Three things compose:

1. **It is free.** No titanium, no action, no store slot. The failure mode is "reverts to
   today's chase".
2. **The modern head already ships the detector it lacked.** PLANK FT identifies a
   launcher-thrown raider by pure move-rule geometry (`manhattan(enemy builder, their Core) >
   round + 2`) and encodes it as `SLOT_UNDER = 2`. That state currently changes **nothing** —
   verified: every one of the seven behavioural readers is a truthiness test, and the only two
   `== 2` reads are the writers' own no-downgrade guards. FT is a detector with no responder,
   and body-block is the responder it was scouted for.
3. **It is topical right now.** The same sweep that motivated this document flagged **v79's cad
   leg at 53.3 against v75/v77's 73-77** (`results.tsv:222`), and body-block was built
   specifically against the decoded CtrlAltDefeat insertion class.

**Caution — the pre-r120 argument cuts both ways.** `_v70cg`'s own comment offers body-block as
*the* pre-r120 answer to an inserted raider precisely because early *hunting* was refuted
(eider 8/16 → 0/16). That argument is intact. But `_v70cg` as a package still lost its
cad_probe gate 63.3 vs 65.0, and although the snowflake damage was later attributed to seed
amplification rather than a knob (`elo_history.tsv:112`), **no ablation ever isolated
body-block itself**. Treat it as unpriced.

**Field-transfer honesty.** The mechanic it exploits — builders are mutually impassable, cannot
attack units, and thrown raiders walk their final tiles — is an engine property, not an opponent
habit, so it does not go stale. What *is* era-bound is the claim that CAD-class raiders walk a
blockable doorway; the current CAD probe is `cad_probe` md5 `6d0e955f…`, and cad_probe carries
**attribution-only standing**, so a cad leg alone cannot ship it.

---

## 3. Not worth reviving

Nine items. One-line reason each.

1. **`_v70ec` labour reserve** — REFUTED with a number: gating link spending inverted the income
   bootstrap, eider collected **9390 → 3160** by ablation (`docs/strategy-log.md:47-49`); the
   modern head cites this failure by name in `_eco_spendable`'s docstring (`_v91osb:2144`).
2. **`_v70ec` conveyor-churn rebuild ledger** (`CHURN_TILE_BUILDS`/`CHURN_REBUILD_WAIT`) — its
   diagnosis is excellent (146 conveyors for 13 harvesters vs the winner's 65 for 16; +1% team-wide
   scale each) but it was bundled with the reserve and refuted as one unit ("reserve/rebuild-cap"),
   never isolated; the surviving idea shipped narrowed as `SIEGE_HEAL_RESERVE_TI` + `_eco_spendable`,
   and the churn itself was attacked from a different angle by PIECE F (fewer dead heads) and
   PIECE E2B (no paving onto ore). Re-isolating it means contradicting a stated measurement.
3. **`HUNT_EARLY_MIN_AREA` early-hunt waiver** (`_v70cg:227`) — self-refuted in its own source
   comment by ablation (kladde eider 8/16 → 0/16 with the waiver on, 8/16 with only it off);
   pre-r120 hunting relocates the fjordgate disease to every map.
4. **`HUNT_BAND_DSQ = 41`** — not dropped at all; **already merged** (`_v91osb:159`), present
   from `_v76e51` onward.
5. **`SIEGE_HURT_RNDS` / `SIEGE_SPAWN_MARGIN` respawn half** — superseded by `SIEGE_RESPAWN_ON`
   (`:2044`) and the more general POP_FLOOR refill; only the converter-reserve half survives as
   plank 1.
6. **`SLOT_LINKS_DONE` (slot 9)** — not a plank: two writes, **zero reads**, in both old heads.
   Dead telemetry. Its index was legitimately reclaimed for `SLOT_HEAL_BUDGET` (K').
7. **`SLOT_HOME_SENT` (slot 13)** — not a plank: a bare `= 13` declaration in `_v68si` with **no
   other occurrence in the file**. (Note: the same name in `docs/v79-analysis.md` refers to
   *x3r0's* v79 slot 13, a different thing.) Our slot 13 is `SLOT_DEFEND_BEAT`, live since v54.
8. **`self.forward_barriers`** — initialised to 0 in every head from `_v68si` to `_v91osb` and
   **never read or written anywhere**. A pre-v53 vestige; cleanup candidate, not a plank.
9. **Multi-healer convergence / builder respawn / defend-role succession / melee-first / launch
   insertion / counterbattery / siege planning / `CORE_PAIRS`** — all **present** in `_v91osb`
   (several altered and bounded, none removed). There is nothing to revive.

---

## 4. Revival-cost constraints that apply to any plank

- **Store slots: 15 of 16 are live.** Index **5 (`SLOT_ECO_READY`) is provably free** — four
  write sites (`:1796, :2128, :3731, :3978`), **zero reads**, and there are no numeric slot
  literals anywhere in the file, so the audit is complete. That is the one cheap slot, and it is
  the same pattern used to justify reclaiming slot 9 for K'. All three planks above need **no**
  slot; spend index 5 only on something that genuinely needs a team-wide counter, and remember
  writes are buffered one round with last-write-wins.
- **`SLOT_UNDER` is tri-state (0/1/2)** since PLANK FT. Any revived writer must preserve the 2 —
  there is a no-downgrade invariant at `:1777-1790` and `:2300-2302`.
- **Role numbering did not change between eras** (`_v91osb:2200-2227` ≡ `_v70mh:578-602`, same
  code and comments). Old role_n-keyed code ports cleanly. Two caveats: role_n 0 now owes the OS
  standoff plant in rounds ≤ `OS_EARLY_RND` (40) and is exempted from two recall paths there;
  role_n ≥ 5 now converges as a healer.
- **Three regions are shipped-but-dead** — `B8_ON = False` (9 call sites), `SPORKS_AMMO_ON =
  False` (the whole alternative ammo policy), `HS_SEAT_BAN_CONVEYORS = False`. Code there looks
  live and is not; plank 1 sits directly beside the SPORKS block, so read the flag before editing.
- **The head has zero behavioural opponent identification** and states the reason (`:1085-1089`):
  the commitment window closes before recognition could name a class. Any revived mechanism must
  gate on map geometry or ship unconditionally — never on a behavioural read of the opponent.

---

## 5. Honesty ledger

- **The trough may be a field story, not a plank story.** v53/v54 were measured against the
  s10-11 field; v64-e6e against a field that had already absorbed x3r0's v79 line and forked our
  own Eir 4 into `wave_ghost`/opp v67. The sweep controls for instrument (same three probes,
  same batch) but *not* for the possibility that the middle era's regressions were specific to
  opponents it faced and the probes now over-represent. Per-plank transfer risk is stated in
  each section; plank 2's is the highest, plank 1's the lowest.
- **No plank below is claimed to gain anything today.** Each row carries a pricing test, not a
  projection. Planks 1 and 3 have never been isolated at all; plank 2's only positive number
  (8880 → 4120) is an *opponent-economy* measurement, not a win-rate one.
- **Wilson CIs overstate** on this arena: a seat-decided per-map row is ≈2 distinct games, not
  2×seeds (`elo_history.tsv:112`, `HANDOVER.md:572-574`). Prefer paired det legs and
  identical-rows fingerprints over per-map swings.
- **cad_probe is attribution-only standing**, so plank 3 cannot ship on a cad leg alone even if
  that leg is strong.
- **The docstring trap held here too.** `_v70cg`, `_v70cm` and `_v70rp` all carry `_v70th`'s and
  `_v70sb`'s headers describing mechanisms they do not contain. Every presence/absence verdict
  in this document was taken from function-set and constant diffs, never from header text.
