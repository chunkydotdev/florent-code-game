# Clankers — no-confound corpus + FIRST OBSERVED LOSS — 2026-08-07

**Version tags (rule 2):** target = **Clankers v1** (`teamAVersion`/`teamBVersion: 1`
— still their only observed version, now 15 games read). Opponents:
**Leviathan v26** and **O(1) v10**.

**Corpus (10 games, 2 ladder matches):**

| match id | seats | score | created (Z) | our bot present? |
|---|---|---|---|---|
| `024d13d6-e0f5-4d29-819f-b1d02bc15fa8` | A = Leviathan v26, **B = Clankers v1** | 0–5 Clankers | 2026-08-07T20:12:43 | **no** |
| `5792d8fa-f3aa-41e2-9821-cfba0dd35f11` | **A = Clankers v1**, B = O(1) v10 | 1–4 O(1) | 2026-08-07T21:02:43 | **no** |

> **OUR-VERSION CONFOUND: GONE.** Neither match contains an OpenSverige bot. Both
> seats alternate for Clankers (B in one match, A in the other). Every statement
> below is measured against two third parties, and the eight watch items from
> `clankers-classification-2026-08-07.md` §5 are tested verbatim.

**Elo at read time** (from the `.meta.json`): Clankers 1694.90 → **1722.30** after
beating Leviathan, 1723.67 → 1722.30 after losing to O(1); **36 matches played**.
Leviathan v26 1674.48 → 1650.60 (479 matches). O(1) v10 1789.46 → **1786.10**
(280 matches) — the highest-rated bot we have decoded.

**Parser:** `scratchpad/clank2.py` (extends the tonight-scratch `decode.py`) plus
`rep1–rep7.py`. Turret counts deduped by entity id; launcher throws attributed at
d²≤2 including diagonals; `core_deliv × 10 == titaniumCollected` **holds on
20/20 team-sides**. Independent second check: core damage ledger
`500 + 4×core_heals − (turret_dmg + builder_dmg)` closes to within 26 HP on
10/10 Clankers-core ledgers (residuals 2, 2, 26 on the three kills).

---

## 0. VERDICT BLOCK

### 0.1 Watch-item scorecard

| # | Watch item | Verdict | One-line evidence |
|---|---|---|---|
| 1 | Gunner = counterbattery or standing picket? | **REVISED → reactive counterbattery, and conditional** | 18 gunners / 10 games; **0 ever precede an enemy turret** (8/8 games with a gunner); 17/18 sited at d²≤2 of a live enemy turret, 14/18 with it on the facing ray; **2 games with enemy forward turrets and no gunner answer at all** — `5792d8fa` g3 while broke (Ti 3–22), `024d13d6` g5 while solvent (Ti 95–330), so the suppression trigger is **not** purely income. "Picket" is the wrong word. |
| 2 | Launcher ring standing or threat-driven? | **REVISED → income-gated, threat-scaled** | 17 launchers, **439 ejections, 439/439 enemy builders, 439/439 AWAY from Clankers' core**. Built early (r11–r65) when solvent; **zero launchers in the 2 games where Ti sat at 0–22** — and those are 2 of the 4 losses. |
| 3 | Siege fires on an r95–125 schedule? | **REFUTED** | First forward sentinel (d²≤32 to enemy core): **r7, r7, r10, r20, r32, r41, r77, r236**. In 3 games it precedes any enemy turret. Clankers is an **early forward-sentinel siege bot**, structurally the same opening family as our own x3r0/v68 lineage. |
| 4 | Heal-tank trigger + economy cost | **CONFIRMED and quantified — the single most important number in this read** | Core heal rate tracks incoming core damage to within 2% in all 7 games their core lived, and falls short in all 3 games it died. Predicted death round from the deficit: 220/395/385 vs actual **219/393/365**. Ti cost: 31–42% of lifetime income in the lost games. |
| 5 | Tiebreak behaviour | **NOW OBSERVED — they have no late game** | `5792d8fa` g5 ran to r1000, lost on `titanium_collected` **2,290–0**. 82% of lifetime Ti (2,446 of ~2,970) converted to ammo for one sentinel; ended 30 Ti stored, 4 ammo, **0 harvesters ever built**. |
| 6 | Any barrier or splitter? | **CONFIRMED-AS-CLASSIFIED** | 0 barriers, 0 splitters in 10/10 games (now 0 in 15 games). Both opponents build barriers. |
| 7 | Conveyor siphon — designed tap or artifact? | **REVISED → emergent but systematic, and it has a starvation failure mode** | 196 cross-team stacks (1,960 Ti), **100% into Clankers, 0 out**, in 3 of 5 Leviathan games. Mechanism identified: their router puts a conveyor orthogonally adjacent to an ore tile **facing away from the ore** *before* the harvester exists. Enemy ore → free siphon. Unclaimed ore → in `5792d8fa` g5 they built 6 such terminals and **never placed the harvester**, delivering 0. |
| 8 | Small-map zero-harvester rule? | **REVISED → not a map rule** | Zero-harvester games here are 16×16, 20×26 and 14×18 — all vs O(1); on a 16×16 vs Leviathan they built 4 harvesters. Driver is enemy turret coverage of their near-side ore plus the ammo drip outbidding the 20 Ti harvester. |

### 0.2 How O(1) v10 beats this sub-type (headline)

**Forward-gunner saturation on the core, plus builder chip on the conveyors to
hold the heal budget at passive-income-only.** Not one lever — two, applied as
one plan, and the arithmetic is exact.

Clankers runs a **proportional heal controller**: builders heal damaged friendly
assets at a rate that tracks incoming damage almost perfectly, bounded by
titanium. Measured over all 10 games:

| match | g | core dmg/round | core heal HP/round | net | core died? | predicted death round | actual |
|---|---|---|---|---|---|---|---|
| 024d13d6 | 1 | 0.00 | 0.00 | +0.00 | no | — | — |
| 024d13d6 | 2 | 0.09 | 0.10 | +0.01 | no | — | — |
| 024d13d6 | 3 | 2.35 | 2.37 | **+0.01** | no | — | — |
| 024d13d6 | 4 | 0.02 | 0.02 | +0.00 | no | — | — |
| 024d13d6 | 5 | 2.81 | 2.87 | **+0.06** | no | — | — |
| 5792d8fa | 1 | **8.39** | 6.12 | **−2.27** | **YES** | r220 | **r219** |
| 5792d8fa | 2 | 1.77 | 1.94 | +0.17 | no (they won) | — | — |
| 5792d8fa | 3 | **3.92** | 2.66 | **−1.27** | **YES** | r395 | **r393** |
| 5792d8fa | 4 | **6.64** | 5.34 | **−1.30** | **YES** | r385 | **r365** |
| 5792d8fa | 5 | 0.01 | 0.02 | +0.00 | no (lost tiebreak) | — | — |

The kill condition is a single inequality:

> **`core_damage_per_round > 4 × clankers_heals_per_round`, sustained.**

and their heal rate has a hard ceiling set by titanium. **Observed ceiling with a
suppressed economy: 1.53 heals/round = 6.12 HP/round** (`5792d8fa` g1). Passive
income alone would allow 2.5 heals/round = 10 HP/round, but heal spend competes
with rebuild + ammo spend, so ~6 HP/round is what they actually achieve when
their delivery is zero.

O(1) produces 6.6–8.4 dmg/round on the core from **3–5 gunners planted at d² 1–9
from the Clankers core between r12 and r60**, each firing on consecutive rounds
(gunner reload 1 ⇒ 7 dmg/round each; verified from fire rounds
21,22,23,24,25,26,28,31 for one gunner). Simultaneously it lands **231–575
builder attacks per game, 64–81% of them on Clankers conveyors**, which forces
the heal controller to spend on repair instead of the core and holds delivered
titanium at 0–540.

**Delivered titanium is the single best predictor of the result in this corpus.**
Clankers delivered 0 / 1,500 / 0 / 540 / 0 → **L / W / L / L / L**.

### 0.3 Pre-registered exploit candidates — test results

**(i) "Two simultaneous damage sources break the core heal-tank equilibrium
(~60 rounds)."**
→ **PARTIALLY CONFIRMED, mechanism restated; the "~60 rounds" figure is REFUTED.**
Source *count* is the wrong variable. Two simultaneous sources delivering
2.35 dmg/round (`024d13d6` g3) were absorbed for 223 rounds with the core back at
500 HP. Four–five sources delivering 8.39 dmg/round killed in 219. What matters is
sustained **dmg/round vs 4 × heals/round**. Time-to-kill is
`500 / (dmg_rate − heal_rate)`, which was **219–393 rounds** in all three observed
kills, never ~60. A second source helps only because it raises dmg/round.

**(ii) "Sustained cheap chip converts their builder pool to medics and zeroes
their economy."**
→ **CONFIRMED.** O(1)'s 231/401/575/467 builder attacks pulled 72/329/184/215
Clankers heals onto conveyors and left them at 0/1,500/0/540 delivered. In the
three games where chip + turret coverage held delivery near zero, the heal
ceiling collapsed to ~6 HP/round and the core died. In the one game where
Clankers got 1,500 Ti delivered (`5792d8fa` g2) their heal rate never approached
the ceiling and **they won**.

**(iii) A third mechanism, and it is the real headline:** the two above are one
plan. O(1) does not out-range, out-heal, or counterbattery them; it **raises the
core damage rate above their titanium-limited heal throughput while
simultaneously capping that throughput at passive income**. Neither half alone
was sufficient in this corpus: Leviathan applied 2.35–2.81 dmg/round with a
*healthy* Clankers economy and went 0–5.

**Practical target for us:** to kill a Clankers core we need roughly
**≥10 dmg/round sustained on the footprint while their delivery is under ~500 Ti
for the game.** One sentinel at d²≤32 firing every other round is ~9 dmg/round —
right on the line and not enough on its own if their economy is alive. Adding one
inline gunner (7/round) or ~2 builder attacks/round clears it comfortably. Note
that a lone forward sentinel is also exactly what their counterbattery gunner
answers in 4–6 shots, so the second source has to be built to survive that.

### 0.4 Probe spec: **GO** — but a different probe than the classification imagined

`clanker_probe` is worth building; **the shape has changed**. It is not "picket +
delayed siege". Reproducible spec, all items measured in ≥8/10 games:

1. **Opening:** 5 builder bots, one per round, r0–r4, on core-adjacent tiles.
   (10/10 games; one game shifted to r0–r5.)
2. **Standing forward sentinel:** first builder walks to a passable tile at
   d² 16–25 from the enemy core and builds a sentinel facing it as soon as 30 Ti
   allows. **Proactive** — it precedes any enemy turret in 3/10 games
   (r7, r7, r10). Timing is walk-distance-gated, not schedule-gated.
3. **Proportional heal controller (the class signature):** each idle builder
   heals the most-damaged friendly asset on an orthogonally adjacent tile;
   aggregate heal rate must track incoming damage 1:1 in HP (4 HP per 1 Ti),
   capped by the titanium budget. Priority order observed: core ≥ turret >
   conveyor. Total 3,304 heals in 10 games.
4. **Reactive counterbattery gunner:** when an enemy turret is in vision, build a
   gunner at d²≤2 of it, facing it, and fire until dead. Kill cost is exactly
   `ceil(HP/7)` — **4 shots for a 25 HP gunner, 6 for a 40 HP sentinel**, both
   observed repeatedly. **Never** build a gunner when no enemy turret exists.
5. **Income-gated launcher ring:** 1–3 launchers at d² 4–17 from own core, built
   r11–r65 when Ti allows; throw any adjacent enemy builder to a passable tile
   further from own core. Suppress entirely when Ti < ~50.
6. **Ammo drip:** one 30 Ti conversion timed to the first turret coming online,
   then 4–10 Ti every 1–2 rounds, holding balance in 4–40. (First conversions
   r4–r38; 9–247 calls/game.)
7. **Conveyor-first economy router:** chain from core outward, terminal conveyor
   orthogonally adjacent to an ore tile **facing back toward the core**,
   harvester placed on the ore afterwards. Chain-wiredness 100% whenever the
   chain is intact.
8. **Preserve the defects — they are the exploit surface:** no barriers, no
   splitters, no tiebreak logic, and an ammo drip that outbids the 20 Ti
   harvester (so a sentinel in a stalemate eats 100% of passive income and the
   economy can never restart).

### 0.5 Class label

**"Picket sub-type, NOT probe-covered (~1/3 ouroboros)" does NOT survive.**
Probe *coverage* is unchanged (still uncovered — ouroboros' gunners creep at
builders and never answer turrets, cad_probe is the inverse launcher polarity,
nothing in the instrument set models a heal controller). But the *label* is wrong
in two of its three parts: the gunners are not a picket, and the siege is not
delayed.

Proposed replacement:

> **HEAL-TANK SIEGE** — a standing early forward-sentinel siege carried on a
> proportional heal controller, with a reactive counterbattery gunner and an
> income-gated launcher-ejection ring. Co-labels: **conveyor-first econ**,
> **no-tiebreak**.

Confidence: **HIGH** on mechanisms (measured in 15 games across 3 opponents and
both seats), **MEDIUM-HIGH** on the label — the one thing still unobserved is an
opponent that builds no turret at all, so watch item 1's strict form is still
NOT EXERCISED.

---

## 1. MATCH `024d13d6` — Leviathan v26 0–5 Clankers v1

| g | map | cores (A/B) | ore | wall | rounds | end |
|---|---|---|---|---|---|---|
| 1 | 14×18 | (6,4) / (6,12) | 12 | 18 | 204 | core kill r203 |
| 2 | 18×18 | (2,14) / (14,2) | 8 | 18 | 245 | core kill r244 |
| 3 | 16×16 | (0,0) / (14,14) | 14 | 50 | 223 | core kill r222 |
| 4 | 25×15 | (11,3) / (11,10) | 24 | 8 | 342 | core kill r341 |
| 5 | 26×26 | (5,5) / (19,19) | 38 | 208 | 152 | core kill r151 |

Clankers = **team B** in all five (opposite seat to the confounded corpus).
`024d13d6` g4 is the **same map** as the confounded corpus g4 (25×15, cores
(11,3)/(11,10)) with the seats swapped — a useful direct comparison: there
Clankers heal-tanked for 690 rounds and lost; here they built a forward sentinel
at r20 and won at r341.

### 1.1 What Leviathan v26 actually is (as observed)

Not a rush in these five games. **Econ + gunner bot: 4–11 builders, 3–17
harvesters, 2–11 gunners, ZERO sentinels, ZERO launchers, zero builder attacks
(0 in all five games).** Its gunners are overwhelmingly a *home* picket
(d²_own 9–41); it planted only **1–2 forward gunners per game** (r8, r15, r20,
r31, r33/r36) at d² 1–9 from Clankers' core.

Result: it never generated more than **2 simultaneous damage sources** on the
Clankers core, at 0.00–2.81 dmg/round. Clankers' heal controller absorbed all of
it (net +0.00 to +0.06 HP/round in every game) and their core finished at **500
HP in all five**, having taken 0 / 21 / 525 / 7 / 427 total damage.

Leviathan also lost the ore war *while winning it*: it built 6/6/10/17/3
harvesters to Clankers' 6/2/4/7/7, and delivered 660/1,710/750/2,980/740 — but
lost 196 stacks (1,960 Ti) to the siphon (§1.3) and had no answer to a sentinel.

### 1.2 How Clankers won all five

One mode, five times: **standing forward sentinel at d²_enemy 16–25 → heal the
sentinel → replace it when it dies → 45–78 sentinel shots into the core.**

| g | 1st fwd sentinel | fwd sentinels total | sentinel shots | launcher at d²_enemy=1 before kill | core kill |
|---|---|---|---|---|---|
| 1 | **r10** @(2,8) | 4 | 78 | r114 @(6,3), r181 @(5,4) | r203 |
| 2 | r41 @(2,9) | 3 | 75 | — | r244 |
| 3 | r32 @(6,1) | 6 | 46 | — | r222 |
| 4 | **r20** @(6,3) | 7 | 54 | r293 @(10,3) | r341 |
| 5 | r77 @(5,11) | 3 | 45 | — | r151 |

The **launcher planted at d²_enemy = 1 immediately before the kill** recurs
(3 of 6 Clankers core-kills in this corpus, plus 2 in the confounded corpus) —
**CONFIRMED-AS-CLASSIFIED**.

Counterbattery in this match: 11 gunners, all after an enemy turret existed, all
at d²≤2 of one, and lethal at minimum cost — e.g. `g2` gunner r24 @(12,2)
facing SE killed the Leviathan gunner at (13,3) in **4 shots** (25 HP / 7 dmg);
`g4` gunner r10 @(11,8) killed the r8 forward gunner in **3 shots** plus chip.
In `g5` Clankers built **no gunner at all** against a forward gunner that dealt
427 damage over 115 rounds — they simply healed it off and won by siege.

### 1.3 The siphon (watch item 7), fully characterised

| g | cross-team stacks | direction |
|---|---|---|
| 1 | 66 | Leviathan → Clankers |
| 3 | 38 | Leviathan → Clankers |
| 4 | 92 | Leviathan → Clankers |
| 2, 5 | 0 | — |

**196 stacks = 1,960 Ti, 100% into Clankers, 0 out.** Mechanism (new): Clankers'
router builds a conveyor orthogonally adjacent to an ore tile with its **output
facing away from the ore, toward its own core**, and does so *before* the
harvester goes down. Examples from g1 where they own the ore: conveyor (7,14)
face N at r21 → their own harvester (7,15) at r23; conveyor (5,15) face N at r30
→ harvester (5,16) at r33. Where Leviathan owns the ore, the identical terminal
silently accepts the enemy harvester's output: conveyor (4,7) face S at r81
adjacent to Leviathan's harvester (3,7) built r17; conveyor (12,4) face S at r85
adjacent to Leviathan's harvester (12,3) built r35; conveyor (8,0) face W at r194
adjacent to Leviathan's harvester (9,0) built r17.

So: **not a designed tap, but a systematic and free consequence of a
conveyor-first-then-harvester router.** It fires whenever the enemy holds ore
they can reach. Its failure mode is in §2.5.

---

## 2. MATCH `5792d8fa` — Clankers v1 1–4 O(1) v10 (THE LOSS)

| g | map | cores (A/B) | ore | wall | rounds | end | winner |
|---|---|---|---|---|---|---|---|
| 1 | 16×16 | (3,3) / (11,11) | 12 | 64 | 219 | core kill r218 | O(1) |
| 2 | 18×18 | (2,14) / (14,2) | 8 | 18 | 282 | core kill r281 | **Clankers** |
| 3 | 20×26 | (9,6) / (9,18) | 22 | 74 | 393 | core kill r392 | O(1) |
| 4 | 25×25 | (5,5) / (18,18) | 30 | 4 | 365 | core kill r364 | O(1) |
| 5 | 14×18 | (6,4) / (6,12) | 12 | 18 | **1000** | **titanium_collected 2290–0** | O(1) |

### 2.1 What O(1) v10 is (first classification)

**Forward-gunner saturation + builder chip, over a deliberately tiny fixed
economy, with a heal-tank tiebreak fallback.** Opening is identical in all five
games:

- **r0–r3: 4 builder bots** (6 in g3/g5, extras at r9/r10). Never more.
- **r1–r6: 2 harvesters**, a third at r17–r93 in 4/5 games. **2–3 harvesters and
  5–14 conveyors, in every game** — the economy is a fixed small constant, wired
  67–100%, never grown.
- **r8–r26: the first forward turret at d² 1–9 from the enemy core**, then 3–7
  more; plus one forward *sentinel* in 4/5 games. Home picket gunners come late
  (r55–r252) at d² 1–4 from their own core.
- **Builder attacks are their primary weapon: 231 / 401 / 575 / 467 / 9 per
  game, 64–81% of them on enemy conveyors.** (Contrast Leviathan: 0.)
- Ammo: 422–1,866 Ti converted; the gunners are run hot.
- **Heal-tank fallback (g5): 1,191 core heals at a metered 1.25/round for 1,000
  rounds** while banking 3,346 Ti. They will happily take a tiebreak.

O(1) is a genuine threat to the x3r0/v68 shape too — a forward gunner swarm at
d²≤9 plus 400–575 conveyor attacks is precisely the anti-forward-sentinel,
anti-conveyor-spam pattern.

### 2.2 g1 (16×16) — the cleanest kill

- r4: O(1) takes 2 harvesters; r17 a third. Clankers builds **zero harvesters all
  game** — all 6 near-side ore tiles end up inside an O(1) turret's attack radius.
- r12/r13/r14: O(1) plants gunner (6,6) d²=8, sentinel (7,7) d²=18, gunner (4,7)
  d²=9 from the Clankers core.
- r16/r20: Clankers answers with counterbattery gunners at (6,5) and (7,6) —
  kills the (6,6) gunner in **4 shots** (r20) and the (7,7) sentinel in **6**
  (r26). The counterbattery works exactly as advertised.
- r21/r32: O(1) simply replaces them, closer — (2,5) d²=2 and (5,4) d²=1. Those
  two are **never killed** and fire 99 and 55 core shots.
- r42 onward: Clankers Ti pinned at 0–15. **No launcher is ever built**, so O(1)'s
  builders walk in freely (42 approach-samples at d²≤9) and land 231 attacks.
- Steady state: 8.39 dmg/round in, 6.12 HP/round healed. Core 500 → 448 (r75) →
  385 (r83) → 285 (r176) → 99 (r200) → dead **r218**. Predicted r220.

Clankers' whole-game spend: **427 Ti on heals out of ~1,010 lifetime income
(42%)**, 14 conveyors, 0 harvesters, 76 Ti of ammo.

### 2.3 g3 (20×26) and g4 (25×25) — the same shape, slower

- g3: Clankers plants **two forward sentinels at r7 and r9 — before O(1)'s first
  turret (r10)**. O(1) answers with a single gunner at (11,9) d²=5 at r11 that
  fires 76 core shots and never dies, adds four more forward gunners r120–r155,
  and grinds 575 builder attacks (463 on conveyors) — **39 of Clankers' 49
  conveyors destroyed, 0 Ti delivered all game**. Clankers builds **no gunner at
  all** (Ti 3–22 throughout). 3.92 in vs 2.66 healed; core dead r392 (predicted
  r395). O(1) heal-tanked its own core through the two sentinels (112 core heals)
  and never dropped below 402.
- g4: O(1) plants gunners (8,8) r24, (7,8) r26 and sentinel (6,10) r25, all
  d²≤16, then (3,5) r60. The (7,8) gunner alone fires **183 core shots**.
  Clankers builds one counterbattery gunner (r36, kills (8,8) in 4 shots) and two
  launchers (21 ejections), loses **46 of 58 conveyors** to 445 conveyor attacks,
  delivers 540. 6.64 in vs 5.34 healed; core dead r364 (predicted r385).

### 2.4 g2 (18×18) — Clankers' only win, and it proves the mechanism

Same O(1) plan: 5 forward gunners + 1 forward sentinel at d² 5–13, r20–r37; 401
builder attacks, 368 on conveyors. Two things went differently:

1. **Clankers got an economy.** 5 harvesters (first r21), 30 wired conveyors,
   **1,500 Ti delivered** — the only game in the match above 540. That funded 482
   heals, of which **329 went to conveyors**: only 3 conveyors died all game
   despite 368 attacks on them (heal = +4 HP per 1 Ti vs attack = 2 dmg per 2 Ti,
   a 4:1 exchange in the healer's favour).
2. **O(1)'s core damage rate stayed low** — 1.77/round vs 1.94 healed. Clankers'
   core never left 480–500.

Then Clankers won it the normal way: sentinels at (15,7) r236 and (14,7) r252,
d²_enemy 16, **38 shots = 684 damage** against O(1)'s 40 core heals; launcher
planted at (15,4) d²_enemy = 1 at r255; core dead r281.

### 2.5 g5 (14×18, r1000) — the tiebreak, and the starvation loop

The first Clankers game ever to reach r1000. It is a total structural failure and
it explains their ceiling:

- r7: forward sentinel at (3,8), d²_enemy 25 — before O(1)'s first turret (r8).
- r8/r10: O(1)'s two forward gunners. Clankers' counterbattery gunner (r11)
  kills one in **4 shots** (r15); the other dies r23. **O(1) never rebuilds a
  forward gunner.** Total damage to the Clankers core for the rest of the match:
  **14 HP.**
- r15: Clankers' launcher at (9,7). It then ejects O(1) builders **360 times
  between r16 and r996**, always the same two victims, always to the same tile
  (13,10). The ejection ring works perfectly — and wins nothing.
- **The starvation loop:** their sentinel fires every ~4 rounds at 10 ammo;
  passive income is 10 Ti per 4 rounds. **247 ammo conversions totalling 2,446 Ti
  = 82% of their ~2,970 lifetime income** went straight into 239 sentinel shots.
  Stored Ti sat at **20** and ammo at **4** from r200 to r900. A harvester costs
  20 Ti and was never affordable in practice.
- They laid **19 conveyors, 100% wired, and 6 of them terminate orthogonally
  adjacent to an ore tile facing home** — (7,3)/(6,2)/(6,1)/(8,0)/(11,3)/(11,2)
  next to ore (7,2)/(5,1)/(9,0)/(12,3)/(12,2) — **and never placed a single
  harvester**, on a map where only 1 of their 6 near-side ore tiles was under an
  O(1) turret. Two of their builders logged 989 and 992 moves without building.
  *Why the harvester step never fires is* **UNCERTAIN** *from the replay; the
  ammo drip pinning Ti at 20 is the most likely gate, but not proven.*
- O(1) meanwhile out-healed the sentinel trivially (1,191 core heals = 1.25/round
  = 5 HP/round vs the sentinel's ~4.3 dmg/round), farmed a flat **250 Ti per 100
  rounds** from r100 to r1000, and finished **2,290 delivered / 3,346 stored**.

**Tiebreak verdict: Clankers has no tiebreak game.** They lose criterion 1
(titanium delivered) 0–2,290 and would lose criterion 2 (harvesters alive) 0–3.

---

## 3. METHOD NOTES

- Parser: `scratchpad/clank2.py` + `rep1.py`…`rep7.py` (this session's
  scratchpad). Built on the tonight-scratch `decode.py`, extended with
  `DistributeResources` (field 4), per-round core-HP tracking, chain-wiredness
  snapshots every 25 rounds, and a builder-bot position history so heal/attack
  targets resolve correctly.
- **Turret dedupe**: all counts by entity id. Rotations counted separately —
  Clankers rotated 0–3 times per game (max 3), consistent with the classification's
  rotation-discipline note.
- **Launcher throws**: `moveBuilderBot` with `d²(from,to) > 1`, thrower = a live
  launcher at d²≤2 **including diagonals**. **439/439 throws attributed** —
  the corrected diagonal rule returned no NONEs anywhere in this corpus.
- **Core footprint**: heals and attacks on any of the 4 footprint tiles resolve to
  the core. Missing this initially mis-binned ~1,200 heals as unresolved; it is
  the single easiest way to under-count a heal-tank.
- **Sanity check 1**: `core_deliv × 10 == titaniumCollected` — **20/20 team-sides
  pass**.
- **Sanity check 2** (new, recommended for any heal-line read): the core damage
  ledger `500 + 4×heals_on_footprint − (Σ turret shots × dmg + 2 × builder
  attacks)` should equal final core HP. Residuals here: +2, +2, +26 on the three
  Clankers core deaths; ≤ +9 elsewhere. This validates fire attribution, heal
  attribution and footprint geometry in one number.
- **Turret cadence, measured from raw fire rounds** (worth pinning, several
  damage-rate estimates elsewhere may need it): a **gunner fires on consecutive
  rounds** (reload 1 ⇒ **7 dmg/round**), not every other round; an unconstrained
  **sentinel fires every 2 rounds** (46/46 observed gaps = 2 for `024d13d6` g1
  sentinel #264 ⇒ **9 dmg/round**). The `5792d8fa` g5 Clankers sentinel instead
  shows gaps of **4** (224/236) — that is the ammo-starvation loop in §2.5 visible
  directly in the cadence: 10 ammo/shot against 2.5 Ti/round passive halves its
  damage output to 4.5/round.
- **Not measured / UNCERTAIN:** why the harvester step fails after the terminal
  conveyor is placed (§2.5); whether Clankers would build a gunner against an
  opponent with no turret at all (still unobserved — watch item 1's strict form);
  Leviathan v26's reputation as a fast rush-family killer is **not** reproduced in
  these 5 games (it built zero sentinels, zero launchers and zero builder attacks,
  and killed nothing).

---

## Addendum (2026-08-08): 024d13d6 seat-mapping re-audit

**Trigger.** `docs/research/v73-production-read-2026-08-08.md` measured Leviathan
**v25** in a fresh ladder match as a clear forward-gunner rush (r9-r12 plants at
d²≤5 of our core in 3/5 games, 100% of our core damage from gunners) and flagged
this match's "Leviathan v26 = ZERO rush, 0 sentinels/launchers/builder-attacks"
side finding as suspicious — a seat inversion would produce exactly that misread,
crediting the aggressor's (Clankers') behaviour to the passive side's (Leviathan's)
label.

**Version-tag header.** Corpus:
`replay_archive/024d13d6-e0f5-4d29-819f-b1d02bc15fa8_game_1..5.replay26` +
matching `.meta.json` (all 6 files present, verified on disk before reading).
Cross-reference: `docs/research/v73-production-read-2026-08-08.md` (today's
Leviathan v25 read). Our live version: v73 "Eir 7" = `bots/_v84g/main.py`, md5
`cbb0b8b449110f89be9765028fbf8c54` (re-verified on disk, unchanged) — not itself
in this corpus (neither seat is OpenSverige here). No bot source directories
were read for this audit; it is pure replay decode against
`tools/replay_schema.md` + `tools/replay_census.py`, plus a scratch instrument
script (`seat_audit.py`, read-only, discarded after use — not committed) that
re-parses the wire format independently of any assumption in the original
deliverable's (now-dead) scratchpad walkers. `meta.json`:
`teamAId → Leviathan v26` (1674.48→1650.60, 479 matches),
`teamBId → Clankers v1` (1694.90→1722.30, 36 matches), `scoreA:0 scoreB:5`,
`winnerId == teamBId`.

### (a) Verdict per game: **CORRECT in all 5 games — not inverted**

Four independent instruments, all measured fresh from the raw replay wire
format (no reliance on the original walker's output):

1. **Score/winner match.** Replay `winner` field is **B** in all 5 games
   (`core_destroyed` in all 5). `meta.json`: `scoreB:5`, `winnerId == teamBId`
   (Clankers). Replay-B = winner = Clankers, all 5 games. ✔ agrees.
2. **Clankers heal-tank-siege fingerprint, reproduced on replay-B to the exact
   round and tile.** Team B's first forward sentinel and first d²=1 launcher
   plants match the original deliverable's own §1.2 table **exactly**, digit
   for digit, independently re-derived: g1 sentinel r10 @(2,8) [doc: r10
   @(2,8)]; g2 r41 @(2,9) [r41 @(2,9)]; g3 r32 @(6,1) [r32 @(6,1)]; g4 r20
   @(6,3) [r20 @(6,3)]; g5 r77 @(5,11) [r77 @(5,11)]. Launcher-at-d²=1 events:
   g1 r114 @(6,3) and r181 @(5,4) [doc: identical]; g4 r293 @(10,3) [doc:
   identical]. Team B: 0 barriers, 0 splitters, 100%-chain-wired end state, all
   5 games. ✔ agrees.
3. **Leviathan gunner-rush + TLE-on-builders fingerprint, found on replay-A.**
   Team A plants a forward gunner at d²≤9 of the *enemy* (replay-B) core in
   4/5 games — g2 r20 @(13,3) d²=1; g3 r33 @(13,13) d²=2; g4 **r8** @(12,9)
   d²=1 (earlier than v25's fastest, r9); g5 r31 @(21,17) d²=5 — and at d²=20
   in g1 (r15 @(4,8)). Team A never builds a sentinel or launcher in any of
   the 5 games (0/5 each). The one game with any TLE activity, g4, shows
   **8 TLE unit-rounds, all on entity #5, kind `builder_bot`, all on team A**
   (r288-r292, r307-r309) — 0 on team B — matching the "TLE forfeits land on
   builders" shape from the v25 read (n is far smaller here, 8 vs 335, but the
   direction and target class agree). ✔ agrees.
4. **Damage-ledger reproduction.** Re-attributing every `FireTurret` event to
   the live gunner/sentinel entity standing on its `from` tile (0 unattributed
   shots in any of the 5 games) and filtering to shots landing on the enemy
   core footprint: team-A gunner hits on team-B's core total **0 / 3 / 75 / 1
   / 61** shots × 7 dmg = **0 / 21 / 525 / 7 / 427 HP** — this reproduces the
   original deliverable's own §1.1 sentence ("having taken 0 / 21 / 525 / 7 /
   427 total damage") **exactly**, digit for digit, from an independent
   re-parse. Team-B's damage to team-A's core is **100% sentinel** in every
   game (68/54/41/47/43 core-landing sentinel shots; 0 gunner or builder-melee
   hits on the core footprint from B in any game) — team B's own gunners fire,
   but never land on A's core (consistent with the "reactive counterbattery"
   role, not a siege role). ✔ agrees.

All four instruments agree, in all five games: **replay-A = Leviathan v26,
replay-B = Clankers v1, exactly as the original deliverable had it.** No
inversion, no re-attribution needed.

### (b) Consequence for the original CLANKERS findings: **all unaffected**

Since the mapping is correct, every Clankers-attributed finding in §0-2 of
this deliverable was measured on the right team. Explicitly, per claim:

| Claim | Status | Basis |
|---|---|---|
| Heal-tank controller law (core heal tracks dmg to within 2%) | **UNAFFECTED** | Team B is confirmed Clankers; not independently re-measured here (out of this audit's scope), but the seat it was measured on is correct |
| Standing forward sentinel siege, d²_enemy 16-25 | **UNAFFECTED, and independently re-confirmed** | Re-derived first-sentinel round+tile for team B matches the original's published table exactly in all 5 games (instrument 2 above) |
| Income-gated launcher-ejection ring, launcher-at-d²=1-before-kill | **UNAFFECTED, and independently re-confirmed** | Re-derived launcher plants at d²=1 for team B match the original's published events exactly (g1, g4) |
| Reactive counterbattery gunner siting (d²≤2 of a live enemy turret) | **UNAFFECTED** | Consistent with instrument 4: team B's gunner fire never lands on the enemy core, i.e. it is not being used as a siege weapon — behaviourally consistent with a counterbattery role, though the d²≤2-of-enemy-turret siting itself was not re-derived here |
| Conveyor siphon (196 stacks, 100% into Clankers) | **UNAFFECTED (not independently re-verified this pass)** | Team identity underneath the claim is correct; the siphon *mechanism/direction* itself is outside this audit's scope (it concerns which team's ore feeds which team's network, not which replay-letter is which team) and was not re-derived here |
| Zero barriers / zero splitters (10/10 games incl. the other match) | **UNAFFECTED, and independently re-confirmed for this match** | Team B: 0 barriers, 0 splitters, all 5 games (census) |
| Delivered-titanium tiebreak/outcome pattern | **UNAFFECTED** | Team B wins all 5 by `core_destroyed`, matching `scoreB:5` |

### Corrected — really, clarified — Leviathan v26 behavioural profile

The seat mapping was never the problem; the **side-finding's framing** was too
compressed and reads as a stronger claim ("ZERO rush behaviour") than the
original deliverable's own body text supports. §1.1 of this document already
reports "it planted only 1–2 forward gunners per game (r8, r15, r20, r31,
r33/r36) at d² 1–9 from Clankers' core" — this audit reproduces those same
round numbers independently (instrument 3) and confirms them. What v26
actually does in these 5 games, stated precisely:

- **A genuine but weak forward-gunner rush attempt, present in all 5 games**:
  first forward gunner at **r8 (g4), r15 (g1), r20 (g2), r31 (g5), r33 (g3)**,
  landing at **d²=1 (g2, g4), d²=2 (g3), d²=5 (g5), d²=20 (g1)** from the
  enemy core — matching, and in g4's case (r8) *beating*, v25's r9-r12 timing
  against a different opponent today.
- It never escalates: **0 sentinels, 0 launchers, 0 builder attacks in all 5
  games** (independently re-confirmed, not a decode artifact — team B's
  corresponding counts are non-zero in every category, so this isn't a
  parser blind spot). Total gunners built per game: 18/8/13/20/4, of which
  only 1-2 per game are forward-sited; the rest sit at d²_own 9-41 as a home
  picket.
- **The rush is fully neutralized by Clankers' heal-tank, not absent.** Damage
  delivered to Clankers' core: 0/21/525/7/427 HP across the 5 games — versus a
  core with 500 HP and a heal controller that (per §0.2 of this doc) tracks
  incoming damage to within 2% up to a titanium-gated ceiling. v26's peak
  output, 2.81 dmg/round in g5, sits far under the "4× heal rate" kill
  threshold this deliverable establishes elsewhere. So the *behaviour*
  (forward gunner plant, early rounds) is the same shape as v25's; the
  *outcome* (near-zero core damage, 0-5 result) is a function of the opponent,
  not the absence of aggression.
- v26 **lost all 5 games (0 wins, 0 core kills)** in this corpus, so the
  family's "median 64-round kill" claim (from
  `docs/research/wave-ghost-first-read-2026-08-07.md`) is **not tested here at
  all** — it can only be measured on v26 wins, and none exist in this match.
  This match cannot confirm or refute the family kill-speed claim either way.

**One-line answer to the era question:** the zero-sentinel/zero-launcher/
zero-builder-attack datum is **real, not a seat-mapping artifact** — the seat
mapping was correct in all 5 games — but "ZERO rush behaviour" oversold it:
v26 attempts the same forward-gunner opening as v25 (sometimes earlier: r8 vs
r9-12), just with lower commitment (1-2 forward gunners vs v25's much heavier
and more sustained pressure) and against a heal-tank opponent that fully
absorbs it, producing a near-zero-damage line that looks passive by outcome
but isn't passive by intent.

**Surprise worth flagging to the next reader.** Re-deriving the exact
round/tile/damage figures from the raw wire format and finding them match the
original deliverable's own published numbers digit-for-digit (instruments 2
and 4 above) is itself the strongest evidence available that the original
walker's team/seat resolution was sound — the suspicion in the v73 read was
reasonable to raise (a seat inversion is a real, previously-seen failure mode
per the v73 doc's own "Seat-map verification" self-check), but it does not
apply here. The lesson generalizes: a "does nothing" side-finding should be
checked against the source document's own body text before it's treated as
suspicious — here the body text already had the answer.
