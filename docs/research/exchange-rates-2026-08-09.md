# Exchange rates: what costs us little and them a lot

**Research arm, 2026-08-09 (session 22).** Magnus's trickster tasking, axis A.
Spec-derived — **no corpus, so nothing here can be confounded by sampling.**
Sources: `CLAUDE.md` (cited `CM:n`) and the engine type stubs
`.venv/.../fcode/_types.py` (cited `TY:n`). **Stubs outrank CLAUDE.md.** The
engine itself is a compiled `.so`, so stub docstrings are documented intent.
Claims marked **[V]** were re-verified against source by me before relay.

---

## 0. THE PRIMITIVES — and a correction to `heal-arithmetic-2026-08-09.md`

| channel | rule | rate |
|---|---|---|
| **fresh barrier** | 3 Ti → 30 HP | **10.00 HP/Ti** |
| builder heal | 1 Ti → +4 HP, all friendly on the tile | 4.00 HP/Ti |
| sentinel | 10 ammo → 18 dmg | 1.80 HP/Ti |
| gunner | 4 ammo → 7 dmg | 1.75 HP/Ti |
| builder attack | 2 Ti → 2 dmg, **buildings only** | 1.00 HP/Ti |

**My heal doc claimed healing is the most titanium-efficient HP in the game. It
is not — a fresh barrier is, by 2.5x.** What rescues healing is scaling:
**cost scale touches BUILDS ONLY.** Heal, attack, ammo and rotate are flat
constants, not `*_BASE_COST`. So heal is 4.00 HP/Ti *forever* while barrier
decays as `30/(3S)`.

> **Crossover at S = 2.5** (conveyor at S = 1.67). **Barriers before heals early,
> heals after.** Readable at runtime from `get_scale_percent()`.

Healing also beats attacking **2:1 in TURNS** (4 HP repaired/turn vs 2 dealt),
which is scale-invariant and drives §2.

## 1. RANKED ASYMMETRIES (enemy Ti to undo ÷ our Ti to do)

| # | asymmetry | ratio |
|---|---|---|
| A1 | **harvester kill + ore-tile barrier** | **~87:1** |
| A2 | sentinel facing is permanent — step one tile off its line | ∞ |
| A3 | launcher displacement (no ammo, no titanium) | ∞ per use |
| A7 | **core spawn-ring lock** | 10:1 sustained |
| A6 | barrier as ammo bait / raw denial | 6.67:1 Ti, **15:1 turns** |
| A4 | own-territory barrier maze (one-way permeable via `destroy()`) | 10:1 |
| A9 | **shoot healers, not cores** | 7:1 to 25:1 |
| A8 | destroy-and-rebuild cheap buildings vs healing them | 2.5:1 Ti, 8:1 turns |

**Place-vs-remove, S=1.0.** Builder removal costs exactly 1 Ti per HP.

| entity | place | HP | cheapest removal | **ratio** | HP/Ti |
|---|---|---|---|---|---|
| **Barrier** | 3 | 30 | 20 | **6.67** | **10.00** |
| **Conveyor** | 3 | 20 | 12 | **4.00** | 6.67 |
| Splitter | 6 | 20 | 12 | 2.00 | 3.33 |
| Harvester / Launcher | 20 | 30 | 20 | 1.00 | 1.50 |
| Gunner | 20 | 25 | 16 | 0.80 | 1.25 |
| Sentinel / Builder bot | 30 | 40 | 24 | 0.80 | 1.33 |

**Only barrier and conveyor are cheap-to-place and dear-to-remove.** Turrets and
builder bots are *cheaper to remove than to place* — bad denial, good targets.

## 2. THE IMMUNITY THEOREM — the heal finding in closed form

A 1x1 building has 4 orthogonal neighbours. Two healers repair 8 HP/round for
2 Ti; the two attackers they leave room for deal 4 dmg/round for 4 Ti. **Net HP
never falls, and builders cannot attack builders, so the healers cannot be
removed either.**

**[V] Core version.** `is_tile_passable` (`TY:345-348`): *"either has no building
on it or has a conveyor, splitter, **or the allied core**"* — **builders may
stand on their own core.** Four healers on the 2x2 footprint repair +16/round
against a theoretical maximum 16 dmg/round from all 8 ring tiles: **exact
standoff. A fifth healer makes the core mathematically unkillable by builders**
(20 vs 14), costing them 5 Ti/round against our 14.

**Only turrets and launchers break it.**

## 3. THE CONVERSION WALL, PRICED

Grinding a 4-healer-screened 500 HP core:

```
2 sentinels  net  2 HP/round -> 250 rounds, ~2,500 Ti
3 sentinels  net 11 HP/round ->  46 rounds,   ~780 Ti
clear the 4 healers first: 4 x 40 HP x 6 gunner shots = 96 Ti
```

> **Shoot the healers, not the core: 96 Ti versus 780-2,500 Ti.**

Screen regrowth is capped at **1 builder/round** at 30·S each. Six gunners firing
(24 Ti/round of ammo) exactly matches a 1/round respawn costing 30 Ti/round —
**an income race**, which is why ore denial (A1) outranks everything.

## 4. **[V] CLAUDE.md IS WRONG ABOUT THE SPAWN RING**

```
CORE_SPAWNING_RADIUS_SQ = 2      (TY:52)   <-- exists SEPARATELY
CORE_ACTION_RADIUS_SQ   = 8      (TY:53)
```

`CM:24` and `CM:31` say the r²=8 action radius governs spawning; **the stubs
define a distinct spawning radius of 2**, and `spawn_builder` says *"immediately
surrounding the core's footprint"*. CLAUDE.md contradicts itself at `:134`.

**The spawn ring is the 12-tile Chebyshev-1 ring — a lock is ~36 Ti, not ~120.**
Since `destroy()` is allied-only, clearing one tile costs them 30 Ti and 15
builder-turns; we re-seal for 3 Ti and one turn.

## 5. **[V] THE HIGHEST-VALUE UNTESTED CLAIM — one probe settles it**

`is_tile_empty` (`TY:341-343`): *"Return True if the tile has no building and is
not a wall."* **A builder bot does not make a tile non-empty.**

If `can_build_barrier` inherits that definition literally, **a 3 Ti barrier can be
built on top of a 30 Ti enemy builder, and barriers are impassable — imprisoning
it permanently.** 10:1, refunds no cost-scale (§6), and it would also mean
parking bots on our own spawn ring is no defence against §4.

**Builder's lane: one local probe.**

## 6. KILLING IS A REBATE; IMPRISONING IS NOT

Scale tracks **live** entities (builder-probed 2026-08-09). A kill returns **−20%
scale** — against a 500 Ti remaining plan, a ~100 Ti gift, potentially exceeding
the 30·S body destroyed. Imprisonment refunds nothing, keeps the +20% on their
books, and holds a `MAX_TEAM_UNITS` slot.

> **Never kill a capped opponent's builder — you are freeing their slot.**

## 7. **[V] TIEBREAK KEY 1 IS UNOBSERVABLE IN-GAME**

No Controller getter exposes cumulative delivered titanium. `get_global_resources`
is *stored* (key 3). **The primary tiebreak cannot be read**, so any endgame
"am I ahead?" logic is structurally blind. Key 3 corollary: **banked ammo at
r1000 scores nothing — never pre-convert beyond one round of expected shots.**

## 8. NEGATIVES — reported so nobody chases them

- **Conveyor cutting as sustained denial is 4:1 AGAINST us** (12 Ti of ammo to
  cut, 3 Ti for them to repair). The correct version is a barrier on the output
  tile.
- **Harvester killing without ore denial is ~1:1** — "first stack immediately on
  build" means output resumes instantly; only downtime is gained.
- **Builder bots as ammo bait are 0.8:1, a loss.** Barriers are the only
  profitable bait.
- **Killing builder bots is 1.25:1**, the weakest positive trade in the game, and
  it refunds scale.
- **Self-destruct does 0 damage.** No offensive use.
- **Gunners are the most inflationary build per titanium** (0.0100 δ/B) **and
  blind themselves on our own barriers.** A walled defence must use sentinels.
- Passive income, comm store and starting titanium are perfectly symmetric.

## 9. WHAT IS LEAST VERIFIED — read before ranking anything

**The scale increments (+1/+5/+10/+20%) appear ONLY in CLAUDE.md; there are no
scale constants anywhere in the stubs.** The builder's probe corroborates the
global-multiplier *shape*, but the per-category rates are the least-verified
numbers here and several rankings depend on them. Also stub-silent: attack radii,
the sentinel's line pattern, harvester output rate, `destroy()`'s "unlimited per
turn", and the 10 ms budget.

**The most consequential ambiguity is `CM:18`** — physical stacks "separate from
the global pool". Read literally, harvested titanium never funds builds and
harvesters are tiebreak-only, which **collapses A1**. The working reading is that
stacks are separate *in transit* and credit the pool on delivery.

## 10. OTHER CLAUDE.md / STUB CONFLICTS WORTH KNOWING

- **Launcher pickup range**: `CM:39` says "adjacent"; `can_launch` (`TY:699`)
  states no adjacency requirement. If pickup is range-wide (r²=26) the launcher
  is a 5-tile enemy-teleporter. **Cheap, high-value test.**
- **`can_heal` requires a damaged target** (`TY:588-589`) — you cannot pre-heal.
- **`get_nearby_tiles` raises if `dist_sq` exceeds vision** (`TY:357`); an
  uncaught raise **permanently destroys the unit**.
- **`rotate` to the current facing is illegal** (`TY:663`) — an easy GameError.
- **`write_store` is u32** (`TY:625`) — negatives wrap silently.
- **Conveyors and splitters are walkable and are NOT team-qualified in the
  passability rule** (only the core is). **Our conveyor network may be the
  enemy's fastest road into our base.**
