# SCREEN PREREG — SEATSCAN: seat-relative `CARDINALS` scan order on the v140 chassis (QUEUE #8)

**STATUS: committed BEFORE the `SEATSCAN` shard's first row exists** (two-clock:
this file's git author time vs the first `SEATSCAN` row's timestamp in
`scratchpad/overnight/SEATSCAN.tsv` / `scratchpad/corefill.log`; the side lane
certifies the pair). No row of this shard exists at commit time — the shard key
`SEATSCAN` appears **0 times** in `scratchpad/corefill_work.txt` at draft — and
none may be read before it does. Drafted 2026-08-14T21:13:20Z (`date -u`, same
shell call), repo at `59cc5406`.

**PROVENANCE: docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md · QUEUE.md (row #8, line 462) · tests/test_seat_relative.py · tools/prereg_check.py · bots/_v223sealrepair/doctrine.py · bots/_v223sealrepair/main.py · bots/_v223sealrepair/eco.py · bots/_v223sealrepair/raid.py · bots/_v216seatrel/doctrine.py · bots/_v216seatrel/main.py · bots/_v151seatrel/doctrine.py · bots/_v197mapcode · bots/_v198null125 · tools/overnight.sh · tools/overnight_read.py · tools/map_encode.py · docs/prereg/SCREEN-sealfloor6-2026-08-14.md · docs/prereg/SCREEN-seatrel-2026-08-14.md · docs/prereg/RULE-futility-gates-2026-08-13.md · docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md · docs/research/CLOSED-BY-LEG-INDEX-2026-08-14.md · scratchpad/corefill_work.txt · scratchpad/overnight-remote/worker@work-server-1/worklist.txt · scratchpad/overnight/NULL114.tsv · scratchpad/overnight/NULL123.tsv · scratchpad/overnight/NULL125.tsv · scratchpad/overnight/NULLSALT.tsv · scratchpad/overnight/SHIPGATENULL.tsv · scratchpad/overnight/SEATREL.tsv · scratchpad/_seatrel_dose.err · maps/*.map26**

Drafted by a FRESH agent with **no inherited session context** beyond the item
brief. Four measurements were made by this agent and are marked ⭐MEASURED
wherever they appear; everything else is quoted from the files above.
**No row of the SEATSCAN shard exists and none was read.**

---

## 1. THE ARM — one function, one call site

**TREATMENT `bots/_v240seatscan`** = `bots/_v223sealrepair` (v140, the LIVE
incumbent and the CONTROL) plus the `_v151seatrel`/`_v216seatrel` plank ported
verbatim. **Two hunks, both ADD-only:**

```
bots/_v240seatscan/doctrine.py   AFTER line 26  (after `CARDINALS = [...]`)   +22 lines
+
+SEAT_RELATIVE_SCAN = True
+
+def orient_cardinals(core, enemy):
+    """Rotate CARDINALS in place to start at the cardinal facing ``enemy``."""
+    if not SEAT_RELATIVE_SCAN or core is None or enemy is None:
+        return
+    dx, dy = enemy.x - core.x, enemy.y - core.y
+    if abs(dx) >= abs(dy):
+        first = Direction.EAST if dx > 0 else Direction.WEST
+    else:
+        first = Direction.SOUTH if dy > 0 else Direction.NORTH
+    base = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
+    i = base.index(first)
+    CARDINALS[:] = list(base[i:] + base[:i])

bots/_v240seatscan/main.py       AFTER line 167 (after the SLOT_ENEMY_CORE write)  +1 statement
+        orient_cardinals(self.core, enemy_core_for(w, h, self.core))
```

**OLD → NEW, stated as the single behavioural fact:** `doctrine.py:26`
`CARDINALS = [NORTH, EAST, SOUTH, WEST]` is a **fixed ABSOLUTE order** in the
control and stays that literal in the treatment; the treatment **rotates the
same list, in place, once per Core turn, so that element 0 is the cardinal
facing the enemy core.** No literal is edited. No consumer is edited.
`main.py` already imports `orient_cardinals` via `from doctrine import *`
(`main.py:28`) and already computes the enemy anchor at `main.py:167`, so the
call site needs no new import and no new computation.

**Verified at draft, not asserted:**
* The ported function body is **byte-identical** to `_v151seatrel/doctrine.py:91-110`
  and `_v216seatrel/doctrine.py:33-48` apart from docstring wording (`diff` run).
* `bots/_v223sealrepair` contains **no `orient_cardinals`, no `SEAT_RELATIVE_SCAN`
  and no other seat-canonicalising call** (grep).
* `enemy_core_for` (`eco.py:38-52`) returns the **true** enemy core anchor on
  **15 of 15** pool maps and equals the plain point reflection
  `(w-2-x, h-2-y)` on **15 of 15** ⭐MEASURED — see §4.

**TREATMENT TREE: bots/_v240seatscan (not built at lock time — this document is
committed before the tree exists, which is the required order).**
**TREATMENT DIFF REFS: N/A — the arm tree does not exist at lock; `git diff` has nothing to intersect and the OB13 computation is CANNOT-COMPUTE by design, not a clean pass (§5).**

---

## 2. REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen, ZERO live rated exposure; no submit, no activation, no prototype on the ladder, so `tools/target_value.py`'s reachable-band gate does not bind.**
**PINNED: N/A — local screen. The control is a byte-frozen local tree (`bots/_v223sealrepair`), so opponent churn cannot reach this shard; the pin/never-pin design rule governs PLATFORM legs only.**
**SURFACE: local**
**CLUSTER UNIT: none — enumeration in §7; both clusters die, applicable DEFF = 0.98 (local, pair-weighted, s39 audit)**
**ESTIMATOR: pooled game share = treatment wins / (rows − NOWINNER rows), unweighted, over `SEATSCAN.tsv` rows only. No map weighting, no seat weighting, no pooling with any other shard.**
**DOSE: 25 of 30 (map, ORD) cells receive a CHANGED scan order in the treatment vs 0 of 30 in the control (n = 30 cells = 15 pool maps × 2 seat orders, the complete enumeration, not a sample) — computed cell-by-cell from the measured core anchors in §4; the 5 zero-dose cells are named there and are a within-shard placebo.**
**PLANNED n: 5400 games**
**BOUNDARY: 5400 shard rows = 5400 games (LOCAL fixture: 1 game per row; the platform `games = 5 × accepts` identity has no accepts to close on here — declared exemption in §11)**
**CUT-SHORT: below n=1000 this shard publishes descriptive tallies only and takes NO comparative look; a futility drop at either gate publishes the label, the n and the share and makes NO claim about the scan order beyond "not worth more cores now"**
**BAR: 51.33**
**BASE RATE: 50.0**
**BAR SOURCE: OB-F final band upper edge at n=5400 (= the 95% half-width ±1.33pp), the standing corefill screen band; identical construction to `SCREEN-sealfloor6-2026-08-14.md`. With the local DEFF 0.98 the half-width is ±1.32pp, so the house band is marginally conservative and is used unchanged.**
**BASE RATE SOURCE: structural null of a paired local screen — `tools/overnight.sh:99-110` plays every (seed, map) in BOTH seat orders (`ORD` A and B), so under H0 (the treatment is behaviourally identical to the control) the shard IS a byte-identical null and the expected treatment share is exactly 50.0, per map and overall. No historical population is consumed by the bar.**
**REFERENCE n: none — the byte-identical-null seat gaps in §6 are a DIRECTION AND SIZE PRIOR only and are a comparator in no share bar on this page**
**POOL ERA: post-2026-08-13-rotation — the 15-map local pool `tools/overnight.sh:68` (antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune), post-patch geometry (valkyrie `maps/valkyrie.map26` mtime 2026-08-14T14:53:12, glacierkeep 2026-08-14T09:01:09, the other 13 unchanged since 2026-08-06/08-13). The null priors in §6 were measured on shards that ran BEFORE the valkyrie/glacierkeep rewrite; those two maps are excluded from every prior quoted here and the exclusion is stated at each use. The rated-tape pool boundary bounds no number on this page, because no number on this page comes from the rated tape.**
**POOL_ERA: post-2026-08-13-rotation**
**MECHANISM METRIC READS: doctrine.py:26 (`CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]` — the list whose ORDER is the treated quantity, read by all 29 consumer sites enumerated in §3). TREATMENT DIFF TOUCHES: doctrine.py (the +22-line hunk after :26), main.py (the +1 call site after :167). INTERSECTION: YES — the metric's read site and the diff are the SAME FILE, `doctrine.py`.**
**GATE RESOLUTION: §8 — the band discriminates a true pooled effect ≥ 1.91pp at 80% power, against an arithmetic ceiling of 3.06pp and a random-sign central estimate of ~0.8pp (§6). ⇒ THE SCREEN IS POWERED FOR THE TOP THIRD OF THE EFFECT RANGE THIS PLANK CAN PRODUCE AND FOR NOTHING BELOW IT; UNRESOLVED is the MODAL outcome and defaults to the RESTRICTION — the absolute order stays, the arm is not promoted.**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock. `bots/_v223sealrepair` ships the fixed absolute order at `doctrine.py:26` and contains no `orient_cardinals` (grep, §1); the contrast "seat-relative vs absolute on the v140 chassis" has never been measured on any fixture (the two prior arms are v114 and v125 chassis, §6). PARTIAL PRE-STATE, declared: three sites already order their scan relative to a target (`eco.py:751-753`, `eco.py:866-871`, `eco.py:907`) and are ROTATION-INVARIANT, so the treatment cannot move them — they are pre-satisfied and are excluded from the mechanism claim (§3).**
**PRIMARY SEGMENT: the 10 ROT180 maps (archipelago, drakkarfjord, drumlin, fjordgate, glacierkeep, icefloe, midgard, ragnarok, royale, yulerune) versus the 5 MIRROR maps (antler, auroraveil, nordkap = MIRROR-Y; frostgate, valkyrie = MIRROR-X). MECHANISM: the treatment rotates the scan list while PRESERVING its cyclic handedness. A 180°-rotation map relates the two seats by a point reflection, which also preserves handedness — so on those 10 maps the rotation makes the two seats execute the SAME scan in their own frames, completely. A MIRROR map relates the two seats by a reflection, which REVERSES handedness — so on those 5 maps the rotation fixes only the FIRST scan direction and leaves the second and third swapped. The symmetry group of the map is the terrain property the mechanism names; ⭐MEASURED from the map files themselves in §4, not from a size proxy.**
**EXPECTED DIRECTION: the treatment's |share − 50.0| is LARGER on the 10 ROT180 maps than on the 5 MIRROR maps, with the SAME SIGN on both. ⛔ THE POOLED SIGN IS NOT PREDICTED and the reason is stated rather than hidden (§6): on 12 of the 15 maps the canonical order is a NEW behaviour for BOTH seats, so this arm is not "the losing seat adopts the winning seat's order" — it is "both seats adopt a third order", whose merit is exactly what the screen measures. The segment ordering is the signed, falsifiable part.**
**SEGMENT VALUE CEILING: 66.7% x 4.59pp on-segment = 3.06pp pooled**

**EXACTLY ONE PRIMARY SEGMENT (15b).** Every other cut on this shard —
per-map, per-seat (`ORD` A vs B), the zero-dose placebo cells of §4, the
three-class CQ/STD/GRAND split, size class — is **DESCRIPTIVE ONLY** and may not
be used to rescue a pooled fail. Named explicitly here so none can be promoted
later. **15c applies:** a pooled fail that clears the primary segment in the
predicted direction buys a **NEW screen with its own n**; these rows may never
confirm the segment they suggested.

---

## 3. MECHANISM OCCURRENCE — where an iteration order actually decides something

`CARDINALS` is consumed at **32 sites** in the control tree (grep, `bots/_v223sealrepair`).
They split three ways and only the first group is treated:

**(a) 29 ORDER-SENSITIVE sites — first-match-wins scans and set/BFS expansions.**
`main.py:492` (`_sabotage_prio`, which enemy building to attack),
`main.py:563` (`_try_counterbattery`, which adjacent tile takes the turret),
`main.py:650` (`_try_build_launcher`, which tile takes the launcher);
`raid.py:271` (which spawn seat gets the barrier seal), `:296` (which adjacent
enemy builder is grabbed), `:317` and `:599` (which building gets pecked),
`:456/:489/:544/:575` (which tile gets salted), `:672` (where the forward
sentinel goes), `:834` (which seat is scored open);
`eco.py:333` (which tile gets healed), `:394/:436/:468/:845` (BFS goal set and
neighbour expansion — the order decides WHICH of several equal-length conveyor
routes is built), `:514/:605/:975` (acceptor/starvation/siphon predicates),
`:674/:697` (which belt gap gets repaired), `:856`, `:1082` (which cardinal the
denial builder MOVES in), `:1146/:1200` (which tile takes the next expansion
building), plus the two fallback branches `eco.py:874` (`order = CARDINALS` when
the desired direction is diagonal) and `eco.py:906` (`... else 0`).
**Every one of these breaks a tie by list position**, and a builder bot has at
most 4 orthogonal neighbours, so a tie is the normal case rather than the rare
one: any turn on which ≥2 adjacent tiles satisfy the predicate is decided by the
scan order alone.

**(b) 3 ROTATION-INVARIANT sites — pre-satisfied, and the treatment cannot move them.**
`eco.py:751-753`, `eco.py:866-871`, `eco.py:907` read `CARDINALS[(i±1) % 4]`
relative to `i = CARDINALS.index(desired)`, where `desired` comes from
`cardinal_direction_to(target)`. Those offsets are preserved under any cyclic
rotation, so these sites are ALREADY seat-relative and stay byte-equivalent.
**This is the QUEUE row's "20+ first-match-wins scans" claim, re-checked and
narrowed: the tree is not uniformly seat-blind; three sites already do it.**

**⛔ WHAT IS NOT ESTABLISHED, and it is the same limit QUEUE #8 states about
itself:** none of the 29 sites has been shown to change a GAME OUTCOME. The
honest status is *"the order is absolute, the order decides ties, and ties are
common"* — a structural argument, not a measured one. §9 registers the
measured dose check this leaves OWED and states why the obvious cheap version
of it does not work on this chassis.

**HOT-TURN COST: NEUTRAL.** `orient_cardinals` is O(1) — four subtractions, two
comparisons, one `list.index`, one slice-assign — and runs **once per CORE
turn**, i.e. once per round on the one unit that is not the CPU-critical one
(worst observed 8,748µs of the 10,000µs budget is on 900-area builder/raider
turns). It adds **zero** work to every builder, raider and turret turn: the
consumers iterate the same 4-element list they iterate today. ⚠
`get_cpu_time_elapsed()` reads ZERO locally, so no local test can catch a CPU
regression — the claim above rests on the diff adding no per-tile work, which is
verifiable by reading the two hunks in §1 and is not a measurement.

---

## 4. THE DOSE, COMPUTED CELL BY CELL ⭐MEASURED

**Core anchors were measured on the engine**, not read off a table: a passive
probe (`Player.run` printing `get_team()` and `get_position()` on round 0 from
the Core, stderr, one game per map, seed 990003) reports **Team A at the LOW-y
anchor and Team B at its point reflection on 15 of 15 pool maps**, and
`eco.enemy_core_for(w, h, A)` reproduces the measured Team-B anchor on **15 of
15**. In `tools/overnight.sh:109-110` the tree listed FIRST is Team A, so
`ORD=A` rows are the treatment on the low-y seat.

**Map symmetry class comes from the map FILES** (`tools/map_encode.py:41
parse_map26`, then testing the decoded grid for `g[y][x] == g[h-1-y][w-1-x]`
(rot180), `g[y][w-1-x]` (mirror-X) and `g[h-1-y][x]` (mirror-Y)):

| class | maps | treatment's rotation is… |
|---|---|---|
| **ROT180** (10) | archipelago, drakkarfjord, drumlin, fjordgate, glacierkeep, icefloe, midgard, ragnarok, royale, yulerune | **the map's own seat symmetry — complete fix** |
| **MIRROR-Y** (3) | antler, auroraveil, nordkap | first direction only; handedness stays reversed |
| **MIRROR-X** (2) | frostgate, valkyrie | first direction only; handedness stays reversed |

*(glacierkeep and royale satisfy all three tests; rot180 holds, so the rotation
canonicalises them and they sit in the ROT180 group.)*

**Per-(map, ORD) dose**, computed by running the treatment's own transform on
the measured anchors:

* **25 of 30 cells CHANGE the scan order.**
* **5 of 30 cells are ZERO-DOSE — the treatment's rotated list is byte-equal to
  the shipped `[N, E, S, W]`, so on those rows the treatment tree is
  behaviourally identical to the control:**
  `ORD=B` on **antler, auroraveil, glacierkeep, nordkap** (Team B's enemy lies
  due NORTH, so the canonical first direction is already `NORTH`), and `ORD=A`
  on **royale** (the one pool map whose Team A sits at the HIGH-y anchor).
* Those 5 cells are a **within-shard placebo**: a real effect must not be
  concentrated in them. ⚠ Their expected share is **not** 50 — it is whatever a
  byte-identical null gives that cell — so this placebo is a **pattern check and
  an instrument alarm, not a bar**, and it becomes a hard test only against a
  v140 byte-identical null, which does not exist (§6, §10).

---

## 5. OBLIGATION 13 — the intersection, stated exactly

```
MECHANISM METRIC READS:  doctrine.py:26
TREATMENT DIFF TOUCHES:  doctrine.py (+22 after :26), main.py (+1 after :167)
INTERSECTION:            YES — same file, doctrine.py
```

This arm is the easy case for Obligation 13: the quantity the metric reads (the
ORDER of `CARDINALS`) and the quantity the diff changes are the same object in
the same file, so there is no import-binding indirection to argue about.

**⛔ WHAT `tools/prereg_check.py` WILL ACTUALLY PRINT, declared in advance so a
tool verdict is not mistaken for a fact.** At lock time `bots/_v240seatscan`
does not exist, so `git_diff_paths` falls back to `git diff --name-only HEAD` —
which at draft returns **`tools/effective_n.py`, `tools/gate.py`,
`tools/overnight_read.py`, `tools/prereg_check.py`**, i.e. *another agent's
in-flight tool edits*, and `doctrine.py` is correctly absent from that list.
**The checker therefore FAILs `OB13_INTERSECTION` for a reason that has nothing
to do with this arm: the repo's working diff is not this arm's diff, and cannot
be until the tree is built.** The intersection above is verified by reading the
two hunks, and the checker's computed cell should be re-run with `--fire` once
`bots/_v240seatscan` exists and is `git add -N`'d — at which point it must read
**ok** (same file), and if it does not, that is a real defect and blocks the
fire. Filed for the builder as a triage note, not worked around here.

---

## 6. PRIOR, HYPOTHESIS, AND THE ARITHMETIC THAT SIZES THE EFFECT (⚖ builder ratifies)

**⚖ HYPOTHESIS (one sentence, falsifiable).** *Ordering the shared `CARDINALS`
scan list by the direction of the enemy core makes both seats execute the same
tie-breaking policy in their own frame, and the policy that results is a better
policy than the two seat-dependent ones it replaces — so `bots/_v240seatscan`
wins more than half its games against `bots/_v223sealrepair` at n=5400.*

### The prior, and it is stronger than QUEUE #8 recorded ⭐MEASURED

Pooled over the five **byte-identical** null shards
(`NULL114`, `NULL123`, `NULL125`, `NULLSALT`, `SHIPGATENULL`; byte-identity of
all five tree pairs re-verified at draft, 4/4 `.py` files each), n = 24,226
scored rows: **seat A 54.01% vs seat B 46.43%, gap +7.58pp ±1.26.** That
reproduces the row's own 7.58pp.

**The new reading is per map, and it is not what the pooled number suggests**
(valkyrie and glacierkeep excluded everywhere below — their map files were
rewritten after these shards ran):

| map | class | null seat gap | | map | class | null seat gap |
|---|---|---|---|---|---|---|
| nordkap | MIR-Y | **+19.98** | | ragnarok | ROT | +11.28 |
| fjordgate | ROT | **+17.80** | | icefloe | ROT | +11.24 |
| drumlin | ROT | **+16.24** | | archipelago | ROT | **−11.24** |
| midgard | ROT | +15.36 | | yulerune | ROT | **−10.53** |
| royale | ROT | **−15.41** | | drakkarfjord | ROT | +8.24 |
| auroraveil | MIR-Y | +13.86 | | antler | MIR-Y | +7.18 |
| | | | | frostgate | MIR-X | −0.75 |

**Mean |per-map gap| = 12.24pp across the 13 clean maps, and the SIGN FLIPS
between maps** (glacierkeep, excluded above for staleness, read +47.94). **The
pooled 7.58pp is a partial CANCELLATION of much larger opposing per-map gaps.**
Two consequences, both load-bearing:

1. **The seat gap is NOT a fixed engine bonus to the first-listed team.** A
   constant seat-A advantage cannot change sign between nordkap (+19.98) and
   royale (−15.41). It is geometry-dependent code behaviour — which is exactly
   what QUEUE #8 asserts and what nothing had yet shown.
2. **Any effect size computed from the pooled 7.58pp UNDERSTATES the mechanism
   by about a factor of 1.6.**

### Sizing the treatment effect, and the model that does it

Write `f(x, y)` for the probability the seat-A player `x` beats the seat-B
player `y`, and model it additively as
`f(x, y) = 0.5 + m + (u_x(A) − u_y(B)) / 2`, with `m` a seat-A term that belongs
to the map/engine and `u_i(seat)` the strength of code `i` on that seat. Let
`d = u_s(A) − u_s(B)` be the shipped code's own seat asymmetry, so a
byte-identical null reads `gap0 = 2m + d`. Then for any seat-symmetric
treatment `t`:

* **pooled treatment share = 0.5 + (2·u_t − u_s(A) − u_s(B)) / 4**, i.e.
  **between −d/4 and +d/4**, and **exactly 50.0 if the canonical order is the
  average of the two orders it replaces**;
* **head-to-head seat gap = 2m + d/2 — HALF the null's `d` term — and this is
  INDEPENDENT of `u_t`.**

⇒ **The two readings are algebraically orthogonal: the pooled share measures
whether the canonical order is BETTER, the seat gap measures whether the
treatment became SYMMETRIC, and neither contaminates the other.** That is why
both are declared, and why only the first is a decision gate.

⇒ **SYMMETRY ALONE IS WORTH ZERO.** The ladder pays game share, and our expected
share is the average over seats; equalising two seats at their own average
changes nothing. **QUEUE #8's "+1–2pp ≈ +7–14 Elo" does NOT follow from the gap
existing** — it follows only if the canonical order is better than the mean of
the orders it replaces. **This screen is the test of that, and it can come out
at zero with the mechanism entirely real.**

**Effect range, per map:** `|per-map effect| ≤ d/4 ≈ 12.24/4 = 3.06pp`.
**Pooled:** if the per-map signs align, up to **3.06pp**; if they are unrelated,
`3.06/√15 ≈ 0.8pp`. **Predicted |pooled effect| ∈ [0, 3.06]pp, central ~0.8pp.**

**⚠ The prior's limits, stated rather than buried.** The null shards span three
chassis (v116/v125/v187-era) and two map-pool eras; none is v140. Their `m`
term is unmeasured except for one "n.s." third-party estimate of ~1.8pp quoted
in QUEUE #8, so the split of `gap0` into `2m` and `d` is a modelling choice, not
a measurement. **A v140 byte-identical null does not exist** — no worklist row in
`scratchpad/corefill_work.txt` has two byte-identical v140 trees — and its
absence is the single largest gap in this design (§10).

### Why this is not a re-run of SEATREL or GUNSEAT

Two arms have carried this plank: **GUNSEAT** (`_v156gunseat`, v114 chassis,
**51.04 ±1.33 @5408**) and **SEATREL** (`_v216seatrel`, v125 chassis,
**50.40 ±1.87 @2752**, futility-dropped at `GATE-2700`). This arm is a **third
chassis (v140), a different control (`_v223sealrepair`), a different map pool
and a different post-patch geometry**. It is also, per
`QUEUE-ECONOMICS-SWEEP-2026-08-14.md:106`, still **not** the row's own declared
fixture — that is a byte-identical null with BOTH sides seat-relative, which
§10 registers as owed and which this shard does not attempt.

---

## 7. CLUSTER ENUMERATION (CLAUDE.md scope procedure, performed in writing)

1. **MATCH cluster — DIES.** A local shard has no 5-game match wrapper; each row
   is an independently seeded single game (`tools/overnight.sh:95-99`, one game
   per (seed, map, ORD) triple). No stratum can hold two games from one match
   because no match object exists.
2. **OPPONENT cluster — DEGENERATE.** Exactly one opponent
   (`bots/_v223sealrepair`) for all 5400 rows; no between-opponent contrast is
   drawn, so there is no multi-member opponent stratum to inflate.

⇒ **Applicable DEFF = 0.98** (local pair-weighted, ρ = −0.020, 124 shards, s39
audit). **The platform constants 1.529 / 1.833 are NOT imported** — that would
widen these intervals 24–35% for correlation that is not there.

⚠ **Where this could bite:** the s39 audit found local outlier arms with strong
map interaction at DEFF ≈ 1.20–1.25, and this arm declares a map segment and
predicts map interaction explicitly. **The segment split is therefore
INDICATIVE; a segment claim is banked only via the 15c re-screen, never off
these rows.**

---

## 8. DESIGN, GATES AND THE DECISION RULE (⚖ builder ratifies the branch labels)

**Fixture.** `tools/corefill.sh` → `tools/overnight.sh`, full 15-map post-patch
pool, `--tle 10` wall-clock enforced, `--replay /dev/null`, both seat orders per
seed. Worklist row:

```
SEATSCAN    bots/_v240seatscan     bots/_v223sealrepair   5400 310000
```

Seedbase **310000** is disjoint from every row in
`scratchpad/corefill_work.txt` (highest local base in use is 308000, SEALFLOOR6;
this shard consumes 310000–310337) and from the remote worklist
`scratchpad/overnight-remote/worker@work-server-1/worklist.txt` (32xxxxxx band).
Basenames `_v240seatscan` / `_v223sealrepair` do not collide as substrings, so
`corefill.sh`'s scoring refusal does not trigger. `_v240seatscan` is a free
directory name (highest existing is `_v239wirehold`).

**⛔ READ HYGIENE:** the shard key is **`SEATSCAN` exactly**. A `grep SEAT`
pools **`SEATREL`** (v125 chassis, control `_v197mapcode`) and **`GUNSEAT`**
(v114 chassis) — different contrasts entirely. Any read that cannot show it
matched the exact key is not a read of this shard.

**n and resolution** (n = 5400, p̄ ≈ 0.5):

| quantity | in pp | in games (of 5400) |
|---|---|---|
| 1 SE | 0.68pp | 36.7 |
| **95% half-width** | **±1.33pp** (±1.32pp at DEFF 0.98) | **±72** |
| **80%-power MDE** (one-sample vs 0.5, Z=2.802) | **1.91pp** | ≈103 |
| OB-F final band | 48.67 – 51.33 | 2629 – 2771 |
| seat gap, half-width (2700/seat) | **±2.67pp** | — |
| ROT180 segment (3600 rows) half-width | ±1.63pp | — |
| MIRROR segment (1800 rows) half-width | ±2.31pp | — |

**⛔ THE POWER STATEMENT, WRITTEN BEFORE THE DATA.** The MDE (1.91pp) sits at
**62% of the arithmetic ceiling** of what this plank can do (3.06pp) and **2.4×
the random-sign central estimate** (0.8pp). **This screen is well designed to
CLOSE the road and poorly designed to OPEN it.** An `UNRESOLVED` band read is
the MODAL outcome and is pre-typed below as a DROP, not as something to argue
with afterwards.

**GATES (per `RULE-futility-gates-2026-08-13.md`, read ONCE each at first
crossing; the builder types the decision, the watcher never decides):**

* **GATE-1000 (n ≥ 1000): drop if share < 48.0% — i.e. ≤ 479 of 1000.** Label `FUTILITY-EARLY`.
* **GATE-2700 (n ≥ 2700): drop if share ≤ 50.5% — i.e. ≤ 1363 of 2700.** Label `FUTILITY-ALONE`.
* This is **not an ablation arm**, so the `DECISION-REACHED` clause does not apply.

**⚖ DECISION RULE (proposed; the branch labels are the judgment lines):**

| final at n=5400 | in games | branch |
|---|---|---|
| **≥ 51.33%** | **≥ 2772** | **OUTSIDE-ABOVE → KEEP-dev.** The canonical order is better than the pair it replaces. Mandatory next steps: **D26 replication** (seed 312000, scored alone, same-side pooling) AND the OWED dose check of §9 before any verdict sentence cites mechanism. No ship implication: `SHIP_SIT` governs and v140 is sitting. |
| **48.67 – 51.33%** | 2629 – 2771 | **NO-INFORMATION → DROP, order unchanged.** Per the pre-committed UNRESOLVED default: the restriction, never the permission. Written as *"the screen could not separate the seat-relative order from the absolute one at ±1.33pp, against a mechanism whose ceiling is 3.06pp"*, **never** as *"the seat asymmetry does not matter"* and never as *"the effect is zero"*. |
| **≤ 48.67%** | **≤ 2628** | **OUTSIDE-BELOW → REAL NEGATIVE, road closes for THIS transform.** The enemy-first canonical order is worse than the two seat-dependent orders it replaces. #8's premise (the order is absolute, and that costs us) survives; #8's PRESCRIPTION (`cardinal_direction_to(enemy_core)`) is refuted, and the surviving candidate is the handedness-aware variant named in §10 — a different change, needing its own prereg. |

**D26:** any final with |share − 50| ≥ 2.0pp (≤2592 or ≥2808 games) replicates at
seed 312000.

**⚖ KEEP-dev vs DROP, as the single sentence the builder ratifies:** *only an
OUTSIDE-ABOVE final keeps this arm alive; the band and everything below it drop
the arm and leave `CARDINALS` absolute.*

---

## 9. DOSE VERIFICATION — what is verified, what is OWED, and the probe that DOES NOT WORK

**VERIFIED AT DRAFT (code level, both verdicts driven):** the treatment's scan
list differs from `[N, E, S, W]` in **25 of 30** (map, ORD) cells and is
byte-equal in **5 of 30** (§4). Both verdicts are produced by the same
computation over the same measured anchors, so the "changed" cells are not
asserted by a check that can only say yes.

**⭐MEASURED AND REPORTED AS A FAILED INSTRUMENT, because it is the cheap probe
anyone would reach for next.** A paired same-seed run — treatment-vs-control
against byte-identical-null-vs-control on the same map and seed — showed all
6 of 6 map pairs differing (different winner and/or turn count), which reads
like a clean dose. **The negative control refutes it:** re-running the
*identical* command (same trees, same map, same seed 990001) **twice** produced
different games in **6 of 6** maps — e.g. antler `_v197mapcode` core-kill at
turn 122 vs a turn-1000 titanium tiebreak; nordkap turn 156 vs turn 334.
**With `NOISE_ON = True` this chassis is nondeterministic run-to-run, so a
same-seed trajectory diff cannot distinguish a real dose from noise and the
first probe measured nothing.** Recorded here so nobody re-derives it and banks
the first half.

**⛔ OWED, PRE-FLIGHT AND BLOCKING — the determinism-pinned dose probe.** Before
`SEATSCAN` fires, run a paired probe on **throwaway copies with
`NOISE_ON = False` in BOTH arms** (the QUEUE #8 rider's "never pin the measured
copies" governs the SHARD; a dose probe is not a measured copy, and the pin is
what makes the comparison legible):
* **Cell 1, the negative control:** null-vs-control, 15 maps, one seed, run
  twice. **Must be 15/15 identical.** If it is not, the instrument is blind and
  the gate is void.
* **Cell 2, the dose:** treatment-vs-control against null-vs-control on the same
  15 maps and seed. **Report the count of differing games.**
* **PRE-DECLARED expectation:** ≥ 20 of the 25 full-dose cells differ, and
  **0 of the 5 zero-dose cells differ** (§4). **If any zero-dose cell differs,
  the treatment is not the change this document describes** — either the module
  is shared between teams or the port is not verbatim — **and the shard must not
  fire.** If fewer than 10 full-dose cells differ, the plank is close to inert
  and the shard is not worth its cores.

**A SECOND STANDING ASSUMPTION, named because nothing on this page proves it:**
`orient_cardinals` mutates a **module-level** list, so the arm is only coherent
if the two teams get separate module namespaces. The evidence is indirect but
strong — asymmetric local arms read far from 50 (`SURCH90` 26.42 @757), which is
impossible if both teams executed one shared module — and Cell 1 above tests it
directly at the level that matters.

---

## 10. WHAT THIS SCREEN MAY NOT CONCLUDE, AND THE TWO THINGS IT LEAVES OPEN

**COUPLING CLASS: SELF-KNOWLEDGE / pure geometry** — the transform reads only
our own core, the enemy core anchor and the map dimensions; it is
opponent-invariant by construction, so a local self-play screen is a
trustworthy instrument for it and no live window is spent.

**NOT LICENSED by this screen:**
* **No ship implication.** `SHIP_SIT` governs; v140 is sitting.
* **No claim that the seat gap CLOSED.** The head-to-head gap is `2m + d/2`
  under any seat-symmetric treatment — a predicted move of roughly `d/2` ≈
  1.0–3.8pp against a ±2.67pp band. **It is reported with its band and read as a
  consistency check, never as a bar**, and it cannot be compared to a v140 null
  because none exists.
* **No claim about the row's declared fixture.** The byte-identical null with
  BOTH sides seat-relative — the reading that would drive the gap to the map
  residual — is still **never run**. If this screen reads OUTSIDE-ABOVE, that
  null (seed 314000) is the natural follow-on and needs its own prereg.
* **⭐ NO CLAIM ABOUT MIRROR MAPS BEING FIXED.** §4 shows the transform is only a
  partial canonicalisation on 5 of 15 pool maps. **The handedness-aware variant
  — reverse the cycle for the reflected seat on mirror-symmetric maps — is a
  DIFFERENT CHANGE and is deliberately not built here.** The segment result is
  what would motivate it.

**INTERACTION with the two live legs, and one of them is a mechanism overlap,
not just core contention:**
* **SEALFLOOR6** (`_v238sealfloor6` vs `_v223sealrepair`, seed 308000) doses the
  barrier-seal titanium floor, whose guard sits at **`raid.py:270`** and whose
  seat scan is **`raid.py:271` — a `for d in CARDINALS` loop this arm reorders.**
  **SALTREF2** (`_v231saltref` vs `_v223sealrepair`, remote, seed 32310000)
  doses salt, whose tile scans are **`raid.py:456/:489/:544`** — also reordered
  here. ⇒ **A future tree carrying both this plank and either of those is NOT
  the sum of the parts: this arm changes WHICH seat is sealed first and WHICH
  tile is salted first.** No combined read may be taken from the two separate
  screens.
* Fixture-level: same CONTROL (`bots/_v223sealrepair`), disjoint seedbases, no
  shared rows, no pooling — the three shards contend only for cores.
* **Rebase risk:** if SEALFLOOR6 or SALTREF2 ships into v141, `_v240seatscan`
  must be rebuilt on the new incumbent and this screen re-run. The diff is two
  ADD-only hunks, so the rebase is mechanical, but the reading does not carry.

---

## FALSIFIER

**The hypothesis (§6) is falsified by any of:**

1. **A final ≤ 48.67% (≤ 2628 of 5400)** — the enemy-first canonical order is
   measurably worse than the two absolute orders it replaces, and #8's
   prescription is refuted even though its premise stands.
2. **A futility drop at either gate** (≤479/1000 or ≤1363/2700).
3. **A final inside the band** — the hypothesis is not supported at ±1.33pp, and
   by the pre-committed UNRESOLVED default the absolute order stays. *(This is
   the modal outcome, pre-typed as a drop.)*
4. **The pre-flight dose probe (§9) failing either cell** — Cell 1 not 15/15
   identical (instrument blind), or any of the 5 zero-dose cells differing
   (the treatment is not the described change). Either voids the shard before
   it fires.

**The PRIMARY SEGMENT prediction is falsified** if the treatment's |share − 50|
on the 10 ROT180 maps is **≤** its |share − 50| on the 5 MIRROR maps, or if the
two segments carry **opposite signs**. *(A reversal — the transform helping most
where it is only a partial canonicalisation — would contradict the geometric
account outright, and per 15c it buys its own screen with its own n; it does not
rescue a pooled fail on these rows.)*

**The MECHANISM METRIC is falsified** if the shard's seat gap comes in at or
above the byte-identical-null prior (7.58pp pooled) with the CI excluding
`2m + d/2` — that would mean the treatment did not become seat-symmetric at all,
which no reading of the pooled share can rescue.

---

## 11. OBLIGATIONS REGISTER (`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md`)

* **Ob. 7 (PRE-STATE / outcome form):** satisfied — outcome is **game share IN
  OUR FAVOUR** on this shard; the predicted-change set is verified not
  pre-satisfied, **including the partial pre-state** (3 rotation-invariant sites
  named and excluded, §2 `PRE-STATE` and §3(b)).
* **Ob. 8 (denominator rule):** single control, single fixture, single shard;
  5400 rows from one worklist row, pooled with nothing.
* **Ob. 11 (verify the treatment the EXPERIMENT requires):** §9 — the code-level
  dose is verified in both verdicts; the BEHAVIOURAL dose is declared OWED with
  a named, blocking, two-cell pre-flight probe, and the probe that does **not**
  work is reported with the negative control that killed it.
* **Ob. 12 (a gate is a bar and carries its resolution + pre-committed
  unresolved default):** satisfied in §8, including the explicit statement that
  the MDE sits above the central predicted effect.
* **Ob. 13 (`file:line` + intersection):** satisfied in §5, with the tool's
  expected FAIL and its cause declared in advance.
* **Ob. 14 (opponent version stability):** **N/A by shape** — the control is a
  byte-frozen local tree, not a platform cell. No `CELLS:` line exists.
* **Ob. 15a/b/c (map dependence):** satisfied in §2 with one primary segment
  chosen on a **mechanism-named terrain property** (the map's symmetry group,
  measured from the map files) rather than a size proxy, a signed direction, a
  recomputable value ceiling, and an explicit descriptive-only list.
* **Ob. 1–6, 9, 10:** Ouroboros/CAD-leg-specific or platform-mechanism-leg
  specific; they do not instantiate on a local single-knob screen. Stated rather
  than skipped.
* **⛔ NOT SATISFIED, structural — `BOUNDARY` in accepts.** `prereg_check.py`'s
  `BOUNDARY_UNITS` wants the boundary in both accepts and games with the
  platform identity `games = 5 × accepts`. **A local shard has no accepts** (one
  row is one game; the same fact that kills the MATCH cluster in §7). Declared in
  the only two units it has — 5400 rows = 5400 games — as a local-fixture
  exemption the tool does not model, not as a waived obligation.

## Target-value line

Local screen, zero live exposure ⇒ payout gate N/A (see §2 `TARGET BAND`).
