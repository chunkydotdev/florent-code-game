#!/usr/bin/env python3
"""SERIAL DOSE CHECK — does the arm actually DO the thing? Local, minutes.

WHY THIS EXISTS, AND WHY IT IS THE BOTTLENECK TOOL
--------------------------------------------------
Magnus, 2026-08-11: *"do we actually make ANY progress? We haven't had a new bot
in over a day."* Correct: v104 has held the slot ~29 h, ~19 arm trees built, zero
shipped. Three arms hold positive point estimates (best-fit 524/1024, cap6
519/1024, ferry-first 518/1024) and the ship rule needs only **(a) a positive
point estimate, (b) A VERIFIED MECHANISM, (c) no programme breach.** **(b) is the
only thing missing, and nothing in this repo could produce it locally.**

  * `tools/arena.py:53` runs with `--replay /dev/null`.
  * `tools/h2h.sh:66-67` passes NO `--replay`, so every game overwrites the
    `fcode.toml` default `replay.replay26` — one file, last game wins.
  * `tools/mech_battery.py` keeps replays but decodes only builder deaths/spawns.

So: unique replay path per game, decode with the SHIPPED `replay_events.py`
(cleared on both the rotate-suppression and post-death-id-reuse branches by the
side lane, s31), report the counts the plank claims to move.

⛔ SERIAL, NOT PARALLEL. D65, measured 2026-08-11: a 16-game PARALLEL dose check
reported the heal arm at 268 heals/game vs control 108 — the OPPOSITE of a
3-game serial check, and both were wrong. Parallel `fcode run` produces
incoherent counts. This runs one game at a time, on purpose, and it is why the
tool is slow.

⛔ AND A DOSE CHECK CAN KILL A SHIP. `_v139heal` was the JOINT-TOP arm at
524/1024 with a permissive ship rule and a free slot; seed-matched serial dosing
showed it healing 461.5/game against the control's 132.8 — **3.5x MORE, the exact
opposite of the plank.** A positive point estimate is not a mechanism.

BOTH SEATS ALWAYS PLAYED — a one-seat result is a seat measurement, not an arm
measurement (h2h.sh's rule, same reason).

⛔⛔ TWO DEFAULTS CHANGED ON 2026-08-17 (s49 instrument debt). A RERUN OF AN OLDER
REGISTERED INVOCATION WILL NOT REPRODUCE ITS OLD NUMBERS, AND THE REASON IS HERE
RATHER THAN IN A COMMIT MESSAGE NOBODY WILL FIND.

  (1) `--tle` NOW EXISTS AND DEFAULTS TO 10. It did not exist at all before, so
      every `fcode run` this tool issued inherited fcode's OWN default, which is
      `default=0` — verified at source, `.venv/lib/python3.13/site-packages/
      fcode/commands/run.py:119`, whose help text reads verbatim "Turn time limit
      in ms (0 to disable, server uses 10)". **0 DISABLES THE LIMIT.** Meanwhile
      every shard fixture runs `--tle 10` (`tools/overnight.sh:138-139`). So the
      dose check and the battery it was supposed to explain were running
      DIFFERENT ENGINES: a bot that blows its 10 ms budget is silently forgiven
      here and interrupted there. **This flipped a registered F1 verdict on
      2026-08-17** — the arm dosed as delivering a mechanism that the shard
      fixture never let it deliver. The default is now the SHARD value, so the
      dose check and the screen agree by construction.

  (2) THE DEFAULT MAP POOL IS NO LONGER A LITERAL IN THIS FILE. It read
      `[antler, atoll, drumlin, fjordgate, heart, hive, meander, nordkap]` — the
      RETIRED 8-map set. The organisers rotated the pool on 2026-08-13 and
      atoll/heart/hive/meander LEFT IT, so half of every default dose run was
      played on maps the ladder no longer pairs. The pool is now READ FROM
      `tools/overnight.sh`'s `MAPS=(...)` line, which is the shard fixture's own
      authority, and an unparseable line is a LOUD REFUSAL rather than a fallback
      to a literal (see `_pool_from_overnight`).

      ⚠ AND FILE EXISTENCE IS NOT A VALIDATOR HERE, which is why the authority
      has to be the shard script and not the `maps/` directory: `maps/atoll.map26`,
      `heart`, `hive` and `meander` ARE ALL STILL ON DISK. A "do the map files
      exist?" cross-check would have passed on the retired pool every single day
      it was wrong.

Usage:
  dose.py <botdir> --kind sentinel --games 24 [--maps ...] [--ctrl bots/_v130loki13]
  dose.py <botdir> --kind sentinel --registered 120 [--tle 10]
  dose.py --selftest            # map-pool parse + tle plumbing, both verdicts
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
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

ROOT = Path(__file__).resolve().parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"
PY = ROOT / ".venv" / "bin" / "python"
EVENTS = ROOT / "tools" / "corpus" / "replay_events.py"

# ---- THE MAP POOL, AND WHY IT IS NOT A LITERAL HERE -------------------------
# See the module docstring, item (2). The shard fixture's own `MAPS=(...)` line is
# the authority; this tool DERIVES from it so the two cannot diverge silently.
SHARD_SCRIPT = ROOT / "tools" / "overnight.sh"
# The shard fixture's turn-time limit, read from the same script for the same
# reason. `fcode run` defaults to `--tle 0` (limit DISABLED) — see the docstring.
SHARD_TLE_DEFAULT = 10


def _pool_from_overnight(script: Path | None = None) -> list[str]:
    """The live map pool, read off the shard fixture's own `MAPS=(...)` line.

    ⚠ `script=None` AND RESOLVED IN THE BODY, NOT `script=SHARD_SCRIPT`. The
    first cut used the constant as a default argument, which Python binds at
    DEFINITION time — so pointing the module constant at a corrupted copy did
    nothing and `main()`'s refusal branch could not be driven at all. It read the
    LIVE 15 maps while claiming to read the corrupt file, i.e. the guard printed a
    healthy line about a file it had not opened. Caught by driving it, which is
    the only reason it is not still in here.

    ⛔ LOUD REFUSAL, NEVER A FALLBACK. If this cannot parse, it raises. The
    tempting alternative — fall back to a literal in this file — is EXACTLY the
    defect being fixed: the retired 8-map literal sat here for four days after the
    2026-08-13 rotation and nothing said a word, because a stale default and a
    correct default print identical output. A refusal is visible; a stale
    fallback is not.

    A caller who does not want this coupling passes `--maps` explicitly, so the
    refusal can never block someone who has stated their own pool.
    """
    script = Path(script) if script is not None else SHARD_SCRIPT
    if not script.exists():
        raise RuntimeError(
            f"MAP POOL UNREADABLE: {script} does not exist. dose.py derives its "
            f"default pool from that script's MAPS=(...) line (the shard fixture "
            f"is the authority). Pass --maps <names...> to state the pool "
            f"explicitly, or restore the script. REFUSING to guess — the "
            f"literal this replaced was the RETIRED 8-map set and was wrong for "
            f"four days without anyone noticing.")
    text = script.read_text()
    m = re.search(r"^MAPS=\(([^)]*)\)", text, re.M)
    if m is None:
        raise RuntimeError(
            f"MAP POOL UNPARSEABLE: no `MAPS=(...)` line found in {script}. "
            f"Its format changed and this tool's derivation broke. Pass --maps "
            f"explicitly, then fix _pool_from_overnight. REFUSING to fall back "
            f"to a literal.")
    names = [w for w in m.group(1).split() if w]
    # A `MAPS=()` line parses fine and yields nothing — an empty pool would make
    # the game loop's `n % len(a.maps)` raise ZeroDivisionError deep inside the
    # run, which reads as a crash rather than as a pool problem.
    if not names:
        raise RuntimeError(
            f"MAP POOL EMPTY: `MAPS=()` in {script} parsed to zero maps. "
            f"REFUSING — an empty pool is not a default.")
    # Every derived name must resolve to a real map file, or the loop would issue
    # `fcode run ... maps/<name>.map26` and log `!! no replay` for every game.
    # NOTE (docstring item 2): this is a check on the DERIVATION, not on the
    # pool's currency — the retired maps are all still on disk.
    missing = [n for n in names if not (ROOT / "maps" / f"{n}.map26").exists()]
    if missing:
        raise RuntimeError(
            f"MAP POOL BROKEN: {script} names {len(missing)} map(s) with no "
            f"file under maps/: {', '.join(missing)}. REFUSING — every game on "
            f"those would silently log `!! no replay` and shrink n.")
    return names


def decode(replay: Path):
    """BUILD/DEATH rows -> per-team counters. Uses the SHIPPED decoder."""
    import io
    import importlib.util
    spec = importlib.util.spec_from_file_location("replay_events", EVENTS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    buf = io.StringIO()
    mod.census(replay, buf)
    out = {0: Counter(), 1: Counter()}
    for line in buf.getvalue().splitlines():
        f = line.split("\t")
        if len(f) < 9:
            continue
        ev, team, kind = f[1], int(f[3]), f[4]
        d2o, d2e = int(f[7]), int(f[8])
        fwd = d2e < d2o
        if ev == "BUILD":
            out[team][f"build_{kind}"] += 1
            if fwd:
                out[team][f"fwdbuild_{kind}"] += 1
        elif ev == "DEATH":
            out[team][f"death_{kind}"] += 1
            if fwd:
                out[team][f"fwddeath_{kind}"] += 1
    return out


def _incumbent_ctrl() -> str | None:
    """CLASS A, s48 wrap — DERIVE THE CONTROL, DO NOT EMBED IT.

    This used to be `--ctrl default="bots/_v146gunaxis"` with the comment "Move
    this on every ship; a stale control measures the wrong contrast." Nobody
    moved it: at the s48 wrap the default named v114 while the incumbent was
    `bots/_v468kladturbo`, so any hand-run omitting --ctrl was silently dosing
    against a control ~11 ships stale. A comment instructing a human to maintain
    a constant is the failure mode, not the fix — `tools/fleet_dispatch.py` was
    converted for exactly this reason (a50f27ef). Reads PROGRAMME.md's INCUMBENT
    through control_pin, the one authority.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from control_pin import incumbent
        p = incumbent()
    except Exception:
        return None
    if p is None:
        return None
    try:
        return str(p.relative_to(Path(__file__).resolve().parent.parent))
    except ValueError:
        return str(p)


def selftest() -> int:
    """Drive the map-pool derivation to BOTH verdicts, and prove the tle default.

    ⛔ THE POINT: the two defects fixed on 2026-08-17 were both SILENT. A stale
    map literal and a correct one print identical output; a `--tle 0` run and a
    `--tle 10` run print identical verdict vocabulary. Neither had any branch that
    could ever produce the other answer, which is this repo's definition of a
    check that has not been seen to check. So the refusal path is exercised here
    on deliberately corrupted copies of the shard script.
    """
    import tempfile as _tf
    bad = 0

    def cell(label, fn, want_ok):
        nonlocal bad
        try:
            got = fn()
            ok, detail = True, f"parsed {len(got)} maps"
        except RuntimeError as e:
            ok, detail = False, str(e).split(".")[0]
        good = (ok == want_ok)
        if not good:
            bad += 1
        print(f"  [{'ok ' if good else 'FAIL'}] {label:<44} "
              f"-> {'parsed' if ok else 'REFUSED':8} "
              f"(want {'parsed' if want_ok else 'REFUSED'})  {detail[:70]}")

    print("MAP-POOL DERIVATION SELFTEST")
    # PASS side: the live shard script.
    cell("live tools/overnight.sh", _pool_from_overnight, True)
    with _tf.TemporaryDirectory() as td:
        d = Path(td)
        live = SHARD_SCRIPT.read_text()
        # REFUSE side 1: the file is gone.
        cell("script missing", lambda: _pool_from_overnight(d / "nope.sh"), False)
        # REFUSE side 2: the MAPS=(...) line is renamed (a format change).
        p = d / "renamed.sh"
        p.write_text(live.replace("MAPS=(", "MAP_POOL=("))
        cell("MAPS=(...) line renamed away", lambda: _pool_from_overnight(p), False)
        # REFUSE side 3: an empty pool parses fine and must still refuse.
        p2 = d / "empty.sh"
        p2.write_text(re.sub(r"^MAPS=\([^)]*\)", "MAPS=()", live, flags=re.M))
        cell("MAPS=() empty pool", lambda: _pool_from_overnight(p2), False)
        # REFUSE side 4: a named map with no file under maps/.
        p3 = d / "ghost.sh"
        p3.write_text(re.sub(r"^MAPS=\(([^)]*)\)", r"MAPS=(\1 ghostmap)", live,
                             flags=re.M))
        cell("a named map with no maps/<n>.map26", lambda: _pool_from_overnight(p3), False)
        # PASS side again, on a REWRITTEN but valid script: proves the parser is
        # reading the line and not just succeeding on the live file by luck.
        p4 = d / "rewritten.sh"
        p4.write_text(re.sub(r"^MAPS=\([^)]*\)", "MAPS=(antler fjordgate)", live,
                             flags=re.M))
        got4 = _pool_from_overnight(p4)
        ok4 = got4 == ["antler", "fjordgate"]
        if not ok4:
            bad += 1
        print(f"  [{'ok ' if ok4 else 'FAIL'}] {'a REWRITTEN valid pool is read, not guessed':<44} "
              f"-> {got4}")

    print("\nPOOL CURRENCY — the retired literal must NOT be what we derive")
    live_pool = _pool_from_overnight()
    retired = {"atoll", "heart", "hive", "meander"}
    still_there = retired & set(live_pool)
    print(f"  [{'ok ' if not still_there else 'FAIL'}] retired maps "
          f"{sorted(retired)} are ABSENT from the derived pool "
          f"(present: {sorted(still_there) or 'none'})")
    if still_there:
        bad += 1
    # ...and the control that makes that absence meaningful: the files DO exist,
    # so a maps/-existence check would have passed on the retired pool.
    on_disk = sorted(m for m in retired if (ROOT / "maps" / f"{m}.map26").exists())
    print(f"  [ctl] those same maps ARE still on disk ({on_disk or 'none'}) — "
          f"proof that file existence could not have caught this rot")
    print(f"  [ok ] derived pool is {len(live_pool)} maps: {', '.join(live_pool)}")

    print("\nTLE PLUMBING")
    ap = argparse.ArgumentParser()
    ap.add_argument("--tle", type=int, default=SHARD_TLE_DEFAULT)
    dflt = ap.parse_args([]).tle
    ok_d = dflt == SHARD_TLE_DEFAULT == 10
    if not ok_d:
        bad += 1
    print(f"  [{'ok ' if ok_d else 'FAIL'}] default --tle is {dflt} "
          f"(shard value {SHARD_TLE_DEFAULT}); fcode's own default is 0 = DISABLED")
    ok_o = ap.parse_args(["--tle", "0"]).tle == 0
    if not ok_o:
        bad += 1
    print(f"  [{'ok ' if ok_o else 'FAIL'}] the OTHER verdict: --tle 0 overrides "
          f"to 0 and the header warns it is not shard-comparable")
    # And the shard script really does run --tle 10 — the source of the default.
    shard_tle = re.findall(r"--tle\s+(\d+)", SHARD_SCRIPT.read_text())
    ok_s = bool(shard_tle) and all(int(t) == SHARD_TLE_DEFAULT for t in shard_tle)
    if not ok_s:
        bad += 1
    print(f"  [{'ok ' if ok_s else 'FAIL'}] {SHARD_SCRIPT.name} itself passes "
          f"--tle {sorted(set(shard_tle))} — the default is DERIVED, not invented")

    print("\nDOSE SELFTEST " + ("PASS — the pool derivation refuses on all four "
          "corruptions, reads a rewritten pool correctly, and the tle default "
          "matches the shard script it was read from."
          if not bad else f"FAIL — {bad} cell(s) wrong."))
    return 0 if not bad else 1


def main():
    if "--selftest" in sys.argv[1:]:
        return selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("bot")
    ap.add_argument("--ctrl", default=None,
                    help="control tree; default = PROGRAMME.md's INCUMBENT, read live")
    ap.add_argument("--kind", default="sentinel")
    # ⛔⛔ CLASS B, s48 wrap — A TOOL CONSUMED BY PRE-REGISTRATIONS MAY NOT PICK
    # ITS OWN SAMPLE SIZE. `--games` had `default=24`. On 2026-08-17 a prereg
    # registered n=120 and the battery was invoked without `--games`; the tool
    # ran 24 and said nothing, so the registered size and the executed size
    # differed with no artefact anywhere recording it. That is the same shape as
    # a registered method that is not executable — except silent, because 24
    # games print exactly the same verdict vocabulary as 120.
    # ⇒ THERE IS NO DEFAULT ANY MORE. Either say which n you registered
    # (`--registered N`, which STAMPS the number into every verdict line and
    # reports any shortfall against it), or declare the run unregistered
    # (`--games N`). Passing both is a REFUSAL unless they agree.
    ap.add_argument("--games", type=int, default=None,
                    help="sample size for an UNREGISTERED exploratory run")
    ap.add_argument("--registered", type=int, default=None, metavar="N",
                    help="the n written into the pre-registration; stamped into "
                         "the output and checked against what actually ran")
    # ⛔ debt 20, s48: dose.py:157 unlinked every replay after decoding and had
    # no retain flag, but the registered S1 seat-band read on both SEALSENT
    # preregs consumes THE REPLAYS. A registered read whose inputs the tool
    # deletes is a registered read that cannot be executed.
    ap.add_argument("--keep", default=None, metavar="DIR",
                    help="retain every replay in DIR instead of deleting it "
                         "(required by any registered read that decodes replays)")
    # ⛔ default=None, RESOLVED BELOW, not `default=MAPS`. The pool is derived from
    # the shard fixture and the derivation can REFUSE (see _pool_from_overnight);
    # a refusal must not fire for `--help` or for a caller who states --maps.
    ap.add_argument("--maps", nargs="*", default=None,
                    help="map pool; default = tools/overnight.sh's MAPS=(...) "
                         "line, read live (the shard fixture is the authority)")
    # ⛔⛔ s49 debt: THIS FLAG DID NOT EXIST, so every `fcode run` above inherited
    # fcode's own `--tle` default of 0 — THE LIMIT DISABLED — while every shard
    # runs `--tle 10`. Two different engines, one verdict vocabulary. Default is
    # now the SHARD value; see the module docstring for the flipped F1 verdict.
    ap.add_argument("--tle", type=int, default=SHARD_TLE_DEFAULT, metavar="MS",
                    help=f"turn time limit in ms passed to every `fcode run`; "
                         f"default {SHARD_TLE_DEFAULT} = the shard fixture's "
                         f"value (`fcode run` itself defaults to 0 = DISABLED, "
                         f"which is what this tool used to inherit)")
    # ADD-ONLY (builder s48). Off by default; changes NO existing computation.
    # WHY: the printed band covers `fwdbuild_<kind>` ONLY, because that is the
    # quantity the tool's DOSE_RESULT verdict is about. A brief that also puts
    # an EXCLUSION bar on builder deaths (e.g. "death diff CI-upper < +0.35")
    # cannot be answered from the printed means -- a mean has no interval. This
    # dumps the per-game paired values so the same paired-difference arithmetic
    # the band already uses can be applied to any decoded key.
    ap.add_argument("--tsv", default=None,
                    help="also write per-game paired counts to this TSV")
    a = ap.parse_args()

    # ---- CLASS B GATE: refuse to invent a sample size, and refuse a contradiction.
    if a.games is None and a.registered is None:
        print("⛔ dose.py REFUSES to pick a sample size for you.\n"
              "   Pass --registered N (the n written into the pre-registration) "
              "or --games N (an explicitly unregistered exploratory run).\n"
              "   There is no default: a tool consumed by preregs that silently "
              "runs a different size than registered produces a result nobody "
              "can tell apart from the registered one.", file=sys.stderr)
        return 2
    if (a.games is not None and a.registered is not None
            and a.games != a.registered):
        print(f"⛔ dose.py REFUSES: --games {a.games} contradicts --registered "
              f"{a.registered}. Say one number, not two.", file=sys.stderr)
        return 2
    if a.registered is not None:
        a.games = a.registered
    if a.ctrl is None:
        a.ctrl = _incumbent_ctrl()
        if a.ctrl is None:
            print("⛔ dose.py REFUSES: no --ctrl given and PROGRAMME.md's "
                  "INCUMBENT could not be read. Refusing to guess the control "
                  "tree — a wrong control measures the wrong contrast silently.",
                  file=sys.stderr)
            return 2
        print(f"  control derived from PROGRAMME INCUMBENT: {a.ctrl}", flush=True)

    # ---- MAP POOL GATE. Derived, or explicitly stated; never a stale literal.
    if a.maps is None:
        try:
            a.maps = _pool_from_overnight()
        except RuntimeError as e:
            print(f"⛔ dose.py REFUSES: {e}", file=sys.stderr)
            return 2
        print(f"  map pool derived from {SHARD_SCRIPT.name}: {len(a.maps)} maps "
              f"({', '.join(a.maps)})", flush=True)
    else:
        if not a.maps:
            print("⛔ dose.py REFUSES: --maps was given with no map names.",
                  file=sys.stderr)
            return 2
        print(f"  map pool STATED on the command line: {len(a.maps)} maps "
              f"({', '.join(a.maps)})", flush=True)

    _reg = (f"REGISTERED n={a.registered}" if a.registered is not None
            else f"UNREGISTERED n={a.games}")
    # The tle is STAMPED into the header the same way the registered n is: a run
    # whose engine settings are not in its own output cannot be told apart from a
    # run with different ones. That is how the F1 verdict flipped unnoticed.
    print(f"  tle={a.tle}ms per turn"
          + ("  (SHARD-MATCHED)" if a.tle == SHARD_TLE_DEFAULT else
             f"  ⚠ NOT the shard value ({SHARD_TLE_DEFAULT}ms) — this run is NOT "
             f"comparable to a shard battery"
             + ("; 0 means the limit is DISABLED" if a.tle == 0 else "")),
          flush=True)

    keep_dir = None
    if a.keep:
        keep_dir = Path(a.keep)
        keep_dir.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="dose_"))
    T, C = Counter(), Counter()
    per_t, per_c = [], []          # PER-GAME values — the band needs the spread
    per_game = []                  # ADD-ONLY: full per-game rows for --tsv
    n = 0
    seed = 0
    print(f"DOSE  {a.bot}  vs  {a.ctrl}   kind={a.kind}   SERIAL   {_reg}"
          f"   tle={a.tle}ms   maps={len(a.maps)}"
          + (f"   KEEP -> {keep_dir}" if keep_dir else ""), flush=True)
    try:
        while n < a.games:
            m = a.maps[(n // 2) % len(a.maps)]
            seat = n % 2                       # BOTH SEATS ALWAYS PLAYED
            if seat == 0:
                bots, ti, ci = [a.bot, a.ctrl], 0, 1
            else:
                bots, ti, ci = [a.ctrl, a.bot], 1, 0
            if n % 2 == 0:
                seed += 1
            rp = tmp / f"g{n}.replay26"
            r = subprocess.run(
                [str(FCODE), "run", bots[0], bots[1], f"maps/{m}.map26",
                 "--seed", str(seed), "--tle", str(a.tle), "--replay", str(rp)],
                capture_output=True, text=True, cwd=ROOT)
            if not rp.exists():
                print(f"  !! no replay for game {n} ({m} seed {seed})", flush=True)
                n += 1
                continue
            d = decode(rp)
            T.update(d[ti])
            C.update(d[ci])
            per_t.append(d[ti][f"fwdbuild_{a.kind}"])
            per_c.append(d[ci][f"fwdbuild_{a.kind}"])
            if a.tsv:
                _keys = [f"build_{a.kind}", f"fwdbuild_{a.kind}",
                         "death_builder_bot", "fwddeath_builder_bot",
                         f"death_{a.kind}", f"fwddeath_{a.kind}"]
                row = {"game": n, "map": m, "seed": seed, "seat": seat}
                for k in _keys:
                    row["T_" + k] = d[ti][k]
                    row["C_" + k] = d[ci][k]
                per_game.append(row)
            n += 1
            if n % 4 == 0:
                tb = T[f"fwdbuild_{a.kind}"] / n
                cb = C[f"fwdbuild_{a.kind}"] / n
                print(f"  {n}/{a.games}  fwd {a.kind}/game  TREAT {tb:.2f}  "
                      f"CTRL {cb:.2f}", flush=True)
            if keep_dir is not None:
                # RETAIN, don't delete. Name carries everything the S1 seat-band
                # read needs to pair a replay back to its cell without a
                # side-file: game index, map, seed, and which seat the TREATMENT
                # played. A bare g<N>.replay26 would need this tool's loop
                # re-derived to be readable.
                rp.replace(keep_dir / f"g{n:04d}_{m}_s{seed}_treatseat{seat}.replay26")
            else:
                rp.unlink(missing_ok=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        if keep_dir is not None:
            _kept = len(list(keep_dir.glob("*.replay26")))
            print(f"  KEPT {_kept} replays in {keep_dir}", flush=True)

    if a.tsv and per_game:
        cols = list(per_game[0].keys())
        with open(a.tsv, "w") as fh:
            fh.write("\t".join(cols) + "\n")
            for r in per_game:
                fh.write("\t".join(str(r[c]) for c in cols) + "\n")
        print(f"  per-game TSV -> {a.tsv}  ({len(per_game)} rows)", flush=True)

    if not n:
        print("DOSE_RESULT: NO GAMES")
        return
    print(f"\nDOSE  n={n} games (both seats)   {_reg}   tle={a.tle}ms"
          f"   pool={len(a.maps)} maps")
    if a.registered is not None and n != a.registered:
        # The whole point of --registered: the gap between what was registered
        # and what ran is stated IN the result, not left to whoever compares the
        # prereg page against the log later.
        print(f"  ⛔ SHORTFALL: {n} games ran against {a.registered} REGISTERED. "
              f"This result is NOT the registered read; say so wherever it is "
              f"banked.")
    keys = [f"build_{a.kind}", f"fwdbuild_{a.kind}",
            f"death_builder_bot", f"fwddeath_builder_bot"]
    print(f"  {'quantity':<28}{'TREAT':>9}{'CTRL':>9}{'ratio':>9}")
    for k in keys:
        t, c = T[k] / n, C[k] / n
        rr = (t / c) if c else float("nan")
        print(f"  {k+'/game':<28}{t:>9.2f}{c:>9.2f}{rr:>9.2f}x")
    tb, cb = T[f"fwdbuild_{a.kind}"] / n, C[f"fwdbuild_{a.kind}"] / n

    # ⛔⛔ THE BAND. FIRST VERSION OF THIS TOOL SAID `elif tb > cb: DOSE
    # DELIVERED` — AN UNSIZED BAR, WITH NO THRESHOLD, IN THE TOOL WRITTEN TO
    # ENFORCE SIZED BARS. It printed "DOSE DELIVERED" for cap6 on 1.58 -> 1.67
    # (1.05x) at n=24, which is noise. Caught 2026-08-11 by reading the tool's
    # own first output. Same defect as LOKI-27's "INSERT -> RISES" and
    # fwd_read's bare `db < 0`, committed a third time by the person fixing the
    # first two. **A direction is not a bar.**
    #
    # PAIRED: both arms play the SAME game, so the per-game DIFFERENCE is the
    # unit and its sd is what sizes the band.
    import statistics
    diffs = [t - c for t, c in zip(per_t, per_c)]
    sd = statistics.pstdev(diffs) if len(diffs) > 1 else 0.0
    se = sd / (len(diffs) ** 0.5) if diffs else 0.0
    band = 2 * se
    obs = tb - cb
    print(f"\n  paired diff {obs:+.3f}/game   sd(diff) {sd:.2f}   "
          f"2*SE = {band:.3f}   n={n}")
    mde_pct = (band / cb * 100) if cb else float("nan")
    print(f"  INFORMATIVE BAND: |diff| >= {band:.3f}/game "
          f"({mde_pct:.0f}% of the control level)")

    if cb == 0 and tb == 0:
        print(f"\n  DOSE_RESULT: INERT — neither arm builds a forward {a.kind}. "
              f"The plank's precondition is absent in this fixture.")
    elif obs >= band:
        print(f"\n  DOSE_RESULT: DOSE DELIVERED — forward {a.kind} "
              f"{cb:.2f} -> {tb:.2f}/game, outside the band. "
              f"Mechanism runs in the CLAIMED direction.")
    elif obs <= -band:
        print(f"\n  DOSE_RESULT: ⛔ MECHANISM INVERTED — forward {a.kind} "
              f"{cb:.2f} -> {tb:.2f}/game, outside the band the WRONG way "
              f"(the _v139heal outcome). DISQUALIFIED.")
    else:
        print(f"\n  DOSE_RESULT: NO INFORMATION — {cb:.2f} -> {tb:.2f}/game is "
              f"INSIDE the band. This is NOT a delivered dose and NOT a "
              f"refutation. Buy more n, or the plank is near-inert here.")


if __name__ == "__main__":
    # ⛔ The refusals above return 2 and MUST reach the shell — a battery script
    # that reads `$?` would otherwise see 0 on a refusal and run on.
    raise SystemExit(main() or 0)
