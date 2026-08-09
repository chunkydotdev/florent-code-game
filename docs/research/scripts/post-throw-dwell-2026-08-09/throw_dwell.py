#!/usr/bin/env python3
"""POST-THROW TILE DWELL — how long does a thrown builder bot sit on its landing tile?

Question (builder arm, 2026-08-09, decisive for the "kidnap plank"): a launcher
grabs an ENEMY builder bot and throws it onto a tile covered by our own gunner's
firing ray.  A gunner needs ~11 rounds to kill a 40 HP bot, a sentinel ~7.  If
the thrown bot walks off the ray the round after it lands, kidnap-into-ray is
DISPLACEMENT worth one shot; if it sits there for 3+ rounds it is a KILL play.

This script measures, for every launcher throw in the archive, how many rounds
the victim stayed on its landing tile.

DETECTION (corpus-howto trap 3): launcher throws emit no FireTurret.  A throw is
a `moveBuilderBot` (Update field 2) whose destination is MORE than one tile
(manhattan) from the bot's previous position.  The thrower is a launcher alive at
d^2 <= 2 of the PRE-THROW tile (diagonals included); if launchers of both teams
are in range the throw is UNATTRIB, never guessed.  Same rule as
`tools/corpus/replay_throws.py`, so the throw sets reconcile row-for-row.

DWELL is measured off the same event stream:

    dwell = (round of the first later event that puts the bot on a tile != T) - r0

`moveBuilderBot` is the only positional event a builder bot emits, so this is
exact.  Note dwell CAN be 0: the launcher acts during its own unit turn and the
victim's own run() may come later in the SAME round buffer, in which case the
victim steps off without ever being on T at a round boundary.

CENSORING is reported separately, never folded into the moved-off distribution:

    died   the bot is removed while still on T          -> censored at death - r0
    end    the game ends with the bot still on T        -> censored at last - r0
    rethrow the bot's next positional event is another throw (it still left T,
            but by someone else's hand, so it is tracked as its own exit reason)

Populations: `corpus/join.tsv` maps replay file -> which team index is US.  It
covers only our ladder games; files outside it are reported as UNATTRIBUTED, not
guessed and not dropped.

Modes
-----
    scan   ... one row per throw, TSV on stdout
    report ... read that TSV (+ join.tsv, throws.tsv) and print the tables

Usage
-----
    .venv/bin/python docs/research/scripts/post-throw-dwell-2026-08-09/throw_dwell.py \
        scan --files scratch/files.txt -j 8 > scratch/dwell.tsv
    .venv/bin/python docs/research/scripts/post-throw-dwell-2026-08-09/throw_dwell.py \
        report scratch/dwell.tsv --join corpus/join.tsv --throws corpus/throws.tsv

Run `scan` against a FROZEN file list (the keeper auto-syncs corpus/ every ~10
min and the archive grows ~80 replays/hour), so the numbers are internally
consistent and reconcile against a throws.tsv snapshot taken at the same time.
"""
from __future__ import annotations

import argparse
import collections
import csv
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[4]          # repo root
sys.path.insert(0, str(_ROOT / "tools"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN, WIRE_VARINT  # noqa: E402


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


class Ent:
    __slots__ = ("id", "team", "pos", "kind")

    def __init__(self, eid, team, pos, kind):
        self.id, self.team, self.pos, self.kind = eid, team, pos, kind


def _tiles(pos, kind):
    """Tiles an entity occupies. Core position is the NW corner of a 2x2."""
    x, y = pos
    if kind == "core":
        return ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1))
    return ((x, y),)


COLS = ["file", "rounds", "rnd", "bot", "bteam", "tteam", "tid", "amb", "rel",
        "lx", "ly", "occ", "occ_what", "dwell", "exit", "d2_before", "d2_after"]


def scan(path: Path):
    """One record per throw, with dwell + exit reason resolved."""
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return []

    cores = []
    for num, _wire, value in fields(map_buf):
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
    corepos = {c["team"]: c["pos"] for c in cores}
    if len(corepos) != 2:
        return []

    ents: dict[int, Ent] = {}
    occ: dict[tuple, set] = {}

    def add_occ(e):
        for t in _tiles(e.pos, e.kind):
            occ.setdefault(t, set()).add(e.id)

    def del_occ(e):
        for t in _tiles(e.pos, e.kind):
            s = occ.get(t)
            if s:
                s.discard(e.id)

    for c in cores:
        e = Ent(c["id"], c["team"], c["pos"], "core")
        ents[e.id] = e
        add_occ(e)

    recs = []
    open_recs: dict[int, dict] = {}          # bot id -> throw rec still sitting on T
    nrounds = len(turn_bufs)

    def close(rec, rnd, reason):
        rec["dwell"] = rnd - rec["rnd"]
        rec["exit"] = reason

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
                        old = ents.get(e.id)
                        if old is not None:
                            # placeEntity is RE-EMITTED on gunner rotate (trap 1):
                            # not a new entity, but keep the position authoritative.
                            if old.pos != e.pos:
                                del_occ(old)
                                old.pos = e.pos
                                add_occ(old)
                            continue
                        ne = Ent(e.id, e.team, e.pos, e.kind)
                        ents[e.id] = ne
                        add_occ(ne)
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
                    del_occ(e)
                    e.pos = to
                    add_occ(e)
                    is_throw = abs(to[0] - frm[0]) + abs(to[1] - frm[1]) > 1
                    # Did this move take a previously-thrown bot off its landing tile?
                    prev = open_recs.get(eid)
                    if prev is not None and to != (prev["lx"], prev["ly"]):
                        close(prev, rnd, "rethrow" if is_throw else "step")
                        open_recs.pop(eid, None)
                    if not is_throw:
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
                    # Thrower entity id, but ONLY when exactly one launcher was in
                    # range — with two candidates the id is a guess, and the
                    # turn-order test below is worthless on a guessed id.
                    tid = cand[0].id if len(cand) == 1 else -1
                    bteam = e.team
                    ec = corepos[(1 - tteam) if tteam is not None else (1 - bteam)]
                    rel = ("unattrib" if tteam is None else
                           "own" if tteam == bteam else "enemy")
                    # What else is standing on the landing tile? A builder bot can
                    # legally share a tile with some buildings (`is_tile_passable`
                    # is deliberately weaker than `is_tile_empty`), so "throw
                    # targets are empty tiles" is worth measuring, not assuming.
                    others = [ents[i] for i in occ.get(to, ()) if i != eid and i in ents]
                    rec = dict(file=path.name, rounds=nrounds, rnd=rnd, bot=eid,
                               bteam=bteam, tteam=-1 if tteam is None else tteam,
                               tid=tid, amb=amb, rel=rel, lx=to[0], ly=to[1],
                               occ=len(others),
                               occ_what=",".join(sorted(
                                   f"{o.kind}:{'own' if o.team == bteam else 'foe'}"
                                   for o in others)) or "-",
                               dwell=-1, exit="open",
                               d2_before=d2(frm, ec), d2_after=d2(to, ec))
                    recs.append(rec)
                    open_recs[eid] = rec
                elif unum == 3:                                  # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        if rn != 1:
                            continue
                        e = ents.pop(rv, None)
                        if e is not None:
                            del_occ(e)
                        prev = open_recs.pop(rv, None)
                        if prev is not None:
                            close(prev, rnd, "died")
    for rec in open_recs.values():
        close(rec, nrounds - 1, "end")
    return recs


def _scan_one(p):
    try:
        return scan(Path(p)), None
    except Exception as exc:                                     # noqa: BLE001
        return [], f"{Path(p).name}: {type(exc).__name__}: {exc}"


def cmd_scan(args):
    paths = [ln.strip() for ln in open(args.files) if ln.strip()]
    out = sys.stdout
    out.write("\t".join(COLS) + "\n")
    bad = 0
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        for i, (recs, err) in enumerate(ex.map(_scan_one, paths, chunksize=16)):
            if err:
                bad += 1
                print("ERR " + err, file=sys.stderr)
            for r in recs:
                out.write("\t".join(str(r[c]) for c in COLS) + "\n")
            if (i + 1) % 1000 == 0:
                print(f"  ...{i+1}/{len(paths)} ({bad} err)", file=sys.stderr, flush=True)
    print(f"done {len(paths)} files, {bad} errors", file=sys.stderr, flush=True)


# --- reporting ---------------------------------------------------------------

BANDS = [("0", lambda d: d == 0), ("1", lambda d: d == 1), ("2", lambda d: d == 2),
         ("3", lambda d: d == 3), ("4", lambda d: d == 4), ("5", lambda d: d == 5),
         ("6-10", lambda d: 6 <= d <= 10), ("11+", lambda d: d >= 11)]
BAND_NAMES = [b[0] for b in BANDS]


def band(d):
    for name, test in BANDS:
        if test(d):
            return name
    return "?"


def hist(rows):
    c = collections.Counter(band(r["dwell"]) for r in rows)
    return c, len(rows)


def table(title, groups, out=sys.stdout):
    w = out.write
    w(f"\n{title}\n")
    w(f"{'population':32s}{'N':>8s}" + "".join(f"{b:>9s}" for b in BAND_NAMES)
      + f"{'median':>9s}{'mean':>8s}\n")
    for name, rows in groups:
        c, n = hist(rows)
        if not n:
            w(f"{name:32s}{0:>8d}\n")
            continue
        ds = sorted(r["dwell"] for r in rows)
        med = ds[n // 2]
        mean = sum(ds) / n
        w(f"{name:32s}{n:>8d}"
          + "".join(f"{100.0*c[b]/n:>8.1f}%" for b in BAND_NAMES)
          + f"{med:>9d}{mean:>8.2f}\n")


def cmd_report(args):
    rows = []
    with open(args.tsv) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            r["dwell"] = int(r["dwell"])
            r["rnd"] = int(r["rnd"])
            r["bot"] = int(r["bot"])
            r["occ"] = int(r["occ"])
            r["tteam"] = int(r["tteam"])
            r["bteam"] = int(r["bteam"])
            rows.append(r)
    J = {}
    with open(args.join) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            J[r["file"]] = int(r["our_team"])
    for r in rows:
        ours = J.get(r["file"])
        if ours is None or r["tteam"] < 0:
            r["side"] = "UNATTRIB"
        else:
            r["side"] = "US" if r["tteam"] == ours else "THEM"

    w = sys.stdout.write
    w(f"throws scanned: {len(rows)}   files in join.tsv: {len(J)}\n")

    # ---- validation against corpus/throws.tsv ----
    if args.throws:
        mine = {(r["file"], r["rnd"], r["bot"]) for r in rows}
        theirs = set()
        with open(args.throws) as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                theirs.add((r["file"], int(r["rnd"]), int(r["bot"])))
        inter = mine & theirs
        w("\nVALIDATION vs corpus/throws.tsv on (file, rnd, bot)\n")
        w(f"  mine        {len(mine)}\n  throws.tsv  {len(theirs)}\n")
        w(f"  agree       {len(inter)}  "
          f"({100.0*len(inter)/max(len(mine),1):.4f}% of mine, "
          f"{100.0*len(inter)/max(len(theirs),1):.4f}% of theirs)\n")
        w(f"  mine only   {len(mine - theirs)}\n  theirs only {len(theirs - mine)}\n")
        # life sanity: dwell can never exceed life (INSERT rows only carry life)
        life = {}
        with open(args.throws) as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                if r["kind"] == "INSERT":
                    life[(r["file"], int(r["rnd"]), int(r["bot"]))] = int(r["life"])
        checked = viol = 0
        for r in rows:
            k = (r["file"], r["rnd"], r["bot"])
            if k in life and life[k] >= 0:
                checked += 1
                if r["dwell"] > life[k]:
                    viol += 1
        w(f"  dwell<=life {checked - viol}/{checked} INSERT rows "
          f"({viol} violations)\n")

    moved = [r for r in rows if r["exit"] in ("step", "rethrow")]
    died = [r for r in rows if r["exit"] == "died"]
    ended = [r for r in rows if r["exit"] == "end"]
    w(f"\nexit reasons: step {sum(1 for r in rows if r['exit']=='step')}  "
      f"rethrow {sum(1 for r in rows if r['exit']=='rethrow')}  "
      f"died {len(died)}  end {len(ended)}\n")

    def by(pred, pop):
        return [r for r in pop if pred(r)]

    for label, pop in (("UNCENSORED (left the tile alive)", moved),
                       ("CENSORED: died on the landing tile", died),
                       ("CENSORED: game ended on the tile", ended)):
        groups = [("all", pop)]
        for side in ("US", "THEM", "UNATTRIB"):
            groups.append((f"thrower {side}", by(lambda r, s=side: r["side"] == s, pop)))
        for rel in ("own", "enemy", "unattrib"):
            groups.append((f"victim {rel} bot", by(lambda r, x=rel: r["rel"] == x, pop)))
        for side in ("US", "THEM"):
            for rel in ("own", "enemy"):
                groups.append((f"{side} throws {rel} bot",
                               by(lambda r, s=side, x=rel: r["side"] == s and r["rel"] == x, pop)))
        table(label, groups)

    # combined view: every throw, censored ones counted at their censoring time
    groups = [("all throws", rows)]
    for side in ("US", "THEM", "UNATTRIB"):
        groups.append((f"thrower {side}", by(lambda r, s=side: r["side"] == s, rows)))
    for side in ("US", "THEM"):
        for rel in ("own", "enemy"):
            groups.append((f"{side} throws {rel} bot",
                           by(lambda r, s=side, x=rel: r["side"] == s and r["rel"] == x, rows)))
    table("ALL THROWS (censored counted at censoring time — lower bound)", groups)

    # death-on-tile fraction per population
    w("\nDEATH-ON-LANDING-TILE FRACTION\n")
    w(f"{'population':32s}{'throws':>9s}{'died on T':>11s}{'pct':>8s}\n")
    pops = [("all", rows)]
    for side in ("US", "THEM", "UNATTRIB"):
        pops.append((f"thrower {side}", by(lambda r, s=side: r["side"] == s, rows)))
    for side in ("US", "THEM"):
        for rel in ("own", "enemy"):
            pops.append((f"{side} throws {rel} bot",
                         by(lambda r, s=side, x=rel: r["side"] == s and r["rel"] == x, rows)))
    for name, pop in pops:
        n = len(pop)
        d = sum(1 for r in pop if r["exit"] == "died")
        w(f"{name:32s}{n:>9d}{d:>11d}{(100.0*d/n if n else 0):>7.1f}%\n")

    # landing-tile occupancy (the cheap sub-question)
    occ = collections.Counter(r["occ"] for r in rows)
    w("\nLANDING-TILE OCCUPANCY at the moment of landing "
      "(entities on T other than the thrown bot)\n")
    for k in sorted(occ):
        w(f"  {k:>3d} other entities: {occ[k]:>8d}  ({100.0*occ[k]/len(rows):.3f}%)\n")
    what = collections.Counter(r.get("occ_what", "-") for r in rows)
    w("  by co-occupant:\n")
    for k, n in what.most_common(15):
        w(f"    {k:<28s}{n:>8d}  ({100.0*n/len(rows):.3f}%)\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\nDETECTION")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan")
    s.add_argument("--files", required=True, help="file with one replay path per line")
    s.add_argument("-j", "--jobs", type=int, default=os.cpu_count())
    s.set_defaults(fn=cmd_scan)
    r = sub.add_parser("report")
    r.add_argument("tsv")
    r.add_argument("--join", default="corpus/join.tsv")
    r.add_argument("--throws", default=None)
    r.set_defaults(fn=cmd_report)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
