# DESIGN STUDY — FORTRESS/HEIMDALL (banked verbatim, agent report)

**PROVENANCE: builder-commissioned fresh opus agent, s57 2026-08-22 (registered
on the coordination tail; two mid-flight addenda: the r300 phase-flip ruling and
the belt-repair doctrine question). Banked verbatim by the builder from the
agent transcript. The builder's consumption decisions are on the tail note of
the same timestamp; nothing here is a verdict until the builder types it.**

Both agents are in and I have the rest first-hand. Here is the study.

---

# FORTRESS DESIGN STUDY — `bots/_v628compose` → HEIMDALL

*Game context: in-engine design for the Florent Code League, a sandboxed bot-vs-bot competition on a simulated grid under organiser-approved rules. Every "destroy", "raider", "siege", "kill" below is an engine API call or the game's stated win condition.*

**Directive state at time of writing:** FORTRESS DOCTRINE (`PROGRAMME.md:51-77`) + CITADEL block (`:78-97`), and the Q3 ruling relayed mid-study — *"until round 300 our entire focus is eco, then we send two raiders that puts up as many sentinels as necessary to bring the enemy core down."* That ruling converts the fortress from a doctrine into **phase 1 of a two-phase game**, which changes §6 materially (most "dead" verbs are *deferred*, not dead) and adds §8.

---

## 0. THREE FACTS THAT RESHAPE THE BRIEF BEFORE ANY DESIGN

**0.1 ⛔⛔ BUILDERS CANNOT ATTACK ENEMY BUILDER BOTS. THE BRIEF'S CENTRAL VERB — "4 builders peck the raider, 8 dmg/round vs 40 HP = 5 rounds" — IS ENGINE-BARRED.**
Measured by running, s37 2026-08-13, banked at `docs/coordination.md:43836-43840`: *"builder melee CANNOT target enemy builder bots (`can_fire=False` on adjacent enemy builder, every occurrence)"*. It is also true by the API definition in `CLAUDE.md`: a builder bot's attack is *"2 Ti → 2 dmg to **the building** on an orthogonally adjacent tile"*. Corroborated structurally in the tree: **every one of the 13 `ct.fire()` sites in `sk_roles.py` selects its target through `ct.get_tile_building_id()`** — `_peck_priority:4392`, `_clear_tile:5104`, `_melee_harvester:5283`, `_counter_march:955`, `_belt_evict`, `_seat_clear`, `_door_action:3430`. The **one** exception is `_home_defence` (`sk_roles.py:6738-6766`), which deliberately does *not* refuse on an empty building read (`:6746-6751`: *"a body is not a building — refusing on an empty read would disable the march at exactly the threat V5 exists for"*) and then calls `ct.can_fire(threat)` — **which returns False.** So today's behaviour against an intruding builder is: *the ore denier marches to it and stands there.*

⇒ **The FORTRESS_RESPONSE clause ("all builders are to destroy them") is executable against enemy BUILDINGS and not against enemy BODIES.** The verbs that reach a body are exactly three: **turret fire** (`_turret:6919-6920` reads `get_tile_builder_bot_id` and scores it `SK_PRI_BODY=2`), **launcher relocation** (`can_launch` has no team check — `SK_HOME_LAUNCHER` machinery, OFF), and **tile denial** (bodies cannot stack; barriers/our own bodies deny movement).
⚠ **Recommended action before any build: re-probe it.** The fact is 9 days old, from a different tree and possibly a different engine build, and it is now load-bearing for the whole doctrine. A 10-minute local probe (walk a builder adjacent to an enemy builder, log `can_fire`, and separately log an ungated `fire()` in a throwaway unit) settles it. Doctrine text should be corrected to Magnus either way — this is a "his directive names a verb the engine does not have" item, not a design preference.

**0.2 ⭐ EVERY BOUNDED HOME VERB IN THIS TREE WAS SIZED AGAINST A ONE-BODY HOME BUDGET. THE FORTRESS QUADRUPLES THAT BUDGET, SO EVERY ONE OF THOSE CAPS IS RE-OPENABLE.**
The measured cause behind three separate refutations is one sentence, repeated verbatim across the tree: **"THE KEEPER'S TURN IS THE SCARCE RESOURCE"** (`main.py:16`, citing v603's unbounded collar peck, v610's `SK_SEAT_CLEAR`, and the launcher axis ×3). It is written into constants: `SK_APRON_RELAY_CAP = 2` per 20 rounds (`sk_maps.py:2020-2023`, *"the keeper's turn is scarce and the belt duty has to survive the plank"*), `SK_SEAT_PECK_CAP = 15` / `SK_SEAT_PECK_TOTAL = 90` (`sk_maps.py:1411-1421`), `SK_SEAT_CLAIM_WALK_DSQ = 8` (`sk_maps.py:1807`, *"the v610 finding written into the walk"*), `SK_DOOR_GUN_CAP = 2` (`sk_maps.py:2515`), `SK_SEAT_HEAL_MAX = 60`.
And the structural cap is real, not just numeric: **at most 2 of 4 bodies can ever answer a home threat** — `_home_defence`/`_denier_home_answer` are gated `self.role == SK_ORE_DENIER` (`sk_roles.py:304, 307`), `_keeper_counter` runs only from `_home_keeper:1279`, and `_cage_walker`/`_siege_engineer` contain **zero** references to `corefire`, `_home_defence`, `SK_SLOT_THREAT_POS` or `SK_SLOT_UNDER`. The exemption is explicit doctrine at `sk_roles.py:275-280`: *"the walker is the KILL branch, and 'not at the kill's expense' cuts the other way for it."*
⇒ **The fortress deletes the premise that produced every one of these caps.** This is the single highest-leverage, lowest-code plank family on the board: *raise the caps that were priced against a scarcity that no longer exists.*

**0.3 ⭐ THE CITADEL ZONE IS ALREADY FULLY SENSED. NO NEW SENSOR IS NEEDED FOR THE CITADEL BAR.**
`_threat_scan` (`sk_core.py:82-133`, writer: CORE, once per round) already publishes **the nearest of {enemy BUILDER_BOT, GUNNER, SENTINEL, LAUNCHER, BARRIER}** within `dsq_core ≤ SK_HOME_RING_DSQ*3 = 39` of our core, into slot 2 (`SK_SLOT_THREAT_POS`), and latches slot 1 (`SK_SLOT_UNDER`). Chebyshev-3 of a 2×2 footprint has maximum `dsq_core = 3²+3² = 18` — **strictly inside both the d²≤39 publish fence and the core's own r²=36 vision.** The citadel zone is a subset of what the core already sees and already broadcasts, every round, for free.
⇒ **What is missing is not detection. It is (a) DISPATCH — three of four roles never read slot 2 — and (b) a WEAPON that reaches a body (0.1).**
The exact citadel predicate is a 5-line helper: `dsq_core` (`sk_common.py:187-204`) already computes the footprint-clamped `dx, dy`; `cheb_core(pos, o) = max(dx, dy)` on the same clamp gives Chebyshev-3 exactly. No new engine calls.

---

## 1. RE-HOMING THE FOUR ROLES

**Every enemy-core reference in the tree, enumerated** (`awk` over `sk_roles.py` by enclosing function — this is the complete list):

| function | lines | what the enemy anchor does there |
|---|---|---|
| `_cage_walker` | 4451, 4453, 4664 | `lap = cage_lap(self.enemy)` — the **entire role** |
| `_cursor_target` | 4845 | fallback walk target = enemy core |
| `_attack_enemy_core` | 5138, 5150, 5172 | melee the enemy footprint; the fallback for walker-off **and** engineer-off |
| `_ore_denier` | 5223 | fallback walk target = enemy core |
| `_deny_target` | 5304, 5329 | patrol **skips home-half ore** (`if self.is_home_half(ore): continue`) |
| `_deny_barrier` | 5251-5252 | `preempt = rnd >= 60 and not self.is_home_half(q)` — forward-only |
| `_siege_engineer` | 5360, 5505 | guard + relight |
| `_nest_scan` | **6059, 6081** | `ex, ey = self.enemy.x, self.enemy.y`; `d = dsq_core(q, self.enemy)` — **the band, in two lines** |
| `_firing_face` | **6237** | `for c in core_tiles_xy(self.enemy)` — the site must have a firing line onto **their** footprint |
| `_relight_close` | 5894, 5898 | close on the enemy band |
| `_belt_band` | 1764-1775 | belt must **avoid** d²≤32 of their core (defensive; stays correct) |
| `_home_gun_score` | 2547-2550 | tie-break toward the **enemy approach side** (defensive; stays correct) |
| `_claim_targets` | 2413-2414 | rank our seats enemy-nearest-first (defensive; stays correct) |
| `_hl_toward` | 3222-3224 | throw victims **away** from our core (defensive; stays correct) |
| `_launcher` | 7044-7056 | anchor resolution only |

### 1a. CAGE_WALKER (role 1) — today, and the minimal re-home

**Today** (`sk_roles.py:4440-4695`): computes the 12-tile Chebyshev ring of the **enemy** core (`cage_lap`, `:198-216`), surveys it, seals the 8 seal seats with barriers behind its own walk, evicts enemy conveyors off seal seats (`_evict_seal`), and once `sealed >= accept` falls to `_attack_enemy_core`. It is 100% forward and 100% enemy-anchored. Nothing in it survives the doctrine.

**Minimal re-home — recommended: SECOND ECO BODY + DEMOLITION DETAIL.**
Not "re-point the cage at our own core" — a cage around **our** core is what `SK_APRON_DENY` and `_seat_claim_action` already do, better and cheaper, and a second body running `cage_lap(self.core)` would fight the keeper's belt for the same 8 tiles (`tile_owner`/`may_build` arbitration, `sk_common.py:1585-1612`, would reject most of its builds).

Flag sketch (OFF = exact v628 identity by call-site conjunction, the tree's own convention, e.g. `sk_roles.py:1292` `if SK_DOOR and self._door_action(...)`):

```python
# sk_maps.py
SK_FORTRESS       = False   # master
SK_FORT_WALKER_ECO = False  # walker runs the keeper body plan instead of the cage
```
```python
# sk_roles.py _builder, replacing :319-326
if SK_FORTRESS and SK_FORT_WALKER_ECO and self.role == SK_CAGE_WALKER:
    self._home_keeper(ct, p, rnd)      # second eco body
elif self.role == SK_CAGE_WALKER:
    self._cage_walker(ct, p, rnd)
...
```
With `SK_FORTRESS = False` the first branch is unreachable and the dispatch is character-for-character v628.

⚠ **Two bodies in `_home_keeper` collide on three published slots.** `_belt_report` writes slot 5, `_killer_report` writes slot 14, `_belt_seed_store` reads/writes slot 5 — and the buffered store makes two writers in one round a **silent lost update**, the exact defect `SK_TEAM_TUBES` was built to fix (`sk_maps.py:2265-2290`: *"the RMW read returns LAST round's word... the loser's field is dropped EVERY round, not once"*, measured as a beat frozen for 291 rounds). **The publisher rungs must stay role-0-only:** gate `_belt_report`, `_killer_report`, `_belt_seed_store` on `self.role == SK_HOME_KEEPER`. The *action* ladder is safe to share (it is all local engine calls); only the four `wstore` sites need the gate. This is the single most likely silent-defect source in the whole fortress build and it should be a static-battery assertion, not a comment.

### 1b. ORE_DENIER (role 2) — today, and the minimal re-home

**Today** (`sk_roles.py:5188-5223`): `_deny_barrier` (barrier an ore tile whose harvester just died, or pre-emptively any **enemy-half** ore from r60) → `_peck_priority` → `_melee_harvester` (chew enemy harvesters/conveyors) → walk to `_deny_target`, whose patrol **explicitly skips home-half ore** (`:5329`). It is already the only role wired to the home answer (`_denier_home_answer:304`, `_home_defence:307`) — so it is **half-home already**, and it is the natural seed of the citadel responder.

**Minimal re-home — recommended: PERIMETER BODY (citadel responder + demolition), eco when idle.**
Three sub-changes, each independently flaggable:
1. `_deny_barrier:5252` — invert the pre-empt fence under a flag: `preempt = rnd >= SK_PREEMPT_ORE_ROUND and (not self.is_home_half(q) if not SK_FORT_ORE else self.is_home_half(q))`. ⛔ **But note this is now a self-harm verb:** a barrier on **our** ore denies **our own** harvester seat. The home-side value of `_deny_barrier` is only the *reactive* half (barrier an ore tile after our harvester on it died to a located killer — which duplicates `_harv_blocked`'s ban at `sk_roles.py:1556-1574` at 3 Ti of scale). ⇒ **Recommendation: retire `_deny_barrier` for the fortress rather than invert it.** It has measured 0 of 1,381 anyway (`sk_maps.py:5199-5201`).
2. `_deny_target:5329` — flip the home-half skip to a home-half *keep*, so the idle patrol walks our own ore instead of theirs. This is what makes the denier a useful perimeter body: it stands where harvesters are, which is where intruders come.
3. `_melee_harvester:5289` — the target set `{HARVESTER, CONVEYOR, SPLITTER}` is exactly right for the demolition detail; only the walk needs re-homing (change 2 does it).

### 1c. SIEGE_ENGINEER (role 3) — and the band question, answered precisely

**Today** (`sk_roles.py:5343-5615`): keeps `want` forward sentinels standing in the band d²14–32 of the **enemy** core, prepping each site with 2 barriers, holding station beside the newest when at the floor, falling back to `_attack_enemy_core`.

**⛔ THE BAND CANNOT BE RE-CENTERED BY A REFERENCE SWAP, AND THE REASON IS `_firing_face`, NOT THE DISTANCE.**
The distance test is two lines (`:6059`, `:6081`). But every candidate must also pass `face = self._firing_face(q)` (`:6098-6100`), and `_firing_face` (`:6233-6247`) iterates `core_tiles_xy(self.enemy)` and returns a direction only if the offset from `q` to an **enemy core tile** is axial or exactly diagonal. Swapping the two distance lines to `self.core` produces a ring of tiles 14–32 d² from **our** core, essentially none of which happens to line up axially/diagonally with the enemy footprint — so `_nest_scan` would return `None` almost always and the engineer would silently stop siting. Two further entanglements: the band constants are *defined by the target's counter-battery geometry* (`sk_maps.py:2489-2490`, *"inside sentinel reach (r²=32), outside every gunner's (r²=13)"* — that reasoning is about **their** ring, not ours), and `SK_TUBE_BAND_DSQ = 32` (`sk_maps.py:2315-2321`) independently classifies "is this a FORWARD TUBE" for the whole `SK_TEAM_TUBES` slot-7 machinery, and would desynchronise.

**⇒ A HOME-RING TURRET ENGINEER SHOULD REUSE `_pick_gun_site`/`_home_gun_score`, NOT `_pick_nest`.** Those two already are the our-core-anchored siting mode: `_home_gun_score` (`:2526-2558`) scores a `(site, facing)` **pair** by ray coverage of our delivery seats + apron, with a tie-break toward the enemy approach side; `_pick_gun_site` (`:3491`) scores by ray-reaches-the-named-killer, then ray-hits-the-ring-threat, then weighted trunk coverage. `_prep_barrier` (`:6249`) is site-relative and reusable as-is. The two siting modes already coexist in this tree; they are not interchangeable, and the home mode is the one that exists.

**Minimal re-home — recommended: HOME-RING TURRET ENGINEER on the `_home_gun_*` path, with a raised cap.**
```python
SK_FORT_RING      = False   # engineer buys home-ring turrets instead of forward tubes
SK_FORT_RING_MAX  = 3       # separate cap; SK_HOME_GUN_MAX=1 was priced under the kill clock
SK_FORT_RING_SENT = 1       # one FIXED sentinel on the approach axis (see §5)
```
```python
# _siege_engineer, immediately after :5364 (_stall_check), before `if not SK_NEST:`
if SK_FORTRESS and SK_FORT_RING:
    self._fort_ring_turn(ct, p, rnd)   # _home_gun_window/_score/_action/_walk with the new cap
    return
```
`_fort_ring_turn` is ~40 lines and calls existing methods only. OFF = unreachable branch = exact identity.

### 1d. HOME_KEEPER (role 0) — unchanged in structure, one fence to fix

Keeper stays the belt/harvester owner. **The one defect to fix is already a queue row:** `_home_keeper_move`'s economy walk is fenced by `is_home_half(ore)` **only** (`sk_roles.py:3997`) with **no d² term**, and `is_home_half` is a Voronoi half-plane (`sk_common.py:1562-1567`), so the keeper can legally walk to the midline. This is the confirmed puller behind the E6 keeper collapse (`QUEUE.md:959` row **#128 (a) LEASH**; core-footprint heals 398→80). Under the fortress the keeper is the *only* guaranteed core-adjacent body for the first ~120 rounds, so the leash matters more, not less.

---

## 2. ALL-BUILDER INTRUDER RESPONSE

### 2a. What exists (detection — complete)
| sensor | writer | fires on | fence | anchor |
|---|---|---|---|---|
| slot 1 `SK_SLOT_UNDER` | CORE | nearest {builder bot, turret, barrier} | `dsq_core ≤ 39` | `sk_core.py:114, 129-130` |
| slot 2 `SK_SLOT_THREAT_POS` | CORE | same, its position | same, gated `SK_DOOR` | `sk_core.py:131-132` |
| slot 15 `SK_SLOT_COREFIRE` | CORE | **our core's own HP delta**, + best-effort shooter tile | TTL 24 rounds | `sk_core.py:139-181`; `SK_COREFIRE_TTL` `sk_maps.py:998` |
| `armed_memo` (per body) | `_sense:1236` | `ARMED_TYPES = {GUNNER, SENTINEL, LAUNCHER}` — **not builder bots** | none; **no TTL** | `sk_maps.py:2422`; `sk_roles.py:1236` |
| `vis_enemy` (per body, ephemeral) | `_sense:1196-1246` | everything visible | body vision r²=20 | `sk_roles.py:1196` |
| `_apron_watch` | keeper | apron tile that **was ours and is now empty** | d²≤5 | `sk_roles.py:2878-2929` |

**Traced, an enemy builder at 2 tiles from our core, today:** slot 1 + slot 2 fire. Corefire does **not** (no HP loss yet). Only the ore denier reads slot 2 → `_home_defence` walks it there → adjacency → `can_fire` = False (§0.1) → it stands. Keeper/walker/engineer never engage. A home turret in range **would** kill it (`_turret:6919-6920`, `SK_PRI_BODY=2`) — and today we ship zero home turrets by default (`SK_HOME_GUNNER=False`, `SK_COUNTER_SENT=False`).

### 2b. What exists (dispatch — the reusable precedent)
**`_counter_march` (`sk_roles.py:908-1039`) is the dispatch verb and it is good.** It: retargets away from enemy launcher pickup discs (`_pluck_retarget`, engine bound d²≤2), **re-reads the target's owner at FIRE time, not latch time** (`SK_MARCH_TEAMCHECK`, `sk_maps.py:1092` — the v612 fix for 23 pecks landed on our own conveyor), relaxes the ledger-V7 heal-race veto once ≥2 friendly bodies are adjacent, and falls to a walk. Fenced `SK_COUNTER_PECK_DSQ = 100` of **our** core (`sk_maps.py:1082`) — already a home verb.

**⭐ The converge precedent is `SK_PECK_FOCUS` (`sk_maps.py:2145-2166`), SHIPPED ON — and its mechanism is worth copying exactly: there is no rendezvous protocol.** Two roles independently subscribe to the *same published fact* (slot 15's shooter tile via `corefire_shooter`, or their own `armed_memo` via `_core_ray_shooter`) and independently walk there. `_keeper_counter:1041` is the keeper's half, `_denier_home_answer:1082` the denier's; without the keeper half *"only ONE body ever marches, so 'two bodies adjacent' is unreachable and the relax can never fire — the two halves are one plank"* (`sk_maps.py:2162-2166`). `SK_PECK_FOCUS_BODIES = 2` is a **floor** for the veto relax, not a cap on participation.

### 2c. What is missing, and the minimal response verb

Missing: (i) walker and engineer never read slot 2; (ii) no citadel predicate; (iii) **no weapon that reaches a body** (§0.1); (iv) no staffing rule; (v) no disengage.

```python
SK_CITADEL          = False  # master
SK_CITADEL_CHEB     = 3      # Magnus's "3 squares", board distance, on dsq_core's clamp
SK_CITADEL_BODIES   = 2      # how many bodies may converge on one intruder
SK_CITADEL_GIVEUP   = 20     # rounds one body may hold one intruder (SK_CAGE_MELEE_GIVEUP's value)
SK_CITADEL_ROLES    = (SK_HOME_KEEPER, SK_ORE_DENIER, SK_CAGE_WALKER)   # engineer exempt
```
Verb (`_citadel_answer`, ~50 lines, called from `_builder` between `:305` and `:307`, under `if SK_FORTRESS and SK_CITADEL and self.role in SK_CITADEL_ROLES and self._citadel_answer(...): return`):
1. Read slot 2. Reject if `cheb_core(threat, self.core) > SK_CITADEL_CHEB`.
2. **Staffing without a comms slot.** All 16 slots are allocated (`sk_maps.py:2340-2385`; slot 15 was *"THE LAST FREE SLOT"*). Two options, both zero-slot:
   - **(cheap, recommended for plank 1)** static role priority: keeper + denier always (today's `SK_PECK_FOCUS` pair), walker joins only if `p.distance_squared(threat) ≤ SK_CITADEL_JOIN_DSQ`. Deterministic, no coordination, no new bits.
   - **(exact, for a later plank)** the beat slots have room: `SK_SLOT_BEAT[r]` uses 11 bits (`SK_BEAT_MASK = 0x7FF`) of 32, and `pack_tile` is 10 bits (`sk_common.py:92`, as used in slot 14's `KILLER_TILE_MASK`). Packing each body's tile into b11-20 of **its own** beat slot preserves the one-writer-per-slot rule exactly and gives every body a true nearest-N computation. 11+10 = 21 ≤ 32.
3. **Act.** Because of §0.1 the action ladder against a *body* is: (a) if a home turret bears on the tile, do nothing and let it shoot (`_gun_bears`, `sk_roles.py:2319`, already exists); (b) if `SK_HOME_LAUNCHER` is live and the intruder is inside the launcher's `d²≤2` pickup disc, the launcher's own turn handles it (0 ammo, 1 round — see §5); (c) otherwise **occupy and deny**: step onto the tile the intruder needs next and hold. Against a *building* it is `_clear_tile(ct, threat, rnd)` verbatim (§3).
4. **Disengage** — three independent conditions, all mirroring existing patterns: the tile no longer holds an enemy (owner re-read at act time, `SK_MARCH_TEAMCHECK`'s rule); `rnd - since > SK_CITADEL_GIVEUP` (`_clear_tile:5124`'s pattern); or the target leaves the Chebyshev-3 zone.

**Over-response fence.** The existing structural fence (only 2 of 4 roles can ever answer, `sk_roles.py:304/307/1279`) is *replaced*, so the numeric one has to be real. `SK_CITADEL_BODIES = 2` plus the engineer's exemption keeps ≥2 bodies on eco at all times, which is the CITADEL_ECON_RIDER in code. The mechanism metric that catches over-response is **eco-body-rounds per game** (rounds where a body executed a harvester/belt build), reported alongside intruder survival time in every screen.

---

## 3. DEMOLITION DETAIL

### 3a. The verb exists; the target selector does not
**`_clear_tile` (`sk_roles.py:5096-5134`) is a complete, guarded, general "chew the enemy building on tile q":** in-bounds + affordability (`:5101`), team check (`:5110`), **healing-race veto** `_enemy_builder_adjacent` (`:5119` — *"2 damage against +4 HP a round is a race we lose, and this is where the bulk of the 1,280 barrier pecks went"*), per-tile chew clock capped at `SK_CAGE_MELEE_GIVEUP = 20` rounds (`:5121-5125`), and ledger-V7 `hp_trend_ok` (`:5126`). **It accepts barriers** — the carve-out is explicit (`:5114-5118`: a barrier blocking the path the current action needs is allowed).

**What is missing is an enumerator.** There is **no function anywhere in the tree that lists enemy buildings in our half.** Every attack surface is either a fixed small ring (`_apron_list` d²≤5; `core_seats` 8 tiles; `_door_action` d²≤39, `sk_roles.py:3441-3449`, **TURRET_TYPES only**), a single-nearest pick (`_threat_scan`, `_counter_target`, `_deny_target`), or an orthogonal-4 local scan (`_peck_priority`, `_melee_harvester`, `_clear_tile`). `is_home_half` (`sk_common.py:1562`) has four consumers and **none of them iterates enemy buildings** — all four gate *our own* builds and patrols.

### 3b. The sweep
```python
SK_DEMOLISH      = False
SK_DEMOLISH_DSQ  = 39     # start at the existing home fence (SK_HOME_RING_DSQ*3), widen later
SK_DEMOLISH_CAP  = 20     # pecks per (tile, occupant-id) episode; the _seat_charge pattern
```
`_demolish_target(ct, p, rnd)`: one pass over `ct.get_nearby_buildings()` (already the tree's idiom, `sk_roles.py:233`), filter `get_team != self.team` and `dsq_core(pos, self.core) <= SK_DEMOLISH_DSQ`, score by class, return nearest of the top class. Then `_clear_tile` does the work. ~35 lines, one engine sweep per body per round, well inside the 8 ms budget (`CPU_BUDGET_US = 8000`, `sk_maps.py:2430`).

**Priority — recommended order, with the reasoning:**
`LAUNCHER (30 HP)` > `SENTINEL (40)` > `GUNNER (25)` > `barrier-on-a-delivery-seat (30)` > `conveyor/splitter (20)` > `plain barrier (30)`.
The launcher goes first not by HP but because it is *"a 30 HP BUILDING that cannot defend itself: 15 pecks, and its removal frees every seat it covers"* (`sk_maps.py:2178-2184`, `SK_PLUCK_RETARGET`, already shipped ON) — and because it is the only enemy structure that can move **our** bodies. This ordering does **not** map onto `SK_PRI_*`: `_target_pri` scores `SK_PRI_TURRET = 4` for all three armed types and `SK_PRI_BARRIER = 0`, and `_peck_priority` refuses anything `≤ SK_PRI_OTHER` (`:4406-4407`). **The demolition sweep therefore needs its own ordering, not `_target_pri`.** That is a feature — `_target_pri`'s barrier-0 exists because 1,280 of 1,712 pecks went into barriers under the *kill* currency (`sk_maps.py:66-72`), and the fortress is not paying that currency until r300.

### 3c. The cost arithmetic, and where a gun is cheaper
Builder peck: 2 Ti → 2 dmg. **Barrier 30 HP = 15 pecks = 30 Ti + 15 builder-turns. Conveyor 20 HP = 10 pecks = 20 Ti. Launcher 30 HP = 15 pecks. Sentinel 40 HP = 20 pecks.**
Gunner shot: 4 ammo (= 4 Ti, 1:1) → 7 dmg ⇒ **1.75 dmg/Ti**, fires 1 shot/2 rounds. Sentinel: 10 ammo → 18 dmg ⇒ **1.80 dmg/Ti**, 1 shot/3 rounds.
⇒ **Per titanium, turret fire is ~1.75× cheaper than pecking (1.75-1.80 vs 1.0 dmg/Ti) — and it costs ZERO builder-turns.** A 30 HP barrier is 30 Ti of pecks and 15 turns, or ~17 Ti of gunner ammo and 8 rounds of a turret that was doing nothing else.
⛔ **But the counter-evidence is measured and it is severe.** `SK_GUN_ROUTEBLOCK` (`sk_maps.py:1881-1896`, `main.py:67-77`) put exactly this reasoning into the tree and read: *"control core 1,452 shots / barrier 0; PLANK 3 core 924 / barrier 1,353 — 1,353 shots into collar barriers bought 528 FEWER shots into their CORE — 3,696 HP, i.e. SEVEN AND A HALF ENEMY CORES' WORTH."* **And most of it was the rotation**: rotate-off read 13 kills / by-r300 11 instead of 7/6.
⇒ **The opportunity cost was denominated entirely in shots-not-fired-at-their-core — a currency the fortress phase does not spend.** Under the r300 ruling, from r0 to r300 there is no core to shoot at, so a home gun's alternative use is *idle*. **`SK_GUN_ROUTEBLOCK`'s refutation does not transfer to phase 1** — but it transfers *completely* to phase 2, so the flag must be **phase-gated OFF at r300**, not simply flipped on. That asymmetry should be written into the flag comment.

---

## 4. ECO TO THE ABSOLUTE EDGE

### 4a. What the planner covers
`_plan_belt` (`sk_roles.py:1655-1753`) is **one global plan**, not per-harvester (`:1656-1665`, the #78 fix: *"per-harvester planning is why our harvester→core connectivity reads 58.8% against their 83%"*). `_belt_parents` (`:1782-1856`) is a single-source BFS seeded from **all 8 tiles orthogonally adjacent to the 2×2 footprint** (`:1814-1826`), first pass avoiding ore, relaxed only if a harvester would otherwise be unreachable (`:1720-1727`); each chain terminates by facing a footprint tile (`:1745-1748`).
`_harvester_action` (`:1473-1506`) builds on any cardinal-adjacent ore that is `is_home_half`, not belt-planned, not `_harv_blocked`, arbiter-clean. **There is no harvester-count cap anywhere in the tree** (grepped `SK_HARV_CAP`/`SK_MAX_HARV`/`MAX_HARVEST`: zero hits). **Splitters are never built** — `build_splitter` has zero call sites; `BELT_TYPES` is recognition-only.

### 4b. The measured ceiling, and what stands between us and it

Home-half ore, decoded from the tree's own `MAP_CODES`/`EXTRA_MAP_CODES`/`CORE_PAIRS` (`sk_maps.py:3311-3402`) with `is_home_half`/`dsq_core` reimplemented verbatim, plus a faithful replay of the `_belt_parents` BFS:

| map | dims | ore total | **home-half ore N** | conveyor tiles M for full build-out | unreachable |
|---|---|---|---|---|---|
| auroraveil | 20×20 | 16 | **8** | 42 | 0 |
| icefloe | 20×20 | 20 | **10** | 48 | 0 |
| frostgate | 20×20 | 20 | **10** | 17 | 0 |
| holmgang *(12×12 key, name inferred — no named entry in `EXTRA_MAP_CODES`)* | 12×12 | 6 | **3** | 8 | 0 |

Harvester = 1 stack (10 Ti) per 4 rounds = **2.5 Ti/round delivered**; passive = 10 per 4 rounds = **2.5 Ti/round**.

| map | **eco ceiling, Ti/round** | over r120→r1000 |
|---|---|---|
| auroraveil | 8×2.5 + 2.5 = **22.5** | ~19,800 Ti |
| icefloe / frostgate | 10×2.5 + 2.5 = **27.5** | ~24,200 Ti |
| holmgang | 3×2.5 + 2.5 = **10.0** | ~8,800 Ti |

**Lane capacity is NOT the binding constraint, and this is measured, not assumed.** `docs/research/binding-tile-cut-2026-08-10.md` (8,519 archived replays, 0 decode errors): a conveyor pushes **≤1 stack/round, 0 exceptions in 40,363,446 pushes** (§6a); the core's 8 external faces therefore admit **8 stacks/round = 80 Ti/round, a measured denominator** (§6c). At 4 harvesters/lane a lane saturates exactly (4 × 0.25 = 1 stack/round); icefloe's 10 harvesters over the BFS's multiple first-hops sit well under. Confirmed empirically: our saturation class is **14.3% pooled but 0.1% at our median team-side** (§4) — *"our lines are not saturated... We are breakage-bound"*.

**What actually stands between current behaviour and the ceiling, in measured order:**
1. **Single-body staffing.** `_home_keeper` is the **only** caller of `_harvester_action` and `_belt_action` (one call site each, tree-wide). One body, one action per round, act-and-move mutually exclusive.
2. **The keeper's own priority ladder.** Fourteen rungs run **above** `_harvester_action` (`sk_roles.py:1288-1342`): counter-battery, medic, door, peck, seat-heal, heal, seat-clear, apron, launcher, route-gap. Every one consumes the turn on fire.
3. **Line breakage, not capacity** — 68.6% of our lost harvester emission sits behind a conveyor pointing at something that cannot receive (`binding-tile-cut` §0). The prescription the study derived — *"terminated lines, and a builder that repairs them"* — is `SK_TERMINATE` (shipped ON, `sk_maps.py:1459`) and `_belt_watch`; the fortress's second body is what makes the repair *fast*.
4. **`SK_BELT_BAND_DROP`** (`sk_maps.py:590-612`, logic `:1707-1719`) drops a harvester seat outright rather than route it through the enemy sentinel band — a real working ore tile the bot refuses to deliver from.
5. **Harvester bans**: `SK_HARV_REBUILD_ESCALATE = 2` deaths → `SK_HARV_BAN_ROUNDS = 60` (`sk_maps.py:2521-2530`).

⚠ **Nobody has a current Ti-delivered-per-round number for this tree.** The two figures in circulation carry different subjects and must not be pooled: `10,500 Ti/game = 1.05 stacks/round` (`binding-tile-cut` §6c, 579 **ladder r1000** team-sides, 2026-08-10 era) and `483 → 550 Ti/game` (`main.py:80`, 30-game **local F1 screen**, v618 era, games ending at median r201). **The fortress's first instrument must be a delivery-per-round tape on the current tree.** Without it "the absolute edge" has no baseline.

### 4c. Scale at full build-out

`scale = 1.0 + 0.20·(builder bots) + 0.05·N + 0.01·M`; four builder bots = **+0.80 before anything is built**. `cost = floor(scale × base)`.

| map | N | M | **scale** | gunner (20) | sentinel (30) | barrier (3) | conveyor (3) | harvester (20) |
|---|---|---|---|---|---|---|---|---|
| auroraveil | 8 | 42 | **2.62** | 52 | **78** | 7 | 7 | 52 |
| icefloe | 10 | 48 | **2.78** | 55 | **83** | 8 | 8 | 55 |
| frostgate | 10 | 17 | **2.47** | 49 | **74** | 7 | 7 | 49 |
| holmgang | 3 | 8 | **2.03** | 40 | **60** | 6 | 6 | 40 |

Marginal read: **one harvester costs +1.5 Ti on every later sentinel and earns 2.5 Ti/round.** One conveyor costs +0.3 Ti on a later sentinel. `SK_RENT` (`sk_maps.py:3014`, ON) exists precisely because *"scale is a rent, not a purchase"* — destroying a building refunds its contribution — and `_rent_sweep` (`:5729`) already sweeps orphan belt ≥25 rounds off-plan, capped 2 destroys/body/turn.

### 4d. Where the Bean-counters core-apron mesh fits
Magnus's field observation (`docs/coordination.md:73437`, ae8dd8c2 game 3, r8): their 10 conveyors against the ~4 their two harvesters need — the extras wall the core's exposed face, and tiles (4,8)/(4,9) are *"exactly the point-blank plant ring, i.e. they deny to others the point-blank gunner plant that is their OWN signature move."* Triple duty on paying infrastructure: belt-cut redundancy, plant-tile denial, fire occlusion — at +1% each rather than barrier deadweight.

**It fits in exactly one place, and half of it is already built and shipped OFF.** `SK_APRON_BELT_PREF` (`sk_maps.py:2029`, `_belt_parents:1791-1801`) re-orders each BFS level so apron tiles become the preferred parent at equal depth — *"the belt routes THROUGH the apron rather than around it... and this half pays for it with a conveyor the plan was going to buy anyway... a TIE-BREAK AND NOTHING MORE: the frontier is a level set, so re-ordering inside it cannot make any chain longer."* That is the mesh's *routing* half at literally zero marginal cost. What is missing is the *redundancy* half: a second, parallel trunk to a different core face, which today's shortest-path BFS will never produce because it emits a tree.

Sketch: `SK_APRON_MESH` — after `_plan_belt` completes, for each **unoccupied** apron tile that is (a) cardinal-adjacent to an already-planned belt tile and (b) facing a core footprint tile, add it to `belt_plan` as a terminal conveyor. Cost `floor(scale×3)` ≈ 7-8 Ti each, +1% each. On a 20×20 that is ~6-10 extra tiles: ~60 Ti and +0.08 scale (≈ +2 Ti on a later sentinel), buying plant-tile denial on the apron ring where **28 of the 48 enemy turrets that ever damaged our core stood** (`sk_roles.py:2855-2856`). ⛔ Interaction to check: it competes with `_seat_claim_action` and `_apron_action` for the same tiles via `tile_owner`/`may_build`, and it raises `_belt_watch`'s repair surface.

---

## 5. HOME TURRET RING

### 5a. What exists
- **`SK_HOME_GUNNER = False`** (`sk_maps.py:1828-1880`) — one home gunner, window r10-120, `SK_HOME_GUN_MAX = 1`, reserve 40, own cap. Full machinery: `_home_gun_window/_score/_action/_walk` (`:2511-2686`), with self-trap guard (two free neighbours), never on a delivery seat, never on the enemy sentinel axis, arbiter-checked.
- **`SK_COUNTER_SENT = False`** (`sk_maps.py:1255-1299`) — one home sentinel sited **off** the enemy sentinel's firing axis (`_on_armed_axis:1112`, keyed on tile-persistent `armed_facing` because a sentinel's facing never changes): 3 shots × 18 = 54 kills a 40 HP sentinel **that physically cannot answer**. Shipped off as an exact null — but the *reason* is a trigger collision, not a mechanism failure: it needs 20 rounds of unbroken corefire alarm and the cheap rung (`SK_COUNTER_PECK`) breaks the streak at median 11 (`sk_maps.py:1261-1269`, *"the two planks are ANTAGONISTIC by construction"*).
- **`SK_BELT_COVER = True`**, `_cover_gun_action` (`:3704`) — ray-not-disc siting to cover the belt trunk; spends the same `SK_DOOR_GUN_CAP = 2` budget as `_door_action`.
- **`_turret` (`:6875-7015`)** — the firing turn. Ammo guard is mandatory, not stylistic (`:6878-6883`: `can_fire` returns True at 0 ammo and the engine **raises** inside `finish_firing_turret`, which permanently destroys our own turret). Reads both `get_tile_building_id` **and `get_tile_builder_bot_id`** (`:6919-6920`) ⇒ **turrets are the only shipped verb that reaches an intruding body.**
- **`SK_HOME_LAUNCHER = False`** (`sk_maps.py:1556-1710`) — full machinery, 0 ammo, engine-bound pickup d²≤2 / throw 1≤d²≤26, `SK_HL_TEAM_CHECK = True`, never drops a victim inside our own ring (`SK_HL_DROP_RING_DSQ = 13`).
- Drip: `_drip` (`sk_core.py:266-325`), need-based — `need = 4·(gunners that will fire next round) + 10·(sentinels) + forward tubes + SK_AMMO_FLOOR(10)`, floored onto the 4/10 lattice, ~67 conversions/game, peak balance ~26, **never banks**. `SK_AMMO_FLOOR` swept to 20/30 is monotonically **worse** (`sk_maps.py:2442-2461`).

### 5b. ⛔ A TURRET RING CANNOT BLANKET CHEBYSHEV-3. IT COVERS LANES.
Chebyshev-3 around a 2×2 is an 8×8 box minus the footprint = **60 tiles**. A gunner's shot is a **straight line** along its facing (`get_gunner_target` returns *"nearest targetable tile in a gunner's facing line"*), r²=13 ≈ 3.6 tiles, **obstacle-blocked** — ~3-4 tiles covered. A sentinel is a **single-tile-wide line**, r²=32 ≈ 5.6 tiles, **ignores obstacles**, and **cannot rotate** (`_rotate_toward:7166`, gunner-only — *"COPY 2 seen from our own side"*). Blanketing 60 tiles by rays needs ~12-15 turrets, at +20% scale each. **That is not the design.**

**Recommended ring, and it is three turrets:**
1. **One SENTINEL on the core→enemy-core axis**, sited so its ray runs down the lane every intruder walks (`_home_gun_score:2547-2551` already computes exactly that tie-break). Ignores obstacles, so our own apron mesh does not block it. 18 dmg, 1 shot/3 rounds, reaches beyond Chebyshev-3. This is the highest-value single ring turret because it is fixed *and the approach direction is fixed*.
2. **Two GUNNERS on the flanks**, rotating. `SK_HOME_GUN_ROTATE = True` with `SK_HOME_GUN_ROT_CAP = 6`/game — and the direction of the evidence matters: **rotating toward a LIVE THREAT helps** (rotate-off read 8 kills instead of 12, `main.py:84-86`), while rotating at a **barrier** is the defect (`SK_GUN_ROUTEBLOCK`, §3c). *"Rotation is not the defect; rotating at a BARRIER is."*

**Cost at icefloe scale 2.78:** sentinel 83 + gunner 55 + gunner (scale now 3.18) 63 = **201 Ti**, plus +0.60 scale ⇒ every later sentinel +18 Ti. Rotation budget 2×6×10 = 120 Ti.

### 5c. Ammo economics per intruder
| weapon | dmg/shot | rounds/shot | shots for a 40 HP builder | **ammo-Ti per intruder** | rounds to kill |
|---|---|---|---|---|---|
| gunner | 7 | 2 | 6 | **24** | 12 |
| sentinel | 18 | 3 | 3 | **30** | 9 |
| launcher | — | 1 (cooldown +1) | — | **0** | 1 (displaces, does not kill) |
| builder peck | — | — | — | **engine-barred (§0.1)** | ∞ |

At the CITADEL_BAR's own terms, killing every intruder costs **24-30 Ti of ammo each**. Against an icefloe income of 27.5 Ti/round, even 10 intruders a game is ~300 Ti — **~11 rounds of income.** Magnus's *"spend everything we need"* is not a stretch; it is a rounding error. **The drip needs no change** — it is need-based off `_threat_scan`'s "will fire next round" predicate (`sk_core.py:89-93`), which already counts a home turret with any hostile inside its own reach.

⭐ **The repricing that makes all of this shippable:** `SK_HOME_GUNNER`'s entire measured cost was **by-r300 kills 12→5, median kill 201→315** (`main.py:79-82`) — *"a +20% scale surcharge landing BEFORE the kill machinery is funded."* Under the r300 ruling **there is no kill machinery to fund before r300**, and the surcharge's only surviving effect is +6 Ti on each r300 sentinel. Its advertised gains (enemy builder deaths 63→88, income 483→550) are **exactly the fortress's own currency.** ⇒ **`SK_HOME_GUNNER` is the cheapest, best-evidenced citadel plank on the board, and its refutation is denominated in a currency Magnus has suspended.** Same argument, same shape, for `SK_HOME_LAUNCHER` (shipped off because it *"converts losses into r1000 stalls"*, `sk_maps.py:1572-1576` — the exact outcome the fortress phase is no longer penalised for).

---

## 6. WHAT DIES — and the distinction the r300 ruling introduces

**The ruling splits this list in two, and the builder must keep the halves apart or the phase-2 revival will be a rewrite.**

### 6a. DEAD PERMANENTLY under FORTRESS_NO_RAID (never revive)
The **enemy-ring cage** and **forward ore denial** — these are raid verbs in both phases (the r300 siege is a sentinel battery, not a cage):
`SK_CAGE`, `SK_CAGE_FIRST`, `SK_CAGE_CEIL`, `SK_CAGE_ACCEPT`/`_MIN`, `SK_CAGE_MELEE_GIVEUP`, `SK_LAP_ADJ_SEAL`, `SK_EVICT_ARMED`, `SK_ONE_CURSOR`, `SK_CURSOR_GIVEUP`, `SK_COLLAR_GUNS`, `SK_COLLAR_PECK_CAP`, `SK_COLLAR_ROUTE_GATE`, `SK_STALL_*` (V9's lap-quadrant flip) · methods `cage_lap`, `_cage_survey`, `_cage_report`, `_seal_tile`, `_seal_adjacent`, `_evict_seal`, `_lap_free`, `_cage_cursor_move`, `_cursor_*`, `_peck_out` · `SK_ORE_DENY` + `_deny_barrier`'s pre-empt half (`:5252`) + `_deny_target`'s forward patrol (`:5329`) + `_melee_harvester` as staffed.

### 6b. PHASE-DEFERRED to r300 (must be round-gated, NOT deleted, NOT flipped off)
The entire forward-tube family is **exactly what phase 2 needs**:
`SK_NEST`, `SK_NEST_PAIR`, `SK_NEST_PAIR_MIN_GAP`, `SK_NEST_DSQ_MIN/MAX`, `SK_NEST_POINT_BLANK`, `SK_NEST_EXHAUST_PB`, `SK_NEST_PB_LIFE`, `SK_NEST_N3`, `SK_NEST_PREP_BARRIERS`, `SK_NEST_CLEAR`(+`_OWN`,`_GIVEUP`), `SK_NEST_STUCK_*`, `SK_NEST_EXIT`, `SK_DEATH_MEMO_ROUNDS` · `SK_TUBE_FLOOR`, `SK_TUBE_FLOOR2`(+`_N`,`_GRACE`,`_PREPREP`,`_STAGE`), `SK_TUBE_NOPREP`, `SK_TUBE_FUND`, `SK_TUBE_GAP_RELAX`, `SK_GAP_RELAX_SOLO`, `SK_TUBE_LATENCY_SOLO`, `SK_TUBE_RELIGHT`, `SK_RELIGHT_*`, `SK_TEAM_TUBES` + slot 7 · `SK_S2_*` · `SK_RENT_EARLY*`, `_rent_class` branch (b) · `SK_DISENGAGE` · `_attack_enemy_core` + `SK_CORE_PECK_HEALGUARD` · `_relight_close`.

### 6c. RE-PRICED, not dead (their refutation's currency is suspended in phase 1)
`SK_HOME_GUNNER` · `SK_HOME_LAUNCHER` + all `SK_HL_*` · `SK_SEAT_CLAIM` (measured possession 0.136→0.438 — a *fortress win* that failed the kill clock) · `SK_SEAT_CLEAR` · `SK_SEAT_HEAL` · `SK_GUN_ROUTEBLOCK` (**phase 1 only** — its refutation transfers completely to phase 2, so it must gate OFF at r300) · `SK_COUNTER_SENT` · every cap in §0.2.

### 6d. Stays live and correct, do not touch
`SK_BELT`, `SK_TERMINATE`/`SK_TERM_FIRST`/`SK_TERM_MOVE`, `SK_BELT_EST*`, `SK_BELT_COVER`, `SK_HARV_ESCALATE`, `SK_TARGET_PRIO`, `SK_DANGER_NAV`/`_COST`/`_K`, `SK_CYCLE_*`, `SK_SENSE_NAV`, `SK_ORE_SENSE`, `SK_IDLE_ACT`, `SK_SPAWN_EXIT`, `SK_APRON_DENY`, `SK_DRIP`, `SK_DOOR`, `SK_PECK_FOCUS`, `SK_PLUCK_AWARE`, `SK_RENT`, `SK_MARCH_TEAMCHECK`, `SK_HOMEDEF_TEAMCHECK`.
`SK_BELT_BAND_AVOID`/`_DROP` stay ON (they keep our belt out of *their* guns) but become largely inert once no body goes forward — **and they must be re-checked at r300**, when a raider re-enters that band.
`SK_SLOT_KILLER` (slot 14) is **harvester-killer attribution**, not `KILL_TARGET` — keep it.
`PROGRAMME.md`'s `KILL_TARGET: median_r180_share_by_r200_floor_r300` is now settled by the ruling: **dormant before r300, and its r180/r200 terms are dead constants** — the siege cannot start before r300. Flag to Magnus for a field edit rather than leaving a stale constant a successor trips on.

---

## 7. RISKS — how this design fails the ways this tree has already failed

**R1 — E6, and it is the closest precedent by a distance.** v630's tube guard: *every mechanism column moved as designed and the currency went the other way*, measured **twice in one day** with the opening invariant held (`BUILD-REPORT-v630tubeguard-2026-08-22.md:122-143`; E6 by-r300 −7, our-core-deaths +6). The attribution refuted the flattering hypothesis and found the real one: **the HOME KEEPER relocated forward and stopped healing the core — core-footprint heals 398→80, our core died in 21 ON cells vs 16 CTRL.** The fortress's citadel responder is *the same shape*: a new duty that pulls the keeper off the core. ⇒ **The registered co-diagnostic on every citadel screen must be `core-footprint heals/game` and `our-core-deaths`, not just intruder survival.** Related and already a queue row: `#128(a) LEASH` — the keeper economy walk is fenced by `is_home_half` **only**, no d² term (`sk_roles.py:3997`).

**R2 — the scale-surcharge death (`SK_HOME_GUNNER`, `SK_HOME_LAUNCHER`, v615/v616).** Three separate planks died to *"a +20% scale surcharge landing BEFORE the kill machinery is funded"* (`main.py:82-83`). Under the r300 ruling this is genuinely repriced (§5c) — **but only if the eco is actually built.** If the fortress buys turrets early and the belt build-out is slow, we pay the surcharge *and* get no income, which is the same death in a new hat. ⇒ **Gate every turret purchase on a delivered-Ti-per-round floor, not on a round number.**

**R3 — mechanism-confirmed / currency-negative, twice more.** `SK_SEAT_CLAIM`: possession 0.136→0.438, theirs −17.3pp, ~38 enemy builder-turns/game committed to our door — **and by-r300 12→8.** `SK_SEAT_HEAL`: a real dose (48 heal events, heals/game 0.8→1.3) and a **measured exact zero** on every column, shipped off partly because *"its own DOORWAVE guard has NEVER produced its other verdict on the engine"*. ⇒ **Every fortress guard must be driven to both verdicts on the engine before its plank is scored** (repo standing rule; the seat-heal instance is what it was written for).

**R4 — the v629 pattern: three zero-scale-cost defence planks composed to a negative centre** (`SK_REAIM_CAP_LIVE` + `SK_DOOR_REAIM` + `SK_ARMED_SWEEP`, `bots/_v629reaim/sk_maps.py:1878-1899`), with the minus-one decomposition admitted as `QUEUE.md:946` #125 under a **binding precondition**. ⇒ **Never compose three fortress planks into one arm.** The fortress is naturally a package and that is exactly the trap; `main.py:102-104` names the signature: *"THE PACKAGE MOVES 12 OF THE 12 NAMED F1 CELLS. A targeted fix moves few cells."*

**R5 — the silent lost-update class.** Two bodies in `_home_keeper` (§1a) or two bodies in `_siege_engineer` (§8a) both write slots that assume one writer. Measured precedent: a seat beat **frozen at round 80 for 291 rounds**, the fixed bit reading 0.6% against ground truth 33.7% — *"a producer that looked plausible and was inert"* (`sk_maps.py:2265-2290`). ⇒ Static-battery assertion, not a comment.

**R6 — terminal-idle states.** `SK_IDLE_ACT` is wired into the cage walker and the engineer **only** (`sk_roles.py:4691`, `:5610`); Magnus's own review marker M3 was *"why did this builder stand still for 25 rounds?"* (`docs/coordination.md:73441`). Under §0.1 the citadel responder's default action against a body **is standing still**, which is exactly this class wearing a doctrine's uniform. ⇒ `SK_IDLE_ACT` must be extended to all four roles as part of plank 1, and "body-block" must be scored as a *measured* effect (intruder displacement / intruder actions denied), never assumed.

**Earliest screen that catches all six:** the existing local F1/F2 fixture (`_v542wave` NOISE_OFF copy, 30 games, seed pinned, map/seat varying, bit-deterministic — which is why identity controls come out byte-exact). Registered cells: `core-footprint heals/game` · `our-core-deaths` · `Ti delivered/round` · `eco-body-rounds/game` · `intruder survival rounds` · `enemy-structure dwell rounds in our half` · `r1000 share (reported honestly)`. ⚠ Powered reads: the F1/F2 same-bot swing at n=900 is **2.22pp** (`main.py:45-56`), finer than several bars people will want to write — and per the enumeration rule a multi-map grid carries a MAP cluster (DEFF 4.57) and a CONTENT-DUPLICATE control.

---

## 8. SIEGE PHASE — the r300 flip

### 8a. The phase-flip mechanism
Cleanest form, one insertion, exact OFF-identity by conjunction:
```python
# sk_maps.py
SK_PHASE        = False
SK_PHASE_ROUND  = 300
SK_PHASE_RAIDERS = (SK_CAGE_WALKER, SK_SIEGE_ENGINEER)
```
```python
# sk_roles.py _builder, replacing the dispatch at :319-326
role = self.role
if SK_PHASE and rnd >= SK_PHASE_ROUND and role in SK_PHASE_RAIDERS:
    role = SK_SIEGE_ENGINEER
if role == SK_CAGE_WALKER:   ...
```
With `SK_PHASE = False`, `role` is `self.role` unconditionally — byte-identical dispatch.

**Which two convert, and why:** `CAGE_WALKER(1)` and `SIEGE_ENGINEER(3)`. The engineer *is* the siege body already; the walker is the role with no fortress duty worth keeping past r300 (its fortress job is second-eco, and by r300 the belt is built and static). `HOME_KEEPER(0)` and `ORE_DENIER(2)` stay: the keeper carries the whole belt alone, which it does today by construction, and the denier holds the citadel — **the fortress does not stand down at r300, it loses two bodies.** The citadel's staffing rule (§2c) must therefore drop from `SK_CITADEL_BODIES = 2` to 1 at the flip, or the keeper gets pulled off the belt every time a raider appears with no second body to relieve it.

**Five hazards, all nameable now:**
1. **⛔ Slot-7 writer collision.** `SK_TUBE_ENG_SLOT7 = True` puts *the engineer* on phase 2 of a 3-phase writer schedule (`sk_maps.py:3292-3301`), and the schedule assumes **one** engineer. Two engineer bodies both write on `rnd % 3 == 2` ⇒ R5 exactly. **Two fixes, both already in the tree:** (a) gate `_nest_publish` on the body's **original** `self.role == SK_SIEGE_ENGINEER`; or (b) **flip `SK_NEST_N3 = True`**, which sets `SK_TUBE_ENG_SLOT7 = False` and *removes the engineer from slot 7 altogether* — three writers, three phases, one per round, rule met in its strongest form. (b) is preferable: it also raises the tube target to 3, which is what "as many as necessary" wants. Its own refutation is **−1.22pp game share [−4.36, +1.92]** at n=1800/side (`sk_maps.py:2787-2800`) — CI includes zero, and it was priced under the *early-tube* clock, not a r300 battery.
2. **Site collision.** `_nest_taken()` is a **per-body** ledger, so the two raiders' `SK_NEST_PAIR_MIN_GAP = 8` spread check only sees their own tubes. `SK_TUBE_FLOOR2 = True` makes `live` a team fact (`_floor_live:454-496`) but caps `want` at `SK_TUBE_FLOOR2_N = 2`. Simplest: give each raider a band **half** by role parity (`self.role_parity`, already set at `_claim_role:348`) — the scan loop at `:6075-6076` sweeps `dx,dy ∈ [-7,9)` and can be split without touching any filter.
3. **Travel.** The engineer already crosses the whole board from r0 today, so `step_to`/`_bfs_direction`/`SK_DANGER_NAV`/`SK_DANGER_COST` are proven for this. **But at r300 the board is dense with buildings**, so nav-lock risk is higher; `SK_CYCLE_ALL_ROLES`/`SK_CYCLE_K` are already ON for non-walker roles (`:289-290`), and `SK_IDLE_ACT_ENGINEER` is already ON.
4. **`SK_BELT_BAND_AVOID`/`_DROP`** were inert during phase 1 and re-engage at r300 in the *belt* planner only — harmless, but the keeper re-plans on a changed `self.enemy` key (`:1672`) and should not re-route a working belt at r300. Worth an explicit `rnd < SK_PHASE_ROUND` guard on band re-planning.
5. **`SK_GUN_ROUTEBLOCK`, if flipped on for phase 1 (§3c), must gate OFF at r300** — its 3,696-HP opportunity cost is real the moment a core becomes shootable.

### 8b. The two-raider sentinel siege

**Siting — the band is reusable AS-IS, and this is the one place where nothing needs re-centering.** `SK_NEST_DSQ_MIN = 14` / `SK_NEST_DSQ_MAX = 32` (`sk_maps.py:2489-2490`) is queue row **#41**'s insight already shipped: *"a sentinel at d²14-32 outranges the reactive counter-gunner (r²=13, obstacle-blocked) BY CONSTRUCTION"*, worth a measured **+30% of turret life**. `_prep_barrier` (`:6249`) is #41's second half — *"a 3-Ti barrier on the next-door tile forces their measured +3..+29-round rebuild latency instead of the d²=1 insta-counter."* The fortress phase never uses any of it, so it arrives at r300 unmodified and untested-against-nothing.
⚠ **#41's own s52 addendum is the live risk:** two opponents now ship an **r11 home sentinel guard**, and our forward-build median life fell **14.5 → 8 rounds** there; team lazy kills 62% of our forward turrets at median life 15. `_nest_scan` has no enemy-guard-coverage input.

**Funding — not binding, by an order of magnitude.** At icefloe scale 2.78, sentinels escalate +20% each (`floor(scale×30)`): 83, 89, 95, 101, 107, 113 ⇒ **six = 588 Ti**; twenty = ~2,800 Ti. Bank at r300 with the belt running from ~r120 is thousands of Ti. Prep barriers ≈ 8 Ti each, 2/site.
**Ammo is the real recurring cost and it has a clean rate:** 10 ammo/shot ÷ 3 rounds/shot = **3.33 Ti/round per firing sentinel**. Income 27.5 Ti/round ⇒ **~8 concurrently-firing sentinels sustainable indefinitely.** (Ammo is 1:1 and does **not** scale — a rare cost in this game that inflation does not touch.)

**Battery arithmetic against a healed core.** Their core is 500 HP and the measured heal-tax on an enemy core in this tree is **0.68 of everything we deal** (`sk_roles.py:5144-5147`, v602 autopsy: 95 enemy heals against 82 of our pecks over 41 rounds). Sentinel gross = 18/3 = 6 HP/round each.

| concurrent sentinels | gross HP/rnd | net at 0.68 heal-tax | rounds to 500 HP | ammo Ti/rnd |
|---|---|---|---|---|
| 2 | 12 | 3.8 | **130** | 6.7 |
| 3 | 18 | 5.8 | 87 | 10 |
| 4 | 24 | 7.7 | **65** | 13.3 |
| 6 | 36 | 11.5 | **44** | 20 |
| 8 | 48 | 15.4 | 33 | 26.7 |

⇒ **Two sentinels is not a battery; it is a stalemate.** *"as many sentinels as necessary"* is the correct instruction and the number is **4-6 concurrent**. Note "two raiders" and "two sentinels" are different quantities — the raiders are the *delivery* bodies.

**⛔ THE BINDING CONSTRAINT IS TUBE LIFETIME AND PLANT RATE, NOT FUNDING AND NOT SCALE.** At the measured forward-turret life of **10 rounds** (#41 baseline; **8** against a home-guard opponent), a sentinel fires ~3 shots and delivers 54 HP gross / ~17 net before it dies. Sustaining 6 concurrent tubes at a 10-round life needs **0.6 plants/round**; two builder bodies, each able to build once per round and needing to walk and lay prep barriers, realistically deliver **~0.3-0.4 plants/round** ⇒ steady state **3-4 concurrent tubes** ⇒ **65-87 rounds** to break a healed core. Against ~700 available rounds that is a comfortable margin — **the siege closes on the clock.** The margin evaporates only if tube life falls below ~6 rounds or the raiders die in transit.
**Levers, in leverage order:** (1) prep barriers / #41 siting — the +30% life the band already buys; (2) more raider bodies (the 4-body cap is `SK_N_ROLES`, a constant, and `MAX_TEAM_UNITS = 50` is nowhere near binding — an extra builder is +20% scale = **+6 Ti per sentinel**, trivial at r300); (3) `SK_NEST_N3` / a raised `want`; (4) the v630 tube-guard mechanisms, which **worked** — F2 tube removal rate 0.466→0.333, horizon survival +0.062, first-ever tube-tile heals (`BUILD-REPORT-v630tubeguard-2026-08-22.md` §addendum). **Its refutation was the keeper drifting forward and abandoning core heals — a cost mechanism that does not exist for a deliberate late siege by two dedicated bodies with the keeper explicitly staying home.** ⇒ **v630's held decomposition (bias-only vs heal-only) is a phase-2 asset, and its E6 objection does not transfer.** That is worth telling Magnus.

### 8c. Scale interaction — does the fortress price the siege out?

**No. Measured margin ~7 rounds of income against a 700-round window.**

| | scale | sentinel | 6-sentinel battery |
|---|---|---|---|
| 4 bodies only, no eco | 1.80 | 54 | 54+59+65+70+76+81 = **405 Ti** |
| 4 bodies + full icefloe eco (N=10, M=48) | **2.78** | **83** | 83+89+95+101+107+113 = **588 Ti** |
| **eco surcharge on the battery** | +0.98 | +29 | **+183 Ti** |

**183 Ti ÷ 27.5 Ti/round = 6.7 rounds of the income the eco bought.** The eco pays for its own surcharge before the seventh round of its existence. Marginally: **one harvester adds +1.5 Ti to every later sentinel and earns 2.5 Ti/round.** And ammo — the recurring half — is scale-immune.
Two riders worth stating:
- **A pre-siege scale-deflation sweep is available and already built.** `SK_RENT` (`sk_maps.py:3014`, ON) refunds a destroyed building's scale contribution. At r300, sweeping ~40 surplus barriers (citadel wall, apron mesh) is −0.40 scale ⇒ sentinel 83→71, **saving ~72 Ti across a six-tube battery**, at the cost of the wall the fortress just spent 300 rounds building. Named for completeness; **not recommended** — the wall is what keeps the two remaining home bodies alive while the raiders are away.
- **The scale surcharge is paid once, on purchases; the eco pays every round.** The *ordering* Magnus specified (eco first, siege second) is the one that pays the surcharge in full — and it is still the right order by ~100×.

**⭐ THE REAL BINDING CONSTRAINT ON THE WHOLE TWO-PHASE DESIGN IS SURVIVING TO r300.** Our core dies in **46.3% of all games at median r187** (`CLAUDE.md`, PLAY_DEFENCE scope clause), and the fortress hands the opponent **300 uncontested rounds**. A siege that is fully funded and geometrically sound is worth nothing in the 46% of games that end before it starts. ⇒ **The primary metric of the entire fortress phase is `P(our core alive at r300)`, and it should be the headline cell of every screen in the decomposition below.** Baseline to beat, on the current tree, is unmeasured — that is plank 0.

---

## 9. RECOMMENDED PLANK DECOMPOSITION *(the agent's recommendation; the builder decides)*

Ordered so each plank is independently screenable, each has an exact OFF-identity, and no plank composes with the next (R4). Fortress planks first, per the directive.

| # | plank | change | OFF-identity strategy | mechanism metric | registered co-diagnostic |
|---|---|---|---|---|---|
| **0** | **BASELINE TAPE + THE ENGINE PROBE** | No bot change. (a) Instrument the current F1/F2 tape for `P(core alive at r300)`, `Ti delivered/round`, `harvesters standing`, `intruders entering Chebyshev-3 / their survival`, `enemy structures standing in our half`. (b) **Re-probe `can_fire` on an adjacent enemy builder bot** (§0.1) — 10 min, decides whether FORTRESS_RESPONSE names a verb the engine has. | trivially exact | — | — |
| **1** | **CITADEL DISPATCH (all roles read slot 2)** | `SK_CITADEL` + `_citadel_answer`; static role priority (keeper+denier+walker); `SK_IDLE_ACT` extended to all four roles (R6). No new sensor, no purchase, **zero scale cost.** | call-site conjunction in `_builder`; branch unreachable when OFF | intruder survival rounds inside Chebyshev-3; intruder actions denied | **core-footprint heals/game, our-core-deaths** (R1); eco-body-rounds/game |
| **2** | **DEMOLITION SWEEP** | `SK_DEMOLISH` + `_demolish_target` enumerator feeding the existing `_clear_tile`. Own priority ordering (launcher > sentinel > gunner > seat-barrier > belt > barrier), `_seat_charge`-style per-(tile,occupant) cap. | `if SK_DEMOLISH and self._demolish_target(...)` | enemy-structure **dwell rounds** in our half; structures destroyed/game | Ti spent on pecks; eco-body-rounds/game |
| **3** | **HOME TURRET RING** | `SK_HOME_GUNNER` ON with `SK_FORT_RING_MAX = 3` and one axis sentinel; reuse `_home_gun_*`. **The single best-evidenced plank** — its refutation is denominated in a suspended currency (§5c). | existing flag; new cap behind `SK_FORTRESS` | intruder **deaths** (the CITADEL_BAR itself); ammo Ti/intruder | scale at r300; sentinel price at r300; `P(core alive at r300)` |
| **4** | **KEEPER LEASH** | `QUEUE.md:959` #128(a): add a d² term to the keeper's economy-walk fence (`sk_roles.py:3997`). Two lines. | new constant, `is_home_half and (not SK_LEASH or dsq<=K)` | keeper d² distribution from core | core-footprint heals/game; Ti delivered/round |
| **5** | **SECOND ECO BODY** | `SK_FORT_WALKER_ECO`: walker runs `_home_keeper`. **Requires the publisher gate** (§1a, R5) as part of the same plank — it is a correctness precondition, not a separate flag. | dispatch conjunction; publisher rungs gated on role 0 | **Ti delivered/round**, harvesters standing, belt-repair latency | slot-5/14 write-collision static assertion; scale at r300 |
| **6** | **CAP RE-OPENING** | Raise the §0.2 caps that were priced against one-body staffing: `SK_APRON_RELAY_CAP`, `SK_SEAT_PECK_*`, `SK_SEAT_CLAIM_WALK_DSQ`, `SK_DOOR_GUN_CAP`. **One cap per arm** (R4). | constants only; old values are the identity | apron relays/game; seat possession (baseline 0.136 us / 0.660 them) | eco-body-rounds/game |
| **7** | **CORE-APRON MESH** | `SK_APRON_BELT_PREF` ON (free, tie-break only) as arm A; `SK_APRON_MESH` redundant-terminal conveyors as arm B. Never together. | both are existing/new flags with exact-identity OFF | apron tiles occupied by us; enemy point-blank plants inside d²≤5 | scale delta; Ti delivered/round; belt-repair surface |
| **8** | **PHASE FLIP (skeleton, no siege changes)** | `SK_PHASE` + effective-role remap only. Ships the flip with `SK_NEST_*` **exactly as v628 has them**, so the arm measures the *flip*, not the siege. Includes the slot-7 fix (`SK_NEST_N3` or the publish gate) as a correctness precondition. | `role = self.role` when OFF | raider arrival round; tubes standing at r350/r400 | slot-7 beat freshness (the R5 detector); `P(core alive at r300)` |
| **9** | **SIEGE BATTERY SIZE** | Raise `want` past 2 for the post-r300 phase (`SK_NEST_N3`, or a phase-conditional `SK_TUBE_FLOOR2_N`). Band geometry untouched (§8b). | phase-conditional constant; pre-r300 identity is exact | concurrent tubes standing; **tube median life**; enemy-core HP slope | ammo Ti/round vs income; enemy heal-tax re-measured |
| **10** | **SIEGE SURVIVAL** | The held v630 tube-guard decomposition (bias-only vs heal-only), applied **only** post-r300 where its E6 cost mechanism cannot occur (§8b). | v630's `SK_TUBE_GUARD`, phase-gated | tube removal rate; horizon survival; tube-tile heals | keeper d² from core (must be flat — the E6 falsifier) |

**Sequencing note.** Planks 0-3 answer the CITADEL_BAR and are worth screening before anything else; 4-7 are the ECO half; 8-10 are phase 2 and are **blocked on plank 0's `P(core alive at r300)` baseline** — a siege designed against a fortress that dies at r187 is a siege designed for 54% of games. If that baseline is bad, the ordering should invert: survival first, throughput second.

**Two items for Magnus, not for the builder:**
1. **The engine bars builders from attacking enemy builder bots** (§0.1, pending the plank-0 re-probe). His FORTRESS_RESPONSE clause as written names a verb we do not have; the executable forms are turrets, the launcher taxi, and tile denial. He should choose, rather than have a lane choose for him.
2. **`KILL_TARGET`'s r180/r200 terms are now dead constants** under his r300 ruling (§6d) — a one-line `PROGRAMME.md` edit so no successor trips on them.