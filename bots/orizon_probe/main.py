"""orizon_probe -- the Orizon family's point-blank gunner core battery, frozen
as an instrument.  NOT a ladder bot.

Provenance
----------
Replay-decoded class exemplar for the single largest behavioural block in the
ladder pool: Orizon, team lazy, Team 48 and Leviathan share one script and
between them are ~46% of the field.  Primary decode:
`docs/research/2026-08-07-fanout/findings/thread7_landers_orizon.md` (six games,
v53 -> v56 -> v61, both seats); plant-distance calibration:
`docs/research/orizon-family-2026-08-07.md` sections 1-5 (18 further games).

The script, as measured:

  1. **Exactly 4 builder bots, spawned r0-r3, never another one.**  (The fresh
     `607ffaeb` series shows Orizon itself respawning past r350 in long games;
     this probe freezes the SHORT-game rule, which is the one that produces the
     failure mode we are instrumenting.)
  2. Builder #1 walks **straight at the enemy Core from round 0** at one tile
     per round, ignoring everything on the way.  Builders #2-#4 put up 1-3
     harvesters and a short conveyor stub into the Core -- that is the entire
     economy -- and then follow #1 forward.
  3. The moment a forward builder has an orthogonally adjacent tile whose
     gunner ray contains an enemy Core footprint tile, it plants a **GUNNER**
     there.  Then it keeps planting, each one on the closest legal aligned tile
     left, so the plant sequence creeps in: measured fp_dsq 9 -> 4 -> 2 -> 1
     (Team 48's fjordgate g3 is the cleanest recorded shape: 5,4,2,2,2,1,1,1,1,5).
     **It never rotates** -- a fresh gunner adds DPS, a rotation only redirects.
  4. Builders park orthogonally beside their own gunners and **heal them**
     (3-16 heals/game), so a defender's 2 Ti pecks never win the trade.  This is
     the one place the family splits: Orizon defends its front gunner, team lazy
     and Team 48 mostly do not.  This probe takes Orizon's harder reading.
  5. Titanium is converted to ammunition in **4-20 Ti dribbles, nearly every
     round**, with no reserve held back (eider 64 convert rounds of 93; jackpot
     158/213).  The whole economy is a pump into gunner shots: 116-207 shots per
     game against a defender's 1-50.
  6. **Zero sentinels, zero launchers, zero barriers.  Ever.**  That is the
     class fingerprint and this file must never break it.

Kill mechanism to reproduce: two or three gunners at fp_dsq 1-9, 7 damage each
on a 2-round reload, giving a sustained 7 -> 14 -> 21 HP/round bleed on the
defender's Core while its builders stand next to it spending every action on a
+4 HP repair they cannot win with.  These are not fast kills -- they are a fast
STRIKE followed by an unanswered 60-90 round bleed, landing r64-r159 against
weak defence.

What this instrument is for
---------------------------
Gating our own defensive pieces -- heal budget and counterbattery -- against the
exact pressure that beats them.  Fidelity to the decode beats strength: a probe
harsher than the wild exemplar poisons every verdict taken against it, and a
probe that stalls at home measures nothing at all.

Deliberate deviations from the letter of the spec, both minimal and both
documented where they are implemented:

  * **The Core reserves the next scripted build (see `_reserve`).**  "Hold no
    titanium reserve" taken literally -- `amount = min(ti - 10, 20)` every round
    -- pins the bank at 10 Ti forever, because the 20 Ti/round conversion cap is
    larger than passive income plus three harvesters.  A probe that can never
    afford a 20 Ti gunner reproduces nothing.  So the floor carries the cost of
    the *next item in the script only* (opening builder / harvester below target
    / the next gunner), never a safety float.  It is worth noting that this
    reproduces the measured band exactly: the reserve is one gunner cost, which
    scales 20, 24, 28, 34, 41, 49 ... and the decode's own reading of Orizon is
    "global titanium held at 0-60 all game".  Ammunition still outranks the
    reserve (see AMMO_KEEP) -- the family fires 116-207 shots a game, and a
    battery saving up for a gun it has no shots to feed is not that family.
  * **Forward builders never melee.**  The decode attributes essentially all of
    the family's core damage to gunfire; keeping builder pecks out of the probe
    keeps damage attributable to the battery, which is the whole point of the
    instrument.

Determinism
-----------
No randomness anywhere.  Every tile, direction and target choice is resolved by
an explicit sort key -- `(distance_squared, x, y)` throughout -- and every
collection derived from a set is sorted before it is iterated.  Given
(map, seat, opponent) this file plays the same game every run.

Robustness
----------
An uncaught exception permanently deletes the unit for the rest of the match, so
every unit's turn body is wrapped and every mutating call is gated by its
matching `can_*()` predicate.  No `try`/`finally` anywhere: the platform's
bot-code validator rejects `finally` blocks outright (docs/tooling.md).

Communication store slots
-------------------------
   0  SLOT_HOME        packed position of our own Core
   1  SLOT_ENEMY       packed position of the enemy Core, once sighted
   2  SLOT_ROLE_NEXT   builder role claim counter (0 = lancer, 1..3 = economy)
   3  SLOT_GUNNERS     gunners planted so far
   4  SLOT_HARVESTERS  harvesters built so far
"""

import sys

from fcode import (
    Controller,
    Direction,
    EntityType,
    Environment,
    GameError,
    Position,
)

# --- store slots -----------------------------------------------------------
SLOT_HOME = 0
SLOT_ENEMY = 1
SLOT_ROLE_NEXT = 2
SLOT_GUNNERS = 3
SLOT_HARVESTERS = 4

# --- the labour force ------------------------------------------------------
# "Exactly 4 builder bots at r0-r3, never another one."  The cap is on the
# COUNT, not the round: if a spawn ring tile is blocked on r1 the Core simply
# tries again on r2.  In practice this lands r0/r1/r2/r3 on every pool map.
# Role 0 is the lancer (walks at the enemy Core from round 0); roles 1-3 run the
# economy and then follow it forward.
BUILDER_TARGET = 4
ROLE_LANCER = 0

# --- the economy underneath ------------------------------------------------
# Decoded: 1-4 harvesters and a short conveyor stub, and on fjordgate zero
# harvesters and zero delivered titanium for 350 rounds.  This is not an economy
# in any competitive sense -- it is just enough titanium to keep the ammunition
# converter fed.
HARVESTER_TARGET = 3
# ...and it is time-boxed.  A builder that cannot find ore is worth more walking
# at the enemy Core than wandering: the exemplar's economy failing outright is
# an observed state (fjordgate), not a bug to be defended against.
ECO_GIVEUP_RND = 60
MAX_CHAIN = 8

# --- the battery -----------------------------------------------------------
GUNNER_RANGE_SQ = 13
# An upper bound, not a plan.  Orizon reached 23 plants in a 550-round game and
# 2-3 simultaneous in the short ones; the cap exists so a runaway game does not
# turn the probe into something the decode never saw.
GUNNER_TARGET = 16
# Only scan for plant sites once the builder is roughly within a gunner's reach
# of the enemy Core footprint.  A site is legal only if a hypothetical gunner on
# it could actually fire on a footprint tile (`can_fire_from`, which for gunners
# checks range, alignment AND line-of-sight), so this is a cheap CPU pre-filter,
# not the real gate.
PLANT_SCAN_DSQ = 34
# The heal is 1 Ti for +4 HP.  The reserve floor keeps at least SMALL_FLOOR in
# the bank, so this only ever refuses when the team is genuinely broke.
HEAL_MIN_TITANIUM = 2

# --- ammunition ------------------------------------------------------------
# `amount = min(ti - SMALL_FLOOR, AMMO_CHUNK)` every single round, no ceiling:
# the decode's "4-20 Ti dribbles, nearly every round, holding titanium at 0-60".
# There is deliberately no ammo cap -- banked ammunition the battery cannot spend
# is dead capital, and the exemplar carries exactly that dead capital.
SMALL_FLOOR = 10
AMMO_CHUNK = 20
# Ammunition the battery must be holding before the Core will start saving up
# for the NEXT gunner instead of for shots -- six gunner shots, which is the
# working bank Team 48 is measured holding while under fire (strike 28 vs quiet
# 1 in `bce041d8` g3).
#
# This single condition is what keeps the pump a pump.  Reserving the next
# gunner unconditionally looks harmless and is not: gunners carry a +20%
# category scale, so the reserve climbs 20 -> 24 -> 28 -> 34 -> 41 -> 49 -> 59
# -> 71 -> 86, and a probe with a small economy then pins its whole bank under
# that reserve and stops converting entirely.  Measured on nordkap before this
# gate existed: 8 gunners planted, 187 Ti converted in 155 rounds, and the last
# FOUR gunners -- all of them at fp_dsq 1-2, exactly the ones the instrument
# exists to reproduce -- never fired a single shot in 80 rounds.  The family
# fires 116-207 shots a game.  Ammunition first, then the next gun.
AMMO_KEEP = 24

# Bail at a phase boundary rather than let the engine truncate a statement.
# NOTE: get_cpu_time_elapsed() reads 0 under local `fcode run` even with --tle
# (docs/tooling.md), so this guard only bites on ladder hardware.
CPU_BUDGET_US = 7000

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)

# Competition-map Core anchors, copied from bots/_v70cm via bots/cad_probe.
# Several pool maps are mirror-symmetric rather than 180-degree symmetric, so
# (w-2-x, h-2-y) is not generally the enemy Core; this table lets the lancer
# set off in the right direction on round 0 instead of on first sighting.  The
# rotational fallback below keeps the probe usable on an unknown map.
CORE_PAIRS = (
    (18, 18, 2, 14, 14, 2), (26, 26, 3, 22, 21, 2),
    (21, 8, 0, 6, 19, 6), (16, 16, 2, 11, 12, 3),
    (12, 12, 1, 8, 9, 2), (20, 20, 2, 15, 16, 3),
    (25, 25, 2, 20, 21, 3), (16, 16, 0, 0, 14, 14),
    (28, 20, 2, 8, 24, 8), (14, 18, 2, 2, 2, 14),
    (24, 24, 2, 2, 20, 20), (24, 24, 2, 11, 20, 11),
    (16, 12, 4, 5, 10, 5), (22, 22, 2, 17, 18, 3),
    (10, 10, 1, 1, 7, 7), (20, 26, 2, 2, 2, 22),
    (12, 8, 0, 6, 10, 0), (25, 15, 0, 0, 0, 13),
    (21, 21, 2, 2, 2, 17), (11, 16, 0, 0, 9, 0),
    (24, 24, 2, 19, 20, 3),
    (21, 8, 5, 3, 14, 3), (26, 26, 5, 5, 19, 19),
    (10, 10, 2, 2, 6, 6), (16, 16, 3, 3, 11, 11),
    (14, 18, 6, 4, 6, 12), (20, 26, 9, 6, 9, 18),
    (28, 20, 7, 9, 19, 9), (25, 15, 11, 3, 11, 10),
    (25, 25, 5, 5, 18, 18), (24, 24, 4, 4, 18, 18),
)


def pack_pos(pos: Position) -> int:
    """Encode a position into one store int, offset so (0,0) is not 'empty'."""
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val: int):
    if val <= 0:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def in_bounds(ct: Controller, pos: Position) -> bool:
    """On the map.  Necessary but not sufficient before a tile query -- tile
    getters also raise GameError for in-bounds tiles outside current vision.
    """
    return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()


def core_footprint(nw: Position):
    """The 4 tiles of a Core's 2x2 footprint, given its NW corner."""
    return (
        nw,
        Position(nw.x + 1, nw.y),
        Position(nw.x, nw.y + 1),
        Position(nw.x + 1, nw.y + 1),
    )


def nearest_core_tile(pos: Position, core_nw: Position) -> Position:
    best = None
    for tile in core_footprint(core_nw):
        key = (pos.distance_squared(tile), tile.x, tile.y)
        if best is None or key < best[0]:
            best = (key, tile)
    return best[1]


def core_dist_sq(pos: Position, core_nw: Position) -> int:
    """fp_dsq: squared distance to the NEAREST Core footprint tile.  This is the
    thread7 / denial-book convention the plant-distance tables are quoted in.
    """
    return pos.distance_squared(nearest_core_tile(pos, core_nw))


def adjacent_core_tile(pos: Position, core_nw: Position):
    """The Core footprint tile orthogonally adjacent to pos, if any -- i.e. the
    tile a conveyor on pos must face to actually deliver.
    """
    for tile in core_footprint(core_nw):
        if abs(tile.x - pos.x) + abs(tile.y - pos.y) == 1:
            return tile
    return None


def enemy_core_for(w: int, h: int, own: Position) -> Position:
    for mw, mh, ax, ay, bx, by in CORE_PAIRS:
        if w != mw or h != mh:
            continue
        if own.x == ax and own.y == ay:
            return Position(bx, by)
        if own.x == bx and own.y == by:
            return Position(ax, ay)
    return Position(max(0, w - 2 - own.x), max(0, h - 2 - own.y))


class _BuilderState:
    """Per-builder-bot state.

    The engine creates one Player instance per unit (docs/game-model.md), so
    plain attributes would do -- but this file is a frozen instrument that has
    to keep giving the same answer if that ever changes, so every mutable
    builder field lives in a dict keyed by `ct.get_id()` instead.  At most four
    builder bots ever exist, so the dict never grows.
    """

    __slots__ = (
        "role", "prev_pos", "stuck", "recent", "stage", "known_ore",
        "ore_target", "harvester_pos", "built_harvester", "trail_prev",
        "chain_tiles", "chain_len", "cap_tile", "own_rays", "explore_idx",
    )

    def __init__(self):
        self.role = None
        self.built_harvester = False
        self.prev_pos = None
        self.stuck = 0
        self.recent = []
        # "eco" -> "lay" -> "cap" -> back to "eco"; "forward" is terminal.
        self.stage = "eco"
        self.known_ore = set()
        self.ore_target = None
        self.harvester_pos = None
        self.trail_prev = None
        self.chain_tiles = set()
        self.chain_len = 0
        self.cap_tile = None
        # Tiles already covered by a gunner this builder planted.  Planting a
        # second gunner INTO the first one's ray converts two guns into one, so
        # sites on a known friendly ray are taken last.
        self.own_rays = set()
        self.explore_idx = 0


class Player:
    def __init__(self):
        # --- shared map knowledge -----------------------------------------
        self.home = None
        self.enemy = None
        self.enemy_confirmed = False

        # --- Core ----------------------------------------------------------
        self.spawned = 0

        # --- builder bots ----------------------------------------------------
        self.builders = {}

        self.reported_error = False

    # ------------------------------------------------------------------
    # entry point
    # ------------------------------------------------------------------

    def run(self, ct: Controller) -> None:
        """An exception escaping run() permanently deletes this unit for the
        rest of the match, so the guard is unconditional.  Never try/finally --
        the platform validator rejects `finally` blocks.
        """
        try:
            self._dispatch(ct)
        except Exception:
            if not self.reported_error:
                self.reported_error = True
                import traceback

                traceback.print_exc(file=sys.stderr)

    def _dispatch(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            self._run_core(ct)
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)
        elif etype == EntityType.GUNNER:
            self._run_gunner(ct)
        # No other unit type is ever built: zero sentinels, zero launchers,
        # zero barriers, in all 18 decoded games.  The absence is the class.

    def _cpu_exhausted(self, ct: Controller) -> bool:
        return ct.get_cpu_time_elapsed() >= CPU_BUDGET_US

    # ------------------------------------------------------------------
    # map knowledge
    # ------------------------------------------------------------------

    def _locate(self, ct: Controller) -> None:
        """Establish home and enemy Core positions as cheaply as possible:
        sight them, else read the store, else look the pair up in CORE_PAIRS,
        else fall back to 180-degree rotation.

        The lancer has to set off on round 0, before anything has sighted the
        enemy, so the table matters: several pool maps are mirror-symmetric and
        the rotational guess is a couple of tiles off there.  Any direct
        sighting overrides it.
        """
        if self.home is None or not self.enemy_confirmed:
            my_team = ct.get_team()
            try:
                nearby = ct.get_nearby_buildings()
            except GameError:
                nearby = ()
            for bid in nearby:
                try:
                    if ct.get_entity_type(bid) != EntityType.CORE:
                        continue
                    where = ct.get_position(bid)
                    if ct.get_team(bid) == my_team:
                        self.home = where
                    else:
                        self.enemy = where
                        if not self.enemy_confirmed:
                            self.enemy_confirmed = True
                            ct.write_store(SLOT_ENEMY, pack_pos(where))
                except GameError:
                    continue

        if self.home is None:
            self.home = unpack_pos(ct.read_store(SLOT_HOME))
        if not self.enemy_confirmed:
            stored = unpack_pos(ct.read_store(SLOT_ENEMY))
            if stored is not None:
                self.enemy = stored
                self.enemy_confirmed = True
        if self.enemy is None and self.home is not None:
            self.enemy = enemy_core_for(
                ct.get_map_width(), ct.get_map_height(), self.home
            )

    # ==================================================================
    # CORE -- four builders, then nothing but the ammunition pump
    # ==================================================================

    def _run_core(self, ct: Controller) -> None:
        pos = ct.get_position()
        if self.home is None:
            self.home = pos
            ct.write_store(SLOT_HOME, pack_pos(pos))
        self._locate(ct)

        rnd = ct.get_current_round()
        reserve = self._reserve(ct, rnd)

        # convert_ammo() does not consume the action cooldown, so converting
        # never costs a spawn -- it is always tried first, on every round of the
        # match including r0.
        self._convert(ct, reserve)

        if ct.get_action_cooldown() != 0:
            return
        if self.spawned >= BUILDER_TARGET:
            return  # "Never raise the labour force."  No respawns, ever.
        self._spawn(ct, pos, reserve)

    def _reserve(self, ct: Controller, rnd: int) -> int:
        """Titanium the converter leaves alone: SMALL_FLOOR plus the cost of the
        NEXT item in the script, and nothing else.

        This is the one deliberate deviation from "hold no titanium reserve at
        all" (see the module docstring).  Taken literally that rule pins the bank
        at 10 Ti for the whole match -- the 20 Ti/round conversion cap outruns
        passive income plus three harvesters -- and a probe that can never afford
        a gunner reproduces none of the failure mode it exists to reproduce.

        There is no safety float, no economy float and no ammunition ceiling
        here: everything above the next scripted build goes into shots.  And the
        gunner half of the reserve is itself subordinate to ammunition (see
        AMMO_KEEP) -- a bank saved for a gun the battery has no shots to feed is
        the one thing the exemplar never does.

        The result matches the decode's own reading of the exemplar, which holds
        global titanium at 0-60 all game while converting nearly every round: in
        the ordinary case the reserve is SMALL_FLOOR plus one gunner cost, and a
        gunner costs 20, 24, 28, 34, 41 ... as the +20% category scale climbs.
        """
        reserve = SMALL_FLOOR
        if self.spawned < BUILDER_TARGET:
            reserve += ct.get_builder_bot_cost()
        if ct.read_store(SLOT_HARVESTERS) < HARVESTER_TARGET and rnd < ECO_GIVEUP_RND:
            reserve += ct.get_harvester_cost()
        if (
            ct.read_store(SLOT_GUNNERS) < GUNNER_TARGET
            and ct.get_global_ammo() >= AMMO_KEEP
        ):
            reserve += ct.get_gunner_cost()
        return reserve

    def _convert(self, ct: Controller, reserve: int) -> None:
        """`amount = min(ti - reserve, 20)`, every round, no ceiling."""
        amount = min(ct.get_global_resources() - reserve, AMMO_CHUNK)
        if amount <= 0:
            return
        try:
            if ct.can_convert_ammo(amount):
                ct.convert_ammo(amount)
        except GameError:
            return

    def _spawn(self, ct: Controller, pos: Position, reserve: int) -> None:
        """Spawn on the ring tile nearest the enemy, so the lancer starts its
        walk one tile up the road.

        The whole ring is enumerated via get_nearby_tiles(8) and filtered by
        can_spawn(), never by pos.add(d) -- that only reaches the N/W half of
        the ring and is an absolute-direction bug that decides maps by seat.
        `reserve` already contains one builder cost while spawns are owed, so
        the affordability test is `>= reserve`, never `>= cost + reserve`.
        """
        if ct.get_global_resources() < max(ct.get_builder_bot_cost(), reserve):
            return
        anchor = self.enemy if self.enemy is not None else pos
        best = None
        for tile in ct.get_nearby_tiles(dist_sq=8):
            try:
                if not ct.can_spawn(tile):
                    continue
            except GameError:
                continue
            key = (tile.distance_squared(anchor), tile.x, tile.y)
            if best is None or key < best[0]:
                best = (key, tile)
        if best is None:
            return
        try:
            ct.spawn_builder(best[1])
        except GameError:
            return
        self.spawned += 1

    # ==================================================================
    # BUILDER BOT
    # ==================================================================

    def _run_builder(self, ct: Controller) -> None:
        rnd = ct.get_current_round()
        pos = ct.get_position()
        self._locate(ct)

        uid = ct.get_id()
        st = self.builders.get(uid)
        if st is None:
            st = _BuilderState()
            self.builders[uid] = st

        if st.role is None:
            self._claim_role(ct, st)

        if st.prev_pos is not None:
            if pos == st.prev_pos:
                st.stuck += 1
            else:
                st.stuck = 0
        st.prev_pos = pos
        # Short tabu list.  Without it a builder that meets a blocker on its
        # preferred axis steps aside, finds the axis clear again from the new
        # tile, steps back, and 2-cycles there for the rest of the match --
        # `stuck` never fires because the bot is moving every round.
        st.recent.append((pos.x, pos.y))
        if len(st.recent) > 4:
            st.recent.pop(0)

        if st.role == ROLE_LANCER:
            # "Navigate straight at the enemy core from round 0, ignoring
            # everything else."  The lancer never touches the economy.
            self._run_forward(ct, st, rnd, pos, lancer=True)
            return

        # Leave for the front only from BETWEEN jobs.  Testing this against any
        # stage rather than "eco" abandons half-laid conveyor stubs the moment
        # the third harvester goes up (measured on eider: harvesters at r5/r6/r7,
        # all three chains dropped at r8, one conveyor laid, ZERO titanium
        # delivered in 93 rounds -- which starved the battery to 40 shots against
        # the family's measured 116-207).  An unfinished chain delivers exactly
        # nothing, so the stub has to be finished before the builder walks.
        # ECO_GIVEUP_RND stays a HARD deadline on top of that, so a chain that
        # cannot be finished can never trap a builder at home: the exemplar's
        # economy failing outright is an observed state (fjordgate: zero
        # harvesters, zero titanium delivered in 350 rounds), and the answer to
        # it is a builder walking at the Core, not one milling about.
        if st.stage != "forward" and rnd >= ECO_GIVEUP_RND:
            st.stage = "forward"
        elif st.stage == "eco" and self._eco_done(ct, st):
            st.stage = "forward"
        if st.stage == "forward":
            self._run_forward(ct, st, rnd, pos, lancer=False)
        else:
            self._run_eco(ct, st, rnd, pos)

    def _claim_role(self, ct: Controller, st: _BuilderState) -> None:
        """Roles are claimed in spawn order off a shared counter.

        The Core spawns at most one builder per round (its action cooldown
        guarantees it) and a fresh builder claims on its first turn, so the
        buffered store write cannot hand the same index to two builders: the
        r0 builder reads 0, the r1 builder reads 1, and so on.
        """
        raw = ct.read_store(SLOT_ROLE_NEXT)
        st.role = raw
        ct.write_store(SLOT_ROLE_NEXT, raw + 1)

    def _eco_done(self, ct: Controller, st: _BuilderState) -> bool:
        """One harvester and one stub each, then follow the lancer.

        The primary test is this builder's OWN flag, not the team counter, and
        that is not a stylistic preference -- the counter cannot be trusted for
        this.  Store writes buffer for a round, so two builders that finish a
        harvester on the same round both read the same value and both write the
        same value back, and the count lands one short forever.  Measured on
        nordkap: harvesters at r6/r8/r8, SLOT_HARVESTERS stuck at 2 against a
        target of 3, and all three followers milled around their own ore for
        **sixty rounds** while the lancer's battery sat unhealed at fp_dsq 1-2.
        Three followers with one harvester each is the decoded shape anyway
        ("1-3 harvesters and a short conveyor stub"), so the flag is both the
        robust test and the faithful one; the team counter stays on as a cap.
        """
        return (
            st.built_harvester
            or ct.read_store(SLOT_HARVESTERS) >= HARVESTER_TARGET
        )

    # ------------------------------------------------------------------
    # forward: plant the battery, then keep it alive
    # ------------------------------------------------------------------

    def _run_forward(
        self, ct: Controller, st: _BuilderState, rnd: int, pos: Position, lancer: bool
    ) -> None:
        """The lancer plants first and heals second; the followers heal first
        and plant second.

        That split is the decoded division of labour rather than a tuning knob:
        the walking builder is what creates the battery (its whole job is to
        arrive and plant), and the builders that catch up are what keep it
        standing -- "builders park beside their own gunners and heal them, so
        our 2 Ti pecks never win the trade".
        """
        if self.enemy is None:
            return

        near = core_dist_sq(pos, self.enemy) <= PLANT_SCAN_DSQ
        if ct.get_action_cooldown() == 0 and not self._cpu_exhausted(ct):
            if lancer:
                if near and self._plant_gunner(ct, st, pos):
                    return
                if self._heal_adjacent(ct, pos):
                    return
            else:
                if self._heal_adjacent(ct, pos):
                    return
                if near and self._plant_gunner(ct, st, pos):
                    return

        if self._cpu_exhausted(ct):
            return
        self._forward_move(ct, st, pos, lancer)

    def _plant_gunner(self, ct: Controller, st: _BuilderState, pos: Position) -> bool:
        """Plant a GUNNER on the closest orthogonally adjacent tile whose facing
        ray contains an enemy Core footprint tile.

        This one rule is the whole plant-distance signature.  `can_fire_from()`
        for a gunner checks range (r^2 <= 13), exact alignment on the facing
        ray, AND line of sight -- so a site is legal only if a gunner standing
        there would genuinely be shooting the Core.  Ranking the legal sites by
        (fp_dsq, x, y) and taking the closest is what produces the measured
        creep with no schedule anywhere in the code:

          * the first plant happens the round the walking builder first has ANY
            such tile, which is at the outer edge of gunner reach -- fp_dsq 4-13,
            and 9 in the plurality of decoded games;
          * the builder keeps walking at the Core afterwards, so every later
            plant is picked from a strictly tighter set of adjacent tiles, and
            the sequence creeps to fp_dsq 2 and then 1 (a tile orthogonally
            adjacent to a footprint tile is trivially aligned with it);
          * replants after a gunner dies land tighter still, because by then the
            builder is standing on the Core's doorstep.

        Facing comes from `site.direction_to(target)`, which returns the nearest
        45-degree compass direction -- exact precisely when the target is on a
        row, column or true diagonal from the site, which is the only case a
        single-tile-wide ray can hit anyway.

        Never a sentinel, never a launcher, never a barrier.
        """
        if ct.read_store(SLOT_GUNNERS) >= GUNNER_TARGET:
            return False
        cost = ct.get_gunner_cost()
        if ct.get_global_resources() < cost:
            return False

        targets = core_footprint(self.enemy)
        best = None
        for d in CARDINALS:
            site = pos.add(d)
            if not in_bounds(ct, site):
                continue
            # A site inside one of our own gunners' rays is taken only if
            # nothing else is available: planting there turns two guns into one.
            shadowed = 1 if (site.x, site.y) in st.own_rays else 0
            for tile in targets:
                dsq = site.distance_squared(tile)
                if dsq > GUNNER_RANGE_SQ:
                    continue
                facing = site.direction_to(tile)
                if facing == Direction.CENTRE:
                    continue
                try:
                    if not ct.can_fire_from(site, facing, EntityType.GUNNER, tile):
                        continue
                    if not ct.can_build_gunner(site, facing):
                        continue
                except GameError:
                    continue
                key = (shadowed, core_dist_sq(site, self.enemy), site.x, site.y)
                if best is None or key < best[0]:
                    best = (key, site, facing)
        if best is None:
            return False

        try:
            ct.build_gunner(best[1], best[2])
        except GameError:
            return False
        ct.write_store(SLOT_GUNNERS, ct.read_store(SLOT_GUNNERS) + 1)
        try:
            for tile in ct.get_attackable_tiles_from(
                best[1], best[2], EntityType.GUNNER
            ):
                st.own_rays.add((tile.x, tile.y))
        except GameError:
            pass
        return True

    def _heal_adjacent(self, ct: Controller, pos: Position) -> bool:
        """1 Ti for +4 HP on an orthogonally adjacent damaged friendly.

        `can_heal()` refuses a full-HP target, so the HP check is not merely an
        optimisation -- calling heal() blind on an undamaged gunner raises.
        """
        if ct.get_global_resources() < HEAL_MIN_TITANIUM:
            return False
        my_team = ct.get_team()
        best = None
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile):
                continue
            try:
                bid = ct.get_tile_building_id(tile)
                if bid is None or ct.get_team(bid) != my_team:
                    continue
                if ct.get_hp(bid) >= ct.get_max_hp(bid):
                    continue
                if not ct.can_heal(tile):
                    continue
                etype = ct.get_entity_type(bid)
            except GameError:
                continue
            # Gunners first: the battery is the strategy, the stub is not.
            key = (0 if etype == EntityType.GUNNER else 1, tile.x, tile.y)
            if best is None or key < best[0]:
                best = (key, tile)
        if best is None:
            return False
        try:
            ct.heal(best[1])
        except GameError:
            return False
        return True

    def _forward_move(
        self, ct: Controller, st: _BuilderState, pos: Position, lancer: bool
    ) -> None:
        """The lancer walks at the Core and keeps walking at it.  Followers park
        beside a gunner instead, which is where their heals do the work.
        """
        if ct.get_move_cooldown() != 0:
            return
        if lancer:
            self._step_toward(ct, st, pos, nearest_core_tile(pos, self.enemy))
            return

        station = self._medic_station(ct, st, pos)
        if station is not None:
            if station != pos:
                self._step_toward(ct, st, pos, station)
            return
        self._step_toward(ct, st, pos, nearest_core_tile(pos, self.enemy))

    def _medic_station(self, ct: Controller, st: _BuilderState, pos: Position):
        """A tile orthogonally adjacent to the friendly gunner this builder is
        minding, preferring one that is not standing in that gunner's own ray.

        Assignment is by role index across the gunners currently in vision,
        sorted by (distance, x, y), so three followers spread over three guns
        instead of queueing on one -- and it is recomputed every round rather
        than latched, so a medic whose gunner dies simply picks up the next.
        """
        my_team = ct.get_team()
        guns = []
        try:
            nearby = ct.get_nearby_buildings()
        except GameError:
            return None
        for bid in nearby:
            try:
                if ct.get_team(bid) != my_team:
                    continue
                if ct.get_entity_type(bid) != EntityType.GUNNER:
                    continue
                where = ct.get_position(bid)
                facing = ct.get_direction(bid)
            except GameError:
                continue
            guns.append((pos.distance_squared(where), where.x, where.y, where, facing))
        if not guns:
            return None
        guns.sort(key=lambda g: (g[0], g[1], g[2]))
        idx = min(max((st.role or 0) - 1, 0), len(guns) - 1)
        gun_pos = guns[idx][3]
        gun_facing = guns[idx][4]

        if abs(gun_pos.x - pos.x) + abs(gun_pos.y - pos.y) == 1:
            return pos  # already on station

        ray = set()
        try:
            for tile in ct.get_attackable_tiles_from(
                gun_pos, gun_facing, EntityType.GUNNER
            ):
                ray.add((tile.x, tile.y))
        except GameError:
            pass

        best = None
        for d in CARDINALS:
            tile = gun_pos.add(d)
            if not in_bounds(ct, tile):
                continue
            try:
                if not ct.is_tile_passable(tile):
                    continue
            except GameError:
                continue
            key = (
                1 if (tile.x, tile.y) in ray else 0,
                pos.distance_squared(tile),
                tile.x,
                tile.y,
            )
            if best is None or key < best[0]:
                best = (key, tile)
        return best[1] if best is not None else None

    # ------------------------------------------------------------------
    # economy -- 1-3 harvesters and a short conveyor stub, then forward
    # ------------------------------------------------------------------

    def _run_eco(
        self, ct: Controller, st: _BuilderState, rnd: int, pos: Position
    ) -> None:
        if self._cpu_exhausted(ct):
            return
        if st.stage == "eco":
            self._scan_ore(ct, st)
            self._eco_seek_ore(ct, st, pos)
        elif st.stage == "lay":
            self._eco_lay(ct, st, pos)
        elif st.stage == "cap":
            self._eco_cap(ct, st, pos)

    def _scan_ore(self, ct: Controller, st: _BuilderState) -> None:
        """Remember ore tiles seen.  Builder vision is r^2=20, so ~60 tiles."""
        try:
            tiles = ct.get_nearby_tiles()
        except GameError:
            return
        for tile in tiles:
            try:
                if ct.get_tile_env(tile) == Environment.ORE_TITANIUM:
                    st.known_ore.add((tile.x, tile.y))
            except GameError:
                continue

    def _eco_seek_ore(self, ct: Controller, st: _BuilderState, pos: Position) -> None:
        """Walk to the nearest free ore and plant a harvester on it."""
        free = []
        for (x, y) in sorted(st.known_ore):
            tile = Position(x, y)
            try:
                if ct.get_tile_building_id(tile) is not None:
                    continue
            except GameError:
                pass  # out of vision: assume free, re-checked on arrival
            free.append(tile)
        if not free:
            self._step_toward(ct, st, pos, self._explore_target(ct, st, pos))
            return

        # Nearest to HOME, not to the builder: the stub has to reach the Core,
        # and ranking by distance to the builder walks it steadily away and
        # doubles the conveyor run for every harvester.
        anchor = self.home if self.home is not None else pos
        free.sort(key=lambda t: (t.distance_squared(anchor), t.x, t.y))
        # Each economy builder prefers a different one of the nearest few so
        # they do not all queue for the same tile.  Deterministic in role index.
        rank = min(max((st.role or 1) - 1, 0), len(free) - 1)
        st.ore_target = free[rank]

        if (
            ct.get_action_cooldown() == 0
            and ct.get_global_resources() >= ct.get_harvester_cost()
            and ct.read_store(SLOT_HARVESTERS) < HARVESTER_TARGET
        ):
            for tile in free[:4]:
                if abs(tile.x - pos.x) + abs(tile.y - pos.y) != 1:
                    continue
                try:
                    if not ct.can_build_harvester(tile):
                        continue
                    ct.build_harvester(tile)
                except GameError:
                    continue
                ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)
                st.built_harvester = True
                st.harvester_pos = tile
                st.known_ore.discard((tile.x, tile.y))
                self._begin_chain(st)
                return
        self._step_toward(ct, st, pos, st.ore_target)

    def _begin_chain(self, st: _BuilderState) -> None:
        """A harvester orthogonally adjacent to the Core delivers straight into
        it, so the shortest possible stub is no stub at all.
        """
        st.chain_len = 0
        st.trail_prev = None
        st.chain_tiles = set()
        if self.home is not None and st.harvester_pos is not None:
            if adjacent_core_tile(st.harvester_pos, self.home) is not None:
                st.stage = "eco"
                return
        st.stage = "lay"

    def _eco_lay(self, ct: Controller, st: _BuilderState, pos: Position) -> None:
        """Lay the stub back to the Core, one tile per two rounds.

        A builder cannot build on its own tile, so the chain is laid behind it:
        step toward the Core, then conveyor the tile just vacated, facing the
        tile now occupied.  Conveyors are bot-passable, so nothing it lays can
        box it in.
        """
        if self.home is None or st.chain_len > MAX_CHAIN:
            st.stage = "eco"
            return

        if st.trail_prev is not None:
            if ct.get_action_cooldown() != 0:
                return
            if self._build_link(ct, st.trail_prev, pos):
                st.chain_tiles.add((st.trail_prev.x, st.trail_prev.y))
            st.trail_prev = None
            return

        if adjacent_core_tile(pos, self.home) is not None:
            # This tile is the last link; step off it so it can be built.
            st.cap_tile = pos
            st.stage = "cap"
            self._step_off(ct, st, pos)
            return

        before = pos
        if self._step_toward(ct, st, pos, nearest_core_tile(pos, self.home)):
            # If the step went backwards onto a tile already conveyored, do NOT
            # lay behind us: a conveyor facing back into the one that feeds it
            # is a two-tile loop, and a chain with a loop in it delivers
            # exactly nothing.
            if (ct.get_position().x, ct.get_position().y) not in st.chain_tiles:
                st.trail_prev = before
                st.chain_len += 1
        elif st.stuck >= 4:
            st.stage = "eco"

    def _eco_cap(self, ct: Controller, st: _BuilderState, pos: Position) -> None:
        """Build the final conveyor, the one that actually faces the Core.  An
        unfinished chain delivers exactly nothing, so this step is the economy.
        """
        if self.home is None or st.cap_tile is None or st.stuck >= 6:
            st.stage = "eco"
            return
        if pos == st.cap_tile:
            self._step_off(ct, st, pos)
            return
        if abs(st.cap_tile.x - pos.x) + abs(st.cap_tile.y - pos.y) != 1:
            self._step_toward(ct, st, pos, st.cap_tile)
            return
        if ct.get_action_cooldown() != 0:
            return
        core_tile = adjacent_core_tile(st.cap_tile, self.home)
        if core_tile is None:
            st.stage = "eco"
            return
        if self._build_link(ct, st.cap_tile, core_tile) or st.stuck >= 4:
            st.stage = "eco"

    def _build_link(self, ct: Controller, tile: Position, toward: Position) -> bool:
        """One conveyor on tile, facing the neighbouring tile `toward`."""
        if not in_bounds(ct, tile):
            return False
        try:
            if ct.get_tile_building_id(tile) is not None:
                return True  # already linked; nothing owed
        except GameError:
            pass
        if ct.get_global_resources() < ct.get_conveyor_cost():
            return False
        facing = tile.cardinal_direction_to(toward)
        if facing == Direction.CENTRE:
            return False
        try:
            if not ct.can_build_conveyor(tile, facing):
                return False
            ct.build_conveyor(tile, facing)
        except GameError:
            return False
        return True

    def _step_off(self, ct: Controller, st: _BuilderState, pos: Position) -> None:
        """Vacate the current tile so a conveyor can be built on it -- backwards
        down the chain just laid, which is conveyor and therefore passable.
        """
        if ct.get_move_cooldown() != 0:
            return
        prefs = []
        if self.home is not None:
            core_tile = nearest_core_tile(pos, self.home)
            if core_tile.x > pos.x:
                prefs.append(Direction.WEST)
            elif core_tile.x < pos.x:
                prefs.append(Direction.EAST)
            if core_tile.y > pos.y:
                prefs.append(Direction.NORTH)
            elif core_tile.y < pos.y:
                prefs.append(Direction.SOUTH)
        for d in CARDINALS:
            if d not in prefs:
                prefs.append(d)
        for d in prefs:
            try:
                if ct.can_move(d):
                    ct.move(d)
                    return
            except GameError:
                continue

    def _explore_target(
        self, ct: Controller, st: _BuilderState, pos: Position
    ) -> Position:
        """No ore in memory: sweep outward from home in a fixed rosette."""
        anchor = self.home if self.home is not None else pos
        w, h = ct.get_map_width(), ct.get_map_height()
        ring = ((6, 0), (0, 6), (-6, 0), (0, -6), (5, 5), (-5, 5), (5, -5), (-5, -5))
        if st.stuck >= 3:
            st.explore_idx += 1
        dx, dy = ring[(st.explore_idx + (st.role or 0)) % len(ring)]
        return Position(
            min(max(anchor.x + dx, 0), w - 1),
            min(max(anchor.y + dy, 0), h - 1),
        )

    # ------------------------------------------------------------------
    # movement -- cardinal only, deterministic preference order
    # ------------------------------------------------------------------

    def _step_toward(
        self, ct: Controller, st: _BuilderState, pos: Position, dst
    ) -> bool:
        """One cardinal step toward dst; if the preferred axis is blocked, try
        the other one, then the perpendiculars, then backwards.

        Builder bots may only move in the 4 cardinal directions, so diagonals
        are never offered.  Ties never coin-flip: the preference list is built
        in a fixed order and the tabu list splits it into fresh-then-stale.
        """
        if dst is None:
            return False
        if ct.get_move_cooldown() != 0:
            return False
        dx = dst.x - pos.x
        dy = dst.y - pos.y
        if dx == 0 and dy == 0:
            return False

        horiz = Direction.EAST if dx > 0 else Direction.WEST
        vert = Direction.SOUTH if dy > 0 else Direction.NORTH
        prefs = []
        # When stuck, lead with the minor axis instead -- that is what gets a
        # bot around a wall corner rather than grinding into it.
        major_first = abs(dx) >= abs(dy)
        if st.stuck >= 2:
            major_first = not major_first
        if major_first:
            if dx:
                prefs.append(horiz)
            if dy:
                prefs.append(vert)
        else:
            if dy:
                prefs.append(vert)
            if dx:
                prefs.append(horiz)
        for d in CARDINALS:
            if d not in prefs:
                prefs.append(d)

        fresh = []
        stale = []
        for d in prefs:
            try:
                if not ct.can_move(d):
                    continue
            except GameError:
                continue
            dest = pos.add(d)
            if (dest.x, dest.y) in st.recent:
                stale.append(d)
            else:
                fresh.append(d)
        for d in fresh + stale:
            try:
                ct.move(d)
                return True
            except GameError:
                continue
        return False

    # ==================================================================
    # GUNNER -- fire down the ray, and NEVER rotate
    # ==================================================================

    def _run_gunner(self, ct: Controller) -> None:
        """The enemy Core if it is on the ray, otherwise whatever is.

        The family never rotates (0-3 rotations per game across six decoded
        games, and the plant policy is why: a fresh gunner adds DPS, a rotation
        only redirects).  So there is no rotate branch in this file at all --
        a gunner with nothing on its line simply holds.

        get_attackable_tiles() enumerates row-major in absolute map coordinates,
        so a "first occupied tile wins" scan would engage the farthest enemy for
        N/NE/NW/W facings and the nearest for the other four.  Targets are
        picked by distance_squared instead, never by enumeration order.
        """
        my_team = ct.get_team()
        pos = ct.get_position()
        best_core = None
        best_any = None

        try:
            tiles = ct.get_attackable_tiles()
        except GameError:
            return
        for tile in tiles:
            if not in_bounds(ct, tile):
                continue
            try:
                tid = ct.get_tile_building_id(tile)
                if tid is None:
                    tid = ct.get_tile_builder_bot_id(tile)
                if tid is None:
                    continue
                if ct.get_team(tid) == my_team:
                    continue
                is_core = ct.get_entity_type(tid) == EntityType.CORE
            except GameError:
                continue
            key = (pos.distance_squared(tile), tile.x, tile.y)
            if is_core and (best_core is None or key < best_core[0]):
                best_core = (key, tile)
            if best_any is None or key < best_any[0]:
                best_any = (key, tile)

        choice = best_core or best_any
        if choice is None:
            return
        try:
            if ct.can_fire(choice[1]):
                ct.fire(choice[1])
        except GameError:
            return
