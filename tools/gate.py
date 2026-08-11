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
                                  [--maps hive atoll ...] [--allow-self-play]

Exit code 0 = cleared to run a battery. Non-zero = do not measure.
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

# identifiers that appear in our own lineage and would not appear in a
# genuinely foreign bot; used to detect a self-play pool
OUR_SIGNATURES = ("SLOT_ROLE_N", "HUNT_BAND_DSQ", "_try_counterbattery", "SLOT_UNDER")

FAIL: list[str] = []
WARN: list[str] = []


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


def check_programme(plank: Path, allow_off: bool) -> None:
    """Refuse a battery that is not on the ACTIVE PROGRAMME.

    WHY THIS IS A GATE AND NOT A NOTE. The s22 LOKI-3 result was recorded in
    prose, inherited wrong by three successive sessions, and the road was closed
    on it for two days while every plank went into the line the directive had
    already deprioritised. The measured half-life of a wrap note in this repo is
    about one session; the only surfaces that hold are builder.md and a tool
    that exits non-zero. So the programme is enforced here, in front of the
    battery, where it cannot be forgotten.

    Reads PROGRAMME.md. Edit that file only on Magnus's directive.
    """
    prog = ROOT / "PROGRAMME.md"
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
    pairs = re.findall(r"^\s{4}([A-Z_0-9]+):\s*(.+?)\s*$", raw, re.M)
    # ⛔ PERMISSIVE pattern on purpose. First written as [A-Z_0-9]+ -- the SAME
    # class as the parser -- so an unparseable name dropped out of BOTH counts
    # and the guard could never fire. Driven to the other verdict by renaming a
    # field to KILL-WINDOW-RND: with the matched class it printed nothing; with
    # this one it warns. A guard that cannot produce the other answer has not
    # been seen to check.
    _declared = len(re.findall(r"^\s{4}[^\s:]+:\s", raw, re.M))
    if len(pairs) != _declared:
        print(f"WARN  PROGRAMME.md: parsed {len(pairs)} fields but {_declared} "
              f"are declared -- a field name is unparseable")
    _dupes = [k for k in {k for k, _ in pairs} if [x for x, _ in pairs].count(k) > 1]
    if _dupes:
        # dict() keeps the LAST occurrence, so a copy inside a prose block
        # SILENTLY OVERRIDES the canonical declaration with no error and no diff.
        print(f"WARN  PROGRAMME.md: DUPLICATE field(s) {sorted(_dupes)} -- "
              f"last occurrence wins; de-indent the prose copy")
    fields = dict(pairs)
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
    print(f"  running: fcode match test {plank} {parent}   (real engine, real TLE)")
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plank", required=True)
    ap.add_argument("--control", required=True)
    ap.add_argument("--parent", required=True)
    ap.add_argument("--opponents", nargs="+", required=True)
    ap.add_argument("--maps", nargs="+",
                    default=["hive", "atoll", "meander", "archipelago", "saga", "nordkap"])
    ap.add_argument("--skip-tle", action="store_true",
                    help="skip the remote TLE fidelity check (records a WARN)")
    ap.add_argument("--off-programme", action="store_true",
                    help="run a battery outside the active PROGRAMME.md line")
    ap.add_argument("--pooled-not-paired", metavar="REASON", default="",
                    help="ESCAPE, TAKES A REASON STRING: downgrade the NOISE_ON FAILs to WARN. "
                         "Valid ONLY for a POOLED estimate, never a paired/seed-matched "
                         "one. Pinning NOISE_ON=False is not a free fix: engine seed "
                         "sensitivity is map-dependent and measured at ZERO on antler.")
    ap.add_argument("--allow-self-play", action="store_true",
                    help="acknowledge a self-play pool and proceed (result is SAFETY only)")
    a = ap.parse_args()

    plank, control, parent = Path(a.plank), Path(a.control), Path(a.parent)
    opponents = [Path(o) for o in a.opponents]

    check_programme(plank, a.off_programme)

    check_determinism([plank, control, parent] + opponents,
                      pooled_not_paired=a.pooled_not_paired)
    check_pool_identity(opponents, a.allow_self_play)
    if not FAIL:
        if a.pooled_not_paired:
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
            check_platform_instruments(plank, parent, a.skip_tle)
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
