# Builder-death attribution: no crashes, and the killer is a planted gunner (side lane deliverable)

**Side research lane, 2026-08-09. Closes the home-band death question and the
crash hypothesis. Attribution validated: death-round attributed damage equals
HP-stream loss 99.45% (US) / 99.48% (field); lifetime damage >=40 HP on
19,993/19,993 damage-killed builders; no damage value of 2 in 20,929 deaths
(builders never kill builders, empirically); 0 deaths on throw rounds.**


**Read-only research, 2026-08-09.** Corpus: the 2,735 attributed replays of
`scratchpad/rxfiles.txt` (same provenance as `scratchpad/reaction-atlas.md`
§Provenance; `attrib2.tsv` maps file -> side names). Decoder:
`scratchpad/deathcause/dc_decode.py`, 2,735 files / 0 errors / 22 s.
**20,929 builder-bot deaths**: US 8,664 over 860 team-sides, field 12,265 over
2,214 team-sides.

## Method, and why it can be trusted

The rule constraint the proposal missed is confirmed by the tape: **a builder
attack can never kill a builder bot.** So a builder-bot death has only two
possible causes — turret fire, or a removal with no damage at all.

* **Ground truth for "how much damage" is the HP ledger** (`UpdateHp`, Update
  field 5; `delta` is a 64-bit two's-complement varint — corpus-howto trap 2).
* **Attribution of "who" is `FireTurret`** (field 12), shooter = the building on
  `from` at round start, damage = 7 (gunner) / 18 (sentinel) / 0 (launcher).
* Targets are resolved against **every tile the victim held during the round**
  (round-start position plus each move destination), because `FireTurret` can be
  emitted *after* the victim's `removeEntity` in the same round — the S1
  ordering trap in `tools/replay_schema.md`.
* **Friendly fire is real and is not filtered out.** Turret fire hits whatever
  unit stands on the target tile, own team included. Verified case:
  `010eb62d..._game_3`, a **team-0** gunner at (17,10) shooting the enemy
  conveyor at (18,10) killed **its own** builder bot 5 standing on that tile
  (r112). Filtering to enemy shooters alone loses ~10% of deaths.

### Reconciliation (the validation the verdict rests on)

| check | result |
| --- | --- |
| death-round attributed shot damage **exactly equals** death-round HP loss | **US 8,616/8,664 = 99.45%**, FIELD 12,201/12,265 = **99.48%** |
| damage-killed builders whose **lifetime** cumulative damage >= max HP (40) | **19,993 / 19,993 = 100.000%** |
| residual | 112 rows (0.54%) labelled AMBIGUOUS — two bots contesting one tile inside a round |

Death-round HP-loss values are quantised to turret damage and to nothing else:

```
7: 13,179   18: 5,402   14: 939   36: 221   25: 160   54: 39   21: 35   ...
```

`7`=gunner, `18`=sentinel, `14`=2 gunners, `36`=2 sentinels, `25`=gunner+sentinel.
**No death-round HP loss of 2 exists anywhere in 20,929 deaths** — direct
confirmation that builder attacks (2 dmg) never touch a builder bot. And **0 of
20,929 deaths occurred on a round the victim was thrown** — launcher throws deal
no damage.

---

## 1. Cause of death, US vs FIELD, by band

HOME = the victim's tile within d² <= 32 of **its own** core (core position =
NW corner of the 2x2, matching `ct.get_position()`); FORWARD = everything else.

| side | band | n | enemy GUNNER | enemy SENTINEL | mixed | own-turret friendly fire | **no-damage removal** | ambiguous |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **US** | HOME | 4,285 | **83.22%** | **15.64%** | 0.40% | 0.14% | **0.00%** | 0.61% |
| **US** | FWD | 4,379 | 91.94% | 6.65% | 0.39% | 0.53% | **0.00%** | 0.50% |
| **US** | ALL | 8,664 | 87.63% | 11.09% | 0.39% | 0.33% | **0.00%** | 0.55% |
| FIELD (all non-US sides) | HOME | 5,435 | 58.60% | 29.37% | 0.42% | 4.32% | 6.72% | 0.57% |
| FIELD | FWD | 6,830 | 42.77% | 45.10% | 1.70% | 3.24% | 6.72% | 0.48% |
| FIELD | ALL | 12,265 | 49.78% | 38.12% | 1.13% | 3.72% | 6.72% | 0.52% |

"FIELD" mixes two different populations, and the split matters:

| population | band | n | gunner | sentinel | own-fire | no-damage |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| **FIELD_vsUS** (sides playing *against* us — killed by *our* turrets) | HOME | 1,801 | 56.30% | 38.15% | 1.44% | 3.16% |
| FIELD_vsUS | FWD | 3,612 | 23.50% | 67.58% | 3.65% | 1.83% |
| **FIELD_pure** (games with neither side us) | HOME | 3,634 | 59.74% | 25.01% | 5.75% | 8.48% |
| FIELD_pure | FWD | 3,218 | 64.39% | 19.86% | 2.77% | 12.21% |

**The "different killers" dissolver is real, and it points the other way from
the proposal.** We die at home to *gunners* — a short-range (r²=13),
line-of-sight weapon — in 83% of cases. Our opponents' home deaths are only 56%
gunner and 38% sentinel. And the field carries a 6.7% no-damage class that we do
not have at all.

---

## 2. The exposure control: the 49.5% claim, normalised

**Exposure was computable** — one builder-round per living builder per round,
bucketed by band, straight out of the same pass (13.0M US + field builder-rounds).

| population | home share of **deaths** | home share of **builder-rounds** | deaths / 1k builder-rounds HOME | FWD | HOME/FWD |
| --- | ---: | ---: | ---: | ---: | ---: |
| **US** | **49.5%** | **59.2%** | **1.968** | 2.915 | 0.68 |
| **FIELD_vsUS** | **33.3%** | 51.7% | **1.063** | 2.283 | 0.47 |
| FIELD (all) | 44.3% | 58.5% | 0.717 | 1.269 | 0.56 |
| FIELD_pure | 53.0% | 60.8% | 0.617 | 0.847 | 0.73 |

The background claim's 33.5% field figure reproduces as **33.3% for
FIELD_vsUS** — so the original comparison was us against *our opponents*, not
against the whole field (the whole field is 44.3%, and games we are not in are
53.0%).

**Verdict on the 49.5% number: about half of it is exposure, and the rest is a
real hazard gap.**

* We station **59.2%** of our builder-rounds inside the home band; our opponents
  station **51.7%**. That alone moves the share.
* Normalised, **home is the safer band for both sides** (US 1.968 vs 2.915
  forward; opponents 1.063 vs 2.283). "49.5% of deaths at home" is not evidence
  of a home-defence failure on its face.
* But our **home hazard is 1.85x our opponents'** (1.968 vs 1.063 deaths per
  1,000 home builder-rounds), and our overall builder hazard is **2.355 vs 1.652
  per 1k builder-rounds (1.43x)**, against 0.946 for the field at large (2.5x).

Sensitivity: measuring the band from the nearest core-footprint tile instead of
the NW corner moves the shares (US 55.8%, FIELD_vsUS 48.3%) but barely moves the
rates (US 2.063 HOME / 2.868 FWD). The conclusion is not an artefact of the cut.

---

## 3. US home-band turret kills: which turret, at what range

US HOME deaths with an attributed turret, **n = 4,259**:

| killer | n | share of US home turret deaths |
| --- | ---: | ---: |
| enemy **gunner** only | 3,567 | **83.8%** |
| enemy **sentinel** involved | 687 | **16.1%** |
| own-turret friendly fire | 5 | 0.1% |

**The sentinel-outrange answer: 329 deaths = 7.7% of US home turret deaths came
from a sentinel firing at r² > 13** (beyond any gunner's reach, through
friendlies). That is 47.9% of our sentinel deaths, but only 7.7% of the home
band.

Sentinel shooter distance to the victim, cumulative:

```
d²<=4  26.8%   d²<=8  39.7%   d²<=18  68.7%   d²<=25  85.9%   d²<=32 100.0%
```

**Over a quarter of sentinel kills on our home builders are point-blank
(d² <= 4).** For contrast, the field's home band is 32.1% sentinel-killed with
17.9% of all home deaths beyond gunner reach — more than double our rate.

**Design read-across:** a heal detail standing adjacent to its heal target and
dying to an outranging sentinel line is a **real but minority** mechanism — 7.7%
of our home builder deaths. It does not explain the home-band hazard. A design
that only answers the long sentinel leaves 92% of the problem untouched.

### Where the killing turret actually stands

| population | band | n | killer turret inside the **victim's own** home band (d²<=32 of own core) | median shooter->own-core d² |
| --- | --- | ---: | ---: | ---: |
| US | HOME | 4,254 | **77.1%** | 20 (p25 13, p75 29) |
| US | FWD | 4,334 | 3.1% | 85 |
| FIELD | HOME | 4,807 | 73.6% | 17 |

**65.3% of all our home builder deaths are an enemy *gunner* standing inside
d²<=32 of our own core** — an enemy turret planted in our base, not a
long-range shot into it. This sits directly beside the background finding that
our home turrets are the best-surviving in the corpus: our turrets live, but
they are not preventing enemy turrets from being planted next to our core and
grinding our builders there.

The grinding is concentrated: 4,254 US home deaths come from only **1,559
distinct (game, side, shooter tile) killers** (mean 2.73 kills each, max 45).
Killer tiles with >=5 kills account for **47.3%** of our home deaths, and tiles
with >=10 kills for **23.4%**. Median of **2** distinct killer tiles per US
team-side. A small number of parked enemy gunners does most of the damage.

Worst home-band matchups (US deaths per 1k home builder-rounds, sides with
>20k home builder-rounds):

| opponent | US home deaths | home builder-rounds | rate | sentinel share |
| --- | ---: | ---: | ---: | ---: |
| Ouroboros | 851 | 143,201 | **5.943** | 0.0% |
| Lunds Stallions | 1,050 | 219,038 | **4.794** | 24.3% |
| Powerpuff Girls | 770 | 234,298 | **3.286** | 3.9% |
| Kings College Munich | 409 | 193,573 | 2.113 | 5.4% |
| Orizon | 104 | 49,650 | 2.095 | 0.0% |
| Banminary | 80 | 42,103 | 1.900 | 93.8% |
| CtrlAltDefeat | 220 | 144,308 | 1.525 | 0.0% |
| Memtrace | 119 | 171,978 | 0.692 | 70.6% |

The three teams that hurt us most at home do it with **gunners, essentially
never with sentinels**.

---

## 4. No-damage removals: the alarm does NOT fire for us

**US: 0 no-damage removals in 8,664 builder deaths (0.00%).** Every single US
builder-bot death in the corpus is explained by turret damage. There is **no
crash signature and no self-destruct signature in our bot**, at home or forward,
in any phase. This is consistent with the code: `bots/_v100hf/main.py:1491`
wraps the whole of `run()` in `try/except Exception`, and the file contains
**zero** `self_destruct` calls.

The field, by contrast, carries 824 no-damage removals (6.72% overall; 8.5–12.2%
in games we are not in), and they are concentrated in specific teams and in the
opening:

| team | no-damage / total builder deaths | rate |
| --- | --- | ---: |
| vjg | 387 / 396 | 97.7% |
| S | 101 / 111 | 91.0% |
| Troupe | 96 / 110 | 87.3% |
| Ship Happens | 41 / 54 | 75.9% |
| Cookie | 47 / 103 | 45.6% |
| Ouroboros | 74 / 254 | 29.1% |
| Coreflood | 14 / 63 | 22.2% |
| I Stone | 43 / 235 | 18.3% |

Phase profile (field): 56.1% of no-damage removals happen in r0-99, where they
are **18.8%** of all deaths, falling to 5.0% (r100-299), 3.2% (r300-599) and
2.2% (r600+). Median lifetime of a no-damage-removed bot is 56 rounds
(p10 = 8, p90 = 335). 9.2% had taken damage earlier in life; 2 of 824 were on
the game's final round; **0** were thrown that round.

**Honest limit: crash and self-destruct are NOT separable from the archive.**
The engine prints a traceback for a unit whose `run()` raises, and `BotOutput`
(Update field 9) carries stdout — but **stdout is stripped from every archived
replay**: across 120 random replays, **0 of 1,250,708 `BotOutput` events carry
any stdout at all**. The traceback discriminator does not exist in this corpus.
These 824 rows are therefore labelled `NO_DAMAGE / UNEXPLAINED`, never guessed.
(`tled` *is* recorded and is common — 2,681 timed-out turns in two replays of one
match — but a TLE interrupts a turn, it does not destroy the unit.)

---

## What this changes

1. **The 49.5% home-death share is not, by itself, a finding.** Normalised by
   exposure, home is the *safer* band for us (1.968 vs 2.915 per 1k
   builder-rounds). The share is inflated because 59.2% of our builder-rounds
   are spent at home.
2. **The real gap is hazard, not geography.** We lose builders at 1.43x our
   opponents' rate per builder-round overall, and 1.85x at home.
3. **The killer is a short-range enemy gunner planted inside our base** — 65.3%
   of US home builder deaths, with 77.1% of home killers sitting within d²<=32 of
   *our* core, and half the damage done by turret tiles that kill >=5 of our
   builders each. This is an in-base turret-clearing problem, not a
   long-range-fire problem.
4. **The sentinel-outrange hypothesis prices at 7.7%** of US home builder deaths.
   Worth something, not worth a redesign on its own; and a quarter of our
   sentinel deaths are point-blank (d²<=4) anyway.
5. **No live code defect.** Zero no-damage removals on our side rules out the
   crash-death hypothesis for our bot outright.

## Files

* `scratchpad/deathcause/dc_decode.py` — decoder (read-only, scratchpad output).
* `scratchpad/deathcause/out/dc_deaths.tsv` — 20,929 death rows, 31 columns.
* `scratchpad/deathcause/out/dc_expo.tsv` — per-file per-team-per-band builder-round exposure.
* `scratchpad/deathcause/analyse.py`, `analyse2.py` — the tables above.
* `scratchpad/deathcause/pilot.py`, `pilot2.py`, `dbg.py` — validation pilots.
