---
tactic: The shape of a loss to a much stronger bot — parity in the opening, divergence after the opening
source: https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf
origin: Battlecode 2025 / The Kragle, reporting two sweeps against rated opponents (1737 and 2017)
evidence: documented
transfers: partial
---
WHAT IT IS — The Kragle report two 5-0 sweeps against much stronger teams and describe *where in
the game* the gap opened, with the opponents' ratings attached. **Against a ~200-Elo superior:**

> *"We faced against the 10 seed immutable, who had a rating of 1737 at the time, and got swept
> 5-0. We kept up in the early game"* … *"after some starting territory was established, they
> always pulled away with a commanding lead"*

(The Kragle were rated 1533 at that tournament; the subject of *"we kept up"* is their own
opening, and the subject of *"they always pulled away"* is immutable.)

**Against a ~460-Elo superior:** *"we were against the 2 seed Super Cow Powers with a rating of
2017. We were no match for them and lost 5-0. While they simply did everything better than us"*
— followed by three specific differences (a stronger economy from a denser pattern, a better
unit mix, better exploration).

**The two gaps have different shapes and that is the finding.** At ~200 Elo the loss is
*localised in time*: opening parity, mid-game divergence. At ~460 Elo the loser can name no
single locus — *"they simply did everything better than us"*.

WHY IT MIGHT TRANSFER — **It gives us a discriminating measurement rather than a tactic.** INDEX
already says we win the opening and die in the middle, and that the chance a core kill is ours
falls monotonically after r150. The Kragle's account says that profile is the signature of a
**~200-Elo gap, not a ~460-Elo one** — which is a testable claim about where CtrlAltDefeat-class
opponents sit versus sporks-class opponents. If our replays against 1900+ opponents show the same
opening parity that our replays against 1550 opponents show, the gap is mid-game conversion and
The Kragle's remedy applies. If instead we are behind from r0, we are in the *"everything better"*
regime and no single plank closes it.

WHAT WOULD KILL IT — **This is one team's narration of five-game sets, n small, with no
instrumentation.** "Kept up in the early game" is an impression from watching replays, not a
measured parity. And the ratings are Battlecode's own Elo on its own map pool; the arithmetic
mapping of "200 Elo" between two different leagues' rating systems is not something this source
supports. Do not treat the 200/460 boundary as a constant — treat the *ordering* as the claim.

BUILDER HOOK — Split our existing replay corpus by opponent rating band and compute, per band,
the round at which our resource or structure differential first turns negative. One number per
band. If that round moves *earlier* as opponent strength rises, we are watching the Kragle
transition from "mid-game divergence" to "behind from the start", and it tells us which class of
fix is even eligible. No bot change; corpus query only.
