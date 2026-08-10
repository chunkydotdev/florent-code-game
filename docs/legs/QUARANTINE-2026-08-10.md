# QUARANTINED GAMES — do not re-ingest into any pool

A durable record, because a discarded row that lives only in a scratch file is
the same hazard as a stale row that looks valid: **the next pooling read picks
it up and nothing says it shouldn't.**

## 2026-08-10 — CONTROL arm contaminated by a failed rollback

**Cause.** `tools/fanout.sh`'s CONFIRM-v102 arm activated v102, fired, and its
rollback did not take. The next arm in rotation was **CONTROL — which activates
nothing and therefore asserted nothing** — and fired its challenges into a live
v102. **The denominator every other experiment is measured against was silently
filled with the wrong bot by the arm that had just run.**

**The principle the tool was missing, now enforced in `fire()`: an arm that
activates nothing must still ASSERT what is active.**

| matchId | createdAt | played by | belonged in |
|---|---|---|---|
| `e08e7ef6-5449-4177-9ada-afbf0470742a` | 2026-08-10T12:32:08.004Z | **v102** | v104 CONTROL |
| `9e706e3a-23ba-423e-89e1-4efb65b090ab` | 2026-08-10T12:32:08.641Z | **v102** | v104 CONTROL |

**10 games. Removed from `scratchpad/arm_v104.txt`; control restored to 30 clean
matches. Every other arm audited and 100% correct-version** (loki15 30/30 v105,
v102confirm 20/20 v102, loki16 15/15 v106, loki14 15/15 v107).

## THE BANKED CONFIRM RESULT IS UNAFFECTED — settled on timestamps, not on argument

**Both contaminants were created at 12:32:08Z. The CONFIRM control (n=150) was
read at ~12:18-12:20Z, twelve minutes earlier. They were never in it.**
`RESULT-confirm-pavetrail-2026-08-10.md` needs no recomputation.

**And had they been in it, the bias ran the reassuring way:** v102 games score
~47% sitting in a v104 control measuring ~54%, so they would have dragged the
control DOWN, making the measured -7.0pp an UNDER-statement of v104's edge.
Correcting would have moved the delta toward the -18pp prediction, not away —
to roughly -9pp, still nowhere near the bar. **"NOT CONFIRMED" would have stood
either way.**

## Method note

The contamination was found by **auditing every arm against the platform's own
`teamAVersion`/`teamBVersion` per match**, not by trusting the outfile the runner
wrote. **A runner's record of what it fired is not evidence of what actually
played** — the same class as the elo tape's poll-time version tag, which records
which submission was active when the tape was sampled rather than which one
played the match.
