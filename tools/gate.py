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
import subprocess
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


def check_determinism(bots: list[Path]) -> None:
    """Every side must be deterministic or paired comparison is meaningless."""
    for b in bots:
        s = _src(b)
        if "NOISE_ON = True" in s:
            FAIL.append(f"{b.name}: NOISE_ON = True -- flip it to False in this COPY "
                        f"(tools/det.py says ALL sides, and s23 got this wrong twice)")
        elif "NOISE_ON" not in s:
            WARN.append(f"{b.name}: no NOISE_ON constant (older lineage; assumed deterministic)")


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
    ap.add_argument("--allow-self-play", action="store_true",
                    help="acknowledge a self-play pool and proceed (result is SAFETY only)")
    a = ap.parse_args()

    plank, control, parent = Path(a.plank), Path(a.control), Path(a.parent)
    opponents = [Path(o) for o in a.opponents]

    check_determinism([plank, control, parent] + opponents)
    check_pool_identity(opponents, a.allow_self_play)
    if not FAIL:
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
