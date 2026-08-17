#!/usr/bin/env python3
"""UNRATED per-game decode: the surface join.tsv structurally cannot carry.

WHY THIS EXISTS (s46, 2026-08-16). `build_corpus.stage_join` keys every row off
`ladder_games.tsv`, which is RATED-only by design (CLAUDE.md's corpus-surface
rule). So every unrated challenge replay lands in `unmatched` and join.tsv can
never carry it — structurally, not as a lag. LEG-fieldcal's registered
secondary (ITT RMST300) therefore had NO computable surface at any completion
fraction: research's pooled read 2026-08-16 found join.tsv holds 0 rows for the
leg's 25 matches. "That's the difference between a leg and an expensive tape."

WHAT IT DOES. For every archived match whose meta says triggeredBy != "ladder",
emit one row per game with the outcome read FROM THE REPLAY ITSELF
(`replay_view.peek_outcome`: winner / win_condition / rounds — the replay is
the engine's own record, no seat reconciliation needed) joined to the meta's
opponent/version fields. Our side comes from teamAId/teamBId against OUR_TEAM_ID.

OUR_TEAM_ID IS DERIVED, NOT HARDCODED. At each run we cross-reference rated
matches present in BOTH ladder_games.tsv and the archive metas: ladder_games
says whether we won; the meta's winnerId then names our id (winnerId if won,
the other id if lost). We require >= MIN_CAL matches and UNANIMITY; any
disagreement is a hard refusal, because a wrong team id would silently flip
`won` on every row. This is also the tool's standing positive control — the
same derivation IS a 20-way agreement test between the meta surface and the
tape — and `--selftest` additionally drives the refusal branch with a
deliberately corrupted calibration pair.

⛔ NOT A VERDICT SURFACE ON ITS OWN. Rows here pool PROTOTYPES (unrated pools
prototypes — CLAUDE.md); any read slices by ourver/opp explicitly. This file
answers "what happened in that unrated game", nothing else.

Usage:
    .venv/bin/python tools/corpus/unrated_games.py            # build corpus/unrated_games.tsv
    .venv/bin/python tools/corpus/unrated_games.py --selftest
"""
from __future__ import annotations

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY THIS FILE NEEDED IT (measured 2026-08-16, s47). `tools/corpus/` sat
# OUTSIDE the help-contract sweep, which globbed `tools/*.py` only. Probed:
# 11 of 18 corpus tools violated the contract, and three of the failures are
# the dangerous classes the sweep exists to catch —
#   * `unrated_games.py --help` REWROTE corpus/unrated_games.tsv (1.1 MB)
#   * `ladder_meta.py`, `league_maps.py`, `league_matches.py`, `meta_attrib.py`
#     --help went to the NETWORK and ran until killed at 20 s
#   * `replay_autopsy.py --help` raised TypeError out of replay_census.fields()
# and the rest printed verdict-shaped text in this repo's own vocabulary
# ("no *.replay26 under --help", "sides loaded: 0 (from 0 matches) — --help").
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by build_corpus /
# keeper. Ungated, this would fire during that import and make the PARENT exit 0
# mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: the guard must not depend on what the host file
# happens to import, or on the order its imports appear in.
# ⛔ MUST SIT AFTER `from __future__ import ...`, which the language requires to
# be the first statement after the docstring.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "replay_archive"
OUT = ROOT / "corpus" / "unrated_games.tsv"

sys.path.insert(0, str(ROOT / "tools"))
import replay_view  # noqa: E402  (peek_outcome — the one implementation)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from atomicio import atomic_open  # noqa: E402  (see atomicio.py: the 62% incident)

GAME_RE = re.compile(r"^([0-9a-fA-F-]{36})_game_(\d+)\.replay26$")
MIN_CAL = 10

HEADER = ("file\tmatch\tgame\topp\toppver\tourver\tour_team\tmap_w\tmap_h"
          "\tcond\tturns\twon\tcreatedAt\ttrigger\n")


def load_metas(archive: Path) -> dict[str, dict]:
    metas = {}
    for p in archive.glob("*.meta.json"):
        try:
            metas[p.stem.replace(".meta", "")] = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError):
            continue  # counted implicitly: matches without a parsed meta are skipped
    return metas


def derive_our_id(metas: dict[str, dict], ladder_games: Path) -> str:
    """Cross-reference rated matches against the tape; require unanimity."""
    if not ladder_games.exists():
        raise SystemExit("⛔ REFUSING: no ladder_games.tsv to calibrate our team id against.")
    won_by_match: dict[str, bool] = {}
    for row in csv.DictReader(ladder_games.open(), delimiter="\t"):
        # any game row names the match and whether WE won that game; the match
        # winnerId in meta is the MATCH winner, so calibrate on the match score
        won_by_match.setdefault(row["match"], None)
    votes: dict[str, int] = {}
    used = 0
    for mid in won_by_match:
        m = metas.get(mid)
        if not m or m.get("triggeredBy") != "ladder":
            continue
        sa, sb = m.get("scoreA"), m.get("scoreB")
        wid, ta, tb = m.get("winnerId"), m.get("teamAId"), m.get("teamBId")
        if None in (sa, sb, wid, ta, tb) or sa == sb:
            continue
        # the tape's per-game rows sum to the match result; recompute our match
        # win from the tape rather than trusting either surface alone
        rows = [r for r in csv.DictReader(ladder_games.open(), delimiter="\t")
                if r["match"] == mid]
        if not rows:
            continue
        our_games = sum(int(r["won"]) for r in rows)
        their_games = len(rows) - our_games
        if our_games == their_games:
            continue
        we_won_match = our_games > their_games
        our_id = wid if we_won_match else (tb if wid == ta else ta)
        votes[our_id] = votes.get(our_id, 0) + 1
        used += 1
        if used >= 40:  # 40 matches is plenty; keep the pass cheap
            break
    if used < MIN_CAL:
        raise SystemExit(f"⛔ REFUSING: only {used} calibration matches (< {MIN_CAL}).")
    if len(votes) != 1:
        raise SystemExit(f"⛔ REFUSING: calibration DISAGREES on our team id: {votes}. "
                         "A wrong id silently flips `won` on every row.")
    return next(iter(votes))


def build(archive: Path = ARCHIVE, out: Path = OUT) -> dict:
    metas = load_metas(archive)
    our_id = derive_our_id(metas, ROOT / "corpus" / "ladder_games.tsv")
    kept = skipped_side = skipped_peek = 0
    rows = []
    for p in sorted(archive.glob("*_game_*.replay26")):
        gm = GAME_RE.match(p.name)
        if not gm:
            continue
        mid, game_n = gm.group(1), int(gm.group(2))
        m = metas.get(mid)
        if not m or m.get("triggeredBy") == "ladder":
            continue
        ta, tb = m.get("teamAId"), m.get("teamBId")
        if our_id == ta:
            ours, opp_name, opp_ver, our_ver = "A", m.get("teamBName"), m.get("teamBVersion"), m.get("teamAVersion")
        elif our_id == tb:
            ours, opp_name, opp_ver, our_ver = "B", m.get("teamAName"), m.get("teamAVersion"), m.get("teamBVersion")
        else:
            skipped_side += 1   # a foreign unrated match (not ours) — legitimate skip
            continue
        try:
            pk = replay_view.peek_outcome(p)
        except Exception:
            skipped_peek += 1   # unreadable replay: counted, never silently kept
            continue
        if pk.get("winner") is None:
            skipped_peek += 1
            continue
        won = int(pk["winner"] == ours)
        rows.append(f"{p.name}\t{mid}\t{game_n}\t{opp_name}\t{opp_ver}\t{our_ver}"
                    f"\t{ours}\t{pk['width']}\t{pk['height']}\t{pk['win_condition']}"
                    f"\t{pk['rounds']}\t{won}\t{m.get('createdAt')}\t{m.get('triggeredBy')}\n")
        kept += 1
    # ATOMIC (s50): this table is read by the fieldcal readers WHILE a leg is
    # running, i.e. by definition concurrently with the keeper's sync rebuilding
    # it. In-place truncation gave those readers a short-but-valid table.
    with atomic_open(out) as fh:
        fh.write(HEADER)
        fh.writelines(rows)
    stats = dict(our_id=our_id, kept=kept, skipped_side=skipped_side,
                 skipped_peek=skipped_peek)
    print(f"unrated_games.tsv: {kept} rows (our_id={our_id[:8]}…, "
          f"foreign-match skips={skipped_side}, unreadable={skipped_peek})")
    return stats


def selftest() -> int:
    metas = load_metas(ARCHIVE)
    fails = []
    # 1. POSITIVE: derivation reaches unanimity on the real archive.
    try:
        our_id = derive_our_id(metas, ROOT / "corpus" / "ladder_games.tsv")
    except SystemExit as e:
        print(f"selftest: derivation refused on real data: {e}")
        return 1
    # 2. NEGATIVE (the branch that makes 1 mean anything): corrupt ONE
    #    calibration meta's winnerId in a copy — unanimity must break, and the
    #    tool must REFUSE rather than emit.
    #    Corrupt a match the calibration actually SAMPLES: eligibility here
    #    mirrors derive_our_id (in ladder_games, ladder-triggered, decisive
    #    score) — corrupting a meta the derivation never reads is the vacuous
    #    version of this cell, and it shipped that way for one commit.
    bad = dict(metas)
    lg_matches = []
    for row in csv.DictReader((ROOT / "corpus" / "ladder_games.tsv").open(), delimiter="\t"):
        if row["match"] not in lg_matches:
            lg_matches.append(row["match"])
    for mid in lg_matches:
        m = bad.get(mid)
        if (m and m.get("triggeredBy") == "ladder" and m.get("winnerId")
                and m.get("scoreA") != m.get("scoreB")):
            mm = dict(m)
            mm["winnerId"] = m["teamBId"] if m["winnerId"] == m["teamAId"] else m["teamAId"]
            bad[mid] = mm
            break
    try:
        derive_our_id(bad, ROOT / "corpus" / "ladder_games.tsv")
        fails.append("corrupted winnerId did NOT break unanimity (refusal branch never fired)")
    except SystemExit:
        pass
    # 3. PEEK-vs-TAPE: for 20 RATED games, peek_outcome's winner must agree
    #    with ladder_games.won through the same side-derivation used for
    #    unrated rows. This is the cross-surface control for the `won` column.
    lg = list(csv.DictReader((ROOT / "corpus" / "ladder_games.tsv").open(), delimiter="\t"))
    # ladder_games carries no game index; games are per-match listing order
    # (the same convention stage_join relies on).
    game_idx: dict[str, int] = {}
    checked = agree = 0
    for row in lg:
        if checked >= 20:
            break
        game_idx[row["match"]] = game_idx.get(row["match"], 0) + 1
        m = metas.get(row["match"])
        if not m:
            continue
        ours = "A" if our_id == m.get("teamAId") else ("B" if our_id == m.get("teamBId") else None)
        if ours is None:
            continue
        p = ARCHIVE / f"{row['match']}_game_{game_idx[row['match']]}.replay26"
        if not p.exists():
            continue
        try:
            pk = replay_view.peek_outcome(p)
        except Exception:
            continue
        if pk.get("winner") is None:
            continue
        checked += 1
        if int(pk["winner"] == ours) == int(row["won"]):
            agree += 1
    if checked < 10:
        fails.append(f"peek-vs-tape control only found {checked} checkable rated games")
    elif agree != checked:
        fails.append(f"peek-vs-tape DISAGREES on {checked - agree} of {checked} rated games")
    if fails:
        print("SELFTEST FAILED:\n  " + "\n  ".join(fails))
        return 1
    print(f"SELFTEST PASS — unanimity on real data; corrupted-calibration refusal fires; "
          f"peek-vs-tape agrees {agree}/{checked} on rated games.")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    build()
