# BUILD REPORT (DRAFT) — `bots/_v516teardown` (teardown + global sentinel accounting + sentinel reach), s51 2026-08-18

*Draft by the opus build agent for the s51 builder; RAW DATA ONLY, the builder types the
verdicts. Parent `bots/_v515ecosalt` FROZEN and re-verified untouched by md5 after every leg
(`scratchpad/s51_v516_build/PARENT_FREEZE.md5`). Master `LOKI_FS_V516`; False reproduces the
parent (structurally audited + behaviourally measured). Diff vs parent: doctrine +171, main
+103/−5, siege +271/−8, raid +29/−2, eco untouched. **0 tracebacks, 0 timeouts, 0 no-winners
in every leg.** Artifacts: `scratchpad/s51_v516_build/` (arms, mech/, grid/, gated/, fo/,
five self-tested instruments, the get_hp probe tree and its tape).*

---

## ⛔⛔ FINDING 0 — CHANGE 1'S PREMISE IS REFUTED BY THE AUTOPSY'S OWN REPLAYS

The mandate (and `AUTOPSY-rush-top3-2026-08-18.md` §SHARED ROOT) reads: *"295 launchers/30
games stand forever after ONE throw (224 HOPBUILD vs 217 THROW) … the fired config has ONE
rider, the both-riders condition never satisfies, teardown never fires."*

Re-measured on the **same 30 replays**, joining the replay entity ledger to the bot's own
HOPBUILD log by tile **and build round** (`launcher_census.py`, `scale_decomp.py`):

| | measured |
|---|---|
| HOPBUILD events | 224 |
| …that **tore down inside 20 rounds** (median life **1 round**) | **219 / 224** |
| launchers with life ≥ 20 | 71 |
| …of those, built by `_fs_build_ferry` | **5** |
| …**never built by the ferry at all** | **66** (14 ring EVICTORS, 52 chassis) |

**THE RELAY TEARDOWN FIRES 219 TIMES IN 224.** In the fired configuration
`relay = … and LOKI_FS_CREW and FS_CREW_ON` (`_v515ecosalt/siege.py:3074-3075`) is **False**,
so `hold` at `:3180` is False and the launcher calls `self_destruct()` on the throw round.
The both-riders condition not satisfying is exactly what makes it tear down.

**WHAT ACTUALLY STANDS, and it is a different mechanism in the same function:**
`_v515ecosalt/siege.py:3196` — `if not self.fs_ferry_seen: return False` — sits **above** the
TTL teardown at `:3202-3206`. `fs_ferry_seen` is set only when a published rider is under the
launcher's hand (`:3104`). So **the ferry TTL is unreachable for every launcher that never had
a rider adjacent**: a hop link whose rider died before riding, and every chassis home-doctrine
launcher (`main.py` LOKI-42) that a roaming builder planted forward. Two games in the autopsy
grid reach **16 and 22 live launchers**.

**AND THE SCALE ARITHMETIC DOES NOT SURVIVE EITHER.** The autopsy's "+0.98 scale/game …
prices the sentinel at 124" is *launchers built × 10%*, which ignores that destruction refunds
the contribution. Live-scale decomposition at the round the first forward sentinel is bought
(n=24 of 30 games):

| | median | mean |
|---|---|---|
| live scale | **288%** | — |
| implied sentinel price | **86 Ti** (not 124) | 90.5 |
| **live BUILDER BOTS** | 100 pp | 92.4 pp |
| **live LAUNCHERS** | 10 pp | 7.4 pp |

**Launchers are ~4% of the 188 pp of excess scale at the moment that prices the sentinel;
LIVE BUILDER BOTS are ~50%.** Launchers only dominate at END of game (mean 14.8 pp, carried
by a 2-game tail at 160 and 220 pp).

⇒ **Change 1 shipped in two parts** rather than being dropped: (a) the relay hold generalised
off `FS_CREW_ON` — correct semantics, and honestly a behavioural no-op in the fired config;
(b) an **IDLE-FORWARD teardown** aimed at the population that is actually standing. Part (b)
is the one with a measurable target and it is the one that moved.

---

## ⛔ FINDING 1 — ENGINE FACT, NOVEL, AND IT FORBIDS THE MANDATE'S CHANGE-2 DESIGN

The spec was *"the Core can verify liveness each round via `get_hp(id)` … CHECK on the engine
with a 2-minute probe game before relying on it."* Probe run
(`scratchpad/s51_v516_build/probe_gethp/`, one nordkap game, 478 live probes + 434 dead-id
controls, **positive control in the same tape**):

```
r2    rid 3  dsq 4   invision 1  hp 40    exc ''                    <- POSITIVE
r3+   rid 3  dsq -1  invision -1 hp None  exc POS:GameError|HP:GameError
```
* **471 of 471** out-of-vision probes raised `GameError` on BOTH `get_hp(id)` and
  `get_position(id)`.
* **434 of 434** probes on a **destroyed** id raised identically.

⇒ **`get_hp(id)` AND `get_position(id)` RAISE `GameError` FOR ANY ENTITY OUTSIDE THE CALLER'S
VISION, AND THE ERROR IS INDISTINGUISHABLE FROM THE ONE A DESTROYED ID GIVES. THERE IS NO
ID-BASED LIVENESS CHANNEL IN THIS ENGINE.** This re-prices every "publish the id and let
someone else check it" design in the backlog, not just this one.

**THE SUBSTITUTE, and it is better than the spec's fallback:** a turret is a UNIT, so `run()`
is called for it every round it lives and stops the round it dies — **the sentinel is its own
heartbeat**. It writes the current round into a beat field; the Core and the raider read the
beat's AGE. No TTL guesswork, no staleness window beyond the store's one-round buffer.

**⛔ A BEAT, NOT A COUNT — the one-writer rule is why.** Two sentinels writing one buffered
slot in one round is a lost update (the probe's r197 class). **A beat is collision-safe
because both writers write the IDENTICAL value.** A count is not. The beat therefore answers
"≥ 1 live forward sentinel" exactly, says nothing about 2, and **deliberately cannot inflate
the purchase cap** (`>= FS_SENTINEL_MAX`). Field: `SLOT_ROLE_N` high bits (slot 0 has exactly
one reader and one writer in the whole tree, both on the builder's first-turn role claim);
bits 0-9 keep the counter, bits 10-20 carry round+1, and both writers preserve the other's
field.

---

## HEADLINE — 5 siege maps, 15 blocks × 30, n=450/arm, arms CONCURRENT per block, vs `_v488beltbreak2`

| | **v516 FIRED** | **v515 PARENT (concurrent, same blocks)** |
|---|---|---|
| WINS | **255/450 (56.7% ±4.6)** | 239/450 (53.1% ±4.6) |
| **kills ≤ r300 (ITT primary)** | **132/450 (29.3% ±4.2)** | 136/450 (30.2% ±4.2) |
| our core destroyed | **166** | 180 |
| r1000 games | **67** | 81 |
| median kill round | 236 | **213** |
| tracebacks / timeouts / no-winners | **0 / 0 / 0** | 0 / 0 / 0 |

**Δwins +3.6 pp — INSIDE the interval** (two-sample naive half-width ≈ 6.5 pp; and see the
one-draw law below, which makes even that optimistic). **Δk≤300 −0.9 pp — INSIDE, i.e. the
`DEFENCE_ADMISSION_BAR` timely-kill primary does not fall measurably, but it does not rise
either.** Intervals are NAIVE and local: the s39 audit measured local pair-weighted
DEFF = 0.98, so the platform constants (1.53 / 1.83) do **not** apply and are not used.

**⭐ THE OUTCOME MIX MOVED MORE THAN THE WIN RATE DID, AND IT MOVED IN TWO DIRECTIONS AT ONCE:**

| kill round | v516 | v515 |
|---|---|---|
| ≤ 200 | 84 | 83 |
| 201–300 | 48 | 53 |
| **301–500** | **57** | **29** |
| > 500 | 28 | 24 |
| **total core kills** | **217** | 189 |
| wins taken on the r1000 tiebreak | **38** | 50 |

**v516 converts 28 more games into core kills and 12 fewer into tiebreak wins — and almost
every extra kill lands AFTER r300.** r1000 stalls fall 81 → 67. Under `R1000_IS_DEFEAT` that
is the right direction (a tiebreak win is scored as a defeat); under the r300 bar it is not a
gain. Mechanically this is what change 2 predicts: a magazine that stays armed while the
raider is dead keeps a starved grind alive until it lands, instead of running out the clock.
**Median kill 236 vs 213 is drift inside the reported-not-disqualifying band per the s45
re-pricing, and the bar itself (timely-kill RATE) is not cleared in either direction.**

**PER MAP** (wins/90, k≤300 in brackets):

| map | v516 | v515 parent |
|---|---|---|
| **midgard** | **21/90 (k 7)** | 13/90 (k10) |
| **nordkap** | **55/90 (k23)** | 46/90 (k28) |
| glacierkeep | 80/90 (k50) | 77/90 (k46) |
| atoll | 39/90 (k13) | 38/90 (k18) |
| drakkarfjord | 60/90 (k39) | **65/90 (k34)** |

**PER BLOCK (wins/30), v516 / parent:** 15/18 · 16/17 · 21/16 · 16/15 · 18/16 · 16/16 ·
18/15 · 13/21 · 18/16 · 19/14 · 16/13 · 16/20 · 15/12 · 16/17 · 22/13.
**v516 leads in 10 of 15 blocks and the per-block spread is ±5 games on a mean of 16** —
the v515 one-draw law (±3-5 per 30-block) in one column. **No n=30 or n=90 cut of this table
is a conclusion.**

---

## PER-CHANGE VERIFICATION (every mutant driven, zero-vs-nonzero)

### 1 — TEARDOWN (`FS_V516_TEARDOWN`; sub-flags `FS_V516_HOLD_GENERAL`, `FS_V516_IDLE_ON`, `FS_V516_FERRY_READSITE`)

**Instrument, both ways:** `IDLETEAR516` stderr events — **29 events in 6 of 60 games** across
the two IDLE-ON mech arms, **0 events in 0 of 30 games** in the `FS_V516_IDLE_ON = False`
mutant. Zero-vs-nonzero. ✅

**Currency — the targeted population's LIFE, which is the mechanism and is immune to how many
launchers a draw produces.** In-scope = off-ring, beyond the home keep-out, life ≥ 40:

| arm | in-scope launchers | **mean life (rounds)** |
|---|---|---|
| IDLE ON (`m1_fired`) | 5 | **81** |
| IDLE ON (`m1_holdoff`) | 30 | **129** |
| IDLE OFF mutant (`m1_off`) | 3 | **585** |
| flag-off tree (v516 with the master off) | 43 | **375** |

**An idle forward launcher lives 3–7× shorter.** And the end-of-game scale share follows:
**launcher pp at game end, mean 7.6 (IDLE ON, n=180) vs 14.8 (parent v515, n=60) and 15.8
(flag-off, n=60) — roughly halved.**

**⚠ AND THE SENTINEL PRICE DOES NOT MOVE, WHICH IS FINDING 0 ARRIVING AS A MEASUREMENT.**
Sentinel price at the first forward purchase: mean **88.7 Ti** (IDLE ON, n=142 purchases)
against **90.5** (parent) and **93.5** (flag-off). −1.8 Ti. The autopsy's ~124 is not
reproduced by any arm; live builder bots are the price.

**⚠ NAMED REGRESSION WATCH (the mandate's): the ring evictors.** They are excluded **by
construction** — `_fs_launcher_turn` routes any launcher inside `FS_RING_DSQ` to the eviction
branch and returns before the ferry path, so the idle teardown can never see one. Measured:
ring-sited launchers per game are flat across arms (35/171 fired vs 40/199 mutant vs 76/549
flag-off, i.e. 1.2–1.3 per game everywhere).

**⚠ SURPRISE (unpredicted, written down before explaining): TEARING A FORWARD LAUNCHER DOWN
CAN TRIGGER A REBUILD.** The chassis releases `SLOT_LAUNCHER` when the Core can no longer SEE
a launcher (`main.py:1403`, LOKI6_LAUNCHER_RELEASE FIX 3), and a forward launcher is never in
the Core's r²=36 vision — so a torn-down forward launcher can be immediately re-bought by a
roaming builder. Visible in one game of the first draw (`atoll_s2_A`, 40 pp of launcher scale
at end, **more than any mutant game**). Pooled it does not dominate — launchers built per game
5.7–9.9 across arms, inside the draw spread — but it is the failure mode to watch if
`FS_V516_IDLE_TTL` is ever shortened.

**Sub-flag `FS_V516_HOLD_GENERAL` is NOT the no-op it looks like.** Predicted inert in the
fired config (one rider, thrown ⇒ `any()` False ⇒ same teardown). Measured: the
`HOLD_GENERAL = False` arm produced **25 IDLETEAR events in 5 games against 4 in 1** for the
fired arm on the same seeds, i.e. the two differ. The reachable difference is a link whose
published rider id CHANGES between rounds (raider replacement): the general form then holds
the link open up to `FS_RELAY_TTL` where the parent form tears down at once. Reported, not
resolved — n=30 one-draw.

**`FERRY_HOME_ON` read-site move (change 1c).** The AST scan (below) confirms the module-level
derived default at `doctrine.py:3011` is still the ONLY instance in the tree and is now unread
on the live path: `raid.py` calls `_ferry_home_on()`, which reads both flags at RUN time. The
constant deliberately keeps the parent's value so that reading it still reports what v515
shipped.

### 2 — GLOBALSENT (`FS_V516_GLOBALSENT`) — **the change that moved**

**Instrument, both ways:** `SENTBEAT` — **3,543 beats in 24 of 30 games** fired, **0 in 0** in
the `FS_V516_GLOBALSENT = False` mutant. ✅

**Currency — ammunition under a live core-hitting sentinel of ours**, decoded replay-side
(`magtrace.py`, 4-case guard driven both ways incl. the never-fired branch returning −1 not
0). Baselines the mutant must reproduce come from the autopsy: armed 21.2%, ammo < 10 in
78.3%.

| arm | games | siege rounds | **ammo ≥ 10** | **ammo ≥ 120** (`FS_AMMO_KILL_MIN`) | median ammo |
|---|---|---|---|---|---|
| **GLOBALSENT ON** (6 mech arms pooled) | 180 | 26,647 | **0.421** | **0.227** | 53 |
| GLOBALSENT OFF mutant (`m2_off`) | 30 | 5,796 | 0.249 | 0.014 | 8.5 |
| flag-off tree | 60 | 7,212 | 0.282 | 0.007 | 30 |
| parent v515 as-is | 60 | 10,128 | 0.291 | 0.018 | 25 |

**The mutant reproduces the autopsy's 21.2% armed / 78.3% starved digits** (0.249 / 0.751) and
the parent independently lands at 0.291. Fired: **+13 to +17 pp on armed share and a 12–32×
lift on the kill-window threshold.** Isolated single-arm read (`m2_fired` alone, n=30): 0.527
armed, 0.363 at ≥120, median ammo 92.

*(The Core-side reserve moves with the magazine in the same change: arming while leaving
`ti_floor` at the collar price is the `midgard_s1_A` exemplar exactly — bank pinned at 80 Ti,
ammo 4, a sentinel firing — so `_v516_kill` relaxes the floor on the same beat.)*

### 3 — SENTREACH (`FS_V516_SENTREACH`)

**Instrument, both ways:** `SREACH516` — **82 scans in 27 of 30 games** fired, **0 in 0** in
the mutant. ✅ The scan runs, finds sites, and the walker preference is applied.

**Currency — forward-sentinel purchase rate (a sentinel built within d²≤40 of the enemy core,
read off the replay, not off our own log):**

| arm | games | bought a forward sentinel |
|---|---|---|
| SENTREACH ON (6 arms pooled) | 180 | 144 (**80.0%**) |
| SENTREACH OFF mutant (`m3_off`) | 30 | 23 (**76.7%**) |
| flag-off tree | 60 | 43 (71.7%) |
| parent v515 as-is | 60 | 50 (**83.3%**) |

**NULL, and honestly so.** The mutant reproduces the autopsy's 23/30 exactly, but **the parent
itself reads 83.3%** — above the fired arm. Nothing here separates. Single-arm reads range
66.7%–83.3% across arms that share the flag, which is the one-draw law in one column.
The mechanism is live; its purchase-side effect is not measurable at this power.

---

## FLAG-OFF AUDIT

**Structural.** Every behavioural site is guarded by `LOKI_FS_V516 and FS_V516_<sub>` read at
RUN time (26 guarded sites; the only unguarded additions are the `fs516_*` state fields, which
are written but read only under a guard, and the `SLOT_ROLE_N` mask, a no-op while nothing
writes the high bits).

**NO NEW DERIVED DEFAULTS** — `flagoff_ast.py`, module-level assignments and module-level
conditionals whose RHS/test reads a v516 flag:
```
GUARD: pos=True neg=False if=True            <- three synthetic controls, driven both ways
v516 derived defaults: 0 []
REAL-CASE CONTROL (FS_CREW_ON readers): 2 [(3011,'FERRY_HOME_ON','LOKI_FS_CREW'),
                                           (3011,'FERRY_HOME_ON','FS_CREW_ON')]
RESULT: PASS
```
⛔ **The real-case control is what makes the zero meaningful** — the scanner is proved able to
see the known v515 hazard in this very file before its zero for v516 is believed.

**Behavioural.** Both arms, n=180 each, interleaved blocks on fresh seeds, `_v488beltbreak2`:

| | flag-off (`LOKI_FS_V516 = False`) | parent v515 as-is |
|---|---|---|
| wins | 103/180 (57.2%) | 101/180 (56.1%) |
| kills / k≤300 | 80 / 49 | 77 / 52 |
| our core destroyed | 64 | 68 |
| r1000 | 36 | 35 |
| median kill | 252 | 226 |
| tracebacks | 0 | 0 |

**Δ +1.1 pp.** ⚠ The first n=60 read was 34/60 vs 40/60 with the entire gap on atoll (2/12 vs
7/12) — bought out rather than argued away, and it was the draw.

**AND THE CHANNEL-LEVEL IDENTITY IS THE STRONGER EVIDENCE**, because it is the exact quantity
change 2 moves: ammo ≥ 10 under a live core-hitting sentinel reads **0.282 (flag-off) vs 0.291
(parent)** and ammo ≥ 120 reads **0.007 vs 0.018**, against **0.421 / 0.227** with the plank
on. The flag-off tree sits with the parent on the very column the plank is loudest in.

---

## GATED CONTROL — archipelago vs `_v468kladturbo`

archipelago's board signature `(26, 26, (5, 5), (19, 19))` is in `FS_MAP_SKIP`, so `_fs_gate`
refuses and **all three changes are structurally unreachable** — change 1 returns before
`fs_born` is even set, change 3 lives inside the siege walker, and change 2's beat is gated on
the same predicate (`_fs_map_gated`) precisely so this stays true.

| draw | v516 | flag-off tree | parent v515 |
|---|---|---|---|
| seeds 1-18 | 22/36 | **17/36** | 29/36 |
| seeds 19-36 | 30/36 | 22/36 | 27/36 |
| **pooled n=72** | **52/72 (72.2%)** | **39/72 (54.2%)** | 56/72 (77.8%) |

⚠ **THE FIRST DRAW ALONE READ 22/36 AGAINST THE PARENT'S 29/36 AND WOULD HAVE BEEN REPORTED AS
AN ALARM.** The control that settles it is the FLAG-OFF arm, which cannot differ from the
parent on this board and read **17/36 — five games below v516 and twelve below the parent.**
⇒ **the movement is the draw, not a leak.** v516 pooled lands on the v515 bar (72.2% vs the
26/36 = 72.2% the parent measured in its own report).
**AND THE SIZE OF THE SPREAD IS ITSELF THE FINDING: 36-game same-config swings of 22→30
(v516) and 17→22 (flag-off).** A 36-game gated read is not a control; two of them barely are.

---

## DEVIATIONS FROM THE MANDATE (each with its reason)

1. **Change 1 retargeted** — the mandate's premise ("teardown never fires single-rider") is
   refuted by measurement (finding 0). The generalised hold shipped as specified *and* is a
   no-op in the fired config; the behavioural work is done by the idle-forward teardown, which
   the mandate did not name because the autopsy had mis-attributed the standing population.
2. **Change 2's liveness channel is a beat, not id+`get_hp`** — forbidden by the engine
   (finding 1), probed before building exactly as instructed. The mandate's own fallback
   ("publish-at-build + assume-alive-with-TTL") was **not** used either: the sentinel's own
   per-round `run()` is a strictly better channel with no staleness window to document.
3. **Change 2 is map-gated.** The beat is written only where `_fs_map_gated` says the
   ferry-siege runs, so gated boards cannot start arming the siege magazine. This required
   factoring the gate out of `_fs_gate` as a pure function — because filling in `self.core` on
   a turret (which `_fs_gate` needs) would silently re-open `_door_turret_turn`, which returns
   early **on that null**.
4. **Mechanism arms are n=30, not ~15** — `run_grid` emits 5 maps × 3 seeds × 2 seats and the
   extra 15 games are free (a local game is ~2 s).
5. **The whole battery was re-run from scratch** after a mid-build correction to change 2's
   gating; the first draw is discarded and not reported. Tree md5s are frozen in
   `TREE_FINAL.md5` and every arm was rebuilt from them.

## SURPRISES (written down before being explained away)

1. **v516 kills 28 MORE cores and 12 fewer tiebreak wins, and the extra kills are LATE
   (301-500: 57 vs 29).** Nobody pre-registered this shape. The plausible mechanism is change
   2 — a magazine that stays armed while the raider is dead sustains a starved grind until it
   lands rather than running the clock out — but that is a story fitted after the fact and the
   report does not treat it as established. **It is also the one result that pulls the two
   standing directives apart: `R1000_IS_DEFEAT` says converting stalls into kills is the right
   direction; `DEFENCE_ADMISSION_BAR`'s r300 primary does not pay for a kill at r420.**
2. **`FS_V516_HOLD_GENERAL` is not the no-op it was predicted to be** (change 1, above).
3. **Tearing down a forward launcher can trigger a rebuild** through the Core's
   `SLOT_LAUNCHER` release (change 1, above).
4. **The flag-off arm read 17/36 on archipelago, five games BELOW v516 and twelve below the
   parent, on a board where it is provably the parent.** A 36-game gated read carries a
   same-config swing that a single draw cannot see past.

## OPEN ITEMS

1. **The chassis home-launcher path is the real launcher line item, and v516 only trims it.**
   66 of 71 standing launchers per 30 games are `main.py`'s LOKI-42 buy, re-armed by the
   `SLOT_LAUNCHER` release whenever the Core cannot see one. The idle teardown deletes them
   after 40 rounds; it does not stop them being bought. **The purchase-side fix is a v517
   candidate and it collides with s30's measured "removing home defence is a REAL NEGATIVE" —
   flagged, not resolved.**
2. **`FS_V516_HOLD_GENERAL` is not inert** (above). Needs a powered arm or a targeted
   rider-replacement fixture.
3. **Change 3 is unmeasured, not falsified.** The scan finds sites in 27/30 games; whether the
   walker ever *reaches* them is the untested link (v515's evictor reach failed on exactly
   this: the purchase happened before any station was worth standing on).
4. **The sentinel is priced by LIVE BUILDER BOTS, not by launchers** (finding 0). ~90-95 pp of
   ~186 pp of excess scale. Nothing in v516 touches it; it is the largest unexploited lever
   the decomposition names.
5. Inherited and untouched: magazine/phase gap for FLOOR-PATH turrets on belted maps,
   evictor purchase timing, `FS_SENT_RND_FLOOR` unswept, subadditivity unattributed,
   self-play fixture caveat, platform CPU test, `_wire_tick`, `FS_CREW_CONVERT`.

## ARTIFACTS

`scratchpad/s51_v516_build/` — `arms/` (8 mutant/flag arms + a frozen parent copy),
`mech/` (9 arms × replays + logs + per-arm launcher/mag/scale tapes), `grid/` (headline
blocks), `gated/`, `fo/`, `probe_gethp/` (the get_hp probe tree and `probe.err`),
`launcher_census.py`, `scale_decomp.py`, `magtrace.py` (guarded), `flagoff_ast.py` (guarded),
`summarise.py` (self-tested), `mkarm.sh`, four drivers, `PARENT_FREEZE.md5`, `TREE_FINAL.md5`,
`PIDS`.

---
## BUILDER VERDICT LINES (s51, typed by the lane)
* v516 FIRED: **56.7% [52.1-61.3] n=450 vs incumbent — numerically the line's best powered
  read** (v515 53.2, parent-concurrent 53.1); delta vs parent inside interval, but the OUTCOME
  MIX is programme-positive: +28 core kills, −14 r1000 games, the added kills landing r301-500.
* GLOBALSENT is the paying change (funding under a firing turret 0.249→0.421, ammo≥120 12-32×)
  — the autopsy's #1 mechanism confirmed and fixed. TEARDOWN: real-but-small (launcher scale
  share halved; sentinel-price effect null — the autopsy's shared-root SIZING was wrong, see
  the correction note on that doc). SENTREACH: mechanism live, currency null.
* DOCTRINE TENSION FOR MAGNUS, flagged not resolved: v516's gain is late kills (r301-500) —
  R1000_IS_DEFEAT values them, the r300 bar does not pay them; and the v517 home-launcher
  purchase fix collides with s30's home-defence-is-real-negative measurement.
* Engine fact routed to atlas at wrap: get_hp/get_position RAISE for out-of-vision ids,
  indistinguishable from destroyed — no id-based liveness channel exists.
