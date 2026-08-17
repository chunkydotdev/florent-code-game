# SCREEN PREREG — `BBDEMAND`: the ECO plank's surviving form is the **TARGET** axis, not the **FLOOR** axis (`T4_BURN_RNDS` 10 → 5)

Drafted by a fresh opus subagent with NO inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `docs/prereg/BARS.tsv` row, fired no game, started no
shard, and touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md`
nor `QUEUE.md`. **No tool was fixed** — two live tool defects are named below and
routed around, not repaired.

**STATUS: drafted BEFORE the `BBDEMAND` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any `docs/prereg/BARS.tsv` row exists,
BEFORE any `scratchpad/fleet_queue.tsv` row exists, BEFORE any file named
`scratchpad/overnight/BBDEMAND*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T13:13:03Z`** (`date -u`,
same shell call); repo HEAD at draft **`a7edbd0d`** (author time
`2026-08-17T15:10:29+02:00`). Verified at draft, all four in one shell call:
`grep -c BBDEMAND scratchpad/corefill_work.txt` → **0**;
`grep -c BBDEMAND docs/prereg/BARS.tsv` → **0**;
`grep -c BBDEMAND scratchpad/fleet_queue.tsv` → **0**;
`ls scratchpad/overnight/ | grep -ci bbdemand` → **0**.

### LOCK, clock 2 (local shard)
Per the obligations doc's **2026-08-17T07:24:55Z addendum**, which replaced the
clock-2 boilerplate that eleven preregs had copied and that was not executable as
written. **PRIMARY:** the shard tape's own `# FIXTURE … start=` stamp
(`tools/overnight.sh:99` sets `START=$(date -u …)`, `:103` writes it to the tape
before the first game; measured earlier than the tape's first completed row in
107 of 107 stamped local tapes). Quote it verbatim beside the lock commit's git
author time. **BACKSTOP, if the tape carries no `# FIXTURE` line** (every REMOTE
tape — 0 of 86 carry it): the tape's **FIRST COMPLETED ROW `ts`**, conservative
by construction (the true start is strictly earlier, so the substitution can only
OVERSTATE the gap; measured cost 1–2 s). **SECOND BACKSTOP, serial runners:** the
preceding shard's `COMPLETE` time on the same worker.
⛔ **NOT AVAILABLE: the heartbeat's `STARTING` line** — `overnight.sh:100` writes
it with `>` and every later state overwrites it. **State which clock was used.**
This shard is registered LOCAL / SAME HOST, so the primary is expected to be
available.

### ⭐ COMMIT PROVENANCE OF THE TREATMENT TREE — TRACKED AND CLEAN AT DRAFT
`bots/_v505bbdemand/` **is tracked by git and the working tree is clean**
(`git status --porcelain bots/_v505bbdemand` → **0 lines**;
`git ls-files bots/_v505bbdemand` → **4 files**). It landed in commit
**`3bdb7375`** — *"BUILDER s49: V505 bbdemand — the TARGET axis, not the floor
axis…"*. **This is the opposite of the parent page's condition:**
`PREREG-BELTBREAK2` had to record `OB13_UNTRACKED_ARM` because its arm tree was
`??` to git and the one-line claim was unverifiable *by git*. Here it is
verifiable by git, and it is also verified by the instrument that needs no git
(a direct file diff against the carrier), reproduced verbatim in `THE CHANGE`.

---

## ⛔ READ BEFORE RATIFYING — NINE THINGS THE LANE OWNS

**1. ⛔⛔ WITHOUT A `COMBO-BAR-EXEMPT` TOKEN THIS ARM IS ~98% CERTAIN TO DIE AT
THE n=2700 LOOK, AND THE EXEMPTION'S OWN PRECEDENT TEXT DOES NOT LITERALLY COVER
IT. THIS IS THE DECISION THE LOCK TURNS ON AND IT IS NOT MINE TO MAKE.**
`tools/auto_gate.py:715 combo_of()` greps the `stack.py` compose marker off the
**TREATMENT** tree's own `doctrine.py`; this tree inherits it from the control
chassis (`bots/_v468kladturbo/doctrine.py:1879`), as every arm on this chassis
does. ⇒ the gate scores `BBDEMAND` as a COMBO and `COMBO_BAR = 55.0` binds on the
n=2700 prefix (`auto_gate.py:278`, Magnus 2026-08-16).
**THE ARITHMETIC, done before the fire.** Its own carrier
`bots/_v488beltbreak2` measures **53.09% [51.76, 54.42]** vs the same control at
n=5,400 (`results.tsv:beltbreak2-final`). Taking that as the arm's central prior:

```
true share   P(prefix1000 < 52.0)   P(prefix2700 < 55.0)   P(reaches n=5400)
   52.00            0.500                  0.999                0.000
   53.00            0.263                  0.981                0.014
   53.09            0.245                  0.977                0.018   <- the carrier's own share
   54.00            0.102                  0.851                0.133
   55.00            0.028                  0.500                0.486
   56.00            0.005                  0.148                0.848
```

⭐ **TWO PRECEDENT ROWS EXIST AND MAGNUS GRANTED BOTH DIRECTLY**, and the
builder must carry the token with **HIS ruling as the grant**, quoted, never
self-granted:
* `docs/prereg/BARS.tsv:310` (`BELTBREAK-EARLY`) — *"⭐ COMBO-BAR-EXEMPT … GRANTED
  BY MAGNUS DIRECTLY, 2026-08-17T08:30:36Z, on the builder's escalation. This arm
  is a SOLO plank (ONE mechanism added to the incumbent chassis), not a
  combination. It reads as COMBO only because auto_gate.combo_of() … a
  CLASSIFICATION DEFECT, not a property of the arm."*
* `docs/prereg/BARS.tsv:312` (`BELTBREAK2`) — *"GRANTED BY MAGNUS DIRECTLY on the
  builder's escalation, same ruling as the BELTBREAK-EARLY row."*
Both rows also say: *"⛔ THE 52.0 TREND-FLOOR IS NOT WAIVED and binds at the 1000
look; only the 55.0 combo prefix is lifted."*

⛔⛔ **AND HERE IS THE HONEST COMPLICATION, WHICH THIS PAGE WILL NOT PAPER OVER:
BOTH PRECEDENT GRANTS REST ON THE PREMISE "SOLO PLANK — ONE MECHANISM ADDED TO
THE INCUMBENT CHASSIS", AND THAT PREMISE IS FALSE FOR THIS ARM.** Against the
registered control `bots/_v468kladturbo`, `bots/_v505bbdemand` carries **TWO**
mechanisms: the whole BELTBREAK shredder plank at `RND = 10` (absent from the
control — `grep -c 'BELTBREAK\|_bb_\|beltbreak' bots/_v468kladturbo/{doctrine,eco,main,raid}.py`
→ **0 / 0 / 0 / 0**, verified at draft) **plus** the T4 constant. The
misclassification argument (the marker is inherited, not earned) still holds in
full; the *solo* argument does not. ⇒ **the builder either (a) escalates to
Magnus for a grant that covers a plank-plus-one-constant iteration — the honest
form, and the same escalation path both precedents used — or (b) fires WITHOUT
the exemption, in which case row 1 of the table above is the expected outcome and
the core buys a `cancellation` row plus the F1/F2 reads.** ⛔ **The builder may
not read the two existing rows as covering this arm; their own text says why.**

⭐ **AND THE FRESH PRECEDENT SAYS THE BARS ROW IS NOT OPTIONAL EVEN WITH A
GRANT.** `results.tsv:beltbreakr-final`, same session: *"I queued the replication
WITHOUT a BARS row, so it carried no COMBO-BAR-EXEMPT token, and auto_gate's
remote reach … stop-cycled it at the 2700 combo look (prefix 51.52 < 55) — the
same misclassification Magnus already ruled on, walked into by the builder on the
replication of the very arm his ruling saved."* Its routed lesson: **EVERY shard
gets its BARS row (with any standing exemption) BEFORE its worklist row.**
⛔ **The 52.0 TREND-FLOOR is separately live: at the carrier's own share there is
still a ~24.5% chance of a cancellation at the n=1000 look.** The carrier itself
finished with CI lower **51.76 < 52.0** and survived that look on the draw.

**2. ⛔⛔ THE BAR ON THIS PAGE CANNOT ANSWER THE QUESTION THE ARM ASKS, AND THE
PAGE SAYS SO BEFORE THE DATA EXISTS.** The registered primary is the pooled share
vs `bots/_v468kladturbo` against the house band **51.33**. **That bar is a
TWO-PLANK bar**: the carrier already clears it at 53.09 [51.76, 54.42] with the
T4 constant absent. ⇒ **clearing 51.33 is NOT evidence that the constant helps,
and no readout sentence may say it is.** The question of interest is
**CARRIER-vs-THIS-ARM**, and it is **UNRESOLVABLE ON THIS FIXTURE**: the
half-width on that difference at 5,400 per side is **±1.86pp** (two-sample, DEFF
0.98, p̄≈0.53), against a plausible constant-sized effect of ~1pp.
⇒ **REGISTERED: the carrier-vs-this-arm difference is NOT an estimand of this
leg.** Any sentence comparing the two is **DESCRIPTIVE** and carries ±1.86pp
inline. **The bar is retained anyway**, because it is what keeps this arm
numerically comparable to the twelve sibling house-band rows and to its own
carrier, and because the *combination* (plank + constant) is what a ship would
carry — but its ceiling is *"the combination is still above the house band"*, not
*"the constant paid"*. **The attribution work is done by F1/F2 and by the
COMPLEMENT CELL (`#6`), not by the bar.** This is the same attribution cap
`SEALPIERCE` carries as a two-plank screen; it is named here rather than
discovered at readout.

**3. THE CONTROL IS THE LIVE LADDER HOLDER'S BOT, SO THIS LOCAL SCREEN IS ALSO A
SCREEN AGAINST WHAT IS LIVE.** `bots/_v468kladturbo` is **Sleipnir v1 / v155**,
pinned as the corefill control at `scratchpad/CONTROL_PIN`
(`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo` — quoted from the pin
file, not re-derived). **Every share on this page carries its control inline —
`X% vs _v468kladturbo` — and that notation is mandatory:** three different 60s
live in this repo and they differ by ~9pp through the logistic. **50.0 vs
`_v468kladturbo` means "adds nothing to the bot we ship".** ⚠ The control is the
SHIPPED BOT, not the CURRENT LADDER INCUMBENT — x3r0's Odin holds the slot
(`ODINVSSLEIP` measures that distance), and `SLOT_STOP_LOSS: off` plus the parked
SWITCH step of `X3R0_SLOT_RULE` mean the slot changes only on Magnus's word.

**4. WHY THE TARGET AXIS AND NOT THE FLOOR AXIS — THE PRO CASE, WITH ITS
STRONGEST POINT FIRST.**
* **Ammunition conversion is the #1 titanium claimant, on three independent
  fixtures.** 29.7–36.2% of spend; the third measurement is off raw replays by
  the builder — **1,142 Ti/game converted on the carrier**; and the AMMOFLOOR
  sweep's funnel independently reproduced the share on a second fixture
  (*"737 Ti/game to ammo against 1,902 collected = 39%"*, `docs/coordination.md`
  2026-08-17T12:2xZ). **A lever on the largest line of the ledger is the right
  place to spend a core if any eco lever is.**
* **`weapons_top` is a NON-DECREMENTING counter that counts rubble, and the tree
  says so in its own words.** `bots/_v505bbdemand/main.py:303-310`: *"Both gun
  slots are monotone — written only as `read + 1`, never decremented — so
  `weapons` counts rubble, and rubble is what buys the magazine: one dead forward
  Sentinel still asks for `min(120, 40 + 20*1) = 60` ammunition."* ⇒ **a 10-round
  burn target is held for turrets that may be dead.**
* **5 rounds is not starvation on any weapon in the game.** At
  `T4_AMMO_PER_RND = 4` the cap goes `40 × weapons_top` → `20 × weapons_top`.
  Twenty ammo is **2 sentinel volleys** (10/shot, reload 2 ⇒ 5 rounds of fire) or
  **5 gunner shots** (4/shot, reload 1) **per counted weapon**.
* ⭐⭐ **AND THE ASYMMETRY THAT IS THE WHOLE CASE: `convert_ammo` IS SAME-TURN
  USABLE, SO A LOWER TARGET DEFERS CONVERSION; A HIGHER FLOOR FORBIDS IT.**
  `CLAUDE.md`, engine-documented: *"at most once per team per turn, usable the
  same turn, and it does not use the core's action cooldown."* The top-up branch
  (`main.py:401-406`) re-arms the moment `ammo < ammo_target`. ⇒ **demand
  arriving late converts LATE, not NEVER.** The refuted floor axis worked the
  other way round: it reserved titanium by making the conversion branch
  unreachable (`ti > ti_floor` false), so demand arriving found the tap shut.
  **Replay-measured on the floor arms, and these are the numbers to beat: floor
  ON = shots −48%, conversion −43%, `ammo_end` 14.5 → 7.5.**

**5. ⛔ THE CON CASE, AND IT IS THE REASON THIS PAGE EXISTS RATHER THAN A
COMMIT.** **Three fixtures have already refuted ammo-throttling on currency**,
all in the FLOOR form:
* the **AMMOFLOOR SWEEP** (`docs/coordination.md` 2026-08-17T12:2xZ, 2,897 games,
  5 doses, paired 240 cells/arm): *"THE COST CURVE REPLICATES, THE GAIN CURVE DOES
  NOT. Ammo held 30.9→10.2 and dry-turret rounds 26→181 monotone in reserve size;
  dose 3 DISQUALIFIED at −27.5pp timely-kill [CI excludes 0]"*, and *"dose 1: 0 of
  120 cells changed on ANY metric"*;
* the **v502 STACK's LEG 3** (`docs/coordination.md` 2026-08-17T13:0xZ, n=200
  NOISE_ON): *"the mechanism is REAL (+0.450 plants) AND EVERY CURRENCY COLUMN
  MOVED AGAINST IT — wins 112→102, ITT-r300 28.0→22.5, **median kill 259→303,
  THROUGH the r300 gross backstop**, dry-magazine rounds 6.3→~95"*;
* the earlier `AMMO_FLOOR = 20` arm (`docs/coordination.md:70604`): *"`AMMO_FLOOR
  = 20` is the WRONG LEVER, not the wrong number."*
⇒ **THE BURDEN IS ON THIS ARM TO SHOW IT IS NOT THE SAME TRADE, AND THE
REGISTERED CROSSING IS THE DISCRIMINATOR: CONVERTED TITANIUM DOWN WITH
SHOTS-FIRED FLAT.** **Shots down too is the disqualified trade wearing a new
constant** and the honest-null clause says exactly that. **This is registered
BEFORE the fire and it is scored on F1, which is read before the primary.**

⚠ **AND ONE MORE CON, WHICH WEAKENS MY OWN PRO CASE AND IS NOT IN THE BRIEF: THE
GHOST MAGAZINE ALREADY HAS A BRAKE ON THIS CHASSIS, SO THIS ARM IS A SECOND
MITIGATION OF A PARTLY-MITIGATED DEFECT.** `main.py:315-327` implements
`T4_AMMO_IDLE` (`T4_AMMO_IDLE_ON = True`, `T4_AMMO_IDLE_RNDS = 12`,
`T4_AMMO_IDLE_MIN = 16`, verified in the tree at draft): if the magazine has not
FALLEN in 12 rounds while ≥16 is held, **`weapons_top` is forced to 0** and the
whole burn-cap branch is skipped. ⇒ the residual over-target this arm attacks is
only: (i) rounds 1–11 of each idle window, (ii) turrets that die while ammo is
falling for other reasons, (iii) live-but-idle turrets under the 16-ammo
threshold, and (iv) plain over-buffering of genuinely live turrets. **(iv) is
real and is probably the largest term — but it is a *sizing* argument, not a
*ghost* argument, and the ghost argument is the one the commit message leads
with.** Disclosed before the data, per the standing instrument rule.

**6. ⛔ THE SEGMENT IS INHERITED FROM THE CARRIER AND ITS COMPLEMENT MEANS
SOMETHING DIFFERENT HERE — WHICH TURNS OUT TO BE THIS LEG'S CLEANEST CELL.**
The carrier's plank is **inexpressible on three maps**: on maps of area ≤ 260 the
d² 20-100 annulus of the ENEMY core collides with our own hunt band
(`HUNT_BAND_DSQ = 41` of OUR core) and no tile satisfies both clauses. Measured
zero shredders in both arms on **antler** and **fjordgate** (the pool's two CQ
maps, `tools/overnight_read.py:76-94 map_area_class`, area ≤ 260) and ~0 on
**royale**. **And `results.tsv:beltbreak2-final` reproduced the A/A prediction on
all three at n=5,400: antler 47.78, fjordgate 51.67, royale 50.28 — every CI
containing 50 — against EXPRESSIBLE-12 at 53.89 [52.40, 55.38].**
⭐⭐ **CONSEQUENCE FOR THIS ARM, AND IT IS A GIFT: ON THOSE THREE MAPS THE
TREATMENT DIFFERS FROM THE CONTROL BY `T4_BURN_RNDS` ALONE.** The shredder plank
plants nothing there in either arm; the T4 constant is live everywhere, because
`weapons_top` is `SLOT_HOME_GUN + SLOT_FWD_GUN` and the home counter-battery path
is map-invariant. ⇒ **the complement is a SINGLE-CONSTANT cell at n = 1,080
(±2.95pp)** and the carrier's own three cells are its A/A baseline.
⛔ **AND THE PRICE, STATED PLAINLY: THIS COSTS THE PARENT PAGE'S BEST FALSIFIER.**
`PREREG-BELTBREAK2`'s segment falsifier was *"antler and fjordgate must read
~50%; if either moves, attribution is unresolved"* — the clause that could
surprise its author. **That clause is NOT available to this arm**, because a
complement move is now a *predicted* T4 effect rather than an alarm. The
replacement falsifier is signed and one-sided and is registered in `FALSIFIER`:
**a complement whose CI upper falls BELOW 50.0 convicts the constant on its own,
regardless of the pooled bar.** That is a clause that can still surprise.

**7. ⛔ TWO LIVE TOOL DEFECTS BLOCK THE OBVIOUS F1 INVOCATION, AND ONE OF THEM IS
THE DAY'S BIGGEST INSTRUMENT FACT.** OB17 checks in full are in
`FIRINGS-BEFORE-PRIMARY`; the headline:
* **`tools/dose.py` CANNOT RUN AT THE SHARD'S FIXTURE.** `grep -n 'tle\|TLE'
  tools/dose.py` returns **two lines and both are substring accidents**
  (`BOTTLENECK` in the docstring, `antler` in the MAPS default) — **there is no
  `--tle` path in the tool at all.** `fcode run`'s own default is
  `--tle 0`, i.e. **THE LIMIT IS DISABLED**
  (`.venv/lib/python3.13/site-packages/fcode/commands/run.py`,
  `@click.option("--tle", default=0, …, help="Turn time limit in ms (0 to
  disable, server uses 10)")`), while `tools/overnight.sh:138-139` runs every
  shard game at **`--tle 10`**. This independently reproduces
  `results.tsv:beltbreak2-final`'s banked finding — *"ON THE SHARD'S OWN FIXTURE
  the same registered n=60 reads DOSE DELIVERED at 1.26x/1.45x … which it does
  NOT at tle=0"*. ⇒ **F1 is registered as a direct `fcode run` battery at
  `--tle 10`, not as a `dose.py` invocation.** Routed around, not fixed.
* **`tools/dose.py:77`'s default `MAPS` is the RETIRED 8-map set** (`antler atoll
  drumlin fjordgate heart hive meander nordkap`; four are not in the live pool).
  Moot here because `dose.py` is not used, recorded because it is still live for
  anyone else.
* ⚠ **`fcode run` defaults `--replay ./replay.replay26` in the REPO ROOT** — a
  shared-file race for any parallel runner (`docs/coordination.md`
  2026-08-17T13:0xZ, item 6). **F1/F2 are registered SERIAL with an explicit
  per-game `--replay` path.**

**8. ⛔ SEED DETERMINISM IS VOID ON THIS CHASSIS, SO THE PRE-DRAFT EQUIVALENCE
EVIDENCE COMES FROM A DIFFERENT FIXTURE THAN THE SHARD.** `NOISE_ON = True`
(`bots/_v505bbdemand/doctrine.py:474`) and the spawn salt is
`random.Random().randrange(97)` — seeded from the OS, so `--seed` never reaches
spawn ordering. `results.tsv:beltbreak2-final` banked it: *"fcode run IS NOT
SEED-REPRODUCIBLE FOR THIS CHASSIS — three runs of antler seed 1 gave 45/106/74
event rows."* ⇒ **the builder's pre-draft `tools/det.py` evidence was necessarily
run at `NOISE_OFF` + `--tle 0` on local copies** (`tools/det.py` docstring:
*"flip NOISE_ON=False in local COPIES … --tle 0 removes CPU-kill
nondeterminism"*). **det and the shard are two different instruments and must
never be differenced.** No seed-matched or replay-diff equivalence claim is made
on shard games anywhere on this page.
⚠ **AND A WORDING CORRECTION THE LANE SHOULD CARRY:** the drafting brief said
*"constant-restored 0/16 identical"*; the artifact of record — commit
**`3bdb7375`**'s own message — says *"Equivalence driven both ways:
**constant-restored 0/16 non-identical**, live 8/16 differing, +538 mean
delivered-Ti."* **Those are opposite sentences and only the commit is citable.**
The commit's reading is the one that makes sense (16/16 identical when the
constant is restored = the flag-off half; 8/16 differing when live = the
positive control that makes the zero mean something). ⛔ **No `det_results.json`
or `scratchpad/*bbdemand*det*` artifact exists on disk at draft** (`ls` on
`scratchpad/` and `scratchpad/*det*` → the only det JSONs are `sealpierce_*`), so
**this evidence is cited as the builder's pre-draft check on the builder's
authority and its artifact is NOT on the tape.** That is exactly why the
shard-fixture F2 below is registered anyway rather than treated as already
answered.

**9. THE SHARD TAPE CANNOT SEE THE MECHANISM, AND A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--replay /dev/null`; the tape's columns are `ts shard game map seed seat winner
cond turns` — **no ammunition, conversion, shot, build or entity information
exists on it, in either arm.** The FIRINGS-BEFORE-PRIMARY rule
(`docs/prereg/BARS.tsv` header, research 2026-08-16T13:27:33Z) is registered here
as a **HARD SEQUENCE**:
> **F1 and F2 are RUN, and their numbers written down, BEFORE any sentence
> containing this arm's primary share is typed.** A primary typed ahead of the
> firings read is a REGISTRATION BREACH regardless of what it says, and the
> repair is an amendment chain, not a re-write. *(Precedent on the tape:
> `results.tsv:kladladder-verdict-amendment-f1f2-pending`.)*

---

## RATIFY: Hypothesis

**HYPOTHESIS.** *Halving the standing ammunition-conversion TARGET — one
integer, `T4_BURN_RNDS` 10 → 5, on the otherwise byte-identical Band-1 carrier
`bots/_v488beltbreak2` — converts a **halved burn-cap ceiling (40 × `weapons_top`
→ 20 × `weapons_top`)** into a LOCAL pooled game share vs `bots/_v468kladturbo` of
**51.33% or higher** at n = 5,400 games across all 15 corefill maps and both
seats, **via CONVERTED TITANIUM DOWN WITH SHOTS-FIRED FLAT**, and WITHOUT pushing
our own kill past r300.* Registered direction **POSITIVE**.

**Provenance of the axis, verbatim, from the sweep that closed the other one:**
*"WHY THE STACK IS STILL LIVE: the sweep ran where the reserved money's only
target was a 121-Ti sentinel. On the BELTBREAK chassis the target is a ~54-Ti
gunner with 638x/game TI refusals"* (`docs/coordination.md` 2026-08-17T12:2xZ).
**This arm takes the other half of that finding: not the RESERVE (floor) that
three fixtures refuted, but the standing TARGET, which was never manipulated.**

**The mechanism claim, stated so it can be wrong — a four-link chain, and any
link breaking is a named outcome.**
1. **THE CEILING HALVES.** `main.py:359-361` is
   `ammo_target = min(ammo_target, T4_BURN_RNDS * T4_AMMO_PER_RND * weapons_top)`.
   At `T4_AMMO_PER_RND = 4`: `40 × weapons_top` → `20 × weapons_top`. Arithmetic
   on the manipulated line, not an estimate. **It binds only while
   `weapons_top ≥ 1`** (the branch is `if T4_BURN_CAP_ON and weapons_top`), and
   the BELTBREAK magazine floor (`max(ammo_target, LOKI_BELTBREAK_AMMO = 24)`,
   `main.py:380-384`) is applied **AFTER** it — so with one counted weapon and a
   live beltbreak heartbeat the target moves 40 → 24, and without one, 40 → 20.
   **Both bind; neither reaches zero.**
2. **CONVERSION FALLS.** The top-up branch (`main.py:401-406`) fires only while
   `ammo < ammo_target`. A lower target ⇒ fewer/smaller top-ups ⇒
   **`ammo_converted` DOWN**.
3. **SHOTS DO NOT.** Conversion is same-turn usable and the branch re-arms the
   instant a shot drops `ammo` below the (lower) target, in chunks of up to 16.
   ⇒ **`shots` FLAT.** ⚠ **THE NAMED FAILURE MODE OF THIS LINK: a BURST.** Two
   sentinels firing simultaneously spend 20 in one round against a 16/turn
   top-up ceiling, so a 5-round target may **under-buffer**. The read that
   distinguishes under-buffering from healthy demand-following is registered in
   F1.
4. **THE FREED TITANIUM BUYS SOMETHING.** `ti_floor` is unchanged
   (`main.py:389`), so the money stays in the bank and the plank's own
   `LOKI_BELTBREAK_TI_FLOOR = 40` gate — the gate the sweep instrumented at
   **638×/game TI refusals** — is satisfied more often. ⇒ **plants/game
   FLAT-OR-UP** is a *prediction*, not a side-effect, and a FALL is a named
   negative.

**⇒ AND A FLAT RESULT IS INFORMATIVE ABOUT THE PLANK, NOT ABOUT THE
INSTRUMENT** — provided the F1 crossing landed. The honest-null table below
splits the two states and pre-commits both readings.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068`). There is no opponent churn to pin against and no calibration relevance to protect (CLAUDE.md: pin treatment legs, never pin calibration panels — this is neither, it is self-play).**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe; (iii) a third candidate, **HOST**, is killed by REGISTRATION rather than by measurement: this shard is registered SAME HOST (LOCAL by default), and the Addendum 11 rider (the 0.98 exemption is a WITHIN-HOST measurement; *"the seed partition makes the GAMES independent; it does not make the HOSTS exchangeable"*) is why splitting it across hosts requires an amendment typed BEFORE the first row. All surviving clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit), i.e. **NAIVE intervals are correct and marginally conservative. The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and importing them would widen every interval on this page by 24-35% for correlation measured absent.**
**ESTIMATOR: the unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Because the shard is exactly balanced on 15 maps × 2 seats × 180, the pooled share and the map-stratified equal-weight share coincide by construction; the stratified form is computed at readout as an **arithmetic consistency check only** and is not a second estimator (s28 ring-hold: four estimators inside 0.010 of one bar flipped MEET/MISS among themselves). Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never a bar — seat is worth ~7.6pp on byte-identical arms, which is why n is a multiple of 30. **Any estimate quoted at readout arrives from `tools/cluster_ci.py` (HEAD) so the interval and the point come from the same call; the pre-data half-widths on this page are closed-form Wald with DEFF 0.98 and their arithmetic is shown inline.**
**DOSE: the burn-cap CEILING on the standing ammunition target, expressed as ammunition held per counted weapon: 40 per weapon (the carrier, bots/_v488beltbreak2, whose burn constant is ten rounds) vs 20 per weapon (this arm, five rounds) — a halving that is arithmetic on the one manipulated line rather than an estimate, verified in the tree at draft (the per-round term is 4 and the cap switch is on). BOTH VERDICTS on the runtime side come from the builder's pre-draft `tools/det.py` battery, n=16 paired (map, seed, seat) triples at NOISE_OFF and --tle 0 per that tool's own precondition, quoted from commit 3bdb7375: constant-RESTORED 0/16 games non-identical (i.e. 16/16 byte-identical to the carrier — the flag-off half) and LIVE 8/16 games differing with +538 mean delivered-Ti (the flag-on positive control that makes the zero mean something). ⛔ THAT FIXTURE IS NOT THIS SHARD'S FIXTURE (see READ-BEFORE-RATIFYING #8) and no artifact of it is on disk at draft, which is why F2 re-establishes the runtime effect at --tle 10 with NOISE_ON before the primary is typed.**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:68` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30). ⛔ **5400 IS SAID EXPLICITLY BECAUSE A SOLO SHARD OTHERWISE DEFAULTS TO A 2700 TARGET, and at 2700 the bar arithmetic below is unreachable** (margin 1.33pp against a half-width of ±1.87pp).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture and no accepts count is declared. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: the tape carries an unprefixed header line under the `# FIXTURE` line, so a naive `wc -l` over-reports n by exactly one (measured on KLADLADDER, `results.tsv:kladladder-n-final-correction`). The registered denominator is **DictReader row count over non-`#` lines, cross-checked against the heartbeat's `n TARGET` and against `max(game id) + 1`.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed rows this arm publishes descriptive tallies (share, per-seat, per-map, per-class, kill-round, `cond` mix) and takes **NO bar verdict**; the one-sample half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on, so a sub-2,700 read cannot resolve its own branches. An `auto_gate` firing at CATASTROPHE@400, MARK-1000, TREND-FLOOR@1000 or COMBO-BAR@2700 is an **OPERATIONAL CANCELLATION, not a verdict**, typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 4, so a stop under that clause DOES license the Band-4 sentence at the partial n — **provided F1/F2 have been read first** and provided the partial share is disclosed as **selected-pessimistic** (a floor stop fires on a LOW PREFIX DRAW, so conditional on stopping the true share is HIGHER than the number that stopped it; expect roughly +2pp of regression — side lane s47, n=2 cases, a DIRECTION with a rough size, not a calibrated correction). ⛔ **NO OTHER CLAUSE'S CANCELLATION LICENSES ANY BAND — see READ-BEFORE-RATIFYING #1 for the COMBO-BAR case, which is the likely one at ~0.98 absent a grant.**
**BAR: 51.33. MDE: 0.00pp — THIS BAR IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE** (OB16 corollary, 2026-08-15T03:52:45Z: the standard corefill band IS `50 ± half_width` at n = 5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes no positive effect size whatsoever). n for the one exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n. ⛔ **AND PER READ-BEFORE-RATIFYING #2 IT IS A TWO-PLANK BAR: the carrier already clears it without the manipulated constant, so clearing it is NOT evidence about the constant.** **The r300 admission read below is the OTHER bar on this page and it IS sized — see `KILL-ROUND NON-REGRESSION`.**
**BASE RATE: 50.00**
**BAR SOURCE:** the house-standard corefill futility band, `50 + 1.96*sqrt(0.98*0.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `GUNFERRY`, `NEG114`, `KLADLADDER`, `SEALSENTAN`, `SEALSENTA`, `ROUTESCORE`, `BELTBREAK-EARLY` and **`BELTBREAK2` (`:312`, this arm's own carrier)**, which is what keeps this arm numerically comparable to the turret-family reads it extends. **Constructed, not observed.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own chassis base. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z, same host and fixture (`results.tsv:idnull140-cert-5400`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it. ⇒ **a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced**, which is why Band 2 is pre-registered as WEAK. ⚠ **The two cells are 1.77pp apart**, which is comfortably wider than the ~1pp this constant could plausibly move on top of the carrier — **stated before the data as the reason `#2` exists.**
**REFERENCE n: none** — the bar's comparator is a CONSTRUCTED null of 50.00 generated inside this same shard from its own 5,400 seeds; there is no external reference SAMPLE. ⛔ **AND THE CARRIER'S 53.09% IS EXPLICITLY NOT A REFERENCE SAMPLE ON THIS PAGE.** Naming `BELTBREAK2`'s tape as a reference would make the checker size 51.33 as a two-fixture comparison at ±1.87pp and correctly FAIL it — a true statement about a bar nobody registered. **The carrier-vs-this-arm difference is NOT a registered estimand** (half-width ±1.86pp at 5,400 per side against a plausible ~1pp effect). **Any carrier-vs-arm sentence at readout is DESCRIPTIVE and carries that half-width inline.**
**TREATMENT TREE: bots/_v505bbdemand**
**TREATMENT DIFF REFS: 3bdb7375^ 3bdb7375**
*(That refs pair is the commit which added the arm tree, and it is on a line of its own DELIBERATELY: `prereg_check.py`'s `git_diff_paths()` passes the WHOLE remainder of the declaration line to `git diff` as arguments, so any prose after the refs makes the command fail and the obligation-13 intersection silently reports CANNOT-COMPUTE. Found by running the checker.)*
⚠ **DISCLOSED, because the checker's path proxy passes here for a TRIVIAL reason:** that commit ADDS all four files, so every file in the tree "appears in the diff" and a path-only intersection is uninformative. **That reading is REFUSED on this page.** The substantive intersection is the **IMPORT BINDING** (`main.py:35` is `from doctrine import *`, so the name read at `main.py:359-361` binds to the one line the diff changes) **plus `cmp` cleanliness against the carrier on the other three files**, which is what makes the metric unable to read identically in the two arms. **The executable diff of record is `diff -u bots/_v488beltbreak2/doctrine.py bots/_v505bbdemand/doctrine.py`, reproduced verbatim in THE CHANGE.**
**MECHANISM METRIC READS: bots/_v505bbdemand/main.py:359-361 — the T4 burn cap `if T4_BURN_CAP_ON and weapons_top: ammo_target = min(ammo_target, T4_BURN_RNDS * T4_AMMO_PER_RND * weapons_top)`, the SINGLE site at which the manipulated constant is read at runtime (`grep -rn 'T4_BURN_RNDS' bots/_v505bbdemand/` → four hits: `doctrine.py:1989` and `main.py:355` are COMMENTS, `doctrine.py:1994` is the DECLARATION, `main.py:361` is the ONE EXECUTABLE READ). It sits on the CORE's turn inside the not-`endgame_dumped` branch and NOT on the endgame dump path (`main.py:333-343`, which uses the raw `weapons` count and is untouched). TREATMENT DIFF TOUCHES: bots/_v505bbdemand/doctrine.py. INTERSECTION: yes — by IMPORT BINDING, which is the honest form and the form the checker computes: `main.py:35` is `from doctrine import *`, so `T4_BURN_RNDS` at `main.py:361` binds to `doctrine.py:1994`, the one non-comment line the diff changes. `eco.py`, `main.py` and `raid.py` are BYTE-IDENTICAL to the carrier's (`cmp` clean on all three, verified at draft), so the only thing that can make the metric read differently between the arms is the imported constant. **The metric therefore CANNOT read identically in the two arms, which is the LOKI-18 failure this obligation exists for.**
**METRIC WINDOW: r0-r960. GATING CONSTANTS: T4_BURN_CAP_ON=True, T4_BURN_RNDS=5, T4_AMMO_PER_RND=4, T4_AMMO_IDLE_ON=True, T4_AMMO_IDLE_RNDS=12, T4_AMMO_IDLE_MIN=16, AMMO_FLOOR=16, ENDGAME_RND=960, LOKI_BELTBREAK_AMMO=24, LOKI_BELTBREAK_STALE=3, LOKI_BELTBREAK_TI_FLOOR=40. MECHANISM CAN OCCUR IN WINDOW: yes** — **exactly TWO of these are round quantities and neither closes the window from below.** `ENDGAME_RND = 960` is the only true round gate on this path and it is the window's UPPER edge, not a floor: from r960 the `ENDGAME_SWITCH_ON` branch takes over (`main.py:333-343`) and the burn cap is not reached at all, which is why the declared window ends at r960 rather than r1000. `T4_AMMO_IDLE_RNDS = 12` is a *staleness budget in rounds*, not a start gate — it can only force `weapons_top` to 0 and thereby SKIP the cap, so the window it constrains is a subset, never a prefix. Everything else is an ammunition or titanium threshold or a count. **The mechanism's first opportunity is the first round in which `weapons_top ≥ 1`, i.e. the round after our first counted gunner or sentinel is built** — which is well inside the window on every map (the chassis' median first forward turret sits at r40.0, `results.tsv:beltbreak2-final`).
⚠ **DISCLOSED IN ADVANCE, because a green tool run with warnings under it is how a warning stops being read.** `tools/prereg_check.py` on this document at draft returns **`PREREG_CHECK: OK`** with **NINE `OBLIGATION 17, PARTIAL WINDOW` warns**, and every one of them is an ARTEFACT, not a finding: (a) `check_metric_window`'s arithmetic reads every declared integer as a ROUND, so an ammunition floor of 16, a per-round burn term of 4, a staleness budget of 12, a magazine of 24 and a titanium floor of 40 all render as *"rounds r0-r15 / r0-r3 / r0-r11 / r0-r23 / r0-r39 cannot contain the mechanism"*. **Only `ENDGAME_RND = 960` is a real round quantity among the nine, and its warn is inverted — it is the window's upper edge, which is exactly why the window is declared r0-r960 and not r0-r1000.** The other eight constants are declared anyway, because an undeclared constant is the failure OB17 exists for. (b) the DISCOVERED-gate grep (`ROUND_GATE_RE`) finds **`LAUNCHER_MIN_RND`** in the metric file — `bots/_v505bbdemand/main.py:779`, value **160** (`doctrine.py:1735`) — and it is on the **LAUNCHER DEFERRAL** path, not the T4 conversion path; it is the WARN tier (elsewhere in the file, not in the metric's own function) and it is unrelated. **Checked, not waved through.**
**PLANK CLASS: ECONOMIC — a titanium-budget constant on the core's ammunition-conversion path (not a defensive turret, not a home screen, not a survival plank).** ⭐ **AND THE r300 ADMISSION READ IS REGISTERED ANYWAY, NOT CLAIMED AS INAPPLICABLE.** `PROGRAMME.md`'s `DEFENCE_ADMISSION_BAR` binds on defensive planks; the reason it is carried here regardless is that **this arm has a named, arithmetic mechanism for slowing our own kill — it reduces the standing magazine of every turret we count, and the v502 stack's LEG 3 has already driven a magazine-side change THROUGH the r300 gross backstop (median kill 259→303, dry-magazine rounds 6.3→~95, `docs/coordination.md` 2026-08-17T13:0xZ) — and a plank with a kill-delay mechanism must carry a kill-delay bar whatever its class label.** Registering it is strictly stricter than the programme requires and cannot function as a second chance to pass: **both the share bar and the r300 bar must hold.**
**KILL-ROUND NON-REGRESSION: ITT RMST₃₀₀ is the operational estimator (PROGRAMME.md:534-551, the 2026-08-16T05:36:10Z arbitration, whose vintage rule makes it binding on preregs locked from that date — this one is) — mean kill time censored at the r300 horizon over ALL games, a non-kill scoring 300, computed per side on the same rows; the bar is scored as an EXCLUSION: the 95% CI UPPER bound on (treatment RMST₃₀₀ − control RMST₃₀₀) must EXCLUDE +5.0 rounds (MDE +5.0 rounds; paired sd on the carrier's own 5,400-row tape is 85.02 rounds ⇒ half-width ±2.27 at n=5,400, so the exclusion resolves). SECOND REGISTERED FORM, both required: the ITT timely-kill-by-r300 rate (share of ALL games ending `cond == core_destroyed` with `turns <= 300`, denominator every game played, per side) — its 95% CI LOWER bound on (treatment − control) must EXCLUDE a fall of 3.0pp (MDE 3.0pp; paired sd 73.99pp on the same tape ⇒ half-width ±1.97pp at n=5,400). THIRD, and it is a DIAGNOSTIC ONLY because it carries a collider: the kill-win-CONDITIONED share and conditioned median — reported beside the two bars, never as either of them. Median kill round crossing 300 is the gross backstop.**
**PRE-STATE: the predicted-change behaviour is NOT already in the target state at lock.** Verified at draft on all three trees: `grep -n '^T4_BURN_RNDS' …` → `bots/_v468kladturbo/doctrine.py:1795` = **10**, `bots/_v488beltbreak2/doctrine.py` = **10**, `bots/_v505bbdemand/doctrine.py:1994` = **5**. ⇒ **the control AND the carrier both sit at 10 and only this arm sits at 5**; the halved ceiling is genuinely new runtime behaviour on both comparisons, not a re-weighting of existing behaviour. The T4 burn-cap PATH itself exists in the control (`bots/_v468kladturbo/main.py:349`, same expression), so this is a constant sweep on a shared code path and not a new branch — which is what makes the one-line claim meaningful. ⚠ And the OUTCOME claim is likewise not pre-satisfied: this arm's own share does not exist, and every band below — including a sign-reversed one — is a live, pre-named outcome.
**MAP SEGMENT: plank-EXPRESSIBLE maps — the 12 of 15 excluding `antler`, `fjordgate` and `royale` — mechanism reason: on maps of area ≤ 260 the d²20-100 annulus of the ENEMY core overlaps our own hunt band (`HUNT_BAND_DSQ = 41` of OUR core), so no tile satisfies both clauses of the carrier plank's siting predicate and ZERO shredders are planted in BOTH arms (measured on two independent batteries, and reproduced at n=5,400 on the carrier's own tape: antler 47.78, fjordgate 51.67, royale 50.28, every CI containing 50, against EXPRESSIBLE-12 at 53.89 [52.40, 55.38]) — EXPECTED DIRECTION POSITIVE on the segment.** This is ONE primary segment. The `CQ`/`STD`/`GRAND` split (`tools/overnight_read.py:76-94`) and the per-map table are **DESCRIPTIVE ONLY** and carry no pre-registered direction. ⛔ **AND THE COMPLEMENT IS NOT A/A FOR THIS ARM — SEE READ-BEFORE-RATIFYING #6.** Unlike its carrier, this arm's own manipulated constant is live on every map (`weapons_top` is `SLOT_HOME_GUN + SLOT_FWD_GUN` and the home counter-battery path is map-invariant), so the three complement maps are a **SINGLE-CONSTANT cell** at n = 1,080 (±2.95pp) rather than a zero cell. Its registered prediction is one-sided and appears in `FALSIFIER`. **Per OB15b/15c: the pooled bar is the bar; a pooled fail that clears on-segment RE-SCREENS as a NEW leg with its own n, never as a re-read of these rows.**
**EXPECTED DIRECTION: POSITIVE on the plank-expressible segment (12 maps, n=4,320, ±1.48pp); NOT-BELOW-50 on its complement (antler, fjordgate, royale — n=1,080, ±2.95pp), which for this arm is the single-constant cell and is registered as a one-sided falsifier, not as an A/A prediction.**
**SEGMENT VALUE CEILING: 80.00% × 3.89pp = 3.11pp.** The share is the segment's pairing weight, 12 of 15 maps = 80.00% of a balanced shard; the on-segment effect is the carrier's own measured EXPRESSIBLE-12 effect (53.89 − 50.00 = 3.89pp, `results.tsv:beltbreak2-final`). ⛔ **AND THE ARITHMETIC IS READ DIFFERENTLY HERE THAN ON THE CARRIER'S PAGE, WHICH IS THE POINT OF STATING IT.** For `BELTBREAK2` this product was a HARD CAP, because its complement was A/A by construction. **For this arm it is a cap on the SHREDDER half only**: the T4 constant contributes on the complement too, so the pooled total is `0.80 × on-segment + 0.20 × complement` and the complement term is an ADDITION, not a dilution. ⇒ **the 3.11pp is the floor of what the two-plank contrast should show if the constant does nothing, not the ceiling of what it can show.** A pooled read materially BELOW 3.11pp over 50 is therefore itself informative — it means the constant subtracted from the carrier.
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.)
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: three gates, sized separately.**
* **(a) THE SHARE BAR.** Margin 1.33pp against a one-sample half-width of ±1.320pp at n=5,400, DEFF 0.98 — resolvable, and only just. ⚠ **The slack is 0.01pp, which is `GUNAXABL`'s exact failure mode: that arm missed its keep edge by 0.0152pp — ONE GAME — on a bar with zero constructed slack.** Registered consequence: **a result within one game of the bar is reported as "the fixture cannot resolve the question", not as a verdict in whichever direction the rounding falls.** ⛔ **AND A SECOND RESOLUTION STATEMENT, per OB12 read as a bar: THE CARRIER-VS-ARM CONTRAST DOES NOT RESOLVE AT ANY n THIS LEG CAN BUY** (±1.86pp at 5,400/5,400 against a plausible ~1pp) — it is declared UNRESOLVABLE in advance and **the pre-committed handling is the RESTRICTION: no sentence attributing the pooled share to the constant.**
* **(b) THE r300 ADMISSION BAR.** RMST₃₀₀: MDE +5.0 rounds against half-width ±2.27 → resolves. Timely-kill: MDE 3.0pp against ±1.97pp → resolves. Both branches separated by construction. **Anchors (carrier's tape, quoted as anchors and NOT as this arm's prediction): RMST₃₀₀ T 268.21 vs C 275.52 — the treatment 7.30 rounds FASTER; timely-kill 30.80% [29.56, 32.03] vs 24.35% [23.21, 25.50], NON-OVERLAPPING, paired diff +6.44pp; r1000 share 11.19%.**
* **(c) THE OPERATIONAL FLOORS.** The pinned `tools/auto_gate.py` marks CATASTROPHE@400 (CI-hi < 45.0, `:244,247`), MARK-1000 / TREND-FLOOR@1000 (prefix < 52.0, `:261`), COMBO-BAR@2700 (prefix < 55.0, `:278`) and the CI rule at MARK-2700 — all Magnus's confirmed constants. Their firings are **OPERATIONAL CANCELLATIONS** that free a core, typed `cancellation`, never `verdict`, licensing no exclusion claim beyond the CATASTROPHE carve-out in CUT-SHORT. **The floors bind REMOTE too (`a50f27ef`, s48, via `tools/remote_cancel.py`), so the binding registration is not "LOCAL" but "SAME HOST" — one host, LOCAL by default; moving it is an amendment typed BEFORE the first row.** ⛔ **AND (c) IS THE GATE MOST LIKELY TO DECIDE THIS ARM'S FATE — see READ-BEFORE-RATIFYING #1: ~0.98 probability of a COMBO-BAR cancellation absent a fresh Magnus grant, and ~0.245 of a TREND-FLOOR cancellation at the n=1000 look even WITH one.**
**Everything else on this page (F1, F2, D3, D4, the seat / map / class splits) is DIAGNOSTIC and cannot rescue a failed bar. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## SEGMENT AND POPULATION — the split, its n, and the arithmetic

**Registered per-class n at the planned 5,400** (classes from
`tools/overnight_read.py:76-94 map_area_class`, from each map's own `.map26`
header, never a hardcoded size table):

| class | area | maps | **n** | half-width at DEFF 0.98 | status |
|---|---|---|---:|---|---|
| **CQ** | ≤ 260 | antler, fjordgate | **720** | **±3.62pp** | DIRECTION-ONLY |
| **STD** | 261-676 | archipelago, auroraveil, drumlin, frostgate, icefloe, nordkap, royale, yulerune | **2,880** | ±1.81pp | DIRECTION-ONLY |
| **GRAND** | > 676 | drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie | **1,800** | ±2.29pp | DIRECTION-ONLY |
| **EXPRESSIBLE-12** (the primary segment) | — | all but antler, fjordgate, royale | **4,320** | **±1.48pp** | the one segment carrying a registered direction |
| **COMPLEMENT-3** (the single-constant cell) | — | antler, fjordgate, royale | **1,080** | **±2.95pp** | a ONE-SIDED registered falsifier |

**⇒ EVERY size class is pre-labelled DIRECTION-ONLY: none of the three can
resolve the 1.33pp margin the pooled bar is built on.** Only the pooled read
(±1.32) and the 12-map segment (±1.48, marginal) can. **Registered consequence:
no class cell may be quoted as a verdict.**

**THE COMPLEMENT CELL, sized honestly.** The complement is this leg's cleanest
attribution surface and it is also **UNDERPOWERED for a difference**: against the
carrier's own three cells the half-width on the difference is **±4.17pp** at
1,080 per side. ⇒ **the complement supports a ONE-SIDED exclusion against 50.0
(±2.95pp on its own share) and NOTHING resolved about the size of the constant's
effect.** That asymmetry is registered before the data so no readout upgrades it.

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on this arm's pooled
share vs `bots/_v468kladturbo` falls BELOW 51.33.** That excludes the arm's own
bar. ⛔ **Scoped by READ-BEFORE-RATIFYING #2: failing it refutes the COMBINATION
(plank + constant) against the house band; it does not by itself convict the
constant.**

**SECOND FALSIFIER (the r300 admission bar, and it can fail on its own while the
share passes):** the 95% CI UPPER bound on (treatment − control) ITT RMST₃₀₀
fails to EXCLUDE +5.0 rounds, **or** the CI LOWER bound on the ITT
timely-kill-by-r300 difference fails to EXCLUDE a fall of 3.0pp. **Either failure
is disqualifying on its own, regardless of the share** — `PLAY_DEFENCE:
not_at_the_kill_s_expense`, and this arm's magazine-reduction mechanism is why
the bar is carried on an economic plank. ⛔ **The precedent is one session old and
it went the wrong way: the v502 stack's LEG 3 moved a magazine constant and drove
median kill 259 → 303, THROUGH the gross backstop.**

**THE SINGLE-CONSTANT FALSIFIER (the complement, and it is the clause that can
surprise the person running it):** **on `antler`, `fjordgate` and `royale` — where
the carrier plank plants nothing in either arm and the only live difference from
the control is `T4_BURN_RNDS` — the 95% CI UPPER bound on the complement share
must NOT fall below 50.0** (own-share half-width ±2.95pp at n=1,080). **If it
does, the halved target is a net cost ON ITS OWN, isolated from the shredder
plank, and that convicts the constant EVEN IF THE POOLED BAR CLEARS** — because
the pooled clearance would then be the carrier's plank carrying a losing
passenger. **Registered handling: pooled clearance + complement below 50 is
reported as `CONSTANT CONVICTED, CARRIER UNAFFECTED` and promotes the constant
NOWHERE**, while the carrier's own Band-1 status is untouched. ⚠ Conversely a
complement ABOVE 50 is weak positive evidence only (±2.95pp), never a
promotion — the asymmetry is deliberate and is registered.

**MECHANISM FALSIFIER (independent of all of the above, and it fires FIRST):**
* if **F2** shows the treatment's banded held-ammunition distribution is
  indistinguishable from the carrier's on games where `weapons_top ≥ 1`, **the
  one constant had NO runtime effect at the shard's fixture and the shard ran two
  identically-behaving bots.** This is the specific wiring null this arm is
  exposed to; it is cheap to check; and it is not hypothetical — s47's delta D2
  records a wiring null escaping demos to a 436-game shard, and the pre-draft
  equivalence evidence for THIS arm was taken at a DIFFERENT fixture
  (`NOISE_OFF`, `--tle 0`). **A share near 50 with an unmoved magazine is a
  WIRING NULL, not a finding about ammunition budgeting.** The primary is then
  reported as **NOT MEASURED**, not as a null;
* if **F1** shows `ammo_converted` per game is NOT below the carrier's outside
  the paired band, **the target reduction did not translate into less
  conversion** — the dose did not land in the ledger, and the primary is
  likewise **NOT MEASURED**;
* ⭐ **if F1 shows `ammo_converted` DOWN and `shots` DOWN TOO, this arm is the
  REFUTED FLOOR TRADE WEARING A NEW CONSTANT** — the same crossing the AMMOFLOOR
  sweep measured (*"dose 3 bought +7.8 turrets, lost 13.8 shots, and gave back
  −27.5pp"*) and the same one the floor arms measured on replays (shots −48%,
  conversion −43%). **That is a REFUTATION of the target axis, not a null**, and
  it is written down as one.
Per FIRINGS-BEFORE-PRIMARY both F reads happen BEFORE the primary is typed.

### ⭐ THE HONEST-NULL CLAUSE — pre-committed, because two of these nulls are worth different amounts

**Four states, and they are NOT the same finding. The registered discriminator is
F1+F2, read before the share.**

| state | evidence | pre-committed reading |
|---|---|---|
| **THE CONSTANT DID NOT REACH RUNTIME** | F2 shows no magazine movement on `weapons_top ≥ 1` games | **NOT MEASURED.** The leg says nothing about ammunition budgeting. The defect is wiring; the road stays open; the repair is a probe, not a verdict. |
| **THE LEDGER DID NOT MOVE** | F2 clean, F1's `ammo_converted` inside the paired band | **NOT MEASURED, AND A SIZING FINDING:** the burn cap was not the binding constraint on conversion — some other term (`AMMO_FLOOR`, the `fwd_guns` floor, `LOKI_BELTBREAK_AMMO`, or `T4_AMMO_IDLE` already zeroing `weapons_top`) was setting the target. **Cheap, real, and it names the next constant.** |
| ⭐ **THE CROSSING LANDED AND THE SHARE DID NOT** | F1 shows `ammo_converted` DOWN, `n_convert` flat-or-up, `shots` FLAT — and the pooled share is flat or the complement is flat | ⭐ **A REAL FINDING ABOUT THE PLANK, and it is bankable: the standing ammunition target was NOT overbid on this chassis — the magazine was correctly priced, exactly as the sweep concluded for the sentinel case, and the conclusion now generalises to the gunner case the sweep said was still open.** **That closes the ECO plank's last surviving axis and it must be written down before it is explained away.** ⚠ Attribution bound: it does NOT separate "the target was right" from "the freed titanium had nothing better to buy" — F1's `ti_end` / `ti_collected_end` / plants columns bear on that but do not settle it. |
| ⛔ **THE CROSSING DID NOT LAND** | F1 shows `ammo_converted` DOWN **and** `shots` DOWN | ⛔ **THE REFUTED FLOOR TRADE, RE-DISCOVERED ON THE TARGET AXIS. The axis distinction this whole page rests on is FALSE, and the honest sentence is that the two axes are the same trade at different entry points.** Reported as a REFUTATION regardless of the share, and no further ammunition-budget arm is written without a mechanism that does not go through `ammo_target`. |

**The pro case is arithmetic and the con case is three fixtures, so rows 3 and 4
are both live and they are the two readings worth a core.** That is the whole
reason this arm is worth one if it is worth one at all.

---

## READING, PRE-COMMITTED

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first
row whose condition holds is the reading. Rows are disjoint by construction.**
**Every band below is CONDITIONAL on F1/F2 having been read first and on the
r300 admission bar having HELD; an r300 failure overrides every row and the
reading is `OFF-PROGRAMME — kill delayed`, whatever the share.** ⛔ **And every
band below is a statement about the COMBINATION (`carrier + constant`) vs
`_v468kladturbo`, never about the constant alone — the constant's own reading
comes from the complement cell and from F1.**

| # | band on this arm's pooled share vs `bots/_v468kladturbo` at n = 5,400 | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE COMBINATION HOLDS ABOVE THE HOUSE BAND.** Real and resolved on this fixture. Promotes to a combination input and to a separately-registered head-to-head. ⚠ Report the size with its OB16 status: this bar's MDE is 0, so this branch may claim "we can exclude 50 vs `_v468kladturbo`" and may NOT claim any minimum effect size. ⛔ **AND IT MAY NOT CLAIM THE CONSTANT PAID** — the carrier already cleared this bar; the constant's verdict is the complement cell plus F1. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** (includes the whole [51.33, 52.4] window an A/A cell has already produced) | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Pre-registered as WEAK: `NULL125`'s byte-identical A/A read 51.04, and the two A/A cells are 1.77pp apart. ⚠ **AND ON THIS ARM BAND 2 IS ALSO A DESCRIPTIVE STEP DOWN FROM THE CARRIER'S 53.09 [51.76, 54.42]** — reported with the ±1.86pp half-width and NOT as an attribution. Rows KEPT; no ship conversation. |
| **3** | **point < 51.33 AND CI contains 50.0** | **THE COMBINATION FELL TO PARITY.** Against the carrier's Band-1 that is the informative sentence: descriptively, adding the constant moved the combination from a resolved clearance to parity, which — with the ±1.86pp caveat stated inline — is the strongest DESCRIPTIVE evidence this leg can produce that **the halved target COSTS**. Cross-read with the complement cell and F1's shots column before any sentence is typed. Does NOT license a ship. |
| **4** | **CI upper < 50.0** | **THE COMBINATION SUBTRACTS.** `T4_BURN_RNDS = 5` dies as a ship candidate and the ECO plank's target axis is closed. Attribution is bounded: this refutes *the halved standing target on this chassis*, **not** *the BELTBREAK plank* (whose own arm measured 53.09 vs the same control) and **not** *ammunition budgeting in general*. **REGISTERED CONSEQUENCE: no further `T4_BURN_RNDS` arm is written, in either direction.** |

⚠ **Nothing here treats 50.0 as a floor.** A share below 50 is a live outcome
with named mechanisms (under-buffered bursts against a 16/turn top-up ceiling; a
lower magazine on the forward sentinel that is the raid's only sustained damage;
the freed titanium buying extra units and therefore extra global cost scale) and
it is pre-named so a negative is not explained away as noise.

⛔ **AND ONE CROSS-BAND NOTE, registered so it is not improvised: a COMBO-BAR@2700
or TREND-FLOOR@1000 cancellation reaches NONE of these rows.** Per
READ-BEFORE-RATIFYING #1 those are operational stops on the CHASSIS TOTAL and the
reading is `CANCELLED — the T4_BURN_RNDS 10→5 question is UNRESOLVED and defaults
to the RESTRICTION`.

---

## FIRINGS-BEFORE-PRIMARY — the reads, with exact invocations

**Measurability is declared per read. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape happens
to carry.** ⛔ **NOTHING BELOW READS OUR OWN `print()` OUTPUT.** Every read is a
LOCAL replay decoded by our own decoder, or the LOCAL shard tape. Platform
replays strip `stdout` (30,664 of 30,664 events, `CLAUDE.md`), and
`LOKI_BELTBREAK_LOG = True` is identical in both arms here so it cannot bias this
screen — a statement about THIS CONTRAST, not about a shipped bot. **(It remains
a ship-blocker to be turned off and re-screened if this family is ever promoted.)**

### F0 — THE BATTERY. Registered ONCE; F1 and F2 are both read off it.
⛔ **NOT `tools/dose.py`.** Per READ-BEFORE-RATIFYING #7 that tool has **no
`--tle` path at all** and `fcode run` defaults to `--tle 0` (limit DISABLED),
while the shard runs `--tle 10`. The registered battery is a direct `fcode run`
loop **at the shard's own fixture**, SERIAL, with an explicit per-game replay
path (the default `--replay ./replay.replay26` in the repo root is a shared-file
race):

```
# 60 games per arm. SERIAL. 15 maps x 2 seats x 2 seeds = 60, exactly balanced on
# the live pool. Arms: TREATMENT bots/_v505bbdemand, CONTROL-BY-CONSTANT-RESTORE
# bots/_v488beltbreak2 (the CARRIER, not _v468kladturbo -- see below).
mkdir -p scratchpad/bbd_replays
for M in antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate \
         glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune; do
  for S in 852900 852901; do
    for ARM in bots/_v505bbdemand bots/_v488beltbreak2; do
      for ORD in A B; do
        T=$(basename $ARM); R=scratchpad/bbd_replays/${T}_${M}_s${S}_${ORD}.replay26
        if [[ $ORD == A ]]; then A1=$ARM; A2=bots/_v468kladturbo
        else                    A1=bots/_v468kladturbo; A2=$ARM; fi
        .venv/bin/fcode run $A1 $A2 maps/$M.map26 --seed $S --tle 10 --replay $R
      done; done; done; done
.venv/bin/python tools/corpus/replay_econ.py   scratchpad/bbd_econ.tsv   scratchpad/bbd_replays/*.replay26
.venv/bin/python tools/corpus/replay_events.py scratchpad/bbd_events.tsv scratchpad/bbd_replays/*.replay26
```
**REGISTERED SIZE: 60 games per arm, 120 total. SERIAL** (never parallel: D65 — a
16-game parallel dose check once reported the OPPOSITE of a serial one and both
were wrong; and `fcode run`'s repo-root replay default makes parallel unsafe here
for a second, independent reason).
**⛔ THE CONTROL FOR F0 IS THE CARRIER `bots/_v488beltbreak2`, NOT
`bots/_v468kladturbo`.** The mechanism question is *did `T4_BURN_RNDS` 10→5
change the ammunition ledger*, not *does the chassis differ from the incumbent*;
the carrier is the constant-restore control and the only comparison that isolates
the constant. **(The shard's own control remains `_v468kladturbo` — the two
fixtures answer different questions and must not be crossed.)**
**SEEDS: 852900-852901.** ⛔ **NO COLLISION WITH THE SHARD, and the arithmetic is
shown rather than asserted:** `tools/overnight.sh:124` is
`seed=$(( SEEDLO + n / 16 ))` — sixteen games per seed — so a 5,400-game shard at
base 852000 consumes **852000-852337**, i.e. 338 distinct seeds, and 852900 sits
562 seeds clear of the top of that range while remaining inside this arm's own
2,000-wide block. **The carrier's own demo seeds are excluded by construction:**
reusing the seeds a dose was measured on would screen an arm on the seeds that
selected it.
⛔ **OB17 CHECKS PERFORMED AT DRAFT, AND THE CLAUSE THAT COULD SURPRISE ME WAS
RUN FIRST** (per the OB17 rider: *the tell is whether the check can return an
answer that surprises the person running it*).
1. **THE CLAUSE THAT COULD GO EITHER WAY — CONSEQUENCE OF SILENT
   NON-EXECUTION — RUN FIRST, AND IT KILLED THE OBVIOUS INVOCATION.**
   `grep -n 'tle\|TLE' tools/dose.py` → two hits, **both substring accidents**
   (`BOTTLENECK`, `antler`); `fcode run --help` and
   `.venv/lib/python3.13/site-packages/fcode/commands/run.py` both give
   `--tle` **default 0 = limit disabled**. ⇒ **a `dose.py` battery would not
   fail — it would quietly measure a different fixture from the shard, and print
   the same verdict vocabulary as a correct run.** This reproduces
   `results.tsv:beltbreak2-final`'s banked finding independently, on the same
   tool, one session later. **ROUTED AROUND, NOT FIXED** (standing instruction).
2. **EXECUTING TOOLS NAMED:** `.venv/bin/fcode run` (engine), plus
   `tools/corpus/replay_econ.py` and `tools/corpus/replay_events.py` (decoders),
   all at HEAD `a7edbd0d`.
3. **THE READ PATHS EXIST IN THOSE TOOLS — checked, not assumed.**
   `replay_econ.py:131` emits
   `file team band ammo_converted n_convert shots shots_gunner shots_sentinel
   heals builds attacks deliveries tled turns_run cpu_sum_us cpu_max_us ti_end
   ammo_end ti_collected_end` with `BANDS = (r0-150, r150-200, r200-300, r300+)`,
   and its docstring names the wire sources: *"coreConvertAmmo (14) exact
   titanium→ammo conversions, per team per round"* and *"updatePlayers (6)
   per-round titanium / titaniumCollected / ammo, BOTH teams"*. `SCHEMA_VERSION =
   2`; ⛔ **write to a FRESH TSV, never append to `corpus/econ.tsv`** — the s36
   column-drift defect (31,986 19-field rows under a 17-field header) is exactly
   what `--check-header` refuses, and a fresh file is the safe form.
   `replay_events.py:157` emits `file ev rnd team kind x y d2_own d2_enemy mw mh`
   with the rotation guard at `:16,113` (a build is the FIRST `placeEntity`
   carrying an id — checked, present, recorded as a check that came out clean).
4. ⭐ **AND ONE INSTRUMENT VALIDATOR THAT IS A PHYSICAL LAW, NOT A FIXTURE, AND
   IT IS REGISTERED AS A GATE ON F1:** `ammo_converted − ammo_end` must equal
   `4 × shots_gunner + 10 × shots_sentinel` (validated 16 of 16 team-series
   within 10, `docs/coordination.md:43388`). **If that identity fails on this
   battery, F1 is an INSTRUMENT ALARM and no number off it may be quoted.**
   This is the check that makes the conversion and shot columns mutually
   corroborating rather than two hopes.

### F1 — THE LEDGER READ. **THIS IS THE REGISTERED CROSSING.** MEASURABLE off F0.
Grouped from `scratchpad/bbd_econ.tsv` by (arm, team=ours), summed over bands
except where a band is named:

| # | quantity (per game, ours) | column | **pre-registered direction, treatment vs carrier** |
|---|---|---|---|
| **a** | **converted titanium** | `ammo_converted` | ⭐ **DOWN**, outside the paired band. *This is half the crossing.* |
| **b** | **shots fired** | `shots` (+ `shots_gunner`, `shots_sentinel` split) | ⭐ **FLAT**, inside the paired band. *This is the other half, and it is the half that separates this arm from the refuted floor axis.* |
| **c** | conversion EVENT count | `n_convert` | **FLAT or UP.** ⭐ **THE DEMAND-FOLLOWING SIGNATURE, and it is the discriminator the floor axis could not produce:** a lower TARGET should convert **more often in smaller amounts** (the branch re-arms every time a shot drops `ammo` below it, in chunks of ≤16); a starved TAP converts **less often**. **`n_convert` DOWN alongside `ammo_converted` DOWN is the floor axis's signature, not this one.** |
| **d** | held magazine, per band | `ammo_end` at r0-150 / r150-200 / r200-300 | **DOWN.** Compare against the floor arms' measured `ammo_end` 14.5 → 7.5 and the sweep's 30.9 → 10.2: **this arm should move `ammo_end` down WITHOUT moving `shots`, which is precisely what those arms failed to do.** r300+ is EXCLUDED from this read (it contains the r960 `ENDGAME_SWITCH_ON` dump, which uses the raw `weapons` count and is untouched by this arm). |
| **e** | where the freed titanium went | `ti_end`, `ti_collected_end`, `builds` | **DIRECTIONAL, no bar.** `ti_collected_end` FLAT-or-UP; a FALL is a named negative (the earlier `AMMO_FLOOR = 20` arm fell 1525.2 → 1405.7, −7.8%, and that is what a lever mis-aimed at this ledger looks like). |
| **f** | shredder plants per game | `bbd_events.tsv`: `ev == BUILD`, `kind == gunner`, `d2_enemy` in the 20-100 annulus **and** `d2_own > 41` | **FLAT or UP** — link 4 of the mechanism chain: `ti_floor` is unchanged, so less conversion leaves more bank and the plank's own `LOKI_BELTBREAK_TI_FLOOR = 40` gate (instrumented at **638×/game TI refusals**) is satisfied more often. ⛔ **A FALL IS A NAMED NEGATIVE — the arm starved its own carrier — and is reported, not folded into the share.** ⚠ The band edges are read with an explicit tolerance and CALIBRATED FROM THE CONTROL ARM'S OWN DISTRIBUTION at readout: `replay_events.py:95-96,113` measures d² to a single core anchor while the bot measures to the nearest tile of the 2×2 footprint, so a plant the bot scored at d²=20 can decode a few units higher. **The DIRECTION is registered; only the cut point is deferred.** |

**⛔ DRY-TURRET ROUNDS: PARTLY NOT MEASURABLE, AND THE HALVES ARE NAMED SEPARATELY
RATHER THAN THE METRIC BEING QUIETLY RENAMED.** The brief's discriminator between
under-buffering and healthy demand-following is *dry-turret rounds SPLIT by
whether a live turret had a target that round.* Status, checked at draft:
* **NO SHIPPED TOOL COMPUTES IT.** `grep -rln 'dry_turret\|dry-turret\|dry_rounds'
  tools/` → **no match** (the one `dry` hit is an unrelated comment in
  `tools/turret_selfkill_census.py:420`). The AMMOFLOOR sweep's *"dry-turret
  rounds 26 → 181"* came from a bespoke harness that is not in `tools/`.
* **THE COUNT HALF IS ON THE WIRE BUT NOT IN ANY DECODER'S OUTPUT.**
  `updatePlayers` (field 6) carries per-round ammunition for both teams, but
  `replay_econ.py` AGGREGATES it and emits only a band-END sample
  (`c["ammo_end"] = d.get(7, 0)`, overwritten each round). ⇒ **a per-round
  `ammo == 0` series requires a NEW extractor. NOT WRITTEN BY THIS AGENT (no tool
  fixes).**
* **THE TARGET-PRESENCE HALF IS NOT MEASURABLE AT ALL on this surface.** Turret
  FACING is not in the decoded event stream (research's own stated limit,
  inherited from the carrier's page), so *"a live turret had a target"* cannot be
  reconstructed — only approximated by enemy-entity proximity, which is not
  registered as anything.
⇒ **REGISTERED SUBSTITUTE, and it is labelled a substitute: F1(c) `n_convert` +
F1(d) banded `ammo_end` + the F1(b) shot split.** Together those answer the
question the split was for — *did the magazine fall without the shooting falling*
— and they do it on shipped, header-checked decoders. **A dry-round claim may NOT
be typed off this leg.** *(One line for the builder's queue, not fixed here: a
per-round `updatePlayers` ammunition series would make the dry-round metric
executable for every future magazine arm, and it is the third arm this session to
want it.)*

### F2 — THE WIRING CHECK, AT THE SHARD'S OWN FIXTURE. MEASURABLE off F0.
**This is the read that makes the primary interpretable, and it is registered
even though the builder has pre-draft `det.py` evidence — because that evidence
was taken at `NOISE_OFF` + `--tle 0` and has no artifact on disk
(READ-BEFORE-RATIFYING #8).**
```
# from scratchpad/bbd_econ.tsv, ours only, CONDITIONED on weapons_top >= 1:
#   the conditioning set is games where our team built at least one GUNNER or
#   SENTINEL, taken from bbd_events.tsv (ev == BUILD, kind in {gunner, sentinel},
#   team == ours). The burn cap is `if T4_BURN_CAP_ON and weapons_top:` -- on a
#   game where we never counted a weapon it CANNOT bind, and pooling those games
#   dilutes the wiring signal toward zero.
#   (a) ammo_end at r0-150 / r150-200 / r200-300, treatment vs carrier
#   (b) max(ammo_end over those three bands) per game -> the CEILING read
#   (c) ammo_converted per game, treatment vs carrier
```
**Pre-registered expectations, both directional and both signed:**
* **(a)/(b) ARE THE CONSTANT'S RUNTIME EFFECT.** The treatment's banded
  held-ammunition distribution must sit **BELOW** the carrier's, and its per-game
  ceiling must sit near the **HALVED** cap. The arithmetic that makes this
  falsifiable rather than vague: conversion happens in chunks of ≤16
  (`amt = min(16, ammo_target - ammo, ti - ti_floor)`), so held ammunition can
  overshoot the target by at most ~15 outside the endgame dump. With one counted
  weapon the carrier's reachable plateau is ~40 (+≤15) and this arm's is ~20-24
  (+≤15). **The distributions must SEPARATE; if they do not, the constant did not
  reach runtime and the primary reads NOT MEASURED.**
* **(c)** must move DOWN with (a). **(a) moving without (c) is an INSTRUMENT
  ALARM** (the two are linked by the same branch), not a finding, and is reported
  as one.
⚠ **NOT AVAILABLE AS A WIRING CHECK: a seed-matched or replay-diff equivalence
claim on shard games.** `NOISE_ON = True` pins nothing (the spawn salt is
`random.Random()`, OS-seeded), so base-vs-base at one seed diverges at round 0
and three runs of one (map, seed) gave 45/106/74 event rows
(`results.tsv:beltbreak2-final`). **Pairing on this fixture controls map, seed
and opponent — never the salt.**

### D3, D4 — the outcome-shape reads. MEASURABLE, shard-native.
`cond` and `turns` are on the tape.
* **D3 — THE r300 ADMISSION BAR (see `KILL-ROUND NON-REGRESSION`).** ITT RMST₃₀₀
  per side over all 5,400 rows, plus the ITT timely-kill-by-r300 rate per side,
  plus the kill-win-conditioned share and conditioned median as DIAGNOSTICS. Both
  bars scored as exclusions off `tools/cluster_ci.py --null`.
* **D4 — COND MIX**, the share of games ending `core_destroyed` / `tiebreak` /
  `NOWINNER` per arm, and the **median kill round** as the gross backstop (median
  crossing 300 is disqualifying). Anchors from the carrier's tape:
  `core_destroyed` 4,791 / `tiebreak` 609 of 5,400; r1000 share 11.19%.
  **`R1000_IS_DEFEAT` makes a tiebreak share a cost even when the tiebreak is
  won, and a magazine-reduction arm is exactly the family that could trade kills
  for a bank** — the v502 LEG 3 precedent (median 259 → 303) is why this is a
  registered read and not a formality.

### NOT MEASURABLE on this leg — named, not silently dropped.
* **EVERY AMMUNITION, CONVERSION, SHOT AND BUILD NUMBER IS OFF THE SEPARATE F0
  BATTERY, NOT OFF THE SHARD.** `tools/overnight.sh:138-139` runs `--replay
  /dev/null`: **local corefill keeps TAPES, not REPLAYS.** The tape can carry
  share, kill round, `cond` mix and D3's rates, **and nothing else.** ⇒ **the
  shard's n = 5,400 lends the mechanism reads NONE of its power.** Anyone quoting
  a conversion figure "from the BBDEMAND shard" is quoting something that does
  not exist.
* **DRY-TURRET ROUNDS SPLIT BY TARGET PRESENCE.** See F1's block above: the count
  half needs an unwritten extractor, the target half needs facing, which is not
  decoded.
* **THE ENGINE'S OWN `get_scale_percent()`.** The decoded stream carries BUILD
  events, not the engine's scale counter; any scale statement would be a
  RECONSTRUCTION from the additive table. **Not registered on this arm** (unlike
  the carrier's page, whose plank bought turrets — this arm buys none directly).
* **PER-UNIT CPU / TLE.** Local replays carry no exec-time fields at all
  (`execTimeUs`/`tled` absent from 100% of local `BotOutput` events;
  `get_cpu_time_elapsed()` returned 0 on all 22,289 local unit-turns on the
  carrier's battery) — the s42 addendum's blind zero, on the dimension that
  silently destroys units. **The local number is UNINFORMATIVE, not clean.** The
  structural argument is what carries: the change is a comparison against a
  smaller integer inside a `min()` that already ran every round in both arms —
  **it adds no loop, no scan and no allocation.** `--tle 10` caps a timeout
  engine-side on every game of this leg.
* **BELT-KILL OR CORE-KILL ATTRIBUTION AT SHOT LEVEL.** `shots_gunner` /
  `shots_sentinel` are counts, not outcomes. A "the shots still landed where they
  mattered" claim is not available and is not made.

---

## THE CHANGE — `file:line`, carrier → treatment

**TREATMENT TREE: `bots/_v505bbdemand`** = `bots/_v488beltbreak2` plus **ONE
EXECUTABLE LINE**. Verified at draft, and re-runnable in two commands:

```
$ cmp bots/_v488beltbreak2/eco.py  bots/_v505bbdemand/eco.py   # clean
$ cmp bots/_v488beltbreak2/main.py bots/_v505bbdemand/main.py  # clean
$ cmp bots/_v488beltbreak2/raid.py bots/_v505bbdemand/raid.py  # clean
$ diff bots/_v488beltbreak2/doctrine.py bots/_v505bbdemand/doctrine.py \
      | grep -E '^[<>]' | grep -vE '^[<>] *(#| *$)'
< T4_BURN_RNDS = 10
> T4_BURN_RNDS = 5   # V505: 10->5. THE TARGET AXIS, NOT THE FLOOR AXIS -- the sweep
```
⇒ **ONE non-comment changed line, at `bots/_v505bbdemand/doctrine.py:1994`.** The
whole `diff -u` is **13 lines**: the one changed declaration plus an 8-line
trailing comment block recording the axis argument, the `weapons_top` rubble
warning, the 2.5-volley arithmetic, the same-turn-usable asymmetry and the
1,142 Ti/game replay basis. **`eco.py`, `main.py` and `raid.py` are BYTE-IDENTICAL
to the carrier's, `cmp` clean.**

**THE READ SITE, and it is exactly one:** `bots/_v505bbdemand/main.py:354-361`
```python
            # T4 BURN CAP.  Never bank more magazine than the guns we believe we
            # own could fire in T4_BURN_RNDS rounds at T4_AMMO_PER_RND each --
            # the Sentinel floor above asks for 60 on ONE turret, which is six
            # shots held in reserve, and the decoded game bought that 60 with
            # 35% of everything it mined all match.
            if T4_BURN_CAP_ON and weapons_top:
                ammo_target = min(
                    ammo_target, T4_BURN_RNDS * T4_AMMO_PER_RND * weapons_top)
```
`grep -rn 'T4_BURN_RNDS' bots/_v505bbdemand/` → **four hits, exactly one
executable**: `doctrine.py:1989` and `main.py:355` are comments,
`doctrine.py:1994` is the declaration, **`main.py:361` is the read.** The site
sits on the CORE's turn inside the `if not endgame_dumped:` branch; ⛔ **it is NOT
on the endgame dump path** (`main.py:333-343`, which uses the raw `weapons` count
and is untouched), and it is **NOT on any builder, raid or eco path** — `grep`
finds the name in no other file.

**THE TARGET LADDER AROUND IT, in order, because the cap's POSITION is what
bounds this arm's effect and a certifier should see it once:**
```
main.py:346   ammo_target = 24 if under else AMMO_FLOOR(16)
main.py:347-8 if weapons_top:  max(target, min(48, 4 * weapons_top))
main.py:352-3 if fwd_guns:     max(target, min(120, 40 + 20 * fwd_guns))
main.py:359-61 T4 BURN CAP:    min(target, T4_BURN_RNDS * 4 * weapons_top)   <-- THE ONE LINE
main.py:380-4 BELTBREAK floor: max(target, LOKI_BELTBREAK_AMMO(24)) while the heartbeat is live
main.py:389   ti_floor = 12 if (under or weapons_top) else 52   [UNCHANGED]
main.py:401-6 arm & convert:   if ammo < target and ti > ti_floor: convert min(16, ...)
```
⭐ **TWO CONSEQUENCES A CERTIFIER SHOULD CHECK RATHER THAN TAKE ON TRUST.**
(i) **The BELTBREAK floor is applied AFTER the cap**, deliberately (the tree's own
comment at `:362-379` explains why: `weapons_top` does not count beltbreak
gunners, so a bump above the cap would be multiplied by zero). ⇒ **with one
counted weapon and a live beltbreak heartbeat the target moves 40 → 24, not
40 → 20** — the arm's effective dose is smaller than the raw halving wherever the
plank is firing, and **LARGER (40 → 20) on the three complement maps where it is
not.** That is a second, independent reason the complement cell is this leg's
cleanest surface, and it points the same way as `#6`.
(ii) **`ti_floor` is untouched**, which is the structural difference from the
floor axis: the conversion branch's *reachability* is unchanged and only its
*trigger threshold* moved. **If this arm nonetheless reproduces the floor axis's
shots-down result, that is a refutation of the axis distinction itself** and the
honest-null table says so.

---

## SEEDS

**SEED BASE: 852000.** Registered worklist row (**to be appended by the builder,
not by this agent**):
```
BBDEMAND bots/_v505bbdemand bots/_v468kladturbo 5400 852000
```
**FREENESS, verified at draft on four surfaces, with a POSITIVE CONTROL RUN FIRST
so the check has been seen to produce the other verdict:**
* **POSITIVE CONTROL: `grep -c '826000' scratchpad/corefill_work.txt` → 1**, the
  `ODINVSSLEIP` row. **The grep HITS when it should hit.**
* `grep -c '852000' scratchpad/corefill_work.txt` → **0**;
  `scratchpad/fleet_queue.tsv` → **0**;
  `grep -l '852000' scratchpad/overnight/*.tsv` → **no file**;
  `grep -l '852000' docs/prereg/*.md` → **no file**.
* **Same-day and prior bases enumerated per file, not assumed** (`grep -hoE
  '\b8[0-9]{5}\b' docs/prereg/*.md | sort -u`): 810000, 812000, 814000, 816000,
  818000, 826000, 828000 (`KLADLADDER2`), 830000 (`KLADLADDER3`), 832000
  (`SEALPIERCE`), 834000 (`ECOMMIT2`), 836000 (`OPENFAST`), 838000, 840000
  (`BELTBREAK2`) — plus the two span figures `836337` and `840337`, which are
  those preregs' own consumed-range arithmetic and **not** registrations.
  ⛔ **842000-850000 are unregistered in `docs/prereg/` at draft**, so 852000
  leaves a deliberate gap rather than taking the next slot; the base is the one
  named in the drafting brief and is recorded here as chosen, not derived.
* ⭐ **CONSUMED RANGE, computed from the runner rather than assumed:**
  `tools/overnight.sh:124` is `seed=$(( SEEDLO + n / 16 ))` — **sixteen games per
  seed** — so a 5,400-game shard consumes **338 distinct seeds, not 5,400**.
  BBDEMAND at 852000 uses **852000-852337**, with 1,662 seeds of headroom inside
  its 2,000-wide block. **The F0 battery's 852900-852901 sit inside that block
  and 562 seeds clear of the shard's top.**
* ⛔ **A NAIVE GREP FOR COLLISIONS RETURNS FALSE POSITIVES on any prereg that
  verified its own seed freeness** — `PREREG-BELTBREAK2:737-743` records exactly
  this trap for 840000 against `PREREG-OPENFAST:314`. Named so no successor
  re-derives it as a conflict.

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
remote replications corroborated a null they were not allowed to rescue; and
`results.tsv:beltbreakr-final` is the same session's live example of a
replication read on its own terms).
⚠ **THE ONE AMENDMENT THIS PAGE ANTICIPATES, so it is not improvised at fire
time:** a move of this shard to a REMOTE worker. The `CLUSTER UNIT` line kills
the HOST cluster **by registration**, so a cross-host split needs an amendment
typed BEFORE the first row, naming the host term per the Addendum 11 rider. The
same-day precedent is on the tape (`scratchpad/corefill_work.txt`'s
`# MOVED 2026-08-17T05:48:58Z … per AMENDMENT 1 in each prereg`).

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one LOCAL core to n = 5,400, plus 120 serial games for F0 and the replay
decode for F1/F2.** ZERO rated ladder exposure, zero submissions, zero unrated
challenges — nothing on this page touches the platform, which is why `TARGET
BAND` is N/A rather than a number.
**⚠ AND THE EXPECTED VALUE OF THAT CORE IS DOMINATED BY READ-BEFORE-RATIFYING
#1: absent a fresh Magnus grant the arm reaches its own registered n with
probability ~0.018 at its carrier's measured share; with a grant, ~0.755 (the
TREND-FLOOR@1000 still takes ~0.245).** The cancellation is not a failure mode of
this design — it is the design working as Magnus specified it — but **it means the
core most likely buys a `cancellation` row and the F1/F2 mechanism reads, not a
bar verdict.** That trade is the builder's to make and the numbers are here so it
is made with eyes open.
⭐ **AND THE F0 BATTERY IS WORTH ITS 120 GAMES EVEN IF THE SHARD IS NEVER FIRED.**
F1's registered crossing — converted titanium DOWN with shots FLAT, and
`n_convert` FLAT-or-UP — is the whole distinction between the target axis and the
refuted floor axis, and it is answered at n=120 with shipped decoders and a
physical-law validator. **If that crossing does not land, no share is worth
buying and the road closes on 120 games instead of 5,400.** Consider firing F0
before the shard rather than beside it.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input — and the disjointness is verified, not assumed: **`eco.py` is
byte-identical to the carrier's, which is itself byte-identical to the control's**
— and (b) a separately-registered head-to-head against the live holder, which is
the pipeline step Magnus's procedure names verbatim (*"we start by testing it
against the current slot, if it beats it we can switch"*). **A local screen
against our own shipped bot is gate 1; gate-1-to-gate-2 transitivity is
UNVALIDATED in this repo (QUEUE #65: 3 concordant, 1 not), so the head-to-head is
not skippable on the strength of this number.** And `SLOT_STOP_LOSS: off` plus
the parked SWITCH step of `X3R0_SLOT_RULE` mean **the slot changes only on
Magnus's explicit word**, whatever this leg returns.

**⚠ ONE KNOWN PREFLIGHT FAIL, NAMED AND NOT FIXED:**
`.venv/bin/python tools/preflight.py bots/_v505bbdemand` FAILs on *"no PREREG.md
or README.md"*. **The carrier `bots/_v488beltbreak2` and the control
`bots/_v468kladturbo` have neither either**, so this is not a regression
introduced by this arm — it is a standing property of every tree in this family.
Reported in one line; not fixed by this agent.

**⚠ AND ONE OPEN QUESTION THIS LEG DOES NOT TOUCH, recorded because it is the
deepest thing on the board and it bears on whether this arm's premise is even
the right premise:** `docs/coordination.md` 2026-08-17T13:0xZ, finding 2 —
*"33% MORE SHREDDERS BOUGHT −5.5pp TIMELY KILLS. Plants and kills are DECOUPLED
— the bank may be a SYMPTOM, not the cause (TI still dominates the funnel AFTER
the bank was doubled)."* **If the bank is a symptom, then freeing titanium from
the ammunition ledger buys nothing no matter which axis frees it, and rows 3 and
4 of the honest-null table are BOTH explained by that rather than by anything
about ammunition.** This leg cannot separate those. **Named before the fire so it
is not discovered as a rescue afterwards.**

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read IN FULL: OB7 pre-state, OB8 denominators, OB10 identity, OB11 *verify the treatment the EXPERIMENT requires*, OB12 + its pre-committed restriction default, OB13, OB14, OB15a/b/c + the segment vocabulary and the units rider, OB16 + its `BAR = null + MDE + half_width` amendment, its **zero-MDE corollary** and its **cross-host rider**, OB17 + its *"run the clause that can surprise you"* rider — which is why the `--tle` clause was run FIRST — and the **2026-08-17T07:24:55Z addendum** that replaced the local-shard clock-2 boilerplate, quoted rather than restated) · `PROGRAMME.md` (parsed block `:6-30` — `INCUMBENT: bots/_v468kladturbo`, `PRIMARY_CURRENCY: game_share`, `WIN_RATE_IS_VERDICT: yes`, `KILL_WINDOW_RND: 250`, `R1000_IS_DEFEAT: yes`, `PLAY_DEFENCE: not_at_the_kill_s_expense`, `DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`, `SLOT_STOP_LOSS: off`, `X3R0_SLOT_RULE`; the `:530-565` r300 arbitration in full — the **05:36:10Z ITT RMST₃₀₀ resolution with its vintage rule**, the four ground-truth calibration cases, and the *"drift inside r200-300 is REPORTED, no longer DISQUALIFYING"* clause) · `docs/prereg/PREREG-BELTBREAK2-2026-08-17.md` (**THE CARRIER'S PAGE, read IN FULL** — its match structure, token order, registered machinery and caveat set are inherited here where they still apply; its COMBO precedent, its segment construction and its NOT-MEASURABLE list are re-derived for this arm rather than copied, and the three places this arm's reading DIFFERS from the carrier's are flagged inline: the complement cell's meaning, the segment-ceiling direction, and the untracked-vs-tracked arm state) · `results.tsv` rows **`beltbreak2-final`** (the carrier's Band-1 verdict: 53.09 [51.76, 54.42] n=5400, timely-kill 30.80 vs 24.35 non-overlapping, the EXPRESSIBLE-12 53.89 and the three complement cells 47.78 / 51.67 / 50.28, the `--tle 0` dose.py finding, the NOISE_ON seed-irreproducibility finding, r1000 11.28%) and **`beltbreakr-final`** (the replication's 52.01 [50.48, 53.53] at n=4138 and its BARS-row lesson — *"EVERY remote shard gets its BARS row … BEFORE its worklist row"* — which is why READ-BEFORE-RATIFYING #1 treats the row as mandatory), plus `idnull140-cert-5400`, `null125-final`, `kladladder-n-final-correction`, `kladladder-verdict-amendment-f1f2-pending`, `kladladder2-cancelled-narrowing` · `docs/coordination.md` entries **"AMMOFLOOR SWEEP"** (`:70766-70772`, 2026-08-17T12:2xZ — the five-dose sweep, the inert unarmed branch, the cost-curve/gain-curve split, dose 3's −27.5pp, the turrets-2..n vs first-turret split, the funnel's 39% ammo share, and the verbatim *"WHY THE STACK IS STILL LIVE"* paragraph that names this arm's axis) and **"v502 STACK"** (`:70774-70783`, 2026-08-17T13:0xZ — the per-leg ablation table, LEG 3's NOISE_ON replication with median kill 259→303 through the backstop, finding 2 on plants/kills being DECOUPLED, LEG 0's dead-inner-bail instrument correction and the *"L0-on and L0-off funnels are DIFFERENT INSTRUMENTS"* rule, and the `fcode run` repo-root replay race), plus `:70604` (the earlier `AMMO_FLOOR = 20` *"WRONG LEVER"* read) and `:43388` (the `ammo_converted − ammo_end == 4×gunner + 10×sentinel` physical-law validator, 16 of 16 within 10) · `docs/prereg/BARS.tsv` (**header/format ONLY, incl. the FIRINGS-BEFORE-PRIMARY rule of 2026-08-16T13:27:33Z and the `le`-direction never-stop carve-out; plus `grep -n COMBO-BAR-EXEMPT` → the TWO precedent rows `:310` BELTBREAK-EARLY and `:312` BELTBREAK2, both quoted above, and the sibling house-band rows for bar comparability. NO ROW WAS ADDED BY THIS AGENT**) · `CLAUDE.md` (the DEFF scope procedure and its direction clause; the local 0.98 exemption; the ONE GLOBAL ADDITIVE cost-scale factor; `convert_ammo`'s same-turn-usable / action-free semantics, which is link 3 of the mechanism chain; the `print()`-stripped-from-platform-replays ruling; `R1000_IS_DEFEAT`) · `bots/_v505bbdemand/{doctrine,eco,main,raid}.py` (read at draft: `doctrine.py:1981-2004` the whole T4 block and all its constants, `:474` `NOISE_ON`, `:854-855` the endgame switch, `:963` `AMMO_FLOOR`, `:1005-1013` the E1 floor family, `:1262` `LOKI2B_LIVE_CAP_ON`, `:1437-1454` the BELTBREAK constants, `:1735` `LAUNCHER_MIN_RND`; `main.py:35` the import binding, `:300-407` the entire core ammunition/target ladder, `:755` the `SLOT_HOME_GUN` monotone write, `:779` the unrelated launcher gate; `raid.py:690-800` the forward-sentinel path, `:739-745` the `SLOT_FWD_GUN` live-census-or-monotone write, `:749-800` `_live_fwd_guns` and `_live_beltbreak_guns`) · `bots/_v488beltbreak2/{doctrine,eco,main,raid}.py` (**the carrier, `cmp`'d file-by-file**) · `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` (the control: `doctrine.py:1782-1796` the same T4 block at `T4_BURN_RNDS = 10`, `main.py:349` the same read site, and the four-way `grep -c BELTBREAK` → 0/0/0/0 that establishes this is a TWO-PLANK contrast) · `scratchpad/overnight/BELTBREAK2.tsv` (the carrier's completed tape, **n=5,400 non-`#` rows** — used ONLY as a VARIANCE and ANCHOR source for the r300 sizing: ITT RMST₃₀₀ T 268.21 / C 275.52 with paired sd 85.02, ITT timely-kill 30.80% / 24.35% with paired sd 73.99pp, `cond` mix 4,791 / 609, r1000 share 11.19%, and its `# FIXTURE … start=2026-08-17T09:13:33Z` header as the clock-2 worked example; the pooled 53.09% reproduced from the row counts 2867/5400 as an instrument check against the published verdict) · `scratchpad/CONTROL_PIN` (the quoted digest) · `scratchpad/corefill_work.txt` (row format, the tail rows establishing the 812000-840000 sequence, and the `# MOVED … per AMENDMENT 1` precedent) · `scratchpad/fleet_queue.tsv` (seed and shard-id freeness) · `tools/prereg_check.py` (read for `KNOWN_KEYS`, `key_pattern`/`field`, `first_number`/`raw_number`/`int_before`, `RULES` in full incl. `_defence_bar_ok`, `check_presence`, `check_arithmetic`, `git_diff_paths`, `untracked_arm_paths`, `ROUND_GATE_RE`, `_inert`, `check_metric_window`, `check_pool_era`, `DEFF`/`CLUSTER_SYNONYM`) · `tools/auto_gate.py` (`:244-247` the catastrophe marks, `:261` `TREND_FLOOR = 52.0`, `:278` `COMBO_BAR = 55.0`, `:715` `combo_of` and its read of the TREATMENT tree's `doctrine.py`, `:906-919` the COMBO-BAR-EXEMPT citation guard and its registered purpose) · `tools/overnight.sh` (`:55-68` the live 15-map pool, `:99-103` the `START=` / `# FIXTURE` stamp, `:120-124` the row-count resume and the `SEEDLO + n/16` seed walk, `:138-139` `--replay /dev/null --tle 10`) · `tools/overnight_read.py` (`:76-94` `map_area_class`) · `tools/dose.py` (`--help` and argparse read in full; **the `--tle` absence and the retired `:77` MAPS default, both routed around**) · `.venv/lib/python3.13/site-packages/fcode/commands/run.py` (the `--tle` default of 0, read off the installed engine CLI) and `fcode run --help` · `tools/corpus/replay_econ.py` (docstring in full incl. the s36 column-drift and core-seed defects; `:131-139` `COLS`/`SCHEMA_VERSION`/`BANDS`, `:266-267` the `coreConvertAmmo` accumulation, `:329` the `ammo_end` per-band sample, `:336-392` `check_header` and the CLI) · `tools/corpus/replay_events.py` (`:16,113` the rotation guard, `:95-96` the core-anchor convention, `:157` the output columns) · `tools/det.py` (docstring in full — the `NOISE_ON=False` local-copy precondition and `--tle 0`, which is what makes the pre-draft equivalence a DIFFERENT fixture from the shard) · `tools/cluster_ci.py` and `tools/control_pin.py` and `tools/preflight.py` (invocation surfaces) · `tools/turret_selfkill_census.py:420` (the only `dry` hit in `tools/`, checked and unrelated) · git `a7edbd0d` (HEAD at draft), commit `3bdb7375` (the arm tree's own commit, message quoted verbatim), `git status --porcelain`, `git ls-files`, `git diff --name-only 3bdb7375^ 3bdb7375` · the drafting brief supplied by the builder lane s49. **No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, no tool was fixed, and no game was run. The only write was this document.**
