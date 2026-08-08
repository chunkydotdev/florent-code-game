# v74 "mineguard" delta read (x3r0 upload, auto-activated 07:15 local 2026-08-08)

**Status: COMPLETE — code half only.** Zero v74 matches in `replay_archive/`
at time of writing (136 archived OpenSverige matches, max `teamVersion` = 73;
newest are the v73 ladder set `4e0874d0` / `6fda11c0` / `b5a37d0b`). No
download taken. Production predictions are pre-registered in §5 to make the
next read falsifiable, per the v69 pattern.

Updates `docs/research/v72-delta-read-2026-08-08.md`, which stands unamended
except where flagged.

**Two builder mid-flight datums are answered against the diff:** the
12,530-Ti load-sanity tiebreak in **Q3b**, and the −6.7pp holder-leg drop
(45.0 → 38.3) in **Q6b**.

**Headline in one line:** v74 = v72 **plus 173 inserted lines and nothing
else**. Mineguard is two proactive sentinels parked beside his own harvesters
on quiet maps from r80. It is not ore defense, it is not ore denial, it fixes
no defect, and it contains none of our code.

---

## Version tags and corpus (rule 2)

**Subject.** v74 "mineguard", `bots/opp_v74/main.py`, md5
`cb5452e66c69a21d8aa1af340cdc37dd` (**verified**), 4238 lines. Directory
contains `main.py` and a `__pycache__` only — **no auxiliary module**.

**Predecessor.** v72 "chainwatch", `bots/opp_v72/main.py`, md5
`1d2e804564df6207bea8ddc90cdcc27c` (prefix `1d2e8045` as briefed), 4065
lines. This is the correct lineage predecessor: v73 was OUR bot in the shared
team slot, and his v70/v71 were interim uploads never long-held.

**Diff.** `diff -u opp_v72 opp_v74` → **6 hunks, +173 / −0**.
`difflib.SequenceMatcher` over the two line lists returns **zero `delete` and
zero `replace` opcodes** — the delta is a **pure insertion**. Every line of
v72 survives in v74 byte-for-byte. Insert points (v74 line ranges):

| # | v74 lines | + | What |
|---|---|---|---|
| 1 | :24-33 | +10 | module docstring, "M1 variant: MINE-GUARD SENTINELS" |
| 2 | :492-508 | +17 | `DOCTRINE M1` comment block + `MINEGUARD_CAP/MIN_HARV/MIN_RND` |
| 3 | :734-740 | +7 | `self.mine_guards = 0` in `__init__` |
| 4 | :2710-2808 | +100 | `_mine_guard_harvester` / `_mine_guard_site` / `_try_mine_guard` |
| 5 | :2901-2907 | +7 | `_defend` action phase: build half |
| 6 | :2966-2997 | +32 | `_defend` move phase: walk half |

Of the 173: ~57 comment/docstring lines, ~7 blank, **~109 live code**. All in
`_defend` and its three new helpers. **Nothing outside `_defend` changed.**

**Dirs / files read (all read-only, no bot edited, no arena run, no download).**
`bots/opp_v74/`, `bots/opp_v72/`, `bots/_v84g/` (our v73), `bots/_v81e6e/`
(its base), `bots/_v85hs/`, `bots/_v85hsb/`, plus a negative-search sweep over
`bots/_v7*/main.py` and `bots/_v8*/main.py` (28 files). Docs:
`docs/research/orekeeper-v69-delta-read-2026-08-07.md`,
`docs/research/orekeeper-v69-production-read-2026-08-07.md`,
`docs/research/v72-delta-read-2026-08-08.md`,
`docs/research/v72-bleed-nonfamily-2026-08-08.md` (incl. §10),
`docs/research/v73-production-read-2026-08-08.md`,
`docs/research/tiebreak-split-decode-2026-08-07.md`,
`docs/graft-brief-2026-08-08.md`, `docs/game-model.md`, `docs/coordination.md`,
`HANDOVER.md`, `maps/`, `replay_archive/*.meta.json`.

**Live at write.** v74 holds the team slot (auto-activated 07:15, first match
1600@347 #24). Our lineage head `_v84g` / v73 "Eir 7" is retired to dev.
All line refs below are `opp_v74/main.py` unless tagged v72.

---

## VERDICT BLOCK

### Q1 — WHAT "MINEGUARD" IS: **the ranked hypothesis is REFUTED.** It is not ore defense, not ore denial. It is two proactive sentinels parked beside his own harvesters.

The name points at ore; the code points at **turrets guarding harvesters**.
Full mechanism:

**The claim in his own words** (:28-33, :492-504, docstring at :2776-2779):

> kladde forensics (2026-08-08): kladde loses 0-1 harvesters per game to our
> ~10 (6,000+ Ti per game in rebuilds and lost income) by standing sentinels
> OVER their own mines — 34-48% of income at t200 on 13-16 sentinels plus
> ammo — while our turret construction is exclusively threat-reactive
> (counterbattery) or forward (siege).

**The branch.** The single `role_n == 4` defender gets a third mode. Gates
(all must hold, build half `_try_mine_guard` :2775-2808):

1. `self.mine_guards < MINEGUARD_CAP` (2) — :2781
2. `ct.get_current_round() >= MINEGUARD_MIN_RND` (80) — :2783
3. `ct.read_store(SLOT_HARVESTERS) >= MINEGUARD_MIN_HARV` (4) — :2785
4. `self._eco_spendable(ct, ct.get_sentinel_cost() + 10)` — :2789
5. `not under and not endgame` — the call site, :2906
6. a visible unguarded friendly harvester exists — :2791
7. a legal adjacent build tile within dsq ≤ 8 of it exists — :2794

Then `ct.build_sentinel(bp, facing)` (:2798), `self.mine_guards += 1`
(:2799), and `SLOT_HOME_GUN += 1` (:2807).

**Target pick** (`_mine_guard_harvester` :2710-2741). One
`ct.get_nearby_buildings()` pass (default `dist_sq` = the builder's own
vision, **r²=20**) collects friendly harvesters and friendly sentinels;
harvesters with any sentinel at `distance_squared <= 32` are skipped; nearest
survivor wins. Every per-id getter is inside `try/except: continue` (:2722,
:2730) — no new crash surface.

**Site pick** (`_mine_guard_site` :2743-2773). Walks `CARDINALS` in fixed
order N, E, S, W (:42, :2755) and returns the **first** tile that is (a)
in-bounds, (b) `distance_squared(hpos) <= 8`, (c) not a decoded ore cell
(:2764), (d) not within manhattan 1 of a core footprint tile (:2768), (e)
`can_build_sentinel(bp, facing)`. `facing = nearest_cardinal(bp.direction_to(
enemy_core_anchor))` (:2770), falling back to map centre if `self.enemy` is
None (:2754).

**Walk half** (:2966-2996). Same gates, in `_defend`'s move phase, placed
below the shelled come-home (:2933), the threat chase (:2940) and the link
queue (:2945), and above the home orbit (:2998). If a legal site is already
adjacent it **holds position** (:2988-2993); otherwise `self.tgt = <harvester
position>` and `self._nav(ct, pave=False)` (:2994-2995).

**So: does v74 defend ore, deny ore, or guard harvesters?**

| Reading | Verdict |
|---|---|
| Clears / prevents **enemy** barriers on ore (the rev-4 §S4 finding) | **NO.** Nothing in v74 reads whether an ore tile has been buried. `_try_screen`'s v71 guard (:2669-2670-era) and the new :2764 clause both only stop **him** building on ore. |
| Denies **enemy** ore offensively | **NO.** No hunk touches `_plan_siege`, `_saboteur` or any forward build path. |
| Guards his own mines with turrets | **YES** — this is it. Two sentinels, capped, quiet-map only. |

The `:2764` ore skip is the **third** application of the same self-denial
lesson in three versions (E2b for conveyors, v71 `_try_screen` for barriers,
M1 for sentinels). It is the ore-shaped part of the name — and it is
defensive of his *own* sites only.

**One pre-existing mine-defense path already existed and is untouched:**
`_turret_on_harvester` (:2177-2215, ancestral, present in v72 at :2143)
detects an **enemy** turret within dsq ≤ 8 of a friendly harvester and feeds
`_hunt_turret`. M1's docstring correctly describes this as reactive. M1
borrows that function's dsq ≤ 8 band as its own placement radius (:2745-2746)
— but see FLAG 3: the band was measured for a *gunner besieging* a harvester
(r²=13 reaches it), not for a *sentinel guarding* one (single-tile line).

---

### Q2 — OUR-PIECE UPTAKE: **ZERO. Nothing of ours entered v74.**

The pure-insertion result settles this without further search: every one of
our pieces is in exactly the state v72 left it. Verified individually anyway:

| Piece | v74 status | Evidence |
|---|---|---|
| **Piece H** (endgame spend-switch) | **PRESENT, verbatim, unchanged from v70/v72** | 14 `PIECE H` cites :432, :909-923, :1092, :2847, :2886, :2896, :2905, :3046, :3102 — same set as v72 at −173-line offsets |
| **H-1 fix** (live-turret registry instead of core-vision scan) | **ABSENT** | `_core_turret_mix` (:1091-1124) still scans `ct.get_nearby_buildings()` from the Core's r²=36. `grep "turret registry\|SLOT_TURRET"` → 0. The only `live-turret` hit (:1094) is the pre-existing docstring naming the defective gate. **The graft brief §2.2 defect is UNFIXED in v74 — brief needs no same-day correction.** |
| **E2b** ore-pave ban | his own, unchanged | :3977-3992 / :4011-4020, byte-identical to v72:3804-3819 / :3839-3847. No gating beyond his own E2 line. |
| **E1** ammo floor | his own, unchanged | :1002 `ti_floor = 12 if under else (46 if weapons else 52)` |
| **E1 cap** (our Eir 5.1 burnable-ammo cap) | **PRESENT since v70, unchanged** | :955 `cap = (LAST_RND - rnd) * (3*guns + 5*sents)` — ours, already taken |
| **S1** own-building guard on `_intercept` | **ABSENT** | :3435-3448 unchanged: `tbid` read at :3441, passed only to `_duel_safe`, `elif ct.can_fire(tp) and self._duel_safe(ct, tp, tbid): ct.fire(tp)`. **No team test.** |
| **Piece N** pave-crash guard | **ABSENT** | `grep "PIECE N\|piece N"` → 0. `ct.is_tile_empty(pp)` at **:3977** still outside any `try`. |
| **Piece I** (rotation latch) / **J** (counterbattery discipline) / **K** (gated core heal) | **ABSENT** | `grep` → 0 each |
| Our heal-seat work (`_seat_ban`, `HS_HEAL_DETAIL`) | **ABSENT** | `grep` → 0 |

**Byte-similarity counts: verbatim 0, adapted 0, absent 5** (S1, N, H-1,
I/J/K, seat work). The two of ours he already holds (H and the 5.1 cap) came
in v70 and are untouched.

**Direction of traffic has reversed for now.** v70 was a verbatim graft of our
code. v74 is entirely his own work, sourced from his own overnight kladde
forensics — the same pattern as v72's `_chain_dead` (whose docstring cited
"Pivot-forensics (2026-08-08)"). `grep "MINEGUARD\|mine_guard"` over all 28
`bots/_v7*/_v8*` files → **0 hits**: M1 has no precedent in our line either.

---

### Q3 — DEFECT STATUS AUDIT: **every item UNCHANGED. Nothing was fixed.**

The pure-insertion diff is a complete proof for this section — no v72 line was
altered — but each was re-located and re-read in v74:

| # | Defect (v72 delta read §UNFIXED / graft brief §1.7) | v74 | v74 cite |
|---|---|---|---|
| 1 | **Delivery-freeze / `_link_path` re-plan** — fires only from "a harvester was just built" plus the one chainwatch site | **UNCHANGED** | still exactly **3** call sites: :2706, :3074, :3221 (= v72 :2672, :2901, :3048). **No fourth site, no break-triggered re-plan.** |
| 2 | `SLOT_HARVESTERS` monotonic high-water | **UNCHANGED** | `_sync_harvesters` :1146-1147, `if live > read_store(...)`, no decrement anywhere |
| 2b | `SLOT_HOME_GUN` monotonic | **UNCHANGED, and made worse** | never decremented (his own docstring says so, :1104); M1 adds a **fourth** increment site at :2807 |
| 3 | **Crash-class unguarded `is_tile_empty`** | **UNCHANGED** | :3977 `... and ct.is_tile_empty(pp):` — no `try`; the E2b `try/except` still sits eleven lines below on the same variable. Second site :4011 (`is_tile_empty(nxt)`) likewise ancestral. Third version running. |
| 4 | **E4 ledger scope** (futile swings on turrets) | **UNCHANGED** | ledger still only in `_sabotage_prio`; `ct.fire(` sites :1902, :2504, :3448, :4057, :4094, :4100 — five outside it |
| 5 | **Enemy-throw handshake gap** | **UNCHANGED** | :1491 `if ct.read_store(SLOT_LAUNCHED_ID) == ct.get_id() + 1:` — own throws only |
| 6 | **v71 screen self-block** (barrier on a trunk conveyor's outflow → `_chain_dead` DEAD → `_link_path` blocks the trunk; FLAG 2) | **UNCHANGED** | `_try_screen` and the `_link_path` dead-trunk clause untouched; still never `destroy()`s the offending barrier |
| 7 | **Chainwatch repair-crawl** (the v72 bleed suspect, FLAG 1) | **UNCHANGED** | watchdog :3192-3224, `_chain_dead` :3545, `_build_next_link` still pops occupied tiles it never verifies |
| 8 | E2a hoist (below the `move_cooldown` return) + gate width | **UNCHANGED** | :3226 gate vs :3238 block |
| 9 | Unknown-map link BFS still paves ore | **UNCHANGED** | `_link_path` fallback branch, no `get_tile_env` ore test |
| 10 | `_try_build_launcher` takes the first legal adjacent tile from a core-side builder (graft brief §1.5(b) / bleed §10.d, the corpus's most frequent impassable seat blocker) | **UNCHANGED** | :1178-1200: `for d in DIRECTIONS: ... if can_build_launcher(bp): build_launcher(bp)` — no core-seat exclusion |

**Crash-class status for the NEW code: clean.** All three M1 helpers wrap
every per-id engine getter (:2722-2731); `get_nearby_buildings`,
`get_position`, `read_store`, `get_current_round`, the cost getters and
`can_build_sentinel` are non-raising; `map_grid` is bounds-safe because `bp`
is range-checked first (:2757). `build_sentinel` at :2798 is preceded by
`can_build_sentinel` at :2771 in the same helper — but note the two calls are
in **different turns' worth of state only within one `run()`**, i.e. the same
turn, so no TOCTOU. Everything remains inside `run()`'s blanket
`except Exception`. **No new unguarded engine-call pattern.**

---

### Q3b — THE 12,530-Ti DATUM: **not a delivery-freeze fix. There is no fix to find.**

The builder's mid-flight steer asked specifically for a third `_link_path`
call site or equivalent break-triggered re-plan. Answer, at the strongest
level of evidence this read can produce:

- The v72→v74 diff is a **pure insertion** (zero `delete`, zero `replace`
  opcodes). No line of the chain machinery was touched.
- `_link_path` call sites: **3 in v72, 3 in v74**, at the same three logical
  positions (:2706, :3074, :3221).
- `_chain_dead` / CHAIN WATCHDOG: 3 references in each file, same structure.
- `_build_next_link`: unchanged, still treats occupancy as completion.
- All 173 added lines are inside `_defend` and its three new helpers. The
  economy path (`_expand`, `_link_path`, `_build_next_link`, the pave trail,
  `_sync_harvesters`) is **not reachable from any of them**.

**So the 12,530 has a different cause.** Four candidates, ordered:

1. **Map.** drumlin is, by his own measured table (:87), the **most open map
   in the pool at 0.6% wall fraction** — the single map his comment singles
   out as "the near-wall-free map". Long unobstructed trunks are exactly the
   condition under which his linker does not fail. This is the leading
   explanation.
2. **Opponent.** opp_v63 is his own much older version, i.e. a same-lineage
   sparring partner, not a field opponent. Both sides run the same economy
   code; the game is an economy race his newer build should win.
3. **n = 1, one seed.** And his line ships `NOISE_ON = True` (PIECE G, :368):
   `self.spawn_salt = random.Random().randrange(97)` per game (:1080-1081), so
   a single game is a single draw from a genuinely stochastic process.
4. **PIECE H** already bursts harvesters and stops laying links from r960
   (ours, present since v70 — so present in the v72 baseline too).

**And the baseline it is being compared against is stale.** The 5/11
delivery-freeze rate is a **v68-era** measurement (11 r1000 games, coordination
:785). The v69 production read then found **zero freezes in 20 games across
both versions** and explicitly retired the number ("The v68 read's 5/11 rate…",
production read :483-484). 12,530 delivered is also unremarkable for this
lineage: the v69 corpus records 17,410 (in a *losing* tiebreak), 21,300,
10,240, 23,310 and 26,570. **12,530 sits mid-range.** It is not what a fixed
freeze looks like; it is what an open map looks like.

Recommended framing for the builder: treat the load-sanity number as a
**map-and-opponent artefact**, not a capability signal, and do not let it move
the tiebreak-class battery expectations vs opp_v74. If it is worth resolving,
the cheap paired measurement is v72 vs v63 on drumlin seed 1 — same map, same
opponent, same seed. Under this read it should land in the same band.

---

### Q4 — CARRYOVER AUDIT: everything from the v72 chain carries. Three items sharpen.

| Finding (source) | v74 status |
|---|---|
| v72 delta read Q1 — chainwatch partial fix, vision-bounded, `SLOT_HARVESTERS` untouched | **CARRIES verbatim** |
| v72 delta read Q2 — Piece H at r960 is the last behavior switch | **AMENDED: M1 adds `MINEGUARD_MIN_RND = 80`**, a new round gate, the first non-endgame one since `SURGE_MIN_RND = 300` |
| v72 delta read Q3 — v71 orescreen is decoded-map-only | **CARRIES, and DEEPENS a fourth time** — M1's own ore skip (:2764) is likewise `map_grid is not None` |
| v72 delta read Q4 — graft premise (E2b/E1/E2a/E4 unrefined) | **CARRIES** |
| v72 delta read Q5 FLAGS 1-6 (repair crawl, screen self-block, double BFS, `endgame_dumped` drip suppression, r960 reserve collapse, fresh-harvester false positive) | **ALL CARRY** — no hunk touches any of them |
| v72 delta read Q6 — ancestral pave crash unguarded | **CARRIES** (:3977) |
| Bleed **L1** (never pave the 8 core heal seats) | **CARRIES UNFIXED** for conveyors/launchers — but M1 is the **first build path besides `_try_screen` to carry a core-adjacency exclusion** (:2768). Partial, incidental compliance in one new path only. |
| Bleed **L2** (lifetime spawn ceiling 18; nordkap seat A capped at 4) | **CARRIES**, and see FLAG 2: nordkap seat A is also the map that gets a **double** mineguard budget |
| Bleed **L3** (home ray coverage of the d²=16-32 belt; sentinels cannot rotate) | **PARTIALLY, ACCIDENTALLY ADDRESSED.** M1 puts up to 2 sentinels (r²=32) on the map that are neither counterbattery nor siege — his line's first proactive sentinels. But they are sited by *harvester* proximity, not by core-ring geometry, and their facing is fixed. Whether any lands on a live ring bearing is coincidence. **L3 as specified (re-faced coverage of the belt) remains unfixed.** |
| Bleed **L4** (finish the last link, re-plan on break) | **CARRIES UNFIXED** — see Q3b |
| Bleed **L5** (ammo floor sized for a standing home turret) | **CARRIES, and M1 makes the mis-sizing worse** — see FLAG 4 |
| Bleed **L6** (stop spending builder actions on enemy conveyors) | **CARRIES** — S1 unfixed |
| Bleed **L7** (standing answer to the adjacency plant) | **CARRIES** |
| Bleed **L8** (Leviathan CPU forfeit) | opponent-side, unaffected |
| v73 production read **S4** (ore burial: 8 sites denied, we neither run nor defend) | **CARRIES for his line too.** v74 does not notice buried ore. |
| v73 production read **S1** (Piece H's core-vision gate) | **CARRIES into v74** — H-1 unfixed |
| v69 read: "the post-r300 window is uncontested" | already REFUTED at r960 by Piece H; now additionally **contested from r80** on quiet maps |

**Staleness corrections this read issues.**

1. The **5/11 delivery-freeze rate is stale as a live expectation** for this
   lineage. It is a v68 number; v69's production corpus measured 0/20. Stop
   quoting it as v72/v74's expected rate — quote L4's *specific* signatures
   instead (two missing conveyors at the core end; six harvesters with no
   adjacent conveyor; wiredness 9/33, 20/37, 4/29).
2. **"His turret construction is exclusively threat-reactive or forward" is
   now false**, in his own words and in code, from r80 on quiet maps.
3. **`SURGE_MIN_RND = 300` / `ENDGAME_RND = 960` are no longer the full set of
   round gates.** Any read that enumerates behavior switches must add r80.

---

### Q5 — FIVE PRE-REGISTERED PRODUCTION-READ PREDICTIONS

Each names the exact counter and its falsifier.

**P1 — ORE BURIAL STAYS UNANSWERED.**
*Counter:* per game, (a) count of ore tiles occupied by an **enemy** building
at any point, (b) count of v74 actions (`BuilderAttack`, `destroy`, turret
fire) that target such a building, (c) count of harvesters v74 builds on a
tile that was previously enemy-occupied.
*Prediction:* (a) ≥ 1 per game against the burial class (baseline: 8 tiles
across the v73 corpus, Leviathan 4 + 0033 4), **(b) = 0 in every game**, (c) =
0. v74 also lays **0** of its own conveyors/barriers/sentinels on decoded ore.
*Falsifier:* any v74 action that clears an enemy building off an ore tile.
*Why it matters:* the ranked hypothesis for this read was that "mineguard"
answered §S4. It does not. The denial row stays open in both directions.

**P2 — MINEGUARD FIRE RATE AND THE NORDKAP DOUBLE BUDGET.**
*Counter:* sentinels built by v74 at `distance_squared ≤ 8` from a friendly
harvester, on a round ≥ 80, with no enemy threat reported — the M1 signature.
Tally per game, per map, per seat.
*Prediction:* **0 in any game that ends before r80** (the v68-era median win
was r97, so expect a substantial zero-fraction); **1-2 in quiet long games**;
**exactly 0 on hive seat (21,3)**, because `_defend`'s `hive_bunker` branch
returns in the move phase at :2919-2923 so the walk half is unreachable and
only an already-adjacent harvester can trigger the build half. **Up to 4 on
nordkap 20×26 seat (9,6)** — that map promotes `role_n == 3` to `"defend"`
(:1549-1553) alongside the standing `role_n == 4` seat, and `self.mine_guards`
is a **per-unit** counter (:740), so two defenders carry independent budgets.
*Falsifier:* > 2 mineguards on any non-nordkap map with a single surviving
defender; or any mineguard before r80.
*Second-order:* the counter never decrements, but a **defender death resets
it** (his comment concedes: "its `role_n == 2` successor … starts a fresh
interpreter and thus a fresh count", :736-739). Under kladde/Leviathan melee
attrition, count defender successions per game — the true cap is
2 × successions.

**P3 — THE GUARDS ARE MOSTLY INERT (the mechanism test).**
*Counter:* per mineguard sentinel: shots fired over its lifetime; whether the
guarded harvester's eventual killer ever stood on the sentinel's facing line;
harvester deaths within dsq ≤ 8 of a mineguard vs harvester deaths elsewhere
in the same game.
*Prediction:* **median shots per mineguard sentinel ≤ 2 over its whole
lifetime**, and **no measurable reduction in harvester loss rate for guarded
vs unguarded harvesters in the same game**.
*Mechanism (the reason to expect it):* a sentinel is a **single-tile-wide line
shot** and **cannot `rotate()`** (gunner-only in the API). `_mine_guard_site`
takes the **first** legal cardinal-adjacent tile in N,E,S,W order (:2755) and
faces it at `nearest_cardinal(bearing to the enemy core anchor)` (:2770) —
there is **no test that the harvester, or any approach to it, lies on that
line**. A melee raider must stand orthogonally adjacent to the harvester to
attack it; it is covered only if that tile happens to fall on the one guarded
row/column. He borrowed the dsq ≤ 8 band from `_turret_on_harvester`
(:2745-2746), where it was measured for a **gunner besieging** a harvester
(r²=13 covers the whole disk), and reused it for a **sentinel guarding** one
(one line). The geometry does not transfer.
*Falsifier:* mineguards firing ≥ 5 shots median, or a clear guarded/unguarded
survival split.
*Scope — this prediction is opponent-conditional, and the exception is the
important case.* It is a prediction about **passive** opponents, who present
no target on the ray. Against an opponent that **sends builders at his
harvesters** the same fixed facing becomes an aimed corridor, because the ray
points from his mine at the aggressor's core — which is the bearing the
aggressor arrives on. **Our own line is exactly that opponent** (`_v84g`
ranks HARVESTER as melee priority 2). Split this counter by opponent class
before reading it; a low median across the field is compatible with a sharp
effect against us. See Q6b.

**P4 — THE COST-SCALE TAX.**
*Counter:* `get_scale_percent()` at r200 / r500 / r1000, and the effective
`get_harvester_cost()` / `get_conveyor_cost()` at each, on games where 2
mineguards land vs same-map v72 baselines.
*Prediction:* **~+40 percentage points of team-wide scale** in v74 relative to
v72 on those games (`docs/game-model.md`:365-374: a **single** team-wide
additive scale, **+20% per sentinel**, shared across conveyors, harvesters and
builder bots alike; it reverses when the entity dies). Two mineguards
therefore tax **every subsequent build in the game**, not just turrets. His
own pricing — "two guards is insurance priced at ~2 sentinels + ammo headroom"
(:503-504) — **omits this entirely**. At a mid-game scale near 250% the direct
cost alone is ~150 Ti, not 60.
*Falsifier:* no measurable scale delta on games where guards landed — which
would instead falsify the game-model scale measurement and should be escalated.

**P5 — HIVE SELF-FREEZE (new defect, conditional).**
*Counter:* on hive (25×25, core anchors (2,20)/(21,3)), record
`SLOT_HOME_GUN` at r42 and at the round of the first mineguard; then record
expander activity (builds, moves) for the remainder of the game.
*Prediction:* in any hive game where `SLOT_HOME_GUN` is still **0** at r80,
the first mineguard sets it to 1 (:2807) and **`hive_freeze` (:3010-3016)
turns true from the next round, causing every `_expand` unit to `return`
immediately for the rest of the game** — a permanent, self-inflicted economy
stop. `SLOT_HOME_GUN` is never decremented, so it cannot recover.
*Honest sizing:* his forward-siege build (:2111) and counterbattery
(:2685, :2689) also set this slot, and usually will have done so before r80 —
so this fires only in hive games that stay quiet with no gun built. Expected
rare. Hive is 1 of 15 pool maps. But the failure is total when it occurs, and
his M1 comment audited only the counterbattery gate at :2636, not this one.
*Falsifier:* a hive game with a mineguard at r80+ where expanders keep
working, i.e. `SLOT_HOME_GUN` was already ≥ 1.

---

### Q6 — TIEBREAK / SLOT IMPLICATIONS

**Against the field's bleed classes.**

- **kladde v75 (standoff-ring, the class M1 is aimed at): predicted no
  change, and the premise is contested by our own decode.** x3r0's
  *observation* is corroborated — our bleed doc measures kladde harvesters
  climbing 6/10/12/13/15 while his fell 4/5/7/10/3 (bleed §2.1), i.e. roughly
  his "0-1 vs ~10". But his *causal attribution* is not. Our decode of the
  same opponent (bleed §2.1-2.3) attributes kladde's harvester survival to
  (i) a **2:1 economy lead** that funds rebuilds, (ii) a **heal line** that
  finished 8 of 10 games at exactly 500/500 core HP with 209/240 and 243/250
  heals near their own core, and (iii) **forward-planted harvesters** inside
  d² ≤ 72 of *our* core from r12. And the 13-16 sentinels he priced as mine
  guards are, in our measurement, **his own siege ring**: `3de9f5e0` g4 has
  **25 kladde sentinels built inside d² ≤ 72 of our core**, ten of them on the
  single tile (10,9) at d²=25. "Sentinel near their mine" and "sentinel in our
  half" are the same turrets, because their mines are in our half. **M1 copies
  the correlate, not the mechanism** — and at cap 2 versus their 13-16, i.e. a
  low-dose copy of a doctrine whose dose-response is untested. He says as much
  ("thirteen is kladde's whole doctrine and unmeasured on our economy curve",
  :503-504).
- **CAD-family (ray/bimodal laws):** unaffected. No hunk touches the opening,
  siege planning, counterbattery or the heal line. The ray-coverage law
  (answered turrets die in a median 10 rounds, unanswered live 65.5) predicts
  the **only** upside available to M1: an enemy siege turret that happens to
  land on a mineguard's fixed line dies fast. Coincidence-rate, per P3.
- **0033-style sentinel siege:** unaffected; L3 unfixed, so the d²=25 bearing
  problem stands. New in v43 per the v73 read — gunners alongside, barrier
  ore-denial — is unanswered by v74 (P1).
- **Adjacency-plant class (Ouroboros v8, Leviathan v25):** L7 unfixed. M1's
  guards are near harvesters, not at d² ≤ 1 of the core where 751/881 and
  830/1856 of their shots originate. No effect predicted.

**Net directional call on the delta itself, revised after the builder's leg
datum (Q6b):** against the *passive* field, small and probably slightly
negative for him in long games (P3 inertness + P4 scale tax + FLAG 1 defender
displacement), with one rare catastrophic tail (P5). **Against opponents that
push builders at his economy it is plausibly positive for him**, because the
fixed facing aims the guard down the aggressor's own approach corridor. Our
line is in the second category. So the delta may be **field-neutral and
specifically anti-us** — which is the shape the −6.7pp leg datum has, and a
reason not to read a holder-leg drop as a field-wide capability gain.

**For OUR next candidate's holder leg — what makes old baselines misleading.**

1. **The divergence set is precise and narrow.** v74 ≡ v72 in *every* code
   path except `_defend` on a quiet map at r ≥ 80 with ≥ 4 harvesters and the
   bank to fund a sentinel. **Any leg whose games end before r80 is
   bit-comparable to a v72 leg.** So short-game legs (rush classes, small-map
   collapse) do **not** need re-running.
2. **Long tiebreak grinds DO.** The `_v85hs` stage-1 bar recorded **244 of 480
   games reaching r1000** — that matchup is a tiebreak grind, and it is
   precisely the regime where M1 is live for ~900 rounds. The holder-leg
   rebase to opp_v74 is **not cosmetic** for `_v85hs`/`_v85hsb`.
3. **What our candidate will newly meet:** up to 2 (up to 4 on nordkap seat A)
   sentinels at r²=32, 18 dmg, ignoring obstacles, sited near his harvesters
   and facing our core anchor. Our line's measured winning recipe against this
   family is "contest the ore belt from r5" (bleed §2.3) — walking builders
   toward his harvesters is exactly what crosses those lines. Expect a small
   attrition tax on our forward builders after r80, concentrated on the
   bearing from his mines toward our core.
4. **A counterweight in our favour:** his +40pp team-wide scale (P4) raises
   *his* harvester, conveyor and builder-bot prices for the rest of the game.
   In a delivered-Ti tiebreak that is a small structural handicap for him.
5. **The old `_v85hs` bar (51.2 [46.8,55.7] / 480 vs `_v84g`) is a self-leg**
   and remains valid as attribution only — per the standing rule, ship
   verdicts weigh the class-weighted vs-field battery, not the holder leg.
   The rebase changes the holder leg's *opponent*, not the verdict rule.
6. **Reproducibility caveat unchanged:** opp_v74 carries `NOISE_ON = True`
   (:368) exactly as v72 did, so opp_v74 legs are pooled-read only; no
   paired-seed determinism against him.

---

### Q6b — THE −6.7pp DROP: attribution for our v73 content vs opp_v74 (45.0 → 38.3)

Builder datum (in-batch compact legs, batch-comparable with hsb's 60.0): our
v73-content scored **38.3 vs opp_v74** where the same leg vs **opp_v72 scored
45.0**. The diff admits exactly one candidate mechanism. Ranked by what the
code actually supports:

**RANK 1 — THE GUARD CORRIDOR. The sentinels are aimed at the bearing our
saboteurs arrive on, standing beside the entity our saboteurs rank #2.**
Confidence in the mechanism (conditional on the drop being real): **high — it
is the only behavioral change in the file.** Chain, end to end:

- Our `_sabotage_prio` (`_v84g:2142-2157`) ranks melee targets
  `GUNNER/SENTINEL: 0, CORE: 1, **HARVESTER: 2**, LAUNCHER: 3,
  CONVEYOR/SPLITTER: 4, BARRIER: 5`. **His harvesters are our saboteur's
  second priority**, and our `_saboteur` (`_v84g:2361`) is a standing forward
  seat.
- M1 plants a sentinel at `distance_squared ≤ 8` of one of those harvesters
  (:2759) — i.e. **inside the disk our saboteur must enter to attack it**.
- The facing is `nearest_cardinal(bp.direction_to(enemy_core_anchor))`
  (:2770) — the enemy core is **ours**. So the guarded ray points from his
  mine **at our core**, which is the bearing our forward builders travel in
  on. Our nav is BFS-shortest-path, which on open maps hugs that line.
- A sentinel is **18 dmg, reload 2, r²=32, and ignores obstacles** — no cover
  exists on the ray. A builder bot has **40 HP: three shots, ~5 rounds**.
- Our `_duel_safe` clause (c) (`_v84g:2056-2065`) reads "its current firing ray
  does not cover this builder's tile" as **SAFE to melee**. So our builder,
  standing off-ray beside a 40-HP sentinel, will spend ~20 swings / 40 Ti
  grinding it (prio 0) instead of the harvester — the L6 misallocation, newly
  baited. On-ray it just dies.
- **The compounding cost is bodies, not titanium.** Bleed §10 established that
  the binding constraint on our heal line in 101/101 sampled siege rounds was
  **bodies in reach**, not seats and not money. Every forward builder killed
  or pinned at his mines from r80 is one fewer healer at our core later.

This mechanism also explains the *sign asymmetry* the builder should expect:
it costs us more than it gains him, because he is spending 2 sentinels + 40pp
of team-wide scale (P4) to delete our most valuable forward bodies.

**RANK 2 — (a) HARDER INCOME TARGETS.** Same mechanism, economic framing:
denial of his harvesters is one of our win paths against a same-lineage
economy fork, and it now carries an 18-dmg toll. Not separable from Rank 1 in
a replay; treat as the same finding measured on a different counter (his
harvester uptime rather than our builder deaths).

**RANK 3 — (d) ECONOMY SCALING: WRONG-SIGNED, cannot be the cause.** M1 costs
*him* ~+40pp of a **single team-wide additive scale**
(`docs/game-model.md`:365-374), raising his own harvester, conveyor and
builder-bot prices for the rest of every game where guards land. If anything
this should have moved the leg **toward** us. Any drop must be paid for
against this headwind, which slightly *raises* the implied size of Rank 1.

**RANK 4 — (b) DELIVERY-FREEZE FIX: REFUTED, zero diff support.** No such fix
exists (Q3b). Our tiebreak-#1 wins against him do **not** evaporate through
this route. Note the related staleness: those wins were never resting on a
5/11 freeze rate — that is a v68 number the v69 production read retired at
0/20.

**(c) as literally stated — "new anti-builder-melee or anti-displacement
logic" — is ABSENT.** There is no new code that detects, deters or displaces
enemy builders. The effect above is **emergent geometry**, not a coded
counter. This distinction matters for the graft conversation: there is no
mechanism here to copy, only a placement rule.

**Confidence that the drop itself is real: this read cannot assess it, and
two known confounders apply.** Stated plainly for the hsb ship case:

1. **Compact-leg n and CI.** A −6.7pp difference needs its interval before it
   is a finding. The project's own harness **batch-drift** result (session 15)
   already retro-caveated the v69 deltas and produced the **paired-measurement
   standard** — which applies here directly.
2. **His line is stochastic.** `NOISE_ON = True` (:368) draws a fresh
   `spawn_salt` per game (:1080-1081) in **both** opp_v72 and opp_v74, so
   these legs carry more than binomial variance and are pooled-read only.
3. **A large fraction of games cannot contain the mechanism at all.** M1
   cannot fire before r80, and needs ≥ 4 harvesters, a quiet map and the bank.
   If the leg's games are short, the mechanism has no room to produce −6.7pp,
   and the drop is more likely drift.

**What a production replay must show to confirm — the decisive split is cheap
and is a strict test.** Because v74 is bit-identical to v72 everywhere except
this branch, the effect must be **entirely carried by games that contain a
mineguard**. So:

1. **Partition the leg.** Games with ≥ 1 M1-signature sentinel (built r ≥ 80,
   `dsq ≤ 8` from one of his harvesters, no threat reported) vs games with
   none. **Prediction: the v74-vs-v72 gap is ~0 in the no-guard partition and
   carries the whole −6.7 in the guard partition.** If the gap appears in the
   no-guard partition, the drop is batch drift or noise, full stop — no code
   in v74 can produce it.
2. **Also partition by game length at r80.** Games ending before r80 must show
   **zero** gap. This is the strongest single falsifier available.
3. **Our builder deaths by attacker**, per game, restricted to deaths within
   `dsq ≤ 32` of an M1 sentinel; and whether each death tile lies on that
   sentinel's computed ray (recompute `nearest_cardinal(bp.direction_to(our
   core anchor))` from the build event and walk the line).
4. **Our forward-builder round-count in his half, before vs after the first
   guard lands** — the pinning/deterrence half of the effect, which costs us
   even when nobody dies.
5. **Our melee swings against sentinels** (the `_duel_safe` clause-(c) bait):
   swings on M1 sentinels per game, and Ti spent on them.
6. **Knock-on check:** our core-heal acts per siege round and our builder
   population at the round of our core deaths, guard-games vs no-guard games —
   the bleed §10 bodies channel.

If (1) and (2) come back clean-split, the attribution is settled and the hsb
ship case can price it. If they do not, the −6.7 belongs to the harness, not
to x3r0.

---

### Q7 — C8 NOTE: which constants-era assumptions expire on v74's activation

**The re-seed is caused by the version bump itself, not by M1's behavior.**
His own PIECE G docstring states the law (:351-352): *"A rated game is a pure
function of (opponent, opp_version, map, our_version, our_seat); mapSeed does
not vary it."* `our_version` changed at 07:15. Therefore:

- **EXPIRED: every mid-game constants row keyed to the v72 or v73 era** for
  the deterministic-book opponents (Ouroboros, the CAD family). Mid-game rows
  were already flagged perishable in the CAD v116 read; they are now
  definitively re-seeded.
- **EXPIRED: any v73-era row at all**, since v73 was our bot and v74 is a
  different `our_version` from both v72 and v73.
- **NOT EXPIRED BY BEHAVIOR, only by key: the opening rows.** M1 cannot fire
  before r80 (`MINEGUARD_MIN_RND`, :507, :2783, :2982). v74's behavior in
  rounds 0-79 is **bit-identical to v72's** given identical inputs. So the
  frozen opening assets from the CAD read (launcher round + tile, spawn tiles,
  r2-4 throw destinations, r6 self-destroy, 8/8/8 ammo) are unchanged *on our
  side of the causal chain*.
- **The untested axis, and a free experiment.** The CAD read established
  opening-row independence across **their** version churn (v107→v116,
  byte-identical rows on 4/5 maps). Independence across **our** version change
  was never tested. v74 is the ideal probe for exactly that: because its
  pre-r80 behavior is provably identical to v72's, **any opening-row change
  observed under v74 is attributable to the version-keyed re-seed alone, not
  to a behavior change.** If the rows hold, opening-row re-freeze becomes safe
  across our own bumps too — a standing asset. If they move, `our_version` is
  a real book input and every opening row must be re-extracted per submission.
  Recommend the post-v74 corpus be collected with this split in mind; it
  merges cleanly with the quadruple-due C8 re-extraction already parked.
- **Standing caveat, unchanged:** determinism against OpenSverige was already
  partial. `spawn_salt = random.Random().randrange(97)` (:1080-1081) is drawn
  per game from OS entropy whenever `NOISE_ON` — true in v72 and v74 — so our
  own core's spawn dispersion already diverges game to game. C8 rows describe
  the *opponent's* book, not ours.

---

## What changes for the graft brief TODAY

**Nothing has to be retracted. Two lines gain force, one gains a caveat, and
one item is new.**

- **§0 premise ("the merge is already running in both directions") — CORRECT
  but now one-directional at the margin.** v70 took our Piece H verbatim; v74
  takes nothing. The brief's framing survives; the sentence "he took our code
  first" can be sharpened to "he took our code once, in v70, and has shipped
  only original work since (v71 orescreen, v72 chainwatch, v74 mineguard)".
- **§1.1 (S1 team check), §1.2 (E2a hoist + gate width), §1.3 (chain-repair
  economics), §1.4 (pave-crash guard) — ALL STILL LIVE, verified line-by-line
  in v74.** Every ask in the brief is still an ask. Cites move to
  `opp_v74/main.py`: S1 at **:3442-3448** (`tbid` read :3442, untested
  `ct.fire(tp)` :3448), E2a at **:3226 gate vs :3238 block**,
  `_build_next_link` at **:3746** with the pop-occupied line at **:3756-3758**,
  pave crash at **:3977**.
- **§1.5(b) (the `_try_build_launcher` seat hole, "three-line gate") — STILL
  LIVE at :1178-1200**, and now with a same-file precedent to point at: M1's
  `_mine_guard_site` carries exactly the core-adjacency exclusion the brief
  asks for (**:2766-2769**). The conversation can say "you already wrote this
  gate this morning; it belongs on the launcher too."
- **§1.7 (remaining unfixed list) — UNCHANGED, all five items.** Add a sixth:
  `SLOT_HOME_GUN` now has a **fourth** never-decremented increment site
  (:2807).
- **§2.1 (a real re-plan — what OUR line takes from his) — UNCHANGED.**
  chainwatch is still the only original chain work in his line, still
  vision-bounded and 12-hop-capped, still repair-from-the-harvester. Our graft
  design (third `_link_path` call site, vision-local detection, repair from
  the break) is unaffected.
- **§2.2 (the H-1 defect he inherits) — NO SAME-DAY UPDATE NEEDED.** v74 does
  **not** fix it. `_core_turret_mix` (:1091-1124) still counts turrets through
  the Core's own r²=36 vision; there is no live-turret registry
  (`grep "SLOT_TURRET|turret registry"` → 0). Piece H remains dead weight in
  both lines and the brief's proposed fix is still the right one.
- **NEW ITEM for §3 (do-not-graft) — M1 itself, provisionally.** Do not copy
  mineguard as-built into our line: cap 2 with a fixed cardinal facing and
  first-legal-tile placement is a low-dose copy of a 13-16-sentinel doctrine,
  it taxes a single team-wide cost scale by ~40pp, and our own kladde decode
  attributes kladde's harvester survival to economy + heal line + forward
  siting rather than to mine guarding (Q6, §2.1 of the bleed doc). If the
  placement idea is worth anything to us it is the *facing* insight from Q6b —
  a guard aimed down the aggressor's approach corridor — not the cap or the
  target-picking rule.

---

## FLAGS — new risks introduced by M1, ranked

**FLAG 1 (top) — the sole defender walks away from home, and the come-home
rule cannot recall it.** The walk half sets `self.tgt = <harvester position>`
and navigates (`:2994-2995`), with no distance bound: as long as the target
harvester stays in vision (and it does, since the defender is walking toward
it), the branch keeps returning and the home orbit at :2998-3006 never runs.
The "DEFENDER COMES HOME" rule at :2933 requires `shelled`, which requires the
Core to be **in this builder's own r²=20 vision** — so a defender that has
walked past ~4 tiles from home **cannot be recalled by it**. The remaining
recall is the `under` + `SLOT_THREAT` chase at :2940, which sends it to the
**threat tile**, not home. Net: on a quiet map from r80, his one standing home
body may be several tiles out of position when a siege opens. Against the
bleed corpus's core-death profile — where the binding constraint was measured
as **bodies**, not titanium or seats (bleed §10) — this is the most plausible
way M1 loses games.

**FLAG 2 — nordkap seat (9,6) gets a double mineguard budget, on his worst
seat.** `role_n == 3` is promoted to `"defend"` on that exact map/seat
(:1549-1553), alongside the standing `role_n == 4` seat, and `mine_guards` is
per-unit (:740). Up to 4 sentinels, ~4×20pp of scale. Bleed L2 records his
nordkap seat-A record as **0-3** and notes `nordkap_home_a` caps the builder
base at 4 — so the map that can least afford the spend gets double the dose,
and two of its four builders can both be walking to mines.

**FLAG 3 — the guard geometry does not follow from the evidence cited.**
Detailed under P3. Short form: dsq ≤ 8 is a *gunner-besieging* band reused for
a *sentinel-guarding* role; the site is the first legal cardinal tile with no
coverage test; the facing is fixed and sentinels cannot rotate.

**FLAG 4 — two more sentinel mouths on a gunner-calibrated magazine.** The
ammo target is `max(AMMO_FLOOR=16, min(48, 4 * weapons))` in peacetime (:975,
:986-988), and his own comment sizes `per_gun = 4` as "one shot each" — a
**gunner** figure. A **sentinel costs 10 ammo/shot**. With `weapons` at 1-3 the
target stays pinned at 16, i.e. **one sentinel shot plus change for the entire
team**. M1's `+10` build-time headroom (:2787-2789) is a one-off check on the
*titanium* bank, not a commitment to convert. The predicted state is exactly
the failure his own atoll comment names — dry turrets. This also sharpens
bleed **L5**.

**FLAG 5 — the coverage predicate is structurally blind.** `_mine_guard_harvester`
tests "is there a friendly sentinel within dsq ≤ 32 **of the harvester**"
using a sentinel list drawn from `get_nearby_buildings()` at the **builder's**
r²=20 (:2721). A sentinel 32 from the harvester can be ~10 tiles (dsq ~100)
from the builder — five times outside the disk that could see it. So the
"already guarded" test can only ever succeed for sentinels that happen to be
within r²=20 of the builder. He acknowledges the direction of the error
(:2715-2718) and bounds it with the cap; the honest statement is that the test
is **near-inert**, and the pick is effectively "nearest visible harvester".

**FLAG 6 (low) — `SLOT_HOME_GUN` inflation.** A fourth never-decremented
increment site (:2807) on a slot his own docstring calls out as broken
(:1104). Direct downstream effects are small (the E1 floor drops 52→46 once
`weapons` becomes non-zero; the ammo target is unmoved below `weapons = 4`)
— but it is the trigger for P5, and it makes the "how many guns do we have"
question strictly less answerable in a merged line.

---

## Method notes

- **Files.** `bots/opp_v74/main.py` md5 `cb5452e66c69a21d8aa1af340cdc37dd`,
  4238 lines; `bots/opp_v72/main.py` md5 `1d2e804564df6207bea8ddc90cdcc27c`,
  4065 lines. No auxiliary modules in either directory.
- **Diff method.** `diff -u` plus an independent
  `difflib.SequenceMatcher(None, v72_lines, v74_lines, autojunk=False)` opcode
  dump. Six `insert` opcodes, **zero `delete`, zero `replace`**, 173 lines
  inserted. Offsets cross-checked against every `PIECE F/G/H` cite and every
  `_link_path` / `SLOT_HARVESTERS` / `SLOT_HOME_GUN` site: all shift by exactly
  the cumulative insertion prefix, confirming pure insertion independently.
- **Attribution.** M1 names itself in three places (:28, :492, :2901) and cites
  its own dated forensics. The base is labelled "Everything else is
  bit-for-bit Y1_chainwatch" (:32-33) — corroborated by the diff. Whether a
  v73-era interim upload of his exists between v72 and v74 cannot be
  determined from artifacts we hold, but it does not matter: **the whole of
  v74 minus v72 is M1**, so there is no unattributed capability.
- **Negative searches.** `MINEGUARD|mine_guard` over all 28
  `bots/_v7*/main.py` + `bots/_v8*/main.py` → **0**. `PIECE N|piece N|PIECE
  I|PIECE J|PIECE K|SLOT_TURRET|turret registry|_seat_ban|HS_HEAL_DETAIL`
  over v74 → **0** each. `is_tile_empty(pp)` → one site, unguarded (:3977).
  `ct.fire(` → 6 sites; only :3448 lacks a team test on the building it
  damages. `build_splitter` → still 0 (the `_chain_dead` splitter branch
  remains dead code for his own network).
- **Cost-scale semantics** taken from `docs/game-model.md`:365-374 ([measured]:
  one team-wide additive scale, reversible on destruction), not from the
  organisers' CLAUDE.md table.
- **Read-only throughout:** no bots edited, no arena or platform command run,
  no downloads, no replays parsed (none exist for v74), HANDOVER and tape
  untouched.

## Open questions

- **Is x3r0's kladde harvester-loss attribution testable directly?** Our bleed
  corpus measures harvester *counts* over time, not deaths with causes. A
  targeted re-decode of the kladde matches (`98e2c1fc`, `3de9f5e0`) counting
  harvester destruction events by attacker type, and the position of every
  kladde sentinel relative to both cores, would settle whether their sentinels
  are mine guards or siege ring. This is the highest-value follow-up: if it
  confirms our reading, M1 is a copy of a correlate and the graft conversation
  should say so plainly.
- **What is E3?** Still no trace, four versions on. Question for x3r0 stands.
- **Does `hive_freeze` ever actually fire from M1 (P5)?** Cheap to check once
  a hive v74 replay is archived.
- **Do the mineguard sentinels ever get healed?** The chain medic is the only
  repair path and it is off past `ENDGAME_RND`; nothing in M1 registers the
  guards for maintenance, so a chipped guard is a permanent 20pp of scale
  standing on the map at reduced HP.
- **Carried from the v72 read and still open:** whether the v72 bleed onset was
  v70 or v72. v74 does not help split it, but it also does not contaminate the
  question — the pre-r80 window is unchanged, so a v74 corpus can still be
  pooled with v72 for opening-phase measurements.

---

## Addendum (2026-08-08): the null-partition test (Q6b resolved)

**Version tags.** `bots/_v84g/main.py` (g84, our v73-content) md5
`cbb0b8b449110f89be9765028fbf8c54` — **verified against the briefed
`cbb0b8b4` prefix.** `bots/opp_v74/main.py` md5
`cb5452e66c69a21d8aa1af340cdc37dd` — **verified against the briefed `cb5452e6`
prefix**, matches Q6b's own version tag. Our live platform slot = v74 (x3r0)
throughout.

**Corpus.** `partition_g84_v74.json` (60 rows) joined to
`partition_replays/*.replay26` (60 files) on `(map, seed, seat)`: 15 maps × 2
seeds × 2 seats, g84 vs opp_v74. Parsed with a purpose-built extension of
`tools/replay_census.py`'s wire-level helpers (`tools/replay_schema.md`
gotchas applied throughout) that keeps full turn-by-turn entity state —
position, HP, alive/dead, direction — rather than only the first-build
summary the stock `Replay` class keeps; this was necessary for M1 detection,
lifetime shot tracking and the damage ledger below. `print_counts.tsv` (60
rows, ARENA-STDERR channel) joined on the same key. `hsb_v74_full_print_counts.tsv`
(480 rows) and `hsb_v74_compact_print_counts.tsv` (120 rows) used for marginal
context only — **no replays behind either, explicitly labelled below.**

### 0. Self-checks

| Check | Result |
|---|---|
| JSON-vs-replay outcome agreement (win/turns/cond), 60 games | **60/60** |
| Delivery identity (`core_deliv × 10 == titaniumCollected`), 120 team-sides | **120/120** |
| `print_counts.tsv` vs JSON's own `tb` column, 60 games | **60/60 agree** (cross-tool consistency) |
| Corpus total tracebacks | **19** (matches the briefed 19/60 exactly) |

**Damage-ledger spot check — run over all 60 games, not just 3.** For every
`FireTurret` event where the source tile held a live gunner/sentinel, the
target tile's live occupant (looked up in the running position index *at fire
time*, not post-hoc) was checked for a matching same-round HP delta (−7
gunner / −18 sentinel), pooled per `(round, id)` so multi-hit rounds are
matched one-for-one rather than by round-wide value scanning (an earlier pass
of this check used round-wide matching and produced false positives — fixed
before any number below was trusted).

- **23,608** gunner/sentinel `FireTurret` events, both teams, all 60 games.
- **13,443 (56.9%) had no live occupant on the target tile at fire time** —
  a miss, not a parser gap: `get_attackable_tiles()` is documented as
  "ignores... occupancy," and the replay shows both bots routinely firing on
  fixed or remembered tiles whether or not anything is standing there (walked
  round-by-round in one case: a v74 sentinel at (9,3) on atoll fired at the
  same empty tile (14,3) every second round for 30+ rounds straight).
- **10,113 (42.8%) matched a same-round, same-id HP delta — a confirmed
  hit.** Of those: **7,574 landed on a unit-layer entity** (builder bot,
  gunner, sentinel, launcher, core) and **2,539 (25.1%) landed directly on a
  building** (1,765 conveyor, 672 harvester, 102 barrier).

**This corrects `tools/replay_schema.md`'s "damage-target law."** That note
states turret fire "hits the UNIT... NOT on a building occupying it,"
verified on 30 events in an earlier read (25 enemy-unit hits, 0 *own-building*
hits — a narrower claim than the bolded headline, on inspection). This
corpus's evidence is unambiguous and walked event-by-event: e.g. game
`g84_atoll_2_a`, round 264 — `FIRE from=(1,11) to=(5,7)` is immediately
followed by `HP id=483 delta=-18`, where id 483 is a v74 conveyor built the
prior round at exactly (5,7), with no unit ever registered on that tile. The
same conveyor is healed (+4, from an adjacent builder), fired on again two
rounds later, and dies. This repeats on freshly-rebuilt conveyors at the same
tile five more times over the game. **Turret fire damages whatever occupies
the target tile, building or unit; the "NOT on a building" clause in the
standing law does not hold.** Flagging this here rather than editing
`replay_schema.md` directly — this addendum's write scope is this file only —
but it should be corrected, since any future decode that assumes turret fire
is building-immune will misattribute damage. It also matters directly for
mechanism color below.

### 1. M1-signature per game

Pre-registered signature applied literally: a v74 sentinel built at round ≥
80 within `dsq ≤ 8` of a live v74 harvester.

- **23/60 games (38.3%) contain ≥ 1 M1-signature sentinel; 48 total across
  the corpus.** First-build rounds range 81–974 (gate obeyed everywhere: 0
  instances below r80). Lifetimes range 5–919 rounds (mean 517).
- **Falsifier check (P2):** M1-signature sentinels in a game ending before
  r80 — **0**, as required. But note the corpus caveat below: this corpus
  cannot test the *complementary* falsifier (zero gap in games ending before
  r80), because every game in it runs past r80.
- **Hive cross-check:** 4/4 hive games, **0 M1-signature sentinels** —
  matches the delta read's "exactly 0 on hive seat" prediction exactly (the
  `hive_bunker` move-phase return blocks the walk half).
- **Nordkap cross-check:** 4/4 nordkap games carry M1 (the only map at
  100%), counts 2, 2, 3, 2 — consistent with the "double budget" prediction
  (`role_n==3` promoted to defend alongside `role_n==4` on this seat); the
  observed max in this n=4 sample is 3, not the predicted ceiling of 4 —
  directionally confirmed, not fully saturated at this sample size.
- **By map, games-with-M1/4 (total sentinels):** nordkap 4 (9), atoll 3 (7),
  eider 3 (6), antler 2 (7), drumlin 2 (5), lighthouse 2 (3), moonrise 2 (3),
  fjordgate 1 (2), jackpot 1 (1), meander 1 (2), saga 1 (1), snowflake 1 (2),
  archipelago 0, heart 0, hive 0. Concentrated on quiet/open maps exactly as
  M1's own gates predict (round≥80, ≥4 harvesters, no threat, the bank to
  fund a sentinel) — archipelago/heart, both fast-resolving maps in this
  corpus (median game length well under 400 rounds), never reach the
  conditions.

**Facing-corroboration caveat — this matters for how much to trust the
"23/60" count itself.** M1's own site code always computes a *cardinal*
facing (`nearest_cardinal(...)`); a diagonal facing is structurally
impossible for a genuine M1 build. **10 of the 48 flagged sentinels (21%)
have a diagonal facing** — these are provably **not** M1, they are ordinary
threat-reactive/siege/counterbattery sentinels that happen to satisfy the
round+distance geometric test by coincidence. Restricting to the 38
cardinal-faced sentinels drops the game count to **21/60 (35%)** — only 2
games (`g84_eider_2_a`, `g84_jackpot_1_a`, both wins for us) lose
M1-present status under the stricter filter. Of the 38 cardinal-faced
sentinels, 24 also match this addendum's own `nearest_cardinal`-toward-our-
core recomputation exactly (a simplified tie-break heuristic, offered as
corroboration only, not a claim of exact engine parity). **Bottom line: the
geometric-only signature has a real but modest false-positive rate (~1 in 5
sentinels, ~2 in 23 games); the qualitative story is unchanged by the
correction, and — see §2 — the gap widens slightly, not shrinks, under the
stricter filter.**

**P3 cross-check (mechanism, "guards are mostly inert") — sharply
confirmed.** Shots fired per M1-signature sentinel over its full lifetime,
all 48: median **2.0** (cardinal-only 38: median **1.0**), against a
pre-registered prediction of "≤ 2 median." Distribution is heavily
right-skewed by two long-lived sentinels that racked up 83 and 448 lifetime
shots by repeatedly firing on a fixed, mostly-empty tile for hundreds of
rounds (the same miss-heavy pattern documented in §0). **27/48 (56%) landed
at least one shot on an occupied tile across their entire lifetime; 21/48
(44%) never connected with anything, the whole game.**

### 2. The null-partition test

**Honesty constraint first: every game in this 60-game corpus runs past
round 80** (shortest game is 113 rounds). The delta read's single strongest
proposed falsifier — "games ending before r80 must show zero gap" — **cannot
be run against this corpus**; there is no pre-r80-ending partition to test.
That is a genuine coverage gap in this batch, not a null result, and it means
this addendum settles the *M1-present-vs-absent* half of the pre-registered
test only, not the *game-length* half.

**M1-present vs M1-absent, this batch (n=60):**

| Split | Win rate | 95% Wilson |
|---|---|---|
| All 60 (batch reproduction) | 23/60 = 38.3% | [27.1, 51.0] |
| M1-present (loose, geometric signature) | 7/23 = 30.4% | [15.6, 50.9] |
| M1-absent (loose) | 16/37 = 43.2% | [28.7, 59.1] |
| M1-present (strict, cardinal-faced only) | 5/21 = 23.8% | [10.6, 45.1] |
| M1-absent (strict) | 18/39 = 46.2% | [31.6, 61.4] |

Fisher's exact test (two-sided, computed directly — no scipy in this venv):
loose split **p = 0.42**; strict split **p = 0.10**. **Neither clears
conventional significance at this n.** The gap is in the predicted direction
and gets *larger*, not smaller, when the two probable false-positive games
are removed (both were wins for us, so removing them from the "present"
bucket pulls that bucket's rate down and the "absent" bucket's rate up) — a
mechanism-consistent, non-adversarial robustness signal, but still short of
decisive.

**Confounds, as pre-registered, checked directly:**

1. **Game-length/map confound is real and visible.** M1-present games
   concentrate on the same quiet/open/long maps that this matchup tends to
   grind out to r1000 on anyway (nordkap, atoll, eider). Because every game
   in the corpus is already ≥ 113 rounds, the "M1-eligible vs not" and "long
   game vs short game" splits nearly coincide here — there is no clean
   short-game control group inside this batch.
2. **Turns-regime split, for context (not a clean M1 control on its own):**
   r1000 grinds 13/32 = 40.6% [25.5, 57.7]; core-kill games (any length)
   10/28 = 35.7% [20.7, 54.2]. Materially overlapping, unsurprising given
   (1).
3. **Map-level table (games-with-M1/total, win rate each half) — n is too
   thin per cell (0–4) to read causally, included for completeness:**
   nordkap withM1 2/4 noM1 0/0; atoll withM1 1/3 noM1 1/1; eider withM1 1/3
   noM1 1/1; hive withM1 0/0 noM1 2/4; archipelago withM1 0/0 noM1 2/4;
   heart withM1 0/0 noM1 2/4; jackpot withM1 1/1 noM1 0/3; saga withM1 0/1
   noM1 2/3; snowflake withM1 0/1 noM1 2/3; antler withM1 0/2 noM1 1/2;
   drumlin withM1 1/2 noM1 1/2; lighthouse withM1 1/2 noM1 1/2; moonrise
   withM1 0/2 noM1 1/2; fjordgate withM1 0/1 noM1 0/3; meander withM1 0/1
   noM1 0/3.

### 3. Mechanism color (M1-present games only, n=23)

**Channel A — the guard corridor (melee bait), as hypothesized in Q6b Rank
1.** Our builder deaths within `dsq ≤ 32` of a live M1 guard at the moment of
death: **72**, out of 190 total our-builder deaths across the 23 M1-present
games. Of those 72:

- **40 (56%) took zero confirmed hits from that specific guard** before
  dying — died to something else (another turret, another builder, a
  different guard) while merely in the vicinity. Proximity to a guard is not
  by itself evidence of guard causation.
- Hit-count-before-death distribution: 0→40, 1→11, 2→15, 3→6.
- **6/72 (8%) match the predicted ~3-hit-kill signature** (18 dmg × 3 ≥ 40
  HP) exactly.
- **26/72 (36%) died on a tile that lies on the guard's fixed facing ray** —
  used as a cheap proxy for "on the aimed corridor" in place of a full
  per-round position replay of every builder (out of scope for this pass;
  flagged rather than silently substituted). Example on-pattern death: game
  `g84_antler_2_b`, builder #4, died round 225, took exactly 3 hits from the
  guard before dying.

**Channel B — direct building fire, NOT hypothesized in Q6b, found by the
damage-ledger check in §0.** Of the corpus's 2,539 turret-on-building hits,
**26 were fired by an M1-signature sentinel specifically, and all 26 (100%)
landed on one of *our* buildings** — 14 harvesters, 12 conveyors, spread
across 10/23 M1-present games (antler ×2, atoll, drumlin ×2, eider ×2,
fjordgate, lighthouse, nordkap). Several are repeat kills on the same
position: e.g. `g84_drumlin_1_a`, one M1 sentinel (#1537) kills our
harvester #253 at (12,10) over rounds 417/419, then our harvester #156 at
(13,10) over rounds 421/423, then a rebuilt conveyor at (11,10) over rounds
516/518. **This is a second, previously undocumented M1 damage channel:**
the guard's fixed facing ray does not just threaten a melee saboteur walking
through it, it directly destroys any of our unattended forward
harvesters/conveyors that fall on that line. Framed as mechanism-consistent
with Rank 1/Rank 2 of Q6b (same underlying geometry — the ray points from
his mine at our core, i.e. down our own approach bearing), not as a
free-standing new hypothesis.

**Bodies-drain proxy** (mean live our-builder-bot count at round
checkpoints, games reaching that checkpoint only — not a paired measurement,
different games contribute to different checkpoints):

| Round | M1-present mean (n) | M1-absent mean (n) |
|---|---|---|
| 80 | 4.83 (23) | 5.00 (37) |
| 200 | 5.23 (22) | 5.07 (29) |
| 400 | 5.86 (21) | 5.30 (20) |
| 600 | 5.90 (20) | 6.80 (15) |
| 800 | 6.21 (19) | 7.33 (15) |
| 999 | 6.65 (17) | 7.20 (15) |

Early-game (r80–400) counts are comparable or slightly *higher* in
M1-present games; a gap in the predicted direction (M1-present lower) opens
only from r600 on. **Mechanism-consistent with a cumulative late-game drain
once guards have been up for hundreds of rounds, but this is an unpaired,
survivorship-biased read (only games that reach r600+ contribute to that
row) — suggestive, not confirmatory.**

**Attribution language, as instructed:** the guard-corridor and
direct-building-fire channels are **mechanism-consistent** with the −6.7pp
drop, not proof of it. Both are real, repeatable, corpus-verified game
events; neither is large enough on its own, in this n, to certify the full
size of the drop.

### 4. Print-correlation (ARENA-STDERR channel)

**Channel label, stated plainly:** `print_counts.tsv` counts Tracebacks
captured on shared stderr from **both bots' uncaught-exception handlers** —
it is not attributable to one side without further evidence, and none of
what follows should be read as "v74 crashed more" without that caveat.

- Joined 60/60 games. JSON's own `tb` column reproduces `print_counts.tsv`
  exactly everywhere checked.
- **Mean print_count, M1-present games: 0.74/game (17 tracebacks over 23
  games). M1-absent: 0.05/game (2 over 37).** A roughly 15× difference.
- **Open attribution, per the task's own framing:** the project has
  historically found opponent-side diagnostic prints correlating with *our*
  displacement of their builders (the "spitball entry" pattern). M1-present
  games are also, by construction, games that ran long enough and quiet
  enough to reach the M1 gates — i.e., games where our forward pressure
  against v74's economy had time to accumulate. The elevated print rate in
  M1-present games is therefore **at least as consistent with "these are the
  games where we pushed hardest on his mines" as with "M1 itself throws
  more exceptions."** This corpus cannot separate the two; both track the
  same underlying variable (sustained forward contact with v74's economy).

**Marginal-only context (no replays behind either table, stated per the
task's channel-labelling instruction):**

- `hsb_v74_full_print_counts.tsv`: 480 rows, 97 prints (0.202/game); r1000
  subset (264 games) carries 95 of those 97 prints (0.360/game) — the
  overwhelming majority of prints in the full marginal cluster in long
  games, consistent with §3's late-game-accumulation read.
- `hsb_v74_compact_print_counts.tsv`: 120 rows, 19 prints (0.158/game).
- Task-briefed context reproduced: v74's marginal rate is ~4× v72's
  (97/480 vs the briefed 13/120); this replay-joined 60-game partition shows
  19/60 (0.317/game), the same order of magnitude.

### Verdict

**The −6.7pp drop is mechanism-consistent with M1, not decisively
attributable to it at this n.** Three things are true at once:

1. **Directionally, everything points the same way.** M1-present games win
   at 30.4% vs 43.2% for M1-absent (widening to 23.8% vs 46.2% under the
   stricter cardinal-faced filter, which if anything strengthens rather than
   weakens the read since it drops two probable false positives that were
   both wins for us). Two independent, real damage mechanisms exist and are
   corpus-verified: melee bait near the guard (Channel A) and direct fire on
   our unattended forward buildings (Channel B, previously undocumented).
   P3's "mostly inert" prediction is sharply confirmed (median 1–2 lifetime
   shots, 44% never connect) — consistent with a *small*, not large, per-
   guard effect, which fits a −6.7pp-sized leg-level drop better than a
   large one would.
2. **Statistically, this batch cannot certify it.** Fisher's exact two-sided
   p = 0.42 (loose) / 0.10 (strict) on the M1-present/absent split — neither
   clears significance at n = 23–39 per arm. The wide, heavily overlapping
   Wilson intervals ([15.6, 50.9] vs [28.7, 59.1]) say the same thing more
   bluntly: this n cannot rule out that the entire M1-present/absent gap is
   sampling noise on top of the map/length confound.
3. **The corpus's single cleanest possible test is unavailable here.**
   Every game in this batch runs past r80, so the "zero gap in games ending
   before r80" falsifier — structurally the strongest test the delta read
   proposed, because it requires no behavioral inference at all, only a
   round count — cannot be run. This is a corpus-composition gap, not
   evidence against M1.

**For the ship case:** treat the −6.7 as **plausibly real and
mechanism-supported**, price it as a modest tax concentrated in long, quiet
games against this opponent (consistent with the delta read's own
"field-neutral and specifically anti-us" framing), but do not treat this
partition as statistical confirmation — it is a directionally-consistent,
sub-significant result with a genuine mechanism behind it, not a closed
case. **The next decisive step, cheap and specific:** a corpus (or a
targeted pull from the existing 480/120-row marginal tables, if replays for
any of those games can be located or regenerated) that includes games
ending before r80, so the one falsifier this batch couldn't run can finally
be run.
