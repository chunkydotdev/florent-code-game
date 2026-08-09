# Turret firing lines and friendly entities: both cases now measured, not inferred

**Research arm, session 23, 2026-08-09.** Commissioned by the builder arm.
**Version tag:** live **v90 "Heimdall 1 (launcher relight)"**, 1589 → 1586 @ 502,
rank #28-29/113. Engine `fcode` (compiled `fcode_engine.cpython-313-darwin.so`);
docstrings from `.venv/.../fcode/_types.py`.
**Method:** two local deterministic probes, `--tle 0`, seed 1, `maps/fjordgate.map26`,
against an idle opponent. Probes live in the session scratchpad, **not in `bots/`**.
Zero arena runs, zero downloads, zero bot edits.

---

## 0. TL;DR — the two booleans

| turret | friendly entity in the line | verdict |
|---|---|---|
| **GUNNER** | blocks — `can_fire` goes **True → False**, and the shot cannot be taken | **BLOCKED** |
| **SENTINEL** | ignores it — **18 damage landed through a friendly builder bot *and* a friendly barrier** | **PASSES THROUGH** |

And a third result that neither question asked for but that matters more than
either:

> **`get_attackable_tiles()` returns the target in BOTH the clear and the blocked
> case.** The raw pattern advertises coverage the gunner cannot deliver.

---

## 1. Why a probe rather than a code read

The engine ships as a compiled `.so`; `_types.py` is stubs. The docstrings are
normative but partial — **every blocking sentence in the API is scoped
"for gunners"**, and the sentinel case is never stated:

`_types.py:630` (`can_fire`):
> *"**For gunners**, only empty tiles fail to block the firing line. Walls block
> the line but are not targetable. **Builder bots and buildings are both targetable
> and blocking.**"*

`_types.py:679` (`get_attackable_tiles`):
> *"Return all in-bounds tiles in this turret's raw attack pattern. **This ignores
> ammo, cooldown, occupancy**, and other target-specific legality checks."*

CLAUDE.md says the sentinel *"ignores obstacles (unlike Gunner)"* — but that is a
summary, and it says nothing about *friendly* entities specifically. **The builder
was about to write siting code against the gunner docstring, so both halves needed
behaviour, not prose.**

## 2. Design — each probe is its own control

**Sentinel probe.** A hypothetical-turret query (`can_fire_from`, which ignores
ammo and cooldown, isolating line-of-sight) at a fixed position, facing and target,
measured **before and after** a friendly barrier is placed in the line. The
**GUNNER is the positive control**: its answer is documented, so if the method does
not reproduce "gunner gets blocked", the method is wrong and the sentinel row must
be discarded. Then a **real sentinel fires a real shot** through the line.

**Gunner probe.** Within-subject before/after on one real gunner: same turret, same
facing, same target, only the barrier changes. The blocker is placed from a tile
*beside* the line so the builder bot never occupies the line itself — otherwise bot
and barrier would be confounded and we could not say which one blocked.

## 3. Results

### Sentinel — predicate, with the gunner as control

```
STEP 1  LINE CLEAR                         round 8
  turret (4,6) facing EAST | blocker tile (5,6) | target (6,6) enemy core, d²=4
    can_fire_from GUNNER   (CONTROL)  = True
    can_fire_from SENTINEL            = True

STEP 3  LINE BLOCKED BY OUR OWN BARRIER    round 10
    blocker on (5,6): BARRIER, FRIENDLY=True, hp=30
    can_fire_from GUNNER   (CONTROL)  = False   <-- control PASSED, method sound
    can_fire_from SENTINEL            = True    <-- unchanged
```

### Sentinel — the real shot

```
STEP 4  REAL SENTINEL, REAL SHOT           round 12
  sentinel (3,6) facing EAST, ammo 40
  the firing line, tile by tile:
      (4,6) : BOT(team=A, friendly=True)               <-- our own builder bot
      (5,6) : BARRIER(team=A, friendly=True)           <-- our own building
      (6,6) : CORE(team=B, friendly=False)             <-- target
  can_fire(target) = True    enemy core HP before = 500
  FIRED -> HP after = 482    (delta -18)
```

**−18 is exactly `SENTINEL_DAMAGE`.** Full damage, through two friendly entities of
both kinds the gunner docstring names as blocking.

### Gunner — within-subject before/after

```
CLEAR (line empty)                         round 8
  gunner (6,3) facing SOUTH
      (6,4) empty   (6,5) empty   (6,6) CORE(friendly=False)
  get_attackable_tiles() contains target?  True
  can_fire = True    HP 500 -> 493   (delta -7)      <-- = GUNNER_DAMAGE

BLOCKED (friendly barrier in the line)     round 18
  gunner (6,3) facing SOUTH        [same turret, same facing, same target]
      (6,4) BARRIER(friendly=True)  (6,5) empty   (6,6) CORE(friendly=False)
  get_attackable_tiles() contains target?  True      <-- STILL TRUE
  can_fire = False   -> no shot possible, no damage
```

## 4. What this changes

**1. `sentinel-file-stacking` moves from `inference` to `documented-by-probe`.**
Sentinels can be stacked in single file on one ray, all bearing on the same tile,
without blocking each other. Against a defender's **~16 HP/round per-tile heal cap**
(4 adjacent healers × 4 HP — there is no fifth, adjacency forbids it), 2-3 sentinels
on one tile make net progress and every one beyond that is surplus the defender
*cannot* answer. This is the one mechanism found so far that beats the 2.2:1
defensive edge by concentration rather than by out-damaging it.

*Unmeasured caveats that remain:* sentinel scale is +20% per build (the 6th costs
~3× base), `MAX_TEAM_UNITS = 50` caps the fleet, and reload 2 caps each sentinel at
~6-9 HP/round. **Legal ≠ affordable.** Nothing here says the formation wins, only
that the engine permits it.

**2. Our own gunner ring can self-block, and the scoring function cannot see it.**
`get_attackable_tiles()` returned the target in *both* phases. Any siting logic that
scores candidate tiles with `get_attackable_tiles` / `get_attackable_tiles_from` is
scoring coverage the gun will not deliver once our own bots and buildings stand in
the line. With **41,921 gunner builds against 13,298 sentinel** in the corpus this is
the dominant case, and it sits in the **home band — the one place we measure better
than the field** (+11.4 / +16.6 / +22.3pp). **Statically checkable against the siting
code; no battery needed.** Builder owns it (bot source).

**3. A corollary worth stating: gunners and sentinels want opposite geometry.**
A gunner needs a clear lane and is degraded by our own construction; a sentinel is
indifferent to it and can therefore sit *behind* our own wall. Any ring that places
both by one rule is wrong for one of them.

## 4b. Gap closed: the shot does NOT damage the friendlies it passes through

**A gap in my own probe, surfaced by the third lane's finding that friendly fire is
real in this engine** (turret shots hit whatever unit stands on the **target** tile,
including own team). I had confirmed the sentinel's shot *lands* through friendlies
and **never checked whether it hurts them** — while upgrading `sentinel-file-stacking`
from `inference` to `documented` on that basis. If a sentinel's line damaged its own
file, the formation would be dead.

Re-run with HP recorded on every friendly in the line:

```
sentinel (3,6) facing EAST
  line: (4,6) friendly BUILDER_BOT · (5,6) friendly BARRIER · (6,6) enemy CORE
  FIRED -> enemy core 500 -> 482  (delta -18 = SENTINEL_DAMAGE)
  FRIENDLY ENTITIES ON THE LINE:
     BUILDER_BOT at (4,6)   40 -> 40   unharmed
     BARRIER     at (5,6)   30 -> 30   unharmed
```

**Pass-through friendlies take zero damage. The file formation survives and the
`documented` label holds.**

**The two facts are consistent and both matter:** a friendly on a **pass-through**
tile is unharmed; a friendly standing on the **target** tile would be hit. So a
sentinel file is safe, and a sentinel firing *at* a tile a friendly occupies is not.

## 5. Limits

- One map (fjordgate), one seed, one geometry per turret. These are engine rules,
  which should not be map-dependent, but I have **not** replicated across maps.
- The sentinel's friendly-blocking test used a barrier *and* a builder bot together
  in the real shot; the predicate test isolated the barrier only. **A friendly
  turret as blocker was not tested** — assumed equivalent to a barrier as both are
  buildings, but that is an assumption.
- Enemy entities as blockers were **not** tested for either turret. The gunner
  docstring says "builder bots and buildings" without qualifying team, so enemy
  blocking is expected but unverified.
- `can_fire_from` is a predicate; for the sentinel I confirmed with a real shot, but
  for the gunner's *blocked* case there is no shot to observe by construction —
  `can_fire` was False, so "no damage" is inferred from not firing rather than from
  a fired-and-absorbed shot.

## 6. Provenance

Probes: `probe_sentinel/main.py`, `probe_gunner/main.py`, `probe_idle/main.py` in the
s23 scratchpad. Both were run with a lane check first — a throwaway probe outside
`bots/` plus one local deterministic match is instrumentation, not the arena; the
builder arm concurred and asked that it be announced like any other run, which this
document does. **If Magnus reads that boundary more narrowly, this is the work to
revisit.**
