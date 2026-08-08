# The ship gate

Standing policy, adopted 2026-08-08 19:4x on Magnus's call ("ship it all and
direct us in the right path"), replacing the field-evidence gate that preceded
it. This document is the answer to a specific measured failure, so it starts
with the measurement.

## Why the old gate had to go

The project climbed **1345 → 1625 elo (rank #40 → #21)** in its first 35 hours,
then gave back **−57 elo and 9 ranks in the following 15 hours**. The audit that
prompted this document found the two curves are the same curve:

| phase | ship cadence | committed doc:code churn | elo |
|---|---|---|---|
| 08-06 (v46→) | — | 0.14 | 1345 → 1462 |
| 08-07 (→v72) | 0.79 ships/hr | 1.57 | → **1625 peak** |
| 08-08 (v72→v80) | 0.46 ships/hr | 1.88 | → 1568 |

On 08-08 there were **eleven consecutive hours (06:00–17:00) with zero bot lines
committed** — pure measurement churn — and the session's own handover recorded
*"NOTHING SHIPPED THIS SESSION, deliberately. Five planks reached KEEP-dev and
none earned a window."*

The proximate cause is not laziness or bad judgement. It is that **the gate as
written could not be satisfied by any amount of work**, and the previous session
proved it (tape rows `tle-headroom`, `e1-family-missing-measurement`):

> field evidence about an unshipped head is structurally unobtainable —
> submission download is own-team-only, `match test` takes two local dirs,
> unrated runs the ACTIVE submission.

A gate that demands field evidence for a head that cannot be fielded is a gate
with no gate-opening move. Everything accumulates in KEEP-dev forever, and the
only remaining productive activity becomes measuring the measurement. That is
literally what 08-08 produced: five measurement-stack findings, a bug found in
the fix for one of those findings, and a retroactive caveat invalidating a full
day of kladde legs. All of it high quality. None of it worth 57 elo.

## The gate

**A head ships when all three hold:**

1. **No measured local regression.** Parity counts as a pass. The bar is "the
   battery does not say this is worse", not "the battery proves this is better".
   An interval straddling 50 is a PASS, not a NO-VERDICT-so-hold.
2. **A window is available** — the slot is free, or the current holder's window
   has closed under the swap rule (below).
3. **Nothing is known-broken.** Identity control clean, no crashes in the legs,
   and TLE headroom measured on real hardware if the head added meaningful CPU.

That is the whole gate. **The ladder is the field instrument.** Rollback is the
control, and it costs one click.

### What is explicitly NOT required

- Field evidence for the unshipped head. It does not exist. Stop owing it.
- A positive head-to-head against the current staged head. Self-legs are
  attribution-only in *both* directions (standing rule, unchanged) — so a
  parity result is not a reason to hold any more than it is a reason to ship.
- Every named follow-up leg paid off. Name the debts on the tape row and ship
  anyway; the ladder prices them faster than the probe fleet can.
- Unanimity between arms. Either arm may state a concern on the row; the
  builder decides.

## The rollback rule (unchanged, now load-bearing)

The swap rule is what makes a loose gate safe, so it is the part that must not
drift:

- **Arms at ≥8 matches for the current holder.** Below that the window has not
  said anything — the tape carries three exhibits of early crossings at n≤5
  being pure noise.
- **Prices only the current holder's tape rows.** Version binds at match
  *creation*, not activation, so read the next match's meta stamp after any
  activation before crediting a row. Two tape corrections on 08-08 (v77, v79)
  came from exactly this.
- **Rolling last-5 ≤ 0 frees the slot.** Whoever notices it fire rolls back. No
  discussion required, and it cuts both directions — a teammate swapping our
  flat window is the system working, not a conflict.

## Window budget — the actual scarce resource

At roughly 8 rated matches/hour, an armed window is ~1 hour. That caps the whole
team at **~10–12 evaluated ships per day**, total. Consequences:

- Ship the **biggest available change** per window, not a stream of small ones.
  Attribution is what local legs are for; windows are for finding out whether
  the thing wins.
- A window spent on a head that cannot move the needle is a window burned.
- Two people shipping into the same open window destroys both measurements.
  Announce the activation; respect an armed window.

## What measurement is still for

This is a re-pointing, not an abolition. Local legs remain the only way to:

- **Prove a change is dormant where it should be** (identity controls, 0-flip
  det legs). These are gold and stay mandatory — they are how we ship a plank
  without shipping a regression on 14 other maps.
- **Attribute** a result after the ladder has delivered one.
- **Catch defects in shipped bytes** — the highest-EV find of 08-08 was
  `hive-freeze-live-defect`, a live-bot bug, not a candidate plank.

The rule that changed: **measurement work must name the ship decision it will
change.** If the answer is "none, but it would be good to know", it goes on the
queue, not in front of a window.

## Retired

- **The probe fleet as a ship gate.** Four of five instruments are invalid or
  caveated (kladde ~70pts miscalibrated with unfaithful turret composition;
  flotte never valid in two respects and has no launcher code at all; cad
  attribution-only under P6-widened; band rush-mode only; orizon the lone valid
  one). The recalibration cost recurs every time an opponent ships. Probes stay
  for **attribution**; they no longer gate.
- **`--tle 0` as the default for anything claiming CPU safety.** Platform CPU
  peaks at ~93% of the 10ms limit driven by the *shared base*, and every local
  leg is CPU-blind. Any head that adds meaningful work owes one real
  `fcode match test`.
- **"KEEP-dev" as a resting state.** A plank is either shipping into the next
  window, being fixed, or refuted and closed. If it has been KEEP-dev through
  two windows, it is refuted by neglect — close the row.

## The failure mode this policy accepts

We will ship some heads that lose, and we will see it on the ladder rather than
predict it locally. That is priced: a bad window costs ~8 matches and a click.
The 08-08 audit measured the alternative at 57 elo, and the alternative *felt*
more rigorous the entire time it was happening. Rigor that cannot terminate in a
decision is a cost, not a virtue.
