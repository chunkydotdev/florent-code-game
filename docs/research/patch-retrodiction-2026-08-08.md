# PATCH-RETRODICTION BACKTEST — is the CONTENT of an opponent's next version predictable?

**Research arm, 2026-08-08 evening. Archive snapshot: 458 matches / 2,291 replays,
`completedAt` 2026-08-07T10:28:49Z .. 2026-08-08T10:45:16Z. Our live version at time of
writing: v76.** No games run, nothing downloaded — archive metas + existing decoded
research docs only. (The archiver added 8 matches mid-analysis; all numbers below are on
the refreshed snapshot, and one of those late matches turned out to be the single most
important data point in the study — see CtrlAltDefeat.)

---

## VERDICT LINE

**Patch CONTENT is not predictable. Patch DIRECTION is weakly predictable. Patch
REVERSION is strongly predictable, and reversion is the only one of the three that is
cheap to exploit.**

| Team | Predictable? | One-line reason |
|---|---|---|
| **CtrlAltDefeat** | **No (content) / Yes (state set)** | Two consecutive forward steps moved economy in **opposite** directions; but the bot lives in a closed set {v107, v116, v117} and has now returned to v107 |
| **Lunds Stallions** | **No — nothing to predict** | Opening fingerprint **invariant across all four stamps** (v37/v42/v45/v44) in the opponent-controlled view; win-rate vs us flat at 73–75% |
| **Powerpuff Girls** | **Partially** | Direction after a 0–25 wipeout was guessable ("harden"); the mechanism (first barriers they have ever fielded, 0 → 9.5/game) was not |
| **Kings College Munich** | **Yes — by predicting stasis** | v7 went 0–10, reverted to v1 in 50 min, and has not moved in the 18 h since (13 matches) |
| **Ouroboros (control)** | **Yes — nothing changes** | One stamp (v8) for the whole 24 h window; census fingerprint dead flat over 50 games against 9 different versions of ours |
| **0033** | **Partially — the one clean REACTIVE hit** | Lost 17/17 games by core-kill, then shipped barriers + deferred sentinel + more economy; win-rate vs us 15% → 70% |
| **Powered by SmartFridge** | **No — but the state set is fully enumerated** | 9 stamps, **10 real rollbacks**, 29 stamp-runs in 24 h. Not a patch series; a rotating stable |
| **team lazy / gsxWins / Landers / Banminary / Tyvrets / Kleos / Leviathan / kladde** | **No (content) / Yes (revert)** | Each shipped a build that cratered on a self-test sweep and was reverted within 30–90 min |
| Linear developers (Pantheon, Jython, Pivot, Erebus, not adgato, Lorem Ipsum, Flotte, I Stone, O(1), Coreflood, ArjunWorks) | **No** | Steps are mostly below the census instrument's resolution — see the sensitivity floor below |

---

## 0. THE SENSITIVITY FLOOR — read this before believing any "nothing changed" verdict

The instrument is `tools/replay_census.py` at census resolution (first-build rounds,
end-of-game entity mix, win condition). Its false-negative rate was measured **on our own
patches, against a frozen opponent**, which is the strongest calibration available:

**Our own v64 → v75 (nine consecutive shipped versions, every one a real code change with
a local battery behind it), all seen through the census, all against Ouroboros v8 (which
never changed), 5 games per version:**

| metric | v64 | v65 | v67 | v68 | v69 | v72 | v73 | v74 | v75 |
|---|---|---|---|---|---|---|---|---|---|
| harvester first-build | 6 | 6 | 6 | 5 | 7 | 8 | 6 | 5 | 6 |
| conveyor first-build | 8 | 8 | 8 | 8 | 9 | 10 | 8 | 7 | 8 |
| n_barrier | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| n_sentinel | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| n_gunner | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| n_launcher | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| games won | 0/5 | 0/5 | 1/5 | 2/5 | 2/5 | 0/5 | 2/5 | 0/5 | 1/5 |

Nine real patches, structurally indistinguishable. The only movers (`n_conveyor` 10–38,
`ti` 900–9660) track game length, not code. Across the whole field the same instrument
scored **2 of our 13 own transitions as "fingerprint flat"** and two more as
single-dimension moves.

**Consequence, applied honestly throughout this document:** a FLAT census fingerprint
means *we learned nothing*, **not** *they changed nothing*. Only large structural moves —
a subsystem appearing or vanishing, a first-build round moving by more than ~2×, an
economy going to zero — are above this floor. Every SCALE-TUNE and every "no detectable
change" verdict below carries this caveat. This alone is a substantial part of the answer
to the routing question: **we cannot reliably measure patch content from the archive, so
we certainly cannot price predicting it.**

---

## 1. TRANSITION INVENTORY

### 1.1 Method notes

- **Version timeline** = the ordered sequence of `teamXVersion` stamps for each team,
  taken from `replay_archive/*.meta.json` in `completedAt` order.
- **Queue-lag correction (important).** `completedAt` order ≠ submission order: a match
  queued under version *N* can finish after one queued under *N+1*. The archive bounds
  this: `max(completedAt − createdAt) = 1,101 s = 18.4 min` over 458 matches (median
  198 s). A version reversal is therefore counted as a **REAL rollback only if the lower
  stamp appears more than 18.4 min after the last sighting of the higher stamp.**
  Ground truth: our own team shows two apparent v67→v66 reversals with gaps of 0 and
  3 min. We never rolled back. The rule correctly classifies both as artifacts, and
  correctly clears sporks' apparent v7→v2 (gap 0 min).
- **Usable transition** = ≥2 archived *matches* (not games) on BOTH sides of the stamp
  change.

### 1.2 Inventory totals

| | count |
|---|---|
| Teams in archive | 65 |
| Teams that changed stamp at all | 38 |
| Unique (team, from, to) transitions observed | **160** |
| Usable (≥2 matches both sides) | **88** — of which 13 are ours (calibration only), **75 opponent transitions across 28 teams** |
| **Excluded for thin data** | **72** (listed in §5.1) |
| Real rollback events (queue-lag corrected) | **27, across 13 teams** |
| Self-test sweep events (see §4) | 16 (11 opponent, 4 ours, 1 sporks) |

### 1.3 Focus-team version timelines (chronological, run-lengths in matches)

| Team | Timeline | Shape |
|---|---|---|
| **Ouroboros** | v8 ×10 matches, 10:29 08-07 → 08:48 08-08 | **STATIC (control)** |
| **Kings College Munich** | v7 ×2 → **v1 ×13** (16:26 08-07 → 10:36 08-08) | one rollback, then 18 h of stasis |
| **CtrlAltDefeat** | v107 ×5 → v116 → v117 → v116 → v117 ×8 → **v107** (10:25 08-08) | **closed 3-state oscillation** |
| **Lunds Stallions** | v37 → v42 ×6 → v45 ×3 → v47 ×4 → v44 ×4 | forward × 3 then rollback |
| **Powerpuff Girls** | v26 → v21 ×2 → v23 → v18 ×5 → v27 → v34 ×5 → v35 ×2 | 2 real rollbacks, 7 stamps |
| **Powered by SmartFridge** | 29 stamp-runs over {28,30,31,33,34,35,38,40,41} | **rotating stable, 10 rollbacks** |
| **kladde** | v60 → v63 ×3 → v65 ×4 → v71 → v75 ×3 → v78 → v65 → v79 → **v80** | choppiest by stamp count; archive too thin |
| **0033** | v42 ×4 → v43 ×5 | clean single forward step |
| **team lazy** | v88 ×5 → v94 ×3 → v104 ×3 → v106 → v94 ×8 | experiment then rollback |
| **gsxWins** | v18 ×6 → v19 → v20 ×2 → v22 → v23 ×3 → v22 ×6 | experiment then rollback |
| **Banminary** | v40 → v39 ×5 → v41 ×8 → v39 → v41 | 2-state oscillation |
| **Landers** | v93 ×7 → v97 → v99 ×2 → v93 ×2 → v101 → v103 ×2 → v101 → v106 | 2 rollbacks |

---

## 2. PER-TRANSITION SCORING

Scores: **REACTIVE** (delta plausibly targets what was beating them) · **SCALE-TUNE**
(generic, targets nothing specific) · **EXPERIMENT** (a structural change unrelated to
the prior loss profile) · **ROLLBACK/OSCILLATION** · **UNCLEAR / below instrument floor**.

Loss-mechanism class is read from the replay's own `winCondition`: `core_destroyed`
(they were killed) vs `titanium_collected` (they lost the r1000 tiebreak). That is the
resolution the archive supports; no deeper per-stack decode was done, per brief.

---

### 2.1 CtrlAltDefeat — v107 → v116 → v117 → v116 → v117 → v107

**Pre-bump loss context (v107, 25 games / 5 matches, 08-07 14:04–18:08):** 14–11 overall.
The one catastrophic result is `ad2b9a46`, **0–5 vs Powered by SmartFridge v30**, seat A,
4 of 5 losses by `core_destroyed`, median 71 rounds. Their other losses are scattered
(Lunds v42, gsxWins v18, us).

**Post-bump delta — CITED, not re-derived.**
`docs/research/cad-probe-refreeze-spec-2026-08-08.md` §2 (era-delta table over the 14
map+seat buckets present in both corpora, 22 v107 games vs 24 v117 games) is authoritative:

> *"Subsystems added between v107 and v117: none that is structurally new … Subsystems
> removed: none. **The v107 → v117 change is a scale-up, not a redesign** — the same
> machine, run roughly twice as hard, arriving on our doorstep 7 rounds earlier."*
> First forward turret r10 → r3; first blood on our core r11 → r5; gunners +40–75%;
> conveyors ×4.3; shots +88%; damage into our core ×2.3. **The opening (`convert_ammo`
> 8/8/8, launcher born r1 / dead r6, zero splitters) is byte-unchanged across
> v107 → v116 → v117**, byte-stable within (map, seat) in 10/14 buckets.

And `docs/research/cad-v116-first-read-2026-08-07.md` Q4 on the first step specifically:

> *"**Nothing visible in the opening, and nothing statistically separable elsewhere at
> n=5** … if the family is A/B-testing against the field, v116 is not testing the opening
> — the opening is the shared, frozen asset."*

**My census corroboration (opponent-controlled: CAD games vs OpenSverige only):**

| | v107 (10 g) | v116 (10 g) | v117 (35 g) |
|---|---|---|---|
| first gunner (median round) | 28 | 10.5 | **3** |
| launcher first-build | r1 (10/10) | r1 (10/10) | r1 (32/35) |
| n_conveyor | 35 | 33.5 | 23 |
| n_harvester | 9 | 7.5 | 5 |
| splitters ever | 0 | 0 | 0 |
| our game win rate against them | 20% | 10% | 34% |

**SCORING**

| Transition | Score | Evidence |
|---|---|---|
| v107 → v116 | **SCALE-TUNE** | Economy up (conveyors 6 → 33.5 in the full corpus, barriers appear 20% → 70% presence). Their pre-bump 0–5 loss was a fast core-kill on small maps; an economy expansion does not address that. Nothing structurally new (cited). |
| v116 → v117 | **SCALE-TUNE, and it partially *reverses* the previous step** | Tempo continues to pull in (first gunner 10.5 → 3 vs us) but economy goes back **down** (conveyors 33.5 → 23, harvesters 7.5 → 5). |
| v117 ↔ v116 (08-07 21:40 / 22:39 / 22:59) | **OSCILLATION** | Gaps of 59 min — above the 18.4-min queue-lag bound, so a real A/B alternation, not a completion-order artifact. |
| **v117 → v107 (08-08 10:25, +79 min)** | **ROLLBACK** | Returned to the exact stamp our probe was sourced from (`bots/cad_probe`). |

**Retrodiction test.** Standing at 08-07 22:00 with v107 and v116 in hand, what do we
predict for the next bump? The only trend with two points is "more economy, earlier
turrets." **v117 pulled the turret in further (right) and cut economy back (wrong).**
So a pre-built counter aimed at "v118 will be an even bigger eco engine" would have been
built against the wrong bot. Standing at 08-08 09:00 with v107/v116/v117 in hand, the
correct prediction is not a content prediction at all — it is *"they will land back on
one of these three."* **That prediction was correct 85 minutes later.**

**Caveat on the fresh v107 rollback.** n = 5 games, one match, one opponent (our v76),
one seat. Launcher at r1 in 5/5 and zero splitters — family silhouette intact — but the
volume statistics (`n_conveyor` 32, `n_harvester` 7) are dominated by game length and
map, and at this n I make **no claim** that the 08-08 artifact stamped "v107" is
byte-identical to the 08-07 one. It does not matter much for us: the refreeze spec
already established the opening is byte-stable *across all three stamps*, so an
opening-keyed book transfers regardless of which one is live.

---

### 2.2 Lunds Stallions — v37 → v42 → v45 → v47 → v44 (incl. one rollback)

**Opponent-controlled fingerprint (their games vs OpenSverige only):**

| | v37 (5 g) | v42 (20 g) | v45 (15 g) | v44 (20 g) |
|---|---|---|---|---|
| launcher first-build | r1 (5/5) | r1 (20/20) | r1 (15/15) | r1 (20/20) |
| gunner first-build | 18 | 13 | 11 | 12 |
| harvester first-build | 9 | 10 | 8.5 | 9 |
| conveyor first-build | 11 | 12 | 10.5 | 11 |
| barriers ever | 0/5 | 0/20 | 0/15 | 0/20 |
| n_launcher | 1 | 1 | 1 | 1 |
| **their game win rate vs us** | 100% | 75% | 73% | **75%** |

**SCORING — all three transitions: SCALE-TUNE / no detectable change (instrument-floor).**
Four stamps, one behavioural signature, one win rate. The v45 → v47 step looks dramatic
in raw numbers (`ti` 2,940 → 435, rounds 461 → 142) but v47's entire 20-game corpus is a
single 05:12 self-test sweep against four *different, mostly stronger* opponents
(Askar City v73, gsxWins v22, Banminary v41, KCM v1) — the collapse is opponent mix, not
a patch. The v47 → v44 step (a real rollback, +32 min) restores the pre-sweep numbers
exactly, which is what "same bot, easier opponents" looks like.

**Retrodiction test.** Predicted content of the last bump: *nothing.* Correct — but this
is a trivially correct prediction that buys nothing, since it recommends no build.

---

### 2.3 Powerpuff Girls — 7 stamps, 2 real rollbacks

**Opponent-controlled fingerprint (their games vs OpenSverige only):**

| | v26 (5 g) | v21 (10 g) | v23 (5 g) | v18 (20 g) | v35 (10 g) |
|---|---|---|---|---|---|
| gunner first-build | **5** | 28.5 | 21 | **59** | 21.5 |
| sentinel first-build | 20.5 | 24.5 | 52 | 53 | 38 |
| n_sentinel | 0 | 0.5 | 2 | 3 | 1.5 |
| n_gunner | 6 | 9.5 | 14 | 4.5 | 8.5 |
| **n_barrier** | 0 | 0 | 0 | 0 | **9.5** |
| ti collected | 790 | 5,275 | 4,960 | 4,955 | **8,410** |
| median rounds | 178 | 1,000 | 1,000 | 503 | 1,000 |
| their win rate vs us | 40% | 60% | 40% | 55% | 50% |

These are **not tuning variants of one bot** — first-gunner round ranges r5 to r59 and
sentinel count 0 to 3 across stamps. Powerpuff is cycling a stable of materially
different builds, and (note the last row) **none of the cycling has moved their result
against us**: 40/60/40/55/50%.

**SCORING**

| Transition | Score | Evidence |
|---|---|---|
| v26 → v21 (+82 min) | **ROLLBACK/OSCILLATION** | Different bot, not a patch |
| v23 → v18 (+102 min) | **ROLLBACK/OSCILLATION** | Different bot; already flagged in `docs/spitball.md` ("Rollbacks are re-characterization triggers", s14 ~20:05) |
| **v34 → v35** (5 matches / 2 matches) | **REACTIVE** | See below |

**v34 → v35 in detail.** v34's entire corpus is one 00:29 self-test sweep: **0–25**,
23/25 losses by `core_destroyed`, median 227 rounds, `ti` 490, 1 harvester, 6 conveyors —
a broken build, comprehensively core-rushed by Pantheon v48, Pivot v73, not adgato v17,
Jython v81 and sporks v2. v35, 7.3 h later: **barrier presence 28% → 80%, median barriers
per game 0 → 9.5** (the first barriers this team has ever fielded in the archive),
sentinel presence 40% → 90%, median rounds 227 → 1,000, `ti` 490 → 8,410. The delta
targets exactly the loss class — "we keep getting our core killed" answered with mass
static HP plus a stall to the r1000 tiebreak. **REACTIVE, and effective** (0% → 50% game
win rate).

**Retrodiction test.** Direction: predictable ("after a 0–25 core-rush wipeout they will
harden"). Content: **not** predictable — the specific answer was 9–10 barriers per game,
a subsystem they had never used in ~50 prior archived games. A counter pre-built for
"they'll add turrets" or "they'll fix economy" would have been wasted.

---

### 2.4 Kings College Munich — v7 → v1 (rollback), then 18 hours of stasis

| | v7 (10 g, 15:36 08-07) | v1 (70 g, 16:26 08-07 → 10:36 08-08) |
|---|---|---|
| result | **0–10** | 38–22 (63%) |
| loss condition | 10/10 `core_destroyed` | 77% `core_destroyed` |
| median game length | 95 | 232 |
| n_conveyor | 4.5 | 20.5 |
| n_gunner | 1.5 | 5 |
| ti collected | 180 | 2,010 |
| launcher first-build | r1 (10/10) | r1 (57/60) |

v7's 10 games are one 15:36 pair of unrated matches (vs team lazy v94 and Pantheon v36) —
a self-test that returned an unambiguous verdict. 50 minutes later they were back on v1
and have not moved since (13 matches, 18 hours).

**SCORE: ROLLBACK.** **Retrodiction: full hit.** "A build that goes 0–10 with a dead
economy gets reverted" is the single most reliable prediction in this archive, and the
follow-on prediction — *"KCM will still be v1 tomorrow"* — has held for 18 h.

---

### 2.5 0033 — v42 → v43. The one clean REACTIVE transition in the archive

The cleanest controlled transition available: 4 of 4 pre-bump matches and 4 of 5
post-bump matches are against us, so opponent identity is nearly held fixed.

| | v42 (20 g vs us) | v43 (20 g vs us) |
|---|---|---|
| game win rate vs us | **15%** | **70%** |
| losses by `core_destroyed` | **17/17 (100%)** | 6/9 (67%) |
| median length of a loss | 165 | **284** |
| barrier presence | 9/20 (45%) | 15/20 (75%) |
| sentinel first-build | r18 | **r58** |
| n_harvester | 3.5 | 5 |
| ti collected | 715 | 1,525 |
| median rounds | 133 | 192 |

**Pre-bump, they were being killed — every single loss, at median round 165.** Post-bump:
barriers in three quarters of games instead of half, sentinel investment deferred by
40 rounds in favour of economy, harvesters up, games last half again as long, and the
loss profile shifts from 100% core-kill to a third tiebreak losses.

**SCORE: REACTIVE.** The delta is aimed squarely at the loss mechanism that dominated
before it.

**Retrodiction test.** Standing at 08-08 02:00 we could have predicted the *direction*
("they will try to stop dying") with confidence. We could not have predicted whether the
answer would be barriers, turrets, or economy — and here it was all three at once, in
proportions no prior data implied.

---

### 2.6 The revert-after-a-bad-sweep cluster

Six teams shipped a build, tested it (usually via a self-test sweep, §4), watched it
crater, and moved off it within 30–90 minutes.

| Team | Bad build | Result | What followed | Lag | Score |
|---|---|---|---|---|---|
| Kings College Munich | v7 | 0–10, all core-kill, ti 180 | **revert to v1** | 50 min | ROLLBACK |
| team lazy | v104 (+v106) | 1–15 then 0–5; **gunner presence 100% → 0%** (they deleted the gunner) | **revert to v94** | 42 min | EXPERIMENT → ROLLBACK |
| gsxWins | v23 | 1–15; everything delayed (sentinel r7→13, harvester r4→8) | **revert to v22** | 85 min | EXPERIMENT → ROLLBACK |
| Landers | v97/v99 | 2–15; ti 1,830 → 85, conveyors 29 → 2 | **revert to v93** | 30 min | ROLLBACK |
| Landers | v103 | 0–10 | **revert to v101** | 50 min | ROLLBACK |
| Powerpuff Girls | v34 | 0–25 | **forward to v35** (not a revert) | 7.3 h | REACTIVE |
| arsonist duck | v5 | 0–20 | **forward to v7** | 5.7 h | UNCLEAR (thin) |

**Rate: 6/6 teams moved off the bad build. 4/6 moved by reverting to a state already in
our archive; 2/6 moved forward.**

### 2.7 Powered by SmartFridge — the pure oscillator

29 stamp-runs over nine distinct versions {28, 30, 31, 33, 34, 35, 38, 40, 41} in 24 h,
with **10 queue-lag-corrected rollbacks**. The stamps are behaviourally distinct
(sentinel first-build ranges r24 / r113 / r121 across v28 / v30 / v33; barrier first-build
r19 / r49 / r110 / r142 across v33 / v28 / v35 / v34), so this is not stamp noise — it is
a team rotating a library of stored builds against the field.

**SCORE: OSCILLATION.** There is no "next patch" here to predict. There is a finite state
set, and **we already hold archived games on all nine of their states.**

### 2.8 Everyone else — below the floor

The 28 teams with usable transitions include eleven monotone linear developers (Pantheon
v36→…→v56, Jython v55→…→v93, Pivot, Erebus, not adgato, Lorem Ipsum, The Flotte
Experience, I Stone, O(1), Coreflood, ArjunWorks). Their per-step deltas are mostly
single-dimension moves inside the sensitivity floor established in §0, measured against
shifting opponent mixes. Two above-floor exceptions worth naming:

- **sporks (ladder #1)** v2 → v7: gunners essentially removed (presence 90% → 48%,
  n_gunner 3 → 0), sentinel pulled in r25 → r11, ti 4,920 → 1,080 — a real structural
  **EXPERIMENT**; their win rate dipped 70% → 56%. v7 → v8 restored economy
  (ti → 1,835) and sentinels (2 → 3) and the win rate jumped to 90%. Even the strongest
  team in the pool is running blind experiments and correcting them.
- **Clankers** v1 → v2: launcher presence 74% → 0% and gunner presence 71% → 4% — they
  deleted two whole subsystems, and the win rate fell 57% → 36%. **EXPERIMENT.**

---

## 3. SCORE TALLY

Across the transitions where the delta was above the sensitivity floor and the pre-bump
loss context was legible:

| Score | Count | Transitions |
|---|---|---|
| **REACTIVE** (delta targets what beat them) | **3** | 0033 v42→v43 · Powerpuff v34→v35 · sporks v7→v8 |
| **SCALE-TUNE** (generic, targets nothing specific) | **5** | CAD v107→v116, v116→v117 · Lunds ×3 |
| **EXPERIMENT** (structural, unrelated to loss profile) | **4** | team lazy v94→v104 · gsxWins v22→v23 · sporks v2→v7 · Clankers v1→v2 |
| **ROLLBACK / OSCILLATION** | **27 events, 13 teams** | see §1.2 |
| **UNCLEAR / below floor** | the remaining ~60 opponent transitions | — |

**3 reactive out of ~12 legible forward steps.** Even generously counted, a coin flip
does about as well, and the three reactive cases were reactive only in *direction*, never
in mechanism.

---

## 4. BONUS: THE SELF-TEST SWEEP IS A REAL LEADING INDICATOR

While building the inventory a clean, unanticipated signal fell out.

**Detector:** ≥3 `unrated` matches by one team, completing within a 180-second window,
against ≥3 *distinct* opponents, all under a single own-version stamp. That shape is a
team firing a batch of challenges at the field immediately after uploading a build.

**Result over the archive: 16 sweeps. Excluding our own 4 (which are our arena
challenges) and sporks' 1 (a case where two other teams challenged sporks simultaneously
— 2 distinct opponents on inspection), **11 opponent sweeps, and the next observed stamp
for that team differed in 11 of 11.**

| Team | Sweep | Result of sweep | Next stamp | Lead time |
|---|---|---|---|---|
| kladde | v63 | — | v65 | +61 min |
| Jython | v61 | — | v63 | +18 min |
| Powered by SmartFridge | v28 / v33 / v30 / v40 | — | v34 / v28 / v33 / v41 | +22 / +11 / +152 / +12 min |
| team lazy | v104 | 1–15 | v106 | +43 min |
| gsxWins | v23 | 1–15 | **v22 (revert)** | +85 min |
| Powerpuff Girls | v34 | 0–25 | v35 | +438 min |
| arsonist duck | v5 | 0–20 | v7 | +345 min |
| Lunds Stallions | v47 | 7–13 | **v44 (revert)** | +32 min |

**Median lead time ≈ 32 minutes.** This does not tell us *what* the next build will be —
it tells us, with 11/11 precision on this sample, *that* one is coming, and it tells us
roughly how good it was. That is a monitoring signal, not a build signal, and it is
almost free: it requires only the archiver's existing meta stream.

Caveat: n = 11, one 24-hour window, and the detector cannot distinguish "team X swept the
field" from "several teams challenged X at once" without inspecting opponent identity
(the ≥3-distinct-opponents rule handles the observed cases but is not airtight).

---

## 5. THE FAMILY-SYNCHRONIZATION ANSWER

`docs/spitball.md` ("The CAD family moved versions TOGETHER tonight", research s14
~21:15) recorded four family-adjacent teams changing versions in one evening — CAD
v107→v115, Lunds v42→v43, KCM 7→1, Powerpuff 26→18 — and proposed that a member bump
should trigger a family-wide re-freeze.

**Tested against the base rate, the timing claim does not hold.**

- The archive contains **172 stamp-change events** across 38 teams in a 24 h window.
  Cross-team bump pairs falling within 10 minutes of each other: **235 / 13,929 = 1.69%**.
  That is the chance base rate for "two teams moved together."
- Restricting to the behavioural launcher-family (see below): **1 / 139 pairs = 0.72%** —
  **at or below chance**, not above it.
- The specific coincidence that motivated the note (KCM v1 first seen 16:26, Powerpuff
  v18 first seen 16:24) is real and striking, but CAD's and Lunds' bumps that same
  evening were 19:56 and 23:10 — three and seven hours later, which is not
  "synchronized" in any operational sense.

**Also: Powerpuff is not in that family, behaviourally.** A census scan for the family's
strongest structural marker — a launcher built at round ≤2 — gives:

| Team | launcher at r≤2 | median launcher round | median sentinel round |
|---|---|---|---|
| gsxWins | 95/95 (100%) | 2 | 7 |
| Banminary | 70/70 (100%) | 1 | 6 |
| Mimercraft | 35/35 (100%) | 1 | 3 |
| Lunds Stallions | 87/90 (97%) | 1 | 17 |
| Kings College Munich | 67/70 (96%) | 1 | 37.5 |
| **CtrlAltDefeat** | 73/80 (91%) | 1 | 11 |
| Askar City | 44/60 (73%) | 1 | 18 |
| **Powerpuff Girls** | **0 / 45+ (0%)** | never | 38–53 |

Powerpuff has **never built a launcher** in any archived game. It was grouped with the
family on rollback-timing coincidence, not behaviour. Conversely **Banminary and gsxWins
carry the family's signature strongly** and were never listed.

**Answer, stated for the routed brief:** the family-synchronization hypothesis is
**NOT SUPPORTED at the timing level** — clustering is at or below the field base rate,
and one of the four founding members is not a behavioural member at all. The *shared-code*
argument for family-wide re-freeze may still stand on its own merits (the launcher-at-r1
+ no-splitters signature is genuinely shared across CAD / Lunds / KCM / Banminary /
gsxWins / Mimercraft / Askar City), but **"one member moved, therefore all are stale" is
not a timing inference this archive licenses.**

---

## 6. WHAT THIS PRICES

Three anticipatory strategies were on the table. The evidence sorts them cleanly.

### ❌ A. Pre-built counters for predicted patch content — **REJECT**

Four independent reasons, in descending order of force:

1. **We cannot measure patch content, let alone predict it.** Nine of our own consecutive
   real patches are structurally indistinguishable through the same instrument we would
   use to detect theirs (§0). Any "we predicted their content and were right" claim would
   be unfalsifiable at archive resolution.
2. **Where content *is* legible, it is not reactive.** Only 3 of ~12 legible forward steps
   score REACTIVE, and all three are reactive in direction only. The modal forward step is
   SCALE-TUNE or a blind EXPERIMENT (team lazy deleting its gunner; Clankers deleting its
   launcher *and* its gunner; sporks — the #1 team — deleting its gunners and losing
   14 points of win rate for it).
3. **Consecutive steps by the same team contradict each other.** CAD raised economy
   ×4 from v107→v116 and then cut it back from v116→v117. A counter pre-built off the
   first trend is aimed at a bot that no longer exists.
4. **The lead time is wrong even when the direction is right.** Powerpuff's hardening
   arrived 7.3 h after the signal; 0033's arrived 4.5 h after. A build cycle of ours is
   not shorter than that, so "pre-built" would in practice mean "built after the fact
   anyway" — with the extra cost of having guessed the mechanism.

This also lines up with the external-meta finding already on the books
(`docs/spitball.md`, breakthrough scavenge): *opponent-move prediction is a four-way
negative* across Battlecode/CodinGame champions; what worked was modelling opponent
**latencies and habits**, not their optimal or intended play. Patch-content prediction is
opponent-move prediction one level up.

### ✅ B. Era-stamped books for oscillators — **SUPPORT. This is the strategy the evidence pays for.**

**13 of 38 stamp-changing teams roll back**, with 27 rollback events in 24 hours. For
these teams the "next version" is not a new object at all — it is a **draw from a finite
set of states we have already seen and already hold games for.** Rollbacks arrive fast
(median lag between the bad build and the revert: ~46 min), so a book keyed by version
stamp is live again almost immediately.

**Teams this covers, with what we already hold:**

| Team | States to book | What we already have |
|---|---|---|
| **CtrlAltDefeat** | v107 / v116 / v117 — closed set, **and they are back on v107 as of 08-08 10:25** | Both endpoints: `bots/cad_probe` is v107-sourced; `cad-probe-refreeze-spec-2026-08-08.md` is the v117 spec; `cad-v116-first-read-2026-08-07.md` covers the middle. **The opening is byte-stable across all three** (cited), so the opening-keyed rows in the refreeze spec transfer to whichever stamp is live — only the mid-game scale rows are era-specific. |
| **Powered by SmartFridge** | 9 states {28,30,31,33,34,35,38,40,41} | Archived games on **all nine**; `flotte_probe` covers the class |
| **Powerpuff Girls** | 7 states, 2 rollbacks; v18 and v35 are the live-relevant ones | Archived games on all seven; v35's barrier build is new and unbooked |
| **Banminary** | 2 states {39, 41}, oscillating | Games on both |
| **Landers** | {93, 99, 101, 103, 106}, 2 rollbacks | Games on all but v106 |
| **Tyvrets** | {5, 6, 8}, 2 rollbacks | Games on all three |
| **team lazy** | {88, 94, 104, 106} — v94 is the stable attractor | Games on all four |
| **gsxWins** | {18,19,20,22,23} — v22 is the attractor | Games on all five |
| **kladde** | {60,63,65,71,75,78,79,80} — too thin to book per-stamp | `bots/kladde_probe` is v65-sourced, and **v65 is a state they returned to** (08-08 06:12) |
| Leviathan, Kleos, KCM | 1 rollback each | Games on both endpoints in each case |

**The operational rule this supports:** when a known oscillator's stamp changes, **look up
the stamp before spending anything on a fresh decode.** In 4 of 6 observed
move-off-a-bad-build cases the new stamp was one we already had games for. This is
`docs/spitball.md`'s own "the rolled-BACK-to version may match an OLD era we already
decoded — a lookup beats a fresh decode" (s14 ~20:05), now quantified: **27 rollback
events, 13 teams, and every rolled-back-to stamp in this archive is one we already hold
games on.**

**Add the sweep detector (§4) as the trigger.** It is nearly free, it fires ~32 min ahead
of the stamp change on this sample, and it also *grades* the incoming build — a sweep that
returns 1–15 predicts a revert, a sweep that returns respectably predicts the new stamp
sticks. That converts "have a bot ready when they churn" from a build commitment into a
**watch commitment**, which is what the evidence actually pays for.

### ⚖️ C. Neither — **partially correct, and it is the right default for linear developers**

For the ~11 monotone linear developers (Pantheon, Jython, Pivot, Erebus, not adgato,
Lorem Ipsum, The Flotte Experience, I Stone, O(1), Coreflood, ArjunWorks) and for the
static teams (Ouroboros v8, Team 48 v16, Askar City v73, Troupe v1, OopsGotYourElo v21,
Kvarnholmen v9, Orizon v34, StarTrekker v7 — all one stamp for the whole window), neither
anticipatory strategy applies:

- **Static teams need nothing anticipatory** — the existing frozen book stays valid. The
  Ouroboros control is emphatic: 50 games against **9 different versions of ours** over
  24 h, and its census fingerprint does not move (gunner r16, conveyor r4, harvester r4,
  12 gunners, ti 4,500, and **zero sentinels / launchers / barriers / splitters in every
  single game**). Cite `docs/research/ouroboros-v65-era-reverify-2026-08-07.md`.
- **Linear developers change below our resolution.** We cannot see their steps, so we
  cannot pre-empt them; the correct response is the existing staleness discipline
  (re-verify a book when its version stamp moves), not anticipation.

### The one-line answer for the routed brief

> **Do not build anticipatory counters. Do build the era-stamped book index plus the
> self-test-sweep watcher.** Patch content is unmeasurable at archive resolution and
> non-reactive where measurable (3 REACTIVE out of ~12 legible forward steps, all
> direction-only). But a third of stamp-changing teams oscillate rather than progress —
> 27 rollbacks across 13 teams in 24 h — and **every stamp any team rolled back to in this
> archive is one we already hold games on.** The cheap edge is *recognition*, not
> *prediction*: index the books by version stamp, watch for the challenge-sweep burst
> (11/11 precision, ~32 min lead), and on a stamp change do a lookup before a decode.
> CtrlAltDefeat proved the case during this study: they rolled from v117 back to v107 at
> 10:25 today, and we hold both endpoints.

---

## 7. SELF-CHECKS

### 7.1 Transitions EXCLUDED for thin data (72 of 160)

Excluded = fewer than 2 archived matches on at least one side. Full list, `(matches
before / matches after)`:

Banminary v40→v39 (1/5) · Coreflood v61→v62 (5/1), v62→v63 (1/5) · Erebus v56→v58 (2/1) ·
I Stone v13→v14 (3/1), v14→v17 (1/1), v17→v18 (1/2) · Jython v55→v56 (1/4), v61→v63 (4/1),
v63→v70 (1/1), v70→v73 (1/2), v73→v74 (2/1), v74→v81 (1/2), v81→v90 (2/1), v90→v93 (1/6) ·
Klarum v43→v45 (10/1) · Kleos v30→v33, v33→v37, v37→v28, v28→v38 (all 1/1) ·
Landers v93→v97 (7/1), v97→v99 (1/2), v101→v106 (2/1) ·
Leviathan v9→v10 (1/2), v10→v13 (2/1), v13→v26 (1/1), v26→v25 (1/8) ·
Lorem Ipsum v14→v16 (3/1), v16→v22 (1/1), v22→v23 (1/3) ·
Lunds Stallions v37→v42 (1/6) · Memtrace v27→v28 (1/1), v28→v33 (1/3) ·
O(1) v8→v9 (7/1), v9→v10 (1/5), v11→v12 (4/1) · Oresund Overflow v20→v30 (1/1) ·
Pantheon v36→v39 (6/1), v39→v42 (1/3), v47→v48 (5/1), v48→v49 (1/1), v49→v50 (1/1),
v50→v51 (1/6) · Pivot v63→v64 (1/1), v64→v67 (1/3), v69→v71 (2/1), v71→v73 (1/14) ·
Powered by SmartFridge v40→v41 (5/1), v41→v31 (1/2) ·
**Powerpuff Girls v26→v21 (1/2), v21→v23 (2/1), v23→v18 (1/5), v18→v27 (5/1),
v27→v34 (1/5)** · Torsko v2→v4, v4→v5, v5→v6 (all 1/1) · Viktor5776 v1→v3 (1/5) ·
arsonist duck v5→v7 (4/1), v7→v19 (1/1) · farming_200s v7→v8 (2/1) ·
gsxWins v18→v19 (6/1), v19→v20 (1/2) ·
**kladde v60→v63 (1/3), v65→v71 (5/1), v71→v75 (1/3), v75→v78 (3/1), v78→v65 (1/5),
v65→v79 (5/1), v79→v80 (1/1)** · team lazy v104→v106 (3/1), v106→v94 (1/11).

**Two exclusions deserve explicit flagging against the brief's priors:**

- **kladde was named as a priority choppy team (v65→75→78→65→79→80). Every one of those
  steps is excluded** — six of seven have exactly one archived match on a side. Their
  churn is real and is now confirmed to reach v80, but the archive **cannot score its
  content**. Only v63→v65 is usable, and its delta is inside the instrument floor. The
  brief's characterisation of kladde as choppy is upheld; any claim about *what* they
  changed is not.
- **Powerpuff's v26→v21→v23→v18 rollback chain is excluded transition-by-transition**
  (each stamp has 1–2 matches). It is reported in §2.3 as an *era comparison* across five
  stamps with pooled corpora, not as four scored transitions. The behavioural distinctness
  of the stamps is above the floor; the individual step attributions are not.

Also excluded by construction: CAD v116→v117 and v117→v116 are scored as one
**oscillation** rather than two independent transitions, because the two v116 matches
straddle a v117 match.

### 7.2 Census validation counts

| check | value |
|---|---|
| Archive metas parsed | **458 / 458** |
| Replays present | 2,291 |
| Replays parsed by `tools/replay_census.py` | **2,291 / 2,291**, exit 0, **stderr empty (0 bytes)** |
| Matches with all 5 replays parsed | **457 / 458** (one match has 6 archived replay files; all parsed) |
| Census rows joinable to a meta | 2,291 / 2,291 |
| Team/seat attribution | from `meta.json` `teamAName`/`teamBName`; corroborated behaviourally on CAD (launcher at r1 in 73/80 games, matching the cited refreeze spec) |
| Queue-lag bound | 1,101 s, from `max(completedAt − createdAt)` over 458 matches; validated against our own two known-false reversals (gaps 0 and 3 min, correctly classified as artifacts) |
| Instrument sensitivity floor | measured on 9 of our own known-real patches vs a frozen opponent (Ouroboros v8), 5 games each — see §0 |

### 7.3 Known limitations

1. **The window is 24 hours.** Every "team X is stable" claim means *stable over one day*.
   Ouroboros' 24 h of stasis is the strongest such claim and it is still only 24 h.
2. **Opponent and map mix confound most transitions.** Where I could, I restricted to
   games against a single opponent (usually us) — CAD, Lunds, Powerpuff, 0033, Banminary,
   KCM, Ouroboros in §2. Where I could not (KCM v7 has no shared opponent with v1,
   Lunds v47's corpus is a sweep against four different teams), I have said so inline.
3. **`n_*` end-of-game counts are dominated by game length** and are the weakest evidence
   in every table. First-build rounds and subsystem presence/absence are the load-bearing
   dimensions.
4. **Version stamps are assumed to identify artifacts.** The 08-08 CAD "v107" is treated
   as *a stamp we have a book for*, not as *proven byte-identical to the 08-07 v107*; at
   n = 5 games / 1 match / 1 seat that identity cannot be established or refuted here.
   The refreeze spec's byte-stable-opening result is what makes this not matter.
5. **The sweep detector has n = 11 opponent events.** 11/11 is a clean result on a small
   sample and should be treated as a hypothesis worth cheap monitoring, not a law.
6. **No deep per-stack decode was performed**, per brief. All behavioural claims are at
   census resolution or are citations from the existing decoded docs.

---

## 8. SOURCES CITED (not re-derived)

- `docs/research/cad-probe-refreeze-spec-2026-08-08.md` — §2 era-delta table
  v107→v116→v117; "scale-up, not a redesign"; opening byte-stable across all three;
  10/14 (map, seat) buckets byte-identical.
- `docs/research/cad-v116-first-read-2026-08-07.md` — Q4 churn signal: nothing separable
  in v107→v116 at n=5; "the constants are the *stable* part of a fast-moving family".
- `docs/research/ouroboros-v65-era-reverify-2026-08-07.md` — Ouroboros v8 determinism and
  the opening-as-input finding.
- `docs/research/v72-bleed-cad-family-2026-08-08.md` — family structural invariants
  surviving v107→v116→v117; per-map tile rows are perishable and must be re-checked
  against the live version.
- `docs/spitball.md` — "Rollbacks are re-characterization triggers" (s14 ~20:05);
  "The CAD family moved versions TOGETHER tonight" (s14 ~21:15) — **the timing half of
  which this document tests and does not support**; breakthrough-scavenge finding that
  opponent-move prediction is a four-way negative in the external metas.

Working files for this study: `scratchpad/retrodiction/` (census.tsv, timelines.txt,
rollbacks.txt, fingerprints.txt, inventory.txt, scoring.txt, final.txt).

---

## Prospective addendum (real ~14:1x CEST, same day)

The self-test-sweep leading indicator, found retrospectively (11/11),
was tested prospectively within hours: three teams swept ~11:0x-11:1xZ;
prediction "stamps by ~11:41Z". Confirmed: Torsko v5→v7 by 11:10Z,
Powered by SmartFridge v33→v35 by 11:38Z (both via free match-list
JSON, no downloads). kladde pending (builder opp_watcher). Prospective
record: 2/2, third pending. The watcher graduates from retrospective
finding to working instrument on its first live day.

**Record complete (real ~14:2x CEST):** kladde resolved first —
v80→v81 caught by the builder's opp_watcher at ~11:15Z, ~10 min after
its 11:05Z sweep (the later v81→v80 bounce doesn't unwind the
prediction: the predicted next stamp happened). **Final prospective
record: 3/3 (kladde, Torsko, SmartFridge), all inside the window.**
The sweep watcher is a validated standing instrument as of its first
live day. DIRECTION BOUND (builder's Powerpuff v36 datum): a stamp
occurred with no detected sweep — the instrument predicts stamps FROM
sweeps (high precision on that arrow); it does not claim every stamp
is sweep-preceded. Coverage of the sweep→stamp arrow: 14/14 lifetime
(11 retrospective + 3 prospective).
