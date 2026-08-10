# PREREG — LOKI-18: A FORWARD SENTINEL AIMS AT THE CORE, NOT AT A THREAT

**PROVENANCE: our own replay archive + a code read.** No tactics-library file
spoke to this; it came from decoding 185 of our own games and then reading the
two call sites.

**TARGET BAND: every opponent we are paired with** — a fix to our own play, so it
pays across the reachable band (`us−80…us+125`, 18 teams, a 5-0 paying +12.56 to
+21.30) rather than a chosen stratum.

**Committed BEFORE any bot edit for this plank exists.**

## ⛔ WHY LOKI-17 IS SUPERSEDED — ITS EDIT IS IN A PATH THAT BUILDS ~NONE OF THE SENTINELS

Measured, 528 sentinels across 185 real games (v104): **327 forward sentinels
(d² > 41 from our own core), 97.6% within range of the enemy core, and 0.0%
able to fire at it on the round they are built.** Opponents pooled 1.6%, best
(Askar City) 7.7%.

The live tree has **exactly two** `build_sentinel` call sites:

| site | its `can_fire_from` target | consequence |
|---|---|---|
| `raid.py:439` | **a CORE TILE** | **shootable-at-core BY CONSTRUCTION** |
| `main.py:574` | **a THREAT** (`SLOT_THREAT`, an enemy unit) | aimed at a transient body |

**A sentinel from `raid.py` cannot be non-shootable — the guard forbids it. We
observe 0 of 319 shootable. Therefore essentially NONE of our forward sentinels
come from `raid.py`; they come from the threat-aimed path.**

**LOKI-17's edit (first-fit → best-fit) is inside `raid.py`. It refines the
ordering of a path that builds approximately zero of the population its own
primary measures.** It is not wrong — it is inert. **This is the mechanism gate
doing its job: the plank is retired before a single rate-limited game was spent
on it.**

## The plank

**When a builder is FORWARD and an enemy core tile is in sentinel range, aim the
sentinel at the CORE rather than at the current threat.** The threat-aimed
behaviour is correct at home and is left untouched.

## Bars, stated before the edit exists

1. **PRIMARY (mechanism), on the ENGINE-EXACT ray predicate** — a single-tile
   line shot, validated by research at 12,759/12,759 `FireTurret` events with
   one compass step of rotation taking it to 0.0000:
   **forward shootable-on-build rises 0.0% → ≥ 40%.**
   *Not 85%: that figure came from a 45° tolerance statistic and is not
   comparable. 40% is ~5x the best value observed in this population (Askar
   7.7%) and is the first bar in this project set on the engine's own rule.*
2. **GUARD AGAINST THE OBVIOUS REGRESSION:** home sentinels must NOT lose their
   threat aim — **home shootable-at-threat must not fall**, and total sentinels
   built must not drop by more than 20%.
3. **CURRENCY:** median game length **< 300 rounds** and core-kill share rises,
   read per ring-stratum. **Never a win rate.**
4. **FALSIFIER:** if forward shootable rises above the bar and **core-kill share
   does not move**, then aiming was never the constraint — **the sentinel is not
   what kills the core** — and the launcher/insertion road is the lever instead.

## What this leg may not do

No threshold here may be revised because an implementation reached a different
number. The 0.0% baseline is measured on 319 forward sentinels across 185 real
games and is not an estimate.
