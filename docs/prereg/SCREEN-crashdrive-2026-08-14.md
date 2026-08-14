# SCREEN — **`crashdrive` (`QUEUE #17`)**: does the crash weapon actually FIRE? A LOCAL BOTH-WAYS DRIVE

**Drafted by a fresh opus subagent with no inherited session context, 2026-08-14
21:0xZ (`date -u` in the drafting shell: `2026-08-14T21:05:26Z`; repo HEAD at
drafting `c5f60ad4`). The lane ratifies and commits; the agent does not.**

**STATUS: committed BEFORE the arm trees exist and BEFORE any leg row is
generated** (two-clock standard: git author time of this file vs the mtime of the
first row of `crashdrive` output). **The design-phase dose probe reported in §2 is
OBSERVABLE-AT-LOCK and is labelled as such throughout — it is NOT a leg row, its
seeds are disjoint from the leg's, and no bar below was chosen after seeing a
number it did not already have.** *(Obligation 1, obligations doc.)*

**Control tree / live holder: `bots/_v223sealrepair` (v140).**
**This is an INSTRUMENT-VALIDATION leg, not a ship screen — see §7.**

---

## 0. REGISTRATION BLOCK

**TARGET BAND: N/A — LOCAL leg. Zero rated exposure, zero submits, zero
unrated-window budget, no opponent is ever challenged, so `tools/target_value.py`
has no input to take. The gate is ANSWERED by the absence of a target, not
skipped: nothing here can pay or cost a rating point.**
**PINNED: N/A — local fixture, there is no platform opponent to pin. The local
analogue IS honoured: all four trees (two thrower, two victim) are frozen at the
ratifying commit for the whole leg, and neither victim probe may be edited once a
row exists.**
**SURFACE: local**
**CLUSTER UNIT: none — one `fcode run` is one independent game and one row; there
is no 5-game MATCH cluster locally, so that cluster is dead by construction, and
the OPPONENT cluster is degenerate inside a cell (a cell has exactly one
opponent, so it cannot induce between-opponent correlation within the cell). The
measured local constant is pair-weighted DEFF = 0.98 (rho = -0.020, 124 shards,
s39 audit). ⛔ The platform constants 1.529/1.833 must NOT be applied here.**
**ESTIMATOR: per-cell SHARE OF GAMES containing >=1 weapon-attributable victim
destruction, pooled over the cell's rows, unweighted, one row = one game.
Secondary and reported alongside: raw destruction counts, border arrivals, and
per-1,000-exposed-victim-round rates from `tools/crash_cells.py::dose`. Any
CROSS-CELL rate quote is bound by `tools/crash_cells.py::compare`, which REFUSES
a ratio when exposure differs by more than 15%.**
**DOSE: weapon-attributable victim destructions 11 with the exile arm ON vs flag-off 0 with `EXILE_ON = False` (n=15+15 local design-phase probe rows, 2026-08-14, seed block 92000, single seat, identical maps and seeds and thrower build otherwise; per-game incidence 2 of 15 vs 0 of 15)**
**PLANNED n: 240 games (4 cells x 60 rows)**
**BOUNDARY: 240 games (4 cells x 60 rows; LOCAL surface — one `fcode run` is one
row and one game, and there are no accepted challenges in this fixture)**
**CUT-SHORT: below 120 games in total, or fewer than 30 completed rows in any
single cell, this leg publishes descriptive tallies only and takes NO mechanism
verdict**
**BAR: >=10.0% of cell-P games contain at least one weapon-attributable victim
destruction**
**BASE RATE: 0.0% — the same statistic in cells G and Z, which are forced to zero
BY CONSTRUCTION (guarded victim / no exile), not by expectation**
**BAR SOURCE: pre-registered treatment bar, this document. Sized against the
design-phase probe's 2/15 = 13.3% and against the per-cell half-width computed in
§5; deliberately set BELOW the probe's observation so the bar is not the
observation wearing a bar's clothes.**
**BASE RATE SOURCE: forced-zero controls of this leg, plus the observable-at-lock
probe of 2026-08-14 — cell G (guarded victim, SAME thrower, SAME maps and seeds)
0 destructions in 15 games at a HIGHER measured border dose (15 arrivals vs 2),
and cell Z (`EXILE_ON = False`) 0 destructions and 0 throws in 15 games.**
**REFERENCE n: none**
**MECHANISM METRIC READS: bots/_v224crashon/raid.py:931. TREATMENT DIFF TOUCHES: bots/_v224crashon/doctrine.py bots/_v224crashon/raid.py bots/_v224crashoff/doctrine.py bots/_v224crashoff/raid.py. INTERSECTION: yes.**
**TREATMENT DIFF REFS: HEAD -- bots/** — ⛔ scoped to `bots/` ON PURPOSE and it is
not a convenience: at drafting time the working tree carries unrelated modified
files under `tools/` from another lane, and an unscoped `git diff HEAD` makes the
Obligation-13 intersection read FAIL against a diff that has nothing to do with
this leg. Scoping to the directory the treatment actually lives in is the honest
comparison; it does NOT weaken the check, because the arm trees are under
`bots/` and a real miss would still show as a metric file absent from a non-empty
`bots/` diff.
**GATE RESOLUTION: see §5 — the dose gate (cell G >= 20 border arrivals)
discriminates its two branches at n = 60 rows per cell, where the probe-implied
expectation is ~60 arrivals and P(Poisson(60) < 20) < 1e-8. UNRESOLVED (fewer
than 20 arrivals in cell G, or a contaminated control) DEFAULTS TO THE
RESTRICTION: no verdict is published, the row stays open, and nothing is closed.**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock,
and this was MEASURED rather than assumed — see §3.**
**MAP SEGMENT: none expected — the primary outcome is a per-TILE property. An
unguarded self-relative neighbour query raises iff at least one of the unit's
four cardinal neighbours is off-map, which is true of a border tile on every
grid and false of an interior tile on every grid. Map area changes the DOSE (how
large a share of the launcher's reachable disc is border tile), never the
mechanism, so size class is reported per cell as DESCRIPTIVE ONLY and no
segment read is registered.**
**CELLS: P (forced positive) · G (forced negative, victim-side) · Z (forced
negative, weapon-side) · S (descriptive, shipped configuration) — four LOCAL
arms, no platform opponents**
**CELL VERSION CHURN: N/A — local fixture. The two victim probes and the two
thrower trees are files in this repo, frozen at the ratifying commit; they cannot
ship a new version mid-leg, so the 24-hour distinct-version count that Obligation
14 requires of a panel cell has no local analogue and no substitute is faked.**
**POOL ERA: post-2026-08-13-rotation** *(the parent normalises the spelling
`POOL_ERA: post-2026-08-13-rotation`)*
**SPANS-POOL-CHANGE: no — the map pool here is the LOCAL 15-map list frozen in
`tools/overnight.sh:68`, not the platform rotation; it does not move during the
leg.**
**TREATMENT TREE: `bots/_v224crashon` (thrower, exile ON) and
`bots/_v224crashoff` (thrower, exile OFF)**

---

## 1. HYPOTHESIS — one sentence, and it can lose

**When our launcher throws an ENEMY builder onto a map-border tile, an opponent
whose `run()` queries a neighbour of its own position without a guard is
PERMANENTLY DESTROYED by the engine, while a byte-identical opponent that wraps
the same query survives the same throws — so the crash weapon fires, and the
instrument that reads it separates a forced-positive arm from two forced-negative
arms rather than returning the same answer to all three.**

This is an **instrument-validation / both-ways drive**. The question is *does the
weapon fire at all*, not *does it win games*. A check that has never produced the
other verdict has not been seen to check, so the design contains an arm where a
destruction MUST occur and two arms where it MUST NOT, and the metric must
separate them.

---

## 2. WHAT ALREADY EXISTS — read before building anything

**⛔ THE QUEUE ROW AS WRITTEN IS STALE, AND A DRAFTER WHO TRUSTS IT WILL REBUILD
WORK THAT IS ON DISK.** `QUEUE #17` still names `bots/_probe_oov_raw` /
`bots/_probe_oov_guard` as the victim pair and says *"Nothing to write — this is
a RUN, not a build."* Both halves are out of date:

* `bots/_probe_oov_raw` **cannot serve** and its successor's docstring says why:
  it queries the FIXED corner `Position(w-1, h-1)`, which is in bounds and
  identical wherever the unit stands. **Position-invariant ⇒ the throw changes
  nothing ⇒ cells (a) and (c) return the same answer by construction.**
* The correct victims were built at s33 and are on disk and tracked:
  **`bots/_probe_border_raw`** (unguarded, queries a neighbour of SELF, and
  **refuses to step onto a border tile of its own accord**, so every border
  arrival is a throw) and **`bots/_probe_border_guard`** (byte-identical except
  the query is wrapped).
* The reader was built too: **`tools/crash_cells.py`**, whose `--selftest` passes
  25/25 in this session, including the 26x26 size trap and the immortal-time
  selection cells.

**AND THE PRIOR RESULT MUST BE CARRIED WITH ITS SCOPE.**
`scratchpad/crash_cells_s33_v2.txt` (2026-08-12) reads MECHANISM: CONFIRMED —
13 border arrivals / 13 crashes against the unguarded probe, 16 border arrivals /
**0** crashes against the guarded one. ⚠ **Two limits, both load-bearing:**
1. **It was run on `bots/_v131loki14`, not on the shipped tree.** That tree has
   **no `LAUNCHER_MIN_RND` at all** (grepped: the constant is absent from
   `bots/_v131loki14/doctrine.py` and `bots/_v131loki14off/doctrine.py`), so it
   arms a launcher early. **The shipped v140 defers to r160.**
2. **It was produced by v2 of the instrument, which has since been rewritten
   twice** — v3 introduced EXPOSURE as the denominator after the counter was
   found to be biased by its own treatment (`6865682d`), and the exposure-skew
   refusal followed (`44fe754e`). **The confirming run has never been reproduced
   on the current instrument**, and its clean 1.00-crashes-per-border-throw is
   exactly the shape the truncation bias produces.

⇒ **The mechanism is not unknown; it is UNREPRODUCED ON THE SHIPPED CHASSIS AND
ON THE CURRENT INSTRUMENT.** That is what this leg buys.

**DESIGN-PHASE DOSE PROBE, run 2026-08-14 during drafting, OBSERVABLE-AT-LOCK,
seeds 92000-block, 15 maps x 1 seed, single seat, trees in the drafting agent's
scratchpad (nothing under `bots/` was edited):**

| cell | thrower | victim | border arrivals | interior | exposure | destructions |
|---|---|---|---|---|---|---|
| P | v140 + `LAUNCHER_MIN_RND=0` | `_probe_border_raw` | 2 (2/15 games) | 0 | 9,550 | **11 (2/15 games)** |
| G | v140 + `LAUNCHER_MIN_RND=0` | `_probe_border_guard` | 15 (3/15 games) | 1 | 10,724 | **0** |
| Z | same + `EXILE_ON=False` | `_probe_border_raw` | 0 | 0 | 11,026 | **0** |

Exposure skew P-vs-G = 10.9%, inside `compare()`'s 15% limit.

---

## 3. THE THREE STOP CONDITIONS, ANSWERED

**(1) THE CHANGE IS NAMED, NOT INVENTED.** See §4 — two constants and one
two-line branch, all at named `file:line`, and the `EXILE_ON` form is copied
verbatim from an existing ablation tree (`bots/_v162exile0/doctrine.py:1518`,
gate at `bots/_v162exile0/raid.py:687`).

**(2) DO WE ALREADY DO THIS? — SPECIFIED-AND-WIRED, BUT NOT AS A BORDER
WEAPON.** `bots/_v223sealrepair/raid.py:909-932` ships EXILE: any enemy builder
at d^2 <= 2 of our launcher is thrown to the reachable site **farthest from OUR
core** (`raid.py:925`), and `raid.py:934-957` ships FERRY. **There is no
border-tile selector anywhere in the incumbent** — `grep -n 'border\|edge'` over
`bots/_v223sealrepair/*.py` returns only unrelated prose in `doctrine.py`.
⇒ **The THROW is a live behaviour; border landings are INCIDENTAL to the
farthest-tile ordering, not aimed.** This leg does NOT add aiming; it measures
whether the incidental landings kill.

**(3) MECHANISM OCCURRENCE — MEASURED, AND IT FAILS ON THE SHIPPED
CONFIGURATION.** *This is the finding that shapes the whole design and it is not
a hedge.*

Ran the SHIPPED tree `bots/_v223sealrepair` against `bots/_probe_border_raw`,
15 maps x 2 seeds = **30 games, seed block 91000**:

```
border throws 0   interior throws 0   in 0/30 games
exposure 19,207 victim-rounds        destructions 0
```

**Cause, verified on a single game (`midgard`, seed 91090):**
`{"winner":"A","turns":73,"win_condition":"core_destroyed"}` — we kill the probe's
core at r73, and `doctrine.py:1536 LAUNCHER_MIN_RND = 160` means
`main.py:613` returns False every round of that game. **No launcher is ever
built, so no throw is possible, so the weapon cannot fire.** Across the 30 games
exposure ran 525-651 victim-rounds per game, consistent with games ending far
inside r160.

⇒ **A #17 drive fired at the shipped configuration is UNDOSED BY CONSTRUCTION and
answers nothing.** ⛔ **AND IT MUST NOT BE READ AS "THE SHIPPED BOT NEVER
THROWS":** that zero is a property of *this local fixture* (a probe weak enough to
die at r73), not of the bot. Live, our median kill is r174 and our median death
r187, so a launcher deferred to r160 does exist in a large share of real games.
**The honest statement is: the local fixture cannot present the precondition
unless the weapon is ARMED, which is why §4 lifts the deferral in BOTH thrower
arms and why §7 forbids reading any game-share number off this leg.**

**Arrival rate once armed, measured:** with `LAUNCHER_MIN_RND = 0`, the immune
victim (cell G, never truncated) observed **15 border arrivals across 15 games,
in 3 of 15 games** — 1.0 arrival/game, concentrated. That is the number the dose
gate in §5 is sized on.

---

## 4. THE CHANGE — `file:line`, old -> new

Both thrower trees are copies of `bots/_v223sealrepair` (v140) and differ from it
and from each other ONLY in what follows. **Nothing else may be touched; a
byte-diff wider than this list invalidates the leg.**

**(a) `bots/_v224crashon/doctrine.py:1536` — ARM THE WEAPON**
```
-LAUNCHER_MIN_RND = 160
+LAUNCHER_MIN_RND = 0
```
Same edit, same line, in `bots/_v224crashoff/doctrine.py:1536`.
*Reason: stop condition (3). Without it the launcher is never built in this
fixture and every cell reads UNDOSED. This is an ARMING change, not a plank —
§7.*

**(b) `bots/_v224crashon/doctrine.py`, appended after line 1536 — the
ablation constant, in the established form**
```
+# QUEUE #17 crashdrive: gate ONLY the enemy-pickup exile throw. Same constant
+# name and same gate shape as bots/_v162exile0/doctrine.py:1518.
+EXILE_ON = True
```
and in `bots/_v224crashoff/doctrine.py`: `EXILE_ON = False`.

**(c) `bots/_v224crashon/raid.py` — the gate, inserted immediately BEFORE the
line that is `bots/_v223sealrepair/raid.py:925`, inside `_launcher_turn`'s EXILE
loop**
```
             except Exception:
                 continue
+            if not EXILE_ON:
+                continue
             far = sorted(sites, key=lambda t: t.distance_squared(self.core), reverse=True)
```
Identical insert in `bots/_v224crashoff/raid.py`.
**This gates the ENEMY throw and nothing else.** The `friendly_bots.append(...)`
branch above it and the entire FERRY block below (`raid.py:934-957`) are
untouched, so the two thrower arms differ in exactly one behaviour: whether an
adjacent enemy builder is thrown. The two-line insert shifts subsequent
`raid.py` line numbers by **+2**: the `ct.launch(bp, site)` exile call moves from
`:929` to **`:931`**, which is the line the mechanism metric names.

**Binding for Obligation 13:** `raid.py` is itself in the diff (direct path hit),
and `doctrine.py` binds to it through `bots/_v223sealrepair/raid.py:64
from doctrine import *`, so the changed constants reach the metric's call site by
import. **INTERSECTION: yes.** ⚠ At lock the arm trees do not exist, so
`prereg_check.py` reports OB13 as CANNOT-COMPUTE; **re-run it with `--fire` once
the trees are on disk and `git add -N`'d, where the same condition FAILs.**

---

## 5. THE FOUR CELLS, AND WHICH ONES ARE FORCED

15 maps (`tools/overnight.sh:68`) x 2 seats x 2 seeds = **60 rows per cell**,
seed block **93000** (disjoint from the 91000/92000 probe blocks). Seats are
swapped by flipping the cell's (ours, theirs) order; `tools/crash_cells.py`'s
`_crash_count` and `throws` are seat-agnostic because they parse the victim's own
output and the victim's own traceback path.

| cell | thrower | victim | role | REQUIRED reading |
|---|---|---|---|---|
| **P** | `_v224crashon` (`EXILE_ON=True`) | `_probe_border_raw` | **FORCED POSITIVE** | destructions **> 0** |
| **G** | `_v224crashon` (`EXILE_ON=True`) | `_probe_border_guard` | **FORCED NEGATIVE (victim-side)** | border arrivals **>= 20**, destructions **== 0** |
| **Z** | `_v224crashoff` (`EXILE_ON=False`) | `_probe_border_raw` | **FORCED NEGATIVE (weapon-side)** | enemy throws **== 0**, destructions **== 0** |
| **S** | `bots/_v223sealrepair` **unchanged** | `_probe_border_raw` | **DESCRIPTIVE** | reported, never read as a verdict |

**G is the victim-side forced negative:** same thrower, same maps, same seats,
same seeds; the ONLY difference is a `try/except` in the victim. If G dies too,
the unguarded query is not what kills and cell P may not be published.
**Z is the weapon-side forced negative:** same thrower build, launcher present and
still ferrying, exile branch gated off. It isolates the throw from everything
else that could put a victim on a border tile (spawn-on-border, self-walk, a
launcher of theirs). **Z is only readable if its launcher actually existed** —
liveness check: **>= 1 `LAUNCHER` entity creation in >= 50% of Z rows**, counted
off the saved replay (`tools/corpus/replay_builds.py`, or the raw createEntity
stream), never off any `print()`.
**S is the row's original question** (does the SHIPPED configuration deliver
border landings locally?) and is registered as DESCRIPTIVE because §3 already
shows its answer here is a fixture property.

### THE MECHANISM METRIC, AND WHERE IT COMES FROM
* **DESTRUCTION (primary): a traceback raised inside the VICTIM's own `main.py`
  carrying `GameError`**, counted by `tools/crash_cells.py::_crash_count`. **This
  is ENGINE-SIDE**: the engine prints it when it destroys the unit
  (`0x1ac5c -> Game::destroy_entity`). Our own tree's tracebacks and
  non-`GameError` exceptions are excluded, driven both ways in the tool's
  selftest.
* **BORDER ARRIVAL (dose): a Chebyshev jump >= 2** in the victim's own logged
  position between consecutive rounds — no builder can move that far — with the
  destination classified against the map header's REAL dimensions.
* **EXPOSURE (denominator): victim-rounds actually observed.**

**⛔ LOCAL-ONLY, AND IT DOES NOT TRANSFER.** The arrival and exposure streams come
from the VICTIM probe's `print(..., file=sys.stderr)`, captured locally by
`fcode run`. **The platform strips stdout in 30,664 of 30,664 `BotOutput`
events**, so this half of the instrument cannot exist in a live leg and no live
successor may pre-register it. The DESTRUCTION count is engine-side and is the
half that would survive — but only locally, where stderr is visible. **Nothing in
this leg reads OUR OWN stdout at any point**; that is the exact defect that made
v1 of `crash_cells.py` publish a false road-closing negative.

**⭐ A DESTRUCTION IMPLIES A BORDER TILE, BY THE VICTIM'S CONSTRUCTION — which is
what makes the crash count interpretable without trusting the arrival counter.**
`_probe_border_raw` queries only its own four cardinal neighbours, all of which
are in bounds on any interior tile, so it cannot raise there; and it **refuses to
step onto a border tile of its own accord**. ⇒ a `GameError` from its `main.py`
means it was STANDING on a border tile, which it can only reach by being thrown
or by being SPAWNED there. **Cell Z is the arm that excludes the spawn path**, and
it read 0 destructions on the same maps and seeds in the design-phase probe.
⇒ **the destruction count is itself a LOWER BOUND on border arrivals**, and the
probe's 11-destructions-against-2-observed-arrivals is internally consistent
rather than anomalous.

**⚠ THE ARRIVAL COUNTER UNDERCOUNTS, IN A KNOWN DIRECTION, AND THAT IS WHY THE
DOSE GATE IS READ OFF G AND NOT OFF P.** Two causes: (i) a throw can move a
victim by ONE tile (`can_launch` allows d^2 >= 1 from the LAUNCHER, which can be
a single step for the victim) and a 1-step displacement is indistinguishable from
a legal move; (ii) **a destroyed victim stops logging**, so an arm that kills
more observes fewer subsequent arrivals — immortal-time selection pointing at the
treatment, which is precisely the defect v3 of the tool was written to remove.
The probe shows it plainly: cell P recorded 11 destructions against only 2
observed arrivals, while the immune cell G recorded 15 arrivals and 0
destructions from the SAME thrower. ⇒ **cell G, which is never truncated, is the
unbiased estimate of the dose delivered in cell P.**

### OBLIGATION 12 — GATE RESOLUTION
* **DOSE GATE: cell G must deliver >= 20 border arrivals.** At the
  observable-at-lock rate of 1.0 arrivals/game, 60 rows implies ~60; the gate's
  two branches are separated by P(Poisson(60) < 20) < 1e-8. **The gate resolves at
  the registered n.**
* **BAR RESOLUTION.** The bar is a share of GAMES. At the per-cell n = 60 with
  local DEFF 0.98 and p-bar = 5.0%, the 95% half-width is **+-5.5pp** against a
  registered margin of **10.0pp**; pooled over the 240 registered rows it is
  **+-2.7pp**. **The margin exceeds the half-width at the per-cell n, which is the
  n the bar is actually read at** — stated here rather than left to the pooled
  number, which would flatter it.
* **PER-DESTRUCTION READING, for the record:** at 20 observed arrivals, an
  observed 0/20 has a Clopper-Pearson 95% upper bound of 16.8% and an observed
  20/20 a lower bound of 83.2% — the two do not approach each other, so the
  positive and the refuted branch cannot be confused at this dose.
* **UNRESOLVED DEFAULTS TO THE RESTRICTION.** If cell G delivers fewer than 20
  border arrivals, or any control is contaminated, **no verdict is published, no
  road is closed, and `QUEUE #17` stays open.** An UNDOSED cell answers nothing
  and may never fall through to "the weapon does not fire" — that fall-through is
  the exact false negative v1 of the instrument published.

---

## 6. DECISION RULE

**PRIMARY = MECHANISM COUNT, NOT GAME SHARE.** Game share may be flat, or may
move for reasons unrelated to the weapon (arming a launcher at r0 costs +10%
global scale), and it is not read here at all.

**KEEP — MECHANISM CONFIRMED**, all four required simultaneously:
1. cell G delivers **>= 20** border arrivals (the dose gate), and
2. cell P shows a weapon-attributable destruction in **>= 10.0%** of its 60 rows,
   and
3. cell G shows **0** destructions, and
4. cell Z shows **0** enemy throws and **0** destructions, with its launcher
   liveness check satisfied.
⇒ *Border throws kill an unguarded opponent and leave a guarded twin untouched
under the same throws; the weapon fires from the v140 chassis and the instrument
separates its arms.*

**REAL NEGATIVE — MECHANISM REFUTED, THE ROAD CLOSES LOCALLY:**
cell G delivers **>= 20** border arrivals **and** cell P shows **0** destructions
across its 60 rows.
⇒ *The dose landed on a deliberately maximally-vulnerable victim and nothing
died.* Under CLAUDE.md rule 6 this is a LOCAL closure: it retires the local
question and drops `#17` to the bottom of the queue; **it does not by itself
retire crash-induction against live opponents**, because the local victim is a
fixture we wrote.

**⛔ DROP BAND — "COULD NOT SEPARATE", NEVER "THE EFFECT IS ZERO".** Any one of:
* cell G delivers **< 20** border arrivals ⇒ **UNDOSED / UNRESOLVED** ⇒ the
  RESTRICTION. The leg answers nothing.
* cell G shows **> 0** destructions ⇒ **UNATTRIBUTABLE** — the guarded twin died
  under the same throws, so the unguarded query is not the killer. **Cell P may
  not be published**, however loud it is.
* cell Z shows **> 0** enemy throws, or **> 0** destructions, or fails its
  launcher liveness check ⇒ **CONTROL CONTAMINATED** — something other than our
  exile is putting victims on border tiles, or the control never armed. Nothing
  may be attributed to the weapon.
* cell P shows destructions in **> 0% but < 10.0%** of rows ⇒ **BELOW THE
  REGISTERED BAR AT THIS n.** Report the counts; re-screen at a higher n as a NEW
  leg with its own rows. This is **not** evidence of absence.
* P-vs-G exposure skew **> 15%** ⇒ `tools/crash_cells.py::compare` REFUSES the
  ratio. Per-cell counts may be reported; **no cross-cell rate may be quoted.**

**INSTRUMENT ALARM (halts the read, not a branch):** if cells P and Z disagree on
border arrivals while both read **0** destructions, or if `crash_cells.py
--selftest` does not pass on the exact revision that produced the rows, the rows
are not read at all.

---

## 7. ⛔ THIS IS NOT A SHIP SCREEN, AND THE ARMING CHANGE IS WHY

`LAUNCHER_MIN_RND = 160 -> 0` is an **ARMING change made so the weapon can be
observed**, and it is the deliberate reversal of a shipped decision: **LOKI-42
deferred the launcher precisely because each one adds +10% to the ONE GLOBAL
ADDITIVE cost scale, and bought early that surcharge is levied on the whole
game.** Consequences, registered so nobody reads them off later:
* **NO game-share, kill-round, or economy number from this leg may be quoted for
  or against shipping `LAUNCHER_MIN_RND = 0`.** The arms are not exchangeable on
  economy — that is the second cause `crash_cells.py::compare`'s refusal message
  names, and it applies here by construction.
* **No defence bar and no kill-round non-regression rider is registered**, and
  that is deliberate rather than forgotten: `DEFENCE_ADMISSION_BAR` binds a
  DEFENSIVE PLANK being considered for the tree. Nothing here is proposed for the
  tree. Kill round will very likely RISE in the armed arms (early scale), and
  that is expected, uninteresting, and not evidence about the weapon.
* **What a KEEP buys is permission to design a live leg**, not a ship. The live
  question — *what share of the real field is unguarded* — is untouched here and
  is already bounded from the archive at **<= 4.24%** on the admissible
  population (`docs/research/CRASH-CHANNEL-border-vs-interior-2026-08-12.md`).
  **A KEEP here does not overturn that bound; it only establishes that the weapon
  works when a victim IS unguarded.**

**HOT-TURN COST: neutral** (the `EXILE_ON=False` arm: *reduces*). The diff adds no
loop, no map scan and no per-tile work: (b) is a module constant; (c) is an early
`continue` that, when it fires, SKIPS an existing `sorted()` over <= 81 sites;
(a) allows an already-bounded build attempt (a `get_nearby_buildings` scan plus 4
cardinal `can_build_launcher` checks, all already in the incumbent) to run earlier
in the game rather than never. Budget 10,000us/unit/turn, worst observed
8,748us on 900-area maps. ⚠ **`get_cpu_time_elapsed()` reads ZERO locally**, so
the tree's own CPU guard cannot be exercised in this fixture and this rider is an
argument from the diff, not a measurement.

---

## 8. INTERACTION WITH THE LIVE LEGS

* **SEALFLOOR6** (`bots/_v238sealfloor6` vs `bots/_v223sealrepair`, LOCAL, 5,400
  rows, in flight): **no shared arm, no shared row, no shared metric.** The only
  real interaction is **CPU contention on the same box** — `crashdrive` must run
  as its own shard under the corefill discipline (or wait), and its 240 rows must
  never be pooled with SEALFLOOR6's. ⚠ **`bots/_v223sealrepair` appears in both
  legs** — as SEALFLOOR6's CONTROL and as `crashdrive`'s cell S and diff base.
  **Cell S's rows are generated fresh in this leg's seed block and may not be
  taken from, or contributed to, SEALFLOOR6's tape.**
* **SALTREF2** (remote, `worker@work-server-1`): different box, different arms,
  no overlap. No interaction.

---

## FALSIFIER

**If cell G delivers >= 20 border arrivals — proving the dose landed — and cell P
records ZERO weapon-attributable destructions across its 60 rows, the hypothesis
is refuted:** the crash weapon does not fire even against a probe built to be
maximally vulnerable, on the shipped v140 chassis, with the instrument's own
forced-negative arms behaving. `#17` then closes as REFUTED-LOCALLY rather than
UNDOSED, which is the outcome this leg exists to be able to reach.

**And it can lose the other way too, which is the point of a both-ways drive:**
if cell G's GUARDED probe also dies, the mechanism claim — that the unguarded
self-relative query is what kills — is refuted **even if cell P is loud**, and no
number from cell P may be published. If cell Z throws or kills anything, the
attribution to our exile is refuted outright.

**What would NOT falsify it, stated so it is not offered later:** a flat game
share, a slower kill round, a worse economy in the armed arms, or any result on
`bots/_probe_oov_raw` (position-invariant, cannot serve).

---

**PROVENANCE:** `QUEUE.md` (row 17) ·
`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` ·
`tools/prereg_check.py` · `tools/crash_cells.py` (incl. `--selftest`, 25/25 this
session) · `tools/kidnap_fate.py` (header) · `tools/arena.py` (header) ·
`tools/corefill.sh` (header) · `tools/overnight.sh:68` (the 15-map local pool) ·
`bots/_v223sealrepair/raid.py` · `bots/_v223sealrepair/main.py` ·
`bots/_v223sealrepair/doctrine.py` · `bots/_v223sealrepair/eco.py` (grep only) ·
`bots/_v131loki14/raid.py` · `bots/_v131loki14/doctrine.py` (grep only) ·
`bots/_v131loki14off/doctrine.py` (grep only) · `bots/_v162exile0/raid.py` ·
`bots/_v162exile0/doctrine.py` · `bots/_probe_border_raw/main.py` ·
`bots/_probe_border_guard/main.py` · `bots/_probe_oov_raw/main.py` ·
`bots/_probe_oov_guard/main.py` ·
`docs/research/CRASH-CHANNEL-border-vs-interior-2026-08-12.md` ·
`docs/research/PREREG-SPAWNPOCKET-2026-08-14.md` (house style only) ·
`docs/prereg/LEG-REGISTRY.md` · `scratchpad/crash_cells_s33.txt` ·
`scratchpad/crash_cells_s33_v2.txt` · `scratchpad/corefill_work.txt` ·
`docs/coordination.md` (grep for SEALFLOOR6/SALTREF2 only) · `CLAUDE.md`.
**Games run during drafting (design-phase only, no repo file written):** 30 rows
seed block 91000 (shipped tree vs `_probe_border_raw`) and 45 rows seed block
92000 (three-cell dose probe, arms built in the drafting agent's scratchpad).


## A1 — ADD-ONLY AMENDMENT (2026-08-14, BEFORE the leg exists: zero shard rows, no outcome column read by any lane)

**ARM TREES RENAMED — `_v224crashdrive` → `_v224crashon`, `_v224crashdrive_noexile` → `_v224crashoff`.**

**REASON, and it is a fixture-mechanics defect, not a design change.** The drafted
names collide: **`_v224crashdrive` is a literal SUBSTRING of
`_v224crashdrive_noexile`**, and `tools/overnight.sh` **scores by substring match
on the basename**. `tools/corefill.sh`'s guard 4 documents this exact failure with
its own worked example — *"`_v150cb` vs `_v150cbturret` reads ~100% for the
control"*. Left alone, cell Z (the **weapon-side forced-negative**, the cell that
makes the whole both-ways drive mean anything) would have scored against the wrong
tree, and the leg would have produced a confident, wrong instrument validation.
`corefill.sh` refuses such a pair up front, so this would have surfaced as a
refusal to start — but the names had to change either way. Caught by the builder
at stocking, before any row existed.

**WHAT CHANGES:** the two tree paths, and the OB13 `MECHANISM METRIC READS` path
that names one of them, which had to move with the tree or the intersection check
would read a directory that no longer exists.
**WHAT DOES NOT CHANGE:** the bar, the base rate, planned n, the cut-short floor,
the cell definitions, the dose, the falsifier, the segment, or the seed blocks.
The two arms remain byte-identical except `EXILE_ON`, verified after the rename.
