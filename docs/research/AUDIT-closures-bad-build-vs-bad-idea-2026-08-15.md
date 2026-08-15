# ADVERSARIAL AUDIT — WHICH DISMISSED ROWS DIED BECAUSE THE IDEA IS BAD, AND WHICH BECAUSE **OUR BUILD OF IT** WAS BAD?

**Side lane, s42, 2026-08-15 ~04:1xZ. Commissioned directly by Magnus:**
*"check builder's claim about preregs that have been dismissed, are any of them
dismissed because we just built a bad version of it?"*

**Version tag:** HEAD `9949a75d`; incumbent `bots/_v223sealrepair` (v140, live).
**Surfaces read:** `docs/research/CLOSURES-s43-2026-08-15.md`, the s42 verdict and
closure commits, and the incumbent tree itself.

⚠ **THIS AUDIT IS AIMED AT WORK I CERTIFIED.** I signed off several of these
closures tonight. **The failure Magnus is naming is the one a certifier is least
able to see, because each closure's INTERNAL arithmetic is sound** — the question
is not whether the sums are right but whether the thing measured was the IDEA or
one PARAMETERISATION of it.

---

## THE DISCRIMINATOR

> **A closure is legitimate when the mechanism cannot exist, is not present in the
> field, or is ruled out by the engine. It is a FALSE NEGATIVE when the arm we
> shipped could not have expressed the mechanism — because then the leg tested our
> BUILD, and the idea was never on trial.**

---

## 1. ⛔ **#51 AIM THE THROW LOOP — YES. THIS ONE IS DISMISSED ON A BAD BUILD, AND ON TWO NUMBERS NOW KNOWN FALSE.**

**The closure, verbatim (`CLOSURES-s43-2026-08-15.md:52`, unmodified since banking):**
> *"**ZERO exile throws across 115 RATED ladder games.** All 180 throws on record
> are unrated, 152 of them from a single game."*

**Both numbers are false.** Corrected by the builder in `426383e7`, **seventeen
minutes AFTER the closure was banked**, by doing the `file → version` join the
original claim never had:

    rated    200 games / 193 EXILE throws      <- claimed ZERO
    unrated  483 games / 180 throws            <- the 180 is the UNRATED HALF ONLY

**⇒ THE CLOSURE DOCUMENT STILL CARRIES THE FALSE NUMBERS.** The correction lives
in a commit message. **D21 is explicit: RETRACT AT THE PROVENANCE RECORD FIRST,
THEN THE ARGUMENT SITES.** The provenance record here is the closure doc, and it
is what a successor reads.

### ⭐ AND THE CORRECTED DATA DESCRIBES A DEFECTIVE IMPLEMENTATION, NOT A DEAD IDEA
Corrected shape: **the throws occur in 3 of 200 rated games (1.5%), and ONE game
carries 176 of the 193 (91%)** — the same signature as the banked 152-throw and
548-throw games: **a launcher latching onto ONE victim and cycling it, rather than
a weapon delivered across the field.**

**Those are two different claims with two different remedies:**

| written ground | what the data actually shows |
|---|---|
| *"aiming a loop that never runs where it counts"* ⇒ **the idea is not worth aiming** | *"our loop fires in 1.5% of games and 91% of its output is one pathological game"* ⇒ **the loop is BROKEN** |

**A loop that cycles a single victim 176 times is a description of a bad build.**
Closing *"aim the throw loop"* on that basis is closing the idea **because our
version of it is bad** — which is precisely the failure Magnus asked about.

**⚠ WHAT SURVIVES, STATED SO THIS IS NOT OVER-READ:** the closure's SECOND leg is
independent and untouched — **launcher coverage 16.2%, median build round 264,
past `KILL_WINDOW_RND: 250`.** ⇒ **#51 may still be correctly LOW PRIORITY. What
is wrong is the stated GROUND, and a closure that survives on a reason other than
the one written down is a closure whose document is now misleading.**

---

## 2. ⭐⭐ THE PATTERN, WHICH IS BIGGER THAN ANY SINGLE ROW: **THREE CLOSURES REST PARTLY ON METRICS THAT WERE INERT BY CONSTRUCTION — AND ALL THREE FOR THE SAME REASON**

| row | registered metric window | the gate constant that voids it |
|---|---|---|
| **#60** RENT DON'T OWN | `get_scale_percent()` at **r50 / r100 / r150** | `LAUNCHER_MIN_RND = 160` (`doctrine.py:1536`) — **no launcher exists at any of those rounds, in EITHER arm** |
| **#67** WIRE `_hunt_turret` | living entities at **r75** | `HUNT_MIN_RND = 120` (`doctrine.py:416`) |
| **#54** NAV LIMIT CYCLE | `self.stuck >= 5` | `main.py:400` resets `stuck = 0` on **any** position change, so a moving bot can never accumulate |

**⇒ IN EACH CASE THE LEG COULD NOT HAVE MEASURED THE MECHANISM. A negative from
such a leg is not evidence about the idea — it is evidence that we specified an
observation the mechanism cannot reach.** This is LOKI-18's failure (a metric
reading identically in both arms) recurring three times in one night, and it is
**the general form of Magnus's question.**

**⚠ EACH OF THE THREE SURVIVES ON AN INDEPENDENT LEG, AND I AM SAYING SO RATHER
THAN INFLATING THIS:**
* **#60** survives on **economics measured independently of the metric** — launcher
  = 2.0% of 308.2% of scale contribution at 8.2% coverage ⇒ **0.65% of the tax we
  levy on ourselves** — plus a `GREP` showing the behaviour is **absent entirely**
  (`ct.destroy(`, `can_destroy`, `self_destruct` all **0** occurrences).
* **#67** is **NOT closed** — it is RE-CLASSIFIED as a design row (~120 new lines,
  five unmade design decisions). Honest.
* **#54**'s conclusion survives, **but on a different mechanism than the one
  written**: the closure says *"`self.stuck` increments at exactly one site"* and
  **there are TWO** (`eco.py:910`, `main.py:398`). The impossibility is real and
  **stronger** than stated — `main.py:400`'s reset clobbers accumulation — **but a
  closure whose stated reason is falsifiable in one grep invites re-litigation.**
  *(I re-litigated it. It held. Recorded as a withheld flag, not a finding.)*

**⇒ SO: NO ROW IS CURRENTLY CLOSED ON AN INERT METRIC ALONE. But all three would
have failed IDENTICALLY if the ideas had been good, and in each case the leg was
void before it ran.**

---

## 3. ⛔ THE GAP THIS EXPOSES IS IN **MY OWN** OBLIGATIONS DOC

**OBLIGATION 13** requires a prereg to name the `file:line` its mechanism metric
reads and to assert that path appears in the treatment diff. **Checked: it says
NOTHING about WHEN the metric is observed.**

⇒ **A metric can name the right file, intersect the diff perfectly, satisfy OB13
in full — and still be observed at a round where the mechanism is gated off in
both arms.** All three cases above pass OB13 and are inert.

### PROPOSED OBLIGATION 17 — routed, not yet written into the numbered series
> **A prereg states the ROUND WINDOW its mechanism metric is observed in, and
> asserts that window against every gate constant that controls whether the
> mechanism can occur.** One line:
> `METRIC WINDOW: r<a>-r<b>. GATING CONSTANTS: <NAME>=<value> … . MECHANISM CAN OCCUR IN WINDOW: yes/no.`
> **If NO, the metric is INERT and the leg may not be fired on it** — the same
> consequence OB13 already attaches to a failed intersection.

**This is cheap: it is a grep of the gate constants against two integers.** It
would have caught #60, #67 and #54 before any of them consumed a screen.

---

## 4. WHAT I CHECKED AND CLEARED — so this is an audit, not a prosecution

* **#22 TURRET CUTOFF — CLEAN, and exemplary.** The gate genuinely does not exist
  (all 27 `get_current_round()` sites enumerated). **And the author checked the
  premise against their own interest, finding it FALSE IN THE ROW'S FAVOUR** —
  only 20.8% of games end before r150, so the late window is well occupied. **It
  is the absence of a LEVER, not of opportunity.**
* **#21 GUNNER COUNT — CLEAN.** Set algebra over ENGINE constants (gunner d²≤13 ⊂
  sentinel d²≤32; unobstructed-ray ⊂ any-ray), no behavioural premise. D12's
  carve-out correctly invoked.
* **GUNAXABL (#33) — CLEAN and correctly NOT closed.** Missed its keep edge by
  **one game** and the author wrote *"#33 is NOT answered"* and refused to round.
* **SEALFLOOR6 / #53's floor third — CLEAN and correctly NOT closed.** The lock
  made `≤48.67` the branch that closes the floor third; the leg took the
  **FUTILITY-ALONE** branch at n=2737 instead, and the author explicitly refused
  the REAL-NEGATIVE reading because that edge is defined at n=5400. **⚠ Had it
  gone the other way, a single constant value (floor = 6) would have closed a
  whole third of #53 — the exact bad-build shape, one branch away.**

---

## VERDICT

**ONE row is dismissed on a bad build: `#51`** — on two numbers now known false and
still uncorrected in the record, and on a data shape that describes a defective
launcher loop rather than a worthless idea. **Its low-priority conclusion may
survive on an independent leg; its written ground does not.**

**THE LARGER FINDING IS THE PATTERN**: three closures carried metrics that were
**inert by construction**, all because an observation round was chosen without
checking the gate constants that decide whether the mechanism exists yet. **None
of the three is currently load-bearing — every one survives on an independent
leg — but the near-miss rate is 3 in one night, and OB13 cannot see it.**
