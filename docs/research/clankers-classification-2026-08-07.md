# Clankers classification — 2026-08-07 (PROVISIONAL)

**Version tags (rule 2):** target = **Clankers v1** (`teamAVersion: 1`, their
only observed version). Our live slot at read time: **v68 "chokewall"**
(`teamBVersion: 68`, x3r0's forward-sentinel core-snipe lineage). Decoded from
ladder match **3f024b23-d241-484e-b440-6ee5a883bb30** (Clankers 4–1
OpenSverige, 18:12:43Z→18:16:26Z, 3m43s). Research arm, 5/5 games read.
Parser: `tools/replay_census.py` + a purpose-built event walker; both
turret-dedupe and `core_deliv*10 == titaniumCollected` gotchas honoured
(10/10 team-sides pass).

> ## ⚠ FULL OUR-VERSION CONFOUND — READ THIS BEFORE USING THE VERDICT
>
> **All 5 games in the archive are Clankers vs us, all under v68.** Clankers'
> single most decisive behaviour — a counterbattery **gunner** planted 3–14
> rounds after our forward sentinel appears, in that sentinel's own firing
> line, facing it — is *by construction* a response to a forward sentinel.
> We cannot tell from this corpus whether it is a standing plan or a reaction
> to x3r0's snipe. The same applies to the delayed sentinel siege and to the
> launcher ring. **Every class statement below is PROVISIONAL** and must be
> re-tested against a Clankers-vs-someone-else match (§5).

---

## 1. META

| # | Map | Cores (NW corner) | Terrain | Rounds | End | Winner |
|---|---|---|---|---|---|---|
| 1 | 16×16 | A@(3,3) B@(11,11) | 12 ore, 64 wall | 182 | core kill r181 | **Clankers** |
| 2 | 10×10 | A@(2,2) B@(6,6) | 6 ore, 10 wall | 177 | core kill r176 | **Clankers** |
| 3 | 26×26 | A@(5,5) B@(19,19) | 32 ore, 70 wall | 177 | core kill r176 | **Clankers** |
| 4 | 25×15 | A@(11,3) B@(11,10) | 24 ore, 8 wall | 690 | core kill r689 | OpenSverige |
| 5 | 26×26 | A@(5,5) B@(19,19) | 38 ore, **208 wall** | 315 | core kill r314 | **Clankers** |

- **Seats: Clankers = team A in all five games; we are team B in all five.**
  No seat alternation. Confirmed independently by v68's fingerprint on seat B
  (forward sentinel at dsq 16–32 from the *enemy* core, r3–r23; conveyor spam;
  delivery-freeze).
- Games 3 and 5 share dims and core positions but are different maps (70 vs
  208 walls).
- **Zero r1000 games.** Every game was decided by `core_destroyed`. Clankers'
  tiebreak behaviour is completely unobserved.
- Elo: Clankers 1636.34 → 1654.92 (**+6.48**, 20 matches played). Us
  1567.76 → 1558.54 (282 matches). They sit ~96 Elo above us on far fewer games.

## 2. MECHANISM

### 2.0 Whole-match totals (deduped by entity id)

| | Clankers (A) | v68 (B) |
|---|---|---|
| builder bots created | 44 | 40 |
| gunners (deduped) | **6** | **6** (naive placeEntity count: 63 — 57 rotations) |
| sentinels | 17 | 16 |
| launchers | 11 | 4 |
| harvesters | 21 | 37 |
| conveyors | 124 | 347 |
| splitters / barriers | **0 / 0** | 0 / 0 |
| gunner rotations | **1** (g5 only) | 57 |
| turret shots fired | 263 (189 sentinel, 74 gunner) | 506 |
| Ti→ammo converted | 2,335 | 4,629 |
| builder heals | **2,600** | 290 |
| builder attacks | 145 | 907 |
| **enemy builders ejected by launcher** | **266** | 0 |
| own builders lost | **3** | 8 |
| own conveyors lost | **3** | 19 |

### 2.1 Opening (identical spine, map-size-modulated tail)

**Every game: five builder bots spawned one per round, r0–r4**, at the four
tiles around the core plus one. That is the entire fixed script. What follows
depends on map size:

- **26×26 (g3, g5):** economy first. First conveyor r6/r9, first harvester
  r12/r22. Home turrets do not appear until r37–r59.
- **16×16 (g1):** counterbattery gunner at **r9**, launchers r34/r38, first
  conveyor **r30**, first harvester **r36** — economy delayed ~25 rounds.
- **10×10 (g2):** gunner r18, launchers r25/r28, first conveyor r27,
  **zero harvesters all game** (see §6 anomaly A).
- **25×15 (g4):** first conveyor r24, launcher r47, **zero harvesters all
  game** (see §6 anomaly B).

Builder expansion is map-scaled: 5–6 total on the three small maps, **13–14**
on the 26×26s (extra spawns r29–r224).

### 2.2 Turret geometry — a two-phase, two-radius pattern

Every Clankers turret in the match falls into exactly one of two bands:

**Phase 1 — HOME PICKET (r9–r73), dsq to *own* core 4–25 (≈2–5 tiles):**

| game | unit | r | pos | dsq_own | facing |
|---|---|---|---|---|---|
| 1 | gunner | 9 | (8,6) | 20 | S |
| 1 | launcher ×2 | 34, 38 | (5,8), (8,4) | 17, 16 | — |
| 2 | gunner | 18 | (4,7) | 17 | W |
| 2 | launcher ×2 | 25, 28 | (5,6), (3,5) | 13, 4 | — |
| 3 | launcher, gunner, gunner, launcher | 57, 59, 67, 73 | (9,8),(10,7),(8,10),(5,9) | 13, 17, 20, 9 | —, W, E, — |
| 4 | launcher | 47 | (14,8) | 20 | — |
| 5 | gunner, launcher, launcher, gunner | 37, 43, 48, 57 | (9,8),(4,9),(5,11),(10,8) | 13, 10, 25, 20 | S, —, —, SW |

**Phase 2 — SIEGE (r61–r301), dsq to *enemy* core 16–25** — sentinels placed
exactly inside sentinel range (r²=32) of our core, facing it, plus in two
games a **launcher planted at dsq_enemy = 1** immediately before the kill
(g3 r172, kill r176; g5 r301, kill r314).

- g1: sentinel r124 @(12,7) dsq 16 → 28 shots → core dead r181.
- g2: sentinel r121 @(2,6) dsq 16 → 28 shots → core dead r176.
- g3: sentinel r95 @(19,15) dsq 16, then r159/164/167 → 54 shots from 4
  origins → core dead r176.
- g5: sentinels r105, r127 (both killed by our counterbattery), then r270,
  r279, r297 → 60 shots → core dead r314.
- g4: sentinels r61/r61/r64 — **6 shots all game** (ammo-starved, see §3).

**28 sentinel shots × 18 dmg = 504 ≥ 500.** In g1 and g2 they killed our core
with *exactly* 28 shots and no other damage source — the theoretical minimum,
zero waste.

### 2.3 Ammunition — just-in-time, never a war chest

Uniform pattern: **one 30-Ti conversion timed to the first turret coming
online, then a 4–10 Ti drip every 1–2 rounds forever.**

| game | first convert | amount | first turret | total converted | ammo balance range |
|---|---|---|---|---|---|
| 1 | r10 | 30 | gunner r9 | 498 over 59 calls | 20–40 |
| 2 | r14 | 30 | gunner r18 | 434 over 52 | 20–40 |
| 3 | r60 | 30 | launcher r57 | 652 over 52 | 18–40 |
| 4 | r19 | 30 | launcher r47 | **61 over 7** | 1 (from r98 on) |
| 5 | r38 | 30 | gunner r37 | 690 over 62 | 30–40 |

The balance never leaves 18–40 in the four healthy games — one shot's worth
of headroom, no more. Contrast v68, which caps at 48–72 and banked 3,696 in
g4. Clankers' income goes into *units*, not into an ammo reserve.

### 2.4 Economy — small but perfectly wired

**Clankers' conveyor network was 100% directionally wired to its core at
every 25-round snapshot, in every game.** 124 conveyors, `relay_dir ==
relay` and `harv_dir == harv` throughout. v68's was 27–53% wired
(g1 6/16, g2 0/21, g3 17/62, g4 93/173, g5 31/49) — the known delivery-freeze
defect, visible in all five games.

Delivered titanium (`core_deliv × 10`, sanity-checked against
`titaniumCollected` on all 10 team-sides):

| game | Clankers | v68 | Clankers Ti/round |
|---|---|---|---|
| 1 | 1,410 (5 harvesters) | 630 (3) | 7.7 |
| 2 | **630 (0 harvesters)** | 470 (4) | 3.6 |
| 3 | 3,030 (9) | 1,110 (6) | 17.1 |
| 4 | **0 (0)** | 7,700 (7) | 0 |
| 5 | 3,570 (7) | 2,730 (17) | 11.3 |

In g5 they *banked* rather than spent: 455–993 Ti idle from r154 to r286,
used to fund the second siege wave at r270–301.

### 2.5 The heal line — the signature nobody else in the archive has

**2,600 builder heals across five games** (v68: 290). Targets, by game:

- g1: sentinel ×160, own core ×37, gunner ×6
- g2: **gunner ×131**, own core ×54, conveyor ×30, builder ×4
- g3: conveyor ×97, **gunner ×89**, own core ×18, harvester ×3
- g4: **own core ×1,632**, conveyor ×9
- g5: **gunner ×231**, own core ×74, sentinel ×22

Heal is +4 HP for 1 Ti; a builder attack is 2 dmg for 2 Ti. **A single healer
beats two attackers on both HP and cost.** This is why v68's 907 builder
attacks removed almost nothing (3 Clankers builders and 3 conveyors in five
games) while Clankers' picket gunners survived indefinitely under fire.

### 2.6 Launcher ejection — 266 throws, 100% of them ours, 100% outward

Detected as non-adjacent `moveBuilderBot` updates and attributed to the
adjacent launcher:

| game | throws by Clankers' launchers | victim | direction rel. launcher's core | median dsq |
|---|---|---|---|---|
| 1 | 44 | our builders | AWAY (44/44) | 18 |
| 2 | 8 | our builders | AWAY (7/8) | 20 |
| 3 | 3 | our builders | AWAY (3/3) | 20 |
| 4 | **155** | our builders | AWAY (155/155) | 16 |
| 5 | 56 | our builders | AWAY (56/56) | 16 |

Same bot thrown to the same tile over and over (g4: bot #4 from (15,7) to
(19,7), ~every 4 rounds for hundreds of rounds). This is a **physical
perimeter** — our builder walks in, gets deleted ~4 tiles back, walks in
again. v68 launched 3 times in the whole match, two of them its own bots.

### 2.7 How each game ended

All five `core_destroyed`; no tiebreak chains to report.

- g1 r181 — their sentinel @(12,7), 28 shots from r127.
- g2 r176 — their sentinel @(2,6), 28 shots from r122.
- g3 r176 — their sentinels @(19,15)/(16,15)/(15,16)/(14,19), 54 shots from r100.
- g4 r689 — **our** sentinel @(12,9) + gunner @(11,5) + 61 builder attacks.
- g5 r314 — their sentinels @(20,14)/(19,14)/(20,15)/(16,15), 60 shots from r106.

## 3. HOW THEY BEAT v68

**One mode, four times: they delete the snipe sentinel with a counterbattery
gunner, then out-economy us, then run the same snipe back at us 100 rounds
later off a bigger bank.** This is v68's known loss mode 1 ("snipe dies →
dark") — but delivered by a mechanism the archive has not seen before.

The counterbattery: a **gunner** (20 Ti, 7 dmg, reload 1) placed in the
sentinel's own row/column, facing it. Sentinel HP 40 → **6 gunner shots**.
Six is exactly what was measured in g1, g2 and g3.

| game | our forward sentinel | dmg it did | their answer | our sentinel dies | one-liner |
|---|---|---|---|---|---|
| 1 | r6 @(8,8), 8 shots | 144 | **gunner r9 @(8,6) facing S** (Δ3) | **r27** (6 gunner shots) | **Killed the snipe** in 21 rounds, then out-ground us 1410–630 and counter-sniped from r124. |
| 2 | r3 @(3,7), 11 shots | 198 | **gunner r18 @(4,7) facing W** (Δ15) | **r24** (6 gunner shots) | **Killed the snipe**, then banked 630 Ti *stolen off our own harvesters* (§6-A) with zero harvesters, and counter-sniped from r121. Also a clean small-map-collapse leg (v68 is 4–9 on ≤256 tiles). |
| 3 | r64 @(9,10), 4 shots | 72 | **gunner r67 @(8,10) facing E** (Δ3) | **r73** (6 gunner shots, lived 9 rounds) | **Killed the snipe** — but the game was already decided by grind: 9 wired harvesters from r12 vs our 17/62 wired relays, 3030–1110. |
| 4 | r4 @(12,9), **331 shots** | ~6,500 | **no gunner ever built**; 3 sentinels r61–64 with 61 total ammo → 6 shots | **never** | **Our win.** See below. |
| 5 | r23 @(9,9) + gunner escort r28, 20 shots | 294 | gunner r37 @(9,8) S (we killed it r43), **gunner r57 @(10,8) SW** | **r58 / r63** | **Killed the snipe on the second try**, absorbed two failed siege waves (r105, r127), re-armed, and killed us on the third (r270–297). |

**Is this a new loss mode?** The *outcome* is v68's known mode 1. The
*mechanism* is new to our archive: a cheap counterbattery gunner that
converts our 30-Ti forward sentinel into a 44-Ti trade (gunner + 24 ammo) and
takes our whole game plan off the board before r30 — combined with a heal
line that makes our 907 builder attacks worthless and a launcher ring that
physically evicts our builders. Nothing in the archive matched v68's snipe
this cheaply before.

**Our one win (g4, 25×15, cores 7 tiles apart, r689):**

- The map put our "forward" sentinel at (12,9) — dsq 25 from *their* core but
  **dsq 1 from our own**, i.e. inside our own defended envelope. A gunner
  needs to sit within dsq 13 of it to answer; **Clankers never built one**.
  Their three sentinels (r61–64) bore on it but had 61 lifetime ammo → 6 shots.
- Instead they **heal-tanked**: 1,632 core heals, 83–126 per 50 rounds
  (≈2.4/round) for 690 rounds. Core HP sat at 482–500 from r0 to r610 against
  our sentinel's ~8.7 dmg/round. **2.4 heals/round costs 2.4 Ti/round; passive
  income is 2.5 Ti/round.** They survived on a razor-thin equilibrium funded
  entirely by passive titanium.
- The price: **zero harvesters on a 24-ore map, zero titanium collected, a
  standing balance of 1–20 Ti from r98 to r689, and 1 ammo.** All five
  builders were pinned as core medics. We collected 7,700 to their 0.
- It broke when we added a second damage source: gunner #909 at (11,5),
  dsq_enemy = 1, built r628, plus 61 builder attacks on the footprint from
  r629. Core HP: 498 @r610 → 288 @r653 → 0 @r689.

**The exploit that falls out of this:** their core heal-tank is calibrated to
survive *exactly one* sentinel on passive income. A second simultaneous
damage source on the core breaks the equilibrium immediately, and while they
are heal-tanking they build no economy at all.

## 4. PROVISIONAL CLASS VERDICT

**Nearest class: PICKET — new sub-type: launcher-ejection + counterbattery
gunner, over an econ-first economy, finishing with a delayed sentinel
core-siege.** Co-label: **econ-first**. Confidence in the *mechanisms*:
HIGH (all measured, all five games). Confidence in the *class label*:
**MEDIUM-LOW**, entirely because of the confound.

Why not the other classes:

- **Point-blank gunner battery (orizon):** no. Only 6 gunners in 5 games,
  all at dsq_own 13–20 (home side), never at the enemy core, never massed.
- **Launcher-insertion (cad):** **opposite polarity.** cad throws its *own*
  raiders in; Clankers throws the *enemy's* builders out. Same entity,
  inverted use.
- **Rush (band):** no. First offensive turret r61–r124; first core damage
  r100–r127.
- **Grind (kladde) / econ strangulation (flotte):** no. Every game a core
  kill at r176–r314 (or r689 defending). They never reached r1000; they do
  not play for tiebreaks — as far as we can see, they have no tiebreak game.

**Probe coverage: NOT COVERED.** `ouroboros_probe` is the nearest instrument
and covers roughly a third of the shape (gunner picket over a real economy),
but diverges on all three of the things that actually beat us:

| Clankers mechanism | covered by |
|---|---|
| counterbattery gunner sited in the enemy turret's firing line | **nothing** (ouroboros' gunners creep at builders, don't answer turrets) |
| launcher ejection of enemy builders (266 throws) | **nothing** (cad_probe is insertion, the inverse) |
| builder heal line sustaining turrets and core (2,600 heals) | **nothing** |
| delayed sentinel core-siege at dsq_enemy 16–25 | partially — orizon/ouroboros creep, but with gunners, not sentinels |

If §5 confirms the class against a no-confound match, this warrants a new
instrument (working name: **clanker_probe** — picket ring + heal line +
launcher ejection + r95–r125 sentinel siege). Do **not** build it off this
corpus alone.

## 5. WATCH ITEMS for a no-confound match (Clankers vs anyone else)

1. **Is the gunner counterbattery or standing picket?** Does a gunner appear
   against an opponent that builds *no* forward turret? If gunners only ever
   appear 3–14 rounds after an enemy turret enters vision, and sited in its
   firing line, the counterbattery is a rule and the "picket" label is wrong —
   they are a **reactive counterbattery** class, and every bot in the pool
   that opens with a forward turret is being hard-countered.
2. **Is the launcher ring standing or threat-driven?** Launchers went up
   r25–r73 in all five games. Count ejections against an opponent whose
   builders never approach. If the ring goes up regardless, it is a standing
   perimeter and belongs in the class definition.
3. **Does the siege phase fire on a schedule?** Siege sentinels landed r95,
   r105, r121, r124 (and r61 in g4). Against an econ opponent with no
   pressure applied, does the first siege sentinel still land r95–125? If yes,
   this is a scheduled two-phase bot and the confound is small. If it only
   fires after they have been attacked, the whole offensive half is revenge
   behaviour and the class read changes.
4. **Heal-tank trigger and its economy cost.** g4 shows core heals preempting
   *all* harvester construction on a 24-ore map for 690 rounds. Confirm
   whether "core under damage → all builders heal" is unconditional. If it is,
   it is a first-class exploit: sustained cheap core chip damage turns their
   whole builder pool into medics and zeroes their economy.
5. **Tiebreak behaviour — completely unobserved.** No game reached r1000.
   Find out whether they even have a late game, and whether they finish rich
   (stored Ti) or delivered-heavy.
6. **Do they ever build a barrier or a splitter?** Zero of each in five games.
7. **Does the conveyor siphon (§6-A) recur?** Confirm whether terminal
   conveyors adjacent to enemy-held ore are a designed tap or an artifact of
   losing an ore race.
8. **Small-map behaviour with no snipe to answer:** on the 10×10 they built
   zero harvesters and won on stolen titanium. Is that a map rule or a
   consequence of us taking all 3 contested ore tiles first?

## 6. ANOMALIES

**A. Game 2: 630 titanium banked with ZERO harvesters — siphoned off our own
economy.** Clankers lost the ore race entirely (v68 took 3 of 6 ore tiles at
r7/r8/r20) and then ran a conveyor line to the ore anyway, terminating one
tile short of each enemy-held harvester. 65 cross-team resource moves resulted:

- `harvester/B@(6,2) → conveyor/A@(5,2)` ×27 (from r29)
- `conveyor/B@(7,1) → conveyor/A@(6,1)` ×21 (from r99 — tapping our *transport
  line*, not an ore tile)
- `harvester/B@(6,0) → conveyor/A@(5,0)` ×8, `→ conveyor/A@(6,1)` ×5

Their route `(5,0)→S→(5,1)→S→(5,2)→W→(4,2)→W→core` delivered 630 Ti; our own
3-harvester network delivered 470. **The siphon out-earned the owner.**
Whether this is a designed tap or an emergent consequence of routing toward
contested ore is UNCERTAIN from one game.

**B. Game 4: the heal-tank equilibrium.** 1,632 core heals ≈ 2.4/round vs a
passive income of 2.5 Ti/round, holding a 500-HP core at 482–500 for 610
rounds against continuous sentinel fire — while collecting exactly zero
titanium on a 24-ore map and ending on 7 Ti / 1 ammo. A subsistence defence
that consumes the entire team.

**C. Perfect economy hygiene.** 124 conveyors laid, 100% directionally wired
to their core at every snapshot in every game. We have not measured another
team at 100%.

**D. Near-zero attrition.** Across five games Clankers lost **3 builder bots
and 3 conveyors** (all six in games 4 and 5), against 907 v68 builder attacks
and 506 v68 turret shots. In g1, g2 and g3 they lost nothing but one gunner.

**E. Rotation discipline.** 1 gunner rotation in the entire match (g5); zero
in g1–g4. v68 rotated 57 times, 52 of them in g5 alone — the known bare
nearest-bearing rotate anti-pattern (our piece I, absent from v68). Note for
future parsers: a naive `placeEntity` count gives v68 63 gunners instead of 6.

**F. Clean execution record.** Zero TLE rounds, zero stdout, zero tracebacks
for Clankers in all five games. We TLE'd 2 rounds in g2 and 2 in g4.

**G. Minimum-waste kills.** Games 1 and 2 both ended on exactly 28 sentinel
shots (28 × 18 = 504 ≥ 500) with no other damage source touching the core.

---

**Parser sanity:** `core_deliv × 10 == titaniumCollected` holds on all 10
team-sides (1410/630, 630/470, 3030/1110, 0/7700, 3570/2730). All turret
counts in this document are deduped by entity id; rotations reported
separately (§6-E).
