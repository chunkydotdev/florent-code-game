# ⭐ THE SEAT EFFECT IN THE 8×1024 BATTERY IS THE MAP SET — AND MAPS ARE NOT SEAT-SYMMETRIC

**Research arm, s31, 2026-08-11.** Commissioned by nothing; produced by
re-deriving a builder finding that arrived mid-session. **Every number below is
re-derived from a primary in this repo, not relayed.**

**Populations, named rather than scalarised:**
* **LOCAL** — `scratchpad/battery/*.log`, eight arms × 1,024 games vs
  `_v130loki13` (v104), maps `antler atoll drumlin fjordgate heart hive meander
  nordkap`, 512 games in **each** seat per arm. 8,192 games.
* **PLATFORM** — `corpus/ladder_games.tsv`, 3,740 rated ladder games, all our
  versions, all opponents, `winner_seat` as recorded by the platform.

---

## 1. WHAT THE BUILDER FOUND, REPRODUCED EXACTLY

All eight arms win more from seat A than seat B. Treatment wins **2127/4096
(51.93%) on seat A** against **1789/4096 (43.68%) on seat B**. Both figures
reproduce to the game from the eight logs.

**But "8 of 8 arms" is the wrong statistic**, because the eight arms share the
control bot, the maps and the seeds — they are not eight independent trials. The
informative quantity is the seat, pooled:

> **Seat A wins 4434 of 8192 = 54.13%** (z = +7.47).
> *(2127 A-wins where treatment is A, plus 4096 − 1789 = 2307 A-wins where
> treatment is B.)*

Writing `s` = P(A wins | equal bots) and `t` = the pooled treatment effect, the
two seat rates imply:

| parameter | value |
|---|---:|
| seat advantage `s` | **54.126%** |
| treatment effect `t`, pooled over the eight arms | **−2.195 pp** |

**⛔ AND THE "CHECK" I ORIGINALLY PRINTED HERE WAS VACUOUS — CAUGHT BY THE SIDE
LANE, VERIFIED BY ME, RECORDED RATHER THAN QUIETLY DELETED.** This section read
*"Sixteen cells are fitted exactly by two parameters… no residual"*, followed by
three ✓ marks. **It consumes exactly two observed quantities and solves for
exactly two free parameters** — `t = (a+b−1)/2`, `s = a−t`. **It is saturated:
zero degrees of freedom, and it fits ANY pair of numbers with zero residual.**

Driven to the other verdict, as the standing rule requires:

```
a=0.5193 b=0.4368 -> s=+0.5413 t=-0.0220   residual 0.00e+00
a=0.9000 b=0.1000 -> s=+0.9000 t=+0.0000   residual 0.00e+00
a=0.9900 b=0.9900 -> s=+0.5000 t=+0.4900   residual 0.00e+00
a=0.6509 b=0.0724 -> s=+0.7893 t=-0.1383   residual 0.00e+00
   WORST RESIDUAL OVER ALL PAIRS INCLUDING NONSENSE: 1.11e-16
```

**The sixteen cells are never touched by it. The three ✓ were the identity
restated, not a test of it.** *(And it contradicted §4 of this same document,
which reports a per-arm residual at χ²=15.93, p≈0.026 — "no residual" and "a
residual" on one question in one file.)* **The parameter values above stand as a
description; they were never evidence.**

## 2. ⛔ THE RULER IS **NOT** BENT — THE BALANCED DESIGN CANCELS IT

The leading reading offered was *"seat A is worth ~+8pp, so every pooled screen
verdict this project has produced was measured against a bent ruler."*
**That is false — and the demonstration is one line of algebra, not the fit in §1.**
*(The fit was my original argument for it. The fit is vacuous, §1; the conclusion
was right anyway and the correct ground is stronger. Side lane, s31.)*

Each arm plays **512 games in each seat**, so **arm `i`'s pooled rate is**

> `[(sᵢ + tᵢ) + ((1 − sᵢ) + tᵢ)] / 2 = 0.5 + tᵢ`

**`s` cancels identically.** Verified by driving it where the vacuous version
would have hidden a failure:

| condition | recovered `t` |
|---|---:|
| `s` = 0.541 as observed | **−0.02195** |
| `s` = 0.95 (huge seat advantage) | **−0.02195** |
| `s` = 0.30 (seat advantage REVERSED) | **−0.02195** |
| `s` = 0.50 (no seat advantage) | **−0.02195** |

⇒ **Each arm's pooled estimate is unbiased for its own `tᵢ` regardless of the
seat advantage's SIZE, its DIRECTION, and — critically — regardless of `s`
VARYING BETWEEN ARMS**, which is exactly the heterogeneity §4 of this document
measures and which my original fit-based argument would have had to explain away.

**It even survives a seat × treatment interaction.** With `t_A = −0.05` and
`t_B = +0.01`, the pooled figure recovers **−0.0200**, exactly the seat-averaged
effect `(t_A+t_B)/2` — **which is the estimand a screen wants anyway.**

**Pooled point estimates are unbiased. Past verdicts must not be repriced on
this** — and that claim is now independent of anything §3 or §4 does.

**And the power loss is negligible, which closes the other half of the worry.**
Blocking on seat moves the variance of the pooled proportion from
`p̄(1−p̄) = 0.2495` to the stratified `(p₁q₁+p₂q₂)/2 = 0.2478` — a **0.7%
variance reduction**. Binomial variance is flat near 0.5, so an 8 pp block shift
buys essentially nothing. **What seat-pooling actually costs is not power. It is
the ability to see an INTERACTION** — §4.

## ⛔⛔ §3 IS RETRACTED BY ITS AUTHOR, SAME SESSION, BEFORE ANY LANE ACTED ON IT — READ §3R FIRST

**§3 below concluded "the cause is the map set, and the platform settles it."
Both halves are wrong and §3R replaces them.** The text is kept intact rather
than edited away, because the *shape* of the error is the transferable part.

**What broke it:** I ran the control I should have run before publishing — the
same test on games **we are not in**.

* **§3's headline cell does not replicate.** The 8 battery maps read **52.71%
  (z=+2.33)** in our games but **51.76% (z=+1.01), NOT SIGNIFICANT**, in
  third-party games.
* **Per-map directions do not replicate at all.** `atoll` is **46.95% (z −0.99)**
  in our games and **61.75% (z +3.46)** third-party — *opposite directions, both
  notable.* `jackpot` 40.20% → 50.93%. `hive` 56.31% → 49.53%.
* ⇒ **The per-map bias is NOT a fixed property of the map, and "the 8 local maps
  are A-favouring, which explains the battery's 54.13%" is withdrawn.**

**⭐ AND THE METHOD ERROR IS THE THING TO CARRY, NOT THE NUMBER.** The local
battery is **our bot against a near-identical copy of itself**. That matchup
appears in **neither** platform population — the ladder has never played v104
against v104. **If seat asymmetry is a map × matchup interaction (§3R), then no
quantity of platform data can predict the local figure, because the platform does
not contain the population.** I reached for the platform because it had the
bigger n and did not ask whether it had the matchup. **The larger n made the
wrong population feel like the stronger evidence.**

**Direction of the error, named:** toward the **tidier** explanation. "It's the
map set" closed the question in one table.

**Operational consequence, corrected and relayed to the builder while their run
was live:** I told them a byte-identical null on the same 8 maps "discriminates
nothing." **That was wrong. It is the only instrument that can answer this**, and
it yields a seat baseline for the exact matchup and map set every local screen
runs in — a calibration constant this project has never had.

## 3. ⭐ THE CAUSE IS THE MAP SET, AND THE PLATFORM SETTLES IT — **⛔ RETRACTED, see above and §3R**

The obvious suspects were the engine (a team-A resolution-order advantage) and
the local harness (the battery ran 8-way parallel; TLE under contention). **It is
neither.**

| population | n | seat-A share | z vs 50% |
|---|---:|---:|---:|
| PLATFORM, **all maps** | 3,740 | **50.91%** | +1.11 |
| PLATFORM, **restricted to the 8 LOCAL maps** | 1,848 | **52.71%** | **+2.33** |
| LOCAL battery, same 8 maps | 8,192 | **54.13%** | +7.47 |
| **LOCAL − PLATFORM, same maps** | | **+1.42 pp** | **+1.10 — n.s.** |

**Once you condition on the map set, the local harness is statistically
indistinguishable from the platform**, which runs the same engine with no
contention and no local harness at all.

**⚠ THIS CUT INVERTED MY OWN FIRST CONCLUSION AND THE RECORD SHOULD SAY SO.** The
all-maps figure (50.91%, z=+1.11) had me about to report *"the platform shows no
seat effect, therefore it is the harness."* **The restricted cut reversed it.**
The all-maps number is diluted by maps the battery never used — including
strongly B-favouring ones — and **a pooled population that happens to balance is
not evidence of symmetry in its members.**

### 3b. THE UNDERLYING FACT, AND IT CONTRADICTS THE ORGANISERS' DOC

`CLAUDE.md` states maps are *"symmetric by reflection or rotation."* **The win
outcome on them is not symmetric.**

**Heterogeneity of seat-A share across the 15 platform maps with n ≥ 190:
χ² = 35.33, df = 14, p = 0.0013** (expected χ² under per-map symmetry = 14).

| A-favouring | share | | B-favouring | share |
|---|---:|---|---|---:|
| fjordgate | 59.0% (z +2.58) | | jackpot | 40.2% (z −2.80) |
| saga | 58.4% (z +2.57) | | vault (n=20) | 25.0% |
| meander | 56.9% (z +2.10) | | quarry (n=18) | 16.7% |
| hive | 56.3% (z +1.88) | | | |

**Six of the eight local-battery maps are the A-favouring ones.** That, not the
engine and not contention, is most of the 8/8.

**⚠ CAVEAT, and it is not decorative:** geometric symmetry and outcome symmetry
are different claims, and this measures only the second. A geometrically
symmetric map can still favour a seat through resolution order interacting with
that geometry. *(INFERENCE — I have measured that outcomes differ by map; I have
not measured why, and no mechanism here is established.)*

## 3R. WHAT REPLACES §3 — THE THIRD-PARTY CONTROL, AND WHAT IT DOES AND DOES NOT SETTLE

**Population: games we are NOT in.** `corpus/league_matches.tsv` (`scoreA`/`scoreB`
per match) for the pooled test; `corpus/league_games.tsv` for the per-map test.

### 3R-a. ⭐ THERE IS NO ENGINE-LEVEL SEAT ADVANTAGE. THIS IS THE STRONGEST NUMBER HERE AND NOTHING BELOW WEAKENS IT.

| population | matches | games | seat-A share | z vs 50% |
|---|---:|---:|---:|---:|
| **THIRD-PARTY (every match we are not in)** | 35,578 | **177,618** | **50.137% ± 0.233pp** | **+1.16** |
| our own matches | 748 | 3,740 | 50.909% ± 1.602pp | +1.11 |
| all matches | 36,326 | 181,358 | 50.153% ± 0.230pp | +1.31 |

**The engine is seat-symmetric to a quarter of a percentage point.** A team-A
resolution-order advantage is dead as a hypothesis.

### 3R-b. MAP-LEVEL HETEROGENEITY IS REAL AND REPLICATES ON AN INDEPENDENT POPULATION

| population | maps (n≥190) | χ² | df | p |
|---|---:|---:|---:|---:|
| our games | 15 | 35.33 | 14 | 0.0013 |
| **third-party** | 8 | **23.09** | **7** | **≈0.0017** |

**Seat outcomes genuinely differ by map, in two independent populations.**

### 3R-c. ⛔ BUT THE PER-MAP DIRECTIONS DO NOT REPLICATE — SO IT IS NOT A MAP PROPERTY

| map | our games | third-party |
|---|---:|---:|
| **atoll** | 46.95% (z −0.99) | **61.75% (z +3.46)** |
| jackpot | 40.20% (z −2.80) | 50.93% (z +0.27) |
| hive | 56.31% (z +1.88) | 49.53% (z −0.14) |
| drumlin | 52.30% (z +0.71) | 47.21% (z −0.78) |
| nordkap | 48.00% (z −0.60) | 47.72% (z −0.64) |

*(INFERENCE, the reading I now favour and have not established: this is a **map ×
matchup** interaction — different bots exploit the same geometry differently from
each seat — rather than a map-intrinsic bias. A heterogeneity that is real in
both populations but points different ways in each is what an interaction with
the *players* looks like.)*

### 3R-d. WHAT NOW EXPLAINS THE LOCAL 54.13%: **UNKNOWN, AND THE PLATFORM CANNOT SAY**

The battery is **our bot vs a near-identical copy of itself**, a matchup absent
from both platform populations. **Under 3R-c that makes platform data structurally
unable to predict it.** ⇒ **The byte-identical local null IS the discriminating
instrument** — it measures the seat baseline in the matchup every local screen
actually runs in. A B-favouring-map shard (locally: `jackpot`) now asks a changed
question: not *maps vs harness*, but *does the self-play seat asymmetry track the
map at all?*

### 3R-e. LIMITS OF THE THIRD-PARTY PER-MAP CUT — stated because they are severe

`league_games.tsv` is **stale (newest `createdAt` 2026-08-09T05:12Z, ~2 days
old)** and covers only **6 third-party teams**. With so few teams, matchup
composition drives the per-map cells heavily — which is *consistent with* 3R-c's
interaction reading but cannot be used as evidence *for* it without circularity.
**The pooled 177,618-game result (3R-a) does not depend on this file and is
unaffected.**

## 4. WHAT SURVIVES AND IS WORTH SPENDING ON: SEAT × ARM INTERACTION

Per arm, `(A−B)/512` estimates `2s−1` and is **constant at 8.25 pp if no arm
interacts with seat**. Deviations from that, SE = 3.125 pp:

| arm | (A−B)/512 | deviation | z |
|---|---:|---:|---:|
| heal | 8.59 | +0.34 | +0.11 |
| noseal | 2.54 | −5.71 | −1.83 |
| nohome | 3.32 | −4.93 | −1.58 |
| roster | 7.62 | −0.64 | −0.20 |
| cap6 | 7.62 | −0.64 | −0.20 |
| bestfit | 11.33 | +3.08 | +0.99 |
| gunaxis | 7.42 | −0.83 | −0.27 |
| **ferryfirst** | **17.58** | **+9.33** | **+2.99** |

**Heterogeneity: χ² = 15.93 on 7 df, p ≈ 0.026.** The arms do differ in seat
interaction. **Ferry-first reads 304/512 = 59.4% on seat A against a 54.1%
seat-A null, and its pooled 50.6% "NO-INFORMATION" verdict is the average of a
possible real seat-A effect and nothing.**

**⛔ IT IS THE LARGEST OF EIGHT, SELECTED AFTER THE FACT.** Bonferroni across the
eight gives p ≈ 0.024 — it survives, barely. **This is a HYPOTHESIS deserving a
pre-registered seat-stratified re-run of ferry-first. It is not a finding and
this document does not call it one.**

## 5. THE CONTROL THAT WOULD DISCRIMINATE, AND THE ONE THAT WOULD NOT

A byte-identical null run on **the same 8 maps** returns ~54% seat A and
**discriminates nothing** — the platform already shows those maps doing that with
zero contention. It confirms an effect whose cause it cannot address.

⇒ **Run part of the null on the platform's B-FAVOURING maps.** If the local
harness reproduces the **B**-favouring direction there, the map explanation is
confirmed and the harness is clean. If it still shows **A**, there is a
harness/contention effect on top of the map effect. **Same cost, and unlike the
same-maps version it can come out the other way.**

## 6. WHAT THIS DOES *NOT* SAY

* It does **not** invalidate any pooled verdict from a seat-balanced battery (§2).
* It does **not** establish a mechanism for the map asymmetry (§3R-c), and it no
  longer claims the map set explains the local 54.13% (§3 retracted).
* It does **not** identify what *does* explain the local 54.13% (§3R-d). That is
  open, and the local null answers it.
* It does **not** promote ferry-first (§4).
* The per-map platform cells are thin (n ≈ 200–260 for the big maps, n < 30 for
  the tail); **`quarry` at 16.7% is n=18 and is quoted as colour, not evidence.**
  The χ² uses only the 15 maps with n ≥ 190.
* PLATFORM pools our versions and opponents. That is legitimate for a **seat-
  symmetry** question, which is a property of the engine and map rather than of
  either bot, but it would not be legitimate for a strength question.
