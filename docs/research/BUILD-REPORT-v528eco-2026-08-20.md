# BUILD REPORT — `bots/_v528eco`, s51, 2026-08-20

Two shipped changes + one shipped-but-**measured-inert** third, one master flag
(`LOKI_FS_V528`, `False` reproduces the parent), from parent `bots/_v526transit`
configured **RDV-ONLY** (`FS_V526_TEMPO = False` set at its definition site;
`FS_V526_WALK` confirmed already `False`). v526's own build report measured
M6/TEMPO carrying that build's entire regression alone, so the shippable object
in the parent tree — and therefore the baseline here — is `FS_V526_RDV` alone.

**Tree uncommitted**, per instruction. Wall clock at write time, from `date -u`
in the same shell call: **`2026-08-20T05:09:39Z`**.

---

## ⛔ TOP LINE

**No stop condition. 0 tracebacks in 1,440 headline games + 120 mechanism games
+ 176 byte-identity games.** `DEFENCE_ADMISSION_BAR` is **not** breached — the
ITT share of ALL games ending in a core kill by r300 **rises** 0.481 → 0.531.

**Both shipped planks met a mechanism bar and one missed its mandated target:**

* **M5 `FS_V528_CONNCOST` — MET, decisively, on the metric the plank optimises.**
  Pick-time connection regret: parent **80.671 mean, 74.9% of 3,698 decisions
  nonzero**; v528 **0.000, 0 of 2,404**, with the anti-lock's entire cost at
  0.250 of a round.
* **M4 `FS_V528_WALK` — PARTIAL. The mandate's bar was 0 mid-map stalls; the
  measured result is 13 → 7** (‑46%), attributable to the one predicate. The
  aggravated mutant reads 25, so the scanner sees the mechanism in both
  directions. Seven stalls of a **second, nav-silent** family survive.
* **`FS_V528_WIRE` — BUILT, SHIPPED, AND MEASURED INERT.** It never fires on any
  fixture we have: byte-identical to the parent on **16/16** deterministic
  cells, **0 defer events in 116 instrumented games**, and root-caused
  (`wire_pending` is populated 3 times in 10 games and all 3 already had an
  acceptor). `byte_identity.py`'s overall `RESULT: FAIL` is **entirely** this
  plank's "never fired" control; every other arm passed.

**Headline, n=480/arm vs `bots/_v488beltbreak2`, 8-map panel, all cells INSIDE
the half-width.** The one number that is materially larger than the known zero
and in our favour is **cumulative delivery over all games: 878.0 → 1,027.0 mean,
against a byte-identical known-zero drift of +37.6.** Wins move +4.38 pp against
a +1.04 pp known zero — 4.2x the zero, still inside. `k<=200` is **exactly flat
(+0.00 pp)** and smaller than its own known zero.

---

## ⛔ FILE DISCIPLINE — THE MERGE WITH v527 IS A MECHANICAL UNION

**Only `eco.py` and `doctrine.py` differ from the parent.** `main.py`,
`raid.py` and `siege.py` are byte-identical to the parent **and to
`bots/_v526transit`'s originals** — md5-confirmed at freeze and again at write
time. The sibling v527 build owns those three files; there is no overlapping
hunk.

```
bots/_v528eco/doctrine.py = 2bb7c4afb1c8f83c004f8b86d836f91b   (DIFFERS: +126 / -0 lines)
bots/_v528eco/eco.py      = 91cd121abc63923477a3132843d7a3cf   (DIFFERS: +505 / -2 lines)
bots/_v528eco/main.py     = 2ba1511168e9c869d53accbba3513ab5   == parent == _v526transit
bots/_v528eco/raid.py     = 3b3a0456e9a22083df4653526bfd68c8   == parent == _v526transit
bots/_v528eco/siege.py    = bd59b18981c87528d77e2ce24f71550f   == parent == _v526transit
```

**THE DIFF IS EXACTLY TWO FILES: `eco.py` and `doctrine.py`.** The `-2` lines in
`eco.py` are the two loop headers (`for ddx, ddy in DIR_DELTAS:` and
`for odx, ody in DIR_DELTAS:`) replaced by flag-gated ordered equivalents.

**The instrumented arms DO patch `main.py`** (`instrument528.py` injects the
`RC POS` / `RC MAP` tape) — but only inside copies under
`scratchpad/s51_v528_build/inst_*`, never in `bots/_v528eco`. The md5 block
above is the assertion, not a claim.

Parent freeze: `scratchpad/s51_v528_build/PARENT_FREEZE.md5`
(`parent_arm/eco.py = bba326d71a4f698f555785de13aa4135`, i.e. the parent's eco
layer untouched).

---

## 0. THE MANDATE, AND WHAT EACH CHANGE ACTUALLY DID

| | mandate | verdict |
|---|---|---|
| **M5** `FS_V528_CONNCOST` | ore candidates scored by rounds-to-first-delivery; marker scenario cannot reproduce; myopia guard on r100 **and** r300 delivery; harvester trajectories non-regression | **MET on the plank's own objective, and the mandated metric had to be corrected first.** Pick-time regret **80.671 → 0.000**. Delivery by r100 **+16.1** (known zero −3.1); cumulative delivery over all games **+149.0** (known zero +37.6). Harvester counts flat within the known zero at r50/r100/r200. ⚠ The r300 delivery cell is **collider-contaminated** — see §4.3. |
| **M4** `FS_V528_WALK` | 0 stalls in 24 wall-heavy 30x30 games vs parent's 13; mutant reproduces | **PARTIAL, AND THE BAR IS MISSED.** 13 → **7** mid-map stalls, the one predicate carrying all of it (`inst_walk` alone = 7). The parent's 13 **replicates v526's independently measured 13 digit-for-digit** on a different parent config. The aggravated mutant reads **25** with a 980-round stall. Seven survivors are a **different, nav-silent** family. |
| **`FS_V528_WIRE`** (optional 3rd) | `_wire_tick` orphan fix, own flag, skip if it grows the diff | **BUILT, SHIPPED, MEASURED INERT.** Three independent measurements say the branch never executes on our fixture (§3). |

---

## 1. M5 — CONNECTION-COST ORDERING (`FS_V528_CONNCOST`)

### 1.1 WHAT THE PARENT DID, EXACTLY

`_pick` sorts every ore on the map by `abs(dx)+abs(dy)` to our Core plus a hash
tie-break, partitions the result round-robin among 2 (small map) or 4 (large)
worker seats, and walks its own slice with a monotonic `ore_cursor`. Two
properties of that, and neither is the quantity the tiebreak ladder pays for:

* the rank is **Manhattan** distance, which on a wall-heavy board is not the
  length of any route a conveyor can actually take;
* **existing belt is worth nothing to it** — an ore two tiles off a live trunk
  ranks below a virgin ore one tile nearer the Core.

`titanium_collected` counts **delivery to the Core**, so the quantity that
matters is **rounds-to-first-delivery**.

### 1.2 WHAT REPLACES IT

A single **0-1-2 cost flood outward from the Core's own delivery ring**
(`_link_goals`) over **the same padded flat grid and the same blocked set that
`_link_path` routes on** — so the number the scorer ranks on is the number the
router will actually have to build. Stepping into a tile already holding one of
our belt pieces costs **0**; an empty tile **1**; a contested tile
**1 + `V528_CONN_CONTEST`**. Ore is impassable to the flood exactly as it is to
`_link_path`. Dial's algorithm, `V528_CONN_NODE_BUDGET` node cap, cached for
`V528_CONN_REFRESH` rounds.

`score = V528_CONN_W_LINK * links + V528_CONN_W_WALK * walk`. The parent's
implicit score is the walk term alone, so the new score is a **superset**: two
candidates the new term cannot separate keep the parent's ordering exactly.

**BELT MEMORY, and without it the scorer answers the wrong question.**
`get_nearby_buildings()` is bounded by the unit's own vision (r²=20), so a
builder out at the ore field cannot see the trunk it laid on the way out — every
tile of it would be charged as if it had to be built again, biasing the score
**against exactly the ore Magnus's marker is about** ("two conveyors from a quick
connection" is a claim about belt that ALREADY EXISTS). Friendly-belt sightings
therefore persist on the unit, and staleness is bounded the only honest way
available: a remembered tile that is **currently in vision** and no longer
friendly belt is dropped. Tiles out of vision are kept — that is a guess, and it
is the same guess `_link_path` already makes when it routes through terrain it
cannot see.

### 1.3 ⛔ THE SITE THAT ACTUALLY DECIDES — AND THE FIRST CUT MISSED IT

Re-ordering `_pick` alone re-orders the **walk target**. The harvester that gets
**built** is whichever adjacent ore comes first in `DIR_DELTAS` — compass order,
i.e. **discovery order, which is the thing the mandate replaces**. The same is
true of `_expand`'s adjacent-ore override.

This was caught **by the mechanism tape, before any outcome was read**: with the
scorer wired only into `_pick`, v528's own connection regret over 20 games was
**not ~0** (per-game means 0.0–86.0), because the body walked to the cheap ore
and then built on whatever ore it happened to stand beside. `_v528_adj_order`
closes it — same flag, same plank; ties keep `DIR_DELTAS` order, and with fewer
than two adjacent ore tiles it returns `None` so the parent's sequence is
preserved byte-for-byte.

⚠ **DISCLOSED: an n=80/arm partial of an earlier headline run was viewed before
this change was made.** Every cell in that partial read `inside` **and smaller
than the known zero** — it carried no signal — and the change was motivated by
the regret tape, not by it. Both batteries were destroyed and re-run from
scratch on the final frozen tree. **Every number in §4 comes only from the final
run.**

### 1.4 ⛔ THE MYOPIA GUARD IS STRUCTURAL, NOT A DIAL

The scorer only ever **re-orders** this seat's existing candidate list. It never
truncates it and never drops a candidate. An unreachable ore scores
`V528_CONN_UNREACH` — large, and **finite** — so once the near ore is taken (its
tile carries a building and the parent's own occupancy skip fires) the far ore is
still chosen. **Quick-connect greed can reorder the queue; it cannot cap it.**
The partition is untouched: same seats, same slices, so no two builders converge
on a deposit that were kept apart before. The empirical arm of the guard is §4.2.

### 1.5 THE ANTI-LOCK, WHICH IS NOT OPTIONAL

The parent's `ore_cursor` rotates on every call, so a permanently unbuildable
tile costs it one round. **A scorer is deterministic and would hand the same tile
back forever — the M4 failure wearing a different hat.** When `_expand` re-picks
*because* the body is stuck (`self.stuck >= 5`), the tile it was stuck on is
banned for `V528_CONN_BAN_RNDS`. If the ban would empty the candidate list, the
**ban** is dropped, not the candidates. Measured cost: **0.250 of a round of
regret on average, over 52 of 2,404 picks.**

### 1.6 ⛔ THE VERIFICATION METRIC THE MANDATE NAMED WAS MEASURING THE WRONG THING

The mandate asks for *"chosen-vs-best-available connection length per harvester
decision, parent nonzero regret vs v528 ~0"*. Built literally — at the harvester
build, connection length only — **that number is nonzero even for a perfect
chooser**, because a 1-link ore twenty tiles away costs twenty rounds of walking
and the scorer is **right** to decline it. It measures a quantity nobody is
minimising, and on it v528 reads 4.179 against the parent's 4.907 — a real but
small improvement that would have looked like a failed bar.

So the tape carries **both**, and the primary is the one the plank actually
optimises: **pick-time regret** — at the moment a target is chosen, the score of
the chosen candidate against the best score available *from where the body
stands*. It is emitted from **both arms by the same code** (gated on
`FS_V528_LOG` alone, never on `LOKI_FS_V528`), so the parent's cursor pick and
v528's argmin are scored on one yardstick. v528's value is ~0 **by construction**
and that is the point — it is the check that the scorer is wired to the decision
that lands. **The finding is the parent's value.**

One further correction, also made before any outcome was read: the best-available
score must **exclude banned tiles**, or the metric charges the chooser regret for
obeying its own anti-lock (measured with the bug: 16.6 mean, 1,339 of 1,352 picks
nonzero — an artefact, not the ordering). `regall` keeps the unfiltered best so
the ban's cost is **reported** rather than hidden.

### 1.7 M5 RESULT — 24 wall-heavy 30x30 games per arm

`scratchpad/s51_v528_build/rc/`, `connread.py`.

| arm | picks | **mean pick-regret** | picks regret>0 | max | mean ignoring the ban | picks w/ banned cand |
|---|---|---|---|---|---|---|
| `inst_off` — **the parent** | 3,698 | **80.671** | 2,771 (74.9%) | 1,186 | 80.671 | 0 |
| `inst_walk` — WALK only | 2,719 | 181.152 | 2,142 (78.8%) | 1,220 | 181.152 | 0 |
| `inst_v528` — **as fired** | 2,404 | **0.000** | **0 (0.0%)** | **0** | 0.250 | 52 |
| `inst_mut` — inverted predicate | 1,193 | 136.779 | 876 (73.4%) | 1,186 | 136.779 | 0 |

**Build-time residual** (connection-only; §1.6): parent **4.907** over 107
harvester decisions, v528 **4.179** over 95, mutant 5.651 over 83.

⚠ `inst_walk` reads *higher* than the parent. That is **not** a WALK effect on
ordering — WALK does not touch `_pick` — it is trajectory divergence: a different
bot visits different boards. It is exactly why the M5 comparison is stated
**parent vs as-fired**, never against an ablation arm.

---

## 2. M4 — THE STALLED WALKER (`FS_V528_WALK`)

**Routed here by v526**, which root-caused it OUT of transit (13 mid-map stalls
over 24 wall-heavy 30x30 games, **0 of 13 involving a ferry/siege body**) and
named the absorbing state precisely: `_expand`'s adjacent-ore override re-targets
any 8-neighbour ore tile carrying no **building** — and **a body is not a
building**. With a unit parked on that ore, `self.tgt` is forced back onto it
every round, defeating the `stuck >= 5` re-pick three lines above, while
`can_build_harvester` stays False for as long as the body stands there.

**The fix is one predicate** (`eco.py`, the override): a tile occupied by a
builder bot of **either team** is not a valid re-target.

### 2.1 M4 RESULT — 24 wall-heavy 30x30 games per arm

valkyrie · glacierkeep · drakkarfjord · ragnarok × 3 seeds × 2 seats,
`stallscan2.py` (self-tested: a nav-silent stall, a nav-busy stall and a clean
walker must come out as three different cells; per-arm roll-up added and
guarded — identical counts across arms would print an explicit "cannot
discriminate" alarm).

| arm | games | stalls ≥8 rounds | **MID-MAP** (d² > 64 from BOTH cores) |
|---|---|---|---|
| `inst_mut2` — **AGGRAVATED MUTANT** | 24 | **148** | **25** |
| `inst_off` — **the parent** | 24 | 71 | **13** |
| `inst_mut` — inverted predicate | 24 | 62 | 8 |
| `inst_walk` — WALK only | 24 | 64 | **7** |
| `inst_v528` — **as fired** | 24 | 57 | **7** |

**13 → 7 mid-map stalls (‑46%), and the one predicate carries all of it —
`inst_walk` alone reaches the same 7 as the full build.** The parent's 13 is a
**digit-for-digit replication of v526's independently measured 13** on the same
map class with a *different* parent configuration, which makes 13 a property of
the defect rather than of one build.

**⛔ THE MANDATE'S BAR WAS 0, AND 0 IS NOT WHAT THIS BUYS.** Seven mid-map stalls
survive. The predicate closes the body-on-ore family; it cannot close the second
family v526 already named (a body standing **on** ore inside an ore field —
`ragnarok id 7`, 183 rounds). The two longest survivors in the v528 arm are
`inst_v528_glacierkeep_s3_B` id 19 (r162–r348, **navs 0**) and
`inst_v528_drakkarfjord_s2_A` id 5 (r154–r337, **navs 0**) — both **nav-silent**,
which is a different mechanism from the one fixed here (that one was nav-busy:
`_bfs_direction` returning CENTRE every round).

### 2.2 THE MUTANT CONTROL — AND THE FIRST ONE DID NOT WORK

The first mutant **inverted** the body predicate (accept only occupied ore). That
does not aggravate the defect, it **disables the override**, and it read 8
mid-map stalls — *below* the parent. **A control that moves the wrong way is not
a control**, so it is reported as a third behaviour and carries no evidential
weight.

The correct aggravated mutant (`inst_mut2`) removes the **building** check as
well, so the override re-targets any adjacent ore including one already carrying
a harvester — strictly more absorbing than the parent. It reads **148 stalls / 25
mid-map, including a single 980-round stall** (`glacierkeep_s1_B` id 8, r19–r999,
navs 980). **The scanner sees the mechanism driven hard in both directions:
25 (aggravated) → 13 (parent) → 7 (fixed).**

⚠ **v526's specific reproducer cell (`valkyrie_s1_A` id 7, (9,10), r37–r59) does
NOT reproduce against this parent**, and that is expected rather than alarming:
v528's parent is the RDV-ONLY configuration while v526's was TEMPO+RDV, so the
game diverges from the opening. **The class count is the instrument; the cell is
not.**

---

## 3. THE OPTIONAL THIRD — `FS_V528_WIRE`, BUILT AND **MEASURED INERT**

v513 open item 5: past `SIPHON_WIRE_RNDS`, `_wire_tick` assigns
`self.link_queue = path` **over a live queue**, dropping every unbuilt tile of the
chain in progress. The harvester that chain was for then emits into nothing — and
`titanium_collected` counts delivery, so that harvester is worth 0 on key 1
forever.

**The fix is a DEFER, not an APPEND**, and the reason is load-bearing:
concatenating two paths puts a seam in the queue, and `_build_next_link` reads
`link_queue[1]` to face the tile it is building — at the seam it would face the
last link of chain A at the first tile of chain B. That link is the one beside
our own Core footprint, where v513 change C measured **perfect separation**
(`titanium_collected` > 0 iff a conveyor of ours stands beside our Core).
Mis-facing it is a worse bug than the one being fixed. So: hold the pending item,
refresh its clock, let the live chain drain — bounded by `V528_WIRE_MAX_DEFER` so
a chain that never drains cannot starve the queue.

**⛔ IT NEVER FIRES ON THIS FIXTURE. THREE INDEPENDENT MEASUREMENTS:**

1. **Byte identity, 16 deterministic cells.** The WIRE-only arm (`eq_wire`) is
   **byte-identical to the parent on 16 of 16**. `byte_identity.py` reports
   `<< PLANK NEVER FIRED (FAIL)`, and the run's overall `RESULT: FAIL` is
   **entirely** this — every other arm passed.
2. **Tape count.** `V528 WIRE defer` appears **0 times in 96 instrumented games**
   (the M4 cell, all four arms) and **0 times in 20 further games** spanning all
   ten maps.
3. **Root cause, diagnosed rather than assumed.** A throwaway arm printing at
   every `_wire_tick` with a non-empty queue: across 10 games `_wire_tick` saw a
   non-empty `wire_pending` **3 times**, and **all 3 already had an acceptor**
   (`acc 1`), so the item popped immediately and the clobber branch was never
   reached. `wire_pending` is only populated when a second harvester is built
   while a chain is live, and on this fixture chains drain before
   `SIPHON_WIRE_RNDS = 12` elapses.

**Shipped as measured (`True`), because flipping the flag after the battery would
make the fired tree different from the measured tree** — and the 16/16
byte-identity is the proof that `True` and `False` are the same object here.
**The verdict is the builder's.** This is a real fix for a real defect that our
local fixture does not produce; it may fire against opponents whose pressure
lengthens our chains, and it has never been observed to.

---

## 4. THE HEADLINE — n=480/arm, 1,440 games, 0 tracebacks

3 arms, 8-map panel (**the same panel v526/v527 used** — deviating would make the
cross-build comparison invalid), 30 seeds × 2 seats, arms **interleaved per cell**
(v518 finding 2: pooling non-time-adjacent local fixtures produced a 4.6 pp false
positive on byte-identical play). Opponent `bots/_v488beltbreak2`.

* `v528` — `bots/_v528eco` as fired
* `parent` — `_v526transit` RDV-only
* `flagoff` — `bots/_v528eco` with `LOKI_FS_V528 = False`; **proved byte-identical
  to `parent` on 10/10 deterministic cells**, so it is a **KNOWN-ZERO arm** and
  every `flagoff`-vs-`parent` number below is pure fixture noise at this n.

⛔ **LOCAL FIXTURE, NO DEFF.** The s39 audit measured pair-weighted local
DEFF = 0.98 on a balanced-by-construction fixture, so the platform constants
(1.529 rated / 1.833 unrated) do **not** apply and are not used. Naive two-sample
half-widths.

### 4.1 THE KILL_TARGET PANEL

```
arm             n   wins%    <=r150    <=r180    <=r200    <=r250    <=r300  medkill  ourcore   tb
parent        480   69.8% 107(0.223) 143(0.298) 167(0.348) 212(0.442) 231(0.481)      193      127    0
flagoff       480   70.8% 112(0.233) 147(0.306) 171(0.356) 219(0.456) 244(0.508)      192      118    0
v528          480   74.2% 103(0.215) 151(0.315) 167(0.348) 227(0.473) 255(0.531)      202      108    0
```

| comparison | Δ | half-width | verdict | **KNOWN ZERO on the same metric** |
|---|---|---|---|---|
| v528 vs parent · **wins** | **+4.38 pp** | 5.68 | inside | +1.04 pp |
| v528 vs parent · **k<=200** | **+0.00 pp** | 6.03 | inside | +0.83 pp — **v528's gap is SMALLER than the zero** |
| v528 vs parent · **k<=300** | **+5.00 pp** | 6.33 | inside | +2.71 pp |
| v528 vs parent · **ourcore** | **−3.96 pp** | 5.44 | inside | −1.88 pp |

* **`DEFENCE_ADMISSION_BAR` (ITT, share of ALL games ending in a core kill by
  r300) RISES: 0.481 → 0.531.** Non-regression is satisfied.
* **`k<=200`, the tracked KILL_TARGET metric, is exactly flat** and its gap is
  smaller than its own known zero — i.e. this build buys nothing on the primary
  kill-speed currency and is not measurably costing it either.
* Median kill (kill-conditioned, **diagnostic only — carries the collider**)
  193 → 201.5. Well inside the r300 gross backstop.
* **0 tracebacks across all 1,440 games** (results.tsv column sum = 0).

### 4.2 THE DELIVERY PANEL

⛔ **CROSS-INSTRUMENT GATE PASSED: `deliv.py`'s end-of-game delivery equals the
engine scoreboard's `ours_mined` on 1,440 of 1,440 joined rows, 0 replays
missing.** Two instruments, one of which the other never sees, agree exactly.

```
arm             n     n100  d100med d100mean     n300  d300med d300mean dendmed  t1rate  t1med    h50   h100   h200   h300
parent        480      449      360    373.3      181      660    743.6     540   0.996     22   2.42   2.47   1.91   1.43
flagoff       480      444      350    370.2      173      690    843.1     550   0.998     22   2.42   2.46   2.01   1.34
v528          480      446      370    389.4      168      740    917.8     605   1.000     22   2.39   2.49   2.01   1.30
```

| cell | v528 | parent | Δ | **KNOWN ZERO** |
|---|---|---|---|---|
| **delivered by r100** (mean) | 389.4 | 373.3 | **+16.1** | −3.1 |
| **delivered by r300** (mean) | 917.8 | 743.6 | +174.2 | +99.5 — see §4.3 |
| **cumulative delivery, ALL games** (mean) | **1,027.0** | 878.0 | **+149.0** | +37.6 |
| **first-funded-turret round** (median) | 22 | 22 | +0.00 | +0.00 — flat |
| harvesters alive r50 | 2.39 | 2.42 | −0.04 | −0.01 |
| harvesters alive r100 | 2.49 | 2.47 | +0.01 | −0.02 |
| harvesters alive r200 | 2.01 | 1.91 | +0.10 | +0.10 |
| harvesters alive r300 | 1.30 | 1.43 | −0.13 | −0.09 |

* **The myopia guard passes on its clean columns.** Early delivery rises
  (+16.1 vs a ±3.1 zero) **and** cumulative delivery over all games rises
  (+149.0 vs a +37.6 zero, 4x). Quick-connect greed did not cap throughput.
* **The eco gate did not move the turret clock.** First-funded-turret round is a
  median of 22 in all three arms, and the turret-built rate is ≥0.996
  everywhere. Whatever M5 buys, it is not arriving through the sentinel gate.
* **Harvester trajectories are non-regressive**, every cell at or within the
  known zero except `h300` (−0.13 vs −0.09) — and r300 harvester counts are the
  4.2% tiebreak key that `R1000_IS_DEFEAT` retired.

### 4.3 ⛔ THE r300 DELIVERY CELL IS COLLIDER-CONTAMINATED — DO NOT QUOTE IT ALONE

`d300` exists only for games that **reached** r300, and the arms do not reach it
equally: **parent 181, flagoff 173, v528 168 games**, because v528 resolves more
games by r300 (312 core kills by r300 vs the parent's 299). **Conditioning on
"survived to r300" selects the games we failed to close**, and it selects a
different slice in each arm. `d100`'s denominators are near-identical
(449 / 444 / 446) and `dend` conditions on nothing at all, so those two are the
honest reads. This is why `n100` and `n300` are printed beside every cell.

### 4.4 PER MAP — `wins/n  [k<=300]  {k<=200}`

```
map            parent                  flagoff                 v528
antler         38/60  [32] {17}       41/60  [32] {22}       41/60  [28] {16}
atoll          32/60  [15] {10}       26/60  [14] { 5}       31/60  [17] { 7}
drakkarfjord   57/60  [41] {37}       56/60  [46] {39}       55/60  [42] {40}
fjordgate      38/60  [29] {14}       37/60  [30] {15}       40/60  [26] {15}
glacierkeep    50/60  [30] {23}       52/60  [38] {28}       52/60  [44] {28}
midgard        32/60  [14] { 7}       31/60  [18] { 5}       37/60  [21] { 9}
nordkap        37/60  [23] {17}       38/60  [21] {16}       44/60  [31] {17}
yulerune       51/60  [47] {42}       59/60  [45] {41}       56/60  [46] {35}
```

The wins gain concentrates on **nordkap (+7)**, **midgard (+5)** and
**glacierkeep (+2, with k<=300 30→44)** — the wall-heavier boards, which is where
a path-length-aware scorer should pay and is consistent with the mechanism. It is
**negative on yulerune's `k<=200` (42 → 35)** and on `antler`'s `k<=300`
(32 → 28). At n=60 per map cell the known-zero arm swings as much
(atoll 32 → 26), so **no per-map cell is a reading**; the column is here for
pattern, not for verdict.

---

## 5. VERIFICATION

### (a) FLAG-OFF BYTE-IDENTITY **10/10** · STANDDOWN **10/10** · NEGATIVE CONTROL **15/16**

`byte_identity.py`. Method: `NOISE_ON = False` on **both** sides (ours and
`bots/_v488beltbreak2`), `--tle 0`, replay bytes compared — `--seed` alone does
not pin a game (v518 finding 1/2).

```
ARM 1  LOKI_FS_V528=False vs PARENT              IDENTICAL 10/10   (the known zero)
ARM 3  master ON, all sub-flags OFF vs PARENT    IDENTICAL 10/10   (the standdown)
ARM 2  v528 as fired vs PARENT                   DIFFERS   15/16   (negative control)
ARM 4  eq_conn                                   DIFFERS   15/16
       eq_walk                                   DIFFERS    6/16
       eq_wire                                   DIFFERS    0/16   << PLANK NEVER FIRED
RESULT: FAIL   (entirely eq_wire; see §3)
```

⛔ **WHY v528's STANDDOWN IS NOT A MAP LIST.** Every recent build in this line
gated on the ferry-siege, so `midgard` (CRIPPLE) and `archipelago` (GATED) were
maps where the plank provably could not run and IDENTICAL was the assertion.
**v528's planks are in the ECO layer, which runs on every map** — a map-list
standdown here would be an assertion that cannot fail. The standdown that **can**
fail is the sub-flag one: master ON with all three planks OFF must reproduce the
parent exactly. It does, 10/10. Without it the per-plank ablations would not mean
what they say.

`eq_walk` differing on only 6/16 and `eq_wire` on 0/16 is **reported as a count,
not a rate**, on purpose: WALK fires only where a body parks on ore and WIRE only
where a second harvester queues behind a live chain. Demanding 16/16 would be
demanding the wrong thing; **0/16 is the thing that must not happen**, and it
happened for WIRE.

**0 tracebacks** across the 176 byte-identity games.

### (b) NO NEW DERIVED DEFAULTS — AST SCAN **0**, WITH A POSITIVE CONTROL

`flagoff_ast.py`, extended to the v528 flag set and run over **all five files**:

```
GUARD: pos=True neg=False if=True
v528 derived defaults: 0    (and v527/v526/v525/v524/v522/v521/v520/v519/v518: 0 each)
REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard):
    2 [(3011, 'FERRY_HOME_ON', 'LOKI_FS_CREW'), (3011, 'FERRY_HOME_ON', 'FS_CREW_ON')]
TOTAL derived-default hits across all scanned files: 0
RESULT: PASS
```

Three synthetic guards driven **both ways** (a module-level `X = FLAG and 3` must
be reported, `X = 3` must not, a module-level `if FLAG:` must be), plus the
**real-case control** — the scanner finds the one known live instance
(`FERRY_HOME_ON`), so a clean v528 result is a measurement and not blindness.

Every v528 flag is read **inside the branch it guards** — five read sites, all of
the form `if LOKI_FS_V528 and FS_V528_x:`. `mkarm.sh` patches overrides **in
place at the definition site**, never appended, so the v515 finding-3 hazard
cannot be reintroduced by the arm builder either.

### (c) CPU — AND THE LOCAL SURFACE CANNOT MEASURE IT

⛔ **`BotOutput.execTimeUs` is 0 in every event of every locally-produced
replay** (measured: 8 replays, `tlescan.py` reports `max_us` distinct=1 across
all arms — a constant column, which validates nothing), and
`get_cpu_time_elapsed()` is a local stub (v513 open item 3). **"0 TLEs locally"
is not evidence and is not reported as any.**

What *can* be measured is the algorithm, in isolation, on real terrain read off
replays (`cpubench.py`), against the incumbent hot object on the same grids:

```
  midgard      30x30 ores=16   conn_field=  482.2 us   _link_path=  86.7 us   ratio=5.56
  valkyrie     30x30 ores=16   conn_field=  480.5 us   _link_path=  67.9 us   ratio=7.08
  ragnarok     30x30 ores=26   conn_field=  457.3 us   _link_path=  78.6 us   ratio=5.82
  nordkap      20x26 ores=22   conn_field=  246.8 us   _link_path=  38.3 us   ratio=6.43
  atoll        18x18 ores=8    conn_field=  171.1 us   _link_path=  29.0 us   ratio=5.90
  WORST conn_field = 482.2 us   ·   budget = 10000 us/unit/turn
  GUARD non-constant across maps: distinct=5 of 5
```

**Worst single call is 4.8% of the per-unit budget, and it is cached for
`V528_CONN_REFRESH = 12` rounds** while `_link_path` is not — amortised ~40 µs a
round. The guard matters: a first cut of this bench ran on `known_map_for`'s
ore-free fallback grid and returned 525–527 µs on every map, a 1.6 µs spread that
would have "passed" a non-constant check on noise. **A platform `match test` is
still required before any ship** — this bench prices one function, not a turn.

### (d) EVERY READER SELF-TESTED, EVERY GUARD DRIVEN TO THE OTHER VERDICT

| instrument | guards, each shown producing BOTH verdicts |
|---|---|
| `deliv.py` (delivery panel) | monotone delivery (**corrupted copy CAUGHT**); `d100<=d300<=dend`; **cross-instrument** `dend == scoreboard mined` **8/8**, with a wrong-arm control that differs 8/8 (0 would mean the check cannot fail); **non-constant** `d300`/`dend`/`turret1`; **seat-swap swaps** `d*` and `od*` |
| `headline.py` | all-win / all-loss / mixed tapes fold to different counters; delivery folds low/high to different means; **a game that never reached r300 is EXCLUDED from `n300` (0), not counted as zero delivery** |
| `stallscan2.py` | nav-silent stall, nav-busy stall and clean walker come out as three different cells; per-arm roll-up alarms if all arms produce identical counts |
| `connread.py` | empty tape reported as **blind, not zero**; non-constant pick-regret (distinct=18 on the probe); all-`cands 0` reported as a fixture artefact |
| `flagoff_ast.py` | positive / negative / `if`-form synthetic controls + the real-case `FERRY_HOME_ON` control |
| `cpubench.py` | priced against an object already shipping; non-constant-across-maps guard, which caught the ore-free-grid artefact |
| `tlescan.py` | **reported itself blind** — its own non-constant guard failed (`distinct=1`), which is why §5(c) says the local surface cannot measure CPU |

**⛔ THREE INSTRUMENT DEFECTS WERE CAUGHT BY THESE GUARDS, NOT BY INSPECTION**,
and all three would have produced a confident wrong number:
1. `deliv.py` read the Turn's own fields as Update fields — **every column came
   out constant**; caught by the non-constant guard.
2. `deliv.py` then read `PlaceEntity`'s fields as an `Entity` — **`turret1` was
   −1 on all 8 replays**; caught by the same guard.
3. The in-tree tape printed with bare `print()`. **The engine captures a bot's
   `print()` into the REPLAY, not the harness's stdout** — the tape read 0 lines
   across a 283-turn game while looking healthy. `eco.py` now imports `sys`
   **in the shipped tree** (inert with `FS_V528_LOG = False`) so the v526
   NameError-in-a-bare-except trap cannot recur, and `instrument528.py`
   **asserts** the import rather than injecting it.

---

## 6. FAILURE REEL

Selected by a stated rule: the **earliest our-core-death on EACH map** for the
`v528` arm across the whole headline battery (one per map, so the reel is not
five copies of one board); ties by lowest seed, then seat A.

```
map            turn   seed seat   replay
fjordgate      96     6    A      scratchpad/s51_v528_build/head/rep/v528_fjordgate_s6_A.replay26
antler         149    17   B      scratchpad/s51_v528_build/head/rep/v528_antler_s17_B.replay26
nordkap        154    29   B      scratchpad/s51_v528_build/head/rep/v528_nordkap_s29_B.replay26
midgard        156    2    A      scratchpad/s51_v528_build/head/rep/v528_midgard_s2_A.replay26
atoll          180    15   A      scratchpad/s51_v528_build/head/rep/v528_atoll_s15_A.replay26

EXTENSION (labelled, NOT part of the reel): the 2 latest-kill WINS -- the other
tail, and the one the kill-round bar actually binds on:
nordkap        960    28   A      scratchpad/s51_v528_build/head/rep/v528_nordkap_s28_A.replay26
antler         860    8    B      scratchpad/s51_v528_build/head/rep/v528_antler_s8_B.replay26

our-core deaths = 108 of n=480 (22.5%)   ·   r1000 games = 36
```

---

## 7. RUN DISCIPLINE

* **PAR.** The sibling v527 battery reached `HEADLINE DONE` at `04:19:20Z` and
  `scratchpad/COREFILL_WORKLIST_DRAINED` was present with `corefill_forever.sh`
  idle, so the box was **between batteries**: headline at **PAR=3**, mechanism
  cell at PAR=2, byte-identity sequential, on 10 cores. Load stayed ≤6.5.
  **`scratchpad/overnight*` and corefill were never touched.**
* **PIDs recorded** in `scratchpad/s51_v528_build/PIDS` for every launch,
  including the two restarts.
* **TWO FULL RESTARTS, both disclosed.** The first because a tape-routing fix
  (`print` → `sys.stderr`) touched the tree mid-battery; the second because §1.3's
  `_v528_adj_order` did. In both cases **every prior battery output was deleted**
  (`head/`, `byte_check/`, `rc/`) and re-run from scratch against the re-frozen
  tree (`TREE_FROZEN.md5`). No number in this report mixes trees.

---

## 8. ARTEFACTS

| what | where |
|---|---|
| the tree (uncommitted) | `bots/_v528eco` — **diff is `eco.py` + `doctrine.py` only** |
| tree / parent freezes | `scratchpad/s51_v528_build/TREE_FROZEN.md5`, `PARENT_FREEZE.md5` |
| headline battery (1,440 games + replays) | `scratchpad/s51_v528_build/head/`, `drive_headline.sh`, `run_battery.py` |
| headline + delivery reader | `headline.py` (`--selftest`), `deliv.py` (`--selftest`) |
| byte identity / standdown / per-plank | `byte_identity.py`, `byte_identity.log`, `byte_check/`, arms `eq_*` |
| AST scan | `flagoff_ast.py` |
| M4 + M5 mechanism cell (96 games) | `rc/`, `rc_run.sh`, arms `inst_*` |
| aggravated mutant cell (24 games) | `rc2/`, arm `inst_mut2` |
| M4 stall scanner | `stallscan2.py` (self-tested, per-arm roll-up) |
| M5 regret reader | `connread.py` |
| tape injector (patches COPIES only) | `instrument528.py` |
| arm builder (in-place, never appended) | `mkarm.sh` |
| CPU bench / TLE scan | `cpubench.py`, `tlescan.py` |
| failure reel | `reel.py` |
| one-shot collector | `collect.sh` |

---

## 9. OPEN ITEMS FOR THE BUILDER

1. **`FS_V528_WIRE` ships `True` and is measured inert.** Decide: keep (a real
   fix that may fire on the ladder) or set `False` (a branch we have never seen
   execute). §3 has the three measurements.
2. **M4 missed its 0-stall bar at 7.** The survivors are **nav-silent**, a
   different family from the one fixed. A root-cause pass on those seven is the
   natural successor and the tapes are banked in `rc/`.
3. **`k<=200` is exactly flat.** This build buys delivery and wins, not kill
   speed. If the currency is kill speed, M5 is not the plank that moves it.
4. **CPU is unmeasured end-to-end.** `conn_field` prices at 4.8% of budget worst
   case in isolation, but the local surface cannot see a whole turn. A platform
   `match test` before any ship.
5. **The known zero is large at this n** (`d300_mean` +99.5, `k<=300` +2.71 pp on
   byte-identical play). Every headline claim here is stated against it; the only
   gaps that clear it comfortably are cumulative delivery (4x) and, weakly, wins
   (4.2x — still inside the half-width).

---
## BUILDER VERDICT LINES (s51)
* **M5 ADOPTED — met exactly**: pick-time connection regret 80.67→0.000 (74.9% of decisions
  carried regret; now zero of 2,404), with the myopia guard CLEAN: cumulative delivery +149.0
  vs +37.6 known-zero. The marker's defect class is dead.
* M4 PARTIAL ADOPTED: stalls 13→7 (−46%), bar (0) missed — residual routed to the queue with
  the surviving predicate named. WIRE: inert, stays flagged (harmless, root-caused).
* Headline: wins +4.38 vs +1.04 known-zero (inside interval — suggestive not banked),
  DEFENCE bar RISES (k≤300 48.1→53.1), delivery the clean column. Adopted into the merge.
* Instrument notes: pick-time-vs-build-time regret correction accepted (§1.6 governs);
  the collider-contaminated r300 delivery cell quoted never-alone; **execTimeUs=0 in ALL local
  replays — "0 TLEs" is not evidence anywhere local; platform match test remains mandatory
  pre-ship** (now thrice-established).
