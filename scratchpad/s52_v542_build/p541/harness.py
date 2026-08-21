#!/usr/bin/env python3
"""v541 INSTRUMENT #2 -- THE CARVE-OUT HARNESS (no game engine, no fcode).

⛔ WHY A FAKE ENGINE, AND WHAT IT MAY NOT BE USED FOR.
The local box is running V537POOL and this build is under a HARD ZERO-fcode-run
constraint until `scratchpad/overnight/V537POOL.tsv` reaches 5400 data rows
(2,383 at build time, `date -u` 2026-08-21T07:52Z).  So every MECHANISM claim
is made here, on `tools/stub_engine.py`'s fake Controller, by importing the
REAL trees and calling the REAL methods -- there is no reimplementation of any
predicate in this file.  Every claim about PLAY, TEMPO, KILL ROUND or OUTCOME
is made on the ws1 battery or is DEFERRED and named as deferred.

DIVERGENCES FROM THE ENGINE, stated because they bound the claims:
  * the stub CORE occupies ONE tile, not 2x2.  `core_tiles(o)` returns
    `[o, o+(1,0), o+(0,1), o+(1,1)]` and only `o` carries the entity, so every
    probe here stands the body at `o+(-1,0)` -- Manhattan 1 from `o`, which is
    the first element of that list, so the real target-selection loop picks the
    tile that really holds the core.  A body standing off the anchor would see
    `can_fire` refuse on an empty tile: that is a STUB artefact, and it is why
    the geometry probe below is the ONE probe whose negative case is asserted
    against the real `adjacent_to_core` rather than against `can_fire`.
  * no opponent acts, nothing heals, no resource physics.  So this file can say
    "the verb fires and the core loses 2 HP"; it CANNOT say "the core dies".

WHAT IT ANSWERS, and it is exactly one class of question:
  D  DOSE, BOTH WAYS -- does `_v541_core_attack` fire, and does the enemy core
     lose HP, with the flag ON; and is it 0 with the flag OFF?  The field
     baseline for this quantity is ZERO in 25 of 25 rated games
     (FIELD-DEBUT-v174-2026-08-21 §5.3), so nonzero-on/zero-off IS the dose.
  G  EVERY GATE DRIVEN TO BOTH VERDICTS -- adjacency, cooldown, funding
     (collar reserve AND sentinel reserve, separately), per-body budget, the
     NEED_SENTINEL variant, and the master.
  H  THE HARM CHECK.  LOKI-QUIET's measured harm is ROUNDS TAKEN FROM
     MOVEMENT, and `_v178salt` resurrected it once (kill round r179 vs a pooled
     r129, p=0.008).  `_v541_idle_ok` claims to reproduce `_fs_walk`'s own
     decision.  So this drives the PARENT's `_fs_walk` and the CHILD's
     `_v541_idle_ok` over the SAME boards and asserts they agree on every one:
     idle_ok True exactly where _fs_walk moves nothing.  ⭐ THAT AGREEMENT IS
     THE HARM CHECK -- not an assertion that the harm is absent, a measurement
     that no round the parent spent walking is available to the new verb.

    .venv/bin/python scratchpad/s52_v541_build/harness.py --selftest
    .venv/bin/python scratchpad/s52_v541_build/harness.py --report
"""
import argparse
import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

from tools.stub_engine import (  # noqa: E402
    World, StubController, Position, Direction, EntityType, Team,
)

MODNAMES = ("doctrine", "eco", "siege", "raid", "main")
CHILD = "bots/_v542wave"
PARENT = "bots/_v537socket"


def load_tree(tree, noise=False):
    """Import a bot tree's modules FRESH.  Copied verbatim in behaviour from
    `scratchpad/s52_v539_build/harness.py:load_tree` -- including NOISE OFF,
    which is not cosmetic: `main.py` seeds a per-body `spawn_salt` from an
    unseeded `random.Random()` that `random.seed()` cannot reach, so with noise
    ON the SAME TREE run TWICE IN ONE PROCESS diverges."""
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


def setflag(mods, name, value):
    """Poke a doctrine flag into EVERY module namespace.

    ⛔ NOT JUST `doctrine`.  The tree does `from doctrine import *`, so each
    module holds its OWN binding of every flag; setting it on `doctrine` alone
    changes nothing that siege.py or raid.py reads.  This is `load_tree`'s
    noise-off pattern applied to an arbitrary flag, and getting it wrong is a
    silent no-op that would make every flag-off case pass for free."""
    for m in MODNAMES:
        setattr(mods[m], name, value)


def fc_maps(mods):
    """Translation tables from the stub's bare strings to real fcode enums."""
    import fcode as fcm
    return {
        "team": {t.value: t for t in fcm.Team} | {"A": fcm.Team.A,
                                                  "B": fcm.Team.B},
        "etype": {e.value: e for e in fcm.EntityType},
        "env": {e.value: e for e in fcm.Environment},
        "dir": {d.value: d for d in fcm.Direction},
        "pos": fcm.Position,
    }


class Ct(StubController):
    """StubController with the fcode type shims the real bot code needs.

    The bot compares against REAL fcode enum members (it does
    `from fcode import EntityType, ...`), while the stub stores bare strings.
    Without these five overrides every `get_entity_type(x) == EntityType.CORE`
    in the tree is silently False -- which would make every probe here read
    "did not fire" for a reason that has nothing to do with the plank."""

    def __init__(self, world, eid, fc):
        super().__init__(world, eid)
        self.fc = fc

    def get_team(self, id=None):
        return self.fc["team"][super().get_team(id)]

    def get_entity_type(self, id=None):
        return self.fc["etype"][super().get_entity_type(id)]

    def get_tile_env(self, pos):
        return self.fc["env"][super().get_tile_env(pos)]

    def get_direction(self, id=None):
        return self.fc["dir"][super().get_direction(id)]

    def get_position(self, id=None):
        p = super().get_position(id)
        return self.fc["pos"](p.x, p.y)


# ---------------------------------------------------------------------------
# the board every probe uses
# ---------------------------------------------------------------------------

W, H = 20, 20
OURC = Position(2, 2)
ENEC = Position(14, 14)          # enemy core ANCHOR; core_tiles()[0] == this


def board(mods, ti=500, sentinel=False, enemy_belt=False, ammo=10**6,
          core_hp=100):
    """A 20x20 board: our core NW, THEIR core at ENEC, one of our builders
    standing orthogonally WEST of their core anchor -- i.e. ARRIVED."""
    w = World(W, H)
    w.add(EntityType.CORE, Team.A, OURC)
    w.add(EntityType.CORE, Team.B, ENEC)
    bot = w.add(EntityType.BUILDER_BOT, Team.A,
                Position(ENEC.x - 1, ENEC.y))
    if sentinel:
        # one of OUR forward sentinels, alive and in the body's vision
        w.add(EntityType.SENTINEL, Team.A, Position(ENEC.x - 3, ENEC.y),
              Direction.EAST)
    if enemy_belt:
        # an ENEMY conveyor orthogonally adjacent to the body -- the control
        # that proves the verb targets the CORE and nothing else
        w.add(EntityType.CONVEYOR, Team.B, Position(ENEC.x - 1, ENEC.y - 1),
              Direction.SOUTH)
    if core_hp is not None:
        # ⚠ SET THE ENEMY CORE'S HP DIRECTLY.  The finisher clause reads it
        # through `get_tile_building_id` -> `get_hp`, so this is the input
        # that guard actually consumes; nothing else on the board changes.
        for e in w.entities.values():
            if e["team"] == Team.B and e["type"] == EntityType.CORE:
                e["hp"] = core_hp
    w.titanium[Team.A] = ti
    # ⚠ AMMO DEFAULTS TO EFFECTIVELY INFINITE so that every probe ABOVE the
    # ammunition clause reads the guard it is actually aiming at.  The clause
    # only bites when a sentinel is alive AND the magazine is short, so a
    # default of 0 would have silently refused half the fixture for the wrong
    # reason -- which is how a guard gets "verified" by a board it never saw.
    w.ammo[Team.A] = ammo
    return w, bot


def player(mods, fc, role="raid"):
    """⛔ `P.team` MUST BE THE **fcode** Team, NOT THE STUB'S.

    Caught by this file's own selftest, and it is the exact failure mode the
    "instrument driven both ways" rule exists for: the tree compares
    `ct.get_team(bid) != self.team`, `ct.get_team` is shimmed to return a real
    fcode enum, and the stub's `Team.A` is a different object -- so EVERY
    friendly entity read as hostile and `_fs_live_sentinels` returned 0 on a
    board with a live sentinel standing on it.  Two selftest cases failed and
    named it.  Had those two cases not existed, the sentinel-reserve guard
    would have "passed" while never once seeing a sentinel."""
    P = mods["main"].Player()
    P.core = fc["pos"](OURC.x, OURC.y)
    P.team = fc["team"][Team.A]
    P.mw, P.mh = W, H
    P.role = role
    return P


def core_hp(w):
    for eid, e in w.entities.items():
        if e["team"] == Team.B and e["type"] == EntityType.CORE:
            return e["hp"]
    return None


def probe_attack(tree, clause="idlepeck", **kw):
    """Call ONE of the REAL v541 clauses once and report what happened.

    `clause` selects which:
      "corefirst" -> `_v541_corefirst`, the SHIPPED redirect (build reserve
                     only; no ammunition clause -- the titanium is going to a
                     conveyor either way in the state it fires in);
      "idlepeck"  -> `_v541_core_attack`, the ADDITIVE clause (full reserve).
    ⚠ The two are probed SEPARATELY on purpose.  They have different funding
    gates and different justifications, and a single probe that ran "whichever
    fires" would let one clause's pass certify the other's guard.

    Returns (fired, core_hp_delta, ti_delta, pecks).  `needed` is the collar
    list the ring ladder would pass; an empty list is "collar closed", which is
    the cheapest funding state and the one the arrived body is usually in.
    """
    flags = dict(kw.pop("flags", {}))
    needed = kw.pop("needed", [])
    cd = kw.pop("cooldown", 0)
    at = kw.pop("at", None)
    pecks = kw.pop("pecks", 0)
    # the additive clause ships OFF; a probe of it must switch it on, or every
    # case would read "did not fire" for the wrong reason.
    if clause == "idlepeck":
        flags.setdefault("FS_V541_IDLEPECK", True)
    mods = load_tree(tree)
    for k, v in flags.items():
        setflag(mods, k, v)
    fc = fc_maps(mods)
    w, bot = board(mods, **kw)
    if at is not None:
        w.entities[bot]["pos"] = at
    w.entities[bot]["action_cd"] = cd
    P = player(mods, fc)
    P.v541_pecks = pecks
    ct = Ct(w, bot, fc)
    hp0, ti0 = core_hp(w), w.titanium[Team.A]
    E = fc["pos"](ENEC.x, ENEC.y)
    if clause == "corefirst":
        fired = P._v541_corefirst(ct, E, ct.get_position())
    else:
        fired = P._v541_core_attack(ct, E, ct.get_position(), needed)
    return (bool(fired), core_hp(w) - hp0, w.titanium[Team.A] - ti0,
            P.v541_pecks)


# ---------------------------------------------------------------------------
# H -- the harm check: idle_ok agrees with the PARENT's walker, board for board
# ---------------------------------------------------------------------------

def harm_boards(mods, fc):
    """States that differ in whether the parent's `_fs_walk` would MOVE.

    Each entry: (label, needed, move_cd, bot_offset).  `needed` non-empty with
    the body away from any adjacent stand tile is the case where the parent
    WALKS -- the round the new verb must not be allowed to take.
    """
    n1 = [fc["pos"](ENEC.x, ENEC.y - 1)]          # one collar seat still owed
    n2 = [fc["pos"](ENEC.x + 4, ENEC.y + 4)]      # a seat far from the body
    return [
        ("collar closed, body parked",      [], 0, (-1, 0)),
        ("collar closed, move on cooldown", [], 3, (-1, 0)),
        ("seat owed, body already beside it", n1, 0, (-1, -1)),
        ("seat owed FAR AWAY, body free to walk", n2, 0, (-1, 0)),
        ("seat owed far, but move on cooldown", n2, 3, (-1, 0)),
    ]


def harm_check(verbose=True):
    """⭐ THE HARM CHECK.  For each board, ask the CHILD's `_v541_idle_ok`
    whether the round is free, and ask the PARENT's own `_fs_walk` whether it
    would have moved.  They must never both say yes.

    The parent's answer is measured, not modelled: we run `_fs_walk` on the
    parent tree and compare the body's position before and after.
    """
    rows = []
    pm = load_tree(PARENT)
    pfc = fc_maps(pm)
    cm = load_tree(CHILD)
    cfc = fc_maps(cm)
    for label, needed, mcd, off in harm_boards(cm, cfc):
        # --- parent: would _fs_walk have moved the body?
        w, bot = board(pm)
        w.entities[bot]["pos"] = Position(ENEC.x + off[0], ENEC.y + off[1])
        w.entities[bot]["move_cd"] = mcd
        P = player(pm, pfc)
        ct = Ct(w, bot, pfc)
        before = (ct.get_position().x, ct.get_position().y)
        try:
            P._fs_walk(ct, pfc["pos"](ENEC.x, ENEC.y), ct.get_position(),
                       [pfc["pos"](t.x, t.y) for t in needed])
        except Exception:
            pass
        after = (w.entities[bot]["pos"].x, w.entities[bot]["pos"].y)
        parent_moved = before != after
        # --- child: does the idle gate open?
        w2, bot2 = board(cm)
        w2.entities[bot2]["pos"] = Position(ENEC.x + off[0], ENEC.y + off[1])
        w2.entities[bot2]["move_cd"] = mcd
        P2 = player(cm, cfc)
        ct2 = Ct(w2, bot2, cfc)
        try:
            idle = bool(P2._v541_idle_ok(
                ct2, cfc["pos"](ENEC.x, ENEC.y), ct2.get_position(),
                [cfc["pos"](t.x, t.y) for t in needed]))
        except Exception:
            idle = False
        rows.append((label, parent_moved, idle))
        if verbose:
            bad = parent_moved and idle
            print(f"  {'CONFLICT' if bad else 'ok      '}  {label:42s}"
                  f"  parent_moves={parent_moved!s:5s}  idle_ok={idle!s:5s}")
    return rows


# ---------------------------------------------------------------------------
# SELFTEST -- every guard driven to BOTH verdicts
# ---------------------------------------------------------------------------

def selftest():
    fails = []

    def chk(cond, msg):
        print(("  ok    " if cond else "  FAIL  ") + msg)
        if not cond:
            fails.append(msg)

    print("[D] DOSE, BOTH WAYS -- the quantity the field measures at ZERO")
    f, dhp, dti, n = probe_attack(CHILD)
    chk(f and dhp == -2 and dti == -2 and n == 1,
        f"flag ON: fired={f} core_hp={dhp} ti={dti} pecks={n} "
        "(expect fired, -2 HP, -2 Ti, 1)")
    f0, dhp0, dti0, n0 = probe_attack(CHILD,
                                      flags={"FS_V541_COREPECK": False})
    chk((not f0) and dhp0 == 0 and dti0 == 0 and n0 == 0,
        f"flag OFF: fired={f0} core_hp={dhp0} ti={dti0} pecks={n0} "
        "(expect the other verdict -- nothing at all)")
    chk(not hasattr(load_tree(PARENT)["main"].Player(), "_v541_corefirst"),
        "COUNTER-CONTROL: the PARENT tree has no such method at all")

    print("[G1] GEOMETRY -- orthogonally adjacent to the enemy core, or not")
    f, dhp, _, _ = probe_attack(CHILD, at=Position(ENEC.x - 4, ENEC.y))
    chk((not f) and dhp == 0, "four tiles away: refuses (the other verdict)")
    f, dhp, _, _ = probe_attack(CHILD, at=Position(ENEC.x - 1, ENEC.y - 1))
    chk((not f) and dhp == 0,
        "DIAGONAL to the anchor: refuses -- the verb needs orthogonal "
        "adjacency, and d^2<=2 arrival does not imply it")

    print("[G2] ACTION COOLDOWN")
    f, _, _, _ = probe_attack(CHILD, cooldown=0)
    chk(f, "cooldown 0: fires")
    f, dhp, _, _ = probe_attack(CHILD, cooldown=2)
    chk((not f) and dhp == 0, "cooldown 2: refuses (the other verdict)")

    print("[G3] FUNDING -- the collar reserve, and it is not the bare floor")
    seat = Position(ENEC.x, ENEC.y - 1)
    f, _, _, _ = probe_attack(CHILD, ti=500, needed=[seat] * 8)
    chk(f, "8 seats owed but a 500 bank: fires (surplus exists)")
    f, dhp, _, _ = probe_attack(CHILD, ti=20, needed=[seat] * 8)
    chk((not f) and dhp == 0,
        "8 seats owed and a 20 bank: refuses (the other verdict) -- "
        "the collar's money is senior")

    print("[G4] FUNDING -- the SENTINEL reserve, separately")
    f, _, _, _ = probe_attack(CHILD, ti=20, sentinel=True)
    chk(f, "20 Ti WITH a live forward sentinel: fires "
           "(no sentinel left to reserve for)")
    f, dhp, _, _ = probe_attack(CHILD, ti=20, sentinel=False)
    chk((not f) and dhp == 0,
        "20 Ti with NO sentinel: refuses (the other verdict) -- "
        "a sentinel's price is reserved ahead of the peck")
    f, _, _, _ = probe_attack(CHILD, ti=20, sentinel=False,
                              flags={"FS_V541_KEEP_SENT": False})
    chk(f, "same board, KEEP_SENT off: fires -- proving the refusal above "
           "came from THAT reserve and not from something else")

    print("[G5] PER-BODY BUDGET")
    f, _, _, n = probe_attack(CHILD, pecks=0)
    chk(f and n == 1, "budget 0/60 spent: fires and increments")
    f, dhp, _, n = probe_attack(CHILD, pecks=60)
    chk((not f) and dhp == 0 and n == 60,
        "budget 60/60 spent: refuses (the other verdict)")

    print("[G6] THE NEED_SENTINEL VARIANT (ships OFF)")
    f, _, _, _ = probe_attack(CHILD, sentinel=False,
                              flags={"FS_V541_NEED_SENTINEL": True})
    chk(not f, "variant ON, no sentinel alive: refuses")
    f, _, _, _ = probe_attack(CHILD, sentinel=True,
                              flags={"FS_V541_NEED_SENTINEL": True})
    chk(f, "variant ON, sentinel alive: fires (the other verdict)")
    f, _, _, _ = probe_attack(CHILD, sentinel=False)
    chk(f, "variant OFF (shipped): fires with no sentinel -- which is the "
           "arr2->first-sentinel gap this build exists to fill")

    print("[R] THE SHIPPED CLAUSE -- COREFIRST, the redirect")
    f, dhp, dti, n = probe_attack(CHILD, clause="corefirst")
    chk(f and dhp == -2 and dti == -2 and n == 1,
        f"fires at core adjacency: fired={f} core_hp={dhp} ti={dti} n={n}")
    f, dhp, _, _ = probe_attack(CHILD, clause="corefirst",
                                flags={"FS_V541_COREFIRST": False})
    chk((not f) and dhp == 0,
        "FS_V541_COREFIRST=False: refuses (the other verdict)")
    f, dhp, _, _ = probe_attack(CHILD, clause="corefirst",
                                flags={"FS_V541_COREPECK": False})
    chk((not f) and dhp == 0, "master off: refuses (the other verdict)")
    f, dhp, _, _ = probe_attack(CHILD, clause="corefirst",
                                at=Position(ENEC.x - 1, ENEC.y - 1),
                                enemy_belt=True)
    chk((not f) and dhp == 0,
        "⭐ SCOPE: body adjacent to an enemy CONVEYOR but NOT to the core -- "
        "refuses, so the salt verb keeps every tile except their 8 sockets")

    print("[F] THE FINISHER CONDITION -- the clause the ws1 battery forced")
    f, _, _, _ = probe_attack(CHILD, clause="corefirst", core_hp=100)
    chk(f, "core at 100 HP (<= the 120 budget): redirect fires")
    f, dhp, _, _ = probe_attack(CHILD, clause="corefirst", core_hp=500)
    chk((not f) and dhp == 0,
        "⭐ core at FULL 500 HP: REFUSES (the other verdict) -- and this is "
        "the whole finding: the unconditional form lost 18 timely kills of "
        "180 with 0 gained, because a 2-damage peck FINISHES a 20 HP belt "
        "and never finishes a healed core")
    f, _, _, _ = probe_attack(CHILD, clause="corefirst", core_hp=500,
                              flags={"FS_V541_FINISH_ON": False})
    chk(f, "same board, FINISH_ON off: fires -- proving the refusal came "
           "from THAT clause (and reproducing the refuted arm exactly)")
    f, dhp, _, _ = probe_attack(CHILD, clause="corefirst", core_hp=100,
                                pecks=60)
    chk((not f) and dhp == 0,
        "core at 100 HP but the body's budget is SPENT: refuses -- the cap "
        "is min(FINISH_HP, 2 x remaining budget), so a spent body stops "
        "claiming it can finish")
    f, _, _, _ = probe_attack(CHILD, clause="corefirst", core_hp=120)
    chk(f, "boundary: exactly 120 HP is finishable")
    f, _, _, _ = probe_attack(CHILD, clause="corefirst", core_hp=121)
    chk(not f, "boundary: 121 HP is not (the other side of the same edge)")

    print("[A] THE AMMUNITION CLAUSE -- and the two clauses differ on it")
    #   the state it governs: a live sentinel, an EMPTY magazine, cheap board
    ammo_state = dict(sentinel=True, ammo=0, ti=500)
    f, _, _, _ = probe_attack(CHILD, clause="idlepeck", **ammo_state)
    chk(not f,
        "ADDITIVE clause with a live sentinel and an empty magazine: REFUSES "
        "-- 2 Ti as ammunition is 1.80 HP/Ti against the peck's 1.00")
    f, _, _, _ = probe_attack(CHILD, clause="idlepeck",
                              flags={"FS_V541_AMMO_AWARE": False},
                              **ammo_state)
    chk(f, "same board, AMMO_AWARE off: fires -- proving the refusal above "
           "came from THAT clause and not from the sentinel reserve")
    f, _, _, _ = probe_attack(CHILD, clause="idlepeck", sentinel=True,
                              ammo=10 ** 6, ti=500)
    chk(f, "magazine FULL: fires (the other verdict) -- surplus is surplus")
    f, _, _, _ = probe_attack(CHILD, clause="idlepeck", sentinel=False,
                              ammo=0, ti=500)
    chk(f, "NO live sentinel, empty magazine: fires -- nothing to starve, "
           "and this is the arr2->first-sentinel gap")
    f, _, _, _ = probe_attack(CHILD, clause="corefirst", **ammo_state)
    chk(f, "⭐ THE ASYMMETRY: the REDIRECT fires on the SAME board the "
           "additive clause refused -- there the 2 Ti goes to a conveyor "
           "either way, so the ammunition premise is false")

    print("[G7] TARGET DISCIPLINE -- the enemy CORE and nothing else")
    f, dhp, _, _ = probe_attack(CHILD, at=Position(ENEC.x - 1, ENEC.y - 2),
                                enemy_belt=True)
    chk(not f,
        "body orthogonally adjacent to an ENEMY CONVEYOR but not to the core: "
        "refuses -- demolition lowers their cost scale and is a gift")

    print("[H] THE HARM CHECK -- idle_ok never opens a round the parent walks")
    rows = harm_check()
    conflicts = [r for r in rows if r[1] and r[2]]
    chk(not conflicts, f"0 conflicts over {len(rows)} boards "
                       f"(found {len(conflicts)})")
    chk(any(r[1] for r in rows),
        "POSITIVE CONTROL: at least one board DOES make the parent walk "
        "-- otherwise 'no conflict' is vacuous")
    chk(any(r[2] for r in rows),
        "POSITIVE CONTROL: at least one board DOES open the idle gate "
        "-- otherwise 'no conflict' is vacuous the other way")

    print()
    if fails:
        print(f"SELFTEST FAILED: {len(fails)}")
        for f_ in fails:
            print("  - " + f_)
        return 1
    print("SELFTEST PASSED")
    return 0


def report():
    print("v541 CARVE-OUT HARNESS -- mechanism report (stub engine)")
    print()
    print("DOSE (per single call, arrived body, collar closed, 500 bank):")
    for label, flags in (("FS_V541_COREPECK=True  (shipped)", {}),
                         ("FS_V541_COREPECK=False (parent)",
                          {"FS_V541_COREPECK": False})):
        f, dhp, dti, n = probe_attack(CHILD, flags=flags)
        print(f"  {label:32s} fired={f!s:5s} core_hp={dhp:+d} "
              f"ti={dti:+d} pecks={n}")
    print()
    print("HARM CHECK (parent's own _fs_walk vs the child's idle gate):")
    harm_check()
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.report:
        return report()
    ap.error("give --selftest or --report")


if __name__ == "__main__":
    sys.exit(main())
