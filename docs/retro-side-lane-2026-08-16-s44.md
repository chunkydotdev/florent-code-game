# SIDE-LANE RETRO INSTANCE — s44, 2026-08-16

**Instrument version run: `docs/side-lane-retro.md` v1.13 (bumping to v1.14 in this same action).**
**Session 04:34Z → 07:3xZ (~3 h). Committed in the action that writes it, per the v1.3 bump rule.**
**Answered from the day's artefacts — `git log`, the coordination tail, the certificate — not memory.**

---

## Q0. WHAT DID NOT HAPPEN BECAUSE THIS LANE WAS RUNNING?

**Adopted v1.12; this is its third run. Anchoring rule holds: every item below left an artefact.**

**KILLED PRE-PUBLICATION — 5**, each with the command that killed it:
* *"auto_gate re-looks every poll after a mark (~400 looks)"* — killed by reading `:678-690`.
* *"SPAWNLKL was stopped on a 0.01pp margin"* — **true, and already fixed by the builder**; killed
  by reading past the ledger into `:700-714`.
* *"the six autonomous cancels may not have taken"* — killed by tape mtimes + `corefill_started`
  markers + zero live procs.
* *"HANDOVER names a stale holder"* — killed by reading its first four lines, which self-label as a
  cache.
* *"killing the runner strands an arm"* — killed by `^\s*trap\s`, which found the handler my
  truncated grep had missed. **This one was seconds from being sent as an operational alarm on a
  live leg.**

**REDIRECTED — 1** (v1.12.1's third bucket): *"the −40 halt is 76 min blind"* → the archive is a
30-min sawtooth, so the number was wrong **and the structural gap was real**; the flag survived at
half the magnitude.

**DECISIONS CHANGED BEFORE THEY WERE TAKEN — 4:** the leg's runner named (`unrated_run.sh`, not
`panel2_cal.sh`, which cannot pin); the post-fire `oppver` assertion registered at bar level; both
halves of the cadence rule registered rather than one; the leak check mechanised into the scheduler
instead of depending on me.

⇒ **10 items that never became findings, against 8 published errors.** Q0's premise holds a third
run: **the visible tail is not the output.**

## Q1. CONSUMPTION — acted on, or filed?

**~26 flags/certifications to two lanes. Every single one was consumed the same session** — the
tightest cadence recorded. **11 changed an outcome:** the fire order's primary estimator, the leg's
runner, the leg's shape (20 invocations), the pin assertion, the cadence rotation, the `queue_check`
ellipsis, `gate.py`'s selftest, the `auto_gate` `fired_on` column, `overnight.sh`'s false comment,
the silent-unpin guard, the scheduler heartbeat.
⭐ **And the consumption pattern that repeated: three consumers went PAST the ask** — the ellipsis
got a both-ways control I hadn't specified, the leak check was mechanised rather than documented,
and the heartbeat stated the wait-not-skip guarantee as well as the wait.

## Q2. LATENCY — did the flag beat its decision?

**Ahead in every case that mattered, and the margin was the point twice:**
* **OB17 pre-lock check ran BEFORE the prereg existed** — so the runner constraint, the silent-unpin
  path and the pin assertion were written IN rather than amended ON. **The leg's shape changed on it.**
* The collider flag beat FIRE ORDER #1's lock.
* The `−40` blindness flag beat the escalation it would have caused.
* **Behind once:** the v153 flag reached two lanes and Magnus before I corrected it ~20 min later.

## Q3. ⚠ INFERENCE PUBLISHED AS FACT — **EIGHT, AND FOR THE FIRST TIME THEY ARE ALL ONE MECHANISM**

| # | claim | surface I read | surface it was about |
|---|---|---|---|
| 1 | v153 "never held the slot" | pairings + a 5-min tape | `holder_watch`, a 120s poller |
| 2 | "no conclusion moves" | 7 shards | the board |
| 3 | pin ids "unverifiable" | `ladder_games` alone | the id's existence anywhere |
| 4 | clock 2 = +7m35s | account-wide unrated list | the leg's own accepts |
| 5 | clock 2 field | `our_matches.tsv` local write | the platform `createdAt` |
| 6 | "−40 halt is 76 min blind" | one sample of a sawtooth | the steady state |
| 7 | "the halt measures the window" | the prereg's prose | the running code |
| 8 | **D31 as a Magnus directive** | **a pronoun, vs the nearest paragraph** | **what he meant** |

⇒ **EVERY ONE IS: I READ ONE SURFACE AND REPORTED A PROPERTY OF THE SYSTEM.** Previous runs
recorded this as a mechanism among several; **s44 is the first where it is the only one.**
⛔ **#8 is the worst-sited error this lane has recorded** — not a number in a note but a **directive
attribution, verbatim, in a booted checklist**, the highest-authority object the lane can write.
⚠ **Direction: recorded as data only, per v1.13's ban on direction models.** 5 of 8 ran toward the
alarming, 3 toward the comfortable. **No mechanism proposed.**

## Q4. DID MY OWN WATCH CATCH MY OWN WORK?

**3 of 8 self-caught before publication; 3 of the 5 published self-caught afterwards; 2 needed a peer.**
⭐ **The self-catch mechanism is unchanged from v1.12 and is not diligence: an ILLEGAL VALUE.**
`0.00%` across 10,800 games · `4,755` rows in a 210-row window · a commit postdating the clock ·
`R1000_IS_DEFEAT = ABSENT` from a field I had read at boot. **Four saves, all from arithmetic that
could not be true.**
⛔ **AND THE BLIND SPOT IS EXACT: the two that escaped to a peer returned PLAUSIBLE values** — seven
shards is a plausible sample, a local write time is a plausible timestamp. **The illegal-value
mechanism cannot see a plausible wrong answer, and that is the whole of my published error set.**
⛔⛔ **WORST INSTANCE THIS RUN, AND IT IS AGAINST MY OWN INSTRUMENT: the liveness loop in the monitor
I armed to close a gap in my own watch could never fire** — its `pgrep` pattern was inside its own
command line. **My check printed `scheduler ALIVE` against a log line saying it had exited.**

## Q5. FALSE POSITIVES — what did flagging cheaply cost?

**5 killed pre-publication · 1 redirected · 8 published-and-wrong.** ⚠ **Zero caused harm, and
one nearly did:** the trap alarm would have told a live leg that a kill could strand a prototype —
**wrong, and in the direction that invites `kill -9`, the one signal that actually strands.**
⇒ **The standing sentence *"a wrong flag costs a one-line reply"* held this run** — but #7 cost a
formal ATTRIBUTION RULING in response to a defect that did not exist, **and cost nothing only
because the builder checked their own code instead of deferring.** **A wrong flag costs a reply
only when the recipient audits it.**

## Q6′. CLAIMS ABOUT ANOTHER LANE

**~9, all measured rather than relayed, all with their surface named. Zero wrong.**
⭐ **And the run's best instance is a claim I DECLINED to make: research's churn count read 0
against a claimed 17.** I was one keystroke from reporting a fabricated number against a locked
prereg minutes before firing. **The prereg writes `kladde chatte tville`; the archive carries
`kladde chatte tville (och oss)`.** Their number was exactly right.
⚠ **New this run: I corrected a FAVOURABLE claim about myself, twice** — research's "six
self-caught", then the builder's repetition of it into a wrap block. **Q6′ has only ever counted
claims about OTHERS; the flattering claim about SELF is the same object and is harder to test.**

## Q7. WHAT DID I DECLINE?

**Six, all held:** auditing `replay_view.py` and the equivariance sweep (rescope, stated not silent)
· writing the side-lane scope sentence into a charter file myself (**a lane must not widen its own
charter, especially on evidence only it holds**) · escalating the blind halt to Magnus (thresholds
stated in advance instead) · patching the gate mid-flight · committing a durable note for a clean
check with no finding (**recording every clean check IS the volume problem this lane was rescoped
for**).

## Q8. MECHANISATION — did any flag become a SCRIPT?

**SEVEN became code in one session, the joint-best rate recorded:** `auto_gate`'s `fired_on` column ·
`queue_check`'s ellipsis · `gate.py --selftest` (13 cells) · the `UNPINNED_OK` guard ·
the ELO gate's BLIND-with-age + 3-strike · the scheduler's wait heartbeat · **the per-flip leak
check, which retired ME.**
⭐ **Practice unchanged and confirmed again: flag the defect WITH its fix AND with what the fix was
verified against.** Every one that landed carried a both-ways control in the ask.

## Q9. DID MY CORRECTIONS NEED CORRECTING? — **THREE, AND ONE IS A NEW SHAPE**

1. **The 76-minute figure** — corrected 4 min later; the correction was right.
2. **Clock 2** — corrected from +7m35s to +26m39s, **then the corrected version used the wrong
   FIELD.** Two corrections, the second milder and still wrong.
3. ⛔⛔ **THE NEW SHAPE: I over-read Magnus's pronoun as a directive, struck it correctly on
   research's evidence, and then drew an UNDER-READ from the strike** — *"my wrap waits on Magnus,
   not the builder"* — **when he had given me the word directly.** ⇒ **research's formulation, and
   it is the run's best sentence: A CORRECTION INHERITS THE AMBIGUITY OF THE THING IT CORRECTS.**
   v1.4 already had *"a correction inherits the authority of having been careful"*; **this adds that
   it inherits the AMBIGUITY too**, which the earlier form did not say.

## Q10. DID I ADDRESS THE CONCERN AS STATED, OR AS I RE-STATED IT?

**Clean run, and one deliberate instance the other way:** research asked me to attack their SPEED
column hardest and I did — confirming their own suspicion rather than softening it into a
precision question, and telling them **not** to send the "bind on SPEED" recommendation. **The
denominator asymmetry reached 25% on live arms.**

---

## THE LEDGER

> **Prevented ~11 · Caused 0 · Nearly caused 1** (the trap alarm).
> **DETECTION ~22/30 · PRESCRIPTION 11/11 consumed, 3 improved by consumers.**

**Prescription is the stronger half for a fourth run.** v1.11's retirement of *"detects better than
it prescribes"* holds — **and this run the gap is at its widest in the other direction.**
