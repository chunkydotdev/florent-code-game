# PREREG — LOKI-20: GUNS NOT WALLS. **PROBE TIER.**

**Written 2026-08-11 08:4xZ by the s30 BUILDER. Committed BEFORE submission and
before any LOKI-20 game exists anywhere.** Tree `bots/_v137loki20`, py-tree md5
`c7a6a042`. Diff vs v104 (`bots/_v130loki13`): **one flag + one reorder**, in
`doctrine.py` and `raid.py`; `main.py` and `eco.py` byte-identical.

```
TARGET BAND: the whole reachable band, us−80..us+125, a 5-0 pays +12.8..+21.4,
             reachable YES  (tools/target_value.py --band, our 1686)
```

## 1. THE PLANK — a preference order, not a mechanism

`_raid_act` tries, in order: peck (silenced) → **seal a seat with a BARRIER** →
forward sentinel → buddy heal. **LOKI-20 tries the sentinel BEFORE the barrier.**
Nothing is added, removed or re-costed.

**ON PROGRAMME:** a forward turret opens a lane to their core; a barrier seals a
spawn seat, which is denial. `PLAY_DEFENCE: never` prefers the gun.

## 2. THE FIELD EVIDENCE — motivation, entering no bar (§2 rule inherited)

Forward turret in the **enemy half by ~r20–25**: ρ=**+0.784** across 71 teams,
**dominating generic forward building** (partial +0.452 vs +0.124), within-team
p<0.0001, 8 independent teams, **+0.685 with rating partialled out**, and reverse
causality tested (opponent losses by r30 are flat-to-LOWER in fast games,
p=0.0005). **We sit at first forward turret median r49 (v104) against r23 for the
fast killers, and our forward builds are 81% BARRIER / 13% turret against their
64% turret / 16% barrier — while we lay MORE forward builds per game than they
do.** Out-of-sample control the league supplied itself: HTTP 418 and not adgato
share our barrier composition, have top-decile forward volume, and 4.5%/8.8%
fast kills.

## 3. ⛔ THE FALSIFIER IS OUR OWN HISTORY, AND IT CONTRADICTS THE FIELD

| version | fwd turrets by r40 | fast-kill rate |
|---|---:|---:|
| v92 | 0.70 | 11.1% |
| v104 | 0.34 | 22.3% |
| v107 | **0.15** | **31.3%** |

**Our siting got monotonically WORSE while our speed got monotonically BETTER.**
Either the forward-barrier plank delivers the same tempo by another channel, or
**the league correlation does not transfer to this chassis.** A leg that moves
the mechanism and not the speed has found the second, and that is a result.

## 4. ⛔⛔ THE LOCAL DOSE MOVED THE WRONG WAY, AND IT IS RECORDED BEFORE FIRING

One local game vs `_det_opp_v63`, ours, forward builds (d²_enemy < d²_own):

| | forward builds | barrier share | turret share | fwd turrets by r40 |
|---|---:|---:|---:|---:|
| v104 | 6 | 33% | 17% | 1 |
| **LOKI-20** | **17** | 18% | **6%** | **0** |

**The treatment unmistakably CHANGES BEHAVIOUR — 6 → 17 forward builds — so the
dose fires. But the composition moved AGAINST the plank's intent: turret share
FELL and forward turrets by r40 went 1 → 0.**

**I am firing anyway, and the reason is stated in advance rather than
reconstructed after:** this is **n=1 against `_det_opp_v63`, one of our own
probes**, and `FIXTURE_OF_RECORD: live_unrated` exists precisely because that
pool lies in a known direction. **Pre-judging a live leg on one local game
against a fixture we wrote is the echo loop the programme forbids.**
**But it is a real adverse signal and it is on the record: if the live arm
reproduces it, the plank is refuted by its own dose and I do not get to discover
that at read-out.**

## 5. BARS

* **5a DOSE (live) — GO/NO-GO.** Forward turret share of our forward builds, and
  forward turrets built by r40, ours, live unrated. **Treatment must DIFFER from
  control.** If it does not, VOID — implementation failure, no claim.
* **5b MECHANISM.** First-forward-turret round, ours. *What moves it: the reorder,
  and nothing else in the diff.*
* **5c CURRENCY — NOT RESOLVABLE AT THIS n AND NOT CLAIMED.** Stated now.
* **5d COST.** Barrier seals per game must not collapse to zero — the seal is a
  real behaviour and trading all of it for turrets is a different plank.

## 6. n AND WHAT RESOLVES

**PROBE: 25 games, one window.** Control: the ~400 banked v104 games, **blocked
not interleaved** — disclosed, same compromise and same inherited fixture
imbalance as LOKI-18's Amendment 1.3.

| item | kind | resolves at 25? |
|---|---|---|
| 5a dose | GATE | **YES** — a build-mix shift is visible at 25 games |
| 5b mechanism | BAR | **PARTIALLY** — a large shift in first-turret round, not a small one |
| 5c currency | BAR | **NO. Not claimed under any result.** |
| 5d cost | BAR | **YES for a collapse to zero**, no for a small fall |

**PROBE TIER MEANS LESS WRITE-UP, NOT LESS VERIFICATION** — the lesson from the
LOKI-16b probe ninety minutes ago, where I skipped this document's own gate.

## 7. OBLIGATION 13

```
MECHANISM METRIC READS: bots/_v137loki20/raid.py:267
TREATMENT DIFF TOUCHES: raid.py, doctrine.py
INTERSECTION: raid.py
```
**Asserted by `tools/inert_check.py` BEFORE submission, not after.**

## 8. WHAT THIS PROBE MAY NOT DO

No currency claim. No verdict. It may not borrow LOKI-16's or LOKI-19's bars. It
may not treat the local dose as evidence of effect **in either direction**. And
it may not be read as confirming the field correlation — §3's falsifier is our
own chassis contradicting it, and one probe does not settle that.
