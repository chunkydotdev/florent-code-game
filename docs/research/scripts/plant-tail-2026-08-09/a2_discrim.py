#!/usr/bin/env python3
"""Ranked discriminators for enemy-plant survival, on a CENSORED outcome.

Outcome: alive at +T rounds after the plant, among plants that had >= T rounds
of game left ('at risk at T').  T = 100 and 200.
"""
import csv, collections, math, sys

D = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/tail/"
BASE = "/Users/junghard/Projects/Work/florent-code-game/corpus/"

rows = []
for r in csv.DictReader(open(D + "plants2.tsv"), delimiter="\t"):
    for k in ("our_team", "won", "turns", "lastrnd", "rnd", "x", "y", "d2",
              "died", "drnd", "life", "nb_same8", "nb_sameturret8", "nb_opp8",
              "nb_same16", "nb_opp16", "reuse"):
        r[k] = int(r[k])
    r["fu"] = r["lastrnd"] - r["rnd"]
    rows.append(r)

THEM = [r for r in rows if r["side"] == "THEM"]
US = [r for r in rows if r["side"] == "US"]
print(f"plants THEM={len(THEM)} US={len(US)}  games={len(set(r['file'] for r in rows))}")

# ---- our builder-attack activity per game (build_agg), plus band totals
batk = collections.Counter()       # (file, team) -> batk
batk_band = collections.Counter()  # (file, team, band) -> batk
shots = collections.Counter()
for r in csv.DictReader(open(BASE + "build_agg.tsv"), delimiter="\t"):
    if r["metric"] == "batk":
        batk[(r["file"], r["team"])] += int(r["n"])
        batk_band[(r["file"], r["team"], r["band"])] += int(r["n"])
    elif r["metric"] == "shot":
        shots[(r["file"], r["team"])] += int(r["n"])


def band(rr):
    return "r0-150" if rr < 150 else "r150-200" if rr < 200 else "r200-300" if rr < 300 else "r300+"


for r in rows:
    ourt = str(r["our_team"])
    r["our_batk"] = batk[(r["file"], ourt)]
    r["our_batk_rate"] = r["our_batk"] / max(1, r["lastrnd"])
    r["our_shots"] = shots[(r["file"], ourt)]
    r["batk_after"] = sum(v for (f, t, b), v in ())  # placeholder


def alive_at(r, T):
    return (not r["died"]) or r["life"] > T


def rate(g, T):
    e = [r for r in g if r["fu"] >= T]
    if not e:
        return None, 0
    return sum(1 for r in e if alive_at(r, T)) / len(e), len(e)


def z2p(p1, n1, p2, n2):
    """two-proportion z test -> (diff_pp, z, p)"""
    if n1 == 0 or n2 == 0:
        return None
    p = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return (p1 - p2) * 100, 0.0, 1.0
    z = (p1 - p2) / se
    pv = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return (p1 - p2) * 100, z, pv


print("\n" + "=" * 72)
print("BASELINE: censored survival, THEM plants in OUR band vs US plants in THEIRS")
for T in (25, 50, 100, 200, 400):
    a, na = rate(THEM, T)
    b, nb = rate(US, T)
    print(f"  T={T:3d}  THEM alive {a:6.1%} (n={na:5d})   US alive {b:6.1%} (n={nb:5d})"
          f"   diff {(a-b)*100:+.1f}pp")

for T in (100, 200):
    print("\n" + "=" * 72)
    print(f"### DISCRIMINATORS at T={T} (at-risk THEM plants)")
    pop = [r for r in THEM if r["fu"] >= T]
    base = sum(1 for r in pop if alive_at(r, T)) / len(pop)
    print(f"population n={len(pop)}  games={len(set(r['file'] for r in pop))} "
          f" baseline alive {base:.1%}")

    def show(name, keyfn, minn=40, order=None, top=None):
        g = collections.defaultdict(list)
        for r in pop:
            g[keyfn(r)].append(r)
        items = [(k, v) for k, v in g.items() if len(v) >= minn]
        rows_out = []
        for k, v in items:
            a = sum(1 for r in v if alive_at(r, T)) / len(v)
            gm = len(set(r["file"] for r in v))
            rows_out.append((k, a, len(v), gm))
        if order == "key":
            rows_out.sort(key=lambda t: t[0])
        else:
            rows_out.sort(key=lambda t: -t[1])
        print(f"\n-- {name}")
        for k, a, n, gm in (rows_out[:top] if top else rows_out):
            print(f"   {str(k):28s} alive {a:6.1%}  n={n:5d} games={gm:4d}"
                  f"  ({(a-base)*100:+5.1f}pp)")
        if len(rows_out) >= 2:
            hi, lo = rows_out[0], rows_out[-1]
            d = z2p(hi[1], hi[2], lo[1], lo[2])
            print(f"   spread hi-lo: {d[0]:+.1f}pp  z={d[1]:.2f} p={d[2]:.2element}"
                  if False else
                  f"   spread hi-lo: {d[0]:+.1f}pp  z={d[1]:.2f} p={d[2]:.3g}")
        return rows_out

    show("2. distance d2 (exact ring)", lambda r: r["d2"], minn=60, order="key")
    show("2b. distance bucket", lambda r: ("near d2<=8" if r["d2"] <= 8 else
                                           "mid 9-17" if r["d2"] <= 17 else "far 18-32"),
         order="key")
    show("3. turret type", lambda r: r["kind"])
    show("4. opponent", lambda r: r["opp"], minn=60)
    show("5a. map", lambda r: r["map"], minn=60, top=12)
    show("5b. our seat", lambda r: f"seat{r['our_team']}")
    show("6. our batk in game (quartile-ish)",
         lambda r: ("batk 0" if r["our_batk"] == 0 else
                    "batk 1-49" if r["our_batk"] < 50 else
                    "batk 50-199" if r["our_batk"] < 200 else
                    "batk 200-499" if r["our_batk"] < 500 else "batk 500+"),
         order="key")
    show("7a. enemy buildings within d2<=8 at plant",
         lambda r: min(r["nb_same8"], 6), order="key")
    show("7b. enemy TURRETS within d2<=8 at plant",
         lambda r: min(r["nb_sameturret8"], 4), order="key")
    show("7c. OUR buildings within d2<=8 at plant",
         lambda r: min(r["nb_opp8"], 6), order="key")
    show("8. did we win that game", lambda r: "we WON" if r["won"] else "we LOST")
    show("1b. round built (residual, within at-risk)",
         lambda r: ("r0-99" if r["rnd"] < 100 else "r100-249" if r["rnd"] < 250
                    else "r250-499" if r["rnd"] < 500 else "r500+"), order="key")
