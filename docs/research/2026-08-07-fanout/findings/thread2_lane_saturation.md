# Thread 2: Lane-Saturation Audit vs ECO_CAP=18

Read-only replay analysis. `ECO_CAP = 18` confirmed at `bots/_v72e2/main.py:25` (raised to
`SURGE_ECO_CAP = 24` under the "LATE LABOR SURGE" gate — `bank >= SURGE_TI_FLOOR(1500)` and
`round >= SURGE_MIN_RND(300)`, see `_eco_cap()` at `main.py:1367-1377`). The cap variable read
by the harvester-build gate (`harv < self._eco_cap(ct)`, `main.py:1797`/`1896`) is
`ct.read_store(SLOT_HARVESTERS)` (`main.py:243`), which is **incremented on every successful
`build_harvester()` call and never decremented on death** (`main.py:1901`) — this single fact
turns out to matter more than the cap's numeric value (see Finding 2 below).

Methodology note: "lane" = the `frm` tile of a `ResourceMove` whose `to_core_team` matches the
team (i.e. the orthogonal input tile a delivery arrived from, not the footprint tile it lands
on). Validated against the map's actual 8 orthogonal-neighbor tiles of each core's 2x2
footprint on all 14 games: **zero deliveries ever arrived from a non-input tile** — the lane
model holds exactly.

**Segmented by our bot version per the coordinator's directive.** v61 (`706faea6`) is the
current line and is prioritized; v59 (`2618b9b4`) is one generation back; v54-v56
(`40748bb2`, `3712fb12`, `17622ae0`, `12df1f45`, `abbf93b4`) are older generations — a bottleneck
measured there may already be fixed or irrelevant on the current line.

---

## v61 — CURRENT LINE (priority; directly actionable)

| game | map | we_won | lanes wired (us/8) | first→last lane rnd | harvesters built (us) | harv ALIVE plateau | builder-hands profile | stranded Ti (us) | delivered final (us) | **bound** |
|---|---|---|---|---|---|---|---|---|---|---|
| `706faea6` g1 | eider | No | 3/8 | 11→129 | 10 (<18 cap) | 9-10 from rnd200 | **crashes to sustained 0 at rnd 247**; brief 5-bot respawn wave rnd300-304, all dead by rnd352, then 0 for the remaining ~650 rnds | 70 | 7,830 | **HANDS** |
| `706faea6` g3 | hive | No | 2/8 | 14→37 | 3 (<<18 cap) | 3 flat from rnd7 (frozen) | never crashes — climbs to 12 alive by rnd476 | 80 | 2,580 | **MAP-SPECIFIC FREEZE** (code, not resource) |
| `706faea6` g4 | snowflake | No | 6/8 | 12→361 | 17 (1 below 18 cap) | 12-14 from rnd200 | **crashes to sustained 0 at rnd 235**; brief respawn wave rnd300-304, dead by ~rnd400, then 0 for ~600 rnds | 140 | 13,480 | **HANDS** |

**g1/g4 detail — hands, not lanes, not cap.** Both games have builder-bot count collapse to a
sustained **zero** for the majority of the match (g1: 0 from rnd247 to rnd999, minus a brief
5-bot wave at rnd300-304 that itself dies within ~50 rounds; g4: same shape, 0 from rnd235
onward). Once builders are gone, *nothing* gets built — no new harvesters, no new lanes, no
repairs — for the rest of the game. This happens well short of both resource ceilings: g1 stops
at 10/18 harvesters and 3/8 lanes; g4 stops at 17/18 harvesters (one build short of cap!) and
6/8 lanes (the most lanes wired by us in the whole 14-game set). Neither game shows ECO_CAP or
lane-count as the limiting factor — the bot simply runs out of the only unit that can act.

A secondary effect worth flagging: even where harvesters and lanes already exist, delivered
rate **plateaus** once builders die, well under either lane-capacity or harvester-count
capacity. g1: 3 lanes = 30 Ti/rnd theoretical ceiling, 9-10 alive harvesters = ~22.5-25 Ti/rnd
theoretical, but delivered rate rounds[300:999] holds flat at 7.5-8.25 Ti/rnd — using roughly a
quarter of what's theoretically available. g4: 6 lanes = 60 Ti/rnd ceiling, 12-14 harvesters =
30-35 Ti/rnd ceiling, but delivered rate rounds[300:999] is flat at ~15.0-15.15 Ti/rnd — again
well under both. This points to a **residual conveyor/splitter routing inefficiency** once the
network stops being actively maintained (dead-ends, imbalanced splitter round-robin, or
harvesters whose output path was never fully finished before the builder died) — a distinct,
smaller finding from the primary hands bottleneck, and worth its own follow-up thread if the
hands problem gets fixed and this becomes the new ceiling.

**g3 (hive) detail — not a resource bottleneck at all.** Harvester count freezes at exactly 3
from round 17 onward *despite builder count staying healthy* (up to 12 alive, never zero) — the
opposite builder profile from g1/g4, yet the worst harvester count of the three. This is
explained directly by the bot's own code, not by any measured resource constraint:

```python
# main.py:1867-1876
def _expand(self, ct):
    p = ct.get_position()
    hive_freeze = (
        self.mw == 25 and self.mh == 25
        and (self.core.x, self.core.y) in ((2, 20), (21, 3))
        and ct.read_store(SLOT_HOME_GUN) >= 1
        and ct.get_current_round() >= 42
    )
    if hive_freeze:
        return
```

Once a home gunner exists (`SLOT_HOME_GUN >= 1`) and round ≥ 42 on a 25x25 map with the core in
one of two hive-specific corners, `_expand()` — the function that builds harvesters and lanes —
returns immediately, permanently, for the rest of the match. This is a deliberate "bunker mode"
baked into the bot for this one map, not lane saturation, not hands, not the cap. ECO_CAP=18 is
irrelevant here since the bot never tries to approach it.

**v61 rollup:** ECO_CAP=18 was never hit in any of the three v61 games (max 17/18). Lane count
never saturated either (max 6/8). The measured bottleneck is **builder-hands attrition** in 2 of
3 games and a **hardcoded map-specific strategy freeze** in the third. If the coordinator is
choosing where to spend effort on the current line: fixing builder-bot survivability/replacement
after round ~250-300 is the highest-leverage lever measured here, not lane wiring and not the
ECO_CAP value.

---

## v59 — one generation back (`2618b9b4`, opponent I Stone)

| game | map | we_won | lanes wired (us/8) | harvesters built (us) | real distinct positions | builder-hands profile | stranded Ti (us) | delivered final (us) | **bound** |
|---|---|---|---|---|---|---|---|---|---|---|
| g2 | saga | No | **1/8** | 17 | 17 (no treadmill) | healthy, climbs to 10, never crashes | 490 | 8,050 | **LANES** |
| g3 | atoll | No | 4/8 | 19 (>18 cap; surge active) | **4** (15 of 19 builds are rebuilds at one tile) | healthy, 6-9 alive throughout | 140 | 7,110 | **CAP-TRACKING BUG (treadmill)** |
| g4 | drumlin | No | 5/8 | 25 (>18 cap, >24 surge cap by 1) | **13** (12 of 25 builds are rebuilds at one tile) | healthy-ish, dips to 2 late but not 0 | 360 | 15,980 | **CAP-TRACKING BUG (treadmill)** |

**g2 (saga) — the cleanest lane-bound case in the whole dataset.** Only **one** of the 8 input
tiles was ever wired, carrying all 805 deliveries for the game, despite 17 harvesters built.
One lane's theoretical ceiling is 10 Ti/rnd (4 harvesters' worth); delivered-rate-after climbs
monotonically with each new harvester up to a ceiling of 8.75 Ti/rnd by round 271 and never
exceeds it for the rest of the 1000-round game (final average 8.05 Ti/rnd) — matching the
single-lane ceiling almost exactly. 16 of 17 harvesters built after round 90 are pure waste:
their output has nowhere to go. This is the one game in the set where wiring a second input
lane would have had *immediate, measurable, uncapped upside* — builder-hands were healthy
(never crashed) and harvester count kept growing, so the constraint really was "we only ever
plumbed one pipe into the core."

**g3/g4 — the treadmill bug, quantified.** Both games show a small number of harvester
positions being destroyed and immediately rebuilt at the *identical tile*, over and over, late
in the match:
- `atoll` (g3): position `(5,16)` was built **16 times** (rounds 3, then 843→995 in 15 rebuild
  cycles, each surviving only ~8-33 rounds before dying again). Real distinct harvester
  positions across the whole game: **4**, matching the 4 wired lanes almost 1:1 — consistent
  with the map only offering ~4 defensible ore-adjacent build spots, with the contested one at
  `(5,16)` being fought over repeatedly rather than a genuinely new position ever opening up.
- `drumlin` (g4): position `(12,14)` was built **7 times** and `(13,10)` twice, together
  accounting for 12 of the 25 total "harvesters built." Real distinct positions: **13**, still
  comfortably under the 5 wired lanes' combined ~50 Ti/rnd ceiling.

Because `SLOT_HARVESTERS` only increments (`main.py:1901`) and the cap check reads it directly,
every one of these rebuild cycles **permanently consumes one unit of cap headroom** even though
the live harvester count barely moves and no new economic capacity is added. In atoll this
pushed the raw build counter to 19 (past the base cap of 18, inside the surge cap of 24); in
drumlin it pushed it to 25 (past even the surge cap of 24 by one — most likely a same-round race
where two builder bots each read the store's stale, not-yet-buffered value in the same round and
both passed the `harv < cap` check before either write landed, per the store's documented
next-round-visibility semantics). Either way: **the cap variable itself is not what's binding
game economy here** — a design flaw in how the cap is tracked (cumulative builds, not live
count) is what's binding, by letting a contested tile eat the whole cap budget through
destroy/rebuild churn while the map's real remaining capacity (more ore tiles, more lane
headroom) goes untouched.

---

## v54-v56 — older generations

| game (ver) | map | we_won | opp | lanes wired (us/8) | harvesters built (us) | builder-hands profile | stranded Ti (us) | delivered final (us) | **bound** |
|---|---|---|---|---|---|---|---|---|---|---|
| `17622ae0` g1 (v56) | saga | No | Ouroboros | 3/8 | 13 | crashes to 2 by rnd200, stays | 180 | 8,060 | HANDS |
| `17622ae0` g3 (v56) | heart | No | Ouroboros | 2/8 | 9 | crashes to 1 by rnd300, stays | 250 | 3,670 | HANDS |
| `17622ae0` g5 (v56) | jackpot | No | Ouroboros | 2/8 | 4 | stays ~2 throughout | 60 | 4,940 | HANDS (small map, low headroom either way) |
| `12df1f45` g1 (v56) | saga | No | Powerpuff Girls | 3/8 | 9 | crashes to 1 by rnd400, stays | 130 | 5,310 | HANDS |
| `12df1f45` g3 (v56) | drumlin | No | Powerpuff Girls | 3/8 | 7 | crashes to 1 by rnd400, stays | 10 | 5,650 | HANDS |
| `abbf93b4` g4 (v56) | eider | **Yes** | Askar City | 2/8 | 2 | steady @5, never crashes | 40 | 2,500 | N/A — denial win |
| `3712fb12` g4 (v55) | eider | **Yes** | Lunds Stallions | 5/8 | 20 | dips to 0 twice (rnd~400, ~800-900) but recovers each time | 270 | 20,680 | none reached — healthiest profile in the set |
| `40748bb2` g3 (v54) | eider | **Yes** | Askar City | 4/8 | 8 | steady 5→8, never crashes | 330 | 10,200 | N/A — denial win |

**The hands-attrition pattern is not new to v61** — every one of the five v56 economy-race
losses against Ouroboros/Powerpuff shows the identical shape: builder count crashes to 1-2 early
(rounds 200-400) and never recovers, harvester building stalls well under both ECO_CAP=18 and
lane capacity, and it holds regardless of opponent identity. This is a long-standing,
cross-generation weakness, not something introduced in v61 — which is good news for prioritizing
the fix (it's not a v61 regression) but bad news for how long it's been costing games.

---

## Eider wins vs eider losses — what actually differs

The three eider **wins** (`abbf93b4` v56, `3712fb12` v55, `40748bb2` v54) split into two
distinct stories, neither of which is "we out-scaled our lanes":

1. **Denial wins** (`abbf93b4`, `40748bb2`, both vs **Askar City**): our own economy stayed
   tiny (2 and 8 harvesters, 2 and 4 lanes) but the opponent's economy was even smaller (Askar
   City delivered a combined 40 and 3,830 Ti across the two games, vs our 2,500 and 10,200) —
   these wins were decided by suppressing the opponent's economy/core, not by us saturating
   anything. Builder-hands never crashed to zero in either game (steady 5, later 8).
2. **Out-teching win** (`3712fb12` vs **Lunds Stallions**): this is the one eider game in the
   set that looks like genuine economic superiority — 20 harvesters, 5/8 lanes, delivered
   20,680 Ti (highest of any of our sides in the set). Builder count *does* dip to 0 twice
   (~rnd 400, ~rnd 800-900) but recovers both times, unlike the v61/v56 loss pattern where it
   drops once and never comes back — most of the harvester base (14/20) was built before round
   250, front-loaded ahead of the attrition.

Contrast with the eider **loss** (`706faea6` g1, v61, our_seat B, same core position `(19,9)`
as the winning `40748bb2` g3): identical seat and core position, but builder count collapses
permanently at round 247 and never recovers, versus `40748bb2`'s builder count that never drops
below 5 for the whole game. Seat/map-side is not the differentiator — `40748bb2` g3 is the same
seat and the same core tile as the loss. **Builder-hands survival (permanent collapse vs.
recovery) is the structural difference**, not lanes, not seat, and — critically — the losses
were against a much stronger economic opponent (Ouroboros, opp_v8) whose own builder count and
harvester count never falter, while the two Askar City wins faced an opponent with essentially
no functioning economy at all.

---

## Stranded capital — measured but not material anywhere

Across all 14 games, in-transit (never-delivered) titanium sitting on our own conveyors/
splitters at final round ranged from 10 Ti (`12df1f45` g3) to 490 Ti (`2618b9b4` g2), consistently
**0.1%-2.3% of that game's total delivered Ti** (e.g. `2618b9b4` g4: 360/15,980 = 2.3%;
`706faea6` g1: 70/7,830 = 0.9%). This is noise relative to the hands/lanes/cap gaps above —
stranded capital is not a meaningful throughput bottleneck in any game measured, ours or the
opponent's (opponent stranded values sit in the same small range, 0-1,120 Ti).

---

## Opponent contrast (motivating datum re-checked)

The brief's motivating datum — 16 enemy builders vs our 5-12 on eider — checks out directionally
but the more decisive gap is **builder-count durability**, not peak count. Ouroboros opponents
(`706faea6`, `17622ae0`) sustain 3-10 builders *for the entire 1000 rounds*; ours peaks similarly
(5-12) but then collapses to 0-2 and stays there. Opponent harvester counts also front-load
heavily (first 5 harvesters typically built by round 8-20 across every opponent in the set,
vs. round 6-17 for us on the same games — comparable openings) but opponents keep building
through round 300-600+ where our own harvester building has already stalled from lost hands.
Opponent lane counts also never saturate 8/8 (max observed: 7/8, `12df1f45` g3 opponent) —
confirming lane-count saturation is not the ceiling for either side in this dataset; it is a
side constraint that matters in exactly one measured game (`2618b9b4` g2, 1/8 lanes).

---

## Verdict

Across all 14 games and every bot version from v54 to v61, **ECO_CAP=18 is essentially never the
real constraint** — it was only ever approached via a rebuild-treadmill accounting bug
(`2618b9b4` g3/g4, v59) that lets a single contested harvester tile permanently burn cap headroom
through repeated destroy/rebuild cycles without adding real capacity, and even then the true
bottleneck was ore-tile availability, not the number 18 itself. Lane-count saturation (8/8) was
never once reached by either side in 14 games; it was the dominant, clean bottleneck in exactly
one game (`2618b9b4` g2, v59, 1/8 lanes carrying 17 harvesters' worth of output into an 8.75
Ti/rnd ceiling). The dominant bottleneck, especially on the **current v61 line** where the
coordinator asked for priority, is **builder-hands attrition**: in 2 of 3 v61 games and all 5
of the v56 economy-race losses, our builder-bot count collapses to a sustained near-zero
partway through the match and never recovers — freezing harvester construction, lane wiring, and
conveyor repair simultaneously — well short of both the lane ceiling and ECO_CAP, while a
third v61 game (hive) shows a completely different, non-resource cause: a hardcoded
map-specific "bunker freeze" in `_expand()` (`main.py:1867-1876`) that halts all economic
expansion by design once a home gunner exists past round 42. Stranded in-transit capital is
consistently under 2.5% of delivered Ti everywhere measured and is not a real factor. If
prioritizing one fix for the current line: **builder-bot survivability/replacement after
round ~250** has more measured upside than either raising ECO_CAP or wiring more lanes.
