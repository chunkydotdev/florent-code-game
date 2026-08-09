#!/usr/bin/env python3
"""Incremental corpus sync — run this at session start.

WHY. The archive grows ~80 replays/hour while the archiver monitor runs, so a
corpus built at the start of a session is materially stale by the end of it and
badly stale after an overnight gap. `build_corpus.py --force` re-decodes all
3,800+ files (~15 min across five decoders) to absorb a few hundred new ones.
This decodes ONLY what is new and appends, which is seconds.

    .venv/bin/python tools/corpus/sync.py            # incremental, the default
    .venv/bin/python tools/corpus/sync.py --no-net   # replays only, no fcode calls
    .venv/bin/python tools/corpus/sync.py --check    # report drift and exit

`corpus/decoded.txt` is the ledger of replay filenames already folded in. It is
the source of truth for "what is new", rather than inferring from the tables —
a file that legitimately produces no rows (no throws, no events) would otherwise
be re-decoded forever.

CPU NOTE (protocol, 2026-08-09): a full pass is a real CPU load and a TLE'd turn
in a concurrent arena battery leaves no crash and no traceback, so contention
degrades measurements invisibly. Announce before a large sync; an incremental
one of a few hundred files is seconds and does not need announcing.
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "replay_archive"
OUT = ROOT / "corpus"
PY = str(ROOT / ".venv/bin/python")
HERE = Path(__file__).resolve().parent
LEDGER = OUT / "decoded.txt"

# decoder -> (script, output args builder). Each writes a header we strip when appending.
DECODERS = [
    ("throws.tsv", "replay_throws.py", "stdout"),
    ("events.tsv", "replay_events.py", "argv"),
    ("econ.tsv", "replay_econ.py", "argv"),
    ("flow.tsv", "replay_flow.py", "argv"),
    # replay_builds.py writes TWO outputs
    (("builds.tsv", "build_agg.tsv"), "replay_builds.py", "argv2"),
]


def sh(args, **kw):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, **kw)


def ledger() -> set[str]:
    if not LEDGER.exists():
        # bootstrap from whichever table has the widest coverage
        seen: set[str] = set()
        for name in ("events.tsv", "econ.tsv", "flow.tsv"):
            p = OUT / name
            if p.exists():
                for r in csv.DictReader(p.open(), delimiter="\t"):
                    seen.add(r["file"])
        LEDGER.write_text("\n".join(sorted(seen)) + ("\n" if seen else ""))
        print(f"  bootstrapped ledger from existing tables: {len(seen)} files")
        return seen
    return {ln.strip() for ln in LEDGER.open() if ln.strip()}


def append_stripping_header(src: Path, dst: Path) -> int:
    lines = src.read_text().splitlines(True)
    body = lines[1:] if lines else []
    if not dst.exists() and lines:
        dst.write_text(lines[0])
    with dst.open("a") as fh:
        fh.writelines(body)
    return len(body)


def sync_replays(new: list[Path]) -> dict:
    tmp = OUT / "_tmp"
    tmp.mkdir(exist_ok=True)
    added = {}
    args = [str(p) for p in new]
    for out_name, script, mode in DECODERS:
        s = str(HERE / script)
        if mode == "stdout":
            t = tmp / out_name
            with t.open("w") as fh:
                subprocess.run([PY, s] + args, cwd=ROOT, stdout=fh,
                               stderr=subprocess.DEVNULL, text=True)
            added[out_name] = append_stripping_header(t, OUT / out_name)
        elif mode == "argv":
            t = tmp / out_name
            subprocess.run([PY, s, str(t)] + args, cwd=ROOT,
                           capture_output=True, text=True)
            added[out_name] = append_stripping_header(t, OUT / out_name)
        else:  # argv2
            a, b = out_name
            ta, tb = tmp / a, tmp / b
            subprocess.run([PY, s, str(ta), str(tb)] + args, cwd=ROOT,
                           capture_output=True, text=True)
            added[a] = append_stripping_header(ta, OUT / a)
            added[b] = append_stripping_header(tb, OUT / b)
    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()
    return added


def sync_ladder() -> int:
    """Pull `match info` only for ladder matches not already in the corpus."""
    path = OUT / "ladder_games.tsv"
    known = set()
    if path.exists():
        known = {r["match"] for r in csv.DictReader(path.open(), delimiter="\t")}
    OURS = "379a5d80-9921-4c9e-949b-f9b1dcba16be"
    FC = str(ROOT / ".venv/bin/fcode")
    matches, cursor = [], None
    while True:
        a = ["match", "list", "--mine", "--type", "ladder", "--json", "--limit", "100"]
        if cursor:
            a += ["--cursor", cursor]
        try:
            d = json.loads(sh([FC] + a).stdout)
        except Exception:
            break
        page = d["matches"] if isinstance(d, dict) else d
        if not page:
            break
        matches.extend(page)
        cursor = d.get("next_cursor") if isinstance(d, dict) else None
        # stop paging once we are well into already-known territory
        if sum(1 for m in matches if m["id"] in known) > 120 or not cursor:
            break
    fresh = [m for m in matches if m["id"] not in known]
    if not fresh:
        return 0
    cols = ["match", "created", "opp", "oppver", "ourver", "ourbef", "oppbef",
            "map", "seat", "won", "cond", "turns", "s3"]
    n = 0
    with path.open("a") as fh:
        for m in fresh:
            try:
                d = json.loads(sh([FC, "match", "info", m["id"], "--json"]).stdout)
            except Exception:
                continue
            mm = d["match"]
            side = "a" if mm["teamAId"] == OURS else "b"
            row = dict(
                match=m["id"], created=mm.get("createdAt", ""),
                opp=mm["teamBName"] if side == "a" else mm["teamAName"],
                oppver=mm.get("teamBVersion") if side == "a" else mm.get("teamAVersion"),
                ourver=mm.get("teamAVersion") if side == "a" else mm.get("teamBVersion"),
                ourbef=mm.get("ratingABefore") if side == "a" else mm.get("ratingBBefore"),
                oppbef=mm.get("ratingBBefore") if side == "a" else mm.get("ratingABefore"),
            )
            for g in d.get("games", []):
                row2 = dict(row, map=g.get("mapName", ""), seat=g.get("winnerSide", ""),
                            won=int(g.get("winnerId") == OURS),
                            cond=g.get("winCondition", ""), turns=g.get("turnsPlayed", 0),
                            s3=g.get("replayS3Key", "") or "")
                fh.write("\t".join(str(row2[c]) for c in cols) + "\n")
                n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-net", action="store_true")
    ap.add_argument("--check", action="store_true", help="report drift and exit")
    a = ap.parse_args()

    files = sorted(ARCHIVE.rglob("*.replay26"))
    done = ledger()
    new = [p for p in files if p.name not in done]
    print(f"archive {len(files)} replays · already decoded {len(done)} · NEW {len(new)}")

    if a.check:
        m = json.loads((OUT / "manifest.json").read_text()) if (OUT / "manifest.json").exists() else {}
        print(f"manifest built {m.get('built_utc','?')} at {m.get('archive_replays','?')} replays")
        return

    if new:
        added = sync_replays(new)
        print("  appended rows: " + ", ".join(f"{k} +{v}" for k, v in added.items()))
        with LEDGER.open("a") as fh:
            for p in new:
                fh.write(p.name + "\n")
    else:
        print("  replays: up to date")

    if not a.no_net:
        g = sync_ladder()
        print(f"  ladder_games: +{g} new game rows")

    r = sh([PY, str(HERE / "build_corpus.py"), "--no-net"])
    tail = [ln for ln in r.stdout.splitlines() if "join.tsv" in ln or "RECONCIL" in ln]
    for ln in tail:
        print(" " + ln.strip())


if __name__ == "__main__":
    main()
