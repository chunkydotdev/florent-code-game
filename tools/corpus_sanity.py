#!/usr/bin/env python3
"""Fail loudly on corpus columns that are silently dead.

WHY: corpus/econ.tsv has a `shots` column that is 0 in all 25,530 rows --
replay_econ.py declares it and then does `elif unum == 12: pass`. Every OTHER
column in that file is populated, so the zero does not look like a bug, it
looks like a FINDING. Anyone asking the corpus "how often do we fire?" gets 0
and could reasonably conclude we never shoot. (The live data is in
build_agg.tsv under metric == 'shot'.)

An all-zero numeric column is either a real fact about the game or a decoder
that never fired. It is never safe to assume which.

Usage:  .venv/bin/python tools/corpus_sanity.py [corpus_dir]
"""
import csv, sys
from pathlib import Path

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

# IMPLEMENTS: D43 -- 'same column' is not 'same meaning' when the column is
# keyed to a per-row field.
#
# ===== CONDITIONALLY DEAD: ZERO INSIDE A SUBGROUP, ALIVE OVERALL =====
# A NEW CLASS, added s29 2026-08-11, and this tool CANNOT SEE IT. Every check
# below asks "is this column all-zero across the file". These columns are not:
# they are all-zero within one PARTITION of the rows and healthy in the other,
# so they pass every gate here while being a constant column to anyone who cuts
# on that partition -- which is exactly what a per-team or per-arm analysis does.
#
# THE INCIDENT. `throws.tsv` carries core_atk / any_atk / reached. Split by
# whether the THROWN BOT is on the thrower's team:
#     KIDNAP (cross-team)      172,547 rows   reached 0.00%  any_atk 0.00%  core_atk 0.00%
#     SELF-INSERT (same team)  101,659 rows   reached 17.32% any_atk 8.07%  core_atk 1.72%
# Three columns, exactly zero across 172,547 rows. `reached` at 0.00% is
# physically impossible as a result -- the engine places a thrown bot at the
# target tile -- which is the tell that it is structural.
#
# ⛔ THE CAUSE PUBLISHED HERE FIRST WAS WRONG, AND SO WAS THE PARTITION. Corrected
# 2026-08-11 after a side-lane sweep; verified at source and in the data by me.
#
# I WROTE: the columns are keyed to the thrown bot's own enemy (`foot[1-b.team]`),
# so for a kidnap `core_atk` counts the kidnapped bot attacking OUR core.
# THAT IS FALSE AS THE CAUSE. Split on `kind` rather than on team, 275,358 rows:
#     EXILE     171,984   reached 0.00%   any_atk 0.00%   core_atk 0.00%
#     INSERT     77,844   reached 22.65%  any_atk 10.61%  core_atk 2.25%
#     RETREAT    24,277   reached 0.00%   any_atk 0.00%   core_atk 0.00%  <-- SAME TEAM
#     UNATTRIB    1,253   reached 0.00%   ...
# RETREAT IS SAME-TEAM AND IDENTICALLY ZERO ACROSS 24,277 ROWS. Team keying cannot
# explain that, and it is the observation that falsifies my version.
#
# THE REAL CAUSE, `tools/corpus/replay_throws.py:134`:
#     if kind == "INSERT":  active[eid] = rec
# ONLY INSERT ROWS EVER ENTER `active`, and both the `builderAttack` handler and
# the `reached` loop read exclusively from `active`. For every non-INSERT throw
# THE COLUMNS ARE NEVER COMPUTED AT ALL. The team-keyed line at :157 sits
# DOWNSTREAM OF A GATE IT NEVER PASSES -- re-keying it would change nothing.
#
# ⇒ THE CONCLUSION THAT MATTERED IS UNCHANGED AND IS IF ANYTHING STRONGER: a zero
#   in these columns for any non-INSERT throw is NOT A MEASUREMENT OF ANYTHING.
#   "The launcher raid delivered nothing, 0 of 4,169" remains withdrawn.
#
# ⚠ AND THE FIRST VERSION OF THIS CHECK COMMITTED THE DEFECT IT WAS BUILT TO
#   CATCH: it split on `tteam == bteam`, which pools the 24,277 structurally-dead
#   RETREAT rows into the half it prints as HEALTHY -- publishing 17.29% against a
#   true INSERT rate of 22.65%, diluted ~24%. A partition that is not the
#   defect's own partition is a wrong denominator wearing a control's clothes.
#   Now split on `kind`, which is the column the decoder itself branches on.
#
# IT NEARLY RETIRED A LIVE PLANK. The research arm read "our throws: 0 of 4,169
# any_atk" as "the launcher raid delivers nothing" and was about to close the
# kidnap road -- LOKI-14's whole mechanism, and one of three roads CLAUDE.md
# lists as never balance-changed and still open. Its within-sample control (the
# opponent's non-zero rows, same decoder, same 485 files) proved the code path
# was LIVE but could not prove the two populations were COMMENSURABLE, because
# the field that differs between them is the one the column is defined against.
#
# ⇒ THE GENERAL RULE, and it is the fifth constant-column incident in two days:
#   "same column" is not "same meaning" when the column's definition is keyed to
#   a per-row team or side. Before cutting a column by a partition, check whether
#   the column is DEFINED relative to that partition.
CONDITIONALLY_DEAD = {
    ("throws.tsv", "core_atk"): "ZERO for all cross-team (kidnap) throws; "
                                "measures the THROWN bot attacking ITS enemy, so "
                                "for a kidnap it counts the enemy hitting OUR core",
    ("throws.tsv", "any_atk"): "same partition, same cause as core_atk",
    ("throws.tsv", "reached"): "same partition; 0.00% over 172,547 kidnaps is "
                               "structurally impossible, not a measurement",
}

KNOWN_DEAD = {
    ("econ.tsv", "shots"): "replay_econ.py:109 `elif unum == 12: pass` "
                          "-- use build_agg.tsv metric=='shot'",
    # s25 boot. Same bug shape as `shots`, found by this tool one run after the
    # trap-7 fix taught it to look at string columns: `deliveries` is declared
    # in COLS, allocated in cell(), and never incremented -- the
    # distributeResources branch (`elif unum == 4`) iterates the message and
    # `pass`es. Verified 0/33,672 nonzero.
    ("econ.tsv", "deliveries"): "replay_econ.py `elif unum == 4` "
                               "(distributeResources) loops and passes; never "
                               "increments -- use econ.tsv:ti_collected_end "
                               "(cumulative delivered, 28,925/33,672 nonzero)",
    # s25 boot, CORRECTED s25 later the same session -- read the correction
    # before quoting the first half.
    #
    # These four columns ARE dead: the ingest records the literal string "None"
    # because the API rows it reads carry no version. That much was verified
    # twice and stands.
    #
    # WHAT I GOT WRONG WAS THE CONCLUSION I DREW FROM IT. I wrote these up as a
    # permanent DATA FACT -- "the version simply is not in the corpus" -- and
    # routed analysis around them all session on that basis. It is a fact about
    # THESE FILES and was never a fact about the corpus: `replay_archive/` holds
    # 1,260 `<match-id>.meta.json` sidecars carrying teamAVersion, teamBVersion,
    # both team names, both ratings and triggeredBy, joinable to replays on the
    # match-id filename prefix. The versions were on disk the whole time, one
    # file over, while I recorded them as unrecoverable.
    #
    # THE LESSON THIS ENTRY EXISTS TO CARRY: a dead column proves the INGEST
    # never wrote it. It proves nothing about whether the data exists. Do not
    # promote "this decoder has no version" to "we have no version" again.
    # Use tools/corpus/meta_attrib.py (meta.json-first attribution); fall back
    # to league_matches.tsv teamAVersion/teamBVersion on match id for the ~2%
    # of matches with no sidecar. Do not join on these four columns.
    ("join.tsv", "oppver"): "ingest writes literal 'None'; use "
                            "league_matches.tsv teamAVersion/teamBVersion on match id",
    ("ladder_games.tsv", "oppver"): "ingest writes literal 'None'; use "
                                    "league_matches.tsv teamAVersion/teamBVersion on match id",
    ("league_games.tsv", "verA"): "ingest writes literal 'None'; use "
                                  "league_matches.tsv teamAVersion on match id",
    ("league_games.tsv", "verB"): "ingest writes literal 'None'; use "
                                  "league_matches.tsv teamBVersion on match id",
}

# Time-series corpus files and the column carrying their clock. Anything older
# than STALE_H is reported LOUDLY.
_TIMED = {
    "league_matches.tsv": "createdAt",
    "league_games.tsv": "createdAt",
}

# ---------------------------------------------------------------------------
# FROZEN ARCHIVES — a decision on the record, not a silenced alarm.
#
# ⛔ WHY THIS IS A REGISTRY AND NOT AN `if name == ...: continue`.
# `league_games.tsv` froze at 2026-08-09T05:12Z and this check reported it
# correctly, exiting 1, FOR FIFTY HOURS. Nothing was wrong with the alarm --
# it was UNREAD. Every other instrument defect found on 2026-08-11 was an alarm
# that COULD NOT FIRE (audit_trigger suppressing itself, ring_retention passing
# while inverted, plank_status measuring staleness instead of withdrawal,
# ship_watch printing verdicts off a dead tape). **This was the opposite: a
# correct alarm with nothing scheduled to read it, and the builder who DID run
# it at boot skimmed past the line.**
#
# The wrong fix is to silence it, because then a NEW stale file reads the same
# as an accepted one. The right fix is the shape already used by
# tools/plank_ack.tsv: record the DECISION, keep the file loud about being
# frozen, and leave every unregistered file able to alarm.
#
# DISPOSAL DECISION, builder, 2026-08-11: league_games.tsv is RETIRED, not
# revived. It has ONE producer (tools/corpus/league_games.py, never in the
# keeper cycle) and ZERO analysis consumers in tools/ -- meta_attrib.py:84 is a
# filename list and league_matches.py:57 is a docstring. Its sibling
# `league_matches.tsv` IS in the keeper, IS fresh, and is what this very file
# already recommends for the dead `verB` column. Wiring a 50-hour corpse into
# the keeper to serve nobody is spending compute to keep it warm.
# The FILE IS KEPT rather than deleted: two research documents
# (bisons-fast-kill-autopsy-2026-08-10, league-fast-kill-mechanism-2026-08-10)
# were written on it and deleting it destroys their reproducibility. **Both were
# written on 2026-08-10, when it had ALREADY stopped at 08-09 -- so their
# population silently excludes everything after that point, and either needs its
# population restated before it can carry a plank.**
FROZEN_ARCHIVES = {
    "league_games.tsv": (
        "RETIRED 2026-08-11 — froze 2026-08-09T05:12Z, no producer in the keeper "
        "and no analysis consumer in tools/. USE league_matches.tsv INSTEAD "
        "(fresh, keeper-maintained). Kept for the reproducibility of two "
        "2026-08-10 research docs, whose population already excluded everything "
        "after the freeze."),
}

STALE_H = 6


def freshness(root) -> int:
    """A CORPUS FILE MUST REPORT ITS OWN AGE.

    Found s28, 2026-08-10, the hard way: `league_matches.tsv` was **21 hours
    stale** and `league_games.tsv` **33 hours stale**, while `keeper.py` ran
    healthily and logged a fresh `meta_join` every 10 minutes. The replay-derived
    half of the corpus was minutes old; the match-METADATA half had not moved
    since the previous evening, and NOTHING SAID SO.

    It cost real work before it was noticed: a rating table quoted at "~22h
    stale" (correctly flagged by its author), an opponent record verified at
    31 matches when the platform had 32, and a `diverge` cell that read 5 in the
    corpus and 13 on the platform -- the two sources disagreeing about the SAME
    opponent by 8 matches, which is what finally exposed it.

    This is `CLAUDE.md`'s own monitor rule -- "a monitor that reads a file must
    report that file's FRESHNESS" -- applied one level down, to the corpus the
    monitors read. A stale file and a fresh one are byte-identical in every way
    an analysis can see; only the clock separates them.
    """
    from datetime import datetime, timedelta
    stale = 0
    print()
    for name, col in _TIMED.items():
        f = root / name
        if not f.exists():
            continue
        best = ""
        try:
            for r in csv.DictReader(open(f, newline=""), delimiter="\t"):
                v = r.get(col) or ""
                if v > best:
                    best = v
        except OSError:
            continue
        if not best:
            print(f"*** NO CLOCK ***  {name}:{col} absent -- freshness UNKNOWABLE")
            stale += 1
            continue
        try:
            when = datetime.fromisoformat(best.replace("Z", "+00:00").replace("+00:00", ""))
        except ValueError:
            continue
        age = (datetime.utcnow() - when).total_seconds() / 3600
        if name in FROZEN_ARCHIVES:
            # Loud, but not an anomaly: the state is known and the decision is
            # recorded. It must never read as `fresh`, or a join on it looks safe.
            print(f"FROZEN  {name}  newest row {best[:19]}  ({age:.1f}h) — "
                  f"NOT AN ALARM, a recorded decision")
            print(f"            {FROZEN_ARCHIVES[name]}")
            continue
        if age > STALE_H:
            print(f"*** STALE ***  {name}  newest row {best[:19]}  "
                  f"= {age:.1f}h old (threshold {STALE_H}h)")
            print(f"            any analysis joined on this file is reading a "
                  f"world that ended {age:.1f}h ago")
            stale += 1
        else:
            print(f"fresh  {name}  newest row {best[:19]}  ({age:.1f}h)")
    return stale


def conditionally_dead(root) -> int:
    """RE-DERIVE the conditional-dead partitions rather than trusting the note.

    A dict entry is a comment; this is a check. It re-splits `throws.tsv` on the
    partition and prints the live rates for BOTH sides, so:
      * if someone fixes `replay_throws.py`, the kidnap side goes non-zero and
        this says so -- the entry can then be retired instead of outliving its
        cause, which is how KNOWN_DEAD entries rot;
      * the healthy side is printed too, because a check that only ever prints
        the broken half never demonstrates it can tell them apart.
    """
    p = root / "throws.tsv"
    if not p.exists():
        return 0
    import csv as _csv
    from collections import defaultdict
    part = defaultdict(lambda: [0, 0, 0, 0])
    with p.open(newline="") as fh:
        rd = _csv.DictReader(fh, delimiter="\t")
        # Split on `kind` -- THE COLUMN THE DECODER ITSELF BRANCHES ON. Splitting
        # on team was the first version's error and it diluted the live half by
        # ~24% by pooling structurally-dead RETREAT rows into it.
        if not rd.fieldnames or "kind" not in rd.fieldnames:
            return 0
        for r in rd:
            a = part[r.get("kind") or "?"]
            a[0] += 1
            for i, col in enumerate(("reached", "any_atk", "core_atk"), start=1):
                if r.get(col) not in ("", "0", "False", None):
                    a[i] += 1
    print("\nCONDITIONAL-DEAD CHECK  throws.tsv, split on `kind`")
    print("  replay_throws.py:134 admits ONLY kind=='INSERT' into `active`, and "
          "the attack/reach\n  loops read only from `active` -- so every other "
          "kind has these columns NEVER COMPUTED.")
    flipped = 0
    for k, (n, re_, aa, ca) in sorted(part.items(), key=lambda t: -t[1][0]):
        if not n:
            continue
        tag = "  <- LIVE" if k == "INSERT" else (
            "  <- SAME-TEAM AND DEAD: team keying cannot explain this"
            if k == "RETREAT" else "")
        print(f"  {k:9s} n={n:>7d}  reached {re_/n:6.2%}  "
              f"any_atk {aa/n:6.2%}  core_atk {ca/n:6.2%}{tag}")
        if k != "INSERT" and (re_ or aa or ca):
            flipped = 1
    if flipped:
        print("  *** A NON-INSERT KIND IS NO LONGER ALL-ZERO. The decoder "
              "changed. Retire the CONDITIONALLY_DEAD entries and re-read any "
              "finding that relied on them being zero. ***")
    else:
        print("  non-INSERT kinds still identically zero -- this is NOT a "
              "measurement.\n  A zero here says the column was never computed, "
              "never that the throw achieved nothing.")
    return flipped


def pool_check(pool_names=None) -> int:
    """POOL vs FIXTURE vs BOT-TABLE assertion (audit B1, built s36 after the
    2026-08-13 rotation invalidated half the corpus with no alarm).

    Three surfaces must agree with the live pool:
      1. tools/overnight.sh MAPS= (the battery fixture)
      2. maps/<name>.map26 exists (else nothing else is verifiable)
      3. the INCUMBENT tree's MAP_CODES/EXTRA_MAP_CODES contains the map's key
         (else the bot pathfinds blind on it — the v123 livelock class)

    pool_names=None reads `fcode maps list` live; a failed read prints BLIND
    and returns 0 (a network flake must not fail boot) but says so loudly.
    Pass an explicit list to drive the check without the network — the
    selftest drives it to both verdicts that way.
    """
    import re as _re
    import subprocess as _sp
    root = Path(__file__).resolve().parent.parent
    if pool_names is None:
        try:
            out = _sp.run([str(root / ".venv/bin/fcode"), "maps", "list"],
                          capture_output=True, text=True, timeout=30).stdout
            pool_names = _re.findall(r"^\W*│\s*(\w+)\s*│", out, _re.M)
        except Exception:
            pool_names = None
        if not pool_names:
            print("\nPOOL CHECK: BLIND — `fcode maps list` unreadable; the "
                  "pool-vs-fixture assertion certifies NOTHING this boot.")
            return 0
    bad = 0
    m = _re.search(r"^MAPS=\(([^)]*)\)", (root / "tools/overnight.sh").read_text(), _re.M)
    fixture = set(m.group(1).split()) if m else set()
    inc = None
    for ln in (root / "PROGRAMME.md").read_text().splitlines():
        if ln.strip().startswith("INCUMBENT:"):
            inc = ln.split(":", 1)[1].strip()
            break
    keys = set()
    if inc:
        import importlib.util as _ilu
        spec = _ilu.spec_from_file_location("_doc", root / inc / "doctrine.py")
        mod = _ilu.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            keys = set(mod.MAP_CODES) | {k for k, _c in mod.EXTRA_MAP_CODES}
        except Exception as e:
            print(f"\nPOOL CHECK: cannot load {inc}/doctrine.py ({e}) — "
                  f"bot-table half is BLIND")
    sys.path.insert(0, str(root / "tools"))
    from map_encode import entry_for
    for name in pool_names:
        f = root / f"maps/{name}.map26"
        if name not in fixture:
            print(f"  *** POOL: '{name}' in the live pool, NOT in overnight.sh "
                  f"MAPS — batteries cannot draw it"); bad += 1
        if not f.exists():
            print(f"  *** POOL: maps/{name}.map26 MISSING — bot-table coverage "
                  f"unverifiable for it"); bad += 1
            continue
        if keys:
            key, _code = entry_for(f)
            if key not in keys:
                print(f"  *** POOL: '{name}' has NO MAP_CODES entry in {inc} — "
                      f"the bot pathfinds BLIND on it (the v123 livelock class)")
                bad += 1
    for name in sorted(fixture - set(pool_names)):
        print(f"  *** POOL: '{name}' in overnight.sh MAPS but NOT in the live "
              f"pool — batteries spend rows on dead geometry"); bad += 1
    if not bad:
        print(f"\nPOOL CHECK: OK — {len(pool_names)} pool maps all in the "
              f"fixture and all covered by {inc or '?'}")
    return bad


# ===== TRAP 9: duplicate keys on append-mode surfaces (s42, 2026-08-14) =====
# tools/corpus/league_matches.py:77 reads `known = {r["id"] for r in rows}` and
# then appends the complement -- no lock anywhere in the append path. Two
# processes that read `known` before either writes both classify the same rows
# as fresh and both append. Measured 2026-08-14T19:2xZ: league_matches.tsv
# carried 45,436 rows against 45,317 distinct ids -- 119 duplicates, each
# appearing exactly twice, byte-identical, forming two contiguous tail blocks
# (41 + 78 rows) whose row-index gap equals their own batch size, matching two
# writers (keeper + a lane boot sync) racing the same `known` read after the
# 2026-08-14 18:56:33Z reboot re-armed keeper into a boot-sync collision.
# Spec: docs/research/SPEC-corpus-sanity-trap9-duplicate-keys-2026-08-14.md
#
# Explicit three-surface ALLOWLIST, not a glob over corpus/*.tsv. Several
# corpus files are legitimately event-grain and hold repeated keys by
# construction; a trap that fires on a legitimate surface gets muted, and a
# muted trap is worse than no trap.
TRAP9_SURFACES = {
    "league_matches.tsv": ("id",),          # platform match id; the observed defect
    "ladder_games.tsv": ("match", "map"),   # game grain; a match plays each map once
    "meta_join.tsv": ("file",),             # one row per replay file
}


def _trap9_scan_rows(rows, cols):
    """Group `rows` (list of dict) by `cols` and report duplicates.

    Returns dict(n, ndup, excess, mult, identical, examples). `identical` is
    True iff every duplicated key's rows are byte-identical to each other
    (safe keep-first repair), False if any duplicated key's rows differ (a
    worse defect -- two sources disagreeing about the same key -- and must
    NOT be silently deduped), None if there were no duplicates at all.
    """
    from collections import Counter, defaultdict
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        groups[tuple(r.get(c, "") for c in cols)].append(r)
    dup = {k: v for k, v in groups.items() if len(v) > 1}
    n = len(rows)
    if not dup:
        return dict(n=n, ndup=0, excess=0, mult={}, identical=None, examples=[])
    mult = Counter(len(v) for v in dup.values())
    identical = all(all(row == v[0] for row in v[1:]) for v in dup.values())
    excess = sum(len(v) - 1 for v in dup.values())
    examples = [",".join(str(x) for x in k) for k in sorted(dup, key=str)[:5]]
    return dict(n=n, ndup=len(dup), excess=excess, mult=dict(mult),
                identical=identical, examples=examples)


def _trap9_read(path: Path):
    """Returns (rows, None) or (None, reason). Absence/unreadable is a
    distinct outcome from 0 duplicates -- P6 requires this be ANNOUNCED, never
    silently treated as a pass."""
    if not path.exists():
        return None, "absent"
    try:
        with path.open(newline="") as fh:
            return list(csv.DictReader(fh, delimiter="\t")), None
    except OSError as e:
        return None, str(e)


def _trap9_report(name, cols, result) -> int:
    keyname = ",".join(cols)
    if result["ndup"] == 0:
        print(f"  ok    {name}  key=({keyname})  {result['n']} rows, "
              f"0 duplicate keys")
        return 0
    ident_s = "yes" if result["identical"] else "no"
    print(f"  *** FAIL ***  {name}  key=({keyname})  {result['ndup']} duplicate "
          f"key(s), {result['excess']} excess row(s), "
          f"multiplicity={result['mult']}, identical={ident_s}")
    print(f"            examples: {', '.join(result['examples'])}")
    if not result["identical"]:
        print(f"            DIFFERING duplicates -- two sources disagree about "
              f"the same key. DO NOT auto-dedup; repair tool must refuse this "
              f"surface until resolved.")
    return 1


def trap9_duplicate_keys(root: Path) -> int:
    """TRAP 9: duplicate-key FAIL (not WARN) on the three append-mode
    surfaces. Every surface in TRAP9_SURFACES is either platform-id-keyed or
    key-unique by construction, so a duplicate is always a defect there."""
    print("\nTRAP 9  duplicate-key check (append-mode surfaces)")
    bad = 0
    for name, cols in TRAP9_SURFACES.items():
        rows, err = _trap9_read(root / name)
        if rows is None:
            print(f"  *** TRAP9 BLIND ***  {name}: {err} -- duplicate-key "
                  f"check could not run. Absence of a FAIL is NOT a PASS "
                  f"unless the file was read.")
            bad += 1
            continue
        bad += _trap9_report(name, cols, _trap9_scan_rows(rows, cols))
    return bad


def trap9_selftest(root: Path) -> int:
    """Six both-verdicts cells, SPEC sec 3
    (docs/research/SPEC-corpus-sanity-trap9-duplicate-keys-2026-08-14.md).

    P3/P4/P5/P6 are synthetic and self-contained so this selftest does not
    depend on repair timing. P1/P2 read the LIVE corpus files: P1 is a
    positive control only while league_matches.tsv is pre-repair (it degrades
    to 'already repaired' after the dedup lands -- that is expected, not a
    failure of the selftest itself). P2 is the standing negative control on
    the two clean surfaces.
    """
    print("\nTRAP9 SELFTEST")
    ok = True

    # P1 positive, LIVE DATA: league_matches.tsv as it stands right now.
    rows, err = _trap9_read(root / "league_matches.tsv")
    if rows is None:
        print(f"  P1 FAIL-TO-RUN: league_matches.tsv unreadable ({err})")
        ok = False
    else:
        r1 = _trap9_scan_rows(rows, ("id",))
        p1 = r1["ndup"] > 0
        print(f"  P1 (positive, live league_matches.tsv): "
              f"{'FAIL as expected' if p1 else 'clean -- already repaired'} "
              f"ndup={r1['ndup']} mult={r1['mult']} identical={r1['identical']}")

    # P2 negative, LIVE DATA: the two clean surfaces, unmodified.
    for name, cols in (("ladder_games.tsv", ("match", "map")),
                        ("meta_join.tsv", ("file",))):
        rows, err = _trap9_read(root / name)
        if rows is None:
            print(f"  P2 FAIL-TO-RUN: {name} unreadable ({err})")
            ok = False
            continue
        r2 = _trap9_scan_rows(rows, cols)
        p2 = r2["ndup"] == 0
        print(f"  P2 ({name}): {'PASS as expected' if p2 else 'FAIL -- unexpected'} "
              f"ndup={r2['ndup']}")
        ok = ok and p2

    # P3 positive, synthetic: duplicate one row of a clean fixture.
    fixture = [{"k": "a", "v": "1"}, {"k": "b", "v": "2"}, {"k": "a", "v": "1"}]
    r3 = _trap9_scan_rows(fixture, ("k",))
    p3 = r3["ndup"] == 1 and r3["identical"] is True
    print(f"  P3 (synthetic dup, identical): "
          f"{'FAIL as expected' if p3 else 'WRONG'} "
          f"ndup={r3['ndup']} identical={r3['identical']}")
    ok = ok and p3

    # P4 negative, post-repair: keep-first dedup of the same fixture.
    seen: set = set()
    deduped = []
    for r in fixture:
        if r["k"] in seen:
            continue
        seen.add(r["k"])
        deduped.append(r)
    r4 = _trap9_scan_rows(deduped, ("k",))
    p4 = r4["ndup"] == 0
    print(f"  P4 (post-repair, keep-first): "
          f"{'PASS as expected' if p4 else 'WRONG'} ndup={r4['ndup']}")
    ok = ok and p4

    # P5 differing-duplicate: same key, one field altered -- must NOT read as
    # identical=yes, the branch that must not be auto-repaired.
    fixture5 = [{"k": "a", "v": "1"}, {"k": "a", "v": "2"}]
    r5 = _trap9_scan_rows(fixture5, ("k",))
    p5 = r5["ndup"] == 1 and r5["identical"] is False
    print(f"  P5 (differing dup): "
          f"{'FAIL as expected, identical=no' if p5 else 'WRONG'} "
          f"ndup={r5['ndup']} identical={r5['identical']}")
    ok = ok and p5

    # P6 blind: unreadable/absent path must ANNOUNCE, never silently pass.
    rows, err = _trap9_read(root / "__trap9_does_not_exist__.tsv")
    p6 = rows is None and err == "absent"
    print(f"  P6 (blind path): "
          f"{'announced absent as expected' if p6 else 'WRONG'} err={err}")
    ok = ok and p6

    print(f"TRAP9_SELFTEST: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(d="corpus"):
    bad = 0
    if d == "--pool-selftest":
        # both verdicts: the real pool must PASS; a fabricated map must FAIL
        # on all three surfaces (not in fixture, no .map26, no table entry).
        real = pool_check()   # live read; BLIND is acceptable here
        fake = pool_check(["midgard", "notamap999"])
        okA = real == 0
        okB = fake >= 2       # missing from fixture + missing file at minimum
        print(f"POOL_SELFTEST: {'PASS' if okA and okB else 'FAIL'} "
              f"(real={real}, fake_bad={fake})")
        return 0 if okA and okB else 1
    if d == "--trap9-selftest":
        return trap9_selftest(Path("corpus"))
    for f in sorted(Path(d).glob("*.tsv")):
        with open(f) as fh:
            # TRAP 8 (s40 boot, 2026-08-14). league_maps.tsv opens with a `#`
            # provenance line; DictReader took it as a ONE-COLUMN header, every
            # real row overflowed into the None restkey as a LIST, and
            # float(<list>) raised TypeError -- which the ValueError handler
            # below does not catch, so the whole tool CRASHED before printing
            # its CORPUS_SANITY verdict line. Comment lines are not data.
            data_lines = [ln for ln in fh if not ln.startswith("#")]
        rows = list(csv.DictReader(data_lines, delimiter="\t"))
        if not rows:
            continue
        ragged = sum(1 for r in rows if r.get(None))
        if ragged:
            # Rows wider than the header: a decoder/ingest defect, alarm and
            # skip the file -- per-column stats over misaligned rows lie.
            print(f"*** RAGGED ROWS ***  {f.name}: {ragged} row(s) have more "
                  f"fields than the header -- columns misaligned, file skipped")
            bad += 1
            continue
        for col in rows[0]:
            vals = [r[col] for r in rows if r.get(col) not in (None, "")]
            if not vals:
                continue
            try:
                nums = [float(v) for v in vals]
            except ValueError:
                # TRAP 7 (s24). This tool was built from traps 5 and 6, which
                # were both NUMERIC all-zero columns, so a non-numeric column
                # fell straight through this `continue` and was never checked.
                # `oppver` is the literal string "None" in every row of
                # join.tsv (1,355) and ladder_games.tsv (2,625) -- the filter
                # above only drops None and "", so "None" passes it, and then
                # float("None") lands here and the column is silently skipped.
                # A string column with exactly one null-ish value is as dead as
                # an all-zero numeric one and needs the same alarm.
                distinct = set(vals)
                if distinct <= {"None", "none", "NULL", "null", "-", "nan", "NaN"}:
                    key = (f.name, col)
                    note = KNOWN_DEAD.get(key)
                    tag = "KNOWN-DEAD" if note else "*** UNDOCUMENTED DEAD COLUMN ***"
                    print(f"{tag}  {f.name}:{col}  ({len(vals)} rows, all "
                          f"{sorted(distinct)[0]!r} -- non-numeric, so the "
                          f"all-zero check never saw it)")
                    if note:
                        print(f"            cause: {note}")
                    else:
                        bad += 1
                continue
            if any(n != 0 for n in nums):
                continue
            key = (f.name, col)
            note = KNOWN_DEAD.get(key)
            tag = "KNOWN-DEAD" if note else "*** UNDOCUMENTED DEAD COLUMN ***"
            print(f"{tag}  {f.name}:{col}  ({len(nums)} rows, all zero)")
            if note:
                print(f"            cause: {note}")
            else:
                bad += 1
    bad += conditionally_dead(Path(d))
    bad += trap9_duplicate_keys(Path(d))
    stale = freshness(Path(d))
    bad += stale
    # `fcode maps sync` BEFORE the pool check (research triage @7a90eb8): the
    # standing fix for B1 — the fixture refreshes itself instead of waiting
    # for Magnus to hear about a rotation. Network failure = BLIND note, never
    # a false pass, and never a fail (boot must survive offline).
    import subprocess as _sp
    root_ = Path(__file__).resolve().parent.parent
    try:
        r = _sp.run([str(root_ / ".venv/bin/fcode"), "maps", "sync"],
                    capture_output=True, text=True, timeout=60)
        lines = [ln for ln in (r.stdout + r.stderr).strip().splitlines()
                 if ln.strip() and "Update available" not in ln]
        print(f"\nMAPS SYNC: {lines[-1] if lines else 'ran, no output beyond the update banner'}")
    except Exception as e:
        print(f"\nMAPS SYNC: BLIND ({e}) — pool check runs on the local copy")
    bad += pool_check()
    # CLI capability triage (research @7a90eb8): an untriaged flag is an
    # alarm, not archaeology. Report-only here; its own selftest gates it.
    try:
        r = _sp.run([str(root_ / ".venv/bin/python"),
                     str(root_ / "tools/cli_capabilities.py")],
                    capture_output=True, text=True, timeout=120)
        tail = (r.stdout.strip().splitlines() or ["no output"])[-1]
        print(f"CLI-CAP: {tail}")
        if r.returncode != 0:
            bad += 1
    except Exception as e:
        print(f"CLI-CAP: BLIND ({e})")
    print("\nno undocumented dead columns" if not bad else
          f"\n{bad} UNDOCUMENTED all-zero column(s) or STALE file(s): decoder "
          f"bug, or a real fact? Do not quote them until you know which.")
    # ⛔ A ONE-LINE VERDICT TOKEN AT THE VERY BOTTOM, s30 2026-08-11, AND THE
    # REASON IS THIS TOOL'S OWN FIFTY-HOUR MISS.
    # `league_games.tsv` froze on 08-09 and this file DETECTED IT CORRECTLY and
    # exited 1 for fifty hours. It is in the builder boot sequence and it WAS
    # run at boot on 08-11 -- the builder read past the STALE line in the middle
    # of a long report and never checked `$?`. **The alarm was not broken, it
    # was UNREAD**, which is the inverse of every other instrument defect found
    # that day and is not fixed by making the alarm louder in the middle.
    # So it ends with a single gate line, the same convention as PLANK_STATUS
    # and the *_SELFTEST tokens: **GATE ON THIS LINE, NEVER ON `$?`** -- the
    # natural way anyone runs a long report is `corpus_sanity.py | tail`, which
    # makes `$?` the status of `tail` and therefore always 0.
    print(f"\nCORPUS_SANITY: {'OK' if not bad else 'CHECK'}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
