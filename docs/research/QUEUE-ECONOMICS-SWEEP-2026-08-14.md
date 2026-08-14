# QUEUE ECONOMICS SWEEP — all 45 unblocked rows against the pre-build filters

**Written 2026-08-14T15:21:20Z (`date -u`) by a builder-spawned opus agent, at
HEAD `992964b` (2026-08-14 17:21:07 +0200). Commissioned in
`docs/coordination.md:49141-49152`.**

⛔ **THESE ARE RECOMMENDATIONS TO RESEARCH, WHO OWNS THE QUEUE. I decide
nothing, I changed nothing, `QUEUE.md` is untouched and nothing is committed.**
Every KILL / LIVE-PATH / SEGMENT label below is a *proposal with its arithmetic
attached* so it can be argued with, not a ruling.

---

## WHY THIS SWEEP EXISTS

Pre-build economics has only ever run **per-pull** — the row about to be built
gets the filters, the backlog does not. Today that filter killed two arms in
minutes before any build cost was paid:

* **LAUNCHOFF** — `QUEUE.md:144` (row 57, dead): the launcher premium
  `LAUNCH0 − BOTH0 = +6.34pp` was measured on a bot that built a launcher in
  ~93% of games. **v140 builds one in 8.2% (7 of 85 games)**, so the same
  mechanism scales to **0.56pp** pooled — below screen resolution. Not admitted.
* **ferry #57 / launcher timing** — `docs/coordination.md:43847-43860`: the s37
  family sweep at **n=5408/arm** had already priced the whole lever
  (LAUNCH0 52.77 · LATE160 51.42 · LATE80 50.74 · FERRY0 50.15 · RES20 48.95 ·
  RES0 48.63 · EXILE0 47.02 · BOTH0 46.43 · LAUNCH2 44.67 · LAUNCH3 43.73).

**Nobody has ever swept the ~37-row backlog with those filters. This is that
sweep.**

## THE ARITHMETIC FRAME (stated up front so every cell below is checkable)

1. **THE BAR.** `GATE-1000` futility moved **48 → 51** on Magnus's verbatim
   refinement *"at n=1000 anything below 51 is considered bad now"*
   (`docs/coordination.md:48771-48774`, 2026-08-14T14:45:59Z). At n=1000 the
   band is ±3.1pp, so **a true +2pp arm survives the 51 gate ~74% of the time,
   a true +1pp arm 50%, a true +0.5pp arm ~37%.** ⇒ **the screening question is
   "can this plausibly reach +2pp POOLED".** *(And the gate's own error rate is
   on record: `GATE-1000 < 48` discarded a true-50 arm 10.3% of the time —
   `docs/coordination.md:48958`. The 51 bar is stricter, so that number is a
   floor.)*
2. **THE FIXTURE'S MAP MIX IS FIXED AND KNOWN.** `tools/overnight.sh:68` runs
   **all 15 pool maps uniformly**, so `n=5400` = 360 games/map and
   **900-area = exactly 5/15 = 33.3% of every screen.** ⇒ a 900-only mechanism
   needs **+6.0pp on the segment** to read +2.0pp pooled. *(And the shard TSVs
   carry `map` and `seat` natively — `scratchpad/overnight/*.tsv` cols 4 and 6 —
   so every segment split in this document is free.)*
3. **POOLED ≈ COVERAGE × CONDITIONAL.** Coverage = the share of the SCREEN's own
   population in which the mechanism can fire at all. That is the LAUNCHOFF
   arithmetic, applied row by row.
4. **COUPLING CLASS ROUTES THE BUDGET** (`docs/coordination.md:44913-44919`,
   R5). Screen-trustworthy = field-universal / self-knowledge.
   **COUPLED-INCUMBENT-ABSENT = the payoff needs a behaviour our own control
   does not express, so the self-play screen reads ~50 BY DESIGN and cannot
   clear 51 whatever the plank is worth.** Those rows are LIVE-PATH, not screen
   candidates.
5. **LOCAL BARS ARE NOT WIDENED.** `QUEUE.md:142` (#55): local corefill is
   balanced-by-construction, **pair-weighted DEFF 0.98 across 124 shards**. The
   1.37-1.83 constants are platform-only. Segment bars take DEFF ~1.07
   (`docs/coordination.md:49004-49005`).
6. **A SEGMENT NEEDS A DIRECTION AND THERE IS EXACTLY ONE PRIMARY**
   (Obligation 15a/15b, `docs/coordination.md:48992-49005`;
   `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md:382`).
   Every SEGMENT label below names one primary and its expected sign.

---

## THE TABLE — all 45 unblocked rows (order = `tools/queue_check.py`)

| # | title (short) | COVERAGE — number + arithmetic | ALREADY-MEASURED | PATH | one-line reason |
|---|---|---|---|---|---|
| **36** | 900-area eco-as-kill-enabler | 33.3% of screen games are 900-area (5/15 maps, `overnight.sh:68`); needs +6.0pp on the segment to read +2.0pp pooled | **UNDERECO 51.56 · ECORAID 53.22 · ECORAID2 52.91**, all ±1.33 @ n=5400 vs `_v197mapcode` | **LIVE-PATH** (ship/leg decision) | Lever already screened three times ABOVE the bar; and ECORAID's own class split (CQ 54.3 / STD 53.4 / **GRAND 52.4**, `coordination.md:44503`) says the eco→pressure conversion pays LEAST on 900s — the row's 900-specific premise is contradicted by its own best arm. |
| **37** | Tap the belt (offensive siphon) | r1000-insurance channel ≈ **6% of games**; core-tank denial channel is opponent-class-conditional and 0% in self-play (our tree ships SIPHON_DENY) | novel — no shard | **LIVE-PATH** | 6% × any plausible conditional cannot reach +2pp; the denial channel needs the core-tank class, which self-play cannot express. Also carries a real build cost (dead-end stub ⇒ a full route home, `doctrine.py:896`). |
| **38** | Kidnap/crash at 900 scale | launcher present **8.2%** × 900-area **33.3%** = **2.7%** of screen games — **and crash-induction is 0% by construction in self-play** (our own `eco.py` carries the guard the exploit targets) | launcher family priced @5408/arm; **no shard has ever tested a border throw** | **LIVE-PATH** | Two multiplicative blockers plus a control that is immune to the mechanism. Precondition now RELEASED — see #17 below. |
| **39** | Opening book of the new pool | modal-tile confidence 75-89% on top cells; re-based mechanism (raider targeting prior) fires in ~100% of games | novel — no shard | **SCREEN** | The book is **(MAP, SEAT), not (TEAM, MAP)** — field-wide map geometry — so self-play accuracy ≈ field accuracy and the screen is trustworthy. Table already built, zero games owed. |
| **40** | Pre-seal our own siege ring | camp precondition fired **9/25 = 36%** of control games across 3 of 5 opponents; our core dies in 46.3% of games; our own forward arm reaches their ring in 78% of games so the mechanism IS expressed in self-play | novel for the HOME ring (MAPSEAL is the enemy-seat seal) | **SCREEN** + defensive rider | 36% coverage needs +5.6pp conditional to reach +2pp pooled — reachable for a 3-Ti/tile denial. Carries `DEFENCE_ADMISSION_BAR: kill_round_non_regression`. |
| **41** | Forward-sentinel siting d²14-32 + barrier | forward sentinels 2.28/game in 78% of games — but the VALUE premise (their reactive next-door counter-gunner) is a behaviour our control does not express | **STANDOFF (`_v204standoff`) 50.56 ±1.33 @5400 — the siting half, DONE, flat.** SENT41 built and **DEFERRED** as a harm-gate screen under the 51 bar | **LIVE-PATH** | Siting half measured flat at full n; barrier half is COUPLED-INCUMBENT-ABSENT and its screen was deferred for exactly that reason (`coordination.md:48775-48779`). |
| **42** | Volume-not-sequence | ≥2 simultaneous siege sentinels in **48%** of games (54+29 of 173) | **TWORAID 50.63 · COMBO 52.30 · ECORAID (UNDERECO+TWORAID) 53.22 + 52.91 repl.**, all @5400; FWDFLOOR8 45.88@2788 | **LIVE-PATH** (ship decision) | The row's QUESTION is closed (binder = travel seriality) and the lever is measured; what is left is a ship call, not a screen. |
| **43** | Barrier-in-base crash confirmation | n=6 events in ONE game; **self-play coverage 0 by construction** (our pathing is guarded) | novel | **LIVE-PATH** | The row already specifies its own instrument: a two-arm unrated leg. A screen cannot see a crash our own control cannot suffer. |
| **44** | Self-audit: 87.6% of TLE ceiling on 30×30 | n/a — corpus cut over platform replays, zero games | cut RAN s36 (median 8,748µs, p95 8,803, n=31 900-area) | **TOOL/CUT — re-read now** | The row's own v140 carry flags it: `_l4_repair` adds nested 4-direction adjacency scans per builder-turn BEFORE its own CPU check. **The 87.6% figure has not been re-read post-L4 and every plank below spends from that budget.** |
| **45** | Kill the builder, not the ladder | iter-1 dose fired **1/16**; iter-2 **0/16**, every refusal `gate=eco`; engine fact removed the melee path entirely (builder melee CANNOT target enemy builder bots) | IDLEPECK 44.57@949 (adjacent peck arm, negative) | **MERGE into #47/#58** | Both surviving tools (turret fire, launcher eviction) are already the subject of #47 and #58. Keeping this as a separate row double-counts one prize. |
| **47** | Conditional siege launcher | **the arm CREATES its own coverage** — approach detection fired 15/16 in dose, builds land r48-55 — so the 8.2% blocker does not apply | **APPRLAUNCH 52.94 ±1.33 @5400 · APPRLAUNCH2 52.39 ±1.33 @5400 — a REPLICATED PASS above the 51 bar** | **LIVE-PATH** (screen already passed twice) | The row's own remaining ladder item is the pinned live leg vs CAL-3 C1/C4. No third screen is owed. |
| **48** | Parked-raider terminal idle | **27.5%** of games (1,981/7,203) · **10.68% of ALL builder-bot-rounds at v125** · **41%** of every bot-round at d²≤4 of their core (814,242/1,986,370) — **the highest coverage number on the board** | rung (a) widened peck REFUTED (+44.5 rnds); **IDLEPECK 44.57@949 · QUIET0 32.64@432**; rung (b) SALTREF RUNNING (48.71@700). **Rung (c) has NEVER been screened** | **SCREEN — rung (c) only** | RETIRE60 does **not** cover it: its carve-out (c) deliberately spares bots within d²≤8 of the enemy core (`coordination.md:48250-48256`), which is precisely #48's parked-raider population. Seat release is genuinely novel and self-knowledge-classed. |
| **51** | Aim the throw loop | **8.2%** launcher coverage ⇒ needs **+24pp conditional** to reach +2pp pooled; and the decode measured **marginal denial value = ZERO** in its own reference game (all 8 enemy builders idled from r47 regardless) | **AIMTHROW2 50.09 ±1.55 @4007** — flat, exactly as the arithmetic predicts | **KILL** | Coverage arithmetic and the measured screen agree. Can only revive downstream of a row that restores launcher coverage (#47/#58); it is not an independent plank. |
| **52** | Collar medic | requires enemy melee pecks at our barriers; **`LOKI_QUIET_ON=True` means v140 NEVER pecks ⇒ self-play coverage = 0 BY CONSTRUCTION** | novel (SEALREPAIR is L4 belt repair, a different mechanism) | **LIVE-PATH** | The row declares its own class: COUPLED-INCUMBENT-ABSENT, self-play reads HARM ONLY. Correctly labelled at stocking; nothing here changes it. |
| **53** | Seal timing/geometry sweep | seal fires in ~every game; SELF-KNOWLEDGE/field-universal ⇒ screen-trustworthy | **floor swept DOWNWARD only: SEALFLOOR0 54.74@5400 (SHIPPED as v140) + SEALFLOOR0R 53.13@5400 repl. · SEALFLOOR24 (upward) allocation-CANCELLED at 50.39@1022 · SEALFIRST (timing) cancelled 49.46@2022 · MAPSEAL cancelled at 22% while reading 56.66@1202** | **SCREEN** | The family already produced the biggest recent ship. **MAPSEAL at 56.66@1202 is the highest-leaning cancelled shard on the board and belongs to this row** — resume it before spending on the untested 24-arm. |
| **54** | The nav limit cycle | **11.58% of ALL builder-rounds** locked (183,489/1,584,948, v125 strict) · 47.6% of games · **midgard 35.6%** | **OSCLOCK 48.48@1869 · OSCLOCK2 46.49@1809 (dropped at GATE-1000 46.39@1800)** — two arms, both negative | **SEGMENT** — primary = **area>676 (the five 30×30s)**, direction = **fix helps MORE where locks are denser** | ⚠ **Both negatives were screened at a ~6.6× UNDER-DOSE**: the row's own base-rate note gives self-play midgard control **5.37%** against the real-opponent census **35.6%**. A pooled self-play screen is the wrong instrument for the one row with measured map heterogeneity. |
| **50** | Pave the walk-out → terminus-first | applies to **non-core-adjacent harvester sites only** (`_has_acceptor` counts the core); saving 1-2 stacks (10-20 Ti) per such harvester, against 7.78 harvesters/game | walk-out arm `_v211` **DEAD** on its own dose (harvester #1 lands r4-8 on adjacent ore); terminus-first never screened | **CUT-FIRST, then SCREEN** | The row already declares its own GO/NO-GO: the `bank_trace` first-delivery latency read. **Do not build before that number exists** — the row says so and it is the cheapest half. |
| **49** | Ore-barrier denial, defence side | n/a — corpus question, ANSWERED | (a) binds the tile (0.106× receipt, n=389 vs 1,853, z=−15.78); (b) WITHDRAWN as unresolved; (c) marker not cause; (d) dose = EARLY+TOTAL | **KILL (close as answered)** | The row's question is answered and its residual is already routed to #7 (demand evidence) and #47 (evict the planter). Keeping it open double-books those two. |
| **55** | Carry the DEFF into our tools | n/a — tools row, no games | constants measured 3× (1.45 implied · 1.529/1.366 rated · 1.833/1.434 unrated); local exempt at DEFF 0.98 | **TOOL — build** | One function, touches every platform verdict this repo types, and the correction can only make a bar harder ⇒ it can turn a positive into unresolved but never the reverse. |
| **56** | `target_value` prices off a stale cache | n/a — tools row, no games | measured at boot: Juusto printed ~1815 against a live 1883.3 | **TOOL — build** | It is in EVERY lane's boot sequence and it silently DROPPED the top target (Juusto 1877, +121, a 5-0 pays +21.37) for ~6 hours. A gate that omits the best target is worse than one printing a stale number. |
| **58** | Forward eviction launcher | builds its own launcher on trigger (like #47) so 8.2% does not bind; but the VALUE (their heal/repair staff on their own ring) is not expressed by our control | EVICT58 built + dosed; **screen DEFERRED** under the 51 bar as a coupled harm-gate | **LIVE-PATH** | Already fire-order #2 item 1 with a named customer (0033, 1837, +19.68 for a 5-0). Deferring the screen is not deferring the plank — correct as routed. |
| **59** | Don't get farmed | their throws land **60.1% after r150, median r209** — past our median kill 174 AND median death 187 ⇒ addressable window ≈ **39.9%**; self-play sees an enemy launcher in only **8.2%** of games | the row's own cost cut **found no cost** (signs disagree within-opponent; we BEAT both named users era-rated) | **KILL** | A measured annoyance with no shown leak, and the screen fixture is structurally blind to it. The row itself already ranks this below #58 for exactly this reason. |
| **60** | Rent, don't own | **SPLIT.** (a) general demolition / scale rent: SELF-KNOWLEDGE, ~100% coverage. (b) **launcher rent specifically: 8.2% of games — the LAUNCHOFF arithmetic exactly** | RETIRE60 RUNNING (n=385, no rate yet) | **(a) SCREEN (running) · (b) KILL as a standalone** | The engine fact is rules-level and admissible; but the *launcher* framing that motivates the row is inert in 92% of its own population. The value is in the general case (25-30 conveyors, 7 barriers, 5.4 harvesters per game), which is what RETIRE60 tests. |
| **61** | Lanes have no decision surface | n/a — process row | the firing that motivated it is **EXPLAINED** (both tripped rows were instrument defects; repaired, the day reads 0/6) | **TOOL — reduced priority** | The row says so itself. The two-directional positive control is the only part that still earns build time. |
| **2** | Kill the sentinel from off its axis | sentinel = 40 HP ⇒ **20 pecks × 2 Ti = 40 Ti + 20 raider-rounds** (act/move exclusive) to kill a 30-Ti building — the trade loses on the game's own arithmetic before any coverage question | **QUIET0 (full melee ablation) 32.64@432 · IDLEPECK (narrow melee) 44.57@949 · #48's widened peck +44.5 rounds SLOWER** | **KILL** | Three independent builder-melee reads are catastrophic and the peck-economics rider predicted it. "Off-axis is free" prices the return fire and ignores the 2 Ti/peck ammo diversion and the spent move rounds. |
| **3** | Clear more enemy turrets | universal coverage; sized at **+1.06 destructions ⇒ −0.72 net standing** (4.67→3.95), i.e. 15% of our own stock — **not −1.06, because destroying provokes rebuild at +32.1pp** | **NESTSHOT 47.14@507 · NESTSHOT2 48.38@1633** (allocation-dropped 45.75@1012; ⚠ its HARM reading is AMENDED to UNRESOLVED, `coordination.md:48951-48956`) | **SCREEN — priority-knob arm only** | The s39 decode names the working instrument (sentinel fire = 74.7% of removal damage; zero gunner-fired kills) and sentinels **cannot re-aim**, so the surviving arm is target priority inside the existing envelope. Two arms already below bar ⇒ this is the last cheap shot, not a fresh road. |
| **33** | Does `LOKI_GUNAXIS_PENALTY` do anything? | 0.60 gunner-covered forward deaths/game baseline | ⭐ **ANSWERED TWICE: GUNAX0 (`_v183gunaxis0` vs v116) 48.00 ±1.33 @5408 · GUNAXIS0 (`_v206gunaxis0` vs v125) 49.45 ±1.87 @2752. Both chassis, both BELOW 50 ⇒ ablating the flag COSTS us ⇒ the flag DOES something.** | **KILL (close as answered) — and RELEASE the #30/#31a gate** | The row's own promise was *"one local ablation answers what 5,000 archived games cannot."* It has been run twice, at 8,160 games, and nobody closed the row. Tier-0 rank is stale. |
| **34** | Backfill `wincond` | n/a — decoder column; 37.2% → ~97% coverage of unrated files | novel | **TOOL — build** | `R1000_IS_DEFEAT` is the central currency and 63% of unrated files cannot be read for it. One column, no extraction. |
| **35** | Per-game map name for unrated | n/a; validated proxy exists (mw×mh → 11 pairs, 4 ambiguous) | novel | **TOOL — low priority** | ⚠ The corefill fixture already writes `map` natively (`scratchpad/overnight/*.tsv` col 4), so this gap only bites `fcode match unrated` legs — and `mw`×`mh` already resolves the AREA CLASS, which is all Obligation 15 segments need. |
| **17** | Does the crash weapon actually fire? | purpose-built fixture (`_probe_border_raw` vulnerable, `_probe_border_guard` immune) ⇒ dose is 100% by construction, not a self-play screen | ⭐⭐ **ANSWERED — `scratchpad/crash_cells_s33_v2.txt`. A_ON_RAW: 13 border throws → 13 crashes, 5/24 games, 1.00 crashes/border throw. B_ON_GUARD: 16 border throws → 0 crashes. C_OFF_RAW: 16 border throws → 16 crashes. "MECHANISM: CONFIRMED."** | **KILL (close as answered) — and RELEASE #5/#38/#43** | The three-cell drive the row asks for HAS RUN and drove both ways. ⚠ **It also found something the row did not predict and nobody has consumed: the arm-OFF build lands MORE border throws than the arm-ON build (16 vs 13) — the incumbent's own farthest-tile EXILE ordering already produces the crash geometry, so the border ARM's marginal value is ~zero or negative.** *(The v1 output says the opposite and is superseded: it was UNDOSED, 0 throws in all three cells.)* |
| **16** | The non-strike surcharge | our own pre-r250 eco spend — SELF-KNOWLEDGE, ~100% coverage | ⭐ **SURCH30 38.05 ±3.63 @728 · SURCH90 26.42 ±3.56 @757 — two doses, MONOTONE in the dose, both catastrophic** | **KILL** | −12pp and −24pp at n≈750 with band ±3.6 is unambiguous and monotone: a bigger surcharge is worse. The only untried dose is one small enough to sit inside noise. |
| **5** | Crash induction at scale | bounded by the row itself: **only 2.62%** of enemy builder removals are no-damage AT ALL (360/13,743); launcher present in **8.2%** of v140 games | displacement channel priced (+0.265pp, prioritising-only); border channel never live-tested; **#17 now confirms the mechanism locally** | **LIVE-PATH — gated on a launcher existing** | The mechanism question is closed by #17; the open question (what share of the field is unguarded) is only answerable live. But it is inert until a build row (#47/#58) restores launcher coverage — and #17 says the incumbent's ordering already lands border throws, so the "arm" may be free. |
| **7** | Ore-barrier carve-out (offence) | 100% of games have enemy ore; #49 supplies the demand side — **0.106× harvester-receipt suppression at r≤60, 85.8% of barriers never cleared, ~30 Ti for them to undo our 3 Ti**; prescription 3-5 barriers, r≤60 | novel; we RETIRED the behaviour ourselves (ourver 76: 26/40 games; v125: 1/300) | **SCREEN** | Screen-trustworthy by construction: the transfer inference is *"their planner, like ours, routes around rather than clears"*, and in self-play the opponent's planner IS ours. ⚠ Channel is enemy economy = instrumental under `R1000_IS_DEFEAT`, so it buys the kill indirectly. |
| **8** | Seat-relative scan order | **100% coverage.** ⭐ **FREE MEASUREMENT MADE FOR THIS SWEEP: pooled over the five null/calibration shards (NULL114, NULL125, SHIPGATENULL, NULLSALT, NULL123) the seat gap is A 54.01% vs B 46.43% = 7.58pp, n=12,113 per seat, gap band ±1.26pp** — an independent confirmation of the row's 7.57pp at 3× the n. Current chassis alone (NULL125, n=5400): **A 53.63 / B 48.44 = 5.19pp**. | **GUNSEAT (`_v156gunseat`, v114 chassis) 51.04 ±1.33 @5408 · SEATREL (`_v216seatrel`, v125 chassis) 50.40 ±1.87 @2752** | **SCREEN — but the row's DECLARED fixture, which has never been run** | ⛔ **The two shards that "tested" this are structurally underpowered for it.** In a head-to-head shard the A−B gap is **symmetric by construction** (control's seat-A rate = 100 − treatment's seat-B rate), so a one-sided fix only HALVES the gap: predicted 8.02→4.9 with overall 51.55, observed GUNSEAT 7.69 / 51.04 — consistent with anything from no fix to a full fix. **The byte-identical null with BOTH sides seat-relative drives the gap to the ~1.8pp map residual, a 6pp move that n=5400 resolves easily. That is the row's own declared fixture and it has never been run.** |
| **10** | Blind their gun with their own body | our launcher **8.2%** × enemy gunner on a blockable ray × a kidnappable builder adjacent — compound, well under **3%**; and our own control builds 1.86 gunners/game against the field's 8-14, so the target is under-expressed too | novel | **KILL** | Two multiplicative coverage terms below the LAUNCHOFF threshold, plus an unsettled decoder predicate (exact-ray vs `ALIGNED_DEG=45`) that the row itself flags. |
| **13** | Ambush the rebuild | 3.01 enemy turret destructions/side-game × **22.6%** same-tile within 25 rnds = **0.68 ambushable events/game** (1.02 at d²≤2) | novel | **SCREEN — covering-turret variant only** | The melee variant is dead on #45's engine fact (builder melee cannot target enemy builder bots), so the only live design is a turret already covering the rubble tile — which is the branch the row itself calls "genuinely free". Modest at 0.68 events/game. |
| **14** | Idle builder gets a destination | **25.76% of builder-rounds** idle-and-free (same in wins at 27.59%) — second-highest coverage on the board | **DEST14A 50.49 ±2.94 @1113 (GATE-1000 50.64@1011, deferral CONFIRMED under the 51 bar). DEST14B never ran.** | **SCREEN — arm B only** | ⚠ The segment lean runs AGAINST the mechanism story: DEST14A legacy 52.3@373 vs big 49.6@740, i.e. the destination helps more where the walks are SHORT. Arm B (recall) is free discrimination — the row predicts opposite kill-round signs from the same pool — and it carries the defensive rider. |
| **19** | `NOISE_ON` must not be pinned | bites only batteries that pin it; **current shards do not pin it** | measured 68.8-80.6% degeneracy vs 0.007%; the "~30×" magnitude is RETRACTED, honest interval effective n ∈ [22, 5408] | **TOOL — low priority** | The row names its own cheapest purchase: one shard at `NOISE_ON=False`, 338 seeds/cell, to bound effective n. Do that or nothing. |
| **20** | The harvester target | `ECO_CAP=18` not binding at 7.78 harvesters/game (43% of cap) — so the row has **no named lever**; the candidate binder (builder deaths freezing harvester count) is #48/#54's territory | eco family screened instead: **UNDERECO 51.56 · ECORAID 53.22 @5400** | **MERGE into the eco family** | Title claim already demoted as false; the cap is not the constraint and the real one is another row's mechanism. A separate build here would re-test what ECORAID already banked. |
| **21** | The gunner count | 1.86/game against Pivot 10.77 — a 3-6× gap, the largest in the set; plank is ADDITIVE (gunners where LOS is already clear), not a swap | GUNFIRST 49.61@5408 · GUNSUB 48.32@683 · GBNOSHIELD 51.02@5408 · GBNS 49.70@3133 · GUNBLOCK 52.35@810 — ⭐ **but `GUNADD` (`_v163gunadd`), the ADDITIVE arm this row actually asks for, was cancelled at n=388 with NO RATE PRINTED** | **SCREEN — re-run GUNADD** | The row's own declared lever exists as a built tree and has never been read. Every other gunner arm tested a substitution or a placement, which `raid.py:639-641` correctly forbids. |
| **22** | We stop building turrets after r150 | r150+ us 1.95 vs 3.28-4.75 | no direct arm | **KILL (fails admission 1)** | The row's own GREP says the fall-off is **emergent — no explicit late-game gate exists**, so there is no constant or branch to name. It is a metric, not a plank, and the row itself ranks it lowest and says it may be entirely downstream of #20. |
| **23** | Forward placement | cap binds in **≤12.92%** of games (soft upper bound, alternation-invariant proven) ⇒ **~8× dilution** on any cap lever | ⭐ **FIVE arms, all ≤50.56: CAP6B 49.00@5408 · CAP12B 48.93@5408 (cap) · MINHARV1 47.24@5408 (timing 2→1) · FWDFLOOR8 45.88@2788 (floor 40→8) · STANDOFF 50.56@5400 (siting)** | **KILL the knob family · SCREEN the census fix separately** | Cap, timing, floor and siting have each been measured and none clears. **The one untested residual is the correctness bug**: `_live_fwd_guns` counts with a vision-bound `get_nearby_buildings()`, 35.6% of alive forward sentinels are invisible, 74.7% of over-cap builds had a blind census, and `SLOT_FWD_GUN` under-reports in 17.0% of games — feeding the endgame ammo conversion at `main.py:202`. ⚠ Sign is ambiguous: fixing it makes the cap bind MORE, and more forward guns screened neutral-to-negative. |
| **24** | The launcher singularity | n/a — pricing question | ⭐ **ANSWERED: the 2×2 is complete at n=5408/arm — LAUNCH0 52.77 · FERRY0 50.15 · EXILE0 47.02 · BOTH0 46.43 ⇒ premium −6.34pp** | **KILL (close as answered)** | The row's own pre-registered resolvability criterion is met. The surviving design question lives entirely on #47/#58/#60. |
| **28** | `LAUNCHER_RESERVE = 80` | affordability 5.7-12.4% of games — **and the s40 correction kills the lever outright**: `main.py:613` returns before round 160 (`LAUNCHER_MIN_RND=160`), so RESERVE cannot bind at all in the r6-r18 window where the fleet collapsed | ⭐ **ANSWERED: LAUNCHRES0 48.63 ±1.33 @5408 · LAUNCHRES20 48.95 ±1.33 @5408 — the dose sweep RAN and is negative** | **KILL (close as answered)** | Measured negative at two doses at full n, superseded by #47 on the row's own annotation, and the gate it names cannot reach the window it wants. Keep the affordability arithmetic as a citation, not as a build. |
| **30** | Station scorer: sentinel as threat | **0.32 forward builder deaths/game addressable** (ceiling 0.63) ≈ **25 Ti/game** against our ~4,077 Ti/game collected = **0.6% of our economy** | SENTSAFE2 (`_v188sentsafe_g`, penalise sites inside enemy turret coverage) **49.83 ±1.33 @5408** — the nearest arm, flat at full n; **and #33's gate is now RELEASED** | **KILL-CANDIDATE by arithmetic** | Reaching +2pp win share off 0.6% of our own economy is not plausible, and the closest built arm reads 49.83 at n=5408. The row already prices itself as "real but modest" and warns its own value case is unmeasured. |

---

## ⭐ THE BIGGEST FINDING OF THIS SWEEP — SIX ROWS ARE ALREADY ANSWERED AND NOBODY CLOSED THEM (five of them among the 45)

**These are not kills on economics. They are rows whose declared question has a
completed measurement sitting on disk.** Two of them are ranked in the fire
order's top tiers.

| # | rank today | the answer already on disk | consequence |
|---|---|---|---|
| **#33** | **Tier 0, item 2** ("cheapest decision-unblocker on the board, gates two other rows") | **GUNAX0 48.00@5408 (v116 chassis) + GUNAXIS0 49.45@2752 (v125 chassis)** — both below 50 ⇒ the flag DOES something | Close #33. **RELEASE the #30 / #31a gate** — they are no longer blocked. |
| **#17** | **Tier 2, item 5** ("Magnus asked for this directly") | **`scratchpad/crash_cells_s33_v2.txt`**: 13/13 border→crash on the raw probe, **0/16 on the guarded probe**, 16/16 arm-off. "MECHANISM: CONFIRMED" | Close #17. **RELEASE #5 / #38 / #43.** And consume the unpredicted half: **arm-OFF lands MORE border throws than arm-ON (16 vs 13)** ⇒ the border ARM may be worth nothing; the incumbent already produces the geometry for free. |
| **#24** | Tier 4 | the 2×2 complete at n=5408/arm | Close. Premium −6.34pp is the citation; the design question is #47/#58/#60's. |
| **#28** | Tier 3, item 8 | LAUNCHRES0 48.63 / LAUNCHRES20 48.95 @5408 + the `LAUNCHER_MIN_RND` correction | Close. |
| **#6** *(not one of the 45 — `queue_check` does not count it, no `GREP:` stamp; recorded here because it is still ranked Tier 4 item 16)* | Tier 4, item 16 | **BESTFITB (`_v145bestfit`) 49.08 ±1.33 @5408** — `tools/overnight.sh:109` runs `--tle 10`, so this IS the requested "repeat with the 10 ms TLE enabled", at n=5408 against the requested n=4,096 | Close, negative. |
| **#49** | stocked s37 | its own cut landed s39/s40 | Close; residual already routed to #7 and #47. |

⚠ **The pattern worth a retro line: five of these six are LAUNCHER or FLAG rows
whose answers landed in overnight shards, and the shard results are read by the
BUILDER at gate time while the QUEUE is owned by RESEARCH. Nothing in the loop
walks a completed shard back to the row that asked for it.** `#18`'s staleness
note in `QUEUE.md:406` warns that a GREP validates that a check RAN, not that
its result is still true — **this is the mirror defect: a row can be ANSWERED
and still pass every gate forever.**

---

## LIST 1 — KILL-CANDIDATES (ranked; the pooled screen cannot see it and no other path exists)

1. **#22 — we stop building turrets after r150.** Fails admission criterion 1
   outright: the row's own GREP says no gate exists and the fall-off is
   *emergent*, so there is no constant or branch to name. It is a metric.
2. **#51 — aim the throw loop.** 8.2% launcher coverage needs +24pp conditional
   to clear +2pp pooled; AIMTHROW2 read **50.09@4007**; and the decode measured
   marginal denial value at **zero** in its own best game. Not independent — it
   rides on #47/#58.
3. **#2 — kill the sentinel from off its axis.** Priced on the game's own rules:
   **40 Ti and 20 raider-rounds to remove a 30-Ti building**, plus three
   builder-melee screens at 32.64 / 44.57 / +44.5-rounds-slower.
4. **#10 — blind their gun with their own body.** Compound coverage under 3%
   (8.2% launcher × ray geometry × adjacent kidnappable builder), target
   under-expressed in the fixture, decoder predicate unsettled.
5. **#59 — don't get farmed.** The row's own cost cut found no cost; 60.1% of
   the dose lands after both our median kill and our median death.
6. **#30 — sentinel threat term.** 0.32 deaths/game ≈ 25 Ti/game ≈ **0.6% of our
   own economy**; nearest built arm 49.83@5408.
7. **#60(b) — the LAUNCHER half of rent-don't-own.** Inert in 92% of its own
   population. *(60(a), the general demolition case, is a live SCREEN and is
   running as RETIRE60 — do not kill the row, split it.)*
8. **#45 — kill the builder.** Not wrong, just double-booked: both surviving
   tools are #47's and #58's. Merge.
9. **#20 — the harvester target.** No named lever (cap not binding), and the
   real binder belongs to #48/#54. Merge into the eco family.
10. **#23's KNOB FAMILY (cap / timing / floor / siting).** Five arms measured,
    none above 50.56, on a lever diluted ~8×. *(The census-fix residual survives
    as a separate, sign-ambiguous correctness item.)*
11. **#16 — the non-strike surcharge.** Two doses, monotone, −12pp and −24pp.
12. **#49 — ore-barrier defence side.** Answered; close.

## LIST 2 — LIVE-PATH (screens are pointless; legs are the only honest surface)

Ranked by what a leg would buy, with the coupling reason attached.

1. **#47 — conditional siege launcher.** *Screen has PASSED TWICE (52.94 /
   52.39 @5400).* The only remaining read is the pinned live leg vs CAL-3
   C1/C4. **Highest-value live item on the board: it is the one row whose
   screen work is finished.**
2. **#58 — forward eviction launcher.** COUPLED-INCUMBENT-ABSENT (their heal
   staff); screen correctly deferred; already fire-order #2 item 1 with a
   named customer at +19.68/5-0.
3. **#52 — collar medic.** Self-play coverage **0 by construction**
   (`LOKI_QUIET_ON=True` ⇒ our control never pecks). Declared at stocking.
4. **#42 — volume-not-sequence.** Question closed, lever measured
   (ECORAID 53.22). This is a ship decision, not an experiment.
5. **#36 — 900-area eco as kill enabler.** Screened three times above the bar;
   ⚠ its 900-specific premise is contradicted by ECORAID's own class split
   (GRAND 52.4 < CQ 54.3) — the leg should test the eco→pressure conversion,
   not the map class.
6. **#41 — forward-sentinel siting + barrier.** Siting half already flat at
   n=5400 (STANDOFF 50.56); the barrier half needs their reactive counter-build.
7. **#38 — kidnap/crash at 900.** Screen blind by construction (our control is
   immune); **precondition now released by #17**; still gated on launcher
   coverage.
8. **#43 — barrier-in-base crash confirmation.** Same construction blindness;
   the row already specifies a two-arm unrated leg.
9. **#5 — crash induction at scale.** Mechanism confirmed locally by #17;
   the field-vulnerability share is only answerable live. Bounded by the row's
   own 2.62% ceiling on no-damage removals.
10. **#37 — tap the belt.** ~6% r1000-insurance channel plus an opponent-class
    denial channel self-play cannot express. Build only as a rider.

## LIST 3 — TOP 5 BUILD-READY, ranked by expected POOLED effect

| rank | row | expected pooled | the arithmetic |
|---|---|---|---|
| **1** | **#8 — seat-relative scan order, run as the DECLARED byte-identical null** | **~+1.5-1.9pp** (≈ +11-14 Elo) | Seat gap re-measured for this sweep at **7.58pp ±1.26 over 12,113 games/seat** (five null shards pooled), maps explain ~1.8pp ⇒ self-inflicted p ≈ 5.8-6.2pp on half our games. **The two head-to-head arms could not resolve it (the A−B gap is symmetric by construction); the byte-identical null drives the gap to the ~1.8pp map residual — a 6pp move that n=5400 resolves at ±1.3.** 100% coverage, mechanism not a knob. |
| **2** | **#48 rung (c) — terminal-idle seat release** | unpriced, **highest coverage on the board** | **10.68% of ALL builder-bot-rounds at v125** are ≥100-round silent parks; **41%** of all bot-rounds at d²≤4 of their core. TLE confound CLOSED (detector v2: 0 of 814,242 parked rounds were TLE ⇒ every park is chose-to-idle). Rungs (a) and (b) were screened; **(c) never has**, and RETIRE60's carve-out deliberately excludes this exact population. |
| **3** | **#54 — nav limit cycle, re-screened ON THE 900-AREA SEGMENT** | **+2-4pp on the segment** if the fix works at field dose | 11.58% of all builder-rounds locked; **midgard 35.6%**. Both existing negatives (OSCLOCK 48.48, OSCLOCK2 46.49) ran at a **~6.6× under-dose** (self-play midgard control 5.37% vs census 35.6%). Obligation 15: primary segment = area>676, direction = fix helps more where locks are denser; n=1800 on the segment gives ±2.3pp. |
| **4** | **#53 — resume MAPSEAL, then sweep seal timing + geometry** | MAPSEAL leaning **+6.7pp** at n=1202 | Screen-trustworthy class (self-knowledge/field-universal), and this family already produced v140's ship (SEALFLOOR0 54.74 + 53.13 replication). **MAPSEAL was cancelled at 22% while reading 56.66 ±2.83 — the highest-leaning unfinished shard on the board.** Finish it before spending on the untested upward-floor arm. |
| **5** | **#21 — re-run GUNADD (the additive gunner arm)** | 3-6× structural gap, effect unpriced | `_v163gunadd` is built and was **cancelled at n=388 with no rate printed** — the row's own declared lever has never been read. Every other gunner shard tested a substitution or placement, which `raid.py:639-641` correctly forbids. Cheapest unread arm in the backlog. |

**Runners-up, in order:** **#7** ore-barrier offence (demand side now evidenced
by #49: 0.106× suppression, 85.8% never cleared, 3 Ti vs their 30) · **#40**
pre-seal our own ring (36% camp precondition, 3 Ti/tile) · **#39** opening book
as a targeting prior (screen-trustworthy because the book is (MAP,SEAT), not
(TEAM,MAP)) · **#13** ambush-the-rebuild in its covering-turret form (0.68
events/game) · **#14** arm B only.

**Tools rows that are not planks but pay every verdict:** **#34** (`wincond`
backfill — the currency is unreadable on 63% of unrated files) · **#56**
(`target_value` per-team staleness — it dropped the top target for ~6 hours) ·
**#55** (DEFF into the tools) · **#44** (re-read the CPU margin post-L4 —
`_l4_repair` added per-turn work on top of an 87.6%-of-ceiling reading and
nobody has re-measured).

---

## WHAT I DID NOT DO, STATED SO NOBODY READS MORE INTO THIS THAN IT HOLDS

* **I did not re-verify any GREP.** Every code fact here is quoted from the row
  or from the s40 carry, not re-derived. If a carry is stale, so is my cell.
* **The only new measurements I made are the seat splits** (`awk` over
  `scratchpad/overnight/{GUNSEAT,SEATREL,NULL114,NULL125,SHIPGATENULL,NULLSALT,NULL123}.tsv`,
  cols 6/7) — reproducible in one line, and the pooled 7.58pp is a
  *confirmation* of the row's own 7.57pp, not an independent method.
* **Shard→row attribution is by name and by the worklist comments**
  (`scratchpad/corefill_work.txt`). Three shards I could NOT attribute to a row
  with confidence and therefore did not cite as evidence against one:
  `GUNBLANK`/`GUNBLANKREP`/`BLANKBORDER`.
* **"Coverage" is the screen's coverage, not the field's.** A row killed as a
  screen candidate here may still be a good plank on a fixture that expresses
  its mechanism — which is exactly what the LIVE-PATH list is for.
* **Cancelled-shard rates are point estimates at partial n** and carry their
  own bands; where I lean on one (MAPSEAL 56.66@1202, GUNAXIS0 49.45@2752) I
  print the n and the band beside it.
