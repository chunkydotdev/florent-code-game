#!/usr/bin/env python3
"""FIXTURE STARVATION DETECTOR — is a compute surface idle because nobody stocked it?

    .venv/bin/python tools/fixture_starvation.py            # all surfaces
    .venv/bin/python tools/fixture_starvation.py --selftest  # drive every branch both ways

WHY THIS EXISTS (2026-08-14, builder s43, on a side-lane finding).
At 20:40Z two of our three compute surfaces were idle and NO STATUS SURFACE WE
OWN COULD SAY SO:

  * LOCAL: every row of `corefill_work.txt` DONE or CANCELLED except one shard.
    `corefill_status.sh` printed `filler UP`, a healthy running row and a fresh
    heartbeat. Nothing lied. Nothing reported the starvation either -- because a
    worklist that is 100% DONE and a worklist that is 100% DONE **with more
    coming** render IDENTICALLY.
  * work-server-2: its worklist contained EXACTLY ONE ROW -- its own NULLHOST
    self-certification cell. It certified at 19:37Z and had nothing to do for
    over an hour on 6 cores, while `vps_pull` logged `pull ok` every 5 minutes.

**THE INSTRUMENT FINDING, and it is the reason this is a tool and not a habit:
THE HOST'S CERTIFICATION CELL IS WHAT GENERATES THE HEALTHY READING. Passing
certification is what starvation LOOKS LIKE.** That is a verification sharing
the failure mode of the thing it verifies. `ALWAYS_BE_RUNNING: yes` makes an
idle core a defect by programme, so this defect had an INSTRUMENT cause, not an
attention cause -- which is the only kind that stays fixed.

===== THE FOUR GUARDS, EACH ONE AN INCIDENT =====

1. **A CERT-ONLY WORKLIST IS STARVED, NOT HEALTHY.** `real_work` excludes the
   per-host NULLHOST certification cell by design. A host whose only row is the
   row that proves the host works is a host with nothing to do.

2. **CANNOT-READ IS NOT OK.** A missing/unreadable/empty worklist returns BLIND,
   never OK. An alarm that cannot tell it is blind is this repo's most-repeated
   defect; BLIND is a distinct exit state and a distinct string.

3. **DOMAIN VIOLATIONS FAIL LOUDLY.** `cert_rows > data_rows` is IMPOSSIBLE.
   The side lane's first cut of this detector used `grep -c NULLHOST`, which
   counted the worklist's HEADER COMMENT explaining NULLHOST, and returned
   `data=1 cert=2` -- an illegal value. That illegal value is the ONLY reason
   the bug was caught: the verdict it produced was exactly INVERTED (it flagged
   the busy host starved and the starved host busy), and it agreed with the
   author's live hypothesis, which is the class of error one is least likely to
   check. **We parse fields, never grep lines, and we assert the invariant.**

4. **STARVED AND DRAINING ARE DIFFERENT STATES.** Zero queued with a shard still
   running is DRAINING -- the surface goes idle when that shard lands, which is
   the moment to stock, not after. Rendering it as OK reproduces defect (1) with
   a delay.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# The per-host certification cell. It proves the host can run a game; it is not
# work. Named here once so the exclusion is auditable rather than inline.
CERT_SHARDS = {"NULLHOST"}

OK, DRAINING, STARVED, BLIND, ILLEGAL = "OK", "DRAINING", "STARVED", "BLIND", "ILLEGAL"


class Surface:
    """One compute surface: a worklist plus the output dir its shards write to."""

    def __init__(self, name: str, worklist: Path, outdir: Path, state_dir: Path | None = None):
        self.name = name
        self.worklist = Path(worklist)
        self.outdir = Path(outdir)
        self.state_dir = Path(state_dir) if state_dir else None

    # -- parsing -----------------------------------------------------------
    def rows(self):
        """Data rows as (shard, target). Comments and blanks dropped.

        Fields are SPLIT, never grepped -- see guard 3. A worklist header that
        merely mentions NULLHOST in prose must not read as a NULLHOST row.
        """
        out = []
        for line in self.worklist.read_text().splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            f = s.split()
            if not f:
                continue
            target = 0
            if len(f) >= 4:
                try:
                    target = int(f[3])
                except ValueError:
                    target = 0
            out.append((f[0], target))
        return out

    def _done_in(self, d: Path, shard: str) -> bool:
        """Terminal states. Remote mirrors do not delete, so a mirrored
        .COMPLETE can outlive an upstream reset -- the heartbeat's 5th field is
        rewritten every cycle and is preferred where it exists."""
        hb = d / f"{shard}.heartbeat"
        if hb.exists():
            try:
                f = hb.read_text().strip().split("\t")
                if len(f) >= 5 and f[4] == "COMPLETE":
                    return True
            except OSError:
                pass
        return (d / f"{shard}.COMPLETE").exists()

    def shard_done(self, shard: str) -> bool:
        """⛔ A LOCAL WORKLIST ROW CAN HAVE RUN ON A FLEET BOX.

        First cut of this checked only `self.outdir` and reported the local
        surface DRAINING with `in_flight=3` when exactly ONE shard was running:
        SEALFLOOR0R and SEALREPAIRR had completed REMOTELY, so their terminal
        markers sit in `overnight-remote/<host>/`, not in `scratchpad/overnight`.
        **That error ran in the flattering direction** -- it made a nearly-idle
        surface look busier than it was, which is the direction a starvation
        detector must never fail in. `corefill_status.sh` already carries this
        clause ("without this a remote shard reads DEAD locally"); this one did
        not, and the two disagreed.
        """
        if self._done_in(self.outdir, shard):
            return True
        remote = REPO / "scratchpad/overnight-remote"
        if self.outdir.parent != remote and remote.is_dir():
            for host in remote.iterdir():
                if host.is_dir() and self._done_in(host, shard):
                    return True
        return False

    def shard_cancelled(self, shard: str) -> bool:
        if self.state_dir is None:
            return False
        p = self.state_dir / shard
        if not p.exists():
            return False
        try:
            return "cancelled" in p.read_text()
        except OSError:
            return False

    def shard_started(self, shard: str) -> bool:
        if self.state_dir is None:
            return (self.outdir / f"{shard}.tsv").exists()
        return (self.state_dir / shard).exists()

    def counts(self, rows):
        """(data_rows, cert_rows). A SEAM, on purpose.

        Both counts derive from ONE parsed list here, which makes
        `cert > data` structurally impossible -- and an unreachable guard is
        decoration. The seam exists so the invariant is REACHABLE and therefore
        testable: the detector this replaces counted the two from DIFFERENT
        sources (rows by `grep -vc '^#'`, cert by `grep -c NULLHOST`, which hit
        the header comment) and produced `data=1 cert=2`. Any future
        reimplementation -- a zsh port, a caller passing precomputed counts --
        can reintroduce exactly that skew, and guard 3 is what catches it.
        """
        return len(rows), sum(1 for s, _ in rows if s in CERT_SHARDS)

    # -- the verdict -------------------------------------------------------
    def verdict(self) -> dict:
        r = {
            "surface": self.name,
            "worklist": str(self.worklist),
            "data_rows": 0,
            "cert_rows": 0,
            "real_rows": 0,
            "real_remaining": 0,
            "in_flight": 0,
            "state": BLIND,
            "note": "",
        }

        # GUARD 2: cannot-read is BLIND, never OK.
        if not self.worklist.exists():
            r["note"] = "worklist does not exist -- BLIND, not OK"
            return r
        try:
            rows = self.rows()
        except OSError as e:
            r["note"] = f"worklist unreadable ({e}) -- BLIND, not OK"
            return r

        real = [(s, t) for s, t in rows if s not in CERT_SHARDS]
        r["data_rows"], r["cert_rows"] = self.counts(rows)
        r["real_rows"] = len(real)

        # GUARD 3: impossible values fail loudly rather than producing a verdict.
        if r["cert_rows"] > r["data_rows"]:
            r["state"] = ILLEGAL
            r["note"] = (
                f"cert_rows={r['cert_rows']} > data_rows={r['data_rows']} is IMPOSSIBLE "
                "-- the parser is broken, not the fixture"
            )
            return r

        if not rows:
            r["note"] = "worklist has ZERO data rows -- BLIND (nothing to reason about)"
            return r

        remaining, in_flight = [], []
        for shard, _t in real:
            if self.shard_done(shard) or self.shard_cancelled(shard):
                continue
            remaining.append(shard)
            if self.shard_started(shard):
                in_flight.append(shard)
        r["real_remaining"] = len(remaining)
        r["in_flight"] = len(in_flight)

        # GUARD 1 + 4.
        if r["real_rows"] == 0:
            r["state"] = STARVED
            r["note"] = (
                "worklist is CERTIFICATION CELL ONLY -- the row that proves the host "
                "works is not work. Passing certification is what starvation looks like."
            )
        elif r["real_remaining"] == 0:
            r["state"] = STARVED
            r["note"] = "every real shard is DONE or CANCELLED -- nothing left to launch"
        elif r["real_remaining"] == r["in_flight"]:
            r["state"] = DRAINING
            r["note"] = (
                f"{r['in_flight']} shard(s) in flight and NOTHING queued behind them "
                "-- this surface goes idle when they land; stock it now, not then"
            )
        else:
            r["state"] = OK
            r["note"] = f"{r['real_remaining'] - r['in_flight']} shard(s) queued"
        return r


def discover() -> list[Surface]:
    s = [
        Surface(
            "local",
            REPO / "scratchpad/corefill_work.txt",
            REPO / "scratchpad/overnight",
            REPO / "scratchpad/corefill_started",
        )
    ]
    remote = REPO / "scratchpad/overnight-remote"
    if remote.is_dir():
        for host in sorted(p for p in remote.iterdir() if p.is_dir()):
            s.append(Surface(host.name, host / "worklist.txt", host))
    return s


def render(results) -> int:
    print("FIXTURE STARVATION — is a compute surface idle because nobody stocked it?\n")
    hdr = f"  {'SURFACE':<26} {'STATE':<9} {'REAL':>5} {'LEFT':>5} {'FLIGHT':>7}  NOTE"
    print(hdr)
    bad = 0
    for r in results:
        mark = "ok" if r["state"] == OK else "!!"
        if r["state"] != OK:
            bad += 1
        print(
            f"{mark:>2} {r['surface']:<26} {r['state']:<9} {r['real_rows']:>5} "
            f"{r['real_remaining']:>5} {r['in_flight']:>7}  {r['note']}"
        )
    print()
    if bad:
        print(f"*** {bad} of {len(results)} surface(s) NOT OK — ALWAYS_BE_RUNNING makes an idle core a defect ***")
        print("    stock local: append a line to scratchpad/corefill_work.txt")
        print("    stock remote: tools/vps/orchestrate.sh gen (⚠ check its --source path is IN THE REPO)")
    else:
        print(f"OK — all {len(results)} surface(s) have queued work.")
    return 1 if bad else 0


# ===== SELFTEST — every branch driven to BOTH verdicts =====================
# A guard that has only ever passed has not been seen to check anything. Each
# case below names the verdict it MUST produce; a case that comes out the other
# way exits nonzero. This is the discipline that caught the inverted detector
# this tool replaces.
def selftest() -> int:
    cases, fails = [], 0
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        def mk(name, worklist_text, done=(), cancelled=(), started=()):
            d = td / name
            (d / "out").mkdir(parents=True)
            (d / "state").mkdir(parents=True)
            wl = d / "worklist.txt"
            wl.write_text(worklist_text)
            for s in done:
                (d / "out" / f"{s}.COMPLETE").write_text("x")
            for s in cancelled:
                (d / "state" / s).write_text("cancelled")
            for s in started:
                (d / "state" / s).write_text("started")
            return Surface(name, wl, d / "out", d / "state")

        HDR = "# generated by orchestrate.sh\n# NULLHOST is first and is the per-host certification cell\n"

        # 1. cert-only worklist WITH a header that mentions NULLHOST in prose.
        #    This is the exact fixture whose grep-based predecessor returned an
        #    illegal value and an INVERTED verdict.
        cases.append((mk("cert_only", HDR + "NULLHOST a b 400 1\n"), STARVED))

        # 2. two real rows, both DONE -> starved (the LOCAL defect).
        cases.append((mk("all_done", HDR + "NULLHOST a b 400 1\nAAA a b 100 2\nBBB a b 100 3\n",
                         done=("AAA", "BBB")), STARVED))

        # 3. real work queued -> OK. The positive control: without this the
        #    detector could return STARVED unconditionally and look perfect.
        cases.append((mk("has_work", HDR + "NULLHOST a b 400 1\nAAA a b 100 2\nBBB a b 100 3\n",
                         done=("AAA",)), OK))

        # 4. last shard in flight, nothing behind it -> DRAINING, not OK.
        cases.append((mk("draining", HDR + "AAA a b 100 2\n", started=("AAA",)), DRAINING))

        # 5. cancelled counts as terminal.
        cases.append((mk("cancelled", HDR + "AAA a b 100 2\n", cancelled=("AAA",)), STARVED))

        # 6. missing worklist -> BLIND, never OK.
        cases.append((Surface("missing", td / "nope/worklist.txt", td / "nope"), BLIND))

        # 7. worklist of comments only -> BLIND, not OK and not STARVED.
        cases.append((mk("comments_only", HDR), BLIND))

        # 8. heartbeat COMPLETE is terminal even with no .COMPLETE marker
        #    (mirrors do not delete; the heartbeat is rewritten every cycle).
        s8 = mk("hb_complete", HDR + "AAA a b 100 2\n")
        (s8.outdir / "AAA.heartbeat").write_text("2026-08-14T20:00:00Z\t100\t100\tAAA\tCOMPLETE\n")
        cases.append((s8, STARVED))

        # 9. heartbeat RUNNING is NOT terminal -- the forced-fail twin of 8.
        #    Without this, `shard_done` returning True unconditionally passes 8.
        s9 = mk("hb_running", HDR + "AAA a b 100 2\nBBB a b 100 3\n")
        (s9.outdir / "AAA.heartbeat").write_text("2026-08-14T20:00:00Z\t50\t100\tAAA\tRUNNING\n")
        cases.append((s9, OK))

        print("FIXTURE_STARVATION SELFTEST — every branch, both verdicts\n")
        for surf, want in cases:
            got = surf.verdict()["state"]
            good = got == want
            fails += 0 if good else 1
            print(f"  [{'ok' if good else 'FAIL'}] {surf.name:<16} want={want:<9} got={got}")

        # 10. GUARD 3's forced-fail case, via the `counts()` seam.
        #     A guard whose failing branch cannot be REACHED is decoration. In
        #     this implementation both counts come from one list, so the skew is
        #     structurally impossible -- which is why `counts()` exists as a
        #     seam. Here we reintroduce the EXACT skew the grep-based detector
        #     produced (cert counted off the header prose, data off the rows)
        #     and require ILLEGAL, not a verdict.
        class MiscountingSurface(Surface):
            def counts(self_inner, rows):
                return len(rows), len(rows) + 1  # data=1, cert=2 -- the real bug

        skewed = MiscountingSurface(
            "miscounting", (td / "cert_only" / "worklist.txt"), td / "cert_only" / "out",
            td / "cert_only" / "state",
        )
        got = skewed.verdict()["state"]
        good = got == ILLEGAL
        fails += 0 if good else 1
        print(f"  [{'ok' if good else 'FAIL'}] {'miscounting':<16} want={ILLEGAL:<9} got={got}")

        # 11. The twin: the CORRECT parser on the SAME fixture must NOT return
        #     ILLEGAL. Without this, `counts()` returning ILLEGAL always would
        #     pass case 10 and the guard would be a constant column.
        honest = Surface(
            "honest_twin", (td / "cert_only" / "worklist.txt"), td / "cert_only" / "out",
            td / "cert_only" / "state",
        )
        got = honest.verdict()["state"]
        good = got != ILLEGAL
        fails += 0 if good else 1
        print(f"  [{'ok' if good else 'FAIL'}] {'honest_twin':<16} want=not-ILLEGAL got={got}")

    print()
    if fails:
        print(f"SELFTEST: {fails} FAILURE(S) — do not trust this detector")
        return 1
    print(f"SELFTEST: PASS ({len(cases)} branch cases + 2 invariant cases, every branch driven both ways)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true", help="drive every branch to both verdicts")
    ap.add_argument("--quiet-ok", action="store_true", help="print nothing when all surfaces are OK")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    results = [s.verdict() for s in discover()]
    if a.quiet_ok and all(r["state"] == OK for r in results):
        return 0
    return render(results)


if __name__ == "__main__":
    sys.exit(main())
