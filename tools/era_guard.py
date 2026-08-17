#!/usr/bin/env python3
"""ERA GUARD — refuses to return an our-side statistic unless the caller names an era.

    from era_guard import our_rows
    rows, era = our_rows("corpus/ladder_games.tsv", era="live")   # current line only
    rows, era = our_rows("corpus/ladder_games.tsv", era="all")    # explicit opt-in, ALLOWED
    rows, era = our_rows("corpus/ladder_games.tsv")               # -> raises EraNotSpecified

    .venv/bin/python tools/era_guard.py --selftest

IMPLEMENTS: docs/research/SPEC-era-guard-2026-08-11.md

===== WHY THIS EXISTS =====
The spec's own case was two errors by its author in one hour: an "our core melee
rate" claim read `batk_core ≈ 104/game` pooled and **0.00** on the live version;
a "tiebreak wins convertible" claim read 603 games / "+1,760 points" pooled and
**1.2%, five games in 425** live. Both were caught by an external check, never by
the query itself — which is the whole argument for mechanising this rather than
trusting attention.

**By 2026-08-14 the defect had fired FIVE times across TWO lanes** (see
`docs/coordination.md`, entry timestamped 2026-08-14T13:2xZ, "RESEARCH s40:
`era_guard` WAS SPEC'D THREE DAYS AGO AND NEVER BUILT"):

  | when       | lane     | claim                          | pooled          | era-bounded        |
  |------------|----------|---------------------------------|-----------------|---------------------|
  | 08-11      | side     | our core melee rate             | batk_core ≈ 104 | 0.00                |
  | 08-11      | side     | tiebreak wins convertible        | 603g, "+1,760"  | 1.2%, 5 in 425      |
  | 08-14 13:0x| research | Leviathan h2h                    | week-pooled 47.7%| 24.0% (same era)   |
  | 08-14 13:0x| research | "our three biggest leaks"        | Ouroboros/Lunds/KCM | all three VANISH |
  | 08-14 13:1x| research | LingLing40 "2nd-biggest live leak"| −26.4 Elo       | −0.4, 52.0% (retracted) |

This file is the mechanisation. It does not stop anyone from computing a pooled
figure — `era="all"` stays fully available, because a claim about the LINE'S
HISTORY is a real claim — it only stops pooling from being the accidental default.

===== WHAT `era="live"` MEANS, AND THE TRAP THAT LIVES HERE =====
`PROGRAMME.md`'s `INCUMBENT:` field is NOT a usable platform version number —
it is a bot-TREE PATH, e.g. `bots/_v223sealrepair`. The corpus surfaces below key
on the PLATFORM SUBMISSION VERSION (`ourver` in `ladder_games.tsv`,
`teamAVersion`/`teamBVersion` in `meta_join.tsv`) — a completely different
counter. Confirmed live, 2026-08-14: `INCUMBENT` read `bots/_v223sealrepair`
while `HANDOVER.md`'s own live banner says that tree IS **v140**. The tree
name's embedded digits (**223**) are not the platform version (**140**) — a
regex that stripped digits out of the tree path would have silently picked the
wrong era, which is exactly the defect this file exists to prevent, shipped
under this file's own name. `PROGRAMME.md` carries no parseable numeric-version
field as of this writing, so per this tool's own build brief we do NOT invent one
and do NOT parse `HANDOVER.md`'s prose banner (not a stable, parsed surface,
and it is on the "never edit" list for this build anyway) — we fall back to a
single named constant, below, that must be hand-updated on every ship and is
cross-checked against `HANDOVER.md`'s "`# LIVE: **vNNN = ...`" line and against
the newest `ourver` in `ladder_games.tsv`.

===== SURFACES, AND WHY THEY ARE NOT UNIFORM =====
`ladder_games.tsv` carries `ourver` directly — no join needed.

`meta_join.tsv` carries `teamAName`/`teamAVersion`/`teamBName`/`teamBVersion` for
BOTH sides of every league match (most of which are not ours at all) plus a
`us_side` column (`a`/`b`/`none`) that is verified, byte-for-byte, to agree with
`teamAName == "OpenSverige"` / `teamBName == "OpenSverige"` (0 mismatches across
8,338 of our rows, checked live). `us_side == "none"` rows are not our data at
any era and are always dropped, not just at the requested era.

`build_agg.tsv`, `flow.tsv`, `throws.tsv`, `econ.tsv` are decoded straight off
the replay wire and carry only a raw ENGINE team ordinal (`team` = 0 or 1) —
**not** the platform's teamA/teamB seat, and NOT the same number space as
`meta_join`'s letters. `tools/corpus/build_corpus.py`'s own docstring names this
exactly: *"A replay knows only 'team 0' and 'team 1'. join.tsv maps [file ->
our team index], RECONCILED against the replay... a wrong seat would invert
every per-team claim built on it."* `corpus/join.tsv` is that reconciled table
(file -> our_team, ourver) and this file uses it as the join key — verified live
against `throws.tsv`'s own independent `winner`/`game_winner_side` pair (1,060
+ 947 matches, 0 cross-contamination) that engine team 0 == platform seat A
and engine team 1 == seat B, consistently, before trusting it here.
`corpus/join.tsv` only covers files that are OUR games (~3,520 of the tens of
thousands of league-wide decoded replays), so joining against it is itself the
our-vs-not-ours filter — a file absent from `join.tsv` is simply not ours and is
dropped, at every era.

`econ.tsv` is additionally KNOWN CORRUPT for recently-decoded files (dead
`turns_run`/`cpu_sum` columns, wrong `ti_collected_end`, and a `tled` column
that measures a wire flag which does not exist — `CLAUDE.md`, corroborated by
`tools/corpus_sanity.py`). This file does not attempt to fix that decoder; it
surfaces the surface (era-filterable) and prints a one-line warning every time
it is opened, per the standing rule that a caller must not be able to trust a
number it was never told was suspect.

===== WHAT THIS DOES NOT DO — KEPT FROM THE SPEC, NOT PAPERED OVER =====
* It cannot catch an era error in a figure computed OUTSIDE this helper — a
  hand-rolled `csv.DictReader` loop bypasses it entirely, which is how every one
  of the spec's own two founding failures was written. It lowers the cost of
  doing this right; it does not make doing it wrong impossible.
* It says nothing about the OPPONENT's era — separate, unsolved problem (D18/
  D18b in this repo's own history). **Of the five firings on record above, this
  guard as specified would have caught FOUR. The fifth — the Leviathan head-to-
  head, pooled across ~40 of THEIR versions while ours held steady — is exactly
  the opponent-era half this file does not cover.** Do not read this tool as
  covering that case; it does not, and was never asked to.
* It is not a substitute for the rider that explains WHY pooling misleads here;
  it only makes the right thing (naming an era) the cheap thing.

===== HOUSE RULES THIS FOLLOWS =====
Freshness of every file read is reported via `tools/freshness.py`
(`assert_fresh`/`newest_row_age_h`) — never silently assumed. Several of the
surfaces here (`join.tsv`, `build_agg.tsv`, `flow.tsv`, `throws.tsv`, `econ.tsv`)
carry NO timestamp column at all (only an opaque replay filename), so freshness
on those is reported as UNKNOWN rather than guessed — "we cannot tell" and "we
checked and it's fine" are different states and must not be conflated. Exit code
is not read anywhere in this file as a health signal, per the standing repo rule;
`--selftest` prints PASS/FAIL and returns a real, deliberate exit code only for
that purpose.

CALIBRATION EVIDENCE — THE CATCH RATE, not just the firing count (added s40
2026-08-14, side-lane observation). Of the three era-pooling errors made on
2026-08-14 alone, TWO WERE CONSUMED BY A PEER BEFORE THE AUTHOR CAUGHT THEM
(the week-pooled Leviathan h2h and the "-636 Elo three biggest leaks" table
both reached another lane; LingLing40-as-a-leak was caught pre-publication only
because the first two had just fired). That is the number that argues for a
guard rather than for attention: the errors are not caught by the person making
them, and they travel. This helper cannot catch a hand-rolled csv.DictReader --
which is how all three were written -- so it lowers the cost of doing it right
and does not make doing it wrong impossible.
"""
from __future__ import annotations

import csv
import gzip
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from freshness import assert_fresh  # noqa: E402

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)


class EraNotSpecified(Exception):
    """Raised when our_rows() is called with no era= — the whole point of this file."""


class EraSurfaceUnsupported(Exception):
    """Raised when a surface cannot be era-filtered at all. Never returns
    unfiltered rows in this case — see the module docstring's SURFACES section."""


# ===== LIVE_VERSION_HINT — DERIVED, NOT EMBEDDED (rewritten s48 wrap, CLASS A) ==
#
# ⛔ WHAT THIS USED TO BE, AND WHY IT WAS REPLACED. Until 2026-08-17 this was a
# hand-typed literal (`LIVE_VERSION_HINT = 140  # bots/_v223sealrepair`) with a
# paragraph arguing it could not be derived: PROGRAMME.md's INCUMBENT is a bot-
# TREE PATH (`bots/_v468kladturbo`), whose own digits are a DIFFERENT counter
# from the platform submission version, and HANDOVER.md's banner is prose, not a
# parsed surface. Both halves of that argument are still TRUE — and the
# conclusion drawn from them was still wrong, because there is a third surface
# neither considered: **`elo_history.tsv`'s `active_bot` column, which tags every
# poll row with the version ACTIVE AT POLL TIME.** That is precisely this hint's
# semantics ("who holds the slot RIGHT NOW", ahead of any completed match), it is
# machine-written every ~5 minutes, and nobody has to remember to bump it.
# Measured at the wrap: the literal read v140 while the platform was on v155 —
# FIFTEEN versions and three days stale. A hand-maintained value nobody updates
# is the exact failure class this file exists to close.
#
# ⛔ AND THE SAME COLUMN IS THE WRONG READ ELSEWHERE — that is not a contradiction,
# it is the reason to write the distinction down. `tools/ship_ledger.py:24` and
# `tools/slot_rule.py` both forbid the poll-time tag for LEAK ACCOUNTING, because
# it records who was active WHEN SAMPLED, not who played the match; that question
# needs per-match `ourver`. Here we are asking who is active NOW, which is the one
# question the poll-time tag answers correctly and the per-match column does not.
#
# THE RESOLUTION, and it now has FOUR live branches instead of three. The hint is
# cross-checked against the max `ourver` actually seen in corpus/ladder_games.tsv
# (the one place this happens, so it cannot drift between callers):
#   * EQUAL              -> silent, normal.
#   * HINT AHEAD of tape -> `fresh_ship`: the minutes after a ship, before the
#                           ladder has paired the new version. HINT wins, noted.
#   * HINT BEHIND tape, and the poll tape's newest row is OLDER than the ladder
#     tape's newest row -> `stale_hint`: the poller is lagging. TAPE wins, loudly.
#   * HINT BEHIND tape, and the poll tape's newest row is NEWER -> `rollback`:
#     ⭐ THE BRANCH THE OLD CODE DID NOT HAVE, and it was live-wrong at the moment
#     this was rewritten. 2026-08-17T07:12Z the poll tape read v155 (Odin v157
#     rolled back after 68 minutes) while ladder_games.tsv still carried v157 rows
#     from 06:12Z, so `era="live"` confidently returned the rows of a version that
#     was NO LONGER LIVE. The general rule that fixes both directions is **the
#     MORE RECENT OBSERVATION WINS**, so this branch resolves to the HINT.
# Neither branch ever falls through to a pooled read — every one resolves to one
# concrete version number, or REFUSES.
#
# ⛔ REFUSE, DON'T DEFAULT: if BOTH surfaces are unreadable there is no honest
# answer to "which version is live", and the old code's "use the hint UNVERIFIED"
# is not available any more — there is no embedded constant left to fall back on.
# It raises `EraLiveUnresolvable`. An era guard that invents an era is worse than
# one that stops.
_LIVE_HINT_TAPE = ROOT / "elo_history.tsv"

# The one place era="live" cross-checks the hint against reality.
_LADDER_FOR_LIVE_CHECK = ROOT / "corpus" / "ladder_games.tsv"


def _derive_live_hint():
    """(version, iso_ts) off elo_history.tsv's newest poll row, or (None, None).

    Reads the LAST row carrying a parseable `active_bot` — not the max, because
    a ROLLBACK legitimately moves the tag DOWN and a max would be blind to
    exactly that."""
    ver = ts = None
    try:
        with _open_tsv(_LIVE_HINT_TAPE) as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                raw = (r.get("active_bot") or "").strip().lstrip("vV")
                if not raw.isdigit():
                    continue
                ver, ts = int(raw), (r.get("timestamp") or "").strip() or None
    except (FileNotFoundError, OSError):
        return None, None
    return ver, ts


# ⛔ The module-level BINDING of these two lives further down, immediately after
# `_open_tsv` is defined — `_derive_live_hint()` calls it, so binding here would
# raise NameError at import. Declared here only so the reader meets them beside
# the docstring that explains them.


def _ts_cmp(s):
    """ISO-ish stamp -> datetime, or None. ⛔ NOT a string compare: the two tapes
    write DIFFERENT shapes (`2026-08-17T07:12Z` vs `2026-08-17T06:12:59.805Z`)
    and lexicographic order gets the same-minute case backwards ('Z' > ':').
    This comparison decides ROLLBACK vs LAG, so it parses."""
    if not s:
        return None
    s = s.strip().replace("Z", "+00:00")
    for cand in (s, s + ":00+00:00", s + "+00:00"):
        try:
            return datetime.fromisoformat(cand)
        except ValueError:
            continue
    return None


def _resolve_live(hint, hint_ts, tape_max, tape_ts):
    """PURE. (version, tag, message). Every branch of the table above.

    Pure on purpose: the selftest drives all six states through THIS function
    with literal arguments, so no branch depends on what the two tapes happen to
    say on the day the selftest runs. tag in
    {None, "fresh_ship", "stale_hint", "rollback", "hint_blind", "tape_blind"}.
    """
    if hint is None and tape_max is None:
        return None, "blind", (
            "era='live' UNRESOLVABLE: neither elo_history.tsv (poll-time holder) "
            "nor corpus/ladder_games.tsv (per-match ourver) could be read. There "
            "is no embedded fallback version by design — refusing rather than "
            "inventing an era.")
    if hint is None:
        return tape_max, "hint_blind", (
            f"⛔ era='live' HINT BLIND: elo_history.tsv unreadable or carries no "
            f"parseable `active_bot`, so the live holder is unknown. Falling back "
            f"to the ladder tape's newest ourver v{tape_max}, which is the last "
            f"version that PLAYED, not necessarily the one that HOLDS.")
    if tape_max is None:
        return hint, "tape_blind", (
            f"era='live' cross-check UNAVAILABLE (corpus/ladder_games.tsv missing "
            f"or unreadable) — using the poll tape's holder v{hint} UNVERIFIED.")
    if hint == tape_max:
        return hint, None, ""
    if hint > tape_max:
        return hint, "fresh_ship", (
            f"era='live': the poll tape's holder is v{hint} but ladder_games.tsv "
            f"has not seen it yet (newest ourver v{tape_max}) — normal in the "
            f"minutes right after a ship, before the ladder has paired the new "
            f"version. USING the holder v{hint}.")
    # hint < tape_max: lag or rollback, and only the clocks can tell them apart.
    _h, _t = _ts_cmp(hint_ts), _ts_cmp(tape_ts)
    if _h is not None and _t is not None and _h > _t:
        return hint, "rollback", (
            f"⛔ era='live' ROLLBACK: the poll tape says v{hint} at {hint_ts}, "
            f"NEWER than ladder_games.tsv's newest row {tape_ts} which still "
            f"carries v{tape_max}. The higher version played and was then pulled. "
            f"USING v{hint} (the more recent observation); v{tape_max}'s rows are "
            f"a PAST era, not the live one.")
    return tape_max, "stale_hint", (
        f"⛔ era='live' STALE HINT: the poll tape says v{hint} (at "
        f"{hint_ts or 'unknown time'}) but ladder_games.tsv's newest ourver is "
        f"v{tape_max} (at {tape_ts or 'unknown time'}) and the LADDER tape is the "
        f"more recent observation — the poller is lagging a ship. USING "
        f"v{tape_max} (the tape), NOT the lagging hint.")


class EraLiveUnresolvable(Exception):
    """Both live-version surfaces are unreadable. era="live" refuses rather than
    guessing — there is deliberately no embedded fallback constant."""


def _resolve_live_version():
    """(resolved_version, tag) — reads both surfaces, then defers to _resolve_live.

    Always prints when the two surfaces disagree; never silent about a
    disagreement, never loud about agreement."""
    hint, hint_ts = LIVE_VERSION_HINT, LIVE_VERSION_HINT_TS
    data_max = None
    data_ts = None
    try:
        with _open_tsv(_LADDER_FOR_LIVE_CHECK) as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                v = r.get("ourver")
                if not v:
                    continue
                try:
                    iv = int(v)
                except ValueError:
                    continue
                if data_max is None or iv > data_max:
                    data_max = iv
                c = (r.get("created") or "").strip()
                if c and (data_ts is None or c > data_ts):
                    data_ts = c
    except (FileNotFoundError, OSError):
        pass
    if _LADDER_FOR_LIVE_CHECK.exists():
        assert_fresh(_LADDER_FOR_LIVE_CHECK, max_age_h=24)

    ver, tag, msg = _resolve_live(hint, hint_ts, data_max, data_ts)
    if msg:
        print(f"[era_guard] {msg}", file=sys.stderr)
    if ver is None:
        raise EraLiveUnresolvable(msg)
    return ver, (None if tag is None else tag)


_INT_RE = re.compile(r"\A\d+\Z")
_PLUS_RE = re.compile(r"\A(\d+)\+\Z")


def _era_predicate(era):
    """era spec -> (predicate: int -> bool, era_used: str). Raises on a bad spec."""
    if era is None:
        raise EraNotSpecified(
            "our_rows() called with no era=. Pass era=\"live\" (current incumbent "
            "only), era=\"all\" (explicit opt-in to the whole line's history), an "
            "int (a specific version), a list/tuple of ints, or \"N+\" (a version "
            "and everything after it). A pooled figure is a real thing you can ask "
            "for — it is just no longer the default.")
    if era == "all":
        return (lambda v: True), "all"
    if era == "live":
        live, _tag = _resolve_live_version()
        return (lambda v: v == live), f"live (v{live})"
    if isinstance(era, bool):  # bool is an int subclass; reject before the int branch
        raise ValueError(f"unrecognised era spec: {era!r}")
    if isinstance(era, int):
        return (lambda v: v == era), f"v{era}"
    if isinstance(era, (list, tuple, set)):
        try:
            vs = sorted({int(x) for x in era})
        except (TypeError, ValueError):
            raise ValueError(f"unrecognised era spec: {era!r} — list must be all ints")
        vset = set(vs)
        return (lambda v: v in vset), "v{" + ",".join(str(x) for x in vs) + "}"
    if isinstance(era, str):
        m = _PLUS_RE.match(era.strip())
        if m:
            th = int(m.group(1))
            return (lambda v: v >= th), f"v{th}+"
        if _INT_RE.match(era.strip()):
            v0 = int(era.strip())
            return (lambda v: v == v0), f"v{v0}"
    raise ValueError(
        f"unrecognised era spec: {era!r} — use \"live\", \"all\", an int, a "
        f"list/tuple of ints, or the string \"N+\"")


def _plain_and_gz(path: Path):
    """(plain_path, gz_path) whichever exist; both may point at the same data."""
    if path.suffix == ".gz":
        return path.with_suffix(""), path
    return path, path.with_suffix(path.suffix + ".gz")


def _open_tsv(path: Path):
    plain, gz = _plain_and_gz(path)
    if plain.exists():
        return open(plain, "rt", newline="")
    if gz.exists():
        return gzip.open(gz, "rt", newline="")
    raise FileNotFoundError(f"era_guard: neither {plain} nor {gz} exists")


# ===== The DERIVED live-version hint (see the long block above). Bound HERE and
# not at its docstring because `_derive_live_hint()` calls `_open_tsv`. =====
LIVE_VERSION_HINT, LIVE_VERSION_HINT_TS = _derive_live_hint()


def _report_freshness(path: Path, max_age_h: float) -> None:
    """Print the freshness of `path`'s DATA, per tools/freshness.py. Never gates
    execution here — era_guard's job is the era, not the staleness verdict — but
    a monitor reading this output can act on it, and it is always printed."""
    plain, gz = _plain_and_gz(path)
    if plain.exists():
        _ok, _age, msg = assert_fresh(plain, max_age_h)
        print(f"[era_guard] {msg}", file=sys.stderr)
        return
    print(f"[era_guard] freshness UNKNOWN: only the gzip form of {gz.name} exists "
          f"and assert_fresh() reads raw bytes, which would garble a compressed "
          f"tail rather than report it honestly — refusing to guess.",
          file=sys.stderr)


def _report_freshness_unknown(surface: str) -> None:
    print(f"[era_guard] freshness UNKNOWN for {surface}: this surface carries no "
          f"timestamp column (only an opaque replay filename) — cannot establish "
          f"data age. This is a different state from 'checked and fresh'.",
          file=sys.stderr)


# ---------------------------------------------------------------------------
# Per-surface row extraction. Each returns a list[dict] already filtered to
# (a) rows that are OURS and (b) rows matching the requested era predicate.
# ---------------------------------------------------------------------------

def _rows_ladder_games(path: Path, pred) -> list[dict]:
    _report_freshness(path, max_age_h=24)
    out = []
    with _open_tsv(path) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            v = r.get("ourver")
            if not v:
                continue
            try:
                iv = int(v)
            except ValueError:
                continue
            if pred(iv):
                out.append(r)
    return out


def _rows_meta_join(path: Path, pred) -> list[dict]:
    _report_freshness(path, max_age_h=48)
    out = []
    with _open_tsv(path) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            side = r.get("us_side")
            if side == "a":
                v = r.get("teamAVersion")
            elif side == "b":
                v = r.get("teamBVersion")
            else:
                continue  # not our match at all, at ANY era
            if not v:
                continue
            try:
                iv = int(v)
            except ValueError:
                continue
            if pred(iv):
                out.append(r)
    return out


def _load_join_table(corpus_dir: Path) -> dict:
    join_path = corpus_dir / "join.tsv"
    if not join_path.exists():
        raise EraSurfaceUnsupported(
            f"era_guard: {join_path} is missing. build_agg.tsv/flow.tsv/throws.tsv/"
            f"econ.tsv carry only a raw engine team ordinal (0/1), not the platform "
            f"teamA/teamB seat or a version — resolving 'ours, at what version' for "
            f"these surfaces REQUIRES the reconciled join.tsv (see module docstring). "
            f"Refusing to guess the seat rather than risk inverting every per-team "
            f"claim built on a wrong one.")
    mapping = {}
    with open(join_path, "rt", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            try:
                mapping[r["file"]] = (int(r["our_team"]), int(r["ourver"]))
            except (KeyError, ValueError):
                continue
    return mapping


def _rows_via_join(path: Path, pred, surface_name: str) -> list[dict]:
    mapping = _load_join_table(path.parent)
    _report_freshness_unknown(surface_name)
    if surface_name == "econ.tsv":
        print("[era_guard] WARNING: econ.tsv is KNOWN CORRUPT for recently-decoded "
              "files (dead turns_run/cpu_sum_us columns, wrong ti_collected_end, and "
              "a tled column measuring a wire flag that does not exist). Rows below "
              "are correctly ERA-filtered; the corrupt columns are NOT fixed by this "
              "tool. Do not trust turns_run/cpu_sum_us/ti_collected_end/tled off it.",
              file=sys.stderr)
    out = []
    with _open_tsv(path) as fh:
        rdr = csv.DictReader(fh, delimiter="\t")
        team_col = _team_column(surface_name, rdr.fieldnames or [])
        for r in rdr:
            info = mapping.get(r.get("file"))
            if info is None:
                continue  # not one of our reconciled games, at any era
            our_team, ourver = info
            try:
                if int(r[team_col]) != our_team:
                    continue
            except (KeyError, ValueError):
                continue
            if pred(ourver):
                out.append(r)
    return out


# Per-surface team column. NOT every join surface calls it `team`.
_TEAM_COL_BY_SURFACE = {
    # throws.tsv describes an EVENT WITH TWO PARTIES: `tteam` is the THROWER's
    # team (the launcher's owner) and `bteam` the thrown BOT's. "Ours" for a
    # throw means WE THREW IT, so `tteam` is the correct filter. A caller who
    # wants throws made AGAINST us wants `bteam` and must say so.
    "throws.tsv": "tteam",
}


def _team_column(surface_name: str, fieldnames: list) -> str:
    """⛔ AN UNRESOLVABLE TEAM COLUMN IS A LOUD FAILURE, NEVER A SILENT ZERO.

    This function exists because of a real defect, and the defect was not the
    missing column -- it was the HANDLING. The old code did `int(r["team"])`
    inside `except (KeyError, ValueError): continue`. `throws.tsv` has no
    `team` column (it carries `tteam`/`bteam`), so EVERY row raised KeyError,
    EVERY row was skipped, and `our_rows()` returned **an empty list with no
    error**. An era-guarded read of `throws.tsv` therefore rendered exactly
    like "we made no throws in this era" -- and this repo has just spent a
    session establishing that v140 made **zero rated throws**, which is a real
    and load-bearing finding of the same shape. **A blind instrument that
    renders as a substantive zero is this project's most-repeated defect**, and
    here it sat inside the tool built to keep era claims honest.

    So: resolve the column per surface; if it cannot be resolved, RAISE.
    """
    col = _TEAM_COL_BY_SURFACE.get(surface_name, "team")
    if col not in fieldnames:
        raise EraSurfaceUnsupported(
            f"era_guard: {surface_name} has no usable team column -- wanted "
            f"{col!r}, header is {list(fieldnames)}. REFUSING to return rows: "
            f"the previous behaviour silently dropped every row and returned an "
            f"empty list, which is indistinguishable from a genuine zero. If "
            f"this surface gained or renamed a column, add it to "
            f"_TEAM_COL_BY_SURFACE rather than widening the except clause.")
    return col


_JOIN_SURFACES = {"build_agg.tsv", "flow.tsv", "throws.tsv", "econ.tsv"}


def our_rows(path, era=None):
    """The one entry point. Returns (rows, era_used).

    Raises EraNotSpecified if era is omitted, EraSurfaceUnsupported if the
    surface cannot be era-filtered by this tool, ValueError for a malformed
    era spec. Never returns pooled rows unless era="all" was named explicitly."""
    pred, era_used = _era_predicate(era)   # raises first — see it before opening a file
    p = Path(path)
    name = p.name[:-3] if p.name.endswith(".gz") else p.name

    if name == "ladder_games.tsv":
        rows = _rows_ladder_games(p, pred)
    elif name == "meta_join.tsv":
        rows = _rows_meta_join(p, pred)
    elif name in _JOIN_SURFACES:
        rows = _rows_via_join(p, pred, name)
    else:
        raise EraSurfaceUnsupported(
            f"era_guard: unrecognised surface {p.name!r}. Supported: "
            f"ladder_games.tsv, meta_join.tsv, build_agg.tsv, flow.tsv, "
            f"throws.tsv, econ.tsv.")

    if not rows:
        print(f"[era_guard] 0 rows for era={era_used!r} on {p.name} — returning "
              f"EMPTY, NOT falling back to pooled data. If this is unexpected, the "
              f"era you named may not exist in this data.", file=sys.stderr)
    return rows, era_used


# ---------------------------------------------------------------------------
# --selftest — drives every guard in BOTH directions, per this repo's own rule:
# "a check that has never produced the other verdict has not been seen to check."
# ---------------------------------------------------------------------------

def selftest() -> int:
    import contextlib
    import io

    bad = 0

    def check(label, got, want):
        nonlocal bad
        ok = got == want
        if not ok:
            bad += 1
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<70} got={got!r} want={want!r}")

    LADDER = ROOT / "corpus" / "ladder_games.tsv"
    META = ROOT / "corpus" / "meta_join.tsv"
    BUILD_AGG = ROOT / "corpus" / "build_agg.tsv"
    ECON = ROOT / "corpus" / "econ.tsv"

    with contextlib.redirect_stderr(io.StringIO()):

        # ===== FIXTURE 1: NEGATIVE — no era MUST raise, a named era MUST NOT =====
        print("\n--- fixture 1: NEGATIVE (EraNotSpecified) ---")
        raised = False
        try:
            our_rows(LADDER)
        except EraNotSpecified:
            raised = True
        check("our_rows(no era=) raises EraNotSpecified", raised, True)

        raised2 = False
        try:
            our_rows(LADDER, era="all")
        except EraNotSpecified:
            raised2 = True
        check("...but the SAME call WITH era='all' does not raise", raised2, False)

        # ===== FIXTURE 2: POSITIVE — both era='all' and a named era return data,
        # AND the numbers differ. Current pair (v102/v104 in the original spec are
        # now historical; reproduced today against ladder_games.tsv game share). =====
        print("\n--- fixture 2: POSITIVE, both directions reachable ---")
        rows_all, used_all = our_rows(LADDER, era="all")
        rows_125, used_125 = our_rows(LADDER, era=125)
        check("era='all' era_used label", used_all, "all")
        check("era=125 era_used label", used_125, "v125")
        # ⛔ THESE WERE HARDCODED SNAPSHOTS (4825 / 305) AND FAILED THE DAY THE
        # CORPUS GREW BY 20 GAMES -- a selftest that fails on healthy growth is a
        # selftest that gets ignored. Assert INVARIANTS derived from the file, not
        # a frozen count: invariants catch LOGIC errors, snapshots catch APPENDS.
        import csv as _csv
        with open(LADDER) as _f:
            _raw = [r for r in _csv.DictReader(_f, delimiter="\t")]
        _n_all = len(_raw)
        _n_125 = sum(1 for r in _raw if r.get("ourver") == "125")
        check("era='all' returns EVERY row of the surface", len(rows_all), _n_all)
        check("era=125 returns exactly the ourver==125 rows", len(rows_125), _n_125)
        check("era=125 is a STRICT subset of era='all'", 0 < len(rows_125) < len(rows_all), True)
        share_all = sum(int(r["won"]) for r in rows_all) / len(rows_all)
        share_125 = sum(int(r["won"]) for r in rows_125) / len(rows_125)
        _won_all = sum(1 for r in _raw if r.get("won") == "1")
        _won_125 = sum(1 for r in _raw if r.get("ourver") == "125" and r.get("won") == "1")
        check("pooled share matches the surface", round(share_all, 4), round(_won_all / _n_all, 4))
        check("v125 share matches the surface", round(share_125, 4), round(_won_125 / _n_125, 4))
        check("the two shares actually DIFFER", abs(share_all - share_125) > 0.01, True)
        matches_125 = len({r["match"] for r in rows_125})
        check("ourver==125 distinct matches == 61", matches_125, 61)

        # ===== FIXTURE 3: MUTATION — the most important one. Point the era
        # definition at a version that DOES NOT EXIST; the live path must return
        # EMPTY and say so, never silently fall back to pooled. Driven BOTH ways:
        # a real era on the SAME query still returns data, so this isn't just an
        # always-empty stub. =====
        print("\n--- fixture 3: MUTATION (no silent fallback to pooled) ---")
        rows_missing, used_missing = our_rows(LADDER, era=999999)
        check("nonexistent version era=999999 -> empty, not pooled",
              len(rows_missing), 0)
        check("...and NOT the pooled count (4825) by accident",
              len(rows_missing) != len(rows_all), True)
        rows_real, _ = our_rows(LADDER, era=125)
        check("...while a REAL era on the same surface still returns data",
              len(rows_real) > 0, True)

        rows_live, used_live = our_rows(LADDER, era="live")
        check("era='live' (current hint) -> returns data",
              len(rows_live) > 0, True)
        check("era='live' -> distinct from era='all'",
              len(rows_live) != len(rows_all), True)

        # ===== era='live' TWO-WAY ALARM against the tape (corpus/ladder_games.tsv's
        # actual max ourver). Each cell captures its OWN buffer, nested inside the
        # outer stderr-swallow, so this can inspect exactly what printed. Driven
        # BOTH ways plus the equal/silent case, per this repo's own rule: "a check
        # that has never produced the other verdict has not been seen to check" —
        # a one-directional alarm has not been seen to alarm.
        #
        # ⛔ Mutates LIVE_VERSION_HINT via `global`, not a fresh `import era_guard`
        # — that creates a SEPARATE module object when this file runs as __main__
        # (as --selftest does), so assigning through it silently no-ops on the
        # module actually being called. This is the exact bug the first cut of the
        # old LIVE_VERSION mutation cell had (it passed with got=140 because the
        # mutation never took) — fixed there, and reapplied here rather than risk
        # reintroducing it. =====
        print("\n--- era='live' hint vs tape: two-way alarm (both directions + equal) ---")
        global LIVE_VERSION_HINT, LIVE_VERSION_HINT_TS
        original_hint = LIVE_VERSION_HINT
        original_hint_ts = LIVE_VERSION_HINT_TS
        with open(LADDER, newline="") as fh:
            _lad = list(csv.DictReader(fh, delimiter="\t"))
        real_data_max = max(int(r["ourver"]) for r in _lad if r.get("ourver"))
        real_data_ts = max((r.get("created") or "") for r in _lad)

        # ===== THE PURE RESOLVER, ALL SEVEN STATES, WITH LITERAL ARGUMENTS =====
        # Added s48 with the derive-don't-embed rewrite. The end-to-end cells
        # below can only reach the states the two REAL tapes happen to be in
        # today; this table reaches every branch on every day, which is the only
        # way `rollback` and the two BLIND arms are ever seen to fire at all.
        _H = "2026-08-17T07:12Z"          # a poll stamp NEWER than the ladder row
        _OLD = "2026-08-17T05:00Z"        # a poll stamp OLDER than the ladder row
        _T = "2026-08-17T06:12:59.805Z"   # the ladder tape's shape, note the format
        for _label, _args, _want_v, _want_tag in (
            ("equal -> silent", (155, _H, 155, _T), 155, None),
            ("hint ahead -> fresh_ship, HINT wins", (158, _H, 157, _T), 158, "fresh_ship"),
            ("hint behind + poll NEWER -> rollback, HINT wins",
             (155, _H, 157, _T), 155, "rollback"),
            ("hint behind + poll OLDER -> stale_hint, TAPE wins",
             (155, _OLD, 157, _T), 157, "stale_hint"),
            ("no poll tape -> hint_blind, TAPE wins loudly", (None, None, 157, _T), 157, "hint_blind"),
            ("no ladder tape -> tape_blind, HINT unverified", (155, _H, None, None), 155, "tape_blind"),
            ("neither -> REFUSES (no embedded fallback)", (None, None, None, None), None, "blind"),
        ):
            _v, _tag, _msg = _resolve_live(*_args)
            check(f"_resolve_live: {_label}", (_v, _tag), (_want_v, _want_tag))
        # ...and the refusal is a RAISE at the caller, not a None nobody checks.
        _raised = False
        try:
            LIVE_VERSION_HINT, LIVE_VERSION_HINT_TS = None, None
            _saved_ladder = globals()["_LADDER_FOR_LIVE_CHECK"]
            globals()["_LADDER_FOR_LIVE_CHECK"] = ROOT / "corpus" / "__no_such_tape__.tsv"
            with contextlib.redirect_stderr(io.StringIO()):
                _resolve_live_version()
        except EraLiveUnresolvable:
            _raised = True
        finally:
            globals()["_LADDER_FOR_LIVE_CHECK"] = _saved_ladder
            LIVE_VERSION_HINT, LIVE_VERSION_HINT_TS = original_hint, original_hint_ts
        check("both surfaces blind -> EraLiveUnresolvable raised, never a guessed era",
              _raised, True)
        _ok_ver = None
        with contextlib.redirect_stderr(io.StringIO()):
            _ok_ver, _ = _resolve_live_version()
        check("...but the same call with the real surfaces does NOT raise",
              isinstance(_ok_ver, int) and _ok_ver > 0, True)

        # --- direction 1: hint BEHIND the tape and the POLL TAPE IS OLDER (a
        # lagging poller, not a rollback) -> STALE HINT alarm fires, TAPE wins.
        # ⛔ The timestamp must be forced too. Before s48 the hint was a hand-typed
        # int with no clock, so "below the tape" could only mean "stale"; now that
        # it is derived from a poll tape, below-the-tape is AMBIGUOUS between lag
        # and rollback and only the clock separates them. A cell that forced the
        # version alone would silently test the ROLLBACK branch instead. ---
        stale_buf = io.StringIO()
        try:
            LIVE_VERSION_HINT, LIVE_VERSION_HINT_TS = 1, "2000-01-01T00:00Z"
            with contextlib.redirect_stderr(stale_buf):
                rows_stale, used_stale = our_rows(LADDER, era="live")
        finally:
            LIVE_VERSION_HINT, LIVE_VERSION_HINT_TS = original_hint, original_hint_ts
        check("stale hint (v1, old poll stamp) -> resolves to the TAPE's max, not the hint",
              used_stale, f"live (v{real_data_max})")
        check("stale hint -> STALE HINT alarm text fires",
              "STALE HINT" in stale_buf.getvalue(), True)
        rows_at_data_max, _ = our_rows(LADDER, era=real_data_max)
        check("stale hint -> rows match era=<tape max> exactly (not empty, not pooled)",
              len(rows_stale) == len(rows_at_data_max) and len(rows_stale) > 0, True)

        # --- direction 1b: the SAME low hint with a NEWER poll stamp must take the
        # OTHER branch. This is the cell that proves the clock is load-bearing
        # rather than decorative — same version, opposite verdict. ---
        roll_buf = io.StringIO()
        try:
            LIVE_VERSION_HINT, LIVE_VERSION_HINT_TS = 1, "2099-01-01T00:00Z"
            with contextlib.redirect_stderr(roll_buf):
                rows_roll, used_roll = our_rows(LADDER, era="live")
        finally:
            LIVE_VERSION_HINT, LIVE_VERSION_HINT_TS = original_hint, original_hint_ts
        check("same low hint + NEWER poll stamp -> ROLLBACK, hint wins (clock is load-bearing)",
              used_roll, "live (v1)")
        check("rollback -> ROLLBACK text fires and STALE HINT does not",
              ("ROLLBACK" in roll_buf.getvalue())
              and ("STALE HINT" not in roll_buf.getvalue()), True)
        _rows_v1, _ = our_rows(LADDER, era=1)
        check("rollback -> rows are exactly era=1's, NOT pooled",
              (len(rows_roll), len(rows_roll) == len(_lad)),
              (len(_rows_v1), False))

        # --- direction 2: hint AHEAD of the tape (normal fresh-ship gap) -> a NOTE
        # fires (never the stale alarm), the HINT wins, and it must not read
        # through to pooled data even though no rows exist at that version yet ---
        fresh_buf = io.StringIO()
        try:
            LIVE_VERSION_HINT = 999999
            with contextlib.redirect_stderr(fresh_buf):
                rows_fresh, used_fresh = our_rows(LADDER, era="live")
        finally:
            LIVE_VERSION_HINT = original_hint
        fresh_text = fresh_buf.getvalue()
        check("fresh-ship hint (v999999) -> resolves to the HINT, not the tape",
              used_fresh, "live (v999999)")
        check("fresh-ship hint -> 'has not seen it yet' note fires, STALE alarm does not",
              ("has not seen it yet" in fresh_text) and ("STALE HINT" not in fresh_text), True)
        check("fresh-ship hint -> empty (no data at v999999), NOT pooled",
              len(rows_fresh), 0)

        # --- the DERIVATION itself: it must actually read the poll tape, and it
        # must read the LAST row rather than the max (a rollback moves the tag
        # DOWN, and a max would be blind to exactly the case this rewrite exists
        # for). Driven against a fixture whose last row is NOT its max. ---
        _fix = ROOT / "scratchpad" / "_era_guard_hint_fixture.tsv"
        try:
            _fix.write_text("timestamp\trating\tmatches\tactive_bot\tnote\ttier\n"
                            "2026-08-17T07:00Z\t1800\t1\tv157\tx\tE\n"
                            "2026-08-17T07:05Z\t1800\t1\tv155\tx\tE\n")
            _saved_tape = globals()["_LIVE_HINT_TAPE"]
            globals()["_LIVE_HINT_TAPE"] = _fix
            check("derive reads the LAST poll row, not the max (rollback-visible)",
                  _derive_live_hint(), (155, "2026-08-17T07:05Z"))
            globals()["_LIVE_HINT_TAPE"] = ROOT / "scratchpad" / "__no_such_poll_tape__.tsv"
            check("...and a missing poll tape derives BLIND, never a number",
                  _derive_live_hint(), (None, None))
        finally:
            globals()["_LIVE_HINT_TAPE"] = _saved_tape
            _fix.unlink(missing_ok=True)

        # --- equal case: whatever the CURRENT unforced state actually is.
        # Computed against ground truth rather than hardcoded, so this cell stays
        # correct (and itself becomes part of the alarm) whether or not the hint
        # has drifted by the time this runs. ---
        equal_buf = io.StringIO()
        with contextlib.redirect_stderr(equal_buf):
            rows_now, used_now = our_rows(LADDER, era="live")
        equal_text = equal_buf.getvalue()
        # Ground truth for TODAY'S state, computed the same way the resolver does
        # — including the clock arm, so this cell does not quietly assume the
        # pre-s48 "tape always wins when it is ahead" rule.
        expected_now, _tag_now, _ = _resolve_live(
            original_hint, original_hint_ts, real_data_max, real_data_ts)
        if original_hint == real_data_max:
            print(f"  [note] LIVE_VERSION_HINT (v{original_hint}) == tape max "
                  f"(v{real_data_max}) RIGHT NOW — the silent/equal path is "
                  f"exercised LIVE today, not only under forcing. (The two cells "
                  f"above are the only ones forcing a disagreement.)")
        else:
            print(f"  [note] the poll tape's holder (v{original_hint}) != ladder "
                  f"tape max (v{real_data_max}) RIGHT NOW — resolved as "
                  f"'{_tag_now}'. The two surfaces disagree at the moment this "
                  f"ran and the cross-check is naming it live, which is the "
                  f"point of building it.")
        check("current (unforced) state: era_used matches the actually-resolved version",
              used_now, f"live (v{expected_now})")
        # "silent" means silent about the HINT-vs-TAPE comparison specifically —
        # _rows_ladder_games still prints its own unrelated freshness line for
        # the surface it opened, so the bar is "no alarm/note markers", not a
        # literally empty buffer.
        has_alarm_or_note = any(m in equal_text for m in
                                ("STALE HINT", "has not seen it yet", "ROLLBACK",
                                 "HINT BLIND", "cross-check UNAVAILABLE"))
        check("current (unforced) state: silent iff hint==tape, else something fires",
              (not has_alarm_or_note) if original_hint == real_data_max else has_alarm_or_note,
              True)

        # ===== Multi-surface coverage: meta_join.tsv =====
        #
        # ⛔ THESE CELLS USED TO BE FROZEN ABSOLUTE COUNTS (8338 / 1185 / 42778 /
        # 9018) AND ALL FOUR WERE FAILING, EVERY RUN, FOR DAYS — measured at the
        # s48 wrap: `SELFTEST FAIL (4)`, entirely because the corpus GREW (and
        # meta_join's v125 count grew too, from re-decoded archives: a "frozen"
        # era is not a frozen ROW COUNT). A selftest that always fails is a
        # selftest nobody can gate on; the four real assertions in this file were
        # being read past to get to the noise. Same class as the derived hint
        # above: EMBEDDED WORLD-STATE in a tool, drifting silently.
        #
        # WHAT REPLACES THEM: an INDEPENDENT recount written to the SPEC (the
        # module docstring's SURFACES section), not copied from the reader under
        # test, plus a MONOTONE FLOOR calibrated on a named date. A count that
        # DROPS is still a failure — a corpus that shrinks is an alarm — but
        # growth is not. Driven to the other verdict below by mutating the
        # recount.
        print("\n--- meta_join.tsv (per-row resolution via us_side) ---")

        def _recount_meta(want):
            """Independent our-side count: us_side names the seat, the seat names
            the version column, the version must parse. Written from the spec."""
            n = 0
            with _open_tsv(META) as fh:
                for r in csv.DictReader(fh, delimiter="\t"):
                    col = {"a": "teamAVersion", "b": "teamBVersion"}.get(r.get("us_side"))
                    if not col:
                        continue
                    raw = r.get(col) or ""
                    if not raw.lstrip("-").isdigit():
                        continue
                    if want is None or int(raw) == want:
                        n += 1
            return n

        mj_all, _ = our_rows(META, era="all")
        mj_125, _ = our_rows(META, era=125)
        check("meta_join era='all' == an INDEPENDENT our-side recount", len(mj_all), _recount_meta(None))
        check("meta_join era=125 == the same recount at v125", len(mj_125), _recount_meta(125))
        check("meta_join era='all' has not SHRUNK below the 2026-08-17 floor (8338)",
              len(mj_all) >= 8338, True)
        # MUTATION: the recount must be able to disagree, or it is a constant
        # column validating anything. Compare against a deliberately wrong recount.
        check("...and the recount CAN disagree (mutation: wrong era)",
              len(mj_all) == _recount_meta(125), False)
        check("meta_join both non-empty and different",
              len(mj_all) > 0 and len(mj_125) > 0 and len(mj_all) != len(mj_125), True)
        mj_raised = False
        try:
            our_rows(META)
        except EraNotSpecified:
            mj_raised = True
        check("meta_join also raises with no era", mj_raised, True)

        # ===== Multi-surface coverage: a join.tsv-backed surface =====
        print("\n--- build_agg.tsv (via corpus/join.tsv) ---")
        def _recount_join(surface, team_col_name, want):
            """Independent count for a join.tsv-backed surface: join.tsv names our
            engine team ordinal and our version per FILE; a row is ours iff its
            team column equals that ordinal. Written from the spec, not copied."""
            mapping = {}
            with open(META.parent / "join.tsv", "rt", newline="") as fh:
                for r in csv.DictReader(fh, delimiter="\t"):
                    try:
                        mapping[r["file"]] = (int(r["our_team"]), int(r["ourver"]))
                    except (KeyError, ValueError):
                        continue
            n = 0
            with _open_tsv(surface) as fh:
                for r in csv.DictReader(fh, delimiter="\t"):
                    info = mapping.get(r.get("file"))
                    if info is None:
                        continue
                    ours, ver = info
                    raw = r.get(team_col_name)
                    if raw is None or not str(raw).strip().lstrip("-").isdigit():
                        continue
                    if int(raw) != ours:
                        continue
                    if want is None or ver == want:
                        n += 1
            return n

        ba_all, _ = our_rows(BUILD_AGG, era="all")
        ba_125, _ = our_rows(BUILD_AGG, era=125)
        _ba_col = _team_column("build_agg.tsv", list(ba_all[0].keys())) if ba_all else "team"
        check("build_agg era='all' == an INDEPENDENT join-table recount",
              len(ba_all), _recount_join(BUILD_AGG, _ba_col, None))
        check("build_agg era=125 == the same recount at v125",
              len(ba_125), _recount_join(BUILD_AGG, _ba_col, 125))
        check("build_agg era='all' has not SHRUNK below the 2026-08-17 floor (42778)",
              len(ba_all) >= 42778, True)
        check("build_agg both non-empty and different",
              len(ba_all) > 0 and len(ba_125) > 0 and len(ba_all) != len(ba_125), True)

        print("\n--- econ.tsv (KNOWN CORRUPT, but era-filterable) ---")
        econ_all, _ = our_rows(ECON, era="all")
        econ_125, _ = our_rows(ECON, era=125)
        _ec_col = _team_column("econ.tsv", list(econ_all[0].keys())) if econ_all else "team"
        check("econ era='all' == an INDEPENDENT join-table recount",
              len(econ_all), _recount_join(ECON, _ec_col, None))
        check("econ era=125 == the same recount at v125",
              len(econ_125), _recount_join(ECON, _ec_col, 125))
        check("econ era='all' has not SHRUNK below the 2026-08-17 floor (9018)",
              len(econ_all) >= 9018, True)

        # Corruption warning must actually fire — checked OUTSIDE the redirect
        # below so we can inspect it; done as its own capture here.

        # ===== era spec parsing: list and "N+" forms, both directions =====
        print("\n--- era spec forms: list, 'N+', bad spec ---")
        rows_list, used_list = our_rows(LADDER, era=[125, 140])
        _r125, _ = our_rows(LADDER, era=125)
        _r140, _ = our_rows(LADDER, era=140)
        check("era=[125,140] == era(125) + era(140), an invariant not a snapshot",
              len(rows_list), len(_r125) + len(_r140))
        rows_plus, used_plus = our_rows(LADDER, era="125+")
        _n_plus = sum(1 for r in _raw
                      if str(r.get("ourver", "")).isdigit() and int(r["ourver"]) >= 125)
        check("era='125+' == every row at ourver>=125", len(rows_plus), _n_plus)
        check("era='125+' is a STRICT superset of era=125", len(rows_plus) > len(rows_125), True)
        check("era='125+' label", used_plus, "v125+")
        bad_raised = False
        try:
            our_rows(LADDER, era="banana")
        except ValueError:
            bad_raised = True
        check("garbage era string raises ValueError", bad_raised, True)
        ok_raised = False
        try:
            our_rows(LADDER, era=125)
        except ValueError:
            ok_raised = True
        check("...but a well-formed era does not", ok_raised, False)

        # ===== unsupported surface: named, not silently pooled =====
        print("\n--- unsupported surface ---")
        unsup_raised = False
        try:
            our_rows(ROOT / "corpus" / "not_a_real_surface.tsv", era="all")
        except EraSurfaceUnsupported:
            unsup_raised = True
        check("unknown surface raises EraSurfaceUnsupported", unsup_raised, True)
        supported_raised = False
        try:
            our_rows(LADDER, era="all")
        except EraSurfaceUnsupported:
            supported_raised = True
        check("...but a KNOWN surface does not", supported_raised, False)

    # The econ.tsv corruption warning, checked with stderr visible so the
    # assertion is on real captured text, not a guess that the print happened.
    print("\n--- econ.tsv corruption warning actually fires ---")
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        our_rows(ECON, era="all")
    check("econ.tsv open emits the KNOWN CORRUPT warning",
          "KNOWN CORRUPT" in buf.getvalue(), True)

    print("\nSELFTEST", "PASS" if not bad else f"FAIL ({bad})")
    return 1 if bad else 0


def main() -> int:
    if "--selftest" in sys.argv[1:]:
        return selftest()
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
