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

**Sixteen cells are fitted exactly by two parameters:**

| parameter | value |
|---|---:|
| seat advantage `s` = P(A wins \| equal bots) | **54.126%** |
| treatment effect `t`, pooled over the eight arms | **−2.195 pp** |

Check: treatment-on-A = `s+t` = 51.93% ✓ · treatment-on-B = `(1−s)+t` = 43.68% ✓
· pooled = 47.80% ✓.

## 2. ⛔ THE RULER IS **NOT** BENT — THE BALANCED DESIGN CANCELS IT

The leading reading offered was *"seat A is worth ~+8pp, so every pooled screen
verdict this project has produced was measured against a bent ruler."*
**That is false, and the fit above is the demonstration.**

Each arm plays **512 games in each seat**. A seat advantage enters `s+t` and
`(1−s)+t` with opposite sign and **cancels exactly** in the pooled mean — which
is precisely what seat-balancing is for. The decomposition recovers `t = −2.195pp`
**through** an 8.25pp seat spread with no residual. **Pooled point estimates are
unbiased. Past verdicts must not be repriced on this.**

**And the power loss is negligible, which closes the other half of the worry.**
Blocking on seat moves the variance of the pooled proportion from
`p̄(1−p̄) = 0.2495` to the stratified `(p₁q₁+p₂q₂)/2 = 0.2478` — a **0.7%
variance reduction**. Binomial variance is flat near 0.5, so an 8 pp block shift
buys essentially nothing. **What seat-pooling actually costs is not power. It is
the ability to see an INTERACTION** — §4.

## 3. ⭐ THE CAUSE IS THE MAP SET, AND THE PLATFORM SETTLES IT

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
* It does **not** establish a mechanism for the map asymmetry (§3b).
* It does **not** promote ferry-first (§4).
* The per-map platform cells are thin (n ≈ 200–260 for the big maps, n < 30 for
  the tail); **`quarry` at 16.7% is n=18 and is quoted as colour, not evidence.**
  The χ² uses only the 15 maps with n ≥ 190.
* PLATFORM pools our versions and opponents. That is legitimate for a **seat-
  symmetry** question, which is a property of the engine and map rather than of
  either bot, but it would not be legitimate for a strength question.
