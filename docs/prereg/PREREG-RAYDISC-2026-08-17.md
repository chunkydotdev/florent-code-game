# SCREEN PREREG — `RAYDISC`: forward-sentinel RAY DISCIPLINE, scored as a CLAUSE-ISOLATION HEAD-TO-HEAD against its own carrier

Drafted by a fresh opus subagent with NO inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `docs/prereg/BARS.tsv` row, fired no game, started no
shard, and touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md`
nor `QUEUE.md`.

**STATUS: drafted BEFORE the `RAYDISC` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any `docs/prereg/BARS.tsv` row exists,
BEFORE any file named `scratchpad/overnight/RAYDISC*` exists, and BEFORE the
leg's first game.** Drafting session wall clock at write time
**`2026-08-17T14:17:23Z`** (`date -u`, same shell call); repo HEAD at draft
`f1d6e6d4` (author time `2026-08-17 16:07:16 +0200`). Verified at draft:
`grep -c RAYDISC scratchpad/corefill_work.txt` → **0**;
`grep -c RAYDISC docs/prereg/BARS.tsv` → **0**;
`ls scratchpad/overnight/ | grep -i raydisc` → **0 files**.

### LOCK, clock 2 (local shard)
Per the obligations doc's **2026-08-17T07:24:55Z addendum**, which replaced the
clock-2 boilerplate eleven preregs had copied and that was not executable as
written. **PRIMARY:** the shard tape's own `# FIXTURE … start=` stamp
(`tools/overnight.sh:99` sets `START=$(date -u …)`, `:103` writes it to the tape
before the first game). Quote it verbatim beside the lock commit's git author
time. **BACKSTOP, if the tape carries no `# FIXTURE` line** (every REMOTE tape;
107 of 238 local tapes carry it): the tape's **FIRST COMPLETED ROW `ts`** —
conservative by construction, since the true start is strictly earlier, so the
substitution can only OVERSTATE the prereg-to-start gap (measured cost 1–2 s).
⛔ **NOT AVAILABLE: the heartbeat's `STARTING` line** — `overnight.sh:100` writes
it with `>` and every later state overwrites it. **State which clock was used.**
This shard is registered LOCAL and SAME-HOST, so the primary is expected to be
available.

### ⚠ COMMIT PROVENANCE — THE TREATMENT IS UNTRACKED, THE CONTROL IS NOT
`bots/_v507raydiscipline/` **exists on disk and git does not track it**
(`git status --porcelain` → `?? bots/_v507raydiscipline/`; `git ls-files
bots/_v507raydiscipline` → empty). `tools/prereg_check.py` FAILs that by name
(`OB13_UNTRACKED_ARM`): with no git object, `git diff` returns nothing and **the
one-mechanism claim below is unverifiable *by git* for the treatment arm.** The
claim is nevertheless verified by the instrument that does not need git — a
direct file diff against the carrier, reproduced verbatim in `THE CHANGE` and
re-runnable in four commands. **The builder's lock commit is what converts that
into a git-checkable fact.**
⭐ **THE CONTROL, by contrast, IS git-pinned and clean:** `git ls-files
bots/_v488beltbreak2` lists all four modules, `git status --porcelain
bots/_v488beltbreak2` is **empty**, newest commit touching it is **`997bcd42`
(2026-08-17 11:12:38 +0200)**, and its module digests at draft are
`doctrine.py b572a721531b77a8c27102bf64313996` /
`main.py d7f31eedc6795956b72b541eb383c896`. ⚠ **Caveat a certifier should not
have to find: "the control is the same bytes that produced the completed
`beltbreak2-final` 53.09% tape" is inferred from working-tree CLEANLINESS, not
from a stamp on the tape.** The tape has no tree digest column. The inference is
sound and it is an inference.

---

## ⛔ READ BEFORE RATIFYING — NINE THINGS THE LANE OWNS

**1. ⛔⛔ THE SINGLE BIGGEST THING ON THIS PAGE: HALF THE MEASURED SHARE GAIN IS
r1000 TIEBREAK WINS, AND `R1000_IS_DEFEAT` SAYS THOSE ARE DEFEATS.** The build
relay's own kill-currency decomposition (`docs/coordination.md:70823`) is
**+4 kill-wins / −10 kill-losses / +5 r1000 non-events (all wins)**. The
measured share move is **+4.00pp over 250 cells = +10 games**, and **five of
those ten are r1000 tiebreak wins.** ⇒ **the DOCTRINE-CLEAN half of the effect
is ~+2.0pp, not +4.00pp.**
**WHY THAT DOES NOT DISQUALIFY THE ARM, stated precisely rather than waved
past.** `PROGRAMME.md:310-336` resolves this collision explicitly: **`game_share`
decides the SHIP (it is what the ladder pays — `delta = 32 × (S − E)`,
`S = games won / 5`), while `R1000_IS_DEFEAT` governs what we BUILD — "no plank
may be *designed* to farm tiebreaks".** This plank is a shot-discipline reorder
on a forward turret; it is not designed to farm tiebreaks. **So the r1000 wins
are admissible IN THE SHARE and the bar stays denominated in game share.**
**WHAT IS REGISTERED BECAUSE OF IT, pre-committed so it cannot be chosen after
the number exists:** the share gain is **DECOMPOSED** at readout into
core-kill-win gain vs r1000-tiebreak-win gain (`cond` and `turns` are both on the
tape, so this is shard-native and costs nothing), and:
> **⛔ IF THE SHARD'S SHARE GAIN OVER 50.00 IS MAJORITY r1000 TIEBREAK WINS, THE
> READING IS DOWNGRADED ONE BAND AND LABELLED `OFF-DOCTRINE COMPOSITION`.** It
> promotes to a combination input only: **no ship conversation, no head-to-head
> against the holder, no "the diversion kills better" sentence.** A gain composed
> of tiebreaks means the mechanism delivered SURVIVAL, not KILLING, and the
> `-10` in `tools/score.py` exists to make exactly that worth zero.
**And the arithmetic consequence for power, which is the honest reason this
clause is first: at a doctrine-clean true share of ~52.0 the arm's own
registered floor kills it at the 1000 look HALF THE TIME** (table in `#3`).

**2. THE CONTROL IS THE CARRIER, AND THAT IS THE WHOLE POINT — BUT IT MAKES THIS
A ZERO-SUM SELF-LEG AND CHANGES WHAT EVERY NUMBER MEANS.** Treatment
`bots/_v507raydiscipline` = `bots/_v488beltbreak2` + ONE mechanism; control IS
`bots/_v488beltbreak2`. Consequences, all of them load-bearing:
* **The structural null is EXACTLY 50.00, not "about 50".** On any game where the
  mechanism never engages, the treatment's code path is the carrier's code path,
  so the game is **carrier-vs-carrier** — and the shard is seat-balanced and
  map-balanced, so its expectation is 50.00 by symmetry. This is a stronger null
  than any screen against a third bot can have.
* **"Our win" and "their loss" are the SAME EVENT.** There is no independent
  control outcome to compare against: every metric computed "per side" is
  mechanically anti-correlated with its counterpart. **This is why the kill-round
  reads below are registered WITHIN-ARM and why the r300 bar is registered as a
  one-sided SAFETY BACKSTOP rather than as evidence about kill speed** (`#6`).
* ⭐ **IT IS THE DESIGN THE BBAMMO CRITIQUE MANDATED, verbatim from the s49
  disposition (`docs/coordination.md:70801`): "variation screens must run vs THE
  CARRIER as control (clause isolation), not vs kladturbo",** because the carrier
  alone already reads **53.09% [51.76, 54.42] vs `_v468kladturbo`**
  (`results.tsv:beltbreak2-final`, full registered n=5400, COMPLETE) — so a
  vs-kladturbo screen of this variation could absorb the clause's entire cost and
  still clear a 51.33 bar. **Here the Δ CAN fail on the clause.**
* ⛔ **AND THE CONVERSE, WHICH IS THE PRICE OF CLAUSE ISOLATION: THIS LEG SAYS
  NOTHING ABOUT THE COMPOSITE'S ABSOLUTE LEVEL.** A Band-1 result licenses *"the
  ray-discipline clause adds vs its own chassis"* and **NOT** `53.09 + 4.00`.
  Local screens are not transitive in this repo (QUEUE #65: 3 concordant, 1 not),
  the two fixtures have different opponents, and no composition rule is
  registered. **The absolute level needs a separately-registered
  `_v507raydiscipline` vs `_v468kladturbo` shard — which is also the only thing
  that can address `X3R0_SLOT_RULE`'s 60±2 threshold.** Named as step 2 of the
  promotion pipeline in `WHAT THIS LEG COSTS`.

**3. ⛔⛔ THE COMBO BAR IS THE GATE MOST LIKELY TO DECIDE THIS ARM'S FATE, AND
THE EXEMPTION APPLIES BY CLASS — WITH A CITATION, NOT BY EXTENSION OF MAGNUS'S
SOLO RULING.** `tools/auto_gate.py:715 combo_of()` greps the `stack.py` compose
marker off the **TREATMENT** tree's `doctrine.py`. Verified at draft:
`bots/_v507raydiscipline/doctrine.py:2078` carries `# ---- composed by
tools/stack.py from: turbo (_x3r0v152), bodyaware (_v242bodyaware), samestop
(_v464samestop)` — **byte-identical to the carrier's line at the same line
number**, i.e. inherited, which every arm on this chassis is. ⇒ **the gate scores
`RAYDISC` as a COMBO and `COMBO_BAR = 55.0` binds on the n=2700 prefix**
(`auto_gate.py:278`, Magnus 2026-08-16).
**THE EXEMPTION AND WHY IT IS TYPEABLE HERE.** `auto_gate.py:906-919` states the
token's registered purpose verbatim: *"a MECHANISM test scored against its own
additive prediction can sit ON its registered target and still be under 55."*
**This arm IS that class, and the page makes the claim substantive rather than
asserted: it registers the additive prediction (`REGISTERED ADDITIVE PREDICTION`
below, 50.00 + 0.276 × 14.5 = 54.00pp) and scores the shard against it.**
⛔ **THIS IS NOT AN EXTENSION OF THE `BELTBREAK-EARLY`/`BELTBREAK2` GRANTS.** Those
two rows (`docs/prereg/BARS.tsv:310,312`) say verbatim *"this arm is a SOLO plank
… not a combination"* and were **escalated to Magnus** because a PROSPECT cannot
claim the mechanism-test class. **The distinction is the CONTROL, not the arm:
those arms were scored against `_v468kladturbo` — a prospecting screen. This arm
is scored against its own chassis with a pre-registered additive prediction,
which is the token's registered purpose on its face.** ⇒ **the builder types the
token citing `tools/auto_gate.py:906-919` AND this page's additive prediction, not
Magnus's solo ruling.** If the builder judges otherwise, **escalate rather than
fire unexempted** — the price is in the table.
**⛔ AND THE TOKEN ALONE GRANTS NOTHING** (`auto_gate.py:920-934`): the source
column must cite an `.md` file **that exists**, or the gate fires
`COMBO-BAR-BROKEN-EXEMPT` and applies the 55.0 bar anyway. Cite
`docs/prereg/PREREG-RAYDISC-2026-08-17.md`.
**THE FLOORS PRICED, BEFORE THE FIRE.** Prefix looks are one-shot at each mark
(`auto_gate.py`, `Tape.wins_at_mid` / `wins_at_half`); naive normal, Z95=1.96,
local DEFF 0.98 ⇒ no inflation:

```
true share   P(TREND-FLOOR@1000   P(COMBO@2700 stop,   P(reach n=5400,   P(Band 1 |
             stop, prefix<52.0)   unexempted, <55.0)   EXEMPTED)         completion)
  51.5             0.624                0.9998            0.376            0.045
  52.0             0.500                0.9991            0.500            0.170
  53.0             0.263                0.981             0.737            0.697
  54.0  <- proj.   0.102                0.851             0.898            0.977
  55.0             0.028                0.500            
```
⇒ **at the projected 54.00 the exemption is worth ~6.7× on completion (0.898 vs
0.134) and the arm's overall P(Band 1) is ~0.88.** ⇒ **AND THE 52.0 TREND FLOOR
IS A REAL LOOK HERE, NOT A FORMALITY: it is NOT waived by the combo exemption
(`BARS.tsv:310` states that explicitly for the sibling rows), and at a
doctrine-clean 52.0 it stops the arm on a coin flip.** That is the honest
downside and it is why `#1` is first.
**Registered reading of a floor stop, pre-committed:** a `TREND-FLOOR@1000` or
`COMBO-BAR@2700` firing is an **OPERATIONAL CANCELLATION**, typed `cancellation`,
never `verdict`; it licenses **no** sentence of the form "ray discipline does not
pay". ⭐ And per the side lane's s47 note (n=2 cases, a DIRECTION with a rough
size, not a calibrated correction), **a floor stop fires on a LOW PREFIX DRAW, so
conditional on stopping the arm's true share is HIGHER than the number that
stopped it — expect roughly +2pp of regression.** Disclose the partial as
**selected-pessimistic** or do not quote it.

**4. ⛔⛔ THE SHARD RUNS `NOISE_ON = True` AND THE DOSE BATTERY RAN `NOISE` OFF —
SO THE DOSED/UNDOSED SPLIT IS NOT COMPUTABLE ON THE SHARD, AND THE PAIRING
INSTRUMENT AND THE POPULATION ARE TWO DIFFERENT FIXTURES.** This is the most
consequential mechanical fact on the page and nothing else on it is safe to read
without it.
* **The shard's population is the SHIPPED CONFIG.** `bots/_v507raydiscipline/
  doctrine.py:474` is `NOISE_ON = True` (identical in the carrier), and
  `tools/overnight.sh:31` records that this is **deliberate** (*"NOISE_ON IS
  DELIBERATELY LEFT TRUE (gate.py would FAIL it)"*). `main.py:456` is
  `self.spawn_salt = random.Random().randrange(97) if NOISE_ON else 0` — **an
  unseeded RNG**, so two runs of the same `--seed` are NOT reproducible and
  base-vs-base diverges at round 0.
* ⭐ **The F0 correction is what makes the pairing instrument possible AT ALL, and
  its scope is exact** (`docs/coordination.md:70810`): *"`--seed` IS NOT INERT
  ENGINE-SIDE. With NOISE_ON=False, 3 runs at seed 852900 were byte-identical
  (md5-verified) and 852901 differed — only the bot's unseeded spawn salt is
  inert."* ⇒ **paired deterministic designs require `NOISE_ON = False` battery
  copies.** The relay's `250 cells/arm, NOISE off` figures come from exactly such
  copies.
* ⇒ **CONSEQUENCE, REGISTERED: the shard tape (`ts shard game map seed seat
  winner cond turns`) carries no dose marker and cannot be paired, so
  "undosed cells read ~50.0" is NOT a shard read.** It is registered on **F2**, a
  separate paired-deterministic battery with its own n, and the shard's 5,400
  rows lend it none of their power. **Anyone quoting a dosed/undosed split "from
  the RAYDISC shard" is quoting something that does not exist.**
* ⇒ **AND THIS IS BRANCH 1 OF THE HONEST-NULL TABLE, the arm's main measurable
  risk:** the spawn salt perturbs builder spawn ordering → forward-sentinel
  siting → whether a belt tile lies on the ray. **The 27.6% dosed fraction was
  measured at NOISE OFF and may not hold at NOISE ON.** `F1` is registered to
  measure it **in the shard's own regime** and is read BEFORE the primary.

**5. ⛔ THE 27.6% DOSED FRACTION IS AN OPPONENT-CONTROLLED GEOMETRY FACT AND IT
IS A HARD CEILING, MEASURED IDENTICAL IN BOTH ARMS.** A forward sentinel is built
facing a **CORE tile** (`raid.py:719-738` iterates `core_tiles(E)` and takes the
first facing `can_fire_from` accepts), so its ray is a core-facing line and the
opponent's belt has no reason to lie on it. Measured: **econ-on-ray occurs in
27.6% of games (69 of 250 cells), IDENTICAL in both arms — the control
instruments the opportunity it declines.** ⇒ **72.4% of the population is A/A by
construction and the pooled effect can never exceed `0.276 × on-ray effect`.**
⚠ **And the ceiling is opponent-dependent in a direction we cannot control: a
field opponent that lays belts off the core-lines is byte-identical to the
carrier for this plank.** The fixture here is our own chassis — **an echo loop**
— so the 27.6% is a fact about how OUR bot builds belts, not about the field.
**A live confirmation is owed before any road here is closed** (`CLAUDE.md`
rule 6); this page closes nothing.

**6. THE KILL-CLOCK READS ARE WITHIN-ARM, AND THE r300 BAR IS A ONE-SIDED SAFETY
BACKSTOP — NOT EVIDENCE ABOUT SPEED.** In a zero-sum self-leg the treatment's
kill count and the control's are two halves of one partition, so a "treatment
kills faster than control" claim is **partly the share wearing a clock's
clothes**: an arm that wins more games necessarily kills more of them and its
opponent kills fewer. **Registered handling, three parts:**
(a) each side's ITT RMST₃₀₀ and ITT timely-kill-by-r300 rate are computed over
**all** rows and reported side by side; (b) the r300 admission bar is scored as an
**exclusion on the difference** and is a **backstop that can only catch the bad
case** — "wins more, but every added win lands past r300"; (c) **no sentence on
this page or at its readout claims the arm speeds the kill on the strength of a
cross-arm difference.** The gross backstop (the treatment's own median kill round
must not cross 300) is within-arm and is the clean one.
**Anchors from the dose battery, quoted as anchors and NOT as predictions:**
timely-kill ITT **26.4 → 28.4**, median kill **222 → 220**, and — the one that
points the other way — **the dosed-subset kill median is +4 to +7 rounds SLOWER**.
**The mechanism has an arithmetic worst case and it is small:** budget 6 shots ×
reload 2 = **12 rounds of core delay per forward sentinel, hard, never resetting**
(`doctrine.py:2139-2146`), with `LOKI_RAYDISC_CORE_HP_STOP = 90` overriding the
budget for the last five shots of a siege.

**7. THE SURPRISE IS BANKED BEFORE IT IS EXPLAINED, AND ITS MECHANISM IS A
SECOND-ORDER CLAIM THIS LEG CANNOT TEST.** Relay, verbatim: **+325 core damage
per dosed game** — diverting shots AWAY from the core RAISED core damage. The
proposed mechanism is survival: the forward sentinel's **firing span rose
96.9 → 114.5 rounds** (shots/sentinel 38.4 → 44.1) at an **unchanged first-fire
round r137**, i.e. the diversion starves what would have killed the sentinel and
the longer-lived platform delivers more core damage than the diverted shots cost.
⚠ **REGISTERED AS A HYPOTHESIS, NOT AS A FINDING.** The shard tape cannot see
shots, spans, or core HP; the span/damage figures come from retained replays on a
separate battery (F3), and **"the diversion caused the survival" is not separable
on this leg from "the games where a belt lay on the ray were the games where our
sentinel was going to live anyway"** — the dosed subset is selected by geometry,
not randomised. **F3 measures the span; it does not identify the cause.** Naming
the cause needs an arm that buys the survival some other way, which this leg is
not.

**8. TWO GUARDS, TWO DIFFERENT EVIDENTIARY STATES — AND ONE OF THEM MAY NOT BE
CALLED A CONTROL.**
* **HOME SENTINELS: EXCLUDED, GUARD MEASURED LOAD-BEARING.** `_rd_forward`
  (`main.py:1070-1106`) requires `d² ≤ LOKI_RAYDISC_FWD_DSQ`(50) of the ENEMY
  anchor **AND** `d² > HUNT_BAND_DSQ`(41) of OUR OWN anchor — because maps run
  from 8×8 up and on a small board a home defender satisfies the enemy-core band
  as pure geometry. **Relay: 4 of 100 games diverge when the guard is forced
  off.** ⇒ **driven both ways, a real control.**
* ⛔ **GUNNERS: EXCLUDED, GUARD NEVER FIRED — REGISTERED AS UNVERIFIED, NOT AS A
  DRIVEN CONTROL.** `turret_type == EntityType.SENTINEL` at `main.py:987`.
  **Relay: 100 of 100 games identical when forced.** The structural reason is on
  the page rather than left as a mystery: the GUNNER branch at `main.py:957-971`
  **returns** whenever a gunner has any hostile target in its facing line, so a
  gunner reaching the ray scan at all is already the rare case. ⇒ **`CLAUDE.md`'s
  rule applies: a guard that has never produced the other verdict has not been
  seen to check.** It is correct by construction and unverified by measurement,
  and this page says so.
* ⭐ **AND ONE CHECK THAT CAME OUT CLEAN, recorded rather than assumed.** The
  banked hazard *"`can_fire` reads TRUE on FRIENDLY tiles on our own ray (68/134)"*
  is a property of the **ENGINE's predicate**, not of this arm: the candidate
  loop sets `et` only when `ct.get_team(bid) != self.team`
  (`main.py:997-1000`), and the diversion picks exclusively from that
  team-checked set. **Verified by reading the source at draft. The own-goal is
  prevented by an existing team check; the hazard is a note about the engine.**

**9. ⚠ THE VACUOUS GATE IS DEAD CODE AND IS LABELLED, NEVER CLAIMED.**
`LOKI_RAYDISC_MAX_HP = 36` (2 sentinel shots × 18 dmg) **cannot ever refuse**:
harvester/conveyor/splitter max HP are 30/20/20 and healing cannot exceed max HP.
The tree says so itself (`doctrine.py:2110-2118`). **It is kept as the correct
expression of intent and it is DEAD CODE today; it is declared under `GATING
CONSTANTS` because an undeclared constant is the failure OB17 exists for, and it
must not appear in any readout as a control that was driven both ways.** What
actually decides among candidates is the `BB_SITE_VALUE` ladder
(`raid.py:80-83`: HARVESTER 100 > CONVEYOR 40 = SPLITTER 40) then lowest HP then
`(x, y)` — deterministic and facing-independent, because
`get_attackable_tiles()` is row-major in ABSOLUTE coordinates
(`main.py:973-977`).

---

## RATIFY: Hypothesis

**HYPOTHESIS.** *When a FORWARD sentinel's existing full-ray priority scan picks
a CORE tile, diverting the shot to an economy target on the same ray first —
`BB_SITE_VALUE` ladder, then lowest HP, bounded by `LOKI_RAYDISC_BUDGET = 6` per
sentinel life (never resetting) and released by `LOKI_RAYDISC_CORE_HP_STOP = 90`
— converts a measured **27.6% dosed-game fraction** and a measured **+14.5pp
on-dosed share advantage** into a LOCAL pooled game share of **51.33% or higher**
against its own carrier `bots/_v488beltbreak2` at n = 5,400 games across all 15
corefill maps and both seats, WITHOUT pushing our own kill past r300.*
Registered direction **POSITIVE**.

**Provenance of the idea, verbatim** (`docs/coordination.md:70808`, the F0 engine
identity that produced it): *"the eco waste lives INSIDE the shots: a sentinel
core-plink is a 28-shot/280-ammo proposition while a belt tile on the same ray is
2 shots."* The ammo pipeline is **94% pass-through** to shots fired
(`ammo_converted − ammo_end = 4×gunner_shots + 10×sentinel_shots`, exact over
240/240 team-series, max residual 0), so **the only way to spend less without
firing less is to make each shot worth more.** That closure is a rules-level
engine identity and sits inside `CLAUDE.md` rule 6's carve-out.

**The mechanism claim, stated so it can be wrong.** The 94%-shots-at-core figure
was **never a targeting bug**: the sentinel fire path already scans the whole ray
and `TURRET_PRIO[CORE] = 0` (`main.py:51-57`) simply outranks HARVESTER 5 and
CONVEYOR/SPLITTER 6. **This arm reorders that ladder for forward sentinels only.
It adds no new scan, no new engine call class, and no new cost** — ammo is 10/shot
flat and reload is 2 rounds regardless of what the shot hits, and every candidate
already passed the parent's own `can_fire(t)` gate. The claim is therefore narrow
and falsifiable: **a belt tile on a forward sentinel's ray is worth more than the
core plink it displaces, at a bounded dose.**

**⇒ AND A FLAT RESULT IS INFORMATIVE ABOUT THE PLANK, NOT ABOUT THE INSTRUMENT —
CONDITIONAL ON F1.** The dose evidence is pre-measured and the attribution is
exact (181/181 undosed cells byte-identical), so a flat share **with the dose
delivered** says *the diverted core plinks were worth more than the belt kills*,
which prices the shot-discipline axis rather than leaving it open. **A flat share
with the dose ABSENT at NOISE ON says nothing at all.** That discriminator is
registered in `FALSIFIER` and is read first.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play against our own carrier. The opponent version is fixed by construction: the control tree is `bots/_v488beltbreak2` at commit `997bcd42`, git-tracked and working-tree clean at draft. There is no opponent churn to pin against and no calibration relevance to protect (CLAUDE.md's rule: pin treatment legs, never pin calibration panels — this is neither, it is self-play). ⚠ DISCLOSED: the control is NOT the corefill `scratchpad/CONTROL_PIN` tree (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`); it is deliberately the CARRIER, per the clause-isolation ruling, which is why every share on this page is written `X% vs _v488beltbreak2` and never bare.**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe; (iii) a third candidate, **HOST**, is killed by REGISTRATION rather than by measurement: this shard is registered SAME-HOST (LOCAL by default), and the obligations doc's Addendum 11 rider (the 0.98 exemption is a WITHIN-HOST measurement, and cross-host pooling is not covered by it) is why splitting it across hosts requires an amendment typed BEFORE the first row. All surviving clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit), i.e. **NAIVE intervals are correct and marginally conservative. The platform constants (1.529 rated / 1.833 unrated) are NOT applicable here and importing them would widen every interval on this page by 24-35% for correlation that has been measured absent.**
**ESTIMATOR: the unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Because the shard is exactly balanced on 15 maps × 2 seats × 180, the pooled share and the map-stratified equal-weight share coincide by construction; the stratified form is computed at readout as an **arithmetic consistency check only** and is not a second estimator (s28 ring-hold: four estimators inside 0.010 of one bar flipped MEET/MISS among themselves). Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never a bar — seat is worth ~7.6pp on byte-identical arms, which is why n is a multiple of 30. **The r1000/core-kill DECOMPOSITION of the share (READ-BEFORE-RATIFYING #1) is a mandatory companion read on the same rows, not a second estimator: it cannot rescue a failed bar and it CAN downgrade a passing one.** Any estimate quoted at readout arrives from `tools/cluster_ci.py` (HEAD) so the interval and the point are produced by the same call; the pre-data half-widths on this page are closed-form Wald with DEFF 0.98 and their arithmetic is shown inline.
**DOSE: economy diversions 0.512 econ kills per game (128 econ kills at 2.13 shots each, over 250 treatment cells) vs 0.000 for the flag-off control (`LOKI_RAYDISC_ON = False` IS the carrier byte-for-byte, so the flag-off arm has no diversion path at all — grep count 0/0/0/0 across the carrier's four modules), n=500 games (250 paired cells per arm), NOISE off, `--tle 10`, NOWINNER 0/500, deterministic paired cells.** **BOTH VERDICTS PRESENT, and the flag-off half is the strongest attribution this repo has produced: 181/181 undosed cells BYTE-IDENTICAL end-state (+0.000pp), with the whole effect concentrated in the 69 dosed cells at +14.5pp [+6.1, +22.9].** The zero is not a blind zero: the same instrument reports **10 discordant cells ON-only against 0 OFF-only**, i.e. it demonstrably produces the other verdict where the mechanism engages. ⛔ **PROVENANCE OF THESE FIGURES, DISCLOSED BECAUSE IT BOUNDS THEM: they are quoted from the builder's s49 coordination relay (`docs/coordination.md:70813-70824`, ~14:1xZ). The battery's own artefacts are NOT on disk at draft** (`grep -rl 'RD507\|raydisc' scratchpad/ tools/` → no match; no `bots/` battery copy exists), **so this agent cited them and could not re-derive them.** ⚠ **AND ONE FIXTURE AMBIGUITY THE RELAY DOES NOT RESOLVE, escalated rather than papered over: it does not name the dose battery's OPPONENT.** A paired ON/OFF ablation against a fixed third bot and a direct treatment-vs-carrier head-to-head are DIFFERENT ESTIMANDS, and the additive projection below assumes the on-dosed advantage transfers between them. **The builder must state which fixture produced +4.00pp/+14.5pp before locking** — see `RATIFICATION BLOCKERS`.
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:68` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30). ⛔ **5400 IS SAID EXPLICITLY BECAUSE A SOLO SHARD OTHERWISE DEFAULTS TO A 2700 TARGET, and at 2700 the bar arithmetic below is unreachable** (margin 1.33pp against a half-width of ±1.87pp).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture and no accepts count is declared. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: the tape carries an unprefixed header line under the `# FIXTURE` line, so a naive `wc -l` over-reports n by exactly one (measured on KLADLADDER, `results.tsv:kladladder-n-final-correction`; reproduced at draft — `grep -vc '^#' scratchpad/overnight/BELTBREAK2.tsv` → **5401** for a completed 5,400-game shard). The registered denominator is **DictReader row count over non-`#` lines, cross-checked against the heartbeat's `n TARGET` and against `max(game id) + 1`.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed rows this arm publishes descriptive tallies (share, per-seat, per-map, per-class, kill-round, `cond` mix, the r1000/core-kill decomposition) and takes **NO bar verdict**; the one-sample half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on, so a sub-2,700 read cannot resolve its own branches. An `auto_gate` firing at CATASTROPHE@400, MARK-1000, TREND-FLOOR@1000, COMBO-BAR@2700 or the CI rule at MARK-2700 is an **OPERATIONAL CANCELLATION, not a verdict**, typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 4, so a stop under that clause DOES license the Band-4 sentence at the partial n — **provided F1 and F2 have been read first** and provided the partial share is disclosed as **selected-pessimistic** (a floor stop fires on a LOW PREFIX DRAW; expect roughly +2pp of regression, side lane s47, n=2 cases, a DIRECTION with a rough size and not a calibrated correction). ⛔ **NO OTHER CLAUSE'S CANCELLATION LICENSES ANY BAND.**
**BAR: 51.33. MDE: 0.00pp — THIS BAR IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE** (OB16 corollary, 2026-08-15T03:52:45Z: the standard corefill band IS `50 ± half_width` at n = 5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes no positive effect size whatsoever). n for the one exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n. **The r300 admission read below is the OTHER bar on this page and it IS sized — see `KILL-ROUND NON-REGRESSION`.** ⭐ **AND THE OB16-FORM STATEMENT IS AVAILABLE FOR FREE ON THIS PAGE, because Band 1 requires the CI LOWER bound ≥ 51.33: clearing Band 1 excludes `50.00 + 1.33`, i.e. it does carry an implied minimum effect of +1.33pp. That is a property of the BAND, not of the BAR, and the two must not be conflated in a readout sentence.**
**BASE RATE: 50.00**
**BAR SOURCE:** the house-standard corefill futility band, `50 + 1.96*sqrt(0.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTAN`, `SEALSENTA`, `ROUTESCORE`, `BELTBREAK-EARLY` and `BELTBREAK2`, which is what keeps this arm numerically comparable to the turret-family reads it extends — **and specifically comparable to its own carrier, whose Band-1 clearance was read against this same number.** **Constructed, not observed.** ⭐ **AND ITS NULL IS STRONGER HERE THAN ON ANY OF THOSE ROWS: on a treatment-vs-own-carrier fixture the 50.00 comparator is STRUCTURAL (an undosed game is carrier-vs-carrier), not merely calibrated.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree IS the treatment's own base, with the added property that 72.4% of games are byte-identical by construction. Empirically calibrated on the same host and fixture by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z (`results.tsv:idnull140-cert-5400`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it. ⚠ **The two cells are 1.77pp apart**, so a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced — which is why Band 2 is pre-registered as WEAK. **Disclosed before the data.**
**REFERENCE n: none** — the bar's comparator is a STRUCTURAL null of 50.00 generated inside this same shard from its own 5,400 seeds; there is no external reference SAMPLE. ⛔ **AND THE CARRIER'S OWN 53.09% vs `_v468kladturbo` IS EXPLICITLY NOT A REFERENCE SAMPLE ON THIS PAGE.** It is a different fixture with a different opponent; naming it as a reference would make the checker size 51.33 as a two-fixture comparison at ±1.87pp and correctly FAIL it — a true statement about a bar nobody registered. **The composite's absolute level is NOT a registered estimand here** (see READ-BEFORE-RATIFYING #2); any sentence relating the two numbers at readout is DESCRIPTIVE and must carry the non-transitivity caveat.
**TREATMENT TREE: bots/_v507raydiscipline**
**TREATMENT DIFF REFS: none — the arm tree is UNTRACKED at draft (`git status --porcelain` → `?? bots/_v507raydiscipline/`), so `git diff` has nothing to show and `prereg_check.py` reports `OB13_UNTRACKED_ARM`. The executable diff of record is `diff -u bots/_v488beltbreak2/main.py bots/_v507raydiscipline/main.py` plus the same on `doctrine.py`, with `cmp` clean on `eco.py` and `raid.py`, reproduced verbatim in THE CHANGE; the builder's lock commit is what makes it git-checkable.**
**MECHANISM METRIC READS: bots/_v507raydiscipline/main.py:1033 — `ct.fire(rd_best)`, the diversion itself: the ONE site at which a shot goes to an economy tile instead of the core, reached only when `rd_arm and rd_best is not None and best_prio == 0 and rd_core_hp > LOKI_RAYDISC_CORE_HP_STOP` (`:1030-1032`), inside `_turret` (`:937`) and on the SENTINEL path only. TREATMENT DIFF TOUCHES: bots/_v507raydiscipline/main.py bots/_v507raydiscipline/doctrine.py. INTERSECTION: yes — the metric site is a NEW LINE in the changed file itself, which is the strongest form of the intersection and needs no import-binding argument (the constants it reads also bind through `main.py`'s `from doctrine import *`, so both paths hold). ⚠ A path-only intersection would ALSO pass here for a trivial reason — the whole tree is new to git, so every file "appears in the diff" — and that reading is REFUSED on this page: `eco.py` and `raid.py` are BYTE-IDENTICAL to the carrier's (`cmp` clean on both, verified at draft), the carrier contains ZERO occurrences of `RAYDISC`/`rd_econ`/`rd_fwd`/`_rd_forward`/`_rd_log` in all four modules, and the metric site does not exist in the control at all. **The metric therefore CANNOT read identically in the two arms — it reads structurally 0 in the control — which is the LOKI-18 failure this obligation exists for.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_RAYDISC_ON=True, LOKI_RAYDISC_LOG=False, LOKI_RAYDISC_FWD_DSQ=50, LOKI_RAYDISC_MAX_HP=36, LOKI_RAYDISC_BUDGET=6, LOKI_RAYDISC_CORE_HP_STOP=90, HUNT_BAND_DSQ=41. MECHANISM CAN OCCUR IN WINDOW: yes** — **NOT ONE of these is a round gate.** `FWD_DSQ` and `HUNT_BAND_DSQ` are squared distances, `MAX_HP` and `CORE_HP_STOP` are hit points, `BUDGET` is a per-unit-per-life shot count, and the two booleans are switches. Independently verified against the tree: the only round-gate-shaped constant `ROUND_GATE_RE` finds anywhere in `main.py` is **`LAUNCHER_MIN_RND = 160` at `main.py:790`**, which is in a different function (`_turret` spans `:937-1068`) and on the launcher path, and `raid.py` contains **no** `*_MIN_RND`/`*_MAX_RND` reference on the forward-sentinel path. ⇒ **the mechanism's window is r0-r1000, and no gate closes any part of it.** ⭐ **WHAT DOES BOUND IT IN PRACTICE, stated so the window is not read as a promise: the mechanism cannot occur before a FORWARD SENTINEL exists and fires, measured at first-fire r137 and UNCHANGED between arms** — so the observed diversion mass lives in roughly r137-r1000 and the r0-r136 stretch is empty in BOTH arms, which is a property of the chassis and not of this clause.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` will emit up to five `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE ARTEFACTS OF THE CHECKER.** Its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a d² of 50, an HP of 36, a budget of 6, an HP stop of 90 and a hunt band of 41 all render as "rounds r0-r<v-1> cannot contain the mechanism". The constants are declared anyway.
**PLANK CLASS: OFFENSIVE — an economy-denial shot-discipline reorder on a forward TURRET (the sentinel already on the map), not a defensive turret purchase, not a home screen, and not an economic plank in the `titanium_collected` sense.** ⭐ **AND THE r300 ADMISSION READ IS REGISTERED ANYWAY, NOT CLAIMED AS INAPPLICABLE.** `PROGRAMME.md`'s `DEFENCE_ADMISSION_BAR` binds on defensive planks; the reason it is carried here regardless is READ-BEFORE-RATIFYING #6 — **this arm's mechanism IS the deliberate deferral of core damage (up to 12 rounds per forward sentinel, by arithmetic), and a plank whose mechanism is a kill-delay must carry a kill-delay bar whatever its class label.** Registering it is strictly stricter than the programme requires and cannot function as a second chance to pass: **both the share bar and the r300 bar must hold.**
**KILL-ROUND NON-REGRESSION: ITT RMST₃₀₀ is the operational estimator (PROGRAMME.md's 2026-08-16T05:36:10Z arbitration, whose vintage rule makes it binding on preregs locked from that date — this one is) — mean kill time censored at the r300 horizon over ALL games, a non-kill scoring 300, computed per side on the same rows; the bar is scored as an EXCLUSION: the 95% CI UPPER bound on (treatment RMST₃₀₀ − control RMST₃₀₀) must EXCLUDE +5.0 rounds (MDE +5.0 rounds; the paired per-game sd of the RMST contribution on the carrier's own completed tape is quoted at readout and the half-width recomputed from it — the anchor from the sibling family is sd ≈ 89 rounds, giving ±2.37 at n=5,400, so the exclusion resolves). SECOND REGISTERED FORM, both required: the ITT timely-kill-by-r300 rate (share of ALL games ending `cond == core_destroyed` with `turns <= 300`, denominator every game played, per side) — its 95% CI LOWER bound on (treatment − control) must EXCLUDE a fall of 3.0pp (MDE 3.0pp; paired sd anchor 75.28pp ⇒ half-width ±2.01pp at n=5,400). THIRD, and it is a DIAGNOSTIC ONLY because it carries a collider: the kill-win-CONDITIONED share and the conditioned median — reported beside the two bars, never as either of them. The treatment's own median kill round crossing 300 is the gross within-arm backstop. ⚠ ZERO-SUM DISCLOSURE, registered with the bar rather than beside it: on a self-leg the two sides' kill counts partition one set of games, so this difference is CONFOUNDED WITH THE SHARE and a PASS in a winning arm is partly automatic — the bar is carried as a ONE-SIDED BACKSTOP against "wins more, all added wins past r300" and licenses no claim that the arm speeds the kill.**
**PRE-STATE: the predicted-change behaviour is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c 'RAYDISC\|rd_econ\|rd_fwd\|_rd_forward\|_rd_log' bots/_v488beltbreak2/{doctrine,eco,main,raid}.py` → **0 / 0 / 0 / 0**, against **11 / 0 / 26 / 0** in the treatment. **The carrier has no ray-discipline path at all: every forward-sentinel shot in the control goes to the highest-`TURRET_PRIO` tile on the ray, which is the CORE whenever a core tile is on it — the exact behaviour this arm changes, and it is 100% of the control's forward-sentinel core-facing shots by construction.** ⇒ the behaviour this leg predicts to change cannot already be in the target state. ⚠ And the OUTCOME claim is likewise not pre-satisfied: this arm's head-to-head share against its carrier **does not exist** on any tape (`grep -c RAYDISC` → 0 on the worklist, the registry and every shard tape), the dose battery's artefacts are not on disk, and every band below — including two sign-reversed ones — is a live, pre-named outcome.
**MAP SEGMENT: none expected — the conditioning variable is NOT terrain.** The mechanism fires iff an enemy economy building lies on a forward sentinel's fixed core-facing ray, which is a **per-GAME fact about where the opponent laid its belts relative to a core line**, not a per-map property; and because the opponent here IS our own carrier, it is a fact about our own belt-laying policy interacting with one seed's spawn salt. The dosed fraction was measured **identical in both arms (27.6%)**, which is what a geometry-driven rather than terrain-driven trigger looks like. Per OB15a this is the explicit "none expected" declaration with its mechanism reason; **the per-map and CQ/STD/GRAND tables (`tools/overnight_read.py:76-94 map_area_class`) are computed and reported DESCRIPTIVELY, carry no pre-registered direction, and may not rescue a failed bar.** ⚠ **A map effect is not IMPOSSIBLE — map area bounds sentinel-to-core geometry and small maps compress every ray — so if a map cell moves hard it is a finding to write down, not a segment to promote (OB15b/15c: the rows that suggest a segment cannot also confirm it; a re-screen is a NEW leg with its own n).**
**PRIMARY SEGMENT: the DOSED vs UNDOSED split — games in which at least one forward-sentinel diversion occurred, against games in which none did. This is the registered segment and it is STRONGER than any map partition, because its complement is A/A BY CONSTRUCTION rather than by measurement: with the mechanism unengaged the treatment's code path IS the carrier's, so an undosed game is carrier-vs-carrier. Registered predictions: the UNDOSED subset reads 50.0 and its matched cells are BYTE-IDENTICAL end-state (any drift there is harness contamination — an INSTRUMENT ALARM, not an effect), and the whole share difference concentrates in the DOSED subset. ⛔ MEASURED ON F2, NOT ON THE SHARD: the shard runs `NOISE_ON = True` and its tape carries no dose marker, so this split is NOT computable on the 5,400 rows and the shard lends it no power (READ-BEFORE-RATIFYING #4). What the SHARD tests is the pooled consequence of the split — the additive prediction below.**
**EXPECTED DIRECTION: POSITIVE on the DOSED subset (the treatment wins more of the games where a diversion occurs), and EXACTLY ZERO — 50.0, byte-identical — on its UNDOSED complement.**
**SEGMENT VALUE CEILING: 27.6% x 14.5pp = 4.00pp pooled.** The share is the dosed-game fraction (69 of 250 cells, measured IDENTICAL in both arms); the on-segment effect is the measured on-dosed difference. ⇒ **the dilution is a HARD CAP: no on-dosed effect can pool at more than 0.276× itself, so a 1.33pp pooled margin needs 4.82pp on-dosed and the projected 4.00pp pooled needs the full measured 14.5pp to hold.** ⚠ **And the cap is opponent-controlled: a belt policy that keeps economy off core-lines drives the dosed fraction toward zero and this plank toward exactly A/A, with no code change on either side.**
⚠ **DISCLOSED, second checker artefact: because the map-dependence line reads `none expected`, `prereg_check.py` renders `OB15A_DIRECTION` and `SEGMENT_CEILING` as `[n/a]` — the segment carrying this page's registered direction is the DOSE split, which `_seg_value` does not reach.** Both tokens are declared anyway and **the ceiling arithmetic DOES run and passes** (`SEGMENT_CEILING ok 27.6% x 14.5pp = 4.00pp`), so the number is machine-checked even though the presence rule is waved. Recorded here rather than left for a certifier to discover as a gap.

**REGISTERED ADDITIVE PREDICTION: 50.00 + 0.276 × 14.5 = 54.00pp.** Registered as the arm's own point prediction, before the fire, from two quantities measured on an independent seed set (dosed fraction 69/250; on-dosed advantage +14.5pp [+6.1, +22.9]). **This is the number the COMBO-BAR-EXEMPT class is defined against** (`auto_gate.py:906-919`: *"a MECHANISM test scored against its own additive prediction"*) — it is what makes the exemption claim substantive rather than a label. ⚠ **It is a PREDICTION, not a bar. It cannot be failed and cannot be cleared;** the bands below score the share against 51.33 and the prediction is reported beside them as a calibration read (reproduced / undershot / overshot), with its two known transfer risks named: the NOISE-ON regime change (branch 1) and the dose battery's unnamed opponent (`RATIFICATION BLOCKERS`).
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.)
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: three gates, sized separately.**
* **(a) THE SHARE BAR.** Margin 1.33pp against a one-sample half-width of ±1.32pp at n=5,400, DEFF 0.98 — resolvable, and only just. ⚠ **The slack is 0.01pp, which is `GUNAXABL`'s exact failure mode: that arm missed its keep edge by 0.0152pp — ONE GAME — on a bar with zero constructed slack.** Registered consequence: **a result within one game of the bar is reported as "the fixture cannot resolve the question", not as a verdict in whichever direction the rounding falls.**
* **(b) THE r300 ADMISSION BAR.** RMST₃₀₀: MDE +5.0 rounds against half-width ±2.37 → resolves. Timely-kill: MDE 3.0pp against ±2.01pp → resolves. Both branches separated by construction, and both scored as exclusions.
* **(c) THE OPERATIONAL FLOORS.** The pinned `tools/auto_gate.py` marks CATASTROPHE@400 (CI-hi < 45.0, `:244,247`), MARK-1000 / TREND-FLOOR@1000 (prefix < 52.0, `:261`), COMBO-BAR@2700 (prefix < 55.0, `:278`) and the CI rule at MARK-2700 with its half-a-half-width margin (`:970-996`) — all Magnus's confirmed constants; the bar plausibility guard (`:398-406`, `[30,70]`) admits 51.33. Their firings are **OPERATIONAL CANCELLATIONS** that free a core, typed `cancellation`, never `verdict`. **The floors bind REMOTE too (`a50f27ef`, s48, via `tools/remote_cancel.py`), so the binding registration is SAME HOST — one host, LOCAL by default; moving it is an amendment typed BEFORE the first row.** ⛔ **(c) IS PRICED IN READ-BEFORE-RATIFYING #3 and it is where the exemption decision is worth ~6.7× on completion probability.**
**Everything else on this page (F1, F2, F3, D3, D4, the seat / map / class splits, the additive-prediction calibration) is DIAGNOSTIC and cannot rescue a failed bar. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## ⛔ RATIFICATION BLOCKERS — THREE THINGS THE BUILDER MUST SETTLE BEFORE LOCKING

Written as blockers rather than caveats because each one changes a registered
number, and an amendment after the fire cannot repair a registration.

**B1. NAME THE DOSE BATTERY'S OPPONENT.** The relay reports `+4.00pp` and
`+14.5pp` from `250 cells/arm` and does not say what the arms played against. If
it was **`_v468kladturbo`**, the figures are a paired ON/OFF ablation against a
third bot and the additive projection to a **treatment-vs-carrier** share is a
model. If it was **the carrier itself**, the figures ARE the estimand this shard
measures at larger n and the projection is an identity. **The exemption's class
claim and the `REGISTERED ADDITIVE PREDICTION` both depend on which.** One line
in the lock commit settles it; nothing else on this page needs to move.

**B2. BUILD THE TWO BATTERY COPIES, AND VERIFY THE LOG PRINTS.** F1 and F2 both
require trees that do not exist at draft:
* **F1 copy** — treatment with `LOKI_RAYDISC_LOG = True`, `NOISE_ON = True`
  (the shard's regime), plus a carrier copy for the opponent side.
* **F2 copies** — treatment and carrier both with `NOISE_ON = False`
  (`LOKI_RAYDISC_LOG` may stay False; the instrument is the replay digest).
⛔ **AND THE LOG MUST BE SEEN TO PRINT BEFORE IT IS TRUSTED.** `LOKI_RAYDISC_LOG`
is our own output, and `CLAUDE.md`'s LOKI-14 ruling is that a leg planning to
read its own tag out of a replay is planning on an instrument that does not
exist. **The exemption that applies here is narrow and must be stated: this is a
LOCAL surface and `_rd_log` writes to `sys.stderr`, not `print()`** — console-only
and captured by nothing the platform strips. **The positive control is one game:
run the F1 copy on a map and seed where the carrier is known to lay a belt on a
core line and confirm `RD507` lines appear on stderr.** A log that has never been
seen to print is not an instrument, and `es=`/`chp=`/`thp=`/`b=` are the four
fields every F1 number below is computed from.

**B3. DECIDE THE EXEMPTION AND TYPE IT WITH ITS CITATION, OR ESCALATE.** Per
READ-BEFORE-RATIFYING #3 the token is typeable by class here. **If the builder
does not agree, the arm must not be fired unexempted at P(completion) ≈ 0.13 —
it goes to Magnus, as `BELTBREAK-EARLY` did.** Either branch is defensible; firing
without choosing is not.

---

## THE DOSE EVIDENCE — FIRINGS ONLY, NO EFFECT SIZES BANKED

**⛔ THIS SECTION IS BANKED MECHANISM EVIDENCE, QUOTED FROM THE s49 RELAY. IT
CONTAINS NO OUTCOME NUMBER THIS PAGE MAY USE AS ONE.** The battery is small, is
unregistered, ran in a regime the shard does not run (`NOISE` off), and its
artefacts are not on disk. It establishes that the change FIRES and how, and
nothing about whether it PAYS at the registered n.

**Fixture: 500 games (250 paired deterministic cells per arm), `NOISE` off,
`--tle 10`, NOWINNER 0/500.**

| quantity | carrier (`ON = False`) | this arm (`ON = True`) |
|---|---|---|
| **undosed cells, end-state** | — | **181 / 181 BYTE-IDENTICAL (+0.000pp)** |
| **dosed cells (share)** | — | **69 cells, +14.5pp [+6.1, +22.9]** |
| dosed-game fraction | **27.6%** | **27.6% — IDENTICAL** |
| economy kills | 0 | **128, at 2.13 shots each** |
| core damage per dosed game | — | **+325** |
| fwd-sentinel firing span (rounds) | 96.9 | **114.5** |
| shots per fwd sentinel | 38.4 | **44.1** |
| first fwd-sentinel fire | r137 | **r137 — UNCHANGED** |
| pooled share | — | **+4.00pp [+1.57, +6.43]** |
| discordant cells | **0 OFF-only** | **10 ON-only** (no win flipped to loss) |
| ITT timely-kill | 26.4% | **28.4%** |
| median kill round | 222 | **220** |
| dosed-subset kill median | — | **+4 to +7 rounds SLOWER** |
| kill-currency decomposition | — | **+4 kill-wins / −10 kill-losses / +5 r1000 (all wins)** |

* **FLAG-OFF IS THE CARRIER BYTE-FOR-BYTE** — `LOKI_RAYDISC_ON = False` makes
  `rd_scan` false at `main.py:986` (with `LOG` also false), so the diversion
  block is unreachable; and the carrier tree contains no RAYDISC symbol at all.
  ⭐ **The 181/181 zero is not a blind zero: the same instrument produced 10
  discordant cells in the other direction, which is what makes the zero mean
  something.**
* **0 NOWINNER in 500 games.**
* ⚠ **THE BUDGET BINDS, AND ONE OBSERVATION ABOUT IT IS AMBIGUOUS:** the relay
  records **18 diversions were a sentinel's last**. That is consistent with
  "the diversion was taken shortly before death" and equally with "diverting cost
  the sentinel its life" — the opposite of the survival mechanism in #7. **It is
  registered as an open observation and is part of F1's budget histogram, not as
  evidence for either reading.**
* ⚠ **THE SURVIVAL MECHANISM IS NOT IDENTIFIED** (READ-BEFORE-RATIFYING #7): the
  dosed subset is selected by geometry, not randomised.
* ⚠ **HALF THE SHARE GAIN IS r1000 TIEBREAK WINS** (READ-BEFORE-RATIFYING #1).
* ⛔ **TLE / CPU CANNOT BE MEASURED LOCALLY AND THE LOCAL NUMBER WOULD BE
  UNINFORMATIVE, NOT ZERO.** Local replays carry no exec-time fields at all
  (obligations doc, s42 addendum: `tled/exec_sum/exec_max/over10k = 0` across
  1,649 builder-turns while the same decoder reads 8,847 µs on platform
  replays) and `get_cpu_time_elapsed()` returns 0 on local unit-turns. **The
  structural argument is what carries, and it names a real asymmetry rather than
  claiming none:** the arm adds, **in the treatment only** (the control has no
  such code), one `BB_SITE_VALUE` dict lookup and one `ct.get_hp(bid)` call per
  ENEMY ECONOMY tile on ONE forward sentinel's ray, plus a latched `_rd_forward`
  that short-circuits after its first True. A sentinel's attack radius is
  r²=32, so its single-tile-wide ray is a handful of tiles; the added work is
  bounded by that count and adds no loop, scan or allocation. `--tle 10` caps a
  timeout engine-side. **`LOKI_RAYDISC_LOG = False` in the shipped tree, so the
  stderr instrument costs nothing here — and the F1 battery copy that turns it
  ON is a different tree and must never be the one screened.** If this arm is
  ever promoted toward a ship, the platform `cpu_watch` alarm is the surface that
  can see this dimension.

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on this arm's pooled
share vs `bots/_v488beltbreak2` falls BELOW 51.33.** That excludes the arm's own
bar, on the fixture where the null is structural.

**SECOND FALSIFIER (the r300 admission bar, and it can fail on its own while the
share passes):** the 95% CI UPPER bound on (treatment − control) ITT RMST₃₀₀
fails to EXCLUDE +5.0 rounds, **or** the CI LOWER bound on the ITT
timely-kill-by-r300 difference fails to EXCLUDE a fall of 3.0pp. **Either failure
is disqualifying on its own, regardless of the share** — `PLAY_DEFENCE:
not_at_the_kill_s_expense`, and this arm's mechanism IS a bounded deferral of
core damage, which is why the bar is carried on an offensive plank. ⚠ Read with
the zero-sum disclosure attached to the bar.

**THIRD FALSIFIER (the doctrine composition, and it is the one this arm is most
exposed to):** the share gain over 50.00 is **majority r1000 tiebreak wins**.
Then the reading is downgraded one band and labelled `OFF-DOCTRINE COMPOSITION`
— combination input only, no ship conversation, no head-to-head. **This is
registered as a falsifier and not as a caveat because the dose battery already
measured the composition at 5 of 10, i.e. the boundary case.**

**SEGMENT FALSIFIER (measured on F2, and it is the clause that can surprise the
person running it):** **the UNDOSED matched cells must be BYTE-IDENTICAL between
arms.** The mechanism says an unengaged treatment IS the carrier. **If undosed
cells diverge, the mechanism story is refuted even if the pooled bar clears** —
either the arm changes behaviour where it claims not to (an unregistered second
effect), or the harness is contaminated. **Registered handling: a pooled
clearance with a diverging undosed complement is reported as ATTRIBUTION
UNRESOLVED and promotes nothing.** ⭐ This is stronger than a map complement
because it is an EXACT per-cell check with no interval.

**MECHANISM FALSIFIER (independent of all of the above, and it fires FIRST):**
* if **F1** shows the treatment's diversions per game are **not above zero in the
  shard's own `NOISE_ON = True` regime**, or the dosed-game fraction has collapsed
  well below the 27.6% anchor, **the change did not deliver its dose in the
  population that was screened** and the share is **uninterpretable**: a flat share
  would mean "the mechanism never fired", not "the mechanism fired and did not
  pay". The primary is then reported as **NOT MEASURED**, not as a null;
* ⭐ **if F1 shows the `BUDGET = 6` cap NEVER BINDS, the rail that bounds the
  kill-clock cost is DECORATION and the r300 argument loses its arithmetic
  backing** — which is a finding about the design, reported as one. (The anchor
  says it binds: 18 diversions were a sentinel's last, and 128 kills at 2.13
  shots ≈ 273 diverted shots across the battery.)
* ⭐ **if F2 shows undosed cells diverging, or dosed cells NOT diverging, the
  wiring is wrong.** A share near 50 with no divergent dosed cells is a WIRING
  NULL, not a finding about shot discipline — s47's delta D2 records a wiring
  null escaping demos to a 436-game shard.
* if **F3** shows the treatment's forward-sentinel firing span is NOT above the
  control's, the survival hypothesis of #7 did not reproduce — which does not
  refute the share but does remove the only mechanism story we have for it, and
  must be reported rather than dropped.
Per FIRINGS-BEFORE-PRIMARY all of F1 and F2 are read, and their numbers written
down, BEFORE the primary is typed.

### ⭐ THE HONEST-NULL CLAUSE — pre-committed, because two of these nulls are genuinely informative

**Three null states, and they are NOT the same finding. The registered
discriminator is F1+F2, and it is read before the share.**

| state | evidence | pre-committed reading |
|---|---|---|
| **(1) THE DOSE DID NOT LAND AT NOISE ON** | F1 shows ~zero diversions or a collapsed dosed fraction in the `NOISE_ON = True` regime; F2 clean | **NOT MEASURED.** The leg says nothing about shot discipline. The finding is about the REGIME: the paired NOISE-off fixture that selected this arm does not reproduce its own trigger rate in the shipped configuration — which is a fact worth banking about every paired-deterministic design on this board, not just this one. The road stays open; the repair is a probe, not a verdict. |
| **(2) THE DOSE LANDED AND DID NOT PAY** | F1 above zero at ~27.6%, F2 shows the exact undosed/dosed split, and the share is flat or negative | ⭐ **A REAL FINDING ABOUT THE PLANK, and it is bankable: the core plink a forward sentinel gives up is worth MORE than the belt kill it buys, at a 6-shot dose.** That prices the shot-discipline axis DOWNWARD and it contradicts the F0 ammo arithmetic that motivated the whole axis (2 shots vs 28) — **a genuine surprise, to be written down before it is explained away.** ⚠ Attribution bound: it does NOT separate "belt kills are low-value" from "the 12-round core delay costs more than the belt kill returns". Naming which needs a dose-varied arm (`BUDGET` 2 / 6 / 12), which this leg is not. |
| **(3) THE DOSE LANDED, THE SHARE PAID, AND THE GAIN IS TIEBREAKS** | F1/F2 clean, share clears, and the decomposition is majority r1000 | ⭐ **ALSO A REAL FINDING, and it is the one this arm's own dose battery points at.** The mechanism delivered SURVIVAL, not KILLING: `OFF-DOCTRINE COMPOSITION`, combination input only. **This is banked as a fact about the mechanism** — belt denial buys longevity rather than tempo — **and it closes the "ray discipline is a kill accelerant" reading while leaving the share gain on the record.** |

**The dose evidence is strong, so (2) and (3) are the likely nulls and both are
pre-labelled INFORMATIVE. That is the reason this arm is worth a core.**

---

## READING, PRE-COMMITTED

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first
row whose condition holds is the reading. Rows are disjoint by construction.**
**Every band below is CONDITIONAL on F1 and F2 having been read first, on the
r300 admission bar having HELD, and on the r1000/core-kill decomposition having
been computed. An r300 failure overrides every row and the reading is
`OFF-PROGRAMME — kill delayed`, whatever the share. A majority-r1000 composition
DOWNGRADES the row by one and appends `OFF-DOCTRINE COMPOSITION`.**

| # | band on this arm's pooled share vs `bots/_v488beltbreak2` at n = 5,400 | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **RAY DISCIPLINE ADDS TO ITS OWN CHASSIS.** Real and resolved on the fixture whose null is structural, and the clause is isolated by construction. Promotes to (a) a combination input — `eco.py` and `raid.py` are byte-identical to the carrier's, so the plank is disjoint from the eco trio and the beltbreak ladder by construction — and (b) **a separately-registered `_v507raydiscipline` vs `_v468kladturbo` screen, which is the only thing that can address the absolute level and the `X3R0_SLOT_RULE` 60±2 threshold**, and only then (c) a head-to-head against the holder. ⚠ Report the size with its OB16 status: the BAR's MDE is 0, but clearing this BAND excludes 50.00 AND 51.33, so an implied minimum effect of +1.33pp may be claimed and nothing larger. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** (includes the whole [51.33, 52.4] window an A/A cell has already produced) | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Pre-registered as WEAK: `NULL125`'s byte-identical A/A read 51.04 and the two A/A cells are 1.77pp apart. Rows are KEPT; no ship conversation; **a replication on fresh seeds, same host, is the price of promoting it — reported SEPARATELY and never pooled** (the GUNAXABL/SENTTHR precedent: unregistered pooling is optional stopping with extra steps). |
| **3** | **point < 51.33 AND CI contains 50.0** | **PARITY — THE DIVERSION IS FREE.** 128-per-500-games worth of belt kills, their diverted core plinks and their up-to-12-rounds-per-sentinel of deferred core damage all pay for themselves and nothing more. **Against the F0 motivation that is the informative sentence: the 2-shots-vs-28-shots ammo arithmetic is real and does not convert to game share at a 6-shot dose, so the family's next iteration is DOSE (`BUDGET`) or SITING, not the ladder order.** Does NOT license a ship. |
| **4** | **CI upper < 50.0** | **THE DIVERSION SUBTRACTS.** `LOKI_RAYDISC_ON = True` dies as a ship candidate at this dose. Attribution is bounded: this refutes *diverting a forward sentinel's core-facing shot to a belt tile at a 6-shot budget with a 90-HP endgame release*, **not** *forward sentinels*, **not** *the beltbreak family* (whose own arm measured 53.09 vs `_v468kladturbo`) and **not** *economy denial in general*. **REGISTERED CONSEQUENCE: the core plink is confirmed as the better shot on our own chassis, no further gate-order arm is written on the sentinel path, and the surviving shot-side lever is the beltbreak GUNNER (which is already the arm that pays).** |

⚠ **Nothing here treats 50.0 as a floor.** A share below 50 is a live outcome
with named mechanisms — up to 12 rounds of deferred core damage per forward
sentinel; the possibility that the diversion draws return fire that kills the
platform (the 18-last-diversions observation); a belt tile rebuilt in a median of
2 rounds by the field, making a killed tile a PERPETUAL target rather than a
removed one (`doctrine.py:2135-2138`) — and it is pre-named so a negative is not
explained away as noise.

⛔ **AND ONE CROSS-BAND NOTE, registered so it is not improvised: an operational
cancellation reaches NONE of these rows.** Per READ-BEFORE-RATIFYING #3 a
`TREND-FLOOR@1000` or `COMBO-BAR@2700` firing is a stop on a prefix draw and the
reading is `CANCELLED — the diversion question is UNRESOLVED and defaults to the
RESTRICTION`, with the partial disclosed as selected-pessimistic.

---

## FIRINGS-BEFORE-PRIMARY — the reads, with exact invocations

**Measurability is declared per read. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape happens
to carry.** ⛔ **F1's instrument IS our own stderr output and that is disclosed
rather than hidden** — the exemption is narrow and stated in `B2`: LOCAL surface,
`sys.stderr` not `print()`, plus an engine-side cross-check that does not need
the log at all. **F2 and F3 read engine-side facts only.**

⛔ **AND THE FIRINGS RULE IS A HARD SEQUENCE** (`docs/prereg/BARS.tsv` header,
research 2026-08-16T13:27:33Z):
> **F1 and F2 are RUN, and their numbers written down, BEFORE any sentence
> containing this arm's primary share is typed.** A primary typed ahead of the
> firings read is a REGISTRATION BREACH regardless of what it says, and the
> repair is an amendment chain, not a re-write. *(Precedent on the tape:
> `results.tsv:kladladder-verdict-amendment-f1f2-pending`.)*

**⛔ THE SHARD ITSELF CANNOT SEE THE MECHANISM.** `tools/overnight.sh:138-139`
runs every game with `--replay /dev/null`; the tape's columns are
`ts shard game map seed seat winner cond turns` — **no entity, build, position,
shot or turret information exists on it, in either arm.** Every mechanism number
below comes from a SEPARATE battery and **the shard's n = 5,400 lends them none
of its power.**

### F1 — THE SHARD-REGIME DOSE. MEASURABLE, on a separate battery, NOT off the shard tape.

⛔ **`tools/dose.py` MAY NOT BE USED FOR THIS READ, and the reason is checked, not
assumed (OB17 clause 2).** Two defects, either of which is disqualifying:
1. **IT CANNOT PASS `--tle 10`.** `tools/dose.py:227-229` is
   `[FCODE, "run", bots[0], bots[1], f"maps/{m}.map26", "--seed", str(seed),
   "--replay", str(rp)]` — **there is no `--tle` in the argv and no flag to add
   one.** The shard runs `--tle 10` (`overnight.sh:138-139`); a dose read at a
   different turn-time limit is a dose read on a different fixture. **CONSEQUENCE
   OF SILENT NON-EXECUTION: the read would not fail — it would quietly measure a
   different population**, which is the case OB17 exists for.
2. **ITS DEFAULT `MAPS` IS THE RETIRED 8-MAP SET** (`tools/dose.py:77`:
   `antler atoll drumlin fjordgate heart hive meander nordkap` — four of those
   eight are not in the live pool). Fixable with `--maps`, but moot given (1).
3. **AND IT MEASURES THE WRONG QUANTITY ANYWAY.** `dose.py` counts
   `fwdbuild_<kind>` BUILD events. **This arm builds nothing.** Its dose is a
   FIRE decision, and BUILD-event decoders are structurally blind to it.

**REGISTERED FORM — the direct invocation, SERIAL** (never parallel: D65, a
16-game parallel dose check once reported the OPPOSITE of a serial one and both
were wrong):
```
# F1 copies (B2): TREAT = treatment with LOKI_RAYDISC_LOG = True, NOISE_ON = True
#                 CTRL  = bots/_v488beltbreak2 (unmodified; the shard's control)
for M in antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate \
         glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune; do
  for ORD in A B; do            # both seats, exactly as overnight.sh does
    .venv/bin/fcode run $TREAT $CTRL maps/$M.map26 --seed $S --tle 10 \
        --replay scratchpad/rd_f1/g${M}_${ORD}_${S}.replay26 2> scratchpad/rd_f1/g${M}_${ORD}_${S}.err
  done
done
```
**REGISTERED SIZE: 180 games** (15 maps × 2 seats × 6 seeds — the same balance
`overnight.sh` uses, so the dose is measured on the shard's own population
shape). **Seeds for F1/F2/F3 come from a base OUTSIDE the shard's registered
range** (see `SEEDS`) so no battery game can collide with a screened game.

**THE FOUR NUMBERS, off the `RD507` stderr lines (`ARM r<rnd> id<id>
at<x>,<y> (<tx>,<ty>) es=<n> chp=<coreHP> thp=<targetHP> b=<budget>`):**
* **(a) DIVERSIONS PER GAME** = count of `RD507 ECON` lines / games. **This is the
  dose. Pre-registered expectation: strictly above zero in the `NOISE_ON = True`
  regime; the branch-1 falsifier fires if it is not.**
* **(b) DOSED-GAME FRACTION** = share of games with ≥ 1 `ECON` line.
  **Pre-registered expectation: ~27.6%** (the NOISE-off anchor). At n=180 the
  half-width on a 27.6% rate is **±6.5pp**, so this read resolves "the dose
  survived the regime change" and **does not** resolve a 5pp shift in the
  fraction — **declared, per OB12, and the unresolved case defaults to the
  restriction.**
* **(c) ECONOMY KILLS** = `ECON` lines with `thp <= 18` (one sentinel shot
  finishes the target). **Pre-registered expectation: > 0, at ~2 shots per kill.**
  ⭐ This is why `_rd_log` passes the PRE-shot HP explicitly
  (`main.py:1033-1036`) — a post-shot re-read would see `hp − 18` or a dead tile,
  and a repeat-fire proxy would conflate FARMING one rebuilt tile with failing to
  kill it.
* **(d) BUDGET HISTOGRAM** = distribution of the `b=` field's maximum per
  sentinel id. **THE 6-CAP MUST BIND ON SOME SENTINEL LIVES OR THE RAIL IS
  DECORATION** — and the rail is the entire arithmetic basis of the r300 argument.
  A histogram with no mass at 6 is a registered finding against the design, not a
  footnote.

**⭐ THE ENGINE-SIDE CROSS-CHECK, so F1 does not rest on our own output alone.**
`tools/corpus/replay_events.py` emits **BUILD and DEATH** rows
(`file ev rnd team kind x y d2_own d2_enemy mw mh`, `:157`), with the rotation
guard at `:16,113` (a build is the FIRST `placeEntity` carrying an id — recorded
as a check that came out clean, not as one that was absent). ⇒ **count enemy
HARVESTER / CONVEYOR / SPLITTER DEATH events per arm.** ⚠ **It is a SUPERSET, not
an attribution** — a belt tile also dies to a beltbreak gunner or a builder
attack — **so the admissible form is the DIFFERENCE on matched F2 cells, where the
undosed cells contribute exactly 0 by construction.** Agreement in direction
between an instrument that reads our own stderr and one that reads the engine's
event stream is what makes (c) more than a log line.

### F2 — THE WIRING AND ATTRIBUTION READ. THE EXACT INSTRUMENT. MEASURABLE off replay digests.

The F0-style check, used in anger: with `NOISE_ON = False` a given `--seed` is
**engine-deterministic** (F0, md5-verified: 3 runs at seed 852900 byte-identical,
852901 differed), so a matched cell is an EXACT comparison with no interval.
```
# F2 copies (B2): TREAT2 = treatment with NOISE_ON = False
#                 CTRL2  = bots/_v488beltbreak2 with NOISE_ON = False
# ARM A: TREAT2 vs CTRL2      (the shard's fixture, flag ON)
# ARM B: CTRL2  vs CTRL2      (the same fixture, flag OFF == carrier-vs-carrier)
# same (map, seat, seed) triples in both arms; then:
md5 -q scratchpad/rd_f2/A/*.replay26 > A.md5 ; md5 -q scratchpad/rd_f2/B/*.replay26 > B.md5
```
**REGISTERED SIZE: 180 matched cells** (15 maps × 2 seats × 6 seeds), SERIAL,
`--tle 10`.
**Pre-registered expectations, all three directional and all exact:**
* **UNDOSED cells: digests EQUAL.** Predicted ~72.4% of cells. **Any inequality
  here is an INSTRUMENT ALARM** (harness contamination, a stray non-determinism,
  or a second unregistered effect) **and the cell is not read.**
* **DOSED cells: digests DIFFER.** Predicted ~27.6%. **Zero differing cells is
  the WIRING NULL and the primary then reads NOT MEASURED, never null.**
* **The dosed/undosed partition of ARM A must match the `RD507 ECON` presence
  from an F1-configured re-run of the same triples** — two independent instruments
  agreeing on which cells are dosed.
⭐ **AND THIS IS WHERE THE FREE NULL CONTROL LIVES: ARM B is literally
carrier-vs-carrier on the shard's own fixture, so its share is the STRUCTURAL
50.00 measured rather than assumed.** At 180 cells its half-width is ±7.3pp — a
DIRECTION-ONLY read, declared as such, and it is the cheapest available check
that the fixture is not biased before 5,400 games are spent on it.

### F3 — THE SURVIVAL / CORE-DAMAGE READ. MEASURABLE off F1's retained replays; the #7 hypothesis's metric.
`tools/corpus/replay_autopsy.py` decodes `fireTurret` (`:191`) and the `UpdateHp`
core-damage ledger (`:116-121, :184-191`) with a self-checking identity (summed
per-source damage must equal the summed `UpdateHp` deltas on the core id). Off
`scratchpad/rd_f1/*.replay26`, per arm:
```
#   (a) fwd-sentinel firing span: last fire round - first fire round, per sentinel
#   (b) shots per fwd sentinel, and first-fire round (expect UNCHANGED ~r137)
#   (c) core damage per game on the ENEMY core, dosed cells vs undosed cells
```
**Pre-registered expectation, and it is the hypothesis's own direction:** (a) and
(b) HIGHER for the treatment, (c) higher on dosed cells. ⚠ **`replay_autopsy.py`
is a SINGLE-GAME tool** (`docs/prereg` precedent: name the loop rather than
pretend the tool has it) — **the aggregation loop is a builder to-do and is named
here rather than assumed.** ⛔ **AND F3 CANNOT IDENTIFY THE CAUSE** (#7): the dosed
subset is geometry-selected, so a rise in span is consistent with "the diversion
bought survival" and with "the games with a belt on the ray were the games our
sentinel was going to live in anyway". **F3 measures; it does not attribute.**

### D3, D4 — the outcome-shape reads. MEASURABLE, shard-native.
`cond` and `turns` are on the tape.
* **D3 — THE r300 ADMISSION BAR** (see `KILL-ROUND NON-REGRESSION`). ITT RMST₃₀₀
  per side over all 5,400 rows, plus the ITT timely-kill-by-r300 rate per side,
  plus the kill-win-conditioned share and conditioned median as DIAGNOSTICS. Both
  bars scored as exclusions off `tools/cluster_ci.py --null`. **Read with the
  zero-sum disclosure.**
* **D4 — COND MIX AND THE DOCTRINE DECOMPOSITION**, and on this arm D4 is not a
  formality: the share of games ending `core_destroyed` / tiebreak / `NOWINNER`
  per arm, **the treatment's median kill round** as the gross within-arm backstop
  (crossing 300 is disqualifying), and **the mandatory r1000/core-kill split of
  the share gain** that READ-BEFORE-RATIFYING #1 and the THIRD FALSIFIER are
  denominated in. Anchor from the carrier's own completed tape
  (`results.tsv:beltbreak2-final`): timely-kill **30.80% [29.56, 32.03]**,
  r1000 share **11.28%**.

### NOT MEASURABLE on this leg — named, not silently dropped.
* **DIVERSIONS, ECONOMY KILLS, BUDGET USE, FIRING SPANS AND CORE DAMAGE ARE NOT
  DECODABLE OFF THE SHARD.** `overnight.sh:138-139` runs `--replay /dev/null`:
  **local corefill keeps TAPES, not REPLAYS.** The tape carries share, kill round,
  `cond` mix and D3's rates, **and nothing else.**
* **THE DOSED/UNDOSED SPLIT IS NOT COMPUTABLE ON THE SHARD** (READ-BEFORE-
  RATIFYING #4): `NOISE_ON = True` defeats pairing and the tape carries no dose
  marker. It lives on F2.
* **WHAT A DIVERTED SHOT WAS AIMED AT, IN THE CONTROL.** The control has no
  RAYDISC code, so `es=` (eligible economy tiles on the ray) is unmeasurable in
  the control arm of the SHARD. ⭐ It IS measurable in a LOG-enabled control copy
  — `main.py:986` deliberately reads `LOKI_RAYDISC_ON or LOKI_RAYDISC_LOG`, so a
  control with `LOG = True` and `ON = False` scans and logs the opportunity it
  declines (`doctrine.py:2171-2180`). **That is the geometric-starvation
  instrument and it is registered as an OPTIONAL fourth battery, not as a
  requirement of this leg.**
* **SHOT-LEVEL ATTRIBUTION OF THE CORE-DAMAGE SURPRISE.** F3 gives spans and
  ledgers; it cannot randomise geometry.
* **PER-UNIT CPU / TLE.** Blind zero locally; labelled UNINFORMATIVE, not clean.
* **ANYTHING ABOUT THE FIELD.** The opponent is our own carrier. The 27.6%
  trigger rate is a fact about our belt-laying policy, and `CLAUDE.md` rule 6
  means no road is closed here.

---

## THE CHANGE — `file:line`, carrier → treatment

**TREATMENT TREE: `bots/_v507raydiscipline`** = `bots/_v488beltbreak2` plus ONE
mechanism, in TWO files. Verified at draft and re-runnable in four commands:

```
$ cmp bots/_v488beltbreak2/eco.py  bots/_v507raydiscipline/eco.py    # clean
$ cmp bots/_v488beltbreak2/raid.py bots/_v507raydiscipline/raid.py   # clean
$ diff bots/_v488beltbreak2/doctrine.py bots/_v507raydiscipline/doctrine.py \
      | grep -E '^[<>]' | grep -vE '^[<>] *(#| *$)'
> LOKI_RAYDISC_ON = True          # master switch; False == _v488beltbreak2 exactly
> LOKI_RAYDISC_FWD_DSQ = 50       # forward test (d^2 of the ENEMY anchor).  50 is
> LOKI_RAYDISC_MAX_HP = 36        # 2 sentinel shots x 18 dmg.  VACUOUS today --
> LOKI_RAYDISC_BUDGET = 6         # economy shots per forward sentinel PER LIFE.
> LOKI_RAYDISC_CORE_HP_STOP = 90  # 5 sentinel shots.  At or below this the core
> LOKI_RAYDISC_LOG = False        # LOCAL instrument, stderr, one line per sentinel
$ diff -u bots/_v488beltbreak2/main.py bots/_v507raydiscipline/main.py   # 4 hunks
```
⇒ **`doctrine.py`: SIX new constants and nothing else** (115 diff lines, of which
the remainder is the 94-line `LOKI-RAYDISCIPLINE` reasoning block at
`:2087-2181`; **no existing line is modified or removed** — every `<`-side line in
the diff is zero, which is what makes this an ADD-ONLY change to the constants
module).
⇒ **`main.py`: FOUR hunks, all additive.**
1. **`:167-177` — two per-sentinel fields**: `self.rd_econ = 0` (the per-life
   budget counter, never resets) and `self.rd_fwd = False` (the forward latch,
   latching TRUE only, exactly as `bb_seen` does, because `SLOT_ENEMY_CORE` is
   seeded by REFLECTION at `main.py:246` before anyone has SEEN a core).
2. **`:979-1005, :1030-1045` — the scan and the diversion**, inside `_turret`
   (`:937`). `rd_scan` decides whether the existing ladder ALSO collects economy
   candidates; `rd_arm` decides whether it may ACT on them.
3. **`:1053-1062` — a TAIL log line** so the CORE/ECON split has a measured
   denominator (LOG-gated; inert in the shipped tree).
4. **`:1070-1130` — `_rd_forward` and `_rd_log`**, two new methods.

**THE MECHANISM SITE, and it is exactly one** (`bots/_v507raydiscipline/main.py`):
```python
1030            if rd_arm and rd_best is not None and best_prio == 0 \
1031                    and rd_core_hp is not None \
1032                    and rd_core_hp > LOKI_RAYDISC_CORE_HP_STOP:
1033                ct.fire(rd_best)
1034                self.rd_econ += 1
```
**`best_prio == 0` is the whole safety argument for precedence:**
`TURRET_PRIO[CORE] = 0` and **nothing else scores 0** (`main.py:51-57`: SENTINEL 1,
GUNNER 2, BUILDER_BOT 3, LAUNCHER 4, HARVESTER 5, CONVEYOR/SPLITTER 6,
BARRIER 7), so the diversion fires **only** where the parent ladder had already
chosen a core tile. **Every enemy turret, builder and launcher on the ray keeps
its existing precedence, untouched.** And the candidate set is team-checked at
`:997-1000` (`et` is set only when `get_team(bid) != self.team`), so an own-goal
is impossible on this path.

**WHAT IS SHARED WITH THE BELTBREAK LADDER, and it is one dict, deliberately:**
`BB_SITE_VALUE` (`raid.py:80-83`, imported at `main.py:40`) — HARVESTER 100,
CONVEYOR 40, SPLITTER 40 — reused verbatim **so the two planks cannot disagree
about what a belt tile is worth.** `raid.py` is byte-identical, so nothing about
the beltbreak gunner path changes; the two mechanisms share no counter and no
store slot (`SLOT_BELTBREAK = 13` is written only by the beltbreak ladder;
`rd_econ`/`rd_fwd` are per-unit instance state with no store slot at all).

**⭐ AND ONE STRUCTURAL PROPERTY WORTH A CERTIFIER'S MINUTE: the diversion cannot
be reached by a home sentinel, a gunner, or a launcher.** `main.py:986-988`
requires `turret_type == EntityType.SENTINEL` and `self._rd_forward(ct, p)`; the
latter requires `dsq_core(p, E) <= 50` of the enemy anchor **and**
`dsq_core(p, ours) > HUNT_BAND_DSQ`(41) of our own, using `enemy_core_for` as an
involution so no extra store slot or state is needed. **The exclusions are
enforced by conditions, not by intent** — which is what makes #8's guard audit
possible at all.

---

## SEEDS

**SEED BASE: 854000.** Registered worklist row (**to be appended by the builder,
not by this agent**):
```
RAYDISC bots/_v507raydiscipline bots/_v488beltbreak2 5400 854000
```
**FREENESS, verified at draft on five surfaces, with a POSITIVE CONTROL RUN FIRST
so the check has been seen to produce the other verdict:**
* **POSITIVE CONTROL: `grep -c '826000' scratchpad/corefill_work.txt` → 1**, the
  `ODINVSSLEIP` row. **The grep HITS when it should hit.**
* `grep -c '854000' scratchpad/corefill_work.txt` → **0**;
  `scratchpad/fleet_queue.tsv` → **0**;
  `grep -l '854000' scratchpad/overnight/*.tsv` → **no file**;
  `grep -l '854000' docs/prereg/*.md` → **no file**;
  `grep -c '854000' docs/prereg/BARS.tsv` → **0**.
* **Same-day registered bases enumerated per file, not assumed** (`grep -n
  'SEED BASE' docs/prereg/PREREG-*2026-08-17.md` plus the worklist tail):
  822000 `BELTBREAK-EARLY`, 824000 `BELTBREAK-LATE`, 826000 `ODINVSSLEIP`,
  828000 `KLADLADDER2`, 830000 `KLADLADDER3`, 832000 `SEALPIERCE`,
  834000 `ECOMMIT2`, 836000 `OPENFAST`, 840000 `BELTBREAK2`, 848000 `BBCAP3`,
  850000 `BBAMMO`, 852000 `BBDEMAND`. **854000 is the next free base at the
  2000-wide stride this family uses.** ⚠ Three of those (`BBCAP3`, `BBAMMO`,
  `BBDEMAND`) were HELD and never fired; their bases are avoided anyway, because
  a registered base is registered.
* ⭐ **NO OVERLAP, verified by reading the runner rather than assuming it.**
  `tools/overnight.sh:124` is `seed=$(( SEEDLO + n / 16 ))` — **sixteen games per
  seed** — so a 5,400-game shard consumes **338 distinct seeds, not 5,400**.
  RAYDISC at 854000 uses **854000-854337**; the nearest registered neighbour
  (`BBDEMAND`, 852000) would use 852000-852337. **1,662 seeds of headroom, and the
  stride is ~6× larger than it needs to be.** ⛔ **A naive grep-for-collisions
  returns FALSE POSITIVES on any prereg that verified its own seed freeness**
  (`PREREG-OPENFAST:314` records a freshness line naming 840000; that is a check,
  not a registration) — named so no successor re-derives it as a conflict.
* ⛔ **THE F1/F2/F3 BATTERIES USE A BASE OUTSIDE THE SHARD'S RANGE**, registered
  as **860000-860999**, verified free at draft by the same five greps (0 on the
  worklist, `fleet_queue.tsv`, `BARS.tsv` and every shard tape; the only `.md` hit
  is this page's own freshness line). ⚠ **A bare `grep '8600'` on the worklist
  returns FOUR hits and all four are SUBSTRING false positives** — 286000
  (`SENT41`, deferred), 386000 (`CMB291`), 486000 (`H605h2`), 786000 (`COLLARF`) —
  **the same defect class as the OPENFAST case above, and the reason the check is
  run on the full six digits.** Reusing the shard's seeds for the mechanism read
  would screen the arm on the seeds that measured it.
* ⛔ **AND THE BUILD BATTERY'S OWN SEEDS ARE EXCLUDED FROM BOTH.** The relay does
  not publish them, which is itself a reason to keep the screen at a base no
  battery has touched; **if the builder knows them, they are recorded in the lock
  commit and excluded explicitly.**

---

## AMENDMENTS

**ADD-ONLY, and blind to the data.** Any amendment to this document is a NEW
dated section appended below this line, never an edit to anything above it; it
must be typed and committed BEFORE the number it could bear on exists, and it
must say what it is blind to. An amendment that removes, weakens or re-words a
registered bar, falsifier, band, segment, prediction or MDE is not an amendment —
it is a new pre-registration and needs a new leg. *(`tools/prereg_check.py
--amendment <locked.md> <amended.md>` is the checkable form.)*
**Pooling extra rows into this shard after lock is an unregistered n increase —
optional stopping with extra steps — and is prohibited. A replication on fresh
seeds is reported SEPARATELY and NEVER pooled** (the GUNAXABL/SENTTHR precedent:
remote replications corroborated a null they were not allowed to rescue).
⛔ **Settling `B1` (naming the dose battery's opponent) is a DISCLOSURE, not an
amendment — it adds a fact about a battery that already ran and touches no
registered number except by making the additive prediction's status explicit.
Settling it AFTER the shard's first row would be neither.**

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one LOCAL core to n = 5,400, plus 180 serial games for F1, 360 for F2
(two arms of 180), and the replay decode for F3.** ZERO rated ladder exposure,
zero submissions, zero unrated challenges — nothing on this page touches the
platform, which is why `TARGET BAND` is N/A rather than a number.
**⭐ AND THE EXPECTED VALUE IS GOOD BY THIS BOARD'S STANDARDS, which is the
opposite of the sibling `BELTBREAK2` page's position and worth saying plainly:**
at the projected 54.00 with the exemption typed, the arm reaches its own
registered n with probability **0.898** and clears Band 1 with probability
**~0.88**. **Unexempted it is 0.134, and that gap is the single highest-leverage
decision on this page.** The named downside is not the fixture — it is
READ-BEFORE-RATIFYING #1: **if the doctrine-clean share gain is ~2pp rather than
4pp, P(completion) falls to ~0.50 and P(Band 1) to ~0.17,** and the core most
likely buys a `cancellation` row plus the F1/F2/F3 mechanism reads.

**It does NOT decide a ship.** The strongest branch promotes the arm to
(a) a combination input — and the disjointness is verified, not assumed:
**`eco.py` AND `raid.py` are byte-identical to the carrier's**, so the plank
composes with the eco trio and with the beltbreak ladder by construction;
(b) **a separately-registered `_v507raydiscipline` vs `_v468kladturbo` screen**,
which is the only instrument that can speak to the absolute level and to
`X3R0_SLOT_RULE`'s **60% ±2pp** threshold (Magnus 2026-08-16; the board's ceiling
at that ruling was 55.24%, so the standing state is GRIND); and only then
(c) a head-to-head against the CURRENT slot holder's artifact, which is the
pipeline step Magnus's procedure names verbatim (*"we start by testing it against
the current slot, if it beats it we can switch"*). **Gate-1-to-gate-2
transitivity is UNVALIDATED in this repo (QUEUE #65: 3 concordant, 1 not), so no
step is skippable on the strength of this number.** And `SLOT_STOP_LOSS: off`
plus the parked SWITCH step of `X3R0_SLOT_RULE` mean **the slot changes only on
Magnus's explicit word**, whatever this leg returns.

**⚠ ONE KNOWN PREFLIGHT FAIL, NAMED AND NOT FIXED:**
`.venv/bin/python tools/preflight.py bots/_v507raydiscipline` FAILs on *"no
PREREG.md or README.md in bots/_v507raydiscipline — write the S0 block before the
build, not after the battery"*. **The carrier `bots/_v488beltbreak2` has neither
either, so this is not a regression introduced by this arm** — it is a standing
property of every tree in this family. Reported in one line; not fixed by this
agent. **All four modules parse clean** (`ast.parse` on `doctrine.py`, `eco.py`,
`main.py`, `raid.py` at draft).

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read IN FULL: OB7 the pre-state rule, OB8 denominators, OB10 identity-of-ledger, OB11 verify the treatment the EXPERIMENT requires, OB12 + its pre-committed restriction default, OB13, OB14, OB15a/b/c + the segment vocabulary and the units rider, OB16 + its `BAR = null + MDE + half_width` amendment, its zero-MDE corollary and its cross-host rider, OB17 + its "run the clause that can surprise you" rider, and the **2026-08-17T07:24:55Z addendum** that replaced the local-shard clock-2 boilerplate — quoted rather than restated) · `PROGRAMME.md` (parsed block `:6-30` — `INCUMBENT: bots/_v468kladturbo`, `PRIMARY_CURRENCY: game_share`, `WIN_RATE_IS_VERDICT: yes`, `KILL_WINDOW_RND: 250`, `R1000_IS_DEFEAT: yes`, `PLAY_DEFENCE: not_at_the_kill_s_expense`, `DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`, `SLOT_STOP_LOSS: off`, `X3R0_SLOT_RULE`; `:310-336` the game_share-vs-R1000_IS_DEFEAT collision and its resolution, which READ-BEFORE-RATIFYING #1 is built on; `:488-564` the r300 re-pricing chain in full — the 05:15:45Z re-pricing, the 05:19:38Z collider correction, the 05:3xZ arbitration freeze, and the **05:36:10Z ITT RMST₃₀₀ resolution with its vintage rule**; `:614-668` the kill-speed score and the `-10` tiebreak penalty) · `docs/prereg/PREREG-BELTBREAK2-2026-08-17.md` (**read IN FULL** — the house structure, token order, registered machinery and caveat set are inherited here where they apply; its map-class segment, its scale-drag hazard and its parent-pair void clause are NOT) · `docs/coordination.md` (`:70799-70804` **BBAMMO PREREG LANDED**, the clause-isolation redesign this arm adopts, including the carrier-pre-satisfaction finding and the pairs-vs-solos exemption ruling; `:70806-70811` **F0 LANDED**, the `ammo_converted − ammo_end = 4g + 10s` engine identity, the 94% pass-through, the 2-shots-vs-28-shots arithmetic that motivates this axis, and the **`--seed` is not inert engine-side** determinism correction; `:70813-70824` **RAY DISCIPLINE LANDED**, the sole source for every dose figure on this page) · `docs/prereg/BARS.tsv` (**header/format ONLY, incl. the FIRINGS-BEFORE-PRIMARY rule of 2026-08-16T13:27:33Z and the `le`-direction never-stop carve-out; the `V140VS152:259` and `ODINVSSLEIP:313` calibration rows read in full for the never-stop form and REJECTED for this arm, with the reason on the page; the `BELTBREAK-EARLY:310` and `BELTBREAK2:312` rows read in full for the COMBO-BAR-EXEMPT precedent and its escalation history — `grep -c COMBO-BAR-EXEMPT` → 2, both Magnus-granted solos. NO ROW WAS ADDED BY THIS AGENT**) · `CLAUDE.md` (the ONE GLOBAL ADDITIVE cost-scale factor; the DEFF scope procedure, its direction clause and the local 0.98 exemption; rule 6, a refutation needs live games and its rules-level carve-out; the `print()`-stripped-from-platform-replays ruling and the LOKI-14 instrument-that-does-not-exist lesson, which `B2` answers; `R1000_IS_DEFEAT`; the ladder's `delta = 32 × (S − E)` game-share arithmetic) · `bots/_v507raydiscipline/{doctrine,eco,main,raid}.py` (read at draft: `doctrine.py:2087-2200` the whole LOKI-RAYDISCIPLINE block and all six constants, `:474` `NOISE_ON = True`, `:1735` `LAUNCHER_MIN_RND = 160`, `:163` `HUNT_BAND_DSQ = 41`; `main.py:40` the `BB_SITE_VALUE` import, `:51-57` `TURRET_PRIO`, `:167-177` the new per-unit state, `:456` the spawn salt, `:790` the launcher round gate, `:937` `_turret`, `:957-971` the gunner early return, `:973-1005` the scan, `:997-1000` the team check, `:1030-1045` the diversion, `:1053-1062` the tail log, `:1070-1130` `_rd_forward` and `_rd_log`; `raid.py:80-83` `BB_SITE_VALUE`, `:704` `LOKI2_RUSH_RND`; `ast.parse` clean on all four) · `bots/_v488beltbreak2/{doctrine,eco,main,raid}.py` (the carrier, `cmp`'d and `diff`'d file-by-file; `doctrine.py:2078` the inherited `stack.py` compose marker; `git ls-files` / `git status --porcelain` / `git log -1` for its commit pin `997bcd42`; module md5s quoted) · `results.tsv` (rows `beltbreak2-final` — the carrier's completed 53.09% [51.76, 54.42] at n=5,400 with its timely-kill 30.80% and r1000 11.28% — `beltbreak-early-final`, `idnull140-cert-5400`, `null125-final`, `kladladder-n-final-correction`, `kladladder-verdict-amendment-f1f2-pending`) · `scratchpad/overnight/BELTBREAK2.tsv` (row count only, 5,401 non-`#` lines for a 5,400-game shard — the header-off-by-one, reproduced at draft) · `scratchpad/CONTROL_PIN` (the `_v468kladturbo` digest, quoted to show this leg's control is deliberately NOT it) · `tools/prereg_check.py` (read for `KNOWN_KEYS`, `key_pattern`/`field`, `first_number`/`raw_number`/`int_before`, `RULES` in full, `check_presence`, `check_arithmetic`, `untracked_arm_paths`, `git_diff_paths`, `ROUND_GATE_RE`, `_gate_values`, `_inert`, `check_metric_window`, `check_pool_era`, `DEFF`, and the `_defence_bar_ok` predicate that enforces the r300 form) · `tools/auto_gate.py` (`:244-247` `MARK_CATASTROPHE`/`MARK_MID`/`MARK_HALF`/`CATASTROPHE_CI_HI`, `:261` `TREND_FLOOR = 52.0` and its priced 08-16 raise, `:278` `COMBO_BAR = 55.0` and its pre-adoption pricing table, `:398-406` the `[30,70]` bar plausibility guard, `:715-742` `combo_of` and its read of the TREATMENT tree's `doctrine.py`, `:895-960` the clause order and the COMBO-BAR-EXEMPT citation guard, `:965-996` the CI rule and its half-a-half-width margin) · `tools/overnight.sh` (`:31` the deliberate `NOISE_ON` retention, `:57-68` the live 15-map pool, `:99-103` the `START=`/`# FIXTURE` stamp, `:119-124` the row-count resume and the `SEEDLO + n/16` seed walk, `:138-139` `--replay /dev/null --tle 10`) · `tools/overnight_read.py` (`:76-94` `map_area_class`) · `tools/dose.py` (`:74-77` the FCODE path and the RETIRED default MAPS, `:215-240` the run loop — read to establish that **no `--tle` is passed**, which is why F1 registers the direct form) · `tools/corpus/replay_events.py` (`:16,113` the rotation guard, `:157` the output columns, the BUILD/DEATH scope) · `tools/corpus/replay_autopsy.py` (`:116-121, :184-191` the `UpdateHp` ledger and `fireTurret` at `:191`; single-game scope) · `tools/preflight.py` (run at draft; the named FAIL) · `tools/control_pin.py` · `scratchpad/corefill_work.txt` (the row format and the 820000-840000 seed sequence) · `scratchpad/fleet_queue.tsv` (seed freeness) · `docs/prereg/PREREG-{BBAMMO,BBCAP3,BBDEMAND,OPENFAST}-2026-08-17.md` (`SEED BASE` lines only, for the enumeration) · `fcode run --help` (the `--tle` contract) · git `f1d6e6d4` (HEAD at draft), `git status --porcelain`, `git ls-files` and `git log` output quoted above · the drafting brief supplied by the builder lane s49. **No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run. The only write was this document.**
