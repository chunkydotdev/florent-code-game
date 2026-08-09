"""LOKI-4 -- ORE DENIAL.  The whole plank, in one file.

A 3 Ti BARRIER standing on an ORE tile permanently removes a 24 Ti HARVESTER
site, because harvesters may only be built on ore.  Engine-probed today
(bots/_probe_denial, fjordgate): can_build_harvester goes True -> False when
our barrier lands and back to True only when WE destroy it -- ct.destroy() is
allied-only, so the victim has to chew 30 HP at 2 dmg / 2 Ti a swing (15
attacks, 30 Ti, 15 builder-turns) to undo 3 Ti and one turn of ours.

Every constant and every flag lives in doctrine.py under the LOKI-4 heading,
with the census that justified it.  This file is only the mechanism, and it is
the ablation unit: with ORE_DENIAL_ON False every entry point below returns
immediately and the bot is _v103split.

TWO LAYERS, and the boundary between them is a safety property
==============================================================
LAYER 1 -- GENERIC SITING (required, always on).  The candidate list is derived
from map geometry alone: the decoded ore grid, our Core, and the enemy Core
(which the Core publishes to SLOT_ENEMY_CORE from enemy_core_for, i.e. from the
map's own symmetry).  It works with ZERO opponent knowledge and it is the only
thing that can put a tile into the plan.

LAYER 2 -- OPPONENT TILE BOOK (optional, additive, currently empty).  If a
measured "this opponent opens on this tile on this map" book ever exists, it
enters here as a PREFERENCE ORDERING over the Layer-1 candidates and nothing
else.  The safety property is structural, not a promise: `_apply_book` can only
re-sort a list Layer 1 already approved.  It cannot add a tile, cannot remove
one, and cannot empty the plan.  Therefore an empty book, a stale book, a book
keyed to a map we are not on, or a book naming tiles that generic siting
rejected all degrade to exactly the generic ordering -- never to doing nothing.
That is the lesson from the suspended insertion-tile table: the book is a
tie-break, never the mechanism.

WHAT COULD MAKE THIS WHOLE FILE POINTLESS -- read doctrine.py's census first.
A team consumes a MEDIAN OF 4 distinct ore sites out of the ~9.4 on its side.
Denying two of nine denies nothing.  DENY_MAX_ENEMY_ORE is the gate that turns
the plank off on the 7 of 15 pool maps where that is the situation.
"""

from fcode import EntityType, Position

from doctrine import (  # noqa: F401
    CARDINALS,
    DENY_BOOK_ON,
    DENY_BOOK_STAMP,
    DENY_DEBUG,
    DENY_DETOUR_DSQ,
    DENY_HOME_MAX_BARRIERS,
    DENY_HOME_MIN_RANK,
    DENY_HOME_MIN_RND,
    DENY_HOME_ON,
    DENY_MAX_BARRIERS,
    DENY_MAX_ENEMY_ORE,
    DENY_MAX_RANK,
    DENY_MAX_RND,
    DENY_MIN_OPEN_NBRS,
    DENY_RANK_DEADLINE,
    DENY_TI_FLOOR,
    DENY_TILE_BOOK,
    ORE_DENIAL_ON,
)


# --- geometry ----------------------------------------------------------------

def _dfoot(t, o):
    """Chebyshev distance from tile t to the nearest tile of a 2x2 footprint
    anchored at o.  Same measure dist_core() in main.py uses, restated here so
    this file has no import back into main and stays deletable as a unit."""
    return min(
        max(abs(t.x - o.x), abs(t.y - o.y)),
        max(abs(t.x - o.x - 1), abs(t.y - o.y)),
        max(abs(t.x - o.x), abs(t.y - o.y - 1)),
        max(abs(t.x - o.x - 1), abs(t.y - o.y - 1)),
    )


def _open_nbrs(bot, t):
    """Non-wall, in-bounds cardinal neighbours of t in the decoded grid.

    A barrier BLOCKS MOVEMENT and LOS.  Dropping one into a corridor pinch can
    wall our own saboteur out of the half it is trying to reach, which would
    cost us far more than the site is worth."""
    n = 0
    for d in CARDINALS:
        x, y = t.x + d.delta()[0], t.y + d.delta()[1]
        if 0 <= x < bot.mw and 0 <= y < bot.mh and (x, y) not in bot.map_walls:
            n += 1
    return n


def _map_key(bot):
    """The same key shape CORE_PAIRS / MAP_CODES use: dims plus both Core
    anchors, ordered ours-then-theirs so it is seat-independent when looked up
    with either orientation."""
    return (bot.mw, bot.mh, bot.core.x, bot.core.y, bot.enemy.x, bot.enemy.y)


# --- Layer 2: the opponent tile book -----------------------------------------

def _apply_book(bot, ranked):
    """Re-sort Layer-1 candidates by an optional measured tile book.

    `ranked` is [(Position, rank), ...] already filtered and ordered by generic
    siting.  A book hit moves a tile to the front of the list, preserving the
    generic order within each group.  Nothing is added and nothing is dropped,
    so every failure mode of the book -- off, empty, stale, wrong map, wrong
    tiles -- lands on `preferred` being empty and returns `ranked` unchanged.
    """
    if not DENY_BOOK_ON or not DENY_TILE_BOOK:
        return ranked
    try:
        key = _map_key(bot)
        book = DENY_TILE_BOOK.get(key)
        if not book:
            # Also try the mirrored key: the book may have been measured from
            # the other seat.  Still only a reordering.
            book = DENY_TILE_BOOK.get(
                (bot.mw, bot.mh, bot.enemy.x, bot.enemy.y, bot.core.x, bot.core.y)
            )
        if not book:
            return ranked
        preferred = set(book)
        return tuple(
            sorted(ranked, key=lambda tr: (0 if (tr[0].x, tr[0].y) in preferred else 1, tr[1]))
        )
    except Exception:
        return ranked


# --- Layer 1: generic siting --------------------------------------------------

def forward_plan(bot, ct):
    """The enemy-side ore tiles we are willing to spend a barrier on.

    Returns a tuple of (Position, rank), rank being 1-based position in the
    enemy's own nearest-ore ladder.  Computed once per unit and cached; the
    inputs (decoded ore grid, both Core positions) never change during a match.

    Siting, in the order the filters are applied:
      1. MAP GATE -- if the enemy side carries more than DENY_MAX_ENEMY_ORE ore
         tiles, return nothing at all.  Denying 2-3 of 10-19 sites against a
         team that consumes a median of 4 is noise, and the census says that is
         7 of the 15 pool maps.
      2. ENEMY-SIDE ONLY -- strictly nearer their Core than ours.  Midline ore
         is excluded on purpose: ore is symmetric, so a midline denial is a
         mutual denial, and the pool's contested ore sits on the two maps that
         have the most spare sites anyway.
      3. REACH TEST -- keep rank r only if our own Core is close enough that a
         builder could stand beside the tile before the census median round at
         which rank r is claimed.  This is what drops their doorstep ore on big
         maps, and it is also what KEEPS it on fjordgate and moonrise, where
         the enemy's nearest ore is 3-4 steps from our ring.  A fixed "skip the
         first two ranks" did the opposite and was refuted by the pool dry-run.
         Stop at DENY_MAX_RANK regardless.
      4. CORRIDOR GUARD -- the tile must have DENY_MIN_OPEN_NBRS open cardinal
         neighbours, so a barrier never seals a pinch our own units use.
    """
    if not ORE_DENIAL_ON:
        return ()
    cached = bot.deny_plan
    if cached is not None:
        return cached
    # The decoded grid is the precondition for the map gate, and the map gate
    # is the whole kill criterion.  On a map we cannot decode we do not know
    # how many sites the enemy has, so we do not spend barriers at all.
    if not bot.map_ores or bot.core is None or bot.enemy is None:
        return ()

    enemy = bot.enemy
    own = bot.core
    enemy_side = [t for t in bot.map_ores if _dfoot(t, enemy) < _dfoot(t, own)]
    if len(enemy_side) > DENY_MAX_ENEMY_ORE:
        bot.deny_plan = ()
        return ()

    enemy_side.sort(key=lambda t: (_dfoot(t, enemy), t.x, t.y))
    ranked = []
    for i, t in enumerate(enemy_side):
        rank = i + 1
        if rank > DENY_MAX_RANK:
            break
        if _open_nbrs(bot, t) < DENY_MIN_OPEN_NBRS:
            continue
        # Reach test.  Manhattan from our own footprint is one round per tile
        # for a builder that spawns on the ring at r0-1; if that already
        # overshoots the census median claim round for this rank, the site is
        # gone before we could be standing next to it.
        reach = min(
            abs(t.x - own.x) + abs(t.y - own.y),
            abs(t.x - own.x - 1) + abs(t.y - own.y),
            abs(t.x - own.x) + abs(t.y - own.y - 1),
            abs(t.x - own.x - 1) + abs(t.y - own.y - 1),
        )
        if reach > _deadline(rank):
            continue
        ranked.append((t, rank))
    bot.deny_plan = _apply_book(bot, tuple(ranked))
    return bot.deny_plan


def _deadline(rank):
    """Census median round at which the rank-th nearest ore to a Core is
    claimed by a harvester.  Clamped at both ends of the table."""
    idx = rank if rank < len(DENY_RANK_DEADLINE) else len(DENY_RANK_DEADLINE) - 1
    return DENY_RANK_DEADLINE[idx]


def _live(rank, rnd):
    """Soft per-rank deadline: past the census median claim round for that
    rank the tile is more likely taken than not, and walking to it is wasted
    builder-turns.  can_build_barrier() refuses an occupied tile regardless --
    this only stops the DETOUR."""
    return rnd <= DENY_MAX_RND and rnd <= _deadline(rank)


# --- action phase -------------------------------------------------------------

def try_place(bot, ct):
    """Spend this unit's action on a denial barrier.  True if we built one.

    Only fires on a tile the unit is ALREADY orthogonally adjacent to, so the
    action costs exactly one builder-turn and no walking.  Called from the
    saboteur's action phase below the siege work, so nothing measured-good is
    ever displaced.
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
        plan = forward_plan(bot, ct)
        if not plan:
            return False
        p = ct.get_position()
        for t, rank in plan:
            if abs(t.x - p.x) + abs(t.y - p.y) != 1:
                continue
            if not ct.can_build_barrier(t):
                continue
            ct.build_barrier(t)
            bot.deny_placed += 1
            if DENY_DEBUG:
                import sys
                print(
                    f"DENY r{rnd} tile=({t.x},{t.y}) rank={rank} "
                    f"cost={ct.get_barrier_cost()} n={bot.deny_placed}",
                    file=sys.stderr,
                )
            return True
    except Exception:
        return False
    return False


# --- move phase ---------------------------------------------------------------

def steer(bot, ct):
    """A tile to walk to so the next action can plant a barrier, or None.

    Bounded detour only: the ore must already be within DENY_DETOUR_DSQ (two
    steps) of where this unit stands, and its rank deadline must not have
    passed.  Combined with DENY_MAX_BARRIERS this caps the whole plank at
    ~12 builder-turns per unit for a match, taken from the one unit whose
    measured contribution to core kills is ~zero.
    """
    if not ORE_DENIAL_ON or bot.deny_placed >= DENY_MAX_BARRIERS:
        return None
    try:
        rnd = ct.get_current_round()
        if rnd > DENY_MAX_RND:
            return None
        if ct.get_global_resources() < DENY_TI_FLOOR:
            return None
        plan = forward_plan(bot, ct)
        if not plan:
            return None
        p = ct.get_position()
        best = None
        best_key = None
        for t, rank in plan:
            if not _live(rank, rnd):
                continue
            d = p.distance_squared(t)
            if d > DENY_DETOUR_DSQ:
                continue
            if abs(t.x - p.x) + abs(t.y - p.y) == 1:
                # Already in place; the action phase owns it, do not steer.
                return None
            if ct.is_in_vision(t) and ct.get_tile_building_id(t) is not None:
                continue
            # Stand on the cardinal neighbour nearest the enemy Core, so the
            # detour is taken along the direction this unit was going anyway.
            stand = None
            stand_key = None
            for dd in CARDINALS:
                s = Position(t.x + dd.delta()[0], t.y + dd.delta()[1])
                if not (0 <= s.x < bot.mw and 0 <= s.y < bot.mh):
                    continue
                if (s.x, s.y) in bot.map_walls:
                    continue
                k = (_dfoot(s, bot.enemy), s.x, s.y)
                if stand_key is None or k < stand_key:
                    stand, stand_key = s, k
            if stand is None:
                continue
            k = (d, rank)
            if best_key is None or k < best_key:
                best, best_key = stand, k
        return best
    except Exception:
        return None


# --- LANE B: home-side denial (OFF by default; see DENY_HOME_ON) --------------

def home_plan(bot, ct):
    """Ore on OUR side that we will never work, ranked from our own Core.

    448 of 3,073 harvesters in the replay census (14.6%) were built on the
    opponent's side of the midline at median round r189, so the field does come
    and take our tail ore, but late.  Barriering it from inside our own half is
    far cheaper in builder-turns than the forward trip and it stays reversible
    for us alone -- ct.destroy() is free, has no cooldown and restores the site.

    OFF by default.  The concrete backfire: _pick() only skips an ore tile it
    can SEE is occupied, so our own barriers on out-of-vision ore stay live
    expansion targets and send our own expanders on wasted walks.  That spends
    builder-turns from the economy arm, which is the asset this build exists to
    protect.  Wired and left off so it can be measured as its own arm.
    """
    if not (ORE_DENIAL_ON and DENY_HOME_ON):
        return ()
    cached = bot.deny_home_plan
    if cached is not None:
        return cached
    if not bot.map_ores or bot.core is None or bot.enemy is None:
        return ()
    own = bot.core
    ours = [t for t in bot.map_ores if _dfoot(t, own) < _dfoot(t, bot.enemy)]
    ours.sort(key=lambda t: (_dfoot(t, own), t.x, t.y))
    out = []
    for i, t in enumerate(ours):
        if i + 1 < DENY_HOME_MIN_RANK:
            continue
        if _open_nbrs(bot, t) < DENY_MIN_OPEN_NBRS:
            continue
        out.append((t, i + 1))
    bot.deny_home_plan = tuple(out)
    return bot.deny_home_plan


def try_place_home(bot, ct):
    """Same one-turn, already-adjacent rule as try_place, on the home plan."""
    if not (ORE_DENIAL_ON and DENY_HOME_ON):
        return False
    if bot.deny_home_placed >= DENY_HOME_MAX_BARRIERS:
        return False
    try:
        if ct.get_action_cooldown() != 0:
            return False
        rnd = ct.get_current_round()
        if rnd < DENY_HOME_MIN_RND:
            return False
        if ct.get_global_resources() < DENY_TI_FLOOR:
            return False
        plan = home_plan(bot, ct)
        if not plan:
            return False
        p = ct.get_position()
        for t, rank in plan:
            if abs(t.x - p.x) + abs(t.y - p.y) != 1:
                continue
            if not ct.can_build_barrier(t):
                continue
            ct.build_barrier(t)
            bot.deny_home_placed += 1
            if DENY_DEBUG:
                import sys
                print(f"DENYHOME r{rnd} tile=({t.x},{t.y}) rank={rank}", file=sys.stderr)
            return True
    except Exception:
        return False
    return False
