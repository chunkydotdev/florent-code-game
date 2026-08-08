# Tipping-point decoder v1 — an eval curve for this game (2026-08-08)

**What this is.** v1 of the chess-engine instrument Magnus asked for: per-round
indicator curves over decoded games, validated for outcome prediction, producing
a per-game **TIP ROUND + DOMINANT REASON** annotation, a full **SHIFT SEQUENCE**
(every crossing *and* reversal, both directions), a proximate-event attribution
for each shift, and a **BLUNDER / STRONG-MOVE** census.

**Headline, stated up front because it is the finding.** Against 50 decoded
games, **no single published law works as an early eval.** The six candidate
indicators are, without exception, *terminal separators*: sampled as a state,
they run 46-64% correct at 10-25% of a game, 64-86% at the halfway mark, and only
the two core-controller laws plus the composite become law-grade (93-100%) after
~75% of the game has been played. The one indicator that is genuinely predictive
on its *first crossing* is the delivered-titanium curve, right on 89.3% (25/28) —
one game short of the ≥90% bar the brief set — with a median lead time of only 65
rounds (32% of the game). **What we have is not an eval; it is a very good
post-mortem.** That distinction is the actionable output.

---

## Version tags (rule 2)

| | |
|---|---|
| **Our live platform version at write time** | **v74 "mineguard" (x3r0)**, auto-activated 07:15 (`HANDOVER.md:5`); local copy `bots/opp_v74`, md5 `cb5452e6` |
| **Corpus** | **50 archived games / 10 ladder matches**, all already in `replay_archive/`. **Zero downloads, zero matches run, no bots edited.** |
| Corpus A — v72 bleed band (35 games) | `3de9f5e0` (kladde v75, 1-4) · `98e2c1fc` (kladde v75, 0-5) · `067dcff2` (Ouroboros v8, 0-5) · `fead7e71` (Leviathan v25, 2-3) · `8996dfc2` (Leviathan v25, 3-2) · `6cd1a9a3` (0033 v43, 2-3) · `072c3897` (Coreflood v63, 2-3) — us = **OpenSverige v72 "chainwatch"** |
| Corpus B — v73 windows (10 games) | `240a626c` (v73 3-2 Leviathan v25, we are TEAM_A) · `b5a37d0b` (0033 v43 5-0 v73, we are TEAM_B) |
| Corpus C — Clankers marquee (5 games) | `024d13d6` (Leviathan v26 0-5 **Clankers v1**) — no OpenSverige bot present |
| **Calibration pairs** (read-only, not in the 50) | `hs_archipelago_1_a` / `hsb_archipelago_1_a` and `hs_saga_1_b` / `hsb_saga_1_b` from the builder's `hs_mech_replays/` staged batteries |
| **Docs consumed as ground truth** | `v72-bleed-nonfamily-2026-08-08.md` · `v72-bleed-cad-family-2026-08-08.md` · `v73-production-read-2026-08-08.md` · `clankers-noconfound-2026-08-07.md` (incl. its 2026-08-08 seat-audit addendum) · `kcm-win-c1-validation-2026-08-07.md` · `kcm-wild-establishment-rates-2026-08-07.md` · `tools/replay_schema.md` · `docs/tooling.md` (Replay-decode gotchas) |
| Seat map | resolved per match from `.meta.json` `teamAId`/`teamBId`, not inferred |

**No fitted weights, no trained model, no threshold tuning.** Every threshold is
lifted verbatim from a previously published law and cited below. Where a
published threshold underperforms, it is reported as a finding (§7), not
silently adjusted.

---

## 1. The instrument

### 1.1 One walker, two curves per indicator

`tipwalk.py` walks each replay once and emits, for **both sides**, per-round
series: delivery (stacks onto own core footprint), core HP, core damage, core
heals, live builders, live harvesters, **directed** chain wiredness, melee swings
split by target class, turret shots split by "landed on the enemy core"; plus a
per-turret record (plant round, tile, facing, death round, d² to each core,
ray-coverage verdict, shots, shots-on-core, **first core shot**) and a filtered
event stream for attribution.

Each indicator is then expressed as a **per-side boolean state**, and the eval
curve is the **signed advantage**:

```
adv[ind][r] = +1  if state[A] and not state[B]      (favours replay TEAM_A)
              -1  if state[B] and not state[A]
               0  if both or neither
```

This exclusivity rule matters and is not a tuning knob — it is the difference
between an eval and a tally. Measured naively ("first round either side crosses"),
the ray-coverage indicator is 61% accurate; both sides plant uncovered turrets in
almost every game, so the raw crossing carries no information about *who is
ahead*. A **SHIFT** is any transition of `adv`; `to != 0` from `0` is a crossing,
`to == 0` is a reversal, and a sign flip is a swing.

### 1.2 The six indicators, with the law each threshold comes from

| tag | indicator | state definition | threshold provenance |
|---|---|---|---|
| **D** | delivery dominance | cumulative delivered Ti ≥ **2×** opponent's **and** ≥ **500 Ti** ahead | "economy 2:1" (`v72-bleed-nonfamily` §2.2, §5, §6); "delivery under ~500 Ti for the game" (`clankers-noconfound` §0.2) |
| **H** | siege heal/dmg deficit | inside a core-siege episode, running `4×heals / damage` ≤ **0.86** | bimodal law: ≥0.94 survives 13/13, ≤0.86 dies 16/16 (`v72-bleed-cad-family` L3), replicated 10/11 in `v73-production-read` check 12c |
| **U0 / U20 / UCNT / UDMG** | uncovered near-core turret | enemy G/S at **d²≤36** of the defender's footprint, **uncovered** over its lifetime (gunner = any of 8 rays, d²≤13, LOS-blocked; sentinel = build-time facing ray, d²≤32, obstacles ignored). U0 = planted; U20 = survived to age **20**; UCNT = strict count lead; UDMG = has already landed a shot on the core | ray-coverage law 0/69 (`kcm-win-c1-validation`), 0/147 (`v72-bleed-cad-family`), 0/11 and 45/46 (`v73-production-read`); d²≤36 band and "establishment" definition from `kcm-wild-establishment-rates`; age 20 > the published covered-turret median lifetime band 8-11 |
| **W** | chain wiredness collapse | ≥1 live harvester and **0** directed-wired harvesters, for ≥**50** consecutive rounds | directed-wiredness rule (`tools/replay_census.py` docstring); delivery-freeze mode (`v72-bleed-nonfamily` L4, `067dcff2` g4) |
| **P** | builder population collapse | live builders ≤**1** for ≥**30** consecutive rounds (r≥30) | L2 population mode (`v72-bleed-nonfamily`: "builders reach 0 by r200", "falls to ~1 in the last 100 rounds") |
| **C** | controller-law deficit | on a trailing **100**-round window with ≥50 HP taken, `damage − 4×heals > 0` **and** projected death round `r + hp/net ≤ 1000` | Clankers controller law: kill condition `dmg/rnd > 4 × heals/rnd`, death round `500/(dmg−heal)`, predicted 220/395/385 vs actual 219/393/365 (`clankers-noconfound` §0.2) |
| **CONS** | composite | unweighted sign of `UCNT + H + C + W + P + D` | no weights — a straight vote, per the brief's no-curve-fit constraint |

Sustained-window indicators (**W**, **P**) report a **detection round** =
onset + window, never the retrospective onset, so lead time is what a live
instrument could actually have called.

---

## 2. Self-checks

Run on all 50 games, both sides (100 team-sides).

| check | result |
|---|---|
| **Delivery identity** `core_deliv × 10 == titaniumCollected` | **100 / 100 team-sides, 0 mismatches** |
| **Core HP identity** `500 + Σ(UpdateHp deltas on the core id) == final core HP` | **100 / 100** (deaths land at −2/−4, the killing blow's overshoot) |
| **Damage ledger** `Σ negative core deltas == enemy FireTurret on footprint × 7/18 + enemy BuilderAttack on footprint × 2` | **99 / 100**; the single exception is `024d13d6` g1 team A, over by **18** = exactly one sentinel shot fired at the footprint in r203 *after* the core was already removed. Cause identified, benign, game **retained** and flagged |
| **Heal ledger** `core-heal actions × 4` vs positive core deltas | exact on 40 team-sides, short-by-clamp on 60 (over-heal clamp, the expected direction); **0 cases of positive delta exceeding heals** |
| Cross-check vs published numbers | `240a626c` g1 reproduces the v73 read digit-for-digit: core damage **1,085**, heals **149**, heal HP **596 vs 583 applied**, deliveries **380 / 810**, and turret **#27 covered** (the v73 read's single covered exception in corpus A) |
| Rotation dedupe | `placeEntity` re-emission on a live id updates facing/HP and is counted as a **rotation**, never a build |
| Damage-target law | turret fire attributed to the **unit** on the target tile, builder attack to the **building** — the new `tools/replay_schema.md` entry, honoured throughout |
| Launcher throws | `moveBuilderBot` with d²(from,to) > 1; counted, not load-bearing for any conclusion here |
| Channel | replays carry `print()` only; **no claim below rests on stderr** |

**Zero games excluded.**

---

## 3. Per-indicator validation

### 3.1 Causal first-crossing (what a live instrument would call)

n = games in which the indicator ever produced an exclusive advantage.
Precision = the favoured side won. Lead = rounds from crossing to game end.

| indicator | n | **precision (1st crossing)** | median lead | lead as % of game | all crossings | precision (all) | reversals | % of crossings that persist |
|---|---|---|---|---|---|---|---|---|
| **D** delivery dominance | 28 | **89.3%** (25/28) | 65 | 32% | 38 | **92.1%** | 13 | 65.8% |
| **C** controller deficit | 43 | 81.4% | 132 | 42% | 86 | 87.2% | 51 | 40.7% |
| **W** wiredness collapse | 14 | 78.6% | 103 | 22% | 18 | 83.3% | 4 | 77.8% |
| **UDMG** uncovered + firing | 47 | 63.8% | 216 | 85% | 108 | 67.6% | 68 | 37.0% |
| **UCNT** uncovered count lead | 46 | 63.0% | 258 | 84% | 96 | 64.6% | 56 | 41.7% |
| **U20** uncovered established | 46 | 63.0% | 258 | 84% | 92 | 63.0% | 60 | 34.8% |
| **U0** uncovered planted | 49 | 61.2% | 305 | 93% | 113 | 64.6% | 78 | 31.0% |
| **P** population collapse | 5 | 60.0% | 165 | 45% | 7 | 71.4% | 2 | 71.4% |
| **H** heal/dmg deficit | 48 | 41.7% | 202 | 86% | 109 | 62.4% | 75 | 31.2% |
| **CONS** unweighted composite | 50 | 46.0% | 270 | 88% | 143 | 61.5% | 95 | 33.6% |

**Nothing clears the ≥90% bar.** D misses by one game.

The inverse relationship is the whole story: **the indicators with long lead
times are the ones with no precision, and the one with precision has almost no
lead.** U0 fires at 93% of the game remaining and is a coin-flip; D fires with
32% remaining and is 89% right. H is *worse than chance* on its first crossing —
because in the opening exchanges both cores routinely dip below 0.86 before a
heal line is up, and which side dips first is noise.

### 3.2 The same laws, sampled as a state rather than an event

This is the honest answer to "how early is it knowable". n = games where the
curve had a nonzero sign at that point in the game.

| indicator | at 10% | at 25% | at 50% | at 75% | at 90% |
|---|---|---|---|---|---|
| **H** heal deficit | 60.0% (5) | 50.0% (10) | 85.7% (14) | **100%** (24) | **100%** (27) |
| **C** controller deficit | 60.0% (5) | 66.7% (3) | 85.7% (7) | **100%** (20) | **100%** (26) |
| **CONS** composite | 58.3% (12) | 56.5% (23) | 80.0% (35) | **93.2%** (44) | **95.8%** (48) |
| **D** delivery dominance | 100% (1) | 80.0% (5) | 77.8% (9) | 83.3% (18) | **95.8%** (24) |
| **UDMG** | 47.4% (19) | 61.1% (18) | 66.7% (21) | 85.3% (34) | **91.4%** (35) |
| **UCNT** | 60.0% (10) | 63.2% (19) | 64.3% (28) | 81.8% (33) | 86.8% (38) |
| **U0** | 50.0% (26) | 64.3% (28) | 69.2% (26) | 80.0% (35) | 87.1% (31) |
| **W** | 100% (1) | 75.0% (4) | 80.0% (5) | 83.3% (6) | 83.3% (12) |

**The knowability curve is flat until the halfway mark and then snaps.** The
composite is 56.5% at a quarter of the way through, 80.0% at half, 93.2% at
three-quarters. The two core-controller laws (H, C) are **perfect at 75% and 90%
in this corpus** — 24/24 and 20/20 — but they cover fewer games at that point
(they are only defined while a core is being shelled).

### 3.3 Dwell-filtered first crossing (does stability fix it?)

Requiring the advantage to be *held* K consecutive rounds before it counts:

| indicator | K=0 | K=25 | K=50 | K=100 |
|---|---|---|---|---|
| **D** | 89.3% n=28 L=65 | 87.5% n=24 L=77 | 82.4% n=17 L=198 | **90.9%** n=11 L=243 |
| **C** | 81.4% n=43 L=132 | 83.8% n=37 L=69 | 85.2% n=27 L=69 | **100%** n=10 L=70 |
| **H** | 41.7% n=48 L=202 | 68.2% n=44 L=92 | 80.6% n=31 L=45 | **90.0%** n=10 L=155 |
| **CONS** | 46.0% n=50 L=270 | 74.0% n=50 L=194 | 79.2% n=48 L=168 | 82.1% n=28 L=232 |
| **UCNT** | 63.0% n=46 L=258 | 72.7% n=44 L=228 | 69.2% n=39 L=209 | 76.0% n=25 L=255 |
| **UDMG** | 63.8% n=47 L=216 | 69.8% n=43 L=189 | 69.2% n=39 L=172 | 75.0% n=20 L=251 |
| **W** | 78.6% n=14 L=103 | 75.0% n=12 L=224 | 75.0% n=8 L=574 | 71.4% n=7 L=584 |

Stability helps H a great deal (42%→90%) and the ray-coverage family barely at
all (63%→76%). **A hundred-round dwell is what it costs to make the heal law
predictive, and by then 10 of 48 games are already over.** This table is reported
whole, deliberately: no K is "chosen", because choosing one on 50 games would be
the curve-fit the brief forbids.

### 3.4 Per-opponent-class splits (class imbalance is real: 15 Leviathan games, 10 kladde, 10 0033, 5 each Ouroboros / Coreflood / Clankers)

First-crossing precision, correct/total:

| indicator | kladde v75 | Ouroboros v8 | Leviathan v25/26 | 0033 v43 | Coreflood v63 | Clankers v1 |
|---|---|---|---|---|---|---|
| **D** | 3/3 | 4/4 | 8/9 | 7/7 | 1/1 | 2/4 |
| **C** | 8/10 | 1/3 | 11/13 | 6/8 | 4/4 | 5/5 |
| **UCNT** | 6/10 | 4/5 | 8/15 | 7/10 | 4/4 | 0/2 |
| **UDMG** | 5/10 | 2/3 | 7/15 | 8/10 | 5/5 | 3/4 |
| **H** | 3/10 | 0/5 | 6/15 | 5/10 | 3/3 | 3/5 |
| **W** | 1/1 | 1/1 | 4/6 | 1/2 | 1/1 | 3/3 |
| **CONS** | 4/10 | 0/5 | 7/15 | 5/10 | 5/5 | 2/5 |

Composite sign at the halfway / three-quarter mark, by class:

| class | at 50% | at 75% |
|---|---|---|
| kladde v75 | 3/5 | **9/9** |
| Ouroboros v8 | 4/4 | 5/5 |
| Leviathan | 10/13 | 11/14 |
| 0033 v43 | 7/7 | **9/9** |
| Coreflood v63 | 3/3 | 4/4 |
| Clankers v1 | 1/3 | 3/3 |

**Leviathan is the class the composite handles worst** (11/14 at 75%), and it is
also the class with the most shifts per game (10.1 law-grade crossings, 6.1
reversals) — the point-blank gunner plant that gets killed and re-planted on a
~13-round cadence makes the eval oscillate. Against **0033 and kladde**, whose
sieges are single-sentinel and permanent, the composite is perfect by 75%.

---

## 4. Per-game annotation: TIP ROUND + DOMINANT REASON

**Definitions.** Because §3.1 shows no indicator is a genuine early predictor,
the annotation is explicitly **retrospective** — the chess analogue of "where did
the eval last cross zero", not "when could you have called it":

- **TIP ROUND** = the round after the last round at which the composite curve
  favoured the eventual **loser**. The point of no return.
- **DOMINANT REASON** = of the law-grade curves whose sign at the **final round**
  matches the winner (end-anchored), the one with the earliest round from which
  that sign is never afterwards contradicted. Its onset is `dom_r`.
- **CLUSTER (compound tip)** = every qualifying indicator whose onset is within
  ±10 rounds of the dominant one.
- **UNRESOLVED-BY-v1** = tip lands beyond 90% of the game, or no law-grade curve
  ends on the winner's side.

`res` = winner seat + our result (`-` where OpenSverige is not in the match).
`agree` = **YES** dominant == manual primary · **sec** == a manual secondary ·
**NO** == disagreement (analysed in §5) · `-` == the ground-truth docs give no
per-game mechanism for that game.

| match | g | opponent | map | rnds | res | tip | tip% | dom_r | DOMINANT REASON | cluster | manual read | agree | shifts | swings |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `3de9f5e0` | 1 | kladde v75 | 26x26 | 390 | B L | 217 | 56% | 282 | UNCOVERED-TURRET-FIRING | UDMG | HEAL + uncovered | sec | 20 | 1 |
| `3de9f5e0` | 2 | kladde v75 | 28x20 | 1000 | A **W** | 19 | 2% | 115 | ECONOMY-DOMINANCE | D | ECONOMY | **YES** | 19 | 0 |
| `3de9f5e0` | 3 | kladde v75 | 25x15 | 311 | B L | 193 | 62% | 194 | UNCOVERED-TURRET | UCNT+UDMG | HEAL + uncovered | sec | 24 | 2 |
| `3de9f5e0` | 4 | kladde v75 | 26x26 | 610 | B L | 150 | 25% | 339 | UNCOVERED-TURRET-FIRING | UDMG | UNCOVERED + heal | **YES** | 17 | 1 |
| `3de9f5e0` | 5 | kladde v75 | 20x26 | 480 | B L | 226 | 47% | 54 | UNCOVERED-TURRET | UCNT | POP + heal | NO | 18 | 3 |
| `98e2c1fc` | 1 | kladde v75 | 16x16 | 595 | A L | 294 | 49% | 78 | UNCOVERED-TURRET | UCNT | HEAL + uncovered | sec | 35 | 2 |
| `98e2c1fc` | 2 | kladde v75 | 20x26 | 201 | A L | 136 | 68% | 136 | ECONOMY-DOMINANCE | D+UDMG+C | UNCOVERED + heal | NO | 9 | 0 |
| `98e2c1fc` | 3 | kladde v75 | 18x18 | 797 | A L | 122 | 15% | 184 | UNCOVERED-TURRET | UCNT | ECONOMY + uncovered | sec | 33 | 1 |
| `98e2c1fc` | 4 | kladde v75 | 16x16 | 349 | A L | 31 | 9% | 146 | ECONOMY-DOMINANCE | D | UNCOVERED + heal | NO | 10 | 1 |
| `98e2c1fc` | 5 | kladde v75 | 28x20 | 242 | A L | 115 | 48% | 147 | UNCOVERED-TURRET-FIRING | UDMG+C+H | ECONOMY + heal | NO | 10 | 1 |
| `067dcff2` | 1 | Ouroboros v8 | 16x16 | 370 | B L | 24 | 6% | 99 | UNCOVERED-TURRET | UCNT | POP + heal | NO | 14 | 1 |
| `067dcff2` | 2 | Ouroboros v8 | 25x25 | 232 | B L | 101 | 44% | 71 | UNCOVERED-TURRET | UCNT | UNCOVERED | **YES** | 15 | 3 |
| `067dcff2` | 3 | Ouroboros v8 | 24x24 | 1000 | B L | 38 | 4% | 693 | UNCOVERED-TURRET | UCNT | ECONOMY + pop | NO | 3 | 1 |
| `067dcff2` | 4 | Ouroboros v8 | 28x20 | 1000 | B L | 111 | 11% | 120 | ECONOMY-DOMINANCE | D | CHAIN + economy | sec | 22 | 1 |
| `067dcff2` | 5 | Ouroboros v8 | 26x26 | 1000 | B L | 34 | 3% | 103 | UNCOVERED-TURRET | UCNT | POP + economy | NO | 7 | 1 |
| `fead7e71` | 1 | Leviathan v25 | 16x16 | 102 | A L | 34 | 33% | 24 | UNCOVERED-TURRET-FIRING | UDMG | UNCOVERED | **YES** | 6 | 1 |
| `fead7e71` | 2 | Leviathan v25 | 21x8 | 221 | B **W** | 221 | 100% | — | **UNRESOLVED-BY-v1** | — | — | — | 16 | 2 |
| `fead7e71` | 3 | Leviathan v25 | 28x20 | 417 | A L | 21 | 5% | 18 | UNCOVERED-TURRET-FIRING | UDMG | CHAIN-BREAK | NO | 11 | 1 |
| `fead7e71` | 4 | Leviathan v25 | 25x15 | 142 | A L | 21 | 15% | 11 | UNCOVERED-TURRET-FIRING | UDMG+H | CHAIN-BREAK | NO | 6 | 0 |
| `fead7e71` | 5 | Leviathan v25 | 26x26 | 130 | B **W** | 54 | 42% | 54 | HEAL-DEFICIT | H | — | — | 10 | 0 |
| `8996dfc2` | 1 | Leviathan v25 | 20x26 | 227 | B **W** | 153 | 67% | 153 | CONTROLLER-DEFICIT | C+H | — | — | 19 | 1 |
| `8996dfc2` | 2 | Leviathan v25 | 14x18 | 353 | A L | 66 | 19% | 17 | UNCOVERED-TURRET-FIRING | UDMG | UNCOVERED | **YES** | 30 | 1 |
| `8996dfc2` | 3 | Leviathan v25 | 25x25 | 1000 | B **W** | 858 | 86% | 858 | CHAIN-BREAK | W | — | — | 15 | 2 |
| `8996dfc2` | 4 | Leviathan v25 | 28x20 | 275 | B **W** | 19 | 7% | 19 | HEAL-DEFICIT | H | CHAIN + economy | NO | 11 | 0 |
| `8996dfc2` | 5 | Leviathan v25 | 28x20 | 126 | A L | 86 | 68% | 58 | UNCOVERED-TURRET | UCNT | UNCOVERED | **YES** | 11 | 2 |
| `6cd1a9a3` | 1 | 0033 v43 | 25x25 | 284 | A **W** | 29 | 10% | 19 | UNCOVERED-TURRET-FIRING | UDMG+H | — | — | 16 | 0 |
| `6cd1a9a3` | 2 | 0033 v43 | 20x26 | 113 | B L | 78 | 69% | 73 | UNCOVERED-TURRET-FIRING | UDMG+D+UCNT | UNCOVERED + pop, heal | **YES** | 5 | 1 |
| `6cd1a9a3` | 3 | 0033 v43 | 10x10 | 806 | B L | 398 | 49% | 11 | UNCOVERED-TURRET-FIRING | UDMG | ECONOMY + chain, uncovered | sec | 28 | 4 |
| `6cd1a9a3` | 4 | 0033 v43 | 25x15 | 453 | B L | 192 | 42% | 192 | CONTROLLER-DEFICIT | C+H | UNCOVERED | NO | 20 | 2 |
| `6cd1a9a3` | 5 | 0033 v43 | 14x18 | 1000 | A **W** | 31 | 3% | 45 | UNCOVERED-TURRET | UCNT | — | — | 20 | 2 |
| `072c3897` | 1 | Coreflood v63 | 20x26 | 751 | B L | 243 | 32% | 231 | UNCOVERED-TURRET-FIRING | UDMG | UNCOVERED + heal | **YES** | 5 | 0 |
| `072c3897` | 2 | Coreflood v63 | 16x16 | 1000 | B L | 259 | 26% | 259 | ECONOMY-DOMINANCE | D | ECONOMY | **YES** | 7 | 0 |
| `072c3897` | 3 | Coreflood v63 | 16x16 | 425 | B L | 71 | 17% | 71 | UNCOVERED-TURRET | UCNT | POP + heal | NO | 14 | 0 |
| `072c3897` | 4 | Coreflood v63 | 26x26 | 1000 | A **W** | 463 | 46% | — | **UNRESOLVED-BY-v1** | — | — | — | 18 | 1 |
| `072c3897` | 5 | Coreflood v63 | 26x26 | 105 | A **W** | 34 | 32% | 24 | UNCOVERED-TURRET-FIRING | UDMG+H | — | — | 10 | 0 |
| `240a626c` | 1 | Leviathan v25 | 21x8 | 116 | B L | 41 | 35% | 44 | UNCOVERED-TURRET-FIRING | UDMG | HEAL + uncovered | sec | 7 | 0 |
| `240a626c` | 2 | Leviathan v25 | 26x26 | 200 | A **W** | 93 | 46% | 32 | HEAL-DEFICIT | H | — | — | 14 | 2 |
| `240a626c` | 3 | Leviathan v25 | 28x20 | 389 | B L | 73 | 19% | 13 | UNCOVERED-TURRET-FIRING | UDMG | UNCOVERED + heal | **YES** | 55 | 3 |
| `240a626c` | 4 | Leviathan v25 | 28x20 | 1000 | A **W** | 1000 | 100% | 210 | **UNRESOLVED-BY-v1** | (D) | ECONOMY | NO | 24 | 2 |
| `240a626c` | 5 | Leviathan v25 | 24x24 | 134 | A **W** | 113 | 84% | 113 | ECONOMY-DOMINANCE | D+H | — | — | 8 | 1 |
| `b5a37d0b` | 1 | 0033 v43 | 24x24 | 236 | A L | 97 | 41% | 173 | UNCOVERED-TURRET-FIRING | UDMG+C+H | UNCOVERED | **YES** | 9 | 1 |
| `b5a37d0b` | 2 | 0033 v43 | 21x8 | 133 | A L | 29 | 22% | 29 | UNCOVERED-TURRET | UCNT | UNCOVERED + heal | **YES** | 8 | 1 |
| `b5a37d0b` | 3 | 0033 v43 | 10x10 | 109 | A L | 29 | 27% | 19 | UNCOVERED-TURRET-FIRING | UDMG+H | UNCOVERED | **YES** | 7 | 1 |
| `b5a37d0b` | 4 | 0033 v43 | 25x25 | 129 | A L | 63 | 49% | 56 | UNCOVERED-TURRET-FIRING | UDMG+UCNT | UNCOVERED + heal | **YES** | 3 | 0 |
| `b5a37d0b` | 5 | 0033 v43 | 16x16 | 155 | A L | 52 | 34% | 39 | UNCOVERED-TURRET-FIRING | UDMG+UCNT | UNCOVERED | **YES** | 17 | 1 |
| `024d13d6` | 1 | Clankers v1 | 14x18 | 204 | B — | 112 | 55% | 112 | HEAL-DEFICIT | H+C | UNCOVERED + controller | NO | 4 | 0 |
| `024d13d6` | 2 | Clankers v1 | 18x18 | 245 | B — | 70 | 29% | 70 | HEAL-DEFICIT | H | UNCOVERED + controller | NO | 9 | 0 |
| `024d13d6` | 3 | Clankers v1 | 16x16 | 223 | B — | 88 | 40% | 38 | UNCOVERED-TURRET-FIRING | UDMG | UNCOVERED + controller | **YES** | 13 | 1 |
| `024d13d6` | 4 | Clankers v1 | 25x15 | 342 | B — | 255 | 75% | 100 | CONTROLLER-DEFICIT | C | UNCOVERED + controller | sec | 10 | 1 |
| `024d13d6` | 5 | Clankers v1 | 26x26 | 152 | B — | 95 | 62% | 95 | HEAL-DEFICIT | H+C | UNCOVERED + controller | NO | 9 | 1 |

**Tip-round distribution.** Median tip = **34%** of the game (p25 15%, p75 49%,
n=47 resolved). Median dominant-reason onset = **26%**. So the *point of no
return* is early — typically a third of the way in — even though, per §3, it is
not *recognisable* as such until much later. That gap is the single most useful
thing this instrument says: **games are usually decided long before any of our
laws can tell.**

**Compound tips.** **16 of 47** resolved games carry a cluster of ≥2 indicators
within ±10 rounds. The commonest pairings are **UDMG+H** (an uncovered turret
opens fire and the heal line fails to answer within ten rounds) and **C+H**, 4
games each, then **UCNT+UDMG** (3) and the triple **C+H+UDMG** (2). These are
several readings of one event, not several causes.

---

## 5. Validation against the manual attributions

40 of the 50 games carry a per-game mechanism in the ground-truth docs.

| measure | result |
|---|---|
| **STRICT** — v1 dominant reason == manual primary | **16 / 40 = 40%** |
| **LOOSE** — v1 dominant reason ∈ manual primary + secondary | **24 / 40 = 60%** |
| **RECALL** — manual primary detected *anywhere* in v1's persistent reason set | **34 / 40 = 85%** |

| class | strict | recall |
|---|---|---|
| 0033 v43 | 6/8 | 8/8 |
| Coreflood v63 | 2/3 | 3/3 |
| Leviathan v25 | 4/9 | 8/9 |
| Clankers v1 | 1/5 | 4/5 |
| Ouroboros v8 | 1/5 | 4/5 |
| kladde v75 | 2/10 | 7/10 |

**The gap between 40% and 85% is the whole verdict.** v1's *instruments* see the
human-decoded mechanism in 34 of 40 games; v1's *ranking rule* — "earliest
end-anchored law-grade curve" — puts it first in only 16. **v1 is a competent
detector and a poor prioritiser.**

### 5.1 The disagreements that matter

**(a) Where the manual read is right and v1 is wrong — v1 GAPS.**

1. **`fead7e71` g3 and g4 (Leviathan v25) — v1 says UNCOVERED-TURRET, the manual
   says CHAIN-BREAK.** This is the strongest causal claim in the whole bleed
   corpus, because its counterfactual was actually played (`8996dfc2` g4, same
   map/seat/opponent/version, won 70 minutes earlier). The manual read is right:
   we collected **0 titanium in 417 rounds** because two conveyors (6 Ti) were
   missing at (18,11)→(18,10). v1 does detect the chain break (W fires at r63 in
   g3, r110 in g4) but ranks the uncovered gunner ahead of it because the gunner's
   uncovered state begins at r18/r11 — earlier in wall-clock, later in causality.
   **v1 gap: the ranking rule has no notion of causal precedence, only temporal.**
   The chain break at r14 (harvester #16 built with no route home) is *upstream*
   of everything, and v1's detection lags it by 49 rounds because of the 50-round
   confirmation window.

2. **`067dcff2` g3 (Ouroboros v8, r1000 tiebreak) — manual says ECONOMY, v1's
   delivery indicator never fires.** Final delivery 11,170 vs 14,930 = **1.34:1**,
   comfortably below the published 2:1 gate. v1 saw only a lone uncovered turret at
   r693. **This is a published-threshold failure, reported not tuned** (§7).

3. **`3de9f5e0` g5 and `072c3897` g3 — manual says POP-COLLAPSE, v1 says
   UNCOVERED-TURRET.** The P indicator requires builders ≤1 for 30 rounds; the
   losses the manual describes are "population fell to ~4 against a base cap of 4"
   and "fell to ~1 in the last 100 rounds". P fires in `072c3897` g3 (r219) but is
   out-ranked. **v1 gap: population is measured as an absolute floor, when the
   published mode is a *ratio* — bodies against measured incoming HP/round.** The
   bleed doc's own arithmetic (8 staffed seats = 32 HP/round vs a max siege DPS of
   23.22) is a ratio law, and v1 does not implement it.

**(b) Where v1 is right and the manual read is arguably incomplete — MANUAL-READ
CORRECTIONS, flagged for the record.**

4. **`98e2c1fc` g4 (kladde v75) — v1 says ECONOMY-DOMINANCE from r146, the manual
   read attributes the game to the sentinel ring + heal line.** kladde's delivery
   lead crosses 2:1/500 Ti at r146 of a 349-round game and never reverses; their
   first uncovered near-core turret does not start damaging our core until r250.
   On the timeline, **the economy gap precedes the ring by 104 rounds** — which is
   exactly what the bleed doc's own §2.3 recipe item 3 says ("contest the ore belt
   from r5 … their harvester count is the whole game"), but the per-game
   attribution in §2.2 leads with the ring. Not a contradiction; a re-ordering.

5. **`024d13d6` g1/g2/g5 (Clankers marquee) — v1 says HEAL-DEFICIT, the manual
   says the forward-sentinel siege.** Both describe the same event from opposite
   sides, and here v1 is arguably sharper: the Clankers doc's own headline law is
   `dmg/rnd > 4 × heals/rnd`, i.e. **a heal-rate law**, and v1's H curve is that
   law made per-round. The forward sentinel is the *instrument*; the heal deficit
   is the *mechanism*, and it is the mechanism that generalises (Leviathan v26
   applied 2.35-2.81 dmg/round with the same shape and lost 0-5 because the heal
   rate absorbed it).

**(c) The one case where the ray-coverage law itself is challenged.**

6. **`024d13d6` g2 — v1 classified all four of Clankers' near-core turrets as
   COVERED, and they still killed.** Clankers' sentinel at (2,9) d²=25 lived
   r41→r136 and put 27 shots on Leviathan's core; the (3,10) sentinel from r201
   never died. Leviathan v26 held six turrets that *geometrically* covered them and
   fired 286 shots — but never at those tiles, and landed **0 builder attacks all
   game**. **"Covered" is a statement about geometry, not about suppression.** The
   published law's strong form (0/216 uncovered turrets ever shot at) is
   untouched; its *converse* — that covered turrets get answered — held 90/98 in
   the CAD corpus and fails here against an opponent with no counterbattery
   behaviour at all. Worth carrying: coverage predicts our capability, not our
   conduct.

---

## 6. Shift sequences, attribution, and the blunder / strong-move census

### 6.1 Census — is this game one-shift or multi-swing?

Over the seven law-grade curves, 50 games:

- **9.2 crossings and 5.4 reversals per game.**
- Composite direction switches: **1.1 per game**. **14 of 50 games (28%) never
  switch composite direction** (one-shift games); **36 of 50 (72%) are
  multi-swing.**

| opponent | n | crossings/gm | reversals/gm | composite switches/gm | one-shift games |
|---|---|---|---|---|---|
| kladde v75 | 10 | 11.7 | 7.8 | 1.2 | 2/10 |
| Leviathan v25/26 | 15 | 10.1 | 6.1 | 1.2 | 4/15 |
| 0033 v43 | 10 | 8.7 | 4.6 | 1.3 | 2/10 |
| Ouroboros v8 | 5 | 8.0 | 4.2 | 1.4 | **0/5** |
| Coreflood v63 | 5 | 6.8 | 4.0 | **0.2** | **4/5** |
| Clankers v1 | 5 | 6.4 | 2.6 | 0.6 | 2/5 |

**Coreflood is the flattest opponent in the corpus** (0.2 direction switches per
game): they never contest the middle, so the eval sets once and holds. **kladde
is the churniest** (11.7 crossings, 7.8 reversals) — the rebuildable d²=25
sentinel ring means the ray-coverage curve flips every time we kill one and they
replant.

### 6.2 Actor classification

Every shift is attributed to a proximate world-change in the preceding ≤15
rounds, then classified by the acting team. **729 of 731 law-grade shifts got a
named proximate event** (2 unattributed).

| class | n | share |
|---|---|---|
| **STRONG-MOVE** (winner's action caused the shift) | 363 | **49.8%** |
| **BLUNDER** (loser's action caused it — commission) | 261 | **35.8%** |
| **BLUNDER-OMISSION** (loser failed to act; no proximate enemy cause) | 81 | **11.1%** |
| **WINNER-SLIP** (winner's omission, got away with it) | 24 | 3.3% |

**Answer to Magnus's question: it is very close to an even split, tilting to the
winner's play — 49.8% strong moves against 46.9% loser errors.** But the split
moves with class:

| opponent | STRONG-MOVE | BLUNDER | BLUNDER-OMISSION | WINNER-SLIP |
|---|---|---|---|---|
| Clankers v1 | **57.8%** | 26.7% | 13.3% | 2.2% |
| Ouroboros v8 | 54.1% | 31.1% | 6.6% | 8.2% |
| kladde v75 | 50.5% | 36.6% | 9.3% | 3.6% |
| Coreflood v63 | 50.0% | 37.0% | 9.3% | 3.7% |
| Leviathan v25/26 | 48.3% | **40.5%** | 9.5% | 1.7% |
| 0033 v43 | 46.6% | 30.8% | **18.8%** | 3.8% |

Two readings worth acting on:

- **Against 0033 v43, one shift in five is a pure omission by the losing side** —
  the highest omission rate in the corpus, and 0033 is the opponent that swept us
  0-5 with v73. Their mechanism (one sentinel, uncovered, never moved) generates
  no proximate event to react to; the shift is *us not doing anything*. That is a
  self-inflicted loss class, which is good news: fixable without out-guessing them.
- **Against Leviathan the losses are commission-heavy (40.5%)** — their re-plant
  cadence forces action and we take the wrong ones.

### 6.3 Significance grading

| grade | definition | n | share |
|---|---|---|---|
| **DECISIVE** | crossing to the winner's side, never reversed | 181 | 24.8% |
| **MAJOR (reversed)** | law-grade indicator swung and was later reversed | 269 | 36.8% |
| **MAJOR (ends-wrong)** | law-grade indicator ends favouring the **loser** | 12 | 1.6% |
| **REVERSAL** | advantage returned to neutral | 269 | 36.8% |

Quantified magnitudes, straight from the replay:

- **Uncovered near-core turrets that put damage on a core: n = 220.** Median
  **5.96 HP/round**, p90 **9.00**, max **9.69** — and 9.0 HP/round is exactly the
  sentinel ceiling (18 dmg ÷ reload 2), so the top of the distribution is a
  sentinel firing without interruption for its whole life. Biggest single
  contributions: `b5a37d0b` g1 sentinel @(14,14) **576 HP over 64 rounds**;
  `b5a37d0b` g3 sentinel @(6,3) **396 over 44**.
- **Chain-break windows: n = 18.** Median **2.6 Ti/round** of delivery lost at the
  break, max **14.0 Ti/round**.
- **`rotate()`** is unchanged at 10 Ti (measured in the CAD-family read; not
  re-measured here).

### 6.4 Worked shift sequences

**`b5a37d0b` g4 — a three-shift, one-cause game (0033 v43, 25x25, we are B, core dead r129).**

| r | ind | favours | grade | actor | proximate event |
|---|---|---|---|---|---|
| 56 | UDMG | A | DECISIVE | STRONG-MOVE | uncovered sentinel #102 @(18,1) d²=13 opens fire on our core |
| 63 | UCNT | A | DECISIVE | STRONG-MOVE | same sentinel, planted r43, **504 core dmg, 5.86 HP/rnd over 86 rounds** |
| 69 | H | A | DECISIVE | **BLUNDER-OMISSION** | no proximate enemy event — **our healers never converged on the core** |

Three shifts, all one direction, no reversal. This is the v73 read's S5 ("the
healers never came home") and its S6 (`hive_bunker` barrier on a heal seat) in a
single curve, and it is the cleanest game in the corpus: the eval sets at r56 and
never moves again.

**`3de9f5e0` g1 — a four-swing game (kladde v75, 26x26, we are A, core dead r390).**

| r | ind | favours | grade | actor | proximate event |
|---|---|---|---|---|---|
| 45 | UCNT | A | MAJOR (reversed) | BLUNDER | their uncovered sentinel #63 @(16,16) d²=18 — 162 dmg, 4.63 HP/rnd |
| 60 | UCNT/UDMG | — | REVERSAL | STRONG-MOVE | **we kill #63 at r60** — the ring answered |
| 128-133 | H, UCNT, C | A | MAJOR (reversed) | BLUNDER | their gunner #316 @(20,16) + uncovered gunner #281 @(21,17) d²=5, 448 dmg at 6.59 HP/rnd |
| 180-186 | H, UCNT, UDMG | — | REVERSAL | STRONG-MOVE | **we kill #281 (r180) and #316 (r186)** |
| 301 | UCNT | B | **DECISIVE** | STRONG-MOVE | **sentinel #892 @(10,9) d²=25 — 972 dmg, 8.92 HP/rnd over 109 rounds** |
| 354 | C | B | DECISIVE | BLUNDER-OMISSION | healers did not converge |
| 377 | H | B | DECISIVE | STRONG-MOVE | sentinel #1209 @(11,5) added |

This is the kladde ring made visible: **we win the first two exchanges outright**
(both reversals are our kills) and lose to the third, which is planted at d²=25
— the radius the bleed doc identified as gunner-proof. The eval says the same
thing the doc says: it is not that we cannot answer, it is that we cannot answer
*that bearing*.

**`8996dfc2` g4 — the counterfactual win (Leviathan v25, 28x20, we are B, their core dead r275).**

Shifts run: their sentinel #11 opens (r19-23, H to B — because *we* are the one
under fire, and it is the deficit on **their** side that eventually decides);
**we kill their gunners #20 (r76) and #24 (r90)** — STRONG-MOVE reversal; **D
crosses to us at r117 on harvester #93 @(15,15)**; and the kill lands off our own
uncovered gunner #163 @(10,10) d²=4 planted r235, **210 dmg at 5.25 HP/rnd**. The
manual read attributes this game to the completed chain (r31), which v1's D curve
confirms at r117 — 86 rounds later, because 500 Ti of delivered margin takes that
long to bank.

---

## 7. A published threshold that underperforms — reported, not tuned

**The delivery-dominance gate `≥2:1 AND ≥500 Ti` is too strict for tiebreak
games, and it misses by margins that are almost comic.**

| game | result | final delivered (A vs B) | ratio | absolute gap | gate fired? |
|---|---|---|---|---|---|
| `98e2c1fc` g5 | we lose | 6,190 vs 3,100 | **1.9968** | 3,090 | **NO — short of 2.00 by 10 Ti** |
| `98e2c1fc` g3 | we lose | 4,120 vs 2,370 | 1.74 | 1,750 | NO |
| `067dcff2` g3 | we lose r1000 tiebreak | 11,170 vs 14,930 | 1.34 | 3,760 | NO |
| `067dcff2` g4 | we lose r1000 tiebreak | 740 vs 22,550 | 30.5 | 21,810 | yes |
| `072c3897` g2 | we lose r1000 tiebreak | 3,460 vs 11,570 | 3.34 | 8,110 | yes |

The 2:1 language in the source docs describes **economic suppression** (a state
where the loser cannot fund a counter), which is a different question from **who
wins tiebreak #1**, where any positive margin is decisive. `98e2c1fc` g5 losing
the gate by 10 Ti out of 9,290 is the clearest possible demonstration that the
ratio form is the wrong shape for the outcome question. **Not adjusted here** —
that is a v2 decision with a proper denominator, and tuning a threshold on the
same 50 games that exposed it would be exactly the overfit the brief rules out.

Second, smaller instance: **the P (population) threshold** of "≤1 builder for 30
rounds" fires in only 5 of 50 games while the manual reads name population as the
primary mechanism in 4 games where it never fires (`067dcff2` g1/g5,
`3de9f5e0` g5, `072c3897` g3). The published mode is a *ratio* (heal capacity vs
measured incoming), not an absolute floor. v1 implements the wrong form.

---

## 8. The UNRESOLVED residue — what v1 is not measuring

Three games are UNRESOLVED-BY-v1, and each names a different missing indicator.

**8.1 `240a626c` g4 (v73 vs Leviathan v25, 28x20, r1000, we WON 640-0 on
`titanium_collected`) — v1's composite ends favouring the loser.**
Leviathan held uncovered near-core turrets on us for the entire endgame (UCNT and
UDMG both end at −1), our chain collapsed at r317 (W ends −1), and only D
favoured us, from r210. Unweighted, the vote is 3-1 against the actual winner.
**Missing indicator: a tiebreak-terminal curve.** After ~r900 the delivered-Ti
margin *is* the win condition (tiebreak #1, and every r1000 game in the project's
corpora has resolved at step 1 — 19/19 as of the v73 read, which already counts
this game). A composite that keeps
voting core-health at r990 is measuring the wrong game. This is the single
cheapest v2 fix and it needs no new measurement, only a late-game override.

**8.2 `072c3897` g4 (Coreflood v63, 26x26, r1000, we WON 21,160-18,080) — a flat
eval for 537 rounds.** The composite swings to us at r78, to them at r351, back to
neutral at r463, and then **reads exactly zero for the last 54% of the game**.
Neither core was ever in terminal deficit; the delivery ratio finished at 1.17:1.
**Missing indicator: anything that discriminates two healthy economies.** Every
v1 curve is a *breakage* detector — even D only fires on a gap wide enough to mean
starvation. A game where nothing breaks is invisible to it. Candidate v2 measurements, all cheap from this
walker: delivery *rate* per 100 rounds (not cumulative), harvester count
trajectory, and ore-tile control.

**8.3 `fead7e71` g2 (Leviathan v25, 21x8, r221, we WON by core kill) — every
"we are losing" curve fired and we won anyway.** At the final round UCNT, UDMG, W
and P all favour Leviathan; our chain broke at r132 and was never re-planned, and
two builders died at r137-152 with no replacement spawn. We then killed their core
at r221. **Missing indicator: an offensive one.** Nothing in v1 measures *our*
damage rate on the *enemy* core against *their* heal capacity as a forward-looking
quantity — C does, but only on a 100-round trailing window, which cannot see a
kill that arrives inside it. The Clankers read already gives the exact form
(`time-to-kill = 500 / (dmg_rate − 4×heal_rate)`); v1 applies it defensively only.

**8.4 The residue inside the *resolved* games — six recall misses.** In six games
v1 never detected the mechanism the human decoded at all:

| game | manual mechanism | what v1 saw instead | missing measurement |
|---|---|---|---|
| `067dcff2` g3 | economy / spawn ceiling | one uncovered turret at r693 | sub-2:1 economy margin (§7) |
| `98e2c1fc` g3, g5 | economy | uncovered + heal + controller | sub-2:1 economy margin (§7) |
| `3de9f5e0` g5 | population (nordkap seat-A base cap 4) | uncovered + heal + controller | **map/seat-conditional caps** — v1 has no notion that a seat can bound population |
| `8996dfc2` g4 | chain completed by r31 | heal, controller, economy, uncovered | **chain-completion as a positive event** — W only detects *collapse*, never *repair* |
| `024d13d6` g2 | Clankers' forward sentinel | heal, controller, chain | coverage ≠ suppression (§5.1c) |

Two of these name genuinely new v2 indicators: **chain-completion latency** (how
many rounds from first harvester to first delivered stack — the metric that
separates `8996dfc2` g4 from `fead7e71` g3) and a **seat-conditional population
ceiling**.

---

## 9. Calibration against the builder's staged single-change pairs

The builder's `hs_mech_replays/` batteries contain identical games differing by
one bot change — ground-truth single-blunder games. Magnus named
`archipelago-1-a`. The detector was run on it blind.

| | `hs_archipelago_1_a` | `hsb_archipelago_1_a` |
|---|---|---|
| result | **LOSS**, r1000, `titanium_collected` 12,330-13,570 | **WIN**, **r202**, `core_destroyed` 1,250-450 |
| **our launcher** | **r12 @(5,7)** — `on_own_seat = TRUE` | **r13 @(5,8)** — off-seat |
| core damage taken | 846 | 576 |
| heal/dmg over r0-201 | **0.91** (inside the bimodal dead band) | **1.01** (survive lobe) |
| delivered by r200 | 950 | **1,230** |
| composite shift sequence | identical to hsb through **r51**, diverges at **r74**: 0→−1, then swings at r91/96/163/173/197/201/233 | identical through r51, diverges at **r60**: 0→−1, recovers at r94/96, holds **+1 from r125 to the kill** |

**The detector finds the change.** The two eval curves are byte-identical through
r51 and separate at r60/r74 — 47 rounds after the one differing world-event — and
the attributor's own blunder class for that event ("own impassable building on a
core heal seat") is exactly the change that was made. Our core's heal ratio moves
from 0.91 to 1.01, i.e. **across the published bimodal gap**, which is the
mechanism the seat rule predicts.

Two caveats stated plainly: the detector **dates the divergence at r60, not at
r12** — the eval reacts 48 rounds after the move, which is the same lag §3 measures
everywhere; and the second pair (`hs_saga_1_b` / `hsb_saga_1_b`) is not an outcome
flip (both are B wins) but is a clean **shape** flip — 14+ composite swings become
exactly one, at r74, held for 550 rounds.

---

## 10. Method spec — running this as a standing instrument

Enough detail to re-run without this session.

**Inputs.** `.replay26` files plus their `.meta.json` (for seat→team-name/version
resolution — never infer seat from behaviour when the meta exists).

**Pass 1, the walker** (`tipwalk.py`; stdlib only, reuses `fields`, `scalars`,
`read_pos`, `packed_varints`, `KIND_FIELDS`, `DIRECTION_DELTA`, `CARDINALS` from
`tools/replay_census.py`). One linear pass over `turns[]`:

1. Seed both cores from `map.cores` at 500 HP (they are never a `placeEntity`).
2. `placeEntity`: if the id is already live, this is a **rotation** (update facing
   and HP, count it, never a build). Otherwise register the entity; maintain
   `buildings[pos]→id` and `bots[pos]→{ids}`.
3. `moveBuilderBot`: update position; `d²(from,to) > 1` is a **launcher throw**.
4. `removeEntity`: mark death, clear occupancy, close the turret record.
5. `distributeResources`: a move whose `to` is on a core footprint is a delivery
   (×10 Ti) to that footprint's owner.
6. `updateHp`: sign-extend the varint at **2^63** (int32 negatives are wire-encoded
   as 10-byte sign-extended varints — getting this wrong silently produces
   20-digit HP values); accumulate per-core damage and heal deltas.
7. `fireTurret`: shooter = the live turret standing on the `from` tile. Damage
   lands on the **unit** at `to` (7 gunner / 18 sentinel). Record first
   core-landing shot per turret.
8. `builderAttack`: damage lands on the **building** at the target tile (2 dmg).
   Classify the target as enemy conveyor / enemy core / enemy turret.
9. `builderHeal`: target on own core footprint ⇒ a core heal, +4 HP each.
10. End of round: snapshot builders, harvesters, core HP; recompute **directed**
    chain wiredness only when the harvester/relay set changed (a conveyor feeds
    only the tile it faces; a splitter the three cardinals not directly behind);
    emit a `wire` event when the wired count changes.
11. Ray coverage: for each enemy turret at d²≤36 of the defender's footprint,
    sample at every round of its first 8 and then on a 25-round stride; covered =
    any live defender turret satisfies the coverage predicate at any sample.

**Coverage predicate.** Gunner: target row/col/diagonal aligned, d²≤13, and every
intervening tile free of walls and live buildings (rotation assumed available).
Sentinel: target on the build-time facing ray, d²≤32, obstacles ignored. A
stricter gunner LOS model (blocking on builder bots) can only move turrets **into**
the uncovered column, so the headline uncovered-turret results are unaffected.

**Pass 2, states** (`tipeval.py`): the seven boolean state series of §1.2. Siege
episodes = contiguous core-damage rounds merged across gaps < 30; substantive =
≥100 HP and ≥10 rounds. Sustained-window indicators report detection = onset +
window.

**Pass 3, advantage** (`tipadv.py`): the signed exclusivity rule, shift extraction,
proximate-event attribution (a fixed priority ladder over the ±15-round event
window: near-core turret plant → turret death → wire change → harvester
birth/death → builder death run → own impassable building on a heal seat → core
death), and actor classification (event team == winner ⇒ STRONG-MOVE; == loser ⇒
BLUNDER; an omission with no proximate enemy cause ⇒ BLUNDER-OMISSION, or
WINNER-SLIP if it is the winner's).

**Pass 4, annotation** (`tiptable.py`): tip round, end-anchored dominant reason,
cluster, UNRESOLVED test, grading.

**Runtime.** 4.2 s for 50 games on one core. Cheap enough to run on every
production read.

**Standing self-checks that must pass before any number is quoted:** delivery
identity per team-side; core HP-delta identity; damage ledger closing to the
FireTurret + BuilderAttack attribution (a residue of exactly one shot's damage in
the killing round is expected and benign); heal actions ×4 ≥ applied positive
deltas (clamp direction).

**Known limits of v1.**

- Self-destructs are indistinguishable from kills, so a `died` event is always
  attributed to the opponent. This inflates STRONG-MOVE slightly.
- Builder positions come from `moveBuilderBot` and are read at the start of a
  round; heal and move are mutually exclusive, so this is exact for heal
  attribution and ±1 round elsewhere.
- The 50-game corpus has heavy class imbalance (15 Leviathan / 10 kladde / 10
  0033 / 5 each of the rest) and every opponent appears in at most two matches
  inside a few hours. **No per-class number below n=5 should be leaned on**, which
  includes the whole P row and the Coreflood/Ouroboros/Clankers columns.
- Only 40 of 50 games have a manual attribution, and those attributions are
  themselves single-reader judgements from the same week.

---

## 11. So-what

1. **We have a good post-mortem and no eval.** The published laws separate
   outcomes essentially perfectly *after the fact* (H and C are 100% at 75% of the
   game) and are coin-flips in the first quarter. Anyone building an in-game
   decision rule on them should know they will be acting on noise before ~r250.
2. **The point of no return is at a third of the game and we cannot see it there.**
   Median tip round 34%, median composite reliability at 25% = 56.5%. The prize is
   not a better composite of the existing laws; it is a *new* early measurement.
   §8 names three candidates with evidence behind each.
3. **Wins are roughly half earned and half handed over (49.8% / 46.9%)**, and the
   omission share is highest exactly where we bleed worst — 18.8% against 0033 v43,
   the opponent that swept v73 0-5. Those are shifts with no enemy event to react
   to: our own non-action moved the eval.
4. **The delivery-dominance gate needs re-shaping for tiebreak games** (§7), and
   the composite needs a late-game tiebreak override (§8.1). Both are v2 work with
   the same walker.
5. **The instrument survives a controlled test**: on the builder's staged
   single-change archipelago pair it reproduces the divergence and its own blunder
   taxonomy names the change that was made.

---

## Appendix — scratch (not committed)

`tipwalk.py` (walker), `tipeval.py` (states), `tipadv.py` (advantage curves,
shifts, attribution), `tiptable.py` (annotation), `manual.py` (transcribed
ground-truth attributions), `corpus.json` (seat/version index built from
`.meta.json`). All in the session scratchpad. **Read-only throughout: no bots
edited, no arena or platform commands run, no downloads, no HANDOVER or tape
writes.**
