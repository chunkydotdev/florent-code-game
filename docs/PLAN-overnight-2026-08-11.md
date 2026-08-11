# OVERNIGHT PLAN — 2026-08-11, ~6 hours of local cores

**Magnus: *"make a plan for tonight, we want to run h2h games on cores and need
to use ~6 hours."*** Plan proposed by the side lane, executed and corrected here
by the builder (games are my lane).

**BUDGET.** 10 cores, 1 reserved for the session + 7 monitors ⇒ **9 shards**.
Measured throughput 1,024 games/shard/50 min ⇒ **~7,300 games/shard over 6 h ⇒
~65,000 games.** For scale: **the entire remaining ladder is ~420 matches ≈ 2,100
games. Tonight is ~30× the whole rest of the competition.**

---

## PART A — CALIBRATION: does a local h2h win rate predict the LADDER? (4 shards)

**This is the highest-value question on the board and we have argued about it all
day without measuring it.** Round-robin over four versions with known ladder
history: **v92 (`_v115dodge`) · v102 (`_v124loki8`) · v104 (`_v130loki13`) ·
v112 (`_v148ferryfirst`)**. Six pairings, both seats, ~4,800 games each ⇒ each
pairwise rate to **±0.7pp**.

**THE STATISTIC — and this is correction #1 to the proposal.** *"Correlate the
local ordering against the ladder ordering"* is a correlation on **four points**,
which has ~2 df and cannot resolve anything. **The right test converts each local
win rate to an IMPLIED ELO GAP and compares it against the OBSERVED ladder gap —
six paired comparisons, each with a real interval:**

    implied_elo = -400 * log10(1/winrate - 1)
    residual    = implied_elo - (ladder_elo_A - ladder_elo_B)

**Report the six residuals, their mean and spread.** A tight cluster near zero
means local h2h is a calibrated ladder predictor. A large or systematically
signed spread means it is not, and the SIGN tells us which way it lies.

⛔ **CORRECTION #2, AND IT IS THE LOAD-BEARING CAVEAT: THE FOUR LADDER RATINGS
ARE NOT CONTEMPORANEOUS AND ONE IS BARELY MEASURED.**
* v92 = **1531**, earned days ago against a field that has since moved.
* v102 ≈ **1567**, likewise.
* v104 = **1672–1698**, current era, hundreds of matches.
* **v112 = 1674 on FOUR RATED MATCHES.** That is not a rating, it is v104's
  inherited number plus noise, and it was set at the bottom of a v104 drawdown.
* ⇒ **The residuals confound "local does not predict the ladder" with "the field
  changed between eras".** By morning v112 will have ~30 matches, which is better
  and still thin. **Lean the read on v92/v102/v104, which have real history, and
  report v112's point WITH ITS n=4 beside it rather than pooled in.**

**WHAT IT DECIDES — and it governs the remaining ~4 ship cycles:** if local
predicts ladder, every screen we run this week is trustworthy and we should
screen hard. If it does not, **we stop screening and ship on mechanism alone.**

## PART B — SCREENING: 4 arms + a null (5 shards)

**vs `_v148ferryfirst` (v112, the current incumbent), ~7,300 games each ⇒
SE ≈ 0.8pp, MDE ≈ 1.7pp.** At ~7 Elo per pp that resolves **+12 Elo effects** —
shippable, and far below the **+17.5pp** the n=64 screen could see.

| shard | arm | why |
|---|---|---|
| B1 | `_v149cbfull` — `LOKI_QUIET_ON = False` | crude revert: was LOKI-QUIET right under the CURRENT currency? |
| B2 | `_v150cbturret` — LOKI-29B counterbattery, turrets only | aimed at term `A` (1.77×, **47.3% of the log hazard gap**) |
| B3 | *TBD from the 14:47 screen result* | filled from tonight's own 1,024-game read |
| B4 | *TBD — top unblocked `QUEUE.md` item* | research keeps it stocked |
| **B5** | **NULL — byte-identical copy of v112** | **see control 2. Non-negotiable.** |

---

## THE FIVE CONTROLS

1. **SEAT-BALANCED.** `h2h.sh:68` is `for ORD in A B` inside the seed×map loop, so
   every arm plays **exactly equal games in each seat by construction.**
   **Seat is worth 7.6pp on byte-identical arms — ~2.5× the largest arm effect
   ever screened here — so an unbalanced cut measures SEAT and reports it as the
   plank.** Verified in the harness, not assumed.
2. **A NULL ARM IN THE SAME BATCH.** Byte-identical copy of v112 vs v112, under
   tonight's exact conditions. **It measures the night's own noise floor and
   re-checks seat balance.** ⛔ **And it is required for a second reason: the
   standing 4,096-game null belongs to the RETIRED loki13 control and is marked
   STALE. A null belongs to its control.** Without B5 no band tonight has a
   reference.
3. **`NOISE_ON` — DECIDED DELIBERATELY, REASON RECORDED.** `gate.py` FAILs
   `NOISE_ON = True` because paired fixtures do not pair against a bot that
   reseeds (`main.py:276`, `random.Random().randrange(97)`, unseeded).
   **DECISION: LEAVE IT TRUE.** At n≈7,300/arm we do not need pairing's variance
   reduction, and we want **the behaviour we actually ship**. Pinning it would
   measure a bot we do not run. ⇒ **This is an explicit gate override with the
   reason on the record, not a bypass.**
4. **UNIQUE REPLAY PATH PER GAME** for anything decoded. `h2h.sh` passes no
   `--replay`, so every game overwrites the single `fcode.toml` default — a
   6-hour run against one path keeps the last game. **Part A and Part B read win
   rate and kill round off stdout and need no replays, so they run as-is; any
   DOSE check spun off tonight must pass `--replay`.**
5. **A LIVENESS SIGNAL.** Nobody watches for six hours, and **a run that dies at
   hour one is indistinguishable from one that is working** — this repo's
   signature failure. Each shard's log is polled; the watcher reports **row
   counts, the age of the newest line, and shards that exited early.**

**STANDING RULES CARRIED:** stop/edit/restart, never edit a running script ·
**serial within a shard for any DOSE check (D65)** · report **kill round primary,
win rate secondary** with the informative band beside every number.

---

## ⚠ THE HONEST CEILING ON ALL OF IT

**This is self-play against our own bot, and `FIXTURE_OF_RECORD: live_unrated`.
65,000 local games CANNOT make a currency verdict.** What they can do is resolve
**mechanism and dose** at a precision the ladder will never reach in four days —
**and Part A tells us what the win-rate half is worth.** If Part A comes back
badly, Part B's 36,000 games were still not wasted: they measured behaviour, and
behaviour is what the ship rule's bar (b) needs.

## SEQUENCING

The 1,024-game counterbattery screens launched at 13:56Z finish ~14:47Z. **They
fill slot B3 and tell us whether either counterbattery arm is worth 7,300 games.**
The overnight run launches after they land, not before — spending a shard on an
arm we are about to learn is dead would be the same waste this plan exists to
stop.
