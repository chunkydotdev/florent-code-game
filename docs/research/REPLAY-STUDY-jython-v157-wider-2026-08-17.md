# Jython v157 WIDER-RECORD replay study — the ferry-siege shape, measured over 60 games

**BANKED by research s50, 2026-08-17 ~18:0xZ.** Agent report verbatim below (HTML entities normalised). Banking verification: the 60 downloaded replays exist in the declared scratchpad namespace (counted 60), budget 12/60 respected, decoder validated 12/12 match scores against `league_matches.tsv` per the agent's own control. **Converges independently with the builder's single-match study (`REPLAY-STUDY-jython-inspiration-2026-08-17.md`)** on: one raider, self-destructing launcher relay, ring-barrier seal, sentinel-as-kill-weapon (95.2% here vs 96.8% there). ⟦BANKING note⟧: ledger row appended (Jython v157, 60 games — these are Jython-vs-field games, not vs-us games).

---

## PROVENANCE
agent = opus s50, fresh. Budget used: 12 matches / 60 replays / 15 MB, all v157 (live since 08-16 01:52Z), all matches from 08-17, opponents rated 2011-2132 (all ≥1900), 4 of 12 are Jython losses (21/60 game-losses). Decoders built on `replay_census` audited primitives; per-game winners folded back to match scores agree 12/12 with `league_matches.tsv`. Jython game share on this ground 39/60 = 0.650 ±0.149 (DEFF 1.529). Event counts serve existence/mechanism claims.

## 1. OPENING (n=60)
First launcher **r1 in 60/60 games** (median=p10=max=r1); first self-throw r2; first harvester r8, first conveyor r10, first barrier r9; first sentinel r38 (60/60), first gunner r88 (only 22/60). Builders by r30: **median 3** (opponents 5); harvesters 2, conveyors 8, barriers 5; builder attacks by r30 median 0. **The eco-vs-aggression split is a 1-bot fork: the STARTING builder becomes the raider at r1; everyone else runs a small economy.** Turret book: gunners 0.67/game vs sentinels 3.85 (the field is reversed: 3.70 vs 1.53).

## 2. LAUNCHER DOCTRINE
381 launchers / 60 games = **6.35/game** (≥1 in 60/60). Placement: 255 forward, 99 ON the enemy core ring. Opponents: 106 total, 101 by one team (ph); six of seven opponents build ZERO.
Throw classes: own-forward landing near enemy core 1,195 (27%) · in transit 140 · **shuffle at the core 2,018 (46%** — see stall signature) · own-backward 21 · **eviction of enemy builders AWAY from their core 928 (21%)** · pulls toward us **0**. Self-ferry hop d² median 17, p90 32, max 41 (displacement can exceed the 26 measured from the launcher). **≥3-hop relay inside r<40 in 50/60 games** (median longest 4, max 9).

### ⭐ Launcher demolition — CONFIRMED in effect, ⛔ CONTRADICTED in mechanism
292/381 removed; lifetime median 1 round. Zero-HP removals: 180 — **180/180 lifetime exactly 1 round, 180/180 had thrown first, 0/112 combat kills at lifetime 1** (control fires both ways; per-entity zero-HP rates differ by type and owner). **The discriminating control: 180/180 zero-HP removals had NO friendly builder orthogonally adjacent — `destroy()` was geometrically impossible (the builder had just been thrown away). The launcher `self_destruct()`s the round it fires.** Raw order (O(1) g1): r1 BUILD launcher → r2 THROW + REMOVE (no HP event) → r3 BUILD next → r4 THROW+REMOVE → … one launcher per two rounds. **Scale side-effect: destruction refunds the +10% contribution ⇒ the relay is scale-neutral, costing only ~20 Ti scaled per hop.**

## 3. SIEGE SHAPE
Phase medians: r1 launcher · r2 throw · **r6 raider within d²≤8 of enemy core · r8 orth-adjacent (59/60)** · r9 first ring build · r28 6/12 ring · r38 first sentinel · r52 10/12 ring · **r125 enemy core dies (37/60)** · r190 own core dies (16/60).
**One raider, always:** distinct raiders thrown near the enemy core per game — median 1, **max 1** (60 total/60 games). Max simultaneous adjacent builders median 1. Raider survival 55/60 to game end (median lifespan 145; 86.8 Jython heal events/game).
**Ring barriering:** 995 barriers = 16.6/game; **769 on the enemy 12-ring** (531 on the 8 orthogonal), 5 ever on their OWN ring. Peak occupancy median 10/12; full 12/12 in 15 games; full orthogonal 8/8 in 25.
**Denial, measured with controls (full-8-seal games, n=25):** defender core-heals 0.0200/round unsealed → **0.0000 while sealed** (0/1,967 rounds); defender spawns 0.0523/round → **0.0000**. In 15/15 fully-12-sealed games, 0 post-seal spawns (vs 51 post-r57 spawns in the 45 unsealed). Observed spawn birth offsets = EXACTLY the 12 ring tiles, nothing else. ⚠ **THE PARTIAL SEAL RUNS THE WRONG WAY: on the ≥10/12 cut, heals go 0.0100 → 0.0681/round. The seal must complete the 8 orthogonal tiles or it buys nothing.**
**⭐ SURPRISE (written before explaining): THE RAIDER DOES NOT KILL THE CORE.** Enemy-core damage ledger over 60 games (25,488 HP): **−18 sentinel ×1,348 = 95.2%** · −2 builder ×612 = 4.8% · gunner 0%. (Control: on Jython's OWN core the alphabet differs — sentinel 71.1%, gunner 28.2% — the decoder is not a constant.) **The kill weapon is a forward sentinel shooting OVER the barriers**: 231 sentinels, 81% forward, 74% within d²≤32 of the enemy footprint (median d²=9, built median r75). **Core-kill wins with no in-range sentinel: 0/37.**
**True sequence: ferry one bot in by r8 → wall the ring (spawn+heal denial) → build a sentinel just outside the ring → its obstacle-ignoring shot removes the core the defender cannot body-heal. The barriers are not the weapon; they make the sentinel's DPS un-out-healable.**
**Eviction throws:** 928, median round 109 (maintenance phase, not entry); distance median 4.2 tiles; 50% of victims picked up within d²≤8 of their own core (the healers/rebuilders). Victim fate: 865 alive at end, **0 crash-signature deaths** despite 33.8% landing on border tiles — **the crash channel is unharvested by the top team; additive to the plank for us.**
**REFUTED, retained:** the 2,018 shuffle throws are NOT ring-reaching repositioning (95% followed by no adjacent build within 3 rounds). They are a **stall signature**: 1 bot, 61% a single repeated (from,to) pair (top: 312 repetitions), scaling with game length (8.4/game in ≤r150 wins vs 79.6 in >r300). **Fast wins carry almost none; the ping-pong is what failure looks like.**
Contact→kill latency: first core peck→death median 77 (n=14); first adjacency→death median 111 (n=36).

## 4. WHAT BEATS THEM / STALLS THEM
Record 39-21 (0.650 ±0.149); kill median r125; **timely-kill by r300 = 32/60 = 53%**; own core dies 16/60 at median r190; 7/60 reach r1000.
**Sharpest discriminator: FORWARD ENEMY TURRETS** — opponents' forward-placed turrets: wins median 0 (mean 0.9) vs **losses median 4 (mean 4.4)**; opponent sentinels 0.7 vs 3.1; Jython ring peak 10.1 vs 8.4; Jython sentinels 4.5 vs 2.7; Jython conveyors 22.3 vs 10.3. Readings in confidence order: (1) **counter-siege beats siege — they have no defence (0.67 gunners/game, own core dies r190 median); the race is symmetric and they usually win it first.** (2) **Deny the ring, deny the kill** — and there is exactly ONE raider (60/60): single point of failure. (3) **Starve the ammo**: 1,348 core hits = 13,480 Ti converted; loss games show their economy collapsed.
**The ph anomaly:** the only launcher-building opponent (10.1/game) and Jython's only losing matchup here (4-6). ph MIRRORS the plank (self-ferries, same self-destruct signature) and **does not out-kill Jython — it survives to r1000 and wins on titanium_collected** (its six wins: 1000×4, 840, 358). Defeat-shaped under R1000_IS_DEFEAT, but it is the field's demonstrated stalling answer.
**NULL, reported:** "earlier arrival ⇒ win" does not hold (medians both r8; mean gap outlier-driven — no direction read).

## FERRY-SIEGE COMPATIBILITY (element by element)
| element | verdict |
|---|---|
| ONE offensive builder | **CONFIRM, stronger: it is the STARTING builder, forked r1; median=max=1 raiders/game** |
| Self-throw ferry | **CONFIRM** (1,335 forward self-throws; adjacency by r8 on 30×30) |
| To the BACKSIDE of the core | **NOT MEASURED** (face of footprint untested — treat unverified) |
| Destroy launcher after use | **CONFIRM in effect, ⛔ mechanism is launcher-side `self_destruct()`, not builder `destroy()` — build it that way; scale-neutral by refund** |
| Barrier every ring tile | **CONFIRM (769/995 on enemy ring; 12/12 in 15 games)** |
| Spawn denial | **CONFIRM w/ control (0.0523→0.0000/round; spawn set = exactly the 12 ring tiles)** |
| Heal denial | **CONFIRM w/ control (0.0200→0.0000) — ⚠ BINARY: partial ≥10/12 seal INVERTS (0.0100→0.0681); complete the 8 orthogonals or nothing** |
| Eviction launcher | **CONFIRM (928 throws, 100% away-from-core, 50% of victims picked up at d²≤8 of their core; maintenance phase ~r109)** |
| Eviction as crash channel | **ABSENT in Jython (0/928 crash signature) — our approved class is ADDITIVE here** |
| Kidnap toward us | ABSENT (0/928) |
| Raider pecks the core to death | ⛔ **CONTRADICT: 95.2% of core damage is a forward sentinel (median d²=9, r75); 0/37 kills without one. Without a sentinel the plank has no win condition — only the stall.** |
| Turret choice | sentinel over gunner (range + obstacle-ignoring = exactly what a barriered ring requires) |
| Home defence | ABSENT — they accept the race (5 own-ring barriers ever) |

Profile: 62% core-kill rate, 53% timely-kill by r300, kill median r125, from a 3-builder/2-harvester/8-conveyor opening.

## DOWNLOAD LOG (12 matches, 60 replays, 2.5 s apart, 0 errors — full table with ids, opponents 2011-2132, 4 losses included; artifacts games.jsonl/sides.tsv/jstudy.py/agg*.py/dump.py/dl.log left in scratchpad namespace `jython_study/`)
617d4d27 (sporks 26, 4-1) · e775b59e (Lorem Ipsum 44, 2132, 4-1) · 3dda7812 (Lorem Ipsum 44, 1-4 L) · e7f97cd3 (ph 47, 1-4 L) · 15ef61e3 (O(1) 26, 2-3 L) · 202a0ef6 (Bean counters 47, 4-1) · d4e3b813 (Pivot 199, 4-1) · 69bf9fb9 (Pivot 194, 5-0) · 43370996 (Bean counters 47, 2-3 L) · f709db7c (ph 48, 3-2) · dd08d926 (sporks 25, 4-1) · 2d29e441 (Pantheon 91, 5-0)
