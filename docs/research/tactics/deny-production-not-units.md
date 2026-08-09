---
tactic: (A) THE FIELD'S CONVERSION DOCTRINE IN ONE SENTENCE — you do not win by trading what exists, you win by closing the opponent's ability to make more; two contest-strong authors state it independently
source: http://satirist.org/ai/planetwars/strategy.html
origin: Planet Wars 2010 / Jay Scott; independently CodinGame Ghost in the Cell / Agade (1st place)
evidence: documented
transfers: partial
---
WHAT IT IS — Jay Scott's Planet Wars strategy page has a section called "trading
down", which opens by stating the intuition that grinding a material lead down to
zero should win, and then refutes it:

> *"You don’t win by trading existing ships, you win by closing the enemy’s supply
> of new ships by taking all their planets."*

> *"At heart, trading down is not a winning maneuver but a risk reduction
> maneuver."*

The same principle, arrived at independently by the winner of a different contest
in a different genre. Agade, on how he used Ghost in the Cell's single most
valuable irreversible resource:

> *"My goal with bombs is to deny production, the killing of units being too
> uncertain."*

Referent: "bombs" are the one-shot area weapon, of which each player gets two; the
alternative use he is rejecting is killing massed units.

Note what these two are *not* saying. Neither says "attack more". Both say the
target selection is wrong: **the thing worth destroying is the opponent's
production, not their stock.**

WHY IT MIGHT TRANSFER — Only partly, and the boundary is where the interest is.

The doctrine imports because our attrition arithmetic is worse than theirs. Trading
1.80 HP/Ti of damage against 4.00 HP/Ti of healing means "trading down" against a
healing defender is not even risk reduction here — it is a 2.2:1 donation. If the
field's answer to "how do you convert" is *cut production, don't trade*, then our
version of production denial is the question worth asking.

But our production is unusually hard to deny, and this is the part that must be
said plainly rather than glossed:

- **The core cannot be denied.** It spawns builders from a global titanium pool, on
  a 12-tile ring, and it is the target itself. There is no separate factory to kill.
- **Harvesters are the one deniable production asset**, at 20 Ti and +5% scale, and
  they sit on fixed ore tiles — a known, enumerable set. `ore-tile-denial` already
  holds the pre-emptive half of this.
- **Titanium delivery can be interrupted** by killing conveyors at 20 HP, which is
  by far the cheapest thing on the board to destroy.

So the doctrine points at **conveyors and harvesters**, not at the core — and that
collides with the programme's currency. Killing their harvesters raises our
tiebreak position on key 2 (harvesters alive is a comparison, so removing theirs
counts) and starves the titanium that funds their heal, but it does **not** produce
a core kill by itself. It is a way to make the *later* kill affordable, not a
substitute for it.

The honest reading is therefore a sequencing claim, and it is the same sequencing
[`the-crunch-is-a-rate-race-not-a-damage-race`](the-crunch-is-a-rate-race-not-a-damage-race.md)
arrives at from BC2020: **the defender's reserve is titanium, titanium is HP at
4.00 HP/Ti, and the way to beat a reserve is to stop it being refilled** before
opening fire on the thing you actually want dead.

WHAT WOULD KILL IT — Planet Wars planets and Ghost in the Cell factories are
*capturable* — taking one moves production from them to you, a double swing. Our
harvesters and conveyors are only destroyable; killing theirs costs us titanium and
gains us nothing but their loss. That halves the value of the doctrine before it
starts, and it is why this file is `transfers: partial` rather than `yes`.

It would be killed outright by a measurement showing enemy titanium income is not
what funds the heal that stops our sieges — for instance if the field's defensive
healing is funded from the 500 starting bank and passive income alone, in which
case starving harvesters changes nothing on the timescale of a siege. Nobody has
checked what a defending opponent's titanium balance actually does while it is
repairing a core.

BUILDER HOOK — Before building a commit gate, run the corpus cut it depends on: in
games where we besieged an enemy core, what was their titanium income doing? If
their heal is income-funded, denial-then-siege is the sequence and this file is
load-bearing. If their heal is bank-funded, denial buys nothing inside a siege
window and the sequencing claim collapses to the clearance phase alone.
