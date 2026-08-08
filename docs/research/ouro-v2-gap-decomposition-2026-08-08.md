# ouro-v2 GAP DECOMPOSITION — where the probe's games diverge from the wild's (2026-08-08)

**VERDICT — NOT DIFFUSE.** The 61-point win-rate gap is owned by **two named, code-localizable
subsystems**, not by drift across the behavioural tables: (1) the probe has **no answer to our
standoff sentinel** — it lets it live a median **107 rounds vs the wild's 21.5**, and the 35/60
games where the first enemy sentinel is never killed are **0-for-35** with the probe's own core
dead at median r106; (2) even in the 25 games where that failure does *not* fire, the **serial
gunner ladder throttles to 1.5 plants per 100 rounds after r100 against the wild's 7.5**, so the
r124 strike burst never assembles — **4/25 games ever hold ≥2 gunners alive at d ≤ 9 (wild 7/10)**
and median enemy-core damage is **0**. Questions (a) builder attrition, (c) ammunition and (d)
titanium income are **behaviour present, effect present** in the surviving subset and own
essentially none of the gap.

---

## 0. Version stamps and provenance

| | |
|---|---|
| Probe | `bots/_ouro_v2_dev` (1,557 lines) — **freeze REFUSED**, tape `ouro-v2-freeze` |
| Probe corpus | `replay_archive/diag_ouro_v2_2026-08-08/` — 60 replays + 60 result JSONs, **LOCAL deterministic arena, NOT wild-ladder data** |
| Anchors in corpus | `bots/opp_v74` (ladder v74 "mineguard"), `bots/_v84g` (ladder v73 "Eir 7"); probe played **both seats on every map**, 3 seeds each |
| Wild pairs | `621b841e` (Ouroboros v8 **5–0** vs our v74; atoll, eider, snowflake, drumlin, antler) and `4e0874d0` (v8 **3–2** vs our v73; eider, moonrise, hive, meander, saga) |
| Wild seats | `621b841e`: Ouroboros = **TEAM_B**; `4e0874d0`: Ouroboros = **TEAM_A**. Confirmed **behaviourally**, not from meta: the Ouro side is 100% gunner / 0 sentinel / 0 launcher / 0 splitter / 0 barrier in 10/10 games (11–24 gunners), our side carries sentinels + launchers + barriers in 10/10. Independently agrees with `meta.json` and with the per-game winners. |
| Our live ladder version | **v75 "Eir 8"** — *not in this corpus*, neither as anchor nor as probe opponent |
| Decoder | `docs/research/2026-08-07-fanout/toolkit/replay_lib.py` (stdlib protobuf), read-only. No `fcode`, no arena, no downloads, no bot edits. |
| Scratch | `…/scratchpad/ouro_gap/{decode,deep,sent,econ,face,link,iso}.py` (not committed) |

Headline outcomes reproduced from the replays themselves: probe **9/60 = 15.0%**
[Wilson 8.1, 26.1] here, **57/360 = 15.8%** [12.4, 20.0] on the full battery;
wild **8/10 = 80.0%** here, **23/30 = 76.7%** on the runnable anchor set (spec §5.3).
Gap under decomposition: **76.7 − 15.8 = 60.9 points**.

---

## 1. RANKED DIVERGENCES — the headline

Counterfactual ladder. "SURV" = the 25 probe games in which the first enemy sentinel *was*
killed (i.e. divergence D1 did not fire); "DIED" = the 35 in which it was not.

| # | divergence | probe | wild | incidence | points of the 60.9 it plausibly owns | localized to |
|---|---|---|---|---|---:|---|
| **D1** | **No answer to the standoff sentinel.** Enemy sentinel is left alive; it rays the probe's core down from outside gunner range. | sentinel killed **24.3%** (28/115), median lifespan **107 r**, sentinel→core damage **424/game**, **85.5%** of all core damage taken | killed **72.2%** (13/18), lifespan **21.5 r**, sentinel→core **182/game**, 73.1% of core damage | **35/60 games (58%)**, **0 wins** in that subset, own core dead 34/35 at median **r106** | **≈ 21 pts (34%)**<br>15.0% → 36.0% if all games behaved like SURV | no threat-driven station exists: `BAND_PREFIX`/`BAND_TAIL`/`HOME_SITES`/`MID_STANDOFFS`/`KILL_*` (main.py:144–191) are all pure core-geometry; `_try_melee` (main.py:938) hard-refuses any non-conveyor target |
| **D2** | **Serial gunner ladder throttles after r100** → the r124 burst never assembles. | plants **1.5 per 100 r** over r100→r300; cumulative **6/7/8** at r150/200/300; **4/25** SURV games ever hold ≥2 gunners alive at d ≤ 9; median enemy-core damage **0** | **7.5 per 100 r**; cumulative **8/12.5/20**; **7/10** hold ≥2 alive at d ≤ 9; median core damage **553** | all 60 games; in SURV it is the *only* remaining failure | **≈ 40 pts (66%)**<br>SURV 36.0% vs wild 76.7% | one global index: `idx = ct.read_store(SLOT_GUNNERS)` (main.py:798) and the plant gate `target == idx` (main.py:842) — at most **one** station in flight, ever; `_next_own_station` (main.py:785) + `_station_due_round` (main.py:476) |
| D3 | Economy under-built (conveyor mass, not harvest rate) | conveyors alive **23** @r200 (SURV), harvesters **5**; Ti/harvester-round **1.54** | conveyors **49**, harvesters **9**; Ti/harv-round **2.12** | all games | **≈ 0 directly** — SURV Ti collected **4,960** vs wild **4,645** (parity). Real in DIED (260) but that is downstream of D1 | `_run_eco` (main.py:976), `MAX_CHAIN`, `CHAIN_MAX_ROUNDS` |
| D4 | Ammunition volume ~70% of wild; conversion *shape* wrong (one 60 Ti dump at r0 vs a 20 Ti trickle from r21) | converted **971** (SURV) / 252 (all); balance **60**; starved rounds **0** | **1,384**; balance **46**; starved **1** | all games | **≈ 0** — probe is never ammo-starved, it is *shot*-starved | — |
| D5 | Builder attrition — **PARITY ACHIEVED** | own lost **1**, enemy killed **10** (SURV) | own lost **0.5**, enemy killed **12** | all games | **0** | — |

**Reading.** D1 and D2 are sequential gates, not competing explanations: 58% of games never get
past D1, and 100% of the survivors are stopped by D2. Both are single named mechanisms with a
source citation. **This is a v3-spec-target answer, not a drop-the-probe answer** — with two
caveats stated in §7.

---

## 2. (a) BUILDER-ATTRITION PARITY — *behaviour present, effect present, gap absent*

The enabling condition the spec identifies (§1.7: "they win the builder-attrition war 12:1 from
behind a home screen") is **reproduced by the probe**.

| measure | probe (60, pooled) | probe SURV (25) | wild (10) |
|---|---:|---:|---:|
| builders spawned lifetime (median, range) | 5 (5–14) | 5 | 5.5 (5–10) |
| builders spawned by r10 / r40 | 3 / 5 | 3 / 5 | 3.5 / 5 |
| **own builders LOST per game** | **0** (0–12) | **1** | **0.5** (0–3) |
| own builder losses r0–99 / r100–199 / r200–399 / r400+ | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| **enemy builders killed per game** | 3 (0–18) | **10** | **12** (4–18) |
| enemy builders killed by r200 (survivors only) | 6 | 6.5 | 8 |
| own builders that die at d ≤ 64 of enemy core | 89 total / 60 games (1.5/g) | — | 6 total / 10 games (0.6/g) |
| builder heal actions | 35 | 53 | 57.5 |
| builder median min-excursion (d² to enemy core) | 29 | — | 6.8 |

Verdict on (a): **the probe's builders do not die.** Its own-loss median (0, SURV 1) sits inside
the wild's (0.5), band-by-band, and its enemy-kill rate at r200 conditioned on survival (6 vs 8)
is within noise. The pooled "3 vs 12 enemy builders killed" figure is a **game-length artefact**
(probe median game 140 rounds vs wild 306) and should not be quoted — attrition parity holds.

**"Behaviour present, effect absent."** The wild's attrition dominance is supposed to strip our
heal line and let two rays finish a 500 HP core. The probe achieves the attrition and **still
lands median 0 core damage**. Attrition is therefore *not* the enabling condition on its own; the
strike (D2) is.

One real sub-divergence: the probe's builders keep a longer standoff (min-excursion d² 29 vs the
wild's 6.8) and 20% more of them die forward. That is a cost of the home leash
(`HOME_LEASH_SQ = 36`, main.py:170) and is small.

---

## 3. (b) THE BURST — *departs, arrives, and then does not plant*

| measure | probe (60) | probe SURV (25) | wild (10) |
|---|---:|---:|---:|
| gunners built per game | 5 (0–36) | 7 | **19** (2–24) |
| cumulative planted r25/50/75/100/150/200/300 (alive-conditioned) | — | **2 / 3 / 4 / 5 / 6 / 7 / 8** | **2 / 2.5 / 4 / 4 / 8 / 12.5 / 20** |
| — vs spec A5 target 2/3/4/5/8/11/18 | — | passes to r100, **fails from r150 (−2, −4, −10)** | passes throughout |
| **plants per 100 rounds, r100 → r300** | — | **1.5** | **7.5** |
| first gunner round | 19 (14–59) | — | 21 (4–42) |
| first builder arrival at d ≤ 26 of enemy core | **r93**, 49/60 games | — | **r44**, 10/10 games |
| first builder arrival at d ≤ 9 | r92, **31/60 games** | — | r78.5, **10/10 games** |
| **games with ≥1 gunner planted at d ≤ 9** | **17/60 (28%)** | 12/25 (48%) | **9/10 (90%)** |
| first d ≤ 9 gunner round (games that have one) | 157 | 177.5 | **146** |
| **games with ≥2 gunners simultaneously ALIVE at d ≤ 9** | **5/60 (8%)** | 4/25 (16%) | **7/10 (70%)** |
| burst ≥2 plants at d ≤ 26 inside 12 rounds | 15/60 (25%) | 10/25 | **10/10** |
| max gunners alive at d ≤ 26 (median) | 1 | 1 | **6** |
| gunners planted at d ≤ 26 dead within 20 rounds | 22/133 (17%) | — | 22/84 (26%) |
| **games landing ≥1 shot on the enemy core** | **17/60** | 12/25 | **8/10** |
| core shots landed (median) | 0 | 0 | **79** |
| enemy core damage (median) | 0 | 0 | **553** |
| enemy core kills | **7/60** | 7/25 | **6/10** |
| top-3-shooter share of core shots (games with core damage) | **1.00** | 1.00 | 1.00 (min 0.958) |

**Where it breaks, mechanically.** It is *not* dying en route. The strike builder reaches d ≤ 9 in
**31/60 games** and forward builder deaths are ~1.5/game. But only **17/60 games** ever contain a
gunner at d ≤ 9 — the builder stands on the killer anchor and cannot plant, because the plant gate
requires `target == idx` where `idx` is the single global `SLOT_GUNNERS` counter (main.py:798,
842). `BAND_PREFIX` puts the three KILL stations at indices 6/7/8 with `KILL_DUE = (124, 127, 130)`
(main.py:147–189), but stations 0–5 must all be planted first, **serially, one builder at a time**.
The measured ladder reaches index 5 at r100 and index 6 only at ~r150 — so the R2 fix the
re-freeze spec asked for ("the burst at r124") is written into the constants and **cancelled by the
sequencing**. Wild plants 7.5 gunners per 100 rounds from 5 builders acting in parallel; the probe
plants 1.5 from a queue of one.

**Contrast honestly.** The *shape* the spec asked for is present where it can be measured:
top-3 shooters = **100% of core shots** in every probe game that has core damage (spec: median
100%; A6 target ≥85%) — the 2-3-shooter kill signature is faithfully reproduced, it just almost
never gets built. The killer-band targeting profile is also present and, if anything, *sharper*
than wild: for gunners spawned at d ≤ 13 the probe puts **83.9% of shots into the core** vs wild's
**62.5%** (A7 target 55–75% — the probe **over**-shoots this item, builder share 5.4% vs wild
14.1%).

---

## 4. (c) AMMUNITION — *volume 70% of wild, starvation absent*

| measure | probe (60) | probe SURV (25) | wild (10) |
|---|---:|---:|---:|
| Ti converted to ammo per game | 252 (60–4,312) | **971** | **1,384** (414–2,149) |
| cumulative converted at r25/50/100/200/300 (alive-conditioned) | — | 60 / 108 / 178 / 624 / 728 | 60 / 110 / 240 / 837 / 1,300 |
| convert events per game | 12 | — | 56 |
| **first conversion (round, amount)** | **r0, 60 Ti** — identical in 60/60 | r0, 60 | **r21, 20 Ti** |
| ammo balance held (median over game) | **60** | — | 46 |
| **rounds ammo-starved (<4 with a gunner alive)** | **0** (max 40) | 0 | **1** (max 65) |
| rounds starved with a forward (d ≤ 26) gunner alive | 0 | 0 | 0.5 |
| games ≥1,000 Ti converted, in ≥300-round games (A9) | 12/19 | — | 5/6 |
| total shots fired | 47.5 | 192 | 336.5 |

Verdict on (c): **the probe does not starve.** It holds a *higher* ammo balance than the wild
(60 vs 46) and spends 0 rounds unable to fire. The 252-vs-1,384 pooled gap is a game-length
artefact plus a downstream consequence of D2: with 5 gunners instead of 19 there is nothing to
spend ammo on. The residual conditioned gap (971 vs 1,384 in SURV, ~70%) is real but small, and
it *follows* the shot deficit rather than causing it. **Shape divergence worth one line in the v3
spec:** the probe dumps a flat 60 Ti at r0 in 60/60 games; the wild converts 20 Ti first at r21
and trickles (56 events/game vs the probe's 12). A9's "balance never below 16 while titanium > 60"
is satisfied.

---

## 5. (d) ECONOMY CURVE (spec A10) — *half the conveyor mass, matching delivery in surviving games*

| measure (alive-conditioned medians) | probe SURV | wild | spec A10 target |
|---|---:|---:|---|
| harvesters alive r25 / 50 / 100 / 200 | 3 / 3 / 4 / 5 | 4 / 5.5 / 7 / 9 | 4 / 5 / 5 / 6 (±30%) |
| conveyors alive r25 / 50 / 100 / 200 | 11 / 16 / 16 / 23 | 12 / 15.5 / 32 / 49 | 12 / 16 / 22 / 33 (±30%) |
| harvesters **built** by r25 / 50 / 100 / 200 | 3 / 4 / 5 / 5 | 4 / 5.5 / 8 / 9 | — |
| conveyors **built** by r25 / 50 / 100 / 200 | 12 / 17 / 18 / 25 | 12 / 15.5 / 34.5 / 46 | — |
| harvesters/conveyors **LOST** by r100 | 0 / 1 | 0 / 0 | — |
| Ti delivered by r100 / 200 / 300 | 505 / 1,225 / 2,215 | 860 / 2,630 / 3,320 | — |
| **Ti collected, whole game** | **4,960** | **4,645** | — |
| Ti delivered per harvester-round (chain efficiency) | 1.54 | 2.12 | — |
| first conveyor / first harvester | r6 / r4 | r3 / r4 | ≤r5 / ≤r6 |
| zero-delivery games (D8 reproduction) | 4/60 | 1/10 | — |

Verdict on (d): the economy is **under-built, not destroyed** — losses by r100 are 0–1 on both
sides, and only 4.6% of the probe's economic damage comes from sentinels. The probe lays roughly
**half the conveyor mass** the wild does from r100 onward and runs a **27% worse chain**
(1.54 vs 2.12 Ti per harvester-round), tracking A10's band at r25/r50 and falling out of it by
r100/r200. But **whole-game titanium collected is at parity in the surviving subset**
(4,960 vs 4,645) because those games run to r1000. The pooled 520-vs-4,645 figure is entirely
a D1 artefact (DIED subset median: 260 Ti in a 107-round game).

So (d) contributes to the r1000 tiebreak lane and to build-scale headroom, but it does **not**
explain the win-rate gap — it is ranked D3 for that reason.

---

## 6. SEAT-CONDITIONALITY

**The probe's divergences ARE seat-conditional, strongly.**

| | probe seat A (30) | probe seat B (30) |
|---|---:|---:|
| wins | **8 (26.7%)** | **1 (3.3%)** |
| first enemy sentinel killed | 14/30 | 11/30 |
| enemy sentinel median lifespan | 65.5 r | **91 r** |
| sentinel → own-core damage (median) | 504 | 360 |
| median game length | 154.5 r | **121 r** |
| own core destroyed | 18/30 | 21/30 |
| games with any gunner at d ≤ 9 | 12/30 | **5/30** |
| games landing a core shot | 12/30 | **5/30** |
| Ti collected (median) | 705 | 270 |
| Ti converted to ammo (median) | 339.5 | 232.5 |

Seat B is where both D1 and D2 are worse: the sentinel lives 40% longer, half as many games ever
put a gunner on the doorstep, and the economy runs 2.6× smaller. This **reproduces the frozen
probe's own flagged weakness** ("seat-B legs weakest", `results.tsv`) — i.e. the re-freeze did not
fix it. It is not a wild property: the wild's 10 games split 3/5 (seat A, vs our v73) and 5/5
(seat B, vs our v74), and its sentinel kill rate is 1.00 in both seats. Note the wild seat split
is **fully confounded with opponent** (Ouro held one seat for all five games of each match), so
"wild seat B is stronger" cannot be read out of this pairing — only the probe's asymmetry is
measurable here.

**Anchor-conditional, for the record:** vs `opp_v74` the probe answers the first sentinel in
20/30 games and wins 5; vs `_v84g` it answers in **5/30** and wins 4. `_v84g`'s standoff sentinel
is the harder instrument, and the probe's seat-B games against it are the corpus's floor
(`v84g_hive_*`: sentinel lifespan 112–151 rounds, 802–1,080 core damage, zero counter-plants in
6/6 games).

---

## 7. HOW D1 ACTUALLY WORKS — the measurement chain

This is the finding the v3 decision hangs on, so the chain is spelled out.

1. **Both sides face the same instrument.** Our anchors plant a standoff sentinel in **60/60**
   probe games and **10/10** wild games, at the same time (first sentinel median **r16** probe /
   **r14** wild) and the same place (median d² to the Ouro core **32** in both) — i.e. just outside
   gunner range (r² = 13) and inside sentinel range (r² = 32). Sentinel counts per game are
   identical (1.92 probe / 1.80 wild).
2. **The wild kills it; the probe does not.**
   | | probe (115 sentinels) | wild (18 sentinels) |
   |---|---:|---:|
   | killed | **24.3%** | **72.2%** |
   | median lifespan | **107 r** | **21.5 r** |
   | Ouro gunner damage delivered *per enemy sentinel* | **13.2** | **40.4** (= exactly one 40 HP kill) |
   | got an Ouro gunner planted within r² = 13 of it | **47.0%** (latency 10 r) | **83.3%** (latency 5 r) |
   | of those, **zero damage delivered** | **46%** | **13%** |
   | sentinel → Ouro core damage per game | **424** | **182** |
3. **Two compounding failures inside D1.** Coverage (47% vs 83%) *and* efficacy — when the probe
   does have a gunner within range, 46% of the time it never damages the sentinel at all. Facing
   check: a probe gunner planted near a sentinel is aimed at it at plant time in **6%** of pairs
   and ever aimed (including rotations) in **13%**; the wild's figures are **25% / 33%**. The
   probe's counter-plants are *incidental* — a scheduled station that happens to be nearby — not
   directed.
4. **The consequence is the loss.** 85.5% of all damage the probe's core takes is sentinel fire
   (wild: 73.1% of a much smaller total). 39/60 probe games end with the probe's core destroyed at
   median **r106** (32 of them by r150); in 44 of 50 of those the sentinel share of core damage is
   ≥50%, median **100%**.
5. **The within-corpus dose-response is monotone.** Grouping the 60 probe games by first-sentinel
   lifespan quartile:
   | first sentinel lifespan | n | probe wins | median game length | own core destroyed |
   |---|---:|---:|---:|---:|
   | ≤ 29 r | 16 | **5 (31%)** | 1000 | 2 |
   | 30–64 r | 15 | 3 (20%) | 107 | 10 |
   | 65–95 r | 15 | 1 (7%) | 97 | 14 |
   | > 95 r | 14 | **0 (0%)** | 144 | 13 |
   and binary: first sentinel killed → **9/25 wins (36%)**, median game **1000 rounds**, core dead
   5/25. Not killed → **0/35 wins**, median game **107 rounds**, core dead **34/35**.
6. **The wild's one core-kill loss is the same mechanism.** `4e0874d0` g2 (moonrise): the wild
   fails to kill our sentinel, it lives **83 rounds** and deals **504** damage, the Ouro core dies
   at **r94**. That is the probe's modal game. The failure mode is real for the wild too — it
   occurs in **1/10** of its games and **35/60** of the probe's.
7. **Why the probe cannot answer.** The re-freeze implemented spec §4 D-CRITICAL literally — the
   melee gate refuses every non-conveyor target (`_try_melee`, main.py:938–975, with the comment
   *"the habit that makes a standoff turret outside r² = 13 unanswerable"*). But D-CRITICAL's own
   text is *"no answer to anything outside gunner range **except planting another gunner**"*, and
   the spec's honest bound adds *"their answer is to walk a builder out and plant a gunner within
   r² = 13 of it (411 of their shots hit one of our sentinels)"*. **The operative half of the
   clause was not implemented.** A grep of the probe for any threat-, counter-, or
   defence-keyed station returns nothing: every station site in `BAND_PREFIX` / `BAND_TAIL` /
   `HOME_SITES` / `MID_STANDOFFS` / `KILL_STANDOFF` (main.py:144–191) is a pure function of the two
   core positions. There is no code path in which an enemy turret's position produces a station.

**v3 spec target, named:** a **THREAT band** — a station whose site is derived from the newest
enemy turret inside r² = 13 with a facing that puts it on the ray, pre-empting the ladder index
(i.e. plantable out of `SLOT_GUNNERS` order), plus a directed rotate-to-reacquire while that
turret lives. Acceptance: enemy standoff sentinel median lifespan **≤ 30 rounds** and kill rate
**≥ 70%**, measured off the probe's own replays.

**Second v3 target:** break the serial ladder. `SLOT_GUNNERS` as a single global index
(main.py:798) with `target == idx` gating the plant (main.py:842) makes gunner production a queue
of depth one. Wild parallelism is 5 builders planting from wherever they stand. Acceptance is
already written as A5 at r150/200/300 (8/11/18) — currently **6/7/8**.

---

## 8. SELF-CHECKS

- **Parsing validation.** `replay_lib.check_all()` on **all 70 games** (60 probe + 10 wild):
  **0 failures**. `delivery × 10 == titaniumCollected` **70/70**; `ammo converted − spent ==
  final engine ammo` **70/70**; no unknown top/turn/update/entity fields; no recycled entity ids;
  HP within bounds; winner consistent with dead cores in every game.
- **Cross-check against the result JSONs.** Parsed winner / rounds / win_condition reproduce the
  60 `fcode run --json` lines and the two `meta.json` scorelines (5–0, 3–2) exactly. Probe record
  from replays 9/60 = the README's 9/60.
- **Damage-target law honoured.** All target-kind attribution runs through `replay_lib`'s
  occupancy-aware pass (unit on tile first, else building); rotations are routed to
  `entity_updates` and never counted as builds (probe gunner counts are plant counts).
- **Games excluded: none.** All 70 parsed and used. Two transparency notes: (i) 4 probe games and
  1 wild game collected **zero** titanium — retained, they are D8's own reproduction; (ii) the
  `first d ≤ 9 gunner round` medians are computed only over games that *have* one (17/60 probe,
  9/10 wild) and are reported alongside that denominator everywhere, because taking a median over
  a mostly-absent event is the trap in this table.
- **Spec claims contradicted by measurement, counted explicitly:**
  1. **Spec §1.4 / R6 "gunner mass is already correct — do not fix it."** Contradicted from r150
     onward: the probe holds 6/7/8 at r150/200/300 against the wild's 8/12.5/20 and the spec's own
     A5 target 8/11/18. Correct to r100, wrong after. **This is now a primary v3 target.**
  2. **Spec §4 D-CRITICAL "no answer to a turret outside r² = 13."** Contradicted by the wild's own
     behaviour in the paired games: the wild kills 72.2% of our sentinels in a median 21.5 rounds
     and delivers 40.4 damage per sentinel. The "unanswerable" reading is wrong; the answer is the
     counter-plant, and it is the single most load-bearing thing the probe does not do.
  3. **Spec §1.5 home screen (22.6% at d > 144, lifespan 179).** In these 10 wild games the home
     share is **10%** with median lifespan **267 r**; the probe's SURV games run **20% / 973 r** —
     the probe *over*-satisfies A4 with gunners that are never contested at all. A4 as written is
     passed by an inert behaviour.
  4. **Spec A7 targeting "core 55–75% for d ≤ 13 gunners."** Probe measures **83.9%**, wild
     **62.5%** — the probe overshoots the item it was built to fix.
  5. **Ouroboros seat lock** — already refuted in the spec (§3); reconfirmed here (v8 held B in
     `621b841e`, A in `4e0874d0`).
- **Confounds stated.** (i) The probe corpus is the **local deterministic arena** with 3 seeds per
  map per seat; the wild pairs are **one ladder game per map**, so per-map wild cells are n = 1 and
  are shown for shape, never for significance. (ii) Wild seat is collinear with opponent
  (one seat per match), so no wild seat effect is claimable. (iii) The anchors are *snapshots* of
  ladder v74/v73; the wild games were played against those ladder versions live — anchor-behaviour
  drift is possible but is bounded by the measurements that match: first sentinel r16 vs r14,
  standoff d² 32 vs 32, sentinel count 1.92 vs 1.80/game, enemy ammo converted 384 vs 311.
  The anchors are planting the same instrument in both corpora. (iv) The SURV/DIED split is
  **self-selected** — "games where the probe happened to answer" may differ from "games where a
  fixed probe would answer", so the 21/40 point split between D1 and D2 is a bound, not an
  estimate. The direction is not in doubt: D2 is the larger half.

---

## 9. THE THREE NUMBERS

1. **Enemy standoff sentinel: 107 rounds alive vs the wild's 21.5** — 24.3% killed vs 72.2%,
   424 core damage per game vs 182, and the 35/60 games where it is never killed are **0-for-35**
   with the probe's core dead at median r106.
2. **1.5 gunners planted per 100 rounds after r100 vs the wild's 7.5** — cumulative 8 vs 20 at
   r300, so **4/25** surviving games ever hold ≥2 gunners at d ≤ 9 (wild 7/10) and median enemy
   core damage is **0** (wild 553).
3. **Everything the spec called the enabling condition is present and does not help:** own builders
   lost 1 vs 0.5, enemy builders killed 10 vs 12, Ti collected 4,960 vs 4,645, ammo-starved rounds
   0 vs 1, top-3-shooter share 100% vs 100% — in the surviving subset the probe still wins only
   **9/25 (36%)** against the wild's **76.7%**.
