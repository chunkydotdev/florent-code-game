#!/usr/bin/env python3
"""FORCED-FAIL PROBE for the s43 WIRING BUNDLE (6 items, one diff).

    .venv/bin/python scratchpad/wiring_bundle_probe.py

⛔ WHY THIS FILE EXISTS AND WHY EVERY CELL COMES IN PAIRS. A guard that has only
ever passed has not been seen to check anything. Two same-day failures in this
repo were "the check ran and asserted nothing", and the whole point of the (a)
correction -- a tape of escapes has a numerator and no denominator -- is that an
instrument exercised on one side only reproduces the bug it was built to catch.
So EVERY guard below is driven to BOTH verdicts, including the inline ones:
the `escapes` column is exercised EMPTY as well as full, the CANNOT-COMPUTE
string is compared against the genuine no-intersection string rather than merely
printed, and the pool-era derivation is run against its own degenerate input.

Exits NONZERO if any cell comes out the wrong way. Gate on `PROBE:` on the last
line as well as on $?.

⚠ It never writes to the real invocation tape (TOOL_INVOCATION_TAPE is
redirected) and never touches scratchpad/overnight/ (OUT is redirected).
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import prereg_check as PC            # THE PRODUCTION MODULES. No re-implementation.
import escape_tape as ET
import overnight_read as OR
import effective_n as EN

PY = str(ROOT / ".venv" / "bin" / "python")
ROWS: list[tuple[str, str, str, bool]] = []      # (item, cell, detail, ok)
TMP = Path(tempfile.mkdtemp(prefix="wiring_probe_"))


def cell(item: str, name: str, ok: bool, detail: str = "") -> None:
    ROWS.append((item, name, detail, bool(ok)))


# ===========================================================================
# FIXTURE TEXT — a complete, passing prereg. Every corruption below mutates it,
# so a FAIL is attributable to the mutation and not to a broken base.
# ===========================================================================
BASE = PC.COMPLETE
DIFF = ["eco.py", "main.py"]


def run(text, diff_paths=DIFF, fire=False):
    rows, fails, warns = PC.run_checks(text, "<probe>", diff_paths=diff_paths,
                                       quiet=True, fire=fire)
    return {x[0] for x in fails}, warns, rows


def alines(text, diff_paths=DIFF, fire=False):
    f = PC.parse_fields(text)
    lines, _fails, _warns = PC.check_arithmetic(f, diff_paths=diff_paths, text=text, fire=fire)
    return lines


# ===========================================================================
# (a) INVOCATION TAPE + FOUR ESCAPES, gate.py
# ===========================================================================
def probe_a():
    item = "(a) escape tape"
    gd = TMP / "gate"
    gd.mkdir()
    # A plank that is OFF the programme line (so check_programme FAILs) and
    # carries NOISE_ON = True (so check_determinism FAILs). Both FAILs keep
    # gate.py out of check_control_equivalence, which would shell out to fcode.
    for name, noise in (("_probeplank", "True"), ("_probectl", "False"),
                        ("_probeparent", "False"), ("_probeopp", "False")):
        d = gd / name
        d.mkdir()
        (d / "main.py").write_text(f"NOISE_ON = {noise}\nclass Player:\n    pass\n")
    tape = TMP / "invocations.tsv"
    args = ["--plank", str(gd / "_probeplank"), "--control", str(gd / "_probectl"),
            "--parent", str(gd / "_probeparent"), "--opponents", str(gd / "_probeopp")]

    def gate(*extra):
        env = dict(os.environ, TOOL_INVOCATION_TAPE=str(tape))
        r = subprocess.run([PY, str(ROOT / "tools" / "gate.py")] + args + list(extra),
                           cwd=ROOT, capture_output=True, text=True, timeout=300, env=env)
        return r.stdout + r.stderr

    def rows():
        if not tape.exists():
            return []
        return [l.split("\t") for l in tape.read_text().splitlines()[1:] if l.strip()]

    # a1 -- THE DENOMINATOR HALF. A run with NO escape must still write a row,
    # and its `escapes` column must be EMPTY. If only escaped runs were taped
    # the bypass RATE would have no denominator -- the exact defect that got
    # this item's first spec retracted.
    gate()
    r = rows()
    cell(item, "a1 no-escape run writes a row, escapes EMPTY",
         len(r) == 1 and r[0][5] == "" and r[0][1] == "gate.py",
         f"{len(r)} row(s), escapes={r[0][5]!r}" if r else "no rows")

    # a2 -- THE NUMERATOR HALF, one cell per escape, all four.
    reasons = {
        "off-programme": "probe leg, deliberately off the active line to exercise the tape",
        "skip-tle": "probe leg, no remote engine available in this sandbox at all",
        "allow-self-play": "probe leg, the pool is our own lineage on purpose here",
        "pooled-not-paired": "pooled within-game win rate, no seed-matched comparison at all",
    }
    for flag, why in reasons.items():
        before = len(rows())
        out = gate(f"--{flag}", why)
        r = rows()
        got = r[-1][5] if len(r) > before else ""
        cell(item, f"a2 --{flag} REASON -> taped as an escape",
             len(r) == before + 1 and got == flag, f"escapes={got!r}")
        cell(item, f"a2 --{flag} reason is on the row",
             len(r) > before and why[:24] in r[-1][7], f"reasons={r[-1][7][:40]!r}")
        del out

    # a3 -- BARE flag (no reason) is REFUSED with a named FAIL, for all four.
    for flag in reasons:
        out = gate(f"--{flag}")
        cell(item, f"a3 bare --{flag} is REFUSED",
             f"--{flag} requires a REASON" in out, out.strip().splitlines()[-1][:40])
    # a3b -- a SHORT reason is refused too (the >=20 bar is not decorative).
    out = gate("--allow-self-play", "because")
    cell(item, "a3b --allow-self-play 'because' (7 chars) refused",
         "requires a REASON of >=20" in out, "")

    # a4 -- A REFUSED ESCAPE DOES NOT SILENCE ITS CHECK. Granted, the NOISE_ON
    # FAIL is downgraded to WARN; refused, it stays a FAIL. Same input, two
    # verdicts, and the escape is the only thing that moved.
    granted = gate("--pooled-not-paired", reasons["pooled-not-paired"])
    refused = gate("--pooled-not-paired")
    g_warn = any(l.startswith("WARN") and "NOISE_ON = True" in l for l in granted.splitlines())
    r_fail = any(l.startswith("FAIL") and "NOISE_ON = True" in l for l in refused.splitlines())
    cell(item, "a4 granted escape downgrades NOISE_ON to WARN", g_warn, "")
    cell(item, "a4 REFUSED escape leaves NOISE_ON a FAIL", r_fail, "")

    # a5 -- THE RATE IS COMPUTABLE, and both halves are non-degenerate.
    env_saved = os.environ.get("TOOL_INVOCATION_TAPE")
    os.environ["TOOL_INVOCATION_TAPE"] = str(tape)
    esc, tot = ET.rate("gate.py")
    if env_saved is None:
        os.environ.pop("TOOL_INVOCATION_TAPE", None)
    else:
        os.environ["TOOL_INVOCATION_TAPE"] = env_saved
    cell(item, "a5 bypass RATE has a denominator (esc < tot, both > 0)",
         0 < esc < tot, f"{esc}/{tot}")

    # a6 -- the battery IDENTITY is on the row and is NOT a constant column.
    subj = rows()[0][8]
    cell(item, "a6 subject names the battery, not an empty prereg path",
         "plank=_probeplank" in subj and "opponents=_probeopp" in subj, subj[:52])

    # a7 -- check_determinism's OWN reason guard. main() now validates before
    # calling it, so this branch is unreachable from the CLI and would otherwise
    # be an un-driven guard. Driven here directly, both ways, rather than left
    # as decoration.
    import gate as G
    G.FAIL.clear(); G.WARN.clear()
    G.check_determinism([gd / "_probectl"], pooled_not_paired="too short")
    short_fails = [f for f in G.FAIL if "requires a REASON" in f]
    G.FAIL.clear(); G.WARN.clear()
    G.check_determinism([gd / "_probectl"], pooled_not_paired=reasons["pooled-not-paired"])
    long_ok = not G.FAIL and any("ESCAPE TAKEN" in w for w in G.WARN)
    G.FAIL.clear(); G.WARN.clear()
    cell(item, "a7 check_determinism refuses a short reason directly",
         len(short_fails) == 1, "")
    cell(item, "a7b ...and accepts a valid one", long_ok, "")


# ===========================================================================
# (b) LOCAL-ACCEPTS WARN
# ===========================================================================
LOCAL = (BASE.replace("**SURFACE: unrated**", "**SURFACE: local**")
             .replace("**CLUSTER UNIT: match — one opponent per arm, so the opponent "
                      "cluster is removed**", "**CLUSTER UNIT: none — local shards**"))


def probe_b():
    item = "(b) local-accepts"
    def has_warn(txt):
        _f, warns, _r = run(txt)
        return any("local but BOUNDARY declares" in w for w in warns)
    # b1 FAIL-side: a local surface that ALSO declares accepts.
    b1 = LOCAL.replace("**BOUNDARY: 30 accepts = 150 games**",
                       "**BOUNDARY: 30 accepts = 150 games**")
    cell(item, "b1 SURFACE local + accepts -> WARN", has_warn(b1), "")
    # b2 PASS-side: the same local prereg with a games-only boundary.
    b2 = LOCAL.replace("**BOUNDARY: 30 accepts = 150 games**", "**BOUNDARY: 150 games**")
    cell(item, "b2 SURFACE local, games only -> no WARN", not has_warn(b2), "")
    # b3 PASS-side: accepts on a PANEL surface is normal and must not WARN here.
    cell(item, "b3 SURFACE unrated + accepts -> no local WARN", not has_warn(BASE), "")
    # b4 the exemption still applies (the local branch is what is being guarded).
    cell(item, "b4 local branch still exempts games=5xaccepts",
         any("LOCAL surface" in l for l in alines(b2)), "")


# ===========================================================================
# (c) CUT-SHORT CONSUMER
# ===========================================================================
def probe_c():
    item = "(c) cut-short"
    hi = BASE.replace("below 75 games", "below 200 games")       # floor > planned n
    eq = BASE.replace("below 75 games", "below 150 games")       # floor == planned n
    lo = BASE                                                    # floor < planned n
    none = BASE.replace("**CUT-SHORT: below 75 games this leg publishes descriptive "
                        "tallies only and takes NO comparative look**",
                        "**CUT-SHORT: descriptive tallies only if the leg is short**")
    f_hi, _w, _r = run(hi)
    f_eq, w_eq, _r = run(eq)
    f_lo, w_lo, _r = run(lo)
    f_no, _w, _r = run(none)
    cell(item, "c1 floor 200 > planned n 150 -> FAIL", "CUT_SHORT_FLOOR" in f_hi, "")
    cell(item, "c2 floor 75 < planned n 150 -> pass", "CUT_SHORT_FLOOR" not in f_lo, "")
    cell(item, "c3 floor == planned n -> pass but WARN",
         "CUT_SHORT_FLOOR" not in f_eq and any("EQUALS PLANNED n" in w for w in w_eq), "")
    cell(item, "c3b floor < planned n emits NO such WARN",
         not any("EQUALS PLANNED n" in w for w in w_lo), "")
    cell(item, "c4 no numeric floor -> 'not computed', never a silent ok",
         "CUT_SHORT_FLOOR" not in f_no
         and any(l.startswith("CUT_SHORT_FLOOR  not computed") for l in alines(none)), "")


# ===========================================================================
# (d) OB13 UNTRACKED ARM + THE CANNOT-COMPUTE STRING
# ===========================================================================
UNTRACKED_ARM = ROOT / "scratchpad" / "_wiring_probe_arm"


def probe_d():
    item = "(d) OB13 untracked"
    UNTRACKED_ARM.mkdir(parents=True, exist_ok=True)
    (UNTRACKED_ARM / "eco.py").write_text("# probe arm, deliberately untracked\n")
    tracked = "bots/_v223sealrepair/eco.py"
    assert (ROOT / tracked).exists(), "probe needs a known-tracked arm file"

    unt = BASE.replace("**PROVENANCE: ", "**TREATMENT TREE: scratchpad/_wiring_probe_arm/eco.py**\n**PROVENANCE: ")
    trk = BASE.replace("**PROVENANCE: ", f"**TREATMENT TREE: {tracked}**\n**PROVENANCE: ")

    # POSITIVE CONTROL on the helper itself: it must return the untracked path
    # and NOT the tracked one. A helper that returned [] for both would make
    # every cell below pass for the wrong reason.
    cell(item, "d0a helper flags the untracked arm",
         "scratchpad/_wiring_probe_arm/eco.py" in PC.untracked_arm_paths(PC.parse_fields(unt)),
         "")
    cell(item, "d0b helper does NOT flag a tracked arm",
         PC.untracked_arm_paths(PC.parse_fields(trk)) == [], "")

    f_unt, _w, _r = run(unt, diff_paths=[])
    f_trk, w_trk, _r = run(trk, diff_paths=[])
    f_fire, _w, _r = run(trk, diff_paths=[], fire=True)
    f_real, _w, _r = run(BASE, diff_paths=["main.py", "doctrine.py"])

    cell(item, "d1 untracked arm + empty diff -> FAIL OB13_UNTRACKED_ARM",
         "OB13_UNTRACKED_ARM" in f_unt, "")
    cell(item, "d2 TRACKED arm + empty diff -> WARN, not FAIL",
         "OB13_UNTRACKED_ARM" not in f_trk and "OB13_NOT_COMPUTED" not in f_trk
         and any("NOT COMPUTED" in w for w in w_trk), "")
    cell(item, "d3 --fire turns the same WARN into a FAIL",
         "OB13_NOT_COMPUTED" in f_fire, "")
    cell(item, "d4 genuine no-intersection still FAILs OB13_INTERSECTION",
         "OB13_INTERSECTION" in f_real, "")

    # ⛔ d5 IS THE CELL THE BRIEF ASKED FOR BY NAME: the two strings must DIFFER.
    # "I could not check" and "I checked and it is clean/dirty" rendering the
    # same way is this repo's most-repeated defect class, and asserting that
    # SOMETHING was printed does not catch it.
    cc = next((l for l in alines(trk, diff_paths=[]) if l.startswith("OB13_INTERSECTION")), "")
    ni = next((l for l in alines(BASE, diff_paths=["main.py", "doctrine.py"])
               if l.startswith("OB13_INTERSECTION")), "")
    ok = next((l for l in alines(BASE, diff_paths=DIFF)
               if l.startswith("OB13_INTERSECTION")), "")
    cell(item, "d5 CANNOT-COMPUTE string differs from no-intersection string",
         cc != ni and "CANNOT-COMPUTE" in cc and "CANNOT-COMPUTE" not in ni,
         f"cc={cc[18:52]!r}")
    cell(item, "d5b ...and from the clean-intersection string",
         cc != ok and "CANNOT-COMPUTE" not in ok, f"ok={ok[18:52]!r}")
    cell(item, "d5c three distinct verdict strings, not two",
         len({cc, ni, ok}) == 3, "")


# ===========================================================================
# (e) POOL ERA
# ===========================================================================
POOL_LINE = ("**POOL ERA: 2026-08-13T07:12:59Z..2026-08-14T23:59:59Z "
             "(n=540, the post-rotation pool)**")


def probe_e():
    item = "(e) pool era"
    no_era = "\n".join(l for l in BASE.splitlines() if "POOL ERA" not in l)
    empty = BASE.replace(POOL_LINE, "**POOL ERA:**")
    spans = BASE.replace("2026-08-13T07:12:59Z..2026-08-14T23:59:59Z",
                         "2026-08-01T00:00:00Z..2026-08-14T23:59:59Z")
    spans_ok = spans.replace("## FALSIFIER",
                             "**SPANS-POOL-CHANGE: a whole-history CPU-cost cut does not "
                             "care which maps were in the pool**\n\n## FALSIFIER")
    unparse = BASE.replace(POOL_LINE, "**POOL ERA: the recent era**")
    local_no_era = no_era.replace("**SURFACE: unrated**", "**SURFACE: local**")

    for name, txt, want in (("e1 share line, no POOL ERA -> FAIL", no_era, "POOL_ERA_PRESENT"),
                            ("e3 window spans the rotation -> FAIL", spans, "POOL_ERA_SINGLE"),
                            ("e5 POOL ERA declared EMPTY -> FAIL", empty, "POOL_ERA_NONEMPTY")):
        f, _w, _r = run(txt)
        cell(item, name, want in f, f"got {sorted(f) or 'none'}")
    for name, txt in (("e2 in-era window -> pass", BASE),
                      ("e4 spanning + SPANS-POOL-CHANGE -> pass", spans_ok),
                      ("e10 LOCAL surface needs no POOL ERA", local_no_era)):
        f, _w, _r = run(txt)
        cell(item, name, not {x for x in f if x.startswith("POOL_ERA")},
             f"got {sorted(f) or 'none'}")
    f, w, _r = run(unparse)
    cell(item, "e6 unparseable value -> WARN 'NOT COMPUTED', never a pass",
         not {x for x in f if x.startswith("POOL_ERA")}
         and any("NOT COMPUTED" in x for x in w), "")

    # --- the DERIVATION, including its degenerate cases (SPEC §5 P7/P8/P8b/P9)
    live, note = PC.pool_eras()
    cell(item, "e8 live tape -> exactly ONE event, 2026-08-13",
         live is not None and len(live) == 1
         and live[0][0].strftime("%Y-%m-%d") == "2026-08-13",
         f"{[(d.strftime('%Y-%m-%dT%H:%M:%SZ'), n, p) for d, n, p in (live or [])]}")
    # ⛔ P8b: THE CELL THAT PROVES MIN_PRIOR_GAMES DOES ANYTHING. Disabled, the
    # rule invents a second era at the tape's own beginning, where every map is
    # trivially "previously unseen".
    degen, _n = PC.pool_eras(min_prior=0)
    cell(item, "e8b min_prior=0 -> TWO events (the spurious tape-start cohort)",
         degen is not None and len(degen) == 2, f"{len(degen or [])} event(s)")
    # P7: a tape whose only novelty is ONE new map is not a pool change.
    one_new = TMP / "one_new.tsv"
    rows = ["created\tmap"]
    for i in range(900):
        rows.append(f"2026-08-01T00:{i//60:02d}:{i%60:02d}Z\t{'alpha' if i%2 else 'beta'}")
    rows.append("2026-08-05T00:00:00Z\tgamma")
    one_new.write_text("\n".join(rows) + "\n")
    ev, _n = PC.pool_eras(tape=one_new)
    cell(item, "e7 one new map after 900 games -> NO event (>=3 binds)", ev == [],
         f"{ev}")
    three_new = one_new.read_text() + ("2026-08-05T00:00:01Z\tdelta\n"
                                       "2026-08-05T00:00:02Z\tepsilon\n")
    p3 = TMP / "three_new.tsv"
    p3.write_text(three_new)
    ev3, _n = PC.pool_eras(tape=p3)
    cell(item, "e7b three new maps in the same window -> ONE event", len(ev3 or []) == 1,
         f"{len(ev3 or [])}")
    # P9: BLIND is not "no events".
    blind, why = PC.pool_eras(tape=TMP / "does_not_exist.tsv")
    cell(item, "e9 unreadable tape -> BLIND (None), never []",
         blind is None and "BLIND" in why, why[:44])


# ===========================================================================
# (f) FIXTURE HEADER + START MARKER
# ===========================================================================
GOOD_HDR = ("# FIXTURE\tshard=PROBE\ttreatment=bots/_a\tcontrol=bots/_b\tplanned_n=4"
            "\tworkers=10\thost=probe-host\tstart=2026-08-14T20:25:57Z\trunner=tools/overnight.sh")
COLS = "ts\tshard\tgame\tmap\tseed\tseat\twinner\tcond\tturns"
ROW1 = "2026-08-14T20:25:59Z\tPROBE\t0\tantler\t1\tA\tC\tcore_destroyed\t325"
ROW2 = "2026-08-14T20:26:01Z\tPROBE\t1\tantler\t1\tB\tT\tcore_destroyed\t153"


def _tape_rc(text, *extra):
    p = TMP / f"tape_{abs(hash(text)) % 10**8}.tsv"
    p.write_text(text)
    env = dict(os.environ, TOOL_INVOCATION_TAPE=str(TMP / "invocations.tsv"))
    r = subprocess.run([PY, str(ROOT / "tools" / "prereg_check.py"), "--tape", str(p)]
                       + list(extra), cwd=ROOT, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


def probe_f():
    item = "(f) fixture header"
    full = "\n".join([GOOD_HDR, COLS, ROW1, ROW2]) + "\n"
    legacy = "\n".join([COLS, ROW1, ROW2]) + "\n"
    no_start = "\n".join([GOOD_HDR.replace("\tstart=2026-08-14T20:25:57Z", ""), COLS, ROW1]) + "\n"
    bad_start = "\n".join([GOOD_HDR.replace("start=2026-08-14T20:25:57Z", "start=soon"),
                           COLS, ROW1]) + "\n"
    bad_cols = "\n".join([GOOD_HDR, COLS.replace("\tcond", ""), ROW1]) + "\n"

    rc, out = _tape_rc(full)
    cell(item, "f1 full header -> OK", rc == 0 and out.strip().endswith("PREREG_CHECK: OK"), "")
    rc, out = _tape_rc(legacy)
    cell(item, "f2 NO header -> FAIL on required field `start`",
         rc == 1 and "TAPE_FIXTURE_HEADER" in out and "required field `start` absent" in out
         and "LEGACY" in out, "")
    cell(item, "f2b ...and it is a FAIL, not a WARN",
         "WARN  TAPE_FIXTURE_HEADER" not in out, "")
    rc, out = _tape_rc(no_start)
    cell(item, "f3 header present, `start` missing -> FAIL naming start",
         rc == 1 and "TAPE_FIXTURE_HEADER" in out and "'start'" in out, "")
    rc, out = _tape_rc(bad_start)
    cell(item, "f4 unparseable start -> FAIL TAPE_START_PARSES",
         rc == 1 and "TAPE_START_PARSES" in out, "")
    rc, out = _tape_rc(bad_cols)
    cell(item, "f5 wrong game-row columns -> FAIL TAPE_ROW_SCHEMA",
         rc == 1 and "TAPE_ROW_SCHEMA" in out, "")
    rc, out = _tape_rc(legacy, "--tape-legacy-ok",
                       "pre-header tape from before the runner carried a START stamp")
    cell(item, "f6 legacy escape with a reason -> WARN, exit 0",
         rc == 0 and "escaped" in out, "")
    rc, out = _tape_rc(legacy, "--tape-legacy-ok")
    cell(item, "f6b bare --tape-legacy-ok is REFUSED", rc == 1 and "requires a REASON" in out, "")

    # --- THE RUNNER ACTUALLY EMITS IT. Checking that the checker can read a
    # header I typed proves nothing about the runner; this drives overnight.sh.
    out_dir = TMP / "shards"
    out_dir.mkdir()
    bd = TMP / "bots"
    bd.mkdir()
    for n in ("_probet", "_probec"):
        (bd / n).mkdir()
        (bd / n / "main.py").write_text("class Player:\n    pass\n")
    env = dict(os.environ, OUT=str(out_dir), WORKERS="7")
    subprocess.run(["zsh", str(ROOT / "tools" / "overnight.sh"), "PROBE",
                    str(bd / "_probet"), str(bd / "_probec"), "2", "1"],
                   cwd=ROOT, capture_output=True, text=True, timeout=600, env=env)
    tp = out_dir / "PROBE.tsv"
    hdr = PC.parse_fixture_header(tp.read_text()) if tp.exists() else {}
    cell(item, "f7 overnight.sh WRITES the header with every required field",
         all(hdr.get(k) for k in PC.TAPE_REQUIRED_FIELDS),
         ",".join(f"{k}={hdr.get(k)}" for k in ("shard", "workers", "start")))
    cell(item, "f7b ...and its start is a parseable UTC stamp",
         bool(hdr.get("start")) and PC._iso(hdr["start"]) is not None, hdr.get("start", ""))
    cell(item, "f7c ...and workers comes from the launcher's env", hdr.get("workers") == "7",
         hdr.get("workers", ""))
    n_rows = len([l for l in tp.read_text().splitlines()
                  if l.strip() and not l.startswith("#")]) - 1 if tp.exists() else -1
    cell(item, "f7d the tape holds exactly TARGET game rows", n_rows == 2, f"{n_rows}")

    # f8 -- RESUME ARITHMETIC. The header is a comment line, so a `wc -l` resume
    # count would be off by one and restart at the wrong seed. Re-run with a
    # bigger target and check it resumes at the row count, not at row count + 1.
    r = subprocess.run(["zsh", str(ROOT / "tools" / "overnight.sh"), "PROBE",
                        str(bd / "_probet"), str(bd / "_probec"), "4", "1"],
                       cwd=ROOT, capture_output=True, text=True, timeout=600, env=env)
    cell(item, "f8 resume counts games, not lines (RESUMING at 2/4)",
         "RESUMING PROBE at 2/4" in (r.stdout + r.stderr),
         (r.stdout + r.stderr).strip().splitlines()[0][:44] if r.stdout else "")

    # f9 -- a LEGACY tape resumed is MARKED, and still fails the schema. Not
    # grandfathered, not silently repaired with an invented start.
    leg_dir = TMP / "legacy"
    leg_dir.mkdir()
    (leg_dir / "LEG.tsv").write_text(legacy)
    subprocess.run(["zsh", str(ROOT / "tools" / "overnight.sh"), "LEG",
                    str(bd / "_probet"), str(bd / "_probec"), "2", "1"],
                   cwd=ROOT, capture_output=True, text=True, timeout=600,
                   env=dict(os.environ, OUT=str(leg_dir)))
    lt = (leg_dir / "LEG.tsv").read_text()
    cell(item, "f9 resumed legacy tape gets a FIXTURE-RESUME marker",
         "# FIXTURE-RESUME" in lt and "start=UNKNOWN-legacy-tape" in lt, "")
    rc, out = _tape_rc(lt)
    cell(item, "f9b ...and it still FAILS the schema (no invented start)",
         rc == 1 and "TAPE_START_PARSES" in out, "")

    # --- BLAST RADIUS: the two readers must survive the new comment line.
    # Recount AFTER the f8 resume, which appended two more games to this tape.
    n_rows = len([l for l in tp.read_text().splitlines()
                  if l.strip() and not l.startswith("#")]) - 1
    rows = EN.load(tp)
    cell(item, "f10 effective_n.load() reads a header-bearing tape",
         len(rows) == n_rows and all(r.get("winner") in ("T", "C", "NOWINNER") for r in rows),
         f"{len(rows)} row(s), keys={sorted(rows[0])[:3] if rows else []}")
    loaded = OR.load(str(out_dir))
    got = loaded.get("PROBE", {}).get("rows", [])
    cell(item, "f11 overnight_read.load() reads it and skips the comment",
         len(got) == n_rows and all(g[0].startswith("20") for g in got),
         f"{len(got)} row(s)")
    # AND THE CONTROL that makes f10/f11 mean something: an UNFILTERED read of
    # the same tape must produce the WRONG answer. If it did not, the readers
    # never needed patching and these two cells assert nothing.
    import csv as _csv
    with open(tp, newline="") as fh:
        naive = list(_csv.DictReader(fh, delimiter="\t"))
    cell(item, "f10b control: an UNFILTERED DictReader gets it WRONG",
         not naive or "winner" not in naive[0], f"keys={sorted(naive[0])[:2] if naive else []}")


def main() -> int:
    for fn in (probe_a, probe_b, probe_c, probe_d, probe_e, probe_f):
        try:
            fn()
        except Exception as exc:                                   # noqa: BLE001
            import traceback
            traceback.print_exc()
            cell(fn.__name__, "PROBE RAISED", False, f"{type(exc).__name__}: {exc}")
    width = max(len(c) for _i, c, _d, _o in ROWS) + 2
    item = None
    print("WIRING BUNDLE FORCED-FAIL PROBE — every guard driven to BOTH verdicts\n")
    for it, name, detail, ok in ROWS:
        if it != item:
            print(f"\n{it}")
            item = it
        print(f"  [{'ok ' if ok else 'BAD'}] {name:<{width}} {detail[:46]}")
    bad = sum(1 for *_x, ok in ROWS if not ok)
    print(f"\n{len(ROWS)} cell(s), {bad} wrong")
    print(f"PROBE: {'OK' if not bad else 'FAIL'}")
    return 1 if bad else 0


if __name__ == "__main__":
    try:
        rc = main()
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
        shutil.rmtree(UNTRACKED_ARM, ignore_errors=True)
    sys.exit(rc)
