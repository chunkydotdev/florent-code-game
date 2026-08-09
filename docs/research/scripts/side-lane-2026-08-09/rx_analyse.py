#!/usr/bin/env python3
"""Per-opponent reaction atlas aggregation (read-only, scratchpad output)."""
from __future__ import annotations

import collections
import csv
import statistics
import sys

SC = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/bdac64c0-51b0-4be3-8d69-70930a125ac4/scratchpad"
RX = SC + "/rx"
US = "OpenSverige"

ATT = {}
for r in csv.DictReader(open(SC + "/attrib2.tsv"), delimiter="\t"):
    ATT[r["file"]] = r


def side(f, t):
    """-> (team_name, version, opp_name) for side t of file f, or None."""
    a = ATT.get(f)
    if a is None:
        return None
    t = int(t)
    if t == 0:
        return a["team0"], a["ver0"], a["team1"]
    return a["team1"], a["ver1"], a["team0"]


def rd(name):
    return csv.DictReader(open(f"{RX}/rx_{name}.tsv"), delimiter="\t")


def med(xs):
    return statistics.median(xs) if xs else None


def pct(a, b):
    return 100.0 * a / b if b else None


VS_US_ONLY = "--all" not in sys.argv

def keep(f, t):
    s = side(f, t)
    if s is None:
        return None
    name, ver, opp = s
    if name == US:
        return None
    if VS_US_ONLY and opp != US:
        return None
    return name, ver


# ------------------------------------------------------------------ 0. sides
sides = collections.Counter()
vers = collections.defaultdict(collections.Counter)
for f, a in ATT.items():
    for t in (0, 1):
        k = keep(f, t)
        if k:
            sides[k[0]] += 1
            vers[k[0]][k[1]] += 1

# ------------------------------------------------------------------ 1. shots
shot = collections.defaultdict(collections.Counter)
for r in rd("shot"):
    k = keep(r["file"], r["team"])
    if not k:
        continue
    c = shot[k[0]]
    sk = r["skind"]
    for col in ("bot_enemy", "bot_own", "empty", "b_own", "b_conveyor",
                "b_splitter", "b_harvester", "b_barrier", "b_gunner",
                "b_sentinel", "b_launcher", "b_core", "oor"):
        c[col] += int(r[col])
        c[sk + "|" + col] += int(r[col])

healshot = collections.defaultdict(collections.Counter)
for r in rd("healshot"):
    k = keep(r["file"], r["team"])
    if not k:
        continue
    healshot[k[0]]["tot"] += int(r["bldg_shots"])
    healshot[k[0]]["healed"] += int(r["bldg_shots_on_healed"])

# ------------------------------------------------------------------ 2. defb
defb = collections.defaultdict(lambda: collections.defaultdict(list))
for r in rd("defb"):
    k = keep(r["file"], r["team"])
    if not k:
        continue
    d = defb[k[0]]
    grp = "turret" if r["kind"] in ("gunner", "sentinel") else "barrier"
    if int(r["rnd"]) < 60:
        grp2 = None            # case-crossover control window not available
    else:
        grp2 = grp
    for g in ("all", grp):
        d[g + "_n"].append(1)
        d[g + "_s20"].append(1 if int(r["s20"]) >= 0 else 0)
        d[g + "_c20"].append(1 if int(r["ctrl20"]) >= 0 else 0)
        if int(r["s20"]) >= 0:
            d[g + "_lat"].append(int(r["rnd"]) - int(r["s20"]))
    if grp2:
        for g in ("all", grp2):
            d[g + "_cc_n"].append(1)
            d[g + "_cc_case"].append(int(r["n13"]))
            d[g + "_cc_ctrl"].append(int(r["pn13"]))
            d[g + "_cc_case32"].append(int(r["n20"]))
            d[g + "_cc_ctrl32"].append(int(r["pn20"]))

# ------------------------------------------------------------------ 3. rot
rot = collections.defaultdict(collections.Counter)
for r in rd("rot"):
    k = keep(r["file"], r["team"])
    if not k:
        continue
    rot[k[0]]["n"] += 1
    if int(r["enemy_near_r"]) >= 0:
        rot[k[0]]["near"] += 1
gunbase = collections.defaultdict(collections.Counter)
for r in rd("gunbase"):
    k = keep(r["file"], r["team"])
    if not k:
        continue
    gunbase[k[0]]["rounds"] += int(r["gun_rounds"])
    gunbase[k[0]]["near"] += int(r["gun_rounds_near"])

# ------------------------------------------------------------------ 4. heal
heal = collections.defaultdict(lambda: dict(n=0, resp=0, lat=[],
                                            mode=collections.Counter()))
for r in rd("heal"):
    k = keep(r["file"], r["team"])
    if not k:
        continue
    h = heal[k[0]]
    h["n"] += 1
    if r["mode"] == "none":
        h["mode"]["none"] += 1
        continue
    h["resp"] += 1
    h["lat"].append(int(r["lat"]))
    h["mode"][r["mode"]] += 1

# ------------------------------------------------------------------ 5. launcher
adj = collections.defaultdict(lambda: dict(n=0, thr=0, lat=[]))
for r in rd("adj"):
    k = keep(r["file"], r["lteam"])
    if not k:
        continue
    a = adj[k[0]]
    a["n"] += 1
    if r["thrown3"] == "1":
        a["thr"] += 1
        a["lat"].append(int(r["lat"]))
tint = collections.defaultdict(list)
for r in rd("tint"):
    k = keep(r["file"], r["team"])
    if not k:
        continue
    tint[k[0]].append(int(r["gap"]))
lstat = collections.defaultdict(lambda: dict(nl=0, nthrow=0, nen=0, nown=0))
for r in rd("lstat"):
    k = keep(r["file"], r["team"])
    if not k:
        continue
    lstat[k[0]]["nl"] += int(r["nlauncher"])
    lstat[k[0]]["nthrow"] += int(r["nthrow_enemy"]) + int(r["nthrow_own"])
    lstat[k[0]]["nen"] += int(r["nthrow_enemy"])
    lstat[k[0]]["nown"] += int(r["nthrow_own"])

# ------------------------------------------------------------------ 6. siege
sh = collections.defaultdict(list)
for r in rd("shooter"):
    k = keep(r["file"], r["team"])
    if not k:
        continue
    sh[k[0]].append((r["file"], r["kind"], int(r["born"]), int(r["died"]),
                     int(r["x"]), int(r["y"]), int(r["first"]), int(r["last"]),
                     int(r["n"]), int(r["ncore"]), int(r["nrounds"])))

siege = {}
for team, rows in sh.items():
    byfile = collections.defaultdict(list)
    for row in rows:
        byfile[row[0]].append(row)
    deaths = repl = 0
    idle = []
    for f, rs in byfile.items():
        for (_f, k, b, d, x, y, fi, la, n, nc, nr) in rs:
            if d >= 0:
                deaths += 1
                if any(b2 > d and b2 - d <= 20 and (x2 - x) ** 2 + (y2 - y) ** 2 <= 25
                       for (_g, k2, b2, d2_, x2, y2, *_r) in rs):
                    repl += 1
                idle.append(d - la)
            else:
                idle.append(nr - 1 - la)
    siege[team] = dict(n=len(rows), deaths=deaths, repl=repl, idle=idle)

# ------------------------------------------------------------------ output
ORDER = ["Ouroboros", "Kings College Munich", "Lunds Stallions", "Memtrace",
         "CtrlAltDefeat", "Powerpuff Girls", "Leviathan", "Orizon",
         "OopsGotYourElo"]
teams = [t for t in ORDER if sides.get(t)]
teams += sorted([t for t in sides if t not in ORDER and sides[t] >= 20],
                key=lambda t: -sides[t])

print(f"# scope: {'vs OpenSverige only' if VS_US_ONLY else 'ALL attributed games'}")
print()
for t in teams:
    c = shot[t]
    tot = sum(c[k] for k in ("bot_enemy", "bot_own", "empty", "b_own",
                             "b_conveyor", "b_splitter", "b_harvester",
                             "b_barrier", "b_gunner", "b_sentinel",
                             "b_launcher", "b_core"))
    bldg = sum(c["b_" + k] for k in ("conveyor", "splitter", "harvester",
                                     "barrier", "gunner", "sentinel",
                                     "launcher", "core"))
    d = defb[t]
    r_ = rot[t]
    gb = gunbase[t]
    h = heal[t]
    a = adj[t]
    s = siege.get(t, dict(n=0, deaths=0, repl=0, idle=[]))
    vv = vers[t]
    print(f"## {t}   sides={sides[t]}  versions={dict(vv)}")
    print(f"  SHOTS n={tot}  bot={pct(c['bot_enemy'],tot)}  "
          f"bldg={pct(bldg,tot)}  empty={pct(c['empty'],tot)}  "
          f"own={pct(c['b_own']+c['bot_own'],tot)}  oor={c['oor']}")
    print("   bldg split: " + " ".join(
        f"{k}={c['b_'+k]}" for k in ("core", "barrier", "conveyor", "splitter",
                                     "harvester", "gunner", "sentinel", "launcher")))
    for sk in ("gunner", "sentinel"):
        st = sum(c[sk + "|" + k] for k in ("bot_enemy", "bot_own", "empty", "b_own",
                                           "b_conveyor", "b_splitter", "b_harvester",
                                           "b_barrier", "b_gunner", "b_sentinel",
                                           "b_launcher", "b_core"))
        sb = sum(c[sk + "|b_" + k] for k in ("conveyor", "splitter", "harvester",
                                             "barrier", "gunner", "sentinel",
                                             "launcher", "core"))
        snc = sb - c[sk + "|b_core"]
        if st:
            print(f"   {sk}: n={st} bot={pct(c[sk+'|bot_enemy'],st):.1f}% "
                  f"bldg={pct(sb,st):.1f}% (non-core {pct(snc,st):.1f}%) "
                  f"empty={pct(c[sk+'|empty'],st):.1f}%")
    hsr = healshot[t]
    print(f"  SHOTS-ON-HEALED-BLDG {hsr['healed']}/{hsr['tot']} = "
          f"{pct(hsr['healed'], hsr['tot'])}")
    for g in ("all", "turret", "barrier"):
        n = len(d[g + "_n"])
        if not n:
            continue
        tr = sum(d[g + "_s20"]) / n
        cr = sum(d[g + "_c20"]) / n
        print(f"  DEFBUILD[{g}] n={n} sighted20={tr*100:.1f}% permctrl={cr*100:.1f}% "
              f"ratio={tr/cr if cr else float('nan'):.2f} "
              f"lat_med={med(d[g+'_lat'])}")
        m = len(d[g + "_cc_n"])
        if m:
            ca = sum(d[g+"_cc_case"])/m; co = sum(d[g+"_cc_ctrl"])/m
            ca32 = sum(d[g+"_cc_case32"])/m; co32 = sum(d[g+"_cc_ctrl32"])/m
            print(f"    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n={m}: "
                  f"d2<=13 {ca:.2f} vs {co:.2f} rr={ca/co if co else float('nan'):.2f} | "
                  f"d2<=32 {ca32:.2f} vs {co32:.2f} rr={ca32/co32 if co32 else float('nan'):.2f}")
    print(f"  ROT n={r_['n']} with_enemy_near(3r,d2<=13)={pct(r_['near'],r_['n'])} "
          f"| baseline gunner-rounds-with-enemy-near="
          f"{pct(gb['near'],gb['rounds'])} (gunner-rounds={gb['rounds']}) "
          f"| rot per 1k gunner-rounds={1000*r_['n']/gb['rounds'] if gb['rounds'] else 0:.1f}")
    print(f"  HEAL trig={h['n']} responded={pct(h['resp'],h['n'])} "
          f"lat_med={med(h['lat'])} lat_p25/75="
          f"{sorted(h['lat'])[len(h['lat'])//4] if h['lat'] else None}/"
          f"{sorted(h['lat'])[3*len(h['lat'])//4] if h['lat'] else None} "
          f"modes={dict(h['mode'])}")
    ti = sorted(tint[t])
    ls = lstat[t]
    print(f"  LAUNCH adj_eps={a['n']} thrown<=3r={pct(a['thr'],a['n'])} "
          f"lat_med={med(a['lat'])} | launchers={ls['nl']} throws={ls['nthrow']}"
          f" (enemy {ls['nen']} / own {ls['nown']}) "
          f"| inter-throw n={len(ti)} min={ti[0] if ti else None} "
          f"p10={ti[len(ti)//10] if ti else None} med={med(ti)}")
    print(f"  SIEGE shooters={s['n']} deaths={s['deaths']} "
          f"replaced<=20r&d2<=25={pct(s['repl'],s['deaths'])} "
          f"idle_after_last_fire_med={med(s['idle'])}")
    print()
