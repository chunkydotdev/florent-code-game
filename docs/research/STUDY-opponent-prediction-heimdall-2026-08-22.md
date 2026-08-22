# STUDY — OPPONENT PREDICTION over the three Heimdall fixtures (banked verbatim)

**PROVENANCE: builder-commissioned fresh opus agent, s57 2026-08-22 (Magnus
directive: predict their moves and targets). Banked verbatim from the agent
transcript; scratch instruments scratchpad/s57_heim0/pred_*. Consumption
decisions are the builder's, on the coordination tail.**

All controls pass. Here is the study.

---

# OPPONENT PREDICTION STUDY — s57 Heimdall fortress design input

**In-game league analysis.** All terms below (raider, plant, damage, retired) are in-engine mechanics between competing game bots on the simulated grid.

**Fixtures:** three deterministic tapes, 30 cells each = 15 maps × 2 seats, seed inert.
`scratchpad/s57_v630/t_ctrl_f1` (Baltsars = `_v542wave` NOISE_OFF) · `t_ctrl_f2` (Mjolnir NOISE_OFF) · `scratchpad/s57_heim0/t_ctrl_f3` (Sleipnir-v2 = `_v488beltbreak2` NOISE_OFF, 30/30 complete, 0 tracebacks). Our side in every cell is `_v628compose`.

**Scripts (scratchpad only):** `pred_scan2.py` (per-cell decode) · `pred_agg.py` (aggregation) · `pred_ladder.py` (insertion mechanism) · `pred_ctl.py` (controls). Raw: `pred_scan2.json`, `pred_ladder.json`.

---

## Instrument controls — every classifier driven to both verdicts

| # | Control | Result |
|---|---|---|
| C1 | Midline detector on a unit that cannot cross (their static core) | **0/90 cells** register it as crossing — PASS |
| C2 | Same detector, subject swapped to *our* units entering *their* half | populated and different from the their-side column (e.g. f2 auroraveil A: theirs r3, ours r22) — PASS, not hard-wired to one team |
| C3 | Half partition | our core centre in our half **90/90** |
| C4 | Damage sign filter (`delta < 0`) | **1,190 positive-delta HP events** (their heals) existed to exclude, and were — PASS |
| C6 | peck/fire/unknown attribution | all reachable; v2 resolves **6,433/6,433** events, 0 unknown |
| C6b | **Mutation control**: shift the FIRE/BATK round index | shift 0 → 0% unknown; shift ±1 → **98.2%** unknown; shift +5 → **100%** — the labels are not rubber-stamped |
| C7 | Can a core hit be labelled `peck`? | yes — **19 core pecks** exist in f1. So "first core damage is always fire" is measured, not an artefact |
| C8 | Replay-decoded winner vs engine log | **90/90 agree** (found and fixed a 0-vs-1-indexed winner bug) |
| C10 | Origin team of shots landing on our core | **1,858/1,858 from a their-turret tile**, 0 from ours |
| L1–L3 | Teleport detector | rejected **88,716 walk-steps**, kept **351 teleports**, **0** over-range. Max displacement d²=41 — exactly the engine bound (pickup d²≤2 + throw d²≤26 ⇒ ≈41.6). Independent corroboration of the parse |
| L4 | **Throw attribution mirror**: who threw the builder? | subject=their builders → **351/351 own-team launcher**; subject=our builders → **1,444 ENEMY-launcher**. The verdict that never fired for their side is reachable, so the 100% is real |

**Two v1 bugs the C5 hand-decode caught and v2 fixes:** attribution used *final* positions (mis-tiling every builder that moved after being hit), and target matching ignored the core's 2×2 footprint (core hits fell to `unknown`).

---

## BALTSARS (`_v542wave` NOISE_OFF) — 30 cells, we won 14/30, median game 183.5r

**Q1 first contact** — midline **r8 [7–8]** (6–23, n=30) · Chebyshev-3 of our core **r10 [8–11]** (6–45, n=30) · first structure damage in our half **r24 [15–50]** (n=22, never 8) · **first core damage r61 [52–83]** (n=21, never 9), **21/21 by turret fire, 0 by peck**.
Seat-mirrored: |seatA−seatB| on the crossing round is **0 in 14/15 maps**.

**Q2 lanes** — first crosser **|perp| 1.41**, **76.7% within 2 tiles of the core-to-core axis**, **0% beyond 4**. All 460 crossings: 80.7% axis, 2.4% flank>4, flank side balance 44 left / 45 right (**no side bias — do not pre-position asymmetrically**). Entry Chebyshev from our core: **6 [5–10]**.

**Insertion mechanism — they do not walk in.** **23/30 first bodies arrive by their own launcher throw** (76.7%). A relay ladder marches up the axis:

| rung | round | along (0=their core, 1=ours) | \|perp\| | n |
|---|---|---|---|---|
| 1 | **5 [5–5]** (min 5, max 5) | 0.14 | 0.5 | 28 |
| 2 | 7 [7–7] | 0.42 | 0.5 | 28 |
| 3 | 9 [9–11] | 0.67 | 1.5 | 23 |
| 4 | 13 [11–42] | 0.85 | 1.5 | 19 |

First launcher **inside our half r9 [7–9]** (28/30) · first launcher **within a throw of our core (d²≤26) r11 [7–13]** (22/30).

**Q3 targets** — first of ours damaged in our half: **conveyor 48.1%**, core 33.3%, gunner 7.4%, sentinel/harvester/builder 3.7% each (n=27). All 1,160 in-half events: core 53.0%, conveyor 38.6%, harvester 3.4%, gunner 2.4%.
**Plants:** 245 total (launcher 141 / sentinel 82 / gunner 22), **48.2% in our half**. Our-half plants: **d² to our core footprint 10 [4–36]**, Chebyshev 3, **|perp| 1.5 with 60.2% on-axis**, **point-blank d²≤4 in 30/118 (25.4%)**. **First our-half plant r9 [7–9], 30/30 cells.**
**Collar:** 248 barriers built inside our half, **243 orthogonally/diagonally adjacent to our core footprint (cheb≤1)**, **30/30 cells**, first at **r11 [10–13]** (min 9) — spawn-tile denial around our core.

**Q4 cadence** — **2.5 [2–3]** distinct raider bodies all game. Per 50r bucket (denominator = cells still running): r0–49 mean 2.23, 30/30 cells ≥1 · r50–99 1.90, 28 cells · r100–149 1.34, 23 · r150–199 1.28, 14 · decaying after. **Reinforcement is weak: only 6/18 cells send a new body after their first loss in our half.**

**Q5 belt** — 448 events, 22/30 cells. **87.5% builder pecks**, 12.5% turret fire. **88.2% land at cheb≤2 from our core footprint**; by harvester distance: mid-trunk 42.9%, far 40.6%, near-harvester only 16.5%. First belt tile hit **r52 [24–62]**, at **cheb 1 [1–1] from our core** and cheb 3 from the nearest harvester — **they eat the belt at the core end, not the harvester end.**

---

## MJOLNIR NOISE_OFF — 30 cells, we won 8/30, median game 213.5r

**Q1** — midline **r4 [4–6]** (3–17, n=30) · Chebyshev-3 **r7 [6–12]** (4–127) · struct damage in our half r42 [21–88] (n=17, never 13) · **first core damage r95 [43–156]** (n=23), **23/23 turret fire**. Seat-mirrored 14/15 maps. **This is the fastest opponent to arrive.**

**Q2** — first crosser |perp| **0.5**, **86.7% on-axis**, 0% beyond 4. All 468 crossings 72.6% axis, 7.9% flank>4; side balance 53/75 (mild, not actionable). **80.0% of first bodies arrive by throw.**

Ladder — the tightest metronome of the three:

| rung | round | along | \|perp\| | n |
|---|---|---|---|---|
| 1 | **1 [1–1]** | 0.11 | 0.52 | 29 |
| 2 | **3 [3–3]** | 0.36 | 0.50 | 25 |
| 3 | **5 [5–5]** | 0.63 | 0.50 | 24 |
| 4 | 8 [7–41] | 0.90 | 0.80 | 21 |

First launcher **in our half r5 [5–8]** (29/30) · within a throw of our core **r11 [7–39]** (29/30).

**Q3** — first in-half target: **core 50.0%**, conveyor 38.5% (n=26). All 1,067 events: core 61.9%, conveyor 31.4%, sentinel 3.7%.
**Plants:** 266 (sentinel 126 / launcher 119 / gunner 21), 47.4% in our half. Our-half: **d²_fp 6.5 [4–29], Chebyshev 2, 70/126 at cheb≤2, 41/126 point-blank d²≤4 (32.5%)**, 65.9% on-axis. **First our-half plant r5 [5–7], 30/30 cells** — the earliest turret presence of any opponent.
**Collar:** 217 barriers + 18 conveyors + 8 harvesters in our half; **204 adjacent to our core**, 30/30 cells, first **r11.5 [9–18]**.

**Q4** — **2 [2–5]** bodies. Uniquely, **their commitment does not decay**: r0–49 mean 1.60 (30/30 cells) · r50–99 1.10 · r100–149 1.29 · r200–249 1.38 · **r300–349 2.00 · r350–399 2.00 (8/9 cells)**. **Reinforcement 8/13** cells after a loss — the most persistent of the three.

**Q5 belt** — 335 events, 17/30 cells, **85.7% pecks**. **92.2% at cheb≤2 from our core**, 0% outfield. Near-harvester share 26.9%. First belt tile **r53 [30–88]**, cheb 2 [1–2] from core.

**Bonus (their launchers taking *our* builders):** **1,051 throws of our builders**, 21/30 cells, first at **r11 [9–22]**, destination **d² 50 [50–61] from our core** — they are throwing our builders *away* from our core, not to the border (only 7.7% border). Heavy-tailed (one cell contributes 305); the median 4.5/cell is the honest figure.

---

## SLEIPNIR-v2 (`_v488beltbreak2` NOISE_OFF) — 30 cells, we won 10/30, median 195.5r

**A different class entirely.**

**Q1** — midline **r17 [12–24]** (5–71, **n=23; 7/30 cells they never cross at all**) · Chebyshev-3 **r26 [22–44]** (n=22) · struct damage in our half r42 [23–103] (n=15, never 15) · **first core damage r91.5 [28–159]** (n=20), **20/20 turret fire**.
**Seat mirroring fails: identical in only 1/11 maps** (|A−B| median 5, max 50). **Their timing is not geometry-locked and cannot be predicted from map shape alone.**

**Q2** — first crosser **only 56.5% on-axis**, 13.0% beyond 4 tiles; all 380 crossings 57.9% axis / 17.4% flank>4. Crossing `along` median **0.729** vs 0.93/0.91 for the others — **they loiter near the midline rather than driving to our core.**
**Insertion: 23/23 first bodies WALK. Zero launcher relay** (median 0 launchers built per cell; only 5 cells build any, and never before r160).

**Q3** — first in-half target: **core 57.1%**, harvester 19.0%, conveyor 19.0% (n=21). All 1,124 events: core 53.2%, conveyor 31.3%, **harvester 8.1%** (2.4× the others), builder 5.2%.
**Plants:** 161 (sentinel 108 / gunner 43 / launcher 10), **only 33.5% in our half**. Our-half: **d²_fp 25 [5–34]**, Chebyshev 4, **point-blank d²≤4 only 6/54 (11.1%)**, **just 37.0% on-axis**. First our-half plant **r33 [17–60]**, and **8/30 cells never plant in our half at all**.
**Collar:** 138 barriers + 80 conveyors + 25 harvesters in our half; 122 adjacent to our core but **only 21/30 cells**, first at **r34 [28–48]** — later and less reliable.

**They shoot from their own half.** In **5/30 cells** (bifrost A+B r27, jotunheim A r129 / B r72, longhouse B r63) our structures take damage with **zero opponent bodies ever crossing the midline** — long-range sentinel fire onto our forward structures. A fortress ring sized to intercept bodies would never touch these.

**Q4** — **2 [1–4]** bodies, and sparse: r0–49 only **22/30** cells see one (vs 30/30 for both others); r100–249 buckets have median 0. Reinforcement 4/8.

**Q5 belt** — 352 events, 15/30 cells. **81.8% pecks / 18.2% fire — the most turret-driven belt damage of the three** (first belt hit: 9 pecks vs **6 fire**, against 19/3 and 16/1). 81.8% at cheb≤2 from core, but **25.6% near-harvester** and 13.9% in the apron. First belt tile **r57 [42–106]**, cheb **2 [1–3]** from the nearest harvester.

---

## Cross-opponent table — the pre-positionable regularities

| # | Regularity | Baltsars | Mjolnir | Sleipnir-v2 |
|---|---|---|---|---|
| 1 | First midline crossing | **r8 [7–8]**, n=30, seat-identical 14/15 | **r4 [4–6]**, n=30, seat-identical 14/15 | r17 [12–24], n=23, **never in 7/30**, seat-identical 1/11 |
| 2 | First body within cheb 3 of our core | **r10 [8–11]** n=30 | **r7 [6–12]** n=30 | r26 [22–44] n=22 |
| 3 | Arrival mode | **77% launcher throw** | **80% launcher throw** | **100% walk** |
| 4 | Relay ladder rung 1 | **r5 [5–5]**, along 0.14, \|perp\| 0.5, n=28 | **r1 [1–1]**, along 0.11, \|perp\| 0.5, n=29 | none (med 0 launchers) |
| 5 | First launcher inside our half | **r9 [7–9]**, 28/30 | **r5 [5–8]**, 29/30 | never, 30/30 |
| 6 | First turret plant in our half | **r9 [7–9]**, 30/30 | **r5 [5–7]**, 30/30 | r33 [17–60], 22/30 |
| 7 | Our-half plant distance (d² to core fp) | 10 [4–36], cheb 3 | **6.5 [4–29], cheb 2** | 25 [5–34], cheb 4 |
| 8 | Point-blank plants (d²≤4) among our-half plants | 30/118 (25.4%) | **41/126 (32.5%)** | 6/54 (11.1%) |
| 9 | Plants on-axis (\|perp\|≤2) | 60.2% | 65.9% | 37.0% |
| 10 | First barrier adjacent to our core | **r11 [10–13]**, 30/30 | **r11.5 [9–18]**, 30/30 | r34 [28–48], 21/30 |
| 11 | First core damage | r61 [52–83] | r95 [43–156] | r91.5 [28–159] |
| 12 | Core damage source | **100% turret fire** 21/21 | **100%** 23/23 | **100%** 20/20 |
| 13 | Raider bodies, whole game | 2.5 [2–3] | 2 [2–5] | 2 [1–4] |
| 14 | Late commitment (r300+) | decaying (mean 1.0) | **rising (mean 2.0)** | sparse (mean 1.0, med 0) |
| 15 | Belt damage source | 87.5% peck | 85.7% peck | 81.8% peck (most fire) |
| 16 | Belt hits at cheb≤2 from our core | 88.2% | 92.2% | 81.8% |

**Three invariants across all 90 cells:**
1. **First damage to our core is turret fire in 64/64 cells that took core damage — never a builder peck**, and 1,858/1,858 core-landing shots came from a their-turret tile. Anti-peck aprons do not protect the core; line-of-fire denial and turret-plant denial do.
2. **The belt is eaten at the core end.** 81.8–92.2% of belt damage lands within Chebyshev 2 of our core footprint; near-harvester is the minority class everywhere (16.5 / 26.9 / 25.6%).
3. **Raid bodies are few — median 2 to 2.5 over an entire game — and reinforcement after a loss is a minority event** (6/18, 8/13, 4/8 cells). The pressure comes from *planted turrets and barriers*, not from a stream of bodies.

---

## Direct sizing implications

- **Turret ring / lanes.** Against Baltsars and Mjolnir the corridor is the core-to-core axis: 77% and 87% of first crossers within 2 tiles of it, plant clusters 60–66% on-axis, and flank side balance is 44/45 and 53/75 — so **cover the axis band symmetrically; there is no favoured flank to economise on**. Sleipnir defeats a purely axial ring (57.9% axis, 17.4% beyond 4 tiles, non-mirrored across seats).
- **Apron mesh / plant tiles.** The tiles to deny are **Chebyshev 1–3 of our core footprint**: that is where 243/204/122 of their adjacent builds land and where their our-half turrets sit (median cheb 3 / 2 / 4). The BC point-blank class (d²≤4) **verifies per opponent at 25.4% / 32.5% / 11.1% of our-half plants** — real but a minority; the fuller band is d²≤36.
- **Ammo readiness.** The binding clock is Mjolnir: a launcher lands in our half at **r5 [5–8]** and a body is within Chebyshev 3 of our core at **r7 [6–12]** (min r4). Baltsars: r9 / r10. **Ammunition must be banked by ~r5, not by the first-core-damage round (r61–r95) — by then their ladder and collar are already built.**
- **Ladder interdiction is the single highest-leverage prediction.** Both throw-based opponents put rung 1 at a fixed round (r5 and r1) on the axis at `along` 0.11–0.14 with |perp| ≈ 0.5, in 28–29 of 30 cells. That is a known tile-band at a known round in a known half — *their* half, which is what makes it an offensive answer rather than a fortress one.

---

## Caveats that bind on any use of these numbers

- **All measurements are conditional on our side being `_v628compose`.** Opponent behaviour is reactive; these describe how each bot plays *against a v628-class bot*, not context-free constants. A Heimdall fortress that behaves differently may move these timings.
- **Cluster enumeration (per the standing procedure):** the 30 cells are 15 maps × 2 seats on inert seeds. The MAP cluster binds. On f1/f2 the seat pair is byte-equivalent in timing for 14/15 maps, so **the effective n for the timing medians is ≈15, not 30** — the CONTENT-DUPLICATE cluster is live and I have not applied a numeric DEFF because these are medians and spreads for pre-positioning, not exclusion claims. **Do not convert any of these spreads into a significance test without re-deriving the design effect on this tape.** On f3 the seat pair diverges (1/11 identical), so its 30 cells carry more independent information than f1/f2's do.
- **Censoring is not zero.** Games end early (median 184–214 rounds); every "never" count above is right-censoring, and the per-bucket cadence rows carry their own alive-cell denominators for that reason.