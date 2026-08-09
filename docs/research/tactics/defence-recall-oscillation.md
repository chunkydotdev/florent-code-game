---
tactic: FAILURE MODE — a boolean "come home and defend" trigger makes the attack oscillate and do nothing
source: https://battlecode.org/assets/files/postmortem-2022-5-musketeers.pdf
origin: Battlecode 2022 / 5 Musketeers (semifinalists)
evidence: documented
transfers: yes
---
WHAT IT IS — A concrete, named bug that any bot with both a strike role and a
defence role will reproduce. 5 Musketeers tried two designs. The first wasted
units:

Defence-specific spawns — *"This was okay, but then after defending an attack,
they sat around and did nothing."*

The second, a distress beacon that recalled attackers, produced the failure:
> *"This worked but led to an unfortunate oscillation problem."*
> *"the soldiers will go back to rushing because there's no one else in sight, so
> we think we've neutralized the threat"*

The unit walks home, the threat is no longer visible *because it walked home*, so
it walks back out, and so on. The trigger's own effect erases its input.

**The fix they shipped is the transferable part, and it is not hysteresis — it is
replacing a predicate with a continuous statistic:**
> *"If a single soldier pops into our radius, that isn't enough to shift the
> average. We'll just keep doing what we're doing."*
They routed toward the *average* position of enemy clusters, so home defence and
forward attack became the same computation with different inputs, and a lone
scout could not flip it.

WHY IT MATTERS HERE — Loki is by construction a bot with two roles and a
250-round deadline, so it will need exactly this trigger, and our engine makes the
oscillation **worse than theirs** in three specific ways:

1. **Buffered comms.** Store writes are visible only from the next round, so any
   "threat seen / threat gone" flag is always one round stale. A flag that flips
   on a one-round sighting produces a two-round-period oscillation that no unit
   can observe directly.
2. **Last writer wins.** With several units writing a threat slot, the value is
   whichever unit ran last, not a consensus — so the flag is not even a stable
   reading of a stale state.
3. **Move and act are mutually exclusive** for builder bots, and moves are
   cardinal-only. An oscillating builder is not merely indecisive, it is
   *spending its entire turn budget* on undoing the previous turn: zero builds,
   zero heals, zero attacks, for as long as the oscillation lasts.

This is also the mechanism by which the `rush cost` surcharge
(`the-rush-cost-budget-gate.md`) is safer than a mode flag: a surcharge changes a
*price* and degrades smoothly, where a boolean mode teleports the whole fleet.

WHAT WOULD KILL IT (as a concern) — If Loki never recalls — a strike force that
commits and never returns — there is nothing to oscillate. That is a legitimate
design, but it is the one `the-rush-that-cannot-transition.md` documents as the
most common way a rush loses. The two files bound each other: you need a terminal
state, and the terminal state must not be a flip-flop.

BUILDER HOOK — Never write a raw boolean threat flag. Two options, both cheap
within a 16-slot unsigned store (**and remember a negative write RAISES and
permanently destroys the unit**):
- a **saturating counter** in one slot, incremented on sighting and decremented on
  a clear round, with the role read from a threshold — decay gives hysteresis for
  free; or
- 5 Musketeers' own answer: store a **coarse enemy centroid** and compare
  distances, so one stray builder cannot move the decision.
Then instrument it: log per-match the number of role flips per unit. If a Loki
iteration shows units flipping more than a handful of times per game, the strike
is not being measured — the oscillation is.
