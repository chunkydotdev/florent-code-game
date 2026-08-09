---
tactic: The desperation index — count the turns you have been unable to execute a plan, and relax the plan's constraints as that count rises
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf
origin: Battlecode 2020, Java Best Waifu
evidence: documented
transfers: yes
---

## WHAT IT IS

Java Best Waifu wanted their buildings on ideal tiles, but a bot that waits for an ideal tile
can wait forever. Their solution was a per-building counter that measures **how long the plan
has been blocked while affordable**, and a schedule of thresholds that widen the acceptable
placement as the counter climbs:

> *"we called desperation index the number of such turns"*

**Referent check.** *"such turns"* is defined in the immediately preceding clause: *"We kept
track how many turns were we trying to build the same building and had the soup to do it"* —
so the counter increments only when the build was **affordable and still did not happen**. It
is a measure of *blocked-ness*, not of poverty.

> *"if our desperation index reached 8 we would build it also on Next to Wall Tiles, and if it
> reached 30 we would build it wherever we could"*

**Referent check.** The full sentence names the building — *"for instance we tried to build our
first Design School on an Interior Tile, however"*. Their tile classes (Interior / Next to Wall
/ Wall / Outer Wall / Holes) are a quality ordering, and the desperation index walks down it.

## WHY IT MIGHT TRANSFER

This is a small, cheap device that solves a failure mode our library keeps meeting from
different directions: **a bot that will not act until conditions are ideal is indistinguishable
from a bot that does nothing.**

Where it bites for us:

- **Turret seats.** Sweep 9's `runtime-density-siting` and `turret-threat-field` both propose
  scoring seats at runtime. A scorer with a hard acceptance threshold produces exactly Java Best
  Waifu's problem — on a map where no seat clears the bar, no turret is ever built. A
  desperation index converts that from a deadlock into a delay.
- **Our own measured shape is "we bank and do not spend."** We end r200-300 holding more
  titanium than Ouroboros while buying a twelfth as much ammunition. A counter that increments
  *only when we could afford the thing and did not build it* is a direct, one-integer instrument
  on that pathology — and it is exactly what the desperation index measures.
- **It is free.** One integer per plan in instance state on the unit that owns the plan; no
  store slot, no buffered-write latency, no last-writer-wins hazard, no titanium.

It also composes with the other files here rather than competing with them. It is the *third*
answer to "what if the condition never materialises", alongside
`abort-the-scout-on-a-deadline.md` (give up and go back to economy) and
`branch-on-a-milestone-not-a-round-number.md` (branch on what you have achieved). Abort, relax,
or re-aim — the field uses all three, and they are distinguishable: **abort when the plan has
become worthless; relax when the plan is still worth doing at lower quality.**

## WHAT WOULD KILL IT

- **Relaxing into a bad seat can be worse than not building.** A turret placed *"wherever we
  could"* inside an enemy sentinel's line (r²=32, ignores obstacles) is 20-30 Ti donated plus a
  permanent +20% on our own scale for that category. Java Best Waifu's tile classes were all
  *inside their own wall*; ours would not be. The relaxation ladder must have a floor that is
  still safe, not a floor of "anywhere legal".
- **The thresholds are theirs (8 and 30) and are unmotivated in the source.** What transfers is
  the mechanism.
- **It is not a trigger.** It cannot decide when to make contact; it only stops a decision from
  hanging. Filing it under (A) would be a category error — it belongs with the machinery.
- **Build legality here is strictly stronger than `is_tile_empty`**, so "wherever we could" must
  be enumerated through `can_build_*`, and a relaxation ladder that assumes a tile is buildable
  because it looks empty will raise `GameError` — which, uncaught, **permanently destroys the
  unit for the rest of the match**.

## BUILDER HOOK

Smallest test: instrument only. Add one counter per pending build plan that increments when
`get_global_resources() >= get_<entity>_cost()` and the build still did not happen, and `print()`
its distribution at game end. **If that number is large, we have located where the banking
pathology lives, in one battery, with no behaviour change.** Only then decide whether the fix is
to relax, abort, or re-aim.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
