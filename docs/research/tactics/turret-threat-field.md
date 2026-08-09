---
tactic: Incremental turret threat field — treat covered tiles as obstacles, not as risk
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf
origin: Battlecode 2020 / Java Best Waifu (WINNER)
evidence: documented
transfers: yes
---

WHAT IT IS — the 2020 winner's answer to enemy immobile turrets was a **map, not
a fight**. Every unit maintained a coverage grid updated by ±1 rather than
recomputed:

> "every time a Net Gun is reported they would add +1 to all cells at distance
> 15 or less, and every time a Net Gun is destroyed they would add −1 to all
> cells at distance 15 or less to its original position."

and the routing rule on top of it is **binary, not a soft cost**:

> "A Drone considers all locations with value > 0 as obstacles"

with the payoff stated immediately after: "This feature allowed Drones to circle
around the enemy HQ (and nearby Net Guns), enclosing all enemy units inside and
blocking Miners and Landscapers from getting out."

They also record the limitation, in a footnote, and it is the interesting part:

> "Drones have blind spots, they can move into a HQ or a Net Gun's shooting
> range without seeing them beforehand"

**The same rule appears in StarCraft bot writing as a micro-level prohibition**,
and it is worth having because it names the economic half that JBW's routing
version leaves out — Jay Scott:

> "Don't try to mine a mineral patch that is in cannon range; do mine any patches
> that are out of range. Don't try to build a building, or land a floating
> building, in cannon range."

*(http://satirist.org/ai/starcraft/blog/archives/748-cannon-rush-reactions.html)*
**Two independent fields, one rule: covered ground is not risky ground, it is
ground you do not use.** The economic half is developed in [[yield-and-reroute]].

**And it is still being built in 2026.** A Terminal competition entry describes
the identical structure, on a 28×28 board, as its offensive spawn selector:

> "Offense is powered by a **Danger Map** — a full 28×28 matrix of enemy turret
> attack radii computed each turn — used to pick the safest of 12 spawn
> candidates. A **recency penalty** (1.3×) on the previously used spawn prevents
> repetitive pathing and forces lane rotation."

*(github.com/srj-42/India-Terminal-2026 — competitor writeup, one fetch, README
prose.)* Note the second half: **they add a recency penalty so the safest choice
does not become a predictable one.** A pure argmin over a threat field is a
constant, and this library has already recorded that our own openings are
near-constants an opponent can read ([sweep 6](2026-08-09-sweep-6.md)). If we
ship a threat-field router, it should carry the same anti-repetition term from
the start.

**Three leagues — Battlecode 2020, StarCraft bot writing 2019, Terminal 2026 —
independently maintaining the same object.** That is about as strong a transfer
signal as this library gets.

WHY IT MIGHT TRANSFER — **our version is strictly better than theirs on exactly
the axis that hurt them.** JBW needed the remembered map because their scout
radius was smaller than the threat radius. Ours is the other way round:

| | radius² |
|---|---:|
| builder bot vision | **20** |
| gunner vision **and** attack | **13** |
| sentinel vision and attack | 32 |

A builder sees a planted gunner at d²≤20 while the gunner's kill zone ends at
d²≤13 — **there is a standoff band we can observe before entering it.** And the
threat we face is overwhelmingly the one inside that band: **83.8% of our home
turret deaths are enemy gunners**, and only **7.7%** come from a sentinel firing
beyond gunner reach. The three opponents that hurt us most at home (Ouroboros,
Lunds Stallions, Powerpuff Girls) do it with gunners at 0.0% / 24.3% / 3.9%
sentinel share.

Two further reasons the *shape* of JBW's idea matters here and not just its
content:

- **Our budget is 10 ms of CPU per unit per turn.** A full rescan of the home
  band by every builder every round is precisely the expensive shape; the
  ±1 incremental form is the cheap one.
- **Per-unit state persists.** Confirmed in our own bot (`bots/_v100hf/main.py`
  comments: "The Core is a single unit with a persistent Player instance",
  "per unit instance"). So each builder can carry its own grid across rounds
  without spending any of the 16 store slots.

And our kill zone is **cheaper to represent than JBW's disc**. A gunner is a
facing turret with a straight-line shot; we can read a specific enemy turret's
`get_position(id)` and `get_direction(id)` and hand both to
`get_attackable_tiles_from(position, direction, turret_type)` to get its exact
pattern. The s23 probe found that this getter **ignores occupancy** — which for
*avoidance* errs in the safe direction (it over-marks), even though it made the
same getter useless for siting.

WHAT WOULD KILL IT — four things, and the second is the one to check first:

1. **Avoidance is not removal.** Routing around a planted gunner leaves it
   grinding, and it is the 41.4% survive-to-end tail we actually lose to. This
   buys builder lives, not the tile.
2. **The kill zone is our own economy.** 97.2% of tiles the enemy plants on are
   tiles we also build on. Marking d²≤13 around every planted gunner as impassable
   may disconnect our own conveyor network from the core, and a builder may
   co-occupy only a conveyor, splitter, or the allied core — so there is little
   slack to route through. **A disc rule is likely fatal here; the facing-line
   rule may not be.**
3. Sentinels outrange our vision (32 > 20), so the map has a genuine blind spot
   of exactly JBW's kind — it is just a small one for us (7.7%).
4. If the ±1 bookkeeping is wrong on turret death the grid poisons permanently;
   JBW needed a matching decrement and an explicit special case ("Visible Net
   Guns are treated differently").

BUILDER HOOK — **the smallest test carries no map at all.** One movement guard:
before moving, if the destination tile lies in
`get_attackable_tiles_from(pos, dir, GUNNER)` of any enemy gunner currently in
vision, prefer any other legal cardinal step. No memory, no store slot, no grid.
Measure US home builder deaths per 1,000 home builder-rounds against the
attribution baseline (4,285 home deaths; per-opponent rates 5.943 / 4.794 /
3.286 for the three worst).

Only if that moves does the remembered ±1 grid become worth its CPU — the grid's
whole value is covering turrets we can no longer see, and we can see the gunners.

Related: [[gunner-line-blinding]] · [[sustained-plant-removal-race]] ·
[builder death attribution](../builder-death-attribution-2026-08-09.md)
