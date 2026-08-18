# INCREMENTAL MOVE-MINING STUDY — 0033 v57, THIRD pass (2026-08-18)

**agent** = fresh opus replay-study subagent, research arm. **Clock:** all
timestamps from `date -u` / corpus fields; report written 2026-08-18T03:3xZ.
Parent commit at start `7bdca3eb`; HEAD at write time `75d020ae`.

**Inputs, verbatim as named:** `docs/research/PLAYBOOK-move-mining-2026-08-16.md` ·
`docs/research/REPLAY-STUDY-0033-2026-08-16.md` (exclusion baseline, 60 games) ·
`docs/research/REPLAY-STUDY-0033-INCREMENTAL-2026-08-17.md` (exclusion baseline,
30 games) · `docs/research/move-mining-ledger.tsv` · `corpus/join.tsv`,
`corpus/meta_join.tsv`, `corpus/ladder_games.tsv`, `corpus/league_matches.tsv` ·
`replay_archive/` · `tools/replay_census.py`, `tools/replay_schema.md`,
`tools/move_miner.py` · `bots/_v488beltbreak2/` (read-only GREP).

**SNAPSHOT RULE OBSERVED.** Every corpus file was copied into the agent's
scratchpad before reading and the copy read twice: `join.tsv` 4,809 /
`meta_join.tsv` 64,182 / `league_matches.tsv` 54,971 / `ladder_games.tsv` 6,121 /
`version_trees.tsv` 94 lines on both reads, `join.tsv` md5 identical across the
two copies. No corpus file was read in place.

**NO PLATFORM MATCHES WERE FIRED. NO REPLAY WAS DOWNLOADED** — all 1,125 replays
walked were already in `replay_archive/`.

---

## 0. ⛔⛔ THE TRIGGER FIRED ON FULLY-COVERED GROUND. THE "25 UNSTUDIED MODERN GAMES" DO NOT EXIST.

This study was commissioned against `move_miner`'s 2026-08-18T03:07Z line:

```
score    40.6  '0033' v57: 25 unstudied MODERN of 85 (raw 30 of 90 on this version)
```

**That 25 is an artefact of a LEDGER-SEMANTICS violation, not a game count.**
Reproduced exactly, three independent ways:

| fact | value | source |
|---|---|---|
| (0033, v57) games on the rated tape | **90** | `ladder_games.tsv` snapshot, `opp=0033 & oppver=57` |
| …at a MODERN `ourver` (first seen < 3d) | **85** (139×5 excluded, first seen 08-14T09:12Z) | same |
| covered by the two prior studies | **60 + 30 = 90** | the two reports' own ground tables |
| coverage `move_miner` computes | **60** | `tools/move_miner.py` `_parse_ledger` uses `max()`, not `sum()` |
| ⇒ `unstudied_mod` | **85 − 60 = 25** | matches the printed line digit-for-digit |

**The two studies partition the 90 exactly, with no overlap and no gap** — an
independent reconstruction from the tape reproduces both ground sets:

* PRIOR60 = `ourver` 139(5) + 151(5) + 152(45) + 153(5) = **60** ✅ matches the s47 report
* NEW30 = `ourver` 155(25) + 157(5) = **30** ✅ matches the s50 report

**THE DEFECT IS IN THE LEDGER ROW, NOT THE TOOL.** `tools/move_miner.py`'s own
docstring (opened, lines under "LEDGER IT READS") specifies
`games_covered = the (opp, oppver) game count AT STUDY TIME` — i.e. **CUMULATIVE**.
The s50 incremental row wrote `30`, the **increment**. Under the documented
semantics `max()` is correct and `30` is the wrong value; the cell should have
read `90`. Every other ledger cell has a single row, where `max() == sum()`, so
**0033 is the only cell where the two semantics differ and it is the only cell
that mis-fired.**

⇒ **Fixed in this commit by appending a CUMULATIVE row (`games_covered = 90`),
which makes `max()` return 90 and the trigger go QUIET on 0033 until v58+.**
⇒ **STANDING RULE FOR EVERY FUTURE INCREMENTAL STUDY: `games_covered` is the
CUMULATIVE count for that (opp, oppver) cell, never the increment.** An
increment silently re-arms the trigger and costs one opus agent per boot.

**The absence of new games is REAL, not tape lag** (the failure this repo keeps
re-learning). Newest row on the whole tape `2026-08-18T02:52:59.760Z`, age 0.4 h.
0033 played **47 league matches** between our last game against them
(`2026-08-17T11:12:59.635Z`) and the snapshot, **all at v57**, against 14 named
teams — **none of them `OpenSverige`**. (They met `opensverige - plan B` ×5 and
`OpenSverige - Plan C` ×4; those are different teams.) We simply have not been
paired with 0033 in 15.7 h.

---

## 1. ⭐ WHAT THE TRIGGER *SHOULD* HAVE FOUND: 1,125 UNSTUDIED ARCHIVED GAMES, BECAUSE `join.tsv` IS LADDER-ONLY

Chasing the phantom 25 surfaced a much larger and entirely genuine blind spot.
Both prior studies took their ground from **`corpus/join.tsv`**, which carries
**only `triggeredBy=ladder` games**. `corpus/meta_join.tsv` archives far more:

| ground | n | what it is | studied before? |
|---|---|---|---|
| `join.tsv` OpenSverige-vs-0033 v57 | 90 | rated ladder | **YES** (60 + 30) |
| **GROUND A** — meta_join OpenSverige-vs-0033 v57, `triggeredBy=unrated` | **190** | our own unrated legs | **NO — zero coverage** |
| **GROUND B** — meta_join 0033 v57 vs **28 other teams** | **935** | the field playing 0033 | **NO — zero coverage** |

All 1,125 replay files were present locally (0 missing). **Ground A contains 5
games at `ourver` 159 — the incumbent `_v488beltbreak2`, completed
2026-08-18T02:46:38Z, twenty minutes before the trigger ran.** The s50 report
states its own blind spot verbatim: *"The incumbent `_v488beltbreak2` (v158/159)
has **ZERO games vs 0033** — every compatibility sketch is a GREP, never a
measurement."* **That is now false, and this report replaces the GREP with a
measurement.**

⚠ **FIXTURE HONESTY.** Ground A and 91% of Ground B are UNRATED, which per
`CLAUDE.md` pools PROTOTYPES on the *challenger's* side. 0033's side is pinned at
v57 by the wire in every game. Ground B's per-team win rates are additionally
**challenger-selected** (whoever fired the leg chose to). **Control 1 below is the
rated-only subset, which removes that selection.**

### Instrument

Custom event-stream walker (`scratchpad/walk.py`) on `tools/replay_census.py`
primitives, reproducing the two nesting traps the s50 study documented
(`PlaceEntity{Entity=1}`, `UpdatePlayers{Players=1}`) and the rotation-re-emit
guard (a gunner `placeEntity` for an existing id is a rotation, not a build).

**GATE:** `core_deliv × 10 == titaniumCollected` per team-side.
**Ground A: 190/190 clean. Ground B: 933/935 clean.** The two failures are
`841180f6…_game_2` and `cad933ac…_game_5` (both vs sporks): each is short by
**exactly one stack (10 Ti) on one side**, i.e. a final-round delivery landing
after the engine's player snapshot. **Both EXCLUDED from every number below**;
reported rather than pooled.

**BOTH-VERDICTS CONTROL — the walker was validated against the s50 study's
published anchors, which were produced by a DIFFERENT decoder:**

| quantity | s50 published | this walker | |
|---|---|---|---|
| collared 0033 gunner in `20f922f7…_game_1` | d²=2, present | **1 gunner, d²=2** | ✅ |
| …and in `b4bd82a1…_game_3` / `ed6ebb2c…_game_3` | not cited | **0 and 0** | ✅ **drives the other way** |
| harvester-tap stacks, `20f922f7…_game_1` | 244 | **244** | ✅ exact |
| 0033 conveyor heals, `b4bd82a1…_game_3` | 141 | **141** | ✅ exact |
| …and in `ed6ebb2c…_game_3` | not cited | **0** | ✅ **drives the other way** |
| 0033 barrier pecks, `20f922f7…_game_1` | 836 | **836** | ✅ exact |
| final `titanium_collected`, `20f922f7…_game_1` | us 240 / them 2,740 | **240 / 2,740** | ✅ exact |
| our gunner shots onto their core, 90 ladder games | 0 of 3,999 | see §3 | — |

One discrepancy, reported: s50 quotes **191** leak stacks in `b4bd82a1…_game_3`;
this walker reads **194**. Not load-bearing for either report's conclusion;
likeliest cause is a splitter-vs-conveyor or liveness difference in the acceptor
definition. **Flagged, not resolved.**

**Statistics.** All intervals use the platform-unrated design effect
**DEFF = 1.434** (within-opponent; Ground A is single-opponent so the opponent
cluster is degenerate) and **DEFF = 1.833** (pooled) for Ground B's multi-opponent
cuts, per `CLAUDE.md`. Every claim below that is a *fail-to-exclude* is labelled
as such and **not** laundered through the correction.

---

## 2. WHAT CHANGED vs THE PRIOR REPORTS

**Nothing about 0033 changed: v57 is the same submission and they have held it
for 4 days.** League-wide, 0033 ran **v57 from 2026-08-14T08:52Z to
2026-08-18T02:52Z (221 matches)**, with a **v58/v59/v60 excursion interleaved
2026-08-14T18:32Z → 2026-08-15T15:32Z (50 matches) and then abandoned**. They
have run **v57 exclusively since 2026-08-15T15:32Z**.

⇒ **NEW, and it is a durability fact rather than a move:** 0033 *tried* three
newer bots against the field and **rolled back to v57**. INFERENCE: v57 is their
considered best, so v57-specific counters are a durable investment, not a
perishable one. It also means the s50 report's attribution — *"0033 ITSELF
BARELY DRIFTED… the matchup changed because WE changed"* — has a mechanism
behind it now: a version number is an immutable submission, so no 0033-side
drift was possible across those 90 games (INFERENCE, from the platform's
version-numbering; not engine-probed).

**On Ground A (190 unrated games, `ourver` 139→159) our share is 31.1%
(59/190, ±7.9pp)** against the ladder's 28.3% (PRIOR60) and 46.7% (NEW30). The
per-version trend: 139 → 20.0%, 140 → 24.7%, 144 → 40.0%, 152 → 48.0%,
154 → 32.0%, **159 → 60.0% (3/5)**. n=5 at the incumbent carries no weight on its
own and is reported as a *description of the anchor games*, not a rate.

**Our timely-kill rate (core-kill by r300, ITT) on Ground A is 26.3% (50/190)**,
statistically indistinguishable from PRIOR60's 26.7% and NEW30's 20.0%. **The
s50 gross-backstop alarm — median kill round 144 → 316 — does NOT reproduce on
this fixture: Ground A's median kill round is r140** (n=57 kills). ⚠ This does
**not** retract the s50 finding: different fixture, different our-versions.
**It does mean the r316 median is not a property of `0033 v57` and should not be
quoted as one.**

---

## 3. NEW PIECES

### PIECE G — **WE ARE THE FIELD'S WORST PERFORMER AGAINST 0033, AND THE FIELD KILLS THEM** — MEASURED, 933 + 190 games

0033 v57's record in the archive, from their opponents' side:

| fixture | n | opponents | field/our win | 0033 core died, median | timely-kill ≤r300 |
|---|---|---|---|---|---|
| **FIELD** (Ground B) | **933** | 28 | **65.4% (±4.1pp)** | **r171** | **48.1%** |
| — rated subset (CONTROL 1) | 80 | 8 | **61.2%** | r196 | — |
| — unrated subset | 853 | 24 | 65.8% | r166 | — |
| **US** (Ground A) | 190 | 1 | **31.1% (±7.9pp)** | r140 | 26.3% |

**Gap: 34.3pp ± 9.4pp (two-fixture form, DEFF 1.434/1.833) — EXCLUDES ZERO.**
**CONTROL 1 is the load-bearing one:** the rated subset has unbiased pairing (no
challenger selection) and still reads **61.2%** for the field. Only 3 of the 24
teams with ≥15 games do worse against 0033 than we do (Big O 6.7%, Torsko 5.0%,
Dino 26.7%).

**This is not a new trick. It is the frame every piece below sits in: 0033 v57 is
a bot the field beats and we do not.**

---

### PIECE H — ⭐ **THE COLLAR IS NOT A GENERAL WEAPON. IT IS A WEAPON AGAINST US SPECIFICALLY — BECAUSE WE ARE THE ONLY TEAM THAT NEVER KILLS IT.** MEASURED, 1,123 games. **SHARPENS s50 PIECE A AND CORRECTS ITS GENERALITY.**

s50 Piece A measured 0033 planting gunners inside our core's firing range
(d²≤13) and associated it with our losses. **Both halves replicate on 190
independent games**, then a field control changes what the finding means.

**Replication (Ground A, 190 games, never before studied):**

| | s50 (90 ladder games) | **this study (190 unrated games)** |
|---|---|---|
| 0033 gunners sited d²≤13 of OUR core | 55.6% (174/313) | **48.6% (246/506)** |
| OUR gunners sited d²≤13 of THEIR core | 2.4% (2/85) | **2.2% (4/179)** |
| median gunner d² to enemy core (theirs / ours) | 16 / 484 | **16 / 346** |
| OUR **gunner** shots landing on their core | **0 of 3,999** | **0 of 4,233** |

**CONTROL (drives the other way, within our own team):** our **SENTINELS** put
**84.8% of 6,158 shots (5,219) on 0033's core** in the same games. The channel
resolves our-shot→their-core thousands of times; the zero is real, gunner-specific,
and **holds at every single one of our six versions, including 0 of 363 at the
incumbent v159.**

**⛔ NOW THE FIELD CONTROL, AND IT REVERSES THE GENERAL READING:**

| cut | collar-by-r100 YES | NO | gap |
|---|---|---|---|
| **FIELD 933, all games** | 74.0% (199/269) | 61.9% (411/664) | +12.1pp |
| **FIELD 933, length-matched ≥r200** | **62.9% (88/140)** | **61.9% (193/312)** | **+1.0pp — VANISHES** |
| **US 190, all games** | we win 9.2% (6/65) | 42.4% (53/125) | **−33.2pp ± 16.6pp — excludes zero** |
| **US 190, length-matched ≥r200** | we win 15.8% (3/19) | 35.3% (18/51) | −19.5pp ± 28.9pp — **does NOT exclude zero** |

⇒ **On the field the collar's apparent value is reverse causation (short games).
Against us it survives — and the s50 length-matched cell (0/11 vs 15/37) is
reproduced in DIRECTION at 3/19 vs 18/51, but this fixture's length-matched cell
does NOT clear significance on its own.** Stated as an exclusion claim, per the
DEFF direction rule: *the length-matched interval does not exclude zero here.*
The unmatched cut does.

**THE MECHANISM, and it is the piece — MEASURED, and driven to both verdicts across teams:**

| 0033's collared gunners (d²≤13 of enemy core) | built | killed | kill rate |
|---|---|---|---|
| **vs US (190 games)** | 246 | 35 | **14.2%** |
| **vs FIELD (933 games)** | 741 | 275 | **37.1%** |
| — vs Lorem Ipsum | 16 | 11 | 68.8% |
| — vs Pivot | 13 | 9 | 69.2% |
| — vs gsxWins | 94 | 58 | 61.7% |
| — vs kladde | 44 | 27 | 61.4% |
| — vs sporks | 37 | 22 | 59.5% |
| — **vs The Bisons** | 24 | **0** | **0.0%** ← instrument reads zero when zero is true |
| — **vs Pantheon** | 33 | **0** | **0.0%** |

**22.9pp ± 8.0pp — EXCLUDES ZERO.** (DEFF transferred from the game level to the
gunner level; gunners cluster within games, so treat the interval as indicative.)

⇒ **INFERENCE: the collar grinds us because we uniquely fail to remove it, not
because it is strong. The field removes it (37%) or outruns it (Bisons kill the
core first). We do neither.**

**ANCHOR — `6470b8f7…_game_5`, `ourver` 159, THE INCUMBENT, 2026-08-18T02:46Z:**
0033 plants **one gunner at d²=2** of our core. It fires **250 shots into our
core**. We build **zero gunners** all game, keep 2 sentinels (both in range), and
spend **565 of 565 heals (100.0%) on our own core** — a pure defensive grind that
never touches the gunner. **Our core dies r219.** This is the s50 anchor
(`20f922f7…_game_1`, 661 shots) reproduced on the current tree four weeks of
versions later.

**COMPAT / GREP vs the incumbent (opened):** `bots/_v488beltbreak2/raid.py:732-738`
is the forward-sentinel site and it **already gates on
`can_fire_from(bp, facing, EntityType.SENTINEL, target)` with `target` iterating
the ENEMY CORE tiles** and `bp.distance_squared(target) > 32: continue`.
`bots/_v488beltbreak2/main.py:741-752` is the home/counter-battery site and gates
`can_fire_from(bp, facing, turret_type, threat)` on a **THREAT, not the core**.
⇒ The machinery to answer a collared gunner exists (`main.py` builds *at* threats);
what is absent is any term that treats *a gunner inside our own core's d²≤13* as
the priority threat. **Smallest form: a threat-ranking term, not new machinery.**
Adjacent to `#93`; this report adds the *mechanism* (kill-rate asymmetry) and the
*field control* that says the collar is our bug, not their trick.

---

### PIECE I — ⭐⭐ **THE BISONS DELETE 0033's CORE AT MEDIAN r66 WITH A FOUR-SENTINEL BATTERY AND NOTHING ELSE.** MEASURED, 85 games. **THE MOST ON-CURRENCY THING IN THIS STUDY.**

The Bisons, at their **v9/v11/v12/v13 (current lineage — they are on v14 as of
2026-08-18T02:52Z, so this is not archaeology)**, over **85 archived games vs
0033 v57**:

* **76.5% game share**; **0033's core killed in 66 of 85 games, median round 66,
  45 of them by r75**; **timely-kill (≤r300) 77.6%**; median game length **73**.
* Their own core died in **20 of 85**.

**The entire bot, read off the wire (`builds` in the five fastest kills — the
opening is IDENTICAL every time):**

```
3 builder_bot · 7-9 conveyor · 3 harvester · 3-4 sentinel
first build: builder_bot r0 · conveyor r4 · harvester r9 · SENTINEL r20-23
ZERO barriers · ZERO launchers · ZERO gunners · ZERO builder attacks (85 games)
```

**The arithmetic closes exactly.** In `6721ad33…_game_4` (0033 core dead **r40**):
4 sentinels, **all 4 in range**, **29 shots, 28 onto the core**, 0033's core first
hit **r23**, total core damage **504** — 500 HP + 4 overkill, i.e. **~28 sentinel
hits × 18 dmg = 504, with essentially zero net healing by 0033.** Reproduced
in `f49ad94c…_game_1` (r40, 29/29 shots, 504 dmg), `16769e53…_game_3` (r41,
28/28, 504), `0354b9bf…_game_3` (r44, 30 shots/28 core, 504), `14c70ffa…_game_4`
(r44, 3 sentinels, 29/29, 504).

**THE DISCRIMINATOR IS SITING, NOT COUNT — and this is where we lose it:**

| sentinels | built | **sited within d²≤32 of 0033's core** | killed | shots onto 0033 core |
|---|---|---|---|---|
| **The Bisons** | 312 (3.67/g) | **100.0%** | **4%** | **94.7%** |
| field minus Bisons | 2,138 (2.52/g) | 68.5% | 32% | 76.5% |
| **US (Ground A)** | 419 (2.21/g) | **49.9%** | **34%** | 84.8% |
| **US at `ourver` 159** | 21 (4.20/g) | **42.9%** | 5% | 82.1% |

**Ours vs field-minus-Bisons: 18.6pp ± 6.0pp — EXCLUDES ZERO.** We build sentinels
at a comparable *rate* and **site half of them where they cannot reach the target
core** — and the incumbent v159, which builds the MOST sentinels of any version
measured (4.20/g), sites the FEWEST in range (42.9%).

⚠ **Scope of the siting measure:** d²≤32 is the sentinel's attack radius and is a
**necessary, not sufficient**, condition — a sentinel is a single-tile-wide line
shot along its facing. The Bisons' 94.7% shots-on-core says their *facing* is
right too; our 84.8% says ours mostly is, when in range at all.

⚠ **Length confound, handled and reported.** Per-game build counts are not
comparable across arms with median lengths 73 vs 206. Restricted to games that
reach r75 (so exposure is equal), the Bisons still build **2.87 sentinels by r75
vs our 1.13 and the field's 1.00**, with **0.00 barriers and 0.00 launchers vs our
2.95 and the field's 2.38**. ⚠ That window *conditions on the Bisons not having
already won*, so it selects their slowest games — it is the conservative
direction for them.

**COMPAT (<r300 kill): directly, maximally on-currency.** This is a bot that
executes our own stated doctrine at r66 against an opponent we take 31% off.
**GREP vs incumbent (opened):** the forward path `raid.py:732-738` already
implements the Bisons' exact predicate (`can_fire_from` at the enemy core, d²≤32).
What differs is everything around it: `raid.py:722` caps forward turrets at
`LOKI_FWD_GUN_CAP`; `raid.py:727` gates on `SLOT_HARVESTERS < min_harv`;
`raid.py:713` refuses the scan unless the raider is already within `dsq_core > 50`
of the enemy core; and the second sentinel site (`main.py:744`) is threat-aimed,
which is where the out-of-range half comes from. **Smallest testable form: route
sentinel builds through the core-targeted predicate and let the threat-aimed site
be the fallback rather than a peer.** ⚠ **Not admissible as a queue row until
someone can state what the incumbent's cap and harvester gate currently
evaluate to in a live game — this report GREPs them, it does not measure them.**

---

### PIECE J — 0033'S HAND-TO-MOUTH AMMO REPLICATES; SO DOES THE BELT-HEAL SPLIT — MEASURED, 190 games (CONFIRMATIONS, no new rows)

* **Ammo (s50 Piece E):** 0033 mean **6.6**, below 4 for **51.8%** of rounds, below
  10 for 69.1%; us mean **32.0**, 13.4% / 23.6%. s50 read 6.7-8.2 and 66.9-71.7%.
  **Replicated on an independent 190 games.** "More ammo" remains a dead lever.
* **Belt-heal allocation (s50 Piece C):** 0033 spends **27.2%** of heals on belt
  and 59.2% on core; we spend **7.9%** on belt and 63.9% on core. Direction and
  rough magnitude replicate. ⚠ At `ourver` 159 our belt share falls further to
  **5.4%** with **89.3% on the core** — the incumbent is *more* core-centric, not
  less.
* **Zero core-chew, both ways:** **0 builder attacks on either core footprint in
  all 190 games**, ours and theirs. Confirms the s47 era-split resolution
  (`LOKI_QUIET_ON`) on 190 games it never saw, and confirms 0033 never core-chews.
* **Harvester tap (s50 Piece B):** our harvesters leak **1,046 stacks** to 0033's
  belt vs **425** the other way — **2.46:1**. ⚠ **This is materially different from
  s50's 21.3:1** (1,129 vs 53) on the ladder fixture. The leak is real and
  directional in both, but **the 21.3:1 ratio is not a stable property of the
  matchup and should not be quoted as one.**

---

## 4. REFUTED / CORRECTED — RETAINED SO NOBODY RE-DERIVES

1. **"25 unstudied modern 0033 games exist" — FALSE.** Ledger-semantics artefact (§0).
2. **"The collar is a strong general move" — REFUTED on the field.** Length-matched
   field cut: +1.0pp (74.0→62.9% once short games are removed). It is strong
   *against us*, via the kill-rate asymmetry (14.2% vs 37.1%).
3. **"Our median kill vs 0033 moved to r316" — DOES NOT GENERALISE.** Ground A
   (190 games) reads r140. The s50 number stands for its own fixture only.
4. **"Our harvester leak runs 21.3:1" — NOT STABLE.** 2.46:1 here.
5. **"The Bisons win by out-economising 0033" — REFUTED.** Their
   `titanium_collected` is **279/game vs 0033's 545** — they are outscored on the
   tiebreak key and win anyway, by killing. Their conveyor build rate in a matched
   r0-75 window (13.50) is *below* ours (21.58).
6. **"The incumbent v159 fixed the gunner→core gap" — REFUTED.** v159 sites
   gunners much closer (median d² 95 vs 346 for older versions) and builds 3.2/game,
   yet lands **0 of 363** gunner shots on 0033's core — consistent with the s50
   GREP that `raid.py`'s value ladder carries no core term.
7. Retained from the prior reports and unchallenged here: forward-turret survival
   asymmetry, the barrier-peck sink, 0 launchers/splitters by 0033.

---

## 5. LEDGER ROW

```
2026-08-18	0033	57	90	docs/research/REPLAY-STUDY-0033-incremental2-2026-08-18.md
```

**`games_covered = 90` is CUMULATIVE (the whole v57 cell), not this study's
increment** — see §0. Coverage of the *rated* v57 cell is now 90/90 and the
trigger will go QUIET on 0033 until they ship v58+.

⚠ **Grounds A (190) and B (935) are NOT representable in this ledger**, whose key
is `(opp, oppver)` over the rated tape only. They are covered by this document and
by nothing else. **Open follow-up: the ledger has no way to record that the
unrated and cross-team archives for a given opponent-version have been mined.**

---

## 6. THE ONE THING FOR MAGNUS

**0033 v57 loses 65.4% of 933 archived games to the rest of the league (61.2% on
the unbiased rated subset) and beats us 69% of the time — we are 22nd of 25 teams
against them.** The Bisons, on a current bot, delete 0033's core at **median round
66** with **three builder bots, three harvesters, seven conveyors and four
sentinels — no barriers, no gunners, and not one builder attack in 85 games** —
while collecting **half** the titanium 0033 does. Our bot builds sentinels at the
same rate and **sites half of them out of range of the core**, fires **zero of
4,233 gunner shots** into it, and answers the one enemy gunner parked two tiles
from our core by spending **100% of its heals on its own core** while that gunner
lands 250 shots. The pieces are not exotic: **aim the sentinels at the core, and
shoot the thing that is shooting the core.**

---

## 7. PROVENANCE OF EVERY NUMBER

* **Ground A** = 190 games, `meta_join` `OpenSverige`×`0033` v57 `triggeredBy=unrated`,
  completed 2026-08-14T09:49:54Z → 2026-08-18T02:46:38Z, our versions 139/140/144/152/154/159.
* **Ground B** = 933 clean of 935 games, `meta_join` 0033 v57 × 28 other teams,
  80 ladder + 853 unrated.
* **Rated reference numbers (28.3%, 46.7%, r144, r316)** are quoted from the two
  prior reports over their own 60- and 30-game ladder grounds; nothing in this
  report re-derives them.
* Every "field" percentage is over Ground B and says so; every "our" percentage is
  over Ground A and says so. **No number pools the two.**
