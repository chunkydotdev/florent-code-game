# v69 "orekeeper" delta read (x3r0 upload, live 22:21)

**Status: COMPLETE — code half only. Q5 (production sanity) NOT ANSWERABLE:
zero v69 matches in `replay_archive/` at time of writing; no download taken.**

Updates `docs/research/v68-chokewall-first-read-2026-08-07.md`. That read
stands unamended except where flagged RE-VERIFY below.

**Version tags (rule 2).** Predecessor = **v68 "chokewall"**,
`bots/opp_v68/main.py`, md5 `04811b4a3f065f861e74ab626db559df`, 3684 lines.
Subject = **v69 "orekeeper"**, `bots/opp_v69/main.py`, md5
`562b01e900d9c17a267d85c6e6f6e914`, 3797 lines. `diff -u` = **8 hunks, +119
/ −6 lines** (net +113). `bots/opp_v69/` contains `main.py` only — no
auxiliary module. All line refs are `opp_v69/main.py` unless tagged v68.

---

## VERDICT BLOCK

### Q1 — DELIVERY-FREEZE DEFECT: **UNTOUCHED**

No hunk touches conveyor repair, chain re-attachment, or delivery
continuity. The three functions that own the chain are byte-identical to
v68 (all sit outside the 8 hunks): `_link_path` (:3186), `_build_next_link`
(:3305), the chain medic (:2754+).

Evidence, in order of force:

1. **`_link_path` is invoked from exactly two call sites, in both versions,
   and both are "a harvester was just built"** — v69:2545 and v69:2752
   (v68:2471 / v68:2678), each additionally guarded by `if not
   self.link_queue`. **There is no re-plan trigger on conveyor loss, no
   periodic connectivity check, and nothing anywhere reads whether the chain
   still reaches a Core input tile.** Once a completed chain is cut, nothing
   in the file ever notices.
2. **`_build_next_link` treats occupancy as completion** (:3315-3317):
   `if ct.get_tile_building_id(tile) is not None: self.link_queue.pop(0);
   continue`. A blocked mid-chain tile is popped, not cleared and not
   re-routed — a permanent hole. v69's own E2 comment (:3542-3544) diagnoses
   this exact behavior in writing ("the link machinery pops occupied tiles
   instead of clearing them, so a conveyor on ore blocks the site for the
   rest of the game") **and then fixes only the upstream cause, leaving the
   machinery as-is.**
3. The only repair-shaped mechanism in the file is the pave trail's
   stateless relay, described in the chain-medic comment (:2757-2759):
   melee-cleared conveyors are "stateless-relaid by the next passer-by". It
   is positional (whatever tile a builder walked off), not
   connectivity-driven — it cannot re-attach a severed chain to the core.
   **E2b narrows this relay** (see risk note below).

**Narrow adjacent mitigation, worth naming so the morning conversation does
not over-claim it:** the E2 pair attacks a *different* contributor to the
same observable ("delivered Ti flat, harvesters 0, still laying conveyor").
The v68 replay signature had two halves — chain unwired AND harvesters gone.
E2 addresses harvester-site self-destruction (paving your own ore; squatting
your own ore). It does not address chain re-attachment at all.

**New code-level explanation of the other half of that signature (not in the
v68 read, unchanged v68→v69, cite as CARRIES):** `SLOT_HARVESTERS` is a
**monotonic high-water mark** — `_sync_harvesters` (:991-992) writes only
`if live > ct.read_store(SLOT_HARVESTERS)`, never decrements. After a
harvester wipe the whole bot still believes `harv` = peak. That keeps the
ammo-conversion gate `(under or weapons or harv >= 2)` (:882) open, keeps
`allow_pave = has_launch or harv >= 2` (:2735) true, and keeps both pave
gates' `read_store(SLOT_HARVESTERS) >= 1` (:3551, :3579) true. **"0
harvesters alive while it kept laying conveyor" is exactly what a monotonic
harvester counter produces.** E1 mitigates a symptom of this (bank milked to
12 by ammo top-up) without fixing the stale counter. Untouched in v69.

### Q2 — TIEBREAK TERRITORY: delivered-Ti FLOOR rises, ceiling and post-r300 UNCHANGED

**Post-r300 behavior: identical to v68. Zero new round gates.** Grep for
`MAX_TURNS`, `>= 9xx`, `1000 -`, `999`, `960`, `900` over v69 hits comment
prose only. `SURGE_MIN_RND = 300` (:286) remains the last behavior switch in
the file. `MELEE_FUTILE_BAN_RNDS = 300` is a *duration*, not a threshold.
**Headline 2 of the v68 read — the uncontested endgame — carries in full.**

Per-piece effect on delivered Ti (tiebreak #1):

- **E1 (ammo floor 12 → 46): no direct effect.** Ammo conversion spends the
  *global pool*; delivered Ti counts physical stacks arriving at the core.
  Indirect and triply conditional: it only bites when (a) turrets alive
  (`weapons = read_store(SLOT_HOME_GUN)`, :844), (b) `under` false — i.e. no
  own-core HP drop and no `SLOT_ATK_RND` within **50** rounds (:820-833),
  (c) bank actually near the floor. In that regime the bank now holds 46
  instead of 12, crossing the ~23 Ti scaled harvester rebuild price. Side
  effect: conversion needs bank ≥ **50** to fire at all in peacetime (the
  `amt >= 4` guard on `min(16, target−ammo, ti−46)`, :883-884) versus ≥ 16
  before — **v69 is marginally slower to fill its magazine in quiet
  mid-game.** Under siege nothing changes (floor stays 12, 24 Ti/round). No
  cap moved: AMMO_FLOOR 16, mag caps 72/48, hive 256, atoll 32 all identical.
- **E2a (scarce-ore step-off widening): potentially the largest delivered-Ti
  swing, but map-gated.** Condition added at :2896 —
  `or (self.map_ores and len(self.map_ores) <= 8)`, OR'd with the existing
  `len(self.map_walls) >= ORE_STEPOFF_MIN_WALLS` (80). Fires only on
  **decoded pool maps** (`map_ores` is populated in the map-decode branch
  :1098; `[]` otherwise, :670) whose total ore count is ≤ 8 (his named cases:
  fjordgate 6, moonrise 8). Unsticks the documented "builder loops onto its
  own ore tile, 587 moves, zero build actions, zero harvester builds in the
  last 970 turns" pathology. On an undecoded map it is inert.
- **E2b (ore pave ban): raises the harvester-count ceiling, map-agnostic.**
  Two sites (:3547-3551 trail branch, :3575-3579 next-tile branch): read
  `get_tile_env`, skip the pave if `ORE_TITANIUM`; on exception assume ore
  (fail closed → skip). Prevents the trail burying 3 of 4 harvester sites at
  t=24/30/57 as measured on fjordgate.
- **E4 (melee futility ledger): Ti preservation, not delivery.** Saves 2 Ti
  per skipped swing against a healed bait target. Note the freed builder
  falls through to the *next melee priority*, i.e. it stays a saboteur — it
  does **not** return to economy. No delivery effect.

**For Branch-B instrument design, be specific:** the assumption "v68 delivers
ZERO for 650+ rounds in ~45% of grinds" should be **softened for v69 on two
map classes** — decoded maps with ≤ 8 ore tiles (E2a), and any map where the
pave trail crosses ore (E2b). Expect v69 to recover to a nonzero trickle
where v68 flatlined. It does **not** get a late-game plan, does **not** gain
chain repair, and its delivered-Ti *ceiling* (harvester cap `_eco_cap`,
LATE LABOR SURGE at r≥300 & ti≥1500) is untouched. Design the instrument to
beat a *recovering* opponent, not a dead one: measure our own delivered-Ti
margin to r1000 rather than banking on their zero.

### Graft-brief implication (for the morning human conversation)

v69 is a small, disciplined, **economy-only bug-fix patch**: +119/−6 across
8 hunks, four independent call sites, one new dict of state, two new
constants, zero new round gates, and **zero changes to combat, siege,
chokewall, snipe placement, ammo caps, spawn policy or the endgame.** Every
piece is driven by his own ghost forensics (sporks_g2/g5, pivot_g1) and each
one is a self-contained graft in either direction — none of them conflicts
with, duplicates, or is blocked by anything in our 6e line. Symmetrically,
nothing in v69 closes the gap the v68 read opened: pieces I, J and H are
still absent, and the uncontested post-r300 window is still uncontested. So
the merge conversation is about *direction of travel*, not about reconciling
two designs. **The one asymmetry to say out loud:** the shared ancestral
pave-crash (v69:3536, same unguarded `ct.is_tile_empty(pp)` as v68:3445) is
a **unit kill in our line** (22 crash-units / 120 games, established) but
only a **self-clearing one-round action loss in his** — his `run()`
(:747-758) swallows every exception, and the trail freshness gate (:3534,
`pave_rnd != rnd − 1`) plus the fact that `pave_prev` is written only after
a successful move (:3589-3591) means the stale tile can be read at most once
before it is nulled. "We both have that bug" is a true sentence with a false
implication: our piece-N fix is worth ~nothing to him and everything to us.

---

## E-series characterization (Q4)

| Piece | Where | Mechanism | Constants | Trigger conditions |
|---|---|---|---|---|
| **E1** peacetime ammo floor = harvester reserve | `_core`, :868-881 (1 live line) | `ti_floor = 12 if (under or weapons) else 52` → `12 if under else (46 if weapons else 52)`. Raises the bank the core refuses to convert away. | new literal **46** | `weapons = read_store(SLOT_HOME_GUN)` > 0 AND `under` false (`under` = own-core HP dropped this round, or `SLOT_ATK_RND` within 50 rounds, :820-833). Siege path (floor 12) and no-turret path (floor 52) unchanged. Conversion now needs bank ≥ 50 to fire. |
| **E2a** scarce-ore step-off widening | `_builder` move phase, :2879-2899 | Adds an OR-clause to the ore step-off gate so a builder standing on ore steps to a non-ore passable cardinal neighbour (clears `tgt`/`stuck`, returns). | new literal **8** (ore-count threshold); existing `ORE_STEPOFF_MIN_WALLS = 80` (:122) untouched | Decoded map only (`self.map_ores` non-empty, populated :1098). Fires when total map ore ≤ 8 **or** wall count ≥ 80, and the unit is standing on `ORE_TITANIUM`. |
| **E2b** ore pave ban | `_nav` pave path, :3547-3551 and :3575-3579 | `get_tile_env(target) == ORE_TITANIUM` → skip the pave; `except Exception` → assume ore, skip. Applies to both the trail tile (`pp`) and the next-step tile (`nxt`). | none | Every pave attempt, all maps, all rounds. Fail-closed. |
| **E4** melee futility ledger | `_sabotage_prio`, :722 (state), :1707-1714 (prune), :1722-1731 (skip), :1744-1745 + :1748-1769 (update); constants :102-114 | Per-building-id ledger `[consecutive no-progress hits, last HP, banned-until round]`. After firing, re-read HP: `hp >= last_hp` → hits+=1, else hits=0. At 8 → ban `rnd + 300`, reset counter. Banned ids are skipped in the candidate loop so the melee chooser falls through to the next priority. Pruned each call against `set(ct.get_nearby_buildings())`. | **`MELEE_FUTILE_HITS = 8`**, **`MELEE_FUTILE_BAN_RNDS = 300`** | `_sabotage_prio` only — the melee target chooser. Does **not** cover hunt pecks (`hunt_defer` already does), escort (`ESCORT_STALL_RNDS` 25 / `ESCORT_BAN_RNDS` 400), counterbattery, or the generic adjacent-fire fallback. |

**The relay's four-piece list is confirmed exactly. Nothing undisclosed in
the sense of a hidden feature — every one of the 8 hunks is accounted for.**
What a graft review still needs to see, in descending importance:

1. **There is no E3.** Grep `(E[0-9]` over v69 returns 10 sites, all E1 / E2
   / E4. No E3, no E5+, and `bots/opp_v69/` has no second module. Either E3
   was cut before upload or it never existed. **Worth one question to x3r0 in
   the morning** — if E3 is a delivery/chain fix he held back, that changes
   the Q1 verdict.
2. **E2 is two independent changes under one tag with different gating** —
   E2a needs a decoded map, E2b works everywhere. The relay's summary reads
   as one item; they graft separately.
3. **E2 is incomplete on the link path.** The ore ban is applied only to the
   *pave/trail* builder. `_build_next_link` (:3305-3340) has **no ore
   check**. On decoded maps `_link_path` blocks ore in its BFS (:3202) so
   links avoid ore anyway — but the **unknown-map fallback BFS (:3253-3303)
   does not block ore**, so on any undecoded map the link builder can still
   bury a harvester site. The fix does not cover the case the fix's own
   rationale describes, off-pool.
4. **Second-order risk pointing the wrong way on Q1.** The pave trail *is*
   his stateless conveyor-relay (:2757-2759). Any legacy chain tile sitting
   on ore — reachable via the undecoded-map link fallback in 3 — will now
   **never be relaid** after being destroyed. That is a new permanent chain
   hole in exactly the delivery-freeze failure mode. Low frequency, but it
   is a regression vector and should be named if anyone proposes grafting
   E2b into a line without also fixing `_build_next_link`.
5. **Three new `except Exception` swallows** (:1758-1759, :3549-3550,
   :3577-3578), all fail-closed. Consistent with house style here, but they
   are new silent paths.
6. **One structural (non-additive) edit**, the only tuple-shape change in the
   diff: `best, best_p = None, 99` → `best, best_p, best_bid = None, 99,
   None` (:1714) with the matching assignment at :1745.
7. **New hot-path engine call:** `_sabotage_prio` now calls
   `ct.get_nearby_buildings()` on every invocation (:1711) for the prune. One
   sweep per melee decision; trivial against a 10 ms budget, but it did not
   exist before.
8. **E4's ledger is per-unit-instance**, by his own comment (:719-721). Each
   builder re-learns the bait independently, and the ban expires. **Exploit
   residue for us: a healed bait barrier still buys 8 swings × 2 Ti = 16 Ti
   per builder per 300-round ban — up to ~3 re-engagements per builder over
   1000 rounds.** Down from the measured 865 swings, not to zero. A
   *rotating* bait (a fresh barrier id every ~300 rounds, or two baits
   alternated) defeats the ledger entirely, since the ban is keyed on
   building id and pruned the moment the id leaves vision.

---

## Carryover audit (Q3)

| v68 read finding | v69 status |
|---|---|
| Chokewall gate off on 12/14 maps; **+0 rounds detour** on every current-pool seat | **CARRIES.** Planner (v68:1074-1213 decode BFS, :2643-2657 idle trigger, :3007-3092 plant) lies outside all 8 hunks. `CHOKE_MAX_RND = 140` (:140), `CHOKE_MAX_TILES = 3` (:146) unchanged. |
| **No post-r300 switch — r300 is the last behavior change in the file** | **CARRIES.** No new round gate anywhere in the diff; `SURGE_MIN_RND = 300` (:286) still last. The late-game lever remains uncontested. |
| Small-map collapse on ≤ 256 tiles (10x10 2-4, 21x8 0-2) | **CARRIES (mechanism).** `_plan_siege` and the forward-turret placement are untouched — the sentinel-goes-defensive loss mode is unfixed. **RE-VERIFY magnitude only:** small maps skew scarce-ore, so E2a is disproportionately likely to fire there; expect marginally better small-map economy without touching the loss mode. |
| Median win r97; 11/13 wins are core kills before r140 | **CARRIES.** Opening, rush and snipe paths untouched. E1 cannot bite in the opening (bank starts at 500; the 46 floor only matters below ~50 Ti). |
| Snipe exposure: PRIMARY_SENTINEL, first forward turret = sentinel, dsq 18-32, window r4-30 | **CARRIES.** v68:433 and v68:1760 both fall outside every hunk (hunk 5 ends at v68:1698). |
| Ammo ceiling low + static (72 under / 48 quiet, ≤24 Ti/round) | **CARRIES, marginally deeper.** Caps identical; v69 additionally needs bank ≥ 50 (was ≥ 16) to convert in peacetime-with-turrets. Weakness #2 is slightly *more* exploitable, not less. |
| Map-recognition dependency is total (`_plan_siege` returns if `map_grid is None`) | **CARRIES and DEEPENS.** E2a adds another decoded-map-only feature keyed on `self.map_ores`. A pool rotation now also disables the scarce-ore fix. |
| Razor-thin gates (`ORE_STEPOFF_MIN_WALLS = 80` with maps at 70/74/80) | **CARRIES and REPEATS.** New `len(map_ores) <= 8` with his own moonrise sitting at exactly 8. |
| Interceptor diversion: role-1 off economy r30-140 | **CARRIES.** Untouched. |
| Never dumps ammo; stored-Ti (tiebreak #3) never zeroed; finishes rich | **CARRIES; slightly stronger.** E1 makes it hold *more* stored Ti in peacetime. Dump-stored-Ti plays remain wasted against this line. |
| Tiebreak resolves at step 1, delivered Ti, in 11/11 r1000 games | **RE-VERIFY at the margin** — see Q2. The chain still resolves at step 1; only v69's expected delivered floor moves. |
| OUR-SIDE: our nav routes around barriers, never pecks (`_bfs_direction`, _v79e6c:3581-3634) | **CARRIES** (our code, unchanged). |
| **Ancestral pave-crash class** (established): unguarded `ct.is_tile_empty(pp)` | **CARRIES** — v69:3536, identical to v68:3445, verified in the diff as unchanged context. **Sharp detail for the graft brief:** the E2b `try/except` was inserted at :3547, eleven lines *below* the unguarded call, on the same variable `pp`. He hardened the sibling getter and walked straight past the crash. Severity differs by line: unit-kill in ours, one-round action loss in his (see verdict block). |
| **Piece-F own-throw handshake reset** (established, ancestral, insufficient) | **CARRIES** — v69:1336-1346, ancestral from v68:1302-1310, still keyed on `read_store(SLOT_LAUNCHED_ID) == ct.get_id() + 1` so it covers own-launcher throws only. Enemy-launcher throws still miss the handshake. |
| Piece I (rotation discipline) / J (counterbattery) / H (endgame switch) ABSENT | **CARRIES — all three still absent.** No hunk goes near `_turret`'s idle tail, `_try_counterbattery`, `hive_freeze`, or any late-round logic. |

---

## Evidence appendix

**Diff shape.** `diff -u bots/opp_v68/main.py bots/opp_v69/main.py` — 8
hunks at v68 offsets 99, 700, 844, 1669, 1690, 2803, 3443, 3463. +119 / −6.
The 6 removed lines are: 1 constant-expression line (E1 `ti_floor`), 1 tuple
init and 1 tuple assignment (E4 `best_bid`), 1 gate line (E2a), 2 gate lines
(E2b). Everything else is additive — **78 of the 119 added lines are comment
prose** (plus 1 blank). **Live code delta is 40 lines added / 6 replaced.**
Per hunk (added / of which comment): constants 13/11, `__init__` 8/6,
`_core` ammo 14/13, `_sabotage_prio` head 19/12, `_sabotage_prio` tail 23/8,
ore step-off 18/14, pave trail 15/10, pave next-tile 9/4.

**Chain-repair search (Q1, negative result).** `link_queue`,
`_step_off_link`, `_link_path`, `_build_next_link`, plus greps for
`wired|reattach|re-attach|orphan|disconnect` over v69: no connectivity
check, no repair trigger, no core-input test outside `_link_path`'s
goal-set construction at plan time. `_link_path` call sites: v69:2545,
v69:2752 (v68:2471, v68:2678) — both post-`build_harvester`, both behind
`if not self.link_queue`.

**Round-threshold search (Q2/Q3, negative result).**
`grep -nE 'MAX_TURNS|get_current_round\(\) *[<>]=? *[0-9]{3}|rnd *[<>]=? *[3-9][0-9]{2}|1000 *-|999|960|900'`
over v69 returns 11 hits, all inside comment blocks (:40, :241, :246, :255,
:258, :296, :1007, :2038, :2754, :2818, :2997). No code-level late gate.

**E-tag inventory.** `grep -n '(E[0-9]'` → v69: **9 hits** — E1 ×1 (:868),
E2 ×3 (:2882 widening, :3537 + :3571 pave ban), E4 ×5 (:102, :716, :1707,
:1722, :1748). v68: **0 hits** (the E-tagging scheme is new in v69). No E3,
no E5+.

**Q5 — production sanity: SKIPPED, not answerable.** No files matching
`4d5fcf04*` anywhere in the repo (`find . -name '4d5fcf04*'` → empty).
`replay_archive/` holds 1298 files / 216 matches, of which 69 are
OpenSverige — **all at teamVersion ≤ 68; zero v69 matches archived.** The
most recent archived OpenSverige match is `c821193d` (v68, 3-2 vs Kings
College Munich, completed 2026-08-07T20:19:36Z); the archiver last wrote at
22:40 without picking up a v69 game. Per brief, no download taken. When a
v69 match does land, the chain-wiredness metric (docs/tooling.md, "Chain-
wiredness is the delivery-continuity metric") is the right instrument — and
the specific predictions to test are in the "what to look for" list below.

**What a v69 replay should show, if this read is right** (pre-registered so
the production check is falsifiable):

1. Chain-wiredness still collapses in long games — the 5/11-class freeze
   should recur at a similar rate, because nothing repairs a cut chain.
2. **Zero conveyors ever placed on an `ORE_TITANIUM` tile by the pave path**
   (E2b, map-agnostic). One such placement falsifies E2b's coverage — check
   whether it came from `_build_next_link` on an undecoded map (predicted
   gap 3 above) rather than the trail.
3. On a ≤ 8-ore decoded map, no builder should sit on an ore tile for more
   than ~1 consecutive round (E2a). A long park there falsifies E2a's gate
   or means the map was not decoded.
4. Melee swings against any single enemy building id should now cap near 8
   per builder per 300 rounds (E4), versus v68's measured 865-swing tail.
5. Peacetime ammo conversion should stop firing whenever the bank sits
   between 12 and 50 Ti with turrets alive (E1) — a visible flat stretch in
   converted-ammo against a low bank.

## Open questions

- **What is E3?** No trace in the shipped file. Direct question for x3r0;
  if it is a chain fix, Q1 flips.
- Does `_build_next_link` ever actually place a conveyor on ore in
  production on an undecoded map (the gap E2b does not cover)? Needs a
  replay from off-pool terrain.
- Does the E1 floor change measurably slow his forward sentinel's shot rate
  in the quiet mid-game window (bank 12-50, turrets alive)? That is a
  directly exploitable 38-Ti-wide band and the only place v69 is *weaker*
  than v68.
- Carried from the v68 read and still open: the delivery-freeze root cause
  is now understood on the *harvester-count* side (monotonic
  `SLOT_HARVESTERS`, :991) but the *chain-severance* side is still
  uninstrumented — which conveyor dies first, and does the surviving
  network keep a core input at all?
- Does the `>= 8` ore threshold cover the current pool, or is moonrise
  (exactly 8) the only additional map it unlocks? Needs the ore counts per
  pool map — cheap offline check against the map decode table.
