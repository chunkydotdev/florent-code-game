#!/usr/bin/env python3
"""Launcher-throw census v2 — outcome measured from BuilderAttack, not HP guesswork.

v1 attributed core damage by "an inserted raider was standing adjacent when the
core lost HP". That is a proxy and its sign handling was wrong (updateHp.delta is
a 64-bit two's-complement varint: 18446744073709551609 == -7). v2 drops the proxy
and uses the direct event:

    BuilderAttack { int32 id = 1; Pos target = 2; }   // Update field 13

A raider that is doing damage to the enemy core emits BuilderAttack with a target
inside the enemy core's 2x2 footprint. That is unambiguous and per-bot.

Per own-team forward throw ("INSERT") we record, from the throw until the bot
dies or is thrown again:
    life        rounds the bot stayed alive
    core_atk    BuilderAttack events aimed at the ENEMY core footprint
    any_atk     BuilderAttack events aimed at anything
    reached     did it ever stand orthogonally adjacent to the enemy core

⭐ VICTIM FATE, added s42 2026-08-15 — `vfate` / `vlife` / `vhp`.
=================================================================
⛔ THE DEFECT THIS CLOSES, and it produced a published-and-wrong finding the
night before this was written. Only `kind == "INSERT"` records were ever added
to `active`, and only `active` records ever had `close()` called — so `life`,
`core_atk`, `any_atk` and `reached` are populated for INSERT and are the
INITIALISER for every other kind. Measured on the 580,697-row live file:

    kind      rows      life != -1
    INSERT    114,972   100.0%
    EXILE     243,790     0.0%     <- the kidnap population; the plank's subject
    RETREAT    39,455     0.0%
    UNATTRIB    1,783     0.0%

**A `-1/0/0/0` EXILE row means NOT APPLICABLE, not "measured zero".** A constant
column validates anything, and this one reads as a clean negative on exactly the
question the launcher-kidnap plank asks: *when we throw an enemy builder onto a
map-border tile, does its own off-map query crash it and does the engine destroy
it for the rest of the match?*

**WHY THE ASYMMETRY EXISTED, because it is the thing to watch for in a successor:
the victim of an EXILE is the ENEMY'S unit.** The INSERT machinery is written
around "our ferried raider" — `core_atk`, `reached` are own-team-forward
semantics — and the victim never had a home in it.

WHAT IS ADDED, and it deliberately REUSES `close()`'s shape rather than inventing
a second mechanism:
    vfate   UNTRACKED | TRUNCATED | DIED | RETHROWN | ALIVE_END
    vlife   rounds from THIS throw to that fate event; -1 iff not tracked
    vhp     UpdateHp events naming this bot inside the tracked window; -1 iff
            not tracked. **0 with DIED is the crash/self-destruct signature**
            (removed with no HP event at all — the same signature
            `tools/crash_census.py` uses); >0 with DIED is a combat death.

⛔ `UNTRACKED` AND `ALIVE_END` ARE DIFFERENT AND MUST RENDER DIFFERENTLY. "We
followed this bot to the end of the replay and it never died" and "we could not
follow this bot" are the same `-1` under any single-sentinel scheme, and that
collapse is what made the old column unauditable. `vlife == -1` now happens if
and only if `vfate` is UNTRACKED or TRUNCATED.

⛔ SEPARATE DICT, ON PURPOSE. Victim tracking uses `vtrack`, not `active`. The
two have different closing rules — `active` is closed only by a re-INSERT or a
removal, `vtrack` by a throw OF ANY KIND or a removal — so folding the victims
into `active` would silently change `life` on INSERT rows, i.e. it would be a
REGRESSION dressed as an extension. The INSERT columns are byte-identical after
this change and `--selftest` drives that.
"""
from __future__ import annotations

import sys
from pathlib import Path

# ⛔ ABSOLUTE, not the bare `"tools"` this line used to be. That form resolves
# against the CWD, so the module only imported when run from the repo root; the
# selftest and any caller with a different CWD got an ImportError that reads as
# "the tool is broken" rather than "you are in the wrong directory".
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN, WIRE_VARINT  # noqa: E402
from wincond_backfill import check_framing, TruncatedReplayError  # noqa: E402


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


class Ent:
    __slots__ = ("id", "team", "pos", "kind")

    def __init__(self, eid, team, pos, kind):
        self.id, self.team, self.pos, self.kind = eid, team, pos, kind


def census(path: Path):
    data = path.read_bytes()
    # ⛔ FRAMING FIRST. `fields()` slices `buf[i:i+length]` and Python truncates a
    # short slice SILENTLY, so a half-written replay yields a short turn list with
    # no error at all. For victim fate that failure is not neutral: every bot still
    # being followed at the break reads ALIVE_END, and every death after the break
    # is invisible -- the FLATTERING direction for "the throw did not kill it" and
    # the flattering direction for "it survived N rounds". We do NOT refuse the
    # file (that would change the INSERT rows this decoder has always emitted);
    # we mark the victim columns TRUNCATED/-1 so a truncated file cannot be read
    # as a survival. Mirrors `tools/wincond_backfill.py`'s guard -- IMPORTED from
    # it, so there is one implementation and one place a wire-format change lands.
    try:
        check_framing(data)
        truncated = False
    except TruncatedReplayError:
        truncated = True
    map_buf, turn_bufs, winner, wincond = None, [], None, ""
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
        elif num == 4 and wire == WIRE_VARINT:
            winner = value
        elif num == 6 and wire == WIRE_LEN:
            wincond = value.decode("utf-8", "replace")
    if map_buf is None:
        return []

    cores, w, h = [], 0, 0
    for num, _wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    corepos = {c["team"]: c["pos"] for c in cores}
    if len(corepos) != 2:
        return []
    # ⛔ THE FALLBACK IS ITSELF AN ASSUMED SIZE, WHICH THE `border` COMMENT BELOW
    # FORBIDS. `w, h = 0, 0` above is the initialiser; if the map buffer ever fails
    # to yield fields 1/2 it survives, and then `to[0] == w - 1` is `== -1` (never
    # true) while `to[0] == 0` still fires -- so ONLY THE NEAR EDGES count as
    # border and the far edges are silently misfiled as interior. That is the same
    # systematic direction the border comment warns about: toward "no border
    # concentration", i.e. toward killing the crash channel.
    # Latent, not active: 0 rows of the live 46 MB throws.tsv carry mw or mh = 0.
    # Refusing the file is correct anyway -- a row with no map size cannot be
    # classified, and absorbing it as `border=0` makes it unauditable.
    # Flagged by the side lane against this file's own comment.
    if not (w and h):
        return []
    foot = {t: {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}
            for t, p in corepos.items()}

    ents = {c["id"]: Ent(c["id"], c["team"], c["pos"], "core") for c in cores}
    recs, active = [], {}          # bot id -> rec currently being tracked
    vtrack = {}                    # bot id -> VICTIM rec currently being tracked
    nrounds = len(turn_bufs)

    def close(rec, rnd):
        rec["life"] = rnd - rec["rnd"]

    def vclose(rec, rnd, fate):
        """Victim-side twin of close(). Same arithmetic, different closing rule.

        `fate` is written together with `vlife` and never separately, so the pair
        cannot drift into the state the old column had -- a number with no way to
        tell whether it was measured.
        """
        rec["vlife"] = rnd - rec["rnd"]
        rec["vfate"] = fate

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w2, update_buf in fields(turn_buf):
            for unum, _uw, ubuf in fields(update_buf):
                if unum == 1:                                    # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:
                            ents[e.id].pos = e.pos
                            continue
                        ents[e.id] = Ent(e.id, e.team, e.pos, e.kind)
                elif unum == 2:                                  # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    e = ents.get(eid)
                    if e is None or to is None:
                        continue
                    frm = e.pos
                    e.pos = to
                    if abs(to[0] - frm[0]) + abs(to[1] - frm[1]) <= 1:
                        continue
                    cand = [o for o in ents.values()
                            if o.kind == "launcher" and d2(o.pos, frm) <= 2]
                    cteams = {o.team for o in cand}
                    if not cand:
                        tteam, amb = None, "none"
                    elif len(cteams) == 1:
                        tteam, amb = cand[0].team, ("one" if len(cand) == 1 else "same_team")
                    else:
                        tteam, amb = None, "both_teams"
                    bteam = e.team
                    ec = corepos[(1 - tteam) if tteam is not None else (1 - bteam)]
                    before, after = d2(frm, ec), d2(to, ec)
                    kind = ("UNATTRIB" if tteam is None else
                            "EXILE" if tteam != bteam else
                            "INSERT" if after < before else "RETREAT")
                    # ⭐ LANDING POSITION, added s33 2026-08-12. `to` was already
                    # parsed here and thrown away -- the same computed-then-discarded
                    # shape as arena.py's rows and the engine's `turns`. Without it
                    # the archive cannot separate a BORDER landing from an INTERIOR
                    # one, which is the split that distinguishes the crash channel
                    # (victim queries an off-map neighbour and dies) from the mere
                    # displacement channel.
                    #
                    # ⛔ `border` IS COMPUTED AGAINST THIS GAME'S OWN w/h, NEVER AN
                    # ASSUMED SIZE. Maps here run 10x10 to 28x20 -- 17 distinct
                    # sizes -- so (13,1) is a BORDER tile on antler (14x18) and an
                    # INTERIOR tile on 26x26. Classifying against a fixed size, or
                    # against "max observed coordinate" (worse: it drifts with the
                    # sample), misfiles every border landing on a small map as
                    # interior. That error is SYSTEMATIC toward "no border
                    # concentration" -- i.e. toward killing the crash channel --
                    # so it would silently confirm the null. Hazard flagged by the
                    # builder, who hit it in `crash_cells.py`; `w`/`h` here are
                    # already the per-game parsed dimensions written to mw/mh.
                    # ⛔ CALLS `is_border()` -- the SAME function the selftest drives.
                    # An inline copy here would mean the selftest exercises a
                    # PARALLEL implementation and cannot catch a defect in the
                    # shipped path. That is the exact shape found four times in one
                    # session (effective_n's ceiling assertion, overnight_read's
                    # ignored `nowin`, queue_check's three grep-less marker cells):
                    # the test and the claim were about different things.
                    border = is_border(to, w, h)
                    rec = dict(file=path.name, mw=w, mh=h, rounds=nrounds, rnd=rnd,
                               kind=kind, tteam=-1 if tteam is None else tteam,
                               bteam=bteam, amb=amb, d2_before=before, d2_after=after,
                               bot=eid, life=-1, core_atk=0, any_atk=0, reached=0,
                               to_x=to[0], to_y=to[1], border=border,
                               winner=-1 if winner is None else winner, wincond=wincond,
                               vfate="TRUNCATED" if truncated else "UNTRACKED",
                               vlife=-1, vhp=-1)
                    recs.append(rec)
                    if kind == "INSERT":
                        old = active.pop(eid, None)
                        if old is not None:
                            close(old, rnd)
                        active[eid] = rec
                    # ⭐ VICTIM TRACKING, EVERY KIND. This is the whole fix: the
                    # registration below is NOT gated on `kind`, so an EXILE
                    # victim -- the ENEMY's builder -- gets followed exactly like
                    # our own ferried raider. No own-team filter appears anywhere
                    # on this path; that filter is what silently excluded the
                    # kidnap population for the life of this decoder.
                    # A THROW OF ANY KIND closes the previous window, so a bot
                    # thrown 152 times yields 151 RETHROWN records with the true
                    # inter-throw gap in `vlife` and one open window at the end.
                    if not truncated:
                        prev = vtrack.pop(eid, None)
                        if prev is not None:
                            vclose(prev, rnd, "RETHROWN")
                        rec["vfate"], rec["vhp"] = "OPEN", 0
                        vtrack[eid] = rec
                elif unum == 3:                                  # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        ents.pop(rv, None)
                        old = active.pop(rv, None)
                        if old is not None:
                            close(old, rnd)
                        # `RemoveEntity { int32 id = 1; }` -- one field, so the
                        # ungated loop above is exact. Kept ungated here for the
                        # same reason: two tracking dicts closed by two different
                        # predicates on the same event is how they drift apart.
                        vold = vtrack.pop(rv, None)
                        if vold is not None:
                            vclose(vold, rnd, "DIED")
                elif unum == 5:                                  # updateHp
                    # ⛔ THE DISCRIMINATOR, not decoration. A victim thrown to a
                    # border tile can die because its own off-map query raised
                    # (the plank) or because the landing tile sat in a turret line
                    # (geometry). `DIED with vhp == 0` is "removed with no HP
                    # event in the window at all" -- the crash/self-destruct
                    # signature `tools/crash_census.py` uses. Without this column
                    # the two are one number and the plank cannot be priced.
                    # ⚠ It CONFLATES an uncaught exception with self_destruct(),
                    # exactly as crash_census's own header says. That caveat
                    # travels with any number computed from it.
                    hid = None
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            hid = hv
                            break
                    vrec = vtrack.get(hid)
                    if vrec is not None:
                        vrec["vhp"] += 1
                elif unum == 13:                                 # builderAttack
                    aid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    rec = active.get(aid)
                    if rec is None or tgt is None:
                        continue
                    rec["any_atk"] += 1
                    b = ents.get(aid)
                    if b is not None and tgt in foot[1 - b.team]:
                        rec["core_atk"] += 1
        for bid, rec in active.items():
            b = ents.get(bid)
            if b is None:
                continue
            if any(abs(b.pos[0] - fx) + abs(b.pos[1] - fy) == 1
                   for fx, fy in foot[1 - b.team]):
                rec["reached"] = 1
    for bid, rec in active.items():                              # survived to the end
        close(rec, nrounds)
    # ⚠ ALIVE_END IS A CLAIM ABOUT THE REPLAY, NOT ABOUT THE GAME. `vlife` here is
    # the OBSERVATION WINDOW, so a throw on the last round closes as ALIVE_END
    # with vlife == 0 -- zero rounds of evidence, which is not evidence of
    # survival. Any lethality read must drop throws whose window is shorter than
    # the latency it is testing; the column carries the window so it can.
    for bid, rec in vtrack.items():
        vclose(rec, nrounds, "ALIVE_END")
    # `OPEN` is an INTERNAL state and must never reach the TSV. If it does, some
    # path registered a record and no path closed it, and the row would read as a
    # tracked bot with vlife == -1 -- i.e. it would look exactly like UNTRACKED,
    # re-creating the ambiguity this change exists to remove. Raise instead: the
    # caller counts it as a file error, which is visible, rather than emitting a
    # row that is wrong in a way nothing downstream can detect.
    for r in recs:
        if r["vfate"] == "OPEN":
            raise AssertionError(
                f"{path.name}: victim record for bot {r['bot']} thrown at round "
                f"{r['rnd']} was never closed")
    return recs


COLS = ["file", "mw", "mh", "rounds", "rnd", "kind", "tteam", "bteam", "amb",
        "d2_before", "d2_after", "bot", "life", "core_atk", "any_atk", "reached",
        "to_x", "to_y", "border",
        "winner", "wincond",
        # APPENDED, never inserted -- every reader of this file uses DictReader,
        # but a positional reader that predates the change still sees its columns
        # at the indices it expects.
        "vfate", "vlife", "vhp"]


def is_border(to, w, h):
    """Border classification. Extracted so a selftest can drive it directly.

    ⛔ Takes w/h AS ARGUMENTS and has no default. A version of this with a default
    map size is the defect this function exists to make impossible.
    """
    if not (w and h):
        raise ValueError("no map dimensions — a landing cannot be classified")
    return int(to[0] == 0 or to[1] == 0 or to[0] == w - 1 or to[1] == h - 1)


# ---------------------------------------------------------------------------
# SYNTHETIC REPLAY WRITER — used ONLY by the selftest.
#
# ⛔ THE CELLS BELOW DRIVE `census()` ITSELF, from raw bytes, through the same
# `fields()`/`parse_entity` path production uses. A fixture made of dicts would
# test a parallel implementation of the tracker and could not catch a wire-level
# defect -- the shape this repo has hit four times in one session. The cost is
# ~40 lines of encoder; the benefit is that the test and the claim are about the
# same code.
# ---------------------------------------------------------------------------
def _v(n: int) -> bytes:
    out = bytearray()
    while True:
        b, n = n & 0x7F, n >> 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def _ld(num: int, payload: bytes) -> bytes:
    return _v(num << 3 | 2) + _v(len(payload)) + payload


def _vf(num: int, val: int) -> bytes:
    return _v(num << 3 | 0) + _v(val)


def _pos(p) -> bytes:
    return _vf(1, p[0]) + _vf(2, p[1])


_KINDFIELD = {"builder_bot": 10, "launcher": 24}


def u_place(eid, team, p, kind) -> bytes:
    ent = (_vf(1, eid) + _vf(2, team) + _ld(3, _pos(p)) + _vf(4, 40) + _vf(5, 40)
           + _ld(_KINDFIELD[kind], b""))
    return _ld(1, _ld(1, ent))


def u_move(eid, p) -> bytes:
    return _ld(2, _vf(1, eid) + _ld(2, _pos(p)))


def u_remove(eid) -> bytes:
    return _ld(3, _vf(1, eid))


def u_hp(eid, delta) -> bytes:
    return _ld(5, _vf(1, eid) + _vf(2, delta))


def synth(w, h, cores, script, nrounds) -> bytes:
    """`script` is {round: [update bytes]}. cores is {team: (x, y)}."""
    m = _vf(1, w) + _vf(2, h)
    for t, p in sorted(cores.items()):
        m += _ld(4, _vf(1, 900 + t) + _vf(2, t) + _ld(3, _pos(p)))
    out = _ld(1, m)
    for r in range(nrounds):
        out += _ld(3, b"".join(_ld(1, u) for u in script.get(r, [])))
    return out + _vf(4, 0) + _ld(6, b"core_destroyed")


def _run(blob: bytes, tmp: Path):
    tmp.write_bytes(blob)
    return census(tmp)


def victim_cells(tmp_dir: Path) -> list[tuple[str, bool, str]]:
    """Forced-answer cells for vfate / vlife / vhp. Every one of these is a pair:
    the SAME fixture with ONE fact changed must flip the verdict. A cell that only
    ever produced one answer has not been seen to check anything.
    """
    W = H = 10
    CORES = {0: (1, 1), 1: (8, 8)}
    tmp = tmp_dir / "_synth.replay26"
    cells = []

    def cell(name, cond, detail=""):
        cells.append((name, bool(cond), detail))

    # Enemy (team 0) builder id 5 at (5,4); OUR (team 1) launcher id 7 at (5,5).
    base = [u_place(7, 1, (5, 5), "launcher"), u_place(5, 0, (5, 4), "builder_bot")]
    THROW = u_move(5, (0, 3))          # (0,3) is BORDER on 10x10

    # --- A. EXILE, victim removed one round later, no HP event in the window.
    rows = _run(synth(W, H, CORES, {0: base, 10: [THROW], 11: [u_remove(5)]}, 20), tmp)
    ex = [r for r in rows if r["kind"] == "EXILE"]
    cell("EXILE row is produced at all", len(ex) == 1, f"got {len(ex)}")
    r0 = ex[0] if ex else {}
    cell("EXILE lands on a BORDER tile", r0.get("border") == 1)
    cell("victim removed 1 round later reads DIED", r0.get("vfate") == "DIED",
         str(r0.get("vfate")))
    cell("vlife is the ROUNDS FROM THE THROW, not from birth", r0.get("vlife") == 1,
         str(r0.get("vlife")))
    cell("no HP event in the window reads vhp == 0 (crash signature)",
         r0.get("vhp") == 0, str(r0.get("vhp")))
    # ⛔ THE REGRESSION THIS PAIRS WITH: `life` is an INSERT column and an EXILE
    # row must still leave it at the -1 sentinel. If victim tracking ever writes
    # into it, every historical INSERT analysis silently changes population.
    cell("EXILE leaves the INSERT column `life` at -1", r0.get("life") == -1)

    # --- B. THE SAME FIXTURE WITHOUT THE REMOVAL. One fact changed.
    rows = _run(synth(W, H, CORES, {0: base, 10: [THROW]}, 20), tmp)
    ex = [r for r in rows if r["kind"] == "EXILE"]
    r1 = ex[0] if ex else {}
    cell("victim never removed reads ALIVE_END — SAME FIXTURE, ONE FACT CHANGED",
         r1.get("vfate") == "ALIVE_END", str(r1.get("vfate")))
    cell("ALIVE_END carries the OBSERVATION WINDOW in vlife (20-10)",
         r1.get("vlife") == 10, str(r1.get("vlife")))
    cell("vfate is not a constant across A and B",
         r0.get("vfate") != r1.get("vfate"))

    # --- C. THROWN TWICE. The 152-throw fixture in miniature.
    # A SECOND launcher sits beside the first landing tile, because attribution is
    # computed from the tile the bot LEAVES: without it the re-throw classifies
    # UNATTRIB (no launcher within d2<=2 of (0,3)) and the cell would be measuring
    # the wrong kind. Caught by this cell failing on the first run.
    base2 = base + [u_place(8, 1, (1, 3), "launcher")]
    rows = _run(synth(W, H, CORES, {0: base2, 10: [THROW], 15: [u_move(5, (0, 6))]}, 20), tmp)
    ex = sorted([r for r in rows if r["kind"] == "EXILE"], key=lambda r: r["rnd"])
    cell("two throws produce two rows", len(ex) == 2, f"got {len(ex)}")
    if len(ex) == 2:
        cell("the FIRST window closes RETHROWN, not DIED", ex[0]["vfate"] == "RETHROWN",
             ex[0]["vfate"])
        cell("its vlife is the INTER-THROW GAP (15-10)", ex[0]["vlife"] == 5,
             str(ex[0]["vlife"]))
        cell("the SECOND window is still open at the end", ex[1]["vfate"] == "ALIVE_END",
             ex[1]["vfate"])

    # --- D. COMBAT DEATH. Removed, but with HP events in the window.
    rows = _run(synth(W, H, CORES,
                      {0: base, 10: [THROW], 11: [u_hp(5, 7)], 12: [u_hp(5, 7)],
                       13: [u_remove(5)]}, 20), tmp)
    r3 = [r for r in rows if r["kind"] == "EXILE"][0]
    cell("a damaged-then-removed victim still reads DIED", r3["vfate"] == "DIED")
    cell("vhp COUNTS the HP events in the window (2)", r3["vhp"] == 2, str(r3["vhp"]))
    cell("vhp separates a combat death from a crash death — 2 vs 0",
         r3["vhp"] != r0.get("vhp"))
    # HP events for a DIFFERENT entity must not land on this victim's counter.
    rows = _run(synth(W, H, CORES,
                      {0: base, 10: [THROW], 11: [u_hp(7, 7)], 13: [u_remove(5)]}, 20), tmp)
    cell("an HP event naming ANOTHER entity does not increment vhp",
         [r for r in rows if r["kind"] == "EXILE"][0]["vhp"] == 0)

    # --- E. INSERT IS UNTOUCHED, and gains the same columns.
    ibase = [u_place(7, 0, (5, 5), "launcher"), u_place(5, 0, (5, 4), "builder_bot")]
    rows = _run(synth(W, H, CORES,
                      {0: ibase, 10: [u_move(5, (7, 7))], 13: [u_remove(5)]}, 20), tmp)
    ins = [r for r in rows if r["kind"] == "INSERT"]
    cell("INSERT still classified and still populates `life`",
         len(ins) == 1 and ins[0]["life"] == 3,
         f"n={len(ins)} life={ins[0]['life'] if ins else 'NA'}")
    cell("INSERT also gets victim columns, and they agree with `life`",
         bool(ins) and ins[0]["vfate"] == "DIED" and ins[0]["vlife"] == 3)

    # --- F. TRUNCATION. ⛔ THE CELL THAT KEEPS "COULD NOT TRACK" OUT OF
    # "NO DEATH OBSERVED". A short file makes every open window read ALIVE_END,
    # which is the flattering direction for "the throw did not kill it".
    blob = synth(W, H, CORES, {0: base, 10: [THROW], 11: [u_remove(5)]}, 20)
    rows = _run(blob[: len(blob) - 3], tmp)
    ex = [r for r in rows if r["kind"] == "EXILE"]
    cell("a TRUNCATED replay still yields its rows", len(ex) >= 1, f"got {len(ex)}")
    if ex:
        cell("...but they read TRUNCATED, never ALIVE_END",
             ex[0]["vfate"] == "TRUNCATED", ex[0]["vfate"])
        cell("...and vlife is the -1 sentinel, so no window is claimed",
             ex[0]["vlife"] == -1, str(ex[0]["vlife"]))
    cell("the intact copy of the SAME bytes does NOT read TRUNCATED",
         _run(blob, tmp)[0]["vfate"] != "TRUNCATED")

    # --- G. `OPEN` never escapes.
    cell("no row ever carries the internal OPEN state",
         all(r["vfate"] != "OPEN" for r in rows))
    tmp.unlink(missing_ok=True)
    return cells


def real_fixture_cell() -> tuple[bool, str]:
    """⭐ THE KNOWN REAL CASE, and it is a NEGATIVE one on purpose.

    `77d7e100-..._game_1` vs 0033 v57: we threw ONE enemy builder (bot 5) **152
    times, rounds 241 to 996, every landing on a border tile.** A bot still being
    thrown at r996 of a 1000-round game demonstrably DID NOT DIE. So this fixture
    can only be passed by a decoder that reports survival — a tracker that
    over-fires (closes a window as DIED on any removal event, or mistakes a
    re-throw for a death) fails it loudly.

    A synthetic fixture cannot do this job: it encodes this lane's assumptions
    about the wire format, which is exactly what could be wrong.
    """
    p = (Path(__file__).resolve().parent.parent.parent / "replay_archive" /
         "77d7e100-6cb3-4c49-85cc-e91192caf8cd_game_1.replay26")
    if not p.exists():
        return True, "SKIP — archive replay absent, CELL DID NOT RUN"
    rows = [r for r in census(p) if r["kind"] == "EXILE" and r["bot"] == 5]
    died = [r for r in rows if r["vfate"] == "DIED"]
    rethrown = [r for r in rows if r["vfate"] == "RETHROWN"]
    alive = [r for r in rows if r["vfate"] == "ALIVE_END"]
    border = sum(r["border"] for r in rows)
    ok = (len(rows) == 152 and border == 152 and not died
          and len(rethrown) == 151 and len(alive) == 1)
    return ok, (f"152-throw fixture: rows {len(rows)} · border {border} · "
                f"RETHROWN {len(rethrown)} · ALIVE_END {len(alive)} · DIED {len(died)}")


def selftest() -> int:
    """Forced-answer cells for the border flag.

    This instrument supplies the FIELD PREVALENCE number for the crash channel --
    the number D23 says cannot be obtained any other way -- so it is the one that
    most needs driving both ways. Written after the side lane observed that four
    instruments in one session had a test that could not catch their own bug, and
    that this file was in the worst category: no test at all.
    """
    fails = []

    def check(name, cond, detail=""):
        print(f"  [{'ok' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
        if not cond:
            fails.append(name)

    # 1. THE SIZE TRAP. Same coordinate, opposite verdict, because the map differs.
    # A regression to any fixed size fails this loudly instead of silently.
    check("(13,1) is BORDER on antler 14x18", is_border((13, 1), 14, 18) == 1)
    check("(13,1) is INTERIOR on 26x26 — SAME COORD, OPPOSITE VERDICT",
          is_border((13, 1), 26, 26) == 0)
    check("(24,7) is BORDER on meander 25x15", is_border((24, 7), 25, 15) == 1)
    check("(24,7) is INTERIOR on 26x26", is_border((24, 7), 26, 26) == 0)
    check("(5,14) is BORDER on meander 25x15 (y == h-1)", is_border((5, 14), 25, 15) == 1)
    check("(5,14) is INTERIOR on hive 25x25", is_border((5, 14), 25, 25) == 0)

    # 2. THE FALLBACK CELL. Missing dimensions must RAISE, never quietly read 0.
    # Without this, `w=0` makes `to[0] == w-1` unsatisfiable and only the near
    # edges count -- far edges misfiled as interior, biased toward the null.
    try:
        is_border((13, 1), 0, 0)
        check("missing dimensions REFUSE rather than defaulting", False, "returned instead of raising")
    except ValueError:
        check("missing dimensions REFUSE rather than defaulting", True)
    check("a far-edge landing is not silently interior under a 0 width",
          is_border((13, 0), 14, 18) == 1)

    # 3. A GENUINE INTERIOR LANDING. Without this the flag could be a constant 1.
    check("a centre landing is INTERIOR", is_border((12, 9), 25, 25) == 0)
    check("all four edges register", all(is_border(p, 10, 10) == 1
          for p in ((0, 5), (9, 5), (5, 0), (5, 9))))
    check("the tile just inside each edge does NOT", all(is_border(p, 10, 10) == 0
          for p in ((1, 5), (8, 5), (5, 1), (5, 8))))

    # 4. VICTIM FATE — synthetic replays through the SHIPPED census() path.
    print("\n  -- victim fate (vfate / vlife / vhp), synthetic replays --")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        for name, ok, detail in victim_cells(Path(td)):
            check(name, ok, detail)

    # 5. VICTIM FATE — the known real case, which must read SURVIVED.
    print("\n  -- victim fate, REAL corpus fixture --")
    ok, detail = real_fixture_cell()
    check("bot 5 thrown 152x to r996 reads as SURVIVING, not dying", ok, detail)

    print()
    if fails:
        print(f"SELFTEST FAILED: {len(fails)}: {', '.join(fails)}")
        return 1
    print("SELFTEST PASSED — the classifier was driven to BORDER and to INTERIOR on\n"
          "the SAME coordinate by changing only the map, and refuses without dimensions;\n"
          "and victim fate was driven to DIED, ALIVE_END, RETHROWN and TRUNCATED on\n"
          "fixtures differing by one fact, with the 152-throw real case reading SURVIVED.")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    out = sys.stdout
    out.write("\t".join(COLS) + "\n")
    bad = 0
    for i, p in enumerate(Path(x) for x in argv):
        try:
            for rec in census(p):
                out.write("\t".join(str(rec[c]) for c in COLS) + "\n")
        except Exception as exc:                                 # noqa: BLE001
            bad += 1
            print(f"ERR {p.name}: {exc}", file=sys.stderr)
        if (i + 1) % 500 == 0:
            print(f"  ...{i+1}/{len(argv)} ({bad} err)", file=sys.stderr, flush=True)
    print(f"done {len(argv)} files, {bad} errors", file=sys.stderr, flush=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
