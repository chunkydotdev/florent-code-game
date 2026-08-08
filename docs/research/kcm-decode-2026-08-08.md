# Kings College Munich — seat asymmetry, the v1→v8 inversion, and our own aim gap

Research arm, 2026-08-08 s19. Archive-only, 14 matches / 70 games vs us plus
30 control games (6 other opponents), **zero downloads**. Live version at write
time: v84.

## Two corrections to my own commissioning brief, up front

1. **KCM was NOT undecoded.** `kings-college-classification-2026-08-07.md`,
   `kcm-win-c1-validation-2026-08-07.md` and
   `kcm-wild-establishment-rates-2026-08-07.md` (sessions 13/14) already cover
   the v1/v7 era, and every claim in them reproduced independently. I briefed
   the agent that this was "the largest blank space on the board" and that was
   wrong — I checked the bleed table but not `docs/research/`. What was
   genuinely new: the 40 games added since, the **entire v8 era**, and the seat
   question.
2. **"17.9% of bleed" is denominator-dependent and I quoted only one.** Both
   are now measured: KCM is **17.9% of the sum of net-negative opponent totals
   (−493.3)** and **13.3% of gross match-level bleed (−667.0)**. The second is
   the better measure of "Elo we lose", because the first silently excludes
   losses to opponents we net-beat. Same correction applies to every share in
   `v5-instrument-coverage`: Lunds 27.5%→**20.3%**, Ouroboros 25.0%→**18.5%**,
   CAD 11.6%→**8.6%**. The ORDERING and the concentration conclusion are
   unchanged; the percentages are not.

## 1. Their script is the most reproducible in the archive

Byte-stable across 100 games, 7 opponents, 3 versions:
- `convert_ammo(8)` at r0/r1/r2 in **77/100**; small-map branch `48` at r0 in 10.
- **Launcher built r1, destroyed BY ITS OWN TEAM at r6 — 85/85 launcher games,
  zero exceptions, both seats, all versions.** Tile is a deterministic function
  of (map, core position).
- 196 own-builder throws at r2–r6, **73% at max range** (d²≥25 of a 26 max).
- **Zero splitters in 100/100.** First harvester r7 (v1) / r3 (v8).

What kills our core (7,692 damage events, exact ledger): **sentinel 71.5% of
damage at median d²=25** (modal 25, not the d²=32 the prior doc emphasised),
gunner 28.4% at median d²=2. Median siege 195 rounds, **1,406 raw damage into a
500 HP core** — our healing absorbs ~64% and still loses.

## 2. The seat split is real, and smaller than the map effect

Our wins: seat A 15/35 (42.9%) vs seat B 6/35 (17.1%), Fisher **p=0.036**;
v1-only p=0.045; our-version-matched p=0.097 (n=35). Map-mix adjustment
*strengthens* it (mix slightly favoured B).

**But the map effect dominates:** we win 14/18 on atoll/fjordgate/meander/
lighthouse and **0/19 on saga, snowflake, drumlin, archipelago** — in both
seats, across versions. That is a bigger and completely separate problem.

Strictest test (same map, our-version, KCM-version, both seats) yields 7 cells
/ 14 games: 5 ties, **2 discordant, both favouring seat A** — p=0.25 one-sided.
Consistent with the pooled result, **not confirmation of it**.

## 3. The mechanism is OURS, on offence

**Theirs is seat-symmetric to measurement precision:** launcher r1→r6 in 29/29
seat-A and 27/27 seat-B; **sentinel placement lands on a legal firing ray onto
an enemy core footprint tile in 64/64 and 66/67** — exact and
orientation-independent. Their only measured asymmetry is turn order: first
forward turret at **r6 moving first vs r10 moving second** (control cohort,
opponent-independent).

**Ours is not.** For our turrets built within d²≤36 of their core, does the
build tile + facing put an enemy core tile on the ray?

| | n | aimed on a core ray |
|---|--:|--:|
| our seat A | 78 | **71 (91%)** |
| our seat B | 58 | **44 (76%)** |

Fisher **p=0.029**. Aimed turrets land median 5 shots on their core; misaimed
ones median 0. The corpus's best single predictor — "did one of our forward
turrets land ≥10 shots on their core" — splits 21/70 yes (14 wins) vs 49/70 no
(7 wins), **and its seat split is 15/35 vs 6/35, the same shape as the win
split.** Version-matched, the gap lives entirely in the kill column: seat A
kills their core 5/15, seat B 2/20; tiebreak wins are 4 and 4.

**Caveats the agent refused to paper over:** the aim gap is **version-lumpy**
(v72 A 11/11 vs B 3/10; v68 shows no gap; v80 A 10/12 vs B 6/8), so it may be
several per-version bugs rather than one property. And the obvious
`get_attackable_tiles()` row-major hypothesis was **tested and rejected** —
over 491 multi-target sentinel shots the priority ladder dominates enumeration
order, with no seat differential.

**Also found: at least six hard-coded (map, seat) branches in our live source**
(`_v97e11`): `snowflake_home_b` L2455, `nordkap_home_a` L2459,
`snowflake_attack_now` L2957, `snowflake_home_b`/`hive_home_a` L3133/3138,
`chase_battery` L5339, and `healer_focus` L6682 — the last **changes the turret
target-priority ladder on one seat only**. None ablated (out of research scope).

## 4. v1 → v8 is a strategic inversion

**Confound stated first: all 20 v8 games are against our v79/v80/v82 and there
is no v8 control game.** Only the r0–r3 opening constants are safe.

| | v1 (70g) | v8 (20g) |
|---|--:|--:|
| launcher built | 66/70 | **9/20** |
| first harvester | r7 | **r3** |
| first turret d² to defender core | 9 | **77** |
| our core first damage | r26 | **r88** |
| deliveries | 201 | **378** |

**v1 opens with a forward battery; v8 opens with economy and turtles.** v8 is
better for us head-to-head (9/20 vs 12/50) — but the economic build is what
beats us on the maps we never win.

## 5. Probe feasibility: the best target we have

Reproducible constants are listed in §1 and §5 of the agent's report: the ammo
ladder, launcher r1→r6, max-range throws, zero splitters, the v1 forward-gunner
opening vs the v8 turtle, and a counter-gunner reflex (a turret within d²≤13 of
our forward turret, median 6 rounds later, 126/143).

**Two things a probe must NOT derive:** the launcher tile does **not** follow
from mirroring (on rot180 maps the offset transposes rather than negates — hive
(2,20)→(5,19) is (+3,−1) while (21,3)→(20,6) is (−1,+3)); and the v8
launcher-on/off decision is **not** a pure map key (meander splits within
map+seat+version). Both must be tabled from measurement, not computed.

## What remains undetermined

**Why we lose 19/19 on saga, snowflake, drumlin and archipelago in both seats.**
Not seat, not version, untouched by this decode — and larger than everything
above. Also: whether the seat effect is one mechanism or several; anything
about v8 not confounded with our own v79+; and which of our six hard-coded
(map, seat) gates is net-positive.
