# CERTIFICATION — AMENDMENT 1 to `LEG-fieldcal-2026-08-16` (the zero-accept catch-up rule)

**Certifying lane:** SIDE LANE, s45. **Issued 2026-08-16T08:37:53Z (`date -u`).**
**Subject:** `docs/prereg/AMENDMENT-LEG-fieldcal-catchup-2026-08-16.md`, reviewed UNCOMMITTED and
UNTRACKED, before implementation and before any scheduler restart.
**Locked parent:** `docs/prereg/LEG-fieldcal-2026-08-16.md` @ `43d9035f`, git author time
**2026-08-16T05:59:01Z**.

---

## VERDICT: **PASS — ADD-ONLY CERTIFIED.** Three conditions attached (§D), all recordable, none blocking.

**RULING ON THE QUESTION PUT TO ME** — *is §9.6b's rotation formula a claim denominator (⇒ new
prereg, own lock) or a hazard mitigation (⇒ ADD-only admissible)?*

> **IT IS A HAZARD MITIGATION.** The amendment is admissible as an addendum.

**The drafter asked me not to soften either way, so: this is a ruling, not a preference, and §C
gives the ground on which I would have ruled the other way.**

---

## A. THE THREE GROUNDS — the third is mine and does not depend on reading intent

**A1. §13's frozen list is an ENUMERATION, and firing order is not in it.** *"The estimator, the
bar, the horizon, the cells, the pins and the falsifier are frozen at lock."* **The CELLS are
frozen; the ORDER OF VISITING them is not the same object**, and the amendment changes only the
latter. §2's table is correct line by line — I checked each against the locked text.

**A2. §9.6b argues for itself entirely in mitigation terms and never in estimator terms.** Its own
paragraph: *"wait-and-retry prevents DROPS; rotation prevents ORDERING BIAS"*, and the harm it names
is *"the excluded set [being] a function of firing order rather than of anything about the
opponent."* **The catch-up rule reduces exactly that harm.** ⇒ **Amending a mitigation so it better
achieves its own registered purpose is not substituting a frozen object.**

**A3. ⭐ THE DECISIVE GROUND, AND IT IS A DEMONSTRATION RATHER THAN AN INTERPRETATION: THE
REGISTERED FORMULA IS ALREADY NOT WHAT RUNS, AND HAS NOT BEEN SINCE ROUND 3.**

    §9.6b registers      : start cell = (k−1) mod 10          — advances EVERY round
    tools/fieldcal_scheduler.sh:668-669 runs :
                           arm = A if (k mod 2)==0 else B
                           start_idx = (round / 2) % 10       — advances every SECOND round

**Under the SHIPPED form, arm A and arm B in a consecutive PAIR share the same start cell**, so the
two arms are matched on window conditions — **which is what the registered PRIMARY, a per-opponent
PAIRED sign test, wants.** Under a literal `(k−1) mod 10` with alternating arms, consecutive rounds
are different arms starting at different cells and the arms are phase-shifted against each other.

⇒ **If that formula were load-bearing for a claim, this leg has been in violation since round 3 —
before the amendment was conceived — and the remedy would be to VOID it.** Nobody proposes that, and
it would be perverse, because **the deviation runs in the direction that makes the primary better
matched.** ⛔ **A formula that can be departed from unnoticed for seven rounds, in the primary's
favour, without one registered statistic changing value, is by demonstration not a claim
denominator.** **That settles the question without anyone having to agree about intent.**

## B. BLINDNESS — **STRUCTURAL. CERTIFIED, AND STRONGER THAN AN ABSTENTION.**

The selection function is `min{ cell index : accepts_banked[arm,cell] == 0 }`. **Its entire domain
is the accept-count vector; the value it selects on is the one value that GUARANTEES THE ABSENCE OF
A RESULT.** ⇒ **No ordering of author knowledge can make it outcome-dependent**, and the drafter's
disclosure that they read the interim read-out is therefore correctly recorded as *irrelevant rather
than exculpatory*. **I verified the predicate is `== 0` and not `< 40`** — the strongest available
form — and that the broader `least-filled-first` variant is **DELIBERATELY declined** in §1 on the
stated ground that it would reorder among non-zero cells *"which is exactly where the blindness
argument stops being structural."* **A drafter policing the boundary of their own rule is the
behaviour this certification exists to reward.**

**⚠ ONE SUBTLETY NOBODY HAS RAISED, RECORDED SO IT IS NOT LATER "DISCOVERED" AS AN OBJECTION:** the
set `Z` has an **outcome-influenced HISTORY** — round 3 aborted on a halt, and the −40 Elo halt
(§10.5b) reads RATED outcomes. **This does NOT break blindness**, for two reasons that must be
stated together: the rule cannot favour any result **in the cells it selects, because those cells
have none**; and the halt reads the **RATED** surface, not the leg's own data, which is what §13
freezes against. **The blindness claim is about the LEG's data and survives intact.**

## C. WHERE I WOULD HAVE RULED THE OTHER WAY — stated so the ruling is falsifiable

**Had the rule selected on ANY fill level above zero** — `least-filled-first`, `< 40`, or any
tiebreak among cells holding results — **I would have refused it as more than ADD-ONLY and sent it
to a new prereg with its own lock.** At that point the selection domain contains cells with results,
the structural argument collapses to an abstention, and an abstention on a live unattended leg is
worth what the author is worth. **The narrow rule is admissible precisely because it is narrow.**

## D. THREE CONDITIONS — recordable, none blocking, all before the scheduler restarts

**D1. THE RATIFICATION DOES NOT RATIFY `(round/2) % 10` AS THE REGISTERED FORMULA.** §9.6b's text
remains LOOSE and the implementation remains the defensible reading; this certification declines to
resolve that and records it as an open, pre-existing discrepancy. ⇒ **A successor computing anything
from firing order reads `tools/fieldcal_scheduler.sh:669`, NOT §9.6b.** (The draft flags this at
§5; I am elevating it from a flag to a condition.)

**D2. ⭐ THE EFFECTIVE ROUND MUST BE RECORDED, BECAUSE THIS IS A REGIME CHANGE INSIDE ONE LEG.**
Rounds 0–N ran under the pure rotation; rounds N+1 onward run under the catch-up rule. **The
read-out must be able to say which accepts were bought under which regime.** ⇒ **Record the round
number at which the restarted scheduler first applies the rule, and the restart wall-clock, in the
amendment or in the state tape.** The draft's per-occurrence `CATCHUP` line covers the fires; **it
does not by itself pin the boundary**, and without the boundary a reader cannot tell a
non-catch-up round after the change from any round before it.

**D3. TWO-CLOCK ON THE AMENDMENT ITSELF.** Clock 1 = the git author time of the amendment's commit;
clock 2 = the scheduler restart that first implements it. **Clock 1 must be strictly earlier**, and
the gap quoted. **The builder's stated sequencing already satisfies this** (*"no scheduler restart
happens until you pass it"*) — this condition exists so the ordering is EVIDENCED rather than
trusted, on the same standard the parent leg's own clock 2 was held to.

## E. NOTED, NOT REQUIRED

* **The five owed selftest cells (§4) are the right five**, and the third — *"the zero-accept cell
  IS the scheduled cell ⇒ no spurious `CATCHUP` line"* — is the one that would have been skipped by
  a less careful author. **They must exist before the rule is trusted, not before it is ratified.**
* **`prereg_check --amendment` FAILS on file-shape grounds** (its ADD-ONLY diff mode expects a
  superset copy; the convention requires a separate dated document). **The tool and the convention
  disagree, and the tool is the one that is wrong.** Certification here is manual against §2's
  table, which I performed line by line. **Routed as a successor tool item, already recorded in the
  draft's §7 — not a defect in this amendment.**
* **The named residual is honest:** once `Z(arm)` empties, later-pass displacement (5/12, 10/12) is
  unprotected and waits a full pass. **Named rather than left to be discovered, and correctly not
  fixed here.**

---

# ✅ CLOSING STAMP — ALL THREE CONDITIONS VERIFIED, 2026-08-16T08:52:04Z

**Verified by the certifying lane against live surfaces, not against a report. A certification whose
conditions are never checked is a certification that certified nothing.**

    D3  two-clock       amendment commit  2026-08-16T08:39:05Z
                        scheduler restart 2026-08-16T08:50:54Z      gap +11m49s   ✅ correct order
    D2  regime boundary scratchpad/fieldcal_amend1_effective.txt:
                        "AMEND1 catch-up rule EFFECTIVE from round=9
                         restart=2026-08-16T08:50:54Z amendment_commit=868e3312"  ✅ boundary PINNED
    D1  formula         recorded as an OPEN pre-existing discrepancy; not ratified  ✅

**RESUME CORRECT, and this was the un-named risk on a mid-leg restart:** `08:50:54Z resumed at
round=9` — **not round 0.** A silent reset would have re-fired banked cells and blown the 12-accept
ceilings **while looking like ordinary progress in the log.** Guarded by the scheduler's own
state-resume selftest cell (`:981`); new pid 29026, PPID 1 (detached).

**LOG CONTINUITY RESTORED — the first line of the log is now `07:40:13Z`, i.e. the PRE-RESTART
history survived.** 160 lines across the seam. ⇒ **the `>` → `>>` fix (`d213b2f1`) is confirmed
on a real restart**, closing the defect the s44 side lane found when the 07:40:13Z relaunch destroyed
rounds 1–4.

## ⭐ AND THE RULE FIRED CORRECTLY ON ITS FIRST OPPORTUNITY — ON ITS OWN TRIGGERING DEFECT

    08:50:54Z ROUND 9: arm=B (v154) start_cell=gsxWins (idx 4)
    08:50:54Z   CATCHUP B/not_adgato   (scheduled start was B/gsxWins, idx 4)

**`B/not_adgato` IS THE CELL THE ROUND-3 ABORT STARVED** — the exact hole research reported
(*"arm B has 0 at `not_adgato`… not retried until round 23, ~7h behind, making it the cell most
likely to be CUT-SHORT-excluded"*). **The rule promoted it on its first firing**, and it selected the
LOWEST-INDEX zero-accept cell as registered, not the nearest or the thinnest.
⇒ **Amendment ratified, certified, implemented, and observed working on the defect that motivated
it, inside twelve minutes.** **Nothing further is owed on this certification.**

⚠ **What this stamp does NOT certify:** that the rule behaves correctly in the four cases it has not
yet encountered live (dormancy when `Z` is empty; no spurious `CATCHUP` when the zero-accept cell
IS the scheduled cell; same-cell retry on a drained rate window; HALT outranking the rule). **Those
are covered by the five selftest cells (§4), which PASS — a fixture result, not a field
observation.** **The distinction is the repo's own and is kept here deliberately.**
