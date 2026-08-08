# ouroboros_probe — RE-FREEZE SPEC (2026-08-08)

**What this is.** The behavioural specification a builder-side worker implements and
freezes as the replacement `ouroboros_probe`. Same template as the clanker_probe
pattern: research decode → reproducible spec (openings, timings, mechanism,
defects-to-preserve) → builder's worker builds → builder freezes with a battery.

**Why now.** `docs/research/elo-weighted-battery-2026-08-08.md` §5 measured an
**86.2-point calibration gap** on this leg: candidates score **93.3%** against the
frozen probe while our real win rate against the class it stands in for
(Ouroboros / Lunds Stallions / Powerpuff Girls, POST68) is **7.1%** — our #1 net-Elo
bleed class at **−102.7**. This file names what the old probe gets wrong.

---

## 0. Version tags and provenance

| | |
|---|---|
| Probe under review | `bots/ouroboros_probe/main.py`, 1,252 lines, md5 `8828b5d50039309cdc294ea07833989e` — matches the freeze md5 in `results.tsv`'s `ouroboros_probe` row. Unchanged since freeze. |
| Probe's own provenance | its docstring cites 13 replays / matches `89114461, 9934e516, b498033c, be777476, fcd3e312`, decoded 2026-08-07. **None of those five match ids are in `replay_archive/`** — the frozen probe's source corpus is not re-readable from this repo. Every "measured" figure in its docstring is therefore unverifiable here; this spec re-derives the mechanism from scratch off the 45 games that *are* archived. |
| Our live version at write time | **v74 "mineguard"** (x3r0, `bots/opp_v74`), activated 07:15 local. `_v85hsd` routed as the swap candidate (`results.tsv` `_v85hsd-bar`). |
| Corpus | 9 archived matches, **45 games**, 2026-08-07T10:29Z → 2026-08-08T06:16Z. |
| Opponent version | **Ouroboros v8 in all 9 matches.** There is no opponent-side version drift in this window: the gap is not "they patched." |
| Decode | `docs/research/2026-08-07-fanout/toolkit/replay_lib.py` (stdlib protobuf), read-only. No `fcode`, no arena, no downloads. |

### Corpus manifest

| match | date (UTC) | Ouro seat | opponent | series | maps |
|---|---|---|---|---|---|
| `22f55a05` | 08-07 10:29 | A | Powered by SmartFridge v35 | 2–3 (Ouro **lost**) | nordkap, archipelago, atoll, drumlin, moonrise |
| `bab61537` | 08-07 11:31 | A | OpenSverige **v64** | 5–0 | eider, meander, drumlin, atoll, hive |
| `071cd20c` | 08-07 14:21 | A | **v65** | 5–0 | lighthouse, meander, archipelago, atoll, fjordgate |
| `fb23a610` | 08-07 16:47 | **B** | **v67** | 4–1 | antler, jackpot, meander, saga, eider |
| `313d303f` | 08-07 19:37 | **B** | **v68** | 3–2 | archipelago, antler, meander, moonrise, atoll |
| `50f00a69` | 08-07 21:47 | A | **v69** | 3–2 | heart, fjordgate, meander, eider, jackpot |
| `067dcff2` | 08-08 01:17 | **B** | **v72** | 5–0 | lighthouse, drumlin, saga, heart, snowflake |
| `4e0874d0` | 08-08 04:58 | A | **v73** | 3–2 | eider, moonrise, hive, meander, saga |
| `621b841e` | 08-08 06:16 | **B** | **v74** | 5–0 | atoll, eider, snowflake, drumlin, antler |

**Headline record:** across the 40 games against us we won **7 (17.5%)**. Ouroboros
won 24 by core kill and 9 on the r1000 `titanium_collected` tiebreak; we won 3 by
core kill and 4 on tiebreak. Median core-kill round **r320** (r150–r816).

### Self-checks (binding, per `docs/tooling.md`)

All 45 games passed `replay_lib.check_all()` — **0 failures**: `delivery×10 ==
titaniumCollected`, `ammo converted − spent == final engine ammo`, no unknown
top/turn/update/entity fields, no recycled entity ids, HP within bounds, winner
consistent with dead cores. Two games cited explicitly as required:

- **`621b841e` g1 (atoll)** — delivery A 146 stacks / 1,460 Ti == 1,460 collected;
  B 398 / 3,980 == 3,980. Ammo A 142 − 110 = 32 == engine 32; B 2,149 − 2,104 = 45
  == engine 45.
- **`4e0874d0` g5 (saga)** — delivery A 1,185 / 11,850 == 11,850; B 90 / 900 == 900.
  Ammo A 1,278 − 936 = 342 == engine 342; B 62 − 38 = 24 == engine 24.

**Decode gotchas applied.** (a) Gunner `rotate()` re-emits `placeEntity` with the same
id — `replay_lib` routes those to `.entity_updates`; the script additionally asserted
no entity-id repeat in the gunner build stream (0 assertion failures / 45 games) and
reports rotations separately. (b) `attribute_damage=False` throughout — per-source
damage was recomputed from `Fire` events keyed by `shooter_id`, never from
`replay_lib`'s built-in split. (c) **Damage-target law**: a shot's target is the
*unit* on the tile when one is present, else the building; occupancy was checked
per event. (d) Launcher throws emit no `FireTurret` — irrelevant here (Ouroboros
builds zero launchers) but the rule was honoured for our side.

**Two honest limits.** The `"empty"` rows in the target tables (8.0% / 22.2%) include
shots that *killed* their target that round — `alive_at(r)` is False when
`death_round == r`. Do not read them as wasted fire. And the §2-R3 suppression figure
is **modelled** (probe code read against wild geometry), not measured by running the
probe — this session is read-only. §5-A6 turns it into a direct measurement.

---

## 1. V8 mechanism as played now

Everything below is `channel + game + rounds`. "d" is squared distance to the
**nearest tile of our core's 2×2 footprint** unless stated.

### 1.1 Class fingerprint — invariant, 45/45 games

- **847 turret builds, 100% Gunner.** Zero sentinels, zero launchers.
- **Zero splitters. Zero barriers.** Across all 45 games. This is as hard a
  fingerprint as gunner-only and the frozen probe already honours it.
- **446 builder melee attacks in 45 games, 89.9% on conveyors** (401 conveyor,
  45 `empty` = conveyor that died that round). **Zero on a core, a turret, a
  harvester or a barrier.** See §4 D-CRITICAL — this is the single most
  load-bearing habit in the file.
- **Zero TLEs** in all 45 games (ours: median 0 too). No CPU-pressure lane against
  this class, unlike Leviathan's 801/240/152 (`v72-bleed-nonfamily` L8).

### 1.2 Opening — builders, economy, ammo

| measure | wild median | range | probe as frozen |
|---|---|---|---|
| builders spawned by r10 | **3** | 3–5 | 5 (`OPENING_BUILDERS=5`, main.py:88) |
| builders spawned by r40 | **5** | 3–5 | 5 |
| builders spawned lifetime | **7** | 5–17 | up to 12 (`MAX_BUILDERS_TOTAL`, main.py:90) |
| builders **lost** per game | **1** | 0–15 | — (ours: median **12**, range 0–18) |
| first conveyor | **r3** | r2–r160 | after the first harvester |
| first harvester | **r4** | r2–r331 | before the first conveyor |
| Ti converted to ammo | **1,437** | 258–3,720 | (ours: median **256** — a **5.6×** gap) |
| Ti collected | **4,330** | — | (ours: median **1,460**) |

Their spawn schedule is not a trickle, it is **three clusters**: r0/r1/r2, then two
more at r8–r24, then nothing at all until a late replacement batch (observed at
r150–r330, e.g. `[0,1,2,8,9,254,276,299]`, `[0,1,2,3,4,230,233,234,235,239]`,
`[0,1,2,23,24,183,188,203,314]`). Three builders at the +20% scale cost 109 Ti of
the 500 start; five cost 222. The wild banks the difference and converts it — its
ammo balance sits at **32–56 from r25 onward** and spikes past 300 late.

Economy growth (alive counts, median over 45 games):

| round | harvesters | conveyors | splitters | barriers |
|---|---:|---:|---:|---:|
| r25 | 4 | 12 | 0 | 0 |
| r50 | 5 | 16 | 0 | 0 |
| r100 | 5 | 22 | 0 | 0 |
| r200 | 6 | 33 | 0 | 0 |
| r400 | 12 | 45 | 0 | 0 |

Builder **heal** actions: median **76/game**, range 8–787. Repairing the picket is
how a forward gunner becomes a line instead of a loss.

### 1.3 Opening gunner — f(map, our-seat), with the steering split in §6

First gunner: **median r19**, p10 **r4**, range **r2–r57**. Placed at a median
**3.5 tiles centre-to-centre from their OWN core** (not from ours). On small maps
(core gap D ≤ 9: fjordgate, meander, antler, moonrise) it lands **r2–r10**; on big
maps (D ≥ 17: archipelago, atoll, drumlin, saga, snowflake, hive) **r19–r57**.

The probe's rule — `walk = min(0.5·D, 5.5)` from home (`FIRST_FRACTION`,
`MAX_FIRST_WALK`, main.py:101-102), fired at a flat `BAND_DUE[0] = r14` (main.py:131)
— produces the right *round* at the median but the wrong *place* on every map with
D ≥ 12: probe walks 5.5, wild walks 2.1–4.1. On 17 of 45 games the probe's station 0
is ≥ 1.5 tiles further forward than anything the wild ever plants first.

### 1.4 Gunner mass growth — **the one thing the frozen probe already gets right**

| round | wild cumulative planted (median / max) | wild alive (median / max) | probe schedule |
|---|---|---|---|
| r25 | 2 / 5 | 1 / 4 | 2 |
| r50 | 3 / 6 | 2 / 6 | 3 |
| r75 | 4 / 9 | 3 / 7 | 4 |
| r100 | 5 / 11 | 3 / 10 | 5 |
| r150 | 8 / 16 | 5 / 15 | 7 |
| r200 | 11 / 20 | 6 / 15 | 10 |
| r300 | 18 / 25 | 11 / 18 | 19 |

Gunners built per game: median **20**, range 2–45. **The gap is not a volume gap.**
Preserve `BAND_DUE` / `CREEP_INTERVAL` / `SIEGE_INTERVAL` cadence arithmetic
verbatim; change where the gunners go and who plants them (§2 R1/R2).

### 1.5 The picket is bimodal, not a march

847 gunner sites by d to our core:

| band | n | share | median lifespan |
|---|---:|---:|---:|
| **d > 144 (their own house)** | 191 | 22.6% | **179 rounds** (all d>64: n=305) |
| d 65–144 | 114 | 13.5% | ” |
| d 27–64 | 206 | 24.3% | **64 rounds** (all d≤64: n=542) |
| d 10–26 | 200 | 23.6% | ” |
| **d ≤ 9 (the killers)** | 136 | 16.1% | ” |

Roughly a quarter of every game's gunners never leave their own doorstep and live
~3× as long as the forward ones. That home block is a **screen**, and it is what
keeps their builder losses at a median of 1/game against our median of 12.

The screen's fire profile (gunners spawned at d > 13, n = 8,473 shots): **44.3%
conveyor**, 22.2% empty, 22.0% builder_bot, 4.2% sentinel, 2.8% harvester,
2.4% gunner. It suppresses our forward economy and our raiders; it is not aimed at
our core at all.

### 1.6 The strike — how they actually kill

- **First gunner at d ≤ 9: median r124**, range r2–r748, present in **34/45** games.
- It arrives as a **burst**: median **2** gunners planted at d ≤ 26 within a
  12-round window (range 1–4). `621b841e` g4 (drumlin): r218 @(2,6) d9, r220 @(3,4)
  d5, r224 @(5,3) d4 — three in seven rounds. `621b841e` g2 (eider): r153, r158,
  r158, r158, r161 — five in nine.
- Killer-site geometry (d ≤ 13, n=174): d1 ×24, d2 ×7, d4 ×30, d5 ×30, d8 ×12,
  d9 ×33, d10 ×20, d13 ×18. **69% face toward our core** (120/174) — they mis-aim
  about a third of doorstep plants.
- Their fire profile once at d ≤ 13 (n = 6,887 shots): **65.5% core**, 14.9%
  conveyor, **8.2% builder_bot**, 8.0% empty.
- **Top-3 shooters account for a median 100% of all shots that ever hit our core**
  (n=30 games with core damage). The kill is done by two or three specific turrets.
- **Median 174 rounds from the first d ≤ 9 gunner to our core's death** (51–394).
- **25 core kills; 6 of them (24%) with zero HP healed** — the "504 damage / +0
  heal" signature, i.e. a 500 HP core taken down by 72 unopposed gunner shots
  because every one of our builders was already dead.

### 1.7 Their kill condition against us — `621b841e`, five games of fresh evidence

We were seat A, v74 "mineguard". **0–5, −16.9 Elo.**

| game | map | rounds | their gunners | the killers (round @tile, d, core shots) | our core dmg / healed | our builders lost | their builders lost | ammo converted (them / us) |
|---|---|---:|---:|---|---|---:|---:|---|
| g1 | atoll | 354 | 24 | **r143 @(6,14) d9 → 187 shots**; r278 @(5,17) d8 → 71; r107 @(5,17) d8 → 13 | 1,981 / **+1,477 (75% absorbed) and still died r353** | 11 of 13 | **0 of 5** | 2,149 / 142 |
| g2 | eider | 215 | 17 | r153 @(7,13) d9 → 35; r158 @(10,9) d4 → 22; r199 @(5,9) d4 → 15 | 504 / **+0** — clean 72-shot kill, all 13 builders dead by r200 | 13 of 13 | **0 of 5** | 1,199 / 330 |
| g3 | snowflake | 476 | 24 | r429 @(4,8) d5 → 38; r436 @(4,6) **d1** → 34; r245 @(7,8) d5 → 14 | 602 / +98 (14%) | 18 of 18 | 1 of 8 | 1,980 / **104** |
| g4 | drumlin | 271 | 24 | r220 @(3,4) d5 → 36; r224 @(5,3) d4 → 29; r218 @(2,6) d9 → 28 | 651 / +145 (18%) | 12 of 13 | 2 of 6 | 1,331 / 392 |
| g5 | antler | 1000 | 11 | r69 @(7,8) d9 → 68 (only one) | 476 / +434 (48%) — **core survived** | 18 of 18 | 3 of 10 | 2,050 / 356 |

**The kill condition, stated plainly.** They win the builder-attrition war 12:1 from
behind a home screen, so by r150–r250 we have no heal line left. Then two or three
gunners are planted inside d ≤ 9 in a burst of a few rounds, and a 500 HP core dies
to ray fire at 7 damage a shot with nobody standing next to it. **They never melee
the core** — 0 builder attacks on our core in all five games. g5 is the control:
their strike group never formed (one killer, r69), our core absorbed 48% of
incoming, and the game went to r1000 — where they still won on titanium 9,720 to
8,140.

The economy underneath is the enabling condition, not a side note: they out-collect
us 1.2–2.7× and out-convert us **5.6×** (median 1,437 vs 256 Ti to ammo). In g3 we
converted **104 Ti of ammunition in a 476-round game.**

### 1.8 Endgame / tiebreak

14 of 45 games reached r1000; **Ouroboros won 10.** Their r1000 titanium in wins:
9,750 / 11,850 / 11,980 / 14,930 / 15,340 / 16,430 / 22,550 / 22,680 / 31,540, and
they lead on harvesters alive in every one (e.g. `067dcff2` g4: **22,550 vs 740**
Ti, 18 vs 6 harvesters). The four r1000 games we won are the four where their
economy under-ran ours by ≥ 2× (`313d303f` g2 2,470 vs 13,100; g3 3,220 vs 10,140;
`50f00a69` g1 4,500 vs 19,840; g5 4,920 vs 9,510). **Their default plan when the
strike fails is to win the tiebreak, and it usually works.** Any probe that
under-builds economy converts a real loss into a fake win at r1000.

---

## 2. What the old probe gets wrong

### 2.0 The calibration arithmetic first

The frozen probe's own `results.tsv` row is the primary document:

> `ouroboros_probe … frozen … Fidelity criteria MET (first gunner r14-26, builder
> attrition matches wild kill sequences); **strength 4/8 vs _v72e2 = GENTLER than
> wild 14/15** — verdicts understate real Ouroboros pressure, **safe direction**.
> Known gaps: seat-B legs weakest, endgame under-closes on big maps, ammo overshoot
> artifact in r1000 games.`

So **at freeze the probe won 50% where the wild won 93% — a 43-point gap, measured,
documented and accepted as "safe."** It is not safe: a gentle instrument used as a
*gate score* manufactures confidence rather than withholding it.

What happened next is the other half of the 86. Left column = the ouro leg score of
whichever candidate was under gate in that window (`results.tsv`, not the live
version's own score); right column = what the live version actually did on the
ladder against Ouroboros v8 in the same window:

| window | ouro leg score under gate | wild games won vs Ouroboros v8 |
|---|---|---|
| v64-era long run | 72.5 / 240 | 0 / 5 (`bab61537`) |
| v65 | — | 0 / 5 (`071cd20c`) |
| v67 (`opp_v67` field profile) | 71.7 | 1 / 5 (`fb23a610`) |
| v68 (6b, 6c gates) | 66.7 → 68.3 | 2 / 5 (`313d303f`) |
| v69 (6d race) | 75.0 / 80.0 | 2 / 5 (`50f00a69`) |
| v72 (`_v82c1`, `_v84g` bars) | 78.3 → 83.3 | 0 / 5 (`067dcff2`) |
| v73 / hs, hsd | 83.3 / 85.0 / 86.7 | 2 / 5 (`4e0874d0`) |
| v74 / hsb | **93.3** | **0 / 5** (`621b841e`) |

**The instrument moved +20.8 points. Reality moved zero** (7/40 games across the
whole span, no trend). Seven versions of our line optimised against a frozen soft
target and the leg score tracked the optimisation, not the matchup.

### 2.1 Ranked behavioural deltas

---

**R1 — THE PROBE HAS NO HOME SCREEN; ITS ENTIRE FORCE WALKS THE LANE.**
*Highest gap contribution.*

| | frozen probe | wild v8 |
|---|---|---|
| who plants | **one latched picket builder** (`_picket_latch`/`SLOT_PICKET_ID`, main.py:626-649); assists only after `SLOT_GUNNERS ≥ 6` and only every third builder (`_assist_open`, main.py:612-624) | 5–17 builders, three spawn clusters, planting from wherever they stand |
| where | every station on the own-core→enemy-core lane, `_first_standoff` (main.py:372-378) down to `CORE_STANDOFF = 1.6` (main.py:124) — i.e. onto our doorstep | **22.6% of 847 gunners at d > 144 of our core**, median lifespan **179 rounds** |
| builders lost | one walker, repeatedly, deep in our half | **median 1 per game**, range 0–15; 20% of their builders never leave d ≤ 6 of home; median max excursion 11.7 tiles |

**Consequence.** Our whole measured answer to the probe is *kill the walker* — and
the probe hands us a single point of failure the wild does not have. When the picket
builder dies, `_run_picket` (main.py:651-…) cannot plant (`near` or
`stuck ≥ 6 and dsq ≤ 20` is required), the latch takes ≥ 3 rounds to reassign, and
the replacement re-walks the whole lane. In the wild the ladder never stalls, because
most of the line is planted from safety and only the last two or three need an
excursion. **This is the mechanism the 93.3% is measuring, and it is not the wild's.**

---

**R2 — AGGRESSION TIMING: the probe's killer is ~50 rounds late and always alone.**
*High.*

Wild: first d ≤ 9 gunner at **median r124**, and it comes as a **burst** — median 2
inside d ≤ 26 within 12 rounds; 3-in-7 and 5-in-9 observed in `621b841e` g4/g2.
Two-to-three simultaneous rays is what the measured kill needs: top-3 shooters =
median 100% of all core shots; median 174 rounds from first killer to core death.

Probe: on a D = 12 map the interpolated stations first reach d ≈ 9 around station
7–8 (`_standoff`, main.py:393-395) → **r152–r176**; the true doorstep station
(`CORE_STANDOFF`) is due **r224**, and the tightened `SIEGE_INTERVAL = 9`
(main.py:138) burst cadence only begins *after that*. So the probe delivers its
first core-threatening gunner ~30–50 rounds late and its burst ~100 rounds late —
50–100 extra rounds for a heal line, and never more than one new ray at a time
before r224.

---

**R3 — TARGET SELECTION: builder-first is wrong for the killers, and it can suppress
the shot outright.** *High-medium — and it is a code defect, not a calibration
choice.*

`_pick_target` (main.py:1077-1124) ends:

```python
choice = best_builder or best_core or best_turret or best_eco or best_any
```

— a builder **always** outranks the core. And `_run_gunner` (main.py:1053-1074):

```python
target = self._pick_target(ct, pos)
if target is not None:
    try:
        if ct.can_fire(target):
            ct.fire(target)
            return
    except GameError:
        return
    return          # <-- no fallback to the core, no rotate
```

A gunner's ray **stops at the first targetable tile**, so a builder standing further
down the ray *behind* the core is still in `get_attackable_tiles()` (which ignores
occupancy), is still chosen as `best_builder`, `can_fire()` is False — and the probe's
gunner **does nothing that round**. No fallback, no rotate.

Modelled exposure over the corpus: **454 / 4,555 = 10.0%** of all wild core shots had
one of our builders further along the same ray. But that is the wrong average to
quote — in the three games where our heal line was actually staffed it is
**53.3% (`50f00a69` g2), 43.5% (`4e0874d0` g1), 36.4% (`067dcff2` g4)**. Those are
exactly the games a heal-line candidate is being gated on.

Against that, the wild's killers put **65.5% of their fire into the core and 8.2%
into builders** (n = 6,887). The probe inverts the priority *and* punishes itself for
the inversion.

---

**R4 — ROTATION THROTTLE: probe ~1.5 per gunner, wild 2.78.** *Medium.*

Measured: **median 2.78 rotations per gunner** (mean 3.43, per-game range 0–15.5;
`22f55a05` g3 atoll = 372 rotations over 24 gunners). The probe's docstring claims
"~1.5 per gunner lifetime" and enforces it with `ROTATE_MIN_GAP = 5`,
`ROTATE_MIN_TITANIUM = 40` (main.py:148-149) plus the structural rule that
`_rotate_to_reacquire` is only reached when `_pick_target` returns **None**. A gunner
that re-aims twice as often tracks a moving heal line; one that doesn't gets walked
around. (Note the interaction with R3: because the bare `return` pre-empts it, the
probe under-rotates *even more* than its own constants intend.)

---

**R5 — OPENING SPEND: five bodies by r5 instead of three by r2.** *Medium.*

`OPENING_BUILDERS = 5`, one per round from r0 (main.py:88). Wild: **median 3 by r10,
5 by r40, 7 lifetime**. At +20% scale per builder that is 222 Ti vs 109 Ti out of the
500 start, and it inflates the cost scale of every gunner in the match. The wild
spends the difference on ammunition — balance **32–56 from r25**, median **1,437 Ti**
converted per game. `BUILDER_TRICKLE = 40` (uniform 1/40 rounds) is also the wrong
shape: the wild's replacements come as a single late batch (r150–r330), leaving a
100+ round mid-game window in which a killed Ouroboros builder is simply not
replaced (see §4 D6).

---

**R6 — GUNNER MASS IS ALREADY CORRECT. Do not "fix" it.**

Probe cumulative 2/3/4/5/7/10/19 vs wild median 2/3/4/5/8/11/18 at
r25/50/75/100/150/200/300. This is the dimension a naive re-freeze would over-correct
("make it harder → build more gunners"), and it would be wrong. **The gap is
placement, timing, survivability and targeting — not volume.**

---

**R7 — THE PROBE IS *HARDER* THAN THE WILD IN ONE DIMENSION: ammo discipline.**

**4,779 of 15,360 wild gunner shots (31.1%) resolve onto one of our conveyors** under
the damage-target law (unit-on-tile first, else building) — about **19,100
ammunition** across 45 games spent chipping 20 HP / 3 Ti conveyors at 4 ammo a shot.
(The looser "tile had a conveyor on it" count is 5,330 / 34.7%; the difference is
rounds where one of our builders was standing on the conveyor and took the hit
instead.) The probe ranks `ECONOMY_TYPES` **fourth** in `_pick_target`. A
re-freeze must **add this waste back**, not keep the tighter behaviour (§4 D1). Stated
here so the worker does not read §2 as "make everything more aggressive."

---

## 3. Seat-lock check

**The historic lock is REFUTED for the v8 era.** `HANDOVER.md` ("FIRST ACTIONS" §3)
records *"Ouroboros is PLATFORM SEAT-LOCKED (they hold seat A 13/13, p≈0.008) — only
unrated legs can ever read our seat-A matchup."* The archive, ordered by
`completedAt`:

`22f55a05` A → `bab61537` A → `071cd20c` A → **`fb23a610` B** → **`313d303f` B** →
`50f00a69` A → **`067dcff2` B** → `4e0874d0` A → **`621b841e` B**

**The lock broke at 2026-08-07T16:47Z.** Ouroboros has taken seat B in **4 of the
last 6 matches**, including both of the freshest 0–5 wipes. Consequence for the
builder: **seat-A legs no longer require unrated challenges**, and the standing
"repeat challenges until the seat flips" instruction in HANDOVER is stale.

**Game-level results by OUR seat (40 games):**

| our seat | games won | rate |
|---|---|---|
| A | 3 / 20 | 15.0% |
| B | 4 / 20 | 20.0% |

**No asymmetry at this n.** Per version: v64(B) 0/5, v65(B) 0/5, v67(A) 1/5,
v68(A) 2/5, v69(B) 2/5, v72(A) 0/5, v73(B) 2/5, v74(A) 0/5.

**Confound, stated rather than buried.** Seat and *lineage* are collinear in this
corpus: every x3r0-lineage version we have (v68, v72, v74) played seat A; every
Eir-lineage version except v67 played seat B. The tempting read — "recent seat A is
2/15 while recent seat B is 4/10" — **cannot be separated from "the x3r0 lineage is
worse against this class."** Do not spec a seat-conditional branch on this evidence.

**What is safe to carry into the spec:** the probe must be seat-general (the frozen
one already is, by geometry rather than by coordinates — keep that), and the freeze
battery must run **both seats on every map**, since the frozen probe's own row flags
"seat-B legs weakest" and the wild's freshest wipes are exactly its seat-B matches.

---

## 4. Defects to preserve

The clanker_probe rule: a probe that fixes their bugs trains us against a phantom.
These are measured habits the re-freeze **must** reproduce.

**D-CRITICAL — Ouroboros has no answer to anything outside gunner range except
planting another gunner.**
Across 45 games: 847 turrets, **0 sentinels / 0 launchers**; **0 barriers /
0 splitters**; and **446 builder melee attacks of which 401 (89.9%) hit a conveyor
and 45 are conveyors that died that round — zero against a core, a turret, a
harvester or a barrier.** Their gunner reaches r² = 13. A turret planted at
d² = 14–40 of their core is unanswerable by their entire kit except by walking a
builder out and planting a gunner within 13 of it. In every one of our 3 core-kill
wins the mechanism was an early standoff sentinel and their economy strangled to
**850 / 0 / 70 Ti collected** (`4e0874d0` g2 moonrise r94; `4e0874d0` g4 meander
r154 — where they held 2 harvesters and 9 conveyors and delivered **literally zero
titanium** for 155 rounds; `fb23a610` g3 meander r257). Our wins' median first
standoff-sentinel round is **r5**; our losses' is **r15**.
*If the re-freeze gives the probe any way to answer an out-of-range turret — a
sentinel, a barrier screen, a melee raid — it erases the only exploit lane the
corpus contains.*
**Honest bound on that lane:** we plant a standoff sentinel in 39 of 40 games and
still lose 33 of them. Our 78 sentinels have a median lifespan of **25 rounds** and
63 of 78 die — their answer is to walk a builder out and plant a gunner within
r² = 13 of it (411 of their shots hit one of our sentinels). So the exploit is *"a
standoff turret they cannot answer without an excursion,"* not *"a standoff turret
is invulnerable"* — and the excursion is exactly the thing the corpus says they are
reluctant to make (median 1 builder lost per game). The lever is timing (r5 vs r15)
and keeping the tile out of gunner-plantable range, not the plant itself.

**D1 — Conveyor chipping.** 31.1% of all shots (4,779/15,360), ~19,100 ammunition
into 20 HP / 3 Ti conveyors. Reproduce it: a gunner fires at whatever economy is on
its ray rather than holding for a better target.

**D2 — Fixed-tile rebuild.** **36 of 45 games** contain at least one gunner tile
rebuilt. Worst: `071cd20c` g2 tile (8,5) **×18**; `067dcff2` g3 (11,1) ×10;
`313d303f` g1 (16,16) ×9; `067dcff2` g4 (6,10) ×7 — that last one **independently
reproduces `v72-bleed-nonfamily` L7's count of 7 rebuilds at (6,10)** from a separate
decode, which is a useful cross-validation of both files. They re-plant into a
covered ray at 20 Ti a time on a +20% scale. Our L7 lever is priced against exactly
this; a probe that relocates instead of rebuilding deletes the lever.

**D3 — No splitters, no barriers, ever.** 0 and 0 in 45 games. No defensive walling,
no delivery multiplexing; their runs are plain chains.

**D4 — No builder melee against a core.** 0 in `621b841e`'s 5 games; 0 across the
whole corpus. They will not finish a low core by hand — a core at 20 HP with no ray
on it survives.

**D5 — Zero TLE.** Their turns are cheap; there is no CPU-pressure lane. Do not build
a probe that burns budget "for realism."

**D6 — Late replacement batch.** Spawns cluster at r0–r2 and r8–r24, then nothing
until a late batch at r150–r330. A builder killed in the mid-game is not replaced for
100+ rounds.

**D7 — Mis-aimed doorstep plants.** Only **69% (120/174)** of gunners planted at
d ≤ 13 face toward our core. Roughly a third arrive pointing the wrong way and pay
10 Ti a rotate to fix it.

**D8 — Delivery can break outright.** `4e0874d0` g4 (meander, 155 rounds):
2 harvesters and 9 conveyors alive, **0 deliveries, 0 titanium collected**, 2 gunners
built all game. Their chain-wiredness is not guaranteed. A probe whose economy never
fails is a probe that never hands us the game the way the wild occasionally does.

---

## 5. Freeze battery design notes (for the builder)

### 5.1 Maps and seats

Corpus map frequency: meander 6, atoll 5, eider 5, drumlin 4, archipelago 3, saga 3,
moonrise 3, antler 3, lighthouse 2, fjordgate 2, heart 2, snowflake 2, hive 2,
jackpot 2, nordkap 1. Mechanism coverage:

| maps | core gap D | mechanism they exercise |
|---|---|---|
| **fjordgate, meander** | 5.7 / 7.0 | the r2–r8 opening gunner and the immediately-core-threatening profile. If the probe cannot plant by r4 here it is wrong. |
| **eider, heart** | 12.0 | mid-lane creep + strike burst. eider is where our kladde/ouro legs are historically weakest and where `621b841e` g2 produced the clean 504/0 kill. |
| **drumlin, atoll, snowflake, saga, archipelago** | 17–20 | **the home-screen regime** — 2–5 gunners at d > 144 for the first ~50 rounds, first strike after r120. This is where R1 is most wrong and where the freeze must be validated hardest. |
| **antler** | 8.0 | the r1000 tiebreak lane (`621b841e` g5: 11 gunners, no core kill, won 9,720 vs 8,140). |
| **hive** | 25.5 | longest lane; first gunner r42–r43, tile-stable across two of our lineages. |

**Both seats, every map.** Non-negotiable given §3.

### 5.2 Acceptance signature

Measured off the new probe's own replays with the same decoder and the same
gotchas. Hard-fail items are marked ✱.

| # | signature | target |
|---|---|---|
| **A1**✱ | turret and building mix | 100% gunner; **0** sentinel, launcher, splitter, barrier |
| **A2**✱ | melee profile | ≥ 85% of builder attacks on conveyors; **0** on cores/turrets/harvesters |
| **A3** | builders | ≤ 3 spawned by r10, ≤ 5 by r40, 5–9 lifetime in a ≤ 400-round game; **probe builder deaths ≤ 3/game** against a v74-class opponent (wild median 1) |
| **A4** | site distribution | ≥ 20% of its gunners at d > 144 of the opposing core with median lifespan ≥ 150 rounds; 12–20% at d ≤ 9 |
| **A5** | mass | cumulative planted within **±2** of 2/3/4/5/8/11/18 at r25/50/75/100/150/200/300 |
| **A6** | strike | first d ≤ 9 gunner by **r140** (median over the battery); ≥ 2 gunners at d ≤ 26 inside some 12-round window; top-3 shooters ≥ 85% of all core shots |
| **A7**✱ | targeting | for gunners spawned at d ≤ 13: core **55–75%**, builder ≤ 15%. And the **R3 direct test**: rounds in which a gunner had a legal shot but took none because its chosen target was unfireable must be **< 2%** of gunner-rounds |
| **A8** | rotation | 2–4 rotations per gunner |
| **A9** | ammunition | ≥ 1,000 Ti converted in a ≥ 300-round game; balance never below 16 while titanium > 60 |
| **A10** | economy | first conveyor ≤ r5, first harvester ≤ r6; harvesters alive 4/5/5/6 and conveyors 12/16/22/33 at r25/50/100/200 (±30%) |
| **A11** | defects | ≥ 25% of shots on enemy conveyor tiles; ≥ 1 gunner tile rebuilt in ≥ 70% of games |

### 5.3 The wild-gap validation (the part the last freeze skipped)

Fidelity was "MET" at the last freeze too, and it still produced an 86-point gap.
**Fidelity alone must not be sufficient for acceptance.** Add a predictive gate:

1. **Anchor set.** We hold wild ladder results for eight of our own ladder versions
   against Ouroboros v8, on named maps (§0 manifest): v64 **0/5**, v65 **0/5**,
   v67 **1/5**, v68 **2/5**, v69 **2/5**, v72 **0/5**, v73 **2/5**, v74 **0/5** —
   **7/40 = 17.5%** for us, **82.5%** for the wild.
   **Binaries available for six of the eight:** `bots/opp_v67`, `opp_v68`,
   `opp_v69`, `opp_v72`, `opp_v74`, and `bots/_v84g` (= ladder v73 "Eir 7", per
   `HANDOVER.md`/`results.tsv`). Ladder v64 and v65 have **no** snapshot under
   `bots/` — the `_v64cbA`/`_v65lw` directories are local commit-counter names, not
   ladder versions, and the builder must confirm the counter↔ladder mapping before
   using any `_vNN` directory as an anchor. **Runnable anchor = 30 games, wild
   record 23/30 = 76.7%** (ours 7/30 = 23.3%).
2. **Acceptance.** Run the new probe against those six versions on those maps, both
   seats. **The probe's win rate must have a Wilson interval containing 76.7%.**
   The frozen probe would score roughly 7–28% on that anchor — *inferred*, not
   measured here, from the leg scores our line posts against it (72.5–93.3%). A probe
   that loses 72–93% of the time to our own line, while the wild wins 76.7% of the
   time against exactly those binaries, is the wrong instrument regardless of how
   well its behaviour tables match. Measure the anchor rather than assuming it.
3. **Standing rule afterwards.** The ouro leg score is only quotable **next to the
   class's live win rate**. If the two diverge by more than 25 points for two
   consecutive measurement windows, the instrument is declared stale and re-freezes.
   This is the general fix for the failure mode, not just this instrument's patch.
4. **Class-representativeness note.** The leg stands in for a three-team class
   (Ouroboros 17 matches / 5.9%, Lunds Stallions 19 / 5.3%, Powerpuff Girls 16 /
   37.5% — FULL window). Ouroboros alone is 5.9%, so **class breadth is not the
   explanation for the gap** — the probe misrepresents Ouroboros itself. But note
   that Lunds ships versions fast (v37→v42→v44→v45→v47 inside 24h in the archive)
   while Ouroboros has been pinned at v8 all window; a second instrument for Lunds
   is a separate, later ticket and should not be smuggled into this freeze.

---

## 6. Steering caveat — stable vs conditional

`docs/research/ouroboros-v65-era-reverify-2026-08-07.md` established that their
deterministic queue diverges by **r3** keyed on our **opening signature**, not on
casualties. This corpus reproduces that and, for the first time, **bounds** it.
Grouping the first gunner by `(map, our seat)` across eight of our versions:

**STABLE** — same tile, round within ±4 (these are *validation targets for the
policy*, never constants to embed):

| map / our seat | observations |
|---|---|
| snowflake / A | v72 **r22 @(17,18) NW**, v74 **r22 @(17,18) NW** — identical |
| fjordgate / B | v65 **r2 @(4,6) E**, v69 **r2 @(4,6) E** — identical |
| atoll / A | v68 r19 @(12,3) W, v74 r21 @(12,3) W |
| atoll / B | v64 r27 @(3,12) N, v65 r31 @(3,12) N |
| meander / A | v67 r3 @(11,8) N, v68 r2 @(11,8) N |
| archipelago / B | v65 r28 @(7,7) SE — **and `22f55a05` vs SmartFridge r28 @(7,7) SE**, i.e. stable across a completely different opponent |
| saga / A | v67 r41 @(16,16) NW, v72 r26 @(16,16) NW — tile stable, round varies 15 |
| hive / B | v64 r43 @(6,16) E, v73 r42 @(6,17) NE — ±1 tile |

**CONDITIONAL** — same map, same seat, different tile:

| map / our seat | observations |
|---|---|
| eider / B | v64 r12 @(12,9), v69 r21 @(13,11), v73 r29 @(14,10) — three tiles, 17 rounds of spread |
| eider / A | v67 r13 @(15,9), v74 r14 @(14,12) |
| meander / B | v64 r4 @(13,6), v65 r8 @(8,6), v69 r5 @(12,6), v73 r4 @(10,6) — **row y = 6 invariant, column is not** |
| antler / A | v67 r7 @(7,8), v68 r8 @(7,9), v74 r5 @(4,9) |
| drumlin / A | v72 r34 @(16,14), v74 r21 @(14,17) |

**Spec rules that follow.**

1. **Hardcode nothing at tile granularity.** Express every station as a policy over
   (own core, enemy core, map geometry), exactly as the frozen probe already does —
   that part of its design is correct and must survive. What changes is the policy's
   *shape* (R1/R2), not its parameterisation style.
2. **Only the STABLE column may be used as an acceptance target**, and only as
   "the probe reproduces this row," never as an input.
3. **Everything in §1.1–§1.6 that is quoted as a corpus-wide median is stable across
   our opening variants** — the gunner-only fingerprint, the zero-splitter/zero-barrier
   rule, the conveyor-only melee, the mass curve, the site-band distribution, the
   home-screen lifespan ratio, the 2–3-shooter kill, the ammo ratio. Those are the
   spec's load-bearing content precisely because they do **not** vary with `f(our
   opening)`.
4. **The freeze battery must run against at least three of our lineages** — one
   Eir-line binary, one x3r0-line binary, and one older `opp_v6x` — so that a probe
   accidentally tuned to a single opening signature is caught before it is frozen.

---

## 7. One-line builder handoff

**Build the home screen first:** re-shape the picket from "one latched builder walks
the lane to the enemy doorstep" into "2–5 gunners planted within ~3 tiles of its own
core in the first 50 rounds by multiple builders that never leave home, then a
2–3-gunner burst into d ≤ 9 at ~r124" — and land R3's two-line targeting fix
(core-before-builder for gunners inside d ≤ 13, plus a fallback shot instead of the
bare `return`) in the same change, since it costs nothing and is measurable by A7.

---

## Method notes

- **Scripts** (scratch only, not committed):
  `…/scratchpad/{ouro,deep,deep2,deep3,deep4}.py`, all importing the validated
  `docs/research/2026-08-07-fanout/toolkit/replay_lib.py` + `siege_geometry.py`.
  No new decoder was written.
- **Map identification** by exact `(width, height, wall count, ore count)` match
  against `maps/*.map26` — zero ambiguous, zero UNKNOWN across 45 games, zero
  `fcode` calls (the denial-book §0.2 method).
- **What was not computed.** BFS deniability margins / min-cut geometry (not needed
  for this question). Per-build `builder_id` attribution is not populated on this
  decoder path, so "which builder planted each killer" is unmeasured — builder
  excursion statistics stand in for it. The probe was **not run** (read-only
  session): every probe-side claim is a code read, and the one quantitative
  probe-side claim (R3) is explicitly labelled *modelled* and is converted into a
  direct measurement by acceptance item A7.
- **Read-only compliance.** No bots edited, no arena or platform commands, no
  downloads, `HANDOVER.md` and the coordination tape untouched. This file is the
  only write.
