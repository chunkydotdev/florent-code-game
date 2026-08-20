# BUILD REPORT — `bots/_v529merge`, s51, 2026-08-20

**The mechanical UNION of `bots/_v527collar` and `bots/_v528eco`, both parented on
`bots/_v526transit` configured RDV-ONLY.** No new mechanism, no new flag, no new
constant — **this build's only question is COMPOSITION.**

Tree **uncommitted**, per instruction. `PAR=4` throughout; PIDs in
`scratchpad/s51_v529_build/PIDS` (BYTEID 84913 · SPOT 92330 · HEADLINE 96817 ·
POST 55861). `scratchpad/overnight*` and `corefill_forever.sh` (PID 68004, still
alive) were **not touched**. Wall clock from `date -u` in the same shell call:
freeze `05:17:29Z`, headline `05:24:38Z → 05:43:08Z`, post-batteries
`05:47:14Z`, supplement `05:48:43Z`.

**2,934 games. 0 tracebacks, 0 timeouts, 0 no-winners** (2,400 headline · 288
dose · 106 byte-identity · 60 spot · 48 supplement · 32 standdown).

---

## ⛔ TOP LINE — THREE SENTENCES

1. **The merge is provably mechanical.** The two doctrine deltas do not overlap
   *at all*: each child's doctrine minus its appended constant block is
   **AST-identical** to the shared base, and the two blocks assign 19 and 14
   names with **zero intersection and zero shadowing**. There was nothing to
   arbitrate. Byte-level: `eco.py` = v528's, `main.py`+`siege.py` = v527's,
   `raid.py` = the parent's, all md5-confirmed at freeze and again at write time.
2. **Both mechanisms survive composition, measured not assumed.** In the union
   the v527 collar fires **8 BUNKER swaps / 48 games** (v527 alone: 9) and
   **2 PSURV dispatches** (v527 alone: 2), while v528's pick-time connection
   regret stays at **0.000 over 4,449 picks**. Both ablation controls were driven
   to the other verdict *inside the union* (collar off → 0 fires; CONNCOST off →
   regret 27.185, 2,742 of 4,054 nonzero).
3. **On CURRENCY the union is ADDITIVE and reads NULL; on the ECO/DELIVERY
   columns the point estimates are consistently SUBADDITIVE — but nothing
   separates at n=480, and the harvester-column "signal" the known-zero yardstick
   appeared to show DISSOLVES under a proper two-sample interval.** Details and
   the correction in §5.3, which is the most important paragraph in this report.

---

## 1. THE MERGE — WHY THERE WAS NO CONFLICT

### 1.1 The common base had to be constructed first

Both children were built from `bots/_v526transit` **after** flipping
`FS_V526_TEMPO = False` at its definition site (v526's own report measured that
plank carrying the whole v526 regression alone). So a naive `diff parent child`
reports a *spurious* overlap at line 4840 — both children rewrote that line.

The base used here is therefore `mkarm.sh bots/_v526transit FS_V526_TEMPO=False`
(`scratchpad/s51_v529_build/base_arm`, doctrine md5 `c9a11dee…`), which is the
object both siblings actually parented on.

### 1.2 Against that base, the hunks are disjoint

```
diff base/doctrine.py  v527/doctrine.py  ->  4692,4698c4692,4724 · 4840c4866,4876 · 4921a4958,5132
diff base/doctrine.py  v528/doctrine.py  ->                        4840c4840,4846 · 4921a4928,5053
```

`mergecheck.py` (self-tested; every guard driven to FAIL on a mutated input)
resolves this on the **AST**, not the text — because a text hunk that is
comment-only is not an overlap, and a text-level merge tool would have flagged
one here:

```
C1a  PASS  v527 doctrine minus its block is AST-identical to the RDV-only base
           (its 2 text hunks are COMMENT-ONLY)
C1b  PASS  v528 doctrine minus its block is AST-identical to the RDV-only base
C2a  PASS  both appended blocks are module-level Assign statements only (19 + 14)
C2b  PASS  the two blocks' target names are DISJOINT (overlap: [])
C2c  PASS  neither block shadows a base name (v527 [] / v528 [])
C3   PASS  UNION AST == base ++ v527block ++ v528block, statement-for-statement (551 vs 551)
C4a  PASS  UNION-vs-v527 namespace delta == exactly v528's 14 names (sym-diff [])
C4b  PASS  UNION-vs-v528 namespace delta == exactly v527's 19 names (sym-diff [])
C5   PASS  eco.py == v528 · main.py == v527 · siege.py == v527 · raid.py == PARENT
RESULT: PASS
```

⭐ **NEITHER CHILD EDITED A SINGLE EXECUTABLE STATEMENT OF THE SHARED BASE.**
v527's two non-append hunks are a v524 provenance correction and the
`FS_V526_TEMPO` rationale; v528's is the same rationale in different words. The
merged file takes v527's copy of the shared region (it carries the v524
correction) plus both constant blocks, and the one thing dropped is v528's
variant of a **comment** on a line whose value is identical in all three trees —
recorded at the merge header and preserved verbatim in v528's own report.

**Selftest of the verifier** (a check that has never produced the other verdict
has not been seen to check):

```
C1 broken by planting a real statement in the shared region  -> C1a FAILS
C2 broken by planting a colliding name in both blocks        -> C2b FAILS
C3 broken by dropping one statement from the union           -> C3  FAILS
C4 broken by flipping a v528 value inside the union only     -> C4b FAILS
```

### 1.3 Digest chain (frozen at `05:17:29Z`, re-verified at report time — NO DRIFT)

```
PARENT  _v526transit  doctrine c2c4006e  eco bba326d7  main 2ba15111  raid 3b3a0456  siege bd59b189
BASE    base_arm      doctrine c9a11dee  (= parent + FS_V526_TEMPO=False, in place)
v527    _v527collar   doctrine 9c1d97cb  eco bba326d7  main 93a85f57  raid 3b3a0456  siege 0ee5bb2d
v528    _v528eco      doctrine 2bb7c4af  eco 91cd121a  main 2ba15111  raid 3b3a0456  siege bd59b189
UNION   _v529merge    doctrine 95e46641  eco 91cd121a  main 93a85f57  raid 3b3a0456  siege 0ee5bb2d
                                ^^merged   ^^v528's     ^^v527's      ^^parent's     ^^v527's
```

**Fired configuration** = both masters `True`, every sub-flag exactly as its
sibling shipped it (`FS_V527_BUNKER/DEFENDED/PSURV/PSURV_DISPATCH/SEALPATH` True,
`PSURV_LASTSEAT/TFIRST` False as v527 dominated them; `FS_V528_CONNCOST/WALK/WIRE`
True, `WIRE` inert-by-measurement per v528 §3). No value was changed by this build.

---

## 2. VERIFY-FIRST (2) — FLAG-OFF BYTE-IDENTITY **16/16**, PLUS TWO COMPOSITION ARMS

`byte_identity.py`; `NOISE_ON = False` on **both** sides (`eq_opp` verified to
differ from `bots/_v488beltbreak2` by that ONE line and nothing else, `cmp`'d
file-by-file), `--tle 0`, seed 529820, replay **bytes** compared.

```
A1   eq_off   (union, BOTH masters False)  vs parent    IDENTICAL 16/16   PASS   <- the known zero
A2   eq_v529  (union as fired)             vs parent    DIFFERS    9/10   PASS   <- negative control
A3   eq_u527  (union, V528 off)            vs eq_527    IDENTICAL 16/16   PASS   <- composition, v527 side
A3n  eq_u527                               vs parent    DIFFERS    0/10   see below
A4   eq_u528  (union, V527 off)            vs eq_528    IDENTICAL 16/16   PASS   <- composition, v528 side
A4n  eq_u528                               vs parent    DIFFERS    9/10   PASS   <- negative control
TRACEBACKS 0
```

⭐ **A3/A4 ARE THE ARMS A MERGE BUILD NEEDS AND A FLAG-OFF ARM CANNOT GIVE.**
A flag-off arm only shows the union stands *down*. A3/A4 show that the union with
one side live still reproduces **that side, byte for byte** — so any v529-vs-
sibling gap in the battery is *interaction between two live planks* and cannot be
a merge defect.

⛔ **A3n FAILED, AND IT IS A KNOWN FIXTURE PROPERTY, NOT A MERGE DEFECT — SO IT
WAS RESCUED RATHER THAN EXPLAINED AWAY.** With `NOISE_ON = False` v527's economy
gate refuses every bunker ask; v527's own report §5(a) measured exactly this
(its as-fired arm differed from the parent on **1 of 14** cells, antler seat A
only). My 10 cells contained no antler. **A3 without a firing cell is a
pass-by-default**, so `byteid_supp.py` ran the cell family known to separate:

```
S1  cells where the v527 side separates from the parent: 4/16
    [antler A s527919 · antler A s529820 · frostgate A s527919 · frostgate A s529820]
S2  on those 4 cells, eq_u527 == eq_527 on 4, differs on 0        RESULT: PASS
```

⇒ **On every deterministic cell where the v527 collar actually fires, the union
makes byte-identical choices to `_v527collar`.** That is the claim A3 was for,
and it now has teeth.

### 2.1 STANDDOWN — BOTH FORMS

```
(a) MAP standdown, 12 games, union with both tapes live
    archipelago (GATED)   V527 clauses reached = 0   BUNKER = 0   PSURV = 0   tb 0
    midgard     (CRIPPLE) V527 clauses reached = 0   BUNKER = 0   PSURV = 0   tb 0
(b) SUB-FLAG standdown: both masters TRUE, EVERY sub-flag of BOTH lineages False
    vs parent -> IDENTICAL 10/10
```

(a) **can** fail: the same tape reads 3,554 BUNKER lines in 12 games on
atoll/drakkarfjord/glacierkeep. (b) is the one that matters for a union — it
proves **neither master does anything on its own**, so every per-plank ablation
below means what it says.

---

## 3. VERIFY-FIRST (4) — AST DERIVED-DEFAULT SCAN: **0**, WITH ITS POSITIVE CONTROL

```
GUARD: pos=True neg=False if=True
doctrine.py 0 · siege.py 0 · main.py 0 · eco.py 0     (v527, v528 and every
                                                       inherited set v518-v526)
REAL-CASE CONTROL (FERRY_HOME_ON reads FS_CREW_ON, the known v515 hazard): 2 found
TOTAL derived-default hits: 0        RESULT: PASS
```

The v515 finding-3 hazard (a module-level default that freezes a flag value at
import) cannot bite this tree: both constant blocks are literals only, appended
after every read site, and `mkarm.sh` edits **in place at the definition site**
rather than appending.

---

## 4. VERIFY-FIRST (3) — DOES EACH LINEAGE'S MECHANISM STILL FIRE IN THE UNION?

v527's own dose design: **8 maps × 3 seeds × 2 seats = 48 games/arm**,
`NOISE_ON=True`, `--tle 10`, stderr kept. 288 games, **0 tracebacks**.
⚠ `NOISE_ON=True` re-rolls the spawn salt per process, so these are
**magnitudes, not constants** (v527 read BUNKER FIRE 5/3/2 on three runs of
identical cells).

```
arm          games tb | FIRE RESEAL  HOLD | PSARM PSDIS SLFCUT SWITCH | sealnt/g runmax run>=50 | picks mean_reg reg>0
dose_v529      48   0 |    8      0  7604 |    16     2    245      0 |    47.1    217       9 |  4449    0.000     0
dose_527       48   0 |    9      0  4590 |    19     2    224      0 |    32.7    241       9 |     -        -     -
dose_528       48   0 |    0      0     0 |     0     0      0      0 |    27.9    293       7 |  5141    0.000     0
dose_parent    48   0 |    0      0     0 |     0     0      0      0 |    52.5    917      10 |     -        -     -
dose_ctl527    48   0 |    0      0     0 |     0     0      0      0 |    63.8    776      11 |  8399    0.000     0   <- collar OFF in the union
dose_ctl528    48   0 |    7      0  7493 |    16     2    166      0 |    43.2    606       8 |  4054   27.185  2742   <- CONNCOST OFF in the union
```

**v527 side — FIRES IN THE UNION.** 8 BUNKER swaps vs 9 for v527 alone; 16 PSURV
arms vs 19; **2 PSURV dispatches, exactly as many as v527 alone**; 245 SELFCUT vs
224. `SWITCH` is 0 in every arm — reproducing v527's "0 of 120–175 opportunities",
i.e. the plank that carried zero dose there still carries zero here.
**Control `dose_ctl527` drives all four counters to 0 inside the union.**

**v528 side — SURVIVES INTACT.** Pick-time connection regret **0.000 on 0 of
4,449 picks**, the number v528 banked (0 of 5,141 in its own build).
**Control `dose_ctl528` drives it to 27.185 mean / 2,742 of 4,054 nonzero / max
147 inside the union** — so the zero is the plank, not the fixture.
Instrument guards: pick-regret is **non-constant across the pool (distinct=107)**
and no arm has an empty tape.

**RDV compliance.** All five arms carry `FS_V526_RDV = True` and
`FS_V526_TEMPO = False` at their definition sites (verified by grep on every arm,
§1.3). RDV lives in `siege.py`, which the union takes wholesale from v527 —
md5-identical, so it is the same object v526 measured and v527 shipped; the
sub-flag standdown (§2.1b) confirms nothing in the union perturbs it.

### 4.1 THE v527 MARKER STATISTIC IN THE UNION — READ AGAINST THE RIGHT CONTROL

`[sealed & no-turret]` rounds per game (`sealnt_read.fold_text`, self-tested
against three synthetic tapes including one that catches a reader blind to the
turret column):

| arm | rounds/game | **worst run** |
|---|---|---|
| parent (RDV-only) | 52.5 | **917** |
| `ctl527` — union with the collar OFF | 63.8 | 776 |
| **union `v529`** | **47.1** | **217** |
| v527 alone | 32.7 | 241 |
| v528 alone | 27.9 | 293 |

⛔ **THE UNION'S 47.1 IS HIGHER THAN v527's 32.7, AND THAT IS THE WRONG
COMPARISON.** The within-union control is `ctl527`: turning the collar off inside
the union reads **63.8 → 47.1 (−26%) and worst run 776 → 217**. The absolute
level differs from v527-alone because v528's eco changes the phase mix, not
because the collar stopped working. **On the marker's own worst-case statistic
the union is the best of all five arms (217).** ⚠ Worst-run is a max over 48
games and is high-variance; the parent's 917 and v527-alone's 241 are single
draws too.

---

## 5. THE COMPOSITION BATTERY — n=480/arm, 2,400 games, 0 tracebacks

FIVE arms interleaved per cell, 8-map panel (`atoll drakkarfjord glacierkeep
nordkap yulerune antler fjordgate midgard`), 15 blocks × 2 seeds × 2 seats,
`PAR=4`, opponent `bots/_v488beltbreak2`. `flagoff` is the union with **both**
masters False, proved byte-identical to `parent` on 16/16 cells — so every
`flagoff − parent` number is pure fixture spread and is the yardstick.

### 5.1 THE KILL_TARGET PANEL, PER ARM

```
arm             n   wins%    <=r150     <=r180     <=r200     <=r250     <=r300  medkill ourcore  tb
parent        480   72.7%  116(.242)  157(.327)  176(.367)  218(.454)  252(.525)     189     112   0
flagoff       480   71.0%  117(.244)  140(.292)  173(.360)  226(.471)  247(.515)     193     121   0
v527          480   74.0%  122(.254)  165(.344)  188(.392)  230(.479)  261(.544)     181     104   0
v528          480   72.3%  125(.260)  152(.317)  176(.367)  215(.448)  235(.490)     192     119   0
v529 UNION    480   73.8%  128(.267)  160(.333)  187(.390)  229(.477)  257(.535)     182     115   0
```

`KILL_TARGET` is `median_r180_share_by_r200_floor_r300`. The union's median kill
is **182** (parent 189, v527 181) and its `k<=200` share is **0.390** (parent
0.367) — both the best or joint-best of the five, both **inside** their intervals.

`DEFENCE_ADMISSION_BAR` (ITT, share of ALL games ending in a core kill by r300):
parent **0.525** → union **0.535**. **Does not fall. Not breached.**
⛔ Per CLAUDE.md this is a **fail-to-exclude** claim and must be restated as an
exclusion before any correction: with δ = +1.04 pp and naive hw 6.31, the band is
roughly [−5.3, +7.4] pp, so **we cannot exclude a 5-point regression either.**
The bar is *not breached* and is *not cleared*; the leg is underpowered for it,
exactly as v527's was.

### 5.2 THE ADDITIVITY TABLE — THE BUILD'S ONLY QUESTION

`D527`/`D528`/`D529` are deltas vs `parent`; `SUM = D527+D528` is what pure
additivity predicts; `INT = D529 − SUM`; `GAP = D529 − max(D527,D528)`;
**`KZ` is the known-zero arm's own excursion on the same column.**

**RATE COLUMNS (pp vs parent)**

| column | D527 | D528 | SUM | **D529** | INT | GAP | KZ | verdict |
|---|---|---|---|---|---|---|---|---|
| wins | +1.25 | −0.42 | +0.83 | **+1.04** | +0.21 | −0.21 | −1.67 | **ADDITIVE** (hw 5.60) |
| k≤200 | +2.50 | +0.00 | +2.50 | **+2.29** | −0.21 | −0.21 | −0.62 | **ADDITIVE** (hw 6.14) |
| k≤300 | +1.87 | −3.54 | −1.67 | **+1.04** | +2.71 | −0.83 | −1.04 | super-add (hw 6.31) |
| ourcore | −1.67 | +1.46 | −0.21 | **+0.63** | +0.83 | −0.83 | +1.87 | **ADDITIVE** (hw 5.38) |

**DELIVERY / ECO COLUMNS (absolute vs parent)**

| column | D527 | D528 | SUM | **D529** | INT | GAP | KZ |
|---|---|---|---|---|---|---|---|
| d100 mean | +10.56 | +14.16 | +24.72 | **+9.47** | −15.25 | −4.69 | −2.91 |
| d300 mean | −1.56 | **+101.37** | +99.80 | **+26.66** | −73.15 | **−74.71** | −57.34 |
| dend mean | −32.69 | +11.35 | −21.33 | **+50.54** | +71.87 | +39.19 | +37.77 |
| harv @ r50 | +0.07 | −0.04 | +0.04 | **−0.05** | −0.09 | −0.13 | +0.01 |
| harv @ r100 | +0.11 | −0.06 | +0.04 | **−0.05** | −0.09 | −0.15 | +0.01 |
| harv @ r200 | −0.02 | −0.16 | −0.18 | **−0.19** | −0.01 | −0.17 | −0.01 |
| harv @ r300 | −0.06 | −0.05 | −0.11 | **−0.23** | −0.12 | −0.18 | −0.03 |

Cross-instrument gate: `deliv.dend == scoreboard ours_mined` on **2400/2400**
joined rows, 0 replays missing. Denominators travel: n(d100) 437–445,
n(d300) 166–178 (only games that reached r300), n(dend) 480.

### 5.3 ⛔⛔ THE ANSWER — AND THE CORRECTION THAT CHANGES IT

**On CURRENCY the union is ADDITIVE, and the v515 signature does NOT appear.**
`wins`, `k≤200` and `ourcore` all have |INT| below the known zero, and the union's
`GAP` below the best single arm is **−0.21 pp on wins and −0.21 pp on k≤200**
against a known zero that moved **1.67 pp** on the same fixture. **Union ≈ v527
alone**, and v528's kill/win contribution is ~0 — which is what v528's own build
said about itself (`k≤200` exactly flat, its own gap smaller than its own zero).

**On the DELIVERY/ECO columns the point estimates are consistently
SUBADDITIVE — six of seven columns, all the same sign.** The union keeps only
**26%** of v528's r300 delivery gain (+26.7 of +101.4) and runs **the fewest
harvesters of all five arms at every checkpoint from r50 to r300**. That is a
coherent mechanism story: v527's `PSURV_EXTRA` spends *bodies* and v528's
`CONNCOST` re-orders *eco picks*, and together the eco pool ends thinner than
either alone leaves it.

⛔ **BUT THE KNOWN-ZERO YARDSTICK OVER-READ THE HARVESTER COLUMNS, AND SAYING SO
IS THE POINT.** Scored against `KZ`, `harv @ r300` looks like a 7.7× excursion
(−0.23 vs −0.03) and `additivity.py` printed *"⛔ UNION BELOW BEST SINGLE (v515
signature)"* on five of the seven eco columns. **A proper two-sample 95%
half-width says every one of them is INSIDE:**

```
col    arm       mean      sd      n     delta       hw   verdict
h300   flagoff  1.396   2.228    480    -0.031    0.285   inside
h300   v527     1.367   2.289    480    -0.060    0.289   inside
h300   v528     1.377   2.116    480    -0.050    0.278   inside
h300   v529     1.200   1.914    480    -0.227    0.266   inside
d300   v528   983.652 814.737    178  +101.366  169.373   inside
d300   v529   908.941 713.719    170   +26.655  160.849   inside
dend   v529  1031.896 1321.308   480   +50.542  156.809   inside
```

**The known zero is ONE DRAW, not a standard error.** On a low-variance column it
can land near zero by luck and then make any real delta look enormous; on
`d300`, where the sd is 700–800, it landed at −57 and made a +101 delta look
ordinary. **Used alone it fails in both directions.** The honest reading:

> **NO ARM SEPARATED FROM THE PARENT ON ANY COLUMN AT n=480.** The union is not
> measurably better or worse than v527 alone, than v528 alone, or than the
> parent. What this battery establishes is the **STRUCTURE**: additive and
> v527-dominated on currency, subadditive in point estimate on eco, with the
> subadditive sign consistent across six eco columns but no column powered enough
> to bank it.

**Asked plainly, as the brief requires:** *does the union underperform the best
single arm beyond the known zero's own movement — the v515 signature?*
**On the currency columns, NO** (−0.21 pp on wins and on k≤200, against a 1.67 pp
known zero). **On `d300` the gap is −74.7 against a known zero of 57.3 — 1.30×,
the only column where the raw ratio exceeds 1 — and it does not survive its own
interval (hw 161–169).** So: a subadditive *hint* in the eco layer, not a
finding, and nothing like v515's case, where the composite (53.2%) sat **below
door-off alone (54.4%)** on the currency itself.

### 5.4 PER MAP — wins/n [k≤300] {k≤200}

```
map            parent            flagoff           v527              v528              v529
antler         39/60 [31] {14}   38/60 [31] {21}   38/60 [26] {11}   40/60 [29] {14}   41/60 [29] {17}
atoll          39/60 [23] {11}   31/60 [15] { 3}   29/60 [13] { 4}   39/60 [14] {11}   34/60 [13] {11}
drakkarfjord   57/60 [49] {45}   52/60 [42] {40}   59/60 [47] {44}   57/60 [43] {40}   56/60 [45] {41}
fjordgate      37/60 [26] {15}   42/60 [32] {18}   46/60 [37] {24}   33/60 [27] {16}   38/60 [29] {19}
glacierkeep    47/60 [37] {29}   51/60 [38] {28}   50/60 [37] {26}   49/60 [37] {27}   50/60 [36] {21}
midgard        39/60 [20] { 9}   34/60 [22] {12}   36/60 [23] {13}   32/60 [15] { 5}   33/60 [24] {13}
nordkap        39/60 [26] {15}   39/60 [22] {11}   41/60 [30] {22}   43/60 [21] {15}   44/60 [31] {20}
yulerune       52/60 [40] {38}   54/60 [45] {40}   56/60 [48] {44}   54/60 [49] {48}   58/60 [50] {45}
```

⚠ **`atoll` is the one board where the known zero moves violently** — parent 39
vs flagoff 31 wins on byte-identical play, an 8-game swing in a 60-game cell.
Every per-map cell here is one draw of that spread; no map-level claim is made.

### 5.5 TWO CROSS-BUILD NON-REPLICATIONS, REPORTED BECAUSE THEY ARE INCONVENIENT

Both siblings were re-run here, as fired, on a fresh 480-game panel. **Neither
sibling's own banked headline reproduced.**

| | its own build said | this battery says |
|---|---|---|
| v527 wins vs parent | −2.23 pp | **+1.25 pp** |
| v527 k≤200 vs parent | −2.23 pp | **+2.50 pp** |
| v528 k≤300 vs parent | **+5.00 pp** (bar "RISES") | **−3.54 pp** |
| v528 dend mean vs parent | **+149.0** (its clean column) | **+11.35** |

Every one of these is inside its interval in both batteries, so nothing is
contradicted — but **v528's delivery gain, the one column its builder called
clean, is +11 here against a known-zero drift of +38.** ⇒ **The delivery finding
is not established; it needs a powered re-read before anything is built on it.**
Different seed sets, same maps, same opponent, same n. This is the 12 pp
same-bot swing CLAUDE.md warns about, showing up on schedule.

### 5.6 FAILURE REEL — union arm

Selection rule: the **earliest our-core-death on EACH map** for `v529` across the
whole battery (one per map so the reel is not five copies of one board); ties by
lowest seed, then seat A.

```
map            turn  seed seat  replay
fjordgate       104     6    A  scratchpad/s51_v529_build/head/rep/v529_fjordgate_s6_A.replay26
antler          108    20    A  scratchpad/s51_v529_build/head/rep/v529_antler_s20_A.replay26
midgard         157     3    A  scratchpad/s51_v529_build/head/rep/v529_midgard_s3_A.replay26
nordkap         210     4    B  scratchpad/s51_v529_build/head/rep/v529_nordkap_s4_B.replay26
atoll           215    23    A  scratchpad/s51_v529_build/head/rep/v529_atoll_s23_A.replay26

EXTENSION (labelled, NOT part of the reel) — the 2 latest-kill wins:
atoll           965     2    B  · nordkap  953  23  A

deaths = 115 of n=480 (24.0%)   ·   r1000 games = 41 (8.5%)
```

---

## 6. INSTRUMENTS AND THEIR GUARDS

| instrument | guard, and the verdict it was driven to |
|---|---|
| `mergecheck.py` | C1–C4 each driven to **FAIL** on a purpose-built mutation (§1.2) |
| `byte_identity.py` | 3 identity arms + 3 negative controls; A3n's failure surfaced a real limitation and was rescued, not suppressed |
| `byteid_supp.py` | refuses to pass when **S1 is empty** — "identical because nothing fired" is reported as UNMEASURABLE, not PASS |
| `flagoff_ast.py` | pos/neg/if synthetic controls + the real-case `FERRY_HOME_ON` positive control (2 hits found) |
| `sealnt_read.py` | self-tested on 3 synthetic tapes, incl. one that catches a reader blind to the turret column |
| `connread.py` | non-constant-regret guard (distinct=107), empty-tape guard, `cands>0` guard |
| `doseread.py` | reports an arm with an empty SEALNT tape as **BLIND, not zero** |
| `headline.py` | selftest folds all-win/all-loss/mixed to different counters; r300 gate excludes rather than zeroes; cross-instrument gate 2400/2400 |
| `additivity.py` | selftest folds additive / subadditive / superadditive fixtures to INT = 0 / − / + |

⛔ **ONE INSTRUMENT DEFECT CAUGHT, AND IT WAS MINE.** `additivity.py` scores every
verdict against the known-zero arm's excursion. On the harvester columns that
excursion happened to be ~0.01–0.03 while the true half-width is ~0.27, so the
script printed the v515-signature banner on five columns that are plainly inside
their intervals. **Caught by computing the two-sample interval as a second
instrument rather than trusting the first** (§5.3). The script is kept as-is with
the caveat printed in its own header, because the KZ row is still the right
yardstick on the *derived kill* columns v526 measured it for — it is the
low-variance mean columns where it must not be used alone.

⛔ **`execTimeUs = 0` IN ALL LOCAL REPLAYS**, thrice-established across v526/v527/
v528: **"0 TLEs" is not evidence anywhere local.** The platform match test remains
mandatory pre-ship and this build does not substitute for it.

---

## 7. OPEN ITEMS

1. **v528's delivery gain is unreplicated** (+149 → +11.35). Powered re-read
   needed before anything is built on it. — §5.5
2. **The eco subadditivity is a hint, not a finding.** Union runs the fewest
   harvesters of all five arms at every checkpoint; six eco columns agree in
   sign; none is powered. A targeted battery (harvester-count as the registered
   primary, n pooled across windows) would settle it. — §5.3
3. **Every arm is inside every interval at n=480.** Per CLAUDE.md, windows are
   free and pooling is the default: this panel is a structure probe, not a
   currency read.
4. **`FS_V527_SWITCH` (M3 opportunity-cost) carries zero dose in the union too**
   — 0 fires in 48 games, as in v527's 24. Still unpriced.
5. **`FS_V528_WIRE` remains inert** by inheritance (v528 §3); nothing in this
   build re-measured it.
6. **The v527 marker level differs from v527-alone** (47.1 vs 32.7 rounds/game)
   because v528 changes the phase mix. The within-union control is clean
   (63.8 → 47.1) but the cross-build level is not comparable. — §4.1
7. Inherited and untouched: platform CPU test, `_wire_tick`, `FS_CREW_CONVERT`,
   local-fixture self-play caveat.

---

## ARTIFACTS

`scratchpad/s51_v529_build/` — `FREEZE.md5` / `FREEZE_END.md5` (no drift),
`PIDS`, `mergecheck.py` + `MERGECHECK_OUT.txt`, `byte_identity.py` +
`byte_identity.log`, `byteid_supp.py` + `.log`, `standdown.sh` + `.log`,
`flagoff_ast.py`, `spot.sh`, `dose.sh` + `DOSE_OUT.txt`, `doseread.py`,
`connread.py`, `sealnt_read.py`, `drive_headline.sh` + `headline.log`,
`run_battery.py`, `head/results.tsv` (2,401 lines) + `head/rep/` (2,400 replays),
`headline.py`, `additivity.py`, `reel.py`, `HEADLINE_OUT.txt`, `CI_OUT.txt`.

**Raw data only. The verdict lines are the builder's.**

---
## BUILDER VERDICT LINES (s51)
* **v529 ADOPTED AS HEAD on structure**: union proven byte-perfect (AST 551/551; ablation
  identities 16/16 both ways), all mechanisms alive-and-ablatable inside it, currency
  ADDITIVE (no v515 signature; union within noise of best single arm against a known-zero
  that itself moved 1.67pp).
* Currency pricing DEFERRED to the full pool by design: no arm separates from parent at
  n=480 — the panel measures structure, not points. v528's +149 delivery is downgraded to
  NOT-ESTABLISHED (read +11.4 here; both inside intervals — the column is noisy, the
  mechanism (regret 0.000/4,449) remains proven).
* The agent's self-caught additivity over-read (known-zero-as-standard-error) is the
  instrument note of the build: composition banners need two-sample intervals, not a
  one-draw reference. Adopted for future merge batteries.
* ROUTE: v530 (home package) parents on v529; ONE full-pool read prices the v530 composite —
  cheaper and more decisive than pricing v529 separately.
