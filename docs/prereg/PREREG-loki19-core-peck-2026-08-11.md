# PREREG — LOKI-19: THE CORE PECK, RE-MEASURED UNDER A CHANGED PREMISE

**Written 2026-08-11 06:3x CEST by the s29 BUILDER (`date`, same shell call).
Committed BEFORE leg creation — two-clock standard, git author time vs platform
`createdAt`.** The bot tree `bots/_v136loki19` (py-tree md5 `fb5cba8c`) exists
already and is committed; **no bar in this document was written after any live
measurement of it, and the only measurement taken so far is the LOCAL dose check
recorded in §4, which is explicitly not a result.**

```
TARGET BAND: gaps -39..+88, a 5-0 pays 14.21..19.98, reachable 4/4
```
*(verbatim from `tools/target_value.py`, run before this document was written;
cells: Lunds Stallions −39, Askar City −8, Powered by SmartFridge +6,
farming_200s +88)*

---

## 1. THIS IS NOT A BUG FIX AND NOT A REVERT. IT IS A RE-MEASUREMENT.

`LOKI_QUIET_ON = True` silences all builder melee. It has been in every shipped
tree since `_v123loki7`. **Its adoption was evidenced and its reasoning was
sound**, quoted verbatim from `bots/_v130loki13/doctrine.py`:

> *"Acting and moving are MUTUALLY EXCLUSIVE for a builder bot. Every peck,
> siphon hit and counterbattery swing therefore costs that raider its move for
> the round — **and the ladder says ARRIVAL is the scarce quantity, not
> damage.** … it went 3-2 against CAD landing ZERO builder attacks, so the melee
> was never load-bearing."*

**THE PREMISE IS THE PLANK. ARRIVAL IS NO LONGER SCARCE.**

```
ARRIVAL BASELINE: 38.1% reach, kind=INSERT, ours, RATED corpus, n=475
```
**⛔ THAT TAG IS LOAD-BEARING AND MUST TRAVEL WITH THE NUMBER.** The same
quantity reads **39.5% rated-only** for v104 but **23.3% pooled with unrated**
(n=1,493), and spans **18.2%–40.9%** across v102–v107 on all games. **A read-out
that computes reach on any other population will not get 38.1% and will be
testing against the wrong number.** This is the sixth units-not-data incident of
2026-08-11 and it occurred *inside the guidance written to prevent them*.

Against a pre-quiet rate of **18.6%**, arrival has roughly doubled. **The flag
has ridden fourteen iterations without being re-read against the condition that
justified it.** Nothing failed and no test went red — which is exactly why.

**WHAT THE SILENCE COSTS, measured before this plank existed:**
* **0 builder attacks across 2,247 self-inserts, six consecutive versions**
  (v102–v107); v104 alone **0/1,490**.
* Pre-quiet we landed `any_atk` **80.7%** and `core_atk` **17.5%**.
* **28.1% of night inserts (124/442) stood ORTHOGONALLY ADJACENT TO THE ENEMY
  CORE and never swung.**

**Three innocent explanations, all closed by controls before the build:**
| alternative | control that kills it |
|---|---|
| the attack column broke | opponents' inserts in the **same v104 files** attack at **21.1%** (124/587) |
| the tracking window closes early | our ferried bots hold **57,625 life-rounds vs their 34,298** — *more* observed time |
| we ferry for economy now, not raiding | **28.1% stood adjacent to the ENEMY CORE**; an eco ferry is not on their doorstep |

## 2. ⛔ THE COMPARISON THAT WOULD HAVE SETTLED THIS WAS NEVER SIGNIFICANT

The adoption evidence is **quiet vs Eir**: 12/15 = 80.0% core-kill share vs
33%, p=0.025. **But quiet vs the ATTACKING arm was 12/15 vs 8/15 and its own
prereg calls it "NOT significant"** — on **15 games, 5 short maps, 3 opponents.**

**And LOKI-QUIET's own question never resolved:**
`docs/RESULT-unrated-legs-2026-08-09.md` records it **INVALID BY DESIGN ERROR,
not a null** — the quiet arm still fired 43–315 turret shots/game and killed
CAD's core in 3 of 5, because the flag gates **builder melee** and the forward
**sentinel was never gated**. Damage-vs-presence is still open.

**⇒ THE BAR MAY NOT BE SET OFF THE STORED 12/15 = 80%.** Different fixture,
different era, three opponents, five short maps, Eir comparator.
**BOTH SIDES OF EVERY COMPARISON IN THIS LEG ARE MEASURED INSIDE THE ARM.**
No stored figure enters any bar. *(This rule is here because it was violated
twice on 2026-08-11 — once in Amendment 2 of PREREG-loki16b and once in the
side-lane flag raised against it.)*

## 3. THE QUESTION, STATED SO IT CANNOT DRIFT

**NOT** *"does builder melee help?"* — v96 answered that at 18% arrival and the
answer was no.

> **AT 38% ARRIVAL, IS AN ARRIVED-ROUND WORTH MORE SPENT ON DAMAGE THAN ON
> HOLDING POSITION?**

**The per-round trade is unchanged and the counter-argument is real:** acting and
moving are mutually exclusive, so every peck still costs that raider its move,
and holding a seat is itself worth something (LOKI-16b just cleared its
retention bar at +0.164). **This plank may lose on exactly that trade. That is a
result, not a failure.**

## 4. THE TREATMENT, AND ITS DOSE IS ALREADY VERIFIED — LOCALLY, WHICH IS NOT A RESULT

**ONE GATE**, `bots/_v136loki19/raid.py:256`, opened by `LOKI19_CORE_PECK_ON`:
`main.py` and `eco.py` are **byte-identical to v104**. Counterbattery melee
(defensive — `PLAY_DEFENCE: never`) and the siphon hit (economic —
`R1000_IS_DEFEAT`) **stay silenced deliberately**, so no off-programme change
rides in beside the on-programme one. `_raid_peck` (step 6) also stays silenced.

**Completeness of the gate is established by exhaustive enumeration, not
assumption:** `fire()` is the only attack call in this API; all four builder
paths (`raid.py:256`, `raid.py:335→_raid_peck`, `main.py:505`, `eco.py:911`) are
gated; every other `ct.fire(` site is `_turret` (`main.py:662`).

**DOSE, LOCAL: 777 → 3,005 `builderAttack` events over the same 10 local games.**
**⛔ THIS IS `treatment_occurrence` AND NOTHING ELSE.** Under
`FIXTURE_OF_RECORD: live_unrated` a local run against `_det_opp_v63` establishes
**that the code fires** and says **nothing whatever about effect**. **A successor
must not read the dose as a result.** It is recorded here because LOKI-17 died
for the opposite reason — a metric that could not move — and this check is what
that death bought.

## 5. BARS — each named with what in the DIFF can move it

**Every bar below is a PAIRED, IN-ARM comparison: LOKI-19 vs v104, same four
cells, interleaved windows, same session.**

### 5a. DOSE (live) — GO/NO-GO, not a finding
**Builder attacks on the enemy-core footprint, per game, ours, live unrated.**
Treatment **> 0** and control **≈ 0**. *What moves it: the gate itself.*
**If the treatment reads ~0 live, the leg is VOID and no other bar is read** —
that is an implementation failure, not evidence about melee.

### 5b. MECHANISM — the plank's own channel
**Enemy-core HP removed by builder melee, per game (2 dmg/swing), ours.**
*What moves it: the gate. Nothing else in the diff touches core damage.*
**No threshold.** This is reported to size the effect, because **the honest
prior is that it is small**: 2 damage a swing against a 500 HP core.

### 5c. CURRENCY — `core_kill_share` and time-to-core-kill
`PRIMARY_CURRENCY: kill_speed_score`, `SECONDARY: core_kill_share`,
`KILL_SPEED_IS_LEG_VERDICT: no`.
**⛔ AND THIS BAR IS NOT RESOLVABLE AT THE n BELOW. Stated now, not after.**

### 5d. THE COST SIDE, WHICH IS THE FALSIFIER AND NOT AN AFTERTHOUGHT
**Ring retention (`hold_pinned`, `scratchpad/ring_read.py`, 12-ring stratum,
game-mean, match-clustered) must NOT fall.** Every peck costs a move; if the
raider trades away the seat it was holding, this plank buys damage with
position — **and LOKI-16b just measured that position is worth +0.164.**
*What moves it: the gate, via rounds spent acting instead of moving.*

## 6. n — DECIDED HERE, BEFORE ANY LIVE NUMBER EXISTS

**MINIMUM 4 WINDOWS: 2 per arm, interleaved (control, treatment, control,
treatment), 5 challenges × 5 games each = 50 games/arm, 100 total.**
Interleaving is mandatory — a block design confounds arm with time-of-day and
with opponent version drift.

**Cells: the four PANEL-3 ADMITTED cells** (Lunds Stallions, Askar City,
Powered by SmartFridge, farming_200s), which are calibrated for `leg_read.py
--live-cells`. The 5th challenge each window goes to **farming_200s**, fixed
here by rule (highest-paying admitted cell) so it is not a post-hoc choice.

**WHAT RESOLVES AT n=50/ARM AND WHAT DOES NOT:**
| bar | resolves at this n? |
|---|---|
| **5a DOSE** | **YES** — a rate difference near 0 vs clearly positive |
| **5b MECHANISM** | **YES** — a per-game mean with hundreds of events |
| **5d COST (retention)** | **PARTIALLY** — ~10 match-clusters/arm; a large fall is visible, a small one is not |
| **5c CURRENCY** | **NO.** ~±20pp MDE on core-kill share at 50 games. **Pooling more windows is the ONLY route and windows are free.** |

**PRE-COMMITTED LANGUAGE, so the n decision cannot be laundered at write-up:**

| outcome | how it MUST be written |
|---|---|
| dose fires, mechanism > 0, **currency moves favourably, CI excludes 0** | *"clears at n=50/arm; underpowered for the currency and a pooled confirmation is now worth the exposure."* **"Confirmed" FORBIDDEN.** |
| dose fires, mechanism > 0, **currency CI straddles 0** | **THE EXPECTED OUTCOME. "Dose delivered, mechanism measured, currency unresolved at this n."** The words **"null", "refuted", "fails" are FORBIDDEN.** |
| dose fires, **retention (5d) falls materially** | *"the plank buys damage with position"* — this is the trade in §3 resolving AGAINST the plank and **may be written plainly.** |
| **dose reads ~0 live** | **VOID.** Implementation failure. **No claim about melee may be made in either direction.** |

**And the asymmetry is deliberate and is NOT asserted this time:** the only band
permitting plain language is 5d, and 5d is a **fall in a quantity we measured at
+0.164 with a CI excluding zero** — i.e. it is read against a live in-arm
control, not against a power assumption. **The Flag-2 debt from PREREG-loki16b
(`P(point ≤ 0 | true effect, k clusters)`) is NOT inherited here, because no
band in this table licenses a kill on a null currency result.**

## 7. WHAT THIS LEG MAY NOT DO

It may not be read as a win-rate result. It may not borrow LOKI-QUIET's 12/15,
LOKI-16's or LOKI-16b's bars. **It may not revise any threshold because an
implementation reached a different number.** It may not pool `jackpot` into the
retention stratum. **And it may not treat the local dose figure as evidence of
effect.**

## 8. UNPRICED, STATED SO IT IS NOT DISCOVERED AT READ-OUT

* **We are the field's heaviest user of enemy-bot ejection — 3,727 hostile
  throws to their 1,927 in the night sample — and simultaneously the only team
  whose own inserts never attack.** Our launcher is almost entirely an ejection
  tool and almost not an insertion tool. **This plank does not change that.**
* **Kidnap effectiveness has NO column in `throws.tsv` at all.** That is a
  **decoder gap and must never be read as a null.**
* **The v95–v101 transition zone is unexplained.** v98 was submitted 17:10,
  twenty minutes before the LOKI-QUIET tree existed (`7beac55` 17:30), and reads
  0.0%. **Both other lanes have been wrong about it once each. Do not write the
  tidy history**; this prereg's claims are scoped to the CURRENT tree, where the
  gate is established by enumeration.
* **Opponent versions are pinned from `league_matches.tsv` / `meta_join`, never
  `ladder_games.tsv.oppver`** (literally `'None'` for every row, and a null
  column reads as "no version change").

---

# AMENDMENT 1 — THE ARRIVAL GATE. ADD-ONLY, COMMITTED AFTER THE CONTROL WINDOW FIRED AND BEFORE THE TREATMENT ARM EXISTS.

**Written 2026-08-11 06:4x CEST (`date`, same shell). Control window 1 fired
04:35:21–04:35:38Z, 5/5 accepted, holder v104 asserted before every challenge.
NO TREATMENT GAME HAS BEEN PLAYED AND NO ARRIVAL NUMBER FROM THIS LEG HAS BEEN
READ.** This amendment ADDS a gate and RESTATES a question; it moves no bar.

## 1a. ⛔ THE 38% IN §3 IS A RATED FIGURE AND THIS LEG FIRES UNRATED

Side-lane catch, and it is the one flag that could have invalidated the leg
after the fact. Our own v104, `kind=INSERT`, ours, reach:

| population | reach | n |
|---|---:|---:|
| **RATED** | **39.8%** | 246 |
| **UNRATED — the fixture this leg actually uses** | **20.0%** | 1,247 |

**The pre-quiet rate that justified silencing the melee was 18.6%.**

**⇒ IN THE FIXTURE THIS LEG RUNS IN, ARRIVAL MAY SIT ESSENTIALLY AT THE NUMBER
THAT MADE QUIET CORRECT IN THE FIRST PLACE.** If so, LOKI-19 re-runs v96's
experiment at v96's arrival rate under a new name, and §6's expected outcome
(currency CI straddles 0) is **uninterpretable as evidence about the changed
premise — because in that fixture the premise did not change.**

**And arrival is not a property of our bot at all — it is per-cell, with a 6x
spread** (night panel, INSERT reach): Landers 82.8% · Team 48 72.7% ·
farming_200s 50.0% · gsxWins 29.2% · kladde 27.6% · **Lunds Stallions 25.0%** ·
CtrlAltDefeat 21.2% · I Stone 18.6% · Powerpuff 13.3%. **On this leg's own
admitted cells only two have measured arrival — Lunds 25.0% (12/48) and
farming_200s 50.0% (10/20); Askar City and SmartFridge have NONE.**

**This is D13 on an axis the fixture work has not covered: a cell must admit the
mechanism, and THIS mechanism's PRECONDITION IS HIGH ARRIVAL.** Map admission was
checked for LOKI-16b's ring geometry; nobody had checked arrival admission.

## 1b. NEW GATE — 5a-bis, ARRIVAL, MEASURED IN-ARM ON THE CONTROL

**Our INSERT reach on the four cells, CONTROL arm, live unrated, this leg's own
games. Reported PER CELL, never pooled — a 6x spread makes a pooled mean a
fiction.** Measured with the same decoder on both arms; **no stored figure
enters it**, per §2.

**PRE-COMMITTED READING, written before the number is computed:**

| control-arm arrival | what the leg may claim |
|---|---|
| **> 30%** | the fixture delivers the changed premise. **§3's question stands as written and the leg tests it.** |
| **20–30%** | **AMBIGUOUS. The leg may report dose, mechanism and cost, and may NOT claim to have tested "the changed premise."** Any currency result is reported as fixture-conditional. |
| **≤ 20%** | **the fixture sits at pre-quiet arrival. The leg ANSWERS v96's QUESTION AGAIN and may not be read as evidence about the premise shift in either direction.** Dose and cost still read; the framing in §1 and §3 does not. |

**This gate cannot flatter the result. It can only tell me whether the leg tested
the question I meant** — which is exactly what §2's in-arm rule is for, applied
one level up from the bars to the QUESTION.

## 1c. §3 IS RESTATED FIXTURE-RELATIVE. THE NUMBER LEAVES THE QUESTION.

**Struck:** *"AT 38% ARRIVAL, is an arrived-round worth more spent on damage than
on holding position?"*

**Replaces it:**

> **AT THE ARRIVAL RATE THIS FIXTURE DELIVERS — measured in-arm and reported per
> cell — is an arrived-round worth more spent on damage than on holding
> position?**

**Arrival becomes an OBSERVED COVARIATE of this leg rather than a premise
imported from another population.** The §1 history (18.6% → 38.1% rated) stays as
the MOTIVATION for asking, clearly tagged, and is no longer load-bearing on the
read-out. **A question quantified at 38% and resolved in a fixture at 20% is the
units-not-data failure at the level of the hypothesis instead of the column, and
it would have been invisible in every bar.**

## 1d. A CONTROL FIGURE IN §1 IS FLAGGED, NOT YET RECONCILED

§1 cites *"opponents' inserts in the same v104 files attack at 21.1%
(124/587)."* An independent decode of the same 485 files gives their friendly
inserts as **107/331 = 32.3%**, and **124 is separately OUR reached count
(124/442 = 28.1%)** — so the `124` may be a carry-over, and **`587` does not
reproduce at all.**

**The control's DIRECTION is unaffected — their column is alive and ours is zero
on every version of the cut — so the conclusion it supports (the decoder is not
broken) stands.** But it is a control figure inside a pre-registration and this
document's own §1 says the population tag is load-bearing. **Recorded as
unreconciled rather than quietly corrected; the exact filter behind 124/587 must
be named before it is cited again.**

## 1e. WHAT THIS AMENDMENT MAY NOT DO

It may not move any bar in §5, the n in §6, the cells, or the four-band language.
It may not be read as weakening the plank: **§1's measured facts — 0 attacks
across 2,247 inserts, 28.1% standing adjacent to the enemy core — are unaffected
by which population the ARRIVAL RATE is computed on.** What changes is only what
this leg is entitled to conclude about WHY.

---

# AMENDMENT 2 — ARRIVAL ADMISSION MEASURED PER CELL. THE PANEL LARGELY DOES NOT ADMIT THIS MECHANISM, AND ONE CELL IS REPLACED.

**Written 2026-08-11 06:4x CEST. ADD-only. Committed BEFORE the treatment arm
exists — no LOKI-19 game has been played anywhere.** This is a CELL-SELECTION
decision made on a criterion Amendment 1 stated **before** this measurement was
run, and it does not touch the in-arm gate 5a-bis.

## 2a. THE MEASUREMENT — v104, `kind=INSERT`, OURS, archived, per cell

| cell | n | reach | band (Amendment 1b) |
|---|---:|---:|---|
| **Powered by SmartFridge** | **512** | **7.6%** | **⛔ ≤20 — FAR BELOW the 18.6% pre-quiet rate** |
| Lunds Stallions | 100 | 21.0% | 20–30 ambiguous |
| Askar City | 44 | 27.3% | 20–30 ambiguous |
| farming_200s | 38 | 57.9% | **>30 — premise holds** |
| *Landers (not in panel)* | 54 | **68.5%** | **>30 — premise holds** |
| *Team 48 (not in panel)* | 29 | 44.8% | >30 — premise holds |

**⇒ OF THE FOUR ADMITTED CELLS, EXACTLY ONE DELIVERS THE PREMISE.** And
**SmartFridge — the LARGEST sample on the board at n=512 — arrives at 7.6%, less
than half the rate that made silencing the melee correct in the first place.**
Firing there is not a weak test of the premise; it is a test of the opposite
condition.

**This is the tension named precisely: "ADMITTED" AND "ADMITS THIS MECHANISM"
ARE DIFFERENT PROPERTIES.** PANEL-3's cells were selected for **resolution**
(calibrated for `leg_read --live-cells`). **This plank's precondition is HIGH
ARRIVAL, and nobody had ever checked a panel for it.** Map admission was checked
for LOKI-16b's ring geometry; arrival admission was checked by nobody, for
anything, until now.

## 2b. THE CHANGE — the 5th challenge becomes LANDERS, not a farming_200s double

The §6 rule sent the 5th challenge of each window to farming_200s as the
highest-paying admitted cell. **From window 2 onward it goes to Landers.**

```
TARGET BAND: Landers, gap -37, a 5-0 pays 14.32, reachable YES (p19 of 149)
```
*(verbatim `tools/target_value.py`, run before this amendment was written)*

**Why Landers and not Team 48:** Landers is **reachable at −37** and Team 48 sits
at the band edge (−90) where research has already dropped it as a currency
target (2.7% of v104's rated diet, and its rated sample inverts). **Landers has
the highest measured arrival on the board (68.5%) AND pays inside the band.**

**⛔ WHAT THIS DOES NOT DO: SmartFridge, Askar City and Lunds Stallions STAY.**
Dropping the low-arrival cells after measuring them would be selecting the
fixture to suit the plank — and their §5 bars (dose, mechanism, cost) do not
depend on arrival. **Only the ability to speak about the PREMISE does.**

## 2c. THE ASYMMETRY THIS CREATES IS DISCLOSED, NOT PAPERED OVER

**Control window 1 already fired** (04:35:21–04:35:38Z, 5/5) with the original
rule: four cells plus a **farming_200s double, and no Landers.** Windows 2+ carry
four cells plus **Landers**. **So the arms do not share an identical cell mix and
window 1 is the odd one.**

**This is tolerable ONLY because Amendment 1b already forbids pooling arrival and
mandates per-cell reporting** — per-cell reads are unaffected by the mix; only a
pooled number would be corrupted, and a pooled number is already banned.
**Pre-committed: the LOKI-19-vs-v104 comparison is made CELL-BY-CELL on cells
present in both arms. Window 1's extra farming_200s games are reported and are
NOT silently averaged into the farming cell's treatment comparison** — the
matched control for treatment farming games is the equal number of window-1
farming games, chosen by challenge order, not by outcome.

## 2d. AND THE HONEST FORECAST, WRITTEN BEFORE THE DATA

**On these priors the modal outcome of gate 5a-bis is still the 20–30 AMBIGUOUS
band**, because three of five cells sit at or below 27% and SmartFridge's 7.6%
drags any average hard. **I am firing anyway, and the reason is stated in
advance rather than reconstructed afterwards:** the bars that actually resolve at
this n — **dose (5a), mechanism (5b) and the cost/falsifier (5d)** — are all
arrival-independent. **The premise claim is the ONLY thing at risk from a low
gate reading, and Amendment 1 already forbids me from making it in that case.**

**⇒ A leg that returns "dose delivered, mechanism sized, cost measured, premise
untested" is a SUCCESS of this design, not a failure of it.** Writing that down
now so it cannot be spun either way later.

## 2e. CAVEATS ON THE NUMBERS THIS AMENDMENT RESTS ON

Per-cell n is small for the decisive cells (**farming 38, Landers 54, Team 48
29**) and large only for the cell being demoted (SmartFridge 512). All are
**v104, ours, `kind=INSERT`, archived, pooling rated and unrated** — a broader
population than Amendment 1's rated-only baseline, chosen because the per-cell
rated n would be near zero. **The 6x cross-opponent spread means any of these can
move materially on a different map mix.** They are good enough to SELECT a cell
and **not good enough to be a bar**, which is exactly how they are used here.
