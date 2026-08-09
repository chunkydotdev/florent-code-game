---
tactic: THE SHARPEST FINDING OF THE SWEEP — an economically-correct evaluator never finishes, because the last increment of kill progress has zero economic return; two leagues fixed it with an explicit non-economic bonus term
source: http://satirist.org/ai/planetwars/
origin: Planet Wars 2010 / Jay Scott's oddshrimp 4.3; the same failure mode independently in Steamhammer (StarCraft)
evidence: documented
transfers: yes
---
WHAT IT IS — Jay Scott's Planet Wars bot searched for the materially best move and
therefore would not spend ships taking planets that produce nothing. The result
was games it dominated and did not end. His fix, from the oddshrimp4.3 version
notes:

> *"One tiny tweak is to add a small bonus in the move generator for captures of
> enemy planets. It makes the bot a tad more aggressive, but the real point is to
> allow it to take 0-growth enemies if nothing else beckons. It stops a tiny
> proportion of games from looking silly when the enemy survives to the end
> owning only a 0-growth planet surrounded by oddshrimp’s vast fleets."*

Referent: a "0-growth planet" produces no ships, so capturing it has **no
material return** — a purely material evaluator will never pay for it, and Planet
Wars' win condition (eliminate the opponent, else most ships at turn 200) is
therefore never reached. The fix is a term in the move generator that has nothing
to do with value.

The **same failure mode, independently, in a different league and a different
genre.** Steamhammer's anti-air suicide units are hard-coded not to waste
themselves on floating buildings, which is correct cost-efficiency and is exactly
what stopped the kill. Its author, listing what went wrong in a game he could not
finish:

> *"The scourge might have understood that when only floating buildings are left,
> they are good targets."*

Referent: "the scourge" are Steamhammer's own scourge units; "floating buildings"
are the last two enemy structures, which were the only thing standing between it
and a win.

Two authors, two games, one shape: **the rule that makes you efficient is the rule
that stops you finishing, and the fix is a term that is deliberately not about
efficiency.**

WHY IT MIGHT TRANSFER — This is, on the evidence of this sweep, the best
explanation available for our measured incidence gap, and it is *mechanically*
true of our ruleset rather than merely analogous.

Killing the enemy core returns **nothing economic**. It delivers no titanium, adds
no harvester, and improves no tiebreak key. Every titanium spent on it is
titanium not spent on conveyors (tiebreak key 1), harvesters (key 2) or the bank
(key 3). Under our own arithmetic it is worse than neutral: damage is 1.80 HP/Ti
against a heal of 4.00 HP/Ti, so an attack that does not finish is a **2.2:1
donation**. Any evaluator that prices actions by return — and the library's
standing complaint that *"we bank and do not spend"* suggests ours effectively
does — is *correct* to never commit, and will grind by construction.

That reframes the incidence gap. It may not be that we lack a mechanism for
killing cores. It may be that **nothing in our bot ever pays for one**, because
the payment has no accounting justification until the moment the core dies.
Jay Scott's answer is that the term must be **small and unconditional** — "a
small bonus… if nothing else beckons" — not a large one, and not gated on
advantage.

WHAT WOULD KILL IT — Jay Scott's bonus was cheap because his losing move was
cheap: ships that had nothing better to do. Our equivalent purchase is a sentinel
at 30 Ti with **+20% scale on every subsequent one**, placed inside the enemy kill
zone where it cannot retreat. A "small bonus if nothing else beckons" that buys a
sentinel is not small. So the honest transfer is not the magnitude, it is the
**shape**: a term that exists at all, and that is not justified by return.

It would also be killed outright by a measurement showing our bot already spends
on the core and simply loses those exchanges — in which case the problem is
execution, not accounting. The library has the raw material to check this
(ammo conversion, turret production, forward placement all measured as breaking
at r150) and has never framed the cut this way.

BUILDER HOOK — The smallest version, and it is deliberately tiny: when the build
decision has titanium left over after its normal priorities are satisfied, prefer
a turret bearing on the enemy core over the marginal conveyor — with **no
condition on whether we are ahead**. Then measure core-kill incidence and
delivered titanium together. Jay Scott's claim is that this costs almost nothing
and converts the games that were already won; if it costs us delivered titanium
without buying incidence, the term is too expensive here and the finding does not
transfer at our prices.
