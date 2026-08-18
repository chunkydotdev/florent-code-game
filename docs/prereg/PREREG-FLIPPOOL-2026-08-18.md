# SCREEN PREREG — `FLIPPOOL`: the standdown flip at full pool. **COMPACT SIBLING OF `PINCERPOOL`.**

⛔⛔ **TWO DEVIATIONS FROM STANDING PRACTICE, DISCLOSED FIRST BECAUSE THEY ARE
THE READER'S BIGGEST DISCOUNTS ON THIS PAGE.**

**1. THIS PAGE WAS NOT DRAFTED BY A FRESH AGENT.** The fresh-drafter rule was
deliberately set aside on **Magnus's token-conservation directive** (relayed by
the builder, 2026-08-18): the `PINCERPOOL` drafter was RESUMED rather than a new
agent spawned. ⇒ **the independence the fresh-drafter rule buys is NOT present
here.** This agent wrote `PINCERPOOL`, so its composition method, its priors and
its blind spots are inherited wholesale rather than re-derived by someone who
could disagree with them. **Nothing on this page independently checks
`PINCERPOOL`'s method; it applies it.** The builder ratifies with that known.

**2. THIS PAGE IS INCORPORATION BY REFERENCE, NOT A SELF-CONTAINED PREREG.**
`docs/prereg/PREREG-PINCERPOOL-2026-08-18.md` is the parent. **Everything not
listed under DELTAS below is carried from it unchanged and is NOT restated:**
the ESTIMATOR and its `T`/`C` column note (§REGISTRATION BLOCK); CLUSTER UNIT
`none` and the five-candidate enumeration, local DEFF 0.98, naive intervals
(ibid.); BOUNDARY, CUT-SHORT and the COMBO-STOP carve-out (ibid.); BAR SOURCE
and BASE RATE SOURCE (ibid.); the operational floors and GATE RESOLUTION (a)-(d)
(ibid.); the one-draw law and the measured `--seed` non-reproducibility
(§READ BEFORE RATIFYING 6); FIRINGS-BEFORE-PRIMARY F1-F5 with their alarm
proxies and stop rules (§FIRINGS); the LYING-FIXTURE caveat and the
`STEALTH_UNTIL_DROP` scope (§LYING FIXTURE); CANCEL-FOR-CAPACITY
(§READ BEFORE RATIFYING 7); the FALSIFIER set, the HONEST-NULL clause and the
five READING bands (§FALSIFIER, §READING); the CPU/TLE unmeasurability note
(§READ BEFORE RATIFYING 4); and blockers **B4** (same-host, 8 workers,
`gate_watch`, 2-6 h), **B5** (stealth scope) and **B6** (the `FS_V521_GATEFIX`
discharge). **A reader who has not read `PINCERPOOL` has not read this
registration.**

**STATUS: drafted BEFORE the `FLIPPOOL` row exists anywhere.** Wall clock
**`2026-08-18T17:57:37Z`** (`date -u`, same shell call); repo HEAD `22ab0f0d`.
Verified at draft: `grep -ci flippool` → **0** on `docs/prereg/BARS.tsv`,
`scratchpad/corefill_work.txt`, `results.tsv`, `elo_history.tsv`; `ls
scratchpad/overnight/ | grep -ci flippool` → **0**; no `docs/prereg/PREREG-FLIPPOOL*`
existed before this file.

---

## THE DELTAS — everything that is NOT `PINCERPOOL`

### D1. TREATMENT TREE
**`bots/_v524exact` → `bots/_v525flip`.** Added whole in **`5621ebac`**
(`Tue Aug 18 19:55:10 2026 +0200`); `git ls-files` lists all five modules,
`git status --porcelain bots/_v525flip` **empty**. Digests at draft:
`doctrine.py 6cb12ea45935aba347dcfba534686e9c` (4,796 lines) ·
`eco.py bba326d71a4f698f555785de13aa4135` (1,916) ·
`main.py e5e262e05f35fa85a61cff4c588288e1` (2,456) ·
`raid.py 3b3a0456e9a22083df4653526bfd68c8` (1,382) ·
`siege.py e7d3fc5c44c6058331b7bebcf8dd004f` (5,407).
**`eco.py`, `main.py` and `raid.py` are byte-identical to `_v524exact`'s by
`md5`; the whole delta is 90 doctrine lines + 15 siege lines** — smaller than
v524's, which was itself the smallest this family had fired.
⚠ **The build report's ARTIFACTS section says the tree is *"(uncommitted)"*.
That is STALE — it was committed at `5621ebac` after the report was written, and
the digests above are read off the committed, clean tree.**
CONTROL unchanged: `bots/_v488beltbreak2` at `997bcd42`, digests as `PINCERPOOL`
§COMMIT PROVENANCE.

### D2. THE CHANGE — two selections, one flag
`LOKI_FS_V525 = True` (`doctrine.py:4782`). **`False` reproduces `_v524exact`
exactly and is the REGISTERED MUTANT.** Both selections are read **at runtime**
inside `_fs_map_gated`, never at module scope — the append-ordering hazard
v515/v524 both document.
* **CHANGE 1 — `yulerune` leaves the cripple candidate set.**
  `FS_V525_CRIPPLE_MAPS` (`:4786`) carries **midgard's signature only**;
  yulerune's is deliberately absent, so yulerune *and* `frostgate` (which shares
  it, and which v524's exact-grid match had already reclaimed) never reach the
  CRIPPLE test. Consumed at `siege.py:522-526`. **Midgard's signature stays, and
  v524's exact-grid confirm still disambiguates it from `ragnarok`.**
* **CHANGE 2 — `antler` and `fjordgate` un-gated.** `FS_V525_MIN_MAP_DIM = 10`
  (`:4792`, was 12) and `FS_V525_MIN_CORE_DSQ = 32` (`:4793`, was 72), consumed
  at `siege.py:489-497`. ⭐ **A THRESHOLD CHANGE, NOT A REMOVAL, AND THE NEW
  FLOORS ARE `fjordgate`'S OWN GEOMETRY** (10×10, core d²=32 — the binding map on
  both axes), **so a 9×9 or any closer-cored board is still refused.** The strict
  `<` admits fjordgate exactly at its own boundary. `archipelago` is untouched:
  it is refused by `FS_MAP_SKIP`, a different, closure-based mechanism.
* Also new: `FS_V525_LOG = False` (`:4794`), off in the fired config.

**BASIS — and it is the one thing on this page that is genuinely new evidence
rather than a re-weighting:** Magnus's ask (*"could we test it on all maps and
check if it performs better than we thought?"*), answered by the **FORCEALL
probe** (`scratchpad/s51_forceall/results.tsv`, n=90/map, forced rush with every
threshold zeroed at the definition site, vs `bots/_v488beltbreak2`):
`yulerune` **91.1%** [±5.9] · `antler` **64.4%** · `fjordgate` **63.3%** ·
`midgard` **40.0%** (stays cripple) · `archipelago` **17.8%** (stays gated).
⇒ **THE STANDDOWNS WERE STALE-CALIBRATED — the gates are v510-era thresholds and
the cripple list is a v513-era read, and the rush has since gained pincer,
funding, door-off and terminal-hop. Two of the five standdowns survive their own
re-measurement; three do not.**

### D3. SEGMENTS — the largest delta on the page
Computed against v525's own predicate; **independently reproduced by the build's
own `predicate_table.py`, which drives the real `_fs_map_gated` both ways**:

```
GATED        1 of 15 =  6.67%   archipelago   (FS_MAP_SKIP, unchanged)
CRIPPLE      1 of 15 =  6.67%   midgard       (narrowed candidate set + v524 exact grid)
SIEGE-ACTIVE 13 of 15 = 86.67%  everything else, incl. antler, fjordgate, yulerune
```
**REFUSING = 2 of 15 = 13.33%** (was 33.33% under `PINCERPOOL`/v524, 46.67%
under v522). `LOKI_FS_V525 = False` re-selects the parent's five standdowns
digit-for-digit — `PREDICATE TABLE OK, both directions`.

### D4. `SHIP_BAR` ARITHMETIC — **BOTH MARKS ARE NOW COMFORTABLY REACHABLE**
`pooled = 0.1333 × refusing + 0.8667 × S`:

| pooled target | required `S` | under v524 | under v522 |
|---|---|---|---|
| 51.33 (DECISION bar) | **51.53%** | 51.99% | 52.49% |
| 55.00 (combo bar) | 55.77% | 57.50% | 59.38% |
| **69.57 (REGISTERED PRIOR)** | **72.58%** | — | — |
| **75.00 (`SHIP_BAR` FLOOR)** | **78.85%** | 87.50% | 96.88% |
| **80.00 (`SHIP_BAR` TARGET)** | **84.62%** | 95.00% | ⛔ impossible |
| ceiling (S = 100) | — | **93.33%** max pooled | 83.33% | 76.67% |

⭐⭐ **THE REGISTERED PRIOR (69.57) IS 5.4pp FROM THE DROP FLOOR, AND THE
REQUIRED SIEGE-ACTIVE SHARE (78.85%) IS BELOW THE 82.22% THE THREE POWERED MAPS
ALREADY READ. THIS IS THE FIRST PAGE IN THE FAMILY ON WHICH THE `SHIP_BAR` FLOOR
IS NOT OBVIOUSLY OUT OF REACH.** ⚠ **That is an arithmetic statement about a
composition prior, not a measurement, and the whole point of firing is that the
five never-observed maps carry 1,800 of the shard's rows.**

### D5. COMPOSITION PREDICTION — `PINCERPOOL`'s cell-by-cell method, four classes
`S = (3·trio + 2·reclaimed + 3·flipped + 5·unobserved) / 13`, equal weight per
map (the shard is map-balanced at 360 games/map):

| cell | maps | prior | n | basis |
|---|---|---:|---:|---|
| **trio** | `drakkarfjord` `glacierkeep` `nordkap` | **82.22%** | 540 | the v522/v524 6-map `KILL_TARGET` panel, 180/map, fired config |
| **v524-reclaimed** | `ragnarok` `frostgate` | **63.33%** | 120 | the v524 build's direction battery, 60/map |
| **v525-flipped** | `yulerune` `antler` `fjordgate` | **78.33%** | 180 | **this build's** direction read, 60/map: 58/60 · 38/60 · 45/60 |
| **unobserved** | `auroraveil` `drumlin` `icefloe` `royale` `valkyrie` | **67.05%** | **0** | `PINCERPOOL` §2.3 method: trio × the v513-tape ratio 0.8155 |

⇒ **`S` = 72.58%.** With both refusing cells at the structural 50.00:
**`pooled = 0.0667×50 + 0.0667×50 + 0.8667×72.58 =` 69.57%.**

| # | scenario | `S` | **pooled** |
|---|---|---:|---:|
| A | FLAT — all 13 at the trio | 82.22 | 77.93 |
| B | unobserved at the trio (no ratio discount) | 78.42 | 74.63 |
| **D** | **REGISTERED — cell-built as above** | **72.58** | **69.57** |
| E | flipped maps regress to their FORCEALL basis (72.93) | 71.34 | 68.49 |
| F | unobserved at v513's raw 57.28 (no scaling) | 68.83 | 66.32 |
| G | refusing carries residual chassis drift to 45 | 72.58 | 68.91 |
| H | midgard at its OWN measured 57.78 rather than structural 50 | 72.58 | 70.09 |
| I | OPTIMISTIC — flat, refusing at 55 | 82.22 | 78.59 |

**MAP-COMPOSITION BAND 66.32 – 78.59. SAMPLING band on the observed anchors
65.70 – 74.45.**
⛔ **The registered prior stays 69.57.** Two disclosures that pull opposite ways
and are both on the record before the fire:
* **The flipped cell is the shakiest of the four and it is 3/13 of the segment.**
  Its three maps read 96.67 / 63.33 / 75.00 at **n=60 each (±12.65pp per arm)**,
  and against their FORCEALL basis they run **+5.6 / −1.1 / +11.7pp** — all
  inside the band, but `fjordgate`'s delta sits at its edge and the build report
  says so itself. **A prior, not evidence** (`PINCERPOOL` §2.2a language applies
  verbatim).
* **Scenario H is the one place a measured cell disagrees with the registered
  structural value.** `PINCERPOOL` registered CRIPPLE at 50.00 because the
  structural expectation and the two-cell measurement coincided at exactly
  180/360. **With `yulerune` flipped out, the cripple cell is `midgard` alone and
  its own panel read is 104/180 = 57.78% [50.56, 65.00].** This page keeps
  **50.00** — the refusing segment is the PRIMARY and 50.0 is its registered
  prediction, a single map at n=180 sitting 1.1 half-widths high is not a reason
  to move a prior, and the family's own zero-dose noise floor on these cells is
  ~±6pp (`PINCERPOOL` §2.2). **Registered, disclosed, and worth +0.52pp if it
  holds.**

**SEGMENT VALUE CEILING: 86.67% × 77.06pp = 66.78pp** — the SIEGE-ACTIVE
segment's maximum contribution (pairing share = the exact map composition; the
on-segment figure is the cell-built `S` with every observed anchor at its own
upper 95% bound). Refusing complement at most `0.0667×50 + 0.0667×65.00 =
7.67pp` ⇒ **POOLED CEILING 74.45pp — the first arm in this family whose ceiling
is within 0.6pp of the `SHIP_BAR` floor.** Companion floor **65.70pp**.

### D6. P(COMPLETION) — **1.000, AND THE MARGIN IS THE WIDEST YET**
Same Monte Carlo, same clauses as `PINCERPOOL` §3 (20k trials/row, CATASTROPHE
on the running tape from n≥400, TREND-FLOOR on the n=1,000 *and* n=2,700
prefixes, COMBO-BAR@2700, FUTILITY@2700). **P(reach 5,400) = 1.000 and
P(any stop) = 0.000 at every point in 65.70 – 78.59**, verified at the band's
own floor and ceiling. The clauses only begin to bite below ~57%, which is now
**more than 9pp below the band's floor** (it was 4pp under `PINCERPOOL`).
⇒ **the cost to price is wall clock (~2-6 h on one box, 8 workers), not a lost
shard; this arm will not stop itself; and ANY `auto_gate` firing is an INSTRUMENT
ALARM demanding a per-segment tape inspection before any verdict** — carried from
`PINCERPOOL` §3 and §MECHANISM FALSIFIER.

### D7. PRIMARY SEGMENT and its power — **this is what the flip COSTS**
**The primary segment (declared once, in D11a) is REFUSING = {`archipelago`,
`midgard`} (2 maps, 720 games, half-width ±3.65pp at p=0.5) vs SIEGE-ACTIVE = the
other thirteen (4,680 games, ±1.43pp).** Registered prediction unchanged: **REFUSING reads 50.0 ± its own
half-width; a discordance appends `ATTRIBUTION UNRESOLVED` and blocks promotion
even if the bar clears.** Descriptive sub-split: GATED 360 games ±5.17pp,
CRIPPLE 360 games ±5.17pp.
⚠⚠ **THE FLIP HALVES THIS GATE'S POWER, AND THAT IS THE PAGE'S CLEAREST
TRADE-OFF.** Across three shards the refusing segment has gone 2,520 rows
(±1.95pp) → 1,800 (±2.31pp) → **720 (±3.65pp)**. **The equivalence check that
`PINCERPOOL` could resolve to 2.5pp, this shard resolves only to ~4pp**, and
each of its two cells is a single map. **The chassis-drift question the family
has been chasing since `SIEGECREW`'s 28.71% gets a weaker answer here than it
would have got from the parent tree** — the right trade, since the rows moved to
where the plank actually runs, but a real cost and the reason it is registered
rather than mentioned.
**EXPECTED DIRECTION: POSITIVE on SIEGE-ACTIVE (prior 72.58); NULL (~50.0) on
REFUSING; therefore POSITIVE pooled, prior 69.57.**

### D8. `KILL_TARGET` PANEL — recomputed at the new weights
Registered as a MANDATORY companion read exactly as `PINCERPOOL` §D5, with the
same derivation (trio-overstatement ratios 0.654 on k≤200 and 0.704 on k≤300
from `scratchpad/overnight/SIEGECREW.tsv`; refusing anchors from `midgard`'s own
panel cells, k≤200 14.4% and k≤300 35.0%, blended with the v513 gated profile):

| metric | 6-map panel | this control, full pool | **PRE-REGISTERED prediction** |
|---|---:|---:|---:|
| median kill round | 193 | 261 | **195 - 235 — the r180 target is still NOT met** |
| ITT kills ≤ r200 | 31.5% | 12.81% | **29 - 38%** |
| ITT kills ≤ r300 | 45.6% | 26.25% | **41 - 47%** |

⭐ **Every mark moves toward the `KILL_TARGET` versus `PINCERPOOL` (median
215-255 → 195-235; k200 25-32% → 29-38%), purely because 86.67% of the pool now
runs the plank.** ⚠ `yulerune`'s FORCEALL median kill of **109** is the single
fastest cell measured anywhere in this line and it is 1/15 of this shard — **if
the median lands below 195 that cell is the first place to look, and it is a
composition effect, not a speed-up.**

### D9. SEEDS AND RUNNER
**SEED BASE 878000**, verified free at draft on four surfaces: `grep -l 878000`
over `results.tsv`, `elo_history.tsv`, `docs/prereg/BARS.tsv`,
`scratchpad/corefill_work.txt` → **no hits (rc 1)**; `git grep -l 878000` returns
only a coincidental Elo-float substring in a `corpus/_rebuild` snapshot and
`PREREG-PINCERPOOL`'s own *"the next family shard should take 878000"* line;
`grep -o 'seeds [0-9]*' docs/prereg/BARS.tsv | sort -u` → `830000 · 854000 ·
870000 · 872000 · 874000 · 876000`, **878000 absent**; the worklist's family
bases run 870000/872000/874000/**876000 (PINCERPOOL, now live)**. **876000 IS
TAKEN; 878000 is the next free 2000-block.** A full shard consumes
**878000-878337**; the next family shard should take 880000.
**RUNNER:** `zsh tools/overnight.sh FLIPPOOL bots/_v525flip bots/_v488beltbreak2 5400 878000`
— `_v525flip` vs `_v488beltbreak2` share no substring, so `overnight.sh:76-79`
passes (checked at draft). SURFACE **LOCAL, SAME-HOST, 8 in-process workers**.
**GATE:** `tools/auto_gate.py` against the `FLIPPOOL` row, **unexempted; COMBO_BAR
= 55.0 binds at n=2,700 and is priced at P = 0.000.**

### D10. FIRINGS — what changes in F1-F5
F2-F5 carry from `PINCERPOOL` §FIRINGS unchanged (dose, zero-dose placebo, r1000
proxy, crash invariant), with two substitutions:
* **F1** is re-read against v525's predicate: **GATED 1, CRIPPLE 1,
  SIEGE-ACTIVE 13; REFUSING 2 of 15 = 13.33%**, computed from `maps/*.map26` and
  **independently asserted both ways by the build's own `predicate_table.py`**.
* **F3, the zero-dose placebo, LOSES HALF ITS CELLS.** It is now `midgard`
  alone: 104/180 = 57.78% on the fired-config panel. **STOP RULE, re-sized: a
  CRIPPLE cell outside [42.3, 57.7] at n=360 (±5.17pp, ~1.5 half-widths either
  side of 50) is an INSTRUMENT ALARM.** ⚠ **Note this makes the registered
  structural 50.00 and the observed 57.78 land on opposite sides of the stop
  rule's upper edge; the rule is read against the shard's own 360 rows, not
  against the panel's.**
* **F5's denominator is this build's:** **0 tracebacks across 387 replays** —
  predicate table, byte-identity, siege-path, direction reads and flag-off — by
  recursive `Traceback` grep over every `.err`/log in
  `scratchpad/s51_v525_build`. **Builder-declared absence, NOT upgraded to a
  measurement**, and not re-readable on the shard (stderr discarded).

### D11. THE FLIP'S OWN BOTH-WAYS CONTROLS — the strongest instrument here
* **Deterministic replay-byte `cmp`, `NOISE_ON=False` both sides, `--tle 0`,
  seed 525919, both seats:** **IDENTICAL** on the three maps this build must not
  touch (`drakkarfjord` siege-active, `midgard` cripple, `archipelago` gated —
  6/6 cells) and **DIFFERS** on all three flipped maps (`yulerune`, `antler`,
  `fjordgate` — 6/6). ⚠ n = 1 seed × 2 seats × 6 maps: it establishes the code
  paths, not the outcomes.
* **Siege-path confirmation on the flipped maps** (instrumented `FS_LOG=True`
  copy): every `FS GATE` line reads `ok 1` with the right signature, and SEAL,
  SENTINEL, THROW/EVICT, RUNG and PHASE all fire on all three. ⇒ **the plank
  genuinely runs where the flip admits it, rather than the trees differing by
  coincidence.**
* **AST derived-default scan** (`flagoff_ast.py`, guard driven both ways plus a
  real-case positive control at 2 hits): **0 v525 hits, 0 on every inherited flag
  set.** ⚠ Scope is `doctrine.py` only, matching the v524 precedent.
* **Flag-off behavioural check, n=90 full pool:** flag-off **62/90 (68.9%)** vs
  the true parent `_v524exact` **58/90 (64.4%)**, delta **+4.5pp**, well inside
  n=90 noise. ⛔ **THIS IS "NO DRAMATIC SPLIT", NOT EQUIVALENCE** — the same
  restriction `PINCERPOOL` placed on v524's flag-off arm applies verbatim, and
  this page does not carry a byte-for-byte claim for it.
⭐ **AND IT IS ALSO A SECOND FULL-POOL ANCHOR POINTING HIGH:** the parent reads
**64.4%** and the flag-off arm **68.9%** on the full 15-map pool at n=90, against
`PINCERPOOL`'s registered 63.91 for that same parent configuration. **Registered
and NOT used to move this page's prior**, for the reasons in `PINCERPOOL` §2.4a
(n=90, ±9.7pp, fired to test equivalence rather than to estimate a share).

### D11a. ⛔ REGISTRATION BLOCK — CARRIED FIELDS, RESTATED ONLY BECAUSE THE TOOL REQUIRES IT

`tools/prereg_check.py` enforces field PRESENCE, so incorporation by reference
does not satisfy it. **Each line below is the DELTA VALUE plus a pointer; the
REASONING for every one of them lives in `PREREG-PINCERPOOL-2026-08-18.md` and
is not reproduced.** A green checker on this page therefore certifies the
fields are declared, **not** that the arguments behind them were re-derived.

**TARGET BAND: N/A** — local corefill screen, zero rated exposure; and `STEALTH_UNTIL_DROP: yes` independently forbids the alternative. As `PINCERPOOL`.
**PINNED: N/A** — local self-play; control fixed by construction at `997bcd42`. As `PINCERPOOL`.
**SURFACE: local**
**CLUSTER UNIT: none** — the five-candidate enumeration (MATCH / OPPONENT / HOST / SEED / MAP) is performed in `PINCERPOOL` §REGISTRATION BLOCK and every dismissal transfers unchanged: same runner, same one-row-per-game tape, same single control tree, same registered SAME-HOST, same unseeded `random.Random()` spawn salt (measured), same map-balanced stratum. ⇒ DEFF = the measured local **0.98**; naive intervals; the platform constants 1.529/1.833 are NOT applicable.
**ESTIMATOR: the unweighted pooled treatment game share** = rows with `winner == T` / completed rows, all 5,400 rows, both seats and all 15 maps pooled, no reweighting; seat reported separately as a diagnostic, never a bar; the r1000/core-kill decomposition is a mandatory companion. As `PINCERPOOL`.
**PLANNED n: 5400 games** (15 maps × 2 seats × 180). ⭐ A FORECAST, not only a plan — P(reach) = 1.000 (D6).
**BOUNDARY: 5400 games** — LOCAL, one tape row = one game; DictReader over non-`#` lines, cross-checked against the heartbeat and `max(game id)+1`; `NOWINNER` rows counted in n, excluded from the numerator, reported. As `PINCERPOOL`.
**CUT-SHORT: floor 2700 games** for the bar verdict; below it, descriptive tallies only and NO bar verdict. Any `auto_gate` firing is an OPERATIONAL CANCELLATION typed `cancellation`, never a verdict; the COMBO-STOP carve-out and its four pre-committed conditions carry verbatim from `PINCERPOOL` §CUT-SHORT and are priced at P = 0.000 here.
**BAR: 51.33. MDE: 0.00pp** — POINT RULE only, licenses no effect-size exclusion (OB16). **BASE RATE: 50.00.**
**BAR SOURCE:** the house corefill futility band, `50 + 1.96×sqrt(0.25/5400)×100 = 51.3336`; naive per family convention; identical to the `SALTRAY`/`RINGLADDER`/`SIEGECREW`/`PINCERPOOL` rows, which is what makes the four subtractable. Constructed, not observed.
**BASE RATE SOURCE:** structural A/A expectation of a seat- and map-balanced self-play fixture whose control is the treatment's own ancestor chassis; calibrated by `results.tsv:idnull140-cert-5400` (49.27%) and `null125-final` (51.04%). ⚠ Weaker here than on any sibling — the refusing complement is 2 maps, not 5 or 7. As `PINCERPOOL` §BASE RATE SOURCE.
**REFERENCE n: none** — the comparator is a STRUCTURAL 50.00 generated inside this shard. The 6-map panel, the v524/v525 direction batteries and the n=90 full-pool arms are PRIORS (D5, D11), never reference samples and never bar comparators.
**TREATMENT TREE: bots/_v525flip**
**TREATMENT DIFF REFS: 5621ebac^ 5621ebac**
⚠ An ADD-commit intersects every path in the tree, so the git check is weak on its own; the load-bearing form is the CROSS-TREE diff against the parent — 90 doctrine + 15 siege lines vs `_v524exact`, with `eco.py`/`main.py`/`raid.py` byte-identical by `md5` (D1).
**MECHANISM METRIC READS: `bots/_v525flip/siege.py:489-497`** — `min_dim = FS_V525_MIN_MAP_DIM if LOKI_FS_V525 else FS_MIN_MAP_DIM` and the matching `min_dsq`, the runtime-read dim/dsq floors (change 2); and **`bots/_v525flip/siege.py:522-526`** — `crip_maps = FS_V525_CRIPPLE_MAPS if LOKI_FS_V525 else FS_V519_CRIPPLE_MAPS` / `if sig519 in crip_maps:`, the runtime-read cripple candidate set (change 1); both inside `_fs_map_gated` (`:480`), with `LOKI_FS_V525` at `bots/_v525flip/doctrine.py:4782` and `FS_V525_CRIPPLE_MAPS` at `:4786`. **TREATMENT DIFF TOUCHES: bots/_v525flip/siege.py bots/_v525flip/doctrine.py.** INTERSECTION: yes — both metric sites are NEW LINES in a file the diff touches. ⚠ A path-only intersection is REFUSED: `grep -c` over the control's four modules returns **0** for `LOKI_FS_V525 · FS_V525_CRIPPLE_MAPS · FS_V525_MIN_MAP_DIM · FS_V525_MIN_CORE_DSQ · _fs_map_gated · FS_MAP_SKIP`, and the control has no `siege.py` at all — the metric reads structurally 0 in the control and cannot read identically in both arms.
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_FS_V525=True, FS_V525_MIN_MAP_DIM=10, FS_V525_MIN_CORE_DSQ=32, FS_V525_LOG=False**, on top of the full v524 constant set declared in `PINCERPOOL` §METRIC WINDOW (carried unchanged, including `FS_V522_FLOOR=False`, `LOKI_FS_V524=True`, `FS_LOG=False`, `FS_DRAW_ON=False`, `NOISE_ON=True`). **MECHANISM CAN OCCUR IN WINDOW: yes** — none of the three v525 constants is a round gate: 10 is a board dimension, 32 a squared distance, and the third a switch. ⚠ `prereg_check` may warn OBLIGATION 17 PARTIAL WINDOW against them; those are checker artefacts (it reads every declared integer as a round), disclosed exactly as in `PINCERPOOL`.
**PRE-STATE: the predicted-change behaviour is NOT already in the target state at lock.** The control has no ferry, no collar, no map gate and no cripple list — `grep -c` returns 0 for every symbol above — so it plays the incumbent raid doctrine on all 15 maps and cannot already be standing down on two of them. The OUTCOME claim is likewise not pre-satisfied: `_v525flip`'s share against the incumbent on the 15-map pool **does not exist on any tape at any n** (`grep -ci flippool` → 0 on the worklist, `BARS.tsv`, `results.tsv`, `elo_history.tsv`, and no shard tape names `_v525flip`).
**PLANK CLASS: OFFENSIVE** — a siege package whose object is a core kill (ferry, pincer, collar, gated forward sentinel); the one home-side clause the family carried is dead at `main.py:1609`. The r300 admission read is registered anyway and is the falsifier most likely to fire (D12). As `PINCERPOOL` §PLANK CLASS.
**KILL-ROUND NON-REGRESSION: PRIMARY = ITT RMST₃₀₀, MDE +5.0 rounds**, scored as an exclusion on the 95% CI upper bound of (treatment − control); sized off `scratchpad/overnight/SIEGECREW.tsv`'s paired delta sd **77.48** ⇒ ±2.07 rounds at n=5,400 and ±2.92 at 2,700 — RESOLVES AT BOTH. Co-bar: ITT timely-kill-by-r300 must exclude a 3.0pp fall (paired diff sd 69.88pp ⇒ ±1.86pp / ±2.64pp; the 2,700 form is KNIFE-EDGE and re-tested against the sd recomputed from this tape). Third form, diagnostic only because it carries a collider: the kill-win-conditioned share and median. Zero-sum disclosure and the one-sided-backstop reading carry from `PINCERPOOL` §KILL-ROUND NON-REGRESSION.
**DOSE:** the s51 head's own firings, all measured PRE-LOCK on 6-map or n=60/90 fixtures in the shard's fired (silent) configuration, carried from `PINCERPOOL` §DOSE — v520's pincer at **+6.2 wins / +10.5 k200 / +9.2 k300, all outside their intervals at n=1,404 with the known-zero arm at zero**, PRESENCE and GUNNEAR nulled and shipped False, SYNC rejected, the v522 floor measured indifferent. **v525's own dose is the standdown selection itself, driven BOTH WAYS by `predicate_table.py`: standdowns treatment 2 vs mutant 5, and the maps admitted to the siege path 13 vs 10** (`LOKI_FS_V525 = False` reproducing the parent digit-for-digit); the v520 pincer's own both-ways counter carries too — NOBODY 22 vs 12.6 — and the deterministic replay-`cmp` (D11) shows IDENTICAL bytes on the three unaffected maps against DIFFERING bytes on all three flipped ones. ⛔ **THE DOSE IS NOT DECODABLE FROM THE SHARD** (`--replay /dev/null`, stderr discarded, every log flag off; tape columns `ts shard game map seed seat winner cond turns`), so every dose number is pre-lock and the shard's 5,400 rows lend it none of their power. ⛔ **AND THE NOISE FLOOR BOUNDS ALL OF IT: the family's zero-dose cells have moved ±6pp at n=360** (`PINCERPOOL` §2.2).
**MAP SEGMENT: EXPECTED, AND COMPILED INTO THE BOT** — `siege.py:480-573` refuses on dimension, core d², `FS_MAP_SKIP`, or a grid-confirmed cripple signature; v525 narrows the last two selections (D2, D3). Per-map cells hold 360 games ⇒ ±5.17pp, so no single map cell carries a verdict; per-map/per-seat/class tables are DESCRIPTIVE.
**PRIMARY SEGMENT: REFUSING = {`archipelago`, `midgard`} (2 maps, 720 games, ±3.65pp) vs SIEGE-ACTIVE = the other thirteen (4,680 games, ±1.43pp)** — fixed BLIND before the first row, shard-native and exact. Exactly one primary; every other cut is DESCRIPTIVE (OB15b). Power and its cost: D7.
**EXPECTED DIRECTION: POSITIVE on SIEGE-ACTIVE (prior 72.58%); NULL (~50.0) on REFUSING; therefore POSITIVE pooled, prior 69.57%.**
**GATE RESOLUTION: four gates.** (a) the share bar — margin 1.33pp vs ±1.334pp at n=5,400 (±1.222 at the prior's p≈0.70), resolvable, and the prior sits 18.2pp clear; (b) the primary segment — ±3.65pp against a prediction of exactly 50.0, resolves a ~4pp discordance and nothing below n=2,700 (D7); (c) the r300 bar — resolves at both 5,400 and 2,700 on the primary, knife-edge on the co-bar at 2,700; (d) the operational floors — none binds, P(stop) = 0.000 (D6). **Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no drop conversation, no combination claim.**
**POOL ERA: post-2026-08-13-rotation** — the 15-map pool of `tools/overnight.sh:68` (n/a on a LOCAL surface per SPEC §6; declared because the rotation is load-bearing: the 6-map prior grid carries the retired `atoll`).
**SPANS-POOL-CHANGE: no.** **CELL VERSION CHURN: N/A** — not a panel, no `CELLS:` line, one fixed local control tree.

### D12. HYPOTHESIS, BAR, FALSIFIERS
**BAR: 51.33 ge** — unchanged, same derivation, same OB16 point-rule status
(`PINCERPOOL` §BAR / §BAR SOURCE). **PLANNED n: 5400. BASE RATE: 50.00.**
**HYPOTHESIS:** *the s51 head with the standdown flip — `LOKI_FS_V525` narrowing
the cripple candidate set to `midgard` alone and lowering the dim/dsq floors to
`fjordgate`'s own geometry, on the `_v524exact` base — produces a LOCAL pooled
game share of 51.33% or higher against `bots/_v488beltbreak2` at n = 5,400 across
all 15 maps and both seats, WITHOUT pushing our own kill past r300.*
**REGISTERED DIRECTION: POSITIVE, prior 69.57%, clearing the bar by 18.2pp
(13.6 half-widths).** ⛔ **As on `PINCERPOOL`, the decision bar is registered for
comparability and is not this page's question; the `SHIP_BAR` distance is, and
D4 says it is now 5.4pp.**
**FALSIFIERS: carried from `PINCERPOOL` §FALSIFIER unchanged** — primary
(CI upper < 51.33), second (r300 admission bar on ITT RMST₃₀₀, MDE +5.0 rounds,
co-bar ITT timely-kill excluding a 3.0pp fall, both sized off `SIEGECREW.tsv`'s
paired sds 77.48 and 69.88pp), third (majority-r1000 ⇒ `OFF-DOCTRINE
COMPOSITION`), segment (REFUSING at 50.0 ± 3.65pp), and mechanism.
⭐ **ONE FALSIFIER GAINS TEETH HERE AND IT IS NAMED: the second.** Three maps
that previously played the chassis now run a collar siege, and a collar spends
rounds. **The r300 bar is the most likely to fire on this arm** — as it was on
`PINCERPOOL`, and for a strictly larger reason.

---

## RATIFICATION BLOCKERS — only what is NEW
**B4, B5, B6 carry from `PINCERPOOL` unchanged.** B1, B2, B3 and B7 are spent
(resolved or discharged there). New:

**F1. ⛔ RULE ON THE THREE FLIPPED MAPS ENTERING ON n=60 EACH.** The flip moves
three maps — 1,080 of this shard's rows — into the siege-active segment on the
strength of a **±12.65pp per-arm direction read**, backed by a FORCEALL probe
that measures *forced* rush rather than rush *reached through the real gate*.
**Two branches:** (i) **fire as drafted**, registering the flipped cell as a
PRIOR and letting the shard's 1,080 rows settle it at ±3.0pp; (ii) **pool a
larger pre-lock read on the three maps first**, which costs a battery and delays
the shard. *(Drafter's recommendation: **(i)**. The shard is the powered
instrument and it resolves these three cells an order of magnitude better than
any pre-lock battery would; a pre-lock re-read would answer the same question
worse and later. The registration already labels the cell a prior.)*

**F2. ⛔ RULE ON THE HALVED PRIMARY-SEGMENT POWER (D7).** The refusing segment
falls to 720 rows / ±3.65pp, and the chassis-equivalence question is answered
more weakly than the parent tree would have answered it. **Two branches:**
(i) **accept it** — the rows moved to where the plank runs, which is what the
flip is for; (ii) **register the GATED and CRIPPLE cells as reported-only** and
drop the segment falsifier's blocking status. *(Drafter's recommendation:
**(i)**, keeping the falsifier blocking. A weaker gate that still blocks is
worth more than a strong-sounding one that does not, and ±3.65pp still catches
the ~20pp discordance the family has actually seen.)*

---

**PROVENANCE: docs/prereg/PREREG-PINCERPOOL-2026-08-18.md (the parent — structure, estimator, floors, cluster/DEFF, lying-fixture, stealth scope, carve-outs, falsifiers and bands all incorporated BY REFERENCE) · docs/research/BUILD-REPORT-v525flip-2026-08-18.md · bots/_v525flip/{doctrine,siege}.py (the two selections, read at draft) · scratchpad/s51_forceall/results.tsv (the FORCEALL basis, via the doctrine block) · docs/prereg/BARS.tsv · PROGRAMME.md (SHIP_BAR :30,:34-47 · STEALTH_UNTIL_DROP :31,:42-47 · KILL_TARGET :32,:49-59) · scratchpad/overnight/SIEGECREW.tsv (the trio-overstatement ratio and the r300 sds) · scratchpad/corefill_work.txt · tools/auto_gate.py · tools/overnight.sh · maps/**
*Verified directly at draft: `md5`/`wc -l`/`git ls-files`/`git status --porcelain`/`git log --diff-filter=A` on `bots/_v525flip`, the `diff` against `bots/_v524exact` (90 doctrine + 15 siege lines, three modules byte-identical), the four seed surfaces, and the Monte Carlo re-run at this band's floor and ceiling.*

---

## READY-TO-PASTE ROWS — ⛔ FOR THE BUILDER, AT LOCK
⛔ **`BARS.tsv` row BEFORE the worklist row, and the append is not done until the
row is grepped back out in the same shell call** (`BARS.tsv` header idiom).

### 1. `docs/prereg/BARS.tsv` — four tab-separated columns
```
FLIPPOOL	51.33	ge	docs/prereg/PREREG-FLIPPOOL-2026-08-18.md — DECISION bar 51.33 ge, POINT RULE (OB16, MDE 0.00; 50 + 1.96*sqrt(0.25/5400) = 51.3336), n=5400, h2h share, LOCAL SAME-HOST (one box, 8 in-process workers) seeds 878000-878337. Locked <TS> PRE-START by the builder (s51). ⛔ COMPACT SIBLING OF PINCERPOOL: docs/prereg/PREREG-PINCERPOOL-2026-08-18.md is the PARENT and everything not listed as a DELTA is incorporated BY REFERENCE and NOT restated — estimator, CLUSTER UNIT none + the five-candidate enumeration, local DEFF 0.98 naive intervals, BOUNDARY/CUT-SHORT + the COMBO-STOP carve-out, BAR SOURCE + BASE RATE SOURCE, the operational floors and GATE RESOLUTION (a)-(d), the one-draw law and measured --seed non-reproducibility, FIRINGS F2-F5 with their alarm proxies and stop rules, the LYING-FIXTURE caveat, the STEALTH_UNTIL_DROP scope, CANCEL-FOR-CAPACITY, the falsifier set, the honest-null clause and the five reading bands, and blockers B4/B5/B6. ⛔⛔ AND TWO DISCLOSED DEVIATIONS: (1) NOT DRAFTED BY A FRESH AGENT — the fresh-drafter rule was set aside on MAGNUS'S TOKEN-CONSERVATION DIRECTIVE and the PINCERPOOL drafter was RESUMED, so this page INHERITS that page's method, priors and blind spots instead of independently checking them; (2) it is incorporation by reference, so a reader who has not read PINCERPOOL has not read this registration. TREATMENT bots/_v525flip (commit 5621ebac; doctrine 6cb12ea45935aba347dcfba534686e9c / siege e7d3fc5c44c6058331b7bebcf8dd004f; eco+main+raid BYTE-IDENTICAL to _v524exact by md5; whole delta 90 doctrine + 15 siege lines — smaller than v524's, itself the smallest this family had fired; ⚠ the build report's ARTIFACTS line calls the tree 'uncommitted' and that is STALE) vs CONTROL bots/_v488beltbreak2 (997bcd42, unchanged) = the PROGRAMME INCUMBENT = Sleipnir v2 = SHIP_BAR's NAMED DENOMINATOR; SELF-LEG. THE CHANGE: LOKI_FS_V525=True (doctrine.py:4782), TWO SELECTIONS ON ONE FLAG, both read AT RUNTIME inside _fs_map_gated and never at module scope (the append-ordering hazard v515/v524 document) — CHANGE 1 drops yulerune's signature from the cripple CANDIDATE set (FS_V525_CRIPPLE_MAPS, :4786, midgard's signature only, consumed at siege.py:522-526), so yulerune AND frostgate never reach the CRIPPLE test; CHANGE 2 lowers FS_V525_MIN_MAP_DIM 12->10 (:4792) and FS_V525_MIN_CORE_DSQ 72->32 (:4793), consumed at siege.py:489-497, un-gating antler and fjordgate. ⭐ CHANGE 2 IS A THRESHOLD CHANGE, NOT A REMOVAL, AND THE FLOORS ARE fjordgate's OWN GEOMETRY (10x10, core d^2=32 — the binding map on both axes), so a 9x9 or any closer-cored board is STILL REFUSED and the strict < admits fjordgate exactly at its own boundary; archipelago is untouched because it is refused by FS_MAP_SKIP, a different closure-based mechanism. BASIS — the one genuinely new evidence on the page rather than a re-weighting: Magnus's ask ('could we test it on all maps and check if it performs better than we thought?') answered by the FORCEALL probe (scratchpad/s51_forceall/results.tsv, n=90/map, forced rush with every threshold zeroed at the definition site, vs bots/_v488beltbreak2): yulerune 91.1% [+-5.9], antler 64.4%, fjordgate 63.3%, midgard 40.0% (STAYS cripple), archipelago 17.8% (STAYS gated). ⇒ THE STANDDOWNS WERE STALE-CALIBRATED (gates are v510-era thresholds, the cripple list a v513-era read, and the rush has since gained pincer/funding/door-off/terminal-hop): three of five standdowns fail their own re-measurement and two survive it. SEGMENTS, computed against v525's predicate and INDEPENDENTLY ASSERTED BOTH WAYS by the build's predicate_table.py (which imports the real _fs_map_gated and monkeypatches only the flag): GATED {archipelago} 1/15, CRIPPLE {midgard} 1/15, SIEGE-ACTIVE 13/15 — REFUSING 2 of 15 = 13.33% (was 33.33% under v524, 46.67% under v522); LOKI_FS_V525=False re-selects the parent's five standdowns digit-for-digit. ⭐⭐ SHIP_BAR ARITHMETIC, THE HEADLINE: pooled = 0.1333*refusing + 0.8667*S, so the 75 FLOOR needs S = 78.85% (was 87.50 under v524, 96.88 under v522) and the 80 TARGET needs S = 84.62% (was 95.00; ARITHMETICALLY IMPOSSIBLE under v522); max pooled with a perfect segment is 93.33%. THE REGISTERED PRIOR IS 5.4pp FROM THE DROP FLOOR AND THE REQUIRED S IS BELOW THE 82.22% THE THREE POWERED MAPS ALREADY READ — the first page in this family on which the SHIP_BAR floor is not obviously out of reach, and an arithmetic statement about a composition prior, NOT a measurement. ⭐ COMPOSITION PRIOR 69.57%, PINCERPOOL's cell-by-cell method with FOUR evidence classes, equal weight per map: S = (3*82.22 trio [n=540, the v522/v524 6-map KILL_TARGET panel, 180/map, fired config] + 2*63.33 v524-reclaimed [ragnarok+frostgate, n=120, the v524 direction battery, 60/map] + 3*78.33 v525-flipped [yulerune 58/60, antler 38/60, fjordgate 45/60, n=180, THIS build's direction read] + 5*67.05 unobserved [auroraveil/drumlin/icefloe/royale/valkyrie, n=0, trio x the v513-tape ratio 0.8155 per PINCERPOOL 2.3])/13 = 72.58; pooled = 0.0667*50 + 0.0667*50 + 0.8667*72.58 = 69.57. MAP-COMPOSITION BAND 66.32-78.59 (F unobserved at v513's raw 57.28 -> 66.32; E flipped regress to their FORCEALL basis -> 68.49; G refusing drifts to 45 -> 68.91; D REGISTERED 69.57; H midgard at its own measured 57.78 -> 70.09; B unobserved at the trio -> 74.63; A flat -> 77.93; I optimistic -> 78.59). SAMPLING band 65.70-74.45. SEGMENT VALUE CEILING = 86.67% x 77.06pp = 66.78pp, refusing complement at most 7.67pp ⇒ POOLED CEILING 74.45pp — the first arm in this family whose ceiling is within 0.6pp of the SHIP_BAR floor; companion floor 65.70pp. ⛔ TWO DISCLOSURES PULLING OPPOSITE WAYS, BOTH PRE-FIRE: (a) the FLIPPED cell is the shakiest of the four and is 3/13 of the segment — n=60/map (+-12.65pp per arm), and against their FORCEALL basis the three run +5.6/-1.1/+11.7pp, all inside the band but fjordgate's at its edge, which the build report says itself; registered as a PRIOR, not evidence. (b) SCENARIO H is the one place a measured cell disagrees with the registered structural value: with yulerune flipped out the cripple cell is midgard ALONE and its own panel read is 104/180 = 57.78% [50.56,65.00], where PINCERPOOL could register 50.00 because structure and its two-cell measurement coincided at exactly 180/360. THIS PAGE KEEPS 50.00 — the refusing segment is the PRIMARY, 50.0 is its registered prediction, one map at n=180 sitting 1.1 half-widths high does not move a prior, and the family's own zero-dose noise floor on these cells is ~+-6pp. Worth +0.52pp if it holds. ⭐ P(COMPLETION) = 1.000 AND THE MARGIN IS THE WIDEST YET: same Monte Carlo and same clauses as PINCERPOOL section 3 (20k trials/row, CATASTROPHE on the running tape from n>=400, TREND-FLOOR on BOTH the 1000 and 2700 prefixes, COMBO-BAR@2700, FUTILITY@2700), P(any stop) = 0.000 at every point in 65.70-78.59 verified at the band's own floor and ceiling; the clauses bite only below ~57%, now MORE THAN 9pp below the band floor (it was 4pp under PINCERPOOL). ⇒ the cost to price is WALL CLOCK (~2-6h, one box, 8 workers), not a lost shard; this arm will not stop itself; and ANY auto_gate firing is an INSTRUMENT ALARM demanding a per-segment tape inspection before any verdict. NO COMBO-BAR EXEMPTION CLAIMED; COMBO_BAR=55.0 binds at 2700 and is priced at 0.000. ⚠⚠ PRIMARY SEGMENT = REFUSING {archipelago, midgard} (2 maps, 720 games, +-3.65pp at p=0.5) vs SIEGE-ACTIVE (13 maps, 4680 games, +-1.43pp); REFUSING must read 50.0 +- 3.65pp or the reading is ATTRIBUTION UNRESOLVED EVEN IF THE BAR CLEARS. THE FLIP HALVES THIS GATE'S POWER AND THAT IS THE PAGE'S CLEAREST TRADE-OFF: across three shards the refusing segment has gone 2520 rows (+-1.95pp) -> 1800 (+-2.31pp) -> 720 (+-3.65pp), so the chassis-equivalence question the family has chased since SIEGECREW's 28.71% gets a WEAKER answer here than the parent tree would have given — the right trade, since the rows moved to where the plank actually runs, but a real cost, registered rather than mentioned. Sub-split GATED 360 games +-5.17pp, CRIPPLE 360 +-5.17pp. FIRINGS: F2-F5 carry from PINCERPOOL with two substitutions — F1 re-read against v525's predicate (GATED 1 / CRIPPLE 1 / SIEGE-ACTIVE 13, asserted both ways by predicate_table.py), and F3 THE ZERO-DOSE PLACEBO LOSES HALF ITS CELLS (now midgard alone, 104/180 = 57.78% on the fired-config panel; STOP RULE RE-SIZED to a CRIPPLE cell outside [42.3,57.7] at n=360, and note that the registered structural 50.00 and the observed 57.78 straddle that rule's upper edge — it is read against the shard's own 360 rows, not the panel's). F5's denominator is this build's: 0 tracebacks across 387 replays by recursive Traceback grep over every .err/log in scratchpad/s51_v525_build — builder-declared absence, NOT upgraded to a measurement, and not re-readable on the shard. ⭐ THE FLIP'S OWN BOTH-WAYS CONTROLS ARE THE STRONGEST INSTRUMENT HERE: deterministic replay-byte cmp (NOISE_ON=False both sides, --tle 0, seed 525919, both seats) reads IDENTICAL on the three maps this build must not touch (drakkarfjord siege-active, midgard cripple, archipelago gated — 6/6 cells) and DIFFERS on all three flipped maps (6/6), n = 1 seed x 2 seats x 6 maps so it establishes the code paths and not the outcomes; siege-path confirmation on an instrumented FS_LOG=True copy shows every FS GATE line reading ok 1 with the right signature and SEAL/SENTINEL/THROW/EVICT/RUNG/PHASE all firing on all three flipped maps, so the plank GENUINELY RUNS where the flip admits it rather than the trees differing by coincidence; the AST derived-default scan reads 0 v525 hits and 0 on every inherited flag set with its guard driven both ways plus a real-case positive control at 2 hits (scope doctrine.py only, matching the v524 precedent). ⛔ THE FLAG-OFF BEHAVIOURAL CHECK IS 'NO DRAMATIC SPLIT', NOT EQUIVALENCE, and this page carries no byte-for-byte claim for it: flag-off 62/90 (68.9%) vs the true parent _v524exact 58/90 (64.4%), delta +4.5pp, well inside n=90 noise. ⭐ IT IS ALSO A SECOND FULL-POOL ANCHOR POINTING HIGH — the parent reads 64.4% and the flag-off arm 68.9% on the full 15-map pool at n=90 against PINCERPOOL's registered 63.91 for that same parent configuration — REGISTERED AND NOT USED TO MOVE THIS PAGE'S PRIOR, for the reasons in PINCERPOOL 2.4a (n=90, +-9.7pp, fired to test equivalence rather than to estimate a share). ⭐ KILL_TARGET PANEL RECOMPUTED AT THE NEW WEIGHTS and registered as a mandatory companion read: 6-map median kill 193 / ITT k200 31.5% / k300 45.6% and this control's own full-pool profile median 261 / 12.81% / 26.25% ⇒ FULL-POOL PREDICTION median 195-235 (the r180 target still NOT met), k200 29-38%, k300 41-47%, derived from the v525 segment weights, the trio-overstatement ratios 0.654/0.704 off SIEGECREW.tsv, and midgard's own panel cells (k200 14.4%, k300 35.0%). Every mark moves toward the KILL_TARGET versus PINCERPOOL (median 215-255 -> 195-235, k200 25-32% -> 29-38%) purely because 86.67% of the pool now runs the plank; ⚠ yulerune's FORCEALL median kill of 109 is the fastest cell measured anywhere in this line and is 1/15 of this shard, so a median below 195 is a COMPOSITION effect and that cell is the first place to look, not a speed-up. FALSIFIERS carry from PINCERPOOL unchanged (primary CI-upper < 51.33; the r300 admission bar on ITT RMST300 with MDE +5.0 rounds and the ITT timely-kill co-bar excluding a 3.0pp fall, both sized off SIEGECREW.tsv's paired sds 77.48 and 69.88pp; the majority-r1000 OFF-DOCTRINE downgrade; the segment falsifier at +-3.65pp; and the mechanism falsifier) — ⭐ AND ONE GAINS TEETH HERE: THE SECOND. Three maps that previously played the chassis now run a COLLAR SIEGE, and a collar spends rounds, so the r300 bar is the most likely to fire on this arm, for a strictly larger reason than on PINCERPOOL. NEW BLOCKERS: F1 rule on the three flipped maps entering on n=60 each (1080 rows on a +-12.65pp per-arm read backed by a probe that measures FORCED rush rather than rush reached through the real gate) — drafter recommends firing as drafted, since the shard resolves those cells at +-3.0pp and a pre-lock re-read answers the same question worse and later; F2 rule on the halved primary-segment power — drafter recommends accepting it and KEEPING the falsifier blocking, since a weaker gate that still blocks beats a strong-sounding one that does not and +-3.65pp still catches the ~20pp discordance the family has actually seen. B4/B5/B6 carry from PINCERPOOL; B1/B2/B3/B7 are spent there.
```

### 2. `scratchpad/corefill_work.txt` — five tab-separated fields, appended AFTER the BARS row
```
FLIPPOOL	bots/_v525flip	bots/_v488beltbreak2	5400	878000
```
⛔ **Exactly five fields** (`corefill.sh:142` / `worker.sh` G4 read
`read -r SH TR CT TG SL`; a sixth lands inside `$SL`).

---

## RATIFICATION (builder s51 — the lane types this)
**F1 — RULED:** _(builder)_
**F2 — RULED:** _(builder)_
**B4 / B5 / B6 — CONFIRMED as carried from `PINCERPOOL`:** _(builder)_

**RATIFIED AND LOCKED by the builder s51. Drafted by the RESUMED `PINCERPOOL`
agent under Magnus's token-conservation directive — the fresh-drafter rule was
deliberately set aside and the loss of independence is disclosed at the top of
this page. Lock commit = this commit (clock 1); shard creation follows (clock 2,
the tape's own `# FIXTURE … start=` stamp).**

---
## RATIFICATION (builder s51)
**F1 RULED: fire as drafted** — the n=60/forced-probe cells enter as PRIORS; this shard IS
their powered, real-gate test (that is its purpose, not a defect). **F2 RULED: the refusing-
segment power loss (720 rows, ±3.65pp) is ACCEPTED** — the chassis-equivalence question is
already answered at power by PINCERPOOL's concurrent 2,520-row segments; this page buys the
rush read. Both drafter deviations (resumed-not-fresh under Magnus's token directive;
by-reference construction) stand disclosed. Scenario H's 50.00 registration kept.
**RATIFIED AND LOCKED by the builder s51. Lock commit = this commit (clock 1); shard follows.**
