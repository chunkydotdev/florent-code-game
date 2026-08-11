---
tactic: Nobody governs forward DWELL on a clock — the clocks that survived are all "N rounds since the last event", and they REDIRECT rather than recall
source: https://battlecode.org/assets/files/postmortem-2025-confused.pdf
origin: Battlecode 2025 confused and SPAARK; Battlecode 2020 confused; CodinGame Code Royale robostac (via sweep 17A)
evidence: documented
transfers: yes
---

## WHAT IT IS — arm (B) of sweep 23, and it resolves the library's own contradiction

This library holds two claims that appear to conflict:
[`branch-on-a-milestone-not-a-round-number`](branch-on-a-milestone-not-a-round-number.md)
(sweep 15) and sweep 17A's falsification of it via robostac's *"For the last 40
turns spend gold as fast as possible"* (re-verified verbatim for this sweep
against `https://raw.githubusercontent.com/robostac/cg-code-royale-postmortem/master/README.md`,
1 hit). **Read against forward dwell
specifically, they do not conflict — every surviving clock in the field is one of
three shapes, and none of them is a dwell budget.**

**Shape 1 — the idleness timer (a clock on the ABSENCE of events).** confused,
BC2025, under the heading *"To reduce unproductive wandering:"*:

> *"Implemented an idle timer, redirecting long-inactive units to the opposite side of the map center."*

**Referent check.** "units" are their soldiers/moppers; the stated purpose in the
next sentence is *"This ensured that most units would try to go towards the enemy
towers, guaranteeing their value."* **The timer does not recall the unit. It
sends it FURTHER FORWARD.**

**Shape 2 — the staleness clock on a *structure's* usefulness.** SPAARK, BC2025:

> *"For defense towers, if we haven't seen an enemy robot or paint in the last 30 turns, then we can probably disintegrate."*

Again: the clock measures **time since the last observation**, not time since
game start, and its action is a **conversion**, not a retreat.

**Shape 3 — the deadline on a SEARCH.** confused, BC2020:

> *"If after 180 rounds it still doesn't see the enemy HQ, it gives up on the rush and joins the rest of the miners and do normal miner stuff."*

(Already filed as
[`abort-the-scout-on-a-deadline`](abort-the-scout-on-a-deadline.md).) The clock
bounds an **unbounded search for a target**, not the time spent working on a
found one.

## WHY IT MIGHT TRANSFER

Our reported literals are `rnd + 60`, `STALL_RNDS = 25/36`, `GIVEUP_RND = 180`.
Against this taxonomy:

* `STALL_RNDS` **is already shape 1** if and only if it resets on progress — a
  since-last-event counter. That is the correct form and the field agrees with
  it. (`self.raid_stalls` exists at `bots/_v135loki18/main.py:90`.)
* `GIVEUP_RND = 180` is **shape 3 only if it bounds a search.** If it bounds
  *work at a found target*, it is the construct om nom named as the defect —
  see [`finish-the-task-before-you-withdraw`](finish-the-task-before-you-withdraw.md).
* `rnd + 60` as a dwell budget has **no precedent in 23 postmortems, PurpleWave,
  Steamhammer, or the Halite III 2nd/3rd writeups.** The census found zero
  instances of a competitor budgeting time-in-enemy-territory.

**And the redirect, not the recall, is the transferable action.** confused's
timer answers a unit that has produced nothing for N rounds by sending it
somewhere it might — which under `PLAY_DEFENCE: never` is the only answer we are
allowed to give anyway.

## WHAT WOULD KILL IT

* An idleness timer that redirects **toward** the enemy is only safe when the far
  side is where value is. On our ruleset it is (`R1000_IS_DEFEAT`), so the
  direction is right, but a redirect that walks a builder through a sentinel
  file is a worse outcome than standing still.
* All three shapes still carry a **tuned constant** (30, 180, "long-inactive").
  This is not an argument that constants are avoidable — it is an argument about
  **what the constant measures**.

## BUILDER HOOK

Audit the three literals against the taxonomy rather than retuning them: does
each one measure *time since last progress* (keep), *time bounding a search*
(keep), or *time in enemy territory* (delete — no precedent, and it is the one
that would produce our dwell number as a side effect rather than as a fix).
