# RESULT — the LOKI-2 committed opening COSTS core-kill share, and my prediction was wrong in direction

Answers `docs/PREREG-rush-map-interaction-2026-08-09.md` (`19b8da3`, committed
before any game ran). **Separate dated doc, per the prereg — the prereg is not
amended.**

## 1. MY PRE-REGISTERED PREDICTION FAILED ON EVERY CLAUSE

I predicted: *"`LOKI2_RUSH_ON` improves `core_kill_share` on the SHORT band and
is neutral-or-negative on the LONG band."* The mechanism I argued from was free
arithmetic — the rush recipe is 3 turrets by r22, a builder walks 1 tile/round,
so on `hive` (36 Manhattan) the recipe is physically unreachable.

**Measured: the rush is HARMFUL, and the harm is concentrated on the SHORT band
— the band I predicted it would help.** The LONG band, where I predicted harm,
is null in both opponents. Recording this at the top because a prediction that
fails is the only thing pre-registration buys, and burying it under the result
would waste the purchase.

## 2. THE RESULT — PRIMARY CURRENCY, TWO INDEPENDENT UNSATURATED OPPONENTS

`_det_v118lokinorush` (rush OFF) vs `_det_v118loki2b` (rush ON), paired
deterministic, same (map, seed, seat) triples, 15 maps × 3 seeds × 2 seats,
`--tle 0`, **0 tracebacks in 360 games**, gate CLEARED with control equivalence
identical 12/12.

| opponent | band | rush ON | rush OFF | delta | paired flips (ON-only / OFF-only) | sign test |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| **orizon_probe** | SHORT | 27.1% | **62.5%** | **−35.4pp** | 3 / 20 | **p = 0.0005** |
| | LONG | 78.6% | 71.4% | +7.1pp | 6 / 3 | p = 0.51 (null) |
| | **ALL** | 51.1% | **66.7%** | **−15.6pp** | 9 / 23 | **p = 0.0201** |
| **cad_probe** | SHORT | 56.2% | **79.2%** | **−22.9pp** | 4 / 15 | **p = 0.0192** |
| | LONG | 57.1% | 71.4% | −14.3pp | 3 / 9 | p = 0.15 (null) |
| | **ALL** | 56.7% | **75.6%** | **−18.9pp** | 7 / 24 | **p = 0.0033** |

**It replicates across two opponents that share no lineage with each other** —
Orizon is a point-blank gunner core battery, CAD a sentinel siege. Both agree on
sign, both are significant overall, and in both the SHORT band carries it.

## 3. WHY THE EARLIER READ SAID THE OPPOSITE — A SATURATED INSTRUMENT

The same ablation against `ouroboros_probe` returned **95.8% / 100.0%
core-kill share** and NO VERDICT. That was not the rush working; it was the
instrument having no headroom. Measured baseline for `_det_v118loki2b`, 30
games each, all 15 maps, both seats:

| probe | win rate | usable as an instrument? |
| --- | ---: | --- |
| clanker_probe | 96.7% | **NO — saturated** |
| ouroboros_probe | 93.3% | **NO — saturated** |
| cad_probe | 66.7% | yes |
| **orizon_probe** | **50.0%** | **yes — best resolution in the pool** |

**This is a standing instrument rule now, not an observation about one battery:
a plank measured only against `ouroboros_probe` or `clanker_probe` has not been
measured.** My own rush battery reached NO VERDICT for exactly this reason and I
chose that opponent myself.

## 4. WHAT I AM AND AM NOT CLAIMING

**Claimed:** against two unsaturated foreign proxies, turning the LOKI-2
committed opening OFF **raises** core-kill share, replicated, paired, with
consistent sign and p = 0.02 / p = 0.003 on the overall sign tests. The effect
is concentrated on short maps.

**NOT claimed, and each of these is a real limit:**
- **Effect SIZE is not readable off these legs.** Both runs flagged **LOW
  REPLICATION — 90 pairs collapsing to 42/43 distinct shapes.** The paired sign
  tests on flips are the robust part; the percentage-point deltas are not.
- **Two probe opponents are not the ladder.** Published amputation work puts
  ~2× inflation on proxy results and reports outright sign flips.
- **Band is confounded with map identity**, not merely distance — 8 short maps
  and 7 long ones also differ in terrain, ore and symmetry class. The distance
  story is the hypothesis; the interaction is what was measured.
- **A mechanism for the sign is not established.** The plausible one — on short
  maps you arrive fast anyway, so waiving the harvester prerequisite and cutting
  the bank floor 40→8 buys nothing and costs the economy that would have
  followed up; on long maps the walk is slow enough that the economy matures
  regardless — is a story I find coherent and have **not** tested.

## 5. CONSEQUENCE FOR THE QUEUE

**Queue item 4 (the map/opponent gate on the rush) is ANSWERED, with the
opposite sign to the one I proposed.** A gate is warranted — but it should
**suppress the rush on SHORT maps**, where it measurably costs share, and may
leave it on the LONG band, where both opponents read null. The simplest form is
not a gate at all: the ablation arm that beats the incumbent is
`LOKI2_RUSH_ON = False` outright.

**This bears on a plank that already passed.** LOKI-2's committed opening was
verdicted on `time_to_core_kill` (median core-kill turn 198 → 163). That is the
**secondary** currency, and the ladder says it was not the bottleneck. **This
result says the same plank costs the PRIMARY one.** I am not retracting LOKI-2b
— its own plank was the live-census defect fix, which is separately sound and
is not what is measured here — but **the rush inside it now has evidence
against it and should not be carried forward unexamined.**

---

## ADDENDUM — REAL-ENGINE FIDELITY READ (S5), added 2026-08-09 after the offline result

**Match `dfc4b892`, `fcode match test`, real engine with REAL TLE ENFORCEMENT,
`rated: false`, elo deltas null — no rating exposure and no slot swap.**

`_v120loki4` (rush OFF, side A) vs `_v118loki2b` (rush ON, side B):

| map | winner | condition | turns |
| --- | --- | --- | --- |
| moonrise | **a — LOKI-4** | core_destroyed | 235 |
| eider | **a — LOKI-4** | core_destroyed | 249 |
| heart | **a — LOKI-4** | core_destroyed | 245 |
| hive | b — LOKI-2b | core_destroyed | 319 |
| atoll | **a — LOKI-4** | core_destroyed | 155 |

**`scoreA = 4, scoreB = 1`. All five games decided by `core_destroyed` — no
tiebreaks, so every game is denominated in the PRIMARY currency.**

**WHY THIS LEG WAS WORTH RUNNING EVEN THOUGH n=5 CANNOT CONFIRM ANYTHING.**
Every offline number above was measured at `--tle 0`, which removes CPU-kill
nondeterminism by construction. Real games run a 10 ms per-unit budget where an
overrun truncates a turn **silently** — LOKI-1's DESIGN records a retracted
result (48.3% → 62.2%, same pairing) caused by exactly that. So the offline
result had a live failure mode it could not see, and this leg closes it: **the
direction survives real TLE.**

**WHAT IT IS NOT.** 4–1 at n=5 is **binomial p = 0.1875 one-sided — NOT
significant on its own**, and I am not quoting it as confirmation. Its value is
(a) fidelity, above, and (b) directional agreement with the offline result,
which is the part carrying real weight (two independent unsaturated probes,
paired sign tests p = 0.0201 and p = 0.0033). **A 4–1 that had gone the other
way would have been informative; a 4–1 that agrees is corroboration, not proof.**
The `hive` loss is consistent with the offline LONG-band null.

**Standing caveat unchanged:** this is still our own tree against our own tree.
It says the rush costs share *relative to LOKI-2b*. It does not say LOKI-4 is
better against the field, and only the ladder can say that.
