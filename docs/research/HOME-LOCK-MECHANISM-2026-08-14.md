# HOME-LOCK MECHANISM — why two-tile limit cycles form at OUR OWN core

**Agent-pipeline item 3 · 2026-08-14T15:39:02Z (`date -u`) · head `63d8811`**
**Population: ourver=125 (`bots/_v197mapcode`), the archived replay corpus.
READ-ONLY — no bot edited, no match run, nothing committed by this agent.**

---

## 0. HEADLINE, up front

**The dominant class is NOT a routing failure, and I could not make it one.**
Five candidate nav mechanisms were tested against controls and **all five were
refuted**. The one class that IS a mechanical defect — a builder sealed into a
free region of ≤8 tiles — is **10.7% of locks**, and it splits cleanly into a
**valkyrie-only terrain defect (37 bots, 100% of the terrain pockets)** and
**pockets we build around our own builders with our own conveyors (62 bots)**.

**⛔ AND THE MOTIVATING NUMBER NEEDS DEFLATING.** The "23× concentration at our
own core" (17.9% of never-acted locks within d²≤8 of our core vs 0.8% of
theirs) reproduces exactly — but **0.8% is not a null expectation, it is an
impossibility**. Our builders *spawn* at our core. A bot that locks before it
travels can only lock near our core; nothing in the game could place a
never-travelled builder near the *enemy* core. Of the 138 locked bots ending
within d²≤8, **32.6% are sealed pockets (real, fixable) and the remainder are
simply locks with early onset and zero travel** (median max-d² ever reached =
**9**). The asymmetry is mostly a spawn-location artifact, not a home-specific
mechanism.

**⚠ ROAD ALREADY WALKED TWICE.** `OSCLOCK` (two-tile-lock detector + repick)
finished **46.39** and `OSCLOCK2` (free the locked bot) **46.49/46.39** — both
DROPPED (`docs/coordination.md:46042,46607`). My class decomposition says why:
the detector frees a class-O bot back into the state that produced the cycle,
and it **cannot free a class-P bot at all** — that bot is physically walled in.
**Do not spend a third leg on "detect and repick".**

---

## 1. REPRODUCTION GATE — PASS, exactly

Recovered `nav_limit_cycle_census.py` and its outputs from the surviving
session scratchpads (`.../248fc65e-.../scratchpad`, `.../ee9072f0-.../scratchpad`).
A recovered script is a claim; the published headline was re-derived before any
new column was trusted.

| Published headline | Re-derived here | Verdict |
|---|---|---|
| 11.58% of builder-rounds locked | **11.58%** (183,489 / 1,584,948) | ✅ exact |
| 962–973 locked bots | **962** (1,160 games) / **973** (1,185-game rerun) | ✅ both |
| 39.6–39.8% never-acted | **39.81%** (383/962) | ✅ exact |
| median onset r67 | **68** (1,160-game file) / **67** (1,185 rerun) | ✅ |
| midgard 35.6% > ragnarok 14.1% > valkyrie 12.8% | **35.6 / 14.1 / 12.8** | ✅ exact |
| 17.9% vs 0.8% (never-acted, d²≤8 own vs enemy core) | **69/385 = 17.9%**, **3/385 = 0.8%** | ✅ exact |

**Two population snapshots exist and they are not interchangeable**:
`census_v125.withmap.jsonl` (1,160 games, carries `map`) is the one the
published headline came from; `census_v125.jsonl` (1,185 games, carries core
positions, no `map`) is a later rerun. Map cuts use the former, d² cuts the
latter, joined on `file`.

**Instrument check (tile indexing).** All downstream geometry depends on
`tiles[y][x]` vs `tiles[x][y]`. Positive control: **13/13 harvesters land on
ORE** under `[y][x]` vs **1/13** transposed. Negative control: the random-tile
ORE rate on that map is **1.3%**, so 13/13 is not an artifact of ore being
everywhere.

---

## 2. TRAJECTORY TABLE — 20 locked bots, d²_own ≤ 8, five maps

Full move traces + per-round surroundings decoded from `replay_archive/`
(`placeEntity` / `moveBuilderBot`), sampled across the lock window.
`reach` = generous static free-region from the lock tile (flood over walls +
both core footprints + all buildings; **builder bots deliberately not counted
as blockers**, so a small number means the bot genuinely cannot leave).
`partner` = another builder occupying the counter-tile in counter-phase.
`ore` = first free ore tile in `DIRECTIONS` order (the `eco.py:1232` override).

| # | map | replay | bot | tiles A↔B | reach | class | partner | ore | neighbours (mode over window) | acts |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | valkyrie | `a270de0d` | 11 | (25,14)↔(25,15) | **2** | P-terrain | none | none | WALL N, WALL W, own **core** E | — |
| 2 | valkyrie | `83d5e7e3` | 4 | (25,14)↔(25,15) | **2** | P-terrain | none | none | WALL N/W, own core E | — |
| 3 | valkyrie | `53a0df65` | 373 | (25,14)↔(25,15) | **2** | P-terrain | none | none | WALL N/W, own core E | — |
| 4 | valkyrie | `8f3b60ee` | 7 | (3,12)↔(3,13) | **2** | P-terrain | none | none | WALL N/E, own core S, own conveyor W | build 24, heal 3 |
| 5 | valkyrie | `ddc5554d` | 7 | (4,14)↔(4,15) | **2** | P-terrain | none | none | WALL N/E/S, own core W | heal 103 |
| 6 | valkyrie | `57418c0c` | 5 | (4,14)↔(4,15) | **2** | P-terrain | none | none | WALL N/E/S, own core W | — |
| 7 | valkyrie | `e9a0b91e` | 3 | (4,14)↔(4,15) | **2** | P-terrain | none | none | WALL N/E/S, own core W | — |
| 8 | fjordgate | `421bd359` | 4 | (4,8)↔(4,9) | **14** | P-pave | none | none | own conveyors E/N/S, own harvester W, ENEMY barrier | build 8, heal 35 |
| 9 | midgard | `92a58f58` | 794 | (26,28)↔(27,28) | 714 | **O** | none | none | own core N, own **sentinels** both flanks, S open | — |
| 10 | midgard | `f3bc4960` | 70 | (27,28)↔(28,28) | 779 | **O** | none | none | core N of A; **B has 4 free neighbours** | — |
| 11 | midgard | `7522a013` | 156 | (27,28)↔(28,28) | 697 | **O** | none | none | core N of A; B fully open | — |
| 12 | midgard | `64e15cdf` | 8 | (23,24)↔(24,24) | 783 | **O** | none | none | own builders N and S (transient, different ids) | build 3 |
| 13 | ragnarok | `694165af` | 118 | (1,1)↔(2,1) | 739 | **O** | none | none | own core S of B, rest open | — |
| 14 | ragnarok | `81b1b4b6` | 4 | (27,28)↔(28,28) | 702 | **O** | none | none | core N of A; B fully open | — |
| 15 | ragnarok | `b7338b48` | 8 | (28,25)↔(29,25) | 716 | **O** | none | none | own conveyors N/S, WALL W, map edge E | build 12 |
| 16 | ragnarok | `b717f0df` | 12 | (0,4)↔(1,4) | 716 | **O** | none | none | map edge W, own conveyors, ENEMY builder N | build 3, heal 39 |
| 17 | ragnarok | `7918b5a6` | 5 | (0,4)↔(1,4) | 724 | **O** | none | none | map edge W, own conveyors N/S/E | build 12 |
| 18 | ragnarok | `85f6cc87` | 5 | (0,4)↔(1,4) | 740 | **O** | none | none | map edge W, own conveyors | build 17 |
| 19 | auroraveil | `1defd749` | 374 | (11,3)↔(11,4) | 237 | **O** | none | none | WALL E/S of B, own conveyor W, ENEMY barrier | — |
| 20 | auroraveil | `273ca135` | 226 | (8,16)↔(8,17) | 260 | **O** | none | none | own core E, WALL N, ENEMY sentinel + barrier W | — |

**Dwell is exactly 1 in every window** — strict `ABABAB…` for the whole span
(bot 10: **953 consecutive rounds**, zero actions, on a tile with four free
neighbours). This is not a move-cooldown artifact; the bot moves every round it
is allowed to and chooses to reverse.

**The lock tiles are deterministic per map.** valkyrie `(25,14)↔(25,15)` in
**19 distinct games** and its mirror `(4,14)↔(4,15)` in **18** — one bot per
game, whichever side we are seated on.

---

## 3. CLASS COUNTS — and five refuted mechanisms

### 3.1 The classes that exist

Population-wide, **925 locked bots across 529 games** (every locked bot in
every game that has one; not a sample):

| class | definition | bots | share | locked-rounds | never-acted |
|---|---|---|---|---|---|
| **P — sealed** | static free region ≤ 8 tiles: the bot physically cannot leave | **99** | **10.7%** | 20,973 (11.8%) | **51.5%** |
| **O — open** | free region > 8 (median ~700): free to walk away, oscillates anyway | **826** | **89.3%** | 156,075 (88.2%) | 38.5% |

**Class P splits by what does the sealing** — and the split is clean:

| sealed by | bots | maps |
|---|---|---|
| **TERRAIN** (map walls + our own 2×2 core footprint alone) | **37** | **valkyrie 37, everywhere else 0** |
| **OUR OWN BUILDINGS** (conveyor/barrier paving) | **62** | midgard 30, fjordgate 10, auroraveil 5, archipelago 4, yulerune 3, antler 2, ragnarok 2, royale 1, drumlin 1, valkyrie 4 |

Pocket incidence **per game**: valkyrie **50.0%** (40/80 games lose ≥1 builder
this way), midgard 18.1%, fjordgate 13.5%, all maps pooled **7.1%** (82/1,160).

### 3.2 The five roads I closed

Each has a control that was driven to the other verdict; a check that never
produces the other answer has not been seen to check.

| # | hypothesis (task's classes in brackets) | test | result | verdict |
|---|---|---|---|---|
| 1 | **Two-bot mutual swap** [a] — each blocks the other alternately | for every round the bot is on A, is a *specific other builder* on B, in counter-phase? | **0 / 20**, `partner_frac = 0.00` in every case | ⛔ **REFUTED** |
| 2 | **Ore-magnet target flip** — `eco.py:1232` retargets to the first adjacent free ore in `DIRECTIONS` order, which differs between A and B | first free ore in the 8-neighbourhood of A and of B | **None / None in 20/20** — there is no free ore adjacent to either tile | ⛔ **REFUTED** |
| 3 | **Vision-limited replanning inconsistency** [b/d] — the planner's `blocked` set changes as the bot moves, so each step is locally optimal and they contradict | BFS *distance* (tie-break independent) to the goal under the blocked set the bot computes **while standing on A**, then on B; cycle iff both steps improve | **1 / 20** (and that 1 is the 14-tile enclosed pocket). Controls: **omniscient 0/20**, **physical 0/20** | ⛔ **REFUTED as dominant** |
| 4 | **Planner blindness** — `_bfs_direction` omits CONVEYOR, SPLITTER and BUILDER_BOT from `blocked`, all of which physically block | fraction of bot-rounds where **every** shortest-path first step under the planner's model is physically impassable | locked **21.1%** vs **control (non-locked) 24.1%** — control is *higher* | ⛔ **NOT DIAGNOSTIC** (but see §5.2 — the defect is real and large) |
| 5 | **Target supply exhausted / repick loop** [c] | free ore remaining on the map, and in the bot's vision, at lock onset | median **10 free ore of 16** still on the map; "no free ore in vision" locked **36.5%** vs **control 53.2%** — control again *higher* | ⛔ **REFUTED** |

**And the sealed-pocket class is itself not diagnostic population-wide**:
non-locked builders sit in ≤8-tile regions at **17.9%**, *above* the locked
rate of **10.7%**. A pocket produces **either** a stall (long dwell — excluded
by the detector's `MAX_DWELL = 2`) **or** a 2-cycle. Class P is a real defect
worth fixing; it is not what separates locked from unlocked.

### 3.3 What DOES separate locked from non-locked

| feature | locked (n=925) | non-locked (n=6,591) |
|---|---|---|
| **never acted in its whole life** | **39.9%** | **12.2%** |
| median max d² ever reached from our core | **80** | **148** |
| lock rate by role seat (seat = spawn order; `main.py:314`) | seat 1 (first expander) **18.6%** · seats 2–3 **12.1/12.2%** · seat 0 (raid) **9.7%** · seat 4 (defend) **8.8%** | — |

The locked bot is one that **travels less and does less**. Median lag from
spawn to lock onset is 49 rounds, so most do walk somewhere first — then stop.

### 3.4 Why the cycle never ends, verified from source

`self.stuck` is incremented at **exactly one place in the tree** —
`bots/_v197mapcode/eco.py:747` (= `_v223sealrepair/eco.py:910`), the tail of
`_nav`, reached only when the desired move **and all three fallbacks fail**:

```
if self._move(ct, desired, pave): return
for d in (perp1, perp2, opposite):
    if self._move(ct, d, pave): return
self.stuck += 1
```

Both escape hatches key on that counter — `eco.py:1055` (`stuck >= 5` → repick)
and `raid.py:215/217` (`nav_fail >= 8` → ban station). **A two-tile oscillation
is made entirely of SUCCESSFUL moves, so `stuck` stays 0 and neither hatch can
ever fire.** That is why every mechanism above, whichever fires, is *terminal*
rather than transient. `doctrine.py:1425` records the opposite failure (the
detector counting productive work as stuck); **the false-negative direction —
an oscillation is invisible to it — is not recorded anywhere.**

This is also the exact gap `OSCLOCK`/`_v224osclock2` closed, and it screened
**negative twice**. Closing it is necessary and demonstrably not sufficient.

---

## 4. MAP-GRADIENT CONSISTENCY CHECK — partially, and it names a better segment

| map | lock % of builder-rounds | class O | class P | pocket games | seat-1 lock rate |
|---|---|---|---|---|---|
| midgard | **35.6%** | 86.5% | 13.5% | 18.1% | 27.7% |
| archipelago | 15.8% | 95.4% | 4.6% | 3.9% | 42.9% |
| ragnarok | **14.1%** | **98.2%** | **1.8%** | **2.4%** | 35.7% |
| valkyrie | **12.8%** | 48.1% | **51.9%** | **50.0%** | 20.0% |
| drakkarfjord | 11.0% | 100.0% | 0.0% | 0.0% | 2.6% |
| fjordgate | 8.0% | 74.4% | **25.6%** | 13.5% | 13.5% |
| icefloe | 3.2% | 100.0% | 0.0% | 0.0% | 7.6% |

**Is the gradient explained by the mechanism? Only in part, and honestly: no
for the dominant class.** The gradient is carried by class O on every map
(86–100%) except valkyrie and fjordgate, and I have no confirmed mechanism for
class O. Midgard leads the gradient with 86.5% class O.

**But the gradient and the POCKET defect are almost orthogonal, and that
matters for registration.** valkyrie is only 3rd on lock-rate yet 1st on
pockets by a factor of ~20; ragnarok is 2nd on lock-rate and has essentially
**no** pockets (2 bots in 84 games).

⇒ **`lock-heavy = {midgard, ragnarok, valkyrie}` is the WRONG primary segment
for a pocket fix and would dilute it.** Per Obligation 15a's own rule ("a
mechanism-specific segment beats a size class whenever the mechanism names a
terrain property"), the mechanism names *a sealed spawn-ring or paved-in free
cell*, which gives **pocket maps = {valkyrie, midgard, fjordgate}** — 81 of 99
class-P bots and 67 of 82 pocket games. This is a proposed correction to the
segment vocabulary at
`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md:424`.

---

## 5. PROPOSED MINIMAL CHANGE

### 5.1 PRIMARY — `SPAWNPOCKET`: never put a builder in a cell it cannot leave

**Why this and not another oscillation detector:** it is the only class my
evidence confirms mechanically, and it is **the one class `OSCLOCK` could not
have fixed by construction** — you cannot free a bot from a sealed pocket, so
those bots sat in OSCLOCK's treatment arm as pure dilution.

Two halves, both outside `_bfs_direction` (which is the finding — the dominant
class is not fixable there):

**(a) Terrain half — the core's spawn-tile chooser.**
`bots/_v223sealrepair/main.py`, the `cands.sort(key=…)` immediately before the
`can_spawn` loop (= `_v197mapcode/main.py:284-301`). Add a precomputed-once
free-region size as the **leading** sort key, so a pocket tile is demoted to
last resort rather than banned (never lose a legal spawn):

```python
# region size over STATIC terrain + our own footprint, flooded once per match
cands.sort(key=lambda sp: (0 if self._region_size(sp) > POCKET_MIN else 1,
                           (sp.x*17 + sp.y*31 + self.n*13 + self.spawn_salt) % 97,
                           sp.y, sp.x))
```

`POCKET_MIN = 8`. One cardinal flood per ring tile, cached — MAPCODE-class:
map-keyed, deterministic, zero recurring CPU. Fixes **37/37 terrain pockets,
all on valkyrie, at 50% of valkyrie games**.

**(b) Pave half — stop walling our own builders in.**
`bots/_v223sealrepair/eco.py:934-954`, the `readable` pave branch of `_move`.
Refuse the pave when laying that conveyor would leave an orthogonally adjacent
friendly builder with ≤1 free exit. Addresses the **62 pave-sealed** bots
(midgard 30, fjordgate 10) and composes with §5.2.

**Composition, not competition, with the queued arm.** The same region
precomputation gives `RETIRE60` (`_v234retire60`,
`docs/coordination.md:48250`) a *provable* retirement predicate for class P:
a bot in a ≤8-tile sealed region with zero lifetime actions can never become
employable, so retiring it reclaims its +20% scale with no judgement call.
**51.5% of class-P bots never act.**

**Registration-ready line (Obligation 15a/15b):**

```
MAP SEGMENT: pocket maps {valkyrie, midgard, fjordgate} — the mechanism is a
spawn-ring or paved-in free region of <=8 tiles; these three carry 81/99
class-P bots and 67/82 pocket games, while the 12 other maps carry 0.4 pocket
bots per 100 games. EXPECTED DIRECTION: POSITIVE on the segment, ~ZERO off it.
PRIMARY SEGMENT: pocket maps (single primary, 15b). Descriptive only: the
lock-heavy set {midgard, ragnarok, valkyrie} — ragnarok is explicitly NOT in
the primary segment (2 pocket bots / 84 games) and including it dilutes.
Bars: kill-round non-regression (DEFENCE_ADMISSION_BAR) + scale curve read
beside the build-count curve.
```

**⚠ Size it honestly before firing.** Pooled, this is 7.1% of games losing one
builder; on valkyrie it is 50% of games. **This is a segment-conditional
MAPCODE ship, not a pooled 51-bar clearer**, and it should be registered that
way or it will read as a null exactly like `OSCLOCK`.

### 5.2 SECONDARY — `BELTBLIND`: the defect this investigation actually found

Not the lock fix (control-matched, §3.2 row 4) — but the largest measured
routing defect in the tree, and it lands **exactly** in the function the task
named. `bots/_v223sealrepair/eco.py:829-833` lists
`GUNNER, SENTINEL, LAUNCHER, HARVESTER, BARRIER` and **omits CONVEYOR and
SPLITTER**, which physically block movement.

Measured over 8,731 locked and 8,889 control builder-rounds: in **21.1% /
24.1%** of rounds **every** first step on the planner's own shortest path is
physically impassable, and **64.1% of those blockers are our own conveyors**
(35.9% our own builder bots). So roughly one builder-round in four is spent
walking a plan that cannot be executed, on every map (`ALL_BLOCKED` ranges
3.6% drakkarfjord → 39.8% fjordgate). Tempo is the currency (kill round), so
this is worth its own leg.

**⚠ Not a free change.** Adding conveyors to `blocked` makes the plan correct
but can make a target unreachable, at which point `_bfs_direction` falls back
to `p.cardinal_direction_to(target)` — worse than today's accidental
plan-through-and-sidestep detour. Any such arm needs a goal-relaxation path
before it is fired, and that is a design question, not a two-line change.

```
MAP SEGMENT: none expected — the mechanism is our own belt geometry, which we
build on every map; ALL_BLOCKED is nonzero on all 15 (3.6%-39.8%).
EXPECTED DIRECTION: positive everywhere, larger where our trunk is longer.
```

### 5.3 What I recommend AGAINST

**A third "detect the 2-cycle and repick" leg.** `OSCLOCK` 46.39 and
`OSCLOCK2` 46.39/46.49 already tested it; §3.2 refutes every mechanism a
repick would address for the 89.3% class-O majority, and §3.3 says the locked
bot's distinguishing feature is that it **never acted** (39.9% vs 12.2%), not
that it could not find a route. A bot with nothing to do, freed, has nothing
to do. **The employment/retirement arm already queued is the better customer
for this evidence than any nav arm.**

---

## 6. METHOD AND ARTEFACTS

All work in `…/a9e77d8e-…/scratchpad` (session-local, not committed):
`traj.py` (trajectory + surroundings decode), `reach.py` (static reachability
flood), `bfs_sim.py` (faithful `_bfs_direction` model + replanning-cycle test
with omniscient and physical controls), `invisible.py` (planner-blindness test
+ non-locked control), `popclass.py` (population class census + control),
`seats.py` (role-seat / travel features), `oresupply.py` (target-supply test +
control). Wire helpers reused from `tools/replay_census.py`; the lock detector
(`analyze_bot_lock`, `find_windows`, `MIN_SPAN=50`, `MAX_DWELL=2`) reused
**unmodified** from the recovered `nav_limit_cycle_census.py`.

**Caveats, stated rather than buried.**
1. Every number is **us-only**, on **ourver=125** archived replays.
2. The class-O mechanism is **unidentified**. Five candidates are refuted; I do
   not have a sixth confirmed. Treating §5.1 as a fix for the 89.3% would be
   a misreading of this document.
3. `us_side → replay team index` uses the standing `a→0, b→1` mapping inherited
   from the recovered script; it is not independently re-verified here.
4. The `_pick` / `_raid_station` target-selection paths were read from source
   but **not** confirmed live — per point 6 of the standing brief, that makes
   any statement about them a hypothesis. Nothing in §3.2's refutations depends
   on them; §3.4 is a source fact (a counter incremented at one site), not a
   behavioural inference.
