# LOKI-2 — destroy / cost-scale pruning

Fork of `_v103split` (proven incumbent chassis). Adds `prune.py`; `main.py` and
`doctrine.py` are otherwise byte-identical to `_v103split` apart from 14
non-comment lines at five sites marked `LOKI-2`.

**STATUS: BUILT AND INSTRUMENTED, NOT ARENA-MEASURED.** The box was reserved
for a field battery. Every number below comes from single `fcode run` games and
from offline replay parsing, never from an arena leg. Single games in this
project are near-worthless for strength (`tools/arena.py` docstring: identical
bots have finished 0-units vs 10 on variance alone) — they are used here only
for *mechanism* counts (how often did the code fire, did it crash), which is
what they can support.

**Headline: the doctrine I was briefed to build is second-order and did not
show an effect. The thing I found while building it — our conveyors feeding the
ENEMY network — is larger and is measured below.**

---

## 1. The pruning rule, in five lines

1. On every builder turn, look at the 4 cardinal neighbours only. No BFS, no
   map-wide scan, no wiredness flood.
2. A friendly **CONVEYOR** at `T` facing `f` is a **DEAD HEAD** if `T.add(f)`
   is readable and holds neither a friendly conveyor/splitter nor our Core
   footprint. A conveyor has exactly one output, so this is a *sufficient*
   condition — no false positives on a tile we can actually see.
3. Destroy only after the tile has been **continuously observed** dead for
   `PRUNE_CONFIRM_RNDS = 100` (ambiguous class) or `4` (leak class: the output
   tile holds an **enemy** relay/Core, where "lane under construction" cannot
   be the explanation).
4. Conveyors only; never loaded (the stack is incinerated) unless it is the
   leak class; never within `dist_core <= 1`; never a tile in this unit's own
   `link_queue`; never adjacent to one of our harvesters.
5. One shot per tile per unit, `PRUNE_MAX_TOTAL = 20` per unit, `2` per round,
   and a per-unit condemned set that blocks this unit's own linker and both
   pave sites from rebuilding what it just tore down.

Ablate with `PRUNE_ON = False` in `prune.py` → behaviour is `_v103split`.

---

## 2. Grep result: `destroy()` call sites in `_v103split`

```
$ grep -rn "ct\.destroy\|can_destroy\|\.destroy(" bots/_v103split/
(no matches — exit 1)
```

**Zero.** `grep -c destroy` returns 8 hits in `doctrine.py` and 2 in `main.py`,
and **all ten are prose inside comments**. Confirms the brief. Across the whole
`bots/` tree only 7 files ever call it (`ouroboros_probe`, `_ouro_v2_dev`,
`_ouro_v3_dev`, `_v70ec`, `_v80e6d_tb`, `_v83u`, `_v86z2`) — none in the live
lineage.

## 3. Engine facts this is built on

* `destroy()` — allied building, orthogonally adjacent, no titanium, no
  cooldown, unlimited per turn; consumes neither the action nor the move.
* **Cost scale is ONE GLOBAL multiplier over LIVE entities**, not per-category:
  `scale = 100 + Σ(live entity rates)`, every getter is `floor(scale × base)`,
  and a destroy drops it the same round. So one orphan conveyor taxes every
  future harvester/gunner/sentinel/launcher/builder by 1%, not just conveyors.
* `destroy()` **INCINERATES** an in-transit stack (0 Ti in 191/191 measured).
  Not a refund. `PRUNE_LOADED_ON = False` because of this.
* Scale tracking live entities means enemy churn imposes **no** permanent tax —
  there is no offensive arm here, by design.

## 4. What the pruning actually did (bot-side instrumentation)

`PRUNE_DEBUG = True`, seat A = `_v106loki2`, seat B = `_v103split`, seed 3,
one game per map, `--tle 10`, run **one at a time** on an otherwise idle box.

| map | turns | destroys | distinct tiles | leak-class | dead-head class | crashes | CPU-guard trips |
| --- | --- | --- | --- | --- | --- | --- | --- |
| meander | 1000 | 13 | 9 | 13 | 0 | 0 | 0 |
| atoll | 1000 | 2 | 2 | 2 | 0 | 0 | 0 |
| heart | 1000 | 2 | 2 | 2 | 0 | 0 | 0 |
| nordkap | 1000 | 2 | 2 | 1 | 1 | 0 | 0 |
| saga | 199 | 0 | 0 | 0 | 0 | 0 | 0 |

**Median 2 destroys per game.** Against a live scale of 300-590% that is a
~2-point shave, i.e. a **<1% discount** on future builds. The brief's target
set (18 orphans on heart) is a *global replay census*; the locally provable,
locally *reachable* subset is one to two orders of magnitude smaller.

**Why — and this is a structural limit, not a tuning problem.** `destroy()`
requires orthogonal adjacency, and the confirm clock requires *continuous*
observation. Orphans and leaks sit on walking trails and on the contested seam,
where a builder is adjacent to any given tile for one or two rounds in passing.
The tiles a builder *does* loiter beside for 100 rounds are the tiles it is
actively working on — i.e. precisely the ones that are **not** orphans. The
rule is sound; the sensing geometry adversely selects against it.

### Self-corrections made during the build

* **Cascade accelerator: built, measured, deleted.** "Output tile is one I
  condemned → unambiguous, short clock" assumed our rebuild gates stop the lane
  regrowing — but those gates are per-unit, and a teammate's linker/pave
  rebuilds freely. Measured on heart seed 3: it produced 13 of 16 destroys and
  drove a three-unit relay on tiles (13,16)/(14,16) — destroy at r426, r430,
  r435, r439, r443, r446. Removed.
* **`PRUNE_CONFIRM_RNDS` 25 → 40 → 100.** At 40, teammates rebuilt several
  pruned tiles within a few rounds; 40 rounds does not separate "orphan" from
  "lane whose builder got pulled into a heal or a chase".

---

## 5. THE ACTUAL FINDING — cross-team titanium leak

While classifying destroy targets, the dominant class turned out not to be dead
scale weight but **our conveyors pointing into the ENEMY's network**: 44 of 57
destroys across five games. That is not merely wasted scale — it is titanium we
mined being delivered to the opponent.

Quantified offline against the **ladder replay archive** (real matches, real
opponents), by replaying `DistributeResources` moves with per-round tile
ownership and counting moves whose `from` tile is owned by one team and `to` by
the other. Parser validated two ways: the identity `own_core_moves × 10 ==
titaniumCollected` held **40/40 replays on both sides**, and independent
entity-count cross-validation against `tools/replay_census.py` gave **0
mismatches on 12 replays**.

**40 replays, 80 team-sides:**

| | value |
| --- | --- |
| team-sides with any cross-team leak | **65/80 (81%)** |
| games with leak on at least one side | 34/40 (85%) |
| Ti leaked per team-side | median **55**, mean **256**, max **3,650** |
| leaked Ti landing **directly in the opponent's Core** | **4,390 / 20,460 = 21%** |

It scales hard with map size, i.e. with network size:

| map size | n (team-sides) | mean Ti leaked | nonzero |
| --- | --- | --- | --- |
| 26x26 | 14 | **500** | 13/14 |
| 24x24 | 12 | **462** | 10/12 |
| 25x15 | 8 | 294 | 8/8 |
| 25x25 | 14 | 223 | 13/14 |
| 16x16 | 14 | 117 | 12/14 |
| 28x20 | 10 | 42 | 6/10 |
| 20x26, 14x18 | 4 | 0 | 0/4 |

**It concentrates on the seam, not on scatter.** In every high-leak game
inspected, two adjacent tiles (one owned by each team) carried the large
majority of the game's leak — e.g. 4,050 of 5,060 Ti (80%) on one 24x24 map,
3,630 of 3,930 (92%) on a 26x26. This is two opposing networks abutting near
the symmetric midline and pushing stacks across the boundary.

Worst single case in the sample: one team-side leaked **10,000 Ti**, of which
**6,730 went straight into the opponent's Core** — scoring their tiebreak #1.

### Did the pruning plug it? No.

Paired *within-game* comparison (same match, seat A = pruning ON, seat B =
pruning OFF), replay-measured:

| map | A leak (pruning) | B leak (no pruning) |
| --- | --- | --- |
| meander | 1,140 | 3,310 |
| atoll | **2,230** | 180 |
| heart | 420 | 220 |
| nordkap | 100 | 70 |
| saga | 20 | 20 |

One of five favourable, two unfavourable, two neutral — and seat A/B is not a
symmetric comparison. **No effect.** Consistent with §4: 2-13 destroys per game
cannot plug a seam that is continuously rebuilt by our own trail pave.

*(A `_v103split` vs `_v103split` control was also run but is unusable: those
games ended early on core kills — 146-281 turns, 700-2,600 Ti collected — so
they had far less time to leak. Leak is roughly proportional to game length ×
network size, so any comparison must control for both. Noted so nobody reuses
those rows.)*

### And an important correction to the leak's value

Destroying a leaking head is **denial, not recovery.** A conveyor has one
output; if it fed the enemy, the whole chain behind it was feeding the enemy,
so we were never going to collect that titanium. Destroying it stops *their*
income; it does not add to ours (the upstream chain now dead-ends and strands).
That is still worth having — the primary tiebreak is titanium delivered, and
Elo here is game-share — but it must not be booked as income.

---

## 6. Second arm: leak prevention at BUILD time — WIRED, DEFAULT OFF, UNMEASURED

`PRUNE_LEAK_BUILD_GATE_ON` (default `False`) refuses to lay a conveyor whose
output tile already holds an enemy relay or the enemy Core, at all three build
sites. Rationale: the destroy arm needs a builder to loiter next to the leak;
*not creating* the leak has no adjacency requirement at all, because the
builder is by definition standing next to the tile it is about to build on.

**Do not enable without a full battery.** Three single games gave
`a_titanium_collected` of 350 / 10,520 / 6,620 (heart / nordkap / meander)
against 7,240 / 2,470 / 16,030 for the same map+seed with the gate off —
i.e. one catastrophic, one much better, one much worse. That spread is exactly
the variance this project's own tooling warns about; **it is not evidence in
either direction.** It touches the economy bootstrap, which is the one thing
that must not break.

It is also only half a fix: it addresses the case where *we* build into *them*,
and is blind by construction to the case where they extend their network onto
a tile our conveyor already faces. Which half dominates is unknown.

---

## 7. Safety

* **Crashes: 0** and **CPU-guard trips: 0** across all 14 single games run
  (5 instrumented + 3 arm-2 + 3 smoke + 3 earlier probes), both arms, on 6 maps.
* Every `destroy()` is gated on `can_destroy()`.
* The whole subsystem sits behind its own blanket `try/except Exception` in
  addition to `run()`'s, because an escaped exception permanently deletes the
  unit.
* Every tile read is individually wrapped and **fails safe to "not an orphan"**
  (`get_tile_building_id` raises for an in-bounds tile outside vision).
* CPU: the sweep re-checks `_cpu_exhausted` before doing anything and sits
  after `_builder`'s existing CPU boundary, so it can never eat the emergency
  defense paths. Worst case ~60 engine calls in a round with two destroys;
  typical 4-12 (most neighbours are empty and cost one call). For scale,
  `_try_counterbattery` already budgets up to 64 `can_fire_from` probes.
* **A CPU overrun produces no crash and no traceback** — it silently truncates
  the turn. The arena's crash counter cannot see it. The 0 CPU-guard trips
  above are from an idle box; they say nothing about a contended one.
* No new comm-store slot: all 16 are occupied in `doctrine.py`. All state is
  per-unit instance state, read and written only by its owning unit.
* Pruning conveyors opens no lane for raiders: conveyors are bot-passable
  already. Barriers — the only relay that blocks movement — are excluded.

## 8. Honest verdict

**Do not ship this for the cost-scale story.** Median 2 destroys per game
against a 300-590% scale is a sub-1% discount, which is far below what an arena
battery could resolve, and it carries a real (if bounded) rebuild-churn cost.

The doctrine is *safe* — it is ready for a battery if someone wants the number
— but the mechanism count says the ceiling is low, and the reason is structural
(adjacency + continuous observation adversely selects against real orphans).

**The leak is the finding worth acting on**: 81% of team-sides leak, mean 256
and up to 3,650 Ti per team-side, 21% of it landing in the opponent's Core, and
it concentrates on two seam tiles per game. That is a build-placement problem,
not a destroy problem, and §6 is the shape of the fix — unmeasured, and needing
a proper battery plus probably a smarter response than "refuse the build".

---

## CORRECTION APPENDED AT THE s22 WRAP (builder arm) — read this before §5

**§5 OVERSTATES THE LEAK.** It reports mean 256 / max 3,650 without the
core-landing **median** beside it. The correct headline:

```
titanium landing IN the enemy Core, per team-side per game
  median 0   (ZERO in 70% of team-sides)
  mean  54.9 on this build's 80-side sample
  68% of the entire total comes from TWO sides out of eighty
research's independent flow census over 1,165 ladder games: mean 5.8, median 0
```
**It is a thin tail on large maps, not a steady drain.** The apparent 10x
conflict between this build and the research arm was **a mean paired against the
median of a DIFFERENT metric** (total boundary crossings vs core-landing); on the
comparable metric both medians are 0 and there was never a conflict.

**AND THE DEFINITION CORRECTION, adopted across both arms: plugging a leaking
conveyor head is DENIAL, NOT RECOVERY.** A conveyor has exactly one output, so
the chain behind a leaking head was feeding them all along — **we were never
going to collect that titanium.** Destroying it stops THEIR income and adds
nothing to OURS. Do not book the leak as recoverable revenue.

**Together these lower the leak's expected value materially below what this
document's body implies.**

**VERDICT ON THIS BUILD (s22): DO NOT SHIP THE SCALE ARM.** Median 2 destroys per
game against a 300-590% live scale is a sub-1% discount — below what a battery
can resolve — and the cause is **structural, not tunable**: `destroy()` requires
orthogonal adjacency plus continuous observation, so we can only prune tiles a
builder loiters beside, which are precisely the tiles it is actively working on,
i.e. **not orphans**. The "18 of 40 orphaned relays" that motivated this build is
a GLOBAL census; the locally reachable subset is 1-2 orders of magnitude smaller.

The second arm (`PRUNE_LEAK_BUILD_GATE_ON`, gating where we BUILD rather than
what we destroy) remains wired, **default OFF, and unmeasured** — three single
games gave 350 / 10,520 / 6,620 Ti against 7,240 / 2,470 / 16,030 with it off,
which is variance, not evidence. **If anything here is ever measured, measure
that arm, not the scale arm.**
