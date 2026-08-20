#!/usr/bin/env python3
r"""REMOTE BUILD BATTERY — run a build-agent verification grid on ws1/ws2.

    tools/remote_battery.py --arm A=bots/_v530home --arm B=scratchpad/x/arms/parent \\
        --opp bots/_v488beltbreak2 \\
        --maps atoll,drakkarfjord,glacierkeep,midgard,nordkap \\
        --seeds 1-39 --block-size 3 --par 2 \\
        --hosts work-server-1,work-server-2 \\
        --out scratchpad/s52_thing/grid

    tools/remote_battery.py ... --hosts local        # same driver, this box
    tools/remote_battery.py --selftest               # offline, no host touched
    tools/remote_battery.py ... --dry-run            # plan + preflight, no ship

WHAT IT IS. `scratchpad/*_build/run_grid.py` is the build agent's verification
battery: N arms x MAPS x SEEDS x 2 seats, arms run CONCURRENTLY on the SAME
seeds (interleaved blocks), one tape per arm, consumed by that build's
`summarise.py`. It has only ever run on this box. This ships the same grid to
the two VPS workers, which roughly halves build wall-time and frees the mac.

⭐ THE OUTPUT IS run_grid.py's TAPE, BYTE-FORMAT-IDENTICAL, ON PURPOSE:
      tag map seed seat ours winner cond turn tracebacks ours_mined opp_mined
  same header, same `tag = <map>_s<seed>_<A|B>`, same `ours` in {US,OPP,NONE},
  same `Winner:` and `Titanium ... (N mined)` regexes, same job order. So
  `summarise.py <name> <tape>` consumes a remote tape unchanged. The driver
  below is a transcription of `run_grid.py:one()`; if that file's row format
  ever changes, this must change with it (there is a FORMAT selftest, but a
  selftest cannot notice a change made in the other file).

═══════════════════════════════════════════════════════════════════════════════
⛔ NAMESPACE PROOF — WHY auto_gate CANNOT SEE THIS, AND WHY THAT MATTERED
═══════════════════════════════════════════════════════════════════════════════
Since a50f27ef (s48) `auto_gate.py --apply` STOPS remote shards for real — its
arithmetic-futility floors BIND on anything it discovers under the remote pull
root. A build battery is not a corefill shard: it has no BAR row, its n is 30-
500 not 5,400, and a 24-game format check sitting at 33% would look exactly like
an arm the gate should kill. So the requirement is not "be careful", it is
"be in a namespace the census cannot enumerate". Read off the discovery code,
not off intent:

  * `tools/auto_gate.py:326  DEFAULT_REMOTE_ROOT = REPO/"scratchpad/overnight-remote"`
    `:610  scan_remote()` — `for hostdir in remote_root.iterdir() if is_dir()`
    then `for tsv in hostdir.glob("*.tsv")`. **Non-recursive, one level deep,
    rooted at that constant.** Our tapes land in
    `scratchpad/build_batteries/<host>/<runid>/` — a DIFFERENT root — so no
    iteration ever reaches them. (Even had we used the same root, a second
    directory level would already be invisible to that glob; we do not rely on
    that, because relying on it would make an accidental flattening fatal.)
  * `:324-325  DEFAULT_WORKLIST = scratchpad/corefill_work.txt`,
    `DEFAULT_TSVDIR = scratchpad/overnight`; `:553 scan_local()` iterates the
    SHARD IDS IN THAT WORKLIST and opens `tsvdir/<sid>.tsv`. A tape we never
    name in that worklist and never place in that directory is unreachable by
    construction — it is not filtered out, it is never looked for.
  * The daemon runs with those defaults: `ps` shows
    `.venv/bin/python tools/auto_gate.py --apply` (pid 61319, 2026-08-20) —
    no `--remote-root`, no `--tsvdir`, no `--worklist`.
  * Same story for the other readers: `corefill_status.sh:74` globs
    `scratchpad/overnight-remote/*/${SH}.tsv` for a shard id it already holds;
    `overnight_read.py --include-remote` reads the same pull root.
  ⇒ VERIFIED EMPIRICALLY TOO, not just by reading: run
    `.venv/bin/python tools/auto_gate.py --dry-run --all` before and after a
    battery and diff the shard list. It is unchanged (validation §2 in the
    handover message).

⛔ AND THE SAME SEPARATION ON THE HOST. corefill lives in `~/fcode-worker`;
   we live in `~/fcode-build/<runid>`. We never write `work/worklist.txt`,
   `results/`, `STOP`, or any `.COMPLETE` marker over there. We do READ
   `~/fcode-worker/.venv/bin/fcode` — executing the pinned engine binary is not
   state. `orchestrate.sh kill` is `pkill -f 'tools/vps/worker.sh'` and its push
   guard counts `[w]orker\.sh`; our driver is `driver.py` under a different
   root, so neither tool can see us and we cannot be killed by a corefill stop.

⛔ THE RESIDUAL RACE, STATED BECAUSE IT IS NOT CLOSED. `fleet_dispatch.py
   --once --remote-mode live` (pid 40200) may `start` a corefill worker on a
   host at any 5-minute tick. Its G7 refusal counts `worker.sh` processes — it
   CANNOT see our `fcode run` children, and it does not honour
   `scratchpad/fleet_hold` (only `remote_cancel.py`/`auto_gate.py` do). If it
   dispatches onto a host running a battery, both fixtures are oversubscribed
   and `--tle 10` is WALL-CLOCK, so rows are CORRUPTED, not merely slowed (the
   SALTREF2 condition). We refuse to start on a host that already has a live
   worker, and we PRINT the queue depth so the operator can see whether a
   dispatch is possible; we do not write a hold marker, because that is
   corefill's coordination surface and this tool does not touch it.
   ⇒ Before a long battery, check `scratchpad/fleet_queue.tsv` has no QUEUED
     rows, or stop fleet_dispatch for the duration.

═══════════════════════════════════════════════════════════════════════════════
LOAD DISCIPLINE
═══════════════════════════════════════════════════════════════════════════════
Concurrency is `len(arms) * PAR` — every arm in a block runs at once, each with
PAR threads. That product, not PAR, is the number of busy cores. It is checked
against `scratchpad/vps/host_capacity.tsv` **our_cores** (ws1 = 10, NOT its
nproc of 16; ws2 = 6) and REFUSED above it. `nproc` is the wrong instrument and
overstates ws1 by 60%; oversubscription moved a byte-identical null 2.67pp.

═══════════════════════════════════════════════════════════════════════════════
SEEDS, BLOCKS AND WHAT SPLITTING ACROSS HOSTS DOES AND DOES NOT COST
═══════════════════════════════════════════════════════════════════════════════
Blocks are assigned to hosts round-robin, and a block goes WHOLLY to one host.
So every cross-arm comparison is within-block and therefore within-host: a
host-speed difference cannot bias one arm against another, which is the only
property the interleaving exists to buy. Seeds are explicit here (no crc32
offset — that is corefill's device for hosts running the SAME shard); the tool
asserts the blocks partition the seed list, so no seed is ever played twice.

⭐ CROSS-HOST DETERMINISM: MEASURED, AND IT HOLDS. `--tle 10` is a WALL-CLOCK
  budget, so a faster or slower core can change WHICH TURNS TIME OUT and a
  same-seed game could legitimately diverge between hosts — that is why this was
  tested rather than assumed. Measured 2026-08-20 on NOISE_OFF copies of
  `_v530home` / `_v529merge` vs a NOISE_OFF `_v488beltbreak2`, 2 maps x 3 seeds
  x 2 seats = 12 rows per arm:

      det_home   local vs ws1 / local vs ws2 / ws1 vs ws2 :  0 of 12 rows differ
      det_merge  local vs ws1 / local vs ws2 / ws1 vs ws2 :  0 of 12 rows differ

  compared on ALL ELEVEN COLUMNS, not just winner/cond/turn. Load differed
  across the legs (mac at load 5.7 with another lane's battery running, ws1
  0.59, ws2 0.16) and the rows still matched.
  ⛔ THE CONTROL, because a diff that has only ever printed 0 has not been seen
  to check: the SAME comparison on NOISE_ON arms, same host, same seeds, run
  twice, reports 11/12 and 12/12 rows DIFFERENT. And a one-digit mutation of a
  `turn` value is caught. The instrument can produce the other verdict.
  ⚠ SCOPE: these arms never came near the 10 ms budget (0 tracebacks, no
  timeouts anywhere). An arm that sits ON the CPU limit could still diverge
  between hosts, because that is the one mechanism a wall-clock budget exposes.
  Re-run the check for such an arm before pooling its rows.

⚠ NO REPLAYS COME BACK. Remote games run `--replay /dev/null` (as worker.sh
  does). A build phase that needs replays or per-game stdout/stderr must run
  LOCALLY. This tool is for the row-counting phases: headline grids, dose
  panels, ablation batteries.

═══════════════════════════════════════════════════════════════════════════════
PASTE THIS INTO A BUILD BRIEF
─────────────────────────────
  Verification batteries may run on the VPS workers instead of this box:
  `tools/remote_battery.py --arm NAME=<tree> --arm NAME=<tree> --opp <tree>
  --maps a,b,c --seeds 1-39 --block-size 3 --par N --hosts
  work-server-1,work-server-2 --out <build>/grid`. It ships the trees and maps,
  runs the SAME interleaved grid (arms concurrent on shared seeds, blocks split
  round-robin across hosts, a block never split), and pulls back one tape per
  arm in run_grid.py's exact format, so `summarise.py <name> <out>/<arm>.tsv`
  consumes it unchanged. `--par` is PER ARM: keep `arms x par <= 10` on ws1 and
  `<= 6` on ws2 — the tool refuses above that. It refuses to start on a host
  with a live corefill worker, writes nothing into `fcode-worker/` or any
  auto_gate-scanned path, and cleans its remote scratch. On any shortfall it
  writes `<out>/PARTIAL`, reports delivered-vs-planned rows PER ARM, and exits
  2 — a short tape is never presented as a complete battery. Two limits:
  NO REPLAYS AND NO PER-GAME STDOUT come back (phases that need them stay
  local), and `fleet_dispatch --remote-mode live` can still start corefill on a
  host mid-battery, so check `scratchpad/fleet_queue.tsv` is drained first.
  Reap orphans from a killed wrapper with `--gc`.

═══════════════════════════════════════════════════════════════════════════════
FAILURE REPORTING — the s48 lesson, mechanised
═══════════════════════════════════════════════════════════════════════════════
A partial tape is NEVER presented as a complete one. Every run writes
`<out>/RESULT.txt` with planned vs delivered rows PER ARM PER HOST, and on any
shortfall it also writes `<out>/PARTIAL` and exits 2. A host that dies, is
killed, or is unreachable produces a LOUD error and a nonzero exit; it never
produces a silent empty tape. Exit codes: 0 complete, 2 partial, 3 preflight
refusal, 4 transport/host failure.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP_F = os.path.join(REPO, "scratchpad/vps/host_capacity.tsv")
PIN_F = os.path.join(REPO, "tools/ENGINE_PIN")
QUEUE_F = os.path.join(REPO, "scratchpad/fleet_queue.tsv")
LOCAL_PULL_ROOT = os.path.join(REPO, "scratchpad/build_batteries")

# ⛔ HARD SEPARATION FROM COREFILL. Asserted, not merely defaulted.
COREFILL_ROOT = "fcode-worker"
REMOTE_BUILD_ROOT = os.environ.get("REMOTE_BUILD_ROOT", "fcode-build")

HDR = ("tag map seed seat ours winner cond turn tracebacks "
       "ours_mined opp_mined").split()

SSH = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10"]

# ═════════════════════════════════════════════════════════════════════════════
# THE REMOTE DRIVER. Transcribed from scratchpad/*_build/run_grid.py:one().
# Written to the host as driver.py. Must stay python3.6+ clean: ws1 is 3.9.2.
# ═════════════════════════════════════════════════════════════════════════════
DRIVER = r'''#!/usr/bin/env python3
"""Shipped by tools/remote_battery.py. Runs the interleaved grid on this host.

Row format is run_grid.py's, deliberately byte-identical. Blocks run in order;
within a block every arm runs CONCURRENTLY on the same seeds, each arm with PAR
threads. One tape per (block, arm): out/b<i>/<arm>.tsv.
"""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.abspath(__file__))
SPEC = json.load(open(os.path.join(ROOT, "spec.json")))
FC = SPEC["fcode"]
OPP = os.path.join(ROOT, "opp", SPEC["opp_name"])
PAR = SPEC["par"]
HB = os.path.join(ROOT, "HEARTBEAT")
HDR = ("tag map seed seat ours winner cond turn tracebacks "
       "ours_mined opp_mined").split()


def one(job):
    armdir, armname, mp, seed, ord_a = job
    tag = "%s_s%d_%s" % (mp, seed, "A" if ord_a else "B")
    first, second = (armdir, OPP) if ord_a else (OPP, armdir)
    cmd = [FC, "run", first, second,
           os.path.join(ROOT, "maps", mp + ".map26"),
           "--seed", str(seed), "--tle", "10", "--replay", "/dev/null"]
    try:
        pr = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            universal_newlines=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return "\t".join([tag, mp, str(seed), "A" if ord_a else "B",
                          "NONE", "TIMEOUT", "-", "-1", "0", "-1", "-1"])
    out, err = pr.stdout, pr.stderr
    win, turn, cond = "NOWINNER", -1, "-"
    for line in out.splitlines():
        if "Winner:" in line:
            m = re.search(r"Winner:\s+(\S+)\s+\((.*), turn (\d+)\)", line)
            if m:
                win, cond, turn = m.group(1), m.group(2), int(m.group(3))
            break
    mined_a = mined_b = -1
    m = re.search(r"Titanium\s+(\d+)\s+\((\d+) mined\)\s+(\d+)\s+\((\d+) mined\)",
                  out)
    if m:
        mined_a, mined_b = int(m.group(2)), int(m.group(4))
    ours_mined = mined_a if ord_a else mined_b
    opp_mined = mined_b if ord_a else mined_a
    ours = "US" if armname == win else ("OPP" if win != "NOWINNER" else "NONE")
    tb = len(re.findall(r"Traceback", err))
    return "\t".join(str(x) for x in [
        tag, mp, seed, "A" if ord_a else "B", ours, win, cond,
        turn, tb, ours_mined, opp_mined])


def rows_done():
    n = 0
    for b in SPEC["blocks"]:
        d = os.path.join(ROOT, "out", "b%d" % b["index"])
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if f.endswith(".tsv"):
                with open(os.path.join(d, f)) as fh:
                    n += max(0, sum(1 for _ in fh) - 1)
    return n


def beat(state):
    with open(HB, "w") as fh:
        fh.write("%s\t%d\t%d\t%s\n" % (
            time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            rows_done(), SPEC["planned_rows"], state))


def run_arm(block, arm, outdir):
    jobs = []
    for mp in SPEC["maps"]:
        for seed in block["seeds"]:
            for ord_a in (True, False):
                jobs.append((os.path.join(ROOT, "arms", arm), arm, mp, seed,
                             ord_a))
    tmp = os.path.join(outdir, arm + ".partial")
    with open(tmp, "w") as fh:
        fh.write("\t".join(HDR) + "\n")
        fh.flush()
        with ThreadPoolExecutor(max_workers=PAR) as ex:
            for r in ex.map(one, jobs):
                fh.write(r + "\n")
                fh.flush()
    # ⛔ RENAME LAST. A tape only gets its real name once every one of its games
    # has been written, so a killed driver leaves a *.partial that the puller
    # reports as short rather than a short-but-plausible <arm>.tsv.
    os.rename(tmp, os.path.join(outdir, arm + ".tsv"))


def main():
    beat("STARTING")
    # ⛔ A HEARTBEAT THAT ONLY TICKS PER BLOCK CANNOT TELL WORKING FROM WEDGED.
    # With one block per host it read STARTING for the entire run. This repo's
    # signature defect is a monitor whose healthy line and blind line are
    # byte-identical (ship_watch on a stale tape; SALTREF2 asleep vs dead).
    # 30 s ticks with a live row count, so the age AND the number both move.
    import threading
    _stop = threading.Event()

    def _ticker():
        while not _stop.wait(30):
            try:
                beat("RUNNING")
            except Exception:
                pass
    threading.Thread(target=_ticker, daemon=True).start()
    for block in SPEC["blocks"]:
        outdir = os.path.join(ROOT, "out", "b%d" % block["index"])
        os.makedirs(outdir, exist_ok=True)
        if all(os.path.exists(os.path.join(outdir, a + ".tsv"))
               for a in SPEC["arms"]):
            continue
        procs = []
        import threading
        errs = []

        def go(a):
            try:
                run_arm(block, a, outdir)
            except Exception as e:          # noqa: BLE001 - reported, not raised
                errs.append("%s b%d: %r" % (a, block["index"], e))
        for a in SPEC["arms"]:
            t = threading.Thread(target=go, args=(a,))
            t.start()
            procs.append(t)
        for t in procs:
            t.join()
        beat("RUNNING")
        if errs:
            sys.stderr.write("ARM ERRORS: %s\n" % "; ".join(errs))
    # ⛔ COMPLETE MUST CERTIFY TAPES, NOT LOOP ITERATIONS. The first live run
    # wrote COMPLETE after every arm had raised, delivering 0 of 24 rows with a
    # healthy-looking state word.
    want = [os.path.join(ROOT, "out", "b%d" % b["index"], a + ".tsv")
            for b in SPEC["blocks"] for a in SPEC["arms"]]
    _stop.set()
    absent = [p for p in want if not os.path.exists(p)]
    if absent:
        beat("FAILED")
        sys.stderr.write("MISSING TAPES (%d of %d): %s\n"
                         % (len(absent), len(want),
                            " ".join(os.path.basename(p) for p in absent[:10])))
        sys.exit(1)
    beat("COMPLETE")


if __name__ == "__main__":
    main()
'''


# ═════════════════════════════════════════════════════════════════════════════
# helpers
# ═════════════════════════════════════════════════════════════════════════════
def say(msg):
    sys.stderr.write("%s %s\n" % (time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                time.gmtime()), msg))
    sys.stderr.flush()


def die(msg, code=3):
    say(msg)
    sys.exit(code)


def parse_seeds(spec):
    """'1-39' or '1,2,3' or '1-9,20' -> sorted unique ints."""
    out = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part[1:]:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    seen, ordered = set(), []
    for s in out:
        if s not in seen:
            seen.add(s)
            ordered.append(s)
    return ordered


def host_cores(host, cap_file=CAP_F):
    """our_cores from host_capacity.tsv, matched on the BARE hostname.

    ⛔ Never nproc. The table is keyed `worker@work-server-1` while callers type
    either form; orchestrate.sh's first cut compared literally and refused every
    cell. Strip the user prefix on both sides.
    """
    bare = host.split("@")[-1]
    if not os.path.exists(cap_file):
        return None
    for line in open(cap_file):
        if line.startswith("#") or not line.strip():
            continue
        f = line.split()
        if len(f) >= 3 and f[0].split("@")[-1] == bare:
            try:
                return int(f[2])
            except ValueError:
                return None
    return None


def engine_pin():
    txt = [l for l in open(PIN_F) if not l.startswith("#")]
    return "".join(txt).strip()


def make_blocks(seeds, block_size, hosts):
    blocks = []
    for i in range(0, len(seeds), block_size):
        idx = len(blocks)
        blocks.append({"index": idx, "seeds": seeds[i:i + block_size],
                       "host": hosts[idx % len(hosts)]})
    # partition assertion: every seed exactly once
    flat = [s for b in blocks for s in b["seeds"]]
    assert sorted(flat) == sorted(seeds) and len(flat) == len(set(flat)), \
        "blocks do not partition the seed list"
    return blocks


# ═════════════════════════════════════════════════════════════════════════════
# transport (ssh/rsync, or local)
# ═════════════════════════════════════════════════════════════════════════════
# ssh on this box prints a post-quantum advisory to stderr on every connection.
# We merge stderr into stdout (a transport error is diagnostic and must not be
# thrown away), so the banner would otherwise land inside every reported line —
# it already swallowed a `cleanup ... CLEANED` line whole during validation.
_BANNER = ("post-quantum", "store now, decrypt later", "openssh.com/pq",
           "** WARNING:", "** This session", "** The server may need")


def _scrub(txt):
    if not txt:
        return txt
    return "\n".join(l for l in txt.splitlines()
                     if not any(b in l for b in _BANNER))


def sh(cmd, timeout=120):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       universal_newlines=True, timeout=timeout)
    return p.returncode, _scrub(p.stdout)


def r_exec(host, cmdstr, timeout=120):
    if host == "local":
        return sh(["bash", "-c", cmdstr], timeout)
    return sh(SSH + [host, cmdstr], timeout)


def r_push(host, src, dst):
    if host == "local":
        os.makedirs(os.path.dirname(dst.rstrip("/")) or "/", exist_ok=True)
        return sh(["rsync", "-a", "--chmod=u+rwX", "--exclude", "__pycache__",
                   "--exclude", "*.pyc", src, dst], 600)
    # ⛔ --chmod=u+rwX IS LOAD-BEARING, NOT TIDINESS. Frozen bot trees here are
    # mode dr-xr-xr-x / -r--r--r-- on purpose, and `rsync -a` preserves that, so
    # the remote copy lands in a directory its owner cannot unlink from: the
    # first live run's cleanup failed with "Permission denied" on every opp file
    # and LEFT SCRATCH ON THE HOST. We copy the bytes, not the write-protection.
    return sh(["rsync", "-a", "--chmod=u+rwX", "--exclude", "__pycache__",
               "--exclude", "*.pyc", "-e",
               "ssh -o BatchMode=yes -o ConnectTimeout=10", src,
               "%s:%s" % (host, dst)], 600)


def r_pull(host, src, dst):
    if host == "local":
        return sh(["rsync", "-a", src, dst], 600)
    return sh(["rsync", "-a", "-e",
               "ssh -o BatchMode=yes -o ConnectTimeout=10",
               "%s:%s" % (host, src), dst], 600)


def remote_root(host, runid):
    if host == "local":
        return os.path.join(LOCAL_PULL_ROOT, "_localrun", runid)
    return "%s/%s" % (REMOTE_BUILD_ROOT, runid)


# ═════════════════════════════════════════════════════════════════════════════
# preflight
# ═════════════════════════════════════════════════════════════════════════════
def preflight_local(arms, opp, maps, seeds, par, hosts):
    names = {}
    for name, path in arms:
        p = os.path.join(REPO, path) if not os.path.isabs(path) else path
        if not os.path.exists(os.path.join(p, "main.py")):
            die("⛔ REFUSING: arm %s (%s) has no main.py" % (name, path))
        b = os.path.basename(p.rstrip("/"))
        if b in names:
            die("⛔ REFUSING: two arms share the basename %r (%s and %s). "
                "`ours` is decided by basename == winner, so their rows would "
                "be indistinguishable." % (b, names[b], path))
        names[b] = path
    oppp = os.path.join(REPO, opp) if not os.path.isabs(opp) else opp
    if not os.path.exists(os.path.join(oppp, "main.py")):
        die("⛔ REFUSING: opponent %s has no main.py" % opp)
    if os.path.basename(oppp.rstrip("/")) in names:
        die("⛔ REFUSING: opponent basename collides with an arm basename")
    for m in maps:
        if not os.path.exists(os.path.join(REPO, "maps", m + ".map26")):
            die("⛔ REFUSING: maps/%s.map26 does not exist here" % m)
    if not seeds:
        die("⛔ REFUSING: empty seed list")
    conc = len(arms) * par
    for h in hosts:
        if h == "local":
            continue
        cores = host_cores(h)
        if cores is None:
            die("⛔ REFUSING: %s has no row in %s. Add its ALLOCATION (not its "
                "nproc) before running." % (h, CAP_F))
        if conc > cores:
            die("⛔ REFUSING: %d arms x PAR=%d = %d concurrent games exceeds our "
                "allocation of %d cores on %s. --tle 10 is WALL-CLOCK, so "
                "oversubscription CORRUPTS rows (SALTREF2: a byte-identical "
                "null moved 2.67pp). Lower --par or split the arms."
                % (len(arms), par, conc, cores, h))
        say("capacity: %s  arms=%d x par=%d = %d <= our_cores %d  OK"
            % (h, len(arms), par, conc, cores))
    return list(names)


def preflight_host(host, pin):
    """Reachable, pinned engine, idle of corefill. BLIND is never PASSED."""
    if host == "local":
        fc = os.path.join(REPO, ".venv/bin/fcode")
        rc, out = sh([fc, "--version"], 60)
        have = re.search(r"fcode, version ([0-9.]+)", out or "")
        if not have:
            die("⛔ REFUSING: cannot parse a version from local fcode", 4)
        if have.group(1) != pin:
            die("⛔ REFUSING: local fcode %s != pin %s" % (have.group(1), pin))
        return {"fcode": fc, "cores": None, "nproc": None, "load": None,
                "workers": 0}
    probe = ("echo HOME=$HOME; "
             "echo NPROC=$(nproc 2>/dev/null || echo UNKNOWN); "
             "echo LOAD=$(cut -d' ' -f1 /proc/loadavg 2>/dev/null || echo UNKNOWN); "
             "echo WORKERS=$(ps ax -o command= 2>/dev/null | grep -cw '[w]orker\\.sh'; true); "
             "echo RUNNERS=$(ps ax -o command= 2>/dev/null | grep -c '[f]code run'; true); "
             "echo FC=$(ls %s/.venv/bin/fcode 2>/dev/null); "
             "%s/.venv/bin/fcode --version 2>/dev/null | sed -n 's/^fcode, version /VER=/p'"
             % (COREFILL_ROOT, COREFILL_ROOT))
    rc, out = r_exec(host, probe, 90)
    if out is None:
        die("⛔ HOST UNREACHABLE: %s (no output at all). This is a transport "
            "failure, not an empty result." % host, 4)
    kv = dict(l.split("=", 1) for l in out.splitlines() if "=" in l)
    if "VER" not in kv:
        die("⛔ REFUSING: %s — could not read an fcode version. Output was:\n%s\n"
            "BLIND IS NOT PASSED. (Is the host up? Is %s/.venv present?)"
            % (host, out.strip()[-500:], COREFILL_ROOT), 4)
    if kv["VER"].strip() != pin:
        die("⛔ REFUSING: %s has fcode %s, the pin is %s. Two engine versions "
            "are two fixtures wearing one name and the rows are byte-identical."
            % (host, kv["VER"].strip(), pin))
    workers = int(kv.get("WORKERS", "0") or 0)
    runners = int(kv.get("RUNNERS", "0") or 0)
    if workers > 0:
        die("⛔ REFUSING: %s has %d live corefill worker(s) (and %d fcode run "
            "children). Adding a battery on top oversubscribes the box and "
            "--tle 10 is WALL-CLOCK, so BOTH fixtures' rows would be corrupted."
            % (host, workers, runners))
    say("host %s: nproc=%s load=%s corefill_workers=0 fcode=%s(pin ok)"
        % (host, kv.get("NPROC"), kv.get("LOAD"), kv["VER"].strip()))
    # ⛔ AN ABSOLUTE PATH, RESOLVED HERE. The driver calls the engine through
    # subprocess WITHOUT a shell, so `$HOME/...` is a literal filename that
    # cannot exist — the first live run delivered 0 of 24 rows to exactly that.
    home = kv.get("HOME", "").strip()
    if not home.startswith("/"):
        die("⛔ REFUSING: %s did not report an absolute $HOME (%r). The engine "
            "path must be absolute: the driver runs it without a shell."
            % (host, home), 4)
    fcpath = "%s/%s/.venv/bin/fcode" % (home, COREFILL_ROOT)
    rc, out2 = r_exec(host, "test -x '%s' && echo OK" % fcpath, 60)
    if "OK" not in (out2 or ""):
        die("⛔ REFUSING: %s is not executable on %s. BLIND is not PASSED."
            % (fcpath, host), 4)
    return {"fcode": fcpath,
            "cores": host_cores(host), "nproc": kv.get("NPROC"),
            "load": kv.get("LOAD"), "workers": workers}


def queue_warning():
    if not os.path.exists(QUEUE_F):
        return
    q = 0
    for line in open(QUEUE_F):
        if line.startswith("#") or not line.strip():
            continue
        if "\tQUEUED" in line or line.split("\t")[-1].strip() == "QUEUED":
            q += 1
    if q:
        say("⚠ scratchpad/fleet_queue.tsv has %d QUEUED row(s). fleet_dispatch "
            "--remote-mode live may `start` a corefill worker on a host MID-"
            "BATTERY; its G7 cannot see our fcode run children. Drain the "
            "queue or stop fleet_dispatch for the duration." % q)


# ═════════════════════════════════════════════════════════════════════════════
# ship / launch / poll / pull
# ═════════════════════════════════════════════════════════════════════════════
def stage(stagedir, arms, opp, maps):
    """Build the snapshot ONCE, locally, so each host costs ONE rsync.

    ⛔ MEASURED, NOT PREFERRED: the first cut pushed each arm, the opponent and
    each map as its own rsync — twelve ssh handshakes per host, done for one
    host and then the other. A 120-game split battery spent 92 s shipping for
    ~50 s of games, i.e. the transport was the majority of a run this tool
    exists to make faster. One staged tree, one rsync, hosts in parallel.
    """
    if os.path.isdir(stagedir):
        shutil.rmtree(stagedir)
    for sub in ("arms", "opp", "maps", "out"):
        os.makedirs(os.path.join(stagedir, sub))
    names = []
    for _name, path in arms:
        p = path if os.path.isabs(path) else os.path.join(REPO, path)
        b = os.path.basename(p.rstrip("/"))
        shutil.copytree(p, os.path.join(stagedir, "arms", b),
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        names.append(b)
    oppp = opp if os.path.isabs(opp) else os.path.join(REPO, opp)
    oppname = os.path.basename(oppp.rstrip("/"))
    shutil.copytree(oppp, os.path.join(stagedir, "opp", oppname),
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for m in maps:
        shutil.copy(os.path.join(REPO, "maps", m + ".map26"),
                    os.path.join(stagedir, "maps"))
    with open(os.path.join(stagedir, "driver.py"), "w") as fh:
        fh.write(DRIVER)
    # Frozen bot trees are mode dr-xr-xr-x here; copytree preserves that and the
    # stage dir then cannot be removed. Copy the bytes, not the write-protection.
    for d, subdirs, files in os.walk(stagedir):
        for n in subdirs + files:
            p = os.path.join(d, n)
            try:
                os.chmod(p, os.stat(p).st_mode | 0o200)
            except OSError:
                pass
    return names, oppname


def ship(host, runid, stagedir, armnames, oppname, maps, blocks, par, fc,
         planned):
    root = remote_root(host, runid)
    assert COREFILL_ROOT not in root, "REFUSING: build root overlaps corefill"
    spec = {"arms": armnames, "opp_name": oppname, "maps": maps, "par": par,
            "blocks": [{"index": b["index"], "seeds": b["seeds"]}
                       for b in blocks if b["host"] == host],
            "planned_rows": planned, "fcode": fc}
    with open(os.path.join(stagedir, "spec.json"), "w") as fh:
        json.dump(spec, fh, indent=1)
    rc, out = r_exec(host, "mkdir -p '%s'" % root, 60)
    if rc != 0:
        die("⛔ cannot create %s on %s:\n%s" % (root, host, out), 4)
    rc, out = r_push(host, stagedir.rstrip("/") + "/", root + "/")
    if rc != 0:
        die("⛔ push to %s failed (rc=%d):\n%s" % (host, rc, out), 4)
    say("shipped to %s:%s — %d arms, opp %s, %d maps, %d blocks"
        % (host, root, len(armnames), oppname, len(maps), len(spec["blocks"])))
    return root


def launch(host, root):
    py = "python3"
    # ⛔ `< /dev/null` AND THE fd REDIRECTS ARE WHAT MAKE THIS RETURN. Without
    # stdin closed the backgrounded driver keeps the ssh channel open and `ssh`
    # BLOCKS until it exits — measured 2026-08-20: a "launch" that took 30 s on
    # a 30 s battery and would have held one ssh session open for the whole of a
    # multi-hour one. The poll loop then polls nothing, and a dropped connection
    # would read as a launch failure while the driver ran on happily.
    # ⛔ `command -v`, NOT `{ setsid ...& } || { nohup ...& }`. Backgrounding
    # SUCCEEDS even when the command does not exist — the failure happens in the
    # child, so `||` never fires and the fallback is dead code. Measured
    # 2026-08-20: macOS has no `setsid`, the local leg launched a pid that
    # immediately died, and only the PARTIAL report + driver.log said why.
    cmd = ("cd '%s' && if command -v setsid >/dev/null 2>&1; then "
           "setsid %s driver.py < /dev/null > driver.log 2>&1 & "
           "else nohup %s driver.py < /dev/null > driver.log 2>&1 & fi; "
           "echo PID=$!" % (root, py, py))
    rc, out = r_exec(host, cmd, 60)
    m = re.search(r"PID=(\d+)", out or "")
    if not m:
        die("⛔ launch on %s produced no pid:\n%s" % (host, out), 4)
    say("LAUNCHED %s pid=%s root=%s" % (host, m.group(1), root))
    return int(m.group(1))


def poll(host, root, pid, planned_host, interval=15, quiet=False):
    """Return (rows, state, alive). state from the driver's own heartbeat."""
    probe = ("cd '%s' 2>/dev/null || { echo GONE; exit 0; }; "
             "if kill -0 %d 2>/dev/null; then echo ALIVE; else echo DEAD; fi; "
             "cat HEARTBEAT 2>/dev/null" % (root, pid))
    rc, out = r_exec(host, probe, 60)
    if out is None:
        return None, "UNREACHABLE", None
    alive = "ALIVE" in out
    rows, state = 0, "?"
    for line in out.splitlines():
        f = line.split("\t")
        if len(f) >= 4:
            try:
                rows, state = int(f[1]), f[3].strip()
            except ValueError:
                pass
    if not quiet:
        say("  %-16s rows=%d/%d state=%s driver=%s"
            % (host, rows, planned_host, state, "ALIVE" if alive else "DEAD"))
    return rows, state, alive


def pull(host, root, outdir):
    os.makedirs(outdir, exist_ok=True)
    rc, out = r_pull(host, "%s/out/" % root, outdir + "/")
    if rc != 0:
        say("⚠ pull from %s returned rc=%d:\n%s" % (host, rc, out))
    r_pull(host, "%s/driver.log" % root, os.path.join(outdir, "driver.log"))
    r_pull(host, "%s/HEARTBEAT" % root, os.path.join(outdir, "HEARTBEAT"))
    return rc


def cleanup(host, runid, root):
    """rm -rf, but only ever a validated path under the build root."""
    if not re.match(r"^[A-Za-z0-9_.-]+$", runid):
        say("⚠ refusing cleanup: runid %r is not a safe token" % runid)
        return
    if COREFILL_ROOT in root or root.strip() in ("", "/", "~", "$HOME"):
        say("⚠ refusing cleanup: %r is not a build-battery path" % root)
        return
    rc, out = r_exec(host, "chmod -R u+w '%s' 2>/dev/null; rm -rf '%s' && "
                     "test ! -e '%s' && echo CLEANED" % (root, root, root), 120)
    say("cleanup %s: %s" % (host, (out or "").strip() or "rc=%d" % rc))


# ═════════════════════════════════════════════════════════════════════════════
# assembly
# ═════════════════════════════════════════════════════════════════════════════
def assemble(outroot, hosts, blocks, armnames, planned_per_arm):
    """Per-arm tape in run_grid format, blocks concatenated in block order."""
    counts = {a: 0 for a in armnames}
    missing = []
    tapes = {}
    for a in armnames:
        tapes[a] = open(os.path.join(outroot, a + ".tsv"), "w")
        tapes[a].write("\t".join(HDR) + "\n")
    for b in blocks:
        d = os.path.join(outroot, "_raw", b["host"].replace("@", "_"),
                         "b%d" % b["index"])
        for a in armnames:
            p = os.path.join(d, a + ".tsv")
            if not os.path.exists(p):
                missing.append("%s b%d (%s)" % (a, b["index"], b["host"]))
                continue
            with open(p) as fh:
                for i, line in enumerate(fh):
                    if i == 0 and line.startswith("tag\t"):
                        continue
                    if line.strip():
                        tapes[a].write(line)
                        counts[a] += 1
    for a in armnames:
        tapes[a].close()
    return counts, missing


def driver_errors(outroot, hosts):
    """Whatever the remote driver said about itself. Printed on any shortfall.

    ⛔ The first live run of this tool returned 0 of 24 rows with a heartbeat
    reading COMPLETE, because `$HOME` in the engine path was never expanded (no
    shell ran it) and every arm raised FileNotFoundError into the driver's
    per-arm catch. The row count told the truth and the STATE LIED. Both halves
    are fixed — the driver now writes FAILED unless every tape exists — but the
    log is surfaced anyway: a state word is a summary, the log is the evidence.
    """
    out = []
    for h in hosts:
        p = os.path.join(outroot, "_raw", h.replace("@", "_"), "driver.log")
        if os.path.exists(p):
            txt = open(p).read().strip()
            if txt:
                out.append("%s: %s" % (h, txt[-1500:]))
    return out


# ═════════════════════════════════════════════════════════════════════════════
# selftest — offline, touches no host
# ═════════════════════════════════════════════════════════════════════════════
def selftest():
    import tempfile
    ok = 0

    # 1. seed parsing, both ways
    assert parse_seeds("1-5") == [1, 2, 3, 4, 5]
    assert parse_seeds("1,3,5") == [1, 3, 5]
    assert parse_seeds("1-3,9") == [1, 2, 3, 9]
    assert parse_seeds("2,2,3") == [2, 3], "duplicates must collapse"
    ok += 1

    # 2. block partition — and the assertion must FIRE on a bad split
    bl = make_blocks([1, 2, 3, 4, 5, 6], 3, ["h1", "h2"])
    assert [b["seeds"] for b in bl] == [[1, 2, 3], [4, 5, 6]]
    assert [b["host"] for b in bl] == ["h1", "h2"], "round-robin over hosts"
    fired = False
    try:
        seeds = [1, 2, 3]
        blocks = [{"index": 0, "seeds": [1, 2]}, {"index": 1, "seeds": [2, 3]}]
        flat = [s for b in blocks for s in b["seeds"]]
        assert sorted(flat) == sorted(seeds) and len(flat) == len(set(flat))
    except AssertionError:
        fired = True
    assert fired, "the partition assertion has never produced the other verdict"
    ok += 1

    # 3. capacity gate, driven BOTH ways against the real table
    c1, c2 = host_cores("work-server-1"), host_cores("work-server-2")
    assert c1 == 10 and c2 == 6, (c1, c2)
    assert host_cores("worker@work-server-1") == 10, "user-prefixed form"
    assert host_cores("no-such-host") is None
    ok += 1

    # 4. FORMAT: assemble produces a tape summarise.py consumes, and the
    #    counts it reports separate a complete run from a short one.
    d = tempfile.mkdtemp()
    blocks = [{"index": 0, "seeds": [1], "host": "h1"},
              {"index": 1, "seeds": [2], "host": "h2"}]
    for b in blocks:
        rd = os.path.join(d, "_raw", b["host"], "b%d" % b["index"])
        os.makedirs(rd)
        for a in ("armX", "armY"):
            with open(os.path.join(rd, a + ".tsv"), "w") as fh:
                fh.write("\t".join(HDR) + "\n")
                for seat in ("A", "B"):
                    fh.write("\t".join(str(x) for x in [
                        "m_s%d_%s" % (b["seeds"][0], seat), "m",
                        b["seeds"][0], seat, "US", a, "Core destroyed",
                        150, 0, 100, 50]) + "\n")
    counts, missing = assemble(d, ["h1", "h2"], blocks, ["armX", "armY"], 4)
    assert counts == {"armX": 4, "armY": 4}, counts
    assert missing == [], missing
    hdr = open(os.path.join(d, "armX.tsv")).readline().rstrip("\n").split("\t")
    assert hdr == HDR, hdr
    # ... and the SHORT case must come out different
    os.remove(os.path.join(d, "_raw", "h2", "b1", "armY.tsv"))
    counts2, missing2 = assemble(d, ["h1", "h2"], blocks, ["armX", "armY"], 4)
    assert counts2 == {"armX": 4, "armY": 2}, counts2
    assert missing2 == ["armY b1 (h2)"], missing2
    ok += 1
    shutil.rmtree(d)

    # 5. cleanup refuses anything that is not a build path
    class _Spy:
        called = []
    saved = globals()["r_exec"]
    globals()["r_exec"] = lambda h, c, t=60: (_Spy.called.append(c), (0, "CLEANED"))[1]
    cleanup("h", "run1", "fcode-worker/results")
    cleanup("h", "../evil", "fcode-build/x")
    assert _Spy.called == [], "cleanup ran on a path it must refuse: %s" % _Spy.called
    cleanup("h", "run1", "fcode-build/run1")
    assert len(_Spy.called) == 1 and "fcode-build/run1" in _Spy.called[0]
    globals()["r_exec"] = saved
    ok += 1

    print("SELFTEST PASS: %d groups, each driven to both verdicts" % ok)
    print("DETERMINISM (measured 2026-08-20, NOISE_OFF, 12 rows/arm, all 11 "
          "columns): local vs ws1, local vs ws2 and ws1 vs ws2 all 0/12 rows "
          "differ. Control: NOISE_ON, same host, repeat run -> 11/12 and 12/12 "
          "rows differ. Caveat: no arm tested was near the 10ms TLE budget.")


# ═════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--arm", action="append", default=[],
                    help="NAME=path or path (repeatable, >=2)")
    ap.add_argument("--opp", default="bots/_v488beltbreak2")
    ap.add_argument("--maps", default="atoll,drakkarfjord,glacierkeep,midgard,nordkap")
    ap.add_argument("--seeds", default="1-3")
    ap.add_argument("--block-size", type=int, default=3)
    ap.add_argument("--par", type=int, default=2)
    ap.add_argument("--hosts", default="work-server-1,work-server-2")
    ap.add_argument("--out", required=False)
    ap.add_argument("--runid", default=None)
    ap.add_argument("--poll-s", type=int, default=20)
    ap.add_argument("--timeout-s", type=int, default=6 * 3600)
    ap.add_argument("--keep-remote", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--gc", action="store_true",
                    help="list and remove ORPHANED build roots on --hosts "
                         "(a wrapper killed before its finally: block leaves "
                         "remote scratch; nothing else on the host reaps it)")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return 0
    if args.gc:
        for h in [x.strip() for x in args.hosts.split(",") if x.strip()]:
            if h == "local":
                continue
            rc, out = r_exec(h, "ls -1dt %s/*/ 2>/dev/null; echo END"
                             % REMOTE_BUILD_ROOT, 60)
            roots = [l.strip().rstrip("/") for l in (out or "").splitlines()
                     if l.strip().startswith(REMOTE_BUILD_ROOT + "/")]
            if not roots:
                say("gc %s: nothing under %s/" % (h, REMOTE_BUILD_ROOT))
                continue
            for r in roots:
                say("gc %s: removing %s" % (h, r))
                cleanup(h, os.path.basename(r), r)
        return 0
    if not args.out:
        die("⛔ --out <dir> is required")
    if len(args.arm) < 2:
        die("⛔ REFUSING: a battery needs >= 2 arms (that is what makes it a "
            "contrast). Got %d." % len(args.arm))

    arms = []
    for a in args.arm:
        if "=" in a:
            n, p = a.split("=", 1)
        else:
            n, p = os.path.basename(a.rstrip("/")), a
        arms.append((n, p))
    maps = [m.strip() for m in args.maps.split(",") if m.strip()]
    seeds = parse_seeds(args.seeds)
    hosts = [h.strip() for h in args.hosts.split(",") if h.strip()]
    pin = engine_pin()

    armnames = preflight_local(arms, args.opp, maps, seeds, args.par, hosts)
    queue_warning()

    blocks = make_blocks(seeds, args.block_size, hosts)
    planned_per_arm = len(maps) * len(seeds) * 2
    planned_total = planned_per_arm * len(arms)
    per_host = {}
    for h in hosts:
        hs = [s for b in blocks if b["host"] == h for s in b["seeds"]]
        per_host[h] = len(maps) * len(hs) * 2 * len(arms)

    runid = args.runid or ("bb_%s_%d" % (time.strftime("%Y%m%dT%H%M%SZ",
                                                       time.gmtime()),
                                         os.getpid()))
    outroot = args.out if os.path.isabs(args.out) else os.path.join(REPO, args.out)
    outroot = os.path.abspath(outroot)
    # ⛔ ENFORCE THE NAMESPACE, DO NOT MERELY DOCUMENT IT. The proof in this
    # file's header is about WHERE auto_gate looks; it is worth nothing if an
    # operator can point --out at exactly those two directories. A build tape
    # dropped in `scratchpad/overnight-remote/<host>/` IS a shard to
    # `scan_remote`, and one named after a corefill shard in
    # `scratchpad/overnight/` IS a shard to `scan_local`.
    for forbidden, why in ((os.path.join(REPO, "scratchpad/overnight-remote"),
                            "auto_gate.scan_remote enumerates every *.tsv one "
                            "level under this root"),
                           (os.path.join(REPO, "scratchpad/overnight"),
                            "auto_gate.scan_local opens <sid>.tsv here for "
                            "every id in corefill_work.txt")):
        if outroot == forbidden or outroot.startswith(forbidden + os.sep):
            die("⛔ REFUSING: --out %s is inside %s — %s. Build batteries must "
                "live in a namespace the corefill census cannot enumerate; use "
                "scratchpad/build_batteries/<run>/ or a build's own scratch dir."
                % (outroot, forbidden, why))
    os.makedirs(outroot, exist_ok=True)

    say("PLAN runid=%s" % runid)
    say("  arms=%s opp=%s" % (",".join(armnames), os.path.basename(args.opp)))
    say("  maps=%d seeds=%d blocks=%d par=%d -> %d rows/arm, %d total"
        % (len(maps), len(seeds), len(blocks), args.par, planned_per_arm,
           planned_total))
    for h in hosts:
        say("  %-16s blocks=%s rows=%d"
            % (h, [b["index"] for b in blocks if b["host"] == h], per_host[h]))
    say("  out=%s" % outroot)

    envs = {}
    for h in hosts:
        envs[h] = preflight_host(h, pin)
    if args.dry_run:
        say("DRY RUN — preflight passed, nothing shipped.")
        return 0

    roots, pids = {}, {}
    stageroot = os.path.join(outroot, "_stage")
    try:
        # Ship + launch the hosts IN PARALLEL. Sequentially, ws2 sat idle for
        # the whole of ws1's transport — on a two-host split that is half the
        # saving this tool exists to deliver, given away in the setup.
        import threading
        fail = []

        def setup(h):
            try:
                sd = os.path.join(stageroot, h.replace("@", "_"))
                anames, oname = stage(sd, arms, args.opp, maps)
                roots[h] = ship(h, runid, sd, anames, oname, maps, blocks,
                                args.par, envs[h]["fcode"], per_host[h])
                pids[h] = launch(h, roots[h])
            except BaseException as e:               # SystemExit from die()
                fail.append("%s: %r" % (h, e))
        ts = [threading.Thread(target=setup, args=(h,)) for h in hosts]
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        if fail:
            die("⛔ ship/launch failed: %s" % "; ".join(fail), 4)
        with open(os.path.join(outroot, "REMOTE_PIDS.txt"), "w") as fh:
            for h in hosts:
                fh.write("%s\t%s\t%d\n" % (h, roots[h], pids[h]))
        say("PIDS: " + "  ".join("%s=%d" % (h, pids[h]) for h in hosts))

        t0 = time.time()
        done = {h: False for h in hosts}
        last = {}
        while not all(done.values()):
            if time.time() - t0 > args.timeout_s:
                say("⚠ TIMEOUT after %ds — pulling whatever exists."
                    % args.timeout_s)
                break
            time.sleep(args.poll_s)
            for h in hosts:
                if done[h]:
                    continue
                rows, state, alive = poll(h, roots[h], pids[h], per_host[h])
                last[h] = (rows, state, alive)
                if state == "UNREACHABLE":
                    say("⚠ %s UNREACHABLE this tick — will retry" % h)
                    continue
                if state == "COMPLETE" or not alive:
                    done[h] = True
                    if not alive and state != "COMPLETE":
                        say("⛔ %s: driver pid %d is GONE with state=%s at "
                            "%s/%s rows — this run is PARTIAL."
                            % (h, pids[h], state, rows, per_host[h]))
    finally:
        for h in hosts:
            if h in roots:
                pull(h, roots[h],
                     os.path.join(outroot, "_raw", h.replace("@", "_")))
        if os.path.isdir(stageroot):
            shutil.rmtree(stageroot, ignore_errors=True)

    counts, missing = assemble(outroot, hosts, blocks, armnames,
                               planned_per_arm)
    lines = ["runid\t%s" % runid,
             "generated\t%s" % time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                             time.gmtime()),
             "hosts\t%s" % ",".join(hosts),
             "opp\t%s" % os.path.basename(args.opp),
             "maps\t%s" % ",".join(maps),
             "seeds\t%s" % args.seeds,
             "par\t%d" % args.par,
             "planned_rows_per_arm\t%d" % planned_per_arm]
    short = False
    for a in armnames:
        st = "COMPLETE" if counts[a] == planned_per_arm else "SHORT"
        if st == "SHORT":
            short = True
        lines.append("arm\t%s\tdelivered\t%d\tplanned\t%d\t%s"
                     % (a, counts[a], planned_per_arm, st))
    for m in missing:
        lines.append("missing_cell\t%s" % m)
    for e in driver_errors(outroot, hosts):
        lines.append("driver_log\t%s" % e.replace("\n", " | "))
    with open(os.path.join(outroot, "RESULT.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    for l in lines:
        say("  " + l.replace("\t", "  "))

    if not args.keep_remote:
        for h in hosts:
            if h in roots:
                cleanup(h, runid, roots[h])
    else:
        say("--keep-remote: remote scratch LEFT at " +
            "  ".join("%s:%s" % (h, roots[h]) for h in roots))

    if short:
        with open(os.path.join(outroot, "PARTIAL"), "w") as fh:
            fh.write("\n".join(lines) + "\n")
        say("⛔⛔ PARTIAL RUN — %s written. Row counts above are the truth; the "
            "tapes are SHORT and must not be read as a complete battery."
            % os.path.join(outroot, "PARTIAL"))
        return 2
    p = os.path.join(outroot, "PARTIAL")
    if os.path.exists(p):
        os.remove(p)
    say("COMPLETE — %d rows/arm on each of %d arms. Read it: "
        ".venv/bin/python <build>/summarise.py <name> %s/<arm>.tsv"
        % (planned_per_arm, len(armnames), outroot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
