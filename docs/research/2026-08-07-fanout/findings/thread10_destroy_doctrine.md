# Thread 10 — DESTROY()/WALK-AWAY DOCTRINE (spec)

Read-only analysis, 2026-08-07. Target file: `bots/_v72e2/main.py` (LIVE "Eir 2",
`HANDOVER.md:26`), read end to end (2756 lines). No repo file edited, no platform
call, no `fcode run`.

Marking convention used throughout: **[PRIOR]** = re-cited measurement, **[NEW]** =
computed here from cited counts, **[ASSUMED]** = stated assumption, **[RESOLVED]** =
was open, now settled by an engine probe.

---

## 0. Citation audit — the established facts hold, with two corrections and one resolution

| Claim | Verdict | Citation |
| --- | --- | --- |
| `destroy()` free, unlimited/round, no cooldown, allied building, orthogonally adjacent | HOLDS | `docs/game-model.md:232-236`, `:223-225` |
| Returns in-transit resources on a destroyed conveyor to our balance | HOLDS | `docs/game-model.md:234-236` |
| Removes the entity's cost-scale contribution | HOLDS | `docs/game-model.md:235-236`, `docs/reference/official-docs.md:1424` |
| Cost scale is ONE team-wide multiplier | HOLDS, and is verified in-repo | `bots/cad_probe/main.py:749-751` ("there is one `get_scale_percent()`, and it is what every `get_*_cost()` multiplies"), with a measurement: three opening sentinels pushed the first harvester **20 Ti → 58 Ti** (`cad_probe:752-754`) |
| `destroy()` appears zero times in our bots | HOLDS | `grep -rn "ct\.destroy\|can_destroy" bots/*/main.py` → **one hit, and it is a comment**: `bots/_v70ec/main.py:182` "Nothing in this file calls ct.destroy()". Zero call sites in `_v72e2`, `_v73e3`, `_v70cm`, `_v71eir`, or any other bot. |

### CORRECTION 1 — scale tracks LIVE entities, not cumulative builds. **[NEW, HOT]**

`docs/game-model.md:357-358`: "Scale rises with how much your team has built… and it
**decreases again when an entity is destroyed**." `docs/reference/official-docs.md:1424`
says the same ("removed again on destruction").

So the widely-repeated phrasing "meander 201 conveyor builds = **+201%** conveyor scale
pricing every future build" (`docs/spitball.md:200-202`, `docs/v79-analysis.md:310-312`)
**overstates the standing scale**. 86 of those 201 died, so the standing conveyor
contribution at r1000 is **+115%**, not +201%. The +201% figure is a correct measure of
*titanium burned on churn*, not of the multiplier we are paying.

This matters both ways for the doctrine:

- It **shrinks** the pure "churn inflated our scale" story.
- It **creates** the doctrine's actual lever: because the scale is a live census,
  `destroy()` is the *only* way we can move it downward, and every point we shave is
  permanent for as long as the entity stays dead. Nothing else in the game gives us a
  downward hand on the multiplier.

### CORRECTION 2 — slot 9 is not the only reclaimable store slot. **[NEW]**

The brief says slot 9 is the only reclaimable one. `SLOT_LINKS_DONE = 9` is indeed
write-only (`_v72e2:2352`, `:2368` write; grep finds **zero** `read_store(SLOT_LINKS_DONE)`
anywhere in `_v72e2` or `_v73e3`).

But **`SLOT_ECO_READY = 5` is also write-only** in `_v72e2`: written at `:615`, `:725`,
`:1715`, `:1903`, and never read anywhere in the file. That gives the doctrine **two**
free 32-bit slots, not one.

### CORRECTION 3 — "destroy is a zero-cost rider" is now ENGINE-MEASURED. **[RESOLVED]**

`docs/game-model.md:223-225` lists only "build/attack/heal" as blocking the round's move,
and `:232-234` calls destroy "no titanium and no action cooldown… unlimited per round".
That reading is now confirmed against the engine.

**Measuring-session probe, 2026-08-07, recorded at `docs/open-questions.md:81-88`**
(replicated across builders): `destroy()` consumes **neither the action nor the move**, is
**unlimited per turn** — two destroys in one turn left `acd=0/mcd=0` with build and move
both still available, and the follow-up build then took the action normally.

**Consequence for this spec:** every placement below is **unconditional**. All
`ct.destroy()` calls sit **outside** every `if ct.get_action_cooldown() == 0:` block, and
none of them competes with a heal, a build, or a move for the round. There is no discount
scenario — the doctrine's titanium and scale returns are net, not gross. The remaining
open half is the Elo question, not the mechanics (`docs/open-questions.md:86-88`).
The in-transit-refund residual (does the refund credit tiebreak #3 only, or #1 too?)
is still open at `docs/open-questions.md:61-62` and bears only on §3.3's endgame teardown.

---

## 1. Every target-choice / route-keep site in `_v72e2`

All line numbers are `bots/_v72e2/main.py`.

| # | Site | Lines | Keep/switch rule as written | Sunk cost / abandonment? |
| --- | --- | --- | --- | --- |
| 1 | `_pick` — ore partition | 2393-2414 | Static per-role partition of `self.map_ores`, walked by a monotonic `self.ore_cursor`; skips a tile only if in vision **and** already built on | None. It is a cursor, not a comparison — there is no score to attach hysteresis to. |
| 2 | `_pick` — nearby-ore fallback | 2416-2419 | `min(ores, key=dist_core)` — pure argmin, recomputed from scratch | **None.** Real argmin, no incumbent bias. |
| 3 | `_pick` — spiral wander | 2420-2425 | Angle+radius spiral, no target concept | n/a |
| 4 | `_expand` retarget gate | 2049-2052 | `if self.tgt is None or p == self.tgt or self.stuck >= 5: self.tgt = self._pick(ct)` | `stuck >= 5` is the file's only stickiness on the ore target. No penalty for abandoning. |
| 5 | **`_expand` adjacent-ore override** | 2055-2060 | Runs **every move-phase round**: any of the 8 neighbours that is unbuilt ore *unconditionally* replaces `self.tgt` | **None, and it silently discards the `_pick` result every round.** Highest-churn line in the file. |
| 6 | `_expand` link_queue priority | 2039-2048 | `link_queue` beats everything; positional, survives every interruption (`:1866-1868`, `:2004-2005`, `:2188-2189`) | This *is* commitment — the one place the file already behaves like it has hysteresis. |
| 7 | `_guard_target` — escort victim | 2108-2158 | `k = (damaged?, dist_to_raider, eid)` argmin over visible friendly buildings within dsq 4, recomputed every round | **The only existing sunk-cost machinery in the file**: `escort_watch[eid]` counts consecutive not-whole rounds, `ESCORT_STALL_RNDS = 25` (`:89`) writes the building off, `escort_ban[eid] = rnd + ESCORT_BAN_RNDS` (400, `:90`). Per-unit dicts (`:490-491`). |
| 8 | `_find_intruder` | 2063-2086 | Nearest visible enemy builder in our half, `d < best_d`, tie → lowest eid | None. |
| 9 | `_intercept` chase latch | 2160-2214 | `if eid is not None: self.chase_id = eid` — **overwrites unconditionally every round** (`:2166-2170`) | Only a *forget* rule: `INTRUDER_FORGET_RNDS = 8` (`:83`, `:2174`). A closer intruder steals the chase instantly. |
| 10 | `_hunt_turret` candidate sort | 1547-1554 | `cands.sort(key=(hp, dist, bid))` — weakest-first argmin, recomputed every round | Partial: `self.hunting` sticky flag + `self.hunt_defer` ballot ledger (`:1586-1599`, `HUNT_DEFER_BASE=3`, `HUNT_DEFER_SPREAD=4`, `:167-168`). But **no incumbent bias on the target itself** — a freshly-damaged turret outranks the one we have pecked six times. |
| 11 | `_plan_siege` | 1169-1284 | `candidates.sort(key=row[:6])` on `dist + ray_penalty(20) + terrain_penalty(2)`; pick index 0 (role 0) or 2 | Abandonment at `_saboteur:1357-1359` on `self.stuck >= 3`, with **no penalty** — full replan, previous score not remembered. |
| 12 | `_try_counterbattery` | 1641-1705 | First legal `(turret_type, d, facing)` triple wins; up to 8×8 `can_fire_from` probes | No target memory at all — rebuilt from `SLOT_THREAT` every round. |
| 13 | `_home_defend` threat pick | 1086-1096 | `d < best` nearest hostile within core-dsq 36, per round | None. |
| 14 | `_defend` threat chase | 1831-1834 | `self.tgt = unpack_pos(read_store(SLOT_THREAT))`, per round | None. |
| 15 | `_link_path` — the route | 2216-2333 | Reverse BFS tree from all valid Core input tiles; computed **once**, when a harvester is built (`:1718`, `:1906`) | Committed by construction. **Never re-routed on damage.** This is where "reroute short" has to live. |
| 16 | **`_build_next_link` — the rebuild trigger** | 2335-2370 | Pops the head tile if a building already stands there; otherwise builds a conveyor and pops. **No memory of how many times a tile has been rebuilt.** | **None.** This is the 27/14/7-rebuild site (`docs/v79-analysis.md:311`). |
| 17 | **`_move` pave** | 2534-2552 | Every step, if the next tile is empty, `harvesters >= 1`, `pave=True` (`allow_pave = has_launch or harv >= 2`, `:1891`) and the step strictly decreases Manhattan distance to the Core → lay a 3 Ti conveyor facing the Core | **None**, and no connectivity check whatsoever. This is the orphan factory (see §3.2). |
| 18 | `_launchwait` / `_defend` wander | 1148-1156, 1857-1864 | Angle spiral, retarget on `p == tgt or stuck >= 2` | None. |

**Summary: 18 target/route choice sites; exactly one (#7) has any notion of abandonment
cost, and exactly one (#6/#15) has any notion of commitment. Sixteen are memoryless
argmins or unconditional overwrites.**

---

## 2. Where the three doctrine rules live

Design invariant for all three: **`destroy()` calls go OUTSIDE every
`if ct.get_action_cooldown() == 0:` block** — it costs no cooldown and no titanium, so it
must never compete with a heal or a build for the round. (Conditional on Correction 3.)

### (a) DESTROY DOOMED RELAY

Operational definition of "doomed", built from state the bot **already** tracks:

**D1 — the escort stalemate (the 819/905-round case).** `_guard_target` already knows.
At `:2147-2150` the ban fires:

```
if stalled >= ESCORT_STALL_RNDS:
    self.escort_ban[eid] = rnd + ESCORT_BAN_RNDS
    self.escort_watch.pop(eid, None)
    continue
```

- **Insertion point: `_v72e2:2147`, inside that block, before the `continue`.**
- **Rule:** if `ct.get_entity_type(eid) == EntityType.CONVEYOR` (splitter optional; see
  Risk R5) **and** `abs(p.x-bp.x)+abs(p.y-bp.y) == 1` **and** the tile is not in
  `self.link_queue` → `ct.destroy(bp)` and write `pack_pos(bp)` to the condemned slot.
- **State needed: NONE new.** `escort_watch` (`:490`), `escort_ban` (`:491`),
  `ESCORT_STALL_RNDS` (`:89`) all exist. The escort is adjacent by construction on the
  round it decides (`:2199-2210`).
- The existing ban is **per-unit** and stops only *this* escort. Destroying converts it
  into a team-wide, permanent walk-away *and* refunds −1% scale + up to 10 Ti of stack.

**D2 — the medic patch ledger.** The chain medic (`:1928-1948`) heals any adjacent
damaged `MEDIC_TYPES` building with **no ledger at all** — it is the surviving half of the
ransom the escort ban was supposed to end.

- **Insertion point: `_v72e2:1945`**, at the `ct.heal(bp)` call.
- **New state (per-unit, instance attribute — no store slot):**
  `self.patch_count: dict[int, int]`, keyed by building id, `+1` per heal, reset when the
  building reaches full HP.
- **Rule:** propose `DOOM_PATCH_MAX = 12`. Twelve heals = 12 Ti on a 3 Ti conveyor = 4×
  its replacement price, and the escort ledger's own reasoning is written at `:84-88`
  ("25 escort rounds of a building that never comes whole ≈ 25 Ti of heals on a 3-20 Ti
  building — past its replacement price, the escort is paying ransom"). Over the cap:
  `ct.destroy(bp)` instead of `ct.heal(bp)`, and condemn the tile.

**D3 — the rebuild ledger.** `_build_next_link:2364-2366` rebuilds a link tile with zero
memory. This is the direct answer to "the same three tiles rebuilt 27/14/7 times"
(`docs/v79-analysis.md:311`).

- **Insertion point: `_v72e2:2365`** (`ct.build_conveyor(tile, f)`).
- **New state (per-unit):** `self.relay_rebuilds: dict[tuple[int,int], int]`.
- **Rule:** propose `RELAY_REBUILD_MAX = 3`. On the 4th attempt at the same tile, do not
  build: clear `self.link_queue`, condemn the tile, and force a fresh `_link_path` that
  routes around it. Per-unit undercounts (several builders can rebuild the same tile), but
  the measured pathology is a **single builder** holding one tile for 453 rounds
  (`docs/v79-analysis.md:313`), so per-unit is adequate for the case that was measured.

**The team-wide condemned marker (store).** D1/D2/D3 are per-unit; the medic, the
universal heal, `_heal_adjacent` and the pave code will all happily resurrect a condemned
tile from another unit. So one slot carries the condemnation:

- **Use `SLOT_LINKS_DONE = 9`** (`:248`, write-only — verified). Repurpose to
  `SLOT_CONDEMNED`, holding `pack_pos(tile)` of the single currently-condemned tile.
  `pack_pos`/`unpack_pos` already exist (`:403-410`).
- One tile at a time is enough: every measured stalemate is exactly one tile — atoll
  (10,8), meander (9,11), heart (10,8) (`docs/v79-analysis.md:295`, `:313`;
  `_v72e2:2121-2135`).
- `SLOT_ECO_READY = 5` is the spare if a second condemned tile is wanted.
- Readers to gate on it: the chain medic (`:1936-1945`), `_heal_adjacent` (`:2101-2105`),
  `_build_next_link` (`:2364`), `_move`'s pave (`:2547`).

### (b) ORPHAN SWEEP — local, no global BFS

The authoritative global definition lives offline in `tools/replay_census.py:426-467`:
*undirected* = the relay tile sits in a friendly conveyor/splitter group touching the Core
footprint; *directed* (`chain_dir`) honours facing by walking backwards from the Core.
The census's own note (`tools/replay_census.py:66-68`): **`chain_dir` is the sharper
predictor — 0 false positives against 7 for the undirected number. "Report chain, act on
chain_dir."**

That is the key to a local rule, because the *directed* test has a purely local
**sufficient** condition:

> **DEAD HEAD:** a friendly CONVEYOR at `T` facing `f` is provably non-delivering if the
> tile `T.add(f)` is in vision and holds neither a friendly conveyor/splitter nor a Core
> footprint tile.

A dead head can never be in the `delivering` set, whatever feeds it. It is sufficient (no
false positives on a visible tile), not complete (it misses chains that point into another
dead chain, and cycles) — which is exactly the right asymmetry for a destructive action.

**Local detection procedure** (call it `_sweep_orphans(ct)`):

1. For each of the 4 cardinal neighbours `n` of the builder: `bid = get_tile_building_id(n)`
   (wrap in `try/except` — an in-bounds tile outside vision **raises**, see the comment at
   `_v72e2:1441-1447`; on raise, treat as NOT orphaned).
2. Keep only friendly `CONVEYOR` (see R5 on splitters).
3. `f = ct.get_direction(bid)`; `out = n.add(f)`.
4. If `dist_core(out, self.core) == 0` → connected, skip.
5. `obid = get_tile_building_id(out)` (same try/except, fail-safe to "not orphaned").
   If it is a friendly `CONVEYOR`/`SPLITTER` → connected, skip.
6. Else `n` is a dead head. Confirm and destroy (see gates below).

**Cost:** worst case 4 neighbours × ~7 engine calls = **~28 calls/round**. For scale,
`_try_counterbattery:1690-1692` already runs up to 8×8 = 64 `can_fire_from` probes in the
same budget. Comfortably inside `CPU_BUDGET_US = 8000` (`:277`).

**Call site:** `_expand`, **immediately after the CPU guard at `:1955`** and before the
convergence block at `:1989` — so it runs on every expander round including move-only
rounds (destroy needs no cooldown), and is already behind the file's CPU boundary. Mirror
it in `_defend` after the guard at `:1807`.

**Mandatory gates (all four):**

- `ORPHAN_MIN_RND = 150` — same class as `MEDIC_MIN_RND = 150` (`:184`) and
  `HUNT_MIN_RND = 120` (`:215`). Before that, everything looks like construction.
- **`ORPHAN_CONFIRM_RNDS = 25`**, via a per-unit `self.orphan_seen: dict[tuple,int]`
  storing the round the tile was first observed dead-headed. This is *not* optional and
  it is *not* 2 rounds: **lanes are built harvester-first, core-last**, so a lane under
  construction has a dead head for its entire build. `_link_path` returns the path walking
  parent pointers *from* `start` (the harvester) toward the goal (`:2276-2281`), and
  `_build_next_link` builds `link_queue[0]` first (`:2354`) — so `link_queue[0]` is the
  tile nearest the harvester and the head advances toward the Core one tile per build.
  Twenty-five rounds exceeds any realistic lane build time.
- Never destroy a tile in `self.link_queue`, and never a tile within
  `dist_core(...) <= 1`.
- Never on the round it was built (any tile in `self.relay_rebuilds` written this round).

### (c) HYSTERESIS — the exact comparisons

The prior art is `docs/spitball.md:173-176`: 1.75× abandonment penalty + 3× switch
threshold, three top finishers independently. Mapping used below: **1.75× to cheap
per-round re-picks** (the incumbent's score is divided by 1.75, so a challenger must be
1.75× better), **3× to commitments carrying sunk travel or build cost**.

| Site | Exact comparison to change | Factor | Per-unit state (instance attrs persist per unit; **no store needed**) |
| --- | --- | --- | --- |
| `_pick` nearby-ore fallback, `:2419` | `min(ores, key=lambda t: dist_core(t, self.core))` → give the incumbent `self.tgt`, if still a valid unbuilt ore, `dist_core/3.0` | **3×** | `self.tgt` (exists, `:454`) |
| **`_expand` adjacent-ore override, `:2055-2060`** | The unconditional `self.tgt = bp`. Gate it: take the override **only** if `self.link_queue` is empty **and** the current `self.tgt` is more than 3 steps away (i.e. the adjacent ore at distance 1 must beat the incumbent 3:1). | **3×** | none new |
| `_hunt_turret` sort, `:1554` | `cands.sort(key=lambda row: row[:3])` on `(hp, dist, bid)` → replace `hp` with `hp/1.75` when `bid == self.hunt_target_id` | **1.75×** | **new** `self.hunt_target_id`, set alongside `self.hunting = True` at `:1621` and `:1633`, cleared at `:1472` |
| `_intercept` chase latch, `:2166-2170` | `if eid is not None: self.chase_id = eid` → only overwrite when the new intruder is 1.75× closer than the incumbent's last known position, or the incumbent is not visible | **1.75×** | `self.chase_id`, `self.chase_pos` (exist, `:485-486`) |
| `_guard_target` argmin, `:2155-2156` | `k = (0 if damaged else 1, d, eid)` → `d/1.75` when `eid == self.guard_id` | **1.75×** | **new** `self.guard_id`, set from the returned `best` |
| `_home_defend` threat pick, `:1092-1094` | `if d < best` → `if d * 1.75 < best_for_incumbent` | **1.75×** | **new** `self.defend_target_id` |
| `_plan_siege` replan trigger, `_saboteur:1357-1359` | `if self.stuck >= 3: <full replan>` → replan only if the best new candidate score beats the stored score of the current approach by 3× | **3×** | **new** `self.siege_score`, stored at `:1281-1283` |
| `_link_path` re-route | New: only re-route a lane when the doomed/rebuild ledger fires (D3), never on ordinary damage | commitment | `self.relay_rebuilds` (new, D3) |

**Note on relative value:** the two `3×` sites are worth more than all five `1.75×` sites
combined, because `_expand:2055-2060` runs *every round* while the others run only on a
retarget.

---

## 3. Expected value

### 3.1 Scale relief **[NEW — computed here]**

Live scale = `1.00 + 0.01·(conveyors+splitters+barriers) + 0.05·harvesters
+ 0.10·launchers + 0.20·(builders+gunners+sentinels)`, counting **live** entities
(`docs/game-model.md:357-364`, Correction 1).

End-state census, seat A (our v55/v72e2 family), from `docs/v79-analysis.md`:

| | meander | heart |
| --- | --- | --- |
| conveyors alive | 201 built − 86 killed = **115** (`:310`) | **40** of 48 built (`:186`) |
| — of which orphaned | not measured | **18** (`:187`) **[PRIOR]** |
| harvesters alive @r1000 | **7** (`:177`) | **5** (`:177`) |
| builders alive | 18 spawned − 13 lost = **5** (`:312`) | 17-18 spawned (`:189-190`), losses unstated → **10** **[ASSUMED]** |
| turrets alive | **0** (all dead r40-r276, `:307-308`) | 2 **[ASSUMED]** |
| launcher | 1 at (9,4) (`:317`) | — |
| **live scale** | **3.60** | **4.05** |

| Sweep | Scale | Discount | Ti saved on a 655 Ti-base back-half build sequence |
| --- | --- | --- | --- |
| heart: destroy the measured 18 orphans | 4.05 → 3.87 | 4.4% | **165 Ti** (2634 → 2469) |
| meander: 18 orphans (conservative transfer) | 3.60 → 3.42 | 5.0% | **71 Ti** (2278 → 2207) |
| meander: 52 orphans (heart's 45% orphan rate applied to 115 live relays) **[EXTRAPOLATED]** | 3.60 → 3.08 | 14.4% | **290 Ti** (2278 → 1988) |

Build sequence used (meander-calibrated on `docs/v79-analysis.md:310-312`): 100 conveyors
(3 Ti base) + 5 harvesters (20) + 6 builder replacements (30) + 3 turrets (25 avg) =
**655 Ti of base cost**, `floor(scale × base)` per item.

**Range: 71-290 Ti per match, at zero action cost and zero titanium cost.** For scale,
meander seat A *delivered* 5,660 Ti all match (`docs/v79-analysis.md:300`), so the
aggressive case is ~5% of the entire match's delivered titanium, bought for free.

**The denominator caveat, stated honestly:** with a live scale already at 360-405%,
removing 18 points is only a 4-5% discount. The doctrine's scale lever is real but
*second-order* unless the sweep is large (40+ tiles), because the builder-bot term
(+20% each, 5-10 live = +100-200%) dominates the multiplier. The `SURGE_EXTRA`/replacement
population is a bigger scale problem than the conveyors are — but it is not this thread's.

### 3.2 The orphan generator — mechanism, from code **[NEW]**

`_move`'s pave block (`:2541-2548`) builds the conveyor at `nxt` (the tile about to be
stepped onto) facing `card = nearest_cardinal(nxt.direction_to(nearest_core_tile(...)))`,
while the builder actually steps in direction `d` (chosen by `_bfs_direction` toward an
**ore** target, `:2523`). For the paved trail to be directed-connected, every tile's
`card` must equal the *next* step's direction.

`nearest_cardinal` (`:413-420`) collapses NE→E, SE→E, SW→S, NW→W — so on any diagonal
approach to the Core, `card` is pinned to one axis while the builder's actual path zig-zags.
**Every turn of the zig-zag leaves a conveyor pointing at a tile that never receives one.**
This is a *directed*-connectivity failure; it is priced, worked through step by step, and
specified as a fix in **§3.2b** below. (It is **not** the mechanism behind "18 of 40
surviving relays connect to nothing" — that figure is the *undirected* measure and carries
no facing information; see §3.2b(b). The facing-aware evidence is
`docs/v79-analysis.md:178`.) The open question at `docs/open-questions.md:126-131` ("Every
walked tile lays a conveyor… whether or not the trail will ever carry anything") covers
both modes.

Corollary, now commissioned as piece F: **the cheapest fix here is not `destroy()` at
all** — it is making the pave facing agree with the walk. `destroy()` cleans up the
orphans; fixing the facing stops making them.

### 3.2b Pave-facing fix — exact semantics (commissioning spec for piece F)

**First, two corrections to the framing.**

**(a) The builder paves while walking TOWARD the core, not away from it.** The gate at
`_v72e2:2545` requires `manhattan(nxt, core) < manhattan(here, core)` — paving only fires
on a step that strictly decreases distance to the Core anchor. So stack flow and walk
direction are the **same** direction (coreward). "Trail-behind" is therefore the right
*placement* but the wrong *mental model*: flow is forward along the walk, not backward.

**(b) 18/40 carries no facing information.** `tools/replay_census.py:426-445` computes
`relays_connected` **undirected** — it ignores facing entirely. So "22 of 40 connected"
cannot tell us how the successes were oriented, and the two failure modes are distinct:

- **undirected orphan** = the trail never physically reached the Core (builder retargeted
  mid-walk, died, or the pave gate flipped off);
- **directed orphan** = the trail reached the Core but tiles point sideways. This is what
  piece F fixes.

The facing-aware number is `chain_dir` (`replay_census.py:461-479`), reported per harvester
at `docs/v79-analysis.md:178`: **A directed-connected harvesters = atoll 2, heart 2,
jackpot 2, meander 1**, against 5/5/3/**7** alive (`:177`). **On meander, 1 of 7 live
harvesters could deliver.** And the delivery rates at `:179` confirm the mechanism is
binding: atoll 5.00 Ti/rd = exactly 2 harvesters' throughput with directed=2; heart 5.00 =
exactly 2 with directed=2. **Two of three maps match `directed` to the decimal.** That is
the price tag on piece F, and it is larger than everything in §3.1-3.4 combined: heart
going 2 → 5 directed-connected is +3 × 2.5 Ti/rd × 700 rounds ≈ **+5,000 Ti** (upper bound:
it assumes facing was the only break).

**Why `card` is wrong.** `card = nearest_cardinal(nxt.direction_to(nearest_core_tile(...)))`
(`:2546`). `nearest_cardinal` (`:413-420`) collapses NE→E, SE→E, SW→S, NW→W, so on a
diagonal approach `card` is pinned to one axis while `_bfs_direction` (`:2523`) zig-zags
across two. Worked example, core anchor (0,0), builder walking (5,5)→W→(4,5)→N→(4,4)→W→
(3,4)→N→(3,3): `card` is WEST at **every** one of those tiles, so (4,5) outputs to (3,5)
and (3,4) outputs to (2,4) — **neither is ever visited**. Dead heads at (4,5) and (3,4),
live at (4,4) and (3,3): **exactly 50% on any zig-zag.**

**The rule.** Pave the tile you just **left**, facing the direction you just **moved**;
its output is the tile you now stand on, which is the next tile of the same trail.
Two new per-unit attributes (instance attrs persist per unit; no store slot):
`self.pave_prev: Position | None`, `self.pave_dir: Direction | None`, both set immediately
after the successful `ct.move(d)` at `:2550` and cleared to `None` on every round the unit
does not move.

Replacing the block at `:2541-2548`, the expression that replaces `card` is:

```python
pp, pd = self.pave_prev, self.pave_dir
if dist_core(pp, self.core) == 1:
    # TERMINAL: pp is orthogonally adjacent to the footprint. The original
    # `card` expression is correct here and ONLY here -- it aims into the Core.
    facing = nearest_cardinal(pp.direction_to(nearest_core_tile(pp, self.core)))
    coreward_ok = True          # we are leaving; the coreward gate cannot hold
else:
    facing = pd                 # INTERIOR: output == the tile we now stand on
    coreward_ok = (abs(here.x - self.core.x) + abs(here.y - self.core.y)
                   < abs(pp.x - self.core.x) + abs(pp.y - self.core.y))
```

then the unchanged guards (`is_tile_empty(pp)`, `SLOT_HARVESTERS >= 1`,
`resources >= get_conveyor_cost()`, `dist_core(pp) > 0`, `can_build_conveyor(pp, facing)`)
and `ct.build_conveyor(pp, facing)`. `pp` is orthogonally adjacent by construction (one
cardinal step), and `pd` is always cardinal (moves are cardinal-only, `:2549-2551`), so
both legality preconditions are free.

**First-tile / terminal case.** Under the interior clause alone the trail's *coreward end*
is the one dead head — the worst possible place, since it is the delivery point. The
terminal clause above fixes it: the last tile the builder stands on before leaving the
Core's neighbourhood gets paved facing **into the footprint**. Net: **zero dead heads on a
trail that reaches the Core; exactly one (at the head) on a trail that is abandoned
mid-walk** — versus ~50% of all tiles today.

**Interaction with `_bfs_direction` retargeting.** The pave is opportunistic on whatever
coreward step `_nav` happens to take toward an **ore** target; it is not a deliberate trip
home. Any retarget (`_expand:2049-2052` on `stuck >= 5`, the adjacent-ore override at
`:2055-2060`, `_pick`'s cursor at `:2409-2414`) can turn the builder around and end the
trail. That is the *undirected* failure mode and piece F does not fix it — it bounds it to
one dead head instead of half the trail. Two invalidations are mandatory: clear
`pave_prev/pave_dir` (i) on any round where `ct.move()` was not called, and (ii) on the
Launcher handshake at `_builder:832-834`, since a thrown bot's `pave_prev` is arbitrarily
far away. (`can_build_conveyor` would fail safe on adjacency either way, but a stale
`pave_prev` wastes an engine call every round.)

**Tempo is unchanged.** Build and move are mutually exclusive (`docs/game-model.md:223-225`),
and the current code builds at `:2548` then calls `ct.can_move(d)` at `:2549` — which is
already False after a successful pave, so `_move` returns False, `_nav:2529-2532` retries
three directions (all act-locked) and does `self.stuck += 1`. **Today's pave already costs
a full movement round and inflates `self.stuck`** (feeding the very retarget churn in §1
row 4). The new rule costs the same one round per tile. No regression, and the `stuck`
inflation is identical — but see the note below.

**Re-facing already-paved tiles.** Conveyor facing is **fixed at build time**
(`docs/game-model.md:323-324`) and `rotate()` is **Gunner-only** (`_v72e2:2632-2637`,
Controller API). So a wrong-facing tile can only be corrected by **destroy + rebuild**.
Price, honestly: destroy is free and refunds the +1% and any held stack, but the rebuild is
`floor(scale × 3)` — at meander's live scale of 3.60 (§3.1) that is **10 Ti, not 3**, plus
one act-locked builder round, plus the +1% goes straight back on. Payback: re-facing a
single head that is the only break in a 6-tile lane restores 2.5 Ti/rd, so 10 Ti repays in
**4 rounds**. Verdict: **worth it, but ship it separately.** Recommendation — piece F is
the pave fix **alone** (it stops manufacturing the problem); re-facing is a follow-on that
reuses the §2(b) dead-head sweep with its DESTROY branch replaced by
DESTROY-AND-REBUILD-FACING-`f'`, fired only when exactly one of the tile's other three
sides holds a friendly relay (so `f'` is unambiguous). Note the interaction if both ship
un-coordinated: the plain §2(b) sweep would *unravel* an abandoned trail one tile per
sweep from the head backwards — correct behaviour for a trail that delivers nothing, but
slow, and it must not be pointed at a trail whose head is merely mis-faced.

### 3.3 Returned in-transit stacks **[NEW — estimate]**

A conveyor holds exactly one stack = 10 Ti (`docs/game-model.md:323-325`,
`GameConstants.STACK_SIZE=10`).

- **Pure dead heads carry little**: a chain that connects to nothing but is *fed by a
  harvester* holds stacks that shuffle forever. heart has two such: harvesters #389 (10,19)
  and #844 (5,15) **never shipped a single stack** (`docs/v79-analysis.md:184-185`)
  **[PRIOR]**. At ~5 tiles per dead lane and ~50% occupancy, tearing both down returns
  ~5 stacks = **~50 Ti** **[ESTIMATE]**.
- **End-of-match teardown is free money on tiebreak #3.** Tiebreaks are: delivered → 
  harvesters alive → titanium **stored** → coinflip. Stranded belt stacks score **nothing**
  (`docs/spitball.md:154-156`), and `destroy()` moves them to the balance
  (`docs/game-model.md:234-235`). meander seat A holds 115 live conveyors; at 30% occupancy a
  r998 sweep converts ~34 stacks = **~340 Ti** from "scores nothing" into stored titanium
  **[ESTIMATE]**. Calibration: atoll was lost on tiebreak **#1** by 190 Ti = 19 stacks
  (`docs/spitball.md:242-243`) **[PRIOR]** — the magnitude is decisive-sized.
  - **Caveat, and it is a real one:** `docs/open-questions.md:55-58` records the measured
    fact that the *balance* and `titanium_collected` both move **only on delivery to the
    Core**. So the refund plausibly credits tiebreak **#3 (stored)** and not **#1
    (delivered)**. `docs/open-questions.md:61-62` flags exactly this residual as open. A
    r998 teardown therefore only pays when #1 and #2 are already tied — but it costs
    *nothing*, so it is free option value.

### 3.4 Freed defense labor **[PRIOR — all re-cited]**

| Case | Cost paid | Citation |
| --- | --- | --- |
| atoll: raider pecked one sentinel **819** times r181-999; escort healed it 819 times | one builder's entire action budget + **~1,100-1,200 Ti ≈ 20% of match income** | `_v72e2:2121-2131`; `docs/spitball.md:162-167` |
| heart: **717** pecks on a **3 Ti** conveyor | one builder | `_v72e2:2127-2128` |
| meander: **905** heals, **905 Ti**, **453 rounds**, one builder, on a 3 Ti conveyor inside a gunner kill zone that **never delivered a stack** | 905 Ti + a builder for 45% of the match | `docs/v79-analysis.md:313-314`; `_v72e2:2128-2130` |
| heart secondary: the same loop on (10,8) froze **one more** A builder for **737 rounds** | a second builder | `docs/v79-analysis.md:295` |

`ESCORT_STALL_RNDS=25`/`ESCORT_BAN_RNDS=400` (`:89-90`) was added *after* these
measurements, so they are the pre-fix baseline. But the ban is per-unit and does not stop
the chain medic, `_heal_adjacent`, or the rebuild — hence D1+D2+D3+the condemned slot.

### 3.5 The churn bill, for context **[NEW — computed from cited counts]**

meander, seat A: 201 conveyor builds (`docs/v79-analysis.md:310`) at an assumed
time-weighted average live scale of 2.6 (start 1.0, end 3.60) → `floor(2.6×3) = 7 Ti` each
→ **~1,407 Ti spent on conveyors**, of which the 86 that died and were replaced account for
**~602 Ti** of pure churn. Add the 905 Ti single-tile escort loop: **~2,300 Ti of
identified waste against 5,660 Ti delivered = ~41% of the match's output.** (Sensitivity:
at avg scale 2.2 → 1,206/516 Ti; at 3.0 → 1,809/774 Ti.) **[ASSUMED: the average-scale
figure. Everything else is cited counts.]**

---

## 4. Risks

**R1 — destroying a load-bearing relay.** The orphan test is vision-limited, and
`get_tile_building_id` **raises** for an in-bounds tile outside vision with the same
message as an off-map tile (`_v72e2:1441-1447`). Every lookup must be wrapped and must
**fail safe to "not orphaned"**. Never invert this.

**R2 — the destroy/rebuild oscillation.** `_build_next_link:2345-2347` pops a queued tile
if a building stands there, and rebuilds if not. If unit X destroys a conveyor that is in
unit Y's `link_queue`, Y rebuilds it next round, X destroys it again: 3 Ti and a
+1%/−1% scale flap per cycle, forever. **This is the single most dangerous failure mode of
the whole doctrine.** Mitigations, all three required: (i) never destroy a tile in
`self.link_queue`; (ii) the team-wide condemned slot must gate `_build_next_link:2364` and
`_move`'s pave at `:2547`; (iii) `ORPHAN_CONFIRM_RNDS = 25`.

**R3 — the medic and universal-heal resurrect condemned tiles.** Three call sites will
patch a building we have written off: the chain medic (`:1928-1948`), `_heal_adjacent`
(`:2088-2106`) and — indirectly — the universal Core heal (`:991-993`). `_heal_adjacent`
is the awkward one: it calls `ct.can_heal(t)` with **no type or id check** (`:2101-2105`),
so gating it on the condemned slot costs one extra `get_tile_building_id` per cardinal.
Cheap, but it must be done or D2 leaks.

**R4 — the hardcoded hive barrier at `_v72e2:1729-1745`.** The `hive_bunker` branch
(25×25, core (21,3)) builds a barrier at (20,4) and heals it indefinitely. A doom rule keyed
on "repeatedly damaged" would tear it down — **being repeatedly damaged is a barrier's
entire job** (10 HP/Ti, the best ratio in the game, `docs/spitball.md:210`). **Exclude
`BARRIER` from every doom/orphan set.** Propose `DOOM_TYPES = (EntityType.CONVEYOR,)`.

**R5 — splitters must not be judged by one facing.** A splitter accepts from directly
behind only and rotates output among the **other three** cardinals
(`docs/game-model.md:326-328`). A single-facing dead-head test is wrong for it. Either
exclude splitters from the sweep, or require all three non-back sides to be dead. Simplest
and safest: **conveyors only** in v1.

**R6 — never destroy a harvester.** +5% is a large single refund and the temptation exists
(e.g. heart's #389 and #844, which never shipped). But **harvesters alive is tiebreak #2**,
where we are 13W-26L (`docs/spitball.md:241`). Killing an unwired harvester trades a
tiebreak counter for 5 scale points. Explicit exclusion.

**R7 — self-defeating cheapness.** Destroying our own conveyors lowers the scale, which
makes the *next* conveyor cheaper, which makes the unconditioned pave path (`:2541-2548`)
more affordable. Sweep and pave can chase each other. The condemned slot plus the
build-round stamp handle the same-tile case; the general case needs the pave fix in §3.2.

**R8 — the 819-round atoll case is a SENTINEL, not a conveyor.** Re-reading
`_v72e2:2121-2131`: "the raider pecked one **sentinel** 819 times… and the escort healed it
819 times". So the flagship "walk away" case is a 30 Ti, +20%-scale weapon, not a 3 Ti
relay. Destroying it refunds **20** scale points (4× a conveyor) but loses a gun. The
existing ban already walks away from it; **do not extend D1's destroy to turrets in v1** —
the doctrine's mandate is relays, and the turret case needs its own measurement.

**R9 — `destroy()` raises `GameError` if illegal.** An escaped exception permanently
deletes the unit (`docs/game-model.md`, `_v72e2:524-535`). Every call must be gated on
`ct.can_destroy(pos)` and sit inside the existing `try/except` in `run()` — which it does,
but the `can_destroy` gate is not optional.

**R10 — this file has no dead-code budget.** `HANDOVER.md:17` already records an owed
cleanup (`COUNTERBATTERY_RICH_TI` declared, never used — confirmed: `_v72e2:102` declares
it, zero uses). Adding three ledgers and two constants without shipping them all is how
that happens again.

---

## 5. Recommended ship order (smallest shippable first)

0. **Piece F, the pave-facing fix (§3.2b)** — outranks everything else in this file. It is
   ~10 lines, it costs no tempo (today's pave already burns the movement round), and the
   facing-aware evidence prices it at 2 → 5 directed-connected harvesters on heart, an
   order of magnitude above the scale-relief numbers. Commissioned to the measuring session.
1. ~~The destroy-mechanics probe~~ — **DONE**, `docs/open-questions.md:81-88`: destroy
   consumes neither action nor move, unlimited per turn. All placements are unconditional.
2. **D1 only** — six lines at `_v72e2:2147`, zero new state, zero new constants, and it
   attacks the largest cited number (905 Ti / 453 rounds / one builder). Measurable alone.
3. **Orphan sweep** with `ORPHAN_MIN_RND=150` + `ORPHAN_CONFIRM_RNDS=25`, conveyors only.
4. **Hysteresis at `_expand:2055-2060`** — the 3× gate on the adjacent-ore override. One
   condition, no new state, and it is the only churn site that fires every round.
5. D2/D3 + the condemned slot, together (they are meaningless apart).

Everything else in §2(c) is a one-line change each and should be batched into one
experiment, not five.
