# REPLAY STUDY: `not adgato` v23 — 80 decoded modern games (2026-08-20, research arm)

PROVENANCE: opus move-mining subagent, commissioned by the research arm after
`tools/move_miner.py` scored `not adgato` v23 the top unstudied candidate
(76.1). Method: `docs/research/PLAYBOOK-move-mining-2026-08-16.md`. No prior
`not adgato` study exists in `docs/research/move-mining-ledger.tsv` — this is
the first, so the exclusion baseline is empty.

INPUTS (all snapshotted into a private scratchpad before reading, per the
keeper-rewrites-in-place rule; row counts verified twice and md5-pinned):
`corpus/ladder_games.tsv` (6,856 rows), `corpus/join.tsv` (5,544),
`corpus/{events,builds,econ,flow,build_agg}.tsv` subsets, and a fresh
event-level decode of all 90 `replay_archive/*.replay26` files built on
`tools/replay_census.py` primitives (`fields`/`read_pos`/`parse_entity`) in the
shape of `tools/corpus/replay_autopsy.py`. **No platform matches were fired and
no replays were downloaded — all 90 were already in `replay_archive/`.**

GROUND: 90 rated ladder games vs `not adgato`, **every one of them against
oppver 23** (their only version in our record), across 18 matches
2026-08-16T02:12Z → 2026-08-20T03:52Z. **The study population is the 80 MODERN
games** (ourver ≥ 159; the 10 ourver-152 games of 08-16 are outside the 3-day
window and are quoted only where labelled). Our modern share **38/80 = 47.5%
(95% CI [34.0, 61.0] with the rated pooled DEFF 1.529; 16 matches, 5 games
each, so games are clustered on match + opponent-version + 20-min window)**.
Chassis split: **ourver 159 (our line, beltbreak2) 2/5**; **ourver 161-165
(x3r0's line) 36/75 = 48.0%**. Target value at commission: gap +46, a 5-0 pays
+13.87 — a reachable, high-volume, near-coin-flip cell.

⛔ **EVERY CLAIM BELOW IS LABELLED `MEASURED` (counted from decoded events) or
`DIAGNOSTIC` (an association that survives a stated confound check but whose
direction of causation is NOT established).** Nothing here is a causal claim
unless the inference is written inline.

---

## §0 — INSTRUMENT VALIDATION (read this before trusting any number)

The decoder was driven against two independent checks and both closed exactly.

**(a) Agreement with the corpus pipeline, which was written separately.** My
decode of the same 90 files emits **11,217 BUILD rows and 2,253 DEATH rows** —
byte-for-byte the counts in `corpus/events.tsv` for those files (11,217 /
2,253). My TLE count for the 80 modern games is **1,299**, exactly the summed
`tled` column of `corpus/econ.tsv` over the same games.

**(b) The damage ledger closes to the shot classifier with ZERO residual.**
Summed negative `UpdateHp` deltas on each core, split by delta magnitude, vs
the independently-classified fire events:

| channel | ledger HP | shots × dmg | residual |
|---|---|---|---|
| their gunners → our core | 28,574 | 4,082 × 7 = 28,574 | **0** |
| their sentinels → our core | 26,784 | 1,488 × 18 = 26,784 | **0** |
| their builder attacks → our core | 218 | 109 × 2 = 218 | **0** |
| our sentinels → their core | 35,208 | 1,956 × 18 = 35,208 | **0** |
| our gunners → their core | 4,123 | 589 × 7 = 4,123 | **0** |

Six channels, six exact closures. The target classifier is not guessing.

**(c) Both-verdicts control on the load-bearing zero.** The barrier claim in §1
rests on a zero. The same classifier, on the same 80 games, emits **350 turret
shots onto barriers and 567 builder attacks onto barriers — all of them ours**,
and **61 barrier deaths**. A classifier that cannot see a barrier being hit
would show zero on both sides; this one shows zero on exactly one side.

---

## §1 — ⭐ THEY CANNOT REMOVE A BARRIER. AT ALL. (MEASURED, exposure-controlled)

**We built 612 barriers in 80 modern games. Zero of them died. Ever.**
Their 318 barriers, in the same games, died 61 times (19.2%) — to us.

Two separate weapon paths, both empty:
* **Turret fire: 0 of their 9,730 shots landed on a barrier.** (Ours: 350 of
  3,877, i.e. 9.0%.)
* **Builder attacks: 0 of their 6,136 builder attacks targeted one of OUR
  barriers.** They logged 149 builder attacks on a barrier — **all 149 on their
  OWN barriers**, never on ours.

**THE EXPOSURE CONTROL, because "our barriers were simply out of reach" is the
obvious alternative and it is refuted.** I counted the exact precondition for
`attack` — (one of their builder bots) × (orthogonally adjacent OUR building) ×
(round) — over all 80 games:

| our building class | exposed bot-rounds | their attacks | attacks per 1,000 exposed |
|---|---|---|---|
| conveyor | 31,916 | 3,645 | **114.2** |
| harvester | 2,730 | 286 | **104.8** |
| sentinel | 4,588 (all turrets) | 380 | **82.8** |
| **barrier** | **11,156** | **0** | **0.00** |

At the conveyor rate, 11,156 exposed barrier-rounds should have produced
~1,274 attacks. Observed: **0**. Independently, **300 of our 612 barriers were
built within r²≤13 of an already-standing enemy gunner** — inside its attack
radius — and still none died.

**INFERENCE (stated, not assumed):** the exposure control removes reachability
as an explanation, and the zero holds on two independent weapon paths that share
no code path except target selection. The remaining explanation consistent with
all of it is that `not adgato` v23's target ladders — both the builder-attack
ladder and the turret-fire ladder — **do not contain `EntityType.BARRIER`**.
This is inference from behaviour, not a source read; it is falsifiable by a
single observed barrier kill.

⇒ **AGAINST THIS OPPONENT A BARRIER IS A PERMANENT 3-Ti WALL.** Everything in
§2, §3 and §5 is a consequence of this one fact.

ANCHORS: `1a715609-…_game_2` (drumlin, v164, W) 13 barriers built / 0 lost ·
`4740d0d9-…_game_5` (nordkap, v162, W) 13 / 0 · `40456df0-…_game_4` (nordkap,
v164, **L**) 11 / 0 — the zero holds in losses too, so it is not a
winner's artefact.

---

## §2 — ⭐⭐ THEIR KILL PATH IS THE POINT-BLANK RING GUNNER, AND OUR OWN CORE RING IS WIDE OPEN

**MEASURED.** Their core damage on us, by weapon and by firing distance to our
core footprint (80 modern games, 55,576 HP total):

| source | HP | share of all core damage we take |
|---|---|---|
| gunner fired from d²≤2 — **the 12 ring tiles themselves** | 14,777 | **26.6%** |
| gunner from d² 3-4 | 6,286 | 11.3% |
| gunner from d² 5-8 | 6,664 | 12.0% |
| gunner from d² 9-13 | 847 | 1.5% |
| **all gunner** | **28,574** | **51.4%** |
| sentinel (obstacle-immune, 57.5% of it from d²>13) | 26,784 | 48.2% |
| builder attack | 218 | 0.4% |

**They build gunners ON our 12-tile core ring: 88 of them, in 50 of 80 games,
median build round r116** (44 on orthogonal seats, 44 on corners). Their gunner
placement creeps: median d² from our core is **244 for gunners built r0-30**,
then **10 for r30-60 and 13 thereafter** — from r30 onward their gunners are
built at our doorstep, not at home.

**DIAGNOSTIC, with the confound checked.** Our record splits on it:

| | record | 95% CI (DEFF 1.529) | matches |
|---|---|---|---|
| no ring gunner all game | **21/30 = 70.0%** | ±20.3 | 16 |
| first ring gunner by r60 | 8/18 = 44.4% | ±28.4 | 13 |
| first ring gunner r61-120 | 6/16 = 37.5% | ±29.3 | 11 |
| first ring gunner r121+ | 3/16 = 18.8% | ±23.6 | 9 |

**Game-length confound checked and does NOT explain it**: median turns 235 (no
ring gunner) vs 228 (any ring gunner). Restricted to games ≥150 rounds, so both
sides had time: **16/24 = 66.7% vs 11/29 = 37.9%.** ⚠ The intervals overlap at
the margin and **the direction of causation is NOT established** — a bot that
is already losing lets an enemy builder walk to its core. Treat the split as a
diagnostic; the *mechanism* below is what is measured.

**WHAT WE DO ON OUR OWN RING (MEASURED): nothing defensive.** Our buildings
placed on our own 12-tile ring across 80 games: **565 conveyors, 20 launchers,
9 sentinels, 8 gunners — and 0 barriers.** Meanwhile we place **528 barriers on
THEIR ring** (the incumbent's `LOKI_BARRIER_SEAL_ON`,
`bots/_v488beltbreak2/doctrine.py:1227`, and its raid-side implementation at
`bots/_v488beltbreak2/raid.py:294-305`). **The collar doctrine exists, is
correct, and is pointed only outward.**

⇒ **PIECE: A DEFENSIVE BARRIER COLLAR ON OUR OWN CORE RING.** The incumbent's
own doctrine already states the mechanism in the offensive direction —
*"our own barrier collar blocks a gunner ray"*
(`bots/_v488beltbreak2/doctrine.py:1232` and `:1304-1306`) — and a gunner ray is
obstacle-blocked while a sentinel ray is not (game rules, not inference). Against
**this** opponent the collar is additionally **irreversible** (§1). It attacks
the 51.4% gunner channel two ways: it denies the ring build (26.6% of our core
damage) and it blocks the line from d² 3-13 (a further 24.8%). It does nothing
to the sentinel channel (48.2%) — say so in any prereg.

⚠ **DESIGN CONSTRAINT, not optional:** the 8 orthogonal ring seats are the only
tiles a conveyor can deliver into our core from and the only tiles a builder can
heal it from (`bots/_v488beltbreak2/doctrine.py:1215-1221`), and we occupy 483
of them with conveyors. A full 12-tile self-seal would strangle our own economy
and our own core heal (34,559 HP over 80 games). **The cheap version is the 4
CORNERS ONLY: 4 tiles, ~12 Ti, no delivery seat lost, and it denies 44 of their
88 ring gunners and 5,257 HP (9.5% of all core damage we take).** We currently
put only 82 transit conveyors on corners across 80 games — roughly one per game
to reroute.

ANCHORS (all six top ring-gunner games are LOSSES):
`66f7f716-…_game_4` (drakkarfjord, v161, L, r208) — 5 ring gunners at r56/88/136/161/168, **896 HP** from those tiles alone ·
`ef220281-…_game_3` (frostgate, **v159 — our own chassis**, L, r220) — 5 ring gunners at r75/102/180/187/211, **973 HP** ·
`4740d0d9-…_game_2` (frostgate, v162, L) — 4 ring gunners, 497 HP ·
`8709c9d7-…_game_5` (nordkap, v162, L) — 4 ring gunners, 378 HP.

---

## §3 — THE ENEMY-RING SEAL WORKS AND WE STOP TWO TILES SHORT (MEASURED)

Their core ring is **exactly 12 tiles in all 80 games** (median 0 wall tiles,
max 2). Peak simultaneously-blocked ring tiles per game:

`5:1 · 6:1 · 7:5 · 8:9 · 9:19 · 10:21 · 11:16 · 12:8`

**We reach ≥10 of 12 in 45 of 80 games and close all 12 in only 8.** Summed over
80 games we spend **7,634 rounds at ≥10 blocked, 3,813 at ≥11, and just 538 at
12.** At the peak moment the ring is held by **505 of our barriers, 191 of THEIR
OWN conveyors, 46 of our launchers** — their own belt does a third of the work.

**When the seal closes, it holds and it denies spawns: across the 8 fully-sealed
games they issued 1 builder spawn during 538 sealed rounds, against 545 spawns
while unsealed.** (The 1 is a same-round ordering artefact at best.) Median first
seal r55, median 26.5 sealed rounds, our record in those 8 games 5/8.

⚠ The seal→spawn-denial link is an engine rule (`can_spawn` needs an empty
adjacent tile), so it is not a discovery. **The discovery is that the seal is
STABLE against this opponent** — §1 says they can never reopen it — **and that
we leave the last one or two tiles open for 3,813 rounds per 80 games at 3 Ti a
tile.** ⚠ Peak-ring-occupancy correlates with winning (≥7 tiles: 33/52 = 63%;
≤6: 5/28 = 18%) but that association is **heavily reverse-caused** — getting
seven buildings onto their ring means we already own the map. Do not price the
plank off it.

ANCHOR: `4740d0d9-…_game_5` (nordkap, v162, W, r197) — first seal r42, **155
sealed rounds**, 13 barriers built, 0 lost. Counter-anchor:
`40456df0-…_game_4` (nordkap, v164, **L**) — seal at r49, 18 rounds, still lost;
the seal is not sufficient on its own.

---

## §4 — ⛔ ROAD CLOSED: BORDER-KIDNAP CRASH-INDUCTION DOES NOT WORK ON THEM

**MEASURED, with the detector driven to the other verdict.** Our launchers threw
**755 enemy builder bots** across the 80 modern games (9.4/game, 56 of 80 games,
median throw round r182, median Chebyshev distance 4). **343 of those (45.4%)
landed on a map-border tile — the exact LOKI-14 trigger. Zero of the 755 bots
ever stopped executing.** Median additional rounds of execution after being
thrown: **140** (q25 63, q75 262); 603 of 755 ran ≥50 more rounds.

**CONTROL — the detector fires.** The same "last round this unit id appears in
`BotOutput`" instrument flags **123 of their 546 builder bots** as stopping
before game end (their real deaths). It is not a dead instrument reading zero.

⇒ **`not adgato` v23 handles off-map / displaced-state queries.** Border
crash-induction is refuted against them on live rated games (rule 6 satisfied:
80 rated games, not an arena). **Retain this so nobody re-derives it.** The
throw itself still costs them tempo — but as a *kill* mechanism against this
opponent it is dead, and our launchers are the most expensive thing we field
against them (see §6).

---

## §5 — OUR AMMO LEAK: THEY RUN THE 0033 GUNNER PLUG ON US, AND OUR HOLD-FIRE IS NOT BINDING

**MEASURED.** 350 of our 3,877 shots (9.0%, 1,862 ammo, 23 Ti/game) end on one
of their barriers. It is concentrated: 36 barrier tiles ate all 350, **one tile
ate 74 shots** (`65ee15a5-…_game_2`, nordkap, tile (10,8)) and another 29
(`29b26357-…_game_1`, icefloe, (16,5)). They maintain the rocks — **11.3% of
their 8,559 heals go into barriers** (968 heals × 4 HP = 3,872 HP of plug
maintenance).

**Split by our chassis — this is a chassis defect, not a line-wide one:**

| ourver | games | our shots | onto barrier | ammo burnt |
|---|---|---|---|---|
| 159 (ours, beltbreak2) | 5 | 207 | 17 (8.2%) | 80 |
| **161 (x3r0)** | 15 | 698 | **146 (20.9%)** | **584** |
| **162 (x3r0)** | 40 | 1,595 | **168 (10.5%)** | **1,056** |
| 163 | 5 | 186 | 5 (2.7%) | 20 |
| **164** | 10 | 1,011 | **3 (0.3%)** | 12 |
| 165 | 5 | 180 | 11 (6.1%) | 110 |

v164 has effectively solved it (0.3%); v161 has not (20.9%). The incumbent's
`BB_NO_FIRE = frozenset((EntityType.CORE, EntityType.BARRIER))`
(`bots/_v488beltbreak2/raid.py:88`) is the right guard and it is **not binding on
the x3r0 chassis that plays most of these games.** This is a one-line
cross-chassis port, not a new plank.

⇒ Symmetrically: **they never fire at a barrier at all (§1), so our own barriers
cost them zero ammo — the plug is a one-way trade in their favour today.**

---

## §6 — WHAT EACH SIDE IS ACTUALLY BUYING (MEASURED, per game over 80)

| | THEM | US |
|---|---|---|
| gunners built | **6.44** | 0.82 |
| sentinels built | 0.72 | **3.08** |
| launchers built | **0.00** | 4.03 |
| barriers | 3.98 | 7.65 |
| harvesters | 5.45 | 5.50 |
| conveyors | 35.5 | 39.9 |
| titanium → ammo | **644** | 410 |
| shots fired | **121.6** | 48.5 |
| ammo spent | **608** | 385 |
| builder attacks | 76.7 | 84.9 |
| heals | 107.0 | **149.4** |
| median `titanium_collected` at end | 910 | 845 |

Survival, built → died (80 games):

| entity | OURS | THEIRS |
|---|---|---|
| **launcher** | **232/322 = 72.0%** | — (they build none) |
| sentinel | 95/246 = 38.6% | 25/58 = 43.1% |
| gunner | 24/66 = 36.4% | 102/515 = 19.8% |
| builder bot | 192/583 = 32.9% | 123/546 = 22.5% |
| conveyor | 580/3,190 = 18.2% | 530/2,837 = 18.7% |
| harvester | 32/440 = 7.3% | 4/436 = 0.9% |
| **barrier** | **0/612 = 0.0%** | 61/318 = 19.2% |

Two things jump out. **(a) Our launcher line is a 72%-loss asset against a bot
that is immune to the exploit it exists to deliver (§4)**; they shoot our
launchers 346 times and builder-attack them 114 times. **(b) Our builder attacks
go 53.3% into their turrets — 3,343 pecks at gunners = 6,686 damage — while they
put 22.9% of their heals into gunners = 1,960 heals × 4 = 7,840 HP.** Their heal
budget on gunners **exceeds our entire builder-attack output on gunners.** Our
gunner-chew against this opponent is arithmetically net-negative and their
gunners still die at only 19.8%. Their builder attacks by contrast go **64.2%
into our economy** and only 1.8% (109 attacks, 218 HP) into our core — they do
not core-chew, same as 0033.

**Reaction latency (MEASURED):** rounds from one of their gunners dying to their
next gunner build — n=78, median **16**, q25 7, q75 60, only 3/78 within 2
rounds. Control on our own sentinels: median 30. Their rebuild is fast but not
instantaneous; a ~16-round window follows every gunner kill.

---

## §7 — OPENING DETERMINISM: THEIR FIRST HARVESTER AND FIRST BELT ARE 100% SCRIPTED

**MEASURED**, over (map, seat) cells with n≥2 games:

| their first … | same TILE | same ROUND |
|---|---|---|
| harvester | **77/77 (100%)** | 76/77 (99%) |
| conveyor | **77/77 (100%)** | 76/77 (99%) |
| gunner | 57/75 (76%) | 57/75 (76%) |
| sentinel | 22/27 (81%) | 20/27 (74%) |

Median first-build rounds: conveyor r6, harvester r4, gunner **r11** (79 of 80
games), sentinel r40.5. Ours for comparison: conveyor r2, harvester r8, gunner
r30, sentinel r41.

⇒ **Their opening ore tile and first belt tile are fully pre-emptable per (map,
seat).** A 3-Ti barrier on an ore tile makes `can_build_harvester` false
(builder-probed 2026-08-09), and §1 says they can never clear it. Their first
gunner is 76% modal too — `('fjordgate','B')` puts it on **(4,7) at round 1 in
4/4 games**; `('glacierkeep','B')` on **(12,27) in 6/6 games**, round 16 in 5 of
6. ⚠ Pre-empting a tile at r1-r11 requires one of our builders to be adjacent to
it that early, which on most maps it is not — **this piece is a map-conditional
denial, not a universal one**, and the reachability check belongs in the prereg.

---

## §8 — THEY TIME OUT AND WE NEVER DO — BUT THE DRIVER IS NOT IDENTIFIED

**MEASURED.** Their CPU per unit-turn vs ours, 80 modern games:

| | n unit-turns | median | p99 | max | >9,000 µs |
|---|---|---|---|---|---|
| THEM | 221,605 | 676 µs | 7,466 | 11,357 | 1,589 (0.72%) |
| US | 186,671 | 165 µs | 803 | 3,062 | **0 (0.00%)** |

**Their builder bots cost 1,654 µs median — 10× our 165 µs — with a p99 of
10,444 µs, i.e. over budget.** Their gunners are trivial (22 µs), their core 585
µs. **They lost 1,299 turns to CPU timeout; we lost 0.** But it is concentrated:
**8 of 80 games**, median TLE round **r429**, 920 of 1,299 at r300+, and our
record in those 8 games is 7/8.

⛔ **THE OBVIOUS MECHANISM IS REFUTED BY ITS OWN CONTROL.** Board entity count
looked like the driver (0.00% TLE below 80 live entities, 2.62% above 120) —
**but the single largest game in the corpus, 730 rounds with a peak of 247 live
entities, recorded ZERO timeouts**, while a 289-round game peaking at 206
recorded 239. Entity count is not sufficient. Map area is not it either (TLE
games span 400, 625 and 900 tiles). **Do not build a "flood the board to time
them out" plank on this — the mechanism is unidentified.** What is bankable:
their per-turn cost sits an order of magnitude above ours with almost no margin,
so they are one bad map away from losing turns, and it happens after r300 —
**outside our own <r300 doctrine window anyway.**

ANCHORS: `8709c9d7-…_game_2` (drakkarfjord, v162, W, r591) 671 TLEs from r371 ·
`1a715609-…_game_2` (drumlin, v164, W, r289) 239 TLEs from r143 (the earliest
onset) · counter-anchor `4bead7e5-…_game_2` (glacierkeep, r730, peak 247
entities) **0 TLEs**.

---

## §9 — WHAT THE MATCHUP ACTUALLY IS

It is **not a race, it is a blowout distribution**. In **32 of 80 games (40%)
the winner's core is never scratched at all** (17 where we never touch theirs —
0 wins; 15 where they never touch ours — 15 wins). Of the 48 contested games,
we win 23. Kill rounds are near-identical both ways: **we kill at median r222
(q25 154, q75 338); they kill at median r228 (q25 189, q75 287)**. Only **25 of
our 37 core-kill wins land by r300** — twelve of our wins are off-doctrine
grinds. 77 of 80 games end `core_destroyed`; only 3 go to r1000.

First blood on their core comes at median r97; on ours at median r80. **They
reach our core first.** ⚠ Among the 48 games where both cores are hit, we win
6/23 when we scratch first (median first scratch r43) and 17/25 when they do —
**conditioning on "both cores hit" is a collider** (it deletes both blowout
classes), so read that pair as a warning about the statistic, not a finding. The
unconditioned form is flat and unhelpful: 39.1% when we scratch their core by
r60, 55.8% when by r250.

**Map cells worth naming (80 games, so ~5 games a cell — indicative only):**
best antler 4/4, icefloe 5/6, drakkarfjord 5/6, glacierkeep 5/8; worst valkyrie
0/3, auroraveil 1/6, ragnarok 1/6, frostgate 1/5 (and 3 of the 6 top
ring-gunner anchors are frostgate).

**Their sentinel count correlates with our losses (0 sentinels 25/44 = 56.8%;
≥1 13/36 = 36.1%; ≥2 2/16 = 12.5%) — AND THE TIMING CONTROL KILLS THE CAUSAL
READ**: split on "sentinel by r100" instead, it is 45.8% vs 48.2%, i.e. nothing.
Their sentinel is a *consequence* of a game going their way, not a cause.
Retained here so nobody re-derives it as a plank.

---

## §10 — TRANSFERABILITY VERDICTS

| piece | transfers beyond `not adgato` v23? | verdict |
|---|---|---|
| §2 defensive barrier collar (corners first) | **The MECHANISM yes** — gunner rays are obstacle-blocked by engine rule, and the ring is the modal enemy-turret seat league-wide. **The IRREVERSIBILITY no** — 0033 demonstrably attacks and heals barriers. | **BUILD IT, price it against a field that CAN break it** |
| §1 barrier immunity | **Opponent-specific.** A behavioural property of one bot's target ladder. | **Exploit vs them; never assume it elsewhere** |
| §3 close the last ring tile | **Yes** — 3 Ti to convert 3,813 rounds of ≥11-blocked into 12-blocked. Against opponents who break barriers it needs re-seal logic. | **Cheap; check the incumbent's seal loop for a "why did it stop at 11" gap** |
| §5 hold-fire on barriers | **Yes, universal** (0033 measured 34.1% ammo leak; here 9.0%). Already correct in `_v488beltbreak2`; missing from the x3r0 chassis. | **Port, do not re-invent** |
| §4 border kidnap | **Refuted here only.** LOKI-14 measured 314 kidnaps against other teams; this is one immune opponent. | **Do not generalise the refutation either** |
| §7 opening pre-emption | **Method transfers** (100% modal first harvester is a strong regularity); the tiles do not. | **Needs a per-(map,seat) table and a reachability check** |
| §8 CPU denial | **No mechanism** — refuted by its own control. | **Park** |

---

## §11 — FLAGGED FOR THE v525+ BUILD CAMPAIGN

1. **DEFENSIVE CORNER COLLAR (§2).** Highest-value, cheapest, and the doctrine
   text for it already exists in the tree pointed the wrong way
   (`_v488beltbreak2/doctrine.py:1232`). 4 barriers, ~12 Ti, no delivery seat
   lost, aimed at a channel worth 51.4% of the core damage we take. **Pairs with
   the campaign's forward-sentinel line specifically because a sentinel shoots
   THROUGH our own collar while a gunner cannot** — the same asymmetry the
   incumbent already relies on offensively.
2. **BARRIER HOLD-FIRE PORT (§5).** One frozenset; 584 ammo/15 games of leak on
   v161 alone.
3. **RE-PRICE THE LAUNCHER LINE AGAINST THIS OPPONENT (§4, §6).** 4.03
   launchers/game at 72% loss, delivering 755 kidnaps and 0 kills. Against
   `not adgato` specifically the kidnap's only remaining value is displacement
   tempo — which nothing in this study measures. **That is the gap worth a
   prereg: does a kidnap actually delay their next build?**
4. **THE LAST RING TILE (§3).** Instrument first: log why the seal loop stops at
   11 of 12.
5. **DO NOT SPEND A LEG ON:** border crash-induction vs this team (§4), CPU
   flooding (§8), their-sentinel-count as a lever (§9).

---

## §12 — DROPPED AS ALREADY-KNOWN

Enemy-ring barrier seal (`LOKI_BARRIER_SEAL_ON`, shipping) · gunner-plug ammo
leak as a general phenomenon (0033 study, Piece 1) · zero enemy core-chew
(0033 Piece 2, confirmed again here at 1.8%) · forward turret siting · the
r1000 tiebreak tail (3 of 80 games; off-currency).
