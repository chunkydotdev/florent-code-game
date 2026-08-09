# The hive 7-vs-2 seat turret gap: cause located, plus a defect the code's own comment denies

**Research arm, 2026-08-09 (session 22).**
**Version tag:** our live version **v89 "Eir 9c hivethaw (rollback)"**, submission
`847b8d9d`, = `bots/_v100hf`, **md5 `9e85cae5d3654d1b23c5b4507ae76c8e`** (verified by
me, not relayed). Ladder at boot: 1524, 486 matches, #36/113, recent 2W-8L.
**Code read: `bots/_v100hf/main.py` only** (5,104 lines). Line numbers are that file.
Map primary source: `maps/hive.map26`, decoded here with the schema in
`tools/make_map.py`.
**Zero replay downloads. Zero arena runs** (research lane — the ablation in §6 is
specified for the builder, not run by me).

Prompted by the builder's 06:3x coordination note, which measured a **7-vs-2
seat-dependent home-turret gap on hive**, deterministic across 4/4 seeds on both
seats, and queued the cause to research as HANDOVER item #3.

---

## 0. TL;DR

1. **The premise checks out and is stronger than stated.** hive is *exactly*
   180°-rotationally symmetric — terrain, ore, and both core footprints. So is
   PLANK HS's seat machinery. The asymmetry is not in the map and not in the
   general code.
2. **The cause is two hardcoded single-seat clauses that are not each other's
   mirror**: `hive_home_a` (:2301, **seat A only**) and `hive_bunker` (:3453 +
   :3565, **seat B only**). Each was measured on one seat and never mirrored.
3. **The builder's "no home gun to find" is right about the symptom and
   under-specified about the cause** — and one word of it is wrong: `SLOT_HOME_GUN`
   is not a home-turret count (§3).
4. **A separate, independently shippable defect fell out**: the seat-B bunker
   plants a permanent impassable barrier on **(20,4), one of the two seats PLANK HS
   reserved for harvester delivery**. The plank's own RED FLAG comment at :3468
   asserts the seat ban prevents this. **Computed from the bot's own functions, it
   does not.** Seat A loses no seat to anything.

---

## 1. THE MAP IS EXACTLY SYMMETRIC — verified, not assumed

`maps/hive.map26` decoded directly (protobuf, schema from `tools/make_map.py`):

```
25 x 25   cores: A anchor (2,20)   B anchor (21,3)   34 walls   12 ore
terrain 180-rotation violations, all 625 tiles:  0
```

Under (x,y) -> (24-x, 24-y): A's 2x2 footprint {(2,20),(3,20),(2,21),(3,21)} maps
exactly onto B's {(21,3),(22,3),(21,4),(22,4)}. All 12 ore tiles pair off
((11,3)<->(13,21), (7,7)<->(17,17), (23,7)<->(1,17), ...).

**And the general seat machinery is equivariant too.** Running the bot's own
`heal_seats` / `delivery_seats` against the decoded map:

| | seat A (2,20) | seat B (21,3) | rotation image? |
|---|---|---|---|
| heal seats | 8 | 8 | **identical set** |
| reserved delivery seats | (3,19), (4,20) | (20,4), (21,5) | **identical set** |
| seat ban | 6 tiles | 6 tiles | **identical set** |

So PLANK HS cannot be the source of the gap. Neither can the map. **Whatever
produces 7-vs-2 is written into the file as an explicit seat literal.**

## 2. THE TWO SINGLE-SEAT CLAUSES

```python
# :2301  SEAT A ONLY
hive_home_a = (self.mw == 25 and self.mh == 25
               and self.core.x == 2 and self.core.y == 20)
# effect (:2307): under SLOT_UNDER, role_n in (1,2,3) -> _rank2_hold -> return

# :3453  SEAT B ONLY
hive_bunker = (self.mw == 25 and self.mh == 25
               and (self.core.x, self.core.y) == (21, 3))
# effect A (:3457): adjacent to (20,4) -> heal/build barrier there -> return
# effect B (:3565): ALWAYS -> tgt = (20,3); _nav; return
```

These are two *different strategies*, not one strategy expressed twice. Seat A
pulls ranks 1-3 home under threat; seat B parks its defender on a fixed tile and
builds a barrier. Applying either to the other seat would change that seat's play.

**This is a defect class, not a one-off.** Classifying every map-gated clause in
the file against the core pairs the bot itself knows (`CORE_PAIRS`):

| line | clause | seats covered | status |
|---|---|---|---|
| 2127 | nordkap (9,6) | 1 of 2 | **single seat** |
| 2139 | snowflake_attack (5,5) | 1 of 2 | **single seat** |
| 2298 | snowflake_home_b (19,19) | 1 of 2 | **single seat** |
| 2303 | **hive_home_a (2,20)** | 1 of 2 | **single seat** |
| 2322 | keep_artillery 21x8 core.x==5 | 1 of 2 | **single seat** |
| 3455 | **hive_bunker (21,3)** | 1 of 2 | **single seat** |
| 3494 | chase_battery (9,6) | 1 of 2 | **single seat** |
| 2133 / 2325 / 2329 / 3643 / 4654 | pair-form clauses | both | symmetric |

**Seven single-seat behavioural clauses across four maps.** hive is simply the one
where a probe happened to look at both seats. On the same evidence, nordkap
(two single-seat clauses, both on (9,6)) and snowflake (two, on different seats)
are the next places to look.

## 3. CORRECTION TO THE RELAY: `SLOT_HOME_GUN` IS NOT A HOME-TURRET COUNT

The builder's table reads `SLOT_HOME_GUN 7 / 2` and the note glosses it as *"we
stand 7 home turrets on seat A and 2 on seat B."* The counter does not support
that reading, and the file says so itself at :3070:

- it is incremented at **three** sites, one of which (`_try_siege_build`, :2717) is
  the **saboteur's FORWARD gun at the ENEMY core**;
- it is **never decremented**, so rubble counts forever.

So `7 / 2` is *"turret builds of any kind, anywhere, ever, still counted after they
die."* **The gap is real and the 4/4-seed determinism makes it solid; its
attribution to HOME turrets specifically is not yet established.** A probe that
prints the build site alongside the increment settles it in one run and should be
part of §6 rather than a later question.

## 4. WHY THE GAP HAS THE SHAPE IT DOES — mechanism, and see §5 for its label

The file states the key fact itself, in the DEFEND-ROLE REDUNDANCY block (:660):

> *"the role_n == 4 defender is the ONLY unit that ever calls
> `_try_counterbattery`, so home turrets are its exclusive capability."*

Confirmed against the code: role "defend" is assigned only to `role_n == 4`
(:1982), single-occupancy by design (:1986-1990), and `_try_counterbattery` has
exactly two call sites — `_defend` (:3526) and the saboteur/launchwait melee
recall `_home_defend` (:2380).

`_try_counterbattery` builds on tiles **adjacent to the defender** (`p.add(d)`,
:3403) and requires `can_fire_from(bp, facing, turret_type, threat)` (:3416) — the
candidate tile must have a live firing line to the published threat.

**So home-turret production is a function of where the one defender stands.**

And on seat B, :3565 replaces that unit's entire move phase:

```python
if hive_bunker:
    if ct.get_move_cooldown() == 0:
        self.tgt = Position(20, 3); self._nav(ct, pave=False)
    return          # <-- returns before everything below
```

Bypassed on seat B, every round, for the whole match:
- **DEFENDER COMES HOME** seat-seek (:3579)
- **threat chase** `tgt = threat` (:3594)
- **link-queue navigation** (:3599-3616) — so a seat-B defender can only ever lay a
  conveyor it is *already* standing next to
- the orbit/wander fallback (:3618-3628)

A defender pinned at (20,3) offers at most 8 candidate tiles, and after removing
the two core-footprint tiles, the banned seat (21,2) and the bunker's own barrier
at (20,4), **four** remain — all on the same side of the core. Seat A's defender
roams and presents a new tile set whenever the threat moves.

**The action phase is NOT stolen** — once the barrier stands at full HP,
`can_heal` refuses it and the build arm sees `bid is not None`, so :3457 falls
through and `_try_counterbattery` is still reached. This is a *placement-geometry*
restriction, not a lost turn.

## 5. THE LABEL ON §4, because the builder earned this rule this morning

**§4 was generated after I knew the 7-vs-2 result.** It is the same epistemic
shape as the "type-vs-placement" Thor explanation the builder labelled in the
HANDOVER, and it gets the same label: **hypothesis, not finding.** Nothing I read
distinguishes it from "the two seats just play differently and the turret count is
one of many downstream differences."

What *is* finding-grade here: §1 (symmetry, computed), §2 (the clauses and their
seat coverage, read), §3 (the counter conflation, read), §6/§7 (the barrier on the
reserved seat, computed).

## 6. THE ABLATION THAT DISCRIMINATES — builder's lane, cheap, det, zero Elo

Same recipe as the 06:3x probe (`_dbg_hf` pattern, `NOISE_ON=False`,
`maps/hive.map26`, seeds 1-4, both seats), **plus a print of the build site at each
`SLOT_HOME_GUN` increment** so §3 is settled in the same run.

| cell | change | predicted by §4 | predicted if §4 is wrong |
|---|---|---|---|
| C0 | none (control) | 7 / 2 | 7 / 2 |
| **C1** | **delete only the `hive_bunker` move arm (:3565-3569)** | **seat B rises toward seat A** | flat |
| C2 | mirror `hive_home_a` onto seat B | ~flat (ranks 1-3 don't build turrets) | rises |
| C3 | disable both hive clauses | both seats converge | — |

**C1 vs C2 is the whole test.** If C1 moves it and C2 does not, §4 is confirmed and
the fix is a four-line deletion. If neither moves it, the cause is engine seat
order or a tie-break asymmetry and this document is wrong about the mechanism.

## 7. **A SEPARATE, INDEPENDENTLY SHIPPABLE DEFECT** — and the code comment is wrong about it

At :3468 the bunker plank carries this RED FLAG:

> *"(20,4) IS a heal seat of the hive seat-B footprint ... and a barrier is
> impassable, so this map-gated bunker plank permanently costs one of the eight
> seats. **The ban is applied here for consistency with every other impassable
> build site**"*

The ban *is* queried (:3477-3480). **It does not fire.** Computed by calling the
bot's own `delivery_seats` on the decoded map:

```
seat B (21,3):  reserved delivery seats = (20,4), (21,5)
                seat ban = (20,3) (21,2) (22,2) (22,5) (23,3) (23,4)
                (20,4) in ban ?  False        <-- the barrier IS built
                (20,3) in ban ?  True         <-- the tile it parks on
```

So the plank does not merely cost "one of the eight seats" as the comment fears —
**it puts a permanent impassable barrier on one of the exactly TWO seats PLANK HS
reserved for the harvester chain to terminate on**, and it parks the defender on a
tile the ban already excluded. Seat A's mirror tile (4,20) is likewise a reserved
delivery seat and nothing ever builds on it.

Scope, stated honestly: `HS_SEAT_BAN_CONVEYORS = False`, so `_pave_ban()` returns
None and **conveyor** goals are *not* restricted to the two reserved seats
(`_link_path`, :4074) — a chain can still terminate on any of the eight. The
measured cost is therefore: (20,4) permanently lost as a heal seat (impassable),
as a conveyor terminal (occupied), and as a build site, on seat B only.

**This is a two-plank interaction, and it is invisible to either plank's own
tests** — HS reserves the tile, the bunker fills it, and neither one is wrong on
its own. It is also independent of §4: it holds whether or not the turret
mechanism is what I think it is.

## 8. WHAT THIS DOES NOT SHOW

- No claim about **which** seat's behaviour is *better*. The builder's own numbers
  cut against the obvious reading: seat B never freezes and still banks less
  (4,900 vs 5,260), and both seeds won on the r1000 titanium tiebreak.
- **Single-map, single-opponent, single-lineage.** The 06:3x probe is `bots/_v89sh`
  (v80, freeze ON) vs `bots/opp_v63`. I have verified the clauses are byte-present
  in the live `_v100hf`; I have not verified the 7-vs-2 *number* reproduces there.
- The §2 table says seven clauses are single-seat. It does **not** say the other
  six cost anything — only that nobody has looked at their other seat.
- I did not run the arena or download a replay for any of this.
