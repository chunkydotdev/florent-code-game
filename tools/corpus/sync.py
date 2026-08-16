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



def _pick(listrow, info, key):
    """Prefer the LIST payload for a field the DETAIL endpoint nulls.

    Explicit `is not None` rather than `or`, so a legitimate 0 is never
    silently replaced by the fallback."""
    v = listrow.get(key) if isinstance(listrow, dict) else None
    if v is not None:
        return v
    return info.get(key)

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
    elif lines and dst.exists():
        # HEADER-DRIFT GUARD (s39, 2026-08-14). The s36 COLS widening of
        # replay_econ.py landed 31,986 19-field rows under econ.tsv's 17-field
        # header because this function appends the body VERBATIM — every column
        # past the first difference silently reads its neighbour's value and
        # every cell still parses as an integer. Refusing loudly is the class
        # fix; it covers every appended surface, not only econ.
        with dst.open() as fh:
            dst_header = fh.readline()
        if dst_header != lines[0]:
            raise RuntimeError(
                f"HEADER DRIFT {src.name} -> {dst.name}: source and destination "
                f"headers differ; appending would silently shift columns (the "
                f"s36 econ defect). Rebuild {dst.name} with the current decoder."
                f"\n  dst: {dst_header.rstrip()}\n  src: {lines[0].rstrip()}")
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
            "map", "winner_seat", "won", "cond", "turns", "s3"]
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
                # ⛔ VERSIONS COME FROM THE **LIST** PAYLOAD (`m`), NOT FROM
                # `match info` (`mm`). Measured 2026-08-13 across 6 consecutive
                # matches: `fcode match info` returns the version for OUR side
                # and **None for the OPPONENT'S**, every time, while
                # `fcode match list` returns BOTH. That single asymmetry is why
                # `ladder_games.tsv.oppver` was the literal string 'None' in
                # **all 4,375 rows** while `ourver` populated correctly — the
                # ingest read a field the detail endpoint does not fill in.
                #   list: 24/123   info: None/123   (we are B)
                #   list: 122/52   info: 122/None   (we are A)
                # CLAUDE.md already flagged the consequence — "we pin ourver …
                # and nothing pins or even reads THEIRS" — and prescribed
                # `league_matches.tsv` as the workaround. The field was on the
                # wire the whole time. `mm` is kept as a fallback so a future
                # API that fills it in still works.
                oppver=_pick(m, mm, "teamBVersion" if side == "a" else "teamAVersion"),
                ourver=_pick(m, mm, "teamAVersion" if side == "a" else "teamBVersion"),
                ourbef=mm.get("ratingABefore") if side == "a" else mm.get("ratingBBefore"),
                oppbef=mm.get("ratingBBefore") if side == "a" else mm.get("ratingABefore"),
            )
            for g in d.get("games", []):
                row2 = dict(row, map=g.get("mapName", ""), winner_seat=g.get("winnerSide", ""),
                            won=int(g.get("winnerId") == OURS),
                            cond=g.get("winCondition", ""), turns=g.get("turnsPlayed", 0),
                            s3=g.get("replayS3Key", "") or "")
                fh.write("\t".join(str(row2[c]) for c in cols) + "\n")
                n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-net", action="store_true")
    # ⛔ ADDED s33: the LADDER-METADATA pull only, skipping the CPU-heavy decode.
    # The keeper defers the decode when load is high (156 times on 2026-08-12),
    # and that early return was ALSO skipping this network-bound step -- which is
    # how ladder_games.tsv reached 8.5h stale while every cycle logged healthy.
    ap.add_argument("--net-only", action="store_true",
                    help="ladder metadata only; no replay decode")
    ap.add_argument("--check", action="store_true", help="report drift and exit")
    a = ap.parse_args()

    if a.net_only:
        # LADDER METADATA ONLY. No decode, no ledger, no build_corpus.
        g = sync_ladder()
        print(f"  ladder_games: +{g} new game rows")
        r = sh([PY, str(HERE / "league_matches.py"), "--update",
                str(OUT / "league_matches.tsv")])
        for ln in r.stdout.splitlines():
            if ln.startswith("league_matches:"):
                print("  " + ln.strip())
        return

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
        # LEAGUE-WIDE MATCH TABLE, incremental (s28, Magnus: "fix that with a
        # script that keeps it updated"). Kept OUT of the replay path because it
        # is a network walk over every ladder team; ~90s to catch up a day.
        # It ran by hand only, which is how league_matches.tsv reached 20.9h
        # stale while the keeper logged a healthy cycle every 10 minutes.
        r = sh([PY, str(HERE / "league_matches.py"), "--update",
                str(OUT / "league_matches.tsv")])
        for ln in r.stdout.splitlines():
            if ln.startswith("league_matches:"):
                print("  " + ln.strip())

    r = sh([PY, str(HERE / "build_corpus.py"), "--no-net"])
    tail = [ln for ln in r.stdout.splitlines() if "join.tsv" in ln or "RECONCIL" in ln]
    for ln in tail:
        print(" " + ln.strip())

    sync_meta_attrib()
    sync_unrated_games()


def sync_meta_attrib() -> None:
    """Rebuild `corpus/meta_join.tsv`.

    WIRED IN 2026-08-09 (s26). It was not, and nothing else built this file —
    `meta_attrib.py` had to be run BY HAND. So the one corpus surface that
    carries OPPONENT versions was the stalest file in `corpus/`, while the
    drift-watch told every lane to prefer it. `ladder_games.tsv` and `join.tsv`
    refresh on sync but their `oppver` is universally the literal 'None'
    (corpus_sanity KNOWN-DEAD), so between them there was NO surface that could
    name an opponent's version for a current-era game.

    THE CONCRETE COST, which is why this is wired rather than filed: we played
    Powerpuff Girls twice on v102 eighty minutes apart, 4-1 then 1-4, and could
    not say whether they had shipped in between. (With the table fresh: they had
    not — v49 both times. Askar City, by contrast, went v82 -> v83 inside four
    minutes the same evening, so mid-session opponent ships are real and this is
    the surface that sees them.)

    ~7s on 8,143 replays, so it runs every sync. It refuses to write unless its
    three checks pass, which means the failure mode is a STALE table, i.e.
    exactly the state this function exists to end — so a failure must be LOUD
    rather than swallowed.
    """
    r = sh([PY, str(HERE / "meta_attrib.py")])
    if r.returncode != 0:
        print("  meta_join: **REFUSED TO REBUILD** — attribution checks failed. "
              "The table on disk is now STALE; do not trust its versions.")
        for ln in (r.stdout + r.stderr).strip().splitlines()[-8:]:
            print("    " + ln.strip())
        return
    for ln in r.stdout.splitlines():
        s = ln.strip()
        if s.startswith("wrote ") or s.startswith("versions live"):
            print("  meta_join: " + s)


def sync_unrated_games() -> None:
    """Rebuild `corpus/unrated_games.tsv` — the unrated per-game outcome surface.

    WIRED IN 2026-08-16 (s46), the same session that built the tool, for the
    same reason sync_meta_attrib was wired in s26: a surface that only a hand
    run refreshes is the stalest file in corpus/ by construction. This one is
    what makes LEG-fieldcal readable on its registered RMST300 axis at ANY
    completion fraction — a leg that keeps playing against a decode frozen at
    this morning's build would be readable only as of 08:52Z, which is the
    ship_watch defect wearing a corpus costume. ~seconds on the archive; the
    tool REFUSES (nonzero rc) on calibration disagreement rather than writing
    a table whose `won` column might be flipped, so the failure mode is a
    STALE-and-said-so table, never a wrong one.
    """
    r = sh([PY, str(HERE / "unrated_games.py")])
    if r.returncode != 0:
        print("  unrated_games: **REFUSED TO REBUILD** — calibration failed. "
              "The table on disk is now STALE; its ages say so.")
        for ln in (r.stdout + r.stderr).strip().splitlines()[-6:]:
            print("    " + ln.strip())
        return
    for ln in r.stdout.splitlines():
        s = ln.strip()
        if s.startswith("unrated_games.tsv:"):
            print("  " + s)


if __name__ == "__main__":
    main()
