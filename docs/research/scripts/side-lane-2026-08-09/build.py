#!/usr/bin/env python3
"""Build per-game dataset for the drain-pump discriminator cuts. Read-only."""
import collections, csv, json, os

SC = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/bdac64c0-51b0-4be3-8d69-70930a125ac4/scratchpad"
RX = SC + "/rx"
OUT = SC + "/drain-cut"
REPO = "/Users/junghard/Projects/Work/florent-code-game"
US = {"OpenSverige", "opensverige - plan B"}

def iv(d, k):
    v = d.get(k, "")
    return int(v) if v not in ("", None) else 0


def rd(p, **kw):
    return csv.DictReader(open(p), delimiter="\t", **kw)

# ---- attribution -------------------------------------------------------
ATT = {r["file"]: r for r in rd(SC + "/attrib2.tsv")}
GAMES = {r["file"]: r for r in rd(SC + "/games.tsv")}

# ---- ratings from league_matches (match id -> per-team pre rating) ------
RAT = {}
for r in rd(REPO + "/corpus/league_matches.tsv"):
    try:
        RAT[r["id"]] = (r["teamAName"], float(r["ratingABefore"]),
                        r["teamBName"], float(r["ratingBBefore"]))
    except Exception:
        pass

# ---- shots (rx_shot): per (file, team) class counts ---------------------
CLS = ["bot_enemy", "bot_own", "empty", "b_own", "b_conveyor", "b_splitter",
       "b_harvester", "b_barrier", "b_gunner", "b_sentinel", "b_launcher",
       "b_core"]
shot = collections.defaultdict(lambda: collections.Counter())
for r in rd(RX + "/rx_shot.tsv"):
    k = (r["file"], int(r["team"]))
    for c in CLS:
        shot[k][c] += int(r[c])
    shot[k]["_kind_" + r["skind"]] += sum(int(r[c]) for c in CLS)

# ---- rx_tgt: per (file, shooter team) non-core / healed breakdown -------
CHEAP = {"conveyor", "splitter", "barrier"}
tgt = collections.defaultdict(lambda: collections.Counter())
for r in rd(RX + "/rx_tgt.tsv"):
    k = (r["file"], int(r["team"]))
    n, nh, kind = int(r["nshots"]), int(r["nshots_healed"]), r["kind"]
    tgt[k]["all"] += n
    tgt[k]["all_h"] += nh
    if kind != "core":
        tgt[k]["nc"] += n
        tgt[k]["nc_h"] += nh
        tgt[k]["nc_bldgs"] += 1
        if kind in CHEAP:
            tgt[k]["cheap"] += n
            tgt[k]["cheap_h"] += nh
    else:
        tgt[k]["core"] += n
        tgt[k]["core_h"] += nh

# ---- tl finals ---------------------------------------------------------
tl = {}
for r in rd(OUT + "/tl_final.tsv"):
    tl[(r["file"], int(r["team"]))] = r

# ---- assemble ----------------------------------------------------------
rows = []
for f, a in ATT.items():
    g = GAMES.get(f)
    if not g:
        continue
    names = [a["team0"], a["team1"]]
    ours = [i for i in (0, 1) if names[i] in US]
    if len(ours) != 1:
        continue                      # mirror or not ours
    u = ours[0]
    o = 1 - u
    opp = names[o]
    w = int(g["winner"])
    if w not in (0, 1):
        continue
    rounds = int(g["rounds"])
    if rounds < 50:
        continue
    s_o = shot.get((f, o))
    s_u = shot.get((f, u))
    if s_o is None:
        continue
    tot_o = sum(s_o[c] for c in CLS)
    if tot_o < 20:                    # need shots to define a share
        continue
    t_o = tgt.get((f, o), collections.Counter())
    nc = sum(s_o["b_" + k] for k in ("conveyor", "splitter", "harvester",
                                     "barrier", "gunner", "sentinel",
                                     "launcher"))
    cheap = sum(s_o["b_" + k] for k in ("conveyor", "splitter", "barrier"))
    tlu = tl.get((f, u), {})
    tlo = tl.get((f, o), {})
    m = RAT.get(a["match"])
    rat_o = rat_u = None
    if m:
        an, ar, bn, br = m
        # teamA == replay team 0 (atlas-reconciled)
        rr = {0: ar, 1: br}
        rat_o, rat_u = rr[o], rr[u]
    rows.append(dict(
        file=f, opp=opp, oppver=a["ver1"] if o == 1 else a["ver0"],
        usver=a["ver1"] if u == 1 else a["ver0"],
        us_idx=u, win=1 if w == u else 0, rounds=rounds,
        wincond=g["wincond"],
        e_shots=tot_o, e_spr=tot_o / rounds,
        e_nc=nc, e_nc_h=t_o["nc_h"], e_cheap=cheap, e_cheap_h=t_o["cheap_h"],
        e_core=s_o["b_core"], e_bot=s_o["bot_enemy"], e_empty=s_o["empty"],
        e_own=s_o["b_own"],
        tgt_nc=t_o["nc"],
        abs_nc=nc / tot_o, abs_cheap=cheap / tot_o,
        abs_nch=t_o["nc_h"] / tot_o, abs_cheaph=t_o["cheap_h"] / tot_o,
        us_shots=sum(s_u[c] for c in CLS) if s_u else 0,
        e_ticoll=iv(tlo, "ti_coll"), u_ticoll=iv(tlu, "ti_coll"),
        e_tur=iv(tlo, "turbuilds"), u_tur=iv(tlu, "turbuilds"),
        e_batk=iv(tlo, "batk"),
        rat_o=rat_o, rat_u=rat_u,
    ))

hdr = list(rows[0].keys())
with open(OUT + "/games_us.tsv", "w") as fh:
    fh.write("\t".join(hdr) + "\n")
    for r in rows:
        fh.write("\t".join("" if r[c] is None else str(r[c]) for c in hdr) + "\n")

print("games:", len(rows))
c = collections.Counter(r["opp"] for r in rows)
for k, v in c.most_common(30):
    print(f"  {k:32s} {v:4d}")
# reconciliation: rx_shot non-core vs rx_tgt non-core
bad = sum(1 for r in rows if r["e_nc"] != r["tgt_nc"])
print("rx_shot vs rx_tgt non-core mismatch rows:", bad, "/", len(rows))
