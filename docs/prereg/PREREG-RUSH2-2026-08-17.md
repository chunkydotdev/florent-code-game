# SCREEN PREREG — `RUSH2`: the LOKI-2 COMMITTED OPENING re-priced on the Sleipnir chassis (`LOKI2_RUSH_ON` False → True, one boolean)

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent appended no worklist row, appended no
`BARS.tsv` row, fired no game, started no shard, and touched neither
`results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor `QUEUE.md`. It DID create
one tree — `bots/_v490rush2` — as specified in its brief, and `git add -N`'d its
four files (see LOCK, clock 1) so Obligation 13's intersection is computable; no
commit was made.

**STATUS: drafted BEFORE the `RUSH2` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any `docs/prereg/BARS.tsv` row exists for
it, BEFORE any file named `scratchpad/overnight/RUSH2*` exists, and BEFORE the
leg's first game.** Verified at draft, all four greps returning **0**:
`grep -c RUSH2 scratchpad/corefill_work.txt` → **0** ·
same grep on `docs/prereg/BARS.tsv` → **0** ·
same grep on `scratchpad/fleet_queue.tsv` → **0** ·
`ls scratchpad/overnight/ | grep -ci RUSH2` → **0**.

### LOCK, clock 1
Drafting session wall clock at write time **`2026-08-17T08:03:33Z`** (`date -u`,
same shell call). Repo HEAD at draft **`d226b851`** (author time
`2026-08-17T10:00:20+02:00`). The treatment tree `bots/_v490rush2` was created by
this agent at **`2026-08-17T07:59:56Z`** (`cp` mtime, same shell session as the
`date -u` above) and is **INTENT-TO-ADD, NOT COMMITTED**: `git add -N` on the
four `.py` files, so `git ls-files bots/_v490rush2` returns all four and
`git diff --name-only HEAD -- bots/_v490rush2` returns all four. **This was done
deliberately and it is disclosed rather than left for a certifier to trip on:**
`tools/prereg_check.py`'s `untracked_arm_paths` FAILs (`OB13_UNTRACKED_ARM`) on a
tree that exists on disk and is invisible to git, and its own remedy text is
*"`git add -N` the tree (or commit it) before firing"*. The builder's lock commit
is what makes it tracked for real.

### LOCK, clock 2 (local shard)
Per the obligations doc's **Addendum of 2026-08-17T07:24:55Z**, which replaced the
boilerplate eleven preregs copied, and cited rather than restated here:
* **PRIMARY:** the `RUSH2.tsv` tape's own `# FIXTURE … start=` stamp
  (`tools/overnight.sh:99` sets `START=$(date -u …)`, `:103` writes it to the tape
  before the first `fcode run`). Quote it verbatim beside the lock commit's git
  author time.
* **BACKSTOP, if the tape carries no `# FIXTURE` line** (every REMOTE tape —
  0 of 86 carry it — and every local tape from before the stamp landed): the
  tape's **FIRST COMPLETED ROW `ts`**, which is CONSERVATIVE BY CONSTRUCTION (the
  true start is strictly earlier, so the gap can only be OVERSTATED).
* **SECOND BACKSTOP, serial runners:** the `COMPLETE` time of the preceding shard
  on the same worker.
* ⛔ **NOT AVAILABLE: the heartbeat's `STARTING` line** — `overnight.sh:100` and
  every later state write with `>`, so the start time is destroyed by the first
  progress update.
**Name which of the three you used.** This arm is REGISTERED LOCAL (see
`GATE RESOLUTION`), so the primary form is expected to be available.

---

## ⛔⛔ READ BEFORE RATIFYING — EIGHT THINGS THE LANE OWNS, AND THREE OF THEM ARE REASONS TO ARGUE WITH THIS DRAFT

### 1. ⛔⛔ THIS EXACT ONE-BOOLEAN ARM ALREADY RAN YESTERDAY, ON THE POST-ROTATION POOL, AND THE BRIEF DID NOT NAME IT. `RUSH2` IS A **RE-BASE**, NOT A FIRST MEASUREMENT.

Found at draft and it changes what this page can claim. `docs/prereg/BARS.tsv:272`
carries **`RUSH72`**, registered `2026-08-16T07:16:24Z`, described in its own
source column as *"QUEUE #72 reopen-and-re-measure of `LOKI2_RUSH_ON` (one-flag
arm `_v460rush`) on the post-rotation pool"*. Verified at draft:

* **`bots/_v460rush` IS the same one-boolean arm on the PREVIOUS incumbent's
  chassis.** `diff -rq bots/_v460rush bots/_v223sealrepair` names `doctrine.py`
  only; the per-file changed-line counts are **doctrine.py 2 · eco.py 0 ·
  main.py 0 · raid.py 0**, and its `doctrine.py:1409` reads `LOKI2_RUSH_ON = True`
  with a QUEUE-#72 comment appended.
* **The tape exists and the leg was stopped.**
  `scratchpad/overnight/RUSH72.tsv` header: `# FIXTURE shard=RUSH72
  treatment=bots/_v460rush control=bots/_v223sealrepair planned_n=5400
  workers=8 host=MacBook-Pro start=2026-08-16T08:21:46Z`, **1,116 non-`#` lines**
  (one is the column header ⇒ 1,115 data rows).
* **The result, verbatim off `results.tsv:rush72-autostop-1000`:**
  **50.18% [47.24, 53.12] at n=1112**, `cancellation`, *"AUTO-STOP RUSH72 at
  MARK-1000 n=1112 on 2026-08-16T09:17:53Z by tools/auto_gate.py --apply"*, clause
  **TREND-FLOOR@1000**, prefix **50.40** against the 52.0 floor
  (`scratchpad/auto_gate_cancelled.tsv`, two rows CLAIM/DONE at 09:17:53Z).

⇒ **WHAT `RUSH2` ADDS OVER `RUSH72`, stated precisely, because everything else on
this page is worthless if this list is empty:**
1. **The CONTROL AND BASE MOVE TO THE LIVE INCUMBENT.** `RUSH72` answered *"does
   the flag help `_v223sealrepair`?"*. `PROGRAMME.md:8` now reads
   `INCUMBENT: bots/_v468kladturbo`, and *"when a ship lands, every control moves
   with it — a null belongs to its control"*. `RUSH72`'s number belongs to a
   retired chassis that does not contain turbo/bodyaware/samestop.
2. **`RUSH72` WAS NEVER PRICED.** Its CI `[47.24, 53.12]` **CONTAINS the 52.0
   floor it was stopped on**, which is precisely the class Magnus's s49 directive
   names (see #4): *unpriced, not refuted*. At n=1112 the half-width is **±2.91pp**
   and the arm was stopped for failing to clear a floor its own interval covered.
3. **NO MAP-CLASS SPLIT WAS EVER REGISTERED FOR THIS FLAG**, and the prior
   evidence says the effect is CONCENTRATED BY MAP. See #6.
⚠ **AND ONE THING `RUSH2` DOES NOT ADD:** it does not make the arm attributable.
See #2.
⭐ **A FREE READ THE BUILDER SHOULD TAKE BEFORE SPENDING A CORE, and it is named
here rather than registered as this leg's evidence:** `RUSH72.tsv`'s 1,115 rows
are on disk and can be class-split at zero cost (`tools/overnight_read.py` prints
CQ/STD/GRAND). At n≈1,112 the cells are ~148/~594/~371 games (±8.0/±4.0/±5.1pp),
so **that read can only shape a prior — it cannot resolve any class** and it is on
the retired chassis. It is worth ten seconds and it is not evidence for this page.

### 2. ⛔⛔ THE FLAG IS A **TWO-PLANK BUNDLE**, AND THIS HOUSE HAS ALREADY CUT THIS EXACT ARM FOR IT. THE ATTRIBUTION CEILING IS REGISTERED AS A HARD CEILING.

`LOKI2_RUSH_ON` has **two consumers**, both verified at draft by
`grep -rn LOKI2_RUSH bots/_v468kladturbo/*.py`:
* **(a) THE GATE WAIVER — `raid.py:673-675`.** `rush = LOKI2_RUSH_ON and
  ct.get_current_round() < LOKI2_RUSH_RND`, then `min_harv` swaps
  `LOKI_FWD_MIN_HARV 2 → LOKI2_RUSH_MIN_HARV 0` and `ti_floor` swaps
  `LOKI_FWD_TI_FLOOR 40 → LOKI2_RUSH_TI_FLOOR 8`.
* **(b) THE SEAT CHANGE — `main.py:447-448`.** `LOKI2_RUSH_ON and n in
  LOKI2_RUSH_SEATS and ct.get_current_round() < LOKI2_RUSH_RND` ⇒ `self.role =
  "raid"`, so seat **1** — a member of `LOKI_ECO_SEATS = (1, 2, 3)`
  (`doctrine.py:1209`) — **leaves the economy for the raid** inside the window.

**THE HOUSE RULING, verbatim off `scratchpad/corefill_work.txt:713`:**
> *"CUT `RUSHON` — a second consumer at main.py:324 makes it unreadable AT ANY n.
> ⭐ CONFOUNDING IS NOT A POWER PROBLEM, so no shard size fixes it. Right call."*

and, from the same file's queue note at `:650-659`: *"IT IS QUEUED FOR THE DOSE
AND THE COST, NOT FOR ATTRIBUTION. `MINHARV1` is the clean single-mechanism arm on
the same axis and is already running. **A result here NEVER licenses a sentence
about the rush gate on its own.**"*

⚠ **THE `main.py:324` ANCHOR IN THAT RULING IS STALE AND SO IS THE ONE IN THE
QUEUE ROW THAT PRODUCED THIS BRIEF** (the brief cited `main.py:336` /
`raid.py:656`). **On the Sleipnir tree the live sites are `main.py:447-448` and
`raid.py:673-675`, read personally at draft and quoted above.** Cite those. The
stale anchors are recorded here so the next reader does not chase them.

**REGISTERED CONSEQUENCE, pre-committed so it cannot be softened at readout:**
> **`RUSH2` measures THE FLAG — a two-plank bundle that would SHIP as one boolean
> — and nothing finer. No sentence in any readout, wrap, `results.tsv` row or
> `QUEUE.md` row may attribute this arm's result to the harvester prerequisite, to
> the bank floor, or to the seat change, in either direction. A number that cannot
> be split does not become splittable because the shard was large.**

**AND THE SHIPPABILITY DEFENCE, so the ceiling is not read as futility:** the
question *"is the bundle, as we would ship it, better or worse than the incumbent
on the currency the ladder pays?"* is a legitimate and complete question. It is
just not the question *"is the eco clock the kill clock?"*, which is the one the
brief's motivation actually poses. **The clean arm for THAT question is a
one-line `LOKI_FWD_MIN_HARV 2 → 1` (or `→ 0`) and/or `LOKI_FWD_TI_FLOOR 40 → 8`
flip on the Sleipnir base — the `MINHARV1` design re-based** — and it is NOT this
page. Its banked dose on the old chassis is in #7.

### 3. THE ADVERSE EVIDENCE, BOTH HALVES, AND THE HONEST FRAME

**AGAINST.** `bots/_v468kladturbo/doctrine.py:1395-1408` — the comment block that
switched this flag off — records, measured 2026-08-09, paired deterministic,
**360 games, 0 tracebacks, gate CLEARED 12/12**, against the two probes with
headroom (the saturated ones cannot measure anything — clanker 96.7%, ouroboros
93.3%):

| opponent | band | delta on `core_kill_share` | sign test |
|---|---|---:|---:|
| `orizon_probe` | ALL | **−15.6pp** | **p = 0.0201** |
| | SHORT | **−35.4pp** | **p = 0.0005** |
| | LONG | +7.1pp | p = 0.51 (null) |
| `cad_probe` | ALL | **−18.9pp** | **p = 0.0033** |
| | SHORT | **−22.9pp** | **p = 0.0192** |
| | LONG | −14.3pp | p = 0.15 (null) |

and the author's own note that **they predicted the opposite** — help on SHORT,
harm on LONG — *"and the harm is concentrated exactly where I predicted benefit."*
Corroborated the same day on the real engine with real TLE enforcement
(`fcode match test dfc4b892`, `_v120loki4` rush-OFF vs `_v118loki2b` rush-ON):
**4–1 for rush OFF, all five games `core_destroyed`** — and the source doc itself
prices that honestly at **binomial p = 0.1875 one-sided, NOT significant, n=5,
corroboration not proof**. The same doc's CALIBRATION ADDENDUM supplies a sourced
self-play deflator (one published competitor measured the same amputation at ~30%
in self-play vs ~15% on a real field, ~2×, same sign) and instructs: carry
**≈ −8pp / ≈ −9pp**, not −15.6/−18.9. **The sign is what replicates; the magnitude
is what inflates.**

**⛔ AND THE SUPPOSED LIVE COUNTER-EVIDENCE DOES NOT SURVIVE ITS OWN SECOND
LOOK — stated here because it is the single most tempting thing on this page to
quote and it is dead.** The worklist row that queued `RUSHON` cites *"LOKI-11
live-unrated **+16.0pp** core-kill share"* as the opposite-signed result
(`docs/coordination.md:39853`). **`docs/coordination.md:26739` and `:27352` record
what happened when its n doubled: `+16.0pp` at n=25 → **`+0.0pp`** at n=50.** The
verbatim reading in this repo's own words is *"a sampling artefact regresses toward
zero as n grows; a real effect holds its point estimate"* — and this one did not
hold. **⇒ There is NO live-fixture positive for this flag. Anyone who reads
"tested twice with OPPOSITE signs" as "one arena negative against one live
positive" has read a retracted number.**

**FOR RE-TESTING ANYWAY — three reasons, each with its own limit named.**
1. **THE FIXTURE THAT CLOSED THE ROAD CANNOT CLOSE ROADS.** `CLAUDE.md` point 6:
   arena batteries, corpus statistics, source reads and engine probes may
   **PRIORITISE** a road, never **RETIRE** one; only live-game evidence closes.
   And `bots/*_probe` lies in a measured direction — five probes share a
   `best_core or best_any` short-circuit, and **zero of our forward turrets died in
   480 arena games against 46.9% on the ladder**, which is exactly the quantity a
   plank about planting forward weapons EARLIER depends on. ⚠ **LIMIT: this is an
   argument about ADMISSIBILITY, not about correctness.** It does not make the
   arena numbers wrong; it makes them non-terminal.
2. **THE POOL AND THE CHASSIS BOTH MOVED.** The 2026-08-09 battery ran on the
   pre-rotation pool; `tools/overnight.sh:68` has run a 15-map pool since the
   2026-08-13 rotation, and 5 of those 15 are a size class (area 900) the line had
   never played. The chassis moved further: `_v118loki2b` → `_v223sealrepair` →
   `_v468kladturbo` (turbo + bodyaware + samestop). ⚠ **LIMIT, AND IT IS THE ONE
   THIS SESSION HAS ALREADY BEEN BURNED BY: "the maps changed" is a reason the old
   result may not TRANSFER. It is NOT a reason the old result was WRONG.** A
   version comparison spanning the rotation produced a phantom regression on
   2026-08-17 that had to be retracted; this page does not repeat that move and no
   band below reads a class difference as evidence that 2026-08-09 was mistaken.
3. **THE CURRENCY MOVED.** That study's metric was `core_kill_share`.
   `PROGRAMME.md:11` reads `PRIMARY_CURRENCY: game_share`, `:16`
   `WIN_RATE_IS_VERDICT: yes`, and `:19` `R1000_IS_DEFEAT: yes`. A −15.6pp
   `core_kill_share` result is not a `game_share` result, and this leg is the first
   time the flag is scored in the currency the ladder pays against the live
   control. ⚠ **LIMIT: the two are correlated, not orthogonal.** A plank that
   loses 16pp of core-kill share is not a promising `game_share` candidate, and
   this page predicts accordingly (see the pre-committed reading).

**THE HONEST ONE-SENTENCE FRAME, and every readout sentence must be consistent
with it:** *the road was closed by a fixture that cannot close roads, on a metric
we no longer score, on a map pool and a chassis that no longer exist — and 360
paired games with replication across two independent unsaturated fixtures and four
sign tests at p ≤ 0.02 is real evidence about SOMETHING.* **Not "the old result
was wrong."**

### 4. ⭐⭐ THE s49 MAGNUS DIRECTIVE — GIVEN 14 MINUTES BEFORE THIS DRAFT — **SUPERSEDES PART OF THE BRIEF THAT PRODUCED THIS PAGE**, AND THE PAGE FOLLOWS THE DIRECTIVE.

`docs/coordination.md`, entry `2026-08-17T08:14:52Z`, committed as HEAD
`d226b851` (author `2026-08-17T10:00:20+02:00`). Verbatim:
> *"No, you don't give up on these arms, they are solid, we just need to figure
> out how to make them work, you May propose new arms, but until i approve you
> just continue iterating on the ones we have"*

Operational form recorded in the same entry: **(1) A STOP IS A DOSE/MECHANISM
DIAGNOSIS, NEVER A CLOSURE** — the question on a stop is *which of dose / funding /
siting / timing / instrument failed to land*, and the answer becomes the next
iteration of the same plank. **(2)** Of the five arms that stopped yesterday,
**three stopped with the CI CONTAINING THE FLOOR** — unpriced, not refuted — so
*"iterate, do not close"* is the better-CALIBRATED policy given the width of our
own intervals, not a softer one. **`RUSH72` is a fourth instance of exactly that
shape** (see #1).

⛔ **THE COLLISION, AND IT IS NAMED RATHER THAN QUIETLY RESOLVED.** The drafting
brief instructed: *"pre-commit what a catastrophe stop MEANS: it would be the
first non-probe evidence against the plank … A fast negative is a GOOD outcome
for this arm — it closes a road cheaply … Register that, so a negative cannot be
re-framed as a failure later."* **The directive above forbids the "closes a road"
half of that sentence.** ⇒ **REGISTERED RESOLUTION: the CHEAPNESS clause is kept
and the CLOSURE clause is struck.**
> **A fast stop on this arm is a GOOD and CHEAP outcome and may never be
> re-framed later as a failure of the leg. It is ALSO not a closure of the plank:
> per the s49 directive a stop is a dose/mechanism diagnosis, and the diagnosis
> this leg is instrumented to deliver is which of the four named candidates
> (dose · funding · window-vs-approach · the seat cost) failed to land. The
> falsifier below is written in exactly those terms.**

**AND ONE ADMINISTRATIVE FACT THE RATIFIER NEEDS:** the same entry lists the board
as **"BOARD UNCHANGED, ALL FOUR STILL OUT: OPENFAST (prereg) · BELTBREAK2 (build)
· ECOMMIT3 (build) · **RUSH2 (prereg)**"** ⇒ **`RUSH2` is an arm already on the
s49 board and is therefore inside *"continue iterating on the ones we have"*, not
a new arm requiring Magnus's approval.** If the builder reads it otherwise, this
page does not fire and that is the builder's call, not this draft's.

### 5. ⛔⛔ SOLO OR COMBO — **THE MACHINERY WILL SCORE THIS ARM AS A COMBO, AND THE BRIEF'S QUESTION HAS A MEASURED ANSWER THAT IS NOT THE OBVIOUS ONE.**

The brief asked which of the 52.0 trend floor and the 55.0 combo bar binds, and
warned that getting it wrong judges the arm against the wrong number. **Read off
the tool, not off intuition:**
* `tools/auto_gate.py:908` calls `combo_of(sh.treat)` — **the TREATMENT tree**;
  `:715-742` reads the marker `# ---- composed by tools/stack.py from: …` out of
  that tree's own `doctrine.py`.
* **`bots/_v468kladturbo/doctrine.py:1879` CARRIES that marker** (`turbo
  (_x3r0v152), bodyaware (_v242bodyaware), samestop (_v464samestop)`), and its own
  `:1884` comment says the literal phrasing is used on purpose because
  *"a hand-merge that reads as a SOLO would be scored against the wrong bar."*
* **`bots/_v490rush2` is a COPY of that tree, so it inherits the marker** —
  verified at draft, `grep -n "composed by tools/stack.py from:"
  bots/_v490rush2/doctrine.py` → **`1879`**.
* The same is true of **every arm on this base**: `_v480beltbreak`, `_v477ecommit`,
  `_v478freeround`, `_v479routescore`, `_v481sealsentAnofund` all return **1** on
  that grep (checked at draft).

⇒ **REGISTERED CLASSIFICATION: `RUSH2` is a COMBO arm as `tools/auto_gate.py`
computes it, so the bar that binds at the 2,700 prefix is `COMBO_BAR = 55.0`
(`auto_gate.py:278`, Magnus 2026-08-16), NOT the 52.0 house trend floor — and the
52.0 `TREND_FLOOR` still binds FIRST at the 1,000 prefix (`:261`, order is
load-bearing per `:902-906`: the milder claim wins where both would fire).**
**NO `COMBO-BAR-EXEMPT` TOKEN IS CLAIMED**, deliberately: `auto_gate.py:914-919`
grants the exemption only to a mechanism test scored against its own additive
prediction, and this arm is a PROSPECT against a house band. **A stop is a
CANCELLATION with rows KEPT, never a verdict** (`:277`).
⚠ **SUBSTANTIVELY the plank is a SOLO — one boolean, on a chassis that is itself a
composition, measured against that same composition as control, so 50.0 means
"the flag adds nothing".** The tool's classification and the plank's nature
disagree, and **the registration follows the TOOL**, because the tool is what
stops the shard. **This arm is therefore very likely to be cancelled at the 1,000
or 2,700 prefix.** That is priced in #8 and is not a defect of the design.

### 6. ⭐⭐ THE MAP DEPENDENCE IS REGISTERED **BEFORE THE DATA**, WITH CELL SIZES, AND IT IS THE DESIGN REQUIREMENT THE ADVERSE EVIDENCE CREATES.

The old harm was **concentrated on SHORT and null on LONG in both fixtures**. ⇒ **a
pooled result can hide the truth in either direction**: a pooled null is
consistent with a real positive on one class cancelling a real negative on
another, and a pooled positive could be one class carrying everything. The split
is registered here, with its arithmetic, so no band is chosen after the fact.

**THE HOUSE SPLIT IS `CQ` / `STD` / `GRAND`** — `tools/overnight_read.py:76-94`,
from each map's own `.map26` header, never a hardcoded size table: **CQ ≤ 260 ·
STD 261–676 · GRAND > 676**, printed with per-class n and ±pp at `:572-585` (rate
printed only at n ≥ 400 per class). **The pool is the 15 maps of
`tools/overnight.sh:68`.** Classified at draft, and the CORE-TO-CORE MANHATTAN
DISTANCE computed from the same map files (`tools/map_encode.parse_map26`) because
**approach length, not area, is the terrain property this mechanism names:**

| class | maps | n at 5,400 | ±pp (naive, DEFF 0.98) | core-to-core Manhattan |
|---|---|---:|---:|---|
| **CQ** | antler, fjordgate | **720** | **±3.62** | **8, 8** |
| **STD** | archipelago, auroraveil, drumlin, frostgate, icefloe, nordkap, royale, yulerune | **2880** | **±1.81** | 12–30 (median 15) |
| **GRAND** | drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie | **1800** | **±2.29** | 24–48 (median 44) |

**THE PROXY IS GOOD AND ITS ONE IMPURITY IS NAMED: area class is monotone in
approach length across the pool except for `icefloe` (STD, 30) sitting above
`glacierkeep`/`valkyrie` (GRAND, 24).** One crossing out of fifteen. A
mechanism-specific segment beats a size class (OB15a) — but the size class is what
the READING TOOL emits, and OB17 forbids registering a method the executing tool
cannot perform. ⇒ **the registered split is CQ/STD/GRAND, justified by the
distance table above rather than by size alone.**

**⭐ AND THE ARITHMETIC THAT MAKES THE PRIOR MECHANICAL RATHER THAN A STORY —
`LOKI2_RUSH_RND = 60` IS A WALL-CLOCK WINDOW AND THE APPROACH IS A WALK.** A
builder bot moves **1 cardinal tile per round** and **acting and moving are
mutually exclusive**, so a raider that also seals or pecks arrives strictly later
than `d` rounds after leaving. Our measured median forward arrival is **r31**
(`docs/research/FORWARD-ARRIVAL-BASELINE-2026-08-16.md`, pooled). Against the
table: CQ (d = 8) arrives deep inside the window; STD (d = 12–30) arrives inside
it; **GRAND's three long maps (d = 44, 48, 48) arrive AT OR AFTER r60** — i.e.
**the GATE-WAIVER half of the plank is close to structurally INERT on
midgard/ragnarok/drakkarfjord**, while **the SEAT half fires on every map**,
because the seat is issued when the unit first runs (`main.py:442-443`: *"the
window is read once, when this unit first runs"*) and that is early everywhere.

⇒ **THE PRE-STATED PRIOR, PER CLASS, WITH ITS MECHANISM. Registered before the
data exists; this is what makes a confirmation meaningful and a contradiction
interesting.**

| class | dose expected | pre-stated prior | mechanism reason |
|---|---|---|---|
| **CQ** (d = 8) | **maximal** — the waiver binds hardest, arrival is earliest | **NEGATIVE** | the 2026-08-09 SHORT band, deflated: **≈ −8 to −18pp**. On the shortest approach the tempo is already there, so the plank pays the economy and buys nothing it did not already have. |
| **STD** (d = 12–30) | partial | **NEGATIVE, WEAKER** | same mechanism, diluted: on the longer STD maps the economy has matured before arrival, so the waiver is a smaller change. |
| **GRAND** (d = 24–48) | **near-zero for the waiver, full for the seat** | **~NULL, and a NULL HERE IS AMBIGUOUS BY CONSTRUCTION** | the 2026-08-09 LONG band read null in both fixtures (p = 0.51, p = 0.15). Two mechanisms predict that null and this leg cannot separate them: (i) the waiver never fires because arrival ≥ r60, and (ii) the seat cost is free because on area-900 maps we are **rich and idle** — `PROGRAMME.md:180-181` measures **4,805 Ti banked, 21.6 buildings, 3/10 kills** at area 900 against 94 Ti / 27.2 buildings / 8/8 kills at ≤ 625. **F2 is what tells them apart** (does a forward plant land inside r60 on a GRAND map at all). |

**THE PRIMARY SEGMENT IS `CQ`, EXPECTED DIRECTION NEGATIVE** — see the
registration block. ⛔ **AND THE ONE THING THIS REGISTRATION DELIBERATELY DOES NOT
DO: it does not give the arm a second chance.** A segment declared with a NEGATIVE
expected direction cannot rescue a pooled fail — it can only confirm or refute the
prior. **OB15c's re-screen path is NOT invoked by this page, and no pooled fail may
be re-read as a pass on any cut.** That is the honest structure for a plank whose
prior is negative, and it closes the subgroup-fishing door completely rather than
leaving it ajar with a clause.
**UNDERPOWER, LABELLED IN ADVANCE:** at ±3.62pp the CQ cell **can** resolve the
prior's own effect size (≈ 8–18pp) but **cannot** resolve anything under ~4pp, and
**every CROSS-CLASS difference is a DIRECTION-ONLY read**: CQ−GRAND ±4.28pp,
CQ−STD ±4.04pp, GRAND−STD ±2.91pp. **No class difference smaller than those
half-widths may be stated as a finding**, and `NULL125`'s byte-identical A/A cell
is the reason the caution is not theoretical — it read **CQ 52.1 ± 3.7 / STD 50.4 ±
1.8 / GRAND 51.6 ± 2.3** at n = 5,400 with nothing changed
(`results.tsv:null125-final`). **A 2pp class spread is what this fixture produces
from identical bots.**

### 7. FIRINGS-BEFORE-PRIMARY IS A **HARD SEQUENCE**, AND THIS ARM'S MECHANISM IS CONDITIONAL ON A ROUND GATE, SO THE RULE BINDS AT FULL STRENGTH.

`docs/prereg/BARS.tsv:3-8` (research, adopted 2026-08-16T13:27:33Z): any arm whose
mechanism is CONDITIONAL registers a FIRINGS-PER-GAME read BEFORE its primary,
because *"'never fires' and 'fires but the metric cannot move' read identically."*
This arm's mechanism is gated on `round < 60` **and** on a live-target geometry
scan, so both failure modes are live.
> **F1, F2 and F3 below are RUN, and their numbers written down, BEFORE any
> sentence containing this arm's primary share is typed. A primary typed ahead of
> the firings read is a REGISTRATION BREACH regardless of what it says, and the
> repair is an amendment chain, not a re-write.**
> *(Precedent on the tape:
> `results.tsv:kladladder-verdict-amendment-f1f2-pending`.)*

**THE DOSE IS ALREADY BANKED ON AN OLDER CHASSIS, WHICH IS WHY F1/F2 ARE A
RE-CONFIRMATION AND NOT A DISCOVERY:** `docs/coordination.md:39858-39861` records,
for this exact flag on the `_v169launchlate160` chassis, **first forward sentinel
r27 → r18 (`_v179rushon`, p = 0.0003)**, against the clean single-mechanism arm's
**r22 (`_v180minharv1`, p = 0.097, inside the same-bot band)**. ⇒ **the flag has a
LARGE, SIGNIFICANT, MEASURED dose on the mechanism it claims, on a chassis two
ships old.** F2 asks whether it still does on Sleipnir, and whether it does so on
GRAND maps at all.

### 8. WHAT THIS LEG COSTS, AND THE MOST LIKELY OUTCOME, SAID BEFORE THE DATA

**COST: one LOCAL core, plus 60 serial games for F1/F2/F3.** ZERO rated ladder
exposure, zero submissions, zero unrated challenges, no activation — nothing on
this page touches the platform, which is why `TARGET BAND` is `N/A`.
**MOST LIKELY OUTCOME, stated so it cannot be presented later as a surprise: a
cancellation at the 1,000 or 2,700 prefix.** `RUSH72` stopped at 1,112 with 50.18%
on the previous chassis; the prior is negative; the binding prefix bars are 52.0 at
1,000 and 55.0 at 2,700 (#5). **A stop costs roughly one core-hour and is a
DIAGNOSIS (#4), not a closure.** ⛔ **AND A CATASTROPHE STOP (CI-hi < 45.0 at
n ≥ 400, `auto_gate.py:244,247`) IS A LIVE POSSIBILITY HERE, NOT A FORMALITY** —
this arm buys tempo with economy against an incumbent that beats its own
predecessor 61.09% [59.79, 62.39] (`results.tsv:kladturbo-local-confirm-5400`), and
the only prior direction on the currency is down. **It is registered as an
admissible, informative and CHEAP outcome, and it would be this plank's FIRST
evidence on a fixture whose verdicts this house accepts** — while remaining, per
#4, a diagnosis rather than a closure.

---

## RATIFY: Hypothesis

**HYPOTHESIS.** *Turning `LOKI2_RUSH_ON` on — the LOKI-2 committed opening, which
inside `round < 60` waives the forward-weapon harvester prerequisite
(`LOKI_FWD_MIN_HARV 2 → 0`) and cuts the bank floor (`LOKI_FWD_TI_FLOOR 40 → 8`)
AND sends seat 1 to the raid with seat 0 — raises our LOCAL pooled game share
against `bots/_v468kladturbo` to **51.33% or higher** at n = 5,400 games across all
15 corefill maps and both seats.* Registered direction **POSITIVE** (this is the
direction the flag's own doctrine block claims and the direction a KEEP requires);
**the pre-stated PRIOR is NEGATIVE and is registered as such in #3 and #6**, which
is the whole point of writing both down before the fire.

**PRIMARY BAR.** *Pooled local game share vs `bots/_v468kladturbo` ≥ **51.33%** at
n = 5,400.* **POINT RULE — MDE 0.00pp, licenses NO exclusion claim about an effect
size** (OB16 corollary).

**FALSIFIER (headline form; the full form is under `FALSIFIER`).** *At n = 5,400 the
95% CI upper bound on the pooled share falls BELOW 51.33.*

**SEGMENT / POPULATION.** *All 5,400 rows, 15 maps × 2 seats × 180, both seats
pooled for the primary; ONE primary segment — **CQ** (antler, fjordgate; n = 720),
**EXPECTED DIRECTION NEGATIVE**, which cannot rescue a pooled fail.* STD and GRAND
are DESCRIPTIVE with pre-stated priors.

**⭐ THE KILL-TEMPO READ IS REGISTERED PROMINENTLY, NOT AS AN AFTERTHOUGHT,
BECAUSE THIS IS A KILL-SPEED PLANK.** See `KILL-ROUND NON-REGRESSION` and D2/D3.
**It cannot rescue a failed share primary.** ⇒ **PRE-COMMITTED CROSS-READING: an
arm that IMPROVES `ITT RMST300` while MISSING the share bar is `FLAGGED NOT
BANKED` — a named iteration input (the tempo is real, the funding or the seat cost
is wrong), never a pass.** The inverse — share up, `RMST300` up — is `MAGNUS-CALL`
under `PROGRAMME.md`'s interim scoring and is not resolved by this lane.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**

**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`, quoted from the file, produced by `tools/control_pin.py`, not re-derived by hand here). There is no opponent churn to pin against and no calibration relevance to protect.**

**SURFACE: local**

**CLUSTER UNIT: none** — `CLAUDE.md`'s enumeration PERFORMED, not asserted. (i) The **MATCH** cluster does not exist on this surface: `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another. (ii) The **OPPONENT** cluster is degenerate: all 5,400 rows play the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe. (iii) The **HOST** cluster is killed by REGISTRATION, not by measurement — this shard is registered LOCAL, single host; the Addendum 11 rider (2026-08-15) is explicit that the 0.98 exemption is a WITHIN-HOST measurement, so a split or cross-host pooling would make the host term live and unmeasured. All surviving clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit): **naive intervals are correct and marginally conservative. The platform constants (1.529 rated / 1.833 unrated) are NOT applicable here and importing them would widen every interval on this page by 24–35% for correlation that has been measured absent.** The per-class cells in #6 inherit the same enumeration — the match cluster is dead there for the same reason (1 row = 1 game), and the opponent cluster is still degenerate — so the per-map ≈1.07 constant does NOT apply either.

**ESTIMATOR: the unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Because the shard is exactly balanced on 15 maps × 2 seats × 180, the pooled share and the map-stratified equal-weight share coincide by construction; the stratified form is computed at readout as an **arithmetic consistency check only** and is not a second estimator (s28 ring-hold: four estimators inside 0.010 of one bar flipped MEET/MISS among themselves). Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are **never a bar** — seat is worth ~6.8pp on byte-identical arms, which is why n is a multiple of 30. Per-class shares use the same rule inside each class. Any interval quoted at readout arrives from `tools/cluster_ci.py` (HEAD) so the point and the interval come from one call; the pre-data half-widths on this page are closed-form Wald and their arithmetic is shown in #6.

**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:68` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30). ⚠ **THE WORKLIST ROW MUST CARRY 5400 EXPLICITLY:** `tools/auto_gate.py:269-270` records that solo prospects carry *"a 2,700 default TARGET, set in the worklist, full-n by explicit annotation only"* — **a row written with 2700 measures a different registration than this one and the bar arithmetic below would then be sized on an n the leg cannot reach.**

**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture, so no accepts count is declared (declaring one would be a panel template wearing a local costume). ⛔ **A LINE COUNT IS NOT A ROW COUNT:** this tape carries an unprefixed column header under the `# FIXTURE` line, so a naive `wc -l` over-reports n by exactly one (measured on KLADLADDER, `results.tsv:kladladder-n-final-correction`; reproduced at draft on `RUSH72.tsv`, 1,116 non-`#` lines ⇒ 1,115 data rows). The registered denominator is **DictReader row count, cross-checked against the heartbeat and against `max(game id) + 1`**.

**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this arm publishes descriptive tallies (pooled share, per-seat, per-map, per-class, kill-round, `cond` mix) and takes **NO comparative look and no bar verdict**: the one-sample half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on, so a sub-2,700 read cannot resolve its own branches. An `auto_gate` cancellation at CATASTROPHE@400, TREND-FLOOR@1000, MARK-1000 or COMBO-BAR@2700 is an **OPERATIONAL STOP, typed `cancellation`, never `verdict`**, and licenses no exclusion claim — with ONE pre-committed carve-out: **a CATASTROPHE-clause stop (95% CI upper < 45.0 at n ≥ 400) is arithmetically incompatible with every band above Band 4, so it DOES license the Band-4 sentence at the partial n**, provided F1–F3 were read first and provided the partial share is disclosed as **selected-pessimistic** if the stop was taken on an interim look. **Per #4, no stop licenses a closure sentence about the plank.**

**BAR: 51.33 — POINT RULE ONLY, MDE 0.00pp, LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE.** (OB16 corollary, 2026-08-15T03:52:45Z: the standard corefill band IS `50 ± half_width` at n = 5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes no positive effect size whatsoever.) n for the one exclusion it CAN make (share ≠ 50.0): **5,400**, the planned n.

**BASE RATE: 50.00**

**BAR SOURCE:** the house-standard corefill futility band, constructed and not observed: `50 + 1.96*sqrt(.25/5400) = 51.3336 ⇒ 51.33pp`, local DEFF 0.98 so naive (with the 0.98 applied the half-width is 1.320pp, so the quoted band is marginally conservative — stated because the two arithmetics differ in the third decimal and the margin here is thin by construction). **The identical bar is carried by `docs/prereg/BARS.tsv` rows `RUSHON`, `RUSH72`, `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTAN`, `SEALSENTA`, `ECOMMIT`, `FREEROUND`, `ROUTESCORE`, `BELTBREAK-EARLY`, `BELTBREAK-LATE`** — which is what keeps this arm numerically comparable to `RUSH72` and to the rest of today's board.

**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base (one boolean apart). Empirically calibrated on the SAME host and fixture by two byte-identical A/A cells, one either side of 50.0, both intervals containing it: **`IDNULL140` 49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z (`results.tsv:idnull140-cert-5400`), and **`NULL125` 51.04% at n = 5,400** with per-class **CQ 52.1 ± 3.7 / STD 50.4 ± 1.8 / GRAND 51.6 ± 2.3** (`results.tsv:null125-final`). ⇒ **a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced**, which is why Band 2 below is pre-registered as WEAK; and **the two cells are 1.77pp apart**, which sizes how much of any class spread is fixture noise.

**REFERENCE n: none** — the bar's comparator is a CONSTRUCTED null of 50.00 generated inside this same shard from its own 5,400 seeds; there is no external reference SAMPLE. **`RUSH72`'s 1,112 rows are NOT a reference sample and are NOT pooled with this shard**: different chassis, different control, and pooling them would be an unregistered n increase (the GUNAXABL/SENTTHR precedent — a replication corroborates a result it is not allowed to rescue). They appear on this page as PRIOR only.

**TREATMENT TREE: bots/_v490rush2**

**TREATMENT DIFF REFS: none**

⇒ **the tree is INTENT-TO-ADD at draft (`git add -N`) and not yet committed, so there is no committed diff ref to name and `tools/prereg_check.py` falls back to `git diff --name-only HEAD`** — which lists all four files of the new tree (verified at draft: 8 `.py` paths returned, of which the four are `bots/_v490rush2/{doctrine,eco,main,raid}.py`). **The builder's lock commit is the durable diff ref and should be written into the `BARS.tsv` source column, replacing this fallback.**

**MECHANISM METRIC READS: bots/_v490rush2/raid.py:673 — the `rush = LOKI2_RUSH_ON and ct.get_current_round() < LOKI2_RUSH_RND` line and the two swaps it drives at `:674-675`, which are the gate the F1/F2 dose metric is downstream of (`ct.build_sentinel(bp, facing)` at `:707`). TREATMENT DIFF TOUCHES: bots/_v490rush2/doctrine.py. INTERSECTION: yes — AND THIS IS THE ONE DECLARATION ON THE PAGE A CERTIFIER SHOULD CHECK HARDEST, BECAUSE THE MACHINE-CHECKED VERSION AND THE SUBSTANTIVE VERSION ARE NOT THE SAME QUESTION.**
* **THE MACHINE CHECK PASSES TRIVIALLY AND MEANS LESS THAN IT LOOKS.** The arm is a NEW TREE, so `git diff HEAD` contains all four of its files and `raid.py` matches by path. **That says nothing about whether the metric can move**, which is what OB13 is for.
* ⛔ **THE SUBSTANTIVE ANSWER, SAID PLAINLY: `raid.py` IS BYTE-IDENTICAL TO THE CONTROL'S** (`cmp` clean at draft on `eco.py`, `main.py` AND `raid.py`; the ONLY file differing from `bots/_v468kladturbo` is `doctrine.py`, by one line). **A control-vs-treatment path match would therefore read NO, and that is the LOKI-18 shape on its face.**
* ⭐ **IT IS NONETHELESS A GENUINE YES, by the rule the checker itself encodes at `tools/prereg_check.py:990-1023`: `bots/_v490rush2/raid.py:64` is `from doctrine import *`, so the constant the metric's gate reads IS the one line that differs, and — the checker's own words — *"a diff to an UNIMPORTED module still FAILs."*** **The LOKI-18 failure mode is a metric that must read IDENTICALLY in both arms; here `LOKI2_RUSH_ON` is the metric's own gate condition and it differs between the arms by construction, so the metric cannot read identically unless the mechanism never fires — which is exactly what F2 is instrumented to detect and is registered as NOT MEASURED rather than as a null.** The `main.py:447-448` consumer binds through the same `from doctrine import *` at `main.py:35`.

**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI2_RUSH_RND=60, LOKI2_RUSH_MIN_HARV=0, LOKI2_RUSH_TI_FLOOR=8, LOKI_FWD_MIN_HARV=2, LOKI_FWD_TI_FLOOR=40, LOKI_FWD_GUN_CAP=3, LOKI_DEFEND_SEAT=4, LOKI_COLD_INSERT_RND=150. MECHANISM CAN OCCUR IN WINDOW: yes** — **exactly ONE of these is a round gate**, `LOKI2_RUSH_RND = 60`, and it is a CLOSING window (`raid.py:673` and `main.py:448` both test `round < 60`), so the mechanism's own window is **r0–r59** and it lies wholly inside the declared r0–r1000. The rest are counts (`MIN_HARV` harvesters, `GUN_CAP` live forward sentinels, `DEFEND_SEAT` a seat index) and titanium thresholds (`TI_FLOOR`), not rounds. **The OUTCOME metric (game share, `cond`, `turns`) is observed over the whole game, which is why the declared window is r0–r1000; the MECHANISM metrics F1–F3 are read inside r0–r59 and their band is stated on each.**
⚠ **DISCLOSED so a green run with warnings under it does not launder them: `prereg_check.py` emits SEVEN `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and SIX OF THE SEVEN ARE CHECKER ARTEFACTS.** Its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a harvester count (`LOKI2_RUSH_MIN_HARV=0`, `LOKI_FWD_MIN_HARV=2`), a titanium threshold (`LOKI2_RUSH_TI_FLOOR=8`, `LOKI_FWD_TI_FLOOR=40`), a live-turret cap (`LOKI_FWD_GUN_CAP=3`) and a seat index (`LOKI_DEFEND_SEAT=4`) are each reported as *"rounds r0-rN cannot contain the mechanism"*. **The ONE that is a real statement is `LOKI2_RUSH_RND=60`, and its warn is CORRECT WITH THE SIGN REVERSED:** the checker treats `_RND` as a floor (mechanism inert below it) whereas this gate is a CEILING (`round < 60`), so the true reading is **the mechanism can occur ONLY in r0–r59 and is inert from r60 on** — which is stated in the paragraph above and is the whole subject of #6. Verified against the actual run at draft; `PREREG_CHECK: OK`. **The constants are declared anyway, because they are the gates that actually bind and an undeclared gate is the failure OB17 exists for.**

**GATE RESOLUTION: three gates, sized separately.** **(a) THE PRIMARY BAR** — margin |51.33 − 50.00| = 1.33pp against a one-sample half-width of ±1.32pp at n = 5,400: resolvable, and **only just**. It is a POINT RULE (MDE 0.00), so clearing it licenses *"we can exclude 50.0 vs `_v468kladturbo`"* and **nothing about a minimum effect size**; `GUNAXABL` missed a zero-slack edge of this exact shape **by one game (0.0152pp)** and that is the standing warning against reading a hairline as a result. **(b) THE PRIMARY SEGMENT (CQ)** — ±3.62pp at n = 720 against a prior effect of ≈ 8–18pp: resolvable FOR THE PRIOR'S OWN SIZE, **UNRESOLVED for anything under ~4pp, and every cross-class difference is DIRECTION-ONLY (±4.28 / ±4.04 / ±2.91pp).** **(c) THE OPERATIONAL FLOORS** — `tools/auto_gate.py` CATASTROPHE@400 (CI-hi < 45.0, `:247`), TREND-FLOOR@1000 (prefix < 52.0, `:261`), MARK-1000/MARK-2700 (CI-hi < BAR 51.33), and **COMBO-BAR@2700 (prefix < 55.0, `:278`) which binds on this arm per #5**; their firings are OPERATIONAL CANCELLATIONS that free a core, typed `cancellation`, never `verdict`. The floors bind on REMOTE too since `a50f27ef` via `tools/remote_cancel.py`; **the binding requirement on this arm is SAME-HOST, and it is registered LOCAL.** Everything else on this page (F1, F2, F3, D2, D3, D4, the seat split, the per-map split) is DIAGNOSTIC and **cannot rescue a failed primary.** **Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION** (OB12's pre-committed default): no promotion, no ship conversation, no combination claim, and — specifically — **no sentence in either direction about whether the eco gate is the kill clock.**

**PRE-STATE: the predicted-change set is NOT already in the target state at lock, and this is a CODE claim, verified at draft.** `grep -n LOKI2_RUSH_ON bots/_v468kladturbo/doctrine.py` → **`1409:LOKI2_RUSH_ON = False`** (one occurrence as an assignment). ⇒ in the control, `raid.py:673`'s `rush` is **False in every round of every game**, so `min_harv` is always `LOKI_FWD_MIN_HARV = 2` and `ti_floor` is always `LOKI_FWD_TI_FLOOR = 40` (`doctrine.py:1264-1265`), and `main.py:446-450` always falls through to `LOKI_ECO_SEATS`, so seat 1 is always `"expand"`. **The behaviour this leg predicts to change is structurally absent from the control**, and the outcome is registered as the win-condition **IN OUR FAVOUR** (game share, `winner == T`), never as the win-condition MIX (OB7). ⚠ **AND THE COMPARATIVE CLAIM IS LIKEWISE NOT PRE-SATISFIED, but it IS PRE-MEASURED ON A DIFFERENT CHASSIS at 50.18% [47.24, 53.12] (`RUSH72`, #1) — disclosed here because a prereg whose question already has a partial answer must say so.**

**MAP SEGMENT: CQ — the two shortest-approach maps of the pool, antler and fjordgate (area ≤ 260, core-to-core Manhattan 8 on both, against a pool range of 8–48). MECHANISM REASON: the waiver only binds where the raider arrives inside `LOKI2_RUSH_RND = 60`, and arrival is a walk of `d` rounds at 1 tile/round, so the shortest-approach class is where the dose is maximal and where the 2026-08-09 study measured its harm concentrated (SHORT −35.4pp / −22.9pp against LONG nulls).**

**EXPECTED DIRECTION: NEGATIVE** — the CQ share is expected to come in BELOW 50.0, by roughly the deflated 8–18pp of the prior. This is a sign this page can be wrong about, and #6's table says how the wrongness would read.

**PRIMARY SEGMENT: CQ (n = 720, ±3.62pp).** STD (n = 2,880, ±1.81pp) and GRAND (n = 1,800, ±2.29pp) are **DESCRIPTIVE ONLY** with the pre-stated priors of #6 (STD negative-weaker, GRAND ~null and ambiguous by construction). **Exactly one primary segment is declared** (OB15b), and because its expected direction is NEGATIVE it **cannot rescue a pooled fail**: OB15c's re-screen path is not invoked by this page and no cut may convert a pooled miss into a pass.

**SEGMENT VALUE CEILING: 13.3% x 12.0pp = 1.60pp** — the CQ class is 2 of the 15 pool maps, so its pairing share on this fixture is exactly 13.3%, and an on-segment magnitude of 12.0pp (the midpoint of the deflated 8–18pp prior) can move the POOLED share by at most 1.60pp. ⇒ **the pooled primary is a WEAK instrument for a CQ-only effect and the CQ read is the on-segment one; a CQ-driven effect of the prior's size would show up pooled as ~1.6pp, i.e. astride the 1.33pp bar and inside the noise two A/A cells already produced.** This is registered as a reason the class split exists, not as a licence to read the pooled number as a CQ number.

**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6 — our own fixture config, measured at 66.7% new-pool against the ladder's 66.0%; declared anyway so the population is on the page, and declared because the 2026-08-09 evidence this arm re-tests is PRE-rotation, which is one of the three reasons the re-test exists.)

**PLANK CLASS: offensive — a kill-tempo plank. It buys earlier forward weapon placement and an extra early raid body by spending the opening economy, on a line whose stated objective is a dead enemy core inside r250. It is not defensive: it removes two protective preconditions rather than adding one, and it makes the opening MORE exposed, not less.**

**KILL-ROUND NON-REGRESSION: ITT RMST300 — mean kill time censored at the r300 horizon over ALL 5,400 games (a non-kill scores 300), treatment minus control. REGISTERED AS AN EXCLUSION: the 95% CI on ΔRMST300 must EXCLUDE a RISE of more than +10.0 rounds; equivalently the interval's UPPER bound must sit below +10.0.** Registered MDE **+10.0 rounds**; the half-width is computed at readout from the OBSERVED per-game sd (pre-data: at n = 5,400 per arm, a per-game sd of 100/120 rounds gives ±3.77/±4.53 rounds, so the +10.0 bar resolves with slack). ⛔ **The kill-win-CONDITIONED share of kills past r300 is REPORTED BESIDE IT AS A DIAGNOSTIC ONLY — it carries a collider (15.1% conditioned vs 7.8% ITT on the rated tape) and may not denominate this read.** The ITT timely-kill rate (share of ALL games with `cond == core_destroyed` and `turns ≤ 300`) and the median kill round are also reported as the triple's rate and gross-backstop factors. **Per `PROGRAMME.md`'s vintage rule, RMST₃₀₀ governs preregs locked from 2026-08-16 onward and this is one.** ⚠ **AND THE DIRECTION EXPECTED HERE IS AN IMPROVEMENT (RMST300 FALLS): a tempo plank that does not move kill time has not delivered its mechanism, which is why this read is also part of the falsifier and not only an admission bar.** ⛔ **A `RUSH2` that improves RMST300 and misses the share bar is `FLAGGED NOT BANKED` (see the hypothesis block) — it may not be reported as a pass, and it may not be reported as a null either.**

**DOSE: first forward-sentinel build round — treatment r18 vs control r27 on the `_v169launchlate160` chassis (p = 0.0003, n=64-class serial dose, `docs/coordination.md:39858-39861`); re-confirmed on the Sleipnir base by F1/F2 at n=60 before any primary sentence is typed.** ⛔ **THAT NUMBER IS BANKED ON A CHASSIS TWO SHIPS OLD AND IS NOT THIS LEG'S DOSE.** It is quoted because a prereg must show the mechanism has been seen to fire at all (the flag-off arm returning to baseline is the other verdict, and it is the control's structural `False` at `doctrine.py:1409`). **F1/F2 are what convert it into a measured claim on `bots/_v490rush2`, and the leg may not be read on the primary without them.**

**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on the pooled treatment
share vs `bots/_v468kladturbo` falls BELOW 51.33.** That excludes the bar. Two
sub-cases, both pre-named and disjoint:
* **CI upper < 50.0** → **THE FLAG SUBTRACTS.** The 2026-08-09 direction is
  reproduced on a fixture this house accepts, on the live chassis, in the currency
  the ladder pays. **Attribution is bounded by #2: this refutes THE BUNDLE at
  `RND = 60` with seats (0,1), not the harvester prerequisite and not the bank
  floor.** Per #4 this is a **DIAGNOSIS, not a closure**, and the registered next
  question is which of the four candidates carried it (see below).
* **CI contains 50.0, point below 51.33** → **PARITY — THE FLAG IS FREE.** The
  bundle pays for its own lost eco seat and its own earlier `+20%`/`+30%` scale
  tail. **UNRESOLVED against the bar ⇒ RESTRICTION** (OB12): no promotion, and no
  sentence claiming the 2026-08-09 result is refuted — a parity read at ±1.32pp
  **excludes an effect larger than ~1.3pp in either direction and nothing more**,
  which is not the same as excluding the 8–18pp the prior predicts on CQ alone
  (see the segment ceiling: a CQ-only effect of that size pools to ~1.6pp).

**⭐ THE FALSIFIER IS WRITTEN IN DIAGNOSIS TERMS, PER THE s49 DIRECTIVE.** On any
stop or any miss, the registered question is **which of these four failed to
land**, and F1–F3 plus D2/D3 are the instruments that answer it:
1. **DOSE** — did a forward sentinel get planted earlier at all? (**F1/F2**)
2. **WINDOW vs APPROACH** — did the waiver ever fire on GRAND maps, or did r60
   expire before arrival? (**F2, per class**)
3. **THE SEAT COST** — did losing seat 1 from the economy inside r60 cost more
   than the tempo bought? (**F3** + D4's `cond` mix)
4. **TEMPO ITSELF** — did kill time move? (**`ITT RMST300`**, D2, D3)

**MECHANISM FALSIFIER (independent of the primary, and it can fire FIRST):**
* if **F1** shows the treatment's forward sentinel builds per game are not above
  the control's outside the tool's own paired band, **the plank did not deliver its
  dose** and the primary is reported as **NOT MEASURED, not as a null** — a flat
  share would then mean *"the mechanism never fired"*, not *"the mechanism fired
  and did not pay"*;
* if **F2** shows the treatment's FIRST forward-sentinel build round is not shifted
  DOWN relative to the control's, or shows **zero games in which a forward sentinel
  is planted inside r60 with fewer than 2 harvesters built**, then the WAIVER
  specifically never bound — the same NOT MEASURED handling applies, and the
  diagnosis is candidate 1 or 2 above;
* if **F3** shows no difference in harvester builds by r60 between the arms, the
  **SEAT half had no runtime effect**, and any result is a result about the waiver
  alone — which would *reduce* the confound named in #2 and must be reported as a
  finding about the instrument, not silently used to widen the attribution.
**Per FIRINGS-BEFORE-PRIMARY all three are read BEFORE the primary is typed.**

**⭐ THE HONEST-NULL CLAUSE — WHAT A NULL MEANS WHEN THE PRIOR IS NEGATIVE, AND IT
IS NOT SYMMETRIC WITH A NEUTRAL-PRIOR NULL.**
* Against a **NEUTRAL** prior, a parity read says *"we learned nothing and the
  plank is available for combination."*
* Against a **NEGATIVE** prior, a parity read says something stronger in ONE
  direction and weaker in the other: it is **evidence AGAINST the 8–18pp pooled
  harm the deflated 2026-08-09 numbers predict** (that magnitude would be visible
  at ±1.32pp), and it is **NOT evidence that the flag helps.** ⇒ **the admissible
  null sentence is: *"on the live chassis, in the currency the ladder pays, the
  95% interval excludes a pooled effect larger than X pp in either direction; the
  large pooled harm the probe study implied does not reproduce; the flag remains
  unpromoted because it does not clear the bar."*** ⛔ **The inadmissible sentences
  are *"the 2026-08-09 result was wrong"* (a pooled parity cannot say that — see
  the segment ceiling), *"the rush is safe to ship"* (it did not clear the bar),
  and *"the eco gate is not the kill clock"* (unattributable, #2).**
* ⚠ **AND THE DEFF DIRECTION CLAUSE APPLIES TO EXACTLY THIS PARAGRAPH:** widening
  an interval makes a fail-to-exclude claim EASIER, so **every null sentence above
  is restated as an EXCLUSION with its own bound before any correction is
  applied** — and on this surface the correction is 0.98, i.e. none.

---

## READING, PRE-COMMITTED

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first row
whose condition holds is the reading. Rows are disjoint by construction.**

### POOLED PRIMARY — four bands on the pooled share vs `bots/_v468kladturbo` at n = 5,400

| # | band | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE FLAG ADDS, AND IT IS THE BIGGEST SURPRISE ON THE BOARD.** A plank switched off on replicated adverse evidence reads positive on the live chassis in the currency that pays. It promotes to a combination input and to a separately-registered head-to-head against the holder. ⚠ Report the size with its OB16 status: MDE 0, so this branch may claim *"we can exclude 50 vs `_v468kladturbo`"* and may NOT claim any minimum effect size. ⛔ **Attribution stays bounded by #2 even here: the BUNDLE adds; which half adds is unknown and the follow-up is the one-line `MINHARV`/`TI_FLOOR` arm on this base.** |
| **2** | **point ≥ 51.33 but CI lower < 51.33** (includes the whole [51.33, 52.4] window an A/A cell has already produced) | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Pre-registered as WEAK: `NULL125`'s byte-identical A/A read 51.04. Rows KEPT; no ship conversation; a replication on fresh seeds, same host, is the price of promoting it. |
| **3** | **point < 51.33 AND CI contains 50.0** | **PARITY — THE FLAG IS FREE, AND THE PROBE STUDY'S POOLED MAGNITUDE DOES NOT REPRODUCE.** See the honest-null clause for the exact admissible sentence and the three inadmissible ones. **UNRESOLVED against the bar ⇒ RESTRICTION.** The diagnosis question (which of the four) is answered off F1–F3 and D2/D3, and it is the deliverable of this branch. |
| **4** | **CI upper < 50.0** | **THE FLAG SUBTRACTS.** The 2026-08-09 direction reproduces on an admissible fixture, the live chassis and the current pool — **the first such evidence this plank has ever had, and the thing house rule 6 said the closure was missing.** Attribution bounded by #2. ⛔ **Per #4 this is a DIAGNOSIS, not a closure: the plank stays on the board and the registered next step is the iteration the diagnosis names (most likely `LOKI2_RUSH_RND` down toward the arrival distribution, or the seat tuple back to `(0,)` so the eco seat is not spent).** |

⚠ **Nothing here treats 50.0 as a floor.** A share below 50 is the PRIOR's own
prediction, is pre-named, and may not be explained away as noise. ⚠ **And nothing
here treats the CQ/STD/GRAND table as able to move a pooled band** — the pooled
band is decided by the pooled number alone.

### SECONDARY — the map-class split, three cells, pre-stated priors, DESCRIPTIVE EXCEPT FOR CQ

Read AFTER the pooled band, and never used to change it.

| class | n | ±pp | pre-stated prior | reading rule |
|---|---:|---:|---|---|
| **CQ** (antler, fjordgate) — **PRIMARY SEGMENT** | 720 | ±3.62 | **NEGATIVE, ≈ −8 to −18pp** | **CI upper < 50.0 ⇒ the 2026-08-09 SHORT-band harm TRANSFERS to the live chassis and the current pool.** CI contains 50.0 ⇒ **UNRESOLVED for anything under ~4pp**; the prior's own magnitude IS excluded, and that exclusion is the finding. **CI lower > 50.0 ⇒ the prior is REFUTED IN SIGN on its own strongest cell — the single most interesting outcome available on this page, and it is named here so it cannot be explained away if it lands.** |
| **STD** (8 maps) | 2880 | ±1.81 | **NEGATIVE, WEAKER** | **DIRECTION AND MAGNITUDE, DESCRIPTIVE.** No promotion, no rescue, no closure. |
| **GRAND** (5 × area 900) | 1800 | ±2.29 | **~NULL, AMBIGUOUS BY CONSTRUCTION** | **DESCRIPTIVE, and a null here is NOT interpretable without F2:** two mechanisms predict it (the waiver never fires because arrival ≥ r60; the seat cost is free because we are rich and idle at area 900) and only F2's per-class plant-round read separates them. ⛔ **No readout sentence may pick one without that read.** |

⚠ **CROSS-CLASS DIFFERENCES ARE DIRECTION-ONLY** at ±4.28 (CQ−GRAND), ±4.04
(CQ−STD), ±2.91pp (GRAND−STD), and `NULL125`'s identical-arm cells already spread
**2pp across the three classes**. **A class spread under those half-widths is
fixture noise and must be reported as such.**

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape carries.

### ⛔ ORDERING, REGISTERED AS A HARD SEQUENCE
**F1, F2 and F3 run and are written down BEFORE any sentence containing this arm's
primary share is typed.** See #7.

### F1 — THE DOSE BATTERY. MEASURABLE, but NOT off the shard tape.
`tools/overnight.sh:138-139` runs every game with `--replay /dev/null`, so the
shard produces **no** entity events. F1 runs on a **separate serial battery**:
```
.venv/bin/python tools/dose.py bots/_v490rush2 --kind sentinel \
    --ctrl bots/_v468kladturbo --registered 60 \
    --keep scratchpad/rush2_replays --tsv scratchpad/rush2_dose.tsv \
    --maps antler archipelago auroraveil drakkarfjord drumlin fjordgate \
           frostgate glacierkeep icefloe midgard nordkap ragnarok royale \
           valkyrie yulerune
```
**REGISTERED SIZE: 60 games, SERIAL** (never parallel — D65, and `tools/dose.py`
runs one game at a time by design). **Pre-registered expectation:
`fwdbuild_sentinel`/game in the treatment strictly above the control's, with the
paired difference outside the tool's own band.**

**⛔ OB17 CHECKS PERFORMED AT DRAFT, AND THE TWO THAT COULD HAVE SURPRISED ME BOTH
DID.**
1. **EXECUTING TOOL NAMED:** `tools/dose.py`, read at draft.
2. **⭐ THE FLAG DEFAULTS ARE WRONG FOR THIS POOL AND THE PREREG MUST OVERRIDE
   THEM — this is the clause that returned an answer nobody had.** `tools/dose.py:77`
   sets `MAPS = ["antler", "atoll", "drumlin", "fjordgate", "heart", "hive",
   "meander", "nordkap"]` — **the RETIRED 8-map set; four of those maps
   (`atoll`, `heart`, `hive`, `meander`) left the pool in the 2026-08-13
   rotation** (`tools/overnight.sh:57-62` says so in its own comment). ⇒ **an F1
   run without `--maps` would dose the arm on half-retired geometry while the
   shard runs the live pool, i.e. the dose and the outcome would be measured on
   different map sets.** The invocation above passes the live 15 explicitly.
   **CONSEQUENCE OF SILENT NON-EXECUTION: the run completes, prints the same
   verdict vocabulary, and nothing in the output says which maps it used.**
3. **BALANCE:** `tools/dose.py:218-219` selects `m = maps[(n // 2) % len(maps)]`
   and `seat = n % 2`, so with 15 maps **60 games = 15 maps × 2 seats × 2 seeds,
   exactly balanced** (a multiple of 30, the same requirement the shard has).
4. **SAMPLE SIZE:** `--games` has **no default any more** — `tools/dose.py:132-152`
   REFUSES to pick one, and `--registered 60` stamps the registered n into every
   verdict line and reports any shortfall against it. **This prereg registers 60
   and the invocation says `--registered 60`, not `--games 60`.**
5. **`--keep` EXISTS:** `tools/dose.py:160-162` (added s48, debt 20) retains every
   replay in `DIR` as `g<NNNN>_<map>_s<seed>_treatseat<seat>.replay26`
   (`:257-261`). **F2 and F3 consume those files, so without `--keep` they are not
   executable** — the exact OB17 failure the SEALSENT pair hit.

### F2 — THE WAIVER READ. **THE LOAD-BEARING FIRING.** MEASURABLE off F1's kept replays.
```
.venv/bin/python tools/corpus/replay_events.py scratchpad/rush2_events.tsv \
    scratchpad/rush2_replays/*.replay26
```
`tools/corpus/replay_events.py:157` emits one row per event with columns
`file ev rnd team kind x y d2_own d2_enemy mw mh`. On rows with `ev == BUILD`,
per game and per team:
* **(a) FIRST FORWARD SENTINEL BUILD ROUND** — the minimum `rnd` over rows with
  `kind == sentinel` and `d2_enemy < d2_own`. **Expectation: the treatment's
  distribution is shifted DOWN relative to the control's** (banked prior on the
  old chassis: r27 → r18, p = 0.0003).
* **(b) ⭐ THE WAIVER ITSELF, AND IT IS THE ONE CHECK THAT CAN COME OUT THE OTHER
  WAY: the count of games containing a forward sentinel built at `rnd < 60` with
  FEWER THAN 2 harvester `BUILD` rows preceding it in that game.** **The control's
  count is a STRUCTURAL ZERO** — `raid.py:676-677` returns False while
  `SLOT_HARVESTERS < LOKI_FWD_MIN_HARV = 2` and the control's `rush` is always
  False (PRE-STATE) — **so any non-zero treatment count is the waiver, and a
  treatment ZERO means the waiver never bound and the leg is NOT MEASURED on that
  mechanism.**
* **(c) THE SAME TWO READS, PER MAP CLASS**, which is what separates GRAND's two
  candidate nulls (#6). **Expectation: (b) is non-zero on CQ and STD and near-zero
  on midgard/ragnarok/drakkarfjord.**
⚠ **A HARVESTER-BUILD COUNT IS NOT `SLOT_HARVESTERS`.** The store slot is a live
census maintained by the bot; the replay gives BUILD events, so a harvester built
and destroyed still counts in (b)'s prefix. **This makes (b) CONSERVATIVE for the
treatment claim** (it can only over-count harvesters and therefore under-count
waiver firings), which is the right direction for a check whose non-zero reading is
the positive finding. Stated at lock rather than discovered at readout.
⚠ **`d2` CONVENTION:** `replay_events.py:95-96,113` measures to a single core
anchor position while the bot's `dsq_core` measures to the nearest tile of the 2×2
footprint. **The forward/home split (`d2_enemy < d2_own`) is robust to that
offset; no absolute d² cut is registered anywhere on this page.**
⚠ **ROTATION GUARD PRESENT, checked rather than assumed:** `rotate()` re-emits
`placeEntity` for an existing id and `replay_events.py:16,113` counts a build as
the FIRST `placeEntity` carrying an id. **Recorded as clean, not as absent.**

### F3 — THE SEAT WIRING READ. MEASURABLE off the same events file.
**Harvester `BUILD` rows with `rnd < 60`, per game, treatment vs control.**
`main.py:447-448` sends seat 1 — an `LOKI_ECO_SEATS` member — to the raid inside
the window, so **the expectation is FEWER treatment harvester builds by r60**.
**DIRECTION ONLY at n = 60.** This is the only instrument on this page that shows
the SECOND consumer had a runtime effect at all, which is why #2's confound is
stated as measured rather than assumed. **If F3 is flat, report it as an instrument
finding and do NOT widen the attribution.**

### D2, D3, D4 — the outcome-shape reads. MEASURABLE, shard-native.
`cond` and `turns` are on the tape.
* **D2 — `ITT RMST300` AND THE ITT TIMELY-KILL RATE**, the `DEFENCE_ADMISSION_BAR`
  family, computed on all 5,400 rows per arm, plus the same reads per map class.
  **Registered as an EXCLUSION per `KILL-ROUND NON-REGRESSION`.** ⚠ **This is the
  metric this plank exists to move, and the direction expected is FASTER.**
* **D3 — MEDIAN KILL ROUND**, treatment vs control, as the gross backstop (median
  crossing 300 is disqualifying). Anchor on this fixture: `KLADTURBO`'s own local
  full read had median kill **193** (`results.tsv:kladturbo-local-confirm-5400`,
  61.09% [59.79, 62.39] at n = 5,400 vs `_v223sealrepair`).
* **D4 — `cond` MIX**, the share of games ending `core_destroyed` / r1000 /
  `NOWINNER` per arm. `R1000_IS_DEFEAT: yes` makes an r1000 share a cost even when
  the tiebreak is won, and a plank that spends the opening economy is exactly the
  family that could trade kills for a grind.

### NOT MEASURABLE on this leg — named, not silently dropped.
* **PLANT COUNTS, PLANT ROUNDS AND HARVESTER TIMING ARE NOT DECODABLE OFF THE
  SHARD.** `tools/overnight.sh:138-139` runs `--replay /dev/null`: **local corefill
  keeps TAPES, not REPLAYS.** The tape can carry share, kill round, `cond` mix and
  D2's ITT reads, **and nothing else.** ⇒ **every mechanism number in this leg
  comes from the SEPARATE F1/F2/F3 battery of 60 games, and the shard's n = 5,400
  lends them NONE of its power.** Anyone quoting a plant count "from the RUSH2
  shard" is quoting something that does not exist.
* **THE SPLIT BETWEEN THE TWO CONSUMERS.** Structurally unavailable, #2. No
  battery size fixes it.
* **WHETHER AN EARLIER FORWARD SENTINEL SURVIVED OR CONVERTED.** Facing is not in
  the decoded event stream, and the arena fixture's forward-turret survival is the
  quantity `FIXTURE_OF_RECORD` names as mis-measured locally (0/480 arena vs 46.9%
  ladder). **This leg prices the flag on the currency; it does not price forward
  turret survival, and no sentence about survival may be built off it.**
* **Per-unit CPU** — local replays zero-fill `execTimeUs`, so no timing claim is
  available on this surface (the s42 rider: `tle_census.py` reads 0 across 1,649
  local builder-turns while reading 8,847 µs on platform replays). `overnight.sh:138`
  does pass `--tle 10`, so a timeout is capped engine-side. ⚠ **The treatment adds
  ZERO code and ZERO new call sites — the one changed line is a constant — so a CPU
  regression is not a mechanism this arm has**, but the surface's blindness is
  named rather than converted into a clean zero.
* **Seed determinism** — `NOISE_ON` pins an unseeded RNG, so base-vs-base at one
  seed diverges at round 0. **No seed-matched or replay-diff equivalence claim is
  available on this fixture; the flag-off equivalence claim is made on the CODE
  (`cmp` clean on three of four files, a one-line diff on the fourth) and never on
  a replay comparison.**

---

## THE CHANGE — `file:line`, control → treatment

**TREATMENT TREE: `bots/_v490rush2`** = `bots/_v468kladturbo` plus **ONE BOOLEAN**.
Verified at draft, and the verification is quoted because it is the whole
treatment:
```
diff -rq bots/_v468kladturbo bots/_v490rush2
  Only in bots/_v468kladturbo: __pycache__          (build artefact, not source)
  Files .../doctrine.py and .../doctrine.py differ

diff -u bots/_v468kladturbo/doctrine.py bots/_v490rush2/doctrine.py
  @@ -1406,7 +1406,7 @@
   # this flag is False; the replicated measurement is.
  -LOKI2_RUSH_ON = False
  +LOKI2_RUSH_ON = True
   LOKI2_RUSH_RND = 60        # the committed-opening window

changed-line counts (`diff | grep -c '^[<>]'`):
  doctrine.py 2   eco.py 0   main.py 0   raid.py 0
cmp:  eco.py IDENTICAL   main.py IDENTICAL   raid.py IDENTICAL
py_compile on all four:  OK
```
⇒ **EXACTLY ONE LINE DIFFERS ACROSS ALL FOUR FILES** (`doctrine.py:1409`; the 2 is
one `<` plus one `>` for the same line). **No new code, no new call site, no new
constant.** The four constants the flag activates were already in the tree and are
unchanged: `LOKI2_RUSH_RND = 60` (`:1410`), `LOKI2_RUSH_MIN_HARV = 0` (`:1411`),
`LOKI2_RUSH_TI_FLOOR = 8` (`:1412`), `LOKI2_RUSH_SEATS = (0, 1)` (`:1413`).

**THE TWO CONSUMERS THIS ACTIVATES**, both read personally at draft (and both
differing from the anchors in the queue row that produced this brief — see #2):
1. **`bots/_v490rush2/raid.py:673-675`**, inside `_try_fwd_sentinel`:
   `rush = LOKI2_RUSH_ON and ct.get_current_round() < LOKI2_RUSH_RND` ·
   `min_harv = LOKI2_RUSH_MIN_HARV if rush else LOKI_FWD_MIN_HARV` ·
   `ti_floor = LOKI2_RUSH_TI_FLOOR if rush else LOKI_FWD_TI_FLOOR`.
   The gates they feed are `:676-677` (`SLOT_HARVESTERS < min_harv` → return) and
   `:678-680` (`get_global_resources() < sentinel_cost + ti_floor` → return); the
   plant is `ct.build_sentinel(bp, facing)` at **`:707`**. The forward cap at
   `:670-672` (`LOKI_FWD_GUN_CAP = 3`, live census when `LOKI2B_LIVE_CAP_ON`) is
   **untouched by this flag**.
2. **`bots/_v490rush2/main.py:446-450`**: `elif (LOKI2_RUSH_ON and n in
   LOKI2_RUSH_SEATS and ct.get_current_round() < LOKI2_RUSH_RND): self.role =
   "raid"`, sitting BELOW the `LOKI_DEFEND_SEAT` test (`:444-445`) and ABOVE the
   `LOKI_ECO_SEATS` test (`:451-452`), so **seat 1 is diverted from `"expand"` to
   `"raid"` while seats 2 and 3 and the defender are unaffected**.

**BOTH CONSUMERS BIND THROUGH `from doctrine import *`** — `raid.py:64`,
`main.py:35` — which is the import-binding that makes `INTERSECTION: yes` true
despite `raid.py` and `main.py` being byte-identical between the arms.

**THE COMPOSE MARKER IS INHERITED AND IT IS LOAD-BEARING FOR THE GATE**, not
cosmetic: `bots/_v490rush2/doctrine.py:1879` carries
`# ---- composed by tools/stack.py from: turbo (_x3r0v152), bodyaware
(_v242bodyaware), samestop (_v464samestop)`, which is what makes
`tools/auto_gate.py`'s `combo_of` classify this arm COMBO (#5). **Do not remove
it to change the bar** — the base tree's own comment at `:1884` explains that the
marker is deliberate, and editing it to dodge a bar is editing the registry from
inside the arm.

**⛔ AND THE CONTROL TREE WAS NOT TOUCHED.** `bots/_v468kladturbo` is the pinned
corefill control that every queued row on today's board is scored against, and a
live shard may read it at any moment. This agent copied FROM it and wrote nothing
INTO it; `git status --short bots/_v468kladturbo` shows only the pre-existing
deleted `__pycache__` blobs from before this session.

---

## WHAT THIS LEG COSTS, AND WHAT IT DOES NOT DECIDE

**Cost: one LOCAL core to n = 5,400 (very likely far less — see #8), plus 60 serial
games for F1/F2/F3.** ZERO rated ladder exposure, zero submissions, zero unrated
challenges, no activation.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input — ⚠ **and the disjointness is NOT verified for this arm and must
not be assumed: the flag reaches `raid.py`'s forward-turret path and `main.py`'s
seat assignment, both of which other board arms also touch** — and (b) a
separately-registered head-to-head against the live holder, which is the step
`PROGRAMME.md` records Magnus naming verbatim (*"we start by testing it against the
current slot, if it beats it we can switch"*), gated by
`X3R0_SLOT_RULE`'s 60±2 threshold. **Gate-1-to-gate-2 transitivity is UNVALIDATED
in this repo (QUEUE #65: 3 concordant, 1 not), so the head-to-head is not
skippable on the strength of this number.**

**It does NOT close a road** — `CLAUDE.md` point 6 (only live-game evidence closes)
and the s49 directive (#4) both forbid it, from different directions.

**It does NOT answer *"is the eco clock the kill clock?"*** — that is the question
the brief's motivation poses and #2's confound puts it out of reach. **The clean
arm for it is a one-line `LOKI_FWD_MIN_HARV 2 → 1` (or `→ 0`) and/or
`LOKI_FWD_TI_FLOOR 40 → 8` flip on `bots/_v468kladturbo`, i.e. `MINHARV1` re-based,
and it is a PROPOSAL for Magnus under the s49 directive, not something this page
authorises anyone to build.**

**AND IT FEEDS MAGNUS'S DAY TARGET ONLY WEAKLY, which is said here rather than
implied:** the target is >60% vs Sleipnir v1 and this arm's registered bar is
51.33%. ⚠ **60-vs-Sleipnir is ≈ 70.6-vs-v140 through the logistic**, and the
board's ceiling at the last ruling was 55.24%. **An arm whose prior is negative is
not a candidate for that target; it is a PRICING run for a plank that has never
been priced on an admissible fixture (#1, #4), and that is the honest reason to
spend a core on it.**

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: OB7, OB8, OB10, OB11, OB12 + its pre-committed restriction default, OB13, OB14, OB15a/b/c + the segment vocabulary and the units rider, OB16 + its corollary and the cross-host rider, OB17 + its "run the clause that can surprise you" rider, and the **2026-08-17T07:24:55Z addendum** that replaced the local-shard clock-2 boilerplate — quoted rather than restated) · `PROGRAMME.md` (parsed block `:6-30` — `INCUMBENT: bots/_v468kladturbo`, `PRIMARY_CURRENCY: game_share`, `WIN_RATE_IS_VERDICT: yes`, `KILL_WINDOW_RND: 250`, `R1000_IS_DEFEAT: yes`, `PLAY_DEFENCE: not_at_the_kill_s_expense`, `DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`, `SLOT_STOP_LOSS: off`, `X3R0_SLOT_RULE`; the `:488-564` r300 re-pricing chain including the collider correction and the **ITT RMST₃₀₀ arbitration of 2026-08-16T05:36:10Z with its vintage rule**; `:166-197` the area-900 rich-and-idle measurement) · `docs/prereg/PREREG-BELTBREAK-EARLY-2026-08-17.md` (read in full — today's house structure, token order, and the local-fixture caveat set reused here) · `bots/_v468kladturbo/doctrine.py:1324-1413` (the LOKI-2 block, **the `:1395-1408` adverse-evidence comment quoted verbatim in #3**, and the five constants), `:1209` `LOKI_ECO_SEATS`, `:1210` `LOKI_DEFEND_SEAT`, `:1236-1237` `LOKI_FWD_SENTINEL_ON`/`LOKI_FWD_GUN_CAP`, `:1262` `LOKI2B_LIVE_CAP_ON`, `:1264-1265` `LOKI_FWD_TI_FLOOR`/`LOKI_FWD_MIN_HARV`, `:1317` `LOKI_COLD_INSERT_RND`, `:1879-1884` the stack.py compose marker and its deliberate-phrasing note · `docs/RESULT-rush-map-interaction-2026-08-09.md` (read in full: §1 the failed prediction, §2 the two-fixture table, §3 the saturated-instrument rule, §4 the four not-claimed limits, §5 the queue consequence, the S5 real-engine addendum `dfc4b892` 4–1 at p=0.1875, and the CALIBRATION ADDENDUM's sourced ~2× self-play deflator and its both-ways clause) · `bots/_v468kladturbo/raid.py:655-714` (the live gate and plant, read personally) and `bots/_v468kladturbo/main.py:430-457` (the live seat branch, read personally) · `bots/_v468kladturbo/raid.py:64` and `main.py:35` (`from doctrine import *`, the import binding) · `docs/prereg/BARS.tsv` (header `:1-20` incl. the FIRINGS-BEFORE-PRIMARY rule and the why-not-a-worklist-column note; **`:98` `RUSHON` and `:272` `RUSH72`**, the two prior registrations of this same flag; `:281` `RENT3B`; and the sibling `ECOMMIT`/`FREEROUND`/`ROUTESCORE`/`BELTBREAK-*`/`ODINVSSLEIP` rows for bar comparability — **no row was added by this agent**) · `scratchpad/overnight/RUSH72.tsv` (`# FIXTURE` header verbatim, 1,116 non-`#` lines) and `scratchpad/overnight/RUSH72.heartbeat` · `scratchpad/auto_gate_cancelled.tsv` (the two 09:17:53Z RUSH72 rows) · `results.tsv` (rows `rush72-autostop-1000`, `idnull140-cert-5400`, `null125-final`, `kladturbo-local-confirm-5400`, and the KLADLADDER rows `kladladder-n-final-correction` / `kladladder-verdict-amendment-f1f2-pending`) · `scratchpad/corefill_work.txt` (`:5` the row format, `:625-660` the RUSHON queue note with its two-consumer defect and its "never licenses a sentence about the rush gate" clause, **`:713` the CUT ruling verbatim**, and the tail rows establishing the seed sequence 812000–826000) · `bots/_v460rush/doctrine.py:1409` and `diff -rq bots/_v460rush bots/_v223sealrepair` (establishing that RUSH72's arm is this same one-boolean flip on the previous chassis) · `docs/coordination.md` (**`2026-08-17T08:14:52Z` the s49 Magnus directive verbatim, its four-point operational form, the four-arm board naming RUSH2, and the parked proposals** — via `git show d226b851`; `:26739-26745` and `:27352` the LOKI-11 +16.0pp → +0.0pp regression; `:39853-39861` the two-opposite-signs note and the banked r27→r18 / r22 dose figures) · `tools/prereg_check.py` (read for `RULES`, `KNOWN_KEYS`, `key_pattern`/`field`, `first_number`/`raw_number`/`int_before`, `check_presence`, `check_arithmetic`, `check_metric_window`, `check_pool_era`, `untracked_arm_paths`, `git_diff_paths`, the `:990-1023` import-binding branch, and the `:366-371` `int_before` comma defect it now guards) · `tools/auto_gate.py` (`:244-247` `MARK_CATASTROPHE`/`CATASTROPHE_CI_HI`, `:261` `TREND_FLOOR = 52.0`, `:264-278` the COMBO_BAR block and its pricing, `:280-314` the CONFIRMATION-CLASS exemption, `:715-742` `combo_of`, `:902-960` the clause order and the COMBO-BAR-EXEMPT citation guard) · `tools/overnight.sh` (`:57-68` the 15-map pool and the retired-set comment, `:71-80` the basename-collision guard, `:87-110` the `# FIXTURE`/`START` stamp and the legacy-resume form, `:138-139` `--replay /dev/null --tle 10`) · `tools/overnight_read.py` (`:76-94` `map_area_class` CQ/STD/GRAND from the map headers, `:97-106` `live_pool`, `:361-365` and `:572-585` the per-class tally and its n≥400 print floor) · `tools/map_encode.parse_map26` (used at draft to compute the core-to-core Manhattan distances in #6) · `tools/dose.py` (`:77` the RETIRED default map set, `:132-172` the argparse incl. `--registered`/`--keep` and the no-default refusal, `:218-219` the map/seat rotation, `:257-261` the keep-file naming) · `tools/corpus/replay_events.py` (`:16` and `:113` the rotation guard, `:95-96` the core anchor, `:157` the output columns) · `tools/control_pin.py` and `scratchpad/CONTROL_PIN` (the quoted digest) · `tools/fwd_read.py` (read and NOT registered — its docstring records that arena/h2h emit no forward quantities; F1/F2 use `dose.py` + `replay_events.py` instead) · `CLAUDE.md` (point 6 on what closes a road, the probe-fixture direction and the 0/480-vs-46.9% forward-turret figure, the DEFF scope procedure and its direction clause, the local 0.98 exemption, the `print()`-stripped-from-platform-replays ruling — which is why nothing on this page reads our own stdout from a platform replay; **the F1/F2/F3 reads are LOCAL replays decoded by our own decoder, not stdout, and are unaffected**) · `docs/research/FORWARD-ARRIVAL-BASELINE-2026-08-16.md` (cited for the median forward arrival r31, via the BELTBREAK prereg's quotation of it) · git commits `d226b851` (HEAD at draft), and `git log`/`git ls-files`/`git diff --name-only HEAD` output quoted above · the drafting brief supplied by the builder lane s49. **No file under `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md`, `QUEUE.md`, or `bots/_v468kladturbo/` was created or modified by this agent, and no game was run.** The only writes were this document and the four files of `bots/_v490rush2` (created + `git add -N`, uncommitted).

**AMENDMENTS ARE ADD-ONLY AND BLIND TO THE DATA.** Corrections land as new dated
sections appended to this file (or as a new dated doc, per the obligations doc's
own amendment clause), never as edits to the text above, and no amendment may be
written after the first tape row exists unless it is verifiably blind to that
tape. **The registered n, bar, MDE, primary segment, expected direction, reading
bands and firing sequence are frozen at the lock commit.**
