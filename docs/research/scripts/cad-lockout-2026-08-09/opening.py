#!/usr/bin/env python3
"""Second question: are CAD's r6 launcher self-destruct and r4 ammo dump
map-independent invariants, or nordkap-specific?

The trap here is that CAD churns versions and the maps are not played uniformly
by every version, so a "map effect" can be a version effect wearing a map's
coat.  Everything below is therefore cross-tabbed map x version before any
map-independence claim is made.

The r6 removal is also conditioned on a launcher EXISTING: a map where CAD never
builds a launcher cannot show a launcher self-destruct, and scoring that as
"invariant absent" would be wrong.

Usage: opening.py <freeze_dir>
"""
from __future__ import annotations

import collections
import statistics
import sys

sys.path.insert(0, "docs/research/scripts/cad-lockout-2026-08-09")
from analyse import summarise, win, i  # noqa: E402


def main(d):
    games = summarise(d)
    P = sys.stdout.write

    P("# CAD opening invariants: r6 launcher self-destruct, r4 ammo dump\n\n")

    bymap = collections.defaultdict(list)
    for f, g in games.items():
        bymap[g["mapname"]].append(f)

    P("## Per map, conditioned on a launcher existing\n")
    P(f"{'map':14s} {'dims':>7s} {'n':>4s} {'lnc built r0-5':>15s} "
      f"{'removed r6 nodmg':>17s} {'of those w/ lnc':>16s} "
      f"{'r4 dump':>8s} {'med dump':>9s}\n")
    dump_maps, nodump_maps = [], []
    for m in sorted(bymap):
        fs = bymap[m]
        dims = games[fs[0]]["out"]["mw"] + "x" + games[fs[0]]["out"]["mh"]
        haslnc = rem6 = rem6_c = dump = 0
        amts = []
        for f in fs:
            rs = games[f]["rs"]
            byr = {i(r, "rnd"): r for r in rs}
            lnc = max(i(r, "cad_launchers") for r in rs[:6])
            if lnc > 0:
                haslnc += 1
            if "nodmg" in byr.get(6, {"cad_lnc_gone": "-"})["cad_lnc_gone"]:
                rem6 += 1
                if lnc > 0:
                    rem6_c += 1
            a = win(rs, 4, 4, "cad_convert")
            if a >= 100:
                dump += 1
                amts.append(a)
        P(f"{m[:14]:14s} {dims:>7s} {len(fs):>4d} {haslnc:>15d} {rem6:>17d} "
          f"{f'{rem6_c}/{haslnc}':>16s} {dump:>8d} "
          f"{statistics.median(amts) if amts else '-':>9}\n")
        (dump_maps if dump > len(fs) / 2 else nodump_maps).append(m)

    P(f"\nmaps that ALWAYS dump: {', '.join(dump_maps)}\n")
    P(f"maps that NEVER dump:  {', '.join(nodump_maps)}\n")

    P("\n## Is the dump a MAP effect or a VERSION effect? (cross-tab)\n")
    P("rows = map, cols = CAD version, cell = dumped/played\n\n")
    vers = sorted({g["pop"]["cad_ver"] for g in games.values()}, key=int)
    P(f"{'map':14s} " + " ".join(f"{'v'+v:>8s}" for v in vers) + "\n")
    for m in sorted(bymap):
        cells = []
        for v in vers:
            fs = [f for f in bymap[m] if games[f]["pop"]["cad_ver"] == v]
            if not fs:
                cells.append(f"{'.':>8s}")
                continue
            dd = sum(1 for f in fs if win(games[f]["rs"], 4, 4, "cad_convert") >= 100)
            cells.append(f"{f'{dd}/{len(fs)}':>8s}")
        P(f"{m[:14]:14s} " + " ".join(cells) + "\n")

    P("\n## What separates the dumping maps? core-to-core distance\n")
    P(f"{'map':14s} {'dims':>7s} {'dumps':>6s}\n")
    for m in sorted(bymap):
        fs = bymap[m]
        dims = games[fs[0]]["out"]["mw"] + "x" + games[fs[0]]["out"]["mh"]
        dd = sum(1 for f in fs if win(games[f]["rs"], 4, 4, "cad_convert") >= 100)
        P(f"{m[:14]:14s} {dims:>7s} {f'{dd}/{len(fs)}':>6s}\n")

    P("\n## r6 launcher removal: pooled, and by version\n")
    for v in vers:
        fs = [f for f, g in games.items() if g["pop"]["cad_ver"] == v]
        haslnc = sum(1 for f in fs
                     if max(i(r, "cad_launchers") for r in games[f]["rs"][:6]) > 0)
        rem = 0
        for f in fs:
            byr = {i(r, "rnd"): r for r in games[f]["rs"]}
            if "nodmg" in byr.get(6, {"cad_lnc_gone": "-"})["cad_lnc_gone"]:
                rem += 1
        P(f"  v{v}: n={len(fs):3d}  launcher up by r5 in {haslnc:3d}  "
          f"removed nodmg at r6 in {rem:3d}\n")

    P("\n## Ammo left standing after the dump (the 'poverty window' claim)\n")
    P("CAD titanium at r6-r13, dumping maps vs non-dumping maps\n")
    for label, ms in (("dump maps", dump_maps), ("no-dump maps", nodump_maps)):
        tis, ammos = [], []
        for m in ms:
            for f in bymap[m]:
                rs = [r for r in games[f]["rs"] if 6 <= i(r, "rnd") <= 13]
                if rs:
                    tis.append(statistics.median(i(r, "cad_ti") for r in rs))
                    ammos.append(statistics.median(i(r, "cad_ammo") for r in rs))
        P(f"  {label:14s} n={len(tis):3d}  median Ti {statistics.median(tis):5.0f}"
          f"   median ammo {statistics.median(ammos):5.0f}\n")


if __name__ == "__main__":
    main(sys.argv[1])
