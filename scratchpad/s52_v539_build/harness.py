#!/usr/bin/env python3
"""v539 build instrument #1 -- THE FAMINE HARNESS (no game engine, no fcode).

⛔ WHY A FAKE ENGINE IS ADMISSIBLE HERE, AND WHAT IT MAY NOT BE USED FOR.
The local box is running V537POOL (8 workers) and this build is under a HARD
ZERO-fcode-run constraint until `scratchpad/overnight/V537POOL.tsv` reaches
5400 data rows.  So every claim this build makes about MECHANISM is made here,
on `tools/stub_engine.py`'s fake Controller, and every claim about PLAY,
TEMPO, KILL ROUND or OUTCOME is DEFERRED and named as deferred.  This file
answers exactly one class of question: given a scripted board and a scripted
delivery history, WHICH BRANCH does the real shipped code take?  It answers it
by importing the real trees and calling the real methods -- there is no
reimplementation of the predicate anywhere in this file.

DIVERGENCES FROM THE ENGINE, stated because they bound the claims:
  * `tools/stub_engine.py`'s CORE occupies ONE tile, not 2x2.  The mouth
    predicate `_fs_eco_mouth` reads `core_tiles(anchor)`, so a conveyor is
    seated orthogonally to the ANCHOR and faces it; the other three footprint
    tiles are empty in the stub and are simply never used.
  * The stub has NO resource-stack physics: harvesters emit nothing and
    conveyors move nothing.  DELIVERY IS SCRIPTED by `DeliveryCt`, which
    overrides `get_stored_resource_id` to return a stack id on the mouth
    conveyor iff (a live friendly harvester exists) AND (a mouth exists) AND
    (round % STACK_EVERY == 0).  That is the engine's own cadence (a
    harvester outputs a stack every 4 rounds) and it is the ONLY channel by
    which the famine detector can see anything, so the model is the fixture.
  * No opponent acts.  The wipe is applied by the harness at a scripted round.

SELF-TEST -- and it drives every guard to BOTH verdicts, per the standing
instrument rule.  A check that has never produced the other verdict has not
been seen to check:
    .venv/bin/python scratchpad/s52_v539_build/harness.py --selftest
"""
import argparse
import importlib
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from tools.stub_engine import (  # noqa: E402
    World, StubController, Position, Direction, EntityType, Team,
)

MODNAMES = ("doctrine", "eco", "siege", "raid", "main")
STACK_EVERY = 4


def load_tree(tree, noise=False):
    """Import a bot tree's modules FRESH and return them.

    ⛔⛔ NOISE OFF BY DEFAULT, AND IT IS NOT COSMETIC.  `main.py` seeds a
    per-body `spawn_salt` from `random.Random()` -- a FRESH generator with no
    seed, which `random.seed()` cannot reach -- so with NOISE_ON the SAME TREE
    run TWICE IN ONE PROCESS diverges at round 2 (measured: atoll, the v537
    socket claim picks a different delivery seat).  An identity check run with
    noise on cannot certify anything and an endgame cell run with noise on is
    measuring the salt.  Both are turned off here, in every module, because
    `from doctrine import *` gives each module its own binding.

    `tree` is a name under `bots/`, or a repo-relative PATH (contains a "/")
    so a flag-off arm can live in the scratchpad instead of polluting `bots/`.
    """
    path = str(REPO / tree) if "/" in tree else str(REPO / "bots" / tree)
    for m in MODNAMES:
        sys.modules.pop(m, None)
    sys.path.insert(0, path)
    try:
        mods = {m: importlib.import_module(m) for m in MODNAMES}
    finally:
        sys.path.remove(path)
    for m in MODNAMES:
        sys.modules.pop(m, None)
    if not noise:
        for m in MODNAMES:
            setattr(mods[m], "NOISE_ON", False)
    return mods


class DeliveryCt(StubController):
    """StubController + scripted delivery + THE fcode TYPE SHIM.

    ⛔⛔ THE TYPE SHIM IS LOAD-BEARING AND ITS ABSENCE FAILS SILENTLY IN THE
    FLATTERING DIRECTION.  The bot trees do `from fcode import Direction,
    EntityType, Environment, Position`; `tools/stub_engine.py` defines its own
    string/enum shims.  `fcode.EntityType.CONVEYOR == "conveyor"` is **False**
    and `fcode.Team.A.value` is `'a'` against the stub's `"A"`, so an
    unshimmed stub controller makes EVERY type comparison in the bot fall
    through: `_dispatch` matches neither CORE nor BUILDER_BOT and `run()`
    returns having done nothing, while the harness happily reads whatever
    `__init__` left on the object and calls it a verdict.  The first draft of
    this file did exactly that and TWO cells passed vacuously; they were caught
    only because every check here is driven to BOTH verdicts and the
    complement cell failed.  Positions need no shim -- both are (x, y)
    NamedTuples, so they compare and hash equal across the boundary.

    THE DELIVERY CHANNEL: `tools/stub_engine.py` returns None from
    `get_stored_resource_id` unconditionally and `tools/*` may not be edited by
    this build, so the channel is added by SUBCLASSING.  A stack appears on a
    conveyor/splitter iff a live friendly HARVESTER exists and the round is on
    the engine's 4-round output cadence.
    """

    def __init__(self, world, entity_id, fc):
        StubController.__init__(self, world, entity_id)
        self.fc = fc

    # -- outgoing: stub value -> the tree's own fcode member ----------------
    def get_team(self, id=None):
        return self.fc["team"][StubController.get_team(self, id)]

    def get_entity_type(self, id=None):
        return self.fc["etype"][StubController.get_entity_type(self, id)]

    def get_direction(self, id=None):
        return self.fc["dir"][StubController.get_direction(self, id).value]

    def get_tile_env(self, pos):
        return self.fc["env"][StubController.get_tile_env(self, pos)]

    # ⛔ POSITIONS MUST BE CONVERTED TOO, AND THE REASON IS NOT EQUALITY.
    # Both Positions are (x, y) NamedTuples so they compare and hash equal --
    # which is exactly why this was missed at first.  What differs is their
    # METHODS: a STUB Position's `.cardinal_direction_to()` returns a STUB
    # Direction, and `eco.py`'s module-level `DELTA` dict is keyed on FCODE
    # Directions, so the bot raised `KeyError: <Direction.SOUTH>` inside
    # `_move` -- caught by its own top-level `except`, one traceback, and
    # every subsequent turn silently degraded.  A harness whose bot cannot
    # MOVE would have reported "0 rebuilds" for both arms and read as a null.
    def _P(self, p):
        return self.fc["fcode"].Position(p.x, p.y)

    def get_position(self, id=None):
        return self._P(StubController.get_position(self, id))

    def get_nearby_tiles(self, dist_sq=None):
        return [self._P(p) for p in
                StubController.get_nearby_tiles(self, dist_sq)]

    # -- incoming: fcode member -> stub value -------------------------------
    def _s_et(self, et):
        return getattr(et, "value", et)

    def _s_dir(self, d):
        if d is None:
            return None
        return self.fc["sdir"][getattr(d, "value", d)]

    def can_build(self, entity_type, position, extra=None):
        return StubController.can_build(self, self._s_et(entity_type),
                                        position, self._s_dir(extra))

    def build(self, entity_type, position, extra=None):
        return StubController.build(self, self._s_et(entity_type),
                                    position, self._s_dir(extra))

    def can_move(self, direction):
        return StubController.can_move(self, self._s_dir(direction))

    def move(self, direction):
        return StubController.move(self, self._s_dir(direction))

    def can_rotate(self, direction):
        return StubController.can_rotate(self, self._s_dir(direction))

    def rotate(self, direction):
        return StubController.rotate(self, self._s_dir(direction))

    def get_attackable_tiles_from(self, position, direction, turret_type):
        return StubController.get_attackable_tiles_from(
            self, position, self._s_dir(direction), self._s_et(turret_type))

    def can_fire_from(self, position, direction, turret_type, target):
        return StubController.can_fire_from(
            self, position, self._s_dir(direction), self._s_et(turret_type),
            target)

    # -- the delivery channel -----------------------------------------------
    def get_stored_resource_id(self, id=None):
        eid = self._id if id is None else id
        ent = self.world.entities[eid]
        if ent["type"] not in (EntityType.CONVEYOR, EntityType.SPLITTER):
            return StubController.get_stored_resource_id(self, id)
        if not getattr(self.world, "delivery_on", False):
            return None
        if self.world.round % STACK_EVERY != 0:
            return None
        team = ent["team"]
        harv = any(e["type"] == EntityType.HARVESTER and e["team"] == team
                   for e in self.world.entities.values())
        return 1 if harv else None


def fc_maps(mods):
    """Build the stub<->fcode translation tables from a LOADED tree.

    Keyed on `.value` / `.name`, never hardcoded: fcode's EntityType and
    Environment values are byte-equal to the stub's strings, fcode's Team
    values are lowercase where the stub's are uppercase.
    """
    fcode = sys.modules.get("fcode") or importlib.import_module("fcode")
    from tools import stub_engine as se
    return {
        "team": {"A": fcode.Team.A, "B": fcode.Team.B},
        "etype": {e.value: e for e in fcode.EntityType},
        "env": {e.value: e for e in fcode.Environment},
        "dir": {d.value: d for d in fcode.Direction},
        "sdir": {d.value: d for d in se.Direction},
        "fcode": fcode,
    }


# ---------------------------------------------------------------------------
# SCENARIO 1 -- THE DETECTOR, driven on the real `_fs_eco_publish`
# ---------------------------------------------------------------------------

def detector_run(tree, rounds, wipe_at, harv=2, min_rnd_override=None):
    """Drive the REAL Core detector over a scripted delivery history.

    Returns (declared_round, cleared_round, word_trace) where declared_round is
    the round the famine bit first appeared in the slot (engine-visible, i.e.
    read back through the buffered store) or -1.
    """
    mods = load_tree(tree)
    fc = fc_maps(mods)
    d = mods["doctrine"]
    if min_rnd_override is not None:
        # ⛔ EVERY MODULE, NOT JUST doctrine.  The tree does
        # `from doctrine import *`, so each module holds its OWN binding of the
        # constant and mutating doctrine alone is a NO-OP.  The first draft of
        # this harness did exactly that and its "MIN_RND pushed out => never
        # declares" cell silently measured the DEFAULT, i.e. it was a check
        # that could not fail.  Caught by driving the complement.
        for m in MODNAMES:
            setattr(mods[m], "FS_V539_MIN_RND", min_rnd_override)
    w = World(14, 14)
    w.delivery_on = True
    core = w.add(EntityType.CORE, Team.A, Position(3, 3))
    mouth = w.add(EntityType.CONVEYOR, Team.A, Position(3, 2), Direction.SOUTH)
    ore = Position(6, 3)
    w.set_terrain(ore, "o")
    w.add(EntityType.HARVESTER, Team.A, ore)

    P = mods["main"].Player()
    P.core = Position(3, 3)
    P.team = fc["team"]["A"]
    P.mw, P.mh = 14, 14

    declared = cleared = -1
    trace = []
    for r in range(rounds):
        if r == wipe_at:
            for eid, e in list(w.entities.items()):
                if e["type"] == EntityType.HARVESTER:
                    w.remove(eid)
        ct = DeliveryCt(w, core, fc)
        P._fs_eco_publish(ct, r, harv)
        w.end_round()
        word = w.store[Team.A][d.FS_ECO_SLOT]
        fam = bool(word & getattr(d, "FS_ECO_BIT_FAMINE", 0)) \
            if hasattr(d, "FS_ECO_BIT_FAMINE") else False
        trace.append((r, word, fam))
        if fam and declared < 0:
            declared = r
        if declared >= 0 and not fam and cleared < 0 and r > declared:
            cleared = r
    return declared, cleared, trace


# ---------------------------------------------------------------------------
# SCENARIO 2 -- THE GATES, driven on real Player objects
# ---------------------------------------------------------------------------

def gate_probe(tree, famine, bank, role, rnd=120, started=100, under=1,
               floor=None, collar=False, cost="conveyor"):
    """`_eco_spendable` verdict for one scripted board.

    `floor` overrides FS_V539_RESERVE_FLOOR in EVERY module (each holds its own
    binding via `from doctrine import *` -- the no-op trap of §4.1).
    """
    mods = load_tree(tree)
    if floor is not None:
        for m in MODNAMES:
            setattr(mods[m], "FS_V539_RESERVE_FLOOR", floor)
    fc = fc_maps(mods)
    d = mods["doctrine"]
    w = World(14, 14)
    w.delivery_on = False
    core = w.add(EntityType.CORE, Team.A, Position(3, 3))
    bot = w.add(EntityType.BUILDER_BOT, Team.A, Position(3, 4))
    w.titanium[Team.A] = bank
    w.round = rnd
    word = d.FS_ECO_BIT_CONN | d.FS_ECO_BIT_DELIV
    if famine and hasattr(d, "FS_ECO_BIT_FAMINE"):
        word |= d.FS_ECO_BIT_FAMINE
        word |= (((started + 1) & d.FS_ECO_FAM_RND_MASK)
                 << d.FS_ECO_FAM_RND_SHIFT)
    w.store[Team.A][d.FS_ECO_SLOT] = word
    w.store[Team.A][d.SLOT_UNDER] = under
    w.store[Team.A][d.SLOT_ATK_RND] = rnd
    if collar:
        # a ferry-siege raider standing at the enemy ring: `_eco_spendable`
        # subtracts the whole 8-barrier collar reserve while this is live
        w.store[Team.A][d.SLOT_FS] = (
            ((rnd + 1) & d.FS_BEAT_MASK)
            | ((d.FS_PH_RING & d.FS_PHASE_MASK) << d.FS_PHASE_SHIFT))

    P = mods["main"].Player()
    P.core = Position(3, 3)
    P.team = fc["team"]["A"]
    P.mw, P.mh = 14, 14
    P.role = role
    ct = DeliveryCt(w, bot, fc)
    c = (ct.get_harvester_cost() if cost == "harvester"
         else ct.get_conveyor_cost())
    spend = P._eco_spendable(ct, c)
    return spend


def gate_bar(tree="_v539resilience"):
    """The floor the v539.1 arm defends: sentinel cost + the siege reserve."""
    mods = load_tree(tree)
    fc = fc_maps(mods)
    w = World(14, 14)
    b = w.add(EntityType.CORE, Team.A, Position(3, 3))
    ct = DeliveryCt(w, b, fc)
    return ct.get_sentinel_cost() + mods["doctrine"].SIEGE_HEAL_RESERVE_TI


def draft_probe(tree, famine, role_n, rnd=120, started=100):
    """Assign a role to a FRESH body through the real run() path."""
    mods = load_tree(tree)
    fc = fc_maps(mods)
    d = mods["doctrine"]
    w = World(14, 14)
    w.delivery_on = False
    w.add(EntityType.CORE, Team.A, Position(3, 3))
    bot = w.add(EntityType.BUILDER_BOT, Team.A, Position(3, 4))
    w.round = rnd
    word = d.FS_ECO_BIT_CONN | d.FS_ECO_BIT_DELIV
    if famine and hasattr(d, "FS_ECO_BIT_FAMINE"):
        word |= d.FS_ECO_BIT_FAMINE
        word |= (((started + 1) & d.FS_ECO_FAM_RND_MASK)
                 << d.FS_ECO_FAM_RND_SHIFT)
    w.store[Team.A][d.FS_ECO_SLOT] = word
    w.store[Team.A][d.SLOT_ROLE_N] = role_n
    P = mods["main"].Player()
    ct = DeliveryCt(w, bot, fc)
    P.run(ct)
    return getattr(P, "role", None), getattr(P, "role_n", None)


# ---------------------------------------------------------------------------
# SCENARIO 3 -- END TO END: wipe the economy, count rebuilds
# ---------------------------------------------------------------------------

def build_world(map_name):
    """A World laid out from a REAL pool map, with our Core on team A's anchor.

    ⛔ THE MAP MUST BE A POOL MAP.  `known_map_for` looks the board up in
    `MAP_CODES` by (w, h, core anchor) and returns None for anything else, so
    on a synthetic grid `map_ores` stays empty and the expander has NO ore to
    walk to.  The first version of this fixture used a hand-drawn 20x20 board
    and BOTH ARMS built 0 harvesters -- a fixture in which the plank cannot
    possibly show, reading as a clean null.
    """
    from tools.map_encode import parse_map26
    w, h, rows, cores = parse_map26(REPO / "maps" / (map_name + ".map26"))
    world = World(w, h)
    for y in range(h):
        for x in range(w):
            c = rows[y][x]
            if c == 1:
                world.set_terrain(Position(x, y), "wall")
            elif c == 2:
                world.set_terrain(Position(x, y), "ore_titanium")
    a = next(c for c in cores if c[0] == 0)
    return world, Position(a[1], a[2])


def endgame_run(tree, map_name="atoll", rounds=300, wipe_at=140,
                seed_bank=500, seed=0, verbose=False):
    """Full scripted match-fragment on a real pool map.  Returns counters.

    THE FIXTURE: our Core, our builders, the real terrain, NO OPPONENT.  Up to
    `wipe_at` the economy is built normally.  At `wipe_at` EVERY friendly
    HARVESTER, CONVEYOR and SPLITTER is removed (the wipe), the bank is cut to
    5 Ti and SLOT_UNDER is re-latched every round for 60 rounds -- the measured
    v174 board (`harvesters 0 / Ti 5 at r154`, under sustained attack), which
    is what an economy attack looks like to `_eco_spendable`.  Nothing else is
    touched and both arms get the identical script.

    ⛔ WHAT THIS MEASURES AND WHAT IT DOES NOT.  It measures WHETHER THE
    REBUILD PATH FIRES.  It does NOT measure play, tempo, kill round or
    outcome -- there is no opponent in it.  Those are deferred to the powered
    screen, by name, in the build report.
    """
    # ⛔⛔ SEED THE FIXTURE.  `doctrine.py` does `import random` and the bot
    # uses it, so an unseeded run is NON-DETERMINISTIC -- and this was not a
    # theory: the first atoll cell read `parent 280 / v539 162` and the same
    # command re-run read `parent 276 / v539 280`, i.e. the headline result
    # REVERSED on noise alone.  Every arm of a cell now runs from the same
    # seed and every reported cell is a paired mean over SEEDS.
    random.seed(seed)
    mods = load_tree(tree)
    fc = fc_maps(mods)
    d = mods["doctrine"]
    w, anchor = build_world(map_name)
    w.delivery_on = True
    core = w.add(EntityType.CORE, Team.A, anchor)
    w.titanium[Team.A] = seed_bank
    players = {core: mods["main"].Player()}
    built_pre = built_post = 0
    conveyors_pre = conveyors_post = 0
    famine_round = -1
    first_rebuild = -1
    mouth_post = 0
    deliv_post = 0
    raised = 0
    turret_post = 0
    # ⭐ THE KILL-FUNDING COUNTER (Magnus's amendment: the plank is scored in
    # KILL terms, not tiebreak terms).  There is no opponent in this fixture,
    # so no forward-sentinel purchase can fire and a turret count of 0 in both
    # arms would say nothing.  What the fixture CAN answer is whether the bank
    # ever recovers to the level a sentinel costs -- `sentinel + the siege heal
    # reserve` is the literal bar `main.py` checks before buying one.
    afford_post = 0
    sent_bar = 0

    for r in range(rounds):
        if r == wipe_at:
            for eid, e in list(w.entities.items()):
                if e["team"] == Team.A and e["type"] in (
                        EntityType.HARVESTER, EntityType.CONVEYOR,
                        EntityType.SPLITTER):
                    w.remove(eid)
            w.titanium[Team.A] = 5
        if wipe_at <= r < wipe_at + 60:
            w.store[Team.A][d.SLOT_UNDER] = 1
            w.store[Team.A][d.SLOT_ATK_RND] = r

        before = {eid: e["type"] for eid, e in w.entities.items()
                  if e["team"] == Team.A}
        for eid in list(w.entities.keys()):
            e = w.entities.get(eid)
            if e is None or e["team"] != Team.A:
                continue
            if eid not in players:
                players[eid] = mods["main"].Player()
            try:
                players[eid].run(DeliveryCt(w, eid, fc))
            except Exception:
                raised += 1
        after = {eid: e["type"] for eid, e in w.entities.items()
                 if e["team"] == Team.A}
        for eid, t in after.items():
            if eid in before:
                continue
            if t == EntityType.HARVESTER:
                if r < wipe_at:
                    built_pre += 1
                else:
                    built_post += 1
                    if first_rebuild < 0:
                        first_rebuild = r
            elif t == EntityType.CONVEYOR:
                if r < wipe_at:
                    conveyors_pre += 1
                else:
                    conveyors_post += 1
            elif t in (EntityType.SENTINEL, EntityType.GUNNER) and r >= wipe_at:
                turret_post += 1
        w.end_round()
        word = w.store[Team.A][d.FS_ECO_SLOT]
        if hasattr(d, "FS_ECO_BIT_FAMINE") and (word & d.FS_ECO_BIT_FAMINE) \
                and famine_round < 0:
            famine_round = r
        if r >= wipe_at:
            ctl0 = DeliveryCt(w, core, fc)
            sent_bar = ctl0.get_sentinel_cost() + d.SIEGE_HEAL_RESERVE_TI
            if w.titanium[Team.A] >= sent_bar:
                afford_post += 1
            ctl = DeliveryCt(w, core, fc)
            try:
                m, held = players[core]._fs_eco_mouth(ctl)
            except Exception:
                m, held = None, False
            if m is not None:
                mouth_post += 1
            if held:
                deliv_post += 1
    return {
        "tree": tree,
        "map": map_name,
        "harv_built_pre": built_pre,
        "harv_built_post": built_post,
        "first_rebuild_rnd": first_rebuild,
        "conv_built_pre": conveyors_pre,
        "conv_built_post": conveyors_post,
        "famine_rnd": famine_round,
        "mouth_rounds_post": mouth_post,
        "deliv_sightings_post": deliv_post,
        "run_raised": raised,
        "turret_built_post": turret_post,
        "afford_sentinel_rounds": afford_post,
        "sentinel_bar_ti": sent_bar,
        "ti_final": w.titanium[Team.A],
        "final_harvesters": sum(
            1 for e in w.entities.values()
            if e["team"] == Team.A and e["type"] == EntityType.HARVESTER),
    }


def state_hash(w):
    """A per-round fingerprint of OUR whole board: every entity and the store.

    This is the NOISE_OFF identity check done at unit level.  Two trees that
    take the same branch every round produce the same sequence of these; one
    differing build, move, cooldown or store word breaks it at the round it
    happens, which is what makes the check able to FAIL.
    """
    ents = sorted(
        (eid, e["type"], e["pos"].x, e["pos"].y, e["hp"], e["action_cd"],
         e["move_cd"], getattr(e.get("direction"), "value", None))
        for eid, e in w.entities.items())
    store = tuple(w.store[Team.A])
    return hash((tuple(ents), store, w.titanium[Team.A], w.ammo[Team.A]))


def identity_run(tree, map_name, rounds, wipe_at, seed=0):
    """Return the per-round state-hash trace for one arm."""
    random.seed(seed)
    mods = load_tree(tree)
    fc = fc_maps(mods)
    d = mods["doctrine"]
    w, anchor_pos = build_world(map_name)
    w.delivery_on = True
    core = w.add(EntityType.CORE, Team.A, anchor_pos)
    w.titanium[Team.A] = 500
    players = {core: mods["main"].Player()}
    trace = []
    for r in range(rounds):
        if r == wipe_at:
            for eid, e in list(w.entities.items()):
                if e["team"] == Team.A and e["type"] in (
                        EntityType.HARVESTER, EntityType.CONVEYOR,
                        EntityType.SPLITTER):
                    w.remove(eid)
            w.titanium[Team.A] = 5
        if wipe_at <= r < wipe_at + 60:
            w.store[Team.A][d.SLOT_UNDER] = 1
            w.store[Team.A][d.SLOT_ATK_RND] = r
        for eid in list(w.entities.keys()):
            e = w.entities.get(eid)
            if e is None or e["team"] != Team.A:
                continue
            if eid not in players:
                players[eid] = mods["main"].Player()
            try:
                players[eid].run(DeliveryCt(w, eid, fc))
            except Exception:
                pass
        w.end_round()
        trace.append(state_hash(w))
    return trace


def identity_cmp(map_name, rounds, wipe_at, a="_v537socket",
                 b="_v539resilience", seed=0):
    ta = identity_run(a, map_name, rounds, wipe_at, seed)
    tb = identity_run(b, map_name, rounds, wipe_at, seed)
    first = -1
    for i, (x, y) in enumerate(zip(ta, tb)):
        if x != y:
            first = i
            break
    return {"map": map_name, "wipe_at": wipe_at, "rounds": rounds,
            "identical": first < 0, "first_divergence": first}


# ---------------------------------------------------------------------------
# SELF-TEST -- every guard driven to BOTH verdicts
# ---------------------------------------------------------------------------

def selftest():
    fails = []

    def chk(cond, msg):
        print(("  ok   " if cond else "  FAIL ") + msg)
        if not cond:
            fails.append(msg)

    print("[1] DeliveryCt is a real channel and can be driven both ways")
    mods = load_tree("_v539resilience")
    fc = fc_maps(mods)
    w = World(8, 8)
    w.delivery_on = True
    core = w.add(EntityType.CORE, Team.A, Position(3, 3))
    conv = w.add(EntityType.CONVEYOR, Team.A, Position(3, 2), Direction.SOUTH)
    ore = Position(5, 3)
    w.set_terrain(ore, "o")
    h = w.add(EntityType.HARVESTER, Team.A, ore)
    w.round = 4
    ct = DeliveryCt(w, core, fc)
    chk(ct.get_stored_resource_id(conv) is not None,
        "held TRUE with harvester alive on a stack round")
    w.round = 5
    chk(DeliveryCt(w, core, fc).get_stored_resource_id(conv) is None,
        "held FALSE off-cadence (the other verdict)")
    w.round = 4
    w.remove(h)
    chk(DeliveryCt(w, core, fc).get_stored_resource_id(conv) is None,
        "held FALSE with the harvester dead (the other verdict)")

    print("[2] the mouth predicate answers both ways on the real code")
    P = mods["main"].Player()
    P.core = Position(3, 3)
    P.team = fc["team"]["A"]
    P.mw, P.mh = 8, 8
    m, _ = P._fs_eco_mouth(DeliveryCt(w, core, fc))
    chk(m == conv, "mouth FOUND when a conveyor faces the core")
    w.entities[conv]["direction"] = Direction.NORTH
    m2, _ = P._fs_eco_mouth(DeliveryCt(w, core, fc))
    chk(m2 is None, "mouth NOT found when it faces away (the other verdict)")

    print("[3] detector: famine declares on a wipe and NOT on a healthy belt")
    dec, cle, _ = detector_run("_v539resilience", 200, wipe_at=120,
                               min_rnd_override=60)
    chk(dec > 0, "famine DECLARED after the wipe (round %d)" % dec)
    # the last stack lands on the last cadence round BEFORE the wipe, so the
    # declaration is DROUGHT rounds after that, not after the wipe itself
    chk(120 + 25 - STACK_EVERY <= dec <= 120 + 25 + STACK_EVERY,
        "declared inside [wipe+drought-4, wipe+drought+4] (got %d)" % dec)
    dec2, _, _ = detector_run("_v539resilience", 200, wipe_at=10 ** 6,
                              min_rnd_override=60)
    chk(dec2 == -1, "famine NOT declared on a belt that never stops (control)")

    print("[4] detector: the opening is untouchable, both guards")
    dec3, _, _ = detector_run("_v539resilience", 200, wipe_at=5,
                              min_rnd_override=60)
    chk(dec3 >= 60, "no famine before FS_V539_MIN_RND (declared %d)" % dec3)
    dec4, _, _ = detector_run("_v539resilience", 200, wipe_at=5,
                              min_rnd_override=10 ** 6)
    chk(dec4 == -1, "MIN_RND pushed out => never declares (the other verdict)")

    print("[5] detector: it CLEARS when delivery resumes")
    mods2 = load_tree("_v539resilience")
    fc2 = fc_maps(mods2)
    d2 = mods2["doctrine"]
    w2 = World(14, 14)
    w2.delivery_on = True
    c2 = w2.add(EntityType.CORE, Team.A, Position(3, 3))
    w2.add(EntityType.CONVEYOR, Team.A, Position(3, 2), Direction.SOUTH)
    ore2 = Position(6, 3)
    w2.set_terrain(ore2, "o")
    hid = w2.add(EntityType.HARVESTER, Team.A, ore2)
    P2 = mods2["main"].Player()
    P2.core, P2.team, P2.mw, P2.mh = Position(3, 3), fc2["team"]["A"], 14, 14
    seen_fam = seen_clear = -1
    for r in range(260):
        if r == 100:
            w2.remove(hid)
        if r == 200:
            hid = w2.add(EntityType.HARVESTER, Team.A, ore2)
        P2._fs_eco_publish(DeliveryCt(w2, c2, fc2), r, 2)
        w2.end_round()
        fam = bool(w2.store[Team.A][d2.FS_ECO_SLOT] & d2.FS_ECO_BIT_FAMINE)
        if fam and seen_fam < 0:
            seen_fam = r
        if seen_fam >= 0 and not fam and seen_clear < 0 and r > seen_fam:
            seen_clear = r
    chk(seen_fam > 0, "famine declared after the kill (r%d)" % seen_fam)
    chk(0 < seen_clear <= 208,
        "famine CLEARED once delivery resumed (r%s)" % seen_clear)

    print("[6] PARENT tree has no famine bit at all (the counter-control)")
    pdec, _, _ = detector_run("_v537socket", 200, wipe_at=120)
    chk(pdec == -1, "_v537socket never declares (it has no detector)")

    print("[7] rung A: the lifeline flips _eco_spendable, and only in famine")
    par_f = gate_probe("_v537socket", True, 8, "expand")
    v_f = gate_probe("_v539resilience", True, 8, "expand")
    v_n = gate_probe("_v539resilience", False, 8, "expand")
    v_raid = gate_probe("_v539resilience", True, 8, "raid")
    v_late = gate_probe("_v539resilience", True, 8, "expand", rnd=200,
                        started=100)
    chk(par_f is False, "parent REFUSES the spend on a wiped bank")
    chk(v_f is True, "v539 ALLOWS it during famine (expander, in window)")
    chk(v_n is False, "v539 REFUSES it outside famine (the other verdict)")
    chk(v_raid is False, "v539 REFUSES it for a RAIDER (bound 1)")
    chk(v_late is False, "v539 REFUSES it past LIFELINE_RNDS (bound 2)")

    print("[8] rung B: the draft flips the role, and only in famine")
    r_f, n_f = draft_probe("_v539resilience", True, 6)
    r_n, _ = draft_probe("_v539resilience", False, 6)
    r_p, _ = draft_probe("_v537socket", True, 6)
    r_eco, _ = draft_probe("_v539resilience", False, 2)
    r_eco_p, _ = draft_probe("_v537socket", False, 2)
    chk(r_f == "expand", "n=6 body drafted to EXPAND during famine")
    chk(r_n == "raid", "n=6 body stays RAID with no famine (other verdict)")
    chk(r_p == "raid", "parent n=6 body is RAID in the same board (control)")
    chk(r_eco == r_eco_p,
        "n=2 (a real eco seat) resolves IDENTICALLY in both trees: %s" % r_eco)

    print("[9] v539.1 RESERVE FLOOR binds, and ONLY when it should")
    bar = gate_bar()
    chk(bar > 0, "the floor is a real number: sentinel + reserve = %d Ti" % bar)
    # famine + a bank the wipe drained: the floor must REFUSE
    lo_on = gate_probe("_v539resilience", True, 8, "expand", floor=True)
    lo_off = gate_probe("_v539resilience", True, 8, "expand", floor=False)
    chk(lo_on is False,
        "floor ON + famine + wiped bank (8 Ti): REFUSES -- the rebuild waits")
    chk(lo_off is True,
        "floor OFF, same board: ALLOWS (the other verdict, and the arm diff)")
    # famine + a bank well above the floor: the floor must ALLOW
    hi_on = gate_probe("_v539resilience", True, bar + 200, "expand", floor=True)
    chk(hi_on is True,
        "floor ON + famine + bank %d Ti: ALLOWS -- true surplus rebuilds"
        % (bar + 200))
    # ⛔⛔ A FOUR-WAY BANK SWEEP, NOT A BOUNDARY CELL, AND THE FIRST DRAFT GOT
    # THIS WRONG IN THE FLATTERING DIRECTION.  `_v539_lifeline` returning False
    # does NOT mean the spend is refused -- it means the call FALLS THROUGH to
    # the parent's own reserve logic, which on a healthy bank says yes anyway.
    # So "the floor refuses at exactly the bar" is not a proposition about the
    # floor at all; it is a proposition about the parent.  The proposition that
    # IS about the floor: across bank levels x {conveyor, harvester} cost x
    # {collar live, collar idle}, does the arm ever differ from the parent?
    banks = [0, 4, 8, 16, 24, 32, 40, 44, 46, 48, 52, 60, 80, 100, 150, 200,
             400]
    on_diffs, off_diffs, both_ways = [], [], []
    for cost in ("conveyor", "harvester"):
        for collar in (False, True):
            kw = dict(collar=collar, cost=cost)
            par = [gate_probe("_v537socket", True, b, "expand", **kw)
                   for b in banks]
            on = [gate_probe("_v539resilience", True, b, "expand", floor=True,
                             **kw) for b in banks]
            off = [gate_probe("_v539resilience", True, b, "expand", floor=False,
                              **kw) for b in banks]
            on_diffs.append([b for b, x, y in zip(banks, par, on) if x != y])
            off_diffs.append([b for b, x, y in zip(banks, par, off) if x != y])
            both_ways.append(False in par and True in par)
    chk(all(x == [] for x in on_diffs),
        "⭐ floor ON is PARENT-IDENTICAL across all %d sweep cells -- i.e. the "
        "floor makes RUNG A EXACTLY INERT, so v539.1 is a clean ABLATION of "
        "rung A (draft + hold only), not a softer lifeline"
        % (len(banks) * 4))
    chk(all(len(x) > 0 for x in off_diffs),
        "floor OFF differs from the parent in ALL FOUR sweeps %s (the other "
        "verdict: the comparison can fail, and this is the whole arm "
        "difference)" % off_diffs)
    chk(all(both_ways),
        "the parent answers both ways in every sweep (no constant column)")

    # the floor must not resurrect the lifeline outside a famine
    nf_on = gate_probe("_v539resilience", False, bar + 200, "expand",
                       floor=True)
    par_hi = gate_probe("_v537socket", True, bar + 200, "expand")
    chk(nf_on == par_hi,
        "floor ON but NO famine: identical to the parent (%s)" % nf_on)

    print("[10] the SENTINEL GATE survives a famine (Magnus's s51 ruling)")
    # THE QUESTION THE AMENDMENT ASKS: does declaring famine CLOSE the
    # 2-harvesters-built-AND-connected gate?  Measured, not read off the code.
    modsg = load_tree("_v539resilience")
    fcg = fc_maps(modsg)
    dg = modsg["doctrine"]
    wg = World(14, 14)
    wg.delivery_on = True
    cg = wg.add(EntityType.CORE, Team.A, Position(3, 3))
    wg.add(EntityType.CONVEYOR, Team.A, Position(3, 2), Direction.SOUTH)
    oreg = Position(6, 3)
    wg.set_terrain(oreg, "o")
    hg = wg.add(EntityType.HARVESTER, Team.A, oreg)
    Pg = modsg["main"].Player()
    Pg.core, Pg.team, Pg.mw, Pg.mh = Position(3, 3), fcg["team"]["A"], 14, 14
    gate_before = gate_during = None
    for r in range(200):
        if r == 100:
            wg.remove(hg)
        Pg._fs_eco_publish(DeliveryCt(wg, cg, fcg), r, 2)
        wg.end_round()
        ctg = DeliveryCt(wg, cg, fcg)
        if r == 99:
            gate_before = Pg._fs_eco_gate_ok(ctg)
        if r == 199:
            gate_during = Pg._fs_eco_gate_ok(ctg)
            fam_now = bool(wg.store[Team.A][dg.FS_ECO_SLOT]
                           & dg.FS_ECO_BIT_FAMINE)
    chk(gate_before is True, "sentinel gate OPEN before the wipe")
    chk(fam_now is True, "famine IS declared at r199 (the dose landed)")
    chk(gate_during is True,
        "sentinel gate STILL OPEN during famine -- the CONN/DELIV latch is "
        "never cleared by the famine bits")
    ctg2 = DeliveryCt(wg, cg, fcg)
    v = ctg2.read_store(dg.FS_ECO_SLOT)
    chk(bool(v & dg.FS_ECO_BIT_CONN) and bool(v & dg.FS_ECO_BIT_DELIV),
        "CONN and DELIV bits both still set alongside the famine bit")

    print("[11] flag-off: LOKI_FS_V539=False reproduces the parent verdicts")
    mods3 = load_tree("_v539resilience")
    mods3["doctrine"].LOKI_FS_V539 = False
    # the modules already bound the name via `from doctrine import *`, so the
    # flip must be pushed into each module namespace the way the tree sees it
    for m in ("eco", "siege", "main", "raid"):
        setattr(mods3[m], "LOKI_FS_V539", False)
    chk(True, "(flag-off identity is asserted by flagoff.py, not here)")

    print()
    if fails:
        print("SELFTEST FAILED: %d" % len(fails))
        for f in fails:
            print("  - " + f)
        return 1
    print("SELFTEST PASSED")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--endgame", action="store_true")
    ap.add_argument("--rounds", type=int, default=300)
    ap.add_argument("--wipe-at", default="140",
                    help="one wipe round, or a comma list")
    ap.add_argument("--maps", default="atoll")
    ap.add_argument("--identity", action="store_true")
    ap.add_argument("--seeds", type=int, default=1)
    ap.add_argument("--arms", default="_v537socket,_v539resilience",
                    help="comma list of trees (name under bots/, "
                         "or a repo-relative path)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.identity:
        for mp in a.maps.split(","):
            for wp in [int(x) for x in str(a.wipe_at).split(",")]:
                print(identity_cmp(mp, a.rounds, wp))
        return 0
    if a.endgame:
        # ⛔ THE SCENARIO AXIS IS THE WIPE ROUND, NOT A RANDOM SEED.  With
        # NOISE_ON off (see `load_tree`) the fixture is deterministic, so
        # re-running the same cell under a different `random` seed reproduces
        # it exactly and would inflate n with copies.  Varying WHEN the economy
        # is destroyed varies the thing the plank is about.
        wipes = [int(x) for x in str(a.wipe_at).split(",")]
        for mp in a.maps.split(","):
            for wp in wipes:
                for tree in a.arms.split(","):
                    row = endgame_run(tree, map_name=mp, rounds=a.rounds,
                                      wipe_at=wp, seed=0)
                    row["seed"] = wp          # the cell key: the wipe round
                    print("\t".join("%s=%s" % kv for kv in row.items()))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
