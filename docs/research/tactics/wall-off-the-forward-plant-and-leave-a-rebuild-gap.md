---
tactic: Enclose the forward shooter so enemy workers physically cannot reach it — and leave exactly one gap
source: https://liquipedia.net/starcraft2/Photon_Cannon_Rush
origin: RTS theory / StarCraft II cannon-rush doctrine (retrieved via Wayback snapshot 20250814034647)
evidence: documented
transfers: yes
---
WHAT IT IS — The canonical cannon rush is not "build a turret near their base". It
is "build a turret near their base **that their workers cannot touch**". The
adaptation is described explicitly, and the second sentence states the purpose:

> *"A typical adaptation of the Cannon Rush is to use Pylons to completely wall off
> Cannons behind the mineral line."* … *"The idea is to make it impossible for the
> defending player to attack the Cannons with workers or melee units, while being
> able to completely deny mining in the main."*
Referent: "The idea" = the pylon-walloff adaptation named in the sentence
immediately before it.

Two operational details travel with it. The screen is built to be **repairable
under fire**:
> *"At least one open hex should be left behind each Pylon so they can be quickly
> rebuilt if they are destroyed by melee units"*
and losses are **cut, not fought**:
> *"No Cannons should be allowed to be destroyed while constructing, any that are
> near death should be cancelled to recoup 75% of the mineral cost of
> construction."*

The reason the enclosure matters is the defender's counter-arithmetic, also stated
on the same page:
> *"It takes one Zealot or three Probes to destroy a Cannon that is being built, if
> the Cannon is attacked immediately after it is warped in."*
An unenclosed forward structure dies to three workers. An enclosed one does not.

WHY IT MIGHT TRANSFER — **This is a near-perfect fit for our ruleset, and it is
sentinel-specific in a way that is not obvious.**

- An enemy builder's attack requires an **orthogonally adjacent** tile and
  **cannot target builder bots** — buildings only. So a barrier occupying an
  orthogonal neighbour of our sentinel is a literal, rule-level block on reaching
  it: they must destroy the 30 HP barrier first, at 2 damage per 2 Ti = **30 Ti
  of attacks to remove a 3 Ti building**, and barriers scale at only **+1%**.
- **A sentinel's line ignores obstacles.** Our own barrier ring therefore does
  **not** blind it — probed and confirmed in the library: 18 damage landed through
  a friendly bot *and* a friendly barrier. The identical construction around a
  **gunner is self-defeating**, because a gunner's line is blocked by our own bots
  and buildings (`the-blockade-blanks-your-own-guns.md`).
- This is the same asset the library already priced: *"the ablative barrier screen
  is ~8x HP/Ti and is SENTINEL-ONLY"*. What this source adds is the **topology** —
  enclose the shooter, not the approach — and the **gap discipline** below.

THE GAP IS NOT OPTIONAL, AND IT IS OURS FOR A DIFFERENT REASON THAN THEIRS.
Liquipedia's open hex exists so *pylons* can be rebuilt. Ours must exist because
**heal also requires orthogonal adjacency**: a sentinel ringed on all four sides
is a sentinel our own builder cannot heal. So the correct shape is a **three-sided
ring with the fourth side facing our approach**, held by our own builder bot —
which is itself untargetable by their builders. That is the
`worker-fortified-turret-cell` shape (the field's measured 5.04 lift) built
forward instead of at home, and the enclosure is what makes it survivable there.

WHAT WOULD KILL IT — (a) **The launcher.** It is facing-independent, uses no ammo,
and picks up an adjacent builder bot from either team — so it removes the *healer*
holding the open side without ever touching the barriers, and dodging does not
help. This is the same counter that dominates
`one-cheap-interceptor-decides-the-matchup`, and it is the single thing most
likely to kill this plank.
(b) **Their sentinels also ignore obstacles**, so the ring does nothing against
enemy sentinel fire — it stops builders and gunners, not the 18-damage line.
(c) **Build legality is strictly stronger than `is_tile_empty`**, so a planned
ring may be unbuildable on the tiles that matter; check with the `can_build_*`
predicate per tile rather than assuming.
(d) Each ring segment costs a builder turn, and building is cooldown-gated while
the enemy's response is not — a half-built ring is an unenclosed sentinel.

BUILDER HOOK — Smallest testable unit, and it does not require committing to a
whole strike doctrine: when a forward **sentinel** is planted, immediately
enqueue barriers on its free orthogonal neighbours *except* the one our escort
occupies, ordered by `bearing_count` (see `no-lose-engagement-geometry.md`) so the
most-exposed side is walled first. Measure **sentinel survival rounds** and
**total damage dealt before death** against an unenclosed control. The library
already says our forward assets die fast; this is a cheap, mechanically-grounded
candidate fix with a documented origin.
