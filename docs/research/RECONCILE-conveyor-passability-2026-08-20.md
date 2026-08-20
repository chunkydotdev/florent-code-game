# RECONCILE — are conveyors bot-passable? (2026-08-20, research arm, DECODE-ONLY)

Routed by `docs/research/BUILD-REPORT-v530home-2026-08-20.md:665-669` ("ENGINE
CONFLICT ROUTED TO RESEARCH"). No game was run for this document; every number
below is decoded from replays already on disk.

## VERDICT IN ONE LINE

**Builder bots walk onto conveyors and splitters of either team, at scale, on the
currently pinned engine, today.** Decoded on the wire: **10,953,480 walks onto an
OWN conveyor and 2,072,144 onto an ENEMY conveyor across 8,859 platform replays**
(pre-2026-08-10 population), and **229,308 own-conveyor walks in 800 LOCAL replays
generated 2026-08-20 08:34 on `fcode 2.3.6`** — the same pinned engine
(`tools/ENGINE_PIN` = 2.3.6; `.venv/lib/python3.13/site-packages/fcode/fcode_engine.cpython-313-darwin.so`
mtime 6 Aug 10:15, unchanged) the fresh probe ran against.

The conflict is therefore **not** about the engine's behaviour. It is confined to
what the two *predicates* the probe called (`can_move`, `is_tile_passable`)
returned in that probe's specific state.

## INSTRUMENTS

* `scratchpad/s52_conv/convtape.py` — classifies every builder-bot arrival on a
  tile by the building standing there at arrival. Three channels: **WALK**
  (`moveBuilderBot`, d²≤1), **THROW** (`moveBuilderBot`, d²≥2), **SPAWN** (first
  `placeEntity` of a builder id).
* `scratchpad/s52_conv/ringtrace.py` — for every core-heal `UpdateHp`, buckets the
  team's bodies on the core's 8 ring sockets by *how they arrived*.
* Snapshots (keeper rewrites in place): `scratchpad/s52_conv/meta_join.snap.tsv`
  (78,857 lines, counted twice, md5 `5a4ac067c20623e8da25a12e388cd131`) and
  `throws.snap.tsv` (1,020,246 lines, counted twice).

### Both-verdicts controls, every run

| control | expected | measured |
|---|---|---|
| **POSITIVE — throw population vs the banked instrument.** convtape THROW count vs `corpus/throws.tsv` rows, same 1,500 files | agree | **23,329 = 23,329, exact** |
| **NEGATIVE — impassable classes** (harvester/barrier/gunner/sentinel/launcher/core) under an arriving body | ~0 | **0** in every channel, all 14 days, both local sets |
| **NEGATIVE — WALL arrivals** (independent terrain channel) | 0 | **0** everywhere (`walls={}`) |
| **MUTATION — `--shift +1,0`** on the 2026-08-19 sample | classifier must produce the *other* verdict | conveyor% 34.50 → **24.97**, impassables 0 → **18,840** |
| **MUTATION — `--shift +3,+3`** | collapse toward background | conveyor% → **14.26** vs background conveyor tile density **9.17%**, impassables **13,544** |
| **ORDERING — `--prevround`** (occupancy as of end of previous round) | verdict must not rest on intra-round event order | conveyor% **34.41** vs 34.50; impassables **95** (0.04%: buildings destroyed then walked into, same round) |

The negative controls are the load-bearing ones: a decoder that manufactures
conveyor hits by positional coincidence manufactures harvester hits too. It reads
exactly zero on 27.7M walk arrivals, and the shift mutation proves it *can* report
nonzero.

## H(c) — ENGINE CHANGED SINCE 2026-08-10? **REFUTED.**

120 platform replays sampled per day, `completedAt` from the meta_join snapshot.

| day | walks | walk→conveyor% | own% | enemy% | IMPASSABLE | throws | throw→conv% | spawns | spawn→conv% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-08-07 | 409,560 | 44.50 | 35.42 | 9.08 | **0** | 2,364 | 25.59 | 1,886 | 16.22 |
| 2026-08-08 | 372,856 | 49.94 | 43.21 | 6.73 | **0** | 3,178 | 31.59 | 2,434 | 37.80 |
| 2026-08-09 | 345,788 | 49.89 | 42.89 | 7.00 | **0** | 1,835 | 26.27 | 1,910 | 19.37 |
| 2026-08-10 | 245,204 | 40.04 | 32.86 | 7.18 | **0** | 1,005 | 8.66 | 1,641 | 13.59 |
| 2026-08-11 | 258,514 | 35.41 | 29.45 | 5.96 | **0** | 1,238 | 21.89 | 1,886 | 18.03 |
| 2026-08-12 | 300,911 | 35.75 | 29.19 | 6.56 | **0** | 977 | 53.94 | 2,206 | 21.40 |
| 2026-08-13 | 269,649 | 34.73 | 26.18 | 8.55 | **0** | 796 | 9.55 | 2,094 | 16.62 |
| 2026-08-14 | 292,241 | 36.74 | 28.89 | 7.84 | **0** | 1,011 | 2.87 | 1,883 | 17.68 |
| 2026-08-15 | 254,339 | 38.35 | 29.37 | 8.98 | **0** | 388 | 25.26 | 1,803 | 21.02 |
| 2026-08-16 | 291,331 | 41.78 | 30.83 | 10.95 | **0** | 1,135 | 0.88 | 1,763 | 22.92 |
| 2026-08-17 | 220,069 | 35.60 | 29.00 | 6.60 | **0** | 1,782 | 15.04 | 1,960 | 26.28 |
| 2026-08-18 | 255,387 | 40.92 | 34.14 | 6.78 | **0** | 1,723 | 26.58 | 1,803 | 23.52 |
| 2026-08-19 | 224,457 | 34.50 | 27.21 | 7.29 | **0** | 1,021 | 11.46 | 1,661 | 20.89 |
| **2026-08-20** | **267,369** | **39.90** | **30.65** | **9.25** | **0** | 2,161 | 13.28 | 1,827 | 18.06 |

**No cliff.** The walk channel is flat in a 34.5–49.9% band from 08-07 through
today; the spawn channel is flat in a 13.6–37.8% band. Per-day throw shares swing
0.88–53.94% but the denominators are 388–3,178 throws — that column is noise, not
a trend, and it never reaches zero. The `.so` and the pin are unchanged since
6 Aug. **INFERENCE:** an engine change cannot be the explanation, because the
behaviour is present in replays written hours before the probe on the same binary.

## H(b) — OWN vs ENEMY CONVEYOR ASYMMETRY? **REFUTED, and it points the wrong way.**

Full pre-2026-08-10 platform population, 8,859 replays:

| channel | n | empty | conveyor_own | conveyor_enemy | splitter | IMPASSABLE | walls |
|---|---:|---:|---:|---:|---:|---:|---:|
| WALK | 27,725,317 | 52.95% | **39.51%** | **7.47%** | 0.07% | **0** | 0 |
| THROW | 147,547 | 72.29% | **23.05%** | **4.66%** | 1 event | **0** | 0 |
| SPAWN | 156,213 | 75.45% | **23.59%** | **0.87%** | 0.09% | **0** | 0 |

Own conveyors are not merely permitted, they are **5.3× more common than enemy
ones on the walk channel**. Any rule banning bodies from own conveyors would have
had to suppress 10.9M events. There is no asymmetry to find.

## H(d) — ARE THE BODY-ON-CONVEYOR DECODES ARTIFACTS? **REFUTED.**

Two independent attacks.

**(i) Corpus-wide: could a "walk" be a disguised 1-tile launcher throw?** A throw
needs a launcher of either team within d²≤2 of the bot's *pre-move* tile. Split
every conveyor walk on that:

| population | conveyor walks | **no launcher in pickup range** | launcher in range (ambiguous) |
|---|---:|---:|---:|
| platform 2026-08-18..20, 1,500 replays | 1,075,896 | **1,055,390 (98.09%)** | 20,506 (1.91%) |
| local `s51_vs_holder`, 900 replays | 429,433 | **384,235 (89.47%)** | 45,198 (10.53%) |
| local `s51_v530_build/headA`, 800 replays | 284,271 | **266,181 (93.64%)** | 18,090 (6.36%) |

Per-day on the platform sample the launcher-free share is **93.27–99.57%**. The
sampled examples land in games with **`launchers_alive: 0`** — e.g.
`replay_archive/0739732d-3614-43dd-baf5-4d08558e0c72_game_3.replay26` r15, bot 5
team 0, (2,8)→(2,9) onto `conveyor/team0`, no launcher in the game.

**(ii) The ring study's own fixture.** `ringtrace.py` over all **900 replays in
`scratchpad/s51_vs_holder/rep/`** — the RING-ENGAGEMENT instrument's population.
Unit of observation is **(core-heal event × own body on a ring socket)**, *not*
distinct heals, so this denominator is not comparable to the ring study's
772/2,332; it answers only the mechanism question.

| body standing on | WALKED (no launcher near) | WALKED? (launcher in range) | THROWN | SPAWNED | total |
|---|---:|---:|---:|---:|---:|
| **own conveyor** | **194,848 (84.90%)** | 24,225 (10.56%) | **26 (0.011%)** | 10,389 (4.53%) | **229,488** |
| enemy conveyor | 283 | 0 | 0 | 0 | 283 |
| bare tile | 132,041 | 4,668 | 0 | 5,579 | 142,288 |
| **impassable building (decoder alarm)** | — | — | — | — | **0 — bucket never fired** |

**Bodies reach those sockets by walking, 84.9% of the time with no launcher
anywhere in pickup range.** Thrown accounts for 26 of 229,488 (0.011%). The
"positional coincidence / off-by-one" artifact class would have populated the
ALARM row; it is empty.

## H(a) — DOES THE THROW-LANDING CHECK DIFFER FROM `is_tile_passable`? **NOT NEEDED — and the old doc's predicate NAME is the only part this work cannot verify.**

The hypothesis exists to explain why throws could land on conveyors while walking
could not. **That gap does not exist**: the walk channel is the *larger* of the
two. So (a) explains nothing that needs explaining.

What the 2026-08-09 doc actually wrote
(`docs/research/post-throw-tile-dwell-2026-08-09.md:330-344`), verbatim:

> "So the throw-target legality rule is **`is_tile_passable`, not
> `is_tile_empty`** — and a builder bot may stand on a conveyor or splitter of
> *either* team, but never on a turret, harvester, barrier, core, or another bot."

**RIGHT, and it reproduces exactly.** Its distributional shape reproduces down to
a fingerprint: the doc's table has a lone `splitter, opposing team | 1`; the full
pre-08-10 re-derivation has **`splitter_enemy` = 1**. Its exact-zero for
turret/harvester/barrier/core reproduces on 27.7M walk arrivals as well as on
throws.

**WRONG only in the headline number's advertised generality.** The doc's
**33.5%** is its own 97,999-throw subset. Re-derived on the *complete*
pre-2026-08-10 archive (147,547 throws, 8,859 files) the figure is **27.71%**;
pooled across three later 1,500-replay eras (55,656 throws) it is **15.89%**, and
by era **24.39% (08-08..10) → 8.96% (08-13..15) → 10.09% (08-18..20)**. That
decline is field composition (fewer belts under throw lanes), **not** legality —
the walk channel barely moved and the impassable classes stayed at exactly 0.

**UNVERIFIED, and it is the live residual:** this document decoded *behaviour*.
It never called `is_tile_passable`. Naming that specific predicate as the landing
gate was an inference in 2026-08-09 and remains one. **INFERENCE:** the probe's
result is consistent with `is_tile_passable` being STRICTER than actual movement
legality (an API predicate that reports "no" on a tile a bot demonstrably occupies
7-figure times), with `can_move` having returned False for a state reason —
act/move mutual exclusivity, or `move_cooldown != 0` — rather than for terrain.
That is a hypothesis, not a finding, and only a re-probe settles it.

## THE CORRECTED ENGINE SENTENCE

**DECISIVE — promote to `CLAUDE.md` / the tactics atlas:**

> Builder bots occupy conveyor and splitter tiles of **either** team, and reach
> them by **walking** (the dominant path), by **launcher throw**, and by **core
> spawn**. Turret, harvester, barrier, core and occupied-bot tiles are never
> occupied by an arriving body. Measured on the wire, 2026-08-20: 27,725,317 walk
> arrivals across 8,859 platform replays, **47.05% onto a conveyor/splitter, 0
> onto any impassable class**; flat 08-07 → 08-20; reproduced on the pinned local
> engine `fcode 2.3.6` in replays written the same day.

**PROPOSED — do not promote until re-probed:**

> `is_tile_passable(pos)` may be STRICTER than movement legality and report False
> on a conveyor tile a builder can legally stand on. Do not use it as the test for
> "can my body seat here"; test `can_move(direction)` from a bot with
> `get_move_cooldown() == 0` that has not acted this round, or read
> `get_tile_building_id` and exclude the impassable set explicitly.

## DOWNSTREAM CLAIMS AND WHICH WAY EACH MOVES

| claim | site | direction |
|---|---|---|
| **Mjolnir socket-heal reasoning** — "772 of 2,332 own-socket core heals came from a body standing on its own conveyor" | `bots/_x3r0v162mjolnir/DOCTRINE.md:116-122` (TRACK 3); `docs/research/RING-ENGAGEMENT-mjolnir-2026-08-20.md` | **STANDS, unchanged.** The mechanism is confirmed on the ring study's own 900-replay fixture: 229,488 socket-body heal observations on own conveyors, 84.9% arrived by walking. |
| **x3r0 OPENING.md §G: "passable = empty/ore/conveyors+splitters of either team"** (quoted at `DOCTRINE.md:117`) | as quoted | **STANDS.** Matches the wire exactly, including the either-team half (7.47% of walks are onto enemy conveyors). |
| **heal-outrun mechanism** (healer seated on the belt) | `docs/research/RING-ENGAGEMENT-mjolnir-2026-08-20.md` | **STANDS.** No re-pricing needed. |
| **ring heal-seat cost** — RING held OFF "pending the passability conflict" | `docs/research/BUILD-REPORT-v530home-2026-08-20.md:661-663` | **BLOCKER REMOVED.** The passability premise is intact; RING's OFF/ON decision returns to its own evidence (+4.38 wins inside interval). |
| **`HS_SEAT_BAN_CONVEYORS = False`** and its stated basis ("a PAVED seat does not actually deny a healer the seat — a builder can stand on the conveyor and heal") | `bots/_v525flip/doctrine.py:600-614` | **STANDS — its premise is now measured rather than cited.** The flag's default needs no change. The `docs/game-model.md:226-227,357` sentences it quotes are correct as written. |
| **Builder's statement to Magnus: "healers stand on conveyors" / conveyors measured NOT bot-passable (18/18)** | `docs/research/BUILD-REPORT-v530home-2026-08-20.md:665-667` | **SPLIT. "Healers stand on conveyors" is CONFIRMED and should be restated to Magnus as confirmed.** "Conveyors are not bot-passable" must be **RETRACTED as an engine claim** and narrowed to a predicate-level observation about `is_tile_passable`/`can_move` in that probe's state, pending a re-probe. |
| **Atlas row 5: "33.5% of throws land on a conveyor/splitter of either team; 0% on turret/harvester/barrier/core/another bot"** | `docs/research/BUILDER-TACTICS-ATLAS-2026-08-14.md:51` | **NUMBER DOWN, CLAIM INTACT.** Replace 33.5% with **27.71% (full pre-08-10 archive, 147,547 throws)** and add the era range **24.4% → 9.0% → 10.1%**. The 0% half reproduces exactly. |
| **"40.1% of all spawns land on a conveyor tile"** (used to refute spawn-denial) | `docs/research/SWARM-BAIT-MASS-2026-08-14.md:180`; `docs/research/PROBE-DOSSIER-ferry-siege-2026-08-17.md:40`; `loki-arsenal-pricing-2026-08-09.md:342` | **DIRECTION CONFIRMED, MAGNITUDE DOWN.** Independently re-derived here at **24.55%** on the pre-08-10 population and **20.1–20.9%** in every later era. Occupancy-is-not-blocking still holds. |

## NON-COVERAGE

1. **No API call was made.** Everything here is engine *behaviour* off the wire.
   The `is_tile_passable` question is left open by construction (decode-only brief).
2. **1-tile throws remain indistinguishable from walks** — the same limit
   `post-throw-tile-dwell-2026-08-09.md` §NON-COVERAGE 1 names. Handled by the
   launcher-proximity split, which bounds the contamination at 1.91–10.53%
   rather than eliminating it.
3. **Per-day samples are 120 replays**, chosen with a fixed seed from the
   meta_join snapshot; the era and pre-08-10 cuts are 1,500 and 8,859 files. These
   are decode censuses of an existing archive, not a fixture comparison — no DEFF
   applies (no bar is being cleared and no share is being compared across
   fixtures).
4. **`ringtrace` observations are heal-event × body pairs**, so a long-lived
   seated body is counted once per heal it witnesses. That inflates the absolute
   count and does not affect the arrival-mode *proportions*, which are the finding.
