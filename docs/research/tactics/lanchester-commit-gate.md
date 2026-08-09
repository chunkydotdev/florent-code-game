---
tactic: Lanchester attrition predicate as an attack/retreat gate
source: https://cdn.aaai.org/ojs/12780/12780-52-16297-1-2-20201228.pdf
origin: Stanescu, Barriga & Buro, AIIDE-15 (StarCraft)
evidence: documented
transfers: yes
---
WHAT IT IS — an O(1) closed form replacing combat simulation. Per-unit strength
`alpha_i = dmg(i) * currentHP(i)`; army `alpha_A = sum(alpha_i)/A`. Attack iff
`alpha_A * A^n > beta_B * B^n`, with **n ~ 1.56** the empirically best fixed
attrition order. Survivors `A_f = ((alpha A0^n - beta B0^n)/alpha)^(1/n)`.

WHY IT MIGHT TRANSFER — it is arithmetic only, so it fits a 10 ms/unit budget
where a playout does not (measured: a 50-unit playout is 55.5 ms). And it has a
**measured effect on exactly our failure mode**: swapping UAlbertaBot's
attack/retreat rule for this moved it 41.6% -> 63.9% win rate with **no training
data**, using the default `dmg x HP` strengths. Our bot has no explicit commit
predicate at all.

WHAT WOULD KILL IT — Lanchester assumes an open field. Our sentinel ignores
obstacles (r^2=32, dmg 18) and a defender behind a barrier at a choke gets an
advantage the raw alphas do not capture, so attacker alpha must be discounted
when engaging through a choke. It also says nothing about buildings: a 500 HP
core with no damage output is not an army.

BUILDER HOOK — a `_should_commit()` returning the predicate, logged (not acted
on) for one battery, so we can see how often it would have fired in the r200-300
window before wiring it to anything. Add a round-decay term so the required
margin falls toward 1.0 as r1000 approaches — otherwise two bots both running a
correct gate never fight, which is the stalemate we are already in.
