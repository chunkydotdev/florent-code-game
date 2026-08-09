"""LOKI-4 -- ORE DENIAL.  The whole plank, in one file, in one rule.

    A unit already standing orthogonally beside an unclaimed ENEMY-SIDE ore
    tile spends one turn and 3 Ti on a BARRIER, and the site is gone.

That is the entire mechanism.  It is REACTIVE: no detour, no dedicated trip, no
prediction of where the enemy will build.  Every larger version of this doctrine
was designed in the same session and killed by measurement; doctrine.py's LOKI-4
block records all three refutations (pre-emptive siting, an opponent tile book,
and home-side denial) so they are not rebuilt.  The short form of why only this
survived:

  * Pre-emptive fails on a pincer -- their opening tile is predictable but
    unreachable (first harvesters land r2-13), their late tile is reachable but
    unpredictable (rank 4+ is 82-86% of picks by r150).
  * A per-opponent tile book encodes geometry we already derive: the "modal
    opening tile" is just the nearest ore to that seat's Core, for them and for
    us alike.  It would add a staleness hazard and no signal.
  * On any tile we can economically work, A HARVESTER IS A STRICTLY BETTER
    BARRIER -- same permanence, same denial, plus 2.5 Ti/round.  So barriers are
    only ever correct on ore we cannot work, i.e. ore deep in their half.

Engine-probed, not inferred (bots/_probe_denial, fjordgate): can_build_harvester
on an ore tile goes True -> False the moment our barrier stands, and back to
True only when WE destroy it.  ct.destroy() is allied-only, so clearing 3 Ti and
one turn of ours costs them 15 attacks, 30 Ti and 15 builder-turns.

READ THE KILL CRITERION IN doctrine.py FIRST.  A team consumes a median of 4
distinct ore sites out of the ~9.4 on its side; on the median map denying two
denies nothing.  DENY_MAX_ENEMY_ORE turns this file off on 7 of the 15 pool
maps for exactly that reason.

This file is the ablation unit: with ORE_DENIAL_ON False every entry point
returns on its first line and the bot is _v103split.
"""

from doctrine import (  # noqa: F401
    CARDINALS,
    DENY_DEBUG,
    DENY_MAX_BARRIERS,
    DENY_MAX_ENEMY_ORE,
    DENY_MAX_RND,
    DENY_MIN_OPEN_NBRS,
    DENY_TI_FLOOR,
    ORE_DENIAL_ON,
)


def _dfoot(t, o):
    """Chebyshev distance from tile t to the nearest tile of the 2x2 footprint
    anchored at o.  Same measure dist_core() in main.py uses, restated here so
    this file needs no import back into main and stays deletable as a unit."""
    return min(
        max(abs(t.x - o.x), abs(t.y - o.y)),
        max(abs(t.x - o.x - 1), abs(t.y - o.y)),
        max(abs(t.x - o.x), abs(t.y - o.y - 1)),
        max(abs(t.x - o.x - 1), abs(t.y - o.y - 1)),
    )


def _open_nbrs(bot, t):
    """Non-wall, in-bounds cardinal neighbours of t in the decoded grid."""
    n = 0
    for d in CARDINALS:
        dx, dy = d.delta()
        x, y = t.x + dx, t.y + dy
        if 0 <= x < bot.mw and 0 <= y < bot.mh and (x, y) not in bot.map_walls:
            n += 1
    return n


def plan(bot, ct):
    """The frozen set of ore tiles this bot is willing to barrier.

    A tuple of Positions, computed once per unit and cached -- its inputs (the
    decoded ore grid and both Core positions) never change during a match, so
    every unit that computes it gets the same answer and no store slot is
    needed (all 16 are occupied anyway).  None means "not computed yet", an
    empty tuple means "computed, nothing to deny on this map".

    Siting, in the order the filters apply:

      1. DECODED MAP REQUIRED.  The map gate below is the whole kill criterion,
         and it cannot be evaluated from vision -- a builder sees r^2=20 of a
         676-tile map.  On a map known_map_for cannot decode we do not know how
         many spare sites the enemy has, so we spend nothing.  Every map in the
         current pool decodes.

      2. ENEMY-SIDE ONLY -- strictly nearer their Core footprint than ours.
         Ore is symmetric, so a midline barrier is a mutual denial, and on any
         tile we could work a harvester dominates a barrier outright.

      3. MAP GATE -- if their side carries more than DENY_MAX_ENEMY_ORE tiles,
         return nothing at all.  Denying 2-4 of 10-19 sites against a team that
         consumes a median of 4 is noise; the census says that is 7 of 15 pool
         maps and this is where they are switched off.

      4. CORRIDOR GUARD -- the tile must have DENY_MIN_OPEN_NBRS open cardinal
         neighbours, so a barrier never seals a pinch our own units walk.
    """
    if not ORE_DENIAL_ON:
        return ()
    cached = bot.deny_plan
    if cached is not None:
        return cached
    if not bot.map_ores or bot.core is None or bot.enemy is None:
        return ()

    enemy, own = bot.enemy, bot.core
    enemy_side = [t for t in bot.map_ores if _dfoot(t, enemy) < _dfoot(t, own)]
    if len(enemy_side) > DENY_MAX_ENEMY_ORE:
        bot.deny_plan = ()
        return ()
    # Nearest their Core first: a site they claim early is worth more denied
    # than one they reach at r120.  Only ever a tiebreak between two tiles this
    # unit is simultaneously adjacent to, which is rare.
    enemy_side.sort(key=lambda t: (_dfoot(t, enemy), t.x, t.y))
    bot.deny_plan = tuple(t for t in enemy_side if _open_nbrs(bot, t) >= DENY_MIN_OPEN_NBRS)
    return bot.deny_plan


def try_place(bot, ct):
    """Spend this unit's action on a denial barrier.  True if one was built.

    Fires only on a tile the unit is ALREADY orthogonally adjacent to, so the
    plank costs exactly one builder-turn per barrier and never a step of
    walking.  Called from the saboteur's action phase below the siege work, so
    nothing measured-good is displaced.
    """
    if not ORE_DENIAL_ON or bot.deny_placed >= DENY_MAX_BARRIERS:
        return False
    try:
        if ct.get_action_cooldown() != 0:
            return False
        rnd = ct.get_current_round()
        if rnd > DENY_MAX_RND:
            return False
        if ct.get_global_resources() < DENY_TI_FLOOR:
            return False
        tiles = plan(bot, ct)
        if not tiles:
            return False
        p = ct.get_position()
        for t in tiles:
            if abs(t.x - p.x) + abs(t.y - p.y) != 1:
                continue
            # can_build_barrier is the only occupancy test needed: it is False
            # on a tile that already carries anything, theirs or ours.
            if not ct.can_build_barrier(t):
                continue
            ct.build_barrier(t)
            bot.deny_placed += 1
            if DENY_DEBUG:
                import sys
                print(
                    f"DENY r{rnd} tile=({t.x},{t.y}) cost={ct.get_barrier_cost()} "
                    f"n={bot.deny_placed}",
                    file=sys.stderr,
                )
            return True
    except Exception:
        return False
    return False
