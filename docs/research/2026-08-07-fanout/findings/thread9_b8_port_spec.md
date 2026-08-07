# Thread 9 — B8 PORT SPEC (v79/v82 scaled threat sensing → Eir 2)

Read-only. Sources: `bots/opp_v58/main.py` (= x3r0 v82) read end to end,
`bots/opp_v56/main.py` (= v79) diffed against it, `bots/_v72e2/main.py` (= Eir 2,
live) read end to end, `docs/game-model.md`, `docs/v79-analysis.md`,
`docs/spitball.md`.

---

## 0. HEADLINE — the mechanical question, answered

**`gun_sense = 100` is not a sensing radius. Nothing in v79/v82 ever scans past a
unit's own vision. It is a *classification threshold measured from OUR CORE
ANCHOR*, applied to entities that a builder has already seen inside its own
r²=20 vision.**

The proof is three lines of v82, all in `_builder`:

- `bots/opp_v58/main.py:490` — `for eid in ct.get_nearby_entities():` — **no
  `dist_sq` argument**. Default = the caller's vision radius, i.e. r²=20 for a
  builder bot (`docs/game-model.md:202`).
- `bots/opp_v58/main.py:498` — `d = self.core.distance_squared(ep)` — the
  distance compared is **core→enemy**, not builder→enemy.
- `bots/opp_v58/main.py:508-512` — `gun_sense`/`b_sense` are compared against
  that `d`.

So the sensor is a *distributed net*: each builder contributes its own r²=20
observation disk wherever it happens to stand, and the tier decides how far from
home an observed enemy still counts as "we are UNDER attack". Raising 64→100
adds **zero engine calls and zero new observations** — it only reclassifies
sightings the bot already had and was throwing away.

Corollaries that matter for the port:

- The naive port (`ct.get_nearby_entities(dist_sq=100)` from a builder) is
  **wrong twice**: it cannot return anything outside vision anyway, and the
  documented behaviour of the sibling getter is to **raise** —
  `GameError: dist_sq exceeds vision radius` when `dist_sq` exceeds the caller's
  vision (`docs/game-model.md:418-420`; the string is present in the compiled
  engine, `fcode_engine.cpython-313-darwin.so`). Whether that check is applied to
  `get_nearby_entities` specifically is *measured only for `get_nearby_tiles`* —
  and it is moot, because the correct port never passes `dist_sq` at all.
- Raising the equivalent threshold on the **Core** would be a no-op. The Core's
  scan (`bots/opp_v58/main.py:309-323`, identical at `bots/_v72e2/main.py:580-594`)
  is vision-capped at r²=36, so its `d <= 64` gunner test is already
  non-binding; only its `d <= 16` builder test binds. The Core is a fixed r²=36
  sensor. **The builders are the only extensible sensor in the architecture** —
  which is exactly why v79 put the tier there and nowhere else.

Alarm-zone size, archipelago (26x26, anchors (5,5)/(19,19), from
`CORE_PAIRS`/`EXTRA_MAP_CODES` at `bots/opp_v58/main.py:69` and `:113-114`):

| anchor | turret zone 64 → 100 | builder zone 16 → 36 |
| --- | --- | --- |
| (5,5) | 159 → 213 in-bounds tiles | 49 → 111 |
| (19,19) | 181 → 242 | 49 → 113 |
| interior (lattice) | 197 → 317 | 49 → 113 |

One builder's own observation disk is 69 tiles (r²=20). Five builders can in
principle blanket the whole widened zone; in practice coverage is opportunistic,
which is the honest bound on how much the tier can buy.

---

## 1. v82 / v79: exactly where the tier enters and who consumes it

### 1.1 v79 == v82 for everything in this thread (confirmed)

`diff bots/opp_v56/main.py bots/opp_v58/main.py` is **one hunk plus the
docstring**: 5 added lines at `bots/opp_v58/main.py:949-953`, gated on
`600 <= area < 650 and mw == mh` (drumlin/hive) — archipelago is 676 and fails
it. `gun_sense`/`b_sense` sit at `opp_v56/main.py:508-509` and
`opp_v58/main.py:508-509`, byte-identical; `keep_artillery_forward` at
`opp_v56/main.py:660-681` and `opp_v58/main.py:660-681`, byte-identical. The
`docs/spitball.md:36-46` CORRECTED bullet is verified correct.

### 1.2 The tier itself

```
bots/opp_v58/main.py:499-509
    _midsq_far = 240 <= mw*mh <= 280 and mw == mh and core.x+core.y >= (mw+mh)//2
    _tiny_near = mw*mh <= 120 and core.x+core.y < (mw+mh)//2
    _boost     = _midsq_far or _tiny_near
    gun_sense  = 100 if (mw*mh >= 650 and mw == mh) else (81 if _boost else 64)
    b_sense    =  36 if (mw*mh >= 650 and mw == mh) else (25 if _boost else 16)
bots/opp_v58/main.py:510-515
    if (turret and d <= gun_sense) or (builder and d <= b_sense):
        write SLOT_UNDER=1 ; SLOT_ATK_RND=rnd ; SLOT_THREAT=pack(ep)
```

Note it is recomputed **per visible enemy entity**, inside the loop — wasteful,
and the loop has **no `break`**, so the last qualifying sighting in iteration
order wins `SLOT_THREAT`.

### 1.3 Which pool maps each tier fires on

Dimensions read from `maps/*.map26` headers (protobuf fields 1/2):
fjordgate 10x10=100 · moonrise 21x8=168 · antler 14x18=252 · jackpot 16x16=256 ·
lighthouse 16x16=256 · atoll 18x18=324 · meander 25x15=375 · nordkap 20x26=520 ·
eider 28x20=560 · heart 28x20=560 · saga 24x24=576 · drumlin 25x25=625 ·
hive 25x25=625 · **archipelago 26x26=676** · **snowflake 26x26=676**.

- `area>=650 ∧ square` (100/36) → **archipelago + snowflake, exactly**. Confirms
  `docs/spitball.md` and `docs/v79-analysis.md:95` (V8).
- `_boost` (81/25) → jackpot-B, lighthouse-B (the higher-anchor seat), fjordgate-A.
- everything else → 64/16, which is what Eir 2 uses everywhere
  (`bots/_v72e2/main.py:819-820`).
- `large_square` in `keep_artillery_forward` (`area>=600 ∧ square`) → drumlin,
  hive, archipelago, snowflake — **strictly wider than the sensing gate**.

### 1.4 `keep_artillery_forward` in v82 and its single consumer

```
bots/opp_v58/main.py:658-681
    tiny_arena   = area <= 120                         # fjordgate
    square_band  = 240 <= area <= 280 and mw == mh     # jackpot, lighthouse
    large_square = area >= 600 and mw == mh            # drumlin, hive, archi, snow
    keep_artillery_forward = tiny_arena or square_band or large_square
        or moonrise-A (21x8, core.x==5)
        or nordkap both seats (20x26 @ (9,6)/(9,18))
        or antler both seats (14x18 @ (6,4)/(6,12))
    # release valve: antler band (240-280 non-square) under UNDER with no home gun
    #                → keep_artillery_forward = False        (:675-681)
bots/opp_v58/main.py:682-694    # THE ONLY CONSUMER
    if role in ("saboteur","launchwait") and not keep_artillery_forward
       and p.distance_squared(core) <= 25:
           ... if an enemy builder is within core-dsq 20 → _home_defend(); return
```

i.e. it is a **suppressor of the near-core melee recall**. On a 676-tile square
their saboteurs never abandon the forward siege to answer a melee visitor.

### 1.5 Every downstream consumer of the widened UNDER/THREAT in v82

`SLOT_UNDER` reads: `:645` (rank2_hold gate), `:678` (kaf release valve),
`:784` (launchwait sabotage), `:827` (siege eco_need relax), `:950` (v82's new
hunk), `:1014` (nordkap-S walk-onto-gun-line), `:1030` (saboteur harvester
gate), `:1047` (`_deny_threat_tile`), `:1158` (`_try_rush_deny`), `:1207`/`:1233`
(bunker), `:1270` (`_defend`), `:1386` + `:1417` (`_expand` smash-adjacent-gun on
`area>600`, and heal-under-fire).
`SLOT_THREAT` reads: `:1016`, `:1049` (`_deny_threat_tile`), `:1063`
(`_try_counterbattery`), `:1275`→`:1326` (defender walks to the threat).
Core-side effects of UNDER: ammo target 16→32 (`:354-359`) and Ti floor 52→12
(`:360`).

**On archipelago specifically the chain is: builder sees enemy turret at
core-dsq ≤100 → UNDER latches for 50 rounds (`:333-335`) → core converts ammo on
a 12-Ti floor instead of 52 → `_expand`'s `area>600` branch (`:1385-1415`) smashes
adjacent rush guns → defender counterbatteries the published threat → and
`keep_artillery_forward` keeps the saboteurs forward the whole time.**

---

## 2. Eir 2: our equivalent paths

### 2.1 The sensing site (the thing to change)

```
bots/_v72e2/main.py:810-824      # _builder, per visible enemy entity
    d = self.core.distance_squared(ep)                          # :818
    if (turret and d <= 64) or (builder and d <= 16):            # :819-820
        SLOT_UNDER=1 ; SLOT_ATK_RND=rnd ; SLOT_THREAT=pack(ep)  # :822-824
```

Structurally identical to v82's `:498-515`; the literals `64`/`16` are the whole
delta. They are **not named constants** — no `grep`-able symbol exists. The Core
mirror at `:580-594` is fixed 64/16 and, as noted, vision-bound at r²=36.

Nothing else in the file uses 64/16 as a *threat* radius. Adjacent but unrelated
radii, listed so the port does not touch them by accident:
`:714` (`_sync_harvesters`, core-dsq 64 gate on harvester counting — **not a
threat radius**), `:1035`/`:1042` (melee recall, 25/20), `:1090` (`_home_defend`,
36), `HUNT_BAND_DSQ=41` (`:94`, `:1543`), `HUNT_DESIGNATE_DSQ=8` (`:147`,
`:1545`), `INTRUDER_CORE_DSQ=20` (`:81`, `:2081`), launcher 49/26
(`:2692`, `:2710`).

### 2.2 Every Eir 2 subsystem that would change behaviour, with lines

`SLOT_UNDER` consumers (all `read_store`):

| site | what it does | sensitivity to a wider gate |
| --- | --- | --- |
| `:991` **universal adjacent heal** | any builder beside a damaged Core heals it | **high** — this is the file's central reflex and it is *gated on UNDER*. Wider UNDER = more heals. Bounded by `can_heal` refusing full HP. |
| `:1011` `_rank2_hold` map gate | hive-A roles 1-3, **snowflake-B role 4** → walk home + heal, `link_queue` cleared | **high on snowflake** — one of the two target maps. Fires earlier and stays latched. |
| `:1135` `_launchwait` sabotage | free adjacent peck | low |
| `:1498` `_hunt_turret` core-siege mode | + round≥120 + `_core_shelled` | low (double-gated on real HP loss) |
| `:1746`,`:1751` `_defend` | `under`, and `shelled = under ∧ _core_shelled` | medium |
| `:1756`→`:1831` `_defend` threat chase | `tgt = threat; _nav()` | **highest regression risk** — see §5 |
| `:1989` `_expand` multi-healer convergence | role 2 / role ≥5 converge on the Core | medium (also needs `_core_shelled`, which needs the Core in r²=20 vision) |
| Core `:630-643` | `ammo_target` 16→24, `ti_floor` 52→12 | **this is the intended payoff** |
| Core `:604-611` | 50-round UNDER latch | amplifies every row above |

`SLOT_THREAT` consumers: `:1643` (`_try_counterbattery`), `:1756`→`:1831`
(`_defend` chase). Both take the published position at face value with **no
distance sanity check**.

### 2.3 What Eir 2 does NOT have (relevant deltas vs v79)

- `keep_artillery_forward` (`:1024-1034`) is v55-era: moonrise-A, nordkap both,
  antler both. **No `tiny_arena`, no `square_band`, no `large_square`, no
  release valve.** So on archipelago/snowflake our saboteurs *do* get recalled by
  the near-core melee rule at `:1035-1047`.
- No `_deny_threat_tile` (that is borrow B3, `docs/v79-analysis.md:370`).
- No `_try_rush_deny` / bunker table (B7).
- No `area>600` smash-adjacent-rush-gun branch in `_expand` (v82 `:1385-1415`).
  Our nearest equivalent is `_hunt_turret` (`:1457`), which is round-floored at
  120 (`HUNT_MIN_RND`, `:215`) and needs `_core_shelled`.
- Our counterbattery has an eco gate with a `_core_shelled` waiver
  (`:1650-1663`) that v82 lacks entirely.

---

## 3. THE SPEC

### 3.1 Phase 1 — faithful minimal port (the thing to build and measure first)

**State.** Two new instance attributes, computed **once**, in the
`if self.team is None:` init block of `_builder` (`bots/_v72e2/main.py:753-780`),
alongside the existing one-shot `self.melee_first` idiom (`:804-806`):

```python
# in __init__ (near :466 self.melee_first = False)
self.gun_sense = 64
self.b_sense = 16

# in _builder's team-init block, after self.mw/self.mh are set (:755)
_area = self.mw * self.mh
_big_square = _area >= 650 and self.mw == self.mh      # archipelago, snowflake
self.gun_sense = 100 if _big_square else 64
self.b_sense = 36 if _big_square else 16
```

Hoisting (v79 recomputes both per entity, `opp_v58:499-509`) is a deviation in
*form* only — the values are constant per unit per match — and it removes the
only measurable CPU cost of the port. **No store slot is needed.** No per-map
table, no `map_grid` dependency (unlike snowflake's `map_grid[0][0]` disambiguator
at `:1002`, the gate is pure dimensions, so it is safe before decode).

**Deliberately NOT ported in phase 1:** the `_boost` 81/25 middle tier
(`opp_v58:499-507`). It targets jackpot-B / lighthouse-B / fjordgate-A —
`docs/v79-analysis.md:391` records that we hold lighthouse and sweep fjordgate
32/32 *with* current behaviour. Porting it in the same change would confound the
archipelago read. One gate, two maps, one measurement.

**Edits.**

1. `bots/_v72e2/main.py:466` — add the two attributes to `__init__`.
2. `bots/_v72e2/main.py:755` (inside the `self.team is None` block) — compute the
   gate. `self.mw/self.mh` are already assigned on that line.
3. `bots/_v72e2/main.py:819-820` — replace the literals:
   ```python
   if (et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= self.gun_sense) or (
       et == EntityType.BUILDER_BOT and d <= self.b_sense
   ):
   ```

Total diff: **~8 lines, 3 sites, one function touched.** Everything else in the
file consumes the effect through `SLOT_UNDER`/`SLOT_THREAT` unchanged.

### 3.2 Phase 1b — the threat-write fix that the widening *requires*

`:810-824` writes `SLOT_THREAT` for **every** qualifying sighting with no `break`
and no ordering; last write wins. At `gun_sense=64` the candidates are all
within 8 tiles of home and roughly interchangeable. At 100 on a 676-tile board a
distant, unanswerable sentinel can overwrite a near, actionable one every round,
and store writes are buffered (`docs/game-model.md:386-388`) so no unit can see
another unit's write within the round — a cross-unit priority rule is
impossible. The fix is per-unit and free:

> Collect qualifying sightings in the loop; after the loop write **one**
> `SLOT_THREAT` — the sighting with the smallest `core.distance_squared`.
> Keep `SLOT_UNDER`/`SLOT_ATK_RND` written as soon as any sighting qualifies.

Cost: one list, one `min()`, ≤8 elements. This is a deviation from v79 (which has
the same flaw), justified because Eir 2 has *more* threat consumers than v79 and
because widening the radius is exactly what makes the flaw bite.

### 3.3 Phase 2 — `keep_artillery_forward`, NARROWED (separate measurement)

`docs/spitball.md:42-45` names `keep_artillery_forward` as the second half of
what owns archipelago. `docs/v79-analysis.md:389-391` says **do not borrow V13**,
because the v79 form (`large_square = area>=600 ∧ square`) also covers hive
(we sweep 32/32) and drumlin, plus `square_band` covers jackpot/lighthouse.

**Both are right; the resolution is to gate it on the same predicate as the
sensing tier, not on v79's wider one.**

```python
# bots/_v72e2/main.py:1024-1034, add one clause:
keep_artillery_forward = (
    (self.mw * self.mh >= 650 and self.mw == self.mh)   # archipelago, snowflake ONLY
    or (self.mw == 21 and self.mh == 8 and self.core.x == 5)
    or ...unchanged...
)
```

`>=650` (not `>=600`) leaves hive/drumlin/saga/jackpot/lighthouse and the melee
recall on them **bit-for-bit untouched**, which is precisely the objection in
`v79-analysis.md:389-391`. Ship and measure this **after** phase 1 lands, so the
sensing effect and the recall-suppression effect stay separable — the same
discipline `docs/v79-analysis.md:380` asks for w.r.t. B1.

### 3.4 Ordering against the rest of the borrow list

`docs/v79-analysis.md:380` says take B8 **after B1** (ammo magazine scaling), so
the ammo effect is not attributed to the sensor. Check the live file:
`bots/_v72e2/main.py:641-642` already has `4*weapons` capped at 48, and `:604-611`
already has the 35→50 latch. **B1 is landed.** The one B1 sub-lever *not* taken
is `32 if under` — Eir 2 uses `24 if under` (`:632`) vs v79's 32
(`opp_v58:356`). Leave it at 24 for this measurement; changing it in the same
build re-confounds exactly what B1's staging was meant to separate.

---

## 4. CPU

Budget: `CPU_BUDGET_US = 8000` of the engine's 10 ms
(`bots/_v72e2/main.py:277`). `ct.get_cpu_time_elapsed()` reads 0 under local
`fcode run` (`docs/tooling.md:83-89`), so any local verification must use
`time.process_time()` instrumentation and any real verification is
`fcode match test` on Graviton3.

**Direct cost of the port: zero.** No new engine call, no new scan, no new tile
enumeration. Hoisted, the per-round arithmetic is also zero (v79's in-loop form
would be ~6 int ops × ≤8 visible enemies ≈ single-digit µs, <0.2% of budget —
still negligible, but hoisting makes it exactly nil).

**The tile-count question, answered for completeness.** If someone tried to
implement this as an actual wider scan, the volume would be: r²=20 (builder
vision, what we scan today) = 69 lattice tiles; r²=64 = 197; r²=100 = 317; r²=36
(core vision) = 113. So a naive scan-widening would be a **4.6× increase in
enumerated tiles** — and it is impossible anyway, both because the getter is
documented to raise past vision (`docs/game-model.md:418-420`) and because no
entity outside vision is returned regardless. **The real port has none of this
cost, which is the single most important fact in this spec.**

**Indirect cost — the part that is real.** More rounds with `SLOT_UNDER=1` means
more turns take the expensive UNDER-only paths. Per builder-turn, in engine
calls:

| path | trigger | approx engine calls |
| --- | --- | --- |
| `_heal_core` (`:1429`) | UNDER ∧ cd==0 | ≤4 `can_heal` + 1 `heal` |
| `_core_shelled` (`:1436`) | `_defend`/`_expand`/`_hunt_turret` | 1 `get_nearby_buildings` + ~2/building (≈10-30) |
| `_hunt_turret` candidate scan (`:1522-1569`) | UNDER ∧ rnd≥120 ∧ shelled | `get_nearby_buildings` + `get_nearby_units` + ~4/candidate |
| **`_try_counterbattery` (`:1641-1705`)** | threat set ∧ eco gate open | **up to 2 × 8 dirs × 8 facings = 128 `can_fire_from` + up to 128 `can_build_*`** |

`_try_counterbattery` is the only one that can plausibly approach the guard, and
it already self-checks `_cpu_exhausted` once per direction (`:1685`). It is also
the one the widening makes *structurally futile*: a sentinel is r²=32, so a
turret built adjacent to our own footprint can only reach threats at
footprint-dsq ≲ 44. A threat published at core-dsq 100 will fail every
`can_fire_from` and burn the full ~128-256-call scan for nothing, every defender
turn, for up to 50 latched rounds.

**Mitigation (recommended, ~3 lines, in phase 1b):** early-return in
`_try_counterbattery` when the threat is out of any buildable turret's reach:

```python
# bots/_v72e2/main.py, right after :1645 (threat is None check)
if min(t.distance_squared(threat) for t in core_tiles(self.core)) > HUNT_BAND_DSQ:
    return False
```

`HUNT_BAND_DSQ = 41` (`:94`) is already the measured, twice-validated
"past sentinel range, footprint-measured" constant in this file — reusing it
avoids inventing a number. Net effect on CPU is *negative* (it removes scans that
exist today whenever the threat is far), so this is safe to include in phase 1.

---

## 5. Expected behaviour delta on archipelago / snowflake

**Archipelago (26x26, 30.8% walls, anchors (5,5)/(19,19), 0/32 vs opp_v50-class,
`results.tsv:130`).** Ordered by expected size:

1. **Ammo solvency, early.** UNDER flips the Core from `ammo_target=16, ti_floor=52`
   to `24, 12` (`:630-643`). Thread-brief context and `docs/spitball.md`'s
   research-session findings put *ammo starvation*, not DPS, at the centre of the
   grind losses. On a 676-tile map with distant anchors the current 64 threshold
   means an enemy forward battery can shell our outer economy for its whole life
   without ever tripping UNDER. This is the most likely mechanism of the 0/32.
2. **The universal adjacent heal turns on** (`:991` is UNDER-gated). Same argument:
   heals that currently never fire because nobody classified the siege as a siege.
3. **The threat becomes nameable** → `_try_counterbattery` (`:1641`) and the
   defender's chase (`:1831`) get a target ~2 tiles/rounds earlier along the
   approach, and get one *at all* for the 54-61 in-bounds tiles in the
   64<d²≤100 annulus.
4. **b_sense 16→36 doubles the anti-saboteur window** (49→111 tiles): an enemy
   builder walking in to plant is flagged at 6 tiles instead of 4, which with the
   melee recall at `:1035` (core-dsq ≤25 / enemy-at-core-dsq ≤20) means the
   recall can be *pre-positioned* rather than triggered on contact.
5. With phase 2, saboteurs stop being recalled home at all on this map, so
   forward siege pressure survives melee harassment.

**Snowflake (26x26, 10.4% walls, same anchors).** Same tier fires, but snowflake
has three existing special cases that will now be driven harder — this is why it
must be measured as its own leg, not pooled:

- `snowflake_home_b` + `role_n == 4` → `_rank2_hold` (`:1008-1019`): clears
  `link_queue` and walks the defender home. With b_sense 36 this fires on any
  enemy builder within 6 tiles of home. **Could cost the B-seat economy.**
- `replay_snowflake` role-3 → saboteur at r≥8 (`:886-900`).
- `healer_focus` turret targeting table (`:2560-2564`).

---

## 6. Risks — what a leaking gate can cost on the other 13 maps

**The gate itself cannot leak by dimension.** `area >= 650 ∧ mw == mh` is a pure
function of `get_map_width()/get_map_height()`, read once at `:755`, no store, no
map decode, no seat dependence. The nearest pool map below the line is drumlin/
hive at 625 (square) and saga at 576 (square); the nearest above with a different
shape does not exist. Margin is 25 cells on one side and infinite on the other.
**There is no plausible dimension near-miss in this pool.** The only leak vector
is a *new* rotation map that is square and ≥650 (e.g. 27x27=729) inheriting the
tier untested — a genuine but bounded risk, and the same one v79 carries.

Real risks, in order:

1. **Defender abandonment (`:1831`).** `if under and threat is not None: tgt =
   threat; _nav()`. With gun_sense=100 the defender can be sent up to 10 tiles
   from home, on a 30.8%-wall map where that is a long path, to a turret it
   cannot kill (builder melee is 2 dmg/2 Ti vs a 40 HP sentinel). It is
   pre-empted by the DEFENDER-COMES-HOME rule (`:1824-1829`) only when the Core is
   *provably bleeding and visible*. **This is the single most likely regression
   and it is confined to the two target maps** (the same clause exists in v79 at
   `opp_v58:1326`, so a faithful port keeps it — but instrument it). If it shows
   up, bound the chase with the same `HUNT_BAND_DSQ` test proposed for
   counterbattery.
2. **Counterbattery burn** — quantified in §4; mitigated by the 3-line reach test.
3. **Convergence over-fire (`:1989`)** — role-2 and role-≥5 expanders park at the
   Core more often. Double-gated on `_core_shelled`, which needs the Core inside
   the builder's own r²=20 vision, so there is no cross-map recall. Low.
4. **`_rank2_hold` on snowflake-B (`:1011`)** — see §5. Map-specific, measure the
   snowflake-B seat explicitly.
5. **Phase-2 recall suppression** is the one change that *can* regress other maps
   if written v79's way (`>=600` pulls in hive, which we sweep 32/32, and
   `square_band` pulls in jackpot/lighthouse). The `>=650` narrowing in §3.3
   makes that impossible by construction. **Do not ship v79's literal predicate.**
6. **Composition with B1** — landed already (`:641-642`, `:604-611`), so the
   ammo effect measured here is the *sensor's* contribution on top of an already
   scaling magazine, which is the clean read `docs/v79-analysis.md:380` asked for.

---

## 7. Measurement plan (what the verdict should rest on)

- Ablation legs: **archipelago both seats** and **snowflake both seats** vs an
  opp_v50-class bot (`results.tsv:130` is the 0/32 baseline) — the gate touches
  nothing else, so a pooled 15-map run mostly measures noise. A pooled run is
  still worth one pass as a leak check (it should be a *null* everywhere else;
  any non-null on a non-676 map means the gate is not doing what this spec says).
- Instrument, don't guess: log per-match rounds-with-UNDER, Ti→ammo converted,
  heals landed, and defender distance-from-core. The hypothesis is specifically
  *ammo + heals turn on earlier*; if the win comes without those moving, the
  attribution is wrong again (as it was for v82's hive-B hunk).
- CPU: `time.process_time()` locally on archipelago; the guard is inert under
  `fcode run` (`docs/tooling.md:83-89`).

## 8. Adjacent items surfaced (not part of B8)

- v82 `_expand:1385-1415` — under UNDER on `area > 600`, smash an adjacent
  enemy Gunner/Sentinel **before** heal/eco, with no round floor. Eir 2 has no
  equivalent (our `_hunt_turret` is floored at round 120, `:215`). This is a
  distinct, cheap, archipelago/snowflake/drumlin/hive-relevant borrow. Worth its
  own line on the board.
- v82 `_saboteur:986-993` heals the primary siege turret via `SLOT_SIEGE` — Eir 2
  has this (`:1329-1336`). No gap.
- v79's `_deny_threat_tile` (B3, `v79-analysis.md:370`) becomes **more** valuable
  with a wider `SLOT_THREAT`, since it is the one consumer that costs nothing
  when the threat is unreachable (it only fires when already orthogonally
  adjacent).
