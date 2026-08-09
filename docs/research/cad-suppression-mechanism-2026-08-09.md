# The CAD suppression MECHANISM: what their builders do instead of building

**Research arm, 2026-08-09.** Read-only with respect to the bot; no arena, no
`fcode` submit/activate; **zero replay downloads** — every byte read was already
on disk.

**Verdict in one line: HEALER DISPLACEMENT IS REAL, IS THE LARGEST SINGLE NAMED
EFFECT, AND EXPLAINS AT MOST ~18% OF THE SUPPRESSION. The aggregate arithmetic
closes to 1.00 and that closure is a coincidence — the bots that start healing
are not the bots that stop building. 82% of the missing builds are a per-turn
build-propensity collapse in builders that are OFF the heal collar, hold money,
are alive, are running, and are not on cooldown, and their missing turns go to
IDLE. What CAD's builders are doing instead is: coming home and standing still.**

---

## VERSION TAG AND PROVENANCE

Live ladder slot **v94 = `bots/_v115dodge`, treehash `6ae6871c`**.
Corpus git sha as commissioned: **`7418e13`**. The keeper daemon had moved past
that before I froze: `corpus/manifest.json` at freeze read `git_sha a676ca4`,
`archive_replays 6513`, built `2026-08-09T15:02:02Z`. Repo HEAD during the run
went `91b85bf` → `b84889e`. Both are recorded rather than reconciled, because —
as in the lockout cut — **the analysis does not read the corpus tables**: the
corpus carries no damage stream and no `builderHeal`, so both load-bearing
quantities (when CAD's core was first hit; what each builder did each round) come
from a fresh decode of the archived replays.

**The archive grew from 6,513 to 6,593 `.replay26` files during the run**, which
is exactly why the freeze exists.

### Frozen inputs — `scratchpad/cad-mechanism-freeze/` (own subdirectory, nothing else touched)

| file | rows | md5 |
| --- | ---: | --- |
| `corpus/join.tsv` (copied) | 1,445 | `e943d4ac38e5339ac7c577263b9156cf` |
| `corpus/manifest.json` (copied) | — | `c77d7a4a4971ee3606a8e6904d896fa0` |
| `cad_population.tsv` (derived) | 225 | `0c6edce2c1fcceded52c8293c06a2afd` |
| `replay_md5.txt` — md5 of every replay read | 225 | `f5408e22f07cf7574eec4f9eff491e29` |
| `mech_rounds.tsv` (derived) | 88,066 | `99092fe4329b2a727e6c4e4123758179` |

**All 225 frozen replays were re-md5'd after the run: 225/225 unchanged.**

### Scripts — `docs/research/scripts/cad-suppression-mechanism-2026-08-09/`

| script | md5 (8) | what |
| --- | --- | --- |
| `mech_decode.py` | `47ad5d95` | the builder-turn ledger decoder |
| `analyse.py` | `451044a5` | landmark, ledger, predictions 1-3, alternatives, version/opponent splits |
| `probe.py` | `f9ee7355` | seat split, fixed-cohort trace (prediction 4), contemporaneous cut, invariants |
| `decompose.py` | `8f3154df` | shift-share, idle-by-cooldown, geography, money-matched cut, within-match pairing |
| `validate.py` | `2dfe4078` | seat reconciliation, all-zero sweep, lockout reproduction, build-stream cross-check |

`cad_population.tsv` is produced by the lockout cut's own
`docs/research/scripts/cad-lockout-2026-08-09/population.py`, reused unmodified,
per the commission. Run order in `README.md`.

### The population, and its version distribution

**225 CAD game files across 45 matches** (the lockout cut's 220/44 plus one new
match), attributed entirely from `<match-id>.meta.json` — `join.tsv` sees only
85 of them. **120 of the 225 are CAD against a third party**, i.e. games our own
bot is not in.

| CAD version | all games | in the DAMAGED cell (r14-40) | in the undamaged cell |
| --- | ---: | ---: | ---: |
| v107 | 40 | 11 | 29 |
| v116 | 10 | 0 | 10 |
| v117 | 50 | 15 | 35 |
| v118 | 5 | 1 | 4 |
| v120 | 45 | 11 | 34 |
| v123 | 25 | 2 | 23 |
| v124 | 50 | 13 | 35 |

Opponents: OpenSverige 105, Powered by SmartFridge 45, gsxWins 20, Askar City 10,
Ouroboros 10, LingLing40 10, Powerpuff Girls / Team 48 / Memtrace /
Lunds Stallions / arsonist duck 5 each. **The DAMAGED cell is 53 games from
32 matches and 5 distinct opponents.**

**Nothing is pooled across versions in the headline** — §7 reports the effect per
version and it is present in every version that has a damaged cell.

---

## THE HYPOTHESIS AS HANDED OVER

`docs/reference/official-docs.md:481` and `:1455`: for a builder bot, **acting
and moving are mutually exclusive per round**. A heal is an action. **So a
builder healing the core is a builder not building.**

Two measurements made this the natural candidate.
`opponent-collar-heal-staffing-2026-08-09.md`: CAD is the garrisoner — 39.3% of
rounds have ≥1 CAD bot on its own 8 heal-capable collar seats, ~22.3 core heals
per game, **42.3% of all its heals land on its own core**.
`core-kill-incidence-cut-2026-08-09.md` §4b measured the same physics on our
side: a builder orthogonally adjacent to our own **damaged** core moves 15.5% of
rounds against 68.3% at full HP (n=143,812), and the suppression is gone one tile
further out.

**Hypothesis: early core damage pulls CAD's builders onto collar seats to heal,
and every heal round is a round they do not build.**

---

## LANDMARK DESIGN — inherited, unchanged

CAD's opening is a byte-identical script (185 forward-ferry throws, all in r2-r5,
zero after r5, on all 15 maps), so a within-game before/after contrast measures
the script and not the damage. **Every cell in this document is a landmark:
CAD's behaviour over the SAME ABSOLUTE ROUND WINDOW, compared between games where
core damage had already landed before the window opened and games where it had
not.** Games that did not reach the window's end are excluded, so every game in a
cell contributes the same number of rounds. **No before/after contrast appears
anywhere in this document.**

**The unit of measurement is the BUILDER-TURN.** For every CAD builder bot alive
at the start of a round, exactly one label is assigned from that round's event
stream: `heal_core` / `heal_bldg` / `heal_bot` / `heal_other` / `build` /
`attack` / `thrown` / `move` / `died` / `idle`. Because acting and moving are
mutually exclusive, these partition the bot's turn. Bots born mid-round are
excluded (a unit created mid-round does not act that round).

---

## VALIDATION

**Seat.** meta.json's `teamA == OpenSverige` must independently predict
`join.tsv`'s reconciled `our_team` on every game in both sources:
**85 agree, 0 disagree.**

**Trap 2, the two's-complement varint.** `_s64()` sign census over the whole
population: **99,841 negative, 75,121 positive, 0 zero.** Both signs present, so
the correction is not silently zeroing damage the way the `1<<32` bug once did.

**Trap 1, the rotate re-emit — and the two build streams reconcile exactly.**
A build is the FIRST `placeEntity` carrying an id. Independent check:
first-`placeEntity` builds **13,030** minus `BuilderBuild` (Update 16) events
**10,546** = **2,484**, and CAD's builder-bot placements (which the core spawns,
not a builder) = **2,484**. **Residual 0.**

**The ledger partitions.** Labelled builder-turns **504,863** vs builder-turns
available **504,863**, difference **0**; 0 violating rounds of 88,066. Seat +
off-collar equals total for every one of the ten labels (all differences 0).

**The lockout landmark reproduces.** Published (n=220 archive): r14-40 damaged
mean **1.0**, 31% zero; undamaged **7.4**, 2% zero. This decoder (n=225 archive):

| window | cell | n | mean builds | median | ZERO |
| --- | --- | ---: | ---: | ---: | ---: |
| r14-25 | damaged | 53 | 0.38 | 0 | 35/53 (66%) |
| r14-25 | undamaged | 172 | 4.11 | 4 | 14/172 (8%) |
| r14-40 | **damaged** | **53** | **1.00** | 1 | **16/53 (30%)** |
| r14-40 | undamaged | 170 | **7.32** | 7 | 4/170 (2%) |

**Cooldown reconstruction, validated.** Action/move cooldowns are rebuilt from
`setActionCooldown` / `setMoveCooldown` plus the placeEntity seed, decremented at
end of round. Invariant: a bot that acted must have had `action_cd == 0` at round
start, a bot that moved `move_cd == 0`. **0 violations in 34,363 acting turns and
0 in 374,440 moving turns.**

**All-zero column sweep** (an exact zero is a bug signature before it is a
finding). Eight columns are all-zero; every one is structural, and each was
checked rather than assumed:

| column | why it is zero |
| --- | --- |
| `L_heal_other`, `S_heal_other`, `O_heal_other` | `can_heal` only permits a tile holding a friendly entity, so every heal lands on core / own building / own bot. **This is a correctness signal.** |
| `O_heal_core` | **structural confirmation of the ORTH8 seat definition** — only a bot orthogonally adjacent to the footprint can heal the core, and "off-collar" means not on ORTH8. The footprint-standing edge case (max 1 bot in 4 of 85 games, per the collar census) does not occur here. |
| `idle_acd`, `idle_mcd` | a builder-bot cooldown of 1 always clears by the next round start, so **every** builder-turn in these windows is free to act. Not a bug — and it is what makes `idle` unambiguous. |
| `tled_n` | CAD never exceeds its CPU budget. **Parse verified**: the same field-4 read finds 3 TLEs in 292,693 botOutput events across a 40-game both-teams census, so it detects TLEs where they exist. |
| `b_splitter` | neither CAD nor its opponents build splitters — an independent 60-game entity census returns 0 splitters for both sides (corpus-wide splitters are ~208 builds). Used in no conclusion. |

---

## RESULT 1 — PREDICTION 1: collar occupancy IS higher. CONFIRMED.

Window r14-40, ORTH8 seats, start-of-round snapshot, distinct seats:

| cell | n | collar seats/round | rounds with ≥1 seat occupied |
| --- | ---: | ---: | ---: |
| **DAMAGED before r14** | 53 | **1.481** | **79.9%** |
| undamaged at r14 | 170 | 0.700 | 45.5% |

**2.1× the seat occupancy and 1.8× the share of rounds staffed.** The direction
and the magnitude are both what the hypothesis asked for.

## RESULT 2 — PREDICTION 2: core heals ARE higher. CONFIRMED.

| window | cell | n | core-heal events / game | non-core heals / game |
| --- | --- | ---: | ---: | ---: |
| r14-40 | **DAMAGED** | 53 | **9.64** | 0.11 |
| r14-40 | undamaged | 170 | 3.44 | 0.66 |
| r41-80 | DAMAGED | 121 | 10.41 | 0.99 |
| r41-80 | undamaged | 88 | 1.32 | 1.65 |

**+6.20 core heals per game in r14-40, a 2.8× rate.** Note the second column
already separates the REBUILDING alternative: non-core heals are *lower* in the
damaged cell, not higher.

## RESULT 3 — PREDICTION 3: the arithmetic. **PARTIAL — and the naive closure is a trap.**

### The aggregate closes to 1.00, and that is the wrong answer

| window | missing builds | Δ core heals | Δ non-core heals | Δ attacks | Δ moves | Δ idle turns | Δ builder-turns |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| r14-25 | +3.73 | +3.28 | −0.12 | +0.88 | −8.30 | +6.35 | −1.4 |
| **r14-40** | **+6.32** | **+6.20** | −0.55 | +2.19 | −17.22 | **+11.57** | −4.0 |
| r26-45 | +3.83 | +6.25 | +0.00 | +0.65 | −2.83 | +10.18 | +10.5 |
| r41-80 | +3.02 | +9.07 | −0.66 | +0.03 | +7.58 | +22.02 | +35.2 |
| r81-120 | +1.88 | +8.81 | −0.94 | −0.25 | +3.95 | +16.57 | +26.6 |

At r14-40 CAD loses **6.19 build turns** and gains **6.20 core-heal turns** — a
ratio of **1.00**. Taken at face value this reads as *complete* closure. **It is
not, and the commission's own warning is what caught it: a partial explanation
dressed as complete is not a good result.**

### The bot-level ledger refutes the closure

Splitting the same builder-turns by whether the bot **started the round on a
collar seat**:

**ON a collar seat at round start**

| cell | builder-turns | heal_core | build | attack | move | idle |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| DAMAGED | 40.0 | 9.64 (24.1%) | 0.28 (0.7%) | 1.26 | 15.15 (37.9%) | 13.53 (33.8%) |
| undamaged | 18.9 | 3.44 (18.2%) | 0.51 (2.7%) | 0.12 | 9.74 (51.5%) | 4.82 (25.5%) |

**OFF the collar at round start** (these bots *cannot* heal the core — `O_heal_core` is 0 by construction and measures 0 in fact)

| cell | builder-turns | heal_core | build | attack | move | idle |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| DAMAGED | 72.1 | 0.00 | **0.58 (0.8%)** | 3.00 (4.2%) | 44.42 (61.6%) | 23.92 (33.2%) |
| undamaged | 97.2 | 0.00 | **6.56 (6.8%)** | 1.95 (2.0%) | 67.05 (69.0%) | 21.06 (21.7%) |

**All 9.64 heal turns are on the collar, and the collar's build turns fell by
only 0.23 (0.51 → 0.28). The 5.98 missing build turns are off-collar, in bots
that are structurally incapable of healing the core.** The two quantities that
appeared to cancel belong to disjoint populations of bots.

### Shift-share: the honest number is 18%

Builds = Σ(builder-turns in group) × (build rate per turn in group), groups =
{collar, off-collar}:

| cell | group | turns/game | builds/game | build rate/turn |
| --- | --- | ---: | ---: | ---: |
| DAMAGED | collar | 40.0 | 0.28 | 0.71% |
| DAMAGED | off | 72.1 | 0.58 | 0.81% |
| undamaged | collar | 18.9 | 0.51 | 2.68% |
| undamaged | off | 97.2 | 6.56 | 6.75% |

- undamaged builds/game **7.06**, DAMAGED **0.87** → gap **6.20**
- counterfactual (DAMAGED body distribution, UNDAMAGED per-turn rates): **5.94**
- **COMPOSITION — bodies relocated onto the collar: −1.13 = 18% of the gap**
- **RATE — the same bodies building less per turn: −5.07 = 82% of the gap**
  (of which off-collar alone −4.28)

**18% is the most generous accounting healer displacement can be given**, because
the composition term credits healing with *every* build a relocated bot would
have made, including the ones it would have missed anyway.

### Dose-response inside the damaged band gives an even smaller number

53 damaged games, window r14-40:

- Spearman(core heals, builds) = **−0.479** — more healing does go with less
  building, so the mechanism is not absent.
- but: **heals ≤ median → mean 4.2 core heals, 1.29 builds. heals > median →
  mean 15.8 core heals, 0.68 builds.** An extra **+11.6** heals buys **−0.61**
  builds: about **0.05 builds lost per heal**, not 1.
- **The decisive cell: damaged games whose core-heal count is essentially the
  undamaged baseline (4.2 vs 3.44) still build 1.29 against 7.32 — 82% of the
  full suppression is present with no extra healing at all.**

**PREDICTION 3 VERDICT: PARTIAL. Healer displacement accounts for ~18% by
shift-share and ~5-10% by dose-response. The arithmetic does NOT close.**

## RESULT 4 — PREDICTION 4: recovery timing. **PARTIALLY MET.**

Cohort fixed at r14 (`EARLY` = first CAD core damage ≤ r13, n=53;
`LATE/NEVER` = still undamaged at r14, n=172), then traced. A re-sorted
"damaged before window" cell changes membership every window and cannot show
timing.

| window | cohort | n | builds | core heals | collar seats/rd | %rd collar≥1 | idle/rd | med Ti |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| r14-25 | EARLY | 53 | 0.38 | 4.15 | 1.498 | 79.4% | 1.34 | 24 |
| r14-25 | LATE | 172 | 4.11 | 0.87 | 0.590 | 42.4% | 0.82 | 46 |
| r26-40 | EARLY | 53 | 0.62 | 5.49 | 1.467 | 80.4% | 1.42 | 26 |
| r26-40 | LATE | 170 | 3.16 | 2.56 | 0.787 | 47.9% | 1.08 | 41 |
| r41-60 | EARLY | 49 | 1.43 | 6.57 | 1.405 | 73.5% | 1.41 | 20 |
| r41-60 | LATE | 166 | 4.04 | 2.70 | 0.757 | 46.7% | 1.11 | 52 |
| r61-80 | EARLY | 45 | 1.18 | 5.98 | 1.319 | 71.7% | 1.51 | 21 |
| r61-80 | LATE | 164 | 4.52 | 2.54 | 0.681 | 44.2% | 1.06 | 56 |
| r81-120 | EARLY | 34 | 3.85 | 9.32 | 1.183 | 67.3% | 1.37 | 26 |
| r81-120 | LATE | 149 | 7.99 | 5.31 | 0.610 | 42.5% | 0.91 | 91 |
| r121-200 | EARLY | 26 | 10.27 | 8.12 | 0.900 | 56.0% | 1.20 | 42 |
| r121-200 | LATE | 119 | 14.72 | 8.87 | 0.567 | 43.9% | 0.84 | 118 |
| r201-300 | EARLY | 19 | 12.21 | 7.84 | 0.771 | 50.8% | 0.92 | 122 |
| r201-300 | LATE | 84 | 13.57 | 6.27 | 0.516 | 41.0% | 0.83 | 149 |

As EARLY/LATE ratios:

| window | build ratio | core-heal ratio | collar ratio |
| --- | ---: | ---: | ---: |
| r14-25 | **0.09** | **4.79** | 2.54 |
| r26-40 | 0.20 | 2.14 | 1.86 |
| r41-60 | 0.35 | 2.43 | 1.86 |
| r61-80 | 0.26 | 2.35 | 1.94 |
| r81-120 | 0.48 | 1.76 | 1.94 |
| r121-200 | 0.70 | **0.92** | 1.59 |
| r201-300 | **0.90** | 1.25 | **1.49** |

**Where it agrees:** the heal excess is largest exactly where the build gap is
largest (4.79× at r14-25 against a build ratio of 0.09) and decays as the build
gap closes.
**Where it fails:** the **collar excess never returns to baseline** — still 1.49×
at r201-300 when the build ratio has recovered to 0.90 — and the **heal excess is
gone by r121-200 (0.92) while a 30% build deficit remains.** The two clocks
overlap but do not coincide.

**PREDICTION 4 VERDICT: PARTIALLY MET.** Directionally concordant early,
divergent late in both directions.

## RESULT 5 — the contemporaneous physics, which is where the mechanism actually lives

Not a landmark; every round in r6-300 pooled, keyed on CAD's own core HP at round
start.

| CAD core HP at round start | rounds | P(a build happens) | P(a core heal) | builder-turns | %heal_core | %build | %move | %idle | collar seats/rd |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 500 (full) | 19,166 | 0.228 | 0.000 | 89,593 | 0.0% | **4.9%** | 73.9% | **16.9%** | 0.322 |
| 450-499 | 5,448 | 0.162 | 0.152 | 27,416 | 3.0% | 3.1% | 71.0% | 18.7% | 0.711 |
| 400-449 | 6,391 | 0.146 | 0.141 | 32,537 | 2.8% | 2.8% | 70.1% | 19.7% | 0.734 |
| 300-399 | 8,853 | 0.149 | 0.174 | 46,237 | 3.3% | 2.7% | 70.7% | 20.4% | 0.946 |
| 200-299 | 4,652 | 0.077 | 0.294 | 20,718 | 6.6% | 1.6% | 63.2% | 26.1% | 1.285 |
| 100-199 | 3,661 | 0.079 | 0.358 | 16,559 | 7.9% | 1.6% | 58.2% | 30.7% | 1.267 |
| 1-99 | 1,512 | 0.050 | **0.535** | 6,522 | **12.4%** | **0.9%** | 52.1% | **33.5%** | 1.464 |

Monotone in both directions. But read the last row against the first: heal share
gains **+12.4pp** while build share loses only **−4.0pp**, and **idle gains
+16.6pp while move loses −21.8pp**. **The heal is eating the WALK, not the
BUILD.** The build loss is smaller than either.

---

## THE ALTERNATIVES — each tested, each with a verdict

### REBUILDING (repairing/replacing structures elsewhere) — **REFUTED**

| window | cell | n | CAD buildings lost | conveyors lost | conveyors built | harvesters built | barriers built | heals on own buildings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| r14-40 | DAMAGED | 53 | **0.53** | 0.06 | **0.11** | **0.09** | 0.09 | **0.11** |
| r14-40 | undamaged | 170 | 0.82 | 0.32 | 4.54 | 1.22 | 0.02 | 0.64 |
| r41-80 | DAMAGED | 121 | 1.05 | 0.45 | 3.79 | 0.95 | 0.03 | 0.93 |
| r41-80 | undamaged | 88 | 1.47 | 0.61 | 5.67 | 1.31 | 0.03 | 1.32 |

The damaged cell **loses fewer buildings** (0.53 vs 0.82), **rebuilds fewer**
(conveyors 0.11 vs 4.54, harvesters 0.09 vs 1.22) and **heals its own buildings
less** (0.11 vs 0.64). There is no repair programme to displace the builds into.
The missing builds are **the economy programme itself** — 6.04 of the undamaged
cell's 7.06 builds are conveyors + harvesters + builder bots.

Where the builds were, by distance from CAD's own core:

| window | cell | builds at d²≤20 | d² 21-64 | d² >64 |
| --- | --- | ---: | ---: | ---: |
| r14-40 | DAMAGED | 0.96 | 0.02 | 0.02 |
| r14-40 | undamaged | 4.87 | 2.03 | 0.42 |

The forward and mid-map chain vanishes **and** home building falls 5×. It is not
a relocation of building work.

### POVERTY — **REFUTED DIRECTLY, in money-matched cells**

The lockout cut refuted this with a map-level natural experiment (suppression 1.1
on rich no-dump maps vs 0.9 on broke dump maps). The direct per-round test agrees.
r14-40, every round pooled, `dmgd` = core already damaged at round start:

| CAD titanium at round | state | rounds | %build turns | %heal_core | %move | %idle |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 0-9 | dmgd | 410 | 7.52% | 8.83% | 53.0% | 32.9% |
| 0-9 | clean | 112 | **26.46%** | 0.00% | 56.7% | 29.2% |
| 10-29 | dmgd | 1,031 | 2.57% | 8.64% | 55.9% | 31.0% |
| 10-29 | clean | 613 | **17.83%** | 0.00% | 60.6% | 29.1% |
| 30-49 | dmgd | 909 | 1.94% | 8.31% | 54.8% | 31.8% |
| 30-49 | clean | 731 | **15.19%** | 0.00% | 63.1% | 28.4% |
| 50-99 | dmgd | 481 | 1.35% | 7.27% | 68.2% | 21.1% |
| 50-99 | clean | 1,096 | **14.63%** | 0.00% | 70.8% | 19.4% |
| 100+ | dmgd | 73 | 3.61% | 11.39% | 75.8% | 6.4% |
| 100+ | clean | 613 | **13.48%** | 0.00% | 79.8% | 5.0% |

**Inside every titanium bucket the damaged build rate is 4-11× lower.** At 50-99
Ti — enough for a builder bot, a harvester, or fifteen conveyors — it is 1.35%
vs 14.63%. Money is not the binding constraint. (Median per-round titanium is
lower in damaged games, 25 vs 46, so poverty *co-occurs*; it just does not
explain.)

### WALKING (repositioning / fleeing / converging) — **REFUTED**

Movement is *lower*, not higher: 53.2% of builder-turns in the damaged cell vs
66.2% undamaged (r14-40), and moves/game 59.7 vs 76.9. They are not walking
instead of acting. **They are doing neither.**

The one honest piece of the walking story is a homeward drift, which is real but
small:

| window | cell | collar (ORTH8) | corner d²≤2 | d² 3-20 | d² 21-64 | d² >64 | mean min d² |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| r14-40 | DAMAGED | 1.48 | 0.31 | 1.14 | 0.63 | 0.58 | **21.2** |
| r14-40 | undamaged | 0.70 | 0.23 | 1.23 | 0.85 | 1.29 | **70.5** |

About **0.7 builders per round move from the far half of the map onto the
collar**, and mean squared distance to their own core falls from 70.5 to 21.2.
That relocation *is* the 18% composition term already counted.

### BLOCKED / UNDER FIRE (killed and replaced, contested targets) — **REFUTED**

| window | cell | n | births | deaths | bots/round | botOutput/round | TLE/round |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| r14-40 | DAMAGED | 53 | 0.13 | 0.13 | 4.15 | 7.01 | 0.000 |
| r14-40 | undamaged | 170 | 0.26 | 0.14 | 4.30 | 6.65 | 0.000 |
| r41-80 | DAMAGED | 121 | 0.09 | 0.14 | 4.67 | 8.03 | 0.000 |
| r41-80 | undamaged | 88 | 0.44 | 0.33 | 3.78 | 6.76 | 0.000 |

Churn is not the answer: **deaths are identical** (0.13 vs 0.14 per game over 27
rounds) and *births are lower*, not higher. The bots are alive, the level is
flat, **their `run()` is executing** (7.01 unit-turns of output per round, more
than the undamaged cell) and **CAD never times out** (0 of 88,066 rounds).
Contested build tiles are also implausible in this direction: the damaged cell's
builders are **closer to their own core**, i.e. deeper in their own territory,
where a legal adjacent empty tile is easier to find, not harder.

### The fifth possibility, which is what the data actually shows: **THEY GO IDLE**

`idle` here is unambiguous. It is not cooldown:

| window | cell | idle turns/game | idle with both cooldowns 0 | idle blocked by a cooldown | %turns free to act |
| --- | --- | ---: | ---: | ---: | ---: |
| r14-40 | DAMAGED | 37.5 | **37.5** | 0 | 100.0% |
| r14-40 | undamaged | 25.9 | **25.9** | 0 | 100.0% |
| r41-80 | DAMAGED | 55.7 | 55.7 | 0 | 100.0% |
| r41-80 | undamaged | 33.6 | 33.6 | 0 | 100.0% |

**Every idle builder-turn in the window belongs to a bot that could have acted
and could have moved, and did neither.** (A builder-bot cooldown of 1 always
clears by the next round start, so 100% free-to-act is structural — which is
precisely what makes `idle` a policy observation rather than an engine artefact.)

Of the +11.57 extra idle turns per game at r14-40, **+8.71 are on the collar**
(13.53 vs 4.82) and **+2.86 off it** (23.92 vs 21.06). So the largest single
thing CAD's builders do differently after early core damage is **stand on a
collar seat doing nothing** — garrisoning, not healing. The heal is what a
garrisoned bot does on the ~24% of its turns when there is damage to heal.

**And the sharpest single cell in the document** — off-collar builder-turns only,
r14-40, restricted to rounds where CAD held ≥30 titanium:

| state | rounds | off-collar builder-turns | builds | build rate/turn | %move | %idle | %attack |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **dmgd** | 1,463 | 4,672 | **44** | **0.94%** | 68.9% | **26.4%** | 3.4% |
| **clean** | 2,440 | 8,944 | **738** | **8.25%** | 69.7% | **18.7%** | 2.8% |

Bots that **cannot heal the core**, with **money in the bank**, **not on
cooldown**, **moving at an identical rate**, build at **one ninth** the rate.
The turns go to idle almost 1:1 (−7.3pp build, +7.7pp idle). **No named
alternative and not the leading hypothesis explains this cell.**

---

## RESULT 6 — WITHIN-MATCH PAIRING: the build effect is bulletproof, the heal effect is not

Games inside one match share the map, CAD's version and the opponent, so a match
containing both a damaged and an undamaged game controls every between-game
confound at once. **32 such matches (53 damaged, 105 undamaged games), r14-40:**

| metric | mean DAMAGED | mean undamaged | mean within-match diff | matches D<U | D>U |
| --- | ---: | ---: | ---: | ---: | ---: |
| **builds** | 1.09 | 7.09 | **−5.99** | **32** | **0** |
| build turns | 0.94 | 6.67 | −5.73 | **32** | **0** |
| core heals | 8.41 | 5.39 | +3.02 | 12 | **20** |
| collar seat-rounds | 37.03 | 24.42 | +12.61 | 7 | **25** |
| idle turns | 37.23 | 26.72 | +10.51 | 12 | **20** |
| moves | 59.76 | 80.14 | −20.39 | 24 | 8 |

**The build suppression reproduces in 32 of 32 matches with the map, the
opponent and both bot versions held fixed**, at a magnitude (−5.99) identical to
the pooled figure (−6.32). The heal and collar effects are directional
(20/32 and 25/32) but individually noisy — which is the right relative weighting:
**the effect to be explained is far more certain than the explanation on offer.**

## RESULT 7 — VERSION AND OPPONENT: not confined to either

Window r14-40:

| CAD ver | n DAMAGED | builds | core heals | collar/rd | n undam. | builds | core heals | collar/rd |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v107 | 11 | 0.91 | 12.91 | 1.498 | 29 | 6.93 | 3.17 | 0.663 |
| v116 | 0 | — | — | — | 10 | 9.00 | 0.90 | 0.274 |
| v117 | 15 | 1.60 | 5.20 | 1.407 | 35 | 7.23 | 3.83 | 0.738 |
| v118 | 1 | 1.00 | 18.00 | 1.778 | 4 | 8.00 | 0.50 | 0.398 |
| v120 | 11 | 0.82 | 9.45 | 1.333 | 34 | 7.00 | 3.38 | 0.734 |
| v123 | 2 | 0.00 | 3.00 | 1.463 | 23 | 7.35 | 3.39 | 0.715 |
| v124 | 13 | 0.69 | 12.54 | 1.655 | 35 | 7.49 | 4.43 | 0.806 |

Present in **every version with a damaged cell** (six of seven; v116 has none).
No version escapes it and none carries it alone.

| cell | population | n | builds | core heals | collar/rd | moves | idle turns |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| DAMAGED | vs us | 24 | 1.38 | 7.88 | 1.313 | 62.7 | 38.9 |
| undamaged | vs us | 81 | 7.75 | 3.00 | 0.624 | 74.8 | 26.1 |
| **DAMAGED** | **3rd party** | **29** | **0.69** | 11.10 | 1.619 | 57.1 | 36.3 |
| **undamaged** | **3rd party** | **89** | **6.93** | 3.84 | 0.769 | 78.7 | 25.7 |

**The whole thing reproduces in games our own bot is not in**, so it is CAD's
behaviour and not an artefact of what our bot does.

---

## WHAT THIS MEANS, stated plainly

1. **The effect is CAD's own policy, not the engine.** It survives fixing map,
   opponent and both versions (32/32 matches), and it appears in third-party
   games.
2. **Healer displacement is real and is the largest named component**, but it is
   **~18% at the most generous accounting and ~5-10% by dose-response.** The
   builder-bots that heal are on the collar and were barely building anyway; the
   builds that vanish belong to bots that cannot heal the core at all.
3. **The dominant mechanism is a defensive-mode branch that switches CAD's
   economy programme off.** Its observable signature is *idleness in bots that
   are free to act and can afford to build*, plus a homeward drift, plus a
   doubling of collar staffing of which only about a quarter of turns become
   heals.
4. **For a builder considering a denial plank:** denying the heal denies
   ~18% of a real effect. The build suppression itself is worth far more and
   **is triggered by damage on the core, not by the heal** — the trigger is
   already ours to pull (first core damage ≤ r13, which the lockout cut costed at
   a 4-5× lift in core-kill rate). Nothing here supports "starve the healer to
   keep them idle": they are already idle without it.

---

## NON-COVERAGE AND LIMITS — stated, not implied

1. **"In 225 attributed CAD games", never "CAD always".** The archive is not a
   random sample of the field; it is dominated by matches we or the archiver
   pulled. Third-party coverage is 120 games over 10 opponents, and the DAMAGED
   cell draws on 5 opponents.
2. **The DAMAGED cell is 53 games but only 32 matches.** Games within a match
   share map, version and opponent and are not independent. **No significance
   test is reported anywhere in this document; every figure is descriptive.** The
   within-match pairing (§Result 6) is the closest thing to inference here and is
   reported as a sign count, not a test.
3. **This is observational and the cell is defined by an event we do not
   randomise.** "Damaged before r14" means an enemy reached CAD's core by r13,
   which also means an enemy raider is physically inside CAD's base. **I cannot
   separate "CAD's policy reacts to core damage" from "CAD's policy reacts to an
   intruder", and both would produce every number above.** The lockout cut's
   reverse-causation cut still stands (the damaged band had the *highest*
   pre-damage build rate), so the arrow does not run builds → damage; but
   damage and intrusion are one event in this data.
4. **`idle` is "no observable event", not "chose to do nothing".** It is not
   cooldown (validated) and it is not a crash or a TLE (validated). It *could*
   include an action the wire does not carry: **`destroy()` emits no Update of
   its own** (only the building's `removeEntity`, and CAD loses only 0.53
   buildings per game in the window), and a `can_build()` that returned False for
   a reason I cannot observe would also read as idle. **"They tried and were
   refused" is not separable from "they did not try."** Both are policy outcomes,
   so the direction is unaffected, but the word "idle" should not be read as
   "lazy".
5. **Contested-tile blockage is argued against, not measured.** I show the
   damaged cell's builders are closer to their own core and that their build
   *sites* would be home tiles, but I did not compute per-tile buildability.
6. **Collar occupancy is a start-of-round snapshot**, so a seat taken mid-round
   is missed — occupancy is a slight undercount. 12 of 225 games have a
   wall/edge-truncated collar (< 8 seats); maps are symmetric so this is not
   biased between cells, and it is not excluded.
7. **Throws landing exactly one tile away are indistinguishable from a step**
   (corpus trap 3) and are labelled `move`. Throws are 0.02 turns/game here and
   change nothing.
8. **The r41-80 and r81-120 cells re-sort membership** (a game damaged at r30 is
   "damaged" in the r41-80 cell and "undamaged" in the r14-40 cell). Only the
   fixed-cohort trace in §Result 4 holds membership constant, and only it should
   be read for timing.
9. **CAD's source is not in a replay.** This document says what CAD's builders
   did, per turn, with money and cooldown controlled. It cannot say which branch
   of their code did it. A rebuild-priority ordering, a defensive gate, and a
   `can_build` guard that fails under threat all remain live and are not
   separable here.
10. **Not measured:** whether the enemy raider's *position* predicts the
    suppression better than the damage does (the cleanest next cut, and the one
    that would separate limit 3); CAD's turret behaviour in the window; whether
    the idle bots are adjacent to a legal build tile; and the `econ.tsv` /
    `flow.tsv` / `build_agg.tsv` corpus tables, which were **not read at all** —
    the corpus carries no damage stream and no `builderHeal`, so none of them
    could answer this question and none was frozen beyond `join.tsv`.
