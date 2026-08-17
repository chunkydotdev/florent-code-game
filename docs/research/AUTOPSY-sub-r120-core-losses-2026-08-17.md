# AUTOPSY — the ten sub-r120 core losses of 2026-08-17

**Agent:** fresh-context replay-autopsy subagent, commissioned by the builder lane.
**Written:** `2026-08-17T08:08:53Z` (`date -u`, same shell call).
**Repo HEAD at write time:** `d226b851` (`2026-08-17T10:00:20+02:00`).
**Our tree for every game below:** `bots/_v468kladturbo/` (`ourver = 155` in all ten rows).

**Inputs read**
* `corpus/ladder_games.tsv` — the population and the filter.
* `corpus/join.tsv` — replay file → match → `our_team`.
* `replay_archive/*.replay26` — 108 of the 115 rated games of 2026-08-17.
* Four replays not in the archive, pulled read-only with
  `fcode match replay cfb6744a-b275-4407-b0dc-b2273a9c4080 --game {2,3,4,5}`
  (`docs/fcode-cli.md:130` classes `match replay` READ-ONLY) into a scratch dir.
  **One of the ten target games lives only there** (`cfb6744a…_game_3`).
* `tools/replay_schema.md`, `tools/replay_census.py`, `tools/corpus/replay_autopsy.py`
  (primitives reused, not re-written), `docs/research/corpus-howto.md`.
* `bots/_v468kladturbo/{doctrine,main,raid,eco}.py` — read as the SPECIFICATION for
  §4's gate reconstruction, never as a source of measurement.

**The filter, verbatim**
```python
rows = csv.DictReader(open('corpus/ladder_games.tsv'), delimiter='\t')
tgt  = [r for r in rows
        if r['created'].startswith('2026-08-17')
        and r['won'] == '0' and r['cond'] == 'core_destroyed'
        and int(r['turns']) <= 120]
# -> 10 rows, exactly the ten in the brief
```
**Population decoded:** all 115 rated games of 2026-08-17; **112 decoded**, 3 not
archived and not needed (`833df6a0…_game_{3,4,5}` vs HTTP 418, all wins).
Control = the **102 decoded non-fast-loss games of the same day**, plus the
opponent-matched cuts in §2.

⛔ **No `print()`/`BotOutput` was used anywhere in this study.** Every number below
comes from `placeEntity` / `moveBuilderBot` / `removeEntity` / `updateHp` /
`fireTurret` / `builderAttack` / `builderHeal` / `coreConvertAmmo` /
`distributeResources` / `updatePlayers`.

---

## 0. INSTRUMENTS, AND THE CONTROL THAT MADE EACH ONE MEAN SOMETHING

Per the standing rule: a check that has never produced the other verdict has not
been seen to check. Four instruments carry this report; all four were driven to
the opposite answer on a control.

**0.1 Seat assignment (which team is us).** `join.our_team` descends from
`winnerSide`, so it cannot be cross-checked against `won` or `ladder_games.seat`
(TRAP 7 — all three are the same variable). **Behavioural check:** our tree
spawns its opening five builders on rounds 0,1,2,3,4 unconditionally
(`LOKI_BASE_BUILDERS = 5`).
* **MEASURED:** the side `join` calls ours carries the spawn prefix `(0,1,2,3,4)`
  in **112 of 112** decoded games.
* The fingerprint is **unambiguous** (opponent side lacks it) in **60 of 112**
  games; on those, fingerprint and assignment agree **60/60**.
* **CONTROL:** with the seat flipped, agreement is **0/60**. The instrument can
  fail and does not.
* For the one game with no `join` row (`cfb6744a…_game_3`) the seat was derived
  from in-replay `winner` + `ladder_games.won`; the fingerprint confirms it
  (our side spawns at r0,1,2,3,4,6).

**0.2 The titanium / cost-scale ledger** (load-bearing for §4). Each round I
predict our next-round titanium as
`ti + passive − builds − ammo_converted − 2·builderAttack − 1·builderHeal + 10·deliveries`,
with build prices from a reconstructed additive scale
(`+1%` conveyor/splitter/barrier, `+5%` harvester, `+10%` launcher, `+20%`
bot/gunner/sentinel; destruction refunds).
* **MEASURED: 0 mismatches in 856 of 856 round transitions across the ten games.**
  Titanium at r0 reads **470** in all ten = `500 − 30` (the opening builder at
  scale 100%), and the passive tick lands on `round % 4 == 3`.
* **CONTROL:** pin the scale at 100% and the same ledger fails **338 of 856**.
* ⇒ the `updatePlayers.Player.titanium` decode, the additive-scale model, and
  therefore every "sentinel cost" figure in §4 are verified end to end.

**0.3 "Builder attacks on an enemy turret".** Counts `builderAttack` events by
our team whose target tile holds a live enemy `gunner`/`sentinel`.
* **CONTROL:** the same instrument returns **349** such events day-wide, in
  9 of 112 games (max 77 in one game) — it is capable of a non-zero verdict.

**0.4 Siege-clearance.** Time-to-death of each enemy turret built within
`d² ≤ 41` of our core, **censored at game end** (a turret is only counted if the
game ran ≥ H more rounds), so short games cannot manufacture a low clearance
rate. Reported at H = 20/30/40.

**Everything below is labelled MEASURED (counted, with denominator) or EYEBALL
(seen once, needs a count before anyone quotes it).**

---

## 1. THE TEN — MECHANISM PER GAME, FROM ENGINE-SIDE FACTS

Ordered by round of death. `d²` is to the nearest tile of the victim core's 2×2
footprint. "ALIVE" means the turret was still standing when the match ended.

| # | opponent / map | died | what killed our core | the killing turrets: build round @ tile (d² to our core) | our tree, r0–60 |
|---|---|---|---|---|---|
| 1 | The Bisons v13 / nordkap 20×26 | **r47** | 4 enemy **sentinels**, 558 dmg, first hit **r28**, ~18 HP/round | r27 (9,14) d²16 · r32 (9,16) d²4 · r34 (10,13) d²25 · r35 (7,18) d²4 — **all four ALIVE at the end** | 6 builders (r0-4,6), 4 harvesters, 14 conveyors, **1 forward sentinel r10 at (7,10)**, 5 collar barriers on their core |
| 2 | Erebus v126 / glacierkeep 30×30 | **r48** | 4 enemy **gunners** built point-blank, 588 dmg, first hit **r24** | r23 (14,4) d²1 · r25 (15,4) d²1 · r27 (16,4) d²2 · r31 (16,3) d²1 — 2 alive, 2 died on r48 (the round our core fell) | 6 builders, 3 harvesters, **20 conveyors**, 5 collar barriers; **no forward turret, no home turret**. Erebus spawned **one** builder all game and walked it to our base |
| 3 | The Bisons v13 / drakkarfjord 30×30 | **r70** | 5 enemy **sentinels**, 540 dmg, first hit **r45** | r44 (21,4) d²25 · r50 (21,5) d²25 · r52 (26,2) d²4 · r58 (29,4) d²4 · r61 (27,8) d²9 — **all five ALIVE** | 6 builders, 5 harvesters, **41 conveyors**, first barrier r41; **no forward turret, no home turret** |
| 4 | Juusto v13 / glacierkeep 30×30 | **r92** | **ONE** enemy sentinel at (14,6) d²9, built **r27**, 504 dmg from r28 to r92, **never touched** | r27 (14,6) — ALIVE | 6 builders, 3 harvesters, 10 conveyors, 1 **home** sentinel r18 at (13,5), 7 collar barriers; no forward turret |
| 5 | Clankers v17 / frostgate 20×20 | **r92** | 2 enemy sentinels + 2 gunners, 720 dmg, first hit **r52** | r36 gunner (12,10) d²16 · r49 sentinel (12,13) d²25 · r49 sentinel (12,6) d²25 · r73 gunner (17,13) d²9 — **all ALIVE** | 6 builders, 5 harvesters, 17 conveyors, **1 forward sentinel r9 at (7,9)**, 4 collar barriers. Our sentinel did 378 dmg to their core; **Clankers healed their core +312 over 150 `builderHeal` actions** |
| 6 | lingling_40h v66 / midgard 30×30 | **r92** | 1 sentinel + 5 gunners ringing our core, 560 dmg, first hit **r70** | r63 sentinel (27,22) · r69/73/75/77/82 gunners at (28,25)(28,26)(28,27)(28,28)(27,28) d²1–2 · r79 sentinel (29,28) — **all ALIVE** | 6 builders, 5 harvesters, 16 conveyors, **2 forward sentinels r40/r43**. We did **900** dmg to their core; **they healed +552** and survived on 152 HP |
| 7 | lingling_40h v66 / drumlin 25×25 | **r93** | 1 sentinel + 1 gunner, 698 dmg, first hit **r37** | r32 sentinel (15,14) d²25 · r36 gunner (17,17) **d²2** — both ALIVE | 6 builders, 5 harvesters, 17 conveyors, forward sentinel r21 at (8,8) (**killed by them r28**), home gunner r39 |
| 8 | Juusto v13 / auroraveil 20×20 | **r104** | **ONE** enemy sentinel at (5,1) d²16, built **r27**, 504 dmg from r47 to r104, **never touched** | r27 (5,1) — ALIVE | 5 builders, 2 harvesters, 12 conveyors, 2 forward sentinels r13/r15 (**both killed by them, r22 and r45**), 7 collar barriers |
| 9 | 0033 v57 / midgard 30×30 | **r104** | a **creeping ladder**: sentinel r41 (15,3) → r45 (12,2) → r64 (7,2) → gunners r75 (4,1), r87 (1,1); 504 dmg, first hit **r75**; on the way they destroyed 4 of our harvesters/conveyors (r45–r73) | r64 (7,2) d²16 · r75 (4,1) d²2 · r87 (1,1) d²2 — all ALIVE | 7 builders, 7 harvesters, 24 conveyors, 2 forward sentinels r47/r58. **We got their core to 32 HP; they healed +216** |
| 10 | Juusto v13 / midgard 30×30 | **r114** | **ONE** enemy sentinel at (8,2) d²25, built **r53**, 504 dmg from r60 to r114, **never touched**. Their builder arrived via a **5-throw launcher ladder** r6→r18, (25,26)→(5,6) | r53 (8,2) — ALIVE | 6 builders, 5 harvesters, 26 conveyors, **2 HOME sentinels r21 (4,3) and r23 (5,1)** — which did not stop it; no forward turret |

**MEASURED, over the ten:**

* **All 5,680 HP of damage to our core came from turret fire** — 4,014 sentinel,
  1,666 gunner, **0 from builder attacks**. (Day-wide control: 65,538 sentinel /
  18,130 gunner / **342** builder-attack across the other 102 games — so the
  builder-attack channel exists and is simply irrelevant here.)
* **32 enemy turrets were planted inside `d² ≤ 41` of our core across the ten.
  30 were still standing when the match ended. The 2 that died, died on the
  final round of game #2.**
* **Our builders made 264 attacks on enemy buildings in the ten games and 0 of
  them targeted a gunner or a sentinel** (instrument control in §0.3: it returns
  349 elsewhere).
* **Median interval from the first enemy turret plant to our core's death: 48
  rounds** (range 20–77). **Median from first damage to death: 34.5 rounds**
  (range 19–64). ⇒ in every one of the ten there was a window of 20+ rounds in
  which the killing turret was standing, visible and shooting, and nothing
  happened to it.

---

## 2. THE CONTROL — WHAT ACTUALLY DIFFERS

### 2.1 The matched sets available

**MEASURED:** exact `(opponent, map)` matching is almost impossible on this day —
a 5-game match uses 5 different maps, and 9 of the 10 fast-loss cells have
**exactly one** game vs that opponent on that map. The only matched pair is
**Erebus / glacierkeep** and its two games are **different opponent versions**:

| | v126, r49 **fast loss** | v131, r450 win |
|---|---|---|
| enemy turrets near our core | 4 gunners, r23–r31, d²1–2 | **none, all game** |
| our forward turrets | none | 1 sentinel at r394 |
| our in-band affordability | 1 of 28 rounds | 0 of 95 rounds |
| shots we fired | 0 | 49 |

**EYEBALL (n=1 pair, versions differ):** the difference is not our behaviour —
our affordability gate was closed in the win too — it is that **Erebus v131 never
came**. Do not quote this cell as evidence for anything.

⇒ the usable control is **per-opponent** (same day, same `oppver` except Erebus)
and **whole-day**.

### 2.2 Per-opponent control, 2026-08-17

`a45` = enemy turrets alive within d²≤41 of **our** core at r45 · `o45` = ours at
theirs · `heal/rd` = HP healed on our core per round of exposure · last column =
enemy siege turrets **we destroyed** / built.

| opponent | group | n | a45 | o45 | a45−o45 | 1st enemy plant | heal/rd | we killed siegers |
|---|---|---|---|---|---|---|---|---|
| Juusto v13 | fast loss | 3 | 0.67 | 0.00 | +0.67 | r27 | **0.00** | 0/3 |
| | won | 8 | 0.62 | 0.25 | +0.38 | r27 | 5.89 | 4/11 |
| | slow loss | 4 | 0.75 | 0.50 | +0.25 | r35 | 2.79 | 0/4 |
| The Bisons v13 | fast loss | 2 | 2.50 | 0.50 | +2.00 | r36 | 2.09 | 0/9 |
| | won | 2 | 2.00 | 1.00 | +1.00 | r39 | 6.00 | 0/9 |
| | slow loss | 1 | 3.00 | 1.00 | +2.00 | r1 | 10.67 | 1/5 |
| lingling_40h v66 | fast loss | 2 | 1.00 | 1.00 | 0.00 | r48 | 2.94 | 0/9 |
| | won | 3 | 1.67 | 0.33 | +1.33 | r34 | 4.15 | 1/7 |
| Erebus | fast loss (v126) | 1 | 4.00 | 0.00 | +4.00 | r23 | 3.52 | 2/4 |
| | won | 10 | 0.00 | 0.20 | −0.20 | r72 | 7.31 | 0/3 |
| | slow loss | 4 | 1.25 | 1.00 | +0.25 | r19 | 2.03 | 3/21 |
| Clankers v17 | fast loss | 1 | 1.00 | 1.00 | 0.00 | r36 | 5.17 | 0/4 |
| | won | 2 | 0.50 | 0.00 | +0.50 | r26 | — | 1/4 |
| | slow loss | 7 | 0.71 | 1.00 | −0.29 | r52 | 0.00 | 7/35 |
| 0033 v57 | fast loss | 1 | 0.00 | 0.00 | 0.00 | r64 | 0.00 | 0/3 |
| | won | 2 | 0.00 | 0.00 | 0.00 | r77 | 0.53 | 2/3 |
| | slow loss | 7 | 0.57 | 0.86 | −0.29 | r44 | 3.66 | 7/50 |
| **pooled (6 opps)** | **fast loss** | **10** | **1.40** | **0.40** | **+1.00** | r34 | **1.91** | **2/32** |
| | won | 27 | 0.56 | 0.26 | +0.30 | r30 | 5.20 | 8/37 |
| | slow loss | 23 | 0.87 | 0.87 | 0.00 | r30 | 2.66 | 18/115 |

### 2.3 The whole-day control (10 fast losses vs 102 others), with p-values

Game-level permutation tests, 20,000 shuffles, one-sided. **n=10 — every one of
these is underpowered and the p-values are optimistic** (games cluster by match:
the ten come from 7 matches; the rated pooled DEFF is 1.529 and none of these
tests applies it).

| quantity | FAST (n=10) | CTRL (n=102) | one-sided p |
|---|---|---|---|
| enemy turrets alive at our core, r40 | 1.30 | 0.62 | 0.036 |
| enemy turrets alive at our core, r45 | 1.40 | 0.66 | 0.025 |
| siege differential (theirs at us − ours at them), r45 | **+1.00** | **+0.17** | **0.019** |
| in-band rounds where we could afford a sentinel (rate) | 0.075 | 0.158 | 0.020 |
| forward turrets we planted by r119 | 1.00 | 1.68 | 0.096 |
| heal-seat occupancy while our core was under fire | 0.41 | 0.57 | 0.109 |
| first enemy plant round | r34 | r36 | **no difference** |

### 2.4 The single largest asymmetry, and it is a DAY-WIDE property, not a property of the ten

Censoring-controlled siege clearance — a turret only counts if the game ran ≥H
more rounds after it was planted:

| horizon | | WE clear THEIR sieger | THEY clear OUR sieger |
|---|---|---|---|
| 20 rounds | FAST (10 games) | **0 / 20 = 0.0%** | 2 / 9 = 22% |
| | CTRL (102 games) | 23 / 266 = **8.6%** | **240 / 376 = 63.8%** |
| | CTRL, wins only | 13 / 60 = 21.7% | 109 / 203 = 53.7% |
| | CTRL, losses only | 10 / 206 = 4.9% | 131 / 173 = 75.7% |
| 30 rounds | FAST | 0 / 11 | 3 / 9 |
| | CTRL | 29 / 247 = 11.7% | 252 / 355 = 71.0% |
| 40 rounds | FAST | 0 / 9 | 3 / 8 |
| | CTRL | 33 / 233 = 14.2% | 254 / 334 = 76.0% |

⚠ **HONEST READING, and it is the opposite of the tempting one.** `0/20` in the
fast losses is **not** significantly below the 8.6% base rate — a binomial at
p=0.086 gives P(0 of 20) ≈ 0.17. **The fast losses are not unusually bad at
clearing siege turrets; the WHOLE DAY is bad at it, and they are the tail.**
The opponent removes 64% of our forward turrets inside 20 rounds; we remove 9%
of theirs. **That ~7× asymmetry, at n=266 vs n=376 turrets, is the most robust
number in this document.**

**MEASURED code-side fact that is consistent with it** (spec read, not a
measurement of behaviour): `main.py:597 _home_defend` → `_sabotage_prio` is the
only defensive melee path at our own core, and `main.py:635` reads
`if LOKI_QUIET_ON: return False` before ever calling `ct.fire()`;
`doctrine.py:1488` ships `LOKI_QUIET_ON = True` ("no builder melee: no core peck,
no siphon hit, **no counterbattery**"). Separately `main.py:578
_nearest_home_intruder` filters `get_entity_type(eid) != EntityType.BUILDER_BOT`
→ **an enemy gunner or sentinel parked beside our core is not an "intruder" to
this bot at all.** Both are *specification* facts offered to explain the
measurement; neither was tested by ablation here.

### 2.5 Defence presence during the siege

**MEASURED:** over the rounds in which our core was actually taking fire —
* fast losses: a friendly builder stood on one of the core's 8 heal seats in
  **137 of 400 rounds (34.2%)**; control: **8,600 of 13,531 (63.6%)**.
* **Titanium was not the constraint** — the bank held ≥1 Ti in **91.5%** of those
  fast-loss rounds (control 98.0%).
* In **4 of the 10** (Juusto ×3 and 0033/midgard) heal-seat occupancy was ~0%
  and our core received **exactly 0 HP of healing** across 30–65 rounds of being
  shot. Against the same Juusto v13, the 8 games we **won** show a median of
  **580 HP** healed onto our core.
* ⚠ At game level the difference is **p = 0.109** — not significant at n=10. The
  round-level 34.2% vs 63.6% is heavily clustered and must not be quoted as if
  it were 400 independent observations.

---

## 3. VERDICT — repeatable openings, map hole, or nothing in common?

**None of the three, cleanly. The honest answer is a fourth one.**

**(a) NOT 2–3 repeatable opponent openings.** The openings are real and
identifiable, but **each one is that opponent's normal behaviour in games we
win too**, so none of them discriminates:
* **Juusto v13 runs a launcher ladder** — its own launcher throws its own builder
  toward our core in 3-throw / 5-throw chains starting r6, destroying each
  launcher behind it. **MEASURED: present in 13 of 15 Juusto games on 2026-08-17,
  including 7 of the 8 we won.** Present in all 3 Juusto fast losses. It is a
  signature, not a cause.
* **Juusto plants exactly one turret near our core in 14 of 15 games** (median
  first plant r27), win or lose.
* **lingling_40h v66 uses launchers the other way** — 32 throws of **our** bots
  away from their core across 5 games, 0 insertions. HTTP 418 does both
  (18 insertions, 72 evictions in 7 games).
* Erebus/Bisons/Clankers/0033 walk a builder over and build turrets. Ordinary.

**(b) NOT a map-geometry hole — not at this n.** midgard is 3 of 7 games
(42.9% fast-loss rate against an 8.9% day baseline, uncorrected one-sided
p = 0.019) — but **15 maps were tested**, and after any multiplicity correction
that is p ≈ 0.28. Map area ≥750 tiles: 6/41 (14.6%) vs <750: 4/71 (5.6%),
**Fisher two-sided p = 0.167**. Core-separation d² bands run 4.3% → 6.5% → 9.4%
→ 15.4% — a monotone trend, no significance. **Suggestive, not established.**

**(c) NOT "nothing in common".** One thing is common to all ten and it is
measurable and one-sided:

> **In every one of the ten, the opponent established turret fire on our core
> and we never removed it: 32 turrets planted, 30 still standing at the end,
> 0 of 264 of our builder attacks aimed at one, and 0 of 20 cleared inside 20
> rounds. What separates the ten from the day is that the enemy had ~2×
> as many turrets alive on our core at r45 (1.40 vs 0.66, p=0.025) while our
> own counter-siege was no better than usual (0.40 vs 0.49) — i.e. we lost the
> race, on a board where we have no way to stop the clock.**

**The buildable plank this points at is siege clearance / home defence, not an
opponent-specific counter and not a map ban.** Our forward turret dies to them
64% of the time inside 20 rounds; theirs dies to us 9% of the time. Closing that
gap is worth more than anything specific to these ten games.

---

## 4. FORWARD-TURRET STATE AT THE MOMENT OUR CORE DIED — AND WHICH GATE REFUSED

Commissioned addendum. "Forward turret" = a gunner or sentinel **we** built
within `d² ≤ 50` of the **enemy** core — the band `raid.py:684` itself uses.

### 4.1 Had we planted anything?

**MEASURED: 4 of the 10 had NO forward turret at all when the core died.**

| opponent / map | died | our forward turrets before death |
|---|---|---|
| The Bisons / nordkap | r47 | 1 — sentinel r10 @(7,10) d²13 |
| **Erebus / glacierkeep** | **r48** | **NONE** |
| **The Bisons / drakkarfjord** | **r70** | **NONE** |
| **Juusto / glacierkeep** | **r92** | **NONE** |
| Clankers / frostgate | r92 | 1 — sentinel r9 @(7,9) d²16 |
| lingling / midgard | r92 | 2 — r40 @(7,6), r43 @(6,5) |
| lingling / drumlin | r93 | 2 — r21 @(8,8), r77 @(6,8) |
| Juusto / auroraveil | r104 | 2 — r13 @(6,13), r15 @(5,13) (both killed, r22/r45) |
| 0033 / midgard | r104 | 2 — r47 @(22,23), r58 @(25,29) |
| **Juusto / midgard** | **r114** | **NONE** (the 2 sentinels at r21/r23 were HOME turrets at d²≤5 of *our* core) |

Median forward turrets planted by r119: **FAST 1.0 · WON 2.0 · SLOW LOSS 1.0**
(game-level permutation FAST vs rest p = 0.096 — **not significant**).

### 4.2 Which gate refused — reconstructed per round

`raid.py:653 _try_forward_sentinel` refuses unless **all** hold:
`SLOT_HARVESTERS ≥ LOKI_FWD_MIN_HARV (2)` · `resources ≥ sentinel_cost +
LOKI_FWD_TI_FLOOR (40)` · the raider is already at `dsq_core(p, E) ≤ 50`.
`SLOT_HARVESTERS` is a **monotone high-water mark of harvesters built**
(`doctrine.py:381`, `eco.py:542,1694`), so cumulative harvester builds is the
right reconstruction (store lag ≤ 1 round; not material at these margins).
The titanium and cost figures are the §0.2-validated ledger.

**Round at which each gate first opened, and the state at death:**

| opponent / map | harv≥2 | bank≥cost+40 | raider in band | ALL THREE | at death: Ti / sentinel cost / scale |
|---|---|---|---|---|---|
| Bisons / nordkap (r47) | r7 | r0 | r7 | r7 | 10 / 83 / 279% |
| Erebus / glacierkeep (r48) | r16 | r0 | r21 | **never** | 0 / 78 / 260% |
| Bisons / drakkarfjord (r70) | r14 | r0 | r32 | **never** | 14 / 83 / 279% |
| Juusto / glacierkeep (r92) | r17 | r0 | r22 | **never** | 12 / 81 / 273% |
| Clankers / frostgate (r92) | r8 | r0 | r5 | r8 | 3 / 76 / 254% |
| lingling / midgard (r92) | r5 | r0 | r37 | r37 | 16 / 94 / 315% |
| lingling / drumlin (r93) | r13 | r0 | r15 | r20 | 33 / 74 / 248% |
| Juusto / auroraveil (r104) | r12 | r0 | r11 | r12 | 36 / 71 / 238% |
| 0033 / midgard (r104) | r5 | r0 | r44 | r44 | 8 / 102 / 341% |
| Juusto / midgard (r114) | r6 | r0 | r38 | **never** | 3 / 93 / 313% |

**MEASURED — the answer, and it is not the one the RUSH2 hypothesis predicts.**
Over the **631 rounds** in the ten games where a raider was inside the build band
before our core died:

| gate | rounds it was CLOSED | share |
|---|---|---|
| **bank** (`ti < cost + 40`) | **605** | **95.9%** |
| harvester (`built < 2`) | **4** | **0.6%** |
| — of those 631, current gate fully open | 26 | 4.1% |
| — would be open at the RUSH floor (`cost + 8`) | 40 | 6.3% |
| — **affordable at ALL (`ti ≥ cost`, zero floor)** | **46** | **7.3%** |

**⇒ The binding refusal in all ten is the BANK, and it is not the 40 Ti safety
margin — it is raw affordability. Waiving the harvester prerequisite buys 4
rounds out of 631 (0.6 pp). Cutting the floor 40→8 buys 14 rounds (2.2 pp).
Removing the floor entirely buys 20 rounds (3.2 pp). The other 92.7% of in-band
rounds we could not have paid for a sentinel at any floor.**

**Why: our own opening prices the sentinel out of reach.** At the round of death
our cost scale is **238–341%**, so a 30 Ti sentinel costs **71–102 Ti**, and our
bank is **0–36 Ti**. Scale decomposition at death (live contributions):
builder bots **80–140 pp** (the dominant term, 4–7 bots × 20%), conveyors
**10–47 pp**, harvesters 15–25 pp. Worked example, Erebus/glacierkeep:

```
r0   ti=470  sentinel cost 36   need 76    raider d²=530
r18  ti=144  cost 70            need 110   d²=82
r21  ti= 79  cost 72            need 112   d²=49   <- raider arrives IN BAND, affordable at cost, refused by the +40 floor
r24  ti= 39  cost 74            need 114   d²=16   <- unaffordable at ANY floor from here on
r30  ti=  0  cost 76                       d²=2
r48  ti=  0  cost 78                       d²=2    <- core dies
```
The Bisons/drakkarfjord has the one clean floor-only refusal: **r39, raider at
d²=5, ti=96, cost=78 — affordable at cost and at cost+8, refused by cost+40.**

### 4.3 The control for §4 — is a closed bank gate special to the ten?

Same reconstruction over all 112 decoded games, capped at r119 so long games do
not dominate:

| group | n | in-band rounds | affordable (`ti≥cost`) | current gate open | RUSH floor (8) open | harvester gate blocks | games with NO forward turret by r119 |
|---|---|---|---|---|---|---|---|
| **fast loss** | 10 | 631 | **7.3%** | 3.5% | 6.3% | **0.6%** | 4/10 |
| won | 49 | 4,719 | 18.8% | 5.7% | 15.7% | 1.5% | 10/49 |
| slow loss | 53 | 5,372 | 11.9% | 3.2% | 10.4% | 2.0% | 10/53 |

Game-level, affordability **rate**: FAST 0.075 vs CTRL 0.158, one-sided
permutation **p = 0.020**.

**⇒ VERDICT ON THE RUSH2 HYPOTHESIS, stated symmetrically because both outcomes
were acceptable:**

1. **CONFIRMED, weakly:** the fast losses really are the games where the forward
   turret was least affordable (7.3% vs 18.8% in wins, p=0.020), and 4 of 10
   died having planted none at all. Being unable to open the siege is genuinely
   associated with dying early, on live rated games.
2. **REFUTED, strongly, and this is the load-bearing half:** **neither of the two
   preconditions RUSH2 waives is the binding gate.** The harvester prerequisite
   blocks 0.6% of in-band rounds in the fast losses and ≤2.0% in every other
   group — **it is essentially never binding anywhere**, because it opens at
   r5–r17 while the raider does not arrive until r5–r44. The 40→8 floor cut adds
   2.2 pp. **Together they would open 14 of 631 refused rounds.** The real
   refusal is that a sentinel costs 71–102 Ti at our shipped cost scale and the
   bank is empty by the time a raider is in position.
3. **The lever this points at instead:** the **price**, not the gate. Either
   plant while the opening 470 Ti is still there (i.e. arrive earlier — median
   arrival r21.5 in the fast losses, and affordability is 9–21 of the first
   21 rounds in every one of the ten), or stop inflating the scale before the
   plant (4–7 builder bots = 80–140 pp of the 138–241 pp of inflation; 10–41
   conveyors add 10–47 pp).

⚠ **The counterfactual columns are on the GATE PREDICATE ONLY, holding the
observed titanium path fixed.** Building a sentinel would have spent 71–102 Ti
and added 20 pp of scale, changing every later row. They are an **upper bound on
how often the gate would have said yes**, not a simulation of the game.

---

## 5. REFUTED / RULED OUT — recorded so nobody re-derives them

| hypothesis | verdict | the number that killed it |
|---|---|---|
| The opponents share a distinctive **opening** we can counter | **REFUTED** | Juusto's launcher ladder is in 13/15 of its games including 7/8 wins; its single forward turret is in 14/15. lingling never inserts (0 insertions, 32 evictions). Bisons/Clankers/0033/Erebus never insert. |
| The enemy **planted earlier** in the fast losses | **REFUTED** | median first enemy plant **r34 (FAST) vs r36 (CTRL)**. No difference. |
| We were **short of ammunition** | **REFUTED** | titanium converted to ammo by r60: **FAST median 94, CTRL median 98**. Indistinguishable. (Their conversion was higher — 192 vs 115 — which is downstream of them owning more turrets.) |
| Our **economy** was behind | **REFUTED** | harvesters by r60 FAST 5.0 vs CTRL 4.5; conveyors comparable. If anything we were ahead. |
| It is a **map-geometry hole** | **NOT ESTABLISHED** | midgard 3/7 (p=0.019 uncorrected, ≈0.28 after 15-map multiplicity); large-map 6/41 vs 4/71 Fisher p=0.167. |
| The **harvester prerequisite** (`LOKI_FWD_MIN_HARV=2`) delayed our siege | **REFUTED** | it blocked **4 of 631** in-band rounds (0.6%); ≤2.0% in every control group. |
| The **40 Ti floor** was the refusal | **MOSTLY REFUTED** | it is the sole refusal on 20 of 631 in-band rounds (3.2 pp); on the other 585 we could not afford the sentinel at any floor. |
| We were **too poor to heal** the core under siege | **REFUTED** | bank ≥1 Ti in **91.5%** of fast-loss siege rounds. Nobody was standing on a heal seat — that is a positioning failure, not a bank failure. |
| We are **specifically bad** at clearing siege turrets in these ten | **NOT ESTABLISHED** | 0/20 vs an 8.6% base rate is P≈0.17. The clearance hole is **day-wide** (8.6% ours vs 63.8% theirs), which makes it a bigger finding, not a smaller one. |
| The **titanium tiebreak / passive income** mattered | **N/A** | all ten ended `core_destroyed`; no tiebreak was reached. |

---

## 6. WHAT IS NOT RESOLVABLE FROM THIS SURFACE — stated rather than estimated

* **Turret FACING.** `Entity.gunner/sentinel.direction` is in the schema but was
  not extracted here, so I cannot say whether our two home sentinels in
  Juusto/midgard (r21, r23) had the enemy sentinel at (8,2) in their line. A
  sentinel **cannot rotate** (`can_rotate` is gunner-only), which makes facing a
  plausible reason a home turret is inert — **but that is an untested hypothesis,
  not a finding.** It is cheap to add.
* **Why no builder stood on a heal seat.** The occupancy is measured; the
  decision that produced it is not. Role assignment lives in the comms store,
  which no replay carries.
* **`SLOT_HARVESTERS` exactly.** I reconstruct the quantity it is *specified* to
  carry (monotone harvesters built). A store write is visible one round later; at
  the observed margins that cannot flip any row in §4.2, but it is not the store
  itself.
* **Anything from our own logging.** Platform replays carry
  `BotOutput{id, execTimeUs}` with `stdout` empty; no instrument here touched it.
* **Statistical power.** n=10, from 7 matches, on one day. Every p-value in §2.3
  and §4.3 is game-level and uncorrected for the match cluster (rated pooled
  DEFF 1.529 would widen them by ~×1.24). **Treat every one of them as a
  prioritisation signal, not as a result.** The only figures robust enough to
  quote without hedging are the day-wide clearance asymmetry (§2.4, n=266 vs 376
  turrets) and the §4.2 gate decomposition (631 rounds, deterministic
  reconstruction validated at 856/856).
