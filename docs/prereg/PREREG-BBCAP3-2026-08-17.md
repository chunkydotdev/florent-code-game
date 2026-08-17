# SCREEN PREREG — `BBCAP3`: the beltbreak shredder cap raised to three, with the magazine sized to fund it (`LOKI_BELTBREAK_CAP` 2→3 **and** `LOKI_BELTBREAK_AMMO` 24→36, ONE mechanism)

Drafted by a fresh opus subagent with NO inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `docs/prereg/BARS.tsv` row, fired no game, started no
shard, and touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md`
nor `QUEUE.md`.

**⛔⛔ THIS DRAFT ENDS IN A RECOMMENDATION TO *HOLD*, NOT TO FIRE.** The
registration below is complete and lockable as written — it is drafted in full
because a HOLD that has not been costed is an opinion, and because the arm may be
revived cheaply later. **But the arm's own treatment-occurrence evidence now
points the WRONG WAY on two independent batteries, one of them measured on THIS
arm's exact mechanism on THIS arm's exact chassis.** The reasoning is in
`READ BEFORE RATIFYING #1` and the disposition is in `DRAFT DISPOSITION — HOLD`
at the foot of the page. **The builder weighs it; this page does not decide it.**

**STATUS: drafted BEFORE the `BBCAP3` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any `docs/prereg/BARS.tsv` row exists,
BEFORE any file named `scratchpad/overnight/BBCAP3*` exists, and BEFORE the
leg's first game.** Drafting session wall clock at write time
**`2026-08-17T12:58:09Z`** (`date -u`, same shell call); repo HEAD at draft
`cc64b800` (author time `2026-08-17T14:54:59+02:00`). Verified at draft:
`grep -c -i BBCAP3 scratchpad/corefill_work.txt` → **0**; same grep on
`docs/prereg/BARS.tsv` → **0**; on `results.tsv` → **0**; on
`scratchpad/fleet_queue.tsv` → **0**;
`ls scratchpad/overnight/ | grep -ic bbcap3` → **0 files**;
`ls docs/prereg/ | grep -ic bbcap3` → **0 files** at the moment this file was
opened for writing.

### LOCK, clock 2 (local shard)
Per the obligations doc's **2026-08-17T07:24:55Z addendum**, which replaced the
clock-2 boilerplate that eleven preregs had copied and that was not executable as
written. **PRIMARY:** the shard tape's own `# FIXTURE … start=` stamp
(`tools/overnight.sh:99` sets `START=$(date -u …)`, `:103` writes it to the tape
before the first game). Quote it verbatim beside the lock commit's git author
time. **BACKSTOP, if the tape carries no `# FIXTURE` line** (every REMOTE tape;
107 of 238 local tapes carry it): the tape's **FIRST COMPLETED ROW `ts`** —
conservative by construction, since the true start is strictly earlier, so the
substitution can only OVERSTATE the prereg-to-start gap (measured cost 1–2 s).
**SECOND BACKSTOP, serial runners:** the preceding shard's `COMPLETE` time on the
same worker bounds this start from below.
⛔ **NOT AVAILABLE: the heartbeat's `STARTING` line** — `overnight.sh:100` writes
it with `>` and every later state overwrites it. **State which clock was used.**
This shard is registered LOCAL / SAME-HOST, so the primary is expected to exist.

### COMMIT PROVENANCE OF THE TREATMENT TREE — TRACKED AND CLEAN AT DRAFT
`bots/_v503bbcap3/` is **tracked by git and clean**: `git ls-files
bots/_v503bbcap3` returns all four modules and `git status --porcelain` shows no
entry for it. It was added by **`54129ed7`** (author time
`2026-08-17T14:50:15+02:00`), the same commit that added `bots/_v504bbammo`.
⇒ **the OB13 intersection is COMPUTABLE for this arm** and
`prereg_check.py`'s `OB13_UNTRACKED_ARM` does not apply — the defect the
carrier's own page had to disclose is absent here.

---

## ⛔ READ BEFORE RATIFYING — NINE THINGS THE LANE OWNS

**1. ⛔⛔ THE ARM'S TREATMENT-OCCURRENCE EVIDENCE POINTS THE WRONG WAY ON TWO
INDEPENDENT BATTERIES, AND THE SECOND ONE TESTED EXACTLY THIS ARM ON EXACTLY
THIS CHASSIS. THIS IS THE WHOLE CASE FOR HOLDING.**

| battery | fixture | what it measured | direction |
|---|---|---|---|
| **CAP 2→3 on the `RND=25` PARENT** (`_v480beltbreak`) | pre-lock demo for `BELTBREAK2`, common seed set | shredders/game **1.358 → 1.358 = 0.000 movement**; median plant round moved the WRONG way 45→48; shots/shredder flat 22.4→21.9. Instrumented refusal counters, 30 games: **`CAP` 6.6×/game against `TI` 638×/game** | **FLAT** |
| ⭐ **CAP 2→3 + AMMO 24→36 on the `RND=10` CARRIER** (`_v488beltbreak2` — **this arm's exact mechanism on this arm's exact chassis**) | `_v502bbstack` per-leg ablation, **paired, NOISE_OFF, 50 games/arm, interleaved** | plants/game **1.34 vs the chassis's 1.54 — FEWER PLANTS, NOT MORE**. Composed with the ammo-floor leg: shots/shredder **6.0 vs 14.0** and total fires **−46%** | **NEGATIVE** |

**THE PRO-CASE HAD EXACTLY ONE DISTINGUISHING CLAIM AND THAT CLAIM HAS NOW BEEN
MEASURED DIRECTLY.** The argument for re-testing the cap was: *the parent's null
is explained by the nest — `TI → CAP → siting` — so the cap only binds AFTER
siting and timing improve, and the `RND=10` carrier is precisely that
improvement.* **That is a falsifiable prediction, and the stack's CAP-leg
ablation is its test: on the improved chassis, raising the cap produced FEWER
plants.** The claim is not weakened, it is contradicted on its own fixture.

⚠ **THE HONEST COUNTERWEIGHT, stated because a HOLD must not be built on the
strongest available reading of the negatives:** n=50 games/arm paired is a
DOSE-AND-MECHANISM probe, not a currency read; 1.34 vs 1.54 is roughly one plant
per seven games and the ablation's own arms are NOISE_OFF while the shard is
NOISE_ON; and the one cell where the cap looked healthy (**CAP + step, WITHOUT
the floor: 27.3 shots/shredder**) shows the cap is not intrinsically toxic — it is
toxic *in the compositions tried so far*, and BBCAP3 is a third composition
(cap + magazine, no floor, no step). **The negatives are directional, not
decisive. They are, however, TWO of them, and neither has a rival positive.**

**AND THIS REPO HAS A PRECEDENT FOR THE PROCEDURE, IN THE OBLIGATIONS DOC
ITSELF.** Addendum 4 (LOKI-3): *"built, gated, crash-free across 96 games — and
not going to battery. It failed its own pre-registered treatment-occurrence bar
measured BEFORE the battery."* Its own drift note: *"the stand-down is the
OPPOSITE of drift — a treatment-occurrence bar measured pre-battery, a null owned
as 'never dosed' rather than banked or buried. This is the template."* **BBCAP3's
treatment-occurrence evidence is not merely short of a bar; it is measured
NEGATIVE. The template says stand down and probe, not fire and hope.**

**2. ⛔⛔ THE REGISTERED PRIMARY IS ALMOST PRE-SATISFIED BY INHERITANCE, WHICH IS
OB7'S EXACT DEFECT, AND IT IS DISCLOSED HERE RATHER THAN DISCOVERED AFTER.**
The house bar is **51.33 vs `bots/_v468kladturbo`**. **The CARRIER this arm is
built on already measures 53.09 [51.76, 54.42] at n=5,400 against that same
control** (`results.tsv:beltbreak2-final`). ⇒ **the treatment inherits a share
whose CI LOWER BOUND already clears the bar, and the two constants would have to
be actively harmful by ~1.8pp for the primary to fail.** OB7: *"a prereg
predicting change on cells already changed cannot fail honestly."*
⇒ **REGISTERED CONSEQUENCE, pre-committed: clearing 51.33 on this arm is NOT
evidence about `CAP`/`AMMO`. It is evidence that the carrier still works.** The
DECISION-RELEVANT estimand is the **carrier contrast** — and it is registered
below as **DESCRIPTIVE with its own half-width**, because it is not resolvable at
this n:

```
this arm (n=5400) vs the carrier's own completed tape (n=5400)
two-fixture half-width, DEFF 0.98:
    1.96*sqrt(0.25*(0.98/5400 + 0.98/5400)) = +-1.8671pp
projected difference (see #3):  about -0.4pp, and NEGATIVE
=> the contrast this leg is FOR cannot be resolved by this leg
```
**A shard that resolves the question nobody is asking and cannot resolve the
question it was built for is the shape `target_value.py` exists to catch, one
surface over.**

**3. THE PROJECTION, DONE BEFORE THE FIRE, WITH ITS OWN MODEL'S CALIBRATION
ERROR QUOTED.** The carrier's page projected its share by scaling the parent's
excess linearly with the plant dose. **That device is checkable now: it projected
`50 + 2.90 × 1.287 = 53.73` and the carrier read `53.09` — it OVER-projected by
0.64pp.** Applying the same device to this arm's measured plant ratio
(`1.34 / 1.54 = 0.870`) on the carrier's excess:

```
50 + 3.09 x 0.870 = 52.69      (device output)
device's own known bias         -0.64pp when last checked
honest range                    ~51.5 to ~53.1
```
**Against the pinned floors, at those true shares** (`Z95` 1.96, DEFF 0.98,
prefix SEs 1.565pp at n=1000 and 0.953pp at n=2700; the two looks are NESTED so
treating them as independent UNDERSTATES survival — stated so the number is not
read as tighter than it is):

```
true share   P(prefix1000 < 52.0)   P(prefix2700 < 52.0)   P(reach n=5400)
   51.50            0.625                  0.700               ~0.112
   52.00            0.500                  0.500               ~0.250
   52.69            0.330                  0.234               ~0.513
   53.09            0.243                  0.126               ~0.661
```
⇒ **at the projected 52.69 this arm is roughly a coin flip to reach its own
registered n, and the outcome that ends it is the 52.0 TREND FLOOR, which is NOT
waived by any exemption.** **REGISTERED READING, pre-committed: a TREND-FLOOR@1000
or @2700 stop is an OPERATIONAL CANCELLATION and is NOT a refutation of the
cap-plus-magazine mechanism** — it says *this chassis-plus-plank total fell below
the floor on this prefix draw*, and a floor stop fires on a LOW PREFIX DRAW so
the arm's true share conditional on stopping is HIGHER than the number that
stopped it (~+2pp of expected regression; side lane s47, n=2 cases, a DIRECTION
with a rough size and not a calibrated correction).

**4. ⛔⛔ THE `AMMO` HALF OF THE "ONE MECHANISM" HAS FOUR READ SITES AND ONLY ONE
OF THEM PUSHES THE WAY THE BRIEF ASSUMES. THIS IS THE STRONGEST CODE-LEVEL
FINDING ON THE PAGE AND IT WAS FOUND BY READING THE TREE, NOT BY ARGUING.**
`LOKI_BELTBREAK_AMMO` is not a magazine the gunner draws from — the engine has no
physical ammo. It is a **threshold constant read in four places**, and raising it
24→36 moves three of them AGAINST the plank:

| site | what the constant does there | effect of 24→36 | direction |
|---|---|---|---|
| `main.py:384` | `ammo_target = max(ammo_target, LOKI_BELTBREAK_AMMO)` while a beltbreak heartbeat is fresh — the core converts Ti→ammo 1:1 up to that target | **+12 Ti converted into standing ammo** | ⭐ **the INTENDED effect** |
| `raid.py:904` | `need = gunner_cost; if live > 0: need += LOKI_BELTBREAK_TI_FLOOR + LOKI_BELTBREAK_AMMO` — the funding gate for the **2nd and 3rd** plant | **the Ti bar for plants 2..n rises from `cost+64` to `cost+76`** | ⛔ **STRICTER — fewer plants** |
| `main.py:1093` | `if ct.get_global_resources() < 10 + LOKI_BELTBREAK_AMMO: return` — the gate on a beltbreak gunner ROTATING onto a new target | **the rotation Ti gate rises 34 → 46** | ⛔ **STRICTER — fewer rotations** |
| `main.py:384` (second-order) | the converted Ti leaves the bank that `raid.py:904` then tests | **the raise pays for itself out of the same bank it raises the bar on** | ⛔ **compounding** |

⇒ **"FUND WHAT YOU ALLOW" IS NOT WHAT THIS EDIT DOES ON THIS CHASSIS. It funds
the magazine and simultaneously PRICES OUT the second and third plant** — and
**`TI` is 87–91% of ALL refusals on both measured fixtures** (six independent
confirmations, `docs/coordination.md`), i.e. the constant is being raised on the
one gate that actually binds. **This is a mechanism-level explanation for the
stack ablation's measured plant FALL (1.34 vs 1.54), arrived at independently of
it.** Two instruments, one story.

⚠ **AND THE AMMOFLOOR SWEEP PRICED THE INTENDED HALF AS A COST, NOT A FREE
GOOD** (2,897 games, 5 doses, paired 240 cells/arm): *"Ammo held 30.9→10.2 and
dry-turret rounds 26→181 monotone in reserve size; dose 3 DISQUALIFIED at −27.5pp
timely-kill [CI excludes 0]"*, and *"the kill constraint is turret THROUGHPUT,
not COUNT — dose 3 bought +7.8 turrets, lost 13.8 shots, and gave back −27.5pp.
The magazine was not overbidding; it was correctly priced ON THAT CHASSIS."*
⇒ **the sweep's own conclusion is that 24 may already be the right number, and
the sweep's re-brief for the stack says *"no `BELTBREAK_AMMO` in the reserve"* —
i.e. the direction the evidence points is to REMOVE the constant from
`raid.py:904`, not to raise it.** **This arm does the opposite of what the
sweep's re-brief specified, and the page says so.**

**5. THE CONTROL IS THE LIVE LADDER HOLDER'S BOT, SO THIS LOCAL SCREEN IS ALSO A
SCREEN AGAINST WHAT IS LIVE.** `bots/_v468kladturbo` is **Sleipnir v1**, pinned as
the corefill control at `scratchpad/CONTROL_PIN`. **Every share on this page
carries its control inline — `X% vs _v468kladturbo` — and that notation is
mandatory, not decorative:** three different 60s live in this repo and they differ
by ~9pp through the logistic. **50.0 vs `_v468kladturbo` means "adds nothing to
the bot we ship".** ⚠ The control is the SHIPPED BOT, not the CURRENT LADDER
HOLDER — x3r0's Odin holds the slot (`ODINVSSLEIP` measures that distance).

**6. ⛔ THE GATE WILL SCORE THIS ARM AS A COMBO, AND THE EXEMPTION IS MAGNUS'S TO
GRANT — THE BUILDER CARRIES HIS RULING, NEVER A SELF-GRANT.**
`tools/auto_gate.py:715 combo_of()` greps the `stack.py` compose marker off the
**TREATMENT** tree's own `doctrine.py`. **`bots/_v503bbcap3/doctrine.py:2085`
carries `# ---- composed by tools/stack.py from: turbo (_x3r0v152), bodyaware
(_v242bodyaware), samestop (_v464samestop)` — inherited from the control
(`bots/_v468kladturbo/doctrine.py:1879`), which every arm on this chassis
inherits.** ⇒ **`COMBO_BAR = 55.0` (`auto_gate.py:278`) would bind on the n=2700
prefix.**
⭐ **MAGNUS HAS ALREADY RULED THIS CLASS EXEMPT, TWICE, AND THE PRECEDENT ROWS ARE
ON THE TAPE:** `docs/prereg/BARS.tsv:310` (`BELTBREAK-EARLY` — *"GRANTED BY MAGNUS
DIRECTLY, 2026-08-17T08:30:36Z, on the builder's escalation"*) and
`docs/prereg/BARS.tsv:312` (`BELTBREAK2` — *"GRANTED BY MAGNUS DIRECTLY on the
builder's escalation, same ruling"*). Both record the same reasoning: a SOLO
plank on the incumbent chassis reads COMBO only because of a **CLASSIFICATION
DEFECT** in `combo_of()`, and Magnus pinned 55.0 for COMBINATIONS.
⛔ **INSTRUCTION TO THE BUILDER, and it is the part that matters: carry
`COMBO-BAR-EXEMPT` on the `BBCAP3` row with MAGNUS'S RULING as the grant, citing
`docs/prereg/BARS.tsv:310` and `:312` as the precedent — never self-granted.** The
token's registered purpose (`auto_gate.py:906-919`) is *a MECHANISM test scored
against its own additive prediction*, which a **PROSPECT** like this arm cannot
claim on its own authority; the precedent rows establish that the OWNER of the
bar has already ruled that solos on this chassis are not adjudicated by it.
⛔ **THE 52.0 TREND FLOOR IS NOT WAIVED and binds at both looks. Per #3 it is the
clause most likely to end this arm, and if the arm is genuinely weak it should.**

**7. ⛔ THE REGISTERED F1 IS NOT EXECUTABLE BY `tools/dose.py` AS THE BRIEF NAMES
IT, AND THE CARRIER'S OWN LEG IS WHY WE KNOW.** Full OB17 working in
`FIRINGS-BEFORE-PRIMARY`. In one line: **`tools/dose.py` has NO `--tle`
argument** (`argparse` block `:134-172`, checked) and **`:226-228` invokes
`fcode run … --seed … --replay …` with no `--tle`, so it runs at the engine
default `--tle 0` = LIMIT DISABLED (`run.py:119`) while the shard runs
`--tle 10`.** On the carrier this was decisive:
`results.tsv:beltbreak2-final` records *"F1 AS REGISTERED READ NO INFORMATION AT
0.98× OF ITS BAND … ON THE SHARD'S OWN FIXTURE the same registered n=60 reads
DOSE DELIVERED at 1.26×/1.45×, and the doctrine's quoted median 49.5→40
reproduces (49.0→40) — which it does NOT at tle=0."* ⇒ **registering the F1
invocation as a bare `dose.py` call would register a battery on a fixture the
shard does not run, and it would not fail — it would print the same verdict
vocabulary against a different population.** **LOCK BLOCKER: the builder either
adds `--tle` to `dose.py` (a one-line change this agent did not make) or fires
the explicit `--tle 10` loop registered in F1a. Either is fine; leaving the brief's
wording unresolved is not.**

**8. ⛔ ONE OF THE THREE F1 READS THE BRIEF ASKS FOR IS NOT EMITTED BY ANY SHIPPED
DECODER. Named, not silently renamed into something the tape happens to carry.**
`shots per shredder, including the THIRD shredder's shots` requires per-turret
shot attribution. **`tools/corpus/replay_events.py` emits BUILD and DEATH rows
ONLY (`:157` header `file ev rnd team kind x y d2_own d2_enemy mw mh`) — there is
no fire row at all.** **`tools/corpus/replay_econ.py` DOES decode `fireTurret`
(message 12) but its own docstring records the limit — *"shots, attributed by
POSITION (the message carries only {from,to} — no id, no team)"* — and it emits
`COLS` aggregated **per file × team × round-band** (`:131-132`), never a
per-position or per-entity row.** ⇒ **there is no shipped path from a shot to the
gunner that fired it, and therefore none to "the third shredder".** Registered
handling in F1c: the read is executable only via a **position-join** the builder
must write and validate BEFORE the lock, and its named hazard (a rebuild on the
same tile merges two gunners' shots) must be measured, not assumed away.
⭐ **This is the clause that could surprise the person running it, and it did.**

**9. ⛔ `fcode run` IS NOT SEED-REPRODUCIBLE FOR THIS CHASSIS, SO NO F1/F2 READ
MAY USE SEED-PAIRED LANGUAGE.** `results.tsv:beltbreak2-final`, banked: *"three
runs of antler seed 1 gave 45/106/74 event rows; cause is the unseeded
`random.Random()` spawn salt at `main.py:445` with `NOISE_ON=True` in both
trees … A re-run of an identical registered invocation can return a different
`DOSE_RESULT` (it nearly did)."* ⇒ **pairing controls map, seed and opponent —
never the salt.** Registered consequence: every firings read is quoted with its n
and its band, no read is re-run to a preferred answer, and a re-run that
disagrees is reported as dispersion rather than as a correction.

---

## RATIFY: Hypothesis

**HYPOTHESIS.** *Allowing a third live beltbreak shredder and sizing the magazine
constant to fund it — `LOKI_BELTBREAK_CAP` 2→3 **and** `LOKI_BELTBREAK_AMMO`
24→36, two constants that are ONE mechanism ("fund what you allow"), on the
otherwise byte-identical Band-1 carrier `bots/_v488beltbreak2` — converts into a
LOCAL pooled game share vs `bots/_v468kladturbo` of **51.33% or higher** at
n = 5,400 games across all 15 corefill maps and both seats, WITHOUT pushing our
own kill past r300.* Registered direction **POSITIVE**.

**⛔ AND THE HYPOTHESIS AS STATED IS THE WEAK FORM, BECAUSE #2 IS TRUE.** The
strong form — the one the leg exists to answer — is: *the third shredder and its
funding add share OVER THE CARRIER'S OWN 53.09%.* That form is registered as
**DESCRIPTIVE** with a **±1.87pp** half-width against a projected difference of
about **−0.4pp**, i.e. **unresolvable at this n and pointing the wrong way**.
**No readout sentence may present a clearance of 51.33 as an answer to the strong
form.**

**Provenance of the idea, verbatim (Magnus's directive that created this plank
family):** *"offensive gunner that shreds the enemy economy… a lot of the top
teams do this."* **Provenance of the narrowing (Magnus, s49, via the builder):**
the board was cut to ONE offensive plank (BELTBREAK) and ONE eco plank
(AMMOFLOOR), and this arm is the **LEG-1 isolation** of the four-rung attribution
ladder *carrier / +cap / +ammo / full stack* (`54129ed7`).

**The mechanism claim, stated so it can be wrong.** The plank plants a **GUNNER**
in the **d² 20-100 annulus of the ENEMY core**, aimed at a belt or harvester tile
that exists right now. `raid.py:889` refuses the plant when a **LIVE CENSUS** of
friendly annulus gunners (`_live_beltbreak_guns`) has reached
`LOKI_BELTBREAK_CAP`. **This arm changes NOTHING about siting, timing, targeting
or rotation policy — it changes only how many may stand at once, and the Ti/ammo
thresholds that decide whether the second and third get bought.** The claim is
therefore narrow and falsifiable in two independent places: **(a) a third live
annulus gunner must actually occur** (impossible in the carrier BY
CONSTRUCTION), and **(b) the third one must fire enough to matter** — a 20-HP
belt tile is 3 gunner shots = 12 ammo (study §6), so a third turret that plants
and cannot shoot is the failure the `AMMO` raise exists to prevent and the
failure the AMMOFLOOR sweep says raising a reserve tends to CAUSE.

**⇒ A FLAT OR NEGATIVE RESULT HERE IS INFORMATIVE ABOUT THE PLANK.** It prices
the cap axis DOWNWARD on the improved chassis, which is the one thing two prior
batteries have already suggested and nothing has yet contradicted. **That is the
HONEST-NULL clause and it is registered in `FALSIFIER`.**

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN`. There is no opponent churn to pin against and no calibration relevance to protect (CLAUDE.md's rule: pin treatment legs, never pin calibration panels — this is neither, it is self-play).**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe; (iii) a third candidate, **HOST**, is killed by REGISTRATION rather than by measurement: this shard is registered SAME-HOST (LOCAL by default), and the Addendum 11 rider (the 0.98 exemption is a WITHIN-HOST measurement) is why splitting it across hosts would require an amendment typed BEFORE the first row. All surviving clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit), i.e. **NAIVE intervals are correct and marginally conservative. The platform constants (1.529 rated / 1.833 unrated) are NOT applicable here and importing them would widen every interval on this page by 24-35% for correlation that has been measured absent.**
**ESTIMATOR: the unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Because the shard is exactly balanced on 15 maps × 2 seats × 180, the pooled share and the map-stratified equal-weight share coincide by construction; the stratified form is computed at readout as an **arithmetic consistency check only** and is not a second estimator (s28 ring-hold: four estimators inside 0.010 of one bar flipped MEET/MISS among themselves). Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never a bar — seat is worth ~7.6pp on byte-identical arms, which is why n is a multiple of 30. **Any estimate quoted at readout arrives from `tools/cluster_ci.py` (HEAD) so the interval and the point are produced by the same call; the pre-data half-widths on this page are closed-form Wald with DEFF 0.98 and their arithmetic is shown inline.**
**DOSE: ⛔ MEASURED NEGATIVE PRE-LOCK, AND THIS LINE IS THE ARM'S OWN CASE AGAINST ITSELF. Plants (shredders) per game 1.34 (treatment `CAP=3`/`AMMO=36`) vs 1.54 (the carrier chassis `CAP=2`/`AMMO=24`), `_v502bbstack` per-leg ablation, PAIRED, NOISE_OFF, **n=50 games per arm**, INTERLEAVED — a FALL of 13.0%, i.e. the opposite of the registered direction.** Composed with the ammo-floor leg the same mechanism collapsed shots/shredder **6.0 vs 14.0** with total fires **−46%** — the plants-up-shots-down trade the AMMOFLOOR sweep DISQUALIFIED at −27.5pp timely-kill. The prior battery on the `RND=25` parent read **0.000** movement in shredders/game with refusals `CAP` 6.6×/game against `TI` 638×/game. **BOTH EQUIVALENCE VERDICTS PRESENT (`54129ed7`): flag-off 0/16 games non-identical vs the carrier with restored constants, WITH flag-on positive controls on the same fixture at 8/16 and 16/16 differing** — the 0/16 alone is equally consistent with a harness that cannot see any difference; the positive controls are what make the zero mean something. ⇒ **THE WIRING IS SOUND AND THE DOSE DIRECTION IS WRONG. That is a different failure from the carrier's, and it is the one that argues for a probe rather than a shard.**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:68` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30). ⛔ **5400 IS SAID EXPLICITLY BECAUSE A SOLO SHARD OTHERWISE DEFAULTS TO A 2700 TARGET, and at 2700 the bar arithmetic below is unreachable** (margin 1.33pp against a half-width of ±1.87pp).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture and no accepts count is declared. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: the tape carries an unprefixed header line under the `# FIXTURE` line, so a naive `wc -l` over-reports n by exactly one (measured on KLADLADDER, `results.tsv:kladladder-n-final-correction`). The registered denominator is **DictReader row count over non-`#` lines, cross-checked against the heartbeat's `n TARGET` and against `max(game id) + 1`.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed rows this arm publishes descriptive tallies (share, per-seat, per-map, per-class, kill-round, `cond` mix) and takes **NO bar verdict**; the one-sample half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on, so a sub-2,700 read cannot resolve its own branches. An `auto_gate` firing at CATASTROPHE@400, MARK-1000, TREND-FLOOR@1000/2700 or COMBO-BAR@2700 is an **OPERATIONAL CANCELLATION, not a verdict**, typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400, i.e. a prefix below 40.15 at exactly n=400) is arithmetically INCOMPATIBLE with every band above Band 4, so a stop under that clause DOES license the Band-4 sentence at the partial n — **provided F1/F2 have been read first** and provided the partial share is disclosed as **selected-pessimistic** (a floor stop fires on a LOW PREFIX DRAW; expect roughly +2pp of regression, side lane s47, n=2 cases, a DIRECTION with a rough size and not a calibrated correction). ⛔ **NO OTHER CLAUSE'S CANCELLATION LICENSES ANY BAND — and per READ-BEFORE-RATIFYING #3 the TREND-FLOOR case is the likely one.**
**BAR: 51.33. MDE: 0.00pp — THIS BAR IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE** (OB16 corollary, 2026-08-15T03:52:45Z: the standard corefill band IS `50 ± half_width` at n = 5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes no positive effect size whatsoever). n for the one exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n. ⛔ **AND PER READ-BEFORE-RATIFYING #2 THIS BAR IS SATISFIED BY INHERITANCE FROM A CARRIER MEASURED AT 53.09 [51.76, 54.42], SO ITS CLEARANCE IS NOT EVIDENCE ABOUT THE TWO CONSTANTS.** **The r300 admission read below is the other bar on this page and it IS sized — see `KILL-ROUND NON-REGRESSION`.**
**BASE RATE: 50.00**
**BAR SOURCE:** the house-standard corefill futility band, `50 + 1.96*sqrt(0.98*0.25/5400) = 51.3202 -> 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADLADDER`, `SEALSENTAN`, `ROUTESCORE`, `BELTBREAK-EARLY`, `BELTBREAK-LATE` and **`BELTBREAK2` (`:312`, this arm's own carrier)**, which is what keeps this arm numerically comparable to the turret-family reads it extends. **Constructed, not observed.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own chassis base. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, same host and fixture (`results.tsv:idnull140-cert-5400`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it. ⇒ **a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced**, which is why Band 2 is pre-registered as WEAK. ⚠ **The two cells are 1.77pp apart**; the incremental effect this arm is FOR is projected at about **−0.4pp**, i.e. an order of magnitude inside the fixture's own byte-identical spread. **Disclosed before the data.**
**REFERENCE n: none registered as a BAR comparator** — the bar's comparator is a CONSTRUCTED null of 50.00 generated inside this same shard from its own 5,400 seeds; there is no external reference SAMPLE for the bar. ⛔ **AND THE CARRIER'S 53.09% IS EXPLICITLY NOT A REFERENCE SAMPLE FOR THE BAR.** Naming `BELTBREAK2`'s tape as a reference would make the checker size 51.33 as a two-fixture comparison at ±1.87pp and correctly FAIL it — a true statement about a bar nobody registered. **The carrier-vs-this-arm difference IS the decision-relevant estimand and it is registered as DESCRIPTIVE with its own arithmetic (±1.8671pp at 5,400 + 5,400, DEFF 0.98), never as the bar.** Any carrier-vs-child sentence at readout carries that half-width inline.
**TREATMENT TREE: bots/_v503bbcap3**
**TREATMENT DIFF REFS: 54129ed7^ 54129ed7**

That is the commit which added the tree (author time `2026-08-17T14:50:15+02:00`), and the refs line above carries NOTHING BUT THE REFS on purpose — `tools/prereg_check.py:1546-1550` feeds the whole field value to `git diff --name-only` by `split()`, so a prose tail on that line makes the OB13 intersection read CANNOT-COMPUTE and renders identically to "checked and clean". Run at draft: `git diff --name-only 54129ed7^ 54129ed7` returns 8 `.py` paths — the four under `bots/_v503bbcap3/` and the four under `bots/_v504bbammo/` (the sibling LEG-3 arm added by the same commit). **The executable diff of record for THIS arm is the tree-vs-tree diff reproduced verbatim in `THE CHANGE`, and it is git-checkable because the tree is tracked and clean.**
**MECHANISM METRIC READS: bots/_v503bbcap3/raid.py:889 — the live-census cap gate `if live >= LOKI_BELTBREAK_CAP: return self._bb_refuse("CAP")` — and bots/_v503bbcap3/raid.py:904, main.py:384, main.py:1093 for the AMMO constant's three further read sites (READ-BEFORE-RATIFYING #4). TREATMENT DIFF TOUCHES: bots/_v503bbcap3/doctrine.py. INTERSECTION: yes — by IMPORT BINDING, which is the honest form: `raid.py:64` and `main.py:35` are both `from doctrine import *`, so the names `LOKI_BELTBREAK_CAP` and `LOKI_BELTBREAK_AMMO` read at those four sites bind to the TWO lines the diff changes (`doctrine.py:1445` and `:1453`).** ⚠ **A path-only intersection would ALSO pass here for a trivial reason — the whole tree is new in `54129ed7`, so every file "appears in the diff" — and that reading is REFUSED on this page: `raid.py`, `main.py` and `eco.py` are BYTE-IDENTICAL to the carrier's (`cmp` clean on all three, verified at draft), so the only thing that can make these metrics read differently between arms is the two imported constants. **The metrics therefore CANNOT read identically in the two arms, which is the LOKI-18 failure this obligation exists for.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_BELTBREAK_CAP=3, LOKI_BELTBREAK_AMMO=36, LOKI_BELTBREAK_RND=10, LOKI_BELTBREAK_LATE_RND=70, LOKI_BELTBREAK_MIN_HARV=1, LOKI_BELTBREAK_DSQ_LO=20, LOKI_BELTBREAK_DSQ_HI=100, LOKI_BELTBREAK_MAX_ROT=1, LOKI_BELTBREAK_STALE=3, LOKI_BELTBREAK_TI_FLOOR=40, LOKI_BELTBREAK_MAX_TGT=12. MECHANISM CAN OCCUR IN WINDOW: yes** — **exactly ONE of these is a round gate**, `LOKI_BELTBREAK_RND = 10`, inherited UNCHANGED from the carrier, and it is an OPENING round that never closes (`raid.py:882-884` refuses while `rnd < 10`; `LOKI_BELTBREAK_LATE_RND = 70` is INERT because `LOKI_BELTBREAK_EARLY = True` selects the other branch of the ternary — declared anyway, because an undeclared constant is the failure OB17 exists for). **Neither manipulated constant is a round gate:** `CAP` is a live-census count and `AMMO` is a titanium/ammo threshold. ⇒ **the mechanism's window is r10-r1000, inside the declared r0-r1000, and a THIRD plant can occur at any round from r10 on because the cap is a LIVE CENSUS, so rubble cannot close this arm.** ⭐ **AND THE `CAP=3` SEMANTICS ARE A CEILING, NOT A TARGET:** the carrier's measured 1.44-1.54 plants/game means the third slot is reachable only in the minority of games that already field two, so the manipulated constant is expected to bite in a SUBSET of games — which is exactly why F1 and F2 are HARD-SEQUENCED before the primary.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` will emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE ARTEFACTS OF THE CHECKER.** Its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a harvester count of 1 and a live-gunner cap of 3 render as "rounds r0-r2 cannot contain the mechanism". The constants are declared anyway.
**PLANK CLASS: OFFENSIVE — an economy-denial weapon (forward GUNNERs planted in the enemy's belt, aimed at conveyors and harvesters), not a defensive turret and not a home screen.** ⭐ **AND THE r300 ADMISSION READ IS REGISTERED ANYWAY, NOT CLAIMED AS INAPPLICABLE, because this arm has TWO named arithmetic mechanisms for slowing our own kill.** (a) **SCALE DRAG:** cost scale is ONE GLOBAL ADDITIVE team factor and a gunner is **+20%** (`CLAUDE.md`, engine-confirmed s26, `bots/_probe_scale`); a third live shredder adds a permanent contribution that inflates every later harvester, conveyor and turret. (b) ⭐ **THROUGHPUT STARVATION, which is the bigger one and is MEASURED on a neighbouring fixture:** the AMMOFLOOR sweep found **dry-turret rounds 26→181 monotone in reserve size** and disqualified its dose 3 at **−27.5pp timely-kill**, concluding *"the kill constraint is turret THROUGHPUT, not COUNT"*; the stack ablation reproduced the shape on this arm's own mechanism (**shots/shredder 6.0 vs 14.0, fires −46%** in the CAP+floor cell). **A plank with a measured kill-delay mechanism carries a kill-delay bar whatever its class label.** Registering it is strictly stricter than the programme requires and cannot function as a second chance to pass: **both the share bar and the r300 bar must hold.**
**KILL-ROUND NON-REGRESSION: ITT RMST₃₀₀ is the operational estimator (PROGRAMME.md's 2026-08-16T05:36:10Z arbitration, whose vintage rule makes it binding on preregs locked from that date — this one is) — mean kill time censored at the r300 horizon over ALL games, a non-kill scoring 300, computed per side on the same rows; the bar is scored as an EXCLUSION: the 95% CI UPPER bound on (treatment RMST₃₀₀ − control RMST₃₀₀) must EXCLUDE +5.0 rounds (MDE +5.0 rounds; paired sd on the parent's tape is 88.99 rounds ⇒ half-width ±2.3736 at n=5,400, so the exclusion resolves). SECOND REGISTERED FORM, both required: the ITT timely-kill-by-r300 rate (share of ALL games ending `cond == core_destroyed` with `turns <= 300`, denominator every game played, per side) — its 95% CI LOWER bound on (treatment − control) must EXCLUDE a fall of 3.0pp (MDE 3.0pp; paired sd 75.28pp ⇒ half-width ±2.0079pp at n=5,400). THIRD, and it is a DIAGNOSTIC ONLY because it carries a collider: the kill-win-CONDITIONED share plus the conditioned median — reported beside the two bars, never as either of them. Median kill round crossing 300 is the gross backstop.**
⛔ **AND THE r300 BAR IS SUBJECT TO THE SAME INHERITANCE PROBLEM AS THE SHARE BAR, DISCLOSED HERE RATHER THAN AT READOUT: the CARRIER already beats the control on ITT timely-kill by +6.45pp (30.80 [29.56,32.03] vs 24.35 [23.21,25.50], NON-OVERLAPPING, `results.tsv:beltbreak2-final`).** ⇒ a non-regression against `_v468kladturbo` will very likely pass **by inheritance**, and the throughput hazard would have to eat the whole 6.45pp to trip it. **The DECISION-RELEVANT throughput read is against the CARRIER's tape and it is DESCRIPTIVE: two-shard RMST₃₀₀ half-width (sd 88.99 each, 5,400 + 5,400) is ±3.3567 rounds, and the timely-kill difference carries ±1.8671pp. Both are reported with those half-widths inline and neither is a bar.** Per the exclusion-restatement rule, no fail-to-exclude on this page may be quoted as a null without first being restated as the exclusion it is not.
**PRE-STATE: the predicted-change behaviour is NOT already in the target state at lock.** Verified at draft on the code, both comparisons. Against the CONTROL: `grep -c 'BELTBREAK\|_bb_\|beltbreak' bots/_v468kladturbo/{doctrine,eco,main,raid}.py` → the control has **no beltbreak path at all**, so the whole plank is absent. Against the CARRIER, which is the comparison that matters for an increment: **`raid.py:889` refuses every plant once `live >= 2`, so a THIRD simultaneously-live annulus gunner is IMPOSSIBLE in the carrier BY CONSTRUCTION and is reachable in this arm.** ⇒ the behaviour this leg predicts to change cannot already be in the target state on either comparison. ⚠ **AND THE OUTCOME CLAIM IS THE ONE THAT IS PARTLY PRE-SATISFIED — see READ-BEFORE-RATIFYING #2. That is disclosed as a DEFECT of this registration, not defended.**
**MAP SEGMENT: plank-EXPRESSIBLE maps — the 12 of 15 excluding `antler`, `fjordgate` and `royale` — mechanism reason: on small maps the d²20-100 annulus of the ENEMY core overlaps our own hunt band (`HUNT_BAND_DSQ = 41` of OUR core), so no tile satisfies both clauses of the siting predicate and ZERO shredders are planted in EITHER arm; a cap on a thing that is never planted is inert by construction — EXPECTED DIRECTION POSITIVE on the segment, EXACTLY ZERO on its complement.** This is ONE primary segment. The `CQ`/`STD`/`GRAND` split (`tools/overnight_read.py:76-94 map_area_class`, run at draft: **antler CQ, fjordgate CQ, royale STD**, the other twelve STD/GRAND) and the per-map table are **DESCRIPTIVE ONLY** and carry no pre-registered direction. ⚠ **`royale` is in the complement on OUTCOME EVIDENCE, not on area class, and that is stated plainly:** by `map_area_class` royale is STD, and the carrier's page deliberately kept it in the expressible segment for that reason. **It is moved here because BOTH parent tapes have since reproduced parity on it independently** — `BELTBREAK-EARLY` royale 50.56 [45.38,55.74] and `BELTBREAK2` royale 50.28, both containing 50, alongside near-zero measured dose. ⇒ **the three-map complement is now a REPLICATED prediction rather than a re-chosen one, and moving royale makes the segment ceiling STRICTER, not looser** (0.8000 vs 0.8667), which is the direction that cannot flatter the arm.
**EXPECTED DIRECTION: POSITIVE on the plank-expressible segment (12 maps), and EXACTLY ZERO — A/A — on its complement (antler, fjordgate, royale).**
**SEGMENT VALUE CEILING: 80.00% × 1.66pp on-segment effect = 1.33pp pooled** — the share is the segment's pairing weight (the twelve expressible maps of fifteen in a balanced shard) and 1.66pp is the on-segment effect the pooled bar's own margin requires. ⇒ **the dilution is a HARD CAP: no on-segment effect can pool at more than 0.8000× itself.** *(The conservative variant runs the other way and is recorded so a later reader can price it without re-choosing anything: keeping royale expressible gives a 0.8667 weight and needs only 1.54pp on-segment.)*
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68`, enumerated at draft via `tools/overnight_read.py live_pool()`: antler, archipelago, auroraveil, drakkarfjord, drumlin, fjordgate, frostgate, glacierkeep, icefloe, midgard, nordkap, ragnarok, royale, valkyrie, yulerune. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.)
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: three gates, sized separately.**
* **(a) THE SHARE BAR.** Margin 1.33pp against a one-sample half-width of ±1.3202pp at n=5,400, DEFF 0.98 — resolvable, and only just. ⚠ **The slack is 0.01pp, which is `GUNAXABL`'s exact failure mode: that arm missed its keep edge by 0.0152pp — ONE GAME.** Registered consequence: **a result within one game of the bar is reported as "the fixture cannot resolve the question", not as a verdict in whichever direction the rounding falls.** ⛔ **AND PER #2, THIS GATE DOES NOT DISCRIMINATE THE ARM'S OWN HYPOTHESIS — it discriminates "carrier still works" from "carrier plus these constants is ~2pp worse than the carrier". The gate's registered resolution statement is therefore: it resolves the CHASSIS TOTAL, and it CANNOT resolve the increment. An unresolved gate defaults to the RESTRICTION (OB12).**
* **(b) THE r300 ADMISSION BAR.** RMST₃₀₀: MDE +5.0 rounds against half-width ±2.3736 → resolves. Timely-kill: MDE 3.0pp against ±2.0079pp → resolves. Both branches separated by construction — **against the CONTROL. Against the CARRIER neither resolves (±3.36 rounds / ±1.87pp), and that is declared, not discovered.**
* **(c) THE OPERATIONAL FLOORS.** The pinned `tools/auto_gate.py` marks CATASTROPHE@400 (CI-hi < 45.0, `:244,247` — a prefix below 40.15 at n=400), MARK-1000 / TREND-FLOOR@1000 and @2700 (prefix < 52.0, `:261`), COMBO-BAR@2700 (prefix < 55.0, `:278`, exempt per #6 on MAGNUS'S ruling) and the CI rule at MARK-2700 — all Magnus's confirmed constants. Their firings are **OPERATIONAL CANCELLATIONS** that free a core, typed `cancellation`, never `verdict`, licensing no exclusion claim beyond the CATASTROPHE carve-out in CUT-SHORT. **The floors bind REMOTE too (`a50f27ef`, s48, via `tools/remote_cancel.py`), so the binding registration is SAME HOST — one host, LOCAL by default; moving it is an amendment typed BEFORE the first row.** ⛔ **AND (c) IS THE GATE MOST LIKELY TO DECIDE THIS ARM'S FATE: at the projected 52.69 true share, P(reaching n=5,400) ≈ 0.51, and the clause that ends it is the 52.0 TREND FLOOR, which no exemption waives.**
**Everything else on this page (F1a/b/c, F2, D3, D4, the seat / map / class splits, every carrier contrast) is DIAGNOSTIC and cannot rescue a failed bar. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## THE EVIDENCE BASE — BOTH SIDES, ON ONE PAGE

**⛔ THIS SECTION IS BANKED MECHANISM EVIDENCE FROM OTHER FIXTURES. IT CONTAINS NO
OUTCOME NUMBER FOR THIS ARM AND MAY NOT BE USED AS ONE.**

### FOR — why the cap was worth a second look at all

* ⭐ **`BBSTEP` MEASURED 132% SUBSTITUTION AT `CAP = 2`, WHICH IS THE POSITIVE
  CASE AND IT IS A REAL MEASUREMENT.** The step arm's phase-0 plants FELL by
  almost exactly the step's own plants — *"132% substitution — because
  `LOKI_BELTBREAK_CAP = 2` makes the marginal plant a RE-TIMED plant, not an
  extra one (R_CAP refusals 2,354→2,859 while plants fell)"*. ⇒ **at `CAP=2` an
  improvement in siting converts into re-timing rather than into volume, and the
  ceiling on the current constants is ~0.06 extra plants/game after
  substitution.** That is a genuine argument that the cap is a real constraint
  once siting improves.
* **THE MEASURED CONSTRAINT NEST IS `TI → CAP → siting`**, derived by putting two
  nulls together rather than by assertion: *"raising CAP 2→3 alone moved
  shredders 0.000 (TI binds first, refusals CAP 6.6 vs TI 638); the step alone
  moves 0.06 (CAP binds the moment siting improves)."*
* **THE CARRIER IS A REAL BAND-1 RESULT AND THIS ARM INHERITS IT.**
  `results.tsv:beltbreak2-final`: **53.09 [51.76, 54.42] at n=5,400** vs
  `_v468kladturbo`, ITT timely-kill **+6.45pp NON-OVERLAPPING**, with the
  mechanism complement reproducing on all three inexpressible maps. **The chassis
  under this arm is the best-measured offensive plank on the board.**
* **THE MAGAZINE ARITHMETIC IS SOUND AS ARITHMETIC.** A 20-HP belt tile is 3
  gunner shots = 12 ammo (study §6). `AMMO = 24` is two kill cycles, i.e. one per
  gunner at `CAP=2`; a third gunner under an unchanged 24 gets ~8 ammo = 2 shots,
  **less than the 3 a belt tile needs.** *If* the third gunner plants, funding it
  is not optional. **The question this page cannot answer favourably is whether
  raising the threshold is the way to fund it — see AGAINST.**

### AGAINST — and it is now two independent negatives plus a code reading

* ⛔ **CAP 2→3 ON THE `RND=25` PARENT: shredders/game 0.000 movement**, median
  plant round the wrong way (45→48), shots/shredder flat (22.4→21.9), and a
  permanent **+20% on the ONE GLOBAL ADDITIVE cost-scale factor** per extra
  gunner as the price. *(This is the negative the pro-case explains away via the
  nest; it is listed because the explanation is now itself under test.)*
* ⛔⛔ **CAP 2→3 + AMMO 24→36 ON THE `RND=10` CARRIER — THIS ARM'S EXACT
  MECHANISM, THIS ARM'S EXACT CHASSIS: plants/game 1.34 vs 1.54. FEWER PLANTS.**
  `_v502bbstack` per-leg ablation, paired, NOISE_OFF, 50 games/arm, interleaved.
  **The pro-case's one distinguishing prediction — "the cap binds once timing
  improves" — has been measured on the improved chassis and it went the other
  way.**
* ⛔ **AND COMPOSED WITH THE AMMO-FLOOR LEG IT COLLAPSES THROUGHPUT: shots per
  shredder 6.0 vs 14.0, total fires −46%** — *"the exact plants-up-shots-down
  trade the AMMOFLOOR sweep disqualified"*. The only healthy cell was **CAP +
  step, WITHOUT the floor (27.3 shots/shredder), which is not this arm.**
* ⛔ **THE AMMOFLOOR SWEEP SAYS EVERY EXTRA TITANIUM OF STANDING RESERVE IS PAID
  IN SHOTS, AND THAT COST CURVE REPLICATES WHERE THE GAIN CURVE DOES NOT**
  (2,897 games, 5 doses, paired 240 cells/arm): *"Ammo held 30.9→10.2 and
  dry-turret rounds 26→181 monotone in reserve size; dose 3 DISQUALIFIED at
  −27.5pp timely-kill [CI excludes 0] … Dose 4's turret gain (+4.33) vanishes in
  NOISE_ON (+0.47); its magazine cost (−5.6 ammo) replicates in both. Shipped
  dose selected by MINIMISING A MEASURED COST, not maximising a measured gain."*
  ⇒ **the `AMMO 24→36` raise MUST be checked for magazine cost — dry-turret
  rounds — and may not be assumed free.** It is registered as F1c and as the r300
  bar's named hazard.
* ⛔⛔ **AND THE CODE READING (READ-BEFORE-RATIFYING #4): three of the `AMMO`
  constant's four read sites push AGAINST the plank.** `raid.py:904` raises the
  Ti bar for plants 2..n by 12; `main.py:1093` raises the rotation Ti gate 34→46;
  the conversion at `main.py:384` spends the same bank those gates then test.
  **`TI` is 87-91% of ALL refusals on both fixtures — the raise lands on the one
  constraint that binds.** ⇒ **there is a mechanism for the measured plant fall,
  and it is in the arm's own diff.**
* ⚠ **A REFUSAL COUNTER NAMES THE RUNG THAT FIRED, NOT THE CONSTRAINT THAT
  BINDS** (the stack's funnel finding): *"L0+L3 read CAP refusals 10.4×/game yet
  raising the cap bought nothing — 2.20→2.04."* ⇒ **registered caveat on F1b: a
  rising `R_CAP` count is NOT evidence that the cap was binding, and a falling
  one is not evidence that it was not.** This caveat is attached to the counter
  wherever it is quoted.

---

## SEGMENT AND POPULATION — the split, its n, and the dilution arithmetic

**Registered per-class n at the planned 5,400** (classes from
`tools/overnight_read.py:76-94 map_area_class`, computed at draft from each map's
own `.map26` header, never a hardcoded size table):

| cell | maps | **n** | half-width at DEFF 0.98 | status |
|---|---|---:|---|---|
| **PRIMARY SEGMENT** (expressible, 12 maps) | all but antler, fjordgate, royale | **4,320** | **±1.476pp** | the one cell carrying a registered direction |
| **COMPLEMENT** (inexpressible, 3 maps) | antler, fjordgate, royale | **1,080** | ±2.952pp | registered prediction: **A/A, ~50%** |
| **CQ** (area ≤ 260) | antler, fjordgate | 720 | ±3.616pp | DESCRIPTIVE |
| **STD** (261-676) | archipelago, auroraveil, drumlin, frostgate, icefloe, nordkap, royale, yulerune | 2,880 | ±1.808pp | DESCRIPTIVE |
| **GRAND** (> 676) | drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie | 1,800 | ±2.286pp | DESCRIPTIVE |

**⇒ EVERY size class is pre-labelled DESCRIPTIVE: none of the three can resolve
the 1.33pp margin the pooled bar is built on.** Only the pooled read (±1.320) and
the primary segment (±1.476, marginal) can, and the primary segment's own margin
would have to be 1.66pp or better to clear the diluted bar.

**THE DILUTION ARITHMETIC, written out because it is a HARD CAP and not a
caveat.** Three of fifteen maps are A/A by construction (the plank plants nothing
in either arm, so a cap on it is inert). A balanced shard gives them
**3/15 = 20.00% of all games**, so:

```
pooled_effect  =  0.8000 x on_segment_effect
=> to clear the pooled bar (needs +1.33pp over 50):  on-segment >= 1.66pp
=> and the CEILING: no on-segment effect can pool above 0.8000x itself
```

⭐ **THE COMPLEMENT IS THE FALSIFIABLE HALF AND IT HAS ALREADY REPLICATED TWICE,
ON TWO TAPES THAT ARE NOT THIS ARM'S DATA:**

| map | `BELTBREAK-EARLY` (n=3,053→5,400) | `BELTBREAK2` (n=5,400) | registered prediction here |
|---|---|---|---|
| antler | 52.21 [47.06, 57.36] | 47.78 | ~50, CI contains 50 |
| fjordgate | 48.33 [43.17, 53.50] | 51.67 | ~50, CI contains 50 |
| royale | 50.56 [45.38, 55.74] | 50.28 | ~50, CI contains 50 |
| **expressible set** | **54.68 [53.19, 56.16]** (12 maps) | **53.89 [52.40, 55.38]** (12 maps) | POSITIVE |

**Present exactly where the plank can fire, absent exactly where it cannot, on
two independent shards. That is the shape a real mechanism makes.** ⚠ **The
individual complement cells are underpowered (±2.95pp pooled, ±5pp per map) — the
argument rests on all three pointing at parity TOGETHER, never on any one of
them.** ⚠ **And the segment was chosen using the parents' data, so it is a
PRIOR-INFORMED segment; the prediction it makes about THIS arm's 5,400 rows is
out-of-sample, which is what OB15c requires. The choice itself is not.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on this arm's pooled
share vs `bots/_v468kladturbo` falls BELOW 51.33.** That excludes the arm's own
bar. ⛔ **Read with READ-BEFORE-RATIFYING #2: because the carrier already reads
51.76 at its CI lower edge, this falsifier fires only if the two constants cost
roughly 2pp or more. It is a strong-harm detector, not a null detector.**

**SECOND FALSIFIER (the r300 admission bar, and it can fail on its own while the
share passes):** the 95% CI UPPER bound on (treatment − control) ITT RMST₃₀₀
fails to EXCLUDE +5.0 rounds, **or** the CI LOWER bound on the ITT
timely-kill-by-r300 difference fails to EXCLUDE a fall of 3.0pp. **Either failure
is disqualifying on its own, regardless of the share** — `PLAY_DEFENCE:
not_at_the_kill_s_expense`, and this arm's throughput-starvation mechanism is why
the bar is carried on an offensive plank. Anchors quoted as anchors and NOT as
this arm's prediction: the carrier's ITT timely-kill **30.80 [29.56, 32.03] vs
control 24.35 [23.21, 25.50]**, +6.45pp non-overlapping; the parent's RMST₃₀₀
paired sd 88.99 rounds.

**SEGMENT FALSIFIER (the complement, and it is a clause that can surprise the
person running it):** **antler, fjordgate and royale must read ~50% vs
`bots/_v468kladturbo`** — the mechanism says the plank plants nothing there in
either arm, so a CAP on it is inert. **If any complement cell moves materially
away from 50 (outside its own per-map ±5pp band, or the pooled complement outside
±2.95pp), the mechanism story is refuted even if the pooled bar clears:** either
the plank is expressible there after all — in which case the dose measurement is
wrong — or something other than the plank is moving share, in which case the
attribution is wrong. **Registered handling: a pooled clearance with a moving
complement is reported as ATTRIBUTION UNRESOLVED and promotes nothing.**

**MECHANISM FALSIFIER (independent of all of the above, and it fires FIRST):**
* **F2 IS THE WIRING CHECK AND IT IS THE ONE THIS ARM IS MOST EXPOSED TO.** If
  **no game in the treatment's F1 battery ever holds THREE simultaneously-live
  annulus gunners**, then the manipulated `CAP` had **no runtime effect** and the
  shard ran two behaviourally-identical bots on that axis. **A share near the
  carrier's with an empty three-live cell is a WIRING NULL, not a finding about
  the cap.** *(Not hypothetical: s47's delta D2 records a wiring null escaping
  demos to a 436-game shard.)*
* **If F1a shows the treatment's plants/game are BELOW the carrier's outside the
  band** — the direction the stack ablation already measured — **the dose was
  delivered in the WRONG DIRECTION.** ⛔ **THIS IS NOT "not measured": it is a
  measured negative dose, and the primary is then a read of a plank that
  SUPPRESSES its own mechanism.** Registered reading: **`DOSE INVERTED`**, and
  the share is interpreted as pricing the funding-gate side effect of #4, not the
  cap.
* **If F1c shows shots/shredder FALLING** (the AMMOFLOOR cost curve reproducing
  on this chassis), the magazine raise is being paid in dry-turret rounds and the
  r300 bar is the place that shows up. **A fall here with a flat share is the
  "expensive ornament" reading and is bankable.**
* **If F1c shows shots/shredder HOLDING while plants rise**, that is the
  **plants-up-shots-flat crossing** the stack's LEG-3 brief names as the
  mandatory read, and it is the one outcome that would revive this axis.
Per FIRINGS-BEFORE-PRIMARY all of F1a/F1b/F1c and F2 are read BEFORE the primary
is typed.

### ⭐ THE HONEST-NULL CLAUSE — pre-committed, because this null would be genuinely informative

**THREE null states, and they are NOT the same finding. The registered
discriminator is F1+F2, and it is read before the share.**

| state | evidence | pre-committed reading |
|---|---|---|
| **THE CAP NEVER OPENED** | F2 shows no game with three simultaneously-live annulus gunners | **NOT MEASURED.** The leg says nothing about the cap. The defect is that the third slot is unreachable at this funding level, the road stays open, and the repair is a probe, not a verdict. |
| ⛔ **THE DOSE LANDED INVERTED** | F1a below the carrier outside the band, F2 shows the third slot occasionally reached | ⭐ **A REAL FINDING, AND IT IS THE MOST LIKELY ONE: raising the magazine constant to fund the third plant PRICES OUT the second and third plant, because `LOKI_BELTBREAK_AMMO` is a term in `raid.py:904`'s funding gate and `TI` is 87-91% of all refusals.** This prices "fund what you allow" as MISWIRED on this chassis and names the fix: **remove `LOKI_BELTBREAK_AMMO` from the reserve** (which is what the AMMOFLOOR sweep's own re-brief specified) rather than raise it. **Bankable, cheap to confirm, and it closes a road.** |
| **THE DOSE LANDED AND DID NOT PAY** | F1a above the carrier outside the band, F2 populated, share flat or negative vs the carrier | ⭐ **A REAL FINDING ABOUT THE PLANK: the third shredder is worth less than the scale tail and magazine it buys.** This prices the cap axis DOWNWARD on the improved chassis, i.e. **`CAP=2` is at or past the optimum and the nest ordering `TI → CAP → siting` is wrong at this dose** — a genuine surprise against the FOR case and one that must be written down before it is explained away. ⚠ **Attribution bound: it does NOT separate "the third shredder is low-value" from "the third shredder is fine and the magazine/scale tail eats it".** Naming which requires a magazine-neutral CAP-only arm, which this leg is not. |

**⛔ A NULL HERE IS INFORMATIVE, AND THAT IS EXACTLY WHY IT SHOULD BE BOUGHT WITH
A PROBE RATHER THAN WITH 5,400 GAMES.** All three rows above are decided by F1/F2
— a **60-game paired battery at the shard's own fixture** — and none of them
needs the shard. **The shard adds only the share number, and per #2 the share
number cannot answer the arm's question.** See `DRAFT DISPOSITION`.

---

## READING, PRE-COMMITTED

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first
row whose condition holds is the reading. Rows are disjoint by construction.**
**Every band below is CONDITIONAL on F1a/F1b/F1c/F2 having been read first and on
the r300 admission bar having HELD; an r300 failure overrides every row and the
reading is `OFF-PROGRAMME — kill delayed`, whatever the share.**
**And every band carries its CARRIER CONTRAST inline at ±1.8671pp, because a band
quoted against `_v468kladturbo` alone is a statement about the chassis.**

| # | band on this arm's pooled share vs `bots/_v468kladturbo` at n = 5,400 | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33 AND the point is at or above the carrier's 53.09** | **THE CAP-PLUS-MAGAZINE MAY ADD.** ⚠ Even here the increment is UNRESOLVED (±1.87pp against a difference of ≤2pp): the licensed sentence is *"we can exclude 50 and 51.33 vs `_v468kladturbo`, and we cannot distinguish this arm from its carrier"*. Promotes to a combination input and to a separately-registered CAP-only-vs-carrier probe — **not to a ship conversation.** OB16: MDE 0, no minimum effect size may be claimed. |
| **2** | **CI lower ≥ 51.33 but the point is BELOW the carrier's 53.09** | **THE CARRIER STILL WORKS AND THE CONSTANTS ARE NOT SHOWN TO HELP.** Pre-registered as the MODAL BAND if the arm completes. The two constants are **DROPPED from the carrier** unless F1c shows the plants-up-shots-flat crossing. Rows are KEPT as a combination input for the carrier, not for the constants. |
| **3** | **point ≥ 51.33 but CI lower < 51.33** | **REAL-BUT-SMALL / UNRESOLVED, COMBINATION INPUT ONLY.** Pre-registered as WEAK: `NULL125`'s byte-identical A/A read 51.04, and the two A/A cells are 1.77pp apart. No ship conversation; a replication on fresh seeds, same host, is the price of promoting anything. |
| **4** | **point < 51.33 AND CI contains 50.0** | **THE CONSTANTS SUBTRACT ENOUGH TO ERASE THE CARRIER'S MEASURED GAIN.** Given the carrier's 53.09 [51.76, 54.42], landing here is a **≥3pp fall** and is a strong negative on the increment even though the bar language is "parity". **REGISTERED CONSEQUENCE: `CAP=3` + `AMMO=36` dies as a carrier candidate, and the named suspect is `raid.py:904` — the funding gate the magazine raise tightens.** |
| **5** | **CI upper < 50.0** | **ACTIVELY HARMFUL.** Attribution bounded: this refutes *the third-shredder slot plus its 12-Ti funding raise on the `RND=10` carrier*, **not** *the beltbreak plank* (whose own arms measured 53.81 and 53.09 vs the same control) and **not** *forward gunners in general*. **No further cap-raising arm is written on this chassis.** |

⚠ **Nothing here treats 50.0 as a floor, and nothing here treats the carrier's
53.09 as one either.** A share below either is a live outcome with named
mechanisms (a +20% scale contribution per extra gunner; 12 more Ti of standing
ammo reserve paid in dry-turret rounds; a 12-Ti-stricter funding gate on the
plants the cap was raised to permit; a 12-Ti-stricter rotation gate) and each is
pre-named so a negative is not explained away as noise.

⛔ **AND TWO CROSS-BAND NOTES, registered so they are not improvised.** (i) **A
TREND-FLOOR@1000/@2700 cancellation reaches NONE of these rows** — it is an
operational stop on the chassis total and the reading is
`CANCELLED — prefix below the 52.0 floor; the CAP/AMMO increment is UNRESOLVED
and defaults to the RESTRICTION`. (ii) **A COMBO-BAR@2700 firing would be an
INSTRUMENT ALARM, not a result** — Magnus's exemption per #6 should prevent it;
if it fires anyway the citation did not resolve and the builder repairs the row
rather than reading the stop.

---

## FIRINGS-BEFORE-PRIMARY — the reads, with exact invocations

**Measurability is declared per read. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape happens
to carry.** ⛔ **NOTHING BELOW READS OUR OWN `print()` OUTPUT.** Platform replays
strip `stdout` (30,664 of 30,664 events, `CLAUDE.md`); every quantity below is an
engine-side event off a LOCAL replay, or the LOCAL shard tape.

**THE HARD SEQUENCE** (`docs/prereg/BARS.tsv` header, research
2026-08-16T13:27:33Z):
> **F1a, F1b, F1c and F2 are RUN, and their numbers written down, BEFORE any
> sentence containing this arm's primary share is typed.** A primary typed ahead
> of the firings read is a REGISTRATION BREACH regardless of what it says, and
> the repair is an amendment chain, not a re-write. *(Precedent on the tape:
> `results.tsv:kladladder-verdict-amendment-f1f2-pending`. Structural
> enforcement precedent, and the stronger one: on BOTH parent legs the measuring
> agent was DENIED ACCESS TO THE SHARD TAPE, so it could not check its dose
> against the outcome. **The same denial is registered here.**)*

### F1 — THE DOSE BATTERY. MEASURABLE, but NOT off the shard tape and NOT via `dose.py` as briefed.
`tools/overnight.sh:138-139` passes `--replay /dev/null`, so the shard produces
**no** entity events. F1 runs on a **separate SERIAL battery**.

**⛔⛔ THE REGISTERED FIXTURE IS `--tle 10`, AND THAT IS WHAT MAKES THE
INVOCATION A LOCK BLOCKER.** `results.tsv:beltbreak2-final` banked the reason:
*"`tools/dose.py` passes NO `--tle` and `fcode run` DEFAULTS TO `--tle 0` (LIMIT
DISABLED, `run.py:119`) while the shard runs `--tle 10`. ON THE SHARD'S OWN
FIXTURE the same registered n=60 reads DOSE DELIVERED at 1.26×/1.45×, and the
doctrine's quoted median 49.5→40 reproduces (49.0→40) — which it does NOT at
tle=0."* **Verified independently at this draft: `tools/dose.py`'s argparse
(`:134-172`) has no `--tle` option and `:226-228` builds
`[fcode, run, bots[0], bots[1], maps/<m>.map26, --seed, <s>, --replay, <p>]`
with no `--tle`.** ⇒ **the brief's "`--tle 10` battery" is NOT executable through
`dose.py` at HEAD.**

**REGISTERED INVOCATION — form (A), executable at HEAD with NO tool change:**
```
# 60 games = 15 maps x 2 seats x 2 seeds, SERIAL, --tle 10 (the SHARD's fixture),
# TREATMENT vs the CARRIER (not the control), replays retained for F1b/F1c/F2.
mkdir -p scratchpad/bbcap3_replays
i=0
for seed in 1 2; do
  for m in antler archipelago auroraveil drakkarfjord drumlin fjordgate \
           frostgate glacierkeep icefloe midgard nordkap ragnarok royale \
           valkyrie yulerune; do
    for seat in 0 1; do
      if [ $seat -eq 0 ]; then A=bots/_v503bbcap3;      B=bots/_v488beltbreak2
                          else A=bots/_v488beltbreak2;  B=bots/_v503bbcap3; fi
      .venv/bin/fcode run $A $B maps/$m.map26 --seed $seed --tle 10 \
        --replay scratchpad/bbcap3_replays/g$(printf %04d $i)_${m}_s${seed}_treatseat${seat}.replay26
      i=$((i+1))
    done
  done
done
.venv/bin/python tools/corpus/replay_events.py scratchpad/bbcap3_events.tsv \
    scratchpad/bbcap3_replays/*.replay26
```
**REGISTERED SIZE: 60 games, SERIAL** (never parallel: D65, a 16-game parallel
dose check once reported the OPPOSITE of a serial one and both were wrong).
**REGISTERED ARITHMETIC (the band `dose.py` would have printed, stated explicitly
so form (A) is not a weaker instrument): the paired per-game difference
(treatment count − carrier count) is averaged over the 60 games and compared to
`2 x SE` of that paired mean.** Clearing the band by less than 2× on a short
battery is **UNRESOLVED**, which defaults to the restriction.
**REGISTERED ALTERNATIVE — form (B):** the builder adds `--tle` to
`tools/dose.py` (a one-line argparse addition plus one list element at `:226`)
and fires
`tools/dose.py bots/_v503bbcap3 --kind gunner --ctrl bots/_v488beltbreak2 --registered 60 --keep scratchpad/bbcap3_replays --tsv scratchpad/bbcap3_dose.tsv --tle 10 --maps <all 15>`.
**Form (B) is preferred if the change lands before the lock; form (A) is what
makes this page lockable without one.** ⛔ **What is NOT registered, in either
form, is a bare `dose.py` call at the default fixture.**

**⛔ OB17 CHECKS PERFORMED AT DRAFT, WITH THE CLAUSE THAT COULD SURPRISE RUN
FIRST (the 2026-08-15T07:01Z rider).**
1. ⭐ **CHECK 3 FIRST — "what happens on silent non-execution" — AND IT RETURNED
   TWO ANSWERS NOBODY HAD.** (a) The `--tle` gap above: **the read would not
   fail, it would quietly measure a different fixture and print the same verdict
   vocabulary** — and on the carrier that difference was the whole result. (b)
   **F1c has no shipped read path at all** (next check). **Both are the quiet
   case this obligation exists for.**
2. **EXECUTING TOOLS NAMED:** `.venv/bin/fcode run` and
   `tools/corpus/replay_events.py` at HEAD `cc64b800` for form (A);
   `tools/dose.py` for form (B) **only after the one-line change**.
3. **PATHS CHECKED, NOT ASSUMED.** `--tle` exists on `fcode run` (used at
   `tools/overnight.sh:138`, `tools/dose.sh:97`). `replay_events.py` accepts an
   output TSV plus a replay glob (`:150-170`) and emits `file ev rnd team kind x
   y d2_own d2_enemy mw mh` (`:157`). ⛔ **`tools/dose.py:77`'s default `MAPS` is
   the RETIRED 8-map set** (`antler atoll drumlin fjordgate heart hive meander
   nordkap`) — **four of the eight are NOT in the live pool** — so form (B) MUST
   pass `--maps` explicitly. Defect inherited from the carrier's page and
   **routed around, not fixed**.
4. **`dose.py`'s `--ctrl` DEFAULT IS `PROGRAMME.md`'s INCUMBENT = `_v468kladturbo`,
   WHICH IS THE WRONG CONTROL FOR F1.** The dose question is *did `CAP`/`AMMO`
   add plants over the CARRIER*, so `--ctrl bots/_v488beltbreak2` is MANDATORY in
   form (B); form (A) hardcodes it.
5. **ONE DECODER FACT THAT WOULD HAVE INFLATED EVERY COUNT ~6×, recorded as a
   check that came out clean rather than as absent:** `rotate()` re-emits
   `placeEntity` for an existing entity. `tools/corpus/replay_events.py:113`
   guards it — a build is the FIRST `placeEntity` carrying an id — and the
   carrier's verdict MUTATION-TESTED that guard by deleting it in memory: gunner
   BUILD rows went **20 → 120 (6.00×)** while non-rotating kinds stayed
   byte-identical. **The guard is present and has been driven to the other
   answer.**
6. **FIXTURE HYGIENE, and it came out clean for a structural reason worth
   stating:** `--tle 10` is WALL-CLOCK, so a battery run in per-arm BLOCKS on a
   loaded box hands the arms different handicaps in a non-random direction (a
   real confound, s49, caught mid-battery when load moved 5.1 → 18.6). **Form (A)
   and `dose.py` both put BOTH trees in the SAME `fcode run`, so the arms share
   every game's load by construction and the block confound cannot arise.**
   ⚠ **It DOES arise for any cross-tree comparison run as separate batteries —
   interleave-and-shuffle is mandatory there.**
7. **AND THE REPRODUCIBILITY BOUND (READ-BEFORE-RATIFYING #9):** `fcode run` is
   not seed-reproducible for this chassis (unseeded spawn salt, `main.py:445`,
   `NOISE_ON=True` in both trees; three runs of antler seed 1 gave 45/106/74
   event rows). **Seed-paired language is void; the pairing controls map, seed
   and opponent, never the salt.**

#### F1a — PLANTS PER GAME (the dose). MEASURABLE off the F1 events TSV.
Rows with `ev == BUILD` and `kind == gunner`, filtered to the **BELTBREAK
signature** and counted per game per team, treatment minus carrier, paired.
⛔ **THE FILTER IS THE MIDLINE-AND-BAND CONJUNCTION, NOT THE BAND EDGE — this is
a correction the parent's leg had to make and it is inherited rather than
re-derived.** `results.tsv:beltbreak-early-final`: *"`d2_enemy` ALONE is a
confounded annulus measure, because the control in-band rows ALL have
`d2_own <= 41 = HUNT_BAND_DSQ` (home counter-battery on maps where a tile beside
OUR core is already d² 20-100 from theirs) … THE WORKING DISCRIMINATOR IS THE
MIDLINE-AND-BAND CONJUNCTION."* ⇒ **a shredder is a friendly GUNNER whose FIRST
`placeEntity` lands at `20 <= d2_enemy <= 100` AND `d2_own > 41`.** ⚠ **The band
edges are read with an explicit tolerance CALIBRATED FROM THE CARRIER ARM'S OWN
DISTRIBUTION at readout** (`replay_events.py:95-96,113` measures d² to a single
core anchor while the bot measures to the nearest tile of the 2×2 footprint, so a
plant the bot scored at d²=20 can decode a few units higher). **The DIRECTION is
registered; only the cut point is deferred, and it is derived from the control
arm, which cannot be tuned toward a verdict.**
**PRE-REGISTERED EXPECTATION: treatment plants/game STRICTLY ABOVE the carrier's,
paired difference outside `2 x SE`.** ⛔ **AND THE PRIOR SAYS OTHERWISE (1.34 vs
1.54 on 50 paired games) — so this read is expected to FAIL its own registered
direction, and the `DOSE INVERTED` branch of the falsifier is the pre-committed
handling.**

#### F1b — THE LIVE-CAP REFUSAL COUNT. MEASURABLE only with instrumentation, and DESCRIPTIVE by registration.
The `R_CAP` counter lives behind `self._bb_refuse("CAP")` (`raid.py:889-890`) and
reaches no engine event, so it is readable only off an **instrumented throwaway
copy** whose counters are not rate-limited — the same method the parent used
(30 games: `CAP` 6.6×/game vs `TI` 638×/game). **REGISTERED AS DESCRIPTIVE, and
the caveat travels with the number wherever it is quoted:**
⛔ **A REFUSAL COUNTER NAMES THE RUNG THAT FIRED, NOT THE CONSTRAINT THAT BINDS.**
Measured, stack funnel: *"L0+L3 read CAP refusals 10.4×/game yet raising the cap
bought nothing — 2.20→2.04."* ⇒ **a rising `R_CAP` is NOT evidence the cap was
binding and a falling one is NOT evidence it was not. This number may not appear
in any sentence that concludes something about bindingness.** Its legitimate use
is the FUNNEL SHAPE: the `TI : CAP` ratio at the second and third plant, which is
what tests READ-BEFORE-RATIFYING #4's claim that the `AMMO` raise tightened the
`TI` rung. **Registered secondary expectation, directional: `TI` refusals at
`live > 0` RISE in the treatment relative to the carrier. That is the #4
prediction and it is falsifiable.**

#### F1c — SHOTS PER SHREDDER, INCLUDING THE THIRD SHREDDER'S SHOTS. ⛔ NO SHIPPED READ PATH — REGISTERED AS A LOCK BLOCKER.
**This is the read that decides whether the magazine raise bought throughput or
dry turrets, i.e. the AMMOFLOOR cost curve on this chassis. It is also the read
neither shipped decoder emits.** Checked at draft, both:
* **`tools/corpus/replay_events.py` emits BUILD and DEATH rows ONLY** (`:157`).
  **There is no fire row of any kind.**
* **`tools/corpus/replay_econ.py` DOES decode `fireTurret` (message 12)** at
  `:295-311`, but its own docstring states the limit — *"shots, attributed by
  POSITION (the message carries only {from,to} — no id, no team)"* — and `COLS`
  (`:131-132`) aggregates **per file × team × round-band**. **No per-position and
  no per-entity row is emitted.**
⇒ **Registered method: a POSITION JOIN the builder writes and validates BEFORE
the lock** — `fireTurret` source positions joined to `replay_events.py` gunner
BUILD positions within a game, shredders ranked by BUILD `rnd` so the FIRST,
SECOND and THIRD are separable. **Registered hazards, both of which must be
measured rather than assumed:** (i) **a rebuild on the same tile merges two
gunners' shots** — count same-tile gunner rebuilds per game and report the
merge rate; (ii) **a non-shredder turret standing on a tile that a shredder later
occupies mis-attributes** — the parent's `replay_econ` note records exactly this
class (`:60-68`, `id_pos` staleness). **REGISTERED POSITIVE CONTROL, required
before the number is quoted: the join must reproduce `replay_econ.py`'s own
per-file `shots_gunner` total to the digit when summed over all gunner positions,
and must return ZERO when the kind column is overwritten.** ⛔ **If the join is
not built and driven to the other answer, F1c is `NOT MEASURED` and the r300
bar's named hazard has no metric — which per OB12's default is a RESTRICTION, not
a permission.**

### F2 — THE THREE-LIVE-SHREDDER READ. THIS IS THE WIRING CHECK. MEASURABLE off F1's retained replays.
```
# from scratchpad/bbcap3_events.tsv, per game per team:
#   walk BUILD/DEATH rows in round order, maintaining the LIVE set of gunners
#   satisfying the shredder signature (20 <= d2_enemy <= 100 AND d2_own > 41)
#   (a) MAX SIMULTANEOUS LIVE SHREDDERS per game  -> THE CONSTANT'S RUNTIME EFFECT
#   (b) share of games reaching 3                 -> the cap's occupancy
#   (c) round at which the 3rd first goes live     -> when the new slot is used
#   (d) histogram of d2_enemy for all shredder builds -> siting unchanged check
```
**Pre-registered expectations, all directional:**
* ⭐ **(a) IS THE DECISIVE WIRING SIGNATURE AND IT IS EXACT: the CARRIER CANNOT
  EXCEED 2 BY CONSTRUCTION** (`raid.py:889` refuses at `live >= 2`), so
  `max(carrier) == 2` in every game and **the treatment MUST reach 3 in at least
  one game or the manipulated `CAP` had no runtime effect.** This is the analogue
  of the carrier's own r10-24 mass check, which was *"DECISIVE: the gate
  signature is exact — treatment's earliest plant r10, parent's r25, each on its
  own constant to the round"*.
* **(b)/(c)** describe how often and how late the new slot is used; **a
  three-live share near zero means the constant is nearly inert whatever the
  share says**, and that is the `THE CAP NEVER OPENED` row of the honest-null
  table.
* **(d)** this arm changes siting NOT AT ALL, so **a difference in the `d2_enemy`
  distribution is an INSTRUMENT ALARM, not a finding.**
* ⛔ **AND THE AMMO HALF NEEDS ITS OWN WIRING LINE, because `CAP` alone would
  otherwise carry the whole check:** off `replay_econ.py`'s
  `ammo_converted` / `n_convert` columns per file × team × round-band, **the
  treatment must convert MORE titanium into ammunition than the carrier in the
  band containing the first shredder plant.** ⚠ **The engine's `ammo_target`
  itself is NOT observable and the columns are BAND-aggregated, not per-round —
  so this is a coarse check and is labelled as one. It can show the raise had an
  effect; it cannot show the target was exactly 36.**

### D3, D4 — the outcome-shape reads. MEASURABLE, shard-native.
`cond` and `turns` are on the tape.
* **D3 — THE r300 ADMISSION BAR (see `KILL-ROUND NON-REGRESSION`).** ITT RMST₃₀₀
  per side over all 5,400 rows, plus the ITT timely-kill-by-r300 rate per side,
  plus the kill-win-conditioned share and conditioned median as DIAGNOSTICS. Both
  bars scored as exclusions off `tools/cluster_ci.py --null`. **And the CARRIER
  contrast reported beside them at ±3.3567 rounds / ±1.8671pp, DESCRIPTIVE.**
* **D4 — COND MIX**, the share of games ending `core_destroyed` / `tiebreak` /
  `NOWINNER`, per arm, and the **median kill round** as the gross backstop
  (median crossing 300 is disqualifying). Carrier anchors: ITT timely-kill 30.80%,
  r1000 share **11.28%**. **`R1000_IS_DEFEAT` makes a tiebreak share a cost even
  when the tiebreak is won**, and a plank that buys turrets and starves their
  magazines is exactly the family that could trade kills for a grind — which is
  why this is a registered read and not a formality.

### NOT MEASURABLE on this leg — named, not silently dropped.
* **PLANT COUNTS, PLANT ROUNDS, ANNULUS SITING, LIVE-SET OCCUPANCY, SHOTS AND
  GUNNER LIFESPAN ARE NOT DECODABLE OFF THE SHARD.**
  `tools/overnight.sh:138-139` runs `--replay /dev/null`: **local corefill keeps
  TAPES, not REPLAYS**, and the tape's columns are
  `ts shard game map seed seat winner cond turns`. ⇒ **every mechanism number in
  this leg comes from the SEPARATE F1/F2 batteries, and the shard's n = 5,400
  lends them none of its power.** Anyone quoting a plant count "from the BBCAP3
  shard" is quoting something that does not exist.
* **PER-SHREDDER SHOT ATTRIBUTION** — see F1c. **No shipped path; a validated
  join is a lock precondition.**
* **WHAT A PLANTED GUNNER WAS AIMED AT, AND WHETHER ITS ROTATION WAS USED.**
  Facing is not in the decoded event stream. ⚠ **This bites harder on THIS arm
  than on its parents, because `main.py:1093`'s rotation Ti gate is one of the
  four sites the `AMMO` raise moves (34 → 46) — so the arm changes rotation
  behaviour on a dimension this leg cannot observe.** Registered as a NAMED
  UNOBSERVED CHANNEL: a null on this arm does not separate "the third shredder
  was low-value" from "rotations were suppressed by the raised gate".
* **PER-UNIT CPU / TLE.** Local replays carry no exec-time fields at all
  (`execTimeUs`/`tled` absent from 100% of local `BotOutput` events;
  `get_cpu_time_elapsed()` returned 0 on all 22,289 local unit-turns in the
  carrier's demo) — the s42 addendum's blind-zero, on the dimension that silently
  destroys units. **The local number is UNINFORMATIVE, not clean.** The
  structural argument is what carries: the change is two integer literals
  compared inside gates that already ran every round in both arms — **no loop, no
  scan, no allocation.** `--tle 10` caps a timeout engine-side. ⚠ **If this arm
  is ever promoted toward a ship, `LOKI_BELTBREAK_LOG` must be verified off and
  re-screened** (it is identical in both arms here, so it cannot bias this
  screen — a statement about THIS CONTRAST, not about the shipped bot).
* **SEED DETERMINISM.** `NOISE_ON` pins an unseeded RNG (`main.py:445`), so
  base-vs-base at one seed diverges at round 0. **No seed-matched or replay-diff
  equivalence claim is available on this fixture; the flag-restore equivalence
  claim is made on the CODE plus the 0/16 flag-off battery with its 8/16 and
  16/16 positive controls, never on a replay comparison of shard games.**

---

## THE CHANGE — `file:line`, carrier → treatment

**TREATMENT TREE: `bots/_v503bbcap3`** = `bots/_v488beltbreak2` plus **TWO
EXECUTABLE LINES, ONE MECHANISM**. Verified at draft, and re-runnable in two
commands:

```
$ for f in eco.py main.py raid.py; do cmp bots/_v488beltbreak2/$f bots/_v503bbcap3/$f; done
                                                            # all three clean
$ diff bots/_v488beltbreak2/doctrine.py bots/_v503bbcap3/doctrine.py \
      | grep -E '^[<>]' | grep -vE '^[<>] *(#| *$)'
< LOKI_BELTBREAK_CAP = 2          # live beltbreak gunners at once (study MAX_LIVE_FWD_GUN)
> LOKI_BELTBREAK_CAP = 3          # V503: 2->3. ONE MECHANISM WITH THE LINE BELOW (fund what you allow):
< LOKI_BELTBREAK_AMMO = 24        # two 12-ammo kill cycles held for the gunner
> LOKI_BELTBREAK_AMMO = 36        # V503: 24->36. Three 12-ammo kill cycles for THREE gunners --
```
⇒ **TWO non-comment changed lines, at `bots/_v503bbcap3/doctrine.py:1445` and
`:1453`.** The remainder of the 15-line `doctrine.py` diff is comment
continuation recording the BBSTEP substitution finding and the magazine
arithmetic. **`eco.py`, `main.py` and `raid.py` are BYTE-IDENTICAL to the
carrier's, `cmp` clean on all three.**

**THE READ SITES, and there are FOUR** — `grep -n
'LOKI_BELTBREAK_CAP\|LOKI_BELTBREAK_AMMO' bots/_v503bbcap3/{raid,main,eco}.py`
at draft:
```python
# raid.py:889  — THE CAP GATE (a LIVE CENSUS, not a monotone counter)
        live = self._live_beltbreak_guns(ct, E)
        if live >= LOKI_BELTBREAK_CAP:
            return self._bb_refuse("CAP")

# raid.py:904  — THE FUNDING GATE for the 2nd and 3rd plant.  ⛔ THE AMMO
#                CONSTANT IS A TERM IN THE TITANIUM REQUIREMENT.
        need = ct.get_gunner_cost()
        if live > 0:
            need += LOKI_BELTBREAK_TI_FLOOR + LOKI_BELTBREAK_AMMO   # 40+24 -> 40+36

# main.py:384  — the core's Ti->ammo conversion target while a heartbeat is fresh
                    ammo_target = max(ammo_target, LOKI_BELTBREAK_AMMO)

# main.py:1093 — the ROTATION titanium gate (34 -> 46)
            if ct.get_global_resources() < 10 + LOKI_BELTBREAK_AMMO:
                return
```
`grep` on `eco.py` → **0 hits**, consistent with `eco.py` being byte-identical.
**Import binding: `raid.py:64` and `main.py:35` are both
`from doctrine import *`, so all four sites bind to the two changed lines.**

**⛔ THE ASYMMETRY THAT MAKES "ONE MECHANISM" A CLAIM RATHER THAN A DEFINITION.**
The brief's framing is *fund what you allow* — one lever with two dials. **On
this chassis the second dial has three read sites and only one of them funds
anything** (READ-BEFORE-RATIFYING #4). **A certifier who accepts "one mechanism"
without reading `raid.py:904` is accepting that the magazine raise is neutral to
the plant decision, and it is not: it raises the Ti bar for exactly the plants
the cap raise exists to permit, on the rung that is 87-91% of all refusals.**
⇒ **the two constants are ONE mechanism only in intent. In the code they are one
FUNDING change and one COUNTING change whose interaction is unmeasured and, on
the one battery that measured its net effect, negative.**

**⭐ THE CAP HAZARD THIS PLANK ROUTES AROUND, unchanged from its parents and worth
a certifier's minute:** `LOKI_FWD_GUN_CAP` counts `SLOT_FWD_GUN`, written only as
`read + 1` and never decremented — **it counts RUBBLE**, so three dead forward
turrets close that arm for the match. **BELTBREAK does not touch that counter**;
its cap is a LIVE CENSUS (`_live_beltbreak_guns`, `raid.py:~785-800`), and
`_live_fwd_guns` counts only SENTINELs. **The two arms share no counter and no
store slot** (`SLOT_BELTBREAK = 13`). ⚠ **AND ONE BOUNDED BLINDNESS THE DOCSTRING
ITSELF DISCLOSES, WHICH THIS ARM MAKES SLIGHTLY WORSE:** the live census has no
monotone fallback, so *"a raider that cannot see a teammate's gunner reads a low
count"*; the docstring bounds the worst case as *"two raiders on opposite faces of
the enemy core planting one each — which is `LOKI_BELTBREAK_CAP` exactly."*
**At `CAP = 3` that reassuring identity no longer holds: the bound the docstring
relies on was written against the value this arm changes.** Registered as a
DIAGNOSTIC, measured by F2(a) — a max-live count of 4+ in any game would show the
census under-counting and is an INSTRUMENT ALARM.

---

## THE TW HAZARD — REGISTERED AS CHECKED, WITH THE DIRECTION ARGUED

**The hazard:** x3r0's Odin carries a weapon **gated on never having seen one of
our turrets**. An arm that DELAYS our first visible turret re-enables it. This is
a live opponent capability and the reason the check is on the page.

**THE DIRECTION IS SAFE FOR THE FIRST TURRET, AND THE ARGUMENT IS STRUCTURAL
RATHER THAN ASSERTED.** `raid.py:889` refuses at `live >= CAP`, so raising `CAP`
2→3 **cannot refuse a plant the carrier would have allowed** — the predicate is
monotone in the cap. `raid.py:904`'s funding term applies only `if live > 0`, so
**the FIRST plant's funding is untouched** and its round is unchanged. ⇒ **the
first visible forward turret is identical in distribution to the carrier's
(median plant round ~40), which is the safe direction.**
⚠ **SCOPE, so this is not over-read:** the check is that this arm does not DELAY
the first turret. **It says nothing about the second and third, which
`raid.py:904` DOES delay by 12 Ti — and the s49 deferral battery measured that
delaying our first turret cost `Δmean +11.65 rounds [+1.08, +22.22]` on the
first-turret metric with the TW hazard firing.** The mechanism there was a
DEFERRAL; here the deferral lands on turrets 2..n. **That is a different, smaller
exposure, it is not zero, and it is registered rather than argued away.**
⚠ **AND `first-turret-round` IS FIXTURE-DEPENDENT ON THIS BOARD — three
independent instances in one day of its sign inverting between NOISE regimes.**
**No first-turret claim from a single-regime local battery is quotable on this
page**; the structural monotonicity argument above is what carries.

---

## SEEDS

**SEED BASE: 848000.** Registered worklist row (**to be appended by the builder,
not by this agent**):
```
BBCAP3 bots/_v503bbcap3 bots/_v468kladturbo 5400 848000
```
**FREENESS, verified at draft on four surfaces, with a POSITIVE CONTROL RUN FIRST
so the check has been seen to produce the other verdict:**
* **POSITIVE CONTROL: `grep -c '826000' scratchpad/corefill_work.txt` → 1**, the
  `ODINVSSLEIP` row. **The grep HITS when it should hit.**
* `grep -c '848000' scratchpad/corefill_work.txt` → **0**;
  `scratchpad/fleet_queue.tsv` → **0**;
  `grep -l '848000' scratchpad/overnight/*.tsv` → **no file**;
  `grep -l '848000' docs/prereg/*.md` → **no file**;
  `grep -rl '848000' scratchpad/overnight-remote/` → **no file**.
* **Same-family bases enumerated per surface, not assumed:** 816000 `ECOMMIT`,
  818000 `FREEROUND`, 820000 `ROUTESCORE`, 822000 `BELTBREAK-EARLY`, 824000
  `BELTBREAK-LATE`, 826000 `ODINVSSLEIP`, 828000 `KLADLADDER2`, 830000
  `KLADLADDER3`, 832000 `SEALPIERCE`, 834000 `ECOMMIT2` (prereg only, no
  worklist row at draft), 836000 `OPENFAST` (prereg only), 840000 `BELTBREAK2`
  (worklist row + completed tape).
* ⚠ **DISCLOSED RATHER THAN PRESENTED AS "THE NEXT FREE BASE": 842000, 844000 and
  846000 are ALSO free on all four surfaces at draft.** 848000 is registered as
  the brief specifies, which leaves those three for the concurrent
  `_v502bbstack` / `_v504bbammo` legs — **neither of which has a seed
  reservation on any surface at draft, so a successor must not read the gap as
  reserved.** A collision-avoidance grep that returns a false positive on a
  prereg's own freshness-check line is a known trap here
  (`PREREG-OPENFAST:314`); this enumeration is per-file for that reason.
* **NO OVERLAP, READ OFF THE RUNNER RATHER THAN ASSUMED:**
  **`tools/overnight.sh:124` is `seed=$(( SEEDLO + n / 16 ))`** — sixteen games
  per seed — so a 5,400-game shard consumes **338 distinct seeds, not 5,400**.
  BBCAP3 at 848000 uses **848000-848337**, with 1,662 seeds of headroom before
  850000.
* ⛔ **THE BUILD AGENT'S DEMO / ABLATION SEEDS ARE DELIBERATELY EXCLUDED from the
  screen.** They are the fixture the constants were measured on; reusing them
  would screen the arm on the seeds that selected it.

---

## AMENDMENTS

**ADD-ONLY, and blind to the data.** Any amendment to this document is a NEW
dated section appended below this line, never an edit to anything above it; it
must be typed and committed BEFORE the number it could bear on exists, and it
must say what it is blind to. An amendment that removes, weakens or re-words a
registered bar, falsifier, band, segment or MDE is not an amendment — it is a new
pre-registration and needs a new leg. *(`tools/prereg_check.py --amendment
<locked.md> <amended.md>` is the checkable form.)*
**Pooling extra rows into this shard after lock is an unregistered n increase —
optional stopping with extra steps — and is prohibited. A replication on fresh
seeds is reported SEPARATELY and NEVER pooled** (the GUNAXABL/SENTTHR precedent:
remote replications corroborated a null they were not allowed to rescue).
**Two items are LOCK PRECONDITIONS rather than amendments and must be resolved
BEFORE the lock commit, not after:** (1) the F1 `--tle 10` invocation, form (A)
or form (B) (READ-BEFORE-RATIFYING #7); (2) the F1c position-join with its
positive control (#8). **A lock typed with either unresolved registers a method
that cannot be executed, which is OB17's exact failure.**

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one LOCAL core to n = 5,400, plus 60 serial games for F1/F2, plus an
instrumented 30-game throwaway for F1b, plus the position-join build for F1c.**
ZERO rated ladder exposure, zero submissions, zero unrated challenges — nothing
on this page touches the platform, which is why `TARGET BAND` is N/A.
**⚠ AND THE EXPECTED VALUE OF THAT CORE IS BOUNDED BY TWO THINGS AT ONCE:** at
the projected true share the arm reaches its own registered n with probability
**≈0.51** (READ-BEFORE-RATIFYING #3), and **even on completion the primary
cannot resolve the increment the arm exists to test** (#2). **The core most
likely buys either a `cancellation` row or a Band-2 sentence — "the carrier still
works" — which we already know.**

**It does NOT decide a ship.** `SLOT_STOP_LOSS: off` and the parked SWITCH step of
`X3R0_SLOT_RULE` mean **the slot changes only on Magnus's explicit word**,
whatever this leg returns; `X3R0_SLOT_RULE` requires **≥60% ±2pp** against the
control before an arm even reaches the head-to-head step, and nothing in the
projected range is near it. **A local screen against our own shipped bot is gate
1; gate-1-to-gate-2 transitivity is UNVALIDATED in this repo (QUEUE #65: 3
concordant, 1 not), so the head-to-head is not skippable on the strength of this
number.** Per rule 6, **no local screen closes a road** — a refutation needs
live-game backing.

**⚠ KNOWN PREFLIGHT FAIL, NAMED AND NOT FIXED:**
`.venv/bin/python tools/preflight.py bots/_v503bbcap3` is expected to FAIL on
*"no PREREG.md or README.md"*, exactly as the carrier and the parent do — **a
standing property of every tree in this family, not a regression introduced by
this arm.** Reported in one line; not fixed by this agent.

---

## ⛔⛔ DRAFT DISPOSITION — **HOLD. DO NOT SPEND A CORE ON THIS SHARD YET.**

**This is a recommendation from the drafting agent, not a ruling. The builder
weighs it at lock time.** It is stated plainly because the brief asked for a
plain answer including "no".

**THE CASE FOR HOLDING, in the order the evidence arrived:**
1. **The arm's treatment-occurrence evidence is measured NEGATIVE on its own
   chassis** — plants/game 1.34 vs 1.54, paired, 50 games/arm. The obligations
   doc's own template for this situation (Addendum 4, LOKI-3) is **stand down and
   own the null**, and it calls that *"the OPPOSITE of drift"*.
2. **The one distinguishing prediction of the pro-case has already been tested
   and contradicted.** "The cap binds once timing improves" was the whole reason
   to revisit a 0.000 null; the improved chassis was the fixture; it went the
   other way.
3. **There is a code-level mechanism for why**, found at draft and independent of
   both batteries: `LOKI_BELTBREAK_AMMO` is a term in `raid.py:904`'s funding
   gate, so the "fund what you allow" edit **raises the Ti bar for exactly the
   plants the cap raise permits**, on the rung that is 87-91% of all refusals.
   **This arm may be miswired rather than merely wrong**, and a miswired arm
   should be repaired before it is screened.
4. **Even a completed shard cannot answer the arm's question** (#2): the primary
   is satisfied by inheritance from a carrier at 53.09, and the incremental
   contrast is ±1.87pp against a projected −0.4pp.
5. **The probability of completion is ≈0.51** at the projected share, and the
   clause that ends it is a floor no exemption waives.
6. **The concurrent `_v504bbammo` (LEG-3, the chosen eco×offense pair) interacts
   destructively with this mechanism on the one fixture that has composed them**
   (shots/shredder 6.0 vs 14.0, fires −46%). **Screening BBCAP3 before BBAMMO's
   read is buying the less informative of two ordered legs.**

**WHAT TO DO INSTEAD, cheapest first — each of these is a probe, not a shard, and
all three together cost less than one core:**
* ⭐ **PROBE A (the one that could revive the arm): a MAGAZINE-NEUTRAL CAP-ONLY
  arm.** `LOKI_BELTBREAK_CAP` 2→3 with `LOKI_BELTBREAK_AMMO` **left at 24**, run
  as a 60-game paired F1/F2 battery at `--tle 10` against the carrier. **This is
  the arm that isolates the counting change from the funding change** — the
  confound READ-BEFORE-RATIFYING #4 identifies — and the current arm cannot
  distinguish them at any n.
* ⭐ **PROBE B: the `raid.py:904` variant the AMMOFLOOR sweep's own re-brief
  specified — REMOVE `LOKI_BELTBREAK_AMMO` from the reserve** (`need += TI_FLOOR`
  only) at `CAP = 3`. If #4 is right, this is where the third plant becomes
  affordable, and it is the opposite edit to the one on this page.
* **PROBE C: order the legs.** Take `_v504bbammo`'s read first; it is the eco half
  of Magnus's narrowed board, it is unentangled with the cap, and its result
  changes which cap arm is worth building.
* **AND IF THE BUILDER FIRES BBCAP3 ANYWAY** — a defensible choice, since the
  negatives are n=50 probes and a core is cheap — **the page is lockable as
  written, provided the two LOCK PRECONDITIONS are resolved and the
  `COMBO-BAR-EXEMPT` token carries Magnus's ruling rather than a self-grant.**
  In that case the honest framing at readout is: **this shard measures the
  chassis total and prices the funding-gate side effect; it does not measure the
  cap.**

**⚠ AND THE COUNTER-ARGUMENT, so the HOLD is not the strongest available reading
either:** unrated-and-local games are free, `ALWAYS_BE_RUNNING` is a core value,
an idle core is a defect, and **a 50-game NOISE_OFF ablation is exactly the
underpowered instrument this repo has been burned by in both directions.** If no
better-supported plank is queued for the core BBCAP3 would occupy, firing it and
banking the `DOSE INVERTED` finding is not an error — it is a cheap purchase of a
mechanism fact. **The recommendation is HOLD *relative to Probes A/B/C*, not HOLD
*in favour of an idle core*.**

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read IN FULL: OB7 — which is why READ-BEFORE-RATIFYING #2 discloses the pre-satisfied primary rather than leaving it for a certifier; OB8, OB10, OB11, OB12 + its pre-committed restriction default; OB13; OB14; OB15a/b/c + the segment vocabulary and the units rider; OB16 + its `BAR = null + MDE + half_width` amendment, its zero-MDE corollary and its cross-host rider; OB17 + its *"run the clause that can surprise you"* rider, which is why the OB17 block runs check 3 FIRST and found two live defects; **Addendum 4's LOKI-3 stand-down template**, which is the procedural basis of the HOLD recommendation; and the **2026-08-17T07:24:55Z addendum** that replaced the local-shard clock-2 boilerplate — quoted rather than restated) · `PROGRAMME.md` (parsed block `:6-30` — `INCUMBENT: bots/_v468kladturbo`, `PRIMARY_CURRENCY: game_share`, `WIN_RATE_IS_VERDICT: yes`, `KILL_WINDOW_RND: 250`, `R1000_IS_DEFEAT: yes`, `PLAY_DEFENCE: not_at_the_kill_s_expense`, `DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`, `SLOT_STOP_LOSS: off`, `X3R0_SLOT_RULE` incl. its 60±2 re-pricing and the parked SWITCH step; the `:488-564` r300 chain in full — the 05:15:45Z re-pricing, the 05:19:38Z collider correction, the 05:3xZ arbitration freeze and the **05:36:10Z ITT RMST₃₀₀ resolution with its vintage rule**, which is why RMST₃₀₀ is the operational estimator here) · `docs/prereg/PREREG-BELTBREAK2-2026-08-17.md` (**the CARRIER's prereg, read IN FULL** — its match structure, token order, registered machinery, DEFF enumeration, FIRINGS-BEFORE-PRIMARY hard sequence, seed-freeness method and caveat set are INHERITED here where they still apply; its `RND` timing case is not) · `results.tsv` rows **`beltbreak-early-final`** (the parent's completed 53.81 [52.49,55.14] at n=5400, the midline-and-band discriminator correction, the rotation-guard mutation test at 6.00×, the three parity cells and the expressible-12 read) and **`beltbreak2-final`** (**the carrier's 53.09 [51.76,54.42] at n=5400, ITT timely-kill 30.80 vs 24.35 = +6.45pp non-overlapping, r1000 11.28%, the three parity cells 47.78/51.67/50.28 vs expressible-12 53.89 [52.40,55.38], the F2 gate signature, the `dose.py` `--tle 0` vs shard `--tle 10` finding, the `fcode run` non-reproducibility finding, the scale-drag +4.0pp by r60, and the disposition naming `_v502bbstack` as CAP3/AMMO36's home**) · `results.tsv` rows `idnull140-cert-5400`, `null125-final`, `kladladder-n-final-correction`, `kladladder-verdict-amendment-f1f2-pending` · `docs/prereg/BARS.tsv` (**header/format ONLY, incl. the FIRINGS-BEFORE-PRIMARY rule of 2026-08-16T13:27:33Z, the `le`-direction never-stop carve-out, and rows `:310` `BELTBREAK-EARLY` / `:312` `BELTBREAK2` read for the COMBO-BAR-EXEMPT precedent and for bar comparability. `grep -c -i BBCAP3` → 0. NO ROW WAS ADDED BY THIS AGENT**) · `docs/coordination.md` (the s49 BBSTEP entry — 132% substitution, `R_CAP` 2,354→2,859, the pre-scan inner-bound arithmetic bug, the `TI → CAP → siting` nest, the stack's dependency order; the s49 AMMOFLOOR sweep entry — 2,897 games / 5 doses, ammo held 30.9→10.2, dry-turret rounds 26→181, dose 3 −27.5pp, the turrets-2..n vs first-turret split, *"the kill constraint is turret THROUGHPUT, not COUNT"*, the LEG-3 re-brief's *"no `BELTBREAK_AMMO` in the reserve"*; the s49 deferral battery's TW-hazard firing and the `first-turret-round` fixture-dependence; the interleave-and-shuffle mandate and the load-confound incident) · **the coordinator's s49 relay of the `_v502bbstack` per-leg ablation** (CAP leg plants/game 1.34 vs 1.54; CAP+floor shots/shredder 6.0 vs 14.0 and fires −46%; CAP+step-without-floor 27.3; the funnel finding that a refusal counter names the rung that FIRED, not the constraint that BINDS, with L0+L3 CAP refusals 10.4×/game against 2.20→2.04) · `CLAUDE.md` (the ONE GLOBAL ADDITIVE cost-scale factor and its `bots/_probe_scale` s26 engine confirmation; the DEFF scope procedure and its direction clause; the local 0.98 exemption; the `print()`-stripped-from-platform-replays ruling, which is why no read here touches our own stdout; `R1000_IS_DEFEAT`; rule 6) · `bots/_v503bbcap3/{doctrine,eco,main,raid}.py` (read at draft: `doctrine.py:1392-1460` the comment block and all eleven BELTBREAK constants, the two changed lines at `:1445`/`:1453`, `:2085` the inherited compose marker; `raid.py:785-800` the live-census docstring and its `CAP`-valued worst-case bound, `:875-925` the gate ladder, `:889` the cap gate, `:904` the funding gate; `main.py:35` and `raid.py:64` the `from doctrine import *` bindings, `main.py:370-400` the ammo target, `main.py:1080-1105` the rotation gate) · `bots/_v488beltbreak2/{doctrine,eco,main,raid}.py` (the carrier, `cmp`'d file-by-file) · `bots/_v468kladturbo/doctrine.py:1879` (the compose marker every arm on this chassis inherits) · `tools/prereg_check.py` (read for `KNOWN_KEYS`, `key_pattern`/`field`, `first_number`, the OB13 `git_diff_paths` / `untracked_arm_paths` CANNOT-COMPUTE branch, `ROUND_GATE_RE`/`check_metric_window`, `check_pool_era`, `DEFF`/`CLUSTER_SYNONYM`, and the `_defence_bar_ok` predicate that enforces the r300 form) · `tools/auto_gate.py` (`:244-247` `MARK_CATASTROPHE`/`MARK_MID`/`MARK_HALF`/`CATASTROPHE_CI_HI`, `:261` `TREND_FLOOR = 52.0` and its Magnus provenance, `:278` `COMBO_BAR = 55.0` and its pricing table, `:715-742` `combo_of()` and its read of the TREATMENT tree's `doctrine.py`, and the confirmation-class run-to-completion exemption block) · `tools/overnight.sh` (`:57-68` the live 15-map pool, `:99-103` the `START=` / `# FIXTURE` stamp, `:124` the `SEEDLO + n/16` seed walk, `:138-139` `--replay /dev/null --tle 10`) · `tools/overnight_read.py` (`:76-94 map_area_class` and `live_pool()`, both RUN at draft to classify all 15 live maps — antler/fjordgate CQ, royale STD) · `tools/dose.py` (`--help` read in full; `:77` the RETIRED default `MAPS`, `:134-172` the argparse — **checked for `--tle` and it is ABSENT** — `:175-200` the CLASS B gate, `:212-219` the seed walk and map/seat rotation, `:226-228` the `fcode run` invocation with no `--tle`, `:250-262` the `--keep` retain-and-name path) · `tools/dose.sh` (`:97`, which DOES pass `--tle 10` — the existence proof that the flag is available on `fcode run`) · `tools/corpus/replay_events.py` (`:16,109-113` the rotation guard, `:95-96` the core-anchor convention, `:157` the output columns — **checked for fire rows and there are NONE**) · `tools/corpus/replay_econ.py` (`:60-68` the `id_pos` staleness note, `:86` the `fireTurret` position-only attribution, `:131-132` `COLS` — **checked for per-entity shot rows and there are NONE**) · `tools/cluster_ci.py` (`--help`; `--null` is the exclusion-restatement path the r300 bars use) · `scratchpad/CONTROL_PIN` and `tools/control_pin.py` · `scratchpad/corefill_work.txt` (row format, the 812000-840000 seed sequence, and the pre-existence / freeness greps) · `scratchpad/fleet_queue.tsv` and `scratchpad/overnight-remote/` (seed freeness) · `docs/prereg/PREREG-OPENFAST-2026-08-17.md` (`:309-317` its seed registration and the freshness-line false-positive trap) · git `cc64b800` (HEAD at draft), `54129ed7` (the commit that added this arm and `_v504bbammo`), `git ls-files`, `git status --porcelain` and `git diff --name-only 54129ed7^ 54129ed7` output quoted above · the drafting brief supplied by the builder lane s49 and its mid-task amendment. **No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md`, `QUEUE.md` or `docs/coordination.md` was created or modified by this agent, and no game was run. The only write was this document.**
