# SCREEN PREREG — FINISHHP: a builder standing beside a four-pecks-from-dead enemy turret finishes it instead of taking the universal Core heal (QUEUE #2, RE-SCOPED to the home siege band)

**STATUS: committed BEFORE the `FINISHHP` shard's first row exists, and before
the treatment tree exists at all.** Two-clock: this file's git author time vs the
`# FIXTURE ... start=` stamp `tools/overnight.sh:96` writes into
`scratchpad/overnight/FINISHHP.tsv` before its first game (the START stamp, not
the first result row — `overnight.sh:84-95` records why the first-row clock is
one game length late). No row of this shard exists at commit time and none may
be read before it does. Drafted **2026-08-14T22:03:41Z** (`date -u`, same shell
call), repo at **`7f05e73f`**.

---

## ⛔⛔ VERDICT AT THE TOP, BECAUSE IT CHANGED WHILE THIS WAS BEING WRITTEN

**THIS DOCUMENT IS COMPLETE, PASSES `tools/prereg_check.py`, AND ITS OWN DOSE GATE
SAYS `DO NOT FIRE`.**

The plank is **DRAFTABLE** — the call site is named and unambiguous (§4.1), the
mechanism is **specified but not wired** (§4.2, verified both ways), and the hunk
is expressible without any open design decision (§3). **What is not supportable is
the 5400-game SCREEN.**

The dose gate in §8.2 was written, and its floor of **0.50 finish-fires/game**
fixed, **BEFORE any measurement existed**. An independently-tasked subagent then
measured the trigger directly over **571 archived v140 games / 151,442 rounds**,
reconstructing per-round HP and position from the raw replay stream:

> **0.370 trigger rounds/game ungated · 0.217 with the bot's own `near_home` gate ·
> a trigger in 11.4% of games — against a registered floor of 0.50, and both figures
> are UPPER BOUNDS (cooldown unmodelled).**

⇒ **The gate's lower branch fires. `#2` closes PREMISE-THIN at the home band too,
matching its enemy-ring verdict.** ⛔ **The floor was NOT moved** (§8.2).

**The single sharpest fact, and it is a finding about the FORM this plank was handed
in rather than about its idea:** the best exemplar in the entire corpus — an enemy
gunner sat at **HP=6 for ≥74 rounds** with our builders repeatedly orthogonally
adjacent — is at **d²=29 from our core, OUTSIDE the `near_home` d²≤25 band the hunk
inherits from the heal guard.** **The hunk registered here would not have fired on
it** (§8.1). The tree already carries `HUNT_BAND_DSQ = 41`, the one hunt constant
that IS read.

**⚖ THE LANE'S CALL:** the gate is a **GATE, not a VETO**. Overruling it is
permitted and must be done **in writing, with the number in hand** — a weaker act
than clearing it. §8.3 prices the three knobs that could lift the dose and shows
that **even all three together cap at ~26% of games**.

**PROVENANCE: bots/_v223sealrepair/main.py (:1-30, :128-151, :400-560, :655-720) · bots/_v223sealrepair/doctrine.py (:160-253, :913-932, :1474-1536) · bots/_v223sealrepair/eco.py (:310-340, :365, :1074, :1173) · bots/_v223sealrepair/raid.py (:256, :334, :427, :595-650, :683, :764-772) · bots/_v210idlepeck2/doctrine.py:1490-1498 · QUEUE.md (row #2, line 162) · docs/prereg/SCREEN-sentthreat-2026-08-14.md (structure, kill-round-rider form, dose-gate form) · docs/prereg/DOSE-idlepeck-quiet0-48-2026-08-13.md (header only) · docs/research/CLOSED-BY-LEG-INDEX-2026-08-14.md:26-31 · tools/prereg_check.py (:1-620, :700-1060) · tools/overnight.sh:1-160 · tools/dose.py:1-45,60-180 · tools/corpus/replay_events.py:29-125 · tools/replay_schema.md, tools/corpus/replay_census.py, tools/corpus/replay_autopsy.py, tools/crash_census.py (named as the raw-replay HP-reconstruction primitives; read and run by the delegated dose subagent, whose full result is transcribed at §8) · corpus/version_trees.tsv, corpus/meta_join.tsv, corpus/events.tsv, corpus/builds.tsv, corpus/join.tsv, replay_archive/ (dose subagent's inputs) · maps/*.map26 (encoded sizes, segment corroboration) · scratchpad/corefill_work.txt (seedbase + shard-name collision check) · `ls bots/`, `ls scratchpad/overnight/` (collision checks) · CLAUDE.md (boot block, entity table, DEFF block)**

Drafted by a **FRESH opus subagent with no inherited session context** beyond the
brief recorded in §1. Every file above was opened **read-only**. **No shard row
of any kind was read; no game was run; no tree under `bots/` was created or
edited by this agent; nothing was committed, staged or pushed.**

---

## 1. THE BRIEF, RECORDED AS HANDED (not re-derived)

The task specified: `QUEUE.md` row **#2**, found NOT DRAFTABLE at the ENEMY ring
(positioning half duplicates the locked `SCREEN-sentthreat`, hunt half
premise-thin there), **re-scoped to the HOME SIEGE BAND**; plank name
**`finishhp`**; LOCAL corefill fixture; control `bots/_v223sealrepair` (v140,
LIVE incumbent); 15-map pool; **local DEFF = 0.98** with the platform constants
(1.529 / 1.833) explicitly NOT to be imported; half-widths ±1.33pp at n=5400 /
±1.89 at 2700 / ±3.10 at 1000; `cut_short_floor` ≤ `planned_n`; one local row =
one game; seed base ≥ 322000; kill-round non-regression bar **phrased as an
exclusion**; hot-turn rider.

The brief also relayed, **unverified by the relaying agent and flagged as such**,
that over 571 archived v140 games enemy turrets sit at **d²≤8 of our core
0.856/game** and at **d²≤41 (`HUNT_BAND_DSQ`) 2.214/game**. ⛔ **Neither figure
reproduces on an independent read of the same 571 games (1.019 / 3.047, three
surfaces agreeing digit-for-digit) — an INSTRUMENT ALARM, reported unreconciled at
§8.6 and diagnosed by nobody.** It does not change the verdict: neither number is
the trigger, and the trigger was measured directly (§8.0).

**⭐ AND THE BRIEF'S THIRD STOP CONDITION WAS DISCHARGED BY MEASUREMENT, NOT BY
CAVEAT.** The brief said *"sanity-check them if you can; if you cannot, say so."*
This agent delegated that check to a separate opus subagent, which found the raw
`replay_archive/` carries per-round HP and position (the derived corpus TSVs do
not) and answered the real dose question directly. **§8 is therefore a MEASURED
gate, not a planned probe** — and it is the reason this document's headline is
`DO NOT FIRE`.

**Every game fact used below was re-verified against `CLAUDE.md`'s entity table
before use** (builder attack 2 Ti → 2 dmg, orthogonal only, acting blocks moving;
heal 1 Ti → +4 HP; sentinel 40 HP / r²=32 / dmg 18 / reload 2 / obstacle-piercing
/ **cannot rotate**; gunner 25 HP / r²=13 / dmg 7 / reload 1 / obstacle-blocked).

---

## 2. REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen, ZERO live rated exposure; no submit, no activation, no prototype on the ladder, so `tools/target_value.py`'s reachable-band gate does not bind.**
**PINNED: N/A — local screen. The control is a byte-frozen local tree (`bots/_v223sealrepair`), so opponent churn cannot reach this shard; the pin / never-pin design rule governs PLATFORM legs only.**
**SURFACE: local**
**CLUSTER UNIT: none — enumeration performed in §5; both clusters die, applicable DEFF = 0.98 (local, measured pair-weighted over 124 shards, s39 audit)**
**ESTIMATOR: pooled game share = treatment wins / (rows − NOWINNER rows − comment rows), unweighted, over `scratchpad/overnight/FINISHHP.tsv` rows only. No map weighting, no seat weighting, no pooling with any other shard and specifically NOT with `IDLEPECK`, which is a different call site in the enemy half (§4.4).**
**TREATMENT TREE: bots/_v242finishhp — PROPOSED NAME, NOT YET BUILT. This agent is forbidden to write under `bots/`; the builder builds the tree from the diff in §3 and re-runs `tools/prereg_check.py --fire` once it is `git add -N`'d.**
**PLANNED n: 5400 games**
**BOUNDARY: 5400 shard rows = 5400 games (LOCAL fixture: 1 row = 1 game; the platform `games = 5 × accepts` identity has no accepts to close on here — declared exemption, §11). Interim gates at 1000 and 2700 games.**
**CUT-SHORT: below n=1000 this shard publishes descriptive tallies only and takes NO comparative look; a futility drop at either interim gate publishes the label, the n and the share and makes NO claim about the mechanism beyond "not worth more cores now". `cut_short_floor` = 1000 ≤ `planned_n` = 5400.**
**BAR: 51.33**
**BASE RATE: 50.0**
**BAR SOURCE: the standing corefill screen band — the 95% half-width at n=5400 with DEFF 0.98, i.e. 1.96·√(0.5·0.5·0.98/5400) = ±1.33pp. Identical construction to `SCREEN-sealfloor6-2026-08-14.md`, `SCREEN-sealsweep-2026-08-14.md` and `SCREEN-sentthreat-2026-08-14.md`.**
**BASE RATE SOURCE: structural null of a paired local screen — `tools/overnight.sh:124-136` plays every (seed, map) in BOTH seat orders (`ORD` A and B), so under H0 the expected treatment share is exactly 50.0. No historical population is consumed by the bar. (Seat is worth ~7.6pp on byte-identical arms — `overnight.sh:30-32` — which is why balance is by construction and not by adjustment.)**
**REFERENCE n: none — no fixed historical reference is a comparator in any bar on this page. The relayed 0.856 / 2.214 turrets-per-game figures are UNRECONCILED against an independent read (§8.6), are a comparator in no bar, and are load-bearing for nothing on this page.**
**MECHANISM METRIC READS: main.py:423 (the new `HUNT_FINISH_ON and self._finish_turret(ct)` short-circuit inside the universal-heal guard), whose body is the new `_finish_turret` method at main.py:~521. TREATMENT DIFF TOUCHES: main.py (call site + one new method), doctrine.py (one new toggle line). INTERSECTION: YES — the metric IS the diffed branch, in the diffed file.**
**TREATMENT DIFF REFS: HEAD -- bots/**
**DOSE: MEASURED, not projected — finish-trigger rounds per game (enemy gunner/sentinel alive, HP at or below the threshold, orthogonally adjacent to a living builder of ours): treatment 0.370 vs mutation control 36.737 with the HP predicate inverted (n = 571 archived v140 games, 151,442 rounds, raw-replay HP reconstruction; the inverted control reads 99× and establishes that the HP filter rather than the geometry plumbing is what selects). ⛔ 0.217 once the bot's own `near_home` gate is applied, against a floor of 0.50 registered BEFORE the measurement existed ⇒ THE GATE'S LOWER BRANCH FIRES: DO NOT RUN THE SCREEN (§8.0, §8.2). Structural dose additionally: 1 treatment code path vs 0 in the control, by two independent gates (§4.2).**
**GATE RESOLUTION: §6 — the ±1.33pp band at n=5400 discriminates a true effect of ~1.9pp at 80% power; UNRESOLVED (final inside 48.67–51.33) defaults to the RESTRICTION — the shipped heal-first ordering stays, the arm is not promoted, and per §9 the row then closes rather than re-running at a larger n.**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock. Verified at the primary this session (§4): `_hunt_turret` has NO definition and NO call site anywhere in the tree (three comment mentions only, doctrine.py:160,231,771); `HUNT_DESIGNATE_DSQ`, `HUNT_MIN_HEALERS`, `HUNT_FINISH_HP`, `HUNT_FIRE_TI`, `HUNT_DEFER_BASE`, `HUNT_DEFER_SPREAD` and `DUEL_DISCIPLINE_ON` are each read ZERO times outside comments; `_duel_safe` (doctrine.py:771) does not exist either. There is no cell here that is pre-satisfied.**
**MAP SEGMENT: the 5 900-area maps — drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie — versus the 10 ≤676-area maps (antler, archipelago, auroraveil, drumlin, fjordgate, frostgate, icefloe, nordkap, royale, yulerune). MECHANISM: the branch can only fire on a round where our Core is already under threat AND a nearly-dead enemy turret is orthogonally adjacent to one of our home builders, so its dose is (enemy turrets planted in our home band) × (rounds we survive under siege). Both terms grow with siege duration, and siege duration grows with approach length; map area is the available proxy for approach length.**
**PRIMARY SEGMENT: the 5 900-area maps (drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie).** *(Split corroborated independently this session by encoded map size — those five are `maps/*.map26` of 1050, 1890, 1050, 1050 and 1890 bytes against ≤808 for all ten others; a size ordering, not a grid read, and it agrees with the split `SCREEN-sentthreat-2026-08-14.md` declares.)*
**EXPECTED DIRECTION: POSITIVE on-segment, ~ZERO off-segment — treatment share ABOVE 50 on the 5 900-area maps and ≈50 on the 10 ≤676-area maps.**
**SEGMENT VALUE CEILING: 33.3% x 4.0pp on-segment = 1.33pp pooled**
**POOL ERA: post-2026-08-13-rotation — the local 15-map pool `maps/*.map26` as read by `tools/overnight.sh:68`, post-patch geometry (valkyrie and glacierkeep grids rewritten 2026-08-14 by MAPFIX/v139; the other 13 unchanged). No number on this page comes from the rated ladder tape, so the ladder pool boundary bounds nothing here.**
**SPANS-POOL-CHANGE: no — the shard is created after the 2026-08-13 rotation and every row it will contain comes from the single post-rotation local pool.**

### ⛔ THE SEGMENT SIGN IS ARGUED, NOT MEASURED — and the counter-story is named here rather than kept in reserve

The 900-area prediction rests on **siege duration grows with approach length**.
**The opposing story is real and I cannot rule it out at draft:** on a SMALL map
the enemy reaches our half in fewer rounds, so an enemy turret planted inside
`HUNT_BAND_DSQ` of our Core is *easier* to achieve and arrives *earlier*, giving
more trigger-rounds before the game ends. **If the treatment's share on the 5
900-area maps is ≤ its share on the 10 ≤676-area maps, the segment prediction is
FALSIFIED** (§10) — and per Ob. 15c a reversal buys its own screen with its own
n; it does **not** rescue a pooled fail on these rows.

**The proxy is declared and it dilutes.** The mechanism names **rounds spent
under siege with a finishable turret adjacent**, and no per-map table of that
quantity exists in the repo at draft time. **The §8 dose probe emits it per map
for free**, so ONE probe replaces this document's area proxy with the real
property before the screen is fired. A segment replacement made from the PROBE
(which contains no screen rows) is an ADD-only amendment blind to the screen
data; it is registered here in advance as the intended path.

**EXACTLY ONE PRIMARY SEGMENT (Ob. 15b).** Every other cut on this shard —
per-map, per-seat (`ORD` A vs B), per-`cond`, per-turn-count — is **DESCRIPTIVE
ONLY** and may not be used to rescue a pooled fail.

### The ceiling is an admission, not a forecast

**1.33pp pooled is EXACTLY this screen's 95% half-width.** It is the largest
pooled effect this document is willing to put its name to, and it sits precisely
where the screen stops being able to tell the effect from noise. **It is an upper
bound.** ⛔ **NO ECONOMIC CHANNEL IS CLAIMED AND NONE MAY BE READ IN.**
Destroying an enemy building LOWERS their global cost scale and therefore HELPS
them, and a turret is the largest per-entity contribution at +20%. **The value of
this plank is TACTICAL ONLY — the removal of a shooter from beside our Core — and
the scale refund is a cost the plank pays, not a benefit it earns.**

---

## 3. THE ARM — one behaviour, two files, three previously-dead constants wired

### 3.1 doctrine.py — one new line, inserted after `HUNT_FIRE_TI` (doctrine.py:215)

```diff
 HUNT_FINISH_HP = 8
 HUNT_FIRE_TI = 2
+# FINISHHP (QUEUE #2, re-scoped): wire the HUNT_FINISH_HP exemption described
+# at :205-211 into the universal-heal ordering at main.py:420.  Toggle kept for
+# the ablation matrix, same as DUEL_DISCIPLINE_ON / MEDIC_EARLY_ON / CB_OVER_HEAL_ON.
+HUNT_FINISH_ON = True
```

`main.py:27` is `from doctrine import *`, so the constant binds with no import
change.

### 3.2 main.py:420-424 — the call site, one inserted branch

```diff
         if (near_home and ct.get_action_cooldown() == 0
                 and ct.read_store(SLOT_UNDER) != 0
                 and not (LOKI8_RAIDERS_STAY_OUT and self.role == "raid")):
+            # HUNT_FINISH_HP EXEMPTION (doctrine.py:205-211).  A turret four
+            # pecks from death beside a shelled Core outranks the heal: four
+            # rounds of work against 283 rounds of silence.
+            if HUNT_FINISH_ON and self._finish_turret(ct):
+                return
             if not self._cb_over_heal(ct) and self._heal_core(ct):
                 return
```

### 3.3 main.py — one new method, placed immediately after `_sabotage_prio` (which ends at main.py:521)

```python
    def _finish_turret(self, ct):
        """HUNT_FINISH_HP: peck an orthogonally adjacent enemy turret that is
        four pecks from death, INSTEAD of taking the universal Core heal.

        doctrine.py:205-211 is the spec and this is its only wiring: hunting
        normally waits on HUNT_MIN_HEALERS, and the single exception is a turret
        already inside four pecks, "where removing its damage permanently beats
        four rounds of +4 HP by a wide margin".  DUEL_DISCIPLINE_ON's third
        exemption (doctrine.py:230-235) is the ray test, read from the
        attacker's side: a turret whose ray covers MY tile is killing me while I
        peck it; one whose ray points elsewhere is free damage.

        Orthogonal only -- a builder attack requires an orthogonally adjacent
        tile, so a DIAGONAL neighbour (d^2 = 2) is out of scope by the rules and
        not by choice.  See the prereg's section 4.3.
        """
        if ct.get_global_resources() < HUNT_FIRE_TI:
            return False
        p = ct.get_position()
        for d in CARDINALS:
            t = p.add(d)
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                et = ct.get_entity_type(bid)
                if et not in (EntityType.GUNNER, EntityType.SENTINEL):
                    continue
                if ct.get_hp(bid) > HUNT_FINISH_HP:
                    continue
                if DUEL_DISCIPLINE_ON and ct.can_fire_from(t, ct.get_direction(bid), et, p):
                    continue
                if ct.can_fire(t):
                    ct.fire(t)
                    return True
            except Exception:
                continue
        return False
```

**Every element is precedented in this tree, not invented:**

| element | precedent in v140 |
|---|---|
| `for d in CARDINALS` + in-bounds guard + `get_tile_building_id` + team test + per-tile `try/except` | `_sabotage_prio`, main.py:507-521 (byte-for-byte the same scan shape) |
| `ct.can_fire(t)` from a **builder** context | `_sabotage_prio` main.py:518, `raid.py:626` |
| `ct.can_fire_from(pos, facing, turret_type, target)` from a **builder** context | `_try_counterbattery`, main.py:575 (same argument order) |
| `ct.get_direction(bid)` only on GUNNER/SENTINEL | the type filter above precedes it; LAUNCHER is facing-independent and is excluded, so the raising case is unreachable |
| blanket crash safety | `run()` is one blanket `try/except` (main.py:128-139) **and** every tile is individually guarded here |

**No new tunable other than the on/off toggle.** `HUNT_FINISH_HP=8`,
`HUNT_FIRE_TI=2` and `DUEL_DISCIPLINE_ON=True` all already exist at
doctrine.py:214, 215 and 235 and are read **zero** times in v140.

### 3.4 HOT-TURN COST

**RIDER: ADDS.** Bounded and small, but it is an add and it lands on the segment
with the least headroom.

* **Cost when it fires at all:** one `get_global_resources()`; then per cardinal
  tile, at most `get_tile_building_id` + `get_team` + `get_entity_type` + `get_hp`
  + `get_direction` + `can_fire_from` + `can_fire` — **≤ 4 × 7 = 28 controller
  calls**, with early `continue` on the first failing test (the overwhelmingly
  common case is `bid is None`, which costs 1 call per tile).
* **Cost when it does not fire:** the whole method is behind the existing
  `near_home and cooldown==0 and SLOT_UNDER!=0 and not raider` guard at
  main.py:420, which is unchanged. On a round where that guard is False the cost
  is **zero**.
* **Cheapest-first ordering is deliberate:** the `get_global_resources()` floor
  short-circuits the entire scan for 1 call; `bid is None` short-circuits a tile
  for 1; `get_hp > 8` short-circuits before the two expensive ray predicates.

⭐ **THE `HUNT_FIRE_TI` FLOOR IS CRASH SAFETY, NOT ONLY THRIFT — and the reason is
a documented engine asymmetry.** `CLAUDE.md`'s guard-matrix sweep records that
**`can_fire` returns TRUE at 0 ammo** (`can_fire@0x16280` carries no balance
reference; the check lives in `finish_firing_turret@0x26eac` and **RAISES**). If
the builder-melee path shares that asymmetry for TITANIUM, then `can_fire(t)`
would pass at 1 Ti and `fire(t)` would raise — and an escaping `GameError`
**permanently destroys the unit**. The floor makes that unreachable, and the
per-tile `try/except` plus `run()`'s blanket handler (main.py:128-139) are the
second and third layers. ⚠ **This document does NOT claim the asymmetry is
present for titanium — it claims the guard costs one integer comparison and
removes the question.** *(It also prevents converting a working 1 Ti heal into a
no-op, which is the thrift half.)*

⛔ **THE HAZARD, STATED PLAINLY:** the budget is 10,000 µs/unit/turn and the
worst observed is **8,748 µs on 900-area maps** — **87% of budget** — and the
900-area maps are **this document's PRIMARY SEGMENT**. A timeout does not destroy
the unit (only an uncaught exception does), but it truncates that turn's `run()`,
which on a besieged builder means the heal is not taken either. **This is a
mechanism that could make the arm lose on exactly the maps it predicts a win on,
and it would look like a plank failure rather than a budget failure.**

⛔ **AND THE BLOCK RUNS BEFORE `self._cpu_exhausted(ct)`** (main.py:442), because
it must precede the heal and the heal precedes that guard. **That ordering is
forced by the mechanism and is not a choice this document is free to make
differently.** The mitigation available without inventing design is the
cheapest-first ordering above and the 4-tile bound.

⚠ **`get_cpu_time_elapsed()` READS ZERO LOCALLY**, so the local fixture cannot
measure this and **must not be quoted as evidence that the cost is affordable**.
**FALSIFIER 7 (§10) is the CPU falsifier** and it is scored on the shard's own
`turns`/`NOWINNER` columns, which is the only CPU-sensitive signal a
`--replay /dev/null` shard emits.

---

## 4. STOP-CONDITION FINDINGS — the three the brief demanded, answered at the primary

### 4.1 "Do not invent a change" — the call site is NAMED and it is unambiguous

**`bots/_v223sealrepair/main.py:420-424`.** This is the only site at which the
change can be made, and that is provable rather than asserted: the universal heal
**returns from the turn** on success (main.py:424), so *every* melee path further
down the file — `_home_defend`'s `_sabotage_prio` (main.py:478), `_defend`'s
(main.py:668), the whole role dispatch at main.py:446-451 — is **unreachable on a
round where the Core is damaged and a builder is beside it.** Moving the peck
anywhere below line 424 changes nothing in the state this plank exists for.

### 4.2 "Do we already do it?" — **SPECIFIED BUT NOT WIRED**, confirmed both ways

**THE SPEC EXISTS.** `doctrine.py:169-253` is ~85 lines of present-tense
turret-hunting design prose with a named function, a designation ballot, a
deadlock breaker and seven constants.

**THE BEHAVIOUR DOES NOT.** Verified by exhaustive grep over all four files of
the tree:

| symbol | definition | call site / read |
|---|---|---|
| `_hunt_turret` | **NONE** | **NONE** — three comment mentions (doctrine.py:160, 231, 771) |
| `_duel_safe` | **NONE** | **NONE** — one comment mention (doctrine.py:771) |
| `HUNT_DESIGNATE_DSQ` | doctrine.py:212 | **0** (comments at :194, :197) |
| `HUNT_MIN_HEALERS` | doctrine.py:213 | **0** (comments at :70, :205, :428) |
| `HUNT_FINISH_HP` | doctrine.py:214 | **0** (comment at :208) |
| `HUNT_FIRE_TI` | doctrine.py:215 | **0** (comments at :433, :914) |
| `HUNT_DEFER_BASE` | doctrine.py:252 | **0** |
| `HUNT_DEFER_SPREAD` | doctrine.py:253 | **0** |
| `DUEL_DISCIPLINE_ON` | doctrine.py:235 | **0** |
| *(contrast — the control that makes the column mean something)* `HUNT_BAND_DSQ` | doctrine.py:163 | **3 real reads**: eco.py:365, main.py:535, main.py:546 |

**That last row is the other verdict.** A "zero reads" column that has never
produced a non-zero entry is not a check; `HUNT_BAND_DSQ` sits in the same block,
was found by the same grep, and reads 3.

**AND THE HOME PECK IS SILENCED TWICE OVER, INDEPENDENTLY.** Even if the heal
ordering were changed and nothing else:

1. **`_home_defend` is DEAD CODE.** Its only call site (main.py:436) is gated on
   `not LOKI8_RAIDERS_STAY_OUT`, and `LOKI8_RAIDERS_STAY_OUT = True`
   (doctrine.py:1528). Its `_heal_adjacent` (main.py:480) is therefore
   unreachable, and `MEDIC_TYPES` (doctrine.py:270) excludes turrets anyway.
2. **`_sabotage_prio` returns False unconditionally.** It ranks GUNNER and
   SENTINEL at priority **0** (main.py:504-506) — i.e. the tree already *wants*
   to peck turrets first — and then main.py:517-518 reads
   `if LOKI_QUIET_ON: return False`, with `LOKI_QUIET_ON = True`
   (doctrine.py:1488, *"no builder melee: no core peck, no siphon hit, no
   counterbattery"*).

⇒ **The control arm's finish-fire count is 0 by construction, on two
independent gates.** That is the DOSE line's control value and it is a structural
fact, not an estimate.

**THE SHIPPED `pr=3` AT `raid.py:616` IS A DIFFERENT CALL SITE AND DOES NOT
DELIVER THIS.** It sits in the RAID layer, in the ENEMY half, and it is reached
only through `_raid`, i.e. **only for `self.role == "raid"` builders — which
main.py:422 explicitly EXEMPTS from this entire block.** `raid.py:256` and
`raid.py:334` show the same file's melee is itself `LOKI_QUIET_ON`-gated. The two
sites cannot both fire for the same unit on the same round.

### 4.3 ⛔ THE MOTIVATING ANECDOTE IS **NOT** COVERED BY THIS HUNK — disclosed here, not discovered later

`doctrine.py:176-182` records the case this plank is named after: enemy sentinel
#446 ground to **4/40 HP**, and *"we then kept a living builder at **dist^2 = 2**
from it for the next 283 rounds without ever attacking it once."*

**`d² = 2` IS DIAGONAL.** A sentinel is a 1×1 building, and a builder attack
requires an **orthogonally** adjacent tile. **A builder at d²=2 cannot attack that
turret at all**, this round or any round, without first taking a MOVE — and
because acting and moving are mutually exclusive for a builder, the heal that
claims the action also blocks that move. **So the canonical anecdote needs
heal-exemption PLUS a one-step approach, and this hunk delivers only the first
half.**

**Why the approach step is NOT in this arm:** choosing which of the ≤2 orthogonal
tiles adjacent to the turret to step onto, what to do when both are occupied,
whether to hold the tile once there, and how that interacts with `_nav`'s
existing target, are **design decisions the spec at doctrine.py:169-253 leaves
open** — and open design decisions are exactly what made the parent row NOT
DRAFTABLE at the enemy ring. Adding them here would reproduce that failure.

⇒ **THIS SCREEN MEASURES THE `d² = 1` CASE ONLY.** The §8 probe reports the
`d²=1` and `d²=2` populations **separately** and therefore prices the approach-step
follow-up before anyone builds it. **If the population is overwhelmingly
diagonal, this arm is near-inert and the probe will say so before 5400 cores are
spent.** That is the single largest risk on this page.

### 4.4 The nearest neighbours, named so nobody conflates them

* **`IDLEPECK` / `_v208idlepeck`, `_v210idlepeck2` (QUEUE #48).**
  `bots/_v210idlepeck2/doctrine.py:1490-1498`: *"terminal-idle raiders reopen the
  core peck"* — a **RAIDER**, in the **ENEMY** half, against the **enemy CORE**,
  triggered by `LOKI_IDLE_PECK_RNDS=8` consecutive actionless rounds. Different
  role, different half, different target, different trigger. **Not a duplicate.**
  ⛔ **Its shard result was NOT read by this agent**: `scratchpad/overnight/IDLEPECK.tsv`
  has **no `.COMPLETE` marker** (950 rows against a 5400 target), and this repo's
  rule is that a markerless shard may not be pooled. It is named as a behavioural
  neighbour and as **nothing else**; no direction prior is taken from it.
* **`SCREEN-sentthreat-2026-08-14.md` (QUEUE #30), LOCKED and RUNNING.**
  ⛔ **NOT A DUPLICATE, and the check was made at the code level.** Its sole hunk
  is `raid.py:753-776`, inside `_raid_station`, and it changes **which station a
  raider stands on** by adding SENTINEL to an *avoidance* set. It contains no
  attack, no heal-ordering change, and touches neither `main.py` nor the home
  band. **This arm changes what a HOME builder does with its ACTION; that arm
  changes where an ENEMY-HALF raider PUTS ITS BODY.** Disjoint files, disjoint
  roles, disjoint halves. Full interaction declaration in §9.

---

## 5. CLUSTER ENUMERATION (CLAUDE.md scope procedure, performed in writing)

**Clusters this data has: MATCH and OPPONENT.**

1. **MATCH.** ⛔ **DEAD.** A local corefill row is ONE GAME
   (`overnight.sh:139` and `:155` each write exactly one row per `fcode run`). There is no
   5-game match object on this surface, so a stratum cannot hold two members of a
   match cluster — there is nothing to hold.
2. **OPPONENT.** ⛔ **DEAD.** There is exactly ONE opponent for the entire shard:
   the frozen tree `bots/_v223sealrepair`. A cluster with one member across the
   whole sample contributes no between-cluster variance.

⇒ **Surviving clusters: none. Applicable DEFF = 0.98** (local, measured
pair-weighted, ρ = −0.020 across 124 shards, s39 audit). ⛔ **The platform
constants (1.529 rated / 1.833 unrated) are NOT applied**: doing so would widen
every interval on this page by 24–35% for correlation that is not present, and
per `CLAUDE.md` **over-correction is an error in the same family as
under-correction** — it fails in the FLATTERING direction for the fail-to-exclude
half of §7.

**Half-widths at 0.98, recomputed here rather than copied:** n=1000 → ±3.10pp ·
n=2700 → ±1.89pp · n=5400 → ±1.33pp.

---

## 6. HYPOTHESIS, GATES AND THE DECISION RULE

### ⚖ RATIFY — HYPOTHESIS (one sentence, falsifiable)

**Letting a home builder spend its action finishing an orthogonally adjacent
enemy turret at ≤8 HP whose ray does not cover that builder's tile — instead of
taking the universal Core heal that currently claims the action and ends the turn
— raises v140's game share against itself above 51.33% at n=5400 on the local
15-map pool, WITHOUT raising the median kill round.**

### ⚖ RATIFY — EXPECTED DIRECTION (pooled)

**Treatment share ABOVE 50.0. INSIDE THE BAND IS THE MODAL OUTCOME** and is
pre-typed as a DROP, not as a null to be argued with: the trigger is a narrow
conjunction (§8), and a rare mechanism with a real per-occurrence value still
pools to a share this fixture cannot resolve.

### Fixture

`tools/overnight.sh FINISHHP bots/_v242finishhp bots/_v223sealrepair 5400 322000`
— 15 maps × 2 seat orders, `--tle 10`, `--replay /dev/null`, seat-balanced by
construction, resumable, `.COMPLETE` marker required before any pooled read.

### GATES

| n | gate | action |
|---|---|---|
| 1000 | share ≤ 47.9% (≤479/1000) | **FUTILITY DROP** — publish label, n, share; no mechanism claim |
| 2700 | share ≤ 48.1% (≤1299/2700) | **FUTILITY DROP** — same |
| 5400 | final | decision rule below |

### ⚖ RATIFY — DECISION RULE

* **KEEP (promote to a D26 replication, NOT to a ship):** final share **≥ 51.33%**
  (≥ 2772 of 5400) **AND** the kill-round rider in §7 passes as an exclusion.
* **REAL NEGATIVE (road closes):** final share **≤ 48.67%** (≤ 2628 of 5400) —
  the finish-peck is measurably worse than the heal it displaces, and QUEUE #2
  closes on the home-siege re-scope as well as on the enemy ring.
* **DROP BAND (explicit): final share strictly inside 48.67%–51.33% (2629–2771
  of 5400).** ⛔ **This reads "COULD NOT SEPARATE", NEVER "the effect is zero".**
  The band is ±1.33pp wide and a true effect of, say, +0.8pp lives entirely
  inside it. **UNRESOLVED defaults to the RESTRICTION**: the shipped heal-first
  ordering stays, the arm is not promoted, and per §9 the row closes rather than
  re-running at a larger n.
* **A KEEP that fails the §7 rider is NOT a keep.** It is off-programme whatever
  it does to share.

---

## 7. THE KILL-ROUND RIDER (defence bar, scored as an EXCLUSION)

**This plank is DEFENCE and therefore carries the bar.** `PROGRAMME.md`'s
`PLAY_DEFENCE: not_at_the_kill_s_expense` and
`DEFENCE_ADMISSION_BAR: kill_round_non_regression` bind. `R1000_IS_DEFEAT: yes`
is unconditional and no tiebreak improvement counts for anything on this page.

**The specific hazard, named:** a builder that pecks is a builder that has not
moved and has not healed. Under siege that is one fewer body on the trunk and one
fewer +4 HP on the Core.

⭐ **The structural fact that BOUNDS the hazard, and it is why the bar is
plausibly passable:** main.py:422 exempts `self.role == "raid"` from this entire
block (`LOKI8_RAIDERS_STAY_OUT`). **The bodies this plank can spend are expanders
and defenders — NEVER raiders.** Our kill is delivered by the raid layer, so the
plank cannot take an action away from the units that produce kill round. **This is
an argument, not a measurement, and the bar is carried regardless.**

**⚖ RATIFY — THE RIDER:** the arm passes iff the **95% CI on Δ median kill round
(treatment − control), paired by seed, EXCLUDES +10 rounds** — +10 ≈ **+5.7% of
our 174-round median kill** (us-only, `CLAUDE.md`). Read off the shard's own
`turns` column on `cond == core_destroyed` rows.

⛔ **RESTATED AS AN EXCLUSION BEFORE ANY DEFF IS APPLIED**, per `CLAUDE.md`'s
direction clause. *"No significant rise in kill round"* is a **fail-to-exclude**
claim, and widening an interval makes that class of claim EASIER — a DEFF applied
to the unrestated form would launder a weak null into a confident one. **The bar
above is already the exclusion form: the CI must EXCLUDE the +10 regression.**
Applicable DEFF is 0.98 (§5).

**UNRESOLVED ⇒ RESTRICTION.** If the CI cannot exclude +10 at the achieved n, the
rider does **not** pass, and an above-band share does **not** promote the arm on
its own. ⚠ **This document does NOT assert the rider is resolvable at n=5400** —
that depends on the sd of kill round, which cannot be known before the control
rows exist. **The lane computes it from the control arm's own `turns` column at
the 1000-game gate and, if the CI half-width then exceeds 10 rounds, records the
rider as UNRESOLVED-BY-DESIGN at that point rather than at the end.**

⛔ **THE CONDITIONING TRAP, named before the read.** *Median kill round GIVEN a
kill* moves when **which games end in a kill** changes, with nothing getting
faster or slower. ⇒ **the rider is reported as a pair — P(core-kill win) AND
median-kill-round-given-a-kill, both arms, with both kill counts — or it is not
reported.**

---

## 8. ⛔ THE DOSE GATE — **ANSWERED DURING DRAFTING, AND IT RETURNS `DO NOT FIRE`**

### 8.0 ⛔⛔ THE HEADLINE: THE MEASURED DOSE IS **BELOW THE FLOOR THIS DOCUMENT REGISTERED BEFORE SEEING IT**

**The gate in §8.2 was written, and its floor of 0.50 finish-fires/game fixed, BEFORE any
measurement existed.** While this document was being drafted, a **separate,
independently-tasked opus subagent** reconstructed **per-round position and HP for every
entity** across **571 archived v140 games / 151,442 rounds** by replaying the raw
`replay_archive/*.replay26` update stream with the shipped primitives
(`tools/corpus/replay_census.py`, `tools/corpus/replay_autopsy.py`,
`tools/replay_schema.md`'s `UpdateHp` / `MoveBuilderBot` / `PlaceEntity` / `RemoveEntity`).

**That measurement answers the gate directly, at n=571 games rather than the ~180 the probe
would have bought, and with cross-surface and inverted controls the probe would not have had.**

| reading (571 v140 games, 151,442 rounds) | rounds | **per game** | games ≥1 |
|---|---|---|---|
| **The trigger, exactly as this arm hunks it** — enemy GUNNER/SENTINEL alive, **HP ≤ 8**, at **d²==1** from a living builder of ours | 211 | **0.370** | **81 / 571 = 14.2%** |
| **…AND the builder inside `near_home` (main.py:414's own predicate, d²≤25 of our core)** — i.e. what main.py:420 actually gates on | 124 | **0.217** | **65 / 571 = 11.4%** |

⇒ **`0.217` fires/game against a registered floor of `0.50`. The gate's own lower branch
fires: DO NOT RUN THE 5400-GAME SCREEN.**

⚠ **AND 0.217 IS AN UPPER BOUND, not a point estimate of fires.** The measuring agent did
not track `SetActionCooldown`, so an unknown fraction of those 124 rounds have the builder
on cooldown and unable to attack at all. **The true fire rate is ≤ 0.217/game.**

⛔ **THE FLOOR IS NOT MOVED.** It was set blind in §8.2 and it stays exactly where it was
typed. Moving a gate after seeing the number it was built to judge is the failure this whole
document exists to avoid.

### 8.1 THE SHARPEST SINGLE FACT — the best case in the entire corpus is OUTSIDE the band this hunk fires in

Read off the wire, `a5d9fa2b-2a66-4141-a4da-726d6f38e0be_game_3.replay26` vs **HTTP 418**:
enemy **gunner id=160 at (7,7), HP=6, from r68 through r142 — at least 74 consecutive
rounds** — with our builders (ids 7, then 5) repeatedly standing **orthogonally adjacent** at
(7,8) and (8,7), never finishing it. **Three attacks, 6 Ti, would have killed it.**

⛔ **Its d² to our core's NW corner is 29. `near_home` is `<= 25` (main.py:414). THE HUNK
REGISTERED IN §3 WOULD NOT HAVE FIRED ON IT.**

**That is a finding about the FORM this plank was handed in, not about the plank's idea.**
The tree already carries `HUNT_BAND_DSQ = 41` — the only hunt constant that is actually
**read** (3 sites, §4.2) — and 41 covers d²=29 comfortably. **The band this arm inherits from
the heal guard is the wrong band for the mechanism, and the corpus's single best exemplar is
the proof.**

### 8.2 ⚖ RATIFY — THE GATE (unchanged, quoted as registered, now with its verdict)

**Floor as registered, before the measurement:** ≥ **0.50** finish-fires/game ⇒ fire the
5400-game screen; < 0.50 ⇒ **DO NOT FIRE**, `#2` closes **PREMISE-THIN at the home band too**,
matching its enemy-ring verdict.

**Where 0.50 came from, as typed before the number arrived:** a finish is worth roughly
4 pecks × 2 Ti = 8 Ti and removes a shooter worth 7–18 damage per reload for the rest of the
match; 0.5 fires/game is the floor below which a ±1.33pp fixture is being asked to see an
effect that occurs in a minority of its own rows. **It was, and remains, a judgment line.**

| gate branch | measured | verdict |
|---|---|---|
| ≥ 0.50 fires/game | — | not reached |
| **< 0.50 fires/game** | **0.217 (≤, cooldown unmodelled)** | ⛔ **DO NOT FIRE. `#2` closes PREMISE-THIN at the home band.** |

**⚖ THE LANE'S DECISION, and it is the one thing on this page that is genuinely open:** the
gate is a **GATE, not a VETO**. A lane that judges 0.217/game worth 5400 cores may overrule it
— but it must do so **in writing, naming that it is overriding a pre-registered floor with the
number in hand**, which is a different and much weaker act than clearing it.

### 8.3 WHAT THE MEASUREMENT SAYS ABOUT THE THREE KNOBS — the only route to a dose above the floor

Each of these is a **design decision the spec at doctrine.py:169-253 leaves open**, which is
exactly what made the parent row NOT DRAFTABLE at the enemy ring. **They are named here as
priced follow-ups, and NOT smuggled into this arm.**

| knob | measured effect | cost |
|---|---|---|
| **Drop `near_home` (d²≤25) for `HUNT_BAND_DSQ` (d²≤41)** | 0.217 → **0.370** rounds/game, 11.4% → **14.2%** of games. Recovers the §8.1 exemplar. | changes the guard at main.py:420, which also governs the heal — **not a free change** |
| **HP threshold 8 → 12** | 211 → **296** rounds (+40%), 14.2% → **16.6%** of games. 8 → 4 halves it (120 rounds). **The threshold sits on a steep part of the curve.** | one constant, but `HUNT_FINISH_HP=8` is doctrine's own number and untested |
| **Add the one-step approach (§4.3)** | union with orthogonal: **808 rounds, 26.4% of games** — an upper bound of **~3.8×** the reachable dose — **before** paying the move-vs-act exclusivity, which the measurement does not model | the largest design surface: which tile, what if blocked, hold or not |

⇒ **Even all three together are an upper bound of ~26% of games at ~1.4 rounds/game.** This
mechanism is real, it is rare, and **no arrangement of these knobs makes it a comfortable fit
for a ±1.33pp pooled fixture.**

### 8.4 THE DIAGONAL SPLIT — §4.3's warning, now measured

| | rounds | per game | games ≥1 | distinct turrets |
|---|---|---|---|---|
| d² == 1 (orthogonal, **attackable**) | 211 | 0.370 | 81 (14.2%) | 109 |
| d² ≤ 2 (incl. diagonal) | 497 | 0.870 | 127 (22.2%) | — |
| **d² == 2 with no d²==1 pair that round (diagonal-only, NOT attackable)** | **286** | 0.501 | 98 (17.2%) | 123 ever-diagonal |

**57.5% of the d²≤2 population (286/497) is diagonal-only** — the majority class, and the
class the motivating anecdote belongs to (§4.3).

⛔ **BE PRECISE: this does NOT trip falsifier 2, which was pre-registered at ≥80% diagonal-only.
It measured 57.5%.** The arm fails on the **absolute dose floor**, not on the diagonal share,
and conflating the two would be claiming a falsifier fired when it did not.

### 8.5 CONTROLS — every one was driven to the other verdict

| control | result | what it establishes |
|---|---|---|
| d² == 0 pairs (bodies cannot co-occupy) | **0 / 151,442 rounds** | must be zero; is |
| **HP predicate INVERTED** (HP > 8, same geometry) | **20,977 rounds, 36.737/game, 502/571 games** | **99× the treatment — the HP filter, not the geometry plumbing, is what selects.** This is the DOSE line's other verdict |
| any-HP adjacency (no HP filter) | 21,171 rounds | treatment is 1.0% of it |
| **team flipped** (OUR turret ≤8 HP adjacent to THEIR builder) | **1,032 rounds, 1.807/game, 31.5% of games** | 4.9× our side — non-degenerate, and a separate finding: **the field gets this opportunity against us far more often than we get it against them** |
| kind swapped (enemy *conveyor* at d²≤8) | 302 vs 582 for turrets | different |
| **HP-tracker positive control** — the engine re-emits `placeEntity` on rotate, restating current HP | **0 disagreements in 2,852 re-emits** | the HP reconstruction matches the engine's own statement of HP |
| **HP-at-removal physics** | **1,516/1,800 (84.2%) at HP ≤ 0**; residual = 180 at exactly 25 (gunner max) + 94 at exactly 40 (sentinel max) = never-damaged removals (the crash/destroy class `tools/crash_census.py` names) + 10 damaged-but-alive | no removal at a nonsense HP |
| cross-surface | `corpus/events.tsv`, `corpus/builds.tsv` and a fresh raw parse agree **digit-for-digit**; two independent scripts both returned 211 ortho rounds | |
| population mapping | `meta_join.us_side` → team agreed with `join.tsv.our_team` in **3,645/3,645** rows; `ourver` **3,645/3,645** | the 571-game v140 population is not a mis-join |

### 8.6 ⛔ INSTRUMENT ALARM — THE RELAYED Q1 FIGURES DO NOT RECONCILE

The brief relayed **0.856/game** (enemy turrets at d²≤8 of our core) and **2.214/game**
(d²≤41) over 571 archived v140 games, flagged as unverified by the relaying agent. **The
independent read over the same 571 games returns 1.019 and 3.047**, agreeing digit-for-digit
across **three surfaces** (`corpus/events.tsv` BUILD rows, `corpus/builds.tsv`, and a fresh
raw `.replay26` parse: 582 and 1,740 events).

Seven readings were enumerated rather than a substitute invented. **None reproduces the
relayed pair:**

| variant | d²≤8 | d²≤41 |
|---|---|---|
| enemy builds, core = NW corner (**the corpus convention**, and what `ct.get_position(core)` returns) | **1.019** | **3.047** |
| enemy builds, core = nearest 2×2 footprint tile | 1.287 | 3.142 |
| enemy turrets **alive at end of game** | 0.658 | 1.928 |
| enemy turrets, **max simultaneously alive** | 0.806 | 2.282 |
| **OUR turrets near THEIR core (team-flipped)** | **0.867** | **2.299** |
| ladder-only subset (n=120) | 1.125 | 3.350 |
| unrated-only subset (n=451) | 0.991 | 2.967 |

The relayed pair sits nearest the **team-flipped** and **max-simultaneously-alive** reads but
equals neither; both relayed values are also exact over a denominator of **500**, not 571.
**This is reported as UNRECONCILED, not diagnosed.** ⛔ **Per the pinned-triple rule, a
disagreeing decode is an INSTRUMENT ALARM: do not read that cell until the sibling's filter is
handed over and checked for whether it tests `d2_own` or `d2_enemy`.**

⚠ **It does not change this document's verdict.** Both readings describe *turret presence in
a band*; neither is the trigger, and the trigger was measured directly at 0.370 / 0.217.

### 8.7 THE INSTRUMENT, for the record — and why the shard TSV could never have been it

⛔ **`scratchpad/overnight/*.tsv` carries `ts shard game map seed seat winner cond turns` and
the runner uses `--replay /dev/null` (`overnight.sh:135-136`). There is NO mechanism column and
no replay to decode. The screen shard could NEVER have read this metric** — which is why it was
registered as a separate probe, and why an archive measurement was able to pre-empt it.

* ⛔ **The derived corpus TSVs cannot do it either:** `events.tsv`, `builds.tsv`, `econ.tsv`,
  `flow.tsv`, `throws.tsv` and `build_agg.tsv` carry **no HP column and no per-round
  position** (all six headers checked). **`replay_events.py:92-99` tracks positions internally
  and writes no position row**, which is why §8.7's method had to go to the raw archive.
* ⭐ **The raw `replay_archive/` CAN**: `tools/replay_schema.md` documents `UpdateHp{id,delta}`,
  `MoveBuilderBot{id,to}`, `PlaceEntity{Entity{hp,pos}}` and `RemoveEntity{id}`. **571 replays
  parse in ~12 s.** This is now a demonstrated capability of this repo and should not be
  re-derived.
* ⛔ **DO NOT PLAN TO READ OUR OWN `print()`.** It survives locally and is **stripped from
  platform-downloaded replays**; the engine-side entity events above are the durable
  instrument, and they are what was used.

### 8.8 CAVEATS ON THE MEASUREMENT ITSELF, carried rather than dropped

1. **End-of-round snapshot only** — the finest granularity the wire format has. Whether the
   turret crossed ≤8 HP before or after our builder's own turn within round *r* is not
   recoverable. A trigger at end of *r* is the state units see on *r+1*.
2. **Cooldown not modelled** (`SetActionCooldown` is on the wire, field 7, untracked) ⇒
   **0.217 and 0.370 are UPPER BOUNDS on actionable triggers.**
3. **Clustering: both the MATCH and OPPONENT clusters are LIVE for this cut** — 571 games =
   119 matches, 23 opponents, and a stratum holds many of each. ⇒ **the pooled platform DEFF
   applies here (1.833 unrated; the pool is 79% unrated), NOT the local 0.98.** For the 14.2%
   game incidence: naive ±2.9pp, **DEFF-corrected ±3.9pp**; effective n ≈ 310–370 of 571.
   ⛔ **This is the opposite call from §5, and correctly so** — §5 governs the *screen shard*
   (one frozen opponent, one game per row, both clusters dead); this governs an *archive cut*
   over real opponents. **Naming the surface is what keeps the two from being confused.**
4. **Pooled fixture:** 120 rated ladder + 451 unrated. Fine for a mechanism-occurrence count;
   **not** a rated-record denominator, and not quoted as one.
5. **Opponent spread** (ortho trigger rounds · games with ≥1 / games): 0033 43 · 5/70 ·
   HTTP 418 33 · 6/20 · team lazy 31 · 13/60 · lingling_40h 19 · 8/65 · Jython 14 · 7/40 ·
   Erebus 14 · 8/30 · The Bisons 12 · 4/15. **Four opponents (sporks, not adgato, arsonist
   duck, Askar City — 35 games) produced ZERO.** **Heavily tailed: the top 2 games carry
   61/211 = 28.9% of all trigger rounds.** ⇒ **even conditional on the mechanism existing, its
   value is concentrated in a handful of games**, which is a second, independent reason a
   pooled ±1.33pp screen is the wrong instrument for it.

---
## 9. COUPLING CLASS, INTERACTIONS, AND WHAT THIS SCREEN MAY CONCLUDE

**COUPLING CLASS: SELF-KNOWLEDGE / FIELD-EXPRESSED — with a DECLARED FIXTURE
BIAS.** The heal ordering is ours; the besieging turret is a standard league
building our own control builds. ⇒ a local shard is the right first instrument.
⛔ **But §8.1's asymmetry (we do not heal our own besieged turrets; the field
does) means the local dose is BIASED UPWARD.** **A local KEEP buys a live
confirmation, never a ship.**

### ⚠ INTERACTION with the locked-and-RUNNING `sentthreat` arm (required declaration)

**`SENTTHR` — `bots/_v241sentthreat` vs `bots/_v223sealrepair`, LOCAL, target
5400, seedbase 314000** (`scratchpad/corefill_work.txt`).

* **SAME SUBSYSTEM CLAIM, EXAMINED AND REJECTED AT THE CODE LEVEL.** Both rows
  descend from "our bot mishandles enemy SENTINELs", but the diffs are
  **disjoint**: `sentthreat` is one hunk in `raid.py:753-776`
  (`_raid_station`, enemy half, raider role, *avoidance*); `finishhp` is
  `main.py:420-424` + a new `main.py` method + one `doctrine.py` line (home band,
  **raiders explicitly EXEMPT** via main.py:422, *attack*). **Neither arm
  contains the other's change and neither can execute for the same unit on the
  same round**, so there is **no statistical interaction between the two
  contrasts**; each is measured against the same frozen control.
* **⛔ THE REAL COLLISION IS THE PRIMARY SEGMENT: both declare the SAME 5
  900-area maps.** That is not a confound (separate shards, separate contrasts)
  but it **is** a multiplicity problem for the *programme*: two arms testing the
  same segment double the chance one clears it by noise. **⇒ NO COMBINED
  ON-SEGMENT CLAIM may be made from the two shards read together, and if BOTH
  clear on-segment while BOTH fail pooled, that is one hypothesis to test at a
  new n, not two confirmations.**
* **ALLOCATION, not design:** both draw from the same local core pool, and
  `SENTTHR` was registered first. ⇒ **the §8 probe (~180 games) is affordable
  alongside it; the 5400-game screen is a scheduling decision for the builder.**
* **Seedbases are disjoint:** 314000 (span 314000–314337) vs **322000** (span
  322000–322337). Verified in §12.

### NOT LICENSED by this screen

* **No ship implication.** `SHIP_SIT` governs; v140 is sitting. An above-band
  final buys a D26 replication and a live read, not an activation — and §8.1's
  fixture bias is the specific reason.
* **⛔ NO ECONOMIC CLAIM, in either direction.** Destroying an enemy building
  **lowers their cost scale and helps them**, and a turret is the largest
  per-entity contribution (+20%). The value claimed here is **tactical only**.
  Any write-up that credits this plank with a titanium or scale benefit is
  wrong on the engine.
* **No claim about the HP threshold.** `HUNT_FINISH_HP = 8` is used as written
  in doctrine.py:214 and is **untested**. A null here closes the *wiring*
  question at threshold 8; it does not close the threshold question.
* **No claim about `DUEL_DISCIPLINE_ON`'s ray test.** ⚠ **And this is a live
  doubt, registered now:** for a ≤8 HP turret the duel arithmetic does not
  obviously require the ray check — 4 pecks kill it, over which a sentinel
  (reload 2) lands ~2 shots for 36 damage against a 40 HP builder and a gunner
  (reload 1) ~4 shots for 28. **The ray check is the dose-REDUCING choice and it
  is registered as specified in the brief, not as a derived optimum.** Because it
  is gated on the existing `DUEL_DISCIPLINE_ON`, the ray-check-off variant is a
  **one-constant flip, not a new tree**, and it is the pre-declared FIRST
  follow-up if the §8 probe reads thin for facing reasons.
* **No claim about the approach step (§4.3)**, `HUNT_MIN_HEALERS`, the
  designation ballot, or `HUNT_DEFER_*`. Those remain unwired spec after this
  screen whatever it returns.
* **No combo claim** with `SENTTHR`, `SEALFLOOR6`, `SALTREF2` or any other arm.

### ⛔ WHAT IS LOST IF THE LANE KILLS THE ROW INSTEAD (so the choice is informed)

Killing `#2` here forfeits: (a) the only cheap test of whether **any** builder
melee is worth an action in the home band — a question `LOKI_QUIET_ON` closed
globally in the enemy half and **never tested at home**; (b) the §8 probe's
per-map trigger table, which is the only route to pricing the approach-step
follow-up; and (c) nothing else. **The doctrine defect survives either decision
and should be fixed regardless:** `doctrine.py:169-253` reads as present-tense
description of shipped behaviour, names a function that does not exist, and a
lane grepping `HUNT_FINISH_HP` today is told this bot finishes besieging turrets.
**It does not.** That relabelling is a documentation deliverable independent of
this screen.

---

## 10. FALSIFIER

**⚖ RATIFY — the hypothesis (§6) is falsified by any of:**

1. ⛔ **ALREADY FIRED — a dose reading below 0.50 finish-fires/game (§8.2).**
   **MEASURED at 0.370 ungated / 0.217 near_home-gated, both upper bounds, over
   571 games.** The branch does not get enough chances to matter; **the screen is
   NOT fired and `#2` closes PREMISE-THIN at the home band.** *(A falsifier of the
   PLANK's screenability, NOT of the code fact in §4.2 — the mechanism is still
   unwired and the doctrine block is still wrong. The two must not be conflated in
   the write-up.)*
2. **NOT FIRED — a population ≥80% diagonal-only (§8.4).** **MEASURED at 57.5%
   diagonal-only.** Majority-diagonal, and the motivating anecdote is in that
   class, **but the pre-registered 80% line was not crossed and this document does
   not claim it was.**
3. **A final ≤ 48.67% (≤2628/5400)** — finishing the turret is measurably worse
   than the heal it displaces. **REAL NEGATIVE; the road closes.**
4. **A futility drop at either gate** (≤479/1000 or ≤1299/2700) — not worth more
   cores; no mechanism claim is made at that resolution.
5. **A final inside the band (2629–2771)** — not supported at ±1.33pp. **This is
   the modal outcome and it is pre-typed as a DROP, not as a null to be argued
   with.**
6. **The kill-round rider failing to exclude +10 rounds (§7)** — the arm buys
   removal of a shooter at the kill's expense and is off-programme whatever it
   does to share.
7. **CPU FALSIFIER (§3.4): a rise in `NOWINNER` rows, or a rise in mean `turns`
   concentrated on the 5 900-area maps with no matching rise on the 10 smaller
   maps** — the branch is costing turns to truncation on the maps with 87% of
   budget already spent, and the arm is a budget failure wearing a plank's
   clothes. **Reported before any share verdict, because it changes what the
   share MEANS.**
8. **A probe showing enemy-turret-adjacent deaths at control level, or total
   enemy turret deaths FALLING in the treatment** — the instrument is wrong or
   the diff is not the diff described. **No share reading may be read either
   way.**

**⚖ RATIFY — the PRIMARY SEGMENT prediction is falsified** if the treatment's
share on the 5 900-area maps is **≤** its share on the 10 ≤676-area maps
(§2, "the segment sign is argued, not measured").

---

## 11. OBLIGATIONS REGISTER

| obligation | discharge |
|---|---|
| **Two-clock lock** | §STATUS — git author time of this file vs `overnight.sh:96`'s `start=` stamp in `FINISHHP.tsv`. No shard row exists at commit. |
| **7 — pre-state** | §2 `PRE-STATE:`, evidenced by the grep table in §4.2 with `HUNT_BAND_DSQ` as the other-verdict control. |
| **12 — gate sized, default pre-committed** | §2 `GATE RESOLUTION:` and §6. **UNRESOLVED ⇒ RESTRICTION**, stated in both. |
| **13 — mechanism metric / diff intersection** | §2. Metric reads `main.py:423`; diff touches `main.py` + `doctrine.py`; **INTERSECTION: YES.** ⚠ Computable only once the tree exists — re-run with `--fire` after `git add -N`. |
| **14 — cell version churn** | **N/A** — no `CELLS:` line; this is a local shard against one frozen control, not a panel. |
| **15a — segment + direction** | §2 `MAP SEGMENT`, `PRIMARY SEGMENT`, `EXPECTED DIRECTION`. |
| **15b — exactly one primary** | One `PRIMARY SEGMENT:` declaration. All other cuts declared DESCRIPTIVE ONLY. |
| **15c — segment cannot rescue a pooled fail** | §2 and §10. |
| **Dose gate** | §8, both verdicts, with the behavioural half explicitly gated. |
| **BOUNDARY in both units** | §2. **Declared exemption:** the `games = 5 × accepts` identity is a PLATFORM identity; a local shard has no accepts. 1 row = 1 game. |
| **Defence admission bar** | §7, phrased as an EXCLUSION before any DEFF is applied. |
| **DEFF scope procedure** | §5, enumeration performed in writing, both clusters shown dead. |
| **Numbers carry subjects** | Every figure on this page carries its denominator, population and provenance; the relayed 0.856/2.214 carry their "unverified by the relaying agent" caveat at every use. |

---

## 12. WORKLIST ROW AND COLLISION CHECKS

**Row to append to `scratchpad/corefill_work.txt`** (the lane appends it; this
agent did not):

```
# FINISHHP (#2, re-scoped to the home siege band).  Wires the HUNT_FINISH_HP
# exemption at main.py:420 so a home builder finishes a <=8 HP adjacent enemy
# turret instead of taking the universal Core heal.  GATED on the ~180-game dose
# probe in docs/prereg/SCREEN-finishhp-2026-08-14.md section 8 -- DO NOT LAUNCH
# THIS SHARD UNTIL THE PROBE READS >= 0.50 finish-fires/game.
FINISHHP    bots/_v242finishhp     bots/_v223sealrepair   5400 322000
```

### ⛔ BASENAME COLLISION CHECK, BOTH DIRECTIONS

`tools/overnight.sh:154` scores the winner by **SUBSTRING** on the basename
(`case "$L" in *"$B"*) WIN=T`), and `overnight.sh:78` is the guard that refuses
the run, so a substring relation in **either** direction makes the
shard silently unscorable — every control win would read as a treatment win.

`B = _v242finishhp`, `C = _v223sealrepair`:

| test | result |
|---|---|
| `B == C` | **false** |
| `B == *C*` — is `_v223sealrepair` a substring of `_v242finishhp`? | **false** |
| `C == *B*` — is `_v242finishhp` a substring of `_v223sealrepair`? | **false** |

⇒ **PASSES `overnight.sh`'s guard in both directions.**

**Additional collision checks run this session:**

* `ls bots/ | grep -iE "finish|hp|peck|hunt"` → only `_v208idlepeck`,
  `_v210idlepeck2`. Neither contains nor is contained by `_v242finishhp`.
* `ls bots/ | grep -E "v242|v243|v244"` → **empty**; `_v242finishhp` is free.
* `ls scratchpad/overnight/ | grep -iE "finish|peck|hunt"` → `IDLEPECK.*` only.
  **No `FINISHHP.*` exists**, so the shard name does not clobber a live tape.

### SEED-BASE CHECK

`overnight.sh:121` advances `seed = SEEDLO + n/16` (and `:160` bumps it per map cycle), so a 5400-game shard spans
**⌈5400/16⌉ = 338 seeds: 322000–322337.**

* Highest seed base currently in `scratchpad/corefill_work.txt`: **314000**
  (`SENTTHR`, span 314000–314337). Next highest 312000 (`GUNAXABL`).
* **322000 clears 314337 by 7,663** and satisfies the brief's ≥322000 floor.
* **Next free base after this shard: ≥ 323000.**

---

## 13. ⚖ THE RATIFY LIST, gathered (the lane types these, not this agent)

1. ⛔ **THE ONLY LIVE DECISION: whether to OVERRULE the §8.2 gate**, which
   measured 0.217 against a floor of 0.50 fixed before the number existed. **A
   gate is not a veto — but an override is written down, with the number in hand,
   and is a weaker act than clearing it.** Everything below is conditional on that
   override; absent it, the screen is not fired and §12's worklist row is not
   appended.
2. **Whether the cheap follow-up is worth more than the screen**: swap the
   `near_home` d²≤25 band for `HUNT_BAND_DSQ = 41` (§8.1, §8.3) — the corpus's
   single best exemplar sits at d²=29 and this hunk cannot see it. **Measured lift:
   0.217 → 0.370 fires/game, 11.4% → 14.2% of games.** It touches the guard that
   also governs the heal, so it is not free.
3. **The Hypothesis** (§6).
4. **The Decision rule**, including the explicit DROP band (§6).
5. **The Falsifier list** (§10), including the CPU falsifier and the segment
   falsifier.
6. **The Segment** and its argued sign (§2) — and whether to let the probe
   replace the area proxy before firing.
7. **The dose floor of 0.50 finish-fires/game** (§8.2) — a judgment line.
8. **The kill-round rider at +10 rounds** (§7), and the instruction to declare it
   UNRESOLVED-BY-DESIGN at the 1000-game gate if its CI cannot reach that width.
9. **Whether to keep the `DUEL_DISCIPLINE_ON` ray test in the first arm at all**
   (§9) — it is registered as briefed and it reduces the dose.
