# CUT #116 — DO BEAN COUNTERS ANSWER A GUN ON THEIR OWN BELT?

**Commissioned:** RESEARCH s54, 2026-08-21 (`scratchpad/s54_116_beltgun_commission.md`),
discharging `QUEUE.md` row #116 — the gap named by
`docs/research/PLAYBOOK-beancounters-2026-08-21.md` §8 caveat 6 as *"THE BIGGEST
UNMEASURED CELL IN THE BOOK"*.
**Agent:** decode-only analysis agent. Read-only except this file and
`scratchpad/s54_116_*`. **Nothing fired, submitted, committed; no bot, queue,
tool, corpus or ledger file touched.**
**Clock:** `date -u` in-shell **2026-08-21T17:08:47Z**. Repo HEAD `db33fb9b7`.
`corpus/manifest.json` `built_utc = 2026-08-21T17:01:16Z`.
**Denominator:** the s53 **frozen set** — 1,385 archived Bean counters replays
(`scratchpad/s53_bean_census.jsonl`, v47 1,235 / v68 90 / v64 60), the same set
the base study used. v64 is not analysed (era split is v47/v68 per the brief).

**ANSWER IN ONE LINE.** **Yes, they answer it — the row's premise of "no removal
loop for a belt shooter" is REFUTED at population scale.** A Bean counters
belt-gun is removed **75.9% ± 3.1** of the time (v47, n=837 games / 3,034 turret
lives), median **11 rounds** after the gun first covers a live belt tile, against
their **79.7% ± 2.2** castle clearance — the two cells overlap. **What is real
and exploitable is narrower and it is a COVERAGE hole, not a blindness:** the
sub-class that actually eats belt tiles is shot at **47.5% ± 4.4** against
**67.8% ± 3.3** for a turret in the same half that is not aimed at the belt, and
**41.3% of belt-cutters never enter any live BC turret's reach at all.** When BC
*can* reach one it turns on it exactly as readily as on anything else
(reach→aim 71.6% vs 74.0%, median latency **0 rounds**). **INFERENCE: the belt is
long and the guns are short; the hole is geometric, not logical.**

---

## §1 METHOD VALIDATION — three known cells reproduced, two placebos driven

Per the collar-heal standard: nothing below is trusted until this pipeline has
produced a number that is already known to be right.

### 1.1 KNOWN CELL A — the base study's forward-turret clearance table

`docs/research/REPLAY-STUDY-beancounters-v47v68-2026-08-21.md:415-429` (opened),
definition verbatim: *"forward turret = a gunner/sentinel the attacker built
closer to the defender's core than to its own; removal = a death of that kind on
that tile at a later round"*, games as units, DEFF 1.833.

Rebuilt from `corpus/events.tsv` (`scratchpad/s54_116_repro.py`):

| cell | study | **this pipeline** | games | turrets |
|---|---|---|---|---|
| BC v47, ALL games | 79.7% ± 2.2 | **79.7% ± 2.2** | **1,131** (study: 1,131) | **5,803** (study: 5,803) |
| their opponents, v47 | 33.5% ± 3.0 | **33.5% ± 3.0** | **1,047** (1,047) | **3,881** (3,881) |
| BC v68, ALL games | 76.6% ± 11.1 | **76.6% ± 11.1** | **61** (61) | **117** (117) |
| their opponents, vs v68 | 53.3% ± 6.5 | **53.3% ± 6.5** | **90** (90) | **511** (511) |

**Every cell reproduces digit-for-digit, point estimate AND half-width, on all
four published rows.** The estimator is recovered as well and is worth recording
because the study does not state it: the rate is the **mean of per-game removal
shares** (not the pooled turret-level share, which reads 80.7% for the top row),
and the half-width is `1.96 · sd(per-game shares)/√n_games · √1.833`.

### 1.2 KNOWN CELL B — gunner rotations per game (validates the FACING decode)

The stimulus below needs turret **facing**, which the base study never used.
`REPLAY-STUDY:93-95` (opened): *"gunner **rotations quadrupled** (2.0 → 8.1 a game…)"*.
`scratchpad/s54_116_validate.py` counts BC direction-changing `placeEntity`
re-emits:

```
v47 gunner 2.01/game (1,235 games, 2,486 events)   study 2.0
v68 gunner 8.11/game (   90 games,   730 events)   study 8.1
v47/v68 sentinel 0.00/game  (0 events, both eras)
```

The sentinel row is a free engine-consistency check: `rotate()` is
gunner-only (CLAUDE.md Controller API), and the decode returns exactly zero
sentinel rotations across 1,325 games.

### 1.3 KNOWN CELL C — shots per game (validates the FIRE decode)

`REPLAY-STUDY:93-94` (opened): *"gunner shots went from 38 to 68 a game"*;
`REPLAY-STUDY:780-781` (opened): *"5.4 builder attacks on enemy turrets/game against
75 shots/game"*. Decoding `FireTurret`
(field 12, `tools/replay_schema.md:94`, opened) with the shooter resolved by
tile occupancy (`scratchpad/s54_116_validate2.py`):

```
v47  BC gunner 38.5/game   sentinel 36.6   TOTAL 75.2/game     study: 38 gunner, 75 total
v68  BC gunner 68.2/game   sentinel 36.7   TOTAL 104.8/game    study: 68 gunner
unattributed shooters: 0 (every FireTurret event in both eras resolved to a live turret)
```

### 1.4 DRIVEN PLACEBO 1 — mirror-facing (does the facing decode discriminate?)

Same code path, facing flipped 180°: count BC belt tiles that die **on the
turret's real ray** vs **on the same-length ray pointing the other way**. A blind
decode must return equal counts.

```
v47  real facing 7,272 belt deaths   mirror facing    66    ratio 110.2x
v68  real facing   100 belt deaths   mirror facing     2    ratio  50.0x
```

### 1.5 DRIVEN PLACEBO 2 — friendly-fire targets (does target attribution hold?)

Shots whose resolved target tile holds one of the **shooter's own** entities.
No bot in this pool shoots its own buildings, so this is the attribution error
floor: **BC 633 of 92,872 v47 shots = 0.68%**, OPP 410. **Reported as the
instrument's residual, not as a finding.**

### 1.6 INSTRUMENT CORRECTION MADE MID-CUT

`tools/replay_schema.md:217-228` (opened) records the **FireTurret ordering
trap**: fire events can be emitted *after* the victim's `removeEntity` in the
same round, so resolving a target at event time mis-attributes. The first
version of this probe did exactly that. Rebuilt with **round-start occupancy**
and both versions kept:

| | shots at opp turrets | turrets ever shot at (v47) |
|---|---|---|
| event-time resolution | 17,720 | 4,424 (56.7%) |
| **round-start (used below)** | **17,056** | **4,419 (56.6%)** |

**Sensitivity: 0.1pp.** The trap does not bind on this cut — but the round-start
figures are the ones quoted.

### 1.7 POPULATION-LEVEL INSTRUMENT FINDING — 17.3% of the v47 games are DUPLICATES

Fingerprinting each game by its full opponent-turret event sequence plus game
length: **v47 1,199 games → 992 distinct fingerprints (207 duplicates, 17.3%);
v68 85 → 76 (10.6%).** Deterministic bots replayed on the same map in repeated
unrated challenges produce byte-identical games (worst group: one
Part-timers v66 vs BC v47 game present **six** times). Recomputed on distinct
fingerprints only:

| cell | all files | deduped |
|---|---|---|
| castle (fwd), v47 | 79.7% ± 2.2 (1,131 g) | **79.7% ± 2.5 (929 g)** |
| belt-gun, v47 | 75.9% ± 3.1 (837 g) | **75.6% ± 3.5 (693 g)** |

**Point estimates move ≤0.3pp; intervals widen ~13%.** Nothing here changes, but
**this is pseudo-replication that applies to the base study's cells as well** and
should be carried by anything that promotes one to a bar.

---

## §2 THE TWO PREMISES THE BRIEF FLAGGED

**Q3d — the row's framing of §8 caveat 6. VERIFIED.** `PLAYBOOK:1901-1908`
(opened, inside the §8 block at :1859-1935) reads: *"THE BIGGEST UNMEASURED CELL IN THE BOOK: 'do they answer a gun
on their own belt?' [V47 §9 C9] flags it explicitly — n = 2 watched games — and
the v68 part does not measure it either. T24 and §5 item 5 are built on two v47
games plus one v68-era analogue (D game 1)."* The queue row's "n=2 + one v68-era
analogue" is a faithful restatement. `PLAYBOOK:1373-1377` repeats it as *"the
single highest-value unclosed measurement in the book"*.

**Q3c — the row's GREP cell, *"instrument exists — the parts' own BUILD/DEATH +
position join (`scratchpad/s53_beanwatch*` probes) computes exactly this; no new
decoder"*. ⛔ REFUTED. This is a first-class finding of the cut.** Opened every
s53 probe:
* `s53_bean_verbs.py` — per-game **counts** of builder attacks/heals by target
  ownership. No positions retained, no turret, no range.
* `s53_bean_census.py` / `s53_bean_lib.py` — per-game census rows and the
  file→side→version loader. No stimulus join.
* `s53_beanwatch47_census3.py:36` — the only distance banding anywhere in the
  probe set, and it bands a turret by **d² to the enemy core**, not to a belt tile.
* `s53_beanwatch47_watch.py` — the only file in the set that mentions conveyors,
  and it is a **human-readable single-replay narrative renderer**, not a
  population instrument.
* No probe in the set decodes turret **facing**, `FireTurret` **targets**, or any
  belt-tile↔turret-range join.

**Consequence, and it is why this cut cost four new probes rather than a query:
the row's "no new decoder" costing was wrong, and a leg planned on it would have
started from an instrument that does not exist.** Same class as the CLAUDE.md
LOKI-14 lesson (a leg planned on reading its own stdout out of a platform
replay). **Written down here so the next GREP cell that claims an instrument
exists is expected to name the file AND the join.**

---

## §3 STIMULUS DEFINITION

**Belt tile** — a tile holding a **live** BC `conveyor` or `splitter`. Lifetimes
by **entity id** (`placeEntity` → `removeEntity`), which is stricter than the
base study's positional pairing and removes the rebuild blur of its caveat 8.

**Belt gun (the stimulus)** — an OPPONENT `gunner`/`sentinel` whose **actual
firing line** covers a live belt tile at any round of its life:
* **gunner** (r² ≤ 13): walk the facing ray outward, stop at the first wall or
  occupied tile — that tile is what `get_gunner_target()` returns. The stimulus
  holds iff that stopping tile is a BC belt tile. Facing is tracked through
  `rotate()` re-emissions (validated §1.2).
* **sentinel** (r² ≤ 32): any belt tile on the facing ray — the sentinel line
  ignores obstacles (CLAUDE.md entity table) and sentinels cannot rotate, so
  facing is fixed at build.

**Belt cutter** — a belt gun on whose **line** a BC belt tile actually died.
**INFERENCE-free**: it is the co-occurrence of a belt death with that line, not
an attribution of the kill.

**Answer** — three separate verbs, measured independently, never merged into one
number without saying so:
* **SHOT AT** — ≥1 BC `FireTurret` resolving onto the turret's tile.
* **BUILDER-ATTACKED** — ≥1 BC `BuilderAttack` (field 13) onto its tile.
* **REMOVED** — the turret's `removeEntity`. **This is the base study's response
  variable and §5.1 shows it is the weakest of the three.**

**Latency** — rounds from stimulus onset (first round the line covers a live belt
tile; for the cutter cell, the first belt death on the line) to the verb.

**Disc vs line, and why the line was necessary.** A disc-only stimulus
(`d² ≤ range`, no facing — `scratchpad/s54_116_belt.py`) puts **5,569 of the
5,803** forward turrets in the stimulus group: **96% overlap with the castle
cell, i.e. no discriminating power at all.** That version is retained in the
scratchpad and is *not* the instrument used here.

---

## §4 MAIN TABLE — answer rate and latency, split v47 / v68

Rate = mean of per-game shares (the base study's estimator, §1.1); half-width
`1.96·sd/√n_games·√1.833`, DEFF 1.833 (unrated-dominated pool, CLAUDE.md).
**Population:** BC's archived FIELD games — **v47 1,199 games with ≥1 opponent
turret, 1,082 unrated / 117 ladder; v68 85 games, 70 unrated / 15 ladder**
(`triggeredBy`, `scratchpad/s53_bean_meta_join.frozen.tsv`). **Internal ratios
only** — every cell is BC against the same opponents in the same games.

### v47 (1,199 games, 7,809 opponent turret-lives)

| cell | n turrets | games | **REMOVED** | **SHOT AT** | BUILDER-ATTACKED | ANSWERED (shot or attacked) | med. latency to first shot | med. latency to removal |
|---|---|---|---|---|---|---|---|---|
| **BELT-GUN** (line covers live belt) | 3,034 | 837 | **75.9% ± 3.1** | **58.8% ± 3.5** | 16.2% ± 2.7 | 64.3% ± 3.4 | **6 rnd** | **11 rnd** |
| ↳ **BELT-CUTTER** (belt died on its line) | 2,012 | 577 | 75.3% ± 3.9 | **46.2% ± 4.2** | 12.6% ± 2.9 | 52.3% ± 4.2 | 5 rnd | 9 rnd |
| **CASTLE** (fwd turret in BC half) — base cell | 5,803 | 1,131 | **79.7% ± 2.2** | 66.2% ± 2.7 | 18.6% ± 2.1 | 71.0% ± 2.5 | 4 rnd | 10 rnd |
| **PLACEBO** (no BC belt ever in its disc) | 1,617 | 576 | 73.1% ± 4.3 | **44.0% ± 4.5** | 7.5% ± 2.6 | **46.8% ± 4.6** | 4 rnd | 9 rnd |

### v68 (85 games, 264 opponent turret-lives) — **thin, read the intervals**

| cell | n turrets | games | REMOVED | SHOT AT | BUILDER-ATTACKED | ANSWERED | med. shot latency | med. removal latency |
|---|---|---|---|---|---|---|---|---|
| **BELT-GUN** | 55 | 36 | **74.3% ± 18.2** | 69.4% ± 19.3 | 11.8% ± 13.1 | 69.4% ± 19.3 | **11 rnd** | **16 rnd** |
| ↳ BELT-CUTTER | 33 | 22 | 69.3% ± 24.7 | 61.4% ± 26.1 | 15.9% ± 20.3 | 61.4% ± 26.1 | 11 rnd | 24.5 rnd |
| CASTLE — base cell | 117 | 61 | 76.6% ± 11.1 | 67.6% ± 13.9 | 5.2% ± 4.8 | 67.6% ± 13.9 | 7.5 rnd | 15 rnd |
| PLACEBO | 116 | 52 | 72.3% ± 14.7 | 43.9% ± 14.3 | 4.2% ± 4.1 | 47.0% ± 14.9 | 3 rnd | 12 rnd |

**THE PLACEBO IS THE LOAD-BEARING ROW AND IT DOES TWO JOBS.**
1. It **drives the response variable the other way** on the active verbs —
   46.8% ± 4.6 answered vs the castle's 71.0% ± 2.5 — so shot/attack rates are
   measuring something and not a constant.
2. It **exposes REMOVED as a near-constant column: 73.1% ± 4.3 for turrets BC's
   belt is nowhere near, against 79.7% ± 2.2 for the castle cell.** Roughly
   three-quarters of every enemy turret in a BC game dies wherever it stands.
   ⚠ **Read `REMOVED` accordingly — including in the base study's 79.7%, whose
   discriminating power against its own placebo is ~6.6pp, not 46pp.** (The
   46pp gap in the base study is BC vs *their opponents*, a different and valid
   contrast; this is a different control on the same column.) An end-of-game
   artefact was excluded: only **0.9%** of turret deaths land on the final round.

---

## §5 WHERE THE DEFICIT ACTUALLY IS — stratified, and immortal-time-safe

### 5.1 Within BC's own half, splitting only on what the turret is aimed at (v47)

The belt-gun deficit survives the position control, on the **active** verbs only:

| within the castle cell (fwd, BC's half) | n | games | SHOT AT | ANSWERED | REMOVED | median shots taken |
|---|---|---|---|---|---|---|
| **cuts the belt** | 1,818 | 553 | **47.5% ± 4.4** | 52.2% ± 4.3 | 77.1% ± 3.9 | **0** |
| aims at belt, no cut yet | 963 | 539 | 69.9% ± 4.8 | 73.1% ± 4.6 | 75.8% ± 4.4 | 3 |
| belt not on its line | 3,022 | 945 | **67.8% ± 3.3** | 72.7% ± 3.1 | 80.0% ± 2.8 | 3 |

**A gun that is eating Bean counters' belt takes a median of ZERO shots from
them, and more than half are never shot at once — while a turret standing in the
same half aimed at something else is shot at 67.8% of the time.** The
20.3pp gap has non-overlapping intervals.

### 5.2 …and half of that gap is REACH, not choice

Re-running the same split on the turrets BC could actually reach (≥1 round inside
a live BC turret's disc):

| conditioned on BC having reach | n | SHOT AT | ANSWERED | REMOVED |
|---|---|---|---|---|
| cuts the belt | 1,039 | **73.6% ± 4.3** | 77.2% ± 4.1 | 81.8% ± 4.1 |
| aims at belt, no cut | 776 | 87.0% ± 3.8 | 88.6% ± 3.6 | 82.7% ± 4.3 |
| belt not on its line | 2,441 | **84.6% ± 2.7** | 88.0% ± 2.4 | 87.4% ± 2.5 |

The gap falls from 20.3pp to 11.0pp. The rest is exposure: **only 1,039 of 1,818
belt-cutters (57%) ever enter a BC turret's reach, against 2,441 of 3,022 (81%)
for non-belt turrets. 41.3% of all v47 belt-cutters are never inside any live BC
turret's disc for a single round.**

### 5.3 Reach → aim conversion: no belt-specific blindness

| v47, turrets BC had in reach | n | ever AIMED at | ever SHOT | median reach→aim latency |
|---|---|---|---|---|
| belt-cutter | 1,181 | 71.6% ± 4.3 | 69.5% ± 4.4 | **0 rnd** |
| not a belt-cutter | 4,904 | 74.0% ± 2.5 | 72.2% ± 2.6 | **0 rnd** |

**INFERENCE, and it is the mechanism sentence of this cut: Bean counters do not
fail to *recognise* a belt gun — they fail to *cover* one.** When a home gun can
reach it, they swing onto it in the same round and at the same rate as onto any
other target. The residual 11pp inside the reach stratum is unexplained here.
⚠ **This is an inference from co-occurrence; no internal state is readable
(`print()` is stripped from platform replays, CLAUDE.md s28).**

### 5.4 Per-round removal hazard, conditioned on age (kills the immortal-time bias)

A turret must survive to eat the belt, so any "eaters live longer" comparison is
biased by construction. Hazard per turret-round at risk, by state and by rounds
since build (`scratchpad/s54_116_hazard_age.tsv`), v47:

| age | no belt near | belt in disc, aimed elsewhere | **aimed at belt** | **has cut belt** |
|---|---|---|---|---|
| 0–9 | 4.25% (15,523 rnd) | 5.93% (30,663) | **2.30% (13,450)** | 3.28% (8,099) |
| 10–24 | 3.24% (11,117) | 6.16% (13,180) | **3.44% (5,696)** | 5.90% (14,952) |
| 25–49 | 0.85% (11,566) | 1.51% (7,811) | 1.28% (2,803) | 2.01% (13,558) |
| 50–99 | 0.70% (13,625) | 0.69% (6,521) | 0.41% (1,974) | 0.59% (16,778) |
| 100+ | 0.14% (37,752) | 0.24% (9,781) | 0.32% (2,156) | 0.17% (45,963) |

**In every age bucket a turret aimed at the belt dies no faster than one that is
not, and consistently slower than one standing near the belt aimed elsewhere**
(the latter is presumably in a firefight — **INFERENCE**). The removal loop is
generic and age-driven, not belt-triggered.

---

## §6 THE TAIL — where the playbook's two watched games live

The mean says "answered". The distribution says the counter is still real, in a
minority of games (v47):

| belt-cutters, v47 (n=2,012 in 577 games) | count | share | games |
|---|---|---|---|
| survives ≥25 rnd after its first belt kill | 624 / 1,902 at risk | 32.8% | 360 (30.0% of games) |
| survives ≥50 rnd | 405 / 1,747 | 23.2% | 238 (19.8%) |
| **survives ≥100 rnd** | **233 / 1,371** | **17.0%** | **124 (10.3% of games)** |
| survives ≥200 rnd | 121 / 680 | 17.8% | 59 (4.9%) |
| **never removed at all** | **413** | **20.5%** | median **77 rounds** alive after first belt kill |

v68 (thin): ≥100 rnd survival **45.5% (10/22 at risk), 6 games = 7.1%**; never
removed **33.3% (11/33)**, median 112 rounds.

**The never-removed group is under-covered, not un-noticed.** 52.5% of them sat
inside a live BC turret's disc for a **median 45 rounds**, but only **16.5%** were
ever on a BC turret's firing line. ⚠ **Do not read that pair as "they had the
shot and refused it": BC turret fire is the main killer, so "survived" and
"never aimed at" are partly the same event.** The unconfounded version is §5.3,
where the conversion rate is flat.

**The named case reproduces.** `PLAYBOOK` T24 (`:1030-1075`, opened) describes a
Pivot gunner sitting on BC's delivery face inside their own gunner's reach, never
shot. Population scan of BC-vs-Pivot games in the frozen set finds the shape
repeatedly — e.g. `113d7a69… game 1`: a Pivot gunner at (7,4) built r57,
**45 BC belt tiles killed on its line**, **214 rounds inside a live BC turret's
disc**, **aimed at for 5 of them, 3 shots taken total**, removed at r274.

**Economic co-occurrence — CORRELATIONAL, and length-confounded, so normalised.**
BC's own `titanium_collected` per round (`ti_collected` from the frozen census,
divided by game length):

| v47 | games | BC Ti collected / round, median [IQR] |
|---|---|---|
| no belt-cutter in the game | 622 (51.9%) | **9.09** [6.70, 12.46] |
| belt-cutter, <100 rounds | 453 (37.8%) | 6.58 [3.59, 10.39] |
| belt-cutter surviving ≥100 rounds | 124 (10.3%) | **6.35** [3.37, 10.65] |

v68: 10.00 / 8.91 / 7.28 (n = 63 / 16 / 6). **A ~30% throughput reduction
co-occurs with a long-lived belt cutter. This is NOT causal** — a game containing
a long-lived enemy gun is a game where the opponent is doing well generally, and
the IQRs overlap heavily. **Off-currency for us in any case (`R1000_IS_DEFEAT`,
CLAUDE.md caveat 14 of the playbook): economy denial scores nothing by itself and
is admissible only as "opens the lane".**

---

## §7 CASTLE vs SUPPLY LINE — the contrast the row asked for

Stated as a comparison of **their** cells, same fixture, same games, same
instrument, v47:

| what BC defends | REMOVED | SHOT AT | median latency to removal |
|---|---|---|---|
| the castle (forward turret in their half) | **79.7% ± 2.2** | 66.2% ± 2.7 | 10 rnd |
| the supply line (gun aimed at their belt) | **75.9% ± 3.1** | 58.8% ± 3.5 | 11 rnd |
| the supply line, gun **actually cutting** it | 75.3% ± 3.9 | **46.2% ± 4.2** | 9 rnd |
| *(nothing of theirs is threatened — placebo)* | 73.1% ± 4.3 | 44.0% ± 4.5 | 9 rnd |

**The finding is not "castle, not supply line". It is: THEY DEFEND WHAT THEIR
HOME GUNS COVER, and the belt runs outside that cover.** On the removal column
the castle and supply-line cells are statistically indistinguishable. On the
active-fire column the belt-*cutter* cell falls to placebo level
(46.2% ± 4.2 vs 44.0% ± 4.5) — **but §5.2 shows that is 57%-reach, not
57%-attention**, and §5.3 shows conversion is flat once reach exists.

**What this does to the playbook's Pivot-collapse counter (T24 / §6 COPY 4):**
the mechanism survives, the pricing does not. **Planting one gun on their belt
buys a median of 11 rounds before removal in ~76% of cases; the 128-round freeze
of the watched game is the ~10-20% tail, and it requires siting the gun OUTSIDE
their home-gun disc, which is what the watched games happened to do.**
⇒ **The counter's live-leg form should pre-register the SITING constraint (belt
tile in our reach, gun outside every live BC turret's r²), not the bare "gun on
their belt".** *(Stated as an implication for whoever writes that prereg. No ship
verdict is made here — this cut recommends nothing.)*

---

## §8 LIMITS — what this stimulus definition cannot see

1. **Removal is not attributed.** A `removeEntity` on an enemy turret could be
   BC's fire, BC's builder melee, the owner's own `destroy()`, or a
   `self_destruct`. The SHOT AT / BUILDER-ATTACKED columns *are* attributed
   (0.68% friendly-fire residual, §1.5); **REMOVED is not, and that is the
   column the base study uses.**
2. **Turrets that die before they can matter are in the denominator.** A gun
   killed on the round it is built counts as "answered" and never tested the
   belt loop. The hazard table (§5.4) is the age-corrected view; the headline
   rates are not.
3. **Facing is decoded, blocking is only decoded for gunners.** Sentinel lines
   ignore obstacles by rule, so their stimulus is exact; gunner rays stop at the
   first occupant, which is the engine's `get_gunner_target` semantics but is
   evaluated at end-of-round occupancy, not at the instant of firing.
4. **"Belt" = conveyor + splitter, not "belt that reaches the core".** A gun on a
   disconnected stub counts as a belt gun. Directed connectivity was not
   recomputed here (`replay_census`'s `chain_dir` could do it — a follow-on).
5. **Ammunition is not modelled.** A BC turret that does not fire may be out of
   ammo rather than un-aimed; ammo balance lives in `updatePlayers` and is not in
   this decode. **This is the single most plausible alternative explanation for
   the residual 11pp in §5.2 and it is untested.**
6. **Population is BC's FIELD, ~90% unrated** (v47 1,082/1,199 unrated; v68
   70/85). Unrated pools prototypes on the challenger side, so every cell is
   BC against a prototype-heavy field. **Internal ratios only; no cross-fixture
   comparison to our numbers is made anywhere above.**
7. **Clustering.** DEFF 1.833 is applied to every interval. On top of that,
   **17.3% of the v47 games are exact duplicates** (§1.7) — pseudo-replication
   the DEFF does not cover. Deduped estimates move ≤0.3pp; intervals widen ~13%.
   **Any cell promoted to a bar should be restated deduped.**
8. **No internal state is readable** — `print()` is stripped from platform
   replays. Every trigger sentence here is an **INFERENCE** from engine-side
   position/round/event order and is labelled where it appears.
9. **v68 is thin and under a day old at study time**: 264 turret-lives in 85
   games; the belt-gun cell is n=55 in 36 games with a ±18pp half-width. **It
   cannot separate 74.3% from 79.7%, and no v68 claim above should be quoted
   without its interval.**

---

## §9 REPRODUCTION

All probes are read-only, in `scratchpad/`, run with `.venv/bin/python`:

| file | what it does |
|---|---|
| `s54_116_extract.py` | filters `corpus/events.tsv` (14.95M rows) to the frozen BC set → `s54_116_bc_events.tsv` (229,060 rows, 1,385/1,385 files present) |
| `s54_116_repro.py` | **§1.1 known-cell reproduction** + the recovered estimator |
| `s54_116_facing.py` | the main probe: facing-tracked turret lives, belt lifetimes by entity id, `FireTurret`/`BuilderAttack` attribution, per-round state → `s54_116_facing.tsv` (8,073 rows), `s54_116_hazard_age.tsv` |
| `s54_116_validate.py` | **§1.2 / §1.4** — rotation known cell + mirror-facing placebo |
| `s54_116_validate2.py` | **§1.3 / §1.5** — shots-per-game known cell + friendly-fire control |
| `s54_116_belt.py` | the **rejected** disc-only stimulus (kept: it is the 96%-overlap negative result of §3) |
| `s54_116_final.py`, `s54_116_tail.py`, `s54_116_econ.py`, `s54_116_main.py`, `s54_116_tab.py` | the tables of §4–§7 |

Frozen inputs: `scratchpad/s53_bean_census.jsonl` (file set + `ti_collected`),
`scratchpad/s53_bean_meta_join.frozen.tsv` (version, opponent, `triggeredBy`),
`replay_archive/` (decoded via `tools/replay_census.py`, no hand-rolled decoder).

**⚠ Scratchpad files die with the session.** The four probes above are the ones
worth promoting to `tools/` if #116's answer is ever re-cut — the facing +
`FireTurret` attribution pair is the reusable half, and per §2 nothing
equivalent existed before this cut.
