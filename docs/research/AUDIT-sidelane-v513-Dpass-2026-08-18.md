# SIDE-LANE AUDIT — v513 `_v513siegecrew` D-checklist pass (s51, 2026-08-18 ~03:3xZ)

**Provenance:** produced by an opus audit subagent (read-only brief: no edits, no fcode, no
games), commissioned by the side lane per its s50 inherited item 1. **Verification status:**
the agent reproduced the report's headline table and mechanism table from the raw per-game
TSVs (exact, all columns) and diffed every mutant tree for its intended flip; the side lane
itself re-verified the F1 anchors on the shipped tree (`doctrine.py:2594` `LOKI_FS_CREW=True`,
`:2653` `FS_HOME_TURRET_RESPONSE=True`, `main.py:1097` gate; and the clean lines
`FS_SALT_GATE=True`/`FS_SALT_LATCH=False`/`FS_CREW_ON=False`) before publishing. Everything
else below is the agent's read of primaries, quoted verbatim; per this lane's charter these
are FLAGS with anchors, never verdicts. Prescriptions are one line and belong to the owning
lane.

**Consequence-ranked summary (full text below):**
- **F1 (top):** door-sentinel response ships **ON by default** (`FS_HOME_TURRET_RESPONSE=True`)
  and is live in the fired config; the builder's own 20:32:18Z note says it *"needs Magnus's
  nod (home doctrine)"*, the 20:38:56Z spec re-labels it "flag-gated [my recommendation]", and
  the 21:34Z morning-decisions list omits it. Magnus's approval is NOT-ESTABLISHED either way.
- **F2:** the report scores DEFENCE_ADMISSION on the **superseded** timely-rate estimator and
  calls it "the primary"; the governing estimator (ITT RMST₃₀₀, PROGRAMME.md:534-540) appears
  nowhere. Computed from the artifacts: **RMST₃₀₀ delta −12.93 rounds (faster), 95% CI
  [−25.8, −0.1] — passes directionally**, but no prereg/MDE exists so it is a read, not a
  cleared bar.
- **F3:** the entire evidence base lives in a **foreign session's /private/tmp scratchpad**;
  the report cites `scratchpad/v513_build/` which does not exist in the repo. Nothing in the
  repo reproduces 49/90. (~3 KB/TSV to bank.)
- F4-F12 + NOT-ESTABLISHED items and the CLEAN list: below.

---

## AGENT REPORT (verbatim)

Read-only pass. No edits, no commits, no `fcode`, no games run. All arithmetic below re-derived by the audit agent from the build agent's own artifacts, independently located and tallied.

**Headline first: the report's numbers are real.** All eight headline columns reproduced exactly from the raw per-game TSVs (`shipA2+shipB2+shipC` = 49/90, 41 kills, 24 k≤300, 39 core deaths, 10 r1000, 4 tic-zero, medmine 565, medkill 281, tb 0; v512 `a+b+c` = 13/90, 13, 8, 68, 9, 46, 0, 241, 0). Control identity is established, not inferred. The flags are process/scope flags, not fabrication.

### FLAGS (ranked)

**F1 — TOP RANK. The door-sentinel response ships ON by default, and it is the one plank the builder himself logged as needing Magnus.**
`bots/_v513siegecrew/doctrine.py:2653` → `FS_HOME_TURRET_RESPONSE = True`, gated at `main.py:1097` on `if not (LOKI_FS_CREW and FS_HOME_TURRET_RESPONSE)` with `doctrine.py:2594` `LOKI_FS_CREW = True` — so it is live in the fired config. The record: `docs/coordination.md` 2026-08-17T20:32:18Z — *"door-sentinel response needs Magnus's nod (home doctrine)"*; six minutes later at 20:38:56Z it becomes *"(2) door-sentinel response, flag-gated [my recommendation, executed under the run-with-recommendations standing directive]"*. The 21:34:47Z landing note names TWO Magnus decisions parked for morning (second body, sentinel-after-salt) — the door response is not among them. It also self-describes as piercing a standing doctrine: `main.py:1088` *"⭐ THIS DELIBERATELY PIERCES LOKI_QUIET_ON"*. "Flag-gated" was satisfied in letter; the flag's default is ON and the nod is unrecorded. **No approval record found either way — NOT-ESTABLISHED whether Magnus saw it.**

**F2 — The DEFENCE_ADMISSION bar is scored on the SUPERSEDED estimator, and labelled "the primary".**
Report line 15: `| **kills ≤ r300 (ITT, the DEFENCE_ADMISSION_BAR primary)** |` and line 26: *"**The timely-kill rate ROSE 8.9% → 26.7%**, so the kill-round bar is cleared on its primary (ITT) form"*. `PROGRAMME.md:534-540` moved the operational estimator to **ITT RMST₃₀₀** on 2026-08-16T05:36:10Z and demoted the timely rate to a *reported diagnostic* (`PROGRAMME.md:548-550`) — explicitly because the timely rate *"passes it only by correlating with win share, r²=0.93"*. RMST₃₀₀ appears nowhere in the report. Compounding: there is **no prereg for v513** (none in `docs/research/PREREG-*`, no row in `docs/prereg/BARS.tsv`, no row in `results.tsv`), so there is no registered MDE and "cleared" cannot be scored as the required exclusion.
Computed from the artifacts — it passes, but nobody had the number:

    v513 SHIP (A2,B2,C)    n= 90  RMST300= 276.09  se=5.06
    v512 parent (a,b,c)    n= 90  RMST300= 289.02  se=4.15
    DELTA = -12.93 rounds (FASTER)   95% CI [-25.8, -0.1]

**F3 — The entire evidence base for the day's largest iteration lives outside the repo, in another session's private temp, and the report cites a path that does not exist.**
Report line 46 cites `scratchpad/v513_build/probe_store`. `scratchpad/v513_build` **does not exist in the repo** and was never committed (`git log --all -- 'scratchpad/v513_build*'` → empty). The real artifacts are at `/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/82720aae-f502-4b10-9dd5-ad5f55d16b94/scratchpad/v513_build/` — a *different session's* scratchpad, session-scoped and deletable. Nothing in the repo can reproduce 49/90. (`scratchpad/ringladder_build` is on disk but likewise uncommitted; `scratchpad/` is otherwise tracked, 1,921 files.)

**F4 — Deviation 1 (the second body, −15.6pp) is not code-vintage matched: 2 of 3 crew-ON blocks predate a behavioural edit that all 3 ship blocks carry.**
Report lines 84-85 call it *"same fixture, same seeds, fired config"*. Seeds/maps/side-alternation are matched (verified). The **tree is not**: `main.py` moved the `_door_turret_turn` call from before the raider-assignment block to after it at 23:24 (diff of the 23:02 `inst/` copy vs the shipped tree). Ship blocks: `shipA2`/`shipB2` 23:33, `shipC` 23:25 — all post-move (this is *why* A/B were re-run as A2/B2, correct discipline). Crew-ON blocks: `v513a` 23:03, `v513b` 23:05 — **pre-move**; only `cwONC` 23:26 is post. So report line 92's per-block pairing *"15 v 11 · 17 v 13 · 17 v 11"* has two cross-vintage pairs. **Direction survives** — the one matched pair is 17 v 11 (20pp) and the matched n=60 pre-move pair in `doctrine.py:2725-2726` is 24/60 v 32/60 (13.3pp) — but the report's claim of a matched fixture is not accurate, and `doctrine.py:2721-2726` now carries a *different* number of record (13.3pp @ n=60) from the report's (15.6pp @ n=90) for the same decision.

**F5 — A fail-to-exclude is converted into a positive attribution.**
Report line 98: *"It is not the denial; it is the second body."* The evidence is line 96-98: `FS_CREW_DENY_SEAT=False` at n=60 read *"24 wins / 20 kills / 31 core deaths — indistinguishable from the full crew"*. Half-width at n=60/arm is ~17.9pp (the builder's own figure, `doctrine.py:2738`), so "indistinguishable" excludes almost nothing. Per the exclusion-restatement rule, an elimination claim must be stated as *the CI excludes a denial effect of size X*, which this cannot do. Unremarked instrument oddity: the two arms return an **exactly identical triple** (24 / 20 / 31) — confirmed (`nodeny AB` n=60: win 24, kill 20, died 31; `crew_ON` n=60: win 24, kill 20, died 31) — on a fixture the report itself says is non-deterministic (line 74-75). Both mutant trees are correctly built (`mutf/nodeny` carries `FS_CREW_ON = True` **and** `FS_CREW_DENY_SEAT = False`), so this is coincidence, not a broken mutation — but a triple-exact match deserved a sentence.

**F6 — Two shipped decisions sit below the builder's own one-draw-law floor (n≥60/arm).**
(a) Report lines 113-114: *"`FS_SALT_LATCH = True` … scored **8 wins / 15** against the strict rule's **9 / 15** — no gain, so the strict rule ships and the variant stays off."* That is **n=15/arm** (verified in `mut/tally2.tsv`: `latch_var` wins=8, `on` wins=9); MDE at that n is ~35pp. Mitigation: the strict rule ships because Magnus ordered it, so the measurement is decorative — but "measured-no-gain" was relayed to Magnus at 21:34 as a decision input.
(b) Report line 132-133: *"`convert_ammo`'s minimum drops from 4 to 1 … (the 4-titanium floor blocked 19% of conversion rounds on **the diagnostic's instrumented atoll game**)"* — a shipped constant change resting on **one game**, against the builder's own PROCESS DELTA 2 (`coordination.md` 21:42:29Z).

**F7 — The headline win share does not exclude parity, and no interval is printed for it.**
49/90 = 54.4%; at local DEFF 0.98 the half-width is **10.2pp → CI [44.3, 64.6]**, which contains 50%. The report prints CIs for deviation 1 (14.5pp, correct — agent gets 14.4) but none for the headline; the coordination relay at 21:34:47Z reads *"THE PLANK'S FIRST LOCAL WIN"* unqualified. The programme screening standard is `X3R0_SLOT_RULE: on_60pct_pm2pp_screen…` (`PROGRAMME.md:28`) at the n=5,400 local fixture (`PROGRAMME.md:71`). Mitigating: the builder's s51 boot plan queues exactly that 5,400 shard.

**F8 — No rule-6 scope rider anywhere in the report, and several closure-shaped sentences.**
The research arm's standing rider is explicit (`coordination.md` 20:46:42Z item 5: *"local screens prioritise, they cannot confirm or retire (rule 6); for siege planks the local fixture is doubly wrong"*). The report contains no such sentence and carries: line 26 *"the kill-round bar is cleared"*; line 98 *"It is not the denial; it is the second body"*; line 108 *"The stall … is real but no longer fatal"*; line 116-117 *"**The kill now mostly comes from elsewhere** … the collar plus the economy plus the home defence are carrying it"* (no arm isolates those three).

**F9 — D21 domain-narrower-than-claim, worst three.**
(a) Report line 71: *"ladder priority inversions **0 of 804 logged rung firings**"* — 804 not reproduced. `FS RUNG` lines: `rep_logship` 507, `rep_onlog` 604 (= 1,111); the mut arms sum higher still. The *finding* holds (0 lines matching `inver` across the logged replays), but the denominator's population is **NOT-ESTABLISHED**. What would establish it: the builder naming which arms the 804 pools.
(b) Report line 7/72: *"0 tracebacks in 670 grid games + 165 mechanism/demo games"*. Actual grid TSVs hold **730** rows, all with `tracebacks=0` (so the claim is conservative, but the denominator is wrong), and a real `Traceback` **does** exist in the build's own smoke output — `smoke/i_nordkap.err`: `NameError: name 'sys' is not defined` at `main.py:557`, inside the `FS_MAG_TRACE` print. It is fixed in the shipped tree (`import sys` at `main.py:32`, `FS_MAG_TRACE = False` at `doctrine.py:2781`) and could only fire under a local instrument flag — **no live hazard** — but a NameError in `_core` would have permanently destroyed the core, and the near-miss is nowhere in the report.
(c) Report surprises 4 and 5 (*"22 of 23 fatal tiles were on a previously-seen ray"*, *"0 of 40 attacked"*) are the v512 three-map autopsy's 24 games, stated as general facts about sentinels.

**F10 — The v512 baseline of record contradicts the same day's banked, powered read, unreconciled.**
Report line 13 uses v512 = **13/90 (14.4%)** on 5 maps. `results.tsv:506` (`ringladder-final`, banked 20:46:05Z) reads **25.00% [21.01, 28.99] at n=452** against the same incumbent on a 15-map pool — a CI that **excludes 14.4%**. The map-pool difference explains it (that row itself says *"80% of rows on geometry the grid never saw"*), but the report never names the tension, so a reader takes 14.4% as v512's number.

**F11 — Two different "ship arm" denominators in one report, undisclosed.** Line 13 headline is 49/90; line 128-129 scores H against **48/90** (*"spawn-purpose-off scored 52/90 against 48/90"*). Both reproduce (`shipA2/B2/C`=49, `shipA/B/C`=48; `spoffABC`=52). The reason is recoverable from artifacts and is *good* practice — spoffA/B are pre-move so they pair with shipA/B — but it is not stated, so the report reads as inconsistent.

**F12 (low) — The header's diff-vs-parent counts don't reproduce.** Report line 6-7 says *"doctrine +263, siege +383, main +309/-15, eco +58/-4"*; measured against `bots/_v512ringladder`: doctrine **+275/-0**, siege **+411/-3**, main **+318/-15**, eco **+59/-4**, raid 0/0. siege's three deletions are unreported.

### CLEAN

- **D1 line check — CLEAN, both ways.** `bots/_v513siegecrew` matches `bots/_v[2-9]??*` (`PROGRAMME.md:7`); excluded controls still excluded. (Aside, pre-existing and not v513's: `bots/_v99foo`-shaped names would also match `_v[2-9]??*`, against the widening note's claim at `PROGRAMME.md:59` that it *"cannot collide with the Eir era"* — only true if the Eir era is strictly v1xx.)
- **Control identity — ESTABLISHED, matches PROGRAMME.** `run_grid.py:19` and `mutants.py:21` both set `OPP = bots/_v488beltbreak2` = `PROGRAMME.md:8` INCUMBENT. `COMPARE_AGAINST: previous_line_iteration` also satisfied (v512 parent arm on identical seeds).
- **Headline reproduces exactly** (every column, per-block lines included).
- **Magnus gate (a), sentinel-after-salt: STRICT, correct.** `doctrine.py:2614` `FS_SALT_GATE = True`, `:2633` `FS_SALT_LATCH = False`, grace 8 at `:2621`.
- **Magnus gate (b), second body: OFF, correct.** `doctrine.py:2741` `FS_CREW_ON = False`; sub-switches consistent.
- **Fired config is clean of instruments** (`FS_LOG`/`FS_DRAW_ON`/`FS_MAG_TRACE` all False; the three inherited `LOKI_*_LOG` flags predate v513 and are shared with the control).
- **Every mutant arm verified to carry its flip** (all six `mutf/` trees diffed, eleven `mut/` arms cross-checked; `mutf/spON` misnamed but fed the correct spawn-off block — naming only).
- **Mechanism table reproduces line-for-line** from `mut/tally2.tsv`; flag-off behavioural check reproduces (flagoff n=60: 12/44/27 vs v512 a+b 9/46/30).
- **Traceback check done, not skipped:** 0 across all 730 grid rows + 165 mechanism games; 296 `.err` files grepped, one hit in `smoke/` only (F9b).
- **Paired design confirmed** (5 maps × 6 reps, disjoint seed families 7400s/7500s/7600s, side alternation identical across arms).
- **The report's own hedges are honest and reproduce** (collider caveat on median kill round; 14.5pp half-width; measured noise-floor placebo; the disclosed replacement-latency miss of Magnus's ~15-round cap).

### NOT-ESTABLISHED (with what would settle each)

1. **Magnus's approval of the door-sentinel response.** Settled by: Magnus's answer, or a coordination line recording it.
2. **The `804` rung-firing denominator.** Settled by: the builder naming the arms it pools.
3. **Whether the v513 fixture survives.** Artifacts live in a foreign session's `/private/tmp` scratchpad. Settled by: copying the TSVs into the repo (~3 KB each) or re-running under a repo path.
4. **v513's r300 bar under the governing estimator, as a scored exclusion.** RMST₃₀₀ = −12.93 [−25.8, −0.1] passes directionally, but no prereg registered an MDE. Settled by: the SIEGECREW prereg the builder's s51 plan already queues.
