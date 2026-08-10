# LEG RECORD — PANEL-2 CALIBRATION (s28, 2026-08-10)

Prereg: `docs/prereg/PREREG-panel2-calibration-2026-08-10.md`, git author time
**14:27:30 CEST** (commit `a8ec673`), ~35 min before this arm's first match.
Platform-`createdAt` half of the two-clock standard is owed at read-out.

Runner: `tools/panel2_cal.sh`. **Activates nothing** — v104 is both the live
incumbent and the bot being calibrated — so zero rated exposure and zero holder
risk, unlike `fanout.sh`, which HANDOVER forbids running unattended.

---

## 1. HOLDER-ASSERT GUARD — MUTATION-TESTED, BOTH BRANCHES

`panel2_cal.sh` is a COPY of `fanout.sh`'s s27 D28 fix. The mutation test done on
the original does not cover the copy (side-lane flag, s28: *discipline attaches
to labels, not function*). Both branches were therefore exercised directly:

**ABORT branch** — `INCUMBENT=999 OUT=scratchpad/arm_panel2_MUTTEST.txt zsh tools/panel2_cal.sh 1`

```
13:06:51Z PANEL2: ABORT -- expected v999, holder is 'v104 (Loki v2)'. Firing nothing.
exit=1
corpus/FANOUT_ABORT: 13:06:51Z panel2 aborted: holder v999 expected, saw "v104 (Loki v2)"
scratchpad/arm_panel2_MUTTEST.txt: does not exist  <-- nothing fired
```

Pre-state: `corpus/FANOUT_ABORT` absent. Post-state: written. **The artifact was
then deleted** so a live monitor would not read a test as a real alert — which is
why the file is absent on disk and why this record exists instead. The claim in
the script's header comment was committed ahead of this record; that ordering was
the defect the side lane flagged, and it is corrected here rather than defended.

**PASS branch** — the live arm, holder `v104`, fired and banked challenges
(3 in cycle 1, continuing). A guard that only ever aborts is not a guard.

**RATE-LIMIT branch** (new in the rewrite) — exercised live at
`13:08:51Z PANEL2: rate-limited on bfbb9a68, waiting 330s (attempt 1)`, i.e. it
**waited for the window and retried the same cell** instead of dropping it.

---

## 2. THE RATE LIMIT IS 20 MINUTES, NOT 10 — AND IT SILENTLY STARVES THE TAIL

Measured on the CLI, verbatim:

```
Error: Rate limit exceeded: max 5 test/unrated matches per 20 minutes
```

`CLAUDE.md` and `fanout.sh` both encoded **10 minutes**; `fanout.sh` sleeps 620 s.
Both corrected.

**Evidence it CHANGED rather than always having been 20:** every s27 arm filled
its five panel cells uniformly — control v104 `7/7/7/6/6`, loki15 `7/7/6/6/6`,
confirm `4/4/4/4/4`, loki16 and loki14 `3/3/3/3/3` — on a 620 s inter-arm cadence.
Under a 20-minute window that is impossible: the tail of the id list would starve
every window. **So the s27 legs are not retroactively damaged by this.**

**The failure mode it creates going forward is silent and biased.** `fanout.sh`'s
`fire()` retries a rejected challenge 3× at 25 s, gives up, prints `fired 3/5`,
and moves on. Under a window it cannot outwait, the drop is **systematic and
always lands on the same cells**. It is not hypothetical: **this leg's own cycle 1
fired 3/5, and the two dropped cells were exactly the two RETAINED controls**
(I Stone `bfbb9a68`, gsxWins `ebd8d82a`) — the cells that link panel-2 back to
panel-1. A calibration leg had begun starving its own linkage.

Fixed in `panel2_cal.sh` two ways: **wait out the window and retry the same
cell**, and **rotate the starting cell each cycle** so a residual drop cannot
keep landing on one opponent. `fanout.sh` is patched to the 20-minute cadence but
**still drops on retry exhaustion — fix that before the rotation is restarted.**

---

## 3. REGIME SPLIT — FOR THE READ-OUT, SO NOBODY INVENTS AN OPPONENT EFFECT

This leg spans two instrument regimes and the read-out must say so:

* **Cycle 1** (13:0x Z): old cadence, no backoff, tail-drop. Banked 1 challenge
  each for `f61d19c1`, `48340ad8`, `0774b1b2`; **0** for `bfbb9a68`, `ebd8d82a`.
* **Cycles 2+** (from 13:08Z): rewritten runner, resumed with **`START=3`** so
  the rotation begins at the two starved cells and closes the deficit first.

Any per-window structure in the results has this in front of it.

---

## 4. WHAT THIS LEG DOES AND DOES NOT LICENCE

Per the prereg: **no plank is tested here and no plank result may be derived from
it.** Admission band `[0.20, 0.80]` on `core_kill_share`, n=25/cell. The
falsifier for the exercise itself stands: if all five cells land inside the band,
**the panel was never the problem** and that gets written.

---

## 5. DEFICIT-FIRST ORDERING — MUTATION RECORD (owed by `a49f87e`, s28)

`a49f87e`'s message claims the deficit-first count predicate is "mutation-tested
against the CLI banner split". The test ran; the record did not get committed
with it. **That is the second time in one session I have committed a
mutation-tested claim ahead of its artifact** (§1 was the first), which makes it
a habit rather than a slip — the standing rule is that the record IS the test.

**Why the predicate needed a mutant at all.** The `fcode` CLI now prints an
`Update available: 2.3.6 -> 2.3.7` banner, so one banked challenge lands as TWO
lines:

```
f61d19c1-600e-457b-861b-dbeb6b3d8691 Update available: 2.3.6 -> 2.3.7. Run: pip install --upgrade fcode
{"matchId": "a0ddeb6b-cc0b-4543-b29d-5f7dfaa714b1"}
```

The predicate I first wrote was `grep -c "^$id .*matchId"`. **`matchId` is never
on the same line as the id, so it matches nothing and returns a constant 0 for
every cell** — an ordering that reorders nothing while looking like it works.
Caught by inspecting the outfile before trusting the count, not by the test.

**Three cases, run against the live `scratchpad/arm_panel2.txt` (cells 1-3 banked
1 each, cells 4-5 banked 0):**

| case | input | required | observed |
|---|---|---|---|
| **A** real outfile | 1,1,1,0,0 | starved cells FIRST | `bfbb9a68(0), ebd8d82a(0), 0774b1b2(1), 48340ad8(1), f61d19c1(1)` ✅ |
| **B** absent outfile | no data | order UNCHANGED (must not reorder on nothing) | `f61d19c1, 48340ad8, 0774b1b2, bfbb9a68, ebd8d82a` ✅ |
| **C** MUTANT `^$id .*matchId` | 1,1,1,0,0 | must FAIL to prioritise | all counts read `0`; order scrambled to `0774b1b2, 48340ad8, bfbb9a68, ebd8d82a, f61d19c1` — **starved cells NOT first** ✅ |

Case C is the one that matters: the mutant produces a **different and wrong**
ordering, so case A's correctness is attributable to the predicate rather than to
luck in the sort. Shipped predicate: `grep -c "^$id "` — only the `*matchId*`
branch appends, so one line starting with the id IS one banked challenge,
banner or no banner.

## 6. CROSS-CITE — THE DROP-DIRECTION CLAIM IN §2 IS CORRECTED

§2 states the drop "always lands on the TAIL". **Over-general.** Research's
per-cycle reconstruction of the arm files found genuine mid-run drops starving
the **HEAD** (v104 control cycles 3 and 4 lost cells `{1,2,3}` and `{1,2}`), and
the side lane verified the panel2 fresh-run case starving the **TAIL**. Unified
statement, which is what the code comment now carries:

**Drop position is wherever the rate-limit window boundary falls in the id list,
set by the budget the arm inherits** — fresh/partial budget starves the tail,
restart-exhausted budget starves the head. **The rotation fix is
direction-agnostic and survives both**; what was wrong was the fixed direction,
not the prescription.

Two further corrections from the same audit, which matter for the CONTROL
denominator the audit session is reading: **two of the four apparent deficits are
restart truncation, not drops** (a final partial cycle when the runner was
stopped) — reading them as drops doubles the apparent defect — and
**loki14 / loki16 / v102confirm are perfectly uniform with zero drops. Only the
CONTROL arm is composition-skewed, and I Stone — one of the only two cells that
can move — is the under-represented one.**

---

## 7. `leg_read.py` MDE BRANCH — ALL THREE BRANCHES SEEN TO FIRE (s28)

The `BAR BELOW MDE` warning was added on the cross-lane audit's recommendation,
replacing a **hardcoded string** that printed *"with n~25 per arm this resolves
~20pp at best"* identically at n=25 and at n=150 — a constant column that
reassured two legs which had already spent their power. Demonstrated on the
banked arms rather than asserted:

| branch | invocation | required | observed |
|---|---|---|---|
| **warns** | `--bar 8` | fire | `** BAR BELOW MDE ... ** (bar 8.0pp < MDE 21.7pp)` ✅ |
| **does not warn** | `--bar 25` | stay silent, say resolvable | `bar 25.0pp is above MDE -- resolvable at this n` ✅ |
| **no bar given** | *(omitted)* | neither verdict | `(pass --bar <pp> to check the leg ...)` ✅ |

**The finding that fell out of the demonstration, and it is the audit's central
claim made concrete** — ⚠ **CORRECTED, see below**: the arm against the control
reads **MDE 19.5pp worst-case on ALL cells (n=75/165)**. **An 18pp bar is BELOW
that**, by **1.5pp**.

> **CORRECTION (s28, same session).** This section first published **21.7pp**,
> computed on "live cells" — **and that denominator was chosen by THIS LEG'S OWN
> OUTCOMES.** Selecting the denominator of a resolution claim on the dependent
> variable is the same fault this line exists to catch, caught by the research
> arm and confirmed by the side lane. **The quotable figure is the ALL-cells
> 19.5pp; the claim survives and its margin shrinks from 3.7pp to 1.5pp.**
> The obvious escape was checked and is not there: at the arm's observed share
> (~0.52) the worst-case `p(1-p)=0.25` bound is essentially tight (19.4pp at
> 0.45, 18.6pp at 0.35), so the true MDE is not materially below the bound.
> `leg_read.py` now takes the live-cell set as an INPUT (`--live-cells`, from
> PANEL2-CAL's admission verdict) and **labels the derived path POST-HOC in its
> own output** when none is supplied.
> One point the tool cannot see, in the original figure's favour: the cell it
> dropped was The Bisons at 13.3%, independently inert across four prior windows
> (0,0,0,0) — so that particular exclusion was not purely outcome-driven. **The
> tool cannot know that, which is exactly why the set must come from the
> calibration rather than from the leg.** So the
18pp-class claims this project has been firing all day sit *underneath* the
resolution of the fixture they were fired at — which is why p=0.303 was the
expected output rather than a surprise, and why the same p-value has now been
produced twice by two different instruments.

**Boundary bug caught in the same pass, recorded because it was mine:** the
first version tagged cells with `share <= 0.20` / `>= 0.80`, which throws out a
cell sitting EXACTLY on 0.80. The prereg admits `[0.20, 0.80]` **inclusive**; on
the LOKI-16 treatment arm two cells read exactly 12/15 = 80.0%, so effective n
printed 30/75 instead of 60/75 and the MDE was overstated at 28.3pp instead of
21.7pp. **An admission rule must match the prereg's brackets exactly — an
off-by-one on a boundary silently re-scopes the instrument.**

**Units guard added at the same time:** `--bar` is denominated in the PRIMARY
currency and nothing else. LOKI-16's coverage bar and LOKI-14's removal-count
bar are MECHANISM statistics; feeding either to `--bar` compares them against
the currency's MDE, which is a units error wearing a verdict's clothes.

---

## 8. THE REACHABILITY FINDING — RECORDED **WITH A DISCLOSURE**, NOT ACTED ON

**Magnus flagged that the ladder only pairs within ~±60. The research arm
measured it on our own 3,405 ladder games and he is right:**
**|gap| ≤ 60 in 81.2%** of games, ≤100 in 94.0%, ≤150 in 97.4%. Since we passed
1600 (530 games) the **entire** gap range is **−78.1 to +122.3**. The
highest-rated opponent we have **ever** met on the ladder is `0033` at 1759.2,
gap **+64.1**.

**⇒ The reachable ladder band is ~`us−80 … us+125`.** This also retires the
target-band framework's "climb band = us…us+400, 22 teams" as a *ladder* target:
**19 of those 22 cannot be met** until we are near them.

**And all five PANEL-2 cells sit outside it** — Banminary −204, OopsGotYourElo
−185, Team 48 −99, gsxWins −97, I Stone −88 — while the panel it replaces
contained The Bisons at **+32**, the only reachable-band cell we have ever used.

**THE EXTERNAL-VALIDITY ARGUMENT, which is the real one:** unrated challenges
have no ±60 restriction, so reachability does not *mechanically* constrain a
panel. It constrains **RELEVANCE**. Our rating is produced entirely by games
against `us−80…us+125`; **a panel at −200 measures performance against a
population that never touches our rating.**

## ⚠ DISCLOSURE, AND IT IS THE REASON NOTHING IS BEING CHANGED HERE

**I have already read this leg's interim per-cell numbers** (n=5/cell, via
`leg_read.py`, earlier this session). **So I am no longer blind to the outcome,
and any re-scoping of the candidate pool I make now is POST-DATA panel selection
— structurally identical to the trap that built the original panel**, however
independent the reachability argument is of the numbers I saw.

**Therefore:**
1. **PANEL2-CAL COMPLETES ON ITS PRE-REGISTERED TERMS.** 12 challenges
   outstanding; it reports against its committed `[0.20, 0.80]` admission band
   and its own falsifier stands unchanged.
2. **THE CANDIDATE POOL IS NOT EDITED.** Not now, not before it reports.
3. **The reachable band becomes a SEPARATE, NEWLY PRE-REGISTERED leg (PANEL-3)**
   whose selection criterion is stated in advance — **`us−80…us+125` AND the
   `[0.20, 0.80]` admission band, the INTERSECTION** — and which therefore does
   not inherit my exposure to panel-2's interim numbers as a selection input.

## THE PREDICTION, PRE-REGISTERED NOW SO PANEL-2 ALSO TESTS THE THEORY

Recorded **before** the outstanding 12 challenges land, so completion is a real
test of reachability and not a post-hoc reading:

> **The research arm predicts the two furthest-out new cells — Banminary (−204)
> and OopsGotYourElo (−185) — are the MOST LIKELY of the five to return as
> INERT CEILINGS**, because at −185 to −204 the Elo-expected win rate is already
> ~0.75–0.77 before any skill difference, and our realised rate against that
> stratum runs higher. **If so, selecting cells further below us made the
> ceiling problem WORSE, and the panel's methodology is right while its
> candidate pool was wrong.**

**The counter-prediction is on the record too, from the research arm against its
own point:** a panel exists to **resolve differences**, not to mirror the ladder,
and **reachable does not imply resolving** — **The Bisons at +32 read 0,0,0,0 in
D22, a FLOOR, and it is inside the reachable band.** So a reachable-band panel is
not automatically better; only the **intersection** rule is defensible.

**Caveat on the interim numbers I saw, stated so nobody quotes them:** at n=5
games per cell the sampling SD of a share is ~0.20. Those readings cannot
distinguish a ceiling from a live cell and **must not be cited** — which is
precisely why the leg is being allowed to finish rather than resolved from what
I have already seen.
