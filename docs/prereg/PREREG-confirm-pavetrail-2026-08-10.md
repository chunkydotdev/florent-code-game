# PREREG — **THE SINGLE CONFIRMATORY TEST** of the PAVE_TRAIL effect

**Committed BEFORE this arm's first window.** The `CONFIRM-v102` arm of
`tools/fanout.sh` has fired **0 matches** at the time of writing; the CONTROL
arm fired at 08:18:32Z and this arm is next-but-one, ~08:39Z. Platform clock
quoted in the commit body.

## What is being confirmed, and why a confirmation is owed

**v104 "Loki v2" (`PAVE_TRAIL_ON = False`) is LIVE**, shipped on
`core_kill_share` **60/100 vs 42/100 = +18.0pp**, nominal Fisher p=0.016.

**That evidence was pooled into significance after a null, and the ship record
says so.** Corrected for multiplicity across the session's currency reads and
for optional stopping — LOKI-11 was stopped when it died, LOKI-13 was continued
while it looked good — **the honest figure is ~0.05 family-wise, not 0.016.**

**A fourth un-pre-registered look at the same effect confirms nothing; it just
adds another look.** The only thing that removes optional-stopping and
multiplicity inflation is **one test, declared in advance, at a fixed n.** This
is that test.

## THE TREATMENT IS THE INCUMBENT — read the direction carefully

The live bot is now v104, so this arm runs the **OLD** bot and the comparison is
inverted relative to the ship:

    ARM UNDER TEST : v102 = bots/_v124loki8   (PAVE_TRAIL_ON = True)
    CONTROL        : v104 = bots/_v130loki13  (PAVE_TRAIL_ON = False), the live incumbent

**PREDICTION, stated before any data: v102 scores ~18pp WORSE than v104 on
`core_kill_share`.** If the shipped effect is real, the old bot must lose the
ground the new one gained, on the same panel, on the same pinned maps.

## Pre-declared, and this is the clause that does the work

**THIS IS THE ONE CONFIRMATORY TEST. There will not be a second, and this arm
will not be extended past n=100 whatever it shows.** No stopping early on a
favourable read, no continuing on an unfavourable one. **Both arms run to
n=100 and the result is read once.**

## Bars

**PRIMARY: `core_kill_share`, v102 vs v104, both at n=100** (4 cycles of
`fanout.sh`, 25 games per arm per cycle), on the pinned panel and pinned maps
(fjordgate, jackpot, atoll, saga, snowflake).

**CONFIRMED** if v102 is worse than v104 by a margin whose two-sided interval
excludes zero at n=100/100. **NOT CONFIRMED** otherwise — and *not confirmed*
will be written as **"the ship's evidence did not replicate"**, plainly, with
the rollback question put to Magnus rather than quietly dropped.

**SECONDARY, reported and never substituted:** `r1000_rate` (the ship showed
9% -> 3%), median time-to-core-kill (203 -> 152), kills inside `KILL_WINDOW_RND`.

**NO MECHANISM BAR IS SET, deliberately.** The shipped effect is **not
attributed to a mechanism** — LOKI-13's conveyor bar failed at 0.86x against a
pre-registered <=0.70x, so v104 is better for reasons unknown. **This leg tests
WHETHER, not WHY.** `LOKI-15` (v105, the conveyor-quota arm running alongside)
tests WHY, and the two must not be conflated: different treatments, different
questions.

## Known limits, stated in advance rather than discovered

* **The panel is a two-cell instrument.** The Bisons are a floor, Leviathan and
  CtrlAltDefeat are ceilings; I Stone and gsxWins carry the movement. **This is
  a read on two cells wearing a five-cell denominator** and the per-opponent Δ
  column is mandatory in the result.
* **Seats are assigned by the platform and cannot be pinned.** Seat mix is
  printed per cell; any cell whose seat differs between arms is flagged and the
  claim is stated with and without it.
* **The control is the live incumbent at k=6, still inside its ladder break-in.**
  That affects its *rating*, not its `core_kill_share` on this panel, which is
  what is being measured — but it is recorded so nobody reconciles the two later
  and finds a discrepancy they cannot explain.
* n=100/100 resolves roughly 14pp at 80% power. **An 18pp effect is detectable;
  a 5pp one is not, and no claim will be made in that range.**

## Cost

Zero rated exposure by the measured procedure: the arm activates v102 only for
the ~60 seconds it takes to fire five challenges, then rolls back to v104 and
**verifies the holder**. `breakin_watch` (floor 1567) and `ship_watch` remain
armed on v104 throughout.
