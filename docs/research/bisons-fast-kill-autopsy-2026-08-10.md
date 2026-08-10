# The Bisons' fast kill — replay autopsy

**Object:** unrated match `28537dae-da31-45b5-9ce5-5282b18e583c`, OpenSverige (v102
"Loki-8", team A in all 5 games) **1–4** The Bisons (team B, rank 25, rating 1626,
653 matches played, **bot version 4**). Every game ended `core_destroyed`.
Turns: g1 saga 74 (L), g2 snowflake 66 (L), g3 moonrise 99 (**W**), g4 heart 92 (L),
g5 jackpot 49 (L).

**Written** 2026-08-10T04:15:12Z (`date -u`), repo at `27d4fc2`.

**Instruments:** `tools/replay_census.py` (existing decoder) plus a new
`tools/corpus/replay_autopsy.py` — a build timeline and a **self-checking core
damage ledger**. It attributes every hit on a core to a source (FireTurret by
shooter kind / BuilderAttack) and asserts the attributed total equals the summed
negative `UpdateHp` deltas on that core id. See "Instrument validation" at the
end: the guard has been observed producing both verdicts.

---

## 1. The mechanism, in one paragraph

The Bisons ignore builder-bot melee entirely and kill the core with **sentinels
parked on a cardinal line at maximum standoff range**. A sentinel's line shot has
range r²=32 and **ignores obstacles**, so a sentinel sitting exactly 5 tiles due
N/S/E/W of a core footprint tile (5²=25 ≤ 32; 6²=36 > 32) shoots the core through
every wall, barrier and building in between, and **cannot be blocked by anything
except killing the sentinel**. Each sentinel is 18 damage every 2 rounds = 9 HP per
round. They walk all four of their builder bots into our half, plant 2–4 of these,
convert essentially their entire titanium bank into ammunition, and fire every
single shot into the core.

---

## 2. Core damage ledger — what actually removed 500 HP

Attribution is `FireTurret` events whose `to` lands on a core footprint tile,
resolved to the shooter standing on `from`, plus `BuilderAttack` events targeting
the footprint. Cross-checked against summed negative `UpdateHp` on the core id.

| game | our core: total dmg | source | our heals into core | net | died |
|---|---|---|---|---|---|
| g1 saga | 738 | **100% sentinel** (41 shots landed) | +232 (58 heal events) | −6 | r73 |
| g2 snowflake | 846 | **100% sentinel** (47) | +344 (86) | −2 | r65 |
| g3 moonrise | 558 | **100% sentinel** (31) | +540 (184) | **482 survived** | — |
| g4 heart | 900 | **100% sentinel** (50) | +400 (100) | 0 | r91 |
| g5 jackpot | 504 | **100% sentinel** (28) | +0 (0) | −4 | r48 |

**Damage from builder-bot attacks: ZERO, both teams, all five games.** The
`BuilderAttack` event count is `A=0 B=0` in every game. Nobody used the 2 Ti → 2 dmg
melee. **Gunner damage: zero.** The Bisons built exactly one gunner across the
five games (g3 r7, on their own core footprint — defensive) and it never hit our core.

### g5, the 49-turn kill, arithmetic

- r29 sentinel @(6,1), r31 @(1,5), r31 @(0,3). Our core is at (0,0), footprint
  {(0,0),(1,0),(0,1),(1,1)}.
- First damage r30 (one sentinel, 18). From r32: **54 damage every 2 rounds** —
  three sentinels × 18, all firing on the same even-round cadence.
- r32,34,36,38,40,42,44,46,48 = 9 volleys × 54 = 486, plus the r30 opener 18 = **504**.
- 500 HP core, no healing from us → dead on r48. Attributed 504 = measured 504. **MATCH.**

Per-round DPS: **1 sentinel = 9 HP/round, 3 sentinels = 27 HP/round.** 500 / 27 = 18.5
rounds. That is the whole kill.

---

## 3. Standoff geometry — the part worth stealing

Every sentinel they built, in every game, measured as minimum d² to the *target*
core's 2×2 footprint:

| game | pos | built | facing | min d² to core | Chebyshev | cardinally aligned |
|---|---|---|---|---|---|---|
| g1 | (5,10) | r37 | N | 25 | 5 | yes |
| g1 | (4,10) | r42 | N | 25 | 5 | yes |
| g1 | (9,5) | r58 | W | 16 | 4 | yes |
| g2 | (11,6) | r31 | W | 25 | 5 | yes |
| g2 | (6,11) | r44 | N | 25 | 5 | yes |
| g2 | (11,5) | r44 | W | 25 | 5 | yes |
| g2 | (6,10) | r46 | N | 16 | 4 | yes |
| g3 | (10,4) | r32 | W | 16 | 4 | yes |
| g4 | (12,9) | r36 | W | 16 | 4 | yes |
| g4 | (13,9) | r47 | W | 25 | 5 | yes |
| g5 | (6,1) | r29 | W | 25 | 5 | yes |
| g5 | (1,5) | r31 | N | 16 | 4 | yes |
| g5 | (0,3) | r31 | N | 4 | 2 | yes |

**13/13 cardinally aligned with a footprint tile. Facing always cardinal, always
correct on the build — they never need a rotate (and sentinels can't rotate anyway).
Chebyshev distance is only ever 5, 4 or 2 — never 1, never 3, never diagonal.**
The modal placement is Chebyshev **5**, which is the maximum distance at which a
cardinal line shot is still in range.

Contrast with **our** four sentinels across the same five games: (21,18) Chebyshev 1
diagonal-facing, (12,3) Chebyshev 2, (17,9) Chebyshev 2, (11,11) Chebyshev 3
diagonal-facing. **We hug the enemy core; they stand off at the range cap.** Ours are
inside reach of any defending builder; theirs are 5 tiles away.

> ### ⚠ AMENDMENT (research lead, 2026-08-10, same day) — **THE SENTENCE ABOVE ABOUT
> *OUR* PLACEMENT IS WITHDRAWN. IT RESTS ON n=4 AND THREE INDEPENDENT SOURCES CONTRADICT IT.**
>
> **The defect is an asymmetry in n between the two arms of one comparison.** This
> section reports **13** of their sentinels and generalises **our** placement from
> **4** — then draws a two-sided conclusion ("we hug, they stand off") as though both
> arms were equally supported. The subject and basis are NOT at fault: both arms
> measure minimum d² to the **target** core's 2×2 footprint, which is the correct
> quantity and the correct basis (this document never inherited the anchor-tile bias
> found in `d2_own`/`d2_enemy`).
>
> **What contradicts it, by three separate routes:**
> 1. **n=198 of our own plants** (side lane league cut, nearest-tile basis) puts us at
>    **d²=25 = Chebyshev 5** — at the standoff distance, not hugging.
> 2. **The source explains why**: `_try_forward_sentinel` (`raid.py:425-445`) accepts
>    ANY site with `bp.distance_squared(target) <= 32` and **returns on the first
>    hit**, while the approach gate already admits the builder at d²≤50. **The code
>    plants at the outermost legal tile by construction.** See
>    `plant-distance-from-source-2026-08-10.md`.
> 3. **The boundary arithmetic agrees**: sentinel range is r²=32, and a
>    first-legal-site rule lands on its edge.
>
> **So the Chebyshev 1-3 cluster here is the TAIL — what happens when a builder is
> already deep before a legal site appears — not our mode.** The four points are real;
> the generalisation from them is not.
>
> **CONSEQUENCE, and it is why this amendment is urgent rather than tidy:** the builder
> retired the "plant closer" plank citing this comparison (*"we were already planting
> closer than they do"*). **That retirement is sourced from four sentinels and should be
> reopened.** Not "suspended pending subject resolution" — the subject IS resolved; the
> sample size is the problem.
>
> **Everything else in this section stands and is unaffected**, because it is the arm
> with n=13: 13/13 cardinally aligned with a footprint tile, correct facing on the
> build, never a rotate, Chebyshev only ever 5/4/2 and never diagonal.

---

## 4. Build timelines, first 50 rounds

**Their opening is identical on all five maps** (16×16 to 28×20):

- **r0, r1, r2, r3: four builder bots. Exactly four, never a fifth, in all 5 games.**
- r4–r15: a short conveyor line out of the core plus 2–4 harvesters.
- Economy build-out stops between r10 (g5, 16×16) and r37 (g1, 24×24).
- **r29–r47: sentinels**, 1–4 of them, placed as in §3. First sentinel round by game:
  g5 r29, g2 r31, g3 r32, g4 r36, g1 r37.

g5 (jackpot, 16×16) in full, B side — 14 builds for the whole game:
```
r0 builder_bot@13,13   r1 builder_bot@14,13   r1 conveyor@14,13   r2 builder_bot@15,13
r3 builder_bot@14,13   r3 conveyor@14,12      r4 conveyor@13,15   r5 harvester@14,11
r6 conveyor@12,15      r8 conveyor@11,15      r10 harvester@10,15
r29 sentinel@6,1       r31 sentinel@1,5       r31 sentinel@0,3
```

g2 (snowflake, 26×26), B side, r0–50: 4 builders (r0–3), 11 conveyors (r1–21),
4 harvesters (r7,12,13,14), then sentinels r31 / r44 / r44 / r46.

**Ours, same games:** 6 builder bots (5 at r0–r4, the 6th at r5–r10), a launcher at
r5–r10, and then 19–28 conveyors and 2–6 harvesters laid continuously to r40–r69.
Our first sentinel: g5 r20, g3 r43, g2 r52, g4 r68 — and only **one per game**
(g1: none at all).

Builder-bot counts: **us 6 every game, them 4 every game.**

---

## 5. Where the titanium went — the real difference

All four of their builders walk into our half and get within d² ≤ 16 of our core
(closest approach per bot, g5: 5, 13, 36, 1). Two or three of ours do the same. So
it is not a movement or map-control difference. It is a **budget** difference.

Titanium converted to ammunition (`CoreConvertAmmo`, field 14):

Their ammo ledger closes exactly: (converted − ammo left) / 10 = shots fired, and
almost every shot is aimed at our core footprint.

| game | we converted | they converted | ammo left | ⇒ shots fired | shots aimed at our core | elsewhere |
|---|---|---|---|---|---|---|
| g1 | 24 | **448** | 28 | 42 | 42 (41 landed, 1 post-mortem) | **0** |
| g2 | 120 | **506** | 16 | 49 | 48 (47 landed, 1 post-mortem) | 1 |
| g3 | 317 | 510 | 0 | 51 | 31 | 20 (our barriers — 5 died) |
| g4 | 168 | **544** | 44 | 50 | 50 | **0** |
| g5 | 96 | **288** | 8 | 28 | 28 | **0** |

In the three games where we put nothing in their way, **every single shot they fired
all game went into our core.** g5: converted 288, fired 28, finished on 8.

Cost-scale model (additive, per `CLAUDE.md`), replayed from the build stream:

| | g5 us | g5 them | g2 us | g2 them |
|---|---|---|---|---|
| scale at first sentinel | 249% (r20) | **195%** (r29) | 280% (r52) | **211%** (r31) |
| that sentinel cost | 74 Ti | **58 Ti** | 84 Ti | **63 Ti** |
| total spent on builds | ~725 | ~446 | ~812 | ~656 |
| spent on offence (sentinels + ammo) | 170 (≈21%) | **480 (≈65%)** | 204 (≈22%) | **794 (≈68%)** |

Our 6th builder bot and our 24-conveyor road network are what price us out: every
builder bot is +20% and every conveyor +1% on the **one global additive scale**, so
by the time we buy a sentinel it costs 27% more than theirs did.

And the road network buys nothing: **g5 — we collected 210 Ti with 3 harvesters and
24 conveyors; they collected 200 Ti with 2 harvesters and 5 conveyors.** Titanium
collected across the five games, us vs them: 260/440, 440/520, 450/210, 320/510,
210/200. They are not skipping economy — they run a *smaller, cheaper* economy that
delivers about the same, and spend the difference on ammunition.

---

## 6. What our bot was doing

- **6 builders, spawned r0–r10.** Two or three walk to their core and reach
  adjacency (d²=1) — g5 bots #3 and #16 both ended orthogonally adjacent to the
  Bisons' core — and then **never attack it** (0 `BuilderAttack` events, all games).
- **24–28 conveyors and a long harvester chain**, still being extended at r48 in the
  game we lost on r48 (g5's last build is `r48 conveyor@2,4`, one round before the
  core died).
- **One launcher per game, built r5–r10, used almost entirely to throw ENEMY
  builders backwards.** Throw census across all 5 games: **34 throws, all by us,
  zero by them** (they build no launchers). **31 of 34 were exile throws of enemy
  bots; only 3 inserted our own builder forward** (g2 r8 and r29, g5 r7). In g1 our
  launcher threw the same enemy builder from (2,2) to (2,0) twelve times, every 2
  rounds from r51 to r73, while three out-of-reach sentinels killed our core.
- **Healing.** We healed the core 58–184 times per game (+232 to +540 HP); they
  healed zero times, ever.

### The one game we won (g3, moonrise 21×8) tells you the threshold

They got **one** sentinel up (r32). It did 558 damage over 66 rounds — 9 HP/round.
We healed +540 back in and finished on 482/500 HP, while our own sentinel (r43,
Chebyshev 2) killed theirs on r98. Against **2** sentinels (g4, 18 HP/round) our
+400 of healing was not enough and we died on r91. Against **3–4** we die in 19–35
rounds.

That gives a clean exchange rate: healing is 1 Ti → 4 HP; a sentinel shot is 10
ammo (= 10 Ti) → 18 HP. So the attacker pays 0.56 Ti per HP removed and the
defender 0.25 Ti per HP restored: **healing is 2.2× more titanium-efficient than
sentinel fire — but it is rate-limited to +4 HP per builder per turn**, so beating N
sentinels needs ⌈9N/4⌉ builders healing the core every single round: 3 for one
sentinel, 5 for two, 7 for three. That is why 3 sentinels is their number.

---

## 7. Is it a map artifact or a method? (league-wide)

**Corpus check:** `corpus/league_games.tsv` covers only 6 top-of-ladder teams and
contains **no** Bisons games. `corpus/ladder_games.tsv` contains **80 game-rows vs
The Bisons, but those are OUR OWN games** (us-only sample, 16 matches, 2026-08-05 to
2026-08-10). So the corpus cannot answer the league-wide question; it was pulled
fresh from the API instead.

**Fresh pull** (`fcode match list --team f670dfed… --json` + `match info --json`):
their **100 most recent matches = 500 games**, dated 2026-08-09 to 2026-08-10.
Their record over that sample: **272–228 (54.4%)**.

- When they win: **268 core_destroyed, 4 titanium_collected**. They basically only
  win by killing the core.
- Turns to kill, over their 268 core kills: **min 38, p25 57, median 70, p75 91,
  max 651**.
- **80.6% of their kills land under 100 turns** (216/268); 64.6% under 80; 26.9%
  under 60.
- Median kill turns by map: jackpot 51 (n=21), atoll 56, lighthouse 61, drumlin 66,
  moonrise 66, nordkap 66, antler 67, snowflake 68 (n=12), hive 70, archipelago 71,
  meander 77, saga 77, fjordgate 86, heart 93. **Only eider is slow (170, n=4).**

**Verdict: repeatable method, not a map artifact and not aimed at us.** The 49-turn
jackpot kill is at their fast tail, but their 66-turn kill on 26×26 snowflake is
their *median* for that map. Fast kills by opponent in the sample include Hugging
Farce 23/35, Atlas 16/25, "opensverige - plan B" 15/30, Kings College Munich 14/25,
the one piece 13/15 — and OpenSverige 12/20. We are not singled out.

**They are a glass cannon, though**: they also *lose* their own core 221 times in the
sample, median r82, 135 of those under 100 rounds. 54.4% and rank 25 is what this
method is worth as-is.

**Our own head-to-head history is worth flagging** (us-only, `corpus/ladder_games.tsv`,
80 games, 16 matches): we are **44–36** vs The Bisons overall, but **by our bot
version: v80 11–4, v87 4–1, v91 4–1, v92 8–2, and v102 (current, Loki-8) 5–10.**
Whatever v102 changed, it changed the matchup against them from winning to losing.
Small n per version; treat as a flag, not a verdict.

---

## 8. Instrument validation

Per the standing rule that a check which has never produced the other verdict has
not been seen to check:

1. The ledger's first run (attributed vs *net* `UpdateHp`) reported **MISMATCH on 4
   of 5 games**, because net delta silently nets our healing against their damage.
   Splitting positive and negative deltas moved 8 of 10 core-sides to **MATCH**. The
   guard demonstrably fires.
2. The two remaining sides are off by exactly **+18** (g1, g2) — one sentinel shot.
   Traced to the raw byte stream of the final turn: in g1 turn 73 the events are
   `fire (4,10)→(4,5)`, `hp id=1 delta=−18`, `remove id=1`, **then a second
   `fire (9,5)→(5,5)`** at a footprint tile whose core no longer exists. Post-mortem
   overkill, benign, and it explains the residual exactly.
3. Independent cross-check on the same replays via `tools/replay_census.py`: one
   delivered stack = 10 Ti and `core_deliv × 10 == titaniumCollected` holds on all
   ten team-sides (e.g. g5: A 21 deliveries / 210 collected, B 20 / 200).
4. The ammo ledger closes independently of the HP ledger: g5 B converted 288, fired
   28 attributed shots × 10 = 280, ended on 8. 288 − 280 = 8. ✔

**Not established:** *why* the Bisons pick the specific tile they pick (we measure
Chebyshev 5/4/2 on a cardinal line, but we do not know their selection rule or
tie-break); whether their 4-builder cap is a constant or a resource rule; and
whether their sentinel count adapts to the defender (we only see 1–4 with n=5).
Team-version data is absent from `match info` (`teamAVersion: null`), so "bot
version 4" comes from the `match list` payload only.

---

## 9. What to build against it

Ordered by directness, not by confidence.

1. **Copy the standoff ring.** Our sentinels sit at Chebyshev 1–3 and half of them
   face diagonally. Theirs sit at Chebyshev 5 on a cardinal line, out of reach, with
   the shot passing through anything. This is a placement rule, not a strategy
   rewrite — pick the tile 5 steps due N/S/E/W of a core footprint tile, facing back
   along that line.
2. **Buy the second and third sentinel.** One sentinel (9 HP/round) is beatable by
   3 healing builders; three (27 HP/round) needs 7. We have built exactly one per
   game. The kill clock is 500/(9N) rounds — N=1 is 56 rounds, N=3 is 19.
3. **Convert the bank to ammo.** They put ~65–68% of all titanium into sentinels +
   ammunition; we put ~21%. A sentinel with no ammo is a 60-Ti ornament.
4. **Stop paying for the road.** 24 conveyors for the same 200 Ti that their 5
   conveyors delivered, plus +24% on the global cost scale that then inflates every
   sentinel we buy.
5. **Cap builder bots at 4.** Bots 5 and 6 cost ~80 Ti *and* +40% permanent scale.
6. **The launcher exile loop is a sink.** 31 of 34 throws just shuffled a harmless
   enemy builder while the actual threat sat 5 tiles from our core. Retarget or drop.
7. **Defensively:** the counter that already worked (g3) is healing, but only up to
   2 sentinels. Above that the only answer is reaching the sentinel — which at
   Chebyshev 5 costs a builder ~5 moves and 15 attack turns (30 HP / 2 dmg), i.e.
   ~20 rounds per sentinel with 30 Ti of attack cost. Killing the sentinel is not
   competitive with killing their core first.
