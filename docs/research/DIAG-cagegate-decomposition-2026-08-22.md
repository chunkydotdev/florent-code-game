# DIAG — the cage-walker core-peck gate, decomposed (Q1 parked-role / Q2 Pivot-0-of-20)

**PROVENANCE: builder-commissioned fresh opus decode agent, s56 2026-08-22 (announced
on the coordination tail 11:44Z; report returned ~11:55Z and banked verbatim below by
the builder). Named inputs: bots/_v623healweld tree, scratchpad/s55_skalman_dose.py,
DECODE-firstcontact-v180-2026-08-22.md + the 65 archived first-contact replays.
Read-only: no bot edits, no platform calls; scratch instruments under
scratchpad/s56_treeq_*.**

---

**GAME CONTEXT:** everything below is in-game analysis for the Florent Code League — a sandboxed bot-vs-bot programming competition on a simulated grid under organiser-approved rules. "peck"/"attack"/"fire" are the engine's documented API verbs between competing game bots; nothing here targets real systems, networks or people.

# 0. TREE PROVENANCE — the tape is v623's gate chain, verified, not assumed

The 65 first-contact games are `ourver = 180` = **"Skalman rc619.1"** (`docs/coordination.md:72676`), i.e. the **`bots/_v619skalman`** tree. Diffed before reading tape facts onto v623:

| method | v619 vs v623healweld |
|---|---|
| `_cage_walker` | **byte-identical** (15,322 chars) |
| `_peck_priority` | **byte-identical** (3,298) |
| `_peck_out` | **byte-identical** (1,488) |
| `_attack_enemy_core` | differs **only** in the healweld (v619 `sk_roles.py:5087` `if (SK_CAGE_CEIL and SK_CORE_PECK_HEALGUARD ...)` → v623 `sk_roles.py:5156-5157` `if (SK_CORE_PECK_HEALGUARD ...)`) |
| `_siege_engineer` | differs (v620-623 nest planks) |

Flag defaults **identical across `_v619/_v620/_v622/_v623`**: `SK_CAGE=True(sk_maps.py:43)` · `SK_CAGE_FIRST=True(:79)` · **`SK_CAGE_CEIL=False(:182)`** · `SK_EVICT_ARMED=True(:159)` · `SK_ONE_CURSOR=False(:297)` · `SK_IDLE_ACT=True(:239)` · `SK_TARGET_PRIO=True(:66)` · `SK_CAGE_ACCEPT=7(:2473)` · `SK_CAGE_ACCEPT_MIN=3(:2687)` · `SK_CORE_PECK_HEALGUARD=True(:2680)`.

⇒ **The Q1/Q2 gate chain measured on the v180 tape is the chain v623 ships**, with one forward-looking delta priced in §5.

# 1. THE GATE CHAIN, `builder adjacent to enemy core` → `ct.fire(core_tile)`

All line numbers `bots/_v623healweld/`.

**`_peck_priority` — nine call sites, by function name:**

| # | line | enclosing function | `skip_core` | live? |
|---|---|---|---|---|
| 1 | `sk_roles.py:1296` | `_home_keeper` | absent (core admitted) | live — but this body works OUR ring |
| 2 | `sk_roles.py:4527` | `_cage_walker` | absent | **DEAD** — inside `if not SK_CAGE_FIRST:` and `SK_CAGE_FIRST=True` |
| 3 | `sk_roles.py:4604` | `_cage_walker` (lap offered nothing) | **True** | live |
| 4 | `sk_roles.py:4690` | `_cage_walker` (`SK_IDLE_ACT`, boxed in) | **True** | live |
| 5 | `sk_roles.py:4863` | `_cage_cursor_move` | True | **DEAD** — `SK_ONE_CURSOR=False` |
| 6 | `sk_roles.py:4867` | `_cage_cursor_move` | True | **DEAD** — same |
| 7 | `sk_roles.py:5167` | `_attack_enemy_core` (fallback) | absent | live, but only reached when **not** core-adjacent |
| 8 | `sk_roles.py:5206` | `_ore_denier` | absent (core admitted) | live |
| 9 | `sk_roles.py:5549` | `_siege_engineer` (`SK_IDLE_ACT_ENGINEER`) | True | live |

**`_attack_enemy_core` — the only path that actually fires at a core tile** (`sk_roles.py:5147-5164`) has **four** callers:
* `sk_roles.py:4458` — `_cage_walker`, inside `if not SK_CAGE:` → **DEAD** (`SK_CAGE=True`).
* **`sk_roles.py:4483` — `_cage_walker`, gated by `sk_roles.py:4475-4482`:** with `SK_CAGE_CEIL=False` the gate reduces to **`if sealed >= 7`** — literally, and nothing else.
* `sk_roles.py:5461` — `_siege_engineer`, the `live>=want` empty-ledger edge case.
* `sk_roles.py:5504` — `_siege_engineer`, `nest_site is None` and not relighting.

**Consequence from the code alone:** the CAGE WALKER — the only role stationed orthogonally adjacent to the enemy core by construction (`cage_lap` `sk_roles.py:195-213`, `LAP_SEAL_IDX` `:216`) — reaches the core-peck **only** through `sealed >= 7`. Every other peck it can make passes `skip_core=True`, and `_peck_out` (`sk_roles.py:4890-4891`) explicitly excludes the core ("the core is not a door").

# 2. Q1 — WHICH ROLE PARKS ADJACENT AND WHY IT DOES NOT PECK

**SUBJECT for every number: our team (v180 = rc619.1), the 65 first-contact unrated games of 2026-08-22 (13 matches; MIRROR = Bean counters v68 n=20 · PIVOT = Pivot v249 n=20 · KLADDE = kladde v173 n=25). Effective n = 58 (7 byte-identical repeats, all MIRROR/PIVOT, per DECODE-firstcontact §0.3).**

## 2.1 The role is the CAGE WALKER, and the gate is `sealed >= 7`

Role reconstruction mirrors `_claim_role` (`sk_roles.py:327-353`, ids `sk_maps.py:2394-2397`). Instrument `scratchpad/s56_treeq_roles.py`.

```
CORE-ADJACENCY ROUNDS AND CORE PECKS, BY RECONSTRUCTED ROLE
cell    role      adjRounds corePecks  bodies   sealed/empty/belt while adjacent
KLADDE  CAGE           1589       223      29   0-7 / 0-4 / 1-8
KLADDE  ENGINEER        124        76        9   0-5 / 0-4 / 2-8
MIRROR  CAGE            733       378      17   0-7 / 0-6 / 0-4
MIRROR  ENGINEER          6         0        2   1-3 / 1-6 / 1-4
PIVOT   CAGE            239         0      16   0-6 / 0-5 / 2-4
PIVOT   ENGINEER         33         0        7   0-5 / 0-4 / 3-4
```
**KEEPER and DENIER never once stand core-adjacent in 65 games** — independent behavioural confirmation of the role reconstruction.

## 2.2 THE CONCORDANCE IS PERFECT, 65/65

`scratchpad/s56_treeq_seal.py` measures `sealed` (our buildings on the 8 seal seats) every round of every game:

```
games where `sealed` EVER reached 7 : 11
games with >=1 CAGE core peck       : 11
identical sets                      : True
discordant either direction         : 0
```
Every CAGE core peck in the pool — all 601 — occurred at **`sealed == 7` exactly**. The one other firing game, `abd8f4fc..._game_2`, is the **ENGINEER** at `sealed = 3` (via `sk_roles.py:5504`) — which is why 12 games fire and only 11 are CAGE.

⇒ **Q1 MECHANISM: the walker parks adjacent and does not peck because `sk_roles.py:4482`'s `sealed >= 7` is false, so `_attack_enemy_core` is never called, and the two live in-walker peck sites (`:4604`, `:4690`) both pass `skip_core=True` while `_peck_out` (`:4890`) refuses the core by name.** This is the live half of the FIX-5 dead-code finding already stated in prose at `sk_maps.py:202-211`, now re-measured on a live-team tape.

## 2.3 The named parked games

| game | cell | adjRounds | bodies | role | core pecks | `sealed` range | their belt seats |
|---|---|---|---|---|---|---|---|
| `0de59936…_game_4` | KLADDE | **241** | 1 | CAGE | 0 | 1–3 | 4–5 |
| `abd8f4fc…_game_1` | KLADDE | **201** | 1 | CAGE | 0 | 1–3 | 4–5 |
| `b6ec7f91…_game_5` | KLADDE | 193 | 1 | CAGE | 0 | 1–3 | 4–5 |
| `d18b7d7b…_game_1` | KLADDE | 108 | 3 | CAGE | 0 | 0–3 | 5–8 |
| `919000f0…_game_2` | PIVOT | 26 | 1 | CAGE | 0 | 5–6 | 2 |

⛔ **CORRECTION TO THE RESEARCH FRAMING, and it changes the design read: those are cumulative adjacency rounds, not one continuous stand.** Longest contiguous run in `0de59936_g4` is **7 rounds** — the body is ORBITING, not parked (per-round trace in `s56_treeq_trace.py`; on adjacency rounds it stands on lap SEAL tiles at Manhattan d=1 from a core tile, so **mis-siting is REFUTED**).

## 2.4 Two other candidate blockers, both refuted on the tape

* **2-Ti cost gate** (`sk_roles.py:5137`, `:4378`): rounds where the body did nothing AND team titanium < 2 = **8 of 2,724 (0.3%)**. Not the binder.
* **An earlier branch consuming the turn — real and dominant.** CAGE core-adjacent rounds by emitted action: MOVE 50.1% · core attack 23.5% · other attack 14.8% · build 2.5% · heal 0.0% · IDLE 9.2% (n=2,561). The lap **skip-ahead at `sk_roles.py:4589-4595`** sits above the residual peck at `:4603-4604`, so it shadows any core admission there whenever it can step.

## 2.5 SURPRISE — THE ON-LAP PERIOD-2 ORBIT IS THE LARGEST SINGLE CONSUMER

Ring moves whose destination is the tile stood on 2 rounds earlier: **53.5% pool-wide** (MIRROR 38.1%, PIVOT 48.9%, KLADDE 59.0%; 1,786 of 3,338 ring moves). Both anti-orbit machines miss it: `_two_cycle_back` (`sk_common.py:589-607`) only re-ranks directions and falls back to the return leg when both perpendiculars are blocked (the normal ring state); `_cycle_commit`'s consumer (`sk_roles.py:4645-4648`) is **structurally unreachable while on the lap** because the skip-ahead (`:4581,:4593-4594`) returns first — INFERENCE from code read; the replay shows the orbit, not the issuing branch. `SK_ONE_CURSOR` — the fix built for exactly this — ships False with an outcome-refuting measurement in its own comment (`sk_maps.py:297-319`).

# 3. Q2 — WHY 0/20 vs PIVOT

**Not upstream: the walker reaches core adjacency in 16 of 20 Pivot games** (first contact median ~r60; 239 CAGE adjacency rounds across 16 bodies; the 4 never-adjacent games listed in the agent tape). Approach and siting work.

**The gate that fails is `sealed >= 7`, and vs Pivot it is arithmetically impossible:** their delivery belt terminates on the ring — 100% of their seal-seat occupancy is **conveyor** (0 barriers; 72 of 160 seat-games theirs, 75 ours, 13 empty), their belt holds 4 seal seats in 18/20 games (3 in 2/20), capping `sealed` at 4–5 against a hard bar of 7. **Games reaching `sealed>=7` vs Pivot: 0 of 20; rounds at `sealed>=7`: 0; max reached 2–6.**

| cell | games reaching `sealed>=7` | rounds at it | median their belt seal seats | core-peck games |
|---|---|---|---|---|
| MIRROR (BC v68) | 10 / 20 | 492 | 3 | 10 / 20 |
| PIVOT (v249) | **0 / 20** | 0 | **4** | **0 / 20** |
| KLADDE (v173) | 1 / 25 | 243 | 6 | 1 CAGE (+1 ENGINEER) |

The Pivot ENGINEER's 33 adjacency rounds also produce 0 pecks: they are the `live >= want` hold branch (`sk_roles.py:5426-5465`), which returns after `step_to(hold)` with no action.

# 4. INSTRUMENT VALIDATION — every zero driven to the other verdict first

| control | result |
|---|---|
| Known-positive reproduction | 12/65 games with ≥1 core attack, 677 total — identical to `s55_skalman_dose.py`'s independent ledger |
| Known cell `d18b7d7b_g5` | 223 attacks × 2 Ti = 446 — exactly the s55 expected 446 |
| PIVOT zero | same code path reads 378 (MIRROR) / 299 (KLADDE) — measured zero, not dead counter |
| `--swap` (enemy seat) | totals move completely — seat attribution discriminates |
| `--shuffle-roles` | all role cells collapse — role label load-bearing |
| `--mutate-adj` (Chebyshev-2) | parked-run table changes — adjacency test discriminates |
| `--nullguard` | wouldBlock 44 → 0 — the healguard predicate is live, not constant |
| s55 dose `--mutate` (2→3 dmg) | breaks 12/65 + known cell; unmutated 0/65 mismatches |

Channel discipline: all facts engine-side (positions/entity events); no bot stdout read (dead channel under fcode 2.3.6).

# 5. ⚠ FORWARD-PROJECTION WARNING ON v623 ITSELF

The healweld un-welds a guard that will **REDUCE** core pecks. Replaying the v180 tape's actual pecks against the un-welded predicate (enemy builder orthogonally adjacent to the pecked core tile → turn abandoned): **MIRROR 0/378 blocked · PIVOT 0/0 · KLADDE 44/299 (14.7%) · pool 44/677 (6.5%)** — concentrated in `abd8f4fc…_game_2` (53 of that game's 91 ENGINEER peck-rounds carried an adjacent enemy builder). **SUBJECT: ex-ante projection on the v180 tape under v623's predicate, not a v623 measurement.** This is the guard doing its documented job (declining a 4:1 heal-race exchange), and it is 0% in the cells where the peck count is already zero — it does not touch Q1 or Q2, both upstream. Named here so the adoption record carries it.

# 6. CANDIDATE FIX LEVERS, RANKED BY MEASURED DOSE

Doses are raw rounds × 2 Ti damage, before heal-tax. Measured heal-tax on THEIR cores: MIRROR 0.27 · KLADDE 0.75 · PIVOT 0.88 (aggregate; marginal tax on an added 2/round stream NOT identified — read every dose as an upper bound). Mean damage delivered into their core per game: PIVOT 274.5/500 · MIRROR 223.2 · KLADDE 231.3 — shortfall ~225-277 HP.

* **L1 — replace `sealed >= 7` with a REACHABILITY bar** (`sk_roles.py:4475-4482`): admit the core peck when no seal ACTION is available and no seat is evictable this round. Dose: 1,960 non-firing core-adjacent CAGE rounds across 54/65 games incl. ALL Pivot (239). ⛔ NOT the refuted `SK_CAGE_CEIL=True` (that lowered the bar to `8 − belt_seats` and ended the seal work, selling the healer-denial worth heal-tax 0.49-vs-0.71); L1 keeps sealing and re-admits the core only when there is nothing to seal this round.
* **L2 — break the on-lap period-2 orbit** (lap-index memory in the skip-ahead, which currently breaks after ONE attempt at `:4595` with no from-record). Dose: 1,786 shuttle rounds pool-wide (PIVOT 371, KLADDE 1,221). Orthogonal to L1.
* **L3 — admit the core at `:4604`/`:4690` + lift `_peck_out`'s exclusion** — fires only after seal/evict/lap-step all failed, cannot re-create the v601 lap-stall. Dose: 235 IDLE rounds (PIVOT only 3). Cheapest, weakest, lopsided away from the cell that asked.
* **L4 — give the engineer's hold branch an action** (`:5426-5465`). Unmeasurable dose from this tape (hold station never core-adjacent by design). Lowest priority.
* **L5 — clear the belt terminus, not the ring seat**: their seal-seat occupancy is 100% conveyor (20 HP = ten pecks); `_evict_seal` produces 378 other-attack rounds but `SK_CAGE_MELEE_GIVEUP=20` + `gave_up` retires each seat and they re-lay it. The seat is a symptom; the builder that re-lays it is the cause (same conclusion as `sk_maps.py:179-181` for ring barriers). Only route by which `sealed >= 7` becomes reachable vs Pivot at all.

# 7. SURPRISES (written before explaining away)

1. The concordance is exact — the gate is not *a* cause on this tape; it is *the* cause.
2. "Parked 241 rounds" is orbiting, not parked (longest stand 7 rounds; 50.1% MOVE vs 9.2% idle) — a fix aimed at "the idle body" touches 235 rounds; one aimed at "the orbiting body" touches 1,786.
3. Both prior fixes for this were built, measured, shipped OFF (`SK_CAGE_CEIL`, `SK_ONE_CURSOR`) — any new lever must be genuinely different or it re-runs a settled leg.
4. The 2-Ti gate is a non-issue (0.3%); mis-siting refuted.
5. v623's healweld cuts this channel further (§5) — correct on its own terms, named beside a plank that wants more core melee.
6. PIVOT has the highest heal-tax (0.88) AND the highest mean core damage delivered (274.5) — a 2-damage peck is worth least exactly where the peck count is zero. **The Pivot shortfall is unlikely to be closed by melee alone.**

# 8. WHAT THIS TAPE CANNOT ANSWER

* Which code branch issued each MOVE (skip-ahead-shadows-commit is INFERENCE; needs an instrumented local run, stderr only).
* Whether the enemy healer has spare capacity (aggregate ratio, marginal unidentified).
* Whether `sealed >= 7` is reachable vs Pivot under ANY policy (no durable seat eviction observed; counterfactual unmeasured).
* Duplicate contamination: MIRROR/PIVOT carry 7 byte-identical repeats (effective n ≈ 16-17/cell); the structural facts (belt seats 4 in 18/20, 0/20 reaching the bar) survive de-duplication; any Pivot share interval is ~13% optimistic.

Scratch instruments (read-only): `scratchpad/s56_treeq_{park,roles,seal,dose,trace}.py`.
