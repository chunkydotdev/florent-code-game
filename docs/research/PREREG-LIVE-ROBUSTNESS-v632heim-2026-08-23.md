# PREREG — `LIVE-ROBUSTNESS-v632heim`: does the adopted s57 stack survive contact with LIVE STRANGERS? — a 10-game unrated MECHANISM + SURPRISE probe vs **gsxWins (pinned v87)** and **Jython (pinned v266)**

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition played on a simulated grid under
organiser-approved rules.** "killer turret", "peck", "core takedown", "answer
ladder", "tube", "stranger" are in-engine states and actions of competing game
bots' pieces. Nothing here touches any real system, network or person.

## ⛔ RATIFIED BY BUILDER s57 — see RATIFICATION block below, NOT COMMITTED BY ITS AUTHOR.

**RATIFICATION (BUILDER s57, 2026-08-23):** the judgment lines (M1-M5 bars
+ falsifiers, the barless win column under OB16, the pre-committed
surprise clause, the leak budget, fire gates 1-6) are ratified as
drafted. prereg_check residuals BAR_RESOLVABLE and OB13_INTERSECTION are
ESCAPE-FLAGGED on the record: the tool has no transfer-leg form (this is
a mechanism probe on an adopted config, no treatment diff exists by
design); the transfer-leg form is a wrap-scoped tooling item. CLOCK 1 =
this ratification commit's author time. FIRE GATE 1 remains OPEN pending
Magnus's window sentence (routed to him on the session tail, package
presented).

* **STATUS: drafted BEFORE any challenge is issued, BEFORE any submit, BEFORE any game of this leg exists.** Drafting-shell wall clock **`2026-08-23T20:16:14Z`** (`date -u`, same shell call). Repo HEAD at draft **`08e4b05e2`** (2026-08-23 22:05:52 +0200); `bots/_v632heim` is **clean at that HEAD** (`git status --porcelain` empty).
* Written by a **FRESH opus agent with NO inherited session context** beyond the files named under `PROVENANCE` (the s40 one-fresh-agent-per-prereg rule). This agent read no result tape beyond the named inputs, no `HANDOVER.md`, no `coordination.md`, no s57 session message.
* **THE BUILDER RATIFIES AND LOCKS.** Every judgement line below — design, bar, falsifier, dose, scope of claim — is a **PROPOSAL**, written decisively because a hedged proposal cannot be ratified, not because it is settled.
* **What this agent wrote:** this file, and nothing else. No commit; no edit to `bots/`, `tools/`, `PROGRAMME.md`, `QUEUE.md`, `HANDOVER.md`, `coordination.md`; no `BARS.tsv` row; no challenge; no match; no submit; no activation.
* **⚠ WHAT THIS AGENT DID RUN, disclosed rather than left to boilerplate.** Read-only, in this agent's own shell: `.venv/bin/python tools/target_value.py --band` (the gate; output pasted verbatim below — **it reads our own live rating off `fcode status`, which is the one platform call in this draft's history and it is read-only**); `date -u`; `git log -1`; `git status --porcelain bots/_v632heim`; and local reads/greps of `corpus/league_matches.tsv`, `corpus/ladder_games.tsv`, `corpus/version_trees.tsv`, `bots/_v632heim/*`, `tools/*`, `scratchpad/s57_heim0/*`, `scratchpad/s57_v630/*`. **No mutating platform call of any kind. No `fcode match` call of any kind.**

**PROVENANCE:** exactly the commissioned inputs, plus the surfaces this draft measured for itself —
`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (the obligations doc — OB1–OB17 and the two-clock addenda) ·
`PROGRAMME.md` tail blocks (`VICTORY-BAR CONFIRMATION STANDARD` ll.1169-1179 and `CONFIRMATION STANDARD AMENDED` ll.1181-1192 — *the ROBUSTNESS instrument is opponent variation, and THE LIVE UNRATED FIELD as the instrument of record*; plus `STEALTH_PREDROP_RIDER` ll.169-186, `FIXTURE_OF_RECORD: live_unrated` l.45, `KILL_TARGET` and `THE TRIANGLE` ll.1155-1167) ·
`docs/research/EXPECTATION-v632heim-sentry1-2026-08-23.md` **§V3 VERDICT — ADOPTED** (the adopted config and its new baseline) ·
`docs/research/MJAUT-double-autopsy-2026-08-23.md` (both halves; the field classes A–E, the 28-round free window, 71.7% of killers at d²≤13) ·
`docs/research/DOSSIER-top-finishers-2026-08-23.md` (Jython ferry-siege line; THE GAP: tube life 38; the ladder note that the slot has shipped again) ·
`docs/research/REPLAY-STUDY-jython-v157-wider-2026-08-17.md` + `docs/research/REPLAY-STUDY-jython-inspiration-2026-08-17.md` (the banked ferry-siege study, 60 games) ·
`tools/target_value.py --band` (run at 2026-08-23T20:07:17Z) ·
`CLAUDE.md` (WHAT LOKI IS; the DEFF cluster-enumeration procedure; the rate-limit and submit-is-shipping blocks; the LOKI-14 stdout ruling) ·
and, for the executability checks: `tools/unrated_run.sh`, `tools/submit_clean.py`, `tools/prereg_check.py`, `tools/game_census.py`, `docs/fcode-cli.md` §`match replay`/`match unrated`, `scratchpad/s57_heim0/st1build_dose.py`, `scratchpad/s57_heim0/lossaut_lib.py`, `scratchpad/s57_heim0/e46p1_lib.py`, `scratchpad/s57_v630/e46_lib.py`, `bots/_v632heim/sk_maps.py`, `bots/_v632heim/sk_core.py`.

**LOCK, TWO CLOCKS — PLATFORM LEG** (per the obligations doc's 16:3x addendum; the `# FIXTURE … start=` LOCAL-SHARD form of the 2026-08-17T07:24:55Z addendum **does NOT apply** — this leg produces no shard tape):
* **CLOCK 1** = the ratified file's **lock-commit git author time**.
* **CLOCK 2** = the **first accepted match's platform `createdAt`**, quoted verbatim from `fcode match info <id> --json` → `match.createdAt`. (The field is present on this surface: e.g. the pin candidate `1073e100…` carries `2026-08-23T18:51:10.301Z` in `corpus/league_matches.tsv`, which is the same field the API returns.)
* ⛔ **CLOCK 1 MUST STRICTLY PRECEDE CLOCK 2.** Otherwise this is not a pre-registration and the leg is descriptive only.

---

## ⛔ WHAT THIS LEG CAN AND CANNOT BUY — STATED FIRST, BECAUSE IT SETS THE DESIGN

**THE WHOLE s57 ADOPTION STACK WAS SCREENED ON THREE BOTS WE WROTE.** `scratchpad/s57_heim0/f3_tape.sh:6-11` names them: **F1 = `_v542wave` (our frozen benchmark), F2 = a Mjolnir copy (our own account's other line), F3 = `_v488beltbreak2` (Sleipnir v2, our own retired rush line).** All three are deterministic, all three are ours, and the amended confirmation standard says so in its own words: a 30-cell tape against a deterministic opponent is **a CENSUS, not a sample**; seeds cannot test generalization; **the robustness instrument is opponent variation, with the LIVE UNRATED FIELD as the instrument of record.** `CLAUDE.md` point 3 is the older form of the same rule — *prototypes go at live teams, not at our own probes.*

**⇒ THIS LEG EXISTS TO PUT THE ADOPTED STACK IN FRONT OF TWO BOTS WE DID NOT WRITE, FOR THE FIRST TIME.** It is a **MECHANISM + SURPRISE probe**. It is **NOT** a currency read, **NOT** a ship gate, **NOT** a slot-swap input, and **NO** sentence in its readout may be denominated in game share as a verdict.

**THE ARITHMETIC THAT FORCES THAT, computed at the planned n** (unrated DEFF, `CLAUDE.md`: pooled 1.833 / within-opponent 1.434):

```
per cell   n=5  games, p=0.5, DEFF 1.833  ->  95% half-width = +-59.3pp
pooled     n=10 games, p=0.5, DEFF 1.833  ->  95% half-width = +-42.0pp
(within-opponent convention, DEFF 1.434:  +-52.5pp per cell, +-37.1pp pooled)
```

**A ±42pp interval excludes nothing.** Under OB16 the win column of this leg is a **POINT RULE ONLY** and licenses **no exclusion claim whatsoever** — not "the stack transfers", not "the stack does not transfer".

**WHAT IT CAN BUY, and each is worth the window on its own:**
1. **The V3 band trade, tested against strangers for the first time.** The adopted config narrowed the presence alarm to `SK_SENTRY_DSQ = 13` and *gave up* the d²14–39 band to the damage path, on the strength of a census where killers sit at median d²=5 and 71.7% ≤13. **If live strangers site their killers outside 13, that trade was priced on our own bots.**
2. **A live look at the two constants that bound the answer ladder** — `SK_SENTRY_DSQ = 13` (the band) and `SK_SENTRY_ARM_MAX = 80` (the episode clock, which by its own comment does **not** cover the field's class D parked gun at a 221.5-round lease).
3. **The barrels doctrine's pair share**, which has never been observed off the census.
4. **A defect channel our fixtures structurally cannot show**: a stranger can put our bodies in states our own trees never produce, and an escaping exception permanently destroys that unit for the rest of the match.
5. **A SURPRISE.** `CLAUDE.md` point 4: an unpredicted result from a live-team leg outranks a predicted one from our own arena — *write it down before explaining it away.*

---

## REGISTRATION BLOCK

**TARGET BAND: gsxWins +9 / Jython +44, gaps +9..+44, win pays 16.40..18.01, reachable YES**
*(`tools/target_value.py --band`, run 2026-08-23T20:07:17Z, our rating 1807 live off `fcode status`; verbatim rows: `gsxWins 1816 +9 5-0 pays +16.40 / 0-5 costs -15.60` and `Jython 1851 +44 5-0 pays +18.01 / 0-5 costs -13.99`; both inside the 11-team ADMISSIBLE band `us-80..us+125 AND a 5-0 pays >= 10`. The tool's own caution is carried: **opponent ratings are CACHED** (newest league observation 2026-08-23T19:31, 0.6 h old) and must be re-verified for the selected target before the payoff is quoted again.)*
⚠ **AND THE GATE IS QUOTED FOR THE RIGHT REASON: THIS LEG'S OWN GAMES ARE UNRATED AND PAY ZERO.** The payoff column here prices **the leak** (§ROLLBACK) and prices **relevance** — these are two of the eleven teams the ladder will actually pair us against, and both sit in the band where a win is worth 14–85× what the s28 crash leg's targets were worth. A robustness read against an unreachable team would measure generalization against a population we never meet.

**PINNED: YES — treatment leg, both cells pinned** (`CLAUDE.md`: *pin treatment legs, never pin calibration panels*; `docs/research/SPEC-opponent-pinning-2026-08-13.md`). Pin ids proposed:
* **gsxWins → `1073e100-fd1d-4baf-a7d0-a33eed7d2ba4`** (2026-08-23T18:51:10Z, their **v87**).
* **Jython → `7f9f7202-5e6b-4d2e-b268-1e0706865ae2`** (2026-08-23T18:01:10Z, their **v266**).
⛔ **A decoded `oppver` that differs from the pinned version is an INSTRUMENT ALARM** — the pin did not take, or the decode is wrong. Report it and do not read that cell.

**SURFACE: unrated**
**CELLS: gsxWins (pinned v87) · Jython (pinned v266)** — 1 accepted challenge each = 5 games each.
**CELL VERSION CHURN: gsxWins 1 distinct version / 24 h (v87, all 144 matches) — POOLABLE · Jython 28 distinct versions / 24 h (v266 in 103 of 144; v267 newest) — REPORTABLE, NOT POOLABLE.** (OB14, measured for this draft off `corpus/league_matches.tsv`, trailing 24 h to 2026-08-23T19:31Z.)

| cell | distinct versions / 24 h | matches / 24 h | poolable? |
|---|---:|---:|---|
| **gsxWins** | **1** (v87, all 144) | 144 | **YES — the most stable cell on the board** |
| **Jython** | **28** (v266 in 103 of 144; v267 newest) | 144 | **⛔ NO — REPORTABLE, NOT POOLABLE** |

**The denominator needs no normalisation and that is measured, not assumed: every team in the window played EXACTLY 144 matches** (`OpenSverige` 144, `gsxWins` 144, `Jython` 144, league median 144), so the version counts are directly comparable and the volume confound cannot arise — the same league-scheduler property OB14 recorded at 87.
⛔ **28 VERSIONS IN 24 HOURS IS THE HIGHEST-CHURN CELL THIS PROJECT HAS EVER REGISTERED** — SmartFridge's ten-in-a-day produced five independent defects in one leg (`docs/research/PANEL-selection-version-stability-2026-08-11.md`). **This is exactly why the Jython cell is PINNED and why nothing from it may be pooled with the gsxWins cell.**

**CLUSTER UNIT: match — one match per cell, so MATCH and OPPONENT are collinear within a cell and the POOLED DEFF (1.833) is the applicable constant.** Enumeration performed in writing, per `CLAUDE.md`'s procedure, over all four clusters:
* **MATCH** — binds. 5 games share one opponent, one opponent version, one ~15 s slice.
* **OPPONENT** — binds, and is collinear with MATCH here (1 match per opponent) ⇒ no separate residual to add; use pooled, not within-opponent.
* **MAP** — dies for per-cell reads: a 5-game match uses five different maps (verified 0 of 415 (match, map) pairs with >1 game). Reported descriptively.
* **CONTENT-DUPLICATE** — **cannot be assumed absent against pinned opponents.** REGISTERED CONTROL: md5 every downloaded `.replay26`; report the exact-duplicate count within and across cells. A nonzero count halves effective n and is stated in the readout, not discovered later.

**ESTIMATOR: per-cell descriptive tallies; mechanism columns pooled ONLY where the readout says so and NEVER across the two cells for anything Jython-side (churn).**
**PLANNED n: 10 games (2 accepts × 5).**
**BOUNDARY: 2 accepts = 10 games. The leg ends when the second accept returns, or when the 5-minute `--leg` hold expires, whichever is first.**
**CUT-SHORT: if only ONE cell accepts, the leg publishes that cell's descriptive tallies only, takes NO comparative look between cells, and NO sentence about "the field".**

**DOSE: build-to-first-answer 7 rounds (SENTRY v3 ON, F2 census) vs 28+ rounds unanswered flag-off (the `t_bg_*` baseline: 0 pecks in 17 of 19 killer episodes, the banked 28-round free window) (n = 30 cells/arm/fixture).**
⚠ **AND THE DOSE OF *THIS* LEG IS THE CONFIG ITSELF — THIS LEG HAS NO ARMS.** The line above is the adoption census's dose, quoted so the mechanism is on the page as having fired somewhere; it is **not** re-measured here against a control, because there is no control arm on a transfer read. What this leg asserts instead is CONFIG IDENTITY: the shipped tree must be `bots/_v632heim` at HEAD `08e4b05e2` with, verbatim: `SK_WALK_GUARDS = True` (`sk_maps.py:3556`) · `SK_NAV_STALL = True` (`:3606`) · `SK_KEEPER_CHEW_ON = True` (`:3787`) · `SK_CORE_STAND = True` (`:5088`) · `SK_BATTERY2 = True` (`:6086`, `BURST = False` at `:6198`) · `SK_BARREL_GUARD = True` LEAN (`:7538`, `SK_BG_MEDIC = False` at `:7544`) · `SK_SENTRY = True` (`:7965`) with `SK_SENTRY_ALARM = True` (`:7972`), `SK_SENTRY_FOCUS = False` (`:7982`), **`SK_SENTRY_DSQ = 13` (`:8012`)**, `SK_SENTRY_ARM_MAX = 80` (`:8051`), `SK_SENTRY_FROM = 20` (`:8132`), `SK_SENTRY_IDLE_LIFT = True` (`:8148`).
**TREATMENT TREE: bots/_v632heim (the s57-adopted stack), identity recorded with `tools/treehash.py` BEFORE submit and re-recorded after the restore.**

**BAR: 50.0** — the **only** numeric threshold in this leg: the share of LIVE KILLER TURRETS sited inside the adopted band (d² ≤ 13 to our core footprint).
**BASE RATE: 71.7** — the census value the adopted trade was priced on.
**BAR SOURCE: POINT RULE ONLY — a DIRECTION threshold, not an exclusion bar. It licenses NO exclusion claim and NO effect-size claim** (OB16's second permitted form, and the OB16 corollary's warning that two kinds of bar are indistinguishable from the number alone). At the expected killer population (≈5–15 turrets across 10 games) the 95% half-width at p=0.7 with DEFF≈1.8 is **≈±37pp**, so this bar cannot separate 50 from 71.7 — **it is written down to make the reading pre-committed, not to make it resolvable.**
**BASE RATE SOURCE: `docs/research/MJAUT-double-autopsy-2026-08-23.md`, HALF B — "71.7% of killers at d²<=13", over the field's 877 rated losses.**
**REFERENCE n: none** — the 71.7% is a reference VALUE, not a reference panel that this leg is differenced against.
⛔ **AND ITS OWN DENOMINATOR IS NOT ON THE PAGE:** the killer-population n behind 71.7% lives in the s57 task record, not in the banked summary. **The builder fills it at ratification, or the reference is quoted without an n and the readout says so inline** (the `numbers carry subjects` rule).
**POOL ERA: 2026-08-21T07:52:59Z..now** (the current era, derived for this draft by `tools/prereg_check.py`'s own `pool_eras()` over 9,000 rated rows / 53 maps: boundaries at 2026-08-13T07:12:59Z and 2026-08-21T07:52:59Z). **SPANS-POOL-CHANGE: no — all 10 games are created inside one ~5-minute window and complete in ~15 s each.**

**MECHANISM METRIC READS: `scratchpad/s57_heim0/st1build_dose.py:70` (`cell()`), over `scratchpad/s57_heim0/lossaut_lib.py:79` (`_builds`), `:75` (`_d2_to_fp`), `:105` (`core_shots`), on `scratchpad/s54_klad_lib.py` `Game` (built on `tools/replay_census.py` primitives). TREATMENT DIFF TOUCHES: `bots/_v632heim/sk_maps.py`, `bots/_v632heim/sk_core.py`, `bots/_v632heim/sk_roles.py` (the s57 adoption set). INTERSECTION: yes** — the fence/latency/killer columns read exactly the population governed by `sk_core.py:291` (`if sd <= SK_SENTRY_DSQ`), whose constant is `sk_maps.py:8012`. *(OB13's positive half is what is being satisfied here: the path is NAMED, and it intersects.)*

**METRIC WINDOW: r0-r1000. GATING CONSTANTS: `SK_SENTRY_FROM = 20` (`sk_maps.py:8132`, the dispatch gate, lifted early for an IDLE body by `SK_SENTRY_IDLE_LIFT` at `:8148`), `SK_SENTRY_ARM_MAX = 80` (`:8051`, rounds one (tile, occupant) episode may keep the alarm armed), `SK_SENTRY_DSQ = 13` (`:8012`). MECHANISM CAN OCCUR IN WINDOW: yes** — the banked killer build-to-first-core-shot median is r34 and the free window is 28 rounds, both inside r20–r100; and the answer-latency column is measured from each turret's own birth round, so it is not clipped by a fixed window.
⛔ **AND THE WINDOW DECLARATION CARRIES A LIVE HAZARD RATHER THAN A REASSURANCE: `ARM_MAX = 80` DOES NOT COVER THE FIELD'S CLASS D.** Its own comment (`sk_maps.py:8056-8062`) says 80 rounds is ~3× the 28-round free window and that a parked gun — class D, a **221.5-round lease** — is **NOT** inside it. **gsxWins takes our slot line down at a median of r273.** So the lease-length column below is not decoration; it is the column that says whether the episode clock is the binding constant against this opponent.

**GATE RESOLUTION (OB12): the band gate discriminates its branches at roughly n ≥ 60 killer turrets; this leg expects 5–15. UNRESOLVED ⇒ THE RESTRICTION, IN BOTH DIRECTIONS: no code change to `SK_SENTRY_DSQ` on this leg's evidence, AND no claim that the adopted trade transferred.** An unresolved gate grants no permission — neither the permission to re-open the trade nor the permission to bank a transfer.

**PRE-STATE (OB7): the predicted-change set is NOT already in the target state at lock.** Every mechanism column below is **unmeasured against these two opponents** — the killer-siting d² distribution, the answer latency, the tube lifespans and the pair share have never been read on a game where the opponent was not written by us. There is therefore no column that is pre-satisfied and cannot fail honestly. **And the outcome is declared per OB7's second half: this leg's outcome is the MECHANISM COLUMNS, not the win-condition mix and not the win-condition in our favour** — those are diagnostics with no bar.

**MAP SEGMENT: {large open-lane maps} — killer SITING is a terrain property: a standoff sentinel needs an unobstructed ray, which long open lanes supply and tight maps do not. EXPECTED DIRECTION: POSITIVE on the share of killers sited OUTSIDE the adopted d²≤13 band (i.e. the band covers LESS on large open maps), ~ZERO on tight/small maps.**
**SEGMENT VALUE CEILING: 100.0% pairing share x 0.0pp = 0.00pp — this leg registers NO pooled effect on the segment.** The map draw is the platform's and is unknown at lock; the expected killer population is ≈5–15 events across 10 games. **The segment is DECLARED AND UNPOWERED: it is reported as a raw per-map table and no branch decision is taken on it** (OB15b: exactly one primary segment, and it is this one; everything else is descriptive).

**PLANK CLASS: defensive — the SENTRY answer ladder and CORE_STAND are survival mechanisms at our own core, so the r300 admission bar is in scope by class.**
**KILL-ROUND NON-REGRESSION: ITT timely-checkmate rate — the share of ALL 10 games (not the kill-win-conditioned share, which carries a collider and is a DIAGNOSTIC ONLY) ending in a core takedown by r300, horizon r300, scored as an EXCLUSION — and at this n the exclusion FAILS BY CONSTRUCTION AND IS DECLARED SO IN ADVANCE: the 95% CI upper bound EXCLUDES no rise of any size, so this leg makes NO admissibility ruling in either direction.**
The reason is written as an exclusion precisely so the correction cannot launder it: at n=10 with DEFF 1.833 the 95% interval on any ITT timely-checkmate share is ±42.0pp, and its bound therefore **excludes no regression of any size**. Per the DEFF direction clause, a fail-to-exclude ("no significant rise in kill round") **must first be restated as an exclusion** — restated, this leg excludes nothing, so **it makes NO admissibility ruling and cannot be cited as one.** The r300 bar for the adopted stack was discharged locally at adoption (`EXPECTATION-…-sentry1` §V3: currency grid non-fall, medians −4/−3/−8) and that discharge stands untouched by whatever this leg reads. **Timely-checkmate counts ARE reported here as a DIAGNOSTIC.**

---

## THE FIELD PRIOR — WHAT THE LADDER ALREADY SAYS ABOUT THESE TWO CELLS

Computed for this draft off `corpus/ladder_games.tsv` (the rated-record authority; **never `meta_join` for a denominator**), newest row 2026-08-23T19:31:10Z:

| cell | rated games vs the pinned version | our game share | core-decided | THEIR takedowns of us (median round) | OUR takedowns (median round) | our timely (≤r300) |
|---|---:|---:|---:|---:|---:|---:|
| **gsxWins v87** | 60 | **16.7%** (10/60) | 59/60 | 49 (**r273**) | 10 (r284) | **6/60 = 10.0%** |
| **Jython v266+v267** | 30 | **26.7%** (8/30) | 29/30 | 21 (**r238**) | 8 (r240) | **6/30 = 20.0%** |
| *(gsxWins, all versions, all time)* | 390 | 36.7% | 371/390 | 235 (r216) | 136 (r179.5) | — |
| *(Jython, all versions, all time)* | 110 | 48.2% | 101/110 | 50 (r234.5) | 51 (r212) | — |

⛔ **THE CONFOUND THAT MAKES THIS A PRIOR AND NOT A CONTROL, NAMED HERE SO IT CANNOT BE FORGOTTEN AT READOUT: THOSE ROWS WERE PLAYED BY A DIFFERENT BOT.** The `ourver` values in the v87 cell are v176–v186 — the slot line (x3r0's Mjolnir family) — **not `_v632heim`.** These numbers say what the FIELD does to OUR ACCOUNT's shipped bot; they are **not** a version-matched control arm for this leg and may never be differenced against it as one.

**WHAT THE PRIOR IS FOR — and it is load-bearing for the surprise clause: gsxWins v87 has taken 50 of 60 games off our slot line.** So a 0-5 or 1-4 in the gsxWins cell is **the expected outcome**, carries no information, and is **not** the surprise this leg is watching for. Symmetrically, a 4-1 or 5-0 in that cell would be a very large deviation from a 60-game prior and is **also** a surprise to write down — and still licenses **no** ship claim at n=5.

---

## MEASURES — ENGINE-SIDE, WIRE-READABLE, NEVER OUR OWN STDOUT

⛔ **THE LOKI-14 RULE, AND ITS s54 EXTENSION, BIND EVERY COLUMN BELOW.** Platform-downloaded replays carry `BotOutput` with an **empty `stdout` in 30,664 of 30,664 events**, and under fcode 2.3.6 `print()` does not reach a LOCAL replay either. **Any column read from a bot-side counter is a zero from a channel that does not exist.** Every column here is an engine event: `BUILD` / `removeEntity` / `updateHp` / `fireTurret` / builder attack (`BATK`) / `HEAL`, plus the replay's own `winner` and `cond` fields. `st1build_dose.py`'s own docstring (ll.8-13) states this rule for the same columns and is the reason it is the read path.

**Acquisition, per game:** `fcode match replay <match_id>` (`docs/fcode-cli.md:368`) → `<matchId>_game_<N>.replay26` (read-only per the CLI capability table at `:130`), plus `fcode match info <id> --json` for the per-game `mapName / mapSeed / winnerId / winnerSide / winCondition / turnsPlayed / resignMessage` fields (`tools/game_census.py` docstring — **these are structured JSON on a free endpoint and are never re-derived from the binary**).

### The columns

**A. OUTCOME (diagnostic, no bar).** Per game: won/lost, `turnsPlayed`, `winCondition`, map, seat. Per cell: the 5-game score. **Reported with no bar and no interval-based claim** (see the ±59.3pp per-cell arithmetic).

**B. KILLER-TURRET CENSUS — the primary.** For every enemy gunner/sentinel plant inside d²≤39 of our core footprint (the wide fence, so the band question is answerable): `born`, `died`, tile, **d² to our footprint**, whether it landed ≥1 shot on our core footprint (⇒ KILLER), its **lease** (`died or end − born`), our first peck round on it, and whether it died before its first core shot. Read path: `st1build_dose.py:70` with `ST_DOSE_FENCE=39` (its default), plus the per-turret d² and lease table.
**Derived: (B1) share of KILLERS at d²≤13** [the BAR]; **(B2) killer lease distribution vs `ARM_MAX = 80`**; **(B3) build-to-first-answer median vs the banked 28-round free window and the adopted local value of 7r on F2**; **(B4) destroyed-before-first-core-shot count**; **(B5) pecks-per-engaged-target vs the local 24.3 (post-adoption) and 37.3 (pre-)**; **(B6) per-target completion (pecked turrets that died / pecked turrets) vs the census 13/24.**

**C. FORWARD TUBE CENSUS.** Our gunners/sentinels with d²(build tile, our core centre) > 50 — the `FWD_D2 = 50` definition at `scratchpad/s57_v630/e46_lib.py:33`, assembled at `:114-128`. Per game: **count**, **birth rounds** (local reference r53–r159), **lifespans** (local reference: tube life **5 → 38** under `SK_BARREL_GUARD`), and **PAIR ROUNDS** = rounds in which ≥2 of our forward tubes are alive simultaneously; **pair share** = pair rounds / rounds with ≥1 tube alive.
⚠ **PAIR ROUNDS HAVE NO COMMITTED DECODER.** They are computed from the tube `born`/`died` events the cited lines already carry. **The ~20-line aggregator is written and validated BEFORE the fire** (see FIRE GATE 4) or column C's pair half is **INERT and is dropped from the readout**, per OB13.

**D. OUR CORE'S SIEGE WINDOWS.** Enemy-adjacency and core-damage ledger against our own core: first round an enemy body is orthogonally adjacent to our footprint; the negative `updateHp` deltas on our core by round; heal events on our core (the CORE_STAND answer); and the **answer latency** = first enemy fence-turret plant → first of our pecks on it. Read path as (B), plus `lossaut_lib.py`'s core-damage ledger.

**E. THEIR KILL SHAPE vs THE BANKED CLASSES (descriptive, and the most likely home of a surprise).** For each of their core takedowns, classify against MJAUT half B: **A** lone-sentinel walk-in (0 harvesters, 1 builder, fall ~r51.5) · **B** standoff sentinel (d²25, ~r227) · **C** forward gun line (slow) · **D** parked gun (**221.5-round lease**) · **E** unexplained. For Jython specifically, test the banked ferry-siege signature element by element: first launcher r1 (60/60 in the study), self-throw r2, raider orthogonally adjacent by r8, ring barriers on OUR 12-ring (peak occupancy; the study's binary seal finding: partial ≥10/12 INVERTS heal denial), forward sentinel built ~r75 at median d²=9, and **95.2% of their core damage from a sentinel, 0% from a gunner**.

**F. GUARDS — ours, and they are the reason a losing leg can still be a good leg.**
* **F1. OUR OWN UNIT REMOVALS WITH NO ATTRIBUTABLE DAMAGE** (`tools/crash_census.py`, our side). Any nonzero count is **a live-only defect in our tree** — a stranger put a body in a state our own fixtures never produce and an exception escaped `run()`, which permanently destroys that unit. **Standing count for us in 1,855 games: 0.** Nonzero here ⇒ FIX BEFORE ANY SHIP, and it outranks every other finding in this document.
* **F2. CPU.** `tools/tle_census.py` over the downloaded replays. **Exec-time fields exist on PLATFORM replays and NOT on local ones** (the s42 rider: 8,847 µs read on platform vs a blind 0 across 1,649 local builder-turns) — so this leg can see a dimension the entire local screen is blind to. Report `tled / exec_max / over10k`.
* **F3. TURRET SELF-KILL** (`tools/turret_selfkill_census.py`), ours: `can_fire` returns TRUE at 0 ammo and `fire()` then raises, destroying our own turret. Expected 0.

---

## BARS AND FALSIFIERS — HONEST AT n=5 PER CELL

**⭐ THE FRAME: ONE NUMERIC BAR, FIVE MECHANISM-SHAPED FALSIFIABLE CLAIMS, AND A WIN COLUMN WITH NO BAR AT ALL.**

**M1 — PRIMARY. THE ADOPTED BAND COVERS THE KILLERS THAT LIVE OPPONENTS ACTUALLY USE.**
*Claim:* ≥50.0% of live KILLER turrets (column B) are sited at **d² ≤ 13** of our core footprint. *Census reference:* 71.7% (median d²=5).
*Falsifier:* **if ≥50% of live killers sit in the d²14–39 band, the V3 narrowing is measured to be blind against this field** and the named trade — *"helheim_seatA's 14-32-band-only population is given up to the damage path"* — was priced on a census of our own bots. That is a ROAD RE-OPENED, routed as a queue row, **not** an in-leg code change.
*Both-tail (the instrument must be able to say the other thing):* the same table returns "all killers ≤13" (trade vindicated) or "killers mostly 14–39" (trade blind); it has already produced both verdicts on the local census (71.7 / 28.3). The instrument's own controls are driven at fire time (`ST_DOSE_FENCE=0` must collapse the population; `=9999` must exceed it; `ST_DOSE_SIDE=them` must move the peck columns).
*Resolution:* UNRESOLVED at this n ⇒ **the restriction, both ways** (see GATE RESOLUTION).

**M2 — THE EPISODE CLOCK vs THE LIVE LEASE.** *Claim (pre-committed, directional):* live killer leases are **shorter than `ARM_MAX = 80` rounds**. *Falsifier:* median killer lease > 80 ⇒ **the alarm expires while the gun keeps its lease**, and the binding constant against this field is the episode clock, not the band. **gsxWins killing our slot line at a median of r273 is why this claim can fail**, and the flag's own comment already concedes class D is outside it. A failure here is a finding, not a defect.

**M3 — THE DOSE SURVIVES CONTACT.** *Claim:* build-to-first-answer on fence turrets has a **median ≤ 28 rounds** (inside the banked free window; the adopted local value is 7r on F2). *Falsifier:* median ≥ 28 ⇒ **the answer ladder does not arm against strangers** and the adopted dose is a fixture property. *Companion, reported either way:* destroyed-before-first-core-shot (local reference: 3→6 on F2). **0 across all 10 games while ≥5 fence turrets exist = the ladder never completes live.**

**M4 — TUBE LIFE UNDER STRANGER COUNTERFIRE.** *Claim:* our forward tubes survive materially longer than the pre-BARREL_GUARD form. *Reference:* tube life **5 → 38** locally; the banked GAP read says our tube life is "fixed (38)" while the top finishers' volume is absent. *Falsifier:* **median tube life ≤ 10 rounds live ⇒ the 38 is a census artifact**, and BARREL_GUARD's grade (kills 20→24, wins 37→40) was bought against bots that do not shoot back the way the field does.

**M5 — DOES THE BARRELS DOCTRINE'S PAIR APPEAR AT ALL?** *Claim:* pair rounds > 0 in **at least 1 of 10** games. *Falsifier:* **0/10 ⇒ the pair share does not exist off the census** — a clean mechanism null worth banking, and a cheap one. *(This is deliberately the weakest possible existence bar: at n=10 nothing stronger is honest.)*

**⛔ THE WIN COLUMN: REPORTED, NO BAR, NO EXCLUSION, NO VERDICT.** Per-cell scores and the pooled 10-game share are printed with their ±59.3pp / ±42.0pp half-widths **attached to the number in the same sentence**, and no clause anywhere in the readout may promote them.

### ⭐ THE PRE-COMMITTED SURPRISE CLAUSE (written BEFORE the fire, so it cannot be negotiated after)

1. **A 0-5 sweep against us in EITHER cell while the mechanism columns read STRONG — band coverage high, answer latency short, killers destroyed before their first core shot — IS A SURPRISE TO BANK, NOT TO EXPLAIN AWAY.** It means the columns our census says are strong are not the columns that decide a live game, and that sentence goes in the readout **before** any attempt to account for it. It is written down as an observation, with the games named, and routed as a research row.
2. **A 4-1 or 5-0 in the gsxWins cell is EQUALLY a surprise** (60-game prior: 16.7%) and licenses **no** ship claim, **no** slot-swap input and **no** rating inference. It is written down and re-fired before it is believed.
3. **Any mechanism column that reads at a value the local census cannot produce** — a killer at d²>39, a tube lifespan above the local maximum, a lease beyond r300, an inbound tactic named in none of classes A–E — **is written down verbatim in the readout before it is interpreted.** `CLAUDE.md` point 4: an unpredicted result from a live-team leg outranks a predicted one from our own arena.
4. **F1 nonzero (our own units removed with no attributable damage) outranks every other line in the readout** and converts this leg from a robustness read into a defect report.

### WHAT THIS LEG MAY NOT CONCLUDE, ENUMERATED

* It may not promote, demote, ship, or block the adopted s57 stack.
* It may not move `SK_SENTRY_DSQ`, `SK_SENTRY_ARM_MAX` or any other constant. Findings route as queue rows.
* It may not make a `DEFENCE_ADMISSION_BAR` ruling in either direction.
* It may not compare its game share against the rated prior table as if that were a control (different bot).
* It may not pool the Jython cell with anything (28 versions / 24 h).
* It may not describe 10 games as "the field".

---

## ⚠ `prereg_check.py` STANDING — TWO RESIDUAL FAILS, BOTH DISCLOSED AND NEITHER GAMED

Run by this drafter against this file (read-only; **gate on the last line, never on `$?`**): every presence obligation reads `ok` and the arithmetic closes except two, which are **properties of an honest transfer read colliding with a tool built for arm-vs-arm screens.** They are written here rather than negotiated away, and **the builder rules on them at ratification — not the drafter.**

1. **`BAR_RESOLVABLE FAIL — margin |50.0 − 71.7| = 21.7pp vs half-width ±36.2pp (one-sample, DEFF 1.434, n=10).`**
   **This is TRUE and it is already the document's own position:** `BAR SOURCE` declares the bar a **POINT RULE ONLY**, `GATE RESOLUTION` declares the gate unresolvable at this n, and the default on unresolved is **the restriction in both directions**. The tool has no representation of OB16's point-rule escape, so it reports the unresolvability as a failure. ⛔ **THE ONE THING THAT MUST NOT HAPPEN IS MOVING THE BAR UNTIL THE TOOL IS HAPPY** — OB16's own closing clause: *an unresolvable bar is a reason to state what IS resolved, not a licence to spend games until it resolves*, and sizing off a value chosen to clear a checker is bar-chasing. **Routed as a tooling gap: `prereg_check.py` should recognise a declared POINT RULE and report `not resolvable — declared` instead of `FAIL`.**
2. **`OB13_INTERSECTION FAIL — st1build_dose.py is NOT in the 3-path diff.`**
   **The computed clause cannot pass for this leg by construction: there IS no treatment diff.** The treatment is a tree already committed at HEAD `08e4b05e2`; the working-tree diff the tool intersects against contains unrelated `scratchpad/s48_*` files. **The SUBSTANCE of OB13 is satisfied and is on the page:** the read path is named to `file:line`, and it reads the population governed by `sk_core.py:291` / `sk_maps.py:8012` — the constant the adopted config sets. LOKI-18's failure mode (a metric that reads identically whatever the plank does) is excluded here because the metric's population is *defined by* that constant. **Routed as a tooling gap: the intersection clause needs a transfer-leg form (`TREATMENT DIFF REFS` against the adoption commits, with the metric's GOVERNING CONSTANT rather than its file path as the intersecting object).**

Also carried from the run, as WARNs rather than fails: the declared `TREATMENT DIFF TOUCHES` paths are absent from the *working-tree* diff (same cause as (2)); the `METRIC WINDOW` partial-window notes for `SK_SENTRY_FROM=20` / `ARM_MAX=80` / `DSQ=13` (correct and already reasoned about — the mechanism cannot occur before r20 and the episode clock expires at 80, which is exactly what bars **M2** and **M3** are for); and the segment-ceiling note that any confirmation must be **on-segment, never pooled** — this leg confirms nothing on the segment and says so.

---

## FIRE GATES — ALL SEVEN BEFORE THE FIRST CHALLENGE

**GATE 1 — AUTHORIZATION, and this one is NOT the drafter's to close.** `PROGRAMME.md`'s `STEALTH_PREDROP_RIDER` (ll.169-186) authorizes **full pre-drop unrated testing of screen-clear Skalman versions**, with the remaining gates named as the builder's: *(1) a version clears the local screen (declaration of record required), (2) the activation-window pricing under the 10-min cadence.* ⚠ **AND A SECOND, OLDER BLOCK IN THE SAME FILE (ll.378-380) SAYS THE LIVE UNRATED LEG IS PARKED until an arm clears 60±2 locally or Magnus explicitly opens a window.** The two blocks are from different rulings and this drafter cannot adjudicate them. **The builder either (a) records the screen-clear declaration of record that the rider requires, or (b) routes the question to Magnus. This leg does not fire on an unadjudicated authorization.**

**GATE 2 — THE TREE IS THE ADOPTED STACK, ASSERTED IN THE EXPERIMENT'S OWN VARIABLE (OB11).** The causal variable is *"the bytes on the platform are the adopted config"*, not *"the flags look right in a grep"*. Therefore: `python -m py_compile bots/_v632heim/*.py`; `tools/treehash.py bots/_v632heim` recorded in the readout; the fourteen constants of the DOSE block asserted by value; and `tools/submit_clean.py`'s printed manifest (it stages `*.py` only, allowlist at `:117`) read before the upload is confirmed.

**GATE 3 — OB17, THE EXECUTING TOOLS, RUN CLAUSE-3 FIRST BECAUSE IT IS THE ONE THAT CAN SURPRISE.**
* **Clause 3 — silent non-execution.** ⛔ **FOUND, AND IT IS THE REASON THIS GATE EXISTS: the registered read path is NOT executable on platform files as it stands.** `scratchpad/s57_heim0/e46p1_lib.py:44-49` (`cells_at`) globs `*.replay26` and **derives OUR SEAT FROM THE FILENAME** (`us = 0 if stem.endswith("seatA") else 1`). Platform downloads are named `<matchId>_game_<N>.replay26` — **no seat suffix — so every file would silently be read as seat B.** The failure is quiet: the "ours" columns become THEIRS, and the leg reports a mirror-image dose that looks like data. **REGISTERED REMEDY (must exist and be validated before fire):** an adapter that renames each downloaded game to `<match>_g<N>_seat{A,B}.replay26`, with the seat resolved from `fcode match info --json` (`winnerId` + `winnerSide` determine our side for every game, won or lost), **plus a positive control that the replay's own `winner` index agrees with the API's winner in 10 of 10 games.** If the mapping is wrong the control fails loudly instead of the columns failing quietly. **Second silent path, same clause:** `scratchpad/s57_v630/e46_lib.py:60/:80` (`log_winner`, `log_seat_names`) read `path.with_suffix(".log")`, which **platform downloads do not have** — so every `*_controls.py` / `*_readout.py` module importing them is **LOCAL-ONLY** and is not used here. The platform readout uses `LA`/`Cell` plus the API fields, and nothing else.
* **Clause 1 — name the executing tools.** `tools/submit_clean.py` (`--leg`, parsed at `:552`; `--leg` and `--activate` are mutually exclusive, `:554`) · `tools/unrated_run.sh` · `fcode match replay` · `tools/game_census.py` · `st1build_dose.py` + the adapter.
* **Clause 2 — confirm the runner emits what is registered.** `tools/unrated_run.sh:397` emits `fcode match unrated "$id" --match "$PIN" --json` when `PIN` is set (`:382-397` document the pin); `:408` is the unpinned path. **`PIN` takes ONE opponent id per invocation** (`:10-12`), so this leg is **two invocations, one per cell, each with its own `PIN`**. Naming: `LEG_NAME_RE` at `submit_clean.py:338` is built from `LEG_ERAS = ("Loki", "Skalman")` (`:333`), so **`--name 'Skalman rc632.1'` matches and `--activate` is absent** (a leg, never a ship). *(This clause's answer was NOT known in advance — the last leg on the tape is `Loki rc10.1` and the docstring's prose still says legs stay `Loki rcX.Y`; the `Skalman` era was added at `:334` on 2026-08-22 and v180 shipped as `Skalman rc619.1`. The regex is checked, not the prose.)*

**GATE 4 — THE PAIR-ROUNDS AGGREGATOR EXISTS AND HAS BEEN DRIVEN TO BOTH VERDICTS** (a hand-built fixture with 0 pair rounds and one with a known positive count), or column C's pair half is dropped as INERT.

**GATE 5 — THE WINDOW IS TIMED OFF AN OBSERVED PAIRING, RE-DERIVED AT FIRE TIME.** Measured for this draft off `corpus/league_matches.tsv`: **our last 40 consecutive ladder pairings are 600.0 s ± 0.25 s apart, and 60 of the last 60 land at minute ≡ 1 (mod 10), second `:10`** — i.e. slots at `HH:x1:10`, ~9.5 minutes of clear air. ⛔ **DO NOT HARDCODE THAT.** `CLAUDE.md` records that the offset has shifted at least once inside 18 hours; **re-derive it from recent rows (`fcode match list --mine --type ladder`) immediately before firing.** Fire **just after** an observed pairing.

**GATE 6 — THE RESTORE TARGET IS READ LIVE, NEVER HARDCODED.** ⛔ **THIS DRAFT WAS COMMISSIONED WITH "holder = x3r0 v185" AND THAT INTEGER IS ALREADY STALE: `corpus/league_matches.tsv` shows `OpenSverige v186` playing rated ladder from 2026-08-23T18:31:10Z onward (v185's last row is 18:21:10Z).** This is the s56 defect repeating — *window plans may not carry hardcoded restore integers.* **The restore target is whatever `fcode status`'s `Active bot:` line reads in the minute before the submit, recorded verbatim in the readout, and confirmed on the same line after the restore** (never on `$?` — `fcode status` exits 0 while printing `Error: True`). `submit_clean.py` restores the holder itself and verifies on that line.

**GATE 7 — RATE LIMIT.** 2 accepts are needed and the limit is **5 test/unrated matches per 10 minutes** (re-corrected s54; this constant has flip-flopped 10→20→10). The leg fits in one window with 3 to spare. ⛔ **If a rejection occurs, re-derive the constant from the CLI's verbatim rejection string, never from this line.** Rejected attempts appear to count.

---

## ROLLBACK AND LEAK ACCOUNTING

**SUBMISSION IS SHIPPING.** `fcode submit` auto-activates what it uploads; there is no "upload now, activate later". The only admissible path is:

```
1. read + record the holder             fcode status  ->  `Active bot:`   (verbatim, live)
2. record tree identity                 tools/treehash.py bots/_v632heim
3. observe a ladder pairing              (re-derived cadence; fire just AFTER it)
4. submit as a LEG, holding the slot     .venv/bin/python tools/submit_clean.py \
                                            bots/_v632heim --name 'Skalman rc632.1' --leg
5. fire cell 1 (pinned)                 PIN=1073e100-… tools/unrated_run.sh <V_P> 5 \
                                            ebd8d82a-7365-4ccb-af0b-defea3a1ac4d      # gsxWins
6. fire cell 2 (pinned)                 PIN=7f9f7202-… tools/unrated_run.sh <V_P> 5 \
                                            8cf9b751-00d3-484a-b0ed-e3073ae1d46f      # Jython
7. release the hold                     touch scratchpad/LEG_FIRES_DONE
8. confirm the restore                  `Active bot:` == the string recorded at step 1
```

`V_P` = the prototype's platform version, **unknown at lock time and recorded at fire time** (from the `Active bot:` line after the submit, never from the submit echo).
**The hold is bounded by the tool, not by the operator:** `submit_clean.py:102` sets `LEG_TIMEOUT_S = 300.0` and `:100` `LEG_SENTINEL = scratchpad/LEG_FIRES_DONE` — **the restore fires even if the leg operator dies mid-window, so a hung leg cannot span a rated pairing.** 300 s of exposure inside ~570 s of clear air is the whole safety argument, and it is structural rather than hopeful.

**LEAK BUDGET — DECLARED IN ADVANCE.**
* **Expected: 0 leaked rated matches.**
* **Tolerated: ≤ 1**, budgeted at **≈ −8 Elo** (`CLAUDE.md`'s measured −24.67 across 3 leaked matches).
* **≥ 2 leaked ⇒ the window procedure failed**; that is reported as a process defect in the readout, above the leg's own findings, and the next leg does not fire until the cause is named.
* **Every leaked match is charged to the SHARED rating** — the slot is a co-held account (x3r0's line is the incumbent), so the cost lands on a teammate's holder, which is the reason the budget is 0 rather than "small".

**THE AUDIT, AND IT IS PER-MATCH AT THE PAIRING BOUNDARY — NOT THE MATCH COUNTER.**
`fcode match list --mine --type ladder` → the **last ladder pairing created BEFORE the submit** and the **first created AFTER the restore**, with `teamAVersion`/`teamBVersion` on each. ⛔ **The match COUNTER cannot answer this question** (it proves nothing COMPLETED, and says nothing about what was PAIRED while the prototype held the slot), and **`elo_history.tsv` cannot either** (it tags rows by the version active at POLL time). `corpus/ladder_games.tsv`'s per-game `ourver` is the durable ground truth once ingest catches up — **and it is not the fire-time instrument, because its newest row can sit tens of minutes behind the wall clock; an absence there is not evidence.**

**INBOUND EXPOSURE, DISCLOSED AND ACCEPTED.** Opponents' challenges do NOT count against our budget and **opponents CAN challenge our live prototype mid-window** (measured: Jacobs ×2, 2026-08-22). **Every activation window is also a free look at our line for the field** — the panel-preview law cutting the other way. Record any inbound unrated matches created during the window in the readout; they are exposure, not data.

---

## DISCLOSURES CARRIED INTO THE READOUT — UNDER ONE HEADING (the OB12 companion)

The arms of this leg are **not balanced by any explicit rule** — the platform assigns maps and seats. Per the companion clause, the imbalance is reported **once, under one heading**, across every fixture axis: **seat mix per cell · map mix per cell · opponent version (pinned, asserted per game) · exact-duplicate replay count · per-map killer counts (the declared segment).** Disclosing rather than correcting is deliberate: a matched estimator chosen after the data is the fault this discipline exists to catch.

Also carried: **this is a 10-game probe against 2 opponents; the correct plural for that is "these two bots", never "the field".**

---

## READOUT TEMPLATE (fill at leg end; nothing else is published)

```
LEG            LIVE-ROBUSTNESS-v632heim   tree <treehash>   V_P <version>
LOCK           clock1 <git author time>   clock2 <first accept createdAt>   ORDER OK/FAIL
AUTH           gate-1 disposition: <declaration-of-record ref | Magnus ruling ref>
CELLS          gsxWins  pin 1073e100 oppver=<87?>  score <x-y>   [+-59.3pp]
               Jython   pin 7f9f7202 oppver=<266?> score <x-y>   [+-59.3pp]  NOT POOLABLE
DUPES          exact-duplicate replays: <n>/10   (effective n adjusted: yes/no)
M1 BAND        killers d2<=13: <k>/<n> = <pct>%   bar 50.0   census 71.7   POINT RULE
M2 LEASE       killer lease median <r>   ARM_MAX 80   covered <k>/<n>
M3 DOSE        build-to-first-answer median <r>   free window 28   local F2 7
               destroyed-before-first-core-shot <k>/<n>   pecks/engaged <x>  completion <k>/<n>
M4 TUBES       count/game <x>  life median <r>  (local 38, pre-guard 5)  births <r..r>
M5 PAIR        pair rounds >0 in <k>/10 games   pair share <pct>%
E  SHAPE       their takedowns by class A/B/C/D/E: <...>   Jython ferry elements: <...>
GUARDS         F1 our unattributed removals <n>  F2 tled <n> exec_max <us> over10k <n>
               F3 turret self-kills <n>
LEAK           pairing before <ts>  after <ts>  leaked rated matches <n>  inbound challenges <n>
               holder before <verbatim>  after <verbatim>  MATCH/ MISMATCH
SEGMENT        per-map killer d2 table (descriptive, unpowered)
SURPRISES      <verbatim, written before any explanation>
CONCLUSIONS    <only from the enumerated-permitted set; no ship/no constant change>
```

---

## AUTHORITY

Draft: a fresh opus agent, this file only. **Ratification, lock, firing and every verdict: the builder.** Data cited above is from the repo's own corpora and tools at the timestamps named; the one live figure (our rating 1807) is the `target_value.py --band` run at 2026-08-23T20:07:17Z and is re-verified before the payoff line is quoted again.
