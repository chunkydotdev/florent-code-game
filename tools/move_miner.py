#!/usr/bin/env python3
"""MOVE-MINING TRIGGER — which opponent's games should be studied for new moves?

WHY THIS EXISTS (Magnus, 2026-08-16, s47, verbatim): "What you're doing now
should be in the loop somehow, we need to continuously find out new moves."
The replay-study method that produced the 0033 pieces (gunner plug, zero
core-chew, counter-battery targeting) was a one-off commissioned by hand.
This tool makes it recur: it reads the rated tape and the mining ledger and
names the opponents whose accumulated UNSTUDIED games justify a study — so
the question "who should we watch next?" is answered by an instrument, not
by whoever remembers to ask.

METHOD IT FEEDS: docs/research/PLAYBOOK-move-mining-2026-08-16.md
LEDGER IT READS: docs/research/move-mining-ledger.tsv
    columns: date  opp  oppver  games_covered  doc
    One row per completed study. games_covered = the (opp, oppver) game count
    at study time. A version bump by the opponent resets coverage to zero —
    a new version is a new bot, and its moves are unstudied by definition.

TRIGGER RULES (both drive the same output; thresholds pinned here, not in
any caller):
  * FIRE  if an (opp, latest-oppver) cell holds >= 40 unstudied games, OR
          >= 20 unstudied games while our all-time share vs that opp < 45%.
  * Ranking: unstudied_games * (1 + max(0, 50 - share_pct) / 25) — an
    adverse opponent's games are worth more study per game.
  * BLIND, exit 2, if the tape is missing, unparseable, or its newest row is
    older than 24 h — a stale tape silently under-counts every cell, and an
    alarm that cannot tell it is blind is this repo's most-repeated defect.

Exit: 0 = no candidate above threshold · 1 = candidates printed · 2 = BLIND.
A cancelled/absent ledger file is NOT blind — it means nothing has ever been
studied, which is exactly when this tool should fire loudest.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__)
        raise SystemExit(0)

ROOT = Path(__file__).resolve().parent.parent
TAPE = ROOT / "corpus" / "ladder_games.tsv"
LEDGER = ROOT / "docs" / "research" / "move-mining-ledger.tsv"

FIRE_UNSTUDIED = 40
FIRE_ADVERSE_UNSTUDIED = 20
ADVERSE_SHARE_PCT = 45.0
STALE_H = 24.0


def _parse_tape(tape: Path):
    """-> (rows, newest_created_iso) or (None, reason) on blind."""
    try:
        lines = tape.read_text().splitlines()
    except OSError as e:
        return None, f"tape unreadable: {e}"
    rows = []
    newest = ""
    for ln in lines[1:]:
        p = ln.split("\t")
        if len(p) < 12:
            continue
        # match created opp oppver ourver ... won(9) ...
        rows.append((p[2], p[3], p[1], p[9]))
        if p[1] > newest:
            newest = p[1]
    if not rows:
        return None, "tape parsed to zero rows"
    return rows, newest


def _age_h(iso: str, now: datetime) -> float | None:
    try:
        t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (now - t).total_seconds() / 3600.0
    except ValueError:
        return None


def _parse_ledger(ledger: Path) -> dict[tuple[str, str], int]:
    cov: dict[tuple[str, str], int] = {}
    if not ledger.exists():
        return cov
    for ln in ledger.read_text().splitlines()[1:]:
        p = ln.split("\t")
        if len(p) >= 4 and not ln.startswith("#"):
            try:
                cov[(p[1], p[2])] = max(cov.get((p[1], p[2]), 0), int(p[3]))
            except ValueError:
                continue
    return cov


def evaluate(tape: Path = TAPE, ledger: Path = LEDGER,
             now: datetime | None = None):
    """-> (verdict, lines). verdict in {'BLIND','FIRE','QUIET'}."""
    now = now or datetime.now(timezone.utc)
    rows, newest = _parse_tape(tape)
    if rows is None:
        return "BLIND", [f"BLIND — {newest}. VERDICT IS UNKNOWN, NOT QUIET."]
    age = _age_h(newest, now)
    if age is None or age > STALE_H:
        return "BLIND", [
            f"BLIND — newest tape row {newest!r} is "
            f"{'unparseable' if age is None else f'{age:.1f}h old'} "
            f"(limit {STALE_H:.0f}h). VERDICT IS UNKNOWN, NOT QUIET."]

    per_opp: dict[str, list[int]] = {}
    per_cell: dict[tuple[str, str], int] = {}
    latest_ver: dict[str, tuple[str, str]] = {}  # opp -> (created, ver)
    for opp, ver, created, won in rows:
        w = per_opp.setdefault(opp, [0, 0])
        w[0] += 1
        w[1] += 1 if won in ("1", "True", "true") else 0
        per_cell[(opp, ver)] = per_cell.get((opp, ver), 0) + 1
        if opp not in latest_ver or created > latest_ver[opp][0]:
            latest_ver[opp] = (created, ver)

    cov = _parse_ledger(ledger)
    cands = []
    for opp, (_, ver) in latest_ver.items():
        cell = per_cell[(opp, ver)]
        unstudied = cell - cov.get((opp, ver), 0)
        n, w = per_opp[opp]
        share = 100.0 * w / n
        fires = unstudied >= FIRE_UNSTUDIED or (
            unstudied >= FIRE_ADVERSE_UNSTUDIED and share < ADVERSE_SHARE_PCT)
        if fires:
            score = unstudied * (1 + max(0.0, 50.0 - share) / 25.0)
            cands.append((score, opp, ver, unstudied, cell, share, n))

    if not cands:
        return "QUIET", [
            f"move_miner QUIET — no (opp, latest-ver) cell holds "
            f">={FIRE_UNSTUDIED} unstudied games "
            f"(>={FIRE_ADVERSE_UNSTUDIED} if share<{ADVERSE_SHARE_PCT:.0f}%). "
            f"tape age {age:.1f}h."]
    cands.sort(reverse=True)
    out = [f"*** MOVE-MINING CANDIDATES ({len(cands)}) — study the top one "
           f"per docs/research/PLAYBOOK-move-mining-2026-08-16.md ***  "
           f"[tape age {age:.1f}h]"]
    for score, opp, ver, unstudied, cell, share, n in cands[:8]:
        out.append(
            f"   score {score:7.1f}  {opp!r} v{ver}: {unstudied} unstudied "
            f"of {cell} on this version · all-time share {share:.1f}% "
            f"(n={n})")
    return "FIRE", out


# --------------------------- selftest ---------------------------------------
def _selftest() -> int:
    import tempfile
    ok = True

    def chk(label, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print(f"  [{'ok' if good else 'FAIL'}] {label:58s} got={got} want={want}")

    now = datetime(2026, 8, 16, 12, 0, tzinfo=timezone.utc)
    hdr = "match\tcreated\topp\toppver\tourver\tourbef\toppbef\tmap\twinner_seat\twon\tcond\tturns\ts3\n"

    def tape_of(rows):
        f = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
        f.write(hdr)
        # distinct, increasing created stamps — with equal stamps the
        # latest-version tie-break keeps first-seen, which is exactly the
        # case the version-bump test exists to drive.
        for i, (opp, ver, won) in enumerate(rows):
            f.write(f"m\t2026-08-16T{i // 3600:02d}:{(i // 60) % 60:02d}:{i % 60:02d}.{i:03d}Z\t{opp}\t{ver}\tv1\t1\t1\tmap\tA\t{won}\tcore_destroyed\t100\t-\n")
        f.close()
        return Path(f.name)

    def ledger_of(entries):
        f = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
        f.write("date\topp\toppver\tgames_covered\tdoc\n")
        for opp, ver, n in entries:
            f.write(f"2026-08-16\t{opp}\t{ver}\t{n}\tdoc.md\n")
        f.close()
        return Path(f.name)

    # 1) 60 unstudied games, no ledger -> FIRE
    t = tape_of([("teamX", "5", "1")] * 30 + [("teamX", "5", "0")] * 30)
    v, _ = evaluate(t, Path("/nonexistent-ledger"), now)
    chk("60 unstudied, no ledger file -> FIRE", v, "FIRE")
    # 2) same fully covered -> QUIET (the guard's safe case, driven)
    v, _ = evaluate(t, ledger_of([("teamX", "5", 60)]), now)
    chk("same 60 covered by ledger -> QUIET", v, "QUIET")
    # 3) version bump resets coverage: 25 games on NEW ver, share 30 -> FIRE
    t3 = tape_of([("teamY", "1", "1")] * 30 + [("teamY", "1", "0")] * 45
                 + [("teamY", "2", "0")] * 20 + [("teamY", "2", "1")] * 5)
    v, lines = evaluate(t3, ledger_of([("teamY", "1", 75)]), now)
    chk("25 games on unstudied NEW version, adverse -> FIRE", v, "FIRE")
    chk("...and the candidate line names the NEW version", any("v2" in l for l in lines), True)
    # 4) 25 unstudied but share 55 (not adverse, under 40) -> QUIET
    t4 = tape_of([("teamZ", "3", "1")] * 14 + [("teamZ", "3", "0")] * 11)
    v, _ = evaluate(t4, ledger_of([]), now)
    chk("25 unstudied at healthy share -> QUIET", v, "QUIET")
    # 5) stale tape -> BLIND, not QUIET
    v, lines = evaluate(t, Path("/nonexistent"), datetime(2026, 8, 18, 12, 0, tzinfo=timezone.utc))
    chk("48h-old tape -> BLIND (never QUIET)", v, "BLIND")
    chk("...and BLIND says the verdict is unknown", "UNKNOWN" in lines[0], True)
    # 6) missing tape -> BLIND
    v, _ = evaluate(Path("/nonexistent-tape"), Path("/nonexistent"), now)
    chk("missing tape -> BLIND", v, "BLIND")

    print("MOVE_MINER SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv):
    if argv and argv[0] == "--selftest":
        raise SystemExit(_selftest())
    if argv:
        raise SystemExit(f"unknown argument {argv[0]!r} (only --selftest / --help)")
    verdict, lines = evaluate()
    print("\n".join(lines))
    raise SystemExit({"QUIET": 0, "FIRE": 1, "BLIND": 2}[verdict])


if __name__ == "__main__":
    main(sys.argv[1:])
