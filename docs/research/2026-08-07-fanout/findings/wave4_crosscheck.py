#!/usr/bin/env python3
"""Wave 4: siege-plant cross-check.

Read-only.  For every cached OUR-loss replay vs {Lunds Stallions, CtrlAltDefeat,
Orizon, Ouroboros, Powerpuff Girls} plus kladde-adjacent third-party siege replays
(from thread 3), extract every enemy gunner/sentinel build and classify it against
the thread-6 SeatAnalysis threat model for the VICTIM core (our core for the named
nemeses, the sieged team's core for kladde games).
"""
import json
import os
import sys

SCRATCH = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
           "8c290b06-f7e1-40b4-b90c-7343eb7e2e8e/scratchpad")
REPO = "/Users/junghard/Projects/Work/florent-code-game"
sys.path.insert(0, os.path.join(SCRATCH, "toolkit"))

from replay_lib import load_replay, game_meta, load_match_info, TEAM_NAME  # noqa: E402
import siege_geometry as sg  # noqa: E402

REPLAY_DIR = os.path.join(SCRATCH, "replay_cache", "replays")
FLAT_JSON = os.path.join(SCRATCH, "replay_cache", "all_games_flat.json")

NEMESES = ["Lunds Stallions", "CtrlAltDefeat", "Orizon", "Ouroboros", "Powerpuff Girls"]

# kladde-adjacent games available in the cache (from thread3's master table),
# with (match, game, map, kladde_side 0/1) -- victim/besieger resolved below
# from match_info's actual per-game winnerSide, not assumed.
KLADDE_GAMES = [
    ("225f2360-c7fc-4486-9f87-80923d480530", 2, "meander"),
    ("225f2360-c7fc-4486-9f87-80923d480530", 5, "jackpot"),
    ("69a0c821-9487-43bc-a3dd-8e4f6a88da34", 4, "hive"),
    ("31c83aff-1223-4c3b-b720-25c837409a0d", 5, "drumlin"),
    ("c23600fc-79e6-477b-afde-ceb4062ca48d", 3, "eider"),
    ("c23600fc-79e6-477b-afde-ceb4062ca48d", 5, "meander"),
    ("73624f1b-4c04-4eb8-9353-77e60096550e", 1, "saga"),
]

KNOWN_MAPS = {"antler", "archipelago", "atoll", "drumlin", "eider", "fjordgate", "heart",
              "hive", "jackpot", "lighthouse", "meander", "moonrise", "nordkap", "saga",
              "snowflake"}


def replay_path(match, game):
    return os.path.join(REPLAY_DIR, f"{match}_g{game}.replay26")


class ReplayMapAdapter:
    """Feeds a loaded Replay's own tiles into siege_geometry.SeatAnalysis,
    so the threat geometry is derived from the EXACT played grid rather than
    trusting maps/<name>.map26 to be byte-identical (cheap self-check, see
    verify() below)."""

    def __init__(self, r, name):
        self.width = r.width
        self.height = r.height
        self.tiles = r.tiles
        self.name = name
        self.symmetry = 0
        self.core_by_team = {0: r.core_pos(0), 1: r.core_pos(1)}

    def env(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.tiles[y][x]
        return sg.ENV_WALL

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def footprint(self, team):
        x, y = self.core_by_team[team]
        return {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}


def verify_against_mapfile(r, mapname):
    """Sanity check: does maps/<mapname>.map26 match the replay's own grid?
    Returns True/False/None (None = map file not available for cross-check)."""
    p = os.path.join(REPO, "maps", f"{mapname}.map26")
    if not os.path.exists(p):
        return None
    g = sg.GameMap(p)
    if g.width != r.width or g.height != r.height:
        return False
    for y in range(r.height):
        for x in range(r.width):
            if g.env(x, y) != r.tiles[y][x]:
                return False
    if g.core_by_team.get(0) != r.core_pos(0) or g.core_by_team.get(1) != r.core_pos(1):
        return False
    return True


def analyse_game(r, victim_team, mapname, label):
    """Return dict with plant classification for one replay, one victim seat."""
    besieger = 1 - victim_team
    adapter = ReplayMapAdapter(r, mapname)
    sa = sg.SeatAnalysis(adapter, victim_team)
    fp = adapter.footprint(victim_team)
    nw = adapter.core_by_team[victim_team]

    match_ok = verify_against_mapfile(r, mapname) if mapname in KNOWN_MAPS else None

    # every enemy (besieger) gunner/sentinel build, whole game
    builds = []
    for ev in r.rounds:
        for b in ev.builds:
            if b.team != besieger:
                continue
            if b.kind not in ("gunner", "sentinel"):
                continue
            builds.append(b)

    # damage attribution: turret entity id -> total damage dealt to victim's core
    core_dmg_by_source = {}
    for h in r.damage_log(team=besieger, target_kind="core"):
        if h.target_team != victim_team:
            continue
        if h.source_id is None:
            continue
        core_dmg_by_source[h.source_id] = core_dmg_by_source.get(h.source_id, 0) + h.amount

    rows = []
    for b in builds:
        t = b.pos
        fp_dsq = sg.nearest_footprint_dsq(t, fp)
        nw_dsq = sg.dsq(t, nw)
        aligned_flag = any(sg.aligned(t, c) for c in fp)
        in_sent = t in sa.sentinel_threat
        in_gun = t in sa.gunner_threat
        dmg = core_dmg_by_source.get(b.id, 0)
        rows.append({
            "label": label, "map": mapname, "round": b.round, "id": b.id,
            "kind": b.kind, "pos": t, "fp_dsq": fp_dsq, "nw_dsq": nw_dsq,
            "aligned": aligned_flag, "in_sentinel_threat": in_sent,
            "in_gunner_threat": in_gun, "core_dmg": dmg,
            "core_damaging": dmg > 0,
        })
    return {
        "label": label, "map": mapname, "victim_team": victim_team,
        "besieger_team": besieger, "n_rounds": r.n_rounds,
        "mapfile_match": match_ok, "rows": rows,
        "sentinel_threat_size": len(sa.sentinel_threat),
        "gunner_threat_size": len(sa.gunner_threat),
    }


def collect_our_loss_games():
    data = json.load(open(FLAT_JSON))
    out = []
    for d in data:
        if d.get("opp_name") not in NEMESES or d.get("we_won") is not False:
            continue
        p = replay_path(d["match"], d["game"])
        if not os.path.exists(p):
            continue
        if d.get("map") not in KNOWN_MAPS:
            continue
        out.append(d)
    return out


def main():
    results = []
    errors = []

    # 1. our losses vs the 5 named nemeses
    for d in collect_our_loss_games():
        match, game, mapname = d["match"], d["game"], d["map"]
        p = replay_path(match, game)
        try:
            r = load_replay(p)
            meta = game_meta(match, game)
            victim = meta["our_side"]
            label = f"{d['opp_name']} | {match[:8]} g{game} {mapname} (we_lost, {d.get('wincond')})"
            res = analyse_game(r, victim, mapname, label)
            res["nemesis"] = d["opp_name"]
            res["wincond"] = d.get("wincond")
            res["match"] = match
            res["game"] = game
            results.append(res)
        except Exception as e:
            errors.append((match, game, mapname, str(e)))

    # 2. kladde-adjacent (third-party) siege games
    for match, game, mapname in KLADDE_GAMES:
        p = replay_path(match, game)
        if not os.path.exists(p):
            errors.append((match, game, mapname, "not cached"))
            continue
        try:
            r = load_replay(p)
            info = load_match_info(match)
            g_entry = next(x for x in info["games"] if x["gameNumber"] == game)
            winner_side = g_entry["winnerSide"]  # 'a' or 'b'
            wincond = g_entry["winCondition"]
            teamA, teamB = info["match"]["teamAName"], info["match"]["teamBName"]
            kladde_side = 0 if "kladde" in teamA.lower() else 1
            if wincond == "core_destroyed":
                loser_side = 1 if winner_side == "a" else 0
                victim = loser_side
            else:
                # titanium_collected: no core death -- analyse both sides,
                # tag which one is kladde for reporting
                victim = None
            besieger_name = teamB if kladde_side == 0 else teamA
            victim_name_map = {0: teamA, 1: teamB}
            if victim is not None:
                label = (f"kladde-adj {victim_name_map[victim]} sieged by "
                         f"{victim_name_map[1 - victim]} | {match[:8]} g{game} {mapname} "
                         f"({wincond})")
                res = analyse_game(r, victim, mapname, label)
                res["nemesis"] = "kladde-third-party"
                res["wincond"] = wincond
                res["match"] = match
                res["game"] = game
                res["kladde_is_victim"] = (victim == kladde_side)
                results.append(res)
            else:
                for victim_try in (0, 1):
                    label = (f"kladde-adj {victim_name_map[victim_try]} vs "
                             f"{victim_name_map[1 - victim_try]} | {match[:8]} g{game} "
                             f"{mapname} ({wincond}, both-sides-check)")
                    res = analyse_game(r, victim_try, mapname, label)
                    res["nemesis"] = "kladde-third-party"
                    res["wincond"] = wincond
                    res["match"] = match
                    res["game"] = game
                    res["kladde_is_victim"] = (victim_try == kladde_side)
                    results.append(res)
        except Exception as e:
            errors.append((match, game, mapname, str(e)))

    out = {"results": results, "errors": errors}
    with open(os.path.join(SCRATCH, "findings", "wave4_raw.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)

    print(f"games analysed: {len(results)}, errors: {len(errors)}")
    for e in errors:
        print("ERROR", e)
    total_plants = sum(len(r["rows"]) for r in results)
    print(f"total enemy turret builds found: {total_plants}")
    mismatch = [r["label"] for r in results if r["mapfile_match"] is False]
    if mismatch:
        print("MAPFILE MISMATCHES (adapter used replay tiles, flagged):")
        for m in mismatch:
            print(" ", m)


if __name__ == "__main__":
    main()
