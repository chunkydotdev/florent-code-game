---
tactic: Blind their gunner with THEIR OWN builder — the launcher as the delivery mechanism
source: https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
origin: Battlecode 2021 Wololo (winner) — "dilution" micro; the application to our gunner lane is inference by tactics sweep 11 (this agent)
evidence: documented (the principle) / inference (our application), resting on two measured engine facts
transfers: partial
---

WHAT IT IS — **spoiling the opponent's own attack by controlling who stands in
it is winner-level micro, not a gimmick.** Wololo won Battlecode 2021 with a
minimax movement policy whose explicit terms included deliberately standing units
where the opponent's own strike would be wasted:

> *"Small units would stand next to large opponent politicians which attempted to
> empower to convert an EC, so that the conviction they empowered with was
> diluted and wasted up until the point that the opponent was no longer able to
> convert the EC."*

> *"Large units attempted to dilute an opponent politician’s empower conviction if
> doing so would prevent a smaller friendly unit from being converted and/or
> removed."*

and the emergent case they call out as the highest-value one — a single body,
recycled, denying the same objective indefinitely:

> *"this burier would often be able to micro to greatly dilute the empower
> conviction of any opponent politician who attempted to convert the neutral EC,
> causing the conversion to fail, after which another single burier would come to
> replace the first one, and could do the same, massively delaying the opponent
> by causing the opponent to repeatedly fail to convert the neutral EC"*

**Our engine has no area damage and therefore no dilution.** What it has instead
is a stronger version of the same idea: **the object that spoils their shot can
be their own unit, and we can put it there.**

WHY IT MIGHT TRANSFER — the mechanism is three measured facts, in a chain:

1. **A gunner's line is blocked by bots and buildings** — s23 probe, the gunner
   was the positive control and `can_fire_from` flipped **True → False** with a
   body in the lane (`docs/research/turret-line-blocking-2026-08-09.md`).
2. **The launcher picks up an adjacent builder bot from EITHER team and throws it
   to any passable tile** within r²=26 — no ammo, no titanium, facing-independent.
3. **Turret fire hits whatever unit stands on the target tile, own team
   included** — verified in our replays, not assumed
   (`docs/research/builder-death-attribution-2026-08-09.md`; the toolkit's
   validated case has a gunner shooting its **own** builder bot on rounds 62-89,
   **13 hits, 56 damage, killing it**).

So a single `launch()` puts their builder in their own gunner's lane, and they
are left with three answers, all of which cost them and none of which cost us:

| their answer | what it costs them |
|---|---|
| don't shoot | the gunner is blanked for as long as the body stands there — **0 Ti to us** |
| shoot anyway | **4 ammo (= 4 Ti, no passive income) spent on 7 damage to their own unit** |
| `rotate()` to a new facing | **10 Ti + 1 action cooldown**, gunner-only, and repeatable against us |

**This is the answer to the biggest kill condition on [[gunner-line-blinding]].**
That file's first and largest risk is that *no legal empty tile exists in the
lane* — build requires an orthogonally adjacent **empty** tile and 97.2% of the
tiles the enemy plants on are tiles we build on too. **A thrown body needs only a
`is_tile_passable` tile, not an empty one, and costs 0 Ti instead of 3.** Same
effect, weaker precondition, cheaper.

**And the field's own code has the bug this preys on.** Battlecode 2026's Lorem
Ipsum shipped a throw-targeting system and then wrote:

> *"Note that as of now we do not have any toll at throwing at our own rat kings
> or rats, or any checks for throwing at walls (added later)."*

> *"We prioritize hitting enemy rat kings and enemy cats, else we just throw it at
> an enemy baby rat (or we were supposed to, I later realized we might’ve been
> throwing it at our own as well because I forgot the check)."*

**A top-16 team shipped a targeting routine with no own-team check.** Our own
measurement says the same class of omission is live in this league: own-turret
friendly fire is **0.1% of our home turret deaths (5 cases)** and 0.12-0.14% of
deaths overall — small at baseline precisely because nobody is *inducing* it.

**WHY THERE IS SO LITTLE PRIOR ART, STATED SO THE THIN SOURCING IS NOT MISREAD
AS THIN SEARCHING.** Sweep 11 read all 23 Battlecode postmortems 2019-2026 for
team-agnostic damage and found the mechanic is **rare across the whole series**.
Battlecode 2023 states the opposite rule outright — *"There is no harm in
performing this move, since you can’t damage allied units"* (Don't @ Me) — and
Battlecode 2022's area attacks are enemy-only: *"charge that knocks 22% off all
nearby enemies and a fury that knocks 10% off all nearby buildings"*
(5 Musketeers). Screeps hard-codes its one AoE not to hit its owner
(*"rangedMassAttack will not damage the user's own creeps"*, community wiki
citing engine source). **Battlecode 2021's empower, which splits its conviction
across everything in radius "whether friend or enemy", is the only real
precedent I found in five leagues.**

That cuts both ways and both ways matter: there is **little doctrine to borrow**,
and there is **little reason to expect our opponents' code to guard against it**,
because most of them will have learned turret targeting in games where the
guard was unnecessary.

WHAT WOULD KILL IT — and one of these is likely to, so read them before building:

1. **The conjunction is narrow.** We need their builder **adjacent to our
   launcher** *and* their gunner's lane **within r²=26 of that launcher** *and* a
   passable lane tile nearer to the gunner than its current target. Measured
   grab volume at home is only **~1-3 per game** ([[launcher-defensive-interception]]),
   so this is a handful of opportunities per match, not a doctrine.
2. **A competent opponent gates on `can_fire`.** If their code checks unit
   ownership on the target tile, we get outcome 1 (blanked gunner) and never
   outcome 2 (self-damage). Outcome 1 is still worth having, but the file should
   not be sold on the friendly-fire kill.
3. **Their builder moves.** Unlike a barrier, a thrown body walks off next turn.
   This buys **one to two rounds** of blanking, not a permanent block.
4. **We may be handing them a scale refund if they kill it.** Per
   [[displace-dont-kill]], a dead enemy builder removes its +20% from *their*
   cost scale regardless of who killed it — so the self-kill outcome is not
   unambiguously good for us. **The ammo burn is the reliable payoff; the kill is
   not.**
5. **Untested ownership symmetry.** Our probe showed a *friendly* body blocking a
   *friendly* gunner. The mirror — an enemy body blocking an enemy gunner — is
   near-certain by symmetry but is an assumption, and it is the cheapest thing on
   this page to check.

BUILDER HOOK — **one probe, one local game, before any plank:**
stand an enemy builder bot in an enemy gunner's facing line and read
`can_fire_from(gunner_pos, gunner_dir, GUNNER, target)` from that side.
True → this file is dead. False → the blanking half is real and the rule is
three lines on top of the launcher we would build anyway:

> If a launcher can grab an enemy builder bot, and any passable tile in a visible
> enemy **gunner**'s `get_attackable_tiles_from(...)` lies within throw range,
> prefer that tile over "farthest from our core".

Related: [[gunner-line-blinding]] · [[launcher-defensive-interception]] ·
[[displace-dont-kill]] · [[score-the-throw-destination]] ·
[[ammo-drain-baiting]] · [turret line blocking probe](../turret-line-blocking-2026-08-09.md)
