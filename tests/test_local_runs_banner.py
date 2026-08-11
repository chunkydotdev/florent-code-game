"""The SessionStart banner that tells every lane what is running locally.

WHY THIS TEST EXISTS. `tools/corefill.sh` shipped 2026-08-11 and appeared 6 times
in HANDOVER.md and ZERO times in all three `.claude/commands/*.md`, CLAUDE.md,
PROGRAMME.md and QUEUE.md. That is verbatim the s31 finding about QUEUE.md itself
-- a rule promoted into a file nobody opens -- caught both times by Magnus asking
whether the next session would know. The banner lives in `queue_check.py` because
a SessionStart hook already runs that file in EVERY lane, harness-executed.

A BANNER THAT ONLY EVER SAYS "running" IS WORTHLESS, so all three states are
forced here: live, idle, and BLIND. Blind-vs-idle is the one that matters -- an
alarm that cannot tell it is blind is this repo's most-repeated defect.
"""
import contextlib, io, subprocess, sys, types
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import queue_check as Q

def _run(ps_stdout=None, raise_it=False):
    real = subprocess.run
    subprocess.run = lambda *a, **k: (_ for _ in ()).throw(OSError("simulated")) if raise_it \
        else types.SimpleNamespace(stdout=ps_stdout)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): Q.local_runs()
    finally:
        subprocess.run = real
    return buf.getvalue()

FAILS = []
def chk(name, ok, forced_by):
    print(f"  [{'ok' if ok else 'FAIL'}] {name}")
    if not ok:
        print(f"         forced by: {forced_by}"); FAILS.append(name)

live = _run("zsh tools/overnight.sh SR1CUR a b 1 2\nzsh tools/corefill.sh w 8 8\n")
chk("live: names the status tool, does not claim idle",
    "corefill_status.sh" in live and "NOTHING IS RUNNING" not in live,
    "a successor must be told the entry point, not just that something is running")

idle = _run("/usr/sbin/unrelated\n/bin/zsh\n")
chk("idle: calls it a DEFECT and names the start command",
    "NOTHING IS RUNNING LOCALLY" in idle and "corefill.sh scratchpad" in idle,
    "ALWAYS_BE_RUNNING says idle cores are a defect; the alarm must carry its remedy")

blind = _run(raise_it=True)
chk("BLIND is not reported as idle",
    "BLIND" in blind and "NOTHING IS RUNNING" not in blind,
    "reporting an unreadable process table as 'nothing running' would send a "
    "successor to start a second full programme on top of a live one")

print()
if FAILS:
    print(f"LOCAL_RUNS_BANNER: FAIL ({len(FAILS)}) -> {FAILS}"); sys.exit(1)
print("LOCAL_RUNS_BANNER: PASS (live / idle / blind all forced)")
