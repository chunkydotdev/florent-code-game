import sys, json
from pathlib import Path
sys.path.insert(0, "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/86e927e3-fb77-4d74-bdfe-69717bb9a2ae/scratchpad")
from walker import decode, ROLE_NAME
ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
POOL = "auroraveil bifrost fimbulwinter glacierkeep helheim holmgang icefloe jotunheim longhouse midgard paths skald stavkirke valkyrie yggdrasil".split()
ARMS = {"v600": ("replays_tape30", "{m}_s11.replay26", 0),
        "v601A": ("replays_tape601", "{m}_A.replay26", 0),
        "v601B": ("replays_tape601", "{m}_B.replay26", 1)}
out = {}
for m in POOL:
    for arm,(d,pat,side) in ARMS.items():
        out[f"{m}|{arm}"] = decode(ROOT/f"scratchpad/s54_fidtape/{d}/{pat.format(m=m)}", side)
Path("matrix.json").write_text(json.dumps(out, default=str))
print("ok", len(out))
