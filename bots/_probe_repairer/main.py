"""PROBE REPAIRER — the BELT-REPAIR-AT-FIELD-RATE fixture (library item #2).

Spec: docs/research/SPEC-behaviour-fixture-library-2026-08-14.md section 3.
Reason it exists: the field REPAIRS cut conveyors and v125 does not, so every
salt-class / belt-cut plank we screen against ourselves is screened against an
opponent that never undoes the cut. This bot is the missing opponent: a plain
harvester+belt economy that notices its own severed belt tiles and puts them
back, at roughly the measured field rate and latency.

⛔ FIXTURE, NOT AN ARM. Per FIXTURE_OF_RECORD it proves MECHANISM only; a
currency read is a live pinned leg. Pool screens carry the stated-bias caveat.

CONSTANTS AND THEIR SOURCES (library rule 4 — a constant without a source line
is the s36 interpolation defect):
  * REPAIR_DELAY_ROUNDS / REPAIR_DUTY_* / the ~40.5% target rate — SOURCE: the
    salt docstring bots/_v197mapcode/doctrine.py:1554, verbatim: "Measured 2026-08-12: the
    field REPAIRS 40.5% of cut conveyors at a median latency of 4 rounds".
    Same number restated at bots/_v197mapcode/raid.py:433 and
    docs/builder-arm-retro.md:591 (field 40.5%, median latency 4 rounds;
    ours 6.8%, our own opponents 50.3%).
  * REPAIR_SCAN_DSQ = 20 — SOURCE: GameConstants builder-bot vision radius²
    (project CLAUDE.md entity table: builder bot vision r²=20). It is the
    radius a real builder can actually SEE a hole in, not a tuned number.

HOW THE RATE IS HELD DOWN TO FIELD LEVEL (i.e. deliberately NOT 100%). All
four limiters were needed; measured effect of each is recorded beside its
constant:
  * VISION — a hole is only ever noticed inside REPAIR_SCAN_DSQ. (Not the
    binding limiter in practice: detection measured 100%, holes_unique == cuts
    in 6/6 debug games, because the belt is compact and builders idle on it.)
  * DUTY SHARE — only 1 builder in 5 (REPAIR_DUTY_MOD/ACCEPT) drops its job for
    a hole. Every-builder duty measured 95.9% repaired (n=97 cuts).
  * PER-UNIT BUDGET — REPAIR_MAX_PER_UNIT tiles per builder, for life. One
    repairer on a compact belt otherwise services every cut on it: duty-alone
    measured 65.0% (1-in-5) and 79.4% (2-in-5).
  * NOTICE DELAY — REPAIR_DELAY_ROUNDS before acting, plus walk time.
There is NO repair patrol. Research's build_agg field cut is the eventual
authority on the 40.5%/median-4 target; if that cut moves, recalibrate
REPAIR_DUTY_* / REPAIR_MAX_PER_UNIT, not the header.

MEASURED AT VALIDITY (local `fcode run`, --tle 10, 2026-08-14T06:01Z, maps
antler/hive/saga/meander/eider/midgard x seeds 11/12/13, cuts read as team-0
conveyor DEATH rows off tools/corpus/replay_events.py — ENGINE events, not our
own stdout; the REPAIR45 tag supplies only the rebuild round and tile):
  * vs bots/_v190saltcutonly (BARE CUTS — the calibration fixture), 18 games:
    79 eligible cuts, 34 repaired = 43.0%, median latency 4 rounds (mean 4.79).
    Field target 40.5% at median 4. THIS IS THE CALIBRATION OF RECORD.
  * vs bots/_v197mapcode (SALT = cut + barrier), 6 games seed 11: 3 eligible
    cuts, 0 repairs = 0%. NOT a fixture defect: 6/6 cuts by that arm were
    followed by an enemy BARRIER on the same tile within 1-2 rounds (r34->36,
    r46->47, r45->46, r79->80, r84->85, r67->68), i.e. inside the notice delay,
    so the tile never reads as empty. The salt half denies the repair by
    construction — which is what salt is for — and this fixture reproduces that
    asymmetry rather than papering over it. Exposure is also thin against that
    arm: it kills this fixture at r53-91, so most cuts land in the death rush.
  * POSITIVE CONTROL (REPAIRER_SELFTEST, self-inflicted cuts at known rounds):
    tags fire, 3/10 self-cuts repaired at median latency 4 under the derated
    config; at full duty and no budget the same control read 42/47 = 89.4%,
    which is how the derating knobs were shown to be load-bearing.
  * FLAG-OFF CONTROL (REPAIRER_LOG=False), 2 games: 0 REPAIR45 tags, both games
    completed clean, 0 tracebacks, economy unchanged (24-29 conveyors built,
    6-11 cuts taken).
  * NOTE ON REPRODUCIBILITY: local `fcode run` is NOT deterministic at a fixed
    map+seed (same command, 3 runs, ended r81/r62/r79 with --tle 10 and also
    varied at --tle 0). Single-game reads off this fixture are noise; pool.

⛔ DIRECTION OF LIE (library rule 1), stated after measuring:
  * RATE: OVERSTATES the field slightly on bare cuts (43.0% vs 40.5%, n=79,
    binomial SE ~5.6pp — i.e. statistically indistinguishable, but the point
    estimate sits high). A cut is undone slightly more often here than in the
    field, so a salt-class plank screened here looks slightly WORSE than it
    will live: FALSE NEGATIVES, the safe direction for ship decisions, and the
    direction the spec predicted for a dedicated repairer.
  * LATENCY: median honest (4 vs field 4) but the TAIL IS THIN — this bot
    repairs within ~10 rounds or never, because the repairer is a builder
    already standing on the line. A real team's slow repairs (a builder
    recalled from far away) are missing, so anything keyed to a 15+ round
    window of a dead belt will read too favourably here.
  * SALT CLEARING: this fixture NEVER clears a barrier off a salted tile (it
    reads any building as "the belt is fine"). Real teams pay 15 pecks and some
    do. That OVERSTATES salt's stickiness — the unsafe direction — so a
    salt-with-barrier plank must not take its win against this fixture at face
    value. The bare-cut arm is the honest screen for the cut half.
  * ECONOMY: naive greedy L-path wiring, no splitters, no redundancy, so one
    cut severs a whole line — cuts are worth MORE here than against real wiring.
    It builds no turrets and never attacks, dies to any aggressive bot by
    r55-115; it is a belt-BEHAVIOUR fixture, not an opponent-strength fixture.
"""
import sys

from fcode import Controller, Direction, EntityType, Environment, Position

CARDINALS = (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST)

# Spec said "~4 builders"; 6 measured, because at 4 the fixture laid only
# 4-11 conveyor tiles per game and there was nothing for a cut to land on
# (13-39 tiles at 6). The habit under test needs a belt to exist.
MAX_BUILDERS = 6
MAX_LINES_PER_BUILDER = 2  # then it stops; abandoned lines rot (rate limiter)
MAX_PATH = 40              # cap on a belt path length, CPU guard

# SOURCE: bots/_v197mapcode/doctrine.py:1554 — field repairs 40.5% of cut
# conveyors at a MEDIAN LATENCY OF 4 ROUNDS. Split into a notice delay plus
# whatever travel costs; calibrated at validity to a measured median of 4.
REPAIR_DELAY_ROUNDS = 3
# SOURCE: builder-bot vision r²=20 (CLAUDE.md entity table). Holes outside a
# builder's own vision are never noticed. Measured NOT to be the binding
# limiter here (detection came out 100% of cuts) — kept because it is the
# physically true constraint, not because it does the derating.
REPAIR_SCAN_DSQ = 20

REPAIRER_LOG = True        # gates the REPAIR45 dose tag (both-verdict flag)

# DERATING KNOB — how many builders carry repair duty at all. Every builder
# SEES the hole (detection is 100%, measured); only a duty builder drops what
# it is doing for it. With every builder on duty the fixture repaired 95.9% of
# bare cuts (18 games vs _v190saltcutonly) against a field 40.5%, i.e. it was a
# perfect repairer and not a field-shaped one. Duty share is the honest knob:
# a real team has some builders committed elsewhere. CALIBRATED at validity —
# see the header for the achieved rate. SOURCE of the 40.5% target: the salt
# docstring, bots/_v197mapcode/doctrine.py:1554.
REPAIR_DUTY_MOD = 5
REPAIR_DUTY_ACCEPT = 1     # builder is a repairer iff get_id() % MOD < ACCEPT
# Second derating knob: a builder that has already put back this many tiles
# goes back to its own job for good. Duty share alone did not derate enough
# (65.0% at 1-in-5 duty, 79.4% at 2-in-5, both vs a field 40.5%) because one
# repairer standing on a compact belt can service every cut on it.
REPAIR_MAX_PER_UNIT = 2

# POSITIVE CONTROL, off in the shipped fixture. With this True a builder
# destroys one of its own adjacent belt tiles every SELFTEST_PERIOD rounds and
# prints SELFCUT — the only way to drive the repair path from a KNOWN cut round
# without editing another bot. Standing practice: an alarm that has never fired
# has not been seen to work. Rates measured under it are NOT field rates (the
# cut lands under a builder's feet by construction).
REPAIRER_SELFTEST = False
SELFTEST_PERIOD = 25

REPAIRER_DEBUG = False      # stderr HOLE/NOBUILD trace (dev only)
BELT_MEMORY_MAX = 80       # cap on remembered belt tiles (CPU guard)

# Ore acceptance: own half by the reflected-core rule, OR within this of our
# own core (some maps put every ore tile on or past the mid-line, and a fixture
# with no economy exhibits no belt habit at all). 12 tiles, i.e. inside the
# core's own working area — no measured field source, it is a fixture-shape
# guard and is named as such.
NEAR_CORE_DSQ = 144


class Player:
    spawned = 0

    def run(self, ct: Controller) -> None:
        try:
            kind = ct.get_entity_type()
            if kind == EntityType.CORE:
                self._core_turn(ct)
            elif kind == EntityType.BUILDER_BOT:
                self._builder_turn(ct)
        except Exception:
            import traceback
            traceback.print_exc(file=sys.stderr)

    # ------------------------------------------------------------- core
    def _core_turn(self, ct: Controller) -> None:
        if ct.get_action_cooldown() != 0:
            return
        if Player.spawned >= MAX_BUILDERS:
            return
        # Keep a float so builders can afford belt/harvester work.
        if ct.get_global_resources() < ct.get_builder_bot_cost() + 40:
            return
        p = ct.get_position()
        for d in Direction:
            if d == Direction.CENTRE:
                continue
            t = p.add(d)
            try:
                if ct.can_spawn(t):
                    ct.spawn_builder(t)
                    Player.spawned += 1
                    return
            except Exception:
                continue

    # ---------------------------------------------------------- builder
    def _own_core(self, ct, me):
        """Own-core discovery: a builder spawns adjacent to it, so turn 1 sees
        it. Class attributes do NOT share across units in this sandbox (each
        unit runs its own Player), so every builder discovers it itself."""
        if getattr(self, "_core", None) is not None:
            return self._core
        for bid in ct.get_nearby_buildings():
            try:
                if (ct.get_team(bid) == me
                        and ct.get_entity_type(bid) == EntityType.CORE):
                    self._core = ct.get_position(bid)
                    return self._core
            except Exception:
                continue
        return None

    def _register_belts(self, ct, me):
        """Adopt every friendly conveyor I can currently SEE into belt memory.

        Without this a builder only knows the belt it laid itself, so a cut on
        a line whose author has died or walked away is repaired by nobody and
        the fixture's rate collapses to ~0. A real team's builders repair the
        TEAM's belt; per-unit memory is only how it is implemented here (no
        shared state in the sandbox), not a behaviour claim."""
        if len(self._belt) >= BELT_MEMORY_MAX:
            return
        try:
            ids = ct.get_nearby_buildings()
        except Exception:
            return
        for bid in ids:
            try:
                if ct.get_entity_type(bid) != EntityType.CONVEYOR:
                    continue
                if ct.get_team(bid) != me:
                    continue
                pos = ct.get_position(bid)
                key = (pos.x, pos.y)
                if key in self._known:
                    continue
                self._known[key] = True
                self._belt.append((pos, ct.get_direction(bid)))
                self._built.add(key)
                if len(self._belt) >= BELT_MEMORY_MAX:
                    return
            except Exception:
                continue

    def _selftest_cut(self, ct, p: Position, me) -> bool:
        """Positive control: sever one of my own belt tiles on a fixed clock."""
        r = ct.get_current_round()
        if r < 20 or r % SELFTEST_PERIOD != 0:
            return False
        for d in CARDINALS:
            t = p.add(d)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) != me:
                    continue
                if ct.get_entity_type(bid) != EntityType.CONVEYOR:
                    continue
                if ct.can_destroy(t):
                    ct.destroy(t)
                    print(f"SELFCUT r={r} tile={t.x},{t.y}")
                    return True
            except Exception:
                continue
        return False

    def _path_to_core(self, ct, start: Position, core: Position):
        """Greedy cardinal L-path from `start` to a tile orthogonally adjacent
        to the core tile. Returns the belt tiles (excluding `start`), each of
        which will face the NEXT tile in the list (last one faces the core)."""
        tiles = []
        cur = start
        seen = {(start.x, start.y)}
        for _ in range(MAX_PATH):
            if abs(cur.x - core.x) + abs(cur.y - core.y) <= 1:
                break
            step = None
            dx, dy = core.x - cur.x, core.y - cur.y
            order = []
            if abs(dx) >= abs(dy):
                order = [Direction.EAST if dx > 0 else Direction.WEST,
                         Direction.SOUTH if dy > 0 else Direction.NORTH]
            else:
                order = [Direction.SOUTH if dy > 0 else Direction.NORTH,
                         Direction.EAST if dx > 0 else Direction.WEST]
            for d in order:
                nxt = cur.add(d)
                if (nxt.x, nxt.y) in seen:
                    continue
                if not (0 <= nxt.x < ct.get_map_width()
                        and 0 <= nxt.y < ct.get_map_height()):
                    continue
                try:
                    if ct.get_tile_env(nxt) == Environment.WALL:
                        continue
                except Exception:
                    continue
                step = nxt
                break
            if step is None:
                break
            tiles.append(step)
            seen.add((step.x, step.y))
            cur = step
        # each tile faces the next; the last faces the core
        out = []
        for i, t in enumerate(tiles):
            nxt = tiles[i + 1] if i + 1 < len(tiles) else core
            out.append((t, t.direction_to(nxt)))
        return out

    def _nearest_ore(self, ct, p: Position, core: Position):
        """Nearest unclaimed ore IN OUR OWN HALF. The half test is the
        reflected-core rule (no magic radius): ore is ours if it is closer to
        our core than to the reflected enemy core. Without it a builder walks
        20+ tiles to contested ore, abandons its near-core belt, and the
        fixture stops exhibiting the habit it exists for."""
        best, best_d = None, 10 ** 9
        mirror = Position(ct.get_map_width() - 1 - core.x,
                          ct.get_map_height() - 1 - core.y)
        try:
            tiles = ct.get_nearby_tiles()
        except Exception:
            return None
        for t in tiles:
            if (t.distance_squared(core) >= t.distance_squared(mirror)
                    and t.distance_squared(core) > NEAR_CORE_DSQ):
                continue
            try:
                if ct.get_tile_env(t) != Environment.ORE_TITANIUM:
                    continue
                if ct.get_tile_building_id(t) is not None:
                    continue
            except Exception:
                continue
            d = p.distance_squared(t)
            if d < best_d:
                best, best_d = t, d
        return best

    def _step_off(self, ct, p: Position) -> bool:
        """Standing ON a tile my own belt needs is a deadlock (a builder may
        not build under itself), so vacate to a tile the belt does not want."""
        want = {(t.x, t.y) for t, _ in getattr(self, "_belt", [])}
        for d in CARDINALS:
            t = p.add(d)
            if (t.x, t.y) in want:
                continue
            try:
                if ct.can_move(d):
                    ct.move(d)
                    return True
            except Exception:
                continue
        for d in CARDINALS:                 # boxed in: any move beats none
            try:
                if ct.can_move(d):
                    ct.move(d)
                    return True
            except Exception:
                continue
        return False

    def _step_toward(self, ct, p: Position, target: Position) -> bool:
        if ct.get_move_cooldown() != 0:
            return False
        if p.x == target.x and p.y == target.y:
            return self._step_off(ct, p)
        if p.distance_squared(target) <= 1:
            return False                    # already orthogonally adjacent
        d = p.cardinal_direction_to(target)
        try:
            if d != Direction.CENTRE and ct.can_move(d):
                ct.move(d)
                self._stuck = 0
                return True
        except Exception:
            pass
        cur = p.distance_squared(target)
        for d2 in CARDINALS:
            try:
                if ct.can_move(d2) and p.add(d2).distance_squared(target) < cur:
                    ct.move(d2)
                    self._stuck = 0
                    return True
            except Exception:
                continue
        self._stuck = getattr(self, "_stuck", 0) + 1
        if self._stuck >= 3:
            off = (ct.get_id() + self._stuck) % 4
            for k in range(4):
                try:
                    if ct.can_move(CARDINALS[(off + k) % 4]):
                        ct.move(CARDINALS[(off + k) % 4])
                        return True
                except Exception:
                    continue
        return False

    def _builder_turn(self, ct: Controller) -> None:
        me = ct.get_team()
        p = ct.get_position()
        core = self._own_core(ct, me)
        if core is None:
            self._step_toward(ct, p, Position(ct.get_map_width() // 2,
                                              ct.get_map_height() // 2))
            return
        belt = getattr(self, "_belt", None)
        if belt is None:
            belt = self._belt = []          # [(Position, Direction)] I laid
            self._lines = 0
            self._holes = {}                # (x,y) -> round first seen empty
            self._built = set()             # tiles OBSERVED to carry a belt
            self._known = {}                # (x,y) -> in belt memory already
            self._repairs = 0               # this unit's spent repair budget
        self._register_belts(ct, me)
        if REPAIRER_SELFTEST and self._selftest_cut(ct, p, me):
            pass                            # destroy is free; keep acting

        # ---- 1. THE HABIT: repair a remembered belt tile that is now empty.
        # Only tiles inside my own vision are ever noticed; there is no patrol.
        # The OBSERVATION pass runs every turn (a builder sees the hole whether
        # or not it can act on it); only the rebuild is cooldown-gated.
        r = ct.get_current_round()
        target_hole = None
        pending = None
        on_duty = (ct.get_id() % REPAIR_DUTY_MOD) < REPAIR_DUTY_ACCEPT
        for pos, facing in belt:
            if p.distance_squared(pos) > REPAIR_SCAN_DSQ:
                continue
            try:
                if ct.get_tile_building_id(pos) is not None:
                    self._built.add((pos.x, pos.y))
                    self._holes.pop((pos.x, pos.y), None)
                    continue
            except Exception:
                continue
            # a tile that never carried a belt is UNBUILT, not CUT — it
            # belongs to the laying branch below, and counting it as a
            # repair would inflate the dose with construction.
            if (pos.x, pos.y) not in self._built:
                continue
            seen = self._holes.get((pos.x, pos.y))
            if seen is None:
                self._holes[(pos.x, pos.y)] = r
                if REPAIRER_DEBUG:
                    print(f"HOLE r={r} tile={pos.x},{pos.y} "
                          f"d2={p.distance_squared(pos)}", file=sys.stderr)
                continue
            if not on_duty or self._repairs >= REPAIR_MAX_PER_UNIT:
                continue
            if r - seen < REPAIR_DELAY_ROUNDS:
                # CLAIMED but not yet due. A builder that notices a hole and
                # then walks off to its next ore job never comes back (measured:
                # holes were seen and never repaired), so it holds station by
                # the hole until the delay elapses. This is what makes the
                # latency a LATENCY rather than a silent drop.
                if pending is None:
                    pending = (pos, facing, seen)
                continue
            if target_hole is None:
                target_hole = (pos, facing, seen)
        if target_hole is not None:
            pos, facing, seen = target_hole
            if ct.get_action_cooldown() == 0:
                try:
                    if ct.can_build_conveyor(pos, facing):
                        ct.build_conveyor(pos, facing)
                        self._holes.pop((pos.x, pos.y), None)
                        self._repairs += 1
                        if REPAIRER_LOG:
                            print(f"REPAIR45 r={r} tile={pos.x},{pos.y} "
                                  f"seen={seen} lat={r - seen}")
                        return
                    elif REPAIRER_DEBUG:
                        print(f"NOBUILD r={r} tile={pos.x},{pos.y} "
                              f"d2={p.distance_squared(pos)} "
                              f"bank={ct.get_global_resources()}", file=sys.stderr)
                except Exception:
                    pass
            # not adjacent yet: walk to it (this is where latency accrues).
            # NB > 1, not > 2: building needs ORTHOGONAL adjacency (d²==1), so
            # a builder sitting diagonally (d²==2) must still take a step.
            if p.distance_squared(pos) > 1:
                if self._step_toward(ct, p, pos):
                    return
                return                      # hold station rather than wander
        elif pending is not None:
            pos = pending[0]
            if p.distance_squared(pos) > 1:
                self._step_toward(ct, p, pos)
            return                          # wait out the notice delay here

        # ---- 2. Lay the current line: build the nearest missing belt tile.
        if ct.get_action_cooldown() == 0 and belt:
            for pos, facing in belt:
                if (pos.x, pos.y) in self._built:
                    continue    # a CUT tile: branch 1 owns it, at field latency
                try:
                    if ct.get_tile_building_id(pos) is not None:
                        continue
                    if ct.can_build_conveyor(pos, facing):
                        ct.build_conveyor(pos, facing)
                        return
                except Exception:
                    continue
            # walk to the first missing tile of the line
            for pos, facing in belt:
                if (pos.x, pos.y) in self._built:
                    continue
                try:
                    if ct.get_tile_building_id(pos) is None:
                        if self._step_toward(ct, p, pos):
                            return
                        break
                except Exception:
                    continue

        # ---- 3. No pending belt work: start a new harvester line.
        if self._lines < MAX_LINES_PER_BUILDER:
            ore = self._nearest_ore(ct, p, core)
            if ore is not None:
                if ct.get_action_cooldown() == 0:
                    try:
                        if ct.can_build_harvester(ore):
                            ct.build_harvester(ore)
                            for pair in self._path_to_core(ct, ore, core):
                                key = (pair[0].x, pair[0].y)
                                if key in self._known:
                                    continue
                                self._known[key] = True
                                self._belt.append(pair)
                            self._lines += 1
                            return
                    except Exception:
                        pass
                if self._step_toward(ct, p, ore):
                    return
            else:
                # No ore in sight: sweep our OWN quarter, not the enemy half.
                mirror = Position(ct.get_map_width() - 1 - core.x,
                                  ct.get_map_height() - 1 - core.y)
                k = ct.get_id() % 8
                # spiral outward as the game goes on: a fixed 6-tile probe
                # leaves builders idle on maps whose ore is 10+ tiles out
                span = 4 + min(16, ct.get_current_round() // 6)
                unit = ((1, 0), (1, 1), (0, 1), (-1, 1),
                        (-1, 0), (-1, -1), (0, -1), (1, -1))[k]
                tx = min(max(core.x + unit[0] * span, 0),
                         ct.get_map_width() - 1)
                ty = min(max(core.y + unit[1] * span, 0),
                         ct.get_map_height() - 1)
                probe = Position(tx, ty)
                while (probe.distance_squared(core)
                       >= probe.distance_squared(mirror) and span > 1):
                    span -= 2
                    tx = min(max(core.x + unit[0] * span, 0),
                             ct.get_map_width() - 1)
                    ty = min(max(core.y + unit[1] * span, 0),
                             ct.get_map_height() - 1)
                    probe = Position(tx, ty)
                if self._step_toward(ct, p, probe):
                    return

        # ---- 4. Idle beside my belt so I stay in repair range of it.
        if belt:
            anchor = belt[len(belt) // 2][0]
            if p.distance_squared(anchor) > REPAIR_SCAN_DSQ:
                self._step_toward(ct, p, anchor)
