# SCOUT — field mechanism census: what the teams above us do that we do not

Side lane, read-only. Written **2026-08-11T08:26:21Z** (`date -u`, same shell).
Repo at `d790dc3` (`git log -1`, committer time 2026-08-11T10:23:51+02:00).
No bot was edited, no arena was run, no match was fired.

Question put to this lane: **what do the teams ABOVE us do that we do not do at
all?** Method template and its limits: `docs/research/SCOUT-farming200s-v12-v13-2026-08-11.md`.

Nothing here is a verdict on a plank. It is a behavioural census of third-party
replays with above/below-us controls. No word in this file means "proven" or
"refuted", and section 5 is the part that constrains every number above it.

## Population clocks

* `corpus/meta_join.tsv` — **17,628 archived-replay rows**, newest `completedAt`
  **2026-08-11T08:16:54Z** (~9 min behind the wall clock at writing).
* `replay_archive/` — **21,374** `.replay26` files on disk.
* `corpus/league_matches.tsv` — **35,828 ladder matches**, newest `createdAt`
  **2026-08-11T07:52:59Z**. Used ONLY for team ratings, never for behaviour.
* **Ratings** are each team's newest `ratingABefore`/`ratingBBefore` seen in
  `league_matches.tsv`. Our line: OpenSverige **1686**, rank 21 of 72.
* **Third-party sample throughout.** Except where a row is explicitly labelled
  OpenSverige, every behavioural number is a third party's bot playing its own
  games; ~98% of `league_matches` rows are matches between other teams.

---

## 1. COVERAGE — and it is not the answer this time

Archived games per team, for the 20 teams above us. **`n` counts team-games (one
row per game per side), pooled across all of that team's versions.**

| team | rating | archived team-games | latest ver | n @ latest ver | share of latest-ver games played vs US |
|---|---|---|---|---|---|
| sporks | 2096 | 522 | 13 | 115 | 0 |
| not adgato | 2061 | 430 | 21 | 260 | 0 |
| Clankers | 2050 | 467 | 11 | 35 | 0 |
| The Flotte Experience | 2013 | 435 | 50 | 180 | 5 |
| Erebus | 2010 | 440 | 86 | 35 | 0 |
| Lorem Ipsum | 1973 | 360 | 29 | 30 | 0 |
| Jython | 1965 | 471 | 111 | 35 | 0 |
| Pantheon | 1933 | 595 | 56 | 395 | 15 |
| ph | 1929 | 270 | 22 | 50 | 0 |
| O(1) | 1909 | 390 | 15 | 125 | 0 |
| Pivot | 1860 | 565 | 110 | 20 | 0 |
| farming_200s | 1830 | 420 | 13 | 110 | 85 |
| Leviathan | 1799 | 760 | 55 | 145 | 0 |
| HTTP 418 | 1780 | 465 | 83 | 20 | 0 |
| kladde chatte tville (och oss) | 1761 | 840 | 87 | 135 | 15 |
| 0033 | 1751 | 875 | 50 | 425 | 45 |
| team lazy | 1746 | 640 | 195 | 35 | 0 |
| Big O | 1727 | 275 | 7 | 120 | 5 |
| Powered by SmartFridge | 1707 | 1780 | 35 | 240 | 50 |
| arsonist duck | 1693 | 305 | 24 | 215 | 25 |
| **OpenSverige (us)** | **1686** | **4,978** | **104** | **1,605** | — |

**Coverage is sufficient and it is NOT the finding.** Every team above us has
270–1,780 archived team-games. The census below therefore pools versions and
reports **team-level** behaviour. The `n @ latest ver` column is the honest
warning attached to that choice: seven of the twenty (Pivot 20, HTTP 418 20,
Lorem Ipsum 30, Clankers 35, Erebus 35, Jython 35, team lazy 35) ship often
enough that their *current* bot is thin on disk. **Any claim about what a
specific team is doing RIGHT NOW rests on ≤35 games for those seven.** Claims
about what a team has done across its history rest on the full column.

**Selection note, inherited from the template:** for teams we play often
(farming_200s 85/110, SmartFridge 50/240, 0033 45/425) part of the archive is our
own unrated legs. That is disqualifying for outcomes and close to ideal for
behaviour — their code does not know who it is playing. **No outcome or win-rate
number is taken from the archive anywhere in this file.**

## 1b. Instrument validations run BEFORE any number below was trusted

* **The headline metric has been seen to come out the other way, on our own
  files.** `batk` (builder-bot melee attacks, protobuf Update field 13) reads
  **117–386 per game for OpenSverige v64 through v94**, and **exactly 0.00 for
  v96, v99, v100, v102, v103, v104, v105, v106, v107, v109**, in the same corpus
  through the same decoder. It is not a constant column and it is not a decoder
  gap on recent files.
* **A dedicated 780-file raw re-decode reproduced both poles.** A fresh
  per-attack decoder over the 60 most recent archived games for each of 12 top
  teams plus two OpenSverige control arms: **0 file misses, 0 parse failures.**
  OpenSverige **v104 → 0 attacks in 60/60 games** (negative control, exact);
  OpenSverige **v94 → 15,219 attacks in 59/60 games** (positive control).
* **Two scripts agree exactly** — `build_agg.batk` (`tools/corpus/replay_builds.py`)
  and `econ.attacks` (`tools/corpus/replay_econ.py`) match to 2 d.p. on every
  version and every spot-checked team, with **0/1,605 per-game sign
  disagreements** on v104. ⚠ **This is a consistency check, not an independent
  one** — both count the same wire event via the same primitives. The load-bearing
  control is the v94-vs-v104 contrast above, not this agreement.
* **`corpus/econ.tsv` covers 100% of archived files** (17,946 distinct files ⊇
  all **17,588 unique** files in meta_join), checked per-version for our own line
  (v64/v80/v94/v102/v104/v106 all 100%). Checked because an early draft of this census printed
  `n_convert = 0.00` for our v104 — **that zero was a JOIN BUG in my own scratch
  script** (the per-version cell was reading a table built before the econ merge),
  not a fact about the bot. Corrected; the corrected row is in §3.
* **A degenerate column was found and dropped.** `econ.deliveries` reads 0.00 for
  every team in the corpus and so produced a meaningless Spearman ρ = −1.000. It
  is excluded. Any statistic computed on it is void.
* **team index 0 = teamA**, relied on per the template's 16,590-game
  cross-tabulation (8,724 (0,a) / 7,866 (1,b), zero cross-cells).

---

## 2. THE CENSUS — ranked by discontinuity, breadth, and control behaviour

The control that does the work: **every statistic is computed identically for the
20 teams ABOVE us and the 50 teams BELOW us** (all teams with ≥150 archived
team-games and a rating; 70 teams total), plus Spearman ρ against rating across
all 70. **A behaviour that also appears in weak teams is not a strength marker.**

| metric | ρ vs rating (n=70 teams) | ABOVE median (20) | BELOW median (50) | us ALL (4,978) | **us v104 (1,605)** | us v94 (200) |
|---|---|---|---|---|---|---|
| **% of games with ≥1 builder melee attack** | **+0.591** | **90.0%** | 57.2% | 41.0% | **0.0%** | 95.5% |
| **early-attack share (r0–150), teams that attack** | **+0.709** | **47.3%** | 27.4% | 29.8% | n/a | 31.9% |
| **turrets sited forward (d²enemy < d²own)** | **+0.505** | **66.7%** | 43.3% | 43.8% | **52.0%** | 36.7% |
| builder melee attacks per game | +0.278 | 70.3 | 62.3 | 94.8 | **0.00** | 218.0 |
| turrets built per game | +0.258 | 8.2 | 5.9 | 5.6 | 6.5 | 5.4 |
| turret shots per game | +0.183 | — | — | 67.5 | 57.3 | 83.4 |
| shots per turret per game | −0.089 | 20.4 | 20.6 | 12.1 | 8.8 | 15.5 |
| gunner share of turrets | **−0.262** | 82.0% | 79.3% | 28.0% | 14.6% | 50.5% |
| launchers built per game | **−0.298** | 0.00 | 0.00 | 0.96 | 1.19 | 0.62 |
| launcher INSERT throws per game | **−0.531** | 0.00 | 0.00 | 0.66 | 0.95 | 0.00 |
| launcher EXILE throws per game | **−0.375** | 0.00 | 0.00 | 6.89 | 6.14 | 0.00 |
| game length (max round reached) | −0.306 | 242 | 330 | 273 | **187** | — |
| barriers built per game | +0.556 | 1.70 (field med) | — | 3.84 | 6.27 | — |
| sentinels built per game | +0.375 | 1.27 (field med) | — | 3.33 | 4.53 | — |
| ammo conversions per game | +0.108 | 85.4 | 78.7 | 63.4 | 57.8 | 74.1 |
| titanium per conversion | +0.174 | 8.6 | 9.0 | 9.7 | 9.9 | 9.6 |
| CPU peak µs per game | +0.358 | 3,026 | 2,549 | 5,451 | 3,938 | 7,773 |
| heals per game | +0.088 | 180.9 | 182.6 | 323.7 | 248.1 | 532.4 |
| resource stacks pushed onto enemy net | −0.112 | — | — | 18.6 | 5.5 | — |

`us v94` is our own line **before** the melee switch was thrown, kept as the
within-our-own-code control column.

### 2a. The near-zero / substantial discontinuity, with its control

**Builder-bot melee.** Presence, per team, all teams with ≥150 archived games:

* **20 of 20 teams above us do it.** Minimum is Leviathan at 4.8 attacks/game in
  10% of games; the ABOVE-us median is **90% of games**.
* **15 of 50 teams below us do not** (`batk` mean < 1.0/game). **14 of those 15
  are rated below 1550**: Team 48 1545, Orizon 1364, PromptNPray 1265, Bean
  counters 1205, ArjunWorks 1179, Albert And Einstein 1145, Prompt Engineers
  Anonymous 1116, StarTrekker 1080, S 1038, Troupe 1011, Ship Happens 1010, Tim
  Tam 956, Hiver01 916, vjg 730. **The one exception is The Bisons at 1680**
  (0.80/game, 4.5% of 490 games).
* **Our v104 is 0.00 across 1,605 games.** On this axis our shipped bot groups
  with vjg (730), Troupe (1011) and Ship Happens (1010).

**The control discriminates.** Melee is not a universal behaviour that says
nothing — its *absence* is concentrated in the bottom third of the ladder, and we
are the highest-rated team with a hard zero except The Bisons.

**Counter-pressure on that same control, and it must be stated:** several teams
BELOW us attack *more* than the strong teams do — Besvikomat 649/game (99% of
games, rated 1621), Powerpuff Girls 335 (1559), Coreflood 267 (1669), Kleos 957
(1313). **Volume of melee is not the strength marker; ρ on raw attacks/game is
only +0.278.** What separates the cohorts is *whether the code path exists at
all* (ρ +0.591 on presence) and *how early it fires* (ρ +0.709 on r0–150 share,
restricted to the 52 teams that attack, which removes the zero-team confound).

### 2b. It is our own switch, and it has a name

`bots/_v130loki13/doctrine.py:1470`:

```
LOKI_QUIET_ON = True     # no builder melee: no core peck, no siphon hit, no counterbattery
```

Four call sites gate on it — `raid.py:256`, `raid.py:334`, `main.py:505`,
`eco.py:911`. `bots/_v130loki13` is the live v104 tree per `HANDOVER.md:13`. **The
mechanism is fully implemented in the shipped bot and switched off by one
boolean.** The replay record dates the change precisely: v94 (2026-08-09, 218
attacks/game, 95.5% of games) → v96 onward (0.00). v108, last night's LOKI-19
prototype, is the only recent exception at 192.90/game, all of it core-directed.

### 2c. What they aim at — five distinct doctrines, none of them ours

Per-attack raw decode, **60 most recent archived games per team**, target tile
classified by the building standing on it at the moment of the attack. Percent of
that team's attacks:

| team | rating | attacks | e.conveyor | e.core | e.harvester | e.turret | e.barrier | empty/bot | own | med d² to enemy core | med round |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Jython | 1965 | 16,258 | 41.1% | **39.6%** | 7.3% | 4.6% | 3.3% | 4.1% | 0.0% | 5 | 292 |
| *OpenSverige @v94* | *(ours, off)* | *15,219* | *24.0%* | *31.9%* | *3.9%* | *29.7%* | *7.8%* | *2.4%* | *0.0%* | *9* | *271* |
| O(1) | 1909 | 8,733 | 49.8% | 0.0% | 2.3% | **33.9%** | 7.7% | 6.1% | 0.0% | 34 | 131 |
| 0033 | 1751 | 8,433 | **74.3%** | 0.0% | 6.0% | 7.1% | 6.6% | 5.1% | 1.0% | 16 | 119 |
| Lorem Ipsum | 1973 | 7,748 | 47.7% | **30.5%** | 8.5% | 9.8% | 0.0% | 3.6% | 0.0% | 9 | 141 |
| not adgato | 2061 | 7,250 | **59.5%** | **24.7%** | 2.8% | 10.9% | 0.0% | 2.1% | 0.0% | **2** | 128 |
| ph | 1929 | 4,882 | 63.6% | 0.0% | 0.0% | 0.0% | **30.7%** | 5.7% | 0.0% | 10 | 141 |
| kladde | 1761 | 4,264 | 68.3% | 0.1% | **22.4%** | 2.1% | 1.7% | 5.3% | 0.0% | 32 | 206 |
| sporks | **2096** | 3,770 | **70.4%** | 0.0% | 0.0% | 0.1% | **24.2%** | 5.3% | 0.0% | 13 | 116 |
| Pantheon | 1933 | 3,563 | 26.5% | 0.0% | 0.0% | **70.1%** | 0.0% | 3.3% | 0.0% | 100 | 155 |
| The Flotte Experience | 2013 | 3,556 | 43.1% | 0.0% | **53.9%** | 0.0% | 0.0% | 3.0% | 0.0% | 16 | 128 |
| Erebus | 2010 | 3,103 | 0.0% | 0.0% | 0.0% | 4.1% | **93.7%** | 2.2% | 0.0% | 145 | 287 |
| Clankers | 2050 | 2,969 | 66.9% | 0.0% | 0.0% | 7.2% | **20.6%** | 5.4% | 0.0% | **1** | 127 |

**`own` is 0.0–1.0% everywhere**, which closes the main interpretation risk on
`batk`: this is offensive melee against enemy buildings, not builders demolishing
their own structures. Five doctrines are visible and teams pick one or two:

1. **Belt raid** — enemy conveyors. Broadest: 0033 74%, sporks 70%, kladde 68%,
   Clankers 67%, ph 64%, not adgato 60%.
2. **Core peck** — attacks landing inside the enemy core 2×2 footprint. Jython
   40%, Lorem Ipsum 31%, not adgato 25%. **Only three of twelve.** Our own v94 did
   32% and v108 does 100%.
3. **Counter-battery** — melee onto enemy gunners/sentinels. Pantheon 70% (median
   target d²=100 from the enemy core, i.e. mid-map), O(1) 34%. Our v94 did 30%.
4. **Breaching** — chewing through enemy barriers. Erebus **93.7%** — Erebus's
   builders do essentially nothing else with melee — plus ph 31%, sporks 24%,
   Clankers 21%.
5. **Harvester kill** — The Flotte Experience 54%, kladde 22%.

**Timing.** Median attack round runs 116–155 for most of the cohort; Clankers and
not adgato reach targets at median d² = 1 and 2 from the enemy core.

### 2d. Turret siting — a gradient, not a discontinuity

ρ **+0.505**, the second-strongest correlate. Fraction of a team's turrets built
closer to the ENEMY core than to their own (`builds.tsv d2_enemy < d2_own`):

* ABOVE-us median **66.7%**; 15 of 20 exceed 60%. Pivot 80.6%, O(1) 73.6%,
  Jython 73.1%, Pantheon 70.8%, team lazy 70.3%.
* BELOW-us median **43.3%**.
* **Our v104: 52.0%** (our all-versions figure is 43.8%; v94 was 36.7%).

This is **not** a near-zero/substantial gap — we do it, at roughly the ladder
median, ~15pp under the strong cohort. It is on the list because it is the
cleanest continuous strength gradient in the census and it points the same way as
`PLAY_DEFENCE: never`. Absolute turret volume moves with it (ABOVE median 8.2 per
game vs our 6.5, ρ +0.258).

### 2e. Things we do that the field above us does NOT — the reverse census

Reported because they are the same instrument run the other way, and they are
uncomfortable.

* **Launchers.** ρ **−0.298**. **15 of the 20 teams above us build ZERO
  launchers** and two more are near-zero (Clankers 0.12/game in 6% of games,
  Pantheon 0.06 in 4%); the only real users above us are SmartFridge 2.66/game,
  The Flotte Experience 1.86, ph 0.72. We build 1.19/game in 92% of games.
* **Launcher throws.** INSERT ρ **−0.531**, EXILE ρ **−0.375** — the two most
  strongly *negative* correlates in the whole census. The heaviest throw users in
  the league are Kleos (1313, 82 INSERT + 79 EXILE), Memtrace (1451, 11 + 80),
  SingleCore (1357, 61 + 23), Focalground (1677, 3 + 46). Our v104 does 6.14
  EXILE/game.
  ⚠ **A cross-team correlation is not an effect within our bot.** This says
  launcher play is *concentrated among low-rated teams*, which is equally
  consistent with "it is a weak mechanism" and with "it is what teams reach for
  when their fundamentals are weak". Nothing here measures what removing it from
  *our* bot would do, and this lane is not the place that decides.
* **Barriers** (ρ +0.556) and **sentinels** (ρ +0.375) are genuine positive
  correlates and we are already **above** the field median on both (6.27 vs 1.70;
  4.53 vs 1.27). Not gaps.
* **Gunner share.** We are an extreme outlier — v104 is **14.6%** gunners against
  an ABOVE-us median of 82%, and 12 of 20 teams above us are >70% gunner. **But
  ρ is −0.262**, i.e. gunner share does not track rating across the field
  (Besvikomat 94%, Lunds Stallions 94%, CtrlAltDefeat 89% all sit below us).
  **It fails its own control and is demoted out of the ranked list** despite
  being the largest-looking build-mix gap in the table.
* **Shots per turret**: ours 8.8 vs field 20.4, ρ −0.089 — no field support.
* **Game length**: our v104 reaches median round **187** vs an ABOVE-us median of
  242 and a BELOW-us median of 330 (ρ −0.306). Our games are the shortest in the
  comparison. On-programme, and it is the one axis where we lead the cohort.

---

## 3. RANKED — candidate mechanisms we lack

Ranked by (a) size of the discontinuity, (b) breadth across strong teams,
(c) plausibility of being causal rather than incidental.

**1. Builder-bot melee, at all.** Discontinuity: **0.0% of 1,605 v104 games vs an
ABOVE-us median of 90% of games; 20 of 20 teams above us have it.** Breadth:
maximal — it is the only mechanism in this census present in *every* team above
us. Control: its absence clusters at the bottom of the ladder (14 of the 15
zero-teams are rated <1550). Causality: unresolved, and the honest note is that
*volume* barely tracks rating (ρ +0.278) while *presence* does (ρ +0.591). The
cheapest fact in this file: it is one boolean in our own shipped tree, and our
own bot ran it at 218/game as recently as 2026-08-09.

**2. Early melee — attacking inside r0–150.** Discontinuity: ABOVE-us median
**47.3%** of attacks in the first 150 rounds vs BELOW-us **27.4%**, ρ **+0.709**
restricted to the 52 teams that attack at all. Breadth: broad within the
attacking cohort. Causality: this is the strongest correlate in the census and it
survives the obvious confound (zero-attack teams excluded). Note against us:
**when our own line did attack (v94) it was 31.9% early — the weak-cohort
profile.** So this is a gap even against our own switched-off code.

**3. Melee target doctrine — pick one of five and commit.** Not a single metric
but the §2c table. The prize inside it, on discontinuity size: **breaching
(Erebus 2010, 93.7% of its melee on enemy barriers; ph 31%, sporks 24%, Clankers
21%)** and **counter-battery (Pantheon 1933, 70% on enemy turrets; O(1) 34%)**.
Both are near-zero for us at v104 by construction, and both would have been
near-zero even at v94 for breaching (7.8%). We ourselves build 6.27 barriers per
game in 89% of games; **a quarter of the strong cohort's melee budget exists to
delete exactly that kind of structure**, which is worth knowing in both
directions.

**4. Forward turret siting and turret volume.** ABOVE-us **66.7%** forward and
8.2 turrets/game vs our v104's **52.0%** and 6.5. ρ +0.505 / +0.258. Ranked
fourth because it is a ~15pp gradient, not a discontinuity — we already do this,
just less.

**Explicitly NOT ranked, having failed its control:** gunner-vs-sentinel mix
(largest visual gap in the build table, ρ −0.262 across 70 teams).

---

## 4. What the controls said, in one paragraph

**Do weak teams do it too?** For raw melee volume, emphatically yes — the four
heaviest attackers in the league are rated 1313–1669. For melee *presence*, no:
90% of games above us versus 57% below, with the hard zeros concentrated 14-of-15
below 1550. For *early* melee, no: 47.3% versus 27.4%. For forward siting, no:
66.7% versus 43.3%. For gunner share, **yes** — which is why it is demoted. For
launcher play, the control runs the other way entirely: it is a below-us
behaviour we have more of than anyone above us.

---

## 5. LIMITS

1. **THE SINGLE BIGGEST THREAT: every number here is cross-sectional, and
   correlation across teams is not an effect within our bot.** Strong teams differ
   from weak teams in dozens of ways at once — pathing, target selection, comms
   use, build economy, code quality — and melee presence may be a *marker* of a
   team that writes aggressive code rather than a *cause* of rating. The census
   cannot separate "teams that attack are better" from "better teams attack".
   Nothing in this file is a live-game test of the mechanism on our own bot, and
   under the standing rule (§6 of the project brief) **it can prioritise a road
   and cannot close or open one.**
2. **The v94→v104 contrast is not an experiment.** Our own line stopped attacking
   at v96 *and changed many other things across v96–v104*. Our rating history
   across that boundary is not evidence about melee, and no rating number was
   computed here for exactly that reason.
3. **Version pooling.** §2 pools all of a team's versions. `n @ latest ver` in §1
   is ≤35 for seven of the twenty teams above us, so a team's *current* doctrine
   may differ from its pooled profile — precisely the farming_200s v12→v13 case,
   where a team's melee behaviour went 0 → 3,329 at one version boundary. **Read
   the §2c doctrine table as "this team has done this", not "this team does this
   now."** (§2c mitigates by sampling the 60 most recent games, but 60 games can
   still straddle a version boundary.)
4. **`batk` counts an event, not an outcome.** A builder attack is 2 damage for
   2 Ti against 20 HP (conveyor) or 500 HP (core). The template document's own
   arithmetic is the caution: 3,329 attacks bought roughly one conveyor kill once
   healing is in play. **Attack counts are not damage and are certainly not
   kills.** No destruction pathway is measured anywhere in this file.
5. **Ratings are a snapshot from the newest `ratingXBefore` seen per team**, and
   teams move. All ρ values are computed against that snapshot with n=70 teams;
   a Spearman ρ near ±0.3 on n=70 is weak evidence and is treated as such above.
   No confidence intervals or permutation tests were run on the ρ column — the
   ranking rests on the ABOVE/BELOW median split and the presence counts, which
   are descriptive.
6. **The "EMPTY/bot" bucket in §2c (2.1–6.1%)** is real ambiguity: the target-tile
   map tracks buildings only, so an attack on a tile holding an enemy *builder
   bot* — or on a building destroyed earlier the same round — lands there.
7. **`corpus/meta_join` was used for behaviour and coverage only, never for a
   denominator or an outcome**, per the standing surface rule. Ratings came from
   `league_matches.tsv`.
8. **One metric was found degenerate and dropped** (`econ.deliveries`, all-zero,
   ρ −1.000) and **one zero in an early draft was a bug in my own join, not a
   fact** (§1b). Both are recorded rather than smoothed. Other columns not
   individually validated against a forced-opposite case: `heals`, `n_convert`,
   `cpu_max`, `turns_run`, `ENEMY_NET`. Treat those rows as unvalidated.
9. **`tur_fwd` uses `d2_enemy < d2_own` as the definition of "forward".** On a
   symmetric map that is the midline, which is defensible; it is still a
   threshold choice made by me and not by the engine.

## 6. Reproduction

All scripts were written to the session scratchpad, not to `tools/` (read-only
commission). Everything is reproducible from committed surfaces:
`corpus/meta_join.tsv` (file → match/team/version/side), `corpus/league_matches.tsv`
(ratings), `corpus/build_agg.tsv` (`batk`, `batk_core`, `build_*`, `shot`, per
band), `corpus/builds.tsv` (turret siting, `d2_own`/`d2_enemy`),
`corpus/events.tsv` (BUILD/DEATH by kind), `corpus/econ.tsv` (ammo, heals, CPU,
turns), `corpus/throws.tsv` (launcher `kind` = INSERT/EXILE/RETREAT/UNATTRIB),
`corpus/flow.tsv` (resource routing classes). The §2c per-attack decode mirrors
the `unum == 13` block of `tools/corpus/replay_builds.py`, importing `fields`,
`read_pos` and `parse_entity` from `tools/replay_census.py` per the standing rule
against re-deriving the protobuf parser, with a live building-occupancy tile map
added to classify the target.
