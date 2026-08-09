# The CAD "lockout": a population test, commissioned to kill it

**Research arm, 2026-08-09. Adversarial check, run BEFORE the hypothesis is
allowed to become a build input.**

**Version tag:** live slot **v94 = `bots/_v115dodge`, treehash `6ae6871c`**.
Corpus git sha per the commission: **`7418e13`** — note `corpus/manifest.json`
at freeze time records `git_sha: abc18cb`, `built_utc 2026-08-09T14:40:25Z`,
`archive_replays: 6393`; both are recorded rather than reconciled, because the
core analysis below does **not** read the corpus tables (see PROVENANCE).

**Verdict in one line: the lockout as stated — "after early core damage CAD
never executes another build action" — is REFUTED at population level, 0 of 51
games in the trigger cell. A real, large, but TRANSIENT ~25-round build
suppression does reproduce, and survives every confound the commission named.
The autopsy's arrival mechanism is worth something; its paralysis mechanism and
its r70–85 kill timing are not.**

---

## PROVENANCE AND FREEZE

The commission pointed at `corpus/*.tsv`. Those files answer a different
question: `events.tsv` carries BUILD and DEATH only, and **no damage stream at
all**, so the load-bearing measurement here — *when did CAD's core first take
damage* — cannot come from the corpus. It came from a fresh decode of the
archived replays, reusing the validated wire primitives in
`tools/replay_census.py` (`fields`, `read_pos`, `parse_entity`,
`packed_varints`) and the Update field map in `tools/replay_schema.md`.

The corpus was still used, and frozen: `join.tsv` for the seat cross-validation
and for map names, the rest for the trap checks. **Zero replay downloads** —
every file read was already on disk.

Frozen into `scratchpad/cad-lockout-freeze/` (own subdirectory, nothing else
touched):

| file | rows | md5 |
| --- | --- | --- |
| `join.tsv` | 1,446 | `e943d4ac38e5339ac7c577263b9156cf` |
| `events.tsv` | 1,040,627 | `4cbf7e0f858956c0e165495d58f21057` |
| `builds.tsv` | 93,361 | `ddf35879dd5db70f31fc2d4fabd06c3b` |
| `build_agg.tsv` | 150,435 | `5c0953507b4466f6901a7c016c116e72` |
| `econ.tsv` | 37,383 | `ecffa74d1c7b2d464c0523a2b83f776b` |
| `throws.tsv` | 100,910 | `4c66dbdac419830e6a828fe260800e2d` |
| `flow.tsv` | 68,465 | `4043225a0c1365d793dbc546758417a3` |
| `ladder_games.tsv` | 2,716 | `ca2c6f599839fb30d9284b28bdec46d2` |
| `league_matches.tsv` | 27,074 | `f1610459534b6e61ce38d36f5549faed` |
| `league_games.tsv` | 3,706 | `644fff75bbbfa0d52e69b23cb2f27014` |

Derived, and also frozen:

| file | rows | md5 |
| --- | --- | --- |
| `cad_population.tsv` | 221 | `228d183adbc11ce8742c1ff39ea95f79` |
| `cad_rounds.tsv` | 87,528 | `20b99ff6dfac6d772b42198f18e4d079` |
| `cad_outcome.tsv` | 221 | `53810a789a038ceb66555c38fba4e0e1` |

The archive grew from 6,393 replays (manifest) to **6,473** during the run,
which is exactly why the freeze exists. Scripts:
`docs/research/scripts/cad-lockout-2026-08-09/`.

### The population is 220 games, not 85 — and 115 of them are not ours

`join.tsv` attributes **85** CAD games, all of them ours. But every archived
match carries a sibling `<id>.meta.json` holding `teamAName`/`teamBName` and
`teamAVersion`/`teamBVersion`. That yields **220 CAD game files across 44
matches**, of which **115 are CAD versus third parties** — games our own bot is
not in, and therefore the cleanest available test bed for "does CAD lock out".
It also **solves the version problem the commission flagged as possibly
unsolvable**: `meta.json` gives CAD's version directly, so nothing is pooled.

| | n |
| --- | --- |
| CAD game files | 220 |
| distinct matches | 44 |
| vs OpenSverige | 105 |
| vs third parties (gsxWins, Powered by SmartFridge, Askar City, LingLing40, Team 48, Ouroboros, Lunds Stallions, Memtrace, Powerpuff Girls, arsonist duck) | 115 |
| distinct maps | 15 |
| CAD versions | 7 (v107, v116, v117, v118, v120, v123, v124) |

---

## PRE-COMMITMENT

Three sharpenings arrived from the hypothesis's author **mid-run, before any
result existed**, and are recorded here because that ordering is what makes the
third one honest rather than a post-hoc excuse:

1. **The signature is ZERO, not "lower."** A merely depressed build rate is not
   this mechanism and must be reported as *something else*.
2. **Stratify by first-damage band** ≤r13 / r14–25 / r26+, with paralysis
   predicted in band 1 and demonstrable counter-building in band 2.
3. **Band 1 was expected to be nearly empty**, with the pre-committed
   conclusion being "the population cannot test the trigger cell."

Prediction 3 turned out to be **wrong in our favour: band 1 holds 51 games**, so
the trigger cell *is* testable and the pre-committed underpowered-verdict does
not apply. Prediction 2 **held**. Prediction 1 is the rule under which the
headline verdict below is a refutation rather than a confirmation.

---

## THE DESIGN, AND WHY EACH CONFOUND FORCED IT

**Confound 1 — the opening is a script.** Taken as given from the commission:
185 forward-ferry `INSERT` throws in r2–r5, zero after r5, on all 15 maps. A
team with a fixed opening shows a build-rate cliff at a fixed round in *every*
game, damaged or not. **A within-game before/after contrast therefore measures
the script, not the damage, and is not reported anywhere in this document.**
Every headline number is a **landmark**: CAD's build count over the **same
absolute round window**, compared between games where core damage had already
landed by the window's start and games where it had not. The script is identical
on both sides and cancels.

**Confound 2 — reverse causation.** Cut: CAD's build rate in rounds
`[6, first_damage−1]`, strictly before any damage landed in that game.

**Confound 3 — selection on the outcome.** Every band is also reported split by
whether CAD's core eventually died.

**Confound 4 (the commission's own) — CAD may be dead, not paralysed.** Cut:
CAD's living builder bots through the window.

**Confound 5, which the commission did not anticipate and I found in the first
pass — CAD IS BROKE.** CAD's scripted r4 ammo conversion can leave it under 10
titanium, and an opponent close enough to hit the core by r13 is also close
enough to be eating the economy that would refill it. This got its own natural
experiment; see §6.

---

## VALIDATION

**Trap 2, the two's-complement varint.** `updateHp.delta` is sign-extended to 64
bits; `_s64()` subtracts `1<<64` above `1<<63`. Sign census over the whole
population: **98,867 negative, 74,576 positive, 0 zero.** Both signs observed —
heals are the positives — so the correction is not silently zeroing damage the
way the `1<<32` bug once did.

**Trap 1, the rotate re-emit.** A build is the FIRST `placeEntity` carrying an
id; later ones update state. Independent check: `placeEntity`-builds 12,944
minus `BuilderBuild` events 10,490 = **2,454**, and the independent core-spawn
estimate (CAD builder-bot deaths + builder bots alive at end) = **2,454
exactly**. The two build streams reconcile.

**FireTurret attribution.** 66,224 shots seen, **0 unattributed** against the
live turret-tile→team index.

**Seat.** Replay team 0 == meta `teamA`, checked against `join.tsv`'s
independently reconciled `our_team` on the 85 overlapping games: **85 agree, 0
disagree.**

**Reproduction of the originating game** (`f92f1ca2` game 5, decoded blind by
this pipeline): first CAD core damage **r12**; core HP at the final round
**−15** at **r73** (74 turns) — matching the autopsy's 15 overkill exactly; r4
conversion **187 Ti**; CAD ammo frozen at **195**; CAD launcher removed at
**r6** with zero prior damage. Independent decode, same numbers.

**One correction to the autopsy.** The autopsy states *"zero build actions
r12–73."* It was **one**, not zero: at **r20 CAD's core spawned a builder bot**,
CAD titanium 50 → 4, builder count 4 → 5. This matters to the claim's own
wording — *"with 30–92 Ti in hand"* — because CAD in fact **spent** down to 4 Ti
at r20. The `BuilderBuild` count for r12–73 is genuinely zero; the *build
action* count is one.

---

## RESULTS

### 1. How rare is early core damage on CAD? (a useful number in its own right)

| population | n | ≤r13 | r14–25 | r26+ | never | median first damage |
| --- | --- | --- | --- | --- | --- | --- |
| all | 220 | **51** | 60 | 70 | 39 | r21 |
| vs us | 105 | **24** | 29 | 29 | 23 | r20 |
| vs third parties | 115 | **27** | 31 | 41 | 16 | r23 |

**Band 1 is not rare and not empty.** 51 games from **31 distinct matches, 5
distinct opponents, 9 distinct maps** — so the cell is not one match repeated.

### 2. THE LANDMARK — the suppression is real and large

| window | cell | n | mean builds | median | **ZERO** |
| --- | --- | --- | --- | --- | --- |
| r14–r25 | damaged before window | 51 | **0.4** | 0 | **35/51 (69%)** |
| r14–r25 | undamaged at window open | 169 | 4.1 | 4 | 13/169 (8%) |
| r14–r40 | damaged before window | 51 | **1.0** | 1 | **16/51 (31%)** |
| r14–r40 | undamaged at window open | 167 | 7.4 | 7 | 3/167 (2%) |
| r26–r45 | damaged before window | 108 | 1.6 | 1 | 26/108 (24%) |
| r26–r45 | undamaged at window open | 109 | 5.4 | 5 | 5/109 (5%) |
| r41–r80 | damaged before window | 116 | 6.2 | 4 | 18/116 (16%) |
| r41–r80 | undamaged at window open | 88 | 9.1 | 7.5 | 3/88 (3%) |

A ~7× gap in the same absolute window. `BuilderBuild`-only figures track within
0.3 throughout. **Something is real here.** Note also that the gap **closes with
time** — 7× at r14–40, 1.5× at r41–80.

### 3. Banded, window r14–r40 — and band 2 behaves exactly as predicted

| band | n | mean builds | median | ZERO |
| --- | --- | --- | --- | --- |
| ≤r13 | 51 | **1.0** | 1 | 16/51 (31%) |
| r14–25 | 58 | 5.7 | 5 | **1/58 (2%)** |
| r26+ | 70 | 8.7 | 9 | 2/70 (3%) |
| never | 39 | 7.5 | 6 | 0/39 (0%) |

**Pre-committed prediction 2 confirmed:** band 2 counter-builds robustly — only
1 of 58 games has a zero window. The failure branch of the autopsy's prediction
("first shot ≥ r16 → the plant meets a counter-gunner") rests on behaviour that
does reproduce.

### 4. THE HEADLINE — the latch does not exist

The hypothesis is not "fewer builds." It is *"CAD never executed another build
action for the remaining 62 rounds."* Scored strictly, over games with a tail of
**≥30 rounds** after first damage so a game that merely ended cannot masquerade
as a latch:

| band | n (tail ≥30) | latched (0 builds in tail) | latched with a builder alive | median builds in tail |
| --- | --- | --- | --- | --- |
| **≤r13** | **51** | **0** | **0** | **8** |
| r14–25 | 57 | 1 | 1 | 46 |
| r26+ | 67 | 4 | 3 | 27 |

**Zero of 51.** And the reaction is not merely non-zero, it is *immediate*:

| band | median rounds from first core damage to CAD's next build | never builds again |
| --- | --- | --- |
| ≤r13 | **0** (same round) | **0** |
| r14–25 | 1 | 1 |
| r26+ | 1 | 5 |

Distribution of post-damage build counts in the trigger cell: min **1**, p25
**3**, median **8**, p75 **50**, max **210**. Games with 0: **0**. Games with
≥10: **24 of 51**.

The four games that *are* latched sit in bands 2 and 3, and three of them have
first damage at **r218, r251, r374** — a late-game collapse under a won
position, which is a different phenomenon wearing the same shape.

**CAD resumes.** Trigger-cell games surviving past r120: median **2** builds in
r41–80 and **1.5** in r81–120, against 9.0 / 7.5 for band 2. Suppressed, not
latched.

### 5. The three named confounds do NOT explain the suppression

**Reverse causation — refuted, and it points the other way.** Builds per round
in `[6, first_damage−1]`, strictly pre-damage:

| band | n | median builds/round before any damage |
| --- | --- | --- |
| ≤r13 | 25 | **0.83** |
| r14–25 | 60 | 0.65 |
| r26+ | 70 | 0.35 |
| never | 39 | 0.62 |

Early-damaged games had the **highest** pre-damage build rate of any band. The
arrow does not run "CAD built less → we got close." (n=25 because games damaged
at or before r6 have no pre-damage window to measure.)

**Builder death — refuted.** In every band, CAD holds a **median of 4 builder
bots** both at r14 and at the minimum across r14–r40. **16** of the trigger
cell's zero-build games had **≥1 builder alive throughout**. CAD is not
paralysed because it is dead.

**Outcome selection — survives it.** Within games where **CAD's core survived**
(the cleaner cut, since nothing downstream is contaminated by an imminent loss):

| band | n | mean builds r14–40 | ZERO |
| --- | --- | --- | --- |
| ≤r13 | 21 | **1.1** | 3/21 |
| r14–25 | 38 | 6.8 | 0/38 |
| r26+ | 42 | 9.7 | 0/42 |
| never | 39 | 7.5 | 0/39 |

Same shape, same magnitude.

### 6. Poverty — the confound I added, tested by natural experiment, also refuted

§8 below establishes that CAD's r4 ammo dump fires on **5 of 15 maps** and
essentially never on the other 10, leaving CAD at a median **28 Ti** through
r6–r13 on dump maps against **204 Ti** on no-dump maps. That is a free
experiment: if the suppression were poverty, it should shrink on maps where CAD
is holding 200 titanium.

| map class | band | n | mean builds r14–40 | ZERO |
| --- | --- | --- | --- | --- |
| **dump** (CAD broke) | ≤r13 | 28 | **0.9** | 7/28 |
| dump | r14–25 | 9 | 3.0 | 1/9 |
| dump | r26+ | 21 | 5.8 | 1/21 |
| **no-dump** (CAD rich) | ≤r13 | 23 | **1.1** | 9/23 |
| no-dump | r14–25 | 49 | 6.2 | 0/49 |
| no-dump | r26+ | 49 | 10.0 | 1/49 |

**The suppression is the same size on rich maps as on poor maps** (1.1 vs 0.9;
39% zero vs 25%). Poverty does not explain it.

Honest counterweight, because it cuts the other way and belongs here: CAD's
titanium in the r14–40 window is low in *both* early-damage cells (26 and 20)
regardless of map class, and titanium balance is an **outcome** of building, not
a clean instrument — a team that does not build accumulates money. The
idle-rich audit is mixed: the 16 zero-build trigger games have a **median 4
rounds** where CAD held ≥36 Ti and built nothing, but two of them
(`ad5ce3c9`, `20ff06a2`) sat on 44–50 Ti for 22–27 idle rounds while four
others (`071c8384` max 19 Ti, `922be463` max 16 Ti) genuinely could not afford
a builder bot. **Poverty is a real contributor in some games and cannot be the
whole story in others.**

### 7. Version — the join is feasible, nothing is pooled, the effect is not version-confined

`meta.json` gives CAD's version per match, so the dead columns
(`join.tsv.oppver`, `ladder_games.tsv.oppver`, `league_games.tsv.verA/verB`, all
the literal string `"None"`) were never needed.

| CAD version | n | ≤r13 | r14–25 | r26+ | never | builds r14–40, mean | ZERO |
| --- | --- | --- | --- | --- | --- | --- | --- |
| v107 | 40 | 11 | 10 | 12 | 7 | 5.3 | 5/40 |
| v116 | 10 | 0 | 0 | 4 | 6 | 9.0 | 0/10 |
| v117 | 50 | 15 | 14 | 14 | 7 | 5.5 | 1/50 |
| v118 | 5 | 1 | 1 | 1 | 2 | 6.6 | 0/5 |
| v120 | 45 | 11 | 14 | 12 | 8 | 5.5 | 3/45 |
| v123 | 25 | 2 | 8 | 12 | 3 | 6.8 | 2/25 |
| **v124** (the originating version) | 45 | 11 | 13 | 15 | 6 | 6.0 | 8/43 |

Banded, **v124 vs everything else**, window r14–r40:

| group | ≤r13 | r14–25 | r26+ | never |
| --- | --- | --- | --- | --- |
| v124 | 0.5 (ZERO 7/11) | 6.3 (0/11) | 7.3 (1/15) | 12.0 (0/6) |
| not v124 | 1.1 (ZERO 9/40) | 5.5 (1/47) | 9.1 (1/55) | 6.7 (0/33) |

The transient suppression is present in **both**, somewhat stronger in v124.
**The latch is present in neither: 0 latched of 11 v124 trigger games (median 5
builds in the tail) and 0 of 40 non-v124 (median 10).** The originating
version does not behave differently in kind.

### 8. The second question: r6 launcher self-destruct and r4 ammo dump

**The r6 launcher removal is a genuine map-independent invariant.** Conditioned
on a launcher existing by r5 — a map where CAD never builds one cannot show the
behaviour, and scoring that as "absent" would be wrong:

**201 of 201 games in which a CAD launcher existed by r5 had it removed at r6
with zero prior damage. Zero combat removals at r6. Zero launcher removals at
any other round in r0–r12.** Present on **all 15 maps** and **all 7 versions**
(v107 37/37, v116 10/10, v117 44/44, v118 5/5, v120 39/39, v123 23/23, v124
43/43).

What varies is whether CAD builds a launcher at all: 16/16 archipelago, 14/14
atoll, 19/19 drumlin, 21/21 moonrise, 12/12 nordkap … but only **7/14 meander**
and **2/11 fjordgate** (10×10 — no distance to ferry across). *Caveat, matching
the autopsy's own "could not determine":* "no prior damage" establishes the
removal is **non-combat**, but cannot separate `self_destruct()` from an allied
builder's `destroy()`.

**The r4 ammo dump is NOT map-independent. This corrects the working
assumption.**

| map | dims | n | r4 dump (≥100 Ti) | median dump |
| --- | --- | --- | --- | --- |
| eider | 28×20 | 16 | **16/16** | 187 |
| heart | 28×20 | 14 | **14/14** | 176.5 |
| nordkap | 20×26 | 12 | **12/12** | 187 |
| moonrise | 21×8 | 21 | **15/21** | 187 |
| antler | 14×18 | 16 | **10/16** | 248 |
| fjordgate | 10×10 | 11 | 2/11 | 112 |
| meander | 25×15 | 14 | 1/14 | 254 |
| archipelago, atoll, drumlin, hive, jackpot, lighthouse, saga, snowflake | — | 116 | **0/116** | — |

On the ten no-dump maps CAD converts a total of **24 Ti** across r0–r5 — the
8/8/8 opening trickle and nothing more. Pooled by round, r4 is the only spike:
97 of 220 games convert at r4, mean **146.8 Ti**, against means of 8–12 at
r0–r2.

**It is a map effect, not a version effect.** The cross-tab holds within every
version: archipelago is 0/n for all seven, eider dumps for v107/116/117/120/124,
nordkap 12/12 across v116/117/120/123/124. (Antler and moonrise show genuine
version drift on top of the map effect — antler v107 4/4 but v124 0/3.)

**Consequence, which is the part the side lane actually asked about: the
"poverty window" after the dump is real but confined to ~5 of 15 maps.** Median
CAD titanium in r6–r13 is **28** on dump maps and **204** on no-dump maps
(median ammo 184 vs 24). **nordkap is a dump map**, so the autopsy's
nordkap-specific reasoning about CAD's post-dump poverty is locally correct —
it simply does not generalise to two thirds of the pool.

### 9. What the leg actually rests on: does early damage convert to a kill?

The autopsy's pre-registrable prediction, scored on the population:

| claim | result |
| --- | --- |
| trigger cell (first damage ≤ r13) | n = **51** |
| (a) zero build actions thereafter | **0/51** |
| (b) CAD core killed at all | 30/51 (59%) |
| (b) CAD core killed by r85 | **7/51 (14%)** |
| (a) and (b) together | **0/51** |

Restricted to **our own games**, which is the population a leg would fire into:

| band | n | CAD core died | rate | median kill round | killed by r85 |
| --- | --- | --- | --- | --- | --- |
| ≤r13 | 24 | 9 | **38%** | r168 | **1** |
| r14–25 | 29 | 2 | 7% | r178 | 0 |
| r26+ | 29 | 3 | 10% | r315 | 0 |
| never | 23 | 0 | 0% | — | 0 |

**The one game killed by r85 is the originating game itself.** So the specific
timing claim ("core kill ~r70–85 even sentinel-only") has a population support
of exactly n=1, and that n=1 is the game the hypothesis was fitted to.

**But the arrival mechanism is not worthless, and this is the finding worth
keeping:** early damage raises our kill rate against CAD from 7–10% to **38%**,
a 4–5× lift, and third parties convert it at **78%**. What it does not do is
produce paralysis, and it does not produce a fast kill — the median is r168, not
r73.

---

## WHAT GAME 5 WAS INSTEAD

Game 5 is the **extreme tail of a real distribution, not a different
mechanism**. Its post-damage build count of 1 is the minimum of 51 (p25 = 3,
median = 8). Every ingredient of it is population-normal on its own — nordkap is
a dump map so CAD was poor by script; early damage genuinely suppresses building
for ~25 rounds; CAD's single-healer collar cannot outpace 9 HP/round — and the
autopsy's arithmetic on those is sound. What is not supported is the **latch**:
the inference that damage *gated* CAD's build branch. In 51 comparable games CAD
built again, usually in the same round.

The honest reading of game 5 is that **we caught the tail of the suppression
window in a game where the suppression happened to run long enough for a
sentinel to finish the job** — with `3bea0784` game 2 as the direct counterpart
on the same map, same version (v124), first damage r7, where CAD went on to
execute **84** further build actions and survive 544 rounds.

---

## NON-COVERAGE AND LIMITS

1. **"In 220 attributed CAD games," never "CAD always."** The archive is not a
   random sample of the field; it is dominated by matches we or the archiver
   pulled. Third-party coverage is 115 games but concentrated on 5 opponents.
2. **The trigger cell is 51 games but only 31 matches** (games within a match
   share a version and an opponent, so they are not independent). No
   significance test is reported; treat the 7× gap as descriptive.
3. **Titanium balance is an outcome, not an instrument.** The poverty cut leans
   on a map-level natural experiment precisely because the per-round balance is
   endogenous, but the idle-rich audit that supplements it is a judgement call
   at the 36 Ti threshold.
4. **`nodmg` launcher removal cannot separate `self_destruct()` from an allied
   `destroy()`** — the autopsy's own open item stands.
5. **CAD's internal gate is not in a replay.** This document can show that CAD
   *does* build after early damage; it cannot show *why* it built less for 25
   rounds. Candidate explanations not separable here: a rebuild-priority
   ordering that reorders under threat, a defensive branch that spends on heals
   instead, or contested-tile `can_build` failures near a live sentinel.
6. **Not measured:** whether the suppressed builds are *displaced* into heals
   (the collar) rather than lost. `BuilderHeal` (Update field 15) is decodable
   and would settle it; out of scope for this pass and the obvious next cut.
7. **The five maps that dump were not explained.** eider/heart (28×20),
   nordkap (20×26), moonrise (21×8), antler (14×18) share no obvious dimension
   rule; the trigger is probably ore layout or core distance, unmeasured here.
8. **`econ.tsv`'s `shots`/`deliveries` dead columns and the `oppver`/`verA/verB`
   dead columns were avoided entirely**, not worked around — shots came from a
   fresh `fireTurret` decode (0 unattributed) and versions from `meta.json`.

---

## FOR THE BUILDER, IF A LEG IS STILL FIRED

Not a verdict — verdicts are the builder's. The measured facts a prereg would
need to survive:

- **Do not preregister "CAD stops building."** It is 0/51. A leg predicting
  paralysis will be scored a failure by its own instrument.
- **A defensible prereg is the arrival mechanism only:** first core damage ≤ r13
  raises CAD core-kill rate from 7–10% to ~38% in our games (n=24). That is the
  effect with population support.
- **Do not preregister the r70–85 kill window.** Population median for our
  early-damage kills is **r168**; n=1 has ever landed by r85 and it is the
  originating game.
- **The geometry precondition is narrower than "nordkap-like."** The post-dump
  poverty window exists on antler, eider, heart, moonrise, nordkap and
  essentially nowhere else.
