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
"""
from __future__ import annotations

import csv
import gzip
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from freshness import assert_fresh  # noqa: E402


class EraNotSpecified(Exception):
    """Raised when our_rows() is called with no era= — the whole point of this file."""


class EraSurfaceUnsupported(Exception):
    """Raised when a surface cannot be era-filtered at all. Never returns
    unfiltered rows in this case — see the module docstring's SURFACES section."""


# ===== LIVE_VERSION_HINT — see "WHAT era=\"live\" MEANS" above for why this is
# a hand-maintained constant rather than something parsed out of PROGRAMME.md. =====
#
# PROGRAMME.md's INCUMBENT field is a bot-TREE PATH (`bots/_v223sealrepair`), not
# the platform submission-version number the corpus surfaces key on. The tree
# name's own digits (223) are a DIFFERENT counter from the platform version (140)
# — confirmed live 2026-08-14 against HANDOVER.md's banner ("LIVE: v140 =
# `bots/_v223sealrepair`") and cross-checked as the max `ourver` present in
# corpus/ladder_games.tsv. Update this by hand on every ship; do not attempt to
# derive it from INCUMBENT's tree-path digits, and do not parse HANDOVER.md's
# prose banner into this file — it is not a stable, parsed surface.
#
# ⭐ THIS CONSTANT IS A HINT, NOT THE LAST WORD, PER MAGNUS'S CATCH 2026-08-14 —
# a hand-maintained value nobody updates on the next ship is the SAME failure
# class this file exists to close: era="live" would then report a confident
# WRONG era under this file's own name. `_resolve_live_version()` below turns it
# into a TWO-WAY ALARM against the max `ourver` actually seen in
# corpus/ladder_games.tsv (the one place this cross-check happens, so it can't
# drift between callers): if the tape has gone PAST the hint, the hint is stale
# (we shipped and forgot to bump this file) and the TAPE wins, loudly. If the
# hint is AHEAD of the tape, that's the normal few minutes right after a ship —
# the ladder hasn't paired the new version yet — and the HINT wins, quietly
# noted rather than alarmed. Naively trusting the tape alone would be wrong in
# THIS second direction: for ~20 minutes post-ship it would silently return the
# previous version's rows under the name "live". Neither branch ever falls
# through to a pooled read — both resolve to one concrete version number.
LIVE_VERSION_HINT = 140  # bots/_v223sealrepair "Loki v10", shipped 2026-08-14T11:37Z

# The one place era="live" cross-checks the hint against reality.
_LADDER_FOR_LIVE_CHECK = ROOT / "corpus" / "ladder_games.tsv"


def _resolve_live_version():
    """(resolved_version, tag). tag in {"stale_hint", "fresh_ship", None}.

    None means the hint and the tape agree (or the tape couldn't be read) —
    the silent, normal path. Always prints when it disagrees; never silent
    about a disagreement, never loud about agreement."""
    hint = LIVE_VERSION_HINT
    data_max = None
    with_freshness_age = None
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
    except FileNotFoundError:
        pass
    if _LADDER_FOR_LIVE_CHECK.exists():
        _, with_freshness_age, _ = assert_fresh(_LADDER_FOR_LIVE_CHECK, max_age_h=24)
    age_txt = f"{with_freshness_age:.1f}h" if with_freshness_age is not None else "unknown"

    if data_max is None:
        # No tape to cross-check against at all -- use the hint, unverified,
        # and say so rather than pretending this was checked.
        print(f"[era_guard] era='live' cross-check UNAVAILABLE "
              f"({_LADDER_FOR_LIVE_CHECK} missing or unreadable) — using "
              f"LIVE_VERSION_HINT v{hint} UNVERIFIED.", file=sys.stderr)
        return hint, None

    if data_max > hint:
        print(f"[era_guard] ⛔ era='live' STALE HINT: LIVE_VERSION_HINT is v{hint} "
              f"but ladder_games.tsv's newest ourver is v{data_max} (tape age "
              f"{age_txt}) — the constant was not bumped after a ship. USING "
              f"v{data_max} (the tape), NOT the stale hint.", file=sys.stderr)
        return data_max, "stale_hint"

    if data_max < hint:
        print(f"[era_guard] era='live': LIVE_VERSION_HINT is v{hint} but "
              f"ladder_games.tsv has not seen it yet (newest ourver v{data_max}, "
              f"tape age {age_txt}) — normal in the minutes right after a ship, "
              f"before the ladder has paired the new version. USING the hint "
              f"v{hint}.", file=sys.stderr)
        return hint, "fresh_ship"

    return hint, None  # equal — silent, normal path


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
        for r in csv.DictReader(fh, delimiter="\t"):
            info = mapping.get(r.get("file"))
            if info is None:
                continue  # not one of our reconciled games, at any era
            our_team, ourver = info
            try:
                if int(r["team"]) != our_team:
                    continue
            except (KeyError, ValueError):
                continue
            if pred(ourver):
                out.append(r)
    return out


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
        check("era='all' returns data (n games)", len(rows_all), 4825)
        check("era=125 returns data (n games)", len(rows_125), 305)
        share_all = sum(int(r["won"]) for r in rows_all) / len(rows_all)
        share_125 = sum(int(r["won"]) for r in rows_125) / len(rows_125)
        check("pooled game share ~51.2%", round(share_all, 4), round(2472 / 4825, 4))
        check("ourver==125 game share ~55.7%", round(share_125, 4), round(170 / 305, 4))
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
        global LIVE_VERSION_HINT
        original_hint = LIVE_VERSION_HINT
        with open(LADDER, newline="") as fh:
            real_data_max = max(int(r["ourver"]) for r in csv.DictReader(fh, delimiter="\t")
                                 if r.get("ourver"))

        # --- direction 1: hint STALE (below the tape) -> alarm fires, TAPE wins ---
        stale_buf = io.StringIO()
        try:
            LIVE_VERSION_HINT = 1
            with contextlib.redirect_stderr(stale_buf):
                rows_stale, used_stale = our_rows(LADDER, era="live")
        finally:
            LIVE_VERSION_HINT = original_hint
        check("stale hint (v1) -> resolves to the TAPE's max, not the hint",
              used_stale, f"live (v{real_data_max})")
        check("stale hint -> STALE HINT alarm text fires",
              "STALE HINT" in stale_buf.getvalue(), True)
        rows_at_data_max, _ = our_rows(LADDER, era=real_data_max)
        check("stale hint -> rows match era=<tape max> exactly (not empty, not pooled)",
              len(rows_stale) == len(rows_at_data_max) and len(rows_stale) > 0, True)

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

        # --- equal case: whatever the CURRENT unforced state actually is.
        # Computed against ground truth rather than hardcoded, so this cell stays
        # correct (and itself becomes part of the alarm) whether or not the hint
        # has drifted by the time this runs. ---
        equal_buf = io.StringIO()
        with contextlib.redirect_stderr(equal_buf):
            rows_now, used_now = our_rows(LADDER, era="live")
        equal_text = equal_buf.getvalue()
        expected_now = real_data_max if real_data_max > original_hint else original_hint
        if original_hint == real_data_max:
            print(f"  [note] LIVE_VERSION_HINT (v{original_hint}) == tape max "
                  f"(v{real_data_max}) RIGHT NOW — the silent/equal path is "
                  f"exercised LIVE today, not only under forcing. (The two cells "
                  f"above are the only ones forcing a disagreement.)")
        else:
            print(f"  [note] LIVE_VERSION_HINT (v{original_hint}) != tape max "
                  f"(v{real_data_max}) RIGHT NOW — the constant is out of sync "
                  f"with the tape at the moment this ran; the cross-check is "
                  f"catching that live, which is the point of building it.")
        check("current (unforced) state: era_used matches the actually-resolved version",
              used_now, f"live (v{expected_now})")
        # "silent" means silent about the HINT-vs-TAPE comparison specifically —
        # _rows_ladder_games still prints its own unrelated freshness line for
        # the surface it opened, so the bar is "no alarm/note markers", not a
        # literally empty buffer.
        has_alarm_or_note = ("STALE HINT" in equal_text) or ("has not seen it yet" in equal_text)
        check("current (unforced) state: silent iff hint==tape, else something fires",
              (not has_alarm_or_note) if original_hint == real_data_max else has_alarm_or_note,
              True)

        # ===== Multi-surface coverage: meta_join.tsv =====
        print("\n--- meta_join.tsv (per-row resolution via us_side) ---")
        mj_all, _ = our_rows(META, era="all")
        mj_125, _ = our_rows(META, era=125)
        check("meta_join era='all' our-side rows", len(mj_all), 8338)
        check("meta_join era=125 our-side rows", len(mj_125), 1185)
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
        ba_all, _ = our_rows(BUILD_AGG, era="all")
        ba_125, _ = our_rows(BUILD_AGG, era=125)
        check("build_agg era='all' our rows", len(ba_all), 42778)
        check("build_agg era=125 our rows", len(ba_125), 3203)
        check("build_agg both non-empty and different",
              len(ba_all) > 0 and len(ba_125) > 0 and len(ba_all) != len(ba_125), True)

        print("\n--- econ.tsv (KNOWN CORRUPT, but era-filterable) ---")
        econ_all, _ = our_rows(ECON, era="all")
        econ_125, _ = our_rows(ECON, era=125)
        check("econ era='all' our rows", len(econ_all), 9018)
        check("econ era=125 our rows", len(econ_125), 679)

        # Corruption warning must actually fire — checked OUTSIDE the redirect
        # below so we can inspect it; done as its own capture here.

        # ===== era spec parsing: list and "N+" forms, both directions =====
        print("\n--- era spec forms: list, 'N+', bad spec ---")
        rows_list, used_list = our_rows(LADDER, era=[125, 140])
        check("era=[125,140] combined count", len(rows_list), 320)
        rows_plus, used_plus = our_rows(LADDER, era="125+")
        check("era='125+' count", len(rows_plus), 395)
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
