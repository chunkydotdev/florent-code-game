# SIDE-LANE RETRO — instance s35, 2026-08-13. Instrument **v1.4**, this is **FIRING 5**.

Run at Magnus's wrap call, 08:2xZ (`date -u`). Answered from the day's artefacts —
git log, the coordination appends, and the live instruments — not from memory.

> **⚠ THE STANDING CAVEAT ON THIS INSTANCE, CONCEDED BEFORE ITS NUMBERS ARE READ.**
> The meta lane's review noted that this lane's consumption ledger was computed
> *because* the review was announced — **a self-measurement under observation**.
> That is true of the ledger and it is true of this retro. The flags and the
> commits that consumed them are independently anchored in git; **the decision to
> count them at this moment was not disinterested.** Discount accordingly.

---

## Q1. CONSUMPTION — were flags ACTED ON, or filed?

**16 outcome-changing flags. All 16 consumed, each with a named commit.**
Full table at `coordination.md` (the Q1/Q2 ledger append). Six became CODE:
`ship_ledger.py`, the `submit_clean --activate` INCUMBENT guard, `dose.sh`'s tag
gate and positive control, the `cores_idle` picker fix, the lag-in-matches column,
the `--since` default.

**⭐ AND THE PER-ARTEFACT FINDING FROM s29 REPLICATED HARD.** Every single-flag
message was actioned in minutes. **The one multi-item message I sent early (the
boot note's combined flag) took 62 minutes on its second half.** Ship the live
finding as its own message; let the rest be a document.

## Q2. LATENCY — did the flag beat the decision it bore on?

**Median ≈ 2 minutes.** Every ship-critical flag beat its decision:
* the stop-loss mis-specification landed **~2.7 h before the gate could arm**;
* the two-clock certs on v122 and v123 were computed **before any match existed**
  that could have violated them;
* the `INCUMBENT`-as-editor correction landed **before the builder built it**;
* the `#18` catch landed **before the repaired picker handed it to anyone**.

**Two outliers, 47 and 62 minutes, and they share a cause: the fix was owned by a
lane other than the one flagged.** That is a routing property, not a delay.

## Q3. ⚠ INFERENCE PUBLISHED AS FACT — what was SEARCHED vs what was CLAIMED

**FIVE, and four are ONE substitution: A CLAIM ABOUT MY OWN SCOPE PUBLISHED AS A
CLAIM ABOUT THE WORLD.** Q3 asks for both fields; here they are:

| # | what I SEARCHED | what I CLAIMED | fate |
|---|---|---|---|
| 1 | `cores_idle`'s picker on row `#3` | *"the alarm names `#3`, which is withdrawn"* | it names **`#2`**; saved by a failed send |
| 2 | nothing — I did not look | *"you have the match ids; I do not"* | `meta_join` attributes them by version |
| 3 | **my own inbox** | *"the table in front of you"* about the builder's | caught by the builder |
| 4 | an arbitrary `--since 19:00Z` | **−49.61**, read as the holder's life | since-activation is **−17.50** |
| 5 | the dashboard I was writing | the local-time elo tape as a *"genuine find"* | `freshness.py` already had `assume_local`, with the identical −2.0h symptom in its own comment |

**⇒ THE MECHANISM REPLICATES FOR THE FOURTH CONSECUTIVE RUN. The DIRECTION does
not, and this run adds a new axis: #3 and #5 are claims about MY OWN CAPABILITY
and MY OWN NOVELTY**, not about a file. **The substitution is not confined to
evidence; it reaches self-description.**

**⛔ AND THE ONE THAT IS NOT IN THAT TABLE, because it is A DIFFERENT AND WORSE
FAULT — new to this lane:**
**I RESTATED THE BUILDER'S RESERVATION IN WEAKER TERMS AND THEN ADDRESSED THE
WEAKER VERSION.** They distrusted their result because *they chose when to look*
(optional stopping). I wrote that their concern *"reads as being about precision"*
and offered z≈3.56 as reassurance — **a multiplicity correction, which a fixed-n z
cannot even see.** **Worse than a scope error, because a scope error is merely
wrong while this one is COMFORTING: it hands an author permission they did not ask
for, on grounds they did not offer.** From a lane whose product is the objection,
that is the failure that matters most.
**Tagged `KIND: judgement · STATE: auditing · WHOSE HYPOTHESIS: theirs, restated
as mine`.**

## Q4. DID MY OWN WATCH CATCH MY OWN WORK?

**5 of 7 self-caught; 2 by the builder** (the inbox claim; the optional-stopping
mis-classification).
**THE MECHANISM IS UNCHANGED AND IS STILL NOT DILIGENCE — IT IS GOING TO USE THE
THING.** Running the GUNBLOCK test I had called free; opening `target_value.py`;
computing the binomial band; going to build the `INCUMBENT` fix; **and grepping
for prior derivations before publishing the `p_null` duplicate — that last one
found the cumulative-vs-rolling-5 discrepancy, which was the session's
highest-value flag. The near-duplicate WAS the instrument.**

**⛔ AND THE BLIND SPOT THIS RUN EXPOSED, WHICH THAT MECHANISM CANNOT REACH:
a claim about someone else's inbox has NO PRIMARY TO OPEN.** *Go and use the
thing* fails by construction there. **The fix is not a better check; it is not
making the claim** — the substance was identical without the sentence.

## Q5. FALSE POSITIVES — what did flagging cheaply cost?

**3 wrong or withdrawn. ZERO harm, second consecutive clean run.**
* the borrowed-band suspicion — **dropped before publishing**, unfounded (±1.33pp
  is the binomial half-width and transfers anywhere at that n);
* the GUNBLOCK ambiguity — real, but the builder showed the sibling arm's full-n
  null made resolving it worthless. **Dropped on their evidence.**
* the `PROGRAMME.md` staleness flag — I went looking to flag it stale and it was
  **correct but uncommitted**, a different and more urgent defect.

**The cause is structural and is why the policy survives: every flag shipped with
BOTH BRANCHES AND A DISCRIMINATING TEST**, so a wrong one cost a reply.
**⚠ SUNSET NOTE: Q5 has now gone TWO runs at zero harm** (s33 had two). v1.4 asked
whether it has become a subset of Q9. **This run says NO — it caught the
dropped-before-publishing case, which Q9 cannot see because it never became a
correction.** Keep it.

## Q6′. CLAIMS ABOUT ANOTHER LANE — including relayed FIGURES

**~12 claims about peers' work or output. ONE wrong** — *"the table in front of
you"*, a claim about the builder's inbox inferred from mine. **Every relayed
FIGURE carried its owner and window** (research's p=0.162 simulation, their
gsxWins 541-match control, their log-rank z=−0.22, the builder's 5,408/8×676
recount). **Conduct claims: ZERO, sixth consecutive run** — the s28 rule holds
after the question measuring it was struck.

**⭐ AND ONE CLAIM ABOUT A PEER THAT WAS WORTH MAKING: I recorded the builder's own
disclosure that the `submit_clean` guard came out read-only "from a local habit and
a fresh memory", not from seeing the trap.** Correct-by-habit and
correct-by-principle are identical in the artefact and different in durability.
**Banking a peer's honest self-report is a use of this question I had not made
before.**

## Q7. WHAT DID I DECLINE, and was declining right?

**Six, all held.**
1. **Running `dose.sh`** — it spends games. Audited by reading. *(Right: the audit
   found both defects anyway.)*
2. **Running `submit_clean.py`** — it ships. Read-only audit even for the guard I
   had specified.
3. **Editing `PROGRAMME.md`** — Magnus-only, three times over, including when I
   knew the exact lines.
4. **GUNBLOCK** — dropped on the builder's evidence rather than defending my own
   open question. *(A decline to CONTINUE, which is distinct from a decline to act.)*
5. **Verdicting on R1** — supplied the number, refused the recommendation. This
   lane issues no verdicts, least of all about its own charter.
6. **⭐ NEW TYPE: declining to INTERPRET a favourable number.** v123 read +36.99 at
   k=4 under a look schedule I had just proposed. **I reported it as progress and
   did not read it.** Distinct from declining to act or to tell — it is declining
   to CONCLUDE, and it is the only one of the six that constrained me rather than
   protecting someone else.

## Q8. MECHANISATION — did any flag become a SCRIPT?

**SIX, the highest recorded** (s28 3 → s32 6 → s33 10 → s34 → s35 **6 in code +
2 promoted rules**):
`tools/ship_ledger.py` · the `submit_clean --activate` INCUMBENT guard ·
`dose.sh`'s tag-existence gate + `exit 5` · `cores_idle` calling
`queue_check.unblocked()` · the lag-in-matches column · the `--since` default.
Plus **D31 and D32 promoted into the booted drift-watch**, and `tools/dash`.

**THE PRACTICE IS UNCHANGED AND CONFIRMED: FLAG THE DEFECT WITH ITS FIX, AND NAME
WHAT THE FIX WAS VERIFIED AGAINST.** Every one of the six named a file, a line,
and a cell that must come out the other way.

## Q9. DID MY CORRECTIONS NEED CORRECTING?

**FOUR. Two caught by me before or at the point of build; two by the builder.**
1. **GUNBLOCK's discriminating test** — I called it *"free and retrospective"*, ran
   it, and it does not discriminate (no facing on the wire; 3.5 barriers/side/game
   against a 0.20 dose). **Superseded in the record.**
2. **The `INCUMBENT` fix** — proposed as *"the ship procedure UPDATES the field"*,
   which conflicts with that file's Magnus-only rule. **Corrected to a GUARD before
   the builder built it.**
3. **The optional-stopping reassurance** — see Q3.
4. **The elo local-time "find"** — already solved in `freshness.py`.

**⇒ THE s34 SPLIT HOLDS AND IS NOW MEASURED: of 16 outcome-changing flags the
DEFECT WAS REAL IN 16. Of the FIXES I named, 2 needed correcting.**
**DETECTION 16/16. PRESCRIPTION 14/16.**

---

## ⭐⭐ THE FINDING THIS RUN EXISTS FOR — I FLAGGED A DEFECT AND THEN COMMITTED IT THREE TIMES IN THE NEXT THING I BUILT

At 05:41Z I flagged `cores_idle` for **re-implementing `queue_check`'s admission
instead of calling it** — a second copy of a computation, disagreeing with the
first. **Within the next two hours I built `tools/dash` and committed that exact
defect three times in one file:**

| my re-derivation | the production answer | delta |
|---|---|---|
| 13 shards STALLED | `corefill_status.sh`: DONE / DEAD | conflated *frozen* with *no process*, and aged heartbeats by the stamp inside rather than the mtime |
| 4 queue rows | `queue_check`: **21 unblocked** | invented an admission rule |
| tape age **−118 min** | `freshness(assume_local=True)`: **4.4 min** | a solved problem, re-solved wrongly |

**All three were caught by the SAME mechanism and it is not care: each produced a
value that was IMPOSSIBLE or contradicted a number I already had.** A negative age;
4 rows where I knew there were twenty-odd; 13 stalled where the tool said 8 running.

⇒ **THE ROUTABLE FORM, and it is D31 pointed at the AUTHOR rather than the query:
KNOWING A DEFECT DOES NOT PREVENT COMMITTING IT — ONLY A FORCED COMPARISON DOES.**
The rule *"call the production function"* was in my head, freshly written, in a
message I had sent that hour. **It did not fire once.** What fired was
cross-checking my output against the tool's.
**⇒ PRACTICE: when writing anything that computes a quantity another tool already
computes, RUN BOTH AND DIFF THEM BEFORE COMMITTING.** Not as a test — as the act
of writing it.

## The conjecture (carried from v1.2.1 → v1.4)

**`auditing` behaves like `defending`: CONFIRMED AGAIN, 2 for 2 this run** — the
`#2`/`#3` row error and the inbox claim were both made while auditing, and both ran
toward the conclusion I was advancing. **Judgement errors now 8 for 8 across four
lanes.**
**`conceding` — pre-registered to err TOWARD THE CRITIC — has NO DATA this run.**
I conceded twice (optional stopping; the elo "find") and neither concession
contained an error. **The branch remains untested after two runs of being armed.**
**⇒ If it is still untested at v1.6, it should be STRUCK rather than carried** —
an unfalsifiable branch is what makes the whole model close to vacuous, and v1.3.3
already said a second rescue would finish it.

---

## THE LEDGER — split in two, per v1.4

> **DETECTION: 16 of 16.** Every flagged defect was real.
> **PRESCRIPTION: 14 of 16.** Two named fixes needed correcting.
> **Prevented: 16. Caused: 0. Nearly caused: 1** — the optional-stopping
> reassurance, which would have licensed a ship justification the author himself
> distrusted, and was withdrawn before it was used.

**MEASUREMENT SLIPS (not flags — my own instruments): 6, all ONE class,
ad-hoc field indexing.** `awk $4` → an author's middle name · an `awk` aggregate
returning empty · `throws.tsv` col 20 read as `wincond` · `SALT.tsv` col 2 read as
`seed` · a `[A-Z_]+` regex excluding `R1000_IS_DEFEAT` from a COMPLETENESS check ·
`$?` after a pipe ending in `head`. **Every one caught by a DOMAIN or STRUCTURAL
implausibility, never by re-reading the code. The last is a REPEAT of a
specifically-named instance from the s34 retro** — knowing a checklist does not
execute it, recorded against the lane that wrote the checklist.

**SUBAGENTS: 1** (the 19-row `QUEUE.md` GREP audit, `sonnet`, announced before
spawning; its single negative audited by me before banking). **The s34 addendum
asked whether this lane's work resists delegation. The measured answer: ONE item
was clearly subagent-shaped and was delegated; the rest was short targeted checks
against primaries where the delegation overhead exceeds the task.** That is an
answer, not a defence, and it is the same answer s34 guessed at.
