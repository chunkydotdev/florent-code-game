---
tactic: Defensive interception — the launcher as goalkeeper, not spear
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
origin: Battlecode 2020 / The High Ground (4th place); field-wide "drone harass" by week 3
evidence: documented
transfers: yes
---

WHAT IT IS — Battlecode 2020's Delivery Drone is the closest published analogue to
our Launcher that exists: adjacent pickup, **either team**, place on a legal tile,
held unit frozen. The High Ground won a knife-edge series against the top rush team
because *"we happened to pick up and drown their rushing miner right as it was
reaching our base"*, and they name the cost of not doing it: *"Unlike many other
teams, we didn't keep a drone back to defend rushes, which made us weaker vs rush
teams."* By week 3, *"every top team, no matter what their strategy, now had a
drone harass."*

WHY IT MIGHT TRANSFER — **Our ruleset makes this stronger than theirs.** An enemy
builder inside our base can be answered in exactly two ways:

| answer | cost |
|---|---|
| turret fire | 40 HP builder = 3 sentinel shots (30 ammo) or 6 gunner shots (24 ammo) → **24-30 Ti of converted titanium** |
| **launcher throw** | **0 ammo, 0 titanium, facing-independent** |

and our own builder bots **cannot help at all** — a builder's attack hits buildings
only, never enemy builder bots. Crucially the **adjacency comes free**: an enemy
builder attacking one of our buildings *must* be orthogonally adjacent to it, which
is exactly the geometry a launcher needs. We do not have to chase anything.

It also compounds with the cost-scale rule (see [[displace-dont-kill]]): killing
that builder would *refund* their +20% scale and free one of their 50 unit slots.
Throwing it refunds nothing.

**And it points at the band the builder's 09:05 note measures as our single large
advantage — home defence, +11.4 / +16.6 / +22.3pp over the field.** This is the
rare tactic that reinforces a measured strength rather than opening a sixth
doctrine road.

WHAT WOULD KILL IT — If `launch` carries a long action cooldown, one launcher
cannot keep pace with several raiders. If raiders preferentially hit perimeter
buildings far from the launcher, it never gets a grab. Both are measurable before
any build.

> ## ✅ THE TARGETS EXIST — MEASURED, 2026-08-09 (s23), 1,250 ladder games
>
> Sweep 3 asked for exactly this instrument before anything was built: *"count how
> often an enemy builder ends a round orthogonally adjacent to one of our buildings
> inside our half. Large ⇒ a defensive launcher ring has targets. Near zero ⇒ dead
> on arrival."* Per-round positions are not in the corpus, so the proxy is **where
> enemy builder bots die** — which **undercounts** intrusion, since a raider we
> never kill never appears.
>
> **Enemy builder deaths by distance to OUR core, against our builder deaths by
> distance to THEIRS:**
>
> | band | ENEMY, near our core | US, near their core |
> |---|---|---|
> | d²≤2 (adjacent) | **7.5%** | 1.9% |
> | d² 3-8 | **19.9%** | 5.7% |
> | d² 9-32 | 41.4% | 32.9% |
> | d² >32 | 31.2% | 59.5% |
>
> **At close range the asymmetry is 27.4% vs 7.6% — they reach our door, we reach
> only their neighbourhood.** Note where the asymmetry *isn't*: at d² 9-32 the two
> sides are comparable (41.4% vs 32.9%). **We get to the street and die in the last
> three tiles**, which is the same shape as the 2.34% core-touch figure.
>
> **Volume and timing, both favourable:**
> - **3.15 enemy builder deaths per game within d²≤32 of our core**; **1.26 within
>   d²≤8**.
> - **49.4% of games** have at least one at d²≤32; **29.0%** at d²≤8.
> - Rounds: p25 **160**, median **317**, p75 **526** — and **77.1% land at r150+,
>   the exact window where our core-death hazard runs 72-76%.**
>
> **So: a launcher sited at home has ~1-3 grabs per game available, concentrated in
> the window we actually lose.** That is not a huge volume, and it should not be
> sold as one — but it is emphatically not zero, and every grab is 0 ammo and 0
> titanium against the 24-30 Ti a turret kill costs.
>
> **Caveat that cuts the other way, stated plainly:** these are bots we *already
> killed*. The launcher's case is not "we finally get to answer them" but
> "**displacement is cheaper than the answer we already use**" — which rests on the
> cost-scale argument in [[displace-dont-kill]], not on this measurement.

BUILDER HOOK — **The smallest test in either sweep.** One launcher orthogonally
adjacent to the core footprint, one rule: *if any enemy builder bot is adjacent,
throw it to the farthest passable tile from our core.* Measure enemy damage dealt
to our core per game against current. No other change.

Prerequisite reads, both cheap and both gating every launcher tactic:
1. Is `can_launch` adjacency 4-way or 8-way?
2. Must the throw target be *reachable*, or merely `is_tile_passable`?
3. Does being thrown alter the thrown bot's action/move cooldown?

Related: [[displace-dont-kill]] · [[throw-into-prebuilt-cell]] ·
[sweep 3](2026-08-09-sweep-3.md)
