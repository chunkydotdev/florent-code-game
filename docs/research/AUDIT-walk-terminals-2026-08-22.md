# AUDIT — walk terminals in `bots/_v632heim`, and the freeze invariant on the s57 tapes

**GAME CONTEXT.** This is in-game analysis for the Florent Code League, a
sandboxed bot-vs-bot programming competition played on a simulated grid under
organiser-approved rules. Every "freeze", "chew", "kill", "threat", "intruder"
and "attack" below is an in-engine event between competing game bots — a piece
acting, or failing to act, per the engine's documented rules. Nothing here
concerns real systems, networks or people. The audit is READ-ONLY on `bots/`;
**zero platform matches were played** (the tape half decodes replays that
already existed).

Commissioned by the research arm for QUEUE row **#130 half (a)** — the
stand-on-your-own-target freeze. **This document audits and measures. It
contains no fix design; the ports are the builder's.**

---

## PROVENANCE

| input | path (verbatim) / identity |
| --- | --- |
| the row being answered | `QUEUE.md` row **#130** |
| the attribution that produced the class | `docs/research/ATTRIBUTION-keeper-fivecell-2026-08-22.md` |
| **audit target** (builder's working tree) | `bots/_v632heim/` — `main.py`, `sk_roles.py`, `sk_core.py`, `sk_common.py`, `sk_maps.py` |
| audited file identity | `sk_roles.py` md5 `2e54be9fe80d32048dd84b65fe531ad7` (380,031 b, mtime 2026-08-22 23:10 local) · `sk_maps.py` md5 `9827632596ef7d082ed1642dce9f6b20` (277,721 b, mtime 23:07 local) |
| **known-good / known-bad controls** | `bots/_v628compose/sk_roles.py` (mtime 15:46 local) — belt step-off guard, and the un-ported ore walk |
| tapes | `scratchpad/s57_heim0/t_p11_f1/*.replay26` (30 cells) · `scratchpad/s57_heim0/t_leash_f1/*.replay26` (30 cells) |
| event walker (reused, not re-implemented) | `scratchpad/s54_klad_lib.py` `Game` over `tools/replay_census.py` primitives |
| cell enumeration | `scratchpad/s57_heim0/e46p1_lib.py` `cells_at` |
| wire field reference | `tools/replay_schema.md` |
| this audit's scripts (session scratchpad, **not committed**) | `walk_sites.py` (site enumeration) · `freeze_detect.py` + `freeze_run.py` + `freeze_trace.py` (the invariant, its four validations, per-round adjudication) · `out.txt` (full 284-row N≥20 table) · `freeze_check2.py` (the author's independent from-scratch re-implementation of the invariant, used to cross-check the headline rows) — all under `/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/1ae1d0c6-9409-4fd1-a875-e962ebbc738f/scratchpad/` |

Repo at `a94383ad5`, written 2026-08-22T21:13:58Z (`date -u`). Interpreter
`.venv/bin/python` 3.13.7.

⚠ **The audited tree is being edited live by the builder** (`sk_roles.py` grew
372,719 → 380,031 bytes during the audit window). Every line number below was
**re-verified against the md5 recorded above** after the enumeration was
complete; a later edit will shift them.

---

## THE DEFECT CLASS, restated as a mechanical test

The class is not "a body stops moving". It is one specific engine fact meeting
one specific code shape:

1. **Builds, attacks and heals are ORTHOGONAL-ADJACENCY-ONLY.** A builder bot
   cannot build on, attack, or heal the tile it is standing on.
2. **`_bfs_direction` answers `CENTRE` when the goal is underfoot**
   (`sk_common.py:986-989`): the goal set is `[tidx]` when the target tile is
   free, and `if start in goals: return Direction.CENTRE`. `_nav` then returns
   `False` without moving (`sk_common.py:1117-1118`).
3. ⇒ **A walk whose target is a tile the body must ACT ON, and which the body
   can legally STAND ON, has a terminal state with no legal act and no motion.**
   Whether that terminal is a bounded pause or a permanent freeze depends
   entirely on whether anything re-plans.

**The corollary that decides most rows, and it is why the table has so many
NOT-APPLICABLE verdicts:** when the target tile carries a BUILDING (an enemy
turret, a harvester, a barrier), `st[tidx] != 0` and the same function switches
the goal set to *the target's free orthogonal neighbours*
(`sk_common.py:977-985`). A walk at a not-standable target therefore
**terminates BESIDE it by construction** — which is exactly the legal act
stance. `CONVEYOR`/`SPLITTER` are deliberately absent from
`BFS_BLOCKING_TYPES` (`sk_maps.py:2411-2414`), so belt tiles are standable and
belt targets are *in* the class.

### The test applied to every site

* **what is the target?** — and where does it come from;
* **can the path terminate ON it?** — STANDABLE (empty/ore/belt tile) = yes;
  a tile carrying a building = **NOT-STANDABLE**, the BFS lands the body beside
  it;
* **must the body ACT ON that exact tile?** — a *stance* target (a medic seat, a
  lap tile, a hold tile) is walked to in order to STAND there and act on a
  DIFFERENT tile; those are outside the class however standable they are;
* **arrival / step-off handling?** — an explicit adjacent-stance terminal
  ("stand beside the site, never on it" + "already in position → return None"),
  an explicit step-off branch (the belt guard), a per-round staleness re-check,
  a re-plan when `step_to` returns `False`, or a timer that bans the target;
* **verdict** — GUARDED / NOT-APPLICABLE / **EXPOSED**.

### Enumeration bound (stated, not silent)

`walk_sites.py` matches `self.step_to(`, bare `ct.move(`, `self._bfs_direction(`
and `self._nav(` across all five files, skipping comment-only lines, and maps
each hit to its enclosing class/method. Result: **36 sites — 33 in
`sk_roles.py` (32 `step_to` + 1 raw `ct.move`), 3 in `sk_common.py` (the
primitives themselves), 0 in `main.py`, `sk_core.py`, `sk_maps.py`.** All 33
`sk_roles.py` sites are in the table; the 3 primitives are the mechanism, not
call sites, and are described in the section above. **Nothing is omitted.**
(`_v628compose` returns 33 total by the same script — 29 `step_to` + the same
raw move + primitives; the delta is v632's own new code.)

---

## THE AUDIT TABLE

Flag defaults are quoted from `bots/_v632heim/sk_maps.py` as shipped in this
tree; a site whose flag is OFF is still audited, and the flag state is named.

| # | file:line · method | what the target is | terminate ON it? | arrival / step-off handling | verdict |
| --- | --- | --- | --- | --- | --- |
| 1 | `sk_roles.py:321` `_builder` | `commit_tgt` — a frozen copy of last round's `self.tgt` (v604 FIX 2 orbit freeze), denier + V5 branch | inherits its source's class | **fails open**: the branch is `… and self.step_to(...)`, so a `False` short-circuits and the ordinary ladder runs; window bounded at `k + SK_CYCLE_COMMIT_SLACK` (2) | GUARDED |
| 2 | `sk_roles.py:763` `_medic_turn` | `_medic_seat` — a core-ring tile to STAND on; the heal targets an adjacent footprint tile | yes, but a **stance**, not an act-target | explicit `if seat == p: return False` (`:757-762`) | NOT-APPLICABLE |
| 3 | `sk_roles.py:1053` `_counter_march` | the shooter's tile, or `_pluck_seat`'s orthogonal seat of it | shooter = building = **NOT-STANDABLE**; seat = stance | `if adj: return False` above (`:1031`); BFS lands beside the turret | NOT-APPLICABLE |
| 4 | `sk_roles.py:1064` `_counter_march` (soft-bodies variant) | same as #3 | same | same, plus `nav_held` | NOT-APPLICABLE |
| 5 | `sk_roles.py:3912` `_home_keeper_move` | `_medic_seat` | stance | explicit `if seat.x != p.x or seat.y != p.y` (`:3911`) | NOT-APPLICABLE |
| 6a | `sk_roles.py:3916` `_home_keeper_move` | `_escalate_target` **branch 1** — a LIVE visible armed enemy inside d²100 of our core (`:3436-3443`) | **NOT-STANDABLE** (building read live this round) | BFS lands beside it; the keeper chews | NOT-APPLICABLE |
| **6b** | `sk_roles.py:3916` `_home_keeper_move` | `_escalate_target` **branch 2** — `harv_killer[xy]`, an **INFERRED** killer tile from `armed_memo`, not re-verified at this call (`:3448-3455`) | **YES when the remembered turret is already gone** — the tile is then empty | **NONE at this site.** `self.step_to(ct, shooter); return` ignores the verdict. The escalation's own lift (`_harv_blocked` → `_killer_dead`, `:1602-1620`) is never evaluated here: the branch **returns above** the ore loop that calls it (`:4086`), and the only other caller is `_harvester_action`'s own-4-neighbour scan (`:1534`) | ⛔ **EXPOSED** |
| 7 | `sk_roles.py:3927` `_seat_walk` | the orthogonal **stance beside** a delivery seat (`:2299-2318`) | stance | target-adjacent pathing + `d²==1 → None` + `r == p → None` | GUARDED |
| 8 | `sk_roles.py:3936` `_apron_walk` | stance beside a lost apron tile (`:3088-3103`) | stance | same three guards | GUARDED |
| 9 | `sk_roles.py:3945` `_seat_heal_walk` | ONE cardinal step onto a tile from which a seat becomes healable (`:2860-2890`) | stance | `d²==1 → None`; the walk is one step by construction | GUARDED |
| 10 | `sk_roles.py:3954` `_seat_claim_walk` | stance beside a claim seat (`:2532-2551`) | stance | same three guards | GUARDED |
| 11 | `sk_roles.py:3962` `_home_gun_walk` | stance beside the gun site — *"Stand orthogonally beside the site, not on it"* (`:2711-2727`) | stance | same three guards | GUARDED |
| 12 | `sk_roles.py:3972` `_hl_walk_target` | stance beside the launcher site (`:3396-3416`) | stance | `d²==1 → None` + `r == p → None` | GUARDED |
| 13 | `sk_roles.py:3992` `_home_keeper_move` | nearest `_route_gaps` tile — an UNBUILT belt-plan tile (act-on) | **STANDABLE** | own tile excluded in the loop (`:3989`); `_route_gaps ⊆ belt_plan` (`:2097`), so a gap tile underfoot falls through to the belt step-off at #14 | GUARDED |
| **14** | `sk_roles.py:4017` `_home_keeper_move` | ✅ **THE BELT STEP-OFF GUARD** (positive control) — walks to a free cardinal neighbour when standing on an unbuilt belt-plan tile (`:4009-4018`) | n/a — this IS the step-off | explicit step-off branch, carrying its own measured (7,9) incident in the comment | **GUARDED** ✅ |
| **15** | `sk_roles.py:4037` `_home_keeper_move` | ✅ **THE NEW ORE STEP-OFF GUARD** (positive control) — same shape, gated `SK_ORE_STEPOFF and self._on_eligible_ore(...)` (`:4027-4038`) | n/a | explicit step-off; `_on_eligible_ore` (`:6378-6395`) mirrors the ore loop's four filters (`harv_tiles`, `is_home_half`, `belt_plan`, `_harv_blocked`) **verbatim** | **GUARDED when armed** ✅ — **`SK_ORE_STEPOFF = False` at `sk_maps.py:3403`, so it is inert in the shipped configuration** |
| **16** | `sk_roles.py:4100` `_home_keeper_move` | the economy-walk terminal: nearest unbuilt **belt-plan tile**, else nearest eligible **ORE tile** (`:4076-4092`), else `explore_step`, else `self.core` | belt + ore = **STANDABLE act-on**; explore = stance (self-advancing, `:1578-1580`); core = NOT-STANDABLE | belt half guarded at #14; **ore half guarded at #15 ONLY when `SK_ORE_STEPOFF` is True**; the ore loop itself never excludes the body's own tile, and the fall-through rung is `SK_IDLE_ACT_ALL … and self.free_neighbours(ct, p) == 0` (`:4102-4111`) — **the wrong gate for this defect, whose signature is free neighbours** | ⛔ **EXPOSED at shipped flags** (the #130 anchor; GUARDED with `SK_ORE_STEPOFF=True`) |
| 17 | `sk_roles.py:4694` `_cage_walker` | the next free **lap tile** (12-tile ring), with a 1..12 skip-ahead | stance | skip-ahead walks PAST a blocked tile; arrival on a lap tile is the goal | NOT-APPLICABLE |
| 18 | `sk_roles.py:4748` `_cage_walker` | `commit_tgt` | inherited | fails open (`if … : return` on True only) | GUARDED |
| 19 | `sk_roles.py:4762` `_cage_walker` | nearest **EMPTY SEAL tile** — a barrier build site — else `self.enemy` | **STANDABLE act-on** | **re-plan on `step_to` False**: v602 FIX 1's second half (`:4768-4782`) walks to the nearest free lap tile instead; and a seal seat that is a lap tile is taken by #17's branch first | GUARDED |
| 20 | `sk_roles.py:4781` `_cage_walker` | nearest free lap tile | stance | `_lap_free` occupancy test per round | NOT-APPLICABLE |
| 21 | `sk_roles.py:4958` `_cage_cursor_move` | `_cursor_target`: seal seat (act-on), evict target (enemy building), or lap tile | seal = **STANDABLE act-on**; evict = NOT-STANDABLE; lap = stance (own tile excluded, `:4928`) | **timer only**: `_cursor_done` never completes on an occupied-by-self seal tile, but `SK_CURSOR_GIVEUP = 20` bans the tile and re-picks (`:4906-4913`) | GUARDED (timer-bounded ≤20 r) — **and DEAD in this tree: `SK_ONE_CURSOR = False`, `sk_maps.py:297`** |
| 22 | `sk_roles.py:5270` `_attack_enemy_core` | `self.enemy` — the enemy core | **NOT-STANDABLE** (2×2; `_bfs_direction` has an explicit core-ring goal branch, `:978-984`) | lands on the ring | NOT-APPLICABLE |
| 23 | `sk_roles.py:5335` `_ore_denier` | `commit_tgt` | inherited | fails open | GUARDED |
| **24** | `sk_roles.py:5338` `_ore_denier` | `_deny_target` (`:5430-5466`): **(a)** a remembered `enemy_harv` tile, **(b)** a live visible enemy harvester, **(c)** PATROL — the nearest enemy-half **ORE tile** not in `denied_tiles` | **(b) NOT-STANDABLE. (a) and (c) STANDABLE** — (a) the moment the harvester there is gone, (c) always | **NONE.** The act is `_deny_barrier`, which scans `p.add(d)` — an **orthogonal neighbour** (`:5369-5391`) — so the tile underfoot is never a legal barrier site. `enemy_harv` is popped **only on a successful build on that tile** (`:5394`) and `denied_tiles` gains **only** the tile actually built on (`:5395`), so the body's own tile stays the nearest target at d²=0 forever. The fall-through is again `SK_IDLE_ACT … free_neighbours == 0` (`:5344-5352`) | ⛔ **EXPOSED** — `SK_ORE_DENY = True` (`sk_maps.py:44`), live |
| 25 | `sk_roles.py:5597` `_siege_engineer` | `hold` — `nest_site`, else `_nest_slots()[-1][1]`, a LIVE turret's tile | NOT-STANDABLE | *"Hold station beside the newest one"*; BFS lands beside | NOT-APPLICABLE |
| 26 | `sk_roles.py:5731` `_siege_engineer` | `nest_site` — an EMPTY band tile the engineer must build a turret on | **STANDABLE act-on** — and the act is explicitly gated `adj = manhattan == 1` (`:5650`), so standing on it makes prep AND plant illegal | **watchdog only**: `_nest_watch` (`:6288-6350`) re-arms on arrival (d²=0 is a new closest approach) then, with the body motionless, both the `nest_since` and `nest_anchor` clocks expire together after `SK_NEST_STUCK_ROUNDS = 25`; the tile goes into `nest_bad` (permanent) and a fresh site is picked | GUARDED (timer-bounded ≤~25 r per site, then permanently banned) |
| 27 | `sk_roles.py:6027` `_relight_close` | `self.enemy` | NOT-STANDABLE | fenced to fire only OUTSIDE the band | NOT-APPLICABLE — `SK_RELIGHT_CLOSE = False` |
| 28 | `sk_roles.py:6475` `_preprep` (STAGE mode) | `preprep_site` — the next band site, **walked to on purpose to stage on it** | STANDABLE, and standing there is the design intent (no build at all in this mode) | explicit: *"IT RETURNS `step_to`'s VERDICT, so a body already ON the site falls through to v619's hold"* (`:6474-6475`) | GUARDED — `SK_TUBE_FLOOR2_STAGE = True`, live |
| 29 | `sk_roles.py:6493` `_preprep` (build mode) | `preprep_site`, with barriers laid when `manhattan == 1` (`:6479`) | **STANDABLE act-on** | body-level: `step_to` False → `_preprep` returns False → the caller falls through to the v619 hold, so **the body is not frozen**. But `preprep_site` is never cleared on that path, so the sub-plank stalls and the body can alternate hold ↔ site. **NOTE, not a #130 verdict:** that is the #54 limit-cycle class, not the freeze class | GUARDED at body level (**see note**) — `SK_TUBE_FLOOR2_PREPREP = False` |
| **30** | `sk_roles.py:6915` `_home_defence` | `SK_SLOT_THREAT_POS` — the tile where the CORE last saw an enemy body, turret or barrier (`sk_core.py:114-132`) | **YES when the tile has gone empty** — an enemy builder walks away, or its structure is removed; the slot **is never cleared** (`:6825-6826` says so in those words) | **NONE.** The only tile-content tests are the barrier skip and the own-building shot veto, both inside the `manhattan == 1` branch; at manhattan 0 nothing runs and the site ends `self.step_to(ct, threat)` / **`return True`** — the turn is consumed unconditionally, so no lower authority ever gets it | ⛔ **EXPOSED (bounded ≤50 rounds** by the slot-1 latch: `_under_attack` = `beat_fresh(..., 50)`, `:396-397`; the caller only runs while that latch is fresh) |
| **31** | `sk_roles.py:7078` `_citadel_answer` | the same `SK_SLOT_THREAT_POS` tile | an enemy BODY's tile — NOT-STANDABLE while occupied | ✅ **the model answer, and a third positive control**: the tile's occupant is re-read EVERY round (`:7015-7048`) and `citadel_tgt` is cleared on *our own building*, *nothing there any more*, and *our own body walked onto it*; adjacent → HOLD (with a free peck); **and `step_to` False returns False so the role's own ladder runs** | **GUARDED** ✅ |
| 32 | `sk_roles.py:7370` `_demolish_action` | `walk_q` — the position of a live enemy building read from `get_nearby_buildings()` **this round** (`:7247-7288`); act and walk sets are disjoint by construction | **NOT-STANDABLE** | BFS lands beside; next round the target enters the ACT set; `step_to` False → returns False | NOT-APPLICABLE — `SK_DEMOLISH = False` |
| 33 | `sk_roles.py:5963` `_rent_step` (raw `ct.move`) | not a walk target at all: one cardinal step that makes an adjacent DIAGONAL sweep candidate reachable | n/a | budgeted (`SK_RENT_STEP_BUDGET`), pre-floor window only, explicitly *"NEVER A WALK TARGET"* | NOT-APPLICABLE |

**Primitives (not call sites):** `sk_common.py:1116` (`_nav` → `_bfs_direction`),
`sk_common.py:1420` (`step_to` → `_nav`), `sk_common.py:1221` (`_move` → `ct.move`).

### Control check — the method reads the controls correctly

| control | required verdict | this audit reads |
| --- | --- | --- |
| belt step-off guard, `_v632heim:4017` (= `_v628compose:3954-3971`) | GUARDED | **GUARDED** ✅ |
| new ore step-off guard, `_v632heim:4037` (`sk_maps.py:3403`) | GUARDED | **GUARDED when armed; inert at `SK_ORE_STEPOFF=False`** ✅ |
| pre-port ore walk, `_v628compose:3996-4015` | EXPOSED | **EXPOSED** ✅ — `grep -c 'SK_ORE_STEPOFF\|_on_eligible_ore' _v628compose/{sk_roles,sk_maps}.py` = **0, 0**: the guard does not exist in that tree at all, and the ore loop there is byte-for-byte the v632 loop minus the leash lines |
| (bonus, unprompted) `_citadel_answer:7078` | — | **GUARDED**, and it is the only site in the tree that re-checks its target's occupancy every round |

**The method was not tuned to produce those answers**: the discriminator is the
`st[tidx] == 0` branch in `_bfs_direction`, applied identically to all 33 sites,
and it independently classifies 12 sites NOT-APPLICABLE purely because their
target carries a building.

### Where the two trees differ

`sk_core.py` is identical. `_v632heim` adds, relative to `_v628compose`:
the ore step-off guard (#15) and its `_on_eligible_ore` predicate; the
threat-conditional keeper leash inside the same economy walk (#16, two
`_leashed` filters); the `SK_IDLE_ACT_ALL` rung under #16; the citadel dispatch
(#31); and the demolition sweep walk (#32). **Every EXPOSED site below except
#16's guard availability exists identically in `_v628compose`** — #6b, #24 and
#30 are inherited, not new, and #16 is the same walk with a guard the shipped
flag leaves off.

---

## THE FREEZE INVARIANT — method

**The wire signature the row asked for:** a body of ours standing **N
consecutive rounds emitting ZERO actions on its own id** (no `moveBuilderBot`,
no `builderBuild`, no `builderAttack`, no `builderHeal`) **while having ≥1 free
orthogonal neighbour** in every round of the run. Decoded over
`t_p11_f1/` and `t_leash_f1/` — **all 30 cells each, all our builder bots, both
arms** — with `s54_klad_lib.Game` under `e46p1_lib.cells_at`; no second decoder
was written.

Conventions, stated because they move the numbers:

* State at round `r` is evaluated **after** that round's events (the `e46p1_lib`
  convention). A body is alive in `[born, died-1]`, or through `rounds-1` if it
  never appears in `died`.
* The run length counts **zero-action rounds**, so the arrival `MOVE` onto the
  tile is excluded. **This produces a systematic −1 against the ATTRIBUTION
  doc's "longest stationary run" figures**, which count the arrival round.
* A body's `builderBuild` also emits a `placeEntity` for the NEW entity; that is
  keyed to the new id and is never credited to the body.

### ⛔ A SPEC CORRECTION THAT WAS LOAD-BEARING, AND IT SUPPRESSED A POSITIVE CONTROL

The commission defined a free neighbour as one with *"no building occupying
it"*. **That is wrong about this engine, and under it the skald control reads 8
rounds instead of 33.** A builder bot **can stand on a friendly
conveyor/splitter**; harvesters, barriers and turrets block. Established two
ways before the model was changed:

1. **Off the wire, both directions** — across all 60 tapes our bodies occupy a
   live building's tile in **9,282 (body, round) pairs, and 9,282 of 9,282 are a
   CONVEYOR; 0 are of any other kind.** In skald itself: conveyor id 89 is built
   on (9,5) at r57 and our body 3 MOVEs onto (9,5) at r58 while id 89 is alive
   (it dies r153).
2. **In the bot's own source** — `arm_p11/sk_common.py:885-905` records the s54
   engine measurement verbatim (conveyor `is_tile_passable=True/can_move=True`,
   harvester `False/False`), and `BFS_BLOCKING_TYPES`
   (`sk_maps.py:2411`) is exactly `{gunner, sentinel, launcher, harvester,
   barrier}`.

Both models were run everywhere; **the engine model is primary** and is what is
quoted below, with the literal-spec figures kept alongside. ⚠ **We built 0
splitters in these 60 tapes** (586 conveyors, 601 barriers, 128 harvesters, 144
sentinels, 96 gunners), so the splitter half of "passable" rests on the source
note, not on these tapes.

---

## VALIDATION — all four, both directions

### (4) The action detector is not silently empty — **PASS, exactly**

| arm | MOVE | BBUILD | BATK | HEAL |
| --- | ---: | ---: | ---: | ---: |
| P11 | 21,885 | 773 | 1,950 | 433 |
| LEASH | 18,704 | 782 | 1,615 | 539 |

Banked spot-check, `icefloe_seatB` keeper id 4: **P11 101 moves / 42 builder
attacks · LEASH 289 / 46** — the ATTRIBUTION doc §1 figures, digit for digit.

### (1) Positive controls — **PASS, 2 of 2 in scope**

| control | ATTRIBUTION doc | measured (engine model) | verdict |
| --- | --- | --- | --- |
| p11 `icefloe_seatB` body 4 | ~475 r, r164→r638, ORE (16,8), 0 actions | **r165–638, len 474, ORE (16,8)** | **MATCH** (−1 = the arrival MOVE at r164) |
| p11 `skald_seatA` body 3 | 33 r, ORE (8,5) | **r83–114, len 32, ORE (8,5)** | **MATCH** (−1 = arrival MOVE at r82) — **reads 8 under the literal spec model** |
| the belt guard's (7,9) incident | a different, older tape | absent, as expected | out of scope, not chased |

**Independently re-implemented from scratch** by the audit author against
`s54_klad_lib` (a second script, not the detector): `icefloe_seatB` body 4
→ **start 165, len 474, tile (16,8), env 2 (ORE)**; `paths_seatA` body 3 →
**663 @ r325** and **121 @ r25**. Two implementations, same answers.

**The skald control is why the occupancy model had to be corrected.** From r82
the body sits on ore (8,5) with all four cardinals carrying **its own**
buildings — harvester (8,6) r56, conveyor (9,5) r57, conveyor (8,4) r64,
harvester (7,5) r76. Two are conveyors, which the engine lets it walk on, so it
has 2 free neighbours and the run is a genuine freeze; the literal model called
it boxed-in and split the run at r76. That is the `free_neighbours` self-trap
docstring's own scenario, read off the wire.

### (2) Negative control — **PASS on 3 of 5 leash keepers at N≥50; the 2 hits are explained, not waved away**

| cell | LEASH keeper: N≥20 / N≥50 / longest | P11 keeper: N≥20 / N≥50 / longest |
| --- | --- | --- |
| icefloe_seatB (id 4) | 6 / **2** / 60 @r304 (16,3) | 3 / 1 / **474 @r165 ORE (16,8)** |
| holmgang_seatA (id 3) | 0 / 0 / 17 | 0 / 0 / 6 |
| glacierkeep_seatB (id 4) | 1 / 0 / 30 | 1 / 0 / 24 |
| skald_seatA (id 3) | 0 / 0 / 1 | 2 / 0 / **32 @r83 ORE (8,5)** |
| stavkirke_seatA (id 3) | 2 / **1** / 127 @r158 (8,2) | 1 / 1 / 56 @r75 (8,2) |

(Under the literal-spec model only stavkirke hits at N≥50 — 4 of 5 clean.)

**All three hits are the same benign shape — a keeper sitting ON its medic seat
with nothing to heal:**

* **LEASH `stavkirke_seatA` id 3, r158–284 at (8,2).** (8,2) *is* a medic seat
  (core anchor (9,2)). The body heals on **r152–157**, the six rounds
  immediately before, and our core then takes **zero damage for the rest of the
  game** (11 damage rounds all game, **none in r158–284**). The tape ends r284
  with our win by core takedown.
* **LEASH `icefloe_seatB` id 4, r304–363 at (16,3)** — also a medic seat (core
  (17,2)). Heals **r298–303** immediately before and **r364** immediately after;
  **zero core damage inside the window**.
* **LEASH `icefloe_seatB` id 4, r607–666 at (15,3)** — one tile outside the ring
  (cheb 2). Zero core damage r607–664; the first tick lands **r665** and the
  freeze breaks the next round.
* (Same shape in P11 `stavkirke_seatA` id 3, r75–130 at (8,2): heals resume
  r131–138, the round after the r130 tick.)

⇒ **The invariant as specified does not by itself separate a deadlock from an
idle sentry on station.** The discriminator that does is on the wire: a deadlock
keeps standing *through* core-damage rounds; an idle sentry breaks within a
round or two of the first tick. The p11 icefloe keeper stands through **all** of
them; the leash ones do not. **This is a stated defect of the instrument, not a
result.**

### (3) Mutation control — **PASS; the free-neighbour condition binds**

Dropping the free-neighbour condition changes the counts under **both** models:

| model | arm | (body, round) pairs with ZERO free neighbours | N≥20 | N≥50 | N≥100 |
| --- | --- | ---: | ---: | ---: | ---: |
| engine | P11 | **380** | 146 → **150** | 16 → **18** | 7 → **8** |
| engine | LEASH | **510** | 138 → **140** | 19 → **21** | 8 → **9** |
| spec | P11 | 1,688 | 139 → 150 | 12 → 18 | 5 → 8 |
| spec | LEASH | 1,602 | 132 → 140 | 15 → 21 | 6 → 9 |

Legitimately boxed-in bodies **do exist** here, so the condition is not inert —
and the case it binds on is exactly the one the brief named: a body ringed by
its own harvesters/conveyors (skald p11 body 3 at (8,5) reads genuinely 0-free
at r76 under **both** models, four cardinals = harvester / conveyor / conveyor /
harvester).

---

## THE FREEZE READOUT

**Per-arm totals (engine model primary; spec model in parentheses):**

| arm | N≥20 | N≥50 | N≥100 | alive body-rounds inside a ≥20 r freeze |
| --- | ---: | ---: | ---: | --- |
| **P11** | **146** (139) | **16** (12) | **7** (5) | 6,050 / 31,932 = **18.9 %** |
| **LEASH** | **138** (132) | **19** (15) | **8** (6) | 6,085 / 28,656 = **21.2 %** |

**N≥50, sorted by length** (35 rows; the full 284-row N≥20 table is in the
scratchpad `out.txt`):

| len | arm | cell | body | start | tile kind | (x,y) | note |
| ---: | --- | --- | ---: | ---: | --- | --- | --- |
| **663** | LEASH | paths_seatA | 3 | 325 | EMPTY | (2,13) | longest in the fixture |
| **474** | **P11** | **icefloe_seatB** | **4** | **165** | **ORE** | **(16,8)** | **KEEPER — #130's anchor** |
| 418 | P11 | yggdrasil_seatB | 4 | 35 | EMPTY | (26,24) | |
| 383 | P11 | yggdrasil_seatB | 12 | 70 | EMPTY | (0,7) | |
| 380 | LEASH | yggdrasil_seatB | 4 | 17 | EMPTY | (26,24) | twin of row 3 |
| 327 | LEASH | yggdrasil_seatB | 12 | 70 | EMPTY | (0,7) | twin of row 4 |
| **291** | LEASH | helheim_seatA | 3 | 74 | **ORE** | (1,16) | ore freeze in the CONTROL arm |
| 287 | P11 | helheim_seatB | 131 | 86 | EMPTY | (17,2) | |
| **157** | P11 | valkyrie_seatA | 3 | 93 | **ORE** | (2,22) | |
| 152 | LEASH | holmgang_seatB | 92 | 111 | EMPTY | (11,3) | |
| 127 | LEASH | stavkirke_seatA | 3 | 158 | EMPTY | (8,2) | KEEPER, idle-on-seat (see V2) |
| 126 | LEASH | auroraveil_seatB | 4 | 92 | EMPTY | (14,12) | |
| 126 | P11 | auroraveil_seatB | 4 | 92 | EMPTY | (14,12) | byte-twin of the row above |
| 121 | LEASH | paths_seatA | 3 | 25 | EMPTY | (1,10) | |
| 101 | P11 | paths_seatA | 3 | 230 | EMPTY | (1,10) | |
| 95 | LEASH | skald_seatB | 4 | 24 | EMPTY | (9,9) | |
| 95 | P11 | skald_seatB | 4 | 24 | EMPTY | (9,9) | twin |
| 80 | LEASH | paths_seatB | 12 | 54 | EMPTY | (2,7) | |
| 80 | P11 | helheim_seatB | 258 | 293 | EMPTY | (16,2) | |
| 76 | P11 | paths_seatB | 12 | 54 | EMPTY | (2,7) | |
| **74** | LEASH | icefloe_seatA | 3 | 47 | **ORE** | (1,9) | ore freeze in the CONTROL arm |
| **69** | P11 | helheim_seatB | 4 | 137 | **ORE** | (10,11) | |
| 68 | LEASH | fimbulwinter_seatA | 3 | 30 | EMPTY | (2,3) | |
| 68 | LEASH | glacierkeep_seatA | 5 | 189 | EMPTY | (13,26) | |
| 67 | LEASH | glacierkeep_seatA | 3 | 190 | EMPTY | (15,0) | |
| 64 | P11 | glacierkeep_seatA | 5 | 189 | EMPTY | (13,26) | |
| 63 | P11 | glacierkeep_seatA | 3 | 190 | EMPTY | (17,0) | |
| 61 | LEASH | longhouse_seatA | 5 | 237 | EMPTY | (24,10) | |
| 60 | LEASH | icefloe_seatB | 4 | 304 | EMPTY | (16,3) | KEEPER, idle-on-seat |
| 60 | LEASH | icefloe_seatB | 4 | 607 | EMPTY | (15,3) | KEEPER, idle at cheb 2 |
| 56 | P11 | stavkirke_seatA | 3 | 75 | EMPTY | (8,2) | KEEPER, idle-on-seat |
| 54 | P11 | paths_seatA | 3 | 20 | EMPTY | (1,10) | |
| 53 | LEASH | jotunheim_seatA | 58 | 424 | EMPTY | (17,19) | |
| 53 | P11 | fimbulwinter_seatA | 11 | 138 | EMPTY | (13,14) | |
| 50 | LEASH | paths_seatB | 4 | 12 | EMPTY | (22,10) | |

**30–49 band, 21 rows:** 48 LEASH holmgang_seatB/4/r29 · 47 P11
valkyrie_seatA/11/r126 · 47 LEASH jotunheim_seatA/8/r430 · 44 P11
bifrost_seatB/4/r244 · 44 P11 holmgang_seatB/9/r76 · 43 LEASH paths_seatB/9/r91
· 41 P11 paths_seatB/9/r81 · 40 P11 jotunheim_seatA/3/r384 · 40 P11
jotunheim_seatA/8/r384 · 40 LEASH jotunheim_seatA/3/r437 · 39 P11
paths_seatB/4/r28 · 38 P11 jotunheim_seatB/4/r142 · 38 P11 jotunheim_seatB/6/r142
· 37 P11 icefloe_seatA/8/r80 · 34 LEASH longhouse_seatA/10/r160 · 34 LEASH
valkyrie_seatA/3/r74 · 33 P11 longhouse_seatB/4/r135 · **32 P11 skald_seatA/3/r83
ORE (8,5) — KEEPER, #130's second anchor** · 32 P11 valkyrie_seatB/4/r87 · 32
LEASH valkyrie_seatB/4/r87 · 30 LEASH glacierkeep_seatB/4/r38 (keeper).

**20–29 band: 228 rows, and it is one repeating artefact, not 228 findings.**
169 of the 228 are **exactly 26 rounds long** and 182 of 228 belong to bodies
**11 and 12**, recurring on a ~27-round cycle (e.g. P11 jotunheim_seatA body 11
at r74, 101, 129, 161, 188, 234, 261, 291, 319, 356, 384). That is a body taking
**one step per ~27 rounds** — see surprise 3.

### SURPRISES

1. **The freeze rate is an arm-level constant, not a p11 defect.** 18.9 % (P11)
   vs **21.2 % (LEASH/control)** of alive body-rounds — the control arm freezes
   *marginally more by volume*, and 6 of the 15 N≥100 runs are twins across the
   two arms (auroraveil_seatB body 4 r92+126 identical; skald_seatB body 4
   r24+95 identical; yggdrasil_seatB and paths_seatA/B near-identical). **The
   keeper deadlock #129 attributed to the dispatch is a specific, correctly
   attributed case inside a much larger pre-existing population of frozen bodies
   that BOTH arms share.** The p11 icefloe keeper is the *second* longest run in
   the fixture; the longest, 663 rounds, is in the control arm. This is
   consistent with the code half, where #6b, #24 and #30 are all inherited from
   `_v628compose`.
2. **The longest freeze in the fixture is in a game we WIN.** LEASH
   `paths_seatA` body 3 freezes r325–987 (663 r) at (2,13) and the tape ends
   r988 `core_destroyed` in our favour; same for yggdrasil_seatB (two bodies,
   418 + 383 r) and valkyrie_seatA (157 r). **13 of the 15 N≥100 runs terminate
   at the last round of the tape** — those bodies never unfreeze, the game just
   ends. A long freeze is not by itself predictive of the result, and this row
   is an idle-asset argument, not a win-rate one.
3. **A second, distinct pathology the invariant does NOT catch: the ~27-round
   crawl.** Bodies 11 and 12, present in nearly every cell in both arms, move
   once and then emit nothing for exactly 26 rounds, repeatedly. Each stretch is
   short, so no N≥50 row names it, yet a body making one cardinal step every 27
   rounds is functionally as inert as a frozen one — and it accounts for 182 of
   the 284 N≥20 instances. It wants its own detector; it is not #130's class.
4. **ORE tiles are over-represented at the long end, and two of the ore freezes
   are in the CONTROL arm.** Only 10 of 284 N≥20 runs sit on ore, but **5 of the
   35 N≥50** do. Beyond the two cells #129 named: `LEASH helheim_seatA` body 3
   **291 r on ORE (1,16)**, `LEASH icefloe_seatA` body 3 **74 r on ORE (1,9)**,
   `P11 valkyrie_seatA` body 3 **157 r on ORE (2,22)**, `P11 helheim_seatB` body
   4 **69 r on ORE (10,11)**. **The stand-on-an-ore-target shape occurs without
   the dispatch arm.** ⚠ No role is attributed to those bodies here — the
   keeper-identifier model was validated only for the five cells of the
   ATTRIBUTION doc — so whether they are keepers (site #16) or ore deniers
   (site #24) is **open and not claimed**.

---

## LIMITS

* **Static reachability, not execution.** The audit reasons about the terminal
  state each call site can reach; it does not prove any particular site is
  reached in any particular game. The tape half supplies the live evidence for
  the class, not per-site attribution — **no freeze instance below is attributed
  to a named call site**, and doing so would need an instrumented local run this
  commission did not perform.
* **Flag state is as shipped in this tree at the recorded md5.** Six of the
  audited sites sit under flags that are OFF; a flag flip changes their verdict
  (and #16's verdict flips to GUARDED the moment `SK_ORE_STEPOFF` is armed).
* **The tree is being edited live.** Line numbers are valid against the recorded
  md5 only.
* **Timer-bounded is not guarded in the same sense as step-off.** #21, #26 and
  #30 all terminate — after 20, ~25 and ≤50 rounds respectively. They are
  ranked GUARDED/EXPOSED on whether anything re-plans *at all*, and the bound is
  quoted so the builder can price them; a 25-round stall repeated per site is
  not the same object as a 475-round freeze.
* **#6b's precondition chain is long and is stated in full so it can be
  falsified**: `SK_HARV_ESCALATE` on (default True) ∧ an escalated harvester
  tile with an inferred killer ∧ that killer's structure no longer on its tile
  ∧ no live armed enemy visible within d²100 of our core ∧ the keeper not
  standing beside the escalated ore tile with harvester funds. It is a narrower
  road than #24 and #16.
* **The freeze invariant is a WIRE signature, not a code fact.** It cannot
  distinguish a stand-on-target deadlock from any other zero-action stand with
  free neighbours — a deliberate medic-seat hold with nothing to heal
  (`_medic_seat` returns `p`, bounded by `SK_COREFIRE_TTL`) has the same
  signature at short lengths. That is why the readout is reported at N≥20 and
  the discussion leans on the long tail.

---

## THE EXPOSED LIST

Four sites, in the order the audit found them. **Design and porting are the
builder's; this list is the finding, not a plan.**

1. ⛔ **`sk_roles.py:4100` · `_home_keeper_move`, the ore half of the economy
   walk** — #130's own anchor. GUARDED the moment `SK_ORE_STEPOFF`
   (`sk_maps.py:3403`) is armed; **EXPOSED at the shipped default `False`.**
   Live evidence: icefloe_seatB 474 r, skald_seatA 32 r.
2. ⛔ **`sk_roles.py:5338` · `_ore_denier` → `_deny_target`** — the patrol branch
   walks at an enemy-half **ORE tile** and the remembered-harvester branch walks
   at a tile that becomes empty the moment that harvester is gone; the act
   (`_deny_barrier`) is orthogonal-neighbour-only, and neither `enemy_harv` nor
   `denied_tiles` ever records the tile the body is standing on. **No bound.**
   Flag live (`SK_ORE_DENY = True`).
3. ⛔ **`sk_roles.py:3916` · `_home_keeper_move` → `_escalate_target`,
   inferred-killer branch** — walks at a remembered turret tile that is not
   re-verified at this call site; when that structure is gone the tile is
   standable, and the escalation's own lift (`_killer_dead`) sits on a code path
   this branch returns above. **No bound**, but a long precondition chain (see
   LIMITS). Flag live (`SK_HARV_ESCALATE = True`).
4. ⛔ **`sk_roles.py:6915` · `_home_defence`** — walks at
   `SK_SLOT_THREAT_POS` with no staleness test on the tile's contents, and
   `return True` consumes the turn unconditionally. **Bounded ≤50 rounds** by
   the slot-1 latch TTL (`beat_fresh(..., 50)`).

**All four exist in `_v628compose` as well** — #1 is the same walk without the
new guard, and #2–#4 are unchanged code. **Nothing in the citadel dispatch
introduced this class; the dispatch changed which bodies reach the terminals.**
