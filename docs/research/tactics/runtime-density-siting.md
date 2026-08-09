---
tactic: Site defence by LIVE enemy density and interposition, not by a fitted map table
source: https://battlecode.org/assets/files/postmortem-2024-cout-for-clout.pdf
origin: Battlecode 2024 / Cout for Clout; the anti-clustering half corroborated independently by Battlecode 2020 / The High Ground
evidence: documented
transfers: partial
---

WHAT IT IS — Cout for Clout scored every candidate placement **at runtime, from
what the unit could see that round**, on three terms.

**Density** — put it where the enemy actually is:

> "in each possible build location, we count the number of enemy robots in
> radius 8. More robots would signify a higher chance that one of them would
> trigger our trap. This also causes traps to be placed in higher density areas,
> affecting more enemy ducks."

**Interposition** — put it on the line the enemy must walk:

> "Another heuristic used to maximize the speed our traps would be triggered is
> to see if the trap-building location is between the enemy and your flag. If
> this is true, it is much more likely that they will walk on your trap."

**Anti-clustering** — an explicit exclusion zone, producing a lattice:

> "choosing not to place traps if there's another one in an +-pattern"

The High Ground reached the same anti-clustering shape independently for their
BC2020 Net Guns: "at least 8 distance squared away from each other. Additionally,
we would only build net guns in the “corners” of the space inside our wall".

WHY IT MIGHT TRANSFER — **because it is the surviving half of an idea we already
refuted.** `gunner-plant-tiles-are-not-enumerable-2026-08-09.md` killed the
*pre-computed* version for us: a per-map/seat table of ≥5-kill tiles carries
**+3.8pp** of held-out information at best and **−3.0pp** at the sizes worth
shipping, because "the apparent repetition is an artefact of a small universe".

That refutation is specifically about **a table learned across games**. Cout for
Clout's heuristic is a different object: *a count taken this round, from this
unit's vision, of where the enemy is standing now.* It never claims tiles repeat.
It survives the refutation intact, and it is the only form of "put defence where
the attacks come" that does.

The interposition term maps cleanly and cheaply: our defensive turret wants to be
**between the enemy builder and our core**, not on a symmetric ring — and both
endpoints are readable (`get_position(id)` of a visible enemy builder, and our
own core's position).

And the anti-clustering term has a reason to matter here that BC2024's did not:
**our gunner's line of sight is blocked by our own buildings** (s23 probe), so two
gunners sharing a lane are partly wasted, while two sentinels sharing a ray are
not (`sentinel-file-stacking`). **A single spacing rule applied to both turret
types is wrong for one of them** — the corollary already recorded in
[[sentinel-file-stacking]], now with an outside precedent for the gunner half.

WHAT WOULD KILL IT — one disanalogy that may be fatal, plus the usual budget:

1. **Transient evidence, permanent commitment.** BC2024's traps were *consumed on
   trigger*; our turrets are permanent and immovable, a gunner rotates only for
   10 Ti, and a sentinel cannot rotate at all (`machinery-audit`). Scoring a
   placement on this round's enemy density commits it for up to 1000 rounds.
   BC2024 could afford to be wrong; we buy the mistake outright. **This is the
   sharpest objection in the file and it is not answered by anything I found.**
2. **10 ms per unit per turn.** Counting enemy robots in a radius for every
   candidate tile is the classic budget-blowing shape. It must be bounded to the
   ≤4 tiles a builder can legally build on anyway.
3. Enemy density seen from one builder's r²=20 vision is a very small sample of
   the band; BC2024's units saw a larger share of a smaller map.

BUILDER HOOK — **take the free half first.** The anti-clustering rule needs no
enemy data, no memory, and no measurement to justify:

> Before building a **gunner**, reject the tile if an existing friendly gunner
> already covers that lane (check with `get_attackable_tiles_from`). Do **not**
> apply the rule to sentinels — they stack on purpose.

Instrument it with realised shots per gunner-round. If our gunners are firing
well below their reload ceiling, lane collision is a live cost and the rest of
the file becomes worth pricing; if they are already near it, the free half is
the whole file.

The density/interposition half should **not** be built before the objection in
kill condition 1 is answered, because it is the half that spends permanent
titanium on transient evidence.

Related: [[sentinel-file-stacking]] · [[turret-threat-field]] ·
[gunner plants are not enumerable](../gunner-plant-tiles-are-not-enumerable-2026-08-09.md)
