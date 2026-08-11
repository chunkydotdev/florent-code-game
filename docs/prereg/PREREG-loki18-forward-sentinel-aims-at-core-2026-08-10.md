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

---

# AMENDMENT 1 — FIRING PARAMETERS, THE NEW MECHANISM STORY, AND A RESOLUTION TABLE THAT SIZES THE GATES AS WELL AS THE BARS

**Written 2026-08-11 by the s30 BUILDER. ADD-ONLY. Committed BEFORE the tree is
submitted and before any LOKI-18 game exists anywhere — the two-clock standard,
git author time vs platform `createdAt`.** `bots/_v135loki18` (py-tree md5
`bfac4615`) was built on 2026-08-10 and has never been fired. **No bar, guard,
falsifier or threshold in the document above is touched.** This amendment adds
firing parameters, records a mechanism the original could not have known, and
supplies a resolution table the original does not have.

```
TARGET BAND: the whole reachable band, us−80..us+125, 18 teams,
             a 5-0 pays +12.82..+21.36, reachable YES
```
*(verbatim `tools/target_value.py --band` at our 1685, run before this amendment
was written. LOKI-18 is a fix to OUR OWN PLAY, so unlike a stratum-specific
plank it pays wherever we are paired — which is why the band and not a chosen
cell list is the gate line.)*

## A1.1 ⭐ THE MECHANISM STORY CHANGED TODAY, AND IT CHANGED IN THIS PLANK'S FAVOUR

The document above justifies the plank on a **defect**: 327 forward sentinels,
97.6% already in range of the enemy core, **0.0% able to fire at it on the round
they are built.** That stands and is not an estimate.

**What is new is WHY IT MATTERS, and it comes from LOKI-19's read-out four hours
ago rather than from this plank's own evidence:**

* The core peck delivers real damage and **the opponents answer it with healing
  in five cells out of five** (`docs/legs/LEG-loki19-core-peck-readout-2026-08-11.md` §11).
* Research's follow-up (`docs/research/HEAL-RESPONSE-loki19-s11-2026-08-11.md`)
  measures the defenders' response as a **LEVEL, not a trigger**: on the control
  arm — which has **zero** pecks by construction — they already heal back
  **0.763 HP per HP our turrets remove**, r=0.858, n=50.
* **But healing is THROUGHPUT-CAPPED at 4 HP per builder per turn, and they run
  almost no healers**: 1.08 distinct core-healers per game, peak simultaneous
  0.86, **maximum ever observed across 100 games: 4.** Realised throughput
  ~6 HP/round typical, ~16 HP/round at the ceiling.
* **A sentinel is 18 damage on a 2-round reload = 9 HP/round.** One forward
  sentinel firing at the core **exceeds their typical realised heal throughput
  on its own**; two exceed even the 4-healer ceiling.

**⇒ THE BINDING QUANTITY IS BURST AGAINST THEIR HEALER COUNT, NOT CUMULATIVE
DAMAGE — and cumulative damage is precisely what a 0.763 coefficient eats.**
This plank is the cheapest available instance of concentration: it buys no new
unit, spends no titanium, and changes only where a turret we already built is
pointed. **Today 0.0% of them point at the thing that cannot dodge.**

**⛔ AND THIS PARAGRAPH MAY NOT BE READ AS EVIDENCE FOR THE PLANK.** It is a
motivation for spending the window, in the same class the six-roads queue calls
"prioritises a road, closes none". The heal figures come from a tool
(`scratchpad/hp_ledger.py`) with **no selftest**, whose magnitude LOKI-19's
read-out fenced as **instrument-unverified**; research's `heal_read.py` has six
forced-answer cells and three caught mutations and is the better instrument, but
neither has been tested against a burst intervention. **Nothing in §A1.1 enters
a bar. Every bar in this document remains the one written on 2026-08-10, before
any of this was known.**

## A1.2 FIRING PARAMETERS

* **Treatment:** `bots/_v135loki18`, py-tree md5 `bfac4615`. Diff against the
  live tree `bots/_v130loki13` is **one hunk in `main.py:560`** and nothing else;
  `raid.py`, `eco.py` and `doctrine.py` are byte-identical. The edit is wrapped
  in `try/except` so a scope or geometry error degrades to the incumbent's
  threat aim rather than destroying the unit.
* **Comparator:** v104 (`bots/_v130loki13`), per `COMPARE_AGAINST:
  previous_line_iteration`.
* **Cells:** the four PANEL-3 admitted cells plus Landers — Askar City, Lunds
  Stallions, Powered by SmartFridge, farming_200s, Landers. **Chosen for
  continuity with today's banked control, not for expected effect.**
* **n, window 1:** 5 challenges × 5 games = **25 treatment games.**
* **Runner:** `tools/unrated_run.sh` and nothing hand-rolled.

## A1.3 ⛔ THE CONTROL IS RE-USED, NOT FRESH, AND THAT IS A DESIGN COMPROMISE I AM DECLARING IN ADVANCE

**The control arm is the 50 v104 games already banked this morning as LOKI-19's
control** (`scratchpad/arm_loki19_ctrl_w1.txt` +
`scratchpad/arm_unrated_v104_20260811T052031Z.txt`, fired 04:35–05:31Z). They are
plain v104 on these same five cells with no treatment of any kind, so they are a
valid comparator for **any** v104-vs-X question.

**WHAT THIS COSTS, stated now rather than discovered at read-out:**
1. **THE DESIGN IS BLOCKED, NOT INTERLEAVED.** LOKI-19's own §6 says a block
   design confounds arm with time-of-day and with opponent version drift, and I
   am knowingly accepting that here to buy a same-session read on a plank that
   has sat unfired for a day. **The read-out must say "blocked, ~2 hours apart",
   not "paired".**
2. **THE CELL AND SEAT MIX WILL NOT MATCH** — the control carries a farming_200s
   double and only 5 Landers games, and its seat mix differed in all five cells
   against LOKI-19's treatment. **The same single confound LOKI-19 §6 names —
   the arms are not balanced on the fixture axes — applies here and is inherited,
   not avoided.**
3. **MITIGATION, pre-committed:** if the mechanism bar (bar 1) clears, **a fresh
   interleaved v104 control is fired before any currency claim is made.** Bar 1
   is a property of our own build decisions and is the bar least exposed to the
   blocking; bar 3 is the most exposed and may not be read on a blocked design.

## A1.4 ⭐ THE RESOLUTION TABLE — AND IT SIZES THE GATES, WHICH IS THE ONE THING LOKI-19'S DID NOT

**This exists because LOKI-19 §6 tabulated what resolves at n=50/arm for all
four BARS and never asked it of gate 5a-bis — which then arrived under-resolved
and decided what the leg was allowed to claim.** The standing rule adopted from
that read-out: **a prereg's resolution table must include every GATE, not only
every BAR, and the pre-committed default when a gate does not discriminate is
the RESTRICTION.**

| item | kind | resolves at 25 treatment games? |
|---|---|---|
| **bar 1, forward shootable-on-build 0.0% → ≥40%** | BAR | **YES.** ~1.8 forward sentinels/game ⇒ ~45 events. Against a control baseline measured at **0/319**, any rate near 40% is unmistakable at that n. This is the bar the leg is being fired for. |
| **bar 2, home shootable + total sentinels built** | GUARD | **YES for a large regression, NO for a small one.** The −20% build-count clause is a per-game mean over 25 games and will not resolve a 5% change. |
| **bar 3, currency (median length < 300, core-kill share)** | BAR | **NO — stated before firing.** LOKI-19 measured the MDE on core-kill share at **28.0pp on 50 games/arm**; at 25 treatment games against a blocked control it is worse. **No currency claim may be made from window 1 under any result.** |
| **bar 4, the falsifier** (shootable rises, share does not move) | BAR | **NO, AND THIS IS THE IMPORTANT ROW.** The falsifier is a conjunction whose second half is bar 3, which does not resolve. **⇒ THE FALSIFIER CANNOT FIRE ON WINDOW 1. A null on core-kill share here is NOT evidence that aiming was never the constraint**, and writing it as such would be reading an unpowered comparison as a refutation. |
| **the DOSE gate** (does the edit change any aim at all) | GATE | **YES.** Measured as forward sentinels whose build-round facing differs from the incumbent's threat aim. **If the dose reads ~0, the leg is VOID and no bar is read** — an implementation failure, not evidence about aiming. |
| **the ADMISSION gate** (do these cells produce forward sentinels) | GATE | **PARTIALLY, AND IT IS MEASURED IN-ARM BEFORE ANY BAR IS READ.** Precondition is that we build sentinels forward at all. Base rate ~1.8/game pooled over 185 games, **but it has never been cut per cell**, and LOKI-19 learned that a panel admitted for RESOLUTION need not admit a given MECHANISM. **If a cell produces <5 forward sentinels across its 5 games, that cell is reported as UNDER-DOSED and contributes to no bar.** Default on non-discrimination is the restriction. |

## A1.5 WHAT WINDOW 1 MAY CLAIM, PRE-COMMITTED

| outcome | how it MUST be written |
|---|---|
| dose fires, forward shootable ≥40% | *"the mechanism bar clears at n=25 on a BLOCKED control; a fresh interleaved control is now justified and no currency claim is made."* **"Confirmed" FORBIDDEN.** |
| dose fires, forward shootable rises but <40% | *"the aim changes and the bar is missed at this n."* Report the rate with its event count. **"Refuted" FORBIDDEN** — 25 games is a dose-and-mechanism probe. |
| dose reads ~0 | **VOID.** Implementation failure. No claim about aiming in either direction. |
| any currency movement | **REPORTED AS OBSERVED, NEVER AS A RESULT.** Bar 3 does not resolve at this n and bar 4 cannot fire. |

## A1.6 WHAT THIS AMENDMENT MAY NOT DO

It may not move bar 1's 40%, bar 2's −20%, bar 3's 300 rounds, or bar 4's
conjunction. It may not read §A1.1's healing arithmetic as evidence for the
plank. It may not upgrade the re-used control into a paired design. And it may
not revise the 0.0%/319 baseline, which is measured and not an estimate.
