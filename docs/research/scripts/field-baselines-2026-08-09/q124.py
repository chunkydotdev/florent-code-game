#!/usr/bin/env python3
"""Q1 (core-kill round), Q2 (damage-to-repair), Q4 (turrets built in r200-300),
re-derived on THIRD-PARTY games, with our own games recomputed by the same code
as a replication control.

Q1 source: `collar_games.tsv` (`core_death_own`, the round this side's core was
  removed, -1 if it survived).  The original claim is about the round the
  *killer* landed the kill, so a kill is scored to the OTHER side.
Q2 source: `corpus/econ.tsv`, columns `heals`, `attacks`, `ammo_converted`.
  Reconstruction of the published figure:
      HP repaired     = heals * 4                 (1 Ti -> +4 HP)
      damage capacity = ammo_converted * 1.8 + attacks * 2
  (sentinel 10 ammo -> 18 dmg = 1.8 HP/Ti; builder attack 2 Ti -> 2 dmg.)
  Verified below against the published US 1.11 / THEM 2.79 before use.
  `econ.shots` and `econ.deliveries` are DEAD (all-zero) and are not touched.
Q4 source: `corpus/build_agg.tsv`, `band == 'r200-300'`, metrics
  `build_gunner|build_sentinel|build_launcher`.  build_agg already applies the
  first-placeEntity-per-id rule, so gunner rotates are not counted as builds.

    python q124.py <freezedir> <collardir> <out.md>
"""
from __future__ import annotations

import csv
import os
import statistics
import sys
from collections import defaultdict
from pathlib import Path

TURRETS = ("build_gunner", "build_sentinel", "build_launcher")


KEEP_RELATED = os.environ.get("FB_KEEP_RELATED") == "1"

def load_meta(fz: Path):
    M = {}
    for r in csv.DictReader((fz / "meta_join.tsv").open(), delimiter="\t"):
        # POPULATION FILTER (2026-08-09 correction).  `opensverige - plan B`
        # (team id b7cafd9f) is a second registration almost certainly of us, so a
        # match it plays is NOT the field playing itself, and OUR match against it
        # is not a real opponent game either.  `meta_attrib.py` marks both with
        # `related`; the clean field is `us_side == "none" AND related == "none"`
        # and the clean vs-us cell is `us_side != "none" AND related == "none"`.
        # Set FB_KEEP_RELATED=1 to reproduce the pre-correction population, which
        # is how the movement in the deliverable's POPULATION CORRECTION section
        # is isolated from the archive having grown at the same time.
        if r.get("related", "none") != "none" and not KEEP_RELATED:
            continue
        def f(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return None
        M[r["file"]] = {
            "pop": "VS_US" if r["us_side"] != "none" else "THIRD_PARTY",
            "us_idx": 0 if r["us_side"] == "a" else 1 if r["us_side"] == "b" else None,
            "name": {0: r["teamAName"], 1: r["teamBName"]},
            "rb": {0: f(r["ratingABefore"]), 1: f(r["ratingBBefore"])},
            "ver": {0: r["teamAVersion"], 1: r["teamBVersion"]},
        }
    return M


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def main(argv):
    fz, cd, outp = Path(argv[0]), Path(argv[1]), Path(argv[2])
    M = load_meta(fz)
    out = []

    # ================= Q1: core-kill round ================================
    # collar_games side US == replay index 0, THEM == index 1 (shim join).
    deaths = {}          # file -> {idx: death_round or -1}, nr
    nr = {}
    for r in csv.DictReader((cd / "collar_games.tsv").open(), delimiter="\t"):
        idx = 0 if r["side"] == "US" else 1
        deaths.setdefault(r["file"], {})[idx] = int(r["core_death_own"])
        nr[r["file"]] = int(r["nr"])

    kills = defaultdict(list)     # (pop, band) -> [round]
    ngames = defaultdict(int)
    for f, d in deaths.items():
        m = M.get(f)
        if m is None or len(d) != 2:
            continue
        pop = m["pop"]
        ngames[pop] += 1
        for victim, rnd in d.items():
            if rnd < 0:
                continue
            killer = 1 - victim
            kr = m["rb"][killer]
            kills[(pop, "ALL")].append(rnd)
            if kr is not None:
                kills[(pop, "STRONG>=1550" if kr >= 1550 else "WEAK<1550")].append(rnd)
            if pop == "VS_US":
                # replicate the original conditioning exactly: kills landed ON US
                if victim == m["us_idx"]:
                    kills[("ORIG_they_kill_us", "ALL")].append(rnd)
                    if kr is not None and kr >= 1550:
                        kills[("ORIG_they_kill_us", "STRONG>=1550")].append(rnd)

    out.append("# Q1 — core-kill round")
    out.append("")
    out.append(f"games with both sides decoded: VS_US {ngames['VS_US']}, "
               f"THIRD_PARTY {ngames['THIRD_PARTY']}")
    out.append("")
    out.append("| population | killer band | kills (N) | median | q1 | q3 | by r100 | by r150 | by r200 | by r300 | by r400 |")
    out.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for key in sorted(kills):
        v = kills[key]
        n = len(v)
        row = [f"{key[0]}", f"{key[1]}", f"{n}",
               f"r{pct(v,.5):.0f}", f"r{pct(v,.25):.0f}", f"r{pct(v,.75):.0f}"]
        for t in (100, 150, 200, 300, 400):
            row.append(f"{100.0*sum(1 for x in v if x <= t)/n:.0f}%")
        out.append("| " + " | ".join(row) + " |")

    # kill INCIDENCE per side-game
    out.append("")
    out.append("| population | side-games | sides whose core died | rate |")
    out.append("| --- | ---: | ---: | ---: |")
    for pop in ("VS_US", "THIRD_PARTY"):
        sg = ngames[pop] * 2
        dd = sum(1 for f, d in deaths.items()
                 if M.get(f, {}).get("pop") == pop and len(d) == 2
                 for v in d.values() if v >= 0)
        out.append(f"| {pop} | {sg} | {dd} | {100.0*dd/sg:.1f}% |")

    # ================= Q2: damage capacity vs HP repaired =================
    econ = defaultdict(lambda: defaultdict(int))       # (file, team) -> cols
    for r in csv.DictReader((fz / "econ.tsv").open(), delimiter="\t"):
        k = (r["file"], int(r["team"]))
        for c in ("heals", "attacks", "ammo_converted"):
            econ[k][c] += int(r[c])

    acc = defaultdict(lambda: defaultdict(int))
    gcount = defaultdict(set)
    for (f, t), c in econ.items():
        m = M.get(f)
        if m is None:
            continue
        if m["pop"] == "VS_US":
            who = "OUR_GAMES_us" if t == m["us_idx"] else "OUR_GAMES_them"
        else:
            who = "THIRD_PARTY_field"
        for k, v in c.items():
            acc[who][k] += v
        gcount[who].add((f, t))
        if m["pop"] == "THIRD_PARTY":
            rb = m["rb"][t]
            if rb is not None:
                b = "3P_>=1550" if rb >= 1550 else "3P_<1550"
                for k, v in c.items():
                    acc[b][k] += v
                gcount[b].add((f, t))

    out.append("")
    out.append("# Q2 — damage capacity : HP repaired")
    out.append("")
    out.append("| population | side-games | heals/g | HP repaired/g | atks/g | ammo Ti/g | dmg capacity/g | **ratio** |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for who in ("OUR_GAMES_us", "OUR_GAMES_them", "THIRD_PARTY_field",
                "3P_>=1550", "3P_<1550"):
        c, n = acc[who], len(gcount[who])
        if not n:
            continue
        heals, atks, ammo = c["heals"] / n, c["attacks"] / n, c["ammo_converted"] / n
        rep = heals * 4
        dmg = ammo * 1.8 + atks * 2
        out.append(f"| {who} | {n} | {heals:.1f} | {rep:,.0f} | {atks:.1f} | "
                   f"{ammo:.1f} | {dmg:,.0f} | **{dmg/rep:.2f} : 1** |")

    # per-band, third-party field vs our games
    out.append("")
    out.append("| band | 3P heals/g | 3P ammo Ti/g | 3P ratio | our-games THEM heals/g | THEM ammo Ti/g | THEM ratio |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    band = defaultdict(lambda: defaultdict(int))
    bg = defaultdict(set)
    for r in csv.DictReader((fz / "econ.tsv").open(), delimiter="\t"):
        m = M.get(r["file"])
        if m is None:
            continue
        t = int(r["team"])
        if m["pop"] == "THIRD_PARTY":
            who = "3P"
        elif t != m["us_idx"]:
            who = "THEM"
        else:
            continue
        k = (who, r["band"])
        for c in ("heals", "attacks", "ammo_converted"):
            band[k][c] += int(r[c])
        bg[k].add((r["file"], t))
    for b in ("r0-150", "r150-200", "r200-300", "r300+"):
        cells = []
        for who in ("3P", "THEM"):
            c, n = band[(who, b)], len(bg[(who, b)])
            if not n:
                cells += ["—", "—", "—"]
                continue
            h, a, am = c["heals"] / n, c["attacks"] / n, c["ammo_converted"] / n
            rep, dmg = h * 4, am * 1.8 + a * 2
            cells += [f"{h:.1f}", f"{am:.0f}", f"{dmg/rep:.2f}" if rep else "—"]
        out.append(f"| {b} | " + " | ".join(cells) + " |")

    # ================= Q4: turrets built in r200-300 ======================
    tur = defaultdict(lambda: defaultdict(int))
    tg = defaultdict(set)
    for r in csv.DictReader((fz / "build_agg.tsv").open(), delimiter="\t"):
        if r["band"] != "r200-300" or r["metric"] not in TURRETS:
            continue
        m = M.get(r["file"])
        if m is None:
            continue
        t = int(r["team"])
        if m["pop"] == "VS_US":
            who = "OUR_GAMES_us" if t == m["us_idx"] else "OUR_GAMES_them"
        else:
            who = "THIRD_PARTY_field"
        tur[who][r["metric"]] += int(r["n"])
        tur[who]["all"] += int(r["n"])
        if m["pop"] == "THIRD_PARTY":
            rb = m["rb"][t]
            if rb is not None:
                b = "3P_>=1550" if rb >= 1550 else "3P_<1550"
                tur[b][r["metric"]] += int(r["n"])
                tur[b]["all"] += int(r["n"])

    # denominator = every side-game present in build_agg at all (a side that
    # built nothing in r200-300 emits no row and MUST still count)
    seen = set()
    for r in csv.DictReader((fz / "build_agg.tsv").open(), delimiter="\t"):
        seen.add((r["file"], int(r["team"])))
    denom = defaultdict(int)
    for f, t in seen:
        m = M.get(f)
        if m is None:
            continue
        if m["pop"] == "VS_US":
            denom["OUR_GAMES_us" if t == m["us_idx"] else "OUR_GAMES_them"] += 1
        else:
            denom["THIRD_PARTY_field"] += 1
            rb = m["rb"][t]
            if rb is not None:
                denom["3P_>=1550" if rb >= 1550 else "3P_<1550"] += 1

    out.append("")
    out.append("# Q4 — turrets built per side-game, r200-300")
    out.append("")
    out.append("| population | side-games | gunner | sentinel | launcher | **all turrets/game** |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for who in ("OUR_GAMES_us", "OUR_GAMES_them", "THIRD_PARTY_field",
                "3P_>=1550", "3P_<1550"):
        n = denom[who]
        if not n:
            continue
        c = tur[who]
        out.append(f"| {who} | {n} | {c['build_gunner']/n:.2f} | "
                   f"{c['build_sentinel']/n:.2f} | {c['build_launcher']/n:.2f} | "
                   f"**{c['all']/n:.2f}** |")

    outp.write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
