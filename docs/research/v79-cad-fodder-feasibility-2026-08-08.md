# v79 CAD "THROW FODDER" — FEASIBILITY GATE (2026-08-08)

**Question routed from the builder's field sweep (`results.tsv` row `field-sweep-9v`):**
v79 "Eir 10" scored **53.3 on the cad_probe leg vs v75/v77's 73–77**. Hypothesis: the OS
plank's early standoff WALKER crosses the lane on close-core maps and gets grabbed and
thrown by a CAD-class launcher (launchers pick up *either* team's adjacent builders), and
the lost tempo is the dip.

**Provenance.** Read-only. **95 games / 19 matches** — every CtrlAltDefeat match in
`replay_archive/` — decoded with `docs/research/2026-08-07-fanout/toolkit/replay_lib.py`
under `.venv/bin/python`. No games run, no bot file touched. Source read of
`bots/_v91osb/main.py` (v79, **md5 `6a909e72`**) and `bots/cad_probe/main.py`. Sweep
per-game data read from the builder's `sweep_cad_probe.json` (270 rows, 9 heads × 30).
`cad_probe` remains **attribution-only** (standing: 20–27 pts too easy vs wild). Scratch
scripts in `…/scratchpad/cad_fodder/` (not committed).

---

## 1. VERDICT — **(c) IMPOSSIBLE BOTH. The dip needs a different owner — and the replays name it.**

Three independent kills, in increasing order of decisiveness:

1. **The instrument cannot do it.** `cad_probe` **explicitly team-filters its throw
   candidates** — `main.py:1358–1361`: `if ct.get_team(uid) != my_team: return`. It does
   not even tile-scan; it reads one tile from `SLOT_THROW_REQ`, which only its own raiders
   write (`main.py:647`). **The leg that produced 53.3 is mechanically incapable of
   throwing our builder.** This alone closes the case for the number under investigation.
2. **Wild CAD has never done it.** **0 cross-team throws by a CAD launcher in 95/95
   games**, across all three eras. Its whole throw budget (215 throws) is spent on its own
   raiders in **r2–r5, never later** (max round of any CAD throw in the corpus: **r5**).
3. **Wild CAD declined the one opportunity that ever arose.** In 95 games an opposing
   builder stood inside a live CAD launcher's pickup ring exactly **once** — and CAD did
   not throw it (§4).

**But the dip is real, and it is partly the OS plank — via a different mechanism.** The
sweep's per-game data shows v79 losing **both fjordgate games with 0 Ti delivered and
0–5 buildings standing** (v75/v77 won the same two games with 4,510–10,790 Ti and 27–55
buildings). That is an **opening-economy collapse, not a tempo loss**. A thrown walker
costs the standoff plant a few rounds; it does not produce zero harvesters and zero
conveyors. See §6 for the ranked replacement suspects.

**Correction to the routing brief:** the cad leg is **n=30**, not 90 (90 is the pooled
3-instrument column). At n=30, 16/30 vs 22/30 is **Fisher two-sided p = 0.18** (vs v77
23/30, p = 0.089) with overlapping Wilson intervals — *statistically* the dip is a lean,
not a fact. The per-map decomposition below is what makes it worth acting on, not the
pooled rate.

---

## 2. CAD LAUNCHER LIFECYCLE — 95 games, 3 eras, zero exceptions

| Match | Era | CAD seat | Opponent | Games | Launcher games | born | died | dmg events | alive after r6 | 2nd launcher | own-builder throws |
|---|---|---|---|--:|--:|---|---|--:|--:|--:|--:|
| `393088af` | v107 | A | OpenSverige v76 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 11 |
| `922b5da8` | v107 | B | OpenSverige v77 | 5 | 4 | r1 | r6 | 0 | 0 | 0 | 10 |
| `9d2b38bb` | v107 | B | OpenSverige v68 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 9 |
| `a7aa49ec` | v107 | B | OpenSverige v66 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 12 |
| `ad2b9a46` | v107 | A | SmartFridge v30 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 13 |
| `b10cce55` | v107 | B | Lunds Stallions v42 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 13 |
| `cdbd5b52` | v107 | B | gsxWins v18 | 5 | 3 | r1 | r6 | 0 | 0 | 0 | 9 |
| `d385731d` | v107 | A | arsonist duck v17 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 11 |
| `27435b40` | v116 | A | OpenSverige v68 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 11 |
| `2876f21d` | v116 | A | OpenSverige v70 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 14 |
| `0803bd92` | v117 | B | OpenSverige v69 | 5 | 4 | r1 | r6 | 0 | 0 | 0 | 12 |
| `0ae5da15` | v117 | B | OpenSverige v75 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 9 |
| `2b05487d` | v117 | B | OpenSverige v72 | 5 | 4 | r1 | r6 | 0 | 0 | 0 | 8 |
| `37e6ccf9` | v117 | B | SmartFridge v33 | 5 | 4 | r1 | r6 | 0 | 0 | 0 | 12 |
| `3e8bd0bf` | v117 | A | OpenSverige v72 | 5 | 4 | r1 | r6 | 0 | 0 | 0 | 9 |
| `8704178a` | v117 | A | OpenSverige v74 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 16 |
| `8d0e02c1` | v117 | A | OpenSverige v75 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 13 |
| `922be463` | v117 | B | Team 48 v16 | 5 | 4 | r1 | r6 | 0 | 0 | 0 | 9 |
| `c6383349` | v117 | B | OpenSverige v72 | 5 | 5 | r1 | r6 | 0 | 0 | 0 | 14 |
| **TOTAL** | **v107/116/117** | — | 12 opponents | **95** | **87** | **r1 × 87** | **r6 × 87** | **0** | **0** | **0** | **215** |

**Every launcher-bearing game, every era: born r1, dead r6, age exactly 5, zero damage
events.** 87/87. This confirms and extends the re-freeze spec's 35/35 (v117-only) to the
full 95-game / 3-era corpus, including the four matches archived since the spec was
written (`393088af`, `d385731d`, `922b5da8`, `0ae5da15`).

**Does CAD ever field a launcher after r6? NO — 0/95.**
**Does CAD ever build a second launcher? NO — 0/95** (max concurrent and max lifetime
count both 1).
**8 games have no launcher at all** — and they cluster exactly where the OS plank lives:
4 of 5 `10×10` games and 3 of 6 `25×15` games (plus one 14×18). Era split: v107 3/40,
v116 0/10, v117 5/45.

**⇒ The fodder window against wild CAD is r1–r5 inclusive, in 87 of 95 games, and does
not exist at all in the other 8.**

---

## 3. ENEMY-BUILDER THROW CENSUS

Detection method per `opponent-recognition-feasibility-2026-08-08.md`: a `MoveBuilderBot`
whose displacement exceeds one tile per round cannot be a walk. **1,472** such events
found in 95 games; each was attributed to the nearest launcher alive that round.

**Pickup-ring calibration (a by-product worth recording):** 1,471 of 1,472 events resolve
to a launcher at **Chebyshev distance exactly 1** — `d²=1` (938) or `d²=2` (533). The
pickup ring is the **full 8-neighbourhood, diagonals included**, not the orthogonal-4.
(The remaining 1 event had no launcher alive; see §7.) The engine's `can_launch` is
compiled, so this is the empirical ground truth.

| Class | Events | Games |
|---|--:|--:|
| Own-team throw by an **OPPONENT** launcher | 620 | — |
| **OPPONENT launcher throwing a CAD builder** (cross-team) | **636** | 45 |
| Own-team throw by a **CAD** launcher | 215 | 87 |
| **CAD launcher throwing an ENEMY builder** | **0** | **0** |

**CAD's own-throw round histogram: r2 ×87, r3 ×57, r4 ×57, r5 ×14. Nothing at r6 or
later, in any era.** Per-game budget: 1 throw (29 games), 2 (1), 3 (44), 4 (13) — the
spec's "≤4 throws" holds at 95 games.

**Cross-team throwing is a real, live ladder mechanism — it is just not CAD's.** Twelve
opponent versions do it to CAD, including **our own line**:

| Thrower | Cross-team throws | Games |
|---|--:|--:|
| OpenSverige v72 | 255 | 12 |
| Powered by SmartFridge v33 | 127 | 3 |
| Lunds Stallions v42 | 61 | 5 |
| OpenSverige v76 | 52 | 5 |
| OpenSverige v68 | 40 | 6 |
| Powered by SmartFridge v30 | 38 | 2 |
| OpenSverige v66 / v75 / v77 / v70 / v69 / v74 | 19 / 16 / 16 / 8 / 3 / 1 | 2 / 5 / 2 / 3 / 2 / 1 |

So the hypothesis' *physics* is sound and the class exists — it simply points at the wrong
opponent. **CAD is one of the ladder bots that does NOT ferry enemy builders.**

---

## 4. THE ONE OPPORTUNITY CAD EVER GOT — and declined

Scanning all 87 CAD-launcher lifetimes for an opposing builder standing anywhere in the
8-ring yields **exactly one event in 95 games**:

> `393088af` game 5 (v107, 28×20, cores (7,9)/(19,9)) — **round 5**.
> CAD launcher `#7 @(10,10)`, born r1, died r6. Our builder `#4` (OpenSverige v76) at
> `(11,9)` — Chebyshev 1, inside the ring, **inside the r1–r5 throw window**.
> **CAD did not throw it.** Our builder survived to r34; the launcher self-destroyed on
> schedule at r6.

The irony is instructive: our builder got there because **our own launcher threw it**
(`#4` teleported `(16,11) → (11,9)` that same round). The only time in the corpus a
builder was ever handed to CAD's launcher on a plate, we handed it over ourselves, and CAD
had no code to pick it up.

n=1 is thin evidence for a behavioural claim on its own. It is decisive **in combination**
with §3's 0/95 and the fact that CAD's ≤4-throw budget is already fully spent on its own
raiders by r5.

---

## 5. WALKER-ARRIVAL GEOMETRY, AND THE PROBE-vs-WILD LAUNCHER DIVERGENCE

### 5.1 Where the OS plank actually arms

`OS_GATE_MODE = "geometry"`, `OS_D_SQ_MAX = 49` (`_v91osb/main.py:1106–1107`), gate
function at `1240–1257`: the map must be in `CORE_PAIRS` **and** D² ≤ 49. Against the live
15-map pool that is **exactly two maps**:

| Map | Dims | Cores | D² | Gate |
|---|---|---|--:|---|
| **fjordgate** | 10×10 | (2,2)/(6,6) | **32** | **ARMED** |
| **meander** | 25×15 | (11,3)/(11,10) | **49** | **ARMED** |
| eider / heart / nordkap | 28×20, 20×26 | — | 144 | off |
| moonrise | 21×8 | (5,3)/(14,3) | 81 | off |
| antler / lighthouse / the rest | — | — | 64–650 | off |

`(16,12,4,5,10,5)` (D²=36) is in `CORE_PAIRS` but has no map file in the pool. **The OS
plank can touch at most 2 of 15 maps = 4 of the 30 leg games (13.3%).**

### 5.2 Does the walker enter CAD's pickup ring?

The walker is `role_n == 0`, the first builder, assigned `saboteur` at `2205–2208` and
exempted from the home-defence recall by `os_hold` at `2589`. Its target is a tile 1–5
along a clear ray onto an enemy Core footprint tile (`2891–2900`, `ranges=(5,4)` for
SENTINEL), reached by BFS (`4809–4899`). **It has no enemy-launcher awareness whatsoever**
— `_plan_siege`'s blocked set is walls + core footprints only (`2861–2864`); `_bfs_direction`
marks a launcher's *own tile* impassable (`4829`) but applies **no adjacency ban, no
pickup-ring ban, no threat penalty**; and the approach tile is never validated against
enemy buildings at all. It also **cannot detect being thrown**: the only displacement
handler is the *friendly* handshake on `SLOT_LAUNCHED_ID` (`2318–2327`), and a teleport
*resets* `self.stuck` to 0 (`2427–2432`) — the opposite of raising a flag. So if a launcher
that grabbed enemy builders existed, the walker would walk back into the ring indefinitely.

Applying that geometry to the archived CAD launcher tiles on the two gate maps:

| Gate map | CAD seat | CAD launcher tile (observed) | OS spot / approach band | Min Chebyshev, walker → launcher | In ring? |
|---|---|---|---|--:|---|
| **meander** (25×15) | B, core (11,10) | `(14,9)` (`0803bd92` g1) | spot (11,5), route x∈[10,12] y∈[4,6] | **3** | **NO** |
| **meander** | A, core (11,3) | `(14,5)` (`ad2b9a46` g5, `8704178a` g1) | spot (11,9), route x∈[10,12] y∈[8,10] | **3** | **NO** |
| **fjordgate** (10×10) | A, core (2,2) | `(5,4)` (`8d0e02c1` g1) | ray spots (5,5)/(4,4); spawn ring (6,5)/(5,6) | **1** | **YES** |

On **meander** the launcher sits on CAD's core ring off the x=11 lane; the walker's entire
route stays ≥3 tiles away in both seats. **Geometrically impossible.**

On **fjordgate** the geometry **does** overlap — the walker's spawn ring tile `(6,5)` and
both leading ray spots `(5,5)`/`(4,4)` are Chebyshev 1 from `(5,4)`, and the walker is
there from ~r2 while the launcher lives r1–r6. **But CAD builds no launcher on 4 of the 5
archived 10×10 games** (spec P10; corroborated here), and in the one game where it did, it
threw only its own raiders. So the wild residual risk is: *behavioural*, not physical —
CAD would have to ship new code, on 20% of fjordgate games, inside a 4-round window whose
throw budget is already spent.

### 5.3 Probe-vs-wild launcher divergence (the check that decides the leg)

| | Wild CAD (95 games) | `cad_probe` (source) |
|---|---|---|
| Launcher born | r1 (87/87) | r1 (`main.py:681–716`, `_run_raider:651`) |
| Launcher destroyed | **r6, self-destruct, 87/87** | **NEVER** — `grep destroy` returns only the docstring at line 6; `SLOT_LAUNCHER_POS` written once (716), never cleared |
| Launchers per game | 1, never rebuilt (0/95 second) | exactly 1, never rebuilt (store slot is the cap; `LAUNCHER_GIVEUP_RND=12`) |
| Throws | ≤4, **all in r2–r5, none after r5** | unbounded, demand-driven, all game (raider seats refilled every `RAID_STALE_RNDS=5`) |
| **Throws ENEMY builders** | **0 / 95 games** | **impossible by construction** — `if ct.get_team(uid) != my_team: return` (1358–1361), plus it only reads `SLOT_THREAT`-style single tile `SLOT_THROW_REQ` written by its own raiders (647), plus `uid in self.launched` one-throw-per-builder |

The divergence is real and worth fixing in the probe (**permanent launcher + unbounded
ferry vs wild's r6 self-destruct and 4-throw cap** — this is spec item **P6**, now
confirmed at 95 games). **But it does not run in the fodder direction:** the probe is
*more* launcher-active than wild CAD and still cannot touch our walker. So this is not
verdict (b) either — the 53.3 is not a fodder artefact of the instrument.

---

## 6. WHAT THE DIP ACTUALLY IS — ranked replacement suspects

Per-map decomposition of the builder's own `sweep_cad_probe.json` (n=30/head, 15 maps ×
1 seed × 2 seat orderings):

| | v75 | v77 | v79 |
|---|--:|--:|--:|
| **GATE maps** (fjordgate + meander, 4 games) | 4/4 | 3/4 | **1/4** |
| **NON-GATE** (13 maps, 26 games) | 19/26 | 19/26 | **15/26** |
| Total | 23/30 | 22/30 | 16/30 |

**The 6-game gap splits ~50/50 across the gate boundary.** The OS plank arms on 13.3% of
the leg; even losing **all four** gate games from a 73%-expected baseline caps its share of
the gap at **2.93 of 6 games (49%)**. *Something non-OS owns the other half*, regardless of
which OS mechanism is at fault.

### Suspect 1 — OS plank starves the fjordgate opening (owns the gate half)

| Game | v75 | v77 | **v79** |
|---|---|---|---|
| fjordgate-a | W 1000r, 10,790 Ti, 55 bld | W 688r, 6,880 Ti, 55 bld | **L 194r, 0 Ti, 0 bld** |
| fjordgate-b | W 817r, 5,650 Ti, 28 bld | W 1000r, 4,510 Ti, 27 bld | **L 305r, 0 Ti, 5 bld** |
| meander-a | W 287r | W 874r | L 416r, 1,720 Ti, 22 bld *(ordinary loss)* |
| meander-b | W 1000r | L 179r | **W** 190r |

**Zero titanium delivered and zero standing buildings in ~200 rounds** is an opening that
never happened — not a walker arriving late. v79 posts **4 zero-economy games, the most of
any of the 9 heads** in the sweep (v75: 0, v77: 3, v53/v54: 0). Candidate mechanisms
inside the plank, all source-visible and all cheap to instrument: the `os_hold`
home-defence exemption (`2589`) leaving our core unanswered on a 10×10 map for r≤40; the
`role_n == 0` seat — a large share of a 10×10 opening — consumed by the standoff walk;
and the OS funding arm raising `ammo_target` to `OS_AMMO_TARGET=24` for r≤120
(`1935–1946`), converting opening titanium away from harvesters. **Meander is NOT part of
this signature** (1/2, ordinary game shapes) — the damage is fjordgate-specific.

### Suspect 2 — a leg-wide, non-map-gated regression in the v77→v79 delta (owns the other half)

v79 = v77 content + `_v90ft` (ferry test) + `_v91osb` (OS). OS is gate-bounded to 4 games
by construction, so **the FT plank is the only candidate that can carry a non-gate deficit
of 4 games across 13 maps**. FT fires `SLOT_UNDER = 2` whenever an enemy builder is
farther than `r+2` manhattan from its core footprint (`ferried()`, `1260`), i.e. on any
opponent ferry — and `cad_probe` ferries its own raiders from r2. Because **no site may
downgrade a 2 to a 1** (`1776–1779`) and a siege opponent keeps `SLOT_ATK_RND` fresh
inside the 50-round latch, one early sighting can pin the whole under-siege response
package on for the rest of the game. Note the comment's claim that "every reader is a
truthiness test" makes 2 ≡ 1 behaviourally — **if that invariant holds, FT's only effect
is earlier latching, and the suspect is the earlier latch, not the value 2. Verifying that
invariant is a one-grep job and should be step 0.**

### Suspect 3 — late core-defence failure at high economy (heart, non-gate)

`heart` is D²=144, gate off, yet v79 lost **both** seats after 922 r / 633 r with
**10,780 / 7,850 Ti** banked — the opposite shape to fjordgate. v75 and v77 won both.
This is a third, distinct failure mode that neither OS nor fodder can explain, and it is
the single largest non-gate contributor.

---

## 7. SELF-CHECKS

| Check | Result |
|---|---|
| Games parsed | **95 / 95** CAD games in `replay_archive` (19 matches, 3 eras) — 0 parse errors |
| `check_delivery()` (core deliveries × 10 == `titaniumCollected`) | **95/95 pass, 0 mismatches** |
| Launcher rows emitted | 95 (87 with a launcher, 8 without) — one row per game, no double-count |
| Displacement events attributed | 1,472; **1,471 (99.93%)** resolve to a Chebyshev-1 launcher — the pickup-ring physics validates the detector |
| Unattributed events | **1** — `8d0e02c1` g5 r241: CAD's own builder `#609` displaced `(14,9) → (10,8)` (cheb 4) with **no launcher alive anywhere on the board** (all launchers die r6). Cause unresolved (likely a decoder edge case, not a throw); 1/1,472 = 0.07%, and it is a CAD-own-builder event either way, so it cannot affect the 0-cross-team-throw finding |
| Seat assignment | stamped from `meta.json` per `bo5-seat-assignment-2026-08-08.md` (meta `teamAName` == engine `TEAM_A`), fixed for the whole Bo5 |
| Spec cross-check | re-freeze spec's launcher claim (35/35 v117, born r1 / dead r6 / 0 dmg) **reproduced independently and extended to 87/87 across v107+v116+v117** |
| Version stamps | v79 = `bots/_v91osb/main.py` **md5 6a909e72**; `cad_probe` **attribution-only**, frozen v107-era; archive as of 2026-08-08, 19 CAD matches / 95 games |

---

## 8. RECOMMENDED NEXT STEP

**Do not commission a det replay-on set for fodder.** There is nothing to confirm: the
probe cannot throw our builder, and wild CAD has not in 95 games. Spending a det battery
here would measure zero.

**Do commission, in this order:**

1. **(free, 5 min) Verify the FT truthiness invariant.** Grep every `SLOT_UNDER` reader in
   `_v91osb/main.py` (25 sites listed in §6) and confirm each is `!= 0` / bare-truthy. If
   any site branches on `== 1` or `== 2`, suspect 2 is promoted to prime and the fix is
   local. If all are truthy, the FT suspect narrows to "earlier latch" and step 3 covers it.
2. **The fjordgate replay-on set — this is the high-value one.** 2 maps × 2 seats × 6 seeds
   = 24 games, `_v91osb` vs `cad_probe`, replays saved, plus the **same 24 with `OS_ON =
   False`** as the paired control (the toggle is byte-exact-identity-verified at
   acceptance, so the control is clean). Maps: **fjordgate and meander only**.
   Instrument, per game: first-harvester round; first-delivery round; builder count at
   r20/r40; the `role_n == 0` seat's position each round r0–r40; `SLOT_UNDER` value each
   round; ammo converted before r40; and the round our core first takes damage. The
   pre-stated discriminator: **if `OS_ON = False` restores fjordgate to a 4,000+ Ti / 27+
   building game shape, suspect 1 is confirmed and the fix is a fjordgate-class carve-out
   of the gate (D² ≤ 49 currently admits both maps; only meander behaves).**
3. **A non-gate FT leg.** `_v90ft` vs its own parent `_v89sh` on the 13 non-gate maps ×
   cad_probe, n ≥ 60, to price the other half of the gap. FT's acceptance measured cad
   60.0-vs-56.7 at n=60 — right direction, so this is a re-measure, not a retraction.
4. **Probe fix (queued, not urgent):** give `cad_probe`'s launcher the wild r6
   self-destruct and the ≤4-throw cap (spec **P6**, now at 95/95 confidence). It will not
   change the fodder answer, but the permanent launcher is a standing lane obstacle wild
   CAD does not have, and it distorts every future gate-map read.

**Also worth banking:** the pickup ring is the **full 8-neighbourhood** (§3, 1,471 events).
Any future "stay out of throw range" logic must use `d² ≤ 2`, not orthogonal adjacency.
And v79's walker has **no thrown-detection at all** (`self.stuck` *resets* on a teleport,
`2427–2432`) — harmless against CAD, but 12 ladder versions including three SmartFridge/
Lunds heads *do* ferry enemy builders (§3). That is a real exposure against a different
opponent class, and it is the one piece of the original hypothesis worth keeping.
