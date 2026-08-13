# Lane-structure review — 2026-08-13 (meta lane, Magnus-commissioned)

**TAGS:** written 2026-08-13T~09:30Z by a fourth, read-only session. Incumbent at
review time: v123 `bots/_v187saltidle_f` (shipped ~06:06Z). Rating 1648, rank
#27. Method: four read-only subagents (full coordination read for 08-12/08-13 +
sampled 08-10/11; git census of 1,927 commits since 08-07 with a validated
classifier; retro + vault synthesis; outcomes/bottleneck read). Per this
folder's charter: **this document proposes. Builder ships. Magnus decides lane
structure** (protocol rule 5: only Magnus widens a lane).

The questions asked: what has each lane done, how do they actually work, should
we split into more arms, is any lane unnecessary.

---

## 1. What each lane produced (08-07 → 08-13 ~07:30Z)

Commits since 08-07: **builder 621 · research 491 · side lane 248 · 412
coordination-only · 155 other = 1,927.** The side lane did not exist until
08-09 (Magnus founded it, overriding protocol rule 5's "never a third peer
session"); per active day its rate is comparable to the other two, not smaller.

**BUILDER** — 221 bot trees in 8 days; 26 version activations, 8 durable
holders; ~281k local games in the current corefill programme alone; ~30 tools
with selftests; **zero rated leakage across every prototype window** measured
at the pairing boundary (8–17 s exposure); and the honest self-accounting that
falsified the repo's "prototype legs cost zero" claim (−24.67 Elo, 3 matches).
Its retro's own summary of its failure mode holds up: errors that run toward
the work it wanted to do next, and guards that cannot fire — "all caught by
another lane, none by me."

**RESEARCH** — 229 docs in `docs/research/`; the corpus (3,831 replays, join
reconciled 1,155/1,155) — the single most-reused asset in the repo; a
retraction discipline no other lane matches (retractions-reaching-another-lane
per session: 3→4→5→10→7→4). Its own worst finding is about itself and it acted
on it: the protocol-mandated tactics library reached **313 files → 7
conversions → 0 decision-path citations** and the lane retired its flagship
activity, pivoting to `QUEUE.md` rows + instrument specs (D85: "instrument-
shaped output gets consumed; survey-shaped output does not"). s34 was the model
run: 11 findings consumed, 0 unread, all pre-decision. Today: the `oppver`
root-cause fix (`c7cd171`). Research-tagged commits: 125 → 79 → 54 → 22 → **1**
— the queue is full and its consumer cannot consume.

**SIDE LANE** — the channel's heaviest writer on all four of its days
(1.4–7×). Detection record is the best-measured value in the repo: today's
self-ledger (caveat §6) counts **16/16 outcome-changing flags real, median
flag→fix ~2 minutes**. The catches that mattered: the v122 stop-loss that
arithmetically **could never fire** (`coordination.md:40698`); the 60k-trial
sim showing the amended gate **doubled the false-wake rate** (`:40757` —
arguing against its own request); the screening power-curve that had been
**calibrated to reject LOKI-13-sized effects** → four killed planks reinstated
on Magnus's word (`:32500`); research's sign error caught ~20 min before
read-out (`:34786`); the kidnap-closure immortal-time bias → **sign reversal,
road reopened** (`:36290`). The costs are equally on record: 2 caused harms
(s33), 2 lane breaches (s30), and a stable asymmetry — **detection excellent,
prescription weak** (s34: "right that something was wrong, wrong about what
would fix it — every time"; today 2/16 named fixes needed correcting).

**Outcome** — rating 1345 → 1648 (peak 1700 on 08-11); **+254 in the 3.25
pre-prereg days, +49 in the 3.4 full-machinery days**, of which +75 is one
30-match v104 window. Rated game share flat: 49.8% → 50.3% (±1.7pp).
Meanwhile the named doctrine was delivered **completely**: r1000 games 56.2% →
2.0%, mean turns 655 → 217, wins-by-core-kill 41% → 100%. **The system can
drive any metric it names to completion; the metric it named did not pay. The
missing link is between the local screen and ladder game share — and only live
games can build that link.**

## 2. How they actually work (vs. how the protocol says)

- **The designed channels are dead.** The IN-FLIGHT registry's last edit was
  2026-08-08 (still lists v67-era rows); the `ASK:` convention was last used
  operationally 08-10. Real coordination is session pings + an append-only log
  written after the fact. Ceremony (boot/wrap/seam banners) is 8–19% of
  channel lines; ten sessions in 3.5 days, ~28 ceremony headers on 08-11 alone.
- **The mechanism that works is adversarial redundant derivation, not role
  partition.** Both the vault and `workflow-analysis/README.md:96-104` found
  4 of 5 catches came from *independently re-derived numbers* (often within
  one arm), not from the surface split. The lanes' catches of each other are
  real and symmetric — each lane has caught each other lane's worst error —
  but "the pass works because it is ADVERSARIAL, not because any lane is
  reliable" (`coordination.md:38805`).
- **All three lanes have converged on one function: instrument QA.** The side
  lane is de facto the statistics-methodology lane (power curves, estimator
  proofs, Monte Carlo — none in its charter); research writes `tools/`;
  the builder runs analysis subagents. Charters partition **surfaces**;
  the lanes converged on the same **question** (can we trust our numbers?).
  One day's honest tally: 12 instrument defects vs 1 plank that failed on its
  merits (`:30378`).
- **The real topology is: one executor (builder) + two detectors (research,
  side) + one decision-forcer (Magnus).** Every ship in the last four days was
  ordered or executed on Magnus's word; his one-line questions ("what's vjg?",
  "are the maps really different?", "we have become a machine that suppresses
  itself") produced the largest pivots; shared-premise catches are
  **three-for-three to the human** (vault). The vault's conclusion stands: he
  is a load-bearing component of the topology, not a supervisor of it.
- **The one measured interface defect: one-sided handoffs.** 32.6% of
  non-tactics research docs self-disclaim that they change anything; "a correct
  hand-off and a dropped one look identical in the repo." Four redo clusters
  (9,134 lines), same-question duplicates 21 and 92 minutes apart with zero
  cross-citation, D-number collisions across lanes twice, unflagged.

## 3. Where the capacity actually is

| surface | cap/day | used | notes |
|---|---|---|---|
| local self-play | ~230k games | **over-saturated** (load 12.25 vs ceiling 11.0) | 44 powered arms → **1** new decisive plank (SALT) |
| live unrated | 1,800 games (5 matches/20 min) | **~8–20%** | the `FIXTURE_OF_RECORD`; 34/40 legs ever fired used ≤16 matches, under the repo's own MDE |
| rated ladder | 360 games / 72 matches | 100%, non-discretionary | the only currency-bearing surface |

- **Queue:** 21 unblocked items, floor 3 — generation is oversupplied 7×.
  `#8` carries the board's only Elo estimate (~+7–14) and has gone unbuilt
  three sessions; the record says three times "it needs SCHEDULING, not
  re-ranking."
- **Decision rate:** the repo's own `cross-lane analysis` alarm has fired at
  every boot for four sessions (peak 37 docs / 0 decision rows);
  `ship_cadence` 0.20/hr beside it. `results.tsv` last wrote 08-11.
- **⛔ A load-bearing number is stale at HEAD:** "~84 rated matches/day ⇒ ~420
  remaining" was computed across the 08-10 cadence change and propagated into
  PROGRAMME.md:80, QUEUE.md:11, both SHIP preregs, and the builder retro. The
  measured current cadence is **20.0 min ⇒ 72/day** (40/40 recent gaps;
  corroborated by the elo tape's counter two days running). No hard end date
  exists on record — "over in a week" (08-11) ⇒ ~388 matches to 08-18.
- **Convergence cost is unvalidated in both directions.** "~100 to converge"
  has no derivation on record; the counter-claim (~30, from v104's +75-in-30)
  is contradicted by v116 (+32 in its first 15, −57 in its next 27). What is
  certain: **displacement at k=4 buys zero rated information**, and two ships
  in 80 minutes on 08-13 did exactly that — s35 flagged it as a pattern to put
  before Magnus at the third instance; this review makes it the second.
- **Gaps no lane owns** (all recurring in the record): PROGRAMME.md
  `INCUMBENT` staleness (4th lapse today; Magnus-only field, goes stale at
  every ship, and the ship IS a script); monitor/ops continuity (two stale
  loops alive 22 h, keeper fix unarmed, cores idle 45–70 min twice); letting a
  ship sit to its own gate; decoding our own rated games (a 0-5 loss by the
  live holder was invisible to every lane for an hour); opponent-version
  pinning cadence; directive propagation into boot surfaces (D79 family, five
  in one day).

## 4. Answers

**Should we split into more arms? No.** Every additional analysis arm lands in
a saturated function (detection), inherits the shared premises (the vault,
twice: "adding lanes makes it worse per unit cost, because each new lane
inherits the premise along with the boot context"), burns the shared channel
(41,463 lines) and the token budget Magnus named as binding on 08-12 — and
cannot touch either real constraint (the rated cap is a platform floor; ships,
PROGRAMME.md, and norms questions are Magnus-only). The repo answered this
question before it was asked: protocol rule 5 ("wider parallelism = subagent
fan-outs, never a peer session") and `tools/audit_trigger.py:11-15`, which
argued for **ephemeral stakeless auditors** the day before the permanent third
lane was created — a prediction ("a permanent third arm would eventually
acquire a stake") the side lane later confirmed in its own retro ("auditing is
a defending state").

**Is any lane unnecessary? None is dead weight — but marginal value is now
ordered, and two charters are pointed at the wrong decade of the project.**
The builder is the only lane on the critical path. The side lane's detection
half is the best-measured value in the record; its prescription half and its
channel volume are the cost. Research is the weakest *marginal* lane right now
— not through failure (s34 was its best run) but through success: the queue it
was chartered to fill is at 7× floor, and knowledge-that-pays-over-weeks has
no weeks left to pay in.

## 5. Recommendations (R1–R7; Magnus decides, builder ships)

- **R1 — keep three sessions, repurpose two charters for the endgame.**
  **Research → live-measurement operator:** owns the unrated-fixture cadence
  plan (which leg fires each 20-min window, pooled across windows), the pooled
  readouts, decode of our own rated games, and opponent-version pinning. All
  platform actions stay builder-only — research schedules and reads, never
  fires. This points the analytical muscle at the only idle instrument
  (~290 unused unrated matches/day ≈ 1,450 live games on the fixture of
  record, idle while the v116→v122→v123 chain shipped on local evidence
  alone). **Side lane → ship-critical verification only** — its own s31
  proposal: two-clock certs, gate/stop-loss arithmetic, rated-leak checks,
  rollback readiness. Drop α-methodology beyond live ships and per-commit
  audits of analysis docs; cap channel output.
- **R2 — a ship-sit rule (Magnus policy, one line):** no displacement before
  the shipped version's own gate arms (k≥8) unless a stop-loss fires. Two
  ships in 80 minutes spent two converge windows for zero rated information.
- **R3 — delegate the `INCUMBENT` line to `submit_clean --activate`** (the
  side lane's proposed procedure, `coordination.md:41296`). Four lapses;
  the field goes stale at exactly one event and that event is the script.
- **R4 — drive the live fixture toward cap as a standing loop** (the
  `panel2_cal.sh` pattern: safe window just after an observed pairing, rotate
  cells, pool across windows). This is the highest-leverage single move on the
  board and it is procedure, not headcount.
- **R5 — no fourth standing lane; ephemeral stakeless auditors for one-shot
  questions.** This review is the pattern working as designed —
  `audit_trigger`'s cross-lane row was firing at boot when it was
  commissioned.
- **R6 — consumption receipts:** the builder answers every relayed finding
  with one line, `CONSUMED:` or `KILLED:`. Fixes the one measured interface
  defect (one-sided handoffs) at the cost of a line.
- **R7 — bring the protocol doc up to date** (cheap, symbolic, overdue): it is
  still titled "two-session", gives the side lane no Roles entry, and mandates
  the tactics sweep research retired on evidence.

## 6. Caveats

- The side lane's 16/16 ledger was computed today explicitly *because* this
  review was announced (`5802676`) — a self-measurement under observation.
  The underlying flags and consuming commits are independently anchored.
- Lane attribution: coordination-channel line counts use carry-forward banner
  attribution (±10%); 274 coordination-only commits are unattributable by
  subject.
- This review cost four subagents (~860k tokens) — priced against its own
  thesis, which is why it ran once, as an ephemeral lane, per R5.
