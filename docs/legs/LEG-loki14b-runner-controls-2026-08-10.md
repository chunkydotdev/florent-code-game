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
