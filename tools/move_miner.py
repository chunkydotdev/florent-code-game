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

⛔⛔ RANKING REBUILT 2026-08-17 (s48 WRAP-FIX, debt 15) AFTER RESEARCH MEASURED IT
INVERTED RELATIVE TO STUDY VALUE (docs/coordination.md 05:21:54Z + 05:30:55Z).
Two compounding defects, and both got worse for exactly the same candidates:

  1. COVERAGE RESET ON *THEIR* VERSION BUMP AND NEVER ON *OURS*. Our version
     churns far faster than theirs, so "unstudied games on their current version"
     accumulated FASTEST for opponents whose version is STABLE and whom we played
     heavily in the PAST — precisely the stale ground. Measured on the shipped
     tool: the top three were `arsonist duck` (60 of 160 games at a
     current-lineage `ourver`), `Kings College Munich` (0 of 95) and
     `OopsGotYourElo` (0 of 140), and all three sat OUTSIDE the admissible target
     band. The three we could actually learn from ranked 4th, 5th and 6th.
     ⚠ AND A LIVENESS CHECK ON *THEM* WOULD HAVE PASSED ALL EIGHT — every one had
     played a league match within the hour. The staleness is on OUR side of the
     pairing, which is why s47's "add a recency term" would not have caught it.
  2. "THEIR CURRENT VERSION" WAS INFERRED FROM *OUR* TAPE, so it froze at our
     last pairing. It named `lingling_40h` v61; they had left v61 eight hours
     earlier and were on v66. The same run named Kings College Munich v8 (league:
     v21) and OopsGotYourElo v21 (league: v39) — studies of versions nobody runs.

TRIGGER RULES (thresholds pinned here, not in any caller):
  * The COUNTED population is games at a MODERN `ourver` — one whose FIRST
    appearance on the tape is within MODERN_DAYS. That is the load-bearing fix:
    a bot three incumbents ago losing to a team we no longer meet is archaeology,
    not a move to mine.
  * FIRE  if an (opp, latest-oppver-WE-HAVE-PLAYED) cell holds >= 40 unstudied
          MODERN games, OR >= 20 while our share against that opponent is < 45%.
  * SUPPRESSED, NEVER SILENT: a candidate that clears the raw threshold but is
    dropped for zero modern coverage or for paying under the target-value floor
    is PRINTED with its reason. A ranker that silently drops candidates hides its
    own bug — a successor cannot tell an empty list from a filtered one.
  * Ranking: modern_unstudied · badness · recency · payout, where
      badness = 1 + max(0, 50 - share)/25          (adverse games teach more)
      recency = 0.5 ** (days_since_WE_played / RECENCY_HALFLIFE_D)
      payout  = (rating points a 5-0 pays) / 16    (16 = parity, so ~1.0)
  * THEIR CURRENT VERSION IS READ LEAGUE-WIDE from corpus/league_matches.tsv,
    never from our own pairings, and BOTH are printed. The GAP between "their
    current vN" and "our newest games are vM" IS the staleness signal.
  * BLIND, exit 2, if the tape is missing, unparseable, or its newest row is
    older than 24 h — a stale tape silently under-counts every cell, and an
    alarm that cannot tell it is blind is this repo's most-repeated defect.

⚠ LEAGUE-TAIL CAVEAT (research, 2026-08-17T05:26:06Z): the last ~2.5 h of
`corpus/league_matches.tsv` is PARTIAL, not merely lagged. Everything read from
it here is a PRESENCE claim (the newest version actually observed), which that
caveat does not touch; no branch turns on an absence.

Exit: 0 = no candidate above threshold · 1 = candidates printed · 2 = BLIND.
A cancelled/absent ledger file is NOT blind — it means nothing has ever been
studied, which is exactly when this tool should fire loudest.
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__)
        raise SystemExit(0)

ROOT = Path(__file__).resolve().parent.parent
TAPE = ROOT / "corpus" / "ladder_games.tsv"
LEDGER = ROOT / "docs" / "research" / "move-mining-ledger.tsv"
LEAGUE = ROOT / "corpus" / "league_matches.tsv"

FIRE_UNSTUDIED = 40
FIRE_ADVERSE_UNSTUDIED = 20
ADVERSE_SHARE_PCT = 45.0
STALE_H = 24.0

# ⭐ THE MODERN ERA IS DERIVED FROM THE DATA, NOT HAND-PICKED. A version is
# MODERN if its first appearance on the tape is within this many days. Research's
# manual gate used `ourver >= 140`; at 3.0 days this rule reproduces exactly that
# set (140 first appears 2026-08-14T11:52, 125 and below are older), and unlike a
# pinned version number it does not go stale the next time we ship.
MODERN_DAYS = 3.0
RECENCY_HALFLIFE_D = 3.0    # days since WE last met them; halves the score each
MIN_MODERN_FOR_SHARE = 20   # below this, badness falls back to the all-time share
PARITY_PAYOUT = 16.0        # a 5-0 at parity pays K/2 = 16, so payfac ~ 1.0 there


def _parse_tape(tape: Path):
    """-> (rows, newest_created_iso) or (None, reason) on blind.

    row = (opp, oppver, created, won, ourver)
    """
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
        rows.append((p[2], p[3], p[1], p[9], p[4]))
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


def _dt(iso: str) -> datetime | None:
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
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


def _modern_ourvers(rows, now: datetime) -> set[str]:
    """Our versions whose FIRST appearance on the tape is within MODERN_DAYS.

    ⛔ FIRST appearance, not last: a version that debuted a week ago is a week-old
    bot even if it played this morning, and games against it teach us about a tree
    we no longer ship.
    """
    first: dict[str, str] = {}
    for _opp, _ver, created, _won, ourver in rows:
        if ourver and (ourver not in first or created < first[ourver]):
            first[ourver] = created
    cut = now - timedelta(days=MODERN_DAYS)
    out = set()
    for v, c in first.items():
        d = _dt(c)
        if d is not None and d >= cut:
            out.add(v)
    return out


def _league_current(league: Path) -> dict[str, tuple[str, str]]:
    """{team: (createdAt, version)} — the newest version each team has been
    OBSERVED running, LEAGUE-WIDE. Never from our own pairings: a version derived
    from our tape freezes at our last meeting (defect #2)."""
    cur: dict[str, tuple[str, str]] = {}
    try:
        lines = league.read_text().splitlines()
    except OSError:
        return cur
    if not lines:
        return cur
    hdr = lines[0].split("\t")
    try:
        i_when = hdr.index("createdAt")
        cols = [(hdr.index("teamAName"), hdr.index("teamAVersion")),
                (hdr.index("teamBName"), hdr.index("teamBVersion"))]
    except ValueError:
        return cur
    for ln in lines[1:]:
        p = ln.split("\t")
        if len(p) <= i_when:
            continue
        when = p[i_when]
        for i_n, i_v in cols:
            if len(p) <= max(i_n, i_v):
                continue
            name, ver = p[i_n], p[i_v]
            if name and ver and when > cur.get(name, ("", ""))[0]:
                cur[name] = (when, ver)
    return cur


def _lookup_ratings() -> tuple[float, dict[str, float], str]:
    """(our rating, {team: rating}, note). Reuses the gate CLAUDE.md already
    mandates before every prereg rather than re-deriving payout here."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import target_value as tv
        ours, ratings = tv._live_ratings()
        if not ours or not ratings:
            return 0.0, {}, "ratings unavailable"
        return ours, ratings, ""
    except Exception as e:                                    # noqa: BLE001
        return 0.0, {}, f"ratings unavailable ({type(e).__name__})"


def _payout(gap: float) -> float:
    return 32.0 * (1.0 - 1.0 / (1.0 + 10 ** (-gap / 400.0)))


def _admissible(gap: float) -> tuple[bool, str]:
    """The target-value gate, imported when available so one definition governs;
    the inline fallback keeps this tool usable if that import ever breaks."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import target_value as tv
        return tv.admissible(gap, 0.0)
    except Exception:                                         # noqa: BLE001
        pay = _payout(gap)
        if pay < 10.0:
            return False, f"a 5-0 pays only {pay:.2f} (< 10)"
        if not (-80 <= gap <= 125):
            return False, "outside band"
        return True, ""


def evaluate(tape: Path = TAPE, ledger: Path = LEDGER,
             now: datetime | None = None, league: Path = LEAGUE,
             ratings: dict[str, float] | None = None,
             ours: float | None = None):
    """-> (verdict, lines). verdict in {'BLIND','FIRE','QUIET'}.

    `ratings`/`ours` are the injection point for the selftest; left None they are
    read live so the payout gate is applied to the ratings that actually hold.
    """
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

    rating_note = ""
    if ratings is None:
        ours, ratings, rating_note = _lookup_ratings()
    ours = ours or 0.0

    modern = _modern_ourvers(rows, now)
    per_opp: dict[str, list[int]] = {}
    per_opp_mod: dict[str, list[int]] = {}
    per_cell: dict[tuple[str, str], int] = {}
    per_cell_mod: dict[tuple[str, str], int] = {}
    latest_ver: dict[str, tuple[str, str]] = {}   # opp -> (created, oppver)
    last_met: dict[str, str] = {}
    ourvers_vs: dict[str, set[str]] = {}
    for opp, ver, created, won, ourver in rows:
        w = 1 if won in ("1", "True", "true") else 0
        a = per_opp.setdefault(opp, [0, 0]); a[0] += 1; a[1] += w
        per_cell[(opp, ver)] = per_cell.get((opp, ver), 0) + 1
        ourvers_vs.setdefault(opp, set()).add(ourver)
        if ourver in modern:
            m = per_opp_mod.setdefault(opp, [0, 0]); m[0] += 1; m[1] += w
            per_cell_mod[(opp, ver)] = per_cell_mod.get((opp, ver), 0) + 1
        if opp not in latest_ver or created > latest_ver[opp][0]:
            latest_ver[opp] = (created, ver)
        if created > last_met.get(opp, ""):
            last_met[opp] = created

    cov = _parse_ledger(ledger)
    cur_ver = _league_current(league)
    league_note = "" if cur_ver else (
        f"⚠ {league.name} unreadable/empty — THEIR CURRENT VERSION IS UNKNOWN "
        f"this run, so a candidate may name a version they have abandoned.")

    cands, suppressed = [], []
    for opp, (_, ver) in latest_ver.items():
        cell = per_cell[(opp, ver)]
        cell_mod = per_cell_mod.get((opp, ver), 0)
        covered = cov.get((opp, ver), 0)
        # coverage is recorded per (opp, oppver) without an era column, so a study
        # is charged against the modern games first — the conservative direction:
        # it can only ever UNDER-state how much is left to learn.
        unstudied_raw = cell - covered
        unstudied_mod = max(0, cell_mod - covered)
        n_all, w_all = per_opp[opp]
        n_mod, w_mod = per_opp_mod.get(opp, [0, 0])
        share_all = 100.0 * w_all / n_all if n_all else 0.0
        share = (100.0 * w_mod / n_mod) if n_mod >= MIN_MODERN_FOR_SHARE else share_all
        share_src = "modern" if n_mod >= MIN_MODERN_FOR_SHARE else "all-time"
        met = _dt(last_met.get(opp, "")) or (now - timedelta(days=999))
        days = max(0.0, (now - met).total_seconds() / 86400.0)

        fires_raw = unstudied_raw >= FIRE_UNSTUDIED or (
            unstudied_raw >= FIRE_ADVERSE_UNSTUDIED and share_all < ADVERSE_SHARE_PCT)
        fires = unstudied_mod >= FIRE_UNSTUDIED or (
            unstudied_mod >= FIRE_ADVERSE_UNSTUDIED and share < ADVERSE_SHARE_PCT)

        their_now = cur_ver.get(opp)
        rating = ratings.get(opp) if ratings else None
        gap = (rating - ours) if (rating is not None and ours) else None
        pay = _payout(gap) if gap is not None else None
        payfac = (pay / PARITY_PAYOUT) if pay is not None else 1.0

        drop = ""
        if cell_mod == 0:
            # numeric sort: a lexicographic one printed "ourver 102..94"
            spans = sorted((v for v in ourvers_vs[opp] if v),
                           key=lambda s: (0, int(s)) if s.isdigit() else (1, 0))
            drop = (f"ZERO of {cell} games at a MODERN ourver "
                    f"(we played them on ourver "
                    f"{spans[0] if spans else '?'}..{spans[-1] if spans else '?'}; "
                    f"modern = first seen < {MODERN_DAYS:.0f}d ago) — archaeology")
        elif not fires:
            drop = (f"only {unstudied_mod} unstudied MODERN of {unstudied_raw} raw "
                    f"(bar {FIRE_UNSTUDIED}, or {FIRE_ADVERSE_UNSTUDIED} at "
                    f"share<{ADVERSE_SHARE_PCT:.0f}%)")
        elif gap is not None:
            ok, why = _admissible(gap)
            if not ok:
                drop = (f"target value: gap {gap:+.0f}, {why} — the best possible "
                        f"outcome of this study cannot be converted into rating")

        rec = dict(opp=opp, ver=ver, cell=cell, cell_mod=cell_mod,
                   unstudied_raw=unstudied_raw, unstudied_mod=unstudied_mod,
                   share=share, share_src=share_src, n_all=n_all, n_mod=n_mod,
                   days=days, gap=gap, pay=pay, their_now=their_now, drop=drop)
        if drop:
            if fires_raw or fires:
                suppressed.append(rec)
            continue
        badness = 1.0 + max(0.0, 50.0 - share) / 25.0
        recency = 0.5 ** (days / RECENCY_HALFLIFE_D)
        rec["score"] = unstudied_mod * badness * recency * payfac
        rec["rating_unknown"] = gap is None
        cands.append(rec)

    def _detail(r):
        out = []
        pay = (f"gap {r['gap']:+.0f}, a 5-0 pays {r['pay']:+.2f}"
               if r["gap"] is not None else
               "⚠ RATING UNKNOWN — the payout gate could NOT be applied")
        out.append(f"        share {r['share']:.1f}% ({r['share_src']}, "
                   f"n={r['n_mod'] if r['share_src'] == 'modern' else r['n_all']}) · "
                   f"we last played them {r['days']:.1f}d ago · {pay}")
        if r["their_now"] is None:
            out.append(f"        ⚠ they do not appear in {league.name} — current "
                       f"version UNCONFIRMED (our tape says v{r['ver']})")
        elif r["their_now"][1] != r["ver"]:
            out.append(f"        ⚠ THEY NOW RUN v{r['their_now'][1]} (league, seen "
                       f"{r['their_now'][0][:16]}) — our newest games against them "
                       f"are v{r['ver']}: LINEAGE evidence, not current-opponent")
        else:
            out.append(f"        ✅ their current version IS v{r['ver']} "
                       f"(league, seen {r['their_now'][0][:16]})")
        return out

    tail = []
    if suppressed:
        suppressed.sort(key=lambda r: -r["unstudied_raw"])
        tail.append(f"   SUPPRESSED ({len(suppressed)}) — printed, never silent: a "
                    f"ranker that drops candidates without saying so hides its own bug")
        for r in suppressed[:8]:
            tail.append(f"     {r['opp']!r} v{r['ver']}: {r['unstudied_raw']} "
                        f"unstudied raw — DROPPED: {r['drop']}")
    if league_note:
        tail.append("   " + league_note)
    if rating_note:
        tail.append(f"   ⚠ {rating_note} — the payout gate was NOT applied this run")

    if not cands:
        return "QUIET", [
            f"move_miner QUIET — no (opp, latest-ver) cell holds "
            f">={FIRE_UNSTUDIED} unstudied MODERN games "
            f"(>={FIRE_ADVERSE_UNSTUDIED} if share<{ADVERSE_SHARE_PCT:.0f}%), "
            f"admissible as a target. tape age {age:.1f}h."] + tail
    cands.sort(key=lambda r: -r["score"])
    out = [f"*** MOVE-MINING CANDIDATES ({len(cands)}) — study the top one "
           f"per docs/research/PLAYBOOK-move-mining-2026-08-16.md ***  "
           f"[tape age {age:.1f}h; MODERN = ourver first seen < "
           f"{MODERN_DAYS:.0f}d ago, {len(modern)} versions]"]
    for r in cands[:8]:
        out.append(f"   score {r['score']:7.1f}  {r['opp']!r} v{r['ver']}: "
                   f"{r['unstudied_mod']} unstudied MODERN of {r['cell_mod']} "
                   f"(raw {r['unstudied_raw']} of {r['cell']} on this version)")
        out.extend(_detail(r))
    return "FIRE", out + tail


# --------------------------- selftest ---------------------------------------
def _selftest() -> int:
    import tempfile
    ok = True

    def chk(label, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print(f"  [{'ok' if good else 'FAIL'}] {label:64s} got={got} want={want}")

    now = datetime(2026, 8, 16, 12, 0, tzinfo=timezone.utc)
    hdr = "match\tcreated\topp\toppver\tourver\tourbef\toppbef\tmap\twinner_seat\twon\tcond\tturns\ts3\n"
    # every fixture opponent sits at parity unless a cell says otherwise, so the
    # payout gate is NEUTRAL by default and only the cell that tests it moves it.
    RAT = {"teamX": 1700.0, "teamY": 1700.0, "teamZ": 1700.0,
           "A": 1700.0, "B": 1700.0, "far": 800.0}
    OURS = 1700.0

    def tape_of(rows):
        """rows = (opp, oppver, won[, ourver, created])."""
        f = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
        f.write(hdr)
        # distinct, increasing created stamps — with equal stamps the
        # latest-version tie-break keeps first-seen, which is exactly the
        # case the version-bump test exists to drive.
        for i, r in enumerate(rows):
            opp, ver, won = r[0], r[1], r[2]
            ourver = r[3] if len(r) > 3 else "155"
            created = r[4] if len(r) > 4 else (
                f"2026-08-16T{i // 3600:02d}:{(i // 60) % 60:02d}:{i % 60:02d}.{i:03d}Z")
            f.write(f"m\t{created}\t{opp}\t{ver}\t{ourver}\t1\t1\tmap\tA\t{won}\tcore_destroyed\t100\t-\n")
        f.close()
        return Path(f.name)

    def ledger_of(entries):
        f = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
        f.write("date\topp\toppver\tgames_covered\tdoc\n")
        for opp, ver, n in entries:
            f.write(f"2026-08-16\t{opp}\t{ver}\t{n}\tdoc.md\n")
        f.close()
        return Path(f.name)

    def league_of(entries):
        """entries = (team, version, createdAt)."""
        f = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
        f.write("id\tcreatedAt\tteamAName\tteamAVersion\tteamBName\tteamBVersion\n")
        for team, ver, when in entries:
            f.write(f"x\t{when}\t{team}\t{ver}\tsomeone\t1\n")
        f.close()
        return Path(f.name)

    NOLEAGUE = Path("/nonexistent-league")

    def ev(t, l=Path("/nonexistent-ledger"), n=now, lg=NOLEAGUE,
           ratings=RAT, ours=OURS):
        return evaluate(t, l, n, lg, ratings, ours)

    # 1) 60 unstudied MODERN games, no ledger -> FIRE
    t = tape_of([("teamX", "5", "1")] * 30 + [("teamX", "5", "0")] * 30)
    v, _ = ev(t)
    chk("60 unstudied, no ledger file -> FIRE", v, "FIRE")
    # 2) same fully covered -> QUIET (the guard's safe case, driven)
    v, _ = ev(t, ledger_of([("teamX", "5", 60)]))
    chk("same 60 covered by ledger -> QUIET", v, "QUIET")
    # 3) version bump resets coverage: 25 games on NEW ver, share 30 -> FIRE
    t3 = tape_of([("teamY", "1", "1")] * 30 + [("teamY", "1", "0")] * 45
                 + [("teamY", "2", "0")] * 20 + [("teamY", "2", "1")] * 5)
    v, lines = ev(t3, ledger_of([("teamY", "1", 75)]))
    chk("25 games on unstudied NEW version, adverse -> FIRE", v, "FIRE")
    chk("...and the candidate line names the NEW version", any("v2" in l for l in lines), True)
    # 4) 25 unstudied but share 55 (not adverse, under 40) -> QUIET
    t4 = tape_of([("teamZ", "3", "1")] * 14 + [("teamZ", "3", "0")] * 11)
    v, _ = ev(t4, ledger_of([]))
    chk("25 unstudied at healthy share -> QUIET", v, "QUIET")
    # 5) stale tape -> BLIND, not QUIET
    v, lines = ev(t, Path("/nonexistent"), datetime(2026, 8, 18, 12, 0, tzinfo=timezone.utc))
    chk("48h-old tape -> BLIND (never QUIET)", v, "BLIND")
    chk("...and BLIND says the verdict is unknown", "UNKNOWN" in lines[0], True)
    # 6) missing tape -> BLIND
    v, _ = ev(Path("/nonexistent-tape"))
    chk("missing tape -> BLIND", v, "BLIND")

    # ---- DEFECT 1: OUR-VERSION COVERAGE, DRIVEN BOTH WAYS ------------------
    # The SAME 60 adverse games, the same opponent, the same threshold: modern
    # ourver fires, archaic ourver does not. If this cell could only ever push one
    # way it would not have been seen to work.
    old = "2026-08-09T00:00:00.000Z"     # 7 days before `now` -> ourver 90 is stale
    # ...plus a handful of FRESH rows against someone else, or the tape's newest
    # row would be 7 days old and this cell would read BLIND for the wrong reason
    # (it did, on first run — the fixture was testing the staleness guard, not the
    # coverage term).
    fresh_filler = [("filler", "1", "1", "155")] * 3
    t7 = tape_of([("teamX", "5", "0", "90", old)] * 40
                 + [("teamX", "5", "1", "90", old)] * 20 + fresh_filler)
    v, lines = ev(t7)
    chk("60 adverse games at an ARCHAIC ourver -> QUIET", v, "QUIET")
    chk("...and the dropped candidate is PRINTED, not silent",
        any("teamX" in l and "DROPPED" in l for l in lines), True)
    chk("...naming zero-modern-coverage as the reason",
        any("ZERO of 60" in l for l in lines), True)
    t8 = tape_of([("teamX", "5", "0", "155")] * 40 + [("teamX", "5", "1", "155")] * 20)
    v, _ = ev(t8)
    chk("THE SAME 60 games at a MODERN ourver -> FIRE", v, "FIRE")

    # ---- DEFECT: PAYOUT TERM, DRIVEN BOTH WAYS -----------------------------
    t9 = tape_of([("far", "7", "0")] * 40 + [("far", "7", "1")] * 20)
    v, lines = ev(t9)
    chk("a candidate 900 points below us -> QUIET (payout)", v, "QUIET")
    chk("...and the payout drop is PRINTED with its gap",
        any("target value" in l and "far" in l for l in lines), True)
    v, _ = ev(t9, ratings={"far": 1690.0})
    chk("THE SAME candidate at parity -> FIRE", v, "FIRE")
    # ...and when we cannot price it at all, the tool says so rather than
    # silently ranking as if the gate had passed.
    v, lines = ev(t9, ratings={})
    chk("an UNPRICEABLE candidate still fires, flagged", v, "FIRE")
    chk("...and says the payout gate could not be applied",
        any("RATING UNKNOWN" in l for l in lines), True)

    # ---- RECENCY ON OUR SIDE, DRIVEN BOTH WAYS -----------------------------
    # Two identical candidates inside the modern window; only the date WE last
    # met them differs. Both orderings are asserted, so the term cannot be a
    # constant that happens to agree with the volume ordering.
    recent, older = "2026-08-16T08:00:00.000Z", "2026-08-14T00:00:00.000Z"
    tA = tape_of([("A", "1", "0", "160", recent)] * 40 + [("A", "1", "1", "160", recent)] * 20
                 + [("B", "1", "0", "161", older)] * 40 + [("B", "1", "1", "161", older)] * 20)
    _, lines = ev(tA)
    first = [l for l in lines if "score " in l][0]
    chk("the opponent we met TODAY outranks the one from 2.5d ago", "'A'" in first, True)
    tB = tape_of([("A", "1", "0", "160", older)] * 40 + [("A", "1", "1", "160", older)] * 20
                 + [("B", "1", "0", "161", recent)] * 40 + [("B", "1", "1", "161", recent)] * 20)
    _, lines = ev(tB)
    first = [l for l in lines if "score " in l][0]
    chk("...and swapping the dates swaps the ranking", "'B'" in first, True)

    # ---- DEFECT 2: THEIR VERSION COMES FROM THE LEAGUE, DRIVEN BOTH WAYS ---
    lg_moved = league_of([("teamX", "9", "2026-08-16T11:00:00.000Z")])
    v, lines = ev(t8, lg=lg_moved)
    chk("their league version v9 vs our tape v5 -> FIRE with a warning", v, "FIRE")
    chk("...and it names BOTH versions, which is the staleness signal",
        any("THEY NOW RUN v9" in l for l in lines), True)
    lg_same = league_of([("teamX", "5", "2026-08-16T11:00:00.000Z")])
    v, lines = ev(t8, lg=lg_same)
    chk("...and when they are still on v5 the warning does NOT fire",
        any("THEY NOW RUN" in l for l in lines), False)
    chk("...it confirms the version instead",
        any("their current version IS v5" in l for l in lines), True)
    v, lines = ev(t8, lg=NOLEAGUE)
    chk("an unreadable league file is announced, not assumed",
        any("current version is unknown" in l.lower() for l in lines), True)

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
