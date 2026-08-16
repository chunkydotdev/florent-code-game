> ⛔⛔ **BOOT-FOUND ANNOTATION, BUILDER s45, 2026-08-16T04:48:33Z (`date -u`) — THIS
> DOCUMENT WAS NEVER LOCKED AND ITS LEG ALREADY RAN. READ IT AS A DRAFT, NOT A PREREG.**
> The draft below was written s44 (drafting wall clock 2026-08-15T06:55:41Z, per its own
> STATUS block) and was found UNTRACKED at the s45 builder boot — its "committed BEFORE
> the leg" status line never became true. The homeearly arm (`_v250homeearly` vs
> `_v223sealrepair`) then ran overnight on ws2 as fleet rows F250HOMEEAR (50.48%,
> n=5,400) and LNCHERL2 (50.32%, n=5,405), BEFORE this commit. Both cells are therefore
> UNREGISTERED SCREEN reads — usable for prioritisation, not bankable against this
> document's bar. Committed now for the record of what was drafted and when, per the
> verdict block in docs/coordination.md (BUILDER s45, 04:48:33Z). Nothing below this
> annotation was edited.

# SCREEN PREREG — `homeearly`: lift the round gate on the HOME launcher (160 → 24)

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, fired no game, and touched neither `results.tsv` nor `HANDOVER.md`
nor `PROGRAMME.md`.

**STATUS: committed BEFORE the `HOMEEARLY` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/HOMEEARLY.*` exists, and BEFORE the leg's first game.**
Two-clock form: this commit's git author time against the shard tape's own
`# FIXTURE … start=` stamp, which `tools/overnight.sh:99` writes BEFORE the first
game (a START, not a first-completed-row). Drafting session wall clock at write
time **`2026-08-15T06:55:41Z`** (`date -u`, same shell call); repo HEAD at draft
`914e4a4f` (author time `2026-08-15T08:55:39+02:00`). Verified at draft:
`grep -c HOMEEARLY scratchpad/corefill_work.txt` → **0**;
`ls scratchpad/overnight/ | grep -i home` → **empty**.

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v250homeearly`,
added `3d303baf`, 2026-08-15T08:34:36+02:00). That is legitimate — the tree was
built for the dose probe that gates this screen — but it means this document is
NOT locked before the arm exists, only before the arm's first screen row. Said
here rather than left for a certifier to discover.

---

## ⛔⛔ READ THIS BEFORE RATIFYING — FOUR THINGS THE LANE MUST DECIDE, NOT INHERIT

**1. THE COMMISSION IS A DIRECT MAGNUS DIRECTIVE AND IT BINDS THIS DOCUMENT.**
Verbatim, s44: *"If dosage shows that the build has an effect we put it directly
as a shard, dont dismiss based on logical thinking after dosage."* The dose fired
(0 throws → 183 throws). **So this prereg does not argue whether to run the leg.
It argues only about HOW the leg is read**, and every pushback below is a design
pushback, never a stand-down.

**2. THE BRIEF'S `n` UNIT IS TWO DAYS STALE AND WOULD BREAK MAP/SEAT BALANCE.**
The commissioning brief says *"target n a multiple of 16 (8 maps × 2 seats)"*.
`tools/overnight.sh:66` has run a **15-map** pool since the 2026-08-13 rotation
and its own comment says so: *"Targets should be multiples of 30 (15 maps x 2
seats) for exact map/seat balance; the old multiples of 16 no longer balance."*
The seed advances every 16 games (`overnight.sh:121`) — that is the SEED stride,
not the balance period. **Every n on this page is a multiple of 30.** A
multiple-of-16 target on this runner measures seat, which is worth ~6.8pp on
byte-identical arms.

**3. THE DOSE'S OPPONENT IS NOT THIS SCREEN'S OPPONENT, AND THAT IS THE LARGEST
RISK ON THE PAGE.** The banked dose was measured against `_probe_creeper` — a
fixture WE authored precisely because *"their builders walk to OUR core and stand
there as turret feeders"*. The screen's control is `bots/_v223sealrepair`, our own
raid line, which does not camp. **If our own builders never dwell inside the home
launcher's d²≤2 pickup envelope, this shard measures the PRICE and nothing else,
on every map, and its null is a fixture artefact rather than a finding about the
plank.** That is the exact inverse of the coverage-dilution nulls
`SCREEN-launchmax-2026-08-15.md` §1 documents for the launcher family. **A PRE-FIRE
DELIVERY GATE (G1/G2, below) is therefore registered and the shard may not be
SCORED until it passes.** Cost: ~160 games, ~3 minutes.

**4. A SIBLING PREREG ARGUED THE OPPOSITE ABOUT THIS EXACT CONSTANT, ELEVEN HOURS
AGO, AND THE LANE SHOULD KNOW BEFORE RATIFYING.** `SCREEN-launchmax-2026-08-15.md`
§1 lists `LAUNCHER_MIN_RND 160 → 0` as throttle **T1** and decides **NOT LIFTED**,
on the ground that it *"buys ZERO coverage given T3"* and is *"a price lever with
no occurrence return"*. **That reasoning is sound INSIDE LAUNCHMAX and does not
reach here**, because LAUNCHMAX lifts T3 (a forward launcher planted where the
victims are), which makes the home launcher's 1-in-17 pickup rate irrelevant to
it. HOMEEARLY lifts T1 **alone**, so the home envelope is the entire mechanism,
and the dose measured it firing at 21.9% of games rather than 0.5%. **Two
documents, opposite calls on one constant, both defensible on their own fixtures
— the lane owns reconciling them, and the reconciliation is that they are testing
different objects.**

---

## RATIFY: Hypothesis

**Lifting `LAUNCHER_MIN_RND` from 160 to 24 (`LOKI_HOMEEARLY_ON`) raises our LOCAL
game share against the shipped v140 tree (`bots/_v223sealrepair`) to 53.62% or
higher ON THE 900-AREA MAP CLASS — midgard, ragnarok, valkyrie, drakkarfjord,
glacierkeep — at n = 3,600 games in that stratum, while COSTING game share on the
ten sub-900 maps, where the +10% scale levy is paid and no pickup opportunity
exists.**

**EXPECTED DIRECTION: POSITIVE on the declared segment; NEGATIVE on its
complement.** The two-sided shape is deliberate: it is what makes this a test of
the throw mechanism rather than of "something changed".

⛔ **AND THE HYPOTHESIS HAS A STRONG, MEASURED, ALREADY-BANKED OPPOSITE — which is
why it can fail and why the bar is where it is.** The launcher family sweep
(n = 5,408/arm, v114 chassis, pre-rotation 8-map pool) reads **LATE160 51.42 vs
RES0 48.63**, i.e. **an ungated early launcher measured 2.79pp WORSE than the
gate this plank removes**, and the ownership premium `LAUNCH0 − BOTH0` is
**−6.34pp**. **The knob this arm reverts was SWEPT, and the sweep chose 160.**
This leg's claim is not that the levy is imaginary; it is that on 30×30 terrain
the pickup opportunity outweighs it. If it does not, the sweep was right and the
road closes properly this time — with the map axis measured rather than pooled
away.

---

## THE CHANGE — `file:line`, old → new

**TREATMENT TREE: `bots/_v250homeearly`** — byte-for-byte `bots/_v223sealrepair`
apart from two hunks. `diff -rq` names exactly two `.py` files (verified at
draft: `doctrine.py`, `main.py`; the `__pycache__` entries are build artefacts and
are not source).

**(1) `main.py:613-616` — the gate round itself is the treatment.**
```
  OLD (:613)
        if ct.get_current_round() < LAUNCHER_MIN_RND:
            return False

  NEW (:613-617)
        # LOKI-HOMEEARLY (v250): the gate round itself is the treatment.  With
        # the toggle off this reads LAUNCHER_MIN_RND and is the parent exactly.
        _lmin = LOKI_HOMEEARLY_RND if LOKI_HOMEEARLY_ON else LAUNCHER_MIN_RND
        if ct.get_current_round() < _lmin:
            return False
```

**(2) `doctrine.py:1537-1558` — two new constants, nothing else.**
```
  NEW   LOKI_HOMEEARLY_ON  = True
        LOKI_HOMEEARLY_RND = 24
```
`LAUNCHER_MIN_RND = 160` is **left in place and still referenced** by the
toggle-off branch, so **toggle-off is byte-identical in behaviour to the
incumbent** — verified by reading the expression, not by assertion: with
`LOKI_HOMEEARLY_ON = False` the line evaluates to `LAUNCHER_MIN_RND` and the
guard is the parent's guard exactly.

**Why 24 and not 0** (the tree's own comment, `doctrine.py:1553-1556`, adopted
here rather than re-derived): `_try_build_launcher` already refuses below
`SLOT_HARVESTERS < 1`, so r24 is the earliest round at which that refusal is
normally already satisfied; a gate of 0 would only add rounds in which the build
cannot happen anyway.

### THREE GATES BETWEEN THE ROUND CHECK AND AN ACTUAL EARLY LAUNCHER — the reason G2 exists

Reading `main.py:593-666` and `:446-451` in full, the round gate is **necessary
and not sufficient**. A launcher at r24 also requires: a builder whose
`self.role == "defend"` (only `_defend` reaches `_try_build_launcher`,
`main.py:449` → `:675`); `SLOT_HARVESTERS >= 1` (`:642`); and
`_eco_spendable(get_launcher_cost() + LAUNCHER_RESERVE)` with
**`LAUNCHER_RESERVE = 80`** (`doctrine.py:965`, consumed `main.py:644`). ⇒ **the
build round is an EMPIRICAL question even after the gate is lifted, and G2 below
is the measurement, not a formality.**

---

## STOP CONDITIONS — the three the method demands, answered by grep and not by memory

**1. IS THE CHANGE ALREADY IN THE INCUMBENT? NO.**
`grep -rn "LOKI_HOMEEARLY" bots/_v223sealrepair/` returns **zero hits**.
`grep -rn "LAUNCHER_MIN_RND" bots/_v223sealrepair/` returns exactly two:
`doctrine.py:1536` (the definition, `= 160`) and `main.py:613` (the single
consumer). **One definition, one live call site — a behaviour, not a dead spec.**

**2. MECHANISM OCCURRENCE — MEASURED, AND THE OCCURRENCE IS THE POINT.** Under the
incumbent the mechanism is **zero by construction in r0–r159** and, in the
archived field, our median actual launcher build lands at **round 318** — so the
gate excludes roughly three quarters of a measured opportunity: **53.7% of our
games contain an enemy builder planting a turret within d²≤8 of OUR core, and
73.3% of near-core enemy builds happen BEFORE round 160.**

**3. LATER RULINGS ON THIS ROW — grepped, not assumed.** `grep -n` over
`docs/coordination.md` for `HOMEEARLY`/`homeearly` returns **nothing** (the dose
landed at 06:41Z today and the row is newer than the coordination tape's last
launcher entry). The adjacent standing rulings that DO bind are recorded above as
item 4 and in "Interaction with the live legs" below. **There is no HELD or KILL
ruling on this arm to override.**

⚠ **INSTRUMENT DEBT, surfaced by this arm and not caused by it:**
`PROGRAMME.md`'s `LINE_DIRS` (`bots/_v1[3-9]?*`) does not match anything past
`_v199`, so `tools/gate.py` needs an off-programme escape for **every** arm in the
`_v2xx` range — the dose commit `01e0a411` took exactly that escape and said so.
**A gate that must be escaped on every invocation is a gate that has stopped
gating.** Not this leg's job to fix; it is this leg's job to say so.

---

## DOSE — the probe, its control, and the three things it does NOT establish

**DOSE: enemy-builder EXILE throws decoded off the replay wire — variant 183 throws in 7 of 32 games (21.9% of games, 5.72 throws/game) vs flag-off control 0 throws in 0 of 32 games (n=32 games/arm; `_det250homeearly` played against `_det223sealrepair`, both `NOISE_ON=False` copies; opponent `_probe_creeper`; 8 maps × 2 seeds × 2 seats; commit `01e0a411`, 2026-08-15T06:41:07Z; metric read off the replay wire, never from `print()`).**

*(The word "vs" appears exactly once on the line above, and deliberately:
`prereg_check`'s DOSE check splits on it and reads the first number in each half.
An arm-pair written as `A vs B` inside the parenthetical makes the tool read the
control value off a DIRECTORY NAME — it read `223` from `_det223sealrepair` on
the first draft of this line and PASSED, because 183 ≠ 223. A guard that reports
success on a misread is worse than one that fails.)*

**The probe carries BOTH verdicts and the control is a genuine zero, not an
untried one:** the control arm is the same tree with the toggle off, i.e. the
incumbent's `LAUNCHER_MIN_RND = 160`, and it read **0 throws in 0 of 32 games** —
which is what the source predicts, so the source read and the measurement agree.

**⛔ THREE LIMITS, carried forward verbatim from the dose commit because the
result is favourable and a favourable result is when limits get dropped:**

* **MAP-CONDITIONAL.** 162 of 183 throws are **ragnarok** (4/4 games) and 21 are
  **midgard** (3/4). **SIX of eight maps read exactly ZERO.** This is the fact the
  Segment section is built on.
* **SATURATED ON VALUE.** Win rate is **32/32 = 100% on BOTH arms**. The dose
  fixture cannot resolve worth at all. **This screen exists because of that, not
  in spite of it.**
* **OUR OWN PROBE.** `_probe_creeper` is a fixture we authored and it lies in a
  known direction. Per `FIXTURE_OF_RECORD: live_unrated` the CURRENCY read is a
  live pinned leg; this local screen is the cheap intermediate, and no branch of
  it ends in a submission.

**⛔ AND A FOURTH LIMIT, which is this document's and not the dose commit's: THE
DOSE OPPONENT IS NOT THE SCREEN CONTROL.** See item 3 of the ratify block. **The
21.9% figure may not transfer to self-play at all**, and the pre-fire gate below
is the only thing standing between that possibility and a null nobody can
interpret.

**Field baselines, for subject-carrying:** v140 archived launcher-throw rate is
**1.26% of games** and we are farmed **18.7×** on this mechanism — in 718 v140
games opponents threw our builders **7,835 times across 17.1% of games** against
our **419 across 1.26%**.

---

## Instrument, fixture and units

* **SURFACE: local** — corefill shard, `tools/corefill.sh` + `tools/overnight.sh`,
  `--tle 10`, `--replay /dev/null`, the 15-map pool, both seat orders.
* **TREATMENT TREE: bots/_v250homeearly** (control `bots/_v223sealrepair`).
* **CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED and MEASURED, not
  asserted, and it is performed over **three** clusters because this leg's primary
  read is stratified:
  * **MATCH cluster — DEAD.** Corefill has no 5-game matches; one tape row is one
    game on its own seed, so a stratum cannot hold two members of a match.
  * **OPPONENT cluster — DEAD.** Every row is played against the same single
    control tree on disk; opponent is a constant and carries no between-cluster
    variance.
  * **MAP cluster — LIVE, AND THEREFORE MEASURED.** The primary stratum holds 720
    games from each of 5 maps, so the stratum *can* hold many members of one map.
    Measured on the A/A cell `NULL125` (byte-identical arms, same 15-map pool,
    n = 5,400): per-map design effect **0.642 on the 900-area stratum**, **0.413
    on the sub-900 stratum**, **0.474 pooled** — all BELOW 1, i.e. the per-map
    shares are LESS dispersed than binomial. ⚠ Quoted with its weakness: k = 5
    clusters is 4 df and the estimate is noisy. **It gives no evidence of
    inflation, so no inflation is applied.**
  ⇒ **Applicable design effect is the standing local constant DEFF = 0.98**
  (pair-weighted, ρ = −0.020, 124 shards, s39 audit).
  ⛔ **The platform constants (1.529 rated / 1.833 unrated) are NOT applied.** Over-
  applying a correction is an error in the same family as omitting it and would
  widen every interval on this page by 24–35% for correlation that has been
  measured absent on this exact fixture.
* **ESTIMATOR: unweighted treatment game share within the declared stratum** =
  rows with `winner == T` over all non-comment, non-`NOWINNER` rows of
  `scratchpad/overnight/HOMEEARLY.tsv` whose `map` column is in the stratum. One
  local row is one game, so game share and win rate coincide here; the
  `WIN_RATE_IS_VERDICT` caution governs MATCH win rate on the platform and does
  not reach this fixture.
* **PINNED: N/A — local self-play.** The opponent version is fixed by construction
  (a directory on disk), so there is nothing to pin and no churn to absorb.
* **TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input.** The rated question this arm must answer LATER is bounded by the segment ceiling below (0.65pp pooled at the registered MDE), and that bound is the reason no branch here ends in a ship.
* **POOL ERA: post-2026-08-13-rotation** (`POOL_ERA: post-2026-08-13-rotation`).
  The 15-map pool at `tools/overnight.sh:66`: antler archipelago auroraveil
  drakkarfjord drumlin fjordgate frostgate glacierkeep icefloe midgard nordkap
  ragnarok royale valkyrie yulerune. **Every historical launcher final quoted on
  this page (LAUNCH0 / BOTH0 / LATE160 / RES0 / RES20) was measured on the
  PRE-rotation 8-map pool and the v114 chassis** — era-labelled, which is one more
  reason each is a PRIOR and a comparator in no bar here.
* **SPANS-POOL-CHANGE: no** — the shard starts and ends inside the current pool
  era.
* **CELL VERSION CHURN: N/A — not a panel.** One control tree, pinned by being a
  file; there are no opponent cells and no churn to count.
* **HOST TERM: within-host only. This leg registers NO cross-host pooling.** Per
  the s42 rider to OB16 (`PREREG-amendments-and-lock-obligations-2026-08-09.md`),
  the local DEFF 0.98 exemption does not cover cross-host pooling. If a remote
  replication of this arm is stocked on `work-server-2`, it is **reported
  separately and may not be pooled into any number on this page** — the precedent
  is GUNAXABLR/SENTTHRR, which corroborated nulls they were not allowed to rescue.

**Shard line to append to `scratchpad/corefill_work.txt`:**
```
HOMEEARLY   bots/_v250homeearly    bots/_v223sealrepair   10800 350000
```

**BASENAME-COLLISION CHECK, BOTH DIRECTIONS** (`overnight.sh:78` refuses on
`$B == *$C*` **or** `$C == *$B*`, because scoring is a SUBSTRING match on the
`Winner:` line and a one-way check reads ~100% for the treatment):
* `_v250homeearly` contains `_v223sealrepair`? **NO.**
* `_v223sealrepair` contains `_v250homeearly`? **NO.**
* Shard name, both directions: no existing shard id in `corefill_work.txt`
  contains `HOMEEARLY` and `HOMEEARLY` contains none of them (checked against the
  full 130-id list; the near misses `GUNEARLY60`/`GUNEARLY150` are neither
  substrings nor superstrings).
* ⚠ **ONE REAL HAZARD TO NAME:** `bots/_det250homeearly` exists (the
  `NOISE_ON=False` dose copy). It is **not** used by this shard. **But
  `_det250homeearly` and `_v250homeearly` share the substring `250homeearly`, so
  running those two against each other would be unscorable** — recorded so a later
  A/A cell is not built out of them by accident.

**SEED BASE 350000, span 350000–350674.** `overnight.sh:121` advances the seed
every 16 games, so 10,800 games consume 675 seeds. Highest live/queued base in the
worklist is **344000 (`NULL5400`, → 344337)**; `BODYAWR` holds 336000–336674 and
`LAUNCHMAX` proposes 340000–340337. **No overlap in either direction, with 5,662
seeds of headroom below 350000.**

---

## RATIFY: Decision rule

* **PLANNED n: 10800 games** (= 15 maps × 2 seats × 360, so map and seat balance
  are exact; the primary stratum is exactly 5 × 720 = **3,600 games** and its
  complement exactly **7,200**).
* **BOUNDARY: 10800 games** — LOCAL surface, one row is one game.
* **BASE RATE: 50.00%** — the structural A/A expectation of a seat-balanced
  self-play shard, within the stratum as well as pooled.
* **BASE RATE SOURCE:** `NULL125` (`bots/_v198null125`, a renamed byte-identical
  copy of `_v197mapcode`, against `_v197mapcode`), same 15-map pool, n = 5,400,
  read by this agent from `scratchpad/overnight/NULL125.tsv`: **pooled 51.04%**,
  **900-area stratum 51.61% at n = 1,800** (±2.29pp, interval [49.32, 53.90],
  which contains 50), **sub-900 stratum 50.75% at n = 3,600**.
  ⚠ **DISCLOSED, NOT CORRECTED, AND IT IS THE MOST IMPORTANT CAVEAT ON THIS PAGE:
  the A/A point estimate runs +1.61pp HIGH on exactly the stratum this leg's
  primary bar lives on.** It is inside its own noise, and it is also most of a
  1.00pp MDE. **It is the reason the MDE below is 2.00pp and not 1.00pp.**
  ⚠ Second-order: `NULL125` is a **v125-chassis** cell. **There is no A/A null on
  the v140 chassis at all.** A `NULL140` cell (a renamed byte-identical copy of
  `_v223sealrepair` against itself, 5,400 games) would calibrate this screen and
  every other screen against the live incumbent; it is proposed to the queue here
  and is not a precondition of this leg.
* **BAR: 53.62% or higher**, on the treatment's game share **within the 900-area
  stratum**, at n = 3,600.
* **BAR SOURCE:** constructed, not observed — **`50.00 + MDE(2.00pp) +
  half_width(1.62pp)`**. Half-width computed as
  `1.96·sqrt(p̄(1−p̄)·0.98/3600)` at p̄ = 0.5181, giving **±1.616pp**. **Clearing
  this bar means the 95% interval excludes BOTH 50.00 AND the +2.00pp
  indifference threshold** — the MDE is inside the bar's construction, not beside
  it, so the bar cannot be quoted without it.
* **REFERENCE n: none** — the comparator is generated inside the same shard from
  the same seeds, so no fixed external reference contributes a variance floor.

⚠ **`tools/prereg_check.py` WILL PASS THIS BAR ON A HALF-WIDTH THAT IS NOT THE
ONE THAT BINDS.** Its `BAR_RESOLVABLE` check recomputes the interval at
`PLANNED n = 10,800` (**±0.93pp**) against a margin of 3.62pp and will report
`ok` with room to spare. **The read registered here is on a 3,600-game stratum
whose true half-width is ±1.62pp.** The tool is not wrong; it is not binding.
**The binding arithmetic is the table below and it is done by hand.**

### ⭐ THE PRE-SPECIFIED MDE, AND HOW IT WAS CHOSEN — sized off a value we must EXCLUDE, never one we hope to observe

**MDE: +2.00pp of game share within the primary stratum. WE WILL CALL THIS ARM A
MISS IF ITS TRUE ON-SEGMENT EFFECT IS AT OR BELOW +2.00pp.**

**There is no point estimate of this arm's VALUE anywhere in the world to size
off** — the dose fixture saturated at 32/32 on both arms and measured occurrence
only — **so nothing in this document can be circular in the `#17` sense.** The
threshold comes from three prices, all knowable before any row:

1. **THE FIXTURE'S OWN MEASURED TILT.** The A/A cell reads **+1.61pp** on this
   exact stratum with byte-identical arms. **An MDE at or below that cannot be
   distinguished from the fixture.** 2.00pp is the smallest round value that
   dominates it.
2. **THE ARM REVERTS A COMPLETED SWEEP.** `LATE160 51.42` vs `RES0 48.63`
   (n = 5,408/arm) put the knob at 160 on the merits. Reverting a swept constant
   on one third of the map pool should have to beat that prior by more than
   noise.
3. **THE SHIP FORM IS CONDITIONAL AND DISCOUNTED TWICE.** A positive result here
   ships as a `MAP_CODES`-style per-map branch, and its pooled ladder value is
   bounded at **0.65pp** (segment ceiling below). A sub-2pp LOCAL effect discounts
   below anything the ladder can ever confirm.

**The sizing then follows mechanically rather than being negotiated. Convention
(the house form, `SCREEN-bodyaware`): the fixture must produce an interval
NARROWER than the MDE it registers, with real slack.**

| quantity | value on the PRIMARY stratum |
|---|---|
| stratum n at PLANNED n = 10,800 | **3,600** (5 maps × 2 seats × 360) |
| σ (game share), DEFF 0.98 | **0.824pp** |
| 95% half-width | **±1.616pp** |
| smallest excluded effect at the bar | **2.00pp** |
| **slack (MDE − half-width)** | **+0.384pp** |
| n needed for half-width < 2.00pp | **2,350 stratum ⇒ 7,050 total ⇒ 7,080 (next multiple of 30)** |
| effect detected with 80% power vs 50 | **≥ 2.31pp** |
| effect needed for 80% power to CLEAR the bar | **≥ 4.31pp** |
| n needed for half-width < 1.00pp (an MDE of 1.00) | **9,400 stratum ⇒ 28,200 total** — priced and REJECTED |

**⇒ WHY 10,800 AND NOT 7,080.** 7,080 is the smallest balanced total at which the
2.00pp MDE is expressible — and it lands the half-width at **1.996pp against a
2.00pp MDE, i.e. slack 0.004pp.** That is the `GUNAXABL` trap exactly: **that leg
missed its edge by 0.0152pp, one game, on a bar whose slack was zero by
construction.** 10,800 buys 0.384pp of slack for 3,720 games. **A bar with no
slack produces a verdict with no slack.**

**⇒ WHAT THIS LEG CAN AND CANNOT DO, one sentence each.** It **can** separate "worth
more than two points on 30×30 maps" from "worth two points or less there". It
**cannot** distinguish "worth 1.2pp on-segment" from "worth nothing" — that needs
28,200 games (≈ 25 hours on one corefill worker at the measured 1,125 games/hour)
and is **not** what is being bought. **A ratifier who needs the sub-2pp question
answered should not fire this leg; they should budget a NULL140 cell first and
then four shards.**

**⚠ THE CHEAPER ALTERNATIVE, PRICED SO THE CHOICE IS DELIBERATE AND NOT DEFAULTED.**
A runner restricted to the five segment maps would deliver n_stratum = 5,400 in
**4.8 hours** instead of 14.4, i.e. the same power **3× cheaper**. **It is
rejected, and the reason is the design and not the cost:** the complement stratum
is the only control that can tell "the throws paid" from "something else moved" —
if the treatment gains equally on both strata, the registered mechanism is refuted
whatever the segment column says. **A restricted runner buys power by deleting the
control.** *(It would also require an edit to `tools/overnight.sh`, which this
agent may not make.)*

### FOUR BRANCHES, pre-committed

1. **KEEP (conditional) — stratum share ≥ 53.62%.** The early home launcher pays
   on 30×30 terrain net of its own levy. **It goes to a `MAP_CODES`-conditional
   design note and a live pinned leg, NOT to a submission** — `FIXTURE_OF_RECORD`
   is `live_unrated` and no local branch may ship. **Gated additionally on the
   defence-admission exclusion in "Secondary columns" below, which it does not
   automatically pass.**
2. **REAL NEGATIVE — stratum share ≤ 48.38%.** The interval excludes 50 downward
   on the plank's own best ground. The levy beats the pickup even where the
   pickup fires; `LAUNCHER_MIN_RND = 160` is re-confirmed on the v140 chassis and
   the new pool, and the home-launcher timing road closes **with live-fixture
   backing still owed** per CLAUDE.md point 6 (a local screen may prioritise a
   road, it may not retire one).
   ⚠ **The negative branch is deliberately NOT symmetric with the positive one**
   (1.62pp below 50 against 3.62pp above): an arm that reverts a completed sweep
   is granted no indifference margin on the downside. Stated here rather than
   discovered in the analysis.
3. **DROP BAND — 48.38% < stratum share < 53.62%: COULD NOT SEPARATE.**
   ⛔ Written as *"the screen could not separate the on-segment effect from the
   ≤2.00pp indifference region at ±1.62pp on this fixture"*, **NEVER as "the
   effect is zero"** and never as "the mechanism does not work". The dose showed
   the mechanism fires; this band bounds its worth at roughly ≤2pp locally on
   30×30 maps and says nothing about the ladder.
4. **CHANNEL VIOLATION — the stratum clears 53.62% AND the complement stratum
   also reads ≥ 50.00%.** The arm helps, and **not** by the registered mechanism
   (there is no pickup population on sub-900 maps to explain a gain there). The
   currency reading is banked; **the mechanism claim is BARRED** and a new leg with
   a new mechanism is owed. This branch exists so a favourable number cannot be
   attributed to a story the data does not support.

* **CUT-SHORT: floor 5400 games.** Below 5,400 tape rows nothing is read and no
  branch is claimed; the rows are KEPT and remain poolable with a later completion
  of the same shard on the same seed base, and with nothing else. At
  5,400 ≤ n < 10,800 (stratum 1,800, ±2.29pp) the ONLY claims permitted are
  branches 1 or 2 read at that n's own wider band (KEEP needs ≥ 54.29%, REAL
  NEGATIVE ≤ 47.71%), **never branch 3 — an under-powered shard cannot deliver a
  "could not separate" verdict, because that is what an under-powered shard always
  says.** Floor (5,400) ≤ planned n (10,800).

### Obligation 12 — the futility gates, sized, with one DISARMED and the standing rule REPLACED

**GATE RESOLUTION: the standing corefill futility rule (`RULE-futility-gates-2026-08-13.md`: drop below 48.0% at n≥1000, drop at or below 50.5% at halfway) is written for a leg whose PRIMARY read IS the pooled share, and both ways of applying it to this leg are broken — read on the stratum it is UNRESOLVED at every plausible value (half-width ±5.31pp at n_stratum≈333, ±3.23pp at ≈900), and read on the POOLED share it fires hardest on this leg's own SUCCESS scenario (a segment at the bar against a complement at its predicted −2.8pp pools to 49.34%, i.e. BELOW the standing 50.5% halfway boundary). It is therefore REPLACED, before the fire, by three EXCLUSION gates that are resolvable at their own n, plus one gate DISARMED on the record.**

**The replacement rule, one sentence:** *drop iff the 95% interval at the gate's n
lies entirely below the leg's own pre-computed success scenario.* The success
scenario is fixed here, before any row: **pooled 49.34%** = ⅓ × 53.62 (the bar) +
⅔ × 47.20 (the complement's prior, `RES0`-equivalent).

| gate | n (pooled / stratum) | half-width | **DROP iff** | status |
|---|---|---|---|---|
| **GATE-1000** | 1,000 / ≈333 | ±3.07pp pooled | **pooled share < 46.27%** | ARMED (pooled only) |
| **GATE-2700** | 2,700 / 900 | ±1.87pp pooled | **pooled share < 47.47%** | ARMED (pooled only) |
| **GATE-5400** | 5,400 / 1,800 | ±1.32pp pooled · ±2.29pp stratum | **pooled share < 48.02% OR stratum share < 47.71%** | ARMED (both) |
| **STRATUM GATE at n<5400** | ≈333 / ≈900 | ±5.31 / ±3.23pp | — | **DISARMED** |

* **THE DISARMED GATE IS DECLARED, NOT OMITTED, AND THIS IS THE OB12 POINT.** A
  stratum-side futility read before n = 5,400 has a half-width of ±5.31pp
  (at 1,000) or ±3.23pp (at 2,700) against boundaries 1–2pp from the null. **It
  cannot produce a reading in either direction at ANY value of its own statistic.
  That is an INERT gate, not an UNRESOLVED one**, and the difference matters:
  pre-committing an inert gate to the restriction would DROP the leg on 100% of
  runs, which is a stop rule carrying no information. **An inert gate is
  disarmed in advance and says so; an unresolved gate takes the restriction.**
* **THE UNRESOLVED DEFAULT, where it still applies.** Each ARMED gate above is an
  exclusion test, so every reading resolves into drop / continue. **Where any gate
  reading cannot be computed at all (a corrupt or short tape at the boundary), the
  gate is UNRESOLVED and takes the RESTRICTION — for a futility gate the
  permission is CONTINUING to spend cores, so the restriction is the DROP.**
* ⚠ **THE LANE MUST RATIFY THIS SUBSTITUTION EXPLICITLY.** It departs from a
  standing Magnus rule and from the form `SCREEN-bodyaware` used last night. **The
  departure is forced by the stratified primary and by nothing else**; a
  pooled-primary leg should keep the standing gates unchanged.
* **A futility drop is NOT a refutation.** Rows are kept, the dose evidence
  stands, the arm remains a combo ingredient, and the record line carries the
  label, the n and both shares.

---

## MECHANISM METRIC — and the pre-fire gate, because the shard tape cannot carry it

**MECHANISM METRIC READS: bots/_v250homeearly/main.py:616 — the round gate inside `_try_build_launcher`, observed as (M1) the round of our first LAUNCHER creation and (M2) the count of enemy-builder EXILE throws, both decoded off the replay wire by `tools/corpus/replay_throws.py`. TREATMENT DIFF TOUCHES: bots/_v250homeearly/main.py bots/_v250homeearly/doctrine.py. INTERSECTION: yes — M1 is the direct output of the line the diff rewrites, and M2 is downstream of it with no other gate between; the metric cannot read identically in both arms because the control's gate is 160 and the treatment's is 24.**

**TREATMENT DIFF REFS: --no-index bots/_v223sealrepair bots/_v250homeearly**
(verified at draft: `git diff --name-only --no-index bots/_v223sealrepair
bots/_v250homeearly` returns exactly `bots/_v250homeearly/doctrine.py` and
`bots/_v250homeearly/main.py`. **This form is used deliberately instead of a
ref-pair: both trees are committed at the same HEAD, so `git diff HEAD` is empty
for this arm and OB13's intersection would report CANNOT-COMPUTE at lock and
FAIL under `--fire`.** The directory diff is also the semantically correct object
— the treatment is defined against the control tree, not against a parent
commit.)

**METRIC WINDOW: r24-r1000. GATING CONSTANTS: LOKI_HOMEEARLY_RND=24, LAUNCHER_MIN_RND=160. MECHANISM CAN OCCUR IN WINDOW: yes.**

⚠ **`prereg_check` WILL EMIT A PARTIAL-WINDOW WARN HERE AND IT IS NOT A DEFECT —
IT IS THE TREATMENT.** `LAUNCHER_MIN_RND = 160` sits inside r24–r1000, so the tool
will note that r24–r159 cannot contain the mechanism. **That is true of the
CONTROL arm and false of the treatment arm, and the asymmetry IS the plank.**
OB17 exists to catch a metric gated off in **both** arms (`#60` read
`get_scale_percent()` at r50/r100/r150 against this very constant); here the
binding gate in the treatment is `LOKI_HOMEEARLY_RND = 24` and the window opens
exactly on it. `main.py` contains **exactly one** name matching OB17's round-gate
pattern (`LAUNCHER_MIN_RND`), it resolves to a single value (160, from
`doctrine.py:1536` via the tree's `import`), and it is referenced inside the
metric's own function — so the assertion is computed, not declared.

⛔ **THE SHARD TAPE CANNOT CARRY M1 OR M2 AND MUST NOT BE ASKED TO.** The row
schema is `ts shard game map seed seat winner cond turns` and the runner uses
`--replay /dev/null`; there is no mechanism column, and our own `print()` output
is stripped on the platform anyway. **The instrument is a separate replay-keeping
probe, and it runs BEFORE the shard.**

### ⭐ PRE-FIRE DELIVERY GATE — the shard may not be SCORED until this passes

**Run `tools/dose.py`-style pairs of `bots/_v250homeearly` and
`bots/_v223sealrepair` against EACH OTHER (treatment as team A and as team B),
with `--keep-replays`, on the five 900-area maps, 8 seeds × 2 seats = 80 games per
arm, and decode with `tools/corpus/replay_throws.py`.** Required:

| gate | control (predicted) | required of the treatment | why this number |
|---|---|---|---|
| **G1 — share of treatment games on 900-area maps carrying ≥1 EXILE throw** | **0%, by construction** (`LAUNCHER_MIN_RND=160` and median build r318) | **≥ 10%, with the 95% lower bound above 10%** | the screen's opponent is our own raid line, not the camping `_probe_creeper`; below this the shard measures the LEVY only and its null is a fixture artefact |
| **G2 — median round of our first LAUNCHER creation** | **≥ 160 by construction** | **≤ 60** | separates "the gate lifted but the build still did not land" (role/`LAUNCHER_RESERVE=80`/`SLOT_HARVESTERS` gates, `main.py:642-644`) from "the build landed and nothing walked into it". Without G2 a G1 failure is uninterpretable |
| **G3 — decoder accounting** | `vfate`/`vlife` populated on EXILE rows | same | `replay_throws.py`'s own docstring records that EXILE victim columns were a constant `-1/0/0/0` until s42; **a constant column validates anything** |

**G1 RESOLUTION, per Obligation 12 — sized in COUNTS, because a percentage hides
which readings the gate can actually tell apart.** Wilson 95%, n = 80 treatment
games on the stratum:

| reading | Wilson 95% | verdict |
|---|---|---|
| **≤ 2 / 80** (≤ 2.50%) | 2/80 → [0.69, **8.66**] | **FAIL, resolved** — the interval excludes 10% |
| **3 – 13 / 80** (3.75 – 16.25%) | 8/80 → [5.15, 18.51] | **UNRESOLVED** |
| **≥ 14 / 80** (≥ 17.50%) | 14/80 → [**10.10**, 26.87] | **PASS, resolved** |

**The pre-committed default on an UNRESOLVED reading is the RESTRICTION: do not
fire the 10,800-game shard. Raise the gate probe to 240 stratum games** (≈ 13
minutes at the measured throughput) **and re-read ONCE**, where the bands become
FAIL ≤ 14/240 (5.83%), PASS ≥ 34/240 (14.17%), UNRESOLVED 15–33.
⚠ **AND THE SECOND READ IS THE LAST ONE, because a true rate sitting ON the 10%
boundary is unresolvable at any n** (OB16: `p → bar ⇒ n → infinity`). **A second
UNRESOLVED reading takes the restriction and the leg does not fire** — it is not
an invitation to a third probe.

**A failure of G1 or G2 means the arm was not delivered as specified against THIS
control.** The shard is then not fired, and the reading banked is *"HOMEEARLY's
throw mechanism does not fire against our own tree, so its dose against
`_probe_creeper` does not transfer to self-play"* — **a real finding about the
FIXTURE, and one that also tells the live-leg design which opponents are worth
pinning.**

**PRE-STATE (Obligation 7): neither the outcome nor the mechanism is already in
its predicted state.** **Outcome:** no HOMEEARLY reading exists on this chassis or
this pool; the only reading on the cell is the structural 50.00% of a bot against
itself (A/A control 51.61% on the stratum, interval containing 50), so the
predicted 53.62% is demonstrably NOT already there. **Mechanism:** the control's
EXILE-throw count in r24–r159 is **zero by construction** and its median launcher
build is r318, so a null cannot be blamed on a treatment that was already true.

---

## Secondary columns — the DEFENCE ADMISSION BAR, written as an EXCLUSION

**THIS PLANK IS DEFENSIVE AND IS REGISTERED AS SUCH.** `main.py:618-620` says it in
the tree's own words: *"~70% of all launcher activity in the field is defensive
disposal and ours is ~97% defensive — so this is bought as home defence first and
as the raid ferry second."* The plank throws away enemy builders creeping at our
core. `PROGRAMME.md` carries **`PLAY_DEFENCE: not_at_the_kill_s_expense`** and
**`DEFENCE_ADMISSION_BAR: kill_round_non_regression`**, so a kill-round bar rides
beside the currency bar and the arm is **inadmissible without it**, whatever the
game-share column says.

⛔ **AND IT IS WRITTEN AS AN EXCLUSION BEFORE ANY CORRECTION IS CONSIDERED, per
CLAUDE.md's DEFF direction clause.** *"HOMEEARLY did not slow the kill"* is a
FAIL-TO-EXCLUDE claim and **may not be banked in that form** — widening an
interval makes exactly that claim EASIER, which is how a design effect launders a
weak null into a confident one. The admissible form is:

* **D-KILL (the admission bar, on the primary stratum).** Median `turns` over rows
  with `cond == core_destroyed` won by the treatment, against the same statistic
  for the control, within the 900-area stratum. **ADMITTED IFF the 95% bootstrap
  interval (10,000 resamples) on the difference of medians EXCLUDES a +10-round
  regression.** If it does not, the column reads **UNRESOLVED**, no kill-round
  claim is made in either direction, and **the arm is not admitted as a defensive
  plank** — branch 1 does not fire.
  **A/A noise floor, measured for this bar rather than assumed** (`NULL125`,
  byte-identical arms, same pool): **0.0 rounds on the 900-area stratum** (T 191.0
  vs C 191.0, n = 819 / 774 core-kill rows) and **+3.0 rounds pooled** (T 211.5 vs
  C 208.5). **The +10-round threshold is >3× the pooled floor and infinitely above
  the stratum floor.**
  No design-effect inflation is applied: same fixture, DEFF 0.98, MATCH and
  OPPONENT clusters dead, MAP cluster measured at 0.64 on this stratum.
* **D-R1000 — share of rows with `cond == tiebreak`, per arm, per stratum.**
  **Predicted UP** if the levy slows our own economy; `R1000_IS_DEFEAT` is
  unconditional, so a rise is a cost even when the currency column is flat.
  Reference density from the same A/A cell: **11.50% on the 900-area stratum**,
  **8.36% sub-900**, **9.41% pooled**. **DESCRIPTIVE — no bar, no branch.**
* **D-WINDOW — share of the treatment's core-kill wins landing at `turns` ≤ 250**
  (`KILL_WINDOW_RND: 250`), per arm, per stratum. **DESCRIPTIVE**, reported beside
  D-KILL so a median that moves 3 rounds cannot hide a tail that moved 100.

---

## RATIFY: Segment

**MAP SEGMENT: the 900-area class — midgard, ragnarok, valkyrie, drakkarfjord, glacierkeep — 5 of the 15 pool maps, all 30×30, and the ONLY primary segment declared by this document. Mechanism reason: the plank's pickup opportunity is an ENEMY BUILDER DWELLING inside our home launcher's d²≤2 envelope, and dwell inside our half scales with the length of the enemy's approach; the banked dose separated PERFECTLY on this axis (2 of 2 probed 900-area maps fired — ragnarok 4/4 games, midgard 3/4 — against 0 of 6 sub-900 maps).**

**EXPECTED DIRECTION: POSITIVE on the 900-area class; NEGATIVE on its ten-map complement.**

**SEGMENT VALUE CEILING: 32.5% x 2.00pp = 0.65pp** — pairing share × on-segment
effect at the registered MDE. The share is **measured, not assumed**: the five
900-area maps are **231 of 710 rated games (32.54%)** in the post-2026-08-13
rotation era of `corpus/ladder_games.tsv`, which is within half a point of the
local fixture's structural 33.3%. ⇒ **A POSITIVE RESULT HERE CAN NEVER BE
CONFIRMED POOLED. Any confirmation must be read ON-SEGMENT, and this sentence is
registered now so that it is not negotiated later.**

### Why RESTRICTED and not POOLED — decided before any row, with the counter-argument stated

**This is the judgement the document exists to make, so it is argued rather than
asserted, and both sides are on the page.**

**THE CASE FOR POOLING, and it is real** (`tools/map_admits.py`'s own docstring
makes it): *"jackpot is KEPT on the panel … that is a real property of the plank
and deleting the map would delete the evidence for it."* Here the argument is even
stronger than in the `jackpot` case, because **this plank's PRICE is universal
while its BENEFIT is conditional** — the +10% scale levy is paid at r24 on all
fifteen maps, including the ten where the dose read exactly zero. A restricted
read measures the benefit where it fires while the price is paid everywhere.

**WHY IT LOSES ANYWAY — arithmetic, not preference.** Under the leg's own
hypothesis (segment at the bar, complement at its `RES0`-equivalent prior), the
POOLED share is **⅓ × 53.62 + ⅔ × 47.20 = 49.34%.** **A pooled primary would
therefore read a SUCCESS as a small negative and close the road** — Obligation
15's stated failure mode verbatim: *"a pooled screen does not measure a
conditional plank weakly, it measures it as ZERO, and the road closes."* And the
ten zero-dose maps are not hard cells; **they are dead denominators for the
mechanism** — `map_admits`'s other half — because there is no pickup population
on them for the launcher to act on.

**HOW THE PRICE IS KEPT ON THE PAGE RATHER THAN HIDDEN — and this is what makes
the restriction honest.** The complement is **not** deleted and **not**
descriptive-only: it is registered with its own pre-committed direction
(NEGATIVE), it is one of the two inputs to every futility gate, and it is the
subject of **branch 4**, which BARS the mechanism claim if the treatment gains on
both strata. **The restriction changes which stratum carries the VERDICT; it does
not remove a single game from the reading.** A pooled column is reported for
completeness and **may not rescue or defeat the registered read.**

**THE THREE HONEST WEAKNESSES OF THIS SEGMENT, stated before the data:**

1. **THREE OF THE FIVE SEGMENT MAPS WERE NEVER PROBED.** The dose covered
   midgard and ragnarok; **valkyrie, drakkarfjord and glacierkeep were not in the
   probe's 8-map set at all.** Registering them is a **PREDICTION**, and a
   falsifiable one: if the effect is confined to ragnarok and midgard while the
   three unprobed 30×30 maps read flat, the segment as declared is **wrong** and
   the honest label is "a two-map effect", not a size-class effect. **That is a
   real way for this registration to be caught out, and it is the reason the class
   is declared rather than the two maps that fired.**
2. **THE SEGMENT IS A SIZE CLASS, WHICH OB15 WARNS IS A PROXY.** The mechanism
   names APPROACH LENGTH, and area is a proxy for it. **A direct threshold on
   core-to-core distance would be a better segment and is deliberately NOT used**,
   because the threshold would have to be chosen to fit an observed 2-vs-6 split —
   subgroup fishing wearing a mechanism's clothes. **The 900-area class is the
   repo's own standing vocabulary term** (obligations doc, Addendum 10), defined
   before this plank existed and chosen by nobody here. **Provenance is the
   defence against fitting.**
3. **THE DOSE'S MAP SPLIT IS THIN.** 4 games per map per arm, on a saturated
   fixture, against a probe we wrote. **162 of 183 throws come from one map.**

**A PER-MAP COLUMN IS REGISTERED — DESCRIPTIVE, with NO bar and NO branch**, so a
successor can define the segment properly over all fifteen maps.
⛔ Per Obligation 15c, **a segment suggested by these rows requires a NEW leg with
its own n and its own seed base; the rows that suggest a segment may not also
confirm it.** The 900-area stratum reading is this leg's verdict.

---

## RATIFY: FALSIFIER

**FALSIFIER: the treatment finishes at or below 48.38% game share on the 900-area stratum at n = 3,600.** That refutes the hypothesis outright on the plank's own
best terrain: the +10% early scale levy beats the pickup even where the pickup
fires, `LAUNCHER_MIN_RND = 160` is re-confirmed on the v140 chassis and the
post-rotation pool, and the home-launcher-timing road narrows to designs that
change WHERE the launcher goes (LAUNCHMAX's T3) rather than WHEN.

Four further pre-committed off-prediction outcomes, each landing somewhere other
than "the arm is good":

* **DELIVERY falsifier (pre-fire gate G1).** Fewer than 10% of the treatment's
  900-area games carry an EXILE throw against our own tree. The mechanism does not
  fire on this fixture; the shard is not fired; the finding is about the fixture
  and about which opponents a live leg must pin, not about the currency.
* **BUILD falsifier (pre-fire gate G2).** The treatment's median first-launcher
  round is above 60. The gate was lifted and the build still did not land — the
  binding constraint is `LAUNCHER_RESERVE = 80` / role assignment /
  `SLOT_HARVESTERS`, not the round gate, and **`#28`'s reserve question reopens as
  the actual lever**.
* **SEGMENT falsifier.** The stratum clears its bar, but the per-map column shows
  the effect confined to ragnarok and midgard with the three unprobed 30×30 maps
  flat. **The declared segment is wrong**; the result may be banked as a two-map
  effect only, its ceiling drops to ~13% × effect, and a new leg is owed.
* **CHANNEL falsifier (branch 4).** The stratum clears its bar while the
  complement also reads ≥ 50.00%, or while **D-KILL rises by ≥10 rounds** and
  **D-R1000 rises**. The arm then wins by some route other than early home denial;
  under `R1000_IS_DEFEAT` and `DEFENCE_ADMISSION_BAR` that is not the plank that
  was registered and it may not be banked as one.

---

## Interaction with the live legs — required line

At draft (`ps`, `scratchpad/corefill.log`, `scratchpad/overnight/*.heartbeat`,
2026-08-15T06:55Z):

* **`BODYAWR`** (`bots/_v242bodyaware` vs `bots/_v223sealrepair`, seed base
  336000, **7,577 / 10,800**) is the ONLY shard running, on **one** corefill slot
  (`corefill.sh … 1 12`). Its diff is `eco.py:809-896` (`_bfs_direction`) —
  **different module, different function, no shared line with `main.py:593-666` or
  `doctrine.py:1536-1558`.**
* **`NULL5400`** (`bots/_v146null` vs `bots/_v146gunaxis`, 5,400, seed 344000) is
  queued and unstarted.
* **`LAUNCHMAX`** (`bots/_v243launchmax`, 5,400, seed 340000) is pre-registered
  and not yet in the worklist. **It shares the launcher family with this arm but
  not one line of code** (its diff is `raid.py` + `doctrine.py`'s forward-eviction
  block; T1 is explicitly NOT lifted there). **Separate shards, disjoint seed
  bases, each measured independently against the same control ⇒ no confound.**

⇒ **THE REAL INTERACTION IS RESOURCE, AND IT IS THE ONE COST THE LANE SHOULD
WEIGH.** Measured throughput on the current single worker, from BODYAWR's own tape
(7,576 rows between 2026-08-15T00:03:31Z and 06:47:37Z): **1,125 games/hour.**
A 10,800-game shard is **≈ 9.6 hours of one worker**, and it queues behind
BODYAWR's remaining ≈ 2.9 h and NULL5400's ≈ 4.8 h — **≈ 17 hours to completion at
the present board.** Options, priced, for the lane to pick: raise `corefill.sh`'s
`max_shards` above 1; stock this arm on `work-server-2` instead (**reported
separately, never pooled** — the s42 cross-host rider); or accept the queue. **The
pre-fire gate is unaffected either way: it costs ~160 games and should be run
first regardless of when the shard starts.**

**⛔ ONE ORDERING RULE FOR THE NEXT LEG, recorded here so it is not rediscovered
in an analysis.** HOMEEARLY changes the round at which the +10% launcher levy is
levied, which is the input to every economy-timing arm on this chassis
(`#28` `LAUNCHER_RESERVE`, `TINYECO62`, the ammo family). **On any shared stratum
those must not be measured concurrently with HOMEEARLY in the same tree.** This
leg is a single-arm screen against the incumbent and confounds nothing today.

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: Obligations 1-17, the OB16 corollary and the s42 cross-host rider) · `docs/prereg/SCREEN-bodyaware-2026-08-14.md` (house template and most recent locked example) · `PROGRAMME.md` · `CLAUDE.md` · `tools/prereg_check.py` (read for the required tokens, the DEFF table, `check_arithmetic`, `check_metric_window`, `check_pool_era`) · `tools/map_admits.py` (dead-denominator docstring and the `jackpot` counter-argument) · `tools/overnight.sh` · `tools/corefill.sh` · `tools/dose.py` · `tools/corpus/replay_throws.py` · `docs/prereg/RULE-futility-gates-2026-08-13.md` · `docs/prereg/SCREEN-launchmax-2026-08-15.md` (the sibling launcher prereg; §1 T1/T2 decisions) · `docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md` (the launcher-family finals and `#24`/`#28` closures) · `docs/research/BUILDER-TACTICS-ATLAS-2026-08-14.md` (the -6.34pp premium line) · `bots/_v250homeearly/main.py` · `bots/_v250homeearly/doctrine.py` · `bots/_v223sealrepair/main.py` · `bots/_v223sealrepair/doctrine.py` · `scratchpad/corefill_work.txt` · `scratchpad/corefill.log` · `scratchpad/overnight/NULL125.tsv` (A/A calibration; base rate, kill-round floor, tiebreak density and the per-map design effect were computed from it by this agent) · `scratchpad/overnight/BODYAWR.tsv` (throughput only) · `scratchpad/dose_he2/` (the dose fixture's replay filenames, read to recover its 8-map set) · `corpus/ladder_games.tsv` (the 32.54% post-rotation pairing share) · `maps/*.map26` via `tools/map_admits.py:_terrain` (map dimensions) · git commit `01e0a411` (the dose) and `3d303baf` (the arm tree's add). No file under `bots/`, `tools/`, `scratchpad/`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.
