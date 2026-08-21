#!/usr/bin/env python3
"""Per-game cage/barrier/builder table for tape30 (v600) and tape601 (v601).
Reuses tools/skalman_fidelity.scan_replay (the SAME instrument that produced the
published M2a/M5 numbers) so per-game rows sum to the published aggregates."""
import sys, json
from pathlib import Path
ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(ROOT / "tools"))
from skalman_fidelity import scan_replay

POOL = "auroraveil bifrost fimbulwinter glacierkeep helheim holmgang icefloe jotunheim longhouse midgard paths skald stavkirke valkyrie yggdrasil".split()
rows = {}
for m in POOL:
    rows[(m, "v600")] = scan_replay(ROOT/f"scratchpad/s54_fidtape/replays_tape30/{m}_s11.replay26", 0)
    rows[(m, "v601A")] = scan_replay(ROOT/f"scratchpad/s54_fidtape/replays_tape601/{m}_A.replay26", 0)
    rows[(m, "v601B")] = scan_replay(ROOT/f"scratchpad/s54_fidtape/replays_tape601/{m}_B.replay26", 1)
out = {f"{k[0]}|{k[1]}": v for k, v in rows.items()}
Path(sys.argv[1]).write_text(json.dumps(out, default=str))
hdr = f"{'map':<14}{'arm':<7}{'rnds':>5}{'win':>4}{'bar':>5}{'ring':>5}{'ropen':>6}{'seal':>5}{'1stR':>6}{'bots':>5}{'cage':>6}{'harv':>5}"
print(hdr)
for m in POOL:
    for arm in ("v600","v601A","v601B"):
        r = rows[(m,arm)]
        side = r["side"]
        won = "W" if r["winner"] == side else ("L" if r["winner"] is not None else "?")
        cage = r["roles"].get("cage_walker")
        print(f"{m:<14}{arm:<7}{r['rounds']:>5}{won:>4}{r['barriers_total']:>5}"
              f"{r['barriers_on_enemy_ring']:>5}{r['ring_open']:>6}{r['max_seal']:>5}"
              f"{str(r['first_ring_build']):>6}{r['builders_spawned']:>5}{str(cage):>6}"
              f"{r['harv_end_total']:>5}")
