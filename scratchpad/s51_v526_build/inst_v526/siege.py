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
    _decode_grid, core_corners, core_tiles, dsq_core, enemy_core_for,
    heal_seats, known_map_for, unpack_pos,
)

# v524 CHANGE 1 -- the two CONFIRMED cripple grids, decoded once at import
# with the exact same house routine `known_map_for` uses for every other
# same-signature map collision (`eco.py:121-134`).  See doctrine.py's
# LOKI-FS-V524 block for the full account of the bug this closes.
FS_V524_CRIPPLE_GRIDS = frozenset((
    _decode_grid(FS_V524_MIDGARD_CODE, 30, 30),
    _decode_grid(FS_V524_YULERUNE_CODE, 20, 20),
))

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
                (v >> FS_RID_SHIFT) & FS_RID_FIELD_MASK)

    def _v520_arc_at(self, ct, slot):
        """The ARC a body has claimed on `slot`, or FS_V520_ARC_NONE.

        v520 change 1.  Bits 30-31 of the same word; see FS_V520_ARC_SHIFT for
        why not 28-29.  Returns NONE whenever the plank is off, so every
        consumer degrades to the parent's undifferentiated seat order.
        """
        if not (LOKI_FS_V520 and FS_V520_PINCER and FS_V520_ARC_PUBLISH):
            return FS_V520_ARC_NONE
        try:
            v = ct.read_store(slot)
        except Exception:
            return FS_V520_ARC_NONE
        return (v >> FS_V520_ARC_SHIFT) & FS_V520_ARC_MASK

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
        word = (((rnd + 1) & FS_BEAT_MASK)
                | ((phase & FS_PHASE_MASK) << FS_PHASE_SHIFT)
                | (((rid + 1) & FS_RID_FIELD_MASK) << FS_RID_SHIFT))
        if LOKI_FS_V520 and FS_V520_PINCER and FS_V520_ARC_PUBLISH:
            # ⭐ v520 CHANGE 1 -- THE ARC CHANNEL RIDES THE BODY'S OWN SLOT.
            # One writer per slot is the r197 discipline and this adds no
            # second writer: `_fs_slot()` already routes body 2 to
            # FS_SUPP_SLOT, so each body stamps only its own word.
            word |= ((getattr(self, "v520_arc", FS_V520_ARC_NONE)
                      & FS_V520_ARC_MASK) << FS_V520_ARC_SHIFT)
        try:
            ct.write_store(self._fs_slot(), word)
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
        if LOKI_FS_V514 and FS_V514_RELAY and LOKI_FS_CREW and fs_crew_on() \
                and getattr(self, "fs_body", 1) == 2:
            return FS_SUPP_SLOT
        return SLOT_FS

    def _fs_crew_slots(self):
        """Every slot a ferry-siege body of ours may be publishing into."""
        if LOKI_FS_V514 and FS_V514_RELAY and LOKI_FS_CREW and fs_crew_on():
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
                and fs_crew_on():
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
                and fs_crew_on():
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
        # ⭐ v525 CHANGE 2 -- STANDDOWN FLIP, dim/dsq floors.  Read at RUNTIME,
        # never at module scope (doctrine.py's own append-ordering note).
        # `False` reproduces the parent's v510-era thresholds exactly.
        min_dim = FS_V525_MIN_MAP_DIM if LOKI_FS_V525 else FS_MIN_MAP_DIM
        min_dsq = FS_V525_MIN_CORE_DSQ if LOKI_FS_V525 else FS_MIN_CORE_DSQ
        if max(mw, mh) < min_dim:
            ok = False
        elif ours.distance_squared(E) < min_dsq:
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
        if ok and LOKI_FS_V519 and FS_V519_MODESWITCH:
            # ⭐ v519 CHANGE 2 -- MODESWITCH.  A board on the registered CRIPPLE
            # list plays the chassis' own beltbreak+home game, which is exactly
            # the state a GATED board already reaches: refusing here is not a
            # new stand-down path, it is the SAME one.  The signature is
            # recomputed rather than reused because the block above is itself
            # conditional (FS_MAP_SKIP_ON, LOKI_FS_SEAL_ONLY, LOKI_FS_RING_LADDER)
            # and this clause must not inherit another flag's gating.
            sig519 = (mw, mh,
                      min((ours.x, ours.y), (E.x, E.y)),
                      max((ours.x, ours.y), (E.x, E.y)))
            # ⭐ v525 CHANGE 1 -- STANDDOWN FLIP, cripple-list.  Read at
            # RUNTIME, never at module scope. `False` reproduces the parent's
            # coarse candidate set exactly (midgard AND yulerune signatures).
            crip_maps = FS_V525_CRIPPLE_MAPS if LOKI_FS_V525 else FS_V519_CRIPPLE_MAPS
            if sig519 in crip_maps:
                cripple = True
                # ⭐ v524 CHANGE 1 -- EXACT MATCH.  `sig519` alone collides:
                # ragnarok shares midgard's (30,30,(2,2),(26,26)) and
                # frostgate shares yulerune's (20,20,(2,9),(16,9))
                # (PREREG-PINCERPOOL-2026-08-18.md finding 2). `False`
                # reproduces the parent's coarse-only match unchanged -- the
                # registered mutant. `True` demotes the coarse hit to a
                # CANDIDATE and confirms it against the actual tile grid,
                # exactly the way `known_map_for` already disambiguates every
                # other same-signature collision this tree ships.
                if LOKI_FS_V524:
                    grid = self.map_grid
                    # ⛔ DELIBERATELY NOT CACHED INTO `self.map_grid` HERE, ON
                    # ANY PATH.  `main._builder`'s own map_grid init
                    # (`main.py:1325-1341`) is GUARDED BY `if self.map_grid is
                    # None:` and, on the SAME round a unit's `self.core` first
                    # resolves, this gate can be asked FIRST -- the v521
                    # gatefix crew-seat read (`main.py:1283`) runs before that
                    # init block.  FOUND THE HARD WAY, by the byte-identity
                    # spot-check this build's own verification requires: an
                    # earlier draft of this fix cached here, which made that
                    # `if self.map_grid is None:` false before the walls/ores
                    # extraction ever ran, silently losing `self.map_walls`/
                    # `self.map_ores` for that unit for the rest of the match
                    # -- a live, ~830-round-earlier-kill divergence on midgard
                    # that should have been byte-identical to the parent
                    # (seed 524919 vs `_v488beltbreak2`, this build's own scratch
                    # battery). A correctness fix must not race a pre-existing
                    # initialiser for the SAME attribute.  Recomputing here
                    # costs a `known_map_for` call (tile-sense + compare, no
                    # re-decode -- `_decode_grid` is cache-memoised in eco.py)
                    # on any round asked before the official init resolves it;
                    # cheap, and it only happens on the 2 (v524) / 4 (parent)
                    # colliding-signature maps to begin with.  The one caller
                    # with no OTHER route to `self.map_grid` at all -- the v516
                    # turret beat (main.py), whose `self.core` is None by
                    # design -- pays this every round rather than once; still
                    # cheap by the same argument.
                    if grid is None and ct is not None:
                        grid = known_map_for(mw, mh, ours, ct)
                    cripple = grid is not None and grid in FS_V524_CRIPPLE_GRIDS
                    if FS_V524_LOG and ct is not None:
                        try:
                            print("V524", ct.get_current_round(), "sig", sig519,
                                  "grid_known", grid is not None,
                                  "confirmed", cripple, file=sys.stderr)
                        except Exception:
                            pass
                if cripple:
                    ok = False
                    if FS_V519_MODE_LOG and ct is not None:
                        try:
                            print("MODE519", ct.get_current_round(),
                                  "sig", sig519, "cripple 1", file=sys.stderr)
                        except Exception:
                            pass
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

        # ⭐ v520 CHANGE 1 -- THE ARC TERM.  Read ONCE per census, not per tile,
        # and only when the plank is on; `_v520_arc_of` is pure integer work
        # but the seat list is walked twice by `sort` and this is the hot path.
        my_arc = (getattr(self, "v520_arc", FS_V520_ARC_NONE)
                  if (self._v520_on() and FS_V520_ARC_SEAL)
                  else FS_V520_ARC_NONE)

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
            # ⭐ v520: MY ARC FIRST -- and FIRST, NOT ONLY.  This is an ORDERING
            # term inside the seat class, so when my arc has nothing actionable
            # left the other arc's seats are simply next in the list and get
            # sealed anyway.  A filter here would orphan seats whenever the peer
            # body died, which is the failure the presence change exists for.
            arcp = 0
            if my_arc != FS_V520_ARC_NONE:
                arcp = 0 if self._v520_arc_of(t, E) == my_arc else 1
            return (blocked, fresh, worn, pr, arcp, nw,
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
        if self._v520_appt_lost(ct, rnd):
            # ⛔ THE READBACK ARM OF THE APPOINTMENT GUARD.  Two bodies can
            # still CLAIM the support seat in the same round (the store is
            # buffered, so neither can see the other's write until next round);
            # what the guard guarantees is that exactly one of them KEEPS it.
            # The loser leaves the plank entirely rather than re-deriving
            # `fs_body`, because a body that flipped to 1 would start clobbering
            # the SEALER's slot -- the r197 defect with the sign reversed.
            self.fs_raider = False
            self.role = "raid"
            self._raid(ct)
            return
        E = self._enemy_anchor(ct)
        if E is None or not self._fs_active(ct):
            self._fs_degrade(ct, rnd)
            return
        p = ct.get_position()
        d = dsq_core(p, E)
        if V526RC:
            self._v526_arrive(ct, E, p, rnd)

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
        if LOKI_FS_V520 and FS_V520_PROBE_KILL_RND >= 0 \
                and rnd == FS_V520_PROBE_KILL_RND \
                and self.fs_arrived and self.fs_role == "seal":
            # VERIFICATION PROBE, NEVER SHIPPED (FS_V520_PROBE_KILL_RND = -1).
            # v513's forced-death method: kill the SEALER at a fixed round with
            # the game otherwise untouched, so replacement latency is a
            # measurement rather than a wait for a natural death that arrives
            # at a different round in every arm.
            try:
                print("PRESKILL520", rnd, "id", ct.get_id(),
                      "body", getattr(self, "fs_body", 1), file=sys.stderr)
            except Exception:
                pass
            ct.self_destruct()
        if at_ring and self._v520_on() and FS_V520_ARC_PUBLISH:
            # ⭐ v520 CHANGE 1 -- CLAIM THE ARC BEFORE THE CENSUS READS IT.
            # The census orders `needed` by arc, so the claim has to be settled
            # for this round before the ordering is computed.
            self._v520_claim_arc(ct, E, p, rnd)
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
                # ⭐⭐⭐ v521 CHANGE 1e -- `FS_PH_KILL` CONFLATES TWO FACTS AND
                # THIS BUILD'S WHOLE THESIS IS THAT THEY ARE DIFFERENT ONES.
                # As published by the parent, KILL means "a turret is alive" and
                # KILL_OPEN means "a turret is alive AND THE COLLAR HAS NEVER
                # CLOSED" (`fs_sealed_rnd is None`).  So a game whose collar
                # closed once at r30 and broke at r34 publishes KILL for the
                # next 900 rounds, and every consumer that asks the phase "is
                # the collar shut?" -- the magazine floor, `_fs_salt_ok`'s
                # crew-wide read, v521's own collar reserve -- is told YES on a
                # board where it is open.  ⛔ THAT IS THE SEAL-SHOT DISJOINTNESS
                # AS A DATA DEFECT: the two windows cannot be made to meet by
                # any consumer of a channel that cannot tell them apart.
                # The correction is to publish the CURRENT reading, which is the
                # word's own documented meaning ("a turret bought with the
                # collar STILL OPEN").
                if LOKI_FS_V521 and FS_V521_PHASE_HONEST and orth_open:
                    phase = FS_PH_KILL_OPEN
                elif LOKI_FS_V514 and FS_V514_ECOGATE \
                        and self.fs_sealed_rnd is None:
                    # A turret bought under Magnus ruling 2 with the collar
                    # still open.  The Core needs to know, because every
                    # magazine floor below FS_PH_KILL was written for a state
                    # that could only be reached AFTER a closure.
                    phase = FS_PH_KILL_OPEN
                # ⭐⭐⭐ v522 -- THE NEAR REFINEMENT.  Strictly narrower than the
                # two branches above: it can only fire in a round that already
                # published KILL or KILL_OPEN, and it hands the Core the ONE
                # fact it cannot see for itself.  The Core converts ammunition
                # and has no eyes at the enemy ring; the raider is standing on
                # the collar and has counted the open seats this round.
                if self._v522_near_publish(ct, rnd, orth_open):
                    phase = FS_PH_KILL_NEAR
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
            if (fs_crew_on() and self.fs_role == "supp"
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

    def _v526_arrive(self, ct, E, p, rnd):
        if not V526RC or getattr(self, 'v526_arrived', False):
            return
        try:
            _d = dsq_core(p, E)
        except Exception:
            return
        if _d > FS_RING_DSQ:
            return
        self.v526_arrived = True
        try:
            print('RC ARRIVE', rnd, 'id', ct.get_id(),
                  'body', getattr(self, 'fs_body', 1),
                  'dsq', _d, file=sys.stderr)
        except Exception:
            pass

    def _fs_ferry_turn(self, ct, E, p, rnd):
        T = self._fs_target(ct, E)
        lp = self._fs_pickup_launcher(ct, p)
        if self.fs_body_born is None:
            self.fs_body_born = rnd
        if V526RC and rnd <= V526RC_MAXRND:
            try:
                _m = self._fs_relay_mustered(ct, p, rnd)
                print('RC TEMPO', rnd, 'id', ct.get_id(),
                      'body', getattr(self, 'fs_body', 1),
                      'born', self.fs_body_born,
                      'lp', 1 if lp is not None else 0,
                      'must', 1 if _m else 0,
                      'why', getattr(self, 'v526_must_why', '-'),
                      'ride', self.fs_ride_rnd,
                      'ti', ct.get_global_resources(),
                      'lcost', ct.get_launcher_cost(),
                      'acd', ct.get_action_cooldown(),
                      'mcd', ct.get_move_cooldown(),
                      'pos', '%d,%d' % (p.x, p.y),
                      'dsq', dsq_core(p, E), file=sys.stderr)
            except Exception:
                pass

        # ⭐ v519 CHANGE 1 -- GUNNER-FIRST / PLANT-ON-THE-WAY.  The log call is
        # OUTSIDE the behaviour flag on purpose: the BEFORE tape (what the bank
        # and the prices look like on the ferry with the behaviour OFF) is what
        # sets FS_V519_GF_TI_FLOOR, and an instrument that only runs in the
        # treatment arm cannot measure a baseline.
        if LOKI_FS_V519 and FS_V519_GF_LOG:
            self._v519_gf_log(ct, E, p, rnd, lp)
        if LOKI_FS_V519 and FS_V519_GUNFIRST and self._v519_gunfirst(ct, E, p, rnd):
            # The action went to the shredder.  A builder that acts cannot move
            # (engine rule), so with no launcher beside us this costs the chain
            # exactly one hop; with a launcher beside us it costs nothing at all
            # -- the launcher is younger, acts later this round, and throws us
            # regardless.  Either way the round is spent and we return.
            return

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
            and LOKI_FS_CREW and fs_crew_on()
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
                # ⭐⭐ v526 CHANGE 2 (M3) -- THE RENDEZVOUS.  No ferry launcher
                # exists yet, so this is the MUSTER, and the parent's fall-
                # through walks body 2 AT THE ENEMY CORE while the lead stands
                # still waiting for it -- the drift the probe measured, which
                # puts body 2 outside the first link's envelope and (once
                # `FS_RELAY_PATIENCE` expires) buys a second, parallel chain.
                # HOLD STATION instead, and vacate the lead's forward build
                # tile if we are standing on it.  ⛔ NOT lead-follow: that was
                # tried, measured NEGATIVE (two-throw links 2 -> 0, n=6) and
                # reverted, because it occupied exactly that tile.
                if LOKI_FS_V526 and FS_V526_RDV \
                        and self.fs_ride_rnd is None:
                    self._v526_rendezvous(ct, p, T, E, rnd)
                    return
        if may_build and ct.get_action_cooldown() == 0 \
                and self._fs_build_ferry(ct, p, T, E):
            return
        # No launcher and none affordable: walk.  The ferry is a speed-up,
        # never a prerequisite.
        if ct.get_move_cooldown() == 0:
            self.tgt = T
            self._nav(ct, pave=False)

    # --- v519 change 1: GUNNER-FIRST / PLANT-ON-THE-WAY --------------------

    def _v519_gf_log(self, ct, E, p, rnd, lp):
        """GF519 -- the BEFORE tape.  One line per ferry round, stderr only.

        Carries the bank and the three prices the budget guard has to trade
        against (gunner vs launcher vs barrier) plus the band test, so the
        opening budget can be read off a tape taken with the BEHAVIOUR OFF.
        """
        if rnd > FS_V519_GF_MAX_RND:
            return
        try:
            d = dsq_core(p, E)
            band = 1 if (LOKI_BELTBREAK_DSQ_LO - 24 <= d
                         <= LOKI_BELTBREAK_DSQ_HI + 24) else 0
            print("GF519", rnd, "id", ct.get_id(),
                  "d", d, "band", band,
                  "ti", ct.get_global_resources(),
                  "ammo", ct.get_global_ammo(),
                  "gun", ct.get_gunner_cost(),
                  "lau", ct.get_launcher_cost(),
                  "bar", ct.get_barrier_cost(),
                  "cd", ct.get_action_cooldown(),
                  "lp", 1 if lp is not None else 0,
                  "plants", getattr(self, "v519_gf_plants", 0),
                  file=sys.stderr)
        except Exception:
            return

    def _v519_gunfirst(self, ct, E, p, rnd):
        """Spend ONE ferry action on the beltbreak shredder.  True if planted.

        TWO CALL SITES, one function: the FERRY turn (plant-on-the-way, while
        the chain crosses the annulus) and the RING ladder, immediately above
        rung 1 (the barrier).  The second is the amendment to Magnus's priority
        ruling 1 that the build report flags; both are bounded by the same
        three guards below and by the same one-plant-per-body counter.

        ⛔ WHAT THIS FUNCTION DOES NOT DO: it does not site, score, aim, price
        or target anything.  `_try_beltbreak_gunner` (raid.py) does all of that
        and is called UNMODIFIED -- the annulus test on the build tile, the
        r>=LOKI_BELTBREAK_RND gate, the harvester minimum, the live census cap,
        the live-target `can_fire_from` gate, the friendly-ray walk and the
        harvester-over-belt ladder are the parent's code reached from a second
        call site.  This function is the WHEN and the WHO, and nothing else.

        The four guards it adds, in the order they are cheapest to fail:
          * the action is available at all;
          * the clause is bounded to the crossing (`FS_V519_GF_MAX_RND`) -- past
            it, a ferry plant would BE the r36-75 lateness this change replaces;
          * one plant per body (`FS_V519_GF_MAX_PLANTS`), so a body cannot spend
            hop after hop replanting and never arrive;
          * ⭐ THE BUDGET GUARD.  The collar's opening bank pays for the ferry
            launchers and the first barriers; a gunner bought out of it that
            leaves less than `FS_V519_GF_TI_FLOOR` behind is a shredder that
            bought itself with the seal.  The floor is measured, not chosen --
            see doctrine §1 and `GFBUDGET.txt`.
        """
        if not (LOKI_FS_V519 and FS_V519_GUNFIRST):
            return False        # the helper's own early return: this function
                                # is called from TWO sites and neither may be
                                # the only place the flag is read.
        if ct.get_action_cooldown() != 0:
            return False
        if rnd < FS_V519_GF_MIN_RND or rnd > FS_V519_GF_MAX_RND:
            return False
        if getattr(self, "v519_gf_plants", 0) >= FS_V519_GF_MAX_PLANTS:
            return False
        try:
            if ct.get_global_resources() < ct.get_gunner_cost() + FS_V519_GF_TI_FLOOR:
                return False
        except Exception:
            return False
        # ⭐⭐ v520 CHANGE 3 -- THE LOWERED ANNULUS FLOOR, GUNFIRST ONLY.
        # `FS_V520_GF_RING_ONLY` decides whether the ferry call site also gets
        # it; shipped False (both sites), because the ferry site costs nothing
        # extra to leave open and the arm is measured either way.  The RING
        # site is `siege.py`'s rung 1'' and is where the probe's plants came
        # from (a body at d^2 = 4-13).
        _lo = None
        if LOKI_FS_V520 and FS_V520_GUNNEAR:
            at_ring = dsq_core(p, E) <= FS_RING_HOLD_DSQ
            if at_ring or not FS_V520_GF_RING_ONLY:
                _lo = FS_V520_GF_DSQ_LO
        try:
            planted = self._try_beltbreak_gunner(
                ct, E, rnd_floor=FS_V519_GF_MIN_RND, dsq_lo=_lo)
        except Exception:
            return False
        if not planted:
            return False
        if _lo is not None:
            self.v520_gf_near = getattr(self, "v520_gf_near", 0) + 1
        self.v519_gf_plants = getattr(self, "v519_gf_plants", 0) + 1
        self.v519_gf_rnd = rnd
        if FS_V519_GF_LOG:
            try:
                print("GF519 PLANT", rnd, "id", ct.get_id(),
                      "d", dsq_core(p, E),
                      "ti", ct.get_global_resources(), file=sys.stderr)
            except Exception:
                pass
        return True

    def _fs_relay_mustered(self, ct, p, rnd):
        """May the LEAD buy its first link yet?  (v514 change D.)

        True once body 2 is within FS_MUSTER_DSQ, or after FS_MUSTER_WAIT
        rounds -- the patience clause is what stops a body 2 that was never
        appointed, or died in the opening, from stalling the siege outright.
        """
        if not (LOKI_FS_V514 and FS_V514_RELAY and FS_RELAY_ON
                and LOKI_FS_CREW and fs_crew_on()):
            return True
        self.v526_must_why = 'waitexp'
        if rnd - self.fs_body_born >= fs_muster_wait():
            return True
        _b, _ph, rid = self._fs_state_at(ct, FS_SUPP_SLOT)
        if not rid:
            self.v526_must_why = 'norid'
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
                _dd = ct.get_position(eid).distance_squared(p)
                self.v526_must_why = 'near%d' % _dd
                return _dd <= FS_MUSTER_DSQ
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

    # --- v526 change 2 (M3): THE RENDEZVOUS ------------------------------

    def _v526_lead_pos(self, ct, p):
        """Position of the LEAD (body 1) if it is in vision, else None.

        The lead publishes into `SLOT_FS` and the rid field is `id + 1` (0 is
        "never reported"), which is the same channel `_fs_relay_mustered` reads
        in the other direction -- one writer per slot, the r197 discipline.
        """
        try:
            _b, _ph, rid = self._fs_state_at(ct, SLOT_FS)
        except Exception:
            return None
        if not rid:
            return None
        want = rid - 1
        try:
            for eid in ct.get_nearby_units():
                if eid != want:
                    continue
                if ct.get_team(eid) != self.team:
                    continue
                return ct.get_position(eid)
        except Exception:
            return None
        return None

    def _v526_veto_tiles(self, lp, T):
        """The tiles the LEAD may build its next link on.

        ⛔ NOT a guess about the lead's siting: this is `_fs_build_ferry`'s own
        candidate filter -- the lead's cardinal neighbours, minus any that is
        not strictly nearer the ferry target (`if d > here: continue`) -- so the
        veto set is a superset of whatever tile the lead actually picks, in
        bounds, with the same `here` computed from the lead's position.
        """
        out = set()
        here = lp.distance_squared(T)
        for dx, dy in CARD_DELTAS:
            bx, by = lp.x + dx, lp.y + dy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            if Position(bx, by).distance_squared(T) > here:
                continue
            out.add((bx, by))
        return out

    def _v526_rendezvous(self, ct, p, T, E, rnd):
        """Body 2's muster turn: HOLD STATION, and vacate the lead's tile.

        Three states, and the ordering is the whole plank:
          * the lead is not visible -> HOLD.  Never drift: the parent's drift
            is what this change exists to remove, and a blind body walking at
            the enemy core is the drift.
          * we are not on a veto tile -> HOLD.  The lead builds beside us and
            throws us next round.
          * we ARE on a veto tile -> step off, to the legal neighbour that is
            NOT itself a veto tile and is closest to a veto tile (i.e. closest
            to the future launcher's d^2 <= 2 pickup envelope).  This is the
            half lead-follow got wrong: it walked ONTO the tile.
        """
        if ct.get_move_cooldown() != 0:
            return
        lp = self._v526_lead_pos(ct, p)
        if lp is None:
            self._v526_log("RDV", rnd, "id", ct.get_id(), "state", "nolead")
            return
        # ⛔⛔ THE HOLD IS BOUNDED BY THE LEAD STILL BEING A FERRY BUILDER, and
        # this clause is MEASURED, not defensive: without it the first
        # mechanism battery read fjordgate `b2chain` 12/12 games -- a 10x10
        # board where the lead is at the enemy ring by r1 (arr1 median 1) and
        # therefore never buys a link, so body 2 held station for the whole
        # `FS_RELAY_PATIENCE` and then bought a SECOND CHAIN, which is the exact
        # duplication M3 exists to remove.  A lead already at the ring has no
        # relay to catch: fall through to the parent's walk.
        try:
            if dsq_core(lp, E) <= FS_RING_DSQ:
                self._v526_log("RDV", rnd, "id", ct.get_id(),
                               "state", "leadatring")
                if ct.get_move_cooldown() == 0:
                    self.tgt = T
                    self._nav(ct, pave=False)
                return
        except Exception:
            pass
        veto = (self._v526_veto_tiles(lp, T)
                if (LOKI_FS_V526 and FS_V526_VETO) else set())
        if (p.x, p.y) not in veto:
            self._v526_log("RDV", rnd, "id", ct.get_id(), "state", "hold",
                           "dlead", p.distance_squared(lp))
            return
        best, best_k = None, None
        for i in range(4):
            dx, dy = CARD_DELTAS[i]
            nx, ny = p.x + dx, p.y + dy
            if not (0 <= nx < self.mw and 0 <= ny < self.mh):
                continue
            if (nx, ny) in veto:
                continue
            try:
                if not ct.can_move(CARDINALS[i]):
                    continue
            except Exception:
                continue
            n = Position(nx, ny)
            d = min(n.distance_squared(Position(vx, vy)) for vx, vy in veto)
            k = (0 if d <= FS_V526_RDV_PICKUP_DSQ else 1, d,
                 n.distance_squared(lp))
            if best_k is None or k < best_k:
                best, best_k = CARDINALS[i], k
        if best is None:
            self._v526_log("RDV", rnd, "id", ct.get_id(), "state", "boxed")
            return
        try:
            ct.move(best)
        except Exception:
            return
        self._v526_log("RDV", rnd, "id", ct.get_id(), "state", "vacate",
                       "to", best.name, "k", best_k)

    def _v526_log(self, *a):
        if not (LOKI_FS_V526 and FS_V526_LOG):
            return
        try:
            print("V526", *a, file=sys.stderr)
        except Exception:
            return

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

    def _fs_build_ferry(self, ct, p, T, E=None):
        """Build the next hop's launcher on our own forward tile.

        ⭐⭐ v520 CHANGE 1 (Magnus's mid-build refinement) -- THE TERMINAL
        LAUNCHER'S TILE IS A CHOSEN SITE, NOT WHEREVER THE LATTICE LANDS.  Once
        the body is inside FS_V520_TERM_DSQ of their core the <=4 legal
        candidates are scored on (a) how many split arcs sit inside their
        d^2<=26 throw envelope, then (b) how many heal seats sit inside their
        d^2<=2 PICKUP envelope, then (c) the parent's distance key.  Every
        earlier link keeps the parent's siting exactly: scoring the whole chain
        for seat coverage would site six launchers for a job only the last one
        can do.
        """
        try:
            cost = ct.get_launcher_cost()
            if ct.get_global_resources() < cost + FS_LAUNCHER_TI_FLOOR:
                return False
        except Exception:
            return False
        ban = self._home_seat_keys_set()     # never seat one on OUR heal seats
        here = p.distance_squared(T)
        terminal = (self._v520_on() and FS_V520_TERMSITE and E is not None
                    and dsq_core(p, E) <= FS_V520_TERM_DSQ)
        legal = []
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
            if not terminal and best_d is not None and d >= best_d:
                continue
            try:
                if not ct.can_build_launcher(bp):
                    continue
            except Exception:
                continue
            if terminal:
                legal.append(bp)
            if best_d is None or d < best_d:
                best, best_d = bp, d
        if terminal and legal:
            scored = [(self._v520_term_score(ct, E, bp, T), bp) for bp in legal]
            scored.sort(key=lambda s: (s[0], s[1].y, s[1].x))
            pick = scored[0][1]
            # ⛔ THE CONFLICT IS COUNTED, NOT ASSUMED AWAY.  (a) wins by the
            # sort order; this records the rate at which the tile (b) would
            # have chosen is a DIFFERENT tile, per Magnus's request.
            cov_best = max(legal, key=lambda bp: (self._v520_covers(E, bp),
                                                  -bp.distance_squared(T)))
            if (cov_best.x, cov_best.y) != (pick.x, pick.y) \
                    and self._v520_covers(E, cov_best) \
                    > self._v520_covers(E, pick):
                self.v520_term_conflict += 1
            if FS_V520_TERM_LOG:
                try:
                    print("TERM520", ct.get_current_round(),
                          "id", ct.get_id(), "at", (p.x, p.y),
                          "n", len(legal), "pick", (pick.x, pick.y),
                          "arcs", self._v520_arcs_reachable(ct, E, pick),
                          "cov", self._v520_covers(E, pick),
                          "covbest", self._v520_covers(E, cov_best),
                          "conflict", self.v520_term_conflict,
                          "dsq", dsq_core(pick, E), file=sys.stderr)
                except Exception:
                    pass
            best = pick
        if best is None:
            return False
        try:
            _lid = ct.build_launcher(best)
        except Exception:
            return False
        self._fs_draw_dot(ct, best, 0, 200, 255)
        if V526RC:
            try:
                print('RC HOP', ct.get_current_round(),
                      'lid', _lid,
                      'body', getattr(self, 'fs_body', 1),
                      'at', '%d,%d' % (best.x, best.y),
                      'dsq', dsq_core(best, E) if E is not None else -1,
                      file=sys.stderr)
            except Exception:
                pass
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

    # ======================================================================
    # v520 CHANGE 1 -- THE PINCER.  Arcs, the terminal launcher, the split.
    # ======================================================================

    def _v520_on(self):
        """The master read, at RUN time.  One expression, one place."""
        return LOKI_FS_V520 and FS_V520_PINCER

    # ==================================================================
    # v521 -- SEAL-SHOT SYNCHRONIZATION
    # ==================================================================

    def _v521_on(self):
        """The master read, at RUN time.  One expression, one place."""
        return LOKI_FS_V521 and FS_V521_SYNC

    def _v521_core_resolve(self, ct):
        """v521 change 0, site 2: make `self.core` available where the ROSTER
        seat is issued, so the map gate is computable there.

        ⛔ THE SAME SCAN `_builder` DOES TWENTY LINES LOWER, moved rather than
        duplicated in effect: it assigns the same attribute, it is idempotent
        (a no-op once `self.core` is set), and it never RETURNS on failure --
        the parent's `if self.core is None: return` guard keeps its position, so
        a body that cannot see its Core behaves exactly as it did before.
        """
        if self.core is not None:
            return
        try:
            for eid in ct.get_nearby_buildings():
                try:
                    if ct.get_entity_type(eid) == EntityType.CORE \
                            and ct.get_team(eid) == self.team:
                        self.core = ct.get_position(eid)
                        return
                except Exception:
                    continue
        except Exception:
            return

    def _v521_fwd_sentinels(self, ct, E):
        """Forward turrets of ours that are ALIVE, from this body's own eyes.

        ⛔ NOT a replacement for the beat -- a DISJUNCT with it, the same shape
        `_fs_live_sentinels` already uses.  The beat answers ">= 1 alive"
        team-globally with nobody's vision involved, which is what makes the
        raider's own death stop mattering; the vision census is the fallback on
        a tree where GLOBALSENT is flagged off.
        """
        if LOKI_FS_V516 and FS_V516_GLOBALSENT and self._fs_sent_beat_live(ct):
            return True
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.SENTINEL:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                if dsq_core(ct.get_position(bid), E) <= FS_V521_FWD_DSQ:
                    return True
        except Exception:
            return False
        return False

    #: the three SYNC states.  0 = nothing joined, 1 = NEAR (close the last
    #: seats), 2 = HOLD (keep it closed), 3 = BUYIN (no turret, closure live).
    V521_SYNC_NONE = 0
    V521_SYNC_NEAR = 1
    V521_SYNC_HOLD = 2
    V521_SYNC_BUYIN = 3

    def _v521_sync_state(self, ct, E, orth_open):
        """⭐⭐ THE JOIN.  Closure state x turret liveness x funding, in one read.

        This is the whole mechanism of v521 and everything else in the build is
        a consequence of it.  Both inputs already existed on this tree and
        NEITHER SIDE EVER LOOKED AT THE OTHER: the collar published closure and
        the turret published liveness, and the reel measured a real 43-round
        closure sitting DISJOINT from its own turret's life.

        Returns (state, live, ammo) -- the two raw inputs come back with the
        verdict so the instrument prints what the decision was made on rather
        than a re-read that could differ.
        """
        if orth_open is None or not self._v521_on():
            return self.V521_SYNC_NONE, False, 0
        try:
            ammo = ct.get_global_ammo()
        except Exception:
            ammo = 0
        live = self._v521_fwd_sentinels(ct, E)
        funded = ammo >= FS_V521_FUND_AMMO
        if live:
            if orth_open == 0:
                if FS_V521_HOLD and (funded or not FS_V521_HOLD_FUNDED):
                    return self.V521_SYNC_HOLD, live, ammo
                return self.V521_SYNC_NONE, live, ammo
            if FS_V521_NEAR_CLOSE and funded \
                    and orth_open <= FS_V521_SYNC_NEAR:
                return self.V521_SYNC_NEAR, live, ammo
            return self.V521_SYNC_NONE, live, ammo
        # No forward turret exists.  A closure with nothing to shoot through it
        # is the `glacierkeep_s37_A` state and it is worth exactly nothing.
        if FS_V521_BUYIN and orth_open <= FS_V521_SYNC_NEAR:
            try:
                if ct.get_current_round() <= FS_V521_BUYIN_MAX_RND:
                    return self.V521_SYNC_BUYIN, live, ammo
            except Exception:
                return self.V521_SYNC_NONE, live, ammo
        return self.V521_SYNC_NONE, live, ammo

    def _v521_log(self, ct, rnd, state, orth_open, live, ammo, rung):
        if not FS_V521_SYNC_LOG:
            return
        try:
            print("SYNC521", rnd, "st", state, "orth", orth_open,
                  "live", 1 if live else 0, "ammo", ammo,
                  "body", getattr(self, "fs_body", 1), "rung", rung,
                  file=sys.stderr)
        except Exception:
            pass

    def _v521_why(self, ct, E, p, rnd, state, needed, ti, orth_open):
        """⛔⛔ THE DIAGNOSTIC THAT DECIDED THIS BUILD, and it is here because
        the FIRST TWO designs of clause 1a were both inert and neither the win
        column nor the rung tape could say why.

        The deterministic dose test (same seeds, randomness off, replay bytes
        diffed) read 0 of 18 changed games on the three maps where SYNC fires.
        A reorder that never changes the chosen action is not a mechanism, and
        the only way to find out WHICH rung was supposed to fire is to ask, in
        the round it did not, what stopped it.  Per NEAR/HOLD round this emits
        the four candidate blockers, each read off the same predicate the rung
        itself uses:
          nneed  seats the census still wants
          adj    needed seats orthogonally ADJACENT to this body (rung 1 can
                 only build on those -- a seat two tiles away is a WALK, not a
                 refusal)
          blk    needed seats in `fs_blocked_now` (a body or building on them)
          clr    would rung 3 fire?  (`_fs_try_clear(probe=True)`, the parent's
                 own predicate, no side effect)
          afford ti vs the binary-seal price the WAIT is holding for
        """
        if not FS_V521_WHY_LOG:
            return
        try:
            n = len(needed) if needed else 0
            adj = sum(1 for t in (needed or [])
                      if abs(t.x - p.x) + abs(t.y - p.y) == 1)
            blk = sum(1 for t in (needed or [])
                      if (t.x, t.y) in self.fs_blocked_now)
            clr = 1 if self._fs_try_clear(ct, E, p, needed or [],
                                          probe=True) else 0
            price = n * ct.get_barrier_cost() + FS_SEAL_MARGIN
            print("WHY521", rnd, "st", state, "orth", orth_open,
                  "nneed", n, "adj", adj, "blk", blk, "clr", clr,
                  "ti", ti, "price", price,
                  "body", getattr(self, "fs_body", 1), file=sys.stderr)
        except Exception:
            pass

    def _v521_rung(self, ct, rnd, rung, state):
        """⛔ THE REORDER'S OWN INSTRUMENT, and it is separate from SYNC521 on
        purpose: the state line fires every at-ring round (so a zero is
        readable), this one fires only when a rung actually wins the round.
        A mechanism arm reads the two columns zero-vs-nonzero without turning
        on the whole siege trace.
        """
        if not FS_V521_RUNG_LOG:
            return
        try:
            print("RUNG521", rnd, "rung", rung, "st", state,
                  "body", getattr(self, "fs_body", 1), file=sys.stderr)
        except Exception:
            pass

    # ==================================================================
    # v522 -- THE MAGAZINE FLOOR STOPS STARVING THE SEAL
    # ==================================================================

    def _v522_on(self):
        """The master read, at RUN time.  One expression, one place."""
        return LOKI_FS_V522 and FS_V522_FLOOR

    def _v522_crew_near(self, ct, rnd):
        """⭐ CORRECTION (2), CORE SIDE: is ANY live crew body publishing NEAR?

        `_fs_state` reads SLOT_FS, which is body 1's word.  Body 2 publishes
        into FS_SUPP_SLOT (v514 change D, one writer per slot) and the Core has
        never read it -- measured at 60 of 69 nordkap publishes and 68 of 269
        glacierkeep publishes lost to that gap, before any headline game ran.

        ⛔ A DISJUNCT, AND WITH A GUARD THE SLOT_FS PATH DOES NOT HAVE.  It can
        only ADD a NEAR round.  Every slot's own BEAT must be fresh
        (FS_BEAT_STALE) before its phase is believed, so a body that died
        holding a NEAR word cannot pin the Core's floor for the rest of the
        match -- which is a hazard the SLOT_FS read is exposed to and the TTL
        (FS_V522_MAX_RNDS) is only the second line against.
        """
        if not (LOKI_FS_V522 and FS_V522_FLOOR and FS_V522_CREW_READ):
            return False
        try:
            slots = self._fs_crew_slots()
        except Exception:
            return False
        for s in slots:
            try:
                beat, ph, _r = self._fs_state_at(ct, s)
            except Exception:
                continue
            if ph != FS_PH_KILL_NEAR:
                continue
            if not beat or rnd - (beat - 1) > FS_BEAT_STALE:
                continue                 # a dead body's last word
            return True
        return False

    def _v522_near_publish(self, ct, rnd, orth_open):
        """⭐⭐ THE RAIDER HALF OF v522, AND IT IS ONE PUBLISHED BIT OF STATE.

        The Core owns `convert_ammo` and cannot see the enemy ring; the raider
        is standing on the collar and has just counted it.  Everything else the
        join needs -- turret liveness (the caller has already established it),
        team ammunition, the barrier price -- the Core can read for itself, so
        the ONLY thing that has to cross is "closure is NEAR and the seal costs
        more than the repair allowance".

        ⛔ NO NEW SLOT, NO NEW WRITER.  It rides the phase field that
        `_fs_publish` already stamps into this body's own word, using
        FS_PH_KILL_NEAR = 6, the last free code in a 3-bit field.  The
        one-writer rule (the r197 defect) is untouched.

        ⛔ AND IT IS A REFINEMENT, NEVER A NEW STATE.  Returns True only in
        rounds the caller has already resolved to KILL or KILL_OPEN, so every
        round that publishes 6 would have published 4 or 5 under the parent.
        With `orth_open >= 1` required, a SEALED collar can never reach it.
        """
        # ⭐ THE LOG IS GATED ON ITSELF, NOT ON THE MASTER (v521 surprise 7).
        # With LOKI_FS_V522 = False the tape still emits a PH522 line per
        # eligible round with `on 0 pub 0`, so a mechanism arm's ZERO has a
        # visible denominator instead of being void by construction.  The ship
        # pays nothing: FS_V522_PH_LOG is False and this returns on the first
        # test.
        _on = self._v522_on()
        if not (_on or FS_V522_PH_LOG):
            return False
        if orth_open is None or orth_open < 1 or orth_open > FS_V522_NEAR:
            return False
        try:
            bar = ct.get_barrier_cost()
        except Exception:
            return False
        price = orth_open * bar + FS_SEAL_MARGIN
        allow = FS_MAG_REPAIR_BARRIERS * bar
        ok = _on
        if FS_V522_BIND_IF and price <= allow:
            # The bank the Core already holds covers this seal.  Nothing to
            # fix, so nothing is published and the channel does not move.
            ok = False
        if ok:
            try:
                if ct.get_global_ammo() < FS_V522_FUND_AMMO:
                    # A turret with no shot in the magazine is a decoration,
                    # and holding titanium back from a magazine that is ALREADY
                    # empty is v521's failure mode in miniature.  The Core
                    # re-checks this against ITS OWN round (the store is
                    # buffered by one), and that re-check is the binding one.
                    ok = False
            except Exception:
                ok = False
        if FS_V522_PH_LOG:
            try:
                print("PH522", rnd, "orth", orth_open, "bar", bar,
                      "price", price, "allow", allow,
                      "on", 1 if _on else 0,
                      "pub", 1 if ok else 0,
                      "body", getattr(self, "fs_body", 1), file=sys.stderr)
            except Exception:
                pass
        if FS_V522_PROBE_NOPUB:
            return False        # every read performed, nothing published
        return ok

    def _v520_appt_lost(self, ct, rnd):
        """Did this body LOSE the support-seat race?  (Readback arm.)

        Checked once, on the first turn AFTER the claim -- store writes are
        buffered one round, so a same-round readback would read the word from
        before either claim and could only ever say "free".
        """
        if not (self._v520_on() and FS_V520_APPT_GUARD):
            return False
        if getattr(self, "v520_appt_rnd", -1) < 0:
            return False
        if rnd <= self.v520_appt_rnd:
            return False
        self.v520_appt_rnd = -1              # one-shot: verified, either way
        try:
            _b, _p, _r = self._fs_state_at(ct, FS_SUPP_SLOT)
            if _r and (_r - 1) != ct.get_id():
                self.v520_appt_yield += 1
                if FS_V520_APPT_LOG:
                    print("APPT520 YIELD", rnd, "id", ct.get_id(),
                          "won", _r - 1, "n", self.v520_appt_yield,
                          file=sys.stderr)
                return True
        except Exception:
            return False
        return False

    def _v520_arc_of(self, t, E):
        """FRONT (facing our core) or BACK (beyond theirs) for a ring tile.

        ⭐ THE AXIS IS THE CORE-TO-CORE LINE, not a compass direction, so the
        split means the same thing on every map and on both seats.  Integer
        arithmetic throughout: the 2x2 footprint's centre is a half-tile, so
        every coordinate is doubled and the -1 is the two halves.

        A tile exactly on the perpendicular is split by the PERPENDICULAR
        component's sign, which is deterministic and hands the two straddling
        seats one to each arc rather than both to the same one.
        """
        C = self.core
        if C is None:
            return FS_V520_ARC_FRONT
        ux, uy = C.x - E.x, C.y - E.y
        vx, vy = 2 * t.x - 2 * E.x - 1, 2 * t.y - 2 * E.y - 1
        dot = vx * ux + vy * uy
        if dot > 0:
            return FS_V520_ARC_FRONT
        if dot < 0:
            return FS_V520_ARC_BACK
        perp = vx * uy - vy * ux
        return FS_V520_ARC_FRONT if perp > 0 else FS_V520_ARC_BACK

    def _v520_arc_anchor(self, ct, E, arc):
        """A representative SEAT of `arc`: the one nearest the core centre on
        that side, used as the throw destination the split aims at."""
        try:
            seats = [s for s in heal_seats(E, self.mw, self.mh)
                     if not self._fs_wall(s)]
        except Exception:
            return None
        best, best_k = None, None
        for s in seats:
            if self._v520_arc_of(s, E) != arc:
                continue
            k = (dsq_core(s, E), s.y, s.x)
            if best_k is None or k < best_k:
                best, best_k = s, k
        return best

    def _v520_covers(self, E, lp):
        """How many enemy HEAL SEATS sit inside `lp`'s d^2<=2 pickup envelope.

        The eviction/closure autopsy's own metric: accidental ferry termini
        measured 0 of 8 in 12 of 12 cases (they land on the outer diagonal),
        while the best legal tile reaches 4 of 8 on every grid map and covered
        279 of 280 body-on-seat rounds in the midgard counterfactual.
        """
        try:
            seats = heal_seats(E, self.mw, self.mh)
        except Exception:
            return 0
        n = 0
        for s in seats:
            if (lp.x - s.x) ** 2 + (lp.y - s.y) ** 2 <= 2:
                n += 1
        return n

    def _v520_arcs_reachable(self, ct, E, lp):
        """How many of {FRONT, BACK} have a LEGAL landing tile inside `lp`'s
        d^2<=26 throw envelope.  This is objective (a) of Magnus's terminal
        siting rule and it wins every conflict with objective (b)."""
        n = 0
        for arc in (FS_V520_ARC_FRONT, FS_V520_ARC_BACK):
            if self._v520_arc_site(ct, E, lp, arc, probe=True) is not None:
                n += 1
        return n

    def _v520_arc_site(self, ct, E, lp, arc, probe=False):
        """The landing tile for a rider assigned to `arc`, thrown from `lp`.

        Prefers a tile ON the arc and INSIDE the ring; falls back (under
        FS_V520_SPLIT_WALK) to the legal site closest to the arc's anchor, so a
        far arc outside the 5.1-tile envelope is approached rather than
        abandoned -- and the remaining WALK is what the report measures.
        `probe=True` skips the passability read, which is what makes this
        usable as a SITING predicate before the launcher exists.
        """
        anchor = self._v520_arc_anchor(ct, E, arc)
        if anchor is None:
            return None
        best, best_k = None, None
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                if dx * dx + dy * dy > FS_HOP_DSQ:
                    continue
                tx, ty = lp.x + dx, lp.y + dy
                if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                    continue
                t = Position(tx, ty)
                if self._fs_wall(t):
                    continue
                if not probe:
                    try:
                        if not ct.is_tile_passable(t):
                            continue
                    except Exception:
                        continue
                dc = dsq_core(t, E)
                on_arc = 0 if self._v520_arc_of(t, E) == arc else 1
                in_ring = 0 if dc <= FS_RING_DSQ else 1
                k = (on_arc, in_ring, t.distance_squared(anchor), dc)
                if best_k is None or k < best_k:
                    best, best_k = t, k
        if best is None:
            return None
        if best_k[0] and not FS_V520_SPLIT_WALK:
            return None                      # off-arc landings are the WALK
        return best

    def _v520_term_score(self, ct, E, bp, T):
        """(-arcs_reachable, -seat_cover, d_to_T) for a candidate launcher tile.

        Magnus's priority order, verbatim: (a) both split arcs inside the
        d^2<=26 envelope, (b) the d^2<=2 pickup envelope covering the most heal
        seats, (c) the parent's own key.  (a) BEATS (b) -- delivery before
        eviction -- and the report carries the per-map rate at which they
        disagree.
        """
        return (-self._v520_arcs_reachable(ct, E, bp),
                -self._v520_covers(E, bp),
                bp.distance_squared(T))

    def _v520_claim_arc(self, ct, E, p, rnd):
        """Derive MY arc from where I stand, deconflict, publish.  Returns it.

        ⛔ DERIVED FROM THE ENGINE, NOT FROM A MESSAGE.  A body knows which
        side of their core it landed on by looking at its own position; the
        store is only used to DECONFLICT, which is the one thing position
        cannot do.  On a collision the higher `fs_body` yields -- deterministic,
        so the two bodies cannot both yield or both hold -- and the event is
        COUNTED (`v520_arc_collide`), because "two bodies claiming one arc" is
        the alarm this change has to be able to fail.
        """
        if not (self._v520_on() and FS_V520_ARC_PUBLISH):
            return FS_V520_ARC_NONE
        me_body = getattr(self, "fs_body", 1)
        peer_slot = SLOT_FS if me_body == 2 else FS_SUPP_SLOT
        peer = self._v520_arc_at(ct, peer_slot)
        peer_beat = self._fs_state_at(ct, peer_slot)[0]
        peer_live = bool(peer_beat) and (rnd - (peer_beat - 1)) <= FS_CREW_STALE
        if self.v520_arc != FS_V520_ARC_NONE:
            # ⛔⛔ THE CLAIM IS STICKY, AND THE FIRST BUILD OF THIS FUNCTION WAS
            # NOT -- IT RE-DERIVED THE ARC FROM `p` EVERY ROUND AND THRASHED.
            # Measured on the first nordkap smoke: 11 "collisions" in one game,
            # both bodies flipping arc as they walked round the collar, i.e.
            # the two halves swapping owners mid-seal.  An assignment that
            # changes when you step is not an assignment.  It is claimed ONCE,
            # on arrival, and held for the body's life.
            # ⭐ THE RESIDUAL ALARM LIVES HERE INSTEAD, and it is an OBSERVATION
            # rather than a self-report: if a live peer is publishing MY arc
            # after both claims have settled, the split has failed and the two
            # bodies are working the same half.  It must be 0.
            if peer_live and peer == self.v520_arc:
                self.v520_arc_dup += 1
                if FS_V520_ARC_LOG:
                    try:
                        print("ARC520 DUP", rnd, "id", ct.get_id(),
                              "body", me_body, "arc", self.v520_arc,
                              "n", self.v520_arc_dup, file=sys.stderr)
                    except Exception:
                        pass
            return self.v520_arc
        mine = self._v520_arc_of(p, E)
        if peer_live and peer == mine and peer != FS_V520_ARC_NONE \
                and not FS_V520_PROBE_NO_DECONFLICT:
            # The peer got here first and is on the arc I landed on.  Take the
            # other one -- COUNTED, because a claim-time conflict is the thing
            # this deconfliction exists to resolve and a silent resolution is
            # indistinguishable from no conflict.
            self.v520_arc_collide += 1
            mine = (FS_V520_ARC_BACK if mine == FS_V520_ARC_FRONT
                    else FS_V520_ARC_FRONT)
            if FS_V520_ARC_LOG:
                try:
                    print("ARC520 COLLIDE", rnd, "id", ct.get_id(),
                          "body", me_body, "peer", peer, "took", mine,
                          "n", self.v520_arc_collide, file=sys.stderr)
                except Exception:
                    pass
        self.v520_arc = mine
        self.v520_arc_rnd = rnd
        if FS_V520_ARC_LOG:
            try:
                print("ARC520 CLAIM", rnd, "id", ct.get_id(),
                      "body", me_body, "arc", mine,
                      "at", (p.x, p.y), file=sys.stderr)
            except Exception:
                pass
        return mine

    # --- v520 CHANGE 2 -- PRESENCE.  The Core side. -------------------------

    def _v520_presence_reserve(self, ct, rnd):
        """⭐⭐ v520 CHANGE 2 -- CORE SIDE.  The titanium floor a REPLACEMENT
        BODY needs while a ring seat reads dead, or 0.

        ⛔ MUTATES `v520_pres_until` AND IS CALLED FROM THE CORE'S TURN ONLY,
        once per round -- the same contract `_v518_twin_reserve` documents.

        THE ARGUMENT, and it is v513's own: replacement latency is a median of
        90 rounds with 0 of 14 inside Magnus's ~15-round cap, and that report
        names the binding constraint as FUNDING the body (60-100 Ti at live
        scale plus the spawn reserve), not NOTICING the death -- the dedicated
        crew bits already notice it in <= FS_CREW_STALE = 6.  v518's twin
        reserve is the mechanism that answers exactly that shape of problem and
        it is live and measured: raise the CORE's `convert_ammo` floor by the
        purchase's OWN bar while the purchase is pending, bounded by a TTL,
        entering through `max()` so no other floor is lowered.

        THE THREE DEFECTS IT IS BUILT NOT TO REPEAT:
          * PRICED BELOW THE BAR (v517): the bank equilibrates to exactly
            `ti_floor` because `convert_ammo` is the marginal consumer, so a
            reserve under the purchase bar parks the bank permanently short.
            This prices the SAME quantity the spawn site tests -- builder cost
            plus one ferry launcher -- plus a margin.
          * A MONOTONE COUNTER READ FOR LIVENESS (v517): the vacancy here is
            read off the dedicated crew beats, which are absolute round
            numbers and fall stale on death.
          * NO CEILING (autopsy #4, the magazine lock, three times): capped at
            FS_V520_PRES_CAP.

        ⛔ AND THE OPENING IS EXEMPT BY CONSTRUCTION: a seat that has NEVER
        reported is not vacant, it is unborn.  Without that latch the reserve
        would hold titanium back from r0 on every map and starve the very
        opening the crew is spawned out of -- which is the -13.3pp shape this
        build is trying not to repeat.
        """
        if not (LOKI_FS_V520 and FS_V520_PRESENCE):
            return 0
        # ⛔⛔ TWO HARD STOPS, AND THE FIRST SMOKE RUN IS WHY THEY EXIST.
        # Without them the reserve read `vacant 456` on one nordkap game: the
        # support died at r36, no replacement ever arrived, the seat stayed
        # stale for the rest of the match and the Core held 160 Ti back from
        # `convert_ammo` for 456 CONSECUTIVE ROUNDS.  That is the magazine lock
        # (autopsy #4) wearing a new hat, and it is the exact failure this line
        # has now been taught three times.  A reserve for a purchase that can
        # no longer be made is not a reserve, it is a freeze.
        if self.fs_replaced >= FS_MAX_REPLACE:
            return 0                         # no replacement door left to fund
        if self.v520_pres_rounds >= FS_V520_PRES_MAX_RNDS:
            return 0                         # per-match budget spent
        seats = (0, 1) if fs_crew_on() else (0,)
        vacant = False
        for seat in seats:
            age = self._fs_crew_age(ct, seat, rnd)
            if age <= FS_CREW_STALE:
                self.v520_pres_seen[seat] = 1
            elif self.v520_pres_seen.get(seat):
                vacant = True
        if vacant:
            self.v520_pres_until = rnd + FS_V520_PRES_TTL
            self.v520_pres_vacant += 1
        if rnd >= self.v520_pres_until:
            return 0
        try:
            need = ct.get_builder_bot_cost() + ct.get_launcher_cost()
        except Exception:
            return 0
        need += FS_V520_PRES_MARGIN
        if need > FS_V520_PRES_CAP:
            need = FS_V520_PRES_CAP
        self.v520_pres_rounds += 1
        return need

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
        if LOKI_FS_CREW and fs_crew_on() and self.fs_role == "supp" \
                and not (self._v520_on() and FS_V520_ARC_SEAL):
            self._fs_supp_turn(ct, E, p, rnd, needed, orth_open)
            return
        # ⭐⭐ v520 CHANGE 1 -- BOTH BODIES SEAL, SPLIT BY ARC.  Magnus,
        # verbatim intent: two raiders, "one to the BACK one to the FRONT of the
        # enemy core, SO THEY CAN BARRIER FROM DIFFERENT SIDES".  The v513 verb
        # split (support = evictor + late sentinel, never a barrier) existed to
        # stop two bodies competing for the same round; the ARC assignment is
        # the replacement for it and it is the stronger anti-competition device,
        # because the two bodies are working opposite halves of a closed curve
        # rather than taking turns on the same half.  The closure autopsy prices
        # what this buys: 85.5% of open-seat rounds are paid to SERIAL sealing.
        # ⛔ The support keeps its own PUBLISH SLOT (`fs_body` is fixed at
        # appointment and never re-derived) -- only its VERB SET changes here.
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

    def _v518_early_sentinel(self, ct, E, p, rnd, needed, ti, orth_open):
        """⭐⭐ v518 CHANGE 2(a) -- THE FIRST FORWARD SENTINEL OUTRANKS THE
        COLLAR ONCE THE GATE IS OPEN.

        THE MEASUREMENT THAT ASKS FOR IT.  v517's phase budget:
        `arrive -> sent` is 81 rounds, IDENTICAL in all three of its arms, and
        45% of the whole r180 `KILL_TARGET` budget.  `PROGRAMME.md`'s phase
        budget wants the first funded turret at <= r75 against a measured
        median of r88.  The autopsy (#2) named the shape: the raider seals
        first and the turret is rung 4, so it is bought on rounds the collar
        has nothing left to do.

        ⛔ THE DISPLACEMENT IS BOUNDED BY CONSTRUCTION, AND THAT IS WHY THIS IS
        NOT A RETURN TO v510.  The clause is gated on
        `live <= FS_V518_EARLY_MAX_LIVE` (= 0), so it can fire only on a round
        where the purchase SUCCEEDS -- the very next round a sentinel is alive
        and the clause is shut until that sentinel dies.  Its total cost to the
        collar is ONE BARRIER-ROUND per period with no forward sentinel alive
        (⛔ not "once per game": measured 17 firings over 15 of 30 games in the
        `mF` arm), against the ~81 rounds it is trying to buy back.  v510's
        failure was five verbs competing every round for ever; this is one
        verb, once per sentinel.

        ⛔ AND IT CANNOT STRAND THE COLLAR.  `_fs_sentinel_ok` reserves
        `len(needed) * barrier_cost + sentinel_cost` before it returns True, so
        every purchase this clause takes is one the whole remaining collar was
        already paid for.  What is skipped is the WAIT (`_fs_seal_pending`, the
        rung-1-actionable-but-unfunded hold), not the funding.

        ⚠⚠ DOCTRINE COLLISION, FLAGGED FOR THE LANE AND NOT RESOLVED HERE.
        Magnus's priority ruling 1 ordered the collar sequence barriers ->
        launchers -> sentinels, and the ladder's own docstring says rung 4 is
        "bottom of the ladder BY DESIGN".  Magnus's `KILL_TARGET` ruling
        post-dates it and wants a funded turret by r75.  On the round the gate
        opens those two point in opposite directions.  This build encodes the
        later ruling, measures what it costs the collar (the closure and
        barrier counters are in the mechanism table), and asks for the routing.
        """
        if not (LOKI_FS_V518 and FS_V518_EARLYSITE):
            return False
        try:
            if self._fs_live_sentinels(ct, E) > FS_V518_EARLY_MAX_LIVE:
                return False
        except Exception:
            return False
        if not self._fs_sentinel_ok(ct, ti, needed, orth_open):
            return False
        if not self._fs_try_sentinel(ct, E, p):
            return False
        self.v518_early += 1
        if FS_V518_EARLY_LOG:
            try:
                print("EARLY518", rnd, "id", ct.get_id(),
                      "ti", ti, "need", len(needed), "orth", orth_open,
                      "rung1", 1 if self._fs_rung1_ready(ct, p, needed, ti)
                      else 0,
                      "pend", 1 if self._fs_seal_pending(ct, needed, ti) else 0,
                      "n", self.v518_early, file=sys.stderr)
            except Exception:
                pass
        return True

    def _v518_gap_mark(self, ct, rnd, code):
        """A ring round the purchase never got a chance at: the body spent the
        round surviving.  Same tape as `_v518_gap_log` so the decomposition
        covers EVERY ring round with no gaps."""
        if not (LOKI_FS_V518 and FS_V518_GAPLOG):
            return
        try:
            print("GAP518", rnd, "id", ct.get_id(), "code", code,
                  "live", -1, "salt", -1, "eco", -1, "ti", -1, "sen", -1,
                  "bar", -1, "need", -1, "orth", -1,
                  "floor", FS_SENT_RND_FLOOR, file=sys.stderr)
        except Exception:
            pass

    def _v518_gap_log(self, ct, E, p, rnd, needed, ti, orth_open):
        """⭐⭐ v518 -- THE DECOMPOSITION OF THE 81-ROUND `arrive -> sent` GAP.

        One line per ring round, carrying the FIRST reason no forward sentinel
        was bought this round.  The v517 phase budget measured the gap and could
        not say what it was made of; this says.

        The codes, in the order they are tested (first match wins):

          HAVE   a forward sentinel is already alive -- not part of the gap
          COOL   the body's action cooldown is not 0 (it moved last round)
          GATE   neither disjunct of the v515 sentinel gate is open
                 (salt-complete OR (conn2 AND rnd >= FS_SENT_RND_FLOOR))
          FUND   a disjunct IS open but `_fs_sentinel_ok` refuses on money --
                 the collar reserve, the per-purchase floor or the rebuy bar
          SITE   gate and funding both pass, and `_fs_try_sentinel` (probed,
                 one statement short of the build) finds NO legal aligned site
                 among the <= 4 tiles under this body's hand
          BUSY1  everything passes and rung 1 (barrier) is actionable this
                 round -- the ladder will spend the action on the collar
          BUSYW  everything passes, rung 1 is not actionable, but the ladder is
                 WAITING on `_fs_seal_pending` (an open seat it cannot yet pay
                 for), which blocks rungs 2-4
          BUSY23 everything passes and rung 2 (evictor) or 3 (clear) will take
                 the action
          OPEN   nothing blocks it: the purchase happens this round

        ⛔ IT IS AN INSTRUMENT AND NOTHING READS IT.  Gated on FS_V518_GAPLOG,
        which is False in every shipped configuration; it takes no decision and
        writes no state.  It DOES cost CPU (one probed purchase scan per ring
        round), which is why it is not on by default.
        """
        if not (LOKI_FS_V518 and FS_V518_GAPLOG):
            return
        code = "OPEN"
        gate = (-1, -1)
        live = -1
        try:
            live = self._fs_live_sentinels(ct, E)
            if live > 0:
                code = "HAVE"
            elif ct.get_action_cooldown() != 0:
                code = "COOL"
            else:
                ok = self._fs_sentinel_ok(ct, ti, needed, orth_open)
                g = getattr(self, "fs515_gate", None)
                if g:
                    gate = (g[1], g[2])
                if not ok and gate != (-1, -1) and not (gate[0] or gate[1]):
                    code = "GATE"
                elif not ok:
                    code = "FUND"
                elif not self._fs_try_sentinel(ct, E, p, probe=True):
                    code = "SITE"
                elif FS_SEAL_ON and self._fs_rung1_ready(ct, p, needed, ti):
                    code = "BUSY1"
                elif self._fs_seal_pending(ct, needed, ti):
                    code = "BUSYW"
                elif (FS_EVICT_ON and self._fs_try_evict_launcher(
                        ct, E, p, ti, needed=needed, probe=True)) \
                        or self._fs_try_clear(ct, E, p, needed, probe=True):
                    code = "BUSY23"
        except Exception:
            code = "ERR"
        try:
            print("GAP518", rnd, "id", ct.get_id(), "code", code,
                  "live", live, "salt", gate[0], "eco", gate[1],
                  "ti", ti, "sen", ct.get_sentinel_cost(),
                  "bar", ct.get_barrier_cost(), "need", len(needed),
                  "orth", orth_open, "floor", FS_SENT_RND_FLOOR,
                  file=sys.stderr)
        except Exception:
            pass

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
                self._v518_gap_mark(ct, rnd, "DODGE")
                return
        # ⭐ v513 change G: the HP floor.  Below it the body is one sentinel
        # shot from dead (18 damage against a 40 HP builder) and 20 of the 23
        # measured deaths sat at exactly 4 HP for two to four rounds first --
        # there was time to leave every single time.
        if self._fs_try_retreat(ct, E, p, rnd, hp):
            self._v518_gap_mark(ct, rnd, "RETREAT")
            return

        ti = ct.get_global_resources()
        self._v518_gap_log(ct, E, p, rnd, needed, ti, orth_open)
        # The eviction siting signal is REACTIVE (48.4% interception against
        # 29.0% for the best fixed tile), so it has to be collected every round
        # the raider is at the ring -- including the rounds rung 1 wins.
        if FS_EVICT_ON:
            self._fs_observe_healers(ct, E)
        # v514 change B: has a sentinel of ours been killed?  (Magnus ruling 2.)
        self._fs_sent_watch(ct, rnd)

        # ⭐⭐⭐ v521 -- THE SYNC READ.  Computed ONCE per round, before any rung,
        # because three different clauses below consult it and a state that
        # changed between them would not be a state.  It is a pure read: no
        # gate is relaxed by it and no purchase is authorised by it.
        _v521_st, _v521_live, _v521_ammo = self._v521_sync_state(ct, E,
                                                                orth_open)
        self._v521_log(ct, rnd, _v521_st, orth_open, _v521_live, _v521_ammo, -1)
        if _v521_st in (self.V521_SYNC_NEAR, self.V521_SYNC_HOLD):
            self._v521_why(ct, E, p, rnd, _v521_st, needed, ti, orth_open)
        _v521_near = (_v521_st == self.V521_SYNC_NEAR)
        _v521_hold = (_v521_st == self.V521_SYNC_HOLD)
        _v521_buyin = (_v521_st == self.V521_SYNC_BUYIN)

        if ct.get_action_cooldown() == 0:
            # ⭐⭐⭐ v521 RUNG 0' -- BUY INTO THE CLOSURE.  The collar is closed
            # (or two seats from it) and NOTHING IS SHOOTING THROUGH IT.  Rung 4
            # sits at the bottom of the ladder because "it fires on the rounds
            # the collar has nothing actionable left" -- and inside a closure
            # window that reasoning inverts: those are the rounds the turret is
            # worth the most, and `glacierkeep_s37_A` held a 43-round closure
            # and bought its sentinel five rounds AFTER the seal broke.
            # ⛔ EVERY GATE IS THE PARENT'S.  `_fs_sentinel_ok` still decides
            # (salt/eco disjunction, the collar reserve, the live count, the
            # purchase cap) and `_fs_try_sentinel` still decides the siting.
            # This clause moves the round, not the bar.
            if _v521_buyin \
                    and self._fs_sentinel_ok(ct, ti, needed, orth_open) \
                    and self._fs_try_sentinel(ct, E, p):
                self._fs_rung(ct, rnd, 4, E, p, needed, ti, orth_open)
                self._v521_rung(ct, rnd, 0, _v521_st)
                return
            # ⭐⭐ v521 1a -- UNDER *NEAR*, RUNGS 1' AND 1'' STAND DOWN.  A
            # forward turret is alive AND funded and the collar is one or two
            # seats from closing: every round spent on a second sentinel site or
            # a shredder plant is a round the OVERLAP window does not start.
            # The reel's arithmetic is the whole argument -- 0 of 119 enemy-core
            # heal rounds fell in a fully-sealed round, so closing those last
            # seats *while the turret is firing* is the only action on this
            # ladder whose damage is permanent.
            if not _v521_near:
                # ⭐⭐ v518 CHANGE 2(a) -- RUNG 1', THE FIRST FORWARD SENTINEL
                # JUMPS THE COLLAR.  See `_v518_early_sentinel` for the argument
                # and for the flagged collision with Magnus's priority ruling 1.
                if self._v518_early_sentinel(ct, E, p, rnd, needed, ti,
                                             orth_open):
                    return
            # ⭐⭐ v519 CHANGE 1 -- RUNG 1'', THE SHREDDER JUMPS THE COLLAR ONCE.
            # ⚠⚠ THIS IS A DELIBERATE, BOUNDED AMENDMENT TO MAGNUS'S PRIORITY
            # RULING 1 (2026-08-18 ~04:02Z: "1. build barriers, 2. build
            # launchers ..., 3. build sentinels") AND IT IS FLAGGED IN THE BUILD
            # REPORT RATHER THAN RESOLVED HERE.  The anchor for taking it at all
            # is Magnus's own later variant (~05:07Z): "maybe there's some
            # scenario where we can cripple them hard by an early gunner ...
            # while the offensive builders go and set up barriers around their
            # core AFTER the gunner is placed" -- barriers after the gunner is
            # the ordering, in his words.
            # THE COST IS BOUNDED THREE WAYS and none of them is a judgement
            # call: at most ONE plant per body (FS_V519_GF_MAX_PLANTS), only
            # before FS_V519_GF_MAX_RND, and only with the collar's own money
            # still on the table (FS_V519_GF_TI_FLOOR).  It is BELOW the
                # first-sentinel clause because the autopsy is explicit that the
                # sentinel is the kill and the shredder is its ENABLER, not its
                # rival.
                # (⛔ INERT IN THE v521 FIRED CONFIG: FS_V520_GUNNEAR ships
                # False, so `_v519_gunfirst` is back to v519's measured zero
                # dose -- 0 plants in 356 attempts.  The clause is here, and
                # under the NEAR skip, because the flag is a dose decision that
                # can be reversed without touching this file.)
                if self._v519_gunfirst(ct, E, p, rnd):
                    return
            # rung 1 -- BARRIER.
            if FS_SEAL_ON and self._fs_try_seal(ct, E, p, needed, ti):
                self._v521_rung(ct, rnd, 1, _v521_st)
                return
            # THE WAIT.  A seat is open and buildable but the collar is not yet
            # paid for: hold the bank.  Spending it one rung down is exactly how
            # a binary seal ends up at 10/12, which measured WORSE than no seal.
            #
            # ⭐⭐⭐ v521 1a, SECOND HALF -- UNDER *NEAR* THE WAIT IS BYPASSED FOR
            # THE TWO SEAT-CLEARING RUNGS AND RUNG 4 IS SUPPRESSED.
            #
            # ⛔⛔ THE FIRST BUILD OF THIS CLAUSE SUPPRESSED RUNGS 2-4 WHOLESALE
            # AND THE DETERMINISTIC DOSE TEST KILLED IT: 0 of 18 games changed a
            # single byte on the three maps where SYNC actually fires (atoll,
            # drakkarfjord, glacierkeep), because THE PARENT'S LADDER IS ALREADY
            # COLLAR-FIRST IN EXACTLY THE STATES NEAR SELECTS.  Suppressing
            # rungs that never win a round is not a mechanism.
            #
            # The tape said what the real blocker is: rung 1 did not fire, so
            # the last seats are not PLACEABLE this round -- and the two things
            # that make a seat unplaceable are an enemy BUILDING on it (rung 3's
            # job) and an enemy BODY on it (rung 2's job, and the closure
            # autopsy's own words: "the eviction launcher is the seal's
            # PRECONDITION, not its garnish").  The parent gates both behind
            # `_fs_seal_pending`, the WAIT that holds the bank for a barrier --
            # a barrier that CANNOT BE PLACED on that tile at any price.
            #
            # ⇒ UNDER NEAR THE WAIT IS THE DEFECT, NOT THE DISCIPLINE.  A live
            # FUNDED turret is firing and the collar is one or two seats from
            # making its damage permanent; holding titanium for a build that is
            # arithmetically impossible while the only two verbs that could
            # unblock the tile stand down is the disjointness this build exists
            # to cure, one level down.
            #
            # ⛔ AND RUNG 4 GOES THE OTHER WAY -- suppressed under NEAR.  A
            # SECOND sentinel is off-collar spend in the two rounds the first
            # one's window is being closed; it keeps its place under HOLD, where
            # the window is already open and more damage per round is the
            # quantity.  The two clauses are deliberately asymmetric and the
            # RUNG521 tape reports each separately.
            if _v521_near or not self._fs_seal_pending(ct, needed, ti):
                # rung 2 -- ONE EVICTION LAUNCHER, sited by cov over observed
                # healer tiles, Ti-gated above every barrier still owed.
                # ⭐ v521 1b -- SUPPRESSED UNDER *HOLD*.  The collar is closed
                # and a turret is alive: the body's job is to be STANDING THERE
                # when a seat breaks, and an evictor three tiles away is a body
                # that is not.  Rung 1 re-seals the moment `needed` refills, and
                # this is what keeps the body in range to let it.
                if FS_EVICT_ON and not _v521_hold \
                        and self._fs_try_evict_launcher(ct, E, p, ti,
                                                        needed=needed):
                    self._fs_rung(ct, rnd, 2, E, p, needed, ti, orth_open)
                    self._v521_rung(ct, rnd, 2, _v521_st)
                    return
                # rung 3 -- CLEAR a squatting enemy building off a seat.  Rung 1
                # barriers it the same or the next round (the census re-reads
                # denial every round and a just-cleared seat jumps the queue).
                # ⭐ v521 1b -- also suppressed under HOLD, and for a reason
                # that is arithmetic rather than stylistic: with orth_open == 0
                # there is no squatted seat left to clear, so a rung-3 hit in
                # this state is the clause working on a tile the collar does not
                # need.  (If it never fires, this suppression is worth zero and
                # the RUNG521 tape will say so.)
                if not _v521_hold and self._fs_try_clear(ct, E, p, needed):
                    self._fs_rung(ct, rnd, 3, E, p, needed, ti, orth_open)
                    self._v521_rung(ct, rnd, 3, _v521_st)
                    return
                # rung 4 -- THE SENTINELS.  Bottom of the ladder BY DESIGN: it
                # fires on the rounds the collar has nothing actionable left,
                # which are exactly the rounds the raider would otherwise spend
                # walking.  No jump-queue clause is needed (v510 had one) --
                # under the ladder those rounds arrive on their own.
                # ⭐ v521: KEPT UNDER *HOLD*, SUPPRESSED UNDER *NEAR*.  Under
                # HOLD a SECOND aligned sentinel raises the damage rate INSIDE
                # an overlap window that is already open, which is the quantity
                # this build is buying, and v517's twin plank already prices it
                # against the collar's own repair allowance.  Under NEAR the
                # window is not open yet and the same purchase is off-collar
                # spend in the two rounds that decide whether it opens at all.
                if not _v521_near \
                        and self._fs_sentinel_ok(ct, ti, needed, orth_open) \
                        and self._fs_try_sentinel(ct, E, p):
                    self._fs_rung(ct, rnd, 4, E, p, needed, ti, orth_open)
                    self._v521_rung(ct, rnd, 4, _v521_st)
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
        # ⭐⭐ v518 CHANGE 2(b) -- WHILE NO FORWARD SENTINEL IS ALIVE, THE
        # SENTINEL'S REACH OUTRANKS THE EVICTOR'S.  The two terms are v515's
        # (`rstat`) and v516's (`sstat`), unchanged, both still PREFERENCES with
        # their own patience timers; the ONLY thing this flag changes is which
        # of the two tie-breaks first, and only in the state where the phase
        # budget says the clock is running (`arrive -> sent`, 81 rounds, 45% of
        # the r180 target).  The v516 ordering ("the collar is what the body is
        # there for") is restored the moment a sentinel exists.
        _sent_first = False
        if LOKI_FS_V518 and FS_V518_EARLYSITE and FS_V518_EARLY_REACH_FIRST:
            try:
                _sent_first = (self._fs_live_sentinels(ct, E)
                               <= FS_V518_EARLY_MAX_LIVE)
            except Exception:
                _sent_first = False
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
                if _sent_first:
                    k = (1 if (sx, sy) in axis else 0,
                         0 if (sx, sy) in sstat else 1,
                         0 if (sx, sy) in rstat else 1,
                         abs(sx - p.x) + abs(sy - p.y), rank)
                else:
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
        supp = LOKI_FS_CREW and fs_crew_on() and self.fs_role == "supp"
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

    def _v518_twin_reserve(self, ct, sen, bar):
        """⭐⭐ v518 CHANGE 3 -- CORE SIDE.  The titanium floor the twin's
        purchase actually needs, or 0.

        ⛔ THIS MUTATES `v518_res_until` AND IS CALLED FROM THE CORE'S TURN
        ONLY, once per round, from the one `fs_live` branch in `_core` -- the
        same contract `_v517_bank_open` documents for itself.

        WHY IT IS NOT `FS_V517_TWINBANK` AGAIN.  Two defects in that reserve,
        both arithmetic and both visible without a game:

        1. **IT IS PRICED BELOW THE BAR IT FUNDS.**  v517 holds
           `ti_floor >= sen + FS_SENTINEL_TI_FLOOR` (= sen + 4).  The purchase
           it exists for tests, under a hold,
           `ti >= min(len(needed), FS_V517_TWIN_NEEDED_CAP) * bar + sen
                 + FS_V517_TWIN_TI_FLOOR`  (= sen + 2*bar, and `bar` is 8-9 at
           the live 2.8x scale).  In this state `convert_ammo` is the marginal
           consumer, so THE BANK EQUILIBRATES TO EXACTLY `ti_floor` (v513
           change F measured that equilibrium to the titanium: "median bank
           equal to the floor").  A reserve 12-14 Ti under the bar therefore
           parks the bank permanently just short of the purchase.  Reported
           v517 measurement: 0 of 80 purchases under a hold.
        2. **IT READS A MONOTONE COUNTER FOR A LIVENESS QUESTION.**  v517 gates
           on `read_store(SLOT_FWD_GUN) < FS_SENTINEL_MAX`; `SLOT_FWD_GUN` is
           written only as `read + 1` and is never decremented (its own
           doctrine entry says so).  A team that bought two and lost one reads
           2 and can never reserve for the replacement -- exactly the state
           v514 change B (resite-on-death) exists to serve.  This reads
           LIVENESS: the v516 beat says >= 1 alive, the v517 peer stamp says
           >= 2 alive, so `beat AND NOT peer` is "exactly one", which is the
           mandate's own wording.

        BOUNDED, NOT A FREEZE.  It returns a ti_floor for `convert_ammo` and
        nothing else; it enters through `max()` so it can only RAISE the floor
        and can never lower `E1_AMMO_FLOOR`, the harvester reserve or the
        collar reserve; it caps at `sen + cap*bar + margin` and scales with
        nothing; and it RELEASES on (twin alive) or (no published hold for
        FS_V518_RES_TTL rounds).
        """
        if not (LOKI_FS_V518 and FS_V518_TWINRES):
            return 0
        try:
            rnd = ct.get_current_round()
        except Exception:
            return 0
        if self._v517_twin_live(ct):
            self.v518_res_until = -1         # the twin exists: release
            return 0
        # "exactly one live forward sentinel, and it is HOLDING".
        # `_fs_hold_live` already requires the exact v516 beat (a mod-15 stamp
        # nobody rewrites reads fresh once per wrap for ever -- v517 surprise
        # 1), so the liveness half is not re-tested here.
        if self._fs_hold_live(ct):
            self.v518_res_until = rnd + FS_V518_RES_TTL
        if rnd >= self.v518_res_until:
            return 0
        self.v518_res_rounds += 1
        return (sen + FS_V517_TWIN_NEEDED_CAP * bar + FS_V518_RES_MARGIN)

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

    def _fs_try_sentinel(self, ct, E, p, probe=False):
        """ONE ALIGNED SENTINEL, and the alignment is checked BEFORE the spend.

        ⛔ `probe=True` STOPS ONE STATEMENT SHORT OF `build_sentinel` and is the
        house pattern already used by `_fs_try_clear` / `_fs_try_evict_launcher`
        (see `_fs_rung`): the predicate cannot drift from the behaviour, because
        it IS the behaviour with the mutating call removed.  Used only by the
        v518 GAP518 decomposition instrument, which is off in every shipped
        configuration.

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
        if probe:
            return True
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
            # ⭐⭐ v520 CHANGE 1 -- THE IN-RING FERRY EXEMPTION, AND IT IS AS
            # NARROW AS THE RULE IT PIERCES.  Magnus's terminal-siting rule
            # puts this launcher inside the ring BY ARITHMETIC: a heal seat is
            # at dsq_core = 1, so any tile whose d^2<=2 pickup envelope covers
            # one is at dsq_core <= 5.  Without an exemption the launcher we
            # sited to make the split throw could never make it.
            # ⛔ THE ROLE-BY-SITE RULE EXISTS BECAUSE THE PROBE'S RING LAUNCHER
            # THREW OUR OWN SEALER OFF THE RING.  That cannot happen here: the
            # exemption only applies while an expected rider is still OUTSIDE
            # FS_RING_DSQ, so a body that has already arrived is never picked
            # up, and it lapses the round both riders are down -- after which
            # this launcher is an ordinary evictor for the rest of its life.
            if self._v520_on() and FS_V520_INRING_FERRY \
                    and rnd <= FS_V520_SPLIT_MAX_RND \
                    and self._v520_split_pending(ct, E, lp):
                return self._fs_ferry_launcher(ct, E, lp, rnd)
            if not FS_EVICT_ON:
                return False
            self._fs_evict(ct, E, lp)
            return True                      # never ferries.  Ever.

        return self._fs_ferry_launcher(ct, E, lp, rnd)

    def _v520_split_pending(self, ct, E, lp):
        """Is a published crew body adjacent to this launcher and STILL OUTSIDE
        the ring?  (v520 change 1: the in-ring exemption's whole safety case.)
        """
        if self.fs_thrown is None:
            self.fs_thrown = []
        want_ids = []
        for _s in self._fs_crew_slots():
            _b, _p, _r = self._fs_state_at(ct, _s)
            if _r and (_r - 1) not in want_ids:
                want_ids.append(_r - 1)
        if not want_ids:
            return False
        try:
            for eid in ct.get_nearby_units():
                if eid not in want_ids or eid in self.fs_thrown:
                    continue
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                if ct.get_team(eid) != self.team:
                    continue
                bp = ct.get_position(eid)
                if bp.distance_squared(lp) > 2:
                    continue
                if dsq_core(bp, E) <= FS_RING_DSQ:
                    continue                 # already arrived: never our rider
                return True
        except Exception:
            return False
        return False

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
            and LOKI_FS_CREW and fs_crew_on()
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
                    if dsq_core(lp, E) <= FS_RING_DSQ \
                            and dsq_core(bp, E) <= FS_RING_DSQ:
                        # ⛔ v520: an IN-RING launcher never picks up a body
                        # that has already ARRIVED.  Unreachable with the plank
                        # off (an in-ring launcher never enters this function),
                        # and it is the safety case for the exemption above.
                        continue
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
            # ⭐⭐ v520 CHANGE 1 -- THE TERMINAL SPLIT.  Magnus, verbatim
            # intent: two raiders, one to the BACK and one to the FRONT of the
            # enemy core, so they can barrier from different sides.
            # WHICH RIDER GETS WHICH ARC IS NOT ARBITRARY: the lead is thrown
            # FIRST (it buys the next link, so it must land first) and it takes
            # the BACK arc, because the back is the arc that NEEDS the throw --
            # the core+ring span is 4-6 tiles against a 5.1-tile envelope, so
            # the far side is at the edge of what a launcher can reach, while
            # the front arc is reachable from any terminal tile by construction.
            # ⛔ AND THE STRICT-IMPROVEMENT RULE IS BYPASSED FOR THE FRONT RIDER
            # ONLY, AND ONLY ONTO A RING TILE.  `_fs_target` is the BACKSIDE
            # tile, so a front-arc landing is by definition further from it than
            # the rider already was -- the parent's rule would refuse the throw
            # this change exists to make.  Requiring the landing to be INSIDE
            # FS_RING_DSQ is what keeps that from becoming "throw riders
            # anywhere": the only exception is a tile ON the collar.
            # ⛔ TERMINAL LINKS ONLY, AND THE FIRST SMOKE RUN IS WHY.  Without
            # the distance gate the arc key replaced the parent's key on EVERY
            # hop -- measured 5-6 split throws per game on nordkap/atoll, half
            # of them from launchers 8-10 tiles out, where "the front arc" is
            # just a worse forward throw.  The split is an ARRIVAL clause: it
            # only means anything from a launcher close enough that both arcs
            # are a real choice.
            if self._v520_on() and FS_V520_SPLIT \
                    and rnd <= FS_V520_SPLIT_MAX_RND \
                    and dsq_core(lp, E) <= FS_V520_TERM_DSQ:
                arc = (FS_V520_ARC_BACK if not self.fs_thrown
                       else FS_V520_ARC_FRONT)
                site = self._v520_arc_site(ct, E, lp, arc)
                if site is not None:
                    dc = dsq_core(site, E)
                    ok = (dc <= FS_RING_DSQ) or (dc < dsq_core(me, E))
                    if ok:
                        try:
                            can = ct.can_launch(me, site)
                        except Exception:
                            can = False
                        if can:
                            anchor = self._v520_arc_anchor(ct, E, arc)
                            walk = (site.distance_squared(anchor)
                                    if anchor is not None else -1)
                            try:
                                self._fs_draw_line(ct, me, site, 255, 120, 0)
                                ct.launch(me, site)
                            except Exception:
                                site = None
                            if site is not None:
                                self.v520_split_n += 1
                                self.fs_thrown.append(me_id)
                                if V526RC:
                                    try:
                                        print('RC SPLIT', rnd,
                                              'lid', ct.get_id(),
                                              'body', me_id,
                                              'arc', arc,
                                              'n', len(self.fs_thrown),
                                              file=sys.stderr)
                                    except Exception:
                                        pass
                                self.fs516_last_throw = rnd
                                if FS_V520_SPLIT_LOG:
                                    try:
                                        print("SPLIT520", rnd,
                                              "lch", (lp.x, lp.y),
                                              "body", me_id, "arc", arc,
                                              "to", (site.x, site.y),
                                              "dsq", dc, "walk", walk,
                                              "n", self.v520_split_n,
                                              file=sys.stderr)
                                    except Exception:
                                        pass
                                self._fs_log("SPLIT", rnd, "arc", arc,
                                             "to", (site.x, site.y),
                                             "body", me_id, "walk", walk)
                                return self._v520_after_throw(
                                    ct, E, lp, rnd, relay, want_ids)
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
                    if V526RC:
                        try:
                            print('RC THROW', rnd,
                                  'lid', ct.get_id(),
                                  'body', me_id,
                                  'n', len(self.fs_thrown),
                                  file=sys.stderr)
                        except Exception:
                            pass
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
                    if self._v520_on():
                        return self._v520_after_throw(
                            ct, E, lp, rnd, relay, want_ids)
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
        if self._v520_on() and FS_V520_TERM_NOTEAR \
                and self._v520_covers(E, lp):
            # ⛔ THE TERMINAL LAUNCHER IS EXEMPT FROM THE TTL TOO, and this is
            # the branch that would otherwise kill it: a link that has thrown
            # both riders has `relay and self.fs_thrown`, so its TTL is
            # FS_RELAY_TTL = 3 rounds.  A launcher covering a heal seat is an
            # evictor and an evictor's job is to stand.
            self.v520_term = True
            return True
        if rnd - self.fs_born >= ttl:
            ct.self_destruct()
        return True

    def _v520_after_throw(self, ct, E, lp, rnd, relay, want_ids):
        """The hold / teardown decision after a throw, with the v520 exemption.

        ⭐ THE EXEMPTION, AND IT IS ONE LINE OF POLICY: A LAUNCHER THAT COVERS A
        HEAL SEAT NEVER TEARS ITSELF DOWN.  Standing IS its job once the riders
        are down -- it is the EVICTOR (Magnus's priority 2, "keep healers and
        enemy builders away from their core"), its covered seats count as
        denial in `_fs_census`, and `_fs_live_evictors`' own measured
        discriminator (coverage, not tagging) already classifies it as one.
        The scale argument that motivates teardown does not apply to a launcher
        that is doing a job: the +10% is bought, not wasted.
        ⛔ IDLETEAR (v516 1b) cannot reach it either -- that branch is gated on
        `not self.fs_ferry_seen`, and a launcher that has thrown a rider has it
        True -- but the FS_RELAY_TTL / FS_LAUNCHER_TTL path at the end of
        `_fs_ferry_launcher` can, so the exemption is asserted THERE too.
        """
        hold = (any(i not in self.fs_thrown for i in want_ids)
                and rnd - self.fs_born < FS_RELAY_TTL)
        if not (LOKI_FS_V516 and FS_V516_TEARDOWN and FS_V516_HOLD_GENERAL):
            hold = hold and relay
        if FS_V520_TERM_NOTEAR and self._v520_covers(E, lp):
            self.v520_term = True
            hold = True
        if not hold:
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
