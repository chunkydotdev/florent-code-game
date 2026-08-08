# Tipping-point decoder v2 — the three missing measurements (2026-08-08)

**What this is.** v2 of the eval-curve instrument. v1
(`docs/research/tipping-point-decoder-2026-08-08.md`) validated six
breakage-based laws as *post-mortem* instruments and left three games unresolved,
each naming a different missing measurement. This document builds those three —
**T (tiebreak-terminal)**, **K (offensive time-to-kill)**, **G (healthy-economy
discriminator)** — reports them against a pre-stated acceptance battery, and adds
the **eco-optimal game signature**: a production-read yardstick for whether we are
playing our own game.

**Headline, stated up front.** All three v1-unresolved games now resolve with the
correct winner, agreement with the human attributions is up (40%→42% strict,
85%→92% recall), the composite is now defined in **50/50 games at every sample
point** instead of 12–48, and it is **100% correct at 90% of the game (50/50)**.
But the thing Magnus actually asked for is still not delivered: **earliness did
not move.** At a quarter of the game the composite reads 58.0% against v1's
56.5%, and on v1's own subset it is *worse* (52.2%). The three new curves close
the *coverage* hole and the *terminal* hole; they do not close the *prediction*
hole. v1's verdict stands — this is a very good post-mortem, now with no blind
spots, and still not an eval.

The one genuinely new predictive result is **G**: the delivery-*rate* curve is
**73.9% correct on its first crossing with a 234-round median lead (86% of the
game)** — strictly better than every uncovered-turret curve in v1 at the same
lead time (UDMG 63.8% at 85%). It is the only thing in either version that is
both early *and* better than a coin flip.

---

## Version tags (rule 2)

| | |
|---|---|
| **Our live platform slot at write time** | **v74 "mineguard" (x3r0)**, auto-activated 07:15, slot bar rebased to it (`HANDOVER.md` §"State at 07:25"); a **c-rev candidate cycle** is running (`_v85hsb`, md5 `33a42f94`, confirmation legs pending) |
| **Baseline document** | `docs/research/tipping-point-decoder-2026-08-08.md` (v1). Its §10 method spec is reused verbatim; its six laws are **not** retuned |
| **Corpus** | the **same 50 games / 10 ladder matches** as v1, for comparability. **Zero downloads, zero matches run, no bots edited, no arena or platform commands.** |
| Corpus A — v72 bleed band (35 games) | `3de9f5e0-6dd0-4d1e-bcac-f1f2ff28bd3b` · `98e2c1fc-1670-459d-87f8-79702054fc29` · `067dcff2-0649-4a81-a003-387aeb7d6513` · `fead7e71-4efc-4300-93a1-8abf6a38bd8a` · `8996dfc2-edbc-4734-9969-96dac1c29558` · `6cd1a9a3-55f3-4830-b33c-b6604f27d65f` · `072c3897-bf53-4e87-a7f3-31a15c22700f` — us = **OpenSverige v72 "chainwatch"** |
| Corpus B — v73 windows (10 games) | `240a626c-18a3-4c25-bd49-7b7cc28bf003` (we are TEAM_A) · `b5a37d0b-87f5-46c6-968b-ef19099d90f9` (we are TEAM_B) |
| Corpus C — Clankers marquee (5 games) | `024d13d6-e0f5-4d29-819f-b1d02bc15fa8` — no OpenSverige bot present |
| Seat map | resolved per match from `.meta.json` `teamAId`/`teamBId`, never inferred |
| Decode contract | `tools/replay_schema.md` (incl. the corrected **damage-target law**, §Damage-target law: turret fire hits the tile's UNIT when present, ELSE the BUILDING; builder attacks always hit the BUILDING) and `docs/tooling.md` Replay-decode gotchas |

**No fitted weights, no trained model, no threshold tuning.** Every v2 threshold
is either an engine constant, a previously published law, or the engine's own win
condition — each is named, and each is *checked* against a measurement in §2. The
2:1 delivery gate stays hard-edged: its near-misses are reported (§7), not moved.

---

## 1. What v1 said was missing, and what v2 built

| v1 unresolved game | v1's diagnosis | v2 indicator |
|---|---|---|
| `240a626c` g4 — we won 640-0 on `titanium_collected` while 3 of 4 v1 curves voted against us | "missing: a tiebreak-terminal curve" | **T** |
| `fead7e71` g2 — every "we are losing" curve fired and we killed their core first | "missing: an offensive one" | **K** |
| `072c3897` g4 — v1's eval read exactly zero for the last 54% of the game | "missing: anything that discriminates two healthy economies" | **G** |

### 1.1 T — TIEBREAK-TERMINAL

**Question it answers.** If nobody's core dies, who wins at round 1000?

**Definition.** A signed curve evaluated every round, following the engine's own
tiebreak ladder in order:

1. **Projected delivered titanium at r1000** —
   `proj[t] = cum_deliv[t][r] + rate[t][r] × (1000 − r)`, where
   `rate[t][r]` is the trailing-100-round delivered-Ti-per-round.
   This is an *income-rate projection*, not a curve fit: it is a linear
   extrapolation of a measured rate, with no free parameters.
2. **Harvesters alive** (tiebreak #2) — used only when the projections tie.
3. **Banked titanium** (tiebreak #3) — used only when #1 and #2 tie.

**Threshold provenance.** There is no threshold. The ladder is the game's win
condition verbatim (`CLAUDE.md`: "titanium delivered to core → harvesters alive →
titanium stored → coinflip"). The 100-round rate window is **the C law's own
trailing-rate window**, reused unchanged from v1 §1.2 (Clankers controller law).

**Measured justification (M2).** Of the 50 games, **9 reach r1000, and all 9
resolve at step 1 — delivered titanium — 9/9.** Steps 2 and 3 never decided a
game in this corpus. This replicates the v73 read's 19/19 and is why the ladder is
implemented in order rather than as a blend.

### 1.2 K — OFFENSIVE TIME-TO-KILL

**Question it answers.** Whose core dies first?

**Definition.** For each side, the Clankers kill formula is applied to the
**enemy** core, scoped to the currently live siege episode:

```
proj_kill[attacker] = r + hp_defender(r) / ( dmg_rate − 4 × heal_rate )
```

where `dmg_rate` and `heal_rate` are accumulated *within the live episode* (not
over a fixed trailing window), and the projection counts only when it lands at or
before r1000. **K favours whichever side's projected kill round is EARLIER.**

**This is a race, not an exclusivity test — and that distinction is the whole
indicator.** Built the v1 way (side A in deficit *and* side B not), K reads zero
in exactly the game it was built for: in `fead7e71` g2 **both** cores carry a
computable death round simultaneously (ours projects r165 from r27, theirs r148
from r98), so an exclusivity test cancels to nothing. The offensive law does not
ask "can I kill?" — it asks "do I get there first?", so the curve compares death
rounds.

**Threshold provenance.** The formula is the Clankers controller law verbatim
(`clankers-noconfound` §0.2: `time-to-kill = 500/(dmg − 4×heal)`, predicted
220/395/385 vs actual 219/393/365). The episode scoping is v1's own H machinery,
unchanged (gap 30, ≥100 HP, ≥10 rounds; CAD-family L3).

**Measured justification (M3) — why the window had to change.** Substantive siege
episodes have a median length of 84 rounds; the *lethal* episode (the one that
killed a core) has a median length of 98. **21 of 41 lethal episodes (51%) are
shorter than the C law's 100-round trailing window.** C literally cannot see half
the kills in this corpus, because the kill lands inside its own averaging window.
Episode scoping is not a tuning choice; it is the only window that resolves.

### 1.3 G — HEALTHY-ECONOMY DISCRIMINATOR

**Question it answers.** Two economies, neither broken — which one is actually
pulling ahead?

**Definition.** A **comparative** curve on the trailing-100-round delivery *rate*:

```
G = +1  if rate[A] − rate[B] ≥ 2.5 Ti/round
    −1  if rate[B] − rate[A] ≥ 2.5 Ti/round
     0  otherwise
```

Per the brief's constraint, this is a side-A-vs-side-B curve with crossing events
only — there is no "healthy" threshold, because no published law defines one.

**The deadband is a game constant, not a fitted parameter.** 2.5 Ti/round is
exactly **one harvester's steady-state output**: `STACK_SIZE (10) ÷ harvester
period (4 rounds) = 2.5`. G therefore says precisely "one side is out-earning the
other by at least one working harvester", which is the smallest economically
meaningful difference the game can express.

**Measured justification (M1) — the constant checked against the corpus.** Pooled
over all 100 team-sides: **363,570 Ti delivered over 152,740 wired-harvester-rounds
= 2.380 Ti per wired harvester per round.** Per team-side (n=82 with ≥200
harvester-rounds): **median 2.509**, p25 2.363, p75 2.584. The engine constant
2.500 sits inside the interquartile range of the measurement, so the deadband is
one real harvester, not a number chosen to make the curve work.

**Supporting components measured but not thresholded.** Ore headroom (M4: median
peak saturation 0.67 harvesters per ore tile; 15/50 games exceed 80%, so ore *is*
sometimes the binding constraint), harvester-count trajectory, and directed
wiredness are all carried in the walker and reported per crossing as diagnostics —
none of them gets a threshold, because none has a published one.

### 1.4 CONS9 — the 9-indicator composite, and its one structural rule

v1's composite is an unweighted vote of six curves. Adding three more curves to
that vote does **not** fix `240a626c` g4: the vote goes 3–2 against the actual
winner instead of 3–1. What fixes it is not a weight but the game's own structure.

**The game has exactly two terminal conditions, and each owns one curve that *is*
its win condition rather than a cause of it:**

| terminal condition | the curve that IS it |
|---|---|
| `core_destroyed` | **K** — the race between the two projected death rounds |
| round 1000 | **T** — the engine's tiebreak ladder |

The other six curves (UCNT, H, C, W, P, D) are **mechanism** curves: they explain
*why* a race is going the way it is. They are not independent evidence about who
wins. So:

```
CONS9[r] =  if some core has a computable death round (C or K live on either side):
                K[r]  if K[r] ≠ 0  else  sign(UCNT + H + C + W + P + D)   # v1's exact six
            else:                                                  # r1000 is the live terminal
                T[r]  if T[r] ≠ 0  else  G[r]
```

**No weights are introduced anywhere**; the fallback vote is v1's six, unweighted
and unchanged. The precedence is a statement about the rules of the game, not
about this corpus. §4 reports the **flat unweighted 9-vote** alongside it so the
cost of the precedence is visible.

**Why the r1000 case needs no late-game override.** v1 §8.1 proposed "a late-game
override" for tiebreak games. None is needed and none is used: C's own condition
is `r + hp/net ≤ 1000`, so as r→1000 it requires an ever-larger net damage rate
and switches itself off. The branch changes hands automatically. Measured: the
mean share of rounds spent in the TIEBREAK branch is **0.90 in games that reached
r1000** vs **0.51 in games that ended by core kill**, and every r1000 game in the
corpus spends the majority of its rounds there (recall 100%, precision 28% — the
branch is a good *necessary* condition, a weak sufficient one).

### 1.5 Ranking tiers for the DOMINANT REASON

T and G have a sign from round 0 in every game. v1's ranking rule is "earliest
end-anchored curve wins", so dropping two always-defined curves into it makes them
the dominant reason nearly everywhere — measured, that alone dropped strict
agreement from 40% to **28%**. The repair is a taxonomy, not a tuning knob:

- **Tier 1 — event curves** (UCNT, UDMG, H, C, **K**, W, P, D): each turns on
  because something happened in the world, so "earliest onset" orders them
  meaningfully. This is exactly v1's law-grade set plus K.
- **Tier 2 — always-defined race curves** (**T**, **G**): their onset carries no
  event information. They are the fallback that says "decided on the clock",
  used only when no event curve explains the result.

Dominant reason = earliest end-anchored tier-1 curve; if none, earliest tier-2;
if none, UNRESOLVED. With tiering restored, strict agreement is **42%** (§4.2).

---

## 2. Measured relationships behind every v2 threshold

Reported so each constant can be checked rather than trusted.

| # | measurement | result | what it licenses |
|---|---|---|---|
| **M1** | Ti delivered per wired-harvester-round, pooled over 100 team-sides | **2.380** pooled; per-side median **2.509** (p25 2.363, p75 2.584), n=82 | G's deadband of 2.5 = `STACK_SIZE/4` is one real harvester |
| **M2** | how r1000 games actually resolve | **9/9 at step 1** (delivered Ti); steps 2 and 3 never used | T implements the ladder in order |
| **M3** | lethal siege-episode length vs C's 100-round window | median lethal episode **98** rounds; **21/41 (51%) shorter than 100** | K must be episode-scoped, not trailing-window |
| **M4** | peak ore saturation (live harvesters ÷ ore tiles) | median **0.67**, max 1.00; >80% in **15/50** games | ore headroom is a real constraint; carried as a diagnostic, not a threshold |

---

## 3. Self-checks

Standing checks from v1 §10, re-run on all 50 games / 100 team-sides, plus the two
new series.

| check | v2 result | v1 |
|---|---|---|
| **Delivery identity** `core_deliv × 10 == titaniumCollected` | **100 / 100** | 100/100 |
| **Core HP identity** `500 + Σ(UpdateHp deltas) == final core HP` | **100 / 100** | 100/100 |
| **Damage ledger** `Σ neg core deltas == turret + melee attribution` | **99 / 100** | 99/100 |
| — the single exception | `024d13d6` g1 team A: observed 1,206, attributed 1,224, **residue exactly −18** = one sentinel shot at the footprint in r203 after the core was already removed. Cause identified, benign, game **retained** | identical |
| **Heal ledger** heal actions ×4 vs positive core deltas | exact on **40**, short-by-clamp on **60**, **0** cases of positive delta exceeding heals | 40 / 60 / 0 |
| **NEW — banked-Ti series** no negative balances | **PASS** | — |
| **NEW — ore headroom** live harvesters ≤ ore tiles, every round | **50 / 50** | — |

**No lookahead.** T reads cumulative delivery, trailing rate, harvester count and
bank as of round r only. G reads trailing rates only. K accumulates damage and
heals within the live episode up to r; episode *membership* at round r is
"damage within the last 30 rounds", which is knowable live — the same property
v1's H relies on. Zero games excluded.

---

## 4. Acceptance — against each pre-stated criterion

### 4.1 Criterion 1 — the three v1-unresolved games resolve with the correct winner

**PASS, 3/3.**

| game | v1 | v2 dominant reason | v2 CONS9 at end | verdict |
|---|---|---|---|---|
| `240a626c` g4 (Leviathan v25, r1000, **we won** 640-0) | UNRESOLVED; CONS ends **−1, the wrong side** | ECONOMY-DOMINANCE @r210, cluster D | **+1, correct** | **PASS** |
| `072c3897` g4 (Coreflood v63, r1000, **we won** 21,160-18,080) | UNRESOLVED; CONS ends **0** (flat for the last 54%) | TIEBREAK-TERMINAL @r548, cluster T | **+1, correct** | **PASS** |
| `fead7e71` g2 (Leviathan v25, r221, **we won** by core kill) | UNRESOLVED; CONS ends **+1, the wrong side** | TIME-TO-KILL @r98, cluster K | **−1, correct** | **PASS** |

Mechanism, per game:

- **`240a626c` g4.** Leviathan delivered **0 titanium in 1000 rounds**. The game
  spends **618/1000 rounds in the TIEBREAK branch**, where T reads the ladder and
  never wavers. Note the honest detail: T's *first* crossings here are step-3
  (banked-Ti) noise at r0–r6 while both projections are 0; the load-bearing signal
  is the state, not the crossing. The tier-1 rule then hands the dominant reason
  to **D** (r210) rather than T, which is the right answer — this game was decided
  by an economy that existed against one that did not.
- **`072c3897` g4.** Two healthy economies, final ratio 1.17:1 — far under the 2:1
  gate, which is why v1 saw nothing. T tracks the projected delivery race
  throughout, flips to Coreflood at r346 (proj 19,388 vs 19,424 — a 36-Ti lead)
  and back to us at r548, where it stays. **861/1000 rounds in the TIEBREAK
  branch.** G independently ends +1 on a trailing-rate gap of 25.1 vs 20.0 Ti/rnd.
- **`fead7e71` g2.** Both cores carry a computable death round at once, which is
  precisely why an exclusivity test reads zero here. Leviathan's kill on **our**
  core becomes computable at r27 (net 3.27 HP/rnd, first projecting r165); ours on
  **theirs** at r98 (net 7.71 HP/rnd, projecting r148). K favours us from r98 —
  the round our projected kill first lands earlier than theirs — and the real kill
  arrives at r220 (the projection is optimistic in level, correct in order, which
  is all the curve claims). Every v1 curve that fired (UCNT, UDMG, W and P all end
  favouring Leviathan) was describing damage that was never going to be collected.

### 4.2 Criterion 2 — strict agreement ≥ v1's 40%

**PASS.** Recomputed over all 40 mechanism-decoded games with the 9-indicator set:

| measure | v1 (6-indicator) | **v2 (9-indicator)** |
|---|---|---|
| **STRICT** — dominant reason == manual primary | 16/40 = **40%** | **17/40 = 42%** |
| **LOOSE** — dominant reason ∈ primary + secondary | 24/40 = 60% | **26/40 = 65%** |
| **RECALL** — manual primary detected anywhere | 34/40 = 85% | **37/40 = 92%** |

Per class (strict): 0033 6/8 (unchanged) · Coreflood 2/3 (unchanged) · Leviathan
**4/9 → 5/9** · Clankers 1/5 (unchanged) · Ouroboros 1/5 (unchanged) · kladde
2/10 (unchanged).

The strict gain is one game — **`240a626c` g4**, which v1 could not resolve at all
and v2 attributes to ECONOMY-DOMINANCE, matching the manual read. The recall gain
is three — **`067dcff2` g3, `98e2c1fc` g3, `98e2c1fc` g5**, all three of v1's
*sub-2:1 economy* recall misses (§5.1a.2 and §8.4), now caught by the new
economy-race curves: **T** first in every case (r68 / r97 / r13), **G** confirming
(r120 / r192 / r31). This is exactly the gap v1 §8.4 predicted, and it closes with
the rate form rather than by moving the 2:1 gate. **v1's diagnosis that
it is "a competent detector and a poor prioritiser" survives v2 intact**: recall
92%, strict 42%. The ranking rule is still the weak link, and it is still
temporal-not-causal.

### 4.3 Criterion 3 — v1's six indicator precision/lead numbers unchanged

**PASS — reproduced digit-for-digit.** v2 reuses v1's walker output unmodified
(the two new series come from a *separate* supplementary pass, so `all.json` is
byte-identical), and every published v1 number was recomputed:

| v1 section | cells checked | result |
|---|---|---|
| §3.1 causal first-crossing | 10 indicators × 8 columns | **exact**, including D 89.3% (25/28) / lead 65 / 32%, C 81.4% / 132, H 41.7%, CONS 46.0% |
| §3.1 CONS reversals cell | 1 | published **95** = 93 transitions to zero **+ 2 direct sign flips**, per v1 §1.1's own "a sign flip is a swing" definition — accounted, not a walker difference |
| §3.2 state-sampled at 10/25/50/75/90% | 8 indicators × 5 | **exact**, incl. H 100% (24) at 75% and 100% (27) at 90% |
| §3.3 dwell-filtered | 7 indicators × 4 × (precision, n) | **28/28 precision exact, 28/28 n exact** |
| §3.3 median-lead column | 21 | **21/21 exact** once v1's inclusive detection round (`detect = onset + K − 1`, as in `tipeval.py`'s W/P detail) and `round()` on an even-n median are applied |
| §4 annotation | tip, tip%, dominant reason, cluster, all 50 games | **exact**, incl. all three UNRESOLVED games |
| §4 distribution | median tip 34%, p25 15%, p75 49%, n=47; dom onset 26%; compound 16/47 | **exact** |
| §5 agreement | 3 measures + 6 class rows | **exact** (16/40, 24/40, 34/40; 0033 6/8 8/8, Coreflood 2/3 3/3, Leviathan 4/9 8/9, Clankers 1/5 4/5, Ouroboros 1/5 4/5, kladde 2/10 7/10) |
| §6.1 census | 9.2 crossings, 5.4 reversals, 1.1 switches, 14/50 one-shift + all 6 class rows | **exact** |
| §6.2 actor classification | 363 / 261 / 81 / 24 of 729 attributed (731 total) | **exact** |
| §6.3 grading | 181 DECISIVE / 269 MAJOR-reversed / 12 ends-wrong / 269 REVERSAL | **exact** |

Two reporting conventions were recovered rather than guessed, and are recorded
here so v3 does not have to rediscover them: **(a)** v1's dwell lead is measured
from the *detection* round `onset + K − 1`, not the onset; **(b)** v1's "reversals"
column counts transitions to zero *plus* direct sign flips.

### 4.4 Criterion 4 — earliness re-measured with 9 indicators

**Reported honestly: no early improvement.**

| composite | at 10% | at 25% | at 50% | at 75% | at 90% |
|---|---|---|---|---|---|
| v1 CONS (6) | 58.3% (12) | 56.5% (23) | 80.0% (35) | 93.2% (44) | 95.8% (48) |
| v2 flat 9-vote (no precedence) | 53.3% (45) | 61.4% (44) | 79.5% (44) | 95.6% (45) | 97.9% (48) |
| **v2 CONS9 (9, terminal-first)** | 48.0% (50) | 58.0% (50) | 78.0% (50) | 95.8% (48) | **100.0% (50)** |

The raw comparison flatters v2 on coverage and flatters v1 on accuracy, because
v1's composite is *silent* in most games early. Matched to v1's own defined subset:

| on the games where v1's CONS had a sign | at 10% | at 25% | at 50% | at 75% | at 90% |
|---|---|---|---|---|---|
| v1 CONS (6) | 58.3% (12) | **56.5%** (23) | 80.0% (35) | 93.2% (44) | 95.8% (48) |
| v2 CONS9 (9) | 50.0% (12) | **52.2%** (23) | **82.9%** (35) | **95.5%** (44) | **100.0%** (48) |

| on the games where v1's CONS was SILENT | at 10% | at 25% | at 50% | at 75% | at 90% |
|---|---|---|---|---|---|
| v2 CONS9 (9) | 47.4% (38) | 63.0% (27) | 66.7% (15) | 100% (4) | 100% (2) |

**The honest reading.** v2 buys three things and not the fourth:
1. **Coverage** — 50/50 games have a signed eval at every sample point (v1: 12, 23, 35, 44, 48). There are no longer any invisible games.
2. **Terminal accuracy** — 100% at 90% of the game, and **0/50 UNRESOLVED** (v1: 3/50).
3. **Attribution** — recall 85%→92%.
4. **Earliness — no.** At 25% of the game the composite is 58.0%, and on v1's own subset it is *worse* (52.2% vs 56.5%). The median point of no return moved from 34% to **37%** of the game (p25 12%, p75 52%), and it remains unrecognisable when it happens.

**Where earliness *did* move is inside the regimes.** Sampled as a state, each new
curve is law-grade in the regime it was built for:

| indicator | at 10% | at 25% | at 50% | at 75% | at 90% |
|---|---|---|---|---|---|
| T (all games) | 56.0% (50) | 58.0% (50) | 72.0% (50) | 82.0% (50) | 88.0% (50) |
| **T (games that reached r1000)** | **100% (9)** | **100% (9)** | 88.9% (9) | **100% (9)** | **100% (9)** |
| K (all games) | 50.0% (6) | 54.5% (11) | 88.9% (18) | 96.3% (27) | 100% (34) |
| **K (games ending by core kill)** | 33.3% (3) | 44.4% (9) | **93.8% (16)** | **96.3% (27)** | **100% (34)** |
| G (all games) | 53.8% (13) | 68.2% (22) | 75.0% (28) | 92.3% (39) | 97.4% (38) |

**T is 9/9 from the tenth round of any game that goes the distance.** That is the
strongest early number in either document — with the honest caveat that it is
conditioned on an outcome you do not know in advance. The branch predicate is the
live proxy for that condition and it is a good necessary condition only (recall
100%, precision 28%): it will tell you a game is *not* going to r1000, not that
it is.

### 4.5 The new indicators as events (v1 §3.1 form)

| indicator | n | **precision (1st crossing)** | median lead | lead as % of game | all crossings | precision (all) | reversals | % persisting |
|---|---|---|---|---|---|---|---|---|
| **G** economy-rate lead | 46 | **73.9%** | 234 | 86% | 175 | **79.4%** | 136 | 22.3% |
| **K** time-to-kill race | 49 | 42.9% | 203 | 86% | 145 | 65.5% | 95 | 28.3% |
| **T** tiebreak-terminal | 50 | 46.0% | 297 | 100% | 319 | 52.7% | 3 | 15.7% |
| *(v1 reference)* **D** | 28 | 89.3% | 65 | 32% | 38 | 92.1% | 13 | 65.8% |
| *(v1 reference)* **UDMG** | 47 | 63.8% | 216 | 85% | 108 | 67.6% | 68 | 37.0% |

**G is the result.** At essentially the same lead time as v1's best-covered curve
(86% vs 85% of the game remaining), G is **73.9%** where UDMG is 63.8% and UCNT is
63.0% — and 79.4% across all crossings where they are 67.6% and 64.6%. It is the
first indicator in this project that is early *and* better than noise. By class its
first crossing is 10/10 against kladde v75, 11/12 against Leviathan, 7/9 against
0033, 5/5 against Ouroboros — and **0/5 against Clankers, 1/5 against Coreflood**,
the two classes where the winner's economy was not the mechanism.

**T's crossing precision (46.0%) should be ignored, and its state reading used
instead.** T is defined from round 0, so its "first crossing" is usually a
banked-titanium tie-break between two economies that have delivered nothing. Its
3 reversals over 319 crossings tell the same story: it is a state instrument.

**K's crossing precision (42.9%) is honest and low for a real reason**: the first
side to establish a computable kill is frequently the side that loses the
counterattack. K only becomes law-grade once both sides' projections exist and can
be compared — from the halfway mark, where it is 93.8% and then 96.3% and 100%.

---

## 5. The 9-indicator per-game annotation

`res` = winner seat + our result (`—` where OpenSverige is not in the match).
`T`/`K`/`G` = each new curve's sign at the final round (`+` = TEAM_A).
`agree`: **YES** = dominant == manual primary · `sec` = a manual secondary ·
`rec` = manual primary detected but not ranked first · `NO` = not detected at all.

| match | g | opponent | rnds | res | tip | tip% | dom_r | DOMINANT REASON | cluster | T | K | G | manual | agree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `024d13d6` | 1 | Clankers v1 | 204 | B&mdash; | 97 | 48% | 111 | TIME-TO-KILL | K,H,C | &minus; | &minus; | &minus; | UNCOVERED + controller | sec |
| `024d13d6` | 2 | Clankers v1 | 245 | B&mdash; | 202 | 82% | 70 | HEAL-LINE-DEFICIT | H,K | &minus; | &minus; | 0 | UNCOVERED + controller | NO |
| `024d13d6` | 3 | Clankers v1 | 223 | B&mdash; | 114 | 51% | 38 | UNCOVERED-TURRET-FIRING | UDMG | &minus; | &minus; | &minus; | UNCOVERED + controller | **YES** |
| `024d13d6` | 4 | Clankers v1 | 342 | B&mdash; | 255 | 75% | 100 | CONTROLLER-DEFICIT | C | &minus; | &minus; | &minus; | UNCOVERED + controller | sec |
| `024d13d6` | 5 | Clankers v1 | 152 | B&mdash; | 95 | 62% | 95 | HEAL-LINE-DEFICIT | H,K,C | &minus; | &minus; | &minus; | UNCOVERED + controller | rec |
| `067dcff2` | 1 | Ouroboros v8 | 370 | B L | 24 | 6% | 99 | UNCOVERED-TURRET | UCNT | &minus; | &minus; | &minus; | POP + heal | rec |
| `067dcff2` | 2 | Ouroboros v8 | 232 | B L | 101 | 44% | 71 | UNCOVERED-TURRET | UCNT | &minus; | &minus; | &minus; | UNCOVERED | **YES** |
| `067dcff2` | 3 | Ouroboros v8 | 1000 | B L | 68 | 7% | 693 | UNCOVERED-TURRET | UCNT | &minus; | 0 | &minus; | ECONOMY + pop | rec |
| `067dcff2` | 4 | Ouroboros v8 | 1000 | B L | 111 | 11% | 120 | ECONOMY-DOMINANCE | D | &minus; | 0 | &minus; | CHAIN + economy | sec |
| `067dcff2` | 5 | Ouroboros v8 | 1000 | B L | 34 | 3% | 103 | UNCOVERED-TURRET | UCNT | &minus; | 0 | &minus; | POP + economy | rec |
| `072c3897` | 1 | Coreflood v63 | 751 | B L | 194 | 26% | 231 | UNCOVERED-TURRET-FIRING | UDMG | &minus; | &minus; | &minus; | UNCOVERED + heal | **YES** |
| `072c3897` | 2 | Coreflood v63 | 1000 | B L | 5 | 0% | 259 | ECONOMY-DOMINANCE | D | &minus; | 0 | &minus; | ECONOMY | **YES** |
| `072c3897` | 3 | Coreflood v63 | 425 | B L | 160 | 38% | 71 | UNCOVERED-TURRET | UCNT | &minus; | &minus; | &minus; | POP + heal | rec |
| `072c3897` | 4 | Coreflood v63 | 1000 | A **W** | 548 | 55% | 548 | TIEBREAK-TERMINAL | T | + | 0 | + | &mdash; | &mdash; |
| `072c3897` | 5 | Coreflood v63 | 105 | A **W** | 34 | 32% | 24 | UNCOVERED-TURRET-FIRING | UDMG,H,K | &minus; | + | 0 | &mdash; | &mdash; |
| `240a626c` | 1 | Leviathan v25 | 116 | B L | 35 | 30% | 44 | UNCOVERED-TURRET-FIRING | UDMG,K | &minus; | &minus; | &minus; | HEAL + uncovered | sec |
| `240a626c` | 2 | Leviathan v25 | 200 | A **W** | 32 | 16% | 32 | HEAL-LINE-DEFICIT | H,K | &minus; | + | &minus; | &mdash; | &mdash; |
| `240a626c` | 3 | Leviathan v25 | 389 | B L | 64 | 16% | 13 | UNCOVERED-TURRET-FIRING | UDMG | &minus; | &minus; | &minus; | UNCOVERED + heal | **YES** |
| `240a626c` | 4 | Leviathan v25 | 1000 | A **W** | 54 | 5% | 210 | ECONOMY-DOMINANCE | D | + | 0 | 0 | ECONOMY | **YES** |
| `240a626c` | 5 | Leviathan v25 | 134 | A **W** | 105 | 78% | 105 | TIME-TO-KILL | K,D | + | + | + | &mdash; | &mdash; |
| `3de9f5e0` | 1 | kladde chatte tvil v75 | 390 | B L | 243 | 62% | 282 | UNCOVERED-TURRET-FIRING | UDMG,K | &minus; | &minus; | &minus; | HEAL + uncovered | sec |
| `3de9f5e0` | 2 | kladde chatte tvil v75 | 1000 | A **W** | 7 | 1% | 115 | ECONOMY-DOMINANCE | D | + | 0 | 0 | ECONOMY | **YES** |
| `3de9f5e0` | 3 | kladde chatte tvil v75 | 311 | B L | 153 | 49% | 194 | UNCOVERED-TURRET | UCNT,UDMG | &minus; | &minus; | &minus; | HEAL + uncovered | sec |
| `3de9f5e0` | 4 | kladde chatte tvil v75 | 610 | B L | 287 | 47% | 339 | UNCOVERED-TURRET-FIRING | UDMG | &minus; | &minus; | &minus; | UNCOVERED + heal | **YES** |
| `3de9f5e0` | 5 | kladde chatte tvil v75 | 480 | B L | 320 | 67% | 54 | UNCOVERED-TURRET | UCNT | &minus; | &minus; | &minus; | POP + heal | NO |
| `6cd1a9a3` | 1 | 0033 v43 | 284 | A **W** | 108 | 38% | 19 | UNCOVERED-TURRET-FIRING | UDMG,H,K | + | + | + | &mdash; | &mdash; |
| `6cd1a9a3` | 2 | 0033 v43 | 113 | B L | 83 | 73% | 73 | UNCOVERED-TURRET-FIRING | UDMG,D,UCNT,K | &minus; | &minus; | &minus; | UNCOVERED + pop, heal | **YES** |
| `6cd1a9a3` | 3 | 0033 v43 | 806 | B L | 398 | 49% | 11 | UNCOVERED-TURRET-FIRING | UDMG | &minus; | &minus; | &minus; | ECONOMY + chain, uncovered | sec |
| `6cd1a9a3` | 4 | 0033 v43 | 453 | B L | 172 | 38% | 192 | CONTROLLER-DEFICIT | C,H,K | &minus; | &minus; | &minus; | UNCOVERED | rec |
| `6cd1a9a3` | 5 | 0033 v43 | 1000 | A **W** | 503 | 50% | 45 | UNCOVERED-TURRET | UCNT | + | 0 | 0 | &mdash; | &mdash; |
| `8996dfc2` | 1 | Leviathan v25 | 227 | B **W** | 33 | 15% | 153 | CONTROLLER-DEFICIT | C,H,K | &minus; | &minus; | &minus; | &mdash; | &mdash; |
| `8996dfc2` | 2 | Leviathan v25 | 353 | A L | 120 | 34% | 17 | UNCOVERED-TURRET-FIRING | UDMG | + | + | 0 | UNCOVERED | **YES** |
| `8996dfc2` | 3 | Leviathan v25 | 1000 | B **W** | 147 | 15% | 858 | CHAIN-BREAK | W | &minus; | 0 | &minus; | &mdash; | &mdash; |
| `8996dfc2` | 4 | Leviathan v25 | 275 | B **W** | 23 | 8% | 19 | HEAL-LINE-DEFICIT | H,K | &minus; | &minus; | &minus; | CHAIN + economy | NO |
| `8996dfc2` | 5 | Leviathan v25 | 126 | A L | 86 | 68% | 58 | UNCOVERED-TURRET | UCNT | + | + | + | UNCOVERED | **YES** |
| `98e2c1fc` | 1 | kladde chatte tvil v75 | 595 | A L | 475 | 80% | 78 | UNCOVERED-TURRET | UCNT | + | + | + | HEAL + uncovered | sec |
| `98e2c1fc` | 2 | kladde chatte tvil v75 | 201 | A L | 47 | 23% | 136 | ECONOMY-DOMINANCE | D,UDMG,C | + | + | + | UNCOVERED + heal | rec |
| `98e2c1fc` | 3 | kladde chatte tvil v75 | 797 | A L | 97 | 12% | 184 | UNCOVERED-TURRET | UCNT | + | + | + | ECONOMY + uncovered | sec |
| `98e2c1fc` | 4 | kladde chatte tvil v75 | 349 | A L | 31 | 9% | 146 | ECONOMY-DOMINANCE | D | + | + | 0 | UNCOVERED + heal | rec |
| `98e2c1fc` | 5 | kladde chatte tvil v75 | 242 | A L | 86 | 36% | 147 | UNCOVERED-TURRET-FIRING | UDMG,C,H,K | + | + | + | ECONOMY + heal | rec |
| `b5a37d0b` | 1 | 0033 v43 | 236 | A L | 28 | 12% | 173 | UNCOVERED-TURRET-FIRING | UDMG,C,H,K | + | + | + | UNCOVERED | **YES** |
| `b5a37d0b` | 2 | 0033 v43 | 133 | A L | 50 | 38% | 29 | UNCOVERED-TURRET | UCNT | + | + | + | UNCOVERED + heal | **YES** |
| `b5a37d0b` | 3 | 0033 v43 | 109 | A L | 10 | 9% | 19 | UNCOVERED-TURRET-FIRING | UDMG,H,K | + | + | + | UNCOVERED | **YES** |
| `b5a37d0b` | 4 | 0033 v43 | 129 | A L | 69 | 53% | 56 | UNCOVERED-TURRET-FIRING | UDMG,UCNT | &minus; | + | 0 | UNCOVERED + heal | **YES** |
| `b5a37d0b` | 5 | 0033 v43 | 155 | A L | 64 | 41% | 39 | UNCOVERED-TURRET-FIRING | UDMG,UCNT | + | + | + | UNCOVERED | **YES** |
| `fead7e71` | 1 | Leviathan v25 | 102 | A L | 34 | 33% | 24 | UNCOVERED-TURRET-FIRING | UDMG,K | + | + | 0 | UNCOVERED | **YES** |
| `fead7e71` | 2 | Leviathan v25 | 221 | B **W** | 98 | 44% | 98 | TIME-TO-KILL | K | + | &minus; | 0 | &mdash; | &mdash; |
| `fead7e71` | 3 | Leviathan v25 | 417 | A L | 254 | 61% | 18 | UNCOVERED-TURRET-FIRING | UDMG | &minus; | + | 0 | CHAIN | rec |
| `fead7e71` | 4 | Leviathan v25 | 142 | A L | 16 | 11% | 11 | UNCOVERED-TURRET-FIRING | UDMG,H,K | + | + | + | CHAIN | rec |
| `fead7e71` | 5 | Leviathan v25 | 130 | B **W** | 18 | 14% | 54 | HEAL-LINE-DEFICIT | H,K | &minus; | &minus; | &minus; | &mdash; | &mdash; |

**Annotation summary.** **0 of 50 UNRESOLVED-BY-v2** (v1: 3). Agreement over the
40 mechanism-decoded games: **17 YES · 9 sec · 11 rec · 3 NO**. Median tip round
**37%** of the game (p25 12%, p75 52%) against v1's 34% / 15% / 49% — the point of
no return did not move, and the small rightward shift is the terminal-first rule
declining to call a game while the kill race is still genuinely two-sided.

**K appears in 20 of the 50 clusters**, almost always alongside H or C — which is
the expected reading, not a redundancy: the heal deficit is the mechanism and the
time-to-kill is the consequence, and they are supposed to co-fire. K is the
*dominant* reason in only 3 games (`024d13d6` g1, `240a626c` g5, `fead7e71` g2),
all of them games decided by a kill that arrived faster than a trailing window
could average.

---

## 6. The eco-optimal game signature

We play an economy strategy. This section defines what that strategy looks like
when it is working, measurably and from the laws, then scores every one of our
games against it. The point is a production-read yardstick: **not "did we win"
but "did we play our own game".**

### 6.1 Definition

Five components, each HOLD or BREAK, each with a break round:

| # | component | measurable definition | provenance |
|---|---|---|---|
| **1** | **DELIV-EARLY** | delivery dominance (D: cum ≥2× opponent **and** ≥500 Ti ahead) crosses to us **before 34% of the game** and never afterwards favours them | 34% = the corpus median point-of-no-return (v1 §4); D's gate unchanged from v1 §1.2 |
| **2** | **FLAT** | **no** breakage curve {UCNT, UDMG, H, W, P} ever crosses against us | "breakage curves flat, no reversals against us" |
| **3** | **SIEGE-MINOR** | for **every** substantive siege on our core: first core-heal lands within **≤3 rounds** of first damage **AND** episode heal/dmg **≥ 0.94** | 0.94 = published bimodal survive lobe (CAD-family L3, replicated `v73-production-read` 12c); ≤3 rounds per the brief |
| **4** | **NO-OMISSION** | **zero** omission-class shifts whose actor is us (BLUNDER-OMISSION when losing, WINNER-SLIP when winning) | v1 §6.2 actor taxonomy, unchanged |
| **5** | **TERMINAL** | ends in **T** favouring us, **or** **K** favouring us with their core dead | v2 §1.4 terminal curves |

**Score = components held, 0–5.** A companion column re-runs component 1 on the
v2 **rate** curve G instead of the hard 2:1 gate, and a diagnostic column counts
breakage crossings against us.

### 6.2 Scorecards — all 45 our-side games

| match | g | opponent | rnds | res | 1 DELIV-EARLY | 2 FLAT | 3 SIEGE-MINOR | 4 NO-OMISSION | 5 TERMINAL | score | crossings against us | 1b rate-curve |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `067dcff2` | 1 | Ouroboros v8 | 370 | BL | never fires | BREAK r99 | BREAK r221 | BREAK r229 | BREAK | **0/5** | 6 | never fires |
| `067dcff2` | 2 | Ouroboros v8 | 232 | BL | never fires | BREAK r71 | BREAK r146 | BREAK r26 | BREAK | **0/5** | 4 | never fires |
| `067dcff2` | 3 | Ouroboros v8 | 1000 | BL | never fires | BREAK r693 | HOLD | BREAK r33 | BREAK | **1/5** | 1 | never fires |
| `067dcff2` | 4 | Ouroboros v8 | 1000 | BL | never fires | BREAK r203 | BREAK r203 | BREAK r17 | BREAK | **0/5** | 10 | never fires |
| `067dcff2` | 5 | Ouroboros v8 | 1000 | BL | never fires | BREAK r103 | HOLD | HOLD | BREAK | **2/5** | 3 | never fires |
| `072c3897` | 1 | Coreflood v63 | 751 | BL | never fires | BREAK r231 | HOLD | BREAK r705 | BREAK | **1/5** | 3 | BREAK r241 |
| `072c3897` | 2 | Coreflood v63 | 1000 | BL | never fires | BREAK r195 | BREAK r368 | HOLD | BREAK | **1/5** | 1 | never fires |
| `072c3897` | 3 | Coreflood v63 | 425 | BL | never fires | BREAK r71 | BREAK r242 | BREAK r422 | BREAK | **0/5** | 8 | BREAK r188 |
| `072c3897` | 4 | Coreflood v63 | 1000 | AW | never fires | BREAK r332 | BREAK r332 | BREAK r78 | HOLD | **1/5** | 3 | BREAK r501 |
| `072c3897` | 5 | Coreflood v63 | 105 | AW | never fires | HOLD | HOLD | BREAK r53 | HOLD | **3/5** | 0 | never fires |
| `240a626c` | 1 | Leviathan v25 | 116 | BL | never fires | BREAK r41 | BREAK r19 | HOLD | BREAK | **1/5** | 4 | never fires |
| `240a626c` | 2 | Leviathan v25 | 200 | AW | never fires | BREAK r30 | HOLD | BREAK r100 | HOLD | **2/5** | 3 | never fires |
| `240a626c` | 3 | Leviathan v25 | 389 | BL | never fires | BREAK r13 | BREAK r13 | BREAK r59 | BREAK | **0/5** | 20 | never fires |
| `240a626c` | 4 | Leviathan v25 | 1000 | AW | HOLD | BREAK r15 | HOLD | BREAK r317 | HOLD | **3/5** | 10 | HOLD |
| `240a626c` | 5 | Leviathan v25 | 134 | AW | BREAK r113 | BREAK r45 | BREAK r45 | BREAK r121 | HOLD | **1/5** | 3 | BREAK r72 |
| `3de9f5e0` | 1 | kladde chatte tvil v75 | 390 | BL | never fires | BREAK r282 | BREAK r282 | BREAK r45 | BREAK | **0/5** | 3 | never fires |
| `3de9f5e0` | 2 | kladde chatte tvil v75 | 1000 | AW | HOLD | BREAK r348 | HOLD | BREAK r19 | HOLD | **3/5** | 1 | HOLD |
| `3de9f5e0` | 3 | kladde chatte tvil v75 | 311 | BL | never fires | BREAK r8 | BREAK r197 | HOLD | BREAK | **1/5** | 8 | never fires |
| `3de9f5e0` | 4 | kladde chatte tvil v75 | 610 | BL | never fires | BREAK r339 | BREAK r325 | BREAK r36 | BREAK | **0/5** | 2 | BREAK r311 |
| `3de9f5e0` | 5 | kladde chatte tvil v75 | 480 | BL | never fires | BREAK r35 | BREAK r352 | BREAK r17 | BREAK | **0/5** | 6 | never fires |
| `6cd1a9a3` | 1 | 0033 v43 | 284 | AW | never fires | HOLD | HOLD | BREAK r29 | HOLD | **3/5** | 0 | BREAK r190 |
| `6cd1a9a3` | 2 | 0033 v43 | 113 | BL | never fires | BREAK r73 | BREAK r73 | HOLD | BREAK | **1/5** | 2 | never fires |
| `6cd1a9a3` | 3 | 0033 v43 | 806 | BL | never fires | BREAK r11 | BREAK r469 | BREAK r100 | BREAK | **0/5** | 6 | never fires |
| `6cd1a9a3` | 4 | 0033 v43 | 453 | BL | never fires | BREAK r26 | BREAK r190 | BREAK r64 | BREAK | **0/5** | 4 | BREAK r254 |
| `6cd1a9a3` | 5 | 0033 v43 | 1000 | AW | HOLD | BREAK r25 | HOLD | BREAK r45 | HOLD | **3/5** | 2 | HOLD |
| `8996dfc2` | 1 | Leviathan v25 | 227 | BW | BREAK r181 | BREAK r14 | HOLD | BREAK r159 | HOLD | **2/5** | 7 | BREAK r137 |
| `8996dfc2` | 2 | Leviathan v25 | 353 | AL | never fires | BREAK r17 | BREAK r94 | BREAK r49 | BREAK | **0/5** | 13 | never fires |
| `8996dfc2` | 3 | Leviathan v25 | 1000 | BW | never fires | BREAK r34 | HOLD | BREAK r100 | HOLD | **2/5** | 5 | BREAK r907 |
| `8996dfc2` | 4 | Leviathan v25 | 275 | BW | BREAK r117 | BREAK r12 | BREAK r12 | BREAK r90 | HOLD | **1/5** | 2 | HOLD |
| `8996dfc2` | 5 | Leviathan v25 | 126 | AL | never fires | BREAK r58 | BREAK r78 | HOLD | BREAK | **1/5** | 4 | never fires |
| `98e2c1fc` | 1 | kladde chatte tvil v75 | 595 | AL | never fires | BREAK r34 | BREAK r24 | BREAK r44 | BREAK | **0/5** | 9 | BREAK r494 |
| `98e2c1fc` | 2 | kladde chatte tvil v75 | 201 | AL | never fires | BREAK r137 | BREAK r137 | BREAK r167 | BREAK | **0/5** | 3 | never fires |
| `98e2c1fc` | 3 | kladde chatte tvil v75 | 797 | AL | never fires | BREAK r184 | BREAK r296 | BREAK r29 | BREAK | **0/5** | 8 | never fires |
| `98e2c1fc` | 4 | kladde chatte tvil v75 | 349 | AL | never fires | BREAK r250 | BREAK r250 | BREAK r28 | BREAK | **0/5** | 3 | never fires |
| `98e2c1fc` | 5 | kladde chatte tvil v75 | 242 | AL | never fires | BREAK r147 | BREAK r147 | BREAK r40 | BREAK | **0/5** | 3 | never fires |
| `b5a37d0b` | 1 | 0033 v43 | 236 | AL | never fires | BREAK r173 | BREAK r173 | BREAK r96 | BREAK | **0/5** | 3 | never fires |
| `b5a37d0b` | 2 | 0033 v43 | 133 | AL | never fires | BREAK r29 | BREAK r78 | BREAK r88 | BREAK | **0/5** | 3 | never fires |
| `b5a37d0b` | 3 | 0033 v43 | 109 | AL | never fires | BREAK r19 | BREAK r19 | BREAK r100 | BREAK | **0/5** | 3 | never fires |
| `b5a37d0b` | 4 | 0033 v43 | 129 | AL | never fires | BREAK r56 | BREAK r56 | BREAK r69 | HOLD | **1/5** | 3 | never fires |
| `b5a37d0b` | 5 | 0033 v43 | 155 | AL | never fires | BREAK r39 | BREAK r39 | BREAK r73 | BREAK | **0/5** | 4 | never fires |
| `fead7e71` | 1 | Leviathan v25 | 102 | AL | never fires | BREAK r24 | BREAK r24 | BREAK r54 | BREAK | **0/5** | 3 | never fires |
| `fead7e71` | 2 | Leviathan v25 | 221 | BW | never fires | BREAK r13 | BREAK r13 | BREAK r181 | HOLD | **1/5** | 8 | never fires |
| `fead7e71` | 3 | Leviathan v25 | 417 | AL | never fires | BREAK r18 | BREAK r62 | BREAK r63 | HOLD | **1/5** | 5 | never fires |
| `fead7e71` | 4 | Leviathan v25 | 142 | AL | never fires | BREAK r11 | BREAK r11 | BREAK r110 | BREAK | **0/5** | 4 | never fires |
| `fead7e71` | 5 | Leviathan v25 | 130 | BW | BREAK r116 | BREAK r45 | HOLD | BREAK r73 | HOLD | **2/5** | 2 | HOLD |

### 6.3 What the scorecard says

**Headline: we score a mean of 0.84 / 5, median 1 / 5, and not one game in 45
plays the eco-optimal signature.**

| score | games | of which we won |
|---|---|---|
| 0/5 | 22 | **0** |
| 1/5 | 13 | 4 |
| 2/5 | 5 | 4 |
| 3/5 | 5 | **5** |
| 4/5 | 0 | — |
| 5/5 | **0** | — |

**The template separates outcomes cleanly and monotonically** — 0/22 wins at 0/5,
5/5 wins at 3/5 — which is the validation that it measures something real. Mean
score in our wins **2.08** (n=13) vs our losses **0.34** (n=32).

| component | broke in | rate |
|---|---|---|
| 1 DELIV-EARLY | 42/45 | 93% |
| 2 FLAT | 43/45 | 96% |
| 3 SIEGE-MINOR | 33/45 | 73% |
| 4 NO-OMISSION | 39/45 | 87% |
| 5 TERMINAL | 30/45 | 67% |

**What breaks first, by round: FLAT in 29 games, NO-OMISSION in 14,
SIEGE-MINOR in 2.** The first thing that goes wrong in our games is a breakage
curve crossing against us — median **3 such crossings per game**, max **20**
(`240a626c` g3), and only **2 of 45 games** have none.

Three findings worth acting on:

1. **Our heal line is fast and outgunned.** Across our 53 substantive sieges the
   median heal latency is **1 round** and 36/53 answer within ≤3 rounds — the
   healers *do* come. But the episode heal/dmg ratio has median **0.73** and
   clears the 0.94 survive lobe in only **16/53**. Component 3 fails almost
   entirely on the *ratio* limb, not the *latency* limb. **The problem is heal
   volume per round, not heal reaction time** — which points at bodies-on-seats
   and seat availability, not at trigger logic. This is a sharper statement of
   v1 §5.1(a).3's "population is a ratio law, not an absolute floor".

2. **The 2:1 delivery gate never fires for us.** D never crosses to us at all in
   **38 of 45** games; component 1 holds in **3/45**. Swapping in the v2 rate
   curve G lifts that only to **5/45**. This is v1 §7 restated on our own games:
   the gate describes economic *suppression*, and we are almost never suppressing.
   **Reported, not moved** — retuning it on the same corpus that exposed it is the
   overfit both briefs forbid.

3. **Component 5 TERMINAL holds in 15/45**, and it is the only component that
   holds more often than it breaks in our wins. The eco strategy's actual win
   route in this corpus is the r1000 tiebreak, not the kill.

**A necessary caveat on the headline.** This corpus was assembled as a **bleed**
corpus — 32 losses to 13 wins. "We play 0.84/5 of our own game" is therefore a
statement about a deliberately adverse sample, not about our overall play. The
right production use is the *per-game* scorecard and the monotone score→result
relationship, not the corpus mean.

### 6.4 Using it as a production read

For a new match window, score each game 0–5 and report the distribution plus what
broke first. The interpretation is calibrated by the table above:

- **0/5** — we did not play our game at all. In this corpus that is 0 wins in 22.
- **1–2/5** — contested; outcome roughly a coin flip (8 wins in 18).
- **3+/5** — we played our game. 5 wins in 5.
- **FLAT breaking before r50** is the earliest actionable alarm: it is the modal
  first break and it precedes everything else.

---

## 7. Published thresholds that underperform — reported, not tuned

Carried forward from v1 §7, re-checked, unchanged:

- **The `≥2:1 AND ≥500 Ti` delivery gate** remains too strict for tiebreak games.
  `98e2c1fc` g5 still misses the ratio limb by **10 Ti out of 9,290** (1.9968).
  v2 does **not** move it. G is added *beside* it as a rate-form curve with its
  own independently-derived deadband; D is untouched, and both are reported.
- **The P (population) threshold** (≤1 builder for 30 rounds) still fires in only
  5 of 50 games while the manual reads name population as primary in 4 games where
  it never fires. v2 does not implement the ratio form either — §6.3 finding 1
  measures the quantity that would drive it (heal volume vs incoming damage), and
  that is the v3 candidate.

New in v2, and reported the same way:

- **T's crossing form is not usable** (46.0% first-crossing precision). The curve
  is sound as a state (100% in-regime from 10% of the game) and its crossings
  before either side has delivered anything are banked-Ti noise. Any future use of
  T should read the state, and any composite that consumes T should gate it on
  "at least one side has delivered", which v2 does **not** do — reported as a
  known limitation rather than patched, since the gate would be a new threshold.

---

## 8. Method spec — the v2 delta

Everything in v1 §10 still applies. The v2 additions:

**Pass 0, supplementary walker** (`tipwalk_sup.py`; stdlib only, reuses
`fields`/`scalars`/`packed_varints` from `tools/replay_census.py`). A *separate*
linear pass, deliberately not folded into v1's walker so `all.json` stays
byte-identical and v1's numbers keep reproducing. Emits per game:
`bank[t][r]` (Player.titanium field 1, carried forward between `updatePlayers`
snapshots, seeded at `STARTING_TITANIUM`) and `ore_total` (count of
`ENV_ORE_TITANIUM` map tiles).

**Pass 5, v2 curves** (`tipv2.py`):
1. `rates()` — trailing-100 delivered-Ti-per-round per side, window clamped at r<100.
2. `tiebreak_curve()` — T, the three-step ladder above.
3. `ttk_states()` — K, per-attacker projected kill round inside the live episode; the curve is the **argmin over the two projections**, never an exclusivity test.
4. `econ_curve()` — G, rate difference against a 2.5 Ti/round deadband.
5. `CONS9` — terminal-first precedence; `CONS9F` (flat 9-vote) computed alongside as the honest comparator.

**Pass 6, tiered annotation** (`v2accept.py`): dominant reason ranked tier-1
(event curves) before tier-2 (always-defined race curves), earliest onset within
tier.

**Runtime.** Supplementary walk 1.3 s for 50 games; all v2 passes 0.3 s on cached
walker output. Cheap enough for every production read.

**Known limits of v2** (in addition to all of v1's, which carry over):

- **T is conditioned on a regime you cannot observe live.** Its 9/9-from-r100
  result holds *given* the game reaches r1000. The branch predicate is a good
  necessary condition (recall 100%) and a weak sufficient one (precision 28%).
- **T's early crossings are meaningless** (banked-Ti ties at zero delivery); use the state.
- **K's crossing form is weak early** (42.9%) and law-grade only from the halfway mark.
- **G is a two-sided rate comparison**, so it says nothing about *absolute* economic health — by construction, per the brief's "if no honest threshold exists, make it comparative".
- **The eco-optimal corpus is loss-weighted** (32L/13W); the mean score is not a fair estimate of our typical play.
- **Class imbalance is unchanged** (15 Leviathan / 10 kladde / 10 0033 / 5 each of the rest); no per-class cell below n=5 should be leaned on, which includes every Clankers, Coreflood and Ouroboros column.
- **The tier assignment is a judgement**, defensible from the always-defined-vs-event distinction but not derivable from a measurement. It is the only structural choice in v2 that is not a game constant or a published law, and it moves strict agreement from 28% to 42% — so it is load-bearing and should be the first thing a reviewer challenges.

---

## 9. So-what

1. **The three holes are closed and the prediction hole is not.** 0/50 unresolved, 100% correct at 90% of the game, full coverage at every sample point — and 58.0% at a quarter of the way in. v1's headline stands verbatim: **we have a very good post-mortem and no eval.**
2. **G is the one new early instrument worth having.** 73.9% on first crossing at 86% of the game remaining, beating the entire ray-coverage family at the same lead. If anything in this document goes into a live decision rule, it is the delivery-rate curve with a one-harvester deadband.
3. **Time-to-kill is a race, not a condition.** The single most useful mechanical finding: 51% of lethal sieges are shorter than the C law's averaging window, and in the game v1 could not resolve, *both* cores were dying — only the order mattered. Any future kill-side logic should compare projected death rounds, not test a threshold.
4. **We essentially never play our own game in this corpus** — mean 0.84/5, no game above 3/5, 0 wins in the 22 games that scored zero. The modal first break is a breakage curve crossing against us, and the modal reason component 3 fails is **heal volume, not heal latency**: our healers arrive in a median of 1 round and still lose the ratio 0.73 to 0.94.
5. **Two v1 thresholds are still wrong and still not moved** (the 2:1 gate, the population floor), and v2 adds a third known-weak form (T's crossings). All three are reported with the measurement that would fix them, for a v3 that has a corpus other than the one that exposed them.

---

## Appendix — scratch (not committed)

`tipwalk_sup.py` (supplementary walker), `tipv2.py` (T/K/G + CONS9),
`v2verify.py` / `v2sweep.py` / `v2verify2.py` (v1 reproduction),
`v2measure.py` (M1–M4), `v2accept.py` (acceptance battery),
`v2selfcheck.py` (identities + matched-coverage earliness),
`v2eco.py` (eco-optimal scorecards), `v2md.py` (table emission).
All in the session scratchpad, alongside v1's `tipwalk.py` / `tipeval.py` /
`tipadv.py` / `tiptable.py` / `manual.py` / `corpus.json`, which are reused
unmodified. **Read-only throughout: no bots edited, no arena or platform commands
run, no downloads, no HANDOVER or tape writes.**
