# AMENDMENT 2 to `LEG-fieldcal-2026-08-16` — **RESUMPTION AFTER THE 12:14:40Z RUNNER ABORT**

**AMENDS:** `docs/prereg/LEG-fieldcal-2026-08-16.md` (locked `43d9035f`), as further amended by
`docs/prereg/AMENDMENT-LEG-fieldcal-catchup-2026-08-16.md` (`868e3312`). Per the parent's §13,
corrections land as a **new dated document** naming the prior ones; amendments are **ADD-ONLY** and
blind to the leg's data.

**PROVENANCE:** `docs/prereg/LEG-fieldcal-2026-08-16.md` · `docs/prereg/AMENDMENT-LEG-fieldcal-catchup-2026-08-16.md` ·
`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` · `docs/research/CERT-LEG-fieldcal-2026-08-16.md` ·
`docs/research/CERT-LEG-fieldcal-observation-2026-08-16.md` · `docs/research/CERT-AMENDMENT-fieldcal-catchup-2026-08-16.md` ·
`docs/research/FIELDCAL-READER-2026-08-16.md` · `scratchpad/fieldcal_state.tsv` · `scratchpad/fieldcal_scheduler.log` ·
`tools/fieldcal_scheduler.sh` · `tools/unrated_run.sh` · `CLAUDE.md`

---

## ⭐ RATIFICATION BLOCK — RESEARCH ARM, s47. **READ THIS BEFORE THE AMENDMENT BODY.**

**DRAFTED** by a fresh opus subagent with no inherited session context beyond the `PROVENANCE` line
(the s40 rule). **RATIFIED** here by the research arm, which verified the load-bearing claims against
live surfaces rather than accepting them, and which types this lock commit itself.

### ⭐⭐ ABSTENTION — AND IT IS STRONGER THAN THE DRAFT'S, WHICH IS WHY IT IS STATED SEPARATELY
`CERT-LEG-fieldcal-observation-2026-08-16.md` §D requires the ratifying lane to **either** rest on the
structural argument **or** state on the face of the ratification that it viewed no leg games.

**THIS LANE STATES BOTH, AND THE SECOND IS BROADER THAN THE CERTIFICATE ASKS:**
* **I viewed ZERO leg games and ZERO leg replays.**
* ⭐ **I ALSO DID NOT OPEN `FIELDCAL-READER-2026-08-16.md` OR `FIELDCAL-POOLED-READ-2026-08-16.md` AT
  ANY POINT THIS SESSION** — so I have not seen interim per-cell shares, pooled figures, or any
  result-shaped number from this leg.
⛔ **THE DRAFTING AGENT DID READ `FIELDCAL-READER` §4, WHICH CONTAINS INTERIM PER-CELL SHARES AT
n=225, AND DISCLOSED IT IN THE OPEN.** ⇒ **the ratification therefore carries an abstention the draft
does not**, and the document does not have to lean on the structural argument alone. **I record this
as the reason a fresh-drafter/abstaining-ratifier split is worth its cost: neither party had to be
trusted about blindness, because between them the property is covered twice.**

### WHAT I VERIFIED MYSELF — none of it inherited, all against live surfaces
| claim | verdict |
|---|---|
| `--limit 60` on the −40 Elo halt's platform fallback | ✅ **CONFIRMED** — `fieldcal_scheduler.sh:167`. **And the hazard is worse than "a limit": `:555` computes `blind = age_min > stale_min`, i.e. blindness is judged on AGE ALONE. A read that is FRESH but TRUNCATED prints `blind=0` and a summed number.** The alarm cannot tell it is blind. |
| Round 18 was arm **A** | ✅ **CONFIRMED** — `:668` `if (( round % 2 == 0 )); then arm=A`. 18 is even. |
| Round 18 banked **zero** accepts | ✅ **CONFIRMED** — `scratchpad/arm_unrated_v140_20260816T115454Z.txt` is **0 bytes**. |
| The scheduler's STOP NOTE contradicts this | ✅ **CONFIRMED** — `:698`, `:718`, `:756` all say *"an early stop shorts B on every possible stop"*. **False for the stop that happened.** |
| Ledger/tape identity | ✅ **CONFIRMED both ways** — **17** `arm_fieldcal_*.txt` ledgers; tape `COUNT` sums **A=45, B=40 = 85**. |
| `SHIP_ALERT` is live and frees the slot | ✅ **CONFIRMED** — `RULE=SLOT FREE`, `k=63`, `net5=-29.0`, `rating=1738`, `drawdown=-64.0`. |
| The three `ourver=v152` displacement rows | ✅ **INDEPENDENTLY RE-DERIVED BY THIS LANE EARLIER TODAY** off `corpus/ladder_games.tsv` with `delta = 32(S−E)`: −2.48 / +1.56 / +2.26, **sum +1.33**, bracketed by v153 at 12:12:59Z and 13:32:59Z. Matches §7. |

⚠ **ONE RELAY-FIDELITY CORRECTION TO THE DRAFT, made because I re-read the source rather than the
summary:** the draft dates `SHIP_ALERT` to **15:02:54Z** in §4 P2b and again in its surprises. **The
row reads `2026-08-16T15:12:54Z`.** Ten minutes, substance unaffected — every other field
(`RULE=SLOT FREE`, `k=63`, `net5=-29.0`, `drawdown=-64.0`, `rating=1738`) reproduces exactly. **Recorded
because a timestamp nobody re-read is how a wrong constant enters a document that outlives its author.**

### ⚖ MY RULINGS ON THE THREE CONTESTABLE LINES THE DRAFT FLAGGED
**(i) Is §9's truncation guard a change to the HALT, or to the READ that feeds it? — RULED: THE READ.
IN SCOPE.** The threshold (−40), the population (arm-filtered rated matches since `clock2`) and the
semantics are untouched. What changes is that **a read which cannot see the whole window must declare
itself BLIND instead of reporting a sum.** That repairs an instrument's honesty; it does not move a
bar. **And the direction settles it: the guard is one-way restrictive — it can only make the halt fire
more readily or refuse to declare itself clear. It cannot license a fire that a registered gate would
have refused**, which is the exact test Amendment 1's exclusion 3 was certified on.
⇒ **RATIFIED IN SCOPE.** ⚠ **AND THE FALLBACK IF THE CERTIFIER DISAGREES IS PRE-AGREED: §9 splits into
its own dated document with its own lock, and §§0-8 and 10-12 stand unchanged without it.** No
re-litigation needed.

**(ii) Does §6's interruption sub-axis belong at all, or does the existing `time-of-day / window` axis
already cover it? — RULED: IT BELONGS, AS A SUB-AXIS, AND ITS VALUE IS THE THIRD FINDING NOT THE
FIRST TWO.** The axis does cover the block effect generically. **What it does NOT carry is the
correction in §6 finding 3 — that this abort cost arm A and widened nothing, against a STOP NOTE in
the scheduler's own output saying every stop shorts B.** ⇒ **without §6 a successor reads the note,
not the tape, and over-corrects toward B — which is precisely the fill-level reordering the s45
certification already refused as more than ADD-ONLY.** ⭐ **A disclosure that pre-empts a forbidden
action is worth its text.** **RATIFIED.**

**(iii) Should this be scoped down to a restart CERTIFICATE (§4+§5) rather than an amendment? —
RULED: NO.** §7 (the do-not-"fix" hazard) and §9 (the blind tripwire) must live in the **leg's own
paper trail**, because both are addressed to a reader of the READ-OUT, not to the operator of the
restart. A certificate is read once, before launch, and then never again. **RATIFIED AS AN AMENDMENT.**

### ⛔ WHAT THIS RATIFICATION DOES **NOT** DO
* **It does NOT open P1.** The Magnus × x3r0 team decision is **not mine and is not taken.** This
  document specifies what happens **when** the gate opens; it is **not evidence that it has.**
* **It does NOT relaunch anything.** This lane never submits, activates, fires, or runs a scheduler.
  **The relaunch is a builder action gated on P1–P12.**
* **It types no verdict on the leg.** Ratifying a registration document is not reading a result.

### ⭐ AND THE ONE THING THE LANE SHOULD ACT ON EVEN IF THE LEG NEVER RESUMES
**§9's blind-tripwire finding is not conditional on the restart.** `elo_round_gate()`'s fallback judges
blindness on **age alone** while its window is bounded by `--limit 60`. **That defect is live in the
tool right now**, and it is the same family as the two this repo has already been bitten by (the
stalled `ship_watch` printing a healthy line; the exit-code health signal). ⇒ **route it to the
builder as a tool item regardless of P1.** ⚠ Per Magnus's momentum rule it is a **tooling fix and
therefore a WRAP item, not a now item** — unless the leg resumes, in which case it becomes
loop-breaking and moves ahead of the resume.

---

## 0. WHAT THIS DOCUMENT IS, AND WHAT IT IS NOT

**THE RESUMPTION ITSELF IS NOT AN AMENDMENT. IT IS THE EXECUTION OF REGISTERED §10.4**, which
registers this leg as a two-session leg in advance — *"When session 1 ends this leg is LIVE, NOT
ABANDONED… A successor reading a half-filled tape without this paragraph would read a stopped leg"* —
and names `scratchpad/fieldcal_state.tsv` as **the handover itself**. `load_state()`
(`tools/fieldcal_scheduler.sh:225-240`) implements it as a pure function of the state tape, with zero
operator discretion.

⇒ **Continuing is the NULL ACTION. It requires no new permission and this document grants none.**
What would require justification — and does not have it — is the other branch: **discarding 425
banked games after a read-out of them exists.**

**THIS DOCUMENT ADDS EXACTLY FOUR THINGS**, each a constraint on the scheduler or the read-out, never
on a frozen object:
1. **§4** — eleven **PRECONDITIONS**, each defaulting to the restriction (OB12).
2. **§5** — **HEALTH OBSERVABLES** stated in the experiment's variables, not the implementation's (OB11).
3. **§6** — an **INTERRUPTION SUB-AXIS** under the parent's existing §6.2 heading. Disclosure only.
4. **§9** — a **TRUNCATION GUARD** on the −40 Elo halt's platform-fallback read.

**No estimator, bar, horizon, cell, pin or falsifier is touched. This document registers NO bar and
licenses NO exclusion claim of any kind (OB16).**

---

## 1. THE AMENDMENT — ADD-ONLY

> **RESUMPTION RULE.** After any abnormal termination of `tools/fieldcal_scheduler.sh`, the leg
> **RESUMES from the persisted state tape** — the same `ROUND_NUM`, the same `CLOCK2`, the same
> per-`(arm,cell)` `COUNTS` — and **never restarts from zero.** All accepts banked before the
> termination are **ADMISSIBLE and POOLED** with those banked after it, under the estimator, bar,
> horizon, cells, pins and falsifier frozen at the original lock.
>
> **The scheduler may not be relaunched until every precondition in §4 is RESOLVED IN THE
> AFFIRMATIVE. An unresolvable precondition defaults to the RESTRICTION: do not resume.**
>
> **The read-out reports the interruption under the parent's existing §6.2 imbalance heading**, as a
> named sub-axis of `time-of-day / window`, with per-arm accept counts on each side of the seam.
> **It is disclosed, never corrected.**

**SCOPE — four exclusions, so the rule cannot be stretched:**
1. **IT ADMITS, EXCLUDES, RESCUES AND VOIDS NOTHING.** Cell admissibility remains governed solely by
   §1 `CUT-SHORT` and cell voiding solely by §9.3. This rule changes **when** accepts are bought,
   never **whether** any of them counts.
2. **IT REORDERS NOTHING.** Round parity, `start_idx = (round/2) % 10`, and Amendment 1's catch-up
   prepend all run exactly as at 12:14:40Z. ⛔ **No rebalancing toward the thinner arm is registered
   and none may be improvised** — a fill-level reordering is what the s45 certification refused.
3. **EVERY EXISTING GATE STILL BINDS, UNCHANGED AND IN ORDER**: rate budget, wait-and-retry-same-cell,
   `HALT` file, −40 Elo round gate, per-flip leak check, `PIN`/`UNPINNED_OK` guards, 12-accept
   ceiling, 5-accept window budget. ⛔ **`UNPINNED_OK` must never be set.**
4. **IT MOVES NO CLOCK.** `CLOCK2 = 2026-08-16T06:25:40.381Z` is **not recaptured.** The leg era does
   not restart with the scheduler.

---

## 2. WHAT THIS AMENDMENT DOES NOT CHANGE

**UNTOUCHED, verified line by line:** the PRIMARY (exact two-sided binomial sign test over 10 pinned
cells on `sign(share_T − share_C)`, ties excluded and k reduced) · the BAR (9/10 MEET, p = 0.0215;
8/10 UNRESOLVED; ≤7/10 MISS) · the IMPOTENCE CLAUSE, MDE and power · the SECONDARY (pooled ITT
RMST₃₀₀, H = 300) · the FALSIFIER (both half-widths at 600 games/arm, POOLED only) · CELLS, PINS,
`theirver` assertions, arms and trees · BOUNDARY (240 accepts = 1,200 games) · PLANNED n · `CUT-SHORT`
· the DEFF re-measurement obligation and the direction rule · §10.3 alternation · §10.5 rated-exposure
obligations and the −40 Elo halt · Amendment 1's catch-up rule and its effective-round-9 boundary ·
`CLOCK2`.

---

## 3. BLINDNESS — STRUCTURAL, AND DISCLOSED IN THE OPEN

**Result rows exist: 85 accepts / 425 games are banked.** The drafting agent viewed zero leg games and
zero replays but **did read `FIELDCAL-READER` §4, which contains interim per-cell shares at n=225** —
stated plainly rather than avoided. **The ratifying lane read neither read-out (see the RATIFICATION
BLOCK).**

**THE STRUCTURAL ARGUMENT, which does not depend on either author:**
> **The amendment's entire content is "continue exactly as registered, having verified the machine is
> intact." Its selection domain is empty:** it selects no cell, no arm, no ordering, no inclusion, no
> exclusion, no threshold, no horizon. **There is no degree of freedom for a result to enter through.**
> The only branch a result could motivate — discarding banked games, or rebalancing toward an arm — is
> the branch this document **forbids** (§1 exclusions 1–2).

Three properties carry it: **continuation is the null action** (§10.4 + `load_state()`); **the
additions are direction-neutral by construction** (§4 can only prevent firing, §5 can only stop a run,
§6 is disclosure, §9 can only make a halt fire more readily — three of the four can only ever cost us
games); and **the one discretionary-looking choice is not discretionary** — resuming at round 18
rather than 19 is what `load_state()` reads off the tape, and **round 18 bought zero accepts** (its
outfile is 0 bytes), so resuming at 18 reproduces the exact counterfactual in which the abort never
happened.

⚠ **SCOPE OF THE CLAIM:** this establishes that the *decision to continue* is outcome-independent. It
does **not** establish that any *result* is unaffected by the interruption — that is §6's question,
and §6 answers it with counts and **discloses rather than corrects.**

---

## 4. PRECONDITIONS — TWELVE GATES. EVERY UNRESOLVED GATE DEFAULTS TO THE RESTRICTION (OB12).

*(**[V]** = verified by the drafter or ratifier against a live surface; **[F]** = executed by the
firing session at resume time.)*

**P1 — THE TEAM GATE IS OPEN. [F]** Magnus × x3r0 have decided the leg may borrow the slot again.
⛔ **NOT PRESUMED BY THIS DOCUMENT AND NOT EVIDENCE THAT IT HAS BEEN TAKEN.** UNRESOLVED ⇒ **DO NOT RESUME.**

**P2 — THE HOLDER IS READ LIVE AND `FIELDCAL_MAIN` MATCHES IT. [V/F]** Gate on the **`Active bot:`
line**, never on `$?` — this CLI exits 0 while printing `Error: True`. If the holder has changed, pass
`FIELDCAL_MAIN=<n>`; **a wrong value fails SAFE** (`unrated_run.sh` aborts and fires nothing).
Unreadable `Active bot:` line ⇒ **DO NOT RESUME.**

**P2b — THE SLOT DECISION AND THE RESUME DECISION ARE ONE DECISION. [V — live]** `corpus/SHIP_ALERT`
at **2026-08-16T15:12:54Z** reads **`RULE=SLOT FREE`**: `k=63`, `net5=-29.0`, `rating=1738`,
`drawdown=-64.0`. **The stop-loss has freed the slot.** ⇒ if the team swaps the holder while the leg
runs, `FIELDCAL_MAIN` goes stale and every subsequent invocation aborts — **fail-safe, but the leg
stops dead.** **Named, not resolved: take the resume decision and the slot decision together, or
accept that the leg halts the moment the slot moves.**

**P3 — NO HALT FILE. [V]** `scratchpad/FIELDCAL_HALT` ABSENT; `corpus/HOLDER_ALERT` ABSENT. If either
is present at resume, **DO NOT RESUME** until a human clears it **and records why** — *a halt cleared
without a reason is a tripwire disabled.*

**P4 — THE ROLLBACK-OWNERSHIP FIX BINDS THE PATH THAT WILL RUN. [V]** `unrated_run.sh` `restore()`
carries the ownership check (holder already target ⇒ no-op; holder is this run's own arm ⇒ ours to
undo; **anything else ⇒ leave the slot untouched, append `corpus/HOLDER_ALERT`, return 0**);
`fieldcal_scheduler.sh` has **zero functional restore/activate calls**; `acb28ca7` is in `origin/main`.
⇒ **single fix site, binds by construction.** Missing or reverted ⇒ **DO NOT RESUME.**

**P5 — NO ORPHAN GAMES OUTSIDE THE LEDGER. [V]** The aborted round-18 outfile is **0 bytes**;
`corpus/our_matches.tsv` newest row **11:54:41Z**. **Nothing was bought between the abort and now.**
Any accept newer than the tape ⇒ **DO NOT RESUME** until reconciled.

**P6 — STATE INTEGRITY AS AN IDENTITY, NOT AN ASSERTION. [V]** `ROUND 18`, `CLOCK2
2026-08-16T06:25:40.381Z`, `BLIND_STREAK 0`. Cross-check: **17 ledgers × 5 = 85** against tape
**A 45 + B 40 = 85**. **Exact agreement both ways.** Disagreement ⇒ **DO NOT RESUME.**

**P7 — NO SECOND SCHEDULER. [V]** `pgrep -f fieldcal_scheduler` returns nothing; it exited `rc=4
round=18` at 12:14:40Z. A live process ⇒ **DO NOT LAUNCH** — two schedulers on one tape double-fire
and blow the ceilings.

**P8 — §9.3 PIN ASSERTION RE-RUN OVER ALL 85 ACCEPTS. [F]** Any decoded `oppver` ≠ registered
`theirver` **VOIDS that cell** — recorded, k reduced, exact p recomputed; **not repaired, not
re-fired.** ⛔ **OB12 variant:** if the assertion cannot run because the archive lags (§9.5), **resume
is still permitted**, but that cell's admissibility is **UNRESOLVED and defaults to EXCLUSION**.

**P9 — THE RELAUNCH APPENDS. [F]** Use **`>>`, never `>`.** The 07:40:13Z relaunch used `>` and
destroyed rounds 0–4; which halt fired at round 3 is **permanently unrecoverable.** **Verify after
launch:** `scratchpad/fieldcal_scheduler.log` is **not shorter than 56,850 bytes** and its first line
is unchanged.

**P10 — STAMP THE RESTART BOUNDARY TO ITS OWN SIDECAR. [F]** ⛔ `scratchpad/fieldcal_amend1_effective.txt`
exists and the stamp block is **one-shot — it will NOT re-stamp.** ⇒ write
`scratchpad/fieldcal_restart2_effective.txt` carrying the resumed round (18), the restart wall clock
from `date -u`, the abort wall clock (12:14:40Z), and this amendment's commit hash. **Without a pinned
boundary §6's disclosure is uncomputable.**

**P11 — TWO-CLOCK ON THIS AMENDMENT. [F]** Clock 1 = this document's lock commit author time; clock 2
= the scheduler restart wall clock. **Clock 1 strictly earlier, gap quoted.**

**P12 — PIN AGE AND CHURN RE-READ, FOR THE RELEVANCE DISCLOSURE ONLY. [F]** ⛔ **These CANNOT move the
matched contrast — the pin neutralises churn by construction — and may NOT be used to admit, exclude
or reweight any cell.** `Erebus` and `kladde` remain **REPORTABLE, NOT POOLABLE** into any relevance
claim.

---

## 5. HEALTH OBSERVABLES — IN THE EXPERIMENT'S VARIABLES (OB11)

⛔ **`pgrep` returning a pid is NOT a health signal.** *Alive in `ps` is not verified* — and a
scheduler that silently reset to round 0 would be maximally alive.

| # | observable | failure action |
|---|---|---|
| **H1** | restart seam in the log **and** pre-restart history survives (≥ 56,850 B) | investigate before trusting any later line |
| **H2** | ⛔ **`resumed at round=18 clock2='2026-08-16T06:25:40.381Z' blind_streak=0`** — all three fields | **`round=0` ⇒ KILL THE SCHEDULER IMMEDIATELY.** Every fire under a zeroed tape re-buys banked cells and blows the ceilings **while looking like ordinary progress** |
| **H3** | round 18 logs `arm=A (v140) start_cell=farming_200s (idx 9)` and **no `CATCHUP` line** | a `CATCHUP` line here means the predicate is wrong |
| **H4** | round 19 logs `arm=B … idx 9` **and** `CATCHUP B/The_Bisons` | **falsifiable forward prediction**; absence ⇒ catch-up not firing, stop and diagnose |
| **H5** | after each cycle either `rollback confirmed: holder=…` **or** `⛔ HOLDER … NOT OURS TO DISPLACE` + a `HOLDER_ALERT` line **with no displacement** | **both are healthy** — the second is `acb28ca7` working. A *third* shape ⇒ halt |
| **H6** | `LEAK CHECK: clean` after every accept | any leak ⇒ the scheduler writes `FIELDCAL_HALT` itself; **do not clear without a written reason** |
| **H7** | tape totals and the ledger identity continue to agree | drift ⇒ stop; the read-out's denominators are compromised |
| **H8** | the `Active bot:` line reads the holder — not v140, not v154 — between invocations | an arm holding the slot at rest is the §10.5 leak scenario |

---

## 6. DID THE INTERRUPTION BIAS THE ARMS DIFFERENTIALLY? — **NO.**

**Registered as a sub-axis of the parent's existing §6.2 `time-of-day / window` axis. ONE heading.
Disclose, do not correct.**

```
cell (index)        arm A   arm B      note
Juusto        (0)     5       5
not_adgato    (1)     5       5
Erebus        (2)     5       5        HIGH-CHURN at lock (10 versions/24h)
kladde        (3)     5       5        HIGH-CHURN at lock (17 versions/24h)
gsxWins       (4)     5       5
0033          (5)     5       5
lingling_40h  (6)     5       5
HTTP_418      (7)     5       5
The_Bisons    (8)     5       0   <--  B zero
farming_200s  (9)     0       0   <--  both zero
                    ----    ----
                     45      40        = 85 accepts = 425 games (A 225, B 200)
```

1. **8 of 10 cells are EXACTLY MATCHED at 5/5 accepts.** The primary's unit of analysis is the
   **cell**, and 80% of cells carry zero arm imbalance.
2. **The 5-accept A>B differential is PRE-EXISTING**, originating at **round 3** (arm B, `not_adgato`,
   a window consumed for zero challenges) — the defect Amendment 1 exists for, already disclosed there.
3. ⭐ **THE ABORT LANDED ON AN ARM-A ROUND AND COST ARM A, NOT ARM B.** Round 18 was arm A (even
   parity, `:668`), fired `farming_200s`, banked **zero**. ⇒ **it did not widen the A−B gap by a single
   game.** ⛔ **AND THIS CONTRADICTS THE SCHEDULER'S OWN STOP NOTE** (`:698`, `:718`, `:756`: *"an
   early stop shorts B on every possible stop; CUT-SHORT shortfall is ASYMMETRIC"*). **That note is a
   sound general statement about parity and it is FALSE for the stop that actually happened.**
   **A successor who reads the note and not the tape will over-correct toward B** — a fill-level
   reordering the s45 certification already refused. **Recorded here so that cannot happen.**
4. **The imbalance is concentrated in the two highest-index cells** — the tail-cell starvation §9.6b
   predicted — and Amendment 1 heals it with **no new rule**.

**THE ONE RESIDUAL THE INTERRUPTION DOES CREATE — A TIME BLOCK.** All 425 banked games were bought
06:25:40Z → 11:54:52Z; the remainder comes from a second block. Within each block the arm/time
confound is controlled by §10.3's alternation. **But block weights differ: at completion A's pre-seam
share is 45/120 = 37.5% and B's is 40/120 = 33.3% — a 4.2 pp difference. DISCLOSED, NOT CORRECTED**,
because a matched or reweighted estimator chosen after the data is exactly the fault this discipline
exists to catch.

**READ-OUT OBLIGATION:** report, per arm, accepts and games **on each side of the seam**, seam clock
from `scratchpad/fieldcal_restart2_effective.txt`. One table, one heading, no correction.

---

## 7. ⛔⛔ A CLEANUP HAZARD THE READ-OUT MUST NOT "FIX"

**Three rated ladder matches played during the wrongful-displacement window correctly read
`ourver=v152` even though the teammate's v153 was the intended ship. THAT RECORD IS ACCURATE AND MUST
NOT BE CORRECTED.**

```
12:12:59Z  ourver=v153  I Stone                <- v153 bracketing
12:32:59Z  ourver=v152  lingling_40h           <- displacement window   -2.48
12:52:59Z  ourver=v152  opensverige - plan B   <- displacement window   +1.56
13:12:59Z  ourver=v152  HTTP 418               <- displacement window   +2.26
13:32:59Z  ourver=v153  0033                   <- v153 restored
```

**v152 is what actually played.** The per-match column records the version **that played**, not the
one that **should have**. ⇒ **the tape is CORRECT and merely looks wrong.** A successor who notices
v152 rows inside v153's tenure, concludes the column is broken, and "repairs" them **would replace a
true record with a tidy false one.** *(The poll-time-tag defect's mirror image: there the tape was
wrong and looked right.)*

**AND IT IS NOT A LEG COST.** The leg era contains **zero rated matches played by v140 or v154** ⇒ no
arm played a rated match, the leak check's `clean` is correct, and the −40 gate's arm-filtered sum of
**0.00 is a real zero rather than a blind one.** **Displacement cost priced at 3 matches, net
+1.33 Elo — independently re-derived by the ratifying lane from `ladder_games.tsv`.**

---

## 8. THE STOPPING RULE IS UNCHANGED

`CUT-SHORT` and `BOUNDARY` are frozen. **Moving either now — in the direction of "we lost three hours,
let us settle for less" — would be a frozen-object substitution made after result rows exist, which
§13 forbids.**

Honest wall-clock, stated so nobody is surprised into wanting to move it: **85 of 240 accepts banked
⇒ 155 remaining ≈ 31 rounds ≈ 10.3 h.** The `CUT-SHORT` floor needs **≥ 75 more accepts ≈ 5 h, and
only if the fill lands on the right cells.** **The interruption lengthens the floor. It does not change
what the leg may claim.**

---

## 9. TRUNCATION GUARD — THE −40 ELO HALT'S FALLBACK READ WILL GO SILENTLY BLIND INSIDE THIS LEG'S RUNTIME

`fieldcal_scheduler.sh:167` sets `PLATFORM_LIST_CMD=… --limit 60`. When the archive is stale
(`age_min > 40`), `elo_round_gate()` falls back to that live read and sums `eloDelta` over every ladder
match since `clock2`. ⛔ **The fallback is the ACTIVE path much of the time** — the archive read
`age_min=41.89` at 11:54:53Z.

**Arithmetic:** the leg era holds **25 rated matches over ~8.1 h ⇒ ~3.1/h**. The leg needs **≈10.3
more hours ⇒ ~32 more matches ⇒ an era total of ≈57**, against a hard `--limit 60`.

⇒ **The gate will cross its own read horizon while the leg is still running.** The truncation is
**silent** and **permissive** — it drops the OLDEST matches, so it can only make a cumulative loss look
smaller. ⛔ **And the ratifier's verification makes it worse than a limit: `:555` computes
`blind = age_min > stale_min`, so blindness is judged on AGE ALONE. A read that is FRESH but TRUNCATED
prints `blind=0` and a summed number.** This is `CLAUDE.md`'s *"an alarm that cannot tell it is BLIND"*,
on the tripwire Magnus's own −40 ruling put there.

> **REGISTERED: BEFORE THE LEG ERA REACHES 50 RATED LADDER MATCHES** (currently 25), the platform
> fallback must (a) raise its limit so the response demonstrably reaches back past `clock2`, **and**
> (b) **DETECT TRUNCATION** — if the OLDEST ladder match in the response is newer than `clock2`, the
> read is **TRUNCATED and must be treated as BLIND**, feeding `BLIND_STREAK` exactly as an unparseable
> read does, **never summed and never reported as `clear`.**
> **The change requires a `--selftest` cell that can return the other verdict.** Per the OB17 rider,
> **a guard that has only ever returned one verdict has not been seen to guard.**

**This does NOT block the resume** — at 25 of 60 the gate reads the full era and its arm-filtered sum
is a real 0.00. **It blocks the leg from running past ~50 era matches on an instrument that cannot
tell it has gone blind.**

---

## 10. INSTRUMENT NOTE ON `tools/prereg_check.py`

**Unchanged from Amendment 1 §7, restated so it is not rediscovered:** plain-file mode FAILS on an
addendum (it demands the 17 registration-block tokens that live in the LOCKED document and are
**deliberately not repeated here** — repeating them is how an amendment quietly restates a bar);
`--amendment` mode also FAILS, because its ADD-ONLY diff expects a **superset copy** while this repo's
convention requires a **separate dated document**. ⇒ **the repo's amendment convention and its
amendment checker disagree about file shape, so no addendum here can be machine-certified ADD-ONLY.**
**ADD-ONLY is a MANUAL certification item** against §2 and §11. Routed as a successor tool item; **not
a blocker.**

---

## 11. WHERE AN AUDITOR CAN OBJECT — IN THE OPEN

**The objection at its strongest:** *"you have added preconditions and a guard to a locked leg.
Preconditions are gates; gates are measurements; a new gate mid-leg is more than ADD-ONLY."*

The case for admissibility: **§13's frozen list is an ENUMERATION and none of its six members is
touched** (§2, checked line by line); **every addition is one-directional and restrictive** — none can
cause a fire that a registered gate would have refused, the exact test Amendment 1's exclusion 3 was
certified on; **§6 adds no estimator, only a disclosure**, under a heading the parent already
registers; and **the resume itself is registered behaviour** (§10.4), not a new rule.

⛔ **THE HONEST RESIDUAL:** if the certifying lane reads §9 as changing the **−40 halt itself** rather
than **the read that feeds it**, §9 belongs in a separate document with its own lock and the rest
stands without it. **The ratifying lane's ruling is recorded in the RATIFICATION BLOCK: it changes the
READ. The fallback is pre-agreed so no re-litigation is needed.**

---

## 12. AMENDMENT CLAUSE

This document is IMMUTABLE once locked. It amends `docs/prereg/LEG-fieldcal-2026-08-16.md` and
`docs/prereg/AMENDMENT-LEG-fieldcal-catchup-2026-08-16.md` and nothing else. Further corrections land
as a new dated document naming all three. **Nothing here may be read as licence to change the
estimator, the bar, the horizon, the cells, the pins or the falsifier — all six remain frozen at the
original lock. This document registers no bar and licenses no exclusion claim.**
