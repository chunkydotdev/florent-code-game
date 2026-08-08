# v72 bleed map B — the non-CAD-family band (2026-08-08)

Read-only replay decode. No bots edited, no matches run, nothing downloaded.
Corpus: 7 archived ladder matches = **35 games**, all played 2026-08-08
00:32Z–03:25Z with **OpenSverige v72 "chainwatch"** live. Record across the
corpus: **10 W – 25 L** (21 of the 25 losses are `core_destroyed`, 4 are
`titanium_collected` at r1000; 6 of the 10 wins are core kills, 4 are
tiebreaks).

| match | opponent | score (us) | maps |
|---|---|---|---|
| `98e2c1fc` | kladde chatte tville (och oss) **v75** | 0–5 | lighthouse, nordkap, atoll, jackpot, eider |
| `3de9f5e0` | kladde **v75** | 1–4 | archipelago, heart, meander, snowflake, nordkap |
| `067dcff2` | Ouroboros **v8** | 0–5 | lighthouse, drumlin, saga, heart, snowflake |
| `fead7e71` | Leviathan **v25** | 2–3 | jackpot, moonrise, heart, meander, snowflake |
| `8996dfc2` | Leviathan **v25** | 3–2 | nordkap, antler, hive, heart, eider |
| `6cd1a9a3` | 0033 **v43** | 2–3 | drumlin, nordkap, fjordgate, meander, antler |
| `072c3897` | Coreflood **v63** | 2–3 | nordkap, jackpot, lighthouse, snowflake, archipelago |

Maps identified by exact `(w, h, walls, ore)` match against `maps/*.map26`;
zero ambiguous, zero UNKNOWN. Every number below is parsed from the replays
(method notes at the end). Where a claim is inference rather than measurement
it is marked **UNCERTAIN**.

---

## 1. Synthesis — ranked mechanical changes for the replacement candidate

The corpus splits the band into **two kill geometries**, and v72 answers
neither:

| geometry | opponents | where their core-shots come from | answerable by |
|---|---|---|---|
| **standoff ring** | kladde v75, 0033 v43, Coreflood v63 | 78% / 73% / 57% of shots from tiles at **d² > 13** of our core (kladde: 729 of 1176 shots from **d² = 25 exactly**) | a home **sentinel** only (gunner r²=13 cannot reach) |
| **adjacency plant** | Ouroboros v8, Leviathan v25 | **100%** of shots from d² ≤ 13; 751/881 and 830/1856 from **d² = 1** | home gunner + builder melee |

And one law holds across all five opponents — the ray-coverage law, now
measured on 322 enemy siege turrets:

| opponent | siege turret we ever shot at → median lifetime | never shot at → median lifetime |
|---|---|---|
| kladde v75 | **10** rounds (n=49) | **65.5** (n=78) |
| Ouroboros v8 | 17 (n=5) | 87.5 (n=44) |
| Leviathan v25 | 11 (n=9) | 23.0 (n=72) |
| 0033 v43 | 9 (n=9) | 56.5 (n=12) |
| Coreflood v63 | 2 (n=13) | 37 (n=31) |

(consistent with the spitball's covered 8–11 / uncovered 81–105 numbers, now
across five opponents instead of one.)

### Ranked levers

**L1 — Never pave the core's 8 heal seats. [NEW]**
The 8 orthogonal neighbours of our 2×2 footprint are the *only* tiles from
which a builder can heal the core. v72 fills them with its own
conveyors/splitters. Averaged over the last 100 rounds before each core death:

| game | incoming HP/rnd | healed HP/rnd | max heal acts in any one round | seats blocked by OUR buildings |
|---|---|---|---|---|
| `3de9f5e0` g1 (archipelago) | 23.22 | 18.38 | 6 | 7.76 / 8 |
| `3de9f5e0` g4 (snowflake) | 18.72 | 13.90 | 5 | **8.00 / 8** |
| `072c3897` g1 (nordkap) | 18.14 | 13.16 | 4 | 6.38 / 8 |
| `98e2c1fc` g1 (lighthouse) | 17.45 | 13.28 | 4 | 4.81 / 8 |
| `3de9f5e0` g3 (meander) | 16.92 | 12.10 | 4 | 5.57 / 8 |
| `98e2c1fc` g5 (eider) | 16.20 | 11.04 | 3 | **8.00 / 8** |

Every one of those is a **4.2–5.2 HP/round shortfall = one healer**. Across all
21 core deaths we absorb a mean **59%** of incoming (10.82 in, 6.39 healed).
The arithmetic that matters: a heal is +4 HP for 1 Ti, one act per adjacent
builder per round (measured: 9 builders alive → 4.78 acts/rnd; the per-round
maximum ever observed is 6). **8 free seats = 32 HP/round, above every siege
DPS in the corpus (max 23.22).** The geometry is winnable; v72 gave it away.
Prescription: at most 1–2 seat tiles carry a delivery input into the core; the
other 6 are a permanent no-build zone, and any friendly building already on
one gets `destroy()`ed (free, no cooldown) the round the core takes fire.
This is a *different* pave ban from the E2b ore-pave-ban in the graft queue —
complementary, not the same tiles.

**L2 — Lift the lifetime builder-spawn ceiling; spend the bank. [NEW]**
`bots/opp_v72/main.py` caps *lifetime* spawns at `MAX_BUILDERS(5) +
REPLACEMENT_MAX(8) + SURGE_EXTRA(5) = 18`. Observed exactly:

- `067dcff2` g5 (snowflake): spawns at r0–4, 63–131, 300–304 = **18, then never
  again**. Builder population 0 from r200 to r999 while the bank climbed to
  **9,982 Ti**. Lost the r1000 tiebreak 10,130 vs 22,680.
- `067dcff2` g3 (saga): **18 spawns**, last at r432, then 568 dead rounds with
  **8,298 Ti** banked and 2 builders alive.
- `067dcff2` g1 (lighthouse): builders reach **0 by r200**; the last 100 rounds
  before the core died had **zero heal actions** against 3.78 HP/round. The
  core death is directly caused by having no bodies, not by their firepower.
- Map/seat hardcodes make it worse: `nordkap_home_a` (seat (9,6)) caps the base
  at **4**. Our nordkap record in this corpus is **0–3 in seat A**
  (`3de9f5e0` g5, `6cd1a9a3` g2, `072c3897` g1) and **1–1 in seat B**.

Secondary trap on the same ring: with the ring paved, `can_spawn` can be false
*everywhere*. Measured `free == 0` over the whole legal spawn set (d² ≤ 8) in
`072c3897` g2 at r100/r200/r300 (jackpot corner seat, ring is only 11 tiles and
we occupied all 11) and `072c3897` g4 at r800/r998.

**L3 — Home ray coverage of the d² = 16–32 belt, with re-facing. [SHARED with
the CAD arm — extended here]**
The CAD arm's "home ray coverage" plank is confirmed and given a target ring.
The cleanest single instance is `6cd1a9a3` g4 (meander, 0033 v43): we had a
home sentinel *plus* 2–3 home gunners for the entire game, and

- their sentinel at **(11,8), d²=16** took 16 of our shots and died in **17
  rounds**;
- their sentinel at **(15,8), d²=25** — a different bearing — took **zero** of
  our shots, fired **132 times**, and lived **264 rounds** to kill us.

Sentinels have **no `rotate()`** (gunner-only in the API), so covering a second
bearing requires either a second sentinel or `destroy()` + rebuild to re-face
(destroy is free and uncapped; rebuild is 30·scale Ti — we banked 300–4,210 Ti
in 7 of the 12 grind deaths). A gunner cannot substitute: from a core seat its
r²=13 does not reach the d²=25 ring at all.

**L4 — Finish the last link, and re-plan it when it breaks. [SHARED]**
The sharpest evidence in the corpus is a same-map, same-seat, same-opponent,
same-version pair 70 minutes apart (heart 28×20, our seat (19,9), Leviathan
v25):

| | `8996dfc2` g4 **WIN** | `fead7e71` g3 **LOSS** |
|---|---|---|
| harvester → core chain at r100 | (26,11)→…→(18,9)→**CORE**, complete by r31 | (15,13)→(15,12)→(16,12)→(17,12)→(17,11)→**(18,11) NOTHING** |
| titanium collected | 410 by r100, 1,290 total | **0 for the entire 417-round game** |
| ammo converted | 1,099 | 274 |
| result | their core dead r274, we lose 1 gunner + 1 sentinel all game | our core dead r416 |

The break is **two missing conveyors (6 Ti)** at (18,11)→(18,10)→core, and it
is still broken at r300 — v72 never re-plans the link. Related failure modes
in the same family: `067dcff2` g4 (heart) freezes delivery permanently at r200
(harvesters wired 0/9, `ti_coll` pinned at 740 for 800 rounds) with six
harvesters that have **no adjacent conveyor at all**, and a mutual two-cell
conveyor loop (3,17)↔(4,17) in `067dcff2` g4. Directed wiredness of our
conveyor field in the losses runs 9/33, 20/37, 4/29 — a third to a half of our
conveyors are dead weight that also consume the pave budget.

**L5 — Ammo floor sized for a standing home turret. [NEW, adjacent to the E1
graft piece]**
Total ammo converted, us vs them, per game: kladde matches 104/1127, 290/866,
626/1734, 596/1738, 1366/1574; Ouroboros 94–750 vs 1,277–3,586. A home
sentinel needs 10 ammo/shot and ~3 shots per ring-turret kill (sentinel 40 HP,
18 dmg); 20 kills across a long game = 600 ammo. Correlation only, but sharp:
of the 9 games where we converted ≥ 1,000 ammo we won **5 (56%)**, against
10/35 (29%) overall.

**L6 — Stop spending builder actions on enemy conveyors. [NEW]**
Our builder attacks by target: `98e2c1fc` g1 — conveyor 198 of 497; g4 —
conveyor 208 of 294; g3 — conveyor 234 of 473. Chipping a 20 HP conveyor at
2 dmg / 2 Ti while the sieging sentinel goes unanswered is the single most
common misallocation in the corpus. The answered/unanswered lifetime table
above prices it.

**L7 — A standing answer to the adjacency plant, not a one-shot. [NEW]**
Ouroboros and Leviathan both **rebuild the same tile** repeatedly: Ouroboros
rebuilt (6,10) at d²=1 in `067dcff2` g4 seven times (r202, 248, 479, 710, 743,
800, 821), Leviathan rebuilt (8,13) at d²=1 in `8996dfc2` g2 nine times
(r205–r343). A builder-melee clear that leaves nothing standing invites the
next plant; a home gunner covering the d² ≤ 9 seats turns each rebuild into a
20 Ti loss for them (their gunner scale is +20%/build).

**L8 (opportunistic, play-the-players) — Leviathan burns CPU. [NEW]**
TLE counts against us, per game: Leviathan **801, 240, 152, 41, 15**;
Coreflood 129, 2, 1; Ouroboros 29, 2; kladde and 0033 zero. Leviathan losing
~0.8 unit-turns/round in a 1000-round game is a measured, exploitable
asymmetry — long games are strictly better against them. **UNCERTAIN** whether
the TLEs are load-dependent (i.e. whether we can *induce* more).

### What is shared with the CAD-family arm, what is new

- **Shared:** L3 (home ray coverage) and L4 (delivery continuity). This corpus
  adds the target radius for L3 (the d²=16–32 belt, gunner-proof) and the
  re-facing requirement (sentinels cannot rotate).
- **New here:** L1 (heal-seat geometry), L2 (spawn ceiling / unspent bank),
  L5 (ammo floor), L6 (builder-attack targeting), L7 (standing vs one-shot
  answer), L8 (Leviathan CPU).

---

## 2. kladde chatte tville v75 — deep dive (Q3)

10 games, we won 1. Elo: they sit ~1,746 vs our ~1,590 — the most valuable
scalp in the corpus.

### 2.1 Their mechanism, end to end

**Opening (r0–r30).** Conveyor *before* harvester: first conveyor r1–r2, first
harvester r5–r10. First sentinel r3–r59 (median r15). First ammo conversion
r12–r31, banked to 100–150 by r25 (`98e2c1fc` g2: ammo 100 at r25 while ours
was 16). They push economy into contested ground early — harvesters inside
d² ≤ 72 of *our* core at r12 (lighthouse), r14 (eider), r80 (nordkap).

**Economy curve.** They out-harvest us roughly 2:1 on open maps and the gap
compounds: eider `98e2c1fc` g5 — their harvesters 6/10/12/13/15 at
r25/50/75/100/241 vs ours 4/5/7/10/3; deliveries per 50 rounds settle at
137–151 for them vs 28–105 for us; final collected 6,190 vs 3,100. Their
directed chain wiredness is near-perfect throughout (63/68 conveyors wired at
r241) against our 30/31 → 9/27.

**Kill pattern — the rebuildable sentinel ring.** They plant sentinels on a
ring at **d² = 13–29 from our core, overwhelmingly d² = 25**, and rebuild them
as fast as we kill them. `3de9f5e0` g4: **25 sentinels built inside d² ≤ 72 of
our core**, ten of them on the single tile (10,9) at d²=25 (r129, 268, 275,
324, 331, 415, 422, …). `98e2c1fc` g3: the tile (9,3) rebuilt six times
(r277, 306, 316, 334, 352, 373), each dying in 10–36 rounds to builder melee —
a grind we lose because their economy funds the rebuilds and ours does not.
Ring DPS at its peak: 23.2 HP/round (`3de9f5e0` g1).

The ring radius is not incidental. d²=25 is **inside sentinel range (r²=32)**
and **outside gunner range (r²=13)** — and it is out of reach even for a gunner
standing on our own core seat. Nothing v72 fields can shoot it.

**Their defence — a heal line that makes their core unkillable by chip.** In
**8 of the 10 games their core finished at exactly 500/500** despite taking
54–830 damage; one finished at 423; the tenth is the game we won. Damage
dealt/healed on their core: 543/543, 54/54, 218/218, 830/830. Their heals
near their own core: 209 of 240, 243 of 250. Our gunner chip (up to 450 fires
in one game) is fully absorbed.

### 2.2 Why v72 loses these

Not one defect — the ring exploits three at once:

1. **No home sentinel, ever.** Our first sentinel goes forward: d² from our own
   core = 18, 36, 157, 162, 36 (`98e2c1fc`), 200, 36, 1, 181, 36 (`3de9f5e0`).
   Sampled every 10 rounds, we hold a sentinel inside d² ≤ 40 of our core for
   **0–28% of the game in 6 of the 10** (0, 0, 2, 2, 28, 28%).
2. **Heal ceiling below their ring DPS** (L1): 4–6 acts/round against 16–23
   HP/round, with 4.8–8.0 of our 8 seats paved by our own conveyors.
3. **Economy 2:1 behind** (L4/L2), so we cannot fund a counter-ring while they
   fund rebuilds. In `3de9f5e0` g4 we still had **4,210 Ti banked** at the point
   the ring was killing us — the money was there, the plan wasn't.

### 2.3 What a bot that takes 2–3 games off kladde does differently

Their core is not killable by our chip damage (8/10 games ended at 500/500),
so **the win condition against kladde is the r1000 tiebreak, not a core kill.**
Our one win (`3de9f5e0` g2, heart) was exactly that: we planted 16 harvesters
and 89 conveyors *into their half* starting r11, suppressed their economy so
badly their first harvester came at **r82**, and won `titanium_collected`
7,350 vs 2,980 with our core untouched all game.

The recipe, in the order the data supports:

1. **Survive the ring** — 6 free heal seats (24 HP/round) exceeds their peak
   23.2. This alone converts `98e2c1fc` g1, `3de9f5e0` g1/g3/g4 and
   `072c3897` g1 from core deaths into round-1000 games.
2. **Two home sentinels, re-faced on demand** onto the live ring bearings —
   answered ring turrets die in a median of 10 rounds vs 65.5 unanswered.
3. **Contest the ore belt from r5**, the way we did in the one win. Their
   opening is conveyor-first and their harvester count is the whole game.

---

## 3. Leviathan v25 — class verdict (Q4)

**Verdict: RUSH. Leviathan v25 is an adjacent-gunner core rush.** Era stamp:
observed 2026-08-08 **02:12Z–03:25Z**, matches `8996dfc2` and `fead7e71`,
10 games, their rating ~1,678–1,685.

Evidence:

- **First gunner planted at d² ≤ 9 of our core** at r5, r10, r10, r11, r11,
  r13, r23, r32, r38, r41 across the ten games — **median r12**. Several land
  at d² = 1 (orthogonally touching the footprint): (11,9) r5 on meander,
  (9,17) r13 on nordkap, (18,10) r14 and (19,8) r42 on heart.
- **Ammo conversion begins at r0** in 8 of 10 games (they bank before they
  build).
- **Two of ten games are pure all-in**: `fead7e71` g3 and `8996dfc2` g4 —
  Leviathan built **zero harvesters and zero conveyors for the whole match**
  (`ti_collected` 0 for both teams in g3).
- Total core-shots on us: 1,856, of which **1,811 are gunner** and 100% come
  from d² ≤ 13; 830 from d² = 1 and 642 from d² = 2.
- They rebuild the plant: (8,13) at d²=1 rebuilt nine times in `8996dfc2` g2.

**Class caveat:** the rush is not always all-in. In 5 of 10 games they ran a
normal economy alongside it (`8996dfc2` g5 — 10 harvesters and 1,120 collected
by r100 *and* gunners at d² = 5 by r38). So the precise class is
**"gunner-adjacency plant, median r14, economy optional"**, not "all-in rush".

**On the v26 anomaly:** v25 is unambiguously aggressive, so the afternoon
family read was *not* wrong-era for v25. The zero-aggression v26 observation vs
Clankers is either a genuine v26 behaviour change or map/opponent-specific.
**UNCERTAIN** which — settling it needs v26 replays, not in this corpus. What
this corpus does settle: **the rollback restored (or retained) the rush**, and
any candidate that meets Leviathan must handle a d²≤2 gunner arriving around
r14.

**Bonus characteristic:** their TLE load is the highest in the corpus (801,
240, 152, 41, 15 unit-turns lost across the five games of `8996dfc2` +
`fead7e71` g5). See L8.

---

## 4. Ouroboros v8 — is it still the seat-lock? (Q5)

**No. The 0-5 vs v72 is not a denial/seat-lock loss — it is an economy loss,
three of five games with our core alive.**

| game | map | result | how |
|---|---|---|---|
| g1 | lighthouse | L r369 | core kill — but with **0 builders alive from r200** and **0 heal acts** in the last 100 rounds against 3.78 HP/rnd |
| g2 | drumlin | L r231 | core kill, gunners at d²=1 and d²=9, 156 shots |
| g3 | saga | L r1000 | **tiebreak**, our core untouched, 11,170 vs 14,930 |
| g4 | heart | L r1000 | **tiebreak**, our core ended at **493/500** after 653 shots; our delivery froze at r200 and `ti_coll` stayed at 740 for 800 rounds; final 740 vs 22,550 |
| g5 | snowflake | L r1000 | **tiebreak**, our core **never touched**, 10,130 vs 22,680, our builders 0 from r200 |

Their build profile is monotonous and confirms the family read: **gunners
only** — across all five games Ouroboros v8 built **zero sentinels and zero
launchers**, reaching 13–17 gunners. 881 core-shots, all gunner, all from
d² ≤ 13 (751 of them from d² = 1). Their economy is what beats us: harvesters
18–20, conveyor wiredness 48/48 to 72/72, delivery locked at 121–125 stacks per
50 rounds for 800 straight rounds in g4 and g5.

**On the r3-divergence / opening-signature mechanism.** Their opening in this
match does not reproduce the v65-era transcript. On lighthouse — the one map
shared with `docs/research/ouroboros-v65-era-reverify-2026-08-07.md` (we held
the opposite seat there) — their v65 first gunner was r11 @(6,6); here it is
**r17 @(10,7)**, relative to their own core (−1,−4), followed by r18 @(9,9),
r31 @(5,10), r45 @(9,3). Their first *core-threatening* build (d² ≤ 13 of our
core) is r57 (drumlin), r83 (snowflake), r202 (heart), and **never** on saga.
This is the same conclusion the v65 re-verify reached — the queue is
perturbable and not a fixed station — with a fresh version pair as evidence.
**UNCERTAIN**, and unresolvable from replays alone: whether the perturbation is
a *function* of our opening signature (that needs the paired-variant probe the
spitball describes, which is a match-running experiment, not a decode).

**On the opening-as-steering lever: the data says it is not where the Ouroboros
Elo is.** Their turrets did not kill us in 3 of the 5 games — our core finished
at 500, 500 and 493. Steering their gunner onto our firing rays would buy those
three games nothing. What loses them is L2 (spawn ceiling: exactly 18 spawns,
then 8–10k Ti sitting idle) and L4 (delivery freeze at r200). Recommendation:
**park opening-steering for Ouroboros; the same five games are addressable by
economy fixes that also pay against everyone else.** g1 and g2 (the two core
kills) are additionally L1/L2 cases — g1 died with literally nobody left to
heal.

Side note on the launcher: in g5 our launcher threw enemy builders **453
times** and their delivery rate never dipped below 120 stacks/50 rounds. High
throw volume bought nothing there.

---

## 5. 0033 v43 — first read

Class: **economy-first, late standoff sentinel.** Harvesters 6/8/10 by
r25/50/75 (drumlin) while building **no turret at all until r109**; ammo banked
50–55 and held. Then, between r58 and r190, sentinels arrive at d² = 2–25 of
our core and grind. All 544 of their core-shots are **sentinel** (zero gunner
shots on our core), **73% from d² > 13**.

Per-game loss mechanism:

- **g2 (nordkap seat A, r113)** — *the closest game in the match*. Their
  sentinels at (7,8) d²=5 (27 shots) and (6,9) d²=13 (16 shots). We had a home
  sentinel + home gunner + launcher standing the whole time, and fired at
  **neither tile** (`our_fires_at_tile = 0` for both). Their core finished at
  **154/500** — we were 154 HP from winning.
- **g3 (fjordgate 10×10, r806)** — economy collapse: our `ti_coll` stops at 260
  at r300 and never moves; their sentinel at (1,4) d²=2 built r468 fired **102
  times** and our first response came at **r668 (+200 rounds)**.
- **g4 (meander, r453)** — the L3 exemplar described in §1: home turrets
  present, wrong bearing, (15,8) d²=25 fires 132 times unanswered.

**Their one pattern:** delay all military spend until the economy is 2:1, then
place a *single* sentinel on an uncovered bearing at standoff range and never
move it.

---

## 6. Coreflood v63 — first read

Class: **conveyor/barrier creep + builder-melee on the core + late sentinel
step-in.** Two signatures nothing else in the corpus shows:

- **Builder attacks directly on our core**: 434 (`072c3897` g1) and **612**
  (g2). Nobody else in the corpus does this at all (kladde 11, everyone else 0).
- **A conveyor wall creeping to touching distance**: conveyors built at d² = 1,
  2, 4, 5, 9, 10 of our core (g1: (10,5) r140, (9,5) r221, (11,7) r644; g2:
  (4,1) r366, (4,2) r287/r361, (4,3) r395/r406).

Then sentinels step into d² = 4–18 from r195–r387 (417 of their 513 core-shots
are sentinel, 57% from d² > 13) and finish.

Per-game:

- **g1 (nordkap seat A, r751)** — sentinels at (10,11) d²=16 → (14,7) d²=16 →
  (13,6) d²=9; our delivery decays from 57 to 21 stacks/50 rounds after r450;
  we healed 4,970 of 5,476 (91%) and lost by 506 HP with **1,491 Ti banked**.
- **g2 (jackpot corner seat (0,0), r1000 tiebreak, 3,460 vs 11,570)** — our
  core survived (1,278 dealt, 1,278 healed) but the **11-tile spawn ring was
  100% paved by our own buildings at r100/r200/r300**, and we lost purely on
  economy.
- **g3 (lighthouse, r424)** — our builder count falls to ~1 in the last 100
  rounds (18 builder deaths) while **1,643 Ti** sits unspent; incoming is only
  5.04 HP/round and we heal 1.74. Two healers would have held it indefinitely.

**Their one pattern:** never contest the middle; creep infrastructure to the
enemy core, chip with builders, and let the economy gap (2–3:1 deliveries)
carry the tiebreak if the kill is slow.

---

## 7. Margin flips (Q2)

Each of the three 2–3 matches turns on one game and one mechanism.

**`fead7e71` (Leviathan v25, 2–3) → g3, heart, seat (19,9).**
Same map, same seat, same opponent version as `8996dfc2` g4 which we **won 70
minutes earlier**. The only material difference is the delivery chain: the win
completed harvester→core by r31; the loss dead-ends at (17,11)→(18,11) with
nothing there, and never re-plans, so we collect **0 titanium in 417 rounds**
and convert 274 ammo instead of 1,099. **Single change that flips it: L4 — a
last-link completion/re-plan pass (two conveyors, 6 Ti).** This is the
strongest causal claim in the document because the counterfactual is an
actually-played game.

**`6cd1a9a3` (0033 v43, 2–3) → g2, nordkap seat A, r113.**
Their core was at **154/500** when ours died. Two sentinels at d² = 5 and 13
did all the damage and we shot at neither, despite holding a home sentinel, a
home gunner and a launcher for the whole game. **Single change that flips it:
L3 — re-face the standing home sentinel onto the live threat bearing** (3 shots
= 30 ammo of the 424 we converted; answered siege turrets die in a median of 9
rounds against 0033). Secondary contributor: the nordkap seat-A base cap of 4
builders (L2) held our heal line to 1.44 HP/round against 6.48 incoming.

**`072c3897` (Coreflood v63, 2–3) → g3, lighthouse, r424.**
Incoming was only **5.04 HP/round** — the weakest siege in the whole corpus to
kill us — and we healed 1.74 because the builder population had collapsed to
~1 while **1,643 Ti** sat in the bank. **Single change that flips it: L2 —
respawn bodies out of the bank under siege** (two healers = 8 HP/round > 5.04,
i.e. the core never dies and the game goes to r1000; we were also out-delivered
241 vs 447, so the tiebreak is **UNCERTAIN** — this flips the core death, not
necessarily the game).

**The Leviathan pair (W vs L, same opponent+version, 70 minutes apart).**
`8996dfc2` (3–2) vs `fead7e71` (2–3). What differed:

| | wins (5 of 10) | losses (5 of 10) |
|---|---|---|
| ammo converted | 342–2,638, **median 676** | 64–358, **median 270** |
| collected by r100 | 220 / 260 / 410 / 540 / 570 | **0** / 70(r75) / 440 / 550 / 830 |
| our unit losses | as low as 1 gunner + 1 sentinel (`8996dfc2` g4) | 5–9 builders + the core |

Ammo separates the two columns cleanly (no overlap); delivery does not — and
that is the useful nuance. The five losses are **two different failures**:

- `fead7e71` g3 and g4 are **chain failures** (0 and 70 collected; harvester
  wiredness 0/3 and 0/3) → no ammo → their r11/r5 plant lives. **L4.**
- `fead7e71` g1, `8996dfc2` g2 and g5 are **well-fed losses** (440/830/550
  collected, wiredness 2/3, 4/5, 3/5): the economy was fine and we still had no
  standing answer to a gunner at d²=1–2 that gets rebuilt nine times. **L3/L7.**

Map/seat is *not* the discriminator — heart seat (19,9) appears once in each
column, with the chain the only material difference.

---

## 8. Per-opponent one-line patterns (Q1 summary)

| opponent (version) | the one pattern across their wins |
|---|---|
| kladde v75 | rebuildable **sentinel ring at d²=25** — gunner-proof by construction — behind a heal line that returns their core to 500/500 in 8 of 10 games |
| Ouroboros v8 | **gunner-only mass** (13–17, zero sentinels/launchers ever) that pins rather than kills; wins on economy, 3 of 5 at the r1000 tiebreak |
| Leviathan v25 | **gunner planted at d²≤2 of our core by ~r14**, ammo banked from r0, rebuilt on the same tile until it sticks |
| 0033 v43 | economy to 2:1 first, then **one sentinel on an uncovered bearing** at d²=5–25, never moved |
| Coreflood v63 | **infrastructure creep to d²=1** plus 400–600 builder attacks on the core, sentinels stepping in late |

---

## 9. Method notes

**Parser.** Fresh stdlib walker in the session scratchpad
(`nf.py` + `rep.py` / `siege.py` / `agg.py` / `endgame.py` / `seats2.py` /
`spawnblock.py` / `spawndeep.py` / `coverage.py` / `chainbreak.py` /
`maps_id.py`), reusing the wire helpers and schema constants from
`tools/replay_census.py` and `GameMap` from
`docs/research/2026-08-07-fanout/toolkit/siege_geometry.py` for map
identification. Scratch only, not committed.

**Gotchas honoured** (`docs/tooling.md` "Replay-decode gotchas"):

- `placeEntity` re-emission on gunner rotation is deduped by entity id — a
  same-id re-emission updates facing/HP and is counted as a rotation, never as
  a new build.
- Launcher throws are detected as `moveBuilderBot` with
  `d²(from, to) > 1`, with the thrower attributed to a live launcher at
  **d² ≤ 2 including diagonals**. (Throw volume is reported but not load-bearing
  for any conclusion here; the one large number — 453 throws by us in
  `067dcff2` g5 — is used only to show it bought nothing.)
- Chain-wiredness is computed **directed**: a conveyor feeds only the tile it
  faces, a splitter the three cardinals that are not directly behind it, and a
  harvester its four cardinals.

**Sanity check.** `core_deliveries × 10 == titaniumCollected` verified for
**70 of 70 team-sides** (35 games × 2), zero mismatches.

**Cross-reference to bot source.** L2's constants were read directly from
`bots/opp_v72/main.py` (the live v72 fetched by the builder arm, md5
`1d2e8045…`): `MAX_BUILDERS = 5`, `EARLY_BUILDERS = 5`, `REPLACEMENT_MAX = 8`,
`SURGE_EXTRA = 5`, `SURGE_TI_FLOOR = 1500`, `SURGE_MIN_RND = 300`,
`REPLACE_TI_FLOOR = 250`, `HUNT_MIN_HEALERS = 2`, plus the `nordkap_home_a`
(cap 4) and `snowflake_home_b` (cap 6) map hardcodes. The 18-spawn ceiling is
predicted by the source and observed exactly in the replays — the two
independent confirmations are why L2 is stated as fact rather than inference.
Read-only; a separate agent owns the v69→v72 delta read.

**Known limits.**

- Every number is from ten opponent-games or fewer per opponent; 0033 and
  Coreflood are five each (first reads, flagged as such).
- Heal-seat occupancy is sampled every 5 rounds over the last 100 before core
  death, so it slightly understates churn (builders can `destroy()` a seat
  conveyor, stand, heal). The measured *ceiling* — max heal acts in any single
  round, 3–6 — is exact and is the number the lever rests on.
- The counterfactuals in §7 are arithmetic on measured rates, not simulated
  games. The `fead7e71` g3 flip is the exception: its counterfactual was
  actually played (`8996dfc2` g4).
