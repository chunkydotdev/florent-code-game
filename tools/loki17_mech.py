#!/usr/bin/env python3
"""LOKI-17 MECHANISM: shootable-on-build, on retained local replays.

    .venv/bin/python tools/loki17_mech.py <bot_dir> [n_seeds]

PREREG-loki17's primary: a sentinel is SHOOTABLE-ON-BUILD if on the round it is
built the nearest ENEMY CORE FOOTPRINT tile is within d^2 <= 32 AND lies on its
actual facing ray. Amendment 1 baseline: 50.4%; target >85%.

Local, unlimited, zero rate-limit, zero rated exposure -- the primary is a
property of OUR OWN placement geometry, so the arena's opponent-behaviour bias
does not reach it. `arena.py` discards replays, so this drives `fcode run
--replay` directly.

Decoding reuses `replay_census.parse_entity` and the three traps loki9_facing.py
already paid for: turn -> update-list -> update -> entity is THREE levels; a
rotate() re-emits placeEntity for an existing id so only the FIRST is a build;
and distance is to the nearest of the four footprint tiles, not the anchor.
"""
import subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN, WIRE_VARINT  # noqa: E402

# ⚠ 0 IS *CENTRE*, NOT NORTH. My first table omitted it and shifted every
# facing one compass step -- and research's own validation had already shown a
# one-step rotation drives the facing/shot match rate to EXACTLY 0.0000. That is
# precisely the 0/287 this tool reported, and I read it as a bot defect, wrote a
# retraction, retired a plank and pre-registered another on it.
# Mapping copied from tools/loki9_facing.py, which is validated at 12,759/12,759
# FireTurret events.
DELTA = {0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
         5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1)}


def decode(path):
    data = path.read_bytes()
    mb = None; turns = []
    for num, wire, val in fields(data):
        if num == 1 and wire == WIRE_LEN and mb is None: mb = val
        elif num == 3 and wire == WIRE_LEN: turns.append(val)
    if mb is None: return []
    cores = {}
    for num, wire, val in fields(mb):
        if num == 4 and wire == WIRE_LEN:
            t, p = 0, None
            for cn, _cw, cv in fields(val):
                if cn == 1: t = cv
                elif cn == 3: p = read_pos(cv)
            if p is not None: cores[t] = p
    if len(cores) < 2: return []
    # ⚠ TEAM NUMBERING DIFFERS BY SOURCE. Locally-generated replays key the map's
    # core entries as teams {1,2}; platform-downloaded replays use {0,1}, while
    # ENTITY.team is 0/1 in both. Keying cores by team id therefore matches
    # nothing on local replays and silently returns zero sentinels -- which is
    # exactly what this tool did on its first three runs, reporting "no
    # sentinels decoded" while a hand decode of the same file found three.
    # Index by SORTED POSITION instead, which is correct under both encodings.
    ordered = [cores[k] for k in sorted(cores)]
    rows = []; seen = set()
    for rnd, tb in enumerate(turns):
        for _n, _w, ub in fields(tb):
            for un, _uw, uv in fields(ub):
                if un != 1: continue
                for en, _ew, ev in fields(uv):
                    if en != 1: continue
                    ent = parse_entity(ev, rnd)
                    if ent is None or ent.kind != "sentinel": continue
                    if ent.id in seen: continue
                    seen.add(ent.id)
                    if ent.team not in (0, 1): continue
                    foe = ordered[1 - ent.team]
                    foot = [(foe[0]+a, foe[1]+b) for a in (0,1) for b in (0,1)]
                    pos = tuple(ent.pos)
                    d2 = min((pos[0]-t[0])**2 + (pos[1]-t[1])**2 for t in foot)
                    d = DELTA.get(ent.direction or 0)
                    ok = False
                    if d and d != (0, 0):
                        dx, dy = d
                        for t in foot:
                            vx, vy = t[0]-pos[0], t[1]-pos[1]
                            if vx*vx + vy*vy > 32: continue
                            if vx*dy - vy*dx != 0: continue
                            if vx*dx + vy*dy <= 0: continue
                            ok = True; break
                    own = ordered[ent.team]
                    ownfoot = [(own[0]+a, own[1]+b) for a in (0,1) for b in (0,1)]
                    d2own = min((pos[0]-t[0])**2 + (pos[1]-t[1])**2 for t in ownfoot)
                    rows.append((ent.team, d2, ok, d2own))
    return rows


def main(argv):
    bot = argv[0]; seeds = int(argv[1]) if len(argv) > 1 else 4
    maps = ["fjordgate", "atoll", "saga", "snowflake", "jackpot"]
    tot = hit = 0; d2s = []
    fwd_tot = fwd_hit = 0                      # forward-sited subset (see below)
    games = 0
    with tempfile.TemporaryDirectory() as td:
        for mp in maps:
            for s in range(seeds):
                out = Path(td) / f"{mp}_{s}.replay26"
                cmd = [str(ROOT/".venv/bin/fcode"), "run", f"bots/{bot}",
                       "bots/_det_opp_v63", f"maps/{mp}.map26",
                       "--replay", str(out), "--seed", str(1000+s)]
                r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
                if not out.exists(): continue
                games += 1
                # ⚠ decode() yields FOUR fields. It yielded three until d2own was
                # added, and main() was never updated -- so this tool raised
                # `ValueError: too many values to unpack` on every invocation and
                # CANNOT have produced any number now in circulation. Found
                # 2026-08-11 by running it. Anything sourced to this tool before
                # that date came from a different code path and must be re-derived.
                for team, d2, ok, d2own in decode(out):
                    if team != 0: continue          # OUR side only (seat A)
                    tot += 1; d2s.append(d2); hit += ok
                    # FORWARD subset: nearer the ENEMY core than our own. The
                    # plank edits `_try_forward_sentinel` only, so this is the
                    # population it can actually move; the headline stays ALL
                    # sentinels because that is the population Amendment 1b's
                    # 50.4% baseline was computed on. Reported, never a bar.
                    if d2 < d2own:
                        fwd_tot += 1; fwd_hit += ok
    if not tot:
        print(f"{bot}: no sentinels decoded -- cannot measure"); return 1
    d2s.sort()
    print(f"{bot}: {hit}/{tot} shootable-on-build = {hit/tot:.1%}   "
          f"median nearest d2 = {d2s[len(d2s)//2]}   ({games} games)")
    if fwd_tot:
        print(f"    forward-sited subset (d2_enemy < d2_own): "
              f"{fwd_hit}/{fwd_tot} = {fwd_hit/fwd_tot:.1%}")
    else:
        print("    forward-sited subset: 0 sentinels -- nothing forward was built")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
