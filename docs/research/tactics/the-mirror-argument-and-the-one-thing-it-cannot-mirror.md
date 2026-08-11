---
tactic: THE COUNTERWEIGHT — the strongest published argument that defence simply wins is the MIRROR argument, and it names its own two exceptions: choosing when the fight happens, and bugs in the defence code
source: https://screeps.com/forum/topic/2809/encouraging-more-combat-at-high-gcl
origin: Screeps official forum, "Encouraging more combat at high GCL" — Tigga (a top-GCL player) and likeafox
evidence: documented
transfers: partial
---

## WHAT IT IS

Sweep 24 was briefed to find where defence PAID and where it cost the kill. **This file
is the honest counterweight: the sharpest statement in the corpus that defence structurally
wins, filed so nobody has to rediscover the argument against our own doctrine.**

Tigga, replying to a claim that Screeps' designers intended it (*"But I did hear/read that
this was intentional, the developers wanted to allow the perfect defense"*):

> *"In the no-power world defense should always win. This is because you can just employ
> the mirror strategy - whatever the other guy does you do the same. You have towers, so
> you win with equal code."*

> *"It's pretty much impossible to remove the defender's advantage while towers are a
> thing, and that's fine. Right now I feel it's too high and winning is too easy on
> defense."*

**The mirror argument is a third mechanism, distinct from the two in
[`defenders-advantage-has-exactly-two-mechanisms`](defenders-advantage-has-exactly-two-mechanisms.md)**
(reinforcement distance, and production time bought by it). It is a SYMMETRY argument:
if both sides can build the same static defence and the defender additionally has it
already standing, then equal code means the defender wins, and no amount of attacker skill
at parity breaks it.

**And in the same thread he names exactly what the mirror CANNOT copy:**

> *"The attacker has two advantages - nukes and the ability to determine when the fight
> takes place."*

**A second player names the third, and it is the one that matters most to us:**

> *"I think most high GCL attacks are focused on bugs in the defense code, since direct
> attacks will be degraded into a war of attrition."*

## WHY IT MATTERS HERE — the transfer, and where it breaks

**Our game satisfies the mirror argument's premises almost exactly, and that should be
uncomfortable.** Maps are symmetric by reflection or rotation. Both teams have the same
entity list, the same base costs, the same 500 Ti start, the same passive income, and a
cost-scale factor that is **team-keyed and cannot be inflated by an enemy**. A defender who
mirrors our build order gets our structures plus a head start on siting them. **On the
symmetric-parity reading, our own programme's `KILL_WINDOW_RND: 250` is asking for the
thing this argument says cannot be had at parity.**

**So the whole content of our line is in the two exceptions, and both are live here:**

1. ***"the ability to determine when the fight takes place"* is ours by construction.** The
   defender must be ready every round; we must be ready once. Our median kill lands at
   r174 against a median death at r187 — **a thirteen-round race we currently win on
   average**, which is a timing advantage, not a strength advantage.
2. ***"most high GCL attacks are focused on bugs in the defense code"* IS the LOKI
   programme, stated by somebody else's competitive ladder.** Crash-induction is approved and shipped
   (`bots/_v131loki14`); `tools/crash_census.py` measures **2,451 unexplained unit removals
   by opponents across 1,855 of our games against 0 by us**. **An exception the mirror
   cannot copy is one where our opponents' code fails and ours does not — and that is a
   code-quality asymmetry, not a resource one.** It is the only channel in this file that
   parity does not close.

**⇒ The mirror argument does not refute our line; it explains why our line is the two
things it is.** And it is a genuine warning against the third thing: **any plank that wins
by out-building an opponent at parity is the arm the mirror argument closes.**

## HOW IT MEETS `DEFENCE_ADMISSION_BAR: kill_round_non_regression`

**It supplies the reason the bar has to exist at all.** If defence wins at parity, then
every marginal unit of defence looks locally profitable on a survival metric, and a bot
optimised on survival alone converges on the turtle — which the same thread's players
describe as the state their game is stuck in, and which
[`turtling-persists-because-nobody-punishes-it`](turtling-persists-because-nobody-punishes-it.md)
independently attributes to opponents who do not adapt. **`kill_round_non_regression` is
the term that stops that gradient.** It is not a stylistic preference; it is the only thing
in the programme pointing the other way from a real local optimum.

**What would show a plank slipped down that gradient:** median kill round rising while
core-death rate falls — **both moving, in opposite directions, is the turtle signature**,
and it is a pattern a win-rate-only bar would score as a success.

## WHAT WOULD KILL IT

* **It is forum argument, not measurement.** No n, no experiment, and the participants
  disagree with each other in the same thread (Nicle: *"Perfect defense should be
  possible"*). **It is a strong statement of a mechanism, from players who ship, and it is
  not evidence about our engine.**
* **Screeps has no round limit and no core to kill.** Its equilibrium is a permanent
  standoff; ours ends at r1000 with a tiebreak we have declared a defeat. **The mirror
  argument's conclusion ("defence always wins") is therefore conditional on a game where
  nothing forces resolution — and our clock does force one.**
* **Their towers are cheap relative to the economy and ours are not.** Our gunners and
  sentinels each add +20% to a global multiplier on *every* subsequent build. **A mirroring
  defender pays that tax too, which weakens the symmetry in our favour**: the defender who
  mirrors our turret spend has also mirrored our price increase, while we have the option
  to spend on bodies (0 scale) instead.

## BUILDER HOOK

**None — this is a framing file and should not produce a plank.** Its operational content
is one prohibition and one priority:

* **Prohibition:** do not pre-register a plank whose theory of victory is "we out-build a
  symmetric opponent's defence". The mirror argument closes that arm and the library has
  no counterexample to it.
* **Priority:** the two exceptions — **timing** and **their code failing** — are where the
  budget goes. Both are already programme, and this file is external corroboration from a
  league that arrived at the same two by watching its own metagame stall.
