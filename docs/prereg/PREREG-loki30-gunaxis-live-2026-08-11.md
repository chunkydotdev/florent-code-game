# PREREG — LOKI-30: THREE ARMS (v104 · v112 · gunaxis) AGAINST TWO LIVE CELLS WE LOSE TO

## ⭐⭐ 0. THE REASON THIS LEG IS NECESSARY RATHER THAN NICE — THE ARCHIVE IS STRUCTURALLY CONFOUNDED IN BOTH CELLS

**Magnus asked to "compare v104 vs them so we see if we improve." THE TAPE CANNOT
ANSWER IT.** Cross-tabulating OUR version against THEIR version over every rated
game (`league_matches.tsv`, which carries both; **never
`ladder_games.tsv.oppver`, NULL for these cells**):

**The Bisons — perfectly collinear.**

| our version | their v1 | v2 | v3 | v4 |
|---|---|---|---|---|
| v45 · v47 · v80 · v87 · v91 · v92 | 5/5, 4/5 | 11/15, 4/5, 4/5, 4/5 | 4/5 | **—** |
| **v102 · v104 · v112** | — | — | — | **7/30 · 9/20 · 1/5** |

**Every modern bot we own has met ONLY their v4. Every bot of ours that beat them
met ONLY v1–v3.** We read 73–80% against their v2 and 20–45% against their v4.
*"We regressed"* and *"their v4 is much better"* **fit these 120 games
identically.** This is the confound `CLAUDE.md` names for this exact opponent —
their v4 shipped ~40 minutes before our v102's first ladder game.

**Focalground — worse, and it spans two changes in one step.**
v104 met **only their v10** (21/50 = 42%). **v112 has met only their v11** (3/5).
They shipped v11 and v112 is the only bot of ours ever to face it.

⇒ **A v104-vs-v112 comparison off the archive measures our change and theirs
simultaneously, in both cells. It is not underpowered — it is UNIDENTIFIED.**

⇒ **THE LEG'S PRIMARY VALUE IS THE DESIGN, NOT THE n: three arms against the SAME
opponent version inside the same window.** That is a within-opponent-version
contrast the archive can never supply at any n, and it is why this is worth a
window even though §2 says the currency will not resolve.
⚠ **The design's validity depends on the opponent NOT shipping mid-leg.**
Focalground is a frequent re-versioner (11 versions). **Their version is asserted
per match from `league_matches.tsv` at read-out; if it changes inside the window
the arms straddle it and the contrast is void — checked, not assumed.**

---

# THE ARMS

**Author:** builder arm, s32. **Committed BEFORE leg creation** (two-clock: this
file's git author time vs the platform `createdAt` of the first challenge).
**Magnus, direct, 2026-08-11:** *"I would definitely throw it at the unrated
ladder for a bunch of games to verify it wins against bots we lose against… it
would be interesting to see what maps we are able to turn into wins"* and
*"compare v112 vs The Bison and the focalground with this new gunaxis and see if
we can flip one or more maps on our side. They are keeping us just below 1700."*

**TARGET BAND: The Bisons (1704, gap +15, 5-0 pays +16.7) and Focalground
(1720, gap +31, 5-0 pays ~+17.6) — both inside the reachable band `us−80 .. us+125`
at our 1689. Gaps +15..+31, win pays +16.7..+17.6. REACHABLE: YES.**
*(For contrast, the s28 leg that motivated this gate was aimed at teams paying
0.25–1.18. These two pay 14–70× that.)*

## 1. WHY THESE TWO CELLS — and it is Magnus's criterion, not rating proximity

Both are teams **we lose to**, both sit just above us, and both are named by him
as holding us under 1700. Off `ladder_games.tsv` (the rated-record surface;
**never `meta_join`**, which pools unrated):

| cell | rating | gap | our game share, all versions | v104+ era |
|---|---:|---:|---|---|
| The Bisons | 1704 | +15 | 56/120 = 46.7% | 10/25 = 40% |
| Focalground | 1720 | +31 | 33/75 = 44.0% | 24/55 = 44% |

⚠ **Per-opponent shares are quoted to ONE decimal at most and are known to read
HIGH** (s30: a team scores materially less against an opponent's LATER versions;
direction replicates across four estimators, magnitude spans 1.8× and must never
be applied as a numeric correction).

## 2. ⛔ WHAT THIS LEG CANNOT DO, STATED FIRST BECAUSE IT IS THE THING MOST LIKELY TO BE OVERCLAIMED

**PER-MAP FLIPS ARE NOT RESOLVABLE BY THIS INSTRUMENT AT ANY SESSION-LENGTH n.**
* The platform caps us at **5 unrated matches / 20 min = 75 games/hour**, shared
  across every runner and lane.
* Detecting a **+10pp** pooled shift vs ONE team needs **~390 games per arm per
  team** ⇒ ~1,570 games for the 2×2 ⇒ **~21 hours**.
* A **one-hour** leg gives ~75 games ⇒ **MDE ≈ 23pp** pooled, and **~1 game per
  map per cell.**
* The existing archive already has 120 (Bisons) and 75 (Focalground) games and
  its per-map cells are still only **3–12 games**.

⇒ **The map table this leg produces is DESCRIPTIVE and hypothesis-generating.
Any sentence of the form "map X flipped" is forbidden in the read-out.** The
per-map archive cut below is the better instrument for *which* maps to care
about, and it is free.

**AND THE MAP EFFECT IS OPPONENT-SPECIFIC, MEASURED, WHICH IS WHY POOLING WOULD
HIDE IT:** `eider` is **8/8 (100%) vs The Bisons** and **0/5 vs Focalground**.
`jackpot` 1/4 vs Bisons, 0/6 vs Focalground. **The same map inverts between the
two cells.** This reproduces s30's finding that the map × opponent interaction
cancels in every pooled statistic we compute. ⇒ **maps are reported PER CELL,
never pooled across the two.**

## 3. THE PRIMARY, AND IT IS THE ONE THAT ACTUALLY RESOLVES AT SMALL n

**DOES `_v146gunaxis` SURVIVE THE PLATFORM'S 10 ms PER-TURN CPU LIMIT?**

The arm adds, per raider turn, a `ct.get_attackable_tiles_from(gp, gd, GUNNER)`
call **for every nearby enemy gunner**, accumulating a `gun_axis` set
(`raid.py:501-526`). **Local `fcode run` measures a chassis the platform does not
have** — the default `--tle` is 0, and `doctrine.py` records that
`get_cpu_time_elapsed()` reads 0 locally. **This is exactly how `best-fit` died:
6/6 with the limit off, 5/6 with it on.** Tonight's 5,408-game result was
produced under `--tle 10` locally, which is better, but still this laptop's
timing rather than the platform's.

* **BAR: zero timeout-attributable unit losses, and no per-game collapse in unit
  count relative to the v112 arm.** A TLE'd turn does nothing; a bot losing turns
  loses builders and buildings, which is visible in the replay entity counts.
* **RESOLVES AT SMALL n** — a CPU regression that costs 5/6 games shows in ~10
  games. **This bar GATES the rest: if it fails, the currency numbers describe a
  bot dying to the clock and mean nothing about siting.**
* ⛔ **READ IT ENGINE-SIDE, off entity/removal events — NEVER off `print()`.**
  The platform strips stdout: 0 of 30,664 `BotOutput` events carried it.

## 4. SECONDARY — DIRECTIONAL CURRENCY, EXPLICITLY UNDERPOWERED

Game share per cell, **THREE arms — v104 (`_v130loki13`), v112
(`_v148ferryfirst`, the incumbent), and gunaxis (`_v146gunaxis`)** — against the
same two opponents, **round-robin by arm** so all three sample the same
wall-clock and the same opponent version, and so a mid-leg version change hits
every arm equally rather than the arm that happened to run last.
**Arm order is ROTATED each cycle** so a drift in the opponent's form cannot land
on one arm systematically.

* **Reported as a POINT ESTIMATE WITH ITS INTERVAL, and the MDE printed beside
  it.** At the n this leg will actually reach, **the interval will contain both
  zero and the effect size we care about.** That is stated in advance so it is
  not discovered afterwards.
* **NO VERDICT LANGUAGE.** "null", "refuted", "confirmed", "flipped" are
  forbidden. The admissible sentences are *"consistent with"*, *"did not
  resolve"*, and *"the point estimate is X with interval Y"*.
* **`WIN_RATE_IS_VERDICT: yes` governs the SHIP, and this leg is not sized to
  supply it.** Tonight's 5,408-game self-play already gave the powered currency
  read; **this leg exists to check the live chassis and to sample the field.**

## 5. WHAT WOULD MAKE ME STOP THE LEG

1. **Any timeout-attributable loss** ⇒ stop, the plank has a CPU regression, and
   that is a finding rather than a failure.
2. **A holder-assertion failure** — `unrated_run.sh` aborts unless the holder is
   `v$MAIN`; `MAIN` was 104 and stale until s32 and is now 112.
3. **Rated leakage beyond budget.** Cost is real and measured at **~−8 Elo per
   leaked rated match**, not zero. The runner activates for the window and rolls
   back, verifying on the `Active bot:` line and never on `$?`.

## 6. VERSION PINNING, BOTH SIDES

* **OURS:** per-match `ourver` at the pairing boundary from `--json createdAt`,
  read off the LIVE CLI. **Never the `match list` table** (Date column lags
  ~2 min) and **never `elo_history.tsv`** (tags by version active at POLL time).
* **THEIRS:** `league_matches.tsv`, **not `ladder_games.tsv.oppver`, which is
  NULL for these cells and reads as "no version change" to any cut that trusts
  it.** Both opponents' version timelines are recorded before the read-out.
  ⚠ Focalground is nominated in the archive as a cell that **re-versions often**;
  if it ships inside the window, the two arms straddle a version change and the
  comparison is confounded. **That is checked, not assumed.**

## 7. ARCHIVE CUT — THE FREE HALF, ALREADY DONE, PRE-REGISTERED HERE SO IT IS NOT RE-CUT AFTER THE FACT

Per-map game share, all versions (n in parentheses):

**The Bisons** — worst: saga 1/6 · heart 1/5 · jackpot 1/4 · nordkap 2/7 ·
hive 2/6 · drumlin 2/6 · snowflake 3/8 · lighthouse 4/9 · atoll 4/9.
Best: **eider 8/8 · antler 10/12 · fjordgate 5/8.**

**Focalground** — worst: **eider 0/5 · jackpot 0/6** · lighthouse 1/4 ·
atoll 2/7 · moonrise 2/6. Best: antler 3/3 · saga 5/6 · nordkap 5/7.

**These are the maps a future powered leg would target. They are NOT this leg's
bar** — every cell is 3–12 games and several are 0/n, where the point estimate is
0% and the interval reaches past 40%.

---

# AMENDMENT 1 — **MY PRIMARY BAR COULD NOT FIRE.** Replaced, n fixed, leakage repriced. Committed BEFORE leg creation.

## A1.1 ⛔ THE GATING BAR WAS A GUARD THAT FIRES ON NOTHING

§3 read: *"BAR: zero timeout-attributable unit losses."* **There is no such
event.** `CLAUDE.md:13`: a CPU overrun means *"that turn's `run()` is interrupted
and does not resume next turn. **This is different from an uncaught exception**"*;
`CLAUDE.md:430`: *"an escaping `GameError` kills the unit; **a CPU timeout does
not.**"*

⇒ **A timeout costs a TURN, never a UNIT.** The bar reads **zero under a healthy
bot and zero under a bot timing out on every single turn** — and I made it the
clause that GATES the leg. That is this session's most-repeated defect, written
by the person who spent the session flagging it in other people's instruments.
The second clause (*"no per-game collapse in unit count"*) was doing the real
work, is indirect, and *"collapse"* had **no threshold** — the same undefined-bar
defect as Part A's *"large residuals"*.

## A1.2 ⭐ THE REPLACEMENT IS DIRECT, AND MY OWN CORRECTION DOCUMENTED IT

The s28 print-stripping finding (`CLAUDE.md:28`) records that platform replays
carry **30,664 `BotOutput` events of `{id, execTimeUs}`** — **stdout is stripped;
`execTimeUs` is NOT.** That is the CPU cost of every unit-turn, **engine-side, on
the platform's own chassis**, in the replays this leg downloads. The instrument
was two lines from the sentence I wrote about stdout.

**NEW PRIMARY — per-turn `execTimeUs`, gunaxis arm vs v112 arm:**

| statistic | bar |
|---|---|
| **count of turns ≥ 10,000 µs** | **0 for gunaxis, or gunaxis ≤ v112** |
| **p99 execTimeUs** | gunaxis ≤ **1.5×** v112 |
| **max execTimeUs** | reported; a max ≥ 10,000 µs is a FINDING regardless of count |

**Resolves at TENS OF TURNS, not tens of games** — a 60-game leg yields on the
order of 10⁵ unit-turns per arm. **It measures the platform chassis, which is the
entire reason §3 exists** (local `--tle` is this laptop's timing), and it makes
the *best-fit* precedent **directly comparable rather than analogous.**
**Driven both ways:** v112 is the incumbent and is known not to TLE, so a
non-zero ≥10,000 µs count on the v112 arm would indict the INSTRUMENT, not the
plank. **That cell is the negative control and it must read ~0.**

## A1.3 ⛔ THE PREREG DID NOT FIX ITS n — AND THE EXPOSED SURFACE IS THE MAP TABLE

Nothing said when a HEALTHY leg ends; §5 listed only failure-triggered stops.
**An unfixed n permits optional stopping, and the per-map table is exactly the
kind of thing that can be extended until a cell looks interesting.**

**FIXED NOW: 12 matches — 2 per arm-cell across 3 arms × 2 opponents — = 60
games, ~50 minutes at the 5-per-20-minute cap.**
* **The leg STOPS at 12 accepted matches** whatever the map table shows.
* **If cut short**, the read-out reports what was fired per cell and **the leg is
  not extended to complete a cell that looks interesting.**
* **No interim read of the currency or the map table.** The `execTimeUs` primary
  MAY be read early — it is a safety gate and stopping on it is a stop-for-harm,
  not optional stopping.

*(This is the LOKI-16b miss verbatim, and the side lane recorded that it was
theirs: they audited that prereg for provenance, estimator, clustering unit, map
stratum and control, reported no flags, and never asked how many games it fires.)*

## A1.4 TWO OF THREE ARMS ARE NON-INCUMBENT — THE LEAKAGE BUDGET WAS UNDERSTATED

§5.3 priced leakage generically. **v104 AND gunaxis are both non-incumbent, so
~2/3 of the window is exposed, not 1/3.** The s28 measurement is the anchor:
**−24.67 Elo across 3 leaked matches**, one by an arm later measured at −14.7pp,
**and the discriminator was the ACTIVATION TIMESTAMP, not the version tag.**

* **BUDGET: ≤ 2 leaked rated matches (~−16 Elo worst case).** Exceeding it stops
  the leg.
* **Leakage is verified per-match on `ourver` at the PAIRING BOUNDARY** from
  `--json createdAt` on the LIVE CLI — **never the match counter** (blind to
  pairing), **never `elo_history.tsv`** (tags by version active at poll time),
  **never the corpus** (lags the platform by up to an hour).
* `unrated_run.sh` serves the rate-limit wait with the INCUMBENT live and
  activates only inside the window; the pairing-clock offset is **re-derived from
  recent rows, never hardcoded** — it has shifted at least once inside 18 hours.

# AMENDMENT 2 — BAR ON THE WIRE'S OWN `tled` BOOLEAN, NOT ON A THRESHOLD I CHOOSE. Committed before any replay is read.

**A1.2's bar counted `execTimeUs ≥ 10,000` as a proxy for a flag that is sitting
in the NEXT FIELD.** `botOutput` carries **`execTimeUs` in field 3 and a `tled`
BOOLEAN in field 4** — `tools/corpus/replay_econ.py:93-97` reads
`us = d.get(3)` then `if d.get(4): c["tled"] += 1`; `tools/crash_census.py:63`
already reasons off `botOutput.tled` directly.

**AND THE PROXY HAS A NAMED FAILURE MODE IN BOTH DIRECTIONS.** `CLAUDE.md:13`:
the 10 ms limit carries **"a small rolling 5% buffer"**, so the cutoff is not
exactly 10,000 µs. A turn interrupted at 9,800 µs is `tled=True` and **below** my
threshold; a 10,200 µs turn inside buffer is **above** it and not TLE'd.
⇒ **the proxy misses precisely on the marginal turns a CPU regression produces
first**, which is the population the bar exists to catch.

**REVISED PRIMARY — one row swapped, the other two unchanged:**

| statistic | bar |
|---|---|
| **count of `tled` turns** *(the wire's own answer — no threshold to choose)* | **0 for gunaxis, or ≤ v112** |
| p99 `execTimeUs` *(leading indicator, kept)* | gunaxis ≤ **1.5×** v112 |
| max `execTimeUs` *(kept)* | reported; near the limit is a finding |

**AND THE NEGATIVE CONTROL NOW HAS A PUBLISHED PRIOR VALUE RATHER THAN AN
EXPECTATION.** `tled` is column 10 of `corpus/econ.tsv` and is **not a dead
column** — 8,623 of 118,524 rows nonzero (7.28%), 2,153,335 TLE'd turns total —
against `QUEUE.md:61`'s **`tled` 0.00% for us vs 1.52% on the field.**
⇒ **v112 must read ~0.00%, matching our measured field-wide zero. A nonzero there
indicts the INSTRUMENT, not the plank.** The "a constant column validates
anything" check is therefore already passed, on the live corpus, before this leg
reads a byte.

*(`tools/cpu_lag_probe.py` already counts `tled` and `replay_econ.py` already
aggregates it per game — this is a column selection, not a decoder to write.)*

## LEG STATE AT AMENDMENT TIME
**Cycle 1 fired 19:06:47–19:06:50Z**: v114 vs The Bisons (`db5f1812`) and vs
Focalground (`988554e3`), 10 games, 2/2 accepted, 0 rejected.
**Rollback confirmed at 19:06:55Z on the `Active bot:` line** — v114 held the
slot for **8 seconds**, against observed pairings at 18:52:59Z and 19:12:59Z
(minute ≡ 12 mod 20, second :59, ten consecutive rows, **re-derived tonight and
not hardcoded**). **Rated leakage is expected to be ZERO and will be verified
per-match at the pairing boundary rather than asserted from that arithmetic.**

# AMENDMENT 3 — THE SHIP INVERTED THIS LEG'S EXPOSURE PROFILE (and made it cheaper)

**§5.3 and A1.4 priced the leg with gunaxis as the PROTOTYPE needing activation.
It is now the INCUMBENT (v114, 19:14Z), so the gunaxis arm costs NOTHING** — it
holds the slot already. **v104 and v112 are now the exposed arms.** Still 2 of 3
non-incumbent, but **the plank under test is the free one and the CONTROLS are
the expensive ones**, which is the reverse of what was priced. `MAIN` 112→114
already handles the holder assertion. **Budget unchanged at ≤2 leaked rated
matches; the arm-rotation cost model in A1.4 now describes the old world.**

# ⭐ OBSERVATION, NOT A BAR — WE ARE BEING SCOUTED, AND THE OPPONENT IS ITERATING FASTER THAN OUR STATISTICS

`fcode match list --mine` at 20:30Z, reading the OPPONENT's version column:

    19:16:03   SmartFridge v28  vs v114   we took 3/5
    19:38:03   SmartFridge v30  vs v114   we took 2/5
    19:52:59   SmartFridge v34  vs v114   we took 1/5
    20:27:06   SmartFridge v35  vs v114   we took 2/5

**v28 → v35 in seventy minutes**, and the off-slot timestamps (19:16:03,
19:38:03, 20:27:06 — not the `:12:59/:32:59/:52:59` ladder cadence) are **unrated
matches THEY initiated against US.** The platform never says who started a match
(`triggeredBy` is the TYPE, not the actor), so this is inferred from the cadence,
not read — **but the version churn is read directly and is not in doubt.**

**TWO CONSEQUENCES, both about our measurement rather than about them:**
1. **Any per-opponent statistic we hold on SmartFridge is stale on arrival.**
   D18 already says a team scores materially less against an opponent's LATER
   versions; here the later version arrives every ~20 minutes. **Their cell was
   already the one where five independent defects landed in LOKI-19.**
2. **This is the collinearity problem accelerating**, not a new one: we cannot
   grade our own ships against a cell that re-versions faster than we accumulate
   games in it. ⇒ **prefer STABLE opponents for measurement and treat SmartFridge
   as a live sparring partner, not as a yardstick.**

⚠ **NOT A CLAIM ABOUT INTENT.** *"They are scouting us"* is one reading; another
is that they run their own unrated screens against whoever is adjacent and we
happen to be adjacent. **Nothing here distinguishes those and no plank should be
built on the difference.** What IS established: their version churn, and that our
per-opponent numbers on that cell decay faster than we can measure them.
