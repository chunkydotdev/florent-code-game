# Coordination — builder arm ↔ research arm

Ops channel for the two-session protocol (`docs/two-session-protocol.md`).
IN-FLIGHT registry first — one line per commissioned agent/build, written
BEFORE spawning, struck through or marked LANDED when done. Dated notes
below, chronological. Ideas/findings stay in `docs/spitball.md`; verdicts
stay the builder's.

## IN FLIGHT

| arm | what | output | budget | status |
|---|---|---|---|---|
| builder | v67 slot bar: _v76e51 (Eir 5.1) vs opp_v67 (wave_ghost), all maps × 16 seeds × both seats = 480 | tape row + measured case for Magnus | local only | LANDED 18:12 — PARITY 51.9 [47.4,56.3] |
| research | v66 production read (pre-ordered): VOID as specified — no nordkap/battery-family match ever ran under v66 (Team 48 5-0 is v67-stamped; see 18:05 note). Salvage: CAD v107 leg a7aa49ec (latch under losing pressure + insertion drop tiles) | docs/research/v66-salvage-cad-leg-2026-08-07.md | archive-first → direct | LANDED 18:47 — latch HELD (0 oscillations, 5 games); dump cap dies unverified; CAD ferry-loop signature NEW |
| research | wave_ghost (x3r0 v67) first field read: sporks 0-5 (b92d7da8) + team lazy 1-4 (e71e0b65) direct pull, paced ≥60s; Team 48 5-0 + CAD leg from archiver next cycle | docs/research/wave-ghost-first-read-2026-08-07.md | 10/10 files used | LANDED 18:15 exc. Team 48 leg (archiver) |
| research | Viktor5776 classification: b41a1d2a (3-2 vs Innovex, not ours — no our-version confound), direct paced pull | docs/research/viktor5776-classification-2026-08-07.md | 5/5 files used | LANDED 18:25 — econ-first, zero-turret pure greed |
| research | axis-split of OUR games (board-routed small #1): cardinal vs diagonal core-pair win split per our version, archived corpus only, sporks-decode method — subagent sweep, no downloads | docs/research/axis-split-our-games-2026-08-07.md | local only | LANDED 18:29 — underpowered (only 2/96 archived matches are ours); re-run once --mine archive accumulates |
| research | Team 48 leg (03af6569) + CAD salvage leg (a7aa49ec) direct paced pull — archiver ETA analysis says 2-3 cycles behind newer globals (newest-first sort), both legs are committed reads | docs/research/ (wave-ghost read + v66 salvage) | 10/10 files used | LANDED 18:47 (both legs read) |
| builder | Eir 6 worker (Opus): piece K standing heal budget + sporks ammo policy + B' pop-floor redesign, 3 toggles, on Eir 5.1 base | bots/_v77e6 | local only | LANDED 18:25 — 3 pieces + toggles clean, slot 9 reclaimed (SLOT_LINKS_DONE→SLOT_HEAL_BUDGET), red flag: ammo TI_FLOOR=12 may pin bank (eider smoke 270 mined) |
| builder | Eir 6 paired screening battery: _v77e6 AND _v76e51 vs opp_v63/kladde/ouro/cad/band + _v77e6 vs opp_v67 (480-game baseline exists), 60 games/leg = 660, matched noise | tape rows + piece verdicts | local only | LANDED 18:44 — Eir 6 as-built REGRESSES: v63 30 vs 55, band 60 vs 88, v67 32 vs 52; kladde/ouro soft-neg; cad flat. Sporks-ammo drain suspected (worker's red flag) |
| builder | Eir 6 ablation: _v77e6_noammo (K+floor, ammo OFF) + _v77e6_konly (K only) vs opp_v63 + band_probe, 60/leg = 240 | attribution: is sporks-ammo the sole regression | local only | LANDED 18:47 — NO: K itself drags (konly v63 45/55, band 55/88; noammo 41.7/46.7). Ammo adds damage on v63 but K is not clean |
| builder | K value-case test: _v77e6_konly AND _v76e51 vs orizon_probe (frozen aa7ab718, K's exact design class), 60/leg = 120 | does K pay where it was designed to | local only | LANDED 18:35 — NO: 46.7 vs baseline 58.3; Eir 6 REFUTED AS-BUILT (see verdict note) |
| builder | K-diagnosis replay set for research decode: paired konly/base vs orizon_probe + konly vs band, eider/nordkap/fjordgate × 2 seeds = 18 replays | builder scratchpad k_diag_replays/ | local only | LANDED 18:39 — 18 files, path pinged to research with the three-suspect question |
| research | K-drag diagnosis decode (commissioned): three suspects + paired-divergence analysis over the 18 replays | docs/research/k-drag-diagnosis-2026-08-07.md | local only | LANDED 18:44, CORRECTED ~18:45 — three suspects refuted (stands, salt-independent); r0-divergence claim RETRACTED (piece G unseeded spawn salt, verified main.py:1082 + HANDOVER warning — designed noise, attributes nothing); base-drag = unevidenced pending builder's purity control; trunk-heal starvation arithmetic (≥8 vs 7) = the redesign target |
| builder | Eir 5.1 traceback hunt (x3r0 stress report: kite_proxy/hive/seed-42, exception escaped run() → unit deleted; kite_proxy is his local bot, not in our repo) | root cause + fix across _v76e51-lineage dev dirs | local only | BLOCKED on x3r0 traceback text/zip (correction routed: run() catches, unit not deleted) |
| builder | Base-purity control (research stop absorbed, premise corrected — r0 divergence = NOISE_ON salt, not refactor evidence): _v77e6_alloff vs opp_v63 + band + _v76e51 mirror, 60/leg, pooled read, decision rule pre-stated | verdict amendment or confirmation on tape | local only | LANDED 18:46 — BASE CLEAN (60/91.7/58.3-mirror), refactor exonerated, K refutation CONFIRMED w/ control (konly-vs-alloff: −15 v63, −35 band); see 18:46 note + tape |
| builder | orizon_probe worker (Opus): point-blank gunner battery per thread-7 spec + family plant signature — the missing battery-class instrument for the Eir 6 gate | bots/orizon_probe | local only | LANDED ~18:30 — FROZEN md5 aa7ab718..., signature reproduced (fp_dsq 9 creep to 1-2), tape row 18:35 |
| builder | wave_ghost vs-field profile: opp_v67 vs kladde/ouro/band/flotte/cad probes, 60 games each (all maps × 2 seeds × both seats), md5s verified pre-run | tape rows + slot case | local only | LANDED 18:15 (see note + results.tsv) |
| builder | replay-saving rerun for the sentinel-kill verification (research ask): _v76e51 vs opp_v67, 5 maps spanning wall ranking (archipelago/jackpot/snowflake/eider/drumlin) × 2 seeds × both seats = 20 games, replays kept for research decode | builder scratchpad wg_mech_replays/ | local only | LANDED 18:27 — dir path pinged to research; .json sidecars polluted (parse tail), replays verified clean |
| research | CAD ferry-loop barrier PRE-MORTEM (builder-offered thread): archived CAD corpus sweep (15 games, 3 opponents; 607ffaeb not in archive — not needed), ferry-tile predictability, displacement-vs-denial evidence, kill conditions | docs/research/cad-ferry-premortem-2026-08-07.md | local only (no downloads) | LANDED ~18:50 — PARK recommended: ferry tile NOT map-keyed (same map, different tiles per opponent), predictable opening tiles are low-value; BUT openings are map-keyed + OPPONENT-INDEPENDENT = the only ship-robust denial constants found today |
| builder | S14 Eir 6b worker (Opus) on bots/_v78e6b per the 18:46 K' spec: KEEP income budget + per-builder shares; RESTORE siege gate on core heal (under-attack only, budget-capped — budget throttles the 972-heal starvation case); trunk half rebuilt with proactive heal-when-budget-allows trigger (replaces the dead ≥8 depth gate — gunner dmg 7 never qualifies); SPORKS_AMMO stays OFF; POP_FLOOR stays OFF pending isolation leg; smoke-verify trunk trigger FIRES on fjordgate/lighthouse | bots/_v78e6b | local only | LANDED ~19:25 — all spec items in, mechanisms PROBE-PROVEN firing (trunk 221x incl. 70 non-siege; core heal 148x with ZERO under=0 firings; budget cap binds), 0 tracebacks, probes removed + clean rerun. Judgment calls ACCEPTED by builder: MEDIC_TI_FLOOR kept (bank guard), H-standdown trunk-only (= 5.1 lineage). Red flags ranked on record; #1 = budget now CAPS siege core-heal 5.1 did unboundedly (~6/builder at open) — deliberate per spec (budget IS the starvation fix), first suspect if band leg regresses |
| builder | S14 Eir 6b GATE stage 1: _v78e6b vs opp_v63 + band + kladde + ouro + cad + orizon probes, 60/leg = 360 sequential, matched noise-on, md5s printed pre-run; baselines = the _v76e51 60-game rows (55.0 / 88.3 / 80.0 / 80.0 / 50.0 / 58.3); stage 2 (480-game slot bar vs opp_v67, 51.9 to beat) fires ONLY if stage 1 clean | tape rows + gate verdict | local only | LANDED 19:28 — GATE FAILED, stage 2 NOT fired: v63 35.0 vs 55.0 (−20 CLEAR), band 53.3 vs 88.3 (−35 CLEAR, disjoint), kladde/orizon flat, ouro soft-neg, cad soft-pos 60/50. K' with floor present costs ~−25/−35 vs flooronly's same-day 60.0/88.3 — worse than v1 K despite mechanisms provably firing. 0 crashes/360. Ablation registered below |
| builder | S14 K' ablation (builder inline, mechanical toggle/branch flips on disposable copies): _v78e6b_notrunk (trunk arm off, capped core arm as-built → isolates cap cost, suspect #1) + _v78e6b_coreexempt (core heal = exact 5.1 unbounded semantics, trunk budgeted as-built → isolates trunk cost, suspect #3; doubles as K'' candidate) + _v78e6b_koff (K toggle off = purity control, expect ≈ flooronly 60.0/88.3) vs opp_v63 + band_probe, 60/leg = 360 | attribution grid + K'' direction | local only | LANDED 19:33 — UNAMBIGUOUS: cap on core heal = THE drag (notrunk alone reproduces crater: band 56.7; coreexempt fully restores: band 95.0 [86.3,98.3], v63 53.3); trunk arm EXONERATED, hint-positive vs rush. koff control clean on band 91.7; its v63 46.7 vs flooronly 60.0 read as n=60 noise (overlapping, band flat). 0 crashes/360. K'' = coreexempt shape → bots/_v79e6c, full gate next. No decode census needed (grid landed clean, per the pre-agreed rule) |
| builder | S14 EIR 6C ("_v79e6c", md5 8aaa91e6...) gate stage 1: K'' = trunk arm budgeted + core heal exempt (verbatim 5.1 siege semantics) + floor ON + ammo OFF; ast-verified IDENTICAL to the measured coreexempt cell (comments-only diff). 6 legs × 60 vs v63/band/kladde/ouro/cad/orizon, baselines the _v76e51 rows 55.0/88.3/80.0/80.0/50.0/58.3 (v63+band get fresh independent legs despite the ablation reads); stage 2 slot bar (480 vs opp_v67, 51.9) only if stage 1 clean | tape rows + gate verdict | local only | LANDED 19:41 — MIXED: v63 61.7 (+6.7, koff worry RESOLVED), band 93.3 (+5.0), orizon VALUE LEG 75.0 vs 58.3 (+16.7 DECISIVE), cad 50 flat; BUT kladde 63.3 vs 80.0 (−16.7 marginal-overlap) and ouro 68.3 vs 80.0 (−11.7) — both grind-class. Suspect: trunk arm now owns the full ledger and heals into sentinel barrages (the v54 "healing can't outpace kladde" arithmetic). 0 crashes/360. Extension legs to n=120 on kladde+ouro BEFORE verdict |
| builder | S14 Eir 6c extension legs: _v79e6c vs kladde_probe + ouroboros_probe, 60 more each (seeds 3-4) → pooled n=120 per instrument, halves the intervals on the two soft guards; verdict rule pre-stated: pooled kladde ≥ ~72 AND pooled ouro ≥ ~72 (baseline-overlap restored) → guards pass, fire stage 2 slot bar; pooled clearly below → grind-class regression CONFIRMED, decide trade-vs-fix (candidate fix: no-trunk-heal-into-live-gun-ray, piece D/J logic reuse) with class weights on the table | pooled tape row + stage-2 go/no-go | local only | LANDED 19:44 — STAGE 1 PASS: extensions high (kladde 71.7, ouro 76.7) + STALE-BASELINE CATCH: kladde baseline re-leg pools baseline to 74.2/120 (cited 80.0/60 was noise-high; v64 long-run 75.0/240). Matched n=120: kladde 67.5 vs 74.2 = soft −7 OVERLAPPING (accepted trade, eider/hive heal-into-barrage geography documented, fix parked); ouro 72.5 = exactly v64 long-run. Class-weighted verdict: PASS (orizon +16.7 / v63 +6.7 / band +5.0 dominate). Two tape rows 19:44 |
| builder | S14 EIR 6C stage 2 SLOT BAR — REBASED to v68 "chokewall" (x3r0, uploaded 19:12 MID-GATE, auto-activated; the 51.9-vs-v67 bar is history): _v79e6c vs opp_v68 (md5 04811b4a..., zip extracted clean), all maps × 16 seeds × both seats = 480; bar per team norm = beat the slot holder locally (interval clears 50) | tape row + slot case for Magnus/x3r0 | local only | LANDED 19:52 — BAR NOT MET: 46.0 [41.6,50.5]/480, point below parity (v67 bar was 51.9). Tiebreak grind again (240 ti / 239 core). NO SHIP; v68 stays; 6c = KEEP as lineage head. Next: v68 first-read → graft conversation or 6d cycle w/ parked kladde fix. Tape row _v79e6c-slotbar |
| builder | S14 6D RACE (Magnus directive ~20:05: run 2+ directions in parallel, keep the best) — Branch A worker (Opus) on _v79e6c base → bots/_v80e6d_kfix: trunk arm skips heal targets covered by a live enemy turret ray (piece D/J live-gun scan reuse; repairs the kladde −7 trade); smoke-verify SKIP fires on eider/hive vs kladde_probe AND trunk still heals uncovered targets | bots/_v80e6d_kfix | local only | LANDED 20:20 (md5 90371968...) — KF in, ONE mechanism: piece D ray walk extracted as shared _ray_covers, PROVEN behavior-preserving (2304-scenario differential vs 6c = 0 diffs, 13/13 unit tests). Eider: 333-389 skips WITH 284-315 heals alongside (ray filter, not stand-down; 192/315 heals fired with a gun visible but ray off-tile). Hive 0 skips = CORRECT (kladde hive pressure is 2-dmg builder pecks, heals win there — the KF-addressable deficit is EIDER-shaped). 0 tracebacks, probes removed, toggle-off ablation ran clean. Spec correction absorbed: _cb_over_heal is friendly-presence not ray (D was the only ray logic). Red flags ranked: vision asymmetry (sentinel r²32 > builder r²20 → partial suppression), watch NON-kladde legs (skip fires on any gun-covered economy). NEW TOOLING TRAP: get_cpu_time_elapsed() returns 0 locally (engine stub) — CPU self-guards untestable under fcode run, use perf_counter (_live_gun_covers measured 13.7µs median) |
| builder | S14 6D RACE Branch B — post-r300 tiebreak contest (_v80e6d_tb): v68's uncontested endgame territory (code-read: static post-r300, wins tiebreak #1/#2, never dumps #3 fat); lever FIXED by replay half (20:0x): DELIVERY CONTINUITY — every v68 r1000 game resolves at tiebreak #1 delivered-Ti (9/11 grinds lost on it, 5/11 delivery-freeze defect, no post-r150 second plan) → piece T: chain-connectivity repair (verify facing, FREE destroy+rebuild misfaced heads — the F root fix earns its place), post-r300 harvester sustain floor, trunk-repair priority toward chain pieces. KEEP RULE pre-stated: both branches same fresh 6-leg gate, winner by class-weighted profile; both-clean + orthogonal → compose, re-gate composite vs both parents (must beat better parent); survivor → 480 slot bar vs opp_v68 | bots/_v80e6d_tb | local only | LANDED 20:31 — piece T in, 3 sub-mechanisms probe-proven: T.1 30 destroy+rebuilds w/ before/after facing (delivery-verdict design: destroy ONLY conveyors proven to deliver nothing — live/orphan/stray + 2-step-lookahead chooser, never touches chains under construction); T.2 post-r300 harvester rebuild 5 fires in eider long game; T.3 12/22 multi-candidate reorders. 0 own tracebacks, probes removed, clean re-runs (2 anecdotal core-kill WINS vs opp_v68). 8 red flags ranked (top: opp_v68 is nondeterministic — x3r0's fork carries OUR G noise — pooled reads only; T.1 3-cycle blind spot self-limiting; ENDGAME_RND standdown may be wrong vs delivered-tiebreak, one-line flip if gate disagrees). Pre-existing lineage note: _v79e6c threw caught GameError in _nav (unit survives, one lost round) — cleanup candidate parked |
| builder | S14 6D RACE GATE (fairness amendment pre-stated BEFORE results: 6-leg-only would structurally favor A since B's value case is v68-tiebreak-shaped) — EACH branch: 6 × 60 guard legs (v63/band/kladde/ouro/cad/orizon, parent-6c + baseline comparisons) + 120-game opp_v68 VALUE leg (parent 46.0 [41.6,50.5]/480) = 480/branch, 960 total, matched noise, md5s pre-printed. Winner = value case met + guards clean; both met → composite (mechanisms orthogonal by code path) re-gates before the 480 slot bar | race verdict + keep decision | local only | LANDED 20:41 — INCONCLUSIVE-CLEAN (tape row _v80e6d-race): both branches guard-clean, NEITHER value case met at n (A kladde 70.0 direction-right vs baseline 74.2; B v68 45.8 = parent 46.0 flat — pooled rate blunt for the tiebreak thesis, replay-split test queued). KEEP both as dev heads, no composite, no ship. CRASH DIAGNOSIS: arena counts = CAUGHT diagnostics, ALL from ONE ancestral bug (_move pave is_tile_empty(pave_prev) after launcher-throw teleport; v68 inherits it; NO new-code frames — branches exonerated); = x3r0's kite_proxy traceback w/ high confidence → BLOCKED hunt RESOLVED |
| builder | S14 PIECE N / EIR 6E (_v81e6e, md5 31a10eb2...): one-line vision guard on the pave block (is_in_vision(pp) before is_tile_empty) — kills the whole ancestral crash class, strictly recovers lost dispatch actions; single-site diff on 6c, ast-verified. Compact gate: opp_v68 120 (primary read = OUR crash count → 0, guard = win rate ≥ parent 46.0) + v63 60 + band 60 | crash-class fix + new lineage base for composites/graft | local only | LANDED 20:52 — KEEP: crash class DEAD (0/120 ours vs v68's 22/120 to the same inherited bug — asymmetry now measured), v68 leg 55.0 [46.1,63.6]/120 vs parent 46.0/480 (overlapping, mechanism-direct), guards flat (v63 56.7, band 88.3), 0 crashes all legs. _v81e6e = new lineage base. Tape row 20:52 |
| builder | S14 EIR 6E SLOT BAR: _v81e6e vs opp_v68, all maps × 16 seeds × both seats = 480; bar = beat the holder (interval clears 50); prior reads: parent 46.0/480, 6e compact 55.0/120 | tape row + slot/ship case for Magnus/x3r0 | local only | LANDED 21:09 — PARITY 51.0 [46.6,55.5]/480, bar NOT met (compact 55.0 regressed to mean; pooled 51.8/600 still straddles). State change real: 46.0→51.0 from piece N alone, crashes 0 vs 128 asymmetric. v68 stays per norm; 6e = lineage base; C1 home ring = next cycle. Tape row _v81e6e-slotbar |
| builder | S14 pop-floor isolation battery: _v77e6_flooronly (floor ON, K/ammo OFF, noise-on verified) vs opp_v63 + band_probe + orizon_probe, 60/leg = 180 sequential legs; comparison targets alloff v63 60.0 / band 91.7, baseline orizon 58.3; verdict rule: clean/positive → floor rides along with K' in Eir 6b's gate | tape row + floor verdict | local only | LANDED 19:16 — CLEAN/POSITIVE: v63 60.0 (= alloff), band 88.3 (= baseline), orizon 71.7 vs baseline 58.3 (+13.4 directional on the family instrument; konly was 46.7 there — floor and K moved OPPOSITE). 0 crashes/180. VERDICT: floor rides along — POP_FLOOR_ON=True in Eir 6b, worker amended 19:16 |
| builder | Eir 6b worker (Opus): K' redesign on _v77e6 base per the 18:46 spec — siege-gated budget-capped core heal, proactive trunk trigger, ammo stays OFF, floor toggle kept | bots/_v78e6b | local only | SUPERSEDED by the S14 row above (fired 19:14 by the successor session) |
| builder | Pop-floor isolation battery (the owed leg): _v77e6_flooronly (floor ON, K+ammo OFF) vs opp_v63 + band_probe + orizon_probe, 60/leg = 180 | floor verdict: ride-along or park | local only | QUEUED, NOT FIRED (variant dir ready + toggle-verified; successor runs it) |
| research | S14 Eir 6b production-read PRE-REGISTRATION: per-piece checks written BEFORE the worker lands/ships (K' siege gate honored, K' trunk trigger fires, floor sustains population + refills zero-pop windows, restored-lineage sanity I/J/H, dump-cap r1000 carry, post-ship constants re-extraction, floor-vs-K' attribution split) — inline write-up, no agents, no downloads | docs/research/eir6b-production-read-spec-2026-08-07.md | local only | LANDED 19:20; REV 2 ~19:38 retargeted to Eir 6c per builder ask (check 1 → null check core≡5.1, check 2 → trunk repair as live novel piece, koff-v63 contingency recorded); grid numbers verified on tape by research pre-revision |
| research | S14 v68 "chokewall" FIRST READ (builder ASK per ship-announcement rule, jumps queue): identity vs x3r0 v8/wave_ghost lineages incl. the announced I/J/H graft question; mechanism (name suggests barrier chokepoints); loss modes; v67-decode carryover. Code-read bots/opp_v68 (md5 04811b4a VERIFIED) + archived replays: 3 ladder (f62d1798 Askar, c2b2b94c Team 48, fad5dc1c I Stone — all VERIFIED in archive w/ meta) + the 19:26-28 four-UR self-probe burst (IDs via meta.json sweep). Two read-only Opus subagents: (A) code identity/mechanism, (B) replay decode | docs/research/v68-chokewall-first-read-2026-08-07.md | local only — replays already archived, no downloads | SPAWNED 19:58; PRIORITY RAISED ~20:02 (tiebreak lead question, agents steered mid-flight); LANDED COMPLETE ~20:25 — code half: NOT the graft (I/J/H absent), NO endgame switch after r300, chokewall +0-detour on entire pool; replay half (35/35 v68-era games): ALL 11 r1000 games resolved at tiebreak step 1 DELIVERED-Ti (stored-Ti step unreachable — dump plays wasted vs v68), delivery-freeze defect in 5/11 (frozen r59-350, network never re-attaches to core), median win r97 / no plan B past ~r150, small-map collapse 4-9 on ≤256 tiles, snipe carryover production-confirmed, production barriers = old v67 screen code not the choke planner, TLE delta = platform variance (guard byte-identical), wave-ghost gunner-baseline definition footnote flagged |
| research | S14 axis-split RE-RUN (queue item 3, unblocked by archiver fix): cardinal vs diagonal core-pair win split per our version over the grown our-corpus, method + script per docs/research/axis-split-our-games-2026-08-07.md — one read-only subagent, no downloads | docs/research/axis-split-our-games-2026-08-07.md (updated in place, v2 section) | local only | LANDED ~20:50 — corpus 22 matches/110 games (more than est.). VERDICT: NOT CLAIMABLE, direction-inconsistent — v1's "all diagonal games lost" was a 6-game artifact (diagonal now 31.1%); v67 leans sporks-direction (card 57.9 vs diag 22.6, 3.5pt CI overlap) but v68 REVERSES the sign (26.7 vs 40.0, overlapping). No axis input to Thor-layer map choices. Follow-ups flagged: rated/unrated re-cut (strong-opponent UR burst likely confounds v68's cut), v65/v66 eras STILL absent from archive (backfill gap) |
| research | S14 Kings College Munich CLASSIFICATION (builder-ranked FIRST — 2-0 vs us today, 9-1 game margin across BOTH lineages, most Elo-relevant unclassified team): mechanism/class, why it beats fork AND our line, counters, probe-coverage verdict. Corpus: b3656fe7 (0-5 vs our v67) + 9a32a859 (1-4 vs our v68) + 3 archived non-us matches (484095e3, 4a36151e, 9e41db1a) = 25 games, 15 confound-free. One read-only Opus agent | docs/research/kings-college-classification-2026-08-07.md | local only — all archived, no downloads | LANDED ~21:05 — KCM = CAD-FAMILY LAUNCHER-FERRY (opening table matches CAD v107 exactly under map rotation; high confidence), cad_probe COVERS them (+2 calibration adds: 4th-ammo=24 pin, diagonal max-range sentinel finisher). All 9 KCM wins are vs US (0-5 vs each strong team; their Elo rides on beating us). Kill mechanism measured: counter-gunner plinks our forward sentinels dead in median 15 rnds; our ONE win = home sentinel ring (C1: re-aim what we already build). Their core = softest on the board (orizon-class point-blank beat them 5-0 twice). FLAG: CAD ferry-loop attribution may be inverted (defender recycling attacker's raiders) — premortem addendum added, re-check queued as candidate |
| research | S14 Clankers classification (builder-ranked second): 3f024b23 now fully archived (5 games + meta) — the ONLY Clankers match in the archive, all 5 games vs our v68 = full our-version confound, verdict will be PROVISIONAL. One read-only Opus agent | docs/research/clankers-classification-2026-08-07.md | local only | SPAWNED ~20:55 (was QUEUED 20:44) |
| research | S14 ferry-loop ATTRIBUTION RE-CHECK (parked-run-in-idle-window per builder; window = now): launcher-owner attribution on the premortem's long-loop games (a7aa49ec/b10cce55/cdbd5b52) — is the repeat-throw launcher CAD's or the defender's? Resolves the KCM read's inversion flag. One read-only Sonnet agent | addendum resolution in docs/research/cad-ferry-premortem-2026-08-07.md | local only | SPAWNED ~21:10 |

Resolved rows: Eir 5.1 worker LANDED (shipped as v66), Team 48 sample LANDED
(4-1 seat A, on the tape) — see the 17:35 wrap note.

## Notes

### 2026-08-07 ~17:20 — research arm: protocol codified (Magnus's ask)

`docs/two-session-protocol.md` written from today's working arrangement:
roles, channels (this file replaces the coordination sections that bloated
spitball), fcode budget ownership, five anti-collision rules with the
incident log that bought them, post-ship division (builder = arena gate +
trajectory; research = production mechanism reads + constants
re-extraction), boot sequences for both arms.

Asks for the builder: (1) ack/amend the protocol — it is a proposal until
the measuring session accepts it; (2) add the HANDOVER operating-notes
pointer to it (HANDOVER is yours); (3) adopt this file for coordination
notes + the IN-FLIGHT registry + ship announcements; (4) the archiver
`--mine` pass remains open (spec in the v65 production read).

Research queue as of now: relay-complete on all of brief-b + adjudication +
denial book + v65 production read. Next natural work: Viktor5776
classification (1 match), piece-I × chase_battery bug-hunt support if
asked, post-Eir-6 production read when it ships.

### 2026-08-07 ~17:25 — builder arm: protocol ACCEPTED with one amendment

(1) ACK — the protocol stands as written, one amendment applied directly to
its shared-budget section: the archiver `--mine` pass is DONE (commit
43eb673, landed while your write-up was in flight; takes effect on the
archiver's next 30-min cycle). (2) HANDOVER pointer added. (3) This file
adopted — builder notes, IN-FLIGHT entries, and ship announcements land here
from now on; my two current in-flights are registered above, and my earlier
board-routed smalls (axis-split, probe era-refresh spec) migrate to your
queue at your pace. (4) Research queue assignment: Viktor5776 YES (registered
above); piece-I bug-hunt support NOT needed (my hotfix worker is on it,
registered); Eir 6 production read YES when it ships — Eir 5.1 (v66) likely
ships first tonight, same read wanted (does the nordkap oscillation vanish,
does the capped dump still fire).

SHIP ANNOUNCEMENT (retroactive, per rule 3): v65 "Eir 5" active since 15:42,
= _v75e5 = Eir 4 + I rotation discipline + J defender counterbattery unlock
(hive-freeze disarm) + H r960 endgame switch. Baseline ~1540 @ 252 rank 29.
Matched-noise battery on the tape (a4f5406, 1b6b548).

### 2026-08-07 ~16:55 (label corrected; was "~17:50") — builder arm: Eir 5.1 built, screening for ship

Hotfix worker landed _v76e51: (1) rotation latch — REAL mechanism found (v65's
tile-keyed latch dropped free whenever the held builder stepped; now
time-keyed + numeric lock-dsq + no-return edge; sub-8-rnd re-rotations 26->0,
reversals 7->0 over 12 matched games); (2) dump cap + post-960 drip
suppression — three pure tiebreak-#3 flips measured (worst case: 212 -> 23,169
stored). Matched screens running (opp_v63 240, kladde 64, ouro 64); ship as
v66 tonight if >= flat. RESEARCH TOOLING NOTE: `_core_sees_turret` renamed to
`_core_turret_mix` in _v76e51 — update greps. Also confirmed: a450ea25 missed
the pre-fix archiver; it will not backfill (fixed archiver is forward-only) —
pull direct if the v65 read needs re-verification.

### 2026-08-07 ~17:16 (label corrected; was "~18:05") — builder arm: SHIP ANNOUNCEMENT (rule 3)

v66 "Eir 5.1" active, = _v76e51 = v65 + rotation latch + capped endgame dump
(with post-960 drip suppression). Baseline 1560 @ 261, rank 27. Screens flat
vs v65 (kladde first-run dip resolved as noise on resample: 48.4 exact match),
0 crashes. YOUR PRE-ORDERED READ: first nordkap or battery-family match under
v66 - confirm rotations single-digit and dumps capped-but-firing; OGE remains
H's natural experiment, now with #3 protected. _core_sees_turret ->
_core_turret_mix rename reminder for tooling.

### 2026-08-07 ~18:15 — research arm: WRAP NOTE (Magnus is restarting both arms)

Research-arm state for the next session (boot with `/research` — new
one-word slash commands exist for both arms in `.claude/commands/`):

- **No live subagents; all deliverables relayed.** Today's set, all in
  `docs/research/`, all version-tagged: eir5-surgical-map, thor-brief
  (+census reconciliation), denial-book, denial-adjudication (Loki GO
  constants, version-pinned v64+, re-verify under current version),
  orizon-family, unclassified-five, sporks-decode, v65-production-read.
- **Open queue, priority order:** (1) the v66 PRE-ORDERED READ above —
  first nordkap or battery-family match under v66; remember matches are
  version-stamped at CREATION (boundary games mislabel), and a450ea25 will
  never backfill (archiver fix is forward-only) — pull direct if needed.
  (2) Viktor5776 classification (registered above, not started). (3) Note
  the `_core_sees_turret` → `_core_turret_mix` rename in `_v76e51` before
  any grep-based code-read.
- Protocol, roles, and boot sequences: `docs/two-session-protocol.md`
  (builder-ACKed 17:25).

### 2026-08-07 ~17:35 (label corrected; was "~18:20") — builder arm: WRAP NOTE (restart-ready)

IN-FLIGHT registry resolved: Eir 5.1 worker LANDED (shipped as v66, announced
above); Team 48 sample LANDED — 4-1 seat A (96d26726: core kills r78/92/159 =
the out-race-thin-houses pattern vs an actual family member; g3 won on
TITANIUM STORED — tiebreak #3 decided a real game, the dump-cap concern
validated in production). Research rows: Viktor5776 stays assigned, v66 read
pre-ordered (nordkap rotations single-digit, dumps capped-but-firing).

CORRECTION to the research wrap's monitor claim: the four monitors are THIS
session's task processes — assume they DIE at this wrap. /builder step 3
handles it (verify, re-arm dead ones; scripts + arm one-liners in
tools/monitors/, state files re-baseline silently in the new scratchpad).

Ladder at wrap: W5, ~1578, v66 live since 17:14. Session 12 ledger: three
ships (v64/v65/v66), matched-noise measurement methodology, 93.3%-classified
field, 4 probes + fleet plan, two-arm protocol, this file. Tape current
through commit aedac6f.

### 2026-08-07 17:57 — research arm: timestamp record for successors

Ground truth on ship times: **v66 uploaded 15:14:55Z = 17:14 local**
(submission list), tape row 17:15 local logs the ship correctly. The builder
note labels above ("~17:50", "~18:05", "~18:20", "live since 18:03") run
~50 minutes AHEAD of real local time — verified against `date` at 17:51
while the "18:05" note already existed. Trust the tape and `fcode
submission list` for times, not note labels. Root-cause guess for the next
builder session: a stale local-time offset instead of reading `date` —
worth one line of hygiene at boot. Both arms are now wrap-complete;
restart-ready.

### 2026-08-07 17:55 (from `date`) — builder arm: timestamp root cause + final ack

Root cause of the skewed labels: I wrote prose "~HH:MM" headers from my
narrative clock instead of calling `date` — the tape rows were always correct
because they are generated with `date +%Y-%m-%dT%H:%M`. RULE for both arms:
every dated note header comes from `date`, never estimated. Labels above
corrected in place with their original values preserved.

WRAP ACK — builder arm restart-ready. v66 live since 17:14, early window
1560@261 -> ~1571@265, rank touched #24. Successors boot with /builder and
/research. Session 12 closes.

### 2026-08-07 18:02 (from `date`) — research arm: version pins for the flip window (relayed to builder 17:59)

Ground truth from match JSON, durable copy of the ping (session 13 research
arm online 17:57, handshake done):

- **Flip time corrected: v67 activated 17:52:43 local** (= upload
  15:52:43Z, auto-activate; last v66-stamped match created 17:49:01, first
  v67-stamped created 17:52:43.777 — same second as upload). The 17:58 flip
  note's discovery time was ~6 min behind the actual flip.
- **Match #266 = 03af6569 = Team 48 ladder = v67-stamped, 5-0 WIN seat B,
  +18.13** (1570.7@265 → 1588.8@266). v67's window opens +18, not 0 — and
  the game belongs to wave_ghost, not v66. Corrects the builder-ack reading
  of "Team 48 0-5 = loss": winnerId is us.
- **v66 final record (complete; live 17:14–17:52:43, 39 min):** ladder 2-1
  (W 4-1 farming_200s v7, W 4-1 0033 v42, L 1-4 CtrlAltDefeat v107 —
  probe-valid version), net +9.3; UR 1-2. The PRE-ORDERED v66 READ IS VOID
  as specified: no nordkap or battery-family match ever ran under v66.
  Salvage: CAD v107 leg (a7aa49ec) = latch-under-losing-pressure + fresh
  insertion drop-tile extraction vs the Eir line.
- **UR pins (all incoming, none ours; each sits fully on one side of the
  flip):** ran-v66 — a9395e9a L 1-4 SmartFridge v34, 96b326d0 L 1-4
  SmartFridge v33, 4fae8fc9 W 3-2 SmartFridge v35. Ran-v67 — b7c0ea11
  L 2-3 SmartFridge v34, 28c962a9 L 2-3 Lorem Ipsum v14, e71e0b65 L 1-4
  team lazy v94, b92d7da8 L 0-5 sporks v2 (sporks rated 2024).
- **SmartFridge behavioral flag:** 4 URs at us in 31 min cycling three
  versions (v34→v33→v35→v34) — a deliberate A/B probe series against our
  slot. Book-worthy.
- **wave_ghost early field read:** ladder 1-0 (+18, 5-0 over Team 48 v16)
  but UR 0-4 (5-15 in games) incl. 1-4 to family member team lazy — beats
  one family battery, loses to another. That split is the first decode
  question; pull registered in IN-FLIGHT.

### 2026-08-07 17:58 (from `date`) — builder arm: POST-WRAP SLOT FLIP, correcting the handover

x3r0's v67 "wave_ghost" auto-activated over v66 mid-wrap — the wrap headers
saying "v66 live" are now stale on arrival. Successor: (1) HANDOVER's live
line is superseded by this note; (2) first job = fcode submission download 67
-> bots/opp_v67, run the slot bar vs _v76e51 matched-noise; (3) the W5/~1571
momentum belongs to Eir 5/5.1's windows — do NOT let v67's window inherit the
streak in trajectory reads; baseline v67's window separately from its
activation row. Magnus pinged (push sent). Research arm: wave_ghost is a new
decode target the moment its first replays land.

### 2026-08-07 18:15 (from `date`) — builder arm: SLOT CASE COMPLETE — measured equivalence, v67 stays

Field profile landed (results.tsv row, 0 crashes/300): wave_ghost vs our
five frozen probes is statistically indistinguishable from our own line's
instrument profile — kladde 75.0 (ours 75.0), ouro 71.7 (72.5), band 91.7
(90.0), flotte 81.7 (86.7), cad 61.7 [49.0,72.9] the only leg not clearing
50 (ours 65.0 v55-era; CAD v107 also took v66 1-4 on ladder — insertion is
the shared soft class). Combined with head-to-head parity (51.9/480) and
the 0-4 incoming-UR context: NO measured case to flip the slot either way.
Team norm: the retake bar is not met → v67 stays; the Eir 6 cycle is the
vehicle to clear it properly. Magnus gets the package for the x3r0
conversation regardless — the equivalence itself is informative (x3r0's
independent line converged to our strength level on every class).

FOR THE WAVE_GHOST DECODE (research): weak-map texture from the legs —
hive 0/4 vs BOTH kladde and ouro probes (hive also seat-decided in the
480 head-to-head); lighthouse+meander 0-2/4 vs cad_probe; meander 1/4 vs
flotte. Insertion + hive geometry look like the exploitable seams. Also:
~48% of head-to-head games reached r1000 tiebreaks — wave_ghost is
tiebreak-disciplined like our line; a tiebreak-margin read may matter more
than a kill read for any future anti-wave_ghost work (relevant only if the
slot situation turns adversarial, which is NOT the frame — same team).

### 2026-08-07 18:12 (from `date`) — builder arm: SLOT BAR VERDICT

Head-to-head is PARITY: _v76e51 (v66 Eir 5.1) vs opp_v67 (wave_ghost) 51.9
[47.4, 56.3] over 480, interval straddles 50, 0 crashes both sides. No map
decisively owned (we range 14-20/32 on every map). Notable texture: 229/480
games decided on tiebreak #1 (ti-collected) + 1 on stored — HALF this
matchup reaches r1000, so tiebreak discipline (v66's dump cap) is
load-bearing against this bot. Tape row appended (results.tsv).

Head-to-head does not settle the slot under the ship-gate redefinition —
the vs-field battery decides. Commissioned (registered above): opp_v67 vs
the five frozen probes (md5s verified against HANDOVER records pre-run), 60
games each, to set wave_ghost's field profile against the same instruments
our line is scored on. Package for Magnus when in: parity head-to-head +
field profile + the 0-4 incoming-UR read. The slot call stays his.

TRAP for the tape (also in HANDOVER): `fcode submission download -o <path>`
writes a ZIP at <path> — extract it; a zip-as-botdir makes arena report
"every match failed to produce a result" (bot-B load failure), which burned
one full 480 run this session.

### 2026-08-07 17:59 (from `date`) — builder arm: BOOT (session 13)

Booted via /builder. All four monitors re-armed (tools/monitors/, state
re-baselined silently in the new scratchpad). Tape row 17:58: 1589 @ 266,
rank #24 — one rated match landed since wrap, +18 over the 1571@265
activation row; v67's window baselines from 1571@265 per the post-wrap rule.

opp_v67 downloaded. SLOT BAR RUNNING (registered above): _v76e51 (Eir 5.1)
vs opp_v67 (wave_ghost), all maps x 16 seeds x both seats = 480. Verdict +
tape row when it lands; slot conversation is Magnus's per team norm.

Research arm handshake received 17:57 (successor session online); its queue
confirmed and registered: v66 production read (Team 48 0-5 at 17:55 = the
battery-family sample, and a LOSS — check the rotation latch under losing
pressure too), Viktor5776, wave_ghost decode. Research heads-up in flight:
three incoming URs completed ~17:58 (1-4 team lazy, 2-3 Lorem Ipsum, 2-3
SmartFridge) — NOT fired by this arm, so they're other teams challenging us,
which means they ran our ACTIVE bot at runtime; version pins pending from
research. If v67-ran, wave_ghost's first field read opens 5-10 across 3
opponents.

### 2026-08-07 18:32 (from `date`) — builder arm: IDENTITY ADJUDICATED + x3r0/Magnus slot decision + Eir 6 regression

IDENTITY CLOSED (research hold resolved): bots/opp_v67 is GENUINE — fresh
re-download byte-identical (zip 700dfeb5..., main.py 27b33652...). The
gunner anomaly dissolves: **wave_ghost is a fork of OUR Eir 4** — diff to
_v74e4 is 304 lines (vs 2,268 to x3r0's own v89) — with a sentinel-snipe
overlay and a PRIMARY_SENTINEL selector (first forward turret = sentinel,
later ones = gunner; opp_v67 main.py ~1570). Production 1-gunner-in-25 =
the conditional path rarely firing vs the field; arena mirror gunners =
Eir-4-inherited behavior both sides. Swap anomaly = shared per-(map,seat)
opening geometry, not a harness bug. ALL measurements stand (480 parity,
field profile); the INTERPRETATION changes: not independent convergence —
one lineage, and v67 DROPS our measured v65/v66 pieces (I/J/H/latch/cap).

TEAM DECISION (Magnus relayed x3r0, ~18:30): KEEP v67 — x3r0's own Fable
read: 104-100 direct/204 (parity, matches our 51.9/480), ~7pts better vs a
common baseline (CIs overlap but direction consistent), stress 89/100 w/ 1
traceback vs 92,90. No dispute from this arm: our tape said bar-not-met
before the decision. x3r0's takeaway 3 (graft I/J/H onto v8) is EXACTLY
re-adding what the fork dropped — we hold the measured specs.

BUG REPORT CORRECTION (for x3r0 via Magnus): Eir 5.1's run() catches ALL
exceptions and prints ONE traceback per unit lifetime by design
(_v76e51/main.py:832-843) — the unit is NOT deleted; the print is the
diagnostic. Underlying exception still real + hunted: NOT reproducible vs
opp_v67/cad/band/kladde on hive/seed-42 (kite_proxy-specific). ASK routed
to x3r0: the traceback text (it is in his fixture's replay bot output) or
the kite_proxy zip; fix lands in minutes with either.

EIR 6 FIRST BATTERY (tape row 18:32): as-built REGRESSES — v63 30/55,
band 60/88, v67 32/52 paired; kladde/ouro soft-neg; cad flat; 0 crashes.
Pattern = sporks-ammo bank drain (worker's red flag). Ablation running
(_noammo = K+floor, _konly = K) vs the two clear-regression instruments.
K's verdict pends ablation — do NOT read the battery as killing piece K.

orizon_probe LANDED + FROZEN md5 aa7ab7185e5e1f6906071a72eb48d843:
signature reproduced (first plant fp_dsq 9, creep 9,5,1,1,1; eider seat A
+ nordkap seat B smokes, 0 crashes, deterministic, gunner-only). Gentler
than family wild exemplars (3 harvesters, 65-82 shots vs their 116-207) —
safe direction, same convention as ouroboros_probe. Validation vs the
family battery-class + fidelity ledger entry = next cycle with the fleet
work. Research: wave-ghost-first-read + T48 leg absorbed; production
signature reference (1 gunner/25 games, snipe r4-30 dsq 18-32) matches the
fork+selector explanation cleanly.

### 2026-08-07 18:34 (from `date`) — research arm: session-13 deliverable set complete; salvage + specs

All registered research rows LANDED. Durable summary (pings die with
sessions):

- **wave_ghost first field read** → docs/research/wave-ghost-first-read-
  2026-08-07.md. Forward-sentinel core-snipe strangler; one gunner in 25
  platform games; three measured loss modes (snipe dies → permanently
  dark; out-tempoed by healing batteries; economy/tiebreak collapse);
  family-split answered (Team 48's broken fire establishment vs lazy's
  heal-while-shooting). ARENA IDENTITY FLAG open with the builder: the
  20-game rerun's opp_v67 does not match platform v67's signature —
  everything platform-derived is unaffected; the 480/field-profile
  verdicts are the builder's to re-verify.
- **Viktor5776 v2** → docs/research/viktor5776-classification-2026-08-07.md:
  econ-first pure-greed, zero turrets, 250-ammo fossil bank; nudges the
  econ pool row up; no probe warranted.
- **v66 salvage (CAD leg)** → docs/research/v66-salvage-cad-leg-2026-08-07.md:
  rotation latch HELD under losing pressure (0 fast flips, 8 gunners, 5
  games); dump cap dies UNVERIFIED (no r1000 game in v66's 39-min life) —
  carry to Eir 6 reads. NEW CAD v107 signature: corner ferry loop (17
  throws → one tile in g3) = cheapest denial target measured today; also
  first observed abduction of OUR builder (g2 r32). Throw map v66-era-
  pinned per the standing constants rule.
- **axis-split** → docs/research/axis-split-our-games-2026-08-07.md:
  underpowered (2/96 archived matches are ours) — becomes meaningful as
  the --mine archive accumulates; method + script reusable.
- **ARCHIVER SPEC (shared-infra clause, builder fixes):** (1) dedupe is
  manifest-only — add file-existence check (all 5 games + meta present →
  mark archived) so research direct-pulls aren't re-downloaded; my 25
  direct-pulled game files for b92d7da8/e71e0b65/b41a1d2a/03af6569/
  a7aa49ec sit in replay_archive/ with standard names but are NOT in the
  manifest. (2) The --mine pass is defeated by the final
  `todo.sort(completedAt desc)` + PER_CYCLE cap — our matches should get
  reserved slots ahead of globals, or 03af6569-class items queue behind
  fresh globals for cycles.
- Research budget spent this session: 25 game files direct (10+5+10),
  all declared pre-pull, all paced ≥60s, all archived locally.

### 2026-08-07 18:35 (from `date`) — builder arm: EIR 6 REFUTED AS-BUILT; cycle verdicts

VERDICTS (tape rows 18:32/18:35): **Eir 6 first implementation REFUTED — all
three pieces PARKED.** K sits below baseline in all six paired comparisons
including its own value case (orizon_probe: konly 46.7 vs baseline 58.3).
Mechanism suspects for the redesign: heal-on-quiet-rounds burning builder
actions, and K x role coverage (forward roles heal instead of acting —
worker risk 5). Sporks ammo policy: refuted AS-PORTED (bank drain; needs an
economy guard = redesign, and our sentinel-heavy mix may just not be
sporks' gunner economy). Pop floor: never isolated — owes one clean leg
next cycle before any verdict. The DESIGN AIMS survive: baseline vs
orizon_probe at 58.3 shows the family fight is real and close; K's aim was
right, its trigger was too broad. Dev dirs kept: _v77e6, _v77e6_noammo,
_v77e6_konly (disposable ablation variants).

orizon_probe FROZEN (5th instrument, md5 aa7ab718..., tape row) — the
point-blank battery class finally has a local exemplar; add to every
future gate.

RESEARCH ABSORBED: CAD salvage read (latch HELD in production under losing
pressure — v66's rotation latch is production-verified; ferry-loop
signature noted as new CAD material). Traceback hunt BLOCKED on x3r0's
traceback text or kite_proxy zip (ask routed via Magnus; correction also
routed — run() catches, unit not deleted, one-per-lifetime diagnostic
print).

NEXT CYCLE (queue, in order): (1) K redesign with narrow trigger
(core-adjacent + recent-damage only, budget kept); (2) pop-floor isolation
leg; (3) the graft question — x3r0's v8 + I/J/H merge may become the team
line; our specs are the contribution either way; (4) F root fix +
kladde_probe_v2 (kladde settled?) from the standing queue; (5) traceback
fix when x3r0's data arrives.

### 2026-08-07 18:46 (from `date`) — builder arm: BASE-PURITY VERDICT — base clean, K refutation CONFIRMED, mechanism pinned

Per the pre-stated decision rule (tape row 18:46): _v77e6_alloff matches
baseline on both guards (v63 60.0/55.0, band 91.7/88.3) and mirrors
_v76e51 at 58.3 (≈50, no verdict) — **the refactor is exonerated**, the
base-defect hypothesis is refuted (its r0-divergence evidence was the
NOISE_ON salt, see 18:4x exchange), and the Eir 6 piece verdicts STAND,
now with a proper control cell. Clean attribution: konly vs alloff on the
SAME base = v63 45/60, band 55/91.7 — piece K alone costs ~15/~35 pts.

MECHANISM PINNED (builder code audit + research decode jointly): K's trunk
half never fires (depth gate 8 > gunner dmg 7 → one-reload qualify window,
behind TI floor and core-first ordering), so K-as-built is ONLY un-gated
core-heal-from-r0 — which consumes builder turns mid-fight (27-31% of
builder turns in fast band losses). Dropping the SLOT_UNDER siege gate was
the specific error. The actual sporks trunk mechanism was never tested.

K REDESIGN SPEC (next cycle lead): keep the income budget + per-builder
shares (measured safe), RESTORE the siege gate on core heal (under-attack
only, budget-capped — the starvation fix K was for), replace the trunk
trigger with proactive heal-any-damage-when-budget-allows (sporks-style),
keep H standdown. Pop-floor isolation leg still owed. Sporks ammo stays
refuted as-ported.

Session totals at this checkpoint: 2,258 arena games today (480+300+20+
660+240+120+18+180+240 incl. the failed-extraction 480), 6 instruments, 5
research deliverables absorbed, 2 two-arm adjudications both resolved with
evidence (identity: genuine fork; purity: base clean). Two-arm protocol
paying for itself in both directions in one session.

### 2026-08-07 18:51 (from `date`) — research arm: board drained, wrap-safe

Ferry pre-mortem closed the last open research thread (PARK; ship-robust
opening constants kept — registry row + deliverable). No live subagents,
no pending relays, downloads budget closed at 25 files (all declared,
paced, archived). Session-13 research set, all in docs/research/, all
version-tagged: wave-ghost-first-read, viktor5776-classification,
v66-salvage-cad-leg, axis-split-our-games, k-drag-diagnosis (corrected
19:00), cad-ferry-premortem. Successor queue = builder's 18:49 list:
(1) Eir 6 production read when a clean lineage version ships (pre-ordered),
(2) dump-cap verification on the first r1000 game under an Eir-lineage
ship, (3) axis-split re-run once --mine accumulates, (4) instrumented
CAD challenge decode if the builder ever spends it.

### 2026-08-07 18:56 (from `date`) — builder arm: SESSION 13 WRAP (Magnus restarting both arms for the next major-version run)

State at wrap: v67 (x3r0 wave_ghost) live by team decision, 1575 @ 271 —
window +4 net from its 1571@265 baseline over 6 matches. No open builds:
Eir 6 refuted-with-control, dev dirs kept for lineage (_v77e6 + _noammo/
_konly/_alloff/_flooronly ablation set, _v78e6b = clean unmodified base
copy). Eir 6b worker + pop-floor isolation are QUEUED NOT STARTED (rows
above) — the successor's first builds, spec in the 18:46 note + task text
mirrored in HANDOVER. Blocked: x3r0 traceback data (correction routed).
MONITORS: all four are THIS session's task processes — they DIE at this
wrap; /builder step 3 re-arms (~30s, scripts in tools/monitors/).

Session 13 ledger: slot case measured (parity + field equivalence + fork
discovery), team slot decision supported, Eir 6 cycle run end-to-end
(build → battery → ablation → value case → purity control → controlled
refutation with mechanism + redesign spec), orizon_probe built + frozen
(5th instrument, battery class covered), 2,438 arena games, two arm-vs-arm
adjudications resolved on evidence with one catch each way, protocol
incident-log grew one rule (NOISE_ON provenance). Tape current, all
verdicts evidenced. Research arm wrapped clean at ~19:15 (its 18:50-ish
message = its wrap note; all deliverables landed/corrected/registered).

### 2026-08-07 19:12 (from `date`) — research arm: successor online; monitor-gap ladder relay

Successor research session booted per protocol (coordination tail, spitball
tail, docs/research/ inventory, handshake ping sent to the builder session).
Queue inherited unchanged from the 18:51/18:56 wrap notes: (1) Eir 6b
production read when a clean lineage version ships, (2) dump-cap
verification on the first r1000 Eir-lineage game, (3) axis-split re-run
once --mine accumulates, (4) instrumented CAD decode if spent. All
builder-gated; watch state.

MONITOR-GAP RELAY (monitors died at the 18:56 wrap; `match list --mine`
checked 19:10 — free tier, no downloads). Timezone key, verified: platform
timestamps are UTC = local − 2h (the 15:58-59 platform triple-UR rows are
the builder's "~17:58 incoming URs" exactly). Completions since the last
monitored window, all v67-era (row shows plain "OpenSverige", not "(OLD)"):

- 03e63d07 ladder **L 2-3 vs Lunds Stallions** (seat A), 19:06 local —
  post-wrap, unmonitored. Note: session 13 celebrated Lunds seat-B 0-5→2-3
  under v65; this is a seat-A 2-3 loss under v67.
- 2b92b4fd ladder **W 4-1 vs 0033** (seat B), 18:55 local — right at wrap;
  may or may not be in the wrap's "+4 net over 6" figure.
- Pre-wrap but possibly post-last-monitor-tick: fb23a610 L 1-4 Ouroboros
  (18:47, seat-lock pattern intact), ce6ec7e2 UR L 1-4 SmartFridge (18:39),
  ba007b91 ladder **L 2-3 OopsGotYourElo** (18:36 — old watchlist flagged
  OGE as H's designed prey, but v67 dropped H; the loss is consistent with
  the fork lacking the endgame switch, unverified), b3656fe7 ladder L 0-5
  Kings College Munich (18:26).

Tape absorption is the builder's; no verdicts implied here. Elo not
queried (builder's monitor surface).

### 2026-08-07 19:14 (from `date`) — builder arm: SESSION 14 ONLINE — monitors re-armed, both queued builds firing

Successor builder booted per /builder (HANDOVER top block + coordination
tail + monitor check). MONITORS RE-ARMED 19:11, all four (elo_logger 5-min
/ match_watcher 2-min / opp_watcher 10-min / replay_archiver 30-min),
state in the fresh session scratchpad, first polls = silent re-baseline —
research item 3 (axis-split --mine accumulation) can start its clock now.

Research 19:12 monitor-gap relay ABSORBED: v67 1W-4L ladder since 18:26
incl. post-wrap L 2-3 Lunds (seat A) and L 2-3 OGE (H-prey watchlist echo,
unverified). Elo trajectory read comes from the fresh logger baselines —
no rollback/trajectory verdict on one relayed window; slot remains team
decision (v67 stays per 18:30 team call) unless the 20-match check says
otherwise.

FIRING NOW (registry rows above): (1) Eir 6b worker on _v78e6b (K' per the
18:46 spec; smoke-verify the trunk trigger actually fires — the v1 lesson);
(2) pop-floor isolation battery, 3×60 sequential, matched noise-on,
targets alloff 60.0/91.7 + baseline orizon 58.3. Gate after both land:
guards (v63 55 / band 88.3 / kladde 80 / ouro 80 / cad 50) + orizon value
leg (beat 58.3) + slot bar vs opp_v67 480 (51.9 to beat). Traceback hunt
stays BLOCKED on x3r0 data.

### 2026-08-07 19:16 (from `date`) — builder arm: POP-FLOOR ISOLATION LANDED — floor is CLEAN/POSITIVE, rides along with K'

Tape row _v77e6_flooronly (0 crashes/180, md5s verified): guards FLAT at
their controls (v63 60.0 = alloff 60.0; band 88.3 = baseline 88.3), and
the orizon_probe value leg is POSITIVE — 71.7 [59.2,81.5] vs baseline
58.3 [45.7,69.9], +13.4 directional. Notable for the decode ledger: on
the SAME orizon leg, konly measured 46.7 — the floor and K moved in
OPPOSITE directions on the family instrument. The floor's design aim
(population sustain under point-blank pressure) looks real; K-as-built's
drag was never the floor. Verdict per the pre-stated rule: POP_FLOOR_ON
= True in Eir 6b; worker amended mid-flight 19:16. Attribution stays
possible via the isolation row if the combined gate surprises.

### 2026-08-07 19:26 (from `date`) — builder arm: EIR 6B WORKER LANDED, mechanisms probe-proven; GATE STAGE 1 FIRING

Worker report absorbed (registry row updated). The v1 lesson closed
properly: every K' mechanism has positive firing evidence BEFORE the
battery — trunk arm 221 firings in one smoke game (70 at under=0, the
state v1's dead gate could never reach), core arm 148 firings across 4
games with ZERO outside the siege signal, budget defer observed binding.
0 tracebacks, probes removed, post-removal reruns clean. ast/finally
checks pass. Builder sign-offs: MEDIC_TI_FLOOR stays (bank-solvency
guard, lineage behavior), H-standdown stays trunk-only (= 5.1 shipped
behavior). SPORKS_AMMO_ON now actually False (v1 had shipped it True);
POP_FLOOR_ON True per the 19:16 isolation verdict.

Worker red flags on record pre-measurement (ranked, full text in its
report): (1) budget caps siege core-heal that 5.1 did unboundedly —
deliberate (budget IS the 972-heal starvation fix) but strictly less
defensive in the rush window; first suspect + lever (base-grant retune /
under-siege exemption) if band regresses. (2) shared ledger: trunk arm
can drain the core arm's share pre-siege. (3) ungated trunk arm on the
fjordgate/lighthouse flip maps is battery-unmeasured (smoke budget was
eaten by core heals there). (4) restored gate's cost unproven (probe
artifact). All testable by stage 1 legs.

GATE STAGE 1 RUNNING (registry row): 6 × 60 vs v63/band/kladde/ouro/cad/
orizon, baselines the _v76e51 rows 55.0/88.3/80.0/80.0/50.0/58.3. Stage
2 = 480-game slot bar vs opp_v67 (51.9 to beat) only if stage 1 clean.

### 2026-08-07 19:31 (from `date`) — builder arm: EIR 6B GATE FAILED; K' ablation grid running

Gate stage 1 FAILED (tape row 19:28, registry): v63 35.0 vs 55.0, band
53.3 vs 88.3 — both CLEAR; value leg flat (orizon 56.7 vs 58.3); cad the
one soft-positive (60 vs 50). Stage 2 slot bar NOT fired. The key
attribution fact: flooronly measured 60.0/88.3 on the same instruments
same-day, so K' costs ~−25/−35 WITH the floor riding — worse than v1's K
despite every mechanism now provably firing (the worker's smoke probes).
Prediction score: worker red flag #1 (budget caps siege core-heal that
5.1 does unboundedly; builders hit left=0 by r10-27 under rush) called
the band crater before the battery ran.

ABLATION RUNNING (registry row): three cells × v63+band, 60/leg —
notrunk (capped core arm alone → prices the cap, suspect #1), coreexempt
(core = verbatim 5.1 unbounded semantics, trunk budgeted → prices the
trunk arm, suspect #3; this cell IS the K'' candidate shape if clean),
koff (toggle off → purity control, expect ≈ flooronly). Verdict logic
pre-stated: if notrunk ≈ flooronly, the trunk arm is exonerated and the
cap is the drag → K'' = coreexempt shape. If coreexempt ≈ flooronly, the
trunk arm is cheap and the cap is the drag (same conclusion from the
other side). If BOTH sit below flooronly, the two arms are independently
harmful and the sporks mechanism doesn't port to our mix at all — park
K-line, keep floor, move to the graft question (queue item 3).

### 2026-08-07 19:35 (from `date`) — builder arm: ABLATION UNAMBIGUOUS — cap was the drag; EIR 6C (K'') gating now

Grid landed 19:33 (tape row _v78e6b-ablation): the budget cap on core
heal was THE drag, confirmed from both directions — capped core arm
ALONE reproduces the band crater (56.7) with no trunk arm present;
exempting the core restores band completely (95.0 [86.3,98.3], above
both controls). Trunk arm EXONERATED and hint-positive vs rush. Purity
control clean on band (91.7); its v63 leg 46.7 vs flooronly's 60.0 noted
honestly as overlapping n=60 noise (v63 legs swing ~±12 at this n).
Decode census NOT commissioned per the pre-agreed rule (grid clean).

Sporks lesson now fully extracted across two failed builds: heal-as-
income-line-item PORTS for trunk repair; core defense must NEVER be
budget-capped in our mix. The 972-heal endgame starvation case stays
unfixed (= 5.1 shipped behavior, retained knowingly); ENDGAME_RND
standdown on the core arm is a parked follow-up, deliberately NOT a
ride-along.

EIR 6C = bots/_v79e6c (md5 8aaa91e6...), ast-verified behaviorally
IDENTICAL to the measured coreexempt cell (comment canonicalization
only). Contents vs 5.1: budgeted proactive trunk repair + pop floor
(isolation-verified) + refuted ammo policy actually OFF. Gate stage 1
running (registry row): 6 × 60, v63+band re-run fresh for independent
confirmation. Stage 2 = the 480 slot bar vs opp_v67 (51.9) if clean.

### 2026-08-07 19:47 (from `date`) — research arm: MAGNUS DIRECTIVE — no self-initiated wraps

Relayed from Magnus (verbatim intent): sessions have been handing over
automatically; he does not want that. BOTH ARMS keep working until Magnus
explicitly calls a wrap-up. A drained queue means watch state (say you're
blocked and hold), not a wrap. Wrap mechanics (research state note,
HANDOVER successor block, monitor teardown) fire ONLY on his call — session
13's autonomous wrap killed the monitors and left a ~15-min unwatched
ladder gap, which is exactly the cost this rule removes. Research side
codified in .claude/commands/research.md + auto-memory; builder side:
please mirror in HANDOVER operating notes (your surface) and ack. Proposed
as a protocol-doc amendment too — one line under Boot sequences ("Sessions
wrap only on Magnus's explicit call") — pending your ack per the bilateral
rule.

### 2026-08-07 19:52 (from `date`) — research arm: MAGNUS PROCESS PROPOSAL — retro cadence

Magnus asked whether every new version should trigger a self-improvement
retro (workflow + harness + bot learnings). Research recommendation, wired
pending builder ack: NOT a full retro per version (ship cadence today was
3 versions/day — it would tax the build loop, and tape verdicts +
production reads + the incident log already capture the bot and incident
layers inline). Instead, three layers:
(1) PER VERSION, micro: when a version's verdict settles, the arm holding
the datum appends a "process delta" — 1-3 bullets, what slowed us / what
to change — to the coordination note of the verdict. ~2 min, captures the
friction that never becomes an incident.
(2) PER WRAP-CALL: the full retro (vault daily-retro playbook, seeded by
the accumulated deltas) runs when Magnus calls the wrap — composes with
the 19:47 no-self-wrap directive; deltas become config/protocol/vault
changes there.
(3) TRIGGER-BASED: incident-log rules keep landing immediately, unchanged.
Builder ask: ack layer (1) as shared discipline (it touches your verdict
notes), and the protocol doc gets one line under channels if you ack.

### 2026-08-07 19:50 (from `date`) — builder arm: V68 CHOKEWALL LIVE (x3r0, mid-gate); EIR 6C PASSES STAGE 1; stage 2 rebased + running; acks and process items

THE SLOT MOVED MID-CYCLE: x3r0 uploaded v68 "chokewall" 19:12 local,
auto-activated over v67 (elo_logger caught it — see process gap below).
Ladder under v68: 1579→1589, #25, climbing. His 19:26-28 four-UR burst
(Jython/sporks/not-adgato/Pivot) reads as self-field-probing; all four +
his 3 fresh ladder matches are archived. ASK (research, jumps queue):
v68 first read — graft-or-new identity vs v8/wave_ghost, mechanism
behind the name, loss modes. Local copy bots/opp_v68 md5 04811b4a...

EIR 6C GATE, full arc on tape (rows _v79e6c + _v79e6c-ext-pool): stage 1
PASS after soft-guard resolution — the kladde "regression" was half
stale-baseline (re-legged: pooled baseline 74.2/120, not 80; matched
n=120 delta −6.7 overlapping = accepted trade, eider/hive heal-into-
barrage geography, parked fix no-trunk-heal-into-live-gun-ray); ouro
pooled 72.5 = exactly its v64 long-run. Carried by orizon +16.7 (44%
class), v63 +6.7, band +5.0. STAGE 2 RUNNING vs opp_v68, 480, bar =
beat the holder. Ship decision after stage 2; slot call Magnus/x3r0.

ACKS + PROCESS (all applied): no-self-wrap → protocol Boot-sequences
line added (bilateral on record) + HANDOVER session-14 header mirror;
retro cadence (1) micro process-deltas ACKED (research adds the
Channels line). NEW INCIDENT-LOG CANDIDATE (mine): monitor wake lines
sit unread in background task files — v68 activation wake sat ~30 min
while I was heads-down. Interim rule (in HANDOVER header): read all
four monitor output files at every natural wake-up. Better fix →
spitball. Archiver sort bug: found, fixed, caught up (2-line fix +
comment in replay_archiver.py; "ours-first" was defeated by the
newest-first sort — also explains the Memtrace miss).

PROCESS DELTAS, Eir 6b/6c verdicts (retro item 1, first practice):
- Worker red-flag ranking predicted the 6b band crater precisely —
  consider a cheap red-flag-#1-targeted screen (1 leg, 60 games) BEFORE
  full 6-leg gates on redesigns.
- Two stale-baseline catches in one cycle (kladde 80.0/60 noise-high,
  koff v63 46.7 scare): 60-game single legs keep masquerading as
  baselines. Rule candidate: any guard verdict that would FAIL a gate
  must first re-leg its baseline to n≥120 matched regime before the
  fail stands. (This turned a would-be 6c refusal into a pass with a
  documented soft trade — cheaper than the redesign it nearly triggered.)
- Mid-gate slot flips happen (v68 landed between stage 1 and stage 2):
  check `fcode status` / elo tail BEFORE firing any slot bar.

### 2026-08-07 19:53 (from `date`) — builder arm: EIR 6C SLOT BAR NOT MET (46.0 vs v68); 6c KEEP as lineage head; session-14 work committed

Stage 2 landed (tape row _v79e6c-slotbar): 46.0 [41.6,50.5]/480 vs
chokewall — below the beat-the-holder bar, weaker than our 51.9 showing
vs v67, and another half-the-games-reach-r1000 tiebreak grind. NO SHIP.
v68 stays (and is climbing live). Eir 6c = KEEP: the cleanest measured
head of our lineage (class-weighted +16.7/+6.7/+5.0 over 5.1, kladde
soft −7 traded and documented). The 4.5-pt slot gap has two candidate
closers, both gated on research's v68 first-read: the graft conversation
(chokewall + our 6c pieces — Magnus/x3r0 call, same shape as x3r0's own
announced I/J/H plan) and a 6d cycle led by the parked kladde fix
(no-trunk-heal-into-live-gun-ray) + tiebreak-discipline work (ti-
collected decided 240/480 — the drip/dump levers matter vs chokewall
exactly as they did vs wave_ghost).

PROCESS DELTA (6c slot bar): the mid-gate v68 flip cost nothing this
time only because stage 2 hadn't fired — the new check-status-before-
any-slot-bar rule (19:50 note) is now load-bearing, keep it.

Housekeeping: session-14 work committed (archiver sort fix, HANDOVER
s14 header, protocol amendments, coordination/tape). The protocol doc's
"commit 43eb673" reference for the --mine fix predated the actual
commit (phantom hash, research wrote it in good faith describing my
fix) — corrected to the real hash in the same commit.

### 2026-08-07 19:57 (from `date`) — builder arm: watch-state wake check — Powerpuff ROLLBACK v26→v18 (opp_watcher)

First catch for the new read-the-wake-files rule: opp_watcher flagged
Powerpuff Girls v26 → v18 (rollback, CAD-style). Effect: their v26-era
rows and any census-era Powerpuff characterization are now suspect;
class coverage via flotte_probe (strangle/chip class) is unaffected as
an instrument, but wild-fidelity for Powerpuff specifically is unknown
under v18. No action owed now — logged for the next cycle that touches
the strangle class. Elo meanwhile: v68 1580@277 #26 (−9 on one match,
below wake threshold, normal variance). Research's two v68 agents
mid-flight on the tiebreak-led read; builds holding.

### 2026-08-07 20:03 (from `date`) — builder arm: v68 code-read absorbed; routed nav check ANSWERED (we route around barriers)

Research's v68 code half landed: NOT the graft (I/J/H absent at
file:line), NO endgame switch (static post-r300; tiebreak-#1/#2 engine
via r300 labor surge + never-dump, tiebreak-#3 fat unspent —
post-r300 H-class levers UNCONTESTED = the 6d anchor), chokewall
namesake near-dead on the current pool (fires archipelago+saga only,
+0-round detours), snipe carries over → our v67 measurements apply.

ROUTED CHECK answered on my surface (relayed with file:line): nav
routes AROUND enemy barriers — _bfs_direction :3581-3634 blocks every
visible barrier both teams; no blocked→attack logic exists; BARRIER
sits at attack-priority 7/8 (last-resort adjacent fire only). The
30-Ti peck bait does not exist for us; residual exposure ≈ nil.
Out-of-vision barriers = re-route on first contact (detour, not peck).

HOLDING for the replay half (tiebreak trajectories) before drafting
the graft brief for Magnus + the 6d spec. Graft question status
sharpened by headline 1: x3r0's announced I/J/H graft has NOT happened
in v68 — our specs remain the outstanding contribution, and 6c's
pieces (trunk repair, floor) plus post-r300 tiebreak discipline are
additive on top.

### 2026-08-07 20:09 (from `date`) — builder arm: 6D RACE FIRED (2 branches, Magnus's experiment directive); v68 read complete → graft brief

Magnus directive ~20:05: run 2+ directions in parallel, keep the best —
formalized as the 6D RACE (registry rows + pre-stated keep rule: same
fresh 6-leg gate, class-weighted winner; both-clean+orthogonal →
composite re-gated vs both parents; survivor → 480 slot bar vs v68).
Branch A _v80e6d_kfix (kladde fix: trunk arm skips ray-covered targets,
D/J scan reuse) and Branch B _v80e6d_tb (delivery continuity: F-root
facing verification w/ free destroy+rebuild, post-r300 harvester
sustain, chain-first trunk priority) BOTH SPAWNED 20:08 on the 6c base.
Branch B's lever was fixed by research's replay half: ALL v68 r1000
games resolve at tiebreak #1 delivered-Ti; v68 lost 9/11 grinds on it,
5/11 via a permanent delivery-freeze defect; no post-r150 second plan.

GRAFT BRIEF (for Magnus → x3r0, evidence in docs/research/v68-chokewall-
first-read-2026-08-07.md + our tape): (1) v68 is NOT the graft — I/J/H
absent at file:line; x3r0's announced plan is still open and our specs
remain the contribution. (2) The complementarity is now production-
crisp: his line wins fast or not at all (median win r97, 11/13 wins
pre-r140, no endgame behavior after r300, delivery freezes in 45% of
long games); our line grinds and holds tiebreaks. A graft = his
fast-kill opening + our grind/tiebreak endgame. (3) Direction
recommendation: his snipe overlay is ~300 additive lines outside every
diff hunk with a self-contained window (r4-30, role 0) — porting IT
onto OUR 6c/6d head is now the cheaper graft direction vs re-adding 5+
pieces to his older base; propose as experiment branch C once the A/B
race resolves, x3r0 reviews. (4) His two open defects (delivery freeze,
small-map defensive sentinel) are fixable on his side with our F-root
insight — same disease our linker had ("occupied-implies-correct").

Research read absorbed in full incl. reconciliations (production
barriers = old plug code, choke planner never observed; TLE delta =
platform variance; wave-ghost gunner-rate footnote). Defect candidates
(delivery-freeze code look at opp_v68, small-map gate) parked on the
queue behind the race.

### 2026-08-07 20:36 (from `date`) — builder arm: wake check — v68 L4 STREAK (1561@280 #26); older-5 archived; race gate running

match_watcher fired STREAK L4: v68 latest L 1-4 vs Clankers, rating
1589→1561 over 4 matches. v68 window now NET NEGATIVE: 1579@273 →
1561@280 (−18/7 matches) after opening +10. No verdict off 7-9 matches
— but it's context for the graft brief and the race: the slot holder
is not running away with it while our 6d branches gate. Archiver: the
older 5 gap matches all landed on the regular cycle (fix fully
confirmed); our-match archive now 13 and growing — research's
axis-split re-run (queue item 3) is UNBLOCKED. Race gate (960 games)
running, ETA ~20:50.

### 2026-08-07 20:43 (from `date`) — builder arm: RACE VERDICT (inconclusive-clean) + THE CRASH THREAD: ancestral pave bug found, x3r0 traceback hunt RESOLVED, piece N gating

RACE (tape row _v80e6d-race): both 6d branches guard-clean vs parent,
neither value case met at n. KEEP both as dev heads; no composite, no
ship. Branch B's tiebreak thesis is NOT refuted — pooled win rate is
the wrong instrument for it; the proper test (replay-saved
delivered-tiebreak split, tb vs 6c control vs opp_v68) is the queued
next measurement.

THE REAL FIND of the race: the "crash" counts were caught-diagnostic
prints miscounted by arena (it splits stderr on Traceback blocks; our
run() catch prints once per unit), and every single traceback — both
sides, all legs — is ONE ancestral bug: the pave block calls
is_tile_empty(pave_prev) assuming pp is adjacent "by construction",
which a between-turns LAUNCHER THROW violates → GameError aborts the
whole dispatch for that unit that round (and every round it recurs).
Both lineages build launchers; v68 inherits the bug (12-23 affected
units/120 games live on the ladder — graft-brief material for x3r0,
we can hand him the one-line fix). HIGH-CONFIDENCE match to x3r0's
Eir 5.1 kite_proxy/hive stress traceback — the BLOCKED hunt is
RESOLVED without his data. PIECE N (_v81e6e, md5 31a10eb2): one-line
is_in_vision guard, skips the pave never the move, strictly recovers
lost actions. Compact gate running (v68 120 primary read = crash
count → 0; v63/band guards).

PROCESS DELTAS (race verdict):
- Arena's crash counter conflates caught-and-printed diagnostics with
  fatal crashes — for any lineage bot that prints tracebacks from a
  catch, read crash counts as "units that hit ≥1 exception", and
  diff them against the parent's leg before treating them as new.
  (Candidate arena.py improvement: distinguish blocks followed by
  engine unit-deletion messages, if the engine emits any.)
- The race's fairness amendment (adding value legs per branch) was
  right but insufficient: value cases whose mechanism lives in a
  GAME-SHAPE subset (tiebreak games) need their instrument designed
  BEFORE the race fires, not diagnosed after. Pre-commit the split
  measurement next time.
- 41 "crashes" on a clean-guard branch nearly triggered a defect
  hunt inside the new code; the 5-minute foreground-traceback sample
  (attribute FIRST) prevented it. Rule: attribute crash counts by
  traceback before any code-level suspicion.

### 2026-08-07 21:02 (from `date`) — builder arm: KCM read absorbed — C1 home-ring = leading next-cycle candidate; ferry re-check PARKED

Research's KCM classification absorbed (CAD-family launcher-ferry,
cad_probe covers them; 9-1 mechanism = their counter-gunner kills our
forward sentinel in median 15 rounds while we under-shoot 3-20x;
predictor: ≥3 their turrets at d²≤36 of our core = 9/9 losses). Their
~1585 Elo is substantially farmed FROM US — the cheap counter C1 (home
sentinel ring, re-aiming what we already build; our only win did it:
one r19 gunner kill and they never re-established) flips both cells.
QUEUE: C1 = leading candidate for the cycle AFTER the 6e slot bar
resolves, on whatever base wins. C2 (orizon-recipe battery on their
soft core) = the play-the-players pairing if C1 gates clean.

GRAFT-BRIEF NUANCE from this read: x3r0's snipe overlay is exactly
what the KCM/CAD counter-gunner farms — a graft inherits that
exposure; our home-defense identity is what beats KCM. The merge
needs C1-style home cover for the snipe, not just the snipe.

Ferry-loop owner re-attribution (research's own correction flag on
the premortem): PARKED — no verdict depends on it tonight; run it in
any idle window, no collision risk from my side.

### 2026-08-07 21:10 (from `date`) — builder arm: 6E SLOT BAR = PARITY (51.0/480, bar not met); session-14 arc closed to a decision point; CAD v115 + Lunds v43 bumps

Slot bar landed (tape row _v81e6e-slotbar): 51.0 [46.6,55.5]/480 —
parity, not a clear-50 flip case. v68 stays per team norm. But the
board state for the Magnus/x3r0 slot-and-graft conversation is now
fully measured: (a) our line moved 46.0 → 51.0 vs the holder on a
ONE-LINE bug fix (piece N), crashes 0-vs-128 asymmetric; (b) the same
one-liner is a gift for his line; (c) the matchup is a delivered-
tiebreak grind (248/480) where his engine has a measured freeze
defect and no post-r300 plan; (d) his ladder window is net-negative
(1561@283 #28, L4 streak within it); (e) KCM farms his snipe class
and our home identity is the measured cheap counter — the graft
needs both parents. Next builds queued in order: C1 home ring (on
6e base), tiebreak-split instrument for Branch B's thesis, archive
backfill. Lineage state: _v81e6e = base (6c+N); 6d branches KEEP-dev
pending their instruments.

PROCESS DELTA (6e slot bar): the compact 120-leg's 55.0 was mean-
regressed optimism by 480 — pre-registered full-bar discipline
prevented a premature ship claim; keep the two-stage (compact →
full) pattern but never quote the compact number as the case.

WAKE ITEMS: CAD v107→v115 AND Lunds v42→v43 (opp_watcher) — cad_probe
fidelity + the v107-era opening constants + the KCM-CAD calibration
adds are all SUSPECT until re-frozen; the whole CAD family moved
tonight (KCM label 7→1, Powerpuff v26→v18, CAD v115). Probe
maintenance list grows; nothing tonight depended on cad legs beyond
guard duty. v68 ladder: 1561@283 #28.
