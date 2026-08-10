# PREREG — LOKI-11 "AIMED PLANT": search the sentinel's facing instead of guessing it

**Committed BEFORE submission, activation, or leg creation.** Line `loki`.
Comparator **LOKI-8 = v102 = `bots/_v124loki8`**, the previous line iteration and
the currently live bot — measured on the **pinned testbed control fired one
window earlier**, same 5 maps, same panel.

## The defect, read off our own code

`bots/_v127loki10/raid.py` `_try_forward_sentinel`:

    facing = bp.direction_to(target)

**One guess.** `direction_to` returns the nearest 45-degree compass direction,
which is frequently DIAGONAL. If that single facing fails `can_fire_from`, the
target is abandoned. The s26 engine probe established the engine permits **at
most one of the eight facings** to hit a given tile — so a one-guess rule
discards legal plants on ground a raider has already been paid to walk to.

## What the treatment is

Try **all eight facings, cardinals first**, take the one the engine says can
fire. **A pure widening: it can find MORE legal plants than the guess, never
fewer.** No new mechanism, no new spend, no re-siting, nothing moved.

## Why this and not the plank I built first — the correction is the evidence

A league corpus cut put our median sentinel plant at `d²=32` (a sentinel's exact
maximum range) against fast killers at 8-25, and the obvious reading was *plant
closer*. **I built that, then a direct replay autopsy of the 0-5 loss refuted
it:**

**13 of 13 Bisons sentinels sit CARDINALLY ALIGNED with a core footprint tile at
Chebyshev 5, 4 or 2 — modally 5.** Chebyshev 5 is `d²=25`: **maximum standoff
that still fires** (25 ≤ 32 < 36), and out of a defending builder's orthogonal
reach. Our own sentinels in those games sat at **Chebyshev 1-3, half
diagonal-facing, one per game.**

**So "plant closer" would have forbidden the Bisons' own plant, and we were
already planting closer than they do. Distance was never the variable.**
Alignment is — their line shot ignores obstacles, so a cardinally aligned
sentinel fires through everything and only its own death stops it.

*(The `d²=32` figure is additionally under a basis check by the side lane —
centre-of-core vs nearest-occupied-tile is ambiguous and decisive at these
magnitudes. **This plank does not depend on it**, which is why it is being fired
while that is unresolved.)*

## Why it can matter at all — the damage arithmetic, replay-reconciled

3 sentinels × 18 dmg / 2-round reload = **27 dmg/round → 500 HP of core in ~19
rounds of fire**, ~280 Ti of ammo, inside the 500 Ti we start with. In the
autopsied match **100% of core damage on BOTH sides was sentinel fire** — zero
builder attacks, zero gunner damage — and the Bisons put **65-68% of all their
titanium into sentinels and ammo against our ~21%**. The kill is not
economy-limited; it is limited by how fast a correctly-aimed sentinel starts
shooting.

## Bars, stated before the leg

**MECHANISM (did it fire — NOT the verdict):** forward sentinels built per game,
and the share whose facing is CARDINAL. Control (v102) autopsy showed ~1
sentinel/game and "half diagonal-facing". **LOKI-11 must build strictly more
forward sentinels per game than the control, or the widening did not bind and
the leg answered nothing** (the D7 shape — a guard with no opportunity to fire
is not evidence).

**VERDICT (PRIMARY_CURRENCY): `core_kill_share`** on the pinned testbed vs the
pinned control's **/25**, paired by map and opponent. **SECONDARY, reported and
never substituted:** time-to-core-kill against `KILL_WINDOW_RND: 250`, and
**their** kill time against us.

## Falsifier — three branches, written so a null cannot be argued away

1. **More cardinal plants, `core_kill_share` flat → LABELLED NULL.** I will
   write the word. Widening the facing search would then be established as
   insufficient on its own.
2. **No increase in sentinels built → THE LEG ANSWERED NOTHING**, not evidence
   against the idea. Cause would be that raiders never reach a site where a
   second facing was legal, which is a PATHING problem and a different plank.
3. **`core_kill_share` improves while sentinel count is unchanged → OFF-PREDICTION.**
   Labelled, not banked: something else moved and I do not know what.

**And the one that would actually hurt:** if **their** kill time against us gets
FASTER, the widening bought plants at the cost of raider survival — raiders
spending 30 Ti deeper in enemy ground and dying for it. Reported either way.

## Cost, priced before it is paid

`fcode match unrated` plays the **ACTIVE** submission, so this leg requires
activating LOKI-11 and paying rated ladder exposure for the window — **~6 rated
matches/hour, so ~2-3 matches**. v102 is re-activated immediately after.
**Rollback target: v102, submission `ff270a6c`, currently 1593 @ k=57, net_act
+25.6, `slot_free` False.** The slot rule is untouched by this leg and
`ship_watch` stays armed on the v102 baseline throughout.

## What this leg does NOT test

Economy suppression (we lay 19-28 conveyors while they lay ~0), ring-body
denial, launcher kidnap, or plant DISTANCE. One plank, one leg.

---

# ⛔ SUPERSEDED BEFORE ANY LEG FIRED — THIS PLANK IS NOW **LOKI-12**, NOT LOKI-11

**No leg was ever created against this file.** The bot it describes has been
moved to `bots/_v129loki12` and is parked, unfired. What follows is why, because
the reason is worth more than the plank was.

**THE MECHANISM CHECK CAME BACK NEGATIVE, AND I RAN IT BEFORE SPENDING RATED
EXPOSURE.** Paired local runs, `_probe_victim`, saga, seed 7, LOKI-11 vs the
live LOKI-8:

    LOKI-8  : 1 sentinel, at (21,20), d^2=13, born r73
    LOKI-11 : 1 sentinel, at (21,20), d^2=13, born r93

**Same count, same tile, and the treatment planted it TWENTY ROUNDS LATER.** The
facing search cannot bind when only one plant is ever attempted — falsifier
branch 2 as written ("the leg answered nothing"), established for ~90 seconds of
local compute instead of a rated-exposure window. **The falsifier earned its
keep before the leg, which is the only time it is cheap.**

**AND THE NEGATIVE RESULT LOCATED THE REAL DEFECT, which the facing plank would
have masked.** We do not plant one sentinel because we aim badly. **We plant one
sentinel because `LOKI2_RUSH_ON = False`** — with the committed-opening window
off, the 2-harvester prerequisite and the 40 Ti bank floor apply from round 0.
That is the whole timing gap: **Bisons plant r29-r47; we plant r73-r93.**
