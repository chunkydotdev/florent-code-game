"""prune.py -- LOKI-2: the DESTROY / COST-SCALE PRUNING doctrine.

ABLATION UNIT.  Everything this doctrine adds lives in this file.  Its entire
footprint in main.py is four marked edits (grep ``LOKI-2``):

  1. ``from prune import prune_condemned, prune_state_init, prune_sweep``
  2. ``prune_state_init(self)`` at the end of ``Player.__init__``
  3. ``prune_sweep(self, ct)`` in ``_builder``, right after ``_wire_tick``
  4. three one-line ``prune_condemned()`` gates -- one in ``_build_next_link``
     and one on each of ``_move``'s two pave sites -- that stop this unit
     rebuilding a tile it just tore down (the R7 self-chase)

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

The cost scale is ONE GLOBAL multiplier, not a per-category one, and it tracks
**live** entities.  Engine-probed 2026-08-09 (bots/_probe_scale on hive):

    built 44 -> scale 164.000    destroy -> 42 -> 162.000
    built 12 -> scale 132.000    destroy -> 10 -> 130.000 -> 7 -> 127.000
    rnd=1    0 conveyors  scale 120  harv 24 gun 24 sent 36 bot 36 launch 24
    rnd=53  39 conveyors  scale 159  harv 31 gun 31 sent 47 bot 47 launch 31

i.e. ``scale = 100 + sum over LIVE entities of their category rate`` (Core
contributes 0), every getter is exactly ``floor(scale x base)``, and a destroy
drops the scale the SAME round.  So one orphaned conveyor does not merely make
conveyors 1% dearer -- it taxes every future harvester, gunner, sentinel,
launcher and builder bot by 1%.  ``destroy()`` is the only downward hand we
have on that number, and every point shaved stays shaved.

Measured target set: **18 of 40 surviving relays on heart connect to nothing**
(docs/v79-analysis.md:187).  Eighteen points off a live scale of ~4.05 is
4.05 -> 3.87: a sentinel drops 121 -> 116 Ti, a harvester 81 -> 77, a builder
bot 121 -> 116.  Over a back-half spend of ~2,500 Ti that is ~110-165 Ti
(thread10_destroy_doctrine.md:258-294).

STATED HONESTLY, BECAUSE THE BRIEF ASKED FOR IT: this is a SECOND-ORDER lever
even with the global-multiplier correction.  The discount is ~4-5% of future
spend, not a doubling, because the live builder-bot population (+20% each,
5-10 alive = +100-200%) dominates the multiplier and this doctrine will not
touch it.  The honest expected value is one or two extra purchases per match.

UNPROVEN, AND FLAGGED AS SUCH: late game we run large networks, so replacing a
lost turret may cost us ~1.6-2x base while a lean opponent pays near base --
which would be a second reason the doctrine pays, via late-game replacement
tempo rather than via total titanium.  Nothing here is built on that; it is
recorded so a later measurement knows where to look.

WHY THE SWEEP IS NOT CONDITIONAL ON AN IMPENDING PURCHASE.  It is tempting to
prune harder just before buying a sentinel, since that is where the scale
bites hardest in absolute Ti.  It is not actionable: ``destroy()`` requires
the builder to be orthogonally adjacent to the target, so which orphans are
reachable is decided by where the builder happens to be walking, not by what
the Core wants to buy.  Deferring a provably-safe destroy until a purchase is
pending would only shorten the window in which we enjoy a discount that is
permanent and free.  The correct policy for a free, permanent, monotone lever
is: take it the moment it is provably safe, and never give it back.  The only
condition kept is a scale FLOOR (PRUNE_MIN_SCALE) -- below it there is nothing
worth discounting.


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

from fcode import EntityType

from doctrine import CARDINALS


def _dist_core(pos, o):
    """Chebyshev distance to the nearest tile of the 2x2 Core footprint.

    A local copy of main.py's ``dist_core``: importing it from main would be
    circular (main imports this file).  Three lines, and keeping them here is
    what lets the whole doctrine be one deletable file.  0 means "pos IS a
    footprint tile"; 1 means "orthogonally or diagonally touching it".
    """
    ox, oy = o.x, o.y
    return min(
        max(abs(pos.x - cx), abs(pos.y - cy))
        for cx, cy in ((ox, oy), (ox + 1, oy), (ox, oy + 1), (ox + 1, oy + 1))
    )


# ---------------------------------------------------------------------------
# FLAGS
# ---------------------------------------------------------------------------

# Master ablation switch.  False == _v103split.
PRUNE_ON = True

# LEAK CLASS ONLY: the round from which a conveyor feeding an ENEMY network
# may be pruned.  Much earlier than PRUNE_MIN_RND because the ambiguity that
# gate exists for -- "is this a lane still under construction?" -- cannot
# apply: an enemy building is standing on the output tile, and our lane is not
# going to grow through it.  Every round of delay here is titanium gifted.
PRUNE_LEAK_MIN_RND = 40

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
# lane build time".  MEASURED AND RAISED TWICE: at 40, heart seed 3 destroyed
# 7 distinct tiles and several were rebuilt by a teammate within a few rounds,
# i.e. 40 rounds does not separate "orphan" from "lane whose builder got
# pulled into a heal or a chase" -- and that stall is bounded by nothing.
# 100 rounds still leaves r150..r1000 to prune in, and the asymmetry is stark:
# waiting costs a few rounds of a ~1% discount, a wrong destroy costs a
# rebuild plus a scale flap plus whatever the chain was carrying.
PRUNE_CONFIRM_RNDS = 100

# The confirm clock resets if the tile went unobserved for longer than this.
# Without it, walking away for 300 rounds and coming back makes a tile
# instantly destroyable off one stale sighting.
PRUNE_GAP_RNDS = 8

# SHORT CLOCK, for the two dead-head classes that carry no ambiguity at all.
# The long clock exists solely because an empty output tile might be a lane
# still growing.  Two cases cannot be that:
#   (a) the output tile holds an ENEMY conveyor/splitter/Core.  An enemy
#       building is never going to become our next lane segment, and this
#       conveyor is actively PAYING THEM -- a heart replay has one of our
#       chains delivering a stack into the opponent's Core, scoring their
#       tiebreak #1 (docs/spitball.md T11).  Every round of confirm is loss.
#   (b) the output tile is one THIS UNIT already tore down and still holds
#       condemned.  It was dead the instant that tile died, and our own
#       rebuild gates stop the lane growing back into it.  This is what lets
#       a dead chain unravel backwards at a useful rate instead of one tile
#       per PRUNE_CONFIRM_RNDS.
PRUNE_SHORT_CONFIRM_RNDS = 4

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

# ---------------------------------------------------------------------------
# SECOND ARM -- LEAK PREVENTION AT BUILD TIME.  DEFAULT OFF, UNMEASURED.
# ---------------------------------------------------------------------------
# Refuse to lay a conveyor whose output tile already holds an ENEMY relay or
# the ENEMY CORE.  Costs 3 engine calls per conveyor build, never fires on a
# tile we cannot see, and can only ever REFUSE a build -- it destroys nothing.
#
# WHY IT IS HERE.  The destroy arm can only reach a leaking conveyor if a
# builder stands orthogonally adjacent to it for the whole confirm window, and
# leaking conveyors live on the contested seam where our builders pass through
# rather than loiter.  Measured: 2-13 destroys per game (see DESIGN.md), which
# did not move the replay-measured leak.  Refusing to CREATE the leak has no
# adjacency requirement at all -- the builder is by definition standing next
# to the tile it is about to build on.
#
# WHY IT IS OFF.  Two reasons, both honest.  (1) It is unmeasured: no arena leg
# has been run on it, and the box was reserved when it was written.  (2) It
# only addresses the half of the leak where WE build into THEM; the other half
# is the enemy extending their network onto the tile our conveyor already
# faces, and this gate is blind to that by construction.  Which half dominates
# is not known.  Flip to True and run the leg to find out.
PRUNE_LEAK_BUILD_GATE_ON = False

# Per-unit stderr instrumentation.  print() goes to the replay; stderr is
# console-only (docs/tooling.md), so this is safe to leave compiled in and
# costs one branch when off.
PRUNE_DEBUG = True


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
    # Last round the sweep ran; the condemn window is measured from it.
    player.prune_rnd = -10 ** 9
    # Instrumentation only; stays empty unless PRUNE_DEBUG.
    player.prune_obs = set()
    player.prune_leak_obs = set()


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
    # The LOWER of the two gates: the leak class (verdict 2) opens at
    # PRUNE_LEAK_MIN_RND, the ambiguous class (verdict 1) at PRUNE_MIN_RND,
    # which is re-checked per candidate below.
    if rnd < PRUNE_LEAK_MIN_RND:
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
        if verdict == 1 and rnd < PRUNE_MIN_RND:
            verdict = 0
        if verdict == 0:
            # Alive, or unprovable.  Forget any partial confirm -- the clock
            # only ever runs on continuous evidence.
            if key in player.prune_seen:
                del player.prune_seen[key]
            continue

        if PRUNE_DEBUG:
            player.prune_obs.add(key)
            if verdict == 2:
                player.prune_leak_obs.add(key)

        seen = player.prune_seen.get(key)
        if seen is None or rnd - seen[1] > PRUNE_GAP_RNDS:
            player.prune_seen[key] = [rnd, rnd]
            continue
        seen[1] = rnd
        need = PRUNE_SHORT_CONFIRM_RNDS if verdict == 2 else PRUNE_CONFIRM_RNDS
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
                   "unambiguous" if verdict == 2 else "dead-head",
                   player.prune_kills, len(player.prune_obs)),
                file=sys.stderr,
            )

    if PRUNE_DEBUG and rnd % 250 == 0:
        import sys
        print(
            "PRUNE census uid=%d rnd=%d observed_orphan_tiles=%d leak_tiles=%d destroyed=%d scale=%.1f"
            % (ct.get_id(), rnd, len(player.prune_obs),
               len(player.prune_leak_obs), player.prune_kills,
               ct.get_scale_percent()),
            file=sys.stderr,
        )
    return killed


def _dead_head(player, ct, n):
    """0 = keep, 1 = dead head (long clock), 2 = dead head with no ambiguity
    left in it (short clock: feeding the enemy, or feeding a tile we condemned).

    EVERY unreadable answer returns 0.  ``get_tile_building_id`` raises for an
    in-bounds tile outside vision with the same message as an off-map tile, so
    the fail-safe direction has to be "not an orphan" and must never be
    inverted (R1).
    """
    # Never touch the delivery ring: those tiles aim into the footprint and a
    # gap there severs whatever is behind them.
    if _dist_core(n, player.core) <= 1:
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
        loaded = ct.get_stored_resource(bid) is not None
        f = ct.get_direction(bid)
    except Exception:
        return 0
    if f is None:
        return 0

    verdict = _out_verdict(player, ct, n, f)
    # THE LOADED RULE, and why it is asymmetric.  destroy() INCINERATES the
    # stack (0 Ti returned in 191/191 measured cases), so for an ordinary dead
    # head we simply refuse: 10 Ti burned to shave 1 scale point is a bad
    # trade, and the tile will still be there when it is empty.
    #   But for verdict 2 -- a conveyor whose output is an ENEMY relay or the
    # ENEMY CORE -- the stack's only future is the opponent's balance, and
    # 21% of measured cross-team leak lands directly in their Core, scoring
    # their tiebreak #1.  Incinerating a stack that was about to be GIFTED is
    # a strict improvement over delivering it.  Refusing to prune the loaded
    # ones would also select exactly against the conveyors that are actively
    # leaking, which is the opposite of what this class exists to do.
    if verdict == 1 and loaded and not PRUNE_LOADED_ON:
        return 0
    return verdict


def _out_verdict(player, ct, n, f):
    """Classify the tile a conveyor at ``n`` facing ``f`` outputs into."""
    out = n.add(f)
    if not (0 <= out.x < player.mw and 0 <= out.y < player.mh):
        return 1                      # faces off the map: provably dead
    if _dist_core(out, player.core) == 0:
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
        # A cascade accelerator lived here and was REMOVED after measurement:
        # "output tile is one I condemned -> unambiguous, use the short clock".
        # Its premise was that our own rebuild gates stop the lane growing back
        # into a condemned tile -- but those gates are PER UNIT, so a teammate's
        # linker or trail pave rebuilds it freely.  Measured on heart seed 3:
        # the rule produced 13 of 16 destroys and drove a three-unit relay on
        # tiles (13,16)/(14,16) -- destroy at r426, r430, r435, r439, r443,
        # r446.  Deleted rather than tuned; a dead chain still unravels here,
        # one tile per PRUNE_CONFIRM_RNDS, on evidence rather than on inference.
        return 1
    try:
        oteam = ct.get_team(obid)
        otype = ct.get_entity_type(obid)
    except Exception:
        return 0
    if oteam == player.team:
        if otype in (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.CORE):
            return 0                  # wired onward
        if otype == EntityType.HARVESTER:
            # A conveyor pointing INTO a harvester almost certainly delivers
            # nothing (harvesters are sources), but "almost certainly" is not
            # the standard for an irreversible action and the case is rare.
            return 0
        # Barrier / gunner / sentinel / launcher: turrets "never hold or accept
        # resources" and a barrier has no function at all, so this conveyor is
        # provably terminal.
        return 1
    if otype in (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.CORE):
        return 2                      # WE ARE FEEDING THEM
    return 1


def prune_leak_build_ok(player, ct, tile, facing):
    """False if a conveyor at ``tile`` facing ``facing`` would feed the ENEMY.

    Fail-safe direction is the opposite of the sweep's: an unreadable answer
    returns True (allow the build), because refusing builds on unprovable
    evidence would starve the economy, which is the one failure this bot
    cannot afford.  Never raises.
    """
    if not PRUNE_ON or not PRUNE_LEAK_BUILD_GATE_ON:
        return True
    try:
        if facing is None or player.team is None:
            return True
        out = tile.add(facing)
        if not (0 <= out.x < player.mw and 0 <= out.y < player.mh):
            return True
        if not ct.is_in_vision(out):
            return True
        obid = ct.get_tile_building_id(out)
        if obid is None:
            return True
        if ct.get_team(obid) == player.team:
            return True
        return ct.get_entity_type(obid) not in (
            EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.CORE
        )
    except Exception:
        return True


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
