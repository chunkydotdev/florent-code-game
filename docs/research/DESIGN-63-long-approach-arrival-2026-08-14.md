# DESIGN — `#63` LONG-APPROACH ARRIVAL, **A NAVIGATION CHANGE WITH A SOURCE-GRADE MECHANISM AND A PROBE THAT CAN KILL IT**

**Research arm, s41, 2026-08-14T18:33:08Z (`date -u`).** Owed from the s40 wrap
("`#63`'s design — deliberately held"). **Subject tree: `bots/_v223sealrepair`
(v140 "Loki v10"), `eco.py` at commit `4990599` (2026-08-14T11:32:53+02:00).**
Every line number below was read in that tree at that commit.

**THIS IS A DESIGN NOTE, NOT A PRE-REGISTRATION.** It ends with a probe, not a
bar. The prereg is written after the probe reports, per R4 ("the dose probe is a
design phase, not a check") — three arms screened cleanly and meaninglessly
yesterday for want of exactly this step.

---

## 0. WHAT THE ROW DEMANDS, AND THE TRAP IT NAMES

`QUEUE.md#63`: *"NOT A THIRD DETECTOR. Any arm off it must change the NAVIGATION
or the DESTINATION, not the detection — and its prereg must say which, or it is
the same dead arm renamed."* Two detect-and-repick arms (OSCLOCK, OSCLOCK2) are
already dead. **The design below changes the NAVIGATION — specifically, the WORLD
MODEL the navigation searches over. It adds no detector and reads no counter.**

---

## 1. THE SOURCE FACTS — certain, verifiable by reading, no inference

These are reads of the shipped tree. They are **not** claims about midgard.

**F1. THE BFS's `blocked` SET OMITS BUILDER BOTS — THE ONLY MOBILE OCCUPANT.**
`eco.py:815-835` builds `blocked` from `self.map_walls`, both cores' footprints,
and, for entities in vision, this list:
```python
elif et in (EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER,
            EntityType.HARVESTER, EntityType.BARRIER):
    blocked.add((ep.x, ep.y))
```
**`EntityType.BUILDER_BOT` is absent from that tuple, and from every other branch.**
⇒ the search treats a tile occupied by a builder bot — ours or theirs — as free.

**F2. THE MOVE LAYER DISAGREES WITH THE SEARCH LAYER.** `_move` (`eco.py:955`)
gates on `ct.can_move(d)`, which is False for an occupied tile. ⇒ **the BFS can
propose, every round, a first step the move layer will refuse every round.** The
two layers hold different models of the same tile. *(The engine premise — that
two builder bots cannot share a tile — is the guard-matrix finding that
bot-stacking desync is impossible; it is the one item here I would still drive
in the probe rather than assume, see §4 C0.)*

**F3. A BACKSTEP COUNTS AS A SUCCESSFUL MOVE.** `_nav` (`eco.py:898-910`):
```python
if self._move(ct, desired, pave):
    return
idx = CARDINALS.index(desired) if desired in CARDINALS else 0
for d in (CARDINALS[(idx + 1) % 4], CARDINALS[(idx + 3) % 4], desired.opposite()):
    if self._move(ct, d, pave):
        return          # <-- returns on desired.opposite() too
self.stuck += 1         # <-- reached ONLY if all four moves fail
```

**F4. `stuck` IS THE SOLE ESCAPE HATCH AND IT IS UNREACHABLE FROM AN
OSCILLATION.** `eco.py:1226`: `if self.tgt is None or p == self.tgt or
self.stuck >= 5:` is the only re-pick. In a two-tile oscillation **`tgt` is set**
(not None), **`p` never equals `tgt`** (we never arrive), and **`stuck` never
increments** (F3 — the backstep succeeded). ⇒ **all three disjuncts are false
forever. There is no exit.**

**F5. THE GREEDY FALLBACK RE-PROPOSES THE SAME BLOCKED STEP.** When the BFS
drains without reaching a goal it returns `p.cardinal_direction_to(target)`
(`eco.py:896`) — the greedy step, i.e. straight back into the obstruction. Same
at `:882` on CPU exhaustion and `:863` when `goals` is empty.

---

## 2. THE MECHANISM — **HYPOTHESIS**, not observation

⚠ **LABELLED DELIBERATELY.** F1–F5 are source facts and are certain. The sentence
below is a story about what those facts do on midgard, and **this lane shipped
three mechanism stories yesterday that died to evidence gathered for other
purposes** (wall-clock non-determinism, the grid fix, home-base locking). It gets
the weaker label until §4 reports.

> **H1 (BODY-BLOCK OSCILLATION).** On a long approach, builders travel as a
> loose column toward the same distant target region. A trailing builder's BFS
> plans through the leading builder's tile (F1); the move is refused (F2); the
> perpendiculars are unavailable (column in a lane or against terrain); the
> backstep succeeds and is scored as progress (F3); next round the BFS — planning
> over an unchanged world model — proposes the identical first step. **The pair
> oscillates on two tiles with no counter rising and no re-pick (F4), for the
> rest of the game or until the leader moves.**

**WHY IT WOULD BE MAP-DIFFERENTIAL, which is the part `#63` actually observed.**
H1 needs (a) a long shared approach, so the column has time to form and to stay
formed, and (b) locally narrow passable width, so the perpendiculars fail. It
predicts **nothing on short-approach maps regardless of area** — which is the
shape of the row's own control: *"valkyrie and glacierkeep read 77%/73% and are
among our BEST cells despite being the same size."* **H1 is consistent with the
area-null. It is not evidence for H1** — several stories fit that control — but a
mechanism that contradicted it would already be dead.

**WHAT H1 DOES NOT EXPLAIN, stated now so it is not quietly dropped later:** the
`#63` observation is a **RATIO — 3.3× ours vs theirs on the same maps against the
same opponents.** H1 is a defect in OUR tree and predicts a ratio > 1 only if
opponents lack the same defect. **We have not read their trees and cannot.** So
H1 explains our absolute rate; the ratio is explained only under the added
assumption that this pattern is ours specifically. **That assumption is untested
and is not testable on any surface we own.** ⇒ **the arm must be justified by the
absolute builder-rounds it recovers, never by the ratio.**

---

## 3. THE ARM — **BODYAWARE**: the search learns about bodies

**ONE CHANGE, in `_bfs_direction`'s world model. No detector, no counter, no
re-pick logic touched.**

```
BODYAWARE_ON = True
1. Add BUILDER_BOT positions (BOTH teams, from the existing
   ct.get_nearby_entities() loop that already runs at eco.py:822) to `blocked`.
2. Run the BFS exactly as now.
3. ⭐ THE FALLBACK IS THE LOAD-BEARING HALF: if that search finds no goal,
   re-run it ONCE with the body positions removed — i.e. today's behaviour.
```

**WHY STEP 3 IS NOT OPTIONAL AND IS WHERE A NAIVE VERSION OF THIS ARM DIES.**
Bodies are transient; walls are not. Without the retry, a single bot standing in
a genuine one-wide corridor turns a reachable target into an unreachable one, and
the greedy fallback (F5) fires — **which is exactly the current failure, now
reached by a new route.** With the retry, the arm is a strict refinement:
**where a body-free detour exists it is taken; where none exists, behaviour is
byte-identical to today.**

**COST.** One extra `EntityType` comparison inside a loop that already runs, plus
at most one repeated BFS. ⚠ **CPU is a live constraint on this tree —
`QUEUE.md#44` records v125 at 87.6% of the TLE ceiling on 30×30.** The BFS
already self-limits (`_cpu_exhausted` every 64 nodes, `eco.py:881`), so the
degenerate case degrades to today's greedy step rather than to a timeout — **but
the doubled search must be CPU-probed on 30×30 before any live leg, and that
probe is a release gate, not a nicety.**

**SECOND ARM, HELD IN RESERVE — `NOBACKSTEP` (F3-side).** Drop
`desired.opposite()` from the `_nav` fallback so a backstep raises `stuck`
instead of masking it. **Deliberately NOT the primary**: it is one line from
being a detector arm (it works only by making the existing counter fire), and it
is the shape `#63` forbids. **It is also the natural CONTROL** — if BODYAWARE
moves the metric and NOBACKSTEP does not, the defect is in the world model; if
both move it equally, the cheaper one wins.

---

## 4. THE PROBE — **run this before any prereg; it is designed to kill H1**

**Fixture: LOCAL, instrumented, incumbent tree, midgard + ragnarok.** Local is
admissible here because the question is *"does this code path execute"*, not
*"does it win"* — and per the corpus/DEFF rule, local batteries read
pair-weighted DEFF ≈ 0.98, so naive local intervals are correct there. **A live
leg is required before any road is CLOSED (point 6); none is closed here.**

Instrument every builder-round where the bot held a target and did not reduce
its Chebyshev/Manhattan distance to it, and classify the FIRST refused step:

| cell | classification of the refused first step | H1 predicts |
|---|---|---|
| **C0 — CONTROL, DRIVE IT FIRST** | two builder bots ordered onto one tile; assert the second `can_move` is False | **must be False**, else F2 is wrong and the whole design dies |
| **C1** | refused because a **BUILDER BOT** occupies the tile | **the dominant cell on midgard/ragnarok** |
| **C2** | refused because a **BUILDING/WALL** occupies it | present but not dominant |
| **C3** | move succeeded but was `desired.opposite()` (a scored backstep) | **must be non-trivial — this is F3 firing** |
| **C4** | all four refused (`stuck` incremented) | **should be RARE**; if it is common, `stuck>=5` is already rescuing us and H1 is not the binding constraint |

**FALSIFIERS, written before the data exists:**
* **C0 comes out passable ⇒ F2 is false and BODYAWARE has nothing to fix. Stop.**
* **C1 ≈ 0 on midgard ⇒ H1 IS DEAD.** Bodies are not what blocks us; the lock is
  terrain and the arm should be a DESTINATION change instead (re-pick targets so
  columns do not form), which is a different design and needs a different note.
* **C3 ≈ 0 ⇒ the backstep path is not being taken**, so F3 is inert here and
  NOBACKSTEP is withdrawn outright.
* **C4 dominant ⇒ the existing escape hatch already fires** and `#63`'s premise
  ("the escape hatches can never fire inside an oscillation") is true of
  oscillations but irrelevant to what actually happens on this map.
* **A comparison cell that cannot separate: valkyrie/glacierkeep.** Same area,
  BEST cells. **C1 must be materially lower there than on midgard.** If C1 is
  equally high on our best maps, the indicator is measuring something that does
  not track outcome and **it validates nothing** — the constant-column failure.

⛔ **AND NOTE WHAT THE PROBE CANNOT DO.** It measures OUR tree only. It cannot
touch the RATIO (§2), because opponents' internals are unreadable. **Any prereg
off this note declares its target mix and its ratio-blindness inline, or it is
claiming a comparative result off a self-only instrument.**

---

## 5. OBLIGATION 15a — MAP SEGMENT

**PRIMARY SEGMENT: {midgard, ragnarok}** (LONG-APPROACH), inherited from `#63`
unchanged. **{valkyrie, glacierkeep} is the CONTROL segment** — same area, best
cells, and it exists so the arm cannot pass by moving everything everywhere.
**One primary. No sweep across the remaining maps.**

### ✅ SEGMENT-VALUE LINE — DELIVERED 2026-08-14 (research s42), closing a debt this note declared against itself

**`SEGMENT VALUE CEILING: 14.6% × 13.6pp = 1.98pp pooled`**

Derived off `corpus/ladder_games.tsv`, population stated because it is the whole finding:

```
NEW-POOL ERA (from 2026-08-13T07:12:59Z, the first new-map pairing): n = 540 rated games
  primary segment {midgard, ragnarok}   79/540 =  14.6% of pairings
  our win, overall                                54.1%
  our win, on segment                             40.5%   deficit 13.6pp
  segment cell interval at n=79 (DEFF 1.366)     ±12.7pp
```
The **13.6pp** figure is the effect CEILING in the strict sense — it is what closing the
entire on-segment deficit to our own overall rate would buy, and no plank that fixes a
defect can exceed it. **⇒ the whole plank is worth at most ~2pp pooled.**
⚠ **And the deficit is only just resolved by its own cell: 13.6pp against ±12.7pp.**

### ⛔⛔ AND THE REASON THIS LINE WAS WORTH COMPUTING IS NOT THE ANSWER, IT IS THE WINDOW

**THE MAP POOL CHANGED 36 HOURS AGO AND EVERY SEGMENT PRICED OFF POOLED HISTORY IS WRONG.**
Ten maps entered the rated pool on **2026-08-13 between 07:12:59Z and 10:32:59Z** —
`valkyrie · midgard · icefloe · frostgate · auroraveil · glacierkeep · drakkarfjord ·
yulerune · royale · ragnarok`. **They are now 66% of pairings.** An all-time share averages
over a period in which these maps DID NOT EXIST:

| segment | all-time share | new-pool share | **misprice factor** |
|---|---|---|---|
| `#63` primary {midgard, ragnarok} | 1.6% | **14.6%** | **9.1×** |
| `#63` control {valkyrie, glacierkeep} | 1.5% | **13.7%** | **9.1×** |
| SPAWNPOCKET primary {midgard, fjordgate} | 6.5% | **14.4%** | **2.2×** |

⇒ **a `SEGMENT VALUE CEILING` computed off the all-time tape would have priced this plank at
0.16pp pooled instead of ~2pp and killed it on arithmetic that was 9× wrong.** *(The
SPAWNPOCKET row is included because that prereg is LIVE and its segment is mispriced 2.2× in
the same direction — flagged to its owner, not edited here.)*

**STANDING CONSEQUENCE, and it generalises past segments: a pairing share is a property of
the CURRENT pool, not of the archive. Any share, base rate or reference cut that spans
2026-08-13T07:12:59Z pools two different games.** The `#63` debt was declared because
TINYECO62 *"spent 2,700 rows on a cell whose overall ceiling was computable at prereg time"*
— **the sharper lesson is that it was computable, and computable WRONG, from the obvious
population.**

## 6. COMBO-INTERACTION WITH `SPAWNPOCKET` — owed by the s40 wrap

**The segments overlap on midgard** (`#63` = {midgard, ragnarok}; SPAWNPOCKET =
{midgard, fjordgate}), and the wrap's rule is that **whichever prereg lands
second owes this line.**

**THE INTERACTION IS MECHANISTIC, NOT MERELY A SHARED CELL, AND IT RUNS ONE WAY:**
SPAWNPOCKET is *"never put a builder in a cell it cannot leave"* — a change at
**spawn/placement** time. BODYAWARE is a change at **transit** time. **A pocket
is ENTERED, not spawned into** (the s40 wrap's own correction), and F1 says the
BFS routes *through* bodies — **so BODYAWARE changes which tiles a builder walks
into, which is precisely the input SPAWNPOCKET's rule is defined over.** ⇒
**BODYAWARE can change SPAWNPOCKET's measured effect on midgard; SPAWNPOCKET
cannot symmetrically change BODYAWARE's**, because placement does not alter the
BFS's world model.
⇒ **ORDERING RULE: on the shared midgard cell the two arms must not be measured
concurrently.** If both are live, BODYAWARE is the confound and reads second, or
the midgard cell is dropped from whichever leg runs later and the segment
declared as {ragnarok} / {fjordgate} respectively. **Written here so the second
prereg inherits it rather than rediscovering it in an analysis.**

---

## 7. ROUTING
* **To the BUILDER:** the §4 probe (local, instrumented, C0 driven FIRST), and
  the §3 CPU probe on 30×30. **No arm is built before C0 and C1 report.**
* **To the SIDE LANE:** §6's ordering rule is a certification condition on
  whichever of SPAWNPOCKET/`#63` fires second on midgard.
* **Owed by me before any prereg:** the §5 segment-value arithmetic.
* **`QUEUE.md#63`:** annotate with this file per R5 (make the row cite its arm).
