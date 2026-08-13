#!/usr/bin/env python3
"""ship_ledger.py — cumulative Elo since a holder's activation, and leaked
rated matches.

    tools/ship_ledger.py --since <ISO8601Z> [--holder vN | --holder N] \\
                          [--tsv <path>] [--json]
    tools/ship_ledger.py --selftest

WHY THIS EXISTS. `tools/slot_rule.py` (armed at `tools/monitors/ship_watch.py`)
is a ROLLING 5-MATCH SLOPE. Per `ship_watch.py:112-120` that slope RELAXES as a
bad result ages out of the window, and a steady bleed slower than -4.2/match
holds `net5` above the -21 swap threshold FOREVER while still losing hundreds of
Elo. This tool is the LEVEL statistic the slope cannot see: cumulative Elo since
activation, summed match-by-match from the exact, already-verified model
(`delta = 32 * (S - E)`, K=32, max |residual| 0.000000 over 100 matches — see
the model check in `--selftest`, cell 3).

It also answers a distinct question the slot rule does not ask at all: were any
RATED LADDER MATCHES played by a version that was not the intended holder? The
"rated cost is zero" claim in CLAUDE.md was falsified once already (s28,
-24.67 Elo across 3 leaked matches from an arm rotation) — this is the general
instrument for catching that again, not a one-off grep.

THE READ, per CLAUDE.md's own instruction: per-match `ourver` off
`corpus/ladder_games.tsv`, never the elo tape's poll-time version tag (that tag
records who was active WHEN SAMPLED, not who played the match — the exact
defect documented at the top of `tools/slot_rule.py`).

THREE GUARDS, each enforced, none decorative:
  1. HOLDER READ LIVE. `--holder` is optional; when omitted this reads
     `.venv/bin/fcode status` and parses the `Active bot:` line, gating on the
     LINE'S PRESENCE, never the subprocess exit code — `fcode status` exits 0
     while printing `Error: True` on this platform (standing repo rule). No
     holder is ever hardcoded.
  2. REFUSE ON A STALE TAPE. `corpus/ladder_games.tsv` is refreshed by a keeper
     whose net pull fires every ~6th cycle, so its age SAWTOOTHS to ~85 minutes
     BY DESIGN. If the newest `created` row is older than 170 minutes (~2
     cadences), this refuses to print a verdict (exit 3). The freshness line is
     printed on EVERY run, pass or fail — a monitor that reads a file must
     report that file's freshness.
  3. `0 leaked` != `0 rows`. The number of matches examined in the window is
     always printed, and an empty window says so explicitly rather than
     printing a silently-vacuous "0 leaks".

A match with fewer than 5 game rows present is INCOMPLETE. It is counted (games
played, games won) but excluded from the Elo sum, which needs all 5 results to
compute S — and reported as its own line so a reader can see it was excluded,
not lost.
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LADDER = ROOT / "corpus" / "ladder_games.tsv"
FCODE = str(ROOT / ".venv" / "bin" / "fcode")

STALE_LIMIT_MIN = 170


# ===========================================================================
# Live holder — never hardcoded.
# ===========================================================================

def read_live_holder() -> str | None:
    """Parse the `Active bot: vNNN (...)` line from `fcode status`. Returns the
    bare version digits ("122") or None if the line cannot be found — which is
    a BLIND state, not a guess. Gates on the LINE'S PRESENCE, never on the
    subprocess exit code (this CLI exits 0 while printing `Error: True`)."""
    try:
        r = subprocess.run([FCODE, "status"], cwd=ROOT, capture_output=True,
                           text=True, timeout=60)
    except Exception:
        return None
    for line in r.stdout.splitlines():
        if "Active bot:" in line:
            rest = line.split("Active bot:", 1)[1].strip()
            tok = rest.split()[0] if rest else ""
            if tok.lower().startswith("v") and tok[1:].isdigit():
                return tok[1:]
            if tok.isdigit():
                return tok
    return None


def normalize_holder(raw: str) -> str:
    """'v116', 'V116' or '116' -> '116', matching how `ourver` is stored in the
    tape (bare digits, no 'v')."""
    raw = raw.strip()
    if raw[:1].lower() == "v":
        raw = raw[1:]
    return raw


# ===========================================================================
# The tape.
# ===========================================================================

def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def parse_iso(s: str) -> datetime:
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


def newest_created_age_min(rows: list[dict], now: datetime | None = None):
    """(age_minutes, newest_dt) off the DATA (the `created` column), or
    (None, None) if there is nothing to read. Two clocks are deliberately not
    conflated here: this is the data clock, not file mtime — a daemon that
    rewrites the file with nothing new would keep mtime fresh forever."""
    now = now or datetime.now(timezone.utc)
    stamps = []
    for r in rows:
        c = r.get("created")
        if not c:
            continue
        try:
            stamps.append(parse_iso(c))
        except ValueError:
            continue
    if not stamps:
        return None, None
    newest = max(stamps)
    return (now - newest).total_seconds() / 60.0, newest


def check_staleness(rows: list[dict], now: datetime | None = None,
                    limit_min: float = STALE_LIMIT_MIN):
    """(ok, age_min, message). ok=False means DO NOT PRINT A VERDICT — the
    caller must refuse and exit(3). age_min is None only when the tape has no
    parseable `created` value at all (also refuses)."""
    age_min, newest = newest_created_age_min(rows, now=now)
    if age_min is None:
        return False, None, "BLIND: ladder tape has no parseable `created` timestamp"
    if age_min > limit_min:
        return (False, age_min,
                f"STALE: newest ladder row is {age_min:.1f} min old "
                f"(> {limit_min:g}) — REFUSING to print a verdict")
    return (True, age_min,
            f"freshness: newest ladder row is {age_min:.1f} min old "
            f"(limit {limit_min:g})")


def build_matches(rows: list[dict]) -> list[dict]:
    """Group game rows into one summary per match, sorted by `created`.

    S (game share) and delta are None for an INCOMPLETE match (< 5 game rows
    present) — never silently treated as a loss.
    """
    grouped: dict[str, list[dict]] = {}
    order: list[str] = []
    for r in rows:
        mid = r.get("match")
        if not mid:
            continue
        if mid not in grouped:
            grouped[mid] = []
            order.append(mid)
        grouped[mid].append(r)

    out = []
    for mid in order:
        games = grouped[mid]
        first = games[0]
        n = len(games)
        won = sum(1 for g in games if g.get("won") == "1")
        try:
            ourbef = float(first["ourbef"])
            oppbef = float(first["oppbef"])
        except (KeyError, ValueError, TypeError):
            continue
        E = 1.0 / (1.0 + 10 ** ((oppbef - ourbef) / 400.0))
        complete = n == 5
        S = (won / 5.0) if complete else None
        delta = 32 * (S - E) if complete else None
        out.append({
            "match": mid, "created": first.get("created", ""),
            "opp": first.get("opp", ""), "ourver": first.get("ourver", ""),
            "ourbef": ourbef, "oppbef": oppbef,
            "n_games": n, "won": won, "complete": complete,
            "S": S, "E": E, "delta": delta,
        })
    out.sort(key=lambda m: m["created"])
    return out


def in_window(matches: list[dict], since_dt: datetime) -> list[dict]:
    filtered = []
    for m in matches:
        if not m["created"]:
            continue
        try:
            c = parse_iso(m["created"])
        except ValueError:
            continue
        if c >= since_dt:
            filtered.append(m)
    return filtered


# ===========================================================================
# LEDGER (question A) and LEAKS (question B).
# ===========================================================================

def build_ledger(holder_matches: list[dict]) -> dict:
    complete = [m for m in holder_matches if m["complete"]]
    incomplete = [m for m in holder_matches if not m["complete"]]
    total_games = sum(m["n_games"] for m in holder_matches)
    games_won = sum(m["won"] for m in holder_matches)
    game_share = (games_won / total_games) if total_games else None
    cum_delta = sum(m["delta"] for m in complete)
    mean_delta = (cum_delta / len(complete)) if complete else None
    created = [m["created"] for m in holder_matches if m["created"]]
    return {
        "n_matches": len(holder_matches),
        "n_complete": len(complete),
        "n_incomplete": len(incomplete),
        "incomplete": incomplete,
        "total_games": total_games,
        "games_won": games_won,
        "game_share": game_share,
        "cumulative_delta": cum_delta,
        "mean_delta_per_match": mean_delta,
        "first_created": min(created) if created else None,
        "last_created": max(created) if created else None,
    }


def build_leaks(leaked_matches: list[dict]) -> dict:
    complete = [m for m in leaked_matches if m["complete"]]
    incomplete = [m for m in leaked_matches if not m["complete"]]
    total = sum(m["delta"] for m in complete)
    return {
        "n_examined": len(leaked_matches),
        "n_complete": len(complete),
        "n_incomplete": len(incomplete),
        "matches": leaked_matches,
        "total_delta": total,
    }


# ===========================================================================
# Reporting.
# ===========================================================================

def format_report(holder: str, since: str,
                  windowed_n: int, ledger: dict, leaks: dict) -> str:
    lines = []
    lines.append(f"holder: v{holder}   since: {since}")
    if windowed_n == 0:
        lines.append("NO ROWS IN WINDOW — 0 matches with created >= since")
    else:
        lines.append(f"matches examined in window: {windowed_n}")
    lines.append("")

    lines.append("=== LEDGER (cumulative Elo since activation) ===")
    lines.append(f"  holder v{holder}: {ledger['n_matches']} match(es) "
                 f"({ledger['n_complete']} complete, {ledger['n_incomplete']} incomplete)")
    if ledger["n_incomplete"]:
        lines.append(f"  ** {ledger['n_incomplete']} INCOMPLETE match(es) excluded "
                     f"from the Elo sum (games played/won still counted below):")
        for m in ledger["incomplete"]:
            lines.append(f"       {m['created']}  {m['match']}  vs {m['opp']}  "
                         f"{m['n_games']}/5 games present")
    if ledger["total_games"]:
        share = ledger["game_share"]
        lines.append(f"  games: {ledger['games_won']}/{ledger['total_games']} won "
                     f"(game share {share:.3f})")
    else:
        lines.append("  games: none")
    if ledger["n_complete"]:
        lines.append(f"  cumulative Elo delta: {ledger['cumulative_delta']:+.2f}  "
                     f"(mean {ledger['mean_delta_per_match']:+.2f}/match over "
                     f"{ledger['n_complete']} complete match(es))")
    else:
        lines.append("  cumulative Elo delta: n/a (no complete matches)")
    if ledger["first_created"]:
        lines.append(f"  span: {ledger['first_created']} .. {ledger['last_created']}")
    lines.append("")

    lines.append("=== LEAKS (rated matches NOT played by the holder) ===")
    lines.append(f"  matches examined: {leaks['n_examined']}")
    if leaks["n_examined"] == 0:
        lines.append("  0 leaks (0 rows examined for non-holder versions in window)")
    else:
        for m in leaks["matches"]:
            if m["complete"]:
                lines.append(f"    {m['created']}  ourver={m['ourver']}  opp={m['opp']}  "
                             f"S={m['S']:.3f}  E={m['E']:.4f}  delta={m['delta']:+.2f}")
            else:
                lines.append(f"    {m['created']}  ourver={m['ourver']}  opp={m['opp']}  "
                             f"INCOMPLETE ({m['n_games']}/5 games) — delta not computed")
        if leaks["n_incomplete"]:
            lines.append(f"  ({leaks['n_incomplete']} incomplete leaked match(es) excluded "
                         f"from TOTAL below)")
        lines.append(f"  TOTAL: {leaks['n_complete']} leaked complete match(es), "
                     f"{leaks['total_delta']:+.2f} Elo")
    return "\n".join(lines)


# ===========================================================================
# Selftest — mandatory, and pre-named on real data (corpus/ladder_games.tsv).
# ===========================================================================

def selftest() -> int:
    print("SHIP_LEDGER SELFTEST\n")
    bad = 0

    def check(label, got, want):
        nonlocal bad
        ok = got == want
        if not ok:
            bad += 1
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<62} got={got!r} want={want!r}")

    def check_close(label, got, want, tol):
        nonlocal bad
        ok = got is not None and abs(got - want) <= tol
        if not ok:
            bad += 1
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<62} got={got!r} want~={want!r} (tol {tol})")

    rows = load_rows(LADDER)
    if not rows:
        print(f"  CANNOT RUN: {LADDER} has no rows")
        return 1
    matches = build_matches(rows)

    # ---- CELL 1: the known-positive cell -------------------------------
    since_dt = parse_iso("2026-08-12T19:00:00Z")
    holder = "116"
    windowed = in_window(matches, since_dt)
    leaked = [m for m in windowed if m["ourver"] != holder]
    leaks = build_leaks(leaked)
    check("cell1: exactly 2 leaked matches", leaks["n_complete"], 2)
    check("cell1: all leaked matches are ourver=120",
          all(m["ourver"] == "120" for m in leaks["matches"]), True)
    check_close("cell1: leaked total ~= -8.01 Elo", leaks["total_delta"], -8.01, 0.05)
    if leaks["n_complete"] == 2:
        d1, d2 = sorted((m["delta"] for m in leaks["matches"]))
        check_close("cell1: smaller-magnitude leak ~= -0.52", d1 if abs(d1) < abs(d2) else d2,
                    -0.52, 0.05)
        check_close("cell1: larger-magnitude leak ~= -7.49", d2 if abs(d2) > abs(d1) else d1,
                    -7.49, 0.05)
    print(f"       (this is the cell that proves the tool can return the "
          f"ALARMING verdict — {leaks['n_complete']} leak(s) found, "
          f"{leaks['total_delta']:+.2f} Elo)")

    # ---- CELL 2: the known-negative cell --------------------------------
    since_dt2 = parse_iso("2026-08-12T20:00:00Z")
    holder2 = "116"
    windowed2 = in_window(matches, since_dt2)
    leaked2 = [m for m in windowed2 if m["ourver"] != holder2]
    leaks2 = build_leaks(leaked2)
    check("cell2: examined count is nonzero (0 leaks != 0 rows)",
          leaks2["n_examined"] >= 0 and len(windowed2) > 0, True)
    check("cell2: zero leaks in this window", leaks2["n_examined"], 0)
    print(f"       (examined {len(windowed2)} matches in window, all ourver={holder2}, "
          f"0 leaked — distinguishable from an empty window)")

    # ---- CELL 3: the Elo model -------------------------------------------
    complete = [m for m in matches if m["complete"]]
    if len(complete) >= 100:
        resid = []
        for i in range(len(complete) - 1):
            cur, nxt = complete[i], complete[i + 1]
            predicted_next_ourbef = cur["ourbef"] + cur["delta"]
            resid.append(abs(nxt["ourbef"] - predicted_next_ourbef))
        max_resid = max(resid) if resid else None
        check(f"cell3: broad model check over {len(complete)} complete matches "
              f"({len(resid)} consecutive pairs) — max residual tiny",
              max_resid is not None and max_resid < 0.01, True)
        print(f"       (max |residual| = {max_resid:.6f} across {len(resid)} "
              f"consecutive-match pairs, all drawn from {LADDER.name})")
    else:
        print(f"       broader >=100-match check NOT RUN — only {len(complete)} "
              f"complete matches available; falling back to the two v120 matches.")
        S1, E1 = 0.600, 0.6164
        S2, E2 = 0.400, 0.6340
        check_close("cell3 (fallback): delta(S=0.600,E=0.6164) ~= -0.52",
                    32 * (S1 - E1), -0.52, 0.02)
        check_close("cell3 (fallback): delta(S=0.400,E=0.6340) ~= -7.49",
                    32 * (S2 - E2), -7.49, 0.02)

    # ---- CELL 4: staleness guard driven to ITS FIRING verdict ------------
    now = datetime(2026, 8, 13, 12, 0, tzinfo=timezone.utc)
    fresh_rows = [{"created": "2026-08-13T11:00:00Z"}]     # 60 min old
    stale_rows = [{"created": "2026-08-13T08:00:00Z"}]     # 240 min old
    ok_fresh, age_fresh, msg_fresh = check_staleness(fresh_rows, now=now)
    ok_stale, age_stale, msg_stale = check_staleness(stale_rows, now=now)
    check("cell4: fresh synthetic row -> ok=True", ok_fresh, True)
    check("cell4: stale synthetic row -> ok=False (REFUSES)", ok_stale, False)
    check("cell4: stale message says STALE and REFUSING",
          "STALE" in msg_stale and "REFUSING" in msg_stale, True)
    check_close("cell4: stale age computed correctly (240 min)", age_stale, 240.0, 0.5)
    print(f"       (guard driven to BOTH verdicts: fresh -> {msg_fresh!r}; "
          f"stale -> {msg_stale!r})")

    print()
    if bad:
        print(f"*** {bad} cell(s) FAILED ***")
        return 1
    print("PASS: all selftest cells passed.")
    return 0


# ===========================================================================
# CLI
# ===========================================================================

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--since")
    ap.add_argument("--holder")
    ap.add_argument("--tsv")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    if not args.since:
        print("--since is required (ISO8601Z, e.g. 2026-08-12T19:00:00Z)", file=sys.stderr)
        return 2
    try:
        since_dt = parse_iso(args.since)
    except ValueError as e:
        print(f"could not parse --since {args.since!r}: {e}", file=sys.stderr)
        return 2

    tsv_path = Path(args.tsv) if args.tsv else LADDER
    rows = load_rows(tsv_path)
    if not rows:
        msg = f"BLIND: could not read rows from {tsv_path}"
        if args.json:
            print(json.dumps({"blind": msg}, indent=2))
        else:
            print(msg)
        return 2

    # GUARD 2: refuse on a stale tape. Printed on EVERY run, pass or fail.
    # In --json mode the freshness line still goes to stderr so stdout stays
    # pure JSON, and the same message is embedded in the JSON body.
    ok, age_min, staleness_msg = check_staleness(rows)
    if args.json:
        print(staleness_msg, file=sys.stderr)
    else:
        print(staleness_msg)
    if not ok:
        if args.json:
            print(json.dumps({
                "staleness": {"ok": ok, "age_min": age_min, "message": staleness_msg},
            }, indent=2))
        return 3

    # GUARD 1: holder read live, never hardcoded.
    if args.holder:
        holder = normalize_holder(args.holder)
    else:
        raw = read_live_holder()
        if raw is None:
            msg = "BLIND: could not read the live holder"
            if args.json:
                print(json.dumps({"blind": msg}, indent=2))
            else:
                print(msg)
            return 2
        holder = raw

    matches = build_matches(rows)
    windowed = in_window(matches, since_dt)
    holder_matches = [m for m in windowed if m["ourver"] == holder]
    leaked_matches = [m for m in windowed if m["ourver"] != holder]

    ledger = build_ledger(holder_matches)
    leaks = build_leaks(leaked_matches)

    if args.json:
        print(json.dumps({
            "holder": holder, "since": args.since,
            "staleness": {"ok": ok, "age_min": age_min, "message": staleness_msg},
            "windowed_matches": len(windowed),
            "ledger": ledger, "leaks": leaks,
        }, default=str, indent=2))
    else:
        print(format_report(holder, args.since, len(windowed), ledger, leaks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
