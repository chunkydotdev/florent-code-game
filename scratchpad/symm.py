"""SYMMETRY DISCRIMINATOR for the 0%-availability-with-shots artefact.

The availability measure is an end-of-round SNAPSHOT, so a target that enters
and leaves inside one round is invisible. 600 of OUR sentinels read 0 opportunity
rounds while recording shots. That makes availability a LOWER BOUND -- but the
LEVEL does not matter, the SYMMETRY does: if the artefact bites both arms equally
it is common-mode and every comparison drawn survives; if it bites OURS harder it
suppresses our availability more and the 6.5pp forward gap is overstated.
Read-only; reuses the validated decoder, computes nothing new about firing.
"""
import csv, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, "scratchpad")
from sent_read import analyse  # noqa

SIDE = {"a": 0, "b": 1}
rows = []
with open("corpus/meta_join.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        if r.get("triggeredBy") == "ladder" and r.get("us_side") in SIDE:
            rows.append((r["file"], SIDE[r["us_side"]]))
print(f"population: {len(rows)} our rated-ladder replays (meta_join, us_side)")

AR = Path("replay_archive")
stat = {0: defaultdict(int), 1: defaultdict(int)}   # 0=ours 1=theirs
n_files = 0
for fname, ours in rows:
    p = AR / fname
    if not p.exists():
        continue
    try:
        st = analyse(p, None)
    except Exception:
        continue
    n_files += 1
    for rec in st["sent"]:
        side = 0 if rec["team"] == ours else 1
        stat[side]["n"] += 1
        if rec["opp_rounds"] == 0:
            stat[side]["zero_avail"] += 1
            if rec["shots"] > 0:
                stat[side]["zero_avail_but_fired"] += 1
                stat[side]["ghost_shots"] += rec["shots"]
        stat[side]["shots"] += rec["shots"]

print(f"decoded {n_files} replays\n")
print(f"{'':<14}{'sentinels':>10}{'0-avail':>10}{'0-avail & FIRED':>18}"
      f"{'rate':>9}{'ghost shots':>13}{'% of all shots':>16}")
for side, lbl in ((0, "OURS"), (1, "THEIRS")):
    s = stat[side]
    n, za, zf = s["n"], s["zero_avail"], s["zero_avail_but_fired"]
    gs, tot = s["ghost_shots"], s["shots"]
    print(f"{lbl:<14}{n:>10}{za:>10}{zf:>18}{100*zf/max(n,1):>8.2f}%"
          f"{gs:>13}{100*gs/max(tot,1):>15.3f}%")
o, t = stat[0], stat[1]
ro = 100*o["zero_avail_but_fired"]/max(o["n"],1)
rt = 100*t["zero_avail_but_fired"]/max(t["n"],1)
print(f"\nRATE RATIO ours/theirs = {ro/max(rt,1e-9):.2f}x")
print("  ~1.0 => COMMON-MODE: the artefact is a wash for every comparison drawn.")
print("  >>1  => it suppresses OUR availability harder and the 6.5pp forward")
print("         gap is OVERSTATED, possibly to zero.")
