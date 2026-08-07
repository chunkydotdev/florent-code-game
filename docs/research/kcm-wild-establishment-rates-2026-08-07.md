# KCM wild near-core establishment rates — calibration for C1b, 2026-08-07

**Version tags (rule 2):** target = Kings College Munich (KCM), team id `dfa9be96`,
**v1** in 3 matches (`b3656fe7`, `9a32a859`, `9e41db1a`) and **v7** in 2 matches
(`484095e3`, `4a36151e`) — reported separately throughout, never pooled without
a per-era row, per the task brief. This is a **read-only decode task**: no bot
edits, no matches run, no downloads. Research arm, session 14 (continued).
25 games freshly decoded across 5 matches; `c821193d` (5 more games) is
**cited only**, per instruction — not re-parsed here.

**Corpus and seats** (from each match's `.meta.json`, verified against
`winner`/`team` fields in the replay wire format — team A = wire value 0,
team B = wire value 1, confirmed by cross-checking `scoreA`/`scoreB` against
per-game winners):

| Match | KCM ver | KCM seat | Defender | Defender ver | Defender seat | Score (KCM) |
| --- | --- | --- | --- | --- | --- | --- |
| `b3656fe7` | 1 | A | OpenSverige | 67 | B | 5-0 |
| `9a32a859` | 1 | A | OpenSverige | 68 | B | 4-1 |
| `484095e3` | 7 | A | Pantheon | 36 | B | 0-5 |
| `4a36151e` | 7 | B | team lazy | 94 | A | 0-5 |
| `9e41db1a` | 1 | A | Powered by SmartFridge | 33 | B | 0-5 |

**Parser validated exactly against `tools/replay_census.py -v`** on
`b3656fe7` game 1: unique-gunner dedup (6) + rotations (13) = census's naive
19; economy identity (`ti=1008/972, ti_coll=2950/1890, ammo=28/24`) matched
bit-for-bit. See Method notes for the full chain.

---

## VERDICT — the three numbers C1b needs

1. **Wild establishment distribution (d²≤36 of the defender's core, deduped
   by entity id):** across **30 games** (25 freshly decoded + 5 cited from
   `c821193d`), **median 3, min 0, max 14** per game. Split by KCM version:
   **v1 median 4 (0-14, n=20)**, **v7 median 1.5 (0-4, n=10)** — v1 (live)
   establishes roughly **2.7× more** than v7. Split by defender: against our
   own bots (OpenSverige v67/v68, the weakest defenses in the corpus) median
   **4** (range 2-14); against a genuinely defended core (Pantheon, team
   lazy, SmartFridge) median **1-2** (range 0-7). **cad_probe's ~7/game
   sits at the top of the observed wild range, not the middle** — it is
   closer to the single worst-case game in 30 than to the median.
2. **Simultaneity cap:** max simultaneous alive at d²≤36, across the same 30
   games: **median 2, max 7** (min 0). The one game that hit 7 is a 10×10
   map (`9e41db1a` g5) — flagged below as a radius-cut artifact, not
   necessarily comparable to larger maps. Excluding 10×10 maps, wild max
   simultaneous is **5** (matches `c821193d`'s own cited max of 5). **Recommend
   provisioning C1b's capacity for 7**, since that is the observed ceiling
   and it happens to equal cad_probe's number — but budget the *typical*
   load at 2, not 7, so the ring doesn't over-build for the common case.
3. **Arming round:** the KCM/launcher-insertion **class is recognizable by
   round 1 in 25/25 games (100%)** — either via the r1 launcher build
   (23/25) or, on the two 10×10-map exceptions where KCM skips the launcher
   entirely, via an immediate point-blank gunner at r1 itself. But the
   **actual near-core threat's arrival time is highly variable**: median
   **r12**, p75 **r29**, p90 **r93**, max **r156** (2/25 games, 8%, never
   get a near-core turret at all). The critical edge case for C1b: on 10×10
   maps the threat **is** the recognition signal — zero lead time between
   "this is KCM" and "there is a gunner on your core." On everything else,
   C1b has a comfortable median ~12-round window to react after the
   opening signature fires.

**Ray law: HOLDS in the wild corpus, exactly, on the direction that matters.**
Zero of 54 wild "uncovered" established turrets (by full-lifetime coverage)
were ever hit by a single shot from a defender turret — 0/54, not just
"not killed," literally never fired upon — reproducing `c821193d`'s cited
0/15 exactly. Combined: **0/69 uncovered turrets, across two independent
corpora, ever took defender turret fire.** The other direction is weaker in
the wild: only 19/30 (63%) covered established turrets were actually killed
by turret fire (10/30 survived to game end regardless of coverage — mostly
late arrivals or ammo/timing gaps), vs `c821193d`'s cited 8/8 (100%, but
n=8). Combined **27/38 (71%)**. Coverage is a hard *necessary* condition for
a turret kill (no exceptions, n=69) but not a *sufficient* one in the wider
wild sample — consistent with the `c821193d` addendum's own caveat that
coverage is a per-turret lethality law, not a deterministic kill guarantee.

---

## Per-game table — 25 freshly decoded wild games

Establishment = a KCM gunner/sentinel entity (deduped by id; gunner rotations
re-emit the same id, per `docs/tooling.md`), position fixed at build (turrets
never move), d² measured to the nearest tile of the **defender's** core
footprint. `cov(life)` = covered/uncovered count under the facing-aware ray
predicate (gunner = any of 8 rays reachable by rotation within d²≤13;
sentinel = fixed build-time facing ray within d²≤32), classified over each
turret's full lifetime. `killed@turret` = how many of the established turrets
died to defender turret fire specifically (not builder attacks).

| Match | Game | Ver | Defender | Map | Rounds | Winner | n≤36 | n≤9 | maxSim≤36 | maxSim≤9 | 1st launcher | 1st KCM throw | 1st turret≤36 | 1st turret≤9 | cov/unc(life) | killed@turret |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 484095e3 | g1 | v7 | Pantheon v36 | 18x18 | 256 | defender | 0 | 0 | 0 | 0 | 1 | 2 | — | — | 0/0 | 0 |
| 484095e3 | g2 | v7 | Pantheon v36 | 26x26 | 156 | defender | 4 | 1 | 2 | 1 | 1 | 2 | 30 | 34 | 2/2 | 2 |
| 484095e3 | g3 | v7 | Pantheon v36 | 28x20 | 324 | defender | 1 | 1 | 1 | 1 | 1 | 2 | 4 | 4 | 1/0 | 1 |
| 484095e3 | g4 | v7 | Pantheon v36 | 16x16 | 259 | defender | 3 | 0 | 2 | 0 | 1 | 2 | 16 | — | 1/2 | 1 |
| 484095e3 | g5 | v7 | Pantheon v36 | 28x20 | 99 | defender | 2 | 0 | 2 | 0 | 1 | 2 | 8 | — | 2/0 | 0 |
| 4a36151e | g1 | v7 | team lazy v94 | 18x18 | 66 | defender | 2 | 2 | 2 | 2 | 1 | 2 | 10 | 10 | 0/2 | 0 |
| 4a36151e | g2 | v7 | team lazy v94 | 26x26 | 67 | defender | 1 | 1 | 1 | 1 | 1 | 2 | 58 | 58 | 0/1 | 0 |
| 4a36151e | g3 | v7 | team lazy v94 | 28x20 | 91 | defender | 1 | 1 | 1 | 1 | 1 | 2 | 4 | 4 | 0/1 | 0 |
| 4a36151e | g4 | v7 | team lazy v94 | 16x16 | 73 | defender | 3 | 1 | 3 | 1 | 1 | 2 | 14 | 14 | 2/1 | 2 |
| 4a36151e | g5 | v7 | team lazy v94 | 28x20 | 76 | defender | 1 | 1 | 1 | 1 | 1 | 2 | 5 | 5 | 0/1 | 0 |
| 9a32a859 | g1 | v1 | OpenSverige v68 | 25x25 | 663 | KCM | 8 | 5 | 3 | 2 | 1 | 2 | 17 | 19 | 2/6 | 0 |
| 9a32a859 | g2 | v1 | OpenSverige v68 | 28x20 | 127 | KCM | 5 | 2 | 4 | 1 | 1 | 2 | 5 | 5 | 1/4 | 1 |
| 9a32a859 | g3 | v1 | OpenSverige v68 | 18x18 | 1000 | defender | 2 | 1 | 1 | 1 | 1 | 2 | 12 | 12 | 1/1 | 1 |
| 9a32a859 | g4 | v1 | OpenSverige v68 | 24x24 | 445 | KCM | 4 | 0 | 2 | 0 | 1 | 2 | 38 | — | 2/2 | 2 |
| 9a32a859 | g5 | v1 | OpenSverige v68 | 26x26 | 228 | KCM | 4 | 4 | 4 | 4 | 1 | 2 | 144 | 144 | 0/4 | 0 |
| 9e41db1a | g1 | v1 | SmartFridge v33 | 20x26 | 192 | defender | 0 | 0 | 0 | 0 | 1 | 2 | — | — | 0/0 | 0 |
| 9e41db1a | g2 | v1 | SmartFridge v33 | 26x26 | 233 | defender | 4 | 3 | 4 | 3 | 1 | 2 | 27 | 174 | 0/4 | 0 |
| 9e41db1a | g3 | v1 | SmartFridge v33 | 28x20 | 77 | defender | 1 | 1 | 1 | 1 | 1 | 2 | 5 | 5 | 0/1 | 0 |
| 9e41db1a | g4 | v1 | SmartFridge v33 | 18x18 | 82 | defender | 2 | 2 | 2 | 2 | 1 | 2 | 12 | 12 | 0/2 | 0 |
| 9e41db1a | g5 | v1 | SmartFridge v33 | **10x10** | 209 | defender | 7 | 2 | 7 | 2 | none | none* | 1 | 1 | 6/1 | 0 |
| b3656fe7 | g1 | v1 | OpenSverige v67 | 24x24 | 275 | KCM | 4 | 2 | 4 | 2 | 1 | 2 | 156 | 156 | 0/4 | 0 |
| b3656fe7 | g2 | v1 | OpenSverige v67 | 16x16 | 1000 | KCM | 3 | 2 | 1 | 1 | 1 | 2 | 16 | 16 | 1/2 | 1 |
| b3656fe7 | g3 | v1 | OpenSverige v67 | **10x10** | 455 | KCM | 14 | 13 | 5 | 4 | none | none* | 1 | 1 | 9/5 | 8 |
| b3656fe7 | g4 | v1 | OpenSverige v67 | 20x26 | 124 | KCM | 4 | 3 | 3 | 2 | 1 | 2 | 3 | 3 | 0/4 | 0 |
| b3656fe7 | g5 | v1 | OpenSverige v67 | 26x26 | 157 | KCM | 4 | 1 | 3 | 1 | 1 | 2 | 102 | 134 | 0/4 | 0 |

\* On the two 10×10-map games, KCM never builds a launcher and never throws
its own builders (matching the classification doc's "10×10 branch: no
launcher, point-blank gunners r1/r2"). "1st KCM throw" columns show "none"
by the corrected definition (a throw attributed to a **KCM-owned** launcher —
see Method notes on the ownership-inversion trap this avoided).

---

## Cited: `c821193d` (v68 vs KCM v1, 5 games) — CITED, not re-decoded

Per instruction, these rows are **quoted from `docs/research/kcm-win-c1-validation-2026-08-07.md`**,
not re-parsed. `n≤9` is **derived** from the per-turret d² values given in
that doc's Q1 section (marked UNCERTAIN where the doc didn't enumerate every
turret's d²).

| Game | Map | Rounds | Winner | n≤36 (cited) | n≤9 (derived) | maxSim≤36 (cited) | maxSim≤9 (derived) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| g1 | 18x18 | 97 | us (WIN) | 3 | 3 (d²=8,2,4, all held simultaneously r19-r96) | 3 | 3 |
| g2 | 20x26 | 1000 | us (WIN) | 1 | 1 (d²=4) | 1 | 1 |
| g3 | 25x25 | 114 | us (WIN) | 2 | 2 (d²=8,9, overlapped r44-r62) | 2 | 2 |
| g4 | 24x24 | 659 | us (LOSS) | 2 (**of 4 total established over the game**, only 2 ever simultaneous) | 1 (only #159 d²=4 qualifies of the 4 named turrets) | 2 | 1 |
| g5 | 26x26 | 458 | us (LOSS) | 5 (of **13** established over the game) | **UNCERTAIN** — only 2 of 13 turrets' d² are given in the source doc (both d²=1, same tile (7,5), sequential builds) | 5 | **UNCERTAIN**, ≥1 |

Coverage law, cited verbatim from `c821193d`'s VERDICT section (its own
predicate is the full-lifetime classification, same definition used above):
**COVERED n=8, 8/8 killed by our turret fire, 0 survived. UNCOVERED n=15,
0/15 killed by turret fire (6 killed by builder attacks, 9 survived to game
end).**

---

## Distribution summary

**Establishment count at d²≤36, all 30 games (25 wild + 5 cited):**
min **0**, median **3**, max **14**. Full sorted list:
`0,0,1,1,1,1,1,1,2,2,2,2,2,3,3,3,3,4,4,4,4,4,4,4,4,5,7,8,13,14`.

**By KCM version (wild-only, n=25; cited `c821193d` is v1 but not merged
into this split since only aggregate n=23-across-5-games is cited, not
per-game — folding it in would not change the medians materially):**

| Version | n games | n≤36 median | n≤36 range | maxSim≤36 median |
| --- | --- | --- | --- | --- |
| v1 (wild, n=15) | 15 | 4 | 0-14 | 3 |
| v7 (wild, n=10) | 10 | 1.5 | 0-4 | 1.5 |

**By defender identity (wild-only, n=25):**

| Defender | n games | n≤36 values | maxSim≤36 values |
| --- | --- | --- | --- |
| OpenSverige (v67/v68, our own bots) | 10 | 2,3,4,4,4,4,4,5,8,14 | 1,1,2,3,3,3,4,4,4,5 |
| Pantheon v36 | 5 | 0,1,2,3,4 | 0,1,2,2,2 |
| Powered by SmartFridge v33 | 5 | 0,1,2,4,7 | 0,1,2,4,7 |
| team lazy v94 | 5 | 1,1,1,2,3 | 1,1,1,2,3 |

**Interpretation:** KCM establishes roughly **double** the near-core turrets
against our own (undefended) bots than against opponents with any kind of
active defense — Pantheon (barrier walls) held it to a median of 2, team
lazy (fast rush that kills KCM before it can build much) to a median of 1.
This is direct evidence a competent defense **can** suppress establishment
close to zero (`484095e3` g1: **zero** KCM turrets ever got within d²≤36 of
Pantheon's core, in a 256-round game) — which is exactly the outcome C1b is
being built to achieve.

**Covered-vs-uncovered lifetime split, combined wild + cited (n=69
uncovered, n=38 covered, across 30 games / 2 corpora):**

| | n | killed by defender turret fire | survived to game end | killed by builder attacks |
| --- | --- | --- | --- | --- |
| **COVERED (lifetime)** | 38 (30 wild + 8 cited) | **27 (71%)** | 10 (wild only; cited had 0) | 1 (wild only) |
| **UNCOVERED (lifetime)** | 69 (54 wild + 15 cited) | **0 (0%)** | 39 (wild) + 9 (cited) = 48 | 15 (wild) + 6 (cited) = 21 |

Median lifetime: covered established turrets that die average a **short**
life (wild-only covered lifespan median 13 rounds); uncovered turrets that
survive live far longer (wild-only uncovered lifespan median 51.5 rounds) —
same shape as the `c821193d` addendum's independent n=405 replication
(covered median 8-11 rounds vs uncovered 81-105).

**Arming-gate percentiles, wild n=25 (rounds until first near-core turret at
d²≤36; "—" = never happens in that game):**

| Percentile | Round |
| --- | --- |
| p0 (min) | 1 |
| p50 (median) | 12 |
| p75 | 29 |
| p90 | 93 |
| p100 (max) | 156 |
| never established | 2/25 games (8%) |

Class-recognition signal (r1 launcher build, or on the 10×10 no-launcher
branch, the r1 point-blank gunner itself) fires in **25/25 games at round 1
(100%)** — always at or before the earliest possible near-core threat, with
zero lead time only on 10×10 maps.

---

## Contrast: cad_probe's ~7/game vs the wild distribution

The builder's C1 home-ring experiment reported **~7 enemy turrets
established near our core per game against cad_probe** (relayed number, not
independently verified here — UNCERTAIN on exact decimal). Against the wild
distribution measured here (median 3, max 14, n=30 combined):

- **7 sits above the wild median (3) but below the wild max (14)** — roughly
  the 80th-85th percentile of the combined 30-game sample.
- It exactly **equals the wild simultaneity ceiling** (max simultaneous
  alive = 7, `9e41db1a` g5), though that ceiling game is a 10×10 map, a
  size class that mechanically inflates any fixed-radius establishment
  count (see caveat below).
- Against a genuinely defended core (Pantheon, team lazy, SmartFridge),
  median establishment is **1-2**, four to seven times lower than cad_probe's
  ~7. **cad_probe is calibrated closer to "KCM unleashed on an undefended
  core" than to "KCM vs. a competent defense"** — which is arguably correct
  for stress-testing C1b's capacity, but means the *typical* game C1b will
  actually see (once it's doing its job) should look far closer to the
  Pantheon/team-lazy column (median 1-2) than to cad_probe's number.

---

## Method notes

**Reused artifact:** `decode.py` in the session scratchpad
(`/private/tmp/claude-501/.../0a67ca71-984b-4cfe-8807-172307619ab7/scratchpad/decode.py`)
is the walker built for the `c821193d` decode (its own header confirms this:
`"""Scratch decoder for match c821193d..."""`). It wraps
`tools/replay_census.py`'s wire-format primitives (`fields`/`scalars`/
`read_pos`/`packed_varints`/`KIND_FIELDS`) into a `Game` class that replays
every turn's protobuf events (`placeEntity`, `moveBuilderBot`,
`removeEntity`, `updateHp`, `updatePlayers`, `fireTurret`, `builderAttack`,
`coreConvertAmmo`, `builderHeal`) and **dedupes `placeEntity` by entity id**
(gunner rotations re-emit the same id and only change `direction`/`hp`,
tracked separately in `self.rot`) — this is the mandatory dedup from
`docs/tooling.md`. Reused as-is for all 25 games in this task; new work was
a generalized, team-parametrized ray-coverage/establishment script
(`wild_establishment.py`, same scratchpad directory) built on top of it,
since the existing `analyze5.py` was hardcoded to `c821193d`'s "us=team 0"
assumption and this task's 5 matches have KCM on **either** side (team B in
`4a36151e`).

**Cross-validation performed:** `b3656fe7` game 1 parsed independently
against `tools/replay_census.py -v`. Exact matches on: map/cores/terrain,
first-build rounds and positions for every entity type, end-of-game alive
counts, and the full economy row (`titanium 1008/972, ti_collected
2950/1890, ammo 28/24`). One apparent mismatch resolved: `replay_census.py`'s
"total built" column reports 19 KCM gunners where this parser counts 6 —
confirmed as **expected**, not a bug: census's built-count is the **naive**
(non-deduped) `placeEntity` count, and 6 unique + 13 rotations = 19 exactly,
matching the same fact already documented in
`docs/research/kings-college-classification-2026-08-07.md`'s parser note
("6 unique gunners + 13 rotations = the 19 the naive count reports"). This
is independent confirmation the dedup logic in the reused walker is correct.

**Throw-attribution fix applied (worth flagging for future decodes):** a
naive "first throw" signal — the earliest round any KCM-team builder bot
moved more than 1 tile — falsely fired at r38 in `9e41db1a` g5, a 10×10 map
where the classification doc establishes KCM has **no launcher at all**.
Investigating: the "thrower" was launcher #30, **team 1 (the SmartFridge
defender)**, at d²=2 from the pre-throw tile — i.e. the defender's own
launcher picking up and flinging away a KCM raider, exactly the
ownership-inversion pattern documented in `docs/tooling.md` and
`docs/research/kings-college-classification-2026-08-07.md` §6 item 1 ("the
defender recycling the attacker's raiders, not an attacker ferry"). Fixed by
attributing every throw's owner to whichever launcher (either team) is alive
at d²≤2 of the pre-throw tile (the corrected rule from `docs/tooling.md`),
then filtering "first KCM-initiated throw" to require the **thrower's**
team, not the thrown bot's team, to equal KCM. This surfaced **dozens** of
similar long-running defender-recycling-raiders loops across the corpus
(logged in the scratchpad's `wild_establishment_report2.txt`, e.g.
`9a32a859` g1: launcher #30, team 1, threw KCM raiders `(19,15)→(20,11)`
over 100+ times between r64-r639) — none of it changed any "first throw"
answer in this corpus (KCM's own r2 throw always precedes any defender
recycling), but an unfixed version would have reported a false r38 "first
throw" for one game and silently misattributed volume in several others had
throw *counts* been part of this deliverable.

**10×10 map caveat (UNCERTAIN, flagged not resolved):** the two 10×10 games
(`b3656fe7` g3, `9e41db1a` g5) show the corpus's highest establishment
counts (14 and 7) and the only "no launcher" behavior, consistent with the
classification doc's documented map-size branch. A fixed d²≤36 cut on a
10×10 grid covers a much larger *fraction* of the map than the same cut on
a 24×24+ grid, so these two data points are not apples-to-apples with the
rest of the corpus for a "how far from the core is dangerous" reading —
they are included in all headline stats above (per the brief's instruction
to report from parsed replays without cherry-picking), but C1b's capacity
math should weight them cautiously if the ring is being sized primarily for
large maps.

**Establishment/coverage kind scope:** established = KCM **gunner or
sentinel** only (matching the ray-coverage predicate's own scope). KCM
launchers were checked separately and never appear within d²≤36 of a
defender core in any of the 25 games (consistent with the classification
doc: the only launcher is destroyed at r6 on its own core-adjacent tile).

**Scripts, in the session scratchpad (read-only artifacts, not committed to
the repo):** `decode.py` (reused, c821193d walker), `wild_establishment.py`
(new, this task), raw output `wild_establishment_out.json` and
`wild_establishment_report2.txt`.
