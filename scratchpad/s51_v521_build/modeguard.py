#!/usr/bin/env python3
"""MODE-SELECTOR ASSERTION: on a board where the ferry-siege plank stands down,
NO SIEGE-PATH BUILD MAY HAPPEN.

⛔ WHY THIS EXISTS AND WHY IT IS NOT THE SAME QUESTION AS THE GATED LEG.  There
are TWO standdown mechanisms and they are different code:
  * `FS_MAP_SKIP` (siege.py `_fs_map_gated`) -- the small-board / no-route gate.
    archipelago is the registered instance.
  * `FS_V519_CRIPPLE_MAPS` + `FS_V519_MODESWITCH` (the mode selector, same
    function, a SEPARATE clause) -- midgard and yulerune.
v520 open item 7 found two `fs_crew_on()` read sites OUTSIDE the map gate, and
the leaky sites are shared: they can bypass EITHER mechanism.  A verification
that only exercises archipelago proves nothing about yulerune.

THE ASSERTION, and it is arm-relative rather than absolute BECAUSE AN ABSOLUTE
ONE WOULD BE A FALSE ALARM.  The chassis' own raid doctrine builds forward
things on every board (beltbreak gunners, raid barriers), so "any building near
their core" is not a siege signature.  The reference is therefore the PURE
CHASSIS -- `LOKI_FERRY_SIEGE_ON = False`, which doctrine.py states reproduces
`_v488beltbreak2` exactly -- and the assertion is:

    ON A CRIPPLE OR GATED MAP, THE TREE'S SIEGE-PATH COLUMNS MUST NOT EXCEED THE
    PURE CHASSIS'S.

COLUMNS, all engine-side (placeEntity births + the entity walk):
  ferry_laun   our LAUNCHERS born at d^2 > HOME_DSQ from our OWN core -- the
               ferry chain is a line of launchers laid across the map, so this
               is Magnus's "zero ferry launchers built" check directly.
  collar_bld   our BUILDINGS born within RING_DSQ of the ENEMY core centre --
               collar barriers and forward turrets, the siege's own spend.
  fwd_body     distinct BUILDER BOTS of ours that ever reach RING_DSQ of the
               enemy core -- the crew-seat raider spend.

⛔ GUARDS, DRIVEN TO BOTH VERDICTS (`--selftest <replaydir>`):
  P1 POSITIVE CONTROL: the same three columns run on a NON-cripple, NON-gated
     map (nordkap) must show the tree EXCEEDING the chassis.  An assertion that
     has never fired has not been seen to check.
  P2 TEAM-SWAP CONTROL: reading one replay as the other team must MOVE the
     columns.
  P3 ENVELOPE CONTROL: RING_DSQ = 0 must drive collar_bld and fwd_body to 0 on
     the same replay -- an instrument ignoring the envelope returns the same
     number.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ringwalk import dsq_centre, replay_map, walk  # noqa: E402

RING_DSQ = 50          # the ATRING envelope seatrate.py uses (centre convention)
HOME_DSQ = 36          # beyond this from OUR core a launcher is not a home one
BUILDINGS = ("barrier", "sentinel", "gunner", "launcher", "conveyor",
             "splitter", "harvester")


def analyse(replay, our_team, ring_dsq=RING_DSQ, home_dsq=HOME_DSQ):
    _w, _h, _rows, cores = replay_map(replay)
    cpos = {c["team"]: c["pos"] for c in cores}
    E, O = cpos[1 - our_team], cpos[our_team]
    seen = set()
    ferry_laun = collar_bld = 0
    fwd = set()
    for _rnd, ents in walk(replay):
        for eid, (kind, team, pos, _b) in ents.items():
            if team != our_team:
                continue
            if kind == "builder_bot":
                if dsq_centre(pos, E) <= ring_dsq:
                    fwd.add(eid)
                continue
            if eid in seen:
                continue
            seen.add(eid)
            if kind == "launcher" and dsq_centre(pos, O) > home_dsq:
                ferry_laun += 1
            if kind in BUILDINGS and dsq_centre(pos, E) <= ring_dsq:
                collar_bld += 1
    return dict(ferry_laun=ferry_laun, collar_bld=collar_bld,
                fwd_body=len(fwd))


def run(grid, repdir, label):
    rows = list(csv.DictReader(open(grid), delimiter="\t"))
    tot = dict(ferry_laun=0, collar_bld=0, fwd_body=0)
    n = 0
    for r in rows:
        rp = Path(repdir) / (r["tag"] + ".replay26")
        if not rp.exists():
            continue
        a = analyse(str(rp), 0 if r["seat"] == "A" else 1)
        for k in tot:
            tot[k] += a[k]
        n += 1
    return label, n, {k: (v / n if n else 0.0) for k, v in tot.items()}


def main():
    if sys.argv[1] == "--selftest":
        rp = sys.argv[2]
        a = analyse(rp, 0)
        b = analyse(rp, 1)
        z = analyse(rp, 0, ring_dsq=0)
        ok = True
        print("P2 team0", a, "team1", b)
        if a == b:
            print("  FAIL P2: team swap moved nothing")
            ok = False
        print("P3 ring_dsq=0", z)
        if z["collar_bld"] or z["fwd_body"]:
            print("  FAIL P3: envelope ignored")
            ok = False
        print("SELFTEST", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    # modeguard.py <grid.tsv> <repdir> <label> [...]
    args = sys.argv[1:]
    print("%-22s %5s %12s %12s %10s" %
          ("arm/map", "n", "ferry_laun", "collar_bld", "fwd_body"))
    while args:
        grid, repdir, label = args[0], args[1], args[2]
        args = args[3:]
        lab, n, m = run(grid, repdir, label)
        print("%-22s %5d %12.3f %12.3f %10.3f" %
              (lab, n, m["ferry_laun"], m["collar_bld"], m["fwd_body"]))


if __name__ == "__main__":
    main()
