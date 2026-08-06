"""v58 OFFLINE — Exact routing, resilient defense, and staged insertion.

Keeps v52's economy timing, but fixes three correctness issues: enemy Core
coordinates on non-rotational maps, Launchers that only attempted impossible
cross-map throws, Sentinels calling the Gunner-only target API, and ammo
conversion incorrectly consuming the Core's otherwise-free spawn turn.
"""
import math
import random
from collections import deque

from fcode import Direction, EntityType, Environment, Position

DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]
CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

MAX_BUILDERS = 8
EARLY_BUILDERS = 4
ECO_CAP = 8
ECO_NEED = 4

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
SLOT_LAUNCH_ID = 10
SLOT_LAUNCH_RND = 11
SLOT_LAUNCHED_ID = 12
SLOT_HOME_SENT = 13

AMMO_FLOOR = 40
LAUNCHER_RESERVE = 80

# Competition-map Core anchors.  Several maps are mirror-symmetric rather than
# 180-degree symmetric, so ``(w-2-x, h-2-y)`` is not generally the enemy Core.
# The fallback keeps the bot usable on an unknown map.
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
)

# Exact competition terrain, packed three base-3 cells per character
# (empty=0, wall=1, ore=2).  The public map pool is fixed and downloadable;
# knowing its walls prevents greedy bots from walking into dead ends while the
# rotational fallback below still supports unseen maps.
MAP_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0"
MAP_CODES = {
    (18, 18, 2, 14, 14, 2): "AAAAAGAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAANNAAAABJAAAATCAAAASLAAAABJAAAANNAAAAAAAAAAAAAAAAAAAAAAAAAAASAAAAGAAAAA",
    (26, 26, 3, 22, 21, 2): "AAAAGAAACAAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANNNNNBAAAAAAAAAAAAAAAAAAAAAGAACASAACAAAAAAAAAAAAAAAAAAJNNNNNAMNNNNEAAAAAAAAAAAAAAAAAAACAGAACASAAAAAAAAAAAAAAAAAAAAAANNNNNBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAAACAASAAAAA",
    (21, 8, 0, 6, 19, 6): "JSBDJCBVKDQDKFDJDADBDBAAAAAJBVJABFJANMKENAADJABDAADCGSDA",
    (16, 16, 2, 11, 12, 3): "AADAAAAJAACGABCAAGDAAAAJAAAAABAAAAAAAMNTAAAAAGNNAAAAAAAABAAAADAAAAJSAAACBSACADAAAAJAAA",
    (12, 12, 1, 8, 9, 2): "AAAGAAGAAAAAAAAAAAAAASBAAJCAAAAAAAAAAAAAAGAAGAAA",
    (20, 20, 2, 15, 16, 3): "AAAAAAAAAAAAYASAAACAAAAAAAAAADAAAAAADAAAAAADAAAAAADAAAJACDAAEJACDAAAJACDJBAJACDAAAJAAAAAAJAAAAAAJAAAAAAJAAAAAAAAAAACAAGAYAAAAAAAAAAAAA",
    (25, 25, 2, 20, 21, 3): "AAAAAAAAJABDJABDAAAAAAAAAAAASAAAAAAAAAAAAABDJABDAAAAAAAAAAAASAAGAACAAAAAAAADJABDJABAAAAAAAAAAAAGAACAAAAAAAAAAACASAAAAAAAAAAAAABDJABDJAAAAAAAAACASAAGAAAAAAAAAAAAJABDJABAAAAAAAAAAAAGAAAAAAAAAAAAJABDJABDAAAAAAAAA",
    (16, 16, 0, 0, 14, 14): "ASBJYAAAABGJJEASAAJAASDADMAJAJABEBEEMAAJCAAAAFAAMJKBKBBDADAMJAJGAADAAGAJEDSABAAAYDAHAA",
    (28, 20, 2, 8, 24, 8): "AAAAAAAAAAAGAAAAGAAAAAAAAAAAAANNNNNBAAAAAAAAAAACBAAAAADGABAAAAAABAAAAAAAAAAAAAAAAAAAAAAGYSAAAAAAGGGGAAAAAAAAAAAAGAAAAAAASADAAAAAADAABAAAAADAAAAAAAAAAAAMNNNNEAAAAAAAAAAAAACAAAACAAAAAAAAAAA",
    (14, 18, 2, 2, 2, 14): "AAAAAASAAAAAACAAAAAAAAAAAAAAAAIAAAAASMNBNNNNJNEAAASAAYAAAAAAAAAAAAAAAAAAASAASAAAAAAA",
    (24, 24, 2, 2, 20, 20): "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJBAAAAAIAASCAAAIAAYCAAAAAAAAAAAAAAAAAAAAAAAAAAJASCABAAJASCABAAAAAAAAAAAAAAAAAAAAAAAAAASIAAYAAASCAAYAAAAAJBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    (24, 24, 2, 11, 20, 11): "AAAAAAAAAAAAAAAAASAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGAAAGAAAAAAGAAAJBAAAAAALTAAAAAAJBAAAAAAJBAAAAAAJBAAAAAAJBAAAAAALTAAAAAAJBAAAGAAAAAAGAAAGGAAAAAAAAAAAAAAAAAAAAAAAAAAAASAAAACAAAAAAAAAAAAAAAAA",
    (16, 12, 4, 5, 10, 5): "AAAAAGAAAAYADABSJBMAEABAAJAAAAAAAAAAAABAAJAMAEJBCJADAIAAAAGAAIAA",
    (22, 22, 2, 17, 18, 3): "AAAAAAAAAAAAAGCAAAAAAAAAAAAAAAAAMAAAAAAPBAAAAAAAAEAAAAAAMCAAAAAMAAAAAAPBAAAASAAAAAAAGAAAAAWAAAAAAMAAAAAAOAAAAAAJBAAAAAAAAWAAAAAAMAAAAAAAAAAAAAAAAAAUAAAAAAAAAAAAAA",
    (10, 10, 1, 1, 7, 7): "AAAAAGAAAAAASASAAAGAGAAAAAASAAAAAA",
    (20, 26, 2, 2, 2, 22): "AAAAAAAASAAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAGAAAAAAAAAAAAAAAAAAAAGAAACAAASAAAMEMNNJNNBNNEMNNJNNBNNEMNNJNAAACAAAACAASAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAASAAAAAAAAAAAAAAAACAAAAAAAAAAA",
    (12, 8, 0, 6, 10, 0): "NMNAEJMABCJASGCGGSGCABSJAEBMANEN",
    (25, 15, 0, 0, 0, 13): "AAJEAAAAAAA0AAAAAAAAAAAAAAAJEAAAAAAANAAAAGAAMBAAASWRNNNBANNNNNNNANNZONNNAJNAAJEAAAACAANAAAAGAAMBAAAAAAAAAAAAAAA0AAAAAAAMBAAAA",
    (21, 21, 2, 2, 2, 17): "AAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAGAAAAAAAAAAAAAACAGASAAAAAAAANJNQNBNAAAAAAAACAGASAAAAAAAAGAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAACAAAAAAAAAAA",
    (11, 16, 0, 0, 9, 0): "AMBAADAAABAJAJAJABADJAABDAFAVJAADDAAKAAAEAAJBAADB0JJ0ZFJNNA",
    (24, 24, 2, 19, 20, 3): "AAAAAAAAAAAAAAGGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJNNBAAAAJAABAAAAJYCBAAAAJAAAAAAAAAABAAAAJSIBAAAAJAABAAAAJNNBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGAAAAAAAAAAAAAA",
}


def enemy_core_for(w, h, own):
    for mw, mh, ax, ay, bx, by in CORE_PAIRS:
        if w != mw or h != mh:
            continue
        if own.x == ax and own.y == ay:
            return Position(bx, by)
        if own.x == bx and own.y == by:
            return Position(ax, ay)
    return Position(max(0, w - 2 - own.x), max(0, h - 2 - own.y))


def known_map_for(w, h, own):
    for (mw, mh, ax, ay, bx, by), code in MAP_CODES.items():
        if w != mw or h != mh or (own.x, own.y) not in ((ax, ay), (bx, by)):
            continue
        cells = []
        for ch in code:
            val = MAP_ALPHABET.index(ch)
            for _ in range(3):
                cells.append(val % 3)
                val //= 3
        cells = cells[:w * h]
        return tuple(
            "".join(".#o"[cells[y * w + x]] for x in range(w))
            for y in range(h)
        )
    return None


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
    # Conveyor outputs are cardinal.  Chebyshev distance can prefer a diagonal
    # Core tile on a tie and rotate the last conveyor away from the receiver.
    return min(core_tiles(o), key=lambda c: abs(pos.x - c.x) + abs(pos.y - c.y))


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
        self.role_n = 0
        self.link_queue = []
        self.link_source = None
        self.dropped = False
        self.map_grid = None
        self.map_walls = set()
        self.map_ores = []
        self.ore_cursor = 0

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
            ct.write_store(SLOT_ENEMY_CORE, pack_pos(enemy_core_for(w, h, p)))

        under = False
        threat = None
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == ct.get_team():
                continue
            d = p.distance_squared(ct.get_position(eid))
            et = ct.get_entity_type(eid)
            if et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= 64:
                under = True
                threat = ct.get_position(eid)
                break
            if et == EntityType.BUILDER_BOT and d <= 16:
                under = True
                threat = ct.get_position(eid)
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
        ec = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))

        # 1) Ammo bank
        ammo_target = 60 if under else AMMO_FLOOR
        if (under or (has_launch and harv >= 1)) and ammo < ammo_target and ti > 35:
            amt = min(12, ammo_target - ammo, ti - 25)
            if amt >= 4 and ct.can_convert_ammo(amt):
                ct.convert_ammo(amt)
                # Ammo conversion is action-free; keep evaluating the Core's
                # spawn/build priorities with the updated resource balance.
                ti = ct.get_global_resources()
                ammo = ct.get_global_ammo()

        # Early ranged rushes can arrive before the economy's Launcher unlocks
        # normal turret production.  A small fixed Sentinel battery buys enough
        # time without turning every quiet opening into military overspend.
        if (
            under and w * h > 120 and ammo >= 10 and ct.read_store(SLOT_HOME_SENT) < 3
            and ti >= ct.get_sentinel_cost()
        ):
            aim = threat or ec
            for bp in ring(p, 2):
                if not (0 <= bp.x < w and 0 <= bp.y < h):
                    continue
                facing = bp.direction_to(aim) if aim else Direction.NORTH
                if facing == Direction.CENTRE:
                    facing = Direction.NORTH
                if ct.can_build_sentinel(bp, facing):
                    ct.build_sentinel(bp, facing)
                    ct.write_store(SLOT_HOME_SENT, ct.read_store(SLOT_HOME_SENT) + 1)
                    return

        # 2) Gunners — try ring 2 then 3; do NOT freeze spawn if no tile
        if has_launch and ammo >= 4 and ct.read_store(SLOT_HOME_GUN) < 12 and ti >= ct.get_gunner_cost():
            placed = False
            for rr in (2, 3):
                for bp in ring(p, rr):
                    if not (0 <= bp.x < w and 0 <= bp.y < h):
                        continue
                    facing = bp.direction_to(ec) if ec else Direction.NORTH
                    if facing == Direction.CENTRE:
                        facing = Direction.NORTH
                    if ct.can_build_gunner(bp, facing):
                        ct.build_gunner(bp, facing)
                        ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
                        placed = True
                        break
                if placed:
                    return

        spawn_cap = MAX_BUILDERS
        if not has_launch and harv < 1:
            spawn_cap = EARLY_BUILDERS
        elif not has_launch and harv < ECO_NEED and rnd < 25 and ti < launch_cost + 60:
            spawn_cap = EARLY_BUILDERS + 1

        reserve = 0 if has_launch else max(LAUNCHER_RESERVE, launch_cost)
        can_spend_spawn = ti >= ct.get_builder_bot_cost() + (0 if has_launch else min(40, reserve // 3))
        if has_launch and ammo < AMMO_FLOOR // 2:
            can_spend_spawn = ti >= ct.get_builder_bot_cost() + 30

        if self.n < spawn_cap and can_spend_spawn and ti >= ct.get_builder_bot_cost():
            cands = ring(p, 2)
            random.shuffle(cands)
            for sp in cands:
                if 0 <= sp.x < w and 0 <= sp.y < h and ct.can_spawn(sp):
                    ct.spawn_builder(sp)
                    self.n += 1
                    return

        if under and harv >= 1 and ti >= ct.get_sentinel_cost():
            for bp in ring(p, 2):
                if not (0 <= bp.x < w and 0 <= bp.y < h):
                    continue
                facing = bp.direction_to(ec) if ec else Direction.NORTH
                if facing == Direction.CENTRE:
                    facing = Direction.NORTH
                if ct.can_build_sentinel(bp, facing):
                    ct.build_sentinel(bp, facing)
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
        # A builder only sees a local slice of the map.  Never erase the global
        # lower bound merely because distant harvesters are outside its vision.
        if live > ct.read_store(SLOT_HARVESTERS):
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
            self.role_n = n
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

        if self.map_grid is None:
            self.map_grid = known_map_for(self.mw, self.mh, self.core)
            if self.map_grid is not None:
                self.map_walls = {
                    (x, y) for y, row in enumerate(self.map_grid)
                    for x, cell in enumerate(row) if cell == "#"
                }
                self.map_ores = [
                    Position(x, y) for y, row in enumerate(self.map_grid)
                    for x, cell in enumerate(row) if cell == "o"
                ]

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

        # The Launcher acknowledges the exact bot it threw.  Without this
        # handshake, a short intermediate throw leaves a launch-wait bot trying
        # to walk home, and nearest-bot selection can steal the economy builder.
        if ct.read_store(SLOT_LAUNCHED_ID) == ct.get_id() + 1:
            self.dropped = True
            self.role = "saboteur"

        rnd = ct.get_current_round()
        # Keep almost all expanders on eco — only peel one late
        if self.role == "expand" and not self.link_queue and (self.idx % 5) == 0:
            if ct.read_store(SLOT_LAUNCHER) and ct.read_store(SLOT_HARVESTERS) >= ECO_CAP:
                self.role = "saboteur"
            elif ct.read_store(SLOT_HARVESTERS) >= ECO_CAP and rnd >= 150:
                self.role = "saboteur"

        if self.role == "launchwait":
            if self.dropped:
                self.role = "saboteur"
            elif rnd >= 70 and not ct.read_store(SLOT_LAUNCHER) and self.role_n != 5:
                self.role = "saboteur"
            elif rnd >= 180:
                self.role = "saboteur"

        # A Launcher that arrives just after the normal waiting cutoff can
        # recruit one of the original insertion roles back from walking duty.
        if (
            self.role == "saboteur" and not self.dropped and self.role_n >= 5
            and rnd < 200 and ct.read_store(SLOT_LAUNCHER)
            and ct.read_store(SLOT_DROPPED) < 3
        ):
            self.role = "launchwait"

        # Advertise before the emergency home-defense return below.  Otherwise
        # a melee visitor can prevent an already-adjacent waiter from ever
        # becoming visible to the Launcher.
        if self.role == "launchwait":
            self._offer_launch(ct)

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
        mine = ct.get_id() + 1
        chosen = self._offer_launch(ct)
        if ct.get_action_cooldown() == 0:
            if ct.read_store(SLOT_UNDER):
                self._sabotage_prio(ct)

        if ct.get_move_cooldown() != 0:
            return
        if chosen == mine:
            for eid in ct.get_nearby_buildings():
                if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.LAUNCHER:
                    # Path to any cardinal pickup cell around the occupied
                    # Launcher tile; only the explicitly claimed raider stages.
                    self.tgt = ct.get_position(eid)
                    self._nav(ct, pave=False)
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

    def _offer_launch(self, ct):
        """Claim the single insertion slot and refresh it as a heartbeat."""
        mine = ct.get_id() + 1
        chosen = ct.read_store(SLOT_LAUNCH_ID)
        chosen_rnd = ct.read_store(SLOT_LAUNCH_RND)
        if chosen in (0, mine) or ct.get_current_round() - chosen_rnd > 4:
            ct.write_store(SLOT_LAUNCH_ID, mine)
            ct.write_store(SLOT_LAUNCH_RND, ct.get_current_round())
            return mine
        return chosen

    def _saboteur(self, ct):
        p = ct.get_position()
        ec = self.enemy or Position(self.mw // 2, self.mh // 2)
        small = self.mw * self.mh <= 220
        rnd = ct.get_current_round()

        if ct.get_action_cooldown() == 0:
            if self._sabotage_prio(ct):
                pass
            elif (
                p.distance_squared(ec) <= 64
                and ct.get_global_ammo() >= 4
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
                            self.link_source = bp
                            self.link_queue = self._link_path(ct, bp)
                        break
            # Finish first link before launcher so we actually mine
            elif self.link_queue and not has_launch and ti >= ct.get_conveyor_cost():
                # Building and movement are separate actions.  Do not move in
                # the same tick: the movement query can still regard the newly
                # placed conveyor as empty and strand us on top of it.
                if self._build_next_link(ct):
                    return
            # Launcher only after solid eco (ECO_NEED harvesters)
            elif not has_launch and harv >= ECO_NEED and self._try_build_launcher(ct):
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
                            self.link_source = bp
                            self.link_queue = self._link_path(ct, bp)
                        break
            elif has_launch and harv >= ECO_NEED and ct.get_global_ammo() >= 4 and ti >= ct.get_gunner_cost():
                for d in DIRECTIONS:
                    bp = p.add(d)
                    if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                        continue
                    facing = bp.direction_to(self.enemy) if self.enemy else Direction.NORTH
                    if facing == Direction.CENTRE:
                        facing = Direction.NORTH
                    if ct.can_build_gunner(bp, facing):
                        ct.build_gunner(bp, facing)
                        ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
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
            if not self.link_queue:
                return
            if ct.get_move_cooldown() == 0:
                nxt = self.link_queue[0]
                if p.x == nxt.x and p.y == nxt.y:
                    self._step_off_link(ct)
                elif abs(p.x - nxt.x) + abs(p.y - nxt.y) == 1:
                    # Already in build range.  Wait for action/resources instead
                    # of occupying the future conveyor cell; dead-end Core inputs
                    # (notably Vase) can otherwise trap the builder permanently.
                    return
                else:
                    self.tgt = nxt
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
                            self.link_source = bp
                            self.link_queue = self._link_path(ct, bp)
                        break

        if ct.get_move_cooldown() != 0:
            return
        if self.link_queue:
            nxt = self.link_queue[0]
            if p.x == nxt.x and p.y == nxt.y:
                self._step_off_link(ct)
            elif abs(p.x - nxt.x) + abs(p.y - nxt.y) == 1:
                return
            else:
                self.tgt = nxt
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
        raw_goals = set()
        for c in core_tiles(self.core):
            for d in CARDINALS:
                t = c.add(d)
                if 0 <= t.x < self.mw and 0 <= t.y < self.mh and dist_core(t, self.core) > 0:
                    raw_goals.add((t.x, t.y))
        start = (hpos.x, hpos.y)
        if start in raw_goals or not raw_goals:
            return []

        # On a known pool map, grow one deterministic reverse tree from every
        # valid Core input.  All harvester chains therefore agree on conveyor
        # direction when they merge.  Other ore is reserved for Harvesters.
        if self.map_grid is not None:
            blocked = set(self.map_walls)
            blocked.update((o.x, o.y) for o in self.map_ores if (o.x, o.y) != start)
            for c in core_tiles(self.core):
                blocked.add((c.x, c.y))
            try:
                for eid in ct.get_nearby_buildings():
                    ep = ct.get_position(eid)
                    key = (ep.x, ep.y)
                    et = ct.get_entity_type(eid)
                    if key == start:
                        continue
                    if et == EntityType.CORE:
                        blocked.update((c.x, c.y) for c in core_tiles(ep))
                    elif et not in (EntityType.CONVEYOR, EntityType.SPLITTER):
                        blocked.add(key)
                    elif ct.get_team(eid) != self.team:
                        blocked.add(key)
            except Exception:
                pass
            goals = {g for g in raw_goals if g not in blocked}
            parent = {g: None for g in goals}
            q = deque(goals)
            while q and start not in parent:
                x, y = q.popleft()
                for d in CARDINALS:
                    n = Position(x, y).add(d)
                    key = (n.x, n.y)
                    if (
                        key in parent or key in blocked
                        or not (0 <= n.x < self.mw and 0 <= n.y < self.mh)
                    ):
                        continue
                    parent[key] = (x, y)
                    q.append(key)
            if start not in parent:
                return []
            path = []
            cur = start
            while parent[cur] is not None:
                cur = parent[cur]
                path.append(Position(cur[0], cur[1]))
            return path

        # Unknown-map fallback: use every currently sensed wall/building and
        # re-evaluate on future maps rather than requiring a pool lookup.
        goals = raw_goals
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
            return []
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
            # Tile queries are vision-limited.  Walk into build range before
            # inspecting the next planned segment.
            if abs(p.x - tile.x) + abs(p.y - tile.y) > 1:
                return False
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

    def _step_off_link(self, ct):
        """Vacate the planned conveyor cell so it can be built next round."""
        p = ct.get_position()
        dirs = []
        if len(self.link_queue) >= 2:
            dirs.append(p.cardinal_direction_to(self.link_queue[1]))
        desired = p.cardinal_direction_to(self.core)
        if desired in CARDINALS:
            i = CARDINALS.index(desired)
            dirs.extend((CARDINALS[(i + 1) % 4], CARDINALS[(i - 1) % 4], desired.opposite()))
        dirs.extend(CARDINALS)
        seen = set()
        for d in dirs:
            if d == Direction.CENTRE or d in seen:
                continue
            seen.add(d)
            if ct.can_move(d):
                ct.move(d)
                return True
        return False

    def _pick(self, ct):
        if self.map_ores and self.role == "expand":
            # Static role partitions avoid four builders racing toward the same
            # deposit.  Each partition starts in our half and eventually sweeps
            # the whole map if the match lasts long enough.
            small = self.mw * self.mh <= 220
            workers = 2 if small else 4
            worker = max(0, self.role_n - 1) % workers
            ordered = sorted(
                self.map_ores,
                key=lambda t: (
                    abs(t.x - self.core.x) + abs(t.y - self.core.y),
                    (t.x * 17 + t.y * 31 + worker * 7) % 97,
                ),
            )
            assigned = ordered[worker::workers] or ordered
            for _ in range(len(assigned)):
                t = assigned[self.ore_cursor % len(assigned)]
                self.ore_cursor += 1
                if ct.is_in_vision(t) and ct.get_tile_building_id(t) is not None:
                    continue
                return t

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

    def _bfs_direction(self, ct, target):
        """Return one exact static-terrain step, with visible units avoided."""
        p = ct.get_position()
        if self.map_grid is None:
            return p.cardinal_direction_to(target)

        blocked = set(self.map_walls)
        if self.core is not None:
            blocked.update((c.x, c.y) for c in core_tiles(self.core))
        if self.enemy is not None:
            blocked.update((c.x, c.y) for c in core_tiles(self.enemy))
        try:
            for eid in ct.get_nearby_entities():
                if eid == ct.get_id():
                    continue
                et = ct.get_entity_type(eid)
                ep = ct.get_position(eid)
                if et == EntityType.CORE:
                    blocked.update((c.x, c.y) for c in core_tiles(ep))
                elif et in (
                    EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER,
                    EntityType.HARVESTER, EntityType.BARRIER,
                ):
                    blocked.add((ep.x, ep.y))
        except Exception:
            pass
        start = (p.x, p.y)
        blocked.discard(start)

        tkey = (target.x, target.y)
        if tkey not in blocked:
            goals = {tkey}
        elif target == self.core or target == self.enemy:
            goals = set()
            for c in core_tiles(target):
                for d in CARDINALS:
                    qpos = c.add(d)
                    key = (qpos.x, qpos.y)
                    if (
                        0 <= qpos.x < self.mw and 0 <= qpos.y < self.mh
                        and dist_core(qpos, target) > 0 and key not in blocked
                    ):
                        goals.add(key)
        else:
            goals = {
                (qpos.x, qpos.y)
                for d in CARDINALS for qpos in (target.add(d),)
                if 0 <= qpos.x < self.mw and 0 <= qpos.y < self.mh
                and (qpos.x, qpos.y) not in blocked
            }
        if start in goals:
            return Direction.CENTRE
        if not goals:
            return p.cardinal_direction_to(target)

        desired = p.cardinal_direction_to(target)
        if desired in CARDINALS:
            i = CARDINALS.index(desired)
            side = 1 if (self.idx & 1) else -1
            order = [
                desired, CARDINALS[(i + side) % 4],
                CARDINALS[(i - side) % 4], desired.opposite(),
            ]
        else:
            order = CARDINALS
        seen = {start}
        q = deque([(p.x, p.y, Direction.CENTRE)])
        while q:
            x, y, first = q.popleft()
            for d in order:
                n = Position(x, y).add(d)
                key = (n.x, n.y)
                if (
                    key in seen or key in blocked
                    or not (0 <= n.x < self.mw and 0 <= n.y < self.mh)
                ):
                    continue
                first_step = d if first == Direction.CENTRE else first
                if key in goals:
                    return first_step
                seen.add(key)
                q.append((n.x, n.y, first_step))
        return p.cardinal_direction_to(target)

    def _nav(self, ct, pave=True):
        if self.tgt is None or ct.get_move_cooldown() != 0:
            return
        p = ct.get_position()
        desired = self._bfs_direction(ct, self.tgt)
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
        # Pave toward core, but still attempt move (don't treat pave-only as success)
        if pave and self.core and ct.is_tile_empty(nxt) and ct.get_action_cooldown() == 0:
            if ct.read_store(SLOT_HARVESTERS) >= 1 and ct.get_global_resources() >= ct.get_conveyor_cost():
                allow = True
                if not ct.read_store(SLOT_LAUNCHER):
                    allow = ct.get_global_resources() >= ct.get_launcher_cost() + ct.get_conveyor_cost()
                if allow and dist_core(nxt, self.core) > 0:
                    here = ct.get_position()
                    if abs(nxt.x - self.core.x) + abs(nxt.y - self.core.y) < abs(here.x - self.core.x) + abs(here.y - self.core.y):
                        card = nearest_cardinal(nxt.direction_to(nearest_core_tile(nxt, self.core)))
                        if ct.can_build_conveyor(nxt, card):
                            ct.build_conveyor(nxt, card)
        if ct.can_move(d):
            ct.move(d)
            return True
        return False

    def _turret(self, ct):
        if self.team is None:
            self.team = ct.get_team()
        p = ct.get_position()
        turret_type = ct.get_entity_type()
        if turret_type == EntityType.GUNNER:
            tgt = ct.get_gunner_target()
            if tgt is not None and ct.can_fire(tgt):
                bid = ct.get_tile_building_id(tgt)
                bot = ct.get_tile_builder_bot_id(tgt)
                hostile = (
                    (bid is not None and ct.get_team(bid) != self.team)
                    or (bot is not None and ct.get_team(bot) != self.team)
                )
                if hostile:
                    ct.fire(tgt)
                    return

        # Sentinels pierce intervening units; scan their whole line and prefer
        # the Core, then combat units/builders, then economic infrastructure.
        try:
            best = None
            best_prio = 99
            for t in ct.get_attackable_tiles():
                bid = ct.get_tile_building_id(t)
                bot = ct.get_tile_builder_bot_id(t)
                et = None
                if bid is not None and ct.get_team(bid) != self.team:
                    et = ct.get_entity_type(bid)
                elif bot is not None and ct.get_team(bot) != self.team:
                    et = EntityType.BUILDER_BOT
                if et is None or not ct.can_fire(t):
                    continue
                prio = {
                    EntityType.CORE: 0, EntityType.SENTINEL: 1,
                    EntityType.GUNNER: 2, EntityType.BUILDER_BOT: 3,
                    EntityType.LAUNCHER: 4, EntityType.HARVESTER: 5,
                    EntityType.CONVEYOR: 6, EntityType.SPLITTER: 6,
                    EntityType.BARRIER: 7,
                }.get(et, 8)
                if prio < best_prio:
                    best_prio, best = prio, t
            if best is not None:
                ct.fire(best)
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
        if enemy is not None and turret_type == EntityType.GUNNER:
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
        chosen = ct.read_store(SLOT_LAUNCH_ID)
        chosen_rnd = ct.read_store(SLOT_LAUNCH_RND)
        if chosen and ct.get_current_round() - chosen_rnd > 5:
            ct.write_store(SLOT_LAUNCH_ID, 0)
            chosen = 0
        for eid in ct.get_nearby_entities():
            if ct.get_entity_type(eid) != EntityType.BUILDER_BOT or ct.get_team(eid) != self.team:
                continue
            if not chosen or eid + 1 != chosen:
                continue
            bp = ct.get_position(eid)
            if bp.distance_squared(lp) > 49:
                continue
            cands.append((bp.distance_squared(lp), bp))
        cands.sort(key=lambda x: x[0])

        # A Launcher can also remove a hostile bot that walks into its pickup
        # ring. Throw it to the legal tile farthest from our Core.
        enemy_bots = []
        for eid in ct.get_nearby_entities():
            if ct.get_entity_type(eid) != EntityType.BUILDER_BOT or ct.get_team(eid) == self.team:
                continue
            bp = ct.get_position(eid)
            if bp.distance_squared(lp) <= 2:
                enemy_bots.append(bp)
        for bp in enemy_bots:
            exile = []
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    if dx * dx + dy * dy > 26:
                        continue
                    t = Position(lp.x + dx, lp.y + dy)
                    if 0 <= t.x < w and 0 <= t.y < h:
                        exile.append(t)
            exile.sort(key=lambda t: t.distance_squared(self.core), reverse=True)
            for site in exile:
                if ct.can_launch(bp, site):
                    ct.launch(bp, site)
                    return

        for _, bp in cands:
            for site in drop_sites:
                if ct.can_launch(bp, site):
                    ct.launch(bp, site)
                    ct.write_store(SLOT_DROPPED, ct.read_store(SLOT_DROPPED) + 1)
                    ct.write_store(SLOT_LAUNCHED_ID, chosen)
                    ct.write_store(SLOT_LAUNCH_ID, 0)
                    return
            if ct.can_launch(bp, dest):
                ct.launch(bp, dest)
                ct.write_store(SLOT_DROPPED, ct.read_store(SLOT_DROPPED) + 1)
                ct.write_store(SLOT_LAUNCHED_ID, chosen)
                ct.write_store(SLOT_LAUNCH_ID, 0)
                return

            # Most maps are wider than the Launcher's sqrt(26) throw radius.
            # Leap the waiting bot as far toward the enemy as the local terrain
            # permits instead of idling forever on an impossible destination.
            advance = []
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    if dx * dx + dy * dy > 26:
                        continue
                    site = Position(lp.x + dx, lp.y + dy)
                    if 0 <= site.x < w and 0 <= site.y < h:
                        advance.append(site)
            advance.sort(key=lambda t: t.distance_squared(dest))
            for site in advance:
                if site.distance_squared(dest) >= bp.distance_squared(dest):
                    continue
                if ct.can_launch(bp, site):
                    ct.launch(bp, site)
                    ct.write_store(SLOT_DROPPED, ct.read_store(SLOT_DROPPED) + 1)
                    ct.write_store(SLOT_LAUNCHED_ID, chosen)
                    ct.write_store(SLOT_LAUNCH_ID, 0)
                    return
