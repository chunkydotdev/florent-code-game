# Ouroboros v65-era re-verify — match 071cd20c (2026-08-07)

Read-only re-decode. No bots edited, no matches run, nothing downloaded —
match `071cd20c-4eb3-4233-ab7e-a91c7361d97b` was already archived
(`replay_archive/071cd20c-4eb3-4233-ab7e-a91c7361d97b_game_[1-5].replay26` +
`.meta.json`). This is the standing "one v65-era Ouroboros re-verify game"
instrument the denial-adjudication note called for
(`docs/research/denial-adjudication-2026-08-07.md`, closing paragraph) — 5
games, better than the planned single game.

## Correction to the task framing, first

**The brief's framing has the result backwards.** `.meta.json` records
`scoreA: 5, scoreB: 0`, `teamAName: "Ouroboros"`, `teamBName: "OpenSverige"`,
`winnerId` equal to Ouroboros's `teamAId`, `eloDeltaA: +14.06` /
`eloDeltaB: -14.06`. Independently confirmed by decoding all 5 games:
**Ouroboros (v8) won every game**, `winner == A` in all five, 4 by
`core_destroyed` and 1 (game 3) by the `titanium_collected` tiebreaker at
round 1000. **This was a 5-0 loss for us (v65), not a 5-0 win.** Flagging
this because it changes the read: this wasn't a confirmatory "we handily
beat old Ouroboros" game, it was every game going the other way, including 4
core kills. It does not overturn the geometric findings below (Ouroboros
never used a core-threatening gunner in 4 of 5 games — see per-game tables),
so the losses were not caused by the specific denial gap this file gates,
but it belongs on the record.

## Verdict

**Maps played: lighthouse, meander, archipelago, atoll, fjordgate — eider
did not appear in this 5-game sample.** Of the book's two constant-bearing
maps (eider, meander), only **meander** (game 2) was testable.

**Meander: SHIFTED.** The book's v64-era row does not reproduce under v65,
on both the round tolerance (±3) and the exact-tile test:

| | round | tile | facing | fp_dsq | gunner_threat (core-threatening) |
|---|---|---|---|---|---|
| book (v64, corrected per adjudication) — literal 1st ("home picket") | r4 | (13,6) | S | 17 | **False** |
| **observed (v65, game 2)** — literal 1st | **r8** | **(8,6)** | S | 25 | False |
| book's tile, as observed in v65 | r40 (2nd build, not 1st) | (13,6) | SW | 17 | False |
| book (v64, corrected) — core-threat creep | r46 | (13,8) | — | 5 | True |
| **observed (v65, game 2)** — 1st core-threat build | **r489** | **(8,10)** | E | 9 | **True** |

Both rows miss: the literal-first tile is different (not just late — a
different tile entirely, `(13,6)` doesn't show up until Ouroboros's
**second** gunner, 32 rounds after their first), and the core-threat creep
that the book clocked at r46 doesn't happen until **r489** in this game — a
443-round shift, landing on a different tile than predicted. In absolute
terms this makes meander *more* deniable in practice (margin only grows),
but a hardcoded `(round, tile)` constant is not safe to ship: neither
coordinate reproduces within tolerance. **Do not hardcode meander's exact
round/tile into Loki. The DENIABLE conclusion likely still holds (margin
only grew), but as a policy ("plant near the harvester belt, ~turn-dependent
window"), not a fixed station.**

**Mechanism note, important correction to the adjudication doc's working
theory.** The adjudication doc's standing explanation was "the queue is
perturbed by when our builders die." In game 2, Ouroboros's own build queue
already diverges from the book's transcript by **round 3** — their 3rd
builder spawns at `(10,5)` here vs. `(13,5)` in the book's `bab61537`
transcript — while our first builder death doesn't happen until **round
19**, 16 rounds later. Builder-death timing cannot be the mechanism for
*this* divergence; it predates it. Something else about opponent context
(possibly vision-triggered branching, possibly round-resolution-order
jitter between simultaneous units) perturbs the queue before any combat
happens. This doesn't overturn the "perturbable, not fixed" conclusion —
it strengthens it — but the specific causal story ("keyed to our builder
deaths") is not what's driving this instance and should not be repeated as
settled going forward without more evidence.

**Eider: NOT TESTABLE.** No eider game in this 5-game sample. The eider GO
constant (`r50@(16,10)`, dsq9, margin 48) is neither confirmed nor refuted
here.

**Net GO/NO-GO recommendation:** given meander's constant did not survive a
single version step (v64→v65) on either axis, and eider is untested,
**do not hand-code either book row as a fixed `(round, tile)` station for
Loki.** The large margins (45, 48 in the book) make the *practical*
denial-viability conclusion (both maps are comfortably deniable) probably
still true — this v65 game's numbers are even later/looser, not tighter —
but that is a policy-level claim ("deny the harvester-belt cluster, wide
window"), not a coordinate to hardcode. This should gate the hardcode
exactly as the adjudication doc anticipated: **RETIRE the fixed-tile
plan, keep the policy-level DENIABLE verdict.**

**Version-drift caveat (per the task brief):** our live version is now v69,
four ships past the v65 sampled here. A v64→v65 shift being this large is
evidence the mechanism is *not* robust to our own version even one step
out — it is not a blank check that v69's queue-perturbation profile matches
either v64's or v65's. Any future hardcode attempt should re-verify against
current-version replays, not this file's v65 numbers, by the same logic
that retired the original v53-59 sample in the adjudication doc.

---

## Per-game data

All 5 games passed every `replay_lib.check_all()` self-check (delivery×10
== titaniumCollected, ammo conservation, no unknown schema fields, no
entity-id reuse, HP within bounds, winner-vs-dead-core consistency) — see
Method notes.

Map identification used the denial-book's own method (§0.2): exact
`(width, height, walls, ore, core-position-per-team)` match against every
`maps/*.map26`, zero ambiguous results, zero `fcode` calls.

### Game 1 — lighthouse (16×16, walls=64, ore=12)

377 rounds. **Ouroboros won, core_destroyed r376.** *Lighthouse was
previously unobserved for Ouroboros* (denial-book §6 lists it as a coverage
gap) — this fills it.

Ouroboros gunner/sentinel builds, deduped by entity id, r≤120:

| round | kind | tile | facing | fp_dsq | gunner_threat | sent_threat |
|---|---|---|---|---|---|---|
| 11 | gunner | (6,6) | SE | 50 | False | False |
| 13 | gunner | (8,5) | S | 45 | False | False |
| 29 | gunner | (5,5) | NE | 72 | False | False |
| 32 | gunner | (6,2) | SE | 106 | False | False |
| 37 | gunner | (6,2) | SE | 106 | False | False |
| 50 | gunner | (8,5) | S | 45 | False | False |
| 52 | gunner | (7,7) | SE | 32 | False | True |
| 80 | gunner | (9,10) | E | 5 | **True** | True |
| 82 | gunner | (10,4) | NW | 50 | False | False |
| 85 | gunner | (10,11) | NE | 1 | **True** | True |
| 97 | gunner | (5,8) | SW | 45 | False | False |

Our builder-bot deaths before r60: r24 @(7,6), r37 @(7,3), r56 @(6,7) —
3 deaths, i.e. a busier early trade than meander's game.

First core-threatening gunner: **r80 @(9,10)**.

### Game 2 — meander (25×15, walls=8, ore=24)

817 rounds. **Ouroboros won, core_destroyed r816.** This is the sole
constant-bearing map tested — see Verdict above for the book comparison.

Full build list, threat classification, and mechanism note are in the
Verdict section. Our builder-bot deaths before r60: r19 @(10,8), r36 @(8,7),
r47 @(14,5).

### Game 3 — archipelago (26×26, walls=208, ore=38)

1000 rounds. **Ouroboros won on the round-1000 `titanium_collected`
tiebreaker** — our core survived the full game. Not a constant-bearing map
for the GO gate, but notable: **the literal-first-gunner row is an exact
match to the book**, both round and tile:

| | round | tile | facing |
|---|---|---|---|
| book (`22f55a05` g2 vs SmartFridge, v53-59 era per denial-book §1) | r28 | (7,7) | — |
| **observed (v65, game 3)** | **r28** | **(7,7)** | SE |

Ouroboros built 27 turrets total across the full game and **never reached a
`gunner_threat=True` tile** (checked over all 1000 rounds, not just the
first 120) — consistent with the book's own r739 core-threat prediction
being very late and the game ending on tiebreaker with our core untouched.
This is useful corroboration that Ouroboros's queue *can* reproduce exactly
across versions on some maps — which makes meander's large shift a real
finding, not just general noise.

Our builder-bot deaths before r60: **none.**

### Game 4 — atoll (18×18, walls=18, ore=8)

371 rounds. **Ouroboros won, core_destroyed r370.** Atoll is in the book's
table (2-observation row: literal 1st `r21@(4,9)` or `r27@(3,12)`, "aim
policy not fixed coordinate" per its own determinism note).

| round | kind | tile | facing | fp_dsq | gunner_threat |
|---|---|---|---|---|---|
| 31 | gunner | (3,12) | N | 202 | False |
| 33 | gunner | (3,11) | N | 185 | False |
| 40 | gunner | (4,10) | NW | 149 | False |
| 59 | gunner | (13,11) | N | 65 | False |
| 64 | gunner | (13,7) | NE | 17 | False |
| 74 | gunner | (16,6) | W | 10 | False |
| 76 | gunner | (13,7) | NE | 17 | False |
| 99 | gunner | (6,15) | N | 208 | False |
| 101 | gunner | (6,14) | SW | 185 | False |
| 113 | gunner | (13,7) | SW | 17 | False |
| 115 | gunner | (12,5) | N | 8 | **True** |

Literal-first tile `(3,12)` matches one of the book's two observed tiles
exactly; the other early tiles (`(3,11)`, `(4,10)`) are in the same small
cluster the book described. Round is later than the book's r21/r27 (r31 —
about 10 rounds out), consistent with the book's own "plant near the
cluster, round drifts" framing rather than an exact-station claim (atoll was
never called GO in the book, so this isn't a gate failure, just supporting
data for the "policy not station" reading).

Our builder-bot deaths before r60: r47 @(4,9).

### Game 5 — fjordgate (10×10, walls=10, ore=6)

151 rounds. **Ouroboros won, core_destroyed r150.** *Fjordgate was also
previously unobserved for Ouroboros* (denial-book §6 coverage gap) — this
fills it too. Being a small 10×10 map, Ouroboros's literal first gunner is
**already core-threatening from round 2** — a different profile than the
"creeping picket, non-threatening at first" pattern seen everywhere else in
this file:

| round | kind | tile | facing | fp_dsq | gunner_threat |
|---|---|---|---|---|---|
| 2 | gunner | (4,6) | E | 4 | **True** |
| 3 | gunner | (5,5) | SE | 2 | **True** |
| 4 | gunner | (5,4) | SE | 5 | **True** |
| 63 | gunner | (6,4) | SE | 4 | **True** |
| 112 | gunner | (2,6) | SE | 16 | False |

Our builder-bot deaths before r60: r13 @(6,5), r22 @(5,7), r29 @(5,7),
r57 @(6,4) — 4 deaths, the busiest early trade of the five games, on the
smallest/fastest map.

---

## Method notes

**Parser.** Used the existing, already-validated toolkit at
`docs/research/2026-08-07-fanout/toolkit/replay_lib.py` +
`siege_geometry.py` (stdlib-only protobuf decoder; README claims 325/325
self-checks across 35 previously-cached files, cross-validated against
`tools/replay_census.py`). No new decoder was written — a thin orchestration
script was added at
`/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/0a67ca71-984b-4cfe-8807-172307619ab7/scratchpad/decode_071cd20c.py`
(scratch only, not committed) that: loads all 5 games, runs `check_all()`,
identifies each map by exact terrain match against `maps/*.map26` (same
method as denial-book §0.2, zero `fcode` calls), lists Ouroboros
gunner/sentinel builds deduped by entity id up to r120, lists our
builder-bot deaths before r60, and cross-references tile threat
classification via `siege_geometry.SeatAnalysis` built against the correct
defending seat for each map (confirmed "direct" `GameMap`↔`Replay` core-team
correspondence for all 5 maps, i.e. replay team 0 == catalog team 0 in every
case — no seat-swap needed).

**Dedupe confirmed.** Per `docs/tooling.md`'s replay-decode gotcha, a gunner
`rotate()` re-emits `placeEntity` with the same entity id. `replay_lib.py`
already routes same-id re-emissions to `.entity_updates` rather than
`.builds` at the source (see its `_replay()` method, `old = live.get(ent.id)`
branch) — this library was written specifically to fix that bug (its own
README cites catching "6 vs 2 gunners" before the fix). The orchestration
script additionally asserted no entity id repeats across the `.builds`
stream for gunner/sentinel per game (0 assertion failures, all 5 games) as
an independent confirmation, and separately reports rotation counts
(24/11/1/15/8 across games 1-5) so rotation activity is visible without
being miscounted as new builds.

**Self-checks.** All 5 games: `check_all()` all-green (delivery×10 ==
titaniumCollected, ammo converted-spent == final engine ammo, no unknown
top/turn/update/entity-kind fields, no id reuse, HP within bounds, winner
consistent with dead cores).

**What was not computed.** Full BFS deniability margins (à la
`siege_geometry.SeatAnalysis.mincut`/`spawn_ring` walk-distance) were not
re-run for the observed tiles — this file only checked round/tile/threat-
classification congruence against the book's constants, per the task's
stated verdict question. `gunner_threat`/`sentinel_threat` set membership
(the book's own core-threat test, `r²≤13` aligned-and-unblocked for gunner)
was used directly from `siege_geometry.py`, unchanged from the book's own
tool.

**Numbers.** All figures above are parsed directly from the 5 archived
`.replay26` files; nothing is carried over from the book or adjudication doc
except for direct quotation (marked "book" in tables). No UNCERTAIN markers
were needed — every self-check passed and the dedupe assertion held on all
5 games.
