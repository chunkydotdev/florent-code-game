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
- **2026-08-09 01:0x** — **item 2 partly done** (`instrument-audit-bands-2026-08-09.md`).
  **FINDING: `teamXRating` is CURRENT rating, not at-match** (our own is a single
  value 1573 across 100 matches spanning a 1593→1537→1579 window). The strong/weak
  split therefore has look-ahead bias; 51% of the corpus is within ±60 Elo of the
  1550 line and two opponents totalling 75 games sit within 20 Elo pulling in
  opposite directions. **Strong band robust (39-42% at every threshold); weak band
  swings 75→57% on threshold choice — my 38.9-vs-71.3 contrast was the most
  favourable framing, not a stable fact.** Recommended identity-based cohorts to
  the builder, who had locked the bands on my suggestion.
  **NULL recorded so it is not re-run:** hunted a second collider in `ceiling.py`
  `conversion` (kills/wins) and did not find one — attenuation, not inversion, and
  conservative in the builder's actual comparison. `ceiling.py` is clean.
- **NEXT TICK:** finish item 2 (sweep `sprt.py`, `pair.py` r1000-conditioned line,
  `paired_vs_pooled.py`, and the standing tape rows), then item 3 (opponent
  constants under v80 — unblocks the builder's Lunds fixture).
- **2026-08-09 01:1x** — **band drift MEASURED, not predicted.** Comparing my 22:25
  and 00:05 API pulls: **Askar City +41 (WEAK->STRONG) and OopsGotYourElo -14
  (STRONG->WEAK) crossed the line in 100 minutes.** Same 500 games rescored moved
  38.9/71.3 -> 40.0/67.7 with zero new games. Builder's frozen roster verified
  against the 00:05 ratings: all 19 teams agree, freeze is clean.
  **Also: v86 window on the tape is n=4/-34.85 but the complete window is
  n=5/-27.20** — the Banminary +7.65 landed 12 min before v80's re-activation.
  Relayed; the trigger recomputation is the builder's, not mine.
  **My own error corrected:** I said the v80 window was n=7; it is n=6. v80 has two
  lives (17:18-17:35 at -8.82, then 21:17+ at +33.54). A version label is not a
  window — same class as rule 6.
- **NEXT TICK:** finish the sweep (`sprt.py`, `pair.py` r1000 line,
  `paired_vs_pooled.py`), then item 3 (opponent constants under v80).
