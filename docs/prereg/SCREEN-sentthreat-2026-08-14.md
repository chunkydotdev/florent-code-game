# SCREEN PREREG — SENTTHREAT: the raid-station scorer models the enemy SENTINEL as a threat, not only as a target (QUEUE #30)

**STATUS: committed BEFORE the `SENTTHREAT` shard's first row exists, and before
the treatment tree exists at all** (two-clock: this file's git author time vs the
first `SENTTHREAT` row's timestamp in `scratchpad/overnight/SENTTHREAT.tsv` /
`scratchpad/corefill.log`; the side lane certifies the pair). No row of this
shard exists at commit time and none may be read before it does. Drafted
**2026-08-14T21:06:29Z** (`date -u`, same shell call), repo at `81f11e7a`.

**PROVENANCE: docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md · QUEUE.md (row #30, and the two FIRE ORDER blocks at :39-71 and :73-115) · docs/coordination.md (:39058-39067 the grep finding · :39540-39605 D45 · :39606-39645 the side-lane re-sizing · :39647-39680 the GUNAX0 decoupling · :40355-40380 the "gated behind #33" item · :44265-44280 the GUNAXIS0 gate decision that RELEASES that gate · :49510-49535 the s39 sweep relay · :49125-49140 the v140 per-game build fingerprint) · docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md (row 30 cell at :117, LIST 1 item 6 at :163, the release table at :129) · docs/research/COMBO-MINING-sweep-2026-08-13.md (:21-35, :98-99) · bots/_v223sealrepair/raid.py:614-616,726-823 · bots/_v223sealrepair/doctrine.py:1286-1290,1531-1533 · bots/_v188sentsafe_g/raid.py:421-460 · bots/_v188sentsafe_g/doctrine.py:1522-1605 · tools/overnight.sh:42,68,121-155 · tools/prereg_check.py · docs/prereg/SCREEN-sealfloor6-2026-08-14.md (structure only) · scratchpad/corefill_work.txt (seedbase collision check) · HANDOVER.md:1-40**

Drafted by a FRESH agent with **no inherited session context** beyond the brief
recorded in §1. Every file above was opened read-only. **No shard row of any
kind was read; no game was run; no tree under `bots/` was created or edited by
this agent; nothing was committed.**

---

## 0. ⛔ READ THIS BEFORE RATIFYING — THIS ROW HAS A LIVE KILL RECOMMENDATION AGAINST IT

Three dated facts, in the order they happened, because the row's own prose in
`QUEUE.md` is stale in **both** directions:

1. **THE BLOCK IS RELEASED, and `QUEUE.md` was never annotated.**
   `QUEUE.md:102` still reads *"`#30` … **Both gated behind `#33`**"*. That gate
   was **discharged 2026-08-13T20:22:47Z** — `docs/coordination.md:44270-44279`,
   builder s37 gate decision: `GUNAXIS0` dropped at GATE-2700, n=2733,
   **49.51 ±1.87**, *"the `LOKI_GUNAXIS_PENALTY` flag STAYS … **`#30`/`#31a` stop
   being gated on it**."* Re-confirmed 2026-08-14 by the economics sweep
   (`QUEUE-ECONOMICS-SWEEP-2026-08-14.md:129`, *"RELEASE the `#30` / `#31a` gate
   — they are no longer blocked"*). **The blocked language in the FIRE ORDER
   block does not bind.**
2. **AND THE SAME SWEEP PROPOSES KILLING THE ROW.**
   `QUEUE-ECONOMICS-SWEEP-2026-08-14.md:117` prices `#30` at **0.32 forward
   builder deaths/game addressable (ceiling 0.63) ≈ 25 Ti/game ≈ 0.6% of our
   ~4,077 Ti/game collected**, cites the nearest built arm at **49.83 ±1.33 @
   n=5408**, and labels it **KILL-CANDIDATE by arithmetic** (LIST 1, item 6 at
   `:163`). Its frame (`:30-40`) is *"can this plausibly reach +2pp POOLED"*.
3. **THAT PROPOSAL IS NOT A RULING.** The sweep's own header (`:7-10`) reads
   *"THESE ARE RECOMMENDATIONS TO RESEARCH, WHO OWNS THE QUEUE. I decide
   nothing."* **Research has taken no action on `#30`**; the row is unannotated
   and `queue_check` still counts it unblocked.

⇒ **THE RATIFYING LANE HAS TWO LEGITIMATE ACTIONS AND THIS DOCUMENT IS BUILT TO
SERVE BOTH:** kill the row on the sweep's arithmetic (§9 states exactly what is
lost), or fire the **§8 DOSE GATE first** — a ~150-game probe that costs ~3% of
this screen and can close the row for good. **Firing the 5400-game screen
without the dose gate is the one action this document argues against.**

---

## 1. THE BRIEF, RECORDED AS HANDED (not re-derived)

The task specified: item `QUEUE.md` **#30**, plank name **`sentthreat`**,
LOCAL corefill fixture, treatment vs control `bots/_v223sealrepair` (v140, LIVE
incumbent), 15-map pool, **local DEFF = 0.98** with the platform constants
(1.529/1.833) explicitly NOT to be imported, half-widths ±1.33pp at n=5400 /
±1.89 at 2700 / ±3.10 at 1000, rows kept on cancel, `cut_short_floor` ≤
`planned_n`, one row = one game. The game facts about sentinel vs gunner
asymmetry in the brief were **independently re-verified against `CLAUDE.md`'s
entity table** before use.

---

## 2. REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen, ZERO live rated exposure; no submit, no activation, no prototype on the ladder, so `tools/target_value.py`'s reachable-band gate does not bind.**
**PINNED: N/A — local screen. The control is a byte-frozen local tree (`bots/_v223sealrepair`), so opponent churn cannot reach this shard; the pin / never-pin design rule governs PLATFORM legs only.**
**SURFACE: local**
**CLUSTER UNIT: none — enumeration performed in §4; both clusters die, applicable DEFF = 0.98 (local, measured, s39 audit)**
**ESTIMATOR: pooled game share = treatment wins / (rows − NOWINNER rows), unweighted, over `SENTTHREAT.tsv` rows only. No map weighting, no seat weighting, no pooling with any other shard and specifically NOT with `SENTSAFE`/`SENTSAFE2`, which are a different call site (§3).**
**TREATMENT TREE: bots/_v240sentthreat — PROPOSED NAME, NOT YET BUILT. This agent is forbidden to write under `bots/`; the builder builds the tree from the one-hunk diff in §3 and re-runs this check with `--fire` once it is `git add -N`'d.**
**PLANNED n: 5400 games**
**BOUNDARY: 5400 shard rows = 5400 games (LOCAL fixture: 1 row = 1 game; the platform `games = 5 × accepts` identity has no accepts to close on here — declared exemption in §11)**
**CUT-SHORT: below n=1000 this shard publishes descriptive tallies only and takes NO comparative look; a futility drop at either gate publishes the label, the n and the share and makes NO claim about the mechanism beyond "not worth more cores now"**
**BAR: 51.33**
**BASE RATE: 50.0**
**BAR SOURCE: OB-F final band upper edge at n=5400 (= the 95% half-width, ±1.33pp, DEFF 0.98), the standing corefill screen band; identical construction to `SCREEN-sealfloor6-2026-08-14.md` and `SCREEN-sealsweep-2026-08-14.md`**
**BASE RATE SOURCE: structural null of a paired local screen — `tools/overnight.sh:125-136` plays every (seed, map) in BOTH seat orders (`ORD` A and B), so under H0 the expected treatment share is exactly 50.0. No historical population is consumed by the bar.**
**REFERENCE n: none — `SENTSAFE2`'s 49.83 @5408 is cited as a DIRECTION PRIOR and as a dose anchor only (§3, §6, §8) and is a comparator in no bar on this page**
**MECHANISM METRIC READS: raid.py:768 (the enemy-turret type dispatch that fills `gun_axis`), consumed at raid.py:815-816. TREATMENT DIFF TOUCHES: raid.py (sole hunk, lines 753-776). INTERSECTION: YES — same file, same hunk; the metric IS the diffed branch.**
**TREATMENT DIFF REFS: HEAD -- bots/**
**DOSE: enemy turret classes fed into the station-avoidance set `gun_axis` — treatment 2 classes (GUNNER + SENTINEL) vs control 1 class (GUNNER only), single call site, single hunk, both trees inspected; n = 1 diff hunk. ⛔ THE BEHAVIOURAL DOSE (redirected station choices per game) IS NOT PRE-MEASURED and is GATED by the ~150-game probe in §8, whose fire floor is 2.0 redirects/game against the 0.073 our nearest arm measured.**
**GATE RESOLUTION: §6 — the band discriminates a true effect ≥ ~1.9pp at 80% power; UNRESOLVED (final inside 48.67–51.33) defaults to the RESTRICTION — the shipped gunner-only scan stays, the arm is not promoted, and per §9 the row then closes rather than re-running.**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock. Verified at the primary this session: `bots/_v223sealrepair/raid.py:768` tests `== EntityType.GUNNER` and nothing else; `get_attackable_tiles_from` has EXACTLY ONE call site in the whole tree (`raid.py:772`, gunner-typed); no `SENTINEL` branch exists anywhere in `_raid_station`; `LOKI_SENTSAFE_*` is absent from v140's `doctrine.py`. There is no cell here that is pre-satisfied.**
**MAP SEGMENT: the 5 900-area maps — drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie — versus the 10 ≤676-area maps (antler, archipelago, auroraveil, drumlin, fjordgate, frostgate, icefloe, nordkap, royale, yulerune). MECHANISM: the penalty can only fire on a station-round actually spent inside an enemy sentinel's ray, so its dose is (enemy forward sentinels standing) × (our station-rounds near their core). Both terms grow with siege duration, and siege duration grows with approach length; area is the available proxy for approach length.**
**EXPECTED DIRECTION: POSITIVE on-segment, ~ZERO off-segment — treatment share ABOVE 50 on the 5 900-area maps and ≈50 on the 10 ≤676-area maps.**
**SEGMENT VALUE CEILING: 33.3% x 4.0pp on-segment = 1.33pp pooled**
**POOL ERA: post-2026-08-13-rotation — the local 15-map pool `maps/*.map26` as read by `tools/overnight.sh:68`, post-patch geometry (valkyrie and glacierkeep grids rewritten 2026-08-14 by MAPFIX/v139; the other 13 unchanged). No number on this page comes from the rated tape, so the ladder pool boundary bounds nothing here.**

### ⛔ THE CEILING IS AN ADMISSION, NOT A FORECAST

**1.33pp pooled is EXACTLY this screen's 95% half-width.** That is deliberate:
it is the largest pooled effect this document is willing to put its name to, and
it sits precisely at the point where the screen stops being able to tell the
effect from noise. **It is an upper bound and the economics sweep argues the true
value is well below it** — 0.32 forward builder deaths/game ≈ 25 Ti/game ≈ 0.6%
of our own economy (`QUEUE-ECONOMICS-SWEEP-2026-08-14.md:117`).

⚠ **THE CONVERSION FROM "BUILDER DEATHS PREVENTED" TO "GAME SHARE" HAS NEVER
BEEN MADE IN THIS REPO AND IS NOT MADE HERE.** The row's own record says so
twice (`docs/coordination.md:39733-39739`, D46's rider): *"a forward builder
death may COST more now than it did then … that is a VALUE case, not a COUNT
case, and it needs its own number before `#30` leans on it."* **This document
does not smuggle that number in.** It registers a ceiling at resolution, and it
declares that a pooled reading inside the band is the MODAL outcome (§6).

**EXACTLY ONE PRIMARY SEGMENT (Ob. 15b).** Every other cut on this shard —
per-map, per-seat (`ORD` A vs B), per-`cond`, per-turn-count — is **DESCRIPTIVE
ONLY** and may not be used to rescue a pooled fail. **Ob. 15c applies:** a pooled
fail that clears the pre-declared primary segment in the predicted direction buys
a **NEW screen with its own n** on that segment; these rows may never confirm it.

**Proxy dilution, declared (Ob. 15's own warning turned on this page).** The
mechanism names **STATION-ROUNDS SPENT UNDER A SENTINEL RAY**, and no per-map
station-round table exists in the repo at draft time. Map area is a **declared
proxy for siege duration, and a proxy dilutes** — the segment reads weaker than a
true mechanism-specific split would. **The cheap research item this names: the
§8 dose probe emits station-rounds per map for free, so ONE probe replaces this
proxy with the real property before the screen is fired.**

---

## 3. THE ARM — one file, one hunk, no new constant

### 3.1 The defect, verified at the primary this session

`bots/_v223sealrepair/raid.py:749-778`, inside `_raid_station` (the NEAR
rescan), scans enemy buildings and dispatches on exactly two types:

```
:756   if ct.get_entity_type(bid) == EntityType.LAUNCHER:      -> threats  (exile risk)
:768   elif ct.get_entity_type(bid) == EntityType.GUNNER:      -> gun_axis (LOKI-25)
```

and applies the penalty at `:815-816`:

```
:815   if (s.x, s.y) in gun_axis:
:816       score += LOKI_GUNAXIS_PENALTY
```

**`SENTINEL` has no branch.** The tree models the sentinel as something to KILL
— `raid.py:616` gives `GUNNER`/`SENTINEL` a shared attack priority `pr=3` — and
never as something to stand off. **GREP: PASS at the primary, not relayed.**

⚠ **THE COMMENT HIT IS EVIDENCE FOR THE DEFECT, NOT AGAINST IT** (the trap the
brief names). `raid.py:758-767` is the LOKI-25 justification and it argues the
asymmetry backwards in the present tense:

> *"A gunner's shot is a straight line that IS BLOCKED by obstacles and reaches
> only r^2=13; a sentinel's ignores obstacles. **We are dying almost entirely to
> the AVOIDABLE one.**"*

**That sentence is measured STALE for the bot we ship.** On the then-shipped
trees (v114/v115/v116, 325 games, 301 forward deaths) sentinels covered **68.4%**
of forward builder deaths against gunners' **64.8%**, and the sentinel-ONLY share
was **34.9%** (`docs/coordination.md:39570`). **The comment's 92% reproduces
exactly on the ALL-TIME pool and describes a bot nobody runs** — research's own
D45, `:39553-39590`. This is the third member of the class the s42 wrap counted:
**our own prose contradicting the code beside it.**

### 3.2 The change — `raid.py:753-776`, one hunk

**OLD** (as shipped in v140):

```python
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) == EntityType.LAUNCHER:
                    threats.append(ct.get_position(bid))
                # LOKI-25: GUNNER FIRING AXES. ...
                elif ct.get_entity_type(bid) == EntityType.GUNNER:
                    try:
                        gp = ct.get_position(bid)
                        gd = ct.get_direction(bid)
                        for t in ct.get_attackable_tiles_from(
                                gp, gd, EntityType.GUNNER):
                            gun_axis.add((t.x, t.y))
                    except Exception:
                        continue
```

**NEW:**

```python
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) == self.team:
                    continue
                bt = ct.get_entity_type(bid)
                if bt == EntityType.LAUNCHER:
                    threats.append(ct.get_position(bid))
                # LOKI-25 + SENTTHREAT (#30): TURRET FIRING AXES, both classes.
                # The LOKI-25 comment above claimed the gunner was the avoidable
                # one on 92% attribution -- TRUE all-time, STALE on the shipped
                # tree, where sentinels cover 68.4% of forward builder deaths
                # against gunners' 64.8% (coordination.md:39570). A sentinel's
                # ray ignores obstacles and reaches r^2=32, and it CANNOT rotate
                # -- so stepping off its axis is permanent, not one 10 Ti rotate
                # away. Same set, same penalty, one more entity type.
                elif bt == EntityType.GUNNER or bt == EntityType.SENTINEL:
                    try:
                        gp = ct.get_position(bid)
                        gd = ct.get_direction(bid)
                        for t in ct.get_attackable_tiles_from(gp, gd, bt):
                            gun_axis.add((t.x, t.y))
                    except Exception:
                        continue
```

**What changes:** the type test at `:768` admits `SENTINEL`, and the hypothetical
turret type passed to `get_attackable_tiles_from` becomes the actual type `bt`
instead of the literal `EntityType.GUNNER`.

**What does NOT change, and this is what keeps the arm one-hunk:**
* **No new constant.** The penalty stays `LOKI_GUNAXIS_PENALTY = 8`
  (`doctrine.py:1533`), applied at the same `:815-816` site, to the same
  `gun_axis` set. `doctrine.py` is **byte-identical between the arms.**
* **The comment at `raid.py:811-814` already licenses this**: *"Same penalty
  machinery, one more entity type."* The extension is the sentence the tree
  wrote for itself and never executed.
* **The rest of `_raid_station` — the ring, the ban table, the corner/seat
  scores, the exile penalty, the hysteresis, the tiebreak key — is untouched.**

⛔ **THE ONE DESIGN QUESTION IS DELIBERATELY NOT ANSWERED HERE, AND SAYING SO IS
THE POINT.** Our own prior art weighted the two classes **differently**:
`bots/_v188sentsafe_g/doctrine.py:1583-1584` sets `LOKI_SENTSAFE_GUN_PENALTY = 8`
against `LOKI_SENTSAFE_SENT_PENALTY = 3`. **Choosing between reusing 8 and
matching 3 is a DOSE decision that requires its own sweep, and a screen that
changes a branch AND introduces a tuned weight tests two things at once.** This
arm therefore reuses the existing constant unchanged. **A separate-weight sweep
is a follow-up row, admissible only if this screen or the §8 probe shows the
mechanism fires at all.**

### 3.3 ⛔ THE NEAREST MEASURED ARM IS A DIFFERENT CALL SITE — stated before anyone conflates them

`bots/_v188sentsafe_g` (**SENTSAFE2**, `scratchpad/overnight/SENTSAFE2.tsv`,
5408/5408 complete, **49.83 ±1.33**) implements the same *idea* — avoid enemy
turret coverage — **in `_try_forward_sentinel` (`raid.py:421-460`), which chooses
where WE BUILD A SENTINEL.** It never touched `_raid_station`.

| | SENTSAFE2 (measured) | SENTTHREAT (this arm) |
|---|---|---|
| function | `_try_forward_sentinel` | `_raid_station` |
| decides | where our forward SENTINEL is BUILT | where our RAIDER STANDS |
| events/game | ~2.1 builds (409 / 192 games) | station rescans, every `LOKI_RAID_RESCAN`=6 rounds per near raider |
| new constants | 3 (`LOKI_SENTSAFE_*`) | **0** |
| result | **49.83 ±1.33 @ n=5408** | not measured |

`COMBO-MINING-sweep-2026-08-13.md:98-99` names the distinction from the other
side: *"SENTSAFE × shipped GUNAXIS term — **completes a half-built scorer**
(theirs: gunner-only **for stations**; SENTSAFE's dose was 14/14 sentinel-only)."*

⇒ **SENTSAFE2 is a DIRECTION PRIOR of real weight and it is NOT a measurement of
this arm.** Killing `#30` purely on 49.83 would be this repo's recorded
adjacent-arm error; ignoring 49.83 would be worse. **It is registered as the
expected direction in §6 and as the dose anchor in §8.**

### 3.4 HOT-TURN COST

**hot-turn cost: ADDS, bounded — and the type dispatch REDUCES.**

* **Reduces:** the shipped loop calls `ct.get_entity_type(bid)` **twice** for
  every non-launcher enemy building (`:756` then `:768`). Binding `bt` once
  halves that for the whole scan, in both arms' shared path.
* **Adds, per VISIBLE ENEMY SENTINEL only:** one `get_direction` + one
  `get_attackable_tiles_from` + the set inserts. **A sentinel's pattern is a
  single-tile-wide line at r²=32 ⇒ at most 5 tiles cardinally
  (`floor(sqrt(32))=5`) and 4 diagonally (`4²+4²=32`).** So **≤5 inserts per
  sentinel**, against the gunner's ≤3 at r²=13.
* **Bounded three ways, none of them a per-tile map scan:** (a) the loop is
  `ct.get_nearby_buildings()` with no argument = the builder bot's own vision
  r²=20, not the map; (b) it runs only in the **NEAR** branch, and only when
  `rnd >= self.raid_rescan`, i.e. **once every 6 rounds per raider**
  (`raid.py:743-745`, `doctrine.py:1290`); (c) it is inside the existing
  `try/except` and adds no new failure surface.

⚠ **AND THE STANDING WARNING APPLIES UNCHANGED: `get_cpu_time_elapsed()` READS
ZERO LOCALLY, so no local test catches a CPU regression.** Budget 10,000µs/unit/
turn, worst observed 8,748µs on 900-area maps — **and this arm's segment IS the
900-area class**, which is exactly where the margin is thinnest. **The arm is
bounded by inspection above; there is no instrument that can confirm it locally,
and this document does not claim one.**

---

## 4. CLUSTER ENUMERATION (CLAUDE.md scope procedure, performed in writing)

1. **MATCH cluster — DIES.** A local shard has no 5-game match wrapper; each row
   is an independently seeded single game (`tools/overnight.sh:121` — `seed =
   SEEDLO + n/16`, one `fcode run` per (seed, map, ORD) triple, `:135-136`). No
   stratum can hold two games from one match because no match object exists.
2. **OPPONENT cluster — DEGENERATE.** Exactly one opponent
   (`bots/_v223sealrepair`) for all 5400 rows; no between-opponent contrast is
   drawn, so there is no multi-member opponent stratum to inflate.

⇒ **Applicable DEFF = 0.98** (local pair-weighted, ρ = −0.020, 124 shards, s39
audit). **The platform constants 1.529 / 1.833 are NOT imported** — doing so
would widen these intervals 24–35% for correlation that is not there.

⚠ **Where this could bite:** the s39 audit found local outlier arms with strong
map interaction at DEFF ≈ 1.20–1.25, **and this arm declares a map segment**.
The segment split is therefore **INDICATIVE**; a segment claim is banked only via
the Ob. 15c re-screen, never off these rows.

---

## 5. OBLIGATION 13 — the intersection, stated exactly

```
MECHANISM METRIC READS:  raid.py:768   (consumed at raid.py:815-816)
TREATMENT DIFF TOUCHES:  raid.py       (sole hunk, lines 753-776)
INTERSECTION:            YES — same file, same hunk
```

**This is the strongest form of the obligation and it is worth naming why:** the
metric is not merely *in the same file* as the change, it **IS the changed
branch**. LOKI-18's failure — a metric sitting behind a guard whose behaviour
could not differ between arms, reading 100%/100% — cannot occur here: with the
flag-off control the `SENTINEL` branch does not execute, so the counter is
**structurally 0 in the control and >0 in the treatment whenever an enemy
sentinel is visible.**

⚠ **TOOL STATE AT DRAFT TIME, reported rather than worked around.**
`OB13_INTERSECTION` is computed from `git_diff_paths()`
(`tools/prereg_check.py:1075-1094`), which shells `git diff --name-only <refs>`
and defaults `<refs>` to `HEAD`. **At this moment `git diff --name-only HEAD`
returns four `tools/*.py` paths belonging to a CONCURRENT AGENT's in-flight
edits** — `tools/effective_n.py`, `tools/gate.py`, `tools/overnight_read.py`,
`tools/prereg_check.py`. Against that polluted diff the check FAILs every prereg
in the repo, **including `SCREEN-sealfloor6-2026-08-14.md`, which was certified
green by the side lane hours ago and renders `PREREG_CHECK: FAIL` today.**
⇒ **`TREATMENT DIFF REFS: HEAD -- bots/` scopes the diff to where an arm can
live.** This is not a workaround for a real negative: it is the correct scope,
and it is the scope under which the check **will FAIL if the built arm's
`raid.py` is missing from the diff**. At draft time the arm tree does not exist,
so the check renders **CANNOT-COMPUTE**, which the tool itself calls the
legitimate case for a prereg locked before its tree
(`tools/prereg_check.py:1078-1082`). **The builder must `git add -N
bots/_v240sentthreat` and re-run with `--fire` before firing; at that point a
FAIL is real.**

---

## 6. HYPOTHESIS, DIRECTION PRIOR, GATES AND THE DECISION RULE

### ⚖ RATIFY — HYPOTHESIS (one sentence, falsifiable)

*A raid station standing inside an enemy sentinel's firing line dies to a threat
the station scorer cannot see, and admitting `SENTINEL` to the same `gun_axis`
avoidance set the scorer already applies to `GUNNER` moves raiders off those
lines and raises our pooled game share against v140 above 51.33% at n=5400.*

**The mechanism's asymmetry is the reason to expect it to work at all, and it
cuts the opposite way from LOKI-25's premise:** a gunner answers avoidance for
**10 Ti and one cooldown** (`rotate()`), so a raider that steps off a gunner ray
buys one round. **A sentinel cannot rotate at all** — `rotate()` is gunner-only —
so stepping off a sentinel ray is **permanent** against that sentinel. And a
sentinel does **18 damage**, two-shotting our 40 HP builders, against a gunner's
**7**, which needs six.

### ⚖ RATIFY — EXPECTED DIRECTION (pooled): treatment share ABOVE 50.0, and INSIDE THE BAND is the modal outcome

**The one measured point on this mechanism runs flat.** `SENTSAFE2` — the same
avoid-enemy-turret-coverage idea on the adjacent scorer (§3.3) — read
**49.83 ±1.33 at n=5408**, i.e. **inside its own band**, with a behavioural dose
of **14 redirects across 409 builds in 192 games = 0.073 redirects/game**
(`bots/_v188sentsafe_g/doctrine.py:1566-1571`). **The straight-line reading of
that single measurement is that a coverage-avoidance term at a dose below ~0.1
decisions/game is unresolvable at n=5400 on this fixture.** The hypothesis above
is the interesting alternative; **this prereg registers "inside the band" as the
expectation so that a clear result is a SURPRISE and reads as one.**

⚠ **The prior is one point, on a different call site, at a dose two orders of
magnitude smaller than this arm's plausible event rate.** It orders the
expectation; it does not size it. **That is precisely what the §8 gate measures
before any cores are spent.**

### Fixture

`tools/corefill.sh` → `tools/overnight.sh`, full 15-map post-patch pool
(`overnight.sh:68`), `--tle 10` wall-clock enforced (`:135-136`), `--replay
/dev/null`, **both seat orders per seed** (`:125`). Worklist row:

```
SENTTHREAT  bots/_v240sentthreat  bots/_v223sealrepair  5400  312000
```

Seedbase **312000** is disjoint from every row in
`scratchpad/corefill_work.txt` (verified at draft: **zero** occurrences of any
`31?000` seedbase; the highest in use is 308000, SEALFLOOR6). This shard consumes
312000–312337 (`5400/16 = 337.5`). Basenames `_v240sentthreat` /
`_v223sealrepair` do not collide as substrings, so `corefill.sh:96`'s scoring
refusal does not trigger.

**⛔ READ HYGIENE:** the shard key is **`SENTTHREAT` exactly**. A `grep SENT`
pools **`SENTSAFE`** and **`SENTSAFE2`** — a different call site, a different
control (`_v169launchlate160`), a different chassis. Any read that cannot show it
matched the exact key is not a read of this shard.

### n and resolution

n = 5400, p̄ ≈ 0.5, DEFF 0.98:

| quantity | in pp | **in games (of 5400)** |
|---|---|---|
| 1 SE | 0.67pp | 36.4 |
| **95% half-width** | **±1.33pp** | **±72** |
| **80%-power MDE** (one-sample vs 0.5, Z=2.802) | **≈1.9pp** | **≈102** |
| OB-F final band | 48.67 – 51.33 | **2629 – 2771** |

### GATES

Per `docs/prereg/RULE-futility-gates-2026-08-13.md`, read **ONCE each at first
crossing**; the builder types the decision, the watcher never decides.

* **GATE-1000 (n ≥ 1000): drop if share < 48.0% — i.e. ≤ 479 of 1000.** Label
  `FUTILITY-EARLY`.
* **GATE-2700 (n ≥ 2700): drop if share ≤ 50.5% — i.e. ≤ 1363 of 2700.** Label
  `FUTILITY-ALONE`.
* **Not an ablation arm** (LOW does not determine the decision on its own — see
  the branch table), so the `DECISION-REACHED` clause does not apply.

### ⚖ RATIFY — DECISION RULE

| final at n=5400 | in games | branch |
|---|---|---|
| **≥ 51.33%** | **≥ 2772** | **OUTSIDE-ABOVE → KEEP-dev.** The threat term survives its own screen. Mandatory next steps, both OWED before any verdict sentence cites mechanism: **D26 replication** at seed 313000, scored alone; and the §8 dose read, if it was not already taken. **No ship implication** — `SHIP_SIT` governs and v140 is sitting. A separate-weight sweep (`SENT_PENALTY` 3 vs the reused 8) becomes admissible only from this branch. |
| **48.67% – 51.33%** | 2629 – 2771 | **NO-INFORMATION → DROP, `raid.py:768` unchanged.** Per the pre-committed UNRESOLVED default: the restriction, never the permission. Written as *"the screen could not separate a sentinel-aware station scorer from the shipped gunner-only one at ±1.33pp"*, **never** as *"the sentinel term does nothing"* and never as *"gunner-only measured better"*. **Combined with the §8 dose read this closes `#30`** — see §9. |
| **≤ 48.67%** | **≤ 2628** | **OUTSIDE-BELOW → REAL NEGATIVE, road closes.** Avoiding sentinel rays costs us more than it saves — the plausible mechanism being that the least-covered ring tile is also the least useful one (a station is a PECK/BUILD post, not a hiding place), so the penalty trades damage output for survival at a bad rate. `#30` closes as measured-negative and the `LOKI-25` comment's staleness becomes a documentation fix, not a plank. |

**D26:** any final with |share − 50| ≥ 2.0pp (≤2592 or ≥2808 games) replicates at
seed 313000.

**⚖ RATIFY — the single sentence:** *only an OUTSIDE-ABOVE final keeps this arm
alive; the band and everything below it drop the arm and leave `raid.py:768`
gunner-only.*

---

## 7. THE KILL-ROUND RIDER (defence bar, scored as an EXCLUSION)

**This plank reads defensive and therefore carries the bar.** It buys raider
survival, and `PROGRAMME.md`'s `DEFENCE_ADMISSION_BAR: kill_round_non_regression`
binds: **turrets and stations are bought to OPEN a lane, not to hold one.** The
specific hazard is named in the mechanism itself — **a station chosen for safety
rather than for its seat is a station that pecks and seals less**, which is
exactly the trade that slows a kill.

**⚖ RATIFY — THE RIDER, in both units:** the arm passes iff the 95% CI on
**Δ median kill round (treatment − control)**, paired by seed, **EXCLUDES +10
rounds** — +10 ≈ **+5.7% of our 174-round median kill** (us-only, `CLAUDE.md`).

**⛔ RESTATED AS AN EXCLUSION BEFORE ANY DEFF IS APPLIED**, per `CLAUDE.md`'s
direction clause. *"No significant rise in kill round"* is a **fail-to-exclude**
claim, and widening an interval makes that class of claim EASIER — DEFF applied
to the unrestated form would launder a weak null into a confident one. **The bar
above is already the exclusion form: the CI must exclude the +10 regression.**
Applicable DEFF is 0.98 (§4).

**UNRESOLVED ⇒ RESTRICTION:** if the CI cannot exclude +10, the rider does **not**
pass, and an OUTSIDE-ABOVE share does **not** promote the arm on its own.

**⛔ THE CONDITIONING TRAP, named before the read.**
`tools/overnight_read.py` prints *median kill round GIVEN a kill*, with the kill
counts beside it. A change in **which games end in a kill** moves that median
without anything getting faster or slower. ⇒ **the rider is reported as a pair —
P(core-kill win) AND median-kill-round-given-a-kill, both arms, with both kill
counts — or it is not reported.**

---

## 8. ⛔ THE DOSE GATE — MECHANISM OCCURRENCE IS **NOT BOUNDED** AND THIS IS THE MOST IMPORTANT SECTION ON THE PAGE

### 8.1 What is verified at draft, and what is not

**VERIFIED (code level, both verdicts):** the control feeds **1** enemy turret
class into the station-avoidance set; the treatment feeds **2**. Single hunk,
single call site, both trees inspectable. This is a **structural** dose and it is
what the `DOSE:` field declares.

**⛔ NOT VERIFIED — DECLARED GAP, not discovered later. THE BEHAVIOURAL DOSE IS
UNKNOWN AND I COULD NOT BOUND IT.** The quantity that decides whether this arm
can do anything is **redirected station choices per game** — how often an enemy
sentinel's ray actually covers the station the shipped scorer would have picked,
*and* a cheaper alternative exists. **Nothing in the repo answers it:**

* **The archive cannot.** `corpus/events.tsv` carries BUILD and DEATH events; a
  sentinel's ray requires its **FACING**, and reconstructing per-round facings
  for enemy turrets across the archive is not a query anybody has built. The row
  itself lists *"raider station-rounds standing on a sentinel firing line"* as a
  metric and **no measured value for it appears anywhere in `QUEUE.md`,
  `docs/coordination.md`, or `docs/research/`.**
* **The death-attribution numbers are NOT this number.** 34.9% sentinel-only /
  68.4% any-sentinel coverage of forward builder deaths (`coordination.md:39570`)
  is measured on **v114/v115/v116 — two chassis generations before v140** — and
  it counts DEATHS, not STATION-ROUNDS. It bounds the ceiling of what could be
  prevented; it does not bound how often the scorer gets a chance to prevent it.
* **The nearest number we own is the wrong population and it is small.**
  SENTSAFE measured **0.073 redirects/game** on the sentinel-siting scorer.
  Station rescans are far more frequent than sentinel builds, so the station
  figure should be larger — **by an unknown factor.**

### 8.2 ⚖ RATIFY — THE GATE

**A ~150-game dose probe runs FIRST and its result decides whether the 5400-game
screen is fired at all.** It costs **≈2.8% of the screen**.

**Probe design (the SENTSAFE pattern, which is the reason it is trustworthy):**
per station rescan, log `stations_scored`, `stations_on_sent_axis`,
`stations_on_gun_axis`, `redirected` (chosen station ≠ the station the
gunner-only scorer would have chosen), and the map. **⛔ THE LOG IS EMITTED BY
BOTH ARMS, NOT GATED ON THE FLAG** — `bots/_v188sentsafe_g/raid.py:496-500`
records why in its own comment: *"a log that only the treatment emits cannot show
a null."*

| probe reading | action |
|---|---|
| **≥ 2.0 redirects/game** | **FIRE the 5400-game screen** as registered above. |
| **< 2.0 redirects/game** | **DO NOT FIRE.** `#30` closes as **PREMISE-THIN**: the code defect is real and the scorer never gets enough chances for it to matter. Bank the probe numbers; the `LOKI-25` comment fix at `raid.py:758-767` is then the only surviving deliverable. |

**Where 2.0 comes from, stated so it can be argued with rather than defended
later:** it is **≈27× SENTSAFE's measured 0.073 redirects/game**, and SENTSAFE at
that dose produced a reading (**49.83**) that this fixture could not distinguish
from zero at the same n. **It is a judgment line, not a derived constant, and it
is on the ⚖ RATIFY list for exactly that reason.** A lane that prefers a
different floor should set it here, before the probe runs.

### 8.3 ⚖ RATIFY — pre-declared direction for the probe, so it is falsifiable rather than confirmatory

* **`stations_on_sent_axis` > 0 in a majority of games** — if enemy sentinels
  never cover ring tiles, the mechanism is absent and the screen is pointless.
* **`redirected` STRICTLY GREATER in the treatment than in the control** — the
  control's counter is structurally 0 by construction (§5), so a non-zero control
  reading means the probe is instrumented wrong and **no number from it may be
  read**.
* **`stations_scored` IDENTICAL between arms** — the arm is a RANKING, not a
  FILTER; it changes which station wins, never how many are admissible. **If
  `stations_scored` differs, the diff is not the diff this document describes.**

**If the probe shows `redirected` ≈ 0 in the treatment, the mechanism does not
fire and no share reading from any n means anything.** That is the anti-Goodhart
clause for this arm.

### 8.4 ⚠ THE SURVIVAL METRIC, AND WHICH FIXTURE CAN ACTUALLY RESOLVE IT

The natural mechanism metric is **forward builder deaths/game** (using `#23`'s
**verified midline filter `d2_enemy < d2_own`**, 100% clean on 40,000 rows — NOT
the `d2_enemy <= 60` absolute band; the two differ by ~30% at the endpoint and a
forward/home statistic states its filter inline, `coordination.md:39647-39662`).

**⛔ AND THE FIXTURE CAVEAT IS LOAD-BEARING.** Our own probes lie in a known
direction on survival: **zero of our forward turrets died in 480 arena games
against 46.9% on the ladder.** Here the fixture is **self-play against v140**,
which is better than a hand-written probe and still not the field:

* **What the local screen CAN resolve:** the redirect count and
  `stations_scored` invariance (our own code executing — fixture-honest), and
  game share against a real, strong, unmodified opponent tree.
* **What it CANNOT resolve:** whether the deaths prevented are the deaths the
  FIELD inflicts. **The threat population in this fixture is v140's own sentinel
  doctrine — 4.59 sentinels/game (`coordination.md:49134`), 86-89% of them
  forward** — so the mechanism is genuinely expressed and the screen is NOT
  coupled-incumbent-absent. But their **siting** is our doctrine, not the
  league's. **A field death-reduction claim needs a live leg and this screen may
  not make one** (§9).

---

## 9. COUPLING CLASS, INTERACTIONS, AND WHAT THIS SCREEN MAY CONCLUDE

**COUPLING CLASS: SELF-KNOWLEDGE / FIELD-EXPRESSED.** The station scorer is ours;
the threat is a standard league turret that our own control builds 4.59 times a
game. ⇒ **screen-trustworthy**, which is why a local shard is the right first
instrument and why no live window is spent here.

### Interaction with the two live legs (required declaration)

* **SEALFLOOR6** (`_v238sealfloor6` vs v140, LOCAL, seedbase 308000, ~3% filled
  at the s41 wrap). **Its primary segment is the 10 ≤676-area maps; mine is the
  complementary 5 900-area maps.** The diffs are disjoint —
  `doctrine.py:1228` (`LOKI_SEAL_TI_FLOOR`) vs `raid.py:768` — and neither arm
  contains the other's change, so **there is no statistical interaction between
  the two contrasts**; each is measured against the same frozen control.
  **The real interaction is ALLOCATION: both draw from the same local core pool**,
  and SEALFLOOR6 is the incumbent read. ⇒ **the §8 probe (~150 games) is
  affordable alongside it; the 5400-game screen is a scheduling decision for the
  builder, not a design one.** Seedbases are disjoint (308000 vs 312000).
* **SALTREF2** (`_v231saltref` vs v140, REMOTE work-server-1, WORKERS=10, ~970/
  5400 at the wrap). Different host, different pool of cores, disjoint diff.
  **Named behavioural adjacency, NOT claimed and NOT tested here:** salt and seal
  are both raid-layer behaviours executed FROM a station, so a change in which
  station a raider occupies could in principle change salt/seal opportunity.
  **Neither shard's own contrast is confounded by this** (each is a single-hunk
  arm against the same frozen control), and **no combo claim may be drawn from
  the two shards read together.**

### NOT LICENSED by this screen

* **No ship implication.** `SHIP_SIT` governs; v140 is sitting. An OUTSIDE-ABOVE
  final buys a D26 replication and the dose read, not an activation.
* **No field claim about death reduction** — §8.4. That requires a live leg.
* **No combo claim** with `SENTSAFE`, `GBNOSHIELD`, or any other arm. This is a
  single-hunk arm against the incumbent.
* **No claim about the PENALTY WEIGHT.** The reused `8` is untested against the
  `3` our own prior art chose for sentinels (§3.2). A null here does **not**
  close the weight question; it closes the *branch-extension* question at
  weight 8.
* **No claim about `#31a` GUNBLOCK**, which the same FIRE ORDER entry ties to
  this row. Different mechanism, different arm.

### ⛔ WHAT IS LOST IF THE LANE KILLS THE ROW INSTEAD (so the choice is informed)

Killing `#30` on the sweep's arithmetic forfeits: (a) the only cheap test of
whether *any* threat-avoidance term pays at the STATION call site, as opposed to
the SITE call site SENTSAFE already measured flat; (b) the §8 probe's
station-round table, which is the only route to replacing this document's area
proxy with the real terrain property; and (c) nothing else — **the code defect
and the stale `LOKI-25` comment are documentation deliverables that survive
either decision** and should be fixed regardless, since a lane grepping
`raid.py:758-767` today is told the sentinel is the *unavoidable* threat and that
we die *"almost entirely to the AVOIDABLE one"*, both of which are false for the
bot we ship.

---

## FALSIFIER

**The hypothesis (§6) is falsified by any of:**

1. **A dose-probe reading below 2.0 redirects/game (§8.2)** — the scorer does not
   get enough chances for the branch to matter, the screen is not fired, and
   `#30` closes PREMISE-THIN. *(This is a falsifier of the PLANK, not of the code
   fact, and the two must not be conflated in the write-up.)*
2. **A final ≤ 48.67% (≤ 2628 of 5400)** — sentinel avoidance is measurably worse
   than the shipped gunner-only scan; the road closes.
3. **A futility drop at either gate** (≤479/1000 or ≤1363/2700) — the arm is not
   worth more cores; no claim is made at that resolution.
4. **A final inside the band (2629–2771)** — not supported at ±1.33pp; the
   shipped branch stays by the UNRESOLVED default. **This is the modal outcome
   and it is pre-typed as a DROP, not as a null to be argued with.**
5. **A probe showing `stations_scored` differing between arms, or `redirected`
   non-zero in the control** — the arm is not a ranking-only change, or the
   instrument is wrong; **no share reading may be read either way.**
6. **The kill-round rider failing to exclude +10 rounds (§7)** — the arm buys
   survival at the kill's expense and is off-programme whatever it does to share.

**The PRIMARY SEGMENT prediction is falsified** if the treatment's share on the
5 900-area maps is **≤** its share on the 10 ≤676-area maps. *(A reversal — the
term helping most where sieges are shortest — would mean the dose is driven by
something other than siege duration, and per Ob. 15c it buys its own screen with
its own n; it does not rescue a pooled fail on these rows.)*

---

## 10. ⚖ THE RATIFY LIST, gathered (the lane types these, not this agent)

1. **Whether to fire at all**, against `QUEUE-ECONOMICS-SWEEP-2026-08-14.md`'s
   KILL-CANDIDATE recommendation (§0, §9).
2. **HYPOTHESIS** (§6).
3. **EXPECTED DIRECTION** — pooled above 50, modal outcome inside the band (§6).
4. **DECISION RULE** branch labels and the single KEEP-vs-DROP sentence (§6).
5. **THE DOSE GATE and its 2.0 redirects/game floor** (§8.2) — a judgment line.
6. **The probe's three pre-declared directions** (§8.3).
7. **THE KILL-ROUND RIDER** at +10 rounds, in exclusion form (§7).
8. **SEGMENT** — 5 900-area maps, positive on-segment (§2).
9. **FALSIFIER** (all six clauses).

---

## 11. OBLIGATIONS REGISTER (`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md`)

* **Ob. 7 (PRE-STATE / outcome form):** satisfied — the outcome is **game share
  IN OUR FAVOUR** on this shard, not a win-condition mix; the predicted-change
  set is verified not pre-satisfied (§2 `PRE-STATE`, grepped at the primary).
* **Ob. 8 (denominator rule):** single control, single fixture, single shard; the
  denominator is 5400 rows from one worklist row, pooled with nothing — and
  explicitly **not** with `SENTSAFE`/`SENTSAFE2` (§3.3, §6 read hygiene).
* **Ob. 12 (gate carries its resolution statement + pre-committed unresolved
  default):** satisfied in §6, including the explicit restriction default.
* **Ob. 13 (`file:line` + intersection):** satisfied in §5 — **same file, same
  hunk**, the strongest available form — with the tool's current
  polluted-diff state reported rather than worked around.
* **Ob. 14 (opponent version stability):** **N/A by shape** — the control is a
  byte-frozen local tree, not a platform cell. No `CELLS:` line exists.
* **Ob. 15a/b/c (map dependence):** satisfied in §2 with one primary segment, a
  signed direction, a recomputable value ceiling, an explicit descriptive-only
  list, and the proxy-dilution declaration.
* **Ob. 1–4, 6, 9–11:** Ouroboros/CAD-leg-specific or platform-mechanism-leg
  specific; they do not instantiate on a local single-hunk screen. Stated rather
  than skipped.
* **⛔ NOT SATISFIED, structurally — `BOUNDARY` in accepts.**
  `tools/prereg_check.py`'s `BOUNDARY_UNITS` demands the boundary in both accepts
  and games with the platform identity `games = 5 × accepts`. **A local shard has
  no accepts**: one row is one game, and there is no 5-game match wrapper (which
  is also why the MATCH cluster dies in §4). The boundary is declared in the only
  two units it has — **5400 rows = 5400 games**. The tool models this exemption
  explicitly (`prereg_check.py:616-630`); recorded here rather than passed over.
* **⛔ TOOL FINDING, reported not worked around:** `OB13_INTERSECTION` currently
  computes against a diff containing another agent's in-flight `tools/*.py`
  edits, which renders **`PREREG_CHECK: FAIL` on the repo's only
  previously-green prereg** (`SCREEN-sealfloor6-2026-08-14.md`). Full detail and
  the scoping fix in §5. **This is an environment state, not a defect in this
  document, and it must be re-checked with `--fire` after the arm tree lands.**

## Target-value line

Local screen, zero live exposure ⇒ payout gate **N/A** (see §2 `TARGET BAND`).
