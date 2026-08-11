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


def main(d="corpus"):
    bad = 0
    for f in sorted(Path(d).glob("*.tsv")):
        with open(f) as fh:
            rows = list(csv.DictReader(fh, delimiter="\t"))
        if not rows:
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
    bad += freshness(Path(d))
    print("\nno undocumented dead columns" if not bad else
          f"\n{bad} UNDOCUMENTED all-zero column(s): decoder bug, or a real fact? "
          f"Do not quote them until you know which.")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
