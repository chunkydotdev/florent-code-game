---
tactic: What a team that climbed ~270 Elo says it changed (the one postmortem written from below)
source: https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf
origin: Battlecode 2025 / The Kragle (RPI) — 1533 at Sprint 1, ~1800 and 27th by the end
evidence: documented
transfers: partial
---
WHAT IT IS — Sweep 15 established that this library's evidence class is *winners describing
their own winning games*. **The Kragle's 2025 postmortem is the explicit exception, and it says
so in its own introduction:** *"Often, teams who make postmortems are those who have
consistently placed highly from the start."* … *"We have the perspective of a team that spent
years with no consideration of qualifiers, who this year became one of the higher level
contenders, going toe-to-toe with the 2 seed in the US qualifiers."* Their prior years were
*"typically holding a 1200-1500 rating, with no notable performances in any of the
tournaments"*; this year *"We came out of Sprint 2 at 1570 ranked 63rd, and finished the
competition around 1800, ranked 27th."*

**And what closed roughly 270 Elo was not a new weapon. It was conversion of a lead they were
already winning.** The section covering that climb opens with a diagnosis that reads like ours:

> *"Thanks to our excellent opening strategy, we often found ourselves with a resource lead,
> even against higher rated teams. However, our bot was fantastic at throwing leads."*

Two named defects follow. **Floating resources:** *"we could have a paint lead on paper, but if
all of that paint was not spendable, it wasn’t a paint lead in practice."* **Idle time:** *"a
robot-count lead means nothing if half of your robots are derping around"*. Neither is a
mechanism the top tier had and they lacked; both are failures to spend an advantage they
already possessed. Their stated general priority is the same shape: *"you can branch off into
working on converting the economy into the win condition"*.

WHY IT MIGHT TRANSFER — **The diagnosis is ours, almost word for word, and it was made by a team
at almost exactly our rating against opponents at almost exactly the gap we face.** INDEX's
standing context says *"We bank and do not spend. We end r200-300 holding more titanium than
Ouroboros while buying a twelfth as much ammunition"*, and *"We win the opening and we win the
clock; we die in the middle."* The Kragle had a bot that won the opening against higher-rated
teams and threw the lead in the mid-game, closed most of a 270-Elo gap, and attributes the climb
to spending what it had banked. In our ruleset the unspent resource has a specific name —
titanium that never became ammunition, and therefore never became damage, because **the core
converts titanium→ammo 1:1 at most once per team per turn with no passive income.** A bank that
is never converted is *exactly* their floating paint: a lead on paper that is not a lead in
practice. The idle half has a live analogue too: our own corpus shows a builder beside a damaged
core moves in **15.5% of rounds against 68.3% at full HP**.

WHAT WOULD KILL IT — Two things, and both must be stated. **(1) Their floating resource was a
per-building pool with a hard build threshold** (money towers stuck below 100 paint *"can never
build units"*); our titanium is a single global pool with no such trap, so the *mechanism* of
their bug does not exist here — only the category does. **(2) This is a single team's account of
its own climb, with no control.** Nobody, per sweep 15's measured negative, separated cause from
marker anywhere in this corpus; The Kragle changed several things at once between Sprint 2 and
Qualifiers and reports the aggregate. Treat it as a *hypothesis with an unusually good
provenance*, not a proven dial.

BUILDER HOOK — The cheapest instrument is descriptive, not an A/B: over our own replays, plot
**titanium held** against **round** for games we lose from an opening lead, and put a number on
the peak unspent bank in the r150-300 window where INDEX says everything breaks. If the curve
shows a large bank rising while ammunition stays flat, we have measured the Kragle defect in our
own bot, and the plank is a **spend rule** rather than a new mechanism. Note the arena is still
the only verdict instrument.
