# DESIGN BRIEF — v629 "the home answer" (banked verbatim)

**PROVENANCE: builder-commissioned fresh opus design agent, s56 2026-08-22
(announced on the tail ~14:5xZ with the FOCUS directive; report returned
~15:1xZ, banked verbatim below by the builder from the agent transcript).
Named inputs: the COPY 6 / T19 spec (playbook + study), bots/_v628compose,
DECODE-firstcontact §3.1, QUEUE #121/#123, the r300 guard's operational form.
Read-only agent; its §0 head-configuration finding was independently verified
and FIXED by the builder before this banking (tail note ~15:0xZ).**

---

All three research agents are in. Here is the design brief.

---

# v629 DEFENCE BRIEF — the home answer

**GAME CONTEXT (stated per standing directive):** everything below is in-game design work for the Florent Code League — a sandboxed bot-vs-bot programming competition on a simulated grid under organiser-approved rules. "attack", "fire", "clear", "kill", "threat" are the engine's documented API verbs and entity states acting between competing game bots inside the simulator. Nothing here concerns real systems.

**Line head read:** `bots/_v628compose` (sk_roles.py md5 `9db5b17e…`, sk_maps.py md5 `3153f256b…`). Read-only; no files edited.

---

## ⛔⛔ 0. STOP — THE COMMITTED LINE HEAD IS NOT THE ADOPTED CONFIGURATION

Before any v629 branches from it. The adoption record (`docs/coordination.md:73079`, 14:18:59Z) states the adopted config verbatim: **`SK_NEST_CLEAR+OWN ON · SK_TUBE_LATENCY_SOLO+STAGE ON · PB_LIFE OFF`**. The committed tree reads:

| flag | adopted (`scratchpad/s56_cmp/arm_c_full/sk_maps.py`) | **committed `bots/_v628compose/sk_maps.py`** |
|---|---|---|
| `SK_NEST_CLEAR` :2466 | True | True ✓ |
| `SK_NEST_PB_LIFE` :2480 | **False** | **True** ⛔ |
| `SK_TUBE_LATENCY_SOLO` :3148 | **True** | **False** ⛔ |
| `SK_TUBE_FLOOR2_STAGE` :3165 | **True** | **False** ⛔ |

Three of four flags differ. `diff -r bots/_v626nestclear bots/_v628compose` returns only the *addition* of the (False) `SK_TUBE_LATENCY_SOLO` line and its two `or` call sites — i.e. **the committed head is behaviourally `_v626nestclear`, and it additionally carries PB_LIFE, which the adoption explicitly excluded** ("The v626 B-off ship condition is MOOT by construction (PB_LIFE OFF in the adopted config)"). The `arm_c_full` arm that measured +6.33pp was built by `scratchpad/s56_cmp_mkarm.py`, which rewrites flags into a *copy*; the rewrite was never folded back. HANDOVER.md:24 describes the adopted config while citing the committed tree's md5 — the prose and the hash disagree with each other.

**Consequence:** a v629 branched from `bots/_v628compose` inherits neither adopted mechanism, and every ablation identity would be measured against a base that is not the head. Fold `scratchpad/s56_cmp/arm_c_full/sk_maps.py`'s four flag values in first, re-assert the identity, and re-hash. This is a builder decision — I am read-only and have changed nothing.

---

## 1. WHAT WE DO TODAY WHEN AN ENEMY TURRET IS PLANTED IN OUR HALF

### 1.1 The complete chain, by function name

Four bodies exist (`SK_N_ROLES = 4`, sk_maps:2399). Only **two** of them can answer, and they answer different objects through different sensors.

**SENSOR (the CORE, `sk_core.py`)**
- `_threat_scan` :82 — one pass over the core's r²=36 vision. Publishes `SK_SLOT_THREAT_POS` (slot 2) = the **nearest** enemy BUILDER_BOT **or** turret **or** BARRIER within `SK_HOME_RING_DSQ*3 = 39` of the footprint (:114-117, :129-132), and beats the under-attack latch (slot 1). Store writes are buffered → **+1 round**. Returns `(home_guns, home_sents)` into `_drip` :266.
- `_corefire_report` :139 → `_corefire_shooter` :183 — publishes `SK_SLOT_COREFIRE` (slot 15): shooter tile + `CF_SENT_BIT` + `CF_RAY_BIT` + quantised core HP. Ranks ray-confirmed sentinel > ray-confirmed gunner > any sentinel whose *reach* covers a footprint tile. **Latched** (a turret is immovable), cleared only when the remembered tile is re-seen empty (:245-259).

**ANSWER PATH 1 — the HOME KEEPER (role 0), `_home_keeper` sk_roles:1252**
Action block, in order (:1281-1361): `_counter_sent_action` → `_core_medic` → `_door_action` → `_peck_priority` → `_seat_heal_action` → `_heal_action` → `_seat_clear` → `_apron_action` → `_home_launcher_action` → belt/harvester → `_seat_claim_action` → `_home_gun_action` → `_belt_action` → `_cover_gun_action`. Movement: `_home_keeper_move` :3855.

`_door_action` :3417 — COPY 6, the door verb. Its gating, in the order the code applies it:
1. **Threat source = `self.vis_enemy` only** (:3425) — the *keeper's own* r²=20 vision. `TURRET_TYPES` only (:3430, deliberate: the first cut bought six gunners), `dsq_core ≤ 39` (:3432), `gave_up` skipped (:3434), nearest-to-core wins (:3436).
2. **(a) melee** :3442 — fires only if *already orthogonally adjacent*, ≥2 Ti, `hp_trend_ok`. **There is no march.**
3. **(b) counter-turret** :3451 `door_guns >= SK_DOOR_GUN_CAP(2)` → refuse. :3457 `SK_S2_DEFER_GUNS and _s2_pending` — **inert**, because `SK_S2_PRIORITY = False` (sk_maps:805). :3460 funding gate `resources < gunner_cost + 40` → refuse.
4. `_pick_gun_site` :3491 with `require_cover=True`, then a second call with `require_cover=False` (:3477 — "the requirement orders, it does not veto"). Site domain is **`for d in CARDINALS: q = p.add(d)`** (:3537) — orthogonally adjacent to the **keeper** — plus `q.distance_squared(tpos) <= 13` (:3541), `not _on_enemy_axis(q)` (:3543, COPY 2), `free_neighbours(exclude=q) >= 2` (:3558, the self-trap guard), `path_arbiter_ok` (:3480). Facing is *chosen* over all 8 directions, scored `(kill, hits, cov, -dist)`.
5. `self.door_guns += 1` :3488.

`_cover_gun_action` :3704 — the second buyer from the *same* `SK_DOOR_GUN_CAP` (:3724, stated at :3717). Fires when the belt is being eaten (`hurt`, :3741-3756) and `belt gap > 0`.

**ANSWER PATH 2 — the ORE DENIER (role 2), `_role_turn` sk_roles:303-317**
- `_denier_home_answer` :1085 (above ledger V5, :292-305) → `_counter_target` :614 → `_counter_march` :908. Gates: `SK_COREFIRE` on (sk_maps:986), `corefire_fresh` (TTL 24, sk_maps:998), `SK_COUNTER_HP_MAX = 450` (sk_maps:1173 — the core must have lost ≥10% before a builder-turn is sold; dose measured as a plateau), `SK_COUNTER_YIELD_HOME = False`. Target = slot-15 shooter, else `_core_ray_shooter` :569 off this body's own `armed_memo`, fenced `SK_COUNTER_PECK_DSQ = 100`. The march **pecks at 2 Ti / 2 damage**.
- Ledger V5 `_home_defence` :6707 — reads slot 2, melees or `step_to`, refuses BARRIER targets (`SK_HOMEDEF_SKIP_BARRIER`, :6729). Its own docstring (:930-936) says slot 2 "is essentially never the sentinel five tiles out that the anatomy says kills us 19 times in 19."

**ANSWER PATH 3 — the turrets themselves, `_turret` :6875**
- **Ammo guard first** (:6906): `global_ammo < price → return`. A dry gunner does not even re-aim.
- Targets are drawn from `get_attackable_tiles()` — **the current facing ray only**. `_target_pri` :4301 ranks CORE 6 > MARKED 5 > TURRET 4 > HARVESTER 3 > BODY 2 > OTHER 1 > BARRIER 0 (never fired at). `_marked_positions` :4268 **already includes the slot-15 corefire shooter** (:4295-4297) and slot 2 and the inferred belt killer — so an enemy turret shooting our core is already ranked *second only to their core*.
- `_rotate_toward` :7161 is called **only** when `target is None` (:6998) or `hp_trend_ok` fails (:7002).

### 1.2 The five latency sources, named

| # | mechanism | anchor |
|---|---|---|
| L1 | **`_door_action` is keeper-vision-bound (r²=20) and never reads slot 2 or slot 15.** The two published sensors that name the core-killer have no consumer on the *purchase* path. | sk_roles:3425 vs sk_core:132, :181 |
| L2 | **No march.** Half (a) requires prior orthogonal adjacency; half (b) requires a site orthogonally adjacent to the keeper *and* within d²≤13 of the threat — a conjunction satisfiable only if the keeper is already ~d²14 from the enemy turret. | :3442, :3537, :3541 |
| L3 | **The keeper's only march-at-a-shooter is posthumous.** `_escalate_target` :3374 returns `None` unless `belt_escalated or harv_escalated` is non-empty (:3389) — i.e. ≥2 harvester deaths (`SK_HARV_REBUILD_ESCALATE=2`) or 3 conveyor deaths on one tile first. | :3389, sk_maps:2521 |
| L4 | **A gunner with any valid ray target never re-aims**, even at a MARKED core-killer inside its own r²=13 on another bearing. | :6994-7004 |
| L5 | **`armed_memo` has no expiry for turrets.** `_danger_tiles` (sk_common:535-580) rebuilds only on *news* (`_armed_rev`), so a demolished turret's ray is a permanent navigation detour; `_on_armed_axis` :1112 vetoes counter-turret sites off dead sentinels forever; `_core_ray_shooter` :569 can name a corpse (`SK_COUNTER_LIVE_TGT = False`). Only launchers are swept (`_live_launchers` :801, `SK_PLUCK_MEMO_TTL = 60`). | QUEUE #121's GREP, `QUEUE.md:727` |

### 1.3 ⛔ SETTLED LEGS IN THIS AREA — do not re-propose

Every one is `False` in-tree with a measurement attached. **Note the pattern: every plank that adds a home turret purchase failed the r300 bar, and every plank that removes or delays one also failed.**

| flag | line | verdict |
|---|---|---|
| `SK_HOME_GUNNER` | sk_maps:1828 | **This is exactly candidate (b), the T19 "one home gun, always" form.** Built, measured, shipped off, *inverts its own advertisement*: enemy builder deaths 63→88, income 483→550 Ti — and **by-r300 12→5, median kill 201→315**. |
| `SK_SEAT_GUNS` | :1429 | Guns shoot seat-blocking barriers. kills 14→12, by-r300 11→9, **ammo-armed share 8.81%→4.41%** — "the ammo they burn halves the armed share, which is the drip's second sentinel, which is the kill." |
| `SK_GUN_ROUTEBLOCK` | :1881 | Shots into core 1,452→**924**, into barriers 0→1,353. kills 14→7. |
| `SK_SEAT_CLEAR` | :1350 | Mechanism confirmed, outcome inverted. |
| `SK_SEAT_CLAIM` / `SK_SEAT_HEAL` | :1761 / :1924 | v618 planks 1/4: by-r300 12→8 / measured zero. |
| `SK_COUNTER_SENT` | :1255 | **Exact null — and the flag names the cause as the GATE, not the verb**: needs `SK_COUNTER_RNDS = 20` rounds of unbroken alarm; *"the shipped streak median is 11."* See §3.3. |
| `SK_COUNTER_LIVE_TGT` | :1206 | Dead-shooter-tile invalidation, **measured worse alone** (loss moves r129→r152). |
| `SK_HOME_LAUNCHER` | :1556 | v615/v616 arm; 0 launchers built in 65/65 live games. |
| `SK_NEST_POINT_BLANK` | :2491 | v1 ban, unchanged. |
| — | v606 / v607 | Cutting `SK_DOOR_GUN_CAP` 2→1: by-r300 **10→6**. Deferring the purchase: **10→8**. ⇒ the two door gunners are load-bearing. |

---

## 2. WHAT BC'S HOME ANSWER ACTUALLY DOES

**SUBJECT for §2 unless stated:** Bean counters **v47**, n = 1,235 archived games (1,115 unrated / 120 ladder), 24 opponents, 2026-08-16T19:30Z–2026-08-21T04:21Z, mirror control = the opponents in the *same* games. `docs/research/REPLAY-STUDY-beancounters-v47v68-2026-08-21.md` (STUDY) and its v47 part (P47).

### 2.1 Turret fire, not builder melee — but the decomposition matters

| verb, per game | BC v47 | opponents, same games | anchor |
|---|---|---|---|
| builder attacks on enemy **turrets** | **5.4** | **5.7** | STUDY:376 |
| turret shots | **75.2** (gunner 38.5 + sentinel 36.7) | — | STUDY:539-540 |
| gunner `rotate()` | 2.0 (v47) → **8.1 (v68)** | 3.8 / — | STUDY:538 |

⚠ Two corrections to the commissioning numbers, both from the primary:
- **"builders attack turrets only 5.4/game" is not a BC differentiator** — the mirror column is 5.7. It is a fact about the *field*, not about BC.
- **"75 shots/game" is a reconstructed sum never printed as such**, and 92.6% of BC's *sentinel* fire lands on the enemy **core** (PB:679). Only a minority of the 75 can be the home sweep; no document separates them. Do not carry "they fire 75/game at home threats."
- **"69% of gunners home-side" does not reconcile inside its own document**: STUDY:440 says 69%, STUDY:344 gives 28.7% built in the enemy's half ⇒ **71.3% home-side, n = 4,002 gunner builds**. Use the figure with the denominator. v68 **inverts it: 77.9% forward ⇒ 22.1% home-side** (STUDY:542).

### 2.2 The answer's composition (P47:1026-1034, n = 1,235 games)

| | BC | field |
|---|---|---|
| forward turrets planted against them | 6,162 | 3,881 |
| **ever shot at** | **3,811 = 61.9%** | 42.2% |
| mean rounds plant → first shot | **12.6** | 15.8 |
| answered by a counter-turret **orthogonally adjacent** within 3 rounds | **344** | 291 |
| — mean lag | **1.18 rounds** | **0.96** (the field is *faster*) |
| — and the answered turret dies within 15 rounds | **300/344 = 87.2%** | 70.4% |

⇒ **The counter-plant is rare: 344 / 6,162 = 5.6% of plants, 0.28 per game.** The dominant answer is fire from turrets already standing. **BC's edge in the counter-plant is not speed — it is the 87.2% vs 70.4% conversion.**

**Under-specified, and the docs say so:**
- **Type:** never measured at population scale. Both watched instances are **GUNNERS** (P47:527-537 G-C r5; PB:783 G-E r23). n = 2.
- **Facing:** both watched cases face directly at the target. No population rule.
- **Adjacency:** orthogonal, explicitly (P47:1032).
- **Travelling or already there:** P47:542-547 refuses to decide — *"no replay can show the branch."*

### 2.3 Siting, and the rotation verb

Median distance (⚠ the study's column is **d, not d²**): BC v47 gunners sit **d ≈ 5.0 (d²≈25) from their own core**, inside their own belt/harvester cloud (conveyor median 5.8, harvester 7.1) — STUDY:336-346, n = 4,002 gunner builds.

Rotation is **target-exhaustion, not threat-tracking** (P68:201-228, **919 BC rotations over 112 v68 games**, mirror control 206): 97% had already fired from that tile; **64% of last targets died within 3 rounds** of the rotate; **91% fire again within 3 rounds** (field 68%); median rounds since last shot before rotating = 1, **p90 6** (field p90 31). ⛔ No document splits rotations home vs forward.

### 2.4 What it costs them, and what it would cost us

| line | BC v47/game | our budget |
|---|---|---|
| `convert_ammo` | **530 Ti in 56.2 calls** (v68: 650) | **130 / 173 / 162 Ti** (MIRROR / PIVOT / KLADDE medians) |
| all shot cost (derived) | ≈521 Ti — **within 2% of converts; the drip funds shots and nothing else** | — |
| builder melee on turrets | 5.4 × 2 = 10.8 Ti | — |
| counter-plants | 0.28 × 20-30 Ti ≈ **6-8 Ti** | — |
| rotations | 20 Ti (v47) → **81 Ti (v68)** | our rotate is 10 Ti, cap `SK_HOME_GUN_ROT_CAP = 6` (currently gate-dead, §3.1) |
| turrets built | gunner 3.24, sentinel 2.41, **launcher 0.00 in 1,385 games** | our home turrets **1.30 / 1.70 / 1.64 per game** |
| end-of-game bank | 186 Ti (v47) / 137 (v68) — never a war chest | — |

⭐ **The volume deficit nobody has stated:** we hold **1.3–1.7 home turrets against 3.5–4.6 enemy turrets planted in our half — ~2.7×.** *(Subject: v180, 65 unrated games, three pinned opponents, 2026-08-22 08:24–09:01Z, derived from `scratchpad/s54_fc_games.json`.)* BC's plants against us sit at **median d² = 5 from our core, 60 of 86 inside a defending gunner's r²=13, first plant median r63.**

---

## 3. THE EDIT SPEC FOR v629

### 3.0 The two facts that decide the shape

**FACT 1 — the answer fails by REACH, not by speed, and this is measured in the cell where we are fastest.** PIVOT: *"We answered Pivot's killer in 20 of 20 games at median latency 5 rounds — and killed it in 5 of 20 … because a 40-HP sentinel outside our gunners' r²=13 takes more than our answer delivers"* (DECODE:495-497). KLADDE: in **three quarters of losses we could not have covered the killer's tile under any facing** (DECODE:309-311). The killer is a **sentinel in 63/63** losses, at median d² **18 / 25 / 13** from our core.

**FACT 2 — we are at the ammunition ceiling, and it sits below one core.** Converted Ti × ~1.8 is the hard upper bound on turret damage:

| cell | Ti converted (median) | damage ceiling | damage actually put into their core (median) | **saturation** |
|---|---|---|---|---|
| MIRROR (BC v68, 20 g) | 130 | 234 | 227 | **97%** |
| PIVOT (v249, 20 g) | 173 | 311 | 243 | 78% |
| KLADDE (v173, 25 g) | 162 | 292 | 198 | 68% |
| local FIXTURE A / B (15 g each) | **504 / 536** | 907 / 965 | — | — |

⇒ **In the binding cell every Ti spent on defence is subtracted 1:1 from the 227 damage we deliver.** 24 Ti of counter-gunner ammo = 43 damage = **19% of everything we land on their core**. This, not the turret count, is why four consecutive purchase-adding home planks failed the r300 bar.

**⇒ Only verbs that add ZERO turret purchases and ZERO marginal ammo can pass the directive's second clause.**

---

### 3.1 ⭐ RECOMMENDED — PLANK A: `SK_DOOR_REAIM`, pre-emptive re-aim of the gunners we already own

**The defect, exactly.** `_turret` calls `_rotate_toward` only at `target is None` (:6998) or `hp_trend_ok` failure (:7002). A door gunner firing at an enemy *builder body* (`SK_PRI_BODY = 2`) on its current ray will never turn to face the **MARKED** core-killer (`SK_PRI_MARKED = 5`) sitting inside its own r²=13 on another bearing — even though `_marked_positions` :4295-4297 already puts the slot-15 shooter in that set and `_target_pri` already ranks it second only to their core. **The priority ladder is correct; the ray is wrong, and nothing turns it.**

Two supporting defects in `_rotate_toward` itself: the cap (`SK_HOME_GUN_ROT_CAP = 6`) is gated `if SK_HOME_GUN_ROTATE and (SK_HOME_GUNNER or SK_GUN_ROUTEBLOCK)` (:7180) — **both masters are False, so rotation currently ships UNCAPPED**; and the loop takes the *first* passing enemy within d²≤13 (:7184), not the highest-priority one.

**Why this shape and not (b):** the in-tree evidence separates the two halves of the T19 package. sk_maps:1836-1839, on the `SK_HOME_GUNNER` arm: *"⛔ NOTE THE ROTATION GOES THE OTHER WAY FROM PLANK 3's: with `SK_HOME_GUN_ROTATE` off this arm reads **8 kills, not 12**. Rotating at a LIVE threat helps; rotating at a BARRIER is the defect."* The **purchase** half is a measured −7 on by-r300; the **re-aim** half is worth +4 kills inside the same arm. ⚠ Honest framing: rotation was already ON in that arm's control, so this is *not* an un-weld of a dormant flag — the new behaviour is **pre-emption**, and it has never been measured.

**Files / functions touched:** `sk_roles.py::_turret` (:6994-7004), `sk_roles.py::_rotate_toward` (:7161-7210), `sk_maps.py` flag block, `sk_roles.py` import list.

**Flags (defaults; OFF = exact identity):**
```python
SK_DOOR_REAIM      = True   # a gunner may rotate to bring a MARKED target into
                            # its ray, PRE-EMPTING a current target of strictly
                            # lower priority.  OFF restores "rotate only when the
                            # ray is empty" exactly.
SK_DOOR_REAIM_PRI  = 5      # SK_PRI_MARKED.  Only a marked tile (slot-15 corefire
                            # shooter / slot-2 home threat / inferred belt killer)
                            # justifies giving up a round of fire.
SK_DOOR_REAIM_CAP  = 2      # PER TURRET PER GAME.  10 Ti + 1 cooldown each; at
                            # 130-173 Ti of converts in contact, 6 (the existing
                            # SK_HOME_GUN_ROT_CAP) is ~40% of the game's ammo.
SK_DOOR_REAIM_FLOOR= 40     # bank left standing after the 10 Ti.  Strictly above
                            # _rotate_toward's existing 30 (:7168) because the drip
                            # is need-based and clamps to `have` (sk_core:307).
SK_REAIM_CAP_LIVE  = True   # ⛔ CORRECTNESS RIDER: bring SK_HOME_GUN_ROT_CAP live
                            # independent of SK_HOME_GUNNER/SK_GUN_ROUTEBLOCK.
                            # Today both masters are False and rotation is UNCAPPED.
```

**Pseudocode** (in `_turret`, replacing :6998-7004):
```
best, target = <existing scan over get_attackable_tiles()>
if SK_DOOR_REAIM and self.reaims < SK_DOOR_REAIM_CAP:
    cur_pri = best[0] if best is not None else -1
    if cur_pri < SK_DOOR_REAIM_PRI:
        m = self._best_marked_off_ray(ct, p, kind, marked)   # NEW helper
        if m is not None and self._rotate_to(ct, p, m):      # 10 Ti + cd 1
            self.reaims += 1
            return
if target is None:  <existing _rotate_toward path>
```
`_best_marked_off_ray`: gunners only (`kind == EntityType.GUNNER`; a sentinel cannot rotate); over `marked` tiles, `ibp()` **before** any vision or tile call (CLAUDE.md s50 — `is_in_vision` is a pure radius test); `p.distance_squared(m) <= 13`; `ct.can_fire_from(p, face, GUNNER, m)` must be True for `face = p.direction_to(m)`; the tile must currently carry an **enemy** entity (team check — the v612 FIX 1 lesson, sk_roles:960-968: latched tiles have no team check and 23 pecks landed on our own belt); rank by `_target_pri` then by `-d²`, not first-found.

**Per-unit state and clear-list obligations:** `self.reaims = 0` in `main.py::__init__` beside `self.rotations` (:983). **NOT** on `_clear_plans`' list (sk_common:354) — a turret is a building and cannot be thrown; the displacement guard's clear list is for throwable bodies only (design build rule 5). No new cross-round Position cache is introduced.

**Expected dose, with SUBJECT lines.** *Subject: v180, 65 unrated games vs three pinned opponents (BC v68 / Pivot v249 / kladde v173), 2026-08-22 08:24-09:01Z, `scratchpad/s54_fc_games.json`.* Our home-side turrets: **1.30 (MIRROR) / 1.70 (PIVOT) / 1.64 (KLADDE) per game**; our gunners **1.6/game** against Pivot's 4.7 (DECODE:492-494). At cap 2 that is a **ceiling of ~3 re-aims per game and a realistic dose of 0.5–2**. This is a thin lever — the dose column must be read before the outcome column.

**Falsifiers:**
1. **Precondition (dose):** `reaims` summed = 0 across all 60 fixture cells ⇒ inert; the outcome column must not be read.
2. **Mechanism:** re-aims occur but *damage taken by our core from the marked shooter* does not fall in the treated cells ⇒ refuted on its own mechanism, regardless of kills.
3. **Programme (the r300 ITT guard, `DEFENCE_ADMISSION_BAR`):** share of **ALL** games ending in our core-kill by r300 must not fall vs control. Fixture control bars, from the registered v628 screen: **F1 ≥ 14/30, F2 ≥ 7/30 kills**; by-r300 control on the v620 arm = **12/30 = 40.0%** *(recomputed off `scratchpad/s54_v620/t_ctrl_f1/*.log`: kill rounds 119,125,136,137,151,161,178,201,222,265,270,285,402,585)*. First-plant median must not rise.
4. **Funding:** `10 × reaims / Ti_converted` per game must stay below 5%. **Report it as a fraction of converts, never as absolute Ti** — see §4.
5. **Thrash:** any turret re-aiming twice inside 6 rounds, or re-aiming back to a facing it has already held ⇒ the cap is the wrong instrument and a facing memo is required.
6. **Instrument control (mandatory):** one arm with `SK_DOOR_REAIM_PRI` inverted (re-aim only at targets *below* the current one). Every counter must move and the outcome must change; a constant `reaims` column validates nothing.

**Fixture precondition, engine-side only (bot stdout is dead, both platform and local — CLAUDE.md s54):** the marked tile is engine-readable as (i) an enemy gunner/sentinel BUILD event within d²≤13 of one of our live gunners, (ii) with a negative `UpdateHp` delta on our core attributable to it. Facing changes are readable as **`rotate()` re-emissions** — the primitive already exists in `scratchpad/s54_fc_decode.py` (used for DECODE §5.1's belt-gun facing tracking). **There is currently no rotations/game column for our line anywhere in the repo** — building it is a prerequisite, not a nice-to-have.

---

### 3.2 RECOMMENDED RIDER — PLANK B: `SK_ARMED_SWEEP`, in-vision liveness expiry (QUEUE #121)

`armed_memo` / `armed_facing` are written in `_sense` :1227-1246 and **never expire for gunners or sentinels**. The only sweep is `_live_launchers` :801-837 (launchers only, `SK_PLUCK_MEMO_TTL = 60`). QUEUE #121's GREP confirms all four removal sites are conditional and `armed_memo.*(ttl|expir|age)` returns **0 hits**. Consequences, all of which sit on the answer path: `_danger_tiles` (sk_common:535, cache keyed on `_armed_rev` = new tile or new facing only) makes a dead turret's ray a **permanent** navigation detour; `_on_armed_axis` :1112 vetoes counter-turret sites off dead sentinels forever; `_core_ray_shooter` :569 can name a corpse.

**Form — a liveness sweep, NOT a TTL.** A blind TTL kills bodies (turrets are immovable and mostly persist; the docstring's own pricing is "over-marking costs a detour, under-marking costs a body"), and `SK_COUNTER_LIVE_TGT` (sk_maps:1206) already measured the naive invalidation as **worse alone**. The safe generalisation of `_live_launchers`' existing rule costs **zero engine calls**: inside `_sense`, collect this round's seen-armed tiles from the loop already running; afterwards drop any memo tile that is in-bounds and within a *conservative* radius of this body (`d² ≤ vision − 2`, to avoid boundary flapping) yet absent from the seen set. Bump `_armed_rev` on deletion so the danger cache rebuilds.

⭐ **Side-lane rider, already banked on #121 and binding here:** the immobility premise has a **second recorded site** outside `armed_memo`'s four removal points — `_core_ray_shooter`'s docstring (sk_roles:566-570). **The design must enumerate premise sites by grep and fix all of them, not one.**

```python
SK_ARMED_SWEEP      = True   # drop an armed_memo/armed_facing tile that is inside
                             # this body's vision and was NOT re-sensed this round
SK_ARMED_SWEEP_MARGIN = 2    # d² shaved off the vision radius; boundary flap guard
```
**State:** none new. `armed_memo`/`armed_facing` stay off `_clear_plans` — they are absolute tile keys and survive a throw correctly.
**Falsifiers:** (1) deletions = 0 across 60 cells ⇒ inert. (2) `len(_danger_tiles())` at r300 does not fall ⇒ the over-marking claim is refuted. (3) forward-builder deaths inside a <20-round-old enemy gunner's r²≤13 must not *rise* (#121's own column). (4) an inverted control that expires tiles that WERE re-sensed must move every counter and change the outcome. (5) the r300 ITT guard as in 3.1.

---

### 3.3 HELD BEHIND A PRECHECK — the counter-battery gate re-price

`SK_COUNTER_SENT` (sk_maps:1255) is **the only verb in the tree that reaches a d²≤32 killer** — a home SENTINEL (r²=32) sited off their axis, and *a sentinel cannot rotate*, so a gun off its firing line is fighting something that physically cannot answer. Its null is attributed by its own flag comment not to the verb but to the gate: *"⇒ THE GATE IS ALMOST NEVER OPEN IN TIME. It needs `SK_COUNTER_RNDS = 20` rounds of UNBROKEN alarm … the shipped streak median is 11."* **The previous arm tested the gate, not the verb.**

**Do not build it yet.** Run the precheck first, because it is free and it decides the r300 question outright:

> **PRECHECK (engine-side, on an existing tape — no code ships):** reconstruct `corefire_streak` from per-round negative `UpdateHp` deltas on our own core + `SK_COREFIRE_TTL = 24`. Report, per game: (a) does a streak reach N ∈ {6, 8, 10, 12, 20}? (b) **at what round?** (c) **what is the by-r300 kill share of the games in which the gate would open, versus those in which it would not?**
>
> If the gate's opening is essentially disjoint from the by-r300 population — which is the design's own claim, since a game we win at r180 has no 8-round core-fire streak — the plank **cannot** regress the ITT primary by construction, and that is a far stronger r300 argument than any post-hoc non-regression read. If the gate opens in games we currently win by r300, the plank is r300-exposed and must not be built.

Cost if built: 30×scale Ti + `SK_COUNTER_SENT_RESERVE = 20` + 30 ammo (3 shots × 18 = 54 kills a 40 HP turret) ≈ **60-90 Ti**, i.e. **35-50% of a contact game's entire convert budget.** That is why it is second, not first.

---

### 3.4 REFUTED FOR THIS WAVE, with evidence

**(a) as literally specified — "plant a counter-turret orthogonally adjacent to a detected enemy forward turret":** the *idea* survives; the *specification* contains an engine-geometry error worth correcting before anyone codes it.

> ⭐ **A builder standing ORTHOGONALLY adjacent to the target cannot build on a tile orthogonally adjacent to that target.** Builder at (0,0), enemy sentinel at (1,0): the builder's legal build tiles are (−1,0), (0,−1), (0,1), (1,0)[occupied]; the sentinel's orthogonal neighbours are (0,0)[the builder itself], (2,0), (1,−1), (1,1). **Intersection is empty.** The counter-plant requires a **DIAGONAL stance** — builder at (0,0), sentinel at (1,1) ⇒ (1,0) and (0,1) are both legal and both orthogonally adjacent to the target. `_counter_march` :951 marches to *orthogonal* adjacency (`abs(dx)+abs(dy)==1`), so it arrives in the one stance from which the plant is illegal.

If the builder does eventually run this: staff it with the **ORE DENIER**, not the keeper and not the engineer. The denier is already there (`_counter_march`, `SK_COUNTER_PECK = True`, fence `SK_COUNTER_PECK_DSQ = 100`) and its alternative that turn is pecking the same target at 2 damage — so the **marginal turn cost is zero**. Cost comparison per enemy sentinel killed: **20 pecks = 40 Ti at ~19-33% conversion ≈ 160 Ti/kill** versus **an adjacent gunner: 20×scale Ti + 24 ammo + ~26 Ti of scale-tax ≈ 90 Ti at BC's measured 87.2% ≈ 100 Ti/kill.** Real, but it is a *new purchase* and a **+20% step on the one global additive cost factor that reprices the engineer's second band sentinel** — the measured kill lever (0 wins/14 games with ≤1 sentinel, 6/16 with ≥2). Its own cap, never `SK_DOOR_GUN_CAP`.

**(b) the home-gun sweep — REFUTED as re-proposed.** This *is* `SK_HOME_GUNNER`, built and measured: by-r300 **12→5**, median kill **201→315** (sk_maps:1828-1847). The commissioning question "why does `SK_DOOR_GUN_CAP=2` underperform" has a measured answer and it is **none of latency, siting or ammo**: cutting the cap to 1 costs by-r300 10→6 and deferring the purchase costs 10→8 — **the two door guns are already at the local optimum on the purchase axis.** What underperforms is the *aiming* of the guns we own (§3.1).

**(c) #123's counter-target rung — REFUTED for this wave, kept queued.** The rung is one line in `_target_pri` :4308-4309 (GUNNER and SENTINEL are scored identically today; QUEUE #123's GREP confirms the type rung does not exist). Three reasons not to spend a wave on it now: (i) it is a *choice* lever, and our answer is **reach**-limited, not choice-limited — 25-38% of killers are outside every turret we own under any facing; (ii) it points the wrong way for the finisher class — #123 says prefer their GUNNER, while our killer is a **sentinel in 63/63**, and `_core_ray_shooter` :595-605 *already* ranks sentinel above gunner in the home-defence context, which #123's own GREP says should stay; (iii) n=1 opponent, and the row itself says "generality UNKNOWN — stated." **A both-ways fixture spec is given in §5.3 anyway**, because the row is admitted and certified and will rise.

**(d) threat-memory expiry — ADOPTED, as PLANK B.** The staleness is load-bearing for the answer path (L5), so it rides rather than waits.

---

## 4. THE FUNDING QUESTION

Titanium and ammunition are **one currency** (`convert_ammo` is 1:1; `_drip` sk_core:266-325 converts `need − ammo`, clamped to `have`, every round, never banking). So peck-Ti, rotate-Ti, purchase-Ti and shot-Ti all draw the same pool.

**Engine exchange rates** (CLAUDE.md entity table): sentinel 10 ammo → 18 dmg = **1.80 dmg/Ti**; gunner 4 ammo → 7 dmg = **1.75 dmg/Ti**; builder peck 2 Ti → 2 dmg = **1.00 dmg/Ti**; rotate 10 Ti + 1 cooldown, gunner only.

**Cost of one answer, per shape, and what it displaces** *(displacement in sentinel-shot equivalents against the MIRROR median of 130 Ti converted/game, where saturation is 97%)*:

| shape | Ti per answer | as % of a contact game's converts | displaces |
|---|---|---|---|
| **PLANK A re-aim** (cap 2/turret) | **10-20 Ti**, zero marginal ammo — it redirects shots already being fired | **6-15%** | 1-2 sentinel shots = 18-36 core damage |
| **PLANK B sweep** | **0 Ti** (CPU only) | 0% | nothing |
| **(a) counter-plant gunner** | 20×scale + 24 ammo + ~26 scale-tax ≈ **90 Ti** | **52-69%** | ~9 sentinel shots = **162 core damage of the 227 we deliver** |
| **(3.3) counter-battery sentinel** | 30×scale + 20 reserve + 30 ammo ≈ **60-90 Ti** | **35-50%** | 6-9 sentinel shots |
| **(b) `SK_HOME_GUNNER`** | one gunner + its whole ammo stream | — | **measured: by-r300 12→5** |

**The scale-tax term is not decorative.** Cost scale is ONE global additive factor: every gunner or sentinel is **+20 percentage points on all subsequent builds of every type**. On a typical remaining build list (2 sentinels + 10 conveyors + 2 harvesters ≈ 130 Ti of base cost), one extra turret adds ~26 Ti — landing precisely on the engineer's second band sentinel, which the tape identifies as the kill lever.

⇒ **A plank that spends more than ~10% of converts in the contact cell defunds the checkmate and fails the directive's own second clause.** Only PLANK A and PLANK B clear that.

### ⛔ 4.1 THE FIXTURE UNDER-PRICES AMMO BY 3-4×, AND THE r300 GUARD ONLY HAS POWER WHERE THE COST IS INVISIBLE

This is the sharpest methodological risk in the brief.

| surface | Ti converted/game | timely-kill (kills by r300 / all games) |
|---|---|---|
| local FIXTURE A / B (15 g/seat, NOISE_OFF `_v542wave`) | **504 / 536** | **12/30 = 40.0%** |
| live field (65 unrated games, three pinned opponents) | **130 / 173 / 162** | **1/65 = 1.5%** |

**A defensive spend that is 6% of converts on the local screen is 25% of converts in the field.** And the `DEFENCE_ADMISSION_BAR`'s ITT primary has statistical power only on the fixture — where the ammo constraint is 3-4× looser and therefore where the cost is invisible.

**Mitigation, and it should be a standing rule:** report every plank's spend as **`plank_Ti / Ti_converted` per game**, not as absolute Ti. The *ratio* transfers between surfaces; the absolute does not. Then multiply the fixture ratio by the field's 130-173 Ti to predict the field cost before shipping.

---

## 5. FIXTURE DESIGN

### 5.1 The reference tapes and their precondition rate — MEASURED

`scratchpad/s55_siteless/t_pb_f{1,2}`: 30 games each = **15 maps × 2 seats × 1 seed** (f1 seed 7, f2 seed 11 — repo-compliant: vary map and seat, never seed). Our arm = `arm_pb_clean` = `_v622nestfall` with `SK_NEST_EXHAUST_PB=True` (diff vs the shipped tree is comment-only). Outcomes f1 15/30, f2 8/30.

⚠ **Correction to the caveat carried at `docs/coordination.md:73025` ("F1/F2 opponents are our own trees"):** verified off every log's `Running match:` line — **f1's opponent is `opp_v542wave_noiseoff` (our benchmark tree); f2's is `opp_mjolnir_noiseoff`, x3r0's imported Mjolnir tree, which is the PROGRAMME `BASELINE`.** Both are authored deterministic bots and neither establishes prevalence, but only one of them is ours.

Precondition "an ENEMY forward gunner/sentinel is planted in OUR half", decoded with `tools/corpus/replay_builds.py` (no hand-rolled decoder), cross-validated against `skalman_fidelity.py --manifest` (`fwd_turrets_against_anchor` = 47/56, **exact match**):

| | **f1** | **f2** |
|---|---|---|
| games with ≥1 | **24/30 = 80.0%** | **24/30 = 80.0%** |
| plants / game | 1.57 | 1.87 |
| median first-plant round | r60 | r80 |
| type mix | sentinel 38 / gunner 9 | **sentinel 56 / gunner 0** |
| **d² ≤ 13 (gunner-reachable)** | **57.4%** | **64.3%** |
| planted before r150 | 72.3% | 58.9% |
| M7 on the tape (games as units, DEFF 1.833) | 54.9% ± 21.0 | 20.5% ± 15.3 |

**Density vs live:** f1 1.50 / f2 2.10 enemy turrets near our core per game, against **KLADDE 3.48 / MIRROR 4.30 / PIVOT 4.55** ⇒ **the tapes carry the precondition at 35-50% of live density.** Attribution surface, not a rate surface — exactly as the repo already says.

**Densest early cells** (a v629 screen wanting an early home threat should decode these first): f2 `stavkirke_seatA` (3 point-blank, first at **r5**), f2 `stavkirke_seatB` (r6), f2 `midgard_seatB` (r14), f1 `jotunheim_seatB` (r40), f1 `valkyrie_seatA` (r52); densest overall f2 `icefloe_seatB` (6 point-blank but first at r214 — too late), f1 `helheim_seatB` / `holmgang_seatA` (3 each, first r64).

### 5.2 Live archive cells — the MIRROR hypothesis, corrected and then VERIFIED

⛔ **First, a premise correction: "MIRROR" is an OPPONENT CELL, not a map class.** DECODE:8-16 — MIRROR = vs Bean counters pinned v68 (20 games), PIVOT = vs Pivot v249 (20), KLADDE = vs kladde v173 (25). BC's 73.2% is M4b, a **subject-side siting property of BC's own plants that travels with BC on any map**. And **all three cells carry the precondition densely — PIVOT is the densest (4.55/game)**, so "MIRROR is special for the precondition" is refuted. What is special about BC is plant **depth** (M4b 73.2% point-blank vs our 0.0%), not plant **count**.

⭐ **Second, the underlying map hypothesis is VERIFIED, with the opponent confound controlled.** Symmetry classified two ways (`.map26` protobuf field 5 per `tools/make_map.py:12`, plus geometry for the 18 maps lacking it; cross-validated 9/9 on known `inv_*` maps; 35/35 map names classified). Pool = `corpus/join.tsv`, **verified RATED-ONLY** (6,843 of 6,843 files present in `ladder_games.tsv`, **0 overlap** with `unrated_games.tsv` — not the `meta_join` pooling hazard):

| | events | point-blank (d²≤13) share of enemy forward g/s plants |
|---|---|---|
| **MIRROR maps** | 10,282 | **56.6%** |
| ROTATIONAL maps | 15,589 | **41.9%** |

Pooled **+14.7pp**. Stratified **within opponent** (40 opponents with ≥30 events on both classes): **+12.1pp**, and **33 of 40 opponents positive — two-sided sign test p = 4.2e-5, opponents as units** (40 clusters, above the repo's 30-cluster floor). *Caveats stated: RATED only; **anchor-origin** d² per `replay_builds.py:112-113`, which is comparable to M4e/M4f `*_anchor`, **not** to the footprint-origin M4b that produced BC's 73.2%; pooled pp uncorrected for MATCH/MAP/CONTENT-DUPLICATE clustering — **the sign test is the claim to bank, not the pooled pp**.*

**Base rates:** ≥1 enemy forward turret in 5,883/6,843 = **86.0%** of rated games (mean 3.78/game, median first plant r30); narrowed to "≥1 enemy gunner/sentinel within d²≤50 of our core" = **83.1%**; "≥1 point-blank d²≤13" = **60.6%** (n=6,573).

**Named fixture candidates, ranked on density × earliness** (RATED provenance, `corpus/join.tsv`):

| opponent | n | point-blank % | median first pb round | mirror-map games |
|---|---|---|---|---|
| **Team 48** | 140 | **95.0%** | **r15** | 56 |
| **Powered by SmartFridge** | 130 | 92.3% | **r14** | 53 |
| **CtrlAltDefeat** | 135 | 79.3% | **r12** | 63 |
| not adgato | 135 | 87.4% | r55.5 | 63 |
| **lingling_40h** | 255 | 67.5% | r48.5 | 119 |

Team 48 and SmartFridge are the strongest precondition cells on the board. **lingling_40h is the convergence cell** — it is the subject of both #121 and #123, it is the top daily rated pairing, and #121's own fire order routes to it. Bean counters itself is thin in the corpus: **RATED-with-map n=10**, unrated v68 n=40 (100% carry the precondition, 92.5% carry an anchor-origin point-blank plant) — that plus the 20-game MIRROR decode cell is the entirety of our BC data.

### 5.3 The both-ways fixture for #123, honestly specified

We cannot run opponents' code, so a "sentinel-refunded / gunner-sticky" fixture must be **authored**, and CLAUDE.md's standing ruling applies: `bots/*_probe` fixtures lie in a known direction, and a road may be *prioritised* but never *closed* on one.

- **Arm ASYMMETRY-PRESENT:** an authored opponent that rebuilds a killed ring SENTINEL at +1 round and a killed ring GUNNER at +56 rounds — lingling v86's measured shape (`REPLAY-STUDY-lingling40h-v86-2026-08-22.md`: sentinel replaced 59% at median 1 round; gunner 27% at median 56).
- **Arm ASYMMETRY-ABSENT:** the same tree with both replacement latencies set equal (the midpoint). **This arm is the whole point** — the rung must change the outcome in ARM 1 and *not* in ARM 2. A rung that moves both is reading something other than the refund asymmetry.
- **Arm RUNG-INVERTED:** our tree with the priority reversed. Every counter must move and the outcome must change.
- Run each arm against both our rung-on and rung-off trees: **2 opponents × 2 our-configs = 4 cells × 30 games** (15 maps × 2 seats, one seed each). Deterministic ⇒ ablation identity is byte-exact.
- **⛔ Authored-probe caveat, stated inline in any banked result:** this fixture measures whether the rung *responds to* the refund asymmetry. It cannot establish that any real opponent has it. **Field confirmation is a pinned unrated leg vs lingling v86 via `fcode match unrated <team> --match <past_match_id>`** (in-band +37; a 5-0 pays +17.68, `target_value` read 11:12Z) — and per point 6 of the directive, that leg is what would *close* the road either way.

---

## 6. SURPRISES AND RISKS

**S1 — the committed line head is not the adopted configuration (§0).** Highest-priority item in this brief.

**S2 — M7's subject discipline: the brief's direction is RIGHT, its range is WRONG.** `tools/skalman_fidelity.py:236-239` and the implementation at `:541-549` (`if team != enemy: continue`, then `dsq_to_set(pos, cfoot[side]) < dsq_to_set(pos, cfoot[enemy])`) confirm M7 counts **the enemy's turrets planted in the subject's half, removed by the subject** — a defensive metric, our 20.8-… reading is correct. But:
- **The v180 field range is 20.8 – 56.6%** (KLADDE 20.8 / MIRROR 37.6 / PIVOT 56.6). **42.8% ± 3.3 is a different subject** — the v168-v177 archive baseline, n=961 games (`skalman_fidelity.py:35-37`, STUDY:753). Quoting "20.8-42.8" as one range mixes two populations.
- **The missing comparator changes the story:** BC's *opponents* clear at **33.5% (v47 era) / 53.3% (v68 era)**. Our 42.8% sits between them. **BC is the outlier; we are a typical BC opponent.** The honest synthesis: *"average against the average opponent, and 32 points behind the rank-1 bot in matched games"* — the matched pair being **us 37.6% vs BC 69.2% in the same 20 replays**, which the decode never states as a pair.
- **M7 is outcome-conditioned — a collider:** BC reads 89.0% in games it wins vs **61.2% in games it loses** (28pp swing, same bot). We lose 1-19 / 0-20 / 1-24 in the decode cells. Part of the gap is *caused by* the outcome.
- ⛔ **M7 does not attribute the removal to a killer.** `deaths` comes from raw `removeEntity` with no cause filter (`skalman_fidelity.py:398-408`). **An opponent demolishing its own turret scores as our clearance.** #121's own evidence: **541 turret self-removals with no damage across 90 lingling games (6.0/game, 88/90 games)**; our own Mjolnir self-removes launchers 197/358.
- ⛔ **Independent confirmation, and it is one-sided.** Recomputed off `scratchpad/s54_fc_games.json`: of the enemy forward turrets scored "killed", the share that **never took a single damage event** is MIRROR **22/38 = 58%**, PIVOT **20/50 = 40%**, KLADDE **7/26 = 27%** — while **0 of our 112 removed forward turrets were undamaged**. Corrected: **we kill 19-33% of their forward turrets, not 30-55%**, against their clean 70-89% of ours. **The asymmetry is wider than published, and every absolute M7 level in this brief is an over-estimate for us and clean for BC.**
- ⛔ **And M7 is a near-constant column against a driven placebo** (STUDY:3, s54 rider): turrets nowhere near BC's belt read 73.1% ± 4.3 against the castle cell's 79.7% ± 2.2. **Do not A/B anything on M7 within one bot** — it is fine as a between-bot contrast and useless as a treatment response. Same rider: **17.3% of that v47 population are exact duplicate games**; intervals ~13% optimistic on top of DEFF 1.833.

**S3 — the r300 guard and the funding risk live on different surfaces (§4.1).** Fixture 40.0% timely-kill vs field 1.5% — a **26× gap**, and the fixture converts 3-4× more Ti. The guard has power exactly where the cost is hidden.

**S4 — "contact" is a fixture contrast, not a within-game state.** The 4× drip collapse (DECODE §4.1) is a between-fixture difference of medians — an authored local bot vs three real ladder bots — with no round-indexed contact flag and no per-round `need`-vs-balance trace (DECODE:635-637 says so). The honest span is **~2.8–4.5×, centred near 3.3×**, and no interval exists (`ci95` is null for M3b/M3c/M3e in every fidelity JSON). Its two candidate mechanisms — turret lifetime (our forward tubes live 9-14 rounds) vs funding (M1 belt connectivity 42/30 → 17-20) — are explicitly **not separated**.

**S5 — the counter-plant's geometry error (§3.4).** A builder orthogonally adjacent to the target cannot build orthogonally adjacent to it. Anyone implementing (a) from the playbook wording will build a verb that can never fire.

**S6 — who pays, per shape.** PLANK A is paid **entirely by turrets** — no builder turn at all, so it competes with neither the engineer's checkmate (`SK_NEST_CLEAR` now spends up to 12 rounds of chew per site at 2 Ti/turn) nor the keeper's home economy. PLANK B is CPU-only. Shape (a) would be paid by the **ORE DENIER** at zero marginal turn cost (it is already marching and pecking) but competes with COPY 1 ore denial and ledger V5. Shape (b) and 3.3 are paid by the **KEEPER**, whose turn the line has now measured as the scarce resource seven times (`SK_SEAT_CLEAR`, `SK_SEAT_CLAIM`, `_home_launcher`, v603's collar peck, v610). **Never staff a home answer with the engineer.**

**S7 — PLANK A's dose is thin.** 1.3-1.7 home turrets/game, gunners only (sentinels cannot rotate), cap 2 ⇒ ceiling ~3 re-aims/game. And there is **no rotations/game column for our line anywhere in the repo** — the instrument must be built and both-ways-driven before the arm fires, per the standing instruments rule.

**S8 — two latent defects found in passing, neither a plank.** (i) Rotation currently ships **UNCAPPED**, because `SK_HOME_GUN_ROT_CAP`'s gate requires `SK_HOME_GUNNER or SK_GUN_ROUTEBLOCK` and both are False (sk_roles:7180). (ii) `_turret`'s ammo guard returns *before* `_rotate_toward` (:6906) — **a turret at zero ammo cannot even re-aim for next round**, so it stays mis-facing through the whole dry spell.

**S9 — DEFF enumeration for the v629 screens.** MATCH **dead** (deterministic single-seed local fixture). OPPONENT **dead** (one opponent per tape). MAP **live** — measured 4.57 on the v620 tape, interval ×2.14 at 180-240 games/cell. CONTENT-DUPLICATE **must be verified, not asserted** — the v628 grid required a duplicate control and the same-tree same-bot swing measured 2.22pp at n=900, which is **wider than any dose PLANK A can produce**. ⇒ the deterministic tapes are an **attribution** surface; any level claim needs the powered grid with the duplicate control, and the ship rule's ±1.5pp bar remains finer than the fixture's own reproducibility at n=900 (v618's finding, main.py:41-50).

---

## RECOMMENDED ORDER

1. **Fold the adopted flag values into `bots/_v628compose`** and re-assert the identity (§0). Nothing else is meaningful until the head is the head.
2. **Build the rotations/game instrument** off `rotate()` re-emissions (the primitive exists in `scratchpad/s54_fc_decode.py`), drive it both ways, and measure our current rotation dose. If we already re-aim freely, PLANK A's premise is wrong and this is a half-hour null instead of a wave.
3. **v629 = PLANK A (`SK_DOOR_REAIM`) + PLANK B (`SK_ARMED_SWEEP`)**, ablation identities on `t_pb_f{1,2}`, then the composed screen, then one powered read against the duplicate control. Zero new turret purchases, zero marginal ammo — the only class of home answer this line's own seven measured negatives leave open.
4. **Run the §3.3 precheck in parallel** (free, no code): if the counter-battery's alarm gate is disjoint from the by-r300 population, the reach answer becomes buildable with a constructive r300 argument rather than a hoped-for non-regression.
5. **#123 stays queued** with the both-ways fixture spec of §5.3 attached; it is a choice lever and the binding constraint is reach.