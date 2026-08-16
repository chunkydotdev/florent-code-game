# SWEEP TAGGING — QUEUE.md build-cost classification, 2026-08-16

**Purpose.** Magnus's MARK-500 sweep will batch-build queue arms. The binding
cost is BUILDS, not games. This document tags every LIVE row (per
`.venv/bin/python tools/queue_check.py`, which is the authority for what
"unblocked" means — STATUS: token or dead-section only, prose ignored) into a
build-cost tier, with file:line evidence for each call.

**Live-row source.** `tools/queue_check.py` (run 2026-08-16) returned exactly
60 unblocked row numbers:
`2,3,5,7,8,10,13,14,16,17,19,20,21,22,23,24,28,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,55,56,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77`.
This document classifies all 60. I did NOT hand-derive "unblocked" from prose
markers (blocked/withdrawn/refuted/demoted in text) — `queue_check.py`'s own
docstring documents that prose-word matching previously UNDERCOUNTED by
hiding 3 startable rows (#5, #3, #10), which is why it moved to a structural
`STATUS:` token. Using the tool's own output is the control for that failure
mode.

**Incumbent used for verification.** `bots/_v223sealrepair` (v140), current
per PROGRAMME.md. Where a row's own GREP stamp was run against an older
incumbent (`_v197mapcode` or earlier — true for most of #40-53), I re-grepped
the cited symbol against `_v223sealrepair` directly myself before tagging; this
is flagged inline as VERIFIED where I did, and I did **not** re-run to primary
in every low-priority case (time-boxed) — flagged as UNVERIFIED-LINE where I
relied on the row's own (possibly stale) citation.

**Control run (discriminant check).** Before trusting any ONE-FLAG grep, I ran
one that MUST return nothing: `grep -rn "SEGMENT_ASSIGN\|route_crew\|belt_crew"
bots/_v223sealrepair/` (a symbol implied by #66, which the row itself says does
not exist because the comms store is full). Returned zero hits, as expected —
the search discriminates rather than finding everything.

---

## Tier definitions (recap)

- **BUILT** — a tree on disk already implements the mechanism; zero cost.
- **ONE-FLAG** — a single existing boolean/constant, named to file:line, flips
  or moves; near-zero cost.
- **SMALL** — a localized change (~<20 lines) in a named function; real but
  cheap.
- **LARGE** — new mechanism, multi-file, or new state/coordination machinery.
- **NOT-AN-ARM** — not a bot-tree change (tool, instrument, corpus/analysis
  task, or a measurement/self-audit row with no proposed code change).
- **UNSURE** — both candidate tiers given, with the fact that would settle it.

---

## BUILT (2)

| # | Title (short) | Evidence |
|---|---|---|
| 5 | CRASH INDUCTION AT SCALE | `bots/_v131loki14/raid.py:618-645` — two-arm tag `"B"=border/"I"=interior`, behind `LOKI14_KIDNAP_ON`. The border-throw crash mechanism is already built and unshipped from the current incumbent lineage. This row is a live-fire question ("does it move rating"), not a build. |
| 17 | DOES THE CRASH WEAPON ACTUALLY FIRE? | Same tree, `bots/_v131loki14`. Row's own text: *"Nothing to write — this is a RUN, not a build."* A LOCAL both-ways dose check on the tree that already exists. |

---

## ONE-FLAG (7 — 2 of them share a single knob)

| # | Title (short) | File:line | Symbol | Note |
|---|---|---|---|---|
| 72 | THE COMMITTED OPENING (rush) | `bots/_v223sealrepair/doctrine.py:1409` | `LOKI2_RUSH_ON = False` | **VERIFIED directly**: `grep -n LOKI2_RUSH_ON bots/_v223sealrepair/*.py` confirms the flag and 2 live call sites (`main.py:336`, `raid.py:656`), all wired and dormant. Flip to `True`. ⚠ Row itself records adverse evidence from a prior 360-game screen (core_kill_share −15.6pp to −35.4pp sign p<0.05) — cheap to build, not cheap to be right about; re-read that evidence before firing. |
| 33 | DOES `LOKI_GUNAXIS_PENALTY` DO ANYTHING? | `bots/_v223sealrepair/doctrine.py:1533` | `LOKI_GUNAXIS_PENALTY = 8` | **VERIFIED directly**, consumed at `raid.py:816`. Ablation arm: set to `0`. |
| 50 | PAVE THE WALK-OUT | `bots/_v223sealrepair/eco.py:936` | `ct.read_store(SLOT_HARVESTERS) >= 1` | **VERIFIED directly**: this exact guard is the sole reason `PAVE_TRAIL_ON` paving is disabled for harvester #1. Lower the threshold (e.g. `>= 0`) or drop the clause. |
| 24 | THE LAUNCHER SINGULARITY | `bots/_v223sealrepair/doctrine.py:965` | `LAUNCHER_RESERVE = 80` | Same knob as #28 (see below) — **one build serves both rows.** |
| 28 | `LAUNCHER_RESERVE = 80` STARVES THE LAUNCHER | `bots/_v223sealrepair/doctrine.py:965` | `LAUNCHER_RESERVE = 80` | Row's own text: *"the only one of the three gates with a dose."* Same constant as #24 — do not build twice. |
| 23 | FORWARD PLACEMENT (cap raise) | `doctrine.py:1219` (shifts to `:1237` in some re-checks) | `LOKI_FWD_GUN_CAP = 3` | Row's own framing: *"a CAP RAISE on an existing mechanism, not a new behaviour."* Raise the integer. |
| 53 | SEAL TIMING/GEOMETRY SWEEP (floor sub-arm only) | `doctrine.py:1227-1228` | `LOKI_SEAL_TI_FLOOR = 12` | Only the FLOOR axis is one-flag. The row's other two asks — a round-gated timing constant and a seat-order geometry variant — **do not exist in the tree yet** ("no timing constant... no geometry variant... has ever run") and are SMALL new code, not a flip. Tag the floor-sweep sub-arm ONE-FLAG; tag the rest SMALL if pursued separately. |

---

## SMALL (18)

| # | Title (short) | Evidence (file:line, function) |
|---|---|---|
| 2 | KILL THE SENTINEL FROM OFF ITS AXIS | `raid.py:616` shared attack `pr=3` for GUNNER/SENTINEL; `raid.py:768-774` gun-axis built from `GUNNER` only (`doctrine.py:1533` penalty). Add an off-axis-attack preference when adjacent to a SENTINEL — one function, no new state. |
| 7 | ORE-BARRIER CARVE-OUT | `raid.py` build_barrier call sites (277, 500, 558), none ore-gated; `ORE_TITANIUM` occurs 0× in `raid.py`, 6× in `eco.py`, never in the same file as `build_barrier`. New function: barrier an ore tile a forward gun covers. |
| 10 | BLIND THEIR GUN WITH THEIR OWN BODY | Same exile-throw picker as #45/#51 (`raid.py:900-932`). Modify destination scoring to pick a tile inside an enemy gunner's firing lane (reuses `get_attackable_tiles_from`, already used at `raid.py:816`-area for LOKI-25). |
| 13 | AMBUSH THE REBUILD | No destroyed-tile memory exists. Reuses the existing per-unit dict PATTERN already in the tree (`self.raid_ban`, `main.py:87`; written `raid.py:179,223`; read `raid.py:784`) — same shape, new dict keyed on destroyed tiles. |
| 14 | IDLE BUILDER GETS A DESTINATION | `_idle_rotate` (`main.py:797`, guarded `if turret_type != GUNNER: return`) is GUNNER-only; 0 hits for `SLOT_IDLE`/idle-destination anywhere. A deterministic per-unit destination function (no comms slot needed — store is full, see #66) is buildable standalone. |
| 16 | THE NON-STRIKE SURCHARGE | Row names the exact change: add one condition to `_eco_spendable` (`eco.py:225`) — `while rnd<250 and read_store(SLOT_RAID_LIVE) fresh: require ti >= cost + NON_STRIKE_SURCHARGE`. One new constant, zero new slots, zero new call sites (existing chokepoint). |
| 30 | STATION SCORER MODELS SENTINEL AS TARGET NEVER THREAT | `raid.py:749-777` threat scan branches on LAUNCHER and GUNNER only; add a SENTINEL branch mirroring the GUNNER `gun_axis` logic (`r²=32`, ignores obstacles). One `elif` in one function. |
| 38 | KIDNAP/CRASH AT 900 SCALE | Current exile picker `raid.py:900-932` lacks a border-tile selector and map-area gate. The border-tile selector already exists, written, in `bots/_v131loki14/raid.py:618-645` — this is a PORT job, not a from-scratch build, plus one new map-area gate. |
| 41 | FORWARD-SENTINEL SITING d²14-32 + BARRIER ADJACENT | Siting range: `_try_forward_sentinel` currently `d²≤50` with no minimum (cite drifted — row's own `:668` is 2 incumbents stale; **UNVERIFIED-LINE**, re-locate before build, likely near `raid.py:636-691` per #76's fresher citation). Range-bound is a numeric-comparison change; barrier-the-adjacent-tiles reuses existing `build_barrier` call sites. |
| 45 | KILL THE BUILDER, NOT THE LADDER | `raid.py:616` attack priority targets TURRET only; add "enemy builder adjacent to their own turret" as a priority tier in the same list. Localized to the priority list + `LOKI_GUNAXIS_PENALTY` interaction. |
| 48 | PARKED-RAIDER TERMINAL IDLE | Combines three EXISTING signals already in the tree — `LOKI_QUIET_ON` (`doctrine.py:1488`), `LOKI_SALT_CUT_MAX=40` (`doctrine.py:1585`), `SLOT_RAID_LIVE` heartbeat (`doctrine.py:1188`) — into one new terminal-idle check before the heartbeat write. No new state. |
| 51 | AIM THE THROW LOOP | Same picker as #10 (`raid.py:909-931`). Add victim scoring (feeder-adjacent-to-turret) and destination scoring (land on a friendly sentinel's ray + ammo co-requisite). One function. |
| 59 | DON'T GET FARMED | `_bfs_direction` (`eco.py:809-832`) blocks only the enemy LAUNCHER's own tile, not its d²≤2 pickup envelope. Extend the blocked-tile set by 8 tiles around a visible enemy launcher. One function. |
| 71 | FUND THE COLLAR BEFORE THE KILL WINDOW | `SURGE_MIN_RND=300` (`doctrine.py:402-405`) is an absolute round gate. `SLOT_UNDER` (a siege/contact signal) already exists and is already consumed elsewhere (`eco.py:225`, per #16) — reuse it to make the surge gate conditional instead of purely round-keyed. |
| 73 | BELT-CUT REPAIR | **VERIFIED directly.** Two named gates: (a) `eco.py:687` `_l4_repair`'s `is_tile_empty` check excludes any building, including an enemy barrier — needs a destroy-then-repair step, not just a flip; (b) `raid.py:468` `if et in (EntityType.CONVEYOR, EntityType.SPLITTER):` inside `_salt_turn` — the melee carve-out tuple that would need `EntityType.BARRIER` added (near one-flag on its own, but paired with (a) which is real logic). |
| 74 | SEALED-PECK CARVE-OUT | `LOKI_QUIET_ON` gate consumed at `raid.py:256,334`. New OR-condition: allow melee when the builder's own 4 neighbours are all blocked (a mobility check), independent of target HP. One new condition at an existing gate site. |
| 75 | ORPHAN-BELT FACING FIX | Exact site: `eco.py:545 _build_next_link`, pop at `:556-558`. `ct.get_direction(bid)` is already called twice elsewhere in the same file (`:619`, `:719`) — reuse it to check facing before abandoning a link. Row's own words: *"COMPLEMENT DRIVEN... the tree knows how to ask and does not ask here."* |
| 76 | FORWARD-SENTINEL PLANT PATH HAS NO ATTRITION MEMORY | Reuses the exact `self.raid_ban` dict pattern (`main.py:87`) for a new per-tile plant-memory dict, consumed at the forward-sentinel siting loop (`raid.py:672-691` per fresher citation). ⚠ **`bots/_v330sentban` already exists on disk and is described in-row as "being built now"** — I grepped it for `plant_count`/`sentban` and got **zero hits**, so it is a stub/in-progress, not a finished duplicate. Check with the builder before starting a second implementation of the same row. |

---

## LARGE (14)

| # | Title (short) | Why LARGE |
|---|---|---|
| 21 | THE GUNNER COUNT | Diagnostic only — names the constraint (collar LOS) but no code lever; needs new gunner-siting geometry logic compatible with the collar. |
| 22 | WE STOP BUILDING TURRETS AFTER r150 | Row's own text: *"the fall-off is emergent... needs measuring before it is changed."* No code lever named yet. |
| 39 | THE OPENING BOOK OF THE NEW POOL | Needs a new corpus data pipeline (per-team-map modal tiles) AND new bot logic reading opponent identity at match start — two new systems. |
| 42 | VOLUME-NOT-SEQUENCE | Row's own text: *"Which one binds is not determinable by grep — that IS the row."* Requires a multi-arm ablation to find the mechanism before any single arm can be built. |
| 43 | BARRIER-IN-BASE CRASH CONFIRMATION | New targeting logic to induce pathing exceptions via barrier placement — exploratory, no existing scaffold. |
| 47 | CONDITIONAL SIEGE LAUNCHER | Needs a new approach-detection signal and a re-triggerable build latch (current latch is one-way). A partial prototype exists (`bots/_v200siegelaunch`, unverified depth) which lowers but does not zero the cost. |
| 49 | ORE-BARRIER DENIAL, DEFENSE SIDE | Framed as an open question ("does it bind?"); whichever answer, the fix (turret fire or launcher eviction targeting an enemy barrier) is new targeting logic not yet present anywhere. |
| 58 | THE FORWARD EVICTION LAUNCHER | Explicit design choice today is "one launcher, near home" (`main.py:615-617` comment). A second, forward-sited launcher with new eviction-target logic is a new deployment mode. |
| 60 | DESTROY MECHANISM (scale reduction) | `ct.destroy(`/`ct.can_destroy(` appear **zero times** in the entire tree. Deciding what/when to self-destroy for scale reduction is new decision logic with real downside risk (destroying something useful) — needs conditions from scratch. |
| 63 | LONG-APPROACH ARRIVAL LOCK | ⚠ **CAUTION:** this shares its navigation diagnosis with #54, which `queue_check.py`/QUEUE.md marks **STATUS: BLOCKED — road-closed** ("any successor must change NAVIGATION or DESTINATION, never DETECTION" — two prior detect-and-repick builds, OSCLOCK/OSCLOCK2, both died). #63 itself is not STATUS-blocked so it counts as live, but if its fix is another detect-and-repick variant it re-treads a road already closed twice. Read #54's closure before scoping a build. |
| 66 | MULTI-BUILDER BELT COLLABORATION | Row's own text: comms store is **16/16 full** (`doctrine.py:931-961`, `:1184-1188` — **I independently re-verified this: 16 distinct `SLOT_*` constants, 0-15, all bound**). Any crew/segment coordination needs a slot eviction or bit-pack, i.e. new infrastructure, before any coordination logic can be written. |
| 67 | WIRE `_hunt_turret` | Function does not exist (0 hits for `def _hunt`/`_hunt_turret(` anywhere); only 3 comment mentions. Six pre-tuned constants exist but the ~90-line spec'd function itself is unwritten — genuinely new code, likely >20 lines. |
| 69 | THE CONJUNCTION | Two-part: (a) `SIPHON_WIRE_RNDS=12` budget (`eco.py:530`) could be raised as a constant (this half alone would be SMALL/ONE-FLAG), but (b) needs an entirely new d²≤8 enemy-barrier census + spawn-tile contest logic that does not exist. The row bundles both; tagging the whole row LARGE on part (b). |
| 77 | COMPOSE THE CONFIRMED | Depends on THREE components of mixed provenance: bodyaware is a **finished tree** (`bots/_v242bodyaware/eco.py:816` etc.), sentban (#76's mechanism) is **in-progress** (`bots/_v330sentban`, currently a stub per my grep), and the seat-fix component has **0 hits anywhere**. Composing three mechanisms — one done, one mid-build, one unwritten — into a single tree is not a single-row build today. |

---

## NOT-AN-ARM (9 — 3 known + 6 found)

Known members named in the task: **#61, #65, #68.**

Additional members found this sweep:

| # | Title (short) | Why NOT-AN-ARM |
|---|---|---|
| 19 | BATTERY MUST NOT PIN `NOISE_ON=False` ON BOTH SIDES | Fixes the testing methodology (`gate.py`'s instructions to bot-tree copies), not the shipped bot's behaviour. A battery/protocol fix. |
| 34 | BACKFILL `wincond` ONTO A FULL-COVERAGE SURFACE | Row's own text: *"not a bot-tree claim; incumbent unaffected."* Corpus/tooling backfill (`corpus/throws.tsv` coverage gap). |
| 35 | PER-GAME MAP NAME FOR UNRATED GAMES | Row's own text: *"not a bot-tree claim; incumbent unaffected."* Corpus/tooling — a `map` column producer for unrated games. |
| 44 | SELF-AUDIT: v125 RUNS AT 87.6% OF TLE CEILING | Proposes measuring CPU margin BEFORE any future row adds per-round work; no code change of its own. A precondition/self-audit gate for other rows, not a plank. |
| 55 | EVERY BAR WE QUOTE IN GAMES IS TOO NARROW | Row's own text: *"N/A TO THE BOT TREE; this is a TOOLS row."* Fixes `tools/panel_read.py`'s interval math (design-effect correction). |
| 56 | `target_value` PRICES OFF A CACHED RATING | Row's own text: *"TOOLS row."* Fixes `tools/target_value.py`'s freshness/fallback reporting. |
| 61 | TWO OF THREE LANES HAVE NO DECISION SURFACE | Row's own text: *"vs the instruments, not the bot tree."* Fixes `tools/audit_trigger.py`'s denominators. |
| 65 | PAIRED PANEL — GIVE EVERY SCREEN'S LOSING ARM A FIELD READ | Row's own text: *"NOT A BOT CHANGE... a MEASUREMENT PROTOCOL."* Fixes `results.tsv`'s recording schema. |
| 68 | OPPONENT-VERSION QUALITY FROM THE FIELD | Row's own text: *"NOT A BOT CHANGE... an ANALYSIS instrument."* Fixes `tools/target_value.py` to join fields it already has. |

---

## UNSURE (10 — both tiers given, plus the settling fact)

| # | Title (short) | Candidate tiers | What would settle it |
|---|---|---|---|
| 3 | CLEAR MORE ENEMY TURRETS | SMALL / not-yet-buildable | Row admits the behaviour already exists close to what's proposed (SENTINEL-before-GUNNER order confirmed) and names no concrete lever ("may fall under the KNOB BUDGET" — no symbol given). Need: identify the exact priority/threshold constant that would raise clearing rate. |
| 8 | SEAT-RELATIVE SCAN ORDER | SMALL / LARGE | A concrete site exists (`main.py:289`, non-rotation-equivariant hash) but causation is unestablished — the site's own directional prediction came out backwards (P=0.296), and two other candidate non-equivariant sites (`eco.py:868`, `eco.py:97`) are unreconciled. Settling fact: re-run the identity-shard null with ONLY `main.py:289` fixed — if the +6.28pp gap collapses, it's SMALL; if not, the true carrier is elsewhere and it's LARGE. |
| 20 | THE HARVESTER TARGET | Diagnosis-incomplete / LARGE | Cap is confirmed non-binding (7.78 vs cap 18); candidate cause (builder-death freezing harvester count) is named but not confirmed as THE mechanism, and no code lever follows from it yet. Settling fact: confirm the builder-respawn-freeze mechanism against a replay cut before naming a fix site. |
| 36 | 900-AREA ECO-AS-KILL-ENABLER | SMALL / LARGE | Narrow reading ("raise `ECO_CAP`/`SURGE_ECO_CAP` conditionally on map area") is SMALL — two named constants (`doctrine.py:30,405`). Broad reading ("redirect the surplus specifically into kill capacity: builders, forward turrets, ammo") needs new spend-priority logic across multiple systems — LARGE. Settling fact: which reading the builder is meant to implement. |
| 37 | TAP THE BELT (offensive siphon) | SMALL / LARGE | Mirrors an existing DEFENSIVE arm pattern (`SIPHON_WIRE_ON` `doctrine.py:899`, `SIPHON_DENY_ON` `:915`, wiring via `_wire_tick`) which lowers cost, but needs new enemy-harvester detection and a route-home path from an enemy-adjacent origin, which is a different topology than the existing wiring. Settling fact: whether `_wire_tick` can be reused unmodified for an enemy-origin conveyor, or needs new pathfinding. |
| 40 | PRE-SEAL OUR OWN SIEGE RING (defensive) | SMALL / LARGE | An analogous pattern exists for the ENEMY core (seat-seal, `raid.py:267-277`, `seatkeys`) that could plausibly be parameterized for our own ring — that reuse would make it SMALL. If the home-ring geometry doesn't map cleanly onto `seatkeys`, it's a new mechanism — LARGE. Also carries `DEFENCE_ADMISSION_BAR: kill_round_non_regression` per the row, which is a measurement gate on firing it, not on building it. Settling fact: whether `seatkeys`/the seal function can be re-targeted at the home ring without new geometry code. |
| 52 | COLLAR MEDIC | SMALL / LARGE | The exchange exists (`_heal_adjacent`, `eco.py:322-340`) but is purely opportunistic — no dispatch/positioning exists anywhere. If builder role-assignment ("go stand near X") is already a reusable primitive elsewhere in the tree, this is SMALL; if it must be built from scratch, LARGE. Settling fact: grep for an existing "move toward a damaged-building target" helper reusable outside the raid layer. |
| 62 | TINY-MAP ECONOMY FLOOR | LARGE (leaning) | Diagnosis is solid (median builders-before-harvester = 5.0 flat across ALL area classes) but I searched `main.py` at the cited gate lines (202, 548, 639) and found **no explicit "N builders before first harvester" constant** — the count is emergent from spawn/build priority ordering, not a named threshold. Settling fact: locate the actual priority-ordering code that produces "5" before assuming a single lever exists. |
| 64 | SPAWNPOCKET | SMALL / LARGE | Two named sites (core spawn-tile sort in `main.py`; pave branch of `_move`, `eco.py:934-954`) are each plausibly small, but "sealed region" detection may need a local BFS rather than a 4-neighbor check — and this repo has an active CPU-margin concern on the hot path (see #44, and the HOT-TURN RIDER in `QUEUE.md`'s header). Settling fact: whether a 4-neighbor passability check suffices, or true reachability (BFS) is required. |
| 70 | ZERO IDLE-AND-FREE | SMALL / LARGE | Composes with #10's and #30's existing gun-axis/attackable-tiles computation (`raid.py:768-774`, `:816`), which would make a bodyblock-fallback SMALL by reuse. If idle (non-raiding) builders need genuinely new geometry to find a blockable enemy firing line, it's LARGE. Settling fact: whether the existing gun-axis computation is reachable/cheap from the idle-builder code path (which is currently GUNNER-only, `main.py:797`). |

---

## Summary counts

- BUILT: 2
- ONE-FLAG: 7 (5 distinct knobs — #24/#28 share one)
- SMALL: 18
- LARGE: 14
- NOT-AN-ARM: 9
- UNSURE: 10

Total: 60.
