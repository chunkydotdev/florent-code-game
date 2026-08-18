# FIELD PRIOR — do live teams run TWO OR MORE forward bodies at the enemy core, and what co-occurs?

**Research arm, banked 2026-08-18 03:39Z** (`date -u`). Repo head at write time `08bb2079`.
**Ground: 64,181 archived replays × 2 sides = 128,362 attacking sides, 85 distinct teams**,
decoded fresh by `tools/fwd_bodies_census.py` (new; committed with this report).
Corpus surface: `corpus/meta_join.tsv` + `corpus/events.tsv`, both **copied into a scratchpad
namespace and row-counted twice before use** (keeper daemon rewrites `corpus/*.tsv` in place —
the 62% silent truncation flagged in `FIELD-SIEGE-RESPONSE-2026-08-17.md:3`).
**No platform matches fired, no replays downloaded.**

**THIS IS A PRIOR, NOT A VERDICT.** Nothing below is randomised. Every comparison here is
observational and a team CHOOSES when to send a second body; §6 states exactly which
inferences the design does and does not support.

---

## 0. THE QUESTION AND THE ONE-LINE ANSWER

The builder's `_v513siegecrew` shipped its second forward body **OFF** because the crew-on arm
lost on every column (`docs/research/BUILD-REPORT-v513siegecrew-2026-08-17.md:83-105`), and the
surviving hypothesis was **funding contention**.

**The field answer: two-plus forward bodies is the MAJORITY behaviour among sieging teams
(47.0% of 70,572 siege-sides), 82 of 85 teams do it at least sometimes, and within-team it
associates with a HIGHER kill rate, not a lower one (+6.7pp, 95% CI [+5.4, +8.0], DEFF-corrected;
43 of 60 teams positive, sign-test p = 1.5e-4).** The one cell where the field shows **no**
second-body advantage is exactly the economy the crew-on arm was living in: **≤1 harvester built
by r100 → −2.6pp ± 4.2 (null).** So the field prior does not refute the builder's measurement —
it **localises** it: the cost is not "a second body", it is "a second body on a starved bank".

---

## 1. VERIFICATION OF THE RELAYED NUMBERS (I opened the report; the relay was close but not exact)

| relayed to me | what `BUILD-REPORT-v513siegecrew-2026-08-17.md` actually says |
|---|---|
| second body −15.6pp | ✅ `:89-90` — ship (crew off) **49/90 = 54.4%**, crew on **35/90 = 38.9%**. Δ = **15.5pp** (the report's own "15.6pp" at `:102`; rounding of 49/90 − 35/90) |
| n=90/arm | ✅ `:87` "n=90/arm, 3 blocks" |
| median titanium collected 380 vs 640 | ⚠ **the report contradicts itself.** Its table `:89-90` reads **565** (ship) vs **380** (crew on); its prose `:101` reads *"median collected 380 with the crew, 640 without"*. **565 ≠ 640.** I cannot tell from the document which population the 640 is over. Flagged for the builder — one of those two numbers is wrong or is a different cut, and the funding argument leans on it. |
| ⚠ not relayed, but load-bearing | `:102-105` the builder himself calls 15.6pp **"a DIRECTION on every column, not a significance claim"** (half-width ≈14.5pp). This prior should be read against a *direction*, not a *result*. |

Also verified as opened: `FIELD-SIEGE-RESPONSE-2026-08-17.md:13` (all 262,346 spawns on the
12-tile ring), `:18` (539,265 hostile-builder visits; 1.2% of raiders ever thrown);
`REPLAY-STUDY-jython-inspiration-2026-08-17.md:72` (*"every later spawn is economy, never a
second raider"*), `:75-77`, `:115` (the **d²≤8 of enemy core** raider table).

---

## 2. EPISODE DEFINITION AND CLASSIFIER

Reused deliberately so the three studies compose:

* **siege zone** = d² ≤ 8 of the **nearest tile of the enemy 2×2 core footprint**. d²≤8 is the
  radius `REPLAY-STUDY-jython-inspiration-2026-08-17.md:115` used for *"raider at d²≤8 of enemy
  core"*.
* **ring** = d² ≤ 2 of the footprint — the 12 tiles that carry every spawn
  (`FIELD-SIEGE-RESPONSE-2026-08-17.md:13`). Reported but not used for the headline.
* **forward body** = a LIVING **builder bot** of the attacking team, inside the zone, **and
  strictly nearer the enemy core than its own**.
* **dweller** = a body accumulating **≥10 rounds** in the zone across the game. Simultaneity is
  counted over dwellers only.
* **SIEGE side** = ≥20 rounds with ≥1 dweller in the zone. **MULTI side** = ≥20 rounds with
  **≥2 dwellers simultaneously**. **SINGLE** = siege but not MULTI. **NONE** = neither.
* Headline population excludes maps where the two core footprints sit closer than **d² = 100**
  (§2.2).

### 2.1 ⛔ THE TWO GUARDS ARE NOT COSMETIC — THE FIRST CUT OF THIS DECODER WAS WRONG

Maps run 8×8 to 30×30. On a 10×10 map the two footprints sit ~5 tiles apart, so a raw
"d²≤8 of the enemy footprint" zone covers a quarter of the board. The **first** version of this
decoder — zone test only, no own-core comparison, no dwell filter — scored a **known one-raider
Jython game at `peak_bodies = 21`**, i.e. more bots than a team can profitably own. The
own-core comparison kills the overlap; the dwell filter kills bots in transit. Both guards are
in `tools/fwd_bodies_census.py` and both are documented there with this failure.

### 2.2 THE SMALL-MAP CELL IS REPORTED SEPARATELY BECAUSE IT IS STILL DEGENERATE

| population | sides | NONE | SINGLE | MULTI |
|---|---|---|---|---|
| all sides | 128,362 | 29.0% | 35.6% | 35.4% |
| **core_sep_d² ≥ 100 (headline)** | **103,744** | **32.0%** | **36.0%** | **32.0%** |
| core_sep_d² < 100 (excluded) | 24,618 | 16.2% | 33.9% | 49.8% |

On the closest maps "at the enemy core" and "at home" are nearly the same place; the excluded
cell reads 49.8% MULTI and should not be pooled into a behavioural claim.

---

## 3. CLASSIFIER VALIDATION — DRIVEN TO BOTH VERDICTS, EIGHT WAYS

**A check that has never produced the other verdict has not been seen to check.** Every guard
below was run against a case that had to come out the other way.

| # | control | result | verdict driven? |
|---|---|---|---|
| 1 | **Replay team index ↔ platform side.** Decoded the in-binary `winner` (field 4) and crossed it with `meta_join.game_winner_side` on 400 random games. | `(0,'a')` 205, `(1,'b')` 195, **off-diagonal 0** | ✅ non-degenerate table, both cells populated |
| 2 | **Core-death detection vs the replay's own outcome fields**, all 128,362 sides. | agree 128,290 (99.94%); **0 false negatives**; 72 detected-but-not-scored (simultaneous/edge) | ✅ both verdicts present |
| 3 | **MUTATION: false anchor.** Same instrument, enemy-core anchor shifted +6,+6, random 3,000-game sample (4,856 big-map sides). | NONE **33.2% → 78.3%**, MULTI **32.3% → 8.3%**, Σfwd2 −73% | ✅ the instrument collapses on a false anchor — it is not measuring map traffic |
| 4 | **Known-zero teams.** | **Albert And Einstein 0.0%** MULTI over 285 sieges; **LingLing40 0.2%/598**; **Pivot 6.9%/2,607** | ✅ the classifier returns zero on real teams |
| 5 | **Known-high team, hand-verified trajectory.** `27eb359a…_game_3`, our own **v125**, 25×25, cores (5,5)/(18,18). | bots **3 (spawn r0), 9 (r3), 17 (r6)** all arrive and hold **(17,19) (17,17) (17,20)** — collar seats — from r40 to game end | ✅ MULTI verdict is a real three-body collar crew, matching our own doctrine |
| 6 | **Hand-verified MULTI on a field team.** Jython `012bc8aa…_game_2` (25×25). | dweller ids/zone-rounds: **4:132 (spawn r0 — the raider), 275:32 (r86), 353:22 (r111), 628:78 (r219), 785:33 (r268)**; ≥2 dwellers on 66 rounds from r135 | ✅ distinct bodies, distinct spawns, sustained overlap |
| 7 | **`--selftest`: the arm logic forced to every verdict on synthetic tapes.** `empty → NONE`, `one dweller → SINGLE`, `two dwellers → MULTI`, `300 one-round tourists → NONE`, `dweller+tourist → SINGLE`, `15-round overlap → SINGLE`. Fails loudly if fewer than 3 distinct verdicts appear. | 6/6 pass; `decode()` and the selftest share one `_dwellers()` helper so they cannot drift (re-run after the refactor: output byte-identical) | ✅ all three verdicts forced |
| 8 | **Soft external check against the Jython study.** That study's 5 games (match `617d4d27…`) are **NOT in this archive** — I could not re-run them. Across the 2,159 Jython siege-sides that ARE here, **median peak = 1** and MULTI = 35.3%. | consistent with *"one raider"* being Jython's modal shape, **not** its only shape | ⚠ partial — see §6 |

⛔ **WHAT CONTROL 8 COSTS US.** `REPLAY-STUDY-jython-inspiration-2026-08-17.md:72` states
*"every later spawn is economy, never a second raider"* over 5 games of one match. **In the
2,159 Jython siege-sides in this archive that is true of the modal game and false of a third of
them** (35.3% MULTI). Both can hold — that study's own `:76-77` notes game 1's second sentinel
was built by *"a later spawn that walked up"*. **The 5-game shape is not the population shape,
and this prior should not be read as contradicting it.**

---

## 4. PREVALENCE — ≥2 FORWARD BODIES IS THE MAJORITY BEHAVIOUR AMONG SIEGERS

Population: **103,744 attacking sides on maps with core_sep_d² ≥ 100, 85 teams, 64,181 archived
games (81,092 unrated + 47,270 ladder sides), all archived replays that carry a `meta_join` row.**

* **68.0% of sides mount a siege at all** (≥20 rounds with a forward dweller): 70,572.
* **47.0% of siege-sides are MULTI** (33,199) — i.e. **32.0% of ALL attacking sides**.
* **40.8% of all sides reach ≥2 simultaneous forward dwellers at some point** (any duration).
* **82 of 85 teams run MULTI at least once.** Of the 80 teams with ≥40 sieges, **32 are ≥50%
  MULTI and 21 are <20%.**

Peak simultaneous forward bodies, big-map siege-sides (n=70,572): **1 → 28,514 · 2 → 25,819 ·
3 → 10,495 · 4 → 3,148 · 5 → 1,308 · 6+ → 1,288.**

**Per-team MULTI share spans the full range — this is a TEAM property, exactly as
`FIELD-SIEGE-RESPONSE-2026-08-17.md:7` found for seal survival.** Selected rows (share of that
team's siege-sides that are MULTI; `sides` = all its big-map attacking sides):

| team | sides | sieges | MULTI% | med peak |
|---|---|---|---|---|
| Prompt Engineers Anonymous | 721 | 640 | **89.4%** | 4 |
| not adgato | 1,403 | 1,247 | 81.3% | 2 |
| Cookie | 418 | 325 | 80.0% | 3 |
| Troupe | 768 | 449 | 78.8% | **9** |
| **OpenSverige (us)** | **9,593** | **8,033** | **78.2%** | **3** |
| gsxWins | 1,336 | 1,043 | 75.6% | 2 |
| ph | 1,631 | 1,558 | 74.1% | 2 |
| O(1) | 1,728 | 1,480 | 68.2% | 2 |
| Lorem Ipsum | 2,311 | 2,229 | 66.7% | 2 |
| 0033 | 3,198 | 2,901 | 53.7% | 2 |
| The Bisons | 1,225 | 632 | 48.6% | 2 |
| Klarum | 1,707 | 1,447 | 47.0% | 2 |
| Powered by SmartFridge | 3,067 | 2,522 | 38.5% | 1 |
| Jython | 2,347 | 2,159 | 35.3% | 1 |
| Erebus | 4,224 | 3,679 | 16.6% | 1 |
| Torsko | 4,698 | 946 | 17.1% | 1 |
| Pivot | 3,155 | 2,607 | 6.9% | 1 |
| LingLing40 | 755 | 598 | 0.2% | 1 |
| Albert And Einstein | 435 | 285 | **0.0%** | 1 |

### 4.1 ⭐ WE ALREADY SHIP A MULTI-BODY CREW — INCLUDING THE LIVE HOLDER

OpenSverige big-map sides completed since 2026-08-16, split by our own submission version:

| our version | sides | sieges | MULTI% | med peak |
|---|---|---|---|---|
| v125 | 460 | 401 | 82.0% | 2 |
| v140 | 190 | 182 | 83.0% | 3 |
| v152 | 305 | 294 | 88.1% | 3 |
| v154 | 173 | 165 | 90.9% | 3 |
| v155 | 367 | 361 | 90.0% | 3 |
| **v159 (holder)** | **238** | **237** | **72.2%** | **2** |

**The incumbent line already parks two to three builder bots at the enemy core in the large
majority of its sieges** — verified by hand at control 5 above (three bots, three collar seats,
held to game end). ⇒ **v513's `FS_CREW_ON` is not "should we ever run a second body"; it is
"does v513's PARTICULAR second body, funded out of v513's PARTICULAR bank, pay".** That is a
narrower question than the flag name suggests, and it is worth the builder grepping the crew
path against what v159 already does before pricing another leg on it.

---

## 5. SINGLE vs MULTI — LANDMARK DESIGN, WITHIN TEAM

### 5.1 The design, and the bias it is built to remove

Naively comparing MULTI to SINGLE is **immortal-time biased**: a longer game gives more chances
to send a second body, and long games kill less often, so the raw comparison is rigged against
MULTI. The cohort therefore fixes a **landmark at r150**:

* siege started by **r100** (both arms are committed sieges),
* game reached **r150** and **both cores still alive at r150** (both arms had the chance),
* **arm assigned by whether a second body was present by r150** — never by anything after.

**Landmark cohort: n = 42,690 sides (SINGLE 19,937 · MULTI 22,753).**

### 5.2 Cluster structure — MEASURED ON THIS CUT, not borrowed

Enumerated per the standing procedure. Clusters this data has: **MATCH** and **OPPONENT**.
A (team, arm) stratum can hold several games from the same match and several matches against the
same opponent, so **both clusters survive**. Measured directly on the landmark cohort with
cluster = (match × attacking team), outcome = core kill:

```
clusters with >=2 games: 12,757   m̄ = 2.89   p = 0.464   ICC = 0.2636   DEFF = 1.499
```

That **independently reproduces the repo's rated pooled constant (1.529)** to within 0.03 on a
different cut, which is a check on the constant as much as on this study. **DEFF = 1.499 is
applied to every interval below.**

### 5.3 Result — MULTI associates with MORE kills and FASTER kills

| arm | n | kill | 95% CI | kill ≤ r300 | 95% CI | median kill round |
|---|---|---|---|---|---|---|
| SINGLE | 19,937 | 42.7% | ±0.8pp | 25.0% | ±0.7pp | 268 |
| MULTI | 22,753 | **49.6%** | ±0.8pp | **31.9%** | ±0.7pp | **248** |

**Within-team (inverse-variance stratified over the 60 teams with ≥25 sides in each arm):**

```
MULTI − SINGLE, kill      : +6.7pp   95% CI [+5.4, +8.0]   (DEFF 1.499)
MULTI − SINGLE, kill<=r300: +7.1pp
sign test: 43 teams positive, 15 negative, 2 tied   one-sided p = 1.5e-4
median per-team delta = +6.1pp
```

Extremes of the per-team table: **gsxWins +24.2pp · Hugging Farce +22.6pp · Memtrace +19.9pp ·
OpenSverige +16.6pp** against **Askar City −24.6pp · TRRR −18.0pp · I Stone −14.4pp · Jacobs
Code −12.7pp · CtrlAltDefeat −9.8pp.** The negative tail is real and it is 15 teams — this is a
central tendency, not a law.

Both fixtures agree in direction (ladder SINGLE 36.4% → MULTI 42.0%; unrated 45.5% → 53.7%);
the **level** difference between fixtures is the documented prototype-vs-shipped pooling
artefact and is not interpreted.

### 5.4 Dose — the return turns over above three bodies

| peak simultaneous forward bodies | n | kill | kill ≤ r300 | median kill round |
|---|---|---|---|---|
| 1 | 15,403 | 39.4% | 27.5% | **234** |
| 2 | 15,952 | 47.5% | 30.4% | 249 |
| 3 | 6,926 | **55.5%** | **32.0%** | 268 |
| 4 | 2,390 | 56.1% | 27.4% | 307 |
| 5+ | 2,019 | 47.5% | **14.2%** | 419 |

**On the PROGRAMME's currency (`kill ≤ r300`) the optimum is 2–3 bodies and 5+ is a disaster
(14.2%).** Note the collider in the last column: peak=1 has the *fastest* median kill because a
siege that kills at r120 never had time to grow a crew. Read the ≤r300 column, not the median.

---

## 6. ECONOMY — THE FUNDING-CONTENTION READ

### 6.1 Pooled economy looks worse for MULTI; within-team it does not

| arm | n | med harvesters by r100 | med conveyors by r100 | med builders by r100 | med ti_collected (end) | med rounds | med ti_collected / 100 rounds |
|---|---|---|---|---|---|---|---|
| SINGLE | 19,571 | 5 | 25 | 5 | 1,950 | 313 | 641 |
| MULTI | 22,043 | 4 | 24 | 5 | 1,620 | **280** | 589 |

The raw `ti_collected` gap (**1,950 → 1,620, −17%**) has the **same sign as the builder's
565 → 380** — but **MULTI games are 33 rounds shorter** because they kill sooner, and
`ti_collected` is cumulative to game end. Controlling for team doctrine:

```
STRATIFIED within-team delta, harvesters built by r100 (MULTI − SINGLE): −0.04
STRATIFIED within-team delta, ti_collected per 100 rounds (MULTI − SINGLE): +4.9
```

⇒ **In the field, a team that sends a second body does NOT visibly cut its own harvester
programme to pay for it.** Whatever v513's crew was displacing, the field's multi-body teams are
not displacing early harvesters.

### 6.2 ⭐ THE ONE CELL THAT MATCHES THE BUILDER'S HYPOTHESIS

Split by **harvesters built by round 100** — a *decision* taken before the outcome is known,
which is why this is the honest economy instrument and `ti_collected_end` is not:

| harvesters by r100 | n SINGLE | kill SINGLE | n MULTI | kill MULTI | **MULTI − SINGLE** | ±95% (DEFF) | Δ kill≤r300 |
|---|---|---|---|---|---|---|---|
| **0–1** | 1,298 | 28.6% | 1,247 | 26.0% | **−2.6pp** | ±4.2pp | −1.0pp |
| 2–3 | 5,426 | 37.0% | 6,629 | 45.9% | **+8.9pp** | ±2.2pp | +7.6pp |
| 4–5 | 5,429 | 44.8% | 7,113 | 51.9% | **+7.1pp** | ±2.2pp | +7.1pp |
| 6+ | 7,418 | 49.5% | 7,054 | 58.5% | **+9.0pp** | ±2.0pp | +9.9pp |

**The second body's advantage is monotone-ish in economy and is EXTINGUISHED — sign flipped,
interval straddling zero — at ≤1 harvester by r100.** Median end-of-game `ti_collected` in that
0–1 band is **220–240**; in the 2–3 band it is ~1,010.

**Where does `_v513siegecrew`'s crew-on arm sit?** Its median collected was **380**
(`BUILD-REPORT…:90`) — i.e. **in or barely above the field's starved band, the one band where
the field ALSO shows no second-body benefit.** Its crew-off arm at 565 sits in the same
neighbourhood. **Both arms of that leg were poor by field standards** (field landmark median
1,620–1,950), which is a statement about the leg's fixture and bot, not about second bodies.

⛔ **AND THE STRAIGHT-BANK SPLIT DOES NOT SHOW WHAT IT LOOKS LIKE IT SHOWS.** Splitting MULTI
sides at the median of `ti_collected` per round gives lo-econ 26.5% kill vs hi-econ 72.7% — but
**the SINGLE arm splits the same way (22.0% vs 63.4%)**. Economy dominates the outcome in *both*
arms. That split therefore says "economy wins games", which we knew; it is **not** evidence that
the second body's *cost* is what sinks it. The early-harvester table above is the cut that can
speak to cost, because its splitter is a decision rather than an outcome.

### 6.3 Forward spend that actually accompanies a second body

| arm | mean fwd barriers | mean fwd turrets | mean fwd launchers | mean total forward builds | mean builder bots built (whole game) |
|---|---|---|---|---|---|
| SINGLE | 2.65 | 2.16 | 0.17 | 5.54 | 9.38 |
| MULTI | **4.67** | 2.48 | 0.09 | **7.98** | **8.80** |

The second body buys **~2 extra forward barriers and ~0.3 extra forward turrets** — and the
MULTI arm builds **fewer** builder bots over the game, not more. The marginal bill the field
pays for a crew is **~2 barriers**, not a fourth builder plus a launcher.

### 6.4 When the second body arrives

Big-map MULTI sides (n=33,199): `first_fwd2_rnd` quartiles **33 / 52 / 106**; `first_fwd_rnd`
quartiles **22 / 32 / 51**; **median gap first body → second body = 12 rounds**; **48.9% have the
second body in place by r50.** So the field's crew is roughly half opening-crew and half
reinforcement — it is **not** predominantly a late top-up.

---

## 7. WHAT THIS DOES AND DOES NOT SAY ABOUT THE −15.6pp

**IT SAYS:**
1. **The plank is not exotic.** ≥2 simultaneous forward bodies is what **47.0% of 70,572 siege
   sides** and **82 of 85 teams** do. A prior that "a second body is bad" is not the field's.
2. **Within team, the association runs the other way** — +6.7pp kill [+5.4, +8.0], +7.1pp on
   ≤r300, 43/60 teams positive, p = 1.5e-4, on a landmark design that removes immortal-time bias
   and with a DEFF measured on the cut itself.
3. **There is one cell where the field agrees with the builder, and v513's crew arm was in it:**
   ≤1 harvester by r100 → −2.6pp ± 4.2. **Funding contention is a real boundary; it just binds
   far lower than v513's crew was operating above.**
4. **We already do this.** v159 — the live holder — runs MULTI in **72.2% of 237 siege-sides**,
   median peak 2, and a hand-verified v125 game shows three bots on three collar seats. **The
   novel thing in `FS_CREW_ON` is v513's particular crew, not crews.**
5. **Dose matters and the programme's currency turns over:** on `kill ≤ r300` the field optimum
   is 2–3 bodies (30.4% / 32.0%), and 5+ collapses to 14.2%.

**IT DOES NOT SAY:**
1. **That a second body CAUSES more kills.** Nothing here is randomised. **INFERENCE: teams
   choose to send a second body, plausibly when the first one is surviving and the bank is
   healthy — so the MULTI arm is selected for "the siege is going well" in a way the landmark
   cannot fully remove.** The landmark removes *"longer games accumulate more bodies"*; it does
   **not** remove *"a winning siege attracts reinforcement"*. **The builder's local ablation is
   randomised and this is not — on causal identification his leg beats this study, and where
   they disagree the honest reading is that they are measuring different things (his: the causal
   effect of v513's crew; this: the field's selection of when a crew is worth sending).**
2. **That v513's crew implementation is fine.** A −15.5pp direction on a randomised 90/arm
   fixture is evidence about **that code**. This prior only removes the *class-level* reason to
   abandon it.
3. **Anything about which specific mechanism pays.** This decoder sees positions and builds. It
   does not see intent, targets, or the bot's own state — and per the s28 correction, `print()`
   is stripped from platform replays, so arm tags are not recoverable here either.
4. **Anything about opponent version.** `oppver` is not stratified in this cut. A team's MULTI
   share is pooled across every version it ever shipped, so a per-team row is a **team-era
   average**, not a description of its current bot.
5. **Anything about our own unrated prototype legs vs shipped bots.** The pool is
   **81,092 unrated + 47,270 ladder sides**; unrated pools prototypes and ladder pools shipped
   bots. The **fixture split in §5.3 shows the same direction in both**, which is why the
   headline is stated at all — but the *levels* must not be compared across the two.

---

## 8. LIMITS IN FORCE

* **Archive is not a random sample of the field** — it is dominated by games we played or
  archived; per-team coverage runs 43 to 9,593 sides. Every per-team row carries its n.
* Small maps (core_sep_d² < 100, 24,618 sides, 19.2%) are **excluded from every headline** and
  are degenerate for this measurement (§2.2).
* A body **kidnapped by an enemy launcher** into the enemy zone counts as a forward body. The
  field's eviction reflex is ~1.2% of raiders (`FIELD-SIEGE-RESPONSE-2026-08-17.md:18`), so this
  is a small contamination, but it is not zero and it is not separated here.
* `ti_collected_end` is **cumulative to game end** and therefore confounded with game length;
  §6.1 reports the rate form and §6.2 uses an early-decision splitter instead. Any reader
  quoting the raw medians must carry the length caveat.
* The Jython 5-game fixture that motivated the plank is **not in this archive**; control 8 is a
  population-shape consistency check, not a replication.
* **Fail-to-exclude claims restated as exclusions before DEFF was applied**, per the standing
  direction rule: the 0–1 harvester cell is reported as *"the CI [−6.8, +1.6] does not exclude
  zero and does not exclude a −5pp harm"*, not as *"no effect"*.
* DEFF 1.499 measured on the landmark cohort at cluster = (match × team). A per-team row in §4
  is a raw prevalence share and carries **no** interval.

## 9. REPRODUCING

```bash
.venv/bin/python tools/fwd_bodies_census.py <file-list> -o fwd_all.tsv --jobs 10
.venv/bin/python tools/fwd_bodies_census.py <file-list> -o mut.tsv --anchor-shift 6,6   # mutation control
```
Inputs: `corpus/meta_join.tsv` (side↔team names; **replay team 0 = platform side a**, control 1),
`corpus/events.tsv` (harvesters/conveyors built by r100). Analysis scripts were
scratchpad-only; every number above is regenerable from the two commands and those two columns.
