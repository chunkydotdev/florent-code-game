# REPLAY STUDY — "Bean counters": v47 doctrine, and the v68 line that replaced it

> ⚠ **RIDER s54, 2026-08-21 (`CUT-116-beltgun-answer-2026-08-21.md` §1.7, found while reproducing this study's cells digit-for-digit):** (1) **17.3% of the v47 games in this study's population are EXACT DUPLICATES** (1,199 games → 992 distinct turret-event fingerprints; one game present six times — deterministic bots re-challenged on the same map). Point estimates move ≤0.3pp on dedup but **intervals widen ~13%; this pseudo-replication is NOT covered by the DEFF 1.833 this study applies.** Treat every interval here as ~13% optimistic. (2) The forward-turret clearance response variable **REMOVED is a near-constant column against a driven placebo** (turrets BC's belt is nowhere near: 73.1%±4.3 vs the castle cell's 79.7%±2.2) — the BC-vs-opponents 46pp contrast this study draws remains valid; do not reuse REMOVED as a discriminating response against within-BC controls (active-fire columns discriminate properly).

**Commissioned:** 2026-08-21, direct question from Magnus: *"What kind of bot is
bean counter running?"*
**Agent:** move-mining replay-study agent (s53), read-only except this file.
**Ground:** team `Bean counters`, id `47803c19-e264-4492-bd62-fbdd58cfd7e6`,
**rank 1 on the ladder**, 2,116 league matches in `corpus/league_matches.tsv`
(2026-08-01T07:52:43Z .. 2026-08-21T14:21:10Z).
**Corpus build:** `corpus/manifest.json` `built_utc = 2026-08-21T14:44:01Z`,
`git_sha d44861857`, 85,953 archived replays, join agree-rate 1.0000.
**Repo HEAD at study time:** `02cc6c9f7` (2026-08-21T16:53:32+02:00).
**Clock:** every timestamp from `date -u` in-shell or from the cited file.

**Method:** `docs/research/PLAYBOOK-move-mining-2026-08-16.md` +
`docs/research/corpus-howto.md`. Decoders used, none hand-rolled: the corpus
tables (`meta_join`, `events`, `build_agg`, `econ`, `flow`, `throws`,
`league_matches`) plus `tools/replay_census.py` (`Replay` / `census`, for
`chain_dir` / `ti_collected` / `core_deliv`) and two thin probes written for
this study over `replay_census.fields()`:
`scratchpad/s53_bean_verbs.py` (builderAttack field 13 / builderHeal field 15
with target-ownership classification; gunner `rotate()` re-emits) and
`scratchpad/s53_bean_seal.py` (core-adjacency ring occupancy, both directions).
Every claim is labelled **MEASURED** or **EYEBALL**; causal readings are
labelled **INFERENCE**; refuted hypotheses are retained.

**FROZEN DENOMINATOR.** The keeper daemon appends to `corpus/` while a study
runs — v68 grew from 90 to 100 archived games between 14:55Z and 15:11Z during
this one. **Every cell below is computed on a frozen set of 1,385 replay files
(v47 1,235 / v68 90 / v64 60)**, snapshotted at 14:55Z
(`scratchpad/s53_bean_census.jsonl`); `corpus/meta_join.tsv` as of 15:11Z is
kept at `scratchpad/s53_bean_meta_join.frozen.tsv`. Rated-record cells come from
`corpus/league_matches.tsv` read at 15:0xZ and are stated separately.

**POPULATION NOTE, stated once and applying to every cell.** These are **FIELD**
games — Bean counters against the whole league, not against us. **The archived
pool is 90% unrated challenge matches** (v47: 1,115 unrated / 120 ladder), and
unrated pools PROTOTYPES on the challenger side. Wherever it matters the rated
ladder cell is quoted separately, and it is the one to believe.

---

## 1. THE PLAIN ANSWER — what kind of bot Bean counters is running

**They run an economy-strangler that kills with a forward turret nest, and they
have just replaced it with a faster version.**

The shape of it: they spawn **four builder bots in the first four rounds and
essentially never spawn another**. Those four bots lay a big, tidy, *terminated*
conveyor network at home — 43 conveyors and 9 harvesters a game, of which **83%
of the harvesters still alive at the end have a directed path into their own
core** (ours, on the last comparable cut, was 58.8%). They convert about a third
of what they collect into ammunition — 530 Ti a game in **56 separate
`convert_ammo` calls**, i.e. a ~10 Ti top-up roughly every third round rather
than one big bank — and they spend it out of a small, permanent standing army. **They do not
build a single launcher — not one in 1,385 games.** They almost never touch the
enemy core with a builder bot. They do not turtle: **only 2.7% of their games
reach round 1000.**

What they do instead is the interesting part, and it is two verbs.

**Verb one: they cage the enemy core.** A core is a 2×2 block with exactly eight
orthogonally adjacent tiles, and those eight tiles are the *only* places a
conveyor can stand and deliver titanium into it — and the only places the core
can spawn a builder bot. **Bean counters put 55.5% of every barrier they build
on precisely those eight tiles**, occupying a median of five of the eight, and
sealing all eight in 22% of games. When they get a full seal, the victim's
harvester network stops reaching its own core: **directed connectivity falls
from 78.6% to 8.7%**, and the victim's titanium collected falls from a median of
975 to 170. It is a three-titanium building used as a tourniquet, and it works
in both directions — when an opponent does it back to Bean counters, Bean
counters' own connectivity falls the same way. This is the plank, and it is
cheap, mechanical and largely uncontested.

**Verb two: they plant sentinels in the band a gunner cannot answer.** A
sentinel shoots 5.66 tiles and ignores obstacles; a gunner shoots 3.6 tiles and
does not. **92% of Bean counters' sentinels are built in the enemy's half, at a
median distance² of 25 from the enemy core** — inside sentinel reach, outside
gunner reach. Meanwhile their *gunners* stay home (69% of them), where they are
used for something else entirely: **clearing forward turrets out of their own
ring, which they do at 79.7% against the field's 33.5%.** So the picture is a
long-range siege battery parked outside the defender's answer, behind a barrier
cage, while the home guns sweep anything the defender tries to plant back.

**Then, at 07:12Z this morning, they shipped v68 and it is a different bot.**
The commission described v68 as "a new line under test". It is not — **v68 has
played every one of their rated matches since 07:12:59Z and v47 has not played
since 04:12:59Z.** In seven hours v68 went **29 decided rated matches for 29
wins, 84.8% of 145 rated games, and +141.3 rating** (2153.1 → 2294.4; a 30th
match read 0-0, still in flight when the tape was read at 15:0xZ). v47's whole rated life
was 51.2% of 1,570 games. What changed: **they gave up the harvester-chewing
raid and pushed the gunners forward.** v47's builder bots spent the midgame
walking into the enemy economy and chewing harvesters — 129 builder attacks on
enemy harvesters a game. v68 does 20. In exchange, gunner shots went from 38 to
68 a game, gunner **rotations quadrupled** (2.0 → 8.1 a game, 10 Ti and a
cooldown each), and the gunners moved from 71% at home to **78% forward, sitting
right on the enemy core**. Their median kill moved from round 146 to **131**,
their kill share from 67.5% to 88.9%, and against the one opponent both versions
faced in volume (Part-timers, 365 vs 25 games) the same shifts appear with the
opponent held fixed. **This is a real step change, not an opponent-mix
artefact.**

**Where we differ from them, measured on our own last 1,115 archived games
(v168–v177) with the identical instruments.** The cage is *not* the gap: we
already build it — 75.4% of our barriers land on that ring against their 55.5%,
and we start at round 12 against their 35 — and our newest build v177 completes
the seal in 25.6% of games against their 22.3%. **The gap is the home guns.**
Bean counters destroy **79.7% ± 2.2** of the forward turrets planted in their
half (n=1,131 games, 5,803 turrets) while the opponents they face manage 33.5%.
We destroy **42.8% ± 3.3** (n=961 games, 3,799 turrets) — and the opponents
*we* face manage 43.3%. **They are 2.4× better than their own field at
clearing their ring; we are exactly average against ours.** That is the one
verb where the rank-1 team is doing something we are not, and the code path for
it already exists in our tree (`_door_turret`, `main.py:1653-1744`), so the
change is a constant rather than a feature.

**And we should be honest about where we stand against it.** Our record against
them is not merely stale — it is bad on the current versions. We have played
their v47 twice (2026-08-16 our v156, 2026-08-18 our v162) and their v68 once
(2026-08-21 08:11Z, our v175). **We lost all 15 games.** Against their older
v34 we took 16 of 40. Fifteen games is thin — the 95% upper bound on our true
share is about 20% — but the direction is unambiguous and it is worth a leg.

---

## 2. Provenance and premise corrections

**MEASURED.** Version census of Bean counters' rated matches,
`corpus/league_matches.tsv`, 2,116 matches:

| since 2026-08-19 | matches | since 2026-08-21T04:00Z |
|---|---|---|
| v47 | 156 | last rated match **04:12:59Z** |
| v68 | 30 | **07:12:59Z .. 14:21:10Z, unbroken** |
| v64 | 7 | 04:32:59Z .. 06:32:59Z |
| v52 | 1 | — |
| v66 | 1 | 06:52:59Z (single match) |

⛔ **PREMISE CORRECTION 1.** The commission read this split as "v47 the
workhorse incumbent + v68/v64 a new line under test". **The sequence says
otherwise: v47 → v64 → v66 → v68 is a shipping ladder executed this morning, and
v68 has been the sole incumbent for seven hours.** v47 is the *previous*
incumbent (2026-08-16T19:30Z .. 2026-08-21T04:12Z). This changes what the study
is for: the v47 profile is history-with-a-purpose, and **the v68 diff is the
live opponent.**

⛔ **PREMISE CORRECTION 2 — our record against them is not only v34.** From
`corpus/meta_join.tsv`, games where the opponent is OpenSverige
(`379a5d80-…`), by their version:

| their ver | fixture | our ver | date | games | **our wins** |
|---|---|---|---|---|---|
| v34 | ladder | — | 08-12 | 10 | 5 |
| v34 | unrated | v114–v121 | 08-12 | 30 | 11 |
| **v47** | unrated | v156 (08-16), v162 (08-18) | | **10** | **0** |
| **v68** | unrated | v175 | 08-21T08:11:52Z | **5** | **0** |

**MEASURED: 0 of 15 games against v47/v68** (3 matches, 3 different builds of
ours). Wilson 95% upper bound on our true game share = **20.4%**. Small, but the
"stale, we went 6/25" framing in the commission understates how bad the current
picture is. *(Denominator note: `meta_join` is the only table that carries these
— they are unrated challenges, not in `ladder_games.tsv`. That is the sanctioned
use of `meta_join`, not a win-rate denominator breach.)*

⛔ **INSTRUMENT NOTE, worth carrying forward.** `corpus/league_games.tsv` has
**0 rows** for Bean counters (checked: 3,705 rows, none match). Anyone reaching
for the free per-game `cond`/`turns` metadata on this team gets an empty set
that looks like a filter, not a gap. Kill-clock here is derived from the
**in-replay core DEATH event** in `corpus/events.tsv` instead.

---

## 3. v47 — the incumbent doctrine, profiled

All cells: 1,235 archived v47 games (1,115 unrated / 120 ladder),
2026-08-16T19:30Z .. 2026-08-21T04:21Z, 24 distinct opponents.

### 3.1 Outcome and kill clock — **MEASURED**

| fixture | n games | BC game share | core kill | **their** core died | r1000 | median kill round | k≤200 | k≤300 |
|---|---|---|---|---|---|---|---|---|
| all archived | 1,235 | 69.4% | 67.5% | 29.8% | **2.7%** | 146 | 50.5% | 60.1% |
| unrated only | 1,115 | 70.5% ±3.6 | 68.7% | 29.0% | 2.3% | 143 | 53.0% | 62.2% |
| **archived ladder only** | 120 | 59.2% | 56.7% | 37.5% | 5.8% | **204.5** | 27.5% | 40.8% |
| **RATED, all matches** (`league_matches`) | **1,570** (314 matches) | **51.2% ±3.1** | — | — | — | — | — | — |

Half-widths are 95%, DEFF-corrected per CLAUDE.md (rated 1.529, unrated 1.833).
**The 69.4% headline is a fixture artefact** — the archived pool is dominated by
teams challenging them unrated, and unrated pools prototypes on the challenger
side. **On the rated ladder v47 is a 51% bot** — which is what rank-1 looks like
when the ladder pairs you against your equals.

**INFERENCE:** the r1000 rate of 2.7% and a median kill at round 146 make this a
**rush/strangle bot, not a tiebreak turtle.** Under our own programme they are
inside the `<r300` band that we call on-programme.

### 3.2 Opening — **MEASURED**, and it is a lookup table

Modal first-8 build kinds (n=1,235): `bot bot bot bot conv conv conv conv`
27.0%, `bot bot bot conv bot conv conv conv` 12.1%, `bot bot bot conv bot conv
conv harv` 11.2%. First-build round by kind (median / p10 / p90 / coverage):

| kind | median | p10 | p90 | share of games |
|---|---|---|---|---|
| builder_bot | **0** | 0 | 0 | 100% |
| conveyor | 3 | 2 | 7 | 100% |
| harvester | 5 | 2 | 14 | 100% |
| barrier | 28 | 7 | 51 | 99% |
| gunner | 33 | 8 | 70 | 94% |
| sentinel | 50 | 15 | 116 | 84% |

**DETERMINISM — the strongest exploitable fact in this report.** Grouping the
1,235 games by **exact map (md5 of the replay's `battlecode.Map` block) × seat**
gives 30 cells averaging 41.2 games. Within a cell, **95.4% of games follow the
same first-six `(kind, x, y)` signature, and 21 of the 30 cells are 100%
identical, tile for tile.** (v68: 9 cells with ≥4 games, 41 games, **100%**
modal — but at 4.6 games/cell that number is nearly trivial and is reported only
for direction. v64: 5 cells, 25 games, 88.0%.)

**Consequence:** their first harvester tile is knowable from one prior game on
that (map, seat). Example anchors, v47, map-shape cells: 25×25 seat0 first
harvester **(10, 6)** in 45/45 games; 25×25 seat1 **(14, 18)** in 45/45; 26×26
seat1 **(21, 23)** in 46/46; 20×26 seat0 **(9, 2)** in 45/45.

### 3.3 Economy shape — **MEASURED**

Per game, BC vs the opponent in the **same** games (in-game mirror control):

| | BC | opponent (same games) |
|---|---|---|
| conveyors built | 43.3 | 28.5 |
| harvesters built | 8.9 | 4.5 |
| barriers built | 16.6 | 4.5 |
| builder bots spawned | **4.4** | 5.8 |
| **launchers built** | **0.00** | 0.48 |
| splitters built | 0.00 | — |
| `titanium_collected` (mean / median) | 1,658 / 1,330 | 1,042 / 570 |
| titanium banked at end (mean) | 186 | 151 |
| core deliveries/game (mean / median) | 165.8 / 133 | 104.2 / 57 |
| ammo converted (Ti) / convert calls | **530 / 56.2** | 396 / 49.0 |
| harvesters alive at end: **directed**-connected | **82.7%** (6,722/8,133) | 64.1% (1,693/2,643) |
| resource moves reaching own core | 10.3% | 10.6% |
| resource moves leaked to enemy net | **0.2%** | 0.7% |
| moves gifted to the enemy CORE | **0.000/game** | 0.011/game |

**How the economy is converted:** ~32% of collected titanium becomes ammunition
(530 of 1,658), in ~56 separate `convert_ammo` calls per game — i.e. they top up
constantly rather than banking. The rest goes into 43 conveyors + 9 harvesters +
17 barriers + ~6 turrets, and they finish holding almost nothing (mean 186 Ti).
**INFERENCE: this is a bot that spends to the floor and never accumulates a
war-chest.**

#### SEEDED FRAGMENT 1 — the 79.7% "binding-tile" figure: **RESTORED, and its population corrected**

The cited figure is at `docs/research/binding-tile-cut-2026-08-10.md:248`:
*"Per-team directed rate across third-party teams with ≥30 surviving harvesters
(n=10): … **Bean counters 79.7%**"*. **Its true semantics, recovered:** the share
of harvesters *alive at the end* that had a **directed** conveyor path to their
own core, computed by `tools/replay_census.py`'s `chain_dir` — **on ROUND-1000
GAMES ONLY** (the whole §4 population is 2,271 r1000 games), on the 2026-08-10
archive, i.e. their **v28/v34 era**. Its own denominator for Bean counters is not
printed in the doc beyond "≥30 surviving harvesters".

**Re-derived on current v47 data — MEASURED: 82.7%** (6,722 directed of 8,133
harvesters alive at end, across **all 1,235 v47 games**, `chain_dir` from the
same instrument). v68: **81.4%** (445/547, n=90). v64: **81.7%** (316/387,
n=60).

⚠ **The old figure is CONFIRMED in magnitude but its population is now nearly
empty:** it described r1000 games, and **only 2.7% of v47 games reach r1000.**
Quote 82.7% on all games; do not quote 79.7% as a current fact.

⚠ **NAME COLLISION WARNING.** §3.6 below independently produces the number
**79.7%** for a *completely different* quantity (forward-turret removal rate).
Two unrelated 79.7%s about the same team. Always carry the subject.

### 3.4 The kill mechanism — the barrier cage on the enemy core

**MEASURED, `scratchpad/s53_bean_seal.py`, n=1,235 v47 games.** The enemy core's
2×2 footprint has exactly **8 orthogonally adjacent tiles** (the "ring"). Those
are the only tiles from which a conveyor can output into the core, and the only
tiles the core can spawn a builder bot onto.

| | BC → enemy ring | **MIRROR CONTROL:** opponents → BC's ring |
|---|---|---|
| ring tiles open (non-wall), median | 8 | 8 |
| max ring tiles simultaneously held, median | **5 of 8** | **1 of 8** |
| full 8/8 seal achieved | **22.3%** of games | 7.9% |
| ≥6/8 held | 46.7% | 14.9% |
| any ring build at all | 96% (median first at r35) | 72% (r40) |
| **share of ALL their barriers landing on that 8-tile ring** | **55.5%** (11,405 of 20,540) | 2,120 total |

v68: 39.6% of barriers on the ring, median 6/8 held, 22.2% full seal (n=90).
v64: 34.3%, median 7/8, 33.3% full seal (n=60).

**The mechanism, with the control that must run the other way — MEASURED.**
Directed connectivity of the *sealed* team's own surviving harvesters, banded by
how much of its ring was held (v47, n=1,235 games):

| ring tiles held by the attacker | victim = the OPPONENT (BC seals) | **MIRROR: victim = BC** (opponents seal) |
|---|---|---|
| 0–5 of 8 | 78.6% (1,417/1,803 harvesters) | 87.6% (6,151/7,019) |
| 6–7 of 8 | 47.1% (249/529) | 65.5% (390/595) |
| **8 of 8 FULL** | **8.7% (27/311)** | **34.9% (181/519)** |

and the same banding against titanium actually collected:

| seal | enemy `ti_collected` med | enemy core deliveries med | game length med |
|---|---|---|---|
| 0–3/8 (n=366) | 975 | 98 | 174 |
| 4–5/8 (n=292) | 715 | 72 | 159 |
| 6/8 (n=154) | 495 | 50 | 157 |
| 7/8 (n=148) | 350 | 35 | 146 |
| **8/8 (n=275)** | **170** | **17** | 149 |

**Mirror control on the same table:** BC's own median collection under an
opponent seal runs 1,370 / 1,295 / 1,360 / 1,210 / **550** across the same
bands — flat until a *full* seal, then a collapse. **And the length confound runs
the WRONG way for the mirror** (median game length rises 149 → 209 as the seal
tightens, i.e. more time to collect, and collection still halves). The mechanism
is a property of the ring, not of Bean counters.

⛔ **REFUTED IN PASSING — RETAINED so nobody re-derives it. The ring is NOT
spawn denial.** The obvious reading is "sealing the ring stops them spawning
builder bots". **It does not, because the seal arrives too late:** median first
ring build is round **35**, and opponents spawn essentially all their builders in
rounds 0–5 (opponent `build_builder_bot` by band, v47: r0-150 5.36, r150-200
0.14, r200-300 0.12, r300+ 0.18 — only 0.44 late spawns per game exist to
deny). The "enemy spawns after the first ring build ≈ 0" statistic is real
(median 0, mean 1.09, n=1,180) **and is confounded to the point of being
worthless.** The live mechanism is **delivery-face denial**, measured above.

### 3.5 Where the turrets go — the gunner-proof band

**MEASURED**, placement geometry from `corpus/events.tsv` BUILD rows
(d² to own core / d² to enemy core, computed by `tools/corpus/replay_events.py`):

| v47, BC side | n built | median d to own core | median d to enemy core | built in the enemy's half |
|---|---|---|---|---|
| sentinel | 2,979 | 15.8 | **5.0** | **91.7%** |
| barrier | 20,540 | 14.1 | **2.2** | 91.0% |
| gunner | 4,002 | 5.0 | 13.2 | 28.7% |
| harvester | 10,945 | 7.1 | 14.4 | 9.5% |
| conveyor | 53,442 | 5.8 | 15.2 | 14.3% |
| *[control] opponent gunner* | 6,031 | — | — | 75.8% |
| *[control] opponent sentinel* | 1,778 | — | — | 69.1% |

**The standoff band — MEASURED.** Gunner attack range is r²=13, sentinel r²=32,
and the sentinel's line ignores obstacles. Distribution of BC sentinel builds by
d² to the **enemy** core:

| d² to enemy core | v47 sentinels (n=2,979) | v68 sentinels (n=184) |
|---|---|---|
| ≤13 — inside a defending gunner's reach | 23.9% | **53.3%** |
| **14–32 — sentinel band, gunner-proof** | **48.1%** | 32.1% |
| 33–64 | 28.0% | 14.7% |
| >64 (home) | 0% | 0% |

Median v47 sentinel sits at **d² = 25**. **INFERENCE:** the modal v47 sentinel is
deliberately parked where a defending gunner cannot reach it, and shoots the core
through whatever is in the way. v68 abandons that caution and walks onto the core
(median d²=13 for both sentinels and gunners).

### 3.6 Defensive verbs — ring clearance, heals, and what they do NOT do

**MEASURED, per game, `scratchpad/s53_bean_verbs.py`** (builderAttack = update
field 13, builderHeal = field 15, per `tools/replay_schema.md:62,64`; target
classified by the owner of the building standing on the target tile):

| verb (per game) | BC v47 | opponent, same games |
|---|---|---|
| builder attacks on enemy **harvesters** | **128.7** | 18.9 |
| builder attacks on enemy **conveyors** | 70.8 | 24.9 |
| builder attacks on enemy barriers | 18.5 | 18.4 |
| builder attacks on enemy turrets | 5.4 | 5.7 |
| **builder attacks on the enemy CORE** | **0.01** | 0.82 |
| heals on own buildings | 20.6 | 139.6 |
| **heals on own CORE** | 26.6 | 68.5 |
| gunner `rotate()` calls | 2.0 | 3.8 |
| own builders displaced >1 tile (thrown) | 0.12 | 2.21 |
| **launcher throws performed** | **0** | 2,830 (v47 games) |

*Instrument cross-check:* my probe's independent `batk_enemycore` for the
opponent side reads **0.82/game**, matching `corpus/build_agg.tsv`'s
`batk_core` metric (0.82/game) computed by a different decoder with its own core
footprint logic. Two decoders, same number.

*In-leg mirror control (playbook §3):* every column above was produced by the
same code path with the side index swapped, and the columns **do** flip —
BC 128.7 / OPP 18.9 on harvester chewing, BC 0.01 / OPP 0.82 on core melee, BC 0
/ OPP 2,830 on throws. The instrument discriminates in both directions.

**RING CLEARANCE — and this recovers seeded fragment 2.**

#### SEEDED FRAGMENT 2 — "Bean counters 55% vs our 16%": **located, denominator UNRECOVERABLE, restated on current data**

*Located at* `docs/research/BOOK-0033-2026-08-14.md:90-93`, flagged as the
repo's most-exposed bare estimate at
`docs/research/BARE-STRATIFIED-SWEEP-2026-08-14.md:14`. Verbatim: *"their
fwd-turret removal 51% in field games they LOSE vs our 14% in our losses (field
opponents: ph 67%, Flotte 68%, **Bean counters 55% vs our 16%**)"*.

**Semantics:** share of the *attacker's* forward turrets (gunner+sentinel planted
in the defender's half) that the **defender destroys**, computed **only in games
the defender loses**.
**Denominator: NOT RECOVERABLE.** The sweep's own audit says *"no n anywhere, no
interval … this claim's cut is un-named"*; the book names its scripts only as
session scratchpad files (`BOOK-0033:4-5` — `prof.py`, `nest.py`), which died
with s39. The sweep's structural objection stands independently: **the statistic
is stratified on the outcome**, so the three "replications" repeat the
conditioning rather than test it, and two builds (NESTSHOT, NESTSHOT2) were spent
on it before NESTSHOT2 futility-dropped at 45.75 @ n=1012.
⇒ **The quoted "55% vs our 16%" is UNUSABLE as written and must not be re-cited.**

**Restated on current data, in the outcome-unconditional form the sweep
demanded — MEASURED** (games as units, forward turret = a gunner/sentinel built
closer to the defender's core than to its own; removal = a death of that kind on
that tile at a later round; v47, frozen set):

| defender | fixture | n games | fwd turrets | **removal rate** |
|---|---|---|---|---|
| **Bean counters v47** | **ALL games** | **1,131** | 5,803 | **79.7% ± 2.2** |
| Bean counters v47 | games they win | 734 | 2,678 | 89.0% ± 2.3 |
| Bean counters v47 | games they lose | 367 | 2,746 | **61.2% ± 3.7** |
| their opponents | ALL games | 1,047 | 3,881 | **33.5% ± 3.0** |
| their opponents | games they win | 202 | 518 | 67.7% ± 7.9 |
| their opponents | games they lose | 818 | 3,244 | 23.8% ± 2.7 |
| Bean counters v68 | ALL games | 61 | 117 | 76.6% ± 11.1 |
| their opponents (vs v68) | ALL games | 90 | 511 | 53.3% ± 6.5 |

Half-widths 95%, game-level, DEFF 1.833 applied (unrated-dominated pool).
**The unconditional gap is 79.7% vs 33.5% — 46pp, with no outcome conditioning
and no cross-population ratio.** The old book's loses-stratum figure of 55%
sits close to today's 61.2% ± 3.7, but they are different eras (v28/v34 vs v47)
and only one of them has an n.

**INFERENCE on the mechanism:** clearance is done by **turret fire, not builder
melee** — builder attacks on enemy turrets are only 5.4/game while they fire
75/game, and 69% of their gunners are home-side. The home gunners are the ring
sweeper.

### 3.7 CPU — **MEASURED, and it closes a road**

`corpus/econ.tsv`, per-game peak single-unit CPU (max over bands) and timeouts:

| | median peak µs | p90 | p99 | max | **TLEs / unit-turns** |
|---|---|---|---|---|---|
| **BC v47** | 4,733 | 7,045 | 8,130 | 13,821 | **3 / 1,825,401 (0.0002%)** |
| opponents, same games | 3,734 | 10,318 | 11,280 | 11,968 | 3,933 / 1,929,179 (0.204%) |
| **BC v68** | 4,185 | 8,573 | 9,050 | 9,050 | **0 / 90,930** |
| opponents, same games | 6,195 | 10,071 | 11,315 | 11,315 | 108 / 93,096 (0.116%) |

**They leave ~19% of the 10 ms budget unused at p99 and time out three times in
1.8 million unit-turns, against the field's 1-in-500.** ⇒ **CPU-denial /
timeout-induction is a dead road against this opponent** (and separately it is
held ON NORMS by `SIX-ROADS-STATUS`; the two must not be merged).

### 3.8 Reaction latency and replacement — **MEASURED**

Rounds from the death of a BC building to BC's next build of the same kind
(v47, n=1,235 games):

| kind | deaths | replaced | median latency | p90 |
|---|---|---|---|---|
| conveyor | 12,644 | 93% | **2** | 13 |
| barrier | 7,981 | 93% | **2** | 14 |
| builder_bot | **520** (0.42/game) | 91% | 2 | 23 |
| harvester | 2,812 | 69% | 10 | 80 |
| gunner | 1,486 | **66%** | 10 | 59 |
| sentinel | 1,186 | **84%** | **12** | 78 |

v68: sentinel deaths 44, replaced 84%, **median latency 33 rounds (p90 111)**;
gunner 343 deaths, 62% replaced, median 10.

⛔ **REFUTED — RETAINED.** The attractive hypothesis "*they only ever spawn four
builders, so kill the builders and the doctrine stops*" **does not survive the
data**: they lose only **0.42 builder bots per game** and replace 91% of them
within a median of 2 rounds. Their builders are hard to kill and cheaply
replaced. The exploitable latency is on **turrets**, not builders.

### 3.9 Launcher / throw usage — **MEASURED, and it is zero**

**Bean counters built 0 launchers and performed 0 throws in 1,385 games**
(v47/v64/v68). Their opponents in the same files performed 2,830 throws (v47),
of which **162 were kidnaps of a Bean counters builder** (`kind == EXILE`,
`corpus/throws.tsv`).

⛔ **REFUTED — RETAINED. Border crash-induction is NOT demonstrated against
them.** Of the 162 kidnaps, 95 landed on a border tile; victim fate on those:
13 ALIVE_END, 81 RETHROWN, **1 DIED**. Field baseline over all 195,517 border
exiles in the archive: **2.2% DIED**. 1/95 = 1.1% is inside that baseline (95%
CI 0.03–5.7%). **We have no evidence their bot dies to an off-map query, and
n=162 is far too small to exclude it either.** What *is* established is that the
mechanism has been fired at them ~162 times by the field already, so it is not
an unpressed button.

---

## 4. THE v47 → v68 DIFF — what changed, and where they think their edge moved

**Honest denominators, stated per cell: v47 n=1,235 archived games (120 rated),
v64 n=60 (5 rated), v68 n=90 archived games (15 rated) + 145 rated games in
`league_matches`.** v68 is seven hours old. Every v68 share below is a small-n
share; the DEFF/cluster caveats in CLAUDE.md apply and are applied where a
half-width is printed.

### 4.1 The rated result — **MEASURED**, `corpus/league_matches.tsv`

| version | rated matches | rated games | **game share** | match share |
|---|---|---|---|---|
| v47 | 314 | 1,570 | **51.2% ± 3.1** | 48.7% |
| v64 | 7 | 35 | 88.6% | 7/7 |
| **v68** | **29 decided** (+1 in flight) | **145** | **84.8% ± 7.2** | **29/29** |

Difference v68 − v47 = **+33.6pp ± 10.5pp** (95%, two-fixture form with rated
DEFF 1.529 on both terms). ⚠ **Opponent quality is NOT matched between these two
cells** — v47's 314 matches span their whole climb, v68's 30 span seven hours at
rank 1. Treat the number as large-and-real, not as a clean effect size.

Rating trajectory: v68's first rated match at 07:12:59Z opened at **2153.1**;
its 30th at 14:21:10Z opened at **2294.4**. **+141.3 in seven hours, 29 decided
matches, zero match losses.** Score shape: 5-0 ×10, 4-1 ×16, 3-2 ×3.

### 4.2 Behavioural diff, pooled and matched — **MEASURED**

Pooled (all opponents), per game:

| | v47 (n=1,235) | v64 (n=60) | **v68 (n=90)** |
|---|---|---|---|
| core kill share | 67.5% | 91.7% | **88.9%** |
| their core died | 29.8% | 5.0% | 11.1% |
| median kill round | 146 | 147 | **131** |
| k≤200 | 50.5% | 66.7% | **81.1%** |
| r1000 | 2.7% | 3.3% | **0.0%** |
| **builder attacks on enemy harvesters** | **128.5** | 26.7 | **19.9** |
| builder attacks on enemy conveyors | 70.7 | 18.7 | 15.6 |
| **gunner `rotate()` calls** | **2.0** | 9.1 | **8.1** |
| shots — gunner | 38.5 | — | **68.2** |
| shots — sentinel | 36.7 | — | 36.7 |
| gunners built | 3.24 | 6.08 | 4.73 |
| **gunners built in the enemy's half** | **28.7%** | — | **77.9%** |
| sentinels built in the enemy's half | 91.7% | — | 97.3% |
| sentinels at d²≤13 of the enemy core | 23.9% | — | **53.3%** |
| barriers built | 16.6 | 23.1 | 17.8 |
| barriers landing on the enemy spawn/delivery ring | 55.5% | 34.3% | 39.6% |
| harvesters built | 8.86 | 8.12 | 6.53 |
| builder bots spawned | 4.38 | 4.00 | 4.07 |
| heals on own core | 26.6 | 14.7 | 10.3 |
| ammo converted (Ti) | 530 | — | **650** |
| launchers built | **0** | **0** | **0** |

**MATCHED-OPPONENT CONTROL** — the only opponent both versions met in volume:

| vs **Part-timers** | v47 (n=365) | v64 (n=20) | v68 (n=25) |
|---|---|---|---|
| core kill share | 94.2% | 100% | 100% |
| median kill round | 120 | 105.5 | **111** |
| k≤200 | 89.0% | 100% | 100% |
| batk on enemy harvesters | 35.6 | 14.1 | **13.2** |
| batk on enemy conveyors | 27.4 | 14.2 | 13.6 |
| **gunner rotations** | **1.44** | 5.75 | **5.72** |
| gunners built | 2.37 | 3.40 | 3.00 |
| heals on own core | 29.6 | 17.3 | 13.6 |
| barriers built | 15.8 | 16.0 | 15.6 |
| harvesters built | 8.54 | 6.65 | 6.36 |

And a second matched cell (Pantheon, the opponent that hurts them most on the
new line):

| vs **Pantheon** | v64 (n=20) | v68 (n=30) |
|---|---|---|
| core kill share | 90.0% | 73.3% |
| their core died | 10.0% | **26.7%** |
| median kill round | 205 | 138 |
| batk on enemy harvesters | 39.8 | 26.5 |
| gunner rotations | 11.7 | 10.1 |
| gunners built | 8.45 | 5.17 |

**READ — INFERENCE.** With the opponent held fixed, the v47→v68 changes that
survive are: **(a) the harvester-chewing raid is cut to ~37% of its former
volume; (b) gunner rotations quadruple; (c) gunners relocate from home to the
enemy core; (d) core self-heal roughly halves; (e) the kill lands a few rounds
earlier.** The barrier ring and the home economy are **unchanged** — those are
the stable spine of the doctrine across three versions.

**Where they think their edge moved:** from *starving the opponent's economy with
builder melee* to *out-shooting them at the core with a mobile-facing gunner
line*. They spent the builder-time budget on the seal and the nest instead, and
they bought 120 Ti/game more ammunition to feed it.

### 4.3 Who actually beats them — **MEASURED**

Per-opponent, v47, share of games in which **Bean counters' core died**:

| opponent | n games | BC kill | **BC died** |
|---|---|---|---|
| HTTP 418 | 20 | 30.0% | **70.0%** |
| **Pivot** | **300** | 35.0% | **61.0%** |
| O(1) | 50 | 46.0% | 54.0% |
| DinooniD | 50 | 44.0% | 50.0% |
| Lorem Ipsum | 15 | 53.3% | 46.7% |
| Pantheon | 30 | 43.3% | 40.0% |
| Erebus | 150 | 66.0% | 32.0% |
| Jython | 45 | 62.2% | 28.9% |
| **Part-timers** | 365 | 94.2% | 5.8% |
| **OpenSverige (us)** | 10 | **90.0%** | **0.0%** |

⚠ **Fixture caveat, and it is load-bearing:** 90% of these are unrated
challenges, so a team with 300 games against Bean counters is a team **drilling
against them with prototypes**. "Pivot beats them 61%" is a
prototype-vs-shipped comparison. It still tells us what the counter-shape looks
like.

**The counter-recipes, profiled — MEASURED** (opponent-side build and verb
census in those same games):

* **Pivot** (n=300, kills them 61%, median round 214): 9.26 gunners/game **73%
  forward**, 6.3 barriers 96% forward, **307 heals/game on their own
  buildings**, 56 builder attacks on BC harvesters. **Does NOT seal BC's ring**
  (median 1/8). A grind: out-heal the siege, out-gun the nest.
* **O(1)** (n=50, 54%): **seals BC's ring — median 8/8, full seal in 58% of
  games**, plus 56 builder attacks/game on BC's barriers and 30 on their
  gunners. Mirrors the tourniquet back.
* **DinooniD** (n=50, 50%): seal median 7/8, 42% full; 84 attacks/game on BC
  conveyors, 50 on BC barriers.
* **HTTP 418** (n=20, **70%** — best kill rate, smallest n): the only counter
  that **builds launchers — 2.55/game, 61% of them forward** — plus a 7/8 median
  seal (35% full). ⚠ n=20 games / 4 matches. **EYEBALL-grade on the launcher
  attribution; it is a build count, not a demonstrated causal channel.**
* **Part-timers** (n=365, dies 94.2%): builds **0.05 barriers/game**, never
  seals, 10.8 heals/game. The control case — a team that does none of the above
  gets flattened.

**INFERENCE, and it is the single most actionable line in this report:** the
three teams that beat v47 most often all do at least one of *(seal their ring
back at them)* or *(out-heal the siege)*, and the one team that does neither
loses 94% of its games. **Sealing Bean counters' own core ring is a
counter-doctrine that the field has already validated on live games without us.**

---

## 5. EXPLOITABLE HABITS, RANKED (play-the-players)

Ranked by (measured size × our ability to act on it × how cheap the test is).

**1. THE OPENING IS A LOOKUP TABLE — determinism.** 95.4% modal first-six build
signature across 30 (exact map × seat) cells averaging 41 games; **21 of 30
cells are 100% identical, tile for tile** (v47, n=1,235). First harvester lands
at a median round 5. ⇒ **Their first harvester tile is knowable from one prior
game on that map and seat.** A 3 Ti barrier on that ore tile makes
`can_build_harvester` false. Cheap, mechanical, and it hits the round-5 spine of
every game they play. *Risk: the v68 cells are too small (4.6 games/cell) to
confirm the table survived the version bump — re-derive before firing.*

**2. THEIR OWN RING IS THE SOFT SPOT — and we already have the tool, we just
finish it less than half the time.** Opponents hold a median of **1 of 8** tiles
on Bean counters' core ring; when someone gets all 8, **Bean counters' own
harvester connectivity falls 87.6% → 34.9%** and their median collection halves.
O(1) achieves a full seal in 58% of its games against them and takes 54% of
them; HTTP 418 seals 7/8 and takes 70%. **We ship the seal already**
(`LOKI_BARRIER_SEAL_ON`, §6.1) and aim at it harder than they do, but we complete
it in only **12.0%** of our games (n=1,115, v168–v177), swinging 0.0% → 25.6%
across six versions with no instrument on it. ⇒ **The habit to exploit is
theirs; the work is ours, and it is completion, not adoption.**

**3. ZERO LAUNCHERS, EVER — 0 in 1,385 games.** They have no throw, no
counter-throw, and no code path that has ever had to survive one. Their siege
requires builder bots standing **adjacent to our core** from a median of round 35
onward — a stationary, escortless kidnap target, on a script we can predict
(habit 1). Note the honest caveat: the field has already exiled their builders
162 times and only 1 of 95 border throws killed one, so **the crash channel is
unproven; the displacement channel (throw them off the cached plan) is
untested.**

**4. TURRET REPLACEMENT LATENCY IS A BLINDNESS WINDOW.** Kill a forward
sentinel and they take a **median 12 rounds (p90 78)** to replace it, and
**16% are never replaced**; a gunner, median 10 rounds and **34% never
replaced**. On v68 the sentinel latency stretches to **median 33 rounds (p90
111)**, n=44 deaths. Contrast their *carriers*: conveyors and barriers come back
in 2 rounds, 93% of the time. ⇒ **Break the guns, not the belt.**

**5. THEY SPEND TO THE FLOOR.** Mean end-of-game bank 186 Ti (v47) / 137 (v68),
with 56–73 separate `convert_ammo` calls per game. ⇒ **INFERENCE (untested):
they have little reserve to absorb a sudden cost-scale shock or a burst of
repairs.** No measurement here supports acting on it yet; recorded as a
hypothesis, not a habit.

**6. CPU IS NOT A LEVER — CLOSED.** 3 timeouts in 1,825,401 unit-turns; p99 peak
8,130 µs of 10,000. Do not spend a leg on CPU denial against this opponent.

**7. THEY NEVER MELEE A CORE — 0.01 builder attacks on the enemy core per game.**
⇒ **INFERENCE:** their finishing damage is entirely turret fire, so anything that
denies turret *positions* near our core (rather than killing builders) attacks
the whole kill chain. This is the same target as habit 4 and is listed separately
because it names a different verb (deny the tile vs kill the turret).

---

## 6. US vs THEM — the incumbent GREP, and where the gap actually is

### 6.1 GREP against the incumbent (`bots/_v542wave`) — **all five resolved**

A delegated read of `bots/_v542wave/{main,doctrine,eco,raid,siege}.py`
(read-only, file:line anchors below) answered the five behaviours this study
would otherwise have proposed:

| behaviour Bean counters uses | do we already ship it? | anchor |
|---|---|---|
| **barrier ring on the ENEMY core's 8 orthogonals** | **YES** — `LOKI_BARRIER_SEAL_ON = True` (`doctrine.py:1227`), `LOKI_SEAL_TI_FLOOR = 0` (`doctrine.py:1228`), ring built at `raid.py:306`, ring enumerated at `raid.py:112-127` and documented at `raid.py:333` *"the eight tiles orthogonally adjacent to the enemy footprint"*; `FS_CLEAR_RING_ON = True` (`doctrine.py:2485`) additionally destroys enemy buildings occupying a needed seal tile (`eco.py:2480-2484`); diagonals deliberately deferred, `FS_DIAG_DEFER = True` (`doctrine.py:2494-2505`) | ✅ |
| **forward sentinel in the (13, 32] gunner-proof band** | **PARTIALLY** — we cap at `d > 32: continue` (`siege.py:6139`) and maximise distance inside it (`FS_SENTINEL_FAR_FIRST = True`, `doctrine.py:2526`; scoring `siege.py:6158`) plus firing-axis avoidance (`FS_SENTINEL_GUNAXIS_PENALTY = 64`, `doctrine.py:2527`, `siege.py:6160-6161`). **There is no named lower bound at `GUNNER_RANGE_DSQ = 13`** (`doctrine.py:730`, used only for our home gunner's beltbreak scan at `main.py:2420,2524`) | ◐ |
| **barrier on an enemy ORE tile to pre-empt their harvester** | **NO** — no such branch exists in any of the five files | ❌ |
| **ring clearance: destroying enemy turrets planted in OUR half** | **YES** — `_door_turret` (`main.py:1653-1706`) ranks enemy `GUNNER`/`SENTINEL`/`LAUNCHER` (`FS_DOOR_TYPES`, `doctrine.py:2662`) within `FS_DOOR_DSQ = 40` (`doctrine.py:2654`), walked in by `_door_turret_turn` (`main.py:1708-1744`), gated `FS_HOME_TURRET_RESPONSE = True` (`doctrine.py:2653`), floor `FS_DOOR_TI_FLOOR = 6` (`doctrine.py:2658`); plus `SABOTAGE_PRIO` (`main.py:47-52`) and `TURRET_PRIO` (`main.py:53-59`) | ✅ |
| **launchers / kidnap-exile** | **YES** — `_try_build_launcher` (`main.py:1936`, `LAUNCHER_MIN_RND = 160`, `doctrine.py:1735`), forward builds at `siege.py:1892-1929, 4972-5008`, eviction `_fs_evict` (`siege.py:6684-6759`, `FS_EVICT_ON = True`, `doctrine.py:2406`, `FS_DUMP_FAR_DSQ = 36`, `doctrine.py:2441`), wired at `siege.py:6284-6286`; raider-side at `raid.py:1329-1417` | ✅ |

⇒ **Three of the five "new moves" this study would have proposed are already
shipped.** That is the playbook's cheapest-null guard doing its job before a
slot was spent.

### 6.2 So how do our numbers compare? — **MEASURED, same instruments, our own games**

Both cuts below use the *identical* probe code with only the team index
changed, run over **1,115 of our archived games on v168–v177**
(2026-08-20T08:03Z .. 2026-08-21T15:03Z), `scratchpad/s53_bean_ourseal.py`.

**Ring seal attainment — we already target it HARDER and EARLIER, and we
attain it LESS OFTEN:**

| | **US v168–v177** (n=1,115) | **Bean counters v47** (n=1,235) |
|---|---|---|
| share of our barriers landing on the enemy ring | **75.4%** (7,375/9,782) | 55.5% (11,405/20,540) |
| games with any ring build | 98% | 96% |
| median round of first ring build | **12** | 35 |
| median ring tiles simultaneously held | 5 of 8 | 5 of 8 |
| **full 8/8 seal** | **12.0%** | **22.3%** |
| ≥6/8 held | 39.1% | 46.7% |
| *mirror: opponents sealing OUR ring* | 9.3% full, median 2/8 | 7.9% full, median 1/8 |

Per version of ours: v172 2.7%, v173 **0.0%**, v174 19.2%, v175 5.3%, v176
6.1%, **v177 25.6%** (n=180, today from 12:33Z). **INFERENCE: our seal
attainment is volatile version to version and nobody is watching it** — v177
now exceeds Bean counters' rate, v173 achieved a full seal in zero of 35 games.

**Forward-turret ring clearance — this is the real gap, and it is 37pp.**
Same instrument, same definition (a forward turret = a gunner/sentinel the
attacker built closer to the defender's core than to its own; removal = a death
of that kind on that tile at a later round), games as units, DEFF 1.833:

| defender | fixture | n games | fwd turrets | removal |
|---|---|---|---|---|
| **Bean counters v47** | ALL | 1,131 | 5,803 | **79.7% ± 2.2** |
| their opponents (same games) | ALL | 1,047 | 3,881 | 33.5% ± 3.0 |
| **US v168–v177** | ALL | 961 | 3,799 | **42.8% ± 3.3** |
| our opponents (same games) | ALL | 865 | 2,754 | 43.3% ± 3.8 |
| US v168–v177 | our losses | 551 | 2,629 | 30.6% ± 3.2 |
| Bean counters v47 | their losses | 367 | 2,746 | 61.2% ± 3.7 |

**Read the two fixtures INTERNALLY, which is the comparison that is valid:**
Bean counters clear **2.4× better than the opponents they face** (79.7 vs
33.5); **we clear exactly as well as the opponents we face** (42.8 vs 43.3).
**They are exceptional at this verb and we are precisely average at it.**
*(Cross-fixture the gap is 36.9pp, but the two fixtures face different opponent
pools — quote the internal ratios, not the raw difference.)*

**This also completes seeded fragment 2's missing half.** The book's paired
"*our 16%*" (v10x era, no n) restates on current data as **30.6% ± 3.2 in our
losses (n=551 games, 2,629 turrets)** and **42.8% ± 3.3 unconditionally
(n=961)**. Whether the old 16% was wrong or we have genuinely doubled cannot be
told, because the old cut has no n and its script is gone.

### 6.3 QUEUE-ROW CANDIDATES

*(Drafted for research to admit or reject. Not added to QUEUE.md by this study.
Four-part admission + GREP stamp on each.)*

#### CANDIDATE A — **DOORWIDE**: raise our forward-turret clearance rate toward theirs

1. **CHANGE.** Tune the already-shipped door-turret response, named to its
   constants: `FS_DOOR_DSQ = 40` (`doctrine.py:2654`) — Bean counters answer
   turrets planted anywhere in their half, our radius stops at d²=40 —
   and `FS_DOOR_TI_FLOOR = 6` (`doctrine.py:2658`); optionally admit
   turret-fire clearance alongside builder melee (BC clear with turret fire:
   5.4 builder attacks on enemy turrets/game against 75 shots/game).
2. **MECHANISM METRIC only this change can move.** **Forward-turret removal
   rate, unconditional, games as units** — our 42.8% ± 3.3 (n=961) against our
   own opponents' 43.3%. The target shape is BC's internal ratio (2.4× their
   own field), not a raw percentage.
3. **FIXTURE.** Unrated legs, pooled across ≥4 windows. The metric is per-turret
   inside per-game shares, so it resolves far faster than a win rate; the
   decoder is the one in this study (`corpus/events.tsv` BUILD/DEATH +
   positional matching).
4. **WHY A SLOT NOW.** It is the one verb where the rank-1 team is
   *measurably exceptional relative to its own field* and we are *measurably
   average relative to ours*, on n≈1,000 games each side; and the code path
   already exists, so the change is a constant, not a feature.
   ⚠ **Run `tools/target_value.py` before the prereg** — not run by this study.
   ⚠ **Overlap check owed:** this is adjacent to the NESTSHOT / NESTSHOT2 ground
   (futility-dropped at 45.75 @ n=1012, `BARE-STRATIFIED-SWEEP-2026-08-14.md:14`),
   whose parent claim is the very cell restated in §6.2. **Research must state in
   writing how DOORWIDE differs from NESTSHOT2 before admitting it.** NESTSHOT
   attacked the *attacker* side (our forward nest surviving); DOORWIDE is the
   *defender* side (clearing theirs) — but that distinction has to be made
   explicitly, not assumed.
   **HOT-TURN RIDER: adds** — widening `FS_DOOR_DSQ` enlarges a per-turn
   candidate scan on the home-defence path; the builder must stamp it against
   the ~1,200 µs GRAND margin.
   **PROGRAMME:** defensive verb ⇒ carries `DEFENCE_ADMISSION_BAR`'s r300
   timely-kill non-regression as the primary.

#### CANDIDATE B — **SEALWATCH**: a monitor, not a plank

1. **CHANGE.** None to the bot. Add full-seal attainment (share of games
   reaching 8/8 on the enemy ring, and median tiles held) to whatever per-version
   dashboard the builder reads.
2. **MECHANISM METRIC.** The attainment share itself: v172 2.7%, v173 **0.0%**,
   v174 19.2%, v175 5.3%, v176 6.1%, v177 25.6% (n as listed).
3. **FIXTURE.** The archive; no games need firing.
4. **WHY NOW.** `LOKI_BARRIER_SEAL_ON` has been True throughout, and s30
   measured `barrier-seal-off` at 399/1024 (a real negative — removing it cost
   us), yet **attainment swung from 0% to 25.6% across six versions with nobody
   measuring it.** A plank we believe in and do not instrument is the cheapest
   possible regression.
   **GREP: no bot change ⇒ no hot-turn rider.**

#### CANDIDATE C — **OPENDENY**: barrier their modal first-harvester ore tile — **HELD, not admitted**

1. **CHANGE.** Deny the ore tile the opponent's first harvester lands on.
   **GREP: NOT in the incumbent** (confirmed §6.1) — this is the one genuinely
   new road in the study.
2. **MECHANISM METRIC.** Round of the opponent's first harvester (BC median 5,
   p90 14) and their harvester count at r50.
3. **FIXTURE.** Unrated legs on a pinned opponent; per-game metric, no win-rate
   power needed.
4. **WHY NOT NOW.** ⛔ **The evidence is per-(map, seat) and we cannot choose the
   map on the ladder.** The 95.4% determinism reading is a *scouting* asset;
   turning it into a plank needs a map-free trigger (e.g. "the nearest empty ore
   tile to the enemy core at r3") that this study has not measured. **Held as a
   note. Do not admit until the generalised trigger is specified and its base
   rate measured.**

#### NOT CANDIDATES — killed by the GREP or by the data, retained so nobody re-derives them

* **RINGCAP (barrier the enemy core's 8 faces).** We already ship it
  (`LOKI_BARRIER_SEAL_ON`), we target it harder than they do (75.4% vs 55.5% of
  barriers), earlier (r12 vs r35), and v177 already out-attains them (25.6% vs
  22.3%). **Not a gap.**
* **CPU / timeout denial against Bean counters.** 3 TLEs in 1,825,401 unit-turns
  (§3.7). Dead.
* **"Kill their four builders."** They lose 0.42 builders/game and replace 91%
  in a median 2 rounds (§3.8). Dead.
* **Border crash-induction against Bean counters specifically.** 1 death in 95
  border exiles, against a 2.2% field baseline (§3.9). Not demonstrated, not
  excluded, n too small to be either.

---

## 7. LEDGER ROWS

Drafted for `docs/research/move-mining-ledger.tsv` (format read from that file:
`date  opp  oppver  games_covered  doc`). **Not written by this study.**

```
2026-08-21	Bean counters	47	1235	docs/research/REPLAY-STUDY-beancounters-v47v68-2026-08-21.md
2026-08-21	Bean counters	68	90	docs/research/REPLAY-STUDY-beancounters-v47v68-2026-08-21.md
2026-08-21	Bean counters	64	60	docs/research/REPLAY-STUDY-beancounters-v47v68-2026-08-21.md
```

⚠ **v68 coverage is 90 archived games out of 145 rated + 75 unrated played so
far, and they are seven hours old. The trigger should be allowed to re-fire on
v68 once the archive passes ~200 games** — this row does not close that ground.

---

## 8. CAVEATS, KEPT INTACT

1. **The archived pool is 90% unrated** (v47: 1,115/1,235). Unrated pools
   PROTOTYPES on the challenger side, so every "field" share here overstates
   Bean counters relative to their rated record (69.4% archived vs **51.2%
   rated**, n=1,570). The rated cells are the ones to quote.
2. **Clustering.** Games cluster in matches (5/match) and in opponents. Every
   printed half-width applies the CLAUDE.md DEFF (1.529 rated / 1.833 unrated);
   raw shares quoted without a ± are point estimates only.
3. **Direction of the DEFF correction.** The two refutations in this report
   (§3.4 spawn denial, §3.9 border crash) are **fail-to-exclude** claims. Per
   CLAUDE.md they are stated as such and are NOT dressed up as exclusions: the
   spawn-denial refutation rests on a timing argument (seal at r35 vs spawns at
   r0–5), not on a widened interval, and the border-crash refutation explicitly
   says n=162 cannot exclude the effect.
4. **`meta_join` covers the ARCHIVED subset** — 2,790 of their ~10,580 played
   games league-wide. Used here for attribution and for unrated games, never as
   a rated win-rate denominator.
5. **v68 is seven hours old.** 90 archived games, 145 rated games, 30 rated
   matches. Every v68 cell is small-n and several (sentinel latency n=44, v68
   determinism at 4.6 games/cell) are direction-only.
6. **Opponent quality is not matched across versions.** The +33.6pp rated
   game-share jump compares 314 matches spanning their climb against 30 matches
   at rank 1.
7. **Turret-removal matching is positional** (kind + tile + later round), not by
   entity id, because `corpus/events.tsv` carries no ids. Rebuilds on the same
   tile can blur a pairing; the effect is symmetric across the BC and control
   columns.
8. **Claims about OUR tree are confined to §6.1 and are gated on a file:line
   read** of `bots/_v542wave/{main,doctrine,eco,raid,siege}.py` performed for
   this study. **Claims about OUR measured behaviour** (§1, §5, §6.2) come from
   1,115 archived games on v168–v177 decoded here, not from any prior document.
   ⚠ **The US-vs-BC comparison faces different opponent pools** — quote each
   fixture's INTERNAL ratio (BC 79.7 vs their field 33.5; US 42.8 vs our field
   43.3), not the 36.9pp raw difference.
9. **The `titanium_collected` / connectivity plank is OFF-CURRENCY for us.**
   Per `R1000_IS_DEFEAT`, denying their economy scores nothing by itself; it is
   admissible only as *"opens the lane"*. §3.4's dose curve is a fact about the
   engine and about them, not a currency argument for us.
10. **Nothing was fired.** No matches, no submissions, no commits, no edits to
   QUEUE.md / bots/ / tools/ / the ledger. Probe scripts are in `scratchpad/`
   under the `s53_bean_*` prefix.

---

## 9. INCIDENTAL, AND IT IS URGENT — the ladder pairing cadence changed today

**Found while reading Bean counters' match timeline; it is not about them.**
CLAUDE.md's firing-window rule states *"55 of 60 consecutive pairings land at
minute ≡ 12 (mod 20) and 49 of 60 at second `:59`"*, and prices a post-pairing
submit window at *"~16 minutes of clear air"*. **That arithmetic is stale as of
today.**

**MEASURED**, all league pairings in `corpus/league_matches.tsv` (65,895 rows,
all teams), 27 distinct pairing timestamps since 2026-08-21T08:00Z:

* Inter-pairing gaps run `1199, 1200, 1199, 1199, 1200, …` up to
  **2026-08-21T11:51:10Z**, then `1090`, then **`600, 599, 600, 599, …` for
  every gap since**.
* **The cadence halved: 20 minutes → 10 minutes, first 600 s gap ending at
  `2026-08-21T12:01:10Z`.**
* **The offset moved too:** since 11:45Z, **16 of 16** pairings land at minute
  ≡ **1 (mod 10)** and second **`:10`** — i.e. slots at `:x1:10`, not `:x2:59`.

⇒ **The clear-air window after an observed pairing is now at most ~10 minutes,
not ~16, and the old offset will miss.** This is precisely the failure the
CLAUDE.md clause *"the offset has shifted at least once inside an 18-hour span,
so re-derive it from recent rows and never hardcode it"* was written to catch.
**Any submit→fire→rollback planned against the old numbers should be re-timed
before it is executed.** Population caveat: this is the whole league's pairing
tape, not us-only, which makes it stronger than the original us-only reading.
