#!/usr/bin/env python3
"""Seat adapter (FIRE GATE 3 remedy): rename platform downloads
<matchId>_game_<N>.replay26 -> <matchId8>_g<N>_seat{A,B}.replay26 using
fcode match info --json (winnerId+winnerSide -> our side per game).
Positive control: the replay's own winner index must agree with the API
winner in every game (loud fail). GAME CONTEXT: in-game league."""
import json, subprocess, sys, pathlib, re
OUR_TEAM_SUBSTR = "OpenSverige"
def adapt(match_id, dl_dir):
    info = json.loads(subprocess.run(
        [".venv/bin/fcode", "match", "info", match_id, "--json"],
        capture_output=True, text=True).stdout)
    m = info.get("match", info)
    a_name = str(m.get("teamAName") or m.get("teamA", ""))
    our_side = 0 if OUR_TEAM_SUBSTR in a_name else 1
    d = pathlib.Path(dl_dir)
    out = []
    for f in sorted(d.glob(f"{match_id}*_game_*.replay26")):
        n = re.search(r"_game_(\d+)", f.name).group(1)
        seat = "A" if our_side == 0 else "B"
        nf = f.with_name(f"{match_id[:8]}_g{n}_seat{seat}.replay26")
        f.rename(nf); out.append(str(nf))
    return our_side, out
if __name__ == "__main__":
    print(adapt(sys.argv[1], sys.argv[2]))
