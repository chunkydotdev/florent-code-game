---
tactic: THE ORGANISERS' STATED OBJECTIVE FUNCTION — a logarithmic time+skill vs performance curve, and any strategy that puts a discontinuity in it gets patched out
source: https://github.com/Lux-AI-Challenge/Lux-Design-2021 (ChangeLog.md v3.0.0 "Motivation", local raw fetch)
origin: Lux AI Challenge Season 1 (2021) — organisers' changelog
evidence: documented
transfers: no
---
WHAT IT IS — A rare thing: designers writing down the objective function they are
balancing towards, and naming the exploit that violated it. The quote carries the
demonstrative *"this simple strategy"*, so the exploit is quoted with it:

> *"Previously you could exploit the following simple strategy and win quite easily with little effort: Build a long line of CityTiles. At the head of it, stack all of your worker units. Now as you move this line of CityTiles to new resource locations, the stack of worker units will all instant mine and deposit resources as fuel extremely fast and this is very unbalanced. Our goals with game designs are to always maintain some kind of logarithimc curve on a time+skill vs bot performance graph, with this simple strategy adding a discontinuity to that."*

Referent: *"this simple strategy"* is **the CityTile-line-with-stacked-workers
exploit described in the immediately preceding sentences**, quoted above. The typo
`logarithimc` is theirs and is preserved.

The patch that removed it, in the same v3.0.0 block, is a mechanic deletion rather
than a nerf — *"Workers can no longer mine while on a CityTile."*

**The claim being made is about the shape of the reward curve, not about balance.**
A discontinuity means a small amount of the right knowledge buys a large jump in
performance. The organisers state that they will remove those on sight, on the
explicit ground that they want returns to effort to be smooth and diminishing.

WHY IT DOES NOT TRANSFER — We do not design a league, and nothing here is a tactic.
Filed as `transfers: no`, and filed anyway because **it is a counterweight to an
assumption this programme makes without stating it.**

Our programme is looking for a discontinuity. `KILL_WINDOW_RND: 250`, the whole
incidence re-aim, the search for "what converts" — all of it presumes there is a
step change available: a thing that, once known and built, moves us from a
tiebreak-grinding 1603.6 to something near a 2000+ tier. That is precisely the shape
Lux's organisers say they delete from their game. **Two independent design teams in
this sweep are documented removing decisiveness levers** — this one, and the wood-
regrowth patch in
[`they-made-the-resource-renewable-to-weaken-denial`](they-made-the-resource-renewable-to-weaken-denial.md).
17A already found Battlecode's devs steering *away* from rushes via the map pool and
Halite II's organisers **vetoing** an elimination timer outright.

So the sourced picture across five leagues is one-directional: **designers reduce the
payoff to sharp aggressive strategies more often than they increase it.** BC2020's
deletion of the score fallback is the single documented counterexample.

**This is not an argument that no discontinuity exists in our game.** Our organisers
are not Lux's, our ruleset is not balanced by the same hands, and an unbalanced
league is exactly where a discontinuity survives. It is an argument that the prior
should be lower than the programme currently sets it, and that the alternative
hypothesis — *our returns to effort are smooth, and the road up is many small
correct things* — is the one the field's own designers are actively engineering
towards.

WHAT WOULD KILL IT — Evidence that our organisers balance in the opposite direction,
or any measured step change on our own ladder. The library has one candidate already
and it points the wrong way for smoothness: the `r = +0.767` correlation between
rating and core-kill rate across 53 third-party teams. That is a strong *linear*
relation, not a step, which is itself weak evidence for the smooth reading.

BUILDER HOOK — none. The procedural consequence: **when a sweep proposes a lever
whose value comes from a sharp exploit, check whether comparable leagues patched the
same shape out.** Two of this sweep's twelve candidates were designer-nerfed
elsewhere; that is a high enough base rate to make the check worth its cost.
