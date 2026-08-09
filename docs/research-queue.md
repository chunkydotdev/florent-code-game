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
- **2026-08-09 01:3x** — **`pair.py` r1000 line CLEAN** (simulated across lethality;
  the conditional rate tracks a fixed 58% truth at every level). **But the ARGUMENT
  I built on our 58.2% is unsupported** (`grind-pocket-audit-2026-08-09.md`): the
  58% is identical under both "pushing is safe" and "pushing backfires", so it
  cannot support "trading away the grind is a cost". The deciding quantity is the
  **BACKFIRE RATE**, which nothing here measures. Our data weakly favours the
  regime my claim assumed (grind win rate exceeds kill-game win rate in every
  cohort, +13.4pp vs strong), so the top-block claim stands WITH that assumption
  stated. Candidate mechanism for the local/ladder split: backfire rate scales with
  opponent strength, and a dominated probe pool has a near-zero one.
  Sweep status: `ceiling.py` clean · `pair.py` clean · band instrument broken+fixed.
- **NEXT TICK:** `sprt.py` and `paired_vs_pooled.py` to finish item 2, then item 3
  (opponent constants under v80).
- **2026-08-09 01:5x** — **`punishing-pool-2026-08-09.md`: the lethality leg IS
  runnable.** 12 contested opponents (45-65%) + 3 we lose to (opp_v44 40.8%,
  opp_v76 38.3%, band_probe 26.7%). The "~3 effective opponents, all dominated"
  premise is not supported. **CORRECTED MY OWN §4**: ouroboros_probe is ~53%
  (contested), NOT dominated — the 87-93% was kladde only. The builder's
  strength-axis leg stands; my overbroad claim nearly retired it.
  **Limitation:** every `opp_vNN` is our own lineage, so the non-dominated
  self-play pool is our own code. Only band_probe/orizon_probe/ouroboros_probe are
  external and non-dominated, one leg each.
  **MY ERROR, recorded:** first pass pooled map-restricted legs and probe-FIDELITY
  rows into one median and read kladde_probe at 43% (correct: 73%). Caught before
  relay. Same class as rule 6 — it would have inverted the recommendation.
- **NEXT TICK:** `sprt.py` + `paired_vs_pooled.py` to close item 2, then item 3
  (opponent constants under v80, which unblocks the Lunds fixture).
7. **A per-opponent claim requires a per-opponent figure.** Never attribute a
   pooled row's headline number to an entity merely named in its text. Three
   attribution errors in one chain (2026-08-09) came from exactly this.
- **2026-08-09 02:1x** — **RETRACTION of the punishing-pool table.** Builder refused
  my correction to its ceiling battery; I checked the primary and it refuted ME.
  ouroboros_probe is **72.5%** (tape) / 79-93% (current head), not 53% — my figure
  was a pooled row's headline attributed to an opponent named in its text. **The
  whole §2 table was built that way; band_probe (88.3%) and orizon_probe (66.7%)
  invert from "we lose"/"contested" to DOMINATED.**
  **NET: every external replica is dominated. Arm 1 of my three-arm design does not
  exist. The builder's original "may not be runnable locally" was right.** Only
  self-play opponents (opp_v76 38.3, opp_v44 40.8, opp_v69 41.7) can punish, and
  they share our code. Relayed in time to cancel the post-freeze re-measurement of
  band/orizon, which would have burned a window.
  Rule 7 added. Third attribution error in one chain; found only because the
  builder refused a correction that flattered its own work.
- **NEXT TICK:** `sprt.py` + `paired_vs_pooled.py` to close item 2, then item 3.
8. **Verify claims that FLATTER your own work at least as hard as ones that
   damage it.** (Builder's symmetric rule to rule 7, 2026-08-09.) First
   application: the builder's "unrated is the only punishing instrument" finding
   partly vindicated my backfire mechanism — which is why I went at it rather
   than banking it, and found two overstatements.

## Log (continued)
- **2026-08-09 02:3x** — checked the builder's `[gate]` structural finding
  (`unrated-validity-check-2026-08-09.md`). **Their hive figures VERIFIED
  independently** (v80 unrated hive 1/17; the win is vs our own alt team, so
  0-for-16 external; 8 tiebreak losses). **Two narrowings relayed:** (a) the tape
  row "we own no local opponent that can punish us" is false — opp_v76/v44/v69
  beat us and are the builder's OWN primary arm; correct is "no EXTERNAL local
  opponent". (b) The hive-vs-1,080-matches contrast compares an ECONOMY question
  to a LETHALITY one — and local did not fail on hive, local SOLVED hive
  (code-read + my r42 replay test + their 2.10x det leg). The mechanism rests on
  ONE aggression question (v86), not two.
- **NEXT TICK:** `sprt.py` + `paired_vs_pooled.py` to close item 2, then item 3.
- **2026-08-09 02:5x** — **ITEM 2 CLOSED** (`instrument-sweep-close-2026-08-09.md`).
  `sprt.py` DECISION RULE SOUND (alpha 5.2%, beta 5.0% at nominal 5% — the gate can
  be trusted), but its **printed win rate + Wilson CI are biased ~+3pp at an H1
  stop** (+6.6pp when the truth is 50%) with ~90% CI coverage, undocumented.
  Mitigation already in-tool ("confirm with a fixed-480 run"). Also: at a 120-match
  budget a true +5pp bot returns UNDECIDED 44% of the time — the sequential face of
  leg-power-19pct. `paired_vs_pooled.py` clean.
  **SCORECARD: 4 tools swept, 3 clean, 1 cosmetic defect. The two genuinely broken
  things were the band split and my own pool table — not the arena toolchain.**
  NOT tested, flagged: the sprt harness (ticket pairing, discard-at-stop logic).
- **NEXT TICK: ITEM 3** — opponent constants under v80 (Ouroboros denial tiles,
  Lunds r3 launcher insertion measured under v83, KCM launcher r1->destroy r6).
  Unblocks the builder's Lunds fixture. Archive-only, zero downloads.
- **2026-08-09 03:0x** — **ITEM 3 DONE** (`opponent-constants-v80-2026-08-09.md`).
  **BLOCKER REMOVED: the Lunds fixture is unblocked.** My own ~22:4x re-seeding
  block is not supported. Lunds held v44 and Ouroboros v8 all day while we shipped
  v74→v86, so their version was fixed and ours varied — the exact experiment.
  Permutation tests on every opening constant: all p>=0.247 (Bonferroni needs
  0.005). **Lunds builds its launcher at r1 in 40/40 games across six of our
  versions — an exact invariant, not a null.**
  **The KCM "signal" I nearly relayed (harvester r2 vs r7, map-controlled) was
  entirely KCM's v1->v8 ship.** `match info` NULLS the opponent version; `match
  list` carries it. Wrong axis entirely.
  **Rule re-scoped:** pre-contact behaviour cannot depend on OUR version, only
  theirs; post-contact behaviour can. The staleness axis is THEIR ship.
  Remaining unverified: the Lunds insertion TILE (post-contact, and not
  extractable from replay_census which reports builds not launches).
- **QUEUE STATUS: items 1 (partial, metadata-capped), 2 (closed), 3 (done).**
  Remaining: item 4 (eider, exploratory — does NOT survive Bonferroni), item 5
  (prediction scoreboard). Both lower value than anything done tonight.
- **2026-08-09 03:2x** — **`lunds-insertion-tiles-2026-08-09.md`: the fixture's last
  unknown is retired.** 45 Lunds replays, 1,124 throws, zero downloads. Method was
  already in tooling.md (throws = long moveBuilderBot, never FireTurret).
  **Insertion tiles are a pure function of (map, seat) and INVARIANT across every
  one of our versions** — snowflake seat a identical over v74/75/76/80, nordkap
  seat b over v74/76/80/81. First throw at r3 (median, n=44). **The builder can
  hard-code the tiles.**
  **Correction to `lunds-switch-decode`:** its "absolutely oriented" sub-claim does
  not generalise — deriving each map's symmetry from its own tile grid, **5 of 7
  comparable maps FOLLOW the map symmetry** (drumlin/eider/heart/nordkap/snowflake),
  2 do not (atoll, archipelago). **moonrise — the map the original claim was about —
  has only one seat archived and is UNTESTED.** Does not refute the seat-split
  argument.
- **QUEUE NEARLY DRAINED.** Remaining: item 4 (eider, exploratory, fails Bonferroni)
  and item 5 (prediction scoreboard). Both lower value than tonight's output. Next
  tick: if nothing better surfaces, say so and hold rather than manufacture work.
- **2026-08-09 03:4x** — **throw-class split (builder ASK, cheap, done):** our
  launcher is **93% DEFENSIVE disposal** (705/759 enemy builders thrown away);
  only **7.1% offensive insertion** (54/759). Lunds is 31.5% offensive — 4.4x our
  rate. **Consequence: the launcher-deletion leg is ~93% an economy/denial
  question, locally gateable on delivered-Ti, and does NOT need a punishing pool.**
  Only the 7% insertion half inherits the backfire constraint.
  **Corrected my own incidental:** "we throw 2x more than Lunds" is a DEFENCE
  number (705 disposals vs 250), not an aggression one. I offered it loosely and
  the builder promoted it on the aggression reading; the deletion case still
  stands on the top-tier evidence (0/20 top-tier games have a launcher, we build
  one in 69%).

## HOLDING (2026-08-09 03:4x)

**Queue drained of anything worth more than the cost of running it.** Remaining
items 4 (eider — exploratory, fails Bonferroni) and 5 (prediction scoreboard) are
both worth less than tonight's output. Per the builder's agreement and this
queue's own rule 1, **holding rather than manufacturing work.**

Standing watch on the ~25min tick, no deliverables expected:
- **new builder ASKs** — these get priority over everything here
- **a Lunds ship** (v44 all day; a change invalidates every constant in
  `lunds-insertion-tiles-2026-08-09.md` at once — visible in `match list`, and
  `opp_watcher.py` already has `lunds` in NEMESES)
- **KCM / Ouroboros ships** (v8 and v8; same staleness logic)
- **the v80 window reaching n=20**, at which point the pre-registration scores

## WAKE CONDITION FIRED — 2026-08-09 02:31 CEST

**The v80 window has CLOSED at n=20.** Reported as DATA; the verdict is the
builder's and is not written here.

```
v80 re-activation window (all 20 matches >21:10Z):  net +22.38
  peak +45.75 at n=8, trough +4.46 at n=17, close +22.38

ON THE BUILDER'S FROZEN NAMED COHORTS:
  STRONG      n=10   net  -11.98
  WEAK        n= 9   net  +32.84
  UNASSIGNED  n= 1   net   +1.53   (Powered by SmartFridge — correctly
                                    reported separately, never folded in)
```

**This reproduces the strength-conditional finding prospectively.** The
retrospective 500-game cut gave STRONG 38.9% / WEAK 71.3% win rate; this is 20
fresh matches under a cohort definition frozen at n=6, before the outcome was
visible, and it splits the same way in Elo.

**ARITHMETIC FLAG for the builder:** baseline 1537.70 → current 1568 is +30.3,
but the eloDelta sum is +22.38 — a ~7.9 gap. Could be baseline instant, passive
drift, or a filter boundary. I have been wrong on this window's arithmetic once
already; **the builder owns the number and should reconcile it before scoring.**

**BLOCKER: the builder session appears stalled** — pane byte-identical across
three ticks (~65 min): same uptime 2h31m, same 410.9k tokens, same $31.99, with
an unsent prompt on its input line. No commits in that period. **The window has
closed and the arm that must score it is not running.** Surfaced to Magnus.
