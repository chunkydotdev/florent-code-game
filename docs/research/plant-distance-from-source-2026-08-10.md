# Plant distance: the d² finding is HALF WRONG and the surviving half is a one-constant plank

**Research arm, 2026-08-10.** Read against
`docs/research/league-fast-kill-mechanism-2026-08-10.md` (dbe411e, side lane),
which reduces fast killing to **d²(turret → enemy core)** and reports fast
killers planting at **d²=8** (Cookie) / **d²=10** (PEA gunners) against **our
d²=32 on sentinels and d²=16 on gunners**, flagging the gunner figure as a
possible bug because gunner range is r²=13.

**This is a SOURCE read of `bots/_v127loki10`, not a replay statistic.** It
settles the measurement-basis question I raised against that doc without needing
an engine probe, and it converts one half of the finding into a build.

## The answer in six lines

1. **The gunner alarm is wrong on its PREMISE.** Our forward emplacement is
   **SENTINEL-ONLY, by deliberate design** (`raid.py:389`). Gunners are never
   planted to shoot the enemy core.
2. So a **d²=16 gunner-to-enemy-core** figure measures a turret that was never
   aimed at that core. It is the home/counterbattery gunner
   (`main.py:548-581`), sited against a **local threat**.
3. **That siting is engine-checked, not heuristic**: it gates on
   `ct.can_fire_from(bp, facing, turret_type, threat)`. A gunner is planted only
   where the ENGINE says it can fire at its own target. There is no range bug.
4. **The d²=32 sentinel figure is REAL, and it is the range BOUNDARY**
   (sentinel r²=32). It is produced **by construction**, not by choice.
5. **The mechanism is scan order**: `raid.py:425-445` builds on the **first**
   `(direction, core-tile)` pair satisfying `bp.distance_squared(target) <= 32`.
   **First legal site wins. Nothing scores distance.**
6. **The plank is one constant** — plant at d² ≤ K instead of at first
   opportunity. See §4.

## 1. Forward turrets are sentinels ON PURPOSE — the gunner comparison is void

`raid.py:389-403`, `_try_forward_sentinel`, docstring verbatim from the tree:

> "SENTINEL, not Gunner, and not as a preference: the collar blocks LOS,
> so a Gunner built to shoot the Core would be shooting our own barriers."

A gunner's shot is **blocked by obstacles**; a sentinel's **ignores them**. Our
own barrier collar sits between our forward emplacement and their core, so a
forward gunner is structurally useless *for us specifically*. **Any cross-team
comparison of gunner-to-core distance therefore compares our counterbattery
gunners against their kill gunners — different objects with different jobs.**

**Consequence for the parent doc:** PEA's gunners at d²=10 and our gunners at
d²=16 are not the same measurement. The correct comparison for us is
**sentinel-to-core**, and the correct question about their gunners is whether
their approach lacks an LOS-blocking collar — which is a property of *their*
build, not of distance.

## 2. The basis question I raised is already answered correctly IN OUR CODE

I asked whether d² was measured to the core's centre or to its nearest occupied
tile, since the core is 2×2 and the two give opposite verdicts near the range
constants. **Our source uses the nearest-TILE basis throughout:**

* `raid.py:418` — `tiles = core_tiles(E)` (all four tiles, from `eco.py`).
* `raid.py:421` — `min(p.distance_squared(c) for c in tiles)`.
* `raid.py:432-433` — iterates `for target in tiles` and tests each.

So **our** side of the comparison is tile-based. **The parent doc must still
state its own extraction basis** — if it measured to centre, its opponent
figures (d²=8, d²=10) are not comparable to our tile-based d²=32/16, and the
whole ranking needs recomputing. **That check is still owed; this document does
not discharge it.**

## 3. Why we sit at exactly the boundary — it is scan order, not doctrine

`raid.py:425-445`, the emplacement loop, reduced to its control flow:

```
if min(p.distance_squared(c) for c in tiles) > 50: return False   # approach gate
for d in CARDINALS:
    bp = p.add(d)
    for target in tiles:
        if bp.distance_squared(target) > 32: continue             # range gate
        if not can_fire_from(bp, facing, SENTINEL, target): continue
        if not can_build_sentinel(bp, facing): continue
        build_sentinel(bp, facing); return True                   # FIRST HIT WINS
```

Three facts follow, and they are structural rather than statistical:

* **The approach gate admits the builder at d² ≤ 50**, well outside sentinel
  range (32). The builder is therefore *already scanning* while still too far.
* **The range gate accepts anything ≤ 32.** It does not prefer smaller.
* **The loop returns on the first success.** No candidate is scored, none is
  compared, and the builder never waits for a better one.

**So the first tile that becomes legal as the builder walks in is the tile we
build on — and by construction that is the outermost legal tile, d² ≈ 32.**
The side lane measured d²=32; that is the boundary reproducing itself. **Our
observed plant distance is not a decision the bot makes. It is the first moment
the bot is allowed to act.**

## 4. THE PLANK — one constant, and it is the smallest thing that could work

Add a plant-distance gate so the emplacement is taken **deep** rather than at
first opportunity:

```
if bp.distance_squared(target) > PLANT_DSQ_MAX: continue    # PLANT_DSQ_MAX < 32
```

or equivalently score candidates and take the minimum instead of the first.
**The lever is not the scan order alone** — because `bp = p.add(d)` is pinned to
the builder's own position, tightening the gate makes the builder *keep walking*
until a closer site qualifies. That is the intended behaviour and it is why one
constant is enough.

**Pricing, stated honestly and NOT as a prediction of gain:**

* **What it buys, if the parent doc's association is causal:** the fast-killer
  band is d²=8-10. Moving from 32 toward ~10 puts more of the core's four tiles
  inside a single sentinel's reach and shortens the line, which is where a
  single-tile-wide shot is least sensitive to misalignment.
* **What it costs, and this is a real cost:** the builder must walk further into
  their base before it may build, so it spends more rounds exposed and may die
  before planting anything. **A tighter gate can therefore produce FEWER forward
  sentinels, not closer ones** — that is the falsifier, and it must be measured
  as *sentinels planted per game*, not only as plant distance.
* **Currency:** `core_kill_share` and `time_to_core_kill`. On-programme —
  this is about killing their core faster, not about holding ours.

**MECHANISM vs MARKER, unresolved and flagged:** the parent doc establishes that
fast killers plant close. It does not establish that planting close *causes*
fast kills — teams that plant at d²=8 may simply be teams that already achieved
map control. **This plank tests the causal direction directly**, which is its
main value beyond any expected gain, and a null would be informative.

## 5. What this document does NOT establish

* It does **not** verify the parent doc's opponent figures. I read our source,
  not their replays. If their extraction basis is centre-based, §1 and §3 stand
  (they are about our code) and the numerical comparison does not.
* It does **not** measure how often `_try_forward_sentinel` actually fires, what
  distance it achieves in play, or whether `LOKI_FWD_GUN_CAP` binds first.
  **Everything here is control-flow, not behaviour.**
* It does **not** price the plank. The arithmetic above is a mechanism sketch
  with its falsifier named; it is not a costed estimate and must not be quoted
  as one.
* The tree read is `bots/_v127loki10` at working-tree state on 2026-08-10, which
  had **uncommitted modifications** at the time of reading (queue item 1, the
  LOKI-10 wiring pass). Line numbers may move.
