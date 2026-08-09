#!/usr/bin/env python3
"""Keeper — the long-lived data process that survives session wraps.

WHY THIS AND NOT CRON. The archiver currently runs as a child of whichever
session's shell launched it, so it dies at every wrap; between sessions nothing
pulls, and ladder replays may age out of the match-list window permanently. Cron
would fix that but keeps hammering the platform for weeks after we stop working
on the game. A detached keeper matches the real pattern: start it once when work
begins, kill it once when work ends, and it lives through every wrap in between.

    .venv/bin/python tools/corpus/keeper.py --start    # detach and run
    .venv/bin/python tools/corpus/keeper.py --status   # alive? what has it done?
    .venv/bin/python tools/corpus/keeper.py --stop
    .venv/bin/python tools/corpus/keeper.py            # foreground, for testing

WHAT IT DOES, every cycle (default 10 min):
  0. `ladder_watch()` — one `fcode status` poll. Detects a SHIP (active bot
     changed), a RATING DROP past the high-water mark, or a LOSING STREAK, and
     **sends a desktop notification**. Pure detection with fixed thresholds: it
     makes no judgement about regression-vs-variance, because a script cannot.
  1. `tools/monitors/replay_archiver.py` — downloads new replays. READ-ONLY
     against the platform (no submit/activate/challenge) and self-terminating,
     which is why it is safe to invoke on a timer.
  2. `tools/corpus/sync.py` — folds the new files into `corpus/`.
  3. One line to `corpus/keeper.log`.

**CPU SAFETY, and this is the point of the load check.** Decoding is CPU-heavy,
and a unit that overruns its 10 ms in a concurrent arena battery has that turn
silently discarded — no crash, no traceback. So contention degrades the builder's
measurements *invisibly*. On 2026-08-09 load hit 39-42 on a 10-core box with an
uninstrumented mix of batteries and my own passes. The keeper therefore runs
`nice`d and **defers the decode entirely while load is high**, logging the skip.
Archiving still runs — it is network-bound and cheap.

It never writes to the platform, never touches bots, the tape, or HANDOVER.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = str(ROOT / ".venv/bin/python")
HERE = Path(__file__).resolve().parent
PIDFILE = ROOT / "corpus" / "keeper.pid"
LOG = ROOT / "corpus" / "keeper.log"
STATE = ROOT / "corpus" / "keeper_state.json"

INTERVAL = 600          # seconds between cycles
LOAD_CEILING = 6.0      # 1-min load average above which the decode is deferred
NET_EVERY = 6           # pull ladder metadata every Nth cycle (~1h)
DROP_ALERT = 25.0       # notify on this much rating lost from the high-water mark
STREAK_ALERT = 2        # notify when last-10 wins falls to this or below


def stamp() -> str:
    return subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                          capture_output=True, text=True).stdout.strip()


def log(msg: str) -> None:
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a") as fh:
        fh.write(f"{stamp()}  {msg}\n")


def alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def read_pid() -> int | None:
    if not PIDFILE.exists():
        return None
    try:
        pid = int(PIDFILE.read_text().strip())
    except ValueError:
        return None
    return pid if alive(pid) else None


def loadavg() -> float:
    return os.getloadavg()[0]


def notify(title: str, msg: str) -> None:
    """Reach a human. A monitor that only writes files nobody reads is a log,
    not a wake path -- the rule both arms sat blind for five hours to learn."""
    log(f"ALERT {title}: {msg}")
    try:
        subprocess.run(["osascript", "-e",
                        f'display notification {json.dumps(msg)} '
                        f'with title {json.dumps(title)}'],
                       capture_output=True, timeout=15)
    except Exception:                                     # noqa: BLE001
        pass


def ladder_watch() -> None:
    """Cheap `fcode status` poll: ships, rating drops, losing streaks.

    Pure detection with fixed thresholds -- it makes NO judgement about whether a
    drop is regression or variance, because a script cannot. Its whole job is
    that when a human or a session next looks, they already know."""
    p = subprocess.run([str(ROOT / ".venv/bin/fcode"), "status"],
                       cwd=ROOT, capture_output=True, text=True, timeout=60)
    txt = p.stdout
    m_rate = re.search(r"Rating:\s*([\d.]+).*?(\d+)\s+matches", txt, re.S)
    m_bot = re.search(r"Active bot:\s*(.+)", txt)
    m_last = re.search(r"Last 10:\s*(\d+)W", txt)
    if not (m_rate and m_bot):
        return
    rating, matches = float(m_rate.group(1)), int(m_rate.group(2))
    bot = m_bot.group(1).strip()
    wins = int(m_last.group(1)) if m_last else None

    st = json.loads(STATE.read_text()) if STATE.exists() else {}
    peak = max(rating, st.get("peak", rating))

    if st.get("bot") and bot != st["bot"]:
        notify("florent: SHIP DETECTED",
               f"active bot changed {st['bot']} -> {bot} @ {rating:.0f}")
        peak = rating                      # new bot, new baseline
    elif peak - rating >= DROP_ALERT and st.get("alerted_at", 0) != round(rating):
        notify("florent: RATING DROP",
               f"{rating:.0f} is {peak - rating:.0f} below peak {peak:.0f} "
               f"({matches} matches)")
        st["alerted_at"] = round(rating)
    elif wins is not None and wins <= STREAK_ALERT and st.get("wins") != wins:
        notify("florent: LOSING STREAK", f"last 10 = {wins}W, rating {rating:.0f}")

    if st.get("matches") != matches:
        log(f"ladder {bot} · {rating:.1f} @ {matches}"
            + (f" · last10 {wins}W" if wins is not None else ""))
    st.update(bot=bot, rating=rating, matches=matches, peak=peak, wins=wins)
    STATE.write_text(json.dumps(st, indent=2))


def run(cmd: list[str], timeout: int) -> tuple[int, str]:
    """nice'd so the keeper always yields to a battery."""
    try:
        p = subprocess.run(["nice", "-n", "15"] + cmd, cwd=ROOT, text=True,
                           capture_output=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"


def cycle(n: int) -> None:
    try:
        ladder_watch()
    except Exception as exc:                              # noqa: BLE001
        log(f"ladder_watch error {type(exc).__name__}: {exc}")

    rc, _ = run([PY, str(ROOT / "tools/monitors/replay_archiver.py")], timeout=900)
    arch = "archiver ok" if rc == 0 else f"archiver rc={rc}"

    la = loadavg()
    if la > LOAD_CEILING:
        log(f"{arch} · DECODE DEFERRED, load {la:.1f} > {LOAD_CEILING} "
            f"(a battery is probably running)")
        return

    args = [PY, str(HERE / "sync.py")]
    if n % NET_EVERY:
        args.append("--no-net")
    rc, out = run(args, timeout=1800)
    line = next((l.strip() for l in out.splitlines() if l.startswith("archive ")), "")
    added = next((l.strip() for l in out.splitlines() if "appended rows" in l), "")
    log(f"{arch} · load {la:.1f} · {line}" + (f" · {added}" if added else ""))


def loop() -> None:
    PIDFILE.write_text(str(os.getpid()))
    log(f"KEEPER START pid={os.getpid()} interval={INTERVAL}s "
        f"load_ceiling={LOAD_CEILING}")
    n = 0
    try:
        while True:
            try:
                cycle(n)
            except Exception as exc:                      # noqa: BLE001
                log(f"CYCLE ERROR {type(exc).__name__}: {exc}")
            n += 1
            time.sleep(INTERVAL)
    finally:
        log("KEEPER STOP")
        PIDFILE.unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", action="store_true", help="detach and run")
    ap.add_argument("--stop", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()

    if a.status:
        pid = read_pid()
        print(f"keeper: {'RUNNING pid ' + str(pid) if pid else 'not running'}")
        if LOG.exists():
            lines = LOG.read_text().splitlines()
            print(f"log: {len(lines)} lines, last 8:")
            for ln in lines[-8:]:
                print("  " + ln)
        return

    if a.stop:
        pid = read_pid()
        if not pid:
            print("keeper: not running")
            return
        os.kill(pid, signal.SIGTERM)
        print(f"keeper: sent SIGTERM to {pid}")
        return

    if a.start:
        if read_pid():
            print(f"keeper: already running (pid {read_pid()})")
            return
        # detach: new session, no controlling terminal, survives the parent shell
        out = open(ROOT / "corpus" / "keeper.out", "a")
        subprocess.Popen([PY, __file__], cwd=ROOT, stdout=out, stderr=out,
                         stdin=subprocess.DEVNULL, start_new_session=True)
        time.sleep(2)
        pid = read_pid()
        print(f"keeper: {'started pid ' + str(pid) if pid else 'FAILED to start'}")
        return

    loop()


if __name__ == "__main__":
    main()
