#!/usr/bin/env python3
"""Free-metadata corpus of OUR ladder matches: one row per GAME.

`fcode match list --mine` + `fcode match info <id> --json`. Zero replay
downloads. Carries per game: map, our seat, result, winCondition, turnsPlayed,
replayS3Key, plus the match-level opponent identity and the AT-MATCH ratings
(`ratingABefore`/`ratingBBefore` — the reconciled field, NOT teamXRating).
"""
import json, subprocess, sys, collections
from pathlib import Path

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
FC = str(ROOT / ".venv/bin/fcode")
OURS = "379a5d80-9921-4c9e-949b-f9b1dcba16be"
OUT = Path(sys.argv[1])


def run(args):
    r = subprocess.run([FC] + args, capture_output=True, text=True, cwd=ROOT)
    return r.stdout


matches = []
cursor = None
while True:
    args = ["match", "list", "--mine", "--type", "ladder", "--json", "--limit", "100"]
    if cursor:
        args += ["--cursor", cursor]
    d = json.loads(run(args))
    page = d["matches"] if isinstance(d, dict) else d
    if not page:
        break
    matches.extend(page)
    cursor = d.get("next_cursor") if isinstance(d, dict) else None
    print(f"  page -> {len(matches)} matches", file=sys.stderr)
    if not cursor:
        break
print(f"matches listed: {len(matches)}", file=sys.stderr)

games = []
for i, m in enumerate(matches):
    txt = run(["match", "info", m["id"], "--json"])
    try:
        d = json.loads(txt)
    except Exception:
        print(f"  bad json for {m['id']}", file=sys.stderr)
        continue
    mm = d["match"]
    ourside = "a" if mm["teamAId"] == OURS else "b"
    opp = mm["teamBName"] if ourside == "a" else mm["teamAName"]
    oppver = mm.get("teamBVersion") if ourside == "a" else mm.get("teamAVersion")
    ourver = mm.get("teamAVersion") if ourside == "a" else mm.get("teamBVersion")
    ourbef = mm.get("ratingABefore") if ourside == "a" else mm.get("ratingBBefore")
    oppbef = mm.get("ratingBBefore") if ourside == "a" else mm.get("ratingABefore")
    for g in d.get("games", []):
        games.append(dict(
            match=m["id"], created=mm.get("createdAt", ""),
            opp=opp, oppver=oppver, ourver=ourver,
            ourbef=ourbef, oppbef=oppbef,
            map=g["mapName"], seat=(g.get("winnerSide") or ""),
            won=int(g.get("winnerId") == OURS),
            cond=g.get("winCondition", ""), turns=g.get("turnsPlayed", 0),
            s3=g.get("replayS3Key", "") or "",
        ))
    if (i + 1) % 50 == 0:
        print(f"  ...{i+1}/{len(matches)} matches, {len(games)} games", file=sys.stderr)

cols = ["match", "created", "opp", "oppver", "ourver", "ourbef", "oppbef",
        "map", "seat", "won", "cond", "turns", "s3"]
with OUT.open("w") as f:
    f.write("\t".join(cols) + "\n")
    for g in games:
        f.write("\t".join(str(g[c]) for c in cols) + "\n")
print(f"WROTE {len(games)} games from {len(matches)} matches -> {OUT}", file=sys.stderr)
