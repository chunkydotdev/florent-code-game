# SCREEN PREREG — `SIEGECREW`: the autopsy-driven ferry-siege CREW package, head-to-head against the PROGRAMME INCUMBENT

Drafted by a fresh opus subagent with NO inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `docs/prereg/BARS.tsv` row, fired no game, started no
shard, and touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md`
nor `QUEUE.md`.

**⭐ THE PURPOSE LINE, AND IT IS NOT THE SAME AS `RINGLADDER`'S.** The sibling
shard three hours ago was fired FOR THE MEASUREMENT, with its own build grid
predicting Band 5 and delivering it (`results.tsv:ringladder-final` — 25.00
[21.01, 28.99] at n=452, catastrophe stop). **`SIEGECREW` is the first arm of
this family whose own grid predicts a PASS**: `_v513siegecrew` read **49/90
(54.4%)** against this exact control on the same paired fixture, against v512's
13/90. **This shard exists to find out whether that 90-game read survives 5,400
games on the pool we actually play** — **eleven of whose fifteen maps carry no
observation of this tree at all, all three of whose GATED maps carry none, and
one of whose four observed maps (`glacierkeep`) reads a perfect 18/18 while
being 1/15 of this shard rather than 1/5 of the grid.**
⚠ **AND THE 54.4% DOES NOT EXCLUDE PARITY: [44.26, 64.63] at local DEFF 0.98
(side-lane D-pass F7 — the build report printed no interval for its headline).
THE SHARD IS THAT READ'S CURE, and that is the cleanest statement of why it is
worth a core.**

**⛔⛔ AND THE SINGLE BIGGEST THING ON THIS PAGE, SAID BEFORE ANYTHING ELSE: THE
`COMBO_BAR = 55.0` AT n=2,700 BINDS, THE ARM'S OWN PRIOR SITS AT ~53.6%, AND
THAT IS EXACTLY THE BAND THE COMBO BAR EXISTS TO KILL. The modal outcome of
firing this shard is a `COMBO-BAR@2700` CANCELLATION AT ROUGHLY 77%
PROBABILITY, WITH P(reaching n=5,400) ≈ 0.07.** Priced in §3. This is not a
reason not to fire; it is a number the builder must have written down before a
core is spent, and it is the one ratification decision on this page that can
change the shard's fate.

**STATUS: drafted BEFORE the `SIEGECREW` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any `docs/prereg/BARS.tsv` row exists,
BEFORE any file named `scratchpad/overnight/SIEGECREW*` exists, and BEFORE the
leg's first game.** Drafting session wall clock at write time
**`2026-08-18T03:21:28Z`** (`date -u`, same shell call); repo HEAD at draft
`bfc24d38` (author time `2026-08-18 05:16:33 +0200`). Verified at draft:
`grep -ci siegecrew docs/prereg/BARS.tsv` → **0**;
`grep -ci siegecrew scratchpad/corefill_work.txt` → **0**;
`grep -ci siegecrew results.tsv` → **0**;
`grep -ci siegecrew elo_history.tsv` → **0**;
`ls scratchpad/overnight/ | grep -ci siegecrew` → **0**.

**⭐ SEED BASE 874000 VERIFIED FREE — AND THE CHECK IS STATED SO IT CAN BE
RE-RUN, NOT ASSERTED.** Four surfaces checked at draft:
* `git grep -l 874000` returns **exactly one file**,
  `corpus/_rebuild/league_matches.tsv.pre-trap9-20260814T192938Z`, where the
  digits are a coincidental substring of an Elo float — the matched context is
  `2.825874000246344`. **Not a seed.**
* `grep -l 874000` over `results.tsv`, `elo_history.tsv`,
  `docs/prereg/BARS.tsv` and `scratchpad/corefill_work.txt` → **no hits** (rc 1).
* `scratchpad/corefill_work.txt` tail: the ferry-siege family's bases run
  **870000 (`SALTRAY`)** and **872000 (`RINGLADDER`)**, on the 2000-spacing
  convention. `874000` is the next free slot and collides with neither.
* `grep -o 'seeds [0-9]*' docs/prereg/BARS.tsv | sort -u` → `830000 · 854000 ·
  870000 · 872000`. **874000 appears nowhere.**
⇒ `tools/overnight.sh` advances the seed every 16 games, so a full 5,400-game
shard consumes **874000-874337**. **Any battery run against this tree must use
a base OUTSIDE that range**, and the next family shard should take 876000.

### LOCK, clock 2 (local shard)
Per the obligations doc's **2026-08-17T07:24:55Z addendum**, cited rather than
restated. **PRIMARY:** the shard tape's own `# FIXTURE … start=` stamp
(`tools/overnight.sh:99` sets `START=$(date -u …)`, `:103` writes it to the tape
before the first game). Quote it verbatim beside the lock commit's git author
time. **BACKSTOP, if the tape carries no `# FIXTURE` line:** the tape's FIRST
COMPLETED ROW `ts` — conservative by construction (measured cost 1-2 s on the
107 stamped local tapes). ⛔ **NOT AVAILABLE: the heartbeat's `STARTING` line**
(`overnight.sh:100` writes it with `>`; every later state overwrites it).
**State which clock was used.** This shard is registered **LOCAL and SAME-HOST**,
so the primary is expected — both sibling tapes (`SALTRAY`, `RINGLADDER`) carry
it.

### ⭐ COMMIT PROVENANCE — BOTH TREES ARE GIT-PINNED AND CLEAN
* **TREATMENT `bots/_v513siegecrew`** — `git ls-files` lists all **five**
  modules; `git status --porcelain bots/_v513siegecrew` is **empty**; added
  whole in **`a54ccf4c`** (`2026-08-17 23:34:47 +0200`;
  `git log --diff-filter=A` returns that commit for every one of
  `doctrine.py eco.py main.py raid.py siege.py`). Digests at draft:
  `doctrine.py 372eb142d5836d575783be64b840efd6` ·
  `eco.py e414393e4728335f5b26aa777d8a11ad` ·
  `main.py 5462b13ba8ed3f2b2172c22626a040ac` ·
  `raid.py 83d55dbd20fcd3a0e3c0a91ae2c6c713` ·
  `siege.py c8262edede75d2171646cfd732ecf86f`.
  ⭐ **`raid.py`'s digest is BYTE-IDENTICAL to `_v512ringladder`'s** — the build
  report's *"raid untouched"* is verified here by `md5`, not taken on the
  report's word.
* **CONTROL `bots/_v488beltbreak2`** — `git ls-files` lists all four; porcelain
  **empty**; newest commit touching it **`997bcd42`
  (2026-08-17 11:12:38 +0200)**; digests
  `doctrine.py b572a721531b77a8c27102bf64313996` ·
  `eco.py 47dc496fc0d14ba950c45c3d43a5f9d0` ·
  `main.py d7f31eedc6795956b72b541eb383c896` ·
  `raid.py c89950470aca51bfaed68712f3690220`.
  **Unchanged since `RINGLADDER` locked** — all four digits match that page's
  quoted values, so the two shards are numerically comparable on an identical
  control.

⭐⭐ **CONTROL IS ALSO THE LIVE HOLDER — THIS IS A SELF-LEG IN THE STRONGEST
SENSE, AND IT IS DISCLOSED IN THE FIRST PARAGRAPH THAT USES IT.**
`bots/_v488beltbreak2` is the **PROGRAMME INCUMBENT** (`PROGRAMME.md:8`) whose
own completed shard reads 53.09% [51.76, 54.42] vs `_v468kladturbo`
(`results.tsv:beltbreak2-final`) — **and the ladder holder is v159 "Sleipnir
v2", the ship built on this chassis** (side lane s51 boot, `now.py` read
03:08:12Z, 1837 Emerald, rank #18/127). ⚠ **`RINGLADDER` recorded the holder as
v160 (a teammate's ship); that tenure ended by x3r0's own rollback at ~20:56Z
and v159 is back.** Every share on this page is written `X% vs
_v488beltbreak2` and never bare, and **nothing on this page prices this tree
against what the FIELD will do to it.**
⚠ **The inference caveat both siblings carried applies unchanged:** *"the
control is the same bytes that produced the completed `beltbreak2-final` tape"*
is inferred from working-tree cleanliness, not from a stamp on that tape. The
tape has no tree-digest column. It is a sound inference and it is an inference.

---

## ⛔ READ BEFORE RATIFYING — EIGHT THINGS THE LANE OWNS

**1. ⛔⛔ THE COMBO BAR, NOT THE CATASTROPHE BRAKE, IS THIS SHARD'S LIKELY
TERMINATOR — AND IT FIRES IN THE EXACT BAND THE ARM IS PREDICTED TO LAND IN.**
`tools/auto_gate.py:286` sets `COMBO_BAR = 55.0`, checked once on the n=2,700
PREFIX (`:919-967`). This arm's composition prior is **53.56%** (§2) and its
grid point is **54.44%** — **both below 55.0 and both above the 51.33 decision
bar.** The gate's own docstring states the design: *"a TRUE-55 combo is killed
50% of the time here, by design."* **A true 53.5-combo is killed ~93% of the
time.** ⇒ **THE DECISION BAR THIS PAGE REGISTERS AND THE OPERATIONAL FLOOR THE
GATE ENFORCES ARE, FOR THIS ARM'S PRIOR RANGE, INCOMPATIBLE: the shard is
priced to be cancelled before it can clear its own bar.** That is a fact about
the house instrument, not about the plank, and the builder rules on it under
**B1**.

**2. THE COMPOSITION PRIOR, COMPUTED AT DRAFT AGAINST V513'S OWN GATE
PREDICATE — NOT INHERITED FROM `RINGLADDER`.** `bots/_v513siegecrew/siege.py:254-300`
(`_fs_gate`) refuses the plank when `max(w,h) < FS_MIN_MAP_DIM(12)`, or core
`d² < FS_MIN_CORE_DSQ(72)`, or the board's `(w, h, sorted core anchors)`
signature is in `FS_MAP_SKIP` (`doctrine.py:2365-2372`). **Verified at draft
that v513's predicate and skip set are UNCHANGED from v512's** — `diff` over
the two `FS_MAP_SKIP` blocks is clean, and the three constants read 12 / 72 /
the same five signatures. **The composition was nevertheless RECOMPUTED rather
than copied**, by evaluating that predicate against every `maps/*.map26` in the
15-map pool of `tools/overnight.sh:68`:

```
GATED  (plank refuses; plays the incumbent raid)   3 of 15 =  20.0%
   antler        14x18  cores (6,4)/(6,12)     d^2=  64  -> DSQ < 72
   archipelago   26x26  cores (5,5)/(19,19)    d^2= 392  -> FS_MAP_SKIP
                                                            (shares snowflake's signature)
   fjordgate     10x10  cores (2,2)/(6,6)      d^2=  32  -> DIM < 12 AND DSQ < 72
SIEGE-ACTIVE                                      12 of 15 =  80.0%
   auroraveil(20x20,256) drakkarfjord(30x30,976) drumlin(25x25,338)
   frostgate(20x20,196)  glacierkeep(30x30,576)  icefloe(20x20,452)
   midgard(30x30,1152)   nordkap(20x26,144)      ragnarok(30x30,1152)
   royale(20x20,196)     valkyrie(30x30,576)     yulerune(20x20,196)
```

**⇒ THE REGISTERED COMPOSITION PRIOR: 0.80 × 54.44 + 0.20 × 50.00 = 53.56%.**
The 54.44 is the arm's own grid (49/90 vs this control, in the fired config);
the 50.00 is the structural null on a map where the plank is switched off.
⭐ **AND THE HEADLINE INTERVAL IS CARRIED WITH IT, because the build report
printed none and the side-lane D-pass flagged that as F7: 49/90 = 54.44% has a
half-width of ±10.19pp at local DEFF 0.98 ⇒ [44.26, 64.63], WHICH CONTAINS
PARITY** (`docs/research/AUDIT-sidelane-v513-Dpass-2026-08-18.md`, F7, quoted as
[44.3, 64.6]; re-derived here to the second decimal, Wald × DEFF; the Wilson
form gives [44.18, 64.34] and nothing on this page turns on the difference).
**The n=90 read does not exclude 50. THIS SHARD IS THAT READ'S CURE, and that is
the cleanest one-sentence statement of why it is worth a core.**
**Composed through the 80/20 dilution: FLOOR `0.80 × 44.26 + 10.00 = 45.41pp`,
CEILING `0.80 × 64.63 + 10.00 = 61.70pp`.**
⭐ **Read the floor carefully: even the pessimistic edge of the arm's own
SAMPLING interval composes to 45.41, just ABOVE the 45.0 catastrophe
threshold.** Unlike `RINGLADDER`, whose ceiling was 41.03 and therefore below
its own catastrophe brake, **this arm's whole sampling range straddles the bar
rather than sitting under it.**

**⛔⛔ AND NOW THE THING THE SAMPLING INTERVAL DOES NOT CAPTURE, WHICH IS LARGER
THAN IT AND IS THE BIGGEST PRICING FACT ON THIS PAGE: THE GRID'S 54.44% IS
CARRIED BY ONE MAP AT A PERFECT 18/18, AND THAT MAP IS 1/15 OF THIS SHARD
RATHER THAN 1/5 OF THE GRID.** Computed at draft from the now-in-repo raw
per-game artifacts (`scratchpad/v513_build/grid/*.tsv`, arms
`shipA2 + shipB2 + shipC`, banked s51 from the dead s50 session tmp):

| grid map | in the 15-map pool? | v513 wins | share | our core died | kills ≤ r300 | r1000 |
|---|---|---:|---:|---:|---:|---:|
| **`glacierkeep`** | yes, siege-active | **18/18** | **100.00%** | **0** | 11 (61.1%) | 6 |
| `drakkarfjord` | yes, siege-active | 11/18 | 61.11% | 7 | 6 (33.3%) | 0 |
| `atoll` | ⛔ **RETIRED 2026-08-13 — the shard NEVER plays it** | 8/18 | 44.44% | 9 | 2 (11.1%) | 2 |
| `midgard` | yes, siege-active | 6/18 | 33.33% | 12 | 3 (16.7%) | 1 |
| `nordkap` | yes, siege-active | 6/18 | 33.33% | 11 | 2 (11.1%) | 1 |
| **pooled (5 maps)** | | **49/90** | **54.44%** | 39 | 24 (26.7%) | 10 |
| **pooled (4 in-pool maps)** | | **41/72** | **56.94%** | 30 | 22 (30.6%) | 8 |
| **pooled, GLACIERKEEP REMOVED** | | **31/72** | **43.06%** | 39 | 13 (18.1%) | 4 |

**A 68pp spread across five maps, and an 18/18 that is not noise** (P = 3.8e-6
under a true 50; per-map half-width at n=18 is ±23pp, so every OTHER cell in
that column IS one-draw territory). ⇒ **the flat extrapolation that produces
53.56% assumes the eight unobserved siege-active maps behave like the average
of a five-map set one of whose members is a shutout.** Sensitivity, computed
rather than waved at (`pooled = 0.80·S + 10.00`, the four observed maps holding
their own shares and the eight unobserved taking the named fill):

| extrapolation for the 8 unobserved siege-active maps | siege-active `S` | **pooled prior** |
|---|---:|---:|
| flat at the grid's pooled 54.44 — **THE REGISTERED PRIOR** | 54.44 | **53.56** |
| flat at the in-pool-4 mean 56.94 | 56.94 | 55.56 |
| at `drakkarfjord`'s 61.11 (optimistic) | 59.72 | 57.78 |
| **at the non-`glacierkeep` observed mean 42.59** | **47.37** | **47.90** |
| at the lowest observed cell 33.33 (pessimistic) | 41.20 | 42.96 |

**⇒ THE MAP-COMPOSITION BAND IS 42.96 - 57.78, WIDER THAN THE ±10.19pp SAMPLING
BAND AND CENTRED LOWER.** It is registered here, before the fire, as the honest
statement of what is not known: **the shard's fate turns on whether the eight
unmeasured siege-active maps look like `glacierkeep` or like `nordkap`, and
nothing pre-lock can tell us which.** ⛔ **The registered prior stays 53.56 —
it is the arm's own headline, the D-pass's number, and choosing a lower one
after seeing the decomposition would be picking the prior to fit the pricing.
The band is disclosed beside it and both are used in §3.**

**⇒ WHAT THE SIEGE-ACTIVE SEGMENT MUST DELIVER, since the gated 20% contributes
a structural 50.00 and nothing more** (`pooled = 0.80·S + 10.00`):

| pooled target | required siege-active share `S` | vs the grid's 54.44 [44.26, 64.63] |
|---|---|---|
| 45.00 (escape the catastrophe brake) | **43.75%** | below the point, inside the CI — near-certain |
| **51.33 (the decision bar)** | **51.66%** | below the point, inside the CI — **plausible** |
| 52.00 (the trend floor) | **52.50%** | below the point, inside the CI |
| **55.00 (the combo bar)** | **56.25%** | ⛔ **ABOVE the point estimate** — reachable only in the upper half of the grid's CI |

**3. PRICED BEFORE THE FIRE — MONTE CARLO OVER THE ACTUAL GATE, NOT A HAND
ARGUMENT.** The clauses simulated exactly as `tools/auto_gate.py` implements
them: CATASTROPHE re-checked on the RUNNING tape at every look from n≥400
(`:823-836`, not prefix-pinned, so it is a repeated look and is simulated as
one, at a 100-game poll cadence); TREND-FLOOR on the n=1,000 PREFIX (`:895-906`);
COMBO-BAR on the n=2,700 PREFIX (`:919-967`); FUTILITY-BAR at MARK-2700 with
the s44 half-a-half-width margin (`:975-990`). Naive intervals, Z95 = 1.96,
local DEFF 0.98 ⇒ no inflation. 20,000 trials per row.

```
true share   P(CATA   P(TREND    P(COMBO   P(reach   scenario
              @400+)   @1000)     @2700)    5400)
   42.96      0.377     0.623      0.000     0.000    map-pessimistic (unobs @ 33.33)
   45.41      0.044     0.956      0.000     0.000    SAMPLING FLOOR (0.8x44.26+10)
   47.90      0.001     0.993      0.005     0.000    GLACIERKEEP-DILUTED (unobs @ 42.59)
   50.00      0.000     0.895      0.105     0.000    parity
   53.56      0.000     0.155      0.773     0.072    ** REGISTERED PRIOR **
   54.44      0.000     0.056      0.654     0.290    grid point, flat
   55.56      0.000     0.011      0.260     0.729    in-pool-4 flat
   57.78      0.000     0.000      0.002     0.998    map-optimistic (unobs @ 61.11)
   61.70      0.000     0.000      0.000     1.000    SAMPLING CEILING (0.8x64.63+10)
```

**⇒ AT THE REGISTERED PRIOR (53.56) THE SHARD COMPLETES 7% OF THE TIME AND IS
CANCELLED AT `COMBO-BAR@2700` 77% OF THE TIME. Even at the grid's own point
(54.44) completion is 29%.** ⛔ **AND THE MAP-COMPOSITION BAND SPLITS THE
TERMINATOR: at 53.56-57.78 the shard dies at the COMBO bar, at 42.96-50.00 it
dies at the TREND FLOOR, and there is no scenario in the registered band where
completion is the modal outcome.** The one clause that essentially never fires
is CATASTROPHE (≤0.04 across everything but the map-pessimistic corner) — **the
opposite of `RINGLADDER`, whose catastrophe stop was the prediction.** At
~10-20 s a game across 8 in-process workers a 1,000-game shard is roughly
**0.5-1.5 wall-clock hours** and a 2,700-game shard **1.5-3**; a full 5,400 is
double that again. **That must be the builder's stated expectation before a core
is spent, not a surprise at 06:30.**
⚠ **The stop depends on `gate_watch` actually running against the BARS row.**
`tools/overnight.sh:47` records that **no firing path calls the gate
automatically**; if nothing polls, the shard runs on. Confirm the watcher is
live, or every probability in that table is a plan and not a mechanism.
⭐ **AND THE COMBO STOP IS A MILD SELECTION, WHICH IS WHY IT IS WORTH A
CARVE-OUT AND A CATASTROPHE STOP IS NOT.** Conditioning on `prefix@2700 < 55.0`
when the truth is 53.56 removes only the top 7% tail: the truncated-normal
expectation is **53.43 against a true 53.56 — a selection of 0.13pp**, versus
the ~+2pp regression the family carries for a catastrophe or trend-floor stop.
At the grid's 54.44 the selection is 0.45pp. **Registered under CUT-SHORT.**

**4. ⛔ ELEVEN OF THE FIFTEEN POOL MAPS CARRY ZERO OBSERVATION OF THIS TREE —
AND ALL THREE GATED MAPS DO. THIS IS NOW EXACT, NOT A BOUND.**
`docs/research/BUILD-REPORT-v513siegecrew-2026-08-17.md` records *"5 maps × 6
reps × 3 pooled blocks"* and does not name the five; the side lane's D-pass
flagged that the evidence base lived in a dead session's `/private/tmp`
(**F3**), and it has since been **banked into the repo at
`scratchpad/v513_build/` (28 TSVs + runners, s51)**. The grid's map list is
therefore readable at draft and was read:
**`scratchpad/v513_build/run_grid.py:17` — `MAPS = ["glacierkeep", "nordkap",
"atoll", "midgard", "drakkarfjord"]`**, with
`run_grid.py:16` `OPP = bots/_v488beltbreak2` confirming the control identity
from the runner itself rather than from the report.

| grid map | status for this shard |
|---|---|
| `glacierkeep` · `nordkap` · `midgard` · `drakkarfjord` | **IN POOL, all four SIEGE-ACTIVE** |
| `atoll` | ⛔ **RETIRED from the pool 2026-08-13 — 18 of the grid's 90 rows (20%) are on geometry this shard NEVER PLAYS** |

⇒ **4 of the 15 pool maps observed; ELEVEN carry zero observation of
`_v513siegecrew`.** ⛔ **`antler`, `archipelago` and `fjordgate` — the whole
GATED segment, 1,080 of this shard's 5,400 rows — carry NONE**, so the primary
segment's 50.0 prediction is entirely untested pre-lock. **And 8 of the 12
siege-active maps carry none either**, which is what the map-composition band in
§2 is measuring. **THE PRIOR IS EXTRAPOLATED FROM FOUR MAPS TO FIFTEEN, ONE OF
THE FOUR READS 18/18, AND THAT IS EXACTLY THE INFORMATION THIS SHARD BUYS.**
⭐ **RATIFICATION BLOCKER B2 IS THEREFORE DISCHARGED AT DRAFT** — it is retained
below only as the record of what was checked and how.

**5. THIS IS A PACKAGE HEAD-TO-HEAD, AND THE PACKAGE IS NOW THIRTEEN
MECHANISMS DEEP.** Treatment `_v513siegecrew` = incumbent `_v488beltbreak2`
**+ v512's FIVE** (launcher ferry, barriers-only collar, eviction rung,
raider-built sentinel, reactive dodge) **+ v513's EIGHT** (A sentinel-and-magazine
only after the salt · B door-turret response · C belt last link + eco lifeline ·
D second body · E rung-2 seal-wait exemption · F the magazine traced ·
G replacement on dedicated store bits + dodge rework · H purposeful spawns).
**Clause isolation for the v513 layer would be `_v513siegecrew` vs
`_v512ringladder` and IS NOT BEING RUN** — one core, and the builder's s51
directive is *"we continue on our launcher experiments from s50, nothing else."*
**CONSEQUENCES, all registered:**
* **A pass promotes the STACK, not any one change.** No sentence at readout may
  attribute a pass to Magnus's sentinel-after-salt rule, to the door response,
  or to the belt fix individually.
* **A fail does not refute any one of them either**, and specifically does not
  refute **the engine facts** underneath them — P6 (enemy bodies block
  barriers), the 1:1 heal-cancel, the unsigned-32-bit store slot — which stand
  on their own evidence.
* ⭐ **AND THE COMPARISON THE 54.4% ACTUALLY LICENSES IS v513-vs-v512, WHICH
  THIS SHARD DOES NOT MEASURE.** The build grid's headline contrast is
  49/90 against the parent's 13/90 **on the same fixture** — that is the
  strongest number this family has, and it is a fact about the ITERATION.
  This shard measures something different and harder: v513 against the
  chassis both of them sit on.

**6. ⭐ THE FIRED CONFIG SHIPS TWO MECHANISMS SWITCHED OFF, AND BOTH WERE
MEASURED OFF RATHER THAN LEFT OFF.** Read from
`bots/_v513siegecrew/doctrine.py` at draft, verbatim:
* **`FS_CREW_ON = False` (`:2741`) — THE SECOND BODY DOES NOT SHIP.** Built to
  spec, measured, and it **lost on every column**: 35 wins vs 49, kills 29 vs
  41, ≤r300 12 vs 24, our core died 48 vs 39, tic=0 12 vs 4, median collected
  380 vs 565, per-block 11/13/11 against 15/17/17. The obvious confound
  (body-denial publishing `FS_PH_SEALED` while merely standing) was tested
  (`FS_CREW_DENY_SEAT=False`, n=60). ⚠ 15.6pp at n=90/arm is at the edge of a
  ±14.5pp interval — **a DIRECTION on every column, not a significance claim**,
  and the report says so. ⛔ **THREE CORRECTIONS FROM THE SIDE-LANE D-PASS,
  carried because this page cites the number:** (a) **F4 — the fixture is NOT
  code-vintage matched.** Two of the three crew-ON blocks (`v513a` 23:03,
  `v513b` 23:05) predate a 23:24 `main.py` edit that all three ship blocks carry
  (which is *why* A/B were re-run as A2/B2 — correct discipline, undisclosed
  consequence). Only `cwONC` is post-move. **The direction survives on the one
  matched pair (17 v 11) and on the matched n=60 pre-move pair (24/60 v 32/60 =
  13.3pp), and `doctrine.py:2721-2726` now carries 13.3pp @ n=60 as the number
  OF RECORD while the report carries 15.6pp @ n=90 for the same decision.**
  This page cites **both** and prefers the matched one. (b) **F5 — the
  denial-acquittal is a fail-to-exclude dressed as an attribution.** *"It is not
  the denial; it is the second body"* rests on a ±17.9pp half-width, which
  excludes almost nothing; and the two arms returned an **exactly identical
  triple (24/20/31) on a non-deterministic fixture** — coincidence (both mutant
  trees verified correctly built), but it deserved a sentence and gets one here.
  ⇒ **REGISTERED: the second body is OFF on a DIRECTION, and the mechanism
  behind that direction is NOT established.**
* **`FS_SALT_LATCH = False` (`:2633`) — the sentinel-stall fallback does not
  ship.** The strict form is **Magnus's direct rule and ships because he ordered
  it**, which is what makes this decision safe. ⛔ **THE MEASUREMENT BESIDE IT IS
  A PRIOR, NOT AN EVIDENCE ROW, AND IS CITED ONLY AS ONE (D-pass F6a):** *"8
  wins / 15 against the strict rule's 9 / 15"* is **n=15/arm, MDE ≈ 35pp**,
  below this repo's own one-draw-law floor of n≥60/arm. **"Measured no gain"
  means "not measured", and it was relayed to Magnus at 21:34 as a decision
  input.** Nothing on this page leans on it.
* ⛔ **ONE MORE `PRIOR, NOT EVIDENCE` ITEM, same class (D-pass F6b): the
  `convert_ammo` minimum dropping 4 → 1 while the siege is live rests on ONE
  instrumented game** (*"blocked 19% of conversion rounds on the diagnostic's
  instrumented atoll game"*) — a shipped constant change against the builder's
  own PROCESS DELTA 2. It is in the fired binary (`main.py:656`) and is part of
  the package under test; **it is not cited on this page as evidence of
  anything.**
* Also off in the fired binary: `FS_CREW_CONVERT = False` (`:2755`, built and
  **never measured** — moot once the crew went off), `FS_MAG_TRACE = False`
  (`:2781`), **`FS_LOG = False` (`:2561`) and `FS_DRAW_ON = False` (`:2558`)**.
⭐⭐ **THAT LAST PAIR MATTERS AND IS THE ONE PLACE THIS ARM IS CLEANER THAN ITS
SIBLING BY CONSTRUCTION.** `RINGLADDER` had to be repaired at ratification —
its tree carried `FS_LOG`/`FS_DRAW_ON` **ON in the treatment only**, under a
binding `--tle 10`, and the builder flipped them in the lock commit (B1, branch
ii). **`_v513siegecrew` was built with them already off AND ITS 90-GAME GRID
WAS RUN IN THE FIRED CONFIG** (build report headline: *"FIRED config
(FS_LOG/FS_DRAW off)"*). ⇒ **THE INSTRUMENTATION CONFOUND DOES NOT EXIST ON
THIS ARM, AND — UNLIKE `RINGLADDER` — THE PRIOR AND THE SHARD DESCRIBE THE SAME
CONFIGURATION.** No flag flip is owed in this lock commit.
⚠ **The residual CPU exposure is NOT cleared by that**, and it is the build
report's own open item 3: v513 adds a per-round `get_nearby_buildings` +
`can_fire_from` scan for home builders (change B) and set operations in the
stand-tile chooser. **`get_cpu_time_elapsed()` is a stub locally (0 across
200,633 `BotOutput` events) and local replays carry no exec-time fields**, so a
TLE regression under `--tle 10` is a BLIND ZERO here, not a measured zero.
**A platform `match test` is required before any ship and this shard is not it.**

**7. THE SHARD'S REGIME IS `NOISE_ON`, AND NO PAIRING EXISTS.**
`bots/_v513siegecrew/doctrine.py:474` and `bots/_v488beltbreak2/doctrine.py:474`
are both `NOISE_ON = True`, and `tools/overnight.sh:31` records that this is
deliberate (*"we want THE BEHAVIOUR WE SHIP"*). The salt is an **unseeded**
`random.Random()`, so two games at one `--seed` are not reproducible and **no
two rows are a matched pair.** ⭐ **THE ONE-DRAW LAW GOVERNS HOW THIS PAGE READS
ITS OWN INPUTS** (s50 process delta 2; established by the v511 agent — three
runs of v510 on `midgard` seed 7 gave r1000 / r133 / r362). **Every
single-game read is ONE DRAW. The build report's demos are illustrations, never
evidence**, and every number quoted here is at n=90, n=60, n=30 or n=15 with
its denominator attached. **Registered: `CLUSTER UNIT: none`, DEFF 0.98,
naive.** The enumeration is performed in the registration block, not asserted.
⛔ **AND THE BUILD REPORT'S OWN NOISE-FLOOR MEASUREMENT IS CARRIED FORWARD AS A
READING CONSTRAINT ON ITS TABLE, NOT BURIED:** *"`FS_CREW_EVICT_NOWAIT=False`
is INERT in the ship config … and it still moved the evictor count 9 → 5"* ⇒
**on the mechanism counters only ZERO-VS-NONZERO contrasts are readable; ratios
are not.** That mutant is the table's placebo and it is the reason F2-F5 below
are quoted as presence/absence and never as effect sizes.

**8. ZERO-SUM SELF-LEG, AND THE CANCEL-FOR-CAPACITY POLICY, PRE-COMMITTED.**
The control is this tree's own ancestor chassis, so **"our win" and "their loss"
are the SAME EVENT** — every per-side metric is mechanically anti-correlated
with its counterpart, which is why the kill-clock reads are registered
WITHIN-ARM and the r300 bar is a one-sided safety backstop.
⚠ **THE STRUCTURAL NULL ON A GATED MAP IS *NEAR* 50.00, NOT EXACTLY 50.00.** On
a gated map the plank refuses and *"the bot plays the incumbent raid doctrine
for that game, unchanged"* (`siege.py:264`) — but the tree is **not
byte-identical** to the control on that path, and v513 widens the gap that
`RINGLADDER` already disclosed: `eco.py` now differs by **75** lines (v512: 14),
`main.py` by **567** (v512: 250), `doctrine.py` by **758** (v512: 483). Change C
(`_eco_spendable(essential=)`) and change H (`_spawn_ore_anchor`) sit in the
ECONOMY and the SPAWN path, which run on **every** map. They are guarded by
`LOKI_FS_CREW and FS_SALT_GATE` / `LOKI_FS_CREW and FS_SPAWN_PURPOSE`, both
True in the fired binary, and several of them are further conditioned on a live
`SLOT_FS` phase a gated map never reaches — **but not all of them are, and this
page does not claim they are.** ⇒ **THE GATED-MAP EQUIVALENCE IS FLAG-AND-STATE
CONDITIONED, NOT BYTE-VERIFIED, AND IT IS WEAKER ON THIS ARM THAN ON EITHER
SIBLING.** That is exactly why the GATED segment is registered as the PRIMARY
SEGMENT with a hard 50.0 prediction (§PRIMARY SEGMENT) — **it is this page's
own control on its own attribution.**
⭐ **CANCEL-FOR-CAPACITY, PRE-REGISTERED NOW so it cannot be improvised later:
if the builder stops this shard to return the core to other launcher-line work
(the s51 plan names `FS_CREW_CONVERT` and the replacement-funding design as the
session's other items), that is an OPERATIONAL CANCELLATION FOR CAPACITY —
typed `cancellation`, POLICY AND NOT EVIDENCE.** It licenses no sentence about
whether the package pays, the partial share is disclosed as **unselected** (a
capacity stop is blind to the share, unlike a floor, combo or catastrophe stop,
so the selected-pessimistic caveat does NOT apply to it — and saying so is
required, because quoting it would understate the arm), and the rows are kept.

---

## RATIFY: Hypothesis

**HYPOTHESIS (a PACKAGE statement, not a one-mechanism statement).** *The
autopsy-driven ferry-siege CREW package — v512's ferry, barriers-only collar,
eviction rung, raider sentinel and reactive dodge, PLUS Magnus's
sentinel-and-magazine-only-after-the-salt rule, the door-turret response, the
belt last-link and eco lifeline, the rung-2 seal-wait exemption, the traced
magazine, the dedicated-store-bit replacement with reworked dodge, and
purposeful spawns, with the second body and the salt latch shipped OFF — all
behind `LOKI_FERRY_SIEGE_ON` / `LOKI_FS_SEAL_ONLY` / `LOKI_FS_RING_LADDER` /
`LOKI_FS_CREW` and gated off three of the pool's fifteen maps — produces a LOCAL
pooled game share of **51.33% or higher** against the incumbent
`bots/_v488beltbreak2` at n = 5,400 games across all 15 corefill maps and both
seats, WITHOUT pushing our own kill past r300.*

⭐ **REGISTERED DIRECTION: POSITIVE, and this is the first arm in the family
whose page predicts its own bar to clear.** `RINGLADDER` registered a positive
bar with a negative prediction and was right about the prediction. **This page
predicts BAND 1 OR BAND 2** (registered composition prior 53.56, grid point
54.44, bar 51.33, half-width ±1.33 at full n) **and simultaneously predicts that
the shard will be CANCELLED at `COMBO-BAR@2700` before it can say so** (§3,
P = 0.77). **Both predictions are on the record and they are not in tension: the
first is about the plank, the second is about the instrument.**
⛔ **AND THE PREDICTION CARRIES ITS OWN LARGEST DOUBT IN THE SAME BREATH: the
n=90 read that generates it does NOT exclude parity ([44.26, 64.63]), and the
map-composition band runs 42.96 - 57.78 because one of the four observed in-pool
maps reads 18/18 while it is only 1/15 of this shard (§2). A BAND-3 PARITY
READING OR A TREND-FLOOR CANCELLATION IS WELL INSIDE WHAT THE PRE-LOCK EVIDENCE
SUPPORTS, and the page says so before the fire rather than after it.**

**THE MECHANISM CHAIN, stated so it can be wrong.** v512's failure was
diagnosed, not guessed (`docs/research/AUTOPSY-v512-three-maps-2026-08-17.md`,
24 games, causes ranked by measured cost), and v513 answers the ranked list:
* **#1, the door.** 100% of the 1,202 damage events on our core came from enemy
  sentinels planted nearer OUR core than theirs; **40 such plants, 0 attacked,
  38/40 alive at game end**, median warning 56 rounds. Change **B** makes home
  builders peck them.
* **#2, the belt.** `titanium_collected = 0` was **perfect 24/24 separation**
  with "no core-adjacent conveyor"; in 8 of 11 zero games the terminus sat at
  Manhattan 2 — **one 3-Ti link missing.** Change **C** finishes the belt; the
  root cause turned out to be **two of our own reserves deadlocked exactly 6 Ti
  apart** (94.4% of 2,809 eco denials had the money).
* **#3, the healer.** Enemy heals cancel our sentinel fire **1:1, exact to the
  HP in 8 games** — so pre-seal fire nets ZERO. Magnus's change **A** stops
  buying the turret and the magazine before the collar is salted.
* **#4, the magazine.** 73.9% of live-sentinel rounds were dry with ≥10
  unconverted Ti. Change **F** traces it; the root cause was **a SHAPE, not a
  constant** — `convert_ammo` is the only surplus consumer, so the bank
  equilibrates to `ti_floor` and stays there, which is why two blind re-tunes
  had failed.
**⇒ THE CLAIM IS THEREFORE NARROW AND FALSIFIABLE: v512 lost 3 of 4 games to
this chassis because it was blind at home, broke at the belt, and fired into a
healer; fixing those four things — and NOT adding staffing — makes the package
beat the chassis it sits on.** The staffing half of that sentence is the part
the build already refuted on its own fixture (§6), and this shard fires the
configuration that survived it.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship, and the session is under LOCK-IN (no submits/activations/unrated fires by any lane until Magnus reopens).**
**PINNED: N/A — local self-play against our own ancestor chassis. The opponent version is fixed by construction: the control tree is `bots/_v488beltbreak2` at commit `997bcd42`, git-tracked and working-tree clean at draft, digests quoted under COMMIT PROVENANCE and byte-identical to those `RINGLADDER` locked against three hours earlier. There is no opponent churn to pin against and no calibration relevance to protect. ⚠ DISCLOSED TWICE, HERE AND ABOVE: the control is NOT the corefill `scratchpad/CONTROL_PIN` tree (`bots/_v468kladturbo`); it is the PROGRAMME INCUMBENT and it is the chassis under the LIVE LADDER HOLDER v159 "Sleipnir v2" — which is why every share on this page is written `X% vs _v488beltbreak2` and never bare.**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted, over FIVE candidates: (i) **MATCH** — does not exist on this surface: `tools/overnight.sh:138-146` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) **OPPONENT** — degenerate: all 5,400 rows play the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe; (iii) **HOST** — killed by REGISTRATION, not measurement: this shard is registered SAME-HOST, and the obligations doc's Addendum 11 rider (the 0.98 exemption is a WITHIN-HOST measurement; cross-host pooling is not covered) makes splitting it across hosts an amendment typed BEFORE the first row. ⛔ **NOTE THE DISTINCTION THIS PAGE MAKES AND ITS TWO SIBLINGS DID NOT: SAME-HOST IS NOT SAME-WORKER.** Both sibling tapes read `workers=8` in their own `# FIXTURE` line while their preregs registered *"one worker (`WORKERS` unset ⇒ 1)"* — a registration/execution divergence, harmless here because eight in-process workers on one box do not engage the cross-host rider, but not repeated: this shard is registered **SAME-HOST, MULTI-WORKER (8), one box**; (iv) **SEED** — examined because `overnight.sh:134` advances the seed only every 16 games, so 16 rows share one engine seed. It dies for two reasons: 16 does not divide the 30-game map×seat cycle, so those rows span 8 distinct maps × 2 seats and no two share a map, and `NOISE_ON = True` puts an UNSEEDED `random.Random()` spawn salt in BOTH bots, so two rows at one seed are not even reproducible let alone correlated; (v) **MAP** — examined because this plank is EXPLICITLY map-conditional (its own gate refuses 3 of 15 maps) and map heterogeneity is therefore certain. It is a **STRATUM, NOT A CLUSTER**: the runner cycles all 15 maps × 2 seats before repeating (`overnight.sh:135-137`), so the design is map-balanced by construction. ⭐ **AND THAT BALANCE IS MEASURED ON A REAL COMPLETED 8-WORKER TAPE OF THIS EXACT FIXTURE RATHER THAN ASSUMED**: `scratchpad/overnight/BELTBREAK2.tsv` (n=5,400, same runner, same pool) holds gated-map shares of **20.50% at the first 400 rows, 20.20% at 1,000, 20.00% at 2,700 and 20.00% at 5,400**, with seats **exactly 50/50 at every one of those prefixes**. The prefix looks the gate takes are therefore balanced samples, not head-of-list artefacts. A balanced stratum does not inflate the pooled interval. ⚠ **This fifth dismissal governs the POOLED bar only; the per-map and per-segment cuts are sized separately under GATE RESOLUTION.** All candidates die ⇒ DEFF = the measured local constant **0.98** (ρ = −0.020, s39 audit, pair-weighted over 124 shards run by this same runner), i.e. **NAIVE intervals are correct and marginally conservative. The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and importing them would widen every interval here by 24-35% for correlation measured absent.**
**ESTIMATOR: the unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. The shard is exactly balanced (15 maps × 2 seats × 180), so the pooled and map-stratified equal-weight shares coincide by construction; the stratified form is an arithmetic consistency check only, never a second estimator (s28 ring-hold: four estimators inside 0.010 of one bar flipped MEET/MISS among themselves). Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never a bar — seat is worth ~7.6pp on byte-identical arms, which is why n is a multiple of 30. **The r1000/core-kill DECOMPOSITION of the share is a MANDATORY companion read on the same rows: it cannot rescue a failed bar and it CAN downgrade a passing one (THIRD FALSIFIER).** ⛔ **The arm-name normalisation hazard applies to any comparator written for this tape: the shard `winner` column holds an ARM DIRECTORY NAME — normalise to US/OPP before scoring, and note that the substring guard at `overnight.sh:76-79` passes here (`_v513siegecrew` vs `_v488beltbreak2` share no substring, checked at draft).** Any estimate quoted at readout arrives from `tools/cluster_ci.py` (HEAD); the pre-data half-widths here are closed-form Wald with DEFF 0.98 and their arithmetic is shown inline.
**DOSE: the CREW package's own firings, measured on the pre-lock build grid in the SHARD'S OWN FIRED CONFIGURATION (`FS_LOG`/`FS_DRAW_ON` off) and with every guard DRIVEN BOTH WAYS via single-flag mutants (mechanism arms 5 maps × 3 reps = 15 games each; the pooled outcome grid 5 maps × 6 reps × 3 blocks = n=90/arm, paired seeds, local `--tle 10`, `NOISE_ON`). CHANGE A, sentinel-after-salt (`LOKI_FS_CREW`+`FS_SALT_GATE`): pre-seal sentinels **0** ON, against **14** with `salt_off` and **10** with `crewflag_off`. CHANGE B, door-turret response (`FS_HOME_TURRET_RESPONSE`): **152 pecks** at n=15 and a door turret attacked in **11 of 30** logged games, against **0** with `door_off` and **0** with `crewflag_off` — and the v512 baseline this replaces is **0 of 40 plants ever attacked** (autopsy cause #1). CHANGE C, belt last link (`FS_BELT_LASTLINK`): `titanium_collected = 0` in **1 of 15** ON, against **5/15** `belt_off` and **9/15** `crewflag_off`; at the outcome grid the tic-zero rate is **4/90 (4.4%)** against the parent's **46/90 (51.1%)**. CHANGE F, the magazine: **0 of 32** live-sentinel STAT rounds under one shot (**0.0%**) against the v512 autopsy's **73.9%**. CHANGE G: prestand veto **54** dodges vs `prestand_off` **160**; HP-floor retreat **4** vs `retreat_off` **0**. CHANGE D, the crew: **0** promotions in the ship config vs **39** in `crew_var` — the mechanism is present and is switched off deliberately (§6). LADDER PRIORITY INVERSIONS **0 of 804** logged rung firings (in-bot `_fs_rung` probe-mode falsifier). ⚠ **THE FINDING HOLDS AND THE DENOMINATOR IS NOT-ESTABLISHED (D-pass F9a): 0 lines matching `inver` reproduce across the logged replays, but 804 does not reproduce — `rep_logship` carries 507 `FS RUNG` lines and `rep_onlog` 604 (1,111 together), with the mut arms summing higher still. What would settle it: the builder naming which arms the 804 pools. Quoted here with that caveat attached, never bare.** TRACEBACKS **0** across **730** grid rows (the report says 670; the TSVs hold 730, so the claim is conservative and the denominator is corrected here) **+ 165** mechanism/demo games, 296 `.err` files grepped. ⛔ **THE NOISE FLOOR IS MEASURED, NOT ASSUMED, AND IT BOUNDS HOW THIS TABLE MAY BE READ: the INERT mutant `FS_CREW_EVICT_NOWAIT=False` (its only consumer is the support body, which is off) still moved the evictor count 9 → 5, so ONLY ZERO-VS-NONZERO CONTRASTS ARE READABLE ON THESE COUNTERS AND RATIOS ARE NOT.** ⛔ **AND THE DOSE'S FIXTURE IS NOT THE SHARD'S FIXTURE: the grid's five maps are `glacierkeep · nordkap · atoll · midgard · drakkarfjord` (`scratchpad/v513_build/run_grid.py:17`, read at draft), of which `atoll` is RETIRED from the pool and never played by this shard; ELEVEN of the 15 pool maps carry ZERO observation of this tree, ALL THREE GATED maps carry none, and one of the four observed maps (`glacierkeep`) reads 18/18 (§2, §4).** ⛔ **THE DOSE IS NOT DECODABLE FROM THE SHARD: `overnight.sh:138-139` runs with `--replay /dev/null` and the tape's columns are `ts shard game map seed seat winner cond turns` — no entity, build, position, shot, turret, store or stderr information exists on it in either arm, and the runner discards stderr after grepping `Winner:`. Every dose number above is PRE-LOCK and the shard's 5,400 rows lend it none of their power.**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, exact map and seat balance; `tools/overnight.sh:68` has run a 15-map pool since the 2026-08-13 rotation and requires multiples of 30). ⛔ **5400 IS SAID EXPLICITLY because a shard otherwise defaults to a 2700 TARGET, and at 2700 the bar's 1.33pp margin is unreachable against a ±1.89pp half-width.** ⚠ **AND IT IS A PLAN, NOT A FORECAST — see §3: P(reaching it) is 0.069 at the registered prior and 0.290 at the grid's own point.**
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; no accept/attempt distinction and no accepts count. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: the tape carries an unprefixed header line under the `# FIXTURE` line, so a naive `wc -l` over-reports n by exactly one. The registered denominator is **DictReader row count over non-`#` lines, cross-checked against the heartbeat's `n TARGET` and against `max(game id) + 1`.** `NOWINNER` rows are counted in n and excluded from the numerator; their count is reported (both sibling tapes carry 0).
**CUT-SHORT: floor 2700 games for the 51.33 BAR verdict.** Below 2,700 completed rows this arm publishes descriptive tallies (share, per-seat, per-map, per-segment, per-class, kill-round, `cond` mix, the r1000/core-kill decomposition) and takes **NO bar verdict**; the one-sample half-width at 2,700 is ±1.886pp against the bar's 1.33pp margin. An `auto_gate` firing at CATASTROPHE@400, TREND-FLOOR@1000, COMBO-BAR@2700 or FUTILITY-BAR@2700 is an **OPERATIONAL CANCELLATION, not a verdict**, typed `cancellation`; so is a builder cancel-for-capacity (§8). ⭐⭐ **ONE CARVE-OUT, PRE-COMMITTED, AND ON THIS ARM IT IS THE MODAL BRANCH RATHER THAN THE EXOTIC ONE — THE COMBO-STOP CARVE-OUT.** A `COMBO-BAR@2700` cancellation leaves the tape at **exactly the registered 2,700-game floor**, which is the one auto-stop clause on this page that does NOT land below the floor. ⇒ **a COMBO stop DOES license a BAND reading at n=2,700**, on four pre-committed conditions: (a) the completed row count is ≥ 2,700 (DictReader, non-`#`); (b) every band is read at the n=2,700 half-width **±1.886pp**, so Band 1 requires a point of **≥ 53.22** and Band 3's parity interval is correspondingly wider; (c) the share is disclosed as **selected-pessimistic, WITH ITS SIZE** — the selection is `prefix@2700 < 55.0`, whose truncated-normal regression is **0.13pp at the registered prior and 0.45pp at the grid's point** (computed in §3; this is an order of magnitude milder than the ~+2pp a catastrophe or trend-floor stop carries, and quoting the family's generic +2pp here would UNDERSTATE the arm); (d) the r300 admission bar is read at its own 2,700 half-widths and its resolution stated (see GATE RESOLUTION (c) — RMST resolves, timely-kill resolves by 0.16pp and is therefore reported as KNIFE-EDGE). ⛔ **NO OTHER CLAUSE'S CANCELLATION LICENSES ANY BAND.** A TREND-FLOOR@1000 stop (n=1,000, ±3.10pp) and a CATASTROPHE@400 stop (n=400, ±4.90pp) are both below the floor and read `CANCELLED — UNRESOLVED, defaults to the RESTRICTION`; a capacity stop is UNSELECTED and carries no regression caveat at all.
**BAR: 51.33. MDE: 0.00pp — THIS BAR IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE** (OB16 corollary, 2026-08-15T03:52:45Z: the standard corefill band IS `50 ± half_width` at n = 5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes no positive effect size). n for the one exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n. ⭐ **The OB16-form statement is available for free on the BAND: Band 1 requires the CI LOWER bound ≥ 51.33, which carries an implied minimum effect of +1.33pp. That is a property of the BAND, not of the BAR, and the two must not be conflated in a readout sentence.** **The r300 admission read is the OTHER bar on this page and it IS sized.**
**BASE RATE: 50.00**
**BAR SOURCE:** the house-standard corefill futility band, **re-derived at draft rather than copied**: `50 + 1.96 × sqrt(0.25/5400) × 100 = 50 + 1.3336 = 51.3336 → 51.33pp`, local DEFF 0.98 so naive (applying it would give `× sqrt(0.98) = 1.3202`, i.e. a marginally LOWER bar; the family's convention is the naive form and this page keeps it for comparability). The identical bar is carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTA`, `SEALSENTAN`, `ROUTESCORE`, `BELTBREAK-EARLY`, `BELTBREAK-LATE`, `BELTBREAK2`, `RAYDISC`, `SALTRAY` and `RINGLADDER` — **and specifically by `RINGLADDER`, the direct parent arm against this same control, which is what makes the two shards' numbers subtractable.** **Constructed, not observed.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree IS the treatment's own ancestor chassis. ⚠ **WEAKER HERE THAN ON EITHER SIBLING AND SAID SO: the undosed complement is NOT byte-identical, and the gap is LARGER than v512's** (§8 — `doctrine.py` 758 diff lines vs v512's 483, `main.py` 567 vs 250, `eco.py` 75 vs 14, plus a 2,391-line `siege.py` absent from the control entirely), so 50.00 is the structural expectation of the SHIP BEHAVIOUR on a gated map and not of a proven mirror. Empirically calibrated on the same host and fixture by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400** (`results.tsv:idnull140-cert-5400`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it. ⚠ **The two cells are 1.77pp apart**, so a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced — which is why Band 2 is pre-registered as WEAK. **Disclosed before the data.**
**REFERENCE n: none** — the bar's comparator is a STRUCTURAL null of 50.00 generated inside this same shard. ⛔ **The build grid's 49/90 is NOT registered as a reference SAMPLE and no bar on this page is sized against it.** It is the honest PRIOR (§2) and is quoted as one; naming it as a reference sample would make the checker size 51.33 as a two-fixture comparison and correctly FAIL it. ⛔ **The incumbent's own 53.09% vs `_v468kladturbo` (`results.tsv:beltbreak2-final`) is likewise NOT a reference here** — different fixture, different opponent, and local screens are not transitive in this repo (QUEUE #65: 3 concordant, 1 not). ⛔ **Nor is `results.tsv:ringladder-final` (25.00, n=452)** — same control and same pool, but a different treatment tree and a cancelled partial; it is quoted on this page only as the family's prior state.
**TREATMENT TREE: bots/_v513siegecrew**
**TREATMENT DIFF REFS: a54ccf4c^ a54ccf4c**
⚠ **THE REF PAIR AND ITS LIMITATION, stated rather than left for a certifier.** `a54ccf4c` is the commit that introduced `bots/_v513siegecrew` (all FIVE modules added; `git log --diff-filter=A` returns `a54ccf4c` for every one of `doctrine.py eco.py main.py raid.py siege.py`), and naming it is what makes the OB13 intersection machine-computable. **But an ADD-commit intersects EVERY path in the tree, so the git check is weak on its own.** The strong form is the CROSS-TREE diff, which git cannot express as a ref pair, and it is reproduced under THE CHANGE with sizes verified at draft: `doctrine.py` 758 changed lines, `main.py` 567, `eco.py` 75, `raid.py` 28, and **`siege.py` 2,391 lines that DO NOT EXIST IN THE CONTROL AT ALL** — `cmp` clean on NONE of the five. Control pinned at `997bcd42`, unchanged since (`git status --porcelain bots/_v488beltbreak2` empty).
**MECHANISM METRIC READS: `bots/_v513siegecrew/siege.py:1936` — `def _fs_salt_ok(self, ct, rnd, orth_open)`, MAGNUS'S DIRECT RULE (change A: no sentinel and no magazine before the collar is salted), whose sole gate site is `siege.py:1987` `if not self._fs_salt_ok(ct, rnd, orth_open): return False` inside `_fs_sentinel_ok` (`:1977`), with the core-side arming at `main.py:519` `if LOKI_FS_CREW and FS_SALT_GATE:`. Companion sites in the same diff, all new or newly-parameterised and all absent from the control: `bots/_v513siegecrew/main.py:1030` — `def _door_turret(self, ct, p, rnd)`, the door-turret response answering the autopsy's #1 measured cost (0 of 40 plants attacked), hooked at `main.py:1014`; `bots/_v513siegecrew/eco.py:371` — `def _eco_spendable(self, ct, cost, essential=False)`, the belt/eco lifeline whose new `essential` parameter is the fix for the 6-Ti reserve deadlock; `bots/_v513siegecrew/siege.py:296` — `if sig in FS_MAP_SKIP:`, THE MAP GATE, the single line this page's whole composition arithmetic rests on. TREATMENT DIFF TOUCHES: bots/_v513siegecrew/siege.py bots/_v513siegecrew/doctrine.py bots/_v513siegecrew/main.py bots/_v513siegecrew/eco.py bots/_v513siegecrew/raid.py. INTERSECTION: yes — every metric site is a NEW LINE, three of them in files that exist in both trees and one in a file that does not exist in the control at all, needing no import-binding argument (`main.py:41` is `from siege import SiegeMixin`, and the constants bind through `from doctrine import *`). ⚠ A path-only intersection would ALSO pass here and that reading is REFUSED: `grep -c` over the control's four modules returns `LOKI_FS_CREW` 0 · `FS_SALT_GATE` 0 · `_fs_salt_ok` 0 · `_door_turret` 0 · `FS_HOME_TURRET_RESPONSE` 0 · `FS_BELT_LASTLINK` 0 · `essential` 0 · `FS_SPAWN_PURPOSE` 0 · `_fs_try_retreat` 0 · `LOKI_FERRY_SIEGE_ON` 0 · `FS_MAP_SKIP` 0, against 28 · 7 · 3 · 4 · 3 · 6 · 5 · 3 · 3 · 14 · 5 in the treatment. The metric CANNOT read identically in the two arms; it reads structurally 0 in the control. That is the LOKI-18 failure this obligation exists for. ⛔ ONE HONEST EXCEPTION NAMED RATHER THAN HIDDEN: `_build_next_link` (change C's other half) reads 10 in BOTH trees — it is a MODIFIED function, not a new one, and it is therefore NOT used as a metric site; `_eco_spendable`'s `essential` parameter (0 vs 5) is the discriminating read for that change.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_FERRY_SIEGE_ON=True, LOKI_FS_SEAL_ONLY=True, LOKI_FS_RING_LADDER=True, LOKI_FS_CREW=True, FS_MAP_SKIP_ON=True, FS_MIN_MAP_DIM=12, FS_MIN_CORE_DSQ=72, FS_SALT_GATE=True, FS_SALT_GRACE=8, FS_SALT_LATCH=False, FS_HOME_TURRET_RESPONSE=True, FS_DOOR_DSQ=40, FS_DOOR_TI_FLOOR=6, FS_DOOR_MAX_RNDS=40, FS_BELT_LASTLINK=True, FS_ECO_LIFELINE=24, FS_ECO_HEADROOM=8, FS_CREW_ON=False, FS_CREW_SEAT=3, FS_CREW_OPEN_BUILDERS=4, FS_CREW_DENY_SEAT=True, FS_CREW_CONVERT=False, FS_CREW_EVICT_NOWAIT=True, FS_CREW_STALE=6, FS_MAG_REPAIR_BARRIERS=2, FS_MAG_TRACE=False, FS_PRESTAND_AVOID=True, FS_RETREAT_ON=True, FS_RETREAT_HP=14, FS_SPAWN_PURPOSE=True, FS_DODGE_ON=True, FS_DODGE_ON_HIT=False, FS_SENTINEL_MAX=2, FS_AMMO_TARGET=300, FS_AMMO_TI_FLOOR=8, FS_LOG=False, FS_DRAW_ON=False, NOISE_ON=True. MECHANISM CAN OCCUR IN WINDOW: yes** — **NOT ONE of these is a round gate.** `FS_SALT_GRACE`, `FS_DOOR_MAX_RNDS` and `FS_CREW_STALE` are round DURATIONS measured from a live event, not thresholds against the absolute round; `FS_CREW_SEAT`/`FS_CREW_OPEN_BUILDERS`/`FS_SENTINEL_MAX`/`FS_MAG_REPAIR_BARRIERS` are counts; `FS_MIN_MAP_DIM`/`FS_MIN_CORE_DSQ`/`FS_DOOR_DSQ` are lengths and squared distances; `FS_RETREAT_HP` is hit points; `FS_ECO_LIFELINE`/`FS_ECO_HEADROOM`/`FS_DOOR_TI_FLOOR`/`FS_AMMO_TI_FLOOR`/`FS_AMMO_TARGET` are titanium or ammunition; the rest are switches. ⭐ **WHAT DOES BOUND THE WINDOW IN PRACTICE, so it is not read as a promise: the build report's own surprise 2 measured that THE SIEGE PHASE ARRIVES IN THE OPENING, NOT THE MIDGAME — `FS_PH_RING` first seen r6-12 and `FS_PH_KILL` r8-14 — so the observed mass lives in roughly r6-r1000 and r0-r5 is a ferry-only window. That is a property of the chassis, not of these clauses, and it is the OPPOSITE of what the code's own comments assumed.** ⚠ **DISCLOSED so a green tool run with warnings under it does not launder them: `prereg_check.py` may emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE CHECKER ARTEFACTS** — its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a d² of 72, a dimension of 12, a titanium floor of 8 and an ammunition target of 300 all render as *"rounds r0-r<v-1> cannot contain the mechanism"*. The constants are declared anyway. ⛔ **`FS_LOG=False`, `FS_DRAW_ON=False`, `FS_CREW_ON=False` AND `FS_SALT_LATCH=False` ARE DECLARED HERE DELIBERATELY: these are the FIRED values, they were read off `doctrine.py:2561 / 2558 / 2741 / 2633` at draft, and the build grid that produced the 54.4% prior RAN IN THIS SAME CONFIGURATION — which is why, unlike `RINGLADDER`, no flag flip is owed in the lock commit and the prior and the shard describe the same tree.**
**PLANK CLASS: OFFENSIVE — a siege package whose entire object is a core kill: a ferry that inserts a raider into the enemy base, a collar that denies the defender its heal seats and spawn tiles, a magazine and forward sentinel gated to fire only once that collar is salted, and a home-side turret response bought to keep our own core alive long enough for that kill to land. It is not a defensive turret purchase and not an economic plank in the `titanium_collected` sense.** ⚠ **ONE HONEST QUALIFIER, because change B genuinely is home-side: the door-turret response is a DEFENSIVE clause inside an offensive package, and `PLAY_DEFENCE: not_at_the_kill_s_expense` is exactly the rule it must satisfy.** ⭐ **AND THE r300 ADMISSION READ IS REGISTERED ANYWAY, NOT CLAIMED INAPPLICABLE — ON THIS ARM IT IS THE BAR MOST LIKELY TO FAIL AND IT IS THE LEAST WELL PRICED.** A collar is a SIEGE: its mechanism is holding a ring for many rounds. The build grid's own numbers point BOTH ways and the page says so: the ITT timely-kill rate ROSE 8.9% → **26.7%** against the parent, and r1000 games are 10/90 (11.1%) against 9/90 — but the MEDIAN KILL ROUND ROSE 241 → 281 (collider-conditioned: v513 has three times as many kills, so its median includes kills v512 never got; per-block medians straddle at 214 / 414 / 291 and the median is not stable at n=90). **A plank whose mechanism is a siege must carry a delay bar whatever its class label.** Registering it is strictly stricter than the programme requires and CANNOT function as a second chance to pass: **both the share bar and the r300 bar must hold.**
**KILL-ROUND NON-REGRESSION: ⭐ THE PRIMARY IS ITT RMST₃₀₀ WITH AN EXPLICIT REGISTERED MDE OF +5.0 ROUNDS. This is said first and emphatically because the build report scored the SUPERSEDED estimator and called it "the primary" — the side-lane D-pass's F2, and this prereg is the instrument that settles its NOT-ESTABLISHED item 4.** `PROGRAMME.md:534-540` moved the operational estimator to ITT RMST₃₀₀ on 2026-08-16T05:36:10Z and demoted the timely-kill rate to a REPORTED DIAGNOSTIC, explicitly because the timely rate passes by correlating with win share (r² = 0.93). **DEFINITION: mean kill time censored at the r300 horizon over ALL games, a non-kill scoring 300, computed per side on the same rows. SCORED AS AN EXCLUSION: the 95% CI UPPER bound on (treatment RMST₃₀₀ − control RMST₃₀₀) must EXCLUDE +5.0 rounds.** ⭐ **THE MDE IS +5.0 AND IT IS SIZED, NOT ASSERTED: the per-side sd is MEASURED from this arm's own artifacts** (`scratchpad/v513_build/grid/*.tsv`, arms `shipA2+shipB2+shipC`) — **treatment sd 48.03, control sd 49.07, delta sd 68.66** ⇒ half-width **±1.83 rounds at n=5,400** and **±2.59 at n=2,700**, both comfortably inside the 5.0 MDE. *(The sibling-family anchor of sd ≈ 89 ⇒ ±2.37 / ±3.36 is the conservative alternative and also resolves; the measured value is used because RMST is CENSORED at 300 and therefore has a much smaller sd than raw kill time. The sd is recomputed from THIS tape at readout and the half-width with it.)* SECOND REGISTERED FORM, both required, DEMOTED TO A CO-BAR RATHER THAN THE PRIMARY: the ITT timely-kill-by-r300 rate (share of ALL games ending `cond == core_destroyed` with `turns <= 300`, denominator every game played, per side) — its 95% CI LOWER bound on (treatment − control) must EXCLUDE a fall of 3.0pp (MDE 3.0pp; sd anchor 75.28pp ⇒ ±2.01pp at n=5,400 and ±2.84pp at n=2,700). THIRD, a DIAGNOSTIC ONLY because it carries a collider: the kill-win-CONDITIONED share and conditioned median — reported beside the bars, never as either. The treatment's own median kill round crossing 300 is the gross within-arm backstop, and it is a LIVE RISK on this arm: the grid median is 281. ⭐⭐ AND THE PRE-LOCK READ IS NOW AVAILABLE ON BOTH COMPARATORS, COMPUTED AT DRAFT FROM THE BANKED ARTIFACTS — THE DISTINCTION MATTERS AND IS THE ONE PLACE THIS PAGE CORRECTS THE D-PASS: (i) **vs THE PARENT `_v512ringladder`** (the D-pass's figure, re-derived here exactly): treatment RMST₃₀₀ **276.09** (se 5.06) vs parent **289.02** (se 4.15) ⇒ **DELTA −12.93 rounds FASTER, 95% CI [−25.8, −0.1]** — it excludes +5.0 and passes. ⛔ **BUT THAT IS NOT THIS BAR'S COMPARATOR.** (ii) **vs THE CONTROL `_v488beltbreak2`, measured WITHIN THE SAME 90 GAMES — the comparator this shard's bar is actually written on:** treatment **276.09** vs control **276.88** ⇒ **DELTA −0.79 rounds, 95% CI [−15.0, +13.4]** (naive; the two sides are anti-correlated by construction so the true interval is narrower). **It does NOT exclude +5.0 at n=90 — the bar is UNRESOLVED pre-lock, not passed and not failed** — and the ITT timely-kill read on the same 90 games is treatment **24/90 = 26.67%** against control **23/90 = 25.56%**, a difference of **+1.11pp**, i.e. no fall and no resolution. ⇒ **REGISTERED HONESTLY: the r300 bar is DIRECTIONALLY FINE ON BOTH COMPARATORS AND RESOLVED ON NEITHER AT n=90, and the shard is what resolves it.** *(The earlier draft of this line said the bar was "unpriced pre-fire" because the build report never gave the paired control's number; the artifacts now in-repo give it, and the cross-fixture `beltbreak2-final` anchor of 30.80% that looked like a 4.1pp threat is superseded — it was a different opponent on a different fixture and the same-games control reads 25.56%.)* ANCHORS, quoted as anchors and not predictions: build grid kills ≤ r300 24/90 = 26.67% [18.62, 36.62], r1000 10/90 = 11.11% [6.15, 19.26], median kill round 281. ⚠ ZERO-SUM DISCLOSURE, registered with the bar: on a self-leg the two sides' kill counts partition one set of games, so this difference is CONFOUNDED WITH THE SHARE and a PASS in a winning arm is partly automatic — the bar is a ONE-SIDED BACKSTOP against "wins more, all added wins past r300" and licenses no claim that the arm speeds the kill.**
**PRE-STATE: the predicted-change behaviour is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c` over `bots/_v488beltbreak2/{doctrine,eco,main,raid}.py` returns **LOKI_FS_CREW 0 · FS_SALT_GATE 0 · _fs_salt_ok 0 · _door_turret 0 · FS_HOME_TURRET_RESPONSE 0 · FS_BELT_LASTLINK 0 · essential 0 · _fs_supp_turn 0 · FS_SPAWN_PURPOSE 0 · _fs_try_retreat 0 · LOKI_FERRY_SIEGE_ON 0 · FS_MAP_SKIP 0**, against **28 · 7 · 3 · 4 · 3 · 6 · 5 · 3 · 3 · 3 · 14 · 5** in the treatment, and the control has **no `siege.py` at all**. **The incumbent has no ferry, no collar, no at-ring ladder, no salt gate, no door-turret response, no belt last-link clause, no purposeful spawn sort and no map gate: every builder it produces plays the incumbent raid doctrine on all 15 maps.** ⇒ the behaviour this leg predicts to change cannot already be in the target state. The OUTCOME claim is likewise not pre-satisfied: `_v513siegecrew`'s share against the incumbent **does not exist on any tape** (`grep -ci siegecrew` → 0 on the worklist, `BARS.tsv`, `results.tsv`, `elo_history.tsv` and every shard tape at draft), and every band below is a live, pre-named outcome.
**MAP SEGMENT: EXPECTED, AND IT IS NOT AN INFERENCE — IT IS COMPILED INTO THE BOT.** `bots/_v513siegecrew/siege.py:254-300` refuses the entire plank on a map whose `(w, h, sorted core anchors)` signature is in `FS_MAP_SKIP`, or whose larger dimension is under `FS_MIN_MAP_DIM = 12`, or whose core separation is under `FS_MIN_CORE_DSQ = 72`. **Registered per OB15a as a WRITTEN-DOWN conditioning fact and, unusually, as a DESIGNED one. EXPECTED DIRECTION on the segment: NULL (~50.0) on GATED, POSITIVE on SIEGE-ACTIVE.** ⛔ **AND THE GATE'S BEHAVIOUR ON THIS POOL IS COMPUTED AT DRAFT AGAINST V513'S OWN PREDICATE, NOT INHERITED FROM THE SIBLING PAGE:** the predicate and the skip set were `diff`ed against v512's and found unchanged, then re-evaluated from scratch over `maps/*.map26` for the 15 pool maps, giving GATED = {`antler` (d²=64), `archipelago` (signature `(26,26,(5,5),(19,19))` ∈ `FS_MAP_SKIP`), `fjordgate` (10×10 and d²=32)} and SIEGE-ACTIVE = the other twelve. **Note that only ONE of the three (`archipelago`) is gated by the `FS_MAP_SKIP` set; `antler` and `fjordgate` are refused by the dimension/distance gate the family has carried since v510.** Per-map cells at full n hold 360 games ⇒ half-width **±5.17pp**, so no single map cell can carry a verdict; at a 2,700-game combo stop a map cell holds 180 games ⇒ **±7.30pp**. Per-map, per-seat and CQ/STD/GRAND tables (`tools/overnight_read.py:76-94 map_area_class`) are computed and reported DESCRIPTIVELY and may not rescue a failed bar.
**PRIMARY SEGMENT: the GATED vs SIEGE-ACTIVE split, fixed BLIND at draft by evaluating the bot's own gate predicate against every map file — GATED = {`antler`, `archipelago`, `fjordgate`} (3 maps, 1,080 games at full n, half-width ±2.98pp; 540 games and ±4.22pp at a 2,700 stop); SIEGE-ACTIVE = {`auroraveil`, `drakkarfjord`, `drumlin`, `frostgate`, `glacierkeep`, `icefloe`, `midgard`, `nordkap`, `ragnarok`, `royale`, `valkyrie`, `yulerune`} (12 maps, 4,320 games, ±1.49pp; 2,160 games and ±2.11pp at a 2,700 stop).** ⭐ **THIS SEGMENT IS SHARD-NATIVE AND EXACT: the map is on the tape (`ts shard game map seed seat winner cond turns`) and the gate is a deterministic function of the map, so every row's segment is known without an instrument.** Registered prediction: **the GATED cells read 50.0 ± their own half-width (the plank is switched off there and the bot plays the incumbent chassis), and whatever the package does concentrates entirely on the SIEGE-ACTIVE end.** ⛔ **AND ON THIS ARM THAT PREDICTION IS DOING REAL WORK RATHER THAN DECORATING THE PAGE (§8): v513's non-siege diff against the control is FIVE TIMES the size of v512's on `eco.py` and TWICE on `main.py`, and two of its eight changes (C, the eco lifeline; H, the spawn sort) live on paths that run on EVERY map. If the gated segment moves, the pooled effect is partly chassis drift and not the siege package.** Exactly one primary; every other cut on this page is DESCRIPTIVE (OB15b).
**EXPECTED DIRECTION: POSITIVE on the SIEGE-ACTIVE segment (above 50.0, prior 54.44% from the arm's own grid); NULL (~50.0) on the GATED segment; therefore POSITIVE pooled, prior 53.56%.**
**SEGMENT VALUE CEILING: 80.0% × 64.63pp = 51.70pp** — the SIEGE-ACTIVE segment's maximum contribution to the pooled share. The pairing share is the shard's EXACT map composition (12 siege-active of 15, balanced by construction and verified on a completed tape of this fixture at every prefix); the on-segment figure is the **UPPER** 95% bound on the arm's own grid (49/90 = 54.44%, Wald × DEFF 0.98 ⇒ [44.26, 64.63], the D-pass's interval re-derived; the Wilson form gives [44.18, 64.34] and the choice moves the ceiling by 0.23pp). **The GATED complement contributes at most its structural null: 20.0% × 50.00 = 10.00pp. ⇒ POOLED CEILING 61.70pp**, comfortably above the 51.33 bar, above the 52.0 trend floor and above the 55.0 combo bar — **so unlike `RINGLADDER`, whose ceiling of 41.03 sat below its own catastrophe threshold, THIS ARM IS NOT EXCLUDED BY ITS OWN ARITHMETIC.** ⭐ **THE COMPANION FLOOR, computed the same way and reported beside it because a ceiling alone flatters: 0.80 × 44.26 + 10.00 = 45.41pp, which sits just ABOVE the 45.0 catastrophe line — which is why P(CATASTROPHE) is ≤0.04 at every scenario in the registered band except the map-pessimistic corner (§3).** ⇒ the dilution is a HARD CAP on what the gated fifth can contribute: **51.33 pooled needs 51.66% on the siege-active segment, 52.0 needs 52.50%, and 55.0 — the combo bar — needs 56.25%, which is ABOVE the grid's own point estimate.** ⛔⛔ **DECLARED LIMITATION OF THIS TOKEN, AND IT IS THE PAGE'S LARGEST: THIS INTERVAL IS PURELY A SAMPLING INTERVAL AND THE DOMINANT UNCERTAINTY IS COMPOSITIONAL.** The grid's five maps are now known (`run_grid.py:17`) and ELEVEN of the fifteen pool maps carry zero observation; of the four observed, ONE (`glacierkeep`) reads **18/18 = 100%** and one (`atoll`, 20% of grid rows) is RETIRED and never played by this shard. **Removing `glacierkeep` alone drops the grid to 31/72 = 43.06%.** The map-composition band computed in §2 runs **42.96 - 57.78 pooled**, which is WIDER than this sampling interval and centred lower. The ceiling is therefore a *ceiling under the assumption that the eight unmeasured siege-active maps behave like the four measured ones* — which is precisely the assumption this shard exists to test. **A single number cannot honestly express that, the band beside it is the honest expression, and inventing a narrower one would be worse than saying so.**
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page, and because the rotation is load-bearing HERE: if the build grid inherited the parent's five maps, two of them are pre-rotation geometry the shard never plays.)
**SPANS-POOL-CHANGE: no** — the shard is fired entirely after the 2026-08-13 rotation, on a single fixed 15-map pool.
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: four gates, sized separately.**
* **(a) THE SHARE BAR.** Margin 1.33pp against a one-sample half-width of ±1.334pp at n=5,400, DEFF 0.98 — resolvable at full n, and only just. ⚠ **The slack is ~0.00pp, which is `GUNAXABL`'s exact failure mode (missed its keep edge by 0.0152pp — ONE GAME — on a bar with zero constructed slack). Registered consequence: a result within one game of the bar is reported as "the fixture cannot resolve the question", not as a verdict in whichever direction the rounding falls.** At the COMBO-STOP carve-out's n=2,700 the half-width is ±1.886pp, so **Band 1 there requires a point of ≥ 53.22** and that threshold is registered in advance rather than computed after the stop.
* **(b) THE PRIMARY SEGMENT.** GATED cells at full n: ±2.98pp against a registered prediction of exactly 50.0 — resolves a gross discordance and cannot resolve a 3pp one. At a 2,700 stop the gated cells hold 540 rows ⇒ ±4.22pp; at a 1,000-game trend-floor stop ~202 rows ⇒ ±6.9pp — **does not resolve, defaults to the RESTRICTION.**
* **(c) THE r300 ADMISSION BAR — THE PRIMARY IS RMST₃₀₀ AND IT IS SIZED OFF THIS ARM'S OWN MEASURED sd, NOT A FAMILY ANCHOR.** RMST₃₀₀ MDE **+5.0 rounds** against a half-width of **±1.83 at n=5,400** and **±2.59 at n=2,700** (delta sd 68.66, measured from `scratchpad/v513_build/grid/*.tsv`); with the conservative family anchor (sd 89) the same figures are ±2.37 / ±3.36. **RESOLVES at both n, on either sd.** The co-bar, ITT timely-kill, MDE 3.0pp against ±2.01pp at 5,400 and ±2.84pp at 2,700. ⛔ **THE TIMELY-KILL FORM CLEARS BY ONLY 0.16pp AT 2,700 AND IS REGISTERED AS KNIFE-EDGE: if the sd recomputed from THIS tape exceeds the 75.28pp anchor by more than ~6%, that form does NOT resolve at 2,700 and defaults to the RESTRICTION — while RMST₃₀₀, the PRIMARY, still does. That test is performed at readout and its result is reported whichever way it lands.** ⭐ **THIS IS THE SHARP DIFFERENCE FROM `RINGLADDER`, whose modal stop at n=400 resolved neither form: this arm's modal stop at n=2,700 resolves its PRIMARY r300 bar comfortably.** At n=1,000 (±4.26 measured / ±5.52 anchor, and ±4.67pp) and n=400 (±6.73 / ±8.72, and ±7.38pp) neither resolves, and per OB12 the UNRESOLVED gate DEFAULTS TO THE RESTRICTION: no promotion, no ship conversation, no combination claim, regardless of what the share did.
* **(d) THE OPERATIONAL FLOORS, AND ON THIS ARM THEY ARE THE GATE THAT DECIDES ITS FATE.** The pinned `tools/auto_gate.py` marks CATASTROPHE (CI-hi < 45.0 at n≥400, `:823-836`, checked on the running tape rather than a pinned prefix), TREND-FLOOR@1000 (prefix < 52.0, `:895-906`), **COMBO-BAR@2700 (prefix < 55.0, `:919-967`) — WHICH BINDS, UNEXEMPTED, AND IS THIS SHARD'S MODAL TERMINATOR AT P ≈ 0.77 (the TREND FLOOR takes over as terminator anywhere below ~52 in the map-composition band)** — and FUTILITY-BAR@2700 with the s44 half-a-half-width margin (`:975-990`, which at this arm's prior never fires). The bar plausibility guard (`:398-406`, `[30,70]`) admits 51.33. Their firings are OPERATIONAL CANCELLATIONS that free a core, typed `cancellation`, never `verdict` — **with the single pre-committed COMBO-STOP carve-out under CUT-SHORT, which is a BAND licence at the registered floor and not a verdict-by-another-name.** **The floors bind REMOTE too (`a50f27ef`, s48), so the binding registration is SAME HOST — one box, 8 in-process workers; moving it to a second host is an amendment typed BEFORE the first row.**
**Everything else on this page (F1-F5, D3, D4, the seat / per-map / class splits) is DIAGNOSTIC and cannot rescue a failed bar. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## ⛔ NO COMBO-BAR EXEMPTION IS CLAIMED, AND THE REASONING IS THE MERITS, NOT THE CONSEQUENCE

`tools/auto_gate.py:919-946` defines the exemption for *"a MECHANISM test scored
against its own additive prediction"*, opted into by the literal token
`COMBO-BAR-EXEMPT` in the BARS source column, and it grants nothing unless the
token cites a prereg `.md` **that exists** (`:930-957` — a broken citation is
louder than no exemption at all). **This page DOES NOT claim it, and
`COMBO_BAR = 55.0` BINDS on the n=2,700 prefix.** Three reasons, each
sufficient — and the fourth paragraph says plainly what that costs:

1. **THIS TREE IS A GENUINE COMBINATION ON THE MERITS, AND MORE SO THAN ITS
   PARENT WAS.** Against this control it differs in **all four shared modules**
   (`doctrine.py` 758 diff lines, `main.py` 567, `eco.py` 75, `raid.py` 28)
   **plus an entire 2,391-line module that does not exist in the control**, and
   it stacks **thirteen mechanisms** — v512's five plus v513's eight. The
   `BELTBREAK` solo grants (`docs/prereg/BARS.tsv:310,312`) rest on *"this arm
   is a SOLO plank … not a combination"* and **that sentence is not remotely
   true here.**
2. **NO ADDITIVE PREDICTION EXISTS TO SCORE AGAINST.** The exemption's
   registered purpose is a mechanism test that can sit ON its own registered
   target and still read under 55. **This arm has registered no additive
   target** — its grid predicts 54.44% and its composition prior 53.56%, both
   of which are ORDINARY SHARE PREDICTIONS, not additive decompositions of
   component effects. **A token whose premise is absent grants nothing.**
3. **THE COMPOSE MARKER IS PRESENT AND IS NOT THE REASON.**
   `bots/_v513siegecrew/doctrine.py:2078` carries the literal
   `# ---- composed by tools/stack.py from: turbo (_x3r0v152), bodyaware
   (_v242bodyaware), samestop (_v464samestop)` inherited from the chassis, so
   `combo_of()` (`auto_gate.py:723-748`) will classify this arm COMBO
   regardless. **The inherited-marker classification defect is real; this arm
   would read COMBO on the merits anyway,** which is why the defect changes
   nothing here.

⛔⛔ **AND UNLIKE `RINGLADDER`, THIS CALL IS NOT MOOT — IT IS THE MOST
CONSEQUENTIAL DECISION ON THE PAGE, AND IT IS SAID PLAINLY RATHER THAN LEFT IN
A FOOTNOTE.** `RINGLADDER` could refuse the exemption for free because it was
never going to reach 2,700. **This arm's whole plausible range (45.41 - 61.70 sampling,
42.96 - 57.78 map-composition;
prior 53.56) straddles the combo bar, and the band the bar kills — [51.33,
55.00] — is exactly the band the page predicts.** The consequence is priced in
§3: **P(cancelled at COMBO-BAR@2700) ≈ 0.77 at the prior, and the shard is
therefore ~11× more likely to be stopped by the combo bar than to complete.**
The COMBO-STOP carve-out under CUT-SHORT is the honest mitigation — it converts
that stop into a readable n=2,700 band with a 0.13pp selection — **and it is a
mitigation, not a repair: a 2,700-game read cannot deliver the ±1.33pp
precision the 5,400 plan was sized for.** **An escalation to Magnus is
available to the builder and is RATIFICATION BLOCKER B1; a self-granted token
is not, and an escalation would have to argue the opposite of point 1.**

---

## ⛔ RATIFICATION BLOCKERS — FIVE THINGS THE BUILDER MUST SETTLE BEFORE LOCKING

**B1. ⛔⛔ RULE ON THE COMBO BAR, IN WRITING — THIS IS THE ONE THAT DECIDES
WHETHER THE SHARD CAN ANSWER ITS OWN QUESTION.** The arm's prior (53.56) sits
inside the band the 55.0 combo bar kills, and P(stop) ≈ 0.77 (§3). **Four
defensible branches:** (i) **fire unexempted as drafted**, accepting a ~77%
chance of a 2,700-game cancellation and relying on the COMBO-STOP carve-out to
make that outcome readable — the drafter's registration, and the one that needs
no argument; (ii) **escalate to Magnus** for a case-specific ruling, since the
combo bar is his (2026-08-16) and this is the first arm in this family whose
prior lands in its kill band with a passing decision bar; (iii) **re-register
the shard at n=2,700** and treat 2,700 as the plan rather than the floor —
honest, cheap, and it gives up the ±1.33pp precision; (iv) **claim
`COMBO-BAR-EXEMPT`** — **the drafter judges this NOT available on the merits**
(three reasons above) and records it only so the branch is enumerated rather
than silently unavailable. **Firing without choosing is not a branch.**
*(Drafter's recommendation, offered and not decided: (i), with the carve-out as
drafted, plus a one-line note to Magnus at readout that the combo bar killed an
arm predicted to clear its decision bar — that is exactly the kind of
instrument fact he has asked to see.)*

**B2. ⭐ DISCHARGED AT DRAFT — RETAINED AS THE RECORD OF WHAT WAS CHECKED.**
This blocker asked the builder to name the build grid's five maps, because the
build report does not and the cited scratchpad was in a dead session's
`/private/tmp` (the D-pass's F3). **The artifacts were banked into the repo at
`scratchpad/v513_build/` before this draft was finished, so the list was read
rather than asked for: `run_grid.py:17` gives `glacierkeep · nordkap · atoll ·
midgard · drakkarfjord`, and `run_grid.py:16` independently confirms
`OPP = bots/_v488beltbreak2`.** The consequences are folded into §2 (the
per-map decomposition and the map-composition band), §4 (eleven pool maps carry
zero observation; `atoll` is retired) and the SEGMENT VALUE CEILING's declared
limitation. **The builder need only confirm the reading.** ⚠ **AND ONE
RESIDUAL: the artifact directory is now the sole reproduction path for
49/90, so it must stay tracked — the D-pass's F3 was that nothing in the repo
could reproduce the day's largest iteration.**

**B3. THE DEFERRED FLAG-OFF EQUIVALENCE OBLIGATION (§DEFERRED OBLIGATION SLOT).**
The side lane attached a standing obligation to *any future ferry-siege-family
prereg*: full deterministic flag-off equivalence for v510/v511/v512
(`docs/coordination.md:71346`, s50 wrap open item 4 — spot-checks only so far,
builder-declared). **A `tools/det.py` run is in flight (Agent D, artifacts to
`scratchpad/s51_det/`, three pair directories present at draft and empty of
results). The section below carries an explicit placeholder and the drafting
agent has invented nothing.** The builder fills it at ratification, before the
lock commit.

**B4. CONFIRM SAME-HOST, THE WORKER COUNT, AND THAT `gate_watch` IS LIVE.** The
registration is LOCAL, SAME-HOST, **8 in-process workers on one box** — stated
explicitly because both sibling preregs registered *"one worker"* while their
tapes read `workers=8`, and this page does not repeat that divergence.
**What is NOT pre-registered and must be is whether a SECOND HOST may be added
mid-run** — it may not, without an amendment typed before the first row
(Addendum 11 rider: the 0.98 exemption is a WITHIN-HOST measurement).
**AND: confirm the gate watcher actually polls this shard.** Every probability
in §3 is a plan and not a mechanism until it does, and on this arm the gate is
what bounds the core spend.

---

**B5. ⛔⛔ NEW, AND IT IS A SCOPE QUESTION RATHER THAN A STATISTICAL ONE: THE
FIRED TREE SHIPS A HOME-DOCTRINE CHANGE WHOSE MAGNUS APPROVAL IS
NOT-ESTABLISHED.** The side lane's D-pass ranks this **F1, top**:
`doctrine.py:2653` `FS_HOME_TURRET_RESPONSE = True` is **live in the fired
config** (gated at `main.py:1097` on `LOKI_FS_CREW and
FS_HOME_TURRET_RESPONSE`, and `LOKI_FS_CREW = True`), while the builder's own
record at `docs/coordination.md` 2026-08-17T20:32:18Z says the door-sentinel
response *"needs Magnus's nod (home doctrine)"*; six minutes later it is
re-labelled *"flag-gated [my recommendation, executed under the
run-with-recommendations standing directive]"*, and the 21:34:47Z landing note
names only TWO Magnus decisions parked for morning (second body,
sentinel-after-salt) — **the door response is not among them.** The code
self-describes as `main.py:1088` *"⭐ THIS DELIBERATELY PIERCES
LOKI_QUIET_ON"*. **No approval record exists either way.**
⇒ **THIS IS NOT A REASON TO CHANGE THE TREE and this agent proposes no flag
flip** — change B answers the autopsy's #1 measured cost and turning it off
would fire a different package than the one measured at 54.4%. **It IS a reason
the builder must decide, in writing, before the lock:** (i) fire as-is and
record that Magnus's nod is outstanding on a clause inside a screened package;
(ii) get the nod first; (iii) fire as-is and route the question to the morning
decisions list alongside the other two. **Firing without recording the state is
the branch this blocker exists to prevent.** *(Drafter's recommendation: (iii)
— the local shard commits nothing to the ladder, lock-in forbids a ship
tonight, and the decision Magnus actually owns is whether it ever leaves the
local fixture.)*

## ⭐ DEFERRED OBLIGATION SLOT — FLAG-OFF EQUIVALENCE

**THE OBLIGATION, quoted rather than paraphrased** (`docs/coordination.md:71346`,
side lane s50 wrap, open item 4): *"Deferred obligation attached to any future
ferry-siege-family prereg: full deterministic flag-off equivalence for
v510/v511/v512 (spot-checks only so far, builder-declared)."* **This is that
prereg.** The obligation exists because the family's structural-equivalence
claims — *"`LOKI_FERRY_SIEGE_ON = False` reproduces `_v488beltbreak2` exactly"*
(`doctrine.py:2152`), *"`LOKI_FS_SEAL_ONLY = False` reproduces
`_v510ferrysiege` exactly"* (`:2189`), *"`LOKI_FS_RING_LADDER = False`
reproduces `_v511sealonly` exactly"* (`:2251`) — are **comments, and comments
are not measurements.** Every gated-map argument on this page and both sibling
pages leans on them.

**FILLED AT RATIFICATION (builder s51, Agent D complete): ALL THREE PAIRS
EQUIVALENT — the family's structural-equivalence comments are now MEASUREMENTS.**
Method: `tools/det.py`, canonical trees untouched (git-clean throughout), edits
in scratchpad copies only; `NOISE_ON=False` both sides per pair; opponent
`bots/opp_v63` (determinism_report clean); n=400 paired deterministic games per
pair (25 maps × 8 distinct seeds × 2 seats).
* Pair 1 `_v488beltbreak2` vs `_v510ferrysiege` flag-off (`LOKI_FERRY_SIEGE_ON`
  doctrine.py:2152 True→False): **0 flips, 400/400 identical end-states.**
* Pair 2 `_v510ferrysiege` vs `_v511sealonly` flag-off (`LOKI_FS_SEAL_ONLY`
  :2189): **0 flips, 400/400.**
* Pair 3 `_v511sealonly` vs `_v512ringladder` flag-off (`LOKI_FS_RING_LADDER`
  :2251): **0 flips, 400/400.**
POSITIVE CONTROL (instrument driven to the other verdict): pair-1 parent vs the
SAME child copy with the flag left True, n=24 — **24/24 NON-identical end-states.**
⚠ Disclosed caveat: the positive control ran once on pair 1's mechanism and is
shared by pairs 2/3, not re-run per pair. det.py's `LOW REPLICATION` warning
(DISTINCT paired shapes 84/73/71 of 400) concerns effect-size reads off
seed-collapsed NOISE_OFF games and does not touch the identity verdict; win
rates were equal and non-degenerate per pair (97.8/94.0/95.2%, both sides).
Artifacts: `scratchpad/s51_det/pair{1_v510,2_v511,3_v512}.json`,
`pair1_control.json`, matching `.log`s and copy trees. **No instrument alarm;
the gated-map argument's inheritance chain is measured end-to-end.**

⭐ **ONE PIECE OF THE OBLIGATION'S CONTEXT IS ALREADY DISCHARGED, AND IT WAS THE
SIDE LANE'S OWN TOP-THREE FLAG: the family's evidence base is now IN-REPO.** The
D-pass's **F3** recorded that the entire v513 build lived in a foreign session's
`/private/tmp` and that *"nothing in the repo reproduces 49/90"*. It has since
been banked at **`scratchpad/v513_build/`** (28 TSVs plus `run_grid.py`,
`mutants.py`, `tally.py`, `tally2.py`, `demorun.py`, the `smoke/`, `mut/`,
`mutf/`, `inst/`, `kill60/`, `diagC/`, `diagF/` and `probe_store` trees). **Every
number this page computes from the grid — the per-map decomposition, the
map-composition band, the RMST₃₀₀ pair, the ITT timely-kill pair — was derived
at draft FROM THOSE FILES rather than quoted from the report, which is the whole
point of banking them.**

**⭐ WHAT IS ALREADY KNOWN ABOUT V513'S OWN FLAG-OFF STATUS, banked here so the
placeholder is not carrying the whole section.** `LOKI_FS_CREW` is the master
flag for the v513 layer (`doctrine.py:2594`, *"False reproduces
`_v512ringladder` exactly"*), and the build report verifies it **two ways,
neither of which is byte identity — and it says why:**
* ⛔ **BYTE-IDENTICAL OUTCOME COMPARISON IS IMPOSSIBLE UNDER `NOISE_ON`** (the
  s50 one-draw law: an unseeded spawn salt makes a local game one draw). **This
  is a structural limit on the obligation itself, not a shortfall by this
  build**, and it is the reason `det.py` must run its pairs under a
  deterministic regime rather than on ship-config games.
* **STRUCTURALLY:** every new branch sits behind `LOKI_FS_CREW`, and with it
  False, `_eco_spendable`, `_l4_repair`, `_build_next_link`,
  `_fs_stand_target`, `_fs_threat_tiles`, `_fs_try_retreat`, `_fs_salt_ok`,
  `_fs_try_evict_launcher`, `_raid_seat_take` and every core clause **reduce to
  the parent's expressions.**
* **BEHAVIOURALLY:** n=60 paired on the parent's own seeds — flag-off **12 wins
  / 44 core deaths / 27 tic-zero** against v512's **9 / 46 / 30**, inside the
  documented same-bot swing.
⚠ **BOTH ARE EVIDENCE AND NEITHER IS PROOF**, and the page does not upgrade
them. **The v513 pair is NOT part of the deferred obligation as written** (which
names v510/v511/v512) and is recorded here so the successor does not have to
re-derive whether it was ever checked.

---

## FIRINGS-BEFORE-PRIMARY — READ AND WRITTEN DOWN BEFORE THE PRIMARY IS TYPED

⛔ **THE RULE IS A HARD SEQUENCE** (`docs/prereg/BARS.tsv` header, research
2026-08-16T13:27:33Z): **F1-F5 are read, and their numbers written down, BEFORE
any sentence containing this arm's primary share is typed.** A primary typed
ahead of the firings read is a REGISTRATION BREACH regardless of what it says,
and the repair is an amendment chain, not a re-write. *(Precedent:
`results.tsv:kladladder-verdict-amendment-f1f2-pending`.)*

⛔ **THE SHARD ITSELF CAN SEE EXACTLY ONE OF THE FIVE, AND THE OTHER FOUR ARE
NAMED WITH THEIR ALARM PROXIES RATHER THAN ASSUMED CLEAN.**
`tools/overnight.sh:138-139` runs every game with `--replay /dev/null`, the
tape's columns are `ts shard game map seed seat winner cond turns`, the runner
greps `Winner:` out of a merged `2>&1` capture and discards the rest, and the
fired config has `FS_LOG = False` — **so no entity, build, position, shot,
turret, store or stderr information survives, in either arm.** ⛔ **AND THE
`cond` COLUMN IS THINNER THAN IT LOOKS: checked at draft on two completed tapes
of this fixture, it takes exactly TWO values — `core_destroyed` and `tiebreak`
(RINGLADDER 405/54; BELTBREAK2 4,791/609). It does NOT carry the tiebreak KEY,
so `titanium_collected = 0` — change C's entire defect — is NOT recoverable from
the shard by any route.** That is `RINGLADDER`'s F4 lesson applied before the
fact rather than after it.

* **F1 — THE MAP GATE AND THE POOL COMPOSITION. SHARD-NATIVE AND EXACT.**
  Computed at draft by evaluating the bot's own predicate
  (`siege.py:254-300`) against `maps/*.map26`: **GATED 3 of 15** — `antler`
  (d²=64 < 72), `archipelago` (signature `(26,26,(5,5),(19,19))` ∈
  `FS_MAP_SKIP`), `fjordgate` (10×10 < 12 **and** d²=32 < 72) — **SIEGE-ACTIVE
  12 of 15**, and the predicate/skip-set were `diff`ed against v512's and found
  unchanged. **Balance verified on a real completed tape of this fixture:
  gated share 20.50% / 20.20% / 20.00% / 20.00% at the 400 / 1,000 / 2,700 /
  5,400 prefixes of `scratchpad/overnight/BELTBREAK2.tsv`, seats exactly 50/50
  at all four.** Read: **the plank is switched off on exactly 20% of this
  shard's rows and that is SHIP BEHAVIOUR, not a fixture defect.**
  **A readout that omits the per-segment table has not performed F1.**
* **F2 — MAGNUS'S SALT GATE, DRIVEN BOTH WAYS. 0 pre-seal sentinels ON vs 14
  (`salt_off`) and 10 (`crewflag_off`).** The rule Magnus gave directly
  (`docs/coordination.md:71294`) and the change the autopsy's 1:1 heal-cancel
  finding demanded. Read: **the gate holds and it is not a blind zero — the same
  binary with the flag flipped produces the behaviour.** ⛔ **NOT re-readable on
  the shard** (a sentinel build is invisible without a replay). **ALARM PROXY:
  none exists for this one, and the page says so rather than inventing one** —
  if the gate had silently stopped firing, the shard would show it only as a
  share change, which is the thing under test. **This is the F-read whose
  failure would be least visible, and it is therefore the one whose pre-lock
  provenance matters most.**
* **F3 — THE DOOR-TURRET RESPONSE, DRIVEN BOTH WAYS AGAINST A MEASURED ZERO
  BASELINE. 152 pecks at n=15 and a door turret attacked in 11 of 30 logged
  games, against 0 (`door_off`) and 0 (`crewflag_off`) — and 0 of 40 plants ever
  attacked in v512** (autopsy cause #1, which carried 100% of the 1,202 damage
  events on our core). Read: **the #1 measured killer is now contested at all.**
  ⛔ **NOT re-readable on the shard.** **ALARM PROXY: our own core-death rate.**
  The grid reads our core destroyed in **39/90 (43.3%)** against v512's
  **68/90 (75.6%)**; on the shard the complement of the treatment share plus the
  `cond` mix bounds it. **A treatment share whose losses are overwhelmingly
  `core_destroyed` at a rate near v512's is an INSTRUMENT ALARM, not a finding.**
* **F4 — THE BELT LAST LINK. `titanium_collected = 0` in 1/15 ON, against 5/15
  (`belt_off`) and 9/15 (`crewflag_off`); 4/90 (4.4%) at the outcome grid
  against the parent's 46/90 (51.1%).** The defect had **perfect 24/24
  separation** in the autopsy (core-adjacent conveyor ⟺ tic > 0) and its root
  cause was two of our own reserves deadlocked exactly 6 Ti apart. Read: **the
  economy connects.** ⛔ **NOT re-readable on the shard, and NOT EVEN VIA `cond`**
  — the tape's `cond` is binary (`core_destroyed` / `tiebreak`) and carries no
  tiebreak key, so a key-1 double-zero is invisible. **ALARM PROXY: the r1000
  share.** A belt that stops short produces long games; the grid reads r1000 at
  **10/90 = 11.1% [6.15, 19.26]** and the control's completed tape at **11.28%**.
  **STOP RULE: a treatment r1000 share materially above ~19% is an INSTRUMENT
  ALARM — the tape is inspected before any share sentence is written.**
* **F5 — THE CRASH INVARIANT. 0 tracebacks across every grid row and every
  mechanism/demo game, on a tree that adds 2,391 lines of `siege.py` and 758
  lines of `doctrine.py`, including a new store-word layout.** ⚠ **DENOMINATOR
  CORRECTED FROM THE REPORT (D-pass F9b): the report says "670 grid + 165"; the
  grid TSVs actually hold 730 rows, all with `tracebacks = 0`, so the report's
  claim is CONSERVATIVE and its denominator is wrong. The corrected read is 730
  grid rows + 165 mechanism/demo, 0 tracebacks, with 296 `.err` files
  grepped.** An escaping exception permanently destroys that unit for the rest
  of the match (`0x1ac5c` → `Game::destroy_entity`), and **v513's own build
  probed a NEW way to trigger one: a store slot is an unsigned 32-bit integer,
  so a negative or oversized write raises `OverflowError`**
  (`scratchpad/v513_build/probe_store`, six values, both verdicts present).
  Every field written by `_fs_crew_publish` is masked to its width first.
  ⛔⛔ **AND THE NEAR-MISS IS RECORDED HERE BECAUSE THE BUILD REPORT OMITS IT
  (D-pass F9b): a real `Traceback` DOES exist in the build's own smoke output —
  `scratchpad/v513_build/smoke/i_nordkap.err`, `NameError: name 'sys' is not
  defined` at `main.py:557`, inside the `FS_MAG_TRACE` print. It is FIXED in the
  shipped tree (`import sys` at `main.py:32`, `FS_MAG_TRACE = False` at
  `doctrine.py:2781`) and could only fire under a local instrument flag, so
  there is NO LIVE HAZARD in the fired config — but a `NameError` in `_core`
  would have permanently destroyed OUR CORE, and "0 tracebacks" is a claim about
  the shipped tree and not about the build.** ⛔ **NOT measurable on the shard —
  registered as such rather than assumed clean:** stderr is discarded, so a
  destroyed unit is invisible except as an anomalous r1000 spike or a
  `NOWINNER` row. **STOP RULE: any `NOWINNER` row (both sibling tapes carry 0),
  or the F4 r1000 alarm, halts the readout for a tape inspection.**

**NOT MEASURABLE on this leg — named, not silently dropped.**
* **FERRY ARRIVALS, THROWS, SEALS, EVICTIONS, SENTINEL BUILDS, DOOR PECKS,
  BELT LINKS, RETREATS, DODGES, SPAWN PLACEMENTS AND CLOSURES ARE NOT DECODABLE
  OFF THE SHARD** (`--replay /dev/null`; local corefill keeps TAPES, not
  REPLAYS; stderr discarded; `FS_LOG = False` in the fired config).
* **THE THIRTEEN MECHANISMS CANNOT BE SEPARATED ON THIS LEG** (§5). No amount of
  tape reading recovers a decomposition the design does not contain. In
  particular **the v513 layer cannot be separated from the v512 layer** — that
  is `_v513siegecrew` vs `_v512ringladder` and is not being run.
* **PER-UNIT CPU / TLE.** Blind zero locally (`get_cpu_time_elapsed()` is a
  stub; 0 across 200,633 `BotOutput` events; local replays carry no exec-time
  fields) — labelled **UNINFORMATIVE, NOT CLEAN**, and it is exactly the
  dimension the build report's open item 3 flags for change B's per-round scan.
* **ANYTHING ABOUT THE FIELD.** The opponent is our own chassis. `CLAUDE.md`
  rule 6: **this page closes no road.**

**D3, D4 — the outcome-shape reads. MEASURABLE, shard-native** (`cond` and
`turns` are on the tape): **D3** = the r300 admission bar, both forms, per side,
off `tools/cluster_ci.py --null`, read with the zero-sum disclosure and the
resolution statement under GATE RESOLUTION (c); **D4** = `cond` mix per arm, the
treatment's own median kill round (crossing 300 is disqualifying, and the grid
median is 281), and **the mandatory r1000/core-kill split of the share** that
the THIRD FALSIFIER is denominated in. Anchors: `results.tsv:beltbreak2-final`
timely-kill **30.80% [29.56, 32.03]**, r1000 share **11.28%**; build grid
kills ≤ r300 **24/90 = 26.67%**, r1000 **10/90 = 11.11%**, median kill 281.

---

## ⚠ THE LYING-FIXTURE CAVEAT — CARRIED VERBATIM AS AN INTERPRETIVE CONSTRAINT ON THIS WHOLE PAGE

**THIS CONTROL IS A FIXTURE WE WROTE, AND ON THE DIMENSIONS THIS PACKAGE
ATTACKS IT IS MEASURABLY UNLIKE THE FIELD.** The package's currency is the enemy
core's collar — whether the defender's heal seats can be sealed and held — and,
new in v513, whether the defender's forward turret at OUR door gets pecked down.
**Local incumbent defence and field defence are not the same problem:** the
field's sealers close the ring at rates the research survey measured down to a
HARD ZERO on some geometry (`lighthouse`: **0 of 347 observed closures**), and
the field's overall clearance of this class of pressure sits at **8.6%**, which
is why `FS_MAP_SKIP` exists at all. **Our own incumbent is a different defender
with different reflexes, and every number on this page is measured against it.**
⛔ **AND ON THIS ARM THE CAVEAT BITES HARDER IN ONE SPECIFIC PLACE: change B is
a response to a behaviour our own incumbent exhibits** (planting sentinels at
our door — 40 plants in 24 games). **A field opponent that does not plant door
turrets gives change B nothing to do, and a field opponent that plants them
differently gives it a different problem.** The 54.4% grid read is partly a read
of how well we counter OURSELVES.
⇒ **NOTHING ON THIS PAGE — pass, fail, or cancellation — TRANSFERS TO THE
LADDER WITHOUT A LIVE LEG.** A Band-1 reading does not establish that the crew
package beats real opponents; it establishes that it beats
`bots/_v488beltbreak2`. **`CLAUDE.md` rule 6 governs: a refutation without
live-game backing is a hypothesis, not a refutation, and this leg has no
live-game backing by construction.** ⚠ **AND THE LIVE LEG IS NOT AVAILABLE
TONIGHT: the session is under LOCK-IN** (no submits, activations or unrated
fires by any lane until Magnus reopens; `FIXTURE_OF_RECORD: live_unrated`
remains the programme's fixture of record and this shard is not it). **A pass
here buys a place in the queue for that leg. It buys nothing else.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on this arm's pooled
share vs `bots/_v488beltbreak2` falls BELOW 51.33.** That excludes the arm's own
bar on the fixture whose null is structural. ⭐ **THIS PAGE PREDICTS IT DOES NOT
FIRE** — the composition prior is 53.56 and the sampling ceiling 61.70 — **which is
precisely why the leg is worth a core: the sibling arm's page predicted its own
falsifier and was right, and a family that only ever fires arms it expects to
fail is not iterating.**

**SECOND FALSIFIER (the r300 admission bar, and it can fail alone while the
share passes):** the 95% CI UPPER bound on (treatment − control) ITT RMST₃₀₀
fails to EXCLUDE +5.0 rounds, **or** the CI LOWER bound on the ITT
timely-kill-by-r300 difference fails to EXCLUDE a fall of 3.0pp. **Either is
disqualifying on its own, regardless of the share** — `PLAY_DEFENCE:
not_at_the_kill_s_expense`, and a collar siege is a mechanism that spends
rounds. ⛔ **AND ON THIS ARM IT IS THE FALSIFIER MOST LIKELY TO FIRE AND THE
LEAST WELL PRICED PRE-FIRE** (the build report gives the treatment's timely-kill
rate and the parent's but never the paired control's; the treatment's median
kill round rose 241 → 281). Read with the zero-sum disclosure attached to the
bar, and with the resolution statement: **both forms resolve at n=5,400 and at
the 2,700 carve-out (timely-kill by 0.16pp, hence KNIFE-EDGE); at any stop below
2,700 this falsifier is UNRESOLVED, which under OB12 defaults to the RESTRICTION
and not to a pass.**

**THIRD FALSIFIER (the doctrine composition):** the share gain over 50.00 is
**majority r1000 tiebreak wins**. Then the reading is downgraded one band and
labelled `OFF-DOCTRINE COMPOSITION` — combination input only, no ship
conversation, no head-to-head. **Registered as a falsifier and not a caveat
because this plank's mechanism IS a long hold**, and because `R1000_IS_DEFEAT:
yes` means a share bought that way is not a win. ⭐ **The arm's own grid gives
this falsifier real teeth and also a defence: r1000 games are 10/90 (11.1%),
BARELY above the parent's 9/90 and the control's own 11.28% — so the package is
NOT, at n=90, buying its wins with long games. If the shard says otherwise at
n=2,700+, that is a genuine reversal and is reported as one.**

**SEGMENT FALSIFIER:** **the GATED segment (`antler`, `archipelago`,
`fjordgate`; 1,080 games at full n) must read 50.0 ± its own half-width
(±2.98pp; ±4.22pp at a 2,700 stop).** The plank is switched OFF there, so a
gated segment far from 50 means the treatment's NON-siege chassis differs from
the control in a way this page has not accounted for (§8 — the equivalence is
flag-and-state conditioned, not byte-verified, and v513's non-siege diff is
several times v512's). **If the gated segment moves while the siege-active
segment does not, the pooled effect is not coming from the mechanism this page
describes and the reading is ATTRIBUTION UNRESOLVED — promotes nothing, and
refutes nothing, EVEN IF THE BAR CLEARS.** ⚠ **Its power is declared: at
±2.98pp it catches a gross discordance and cannot resolve a 3pp one; below
n=2,700 it resolves nothing at all** (OB12; the unresolved case defaults to the
restriction). ⛔ **AND IT IS THE ONE FALSIFIER ON THIS PAGE WITH NO PRE-LOCK
EVIDENCE WHATSOEVER: all three gated maps carry zero observation of this tree
(§4), so unlike `RINGLADDER` — which at least had a gated cell reading 10/12 to
argue about — this page has nothing at all and says so.**

**MECHANISM FALSIFIER (independent of all of the above, and it fires FIRST):**
* if **F1**'s per-segment table shows the gated maps behaving like siege maps
  (or vice versa), the gate is not doing what the page says and the primary
  reads **NOT MEASURED**, never null;
* if **F4**'s or **F5**'s stop rule trips — any `NOWINNER` row, or a treatment
  r1000 share materially above ~19% — the tape is inspected for silent unit
  destruction and belt failure **before any share sentence is written**;
* if **F3**'s alarm proxy trips — losses overwhelmingly `core_destroyed` at a
  rate near v512's 75.6% — the door response is suspected inert and the primary
  is reported with that suspicion attached;
* ⛔ **F2, F3, F4 and F5 cannot be re-read on this leg. If any is later found to
  have been wrong at lock, this shard measured a tree nobody characterised and
  its number is retracted, not reinterpreted.**

### ⭐ THE HONEST-NULL CLAUSE — pre-committed, because the MODAL outcome is one of these

| state | evidence | pre-committed reading |
|---|---|---|
| **(1) STOPPED BY `COMBO-BAR@2700`** | prefix@2700 < 55.0 | ⭐⭐ **THIS IS THE PREDICTED BRANCH AT P ≈ 0.77 AND IT IS READABLE, NOT A WRITE-OFF.** Typed `cancellation`; rows KEPT; **the COMBO-STOP carve-out under CUT-SHORT licenses a BAND reading at n=2,700** (±1.886pp; Band 1 needs a point ≥ 53.22) with the selection disclosed **as selected-pessimistic AND SIZED at 0.13-0.45pp**, not at the family's generic +2pp. The r300 bar resolves here (timely-kill knife-edge) and the segment falsifier does not. ⛔ **What it CANNOT deliver is the ±1.33pp precision the 5,400 plan was sized for, and the readout says so in the same sentence as the number.** |
| **(2) STOPPED BY `TREND-FLOOR@1000` OR `CATASTROPHE@400`** | prefix@1000 < 52.0, or CI-hi < 45.0 at n≥400 | **CANCELLED — UNRESOLVED, defaults to the RESTRICTION.** Rows KEPT; partial disclosed selected-pessimistic (~+2pp, a DIRECTION not a correction). ⭐ **And it is a genuine surprise if it happens: P ≤ 0.16 at the prior, and it would mean the grid's 54.4% did not survive contact with the twelve unmeasured maps — which is itself the most informative thing this leg could report.** |
| **(3) COMPLETED, BAR CLEARS (CI lower ≥ 51.33)** | n=5,400 | ⭐ **THE FIRST FERRY-SIEGE ARM TO BEAT THE CHASSIS IT SITS ON, at full power.** Promotes the STACK, not any change (§5). Next steps in order: clause isolation vs `_v512ringladder`, a CPU `match test` on the platform (open item 3), and only then — after lock-in reopens — a LIVE unrated leg, which is the only fixture that can price it against the field. |
| **(4) COMPLETED, SHARE FLAT OR NEGATIVE** | n=5,400, CI contains or sits below 50 | ⭐ **A REAL FINDING AND A COSTLY ONE: the n=90 grid did not replicate at n=5,400.** It would make the 54.4% a small-sample artefact of an unnamed five-map subset, and it would put the family's whole autopsy-driven iteration in question. **Attribution bound: it does NOT refute the autopsy's measured causes (the 0/40 door plants, the 24/24 belt separation, the 1:1 heal cancel are facts about v512), and it does NOT price anything against the field.** |
| **(5) COMPLETED, BAR CLEARS, GAIN IS MAJORITY r1000** | decomposition majority tiebreak | ⭐ **`OFF-DOCTRINE COMPOSITION`, downgraded one band, combination input only.** The package delivered SURVIVAL, not KILLING. **Pre-registered as UNLIKELY on this arm** (grid r1000 11.1% vs control 11.28%), which is exactly what makes it informative if it happens. |

---

## READING, PRE-COMMITTED

**Read TOP-DOWN; the first row whose condition holds is the reading. Rows are
disjoint by construction. Every band is CONDITIONAL on F1-F5 having been read
and written down first, on the r300 admission bar having HELD (or being recorded
UNRESOLVED, which blocks promotion), and on the r1000/core-kill decomposition
having been computed. An r300 failure overrides every row
(`OFF-PROGRAMME — kill delayed`, whatever the share). A majority-r1000
composition DOWNGRADES the row by one and appends `OFF-DOCTRINE COMPOSITION`. A
gated-segment discordance appends `ATTRIBUTION UNRESOLVED` and blocks promotion
in every row. At a COMBO stop, every band is read at the n=2,700 half-width
(±1.886pp) and the selected-pessimistic disclosure is attached with its size.**

| # | band on the pooled share vs `bots/_v488beltbreak2` | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE CREW PACKAGE BEATS THE INCUMBENT — THE FAMILY'S FIRST POWERED WIN.** **PROMOTES THE PACKAGE, NOT ANY ONE CHANGE** (§5): the next step is clause isolation `_v513siegecrew` vs `_v512ringladder`, then a platform CPU `match test` (open item 3), then — post-lock-in — a LIVE unrated leg (the lying-fixture caveat), and only then a ship conversation. Report the size with its OB16 status: the BAR's MDE is 0; clearing this BAND excludes 50.00 AND 51.33, so an implied minimum effect of +1.33pp may be claimed and nothing larger. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Pre-registered as WEAK: `NULL125`'s A/A read 51.04 and the two A/A cells are 1.77pp apart. Rows KEPT; no ship conversation; a replication on fresh seeds, same host, is the price of promoting it — **reported SEPARATELY and never pooled** (GUNAXABL/SENTTHR precedent: unregistered pooling is optional stopping with extra steps). ⚠ **At a COMBO stop this is the LIKELIEST row**, since Band 1 there needs a point ≥ 53.22. |
| **3** | **point < 51.33 AND CI contains 50.0** | **PARITY — THE PACKAGE IS FREE.** Thirteen mechanisms and a 2,391-line module pay for themselves and nothing more. ⭐ **Against the parent's completed 25.00 [21.01, 28.99] (`results.tsv:ringladder-final`) that is a very large UPWARD move and must be reported as such** — with the caveat that ringladder-final is a cancelled n=452 partial on the same control and pool, so the comparison is directional and is not a registered estimand. Does NOT license a ship. |
| **4** | **CI upper < 50.0 AND CI upper ≥ 45.0** | **THE PACKAGE SUBTRACTS ON OUR OWN CHASSIS AND THE GRID DID NOT REPLICATE.** Attribution bounded: this refutes *the thirteen-mechanism crew package at this configuration on this map pool against this control*, **not** the autopsy's measured causes, **not** any single change, and **not** anything about the field. ⛔ **REGISTERED CONSEQUENCE: the first suspect is the twelve unmeasured maps, not the changes** — the honest next arm is a per-segment re-screen (OB15c: a NEW leg with its own n, never a re-read of these rows). |
| **5** | **CI upper < 45.0** | **A LARGE NET NEGATIVE, AND AN INSTRUMENT QUESTION BEFORE A PLANK QUESTION.** The composition FLOOR from the arm's own SAMPLING interval is 45.41 (§2), so this band sits below the pessimistic edge of the grid's sampling range — though NOT below its map-composition band, whose pessimistic corner is 42.96 (§2), so a Band-5 reading is compositionally reachable and the page says so. **The FIRST question at readout is whether F1's gate is doing what the page says and whether F5's crash invariant held** — not what the plank did. ⛔ **A Band-5 reading does NOT retire ferry-siege** (`CLAUDE.md` rule 6, and this fixture is our own chassis); it retires THIS CONFIGURATION as a solo ship candidate. |

⚠ **Nothing here treats 50.0 as a floor.** The mechanisms that would produce a
sub-50 reading are pre-named: twelve siege-active maps whose geometry the plank
has never met (long approaches on the four 30×30s, tight cores on `nordkap` at
d²=144); a door response that costs home builder-actions on maps where no door
turret is ever planted; a belt lifeline that reserves titanium the collar
needs; and 20% of the pool played by a chassis that is not byte-identical to the
control.

⛔ **AND ONE CROSS-BAND NOTE: an operational cancellation reaches NONE of these
rows EXCEPT via the COMBO-STOP carve-out at n=2,700** — a trend-floor,
catastrophe or capacity stop reads `CANCELLED — UNRESOLVED, defaults to the
RESTRICTION`.

---

## THE CHANGE — `file:line`, incumbent → treatment

**TREATMENT `bots/_v513siegecrew`** = `bots/_v488beltbreak2` **plus the whole
ferry-siege stack in five files, one of which is entirely new.** Re-runnable in
five commands (all four shared modules DIFFER; none is `cmp`-clean, which is
itself the honest statement of scope):

```
$ diff bots/_v488beltbreak2/doctrine.py bots/_v513siegecrew/doctrine.py | grep -c '^[<>]'   # 758
$ diff bots/_v488beltbreak2/main.py     bots/_v513siegecrew/main.py     | grep -c '^[<>]'   # 567
$ diff bots/_v488beltbreak2/eco.py      bots/_v513siegecrew/eco.py      | grep -c '^[<>]'   #  75
$ diff bots/_v488beltbreak2/raid.py     bots/_v513siegecrew/raid.py     | grep -c '^[<>]'   #  28
$ ls bots/_v488beltbreak2/siege.py                            # does not exist (2,391 new lines)
```

**INHERITED FROM `_v510` / `_v511sealonly` / `_v512ringladder`** (unchanged, and
`raid.py` verified byte-identical to v512's by `md5`): the launcher ferry, the
barriers-only collar, the at-ring priority ladder with its in-bot `_fs_rung`
inversion falsifier, the eviction rung, the raider-built sentinel, the
map gate (`siege.py:254-300`, `FS_MAP_SKIP` at `doctrine.py:2365-2372`) and the
RING/KILL titanium reserves.

**NEW IN `_v513siegecrew` (the eight changes, each answering a ranked autopsy
defect):**
* **A — sentinel and magazine only AFTER the salt** (Magnus, direct). Gate
  `siege.py:1936` `_fs_salt_ok`, consumed at `:1987` inside `_fs_sentinel_ok`
  (`:1977`); core-side arming `main.py:519` under `LOKI_FS_CREW and
  FS_SALT_GATE`. Answers autopsy #3 (fire is 1:1 heal-cancelled pre-seal).
  Constants `FS_SALT_GATE=True` (`doctrine.py:2614`), `FS_SALT_GRACE=8`
  (`:2621`), `FS_SALT_LATCH=False` (`:2633`, the measured-no-gain fallback).
* **B — door-turret response.** `main.py:1030` `_door_turret`, `:1085`
  `_door_turret_turn`, hooked at `:1014`; `FS_HOME_TURRET_RESPONSE=True`
  (`doctrine.py:2653`), `FS_DOOR_DSQ=40`, `FS_DOOR_TI_FLOOR=6`,
  `FS_DOOR_MAX_RNDS=40`, `FS_DOOR_TYPES={GUNNER, SENTINEL}`. Answers autopsy
  **#1** — 0 of 40 plants ever attacked, carrying 100% of our core damage.
* **C — belt last link + eco lifeline.** `eco.py:371`
  `_eco_spendable(essential=)`, `:997` `_build_next_link`, `:1093` `_l4_repair`;
  `FS_BELT_LASTLINK=True` (`doctrine.py:2690`), `FS_ECO_LIFELINE=24`,
  `FS_ECO_HEADROOM=8` (**no longer added to the core's floor — that addition
  WAS the 6-Ti deadlock**). Answers autopsy #2 (perfect 24/24 separation:
  tic=0 ⟺ no core-adjacent link).
* **D — second body (support raider). SHIPS OFF.** `siege.py:1192`
  `_fs_supp_turn`, `:1250` `_fs_supp_walk`; roster `main.py:832`, appointment
  `:981`; `FS_CREW_ON=False` (`doctrine.py:2741`). Measured HARMFUL at
  −15.6pp, direction consistent across 3/3 blocks (§6).
* **E — rung-2 seal-wait exemption.** `siege.py:1478-1520`. Answers autopsy #8
  (0 evictions in 19/24 games). **Inert while D is off.**
* **F — the magazine, traced.** `main.py:519-560` (KILL floor), `:656`
  (`convert_ammo` minimum drops 4 → 1 while the siege is live). Answers autopsy
  #4; the root cause was a SHAPE — the bank equilibrates to `ti_floor` because
  `convert_ammo` is its only surplus consumer — **which is why two blind
  re-tunes had failed.**
* **G — replacement on dedicated store bits + dodge rework.** `siege.py:191/205`
  crew beats, `:223` `_raid_seat_take`, `:899` `_fs_hit_mark`, `:1298`
  `_fs_try_retreat`, veto in `_fs_stand_target:1490`; `FS_PRESTAND_AVOID=True`
  (`doctrine.py:2821`), `FS_RETREAT_ON=True`, `FS_RETREAT_HP=14`,
  `FS_CREW_SLOT`/`FS_RAIDN_MASK`/`FS_CREW_SEAL_SHIFT`/`FS_CREW_SUPP_SHIFT`
  (`:2806-2811`). Answers autopsy #5 (dodge prevented 0 of 23 deaths; the
  blacklist was a sort key, not a veto). ⚠ **Magnus's ~15-round replacement cap
  is NOT met (median 90) — the binding constraint is FUNDING a body, and the
  cheap fix is exactly what D measured as harmful. Top open item, disclosed.**
* **H — purposeful spawns.** `main.py:743` (spawn sort), `:775`
  `_spawn_ore_anchor`; `FS_SPAWN_PURPOSE=True` (`doctrine.py:2842`). ⚠ **Ships
  ON and cannot be shown not to regress at n=90** (52/90 spawn-purpose-off
  against 48/90, per-block direction straddling). Mechanism verified; effect
  unmeasured either way.

---

## SEEDS, SURFACE, RUNNER

**SEEDS: base 874000**, verified free at draft on four surfaces (see STATUS).
`tools/overnight.sh` advances the seed every 16 games, so a full shard consumes
**874000-874337**. ⛔ **Any battery run against this tree must use a base OUTSIDE
that range** so no battery game can collide with a screened game; the next
family shard should take **876000** on the 2000-spacing convention.
**SURFACE: LOCAL, SAME-HOST, 8 in-process workers on one box** (both sibling
tapes ran `workers=8`; registered explicitly here rather than as "one worker").
**RUNNER:** `zsh tools/overnight.sh SIEGECREW bots/_v513siegecrew bots/_v488beltbreak2 5400 874000`
— basenames do not collide (`_v513siegecrew` vs `_v488beltbreak2` share no
substring), so the guard at `overnight.sh:76-79` passes (checked at draft).
**GATE:** `tools/auto_gate.py` against the `SIEGECREW` row below, **unexempted —
`COMBO_BAR = 55.0` binds at n=2,700 and is this shard's modal terminator.**

---

## READY-TO-PASTE ROWS — ⛔ FOR THE BUILDER TO APPEND AT LOCK, NOT BY THIS AGENT

⛔ **ORDER IS LOAD-BEARING: the `BARS.tsv` row goes in BEFORE the worklist row**
(the BELTBREAKR lesson, and the s50 silent-`awk` incident recorded in the
`BARS.tsv` header — a worklist row that lands first is a LIVE SHARD WITH NO
BAR). ⛔ **AND THE APPEND IS NOT DONE UNTIL THE ROW IS GREPPED BACK OUT OF THE
FILE IN THE SAME SHELL CALL** — the `BARS.tsv` header carries the exact
`printf … && grep -qxF … || exit 1` idiom; use it.

### 1. `docs/prereg/BARS.tsv` — tab-separated, four columns (`name`, `bar`, `cmp`, `source`)

```
SIEGECREW	51.33	ge	docs/prereg/PREREG-SIEGECREW-2026-08-18.md — DECISION bar 51.33 ge, POINT RULE (OB16, MDE 0.00; re-derived at draft as 50 + 1.96*sqrt(0.25/5400) = 51.3336), n=5400, h2h share, LOCAL SAME-HOST (one box, 8 in-process workers) seeds 874000-874337. Locked <TS> PRE-START by the builder (s51); drafted by a fresh opus agent, judgment lines ratified by the lane. PACKAGE HEAD-TO-HEAD, NOT CLAUSE ISOLATION: TREATMENT bots/_v513siegecrew vs CONTROL bots/_v488beltbreak2 — the PROGRAMME INCUMBENT and the chassis under the LIVE HOLDER v159 Sleipnir v2; SELF-LEG, win and loss are the same event, kill-clock metrics WITHIN-ARM only. THIRTEEN mechanisms differ (v512's ferry + collar + eviction rung + raider sentinel + dodge, PLUS v513's eight: sentinel-after-salt, door-turret response, belt last-link + eco lifeline, second body, rung-2 seal-wait exemption, traced magazine, dedicated-bit replacement + dodge rework, purposeful spawns) across ALL FOUR shared modules (doctrine 758 / main 567 / eco 75 / raid 28 diff lines) PLUS a 2,391-line siege.py absent from the control; a pass promotes the STACK, clause isolation would be vs _v512ringladder and is NOT being run (one core, s51 directive "launcher experiments, nothing else"). ⭐ FIRED CONFIG SHIPS TWO MECHANISMS OFF: FS_CREW_ON=False (the second body LOST on every column, −15.6pp at n=90 — but per the side-lane D-pass F4 two of three crew-ON blocks are PRE-CODE-MOVE, so the number OF RECORD is the matched 13.3pp at n=60 in doctrine.py:2721-2726; and per F5 the denial-acquittal is a fail-to-exclude at ±17.9pp, so the second body is OFF on a DIRECTION whose mechanism is NOT established) and FS_SALT_LATCH=False (Magnus's strict rule ships because he ordered it; the "measured no gain" beside it is n=15/arm, MDE ≈35pp — a PRIOR, NOT AN EVIDENCE ROW, D-pass F6a, and nothing on the page leans on it; same class: the convert_ammo 4→1 floor change rests on ONE instrumented game, F6b). ⭐ NO INSTRUMENTATION CONFOUND: FS_LOG=False and FS_DRAW_ON=False were ALREADY off in the tree AND in the n=90 build grid, so unlike RINGLADDER the prior and the shard describe the same configuration and no flag flip is owed in the lock commit. ⛔ NO COMBO-BAR EXEMPTION CLAIMED AND COMBO_BAR=55.0 BINDS AT 2700: genuine combination on the merits (13 mechanisms, 4 modules, a new 2,391-line module), no additive prediction exists to score against, and the inherited stack.py compose marker (doctrine.py:2078) is not the reason. ⛔⛔ PRICED PRE-FIRE OVER THE ACTUAL GATE (Monte Carlo, 20k trials/row, clauses as auto_gate implements them) AND THE MODAL OUTCOME IS A COMBO-BAR STOP AT n=2700 (P≈0.77 at the registered prior; P(reach 5400)=0.072, 0.290 at the grid's own point; CATASTROPHE ≤0.04 everywhere but the map-pessimistic corner — the OPPOSITE of RINGLADDER). The arm's own grid reads 49/90 = 54.44% vs this exact control in the fired config, and ITS INTERVAL CONTAINS PARITY: ±10.19pp at local DEFF 0.98 ⇒ [44.26,64.63] (the build report printed none; side-lane D-pass F7). The shard's pool is 12 siege-active / 3 gated (antler d^2=64, archipelago in FS_MAP_SKIP, fjordgate 10x10 — computed at draft from maps/*.map26 against V513'S OWN predicate at siege.py:254-300, which was diffed against v512's and found unchanged), giving a REGISTERED COMPOSITION PRIOR of 0.80x54.44 + 0.20x50.00 = 53.56%, a sampling FLOOR of 0.80x44.26+10 = 45.41 (just ABOVE the 45.0 catastrophe line) and a SEGMENT VALUE CEILING of 0.80x64.63 + 0.20x50.00 = 61.70pp (ABOVE the bar, unlike RINGLADDER's 41.03). The bar needs 51.66% on the siege-active segment; the COMBO bar needs 56.25%, ABOVE the grid's point. ⛔⛔ AND THE DOMINANT UNCERTAINTY IS COMPOSITIONAL, NOT SAMPLING: the grid's five maps are NOW KNOWN (scratchpad/v513_build/run_grid.py:17 — glacierkeep, nordkap, atoll, midgard, drakkarfjord; run_grid.py:16 confirms OPP=bots/_v488beltbreak2) because the evidence base was banked into the repo s51 after the D-pass flagged it living in a dead session's /private/tmp (F3). Per-map, read at draft from the raw TSVs: glacierkeep 18/18 = 100.00%, drakkarfjord 11/18 = 61.11%, atoll 8/18 = 44.44% (RETIRED from the pool 2026-08-13 — 20% of grid rows are geometry this shard NEVER PLAYS), midgard 6/18 = 33.33%, nordkap 6/18 = 33.33%. A 68pp spread; removing glacierkeep alone drops the grid to 31/72 = 43.06%. ELEVEN of the 15 pool maps carry ZERO observation of this tree and ALL THREE GATED MAPS DO, so the primary segment's 50.0 prediction is entirely untested pre-lock. The MAP-COMPOSITION BAND is 42.96 to 57.78 pooled — WIDER than the sampling band and centred lower — and it splits the terminator: COMBO stop at 53.56-57.78, TREND-FLOOR stop at 42.96-50.00. The registered prior stays 53.56 (the arm's headline and the D-pass's number); picking a lower one after seeing the decomposition would be picking the prior to fit the pricing. ⭐ COMBO-STOP CARVE-OUT PRE-COMMITTED: a COMBO stop leaves the tape at EXACTLY the registered 2700 floor, so it licenses a BAND reading at n=2700 (half-width ±1.886pp, Band 1 needs point ≥ 53.22) with the selection disclosed AND SIZED at 0.13pp (prior) to 0.45pp (grid point) by truncated normal — an order of magnitude milder than the family's generic +2pp, which would UNDERSTATE this arm. No other clause's cancellation licenses any band. FIRINGS-BEFORE-PRIMARY HARD: F1 map gate + pool composition (SHARD-NATIVE and exact; prefix balance MEASURED on a real completed 8-worker tape of this fixture at 20.50/20.20/20.00/20.00% gated and exact 50/50 seats at the 400/1000/2700/5400 prefixes), F2 salt gate 0 pre-seal sentinels vs 14 salt_off / 10 crewflag_off, F3 door response 152 pecks and 11/30 games vs 0 door_off / 0 crewflag_off against a v512 baseline of 0 of 40 plants attacked, F4 belt last-link tic=0 in 1/15 vs 5/15 belt_off and 9/15 crewflag_off (4/90 vs the parent's 46/90 at the outcome grid), F5 crash invariant 0 tracebacks across 730 grid rows (the report says 670; conservative, denominator corrected) + 165 mechanism/demo games, 296 .err files grepped — WITH THE NEAR-MISS RECORDED: a real NameError DOES exist in scratchpad/v513_build/smoke/i_nordkap.err at main.py:557 inside the FS_MAG_TRACE print, fixed in the shipped tree (import sys at main.py:32, FS_MAG_TRACE=False) so no live hazard, but it would have destroyed OUR CORE (D-pass F9b). Ladder inversions 0 of 804 — the FINDING holds (0 lines matching 'inver') but the 804 DENOMINATOR IS NOT-ESTABLISHED (rep_logship 507 + rep_onlog 604 = 1,111; D-pass F9a). F2-F5 are NOT re-readable on the shard (--replay /dev/null, stderr discarded, FS_LOG off) and the tape's cond column is BINARY (core_destroyed / tiebreak, checked on two completed tapes) so it carries NO tiebreak key and titanium_collected=0 is unrecoverable by any route; the registered alarm proxies are our-core-death rate (F3), the r1000 share with a STOP RULE above ~19% against the grid's 11.1% (F4), and any NOWINNER row (F5). ⛔ THE NOISE FLOOR IS MEASURED: the INERT mutant FS_CREW_EVICT_NOWAIT=False still moved the evictor count 9→5, so only ZERO-VS-NONZERO contrasts are readable on the mechanism counters and ratios are not. PRIMARY SEGMENT = GATED vs SIEGE-ACTIVE, fixed BLIND at draft and shard-native: GATED must read 50.0 ±2.98pp at full n (±4.22pp at 2700) or the reading is ATTRIBUTION UNRESOLVED EVEN IF THE BAR CLEARS — the equivalence there is FLAG-AND-STATE CONDITIONED, NOT byte-verified, v513's non-siege diff is 5x v512's on eco.py and 2x on main.py with changes C and H on paths that run on EVERY map, and all three gated maps carry zero pre-lock observation. THIRD FALSIFIER: a majority-r1000 gain downgrades one band as OFF-DOCTRINE COMPOSITION (pre-registered as UNLIKELY — grid r1000 11.1% vs the control's own 11.28%; but note 6 of glacierkeep's 18 wins were tiebreaks). ⭐ r300 ADMISSION BAR REGISTERED ON ITT RMST300 AS PRIMARY WITH AN EXPLICIT MDE OF +5.0 ROUNDS — this prereg is what settles the D-pass's NOT-ESTABLISHED item 4, since the build report scored the SUPERSEDED timely-rate estimator and called it 'the primary' (F2; PROGRAMME.md:534-540 moved to RMST300 on 2026-08-16). MDE SIZED OFF THIS ARM'S OWN MEASURED sd (treatment 48.03, control 49.07, delta 68.66, from scratchpad/v513_build/grid/*.tsv): half-width ±1.83 at n=5400 and ±2.59 at n=2700 — RESOLVES AT BOTH, unlike RINGLADDER whose n=400 stop resolved neither. Co-bar ITT timely-kill must EXCLUDE a 3.0pp fall (±2.01pp at 5400, ±2.84pp at 2700 — clears by only 0.16pp, registered KNIFE-EDGE and re-tested against the sd recomputed from this tape). PRE-LOCK READ ON BOTH COMPARATORS, computed at draft: vs the PARENT v512, RMST300 276.09 vs 289.02 ⇒ −12.93 rounds [−25.8,−0.1], excludes +5.0 and passes (the D-pass's figure, re-derived exactly) — BUT THAT IS NOT THIS BAR'S COMPARATOR; vs the CONTROL in the SAME 90 games, 276.09 vs 276.88 ⇒ −0.79 rounds [−15.0,+13.4], and ITT timely-kill 24/90 = 26.67% vs 23/90 = 25.56% (+1.11pp). DIRECTIONALLY FINE ON BOTH, RESOLVED ON NEITHER AT n=90 — the shard resolves it. Treatment median kill round 281 (up from v512's 241, collider-conditioned: 3x as many kills; blocks straddle 214/414/291). LOCAL surface: DEFF 0.98, naive intervals, platform constants 1.529/1.833 NOT imported. CLUSTER UNIT none (match/opponent/host/seed dead; MAP is a balanced STRATUM, not a cluster, MEASURED on a completed tape rather than asserted). SAME-HOST REQUIRED; adding a SECOND HOST mid-run needs an amendment typed before the first row (Addendum 11 rider). DEFERRED OBLIGATION DISCHARGED AT RATIFICATION: full deterministic flag-off equivalence for v510/v511/v512 (coordination.md:71346) — Agent D verdicts and artifact paths filled in at the lock (scratchpad/s51_det/, empty at draft; a NON-equivalence verdict on any pair is an INSTRUMENT ALARM for the gated-map argument and must be resolved BEFORE the lock). v513's own LOKI_FS_CREW flag-off is verified structurally + behaviourally (n=60 paired: 12/44/27 vs v512's 9/46/30) and byte-identity is IMPOSSIBLE under NOISE_ON per the s50 one-draw law. ⛔ OPEN SCOPE ITEM CARRIED INTO THE LOCK (D-pass F1, its top-ranked flag): the fired tree ships FS_HOME_TURRET_RESPONSE=True (doctrine.py:2653, live via LOKI_FS_CREW=True at main.py:1097), a home-doctrine change that self-describes as piercing LOKI_QUIET_ON (main.py:1088), while the builder's own record at coordination.md 20:32:18Z says it 'needs Magnus's nod' and the 21:34Z morning-decisions list omits it. NO APPROVAL RECORD EXISTS EITHER WAY. No flag flip is proposed — turning it off would fire a different package than the one measured at 54.4% — but the builder must record the state before the lock (ratification blocker B5). ⚠ LYING-FIXTURE CAVEAT BINDING ON THE WHOLE PAGE: the control is our own chassis, change B answers a behaviour OUR OWN incumbent exhibits (40 door plants in 24 games) so the 54.4% is partly a read of how well we counter ourselves, and the field's sealers close rings at rates down to 0/347 (lighthouse) with 8.6% clearance overall — NOTHING here transfers to the ladder without a live leg (CLAUDE.md rule 6), and the live leg is unavailable tonight under LOCK-IN. A pass buys a place in the queue for that leg and nothing else. ⭐ CANCEL-FOR-CAPACITY PRE-REGISTERED: if the builder returns the core to other launcher-line work (FS_CREW_CONVERT screen, replacement-funding design), that is POLICY AND NOT EVIDENCE — typed cancellation, partial disclosed as UNSELECTED (no selected-pessimistic caveat, unlike a floor, combo or catastrophe stop), licenses no sentence about whether the package pays.
```

### 2. `scratchpad/corefill_work.txt` — tab-separated, five columns, appended AFTER the BARS row

```
SIEGECREW	bots/_v513siegecrew	bots/_v488beltbreak2	5400	874000
```

⛔ **Exactly five fields.** The `BARS.tsv` header records why a sixth would be
unsafe: `corefill.sh:142` and `worker.sh`'s G4 both read the row with
`read -r SH TR CT TG SL`, so a sixth field lands inside `$SL`, and `corefill.sh`
passes `$SL` unquoted to `overnight.sh:169` while every remote worker refuses a
non-numeric seedbase outright.

---

**PROVENANCE: docs/prereg/PREREG-SALTRAY-2026-08-17.md · docs/prereg/PREREG-RINGLADDER-2026-08-17.md · docs/prereg/BARS.tsv · docs/research/BUILD-REPORT-v513siegecrew-2026-08-17.md · docs/research/AUTOPSY-v512-three-maps-2026-08-17.md · docs/research/AUDIT-sidelane-v513-Dpass-2026-08-18.md · docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md · PROGRAMME.md · results.tsv (rows ringladder-final, saltray-final, beltbreak2-final) · tools/auto_gate.py · maps/ · bots/_v513siegecrew/siege.py · scratchpad/v513_build/**
*Read by the drafting agent. Additional facts verified directly against the repo
at draft and cited inline where used:
`bots/_v513siegecrew/{doctrine,eco,main,raid,siege}.py`,
`bots/_v488beltbreak2/{doctrine,eco,main,raid}.py`, `maps/*.map26` (the 15-map
pool, parsed for `(w, h, core anchors)` and evaluated against the bot's own gate
predicate), `tools/overnight.sh`, `tools/map_admits.py`, `tools/prereg_check.py`,
`scratchpad/overnight/{BELTBREAK2,RINGLADDER,SALTRAY}.tsv` (fixture headers,
`cond` value domains, prefix map/seat balance),
`scratchpad/v513_build/{run_grid.py,grid/*.tsv,smoke/i_nordkap.err}` (the
per-map decomposition, the map-composition band, RMST₃₀₀ and ITT timely-kill on
BOTH comparators, the control identity read off the runner),
`results.tsv:{idnull140-cert-5400,null125-final}`,
`scratchpad/corefill_work.txt`, `scratchpad/s51_det/`,
`docs/coordination.md:71294,71346,71375,71376`, and `git ls-files` /
`git status --porcelain` / `git log --diff-filter=A` / `md5` on both arm trees.*

---

## RATIFICATION (builder s51 — the lane types this, per the fresh-drafter rule)

*(B1, B3, B4 and B5 to be answered here in writing before the lock commit — B2 is
discharged at draft and needs only confirmation — and the
DEFERRED OBLIGATION SLOT's placeholder filled with Agent D's verdicts and
artifact paths.)*

**B1 — RULED: branch (i), FIRE UNEXEMPTED WITH THE COMBO-STOP CARVE-OUT.** The
COMBO bar binds on the merits (13 mechanisms, a new module; no additive
prediction exists) and no exemption token is claimed. The modal outcome is a
COMBO stop at n=2,700, which under the carve-out is a BAND reading at ±1.886pp
with its selection sized (0.13-0.45pp) — that reading is the full-pool
measurement this shard exists to buy (11 of 15 maps carry zero observation).
**NOTE TO MAGNUS, on the page as the drafter recommends: if the COMBO bar stops
this arm, it will have stopped an arm predicted to clear its DECISION bar —
the 55.0 constant is a s48 regime constant and its pricing on combination arms
is his to revisit, not this page's.**

**B2 — CONFIRMED:** grid maps read from the banked runner
(`scratchpad/v513_build/run_grid.py:17`), composition prior stands as drafted.

**B3 — DISCHARGED:** all three pairs EQUIVALENT with a fired positive control;
see the DEFERRED OBLIGATION SLOT above for the full record. No instrument alarm.

**B4 — CONFIRMED:** LOCAL SAME-HOST, 8 in-process workers, one box; no second
host without a pre-row amendment. `auto_gate --apply` alive at boot (fleet
health) and reads `docs/prereg/BARS.tsv`; the builder verifies the SIEGECREW
row appears in auto_gate's next bars census after the append, before trusting
any floor.

**B5 — STATE RECORDED:** `FS_HOME_TURRET_RESPONSE=True` ships live in the fired
tree with NO Magnus approval record either way. It is now item 6 on the Magnus
morning-decision list (HANDOVER.md, added s51 on the D-pass's F1, commit
d1a172ce). No flag flip — this shard measures the package as built at 54.4%;
if Magnus vetoes the flag, the package on this page is not the package we ship
and a new prereg is owed for the changed config.

**RATIFIED AND LOCKED by the builder s51. Drafted by a fresh opus agent per the
standing rule; the judgment lines above are the lane's. Lock commit = this
commit (clock 1, git author time); shard creation follows (clock 2).**
