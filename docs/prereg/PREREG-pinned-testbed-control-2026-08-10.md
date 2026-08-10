# PREREG — THE PINNED TESTBED CONTROL (v102 / LOKI-8)

**Committed BEFORE leg creation.** Supersedes the unpinned baseline
(`PREREG-live-unrated-baseline-2026-08-10.md`) **as the control**; that leg's
numbers stand as a field read and are not reused as a denominator.

Line `loki`. **No treatment.** v102 is already the active submission, so this
leg costs **zero rated exposure**.

## SELF-CERTIFYING CLOCK — and it MEASURES the skew instead of arguing about it

The side lane certified the previous lock with a **15.362 s** margin and flagged
honestly that git time and platform time are two clocks whose offset **this
project has never measured**. A 20 s skew would have inverted it silently.

Measured here, in one shell call, before this leg exists:

    platform: a match `completedAt` 2026-08-10T04:06:04.035Z
    local   : same call read 2026-08-10T04:06:05.898Z

A match cannot be observed before it completes, so the completion instant reads
**no later than 04:06:05.898 on the local clock** while reading 04:06:04.035 on
the platform's: **local is not ahead of platform by more than 1.86 s.** The
opposite bound comes from the previous leg, where a request that left this
machine at local >= 03:58:42 was stamped 03:58:55.362 by the platform:
**local is not behind platform by more than 13.4 s.**

    SKEW (local - platform) is in [-13.4 s, +1.9 s]. First measurement of it.

**Neither bound is tight, so this prereg does not lean on either.** The fix is
structural instead: **this file is committed and pushed before the rate-limit
window even opens**, leaving a margin of minutes against a bound of seconds.
**Standing rule adopted from the side lane: every prereg from here quotes a
platform-clock reading taken in the same shell call as its commit.**

## THE TESTBED — pinned, per Magnus's method, and it does not move without a note

> *"Previously we ran tests against opponents but for 5 specific maps until
> something interesting happened on those, and sometimes we rotated the maps
> when we wanted to try something else."*

    MAPS (5, fixed, size-ordered so distance-to-core is a CONTROLLED axis):
      fjordgate 10x10 | jackpot 16x16 | atoll 18x18 | saga 24x24 | snowflake 26x26

    PANEL (5, fixed):
      The Bisons    1626  f670dfed-dfee-421b-8c01-a67b8a278ce3
      I Stone       1617  bfbb9a68-b37a-4a61-b0ea-d36369c8f65a
      Leviathan     1603  26286680-d861-4f9e-9073-a6201bd48d3b
      gsxWins       1594  ebd8d82a-7365-4ccb-af0b-defea3a1ac4d
      CtrlAltDefeat 1581  74e43df6-bad7-474b-8e37-0ea44a2c80f1

**ONE LEG = 25 games = ONE 10-minute window**, because the platform enforces
`max 5 test/unrated matches per 10 minutes` (learned by hitting it, not by
reading it). Matches themselves complete in ~15 s, so **the rate limit is the
entire cadence constraint** — ceiling 150 games/hour across all legs.

**Why the panel is 5 and not the 6 originally registered.** Ouroboros was
rate-limited out of the first leg. Keeping the panel at 5 makes a leg exactly
one window, which is the property that lets a treatment leg and its control be
fired back-to-back on the same day. **Ouroboros is fired separately to close the
registered set; it is NOT part of the recurring control.** Consequence recorded
per the side lane's obligation 8: **the control denominator is /25, and no later
leg may quote /30 against it.**

## What is measured

**PRIMARY: `core_kill_share`** — of games ending `core_destroyed`, the share
ours. **PRIMARY: `r1000_rate`**, which under `R1000_IS_DEFEAT: yes` is a loss
rate. **SECONDARY, never substituted:** time-to-core-kill distribution against
the `KILL_WINDOW_RND: 250` bar, and the **per-map** split — which is the whole
point of pinning, since map size is now a readable axis rather than noise.

## Bars

**A control cannot fail.** What is pre-committed is its USE: these 25 games are
the denominator for every trick leg fired on this testbed, and a trick leg that
changes the panel, the maps, or the seat mix is **not paired with it** and must
say so in its own write-up.

Pre-committed so it cannot be found convenient later:

* The unpinned leg gave **0/25 r1000, 56.0% core-kill share, 14 wins**. **If the
  pinned leg lands far from that on the same panel, the map draw was carrying
  the result** — which would be a finding about our variance, not about the bot,
  and I will report it as one.
* **The Bisons went 4-1 up on us with kills at 74/66/92/49 turns.** If that
  repeats on the pinned maps it is their method; if it does not, the first leg
  caught a map draw. Either answer is worth the window.

## Falsifier for the pinning itself

If per-map variance turns out to be small — if kill turns cluster regardless of
map size — then pinning bought little and the honest report is that the previous
leg was a serviceable control after all. **I will write that if it happens**
rather than crediting the method for a difference it did not make.
