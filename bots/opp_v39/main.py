"""v42 — v40 eco + narrow melee home defense.

v41 over-defended (expanders abandoned eco → 86/120). Restore link-first single
launcher; only saboteur/launchwait peel for enemy builders within Core range.
"""
import math
import random
from collections import deque

from fcode import Direction, EntityType, Environment, Position

DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]
CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

MAX_BUILDERS = 8
EARLY_BUILDERS = 4
ECO_CAP = 7
ECO_NEED = 3

SLOT_ROLE_N = 0
SLOT_UNDER = 1
SLOT_ATK_RND = 2
SLOT_ENEMY_CORE = 3
SLOT_HARVESTERS = 4
SLOT_ECO_READY = 5
SLOT_LAUNCHER = 6
SLOT_HOME_GUN = 7
SLOT_DROPPED = 8
SLOT_LINKS_DONE = 9

AMMO_FLOOR = 20
LAUNCHER_RESERVE = 80


def pack_pos(pos):
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val):
    if not val:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def nearest_cardinal(d):
    return {
        Direction.NORTH: Direction.NORTH, Direction.NORTHEAST: Direction.EAST,
        Direction.EAST: Direction.EAST, Direction.SOUTHEAST: Direction.EAST,
        Direction.SOUTH: Direction.SOUTH, Direction.SOUTHWEST: Direction.SOUTH,
        Direction.WEST: Direction.WEST, Direction.NORTHWEST: Direction.WEST,
        Direction.CENTRE: Direction.NORTH,
    }[d]


def ring(origin, r=2):
    out = []
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            if dx or dy:
                out.append(Position(origin.x + dx, origin.y + dy))
    return out


def core_tiles(o):
    return [o, Position(o.x + 1, o.y), Position(o.x, o.y + 1), Position(o.x + 1, o.y + 1)]


def dist_core(pos, o):
    return min(max(abs(pos.x - c.x), abs(pos.y - c.y)) for c in core_tiles(o))


def nearest_core_tile(pos, o):
    return min(core_tiles(o), key=lambda c: max(abs(pos.x - c.x), abs(pos.y - c.y)))


class Player:
    def __init__(self):
        self.n = 0
        self.team = None
        self.core = None
        self.enemy = None
        self.mw = self.mh = 0
        self.role = "expand"
        self.tgt = None
        self.last = None
        self.stuck = 0
        self.wall = None
        self.ang = 0.0
        self.idx = 0
        self.link_queue = []
        self.dropped = False

    def run(self, ct):
        e = ct.get_entity_type()
        if e == EntityType.CORE:
            self._core(ct)
        elif e == EntityType.BUILDER_BOT:
            self._builder(ct)
        elif e in (EntityType.GUNNER, EntityType.SENTINEL):
            self._turret(ct)
        elif e == EntityType.LAUNCHER:
            self._launcher(ct)

    def _core(self, ct):
        p = ct.get_position()
        w, h = ct.get_map_width(), ct.get_map_height()
        if ct.read_store(SLOT_ENEMY_CORE) == 0:
            ct.write_store(SLOT_ENEMY_CORE, pack_pos(Position(max(0, w - 2 - p.x), max(0, h - 2 - p.y))))

        under = False
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == ct.get_team():
                continue
            d = p.distance_squared(ct.get_position(eid))
            et = ct.get_entity_type(eid)
            if et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= 64:
                under = True
                break
            if et == EntityType.BUILDER_BOT and d <= 16:
                under = True
                break
        rnd = ct.get_current_round()
        if under:
            ct.write_store(SLOT_UNDER, 1)
            ct.write_store(SLOT_ATK_RND, rnd)
        else:
            last = ct.read_store(SLOT_ATK_RND)
            under = bool(last and rnd - last < 35)
            ct.write_store(SLOT_UNDER, 1 if under else 0)

        harv = ct.read_store(SLOT_HARVESTERS)
        has_launch = ct.read_store(SLOT_LAUNCHER) != 0
        if harv >= ECO_NEED:
            ct.write_store(SLOT_ECO_READY, 1)

        ti, ammo = ct.get_global_resources(), ct.get_global_ammo()
        launch_cost = ct.get_launcher_cost()

        spawn_cap = MAX_BUILDERS
        if not has_launch and harv < 1:
            spawn_cap = EARLY_BUILDERS
        elif not has_launch and harv < ECO_NEED and rnd < 25 and ti < launch_cost + 60:
            spawn_cap = EARLY_BUILDERS + 1

        reserve = 0 if has_launch else max(LAUNCHER_RESERVE, launch_cost)
        can_spend_spawn = ti >= ct.get_builder_bot_cost() + (0 if has_launch else min(40, reserve // 3))

        if self.n < spawn_cap and can_spend_spawn and ti >= ct.get_builder_bot_cost():
            cands = ring(p, 2)
            random.shuffle(cands)
            for sp in cands:
                if 0 <= sp.x < w and 0 <= sp.y < h and ct.can_spawn(sp):
                    ct.spawn_builder(sp)
                    self.n += 1
                    return

        if has_launch and harv >= 2 and ammo < AMMO_FLOOR and ti > 60:
            amt = min(8, AMMO_FLOOR - ammo, ti - 50)
            if amt >= 4 and ct.can_convert_ammo(amt):
                ct.convert_ammo(amt)
                return

        if under and harv >= 1 and ti >= ct.get_sentinel_cost():
            for bp in ring(p, 2):
                if not (0 <= bp.x < w and 0 <= bp.y < h):
                    continue
                ec = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
                facing = bp.direction_to(ec) if ec else Direction.NORTH
                if facing == Direction.CENTRE:
                    facing = Direction.NORTH
                if ct.can_build_sentinel(bp, facing):
                    ct.build_sentinel(bp, facing)
                    return

        if under and has_launch and harv >= 1 and ammo >= 4 and ct.read_store(SLOT_HOME_GUN) < 5 and ti >= ct.get_gunner_cost():
            ec = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
            for bp in ring(p, 2):
                if not (0 <= bp.x < w and 0 <= bp.y < h):
                    continue
                facing = bp.direction_to(ec) if ec else Direction.NORTH
                if facing == Direction.CENTRE:
                    facing = Direction.NORTH
                if ct.can_build_gunner(bp, facing):
                    ct.build_gunner(bp, facing)
                    ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
                    return

    def _note_friendly_launcher(self, ct):
        if ct.read_store(SLOT_LAUNCHER):
            return
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.LAUNCHER:
                ct.write_store(SLOT_LAUNCHER, 1)
                return

    def _sync_harvesters(self, ct):
        if self.core is None:
            return
        p = ct.get_position()
        if p.distance_squared(self.core) > 64:
            return
        live = 0
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.HARVESTER:
                live += 1
        if live != ct.read_store(SLOT_HARVESTERS):
            ct.write_store(SLOT_HARVESTERS, live)
        if live >= ECO_NEED:
            ct.write_store(SLOT_ECO_READY, 1)

    def _try_build_launcher(self, ct):
        """Only call from defend — claim store first to prevent multi-launcher."""
        if ct.read_store(SLOT_LAUNCHER):
            return False
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.LAUNCHER:
                ct.write_store(SLOT_LAUNCHER, 1)
                return False
        if ct.read_store(SLOT_HARVESTERS) < 1:
            return False
        if ct.get_global_resources() < ct.get_launcher_cost():
            return False
        # Claim BEFORE build so later units this round skip
        ct.write_store(SLOT_LAUNCHER, 1)
        p = ct.get_position()
        for d in DIRECTIONS:
            bp = p.add(d)
            if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_launcher(bp):
                ct.build_launcher(bp)
                return True
        # Build failed — release claim so we retry next turn
        ct.write_store(SLOT_LAUNCHER, 0)
        return False

    def _builder(self, ct):
        p = ct.get_position()
        if self.team is None:
            self.team = ct.get_team()
            self.mw, self.mh = ct.get_map_width(), ct.get_map_height()
            self.idx = ct.get_id() & 0xFF
            self.ang = (self.idx % 8) * (math.pi / 4)
            n = ct.read_store(SLOT_ROLE_N)
            small = self.mw * self.mh <= 220
            if n == 0:
                self.role = "defend"
            elif small:
                self.role = "expand" if n <= 2 else "saboteur"
            elif n <= 4:
                self.role = "expand"
            else:
                self.role = "launchwait"
            ct.write_store(SLOT_ROLE_N, n + 1)

        if self.core is None:
            for eid in ct.get_nearby_buildings():
                if ct.get_entity_type(eid) == EntityType.CORE and ct.get_team(eid) == self.team:
                    self.core = ct.get_position(eid)
                    break
        if self.core is None:
            return

        self._note_friendly_launcher(ct)

        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            et = ct.get_entity_type(eid)
            ep = ct.get_position(eid)
            if et == EntityType.CORE:
                self.enemy = ep
                ct.write_store(SLOT_ENEMY_CORE, pack_pos(ep))
            d = self.core.distance_squared(ep)
            if (et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= 64) or (
                et == EntityType.BUILDER_BOT and d <= 16
            ):
                ct.write_store(SLOT_UNDER, 1)
                ct.write_store(SLOT_ATK_RND, ct.get_current_round())

        self.enemy = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        self._sync_harvesters(ct)

        rnd = ct.get_current_round()
        if self.role == "expand" and not self.link_queue and (self.idx % 4) == 0:
            if ct.read_store(SLOT_LAUNCHER) and ct.read_store(SLOT_HARVESTERS) >= ECO_NEED + 1:
                self.role = "saboteur"
            elif ct.read_store(SLOT_HARVESTERS) >= ECO_CAP and rnd >= 120:
                self.role = "saboteur"

        if self.role == "launchwait":
            if self.dropped:
                self.role = "saboteur"
            elif rnd >= 70 and not ct.read_store(SLOT_LAUNCHER):
                self.role = "saboteur"
            elif rnd >= 140:
                self.role = "saboteur"

        if self.last == p:
            self.stuck += 1
        else:
            self.stuck = 0
            self.wall = None
        self.last = p

        if self.core and p.distance_squared(self.core) > 80:
            self.dropped = True
            self.role = "saboteur"

        # Narrow defense: only idle raiders near Core, and only vs melee bots this tick
        if self.role in ("saboteur", "launchwait") and self.core and p.distance_squared(self.core) <= 25:
            melee = False
            for eid in ct.get_nearby_entities():
                if ct.get_team(eid) == self.team:
                    continue
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                if self.core.distance_squared(ct.get_position(eid)) <= 20:
                    melee = True
                    break
            if melee:
                self._home_defend(ct)
                return

        if self.role == "defend":
            self._defend(ct)
        elif self.role == "saboteur":
            self._saboteur(ct)
        elif self.role == "launchwait":
            self._launchwait(ct)
        else:
            self._expand(ct)

    def _home_defend(self, ct):
        """All hands: melee attackers, plant sentinel/barrier, heal Core."""
        p = ct.get_position()
        if ct.get_action_cooldown() == 0:
            if p.distance_squared(self.core) <= 5 and ct.can_heal(self.core):
                ct.heal(self.core)
            elif self._sabotage_prio(ct):
                pass
            elif ct.get_global_resources() >= ct.get_sentinel_cost():
                for d in CARDINALS:
                    bp = p.add(d)
                    if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                        continue
                    facing = bp.direction_to(self.enemy) if self.enemy else Direction.NORTH
                    if facing == Direction.CENTRE:
                        facing = Direction.NORTH
                    if ct.can_build_sentinel(bp, facing):
                        ct.build_sentinel(bp, facing)
                        break
                else:
                    for d in DIRECTIONS:
                        bp = p.add(d)
                        if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_barrier(bp):
                            ct.build_barrier(bp)
                            break
        if ct.get_move_cooldown() != 0:
            return
        # Move onto enemy bots near Core
        threat = None
        best = 10**9
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            ep = ct.get_position(eid)
            if self.core.distance_squared(ep) > 36:
                continue
            d = p.distance_squared(ep)
            if d < best:
                best, threat = d, ep
        self.tgt = threat if threat is not None else self.core
        self._nav(ct, pave=False)

    def _sabotage_prio(self, ct):
        p = ct.get_position()
        for d in CARDINALS:
            t = p.add(d)
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            bid = ct.get_tile_building_id(t)
            if bid is None or ct.get_team(bid) == self.team:
                continue
            if ct.get_entity_type(bid) == EntityType.CORE and ct.can_fire(t):
                ct.fire(t)
                return True
        best, best_p = None, 99
        for d in CARDINALS:
            t = p.add(d)
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            bid = ct.get_tile_building_id(t)
            if bid is None or ct.get_team(bid) == self.team:
                continue
            et = ct.get_entity_type(bid)
            if et in (EntityType.GUNNER, EntityType.SENTINEL, EntityType.CORE):
                continue
            pr = {EntityType.HARVESTER: 0, EntityType.CONVEYOR: 1, EntityType.SPLITTER: 1,
                  EntityType.LAUNCHER: 2, EntityType.BARRIER: 3}.get(et, 4)
            if pr < best_p and ct.can_fire(t):
                best_p, best = pr, t
        if best is not None:
            ct.fire(best)
            return True
        return False

    def _launchwait(self, ct):
        p = ct.get_position()
        if ct.get_action_cooldown() == 0:
            if ct.read_store(SLOT_UNDER):
                self._sabotage_prio(ct)

        if ct.get_move_cooldown() != 0:
            return
        if p.distance_squared(self.core) > 12:
            self.tgt = self.core
        elif self.tgt is None or p == self.tgt or self.stuck >= 2:
            self.ang = (self.ang + 1.1) % (2 * math.pi)
            self.tgt = Position(
                max(0, min(self.core.x + int(2 * math.cos(self.ang)), self.mw - 1)),
                max(0, min(self.core.y + int(2 * math.sin(self.ang)), self.mh - 1)),
            )
        self._nav(ct, pave=False)

    def _saboteur(self, ct):
        p = ct.get_position()
        ec = self.enemy or Position(self.mw // 2, self.mh // 2)
        small = self.mw * self.mh <= 220
        rnd = ct.get_current_round()

        if ct.get_action_cooldown() == 0:
            if self._sabotage_prio(ct):
                pass
            elif (
                p.distance_squared(ec) <= 50
                and ct.get_global_ammo() >= 8
                and ct.get_global_resources() >= ct.get_gunner_cost()
            ):
                for d in DIRECTIONS:
                    bp = p.add(d)
                    if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                        continue
                    facing = bp.direction_to(ec)
                    if facing == Direction.CENTRE:
                        facing = Direction.NORTH
                    if ct.can_build_gunner(bp, facing):
                        ct.build_gunner(bp, facing)
                        break

        if ct.get_move_cooldown() != 0:
            return

        waiting = (
            not self.dropped
            and not small
            and ct.read_store(SLOT_LAUNCHER)
            and ct.read_store(SLOT_DROPPED) < 2
            and rnd < 55
            and p.distance_squared(self.core) <= 25
        )
        if waiting and p.distance_squared(self.core) > 10:
            self.tgt = self.core
        elif p.distance_squared(ec) <= 8 and self.stuck >= 2:
            self.ang = (self.ang + 1.2) % (2 * math.pi)
            self.tgt = Position(
                max(0, min(ec.x + int(2 * math.cos(self.ang)), self.mw - 1)),
                max(0, min(ec.y + int(2 * math.sin(self.ang)), self.mh - 1)),
            )
        else:
            self.tgt = ec
        self._nav(ct, pave=False)

    def _defend(self, ct):
        p = ct.get_position()
        under = ct.read_store(SLOT_UNDER) != 0
        harv = ct.read_store(SLOT_HARVESTERS)
        has_launch = ct.read_store(SLOT_LAUNCHER) != 0
        ti = ct.get_global_resources()

        if ct.get_action_cooldown() == 0:
            if p.distance_squared(self.core) <= 5 and ct.can_heal(self.core):
                ct.heal(self.core)
            elif harv < 1 and ti >= ct.get_harvester_cost():
                for d in DIRECTIONS:
                    bp = p.add(d)
                    if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_harvester(bp):
                        ct.build_harvester(bp)
                        ct.write_store(SLOT_HARVESTERS, 1)
                        if not self.link_queue:
                            self.link_queue = self._link_path(ct, bp)
                        break
            # Finish first link before launcher so we actually mine
            elif self.link_queue and not has_launch and ti >= ct.get_conveyor_cost():
                self._build_next_link(ct)
            elif not has_launch and harv >= 1 and self._try_build_launcher(ct):
                pass
            elif harv < ECO_CAP and ti >= ct.get_harvester_cost():
                for d in DIRECTIONS:
                    bp = p.add(d)
                    if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_harvester(bp):
                        ct.build_harvester(bp)
                        ct.write_store(SLOT_HARVESTERS, harv + 1)
                        if ct.read_store(SLOT_HARVESTERS) >= ECO_NEED:
                            ct.write_store(SLOT_ECO_READY, 1)
                        if not self.link_queue:
                            self.link_queue = self._link_path(ct, bp)
                        break
            elif under and ti >= ct.get_sentinel_cost():
                for d in CARDINALS:
                    bp = p.add(d)
                    if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                        continue
                    facing = bp.direction_to(self.enemy) if self.enemy else Direction.NORTH
                    if facing == Direction.CENTRE:
                        facing = Direction.NORTH
                    if ct.can_build_sentinel(bp, facing):
                        ct.build_sentinel(bp, facing)
                        break
            elif under:
                self._sabotage_prio(ct)

        if self.link_queue:
            if ct.get_action_cooldown() == 0 and self._build_next_link(ct):
                return
            if ct.get_move_cooldown() == 0:
                nxt = self.link_queue[0]
                self.tgt = nearest_core_tile(p, self.core) if (p.x == nxt.x and p.y == nxt.y) else nxt
                self._nav(ct, pave=False)
            return

        if ct.get_move_cooldown() != 0:
            return
        if p.distance_squared(self.core) > 8:
            self.tgt = self.core
        elif self.tgt is None or p == self.tgt or self.stuck >= 2:
            self.ang = (self.ang + 1.0) % (2 * math.pi)
            self.tgt = Position(
                max(0, min(self.core.x + int(2 * math.cos(self.ang)), self.mw - 1)),
                max(0, min(self.core.y + int(2 * math.sin(self.ang)), self.mh - 1)),
            )
        self._nav(ct, pave=False)

    def _expand(self, ct):
        p = ct.get_position()
        has_launch = ct.read_store(SLOT_LAUNCHER) != 0
        harv = ct.read_store(SLOT_HARVESTERS)
        allow_pave = has_launch or harv >= 2

        if ct.get_action_cooldown() == 0:
            if self.link_queue and self._build_next_link(ct):
                return
            if ct.get_global_resources() >= ct.get_harvester_cost() and harv < ECO_CAP:
                for d in DIRECTIONS:
                    bp = p.add(d)
                    if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_harvester(bp):
                        ct.build_harvester(bp)
                        ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)
                        if ct.read_store(SLOT_HARVESTERS) >= ECO_NEED:
                            ct.write_store(SLOT_ECO_READY, 1)
                        if not self.link_queue:
                            self.link_queue = self._link_path(ct, bp)
                        break

        if ct.get_move_cooldown() != 0:
            return
        if self.link_queue:
            nxt = self.link_queue[0]
            self.tgt = nearest_core_tile(p, self.core) if (p.x == nxt.x and p.y == nxt.y) else nxt
            self._nav(ct, pave=False)
            return
        if self.tgt is None or p == self.tgt or self.stuck >= 5:
            self.tgt = self._pick(ct)
            self.stuck = 0
            self.wall = None
        if self.tgt is None:
            return
        for d in DIRECTIONS:
            bp = p.add(d)
            if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh:
                if ct.get_tile_env(bp) == Environment.ORE_TITANIUM and ct.get_tile_building_id(bp) is None:
                    self.tgt = bp
                    break
        self._nav(ct, pave=allow_pave)

    def _link_path(self, ct, hpos):
        goals = set()
        for c in core_tiles(self.core):
            for d in CARDINALS:
                t = c.add(d)
                if 0 <= t.x < self.mw and 0 <= t.y < self.mh and dist_core(t, self.core) > 0:
                    goals.add((t.x, t.y))
        start = (hpos.x, hpos.y)
        if start in goals or not goals:
            return []
        prev = {start: None}
        q = deque([start])
        found = None
        while q:
            x, y = q.popleft()
            if (x, y) in goals and (x, y) != start:
                found = (x, y)
                break
            for d in CARDINALS:
                n = Position(x, y).add(d)
                key = (n.x, n.y)
                if key in prev or not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                    continue
                if dist_core(n, self.core) == 0:
                    continue
                try:
                    if ct.get_tile_env(n) == Environment.WALL:
                        continue
                except Exception:
                    pass
                try:
                    bid = ct.get_tile_building_id(n)
                except Exception:
                    bid = None
                if bid is not None and key not in goals:
                    try:
                        et = ct.get_entity_type(bid)
                        if et not in (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER):
                            continue
                    except Exception:
                        continue
                prev[key] = (x, y)
                q.append(key)
        if found is None:
            best = min(goals, key=lambda t: abs(t[0] - hpos.x) + abs(t[1] - hpos.y))
            path, x, y = [], hpos.x, hpos.y
            while x != best[0]:
                x += 1 if best[0] > x else -1
                path.append(Position(x, y))
            while y != best[1]:
                y += 1 if best[1] > y else -1
                path.append(Position(x, y))
            return path
        path, cur = [], found
        while cur is not None and cur != start:
            path.append(Position(cur[0], cur[1]))
            cur = prev[cur]
        path.reverse()
        return path

    def _build_next_link(self, ct):
        if not self.link_queue or ct.get_global_resources() < ct.get_conveyor_cost():
            return False
        # Prefer saving for launcher only after first link segment started
        if (
            not ct.read_store(SLOT_LAUNCHER)
            and len(self.link_queue) > 2
            and ct.get_global_resources() < ct.get_launcher_cost() + ct.get_conveyor_cost()
        ):
            return False
        p = ct.get_position()
        while self.link_queue:
            tile = self.link_queue[0]
            if ct.get_tile_building_id(tile) is not None:
                self.link_queue.pop(0)
                continue
            if p.x == tile.x and p.y == tile.y:
                return False
            break
        if not self.link_queue:
            ct.write_store(SLOT_LINKS_DONE, ct.read_store(SLOT_LINKS_DONE) + 1)
            return False
        tile = self.link_queue[0]
        if max(abs(p.x - tile.x), abs(p.y - tile.y)) > 1:
            return False
        target = nearest_core_tile(tile, self.core)
        if len(self.link_queue) >= 2:
            f = tile.cardinal_direction_to(self.link_queue[1])
            if f == Direction.CENTRE:
                f = nearest_cardinal(tile.direction_to(target))
        else:
            f = nearest_cardinal(tile.direction_to(target))
        if f == Direction.CENTRE:
            f = Direction.NORTH
        if ct.can_build_conveyor(tile, f):
            ct.build_conveyor(tile, f)
            self.link_queue.pop(0)
            if not self.link_queue:
                ct.write_store(SLOT_LINKS_DONE, ct.read_store(SLOT_LINKS_DONE) + 1)
            return True
        return False

    def _pick(self, ct):
        ores = [t for t in ct.get_nearby_tiles()
                if ct.get_tile_env(t) == Environment.ORE_TITANIUM and ct.get_tile_building_id(t) is None]
        if ores:
            return min(ores, key=lambda t: dist_core(t, self.core))
        r = 3 + (ct.get_current_round() // 30) + (self.idx % 5)
        self.ang = (self.ang + 0.65) % (2 * math.pi)
        return Position(
            max(0, min(self.core.x + int(r * math.cos(self.ang)), self.mw - 1)),
            max(0, min(self.core.y + int(r * math.sin(self.ang)), self.mh - 1)),
        )

    def _nav(self, ct, pave=True):
        if self.tgt is None or ct.get_move_cooldown() != 0:
            return
        p = ct.get_position()
        desired = p.cardinal_direction_to(self.tgt)
        if desired == Direction.CENTRE:
            return
        if self._move(ct, desired, pave):
            return
        idx = CARDINALS.index(desired) if desired in CARDINALS else 0
        for d in (CARDINALS[(idx + 1) % 4], CARDINALS[(idx + 3) % 4], desired.opposite()):
            if self._move(ct, d, pave):
                return
        self.stuck += 1

    def _move(self, ct, d, pave=True):
        if d == Direction.CENTRE:
            return False
        nxt = ct.get_position().add(d)
        if not (0 <= nxt.x < self.mw and 0 <= nxt.y < self.mh):
            return False
        if pave and self.core and ct.is_tile_empty(nxt) and ct.get_action_cooldown() == 0:
            if ct.read_store(SLOT_HARVESTERS) >= 1 and ct.get_global_resources() >= ct.get_conveyor_cost():
                if not ct.read_store(SLOT_LAUNCHER):
                    if ct.get_global_resources() < ct.get_launcher_cost() + ct.get_conveyor_cost():
                        pass
                    elif dist_core(nxt, self.core) > 0:
                        here = ct.get_position()
                        if abs(nxt.x - self.core.x) + abs(nxt.y - self.core.y) < abs(here.x - self.core.x) + abs(here.y - self.core.y):
                            card = nearest_cardinal(nxt.direction_to(nearest_core_tile(nxt, self.core)))
                            if ct.can_build_conveyor(nxt, card):
                                ct.build_conveyor(nxt, card)
                                return True
                elif dist_core(nxt, self.core) > 0:
                    here = ct.get_position()
                    if abs(nxt.x - self.core.x) + abs(nxt.y - self.core.y) < abs(here.x - self.core.x) + abs(here.y - self.core.y):
                        card = nearest_cardinal(nxt.direction_to(nearest_core_tile(nxt, self.core)))
                        if ct.can_build_conveyor(nxt, card):
                            ct.build_conveyor(nxt, card)
                            return True
        if ct.can_move(d):
            ct.move(d)
            return True
        return False

    def _turret(self, ct):
        if self.team is None:
            self.team = ct.get_team()
        p = ct.get_position()
        tgt = ct.get_gunner_target()
        if tgt is not None and ct.can_fire(tgt):
            bid = ct.get_tile_building_id(tgt)
            if bid is None or ct.get_team(bid) != self.team:
                ct.fire(tgt)
                return
        try:
            for t in ct.get_attackable_tiles():
                if ct.can_fire(t):
                    bid = ct.get_tile_building_id(t)
                    if bid is None or ct.get_team(bid) != self.team:
                        ct.fire(t)
                        return
        except Exception:
            pass
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) != self.team and ct.can_fire(ct.get_position(eid)):
                ct.fire(ct.get_position(eid))
                return
        enemy = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        best = 10**9
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            ep = ct.get_position(eid)
            d = p.distance_squared(ep)
            if d < best:
                best, enemy = d, ep
        if enemy is not None:
            want = p.direction_to(enemy)
            if want != Direction.CENTRE and want != ct.get_direction():
                if ct.can_rotate(want):
                    ct.rotate(want)
                else:
                    card = nearest_cardinal(want)
                    if card != ct.get_direction() and ct.can_rotate(card):
                        ct.rotate(card)

    def _launcher(self, ct):
        if self.team is None:
            self.team = ct.get_team()
        ct.write_store(SLOT_LAUNCHER, 1)
        if self.core is None:
            for eid in ct.get_nearby_buildings():
                if ct.get_entity_type(eid) == EntityType.CORE and ct.get_team(eid) == self.team:
                    self.core = ct.get_position(eid)
                    break
        if self.core is None:
            return
        w, h = ct.get_map_width(), ct.get_map_height()
        dest = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        if dest is None:
            dest = Position(max(0, w - 2 - self.core.x), max(0, h - 2 - self.core.y))

        drop_sites = []
        for c in core_tiles(dest):
            for d in CARDINALS:
                t = c.add(d)
                if 0 <= t.x < w and 0 <= t.y < h and dist_core(t, dest) == 1:
                    drop_sites.append(t)
        for c in core_tiles(dest):
            for d in DIRECTIONS:
                t = c.add(d)
                if 0 <= t.x < w and 0 <= t.y < h and dist_core(t, dest) == 1:
                    drop_sites.append(t)
        for c in core_tiles(dest):
            for d in DIRECTIONS:
                t = c.add(d)
                if 0 <= t.x < w and 0 <= t.y < h and dist_core(t, dest) > 0:
                    drop_sites.append(t)
        seen, uniq = set(), []
        for s in drop_sites:
            key = (s.x, s.y)
            if key not in seen:
                seen.add(key)
                uniq.append(s)
        drop_sites = uniq

        lp = ct.get_position()
        cands = []
        for eid in ct.get_nearby_entities():
            if ct.get_entity_type(eid) != EntityType.BUILDER_BOT or ct.get_team(eid) != self.team:
                continue
            bp = ct.get_position(eid)
            if bp.distance_squared(lp) > 49:
                continue
            cands.append((bp.distance_squared(lp), bp))
        cands.sort(key=lambda x: x[0])

        for _, bp in cands:
            for site in drop_sites:
                if ct.can_launch(bp, site):
                    ct.launch(bp, site)
                    ct.write_store(SLOT_DROPPED, ct.read_store(SLOT_DROPPED) + 1)
                    return
            if ct.can_launch(bp, dest):
                ct.launch(bp, dest)
                ct.write_store(SLOT_DROPPED, ct.read_store(SLOT_DROPPED) + 1)
                return
