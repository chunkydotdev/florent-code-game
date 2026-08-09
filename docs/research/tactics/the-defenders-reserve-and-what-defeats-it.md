---
tactic: FAILURE MODE — a held reserve stops single-wave attacks outright; only SUSTAINED chip beats it
source: https://battlecode.org/assets/files/postmortem-2019-oak.pdf
origin: Battlecode 2019 / Oak's Last Disciple; corroborated by Screeps tower-drain doctrine and Tigga's attacker/defender asymmetry
evidence: documented
transfers: yes
---
WHAT IT IS — The cheapest anti-rush ever recorded in Battlecode was not a unit or
a wall. It was **not spending everything**, and it was worth an entire tier:

> *"saving a bit of resources could stop all turn-1 rushes and gave us the edge
> later on. Literally, our bot went from F-tier to S-tier in 1 day."*

And in the same postmortem, the thing that beat the reserve — which is the part
that matters for us:

> *"Even though by saving some resources you could repeal each of the preacher
> waves, the preacher attacks did damage in a 3x3 area, hurt your castle little by
> little and ended up destroying it."*

The reserve absorbs a **wave**. It does not absorb an **integral**. Screeps
encodes the same principle as its standard opening attack — exhaust the defence's
upkeep, then walk in. From the ScreepsPlus community wiki:
> *"it is possible to tank though their damage from a far and 'drain' the tower of
> energy"*
> *"Depending on how well/robust the defending player's refilling of their towers
> is, this can open up windows to attack walls or rush the towers to destroy them
> before they can refill them."*
Referent: "this" is the tower-drain described in the immediately preceding
sentence.

Tigga, on why the asymmetry is structural rather than incidental:
> *"The attacker has to do everything right every tick. The defender just has to do
> something right occasionally."*
and the one edge he concedes the attacker:
> *"The attacker has two advantages - nukes and the ability to determine when the
> fight takes place."*

WHY IT MATTERS HERE — Our defender's reserve is **titanium**, and it is exactly
the same currency as their heal: heal is 1 Ti for +4 HP. So an enemy sitting on
banked titanium *is* sitting on banked HP at 4.00 HP/Ti, and our attack converts
their bank into their defence at a rate we lose 2.2:1. Oak's finding says a
single strike against a defender with a reserve is the worst case for us, and the
heal arithmetic says why.

But the second Oak quote names the escape, and it lines up with our own standing
crack. What beat the reserve was **cumulative damage that never let the target
recover**, not a bigger single hit. The library's version: *"**our** defender's heal
is adjacency-capped at ~16 HP/round per tile while the attacker's damage on that tile
is capped only by titanium"* — concentration, not more damage.
*(Quote corrected 2026-08-09, s26: this file rendered it as "**the** defender's",
which generalises a statement `INDEX.md` makes about **our** defence into a claim about
defence in general. Same near-miss caught in a sweep-17A draft the same day — the
subject-drift family, in the quote layer.)* A reserve is
titanium; the adjacency cap is a **rate**; titanium cannot be spent faster than
adjacency allows. **The reserve is beaten by exceeding the rate, and only by
that.**

That gives a hard commit threshold rather than a vibe. Against the field's
measured 2.68 healers (~10.7 HP/round) a sentinel at 9 HP/round is *below* the
line and donates; two are barely above it; the exchange only becomes decisive at
three or more. Against a defender who fills the cap on a 2x2 core (~32 HP/round)
the line is four sentinels. **Any Loki strike that cannot put ≥3 sentinels' worth
of damage on one target tile is, by our own arithmetic, feeding the reserve.**
(That arithmetic is mine, from the library's published rates — label it inference,
not a source claim.)

WHAT WOULD KILL IT — Tigga's asymmetry cuts against sustained pressure too: our
sustained attacker is a 40 HP immobile sentinel inside their base, and *"the
attacker has to do everything right every tick."* Sustained chip requires the
chipping asset to survive, and ours cannot retreat. The Screeps drain analogue is
also weaker than it looks here: their towers spend a **stored, refillable** energy
that a drain can outpace, whereas our turrets fire from a **global** ammo pool the
core tops up 1:1 from titanium with no travel and no refill logistics — there is
no supply line to cut. `ammo-drain-baiting.md` already holds the live version of
that idea; this file is its boundary condition.

BUILDER HOOK — A **commit threshold**, not a trigger: never open fire on the enemy
core until the number of our turrets bearing on it clears the measured heal rate
with margin. In code that is the sweep-2 gate made quantitative — count bearing
turrets via `can_fire_from`, count enemy builders adjacent to the target tile,
and require `9 * bearing >= 4 * adjacent_healers + MARGIN`. Until then, hold fire
and keep converting titanium to ammo. Sub-threshold fire is the 2.2:1 donation.
