# BUILD REPORT — `bots/_v526transit`, s51, 2026-08-18

Two shipped changes + one **routed non-change**, one master flag (`LOKI_FS_V526`,
`False` reproduces the parent), from frozen parent `bots/_v525flip`.
Parent digests `scratchpad/s51_v526_build/PARENT_FREEZE.md5`, re-verified
unchanged at write time. Tree uncommitted, per instruction. **PAR=2 STRICT**
throughout; PINCERPOOL reached `5400/5400 COMPLETE` at `2026-08-18T18:31:43Z`
and FLIPPOOL ran the whole build (54 → 2,332 rows, **~31 rows/min before, during
and after** every battery — the shard was not slowed) — neither shard was
touched. Wall clock at write time from `date -u` in the same shell call:
`2026-08-18T19:16:25Z`.

Only `doctrine.py`, `main.py`, `siege.py` differ from the parent;
`eco.py` and `raid.py` are **byte-identical (md5-confirmed)**.

---

## ⛔ TOP LINE — STOP AND REPORT

**`bots/_v526transit` AS BUILT IS A REGRESSION AND MUST NOT BE FIRED.** At
n=480/arm it fails `DEFENCE_ADMISSION_BAR` (share of ALL games ending in a core
kill by r300: **0.510 → 0.381**) and loses `k<=200` by **-11.67pp**, with the
median kill moving **207 → 245**. 0 tracebacks in 3,049 games.

**The two planks are NOT equally responsible, and the split is the deliverable.**
A fourth battery (n=240/arm, independent seeds) isolates them:

* **`FS_V526_TEMPO` (M6) carries the whole regression** — `k<=200` **-10.83pp
  OUTSIDE**, median kill 173 → 237, *alone*. Replicated across two seed blocks.
* **`FS_V526_RDV` (M3) is benign-to-positive on every cell** — wins +4.17,
  `k<=300` +5.42, our-core deaths 61 → 50, all inside band — and is the plank
  that answers Magnus's marker 3.

⇒ The shippable object in this tree is **`FS_V526_RDV` alone**
(`scratchpad/s51_v526_build/arm_rdv_only`, already built and measured). M6's
*diagnosis* is solid and reusable; M6's *fix* is what costs.

---

## 0. THE MANDATE, AND WHAT EACH CHANGE ACTUALLY DID

| | mandate | verdict |
|---|---|---|
| **M6** `FS_V526_TEMPO` | first link at probe cadence; root-cause first | **ROOT-CAUSED; THE FIX IS A NET NEGATIVE.** Cause = **roster sequencing**, measured; every tempo metric MET (first-link median **5 → 3**, ring arrival **11.1 → 9.1 mean**, `arr2 ≤ r16` **98.8% → 100.0%**) — **and the kill got SLOWER.** The eco parity claim FAILED at the mean (harvesters at r30 **2.34 → 1.98**), and this plank alone costs `k<=200` **-10.83pp**. |
| **M3** `FS_V526_RDV` | hold-station + build-tile veto; compliance ≥80% | **PARTIAL, AND IT REFUTED ITS OWN PREMISE.** The muster link was **already 97.3% compliant on this fixture** — the 36% production figure did not reproduce. The plank moved the *later* links (59.9% → 64.7%), duplicate chains 6.2% → 4.7%, split-both 75.3% → 83.0%, ARC_DUP alarm **69 → 6**. Pooled compliance 69.5% → 73.2%, **below the 80% bar**. **On the headline it is benign-to-positive in isolation (§6) — the shippable half of this build.** |
| **M4** (`FS_V526_WALK`) | root-cause first; fix only if transit-local | **ROOT-CAUSED, NOT SHIPPED, ROUTED.** The cause is the **eco layer's ore-adjacency override**, not transit. 13 mid-map stalls over 24 wall-heavy 30x30 games, **0 of 13 involve a ferry/siege body.** |

---

## 1. M6 — THE OPENING TEMPO, AND ITS ROOT CAUSE

The mandate named three candidates (funding order · discovery · roster
sequencing) and required the cause be found before the fix. Five instrumented
games (`scratchpad/s51_v526_build/rc/`, tape `RC TEMPO`), 4 of 5 ferry-active:

```
RC TEMPO 1 id 3 body 1 born 1 lp 0 must 0 why norid ... ti 434 lcost 28
RC TEMPO 2 id 3 body 1 born 1 lp 0 must 0 why norid ... ti 392 lcost 32
RC TEMPO 3 id 3 body 1 born 1 lp 0 must 0 why norid ... ti 344 lcost 36
RC TEMPO 4 id 3 body 1 born 1 lp 0 must 0 why norid ... ti 354 lcost 36
RC TEMPO 4 id 9 body 2 born 4 ...                         <- body 2 BORN here
RC TEMPO 5 id 3 body 1 born 1 lp 0 must 1 why near2        <- first link r5
RC SEAT 1 id 3 seat 0 · RC SEAT 2 id 5 seat 1 · RC SEAT 3 id 7 seat 2 · RC SEAT 4 id 9 seat 3
```

* **FUNDING IS EXCLUDED.** The bank is **434 Ti against a launcher price of 28**
  in the first round the lead runs, and never binds in any of the four games.
* **DISCOVERY IS EXCLUDED.** The lead prints a resolved enemy-core `dsq` from r1.
* **ROSTER SEQUENCING IS THE CAUSE, 4/4 games, identically.**
  `_fs_relay_mustered` returns False with reason **`norid` — body 2 has not
  reported** — for rounds 1–4, because body 2 is `FS_CREW_SEAT = 3` and the Core
  spawns one builder per turn. And the muster branch **`return`s**, so the lead
  does not move either: **four rounds of a rush spent standing still.**

**THE FIX IS THE SEAT, NOT THE MUSTER.** `FS_V526_CREW_SEAT = 1` (read only
through `fs_crew_seat()`), plus `FS_V526_MUSTER_WAIT = 3` as the backstop for a
body 2 that died or was never appointed (8 was sized against a seat-3 spawn; at
seat 1 it is 5 rounds of dead rush). This is what the double-ferry probe did —
its second `# PROBE:` sacrifice, *"crew seat moved 3→1 for an r1 spawn"*.

⛔ **AND IT IS NOT AN ECO SEAT BEING SPENT — IN THE ROSTER.** `LOKI_ECO_SEATS =
(1,2,3)`; the parent's crew branch removes seat 3, leaving the effective eco
pool `{1,2}`. Moving the crew to seat 1 leaves `{2,3}`. **Same count, one seat
later.** `LOKI2_RUSH_ON` is `False`, so seat 1 was an ordinary expander.

### ⚠ THE PARALLEL-ECO CLAIM IS THE ONE THING THIS BUILD MEASURED AND DID NOT GET

The mandate's own check — *"harvester count at r30 must not regress vs parent"* —
read off the Core's own tape (`RC ECO`, `SLOT_HARVESTERS`), n=192/arm:

```
harvesters at r30   parent mean 2.344   v526 mean 1.984    (-0.36, -15.4%)
                    parent med  2.0     v526 med  2.0      (unchanged)
per map (median):   atoll 2->3 · drakkarfjord 2->1 · glacierkeep 2->1
                    nordkap 1->1 · yulerune 2->2 · antler 3->2 · midgard 4->4
```

**The median holds; the mean does not.** Two mechanisms are confounded here and
this build does not separate them: one eco seat now spawns a round later, and
the chain starts buying launchers ~2 rounds earlier out of the same opening
bank. **Reported as a measured cost, not explained away.** It is an open item.

---

## 2. M3 — THE RENDEZVOUS

The parent's muster behaviour, read off the code and confirmed on the tape: with
no launcher on the board `_fs_relay_point` returns `None`, `may_build` is False,
so body 2 falls through the whole ferry branch to `self.tgt = T;
self._nav(...)` — **it walks at the enemy core while the lead stands still
waiting for it.**

`_v526_rendezvous` (siege.py) replaces that fall-through with three states:

1. **lead not visible → HOLD** (never drift; a blind body walking at the enemy
   core *is* the drift).
2. **lead already at the ring (`dsq_core(lead) <= FS_RING_DSQ`) → fall through to
   the parent's walk.** ⛔ **This clause is MEASURED, not defensive** — see §2.1.
3. **on one of the lead's forward build candidates → STEP OFF**, to the legal
   neighbour that is not itself a candidate and is closest to a candidate (i.e.
   closest to the future launcher's `d²<=2` pickup envelope). Otherwise **HOLD**.

The veto set is not a guess about the lead's siting: it is `_fs_build_ferry`'s
own filter (the lead's cardinal neighbours, minus any not strictly nearer the
ferry target), so it is a superset of whatever tile the lead actually picks.

⛔ **NOT lead-follow.** That variant was tried by the probe, measured NEGATIVE
(two-throw links 2 → 0, n=6) and reverted, because it walked ONTO that tile.
**The recorded signature is beaten: two-throw links do not collapse — the
muster link stays at 96.6% and the later links rise.**

### 2.1 THE FJORDGATE REGRESSION THE FIRST BATTERY CAUGHT

The first mechanism read (pre-guard, `scratchpad/s51_v526_build/mech/`) showed
**fjordgate `b2chain` 12/12 games** against the parent's 2/12: on a 10x10 board
the lead is at the enemy ring by r1 (`arr1` median **1**), never buys a link, so
body 2 held station for the whole `FS_RELAY_PATIENCE` and then bought a **second
chain** — the exact duplication M3 exists to remove. Clause 2 above is the fix;
after it, fjordgate `b2chain` is **0/24**. The pre-guard battery is kept in-tree
as the counter-example.

---

## 3. M4 — ROOT-CAUSED, **NOT SHIPPED**, ROUTED

24 instrumented games on the wall-heavy 30x30 class (valkyrie · glacierkeep ·
drakkarfjord · ragnarok, 3 seeds × 2 seats), `scratchpad/s51_v526_build/rc3/`,
scanned by `stallscan2.py` (self-tested: a nav-silent stall, a nav-busy stall
and a clean walker must come out as three different cells):

```
total stalls >= 8 rounds: 79   MID-MAP (d^2 > 64 from BOTH cores): 13
mid-map nav-silent: 4   ·   nav-called: 9
0 of 13 involve a ferry/siege body (fs 0, roles expand/defend, 13 of 13)
```

The reproducer of Magnus's *"(8,10) r32 tries to go around, why did it stop?"* is
`valkyrie_s1_A` id 7 at **(9,10), r37–r59**, and the tape names the mechanism:

```
RC WALK 36 id 7 role expand pos 9,10 tgt 9,10 want NORTH  verdict moved
RC WALK 37 id 7 role expand pos 9,10 tgt 9,9  want CENTRE verdict centre   (x23)
```

* **(9,9) is ORE** (`map_encode`, env 2) and is occupied by **our own home
  defender**, parked on its post and never leaving.
* `_expand`'s **adjacent-ore override** re-targets any 8-neighbour ore tile with
  no *building* on it — **a body is not a building** — so `self.tgt` is forced
  back to (9,9) every round, defeating the `stuck >= 5` re-pick (which advances
  `ore_cursor` and *would* have returned a different tile).
* `_bfs_direction` then returns `CENTRE` **correctly**: the target tile is
  blocked, its cardinal neighbours become the goals, and `start in goals` is the
  arrival-by-adjacency convention every build in this bot depends on.
* `can_build_harvester` is False while a body stands there, so nothing is built
  and nothing ever changes.

⇒ **TRANSIT IS BEHAVING TO SPEC.** The absorbing state is the ECO layer's
ore-adjacency override having no body test. `FS_V526_WALK` ships `False` and is
kept as a greppable marker of the routing. The second mid-map family (ragnarok
`id 7` at (16,16), **183 rounds, 184 nav calls**, standing *on* ore in an ore
field) is the same layer.

**ROUTE:** eco `_expand` ore-adjacency override — skip an ore tile occupied by a
builder bot of either team; and/or have `_pick` ban a target that has been
adjacent-but-unbuildable for N rounds.

---

## 4. VERIFICATION

### (a) FLAG-OFF BYTE-IDENTITY **18/18** + NEGATIVE CONTROL **14/14**

`scratchpad/s51_v526_build/byte_identity.py`. Method: `NOISE_ON = False` on
**both** sides (ours and `bots/_v488beltbreak2`), `--tle 0`, seed 526919, replay
bytes `cmp`'d — `--seed` alone does not pin a game (v518 finding 1/2).

```
ARM 1  LOKI_FS_V526=False  vs TRUE PARENT bots/_v525flip
       IDENTICAL on 18/18 (9 maps x 2 seats), 0 tracebacks
ARM 2  v526 AS FIRED       vs the same parent   (THE NEGATIVE CONTROL)
       DIFFERS   on 14/14 ferry-active cells
       IDENTICAL on  4/4  standdown cells (midgard CRIPPLE, archipelago GATED)
RESULT: PASS
```

Without arm 2 an "identical" result would also be produced by a plank that never
runs; with it, the flag is proved to be the only thing that moved.

### (b) GATED/CRIPPLE STANDDOWN ASSERTION

* **midgard (CRIPPLE):** 24 of 24 games per arm, `links = 0`, `first_link = -1`,
  `arr1 = arr2 = -1` — **0 siege clauses reached**, both arms.
* **archipelago (GATED):** `FS_MAP_SKIP`, unchanged by this build; byte-identical
  to the parent in both arms, both seats; plus the direct clause count in §4(e).

### (c) AST DERIVED-DEFAULT SCAN — 0 HITS, WITH ITS POSITIVE CONTROL

`scratchpad/s51_v526_build/flagoff_ast.py` (extended from the v525 tool, same
method). Guard driven all three ways (positive / negative / module-level `if`).

```
GUARD: pos=True neg=False if=True
v526 derived defaults: 0
v525 / v524 / v522 / v521 / v520 / v519 / v518 (inherited): 0 each
REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard):
    2  [(3011,'FERRY_HOME_ON','LOKI_FS_CREW'), (3011,'FERRY_HOME_ON','FS_CREW_ON')]
TOTAL: 0    RESULT: PASS
```

The `FERRY_HOME_ON` pair is the **positive control** the mandate asked for: it
confirms the scanner is not blind to the real defect class while returning 0 for
v526.

Both v526 read sites were driven both ways in-process:
`fs_crew_seat()/fs_muster_wait()` return `1/3` with the master on and `3/8`
(the parent's constants) with it off.

### (d) THE M-METRICS, n=192/arm (8-map mechanism panel, 2 time-adjacent blocks)

Instrumented copies of BOTH trees (`instrument.py`, every substitution asserts
its own match count), interleaved per cell, PAR=2. Parser `mechread.py`, whose
`--selftest` drives a synthetic COMPLIANT and a synthetic NON-COMPLIANT tape
through it and asserts **13 metrics come out different in both directions**.

```
arm      n    firstlink  arr1  arr2   harv30  links  comply        MUSTERLINK    restlinks     b2chain      split_both  ARC_DUP  ARC_COL  APPT  scale30
                 (med)   (med) (med)   (med)                                                                                                    (med)
parent  192      5        9.0  11.0    2.0     580   403/580 69.5% 145/149 97.3% 258/431 59.9% 12/192  6.2% 119/158 75%   69       99      0    238
v526    192      3        7.0   8.0    2.0     563   412/563 73.2% 144/149 96.6% 268/414 64.7%  9/192  4.7% 132/159 83%    6       96      0    237
```

Means, same pool: `first_link` 9.25 → 8.36 · `arr1` 9.77 → **7.93** · `arr2`
11.14 → **9.10** · `P(first_link <= 5)` 0.966 both · **`P(arr2 <= r16)` 0.988 →
1.000**. 0 tracebacks in 384 games.

**What each M-metric says, and two of them are nulls:**

* **M6 first-link cadence: MET.** Median **5 → 3** on 6 of 7 ferry-active maps.
  ⛔ **THE MANDATE'S MUTANT BAR IS NOT MET AND SAYING SO IS THE POINT:** the bar
  was *"mutant reproduces >= 8"*, and the parent on this local fixture reads
  **5**, not 8. Magnus's r11 marker came from a LIVE replay against a real team;
  the local fixture vs `_v488beltbreak2` never showed r8–11 in any arm. **The
  cause found (roster sequencing, 4 dead rounds) is fixture-independent — it is
  a spawn-order fact — but the SIZE of the production delay is not reproduced
  here, so 5→3 is the measured effect and r11→3 is not claimed.**
* **M6 ring-arrival budget: MET.** `arr2 <= r16` goes 98.8% → **100.0%**.
* **M6 eco non-regression: FAILED at the mean** (§1). Median holds.
* **M3 two-rider compliance: THE 36% BASELINE DID NOT REPRODUCE.** The muster
  link — the one M3 acts on — is **97.3% compliant in the PARENT** on this
  fixture. **A plank cannot move a metric that is already at ceiling in the
  control**, and the honest reading is that the local fixture does not contain
  the production failure Magnus saw. What moved instead is the **later** links
  (59.9% → 64.7%) and pooled compliance (69.5% → 73.2%) — **both short of the
  >=80% bar.**
* **M3 terminal split: IMPROVED.** Both-arcs-claimed 75.3% → 83.0% of games that
  reached a split. Per map v526 is at 24/24 on drakkarfjord, glacierkeep,
  nordkap and 22/24 on yulerune.
* **M3 duplicate chains (the 3-launcher marker): IMPROVED, NOT CLOSED.** A game
  in which body 2 built its own hop: **6.2% → 4.7%**; the target was <=1 chain
  per game (i.e. 0%). **Cost model:** team cost scale at r30 is **238 → 237** —
  the duplication is not showing as scale inflation at r30 on either arm, so the
  +10%-per-extra-launcher price Magnus flagged is real per-instance but is **not
  a measurable pooled cost at this rate**.
* **M3 alarms: ARC_DUP 69 → 6, APPT (appointment race) 0 → 0.** ⛔ **NEITHER IS
  ZERO ON THE MANDATE'S TERMS AND THE PARENT IS WHY:** ARC_DUP is **non-zero in
  the CONTROL** (69, of which 65 on nordkap), so it is a pre-existing defect this
  build reduces by 91% rather than one it introduces. `ARC520 COLLIDE` (a
  collision detected and resolved by the higher-`fs_body`-yields rule) is 99 vs
  96 — flat, and pre-existing in both.

⚠ **ONE-DRAW WARNING, MEASURED ON THIS OWN FIXTURE.** The first mechanism block
and the second gave the **byte-identical parent tree** 73.2% and 65.0% pooled
compliance on the same 96 cells (`--seed` does not pin a game with NOISE on —
v515 finding 1). The n=192 pool above is two blocks; every compliance figure
here carries that spread and none of them is a currency read.

### (e) THE ARCHIPELAGO / MIDGARD STANDDOWN CLAUSE COUNT

See §5.3 (run after the batteries, so it appears with the rest of the raw data).

---

## 5. THE HEADLINE — **v526 IS A REGRESSION AND MUST NOT SHIP AS FIRED**

n=**480/arm** (8-map panel = the 6-map panel set + antler + fjordgate, so the
v525-flipped maps are represented), 10 time-adjacent blocks × 3 seeds × 2 seats,
arms **interleaved per cell**, PAR=2, vs `bots/_v488beltbreak2`, 0 tracebacks in
1,440 games.

```
=== THE KILL_TARGET PANEL ===
arm          n    wins%    <=r150      <=r180      <=r200      <=r250      <=r300     medkill  ourcore  tb
parent     480   72.3%  119(0.248)  144(0.300)  159(0.331)  215(0.448)  245(0.510)     207      117    0
flagoff    480   72.9%  124(0.258)  162(0.338)  190(0.396)  236(0.492)  260(0.542)     185      113    0
v526       480   66.2%   51(0.106)   85(0.177)  103(0.215)  148(0.308)  183(0.381)     245      144    0

v526    vs parent   wins     -6.04 pp (hw 5.84)  OUTSIDE
v526    vs parent   k<=200  -11.67 pp (hw 5.64)  OUTSIDE
v526    vs parent   k<=300  -12.92 pp (hw 6.29)  OUTSIDE
flagoff vs parent   wins     +0.62 pp (hw 5.64)  inside
flagoff vs parent   k<=200   +6.46 pp (hw 6.09)  OUTSIDE     <-- READ THIS, see below
flagoff vs parent   k<=300   +3.12 pp (hw 6.32)  inside
```

**`PROGRAMME.md` `DEFENCE_ADMISSION_BAR` (ITT: the share of ALL games ending in
a core kill by r300 must not FALL vs control) is FAILED: 0.510 → 0.381.** Our
own core dies in 144 games against the parent's 117. Median kill 207 → 245.

### 5.1 ⛔ THE KNOWN-ZERO ARM READ **+6.46pp OUTSIDE** AND THAT IS THE HALF-WIDTH THAT MATTERS

`flagoff` is `bots/_v526transit` with `LOKI_FS_V526 = False`, **proved
byte-identical to the parent on 18 of 18 deterministic cells** (§4a). It cannot
differ from the parent by construction, and at n=480 it read **+6.46pp on
k<=200, OUTSIDE its own naive band** — the v518 finding-2 false-positive class,
reproduced here in this build's own control rather than assumed away.

⇒ **The naive half-widths above understate the real spread by roughly 2x.** The
honest reference is the known-zero excursion (~6.5pp), and against it:

| contrast | delta | vs the known-zero excursion |
|---|---|---|
| v526 k<=200 | **-11.67 pp** | ~1.8x |
| v526 k<=300 | **-12.92 pp** | ~2.0x |
| v526 wins | -6.04 pp | ~0.9x — **NOT separated from noise** |

**The kill-timing regression survives the correction; the win-rate delta does
not.** Both are reported; only the first is claimed.

### 5.2 PER MAP — the regression is broad, not one board

```
map            parent  wins [k<=300] {k<=200}   flagoff                 v526
antler         45/60  [32] {16}                 43/60  [33] {20}        29/60  [17] {10}
atoll          31/60  [20] {12}                 35/60  [19] {13}        32/60  [19] { 9}
drakkarfjord   58/60  [44] {40}                 60/60  [47] {43}        51/60  [25] { 9}
fjordgate      40/60  [28] {10}                 42/60  [35] {19}        30/60  [22] { 8}
glacierkeep    50/60  [33] {20}                 50/60  [39] {29}        55/60  [26] {13}
midgard        29/60  [13] { 6}                 28/60  [10] { 4}        28/60  [17] { 5}
nordkap        36/60  [26] {17}                 38/60  [31] {20}        36/60  [18] {14}
yulerune       58/60  [49] {38}                 54/60  [46] {42}        57/60  [39] {35}
```

`k<=200` falls on **7 of 8** maps. **drakkarfjord is the extreme and it is the
diagnostic one: 40 → 9**, on the map where the mechanism panel says v526
arrives EARLIER (`arr2` 16 → 14) with **100% link compliance** and where
`harv30` fell 2 → 1. ⇒ **THE RIDERS ARRIVE SOONER AND CONVERT WORSE.** The
leading hypothesis, stated as a hypothesis: the chain buys its launchers ~2
rounds earlier out of the same opening bank and one eco seat lands a round
later, so the bodies reach the ring **underfunded for the seal/sentinel purchase
the kill depends on** — Magnus's own ruling-2 economy gate, arriving from the
tempo side. midgard is the only cell where v526 is up on `k<=300` (13 → 17), and
midgard is CRIPPLE — i.e. **the plank is off there**, so that cell is noise.

### 5.3 FAILURE REEL (rule: earliest our-core-death per map, v526 arm, capped at 5)

```
map            turn  seed seat  replay
fjordgate       96    20   B    scratchpad/s51_v526_build/head/rep/v526_fjordgate_s20_B.replay26
antler         108    18   A    scratchpad/s51_v526_build/head/rep/v526_antler_s18_A.replay26
midgard        141    17   A    scratchpad/s51_v526_build/head/rep/v526_midgard_s17_A.replay26
atoll          168     7   B    scratchpad/s51_v526_build/head/rep/v526_atoll_s7_B.replay26
nordkap        173     7   A    scratchpad/s51_v526_build/head/rep/v526_nordkap_s7_A.replay26

EXTENSION (labelled, not part of the reel) -- the 2 latest-kill wins:
yulerune       900     4   B    .../v526_yulerune_s4_B.replay26
nordkap        893     1   B    .../v526_nordkap_s1_B.replay26

deaths 144 of 480 (30.0%)  ·  r1000 games 52
```

---

## 6. ATTRIBUTION — **M6 CARRIES THE REGRESSION; M3 IS CLEAN**

Because the headline is a stop-and-report negative, the two planks were split
apart in a fourth battery: `tempo` = `FS_V526_RDV = False`, `rdv` =
`FS_V526_TEMPO = False` (both verified in-process — `fs_crew_seat()`
returns 1/3 and 3/8 respectively). Same 8-map panel, 5 blocks × 3 seeds × 2
seats, **n=240/arm**, arms interleaved, PAR=2, seeds 101-115 (a distinct block
from the headline's 1-30), 0 tracebacks in 960 games.

```
arm        n    wins%     <=r150      <=r200      <=r300     medkill  ourcore
parent   240   72.1%   67(0.279)   87(0.362)  118(0.492)      173       61
rdv      240   76.2%   56(0.233)   82(0.342)  131(0.546)      201       50
tempo    240   71.7%   30(0.125)   61(0.254)  110(0.458)      237       63
v526     240   68.3%   33(0.138)   51(0.212)  107(0.446)      235       68

rdv   vs parent  wins +4.17 (hw 7.83) inside · k<=200  -2.08 (hw 8.55) inside · k<=300 +5.42 (hw 8.94) inside
tempo vs parent  wins -0.42 (hw 8.04) inside · k<=200 -10.83 (hw 8.26) OUTSIDE · k<=300 -3.33 (hw 8.93) inside
v526  vs parent  wins -3.75 (hw 8.18) inside · k<=200 -15.00 (hw 8.10) OUTSIDE · k<=300 -4.58 (hw 8.93) inside
```

* **M6 (`FS_V526_TEMPO`) is the harmful plank.** Alone it moves `k<=200` by
  **-10.83pp** and the median kill from **173 to 237**, and the full build
  (both planks) is worse still at **-15.00pp**. This reproduces the headline's
  `k<=200 -11.67pp` at n=480 on independent seeds — **the only figure in this
  report that has been measured twice, on separate seed blocks, and come out the
  same way both times.**
* **M3 (`FS_V526_RDV`) is benign-to-positive on every cell**: wins +4.17,
  `k<=300` +5.42, `k<=200` -2.08, our-core deaths 61 → **50**, all inside band.
  On the mechanism panel it is the plank that drove ARC_DUP 69 → 6, split-both
  75% → 83%, duplicate chains 6.2% → 4.7%.
* **The two do not interact benignly**: `rdv` alone is up on `k<=300` and
  `tempo` alone is down, and the combination is at the bottom on `k<=200`.

⚠ n=240/arm, one draw, naive half-widths; only the `k<=200` result is claimed,
and only because it replicated.

### 6.1 THE MECHANISM, STATED AS A HYPOTHESIS THE NEXT BUILD SHOULD TEST

M6 does exactly what it was asked to do — first link r5 → r3, `arr2` mean
11.1 → 9.1, `arr2 <= r16` at 100% — **and the kill gets SLOWER.** The bodies
arrive sooner and convert worse. Two costs land together and this build did not
separate them:

1. **the eco seat**: `harv30` mean 2.34 → 1.98 (§1), one expander a round later;
2. **the bank**: the chain starts buying launchers ~2 rounds earlier out of the
   same opening 500, so the seal/sentinel purchase at the ring is later or
   smaller.

Both point at Magnus's ruling-2 economy gate arriving from the tempo side: **an
earlier arrival that cannot be funded is worse than a later one that can.**
⇒ The next iteration of M6 should buy the tempo **without** moving an eco seat
(candidates: leave `FS_CREW_SEAT` at 3 and instead let the LEAD build link 1
before the muster, catching body 2 on link 2; or gate the seat move on the bank).

---

## 7. VERDICT AND FLAG DOCTRINE

**Raw data above; the builder types the verdicts.** What the data supports:

* ⛔ **DO NOT FIRE `bots/_v526transit` AS BUILT.** `LOKI_FS_V526 = True` with
  both sub-flags on fails `DEFENCE_ADMISSION_BAR` (r300 timely-kill share
  0.510 → 0.381 at n=480) and loses `k<=200` by ~12pp, replicated.
* ✅ **`FS_V526_RDV` is shippable on its own evidence** and is the plank that
  answers Magnus's marker 3. The one-line arm that does it is
  `FS_V526_TEMPO = False` on this tree (`scratchpad/s51_v526_build/arm_rdv_only`,
  already built and measured at n=240).
* ⛔ **`FS_V526_TEMPO` needs a different implementation**, not a different
  threshold. Its diagnosis (roster sequencing, 4 dead rounds, funding and
  discovery excluded on the tape) stands and is reusable; its FIX (moving the
  crew seat) is what costs the eco.

### FLAG DOCTRINE COLLISIONS FOUND

1. **`FS_V526_TEMPO` collides with `LOKI_ECO_SEATS` implicitly.** The eco pool
   is defined by subtraction (`LOKI_ECO_SEATS` minus whatever the crew branch
   claims), so a change to `FS_CREW_SEAT` silently re-partitions the economy
   with no flag naming that effect. **The roster has no single read site.** This
   is why the harvester census had to be measured rather than reasoned.
2. **`FS_V526_RDV` inherits `FS_RELAY_PATIENCE` as a hidden escape hatch.** Hold
   station + a 6-round patience means "hold, then buy a second chain" — the
   fjordgate 12/12 duplication (§2.1). Fixed here by the lead-at-ring guard, but
   the general shape (a hold whose timeout is a BUILD) is a doctrine hazard: any
   future hold clause must state what its timeout does.
3. **No new derived defaults** (AST scan, §4c) and **no module-scope reads**:
   both v526 constants are reached only through `fs_crew_seat()` /
   `fs_muster_wait()`, driven both ways in-process.

### THE ARCHIPELAGO / MIDGARD STANDDOWN ASSERTION (§4e, run last)

Instrumented v526, seed 5261, both seats:

```
archipelago_A  HOP=0 TEMPO=0 ARRIVE=0 SPLIT=0 THROW=0  tb=0
archipelago_B  HOP=0 TEMPO=0 ARRIVE=0 SPLIT=0 THROW=0  tb=0
midgard_A      HOP=0 TEMPO=0 ARRIVE=0 SPLIT=0 THROW=0  tb=0
midgard_B      HOP=0 TEMPO=0 ARRIVE=0 SPLIT=0 THROW=0  tb=0
```

**0 siege clauses on 4/4 cells**, and the same instrument emits 5 HOP / 24 TEMPO
/ 2 ARRIVE / 3 SPLIT / 8 THROW on a single drakkarfjord game — so the zero is a
measurement, not a silent instrument. Corroborated by the mechanism panel
(midgard: `links = 0` in 24/24 games per arm) and by byte-identity (§4a).

---

## 8. INSTRUMENT HYGIENE — ONE BLIND INSTRUMENT WAS CAUGHT, AND HOW

The first WALK tape emitted **0 lines across 5 games**. Cause: `eco.py` does not
`import sys`, and the print sat inside a bare `except Exception: pass`, so the
`NameError` was swallowed and the tape looked like "no stalls". It was caught
only because zero was an impossible answer for a case that must produce output.
After the fix the same tape reads **1,914 `moved` · 113 `centre` · 70 `alt*` ·
15 `STUCK`** — four verdicts, i.e. it has been seen to check. `instrument.py`
now **asserts a match count on every substitution** so a silently-unpatched tree
cannot happen again, and both readers (`mechread.py`, `headline.py`,
`stallscan2.py`) carry `--selftest` fixtures driven to the other verdict.
`mechread.py`'s self-test also caught a real field-index bug (`scale30` read the
wrong column) before any number was banked.

---

## 9. ARTIFACTS (all under `scratchpad/s51_v526_build/`)

| what | where |
|---|---|
| parent freeze / child-at-birth digests | `PARENT_FREEZE.md5`, `CHILD_AT_BIRTH.md5` |
| root-cause games (M6 tempo tape) | `rc/`, `rc_run.sh` |
| root-cause games (M4, walk tape fixed) | `rc2/`, `rc3/`, `rc_run2.sh`, `rc_run3.sh` |
| M4 stall scanners (both self-tested) | `stallscan.py`, `stallscan2.py` |
| tape injector (asserts every match count) | `instrument.py` |
| instrumented arms | `inst_v526/`, `inst_parent/` |
| mechanism batteries | `mech/` (pre-guard counter-example), `mech2/`, `mech3/`, pooled `mechpool/`, reader `mechread.py` |
| deterministic fixtures + byte-identity | `eq_v526/`, `eq_off/`, `eq_v525/`, `eq_opp/`, `byte_check/`, `byte_identity.py` |
| AST derived-default scan | `flagoff_ast.py` |
| flag-off (known-zero) arm | `flagoff_arm/` |
| headline battery n=480/arm | `head/`, `drive_headline.sh`, `headline.py` |
| attribution battery n=240/arm | `attrib/`, `arm_tempo_only/`, `arm_rdv_only/`, `drive_attrib.sh` |
| standdown clause count | `standdown/` |
| failure reel | `reel.py` |
| recorded PIDs | `PIDS` |

**Totals: 0 tracebacks and 0 CPU-timeout lines across every game this build ran**
(5 + 4 + 24 root-cause · 576 mechanism · 36 byte-identity · 1,440 headline ·
960 attribution · 4 standdown = **3,049 games**).

---
## BUILDER VERDICT LINES (s51)
* v526 COMPOSITE: REJECTED (DEFENCE_ADMISSION fails; M6-tempo carries the whole regression —
  replicated twice). **M6's lesson banked: tempo bought by moving an eco seat slows the KILL
  (harv30 2.34→1.98) — ruling-2's economy gate read from the other side. Next M6 attempt must
  buy tempo without touching eco seats; until then tempo stays unshipped.**
* **M3 RDV: ADOPTED** — benign-to-positive everywhere, ARC_DUP 69→6, duplicate chains down,
  split-both 75→83%; `arm_rdv_only` is the shippable object. v527 parents on v525+RDV.
* M4: root-caused OUT of transit — the stall is the ECO layer's `_expand` adjacent-ore
  override re-targeting ore occupied by our own parked body (a body is not a building),
  defeating stuck-repick. ROUTED to v528's spec with the reproducer (valkyrie_s1_A id7 r37-59).
* Instrument notes adopted: known-zero read +6.46 OUTSIDE on k200 at n=480 (the recurring
  class — naive halfwidths ~2x understated on derived kill columns at this n; kill-timing
  regression survives the 2x reference, the win delta does not); compliance figures are not
  currency reads (73.2 vs 65.0 same-tree same-method).
