# Instrument audit — 2026-08-08 late (22:2x–22:4x CEST)

**Triggered by** `tools/audit_trigger.py` firing 2/4 (note:verdict 4.38, ship
cadence 0.32/hr). **Author:** short-lived audit session, no stake in the build
queue. **Scope:** can this project's instruments support the decisions it is
making? **Not a plank proposal. No ships, no verdicts, no bot edits.**

**Prior art deliberately NOT re-derived:** `v1` (n=120 leg has 19% power; the
blocked estimator is 1.06x), `v2` (gate↔ladder join unrecorded), `v3` (swap rule
is a timer), `v4` (map pool is ours), `v5`/`v5b` (0% bleed instrument coverage;
kill-rate vs kill-speed). Where my numbers reproduce theirs I say so and move on.

**Version tags.** Live slot at audit time: **v86 "Z2 fastfacing" (x3r0)**, tape
row 436. Bots code-read/run: `bots/_v97e11` (=v83), `bots/_v99mag` (=v84),
`bots/opp_v78`. Tools read at HEAD `b116fed`, including `tools/ceiling.py`
committed by session 20 ~20 minutes before this audit started.

**Machine:** 10 cores (8P+2E), load average 2.16 at start. All legs at 6 workers.
**Measured throughput this session: 2,019 matches/hr** (120 NOISE_ON matches,
15 maps × 2 seeds × 2 seats × 2 arms, 214 s) — consistent with the tape's
`cpu-headroom-corrected` figure of ~2,150/hr, so that row is confirmed, not
revised.

---

## Q1 — Can anything measure a change in core-kill rate or time-to-kill?

### The premise is already half-obsolete, and the new tool has a defect

`tools/ceiling.py` was built by session 20 at ~22:1x, before this audit began,
and it does measure per-arm core-kill rate. **I am not claiming that gap.** What
I found instead is a defect in its second column and a price list nobody has computed.

**FINDING 1a (defect, actionable now).** `ceiling.py:85` computes

```python
kills = [r for r in wins if r["condition"] == "core_destroyed"]
...  statistics.median(turns for kills)
```

— **turns-to-kill conditioned on having won by core kill. That is conditioning
on the outcome: a collider.** A plank that raises kill rate necessarily adds
*marginal* kills — games previously lost or ground to r1000 — and marginal kills
are slow. So the tool's two headline numbers move against each other **by
construction**, and a strictly better bot reads as ambiguous.

Demonstrated on this session's own leg (v83, 60 games vs `opp_v78`, kills at
turns `[106, 117, 121, 126, 169, 169, 184, 224, 230, 265, 404, 461, 481, 656, 729]`):

| synthetic improvement | kill rate | ceiling.py's conditional median | censored mean (correct) |
|---|---|---|---|
| baseline | 15/60 = 25.0% | 224 | 824 |
| +3 kills at turn 900 | 18/60 = 30.0% | **248 (+24, reads WORSE)** | **819 (−5, correctly better)** |
| +3 kills at turn 500 | 18/60 = 30.0% | **248 (+24, reads WORSE)** | 799 (−25) |
| +3 kills at turn 200 | 18/60 = 30.0% | 200 (−24) | 784 (−40) |

**Direction reversal on rows 2 and 3.** The fix is one line: replace the
conditional median with a **censored kill-time** — `turns` if we killed their
core, else `1000` — which is defined on every game and is monotone (any added
kill at any speed improves it). Report the **mean**, not the median: with kill
rate under 50% the censored median is exactly 1000 for both arms and carries
zero information (verified: both arms median 1000 in my leg).

*What would refute this:* if `ceiling.py`'s turns column is only ever read
alongside a stable kill rate, the collider cannot bite. It bit the moment the
tool is used for its stated purpose ("did this plank make us kill cores faster?"),
because that is a question about a plank that changes the kill rate.

### FINDING 1b — the ceiling metric is CHEAPER to measure than the metric we use

Measured on a real 120-match leg (v83 vs v84 vs `opp_v78`, NOISE_ON, `--tle 10`,
the project's standard grid), variance taken from the data, 80% power, α = .05
two-sided, independent games:

| endpoint | sd | target δ | n/arm | total matches | wall clock @2,019/hr |
|---|---|---|---|---|---|
| **kill-time censored@1000** | 328 | 50 turns | 676 | **1,352** | **40 min** |
| enemy units at end | 3.8 | 1 unit | 228 | 457 | 14 min |
| THEY kill our core (rate) | 0.45 | 5 pp | 1,174 | 2,349 | 70 min |
| WE kill their core (rate) | 0.47 | 5 pp | 1,316 | 2,632 | 78 min |
| ti margin (us − them) | 4,624 | 500 Ti | 1,341 | 2,682 | 80 min |
| **game share (what we use now)** | 0.48 | 5 pp | 1,484 | **2,967** | **88 min** |
| reaches r1000 (rate) | 0.50 | 5 pp | 1,536 | 3,072 | 91 min |
| enemy buildings at end | 33.1 | 3 bld | 1,908 | 3,816 | 113 min |
| ti delivered (us) | 6,449 | 500 Ti | 2,608 | 5,216 | 155 min |
| building deficit (ours − theirs) | 41.2 | 3 bld | 2,959 | 5,919 | 176 min |
| ti **stored** (never captured) | 5,066 | 20 Ti | 1,005,849 | 2,011,698 | inert |

And how well each tracks the thing we actually want (Pearson r with winning,
pooled n=120):

```
r(win, our buildings at end)   = +0.440      r(win, enemy buildings) = −0.114
r(win, building deficit)       = +0.566      r(win, enemy units)     = −0.136
r(win, ti margin)              = +0.538      r(win, turns)           = +0.110
r(win, kill-time censored)     = −0.510   (negative = faster kill → more wins)
```

**The recommendation, concretely: make censored kill-time the primary local
endpoint.** 40 minutes of existing CPU resolves 50 turns; |r| = 0.51 with
winning; defined on every game; monotone; no collider. It is **2.2× cheaper
than the game-share leg the gate currently runs** and it measures the metric
the project declared its ceiling four hours ago. Cheap-but-hollow warning:
"enemy units at end" is the cheapest line in the table (14 min) and is nearly
uncorrelated with winning (r = −0.136) — do not pick on price alone.

*What n would refute it:* if a real plank moves censored kill-time by < 25 turns,
the leg doubles to 5,400 matches (2.7 h) and the advantage over game share
evaporates. **Refuting number: a measured plank effect under 25 turns.**

*Honest limits.* (i) The variances come from **one** bot pair against **one**
opponent; a variance from n=60 has ~18% relative standard error, so every n in
that table is ±~40%. (ii) Nothing here says a local kill-rate gain transfers to
the ladder — `v2` established that join was never recorded, and it still isn't.
(iii) Ladder-side, the same endpoint is free (`turnsPlayed`/`winCondition` on
`fcode match info`), but see Q3: the ladder delivers ~30 games/hr, so 2,349
games is **3.3 days** of uninterrupted slot. **The ceiling metric is a local
instrument only.**

### FINDING 1c — the "~10 pp cross-batch spread" is ordinary binomial noise

I ran the **identical 60-cell grid twice** with the same binaries (verified:
`identical grid cells: True`).

| arm | run 1 | run 2 | Δ | in binomial sd |
|---|---|---|---|---|
| v83 | 32/60 = 53.3% | 34/60 = 56.7% | 3.3 pp | **0.37 sd** |
| v84 | 33/60 = 55.0% | 39/60 = 65.0% | 10.0 pp | **1.12 sd** |

`docs/tooling.md` treats a ~10 pp same-binary cross-batch spread as a
*phenomenon* requiring interleaved (`pair.py`) or deterministic-paired
(`det.py`) designs. It is what plain binomial noise at n=60/arm predicts, and
both runs land inside 1.2 sd. This also gives `v1`'s 1.06x pairing null a
**mechanism**: pairing cannot remove a batch effect that does not exist.
Independently confirmed here across seven endpoints — paired-difference sd ÷
unpaired sd ranged **0.88 to 1.13** (win 0.88, core-kill-win 1.07, r1000 1.06,
turns 1.05, censored kill-time 1.05, ti delivered 1.06, ti margin 1.13). On
several endpoints pairing is **worse** than not pairing.

*Caveat against my own claim:* n = 2 batches cannot exclude a small batch effect.
**Refuting number:** four more replicate runs of the same grid with a
between-run variance exceeding binomial by > 2× would reinstate the phenomenon.
That costs 4 × 214 s = 14 minutes and nobody has ever run it.

---

## Q2 — Ship cadence collapsed while notes rose. Which bottleneck?

**None of (a)–(d) as stated. The evidence points at (e): the trigger's two
firing signals are mis-measuring, and the real constraint is ladder bandwidth
(Q3).**

**(a) instruments too slow — REFUTED.** 2,019 matches/hr measured. The most
expensive useful leg in the Q1 table is 88 minutes. Not slow.

**(b) too underpowered to ever return a verdict — PARTLY, and already fixed
once.** `leg-power-19pct` is real, but `_v98hg-powered-verdict` (n=1,200) *did*
return a decisive result the same evening. The instrument returns verdicts when
run at scale; the project simply rarely runs it at scale.

**(c) a gate that cannot be satisfied — REFUTED by the tape.** The gate was
*loosened* at 19:40 and cadence went **up**: 6 distinct versions held the slot
between 19:42 and 22:22 (2.83 h) = 2.12 slot changes/hr, the highest rate on the
entire 53.5-hour tape. Whatever is wrong, it is not gate friction.

**(d) sessions choosing analysis over shipping — NOT SUPPORTED by the trigger's
own other two signals.** `doc:code churn` reads **0.79** (34,746 prose lines vs
44,128 code lines / 24 h) — below its 1.0 threshold, i.e. more code than prose.
`stuck planks` reads 2, below its threshold of 3. Two of four signals say the
opposite of the paralysis hypothesis.

### FINDING 2 — `audit_trigger.py`'s ship-cadence signal is broken, and it is one of the two that fired

```python
ships  = [r for r in rows if r[5]=="baseline" and "SHIP" in r[6][:60]]   # NO TIME WINDOW
recent = len(ships[-12:])                                               # all-time, capped at 12
active_hours = len(set(hours from `git log --since=24.hours`))           # hour-of-day buckets
rate = recent / active_hours
```

Verified against the tape:

- `ships` matches **6 rows in the project's entire history** — `v75-`, `v77-`,
  `v79-`, `v80-`, `v81-`, `v83-baseline`. v82, v84 and v86 all shipped and match
  **none** of them (v82 and v84 were recorded as `verdict` rows, e.g.
  `_v97hv-gate`, `_v99mag-gate`). The predicate depends on prose formatting of
  the first 60 characters of a free-text column.
- `recent` has **no time window**. `ships[-12:]` of a 6-element list is 6,
  forever, regardless of when those ships happened.
- `active_hours` = 19 today — the count of *distinct hour-of-day buckets* with
  any commit in 24 h, which measures **how long the day was**, not how long
  anyone worked.

So the metric is `min(12, all-time ship-row count) ÷ hours-of-today-with-a-commit`.
**Once a working day exceeds 12 active hours, with the current 6 matching rows,
the signal trips unconditionally: 6/13 = 0.46 < 0.50.** It cannot rise. Tonight
was the fastest shipping window on the tape (**1.77 own-ships/hr**, 5 activations
in 2.83 h) and the signal read **0.32/hr — understating by 5.5×**.

The trigger's own docstring calibrates it as "0.79 on the productive day, 0.46 on
the deadlocked one." Both readings are explicable by day length alone.

**FINDING 2b — the note:verdict ratio excludes ships from the denominator.**
Last-50 status mix is `note 27, verdict 8, caveat 8, baseline 7`. The
`decisions` set is `verdict|keep|discard|refuted|gate` — **`baseline` is not in
it**, and a `baseline` row *is* a ship, the most consequential decision the
project makes. Counting the 7 ships: 35/15 = **2.33**, not 4.38. Excluding
`caveat` from the numerator too (a caveat retracts a prior claim — it is a
decision, not new analysis): 27/15 = **1.80**. The signal is directionally real
but inflated ~2.4× by classification.

*What would refute Finding 2:* if `ship_cadence()` produced a value above 0.50 on
any day of this project's history under its current predicate. **Refuting number:
any day with ≥ 7 rows matching `status=="baseline" and "SHIP" in desc[:60]`, or
fewer than 12 distinct commit hours on a productive day.** Neither has occurred.

### FINDING 2c — the premise on which the ship gate was loosened is contradicted by `elo_history.tsv`

`docs/ship-gate.md` justifies the 19:40 loosening with: *"the project peaked at
1625 Elo / rank #21, then lost 57 Elo and 9 ranks in 15 hours with ZERO ships
while five planks sat in KEEP-dev."*

The tape: the 1625 peak is `2026-08-08T04:27` (rank #21, match 329). From there
to 19:42 is **15.2 h**, rating 1625 → 1568 (−57) and matches 329 → 420 (91 games)
— those two figures check out exactly. But the active submission over that window
was **v72 → v73 → v74 → v75 → v76 → v77 → v78 → v76 → v79 → v80 → v81: ten slot
changes.**

Either "ships" in that sentence means something narrower than "the bot on the
ladder changed" (plausibly "ships by this session"), or the causal story is
wrong. Either way **the −57 Elo was earned by ten different binaries, not by one
binary sitting still**, and "we bled because we did not ship" is not what the tape
shows. This matters because the entire gate rewrite — and the "ship the biggest
available change per window" rule that produced tonight's 2/2/5/1/7 windows —
rests on it. *Refuting number:* a per-version eloDelta ledger over 04:27–19:42
showing that the sum of the ten versions' deltas is dominated by one long-held
version. `exact-elo-delta-method` makes this a two-minute query; nobody has run it
on that window.

---

## Q3 — Is the project structurally incapable of evaluating its own ships?

**Yes. Stated plainly, with the arithmetic.**

Ladder feed rate, measured two ways and stable:

- whole tape: **310 matches / 53.5 h = 5.79 matches/hr**
- tonight 19:42–22:22: **17 matches / 2.83 h = 6.00 matches/hr**

At 6.0 matches/hr an 8-match window is **80 minutes**, so:

> **Maximum ship cadence compatible with an 8-match evaluation window:
> 0.75 ships/hr, i.e. one ship every 80 minutes, with zero slot contention.**

Tonight ran **2.12 slot changes/hr (6 versions in 2.83 h) — 2.8× oversubscribed.**
Consequence, forced: 17 matches ÷ 6 versions = **2.8 matches per version**, against
the 8 the rule needs.

**And this is not a tonight anomaly. Over the whole tape: 46 slot runs, mean 6.9
matches, median 5, and only 12 of 45 completed runs (27%) ever reached 8
matches.** Since v69 the runs read 7, 9, 6, 26, 6, 17, 11, 7, 5, 3, 1, 7, 23, 1,
3, 5, 1, 0, 6, 1. **The swap rule has been unable to arm on 73% of everything
this project has ever shipped, for its entire history.** `v3` measured what the
rule does *when it arms* (a coinflip); this is upstream of that — it usually
never arms at all.

**Contention is structural, not a discipline problem.** Three of tonight's five
window closures were not this session's decision: v81's window closed because
`submit` **auto-activates** (the tape says "not a choice"); v82's closed when a
peer Moonfarm session uploaded v83 at 20:20; v84's closed when x3r0 activated
v85 at 21:19. An 8-match window requires **80 minutes of uncontested slot
possession by a shared team account**, and the team ships more often than that.

**Even a completed 8-match window resolves almost nothing.** Using the tape's own
exact per-match figure (`exact-elo-delta-method`, n=100: mean −0.353, sd 9.273):

| window | sum sd | MDE (80%, α=.05) | per-match |
|---|---|---|---|
| 5 matches | 20.7 | 58 Elo | 11.6 Elo/match |
| **8 matches** | **26.2** | **73 Elo** | **9.2 Elo/match** |
| 20 matches | 41.5 | 116 Elo | 5.8 Elo/match |
| 50 matches | 65.6 | 184 Elo | 3.7 Elo/match |

The observed spread across every version on the tape is **v83 +6.8/match (best)
to v79 −5.2/match (worst) = 12.0 Elo/match**. So an 8-match window can *barely*
separate the best version ever shipped from the worst, and can separate nothing
finer. Resolving 2 Elo/match needs **169 matches = 28 hours** of uninterrupted
ladder.

**Two internally-consistent options, and the project must pick one:**

1. **Keep the 8-match rule → cap ships at 0.75/hr** (~18/day at full slot
   occupancy, shared with teammates, so realistically ~8-10/day for this arm) and
   accept that even then the window only catches ≥9 Elo/match effects.
2. **Keep shipping at ~2/hr → delete the 8-match rule** and stop describing the
   slot as evaluated. Rollback becomes a judgement call on 2-3 matches, which is
   what it has actually been for 73% of the project's history.

There is no third option at 6 matches/hr. **The number that would refute this:
a sustained ladder feed above 16 matches/hr**, which would make 8 matches a
30-minute window and reconcile both. The tape shows 5.79/hr over 53.5 hours with
no trend.

---

## Q4 — Free-lunch audit of the data surface

### 4a — The API (`fcode`), full sweep

Complete command tree, every field of every read-only endpoint, and the raw JSON
dumps are in this session's scratchpad. Only the unused/actionable parts are
reproduced here. **Nothing was submitted, activated, or downloaded.** Confirmed
inert: 20 plausible extra endpoints (`/api/ladder/history`,
`/api/teams/{id}/matches`, `/api/matches/{id}/games`, `/api/me`, `/api/stats`,
`/api/leaderboard`, `/api/elo-history`, …) all **404**. There is no hidden
rating-history endpoint.

**Highest-value finding — an active correctness trap:**

> **`fcode match info` returns the OPPONENT's version as `null`.** Only our side
> is populated (verified 10/10 sampled matches; e.g. `0ae5da15` — `match list`
> says `75 / 117`, `match info` says `75 / None`). **`match list` populates
> both.** `docs/tooling.md`'s s18 rule says to read "the next completed match's
> **meta** version stamp", and `docs/opponents.md` cites version stamps "from
> `match info`". Anyone following those literally gets `None` for the opponent
> and has no way to know a stamp was missing. **Every opponent version stamp
> must come from `match list`.**

**Fields that exist and no tool reads:**

| field | endpoint | what we do instead | verdict |
|---|---|---|---|
| `ratingABefore` / `ratingBBefore` | `match list` | poll `status` every 5 min into `elo_history.tsv`, then difference it (which `tooling.md` warns "averages within the gap" and "cannot attribute a match to a version") | **replaces the poller as a data source.** Combined with `eloDeltaA` and `teamAVersion` on the same row, the entire rating history is exactly reconstructible per-match, retroactively, from one paged pull. Keep the poller as a *wake trigger* only. |
| `mapConfig[].s3Key` | `match info` | fingerprint maps by dims + cores + ore + wall counts, after heart/eider and snowflake/archipelago collided and "cost a real conclusion" | **retires the map-identity trap.** `s3Key` is the map's sha256 — the same hash `maps list` returns. Exact, collision-free, available on any historical match including maps since rotated out. |
| `startedAt` | `match info` | infer ladder cadence from `createdAt` alone (`sweep_watcher.py`, the `:x2:43` rule) | separates *scheduled* from *picked up*; gives queue latency and true runtime. Directly relevant to the creation-time version-binding trap that forced three tape corrections. |
| `teamAMatchesPlayed` / `teamBMatchesPlayed` | `match list` | nothing | an opponent's match count *at that match*, so activity rate and games-since-version-bump need no poller. |
| `region`, `studentStatus`, `members[].country/affiliation/isStudent` | `ladder` | opponent modelling is entirely per-team | a free clustering axis (84 nordic / 29 non-nordic; 93 student / 20 non-student) for the class-weighted battery `ship-gate.md` asks for. Untested, one call away. |
| `errorMessage` | `match info` | nothing | the only place an opponent's crash text surfaces. |
| `ladderBanned` | `ladder` | nothing | free "did a rival get banned" signal (0 true today). |

**Pagination — the largest single unused capability:**

- `/api/matches` `limit` is **hard-capped at 100 server-side** (`limit=200` and
  `limit=500` both return 100). `ladder_census.py` passes `--limit 120` and is
  silently truncated to 100 — **its published "n=120 matches" figure is n≤100.**
- `cursor` is **not an opaque token — it is a `createdAt` timestamp**, and an
  arbitrary ISO-8601 string works, so you can seek to any point in history.
- History is **complete, not windowed**: paging `teamIds=<us>` to exhaustion
  returned **702 matches in 8 pages** (437 ladder + 265 unrated) back to our
  first match. The **global** feed reaches platform inception (2026-08-01).
- `teamIds` accepts **repeated params and ORs them**; comma-separated returns 0
  rows — a silent-zero trap.
- **No rate limiting observed on read endpoints** (~45 GETs, zero 429s). The
  5-per-10-min limit is on `match test`, a POST.

> **No tool in `tools/` passes `--cursor` or reads `next_cursor`.** Every census
> in `docs/research/` is computed over at most the most recent 100 matches, while
> ~8 days of the entire platform's history — every team, every game, every win
> condition, every seed — is one trivial cursor loop away at no cost. **`v5`'s
> "the archive cannot answer questions before it started collecting" applies to
> the *replay* archive; it does NOT apply to the API, which goes back to day
> one.** That reopens every retrospective question `v5` closed at game level.

**Confirmed NOT fetchable** (replays remain mandatory): per-team final titanium,
units, buildings, HP, entity placement, damage, per-round behaviour, `execTimeUs`.
`games[]` stops at outcome level, exactly as `game_census.py`'s docstring says.

### 4b — The LOCAL surface, which nobody has audited

`fcode run --json` emits **13 fields**, verified by dumping one match:

```
replay, winner, turns, win_condition, resign_message,
a_titanium, a_titanium_collected, a_units, a_buildings,
b_titanium, b_titanium_collected, b_units, b_buildings
```

What each runner keeps:

| tool | keeps | **discards** |
|---|---|---|
| `arena.py` | winner, seat, map, seed, condition, both `_titanium_collected` | **`turns`**, all `_units`, all `_buildings`, both `_titanium`, `resign_message` |
| `sprt.py` | same as arena | same as arena |
| `pair.py` | win, turns, cond, our Ti collected, **their** Ti collected, our units, our buildings | **their units, their buildings**, both `_titanium`, `resign_message` |
| `det.py` | win, turns, cond, our + their Ti collected, our units, our buildings | **their units, their buildings**, both `_titanium`, `resign_message` |
| `ceiling.py` | winner, map, condition, turns | **seat, seed**, everything economic |

`pair.py` and `det.py` both carefully keep the opponent's *titanium* and then
drop the opponent's *units and buildings* — the one pair of fields that says how
much of the enemy is still standing. **Nothing in the project has ever read
`b_units` / `b_buildings` from the losing side's perspective.** Priced in the Q1
table: enemy units at end resolves 1 unit in 457 matches (14 min) but is nearly
uncorrelated with winning (r = −0.136); the building deficit correlates best of
all continuous endpoints (r = +0.566) but costs 5,919 matches. **Free to capture,
not free to power.** Report it, do not gate on it.

`a_titanium` / `b_titanium` (*stored*, as opposed to collected) is emitted, never
captured by anything, and genuinely inert: sd 5,066 on a mean of ~2,160 means
2.0 M matches to resolve 20 Ti. **Recorded here so nobody spends an evening on it.**

---

## Top 3, as claims with their refuting numbers

**1. `audit_trigger.py`'s ship-cadence signal cannot measure ship cadence, and it
is one of the two signals that summoned this audit.** Evidence: the predicate
matches 6 rows in the project's entire history; `ships[-12:]` has no time window;
the denominator counts distinct commit hour-of-day buckets. On the fastest
shipping window on the tape (1.77 own-ships/hr) it read 0.32/hr. Refuted by: any
day in this project's history on which the current predicate returns > 0.50 —
which requires ≥ 7 rows formatted `baseline` + `"SHIP"` in the first 60 chars, or
a productive day under 12 active commit hours. Neither has occurred.

**2. At 6.0 ladder matches/hr, an 8-match evaluation window caps ship cadence at
0.75/hr — and the project has shipped faster than that for its entire history.**
Evidence: 5.79 matches/hr over 53.5 h; 6.00/hr tonight; 46 slot runs with mean
6.9 / median 5 matches, and **only 27% ever reaching 8**; tonight 6 versions in
2.83 h = 2.8× oversubscribed, with 3 of 5 window closures imposed by
auto-activation or teammates. Even a completed 8-match window only resolves
≥ 9.2 Elo/match against an all-version spread of 12.0. Refuted by: a sustained
ladder feed above **16 matches/hr**. The tape shows no trend in 53.5 hours.

**3. The ceiling metric is 2.2× cheaper to measure than the metric we currently
gate on — and `ceiling.py`'s speed column has a collider that reverses its sign.**
Evidence: measured on a 120-match leg, censored kill-time resolves 50 turns in
1,352 matches (40 min at 2,019/hr) with r = −0.51 against winning, versus 2,967
matches (88 min) for a 5 pp game-share move; and adding 3 slow kills to v83's
kill set raises kill rate 25% → 30% while `ceiling.py`'s conditional median reads
+24 turns *worse*. Refuted by: a real plank whose censored-kill-time effect is
under **25 turns**, which doubles the leg to 2.7 h and erases the advantage.

---

## Things I checked and found clean (recorded so nobody re-checks them)

- **Local throughput.** 2,019 matches/hr on 6 workers, NOISE_ON, full 15-map
  grid. `cpu-headroom-corrected` (~2,150/hr) is confirmed, not revised.
- **`doc:code churn` and `stuck planks`** did not trip (0.79 and 2). The
  paralysis hypothesis is not supported by the trigger's own other half.
- **Blocking turns on map identity buys nothing.** From 600 archived ladder
  replays: within-map sd / total sd variance ratio = **0.984** for core-kill
  games and **1.006** for all games. Map explains ~0-2% of turn variance. Same
  answer as `v1`'s 1.06x, on a different quantity and a different corpus.
- **The archived-replay turn distribution** (n=300 sample of `replay_archive/`):
  `core_destroyed` 225 (75%), mean 265 / median 194 / sd 210 turns;
  `titanium_collected` 70, all at exactly 1000; `harvesters` 3; `titanium_stored` 2.

## Raw data

Scratchpad (session-local, dies with this session — copy anything you need):
`pair_audit.json` (120 matches via `pair.py`), `fullcap.json` (120 matches, all
13 emitted fields), `turns.py` / `icc.py` (archive census), `endpoints.py`
(endpoint cost table), `slots.py` (slot-run arithmetic), `fullcap.py`, plus the
API sweep dumps (`status.json`, `ladder.json`, `subs.json`, `maps.json`,
`all_mine.json` = full 702-match history, `match_info.json`, `tests.json`,
`team_info.json`, `team_search.json`).

**Every number above should be re-derived against primaries before it changes a
decision.** Three of my four sections contradict something currently written in
`docs/`, and I am one session with one evening's data.
