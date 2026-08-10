---
tactic: The one benchmark that MEASURES a feint — and the pure "lure the defenders off the core, then hit the core" scenario scored ZERO for all 21 algorithms
source: https://arxiv.org/pdf/2509.12927
origin: HLSMAC (Hong et al. 2025), a StarCraft II multi-agent benchmark of 12 scenarios built from the Thirty-Six Stratagems, evaluated over 21 MARL algorithms
evidence: documented
transfers: partial
---
WHAT IT IS — **The only quantitative measurement of a deception play found anywhere in this
sweep, and it measures the thing our programme most wants: bait the defenders away, then kill the
base.** HLSMAC builds SC2 scenarios whose *intended* solution is a named stratagem, then reports
win rates for 21 published multi-agent RL algorithms.

**Scenario `sdjx` — feint east, strike west:**

> *"– If our units approach the enemy's main base, the enemy forces will retreat to defend it,
> leaving the expansion base undefended. – If we engage the enemy directly, we will likely lose. •
> Expected solutions: – Two Medivacs feign an attack on the enemy's main base, causing the enemy
> forces to leave their expansion base. – Our main force attacks the enemy's expansion base."*

**Scenario `dhls` — lure the tiger down the mountain, i.e. exactly Loki's dream play:**

> *"• Game mechanisms: – The enemy forces are defending their base. – If any of our units dies
> during the engagement, the enemy forces will advance from the Command Center to attack our
> Hatchery. – If we engage the enemy directly, we will likely lose. … • Expected solutions: – A
> small group of our units lures the enemy forces away. – Our main force attacks the enemy base."*

**The results split the two hard.** Reading the `sdjx` column of the 21-algorithm win-rate table:
**14 of 21 algorithms score exactly 0.00**; two score 0.14 and 0.32; **five score 0.72–0.89**
(CWQMIX 0.83, Qatten 0.88, QPLEX 0.86, RESZ 0.72, dTAPE 0.89). **The feint is not a gradient, it
is a cliff — you either find it or you never find it at all.**

**And `dhls` — the pure lure-then-strike — is not in the table.** The caption reads
*"Win Rates Across 21 MARL Baselines on Non-zero Scenarios (with dhls, fkwz, tlhz, yqgz
excluded)"*, and the exclusion rule is stated separately: *"Note that scenarios where all
algorithms achieved zero win rates are excluded from the table presentation."* **Taken together:
every one of the 21 algorithms scored 0.00 on the scenario whose intended solution is "lure the
defenders off, then attack the base."**

**One more result belongs here, because it is a warning about how we would score our own leg.** The
authors checked whether a high win rate meant the stratagem was actually performed:

> *"win rate in adcc, but replay analysis reveals it does not actually follow the intended
> stratagem approach."*

(The subject is the algorithm RIIT, which scored 0.93 on scenario `adcc`.) **A team can win the
deception scenario without deceiving anybody.**

WHY IT MIGHT TRANSFER — **it is the only place anyone has put a number on the play the programme
is built around, and the number is a warning rather than an encouragement.** Two things carry:

1. **Execution, not concept, is the binding constraint.** Note the crucial property of this
   benchmark: **the opponent's overreaction is guaranteed by the scenario designers** — *"the
   enemy forces will retreat to defend it"* is a scripted game mechanism, not a learned policy.
   **So this measures the feint under ideal conditions, with a victim built to fall for it, and
   most agents still scored zero.** Whatever the difficulty of feinting is, it is not mostly about
   the victim.
2. **RIIT's result is the falsifier design we need.** Our own leg must check that the mechanism
   fired, not only that the outcome moved — which is this repo's standing instrument rule
   (a check that has never produced the other verdict has not been seen to check).

WHAT WOULD KILL IT — **the population is wrong for us in three ways, and they all cut the same
direction.** (i) These are *learning* agents discovering a play from reward; we hand-author
behaviour, so "13 of 21 could not find it" is a statement about exploration, not about whether an
authored feint works. (ii) The scenarios are *asymmetric puzzles* with scripted opponents and
fixed unit compositions, not a symmetric 1v1 ladder. (iii) `dhls`'s all-zero result is inferred by
combining the table caption with the stated exclusion rule — the paper does not print "dhls = 0.00"
in so many words, and **that inference should be quoted as an inference, never as a printed
figure.** What would *strengthen* the file is a version of the paper reporting the excluded
scenarios explicitly.

BUILDER HOOK — **none as a plank; use it to set the leg's shape if the family is entered at all.**
If we ever run a lure leg, pre-register **two** measurements, not one: (a) the outcome —
core_kill_share and time_to_core_kill; and (b) **the mechanism — did enemy units actually leave the
core's neighbourhood in the rounds after the bait appeared?** HLSMAC's RIIT result is the concrete
precedent for (a) moving while (b) never happened. If (b) is flat, the leg is a null regardless of
(a), and it should be banked as one.
