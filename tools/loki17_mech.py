#!/usr/bin/env python3
"""LOKI-17 MECHANISM: shootable-on-build, on retained local replays.

    .venv/bin/python tools/loki17_mech.py <bot_dir> [n_seeds]

⛔ THE PLANK THIS TOOL WAS BUILT FOR IS DEAD (c91c078, 2026-08-10 22:03:
"No defect; LOKI-17 and LOKI-18 both dead"). KEEP READING BEFORE REUSING ANY
NUMBER IT PRINTS -- the tool is fine, the METRIC was the wrong instrument, and
the distinction is the whole lesson:

  `raid.py` gates EVERY sentinel build behind `can_fire_from(...)`, and
  LOKI-17 did not touch that guard. So shootable-on-build reads ~100% in the
  CONTROL arm too. The metric sits causally DOWNSTREAM OF AN UNCHANGED GUARD,
  which means no possible result was informative -- not a bar that was
  pre-satisfied, but a bar that could not move. Confirmed twice independently
  on 2026-08-11: by reading (side lane) and by running this tool on both arms
  (builder: forward subset 16/16 and 20/20, 100% in each).
  ⇒ GENERAL RULE, and it is cheap to apply: before pre-registering a mechanism
    metric, ask what in the DIFF can change it. If the answer is nothing, the
    leg spends a window to learn nothing.

⛔ AND DO NOT COMPARE ITS OUTPUT TO 50.4% / 62.2% / 67.6%. Those come from
`tools/loki9_facing.py` with ALIGNED_DEG = 45.0 -- a full compass step of
angular TOLERANCE -- on Ouroboros/Askar games. This file computes EXACT-RAY
collinearity (cross-product zero). Different predicate. Matching the population
is necessary and NOT sufficient, and a reconciled-looking number across two
predicates is the more dangerous error, not the safer one.

PREREG-loki17's primary: a sentinel is SHOOTABLE-ON-BUILD if on the round it is
built the nearest ENEMY CORE FOOTPRINT tile is within d^2 <= 32 AND lies on its
actual facing ray.

Local, unlimited, zero rate-limit, zero rated exposure -- the primary is a
property of OUR OWN placement geometry, so the arena's opponent-behaviour bias
does not reach it. `arena.py` discards replays, so this drives `fcode run
--replay` directly.

Decoding reuses `replay_census.parse_entity` and the three traps loki9_facing.py
already paid for: turn -> update-list -> update -> entity is THREE levels; a
rotate() re-emits placeEntity for an existing id so only the FIRST is a build;
and distance is to the nearest of the four footprint tiles, not the anchor.
"""
import argparse, csv, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN, WIRE_VARINT  # noqa: E402

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

# ⚠ 0 IS *CENTRE*, NOT NORTH. My first table omitted it and shifted every
# facing one compass step -- and research's own validation had already shown a
# one-step rotation drives the facing/shot match rate to EXACTLY 0.0000. That is
# precisely the 0/287 this tool reported, and I read it as a bot defect, wrote a
# retraction, retired a plank and pre-registered another on it.
# Mapping copied from tools/loki9_facing.py, which is validated at 12,759/12,759
# FireTurret events.
DELTA = {0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
         5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1)}

# --------------------------------------------------------------------------
# ARCHIVED MODE -- decode ALREADY-DOWNLOADED PLATFORM replays instead of
# generating local games. Added 2026-08-11 as reusable infrastructure for any
# future turret-siting question (LOKI-17 itself is dead, see docstring above).
#
# WHERE THE FILES LIVE: `tools/monitors/replay_archiver.py` downloads every
# match into `replay_archive/<matchId>_game_<n>.replay26` flat (its own
# docstring: "Archive layout: replay_archive/<matchId>_game_<N>.replay26").
# No other path convention exists; do not invent one.
#
# WHICH TEAM IS OURS: local mode can hardcode `team == 0` because `fcode run
# bots/US bots/THEM` always seats us first. Archived platform replays carry no
# such guarantee. `corpus/meta_join.tsv` (built by tools/corpus/meta_attrib.py)
# gives the authoritative per-FILE seat via `us_side` ("a"/"b"/"none"), derived
# from the match sidecar's `teamAId`/`teamBId` against our own team id and
# CROSS-CHECKED (meta_attrib.py CHECK 1) against the independently-derived,
# replay-decoded seat in join.tsv: 289/289 matches, 1,445/1,445 files agree.
# `us_side == "a"` means our entities carry `ENTITY.team == 0` in THIS file;
# `"b"` means `== 1`. That is a per-file mapping (a team can sit on either
# side of different matches), so it must be looked up per file, never assumed
# constant the way local mode's `team == 0` is.
#
# The generic form below resolves ANY team id to its per-file seat (0/1) the
# same way, which is what lets it also measure an OPPONENT's own sentinels
# (e.g. Amendment 1b's third row, Askar City's own population) without a
# separate code path.
OURS_TEAM_ID = "379a5d80-9921-4c9e-949b-f9b1dcba16be"      # OpenSverige
                                                             # (tools/corpus/meta_attrib.py)
ARCHIVE_DIR = ROOT / "replay_archive"
META_JOIN = ROOT / "corpus" / "meta_join.tsv"


def _rot(direction, rotate):
    """Apply a deliberate N-step compass rotation to a decoded facing index,
    for the known-answer control (a 1-step rotation must collapse the exact-
    ray match rate to ~0.0%, per c91c078's own published signature). CENTRE
    (0) is not a compass direction and is left alone; rotate=0 is a no-op so
    the default local-mode call site (`decode(path)`) is byte-for-byte
    unchanged."""
    if not rotate or direction == 0:
        return direction
    return ((direction - 1 + rotate) % 8) + 1


def load_meta_rows():
    with META_JOIN.open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def resolve_population(rows, team_id, vs_team_id=None, ver=None, vs_ver=None):
    """file -> our seat (0/1) for every archived replay `team_id` played in,
    optionally restricted to a specific opponent id and/or either side's
    version. Seat resolution: whichever of teamAId/teamBId equals `team_id`
    fixes the seat (A=0, B=1) -- this is the mapping meta_attrib.py's CHECK 1
    validated at 1,445/1,445 files against the independently-derived
    replay-decoded seat in join.tsv.
    """
    out = []
    for r in rows:
        if r.get("teamAId") == team_id:
            idx, my_ver, opp_id, opp_ver = 0, r["teamAVersion"], r["teamBId"], r["teamBVersion"]
        elif r.get("teamBId") == team_id:
            idx, my_ver, opp_id, opp_ver = 1, r["teamBVersion"], r["teamAId"], r["teamAVersion"]
        else:
            continue
        if vs_team_id is not None and opp_id != vs_team_id:
            continue
        if ver is not None and my_ver != str(ver):
            continue
        if vs_ver is not None and opp_ver != str(vs_ver):
            continue
        out.append((r["file"], idx))
    return out


def decode(path, rotate=0):
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
                    d = DELTA.get(_rot(ent.direction or 0, rotate))
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
                    # ⚠ "FORWARD" CARRIES THREE DEFINITIONS IN THIS PLANK'S
                    # EVIDENCE CHAIN AND THEY PARTITION DIFFERENTLY. Named here
                    # because the LOKI-16 sign flip and the two-definitions-of-
                    # `undamaged` incident (3.8% apart under one name) are the
                    # same failure:
                    #   leg doc table ........ d2_own > 41   (n=327)
                    #   the 100.0% control ... d2_own > 145  (n=287) <- the
                    #        number that KILLED this plank attaches ONLY here
                    #   this line ............ d2_enemy < d2_own (a MIDPOINT rule)
                    # The midpoint rule is the LOOSEST of the three: it admits
                    # sentinels sited by main.py's home/threat path, which reads
                    # ~13.9% because it correctly aims at threats rather than at
                    # the core. So this subset is NOT "what LOKI-17 touches" --
                    # the plank edits `_try_forward_sentinel` in raid.py alone,
                    # and the honest filter for that is the reach argument
                    # (d2_own > 145), not this one. Reported as a midpoint cut,
                    # never as a bar, and never mixed with the other two.
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


def main_archived(argv):
    """Archived mode: same shootable-on-build metric, sourced from already-
    downloaded platform replays under replay_archive/ instead of freshly
    generated local games. Population is resolved via corpus/meta_join.tsv
    (see module docstring section above for the seat-resolution argument).

        .venv/bin/python tools/loki17_mech.py --archived [options]

    Options:
        --team-id ID       team whose sentinels to measure (default: us,
                            OpenSverige -- OURS_TEAM_ID)
        --vs-team-id ID    restrict to games against this opponent id
        --ver N            restrict --team-id's own version to N
        --vs-ver N         restrict the opponent's version to N
        --rotate N         KNOWN-ANSWER CONTROL: rotate every decoded facing
                            by N compass steps before scoring (N=1 must
                            collapse the hit rate to ~0%)
        --min-own-d2 N     KNOWN-ANSWER CONTROL / reach filter: keep only
                            sentinels with d2_own > N (strictly). N=145 is the
                            raid.py-reach argument from
                            docs/legs/LEG-loki17-battery-2026-08-10.md that
                            isolates the population raid.py's can_fire_from
                            guard builds by construction -- expected ~100%.
        --limit N          cap the number of matching files (speed)
    """
    ap = argparse.ArgumentParser(prog="loki17_mech.py --archived", add_help=True)
    ap.add_argument("--team-id", default=OURS_TEAM_ID)
    ap.add_argument("--vs-team-id", default=None)
    ap.add_argument("--ver", default=None)
    ap.add_argument("--vs-ver", default=None)
    ap.add_argument("--rotate", type=int, default=0)
    ap.add_argument("--min-own-d2", type=int, default=None)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args(argv)

    rows = load_meta_rows()
    pop = resolve_population(rows, args.team_id, args.vs_team_id, args.ver, args.vs_ver)
    if args.limit:
        pop = pop[: args.limit]

    tot = hit = 0; d2s = []
    fwd_tot = fwd_hit = 0
    games = 0; missing = 0
    for file, want_idx in pop:
        path = ARCHIVE_DIR / file
        if not path.exists():
            missing += 1
            continue
        rows_d = decode(path, rotate=args.rotate)
        if not rows_d:
            continue
        games += 1
        for team, d2, ok, d2own in rows_d:
            if team != want_idx:
                continue
            if args.min_own_d2 is not None and not (d2own > args.min_own_d2):
                continue
            tot += 1; d2s.append(d2); hit += ok
            if d2 < d2own:
                fwd_tot += 1; fwd_hit += ok

    print(f"archived: team={args.team_id} vs={args.vs_team_id} ver={args.ver} "
          f"vs_ver={args.vs_ver} rotate={args.rotate} min_own_d2={args.min_own_d2}")
    print(f"  population: {len(pop)} files matched, {missing} missing on disk, "
          f"{games} games with >=1 decoded sentinel")
    if not tot:
        print("  no sentinels decoded -- cannot measure"); return 1
    d2s.sort()
    print(f"  {hit}/{tot} shootable-on-build = {hit/tot:.1%}   "
          f"median nearest d2 = {d2s[len(d2s)//2]}")
    if fwd_tot:
        print(f"    forward-sited (midpoint) subset (d2_enemy < d2_own): "
              f"{fwd_hit}/{fwd_tot} = {fwd_hit/fwd_tot:.1%}")
    else:
        print("    forward-sited (midpoint) subset: 0 sentinels")
    return 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["--archived"]:
        raise SystemExit(main_archived(sys.argv[2:]))
    raise SystemExit(main(sys.argv[1:]))
