# LOKI-14b RUNNER — CONTROL RECORD (built s28, leg UNFIRED)

`tools/loki14b_leg.sh`, built ahead of the leg so the critical path is code that
has already been seen to fail correctly. **The leg has not fired.** Prereg:
`docs/prereg/PREREG-loki14b-carrier-targeted-2026-08-10.md` (body `ce12795`
15:29:57; Amendment 1 `6463741` 15:38:30).

## Why this runner is NOT a copy of `panel2_cal.sh`

`panel2_cal.sh` activates nothing, so on a rate-limit rejection it can afford to
**wait 330 s and retry the same cell** — the correct choice there, and
fire-verified.

**This leg runs a PROTOTYPE LIVE.** Every second v107 holds the slot is rated
exposure and a scouting window, and the prereg says *"activate only in the
instant before firing"*. So the same rejection gets the **opposite** handling:

> **On a rate-limit rejection this runner does NOT wait. It rolls back
> immediately, sleeps out the window with the INCUMBENT live, and re-activates
> for the next window.**

**Copying the panel2 behaviour here would have been the plausible mistake** —
same symptom, same-looking fix, and it would have quietly extended prototype
exposure by ~5 minutes per rejection. The cost of not waiting is dropped
challenges, so the drop is made **unbiased** rather than eliminated:
**deficit-first ordering** off the arm's own outfile (fewest banked fires first),
the same fix `fanout.sh` now carries.

## Controls — every guard driven to BOTH verdicts before the leg exists

### 1. Amendment 1's floor: fewer than two admitted carriers ⇒ no leg

```
$ zsh tools/loki14b_leg.sh 1 4a7f4c9a-...          # ONE carrier
REFUSING TO FIRE: 1 carrier(s) given, Amendment 1 requires >= 2.
A one-cell fixture cannot support this leg's conclusion. Re-register instead.
exit=2
```

Complement: with two ids the run proceeds past this branch (below), so the
refusal is attributable to the count and not to a script that never runs.

### 2. Holder assert (s27 D26/D28) — abort branch

```
$ TREAT=999 OUT=/tmp/l14b_mut.txt zsh tools/loki14b_leg.sh 1 aaaa bbbb
13:43:25Z ABORT -- expected v999, holder is 'v104 (Loki v2)'. Firing nothing.
13:43:30Z rolled back to v104, VERIFIED
corpus/FANOUT_ABORT: 13:43:25Z loki14b: expected v999, holder is "v104 (Loki v2)"
/tmp/l14b_mut.txt: does not exist          <-- ZERO challenges fired
```

**The rollback path also ran and VERIFIED in the same test**, so the abort does
not leave a foreign holder behind — the exact failure that contaminated the
CONTROL arm in s27. `corpus/FANOUT_ABORT` was **deleted after the test** so a
live monitor cannot read a test as a real alert; this record is its trace, per
the standing rule that the record IS the test.

**Holder verified unchanged after all controls: `Active bot: v104 (Loki v2)`,
rating 1658.** No rated exposure was spent building or testing this runner.

### 3. Not yet exercised, and named so nobody assumes otherwise

* The **rate-limit deferral branch** (`break` without waiting) has not fired —
  it needs a live rejection while the prototype is up, which only happens during
  the leg. **Watch for it in the first cycle's log.**
* The **`HOLDER_ALERT` path** (60 failed re-activations) has not fired and cannot
  be provoked cheaply without leaving a foreign bot live. It is the one branch
  in this runner accepted on construction rather than on evidence, and it is
  recorded here as such rather than left silent.

---

## POST-FIRE: THE RATE-LIMIT DEFERRAL BRANCH FIRED ON THE FIRST CYCLE

Named above as *"not yet exercised"*. It fired within seconds of the leg
starting, and behaved exactly as designed:

```
13:49:57Z cycle 1: v107 LIVE, firing 4 carriers
13:49:59Z rate-limited on 4a7f4c9a -- NOT waiting with v107 live; deferring to next window
13:50:04Z rolled back to v104, VERIFIED
13:50:04Z cycle 1: fired 0/4 (total 0)
```

**v107 held the slot for 7 seconds.** Had this runner copied `panel2_cal.sh`'s
wait-and-retry — the plausible move, same symptom, same-looking fix — the
prototype would have been live for **5½ minutes** on a window it could not
outwait, and then likely again on the retry. **The inversion paid on the very
first cycle.** Holder verified `v104` immediately after.

**MY OWN SEQUENCING ERROR, recorded because the runner absorbed it and I would
otherwise get credit for a clean start.** I paused `panel2_cal.sh` and fired
LOKI-14b **4 minutes after panel2's cycle 2 had spent all 5 challenges of the
20-minute window** (13:45:58Z). Pausing a runner does not refund the budget it
already spent. Cost: one rejected attempt, which itself counts against the
limit. **The runner's design converted my error into a 7-second exposure and a
deferral instead of a contaminated or half-filled window** — which is the whole
argument for putting the pre-commitment in the script rather than in attention.

**Standing note for anyone switching arms:** the rate-limit budget is shared
across ALL unrated/test challenges and is not per-runner. Check when the
outgoing runner last fired before starting the incoming one; the safe gap is
~20 minutes from its last challenge, not from the moment you kill it.

---

## TEXT vs BEHAVIOUR: THE RUNNER WAS LAUNCHED FOR 6 CYCLES, THE PREREG SAYS 4

**Side-lane flag, s28.** The process was started as
`zsh tools/loki14b_leg.sh 6 <4 carriers>` at 13:49Z — **before Amendment 6
existed**. Amendment 6 (14:01Z) then pre-committed *"stop after cycle 4, decode,
and extend ONLY if the throw count is under 150"*. Left alone the runner would
have fired **6 cycles ≈ 24 matches ≈ 240 throws**.

**RESOLVED BY HONOURING THE TEXT: stop after cycle 4.** `tools/loki14b_stop.sh`
is armed and will kill the runner when `cycle 4: fired` appears in the log.

**Why the text and not the process, when the extra dose is scientifically
BETTER.** At 240 throws λ≈5.2 and P(≥5) returns to ~60%, versus 26.5% at four
cycles — so six cycles is the stronger leg, and since the stop was pre-committed
on DOSE, more dose cannot flatter the result. The argument for amending to 6 was
real. It loses anyway:

* **The extra two cycles buy a LABEL, not a DECISION.** They raise the chance of
  reaching the word CONFIRMED — but Amendment 4 already forbids a CONFIRMED from
  licensing a ship and requires it to carry "against teams rated 806–1107 while
  we are 1658". **Nothing downstream changes based on which word we get.**
* **The EXISTENCE PROOF — the leg's whole stated purpose under Amendment 6 — is
  already bought at four cycles.** P(≥1 | mechanism works) = 96.8% at 160
  throws. The ≥5 bar was always about CONFIRMED, never about existence.
* **The other half of Amendment 6's rationale is the budget**, and it is the half
  that serves Magnus's climbing ruling: two extra cycles is ~40+ minutes that
  PANEL2-CAL — paused at 13/25, repairing the instrument every currency verdict
  depends on — does not get.

**And the thing that decides it regardless of the merits:** a prereg that says 4
while the process does 6 means **whichever number a read-out later cites, the
other is evidence the text was written after the fact.** That cost is
unrecoverable and it is larger than the difference between 26.5% and 60% on a
leg whose result cannot license a ship either way.

**The watchdog is a SCRIPT, not a note**, for the same reason Amendment 1's
two-carrier floor is enforced in the runner: this stop fires ~50 minutes out, and
a pre-commitment held in attention is the one that fails under time pressure.
Both branches checked before arming — fires on a log showing `cycle 4: fired`,
stays silent on one showing cycle 3. It also **verifies the holder after killing**
and re-activates v104 if needed, because **a killed runner cannot run its own
rollback** — the one hazard this stop introduces.

---

## THE STOP WAS ARMED ONE CYCLE SHORT — "CYCLE 4" IS NOT "FOUR CYCLES OF DATA"

**Side-lane flag, s28, caught ~45 minutes before the stop would have fired.**

`loki14b_stop.sh` triggers on `cycle N: fired`, i.e. the cycle **NUMBER**.
**Cycle 1 banked 0/4** — fully deferred on the rate limit — so the PRODUCTIVE
cycles are 2, 3, 4:

| stop at | productive cycles | matches | throws @10.0/match | vs the 150 gate |
|---|---:|---:|---:|---|
| cycle 4 (as armed) | 3 | 12 | **~120** | **BELOW — "ANSWERED NOTHING"** |
| cycle 5 (re-armed) | 4 | 16 | ~160 | above |

**As first armed, the watchdog enforced the one outcome nobody wanted: spend the
holder time and buy nothing.** Amendment 6's own arithmetic is explicit —
*"4 cycles × 4 carriers = 16 matches ≈ 160 throws"* — so the literal cycle
number under-delivered the amendment's stated arithmetic **because one cycle was
empty**. No new amendment needed: Amendment 6 already says *"decode, and extend
ONLY if the throw count is under 150"*. **Re-armed to cycle 5**, which is that
extend, taken in advance rather than after an hour of the leg sitting below its
gate while PANEL2-CAL competes for the budget.

**Deviation recorded rather than left silent:** the watchdog now stops on cycle
**5**, not the "cycle 4" Amendment 6 names. That satisfies the amendment's
arithmetic and purpose and departs from its literal cycle number.

**AND THE PROXY IS NOT THE GATE.** 10.0 throws/match is measured on **LOKI-14's
panel of five near-peers**; these four carriers are weaker bots whose builder
counts and border exposure may differ **in either direction**. **The gate is
≥150 THROWS DELIVERED and cycles were only ever a proxy for it — decode and
check the actual count before reading anything.** Written into the watchdog
itself so the read-out cannot inherit the proxy as if it were the gate.

## AND THE PARAMETER IS NOW OBSERVABLE, BECAUSE IT COULD NOT BE VERIFIED

Armed first as `STOP_AFTER=5 zsh tools/loki14b_stop.sh` — and macOS would not
show the variable in an env dump of another process, so **the load-bearing
parameter of a pre-commitment could not be verified from outside.** It was
probably set. "Probably" is not a control.

Changed to a **positional argument**, so `ps` reads
`zsh tools/loki14b_stop.sh 5` and the stop point is visible to anyone —
including a successor session that did not arm it. Default remains 4 when no
argument is given. **Same rule as gating on the `Active bot:` field rather than
an exit code: if a parameter is load-bearing it has to be OBSERVABLE, not
merely correct.**
