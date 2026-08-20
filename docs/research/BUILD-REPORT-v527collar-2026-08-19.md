# BUILD REPORT — `bots/_v527collar`, s51, 2026-08-19/20

Three mechanisms + two hygiene items, one master flag (`LOKI_FS_V527`, `False`
reproduces the parent), from `bots/_v526transit` **configured RDV-ONLY**.
Tree uncommitted, per instruction. **PAR=4** throughout — both full-pool shards
(PINCERPOOL, FLIPPOOL) reached their registered n and are closed in
`results.tsv`; PIDs recorded in `scratchpad/s51_v527_build/PIDS`, including
another lane's live grid (82027) and two dangling v520-era waiter shells, all
left untouched. Wall clock from `date -u` in the same shell call: headline
`04:08:24Z` → `04:19:xxZ`, M2 battery `SEALNT DONE 2026-08-20T04:20:21Z`,
report written `2026-08-20T04:24:35Z`.

`eco.py` and `raid.py` are **byte-identical to the parent** (md5-confirmed).
Only `doctrine.py`, `main.py` and `siege.py` differ.

---

## 0. THE PARENT CONFIG, DOCUMENTED AT ITS DEFINITION SITES

The brief's first instruction. `bots/_v526transit` was copied and reconfigured
**before any v527 code was written**:

| line | file | value | why |
|---|---|---|---|
| `doctrine.py:4850` | `FS_V526_TEMPO` | **`False`** (was `True`) | v526 report §6: this plank ALONE reads `k<=200` **−10.83 pp OUTSIDE**, median kill 173 → 237, replicated across two seed blocks |
| `doctrine.py:4909` | `FS_V526_WALK` | `False` (confirmed unchanged) | never shipped; M4's cause was routed out of the transit subsystem |
| `doctrine.py:4876` | `FS_V526_RDV` | `True` (unchanged) | the **adopted** plank — benign-to-positive on every cell, ARC_DUP 69 → 6 |

Verified in-process, not asserted: with `FS_V526_TEMPO = False`,
`fs_crew_seat()` returns **3** and `fs_muster_wait()` returns **8** — the v525
constants — i.e. the tempo plank's two read sites fall through to the parent.

**Digest chain (all three frozen and re-verified at write time):**

```
PARENT_FREEZE.md5   bots/_v526transit  doctrine c2c4006e… eco bba326d7… main 2ba15111…
                                       raid 3b3a0456…     siege bd59b189…
CHILD_AT_BIRTH.md5  bots/_v527collar before any v527 code (doctrine a877e207… = parent
                    + the TEMPO flip and its comment only; other 4 files identical)
TREE_FINAL.md5      doctrine 9c1d97cb…  eco bba326d7…  main 93a85f57…
                    raid 3b3a0456…      siege 0ee5bb2d…
```

⚠ **ONE TREE EDIT LANDED AFTER THE HEADLINE, AND IT IS PROVED INERT RATHER THAN
ASSERTED.** The headline ran against `siege.py` md5 `734026be…`; the final tree
is `0ee5bb2d…`. The difference is the §7 comment correction only, and
`ast.dump(ast.parse(old)) == ast.dump(ast.parse(new))` is **True** — identical
syntax trees, so the behaviour the headline measured is the behaviour that
ships. (An earlier counter-only edit *during* the first headline run was handled
the other way: that run was **killed and restarted from zero**, because a tape
that mixes two trees is not worth defending even when the edit is write-only.)

⭐ **Cross-check that cost nothing:** the child's `doctrine.py` at birth is
identical to v526's own `arm_rdv_only/doctrine.py` **except for the comment
block** — and the other four files are md5-equal. The RDV-only object this
build parents on is the same object v526 measured.

---

## ⛔ TOP LINE

**The headline is a NULL on every currency column, and it is UNDERPOWERED
rather than reassuring.** n=448/arm, 0 tracebacks in 1,344 games. On `k≤200`
(−2.23 pp) and median kill (+9) the **known-zero arm moved further than the
treatment** (−2.90 pp, +14) on play that is byte-identical to the parent by
construction. `DEFENCE_ADMISSION_BAR` is **neither cleared nor failed**: the
band on `k≤300` cannot exclude an 11-point regression, and it cannot exclude
zero.

**That was predictable from the dose and the dose was measured first:** M1 fires
2–5 times per 24 games, M2 dispatches 2–4, M3's opportunity-cost switch fires
**0 of 120–175 opportunities**. A rare-state plank set measured at n=448.

**The one plank that moved its own registered statistic is M2's**, on the
instrument built for Magnus's marker: `[sealed & no-turret]` rounds/game
**69.2 → 40.7**, worst run **622 → 258**, with eco non-regression confirmed at
four windows. The 780-round sealed-and-turretless signature reproduces in the
*parent* at 622 rounds; v527 more than halves it.

**Three things were found that are worth more than the headline:**
* **Two thirds of M2's mandate is ALREADY SHIPPED** (`_v518_early_sentinel`) and
  would have been a leg testing a feature we already have — §2.1.
* **A dose counter over-reported 104×** and its wrong figure had already reached
  a code comment as a fake measurement — caught with a control, §7.
* **The v523 arc-merge is absent from this lineage entirely**, and the
  same-sounding v520 arc channel that IS live would have been deleted by a
  careless drop — §4.1.

---

## 1. M1 — THE BUNKER SWAP (`FS_V527_BUNKER`)

Magnus, marker 11: *"(19,18) r28 builders walled in themselves; switching to
sentinels is probably not good"*; marker 14: *"maybe it should plant
sentinels?"*.

A ring raider that is **TRAPPED** (no legal cardinal move) or standing at a
**completed-or-near collar** destroys its own adjacent barrier and builds a
**core-aimed sentinel** in the freed slot. A ring seat carrying our SENTINEL is
still a denied seat (`_fs_denied` counts any blocking building of ours), and a
sentinel's ray ignores obstacles, so it shoots the core through the rest of the
ring.

### 1.1 THE MEASURED HOLE IT FILLS

`_fs_try_sentinel` scores only the ≤4 tiles **orthogonally adjacent to the
body**, minus the ring (`FS_SENTINEL_OFFRING`) — and a ring raider stands **on**
the ring. Its own hand excludes its own candidates. v516's `SENTREACH` answers
this by *walking* the body to a site; M1 answers it **without moving**, which is
the only answer available to a body that cannot move.

### 1.2 IT FAILS CLOSED — AND THAT IS THE FIRST CLAUSE, NOT THE CAVEAT

Magnus's archipelago r28 state is the **registered negative** (6v12 conveyors,
100v130 collected, bloated scale, unclosable collar). The swap inherits ruling
2's economy gate **whole** — `_fs_sentinel_ok`: the salt/eco disjunction, the
collar reserve, the purchase cap, the ti floor — and **adds a magazine clause**:
the team ammunition balance must already sustain `FS_V527_MAG_SHOTS` (3)
sentinel shots. **Banked ammunition, never a promise to convert** — a turret
that cannot fire is a 30 Ti barrier that costs 30 Ti.

### 1.3 THE SEAT NEVER FLICKERS — BY CONSTRUCTION, AND IT IS TESTED

Order of operations: **every gate is checked before anything is destroyed**
(`can_fire_from` on a real core tile, funds, gate, magazine, per-body cap) →
`destroy` (free, no cooldown, so it composes with a same-round build) →
`build_sentinel` → **if the build is still refused, rebuild the barrier THIS
TURN**. Worst case is one barrier's price and **zero open-seat rounds**.

### 1.4 M1b — THE DEFENDED-TILE PREFERENCE

Magnus, marker 5: *"(1,16) r36 perfect spot for a Sentinel, defended behind the
Launcher already there"*. The v514 site scorer prices standoff, gun-axis and
side redundancy and had **no term for our own standing pieces**. A site inside
one of OUR launchers' pickup envelope (d²≤2, engine-read) is a site whose
attacker gets thrown off it. **Ordering term, never a filter:** +20, sized
**below** `FS_SENTINEL_GUNAXIS_PENALTY` (64) so it can never buy a tile back
onto a visible enemy gunner's ray, and **below** `FS_SENTINEL_SIDE_PENALTY` (24)
so it cannot collapse the twin onto one side.

---

## 2. M2 — THE PURCHASE SURVIVES THE RAIDER (`FS_V527_PSURV`)

### 2.1 ⛔⛔ THE INCUMBENT GREP CHANGED THE PLANK — TWO THIRDS OF THE MANDATE IS ALREADY SHIPPED

Run **before** the code, per CLAUDE.md (*"grep the incumbent before
pre-registering any plank — the cheapest null is a leg testing a feature we
already ship"*).

`_v518_early_sentinel` (siege.py, v518 change 2a) already sits **above rung 1**
in the ladder. Its entire guard is:

```python
live <= FS_V518_EARLY_MAX_LIVE (= 0)
    and _fs_sentinel_ok(...) and _fs_try_sentinel(...)
```

— i.e. *"while no forward sentinel is alive and the gate is open, the turret
outranks the barrier"*, **unconditionally, at every value of `orth_open`**.
`LOKI_FS_V518` and `FS_V518_EARLYSITE` both ship `True`.

The mandate's clause (b) ("at 7-of-8 seats … the turret outranks the last
barrier") adds `orth_open <= 1` — **strictly narrower** — and `SLOT_FWD_GUN == 0`
— **also strictly narrower** than `live == 0`, since a sentinel bought and then
killed reads `live 0` with the monotone count at 1. The mandated turret-first
ordering is the same conjunction.

⇒ **Both are INERT BY CONSTRUCTION.** A guard that is a shipped guard ∧ two
extra tests can never win a round the shipped guard did not already win. They
are **coded, flagged off** (`FS_V527_PSURV_LASTSEAT = False`,
`FS_V527_PSURV_TFIRST = False`) and left greppable so the finding is
**checkable rather than claimed**; the known-zero arm proves they cost nothing.

### 2.2 WHAT SURVIVES THE GREP IS WHAT THE MARKER ACTUALLY NAMES: THERE WAS NO BODY

`FS_MAX_REPLACE = 2` caps raider replacements **for the whole match**. The
marker games hold a sealed collar for hundreds of rounds with both replacements
long spent — so the shipped clause is correct, funded, and **has nobody to run
it**.

**Shipped:** `FS_V527_PSURV_EXTRA = 2` additional replacements, **only** inside
the PSURV state — published crew phase `FS_PH_SEALED..FS_PH_KILL_NEAR`, **no
forward turret ever bought** (`SLOT_FWD_GUN` monotone, survives the buyer), and
no live forward-sentinel beat. Outside that state the expression is the
parent's.

⛔ **NO NEW STORE CHANNEL.** All 8 phase codes are taken and the SLOT_FS word is
full to bit 31. Every input is already published, so the Core derives the state
rather than being told it. *A channel nobody needs is the v523 arc-merge
defect.*

⚠ **This plank spends BODIES, which is the v526 M6 hazard class** (a body is
78–105 Ti at live scale; M6 cost `harv30` 2.34 → 1.98 and −10.83 pp on
`k<=200`). `harv30` non-regression is therefore **this plank's own falsifier**,
measured on the same tape as its effect (§4e), not a courtesy check.

---

## 3. M3 — THE SEAL-PATH ORDER (`FS_V527_SEALPATH`)

Magnus, marker 14: *"(10,19) r21 builder blocked its way to the next barrier
with this barrier"*.

The census orders seats on arc / NW-bias / wear / distance and has **no term for
whether the tile we are about to fill is the tile we must walk through** to
reach the seats we still owe. `_v527_path_cuts` runs a **bounded flood** from
the body over the ring + one apron tile (`FS_V527_PATH_DSQ = 20`), with the
candidate treated as blocked, and asks whether the remaining owed seats are
still reachable (arrival-by-adjacency, the convention every build in this bot
uses).

⛔ **IT ANSWERS ONLY THE QUESTION IT CAN ANSWER.** Seats already unreachable
*before* the barrier are excluded by a **control flood** — run only when the
first flood found a loss, so the common case pays for one flood, not two. Without
it a walled pocket would be charged to our barrier and the clause would veto
rung 1 on maps where it changes nothing.

`_v527_seal_pick` returns the first adjacent seat that does **not** cut, hoisted
to the front of the build order; when nothing cuts, the loop is the parent's
tile for tile. When **every** adjacent seat cuts **and the sentinel gate is
open**, marker 14's opportunity-cost switch fires and the turret takes the
round. **The gate is the parent's, unrelaxed** — with it shut this falls through
to the parent exactly: seal, and pay for the lap.

---

## 4. HYGIENE — BOTH ITEMS, ONE OF THEM A NON-CHANGE WITH EVIDENCE

### 4.1 THE v523 ARC-MERGE PUBLISH — ALREADY ABSENT, AND THE NEAR-MISS IS THE POINT

The brief asked to DROP it (1,341 publishes, 0 credits). **It is not in this
lineage and there was nothing to drop.** v524 parented on `_v522floor`, skipping
v523 entirely:

```
LOKI_FS_V523  FS_V523  arc_credit  ARC_UNION  SALT_UNION  _v523
      0          0          0          0          0         0     (all 5 files)
```

⛔ **AND A CARELESS "DROP THE ARC PUBLISH" WOULD HAVE DELETED A WORKING PLANK.**
`FS_V520_ARC_PUBLISH` is a different, superficially similar channel that IS
live and IS consumed twice — `siege.py:2147` (peer deconfliction: the `ARC_DUP`
alarm v526 drove 69 → 6) and `siege.py:898` (the census's `arcp` ordering term).
Recorded so the next build does not re-derive the distinction.

### 4.2 THE TWO STALE DOCTRINE COMMENTS — BOTH CORRECTED IN PLACE

| site | what it claimed | what is true |
|---|---|---|
| `doctrine.py:4691-4693` | *"`LOKI_FS_V524 = False` reproduces the parent's four-map collision exactly, **byte-for-byte**, with no other code path touched"* | **No battery in that build measured it.** v524's byte-identity table (`BUILD-REPORT-v524exact:114-134`) is v524 **as fired** vs the parent — identical on midgard/yulerune/archipelago, DIFFERS on ragnarok/frostgate. The flag-off arm the sentence describes **was never run.** A plausible inference wearing the typography of a measurement, in the file every session loads. Downgraded to what the code supports. |
| `doctrine.py:4697-4699` | the fresh `known_map_for` call is *"**cached** into `self.map_grid` exactly as the Core/builder call sites already do"* | **It describes the FIRST DRAFT, which was a correctness bug removed before v524 shipped.** `self.map_grid` is also the guard on `main._builder`'s map init (`main.py:1325`), and the v521 gatefix read runs *before* it — caching there silently lost `self.map_walls`/`self.map_ores` for that unit for the whole match (diverged at r280, winner flipped, units 6 vs 17). The shipped code **recomputes, deliberately uncached**. |

---

## 5. VERIFICATION

### (a) FLAG-OFF BYTE-IDENTITY **18/18** — AND A NEGATIVE CONTROL THAT FAILED INFORMATIVELY

`byte_identity.py`; `NOISE_ON = False` on **both** sides, `--tle 0`, seed 527919,
replay bytes `cmp`'d (`--seed` alone does not pin a game — v518 finding 1/2).

```
ARM 1  LOKI_FS_V527=False  vs the RDV-ONLY PARENT
       IDENTICAL on 18/18 (9 maps x 2 seats), 0 tracebacks     -> PASS
ARM 2  v527 AS FIRED       vs the same parent  (NEGATIVE CONTROL)
       DIFFERS on 1/14 active cells (antler seat A only)       -> "FAIL"
       IDENTICAL on 4/4 standdown cells (midgard, archipelago) -> as required
```

⛔⛔ **THE ARM-2 "FAILURE" IS A FIXTURE PROPERTY, NOT A PLANK PROPERTY, AND IT IS
MEASURED RATHER THAN ARGUED.** On 30 deterministic cells the bunker guard is
reached and **ARMED 5,814 times**, and the ECONOMY GATE (`_fs_sentinel_ok`)
refuses **all 3,732** of the asks that get that far — **0 fires**. The same tree
fires 2–5 times per 24 games with `NOISE_ON=True`. So on this fixture
"identical" means *the plank did not fire*, not *the plank does nothing*.

⇒ **The known-zero claim (ARM 1) is unaffected and stands: 18/18.** What ARM 2
loses is its power to prove reachability — which is why the M1 guards are driven
directly instead (§5c), and why the dose is measured separately (§5e).

### (b) AST DERIVED-DEFAULT SCAN — 0 HITS, WITH ITS POSITIVE CONTROL

```
GUARD: pos=True neg=False if=True
v527 derived defaults:  doctrine.py 0 · siege.py 0 · main.py 0
inherited (v526/525/524/522/521/520/519/518): 0 each
REAL-CASE CONTROL (FERRY_HOME_ON reads FS_CREW_ON, the known v515 hazard): 2
TOTAL: 0    RESULT: PASS
```

⭐ **COVERAGE EXTENDED, AND IT FOUND SOMETHING.** v526 scanned `doctrine.py`
alone; v527 scans doctrine + siege + main. That surfaced 2 inherited hits at
`siege.py:63` (`FS_V524_CRIPPLE_GRIDS` decoding `FS_V524_*_CODE` at import).
**Reclassified, not suppressed:** those are map-code **DATA constants** that no
flag ever changes, so decoding them at import is not the v515 hazard (which is a
module-level default reading a **FLAG**). The scanner keeps full power on the
real class — the FERRY_HOME_ON control still fires.

### (c) M1 GUARD MUTANTS — EVERY GUARD DRIVEN TO BOTH VERDICTS

`mutants_m1.py`, in-process (see §5a for why not on games).

```
arm             fired  sentinel  destroyed  barrier_back
CONTROL          True      True       True        False     <- must fire
MUT-GATE        False     False      False        False     <- _fs_sentinel_ok False
MUT-FUNDS       False     False      False        False     <- bank < cost+floor
MUT-MAG         False     False      False        False     <- magazine < 3 shots
MUT-ARMED       False     False      False        False     <- not trapped, collar open
MUT-NOSITE      False     False      False        False     <- no adjacent barrier
MUT-NOFIRE      False     False      False        False     <- can_fire_from False
MUT-CAP         False     False      False        False     <- per-body cap spent

RESEAL   acts: [('destroy',(6,5)), ('barrier',(6,5))]   -> PASS, same turn, 0 open rounds
FS_V527_BUNKER=False fired: False      LOKI_FS_V527=False fired: False
RESULT: PASS
```

**The two mandated mutants are the first two rows: gate-open-but-unfunded does
NOT fire; funded-but-gate-closed does NOT fire.**

⚠ **THE HARNESS CAUGHT ITS OWN DEFECT FIRST.** The falsifier originally patched
`doctrine.FS_V527_BUNKER` and reported PLANK-OFF **FIRED** — because `siege.py`
does `from doctrine import *`, binding the constants into siege's namespace at
import. A harness artefact, not a bot defect (the shipped bot takes the value at
import, so a doctrine `False` really does gate it). Recorded because a falsifier
that fails for its own reasons is worth as little as one that never fails.

### (d) STANDDOWN ASSERTION — 0 SIEGE CLAUSES ON BOTH GATED BOARDS

```
archipelago (GATED)    V527 clauses reached = 0   BUNKER = 0   PICKASK = 0   tb 0
midgard     (CRIPPLE)  V527 clauses reached = 0   BUNKER = 0   PICKASK = 0   tb 0
```
6 games. Independently corroborated by the byte-identity standdown cells (4/4
IDENTICAL in **both** arms).

### (e) THE DOSE — MEASURED, BECAUSE THE HEADLINE IS UNREADABLE WITHOUT IT

24 games (8 maps × 3 seeds, `NOISE_ON=True`), `dose_arm` with the V527 tape and
a funnel counter. **⚠ These counts are NOT reproducible run-to-run** —
`NOISE_ON=True` re-rolls the spawn salt per process — so they are magnitudes,
not constants (BUNKER FIRE read 5, 3 and 2 on three runs of the same cells).

```
BUNKER funnel (7,581 asks):  4,675 not armed · 2,250 GATE · 647 cap · 4 mag · 2-5 FIRE
BUNKER FIRE      2-5   in 2-5 of 24 games      BUNKER RESEAL   0  (fallback never needed)
DEFHIT (M1b)     5-11  in 4-5 games            PSURV ARM       8-10 in 8-10 games
REORDER (M3)     25    in 7 games              PSURV DISPATCH  2-4  in 1-2 games
SELFCUT (M3)     120-175 in 14-16 games        SWITCH (M3)     0    in 0 games
tracebacks 0
```

**Three things this says, and only the first is comfortable:**
1. **Every swap fired with the magazine already banked** — observed `ammo` at
   fire time 300, 300, 30, i.e. ≥3 sentinel shots. The fail-closed clause holds
   in play, not only in the mutants.
2. **M3's opportunity-cost switch has NEVER FIRED (0 of 120–175 all-cut
   states).** The gate was shut every time. The clause is present, reachable in
   principle, and carries **zero dose** in this configuration.
3. **M1 and M2 are rare-state planks** — 2–5 and 2–4 events per 24 games.
   That is a small dose to hang a 448-game currency read on, and §6 must be read
   in that light.

### (f) THE M2 SIGNATURE — THE MARKER'S OWN STATISTIC, AND IT MOVES

`instrument527.py` injects a per-round Core tape into **both** trees (every
substitution asserts its match count). Reader `sealnt_read.py` is self-tested
against three synthetic tapes driven to different verdicts, including one that
catches a reader blind to the turret column. n=48 games/arm, 0 tracebacks,
0 tape errors.

| | parent | v527 |
|---|---|---|
| `[sealed & no-turret]` rounds / game | **69.2** | **40.7** |
| longest such run — **max** | **622** | **258** |
| longest such run — mean | 65.2 | 38.0 |
| games with a run ≥ 50 | 11 (22.9%) | 11 (22.9%) |

⭐ **The 780-round sealed-and-turretless signature from Magnus's marker game
reproduces in the PARENT at 622 rounds, and v527 more than halves the worst
case.** The *incidence* of long stretches is unchanged (11/48 both); what moves
is their *length*.

**The eco falsifier, and the first version of it was the wrong window:**

```
             hv@r30  hv@r100  hv@r150  hv@r300  hv@r500
parent        2.42     3.10     3.40     3.62     3.67
v527          2.42     3.21     3.38     3.58     3.73
```

⛔ `hv30` read **2.42 vs 2.42, identical to two decimals** — and that is not a
pass, it is a **constant column**. `FS_V527_PSURV_EXTRA` can only spend once the
collar is published SEALED, which cannot happen by r30, so hv30 is
*structurally unable* to register this plank's cost. Re-measured where the spend
actually lands: **every window within ±0.11 harvesters, no direction.** The eco
non-regression holds on an instrument that could have moved.

---

## 6. THE HEADLINE

n=**448/arm** (8 maps × 28 seeds × 2 seats; the brief's 450 is not divisible by
the 16-cell panel), 3 arms interleaved per cell, PAR=4, **0 tracebacks in 1,344
games**. Opponent `bots/_v488beltbreak2`.

```
arm             n   wins%    <=r150     <=r180     <=r200     <=r250     <=r300  medkill ourcore  r1000
parent        448   74.1%  125(.279)  152(.339)  170(.379)  218(.487)  238(.531)    183     100     39
flagoff       448   73.2%  105(.234)  138(.308)  157(.350)  203(.453)  232(.518)    197     106     39
v527          448   71.9%  109(.243)  139(.310)  160(.357)  194(.433)  217(.484)    192     107     41
```

| contrast | wins | k≤200 | k≤300 | medkill |
|---|---|---|---|---|
| **flagoff (KNOWN-ZERO) vs parent** | −0.89 (hw 5.77) | **−2.90** (hw 6.30) | −1.34 (hw 6.54) | **+14** |
| **v527 vs parent** | −2.23 (hw 5.81) | −2.23 (hw 6.32) | −4.69 (hw 6.55) | +9 |

### 6.1 ⛔ THE KNOWN-ZERO ARM IS THE REFERENCE, AND ON TWO COLUMNS IT MOVES FURTHER THAN THE TREATMENT

`flagoff` is `bots/_v527collar` with `LOKI_FS_V527 = False`, **proved
byte-identical to the parent on 18 of 18 deterministic cells**. It cannot differ
from the parent by construction, and it read **−2.90 pp on k≤200** and
**+14 rounds of median kill**.

| column | v527 delta | known-zero excursion | ratio |
|---|---|---|---|
| k≤200 | −2.23 pp | **−2.90 pp** | **0.8× — NOT separated from noise** |
| medkill | +9 | **+14** | **0.6× — NOT separated from noise** |
| wins | −2.23 pp | −0.89 pp | 2.5×, inside the naive band |
| k≤300 | −4.69 pp | −1.34 pp | 3.5×, inside the naive band |

⇒ **v527 reads NULL on every currency column.** On the two kill-speed columns
the treatment moved *less* than a control that cannot move at all.

### 6.2 `DEFENCE_ADMISSION_BAR` — NEITHER CLEARED NOR FAILED, AND SAYING SO IS THE POINT

The bar is `k≤300` non-regression, and it is scored as a **fail-to-exclude**.
Per CLAUDE.md that class must be **restated as an exclusion before any
correction is applied**, or a design effect launders a weak null into a
confident one. Restated: *does the interval exclude a meaningful regression?*

With δ = −4.69 pp and naive hw = 6.55, the 95% band is roughly **[−11.2, +1.9]
pp** — and the known-zero caveat says naive half-widths understate the real
spread by **~2×** on derived kill columns at this n, so the honest band is wider
still. **We cannot exclude an 11-point regression, and we cannot exclude zero.**

⇒ **The bar is not cleared. The leg is UNDERPOWERED for it**, which is the
predictable consequence of a 2–5-event-per-24-games dose (§5e) measured at
n=448. This is the failure mode CLAUDE.md names: *"STOP CALLING UNDERPOWERED
LEGS … buy the power before writing the verdict."*

### 6.3 PER MAP — wins/n  [k≤300]  {k≤200}

```
map            parent            flagoff           v527
antler         40/56 [31] {21}   37/56 [30] {16}   38/56 [27] {15}
atoll          28/56 [16] {12}   37/56 [15] { 8}   27/56 [11] { 5}
drakkarfjord   53/56 [44] {41}   51/56 [41] {39}   53/56 [39] {34}
fjordgate      40/56 [30] { 8}   34/56 [25] {14}   38/56 [29] {18}
glacierkeep    50/56 [34] {28}   45/56 [34] {25}   48/56 [35] {26}
midgard        30/56 [14] { 6}   36/56 [22] { 8}   27/56 [13] { 6}
nordkap        42/56 [28] {18}   40/56 [26] {13}   41/56 [25] {20}
yulerune       49/56 [41] {36}   48/56 [39] {34}   50/56 [38] {36}
```

⛔ **midgard is CRIPPLE — the plank is OFF there** (§5d proves 0 clauses), yet
the three arms read 30 / 36 / 27 wins. **A 9-win spread on a board where the
treatment provably cannot act** is this fixture's noise floor shown directly,
and it is the same magnitude as every difference claimed above. fjordgate shows
the mirror image: `{k≤200}` 8 → 14 → 18, with the *known-zero* arm supplying
most of the movement.

### 6.4 FAILURE REEL (rule: earliest our-core-death per map, v527 arm, capped at 5)

```
map            turn  seed seat  replay
antler          125   23   B    scratchpad/s51_v527_build/head/rep/v527_antler_s23_B.replay26
fjordgate       131   22   A    scratchpad/s51_v527_build/head/rep/v527_fjordgate_s22_A.replay26
atoll           144   11   B    scratchpad/s51_v527_build/head/rep/v527_atoll_s11_B.replay26
midgard         151   25   B    scratchpad/s51_v527_build/head/rep/v527_midgard_s25_B.replay26
nordkap         185    3   B    scratchpad/s51_v527_build/head/rep/v527_nordkap_s3_B.replay26

EXTENSION (labelled, not part of the reel) -- the 2 latest-kill wins:
drakkarfjord    917    7   B    .../v527_drakkarfjord_s7_B.replay26
fjordgate       896   17   A    .../v527_fjordgate_s17_A.replay26

deaths 107 of 448 (23.9%)  ·  r1000 games 41
```

---

## 7. INSTRUMENT HYGIENE — A COUNTER THAT OVER-REPORTED **104×**, CAUGHT WITH A CONTROL

M3's dose counter first compared the chosen seat against `needed[0]`. **The
parent does not build on `needed[0]`** — it builds on the first seat in census
order that is *orthogonally adjacent*, because the build loop skips the rest.
The wrong baseline counts every round whose census head is merely out of reach.

Measured on the **same 30 deterministic cells, both counters, same games**:

```
REORDER, baseline = needed[0]        (BROKEN)    624
REORDER, baseline = first ADJACENT   (CORRECT)     6      <- 104x over-report
SELFCUT  (the fix does not touch it -- a CONTROL) 108 vs 108
```

The control is what makes this checkable: only the counter that was wrong moved.
Caught before any number was banked — but **the wrong figure had already been
written into a code comment as "~10x (measured: 624 against 62)", and the 62 was
never measured.** Both the counter and the comment are corrected in the tree.

⚠ **Consequence for the report above:** every M3 dose figure quoted in §5e is
from the corrected counter. The first dose run's `REORDER 474` is discarded.

---

## 8. ARTIFACTS

See `scratchpad/s51_v527_build/ARTIFACTS.md` for the full table. Totals:
**0 tracebacks and 0 CPU-timeout lines across every game this build ran**
(1,344 headline · 96 M2-signature · 36+36 byte-identity · 24+24 dose ·
30+30 deterministic dose scan · 6 standdown · 3 smoke = **1,659 games**).

---

## 9. WHAT THE BUILDER IS BEING ASKED TO DECIDE

Raw data above; verdicts are the builder's. The three facts that bear on them:

1. **The headline is a NULL on every currency column, and it is underpowered
   rather than reassuring.** On k≤200 and medkill the known-zero arm moved
   further than the treatment. `DEFENCE_ADMISSION_BAR` is neither cleared nor
   failed; the band cannot exclude an 11-point k≤300 regression.
2. **The one place a plank moved its own registered statistic is M2's:**
   `[sealed & no-turret]` rounds/game 69.2 → 40.7 and the worst run 622 → 258,
   with eco non-regression confirmed at four windows on an instrument that
   could have moved. That is Magnus's marker signature, directly attacked.
3. **Two thirds of M2's mandate and all of M3's opportunity-cost switch carry
   zero dose** — the first because the incumbent already ships it (§2.1), the
   second because its gate was shut in 120–175 of 120–175 opportunities (§5e).
   Both are shipped flagged-off or inert, and both are cheap to retire.

---
## BUILDER VERDICT LINES (s51)
* Headline: NULL AND UNDERPOWERED BY DOSE (M1 fires 2-5/24 games; M3 0 opportunities taken;
  the known-zero moved further than the treatment on the kill columns) — no currency claim
  either way; the merge build's composite + the final full-pool read carry the pricing.
* **THE MARKER SIGNATURE MOVED — the plank's own statistic: [sealed & no-turret] 69.2→40.7
  rounds/game, worst run 622→258.** Magnus's 780-round class reproduces in the PARENT (622)
  and is halved by M2's surviving half (the replacement-cap fix; two-thirds of M2 was already
  shipped as _v518_early_sentinel — verified subset, kept flagged-off greppable).
* ADOPTED into the merge as-built (fired config): mechanisms mutant-verified 8/8, fail-closed
  gates driven both ways, doses small but all in the intended direction, no measured downside.
* Instrument catches banked: the 104x over-reporting dose counter (corrected before any number
  travelled), hv30 constant-column, and the v523 arc-merge NOT being in this lineage (the
  planned "drop" would have deleted v520's live arc channel — a careless hygiene item caught
  by reading before cutting).
