#!/usr/bin/env python3
"""s51 DOUBLE-FERRY timing-probe parser.

Reads a game's .err (DF stderr tags) + .out (fcode summary) and emits one TSV
row.  DRIVEN BOTH WAYS on synthetic fixtures (fixture.py): a parser that has
only ever reported an arrival has not been seen to report a NON-arrival, and
"never arrived" must come out as -1, never as round 0.

Columns
  game        <map>-s<seed>-<seat>
  outcome     win | loss
  cond        core_destroyed | r1000 | other
  end_r       last round the engine reported
  b1_*/b2_*   spawn / ring / adj / last-seen round for the FIRST body appointed
              to that channel  (-1 = never)
  b*_alive10  1 if that body still emitted a POS line at ring+10 (or the game
              ended first with it alive), 0 if it was gone, -1 if it never
              arrived
  b*_throws   ferry throws that body rode
  b*_repl     later bodies appointed to the same channel (replacements)
  gap         b2_ring - b1_ring  (-1 if either never arrived)
  links       relay launchers built
  link2       relay launchers that threw BOTH bodies
  link_ti     titanium spent on relay launchers (sum of the logged cost)
  scale_lo/hi min / max get_scale_percent seen on a link event
  muster      rounds the lead waited for its crew mate
"""
import os
import re
import sys

W = re.compile(r"\s+")


def _toks(line):
    return W.split(line.strip())


def _kv(t):
    """DF lines are `DF TAG <rnd> k v k v ...` -- return (tag, rnd, dict)."""
    d = {}
    for i in range(3, len(t) - 1, 2):
        d[t[i]] = t[i + 1]
    return t[1], int(t[2]), d


def parse_err(path):
    bodies = {}        # body no -> list of per-entity dicts, in appointment order
    links = {}         # launcher id -> dict
    muster = 0
    dead = {}          # entity id -> round
    degrade = {}
    last_rnd = -1
    with open(path, errors="replace") as fh:
        for line in fh:
            if not line.startswith("DF "):
                continue
            t = _toks(line)
            if len(t) < 3:
                continue
            try:
                tag, rnd, d = _kv(t)
            except (ValueError, IndexError):
                continue
            last_rnd = max(last_rnd, rnd)
            if tag == "SPAWN":
                b = int(d["body"])
                bodies.setdefault(b, []).append(
                    {"id": int(d["id"]), "spawn": rnd, "ring": -1, "adj": -1,
                     "last": rnd, "throws": 0})
            elif tag == "POS":
                b, eid = int(d["body"]), int(d["id"])
                for e in bodies.get(b, ()):
                    if e["id"] == eid:
                        e["last"] = max(e["last"], rnd)
                        break
            elif tag == "ARRIVE":
                b, eid = int(d["body"]), int(d["id"])
                what = t[-1]           # 'ring' or 'adj' -- a bare trailing word
                for e in bodies.get(b, ()):
                    if e["id"] == eid:
                        if what == "ring" and e["ring"] < 0:
                            e["ring"] = rnd
                        elif what == "adj" and e["adj"] < 0:
                            e["adj"] = rnd
                        break
            elif tag == "MUSTER":
                muster += 1
            elif tag == "DEAD":
                dead[int(d["id"])] = rnd
            elif tag == "DEGRADE":
                degrade[int(d["id"])] = rnd
            elif tag == "HOPBUILD":
                pass
            elif tag == "THROW":
                lid, bid = int(d["launcher"]), int(d["body"])
                lk = links.setdefault(lid, {"built": -1, "throws": 0,
                                            "cost": 0, "tear": -1,
                                            "scales": []})
                lk["throws"] = max(lk["throws"], int(d.get("n", 1)))
                lk["scales"].append(int(d.get("scale", -1)))
                for lst in bodies.values():
                    for e in lst:
                        if e["id"] == bid:
                            e["throws"] += 1
            elif tag == "TEARDOWN":
                lid = int(d["launcher"])
                lk = links.setdefault(lid, {"built": -1, "throws": 0,
                                            "cost": 0, "tear": -1,
                                            "scales": []})
                lk["tear"] = rnd
                lk["scales"].append(int(d.get("scale", -1)))
    # a second pass is not needed for HOPBUILD costs: re-read cheaply
    costs, builds = [], []
    with open(path, errors="replace") as fh:
        for line in fh:
            if not line.startswith("DF HOPBUILD "):
                continue
            t = _toks(line)
            tag, rnd, d = _kv(t)
            costs.append(int(d.get("cost", 0)))
            builds.append(rnd)
    return {"bodies": bodies, "links": links, "muster": muster, "dead": dead,
            "degrade": degrade, "last": last_rnd, "costs": costs,
            "builds": builds}


def parse_out(path, arm):
    outcome, cond, end_r = "?", "other", -1
    if not os.path.exists(path):
        return outcome, cond, end_r
    txt = open(path, errors="replace").read()
    m = re.search(r"Winner:\s+(\S+)\s+\((.*?),\s*turn\s+(\d+)\)", txt)
    if m:
        outcome = "win" if m.group(1) == arm else "loss"
        why, end_r = m.group(2), int(m.group(3))
        cond = ("r1000" if "tiebreak" in why.lower()
                else "core_destroyed" if "core" in why.lower() else "other")
    return outcome, cond, end_r


def row(err, out, arm, game):
    g = parse_err(err)
    outcome, cond, end_r = parse_out(out, arm)
    if end_r < 0:
        end_r = g["last"]
    cells = [game, outcome, cond, str(end_r)]
    rings = {}
    for b in (1, 2):
        lst = g["bodies"].get(b, [])
        if not lst:
            cells += ["-1", "-1", "-1", "-1", "-1", "0", "0"]
            rings[b] = -1
            continue
        e = lst[0]
        rings[b] = e["ring"]
        if e["ring"] < 0:
            alive10 = -1
        else:
            want = e["ring"] + 10
            alive10 = 1 if (e["last"] >= want or end_r < want) else 0
        cells += [str(e["spawn"]), str(e["ring"]), str(e["adj"]),
                  str(e["last"]), str(alive10), str(e["throws"]),
                  str(len(lst) - 1)]
    gap = (rings[2] - rings[1]) if (rings[1] >= 0 and rings[2] >= 0) else -999
    links = g["links"]
    scales = [s for lk in links.values() for s in lk["scales"] if s >= 0]
    cells += [str(gap), str(len(g["builds"])),
              str(sum(1 for lk in links.values() if lk["throws"] >= 2)),
              str(sum(g["costs"])),
              str(min(scales) if scales else -1),
              str(max(scales) if scales else -1),
              str(g["muster"])]
    return cells


HDR = ("game outcome cond end_r "
       "b1_spawn b1_ring b1_adj b1_last b1_alive10 b1_throws b1_repl "
       "b2_spawn b2_ring b2_adj b2_last b2_alive10 b2_throws b2_repl "
       "gap links link2 link_ti scale_lo scale_hi muster").split()


def main(argv):
    d = argv[1]
    arm = argv[2] if len(argv) > 2 else "v513_dblferry"
    print("\t".join(HDR))
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".err"):
            continue
        err = os.path.join(d, fn)
        out = err[:-4] + ".out"
        print("\t".join(row(err, out, arm, fn[:-4])))


if __name__ == "__main__":
    main(sys.argv)
