# The unrated campaign plan: Ouroboros first, one trick, one clean A/B — and why the five teams are TWO problems, not one

**Side lane, 2026-08-09 15:31 CEST, answering Magnus: one opponent first or
spread? which maps, which teams? The pre-autopsy of Ouroboros (85 decoded
games) makes the call — focus one, and it splits the campaign in two.**

## The finding that decides it: the five hard teams are two different weapons

I autopsied our two worst matchups from already-decoded games. They lose to us
by **opposite mechanisms**, which means one trick cannot answer both:

| | Ouroboros | CtrlAltDefeat |
| --- | --- | --- |
| kills our core with | **pure GUNNER grind** (7,831 gun / **0** sen shots) | **sentinel-led siege** (65% sentinel damage) |
| gunner = point-blank → **tile-contestable?** | **YES** (d²≤13, barriers/collar reach it) | no (sentinel ignores obstacles) |
| core death timing | slow grind, median **r369** | median r361 |
| do we win the tiebreak? | **NO — 22%** (they out-economy us too) | **YES — 16-4 / ~80%** |
| so the objective is | **KILL them** (survive ≠ win) | **SURVIVE to r1000** (survive = win) |
| contests our rush? | **NO** (0 launchers, 0 enemy throws) | some |
| version stability | **STATIC** (v8, 373 matches) | churns constantly |

**Do not run one campaign against "the five teams."** Ouroboros wants an
offensive rush; CAD wants patient survival. Running a single trick against both
is the win-and-lose-the-same-games trap.

## PHASE 1 — Ouroboros, and it is the near-perfect first subject

Every property lines up for a clean experiment:

1. **Worst matchup (15.3%)** — biggest headroom, so any flip is worth the most.
2. **Static (v8, 373 matches)** — a tuned trick STAYS tuned; the before/after is
   not contaminated by them patching. This is the cleanest A/B on the ladder.
3. **Cannot contest the rush** — 0 launchers, 0 enemy throws in 85 games, so our
   insertion/rush runs uninterrupted.
4. **We lose anyway (85%), so an all-in rush has no downside** — variance is
   free when the base rate is a loss. This is exactly where to spend an
   aggressive variant.
5. **Their grind is SLOW (r369) and their weapon is CONTESTABLE** — a rush that
   kills by ~r52 wins the race outright, and if it stalls, barriers/collar (A3)
   can actually blunt a point-blank gunner (unlike a sentinel).

**The trick to test first: Loki-2 (the rush), ALONE.** Prediction, pre-registered
before the build: on Ouroboros's 0%-maps, Loki-2 converts core-losses to
core-**wins** (baseline: we win only 10% of core-decided games vs them).

**Maps (the `--map` targets, its worst, all n≥3):**
`lighthouse` (0/7), `atoll` (0/7), `eider` (0/7), `drumlin` (0/3), and
`hive`/`saga` as the 5th. Baseline on these is ~0%, so **any win is signal.**

**The closed loop (per loss-autopsy-method):**
`fcode match unrated <Ouroboros teamId a5631594...> --map lighthouse atoll eider drumlin hive`
→ archive the replays → I autopsy → **did the predicted games flip?**
- Flip → the rush works vs the gunner class; NOT-REFUTED (n=10), promote toward
  a ship.
- **Non-flips → they had a second cause the rush didn't fix** → add A3
  (spawn-ring to deny their gunner grind while we land the rush) and re-run.
  The non-flips ARE the "do we need a combination" answer, measured.

## PHASE 2 — a sentinel team (CAD or Lunds), a SEPARATE experiment

Only after Phase 1's loop closes. Different objective (survive-to-r1000 already
wins vs CAD), different trick (the sentinel-vs-sentinel race needs A1+A3
together, per the CAD autopsy: 18/47 losses are sentinel-led and a gunner-only
rush loses them). Lunds is the alternative Phase-2 subject — most games (180),
also loses us on the same sentinel maps, AND is separately the most
meta-manipulable team (a lopsided loss may revert them onto an older binary).

## Why NOT spread across all five at once

- The rate limit is **5 unrated/10 min**; spreading five teams × five maps
  dilutes n below the point where even NOT-REFUTED means anything.
- Attribution: one opponent + one trick + one map set = a clean flip you can
  read. Five teams at once = a bundle you can't decompose (the exact problem the
  ship-gate amendment removed).
- The two-weapon finding says a single trick can't win all five anyway — so
  spreading tests a false premise.

## The plan in one line

**Ouroboros + Loki-2 alone, on {lighthouse, atoll, eider, drumlin, hive},
pre-registered to flip the 0%-map core losses; autopsy the result; if the
non-flips persist, add the spawn-ring and re-run; only then move to a sentinel
team as a separate experiment.**

## Provenance

Ouroboros autopsy: 85 attributed games (bb_rows core-HP for outcomes, rx_shooter
for gun/sen cause, ladder_games for maps + win-condition). Win-by-condition
verified: core_destroyed 9/86 (we kill them 9, they kill us 77), tiebreak 14/64
= 22%. CAD contrast from cad-core-kill-2026-08-09. Trick map from
offensive-catalog; loop from loss-autopsy-method; fixture IDs from
unrated-fixture-hard-teams. Firing unrated is builder-only (active submission +
slot); this lane owns the autopsy and the pre-registered flip list.
