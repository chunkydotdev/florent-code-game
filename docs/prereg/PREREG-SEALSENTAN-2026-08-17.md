# SCREEN PREREG — `SEALSENTAN`: a SENTINEL on the enemy seal seat, with NO eco-deferral

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: committed BEFORE the `SEALSENTAN` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/SEALSENTAN.*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T05:20:53Z`** (`date -u`,
same shell call); repo HEAD at draft `6bb6a947` (author time
`2026-08-17T07:20:22+02:00`). Verified at draft:
`grep -c 'SEALSENTA\b\|SEALSENTAN' scratchpad/corefill_work.txt` → **0**;
same grep on `docs/prereg/BARS.tsv` → **0**;
`ls scratchpad/overnight/ | grep -i sealsent` → **empty**;
`grep -cE '81[24]000' scratchpad/corefill_work.txt` → **0** (the seed base is free).

### SECOND CLOCK — and the brief's boilerplate correction did NOT survive my check
My drafting brief instructed me to avoid the `# FIXTURE … start=` stamp on the
grounds that it "names an artifact that does not exist". **That is false and I
am registering the correct method rather than the one I was handed.**
`tools/overnight.sh:99-101` stamps `START=$(date -u …)` and writes
`# FIXTURE\tshard=…\tstart=$START\trunner=tools/overnight.sh` as the tape's first
line **before the first `fcode run`**, on any tape that does not already exist.
⇒ **PRIMARY second clock: this commit's git author time against the
`SEALSENTAN.tsv` `# FIXTURE … start=` stamp** (a START, not a first-completed-row).
**BACKSTOP, registered now so no judgement is made later:** if the tape carries
`# FIXTURE-RESUME … start=UNKNOWN-legacy-tape` instead (`tools/overnight.sh:105`),
or carries no `# FIXTURE` line at all, the second clock is **the `ts` of the FIRST
COMPLETED ROW** — conservative, because the true start is strictly earlier and the
gap can therefore only be OVERSTATED, never understated.

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v481sealsentAnofund`,
added `aba27582`, author time `2026-08-17T07:13:50+02:00`; it is the funding
ablation of `bots/_v474sealsentA`, added `493df130`, `2026-08-17T07:07:12+02:00`).
This document is therefore **NOT** locked before the arm exists, only before the
arm's first screen row. Said here rather than left for a certifier to find. It is
also what makes Obligation 13's intersection **computable at lock time**.

---

## ⛔ READ BEFORE RATIFYING — FIVE THINGS THE LANE OWNS

**1. THE CONTROL IS THE LIVE INCUMBENT, SO 50.0 MEANS "ADDS NOTHING".**
`bots/_v468kladturbo` is Sleipnir v1, pinned as the corefill control at
`scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`).
Every number on this page is denominated against the thing we currently ship, per
Magnus's instruction that all our bots compete against Sleipnir during core
shards. **A reader who transplants a 61-shaped intuition from the
KLADTURBO-vs-v140 read onto this page has misread the fixture: the same bot
measured against itself reads 50.**

**2. ⛔ "THE DEFERRAL IS THE POISON, NOT THE PLANT" IS THE HYPOTHESIS UNDER TEST
ON THIS PAGE. IT IS NOT BACKGROUND, AND IT MUST NOT BE WRITTEN AS THOUGH IT WERE.**
An earlier form of the drafting brief said *"three surfaces already agree"*; the
side lane retracted that before this draft was written and the honest inventory is:
* **ONE REGISTERED ARM — `KLADLADDER`** (`results.tsv`, rows
  `kladladder-final-attribution` / `kladladder-n-final-correction`, **41.86%
  [40.20, 43.52] at n = 3,404**, dose battery **DOSE DELIVERED**, 1.58 vs 0.75
  forward sentinels/game). That is **outcome and mechanism of the SAME
  treatment** — it licenses attribution about ITSELF, and it is one arm, not
  three surfaces. Its finding is that a **committed** forward-sentinel plank
  SUBTRACTS ~8pp from Sleipnir. Its mechanism CANDIDATE (builder deaths 1.91x,
  forward deaths 2.25x) is explicitly typed on that tape as **diagnostic, not
  verdict**, and carries two caveats that travel with it everywhere:
  **correlation inside 24 games**, and **a dose DIFFERENCE, not
  presence/absence — the control plants 0.75 forward sentinels/game itself.**
* **ONE UNREGISTERED BUILD DEMO** — the sealsent deferral gradient recorded in
  `bots/_v481sealsentAnofund/doctrine.py:1403-1420`: nofund 54.2% [40.3, 67.4],
  A 37.5% [25.2, 51.6], B (N=2) 22.9% [13.3, 36.5], **48 matches per arm,
  `tools/arena.py`, no `results.tsv` row, no gate, no registration.** The tree's
  own comment already prices the A-vs-nofund contrast at **z ≈ 1.64, p ≈ 0.10**
  and states that neither interval excludes 50.
⇒ **These are PRIORS and an EXPECTED DIRECTION. They are cited nowhere on this
page as evidence, they carry no n-weight in any verdict, and no band below is
chosen to accommodate them.**

**3. THE PRE-STATE IS CLEAN, WHICH IS THE OTHER HALF OF POINT 2.** The
deferral-is-the-poison claim cannot be pre-satisfied here because the control has
**no seal-sentinel machinery at all** — `grep -c LOKI_SEALSENT bots/_v468kladturbo/*.py`
→ **0 in all four files**; `grep -c _sealsent_` → **0 in all four files**. And
the two sealsent trees do **not** inherit KLADLADDER: `grep -c LOKI_LADDER_ON`
→ **0** in both. This arm is the plant on the bare Sleipnir base.

**4. THIS ARM IS *NOT* "THE PLANT WITH ALL FUNDING PRESSURE REMOVED", AND
MIS-READING THAT WOULD MIS-ATTRIBUTE A BAND-4 RESULT.**
`LOKI_SEALSENT_FUND_ON = False` removes the **ECO-DEFERRAL** (the want-beat
reserve). It does **not** remove the **SPEND-DOWN**:
`LOKI_SEALSENT_TI_FLOOR = 0` is set in BOTH arms, so the seat sentinel is still
bought with the reserve floor waived — the same *shape* of waiver that
KLADLADDER's mechanism candidate points at. **⇒ if SEALSENTAN lands in Band 4,
the honest attribution is "the plant plus its waived floor subtracts", NOT "the
plant alone subtracts". Separating those needs a third arm with a non-zero
`LOKI_SEALSENT_TI_FLOOR` and is out of scope here.**

**5. THE SHARD TAPE CANNOT SEE THE MECHANISM, AND A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--replay /dev/null` and the tape's columns are
`ts shard game map seed seat winner cond turns` — **no entity, build or turret
information exists on it, in either arm.** The plank's mechanism is CONDITIONAL
(establishment gate, harvester gate, shared forward cap, N-cap census, site
filter), so `docs/prereg/BARS.tsv`'s FIRINGS-BEFORE-PRIMARY rule binds.
⛔⛔ **AND THE ORDERING IS WRITTEN OUT EXPLICITLY BECAUSE THE RULE WAS INVERTED ON
ITS FIRST FIRING TODAY.** `results.tsv:kladladder-verdict-amendment-f1f2-pending`
records the builder typing KLADLADDER's Band-4 primary **before** its registered
F1/F2 battery read, then amending. **That is a procedural datum on the tape, the
builder is on notice, and this prereg registers the ordering as a hard sequence:**
> **D1/S1 (below) are READ, and their numbers written down, BEFORE any sentence
> containing the primary share is typed.** A primary typed ahead of the dose read
> is a REGISTRATION BREACH regardless of what it says, and the repair is the
> amendment chain KLADLADDER used, not a re-write.

---

## RATIFY: Hypothesis

**Replacing ONE enemy-core heal-seat barrier with a firing-line-sited SENTINEL
(N = 1, seat band only), on the `bots/_v468kladturbo` base and with NO eco
deferral, raises our LOCAL pooled game share against `bots/_v468kladturbo`
itself to 51.33% or higher at n = 5,400 games across all 15 corefill maps and
both seats.**

**Provenance of the idea, verbatim (Magnus, s48):** *"Can we test a few builds
where we place sentinels on some spots instead of barriers around their core? Be
aware that if we allow our builders to build unlimited harvestors they will take
the titanium from our offensive builders trying to set up turrets."* **This arm
is the FIRST half of that directive with the SECOND half deliberately switched
OFF** — the contention guard Magnus's warning motivates is `SEALSENTA`, screened
under its own prereg, and the pair is what prices the warning.

**The mechanism claim, stated so it can be wrong.** The plank does three things
and the hypothesis is that the first outweighs the other two:
* **IT UPGRADES THE SEAL.** A seat that would have taken a 3 Ti / 20 HP barrier
  takes a 40 HP turret that also SHOOTS — sited only where `can_fire_from` puts
  an enemy CORE tile in its line, scored by ring rake (core tiles ×3, seats ×1),
  so the spend buys the widest field of fire available rather than the first
  legal tile (`raid.py:720-828`).
* **IT COSTS FAR MORE THAN A BARRIER, AND NOT 30 Ti.** The tree's own demo
  measures `get_sentinel_cost()` at **42 Ti at r1 and 67-81 Ti through the siege
  window**, because the ONE GLOBAL ADDITIVE cost factor is already 1.4-2.7x by
  then. **No number on this page quotes the base 30.** That titanium is not
  spent on economy.
* **IT CAN LEAVE A SEAT OPEN.** While a site qualifies and the bank does not,
  the barrier loop SKIPS that one seat (`raid.py:307`) for up to
  `LOKI_SEALSENT_HOLD_MAX = 12` raider-rounds. An open enemy heal seat is exactly
  what the collar exists to close.

**⇒ A flat result is INFORMATIVE and is not a null about "sentinels on seats".**
It would say the upgrade pays for its own cost and its own hold — which, given
that the barrier it replaces costs 3 Ti, is already a non-obvious finding.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). There is no opponent churn to pin against and no calibration relevance to protect.**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe. Both clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit), i.e. naive intervals are correct and marginally conservative. **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and applying them would widen every interval here 24-35% for correlation that has been measured absent.**
**ESTIMATOR: unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never the bar — seat is worth ~6.8pp on byte-identical arms, which is why the n is a multiple of 30.
**DOSE: seat-band sentinel plants — treatment ≥1 vs flag-off control 0, to be measured at n=48 games (the registered D1 battery size below).** The control's zero is **structural, not measured at lock, and that is stated rather than dressed up**: `LOKI_SEALSENT_ON = False` makes `_sealsent_try` return `(False, None)` at `bots/_v481sealsentAnofund/raid.py:861` before any board read, `hold` stays `None` at `raid.py:293`, the barrier loop's skip at `raid.py:307` can never match, and the control tree contains the string `LOKI_SEALSENT` **0 times in all four files** (verified at draft). ⛔ **NO UNIT PROBE WAS FIRED FOR THIS LINE.** The registered **D1 dose battery** below is what converts it from a code claim into a measured one, and D1 is registered to run BEFORE the primary is typed.
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:66` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: this tape carries an unprefixed header line, and a naive `wc -l`/`awk '!/^#/'` over-reports n by exactly one (measured today on KLADLADDER, `results.tsv:kladladder-n-final-correction`). The registered denominator is **DictReader row count, cross-checked against the heartbeat and against `max(game id) + 1`.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this leg publishes descriptive tallies (share, per-seat, per-map, kill-round) and takes **NO comparative look and no bar verdict**; the half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on, so a sub-2,700 read cannot resolve its own branches. An `auto_gate` cancellation at CATASTROPHE@400, MARK-1000 or TREND-FLOOR@1000 is an **OPERATIONAL STOP, not a verdict**, and is typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED, AND IT IS THE ONE KLADLADDER USED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 4, so a stop under that clause DOES license the Band-4 falsifier sentence at the partial n — **provided D1/S1 have been read first** and provided the partial share is disclosed as **selected-pessimistic** if the stop was taken on an interim look.
**BAR: 51.33. MDE: 0.00pp — THIS IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE.** Per the OB16 corollary (obligations doc, 2026-08-15T03:52:45Z): the standard corefill band IS `50 ± half_width` at n=5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes **no positive effect size whatsoever**. n for the exclusion it CAN make (bar ≠ 50.0): **5,400**, which is the planned n.
**BASE RATE: 50.00**
**BAR SOURCE:** house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO` and `KLADLADDER`, which is what keeps this arm numerically comparable to the sentinel-family reads it exists to extend. **Constructed, not observed.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base. Empirically calibrated by `IDNULL140` — **49.27% [47.94,50.60] at n=5,400**, 2026-08-16T18:02:04Z, same host and fixture (`results.tsv:idnull140-cert-5400`) — and previously by `NULL125` — **51.04% at n=5,400** (`results.tsv:null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it. ⇒ **a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced**, which is why Band 2 below is pre-registered as WEAK.
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:66`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.)
**REFERENCE n: none** — the comparator is generated inside this same shard from the same 5,400 seeds; there is no fixed external reference sample, so no resolution floor at n→∞.
**TREATMENT TREE: bots/_v481sealsentAnofund**
**TREATMENT DIFF REFS: aba27582^ aba27582**
**MECHANISM METRIC READS: bots/_v481sealsentAnofund/raid.py:950 — the `ct.build_sentinel(tile, facing)` call inside `_sealsent_try`, the single line whose execution IS the dose (a seat-band sentinel bought on a tile the barrier loop would otherwise have walled). Observed as D1 (forward-sentinel builds per game, treatment vs control, `tools/dose.py --kind sentinel`) and S1 (the `d2_enemy` distribution of sentinel BUILD events, which is the only decodable discriminator between a SEAT plant and the control's corner plant — see MECHANISM DIAGNOSTICS). TREATMENT DIFF TOUCHES: bots/_v481sealsentAnofund/doctrine.py bots/_v481sealsentAnofund/eco.py bots/_v481sealsentAnofund/main.py bots/_v481sealsentAnofund/raid.py. INTERSECTION: yes — `raid.py:950` is inside the 316-line block the diff ADDS at `raid.py:672-988`; the whole `_sealsent_*` family did not exist in the control at all (grep for `_sealsent_` across the four control files returns 0 in every one, verified at draft), so the metric CANNOT read identically in both arms.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_SEALSENT_MIN_HARV=2, LOKI_SEALSENT_HOLD_MAX=12, LOKI_SEALSENT_MAX=1, LOKI_FWD_GUN_CAP=3. MECHANISM CAN OCCUR IN WINDOW: yes** — **NOT ONE of these four is a ROUND FLOOR.** `LOKI_SEALSENT_MIN_HARV` is a HARVESTER COUNT, `LOKI_SEALSENT_MAX` and `LOKI_FWD_GUN_CAP` are TURRET COUNTS, and `LOKI_SEALSENT_HOLD_MAX` is a per-raider BUDGET of rounds, not an earliest round. The plank has **no round gate whatsoever**: it arms the first turn a raider is established at the enemy ring (`dsq_core(p) <= LOKI_ESTABLISH_DSQ = 40`, `raid.py:866`) with 2 harvesters on the board, and the demo recorded in the tree plants at **r24 on drumlin s3**. The window is the whole game because a REPLANT can occur at any round — the N-cap census reads the LIVE board (`raid.py:678-719`), so a dead seat sentinel frees its slot.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` will emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE ARTEFACTS OF THE CHECKER.** Its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a harvester count of 2 is reported as "rounds r0-r1 cannot contain the mechanism". The constants are declared anyway because they are the gates that actually bind, and an undeclared gate is the failure the obligation exists for.
**GATE RESOLUTION: the shard is governed by the pinned `tools/auto_gate.py` marks — CATASTROPHE@400 (STOP if the 95% CI upper < 45.0), MARK-1000 (STOP if the CI upper < the registered BAR 51.33), TREND-FLOOR@1000 (STOP if the first-1,000 prefix share < 52.0), and the same floors again at MARK-2700. Those are Magnus's confirmed constants and their firings are OPERATIONAL CANCELLATIONS that free a core — typed `cancellation`, never `verdict`, licensing NO exclusion claim (with the single CATASTROPHE carve-out written into CUT-SHORT above). ⛔⛔ THE FLOORS BIND ONLY ON LOCAL COREFILL: `tools/auto_gate.py:113` is REPORT-ONLY on a remote worker and has no per-shard cancel primitive there, which is exactly why KLADLADDER ran to n≈3,404 at 41.86% with no automatic stop (`results.tsv:kladladder-manual-catastrophe-stop`). ⇒ THIS SHARD IS REGISTERED AS **LOCAL**. Routing it to ws1/ws2 is a REGISTERED DEVIATION requiring an amendment BEFORE the row is written, not a routing convenience. The RESOLVABLE gate this document owns is the primary at full n, whose margin (1.33pp) exceeds its own half-width (±1.32pp) by 0.01pp — resolvable, and only just. Everything else on this page (D1, S1, D2, D3, the seat and map splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c LOKI_SEALSENT bots/_v468kladturbo/*.py` → **0** in `doctrine.py`, `eco.py`, `main.py`, `raid.py`; `grep -c _sealsent_` → **0** in all four. `git diff --name-only aba27582^ aba27582` names exactly the four files of the new tree. The control has no seat-sentinel siting filter, no N-cap census, no hold, no want-beat and no store slot 13 write; it seals every free heal seat with a 3 Ti barrier unconditionally (`raid.py:302-312`, the `2b` block on the treatment side). **The behaviour this leg predicts to change therefore cannot already be in the target state.** ⚠ And the *comparative* claim this pair exists for — "the deferral is what costs, not the plant" — is likewise NOT pre-satisfied: it is the hypothesis, its only prior support is one registered arm about a DIFFERENT plank plus one unregistered 48-game demo, and Band 4 below is a live, pre-named outcome that would refute it.
**MAP SEGMENT: none expected** — the primary is the POOLED share over all 15 maps and both seats. The mechanism is a substitution on the enemy core's own heal-seat ring, and **every map has that ring by construction** (a 2×2 core has a twelve-tile collar whatever the terrain); the plank is gated on harvester count and on establishment distance, not on any terrain property. What terrain changes is the raider's ARRIVAL LATENCY, not whether the plank arms. **No map cut may rescue this arm.** Per-map shares WILL be printed at readout as exploratory description — they carry no pre-registered direction and nothing may be banked off them without a fresh prereg. ⚠ **One candidate segment is named here and DELIBERATELY NOT REGISTERED**: the five 900-area maps (midgard, ragnarok, valkyrie, drakkarfjord, glacierkeep), where the longest approach means the plant lands latest. Registering it would hand this arm a second chance to pass, which is OB15b's exact prohibition; if the pooled read fails and that cut looks alive, it needs its OWN leg with its OWN n.
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on the treatment's
pooled game share falls BELOW 51.33.** That excludes the bar and says a
firing-line-sited seat sentinel does NOT add measurably to Sleipnir **even with
the eco-deferral removed**.
**Consequence, registered in advance and split by how far it falls:**
* **CI upper < 51.33 but CI contains 50.0** → the plant is FREE, not harmful.
  See Band 3.
* **CI upper < 50.0** → **the plant itself costs, and the SEALSENT family is
  DEAD as a ship candidate.** The `SEALSENTA` contrast then becomes a question
  about the size of a penalty rather than about a benefit, and the pair converges
  with `KLADLADDER`'s finding that a **committed** forward-sentinel plank
  subtracts from Sleipnir — with the caveat from READ-BEFORE-RATIFYING #4 that
  this arm still carries `LOKI_SEALSENT_TI_FLOOR = 0`, so "the plant alone" is
  NOT what would have been refuted.

**MECHANISM FALSIFIER (independent of the primary, and it can fire first):** if
**S1** shows the treatment's sentinel builds are not shifted toward the enemy
core relative to the control's — i.e. no seat-band plants are distinguishable —
then the plank did not deliver its dose in this fixture and **the primary is
uninterpretable in either direction**: a flat share would mean "the mechanism
never fired", not "the mechanism fired and did not pay". Per FIRINGS-BEFORE-PRIMARY
this is read BEFORE the primary is typed, and if it fires the primary is reported
as **NOT MEASURED** rather than as a null. **This is not hypothetical: s47's delta
D2 records a wiring null escaping demos to a 436-game shard.**

---

## READING, PRE-COMMITTED — four bands, written before the data

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first
row whose condition holds is the reading. The rows are disjoint by construction.**

| # | band at n = 5,400 | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE PLANT ADDS.** Real and resolved on this fixture. Promotes to a combination input and to a separately-registered head-to-head against the live holder. ⚠ Report the size with its OB16 status: the standard band has MDE 0, so this branch may claim "we can exclude 50" and may NOT claim any minimum effect size. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** (includes the whole [51.33, 52.4] window an A/A cell has already produced) | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Registered in advance as WEAK: `NULL125`'s byte-identical A/A read 51.04, so a bare clearance here is not distinguishable from fixture noise by this leg alone. Rows are KEPT and the arm is available for combination; it does NOT license a ship conversation, and a replication on fresh seeds is the price of promoting it. |
| **3** | **point < 51.33 AND CI contains 50.0** | **PARITY — THE PLANT IS FREE, AND THAT IS A BANKABLE FINDING, NOT A NULL.** For the same ring slot, a 20 HP inert barrier becomes a 40 HP turret that fires on a line containing an enemy core tile, at 42-81 Ti instead of 3, and the game share does not move. That is a genuine structural upgrade bought at no measurable cost — a combination input, and specifically the input the `SEALSENTA` contrast needs in order to price the deferral against something. It does NOT license a ship. |
| **4** | **CI upper < 50.0** | **THE PLANT SUBTRACTS.** The whole SEALSENT family dies as a ship candidate — with the deferral already OFF there is no cheaper funding form left to try. Attribution per READ-BEFORE-RATIFYING #4: this refutes *plant + waived floor*, not *plant alone*. Converges with `KLADLADDER`. |

⚠ **Rows 3 and 4 both fire the PRIMARY FALSIFIER** (both have CI upper < 51.33
whenever the point estimate is meaningfully under the bar); the falsifier's
consequence sentence is the one above, and the band decides which half of it
applies.
⚠ **Nothing here treats 50.0 as a floor.** A share below 50 is a live outcome
with a named mechanism (a 42-81 Ti turret displacing 3 Ti of seal, plus up to 12
raider-rounds of an OPEN enemy heal seat) and it is pre-named so a negative is
not explained away as noise.

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

**Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape happens
to carry.**

### ⛔ ORDERING, REGISTERED AS A HARD SEQUENCE
**D1 and S1 run and are written down BEFORE any sentence containing the primary
share is typed.** See READ-BEFORE-RATIFYING #5 for why this clause is in bold.

### D1 — THE DOSE BATTERY. MEASURABLE, but NOT off the shard tape.
`tools/overnight.sh:138-139` passes `--replay /dev/null`, so the SEALSENTAN shard
produces **no** entity events. D1 runs on a **separate serial battery**:
```
tools/dose.py bots/_v481sealsentAnofund --kind sentinel --ctrl bots/_v468kladturbo --games 48
```
**REGISTERED SIZE: 48 games (8 maps × 2 seats × 3 seeds — `tools/dose.py:126-131`
rotates its 8-map default two games at a time and plays both seats, so 48 is
exactly balanced), SERIAL** (never parallel: D65, `tools/dose.py:26-30`).
**Pre-registered expectation: treatment forward-sentinel builds/game ≥ control's,
with the paired difference outside the tool's own 2×SE band.**
⭐ **REGISTERED-SIZE SHORTFALL RULE, pre-committed, because KLADLADDER's battery
ran 24 of its registered 120 and its diff cleared the band by only 16%:** if the
battery runs short, the readout states the shortfall factor, and **a
`DOSE DELIVERED` verdict whose |paired diff| clears its own band by less than 2×
on a short battery is UNRESOLVED** — which, per GATE RESOLUTION, defaults to the
restriction and means the primary is typed with the mechanism unverified.

⛔⛔ **AND D1 ALONE CANNOT ANSWER THIS PLANK'S DOSE QUESTION. THIS IS AN OB13
FINDING, MADE AT DRAFT, AND IT IS THE MOST IMPORTANT LINE ON THIS PAGE.**
`tools/dose.py`'s headline is `fwdbuild_sentinel/game`. The treatment's seat
sentinel **shares** `LOKI_FWD_GUN_CAP = 3` with the base's own forward sentinel —
the tree says so in terms at `raid.py:874-878`: *"a seat Sentinel IS a forward
Sentinel… this plank relocates a turret rather than adding one."* ⇒ **a treatment
that fires perfectly can read FLAT on D1**, because it moved a turret from a
corner to a seat rather than adding one. **A flat D1 is therefore NOT evidence of
non-delivery for this arm, and must never be reported as one.** S1 is what
separates relocation from non-delivery, and S1 is the metric the MECHANISM
FALSIFIER is written against.

### S1 — THE SEAT-BAND READ. MEASURABLE, but it needs a battery that KEEPS replays.
The discriminator is the **`d2_enemy` distribution of sentinel `BUILD` events**,
treatment vs control. `tools/corpus/replay_events.py` emits one row per build with
columns `file ev rnd team kind x y d2_own d2_enemy mw mh` (`:157`), so the read is:
```
.venv/bin/python tools/corpus/replay_events.py OUT.tsv <replays…>
# then: rows with ev == BUILD and kind == sentinel, grouped by team, histogram d2_enemy
```
**Pre-registered expectation: the treatment's sentinel-build `d2_enemy`
distribution is shifted DOWN (closer to the enemy core) relative to the control's,
and contains a low mode the control's distribution does not reach on the same map.**
⚠ **THE EXACT NUMERIC THRESHOLD IS DELIBERATELY NOT ASSERTED AT LOCK, AND HERE IS
WHY:** `replay_events.py:95-96,113` measures `d2` to a **single core anchor
position** (`corepos[team]` off the map buffer), while the bot's own `dsq_core`
measures to the nearest tile of the 2×2 footprint. **The two conventions differ by
which footprint tile is the anchor, so "a seat reads d2_enemy == 1" is an untested
inference and I will not register it as a fact.** ⇒ **the threshold is CALIBRATED
FROM THE CONTROL ARM'S OWN DISTRIBUTION at readout** — the control never plants on
a seat (its `_try_forward_sentinel` habitually takes a CORNER; the tree's own
census note at `raid.py:697-706` records seat = dsq 1, corner = dsq 2 in the BOT's
convention), so any treatment mass below the control's own minimum on the same map
is the seat plant. **The DIRECTION is registered; only the cut point is deferred,
and it is deferred to a control-derived quantity that cannot be tuned toward a
verdict.**

⛔ **OB17 — THIS READ IS NOT EXECUTABLE OFF A `tools/dose.py` RUN, AND THE BUILDER
MUST FIX THAT BEFORE THE BATTERY FIRES.** `tools/dose.py:157` calls
`rp.unlink(missing_ok=True)` on every replay immediately after decoding, and its
argparse (`:110-116`) defines only `bot`, `--ctrl`, `--kind`, `--games`, `--maps`
— **there is no `--keep`.** ⇒ S1 requires either (a) a `--keep` flag added to
`tools/dose.py` before the battery runs, or (b) its own small serial loop that
passes `--replay <unique path>` and retains the files. **CONSEQUENCE OF SILENT
NON-EXECUTION, registered per OB17 clause 3: if S1 is skipped, the dose evidence
for this arm is D1's headline ALONE, which by the paragraph above cannot separate
relocation from non-delivery — so the primary must then be typed with
"MECHANISM NOT VERIFIED" attached, and Bands 3 and 4 may not be attributed to the
plant.** This is the clause that could still surprise the person running it; run
it first.

### D2, D3 — the kill-round read. MEASURABLE, shard-native.
`cond` and `turns` are on the tape.
* **D2 — TIMELY-KILL RATE (the `DEFENCE_ADMISSION_BAR` primary).** Share of ALL
  treatment-seat games ending `cond == core_destroyed` with `turns ≤ 300`,
  treatment vs control, both computed on the same 5,400 rows. **Non-regression is
  the bar and it is stated as an EXCLUSION, per CLAUDE.md's fail-to-exclude
  clause: the 95% CI on the difference must EXCLUDE a fall of more than 2.0pp.**
  A "no significant rise" phrasing is not admissible.
* **D3 — MEDIAN KILL ROUND**, treatment vs control, as the gross backstop
  (median crossing 300 is disqualifying), reported alongside the r1000 rate since
  `R1000_IS_DEFEAT` makes an r1000 share a cost even when the tiebreak is won.
  Anchor: KLADTURBO's own local full read had median kill 193
  (`results.tsv:kladturbo-local-confirm-5400`, 61.09% [59.79,62.39] n=5,400).

### NOT MEASURABLE on this leg — named, not silently dropped.
* **Whether the HOLD ever costs an open seat.** `LOKI_SEALSENT_HOLD_MAX = 12`
  bounds it per raider, but seat-occupancy-over-time is not decoded by any shipped
  tool and building one is out of scope. **The plank's most plausible cost channel
  is therefore UNOBSERVED on this leg.** Said plainly rather than left implicit.
* **Whether the planted sentinel ever FIRES.** The tree's own drumlin s3 demo
  found a seat sentinel that survived 279 rounds and never fired once, because the
  team magazine sat at 2-14 ammo. `replay_events.py` decodes builds and deaths,
  not shots. **A Band-3 "free" result and a "we bought an expensive barrier"
  result are NOT separable by this leg.**
* **Which of the two remaining sub-mechanisms carries a Band-4 result** — the
  turret's price vs the waived `LOKI_SEALSENT_TI_FLOOR = 0` — is **NOT SEPARABLE**
  here; they ship together in this arm. No readout sentence may attribute a
  negative to one half.
* **Per-unit CPU** — local replays zero-fill `execTimeUs`, so no timing claim is
  available on this surface.
* **Seed determinism** — `NOISE_ON` pins an unseeded RNG, so base-vs-base at one
  seed diverges at round 0. **No seed-matched or replay-diff equivalence claim is
  available on this fixture, and the flag-off base-equivalence claim is made on
  the CODE, never on a replay comparison.** The engine is not run-to-run
  deterministic and nothing on this page assumes it is.

---

## THE CHANGE — `file:line`, control → treatment

**TREATMENT TREE: `bots/_v481sealsentAnofund`** — `bots/_v468kladturbo` plus one
plank across four files. Verified at draft: `diff -rq` names exactly
`doctrine.py`, `eco.py`, `main.py`, `raid.py` (`__pycache__` entries are build
artefacts, not source).

**(1) `doctrine.py` +1387-1441** — the doctrine block and the constants:
`LOKI_SEALSENT_ON = True`, **`LOKI_SEALSENT_FUND_ON = False`** (`:1424` — the one
constant that separates this tree from `bots/_v474sealsentA`),
`LOKI_SEALSENT_MODE = "seat"`, `LOKI_SEALSENT_MAX = 1`,
`LOKI_SEALSENT_CENSUS_MIN/MAX = 0/1`, `LOKI_SEALSENT_MIN_HARV = 2`,
`LOKI_SEALSENT_TI_FLOOR = 0`, `LOKI_SEALSENT_HOLD_MAX = 12`,
`LOKI_SEALSENT_FUND_MAX = 60`, `LOKI_SEALSENT_AMMO_ON/FLOOR = True/20`,
`LOKI_SEALSENT_FUND_STALE = 3`, `LOKI_SEALSENT_FUND_MARGIN = 6`,
`SLOT_SEALSENT = 13`.

**(2) `raid.py:293-309`** — step **2a**, asked BEFORE the barrier step because the
barrier is irreversible for this purpose; `hold` is the one seat key the barrier
loop skips (`:307`).

**(3) `raid.py:672-988`** — the `_sealsent_live` / `_sealsent_site` /
`_sealsent_try` family. The plant lands at **`:950`**. Site legality is probed
with `can_build_barrier` rather than `can_build_sentinel` (`:768`) because every
`can_build_*` folds AFFORDABILITY into the same boolean and would refuse a good
tile whenever the bank is short.

**(4) `raid.py:104-114`** — two cached frozensets (`raid_cornerkeys`,
`raid_corekeys`) on the existing anchor key.

**(5) `main.py:136-142`** — two per-unit counters (`sealsent_hold_n`,
`sealsent_want_n`).

**(6) `eco.py:371-403` + `:412-413`** — `_sealsent_reserve` and its single call
site in `_eco_spendable`. ⭐ **IN THIS ARM THIS ENTIRE HUNK IS INERT AND THAT IS
THE POINT:** `eco.py:393` returns 0 whenever `LOKI_SEALSENT_FUND_ON` is False, so
`:413`'s `if res and …` can never be true and every eco spend behaves exactly as
`bots/_v468kladturbo` spends. **The code is present so that the `SEALSENTA`
contrast is a ONE-CONSTANT difference and not a different tree.** Correspondingly,
`raid.py:926`'s want-beat publication is guarded on the same constant and never
runs here, so store slot 13 is never written by this arm.

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one LOCAL core to n = 5,400, plus 48 serial games for D1 and the S1
battery.** ZERO rated ladder exposure, zero submissions, zero unrated challenges
— nothing on this page touches the platform, which is why `TARGET BAND` is N/A
rather than a number.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input and (b) a separately-registered head-to-head against the live
holder, which is the pipeline step Magnus's procedure names verbatim (*"we start
by testing it against the current slot, If it beats it we can switch"*) and which
`SLEIPH2H` is the template for. **A local screen against the incumbent is gate 1;
gate-1-to-gate-2 transitivity is UNVALIDATED in this repo (QUEUE #65: 3
concordant, 1 not), so the head-to-head is not skippable on the strength of this
number.**

**It is HALF of a pair.** `docs/prereg/PREREG-SEALSENTA-2026-08-17.md` screens
`bots/_v474sealsentA` — byte-identical apart from `LOKI_SEALSENT_FUND_ON` — and
registers the DIFFERENCE of the two shares as its primary. **Neither leg's own
bar is the interesting quantity; the contrast is.** For that contrast to be
computable as registered, **both shards must run LOCAL, on the same host, at the
same planned n** — see the cross-host rider in the obligations doc (Addendum 11
rider, 2026-08-15): the 0.98 exemption is a WITHIN-HOST measurement and does not
cover cross-host pooling.

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: OB7, OB12, OB13, OB14, OB15a/b/c, OB16 + its corollary and cross-host rider, OB17 + its rider) · `docs/prereg/PREREG-KLADLADDER-2026-08-17.md` (today's house style, read in full) · `docs/prereg/BARS.tsv` (registry header, the FIRINGS-BEFORE-PRIMARY rule, the `le`-direction warning, and the sibling klad/sealsent-family rows) · `CLAUDE.md` · `tools/prereg_check.py` (read for `RULES`, `check_presence`, `check_arithmetic`, `check_metric_window`, `check_pool_era`) · `tools/auto_gate.py` (`MARK_CATASTROPHE=400`, `MARK_MID=1000`, `MARK_HALF=2700`, `CATASTROPHE_CI_HI=45.0`, `TREND_FLOOR=52.0`, and the `:113` remote report-only limitation) · `tools/overnight.sh` (`:66` the 15-map pool, `:99-101` the `# FIXTURE … start=` stamp, `:105` the legacy-resume form, `:138-139` `--replay /dev/null`) · `tools/dose.py` (`:110-116` argparse, `:126-131` map/seat rotation, `:157` the replay unlink, `:80-105` the decoder) · `tools/fwd_read.py` (docstring + `:191-208` decode output columns) · `tools/corpus/replay_events.py` (`:56`, `:95-96`, `:113-117`, `:157`) · `bots/_v481sealsentAnofund/doctrine.py` · `bots/_v481sealsentAnofund/raid.py` · `bots/_v481sealsentAnofund/eco.py` · `bots/_v481sealsentAnofund/main.py` · `bots/_v474sealsentA/doctrine.py` · `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `results.tsv` (rows `null125-final`, `idnull140-cert-5400`, `kladturbo-local-confirm-5400`, `kladladder-manual-catastrophe-stop`, `kladladder-verdict-amendment-f1f2-pending`, `kladladder-final-attribution`, `kladladder-n-reconciliation`, `kladladder-n-final-correction`) · git commits `493df130` and `aba27582` and `git diff --name-only aba27582^ aba27582` · the drafting brief supplied by the builder lane s48 and its mid-task correction consumed from the side lane. No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.

---

## AMENDMENT 1 (builder s48, 2026-08-17T05:48:46Z, BEFORE the leg's first game — surface change LOCAL → worker@work-server-1)

The registered LOCAL-ONLY routing cited auto_gate.py:113 (remote = report-only,
floors cannot bind) as its reason. **That reason died one hour after lock:**
commit a50f27ef gives auto_gate --apply a guarded remote stop path
(tools/remote_cancel.py), so the strict floors NOW BIND on ws1. Meanwhile the
local box is load-held (agent work; the load ceiling correctly protects row
validity — wall-clock TLE corruption is load-sourced regardless of cause), so
LOCAL routing would idle both arms indefinitely against Magnus's iterate
directive. CHANGES: host = worker@work-server-1 (seed offset +32,000,000 per
the sidecar; registered seedbases unchanged); second clock = first-completed-row
/ serial-ordering backstop (remote tapes carry no FIXTURE stamp — the registered
backstop, now primary); host certification = NULLWS1S (this host, TODAY,
54.25 [49.37,59.13] n=400, collision/sanity scope as pre-committed). Everything
else — bars, bands, contrast, stops semantics, FIRINGS-BEFORE-PRIMARY —
unchanged. Local worklist rows retired with pointers here.

### AMENDMENT 1a (2026-08-17T05:49:35Z, still before the arm's first game): seedbase correction
Amendment 1 said "registered seedbases unchanged" — WRONG at execution: the
registered 812000 collides with NULLWS1S's seedbase on this host (both would
map to +32M offset 32812000, replaying the null's seeds as treatment games —
the pooled-n-is-a-lie class). Actual seedbases: SEALSENTAN 816000 (host
32816000), SEALSENTA 818000 (host 32818000). Disclosed before first game;
seeds are identity-neutral to the hypotheses.
