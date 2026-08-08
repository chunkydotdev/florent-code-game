#!/usr/bin/env python3
"""Early-stopping match gate: same matches as arena.py, but stops as soon as the
evidence is one-sided.

Why this exists
---------------
`tools/arena.py` plays a FIXED block (15 maps x N seeds x 2 seat orderings = 480 at
--seeds 16) and only then looks at the result. Most candidate changes are either
obviously good or obviously dead, and burning 480 matches to learn "obviously dead"
is the single biggest cost in the change loop. This tool plays the *same* tickets in
the *same* way (it imports arena's match runner outright) but evaluates after every
completed pair and stops the moment a Wald sequential probability ratio test crosses
a boundary.

The accept criterion, vs fixed-480 arena
----------------------------------------
arena: run all 480, then accept if the Wilson 95% lower bound clears 50%. One
       decision, at the end, on a fixed sample.
sprt:  after every completed (map, seed) pair, update
           llr += wins*ln(p1/p0) + losses*ln((1-p1)/(1-p0))
       and stop at
           llr >= ln((1-beta)/alpha)   -> H1: the candidate is better (p >= p1)
           llr <= ln(beta/(1-alpha))   -> H0: not better (p <= p0)
       Budget exhaustion with no crossing is a third outcome: undecided.
       The Wilson interval is still computed and printed, but it is a *description*
       of the sample, not the accept rule. H0/H1 here mean "better than p1" /
       "no better than p0" — NOT "better than 50%". A 52% bot is a real improvement
       and this test is designed to call it H0 at the default p0=0.45/p1=0.55.

Independence caveat (read before shipping on this)
--------------------------------------------------
The two matches inside a pair share a map AND a seed — the same opening, differing
only in who acts first. They are strongly correlated, not two independent draws.
(Measured: they are not even identical, because --tle makes match outcomes
non-reproducible — but the map/seed correlation is real regardless.) Wald's
boundaries assume i.i.d. Bernoulli trials, so the true error rates here are not
exactly alpha/beta; the boundary is approximate and the effective sample size is
somewhere below the match count. Treat a decision that lands just past a boundary
with suspicion, and re-run the fixed-480 arena gate before shipping anything.

Usage
-----
    python3 tools/sprt.py cand incumbent                       # up to 480 matches
    python3 tools/sprt.py cand incumbent --seeds 8 --jobs 8
    python3 tools/sprt.py cand incumbent --p0 0.50 --p1 0.60   # ask a harder question
    python3 tools/sprt.py cand incumbent --dry-run             # just show ticket order

Live progress goes to stderr, the final report to stdout, so `> report.txt` keeps the
report clean.
"""

from __future__ import annotations

import argparse
import math
import os
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arena import ROOT, play, wilson  # noqa: E402  (arena.py is write-protected; import, never copy)


# --------------------------------------------------------------------------- tickets

class Ticket:
    """One match: a (map, seed) pair played in one of the two seat orderings."""

    __slots__ = ("index", "pair", "ordering", "job")

    def __init__(self, index: int, pair: tuple[str, int], ordering: int, job: tuple):
        self.index = index          # position in the interleaved queue
        self.pair = pair            # (map stem, seed) — the unit the SPRT consumes
        self.ordering = ordering    # 0: ref bot is seat A.  1: ref bot is seat B.
        self.job = job              # arena.play's job tuple

    def __repr__(self) -> str:
        bot_a, bot_b, map_path, seed, tle = self.job
        return f"{self.index:>4}  {Path(map_path).stem:<12} seed {seed:<3} {bot_a} (A) vs {bot_b} (B)"


def build_tickets(bot_a: str, bot_b: str, maps: list[Path], seeds: int, tle: int) -> list[Ticket]:
    """Round-robin across maps, so any prefix of this list is stratified over maps.

    Order is: every map at seed 1 (both orderings), then every map at seed 2, ...
    A stop after 60 matches has therefore seen all 15 maps twice, not the first two
    maps thirty times. Seeds are 1..N to match arena exactly, so an sprt run and an
    arena run play literally the same games.
    """
    tickets: list[Ticket] = []
    for seed in range(1, seeds + 1):
        for mp in maps:
            pair = (mp.stem, seed)
            # Both orderings, adjacent in the queue: Team A acts first, and that is
            # not a symmetric advantage, so seat only cancels if the pair completes.
            tickets.append(Ticket(len(tickets), pair, 0, (bot_a, bot_b, str(mp), seed, tle)))
            tickets.append(Ticket(len(tickets), pair, 1, (bot_b, bot_a, str(mp), seed, tle)))
    return tickets


def ref_won(ticket: Ticket, result: dict) -> bool:
    """Did the *first CLI bot* win this match?

    Decided by seat and ordering, not by name: in a mirror (bot_a == bot_b) the names
    collide and arena.play's `winner` field is useless. Ordering 0 puts the reference
    bot in seat A, ordering 1 puts it in seat B.
    """
    return result["seat"] == ("a" if ticket.ordering == 0 else "b")


# --------------------------------------------------------------------------- the test

class Sprt:
    """Wald SPRT on match wins for the reference bot."""

    def __init__(self, p0: float, p1: float, alpha: float, beta: float):
        self.p0, self.p1 = p0, p1
        self.win_term = math.log(p1 / p0)
        self.loss_term = math.log((1 - p1) / (1 - p0))
        self.upper = math.log((1 - beta) / alpha)   # cross up   -> accept H1
        self.lower = math.log(beta / (1 - alpha))   # cross down -> accept H0
        self.llr = 0.0

    def update(self, wins: int, losses: int) -> None:
        self.llr += wins * self.win_term + losses * self.loss_term

    def decision(self) -> str | None:
        if self.llr >= self.upper:
            return "H1"
        if self.llr <= self.lower:
            return "H0"
        return None


# --------------------------------------------------------------------------- report

def report(args, tickets, counted, pairs_done, sprt, decision, errors, discarded, elapsed):
    """Final report. The per-map seat table is arena's, replicated (arena builds it
    inline in main(), so there is no function to import)."""
    a, b = args.bot_a, args.bot_b
    n = len(counted)
    out = print  # stdout

    out("")
    out("=" * 78)
    out(f"  SPRT  {a}  vs  {b}")
    out("=" * 78)
    maps_seen = len({r["map"] for _, r in counted})
    out(f"  matches used: {n} of {len(tickets)} budgeted   "
        f"({pairs_done} complete pair{'' if pairs_done == 1 else 's'}, "
        f"{maps_seen}/{len(args.maps_resolved)} maps covered, {elapsed:.0f}s)")
    if discarded:
        out(f"  discarded: {discarded} in-flight match(es) from an incomplete pair at the stop")
    if errors:
        out(f"  errored:   {errors} match(es) produced no result (not counted, mirrors arena)")

    if n == 0:
        out("\n  no counted matches — nothing to report")
        return

    wins = sum(1 for t, r in counted if ref_won(t, r))
    lo, hi = wilson(wins, n)
    out("")
    if a == b:
        out(f"  mirror match: {a} vs itself. Names collide, so 'wins' are attributed by")
        out(f"  seat+ordering, not by name — the reference is whichever seat the first CLI")
        out(f"  bot occupied. This measures the noise floor: it should trend to 50% and the")
        out(f"  honest expected outcome is UNDECIDED. Crashes are not attributable.")
        out("")
    # The DECISION above is unbiased — the Wald boundaries deliver their nominal
    # 5%/5% error rates (verified by simulation, 6,000 runs per condition,
    # 2026-08-09). This LINE is not. It is conditioned on the stop, and anyone
    # reading an sprt.py report is by definition reading a run that stopped, so
    # the sample is selected on the very quantity it reports.
    #
    #   TRUE 50%, H1 stop -> reports 56.6%   (+6.6pp)   Wilson covers truth 89.2%
    #   TRUE 55%, H1 stop -> reports 58.4%   (+3.4pp)
    #   TRUE 60%, H1 stop -> reports 63.1%   (+3.1pp)
    #
    # Same family as the ceiling.py collider: condition on an outcome, then read
    # a statistic over the conditioned sample. The remedy already lives in the H1
    # verdict string ("confirm with a fixed-480 arena run before shipping") — what
    # was missing was any sign that this line itself is inflated, so a reader
    # quoting it without re-running inherited the bias silently.
    if decision in ("H1", "H0"):
        out(f"  {a} (reference) win rate: {wins}/{n} = {wins/n:.1%}   "
            f"** BIASED BY THE STOP — typically ~3pp AWAY FROM 50%, up to ~7pp when the "
            f"true edge is small. NOT a shippable effect size. Wilson suppressed here "
            f"(it undercovers, ~90% not 95%). Re-run fixed-480 for the real number. **")
    else:
        # Budget exhaustion is not conditioned on the statistic, so the sample is
        # unselected and both figures mean what they say.
        out(f"  {a} (reference) win rate: {wins}/{n} = {wins/n:.1%}   "
            f"Wilson 95% CI [{lo:.1%}, {hi:.1%}]   (unbiased: stopped on budget, "
            f"not on the boundary)")
    out(f"  llr {sprt.llr:+.3f}   boundaries [{sprt.lower:+.3f}, {sprt.upper:+.3f}]   "
        f"H0: p<={sprt.p0:.2f}   H1: p>={sprt.p1:.2f}")

    verdict = {
        "H1": f"--> H1 ACCEPTED: {a} is better than {b} (p >= {sprt.p1:.0%}). "
              f"Confirm with a fixed-480 arena run before shipping.",
        "H0": f"--> H0 ACCEPTED: {a} is not better than {b} (p <= {sprt.p0:.0%}). "
              f"Cheap kill — no confirm run needed unless the change was expected to be small.",
        None: f"--> UNDECIDED: budget exhausted with the llr still inside the boundaries. "
              f"The true edge is probably between {sprt.p0:.0%} and {sprt.p1:.0%}.",
    }[decision]
    out(f"  {verdict}")

    crashes = Counter()
    for _, r in counted:
        for seat, count in r["crashes"].items():
            crashes[r[f"bot_{seat}"]] += count
    out("\n  crashes (uncaught exceptions, each one permanently kills a unit):")
    if a == b:
        out(f"    {crashes[a]} total (not attributable — both seats are the same bot)")
    else:
        for bot in dict.fromkeys([a, b]):
            out(f"    {bot}: {crashes[bot]}")

    out("\n  win conditions:")
    for cond, c in Counter(r["condition"] for _, r in counted).most_common():
        out(f"    {cond}: {c}")

    # arena's per-map seat table, over whatever subset actually ran.
    out("\n  by map (seat A = acts first; with identical bots this should sit near 50%):")
    rows_by_map = defaultdict(list)
    for t, r in counted:
        rows_by_map[r["map"]].append((t, r))
    for mp in sorted(rows_by_map):
        rows = rows_by_map[mp]
        sa = sum(1 for _, r in rows if r["seat"] == "a")
        mlo, mhi = wilson(sa, len(rows))
        flag = "" if mlo <= 0.5 <= mhi else "   <-- seat decides this map"
        line = f"    {mp:<12} seatA {sa}/{len(rows)} = {sa/len(rows):>5.1%} [{mlo:.0%}, {mhi:.0%}]{flag}"
        if a != b:
            line += f"    {a} {sum(1 for t, r in rows if ref_won(t, r))}/{len(rows)}"
        out(line)

    seat_a = sum(1 for _, r in counted if r["seat"] == "a")
    out(f"\n  seat bias pooled: {seat_a}/{n} = {seat_a/n:.1%} — read the per-map rows above "
        f"instead, this average hides the split.")

    out("\n  " + "-" * 74)
    out("  HONEST STATS: the two matches in a pair share map AND seed — the same opening")
    out("  with the seats swapped, strongly correlated rather than independent draws.")
    out("  Wald's boundaries assume i.i.d. trials, so the real error rates are not exactly")
    out("  alpha/beta and the effective sample is smaller than the match count. A decision")
    out("  that lands just past a boundary is weak evidence. For a SHIP gate, re-run the")
    out(f"  fixed-480 arena: python3 tools/arena.py {a} {b} --seeds 16")
    out("  " + "-" * 74)


# --------------------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bot_a", help="candidate / reference bot — the win rate is reported for this one")
    ap.add_argument("bot_b", help="incumbent / baseline bot")
    ap.add_argument("--maps", nargs="*", default=None, help="map names (default: all in maps/)")
    ap.add_argument("--seeds", type=int, default=16,
                    help="MAX seeds per map per ordering — the budget ceiling, not a target (default 16 = 480 matches on 15 maps)")
    ap.add_argument("--tle", type=int, default=10, help="per-turn CPU limit in ms (default 10)")
    ap.add_argument("--jobs", type=int, default=0, help="parallel matches (default: cores-2)")
    ap.add_argument("--p0", type=float, default=0.45, help="H0 win rate: 'not better' (default 0.45)")
    ap.add_argument("--p1", type=float, default=0.55, help="H1 win rate: 'better' (default 0.55)")
    ap.add_argument("--alpha", type=float, default=0.05, help="false-accept-H1 rate (default 0.05)")
    ap.add_argument("--beta", type=float, default=0.05, help="false-accept-H0 rate (default 0.05)")
    ap.add_argument("--dry-run", action="store_true", help="print the ticket order and exit")
    args = ap.parse_args()

    if not 0 < args.p0 < args.p1 < 1:
        sys.exit("need 0 < --p0 < --p1 < 1")
    if not (0 < args.alpha < 1 and 0 < args.beta < 1):
        sys.exit("--alpha and --beta must be in (0, 1)")
    if args.seeds < 1:
        sys.exit("--seeds must be >= 1")

    # Map discovery: identical to arena's.
    maps_dir = ROOT / "maps"
    if args.maps:
        maps = [maps_dir / f"{m}.map26" if not m.endswith(".map26") else Path(m) for m in args.maps]
    else:
        maps = sorted(maps_dir.glob("*.map26"))
    if not maps:
        sys.exit("no maps found — run: python3 tools/make_map.py")
    args.maps_resolved = maps

    tickets = build_tickets(args.bot_a, args.bot_b, maps, args.seeds, args.tle)

    if args.dry_run:
        print(f"{len(tickets)} tickets — {len(maps)} maps x {args.seeds} seeds x 2 orderings, "
              f"interleaved round-robin across maps (pairs are adjacent and never split)\n")
        for t in tickets:
            print(t)
        return

    workers = args.jobs or max(1, (os.cpu_count() or 4) - 2)
    sprt = Sprt(args.p0, args.p1, args.alpha, args.beta)

    print(f"budget {len(tickets)} matches — {len(maps)} maps x {args.seeds} seeds x 2 orderings, "
          f"{workers} parallel", file=sys.stderr)
    print(f"SPRT H0 p<={args.p0:.2f} vs H1 p>={args.p1:.2f}, alpha={args.alpha} beta={args.beta}, "
          f"boundaries [{sprt.lower:+.3f}, {sprt.upper:+.3f}]\n", file=sys.stderr)

    queue = iter(tickets)
    pending: dict = {}
    arrived: dict[tuple, list] = defaultdict(list)
    counted: list = []           # [(ticket, result)] from complete pairs only
    pairs_done = 0
    errors = 0
    decision = None
    started = time.time()
    # Two tickets in flight per worker: enough to keep everyone busy, small enough
    # that a stop throws away little work.
    window = max(2, workers * 2)

    pool = ProcessPoolExecutor(max_workers=workers)
    try:
        def refill():
            while len(pending) < window:
                t = next(queue, None)
                if t is None:
                    return
                pending[pool.submit(play, t.job)] = t

        refill()
        while pending and decision is None:
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            # Deterministic within a batch: process in queue order.
            for fut in sorted(done, key=lambda f: pending[f].index):
                t = pending.pop(fut)
                try:
                    r = fut.result()
                except Exception as exc:                      # a worker blew up
                    print(f"\n  match error ({t.pair}): {exc}", file=sys.stderr)
                    r = None
                arrived[t.pair].append((t, r))
                if len(arrived[t.pair]) < 2:
                    continue

                # Pair complete — this is the only thing the accumulator ever sees.
                pair_rows = arrived.pop(t.pair)
                pairs_done += 1
                wins = losses = 0
                for pt, pr in pair_rows:
                    if pr is None:            # arena discards resultless matches; so do we
                        errors += 1
                        continue
                    counted.append((pt, pr))
                    if ref_won(pt, pr):
                        wins += 1
                    else:
                        losses += 1
                sprt.update(wins, losses)

                n = len(counted)
                w = sum(1 for ct, cr in counted if ref_won(ct, cr))
                rate = f"{w}/{n} = {w/n:.1%}" if n else "no results yet"
                lo, hi = wilson(w, n) if n else (0.0, 1.0)
                print(f"\r  {n}/{len(tickets)} matches  {rate} "
                      f"[{lo:.1%}, {hi:.1%}]  llr {sprt.llr:+7.3f}   ",
                      end="", file=sys.stderr, flush=True)

                decision = sprt.decision()
                if decision:
                    print(f"\n  boundary crossed after {n} matches -> {decision}",
                          file=sys.stderr)
                    break
            if decision is None:
                refill()
    finally:
        # Not-yet-started tickets are cancelled; anything already running is left to
        # finish and is discarded (it would be half a pair).
        discarded = sum(1 for f in pending if not f.cancel())
        pool.shutdown(wait=False, cancel_futures=True)

    print("", file=sys.stderr)
    report(args, tickets, counted, pairs_done, sprt, decision, errors, discarded,
           time.time() - started)


if __name__ == "__main__":
    main()
