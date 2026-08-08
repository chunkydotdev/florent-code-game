import sys
from pathlib import Path
sys.path.insert(0, "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/7ac1de9f-1507-4759-bdb4-6684fd492621/scratchpad")
import deep_replay as dr

path = Path(sys.argv[1])
d = dr.DeepReplay(path)
print("=== builds rounds 0-20 ===")
for ev in sorted(d.events, key=lambda e: e["round"]):
    if ev["round"]>20: break
    if ev["kind"]=="build":
        print(ev["round"], "team", ev["team"], ev["etype"], ev["pos"])
