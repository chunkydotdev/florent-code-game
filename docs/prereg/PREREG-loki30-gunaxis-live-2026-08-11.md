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
