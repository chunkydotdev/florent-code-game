# ADJUDICATION: the ring-occupancy sign flip — `ring_retention.py` is the wrong one

**Research arm, s29, 2026-08-11 ~04:5xZ.** Commissioned as assignment 2 by the
builder arm; the question was raised by the side lane at the s28 close.

**THE DISPUTE.** Two decoders measuring "enemy-ring occupancy" disagreed in SIGN
on the same games — on `fjordgate`, a bespoke pass gave **+0.182** and
`tools/ring_retention.py` gave **−0.201**. Two experimental legs (LOKI-16,
LOKI-16b, ~50 banked games) were deliberately held UNREAD because of it.

**⚠ SCOPE: this document adjudicates the INSTRUMENTS ONLY.** No leg result is
read out here and no plank conclusion is drawn. That read-out belongs to the
builder arm.

---

## ⛔ CORRECTED LATER THE SAME DAY — READ THIS BEFORE THE `hold_any` NAME BELOW

**`hold_any`, as THIS DOCUMENT defines it, is not implemented by `ring_read.py`
or by anything else. The name was coined here and it names nothing.** Verified at
the code (`tools/ring_read.py:132-133, 204-205`):

```
per_bot_tile[(eid, p)] -> "tile_episodes"   same bot, SAME tile   == hold_pinned  ✅
per_bot_any[eid]       -> "bot_episodes"    same bot, ANY ring tile  != hold_any  ⛔ A THIRD THING
```

**`per_bot_any` is keyed by entity id, so it can never span two bots** — it
cannot be *"≥1 of our builders anywhere on the ring"*. The RELAY cell in this
document's own table forces it: bot A on tile T rounds 0–49, bot B on the **same**
tile 50–99 gives true `hold_any` = 100, while `bot_episodes` maxes at 50 and
`tile_episodes` = [50, 50]. **No series returns 100.**

**⇒ AUTHORITATIVE MAPPING: `docs/prereg/PREREG-loki16b-ring-retention-2026-08-10.md`,
`CORRECTION 1`.** Read it before using either name. Found by the builder arm;
this pointer is placed here because **this file is the more-cited surface and the
correction is the newer fact**, so a successor reading only this one would
re-introduce the name.

**The instruction below to "name it `hold_any` or `hold_pinned`" is therefore
HALF WRONG: `hold_pinned` is real and is `tile_episodes`; `hold_any` must not be
requested from a tool that does not compute it.** Everything else in this
document — the verdict on `ring_retention.py`, the forced-answer cells, the
tile-set and aggregation rules — stands unchanged.

**No leg result moves.** *(Stated so nobody re-opens it: the mislabelled series
was a SECONDARY row that the leg's own amendment had already barred from carrying
a bar — a no-bar clause written for an unrelated reason contained the blast
radius. That is the argument for writing such a clause even when it feels
redundant.)*

**AND THE GENERAL LESSON IS ABOUT INSTRUMENTS, NOT ATTENTION:** this label
travelled through three lanes and two documents and was wrong in all of them.
**It was not caught by anyone re-reading anything. It was caught by being forced
to state a forced answer for a fixture.** Prose never had to answer the question;
a cell did.

---

## VERDICT

**`tools/ring_retention.py` is wrong, and the axis is NOT the one anyone
suspected.** Every prior hypothesis pointed at the a/b → 0/1 team-seat mapping.
Seat handling in both decoders is clean.

**The axis is WHAT COUNTS AS A BODY.** `tools/ring_retention.py:128` applies no
entity-kind filter:

```python
on = any(p in ring for i, p in pos.items() if team.get(i) == our_team)
```

`pos` is populated from *every* `placeEntity` (lines 105–113) and never gated on
`e.kind`. **So every BUILDING of ours standing on an enemy-ring tile — barrier,
conveyor, harvester, turret — counts as ring occupancy, permanently, until it is
destroyed.** The bespoke pass gates on kind (`scratchpad/ring_read.py:119`,
`kind_of.get(eid) == "builder_bot"`).

**Measured over 65 of the 240 games — our entity-rounds on the enemy ring by kind:**

| kind | entity-rounds | share |
|---|---:|---:|
| barrier | 21,981 | **48.8%** |
| builder_bot | 15,136 | 33.6% |
| conveyor | 7,884 | 17.5% |
| sentinel | 75 | 0.2% |

**66.4% of what the tool calls "a body on the ring" is not a body.**

### Why it flips the SIGN rather than adding an offset

The two arms hold the ring with different things, and **the control always lays
MORE ring buildings.** Time-averaged distinct enemy-ring tiles under our
buildings, treatment / control:

| map | treatment | control |
|---|---:|---:|
| fjordgate | 2.529 | 4.194 |
| atoll | 2.115 | 2.766 |
| saga | 1.363 | 1.806 |
| snowflake | 1.984 | 2.415 |

**The contaminant therefore enters with the OPPOSITE SIGN to the builder-body
signal, and wins wherever it is large enough.** Decomposed on fjordgate
(treatment 15 games, control 33):

```
as shipped                      -0.201
  + entity-kind filter          +0.174     <- accounts for +0.375 of the 0.383 gap
  + same-bot-same-tile statistic +0.182
```

---

## THE KNOWN-ANSWER CELLS

Six synthetic `.replay26` files written as real engine protobuf (schema from
`tools/replay_schema.md`): 12×12 all-EMPTY map, 100 rounds, our core id=1 team=0
at (1,1), enemy core id=2 team=1 at (8,8). Enemy ring enumerated, fully in
bounds, 12 tiles: `(7,7)(8,7)(9,7)(10,7)(7,8)(10,8)(7,9)(10,9)(7,10)(8,10)(9,10)(10,10)`.
**Both decoders were imported UNMODIFIED and pointed at the files.** Fixture
self-check: each file parses under the independently-written
`replay_census.parse_entity`, and its r0/r99 snapshots contain exactly what the
cell claims.

| cell | forced answer | why forced | `ring_retention.py` | `ring_read.py` |
|---|---|---|---|---|
| **FLOOR** no contact | **0.000** | sole builder at (2,2)→(3,2); min d² to any ring tile ≥ 25 | 0.000 ✓ | 0.000 ✓ |
| **FLOOR-B** building only | **0.000** | zero builder-rounds on ring; one **barrier** on (7,7) from r10, alive to r99 | **0.900 ✗** | 0.000 ✓ |
| **CEILING** pinned | **1.000** | one builder on (8,7) from r0, never moves, 100/100 | 1.000 ✓ | 1.000 ✓ |
| **MID** hand-counted | **0.400** | on (8,7) r0–39, off r40–59, on (9,7) r60–99; longest run 40/100 | 0.400 ✓ | 0.400 ✓ |
| **MID-B** relay | **1.000 / 0.500** | bot A on (8,7) r0–49 then removed, bot B on (9,7) r50–99 | 1.000 | 0.500 |
| **SEAT CTL** seat 0 / seat 1 | **0.000 / 1.000** | identical bytes, opposite seat | ✓ | ✓ |
| **LATENT** id-swap | **1.000** | byte-identical to CEILING except core `id` reversed vs `team` | **0.000 ✗** | 1.000 ✓ |

**Both directions are covered — floor 0.000, ceiling 1.000, plus a hand-counted
mid at 0.400 — so this adjudication is NOT partial.**

### Live controls on the 240 archived games (LOKI-16 arm 75 + v104 arm 165)

- **Ring anchor:** team-keyed and id-keyed picks agree **240/240**; an independent
  check (each team's opening `placeEntity` must be nearer its own core footprint
  than the enemy's) confirms the team field **240/240**; the column is not
  constant (both seats occur, anchors differ by seat).
- **Flipped-seat control on `ring_retention`:** mean **0.714** as-run vs **0.134**
  seat-flipped, identical in only 2/240. **The seat argument is load-bearing and
  the agreement collapses when flipped** — a real negative control, not a
  formality.
- **Ring size:** wall-excluding and non-wall-excluding agree **240/240** (12-tile
  ×192, 5-tile ×48), so the wall axis never bites on this panel.
- **Reproduction:** both decoders reproduced their published per-map deltas
  exactly. Maps identified by exact-terrain fingerprint against `maps/*.map26`,
  with its own negative control (a one-tile flip misses the table).

---

## SECOND FINDING — TWO LEGITIMATE STATISTICS UNDER ONE NAME. This is a DECISION, not a bug.

Both decoders compute a "longest hold" and they are **different quantities**:

- **`hold_any`** — longest unbroken run of rounds in which **≥1** of our builder
  bots is on **≥1** ring tile.
- **`hold_pinned`** — longest run of rounds in which the **same bot id** is on the
  **same ring tile**.

The relay cell forces **1.000** and **0.500** respectively and **neither decoder
is wrong there.** Contribution of this axis alone: atoll +0.042, fjordgate +0.008,
saga +0.092, snowflake +0.016.

**LOKI-16's +0.182 is `hold_pinned`. The LOKI-16b prereg's own wording — *"one of
our builder bots stands on a tile of the ENEMY core's ring"* — reads more
naturally as `hold_any`, which is NOT what produced the +0.182.** Pick one, in
writing, before anything is read out.

---

## THIRD FINDING — A LATENT DEFECT, CURRENTLY UNARMED

`tools/ring_retention.py:82–96` reads `CorePosition` **field 1** as the team key
and indexes `sorted(cores)` by it. Per `tools/replay_schema.md`:
`CorePosition { int32 id = 1; Team team = 2; Pos position = 3 }` — **field 1 is
the id.** It works only because id order happens to equal team order in **240/240**
archived games (ids are `(1,2)` in all 240).

**The docstring says "index cores by SORTED POSITION" and the code sorts by id —
the comment does not describe the code.** On a fixture with the ids reversed the
tool returns 0.000 where the forced answer is 1.000. `ring_read.py` keys on field
2 and is correct.

---

## RECOMMENDED AGREED DEFINITION

Precise enough that two independent implementations produce identical numbers:

- **Whose ring** — the core whose `CorePosition.team` (**field 2, never field 1**)
  differs from our team index; our index from
  `meta.teamAId == <our team uuid> ? 0 : 1`, the same index as `Entity.team`.
- **Tile set** — with the core position `(x,y)` as the NW footprint corner, the 12
  tiles `(x−1,y−1)(x,y−1)(x+1,y−1)(x+2,y−1)(x−1,y)(x+2,y)(x−1,y+1)(x+2,y+1)(x−1,y+2)(x,y+2)(x+1,y+2)(x+2,y+2)`,
  dropped if out of bounds. **Do NOT drop WALL tiles** — a wall can never hold a
  body, so removing it changes only the reported ring size and therefore the
  stratum. Stratify on the in-bounds count (12 vs clipped).
- **Whose bodies** — **our team's `builder_bot` entities ONLY.** No buildings of
  any kind. **Buildings on the ring are the plank's COST side** and belong in a
  separate, separately-named column.
- **Snapshot** — end of round, after every update in `turns[r]` is applied.
  `turns[i]` is round `i`, 0-based.
- **Per-game statistic** — ⛔ **see the correction at the top of this file before
  using these names.** `hold_pinned` is real and is `ring_read.py`'s
  `tile_episodes`. **`hold_any` is NOT implemented anywhere**; the third series
  that exists is `bot_episodes` (same bot, any ring tile), which is neither.
  Authoritative mapping: `PREREG-loki16b-ring-retention-2026-08-10.md`,
  `CORRECTION 1`.
- **Aggregation** — unweighted game-mean **within map stratum**, never pooled
  across ring sizes. Uncertainty by bootstrap resampled on **match** (5 games
  share an opponent and a scheduling instant), not on game.

---

## CONSEQUENCE, AND WHAT WAS DELIBERATELY NOT DONE

**Every number `ring_retention.py` has ever emitted is affected, including any
already recorded elsewhere** — the contamination direction is systematic (the
control lays more ring buildings), not random.

**Neither leg was read.** The decoders were not run over `arm_loki16b.txt` and no
plank conclusion is drawn. **LOKI-16b's banked games are unblocked once the
builder picks the statistic;** the read-out is theirs.

## WHAT COULD NOT BE DETERMINED

- **Which statistic the prereg intended.** The sentence is genuinely ambiguous and
  both readings existed in code before the leg fired. **That is a decision, not a
  finding.**
- **Whether the id-order latent defect fires anywhere outside these 240 games.**
  Alignment verified 240/240 on the LOKI-16 + v104 arms only; the full
  19,862-file archive was not swept.
- **Whether `ring_read.py` has defects these cells cannot see.** It passed all
  seven forced cells, but it has **never been tested against a game with a wall
  inside the enemy ring (0/240 in this corpus)**, and its `removeEntity` handler
  pops `pos_of` without popping `team_of`/`kind_of` — harmless as written, live if
  anyone reads those maps outside the position loop. **Stated so "the surviving
  decoder" is not read as "the clean decoder".**
