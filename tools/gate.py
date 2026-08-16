#!/usr/bin/env python3
"""Pre-flight guard for a plank battery. Refuses to run a battery that cannot
produce a trustworthy answer.

WHY THIS EXISTS. On 2026-08-09 (s23) five planks were gated in one session and
every methodological rule that session produced was written into prose. Two of
them were then broken by their own author within hours:

  * NOISE_ON left True on both arms, so a "control equivalence" check compared
    two NON-DETERMINISTIC bots and returned 0/14. Diagnosed, written into
    docs/coordination.md, relayed to the research arm as a lesson -- and made
    again two hours later on the next build.
  * 1,500 battery games were run before anyone read a docstring in bots/opp_v63
    and discovered THE ENTIRE OPPONENT POOL IS OUR OWN PRIOR VERSIONS. Every
    result that day was self-play. The published literature (Agade, Code Royale
    3rd) puts a ~2x inflation factor on self-play amputation results and other
    winners report outright SIGN FLIPS.

A note is not a control. These are the checks that would have caught both, in
the only place that cannot be forgotten: in front of the battery.

Usage:
    .venv/bin/python tools/gate.py --plank bots/_v114esc \
                                  --control bots/_v114off \
                                  --parent bots/_det_v100hf \
                                  --opponents bots/_det_opp_v63 bots/_det_opp_v78 \
                                  [--maps hive atoll ...] [--allow-self-play REASON]

    .venv/bin/python tools/gate.py --selftest
        Fixture-driven check of the enforcement path (LINE_DIRS on-line/
        off-line, the escape downgrade, the parse-count canary, the
        duplicate-field hazard, the missing-file WARN). No battery, no
        network, no live PROGRAMME.md.

Exit code 0 = cleared to run a battery. Non-zero = do not measure.

EVERY INVOCATION IS TAPED to gate_invocations.tsv (tools/escape_tape.py),
escaped or not, so the BYPASS RATE has a denominator. All four escapes
(--pooled-not-paired, --off-programme, --skip-tle, --allow-self-play) take a
>=20-char REASON and are REFUSED without one; a refused escape does not silence
its check.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from fnmatch import fnmatch
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"

if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from escape_tape import record as tape_record          # noqa: E402
import programme                                       # noqa: E402  (THE ONE PROGRAMME.md parse)

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

# ⛔ FOUR ESCAPES, NOT ONE, AND THEY WERE ASYMMETRIC UNTIL 2026-08-14.
# `--pooled-not-paired` demanded a >=20-char REASON on the argument that "an
# escape with no stated reason is not a decision on the record". Its three
# neighbours -- `--off-programme`, `--skip-tle`, `--allow-self-play` -- were bare
# `store_true` and demanded nothing. **A guard present on one path and absent
# from its neighbour is exactly the shape this project hunts for in opponents'
# code** (CLAUDE.md, "LOOK FOR ASYMMETRIC GUARDS"); finding it in our own gate is
# not something to leave in place. All four now take a reason and REFUSE without
# one -- and a refused escape is NOT taken, so the check it would have silenced
# still runs.
ESCAPE_FLAGS = ("pooled-not-paired", "off-programme", "skip-tle", "allow-self-play")
MIN_REASON_CHARS = 20

# identifiers that appear in our own lineage and would not appear in a
# genuinely foreign bot; used to detect a self-play pool
OUR_SIGNATURES = ("SLOT_ROLE_N", "HUNT_BAND_DSQ", "_try_counterbattery", "SLOT_UNDER")

FAIL: list[str] = []
WARN: list[str] = []


def take_escape(name: str, value: str | None) -> str:
    """-> the REASON if the escape was validly taken, else "" (REFUSED).

    `value is None` means the flag was not passed at all -- silence, no FAIL.
    `value == ""` means the flag WAS passed with no reason (argparse `const`),
    which is a refusal WITH a FAIL: the caller reached for the escape and did
    not pay for it. The distinction matters because "" and None would otherwise
    render identically and a bare flag would read as an untyped flag.
    """
    if value is None:
        return ""
    if len(value.strip()) < MIN_REASON_CHARS:
        FAIL.append(
            f"--{name} requires a REASON of >={MIN_REASON_CHARS} chars naming the "
            f"design decision (got {len(value.strip())}). An escape with no stated "
            f"reason is not a decision on the record -- and a REFUSED escape does "
            f"not silence its check, so re-run with the reason or fix the battery.")
        return ""
    return value.strip()


def _src(bot: Path) -> str:
    return "\n".join(p.read_text(errors="replace") for p in sorted(bot.glob("*.py")))


def check_determinism(bots: list[Path], pooled_not_paired: bool = False) -> None:
    """Every side must be deterministic or PAIRED comparison is meaningless.

    ⛔ ESCAPE ADDED s32 2026-08-11 (`--pooled-not-paired`), AND IT EXISTS BECAUSE
    THIS CHECK'S PRESCRIPTION WAS MEASURED TO DESTROY A BATTERY IT REFUSED.

    The check is right about what it names: a PAIRED design cannot pair against a
    bot that reseeds.  Its REMEDY -- "flip it to False in this COPY" -- assumes
    the engine supplies variation once our own RNG stops.  Measured on this
    machine 2026-08-11 with `NOISE_ON = False` on both sides:

        antler   1 distinct outcome / 6 seeds   (B, turn 170, every seed)
        atoll    1 distinct outcome / 6 seeds   (B, turn 942, every seed)
        meander  1 distinct outcome / 6 seeds   (B, turn 135, every seed)
        hive     2 distinct outcomes / 6 seeds

    ⇒ **The engine's own seed sensitivity is MAP-DEPENDENT and it is ZERO on
    THREE OF THE FOUR maps tested** -- not on antler alone, which is what this
    docstring claimed for its first twenty minutes. The number is the argument,
    so it is stated at its real size.  Pinning `NOISE_ON = False` there would
    have collapsed that map's ~676 games to ONE distinct game while the row count
    still read 676 -- a sample-size collapse invisible in every denominator we
    print.  The gate would have passed and the battery would have been worthless.

    So the flag does NOT silence the check; it downgrades the two NOISE_ON FAILs
    to loud WARNs and prints the caller's justification.  Use it ONLY for a
    POOLED estimate (noise is exchangeable and unbiased, so pooled estimates
    stand -- `QUEUE.md` records this), NEVER for a paired or seed-matched one.
    An escape flag typed is a decision on the record; that is the point of it.
    """
    if pooled_not_paired:
        # The flag takes a REASON STRING and refuses without one. The docstring
        # used to say it "prints the caller's justification" while the code
        # appended a hardcoded constant -- i.e. a self-declared escape whose
        # predicate is supplied by the party it guards. An escape flag typed is
        # a decision on the record only if the caller has to type the decision.
        if not isinstance(pooled_not_paired, str) or len(pooled_not_paired.strip()) < 20:
            FAIL.append("--pooled-not-paired requires a REASON of >=20 chars "
                        "naming the design (e.g. 'pooled within-game win rate, "
                        "no seed-matched or across-run comparison'). An escape "
                        "with no stated reason is not a decision on the record.")
            return
        WARN.append(f"--pooled-not-paired ESCAPE TAKEN. Reason: {pooled_not_paired.strip()}")
        WARN.append("  NOISE_ON determinism FAILs downgraded to WARN. Valid ONLY "
                    "for a POOLED estimate. Pinning NOISE_ON=False is NOT a free "
                    "fix -- seed sensitivity is map-dependent and measured at "
                    "ZERO on 3 of 4 maps tested.")
    for b in bots:
        s = _src(b)
        if "NOISE_ON = True" in s:
            (WARN if pooled_not_paired else FAIL).append(
                f"{b.name}: NOISE_ON = True -- flip it to False in this COPY "
                f"(tools/det.py says ALL sides, and s23 got this wrong twice)")
        elif "NOISE_ON" not in s:
            WARN.append(f"{b.name}: no NOISE_ON constant (older lineage; assumed deterministic)")
        # NOISE_ON is OUR lineage's determinism switch and says nothing about a
        # foreign bot. The probes have no such constant, so the branch above
        # waves every one of them through on "assumed deterministic" -- and
        # s24 found `rush_probe` making TEN `random.` calls in its hot path
        # (spawn choice, three direction shuffles, target choice) while
        # HANDOVER's exclusion list named only `cad_probe`. A determinism gate
        # that passes a bot calling random.shuffle three times per turn is not
        # gating determinism. Check the actual source, not our own idiom.
        calls = sorted({
            name for ln in s.splitlines()
            if "random." in ln and not ln.lstrip().startswith("#")
            for name in (ln.split("random.")[1].split("(")[0].strip(),)
            if name.isidentifier()
        })
        if not calls:
            continue
        if "NOISE_ON = False" in s:
            # Our own lineage declares determinism with the switch, and its one
            # `random.Random()` sits on the False side of a conditional that is
            # never evaluated. Source presence is not execution -- downgrade,
            # don't block, or the gate fails every battery we ever run.
            WARN.append(f"{b.name}: random.{{{', '.join(calls)}}} present but "
                        f"NOISE_ON = False is declared; assumed gated.")
        else:
            (WARN if pooled_not_paired else FAIL).append(
                f"{b.name}: calls random.{{{', '.join(calls)}}} and declares no "
                f"NOISE_ON switch -- paired fixtures do not pair against a bot "
                f"that reseeds. Exclude it from the pool, or pin its seed in a "
                f"COPY before measuring.")


def _norm_line_pat(x: str) -> str:
    return Path(x).name.lstrip("_").removeprefix("det_").lstrip("_")


def incumbent_matches_line_dirs(raw: str) -> bool | None:
    """The invariant behind the LINE_DIRS-STALE warn, importable on its own.

    Returns None when either field is absent (nothing to check), else whether
    the INCUMBENT matches any LINE_DIRS pattern. Lives at module level so
    tests/test_instruments.py can run it against the LIVE PROGRAMME.md at every
    boot — the selftest cells here are fixture-only by design, and the two
    historical breakages (s31, s46) each sat unseen for days precisely because
    nothing boot-run evaluated the live file.
    """
    pairs = dict(re.findall(r"^\s{4}([A-Z_0-9]+):\s*(.+?)\s*$", raw, re.M))
    inc, pats = pairs.get("INCUMBENT", ""), pairs.get("LINE_DIRS", "").split()
    if not inc or not pats:
        return None
    return any(fnmatch(_norm_line_pat(inc), _norm_line_pat(p)) for p in pats)


def check_programme(plank: Path, allow_off: bool, prog_path: Path | None = None) -> None:
    """Refuse a battery that is not on the ACTIVE PROGRAMME.

    WHY THIS IS A GATE AND NOT A NOTE. The s22 LOKI-3 result was recorded in
    prose, inherited wrong by three successive sessions, and the road was closed
    on it for two days while every plank went into the line the directive had
    already deprioritised. The measured half-life of a wrap note in this repo is
    about one session; the only surfaces that hold are builder.md and a tool
    that exits non-zero. So the programme is enforced here, in front of the
    battery, where it cannot be forgotten.

    Reads PROGRAMME.md. Edit that file only on Magnus's directive.

    `prog_path` overrides which file is read; DEFAULT UNCHANGED (ROOT /
    "PROGRAMME.md"). Exists so `selftest()` below can drive this exact function
    against a FIXTURE programme instead of the live one -- a check whose
    verdict depends on today's LINE_DIRS is a defect this repo has already
    fixed twice (timestamps, DEFF constants).
    """
    prog = prog_path if prog_path is not None else ROOT / "PROGRAMME.md"
    if not prog.exists():
        WARN.append("no PROGRAMME.md -- no active line is being enforced")
        return
    # [A-Z_0-9]+ NOT [A-Z_]+ -- the original excluded DIGITS, so `R1000_IS_DEFEAT`
    # sat inside the block headed "The fields below are parsed" and was NEVER
    # PARSED. 15 fields read vs 16 present, and the missing one was that one.
    # A doctrine field that looks machine-enforced and is decorative is the
    # CLAUDE.md-vs-reference-doc failure INSIDE the machine-readable block.
    # (Side lane, s31.) The count selftest below is what keeps it honest.
    raw = prog.read_text()
    # ⭐ THE PATTERNS MOVED TO tools/programme.py (s47 wrap debt 12) so that
    # slot_rule and elo_logger read PROGRAMME.md with THIS parse instead of
    # their own. They used to scan `line.strip()` and take the FIRST match,
    # indented or not, while this one takes the LAST indented one -- opposite
    # answers on the same file, reproduced on a constructed prose copy. The
    # regexes and their two comments (permissive DECLARED_RE, digits in the
    # name class) live in that module now; the guards below are unchanged.
    pairs = programme.pairs(raw)
    _declared = programme.declared(raw)
    if len(pairs) != _declared:
        print(f"WARN  PROGRAMME.md: parsed {len(pairs)} fields but {_declared} "
              f"are declared -- a field name is unparseable")
    _dupes = programme.duplicates(raw)
    if _dupes:
        # dict() keeps the LAST occurrence, so a copy inside a prose block
        # SILENTLY OVERRIDES the canonical declaration with no error and no diff.
        print(f"WARN  PROGRAMME.md: DUPLICATE field(s) {sorted(_dupes)} -- "
              f"last occurrence wins; de-indent the prose copy")
    fields = programme.fields(raw)
    line = fields.get("LINE", "?")
    pats = fields.get("LINE_DIRS", "").split()
    print("ACTIVE PROGRAMME")
    print(f"  line: {line}   incumbent {fields.get('INCUMBENT','?')} "
          f"(frozen: {fields.get('INCUMBENT_FROZEN','?')})")
    print(f"  verdict currency: {fields.get('PRIMARY_CURRENCY','?')} "
          f"| win rate is a verdict: {fields.get('WIN_RATE_IS_VERDICT','?')}")
    # Normalise BOTH sides the same way, or a deterministic copy of an
    # on-line bot fails its own line: `_det_v105loki1` must match `_v105loki1`.
    def norm(x):
        return Path(x).name.lstrip("_").removeprefix("det_").lstrip("_")
    # ⭐ INVARIANT (side lane s45, consumed by builder s46): the INCUMBENT must
    # itself match LINE_DIRS.
    # Both prior repairs of this field were NAME PATTERNS and both expired when
    # the naming convention advanced (s31: loki-names stopped at _v139heal;
    # s46: _v1[3-9]?* stopped at v199 while the line went v2xx — ~47h with the
    # ENTIRE line outside the field, 26/27 batteries bypassing via
    # --off-programme). A pattern renewal has a shelf life; this re-derives
    # from the two fields on every run and cannot expire.
    if incumbent_matches_line_dirs(raw) is False:
        WARN.append(f"LINE_DIRS STALE: the INCUMBENT {fields.get('INCUMBENT','?')} does not match any "
                    f"LINE_DIRS pattern -- the gate would refuse the line it "
                    f"exists to serve. Widen LINE_DIRS (Magnus's directive) "
                    f"before trusting any refusal it produces.")
    on_line = any(fnmatch(norm(plank.name), norm(pat)) for pat in pats)
    if on_line:
        print(f"  {plank.name}: ON the {line} line")
        return
    msg = (f"OFF PROGRAMME: {plank.name} is not on the active '{line}' line "
           f"({fields.get('LINE_DIRS','')}). The incumbent is frozen and Loki is a "
           f"SEPARATE BOT, not a flag on the Eir chassis. Pass --off-programme "
           f"with a reason, or change PROGRAMME.md on Magnus's directive.")
    (WARN if allow_off else FAIL).append(msg)


def check_pool_identity(opponents: list[Path], allow: bool) -> None:
    """State what the opponent pool IS, from its source, before measuring."""
    print("OPPONENT POOL IDENTITY")
    selfplay = []
    for o in opponents:
        s = _src(o)
        hits = sum(1 for sig in OUR_SIGNATURES if sig in s)
        head = next((ln.strip().strip('"') for ln in s.splitlines()
                     if ln.strip().strip('"')), "")[:70]
        tag = "OUR OWN LINEAGE" if hits >= 3 else "foreign"
        if hits >= 3:
            selfplay.append(o.name)
        print(f"  {o.name:22} {tag:16} ({hits}/{len(OUR_SIGNATURES)} sigs)  {head}")
    if selfplay:
        msg = (f"SELF-PLAY POOL: {len(selfplay)}/{len(opponents)} opponents are our own "
               f"prior versions. Published amputation results run ~2x self-play vs field, "
               f"with reported SIGN FLIPS. This battery measures SAFETY, not field effect.")
        (WARN if allow else FAIL).append(msg)


def check_control_equivalence(control: Path, parent: Path, opponent: Path,
                              maps: list[str]) -> None:
    """The flags-off arm MUST be behaviourally identical to its parent.

    This is the check whose absence produced a 0/14 result that looked like a
    catastrophic regression and was actually a forgotten constant.
    """
    print("\nCONTROL EQUIVALENCE  (flags-off arm vs parent)")
    same = 0
    total = 0
    for m in maps:
        for seat in ("a", "b"):
            keys = []
            for bot in (control, parent):
                a, b = ((bot, opponent) if seat == "a" else (opponent, bot))
                r = subprocess.run(
                    [str(FCODE), "run", str(a), str(b), f"maps/{m}.map26",
                     "--seed", "1", "--tle", "0", "--json"],
                    cwd=ROOT, capture_output=True, text=True)
                line = [l for l in r.stdout.splitlines() if l.startswith("{")]
                if not line:
                    FAIL.append(f"control-equivalence run failed on {m}/{seat}")
                    return
                d = json.loads(line[-1])
                keys.append((d["winner"], d["turns"], d["win_condition"],
                             d["a_titanium_collected"], d["b_titanium_collected"]))
            total += 1
            if keys[0] == keys[1]:
                same += 1
            else:
                print(f"  MISMATCH {m}/{seat}: {keys[0]} vs {keys[1]}")
    print(f"  identical {same}/{total}")
    if same != total:
        FAIL.append(f"CONTROL IS NOT ITS PARENT ({same}/{total}). The flags-off arm must be "
                    f"behaviourally identical or every delta is unattributable.")


def check_platform_instruments(plank: Path, parent: Path, skip: bool) -> None:
    """Local batteries run at --tle 0. The real engine enforces 10ms.

    On 2026-08-09 six planks were gated across 1,860 local games, EVERY ONE at
    --tle 0 and every one against our own prior versions, while two platform
    instruments went unused all session:

        fcode match test BOT_A BOT_B   local bots, REMOTE engine, REAL TLE
        fcode match unrated OPPONENT   a REAL opposing team, zero Elo risk

    Our own worst observed unit-turn in real ladder games is 12,967us against a
    10,000us limit, so the headroom is thin and every plank adds per-turn work.
    A plank that has never run under an enforced limit has an untested failure
    mode that the local arena CANNOT see.
    """
    print("\nPLATFORM INSTRUMENTS")
    if skip:
        WARN.append("TLE fidelity unverified (--skip-tle passed): local runs use "
                    "--tle 0 and cannot see a CPU regression")
        print("  skipped (--skip-tle)")
        return
    # ⛔⛔ THIS COSTS A RATE-LIMIT SLOT, AND THE BUDGET IS SHARED WITH UNRATED LEGS.
    # The platform caps `test` AND `unrated` together at 5 per 20 minutes, and
    # REJECTED attempts count. MEASURED s44 2026-08-15: four gate runs inside one
    # 20-minute window left one slot, so CAL418's first firing cycle got 2 accepts
    # and 3 REJECTIONS -- the gate that clears a battery had silently eaten the
    # budget of the leg fired after it. Nothing anywhere said so, and the rate
    # pre-check I ran read "0 non-ladder matches in the trailing 1200s" because it
    # filtered on a `type` field these test matches do not populate.
    # ⇒ IF A LIVE LEG IS IMMINENT, PASS --skip-tle (a recorded decision) OR RUN THE
    # GATE MORE THAN 20 MINUTES AHEAD OF THE FIRING WINDOW.
    print(f"  running: fcode match test {plank} {parent}   (real engine, real TLE)")
    print("  ⚠ this SPENDS one of the 5-per-20-min test/unrated slots, shared with "
          "unrated legs — see the comment above before firing a leg within 20 min")
    r = subprocess.run([str(FCODE), "match", "test", str(plank), str(parent)],
                       cwd=ROOT, capture_output=True, text=True, timeout=900)
    out = r.stdout + r.stderr
    mid = next((w.strip() for ln in out.splitlines() if "Match ID" in ln
                for w in [ln.split(":")[-1]]), None)
    if not mid:
        WARN.append(f"could not queue a remote TLE test: {out.strip()[:160]}")
        return
    print(f"  queued {mid} -- poll with: fcode match info {mid}")
    print("  NOTE: this checks CPU fidelity ONLY. It does NOT make the pool foreign.")


# ═════════════════════════════════════════════════════════════════════════════
# SELFTEST -- the enforcement path, on the SHIPPED function, against FIXTURES
# ═════════════════════════════════════════════════════════════════════════════
# ⛔ WHY THIS EXISTS. A side-lane audit found gate.py was the only significant
# tool in tools/ with NO selftest and NO test coverage -- the LINE_DIRS matching
# that decides CLEARED vs DO NOT MEASURE was exercised by nothing but production
# use. This repo's own rule: "every guard must be drivable to BOTH verdicts,
# and a check never observed to fail has not been seen to check."
#
# SCOPE. Covers check_programme() -- the ENFORCEMENT contract named in the
# audit: on-line pass, off-line refusal (and its escape downgrade), the
# parse-count canary, the duplicate-field hazard, and the missing-file path.
# check_determinism(), check_pool_identity(), check_control_equivalence() and
# check_platform_instruments() all shell out to `fcode` (real subprocess, real
# platform, real rate-limited slots) and are not covered here -- fixturing them
# would mean mocking the platform's own responses, which tests the mock, not
# the gate. That is a real gap, not a hidden one: named so a future selftest
# extension knows what is still uncovered rather than assuming full coverage.
#
# FIXTURE-DRIVEN, NOT LIVE. Every cell builds its own temp PROGRAMME.md and
# passes it in via `prog_path` -- never reads the repo's real PROGRAMME.md.
# The live file's LINE_DIRS changes with every plank rotation; a selftest that
# read it would pass or fail depending on the day, which is a defect this repo
# has fixed twice already (interpolated timestamps, a DEFF constant computed
# from the mutable pool). Reference constants below are typed independently of
# the regex they check, not copied out of a run.
def selftest() -> int:
    import io
    import shutil
    import tempfile
    from contextlib import redirect_stdout

    fails: list[str] = []
    n_cells = 0

    def chk(label: str, got, want) -> None:
        nonlocal n_cells
        n_cells += 1
        if got == want:
            print(f"  [ok]   {label:<66} -> {got}")
        else:
            print(f"  [FAIL] {label:<66} -> {got!r} (want {want!r})")
            fails.append(label)

    tmp = Path(tempfile.mkdtemp(prefix="gate_selftest_"))

    # A minimal but real-shaped programme block: 4-space indent, the two
    # fields check_programme() actually reads (LINE, LINE_DIRS), and nothing
    # else -- so a cell that adds one hazardous line is an isolated diff
    # against a known-clean baseline, not a rewrite of the whole fixture.
    BASE = (
        "# fixture programme -- selftest only, never the live PROGRAMME.md\n"
        "\n"
        "    LINE: fixtline\n"
        "    LINE_DIRS: bots/_fixt* bots/_othr?\n"
        "    INCUMBENT: bots/_fixt_incumbent\n"
        "    INCUMBENT_FROZEN: no\n"
        "    PRIMARY_CURRENCY: game_share\n"
        "    WIN_RATE_IS_VERDICT: yes\n"
    )

    def run(cell: str, text: str | None, plank_name: str, allow_off: bool = False):
        """Call the SHIPPED check_programme() against a fixture and return
        (new_fail, new_warn, printed) -- the FAIL/WARN entries and stdout THIS
        call produced, isolated from every other cell.

        FAIL/WARN are module-level lists check_programme() APPENDS to; that
        append IS the enforcement (main() reads len(FAIL) to pick the exit
        code). Snapshot-and-diff around the call so cells don't see each
        other's residue, then delete what this call added so the module is
        clean for the next cell and for any real run afterward.
        `text is None` -> no PROGRAMME.md is written at all, for the
        missing-file cell.
        """
        cell_dir = tmp / cell
        cell_dir.mkdir()
        prog_path = cell_dir / "PROGRAMME.md"
        if text is not None:
            prog_path.write_text(text)
        fail_before, warn_before = len(FAIL), len(WARN)
        buf = io.StringIO()
        with redirect_stdout(buf):
            check_programme(Path(plank_name), allow_off, prog_path=prog_path)
        new_fail, new_warn = FAIL[fail_before:], WARN[warn_before:]
        del FAIL[fail_before:]
        del WARN[warn_before:]
        return new_fail, new_warn, buf.getvalue()

    print("── a: plank INSIDE the fixture line's LINE_DIRS -- must clear ──────────")
    f, w, out = run("a_online", BASE, "bots/_fixt_v7")
    chk("on-line plank: no FAIL", len(f), 0)
    chk("on-line plank: no WARN", len(w), 0)
    chk("on-line plank: prints 'ON the <line> line'", "ON the fixtline line" in out, True)

    print("\n── b: plank OUTSIDE LINE_DIRS -- the refusal must actually FIRE ────────")
    f, w, out = run("b_offline", BASE, "bots/_totally_unrelated")
    chk("off-line plank, no escape: exactly 1 FAIL", len(f), 1)
    chk("...and it is the OFF PROGRAMME refusal", "OFF PROGRAMME" in (f[0] if f else ""), True)
    f2, w2, _ = run("b_offline_esc", BASE, "bots/_totally_unrelated", allow_off=True)
    chk("off-line plank, --off-programme granted: FAIL is gone", len(f2), 0)
    chk("...refusal downgrades to WARN, is NOT silenced",
        bool(w2) and "OFF PROGRAMME" in w2[0], True)

    print("\n── c: parse-count canary -- an unparseable field name -> WARN ──────────")
    # A hyphenated name matches the loose _declared count ([^\s:]+) but not the
    # strict parser class ([A-Z_0-9]+), so it is declared but never parsed --
    # exactly the KILL-WINDOW-RND failure mode the inline comment documents.
    bad_name = BASE + "    KILL-WINDOW-RND: 250\n"
    f, w, out = run("c_badname", bad_name, "bots/_fixt_v7")
    chk("unparseable field name: prints the parse-count WARN",
        "parsed" in out and "declared" in out, True)
    f, w, out = run("c_clean", BASE, "bots/_fixt_v7")
    chk("clean block: parse-count WARN does NOT fire",
        "parsed" in out and "declared" in out, False)

    print("\n── d: duplicate-field hazard -- an indented duplicate -> WARN ──────────")
    dupe = BASE + "    LINE_DIRS: bots/_someone_elses_pattern*\n"
    f, w, out = run("d_dupe", dupe, "bots/_fixt_v7")
    chk("duplicate field: prints the DUPLICATE WARN", "DUPLICATE" in out, True)
    f, w, out = run("d_clean", BASE, "bots/_fixt_v7")
    chk("clean block: DUPLICATE WARN does NOT fire", "DUPLICATE" in out, False)

    print("\n── e: missing PROGRAMME file -> the documented WARN, not a crash ───────")
    f, w, out = run("e_missing", None, "bots/_fixt_v7")
    chk("missing PROGRAMME.md: no FAIL (no crash)", len(f), 0)
    chk("...WARN fires instead", bool(w) and "no PROGRAMME.md" in w[0], True)

    print("\n── f: INCUMBENT-matches-LINE_DIRS invariant -- both verdicts ───────────")
    # The BASE fixture's incumbent (_fixt_incumbent) matches bots/_fixt* -- the
    # invariant must stay silent on a consistent file...
    f, w, out = run("f_inc_ok", BASE, "bots/_fixt_v7")
    chk("consistent INCUMBENT: no LINE_DIRS-STALE warn",
        any("LINE_DIRS STALE" in x for x in w), False)
    # ...and FIRE when the incumbent falls outside every pattern -- the exact
    # state PROGRAMME.md stood in for ~47h across s44-s46 (incumbent _v223*,
    # patterns capped at v199), which no fixture cell could see.
    STALE = BASE.replace("    INCUMBENT: bots/_fixt_incumbent\n",
                         "    INCUMBENT: bots/_beyond_the_patterns\n")
    f, w, out = run("f_inc_stale", STALE, "bots/_fixt_v7")
    chk("INCUMBENT outside every pattern: LINE_DIRS-STALE warn FIRES",
        any("LINE_DIRS STALE" in x for x in w), True)

    shutil.rmtree(tmp, ignore_errors=True)
    print()
    if fails:
        print(f"SELFTEST FAIL -- {len(fails)}/{n_cells} check(s): " + "; ".join(fails))
        return 1
    print(f"SELFTEST PASS -- {n_cells} cells "
          f"(a: on-line clears / b: off-line refuses + escape downgrades without "
          f"silencing / c: parse-count canary fires on a bad name, not on a clean "
          f"block / d: duplicate-field WARN fires on a dupe, not on a clean block / "
          f"e: missing file WARNs, does not crash)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    # NOT required=True at the argparse level -- --selftest must be runnable
    # with none of these present. Enforced by hand just below the parse, only
    # on the non-selftest path.
    ap.add_argument("--plank")
    ap.add_argument("--control")
    ap.add_argument("--parent")
    ap.add_argument("--opponents", nargs="+")
    ap.add_argument("--selftest", action="store_true",
                    help="fixture-driven check of the enforcement path "
                         "(LINE_DIRS on-line/off-line + escape downgrade, "
                         "parse-count canary, duplicate-field hazard, "
                         "missing-file WARN). No PROGRAMME.md, network, or "
                         "battery required; ignores every other flag.")
    ap.add_argument("--maps", nargs="+",
                    default=["hive", "atoll", "meander", "archipelago", "saga", "nordkap"])
    # ⛔ ALL FOUR ESCAPES TAKE A REASON. `nargs="?"` with `const=""` keeps the
    # bare form PARSEABLE on purpose -- a bare `--skip-tle` must reach
    # take_escape() and be REFUSED with a named FAIL, not die in argparse with a
    # usage string that says nothing about why the reason exists.
    esc = dict(nargs="?", const="", default=None, metavar="REASON")
    ap.add_argument("--skip-tle", **esc,
                    help="ESCAPE, TAKES A REASON: skip the remote TLE fidelity check "
                         "(records a WARN; local runs are --tle 0 and cannot see a CPU "
                         "regression)")
    ap.add_argument("--off-programme", **esc,
                    help="ESCAPE, TAKES A REASON: run a battery outside the active "
                         "PROGRAMME.md line")
    ap.add_argument("--pooled-not-paired", **esc,
                    help="ESCAPE, TAKES A REASON: downgrade the NOISE_ON FAILs to WARN. "
                         "Valid ONLY for a POOLED estimate, never a paired/seed-matched "
                         "one. Pinning NOISE_ON=False is not a free fix: engine seed "
                         "sensitivity is map-dependent and measured at ZERO on antler.")
    ap.add_argument("--allow-self-play", **esc,
                    help="ESCAPE, TAKES A REASON: acknowledge a self-play pool and "
                         "proceed (result is SAFETY only)")
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    missing = [f"--{n}" for n, v in (
        ("plank", a.plank), ("control", a.control), ("parent", a.parent),
        ("opponents", a.opponents)) if not v]
    if missing:
        ap.error(f"the following arguments are required: {', '.join(missing)}")

    plank, control, parent = Path(a.plank), Path(a.control), Path(a.parent)
    opponents = [Path(o) for o in a.opponents]

    # Validate every escape FIRST, so the tape row below records what was
    # actually GRANTED rather than what was typed.
    granted = {}
    for name in ESCAPE_FLAGS:
        r = take_escape(name, getattr(a, name.replace("-", "_")))
        if r:
            granted[name] = r

    # ⭐ ONE ROW PER INVOCATION, ESCAPED OR NOT. The escaped rows are the
    # numerator and ALL rows are the denominator -- a tape of escapes alone is a
    # count with nothing to divide by. See tools/escape_tape.py.
    battery = (f"plank={plank.name};control={control.name};parent={parent.name};"
               f"opponents={','.join(o.name for o in opponents)};"
               f"maps={','.join(a.maps)}")
    tape_record("gate.py", battery, escapes=granted, mode="battery")
    print("ESCAPES  " + (", ".join(f"--{k}" for k in sorted(granted)) if granted
                         else "none taken (this invocation is on the tape as a "
                              "denominator row)"))
    for k in sorted(granted):
        print(f"  --{k}: {granted[k]}")

    check_programme(plank, bool(granted.get("off-programme")))

    check_determinism([plank, control, parent] + opponents,
                      pooled_not_paired=granted.get("pooled-not-paired", ""))
    check_pool_identity(opponents, bool(granted.get("allow-self-play")))
    if not FAIL:
        if granted.get("pooled-not-paired"):
            # ⛔ SKIPPED DELIBERATELY, s32. check_control_equivalence runs the
            # control and the parent in TWO SEPARATE `fcode run` processes at
            # --seed 1 and demands byte-identical outcomes -- an ACROSS-RUN
            # seed-matched design, and the ONLY thing check_determinism was ever
            # protecting. Against a reseeding bot it reports a meaningless
            # mismatch: observed this session as `CONTROL IS NOT ITS PARENT
            # (0/12)` for a directory compared against ITSELF.
            # Downgrading determinism to WARN and then running this anyway
            # traded one confusing FAIL for a more confusing one.
            WARN.append("control-equivalence SKIPPED: it is an ACROSS-RUN "
                        "seed-matched check and cannot run against a reseeding "
                        "bot. This battery is therefore NOT control-verified; "
                        "the treatment/control diff stands on the tree diff alone.")
        else:
            check_control_equivalence(control, parent, opponents[0], a.maps)
    if not FAIL:
        try:
            check_platform_instruments(plank, parent, bool(granted.get("skip-tle")))
        except Exception as exc:                                  # noqa: BLE001
            WARN.append(f"remote TLE check did not run: {exc}")

    print()
    for w in WARN:
        print(f"WARN  {w}")
    for f in FAIL:
        print(f"FAIL  {f}")
    if FAIL:
        print("\nDO NOT MEASURE. Fix the above first.")
        return 1
    print("CLEARED to run a battery.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
