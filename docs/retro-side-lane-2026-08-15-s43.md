# SIDE-LANE RETRO — INSTANCE s43, 2026-08-15

**Instrument version at run time: `docs/side-lane-retro.md` v1.12 (FIRINGS 12).** This run makes
**FIRINGS 13.** Session 05:56Z → 16:0xZ (~10 h). **42 commits by me against 170 in the repo.**
Answered from artefacts — `git log`, the tape, the coordination channel — not from memory.

---

## Q0. WHAT DID NOT HAPPEN BECAUSE THIS LANE WAS RUNNING?

**Adopted permanently at v1.12; anchoring rule is that a withheld flag counts only if the check that
killed it left an artefact.**

**WITHHELD BEFORE PUBLICATION — 6, every one with a command behind it:**
1. *"the dashboard is dead"* (HTTP 000) — `lsof` showed the listener on `:8787`, I curled `:8765`.
2. *"`fanout.sh`'s holder check accepts any holder"* — `:52` shows `fire()` compares to `$want`;
   `gate()` is a CLI-liveness gate. **Redirected into the real find: `INCUMBENT=104` hardcoded.**
3. *"rollback failure is unwatched"* (`HOLDER_ALERT` read by zero tools) — `holder_watch` was
   running. **Redirected into: it EXITS on first change, so a leg's own activation consumes it.**
4. *"the zero-dose arms may be TLE artefacts"* — `gate.py:324`, TLE is disabled locally.
5. *"`_v320` MISSING"* — my own regex split the arm names.
6. *"restricting the primary makes the margin WORSE"* — my own print line contradicted its numbers.

**DECISIONS CHANGED BEFORE THEY WERE TAKEN — 5:** the `unrated_run` `MAIN=114` abort *before*
CAL418 fired · the bodyblock bar re-derived *before* the lock · the v140vs146 row corrected *before*
it was read as a completed screen · the six stale-treatment arms withdrawn *before* their rows were
banked · the control-pin guard built *before* a fourth fork.

**PUBLISHED ERRORS: 5** (§Q3). ⇒ **the product was ~11 things that did not happen against 5 that did.**

## Q1. CONSUMPTION — were flags acted on?

**~24 flags, and I can name no flag that was filed and ignored.** The consumption pattern is the
finding: **every single-flag message was actioned within minutes**, several inside 90 seconds
(SEALQ's stop disclosure, the four dropped caveats, the `mech_battery` reconciliation).
**Outcome-changing: ~14.** The largest: `unrated_run.sh`'s stale `MAIN` (would have aborted CAL418
at pre-flight), the v140vs146 inversion, the bodyblock bar, the control-pin guard, the escalation.

## Q2. LATENCY — did the flag beat its decision?

**Yes on all 14, and three by a margin that mattered:** `MAIN=114` flagged **~50 min before** the
leg fired · the bodyblock ceiling flagged **before ratification**, and it changed the screen's design
· the control-drift escalation landed **while 4 shards were running**, and the withdrawal followed
in 3 minutes. **⭐ The one that did NOT beat its decision is mine and is Q3-1: the `--tle` retraction
came after I had already sent the flag.**

## Q3. ⚠ INFERENCE PUBLISHED AS FACT — which surface was read, which one the claim was about

**FIVE published, and the mechanism replicates for the sixth consecutive run:**

| # | claim | SURFACE READ | SURFACE THE CLAIM WAS ABOUT |
|---|---|---|---|
| 1 | *"`d449720c` over-claims"* | the **commit subject** | `HANDOVER.md`'s **body**, which scoped it |
| 2 | *"the dose ladder ran CPU-free"* | `gate.py`'s **WARN string** (historical, another tool) | `mech_battery`'s **actual `--tle` default** |
| 3 | *"research used DEFF 1.529"* | **arithmetic that reproduced their number** | their **actual script** (p=0.5) |
| 4 | *"no past local n is trustworthy"* | `mech_battery` | **`overnight.sh`, which records NOWINNER** |
| 5 | *"`corefill` has no oversubscription gate"* | grep for **`REFUSE`** | guard 3, which **HOLDS** |

⇒ **All five are one surface adjacent to the right one.** ⭐ **AND THE NEW AXIS THIS RUN: THREE OF
THE FIVE WERE ABOUT A PEER'S WORK** (#1 a predecessor, #3 and #5 a live peer). **v1.12 found the
mechanism; s43 finds its target has moved from evidence to COLLEAGUES.**
**Direction: 4 of 5 alarming, 1 flattering.** State: **auditing** in all five — which **contradicts
v1.12's finding that surveying is the high-risk state.** ⇒ **v1.12's inversion does not replicate;
volume of auditing, not the state, predicts the count.**

## Q4. DID MY OWN WATCH CATCH MY OWN WORK?

**Self-caught 4 of 9; peers caught 5.** ⭐ **The self-catch mechanism is unchanged for the fifth run
and is not diligence — it is A SECOND INSTRUMENT IN THE SAME OUTPUT.** Twelve illegal pairs fired
today: a `stat` printing CEST under a literal `Z` beside a row's own `Z` · `pgrep -cf` printing
usage beside "0" · an 18-name blob reporting "1" beside a list of 18 · a summary saying "WORSE"
above numbers showing +0.54.
**⛔ AND THE BLIND SPOT THIS RUN NAMES: I read trees while an agent was actively restoring them.**
My 15:35Z measurement was true and false 70 seconds later. **There was an IN-FLIGHT note saying so.**
⇒ **a measurement of a moving base is a measurement onto a snapshot — my own diagnosis, applied to
me, unnoticed.**

## Q5. FALSE POSITIVES — killed / redirected / published-and-wrong

**KILLED 4 · REDIRECTED 2 · PUBLISHED-AND-WRONG 5.** The v1.12.1 REDIRECTED bucket earns itself
again: both redirects produced **better** findings than the flag they replaced (`fanout`'s stale
`INCUMBENT=104`; `holder_watch`'s one-shot exit). **Zero harm caused.**

## Q6′. CLAIMS ABOUT ANOTHER LANE

**~10 claims, 3 wrong (Q3 #1/#3/#5), all corrected in-channel within minutes, every relayed figure
carrying its owner.** ⭐ **AND THE ONE TO RECORD: I named a commit hash at the builder that had
NEVER BEEN PUSHED.** My drift watch reads **local** `git log`, so it surfaced a commit that would
never exist for them. ⇒ **push-state is part of any claim naming a hash at another lane** — banked,
and applied one hour later before naming `b25e58ac`.

## Q7. WHAT DID I DECLINE?

**Six, all held.** Declining to escalate the remote-snapshot gap **with my reasoning stated so the
builder could overrule** · declining to compute the `BUILD ∪ DEATH` bound (perspective-dependent
columns I would have guessed) · declining to re-implement `mech_battery`'s logic to test it (would
have certified my copy) · declining a second retro point-bump (the finding was already durable) ·
declining to kill s41's orphaned drift watch (not mine) · **declining to type any verdict, including
on the leg I certified.**

## Q8. MECHANISATION — did any flag become a script?

**SEVEN, the joint-best recorded:** `mech_battery` per-arm reconciliation (+ selftest, single-copy)
· `stack.py` conflict and inert-toggle refusals · `stack.py --batch` (deleted the shell loop rather
than the bug) · `auto_gate` kill switch · `auto_gate` bar plausibility bound · `unrated_run`'s
derived `MAIN` · **`control_pin.py` — the launcher now refuses a moved control.**
⭐ **The practice that produced all seven is unchanged: flag the defect WITH its fix, and name what
the fix was verified against.** **And three times the builder went past the ask** — `--batch`
deleted the failure class, and their bar-bound cells (a dropped decimal, a fraction) were better
than my suggested one.

## Q9. DID MY CORRECTIONS NEED CORRECTING?

**TWO.** (1) The `--tle` retraction: right that the caveat was owed, wrong about the mechanism, and
the builder supplied the correct one. (2) My `#70` bucket-A claim survived one correction and fell to
research's **measurement** — 30.2% of bucket A is adjacent-and-idle, so *"driving it to zero cannot
touch them"* was wrong for the arrived population. ⇒ **both were DETECTION right, MECHANISM wrong.**

## Q10. DID I ADDRESS THE CONCERN AS STATED?

**Clean run.** The one at risk: research asked to be **challenged** on the no-bar call rather than
confirmed, and I nearly confirmed. **I ran the arithmetic, found a third option neither side had
costed, and reported it dead — which is answering the question asked rather than the easy one.**

---

## THE LEDGER

> **Prevented: ~11 (6 withheld + 5 decisions changed before they were taken).
> Caused: 0. Nearly caused: 0.**

**DETECTION ~19/24 · PRESCRIPTION 7/7 CONSUMED, 3 IMPROVED BY THE CONSUMER.**
⇒ **v1.11's retirement of *"this lane detects better than it prescribes"* HOLDS for a third run:
prescription is again the stronger half.** Every prescription that shipped survived contact; the
losses are all detection (Q3).

**⭐ THE SESSION'S OWN HEADLINE, and it is not about this lane: THREE FORKS OF THE CONTROL TREE IN
ONE AFTERNOON, NONE CAUGHT BY A TOOL, THE RULE AGAINST IT WRITTEN BETWEEN THE FIRST AND THE SECOND.**
The builder wrote *"the incumbent should not be edited while rows referencing it are QUEUED"* at
14:32Z and the second fork landed at 15:32Z. **And the composition diagnosis is what made it
un-ruleable:** merge onto the then-current control — correct; revert the control when it drifted —
correct; **the two composed left six arms worse off than before either.** ⇒ **no rule phrased as
"don't do X" catches a fork built from two correct steps, which is why it ended in a refusal
(`control_pin.py`) rather than a discipline.**
