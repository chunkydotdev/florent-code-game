"""LOKI-FERRY-SIEGE -- the self-ferry siege raider.  Ablatable as a unit.

Set LOKI_FERRY_SIEGE_ON = False in doctrine.py and every entry point in this
file returns False on its first line; what is left is `_v488beltbreak2`.

THE FOUR MOVES, and where each one's evidence lives:

  FERRY   The raider builds a LAUNCHER on its own forward tile; the NEXT round
          that launcher's own run() throws the raider ~5 tiles forward and then
          calls `ct.self_destruct()` as the LAST statement of its turn.  2-round
          cycle, ~3 tiles/round, 3x walking, and the +10% scale contribution is
          refunded on the very next round's reading.
          -- PROBE-DOSSIER-ferry-siege-2026-08-17.md P1, P2
  SEAL    Barrier the enemy core's 12-tile ring.  The 8 ORTHOGONAL seats are
          the only tiles a builder can heal that core from; the 12 are exactly
          its legal spawn set.  BINARY: a partial >=10/12 seal measured a
          HIGHER defender heal rate than no seal at all, so the first barrier
          waits until the bank pays for all of them.
          -- P3; REPLAY-STUDY-jython-v157-wider-2026-08-17.md §3
  EVICT   A launcher parked ON the ring throws arriving enemy builders away.
          0 ammo, re-throwable every round, one launcher holds ~4 attackers off
          indefinitely.  SITING by `cov` is the whole game -- the same plant on
          fixed ring indices read 0 evictions in 1,000 rounds.
          -- P4; `_v233evict58/raid.py:694-696` for the score itself
  KILL    ONE ALIGNED SENTINEL.  95.2% of all enemy-core damage over 60 games;
          0/37 core kills without one in range.  Its ray ignores obstacles and
          shoots THROUGH our own collar; a gunner's does not.  A MIS-aligned
          sentinel contributes literally zero, so `can_fire_from` gates the
          build rather than explaining the result.
          -- REPLAY-STUDY-jython-inspiration-2026-08-17.md §2.7

WHAT WE HAVE THAT THE 2174-RATED IMPLEMENTATION DOES NOT.  Four measured
defects, each one an edge rather than a guess: a TEAM FILTER on eviction
pickup (their ring launcher kidnapped its own raider 57 times in one game and
that ring finished 7/12); a SMALL-MAP / NO-ROUTE GATE (fjordgate, 10x10, cores
d^2=32 -- every leg of the plank inverted and they lost); a RAIDER REPLACEMENT
(one raider, 60/60 games, never replaced); and a DUMP-TILE OWN-CORE GUARD
(10 of 13 of their dumps landed inside d^2<=8 of their OWN core).

TWO ENGINE FACTS THIS FILE IS WRITTEN AGAINST, both from the s50 probes:

  * `is_in_vision()` IS NOT A BOUNDS GUARD.  It is a pure radius test; the next
    `get_tile_*` on an off-map position raises.  This plank works at map edges
    BY DESIGN, so every computed position is bounds-checked explicitly.
  * NOTHING MAY FOLLOW `ct.self_destruct()`.  It never returns and raises
    nothing catchable -- `finally:`, `except BaseException` and
    `except SystemExit` are all rejected by the sandbox AST validator at load.
"""
import sys

from fcode import Direction, EntityType, Position

from doctrine import *  # noqa: F401,F403
from eco import (
    core_corners, core_tiles, dsq_core, enemy_core_for, heal_seats, unpack_pos,
)

# A building of one of these types on a ring tile denies the core's spawn AND
# blocks a builder from standing there to heal.  ⛔ CONVEYOR and SPLITTER are
# deliberately ABSENT: they are bot-passable, and 40.1% of all spawns in the
# corpus land on a conveyor tile.  Two trees in this repo state the opposite in
# a comment (`_det269awrspawn/raid.py:673-675`, `_det252spawnlock/doctrine.py`)
# and both are wrong -- see the dossier's prior-art notes.
FS_BLOCKING = frozenset((
    EntityType.BARRIER, EntityType.HARVESTER, EntityType.GUNNER,
    EntityType.SENTINEL, EntityType.LAUNCHER, EntityType.CORE,
))


class SiegeMixin:

    # ------------------------------------------------------------------
    # instrumentation.  stderr, never print(): platform replays strip stdout
    # (measured s28 -- 30,664 of 30,664 BotOutput events carry an empty
    # `stdout`), so a plank that reads its own tag out of a live replay is
    # planning on an instrument that does not exist.  This is a LOCAL demo
    # instrument and it is off by default.
    # ------------------------------------------------------------------

    def _fs_log(self, *a):
        if not FS_LOG:
            return
        try:
            print("FS", *a, file=sys.stderr)
        except Exception:
            return

    # ------------------------------------------------------------------
    # the shared store slot (see doctrine.py, SLOT_FS)
    # ------------------------------------------------------------------

    def _fs_state(self, ct):
        """(beat_round_plus_1, phase, raider_id_plus_1) off SLOT_FS."""
        return self._fs_state_at(ct, SLOT_FS)

    def _fs_state_at(self, ct, slot):
        """The same triple off ANY slot carrying the SLOT_FS field layout.

        v514 change D (ported from the s51 double-ferry probe): body 2
        publishes into its OWN slot, so nothing has two writers.  See
        FS_SUPP_SLOT in doctrine.py for the lost-update defect this exists for.
        """
        try:
            v = ct.read_store(slot)
        except Exception:
            return 0, FS_PH_NONE, 0
        return (v & FS_BEAT_MASK,
                (v >> FS_PHASE_SHIFT) & FS_PHASE_MASK,
                v >> FS_RID_SHIFT)

    # ------------------------------------------------------------------
    # v514 CHANGE A -- THE ECO GATE (Magnus ruling 2: "as soon as 2 harvestors
    # are built and connected").  Published by the CORE only; read by the
    # raider's sentinel gate and by the Core's own magazine.
    # ------------------------------------------------------------------

    def _fs_eco_mouth(self, ct):
        """(mouth_building_id, holding_a_stack) for our belt's last link.

        MOUTH := a friendly CONVEYOR on one of our own core's 8 delivery seats
        whose facing points at a core footprint tile, or a friendly SPLITTER on
        such a seat (a splitter rotates its output among three directions and
        one of them is the core).  Every delivery into a core footprint in the
        corpus originates on one of those eight tiles.

        Called from the CORE, whose vision is r^2 = 36 -- the seats are all at
        d^2 <= 5, so this read can never be blind.  Bounds are checked
        explicitly (`is_in_vision` is a pure radius test, s50 probe).
        """
        if self.core is None:
            return None, False
        try:
            seats = heal_seats(self.core, self.mw, self.mh)
        except Exception:
            return None, False
        ctiles = set((t.x, t.y) for t in core_tiles(self.core))
        for s in seats:
            if not (0 <= s.x < self.mw and 0 <= s.y < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(s)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            if et == EntityType.CONVEYOR:
                try:
                    f = ct.get_direction(bid)
                    dx, dy = f.delta()
                except Exception:
                    continue
                if (s.x + dx, s.y + dy) not in ctiles:
                    continue                 # points somewhere else: not a mouth
            elif et != EntityType.SPLITTER:
                continue
            held = False
            try:
                held = ct.get_stored_resource_id(bid) is not None
            except Exception:
                held = False
            return bid, held
        return None, False

    def _fs_eco_publish(self, ct, rnd, harv):
        """CORE ONLY.  The single writer of FS_ECO_SLOT."""
        try:
            cur = ct.read_store(FS_ECO_SLOT)
        except Exception:
            return
        conn = bool(cur & FS_ECO_BIT_CONN)
        deliv = bool(cur & FS_ECO_BIT_DELIV)
        if conn and deliv:
            return                           # latched: nothing left to say
        mouth, held = self._fs_eco_mouth(ct)
        now_conn = (harv >= FS_SENT_HARV_MIN) and mouth is not None
        new = cur
        if now_conn and not conn:
            new |= FS_ECO_BIT_CONN
            new |= ((rnd + 1) & FS_ECO_RND_MASK) << FS_ECO_RND_SHIFT
            new |= (min(harv, 31) << FS_ECO_HARV_SHIFT)
        if held and not deliv:
            new |= FS_ECO_BIT_DELIV
        if new == cur:
            return
        try:
            ct.write_store(FS_ECO_SLOT, new & 0x3FFFFFFF)
        except Exception:
            return
        if FS_ECO_LOG:
            try:
                print("ECO514", rnd, "harv", harv,
                      "mouth", 1 if mouth is not None else 0,
                      "held", 1 if held else 0,
                      "conn", 1 if (new & FS_ECO_BIT_CONN) else 0,
                      "deliv", 1 if (new & FS_ECO_BIT_DELIV) else 0,
                      file=sys.stderr)
            except Exception:
                return

    def _fs_eco_latch(self, ct):
        """(conn_bit, deliv_bit, latch_round) -- the instrument, not a gate."""
        try:
            v = ct.read_store(FS_ECO_SLOT)
        except Exception:
            return (-1, -1, -1)
        return (1 if v & FS_ECO_BIT_CONN else 0,
                1 if v & FS_ECO_BIT_DELIV else 0,
                ((v >> FS_ECO_RND_SHIFT) & FS_ECO_RND_MASK) - 1)

    def _fs_eco_gate_ok(self, ct):
        """MAGNUS RULING 2, the predicate.  Two harvesters built AND the belt
        demonstrably delivering.  Its failure mode is stated in doctrine.py:
        it does NOT prove both harvesters are routed (the `_wire_tick` orphan
        defect, v513 open item 5) -- it errs toward opening the gate."""
        if FS_SENT_GATE_BYPASS:
            return True                      # change-A mutant, never shipped
        try:
            v = ct.read_store(FS_ECO_SLOT)
        except Exception:
            return False
        if not (v & FS_ECO_BIT_CONN):
            return False
        if FS_SENT_DELIV_REQ and not (v & FS_ECO_BIT_DELIV):
            return False
        return True

    def _fs_publish(self, ct, rnd, phase, rid):
        try:
            ct.write_store(
                self._fs_slot(),
                ((rnd + 1) & FS_BEAT_MASK)
                | ((phase & FS_PHASE_MASK) << FS_PHASE_SHIFT)
                | (((rid + 1) & 0xFFFF) << FS_RID_SHIFT),
            )
        except Exception:
            return

    def _fs_slot(self):
        """The publish slot THIS body owns.  v514 change D: ONE WRITER PER SLOT.

        Routed on `fs_body` (fixed at appointment) rather than on `fs_role`, so
        a support that PROMOTES to sealer keeps its own channel instead of
        starting to clobber the sealer's -- which is precisely the r197 defect
        (probe report: the sealer's beat never advances once the support
        exists, the staleness detector fires, the support promotes itself at
        r10, and every later body reads seat 0 as stale).

        ⛔ Inert unless the crew is ON.  With FS_CREW_ON False there is exactly
        one ferry-siege body, FS_SUPP_SLOT stays the chassis home-ferry's, and
        this returns SLOT_FS for every caller.
        """
        if LOKI_FS_V514 and FS_V514_RELAY and LOKI_FS_CREW and FS_CREW_ON \
                and getattr(self, "fs_body", 1) == 2:
            return FS_SUPP_SLOT
        return SLOT_FS

    def _fs_crew_slots(self):
        """Every slot a ferry-siege body of ours may be publishing into."""
        if LOKI_FS_V514 and FS_V514_RELAY and LOKI_FS_CREW and FS_CREW_ON:
            return (SLOT_FS, FS_SUPP_SLOT)
        return (SLOT_FS,)

    def _fs_beat_only(self, ct, rnd):
        """Write the incumbent's foothold heartbeat without touching the
        plank's fields that live above it in the same slot.

        Store writes are buffered one round, so the high bits preserved here
        are LAST round's -- if a non-ferry raider and the ferry raider both
        write in the same round the phase can lag by one.  Bounded and
        self-healing: the ferry raider republishes its full word every round it
        runs, and every consumer of the phase treats it as advisory.
        """
        if not LOKI_FERRY_SIEGE_ON:
            ct.write_store(SLOT_RAID_LIVE, rnd + 1)
            return
        try:
            cur = ct.read_store(SLOT_RAID_LIVE)
        except Exception:
            cur = 0
        try:
            ct.write_store(SLOT_RAID_LIVE,
                           (cur & ~FS_BEAT_MASK) | ((rnd + 1) & FS_BEAT_MASK))
        except Exception:
            return

    def _fs_stale(self, ct, rnd):
        """⛔ KNOWN DEFECT, MEASURED, NOT FIXED HERE -- READ IT.

        THE RAIDER REPLACEMENT IS GATED ON SOMETHING IT SHOULD NOT BE.  It is
        NOT dead code: measured s50 over 30 local games per arm (5 maps x 6
        repeats), a successor was appointed in 13/30 games here and 10/30 for
        v510.  What is wrong is WHEN it declines to fire.  v510's midgard demo
        is the failure case -- raider id 3 died at r268 and 277 of 545 rounds
        ran with no siege raider at all.

        ⚠ AND AN EARLIER VERSION OF THIS NOTE SAID "NEVER FIRES, 30/30 GAMES".
        That was an INSTRUMENT ERROR, kept here as a warning: the counting
        one-liner read `awk '{print $5}'`'s neighbour and tallied the literal
        token `id` from every PHASE line, so every game returned exactly one
        "distinct id" -- a constant column, which validates anything.

        THE MECHANISM IS THE SHARED STORE SLOT, and it is not a coding slip.
        `SLOT_FS is SLOT_RAID_LIVE`, and the CHASSIS's ordinary raid doctrine
        calls `_fs_beat_only` from `raid.py:174` and `:191` for ANY of our
        bodies established at the enemy ring.  So the low bits stay fresh
        whether or not the FERRY raider is alive, `_fs_stale` returns False,
        and the successor door at `main.py:751-766` stays shut -- ⛔ exactly
        when another body of ours is AT the ring, which is the contested case
        where a replacement is worth most.  Backwards, by construction.

        AND IT CANNOT BE PATCHED INSIDE THIS SLOT.  Any liveness channel needs a
        field the FS raider alone writes and someone else clears.  Turn order is
        entity-id ascending and the FS raider is the r0 spawn -- the LOWEST
        builder id -- so every chassis raider acts AFTER it and would clobber
        (or restore) whatever it wrote in the same round.  A clear-then-set
        scheme needs the raider to write LAST, and it never does.  The fix is a
        dedicated field, which is exactly the thing the v510 build report
        recorded as unavailable ("no free slot exists; index 16 out of range").
        """
        if LOKI_FS_CREW:
            # ⭐ v513: ANSWERED OFF DEDICATED BITS.  The paragraph above is the
            # diagnosis and this is the fix -- `_fs_crew_age` reads a field
            # only a ferry-siege body ever writes, so a chassis raider standing
            # at the ring can no longer hold the successor door shut.  The
            # SEALER seat is the one this predicate is about: it is the body
            # whose absence stops the collar.
            return self._fs_crew_age(ct, 0, rnd) > FS_CREW_STALE
        beat, _ph, _rid = self._fs_state(ct)
        return (not beat) or (rnd - (beat - 1) > FS_BEAT_STALE)

    # ------------------------------------------------------------------
    # the CREW slot (v513) -- two heartbeats with no shared writer
    # ------------------------------------------------------------------

    def _fs_crew_word(self, ct):
        try:
            return ct.read_store(FS_CREW_SLOT)
        except Exception:
            return 0

    def _fs_crew_age(self, ct, seat, rnd):
        """Rounds since seat 0 (sealer) / seat 1 (support) last reported.

        A never-reported seat returns a number no staleness test can pass.
        Beats are ABSOLUTE round numbers in 11 bits (MAX_TURNS = 1000 < 2047),
        so unlike a modular beat there is no window in which a long-dead body
        reads as fresh again.
        """
        if seat and LOKI_FS_V514 and FS_V514_RELAY and LOKI_FS_CREW \
                and FS_CREW_ON:
            # v514 change D: the SUPPORT's beat is the beat field of its OWN
            # publish slot -- one writer, so no lost update.  FS_CREW_SLOT's
            # bits 19-29 are dead in this configuration.
            v = self._fs_state_at(ct, FS_SUPP_SLOT)[0]
            if not v:
                return 10 ** 6
            return rnd - (v - 1)
        shift = FS_CREW_SUPP_SHIFT if seat else FS_CREW_SEAL_SHIFT
        v = (self._fs_crew_word(ct) >> shift) & FS_CREW_BEAT_MASK
        if not v:
            return 10 ** 6
        return rnd - (v - 1)

    def _fs_crew_publish(self, ct, seat, rnd):
        """Write MY seat's beat, preserving the other seat and the counter.

        ⛔ THE SLOT IS AN UNSIGNED 32-BIT INTEGER (engine probe, s50): a value
        above 2**32-1 -- or ANY negative -- raises OverflowError, and an
        OverflowError escaping run() destroys this unit for the rest of the
        match.  Every field written here is masked to its width first, so the
        word is 30 bits by construction and cannot go negative.
        """
        if seat and LOKI_FS_V514 and FS_V514_RELAY and LOKI_FS_CREW \
                and FS_CREW_ON:
            return          # v514 change D: written by _fs_publish, FS_SUPP_SLOT
        shift = FS_CREW_SUPP_SHIFT if seat else FS_CREW_SEAL_SHIFT
        try:
            cur = ct.read_store(FS_CREW_SLOT)
            cur &= ~(FS_CREW_BEAT_MASK << shift)
            cur |= ((rnd + 1) & FS_CREW_BEAT_MASK) << shift
            ct.write_store(FS_CREW_SLOT, cur & 0x3FFFFFFF)
        except Exception:
            return

    def _raid_seat_take(self, ct):
        """Issue the next raider seat, sharing SLOT_RAID_N with the crew beats.

        The incumbent wrote `read + 1` into the whole slot; the counter's
        ceiling is LOKI_MAX_BUILDERS = 11, so it is confined to the low eight
        bits here and the crew heartbeats live above it.  With LOKI_FS_CREW
        False this is byte-for-byte the incumbent read-and-increment.
        """
        try:
            cur = ct.read_store(SLOT_RAID_N)
        except Exception:
            return 0
        if not LOKI_FS_CREW:
            try:
                ct.write_store(SLOT_RAID_N, cur + 1)
            except Exception:
                pass
            return cur
        n = cur & FS_RAIDN_MASK
        try:
            ct.write_store(SLOT_RAID_N,
                           ((cur & ~FS_RAIDN_MASK)
                            | ((n + 1) & FS_RAIDN_MASK)) & 0x3FFFFFFF)
        except Exception:
            pass
        return n

    # ------------------------------------------------------------------
    # B. the gate -- a map on which the plank cannot express
    # ------------------------------------------------------------------

    def _fs_gate(self, ct):
        """May the ferry-siege run on THIS map?  Cached per unit.

        fjordgate (10x10, cores d^2=32) is the game the 2174-rated version
        LOST, and it lost it because every leg of the plank inverts on a small
        board: the ferry buys no tempo, the raider lands in the middle of an
        army that is already home, and the barriers are contested rather than
        built once.  jackpot is the other refusal -- the probe's ferry never
        found a route there on any hop budget.

        Refusing is not a fallback: the bot plays the incumbent raid doctrine
        for that game, unchanged.
        """
        if not LOKI_FERRY_SIEGE_ON:
            return False
        if self.fs_gate_ok is not None:
            return self.fs_gate_ok
        if self.core is None or not (self.mw and self.mh):
            return False            # not cached: ask again once we know
        E = self.enemy
        if E is None:
            try:
                E = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
            except Exception:
                E = None
        if E is None:
            E = enemy_core_for(self.mw, self.mh, self.core)
        if E is None:
            return False
        ok = self._fs_map_gated(self.mw, self.mh, self.core, E, ct)
        self.fs_gate_ok = ok
        return ok

    def _fs_map_gated(self, mw, mh, ours, E, ct=None):
        """The map gate as a PURE function of the two anchors and the board.

        Factored out for v516 change 2, whose beat is written from a SENTINEL
        -- a unit whose `self.core` is None by design (`_door_turret_turn`
        returns on that null) and must stay that way.  Byte-identical tests to
        the ones `_fs_gate` used inline; `_fs_gate` now calls this.
        """
        ok = True
        if max(mw, mh) < FS_MIN_MAP_DIM:
            ok = False
        elif ours.distance_squared(E) < FS_MIN_CORE_DSQ:
            ok = False
        elif LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER and FS_MAP_SKIP_ON:
            # THE CLOSURE-BASED SKIP SET (doctrine.py, FS_MAP_SKIP).  A board
            # the FIELD cannot close is a board we spend 1,000 rounds on and
            # lose on the tiebreak, which the programme scores as a defeat even
            # when we win it.  No map name reaches a bot, so the key is the
            # board's own geometry.
            a, b = (ours.x, ours.y), (E.x, E.y)
            sig = (mw, mh, min(a, b), max(a, b))
            if sig in FS_MAP_SKIP:
                ok = False
            if ct is not None:
                self._fs_log("GATE", ct.get_current_round(), "sig", sig,
                             "ok", 1 if ok else 0)
        return ok

    def _fs_active(self, ct):
        """Is the plank live for this unit right now?"""
        if not LOKI_FERRY_SIEGE_ON or self.fs_off:
            return False
        return self._fs_gate(ct)

    # ------------------------------------------------------------------
    # geometry
    # ------------------------------------------------------------------

    def _fs_ring12(self, E):
        """The enemy core's 12 adjacency tiles, in-bounds and not wall.

        Cached on the anchor: it is a pure function of the anchor and the map,
        so every unit derives the same list with no store traffic.
        """
        key = (E.x, E.y)
        if self.fs_ring_key == key and self.fs_ring is not None:
            return self.fs_ring, self.fs_seats
        seats = [s for s in heal_seats(E, self.mw, self.mh)
                 if not self._fs_wall(s)]
        corners = [c for c in core_corners(E, self.mw, self.mh)
                   if not self._fs_wall(c)]
        self.fs_ring_key = key
        self.fs_seats = seats
        self.fs_ring = seats + corners
        return self.fs_ring, self.fs_seats

    def _fs_wall(self, t):
        """Static terrain test off the decoded grid -- never a get_tile_env.

        Bounds first, always: `is_in_vision()` is NOT a bounds guard (measured
        s50) and this code runs at map edges by design.
        """
        if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
            return True
        g = self.map_grid
        if g is None:
            return False
        try:
            return g[t.y][t.x] == "#"
        except Exception:
            return False

    def _fs_target(self, ct, E):
        """THE BACKSIDE of the enemy core -- Magnus's instruction, verbatim.

        The ring tile FARTHEST from our own core: land behind them, not in
        front.  Jython's killing sentinel sat beyond the core relative to its
        own home in 4 of 5 games, and the far side is where the defender's own
        traffic and belts are not.

        Recomputed from `get_position()`-derived anchors each call rather than
        cached as a Position across rounds -- a launcher throw mutates position
        between turns and a cached Position is exactly the stale-state hazard
        the ferry creates for itself.
        """
        # ⭐ TWO GEOMETRY FACTS RE-CHECKED AGAINST RESEARCH'S CENSUS (s50), both
        # already correct in this tree and both worth stating so nobody
        # "fixes" them:
        #   * A WALL SEAT IS A FREE SEAL.  `_fs_ring12` drops wall tiles from
        #     `seats` entirely, so they never enter `needed` and never count in
        #     `orth_open` -- i.e. they are pre-denied, which is what the census
        #     asks for (jackpot has 4, ragnarok 2 -- the cheapest rings around).
        #   * A BELT SEAT IS A LIVE HEAL SEAT, NOT A BLOCKED ONE.  An enemy
        #     conveyor/splitter is bot-passable, so `_fs_denied` returns False
        #     for it (it is a TARGET, not denial) and `orth_open` counts it
        #     open; `_fs_body_blocked` only demotes it in the ORDERING.  That is
        #     what makes rung 3 worth its rounds.
        ring, seats = self._fs_ring12(E)
        if not ring:
            return E
        C = self.core
        best, best_k = None, None
        seatset = set((s.x, s.y) for s in seats)
        for t in ring:
            k = (t.distance_squared(C), 1 if (t.x, t.y) in seatset else 0)
            if best_k is None or k > best_k:
                best, best_k = t, k
        return best if best is not None else E

    def _fs_park_seat(self, ct, E):
        """The one orthogonal seat we do NOT barrier -- we stand on it.

        A BODY on a ring tile denies the spawn identically to a barrier
        (measured, P3), so parking costs nothing in denial and keeps a
        heal-denied peck station.  Chosen on the backside, and only where the
        seat has a passable OUTWARD neighbour so the raider can still reach it
        once the rest of the ring is barriered.
        """
        _ring, seats = self._fs_ring12(E)
        pool = seats
        if LOKI_FS_SEAL_ONLY:
            # ⛔ PARK ON A DIAGONAL, NOT ON A HEAL SEAT.  THE PARK SEAT IS THE
            # LEAK.  Autopsy of the v510 midgard demo: `_fs_census` excludes the
            # park tile from `needed` so it can NEVER be barriered, and
            # `_fs_denied` scores it denied only while our body is standing on
            # it -- the v510 raider stood there once (r48), left at r49 and
            # never came back.  51 of that game's 59 enemy core-heals were
            # delivered FROM THAT ONE TILE (234 HP restored = 39.4% of all
            # damage we dealt), and `orth_open >= 1` for ever means the phase
            # can never reach FS_PH_SEALED.  A body denies spawn on whatever
            # tile it holds (P3, tile-agnostic), so under seal-only we barrier
            # ALL EIGHT orthogonals and park the body on a DIAGONAL instead:
            # the heal set closes completely and the parked body still denies
            # one of the four spawn corners.
            pool = [c for c in core_corners(E, self.mw, self.mh)
                    if not self._fs_wall(c)]
        if not pool:
            return None
        if self.fs_park is not None and self.fs_park_key == (E.x, E.y):
            return self.fs_park
        C = self.core
        best, best_k = None, None
        for s in pool:
            outward = 0
            for dx, dy in CARD_DELTAS:
                n = Position(s.x + dx, s.y + dy)
                if self._fs_wall(n):
                    continue
                if dsq_core(n, E) == 0:
                    continue                 # a core footprint tile
                outward += 1
            k = (1 if outward else 0, s.distance_squared(C))
            if best_k is None or k > best_k:
                best, best_k = s, k
        self.fs_park = best
        self.fs_park_key = (E.x, E.y)
        return best

    # ------------------------------------------------------------------
    # the ring census
    # ------------------------------------------------------------------

    def _fs_kill_window(self, ct, E):
        """Is the kill actually running?  A live sentinel plus banked ammo."""
        try:
            if ct.get_global_ammo() < FS_AMMO_KILL_MIN:
                return False
        except Exception:
            return False
        return self._fs_live_sentinels(ct, E) >= 1

    def _fs_denied(self, ct, t):
        """Is this ring tile already denied BY US?

        Denied means: a blocking building of ours stands on it, or one of our
        own bodies does.  An ENEMY building on a ring tile is NOT denial -- it
        is a target: it blocks our barrier while doing nothing to their heal
        line.  Unreadable (out of vision) counts as NOT denied, which is the
        conservative direction: the cost is one wasted walk, against the cost
        of banking a partial seal, which INVERTS.
        """
        if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
            return True                      # off-map: nothing can spawn there
        try:
            bid = ct.get_tile_building_id(t)
            if bid is not None:
                if ct.get_team(bid) != self.team:
                    return False
                return ct.get_entity_type(bid) in FS_BLOCKING
            oid = ct.get_tile_builder_bot_id(t)
            if oid is not None and ct.get_team(oid) == self.team:
                return True
        except Exception:
            return False
        return False

    def _fs_enemy_bld(self, ct, t):
        """Is an ENEMY building standing on this tile?  (v514 change C.)"""
        try:
            bid = ct.get_tile_building_id(t)
            if bid is None:
                return False
            return ct.get_team(bid) != self.team
        except Exception:
            return False

    def _fs_census(self, ct, E):
        """(needed, orth_open) for the 12-tile ring, from live vision."""
        ring, seats = self._fs_ring12(E)
        park = self._fs_park_seat(ct, E)
        cands = []
        orth_open = 0
        seatset = set((s.x, s.y) for s in seats)
        # ⭐⭐ v514 CHANGE C -- LAUNCHER COVERAGE COMPLETES THE COLLAR.  A seat
        # carrying the DEFENDER'S OWN BUILDING can never take a barrier
        # (`can_build_barrier` refuses it forever) and it is where the closure
        # failure lives: atoll and midgard closed 0 of 12 in the fired v513
        # arm, and 6 of 9 / 14 of 27 closure-binding seats were enemy buildings
        # placed there because their ore sits at chebyshev d=2/d=3 of their own
        # core.  What a launcher CAN do is keep the seat empty of healers -- a
        # conveyor is bot-passable, so a healer stands ON the belt and heals
        # (Magnus, 2026-08-18).  A covered unsealable seat is therefore denied
        # as a HEAL STATION, which is the only sense in which the collar ever
        # mattered.
        # ⛔ ONLY unsealable seats.  A seat we could barrier stays rung 1's --
        # counting coverage there would stop us sealing what we can seal, which
        # inverts Magnus's priority 1.
        cover = ()
        if LOKI_FS_V514 and FS_V514_DENYSITE and FS_DENY_SEAT_CENSUS:
            cover = self._fs_evict_cover(ct, E)
        for t in ring:
            if self._fs_denied(ct, t):
                continue
            is_seat = (t.x, t.y) in seatset
            # ⛔ COVERAGE CLOSES THE CENSUS, IT DOES NOT CLOSE THE WORK.  The
            # first form of this clause dropped a covered seat out of `needed`
            # entirely and that is wrong twice over: rung 3 stops pecking the
            # belt off it (the autopsy measured clears converting 100% of the
            # time they land) and rung 1 never barriers it if the belt dies.
            # What coverage buys is that the seat no longer holds `orth_open`
            # above zero -- a healer standing there gets thrown off it, which
            # is the only thing `orth_open` was ever a proxy for.
            covered = bool(cover) and is_seat and (t.x, t.y) in cover \
                and self._fs_enemy_bld(ct, t)
            if covered:
                self.fs_cov_denied += 1
            if is_seat and not covered:
                orth_open += 1
            if park is not None and t.x == park.x and t.y == park.y:
                continue                     # reserved for our own body
            cands.append((is_seat, t, self._fs_body_blocked(ct, t)))
        if LOKI_FS_SEAL_ONLY:
            # ⚠ REGISTERED DEVIATION (doctrine.py, LOKI_FS_SEAL_ONLY block).
            # v510 defers the diagonals to the kill window; under seal-only
            # there is no raider-built kill asset to wait for, so that gate
            # would defer them forever and leave the body idle on the park seat
            # with a full bank.  They open instead the moment every orthogonal
            # seat but the park seat is denied -- i.e. the orthogonal-8 first,
            # exactly as before, and the diagonals only as an extension of a
            # finished collar.  The provocation hazard this imports is named in
            # the doctrine block and is the prereg's to price.
            #
            # ⛔ "EVERY SEAT DENIED **OR UNBUILDABLE**", not "every seat
            # denied".  MEASURED on the headline fixture (midgard seed 21 vs
            # `_v488beltbreak2`): three of the eight orthogonal seats --
            # (25,27), (26,25), (27,25) -- carried the DEFENDER'S OWN CONVEYOR
            # from before our arrival and `can_build_barrier` refused them for
            # the rest of the match.  A conveyor is bot-passable, so it is not
            # denial; it is also not clearable, because clearing is a verb this
            # flag removes.  With a strict "all seats denied" gate the raider
            # stood beside (25,27) from r76 to its death with a full bank and
            # NOTHING to do.  The gate therefore asks whether any ACTIONABLE
            # orthogonal work is left, and the ordering still puts seats ahead
            # of diagonals, so a seat that later clears is taken first.
            diag_ok = not any(is_seat and not bl for is_seat, _t, bl in cands)
        else:
            diag_ok = (not FS_DIAG_DEFER) or self._fs_kill_window(ct, E)
        needed = []
        for is_seat, t, bl in cands:
            if not is_seat and not diag_ok \
                    and not (t.x == E.x - 1 and t.y == E.y - 1):
                # A DIAGONAL, and the kill window is not open yet.  Closing the
                # eight orthogonals already zeroes their heal rate -- those are
                # the whole heal set -- while a full TWELVE-seal is broken in a
                # median of 9 rounds against 56 for a >=8 partial.  The one
                # diagonal worth provoking early is the NW tile, which takes
                # 19.6% of all spawns on its own.
                continue
            needed.append((0 if is_seat else 1, t, bl))
        # Orthogonal seats first (they are the ONLY heal stations).  Within
        # them, NW-ADJACENT FIRST: the spawn set is exactly this ring
        # (59,121/59,121) and it carries a 20.28% NW-corner bias -- the field's
        # own `for d in Direction` order showing through -- so a barrier on the
        # north/west seats pre-empts a fifth of their spawns during the race.
        # Then the far-from-park tiles, so the walk ENDS at the park seat
        # rather than starting there.
        px, py = (park.x, park.y) if park is not None else (E.x, E.y)

        tries = self.fs_tile_builds
        cleared = self.fs_cleared if (LOKI_FS_SEAL_ONLY
                                      and LOKI_FS_RING_LADDER) else {}
        try:
            rnow = ct.get_current_round()
        except Exception:
            rnow = 0

        def _order(it):
            pr, t, blocked = it
            # A SEAT WE JUST PECKED CLEAR OUTRANKS EVERYTHING ELSE BUILDABLE.
            # The defender rebuilt those belts in v510; the barrier has to land
            # in the window we opened, not after a lap of the collar.
            fresh = 0 if cleared.get((t.x, t.y), -10 ** 9) \
                >= rnow - FS_CLEAR_HOLD else 1
            nw = 0
            if FS_SEAL_NW_FIRST:
                nw = -((1 if t.y < E.y else 0) + (1 if t.x < E.x else 0))
            # A tile the defender has already pecked open FS_REBUILD_MAX times
            # keeps its place in the list but loses its priority, so the rest of
            # the ring gets finished before we feed it another barrier.
            worn = 1 if tries.get((t.x, t.y), 0) >= FS_REBUILD_MAX else 0
            # ⛔ A TILE WITH AN ENEMY BODY ON IT IS NOT BUILDABLE THIS ROUND AND
            # A BUILDER CANNOT SHOOT A BUILDER.  Measured: the raider chose one
            # such tile as its station, `can_build_barrier` refused every round,
            # `_fs_stand_target` kept answering "you are already in place", and
            # the body sat there being shot until it died with five ring tiles
            # untouched.  Squatters are the EVICTION LAUNCHER's job; the raider
            # walks past them and seals what it can.
            return (blocked, fresh, worn, pr, nw,
                    -((t.x - px) ** 2 + (t.y - py) ** 2))

        needed.sort(key=_order)
        self.fs_blocked_now = frozenset(
            (t.x, t.y) for _pr, t, bl in needed if bl)
        return [t for _pr, t, _bl in needed], orth_open

    def _fs_body_blocked(self, ct, t):
        """Is this needed tile un-buildable by something we will not remove?

        ⛔ SEAL-ONLY WIDENS THIS, and the reason is the squatted-seat trap.  In
        v510 an enemy BUILDING on a ring tile was `_fs_try_clear`'s job, so it
        was a target and not an obstacle; under seal-only that verb is gone and
        nothing will ever shift it.  Left ranked as an ordinary open tile it
        becomes the nearest one, `_fs_stand_target` answers "you are already in
        place" for ever, `can_build_barrier` refuses every round, and the body
        dies there with the rest of the ring untouched -- which is exactly how
        v510's squatted-seat surprise played out with an enemy BODY.  Marking
        it blocked keeps it in `needed` (it is still an open heal seat, and the
        census must say so) while sending it to the BACK of both the build order
        and the walk order: seal everything else, come back if it clears.
        """
        try:
            oid = ct.get_tile_builder_bot_id(t)
            if oid is not None and ct.get_team(oid) != self.team:
                # ⭐⭐ VERIFIED ON THE ENGINE, s50 (probe P6, this build's
                # `scratchpad/ringladder_build/_p6`, 1,438 adjacency readings
                # over 8 local games, BOTH VERDICTS PRESENT):
                #   enemy BODY on the seat, no building, barrier affordable
                #       -> can_build_barrier FALSE in **40 of 40**
                #   empty seat, barrier affordable  (the control)
                #       -> can_build_barrier TRUE  in **383 of 383**
                # AN ENEMY BUILDER BODY BLOCKS THE BARRIER.  It was previously
                # inferred here from one v510 game; it is now measured.  The
                # consequence is a LADDER ORDER fact, not a comment: on a
                # body-held seat, EVICTION IS A PRECONDITION OF SEALING, and
                # the ladder gets that right only because rung 1 fails on such a
                # tile (can_build_barrier is False) and `_fs_seal_pending`
                # excludes blocked tiles from the wait -- so the round falls
                # through to rung 2, which is the evictor.  Do not "optimise"
                # either of those two clauses away.
                return 1
            if LOKI_FS_SEAL_ONLY:
                key = (t.x, t.y)
                bid = ct.get_tile_building_id(t)
                if bid is None:
                    # ⭐ THE SEAT JUST CLEARED.  Under the ladder a seat we have
                    # been pecking and that now reads empty gets FS_CLEAR_HOLD
                    # rounds of queue priority, so the barrier lands before the
                    # defender puts the belt back -- Magnus: "peck conveyors at
                    # their core and REPLACE WITH BARRIERS".
                    if LOKI_FS_RING_LADDER and self.fs_tile_pecks.get(key):
                        self.fs_tile_pecks[key] = 0
                        self.fs_cleared[key] = ct.get_current_round()
                        self.fs_cleared_n += 1
                        self._fs_log("CLEARED", ct.get_current_round(),
                                     "tile", key, "n", self.fs_cleared_n)
                elif ct.get_team(bid) == self.team:
                    return 1            # ours: not clearable, not buildable
                elif self._fs_pecks(ct, key) >= FS_CLEAR_MAX_PECKS:
                    return 1            # peck budget spent: defer this seat
        except Exception:
            return 0
        return 0

    # ------------------------------------------------------------------
    # THE RAIDER'S TURN
    # ------------------------------------------------------------------

    def _fs_turn(self, ct):
        rnd = ct.get_current_round()
        E = self._enemy_anchor(ct)
        if E is None or not self._fs_active(ct):
            self._fs_degrade(ct, rnd)
            return
        p = ct.get_position()
        d = dsq_core(p, E)

        # NO-ROUTE DEGRADE.  jackpot: the probe's ferry never arrived there on
        # any hop budget, and a plank that cannot reach the ring must not keep
        # spending launchers trying.  Measured as progress, not as a map name.
        if self.fs_best is None or d < self.fs_best:
            self.fs_best, self.fs_best_rnd = d, rnd
        elif (not self.fs_arrived and d > FS_RING_DSQ
                and rnd - self.fs_best_rnd > FS_NOPROG_RNDS):
            # ⛔ THE WATCHDOG IS FOR THE APPROACH ONLY, and `self.fs_arrived`
            # is what says so.  Without that clause a raider that had reached
            # the ring, sealed six of eight seats and then stepped one tile
            # wide of FS_RING_DSQ for thirty rounds -- which is ordinary work,
            # the collar is a closed curve and you walk round the outside of it
            # -- read as "no route to the enemy" and abandoned a siege that was
            # ONE TILE from closing.  Measured at r145 on midgard seed 4.
            self._fs_degrade(ct, rnd)
            return

        if d <= FS_RING_DSQ:
            if self.fs_ring_rnd is None:
                self.fs_ring_rnd = rnd
                # v514 change D instrument: the arrival table the probe's
                # b1/b2 medians are read off.  FS_LOG-gated, so no ship cost.
                self._fs_log("ARRIVE", rnd, "id", ct.get_id(),
                             "body", getattr(self, "fs_body", 1),
                             "at", (p.x, p.y), "dsq", d)
            self.fs_arrived = True
        at_ring = self.fs_arrived and d <= FS_RING_HOLD_DSQ
        if at_ring:
            needed, orth_open = self._fs_census(ct, E)
            # KILL outranks SEALED, and it is not a cosmetic ordering: the Core
            # reads this phase to decide how much of the bank the magazine may
            # have.  A live sentinel with an unfinished collar is still the
            # state in which AMMUNITION is the clock -- the first integrated
            # run finished r20 with a sentinel standing and SIX ammunition,
            # because the phase said RING and the Core was still saving for a
            # sentinel it had already bought.
            if orth_open == 0:
                # ⭐ v513 change A: the SALT LATCH, refreshed every round the
                # collar reads closed -- `_fs_salt_ok` is then a pure predicate
                # and cannot depend on which rung happened to ask it.
                self.fs_sealed_rnd = rnd
            if self._fs_live_sentinels(ct, E):
                phase = FS_PH_KILL
                if LOKI_FS_V514 and FS_V514_ECOGATE \
                        and self.fs_sealed_rnd is None:
                    # A turret bought under Magnus ruling 2 with the collar
                    # still open.  The Core needs to know, because every
                    # magazine floor below FS_PH_KILL was written for a state
                    # that could only be reached AFTER a closure.
                    phase = FS_PH_KILL_OPEN
            elif orth_open == 0:
                phase = FS_PH_SEALED
            else:
                phase = FS_PH_RING
        else:
            needed, orth_open, phase = None, None, FS_PH_FERRY
        if FS_V517_TWIN_LOG:
            # v517 change 2's REACHABILITY instrument, and it is deliberately
            # on the RAIDER, not on the purchase: the plank can only land in a
            # round where a body of ours is alive at the ring WHILE a sentinel
            # is holding.  A hold with no TWINGATE line in the same round is a
            # hold nobody could spend.
            try:
                if self._fs_hold_live(ct):
                    print("TWINGATE517", rnd, "atring", 1 if at_ring else 0,
                          "live", self._fs_live_sentinels(ct, E),
                          "ti", ct.get_global_resources(),
                          "ammo", ct.get_global_ammo(),
                          "cost", ct.get_sentinel_cost(),
                          "bought", ct.read_store(SLOT_FWD_GUN),
                          "orth", orth_open, file=sys.stderr)
            except Exception:
                pass
        self._fs_publish(ct, rnd, phase, ct.get_id())
        if LOKI_FS_CREW:
            # The crew heartbeat: dedicated bits, one writer per seat, so a
            # chassis raider at the ring can no longer keep the successor door
            # shut (the v511 defect note at `_fs_stale`).
            self._fs_crew_publish(ct, 1 if self.fs_role == "supp" else 0, rnd)
            if (FS_CREW_ON and self.fs_role == "supp"
                    and self._fs_crew_age(ct, 0, rnd) > FS_CREW_STALE):
                # ⭐ ROLE-CONVERT, the cheapest replacement there is: the sealer
                # is gone and this body is already at the ring, so it takes the
                # collar over this round instead of waiting for a spawn to walk
                # the whole map.  The support seat then reads stale and the
                # ordinary door appoints a new one.
                self.fs_role = "seal"
                self._fs_log("PROMOTE", rnd, "id", ct.get_id())

        if phase != self.fs_last_phase:
            self._fs_log("PHASE", rnd, "id", ct.get_id(), "ph", phase,
                         "d", d, "at", (p.x, p.y))
            self.fs_last_phase = phase

        if at_ring and FS_LOG and rnd % 20 == 0:
            try:
                self._fs_log("STAT", rnd, "id", ct.get_id(), "at", (p.x, p.y),
                             "need", len(needed), "orth", orth_open,
                             "ti", ct.get_global_resources(),
                             "ammo", ct.get_global_ammo(),
                             "sen", self._fs_live_sentinels(ct, E),
                             "hp", ct.get_hp(),
                             "covden", self.fs_cov_denied,
                             "eco", 1 if self._fs_eco_gate_ok(ct) else 0,
                             "lost", self.fs_sent_lost)
            except Exception:
                pass

        if at_ring:
            self._fs_ring_turn(ct, E, p, rnd, needed, orth_open)
        else:
            self._fs_ferry_turn(ct, E, p, rnd)

    def _fs_degrade(self, ct, rnd):
        """Hand this body back to the incumbent raid doctrine, for good."""
        self.fs_off = True
        self._fs_log("DEGRADE", rnd, "id", ct.get_id())
        try:
            _beat, ph, _rid = self._fs_state(ct)
            if ph != FS_PH_DEGRADE:
                self._fs_publish(ct, rnd, FS_PH_DEGRADE, 0)
        except Exception:
            pass
        self._raid(ct)

    # --- C. the ferry ------------------------------------------------------

    def _fs_ferry_turn(self, ct, E, p, rnd):
        T = self._fs_target(ct, E)
        lp = self._fs_pickup_launcher(ct, p)
        if self.fs_body_born is None:
            self.fs_body_born = rnd

        if lp is not None:
            # A ferry launcher is already standing beside us and it acts LATER
            # this round (turn order is entity-id ascending and it is younger
            # than us).  The only thing worth doing with our own turn is a free
            # tile of progress that keeps us inside its d^2<=2 pickup envelope.
            self.fs_ride_rnd = rnd
            if FS_HOP_STEP_ON and ct.get_move_cooldown() == 0:
                self._fs_hop_step(ct, p, lp, T)
            return

        # ⭐ v514 CHANGE D -- THE RELAY (Magnus, s51: "both builders need to be
        # launched before the launcher can be destroyed and a new launcher can
        # be built").  ONE chain, two riders: body 1 buys every link and body 2
        # rides it, so a hop costs one launcher instead of two and the bodies
        # travel one round apart instead of three.  The as-built crew built two
        # PARALLEL chains three rounds apart down identical tiles -- that is
        # the drakkarfjord r197 arrival the probe took to r14.
        # ⛔ INERT IN THE FIRED CONFIG: with FS_CREW_ON False there is one body,
        # `fs_body` is 1 and `_fs_relay_mustered` returns True on its first
        # line, so this whole block reduces to the parent's.
        may_build = True
        relay = LOKI_FS_V514 and FS_V514_RELAY and FS_RELAY_ON \
            and LOKI_FS_CREW and FS_CREW_ON
        if relay and getattr(self, "fs_body", 1) == 1 and self.fs_ride_rnd is None:
            # THE MUSTER -- FIRST LINK ONLY.  Measured on the probe's first
            # relay smoke run: the steady state is self-sustaining, but the
            # first link cannot reach it because the lead spawns a round before
            # body 2 and the chain then leaves at ~2.5 tiles a round against a
            # walk of 1.  Body 2 was never once inside a pickup envelope and
            # walked the whole map.
            if not self._fs_relay_mustered(ct, p, rnd):
                return
        if relay and getattr(self, "fs_body", 1) == 2:
            since = rnd - (self.fs_ride_rnd if self.fs_ride_rnd is not None
                           else self.fs_body_born)
            may_build = since >= FS_RELAY_PATIENCE
            if not may_build:
                lv = self._fs_relay_point(ct, p, E)
                if lv is not None:
                    if ct.get_move_cooldown() == 0:
                        self.tgt = lv
                        self._nav(ct, pave=False)
                    return
        if may_build and ct.get_action_cooldown() == 0 \
                and self._fs_build_ferry(ct, p, T):
            return
        # No launcher and none affordable: walk.  The ferry is a speed-up,
        # never a prerequisite.
        if ct.get_move_cooldown() == 0:
            self.tgt = T
            self._nav(ct, pave=False)

    def _fs_relay_mustered(self, ct, p, rnd):
        """May the LEAD buy its first link yet?  (v514 change D.)

        True once body 2 is within FS_MUSTER_DSQ, or after FS_MUSTER_WAIT
        rounds -- the patience clause is what stops a body 2 that was never
        appointed, or died in the opening, from stalling the siege outright.
        """
        if not (LOKI_FS_V514 and FS_V514_RELAY and FS_RELAY_ON
                and LOKI_FS_CREW and FS_CREW_ON):
            return True
        if rnd - self.fs_body_born >= FS_MUSTER_WAIT:
            return True
        _b, _ph, rid = self._fs_state_at(ct, FS_SUPP_SLOT)
        if not rid:
            return False                     # body 2 has not reported at all
        if _b and rnd - (_b - 1) > FS_CREW_STALE:
            # Body 2 reported once and has stopped: it is dead and there is
            # nothing to muster for.  Without this a REPLACEMENT lead waits out
            # the whole patience for a crew mate that no longer exists.
            return True
        want = rid - 1
        try:
            for eid in ct.get_nearby_units():
                if eid != want:
                    continue
                if ct.get_team(eid) != self.team:
                    continue
                return ct.get_position(eid).distance_squared(p) <= FS_MUSTER_DSQ
        except Exception:
            return True                      # blind: do not stall on a getter
        return False

    def _fs_relay_point(self, ct, p, E):
        """The tile body 2 walks to in order to catch the relay: a passable
        neighbour of the nearest friendly FERRY launcher in vision.

        A launcher inside FS_RING_DSQ of the ENEMY core is an EVICTOR and never
        a ferry -- the same role-by-site rule `_fs_launcher_turn` opens with.
        Bounds are checked explicitly (`is_in_vision` is a pure radius test).
        """
        best = None
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.LAUNCHER:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                bp = ct.get_position(bid)
                if dsq_core(bp, E) <= FS_RING_DSQ:
                    continue
                d = bp.distance_squared(p)
                if best is None or d < best[0]:
                    best = (d, bp)
        except Exception:
            return None
        if best is None:
            return None
        lp = best[1]
        want, want_d = None, None
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1),
                       (1, 1), (1, -1), (-1, 1), (-1, -1)):
            tx, ty = lp.x + dx, lp.y + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            try:
                if not ct.is_tile_passable(t):
                    continue
            except Exception:
                continue
            d = t.distance_squared(p)
            if want_d is None or d < want_d:
                want, want_d = t, d
        return want

    def _fs_pickup_launcher(self, ct, p):
        """Position of a friendly launcher that could pick us up, or None."""
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.LAUNCHER:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                bp = ct.get_position(bid)
                if bp.distance_squared(p) <= 2:
                    return bp
        except Exception:
            return None
        return None

    def _fs_build_ferry(self, ct, p, T):
        """Build the next hop's launcher on our own forward tile."""
        try:
            cost = ct.get_launcher_cost()
            if ct.get_global_resources() < cost + FS_LAUNCHER_TI_FLOOR:
                return False
        except Exception:
            return False
        ban = self._home_seat_keys_set()     # never seat one on OUR heal seats
        here = p.distance_squared(T)
        best, best_d = None, None
        for dx, dy in CARD_DELTAS:
            bx, by = p.x + dx, p.y + dy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            if (bx, by) in ban:
                continue
            bp = Position(bx, by)
            d = bp.distance_squared(T)
            if d > here:
                continue                     # never a launcher pointing home
            if best_d is not None and d >= best_d:
                continue
            try:
                if not ct.can_build_launcher(bp):
                    continue
            except Exception:
                continue
            best, best_d = bp, d
        if best is None:
            return False
        try:
            ct.build_launcher(best)
        except Exception:
            return False
        self._fs_draw_dot(ct, best, 0, 200, 255)
        self._fs_draw_line(ct, best, T, 0, 120, 255)
        self._fs_log("HOPBUILD", ct.get_current_round(), "at", (p.x, p.y),
                     "lch", (best.x, best.y), "T", (T.x, T.y))
        return True

    def _fs_hop_step(self, ct, p, lp, T):
        """One free tile forward that keeps us inside the pickup envelope."""
        here = p.distance_squared(T)
        want, best_d = None, None
        for i, (dx, dy) in enumerate(CARD_DELTAS):
            nx, ny = p.x + dx, p.y + dy
            if not (0 <= nx < self.mw and 0 <= ny < self.mh):
                continue
            n = Position(nx, ny)
            if n.distance_squared(lp) > 2:
                continue                     # would leave the pickup envelope
            d = n.distance_squared(T)
            if d >= here:
                continue
            if best_d is not None and d >= best_d:
                continue
            try:
                if not ct.can_move(CARDINALS[i]):
                    continue
            except Exception:
                continue
            want, best_d = CARDINALS[i], d
        if want is None:
            return
        try:
            ct.move(want)
        except Exception:
            return

    # --- A. THE REACTIVE DODGE (LOKI_FS_RING_LADDER) ------------------------

    def _fs_threat_tiles(self, ct, rnd):
        """Tiles a LOCATED enemy turret's firing line covers, with memory.

        ⭐ READ OFF THE ENGINE, NEVER INFERRED FROM DAMAGE.
        `get_attackable_tiles_from(pos, dir, kind)` is the engine's own
        hypothetical-turret pattern -- the same call `_fs_gun_axis` uses for the
        static stand-tile blacklist.  The difference is the MEMORY: a turret we
        saw four rounds ago is still pointed where it was pointed, and a dodge
        that forgets the ray the instant the turret drops out of vision steps
        straight back onto it.  Entries older than FS_DODGE_MEMORY expire,
        because a gunner that rotated is a ray that moved.

        Returns {(x, y): number of turrets whose line covers it}.
        """
        try:
            for bid in ct.get_nearby_buildings():
                kind = ct.get_entity_type(bid)
                if kind not in (EntityType.GUNNER, EntityType.SENTINEL):
                    continue
                if ct.get_team(bid) == self.team:
                    continue
                gp = ct.get_position(bid)
                gd = ct.get_direction(bid)
                seen = {}
                for t in ct.get_attackable_tiles_from(gp, gd, kind):
                    seen[(t.x, t.y)] = 1
                if LOKI_FS_CREW and FS_PRESTAND_AVOID \
                        and kind == EntityType.SENTINEL:
                    # ⭐⭐ A SENTINEL RAY IS PERMANENT INFORMATION AND v512 THREW
                    # IT AWAY EVERY FIVE ROUNDS.  Sentinels CANNOT ROTATE (only
                    # gunners can: `rotate()` is gunner-only, official-docs
                    # 227/257/282), so a sentinel's facing is fixed for its
                    # whole life and the tiles it covers never move.
                    # FS_DODGE_MEMORY exists because a GUNNER that rotated is a
                    # ray that moved -- that reason does not exist here.  22 of
                    # the 23 raider deaths were on a tile already seen on a ray
                    # of the very turret that fired, and 20 of 23 had LEFT that
                    # tile and walked back onto it.  Expiring this memory is
                    # what let them.
                    for k in seen:
                        self.fs_sray[k] = 1
                if LOKI_FS_V514 and FS_V514_RESITE \
                        and kind == EntityType.GUNNER:
                    # v514 change B: a GUNNER line is remembered too, but only
                    # for SITING and only for FS_RAY_GUN_MEM rounds -- a gunner
                    # can rotate for 10 Ti and a cooldown, so its ray is soft
                    # information where a sentinel's is permanent.
                    for k in seen:
                        self.fs_gray[k] = rnd
                for k in seen:
                    prev = self.fs_threat.get(k)
                    n = 1 if (prev is None or prev[0] != rnd) else prev[1] + 1
                    self.fs_threat[k] = (rnd, n)
        except Exception:
            pass
        live = {}
        for k in list(self.fs_threat.keys()):
            r, n = self.fs_threat[k]
            if rnd - r > FS_DODGE_MEMORY:
                del self.fs_threat[k]
            else:
                live[k] = n
        return live

    def _fs_hit_mark(self, ct, p, hit):
        """Remember the TILE we were hit on, permanently.

        Narrower than the ray and that is deliberate: a full-ray veto refuses
        the only station beside the last needed seat and stops the collar dead
        (measured: the nordkap raider was at `need 1`, with the bank open, when
        it entered the loop).  A tile we have actually BLED on is a much smaller
        set and it is the one the deaths are on -- fatal tile == penultimate-hit
        tile in 19 of 23.
        """
        if hit:
            self.fs_hit_tiles[(p.x, p.y)] = 1

    def _fs_try_dodge(self, ct, E, p, live, hit):
        """ONE perpendicular cardinal step off the line.  Outranks every rung.

        ⛔ THE RULE IS MAGNUS'S AND IT IS ABSOLUTE FOR THE ROUND: "if a sentinel
        starts shooting the builder we need to move it".  Acting and moving are
        mutually exclusive for a builder bot, so a dodge costs exactly one
        barrier -- against a body that in the v510 demo stood at <=8 HP for 222
        rounds and then died on a tile it had watched get shot four times.

        Two triggers, and they are deliberately different in strictness:
          * HP FELL since our last turn -- we are being hit RIGHT NOW, possibly
            by something we cannot see, so ANY legal step that is not onto a
            worse-covered tile is taken (a step breaks an unlocated line too).
          * WE ARE STANDING ON A KNOWN RAY and were not hit -- only a STRICT
            improvement in coverage is worth the round, otherwise the body
            would jitter for ever beside a turret that is reloading.
        Preference among equals: stay ring-adjacent, so we come back next round.
        """
        try:
            if ct.get_move_cooldown() != 0:
                return False
        except Exception:
            return False
        here = live.get((p.x, p.y), 0)
        if hit and here == 0:
            # ⛔ THE BARE-HIT TRIGGER MUST NOT ABANDON A DENIED SEAT.  We are
            # taking damage from something we cannot locate, so there is no line
            # to break by construction -- and if we are STANDING ON a ring tile,
            # our body IS the denial on it (P3: a body denies spawn exactly like
            # a barrier).  Stepping off for an unlocated shooter re-opens a heal
            # seat to buy nothing.  Measured across four 30-game arms: the bare
            # hit trigger unguarded cost 44 raider deaths and 11.3% of ring
            # body-rounds at <=10 HP, against 27 and 2.6% with it disabled
            # outright; this guard is the version that keeps Magnus's rule where
            # it can act and drops it where it cannot.
            ring, _seats = self._fs_ring12(E)
            if any(t.x == p.x and t.y == p.y for t in ring):
                return False
        best, best_k, best_d = None, None, None
        for i, (dx, dy) in enumerate(CARD_DELTAS):
            nx, ny = p.x + dx, p.y + dy
            if not (0 <= nx < self.mw and 0 <= ny < self.mh):
                continue
            n = Position(nx, ny)
            if self._fs_wall(n):
                continue
            cov = live.get((nx, ny), 0)
            if cov > here:
                continue                     # never step onto a worse ray
            if not hit and cov >= here:
                continue                     # no strict break: not worth a round
            try:
                if not ct.can_move(CARDINALS[i]):
                    continue
            except Exception:
                continue
            dc = dsq_core(n, E)
            k = (cov, 0 if dc <= FS_RING_DSQ else 1, dc)
            if best_k is None or k < best_k:
                best, best_k, best_d = n, k, CARDINALS[i]
        if best is None:
            return False
        try:
            ct.move(best_d)
        except Exception:
            return False
        self.fs_dodges += 1
        self._fs_log("DODGE", ct.get_current_round(), "id", ct.get_id(),
                     "from", (p.x, p.y), "to", (best.x, best.y),
                     "cov", here, "->", best_k[0], "hit", 1 if hit else 0,
                     "hp", ct.get_hp())
        self._fs_draw_dot(ct, best, 0, 255, 255)
        return True

    # --- D/E. the ring: evict, then seal, then kill -------------------------

    def _fs_ring_turn(self, ct, E, p, rnd, needed, orth_open):
        if LOKI_FS_CREW and FS_CREW_ON and self.fs_role == "supp":
            self._fs_supp_turn(ct, E, p, rnd, needed, orth_open)
            return
        if LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER:
            self._fs_ladder_turn(ct, E, p, rnd, needed, orth_open)
            return
        act = ct.get_action_cooldown() == 0
        ti = ct.get_global_resources()
        # ⛔ SEAL-ONLY: the whole verb list below collapses to step 2.  This is
        # not a tidy-up -- a builder gets ONE action a round and acting blocks
        # moving, so in v510 every eviction launcher, every sentinel, every
        # clear-peck and every repair was a round the collar did not close (0/13
        # games closed the orthogonal-8, best 7/8).  The observation pass is
        # skipped too: `fs_healer_hist` feeds nothing but the eviction siting.
        seal_only = LOKI_FS_SEAL_ONLY
        if FS_EVICT_ON and not seal_only:
            self._fs_observe_healers(ct, E)

        if act:
            # 1. THE EVICTION LAUNCHER IS THE SEAL'S PRECONDITION, NOT ITS
            #    GARNISH.  Defenders parked on ring tiles make those tiles
            #    unbuildable -- in the probe's spawning-victim run 3 of 12 tiles
            #    were permanently body-blocked and the seal capped at 4/12.
            if FS_EVICT_ON and not seal_only \
                    and self._fs_try_evict_launcher(ct, E, p, ti):
                return
            # 2. THE SEAL FIRST, AND THE REASON IS SURVIVAL, NOT ECONOMY.
            #    The chassis's own raid doctrine already says it: "a barrier is
            #    placed on the first action after landing (value that outlives
            #    the body)".  Measured on this tree's midgard run against the
            #    incumbent, the raider lands at r14 and is dead at r18 -- four
            #    actions.  Spending the first of them on a turret it may not
            #    live to protect leaves NOTHING behind; spending them on
            #    barriers leaves four tiles of the heal set closed for the rest
            #    of the match, and the next raider inherits them.
            if FS_SEAL_ON and self._fs_try_seal(ct, E, p, needed, ti):
                return
            # 3. THE KILL WHEN IT HAS WAITED LONG ENOUGH.  A contested near
            #    face keeps `needed` non-empty indefinitely -- measured on the
            #    first integrated run, the defender pecked one seat open every
            #    ~8 rounds -- so "seal first, always" degenerates into never
            #    buying the only thing that ever wins.  Past FS_SENTINEL_RND
            #    with no turret up, the turret jumps the queue.
            urgent = (not seal_only
                      and ct.get_current_round() >= FS_SENTINEL_RND
                      and self._fs_live_sentinels(ct, E) == 0)
            if urgent and self._fs_sentinel_ok(ct, ti, needed, orth_open) \
                    and self._fs_try_sentinel(ct, E, p):
                return
            # 4. THE KILL on the ordinary schedule: the orthogonals are
            #    closed, or the bank pays for the turret AND every barrier
            #    still owed.
            if not seal_only \
                    and self._fs_sentinel_ok(ct, ti, needed, orth_open) \
                    and self._fs_try_sentinel(ct, E, p):
                return
            # 5. Clear an enemy building squatting on a ring tile we need.
            #    ⭐ THE ONE NON-BARRIER ACTION SEAL-ONLY KEEPS, and it is kept
            #    because it is a PRECONDITION OF SEALING rather than a rival to
            #    it.  Measured on the headline fixture: three of the eight
            #    orthogonal seats -- (25,27), (26,25), (27,25) on midgard --
            #    carried the DEFENDER'S OWN CONVEYORS from before our arrival,
            #    `can_build_barrier` refused them for the whole match, and with
            #    clearing fully off the collar could never close on that map at
            #    all.  A conveyor is 20 HP = ten 2-damage pecks; the budget is
            #    capped per tile (FS_CLEAR_MAX_PECKS) so a defended seat cannot
            #    eat the whole match -- v510 spent 30 rounds and 60 Ti on three
            #    of them.  Past the cap the tile is scored BLOCKED, drops to the
            #    back of both the build and the walk order, and is retried only
            #    when there is nothing else on the ring to do.
            if self._fs_try_clear(ct, E, p, needed):
                return
            # 6. Peck the core from a seat.  Worth 2 dmg/round ONLY because the
            #    seal makes it permanent -- never the plank's kill (2 dmg loses
            #    to one builder healing +4).
            #    (Inert in this tree either way -- LOKI_QUIET_ON is True, so
            #    `_fs_try_peck` already returns False on its first line.  The
            #    seal-only clause is here so the verb list reads honestly.)
            if not seal_only and orth_open == 0 and self._fs_try_peck(ct, E, p):
                return
            # 7. Repair our own collar -- ONLY when it is finished, or when a
            #    barrier is about to be lost outright.
            #    ⛔ Measured on the midgard integration run: an unconditional
            #    repair step froze a raider on one tile for SIXTY ROUNDS.  It
            #    healed the barrier beside it every round, the heal consumed the
            #    action, the action blocked the move, and five ring tiles it had
            #    never visited stayed open for the rest of the match.  A repair
            #    that costs a build is not maintenance, it is a stall.
            #    ⛔ AND UNDER SEAL-ONLY THERE IS NO REPAIR AT ALL.  A heal is
            #    +4 HP for 1 Ti and it costs the action; a REBUILD of the tile
            #    the defender actually finished off costs 3 Ti and buys the
            #    whole 30.  With nothing else in the verb list the raider can
            #    afford to let a damaged barrier die and put a fresh one back,
            #    and that is strictly the cheaper use of the one action -- the
            #    repair-freeze surprise (sixty rounds on one tile) cannot recur
            #    because the step does not exist.
            if not seal_only and self._fs_try_repair(ct, p, bool(needed)):
                return

        self._fs_walk(ct, E, p, needed)

    def _fs_walk(self, ct, E, p, needed):
        """The move half of a ring turn -- unchanged from v511, factored out so
        the ladder and the v511 verb list share one walker."""
        if ct.get_move_cooldown() != 0:
            return
        st = self._fs_stand_target(ct, E, p, needed)
        if st is None:
            return
        if st.x == p.x and st.y == p.y:
            return
        self.tgt = st
        self._nav(ct, pave=False)

    # --- B. THE AT-RING PRIORITY LADDER (LOKI_FS_RING_LADDER) ---------------

    def _fs_ladder_turn(self, ct, E, p, rnd, needed, orth_open):
        """Magnus's order, binding per round: take the HIGHEST-priority action
        that is currently legal and funded, and nothing else.

          0. DODGE     -- being shot outranks every rung (see `_fs_try_dodge`)
          1. BARRIER   an empty ring seat
          2. EVICTOR   one cov-sited launcher
          3. CLEAR     peck an enemy conveyor off a seat (then rung 1 seals it)
          4. SENTINEL  two, outside the ring, aligned on a core tile

        ⛔ THE DISCIPLINE IS THE PLANK, NOT THE VERB LIST.  v510 had all five
        verbs and 0/13 closures because one body with one action a round picked
        whichever was cheapest.  Here a lower rung fires only when no higher one
        is ACTIONABLE -- and "actionable" deliberately excludes "affordable this
        round": an open seat we cannot yet pay for is a WAIT, not a licence to
        spend the same bank on a launcher.  That is `_fs_seal_pending`, and it
        rides the same binary-seal arithmetic (`_fs_seal_ok`) that v511 shipped,
        so the two cannot disagree.
        """
        # --- rung 0: the dodge ---------------------------------------------
        hit = False
        hp = None
        try:
            hp = ct.get_hp()
            hit = self.fs_last_hp is not None and hp < self.fs_last_hp
            self.fs_last_hp = hp
        except Exception:
            pass
        if LOKI_FS_CREW:
            self._fs_hit_mark(ct, p, hit)
        if FS_DODGE_ON:
            live = self._fs_threat_tiles(ct, rnd)
            on_ray = (p.x, p.y) in live
            hit_trigger = hit and FS_DODGE_ON_HIT
            if (hit_trigger or on_ray) \
                    and self._fs_try_dodge(ct, E, p, live,
                                           hit_trigger and not on_ray):
                return
        # ⭐ v513 change G: the HP floor.  Below it the body is one sentinel
        # shot from dead (18 damage against a 40 HP builder) and 20 of the 23
        # measured deaths sat at exactly 4 HP for two to four rounds first --
        # there was time to leave every single time.
        if self._fs_try_retreat(ct, E, p, rnd, hp):
            return

        ti = ct.get_global_resources()
        # The eviction siting signal is REACTIVE (48.4% interception against
        # 29.0% for the best fixed tile), so it has to be collected every round
        # the raider is at the ring -- including the rounds rung 1 wins.
        if FS_EVICT_ON:
            self._fs_observe_healers(ct, E)
        # v514 change B: has a sentinel of ours been killed?  (Magnus ruling 2.)
        self._fs_sent_watch(ct, rnd)

        if ct.get_action_cooldown() == 0:
            # rung 1 -- BARRIER.
            if FS_SEAL_ON and self._fs_try_seal(ct, E, p, needed, ti):
                return
            # THE WAIT.  A seat is open and buildable but the collar is not yet
            # paid for: hold the bank.  Spending it one rung down is exactly how
            # a binary seal ends up at 10/12, which measured WORSE than no seal.
            if not self._fs_seal_pending(ct, needed, ti):
                # rung 2 -- ONE EVICTION LAUNCHER, sited by cov over observed
                # healer tiles, Ti-gated above every barrier still owed.
                if FS_EVICT_ON \
                        and self._fs_try_evict_launcher(ct, E, p, ti,
                                                        needed=needed):
                    self._fs_rung(ct, rnd, 2, E, p, needed, ti, orth_open)
                    return
                # rung 3 -- CLEAR a squatting enemy building off a seat.  Rung 1
                # barriers it the same or the next round (the census re-reads
                # denial every round and a just-cleared seat jumps the queue).
                if self._fs_try_clear(ct, E, p, needed):
                    self._fs_rung(ct, rnd, 3, E, p, needed, ti, orth_open)
                    return
                # rung 4 -- THE SENTINELS.  Bottom of the ladder BY DESIGN: it
                # fires on the rounds the collar has nothing actionable left,
                # which are exactly the rounds the raider would otherwise spend
                # walking.  No jump-queue clause is needed (v510 had one) --
                # under the ladder those rounds arrive on their own.
                if self._fs_sentinel_ok(ct, ti, needed, orth_open) \
                        and self._fs_try_sentinel(ct, E, p):
                    self._fs_rung(ct, rnd, 4, E, p, needed, ti, orth_open)
                    return

        self._fs_walk(ct, E, p, needed)

    # --- v513: THE SUPPORT BODY'S TURN (change D + E) -----------------------

    def _fs_supp_turn(self, ct, E, p, rnd, needed, orth_open):
        """The second crew body.  A DIFFERENT verb set, not a second copy.

        ⛔ THE WHOLE POINT IS THAT THE TWO BODIES CANNOT COMPETE FOR THE SAME
        ROUND.  v510 failed because ONE body had five verbs and picked whichever
        was cheapest; v511/v512 fixed that with a strict ladder on one body, and
        the residue the autopsy measured is that one body has neither the
        COVERAGE (40.9% of enemy heals came from seats we never barriered once,
        heal concentration 0.26-0.67 -- a spread leak, not a park seat) nor the
        THROUGHPUT (9 action-rounds out of 48 alive on nordkap_g1).  So the
        support gets the verbs the sealer's ladder starves:

          0. DODGE / RETREAT   -- survival outranks everything (change G)
          2. EVICTOR           -- rung 2, with no seal-wait (change E)
          4. SENTINEL          -- rung 4, but only AFTER the salt (change A)
          -  BODY DENIAL       -- otherwise stand on the seat the sealer is
                                  furthest from: a body denies a seat exactly
                                  like a barrier (P3) and it denies it NOW.

        It never places a barrier and never pecks a seat clear -- those are the
        sealer's, and splitting them is what keeps the ladder's discipline.
        """
        hit = False
        hp = None
        try:
            hp = ct.get_hp()
            hit = self.fs_last_hp is not None and hp < self.fs_last_hp
            self.fs_last_hp = hp
        except Exception:
            hp = None
        self._fs_hit_mark(ct, p, hit)
        if FS_DODGE_ON:
            live = self._fs_threat_tiles(ct, rnd)
            on_ray = (p.x, p.y) in live
            hit_trigger = hit and FS_DODGE_ON_HIT
            if (hit_trigger or on_ray) \
                    and self._fs_try_dodge(ct, E, p, live,
                                           hit_trigger and not on_ray):
                return
        if self._fs_try_retreat(ct, E, p, rnd, hp):
            return

        ti = ct.get_global_resources()
        if FS_EVICT_ON:
            self._fs_observe_healers(ct, E)
        self._fs_sent_watch(ct, rnd)         # v514 change B

        if ct.get_action_cooldown() == 0:
            if FS_EVICT_ON and self._fs_try_evict_launcher(ct, E, p, ti,
                                                           needed=needed):
                self._fs_rung(ct, rnd, 2, E, p, needed, ti, orth_open)
                return
            if self._fs_sentinel_ok(ct, ti, needed, orth_open) \
                    and self._fs_try_sentinel(ct, E, p):
                self._fs_rung(ct, rnd, 4, E, p, needed, ti, orth_open)
                return

        self._fs_supp_walk(ct, E, p, needed)

    def _fs_supp_walk(self, ct, E, p, needed):
        """Body-denial: stand ON the far end of the collar, not beside it.

        A body denies a ring seat exactly like a barrier (P3) and it denies it
        the round it arrives, which is the coverage number this change exists
        for.  ⛔ BUT A BODY ON A SEAT ALSO BLOCKS OUR OWN BARRIER THERE (P6 is
        the enemy-body form of the same engine rule), so the support only
        occupies a seat while there are at least two left -- with one seat to
        go it steps aside and lets the sealer finish the collar permanently.
        """
        try:
            if ct.get_move_cooldown() != 0:
                return
        except Exception:
            return
        order = self._fs_supp_needed(needed)
        if order and len(needed) >= 2 and FS_CREW_DENY_SEAT:
            blocked = self.fs_blocked_now
            for t in order:
                if (t.x, t.y) in blocked:
                    continue
                if t.x == p.x and t.y == p.y:
                    self.fs_supp_seat = (t.x, t.y)
                    return               # already denying it
                try:
                    if not ct.is_tile_passable(t):
                        continue
                except Exception:
                    continue
                self.fs_supp_seat = (t.x, t.y)
                self.tgt = t
                self._nav(ct, pave=False)
                return
        self.fs_supp_seat = None
        self._fs_walk(ct, E, p, order)

    def _fs_supp_needed(self, needed):
        """The support's walk list: the SEALER'S OWN ORDER, REVERSED.

        One shared destination list would put both bodies on the same tile and
        buy nothing.  The sealer sweeps `needed` from the front (NW-first, then
        nearest); the support takes it from the back, so the two cover opposite
        arcs of the same closed curve without exchanging a single store bit.
        """
        if not needed:
            return needed
        return list(reversed(needed))

    def _fs_try_retreat(self, ct, E, p, rnd, hp):
        """⭐ v513 CHANGE G: GET A NEARLY-DEAD BODY OUT OF THE RAY.

        MEASURED: 23 raider deaths in 24 games, EVERY ONE of them to an enemy
        turret (20 sentinel, 3 gunner), and the reactive ray-dodge prevented
        ZERO of them.  A sentinel deals 18 to a 40 HP builder, so a body below
        FS_RETREAT_HP is one shot from dead and a body at 14 HP standing on the
        ring is not denying a seat for long enough to matter.  Walking two tiles
        out and coming back healed is strictly more denial than dying in place
        -- the v510 raider ran 222 rounds under 8 HP and then died on a tile it
        had watched being shot four times.
        """
        if not (LOKI_FS_CREW and FS_RETREAT_ON) or hp is None:
            return False
        if hp > FS_RETREAT_HP:
            self.fs_retreat = False
            return False
        live = self._fs_threat_tiles(ct, rnd)
        here = live.get((p.x, p.y), 0)
        if not here and (p.x, p.y) not in self.fs_sray:
            # ⛔ ALREADY OFF EVERY KNOWN RAY: THERE IS NOTHING TO RETREAT FROM,
            # AND THIS CLAUSE IS THE WHOLE DIFFERENCE BETWEEN A RETREAT AND A
            # TREADMILL.  The first form of this rule walked away while HP was
            # low and waited to heal -- but nothing heals a body at the enemy
            # ring, so it walked out of FS_RING_HOLD_DSQ, the turn dropped to
            # the FERRY branch, the ferry threw it back in, and the phase log
            # read 1,2,1,2 for four hundred rounds (measured on the first smoke
            # run, glacierkeep seed 7301).  A retreat is ONE urgent step off a
            # covered tile, not a mode.
            self.fs_retreat = False
            return False
        try:
            if ct.get_move_cooldown() != 0:
                return False
        except Exception:
            return False
        best, best_k, best_d = None, None, None
        for i, (dx, dy) in enumerate(CARD_DELTAS):
            nx, ny = p.x + dx, p.y + dy
            if not (0 <= nx < self.mw and 0 <= ny < self.mh):
                continue
            n = Position(nx, ny)
            if self._fs_wall(n):
                continue
            # ⛔ AND IT STAYS AT THE RING.  A step past FS_RING_HOLD_DSQ is not
            # a retreat, it is a re-ferry.
            if dsq_core(n, E) > FS_RING_HOLD_DSQ:
                continue
            try:
                if not ct.can_move(CARDINALS[i]):
                    continue
            except Exception:
                continue
            cov = live.get((nx, ny), 0) + (1 if (nx, ny) in self.fs_sray else 0)
            k = (cov, -dsq_core(n, E))
            if best_k is None or k < best_k:
                best, best_k, best_d = n, k, CARDINALS[i]
        if best is None or best_k[0] >= here + (
                1 if (p.x, p.y) in self.fs_sray else 0):
            return False                 # nowhere strictly safer: work instead
        try:
            ct.move(best_d)
        except Exception:
            return False
        self.fs_retreat = True
        self._fs_log("RETREAT", rnd, "id", ct.get_id(), "hp", hp,
                     "from", (p.x, p.y), "to", (best.x, best.y))
        return True

    def _fs_seal_pending(self, ct, needed, ti):
        """Is rung 1 actionable-but-unfunded?  (=> wait, do not spend lower.)

        "Actionable" means an open ring tile that nothing is standing on: a seat
        under an enemy body or building is rung 2's and rung 3's problem, and
        blocking the lower rungs on it would deadlock the ladder on exactly the
        maps it exists for.
        """
        if not (FS_SEAL_ON and needed):
            return False
        blocked = self.fs_blocked_now
        if all((t.x, t.y) in blocked for t in needed):
            return False
        return not self._fs_seal_ok_peek(ct, needed, ti)

    def _fs_seal_ok_peek(self, ct, needed, ti):
        """`_fs_seal_ok` without the latch -- a predicate, not a decision."""
        if self.fs_seal_started or not needed:
            return True
        try:
            bar = ct.get_barrier_cost()
        except Exception:
            return False
        return ti >= len(needed) * bar + FS_SEAL_MARGIN

    def _fs_rung(self, ct, rnd, fired, E, p, needed, ti, orth_open):
        """⭐ THE LADDER'S OWN FALSIFIER, and it runs in the live bot.

        After a rung fires, re-ask every HIGHER rung whether it was actionable
        at that moment -- using the SAME code path that would have taken the
        action (`probe=True` stops one statement short of the mutating call), so
        the predicate cannot drift from the behaviour the way a hand-written
        mirror of it would.  A non-empty `hi` list in the log is a PRIORITY
        INVERSION and therefore a bug; the verification reads this count.
        """
        if not FS_LOG:
            return
        hi = []
        try:
            if fired > 1 and self._fs_rung1_ready(ct, p, needed, ti):
                hi.append(1)
            if fired > 2 and FS_EVICT_ON and self._fs_try_evict_launcher(
                    ct, E, p, ti, needed=needed, probe=True):
                hi.append(2)
            if fired > 3 and self._fs_try_clear(ct, E, p, needed, probe=True):
                hi.append(3)
        except Exception:
            return
        self._fs_log("RUNG", rnd, "id", ct.get_id(), "r", fired,
                     "hi", ",".join(str(x) for x in hi) if hi else "-")

    def _fs_rung1_ready(self, ct, p, needed, ti):
        """Could rung 1 have placed a barrier this round?"""
        if not (FS_SEAL_ON and needed):
            return False
        if not self._fs_seal_ok_peek(ct, needed, ti):
            return False
        for t in needed:
            if abs(t.x - p.x) + abs(t.y - p.y) != 1:
                continue
            try:
                if ct.can_build_barrier(t):
                    return True
            except Exception:
                continue
        return False

    def _fs_seal_ok(self, ct, needed, ti):
        """BINARY SEAL GATE.  Once open it LATCHES.

        The wider Jython record measured a partial >=10/12 seal running the
        WRONG WAY -- defender heals 0.0100 -> 0.0681/round, i.e. worse than not
        sealing at all -- while a complete 8-orthogonal seal read exactly 0
        heals and 0 spawns.  So the first barrier waits until the bank pays for
        every remaining one PLUS the sentinel that has to finish the game; and
        once we have started, a mid-seal price rise must not strand us at 10/12.
        """
        if self.fs_seal_started:
            return True
        if not needed:
            return True
        try:
            bar = ct.get_barrier_cost()
        except Exception:
            return False
        # ⛔ THIS GATE PRICES THE COLLAR AND NOTHING ELSE.  Two earlier forms
        # added the sentinel's price on top and deadlocked against the Core's
        # own siege reserve, which was computing a reserve over the same bank at
        # the same time: the bank sat a few titanium under both bars for the
        # whole match and not one barrier was placed.  The turret keeps its own
        # reserve in `_fs_sentinel_ok` (which reserves the barriers still owed),
        # so the two gates now point in opposite directions and cannot lock.
        #
        # And the SET it prices is the ORTHOGONALS: those eight tiles are the
        # entire heal set, so closing them is what the binary law is about.  The
        # four diagonals are spawn denial only and are deferred to the kill
        # window (a full 12-seal is broken in a median 9 rounds against 56 for
        # a >=8 partial).
        if ti < len(needed) * bar + FS_SEAL_MARGIN:
            return False
        self.fs_seal_started = True
        return True

    def _fs_try_seal(self, ct, E, p, needed, ti):
        if not needed:
            return False
        gate = self._fs_seal_ok(ct, needed, ti)
        # ⭐ A JUST-CLEARED SEAT JUMPS THE BINARY-SEAL WAIT.  Research's
        # belt-on-seats census (124,536 core-sides, s50): **46.6% of cleared
        # seats get a defender belt back, median 3 rounds and 16% within ONE**,
        # while a seat we CLAIM is 77% permanent however fast we claimed it.
        # So the window between "the squatter died" and "the barrier is up" is
        # the whole value of rung 3, and a binary-seal gate that says "wait
        # until you can pay for the entire collar" spends it.  The bypass is
        # narrow: this ONE tile, only for FS_CLEAR_HOLD rounds after it cleared,
        # and only when the single barrier is affordable.
        rnow = ct.get_current_round()
        fresh = self.fs_cleared if (LOKI_FS_SEAL_ONLY
                                    and LOKI_FS_RING_LADDER) else {}
        try:
            bar = ct.get_barrier_cost()
        except Exception:
            bar = 3
        for t in needed:
            if abs(t.x - p.x) + abs(t.y - p.y) != 1:
                continue
            if not gate:
                if fresh.get((t.x, t.y), -10 ** 9) < rnow - FS_CLEAR_HOLD:
                    continue
                if ti < bar:
                    continue
            try:
                if not ct.can_build_barrier(t):
                    continue
                ct.build_barrier(t)
            except Exception:
                continue
            self.fs_barriers += 1
            self.fs_tile_builds[(t.x, t.y)] = \
                self.fs_tile_builds.get((t.x, t.y), 0) + 1
            self._fs_log("SEAL", ct.get_current_round(), "tile", (t.x, t.y),
                         "n", self.fs_barriers)
            # CLEAR-THEN-SEAL, measured end to end: this barrier landed on a
            # seat we pecked a squatter off.  The pair is the plank's answer to
            # a belt-on-seats map and the verification counts it as a PAIR, not
            # as two independent events.
            if LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER \
                    and (t.x, t.y) in self.fs_cleared:
                self._fs_log("SEALCLR", ct.get_current_round(),
                             "tile", (t.x, t.y),
                             "lag", ct.get_current_round()
                             - self.fs_cleared[(t.x, t.y)])
                del self.fs_cleared[(t.x, t.y)]
            self._fs_draw_dot(ct, t, 255, 90, 0)
            return True
        return False

    def _fs_pecks(self, ct, key):
        """Pecks already spent on this tile -- PER VISIT under the ladder.

        ⛔ v511's cap was per tile FOR THE WHOLE MATCH, and 8 pecks is 16 damage
        against a 20 HP conveyor: the budget could never finish one, so the
        three belt-squatted seats on midgard stayed squatted and that map closed
        0/6.  Magnus's instruction is "peck conveyors at their core and replace
        with barriers ... RETURN until cleared".  The cap therefore bounds a
        VISIT (so a defended seat still cannot eat the match -- v510 spent 30
        consecutive rounds and 60 Ti on three of them), and the budget refills
        once the raider has been away from that tile for FS_CLEAR_REVISIT
        rounds, i.e. once it has actually gone and done other work.
        """
        n = self.fs_tile_pecks.get(key, 0)
        if not n or not (LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER):
            return n
        last = self.fs_tile_peck_rnd.get(key)
        if last is None:
            return n
        try:
            rnd = ct.get_current_round()
        except Exception:
            return n
        if rnd - last >= FS_CLEAR_REVISIT:
            v = self.fs_tile_visits.get(key, 1)
            if v >= FS_CLEAR_MAX_VISITS:
                return FS_CLEAR_MAX_PECKS      # hopeless seat: blocked for good
            self.fs_tile_visits[key] = v + 1
            self.fs_tile_pecks[key] = 0
            self.fs_tile_peck_rnd[key] = rnd
            return 0
        return n

    def _fs_try_clear(self, ct, E, p, needed, probe=False):
        """Peck an enemy building standing on a ring tile we still need.

        ⛔ DELIBERATELY NOT GATED ON LOKI_QUIET_ON.  That flag silences builder
        melee because 2 damage a round is worthless against a core one builder
        can heal at +4 -- true, and irrelevant here: this target is a 20-30 HP
        BUILDING sitting on a tile the collar cannot close around.  Left alive
        it is a permanent hole in the heal set, which is the one thing the whole
        plank is buying.
        """
        if not FS_CLEAR_RING_ON:
            return False
        # ⛔ AND IT SPENDS ONLY SURPLUS ABOVE THE COLLAR.  A peck is 2 Ti; at
        # one a round it drained the bank from 40 to 34 across the exact rounds
        # the seal gate wanted 42, so the collar never opened and the pecking
        # bought a conveyor's worth of damage instead of the heal set.
        try:
            ti = ct.get_global_resources()
            if ti < len(needed) * ct.get_barrier_cost() + FS_SEAL_MARGIN \
                    + LOKI_PECK_TI_FLOOR:
                return False
        except Exception:
            return False
        # ⭐ RUNG-3 OPERATIONAL RULE (research's belt-on-seats census, s50):
        # NEVER START CLEARING A SEAT YOU CANNOT CLAIM WITHIN ~3 ROUNDS OF IT
        # CLEARING.  46.6% of cleared seats get a defender belt back (median 3
        # rounds, 16% within one; 0033 rebuilds at median latency 1), against
        # 77% permanence for a seat we CLAIM.  Two conditions make the claim
        # inevitable rather than hoped-for, and both are already structural
        # here:
        #   * TI BANKED -- the gate above demands the whole remaining collar
        #     plus the peck floor, which strictly exceeds this seat's barrier;
        #     and `_fs_try_seal`'s fresh-seat bypass spends it on THIS tile
        #     without waiting for the binary gate.
        #   * ADJACENT AT CLEAR-TIME -- a peck and a build have the SAME
        #     orthogonal-adjacency requirement, so the body that lands the last
        #     peck is by construction standing where the barrier goes; and the
        #     census ordering (`fresh` in `_fs_census._order`) puts that tile
        #     first the moment it reads empty.
        # DEFER-AND-RETURN: a tile whose peck budget is spent is only picked up
        # again when every other needed tile is unreachable too.
        desperate = all((t.x, t.y) in self.fs_blocked_now for t in needed)
        for t in needed:
            if abs(t.x - p.x) + abs(t.y - p.y) != 1:
                continue
            key = (t.x, t.y)
            if LOKI_FS_SEAL_ONLY and not desperate \
                    and self._fs_pecks(ct, key) >= FS_CLEAR_MAX_PECKS:
                continue
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                if not ct.can_fire(t):
                    continue
                if probe:
                    return True
                ct.fire(t)
            except Exception:
                continue
            self.fs_tile_pecks[key] = self.fs_tile_pecks.get(key, 0) + 1
            self.fs_tile_peck_rnd[key] = ct.get_current_round()
            self._fs_log("CLEAR", ct.get_current_round(), "tile", key,
                         "peck", self.fs_tile_pecks[key])
            return True
        return False

    def _fs_try_peck(self, ct, E, p):
        if LOKI_QUIET_ON:
            return False
        try:
            if ct.get_global_resources() < LOKI_PECK_TI_FLOOR:
                return False
        except Exception:
            return False
        for c in core_tiles(E):
            if abs(p.x - c.x) + abs(p.y - c.y) != 1:
                continue
            try:
                if ct.can_fire(c):
                    ct.fire(c)
                    return True
            except Exception:
                continue
        return False

    def _fs_try_repair(self, ct, p, collar_open):
        for dx, dy in CARD_DELTAS:
            tx, ty = p.x + dx, p.y + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                hp, mx = ct.get_hp(bid), ct.get_max_hp(bid)
                if hp >= mx:
                    continue
                if collar_open and hp * 3 > mx:
                    continue        # still work to do elsewhere and it can wait
                if not ct.can_heal(t):
                    continue
                ct.heal(t)
            except Exception:
                continue
            return True
        return False

    def _fs_stand_target(self, ct, E, p, needed):
        """Where to walk: a tile from which the next needed ring tile is
        orthogonally adjacent.  Pathing is the chassis BFS (`_nav` ->
        `_bfs_direction`), which treats BARRIERs as blocked -- the probe's
        greedy walker deadlocked 995 rounds against its own collar."""
        if not needed:
            park = self._fs_park_seat(ct, E)
            return park if (FS_PARK_ON and park is not None) else None
        # ⛔ WALK TO THE NEAREST NEEDED TILE, NOT TO THE HIGHEST-PRIORITY ONE.
        # The build ORDER (NW first, worn tiles last) decides what to place when
        # something is already under our hand; using that same order to pick a
        # DESTINATION sent the raider all the way round the collar between every
        # barrier -- measured: three barriers at r16, r20 and r32 on a ring it
        # had reached at r12, with a full lap of walking in between.  One body
        # sealing a closed curve wants a sweep, and a sweep is nearest-first.
        # ⛔ A TILE UNDER AN ENEMY BODY IS NOT A DESTINATION.  An earlier form
        # returned "you are already in place" the moment `p` was orthogonally
        # adjacent to ANY needed tile, blocked ones included -- so a raider
        # standing beside a squatted seat froze there for fifteen rounds at full
        # HP with five other tiles open, and then died on that tile.  Squatters
        # are the eviction launcher's job.  The blocked tiles come back into
        # play only when nothing else is left.
        blocked = self.fs_blocked_now
        open_first = [t for t in needed if (t.x, t.y) not in blocked]
        if not open_first:
            open_first = needed
        # ⭐ TURRET-RAY BLACKLIST (seal-only).  A stand tile on a visible enemy
        # turret's firing line is where our bodies die; stepping one tile off it
        # costs a round and forces them to pay a rotate.  It is a PREFERENCE,
        # not a veto -- ranked ahead of distance so an off-ray tile one step
        # further away wins, but a needed tile with no off-ray station is still
        # worked.
        axis = self._fs_gun_axis(ct) if (LOKI_FS_SEAL_ONLY
                                         and FS_AVOID_TURRET_AXIS) else ()
        if LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER and FS_DODGE_ON:
            # ⛔ THE WALKER HAS TO SHARE THE DODGE'S MEMORY OR THE TWO FIGHT
            # EACH OTHER.  Measured on the first ladder smoke run (midgard seed
            # 21): DODGE r16 (23,25)->(24,25), the walker put the body straight
            # back on (23,25) because the shooting sentinel was out of vision
            # that round, DODGE r18 again, dead at r19.  `_fs_gun_axis` is a
            # THIS-ROUND read; `fs_threat` is the same read with
            # FS_DODGE_MEMORY rounds of memory, which is exactly what a
            # stand-tile blacklist needs.  Still a PREFERENCE, not a veto.
            axis = set(axis) | set(self.fs_threat.keys())
        # ⭐⭐ v513 CHANGE G: THE BLACKLIST WAS A SORT KEY, NOT A VETO, AND THAT
        # IS WHY IT SAVED NOBODY.  `k = (on_axis, distance, rank)` picks the
        # least-covered station ACROSS ALL needed tiles -- but when the only
        # station beside the seat we want is on a ray, every candidate ties at 1
        # and distance re-selects the ray tile.  Measured on nordkap: DODGE
        # (10,9)->(10,8) at r200, r203, r205, r207, r209, r213, the walker
        # putting the body back on (10,9) between every one of them, HP 40 -> 33
        # -> 26 -> 8 -> 1, twenty-five dodge-rounds against three productive
        # ones -- the dodge does not merely fail to save the body, IT
        # CANNIBALISES THE SEAL, because it is rung 0 and returns.
        # The veto is over tiles we have actually been HIT on (permanent) plus
        # tiles on a SENTINEL ray (permanent, because sentinels cannot rotate),
        # and it FALLS BACK to the incumbent preference when it would leave the
        # body with nowhere to stand at all.
        veto = ()
        if LOKI_FS_CREW and FS_PRESTAND_AVOID:
            veto = set(self.fs_hit_tiles.keys()) | set(self.fs_sray.keys())
        # ⭐⭐ v515 CHANGE 3 -- THE EVICTOR'S REACH, AS A WALKER PREFERENCE.
        # `_fs_try_evict_launcher` can only score the <=4 tiles orthogonally
        # adjacent to where we are standing, so the max-coverage launcher tile
        # is unreachable unless the WALKER goes and stands beside it (v514
        # report surprise 4: 1 of a 4-seat ceiling, never 2+).  `rstat` is the
        # set of stations from which that tile is buildable.
        # ⛔ PREFERENCE, NOT VETO, and the reason is written six lines above
        # this one: v513 change G's blacklist had to fall back to the incumbent
        # preference because an absolute veto leaves the body with nowhere to
        # stand, and the v510 "contested near face keeps `needed` non-empty for
        # ever" stall is the same shape.  This term only REORDERS a candidate
        # set it does not change, and it sits BELOW the turret-ray avoidance
        # (dying is worse than siting badly) and ABOVE raw distance.
        # ⛔ THE PROBE ARM COMPUTES THE CEILING AND DOES NOT USE IT.  A
        # reach-OFF mutant has to report the same ceiling number as the fired
        # arm or the two ucov distributions are not comparable, so the scan
        # runs under FS_V515_REACH_PROBE too and only `rstat` is withheld.
        rstat = ()
        if LOKI_FS_V515 and (FS_V515_REACH or FS_V515_REACH_PROBE):
            try:
                rt, _ruc, _rwant = self._fs_reach_tile(ct, E,
                                                       ct.get_current_round())
            except Exception:
                rt, _rwant = None, False
            # ⛔ `_rwant` IS WHAT KEEPS THE PROBE INERT.  The scan runs in the
            # probe arm so the two arms report the same ceiling, but the
            # PREFERENCE is applied only when an evictor is genuinely wanted --
            # otherwise the probe arm would walk differently from the fired
            # config it exists to be compared against.
            if rt is not None and FS_V515_REACH and _rwant:
                # ⛔ AND IT EXPIRES.  The one stall this preference can cause
                # that the parent's key cannot is a station the BFS never
                # reaches (barriered off, squatted, on the far side of the
                # collar): the walker would keep re-selecting it for ever
                # because nothing about the tile changes.  After
                # FS_REACH_PATIENCE rounds on the SAME tile with no evictor
                # bought, the term drops and the body reverts to the parent's
                # nearest-first sweep.  The clock restarts if the tile moves.
                key = (rt.x, rt.y, getattr(self, "fs_evictors", 0))
                if getattr(self, "fs515_reach_key", None) != key:
                    self.fs515_reach_key = key
                    self.fs515_reach_since = ct.get_current_round()
                if ct.get_current_round() - self.fs515_reach_since \
                        <= FS_REACH_PATIENCE:
                    rstat = set((rt.x + dx, rt.y + dy)
                                for dx, dy in CARD_DELTAS)
        # ⭐⭐ v516 CHANGE 3 -- THE SENTINEL'S REACH, AS A WALKER PREFERENCE.
        # Same shape as the evictor term above and for the same reason: the
        # purchase can only score tiles under the body's hand, so the site the
        # scan says is best is unreachable unless the WALKER goes and stands
        # beside it.  PREFERENCE, NOT VETO -- an absolute veto leaves the body
        # with nowhere to stand (v513 change G) -- and it EXPIRES after
        # FS_SENT_REACH_PATIENCE rounds on the same site with no sentinel
        # bought, because a station the BFS never reaches would otherwise be
        # re-selected for ever.  It ranks BELOW the evictor reach: the collar
        # is what the body is there for, and the sentinel term must not
        # cannibalise it.
        # ⛔ ONLY WHILE A SENTINEL IS ACTUALLY WANTED.  Computing the scan when
        # the gate is shut or the cap is full would walk the body differently
        # from the config this is compared against, for a purchase that cannot
        # happen.
        sstat = ()
        if LOKI_FS_V516 and FS_V516_SENTREACH:
            try:
                _rnd = ct.get_current_round()
                # v517: the affordability half of `_want` uses the SAME floor
                # the purchase will use, so the walker starts moving toward the
                # twin's site in the round the hold opens the gate rather than
                # FS_SENT_REACH_RECHECK rounds later.
                _v517_floor, _v517_rebuy = self._v517_sent_floor(ct)
                _want = (self._fs_live_sentinels(ct, E) < FS_SENTINEL_MAX
                         and ct.get_global_resources()
                         >= ct.get_sentinel_cost() + _v517_floor)
            except Exception:
                _rnd, _want = 0, False
            if _want:
                st = self._fs_sent_reach_tile(ct, E, _rnd)
                if st is not None:
                    key = (st.x, st.y, self.fs_sentinels)
                    if self.fs516_reach_key != key:
                        self.fs516_reach_key = key
                        self.fs516_reach_since = _rnd
                    if _rnd - self.fs516_reach_since \
                            <= FS_SENT_REACH_PATIENCE:
                        sstat = set((st.x + dx, st.y + dy)
                                    for dx, dy in CARD_DELTAS)
        best, best_k = None, None
        fb, fb_k = None, None
        for rank, t in enumerate(open_first):
            for dx, dy in CARD_DELTAS:
                sx, sy = t.x + dx, t.y + dy
                st = Position(sx, sy)
                if self._fs_wall(st):
                    continue
                if dsq_core(st, E) == 0:
                    continue                 # core footprint: unstandable
                if sx == p.x and sy == p.y and (sx, sy) not in axis \
                        and (sx, sy) not in veto \
                        and not (rstat and (sx, sy) not in rstat) \
                        and not (sstat and (sx, sy) not in sstat):
                    # ⛔ THE EARLY RETURN IS WHAT MADE THIS A REACH BUG.  "You
                    # are already in place" fires the moment the body is beside
                    # ANY needed tile, which is why the launcher tile was never
                    # under its hand; while a reach station exists and we are
                    # not on one, fall through and let the sort decide (`p`
                    # still scores here, at distance 0).
                    return p                 # already in place
                try:
                    if ct.is_in_vision(st) and not ct.is_tile_passable(st):
                        continue
                except Exception:
                    pass
                k = (1 if (sx, sy) in axis else 0,
                     0 if (sx, sy) in rstat else 1,
                     0 if (sx, sy) in sstat else 1,
                     abs(sx - p.x) + abs(sy - p.y), rank)
                if (sx, sy) in veto:
                    if fb_k is None or k < fb_k:
                        fb, fb_k = st, k
                    continue
                if best_k is None or k < best_k:
                    best, best_k = st, k
        if FS_REACH_LOG and rstat:
            # v515 change 3's SECOND instrument, and it is the one that says
            # whether the preference could bite at all: `cand` counts the
            # stations of needed ring tiles that are also stations of the
            # max-coverage launcher tile.  `cand 0` means the ceiling tile has
            # NO station in the candidate set -- a geometric miss, not a
            # preference that lost.
            try:
                cand = 0
                for _t in open_first:
                    for _dx, _dy in CARD_DELTAS:
                        if (_t.x + _dx, _t.y + _dy) in rstat:
                            cand += 1
                print("STAND515", ct.get_current_round(),
                      "cand", cand, "chose",
                      ((best.x, best.y) if best else None),
                      "inrstat",
                      1 if (best and (best.x, best.y) in rstat) else 0,
                      "here", (p.x, p.y), file=sys.stderr)
            except Exception:
                pass
        if best is None:
            return fb
        return best

    # --- D. the eviction launcher ------------------------------------------

    def _fs_observe_healers(self, ct, E):
        """Count enemy builders SITTING ON a heal seat, per tile, this siege.

        ⭐ THIS IS THE SIGNAL, and the study that measured it is the reason it
        is not a fixed ring index.  Fixed a-priori best tile intercepts 29.0%
        of on-core heal traffic; watching 5 heals in THIS siege intercepts
        48.4%.  The pooled distribution over 1,116,056 heal events is nearly
        FLAT (max cell 14.58% against 12.5% uniform), while per-episode traffic
        is CONCENTRATED (busiest tile median 55.6%, median 3 distinct tiles) --
        so the flat pool is a normalisation artefact and reactive siting beats
        fixed siting by ~19pp precisely because of it.

        And we watch SQUATTERS, not lanes: 94.9% / 91.6% / 88.6% of healers are
        already standing on their exact heal tile 3 / 6 / 10 rounds before they
        heal.  "Approach-route interception" is refuted -- there is no approach.
        """
        seatset = set((s.x, s.y) for s in heal_seats(E, self.mw, self.mh))
        hist = self.fs_healer_hist
        try:
            for eid in ct.get_nearby_units():
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                if ct.get_team(eid) == self.team:
                    continue
                ep = ct.get_position(eid)
                if (ep.x, ep.y) not in seatset:
                    continue
                hist[(ep.x, ep.y)] = hist.get((ep.x, ep.y), 0) + 1
                self.fs_healer_obs += 1
        except Exception:
            return

    def _fs_try_evict_launcher(self, ct, E, p, ti, needed=None, probe=False):
        """Plant a launcher whose OWN d^2<=2 ring covers the tiles their
        healers have ACTUALLY been sitting on this siege.

        `cov` is `_v233evict58/raid.py:694-696` and it is what made eviction
        fire at all: the same plant on fixed ring indices read 0 evictions in
        1,000 rounds of a probe with a perfect fixture; the score took the
        identical fixture to 248 throws.  What is new here is the SET it is
        scored over -- observed healer tiles, not generic geometry.

        TWO LAUNCHERS, and the second is DEFAULT-ON: one adaptive launcher tops
        out at 48.4% strict / 58.5% deny-mode interception, two reach 70.5% /
        86.5%, and the second's marginal gain exceeds the first's gain over
        blind siting.  Its only condition is Ti sufficiency -- the seal and the
        sentinel are reserved first.

        DENY MODE: a candidate that is itself ON a ring tile is preferred.  It
        removes that tile from the heal set, from the delivery set (every one
        of 1,524,857 deliveries into a core footprint originates on the eight
        orthogonals) and from the spawn set, with one body.
        """
        ladder = LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER
        live = self._fs_live_evictors(ct, E)
        # ⭐ ONE UNDER THE LADDER.  The autopsy priced the second: v510's pair
        # threw 119 times and 117 of those were the same 4-tile hop recycling
        # two bots, while the tile 51 of 59 heals came from was outside both
        # pickup rings.  Siting is the lever, count is not, and rung 1 owns the
        # bank the second one would have cost.
        if live >= (FS_LADDER_EVICT_MAX if ladder else FS_EVICT_MAX):
            return False
        supp = LOKI_FS_CREW and FS_CREW_ON and self.fs_role == "supp"
        min_obs = (FS_CREW_HEALER_MIN_OBS
                   if (supp and FS_CREW_EVICT_NOWAIT) else FS_HEALER_MIN_OBS)
        # ⭐⭐ v514 CHANGE C -- THE OBSERVATION MINIMUM IS BYPASSED BY A SEAT,
        # AND THE AUTOPSY MEASURED WHY.  `obs < 5` is the single largest binder
        # on the evictor (2,204 of 4,479 blocked at-ring rounds, 49.2%), and on
        # drakkarfjord/glacierkeep the raider spends its ENTIRE at-ring life
        # under it -- the launcher is never even priced.  The minimum exists to
        # stop us siting on GUESSED healer geometry; a seat carrying the
        # defender's own building is not a guess, it is a seat we can see and
        # can never barrier, so coverage of one justifies the purchase on its
        # own.
        unseal = set()
        if LOKI_FS_V514 and FS_V514_DENYSITE:
            unseal = self._fs_unsealable(ct, E) - self._fs_evict_cover(ct, E)
        if self.fs_healer_obs < min_obs and not (
                LOKI_FS_V514 and FS_V514_DENYSITE and FS_DENY_OBS_BYPASS
                and unseal):
            return False
        try:
            cost = ct.get_launcher_cost()
        except Exception:
            return False
        floor = FS_EVICT_TI_FLOOR
        if supp and FS_CREW_EVICT_NOWAIT:
            # ⭐⭐ v513 CHANGE E -- THE SUPPORT'S OWN GATE.  EVICTION FIRED ZERO
            # TIMES IN 19 OF 24 GAMES, and the ladder's collar-first floor is
            # half of why: it reserves every barrier still owed out of a bank
            # this body was never going to spend on a barrier.  A launcher
            # bought by the SUPPORT cannot cost a seat, because the support
            # does not seal -- so it reserves only what the collar cannot
            # recover from income inside FS_CREW_EVICT_RECOVER rounds (passive
            # is 10 Ti / 4 rounds and each harvester another 10 / 4).  And per
            # P6 (enemy bodies block barriers, 40 of 40) this is not an
            # optimisation: a body-held seat is unsealable until something
            # throws that body off it.
            try:
                harv = ct.read_store(SLOT_HARVESTERS)
                owed = len(needed or ()) * ct.get_barrier_cost()
                recover = FS_CREW_EVICT_RECOVER * (10 + 10 * harv) // 4
                floor += max(0, owed - recover)
            except Exception:
                return False
        elif ladder:
            # ⛔ THE EVICTOR MAY NOT EAT THE BARRIER BUDGET.  Rung 1 is above
            # rung 2 in the bank as well as in the ladder: this floor is every
            # seat still owed, priced with the same arithmetic `_fs_seal_ok`
            # uses, so a launcher can only ever be bought out of true surplus.
            try:
                floor += len(needed or ()) * ct.get_barrier_cost() \
                    + FS_SEAL_MARGIN
            except Exception:
                return False
        elif live >= 1:
            try:
                floor += ct.get_sentinel_cost() + 4 * ct.get_barrier_cost()
            except Exception:
                return False
        if ti < cost + floor:
            return False
        hist = self.fs_healer_hist
        ringset = set()
        if FS_RING_SITE_ON:
            ring, _seats = self._fs_ring12(E)
            ringset = set((t.x, t.y) for t in ring)
        best, best_k = None, None
        for dx, dy in CARD_DELTAS:
            bx, by = p.x + dx, p.y + dy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            bp = Position(bx, by)
            if dsq_core(bp, E) > FS_RING_DSQ:
                continue                     # must BE an eviction launcher
            try:
                if not ct.can_build_launcher(bp):
                    continue
            except Exception:
                continue
            cov = 0
            for (sx, sy), n in hist.items():
                if (bx - sx) ** 2 + (by - sy) ** 2 <= 2:
                    cov += n
            if LOKI_FS_V514 and FS_V514_DENYSITE:
                # ⭐ THE SITING OBJECTIVE MAGNUS ASKED FOR: cover the seats the
                # BARRIER cannot take, first; observed healer tiles second.
                # Measured ceiling vs actual (closure autopsy §5): the best
                # legal tile reaches 4 of the 8 seats on every one of the five
                # grid maps, and the rung-2 evictors we actually built reached
                # 1-2 -- siting at half ceiling.
                ucov = sum(1 for (sx, sy) in unseal
                           if (bx - sx) ** 2 + (by - sy) ** 2 <= 2)
                k = (ucov, cov, 1 if (bx, by) in ringset else 0,
                     -dsq_core(bp, E))
            else:
                ucov = 0
                k = (cov, 1 if (bx, by) in ringset else 0, -dsq_core(bp, E))
            if best_k is None or k > best_k:
                best, best_k = bp, k
        if best is None:
            return False
        if LOKI_FS_V514 and FS_V514_DENYSITE:
            # A tile that covers an unsealable seat is worth buying even with
            # zero healer sightings -- that is the whole bypass above.
            if best_k[0] <= 0 and best_k[1] <= 0:
                return False
        elif best_k[0] <= 0:
            return False
        if probe:
            return True
        try:
            ct.build_launcher(best)
        except Exception:
            return False
        self.fs_evictors += 1
        if FS_REACH_LOG:
            # v515 change 3's instrument: the ucov the evictor was ACTUALLY
            # built at, beside the ceiling the ring scan says was available.
            try:
                _rt = getattr(self, "fs515_reach", (None, 0, -1, False))
                print("EVICT515", ct.get_current_round(),
                      "at", (best.x, best.y), "ucov", best_k[0],
                      "cov", best_k[1] if LOKI_FS_V514 and FS_V514_DENYSITE
                      else -1,
                      "ceil", _rt[1], "ceiltile",
                      (_rt[0].x, _rt[0].y) if _rt[0] else None,
                      "n", self.fs_evictors, file=sys.stderr)
            except Exception:
                pass
        if LOKI_FS_V514 and FS_V514_DENYSITE:
            self._fs_log("EVICTOR", ct.get_current_round(),
                         "at", (best.x, best.y),
                         "ucov", best_k[0], "cov", best_k[1],
                         "unseal", len(unseal), "obs", self.fs_healer_obs)
        else:
            self._fs_log("EVICTOR", ct.get_current_round(),
                         "at", (best.x, best.y), "cov", best_k[0])
        self._fs_draw_dot(ct, best, 255, 0, 200)
        return True

    def _fs_live_evictors(self, ct, E):
        """⛔ v514 CHANGE C, THE `:1819` FIX.  The parent counts ANY friendly
        launcher inside FS_RING_DSQ, so a FERRY link that happens to terminate
        in the ring occupies the single evictor slot forever and rung 2 is
        never bought -- measured in 4 of 13 throwing games, all midgard
        (AUTOPSY-evict-v513-fired §3).

        THE DISCRIMINATOR IS MEASURED, NOT TAGGED: in-ring ferry launchers
        cover 0 of the 8 heal seats in 12 of 12 observed cases (they land on
        the outer diagonal), while a purpose-sited evictor reaches 1-4.  So a
        launcher whose own d^2<=2 pickup envelope covers NO heal seat is not
        doing the evictor's job and does not hold the slot.
        """
        roled = LOKI_FS_V514 and FS_V514_DENYSITE and FS_EVICT_ROLED_ONLY
        seats = ()
        if roled:
            try:
                seats = tuple((s.x, s.y)
                              for s in heal_seats(E, self.mw, self.mh))
            except Exception:
                roled = False
        n = 0
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.LAUNCHER:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                bp = ct.get_position(bid)
                if dsq_core(bp, E) > FS_RING_DSQ:
                    continue
                if roled and not any((bp.x - sx) ** 2 + (bp.y - sy) ** 2 <= 2
                                     for sx, sy in seats):
                    continue                 # a ferry terminus, not an evictor
                n += 1
        except Exception:
            return n
        return n

    def _fs_evict_cover(self, ct, E):
        """{(x, y)} of heal seats covered by a live in-ring launcher of ours.

        v514 change C.  A covered seat is one where a healer that stands there
        gets thrown off it -- which is Magnus's priority 2 verbatim ("build
        launchers to keep healers and enemy builders away from their core"),
        and the reason it matters is an engine fact the builder retracted a
        wrong reading of on 2026-08-18: conveyors are PASSABLE, so a healer can
        stand on the defender's own belt and heal through it.  A barrier can
        never take that seat; a launcher can keep it empty.
        """
        cov = set()
        try:
            seats = [(s.x, s.y) for s in heal_seats(E, self.mw, self.mh)]
        except Exception:
            return cov
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.LAUNCHER:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                bp = ct.get_position(bid)
                if dsq_core(bp, E) > FS_RING_DSQ:
                    continue
                for sx, sy in seats:
                    if (bp.x - sx) ** 2 + (bp.y - sy) ** 2 <= 2:
                        cov.add((sx, sy))
        except Exception:
            return cov
        return cov

    def _fs_unsealable(self, ct, E):
        """{(x, y)} of heal seats a BARRIER CAN NEVER TAKE: an enemy building
        stands on them.  These are the closure-binding seats the autopsy
        measured -- 6 of 9 on atoll, 14 of 27 on midgard -- and they are what
        the evictor is now sited to deny.  Ours, and empty seats, are excluded:
        an empty seat is rung 1's and must stay rung 1's.
        """
        out = set()
        try:
            seats = heal_seats(E, self.mw, self.mh)
        except Exception:
            return out
        for s in seats:
            if not (0 <= s.x < self.mw and 0 <= s.y < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(s)
                if bid is None:
                    continue
                if ct.get_team(bid) == self.team:
                    continue
            except Exception:
                continue
            out.add((s.x, s.y))
        return out

    def _fs_reach_tile(self, ct, E, rnd):
        """⭐⭐ v515 CHANGE 3 -- THE TILE THE EVICTOR *SHOULD* BE ON.

        The parent's siting objective (`ucov`, change C) is correct and was
        being maximised over the wrong SET: `_fs_try_evict_launcher` only ever
        scores the <=4 tiles orthogonally adjacent to wherever the raider is
        standing, and the raider stands wherever the barrier sweep put it.
        Measured consequence (v514 report surprise 4): evictors at ucov 1 in 3
        of 9 and never 2 or more, against a ceiling of 4 that the closure
        autopsy measured as reachable on all five grid maps.

        This is the same objective evaluated over EVERY legal in-ring tile, so
        the walker can be told where to stand.  Returns (Position, ucov) or
        (None, 0).

        ⛔ LEGALITY IS APPROXIMATE HERE AND THAT IS DELIBERATE.
        `can_build_launcher` requires orthogonal adjacency to the asking body,
        so it is False for every tile this scan is about and cannot be used.
        The scan uses the parts of the predicate that are position-only
        (in-bounds, not a wall, no building standing there, not the core
        footprint) and lets `_fs_try_evict_launcher` make the real call once we
        are beside the tile.  A tile that turns out to be unbuildable costs a
        preference, not a build.

        ⛔ AND IT IS ONLY COMPUTED WHEN AN EVICTOR IS ACTUALLY WANTED -- slot
        free AND something unbarrierable left to cover.  Otherwise the term is
        identically zero and the walker is the parent's, byte for byte.
        """
        cached = getattr(self, "fs515_reach", None)
        if cached is not None and rnd - cached[2] < FS_REACH_RECHECK:
            return cached[0], cached[1], cached[3]
        ladder = LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER
        want = True
        try:
            if self._fs_live_evictors(ct, E) >= (FS_LADDER_EVICT_MAX if ladder
                                                 else FS_EVICT_MAX):
                want = False
        except Exception:
            want = False
        unseal = ()
        if want or FS_V515_REACH_PROBE:
            try:
                unseal = self._fs_unsealable(ct, E) - self._fs_evict_cover(ct, E)
            except Exception:
                unseal = ()
        if not unseal or not (want or FS_V515_REACH_PROBE):
            self.fs515_reach = (None, 0, rnd, want)
            if FS_REACH_LOG:
                # ⛔ THE EMPTY CASE IS LOGGED TOO.  "no unbarrierable seat yet"
                # and "a ceiling exists and we missed it" are different
                # findings and a log that only fires on the second cannot tell
                # them apart.
                try:
                    print("REACH515", rnd, "tile", None, "ucov", 0,
                          "unseal", len(unseal), "want", 1 if want else 0,
                          file=sys.stderr)
                except Exception:
                    pass
            return None, 0, want
        best, best_k = None, None
        for t in self._fs_ring_tiles(E):
            bx, by = t
            cov = sum(1 for (sx, sy) in unseal
                      if (bx - sx) ** 2 + (by - sy) ** 2 <= 2)
            if cov <= 0:
                continue
            # ties broken OUTWARD, matching `_fs_try_evict_launcher`'s own
            # `-dsq_core` term, so the two agree on which of two equal-coverage
            # tiles is "the" tile.
            k = (cov, -dsq_core(Position(bx, by), E))
            if best_k is None or k > best_k:
                best, best_k = Position(bx, by), k
        ucov = best_k[0] if best_k else 0
        self.fs515_reach = (best, ucov, rnd, want)
        if FS_REACH_LOG:
            try:
                print("REACH515", rnd, "tile",
                      (best.x, best.y) if best else None,
                      "ucov", ucov, "unseal", len(unseal),
                      "want", 1 if want else 0, file=sys.stderr)
            except Exception:
                pass
        return best, ucov, want

    def _fs_ring_tiles(self, E):
        """Every in-bounds non-wall tile inside FS_RING_DSQ of the enemy core,
        excluding the footprint.  Cached for the match: the map and the enemy
        anchor are both constants, so this is a per-match scan of ~20 tiles."""
        cached = getattr(self, "fs515_ringtiles", None)
        if cached is not None:
            return cached
        out = []
        r = 4                                # FS_RING_DSQ = 8 -> |dx|,|dy| <= 2
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                bx, by = E.x + dx, E.y + dy
                if not (0 <= bx < self.mw and 0 <= by < self.mh):
                    continue
                bp = Position(bx, by)
                d = dsq_core(bp, E)
                if d == 0 or d > FS_RING_DSQ:
                    continue
                if self._fs_wall(bp):
                    continue
                out.append((bx, by))
        out = tuple(out)
        self.fs515_ringtiles = out
        return out

    # --- F. the kill --------------------------------------------------------

    # =====================================================================
    # ⭐⭐ v517 -- FIRE DISCIPLINE (change 1) AND THE TWIN GATE (change 2).
    # The sentinel is a UNIT: `run()` is called for it every round it lives
    # (v516 finding 1, which also established that there is NO id-based
    # liveness channel -- `get_hp(id)`/`get_position(id)` RAISE for any id
    # outside the caller's vision, indistinguishably from a destroyed one).
    # So the sentinel measures the enemy core's HP with its own eyes -- its
    # vision r^2 = 32 covers its target BY CONSTRUCTION, because
    # `_fs_try_sentinel` only ever buys a site with `can_fire_from` true on a
    # core tile at d^2 <= 32 -- and publishes the verdict itself.
    # =====================================================================

    def _v517_stamp(self, rnd):
        """(round % 15) + 1 -- a 4-bit clock.  0 is reserved for "never"."""
        return (rnd % FS_V517_STAMP_MOD) + 1

    def _v517_stamp_age(self, stamp, rnd):
        """Rounds since `stamp` was written, or None if it was never written.

        ⛔ MOD-15 ARITHMETIC.  The stamp wraps every 15 rounds, so this is only
        meaningful for ages < 15 -- which is all FS_V517_NET_STALE = 3 needs,
        and the wrap fails in the SAFE direction: an age of 15 reads as 0 and
        the caller believes a channel that is one wrap stale, but nothing
        writes this field except a unit that runs EVERY round it lives, so a
        15-round gap means the writer is long dead and the field has been
        rewritten by nobody.  (The one-wrap ghost is bounded at 1 in 15 rounds
        of one dead publisher; the beat1 field, which is exact, gates the
        magazine, so no ammunition decision rests on this clock.)
        """
        if stamp <= 0:
            return None
        return (rnd - (stamp - 1)) % FS_V517_STAMP_MOD

    def _v517_peer(self, ct, E, my_id):
        """(n_other_forward_sentinels_VISIBLE, lowest_other_id_or_None).

        Vision-limited on purpose: this is a LOCAL read that costs nothing and
        is EXACT when it fires.  Two forward sentinels sit within d^2 <= 32 of
        the same 2x2 core but can be up to ~11 tiles apart, which is outside a
        sentinel's r^2 = 32, so the store's PEER stamp is the second channel --
        either one of the pair seeing the other is enough to raise it.
        """
        n, low = 0, None
        try:
            for bid in ct.get_nearby_buildings():
                if bid == my_id:
                    continue
                if ct.get_entity_type(bid) != EntityType.SENTINEL:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                if dsq_core(ct.get_position(bid), E) > FS_SENT_BEAT_DSQ:
                    continue
                n += 1
                if low is None or bid < low:
                    low = bid
        except Exception:
            return n, low
        return n, low

    def _v517_core_hp(self, ct, E):
        """The enemy core's CURRENT HP, or None if it is not readable.

        ⛔ BOUNDS BEFORE VISION (s50 probe: `is_in_vision` is a pure radius test
        and does NOT guard bounds; the next `get_tile_*` then raises).  And
        `get_hp` raises for anything out of vision, so the whole read is inside
        one try -- an unreadable core is NOT evidence of anything and simply
        suspends the window.
        """
        try:
            for t in core_tiles(E):
                if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                    continue
                if not ct.is_in_vision(t):
                    continue
                bid = ct.get_tile_building_id(t)
                if bid is None:
                    continue
                if ct.get_entity_type(bid) != EntityType.CORE:
                    continue
                if ct.get_team(bid) == self.team:
                    continue
                return ct.get_hp(bid)
        except Exception:
            return None
        return None

    def _v517_netcode(self, net):
        """Bucket a net-damage reading into the 3-bit published code."""
        if net <= FS_V517_NET_EPS:
            return FS_V517_CODE_HELD
        for i, edge in enumerate(FS_V517_NET_BUCKETS):
            if net <= edge:
                return 2 + i
        return 7

    def _v517_sent_tick(self, ct, E, p, rnd, cur):
        """THE SENTINEL'S OWN TURN, v517 part.  Returns the bits this body
        contributes to SLOT_SENT_BEAT's v517 fields, and leaves the fire
        decision on `self.v517_hold_now`.

        THE RULE:
          * TWIN alive (seen locally, or the PEER stamp is fresh) -> FIRE, no
            hold, ever.  Two aligned sentinels are 18 HP/round against a
            measured maximum heal of 9.21 -- the arithmetic that makes holding
            pointless is the same arithmetic that makes the twin worth buying.
          * else, with a FULL window of FS_V517_NET_W core shots, if the net
            core-HP change over that window is <= FS_V517_NET_EPS -> HOLD the
            core shot (the 100.0%-heal-back signature; 11 of 12 failed sieges).
          * else FIRE.
        ⛔ THE FRESH-CONTACT WINDOW IS PROTECTED BY THE BUFFER ITSELF: no
        verdict exists until W shots have been taken, and a TTL reset empties
        the buffer, so a re-probe also gets its W free shots.  `v517_viol`
        counts any hold taken with fewer than W total shots and MUST read 0.
        """
        self.v517_hold_now = False
        bits = cur & (((FS_V517_STAMP_MASK << FS_V517_PEER_SHIFT)
                       | (FS_V517_STAMP_MASK << FS_V517_VERDICT_SHIFT)
                       | (FS_V517_NETCODE_MASK << FS_V517_NETCODE_SHIFT)))
        stamp = self._v517_stamp(rnd)
        try:
            my_id = ct.get_id()
        except Exception:
            my_id = None
        n_peer, low_peer = self._v517_peer(ct, E, my_id)
        if n_peer:
            bits = ((bits & ~(FS_V517_STAMP_MASK << FS_V517_PEER_SHIFT))
                    | (stamp << FS_V517_PEER_SHIFT))
        # the PEER stamp from the OTHER half of the pair, if it saw us first
        peer_age = self._v517_stamp_age(
            (cur >> FS_V517_PEER_SHIFT) & FS_V517_STAMP_MASK, rnd)
        twin = bool(n_peer) or (peer_age is not None
                                and peer_age <= FS_V517_NET_STALE)
        self.v517_twin_now = twin

        hp = self._v517_core_hp(ct, E)
        self.v517_hp_now = hp
        net, code = None, 0
        win = self.v517_win
        if hp is not None and len(win) >= FS_V517_NET_W:
            net = win[0] - hp
            code = self._v517_netcode(net)
        self.v517_net_now = net

        if twin:
            self.v517_hold_since = None
        elif code == FS_V517_CODE_HELD:
            if self.v517_hold_since is None:
                self.v517_hold_since = rnd
            if rnd - self.v517_hold_since >= FS_V517_HOLD_TTL:
                # ⛔ THE RE-PROBE.  A held sentinel deals no damage, so the
                # window cannot improve on its own -- without this the hold is
                # ABSORBING and a defender who dies or stops healing is never
                # noticed.  Reset the buffer and pay W shots to find out.
                del win[:]
                self.v517_hold_since = None
                self.v517_resets += 1
            else:
                if self.v517_shots < FS_V517_NET_W:
                    self.v517_viol += 1     # must be 0: the buffer forbids it
                else:
                    self.v517_hold_now = True
        else:
            self.v517_hold_since = None

        # ⭐ ONE WRITER FOR THE VERDICT, ELECTED BY VISION AND FALLING BACK ON
        # AN IDENTICAL VALUE.  The publisher is the lowest live id: a body that
        # can SEE a friendly forward sentinel with a lower id defers.  Where
        # the pair cannot see each other both publish -- and both are reading
        # the SAME enemy core HP, so the values agree except when their windows
        # started at different rounds; the surviving value is a live sentinel's
        # honest verdict either way, and the only consumer (the raid-side twin
        # gate) reads `== FS_V517_CODE_HELD`.  This is the SENTBEAT discipline
        # the field was designed around: collision-safe by writing the same
        # thing, never by locking.
        publish = (my_id is None or low_peer is None or my_id < low_peer)
        if publish and not n_peer:
            # ⛔ AND THE PUBLISHER CLEARS THE PEER FIELD WHEN IT SEES NOBODY --
            # the same mod-15 wrap ghost that `_fs_hold_live` had to gate on
            # the exact beat, arriving on the other field.  A stale PEER stamp
            # makes a lone sentinel believe it has a twin and fire without the
            # discipline (which fails toward the PARENT's behaviour, so it is
            # the safe direction -- but it is still wrong, and a plank whose
            # instrument reads "twin" when there is no twin cannot be measured).
            bits &= ~(FS_V517_STAMP_MASK << FS_V517_PEER_SHIFT)
        if publish:
            bits = ((bits & ~((FS_V517_STAMP_MASK << FS_V517_VERDICT_SHIFT)
                              | (FS_V517_NETCODE_MASK
                                 << FS_V517_NETCODE_SHIFT)))
                    | (stamp << FS_V517_VERDICT_SHIFT)
                    | (code << FS_V517_NETCODE_SHIFT))
        if FS_V517_FIREDISC_LOG:
            try:
                print("FIREDISC517", rnd, "at", (p.x, p.y), "hp", hp,
                      "ti", ct.get_global_resources(),
                      "ammo", ct.get_global_ammo(),
                      "win", len(win), "shots", self.v517_shots,
                      "net", net, "code", code,
                      "twin", 1 if twin else 0,
                      "peer", n_peer, "pub", 1 if publish else 0,
                      "hold", 1 if self.v517_hold_now else 0,
                      "held", self.v517_held, "heldfund", self.v517_held_fund,
                      "resets", self.v517_resets, "viol", self.v517_viol,
                      file=sys.stderr)
            except Exception:
                pass
        return bits

    def _v517_note_core_shot(self, ct):
        """Called by `_turret` the round it actually fires at an enemy core
        tile: the window advances on SHOTS, not on rounds."""
        self.v517_shots += 1
        hp = self.v517_hp_now
        if hp is None:
            return
        self.v517_win.append(hp)
        if len(self.v517_win) > FS_V517_NET_W:
            del self.v517_win[0]

    def _v517_count_hold(self, ct, fired_elsewhere):
        """Book one suppressed core shot.

        ⛔ THREE COUNTERS, BECAUSE "AMMO SAVED" IS THREE DIFFERENT CLAIMS.
          * `v517_held`       -- a core shot was legal and was skipped.
          * `v517_held_fund`  -- ...and the team could actually have PAID for
            it (>= 10 ammo).  `can_fire` returns TRUE at 0 ammo on this engine
            (guard-matrix sweep), so without this test the "saved" column would
            count shots that were never affordable.  10 x this is the saved
            ammunition, and titanium converts 1:1, so it is also the saved Ti.
          * `v517_held_only`  -- ...and nothing else was fired instead, i.e.
            the ammunition really stayed in the magazine rather than moving to
            another target.
        """
        try:
            self.v517_held += 1
            if ct.get_global_ammo() >= 10:
                self.v517_held_fund += 1
                if not fired_elsewhere:
                    self.v517_held_only += 1
        except Exception:
            pass

    def _fs_hold_live(self, ct):
        """RAID SIDE -- is a forward sentinel of ours HOLDING fire right now?

        This is the funding signal for the twin: the magazine is armed (v516
        GLOBALSENT keeps it armed under a live sentinel) and its only consumer
        is not spending, so the bank is provably accumulating.
        """
        if not (LOKI_FS_V517 and FS_V517_TWIN):
            return False
        # ⛔⛔ THE EXACT BEAT GATES THE MOD-15 CLOCK, AND THIS IS A MEASURED
        # FIX, NOT A BELT-AND-BRACES ONE.  The first smoke grid produced
        # TWINGATE lines in runs of FOUR spaced EXACTLY FIFTEEN ROUNDS APART
        # (r110-113, r125-128, r140-143, r155-158 ...) long after the sentinel
        # that wrote the verdict had died: a 4-bit mod-15 stamp that is never
        # rewritten reads age 0,1,2,3 once per wrap, FOR EVER.  `beat1` is an
        # exact round+1 field written by a unit that runs every round it lives,
        # so requiring it collapses the ghost to nothing -- and it is also the
        # honest semantics, because a hold by a dead sentinel is not a hold.
        if not self._fs_sent_beat_live(ct):
            return False
        try:
            v = ct.read_store(SLOT_SENT_BEAT)
            if ((v >> FS_V517_NETCODE_SHIFT) & FS_V517_NETCODE_MASK) \
                    != FS_V517_CODE_HELD:
                return False
            age = self._v517_stamp_age(
                (v >> FS_V517_VERDICT_SHIFT) & FS_V517_STAMP_MASK,
                ct.get_current_round())
            return age is not None and age <= FS_V517_NET_STALE
        except Exception:
            return False

    def _v517_twin_live(self, ct):
        """">= 2 forward sentinels of ours are alive", off the PEER stamp.

        Gated on the EXACT beat for the same reason `_fs_hold_live` is: a
        mod-15 stamp nobody rewrites reads fresh once per wrap for ever.
        """
        if not (LOKI_FS_V517 and FS_V517_TWIN):
            return False
        if not self._fs_sent_beat_live(ct):
            return False
        try:
            age = self._v517_stamp_age(
                (ct.read_store(SLOT_SENT_BEAT) >> FS_V517_PEER_SHIFT)
                & FS_V517_STAMP_MASK, ct.get_current_round())
            return age is not None and age <= FS_V517_NET_STALE
        except Exception:
            return False

    def _v517_bank_open(self, ct):
        """CORE SIDE, v517 change 2b -- should the Core stop converting and let
        the twin's price accumulate?

        ⛔ THIS MUTATES `v517_bank_until` AND IS CALLED FROM THE CORE'S TURN
        ONLY, once per round, from the one `fs_live` branch in `_core`.  A
        LATCH rather than a level test: the HOLD_TTL re-probe clears the
        verdict for the shots it takes to re-measure, and a Core that released
        the reserve on every probe would convert the part-built bank into
        ammunition and never reach the sentinel's price.
        """
        if not (LOKI_FS_V517 and FS_V517_TWIN and FS_V517_TWINBANK):
            return False
        try:
            rnd = ct.get_current_round()
        except Exception:
            return False
        if self._v517_twin_live(ct):
            self.v517_bank_until = -1        # the twin exists: stop banking
            return False
        if self._fs_hold_live(ct):
            self.v517_bank_until = rnd + FS_V517_BANK_TTL
        open_now = rnd < self.v517_bank_until
        if FS_V517_BANK_LOG and open_now:
            try:
                print("TWINBANK517", rnd, "ti", ct.get_global_resources(),
                      "ammo", ct.get_global_ammo(),
                      "sen", ct.get_sentinel_cost(),
                      "bought", ct.read_store(SLOT_FWD_GUN),
                      "until", self.v517_bank_until, file=sys.stderr)
            except Exception:
                pass
        return open_now

    def _v517_sent_floor(self, ct):
        """(ti_floor, rebuy_extra) for a sentinel purchase -- relaxed ONLY in
        the hold state.  READ SITE, never a module-level derived default
        (v515 finding 3)."""
        if LOKI_FS_V517 and FS_V517_TWIN and self._fs_hold_live(ct):
            return FS_V517_TWIN_TI_FLOOR, FS_V517_TWIN_REBUY_TI
        return FS_SENTINEL_TI_FLOOR, FS_SENT_REBUY_TI

    def _fs_sent_beat_live(self, ct):
        """⭐⭐ v516 CHANGE 2 -- ">= 1 forward sentinel of ours is ALIVE", read
        off the beat the sentinel itself writes (main.py `_turret`).

        Team-global: no unit's vision is involved, so the raider being dead
        stops mattering.  The store is buffered by exactly one round and a live
        sentinel runs every round, so a fresh beat is never older than 1;
        FS_SENT_BEAT_STALE = 3 is two rounds of slack for a CPU-timeout turn.
        """
        if not (LOKI_FS_V516 and FS_V516_GLOBALSENT):
            return False
        try:
            v = ct.read_store(SLOT_SENT_BEAT)
            beat = (v >> FS_SENT_BEAT_SHIFT) & FS_SENT_BEAT_MASK
            if beat <= 0:
                return False
            return ct.get_current_round() - (beat - 1) <= FS_SENT_BEAT_STALE
        except Exception:
            return False

    def _fs_live_sentinels(self, ct, E):
        # ⛔ MAX, NOT REPLACE, and it is what keeps the purchase cap honest.
        # The beat is a >=1 answer; the vision census can see 2.  Taking the
        # larger can never UNDER-count (which would arm nothing) and can never
        # push a 0-or-1 vision read up to FS_SENTINEL_MAX = 2 (which would
        # block a purchase we want).
        if LOKI_FS_V516 and FS_V516_GLOBALSENT and self._fs_sent_beat_live(ct):
            return max(1, self._fs_live_sentinels_vision(ct, E))
        return self._fs_live_sentinels_vision(ct, E)

    def _fs_live_sentinels_vision(self, ct, E):
        n = 0
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.SENTINEL:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                if dsq_core(ct.get_position(bid), E) <= 40:
                    n += 1
        except Exception:
            return n
        return n

    # --- v514 CHANGE B: RESITE-ON-DEATH -------------------------------------

    def _fs_sent_watch(self, ct, rnd):
        """Did a sentinel WE built stop existing?  MAGNUS RULING 2: "If it is
        killed make sure to get a sentry up somewhere else outside the line of
        enemy turrets."

        The tile is checked only when it is actually READABLE -- an unreadable
        tile is not evidence of a death, and scoring it as one would blacklist
        a site we never lost.  Bounds are tested explicitly before any
        `get_tile_*` (s50 probe: `is_in_vision` is a pure radius test and does
        NOT guard bounds).

        ⚠ PER-BODY MEMORY.  `fs_my_sents` dies with the body that bought the
        turret; a replacement raider starts blind and re-learns from
        `fs_sray` (which it rebuilds from its own vision) rather than from the
        death record.  The PURCHASE cap survives, because it is read off
        SLOT_FWD_GUN, which is team-wide and monotone.
        """
        if not (LOKI_FS_V514 and FS_V514_RESITE) or not self.fs_my_sents:
            return
        for rec in self.fs_my_sents:
            if rec[2]:
                continue                     # already scored dead
            t = Position(rec[0], rec[1])
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            try:
                if not ct.is_in_vision(t):
                    continue
                bid = ct.get_tile_building_id(t)
                if bid is not None \
                        and ct.get_entity_type(bid) == EntityType.SENTINEL \
                        and ct.get_team(bid) == self.team:
                    continue                 # still standing
            except Exception:
                continue
            rec[2] = 1
            self.fs_sent_lost += 1
            self.fs_dead_sents.append((rec[0], rec[1]))
            self._fs_log("SENTDEAD", rnd, "at", (rec[0], rec[1]),
                         "lost", self.fs_sent_lost)

    def _fs_site_veto(self, ct, bx, by, rnd):
        """(veto, penalty) for a candidate sentinel tile under change B.

        HARD veto once a sentinel of ours has died: any tile on a remembered
        ENEMY SENTINEL ray (permanent -- sentinels cannot rotate), and any tile
        within FS_SENT_DEADSITE_VETO of a tile one of ours died on.  Before the
        first loss the ray is a large PENALTY rather than a veto, because an
        absolute veto can leave `best is None` and buy nothing at all -- the
        same failure shape as the v513 prestand blacklist, which had to be
        given a fallback for exactly this reason.
        """
        pen = 0
        on_sray = (bx, by) in self.fs_sray
        if on_sray:
            if self.fs_sent_lost:
                return True, 0
            pen += FS_SENT_RAY_PENALTY
        if self.fs_sent_lost:
            for (dx0, dy0) in self.fs_dead_sents:
                if (bx - dx0) ** 2 + (by - dy0) ** 2 <= FS_SENT_DEADSITE_VETO:
                    return True, 0
        g = self.fs_gray.get((bx, by))
        if g is not None and rnd - g <= FS_RAY_GUN_MEM:
            pen += FS_SENTINEL_GUNAXIS_PENALTY
        return False, pen

    def _fs_salt_ok(self, ct, rnd, orth_open):
        """⭐ MAGNUS'S RULE, v513 change A: NO TURRET BEFORE THE SALT IS DOWN.

        The orthogonal-8 must be COMPLETE (`orth_open == 0`: every seat denied
        by a barrier, a body or a building of ours) before a sentinel may be
        bought, with a short grace window afterwards so a seat that flickers
        open does not cancel the second purchase mid-walk.

        Two reasons, one of them measured to the hit point: the eco builders
        need the opening bank, and pre-seal sentinel fire NETS ZERO -- 19,152
        damage dealt across 24 games, 16,962 healed straight back, in eight
        games EXACT (1,530 for 1,530 over 85 shots).  Ammunition spent before
        the healer is locked out is ammunition spent on nothing.

        ⛔ THE GATE IS ON THE PURCHASE ONLY.  A sentinel already standing keeps
        firing whatever happens to the collar afterwards.
        """
        if not (LOKI_FS_CREW and FS_SALT_GATE):
            return True
        if orth_open == 0:
            self.fs_sealed_rnd = rnd
            return True
        # ⭐ CREW-WIDE, NOT PER-BODY.  The census is read from the asking body's
        # own vision, so the support standing on the far arc can score a seat
        # "not denied" that the sealer can see is barriered -- a per-body latch
        # would gate the SECOND sentinel on the wrong body's eyes.  The
        # published phase is the crew's shared answer: SEALED (or KILL) means
        # some body of ours saw the orthogonal-8 closed this round.
        try:
            _b, ph, _r = self._fs_state(ct)
            if FS_PH_SEALED <= ph <= FS_PH_KILL:
                self.fs_sealed_rnd = rnd
                return True
        except Exception:
            pass
        if self.fs_sealed_rnd is None:
            return False
        if FS_SALT_LATCH:
            return True                  # the flagged-off variant: has-been
        return rnd - self.fs_sealed_rnd <= FS_SALT_GRACE

    def _fs_sentinel_ok(self, ct, ti, needed, orth_open):
        """May we spend a turret this round?  The seal is paid for first."""
        live = self._fs_live_sentinels(ct, self.enemy) if self.enemy else 0
        if live >= FS_SENTINEL_MAX:
            return False
        if LOKI_FS_V515 and FS_V515_GATE_OR:
            # ⭐⭐ v515 CHANGE 2 -- THE GATE IS A DISJUNCTION.
            #   salt-complete  OR  (conn2 AND round >= FS_SENT_RND_FLOOR)
            # WHY, and both halves come out of the parent's build report rather
            # than out of a preference:
            #   * v514's gate (conn2 alone) was measured SATISFIED AT r7-24 on
            #     4 of 5 maps -- "in practice change A REMOVES the turret gate
            #     rather than re-timing it" (report finding 1) -- and the
            #     configuration scored 23/60 against a 37/60 control.
            #   * v513's gate (salt alone) never fires at all on atoll and
            #     midgard: the collar closed 0 of 12 there because their
            #     delivery belt sits on the heal seats and a barrier can never
            #     take an occupied tile (closure autopsy).  Zero sentinels on
            #     exactly the two maps we lose.
            # The disjunction keeps v513's timing wherever the collar closes
            # (the salt disjunct fires first, and it is the timing the
            # parent-with-door-off config scored 53/90 on) and gives the belted
            # maps a turret at the floor instead of never.
            # ⛔ THE FLOOR IS ON THE ECO DISJUNCT ONLY.  A closed collar is
            # already the expensive fact; making it wait would re-introduce the
            # v510 lock the salt grace exists to avoid.
            try:
                rnd = ct.get_current_round()
            except Exception:
                return False
            salt = self._fs_salt_ok(ct, rnd, orth_open)
            eco = (self._fs_eco_gate_ok(ct) and rnd >= FS_SENT_RND_FLOOR)
            # WHICH DISJUNCT WAS OPEN, carried to the purchase site so the
            # purchase-vs-latch table is read off ONE instrument in both arms.
            self.fs515_gate = (rnd, 1 if salt else 0, 1 if eco else 0,
                               orth_open)
            if FS_GATE_LOG:
                # ⛔ NOT `_fs_log`: that is gated on FS_LOG, which turns on the
                # whole siege trace.  A mechanism arm must be able to read ONE
                # instrument without changing the volume of everything else.
                try:
                    print("GATE515", rnd, "salt", 1 if salt else 0,
                          "eco", 1 if eco else 0, "orth", orth_open,
                          "floor", FS_SENT_RND_FLOOR, file=sys.stderr)
                except Exception:
                    pass
            if not (salt or eco):
                return False
        elif LOKI_FS_V514 and FS_V514_ECOGATE:
            # ⭐⭐ v514 CHANGE A -- MAGNUS RULING 2, SUPERSEDING v513's CHANGE A.
            # "We can allow the first sentry as soon as 2 harvestors are built
            # and connected, otherwise we cannot sustain them."  The v513 gate
            # was orth_open == 0 (the salt) and it produced a turret in 27% of
            # games and ZERO on atoll and midgard, where the collar closed 0 of
            # 12 times and which are the two maps we lose.
            # ⛔ THE GATE TIMES THE TURRET; IT DOES NOT STOP THE SEALING.  The
            # ladder is unchanged, so barriers (rung 1) and the evictor (rung
            # 2) still outrank the sentinel (rung 4) every round they are
            # actionable -- Magnus ruling 1's order is enforced by the LADDER,
            # not by this predicate.
            if not self._fs_eco_gate_ok(ct):
                return False
        elif LOKI_FS_CREW and FS_SALT_GATE:
            try:
                rnd = ct.get_current_round()
            except Exception:
                return False
            if not self._fs_salt_ok(ct, rnd, orth_open):
                return False
        if live >= 1:
            # ⭐ UNDER THE LADDER THE SECOND SENTINEL IS GATED BY THE RESERVE,
            # NOT BY `orth_open == 0`.  The ORDERING already protects the
            # collar: rung 4 only runs on a round where rungs 1-3 had nothing
            # actionable, so requiring a closed collar on top of that is the
            # v510 failure re-stated (a contested near face keeps `needed`
            # non-empty for ever and the only thing that wins is never bought).
            # Magnus asked for two; the reserve below is what keeps the second
            # from being bought out of the barrier budget.
            if not (LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER):
                return orth_open == 0
        if not FS_SENTINEL_EARLY:
            return orth_open == 0
        # ⭐⭐ v517 CHANGE 2 -- THE COLLAR RESERVE IS A REPAIR ALLOWANCE WHILE
        # WE ARE HOLDING.  Same argument as v513 change F's
        # FS_MAG_REPAIR_BARRIERS: a sentinel is only standing at all once the
        # collar was CLOSED, so pricing a fresh eight-seat ring on top of the
        # twin is pricing a purchase that cannot be pending.  Outside the hold
        # state this line is the parent's, unchanged.
        _v517_floor, _v517_rebuy = self._v517_sent_floor(ct)
        _n_needed = len(needed)
        if LOKI_FS_V517 and FS_V517_TWIN and self._fs_hold_live(ct):
            _n_needed = min(_n_needed, FS_V517_TWIN_NEEDED_CAP)
        try:
            reserve = _n_needed * ct.get_barrier_cost() + ct.get_sentinel_cost()
        except Exception:
            return False
        return ti >= reserve + _v517_floor

    def _fs_gun_axis(self, ct):
        """Tiles a VISIBLE enemy gunner is already pointed at.

        `get_attackable_tiles_from` is the engine's own hypothetical-turret
        pattern; the chassis uses the identical read in `_raid_station` because
        92% of our forward builder deaths are enemy gunners.
        """
        axis = set()
        # ⭐ SEAL-ONLY ALSO READS ENEMY SENTINELS.  v510 lost three units on one
        # tile to one turret and `_fs_gun_axis` covered GUNNERS only.  A gunner
        # ray dies on any interposed body, so our own collar shields us from
        # those; a SENTINEL ray ignores obstacles entirely, which makes its axis
        # the one set a stand-tile choice can actually avoid.  Read off the
        # engine's own hypothetical-turret pattern, never inferred from damage.
        kinds = (EntityType.GUNNER, EntityType.SENTINEL) \
            if LOKI_FS_SEAL_ONLY else (EntityType.GUNNER,)
        try:
            for bid in ct.get_nearby_buildings():
                kind = ct.get_entity_type(bid)
                if kind not in kinds:
                    continue
                if ct.get_team(bid) == self.team:
                    continue
                gp = ct.get_position(bid)
                gd = ct.get_direction(bid)
                for t in ct.get_attackable_tiles_from(gp, gd, kind):
                    axis.add((t.x, t.y))
        except Exception:
            return axis
        return axis

    def _fs_sent_reach_tile(self, ct, E, rnd):
        """⭐⭐ v516 CHANGE 3 -- THE TILE THE FORWARD SENTINEL *SHOULD* BE ON.

        `_fs_try_sentinel` maximises its standoff score over the <=4 tiles
        orthogonally adjacent to the raider, and the raider stands ON the ring
        -- where FS_SENTINEL_OFFRING then excludes its own neighbours, the
        v514 site veto excludes more, and `can_fire_from` excludes the rest.
        7 of 30 games buy no forward sentinel at all with the gate open and
        the bank full (autopsy #2, atoll_s1_A: bank 90-116, gate open at r180,
        seven sentinels built, none forward).  This is the same objective
        evaluated over EVERY off-ring tile in range, so the walker can be told
        where to stand -- the purchase-side twin of v515 change 3.

        ⛔ LEGALITY IS APPROXIMATE AND THAT IS DELIBERATE, exactly as in
        `_fs_reach_tile`: `can_build_sentinel` requires orthogonal adjacency to
        the asking body and is False for every tile this scan is about.  What
        IS used is `can_fire_from`, which is position-only by contract -- and
        it is the half that actually decides, because an unaligned site is a
        turret that fires at nothing (Jython g1: the aligned sentinel took all
        504 damage, its neighbour one shot at an unrelated target in sixty
        rounds).  A tile that turns out to be unbuildable costs a preference,
        not a build.

        ⛔ CPU.  This is the only unbounded scan in the plank, so it is capped
        three ways: cached for FS_SENT_REACH_RECHECK rounds, at most
        FS_SENT_REACH_MAX_TILES candidates taken nearest-the-ring first, and a
        hard abort at FS_SENT_REACH_CPU_US microseconds of the 10 ms turn.

        Returns Position or None.
        """
        cached = self.fs516_reach
        if cached is not None and rnd - cached[1] < FS_SENT_REACH_RECHECK:
            return cached[0]
        best, best_k = None, None
        try:
            tiles = core_tiles(E)
            ladder = LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER
            ringset = set()
            if ladder and FS_SENTINEL_OFFRING:
                ring, _seats = self._fs_ring12(E)
                ringset = set((t.x, t.y) for t in ring)
            gun_axis = self._fs_gun_axis(ct)
            # Nearest-the-ring first, so the CPU cap truncates the FAR tail
            # rather than an arbitrary row of the bounding box.
            cand = []
            r = 6                    # d^2 <= 32 -> |dx|, |dy| <= 5 (+1 slack)
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    bx, by = E.x + dx, E.y + dy
                    if not (0 <= bx < self.mw and 0 <= by < self.mh):
                        continue
                    bp = Position(bx, by)
                    d = dsq_core(bp, E)
                    if d == 0 or d > 32:
                        continue
                    if d <= FS_RING_DSQ and ringset:
                        continue     # OFFRING: the collar owns these seats
                    if (bx, by) in ringset:
                        continue
                    if self._fs_wall(bp):
                        continue
                    cand.append((d, bx, by))
            cand.sort()
            del cand[FS_SENT_REACH_MAX_TILES:]
            for d, bx, by in cand:
                try:
                    if ct.get_cpu_time_elapsed() > FS_SENT_REACH_CPU_US:
                        break
                except Exception:
                    pass
                bp = Position(bx, by)
                site_pen = 0
                if LOKI_FS_V514 and FS_V514_RESITE:
                    vetoed, site_pen = self._fs_site_veto(ct, bx, by, rnd)
                    if vetoed:
                        continue
                # position-only occupancy: a tile with a building on it is not
                # a sentinel site.  Out of vision reads raise; unreadable is
                # NOT evidence of a blocker, so it stays a candidate.
                try:
                    if ct.is_in_vision(bp) and not ct.is_tile_empty(bp):
                        continue
                except Exception:
                    pass
                aligned = False
                for target in tiles:
                    dd = bp.distance_squared(target)
                    if dd > 32 or dd == 0:
                        continue
                    facing = bp.direction_to(target)
                    if facing == Direction.CENTRE:
                        continue
                    try:
                        if ct.can_fire_from(bp, facing,
                                            EntityType.SENTINEL, target):
                            aligned = True
                            break
                    except Exception:
                        continue
                if not aligned:
                    continue
                score = d if FS_SENTINEL_FAR_FIRST else -d
                score -= site_pen
                if (bx, by) in gun_axis:
                    score -= FS_SENTINEL_GUNAXIS_PENALTY
                if best_k is None or score > best_k:
                    best, best_k = bp, score
        except Exception:
            best = None
        self.fs516_reach = (best, rnd)
        if FS_SENT_REACH_LOG:
            try:
                print("SREACH516", rnd, "tile",
                      (best.x, best.y) if best else None,
                      "score", best_k, file=sys.stderr)
            except Exception:
                pass
        return best

    def _fs_try_sentinel(self, ct, E, p):
        """ONE ALIGNED SENTINEL, and the alignment is checked BEFORE the spend.

        `can_fire_from(pos, direction, SENTINEL, core_tile)` is the engine's own
        hypothetical-turret predicate (it ignores ammo and cooldown by
        contract), which is exactly the question.  Jython g1 bought two
        sentinels one tile apart: the aligned one fired 28 core shots for all
        504 damage and the other fired ONCE, at an unrelated target, in sixty
        rounds.  Half the turret budget, zero core DPS -- that is what this
        gate costs nothing to avoid.

        Prefer CLOSE (their median killing site is d^2=9): a shorter ray is
        less likely to be the one the defender walks a body onto, and range is
        not scarce at d^2<=32.
        """
        if self._fs_live_sentinels(ct, E) >= FS_SENTINEL_MAX:
            return False
        # ⭐⭐ v517 CHANGE 2 -- THE TWIN'S GATES RELAX IN THE HOLD STATE ONLY.
        # `_v517_sent_floor` returns the parent's (FS_SENTINEL_TI_FLOOR,
        # FS_SENT_REBUY_TI) unless a forward sentinel of ours is holding fire,
        # in which case the bank is provably accumulating (the magazine is
        # armed and its only consumer is not spending) and the reserve those
        # two constants protect is not at risk.  Read at the READ SITE.
        _v517_floor, _v517_rebuy = self._v517_sent_floor(ct)
        try:
            cost = ct.get_sentinel_cost()
            if ct.get_global_resources() < cost + _v517_floor:
                return False
        except Exception:
            return False
        rnd = 0
        if LOKI_FS_V514 and FS_V514_RESITE:
            # ⛔ THE BANK GUARD ON REBUYS.  Magnus asked for a replacement, not
            # for an unbounded one: SLOT_FWD_GUN is a team-wide MONOTONE count
            # of sentinels bought (it survives the body that bought them), and
            # every purchase after the first also has to clear FS_SENT_REBUY_TI
            # on top of the ordinary floor so a rebuy cannot eat the collar.
            try:
                rnd = ct.get_current_round()
                bought = ct.read_store(SLOT_FWD_GUN)
                if bought >= FS_SENT_BUY_MAX:
                    return False
                if bought >= 1 and ct.get_global_resources() \
                        < cost + _v517_floor + _v517_rebuy:
                    return False
            except Exception:
                return False
        tiles = core_tiles(E)
        gun_axis = self._fs_gun_axis(ct)
        ladder = LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER
        ringset = set()
        sides = set()
        if ladder:
            # ⛔ "PARKED JUST OUTSIDE THE RING OF BARRIERS" -- Magnus, verbatim.
            # A ring seat spent on a turret is a seat the collar does not own,
            # at ten times the price and the same 2-damage peck to break.  The
            # sentinel does not need the seat: its ray IGNORES OBSTACLES and
            # shoots the core straight through our own barriers.
            if FS_SENTINEL_OFFRING:
                ring, _seats = self._fs_ring12(E)
                ringset = set((t.x, t.y) for t in ring)
            # ...and the second one stands on a DIFFERENT SIDE of the core from
            # any sentinel of ours already there: redundancy against a defender
            # who has solved one ray (field median forward-sentinel life is 8
            # rounds, 80% of the deaths to turret fire).
            try:
                for bid in ct.get_nearby_buildings():
                    if ct.get_entity_type(bid) != EntityType.SENTINEL:
                        continue
                    if ct.get_team(bid) != self.team:
                        continue
                    sp = ct.get_position(bid)
                    if dsq_core(sp, E) <= 40:
                        sides.add(((sp.x > E.x) - (sp.x < E.x),
                                   (sp.y > E.y) - (sp.y < E.y)))
            except Exception:
                sides = set()
        best, best_k, best_ray = None, None, None
        for dx, dy in CARD_DELTAS:
            bx, by = p.x + dx, p.y + dy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            if ladder and FS_SENTINEL_OFFRING and (bx, by) in ringset:
                continue
            site_pen = 0
            if LOKI_FS_V514 and FS_V514_RESITE:
                vetoed, site_pen = self._fs_site_veto(ct, bx, by, rnd)
                if vetoed:
                    continue
            bp = Position(bx, by)
            for target in tiles:
                d = bp.distance_squared(target)
                if d > 32 or d == 0:
                    continue
                facing = bp.direction_to(target)
                if facing == Direction.CENTRE:
                    continue
                try:
                    if not ct.can_fire_from(bp, facing, EntityType.SENTINEL, target):
                        continue
                    if not ct.can_build_sentinel(bp, facing):
                        continue
                except Exception:
                    continue
                # STANDOFF, not proximity: 52.3% of forward sentinels in the
                # field die, 80% of those to turret fire, median life 8 rounds.
                # Range inside d^2<=32 is free; a tile closer to their guns is
                # not.  A site on a visible enemy GUNNER's ray is scored down
                # hard -- that ray dies on any interposed body, so stepping off
                # it costs nothing and forces them to pay 10 Ti and a cooldown
                # to answer.
                score = d if FS_SENTINEL_FAR_FIRST else -d
                score -= site_pen            # v514 change B (0 when off)
                if (bx, by) in gun_axis:
                    score -= FS_SENTINEL_GUNAXIS_PENALTY
                if ladder and ((bx > E.x) - (bx < E.x),
                               (by > E.y) - (by < E.y)) in sides:
                    score -= FS_SENTINEL_SIDE_PENALTY
                if best_k is None or score > best_k:
                    best, best_k, best_ray = (bp, facing), score, target
        if best is None:
            return False
        bp, facing = best
        try:
            ct.build_sentinel(bp, facing)
        except Exception:
            return False
        try:
            ct.write_store(SLOT_FWD_GUN, ct.read_store(SLOT_FWD_GUN) + 1)
        except Exception:
            pass
        self.fs_sentinels += 1
        if FS_V517_TWIN_LOG:
            # v517 change 2's purchase instrument.  `hold` is the state THIS
            # purchase was gated under, `live` is the count it passed, so a
            # purchase attributable to the plank is `hold 1` with `live 1`.
            try:
                print("TWIN517", ct.get_current_round(),
                      "at", (bp.x, bp.y),
                      "hold", 1 if self._fs_hold_live(ct) else 0,
                      "live", self._fs_live_sentinels(ct, E),
                      "floor", _v517_floor, "rebuy", _v517_rebuy,
                      "ti", ct.get_global_resources(), "cost", cost,
                      "n", self.fs_sentinels, file=sys.stderr)
            except Exception:
                pass
        if LOKI_FS_V514 and FS_V514_RESITE:
            # [x, y, dead?] -- watched every ring round by `_fs_sent_watch`.
            self.fs_my_sents.append([bp.x, bp.y, 0])
        self._fs_draw_dot(ct, bp, 255, 255, 0)
        self._fs_draw_line(ct, bp, best_ray, 255, 255, 0)
        if FS_GATE_LOG:
            # v515 change 2's purchase instrument.  Independent of FS_LOG so a
            # gate arm reads the purchase table without the whole siege trace.
            try:
                _g = getattr(self, "fs515_gate", None)
                print("SENT515", ct.get_current_round(),
                      "at", (bp.x, bp.y), "n", self.fs_sentinels,
                      "gate", _g, "latch", self._fs_eco_latch(ct),
                      file=sys.stderr)
            except Exception:
                pass
        self._fs_log("SENTINEL", ct.get_current_round(), "at", (bp.x, bp.y),
                     "face", facing.name, "tgt", (best_ray.x, best_ray.y),
                     "score", best_k, "n", self.fs_sentinels,
                     "onring", 1 if (bp.x, bp.y) in ringset else 0,
                     "lost", self.fs_sent_lost,
                     "gate", self._fs_eco_latch(ct),
                     "onsray", 1 if (bp.x, bp.y) in self.fs_sray else 0,
                     "olddsq", (min(((bp.x - a) ** 2 + (bp.y - b) ** 2)
                                    for a, b in self.fs_dead_sents)
                                if self.fs_dead_sents else -1))
        return True

    # ------------------------------------------------------------------
    # THE LAUNCHER'S TURN
    # ------------------------------------------------------------------

    def _fs_launcher_turn(self, ct):
        """Returns True if the ferry-siege owns this launcher's turn.

        ⛔ ROLE BY SITE, and it is not cosmetic: the probe's integrated run had
        the RING launcher take the FERRY branch on our OWN sealer and throw it
        two tiles off the ring.  Ferry launcher and eviction launcher are the
        same entity type doing opposite jobs, so any launcher of ours within
        d^2<=FS_RING_DSQ of the ENEMY core is EVICTION-ONLY, forever.
        """
        if not LOKI_FERRY_SIEGE_ON:
            return False
        if not (self.mw and self.mh):
            return False
        E = self._enemy_anchor(ct)
        if E is None:
            return False
        if self.core is None:
            # A launcher sees r^2=26.  Every ferry link past the second one is
            # already outside that of our own core, so the incumbent's
            # look-around discovery never finds it.  `enemy_core_for` is an
            # involution (table lookup or point reflection, both self-inverse),
            # so applying it to the ENEMY anchor returns ours with no store slot
            # and no extra state -- the same trick `_bb_in_band` uses.
            self.core = enemy_core_for(self.mw, self.mh, E)
        if not self._fs_gate(ct):
            return False
        lp = ct.get_position()
        rnd = ct.get_current_round()
        if self.fs_born is None:
            self.fs_born = rnd

        if dsq_core(lp, E) <= FS_RING_DSQ:
            if not FS_EVICT_ON:
                return False
            self._fs_evict(ct, E, lp)
            return True                      # never ferries.  Ever.

        return self._fs_ferry_launcher(ct, E, lp, rnd)

    def _fs_sites(self, ct, lp):
        """Every legal throw destination: d^2 <= 26 from the launcher.

        Built ONCE -- a launcher is a building and never moves.  The incumbent
        rebuilt this ~81-Position list every round for the launcher's whole
        life.
        """
        key = (lp.x, lp.y)
        if self.fs_sites_key == key and self.fs_sites is not None:
            return self.fs_sites
        sites = []
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                if dx * dx + dy * dy > FS_HOP_DSQ:
                    continue
                tx, ty = lp.x + dx, lp.y + dy
                if 0 <= tx < self.mw and 0 <= ty < self.mh:
                    sites.append(Position(tx, ty))
        self.fs_sites = sites
        self.fs_sites_key = key
        return sites

    def _fs_ferry_launcher(self, ct, E, lp, rnd):
        """Throw OUR raider forward, then delete ourselves.

        Identification is POSITIVE: the raider publishes its own entity id in
        SLOT_FS every round it runs, and this launcher throws that id and
        nothing else.  It is what keeps the two eco builders -- who stand
        beside our own core in exactly the rounds the first hop is built -- out
        of the air.
        """
        # ⭐ v514 CHANGE D -- TWO PUBLISHED IDS, ONE PER CREW CHANNEL.  A ferry
        # link is ridden by whichever body reaches it, so it must be able to
        # identify EITHER of them; with one shared rid field the loser of the
        # store write is a body standing beside a paid-for launcher that
        # refuses to pick it up.  The POSITIVE-IDENTIFICATION property is
        # unchanged -- an id still has to have been published by a ferry-siege
        # body before it can be thrown, which is what keeps the two eco
        # builders (who stand beside our own core in exactly the rounds the
        # first hop is built) out of the air.
        # With the crew off `_fs_crew_slots()` is (SLOT_FS,) and this is the
        # parent's single-id read.
        want_ids = []
        for _s in self._fs_crew_slots():
            _b, _p, _r = self._fs_state_at(ct, _s)
            if _r and (_r - 1) not in want_ids:
                want_ids.append(_r - 1)
        target = self._fs_target(ct, E)
        if self.fs_thrown is None:
            self.fs_thrown = []
        relay = LOKI_FS_V514 and FS_V514_RELAY and FS_RELAY_ON \
            and LOKI_FS_CREW and FS_CREW_ON
        # THE LEAD GOES FIRST, and the probe measured it worth a round per hop:
        # the body on SLOT_FS is the one that BUYS THE NEXT LINK, so throwing
        # it first lets it land at R+1 and build at R+2 while this link still
        # has R+2 to throw body 2 -- a two-round cycle.  Throwing the other
        # body first measured a THREE-round cycle on the same map.
        lead_id = want_ids[0] if want_ids else None
        riders = []
        if want_ids:
            try:
                for eid in ct.get_nearby_units():
                    if eid not in want_ids or eid in self.fs_thrown:
                        continue
                    if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                        continue
                    if ct.get_team(eid) != self.team:
                        continue
                    bp = ct.get_position(eid)
                    if bp.distance_squared(lp) <= 2:
                        riders.append((0 if eid == lead_id else 1,
                                       bp.distance_squared(target), eid, bp))
            except Exception:
                riders = []
        me = None
        me_id = None
        if riders:
            riders.sort()
            me_id, me = riders[0][2], riders[0][3]
        if me is not None:
            self.fs_ferry_seen = True
            here = me.distance_squared(target)
            best = None
            for site in self._fs_sites(ct, lp):
                # STRICT IMPROVEMENT (`_v148ferryfirst/raid.py:693-708`): a
                # throw that does not get closer is a throw that undoes the
                # last one.
                d = site.distance_squared(target)
                if d >= here:
                    continue
                if LOKI_FS_V514 and FS_V514_RELAY and FS_HOP_RING_FIRST:
                    # ⭐⭐ THE TERMINAL HOP MUST LAND IN THE RING.  Measured on
                    # the closure autopsy: the midgard-B chain terminates at
                    # dsq_core = 13 -- outside FS_RING_DSQ = 8 -- in 5 of 6
                    # games; the walk-in from there fails and arrival slips to
                    # r78/123/187 against r5-r11 on every other map, 64 to 173
                    # rounds of a siege spent not being at the siege.  A site
                    # INSIDE the ring beats a site merely nearer the target
                    # tile, because being in the ring is what the whole hop
                    # chain is for.
                    k = (0 if dsq_core(site, E) <= FS_RING_DSQ else 1, d)
                else:
                    k = (0, d)
                if best is None or k < best[0]:
                    best = (k, site)
            if best is not None:
                site = best[1]
                thrown = False
                try:
                    if ct.can_launch(me, site):
                        self._fs_draw_line(ct, me, site, 0, 255, 120)
                        ct.launch(me, site)
                        thrown = True
                except Exception:
                    thrown = False
                if not thrown:
                    ring_first = (LOKI_FS_V514 and FS_V514_RELAY
                                  and FS_HOP_RING_FIRST)

                    def _key(t):
                        d = t.distance_squared(target)
                        if ring_first:
                            return (0 if dsq_core(t, E) <= FS_RING_DSQ else 1,
                                    d)
                        return (0, d)
                    for site in sorted(self._fs_sites(ct, lp), key=_key):
                        # ⛔ `continue`, NOT `break`.  Under the ring-first key
                        # the list is no longer sorted by distance alone, so a
                        # non-improving site is not proof that every later one
                        # is non-improving too.
                        if site.distance_squared(target) >= here:
                            continue
                        try:
                            if ct.can_launch(me, site):
                                self._fs_draw_line(ct, me, site, 0, 255, 120)
                                ct.launch(me, site)
                                thrown = True
                                break
                        except Exception:
                            continue
                if thrown:
                    self.fs_thrown.append(me_id)
                    self.fs516_last_throw = rnd     # v516 change 1b clock
                    self._fs_log("THROW", rnd, "from", (me.x, me.y),
                                 "to", (site.x, site.y), "T", (target.x, target.y),
                                 "body", me_id, "n", len(self.fs_thrown),
                                 "dsq", dsq_core(site, E))
                    # ⭐ v514 CHANGE D -- HOLD THE LINK OPEN FOR THE SECOND
                    # RIDER.  Magnus's rule: "both builders need to be launched
                    # before the launcher can be destroyed and a new launcher
                    # can be built."  A throw costs the launcher cooldown += 1
                    # and cooldowns decrement at END of round, so this link may
                    # throw again NEXT round but never twice in this one -- the
                    # whole relay is that one fact.  Tearing down after one
                    # throw is what strands body 2 five tiles behind with its
                    # own launcher to buy, which is the parallel-chain
                    # behaviour the probe removed.
                    hold = (relay
                            and any(i not in self.fs_thrown for i in want_ids)
                            and rnd - self.fs_born < FS_RELAY_TTL)
                    if LOKI_FS_V516 and FS_V516_TEARDOWN \
                            and FS_V516_HOLD_GENERAL:
                        # ⭐ v516 CHANGE 1a -- THE HOLD IS GENERALISED OFF THE
                        # CREW FLAG.  Magnus's rule is "both builders need to
                        # be launched before the launcher can be destroyed";
                        # the general form is ALL EXPECTED RIDERS, where the
                        # expected riders are the live published crew bodies --
                        # `want_ids`, which is 1 long in the fired config and 2
                        # with the crew on.  The parent ANDs this with `relay`,
                        # i.e. with FS_CREW_ON, so the predicate is wired to a
                        # flag rather than to the rider count.
                        # ⚠ AND IT IS HONEST THAT THIS CHANGES NOTHING HERE.
                        # With one rider, `any(i not in self.fs_thrown ...)` is
                        # False the moment that rider is thrown, so both forms
                        # tear down on the throw round.  The behavioural target
                        # of change 1 is part (b) below, not this.
                        hold = (any(i not in self.fs_thrown
                                    for i in want_ids)
                                and rnd - self.fs_born < FS_RELAY_TTL)
                    # ⛔ NOTHING MAY FOLLOW THIS CALL.  self_destruct() does not
                    # return and raises nothing catchable; `finally:`,
                    # `except BaseException` and `except SystemExit` are all
                    # rejected by the sandbox AST validator at load time.  The
                    # +10% scale contribution is returned on the next round's
                    # reading, which is what keeps a six-hop chain costing +10%
                    # instead of +60% on the price of the sentinel that has to
                    # finish the game.  (Engine-confirmed on the probe's trace:
                    # scale oscillates 190 <-> 200 all chain long.)
                    if not hold:
                        ct.self_destruct()
                    return True

        if not self.fs_ferry_seen:
            # ⭐⭐ v516 CHANGE 1b -- THE IDLE-FORWARD TEARDOWN.  This early
            # return is what makes the ferry TTL below UNREACHABLE for every
            # launcher that never had a rider under its hand: a hop link whose
            # rider died, and every chassis home-doctrine launcher a roaming
            # builder planted forward.  Measured on the autopsy's own 30
            # replays: 71 launchers with life >= 20, of which 66 were never
            # built by `_fs_build_ferry` at all, two games reaching 16 and 22
            # live launchers -- and each of them holds +10% of the ONE GLOBAL
            # ADDITIVE scale factor for the rest of the match.
            # ⛔ THE THREE GUARDS ARE THE WHOLE SAFETY ARGUMENT:
            #   * we are OUTSIDE the ring (the ring branch returned above), so
            #     evictors -- whose job IS to stand -- are never in scope;
            #   * we are beyond FS_V516_IDLE_OWN_DSQ of OUR OWN core, so the
            #     LOKI-42 home-defence launcher is never in scope (s30 measured
            #     removing home defence as a REAL NEGATIVE);
            #   * nothing has been thrown for FS_V516_IDLE_TTL rounds, counting
            #     home-doctrine EXILE throws as well as ferry hops, so a
            #     launcher doing useful work is never in scope.
            # ⛔ AND IT RETURNS FALSE EITHER WAY.  Claiming the turn would take
            # the home doctrine's exile away from a launcher we are choosing
            # NOT to tear down this round; `self_destruct()` never returns, so
            # the only round this branch changes control flow is the last one.
            if LOKI_FS_V516 and FS_V516_TEARDOWN and FS_V516_IDLE_ON \
                    and self.core is not None:
                idle_from = self.fs516_last_throw
                if idle_from is None:
                    idle_from = self.fs_born
                if rnd - idle_from >= FS_V516_IDLE_TTL \
                        and lp.distance_squared(self.core) \
                        > FS_V516_IDLE_OWN_DSQ:
                    self._fs_log("IDLETEAR", rnd, "at", (lp.x, lp.y),
                                 "born", self.fs_born,
                                 "lastthrow", self.fs516_last_throw,
                                 "downsq", lp.distance_squared(self.core),
                                 "dopp", dsq_core(lp, E))
                    if FS_TEARDOWN_LOG:
                        try:
                            print("IDLETEAR516", rnd, "at", (lp.x, lp.y),
                                  "born", self.fs_born,
                                  "lastthrow", self.fs516_last_throw,
                                  "downsq", lp.distance_squared(self.core),
                                  "dopp", dsq_core(lp, E), file=sys.stderr)
                        except Exception:
                            pass
                    ct.self_destruct()
            return False                     # not ours: the home launcher path
        # A link that has ALREADY thrown is holding open only for its second
        # rider and the chain cannot advance past it, so its patience is
        # FS_RELAY_TTL rather than the full FS_LAUNCHER_TTL.  A link that has
        # thrown nobody keeps the incumbent's TTL.
        ttl = FS_LAUNCHER_TTL
        if relay and self.fs_thrown:
            ttl = FS_RELAY_TTL
        if rnd - self.fs_born >= ttl:
            ct.self_destruct()
        return True

    def _fs_evict(self, ct, E, lp):
        """Throw ARRIVING ENEMY BUILDERS away from their own core.

        ⛔ TEAM FILTER, and it is the single most valuable line in this file.
        `can_launch` has no team check.  The 2174-rated implementation does not
        filter, and in the two games where its ring launcher juggled its own
        raider 57 and 28 times the ring finished 7/12 and 7/12; in the two
        games with 2 and 3 own-throws it finished 12/12 and 12/12.

        Victim order: a HEALER STANDING ON A SEAT first -- it both heals and
        blocks the barrier we want on that tile, so the throw does two jobs.
        Destination: farthest from THEIR core, border tiles preferred (the
        approved crash channel rides along for free against unguarded bots),
        and NEVER inside FS_DUMP_MIN_OWN_DSQ of OUR core -- their §4.2 defect
        air-dropped the enemy siege team onto their own doorstep.

        ⭐ AND THE THROW IS EXPLICITLY LONG.  Over 12,652 measured displacement
        events, a victim thrown >5.5 tiles returns 33.4% of the time after a
        median 33-round walk-back; one thrown 3.5-5.5 tiles -- which is what
        "farthest site from the LAUNCHER" produces -- returns 58.7% of the time
        after a median 11.  Same launcher, ~3x the dwell, and the >=6-tile dump
        is legal from 54-86% of candidate placements on real maps.  So the
        first pass demands it and the second pass takes what it can get.
        """
        try:
            seats = set((s.x, s.y) for s in heal_seats(E, self.mw, self.mh))
        except Exception:
            seats = set()
        victims = []
        try:
            for eid in ct.get_nearby_units():
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                if ct.get_team(eid) == self.team:
                    continue                 # ⛔ THE TEAM FILTER
                bp = ct.get_position(eid)
                if bp.distance_squared(lp) > 2:
                    continue
                victims.append(bp)
        except Exception:
            return
        if not victims:
            return
        victims.sort(key=lambda b: (0 if (b.x, b.y) in seats else 1,
                                    dsq_core(b, E)))
        w, h = self.mw, self.mh
        C = self.core
        key = (lp.x, lp.y, E.x, E.y)
        if self.fs_dump_key != key or self.fs_dump is None:
            cands = []
            for t in self._fs_sites(ct, lp):
                if C is not None and t.distance_squared(C) < FS_DUMP_MIN_OWN_DSQ:
                    continue
                border = 1 if (t.x == 0 or t.y == 0 or t.x == w - 1
                               or t.y == h - 1) else 0
                cands.append((-dsq_core(t, E), -border, t))
            cands.sort(key=lambda it: (it[0], it[1]))
            self.fs_dump = [c[2] for c in cands]
            self.fs_dump_key = key
        for bp in victims:
            for far_only in (True, False):
                for site in self.fs_dump:
                    if far_only and bp.distance_squared(site) < FS_DUMP_FAR_DSQ:
                        continue
                    try:
                        if not ct.can_launch(bp, site):
                            continue
                        self._fs_draw_line(ct, bp, site, 255, 0, 0)
                        ct.launch(bp, site)
                        self.fs_evicts += 1
                        self._fs_log("EVICT", ct.get_current_round(),
                                     "from", (bp.x, bp.y), "to", (site.x, site.y))
                        return
                    except Exception:
                        continue

    # ------------------------------------------------------------------
    # replay indicators -- Magnus watches this file's output in the viewer
    # ------------------------------------------------------------------

    def _fs_draw_dot(self, ct, pos, r, g, b):
        if not FS_DRAW_ON:
            return
        try:
            ct.draw_indicator_dot(pos, r, g, b)
        except Exception:
            return

    def _fs_draw_line(self, ct, a, b, r, g, bl):
        if not FS_DRAW_ON:
            return
        try:
            ct.draw_indicator_line(a, b, r, g, bl)
        except Exception:
            return
