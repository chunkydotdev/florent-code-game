# CERT PLAN — what I will check about the `SCREEN-v140vs145` read

**Side lane, s41, written 2026-08-14T19:3xZ — BEFORE the number exists.**

**PRE-DECLARED BLIND, and the blindness is checkable rather than asserted:** at
the time of writing the heartbeat reads `160 / 1000 RUNNING`, ETA ~19:46:3xZ, and
**I have read only the `ts` column and the row COUNT of `V140VS145.tsv` — never
the `winner` column.** The columns I have quoted in the channel all session are
the check on that claim.

**WHY THIS FILE EXISTS.** Research's own R3 from this morning: *fix the analytic
degree of freedom before the data can vote on it.* A certification checklist
written after seeing the number is a checklist the number helped write. CAL-8
carried two candidate reference tables differing by 12pp against a 10pp threshold
for two preregs and five amendments; the fix was pinning the comparator in
writing first. **This is the same move applied to the certifier rather than the
author.**

**SCOPE — this is not a read and not a verdict.** The read is the builder's; the
slot decision is Magnus's rule executing. I certify that the read matches what
was registered. Nothing here computes a game share.

---

## A. THE REGISTERED RULE, transcribed now so it cannot be paraphrased later

From `docs/prereg/SCREEN-v140vs145-2026-08-14.md` @ `8a30265` + A1 `3a94856`
+ A2 `d8f2467` + A3 `adc82ee`:

* **`≥ 51.0` (≥510/1000) → v140 STAYS** (already live; no action).
* **`< 51.0` (≤509/1000) → REACTIVATE v145** in a safe window after an observed
  pairing, verified on the `Active bot:` line.
* **Ties-to-sitter favours v140** (current sitter); a 50.x read leaves v140 up
  **and is not relitigated**.
* **Unresolved ⇒ the RESTRICTION, i.e. the sitter keeps the slot.**
* **A3:** the mirror decides TODAY'S slot only; a `< 51.0` firing **commissions a
  matched six-cell FIELD panel under v145's tenure**, and that panel — not this
  mirror — governs the NEXT slot decision. A `≥ 51.0` read closes the question
  with no field panel owed.

## B. WHAT I WILL CHECK — each with the verdict that would FAIL it

| # | check | fails if |
|---|---|---|
| B1 | **n is exactly 1000**, counted off the tape, not read off the heartbeat | the read quotes 1000 while the tape holds fewer, or the heartbeat says COMPLETE at < 1000 |
| B2 | **the share is recomputed from the `winner` column**, not copied from a runner summary | my recount and the published share disagree |
| B3 | **the decision rule applied is the one in §A**, including the ≥/< boundary at exactly 51.0 and the ≥510/≤509 count form | a 50.x read is relitigated, or the boundary is quoted as > 51.0 |
| B4 | **ONE look.** No interim number appears anywhere in the write-up or channel | any pre-1000 share is quoted, by anyone, including me |
| B5 | **the interval uses the LOCAL DEFF 0.98**, not a platform constant | 1.434 / 1.833 / 1.529 appears on a local screen bar (would widen it 24–35% for correlation that is not there) |
| B6 | **the resolution statement is carried, not dropped**: the prereg's own `1 SE = 1.58pp at n=1000`, and its own sentence that **the 51.0 boundary cannot discriminate true-51 from true-50 at this n** | the read presents 51.x as a decisive separation |
| B7 | **A3's mirror-vs-field limit is restated in the read-out**, not left in the prereg | the number is described as measuring which bot earns more on the FIELD |
| B8 | **`< 51.0` names its consequences BOTH ways**: reactivate v145 **and** commission the field panel | only the comfortable half is executed |
| B9 | **no amendment after the read** | any commit touching the prereg postdates the first outcome read |
| B10 | **the treatment tree is unchanged since the lock** (the prereg's own VOID-on-treatment-edit clause, md5 `c4e563af`) | the md5 differs ⇒ the screen is VOID and re-pregs |

## C. TWO ASYMMETRIES I HAVE ALREADY PRE-DECLARED, so neither is discovered later

**C1. EVERY AMBIGUOUS OUTCOME NOW RESOLVES FOR v140, VIA TWO INDEPENDENT
CLAUSES** (ties-to-sitter, and unresolved⇒restriction) — and the sitter identity
flipped **after** the lock, through Magnus's rollback, i.e. through an event
outside the experiment. **The prereg already states this** (*"ties-to-sitter now
favours v140… the ~3:1 OC note carries with the sitter identity swapped"*), which
is why it is **not a flag**. It is recorded here so that if the read lands in
50.x, nobody discovers the asymmetry at read-out and argues about it then.

**C2. THE `< 51.0` BRANCH IS THE ONE THAT COSTS US SOMETHING**, so it is the one
to watch for softening. It obliges installing a competitor's bot over our own.
**B8 exists because that is where a read-out quietly loses a clause.**

## D. WHAT I WILL NOT DO

Compute the share before the builder's read · issue a slot verdict · object to
the number in either direction · treat a `PREREG_CHECK: FAIL` on this document as
a finding (**per my own `CERT-prereg-check-forced-fail-2026-08-14.md`: no real
prereg passes today, the migration has not happened, and the tool is
DRAFT-UNCERTIFIED and NOT WIRED — a red run here is formalisation, not drift**).

---

## E. ADDENDUM, pre-declared 2026-08-14T20:0xZ — STILL BLIND

**Blindness restated and checkable:** at writing, `V140VS145B.heartbeat` last read
`240/1000 RUNNING`. **I have read only `ts` and the row COUNT. The `winner` column
is unread.** The checks below are added because the plan (`d6feab7`) predates
amendments A4–A6 and the TLE-fixture finding — **a cert plan that does not cover
the amendments is a plan for a different document.**

| # | check | fails if |
|---|---|---|
| **B11** | **the read uses V140VS145B rows ONLY.** A4 voided the 480 WORKERS=40 rows for the decision while keeping them on disk as a labelled artifact | any voided row enters the tally, or n is quoted as 1000 while pooling the two shards |
| **B12** | **A6's sentence is present and in A6's words** if the reading lands in the n=3000 unresolved zone (48.23, 51.77): resolved **by DEFAULT to the sitter**, and the verdict **must say "could not separate", never "measured better"** | the n=3000 number is written as a measurement that settled the question |
| **B13** | **the ONE extension rule holds.** A5 permits exactly one extension, triggered only by a reading inside (46.9, 53.1) | a second extension is proposed, or an extension fires on a reading outside the zone |
| **B14** | **the fixture is the fixed one**: WORKERS=10 on ncpu=16 (0.63× oversubscription), and the shard is not co-resident with another at read time | the worker log shows WORKERS≠10, or §5-style concurrency recurs |

## E1. ⚠ A CARRIED CAVEAT I AM ADDING NOW SO IT CANNOT BE DISCOVERED AT READ-OUT

**THIS PAIRING HAS THE MOST EXTREME COMPUTE ASYMMETRY IN THE WHOLE BANKED SET,
AND THE TLE IS WALL-CLOCK.** From the exposure retro's own table:
`_v223sealrepair` **4,757** lines vs `_x3r0v145` **110,184** — **23×**, against
1.94× for v142/v143 and ~1.05× for the leg the 4.13pp bias proxy was measured on.

**WHY THIS IS NOT THE SAME FLAG I RAISED ON THE RETRO, and the distinction is the
whole point:**
* **A4's fix removes the CONTENTION** (2.5× → 0.63× oversubscription), and
  contention is what manufactures *spurious* TLEs. That defect is closed.
* **It does not remove the ASYMMETRY.** A bot that genuinely exceeds a 10 ms
  wall-clock budget loses its turn, and **that is the game working correctly** —
  on the platform as much as locally. **A compute-heavy bot losing turns is a
  real property of that bot, not a fixture artefact.**

⇒ **THE CAVEAT, and it is about EXTERNAL VALIDITY rather than bias:** this screen
decides a **PLATFORM** slot using a **LOCAL** fixture, and **a 23× compute
asymmetry makes the result more sensitive to the difference between the two hosts
than any previous screen has been.** The local box gives each game one core at
0.63× subscription; the platform's per-turn budget is enforced under conditions we
do not measure. **If v145 loses turns locally that it would not lose on the
platform — or vice versa — the screen is measuring our fixture as much as the
bot.**

**⛔ WHAT I AM NOT SAYING:** that the result is invalid, that the bar should move,
or that a re-run is owed. **The fixture is the fixed one and the number will be
the number.** ⇒ **The obligation is one sentence carried BESIDE the verdict:
`this is a LOCAL-fixture result on a 23× compute asymmetry with a wall-clock
turn budget; local and platform TLE behaviour are not calibrated against each
other.` Pre-declared here, blind, so it is a carried caveat and not a
post-hoc excuse if the number is unwelcome.**

**AND THE ASYMMETRY OF THAT EXCUSE IS WHY IT IS WRITTEN NOW:** the caveat helps
whichever side loses. Declared before the read, it constrains both branches
equally; produced after, it would be available only to the side that dislikes the
answer.

---

## F. CERTIFICATION OF **READ-1** (n=1000) — 2026-08-14T20:0xZ

**READ-1 CERTIFIED.** Every load-bearing number re-derived by me off
`V140VS145B.tsv` — the tape, not the read-out.

| check | result |
|---|---|
| **B1** n exactly 1000, counted off the tape | ✅ **1000 rows** |
| **B11** B-shard rows ONLY, voided 480 excluded | ✅ `shard` column = `V140VS145B` × 1000, no A-shard row present |
| **B2** share recomputed from `winner`, not copied | ✅ **T 492 / C 508 = 49.20%** — identical to the published figure |
| **B5** LOCAL DEFF 0.98, not a platform constant | ✅ **±3.07pp → [46.13, 52.27]**, reproduces the published CI to the digit |
| **B3** registered rule applied at the ≥/< 51.0 boundary | ✅ 49.20 is **BELOW** 51.0 **and inside A5's (46.9, 53.1)** ⇒ extension, **no slot branch executed** |
| **B13** ONE extension, fired only from inside the zone | ✅ fired from inside; one extension |
| **B10** VOID-on-treatment-edit | ✅ **CLEAN** — `c4e563af…` reproduced. ⚠ *my first computation used a different function and disagreed; I identified the method (`cat *.py \| md5`) before reporting anything. A hash cited in a forensic note has run the RIGHT computation — s28.* |
| **B4** one look, no interim number | ✅ 400-CATA never evaluated in flight; no pre-1000 share quoted by any lane |
| **B6** resolution statement carried | ✅ CI beside the estimate; A6's n=3000 clause in force |
| **E1** the 23× external-validity caveat | ✅ **carried VERBATIM** |
| **B14** fixture is WORKERS=10 on ncpu=16 | ⚠ **NOT VERIFIABLE FROM THIS BOX** — `worker.log` is remote and not pulled. **RELAYED by the builder, not certified by me.** Stated rather than ticked. |
| **B7 / B8 / B12** | **n/a at this read** — no slot branch executed, so the mirror-vs-field restatement and the `< 51.0` consequences are owed at the **n=3000** read, not here |

**THE SEGMENT REVERSAL IS HANDLED CORRECTLY AND IS NOT A FLAG.** The primary
segment's registered sign FAILED (predicted our share LOWER on the 9
WEAK_EXPERTS maps; observed expert-9 **54.2%** vs fallback-6 **41.8%**). ⇒ **15c's
re-screen path is NOT available**, because 15c presupposes a segment clearing **in
the predicted direction**; a segment clearing the opposite way is a failed
prediction, not a conditional plank. **The read-out says exactly this** — descriptive
only, confound stated (the fallback-6 set holds our independently-known worst
maps), *"a segment claim, if ever wanted, buys its own screen."* Checked before
flagging, per the read-the-condition-line practice.

### F1. THE MID-FLIGHT TOOL EDIT — CHECKED AGAINST THE STANDING RULE, HAZARD DOES NOT APPLY

Two tool commits landed around the extension, and this repo has a standing note
(*do not edit a script that is already running unattended; stop, edit, restart*).
Clocks, **all `TZ=UTC`**:

```
20:00:24Z   last row of the registered 1000
20:02:55Z   READ-1 taken
20:04:17Z   1d5cf34  orchestrate: reset-done (clears only the .COMPLETE marker)
```

⇒ **The shard had COMPLETED before the tooling changed** — that is precisely why a
`.COMPLETE` marker needed clearing. **No running game process was edited underneath,
and the first 1000 rows were banked and read before the commit existed.** The edit is
to ORCHESTRATION (extending a finished shard), not to the runner during a run.
**Hazard does not apply in its dangerous form.**

### F2. ⇒ **B15, PRE-DECLARED NOW FOR THE n=3000 READ** (still blind to every row past 1000)

The extension resumes the same shard through a code path that did not exist when
the first 1000 ran. **Continuity is therefore a check, not an assumption:**
* **no duplicate `game` indices** — a restart that RE-RAN rows would show them;
* **the first 1000 rows unchanged**, verified by re-tallying them: must still read
  **T 492 / C 508**;
* **seeds continue the partition** rather than restarting it;
* **row-timestamp continuity across the 1000/1001 boundary**, with any gap stated.

⚠ **AND MY OWN SLIP, RECORDED: I printed those git timestamps as `22:04:17Z` first.**
I dropped `TZ=UTC`, and `--date=format-local` renders the AMBIENT zone under a
literal `Z` — **the exact defect my own `drift_watch.sh` calls LOAD-BEARING in its
source comment**, and my second frame slip of the session. Caught by the times
disagreeing with the commit monitor's own UTC line. **A second instrument over my
own output, again — not diligence.**
