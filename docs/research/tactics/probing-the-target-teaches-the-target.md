---
tactic: Testing a counter against the specific opponent it is meant to counter hands them the counter-counter
source: https://battlecode.org/assets/files/postmortem-2020-confused.pdf
origin: Battlecode 2020 / confused (2nd in the high school bracket, 6th on the scrimmage server)
evidence: documented
transfers: partial
---
WHAT IT IS — **The one documented cost of the "scrim upward" answer, and it is severe enough that
it must sit beside it.** confused, needing to beat one specific stronger opponent, deliberately
narrowed their bot to that matchup — *"we decided to basically overfit onto Kryptonite's team"* —
then copied the field's best-known counter to that opponent's strategy (*"We decided to copy Java
Best Waifu's rush defense strategy"*), and tested it the obvious way:

> *"we made the grave mistake of actually testing this feature against Kryptonite by requesting a
> lot of scrimmages"*

Kryptonite saw the games, understood the counter, and shipped the counter-counter: they began
*building net guns even before they reached the HQ*, which nullified the defence. confused's own
summary: *"What was worse was that they submitted their change right before the deadline so we
didn't have any time to respond."* The lesson they draw is stated flatly — *"We learned our
lesson of not requesting scrimmages to test out the feature that was supposed to be countering
that team."*

**Two distinct mechanisms are visible here and both matter:** (1) a scrimmage is a **two-way
information channel**, and the side being probed learns more from a targeted probe than the
prober does; (2) in a game with a submission deadline, **the last mover wins the exchange**.

WHY IT MIGHT TRANSFER — **Every ladder game we play is published to our opponents in exactly the
same way**, and BC2025's winner says so explicitly of his own league: *"Everyone can scrimmage
against your bot and see your strategy anyway"*. We are permanently live on a public ladder as
OpenSverige. Any narrow anti-top-tier mechanism we ship is therefore **visible to the top tier
from the moment it plays a rated game**, and it decays. That has a concrete implication for the
Loki directive: a trick's value should be scored on **the window before it is answered**, not on
its steady-state win rate, and the more precisely it is aimed at one named opponent the shorter
that window is. It also argues for the ordering *build → ship → read*, rather than *build → probe
the target → refine → ship*, since the middle step is the one that leaks.

WHAT WOULD KILL IT — **The transfer depends on facts about our league we have not established:
whether opponents can request games against us at will, whether they can watch our replays, and
whether they iterate on a human timescale at all.** Several of our opponents may be static
submissions that never update, in which case there is nothing to leak to and this file is inert.
It also depends on there being a deadline that ends the exchange — Battlecode's tournament
structure supplies one and a rolling ladder does not, which cuts both ways: no deadline means no
last-mover advantage against us, but also means our own window closes at whatever rate they
iterate. **INDEX's `play the players` mandate is unaffected either way; this file only prices the
leak.**

BUILDER HOOK — Cheap and purely observational: pick two or three top-tier opponents and check
whether their behaviour in our games has **changed over time** — same map, same seat, compare an
early-window replay to a recent one. If their opening is a constant across months, they are
static and nothing leaks. If it moves after our own submissions move, we are in confused's
situation and every narrow trick should be treated as a depreciating asset with an explicit
shelf-life estimate.
