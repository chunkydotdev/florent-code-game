# DECODE — KLADDEDOSE leg, 25 games, v177 vs kladde v173 (pinned)

**Decoded 2026-08-21** (repo clock; see commit time). **This page reports
measured quantities only. It contains no verdict, no bar reading and no
gate call — the builder types those against the locked gate.**

Definitions are taken from the LOCKED prereg
`docs/prereg/PREREG-LEG-KLADDEDOSE-2026-08-21.md` §MECHANISM METRIC and
§HP-GATE, and they bind. Nothing below is redefined for convenience.

---

## 0. Provenance, sides, and the pin

Five unrated matches, `triggeredBy: unrated`, `rated: false`, all created
`2026-08-21T13:19:36Z`–`13:19:50Z`. **Our side is resolved from each match's
`teamAName`/`teamBName`, never assumed** — the leg contains one match where we
are team B:

| match | our side | opp version | `sourceMatch*` (the pin) | score (us–them) |
|---|---|---|---|---|
| `6db3add5` | **A** | **173** | srcB `6ce2d9b6…` | 1–4 |
| `6bf8980e` | **A** | **173** | srcB `6ce2d9b6…` | 0–5 |
| `73e920b9` | **B** | **173** | srcA `6ce2d9b6…` | 0–5 |
| `7c3e9ae0` | **A** | **173** | srcB `6ce2d9b6…` | 0–5 |
| `99bb733a` | **A** | **173** | srcB `6ce2d9b6…` | 0–5 |

**OPPVER ALARM CLAUSE: 0 of 25 games flagged.** Every decoded `oppver` is
**173**; the pin took on all five accepts, including the one where the sides are
reversed. Our version is **177** in all five.

`99bb733a` was not archived at task start. It was fetched through the
archiver's own documented **PRIORITY REQUESTS** path
(`tools/monitors/replay_archiver.py` docstring: *"either arm may append match
ids … Research names ids; the archiver serves them first"*), then one archiver
cycle was run. Read-only download; no platform match was created.

**Metric definitions as implemented** (`scratchpad/s53_kladdedose/peckdecode.py`):

| # | quantity | definition (prereg-bound) |
|---|---|---|
| 1 | **ARRIVAL** | ≥1 round in which one of OUR builder bots occupies a tile **ORTHOGONALLY adjacent** to the enemy core's 2×2 footprint. ⛔ **Not d²≤2** — that admits diagonals. `arr_d2_r` is carried in the TSV as a cross-check only. |
| 2 | **PECK EVENTS** | update field 13 `BuilderAttack {id, target}` where the attacker is OURS and `target` ∈ enemy core footprint — the attribution rule of `tools/corpus/replay_autopsy.py:212-231`. |
| 3 | **PECK-ATTRIBUTED CORE HP** | enemy-core `UpdateHp` deltas of exactly **−2** in a round carrying ≥1 event of type (2). (`hp2_any`, every −2 regardless of coincidence, is decoded alongside so a disagreement would be visible.) |
| 4 | **ADJACENT-MIN** (mandatory decomposition) | minimum enemy-core HP over rounds in which ≥1 of our builder bots was orthogonally adjacent. HP reconstructed from 500 + the cumulative signed `UpdateHp` stream; end-of-round HP, end-of-round positions — the arrival convention `launchtime.py`/`ringrace.py` already use. **≤120 is the redirect path's finishing gate** (`siege.py:4479`, `doctrine.py:5963`). |

---

## 1. INSTRUMENT VALIDATION — driven to both verdicts, three ways

⛔ **A `peck_events` column that has only ever read 0 validates nothing.** This
is the prereg's own OB17 risk, so the zero below is backed by three separate
controls, two of them inside the leg population itself.

1. **Positive fixture** (`--selftest`, the builder's own `bots/_probe_peck_*`
   run): `scratchpad/s53_peckdrive/peck_skald2.replay26` reads
   **`peck_events=250`, `hp2_coincident=250`, `adj_min_hp=0`**. 250 events × 2 HP
   = **500 HP**, reproducing the builder's banked `total=500 MATCH`
   digit-for-digit on an independently written decoder.
2. **Negative fixture**: `peck.replay26` reads **0 / 0** on both sides.
3. ⭐ **MIRROR CONTROL INSIDE THE LEG, and it is the strongest of the three.**
   In `7c3e9ae0` game 3 the OPPONENT pecked a core. Running the same decoder on
   the same file with the sides swapped turns **every** column over:

```
7c3e9ae0 g3, our_team=A (per meta):  peck_events=0  hp2_coincident=0  converted=0  adj_min_hp=500
7c3e9ae0 g3, sides swapped (kladde): peck_events=2  hp2_coincident=2  converted=1  adj_min_hp=10   first_peck_r=297
```

**FALSE-ZERO GUARD — field 13 fires 2,895 times across the 25 games**, so the
channel is present and read on this surface. Full classification of every
builder attack (`scratchpad/s53_kladdedose/attack_classes.txt`):

| attacker | target class | events |
|---|---|---|
| **ours** | enemy conveyor | **1,917** |
| **ours** | empty tile | 52 |
| **ours** | **ENEMY CORE** | **0** |
| theirs | our conveyor | 737 |
| theirs | empty tile | 76 |
| theirs | our harvester / sentinel / launcher | 45 / 40 / 26 |
| theirs | **ENEMY CORE (= our core)** | **2** |

⇒ **Our builders made 1,969 attacks in this leg and 0 of them targeted a core.
Theirs made 926 and 2 of them did.** The decoder sees pecks where they exist and
zeros where they do not.

---

## 2. The 25-row table

`arr_r` = first arrival round (orthogonal, 0-indexed). `arr_rnds` = number of
rounds with ≥1 of our builders orthogonally adjacent. `peck` = metric (2).
`hp2` = metric (3). `adjmin` = metric (4). `≤120` = `adjmin ≤ 120`.

| # | match | g | map | side | oppver | rounds | we won | **arr** | **arr_r** | arr_rnds | **peck** | **hp2** | **adjmin** | **≤120** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 6db3add5 | 1 | longhouse | A | 173 | 523 | no | ✓ | 19 | 101 | 0 | 0 | 500 | no |
| 2 | 6db3add5 | 2 | holmgang\|inv_small12 | A | 173 | 1000 | no | ✓ | 8 | 389 | 0 | 0 | 500 | no |
| 3 | 6db3add5 | 3 | fimbulwinter | A | 173 | 179 | no | ✓ | 16 | 127 | 0 | 0 | 500 | no |
| 4 | 6db3add5 | 4 | valkyrie | A | 173 | 411 | **YES** | ✓ | 12 | 65 | 0 | 0 | **340** | no |
| 5 | 6db3add5 | 5 | icefloe | A | 173 | 301 | no | ✓ | 31 | 83 | 0 | 0 | 500 | no |
| 6 | 6bf8980e | 1 | skald | A | 173 | 153 | no | ✓ | 10 | 54 | 0 | 0 | 500 | no |
| 7 | 6bf8980e | 2 | valkyrie | A | 173 | 371 | no | ✓ | 12 | 98 | 0 | 0 | **472** | no |
| 8 | 6bf8980e | 3 | paths | A | 173 | 281 | no | ✓ | 20 | 66 | 0 | 0 | 500 | no |
| 9 | 6bf8980e | 4 | bifrost | A | 173 | 268 | no | ✓ | 11 | 107 | 0 | 0 | 500 | no |
| 10 | 6bf8980e | 5 | longhouse | A | 173 | 425 | no | ✓ | 19 | 147 | 0 | 0 | **440** | no |
| 11 | 73e920b9 | 1 | holmgang\|inv_small12 | **B** | 173 | 497 | no | ✓ | 8 | 22 | 0 | 0 | 500 | no |
| 12 | 73e920b9 | 2 | stavkirke | **B** | 173 | 167 | no | ✓ | 10 | 104 | 0 | 0 | 500 | no |
| 13 | 73e920b9 | 3 | bifrost | **B** | 173 | 167 | no | ✓ | 11 | 17 | 0 | 0 | 500 | no |
| 14 | 73e920b9 | 4 | glacierkeep | **B** | 173 | 127 | no | ✓ | 12 | 78 | 0 | 0 | 500 | no |
| 15 | 73e920b9 | 5 | paths | **B** | 173 | 162 | no | ✓ | 11 | 119 | 0 | 0 | 500 | no |
| 16 | 7c3e9ae0 | 1 | auroraveil | A | 173 | 158 | no | ✓ | 15 | 63 | 0 | 0 | 500 | no |
| 17 | 7c3e9ae0 | 2 | icefloe | A | 173 | 297 | no | ✓ | 31 | 105 | 0 | 0 | 500 | no |
| 18 | 7c3e9ae0 | 3 | fimbulwinter | A | 173 | 316 | no | ✓ | 21 | 205 | 0 | 0 | 500 | no |
| 19 | 7c3e9ae0 | 4 | midgard\|ragnarok | A | 173 | 213 | no | ✓ | 64 | 149 | 0 | 0 | **464** | no |
| 20 | 7c3e9ae0 | 5 | longhouse | A | 173 | 577 | no | ✓ | 19 | 344 | 0 | 0 | 500 | no |
| 21 | 99bb733a | 1 | longhouse | A | 173 | 300 | no | ✓ | 19 | 150 | 0 | 0 | 500 | no |
| 22 | 99bb733a | 2 | paths | A | 173 | 1000 | no | ✓ | 14 | 935 | 0 | 0 | **436** | no |
| 23 | 99bb733a | 3 | fimbulwinter | A | 173 | 406 | no | ✓ | 16 | 230 | 0 | 0 | 500 | no |
| 24 | 99bb733a | 4 | auroraveil | A | 173 | 183 | no | ✓ | 15 | 65 | 0 | 0 | 500 | no |
| 25 | 99bb733a | 5 | icefloe | A | 173 | 299 | no | ✓ | 31 | 101 | 0 | 0 | 500 | no |

*(Two map signatures collide on dims + core anchors — `holmgang`/`inv_small12`
and `midgard`/`ragnarok` — and are printed with both names rather than picked.
Names come from matching the replay's dims and both core anchors against
`maps/*.map26`; 37 signatures indexed from 44 files.)*

---

## 3. Totals

**ARRIVALS FIRST, per the prereg's own ordering:**

```
ARRIVING GAMES              25 / 25   (100%)
CONVERTING GAMES             0 / 25   (>=1 event of metric type 3)
NON-CONVERTING ARRIVING     25 / 25
```

**DECOMPOSITION of the 25 non-converting arriving games** (§HP-GATE's mandatory
split):

```
"NEVER IN FINISHING RANGE"  25 / 25    core HP never <=120 while our body was adjacent
"IN RANGE AND DID NOT FIRE"  0 / 25
```

**And the margin on that split is not narrow.** The minimum enemy-core HP ever
observed while one of our builders stood orthogonally adjacent, over all 25
games, is **340** — against a finishing gate of **≤120**. Distribution of
`adjmin` across the 25 arriving games:

| adjmin | games |
|---|---|
| **500** (untouched) | **19** |
| 472 / 464 / 440 / 436 | 1 each |
| **340** (the minimum) | 1 |

**Supporting counts:**

```
metric (2) PECK EVENTS, pooled          0     (our builder attacks total: 1,969)
metric (3) 2-HP core decrements, pooled 0     (hp2_any also 0 — no disagreement)
oppver alarms                           0 / 25
our game wins                           1 / 25   (game 4: 6db3add5 g4, valkyrie)
games reaching r1000                    2 / 25   (6db3add5 g2, 99bb733a g2)
```

**One observation flagged, not explained away:** in `6db3add5` g4 — the single
game we won — the enemy core finished at **0 HP** while `adjmin` reads **340**.
The core therefore crossed from 340 to 0 in rounds when none of our builders was
orthogonally adjacent to it, i.e. the kill was delivered off the collar. This is
a description of one game, not a mechanism claim.

**Files:** `scratchpad/s53_kladdedose/peckdecode.py` (decoder, `--selftest`
drives both verdicts), `leg25.tsv` (all 25 rows, all columns),
`leg20.tsv` (the pre-archive 20-game cut), `attack_classes.txt` (the
false-zero guard), `mapnames.json`.
