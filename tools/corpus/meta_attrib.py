#!/usr/bin/env python3
"""Meta-first attribution: every replay FILE -> both teams, both versions, both seats.

WHY THIS EXISTS.  `corpus/join.tsv` is built API-first: it walks OUR ladder
matches (`fcode match list --mine --type ladder`) and maps their games onto
archived files.  That path attributes 1,445 of 6,289 archived replays (~23%) and
its opponent-version column is dead -- `oppver` is the literal string "None" in
all 1,445 rows (documented in tools/corpus_sanity.py), so no analysis can ask
"which version of the opponent did we beat".  (`ourver` there is live, contrary
to the folklore; it is `oppver` that never arrived.)  And everything the archive
holds about other teams' matches -- the scouting bulk, two thirds of the files --
is simply invisible to it.

`replay_archive/` also holds 1,260 `<match-id>.meta.json` sidecars, one per
match, written next to the replays at download time (24 of them are keeper
placeholder stubs; 1,236 carry real headers).  Each real one carries the full
match header: both team ids, both team NAMES, both team VERSIONS, both live
ratings and both at-match ratings, the match winner, the tally, the trigger.  Joining
on the `<match-id>_game_<n>.replay26` filename prefix attributes replays without
touching the network at all, covers third-party matches the API path can never
see, and revives the version columns.

THE TRAP THIS CLOSES, AND THE ONE IT COULD OPEN.  A replay binary knows only
"team 0" and "team 1".  The whole value of an attribution table is the claim that
index 0 is a named team; get the seat backwards and every per-team statistic
built on top silently inverts.  join.tsv earns its seat from a per-GAME
`winnerSide` and reconciles it against the winner recorded inside each replay
(100.0000% agreement, standing rule).  This tool earns its seat from a MATCH-level
header instead, which is a different and weaker claim: it assumes teamA is always
replay index 0 and that the seat never swaps between games of a match.  So it
refuses to emit anything until three checks pass:

  1. SEAT+WINNER vs join.tsv.  Every file present in both tables must get the
     same seat for us and the same win/loss.  289/289 matches, 1,445/1,445 files.
  2. TALLY vs the replays themselves.  Decoding field 4 (top-level varint
     `winner`) out of every replay of a match must reproduce the sidecar's
     `scoreA`/`scoreB` exactly, and the side with the larger tally must be the
     sidecar's `winnerId`.  This is the independent test: the sidecar never sees
     the replay bytes and the replay bytes never see the sidecar.
  3. No seat swap.  Only matches whose files are all present are tallied, so a
     partially archived match cannot fake agreement by arithmetic.

Any failure prints the offending rows and exits non-zero rather than writing a
table that looks right.

    .venv/bin/python tools/corpus/meta_attrib.py [out.tsv]

OUTPUT (default corpus/meta_join.tsv), one row per replay FILE:

    file match game us_side
    teamAId teamAName teamAVersion teamBId teamBName teamBVersion
    teamARating teamBRating ratingABefore ratingBBefore
    match_winner_id match_winner_side game_winner_side game_winner_id our_won
    scoreA scoreB triggeredBy completedAt

`us_side` is "a", "b", or "none" -- "none" marks a third-party match (neither
side is OpenSverige), which is most of the archive and exactly the scouting
material join.tsv drops on the floor.  `game_winner_side` is PER GAME and comes
from the replay binary; `match_winner_id` is per MATCH and comes from the
sidecar.  Do not confuse them: a match winner loses individual games.

SAFETY: corpus/ is written concurrently by the keeper daemon.  This tool creates
exactly two files -- `meta_join.tsv` and its committed `.gz` sibling -- and
refuses to run at all if pointed at any name the keeper owns.
"""
from __future__ import annotations

import gzip
import json
import mmap
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "replay_archive"
OUT_DEFAULT = ROOT / "corpus" / "meta_join.tsv"
JOIN = ROOT / "corpus" / "join.tsv"

OURS = "379a5d80-9921-4c9e-949b-f9b1dcba16be"      # OpenSverige

# Files the keeper daemon owns. Writing any of them from here is a bug.
PROTECTED = {"join.tsv", "keeper_state.json", "manifest.json", "decoded.txt",
             "ladder_games.tsv", "league_games.tsv", "league_matches.tsv",
             "throws.tsv", "builds.tsv", "build_agg.tsv", "econ.tsv",
             "events.tsv", "flow.tsv"}

FILE_RE = re.compile(r"^(?P<match>.+)_game_(?P<game>\d+)\.replay26$")

COLS = ["file", "match", "game", "us_side",
        "teamAId", "teamAName", "teamAVersion",
        "teamBId", "teamBName", "teamBVersion",
        "teamARating", "teamBRating", "ratingABefore", "ratingBBefore",
        "match_winner_id", "match_winner_side",
        "game_winner_side", "game_winner_id", "our_won",
        "scoreA", "scoreB", "triggeredBy", "completedAt"]


# --------------------------------------------------------------------------
# replay: the only thing we need out of the binary is the top-level winner
# --------------------------------------------------------------------------

def _varint(buf, i: int):
    shift = result = 0
    while True:
        b = buf[i]
        i += 1
        result |= (b & 0x7F) << shift
        if b < 0x80:
            return result, i
        shift += 7


def replay_winner(path: Path):
    """Team index (0/1) recorded in the replay's own top-level field 4, or None.

    Skips every length-delimited field without copying it -- a full archive pass
    is ~11s this way, versus minutes if the turn buffers are materialised.
    """
    with path.open("rb") as fh:
        try:
            buf = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
        except ValueError:
            return None                                   # empty file
        try:
            i, n, winner = 0, len(buf), None
            while i < n:
                tag, i = _varint(buf, i)
                num, wire = tag >> 3, tag & 7
                if wire == 0:
                    value, i = _varint(buf, i)
                    if num == 4:
                        winner = value
                elif wire == 2:
                    length, i = _varint(buf, i)
                    i += length
                elif wire == 5:
                    i += 4
                elif wire == 1:
                    i += 8
                else:
                    return None                           # not a replay we know
            return winner
        except (IndexError, ValueError):
            return None
        finally:
            buf.close()


# --------------------------------------------------------------------------

def load_meta() -> tuple[dict[str, dict], int]:
    """match id -> sidecar, plus a count of STUBS.

    The keeper writes `{"id": ..., "_meta_stub": true}` placeholders to mark a
    match as priority before its header has been fetched.  A stub has every
    field None; taken at face value it would attribute a replay to a nameless
    team on neither seat, which is worse than not attributing it at all.
    """
    metas, stubs = {}, 0
    for p in sorted(ARCHIVE.rglob("*.meta.json")):
        try:
            d = json.loads(p.read_text())
        except Exception as exc:                          # noqa: BLE001
            print(f"  WARN unreadable sidecar {p.name}: {exc}", file=sys.stderr)
            continue
        if d.get("_meta_stub") or not d.get("teamAId") or not d.get("teamBId"):
            stubs += 1
            continue
        mid = d.get("id") or p.name[: -len(".meta.json")]
        metas[mid] = d
    return metas, stubs


def load_join() -> dict[str, tuple[int, int]]:
    """file -> (our_team_index, won) from the existing API-first table."""
    out = {}
    if not JOIN.exists():
        return out
    with JOIN.open() as fh:
        header = fh.readline().rstrip("\n").split("\t")
        fi, ti, wi = header.index("file"), header.index("our_team"), header.index("won")
        for line in fh:
            c = line.rstrip("\n").split("\t")
            if len(c) > max(fi, ti, wi):
                out[c[fi]] = (int(c[ti]), int(c[wi]))
    return out


def s(v) -> str:
    return "" if v is None else str(v)


def main(argv: list[str]) -> int:
    # --selftest=seat|winner : NEGATIVE CONTROL, and the reason it is a shipped
    # mode rather than something run once by hand during development.
    #
    # CHECK 1 and CHECK 2 below are this tool's entire safety story: they are
    # what lets a new attribution path be trusted next to the keeper's. But a
    # check that reports 100.0000% proves nothing on its own -- a check that
    # cannot fail reports 100% too, and that is precisely the failure mode this
    # session kept hitting (a treatment census that confidently returned 0/24
    # because it never found a core; a gunner ray bonus that would have scored
    # zero forever because the predicate refuses empty tiles). Both looked
    # healthy. So the flips are wired in permanently: deliberately corrupt the
    # derived seat or winner and REQUIRE the checks to catch it. Exit 1 if they
    # do not, because a silent check is worse than no check.
    selftest = ""
    argv = list(argv)
    for a in list(argv):
        if a.startswith("--selftest"):
            selftest = a.split("=", 1)[1] if "=" in a else "seat"
            argv.remove(a)
    out = Path(argv[0]).resolve() if argv else OUT_DEFAULT
    if out.name in PROTECTED:
        print(f"REFUSING to write {out.name}: owned by the keeper daemon", file=sys.stderr)
        return 2
    out.parent.mkdir(parents=True, exist_ok=True)

    all_files = sorted(ARCHIVE.rglob("*.replay26"))
    # Local arena diagnostics live in dated subdirectories under names like
    # `hive_s1_b_ad.replay26`. They are not league matches, have no match id and
    # can never have a sidecar; counting them in the denominator would understate
    # coverage of the material this tool is actually about.
    files = [p for p in all_files if FILE_RE.match(p.name)]
    local = len(all_files) - len(files)
    metas, stubs = load_meta()
    join = load_join()
    print(f"archive: {len(all_files)} replays ({len(files)} league-named, "
          f"{local} local arena diagnostics), {len(metas)} usable sidecars "
          f"(+{stubs} stubs), {len(join)} rows in join.tsv")

    rows, no_sidecar, bad_name = [], set(), 0
    per_match_games: dict[str, list[tuple[str, int]]] = {}   # match -> [(file, winner)]
    for p in files:
        m = FILE_RE.match(p.name)
        if not m:
            bad_name += 1
            continue
        mid, game = m.group("match"), int(m.group("game"))
        meta = metas.get(mid)
        if meta is None:
            no_sidecar.add(mid)
            continue
        w = replay_winner(p)
        per_match_games.setdefault(mid, []).append((p.name, -1 if w is None else w))

        if meta.get("teamAId") == OURS:
            us = "a"
        elif meta.get("teamBId") == OURS:
            us = "b"
        else:
            us = "none"
        gws = "" if w is None else ("a" if w == 0 else "b" if w == 1 else "")
        gwid = "" if not gws else s(meta.get("teamAId") if gws == "a" else meta.get("teamBId"))
        our_won = "" if us == "none" or not gws else str(int(gws == us))
        wid = meta.get("winnerId")
        mws = "a" if wid and wid == meta.get("teamAId") else \
              "b" if wid and wid == meta.get("teamBId") else ""

        rows.append({
            "file": p.name, "match": mid, "game": game, "us_side": us,
            "teamAId": s(meta.get("teamAId")), "teamAName": s(meta.get("teamAName")),
            "teamAVersion": s(meta.get("teamAVersion")),
            "teamBId": s(meta.get("teamBId")), "teamBName": s(meta.get("teamBName")),
            "teamBVersion": s(meta.get("teamBVersion")),
            "teamARating": s(meta.get("teamARating")),
            "teamBRating": s(meta.get("teamBRating")),
            "ratingABefore": s(meta.get("ratingABefore")),
            "ratingBBefore": s(meta.get("ratingBBefore")),
            "match_winner_id": s(wid), "match_winner_side": mws,
            "game_winner_side": gws, "game_winner_id": gwid, "our_won": our_won,
            "scoreA": s(meta.get("scoreA")), "scoreB": s(meta.get("scoreB")),
            "triggeredBy": s(meta.get("triggeredBy")),
            "completedAt": s(meta.get("completedAt")),
        })

    if selftest == "seat":
        for r in rows:
            r["us_side"] = {"a": "b", "b": "a"}.get(r["us_side"], r["us_side"])
    elif selftest == "winner":
        for r in rows:
            if r["our_won"] != "":
                r["our_won"] = str(1 - int(r["our_won"]))
    elif selftest:
        print(f"unknown --selftest mode {selftest!r} (seat|winner)", file=sys.stderr)
        return 2

    # ---- check 1: seat + winner against the API-first table --------------
    overlap = agree = 0
    seat_bad, win_bad = [], []
    for r in rows:
        jt = join.get(r["file"])
        if jt is None:
            continue
        overlap += 1
        j_team, j_won = jt
        our_idx = 0 if r["us_side"] == "a" else 1 if r["us_side"] == "b" else None
        if our_idx != j_team:
            seat_bad.append((r["file"], r["us_side"], j_team))
        elif r["our_won"] != "" and int(r["our_won"]) != j_won:
            win_bad.append((r["file"], r["our_won"], j_won))
        else:
            agree += 1
    rate1 = agree / overlap if overlap else float("nan")
    print(f"  CHECK 1 seat+winner vs join.tsv: {agree}/{overlap} agree ({rate1:.4%}), "
          f"{len(seat_bad)} seat, {len(win_bad)} winner disagreements")
    for f, a, b in (seat_bad + win_bad)[:20]:
        print(f"    DISAGREE {f}: meta={a} join={b}")

    # ---- check 2: sidecar tally against the replays themselves ------------
    tallied = tally_ok = skipped = 0
    tally_bad, winner_bad = [], []
    for mid, games in per_match_games.items():
        meta = metas[mid]
        sa, sb = meta.get("scoreA"), meta.get("scoreB")
        if sa is None or sb is None:
            skipped += 1
            continue
        if len(games) != sa + sb or any(w < 0 for _f, w in games):
            skipped += 1                      # partial archive / undecodable
            continue
        tallied += 1
        a = sum(1 for _f, w in games if w == 0)
        b = sum(1 for _f, w in games if w == 1)
        if (a, b) != (sa, sb):
            tally_bad.append((mid, (a, b), (sa, sb)))
            continue
        wid = meta.get("winnerId")
        expect = meta.get("teamAId") if a > b else meta.get("teamBId") if b > a else None
        if expect is not None and wid != expect:
            winner_bad.append((mid, wid, expect))
            continue
        tally_ok += 1
    rate2 = tally_ok / tallied if tallied else float("nan")
    print(f"  CHECK 2 sidecar score/winner vs replay winner fields: "
          f"{tally_ok}/{tallied} matches agree ({rate2:.4%}), "
          f"{skipped} untestable (partially archived or undecodable)")
    for mid, got, want in tally_bad[:20]:
        print(f"    TALLY  {mid}: replays {got} vs sidecar {want}")
    for mid, got, want in winner_bad[:20]:
        print(f"    WINNER {mid}: sidecar winnerId {got}, tally says {want}")

    if selftest:
        caught = len(seat_bad) + len(win_bad)
        if caught == 0:
            print(f"SELFTEST {selftest}: FAILED — corrupted the {selftest} on every "
                  f"row and CHECK 1 still agreed {agree}/{overlap}. The check is "
                  f"vacuous and its 100% means nothing.", file=sys.stderr)
            return 1
        print(f"SELFTEST {selftest}: PASS — corruption caught on {caught}/{overlap} "
              f"rows, agreement collapsed to {agree}/{overlap}. The check has teeth.")
        return 0

    if seat_bad or win_bad or tally_bad or winner_bad:
        print("INVARIANT FAILED — refusing to write the attribution table.",
              file=sys.stderr)
        return 1

    # ---- write ------------------------------------------------------------
    # corpus/.gitignore excludes *.tsv: the .gz sibling is the committed form.
    body = "\t".join(COLS) + "\n" + "".join(
        "\t".join(str(r[c]) for c in COLS) + "\n" for r in rows)
    out.write_text(body)
    with gzip.open(out.with_suffix(out.suffix + ".gz"), "wt") as gz:
        gz.write(body)

    ours = [r for r in rows if r["us_side"] != "none"]
    third = len(rows) - len(ours)
    ver_ok = sum(1 for r in ours
                 if (r["teamAVersion"] if r["us_side"] == "a" else r["teamBVersion"])
                 not in ("", "None"))
    opp_ver_ok = sum(1 for r in ours
                     if (r["teamBVersion"] if r["us_side"] == "a" else r["teamAVersion"])
                     not in ("", "None"))
    missing_files = len(files) - len(rows)
    print(f"  wrote {len(rows)} rows -> {out} "
          f"({len(rows)/len(files):.2%} of league-named replays, "
          f"{len(rows)/len(all_files):.2%} of every file in the archive)")
    print(f"  ours {len(ours)} (join.tsv attributes {len(join)}), third-party {third}")
    print(f"  unattributed: {missing_files} files across {len(no_sidecar)} matches "
          f"with no usable sidecar; {local} local diagnostics have no match at all")
    print(f"  versions live: ours {ver_ok}/{len(ours)}, opponent {opp_ver_ok}/{len(ours)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
