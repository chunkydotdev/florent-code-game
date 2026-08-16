#!/usr/bin/env python3
"""Economy / ammo / CPU census — PATCHED (scratchpad candidate for tools/corpus/replay_econ.py).

WHAT WAS ACTUALLY WRONG (diagnosed 2026-08-14, builder-arm decoder audit)
========================================================================
The reported symptom was "econ.tsv is silently corrupt for ~5,455 recently
decoded replays: turns_run=0, cpu_sum_us=0, ti_collected_end wrong, cpu_max
understated, tled fiction". **NONE of that is a wire-format problem and there is
no engine-era branch anywhere in this decoder.** Two independent defects:

DEFECT 1 — COLUMN DRIFT ON APPEND (the whole reported symptom set).
  Commit d62753c (s36, 2026-08-13 18:34 +0200) widened `COLS` from 17 to 19 by
  inserting `shots_gunner`, `shots_sentinel` at index 6/7. `corpus/econ.tsv` was
  NOT rebuilt. `tools/corpus/sync.py:append_stripping_header()` strips the fresh
  header and appends the body verbatim, so every file decoded after that commit
  landed as a 19-field row under a 17-field header. Measured: 195,021 rows are
  17-field, 31,986 rows are 19-field (5,850 distinct files). Under the stale
  header every column from index 6 onward reads two places to the left:

      header col        actually holds       consequence
      heals          <- shots_gunner
      builds         <- shots_sentinel
      attacks        <- heals
      deliveries     <- builds
      tled           <- attacks
      turns_run      <- deliveries           deliveries is a KNOWN-DEAD column,
                                             always 0  ->  turns_run == 0
      cpu_sum_us     <- tled                 usually 0 ->  cpu_sum_us == 0
      cpu_max_us     <- turns_run            "understated" by ~1e3x
      ti_end         <- cpu_sum_us
      ammo_end       <- cpu_max_us
      ti_collected_end <- ti_end             "corpus says 10, truth 240"
      (fields 18,19 fall off the end of DictReader into restkey None)

  That arithmetic reproduces every reported symptom exactly, including the
  otherwise-unexplained 30,085-vs-31,986 gap: the ~1,901 rows where
  cpu_sum_us != 0 are precisely the rows whose REAL tled count is nonzero.

DEFECT 2 — THE CORE'S TURNS WERE NEVER COUNTED, IN EITHER ERA.
  `team_of` was built only from placeEntity (Update field 1). **Cores are never
  emitted as placeEntity** — they exist only in `Map.cores` (field 4 of the map
  message); `tools/replay_census.py:312` has said so since it was written. So
  every core botOutput was dropped by `if t is None: continue`, silently, in
  100% of rows ever written. Measured on 6 files: unresolved botOutput events =
  492/3326, 1248/12936, 806/7645, 326/2764, 284/2151, 314/2124 — and 100.0% of
  them carry a core id from Map.cores (exactly `rounds` events per team, i.e.
  one core turn per round). `turns_run` and `cpu_sum_us` have therefore
  undercounted by 9-15% in EVERY row of econ.tsv, at every era. Fixed by seeding
  team_of/pos_team/id_pos from Map.cores before replaying turn 0 (2x2 footprint,
  NW corner, same convention as replay_census.core_footprint).

`tled` IS NOT FICTION — MEASURED, BOTH DIRECTIONS.
  botOutput.tled is Update-9 field 4, a proto3 bool, therefore OMITTED when
  false. It is present and true in both eras:
      40 files decoded pre-drift : 301,517 botOutput,  2,066 tled, 7/40 files
      40 files decoded post-drift: 334,903 botOutput, 41,705 tled, 12/40 files
  The "0 occurrences" reading came from the drifted column (which holds
  `attacks`) plus the fact that OUR bot does not TLE (~12% of budget) — the
  flag fires on opponents. The column stays a real integer count; no sentinel is
  emitted, because the quantity is measurable. A sentinel here would have
  destroyed a working signal.

WHAT ELSE CHANGED
  * `id_pos` is now kept current on moveBuilderBot (Update 2). Previously a
    builder bot that moved left a stale id->pos entry, so its removeEntity
    popped `pos_team` at a tile it no longer occupied — which can un-attribute a
    turret standing there. Only affects `shots*`, which exist only in
    post-drift rows (all of which need re-decoding anyway).
  * `SCHEMA_VERSION` + `--check-header <table.tsv>`: refuses to run when the
    destination table's header does not match the header this build emits. That
    is the class fix for DEFECT 1 — a widened COLS can no longer be appended
    into a narrower table silently.
  * `--no-core-seed` reproduces the pre-patch (core-dropping) attribution
    byte-for-byte, so an old row can be re-derived on demand for auditing.

WHAT IS STILL DELIBERATELY DEAD
  `deliveries` is still always 0 (`corpus_sanity.py:97` documents it). Filling
  it is now cheap since Map.cores is parsed, but it is out of scope for this
  fix and changing it would move a column nobody asked about.

ORIGINAL DOCSTRING (streams and why they were read):
  coreConvertAmmo (14)  exact titanium->ammo conversions, per team per round.
  updatePlayers   (6)   per-round titanium / titaniumCollected / ammo, BOTH teams.
  botOutput       (9)   execTimeUs and the `tled` flag, per unit per round.
  builderHeal(15)/builderBuild(16)/builderAttack(13)  builder action mix.
  fireTurret      (12)  shots, attributed by POSITION (the message carries only
                        {from,to} — no id, no team).
Emits one row per file x team x round-band.
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

import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import guard_out, fields, WIRE_LEN, WIRE_VARINT  # noqa: E402


def band(r):
    return "r0-150" if r < 150 else "r150-200" if r < 200 else "r200-300" if r < 300 else "r300+"


BANDS = ("r0-150", "r150-200", "r200-300", "r300+")
COLS = ["file", "team", "band", "ammo_converted", "n_convert", "shots",
        "shots_gunner", "shots_sentinel",
        "heals", "builds", "attacks", "deliveries", "tled", "turns_run",
        "cpu_sum_us", "cpu_max_us", "ti_end", "ammo_end", "ti_collected_end"]

# Bump this whenever COLS changes. --check-header compares the emitted header
# against a destination table so the s36 drift cannot recur silently.
SCHEMA_VERSION = 2
HEADER = "\t".join(COLS)


def _parse_cores(map_buf: bytes):
    """[(core_id, team, (x, y))] from Map.cores (field 4). Cores are NEVER
    emitted as placeEntity — see tools/replay_census.py:312."""
    cores = []
    for num, wire, value in fields(map_buf):
        if num != 4 or wire != WIRE_LEN:
            continue
        cid = team = 0
        pos = (0, 0)
        for cnum, cwire, cval in fields(value):
            if cnum == 1 and cwire == WIRE_VARINT:
                cid = cval
            elif cnum == 2 and cwire == WIRE_VARINT:
                team = cval
            elif cnum == 3 and cwire == WIRE_LEN:
                pd = {k: v for k, w2, v in fields(cval) if w2 == WIRE_VARINT}
                pos = (pd.get(1, 0), pd.get(2, 0))
        cores.append((cid, team, pos))
    return cores


def census(path: Path, out, core_seed: bool = True):
    data = path.read_bytes()
    map_buf = None
    turn_bufs = []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if not turn_bufs:
        return
    # entity -> team, so botOutput/heal/build rows can be attributed
    team_of: dict[int, int] = {}
    # ⭐ s36: FireTurret carries only {from, to} POSITIONS (schema line 94) — no
    # id, no team — which is why `shots` was a dead column (0 non-zero in
    # 195,020 rows; corpus_sanity.py:90 has documented it since s25). Attribute
    # by POSITION: turrets are buildings and do not move, so a pos->team map
    # built from placeEntity resolves the shooter exactly.
    pos_team: dict[tuple[int, int], int] = {}
    pos_kind: dict[tuple[int, int], int] = {}
    id_pos: dict[int, tuple[int, int]] = {}
    TURRET_FIELDS = {21: "gunner", 22: "sentinel"}

    # ⛔ DEFECT 2 (2026-08-14): the core is not in the placeEntity stream, so
    # every core turn was dropped from turns_run/cpu_sum_us/cpu_max_us in every
    # row econ.tsv has ever held. Seed it from Map.cores. Footprint is 2x2 with
    # the stored position as the NW corner (replay_census.core_footprint).
    if core_seed and map_buf is not None:
        for cid, cteam, (cx, cy) in _parse_cores(map_buf):
            team_of.setdefault(cid, cteam)
            id_pos[cid] = (cx, cy)
            for fx, fy in ((cx, cy), (cx + 1, cy), (cx, cy + 1), (cx + 1, cy + 1)):
                pos_team[(fx, fy)] = cteam

    acc: dict[tuple[int, str], dict] = {}

    def cell(t, b):
        k = (t, b)
        if k not in acc:
            acc[k] = dict.fromkeys(
                ("ammo_converted", "n_convert", "shots", "shots_gunner",
                 "shots_sentinel", "heals", "builds",
                 "attacks", "deliveries", "tled", "turns_run", "cpu_sum_us",
                 "cpu_max_us", "ti_end", "ammo_end", "ti_collected_end"), 0)
        return acc[k]

    for rnd, turn_buf in enumerate(turn_bufs):
        b = band(rnd)
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        d, sub = {}, {}
                        for k, w2, v in fields(ebuf):
                            if w2 == WIRE_VARINT:
                                d[k] = v
                            elif w2 == WIRE_LEN:
                                sub[k] = v
                        if 1 in d:
                            team_of.setdefault(d[1], d.get(2, 0))
                        if 3 in sub:                            # Entity.position
                            pd = {k: v for k, w2, v in fields(sub[3])
                                  if w2 == WIRE_VARINT}
                            xy = (pd.get(1, 0), pd.get(2, 0))
                            pos_team[xy] = d.get(2, 0)
                            for fn in TURRET_FIELDS:
                                if fn in sub:
                                    pos_kind[xy] = fn
                            if 1 in d:
                                id_pos[d[1]] = xy
                elif unum == 2:                                 # moveBuilderBot
                    # Keep id_pos current: a stale entry makes removeEntity pop
                    # pos_team at a tile the bot has left, which can strip the
                    # team off a turret standing there.
                    eid = None
                    to = None
                    for mnum, mwire, mval in fields(ubuf):
                        if mnum == 1 and mwire == WIRE_VARINT:
                            eid = mval
                        elif mnum == 2 and mwire == WIRE_LEN:
                            pd = {k: v for k, w2, v in fields(mval)
                                  if w2 == WIRE_VARINT}
                            to = (pd.get(1, 0), pd.get(2, 0))
                    if eid is not None and to is not None:
                        old = id_pos.get(eid)
                        if old is not None and pos_team.get(old) == team_of.get(eid):
                            pos_team.pop(old, None)
                        id_pos[eid] = to
                        pos_team[to] = team_of.get(eid, pos_team.get(to, 0))
                elif unum == 3:                                 # removeEntity
                    d = {k: v for k, w2, v in fields(ubuf) if w2 == WIRE_VARINT}
                    xy = id_pos.pop(d.get(1), None)
                    if xy is not None:
                        pos_team.pop(xy, None)
                        pos_kind.pop(xy, None)
                elif unum == 14:                                # coreConvertAmmo
                    d = {}
                    for k, w2, v in fields(ubuf):
                        if w2 == WIRE_VARINT:
                            d[k] = v
                    c = cell(d.get(1, 0), b)
                    c["ammo_converted"] += d.get(2, 0)
                    c["n_convert"] += 1
                elif unum == 9:                                 # botOutput
                    d = {}
                    for k, w2, v in fields(ubuf):
                        if w2 == WIRE_VARINT:
                            d[k] = v
                    t = team_of.get(d.get(1))
                    if t is None:
                        continue
                    c = cell(t, b)
                    c["turns_run"] += 1
                    us = d.get(3, 0)
                    c["cpu_sum_us"] += us
                    if us > c["cpu_max_us"]:
                        c["cpu_max_us"] = us
                    if d.get(4):                                # tled (proto3:
                        c["tled"] += 1                          # absent == false)
                elif unum in (15, 16, 13):                      # heal / build / attack
                    d = {}
                    for k, w2, v in fields(ubuf):
                        if w2 == WIRE_VARINT:
                            d[k] = v
                    t = team_of.get(d.get(1))
                    if t is None:
                        continue
                    c = cell(t, b)
                    c["heals" if unum == 15 else "builds" if unum == 16 else "attacks"] += 1
                elif unum == 12:                                # fireTurret
                    pd = None
                    for fn, fw, fv in fields(ubuf):
                        if fn == 1 and fw == WIRE_LEN:          # Pos from
                            pd = {k: v for k, w2, v in fields(fv)
                                  if w2 == WIRE_VARINT}
                            break
                    if pd is not None:
                        xy = (pd.get(1, 0), pd.get(2, 0))
                        t = pos_team.get(xy)
                        if t is not None:
                            cc = cell(t, b)
                            cc["shots"] += 1
                            k = pos_kind.get(xy)
                            if k == 21:
                                cc["shots_gunner"] += 1
                            elif k == 22:
                                cc["shots_sentinel"] += 1
                elif unum == 4:                                 # distributeResources
                    for _mn, _mw, _mv in fields(ubuf):          # `deliveries` is
                        pass                                    # known-dead: see
                                                                # corpus_sanity.py:97
                elif unum == 6:                                 # updatePlayers
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn not in (1, 2):
                                continue
                            d = {}
                            for k, w2, v in fields(tv):
                                if w2 == WIRE_VARINT:
                                    d[k] = v
                            c = cell(tn - 1, b)
                            c["ti_end"] = d.get(1, 0)
                            c["ammo_end"] = d.get(7, 0)
                            c["ti_collected_end"] = d.get(4, 0)
    for (t, b), c in acc.items():
        out.write(f"{path.name}\t{t}\t{b}\t" +
                  "\t".join(str(c[k]) for k in COLS[3:]) + "\n")


def check_header(table: Path) -> None:
    """⛔ THE CLASS FIX FOR THE s36 DRIFT.

    An appended body under a stale header is invisible: every row still parses,
    every column still holds an integer, and the reader gets a DIFFERENT column
    than the one it named. Refuse rather than append into a table this build's
    header does not match."""
    if not table.exists():
        return
    with table.open() as fh:
        first = fh.readline().rstrip("\n")
    if first != HEADER:
        raise SystemExit(
            f"REFUSING: {table} header does not match this decoder's schema "
            f"v{SCHEMA_VERSION}.\n"
            f"  table : {len(first.split(chr(9)))} cols  {first}\n"
            f"  decoder: {len(COLS)} cols  {HEADER}\n"
            f"  Appending would silently shift every column past the first "
            f"difference (this is exactly the 2026-08-13 s36 defect: 31,986 "
            f"19-field rows written under a 17-field header). Rebuild the table "
            f"with this decoder instead of appending to it.")


def main(argv):
    core_seed = True
    table = None
    rest = []
    it = iter(argv)
    for a in it:
        if a == "--no-core-seed":
            core_seed = False
        elif a == "--check-header":
            table = Path(next(it))
        else:
            rest.append(a)
    if table is not None:
        check_header(table)
    if not rest:
        raise SystemExit("usage: replay_econ.py OUT.tsv <replays...> "
                         "[--no-core-seed] [--check-header TABLE.tsv]")
    guard_out(rest[0])
    out = open(rest[0], "w")
    out.write(HEADER + "\n")
    bad = 0
    for i, p in enumerate(Path(x) for x in rest[1:]):
        try:
            census(p, out, core_seed=core_seed)
        except Exception as exc:                                # noqa: BLE001
            bad += 1
            print(f"ERR {p.name}: {exc}", file=sys.stderr)
        if (i + 1) % 500 == 0:
            print(f"  ...{i+1}/{len(rest)-1} ({bad} err)", file=sys.stderr, flush=True)
    out.close()
    print(f"done {len(rest)-1} files, {bad} errors", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
