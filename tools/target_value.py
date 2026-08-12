#!/usr/bin/env python3
"""TARGET VALUE GATE — what does beating this opponent actually PAY?

    .venv/bin/python tools/target_value.py vjg Troupe "The Bisons" 0033
    .venv/bin/python tools/target_value.py --band          # who is reachable
    .venv/bin/python tools/target_value.py --selftest

RUN THIS BEFORE WRITING A PRE-REGISTRATION. One line in the prereg:
    TARGET BAND: <opponents>, gaps <a..b>, win pays <x..y>, reachable YES/NO

WHY THIS EXISTS — and the case is s28 itself, not a hypothetical.
On 2026-08-10 we built and fired a crash-induction leg that passed **every check
this repo has**: pre-registered before the fact, 8 ADD-only amendments all blind
to the data, a placebo reading exactly 0/164, the dose delivered 150 times,
every control driven to the other verdict, lock cert two-clock clean, holder
asserted before every challenge, prototype exposure 10 seconds per cycle.

**It was aimed at four teams 550-860 points BELOW us, where a win pays ~0.2-1.0
rating points and a loss costs ~31.**

**The machinery inspects the EXPERIMENT and never asks whether the QUESTION is
worth answering.** No amount of rigour inside a leg reaches that, which is why
this is a gate in front of pre-registration rather than another clause inside
one. It takes thirty seconds and it would have redirected the whole session.

THE TWO FACTS IT ENCODES, both measured on our own tape:

1. **The ladder scores GAME SHARE: `delta = 32 x (S - E)`, S = games/5.**
   Verified residual 0.000000 across 100 matches (research: 0.0000 across 678).
   So the value of a matchup is not "can we win" but "how much margin moves".

2. **The ladder only pairs neighbours.** 94.0% of 678 matches within +-100;
   since passing 1600 the entire observed range is -78.1 to +122.3. **Anything
   outside ~`us-80 .. us+125` cannot be met** -- it is a destination, not an
   opponent.

NOT A VETO. A low-value target can still be the right leg (LOKI-14b's negative
closes a road properly, and closing a road is worth something). **The gate makes
you write the number down BEFORE the work, not defend it after.**
"""
from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FCODE = str(ROOT / ".venv" / "bin" / "fcode")
OUR_TEAM = "OpenSverige"

K = 32
BAND_LO, BAND_HI = -80, 125      # measured reachable window, relative to us

# ⭐ RE-DENOMINATED 2026-08-12 (s33) ON MAGNUS'S DIRECTIVE. WAS `RATING_FLOOR =
# 1650`, ABSOLUTE. It is now expressed in the quantity it was always protecting.
#
# THE ORIGINAL DIRECTIVE, unchanged in intent — Magnus, 2026-08-11: "Don't fire on
# targets below 1650 ELO." Its PURPOSE was that a win against a far-weaker team
# pays nothing: s28 fired a crash leg at four teams 550-860 points below us where
# a 5-0 paid 0.2-1.0 rating points.
#
# ⛔ WHY THE ABSOLUTE FORM HAD TO GO, AND IT IS A MEASURED FAILURE NOT A TIDY-UP.
# The thing it protects is RELATIVE (payout is a function of the GAP) while the
# threshold was ABSOLUTE, so it drifted every time OUR rating moved -- tightening
# hardest exactly when we are doing worst and most need reachable targets. At 1689
# it left 39 points of room below us; at 1666, 16; at 1645 it left NONE and
# excluded seven teams inside the reachable band. Measured 2026-08-12:
#
#     EXCLUDED by the 1650 floor     Askar City  gap  -5   a 5-0 paid +15.78
#                                    gsxWins     gap -37   a 5-0 paid +14.32
#                                    Lunds Stns  gap -76   a 5-0 paid +12.56
#     what the floor was BUILT to exclude    S   gap -714  a 5-0 pays   +0.52
#                                    vjg (s28)   gap -841  a 5-0 pays   +0.25
#
# It was excluding targets paying 12-16 points while written to exclude targets
# paying half a point -- 25-60x off its own intent. Predicted by the side lane's
# s32 S5 ("an absolute threshold beside a relative band changes meaning as the
# baseline moves") and it arrived exactly as predicted.
#
# ⇒ A PAYOUT THRESHOLD CANNOT DRIFT, because it is denominated in the thing the
# rule cares about. No boot rule is needed to "update" it; there is nothing to
# update. That is why this is a re-denomination and not a new constant.
MIN_PAYOUT = 10.0        # a 5-0 must pay at least this many rating points

# Derivation, so the number is auditable rather than picked: delta = K*(S - E)
# with S = 1, so payout >= 10 <=> E <= 0.6875 <=> the opponent is no more than
# ~137 points BELOW us. That admits every team the old floor excluded (worst was
# -76) and still excludes S (-714, 0.52) and s28's targets (-841, 0.25) decisively.
PAYOUT_WARN_MARGIN = 3.0   # warn when the best available target is close to the bar


def _hours_since(iso: str) -> str:
    """Age of an ISO timestamp, as text. Never raises -- an unparseable stamp
    reads UNKNOWN, which is louder than a wrong number."""
    from datetime import datetime, timezone
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        h = (datetime.now(timezone.utc) - d).total_seconds() / 3600.0
        return f"{h:.1f}h old" + ("  ⛔ STALE" if h > 2 else "")
    except Exception:
        return "AGE UNKNOWN  ⛔"


def payout_for(gap: float) -> float:
    """Rating points a 5-0 pays against an opponent `gap` points from us."""
    E = 1.0 / (1.0 + 10 ** (-(-gap) / 400))
    return K * (1.0 - E)


def admissible(gap: float, opp_rating: float) -> tuple[bool, str]:
    """Both gates. -> (ok, reason). The payout bar OVERRIDES the band, never the reverse."""
    pay = payout_for(gap)
    if pay < MIN_PAYOUT:
        return False, f"a 5-0 pays only {pay:.2f} (< {MIN_PAYOUT:.0f})"
    if not (BAND_LO <= gap <= BAND_HI):
        return False, "outside band"
    return True, ""


def floor_warning(ours: float) -> str:
    """Retained as the reporting hook. The drift it used to warn about is GONE by
    construction -- a payout bar does not move when our rating moves -- so this
    now says only that, and says it once, so a successor does not go looking for
    a floor that no longer exists."""
    return (f"NOTE: the absolute 1650 floor was RE-DENOMINATED to "
            f"MIN_PAYOUT = {MIN_PAYOUT:.0f} rating points on 2026-08-12. "
            f"It no longer drifts with our own rating ({ours:.0f}).")

_OVERRIDE: dict = {}
_RATING_AGE: dict = {}   # team -> ISO timestamp of its most recent observed rating


def pairing_gaps(min_our: float = 1600.0) -> list[float]:
    """Every observed ladder pairing gap (opponent - us), one per MATCH.

    WHY A DISTRIBUTION AND NOT JUST THE EDGES (s28 flag, research arm). The band
    `us-80..us+125` is the observed MIN/MAX over post-1600 matches -- and
    **sample extremes grow with n by construction.** The same measurement on
    5,000 matches would report a wider band, so a team just outside flips to
    YES from more data alone, with no change in the world. A bare YES/NO also
    renders two very different states identically: "we have literally never been
    paired this far" and "this is the edge of the observed range".

    The live victim was `Ouroboros`: reads NO at gap -102 today, **and we have
    played them 32 times.** Their gap at our last five meetings was
    -31.5, -13.7, +4.4, +10.0, -51.3 -- inside the band every time. It is only
    now, after we climbed to ~1669 while they sit at ~1558, that they fall
    outside. The honest rendering is "reachable until recently, not at current
    ratings", and a binary flag cannot say that.

    Same defect family as `0 / 18,400` vs `0 / 43`: **a verdict without its
    denominator.**
    """
    if "gaps" in _OVERRIDE:
        return _OVERRIDE["gaps"]
    out: list[float] = []
    path = ROOT / "corpus" / "ladder_games.tsv"
    if not path.exists():
        return out
    seen = set()
    for r in csv.DictReader(path.open(), delimiter="\t"):
        try:
            ours = float(r["ourbef"]); opp = float(r["oppbef"])
        except (ValueError, KeyError, TypeError):
            continue
        if ours < min_our:
            continue
        key = r.get("match")
        if key in seen:
            continue                      # one gap per MATCH, not per game
        seen.add(key)
        out.append(opp - ours)
    return sorted(out)


def history(name: str) -> tuple[int, float | None]:
    """(ladder matches played vs this opponent, gap at the most recent one).

    THE COLUMN THAT SEPARATES "NEVER REACHABLE" FROM "NOT REACHABLE ANY MORE",
    and without it those two render identically. `Ouroboros` at gap -102 and
    `vjg` at -841 both print BELOW-every-observed-pairing -- yet we have played
    Ouroboros 32 times (last five gaps -31.5, -13.7, +4.4, +10.0, -51.3, all
    inside the band) and vjg zero. The first is a matchup we climbed away from;
    the second was never on our schedule. **A gate that cannot tell those apart
    will retire a real opponent as unreachable.**
    """
    if "history" in _OVERRIDE:
        return _OVERRIDE["history"].get(name, (0, None))
    path = ROOT / "corpus" / "ladder_games.tsv"
    if not path.exists():
        return 0, None
    seen, latest, latest_gap = set(), "", None
    for r in csv.DictReader(path.open(), delimiter="\t"):
        if r.get("opp") != name:
            continue
        m = r.get("match")
        if m in seen:
            continue
        seen.add(m)
        when = r.get("created") or ""
        try:
            g = float(r["oppbef"]) - float(r["ourbef"])
        except (ValueError, KeyError, TypeError):
            continue
        if when >= latest:
            latest, latest_gap = when, g
    return len(seen), latest_gap


def percentile_of(gap: float, gaps: list[float]) -> str:
    """Where this gap sits in the observed pairing distribution, with its n."""
    if not gaps:
        return "no pairing history"
    below = sum(1 for g in gaps if g < gap)
    n = len(gaps)
    if below == 0:
        return f"BELOW every one of {n} observed pairings"
    if below == n:
        return f"ABOVE every one of {n} observed pairings"
    return f"p{100.0*below/n:.0f} of {n} observed pairings"


def _live_ratings() -> tuple[float, dict[str, float]]:
    """(our rating, {team: rating}) from the freshest source available.

    `league_matches.tsv` is kept current by the keeper (s28); each team's most
    recent `rating*Before` is its latest known rating.
    """
    if "ratings" in _OVERRIDE:
        return _OVERRIDE["ours"], _OVERRIDE["ratings"]
    ours, best = 0.0, {}
    seen: dict[str, str] = {}
    path = ROOT / "corpus" / "league_matches.tsv"
    if path.exists():
        for r in csv.DictReader(path.open(), delimiter="\t"):
            when = r.get("createdAt") or ""
            for side, other in (("A", "B"), ("B", "A")):
                name = r.get(f"team{side}Name")
                rt = r.get(f"rating{side}Before")
                if not name or not rt:
                    continue
                try:
                    rt = float(rt)
                except ValueError:
                    continue
                if when >= seen.get(name, ""):
                    seen[name] = when
                    best[name] = rt
    # ⛔ FRESHNESS, s33. `seen[name]` already holds the timestamp of each team's
    # most recent observation and it was being DISCARDED. CLAUDE.md: "A monitor
    # that reads a file must report that file's FRESHNESS." This gate is MANDATED
    # before every pre-registration, so every target line in every prereg inherited
    # a silently stale rating. Measured 2026-08-12: The Bisons 1762 cached vs 1682
    # live -- 80 points, an 18% payoff error, on a corpus surface 6 hours old. It
    # did not flip admissibility that time; that was luck, not the gate. Caught by
    # the side lane after a prereg author found it BY HAND, post-writing.
    _RATING_AGE.clear(); _RATING_AGE.update(seen)
    ours = best.get(OUR_TEAM, 0.0)
    # prefer the platform for OUR rating -- it is one cheap call and it is the
    # number every gap is measured from
    try:
        out = subprocess.run([FCODE, "status"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if "Rating:" in line:
                ours = float(line.split("Rating:")[1].split()[0])
    except Exception:
        pass
    return ours, best


def value(gap: float) -> tuple[float, float, float]:
    """(E, rating gained by a 5-0, rating lost by a 0-5) at this rating gap.

    gap = opponent - us. Uses the exact ladder rule delta = K*(S-E).
    """
    e = 1.0 / (1.0 + 10 ** (gap / 400.0))
    return e, K * (1.0 - e), K * (0.0 - e)


def selftest() -> int:
    """Drive the gate to both verdicts: a worthless target and a valuable one."""
    print("TARGET VALUE SELFTEST\n")
    bad = 0
    cases = [
        ("parity", 0, 0.500, 16.00, -16.00, True),
        ("900 below (the s28 carriers)", -900, 0.9931, 0.22, -31.78, False),
        ("+400 above (unreachable)", 400, 0.0909, 29.09, -2.91, False),
        ("+111 (0033, reachable)", 111, 0.3450, 20.96, -11.04, True),
    ]
    # PERCENTILE BRANCHES, driven on a fixture so all three render.
    fx = [-50.0, -20.0, 0.0, 30.0, 90.0]
    _OVERRIDE["gaps"] = fx
    for label, gap, want in [("below everything", -200.0, "BELOW every one"),
                             ("mid-distribution", 10.0, "p60 of 5"),
                             ("above everything", 400.0, "ABOVE every one")]:
        got = percentile_of(gap, fx)
        ok = want in got
        print(f"  [{'ok' if ok else 'FAIL'}] percentile {label:<20} -> {got}")
        if not ok:
            bad += 1
    # HISTORY BRANCHES: the column must separate "climbed away from" from
    # "never on our schedule", which is the whole reason it exists.
    _OVERRIDE["history"] = {"Climbed": (32, -51.3), "Stranger": (0, None)}
    for _n, _want in [("Climbed", (32, -51.3)), ("Stranger", (0, None))]:
        _got = history(_n)
        _ok = _got == _want
        print(f"  [{'ok' if _ok else 'FAIL'}] history {_n:<22} -> {_got}")
        if not _ok:
            bad += 1
    _OVERRIDE.clear()

    _OVERRIDE.clear()
    for label, gap, we, wwin, wloss, wreach in cases:
        e, win, loss = value(gap)
        reach = BAND_LO <= gap <= BAND_HI
        ok = (abs(e - we) < 0.005 and abs(win - wwin) < 0.05
              and abs(loss - wloss) < 0.05 and reach == wreach)
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<30} gap {gap:+5} "
              f"E={e:.3f} win {win:+6.2f} loss {loss:+6.2f} "
              f"reachable={'YES' if reach else 'NO '}")
        if not ok:
            bad += 1
            print(f"          expected E={we} win={wwin} loss={wloss} reach={wreach}")
    print()
    # ⛔ THE FLOOR MUST BE DRIVEN BOTH WAYS. A gate that has only ever returned
    # YES has not been seen to gate. Each case pins the FLOOR against the BAND so
    # a future edit cannot silently let the band win.
    # REWRITTEN s33 FOR THE PAYOUT BAR. The old cells pinned an ABSOLUTE floor and
    # two of them referenced RATING_FLOOR itself -- so they MOVED WITH the constant
    # and could never have caught the drift that actually happened. A cell defined
    # in terms of the thing under test cannot test it. These are pinned to MEASURED
    # live gaps instead, and the first two are teams the old floor wrongly excluded.
    floor_cases = [
        ("Askar City (old floor EXCLUDED it)",   -5, 1640, True),
        ("Lunds Stallions (old floor EXCLUDED)", -76, 1569, True),
        ("The Bisons, well above us",           +121, 1766, True),
        ("parity",                                 0, 1645, True),
        # THE BAND IS TIGHTER THAN THE BAR BELOW US, and this cell records it.
        # BAND_LO = -80 already pays 12.44, above MIN_PAYOUT = 10, so the payout
        # bar NEVER BINDS on the low side -- it is a backstop, not the active
        # gate. Found by this cell failing when it was written the other way.
        # A non-binding guard that CANNOT drift is still worth having; what it
        # replaces was a binding guard that drifted in the wrong direction.
        ("-136: refused by the BAND, not the bar", -136, 1509, False),
        ("-140: refused, outside both",            -140, 1505, False),
        ("team S (the ONE concentrated signal)", -714,  931, False),
        ("s28's vjg (the original mistake)",     -841,  804, False),
        ("pays well but OUTSIDE the band",      +400, 2050, False),
    ]
    print(f"  PAYOUT BAR (re-denominated s33): a 5-0 must pay >= "
          f"{MIN_PAYOUT:.0f} rating points -- bar OVERRIDES band:")
    for label, gap, rating, want in floor_cases:
        got, why = admissible(gap, rating)
        ok = got == want
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<28} gap {gap:+5} "
              f"rating {rating:<5} -> {'ADMISSIBLE' if got else 'NO'}"
              f"{(' (' + why + ')') if why else ''}")
        if not ok:
            bad += 1
    # THE CELL THAT WOULD HAVE CAUGHT THE ORIGINAL DEFECT, and it replaces the one
    # that could not. The old cell asserted a WARNING fired as we approached the
    # floor -- it accepted the drift and only announced it. This asserts the drift
    # CANNOT HAPPEN: the same gap must yield the same verdict at any rating of ours,
    # which is exactly what an absolute floor failed to do.
    same = {admissible(-76, ours - 76)[0] for ours in (1500, 1600, 1645, 1700, 1900)}
    ok_w = same == {True}
    print(f"  [{'ok' if ok_w else 'FAIL'}] a gap of -76 is admissible at EVERY rating "
          f"of ours (1500..1900) -- the bar cannot drift  {same}")
    if not ok_w:
        bad += 1
    # ...and the complement, so the cell is not simply always-True.
    same_no = {admissible(-714, ours - 714)[0] for ours in (1500, 1600, 1645, 1700, 1900)}
    ok_w2 = same_no == {False}
    print(f"  [{'ok' if ok_w2 else 'FAIL'}] a gap of -714 is refused at EVERY rating "
          f"of ours  {same_no}")
    if not ok_w2:
        bad += 1
    # ⛔⛔ THE CELL THAT WOULD HAVE CAUGHT THE s33 OUTAGE, and it is the reason this
    # block exists at all. The re-denomination removed RATING_FLOOR and left FIVE
    # references alive in main(). Every cell above exercises `admissible()`; NONE
    # called main(). So the suite was GREEN while the tool -- the gate CLAUDE.md
    # mandates before every pre-registration -- crashed on `--band`, on a named
    # team, and on no args. D24 in its purest form: no cell touched the shipped
    # surface. Found by the side lane, ten minutes after the commit.
    # ⇒ A PREDICATE BEING CORRECT SAYS NOTHING ABOUT WHETHER THE PROGRAM RUNS.
    # FRESHNESS CELL, driven BOTH WAYS. A staleness marker that has never been
    # absent is a constant, and one that has never fired is decoration.
    from datetime import datetime, timezone, timedelta
    _now = datetime.now(timezone.utc)
    fresh = _hours_since((_now - timedelta(minutes=30)).isoformat())
    stale = _hours_since((_now - timedelta(hours=7)).isoformat())
    bad_stamp = _hours_since("not-a-timestamp")
    for nm, got, want in (("a 30-min-old rating is NOT marked stale", fresh, False),
                          ("a 7-hour-old rating IS marked stale", stale, True)):
        ok_f = ("STALE" in got) == want
        print(f"  [{'ok' if ok_f else 'FAIL'}] {nm}  -> {got}")
        if not ok_f:
            bad += 1
    ok_u = "UNKNOWN" in bad_stamp
    print(f"  [{'ok' if ok_u else 'FAIL'}] an unparseable stamp reads UNKNOWN, not a number  -> {bad_stamp}")
    if not ok_u:
        bad += 1

    import io, contextlib
    print("  ENTRY POINTS — the suite must exercise the SHIPPED surface, not just the predicate:")
    for label, args in (("--band", ["--band"]), ("named team", ["The Bisons"]), ("no args", [])):
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                main(args)
            ok_e = True; detail = "ran"
        except SystemExit:
            ok_e = True; detail = "ran (SystemExit is the usage path)"
        except Exception as exc:                                  # noqa: BLE001
            ok_e = False; detail = f"{type(exc).__name__}: {exc}"
        print(f"  [{'ok' if ok_e else 'FAIL'}] main({label}) {detail}")
        if not ok_e:
            bad += 1

    print()
    if bad:
        print(f"*** {bad} case(s) wrong ***")
        return 1
    print("PASS: values a worthless target near zero and a reachable one near "
          "parity, and the band flag separates them.")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    ours, ratings = _live_ratings()
    if not ours:
        print("REFUSING: could not establish our own rating -- the gap every "
              "number here depends on. Check `fcode status`.")
        return 1

    if "--band" in argv:
        rows = [(n, r, r - ours) for n, r in ratings.items() if n != OUR_TEAM]
        band_only = [x for x in rows if BAND_LO <= x[2] <= BAND_HI]
        rows = [x for x in band_only if payout_for(x[2]) >= MIN_PAYOUT]
        excluded = [x for x in band_only if payout_for(x[2]) < MIN_PAYOUT]
        rows.sort(key=lambda x: -x[2])
        _newest = max(_RATING_AGE.values(), default="")
        _age = _hours_since(_newest)
        print(f"RATINGS from corpus/league_matches.tsv — newest observation "
              f"{_newest[:16] or '?'} ({_age})")
        print(f"  ⚠ opponent ratings are CACHED. Ours is live off `fcode status`. "
              f"80-point drift over ~6h has been observed; verify the SELECTED "
              f"target before quoting its payoff.\n")
        print(f"ADMISSIBLE at our {ours:.0f}: us{BAND_LO:+d}..us{BAND_HI:+d} "
              f"AND a 5-0 pays >= {MIN_PAYOUT:.0f}  ({len(rows)} teams)\n")
        print(f"  {'team':<26}{'rating':>8}{'gap':>7}{'5-0 pays':>10}{'0-5 costs':>11}")
        for n, r, g in rows:
            _e, w, l = value(g)
            print(f"  {n[:26]:<26}{r:>8.0f}{g:>+7.0f}{w:>+10.2f}{l:>+11.2f}")
        if excluded:
            excluded.sort(key=lambda x: -x[1])
            # A FILTER MUST NAME ITS CASUALTIES (D83/S6). This section is why the
            # seven teams the old absolute floor wrongly excluded were VISIBLE
            # enough to get the rule re-denominated. Kept for that reason.
            print(f"\n  EXCLUDED — a 5-0 pays less than {MIN_PAYOUT:.0f} "
                  f"(inside the reachable band, but not worth a leg):")
            for n, r, g in excluded:
                print(f"    {n[:26]:<26}{r:>8.0f}{g:>+7.0f}")
        w_ = floor_warning(ours)
        if w_:
            print("\n" + w_)
        return 0

    names = [a for a in argv if not a.startswith("--")]
    if not names:
        print(__doc__)
        return 2

    gaps_hist = pairing_gaps()
    print(f"our rating {ours:.0f}   (reachable band us{BAND_LO:+d}..us{BAND_HI:+d}, "
          f"from {len(gaps_hist)} observed pairings)")
    print("  BAND EDGES ARE SAMPLE EXTREMES AND GROW WITH n -- read the "
          "percentile, not the YES/NO, at the margin.\n")
    print(f"  {'opponent':<26}{'rating':>8}{'gap':>7}{'5-0 pays':>10}"
          f"{'0-5 costs':>11}  reachable   where that gap sits")
    gaps, pays, rated = [], [], []
    unknown = []
    for n in names:
        r = ratings.get(n)
        if r is None:
            unknown.append(n)
            continue
        g = r - ours
        _e, w, l = value(g)
        gaps.append(g)
        rated.append(r)
        pays.append(w)
        print(f"  {n[:26]:<26}{r:>8.0f}{g:>+7.0f}{w:>+10.2f}{l:>+11.2f}"
              f"  {'YES' if admissible(g, r)[0] else '** NO **'}"
              f"   {percentile_of(g, gaps_hist)}")
        _ok, _why = admissible(g, r)
        if not _ok and _why:
            print(f"  {'':<26}{'':>8}{'':>7}{'':>10}{'':>11}     ^ {_why}")
        played, last_gap = history(n)
        if played and not (BAND_LO <= g <= BAND_HI):
            print(f"  {'':<26}{'':>8}{'':>7}{'':>10}{'':>11}"
                  f"     ^ but PLAYED {played}x on the ladder, most recently at "
                  f"gap {last_gap:+.0f} -- reachable UNTIL RECENTLY, not now")
        elif not played:
            print(f"  {'':<26}{'':>8}{'':>7}{'':>10}{'':>11}"
                  f"     ^ never played on the ladder")
    for n in unknown:
        print(f"  {n[:26]:<26}{'?':>8}{'?':>7}{'?':>10}{'?':>11}  ** UNKNOWN **")
    if not gaps:
        print("\nno known opponents -- cannot value this target")
        return 1

    reach = sum(1 for g, r in zip(gaps, rated) if admissible(g, r)[0])
    print(f"\nTARGET BAND: gaps {min(gaps):+.0f}..{max(gaps):+.0f}, "
          f"a 5-0 pays {min(pays):.2f}..{max(pays):.2f}, "
          f"admissible {reach}/{len(gaps)}  (band AND a 5-0 paying >= {MIN_PAYOUT:.0f})")
    _w = floor_warning(ours)
    if _w:
        print(_w)
    if reach == 0:
        print("** NO TARGET IS REACHABLE ON THE LADDER. Even a total success "
              "here cannot be converted into rating by playing them. **")
    if max(pays) < 5.0:
        print(f"** A PERFECT RESULT PAYS UNDER 5 RATING POINTS ({max(pays):.2f}). "
              f"Say in the prereg why the leg is worth running anyway. **")
    print("\nCopy this line into the pre-registration as `TARGET BAND:`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
