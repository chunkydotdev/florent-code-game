# Standing research queue — ladder-independent work

**Owner:** research arm. **Created** session 20, 2026-08-09 00:1x CEST, on
Magnus's ask for a self-paced cadence that uses waiting time.

## Why this file exists

The 20-match slot freeze blocks *shipping*, not *measuring*. Nothing in this
queue needs the ladder, a download budget, or the builder's permission — every
item runs on the 3,573-replay local archive and free `match list`/`match info`
metadata. **A wake-up timer without a queue just manufactures analysis**, which
is the failure mode this project measured in itself tonight (`audit_trigger.py`,
note:verdict 4.38). So the queue is ordered by *how much it retires*, not by how
interesting it is.

## Rules for working this queue

1. **Prefer items that RETIRE a question over items that open one.** A refutation
   is worth more than a new hypothesis right now.
2. **Every claim gets the fixed-round / losses-vs-losses treatment before it
   ships.** Three colliders were found in one night (`ceiling.py` turns-to-kill,
   my peak-saturation law, and the map-ranking multiple-comparisons trap). Assume
   the next one is in whatever you just measured.
3. **Correct for the search space.** "Worst of N" is not a measurement until it is
   Bonferroni-corrected over N.
4. **Do not ping the builder with nothing.** If a tick produces no result, log it
   here and hold. Relay only on a finding, a refutation, or a blocker.
5. **Never touch:** bots, arena, verdicts, the tape, HANDOVER, submissions.

---

## QUEUE, ranked

### 1. Top-tier decode — 3,118 unexploited replays *(highest value, untouched)*
`replay_archive/` holds 3,573 files; only 455 map to our own games. **The rest
are other teams' matches, including the top tier that ends 97% of games by core
kill at a median of 232 turns.** We have never opened one. `match list` without
`--mine` returns every team's matches and `match info` works on matches we are
not in, so the metadata to map files → teams is free.

The ceiling question the whole project reordered around is *how do the strong
teams actually kill cores*, and the answer is sitting on disk. Concretely:
first-sentinel/gunner timing, harvester saturation curve, turret count and
placement, and time-to-first-contact for sporks / Lorem Ipsum / not adgato /
Flotte, against our own numbers.
**Cost:** zero downloads. **Retires:** whether our ceiling problem is a build
order we can copy or a mechanism we cannot.

### 2. Instrument audit sweep — find the remaining colliders
Three conditioning bugs surfaced in one night. Systematically re-check every
tool and every standing number that conditions on an outcome: anything computed
"over kills only", "over wins only", "peak over the game", or "at end of game"
is suspect. `tools/` plus the standing rows on the tape.
**Cost:** free, read-only. **Retires:** how much of the existing corpus is real.

### 3. Opponent constants are stale — the live version changed twice tonight
Protocol rule: deterministic opponents re-seed on OUR version. We went
v84 → v86 → v80 in under three hours. **Every constant extracted under a
different version is suspect** — Ouroboros denial tiles, the Lunds r3 launcher
insertion (measured under v83, and the Lunds fixture is blocked on this), KCM's
launcher r1 → destroy r6. Re-extract under v80.
**Cost:** free (archive). **Retires:** the block on queue item 1 of the builder's
own list.

### 4. eider — the second-worst cell, never examined
−22pp saturation gap at peak, 71% killed against strong opposition, 59% killed
overall. Everything hive had except the Bonferroni survival. The hive toolchain
(ore geometry, per-round tracking, turret lifetime) runs on it unchanged.
**Cost:** free. **Caveat:** eider does NOT survive multiple-comparison correction
(p×15 = 0.83) — treat as exploratory, and say so in the writeup.

### 5. Prediction scoreboard
The builder pre-registers predictions (the v86 strong/weak split was the first).
Nobody scores them systematically, so a prediction that quietly stops being
mentioned costs nothing. Keep a dated table: prediction, registered-at, bands,
outcome, scored-at.
**Cost:** trivial. **Retires:** the incentive to forget.

---

## Log

- **2026-08-09 00:1x** — queue created. Items 1–5 all unstarted. hive decode
  complete (4 docs); harvester-saturation generalisation complete and mostly
  negative.
- **2026-08-09 00:2x** — **item 1 DONE** (`top-tier-decode-2026-08-09.md`): top tier
  rushes gunners (r19 vs our r53), builds ZERO launchers, and holds economy flat
  at 3 harvesters while we grow to 5. Strength confound declared and unremovable
  with current data. **Blocker found: `match list` caps at ~100 recent matches, so
  3,073 of 3,573 archived replays cannot be mapped to a team.** The clean test
  (top-tier vs WEAK opponents) is blocked on it. Item 1 is not fully retired —
  reopen if more metadata becomes mappable.
- Also committed: `harvester-saturation-2026-08-08.md` — game-level saturation law
  REFUTED as a collider; map-level gap survives at r=+0.61.
- **NEXT TICK: item 2** (instrument audit sweep — two colliders found tonight in
  two different tools, assume more), then item 3 (opponent constants under v80,
  which unblocks the builder's Lunds fixture).
6. **A null is only evidence if the treatment was in the pool.** Before reporting
   "no difference across X", check that the thing being tested actually varies
   within the buckets. Three nulls tonight were bucket artefacts (the v77-84 hive
   fork bucket was 17/18 freeze-ON; the era swing was opponent-mix; peak
   saturation was a collider).
- **2026-08-09 00:4x** — builder found the hive mechanism in source (`hive_freeze`,
  arms at r>=42, no exit). **Tested its prediction against my per-round series:
  our hive growth collapses 5x at exactly r42 while both controls grow normally.**
  Code↔replay agreement confirmed. **Withdrew my own "flat across the v86 fork"
  null** — 17/18 of that bucket still carried the clause. Rule 6 added.
- **NEXT TICK: item 2, instrument audit sweep.** Two colliders + three bucket
  artefacts in one session. Sweep `tools/` and the standing tape rows for anything
  computed over-kills-only / over-wins-only / peak-over-game / at-end-of-game, and
  for any null whose bucket may not have contained the treatment.
