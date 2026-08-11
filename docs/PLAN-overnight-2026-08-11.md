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

---

# AMENDMENT 1 — PART A IS REGISTERED AS A **FALSIFIER**, NOT AN ESTIMATOR
### 2026-08-11 ~14:0xZ, BEFORE ANY CALIBRATION GAME IS RUN

**Raised by the side lane against their own proposal, and it is STRONGER than
what either of us had — not a retreat.**

**THE PROBLEM IT SOLVES:** my correction #2 said the four ladder ratings are not
contemporaneous, so the six residuals confound *"local does not predict the
ladder"* with *"the field changed between eras"*. **That objection does not go
away for v92/v102/v104 either** — sweep 22 measured the field itself strengthening
over time, so v92's 1531 and v104's 1672 were set against different fields. **As
an ESTIMATOR, Part A is confounded no matter which three versions I lean on.**

**⭐ BUT ERA CONFOUNDING CAN BEND AN ORDERING. IT CANNOT INVERT ONE.** So the
question is re-registered as a falsification test, and the bar is pre-committed
here, before a single calibration game has been played:

| outcome | verdict |
|---|---|
| **local ranks the ladder-WORST bot as locally BEST**, or the six residuals are **large and unsigned** | ⛔ **LOCAL SCREENS DO NOT PREDICT THE LADDER.** Stop screening for the rest of the week; **ship on mechanism alone.** |
| ordering holds and residuals are modest | **FAILED TO FALSIFY.** Screens are *consistent with* predicting the ladder. **NOT proof, and the write-up must say so in those words.** |

**A falsifier survives a confound that would destroy an estimator.** The
inversion test needs no assumption that the two eras are comparable — only that
a genuinely better bot does not read as worse.

**⇒ THE SIX RESIDUALS ARE STILL COMPUTED AND REPORTED**, because their SIGN and
SPREAD are informative even when their level is not. They are simply no longer
the thing the decision hangs on.

## ⇒ ROUTED TO RESEARCH — THE LADDER SIDE SHOULD NOT BE A RATING SNAPSHOT

**Zero cores, runs while the machine is busy, and it is the fix that would make
the residuals mean something.** We hold **~2,345 ladder games with per-match
opponent, our version, and both ratings**. ⇒ **Estimate each version's strength
as a VERSION EFFECT WITH OPPONENT CONTROLS, from per-match data, instead of
reading whatever rating that version happened to be sitting on.** That removes
most of the era confound on the ladder side, and research already has the
decoders. **If it lands before the read-out, Part A upgrades from a falsifier
back to an estimator. If not, the falsifier stands on its own.**

---

# AMENDMENT 2 — PART A RESIZED 4 SHARDS → 1; B3 FILLED; COUNTERBATTERY DEAD
### 2026-08-11 ~14:1xZ

## 2a. THE 14:10Z COUNTERBATTERY RESULT — BOTH ARMS DEAD, B3 IS NOT THEM

| arm | n | win rate | band | verdict |
|---|---:|---:|---|---|
| `_v149cbfull` (`LOKI_QUIET_ON = False`) | 1024 | 49.6% | 46.9–53.1 | **NO INFORMATION** |
| `_v150cbturret` (counterbattery, turrets only) | 1024 | **45.2%** | 46.9–53.1 | ⛔ **REAL NEGATIVE** |

`_v150cbturret` core kills **449 FOR / 546 AGAINST = 0.82×.** Seat A 48.6% /
seat B 41.8% against a null baseline of 53.8% seat A — **worse in BOTH seats**,
so it is not a seat artefact.

**⛔ THE MECHANISM ERROR IS MINE AND THE CODE SHOWS IT.** I argued: *25.76% of
builder-rounds are idle, so an idle builder swinging at an adjacent turret costs
ZERO movement.* **`raid.py:193` is `if ct.get_action_cooldown() == 0 and
self._raid_act(...): return` — `_raid_act` returning True RETURNS FROM THE TURN
AND MOVEMENT NEVER HAPPENS.** Placing counterbattery LAST in the ranking does not
make it free; it still converts a move-round into an attack-round.

⇒ **The 25.76% figure counts rounds where the bot EMITTED nothing, NOT rounds
where movement was unavailable. It never refuted LOKI-QUIET's premise, and I
treated it as though it had.** **LOKI-QUIET's original rationale — acting and
moving are mutually exclusive, arrival is the scarce quantity — is REVALIDATED
under the current currency**, which had never been rechecked.

**⇒ TERM `A` REMAINS THE LARGEST TARGET ON THE BOARD (1.77×, 47.3% of the log
hazard gap). What is refuted is BUYING IT WITH BUILDER MELEE.** Any future
attempt must reduce enemy turrets **without spending a raider's move** — which
points at turrets shooting turrets, or at not being adjacent in the first place.

## 2b. PART A RESIZED — 4 SHARDS → 1, AND THE REASON IS A MISSING LADDER SIDE

Research's opponent-controlled version effects (`2c261c8`), estimated off
per-match data rather than rating snapshots:

```
v92  1600 [1520,1681]   v102 1609 [1578,1641]   v104 1686 [1656,1717]
v112 -- NOT ESTIMABLE (zero archived ladder games) --
```

* **v104 − v92 = −86, CI [−169,−5] → SIGN RESOLVED** ✅
* **v104 − v102 = −77, CI [−125,−29] → SIGN RESOLVED** ✅
* **v92 − v102 = −9, CI [−104,+71] → NOT RESOLVED** ⛔
* **v112's three pairings → NO LADDER ESTIMATE EXISTS AT ANY LOCAL n** ⛔

**⇒ ONLY TWO OF SIX PAIRINGS HAVE A LADDER SIDE TO PREDICT, AND 65,000 LOCAL
GAMES DO NOT FIX A MISSING ONE.** The two scoreable gaps are **86 and 77 Elo ≈
12pp and 11pp**, resolvable at **n ≈ 500–1,000 each** — not 4,800.

⇒ **PART A: 1 SHARD (v104-vs-v92 and v104-vs-v102 only). ~3 SHARDS ≈ 22,000
GAMES FREED FOR PART B.**

**⭐ AND THE EXERCISE PAID FOR ITSELF BEFORE A GAME WAS PLAYED:** on raw snapshots
**v92 1552 < v102 1600**; opponent-controlled they are **indistinguishable**.
**A residual scored against snapshots would have counted a real local v102 > v92
result as a HIT against an ordering that does not exist** — the falsifier graded
on a fiction, in 1 of 6 cells.

⚠ **Carried against my own reallocation:** at n≈1,000/pairing the LOCAL side is
precise and **the LADDER side stays binding** (±80 and ±48 Elo). **More local
games cannot narrow that. Part A is cheap by necessity, not by choice.**

## 2c. NO LLM DURING THE RUN — A SHELL WATCHDOG, NOT A BABYSITTER

Magnus: *"the overnight runs need to be running without our arms and perhaps with
a sonnet agent or something that makes sure it works well but doesn't steal too
many tokens."* ⇒ **Adopted, and cheaper than offered: ZERO LLM invocations on a
healthy night.** Overnight failures here are **assertion-shaped, not
judgment-shaped** — a dead shard needs a restart, not a thought.

1. **Per-shard HEARTBEAT**, overwritten each game: `ts · games_done · TARGET_N ·
   shard_id`. **TARGET_N is written BEFORE the run so partial output can never
   read as complete.**
2. **Shell watchdog, every 2 min**: heartbeat older than ~3 min, or process gone
   before target ⇒ **restart (bounded, 3 attempts)** and append to an ALERT file.
3. **COMPLETION MARKER per shard, written only on reaching TARGET_N**, and **the
   morning read-out REFUSES to pool a shard without one.** *Silent truncation
   reads as "covered everything".*
4. **The garbage-detection checks go in the RUNNER as assertions, not to an
   agent** — null arm near 50%, seat split near even, more than one map present,
   win rates non-degenerate. **If it can be an assertion it should not be an LLM.**
5. **One sonnet agent in the MORNING** to assemble the read-out. That is where
   judgment actually is.
