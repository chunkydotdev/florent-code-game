#!/usr/bin/env python3
"""Build the Ouroboros master file list from corpus/meta_join.tsv (READ-ONLY)."""
import csv, sys, os, collections
ROOT = "/Users/junghard/Projects/Work/florent-code-game"
rows = list(csv.DictReader(open(f"{ROOT}/corpus/meta_join.tsv"), delimiter="\t"))
print("meta_join rows:", len(rows), file=sys.stderr)

OURS = "OpenSverige"

def sel(oppname):
    out = []
    for r in rows:
        a, b = r["teamAName"], r["teamBName"]
        if {a, b} == {OURS, oppname}:
            out.append(r)
    return out

targets = sys.argv[1:] or ["Ouroboros"]
for t in targets:
    sub = sel(t)
    # dedupe by file
    seen = {}
    for r in sub:
        seen[r["file"]] = r
    sub = list(seen.values())
    print(f"--- {t}: {len(sub)} files ---", file=sys.stderr)
    ver = collections.Counter()
    for r in sub:
        ov = r["teamBVersion"] if r["teamAName"] == OURS else r["teamAVersion"]
        uv = r["teamAVersion"] if r["teamAName"] == OURS else r["teamBVersion"]
        ver[(uv, ov)] += 1
    safe = t.replace(" ", "_")
    with open(f"{ROOT}/scratchpad/ouro/files_{safe}.tsv", "w") as fh:
        fh.write("file\tmatch\tgame\tus_side\tour_won\tourver\toppver\tcompletedAt\tgame_winner_side\n")
        for r in sorted(sub, key=lambda r: (r["completedAt"], r["file"])):
            us = r["us_side"]
            ov = r["teamBVersion"] if us == "a" else r["teamAVersion"]
            uv = r["teamAVersion"] if us == "a" else r["teamBVersion"]
            fh.write("\t".join([r["file"], r["match"], r["game"], us, r["our_won"],
                                str(uv), str(ov), r["completedAt"], r["game_winner_side"]]) + "\n")
    for k, v in sorted(ver.items()):
        print("   ourver=%s oppver=%s n=%d" % (k[0], k[1], v), file=sys.stderr)
