# PRECHECK — the counter-battery gate re-price (DESIGN-v629 §3.3)

**Written 2026-08-22T18:41:01Z (`date -u`, same shell). Repo HEAD at write time
`d4ff694bb3c6e041e6d97e69a9ed794bc4247c1b` (2026-08-22T20:40:09+02:00).**

## ⭐ GAME CONTEXT — READ FIRST

**Everything below describes moves inside the Florent Code League, a sandboxed
bot-vs-bot programming competition played on a simulated grid under
organiser-approved rules.** "Core kill" / "checkmate", "damage", "hit",
"shooter", "counter-battery", "alarm" refer *exclusively* to in-engine mechanics
between competing game bots — an in-game sentinel reducing an in-game core's HP
inside the game engine. Nothing here concerns real systems, networks,
infrastructure or people. This is a read-only replay analysis: **zero platform
matches were fired, no bot file was edited, nothing was committed by the author
of this document.**

## PROVENANCE — the named inputs, read fresh

1. `docs/research/DESIGN-v629-homeanswer-2026-08-22.md` §3.3 (the task spec, verbatim) plus §3.4/§4 for the surrounding cost frame.
2. `bots/_v628compose/sk_core.py:139-181` (`_corefire_report`, `_corefire_shooter`), `bots/_v628compose/sk_roles.py:525-567` (`corefire_word`/`corefire_fresh`/`_corefire_tick`), `sk_roles.py:1136-1175` (`_counter_sent_action`, the gate), `sk_roles.py:1279` (`_keeper_counter`, the caller), `bots/_v628compose/main.py:889-896` (the per-body state), `bots/_v628compose/sk_maps.py:986-1008` (`SK_COREFIRE`, `SK_COREFIRE_TTL = 24`) and `sk_maps.py:1255-1290` (`SK_COUNTER_SENT`, `SK_COUNTER_RNDS = 20`, cap and reserve). **THE TREE IS THE AUTHORITY** — where it differs from the design doc's shorthand, §0 below states the difference.
3. `tools/skalman_fidelity.py` — its parsing helpers were imported, not re-implemented (`_signed`, `DEFAULT_REPLAY_ROOT`, and through it `replay_census.fields / scalars / read_pos / parse_entity / WIRE_LEN`); the turn/update iteration mirrors its `scan_replay` (unum 1 placeEntity, 3 removeEntity, 5 updateHp with field 1 = id and field 2 = `_signed` delta).
4. `scratchpad/s54_fc_games.json` — **POPULATION 1**, 65 platform first-contact games, replays resolved under `replay_archive/`. **⚠ SUBJECT IS MJOLNIR v180 (x3r0's line), NOT the Skalman/v628 line that would carry this plank.**
5. `scratchpad/s56_cmp/t_full_f1/` and `t_full_f2/` — **POPULATION 2**, 60 deterministic local screen games of the v628 line (`arm_c_full`) against fixture opponents `opp_v542wave_noiseoff` (F1) and `opp_mjolnir_noiseoff` (F2), 15 maps x 2 seats per fixture.

Analysis script (not committed, left for review):
`<session-scratchpad>/precheck_counterbattery.py`.

---

## 0. THE GATE'S ACTUAL SEMANTICS, AND WHERE THEY DIFFER FROM THE DESIGN DOC

The design doc's shorthand is *"reconstruct `corefire_streak` from per-round
negative `UpdateHp` deltas on our own core + `SK_COREFIRE_TTL = 24`."* The tree
does four things that shorthand does not say, and **two of them change the
answer**:

| # | the tree's actual code | consequence |
|---|---|---|
| 1 | `sk_core.py:163-164` — `if hp < prev: self.corefire_last = rnd`. **`corefire_last` is a LATCH that only moves forward**; nothing ever clears it. | — |
| 2 | `sk_roles.py:533-539` — `fresh(r) := 0 <= r - corefire_last <= 24`. | ⭐ **ONE core hit makes the alarm fresh for 25 consecutive rounds (r .. r+24).** "20 rounds of UNBROKEN alarm" therefore needs **one** hit and 20 further rounds of play — *not* 20 rounds of sustained fire. **`SK_COUNTER_RNDS = 20` < `SK_COREFIRE_TTL = 24` makes the N dial nearly inert.** |
| 3 | `main.py:892-896` + `sk_roles.py:557-567` — `corefire_streak` is **per BODY**, incremented once per round the body's `_role_turn` runs, reset to 0 otherwise; a body spawned after the alarm armed starts at 0. | reconstruction must be per body, not global (both are computed below; **they came out identical**, see V3b) |
| 4 | comms-store writes are buffered (CLAUDE.md), so a builder reads the core's word **one round late**; a hit landing after the core's own turn is seen by the core one round late too. | open-rounds are quoted at **lag = 1** (primary); the lag 0..2 band is V3 and moves every open-round by at most ±1 |

Two further conjuncts of the shipped gate are **NOT reconstructable from a
replay and are NOT modelled here** — `_counter_sent_action` also requires an
identified shooter tile (`corefire_shooter`, which is a best-effort read the
core itself calls "a best effort extra", `sk_core.py:142-148`) and a bank of
`sentinel_cost + SK_COUNTER_SENT_RESERVE(20)`. **Everything below is therefore
an UPPER BOUND on how often the plank would actually fire, and a correspondingly
CONSERVATIVE (i.e. maximal) estimate of its r300 exposure.** That is the right
direction for a precheck whose question is "can this plank touch the by-r300
population".

---


---

## ⭐ THE SURPRISE, STATED BEFORE THE EXPLANATION

**`SK_COUNTER_RNDS = 20` is very nearly not a gate at all, and the flag comment
that attributes PLANK 3's null to it is describing a constraint the code does
not impose.**

`SK_COREFIRE_TTL = 24` exceeds `SK_COUNTER_RNDS = 20`, and `corefire_last` is a
forward-only latch. **One negative `updateHp` on our core therefore buys 25
consecutive fresh rounds — more than the 20 the gate asks for — with no second
hit required.** "20 rounds of UNBROKEN alarm" is satisfied by *one shot and 20
rounds of the game continuing*.

The tables make this visible as a **flat N ladder**: moving N from 6 to 20
changes the share of games in which the gate opens by **0 games in P1 (63/65 at
both ends)** and **1 game in P2 (44/60 -> 43/60)**, and moves the median opening
round by **exactly N-6 rounds** (P1 ALL: r79 -> r93; P2 ALL: r71 -> r85) — the
signature of a single latched hit, not of an accumulating condition. **The gate
is, to within one game out of 125, a test of "has our core been hit at all, with
N rounds of play left".** In P2 the gate is shut in **16/60** games at
N ≤ 12, and **those 16 are exactly the 16 games in which our core took zero hits
all game** (at N = 20 a 17th joins them: one game whose only core hits landed
within 20 rounds of the end); in P1 it is shut in **2/65** at every N, and both
of those took zero core hits.

⇒ **The flag comment's diagnosis — *"THE GATE IS ALMOST NEVER OPEN IN TIME … it
needs SK_COUNTER_RNDS = 20 rounds of UNBROKEN alarm"* (`sk_maps.py:1261-1266`) —
is not what the reconstruction shows.** The alarm-streak conjunct is open in
**72% of the v628 tape's games** and **97% of the platform first-contact games**,
typically by **r85** (P2 median) / **r93** (P1 median). If PLANK 3 was an exact
null, the binding conjunct is one of the three this precheck does *not* model:
the identified-shooter requirement, the bank requirement, or the keeper body
being the one that has to hold the count. **That relocates the whole diagnosis,
and it means "loosen SK_COUNTER_RNDS" is a re-price of a constraint that was
already loose.**

Second, smaller surprise: **the per-body reconstruction and the global "oracle"
reconstruction are IDENTICAL on both populations** (share opening N=20 and median
max-streak agree exactly, V3b). Our builder bodies are long-lived enough that the
"a replacement restarts the count" cost that `main.py:894-896` prices as
acceptable is, on these tapes, **not paid at all when measured over all bodies**
— which is also why the keeper-specific narrowing in LIMITS #5 matters.

---
## VALIDATION

**V0 core identification (P1, n=65).** Our parser's `removeEntity` round for the core it identified as OURS vs `s54_fc_games.json:our_core_death`: **63 exact match, 0 mismatch, 2 both-null (core survived)**.

**V0b first-core-hit ordering (P1).** `their_first_dmg_on_us` (JSON: first damage on ANY of our entities) vs our first negative `updateHp` on our CORE: our core hit is at or after it in **63/63** games (violations would falsify the id); median offset **0** rounds.

**V1 positive control (P1 — largest `their_dmg_on_us` with a known `our_core_death`).**

| game | cell | JSON their_dmg_on_us | JSON our_core_death | parsed core dmg | parsed core death | core-hit rounds (first..last, n) | max streak (TTL=24) |
|---|---|---|---|---|---|---|---|
| 0e5b63ea_g5 | MIRROR | 998 | 139 | 998 | 139 | 11..139, n=57 | 71 |
| 5ee3afec_g1 | MIRROR | 846 | 118 | 846 | 118 | 26..118, n=47 | 92 |
| b6ec7f91_g1 | KLADDE | 828 | 119 | 828 | 119 | 38..119, n=44 | 81 |

**V2 mutation control (TTL 24 -> 1).** Streak lengths must strictly shrink or stay equal, and shrink materially in aggregate.

| population | n games | median max-streak TTL=24 | median max-streak TTL=1 | any game where TTL=1 > TTL=24 | mean max-streak 24 -> 1 |
|---|---|---|---|---|---|
| P1 platform first-contact | 65 | 54 | 31 | **0** | 54.5 -> 34.1 |
| P2 v628 local screen | 60 | 54 | 24 | **0** | 41.5 -> 24.8 |

| population | share opening N=20, TTL=24 | share opening N=20, TTL=1 |
|---|---|---|
| P1 | 63/65 (96.9%) | 57/65 (87.7%) |
| P2 | 43/60 (71.7%) | 38/60 (63.3%) |

**V3 store-lag sensitivity.** The comms store is buffered, so a builder reads the core's word one round late; the core itself may see a late-in-round hit only on the next round. Primary = lag 1; the band is lag 0..2.

| population | lag | share opening N=20 | median open-round N=20 (openers only) |
|---|---|---|---|
| P1 | 0 | 63/65 | 92 |
| P1 | 1 | 63/65 | 93 |
| P1 | 2 | 63/65 | 94 |
| P2 | 0 | 43/60 | 84 |
| P2 | 1 | 43/60 | 85 |
| P2 | 2 | 43/60 | 86 |

**V3b ORACLE vs PER-BODY.** The tree counts `corefire_streak` per BODY (main.py:892-896: *"counted per body rather than published"*), so a builder spawned after the alarm armed starts at 0. The ORACLE reconstruction (a hypothetical observer alive all game) is the upper bound; PER-BODY (max over OUR builder bodies) is the shipped semantics and is what the (a)/(b)/(c) tables below use.

| population | share opening N=20, ORACLE | share opening N=20, PER-BODY | median max-streak ORACLE | median max-streak PER-BODY |
|---|---|---|---|---|
| P1 platform first-contact | 63/65 (96.9%) | 63/65 (96.9%) | 54 | 54 |
| P2 v628 local screen | 43/60 (71.7%) | 43/60 (71.7%) | 54 | 54 |

**V4 P2 seat convention.** Each `.log` names the match as `<teamA> vs <teamB>`: `arm_c_full` is listed FIRST in **30/30** seatA games and SECOND in **30/30** seatB games ⇒ seatA = our side 0/A, seatB = our side 1/B. Independently, the replay's own winner field equals our side index exactly when the log names `arm_c_full` the winner in **60/60** games — so `winner_raw == side` is the engine-side our-win flag and the seat map is confirmed from the wire, not only from the log text.

**V5 P1 outcome cross-check.** The replay's winner field equals our side index exactly when `s54_fc_games.json:won == 1` in **65/65** games.

---

## POPULATION 1 — 65 platform first-contact games (subject: Mjolnir v180)

### (a) Does the streak reach N rounds of unbroken freshness? — P1 platform first-contact

| cell | n games | N=6 | N=8 | N=10 | N=12 | **N=20 (shipped gate)** | median max-streak |
|---|---|---|---|---|---|---|---|
| ALL | 65 | 63/65 (97%) | 63/65 (97%) | 63/65 (97%) | 63/65 (97%) | 63/65 (97%) | 54 |
| MIRROR | 20 | 19/20 (95%) | 19/20 (95%) | 19/20 (95%) | 19/20 (95%) | 19/20 (95%) | 47 |
| PIVOT | 20 | 20/20 (100%) | 20/20 (100%) | 20/20 (100%) | 20/20 (100%) | 20/20 (100%) | 63 |
| KLADDE | 25 | 24/25 (96%) | 24/25 (96%) | 24/25 (96%) | 24/25 (96%) | 24/25 (96%) | 53 |

### (b) At what round does the gate first open? — P1 platform first-contact

(median [min..max] of the first round whose trailing unbroken-fresh streak >= N, over the games in that cell where it opens at all; games where it never opens contribute nothing)

| cell | N=6 | N=8 | N=10 | N=12 | **N=20** | median game length (rounds) |
|---|---|---|---|---|---|---|
| ALL | 79 [17..455] n=63 | 81 [19..457] n=63 | 83 [21..459] n=63 | 85 [23..461] n=63 | 93 [31..469] n=63 | 140 |
| MIRROR | 42 [17..111] n=19 | 44 [19..113] n=19 | 46 [21..115] n=19 | 48 [23..117] n=19 | 56 [31..125] n=19 | 122 |
| PIVOT | 94 [36..177] n=20 | 96 [38..179] n=20 | 98 [40..181] n=20 | 100 [42..183] n=20 | 108 [50..191] n=20 | 160 |
| KLADDE | 89 [44..455] n=24 | 91 [46..457] n=24 | 93 [48..459] n=24 | 95 [50..461] n=24 | 103 [58..469] n=24 | 120 |

### (c) THE DECISION CELL — by-r300 core-kill win share, gate-open vs gate-shut — P1 platform first-contact

Population by-r300 core-kill wins for our side: **1/65 (1.5%)**.

| cell | N | gate OPENS: by-r300 kill-wins / games | gate SHUT: by-r300 kill-wins / games | by-r300 wins in which the gate ALSO opens |
|---|---|---|---|---|
| ALL | 6 | 0/63 (0.0%) | 1/2 (50.0%) | **0/1** |
| ALL | 8 | 0/63 (0.0%) | 1/2 (50.0%) | **0/1** |
| ALL | 10 | 0/63 (0.0%) | 1/2 (50.0%) | **0/1** |
| ALL | 12 | 0/63 (0.0%) | 1/2 (50.0%) | **0/1** |
| ALL | 20 | 0/63 (0.0%) | 1/2 (50.0%) | **0/1** |
| MIRROR | 6 | 0/19 (0.0%) | 1/1 (100.0%) | **0/1** |
| MIRROR | 8 | 0/19 (0.0%) | 1/1 (100.0%) | **0/1** |
| MIRROR | 10 | 0/19 (0.0%) | 1/1 (100.0%) | **0/1** |
| MIRROR | 12 | 0/19 (0.0%) | 1/1 (100.0%) | **0/1** |
| MIRROR | 20 | 0/19 (0.0%) | 1/1 (100.0%) | **0/1** |
| PIVOT | 6 | 0/20 (0.0%) | — (0 games) | **0/0** |
| PIVOT | 8 | 0/20 (0.0%) | — (0 games) | **0/0** |
| PIVOT | 10 | 0/20 (0.0%) | — (0 games) | **0/0** |
| PIVOT | 12 | 0/20 (0.0%) | — (0 games) | **0/0** |
| PIVOT | 20 | 0/20 (0.0%) | — (0 games) | **0/0** |
| KLADDE | 6 | 0/24 (0.0%) | 0/1 (0.0%) | **0/0** |
| KLADDE | 8 | 0/24 (0.0%) | 0/1 (0.0%) | **0/0** |
| KLADDE | 10 | 0/24 (0.0%) | 0/1 (0.0%) | **0/0** |
| KLADDE | 12 | 0/24 (0.0%) | 0/1 (0.0%) | **0/0** |
| KLADDE | 20 | 0/24 (0.0%) | 0/1 (0.0%) | **0/0** |

**Overlap detail (N=20, P1 platform first-contact): empty — no game is both a by-r300 core-kill win and a gate opener.**

At N=8 the overlap is **0** game(s) of the 1 by-r300 kill-wins.

---

## POPULATION 2 — 60 deterministic local screen games (subject: the v628 line)

### (a) Does the streak reach N rounds of unbroken freshness? — P2 v628 local screen

| cell | n games | N=6 | N=8 | N=10 | N=12 | **N=20 (shipped gate)** | median max-streak |
|---|---|---|---|---|---|---|---|
| ALL | 60 | 44/60 (73%) | 44/60 (73%) | 44/60 (73%) | 44/60 (73%) | 43/60 (72%) | 54 |
| t_full_f1 | 30 | 21/30 (70%) | 21/30 (70%) | 21/30 (70%) | 21/30 (70%) | 21/30 (70%) | 54 |
| t_full_f2 | 30 | 23/30 (77%) | 23/30 (77%) | 23/30 (77%) | 23/30 (77%) | 22/30 (73%) | 45 |

### (b) At what round does the gate first open? — P2 v628 local screen

(median [min..max] of the first round whose trailing unbroken-fresh streak >= N, over the games in that cell where it opens at all; games where it never opens contribute nothing)

| cell | N=6 | N=8 | N=10 | N=12 | **N=20** | median game length (rounds) |
|---|---|---|---|---|---|---|
| ALL | 71 [14..604] n=44 | 73 [16..606] n=44 | 75 [18..608] n=44 | 77 [20..610] n=44 | 85 [28..618] n=43 | 201 |
| t_full_f1 | 67 [44..339] n=21 | 69 [46..341] n=21 | 71 [48..343] n=21 | 73 [50..345] n=21 | 81 [58..353] n=21 | 191 |
| t_full_f2 | 101 [14..604] n=23 | 103 [16..606] n=23 | 105 [18..608] n=23 | 107 [20..610] n=23 | 115 [28..618] n=22 | 222 |

### (c) THE DECISION CELL — by-r300 core-kill win share, gate-open vs gate-shut — P2 v628 local screen

Population by-r300 core-kill wins for our side: **16/60 (26.7%)**.

| cell | N | gate OPENS: by-r300 kill-wins / games | gate SHUT: by-r300 kill-wins / games | by-r300 wins in which the gate ALSO opens |
|---|---|---|---|---|
| ALL | 6 | 6/44 (13.6%) | 10/16 (62.5%) | **6/16** |
| ALL | 8 | 6/44 (13.6%) | 10/16 (62.5%) | **6/16** |
| ALL | 10 | 6/44 (13.6%) | 10/16 (62.5%) | **6/16** |
| ALL | 12 | 6/44 (13.6%) | 10/16 (62.5%) | **6/16** |
| ALL | 20 | 5/43 (11.6%) | 11/17 (64.7%) | **5/16** |
| t_full_f1 | 6 | 4/21 (19.0%) | 8/9 (88.9%) | **4/12** |
| t_full_f1 | 8 | 4/21 (19.0%) | 8/9 (88.9%) | **4/12** |
| t_full_f1 | 10 | 4/21 (19.0%) | 8/9 (88.9%) | **4/12** |
| t_full_f1 | 12 | 4/21 (19.0%) | 8/9 (88.9%) | **4/12** |
| t_full_f1 | 20 | 4/21 (19.0%) | 8/9 (88.9%) | **4/12** |
| t_full_f2 | 6 | 2/23 (8.7%) | 2/7 (28.6%) | **2/4** |
| t_full_f2 | 8 | 2/23 (8.7%) | 2/7 (28.6%) | **2/4** |
| t_full_f2 | 10 | 2/23 (8.7%) | 2/7 (28.6%) | **2/4** |
| t_full_f2 | 12 | 2/23 (8.7%) | 2/7 (28.6%) | **2/4** |
| t_full_f2 | 20 | 1/22 (4.5%) | 3/8 (37.5%) | **1/4** |

**Overlap detail (N=20, P2 v628 local screen) — the games where the shipped gate opens AND we win by a core kill at or before r300:**

| game | cell | our core-kill round | gate opens (N=20) at round | opens BEFORE the kill? |
|---|---|---|---|---|
| f1:skald_seatA | t_full_f1 | 135 | 83 | YES |
| f2:valkyrie_seatB | t_full_f2 | 140 | 110 | YES |
| f1:jotunheim_seatA | t_full_f1 | 264 | 126 | YES |
| f1:holmgang_seatA | t_full_f1 | 269 | 85 | YES |
| f1:stavkirke_seatA | t_full_f1 | 284 | 78 | YES |

At N=8 the overlap is **6** game(s) of the 16 by-r300 kill-wins: f1:skald_seatA (kill r135, gate r71), f2:fimbulwinter_seatB (kill r136, gate r132), f2:valkyrie_seatB (kill r140, gate r98), f1:jotunheim_seatA (kill r264, gate r114), f1:holmgang_seatA (kill r269, gate r73), f1:stavkirke_seatA (kill r284, gate r66).


---

## LIMITS

1. **⚠ POPULATION 1'S SUBJECT IS THE WRONG BOT.** `s54_fc_games.json` is 65 platform first-contact games whose "us" side is **Mjolnir v180 (x3r0's line)**, not the Skalman/v628 line that would carry `SK_COUNTER_SENT`. Its core-hit profile (63/65 games take core fire; median max-streak 54) is a property of *that* bot's home defence, not of ours. **P1 is a range-check on the reconstruction and a field-side sanity read on how long alarms last; it is NOT evidence about this plank's exposure.** The plank's own subject is Population 2.
2. **POPULATION 2 IS A LOCAL FIXTURE WITH TWO AUTHORED OPPONENTS.** `opp_v542wave_noiseoff` and `opp_mjolnir_noiseoff` are frozen local trees, NOISE_OFF, one seed per (map, seat). Per CLAUDE.md this is the fixture class that "lies in a known direction", and §4.1 of the design doc measures the specific distortion that matters here: the local screen converts **504/536 Ti per game against the field's 130-173**, and its timely-checkmate rate is **12/30 = 40%** against the field's **1/65 = 1.5%**. The by-r300 win population that this precheck is asking about is therefore **~18x denser locally than in the field** (26.7% here vs 1.5% in P1). The overlap counts below are the *fixture's* overlap.
3. **DETERMINISTIC OPPONENTS ⇒ CONTENT-DUPLICATE CLUSTER LIVES.** Both P2 fixtures are byte-deterministic per (map, seat, seed); no duplicate control was run in this precheck and no interval is quoted anywhere in this document for exactly that reason. The counts are counts, not estimates with half-widths. Per CLAUDE.md's cluster-enumeration procedure: MATCH cluster — dead (one game per cell); OPPONENT cluster — live (30 games share F1, 30 share F2); MAP cluster — live (2 seats per map); CONTENT-DUPLICATE — unverified. **No DEFF-corrected claim is made and none should be read in.**
4. **THE RECONSTRUCTION IS AN UPPER BOUND ON THE SHIPPED GATE (§0):** the identified-shooter conjunct and the bank conjunct are not modelled, and the per-body streak is taken as the **max over ALL our builder bodies** rather than the **HOME KEEPER body specifically** (`_keeper_counter`, `sk_roles.py:1279`, is the only caller of `_counter_sent_action`). The keeper is not identifiable from the wire without running `skalman_fidelity._roles`, which recognises the keeper only by a "forward-action share 0.000" signature and only for our own line.
5. **⚠ THE DOC'S OWN "STREAK MEDIAN IS 11" IS NOT REPRODUCED, AND THE GAP IS NOT EXPLAINED HERE.** `sk_maps.py:1265-1266` says *"the shipped streak median is 11"*. On the v628 tape this reconstruction reads a **median max-streak of 54** (per body, max over bodies), **median 36 across all 287 individual builder bodies in P2**, and **median 52 for the longest-lived body in each game**. The most likely reconciliation — that the flag's figure is the *keeper body's* streak on the PLANK-2-ON arm, where `SK_COUNTER_PECK` marches the keeper out and gets it retired, restarting its replacement's count — is a **hypothesis this precheck did not test**. Until someone reads the keeper-body streak specifically, the two numbers are measuring different things and neither refutes the other.
6. **"By-r300 core-kill win" is defined here as: our side is the winner, the replay's win condition string starts with `core`, and OUR PARSER SAW THE ENEMY CORE'S `removeEntity` at round <= 300.** Cross-checked against `s54_fc_games.json:won` on P1 (65/65 agreement, V5) and against each `.log`'s `Winner:` line on P2 (60/60, V4).
7. **Rounds are 0-indexed** (engine convention, `get_current_round()`); replay turn index is used directly as the round number.

---

## HOW THE REGISTERED CLAIMS READ

The design doc registers one claim and one contingency. Stating how each reads,
without a build/no-build call — that is the builder's:

* **The disjointness claim** (*"a game we win at r180 has no 8-round core-fire streak … the gate's opening is essentially disjoint from the by-r300 population"*):
  * On **P1** (65 platform games, subject Mjolnir v180) it reads **consistent with disjointness**: the single by-r300 core-kill win took **zero** core hits all game, so the gate is shut in **1/1** of them at every N.
  * On **P2** (60 v628 screen games, the plank's own subject) it reads **NOT disjoint**: the gate opens in **5 of the 16** by-r300 core-kill wins at the shipped N=20 (**31.3%**) and in **6 of 16** at N=8 (**37.5%**), and in **all 5/5** of the N=20 cases it opens **30 to 206 rounds BEFORE** the kill lands.
* **The contingency** (*"if the gate opens in games we currently win by r300, the plank is r300-exposed"*): on the fixture the design doc itself nominates for the ITT primary, **that antecedent is satisfied — 5 of 16.** The exposure is not hypothetical and it is not at the tail: two of the five kill at r135 and r140.
* **A third reading the doc did not register:** the gate-open and gate-shut arms are **strongly separated but overlapping**, not disjoint — P2 by-r300 kill-win share is **5/43 = 11.6% when the gate opens** vs **11/17 = 64.7% when it does not** (N=20). The doc's *intuition* about direction is confirmed; its claim of *disjointness* is not.
