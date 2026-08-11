---
tactic: Choose between a CONSUMABLE blocker and a PERMANENT one on a prediction of the incoming dose — the only conditional in the corpus that picks the FORM of defence rather than the amount
source: https://raw.githubusercontent.com/nknguyenhc/Terminal-Lostkids/main/README.md
origin: Terminal (Correlation One / Citadel), APAC region, team Lostkids — 3rd place overall
evidence: documented
transfers: yes
---

## WHAT IT IS

Every other defensive rule in this sweep decides HOW MUCH defence to buy. **Lostkids'
decides WHICH KIND, and the discriminator is a prediction about the attack's shape:**

> *"In the case where the enemy will likely spam scouts in multiple batches towards the
> side, we use interceptor rather than walls to block their attack."*

> *"In the case where the enemy will likely spam scouts in one batch towards the side, we
> use walls rather than interceptors to block their attack."*

**Interceptors are mobile, one-engagement units; walls are permanent structures.** The
rule reads: **a single large pulse is answered with a permanent structure; a repeated
stream is answered with a consumable.** That is the reverse of the naive intuition (which
would put the permanent thing against the repeated threat), and it follows from the
absorb-vs-attrit distinction — a wall spends its HP once and then is gone, while a
consumable can be re-bought every time the stream arrives.

**They compute the prediction rather than guessing it, from two named inputs:**

> *"Predict likelihood of enemy initiating a scout spam towards each side, based on enemy
> defense structures and mobile points."*

> *"Track enemy's attack pattern to adjust the mobile point threshold of when the enemy is
> going to attack."*

**They also state the condition under which the consumable arm fails**, which most
writeups omit: *"Our defense using interceptors is weak against enemies with upgraded
turrets in the frontline. The interceptors will be destroyed by the turrets before
intercepting the enemy scouts."*

## WHY IT MIGHT TRANSFER — against our ruleset

**We have exactly this dichotomy and we have never made it a decision.** Our defensive
options split cleanly into consumable and permanent, and they differ in the one currency
that matters most here — the **global additive scale factor**:

| form | titanium | scale | recoverable |
|---|---|---|---|
| **a builder body standing on a tile** | 0 (already alive) | 0 | yes — it walks away |
| **barrier** | 3 Ti | **+1%** | yes — `destroy` removes the contribution |
| **gunner / sentinel** | 20 / 30 Ti | **+20%** | yes, but the build is sunk |

**A body on a tile is the purest consumable defence in our ruleset and it is free.** It
blocks a lane, denies a spawn tile, and absorbs nothing but its own 40 HP — and unlike
every build, **it adds nothing to the scale factor that prices our raid**. A barrier is
the cheap permanent form; a turret is the expensive permanent form that also taxes every
future build by 20%.

**So the Lostkids rule instantiates here as: against a single decisive push, buy the
permanent thing; against sustained pressure, hold a body there and re-position it.** And
the cost asymmetry is much sharper for us than for them, because their walls do not
inflate the price of their offence and our turrets do.

**The prediction input is available and cheap.** Their *"mobile points"* is the enemy's
attack budget. Our nearest observable is the enemy's **live entity count and composition
within vision** — and note we cannot read their scale (`get_scale_percent()` is
team-keyed) or their titanium. **We would be predicting from unit counts and positions
only, which is a weaker instrument than theirs, and the plank must say so.**

## HOW IT MEETS `DEFENCE_ADMISSION_BAR: kill_round_non_regression`

**The consumable arm has the better claim and the permanent arm has the honest problem.**

* **Body-as-blocker clears the bar on cost grounds:** zero titanium, zero scale, and the
  body is one we already spawned. Its whole cost is the builder-turns it spends standing
  still — which is directly measurable and directly comparable to what those turns would
  have bought forward.
* **Turret-as-blocker is where the bar bites:** +20% scale on every subsequent build,
  including the harvesters and conveyors that fund the raid, is a kill-round cost that
  does not show up until many rounds later. **A kill-round bar measured over too short a
  horizon will not see it.** ⇒ Any leg testing the permanent arm must report the kill
  round over FULL games, not over the window the turret was built in.

**What would show it slowed the kill:** median kill round, plus **`get_scale_percent()` at
r150 and r250** in both arms. The scale trace is the mechanism by which a permanent
defensive build slows a kill, and it is directly readable — a rise in scale at equal
economy IS the tempo cost, made visible before the kill round moves.

## WHAT WOULD KILL IT

* **Their interceptor is a purpose-built counter-unit; our body is not.** An interceptor
  damages what it intercepts. Our builder **cannot attack an enemy builder at all** — its
  attack targets an adjacent *building* for 2 Ti / 2 damage. **A body blocks and dies; it
  does not trade.** That is a materially weaker consumable and the transfer must not be
  written as if we had theirs.
* **Terminal's arena is lane-based with fixed edges.** "Which side will they attack" is a
  well-posed question there and a much vaguer one on a symmetric 8x8–30x30 grid.
* **The dose-prediction half needs an instrument we do not have.** Without a read on the
  enemy's bank, "one batch or many" is guesswork. **The rule may still be usable with the
  branch hardcoded by map width** — which is a different, weaker tactic and should be
  pre-registered as such.
* One team, one league, no ablation, self-reported 3rd place.

## BUILDER HOOK

**Smallest test, and it is a substitution rather than an addition:** in whatever site our
incumbent currently answers a detected threat with a barrier or a home turret, answer it
instead by holding an already-spawned builder on the threatened tile for as long as an
enemy unit remains in vision, then release it. **No build, no scale delta, one predicate,
one release condition.**

Score it on median kill round, core-death rate, and **builder-turns spent stationary** —
the last of which is the plank's entire cost and is the number that decides whether it is
cheaper than the barrier it replaces.
