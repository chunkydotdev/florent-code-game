#!/usr/bin/env python3
"""Builder-bot DEATH-CAUSE decoder (read-only; scratchpad output only).

Method
------
Ground truth for "how much damage" is the HP ledger (UpdateHp, Update field 5;
`delta` is a 64-bit two's-complement varint -- corpus-howto trap 2).
Attribution of "who" is FireTurret (field 12), resolved against the tiles the
victim occupied during the round (round-start position + every move
destination that round), per the S1 ordering trap in tools/replay_schema.md:
FireTurret can be emitted AFTER the victim's removeEntity in the same round.

Shooter kind comes from the building standing on `from` at round start.
Damage: gunner 7, sentinel 18, launcher 0 (throws deal no damage).

Friendly fire is REAL and must not be filtered out: turret fire hits the unit
on the target tile whatever its team (verified: a team-0 gunner shooting an
enemy conveyor at (18,10) killed its own builder bot standing on that tile,
010eb62d..._game_3, bot 5, r112).

Crash discriminator: BotOutput (field 9) carries the unit's stdout.  The engine
prints a traceback and permanently destroys a unit whose run() raises.  A
no-damage removal whose unit printed a traceback is a CRASH; without one it is
labelled UNEXPLAINED (self-destruct or something else) -- never guessed.

Outputs (TSV, one row per builder death) to <outdir>/dc_deaths.tsv, plus
per-file per-team-per-band builder-round exposure to <outdir>/dc_expo.tsv.
"""
from __future__ import annotations

import os
import sys
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

DMG = {"gunner": 7, "sentinel": 18}
HOME_D2 = 32


def s64(v):
    return v - (1 << 64) if v >= (1 << 63) else v


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def decode(path: Path):
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None
    cores = []
    for num, wire, value in fields(map_buf):
        if num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    if len(cores) != 2:
        return None
    corepos = {c["team"]: c["pos"] for c in cores}
    nr = len(turn_bufs)

    team_of, kind_of, pos_of, born = {}, {}, {}, {}
    bldg_at, bot_at = {}, {}
    for c in cores:
        team_of[c["id"]] = c["team"]
        kind_of[c["id"]] = "core"
        pos_of[c["id"]] = c["pos"]
        born[c["id"]] = 0
        for dx in (0, 1):
            for dy in (0, 1):
                bldg_at[(c["pos"][0] + dx, c["pos"][1] + dy)] = c["id"]

    # per-bot accumulators
    hp_now, hp_lost, hp_healed = {}, {}, {}
    dmg_r = {}          # bid -> {round: hp lost that round}
    shots_r = {}        # bid -> {round: [(skind, steam, sd2)]}
    thrown_r = {}       # bid -> set of rounds thrown
    crashed_r = {}      # bid -> round of first traceback in its stdout
    tled_n = {}         # bid -> count of tled turns
    deaths = []         # (bid, team, rnd, pos)
    expo = {}           # (team, band) -> builder-rounds

    for rnd, turn_buf in enumerate(turn_bufs):
        bot_start = dict(bot_at)
        bldg_start = dict(bldg_at)
        occ = {}                      # bid -> set of tiles held this round
        for p, b in bot_start.items():
            occ.setdefault(b, set()).add(p)
        tile_owner = {}               # tile -> set of bids that held it
        for p, b in bot_start.items():
            tile_owner.setdefault(p, set()).add(b)

        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                    # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in pos_of:                       # re-emit
                            old = pos_of[e.id]
                            if old != e.pos:
                                if kind_of[e.id] == "builder_bot":
                                    if bot_at.get(old) == e.id:
                                        del bot_at[old]
                                    bot_at[e.pos] = e.id
                                    occ.setdefault(e.id, set()).add(e.pos)
                                    tile_owner.setdefault(e.pos, set()).add(e.id)
                                else:
                                    if bldg_at.get(old) == e.id:
                                        del bldg_at[old]
                                    bldg_at[e.pos] = e.id
                                pos_of[e.id] = e.pos
                            if e.hp:
                                hp_now[e.id] = e.hp
                            continue
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                        pos_of[e.id] = e.pos
                        born[e.id] = rnd
                        hp_now[e.id] = e.hp
                        if e.kind == "builder_bot":
                            bot_at[e.pos] = e.id
                            hp_lost[e.id] = 0
                            hp_healed[e.id] = 0
                            dmg_r[e.id] = {}
                            shots_r[e.id] = {}
                            thrown_r[e.id] = set()
                            tled_n[e.id] = 0
                            occ.setdefault(e.id, set()).add(e.pos)
                            tile_owner.setdefault(e.pos, set()).add(e.id)
                        else:
                            bldg_at[e.pos] = e.id
                elif unum == 2:                                  # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid not in pos_of or to is None:
                        continue
                    old = pos_of[eid]
                    if max(abs(old[0] - to[0]), abs(old[1] - to[1])) > 1:
                        thrown_r.setdefault(eid, set()).add(rnd)
                    if bot_at.get(old) == eid:
                        del bot_at[old]
                    bot_at[to] = eid
                    pos_of[eid] = to
                    occ.setdefault(eid, set()).add(to)
                    tile_owner.setdefault(to, set()).add(eid)
                elif unum == 3:                                  # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        if rv not in pos_of:
                            continue
                        p = pos_of.pop(rv)
                        if kind_of.get(rv) == "builder_bot":
                            if bot_at.get(p) == rv:
                                del bot_at[p]
                            deaths.append((rv, team_of[rv], rnd, p))
                        else:
                            if bldg_at.get(p) == rv:
                                del bldg_at[p]
                elif unum == 5:                                  # updateHp
                    eid = delta = None
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            delta = s64(hv)
                    if eid is None or delta is None:
                        continue
                    if eid in hp_now:
                        hp_now[eid] += delta
                    if kind_of.get(eid) == "builder_bot":
                        if delta < 0:
                            hp_lost[eid] = hp_lost.get(eid, 0) - delta
                            d = dmg_r.setdefault(eid, {})
                            d[rnd] = d.get(rnd, 0) - delta
                        else:
                            hp_healed[eid] = hp_healed.get(eid, 0) + delta
                elif unum == 9:                                  # botOutput
                    eid, out, tled = None, b"", False
                    for bn, _bw, bv in fields(ubuf):
                        if bn == 1:
                            eid = bv
                        elif bn == 2:
                            out = bv
                        elif bn == 4:
                            tled = bool(bv)
                    if eid is None:
                        continue
                    if tled and eid in tled_n:
                        tled_n[eid] += 1
                    if out and b"Traceback" in out and eid not in crashed_r:
                        crashed_r[eid] = rnd
                elif unum == 12:                                 # fireTurret
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    if to is None:
                        continue
                    sid = bldg_start.get(frm)
                    if sid is None:
                        sid = bldg_at.get(frm)
                    sk = kind_of.get(sid, "?")
                    st = team_of.get(sid, -1)
                    cands = set(tile_owner.get(to, ()))
                    cur = bot_at.get(to)
                    if cur is not None:
                        cands.add(cur)
                    for bid in cands:
                        shots_r.setdefault(bid, {}).setdefault(rnd, []).append(
                            (sk, st, d2(frm, to) if frm else -1,
                             len(cands), frm))

        # exposure: one builder-round per living builder, bucketed by band
        for p, b in bot_at.items():
            t = team_of[b]
            cp = corepos[t]
            band = "HOME" if d2(p, cp) <= HOME_D2 else "FWD"
            expo[(t, band)] = expo.get((t, band), 0) + 1
            fp = min(d2(p, (cp[0] + dx, cp[1] + dy))
                     for dx in (0, 1) for dy in (0, 1))
            expo[(t, "FP_HOME" if fp <= HOME_D2 else "FP_FWD")] = \
                expo.get((t, "FP_HOME" if fp <= HOME_D2 else "FP_FWD"), 0) + 1

    return dict(name=path.name, nr=nr, corepos=corepos, deaths=deaths,
                hp_lost=hp_lost, hp_healed=hp_healed, dmg_r=dmg_r,
                shots_r=shots_r, thrown_r=thrown_r, crashed_r=crashed_r,
                tled_n=tled_n, born=born, expo=expo)


DEATH_COLS = ["file", "team", "bid", "rnd", "nrounds", "x", "y", "band",
              "core_d2", "born", "life", "hp_lost_life", "hp_healed_life",
              "dr_hploss", "dr_shotdmg", "recon", "cls", "killer",
              "n_gun_enemy", "n_sen_enemy", "n_gun_own", "n_sen_own",
              "n_other", "max_shot_d2", "sen_d2", "thrown", "crash", "tled",
              "band_fp", "core_d2_fp", "shooter_core_d2", "gun_d2",
              "sx", "sy"]
EXPO_COLS = ["file", "team", "band", "botrounds"]


def rows(R):
    for (bid, team, rnd, pos) in R["deaths"]:
        cd2 = d2(pos, R["corepos"][team])
        band = "HOME" if cd2 <= HOME_D2 else "FWD"
        dr_hp = R["dmg_r"].get(bid, {}).get(rnd, 0)
        sh = R["shots_r"].get(bid, {}).get(rnd, [])
        ng_e = sum(1 for s in sh if s[0] == "gunner" and s[1] != team)
        ns_e = sum(1 for s in sh if s[0] == "sentinel" and s[1] != team)
        ng_o = sum(1 for s in sh if s[0] == "gunner" and s[1] == team)
        ns_o = sum(1 for s in sh if s[0] == "sentinel" and s[1] == team)
        nother = len(sh) - ng_e - ns_e - ng_o - ns_o
        sd = sum(DMG.get(s[0], 0) for s in sh)
        maxd2 = max((s[2] for s in sh), default=-1)
        send2 = max((s[2] for s in sh if s[0] == "sentinel"), default=-1)
        gund2 = max((s[2] for s in sh if s[0] == "gunner"), default=-1)
        cp = R["corepos"][team]
        # nearest-footprint-tile band, as a sensitivity control on the d2<=32 cut
        fp = min(d2(pos, (cp[0] + dx, cp[1] + dy))
                 for dx in (0, 1) for dy in (0, 1))
        band_fp = "HOME" if fp <= HOME_D2 else "FWD"
        # how deep in the VICTIM's own base the killing turret sits
        sc = min((d2(s[4], cp) for s in sh
                  if s[4] is not None and s[1] != team), default=-1)
        spos = next((s[4] for s in sh if s[4] is not None and s[1] != team),
                    (-1, -1))
        crash = R["crashed_r"].get(bid, -1)
        # classification
        if dr_hp == 0 and not sh:
            cls, killer = "NO_DAMAGE", ("CRASH" if 0 <= crash <= rnd
                                        else "UNEXPLAINED")
        elif sh and sd == dr_hp and dr_hp > 0:
            cls = "ATTRIB"
            kinds = set()
            if ng_e or ns_e:
                kinds.add("ENEMY")
            if ng_o or ns_o:
                kinds.add("OWN")
            if ng_e + ng_o and ns_e + ns_o:
                tk = "MIXED"
            elif ns_e + ns_o:
                tk = "SENTINEL"
            elif ng_e + ng_o:
                tk = "GUNNER"
            else:
                tk = "OTHER"
            killer = ("ENEMY_" if kinds == {"ENEMY"} else
                      "OWN_" if kinds == {"OWN"} else "BOTH_") + tk
        else:
            cls, killer = "AMBIGUOUS", "?"
        yield "deaths", (R["name"], team, bid, rnd, R["nr"], pos[0], pos[1],
                         band, cd2, R["born"].get(bid, -1),
                         rnd - R["born"].get(bid, -1),
                         R["hp_lost"].get(bid, 0), R["hp_healed"].get(bid, 0),
                         dr_hp, sd, "Y" if sd == dr_hp else "N", cls, killer,
                         ng_e, ns_e, ng_o, ns_o, nother, maxd2, send2,
                         1 if rnd in R["thrown_r"].get(bid, ()) else 0,
                         crash, R["tled_n"].get(bid, 0),
                         band_fp, fp, sc, gund2, spos[0], spos[1])
    for (t, band), n in R["expo"].items():
        yield "expo", (R["name"], t, band, n)


def work(p):
    try:
        R = decode(Path(p))
    except Exception as exc:                                     # noqa: BLE001
        return ("ERR", str(p), repr(exc))
    if R is None:
        return ("ERR", str(p), "no map/cores")
    out = {"deaths": [], "expo": []}
    for tbl, row in rows(R):
        out[tbl].append("\t".join(str(v) for v in row))
    return ("OK", out)


def main(argv):
    outdir = argv[0]
    files = argv[1:]
    if len(files) == 1 and files[0].startswith("@"):
        files = [l.strip() for l in open(files[0][1:]) if l.strip()]
    fh = {"deaths": open(os.path.join(outdir, "dc_deaths.tsv"), "w"),
          "expo": open(os.path.join(outdir, "dc_expo.tsv"), "w")}
    fh["deaths"].write("\t".join(DEATH_COLS) + "\n")
    fh["expo"].write("\t".join(EXPO_COLS) + "\n")
    bad = 0
    with Pool(8) as pool:
        for i, res in enumerate(pool.imap_unordered(work, files, chunksize=8)):
            if res[0] == "ERR":
                bad += 1
                print("ERR", res[1], res[2], file=sys.stderr)
                continue
            for k, lines in res[1].items():
                if lines:
                    fh[k].write("\n".join(lines) + "\n")
            if (i + 1) % 250 == 0:
                print(f"  ...{i+1}/{len(files)} ({bad} err)", file=sys.stderr,
                      flush=True)
    for f in fh.values():
        f.close()
    print(f"done {len(files)} files, {bad} errors", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
