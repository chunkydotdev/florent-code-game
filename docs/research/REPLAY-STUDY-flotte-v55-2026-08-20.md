# REPLAY STUDY — The Flotte Experience, v55 (and the v54 boundary)

**PROVENANCE**
* **Agent:** fresh opus replay-study subagent, no inherited session context beyond the
  commissioning brief. Commissioned by **research s52, 2026-08-20**.
* **Method:** `docs/research/PLAYBOOK-move-mining-2026-08-16.md` (DISCIPLINE section:
  MEASURED vs EYEBALL labels; every mechanism claim carries a control that can come out
  the other way; refuted mechanisms retained; a piece is one behaviour with ≥2 file+round
  anchors).
* **Inputs, exactly:** `corpus/join.tsv`, `corpus/ladder_games.tsv`,
  `corpus/league_matches.tsv`, `corpus/meta_join.tsv`, `replay_archive/*.replay26`,
  `tools/replay_schema.md`, `tools/replay_census.py` (parser primitives),
  `tools/corpus/replay_autopsy.py` (attribution rules re-used verbatim), `QUEUE.md`,
  `bots/_v488beltbreak2/` (control tree, read-only).
* **Ground:** opponent **The Flotte Experience**, current version **v55**
  (`league_matches.tsv`, last match `d0d35d62` at `2026-08-20T08:32:59.776Z`,
  `teamAVersion=55`). Their rating at that row **1892.32**; ours at the same clock
  **1774.43** (`ladder_games.tsv`, match `8dc79d90`, `2026-08-20T08:32:59.776Z`).
* **Games decoded:** **40 rated** games vs us (20 at their v54, 20 at their v55 — every
  rated game that exists at those two versions) **+ 175 third-party** games
  (Flotte vs Erebus at v54/v55, from `meta_join.tsv`, all present in `replay_archive/`).
  **215 replays decoded in total.**
* **No platform matches, submissions, or bot edits were made.** Archive/decode only.

---

## 0. INSTRUMENT AND ITS CONTROLS

The decoder is `tools/replay_census.py`'s parser primitives with
`tools/corpus/replay_autopsy.py`'s attribution rules (damage-target law: turret fire hits
the tile's UNIT when one is present, else the BUILDING; builder attacks always hit the
BUILDING; FireTurret may be emitted after the victim's removeEntity, so entity identity is
resolved off a never-popped registry).

**POSITIVE CONTROL (self-check, MEASURED):** attributed core damage must equal the summed
negative `UpdateHp` deltas on that core's entity id. **80 of 80 team-sides matched exactly,
0 mismatches**, across the 40 rated games. A decoder that mis-priced sentinel damage, or
that ignored unit-absorption on the footprint, cannot pass this — the residual is printed
per team-side and is zero everywhere.

**CONTROL THAT RUNS THE OTHER WAY (core-heal channel):** the same decoder reads core
*healing*. Against Erebus it reports Flotte healing their own core in **142 of 175 games,
60,868 HP total, max 2,584 in one game**, and Erebus healing theirs in 55/175. So the
channel is live and the decoder sees it. That matters because in our own 40 games the same
channel reads **7/20 (v54) and 6/20 (v55)** — a real number, not an instrument zero.
(This is the control that killed one of my own candidate claims — see §6.)

---

## 1. PREMISE AUDIT (each premise re-derived before anything was built on it)

| Premise | Verdict | Evidence |
|---|---|---|
| **P1** rated record by their version: v21 1/5, v53 2/10, v54 7/20, v55 3/20 | **CONFIRMED, on two independent surfaces** | `ladder_games.tsv` (`opp ~ /Flotte/`) game-level tally reproduces all four cells exactly. Independently, `league_matches.tsv` match scores: v54 = 1-4, 3-2, 2-3, 1-4 → **7/20**; v55 = 0-5, 1-4, 1-4, 1-4 → **3/20**. |
| **P2** last-12 all `core_destroyed`, losses at turns 143-278 | **CONFIRMED, amended** | **40 of 40** v54+v55 games end `core_destroyed` (MEASURED, from the replay's own `winCondition` field). Loss turns: v55 **102-278** (median 213), v54 **147-374** (median 167). The "143-278" band is right for v55 and has a 374 outlier at v54 (`d0a8e564_game_2`, glacierkeep). |
| **P3** move_miner share 25.0% "modern" (n=40) | **CONSISTENT WITH RECORD** (per the commissioner's mid-flight amendment; window assumption named, denominator not independently re-derived here) | 7/20 + 3/20 = **10/40 = 25.0% exactly**, if move_miner's "modern" window spans v54+v55. |
| **P4** their lone-intruder economy raid (the `doctrine.py:118` "Flotte 1745" incident) | **CONFIRMED AND SHARPENED — and it is worse than the incident note says** | Their builders make **1,479 attack actions across the 40 games; 971 (65.6%) target OUR HARVESTERS**, 418 our conveyors, 0 our turrets, **0 our core**. We lost **151 harvesters and 340 conveyors** to them across 40 games. See §3 piece C for where those attacks sit relative to our detector. |
| **BRIEF'S PRICING** "a 5-0 pays +10.79" | ⛔ **REFUTED** | At the 2026-08-20T08:32:59Z ratings (us 1774.43, them 1892.32, gap **+117.89**), `delta = 32×(S−E)` with `E = 0.3366` gives **5-0 = +21.23** and **0-5 = −10.77**. **+10.79 is the magnitude of the LOSS side, not the win side.** Full ladder in §5. (`#56` already records that `target_value.py` prices off a cached rating; this is a sign/side error on top of that, whatever its origin.) |

---

## 2. Q1 — WHAT WINS THEM THE GAME, MECHANICALLY

### 2.1 The shape of their bot (MEASURED, 40 rated games vs us + 175 vs Erebus)

**A four-builder, three-harvester economy that stops expanding at ~r25 and spends the rest
of the game converting titanium into turret ammunition.**

| | vs us v54 (n=20) | vs us v55 (n=20) | vs Erebus v54 (n=55) | vs Erebus v55 (n=120) |
|---|---|---|---|---|
| builder bots ever built | **4 in 20/20** | **4 in 20/20** | **4 in 55/55** | 4 in 110/120 |
| first harvester round (median) | 5 | 5 | 5 | 6 |
| harvesters (median) | 3 | 3 | 3 | 3 |
| conveyors (median) | 15 | 10 | 14 | 15 |
| first launcher round (median) | 7 | 6.5 | 6.5 | 7 |
| launchers (median) | 2 | 2 | 2 | 2 |
| first gunner round (median) | 23.5 | 20.5 | 23 | 25.5 |
| gunners (median) | 6 | 5.5 | 5 | 6 |
| **first sentinel round (median)** | **117** | **119** | **115** | **115** |
| **Ti → ammo converted (median)** | **881** | **1,010** | **536** | **576** |

For contrast, **our** medians in the same 40 games: 6 builder bots, 5-7 harvesters, 32-36
conveyors, **0-1 gunners**, 2 sentinels, 3-4 launchers, and **100-198 Ti converted to ammo**.
They out-convert us **5-9×**.

### 2.2 The kill mechanism, in three measured steps

**STEP 1 — GUNNER GRIND FROM ~r20.** First gunner at median r20.5-23.5, ~6 per game, sited
with a p25 distance of **d²=13 from our core** — exactly the gunner's attack radius
(`GUNNER` r²=13). They fire a median of **118 (v54) / 144.5 (v55) gunner shots per game**.
Gunners deliver **7,427 (v54) + 7,014 (v55) = 14,441 HP into our core across 40 games**.

**STEP 2 — THE SENTINEL CLOCK AT ~r115.** Their first sentinel lands at a strikingly tight
round: across **147 games at both versions and against two different opponents**, p25/median/p75
= **113 / 115 / 116** (Erebus, n=47 at v54 and n=99 at v55). It is sited at
**d² 25-41 from our core** — the sentinel's attack radius is **r²=32**, and its line-shot
**ignores obstacles**, so this is a max-standoff siege turret that our walls do not stop.

**⭐ THE OFFSET IS THE MECHANISM CLAIM, and it is MEASURED: in 27 of the 31 games where
they built a sentinel, our core's FIRST damage arrives 1-20 rounds after their first
sentinel is placed, median offset +5 rounds.** Anchors:

| file | their 1st sentinel | our core's 1st damage | d² sentinel→our core |
|---|---|---|---|
| `1eea783c…_game_1.replay26` (v54, nordkap) | r114 | **r119** | 41 |
| `1eea783c…_game_2.replay26` (v54, ragnarok) | r116 | **r119** | 41 |
| `67c1942c…_game_2.replay26` (v54, frostgate) | r112 | **r117** | 32 |
| `296cfc4e…_game_1.replay26` (v55, ragnarok) | r114 | **r115** | 41 |
| `296cfc4e…_game_3.replay26` (v55, archipelago) | r114 | **r127** | 25 |
| `f53fa799…_game_4.replay26` (v55, drumlin) | r111 | **r116** | 41 |

The 4 negative offsets are games where a gunner opened the account first (e.g.
`296cfc4e…_game_2.replay26`, fjordgate v55: our core first bled at r16, no sentinel ever built,
931 HP taken by gunners alone).

Sentinels deliver **8,190 (v54) + 9,540 (v55) = 17,730 HP into our core** — **52-58% of all
core damage they do**, from ~1 turret per game.

**STEP 3 — THEIR BUILDERS EAT OUR ECONOMY WHILE THE TURRETS WORK.** 1,479 builder attacks,
65.6% on our harvesters; 151 harvesters and 340 conveyors of ours destroyed across 40 games,
against 51 conveyors and 3 harvesters of theirs destroyed by us.

### 2.3 Where OUR kill stalls — and it is one sentence

**⭐⭐ 100% of the damage we have ever done to a Flotte core in these 40 games came from
OUR SENTINELS.** MEASURED: **6,840 (v54) + 4,086 (v55) = 10,926 HP, all `sentinel`;
`gunner` = 0; `builder_attack` = 0.**

And our builder attacks are not idle — we made **1,779 of them** (755 at v54, 1,024 at v55)
— but **not one of the 1,779 targeted a tile in their core footprint.** They went to
conveyors (777), gunners (587), sentinels (325), barriers (28), launchers (2). Our builders
**do** reach their core: the minimum distance of one of our builders to their core NW corner
is **d²=1 (median), first achieved at median round 11 (v55) / 31 (v54)**. We arrive and then
convert nothing.

Meanwhile our sentinel — the sole channel — is bought under `AMMO_FLOOR = 16`
(`bots/_v488beltbreak2/doctrine.py:963`), i.e. a magazine of roughly **one sentinel shot**,
while they convert ~1,000 Ti/game. Our sentinel fires a median of **14 (v54) / 6 (v55)**
shots per game. **45 of our sentinels died across the 40 games; 13 of theirs died.**

### 2.4 The attrition ledger (MEASURED, unit deaths across 40 games)

| destroyed | ours | theirs |
|---|---|---|
| builder bot | 82 | **13** |
| conveyor | 340 | 51 |
| harvester | 151 | 3 |
| launcher | **158** | 2 |
| sentinel | 45 | 13 |
| gunner | 16 | 55 |
| barrier | 75 | 9 |

We destroy their gunners (55) and they let us. Everything else runs against us by 3-50×.

---

## 3. Q2 — THE v54→v55 BOUNDARY: THEIR CHANGE OR OUR CHURN?

### VERDICT: **NON-DECOMPOSABLE ON OUTCOME (n=40 games / 8 matches). On MECHANISM the
evidence points at OUR CHURN, and a real Flotte v54→v55 step-up is EXCLUDED above +7.9pp.**

### Branch A — "their change" (the branch that FAILS to establish)

1. **Their league-wide game share barely moved.** `league_matches.tsv`, ALL opponents
   (not us-only): **v54 = 104/210 games (49.52%) over 42 matches; v55 = 338/705 games
   (47.94%) over 141 matches.** Diff **+1.58pp in FAVOUR of v54**, 95% half-width
   **±9.52pp** (two-fixture form, rated pooled DEFF 1.529 on both arms) → CI
   **[−7.94, +11.10]pp**.
   Restated as the EXCLUSION it needs to be (per the DEFF direction clause):
   **their v55 is not better than their v54 by more than 7.9pp of game share.**
2. **Their behaviour against a PINNED third party is indistinguishable.** Erebus **v148**
   is the one third-party version present on both sides of the boundary
   (Flotte v54 n=25, v55 n=5). Every script constant matches:

   | | fl v54 vs ere v148 (n=25) | fl v55 vs ere v148 (n=5) |
   |---|---|---|
   | builder bots ever built | 4 in 25/25 | 4 in 5/5 |
   | median turns | 134 | 134 |
   | first harvester round | 5 | 6 |
   | first launcher round | 7 | 7 |
   | first gunner round | 27 | 20 |
   | **first sentinel round** | **115** | **115** |
   | Ti→ammo (median) | 557 | 527 |
   | damage received by their core (median) | 259 | 259 |
   | damage received by opp core (median) | 504 | 504 |

   ⚠ n=5 on the v55 side is thin and cannot exclude a small change. It CAN and does
   exclude a change large enough to move a 20pp outcome by itself.
3. Across ALL 175 Erebus games the coarse behavioural means DO differ (their builder
   attacks 6.6→45.9/game, heals 72→137, TLE rounds 9.5→38.3). **These are CONFOUNDED by
   game length**: Erebus shipped v143→v169 across the window and median turns rose 134→162.
   The pinned v148 cell removes that confound and the differences vanish. **Reported,
   not banked.**

### Branch B — "our churn" (the branch that DOES show a gradient)

Our version was **not** held constant. `ladder_games.ourver`: the v54 window ran our
**v159 / v160 / v161**; the v55 window ran our **v161 / v162**.

**⭐ WITH THEIR VERSION HELD AT 54 (their bot constant, n=20 games), our own mechanism
metrics fall monotonically across three of our versions:**

| our version | n | our game share | median damage into THEIR core | median our sentinel shots | median our Ti→ammo | median our launchers built |
|---|---|---|---|---|---|---|
| **v159** | 5 | **3/5** | **504** | **28** | **398** | **0** |
| **v160** | 5 | 1/5 | 162 | 9 | 132 | 2 |
| **v161** | 10 | 3/10 | 153 | 16 | 180 | 4 |

and with their version held at 55 (n=20): our v161 **0/5**, median core damage **0**;
our v162 **3/15**, median core damage **0**.

Pooled across both their versions, our four versions read:
**ammo converted 398 → 132 → 112 → 105**, **sentinel shots 28 → 9 → 7 → 7**,
**launchers built 0 → 2 → 4 → 4**, **median damage into their core 504 → 162 → 54 → 0**.
Our launcher production also moved forward: sited at median **d²=85** from their core at
v54-era versions and **d²=8** at v162 — 115 launchers built at v55 against 59 at v54, of
which **104 died**.

**THE CONTROL THAT MUST RUN THE OTHER WAY, AND DOES:** if the 20pp drop were theirs, the
v54 column above would be FLAT across our three versions. It is not — **with their bot
frozen at v54 our share swings 60% → 20% → 30% and our core-damage median falls 504 → 162 → 153.**
Our own churn alone produces a 40pp swing against a constant opponent, which is larger
than the 20pp v54→v55 drop the study was commissioned to explain.

### Why it is NON-DECOMPOSABLE rather than decided

* Outcome: **v54 7/20 (35.0%) vs v55 3/20 (15.0%), diff +20.0pp**, 95% half-width
  **±31.4pp** (two-fixture form, **within-opponent DEFF 1.366** on both arms — correct
  here because the OPPONENT cluster is degenerate: it is the same opponent in both arms,
  while the MATCH cluster survives with exactly 5 games per match).
  **20.0pp sits inside the interval.**
* Match-level: v54 scores `[0.4, 0.2, 0.6, 0.2]`, v55 `[0.0, 0.2, 0.2, 0.2]`; Welch
  t = 1.85 on 4 vs 4 matches (se 0.108) — not significant.
* The reciprocal cut (**our v161 held constant**): opp v54 **3/10**, opp v55 **0/5**,
  diff +30.0pp, 95% half-width **±50.2pp**. Not separable either.
* **Map mix is NOT the explanation:** 13 distinct maps at v54, 12 at v55, 11 shared.
  fjordgate is the largest single shift (1→4 games) and we are 1/5 on it pooled; drumlin
  2→3 and we are 0/5 pooled. Both lean against us in the v55 window but neither carries
  20pp on 3-4 games. **Reported as a residual, not a mechanism.**

**⇒ The honest statement: the 35%→15% drop is not established as anything. What IS
established is (a) their v55 is not more than 7.9pp better than their v54 league-wide, and
(b) our own kill channel against them collapsed monotonically across our v159→v162, with
median damage into their core going 504 → 0.**

---

## 4. Q3 — PIECES

Each piece is one behaviour, ≥2 anchors, a control, and a QUEUE.md/control-tree grep run
BEFORE it was written up. Grepped control tree: **`bots/_v488beltbreak2/`**.

---

### PIECE A — **THE SENTINEL CLOCK: their core-killer arrives at r113-116 and never earlier**
**(THEIRS — attack it. NEW, no QUEUE row covers the opponent-clock read.)**

**MEASURED.** First sentinel build round, p25/median/p75:
**113 / 115 / 116** (Flotte vs Erebus, n=47 at v54 and n=99 at v55 — two versions, one
third-party opponent), and **112-119 median** in our own 40 games. It is sited at
**d² 25-41 from our core** (attack radius r²=32, obstacle-ignoring) and our core's first
damage lands **median +5 rounds later, 27/31 games inside +1..+20**.

**ANCHORS (≥2, file+round):**
* `1eea783c-6aec-4008-a1a9-7fecac59493c_game_1.replay26` (v54, nordkap): sentinel r114 at
  d²=41 → our core first bleeds **r119**; sentinel delivers 738 of the 1,130 HP taken.
* `296cfc4e-66a0-4180-b826-e17c6647153c_game_1.replay26` (v55, ragnarok): sentinel r114 at
  d²=41 → our core first bleeds **r115**; sentinel delivers 828 of 898.
* `67c1942c-7892-4f66-a830-7f5b547bc56f_game_2.replay26` (v54, frostgate): sentinels
  r112/r113/r121 → our core first bleeds **r117**.

**INDEPENDENT CROSS-CHECK on a different code path.** `tools/corpus/replay_autopsy.py`
run on `296cfc4e-66a0-4180-b826-e17c6647153c_game_1.replay26` reports the per-round core
damage trace directly: `first damage r115; (115,18) (117,18) (121,18) (123,18) (125,18)
(127,18) (129,18) (131,18) (133,36) (135,36) …` — **an 18-damage tick every 2 rounds from
r115**, which is one sentinel at `dmg 18, reload 2`, doubling to 36 at r133 when the second
lands. Ledger `{'sentinel': 828, 'gunner': 70} total=898 MATCH`. The mechanism is legible
in the raw event stream, not only in the aggregate.

**CONTROL (runs the other way, and is COLLIDER-EXPOSED — read the caveat):** in the
**9 of 40** games where they built NO sentinel we won **6 (66.7%)**; in the 31 where they
did we won **4 (12.9%)**; diff +53.8pp against a ±37.6pp half-width (within-opponent DEFF
1.366) → separated. **Length-controlled at turns ≥150 (so both arms had the chance to reach
the r115 clock): no-sentinel 5/7 vs with-sentinel 4/27.**
⚠ **The collider: "no sentinel" is partly CAUSED by our early kill** (four of the six
no-sentinel wins ended at r86 / r158 / r165 / r167, at or barely after the clock). **The
non-collider evidence for this piece is the OFFSET and the damage share, not this cut.**

**AGAINST OUR DOCTRINE (`<r300` kill):** perfectly aligned — the piece says the window
**r0-r110 is free of their only reliable core-damage engine**, and everything they can do
before it is gunner chip at 7 dmg/shot. This is an argument to front-load, not to defend.
Our own analogue is **`#92` (decouple the first sentinel from the eco clock)** — theirs is
not eco-coupled at all; it is a fixed clock, which is the whole finding.

---

### PIECE B — **HARD CAP OF FOUR BUILDER BOTS, NEVER REPLACED**
**(THEIRS — attack it. NEW; adjacent to `#45` KILL THE BUILDER but that row is about
point-blank creepers, not about an opponent with no replacement policy.)**

**MEASURED.** Builder bots ever built, per game: **4 in 40/40 rated games vs us**;
**4 in 55/55 vs Erebus at v54**; 4 in 110/120 at v55 (8 games with 5, 2 with 8).

**THE CONTROL, and it is the decisive one — it MUST be able to come out the other way.**
If the "4" were a replacement policy rather than a cap, games where their builders DIE
would show >4 built. **In 8 of the 40 games at least one of their builders died (once, all
four). In 0 of those 8 did they ever build a fifth.**

**ANCHORS:**
* `a0584316-208b-47f3-b526-2e97eb1187f7_game_1.replay26` (v54, fjordgate): their four
  builders die at **r41, r47, r63, r68**. Builds before r68: `{builder_bot:4, harvester:2,
  conveyor:4, launcher:1, gunner:6}`. **Builds after r68: `{}` — nothing, for 90 rounds.**
  No sentinel was ever placed (the r115 clock never fired). **We won at r158.**
* `296cfc4e-66a0-4180-b826-e17c6647153c_game_2.replay26` (v55, fjordgate): builders die
  **r17, r30**; they never exceed 4 built; they still won at r102 on 150 gunner shots.
  **This is the honest counter-anchor: killing 2 of 4 is not enough.**
* `f53fa799-c1fd-47c5-8916-270faccd97cf_game_4.replay26` (v55, drumlin): builder dies
  **r122**, no fifth ever built.

**AGAINST OUR DOCTRINE:** ⛔ **our builder melee CANNOT execute this piece — a builder bot
is not a building, so `attack()` can never target one** (engine fact, already banked at
`#79`/`#45`). Only a turret removes a builder. The piece therefore *is* an argument for
forward turret production in the r20-r110 window — i.e. it converges on
**`#21`/`#22`/`#86`** (the sustained-turret-production family, already re-priced to the top
of the offensive stock) and **`#93`** (point-blank core-sniper gunner), and gives them an
opponent-specific payoff: against Flotte, four builder kills before r110 removes their
economy, their repair, their heal, AND pre-empts Piece A's sentinel by construction.

---

### PIECE C — **THEIR SABOTEUR WORKS IN THE BAND OUR INTRUDER DETECTOR CANNOT SEE**
**(THEIRS — defend it. NOT NEW: this is `QUEUE.md #79`, whose GREP already cites the
`doctrine.py:118` "The Flotte Experience 1745" incident and already names the
`d²>36` cap. Cited to `#79`, refined with a per-opponent number.)**

**MEASURED, against the LIVE control `bots/_v488beltbreak2`:**
* Their builder attacks: **1,479 across 40 games; 971 (65.6%) on our HARVESTERS**, 418 on
  our conveyors, **0 on our turrets, 0 on our core**.
* Distance of the attacked tile to OUR core: **median d²=34 (v54) / 37 (v55)**.
* Against our coverage map — `INTRUDER_CORE_DSQ = 20` (`doctrine.py:126`) recall, then
  `_nearest_home_intruder` up to the hard cap `if self.core.distance_squared(ep) > 36:
  continue` (**`main.py:636`, still present in `_v488beltbreak2`**) — their attacks fall:
  **inside d²≤20: 567 (38.3%) · band 20<d²≤36: 214 (14.5%) · BEYOND THE CAP: 698 (47.2%).**

**So very nearly half of everything they do to our economy happens where the detector is
blind by construction.** `#79` measured (all-teams, 5.01M builds) that 55.5% of harvesters
sit at d²_own > 36; this is the same defect measured **against the opponent the incident
note names**, on our own games.

**ANCHORS:** every one of the 40 games carries attacks past the cap; the two densest are
`cfe44920-1964-4b53-9a7b-b94bdf4eb790_game_1.replay26` (v55, archipelago) and
`67c1942c-7892-4f66-a830-7f5b547bc56f_game_4.replay26` (v54, midgard) — the two games with
the largest belt loss (233 and 345 of their gunner shots respectively, 20+ of our conveyors).

**CONTROL:** the same measurement against the recall band must be able to come out the
other way, and does — at v55 **42.3%** of their attacks land INSIDE `d²≤20`, i.e. squarely
in the covered band. The blindness claim is about the 47.2% beyond 36, not about the whole
population.

**AGAINST OUR DOCTRINE:** defensive, so it carries `DEFENCE_ADMISSION_BAR:
r300_crossing_non_regression`. It composes with `#79`'s already-re-priced part (c),
"extend detection to where the economy actually is".

---

### PIECE D — **THE EJECTION FARM BITES US EARLY AGAINST FLOTTE, NOT LATE**
**(THEIRS — defend it. NOT NEW: this is `QUEUE.md #59` (DON'T GET FARMED). Cited to `#59`;
what is new is that `#59`'s own cost cut, which found no cost, is INVERTED for this
opponent.)**

**MEASURED.** Their launchers pick up OUR builder bots and throw them:
**774 throws (v54) + 481 (v55) = 1,255 across 40 games**, median **34 (v54) / 32 (v55) per
game**, max **198 in one game**. **All 1,255 move our bot to a LARGER d² from their core —
774/774 and 481/481, zero exceptions.** Origin median d² 25-29 → destination median d² 82-85.

**⭐ THE REFINEMENT THAT MATTERS.** `#59`'s archive cut (all opponents, `ourver`≥125, 8,274
throws) reports **60.1% land after r150, median r209 — "past our median kill (174) AND our
median death (187), i.e. mostly in games already decided"**, and rates the row a "measured
ANNOYANCE, not a shown leak". **Against Flotte the distribution is the other way round:
median r120 (v54) / r131 (v55); 66.8% / 61.1% land BEFORE r150; 75.1% / 72.3% land before
r174.** Their launchers are up by **median r6.5-7**, long before their first gunner
(median r20.5-23.5), so the envelope exists from the opening.

**ANCHORS:**
* `1eea783c-6aec-4008-a1a9-7fecac59493c_game_5.replay26` (v54, drakkarfjord): **198 throws**,
  first at **r23**.
* `d0a8e564-009e-4242-80dd-a7ee6324e4e3_game_4.replay26` (v54, archipelago): **107 throws**,
  first at **r22**, median **r107** — inside the window, and we lost at r167.
* `296cfc4e-66a0-4180-b826-e17c6647153c_game_4.replay26` (v55, drumlin): **72 throws**,
  first at **r14**, median **r94**.

**CONTROL:** the counter-direction is in the same measurement — **our own** launchers throw
our own bots FORWARD (58 at v54, 135 at v55; 106 of 135 toward their core at v55), so the
decoder is not simply labelling every long move as an enemy eviction. And against Erebus,
Flotte's throw rate is **median 0 per game** — the farm is reactive to an approach, not a
script, which is why it never showed up in a third-party profile.

**GREP against the live control:** `LOKI_EXILE_PENALTY = 24` (`doctrine.py:1485`) is
referenced **once**, at `raid.py:1130` — the RAID station scorer. `grep -ci launcher eco.py`
= **4**, none of them a block or a penalty in `_bfs_direction`. **`#59`'s finding — the
envelope is unguarded in the walk path — still holds verbatim against `_v488beltbreak2`.**

**AGAINST OUR DOCTRINE:** `#59` is already cross-cited with `#70`; this study supplies the
opponent-specific cost that `#59` says the row needs ("length-controlled evictions per
OUR-builder-round in r0-150"). It does not by itself clear that bar — but it moves the mass
of the dose into the window where the bar is measured.

---

### PIECE E — **THEIR BUILDER BOTS BLOW THE CPU BUDGET ~48 TIMES A GAME, AND THE RATE
TRACKS *OUR* BUILD VOLUME**
**(THEIRS — a candidate weapon. NEW. Nothing in QUEUE.md targets opponent CPU: `#5`/`#17`/
`#38`/`#43` are the crash-induction family, which is *exception* induction, a different
mechanism — a CPU timeout does NOT destroy the unit.)**

**MEASURED.** `BotOutput.tled` events, resolved to the unit that owns them:
* Against us: **993 (v54) + 938 (v55) = 1,931 TLE'd unit-rounds over 40 games (48.3/game).**
* **100% of them are BUILDER BOTS.** Gunner/sentinel/launcher/core TLEs: **0**.
* **Our own TLEs across the same 40 games: 0.**
* Against Erebus: **5,117 over 175 games (29.2/game)**, again builder-only.

**THE DOSE RELATION (MEASURED on two independent surfaces):** Pearson r between the
OPPONENT's total build count in a game and Flotte's TLE'd rounds is **0.589 (n=40, vs us)**
and **0.621 (n=175, vs Erebus)**. Game length is a confounder (r=0.446 / 0.563); the
**partial correlation controlling for length is 0.462 and 0.377** respectively, and the
fully length-normalised form (builds/round vs TLE/round) is **0.331 and 0.330 — the same
number on both surfaces.** We build **61.9 entities/game** against Erebus's **35.4**, and
Flotte TLEs **48.3/game against us vs 29.2/game against Erebus**.

**CONTROL:** the direction must be able to invert and does not — the same decoder reads
**0** TLEs for our units in all 215 games and **0** for Erebus in all 175, so "TLE" is not a
constant column that validates anything. And the correlation is positive on two different
opponents, two different version pairs, and survives length adjustment on both.

⚠ **EYEBALL on the CAUSAL step.** Correlation is measured; *why* their builder's turn cost
scales with entity count is inferred (a per-turn scan over nearby entities/tiles is the
obvious candidate and is exactly what a 10ms budget punishes). **A dose leg is required
before this is a weapon.** The mechanism metric would be *their TLE'd builder-rounds per
our-entity in r0-150*, and the falsifier is a flat dose-response.

**AGAINST OUR DOCTRINE:** on-programme and cheap — it is a *free rider on economy we
already build*, not a new plank, and a TLE'd builder is a builder that does not repair,
does not plant the r115 sentinel (Piece A) and does not eat our harvesters (Piece C). It
composes with Piece B: their four builders are already the bottleneck; freezing them is the
same target by a second route.

---

### PIECE F — **OUR ONLY CHANNEL INTO THEIR CORE IS ONE SENTINEL, AND WE FUND IT WITH A
16-AMMO FLOOR** *(OURS — the self-audit half.)*
**(NOT NEW as a plank: `#21`/`#22`/`#86` own turret production and `#96` owns un-silencing
melee against siege turrets. Recorded here because the opponent-specific number is
extreme.)**

**MEASURED, 40 games:** all **10,926 HP** we have put into a Flotte core came from
`sentinel`. `gunner` = 0. `builder_attack` = 0 of **1,779** builder attacks. We convert a
median of **100-198 Ti/game** to ammo against their **881-1,010**; `AMMO_FLOOR = 16`
(`doctrine.py:963`) is roughly one sentinel shot. Our sentinels die **45** times; theirs
**13**. Their siege sentinel sits at d² 25-41 of our core and `LOKI_QUIET_ON = True`
(`doctrine.py:1687`) silences the only builder verb that could touch it — which is exactly
what **`#96`** proposes to carve out.

**CONTROL:** the zero is not an instrument artefact — the same attribution path reports
**14,441 HP of gunner damage into OUR core** in the same 40 games, so the `gunner`→core
channel is readable and simply empty on our side.

---

## 5. Q4 — TARGET PRICING

**Measured facts only.** At the 2026-08-20T08:32:59Z ratings (`ladder_games.tsv` /
`league_matches.tsv`, same pairing slot) we are **1774.43** and they are **1892.32**, a gap
of **+117.89**, giving an expected game share **E = 0.3366** and, under the exact ladder rule
`delta = 32×(S−E)`: **5-0 = +21.23 · 4-1 = +14.83 · 3-2 = +8.43 · 2-3 = +2.03 · 1-4 = −4.37 ·
0-5 = −10.77**. **Break-even is 1.68 games of 5.** Our measured share is **3/20 = 15.0%** at
their v55 and **10/40 = 25.0%** across v54+v55, so the *expected* value of a Flotte pairing
at current form is **−5.97 Elo/match (v55 form)** to **−2.77 (pooled form)**, and the
realised value is worse: **the eight v54+v55 matches netted −43.98 Elo, and all eleven
Flotte matches on record net −61.17.** A targeting decision therefore needs a plank that
moves our share past **1.68/5**, i.e. **+3.7pp to +18.7pp of game share** depending on which
baseline is believed — not a win-rate claim, because a 2-3 already pays **+2.03** while a
3-2 pays **+8.43**; margin is the currency. **The one number that would justify aiming here
is Piece A's: their core-damage engine does not exist before r113, and our own v159 (median
504 damage into their core, 3/5) is proof from our own record that this opponent's core is
reachable — 20 rated games ago.**

---

## 6. REFUTED, AND RETAINED SO NOBODY RE-DERIVES THEM

1. ⛔ **"They never heal their core."** I formed this from our own 40 games, where their
   core is healed in only 7/20 (v54) and 6/20 (v55). **FALSE.** Against Erebus they heal
   their core in **142 of 175 games, 60,868 HP total, max 2,584 in a single game.** They
   heal it when it is damaged; against us it is usually never damaged. **The near-zero was
   a selection effect of our own failure to hit it, not a property of their bot.** (This is
   what the core-heal positive control in §0 was for.)
2. ⛔ **"Their v55 is a step up that explains the 35%→15% drop."** Their league-wide game
   share is **49.52% at v54 vs 47.94% at v55** (n=210 and 705 games, ALL opponents) and
   their profile against a pinned Erebus v148 is identical on every script constant. The
   improvement is **excluded above +7.9pp**.
3. ⛔ **"Their builder is a lone dormant plant-and-guard infiltrator" (the `#79` shape).**
   Not at v54/v55. Their builders are **four continuously-acting economy raiders**, and
   **971 of 1,479 attacks (65.6%) hit our harvesters** rather than sitting dormant. The
   `#79` *counter* (turret-backed removal, detection past d²=36) is the part that applies;
   the *offensive* plant-and-guard template does not describe this opponent.
4. ⛔ **"They rush our core with builders."** **0 of 1,479** of their builder attacks landed
   on our core footprint across 40 games. Their core damage is 100% turret.
5. ⛔ **"The brief's `5-0 pays +10.79`."** See §1. **5-0 pays +21.23; +10.77 is what a 0-5
   costs.**
6. ⚠ **Reported, not banked:** the coarse behavioural drift between Flotte v54 and v55
   across ALL 175 Erebus games (builder attacks 6.6→45.9/game, TLE 9.5→38.3/game) is
   **confounded by Erebus's own v143→v169 churn and by median game length rising 134→162**.
   The pinned v148 cell shows no such drift. Do not quote the unpinned means.

---

## 7. LEDGER ROW (for `move-mining-ledger.tsv`)

```
2026-08-20	The Flotte Experience	55	40	docs/research/REPLAY-STUDY-flotte-v55-2026-08-20.md
```

*(`games_covered = 40` counts the RATED games vs us at their v54+v55, which is the ledger's
unit. A further 175 third-party Flotte games — vs Erebus at v54/v55 — were decoded as the
branch-separating control and are not counted in that field.)*
