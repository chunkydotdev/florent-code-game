"""prune.py -- LOKI-2: the DESTROY / COST-SCALE PRUNING doctrine.

ABLATION UNIT.  Everything this doctrine adds lives in this file.  Its entire
footprint in main.py is four marked edits (grep ``LOKI-2``):

  1. ``from prune import *`` next to the doctrine import
  2. ``prune_state_init(self)`` at the end of ``Player.__init__``
  3. ``prune_sweep(self, ct)`` in ``_builder``, right after ``_wire_tick``
  4. two one-line ``prune_condemned()`` gates -- one in ``_build_next_link``,
     one in ``_move``'s trail pave -- that stop this unit rebuilding a tile it
     just tore down (the R7 self-chase)

Setting ``PRUNE_ON = False`` restores _v103split behaviour exactly: the sweep
returns on its first line and both condemned gates read an empty dict.  (The
flags are here rather than in doctrine.py, against that file's usual rule,
precisely so the ablation is one file and one flag -- noted in doctrine.py.)


WHY THIS EXISTS
---------------
``ct.destroy(pos)`` is the only completely free action in the game: allied
building, orthogonally adjacent, **no titanium, no action cooldown, unlimited
per turn** (docs/game-model.md:242-245; engine-probed, docs/open-questions.md
:81-88 -- it consumes neither the action nor the move).  Grepped 2026-08-09:
``ct.destroy(`` has **zero call sites** in _v103split (the eight ``destroy``
hits in that tree are all prose in comments).

The cost scale is ONE team-wide multiplier -- there is a single
``get_scale_percent()`` and every ``get_*_cost()`` multiplies by it
(bots/cad_probe/main.py:749-751) -- and it tracks **live** entities, not
cumulative builds: it "decreases again when an entity is destroyed"
(docs/game-model.md:357-358, docs/reference/official-docs.md:1424).  So
``destroy()`` is the only downward hand we have on the price of everything we
build afterwards, and every point shaved stays shaved.

Measured target set: **18 of 40 surviving relays on heart connect to nothing**
(docs/v79-analysis.md:187).  At a live scale of ~4.05 that sweep is 4.05 ->
3.87, a 4.4% discount worth ~165 Ti over a back-half build sequence
(thread10_destroy_doctrine.md:258-294).  Stated honestly: this is a
SECOND-ORDER lever.  Live builder bots (+20% each) dominate the multiplier;
18 conveyor points off a 405% scale is single-digit percent, not a doubling.


TWO STALE CLAIMS THIS FILE DOES NOT BUILD ON
--------------------------------------------
* ``destroy()`` does NOT refund in-transit stacks -- it **incinerates** them.
  Measured 0 Ti returned in 191/191 clean cases against a positive control
  that credited 40,427/40,427 (docs/game-model.md:246-255).  Hence
  ``PRUNE_LOADED_ON = False``: a loaded conveyor is skipped by default.
* Forcing the ENEMY to rebuild imposes no permanent scale tax, for the same
  live-census reason.  There is no offensive arm here.  This doctrine prunes
  OUR OWN dead weight only.


THE RULE, IN ONE PARAGRAPH
--------------------------
DEAD HEAD: a friendly CONVEYOR at tile T facing f is provably non-delivering
if ``T.add(f)`` is readable and holds neither a friendly conveyor/splitter nor
our Core footprint.  A conveyor outputs to exactly one tile, so this is a
**sufficient** condition -- no false positives on a tile we can actually see.
It is deliberately not complete (it misses chains pointing into other dead
chains, and cycles), which is the right asymmetry for an irreversible action.
The test is purely LOCAL -- the four cardinal neighbours of the builder that
is already standing there -- so there is no wiredness flood, no BFS, and no
map-wide scan anywhere in this file.
"""

from fcode import Direction, EntityType, Position

from doctrine import CARDINALS, dist_core


# ---------------------------------------------------------------------------
# FLAGS
# ---------------------------------------------------------------------------

# Master ablation switch.  False == _v103split.
PRUNE_ON = True

# Nothing is pruned before this round.  Same class as MEDIC_MIN_RND = 150 and
# HUNT_MIN_RND = 120.  Before ~r150 every dead head is a lane under
# construction: lanes are built harvester-first, core-last (_link_path walks
# parent pointers FROM the harvester, _build_next_link builds link_queue[0]),
# so a growing chain has a dead head for its entire build.  The scale lever is
# also worth least early, when the multiplier is still near 1.0.
PRUNE_MIN_RND = 150

# Below this scale percent the discount is not worth any rebuild risk.
# get_scale_percent() returns a PERCENTAGE (100.0 at match start, not 1.0 --
# docs/game-model.md:404).  Effectively a no-op by r150 on any live map; it is
# here so the doctrine cannot fire in a game where we built almost nothing.
PRUNE_MIN_SCALE = 150.0

# Rounds a tile must be CONTINUOUSLY observed dead-headed before it may be
# destroyed.  The thread-10 spec proposed 25 as "longer than any realistic
# lane build time"; 40 is used here because a lane build is not the only way a
# head sits dead -- a builder that gets pulled into a heal or a chase leaves
# its half-built chain stalled, and that stall is bounded by nothing.  Waiting
# is nearly free (we have r150..r1000 to prune in); a wrong destroy is not.
PRUNE_CONFIRM_RNDS = 40

# The confirm clock resets if the tile went unobserved for longer than this.
# Without it, walking away for 300 rounds and coming back makes a tile
# instantly destroyable off one stale sighting.
PRUNE_GAP_RNDS = 8

# A conveyor whose output tile holds an ENEMY conveyor/splitter/Core is a
# different animal: it is not ambiguous (an enemy building is never going to
# become our next lane segment) and it is actively PAYING THEM -- a heart
# replay has one of our chains delivering a stack into the opponent's Core,
# scoring their tiebreak #1 (docs/spitball.md T11).  Every round of confirm
# there is pure loss, so it gets its own short clock.
PRUNE_ENEMY_CONFIRM_RNDS = 4

# Per-unit lifetime cap on destroys, and per-round cap.  These bound the blast
# radius of any misjudgement to a number we can price: worst case 20 conveyors
# at ~7 Ti of rebuild = 140 Ti per unit, against the 165 Ti the sweep is
# expected to save.  The per-round cap also bounds the engine calls.
PRUNE_MAX_TOTAL = 20
PRUNE_MAX_PER_RND = 2

# Whether a LOADED conveyor may be pruned.  OFF: the stack is incinerated, not
# refunded (see the header).  A dead head that is fed holds its stack forever
# and that stack scores in no tiebreak, so destroying it is titanium-neutral
# rather than a loss -- but "neutral" rests on the stack being provably
# unreachable, and this v1 does not want to bet on that.  Flip to measure.
PRUNE_LOADED_ON = False

# Skip a conveyor orthogonally adjacent to one of our harvesters.  That tile
# is the designated root of a lane, it is where _wire_on_build / _wire_tick
# aim, and it is the tile most likely to be mid-wiring.  It is also the least
# likely to be a pave orphan (the volume target lives out on the walking
# trails, not against the ore).  Costs at most 4 extra tile reads, and only
# for a candidate that has already survived the whole confirm.
PRUNE_SPARE_HARVESTER_ADJ = True

# Rounds a tile we tore down stays condemned FOR THIS UNIT -- it may not be
# repaved or re-linked by the same builder inside the window.  This is the
# local stand-in for the team-wide "condemned slot" in the thread-10 spec; all
# 16 store slots are occupied in doctrine.py, so the anti-thrash guarantee is
# bought per-unit instead.  Combined with the one-shot rule below it gives a
# hard bound: this unit destroys any given tile AT MOST ONCE per match, so a
# destroy/rebuild oscillation (R2, the doctrine's most dangerous failure mode)
# cannot run more than once per unit per tile.
PRUNE_CONDEMN_RNDS = 250

# Per-unit stderr instrumentation.  print() goes to the replay; stderr is
# console-only (docs/tooling.md), so this is safe to leave compiled in and
# costs one branch when off.
PRUNE_DEBUG = False


# ---------------------------------------------------------------------------
# STATE
# ---------------------------------------------------------------------------

def prune_state_init(player):
    """Per-unit state.  No store slot is spent: all 16 are occupied, and every
    field here is read and written only by the unit that owns it."""
    # (x, y) -> [round first seen dead, round last seen dead]
    player.prune_seen = {}
    # (x, y) -> round this unit destroyed it.  Doubles as the ONE-SHOT ban
    # (a key present here is never condemned again, whatever its age) and as
    # the condemned set the two rebuild gates read.
    player.prune_done = {}
    player.prune_kills = 0
    # Instrumentation only; stays empty unless PRUNE_DEBUG.
    player.prune_obs = set()


def prune_condemned(player, pos):
    """True if this unit tore ``pos`` down recently and must not rebuild it.

    Read by _build_next_link and by _move's trail pave.  Cheap by design: one
    dict hit on a dict that never exceeds PRUNE_MAX_TOTAL entries.
    """
    if not PRUNE_ON:
        return False
    done = getattr(player, "prune_done", None)
    if not done:
        return False
    rnd = done.get((pos.x, pos.y))
    return rnd is not None and player.prune_rnd - rnd < PRUNE_CONDEMN_RNDS


# ---------------------------------------------------------------------------
# THE SWEEP
# ---------------------------------------------------------------------------

def prune_sweep(player, ct):
    """Entry point.  Never raises -- an escaped exception permanently deletes
    the unit for the rest of the match, so this whole subsystem sits behind
    its own blanket except in addition to run()'s."""
    if not PRUNE_ON:
        return 0
    try:
        return _sweep(player, ct)
    except Exception:
        return 0


def _sweep(player, ct):
    rnd = ct.get_current_round()
    player.prune_rnd = rnd
    if rnd < PRUNE_MIN_RND:
        return 0
    if player.core is None or player.team is None:
        return 0
    if player.prune_kills >= PRUNE_MAX_TOTAL:
        return 0
    # CPU: the caller already cleared the file's guard, but the sweep sits
    # ahead of the whole role machine, so it re-checks rather than eating the
    # margin that BFS nav and the counterbattery scan are budgeted from.
    if player._cpu_exhausted(ct):
        return 0
    if ct.get_scale_percent() < PRUNE_MIN_SCALE:
        return 0

    p = ct.get_position()
    killed = 0
    for d in CARDINALS:
        if killed >= PRUNE_MAX_PER_RND:
            break
        n = p.add(d)
        if not (0 <= n.x < player.mw and 0 <= n.y < player.mh):
            continue
        key = (n.x, n.y)
        # ONE-SHOT: a tile this unit has already torn down is never condemned
        # again, even after PRUNE_CONDEMN_RNDS lets the rebuild gates reopen.
        # This is what makes an oscillation terminate rather than run forever.
        if key in player.prune_done:
            continue

        verdict = _dead_head(player, ct, n)
        if verdict == 0:
            # Alive, or unprovable.  Forget any partial confirm -- the clock
            # only ever runs on continuous evidence.
            if key in player.prune_seen:
                del player.prune_seen[key]
            continue

        if PRUNE_DEBUG:
            player.prune_obs.add(key)

        seen = player.prune_seen.get(key)
        if seen is None or rnd - seen[1] > PRUNE_GAP_RNDS:
            player.prune_seen[key] = [rnd, rnd]
            continue
        seen[1] = rnd
        need = PRUNE_ENEMY_CONFIRM_RNDS if verdict == 2 else PRUNE_CONFIRM_RNDS
        if rnd - seen[0] < need:
            continue

        if PRUNE_SPARE_HARVESTER_ADJ and _touches_harvester(player, ct, n):
            del player.prune_seen[key]
            continue

        # R9: destroy() raises GameError on an illegal call and an escaped
        # exception deletes the unit.  can_destroy is not optional.
        if not ct.can_destroy(n):
            continue
        ct.destroy(n)
        del player.prune_seen[key]
        player.prune_done[key] = rnd
        player.prune_kills += 1
        killed += 1
        if PRUNE_DEBUG:
            import sys
            print(
                "PRUNE destroy uid=%d rnd=%d tile=%s kind=%s kills=%d obs=%d"
                % (ct.get_id(), rnd, key,
                   "enemy-fed" if verdict == 2 else "dead-head",
                   player.prune_kills, len(player.prune_obs)),
                file=sys.stderr,
            )

    if PRUNE_DEBUG and rnd % 250 == 0:
        import sys
        print(
            "PRUNE census uid=%d rnd=%d observed_orphan_tiles=%d destroyed=%d scale=%.1f"
            % (ct.get_id(), rnd, len(player.prune_obs), player.prune_kills,
               ct.get_scale_percent()),
            file=sys.stderr,
        )
    return killed


def _dead_head(player, ct, n):
    """0 = keep, 1 = dead head, 2 = dead head feeding the ENEMY.

    EVERY unreadable answer returns 0.  ``get_tile_building_id`` raises for an
    in-bounds tile outside vision with the same message as an off-map tile, so
    the fail-safe direction has to be "not an orphan" and must never be
    inverted (R1).
    """
    # Never touch the delivery ring: those tiles aim into the footprint and a
    # gap there severs whatever is behind them.
    if dist_core(n, player.core) <= 1:
        return 0
    # Never destroy a tile this unit is itself about to build on / has planned.
    # link_queue is a short list of Positions (path length, tens at most).
    if player.link_queue and n in player.link_queue:
        return 0

    try:
        bid = ct.get_tile_building_id(n)
    except Exception:
        return 0
    if bid is None:
        return 0
    try:
        if ct.get_team(bid) != player.team:
            return 0
        # CONVEYORS ONLY.  Barriers are excluded because being repeatedly
        # damaged is a barrier's entire job (R4) and because a barrier is the
        # only one of these that blocks movement -- conveyors are bot-passable
        # either way (docs/game-model.md:346), so pruning one opens no lane
        # for a raider that was not already open.  Splitters are excluded
        # because a single-facing test is simply wrong for them: they rotate
        # output among three cardinals (R5).  Harvesters are excluded because
        # harvesters-alive is tiebreak #2 (R6).  Turrets are excluded because
        # a gun is not a relay (R8).
        if ct.get_entity_type(bid) != EntityType.CONVEYOR:
            return 0
        if not PRUNE_LOADED_ON and ct.get_stored_resource(bid) is not None:
            return 0
        f = ct.get_direction(bid)
    except Exception:
        return 0
    if f is None:
        return 0

    out = n.add(f)
    if not (0 <= out.x < player.mw and 0 <= out.y < player.mh):
        return 1                      # faces off the map: provably dead
    if dist_core(out, player.core) == 0:
        return 0                      # outputs into our own Core footprint
    if not ct.is_in_vision(out):
        return 0                      # cannot prove it -> keep
    try:
        obid = ct.get_tile_building_id(out)
    except Exception:
        return 0
    if obid is None:
        # Empty output tile.  This is the pave orphan and the abandoned-lane
        # head, i.e. the volume target -- and also exactly what a lane under
        # construction looks like, which is what PRUNE_CONFIRM_RNDS is for.
        return 1
    try:
        oteam = ct.get_team(obid)
        otype = ct.get_entity_type(obid)
    except Exception:
        return 0
    if oteam == player.team:
        if otype in (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.CORE):
            return 0                  # wired onward
        return 1                      # outputs into a wall of our own turrets
    if otype in (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.CORE):
        return 2                      # WE ARE FEEDING THEM
    return 1


def _touches_harvester(player, ct, n):
    """True if one of our harvesters is orthogonally adjacent to n."""
    for d in CARDINALS:
        t = n.add(d)
        if not (0 <= t.x < player.mw and 0 <= t.y < player.mh):
            continue
        try:
            bid = ct.get_tile_building_id(t)
            if bid is None:
                continue
            if ct.get_team(bid) != player.team:
                continue
            if ct.get_entity_type(bid) == EntityType.HARVESTER:
                return True
        except Exception:
            continue
    return False
