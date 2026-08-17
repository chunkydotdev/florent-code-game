# REPLAY AUTOPSY — Erebus v143 one-builder gunner rush, rated match e0c4fb0c (with v142 control)

**BANKED by research s50, 2026-08-17 ~17:5xZ.** Agent report verbatim below. Banking-lane verification: constants `T4_BEACON_BAND_DSQ=64` (doctrine.py:2029), `LOKI_DEFEND_SEAT=4` (:1210), `LOKI_FWD_TI_FLOOR=40` (:1264), `SIEGE_HEAL_RESERVE_TI=16` (:437), `LOKI_BARRIER_SEAL_ON`/`LOKI_SEAL_TI_FLOOR=0` (:1227-1228) and the `main.py:701` reserve guard all **opened and confirmed** in `bots/_v488beltbreak2`. ⟦BANKING correction⟧: `_try_forward_sentinel` is at **`raid.py:684`**, not 710 as cited — function confirmed, line offset only. All other anchors are the agent's (MEASURED-labelled per discipline).
⟦BANKING note⟧: per Magnus's s50 one-plank directive (ferry-siege), levers L1-L6 are **candidate edits, deferred — no rows stocked today**. The named highest-value follow-up (do The Bisons' 29 / lingling's 8 / diverge's 8 sub-r100 kills since 08-15 share the one-builder mechanism? — cheap corpus read on archived replays) is **PARKED** pending the directive lifting.

---

## PROVENANCE
- agent: opus s50, fresh, no inherited context.
- ground: rated `e0c4fb0c-2bca-46eb-8cb9-ea9216100bee` (17:14:55Z, us v159=`_v488beltbreak2` 2-3 Erebus v143; games 92/87/80/48/84 turns, all core_destroyed; we won g3 antler r80, g5 yulerune r84).
- control: unrated `c3d122b7-17fd-4e31-a623-401ace225ef4` (17:00:59Z, same holder bytes vs **Erebus v142**, 4-1 us) — decoded from `replay_archive/`, rows 5264-5268 of `corpus/unrated_games.tsv`.
- instruments: `tools/corpus/replay_autopsy.py` (self-checking ledger: attributed dmg == summed UpdateHp on the core, MATCH 20/20 team-sides) + custom per-round decoder on `replay_census` primitives, namespaced scratchpad.
- statistics: per-game claims are event censuses (no DEFF); the one corpus-wide comparison (Finding 8) carries DEFF explicitly.

## THE TWO-HALVES ANSWER

**Erebus v143 is a one-builder, zero-economy gunner rush.** MEASURED 5/5: exactly one builder bot at r0, never a second; zero harvesters/conveyors/splitters/barriers; `titanium_collected`=0 in 5/5. The bot walks to our core and plants 5-9 gunners on/beside our heal seats; their core converts Ti→ammo 1:1 and the gunners grind our core at 7 dmg per 4 ammo.

**What kills us is not their damage — it is our heal throughput.** Their offence is funded by a fixed purse (500 + 10/4 rounds, no income). Their Ti buys 1.75 dmg; ours buys 4 HP of repair — **we win the exchange 2.29:1 and we have an economy. They cannot win a race we actually contest.** The three losses each failed a DIFFERENT limb of the heal chain — bodies (g1), latency (g2), bank (g4) — with the other limbs in surplus, which is what makes the chain causal.

**What wins us the game additionally: their doctrine has a single point of failure.** One builder, never replaced — in g3 our forward sentinel killed it at r10 and they built NOTHING for 69 rounds while holding 470-620 Ti.

**The r48 glacierkeep loss is the same mechanism on a shorter walk** (d=24 vs 48 ⇒ nest at r25 vs r47), colliding with our worst economic opening of the ten games.

## PER-GAME TIMELINE
(d = Manhattan core-to-core; Ti@dmg = our bank when our core first hit; ADJ max = max builders orthogonally adjacent to our core)

| | map | d | doctrine | 1st gunner | our 1st dmg | Ti@dmg | Ti min | ADJ max | heals/HP healed | fwd sentinel | result/end |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v143 g1 | midgard 30x30 | 48 | RUSH | r47 | r48 | 95 | 10 | **1** | 41 / 164 | r42 | **LOSS r91** |
| v143 g2 | ragnarok 30x30 | 48 | RUSH | r58 | r59 | 33 | 3 | 3 | 55 / 220 | r68 | **LOSS r86** |
| v143 g3 | antler 14x18 | 8 | RUSH | — | never | — | — | 0 | 0 / 0 | **r5** | **WIN r79** |
| v143 g4 | glacierkeep 30x30 | **24** | RUSH | **r25** | r26 | 23 | **0** | 4 | 17 / 68 | none | **LOSS r47** |
| v143 g5 | yulerune 20x20 | 14 | RUSH | r31 | r32 | 13 | 3 | 3 | **139 / 556** | r48 | **WIN r83** |
| v142 g4 | 25x25 | 26 | **RUSH** | r21 | r22 | 49 | **19** | 3 | 147 / 588 | r41 | **WIN r80** |
| v142 g1/g2/g3/g5 | — | — | eco ×4 | — | — | — | — | — | — | — | 3W 1L |

**v142 g4 is the matched control and the most important row: same rush, comparable map, same clock, same holder bytes — we won it** (core ended 360/500).

## FINDINGS (all MEASURED unless noted)

**1. v143 is a version-level doctrine switch.** v142 played eco in 4/5 games (5 builders, harvesters, trunks); the one-bot rush appeared in exactly 1/5 v142 games. v143 runs it 5/5. Control: not map-keyed — v142 played eco on antler/yulerune where v143 played rush. **Erebus took the 1-in-5 branch and made it the doctrine**, shipping v143 ~11 min before this match (plausibly maiden rated games).

**2. The heal-throughput law IS the fight:** heals/round == min(builders adjacent, Ti on hand) — **185/205 siege rounds (90.2%)**; disagreements are arrival/cooldown ±1 and a measurement-order artifact. Exchange rate: our heal 4 HP/Ti vs their shot 1.75 dmg/Ti = **2.29:1 us**. Control both ways: vs SENTINEL nests healing loses (doctrine.py:169-174 records it); vs this gunner nest v142 g2 healed 797 of 798 dmg over 125 rounds.

**3. The three losses fail three different limbs, others in surplus:** g1 BODIES (ADJ=1 all 44 siege rounds; Ti 10-108 whole siege) · g2 LATENCY (first heal r63, ADJ=3 only at r77; Ti 21-156) · g4 BANK (Ti=0 on 11 of 22 siege rounds; ADJ=4 — MORE bodies than either win). **Neither input alone predicts; their minimum does.**

**4. g1's single healer is anchored to `T4_BEACON_BAND_DSQ = 64`** (doctrine.py:2029; beacon fallback returns False beyond it, eco.py:506-509; convergence gate eco.py:1756). g1: nearest non-defender at d²=85-365, **inside band 0/44 rounds** → only `LOKI_DEFEND_SEAT=4` body healed = the ADJ=1 measured. Control: g5 and g2 had seats 1/2/4 inside the band 100% of siege — the band explains g1 and ONLY g1 (g2 = walk-in latency, g4 = bank). The code's own comment (eco.py:1744-1747) predicts the one-body outcome.

**5. g4's speed = geometry + stalled opening, same mechanism.** First-gunner round tracks the walk (d48→r47/58, d24→r25, d14→r31 w/ documented detour, d8→arrival r10); same 7→35 dmg/round ramp in all rush games. g4 was our worst opening of ten (first harvester r16 vs median r5; `titanium_collected`=0) — **and we kept spending during the siege: ten builds ~70 Ti on r26-r47 while four bodies stood on heal seats with an EMPTY BANK.** 70 Ti = 280 HP; we healed 68. Control: v142 g4, same rush/clock, bank 25-125 throughout → 588 HP healed, won.

**6. Single point of failure, proven in g3:** our forward sentinel (r5) killed their lone builder at r10 (3 shots × 18 on 40 HP); **zero Erebus builds r10-r79, bank 470→620, zero damage returned.** They never spawn a replacement (~20-30 Ti vs 620 bank). The builder must loiter in our home band to rebuild gunners: rounds within d²≤13 of our core — g1 88%, g2 100%, g4 81%, g5 40%.

**7. Our barrier seal is inert vs this doctrine:** 34 seal barriers built across 5 games (raid.py:294-308, before `_try_forward_sentinel`, gated only by `LOKI_SEAL_TI_FLOOR=0`) against an opponent with **1 builderHeal event in 5 games**. Control: vs v142's eco games the seal has real targets (their heal counts 20/100/45) — **inert against the rush case only, and it competes with the forward-sentinel bank (L4/L5).**

**8. The class is real; the sub-r100 form is new** (corpus-wide, archived subset, NOT a rated denominator): class = opponent built ≤1 builder, 0 harvesters, 0 conveyors, ≥4 gunners → **our share 537/1224 = 43.9% vs 52.8% elsewhere; deficit 8.9pp ±4.4pp (DEFF 1.833) — excludes zero.** But within-class core losses have median turn 281 and only 19/550 land before r100 — **v143 is a fast variant.** Board scale: sub-r100 core losses = 355/2923 of all ladder losses, **62 since 08-15** (Bisons 29, lingling 8, diverge 8, Erebus 5) — whether those share the mechanism is UNMEASURED (parked follow-up).

## REFUTED HYPOTHESES (retained)
R1 "lost because our kill was slower" — forward-turret rounds overlap and order backwards (loss r42 < win r48). R2 "map size decides" — dies on v142 g4 (win on 25x25) and v142 g5 (loss on 20x26); they arrive EARLIER in games we win. R3 "home sentinel refused to shoot their builder" — REFUTED AS STATED: it had them at d²≤32 for 36 rounds and shot 0 times, but a sentinel CANNOT rotate; their builder was never on its ray. **Corrected finding: we bought the unrotatable turret to answer a mobile single target.** R4 "home sentinel was waste" — its 14 shots killed 8 gunners ≈ 150 Ti unconverted ≈ 260 dmg denied — same size as the foregone core damage; **killing gunners is a real economic attack because gunners and ammo share one fixed purse.** R5 "uniquely Erebus" — re-scoped to the 1,224-game class (Finding 8).

## THE SCALE ASYMMETRY UNDERWRITING IT (derivation from measured builds)
Our scale 2.6-3.5 vs theirs 1.2-2.4 ⇒ **our sentinel 77-103 Ti vs their gunner 24-48 all game** — and their ammo is never scaled (1:1 forever). They buy the cheapest damage with the only currency that does not inflate.
**9. Why g1 had exactly one forward sentinel:** `_try_forward_sentinel` (raid.py:684) needs `sentinel_cost + LOKI_FWD_TI_FLOOR(40)` ≈ 128-143 effective. **g1's bank crossed 128 exactly once (r41→sentinel r42), never again above 68.** Same signature g5 (140@r47→r48, 139@r61→r62). **g1 ended with their core at 50/500 — two more sentinel shots wins a game we lost.**

## LEVERS (candidate edits, named anchors opened; NO live leg fired; deferred per directive)
- **L1** `T4_BEACON_BAND_DSQ=64` (doctrine.py:2029): band-blind convergence lost g1 (2 healers instead of 1 flips it with margin, arithmetic projection). Unsafe form = flat widening (eco.py:503-505 records why the band exists); evidence-fitting form = band scaling with observed core DPS (beacon already publishes it via SLOT_HEAL_BUDGET).
- **L2** `LOKI_DEFEND_SEAT=4` single defender: vs r21-25 nests convergence never arrives; a second/conditional defend seat is the direct answer (permanent eco cost — currently one opponent's doctrine).
- **L3** heal-priority claim on the bank: nothing stops out-of-band eco spending the bank to zero under siege (g4: ten builds ~70 Ti while ADJ=4 at Ti=0). **Nearly free: refuse non-defensive builds below a floor while SLOT_UNDER set and core bleeding.**
- **L4** seal-before-sentinel (raid.py:294-308, `LOKI_SEAL_TI_FLOOR=0`): 34 barriers vs 1 enemy heal event; gate the seal behind "forward sentinel exists" (preserves it vs eco opponents — it IS load-bearing there).
- **L5** `LOKI_FWD_TI_FLOOR=40` on a sentinel our scale prices at 88-103: effective ~130 trigger crossed once per siege. The lever on OUR kill clock — moves kills earlier, cannot regress the r300 bar.
- **L6** home counterbattery prefers SENTINEL (main.py:721-724): unrotatable vs a mobile single target = permanent miss; a gunner costs ~60% and **killing their one builder ends their offence permanently (Finding 6).**
Speculation, separated: L1-L6 interactions unknown (L3/L5 compete for the bank); Bisons/lingling/diverge mechanism share unmeasured; any Erebus-aimed leg must PIN the version (they ship ~14×/day); all-time vs Erebus 60/110 (0.545), 18/30 today — **the case is the mechanism and the class, not this match's −2.60.**
