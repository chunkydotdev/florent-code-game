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

# ⛔ ATOMIC WRITES, s50 2026-08-17. Every whole-file write on the keeper's path
# truncated its target first, so a reader inside the rewrite window got a VALID
# BUT SHORT file and no error — the research lane lost 62% of `meta_join.tsv`'s
# joins that way overnight. See `atomicio.py` for the mechanism and for what is
# deliberately NOT converted (appends).
sys.path.insert(0, str(HERE))
from atomicio import atomic_write_text  # noqa: E402

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
    # APPEND, deliberately not atomic-rewritten: an append never truncates, so
    # the truncation class cannot happen here. One line per call, one write.
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
    # Parsed by the SAME function the selftest drives -- not a second copy here.
    parsed = parse_status(p.stdout)
    if parsed is None:
        return                             # degraded response: write NOTHING
    rating, matches, bot, wins = parsed

    st = json.loads(STATE.read_text()) if STATE.exists() else {}
    alerts, st, should_log = decide(st, rating, matches, bot, wins)
    for title, msg in alerts:
        notify(title, msg)
    if should_log:
        log(f"ladder {bot} · {rating:.1f} @ {matches}"
            + (f" · last10 {wins}W" if wins is not None else ""))
    # ATOMIC: `ship_watch` and the lanes read this state file on their own
    # cadence. Truncate-then-refill made an empty/partial JSON readable, and a
    # partial JSON here reads as "no prior bot" -> a spurious SHIP alert.
    atomic_write_text(STATE, json.dumps(st, indent=2))


def decide(st: dict, rating: float, matches: int, bot: str, wins):
    """PURE. -> (alerts, new_state, should_log). No I/O, so `--selftest` can drive it.

    ⛔ EXTRACTED s33 2026-08-12 BECAUSE THIS LOGIC HAD NO TEST OF ANY KIND. keeper
    ingests the corpus every statistic in this repo is computed on, and the ship
    gate's denominators now sit on it -- 22 cells above it and 0 in it (D24(d)).
    It is `ladder_watch()` that CALLS this, so the selftest drives the shipped
    line and not a copy (D24(e)) -- the mistake made in `replay_throws.py` earlier
    today by the lane writing this.

    ⚠ THE ALERT CHAIN IS `elif`, SO IT IS MUTUALLY EXCLUSIVE AND THAT IS A REAL
    PROPERTY, not an accident: a SHIP that is also a 40-point drop notifies SHIP
    ONLY. Preserved deliberately -- the drop is meaningless across a bot change,
    which is exactly why `peak` resets on a ship. A cell pins both halves.
    """
    peak = max(rating, st.get("peak", rating))
    st = dict(st)
    alerts = []

    if st.get("bot") and bot != st["bot"]:
        alerts.append(("florent: SHIP DETECTED",
                       f"active bot changed {st['bot']} -> {bot} @ {rating:.0f}"))
        # NEW BOT, NEW BASELINE. Without this the incoming bot inherits the
        # outgoing bot's peak and can fire a RATING DROP on its first poll for a
        # decline it had no part in.
        peak = rating
    elif peak - rating >= DROP_ALERT and st.get("alerted_at", 0) != round(rating):
        alerts.append(("florent: RATING DROP",
                       f"{rating:.0f} is {peak - rating:.0f} below peak {peak:.0f} "
                       f"({matches} matches)"))
        st["alerted_at"] = round(rating)
    elif wins is not None and wins <= STREAK_ALERT and st.get("wins") != wins:
        alerts.append(("florent: LOSING STREAK",
                       f"last 10 = {wins}W, rating {rating:.0f}"))

    should_log = st.get("matches") != matches
    st.update(bot=bot, rating=rating, matches=matches, peak=peak, wins=wins)
    return alerts, st, should_log


def parse_status(txt: str):
    """PURE. -> (rating, matches, bot, wins) or None if the response is degraded.

    ⛔ THE `None` RETURN IS THE LOAD-BEARING BRANCH AND IT IS THIS REPO'S MOST
    DIRECT EXPOSURE TO THE DOCUMENTED `fcode status` HAZARD: it EXITS 0 while
    printing `Error: True`, and a degraded body still parses as valid JSON. So
    the gate is the PRESENCE OF THE LOAD-BEARING FIELD, never the exit code --
    and a degraded poll must write NOTHING rather than a partial row.
    """
    m_rate = re.search(r"Rating:\s*([\d.]+).*?(\d+)\s+matches", txt, re.S)
    m_bot = re.search(r"Active bot:\s*(.+)", txt)
    m_last = re.search(r"Last 10:\s*(\d+)W", txt)
    if not (m_rate and m_bot):
        return None
    return (float(m_rate.group(1)), int(m_rate.group(2)),
            m_bot.group(1).strip(), int(m_last.group(1)) if m_last else None)


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

    net_on = (n % NET_EVERY == 0)
    rc, _ = run([PY, str(ROOT / "tools/monitors/replay_archiver.py")], timeout=900)
    arch = "archiver ok" if rc == 0 else f"archiver rc={rc}"

    la = loadavg()
    if la > LOAD_CEILING:
        # ⛔⛔ ROOT CAUSE OF THE 2026-08-12 LADDER-METADATA STALL, and it is a
        # SCOPE bug not a throttle bug. This early return skipped ALL of sync.py,
        # including the LADDER-METADATA NET PULL, which is network-bound and cheap
        # -- the same class of work as the archiver, which this function
        # deliberately runs BEFORE the load check for exactly that reason. The
        # docstring even says "Archiving still runs -- it is network-bound and
        # cheap" and then defers an equally network-bound step.
        # Measured: 156 DEFERRED cycles in this log. With 6+ shards running all
        # day the load sat at 8-10, so nearly every cycle deferred, and the net
        # pull (only eligible on n % NET_EVERY == 0 anyway) almost never landed.
        # ladder_games.tsv reached 8.5h stale and league_matches.tsv 5.8h while
        # every cycle logged a healthy line. ladder_games is the surface CLAUDE.md
        # names as AUTHORITATIVE for every rated denominator.
        # ⇒ The NET pull now runs even when the DECODE is deferred.
        if net_on:
            rcn, outn = run([PY, str(HERE / "sync.py"), "--net-only"], timeout=900)
            got = [l.strip() for l in outn.splitlines()
                   if l.strip().startswith(("ladder_games:", "league_matches:"))]
            log(f"{arch} · DECODE DEFERRED, load {la:.1f} > {LOAD_CEILING} "
                f"· NET PULL STILL RAN" + (" · " + " · ".join(got) if got else
                " · *** NET PULL PRODUCED NO OUTPUT"))
        else:
            log(f"{arch} · DECODE DEFERRED, load {la:.1f} > {LOAD_CEILING} "
                f"(a battery is probably running) · net not due (cycle {n})")
        return

    args = [PY, str(HERE / "sync.py")]
    if not net_on:
        args.append("--no-net")
    rc, out = run(args, timeout=1800)
    line = next((l.strip() for l in out.splitlines() if l.startswith("archive ")), "")
    added = next((l.strip() for l in out.splitlines() if "appended rows" in l), "")
    # ⛔ SAY WHETHER THE NET STEP RAN. It is the ONE step in the cycle that never
    # reported, and it stalls INVISIBLY: on 2026-08-12 ladder_games.tsv sat 8.5h
    # stale and league_matches.tsv 5.8h while every cycle logged a healthy line
    # and the replay-derived tables were fresh to the minute. 1,284 log lines
    # contained ZERO mentions of the ladder-metadata pull, so its success and its
    # failure looked identical from outside -- and `ladder_games.tsv` is the
    # surface CLAUDE.md names as authoritative for every rated denominator.
    # Magnus asked why it was stale; this is the line that would have answered it.
    log(f"{arch} · load {la:.1f} · net={'ON' if net_on else 'skipped'}"
        f"(cycle {n} % {NET_EVERY}) · {line}" + (f" · {added}" if added else ""))

    # THE LOG LINE ABOVE IS TWO GREPS, AND EVERYTHING ELSE sync PRINTS IS
    # DISCARDED. That was fine while sync only appended rows. It stopped being
    # fine the moment sync gained a step that can REFUSE (meta_join, 2026-08-09):
    # the refusal was written to be loud, and it was — to a human running sync by
    # hand. Under the keeper, the only thing that runs sync unattended, it went
    # into a discarded stdout. Same shape as ship_watch the same evening: an
    # alarm on a channel nobody reads. Flagged by the research arm.
    for l in out.splitlines():
        s = l.strip()
        if "REFUSED" in s:
            log(f"  *** {s}")
        elif s.startswith(("meta_join:", "league_matches:", "ladder_games:")):
            log(f"  {s}")
    # A net cycle that produced NEITHER table line is a SILENT FAILURE, which is
    # exactly the state that went unnoticed for 8.5 hours. Say so.
    if net_on and not any(l.strip().startswith(("ladder_games:", "league_matches:"))
                          for l in out.splitlines()):
        log("  *** NET STEP RAN AND PRODUCED NO ladder_games/league_matches LINE "
            "-- ladder metadata is NOT being refreshed. Run "
            ".venv/bin/python tools/corpus/sync.py by hand and read its output.")


def loop() -> None:
    # ATOMIC: the pidfile is the ONLY handle a restart has on this process
    # (`--stop`, and the documented restart procedure). A reader that catches it
    # empty concludes "not running" and a second keeper gets started on top.
    atomic_write_text(PIDFILE, str(os.getpid()))
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


def selftest() -> int:
    """Forced-answer cells for keeper's decision branches.

    D24(d) -- `enumerate BRANCHES, not cells`. keeper had ZERO of either while
    the instruments reading its output had 22, which is D20 one level up: a
    compensating check downstream is how an untested writer survives.
    """
    fails = []

    def check(name, cond, detail=""):
        print(f"  [{'ok' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
        if not cond:
            fails.append(name)

    OK = "Active bot: v114\nRating: 1650.0 (795 matches)\nLast 10: 6W 4L\n"

    # --- parse_status: the degraded-response branch, both ways.
    p = parse_status(OK)
    check("a well-formed status parses all four fields", p == (1650.0, 795, "v114", 6), f"{p}")
    check("⛔ `Error: True` with NO rating returns None (writes nothing)",
          parse_status("Error: True\n") is None)
    check("⛔ a body with a rating but NO active bot returns None",
          parse_status("Rating: 1650.0 (795 matches)\n") is None)
    check("a status without `Last 10` still parses, wins=None",
          parse_status("Active bot: v114\nRating: 1650.0 (795 matches)\n")[3] is None)

    # --- decide: SHIP.
    a, st, _ = decide({"bot": "v112", "peak": 1700.0}, 1650.0, 795, "v114", 6)
    check("a bot change notifies SHIP DETECTED", any("SHIP" in t for t, _ in a))
    check("⭐ a ship RESETS peak to the new rating", st["peak"] == 1650.0,
          f"peak={st['peak']}")
    check("...and a ship that is ALSO a 50-point drop notifies SHIP ONLY (elif is deliberate)",
          len(a) == 1 and "SHIP" in a[0][0], f"{[t for t, _ in a]}")

    # --- decide: DROP, driven to fire and to stay silent.
    a2, st2, _ = decide({"bot": "v114", "peak": 1700.0}, 1650.0, 795, "v114", 6)
    check("a 50-point drop from peak notifies RATING DROP", any("DROP" in t for t, _ in a2))
    a3, _, _ = decide({"bot": "v114", "peak": 1670.0}, 1650.0, 795, "v114", 6)
    check("a 20-point drop is BELOW the 25 threshold and is SILENT", not a3,
          f"{[t for t, _ in a3]}")
    a4, _, _ = decide({"bot": "v114", "peak": 1700.0, "alerted_at": 1650}, 1650.0, 795, "v114", 6)
    check("the SAME rating does not re-alert", not any("DROP" in t for t, _ in a4))

    # --- decide: STREAK, both ways.
    a5, _, _ = decide({"bot": "v114", "peak": 1650.0, "wins": 5}, 1650.0, 795, "v114", 2)
    check("last-10 at 2W notifies LOSING STREAK", any("STREAK" in t for t, _ in a5))
    a6, _, _ = decide({"bot": "v114", "peak": 1650.0, "wins": 5}, 1650.0, 795, "v114", 3)
    check("last-10 at 3W is above the threshold and is SILENT",
          not any("STREAK" in t for t, _ in a6))
    a7, _, _ = decide({"bot": "v114", "peak": 1650.0, "wins": 2}, 1650.0, 795, "v114", 2)
    check("an UNCHANGED streak does not re-alert", not a7)

    # --- a healthy poll must be completely silent. Without this the alerts could
    # all be firing constantly and every cell above would still pass.
    a8, _, lg = decide({"bot": "v114", "peak": 1650.0, "wins": 6, "matches": 795},
                       1655.0, 795, "v114", 6)
    check("⭐ a healthy poll raises NOTHING", not a8, f"{[t for t, _ in a8]}")
    check("...and does not re-log an unchanged match count", not lg)
    _, _, lg2 = decide({"bot": "v114", "peak": 1650.0, "matches": 795},
                       1655.0, 796, "v114", 6)
    check("a new match DOES log", lg2)

    # --- peak is a high-water mark, never lowered by a good poll.
    _, st9, _ = decide({"bot": "v114", "peak": 1700.0}, 1650.0, 795, "v114", 6)
    check("peak is a high-water mark and is not lowered by a lower rating",
          st9["peak"] == 1700.0, f"peak={st9['peak']}")

    # --- first-ever poll: no prior bot, so no spurious SHIP.
    a10, st10, _ = decide({}, 1650.0, 795, "v114", 6)
    check("the FIRST poll (no prior state) does not fire a spurious SHIP", not a10)
    check("...and seeds peak from the current rating", st10["peak"] == 1650.0)

    print()
    if fails:
        print(f"SELFTEST FAILED: {len(fails)}: {', '.join(fails)}")
        return 1
    print("SELFTEST PASSED — every alert branch driven to FIRE and to STAY SILENT,\n"
          "the degraded-response gate returns None, and a healthy poll raises nothing.")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", action="store_true", help="detach and run")
    ap.add_argument("--stop", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        raise SystemExit(selftest())

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
