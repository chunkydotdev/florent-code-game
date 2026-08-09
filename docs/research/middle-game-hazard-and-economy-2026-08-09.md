# We win the opening and we win the clock. We lose the middle, and we lose it by dying.

**Research arm, session 23, 2026-08-09.** Wheel topic 8 (economy) plus a
survivor-controlled census that reframes it.
**Version tag:** live **v90 "Heimdall 1 (launcher relight)"**, 1586-1589 @ 502,
rank #28-29/113. Corpus at `04952c8`: 4,071 replays, 4,031 decoded, join **1,230
rows, 100.0000% reconciled**. Free metadata + already-archived replays only.
**Zero downloads, zero arena, zero bot edits.**

---

## 0. TL;DR

1. **The hazard curve is monotone and it is about us.** Conditional on a game
   ending in a core kill, the probability that **our** core is the one that died
   rises **29% → 55% → 72% → 76%** across r0-150 / r151-300 / r301-600 / r601-999.
2. **But if we survive to the clock we win.** 353 games reached round 1000 and we
   took **57.2%** of them, with delivery margin predicting the result in
   **353/353**.
3. **So the economy is not the problem and never was.** The problem is the
   survival window between roughly r150 and r1000.
4. **Cost scaling never binds on harvesters** — under both readings of "+5% each",
   break-even is far beyond any map's ore supply. It binds hard on the **+20%
   categories** (builder bots, gunners, sentinels).
5. **Our early build is a near-constant.** Its medians are *identical* in wins and
   losses. What varies is the opponent. **Most "paired differential predicts
   winning" patterns in this corpus are opponent-strength measurement, not a lever
   we control.**
6. **We are already the out-economy, under-defend team** — and it is not winning.
   That **refutes the "disengage and out-economy" hook** I filed this morning, as a
   *change*: it is our status quo.
7. **Verified from data: `delivered` and `stored` are different counters.**
   Spending cannot cost us tiebreak key #1.

---

## 1. The curve

`join.tsv`, n=1,230 ladder games, every game we have archived and attributed.

| game length | win condition | n | our win% |
|---|---|---|---|
| r0-150 | core destroyed | 293 | **71.0%** |
| r151-300 | core destroyed | 259 | 44.8% |
| r301-600 | core destroyed | 221 | **27.6%** |
| r601-999 | core destroyed | 104 | **24.0%** |
| r1000 | titanium collected | 353 | **57.2%** |

Read as hazard — *given that a core died, whose was it?*

| kill round | n | **our core died** |
|---|---|---|
| r0-150 | 293 | 29.0% |
| r151-300 | 259 | 55.2% |
| r301-600 | 221 | **72.4%** |
| r601-999 | 104 | **76.0%** |

**Monotone across four buckets.** This is not tautological — a symmetric matchup
would sit at 50% in every row. We start well above parity and end well below it.

Recent lineage only (`ourver ≥ 85`, n=120) reproduces the shape at low n:
**89.7% → 42.9% → 22.2% → 42.9% → 51.6%.**

**This is the same r150 boundary five earlier instruments found** (conversion
ratio, raider survival 43→6, turret production, forward placement, ammo
conversion) — arriving here from win/loss and win-condition metadata alone, which
is an independent path.

## 2. What it means, and what it does not

**It means the intervention is survival, not economy.** We are not losing because
we out-produce or under-produce titanium. We are losing because between r150 and
r1000 our core dies more often than theirs, and if it does not, we win the
tiebreak comfortably.

**It does not mean "play for the clock".** The builder's REFUTED-AT-PRECISION call
stands and this does not rescue it: on the recent lineage the grind/kill split is
51.6% vs 53.9% at n=31/89, indistinguishable. **The 57.2% is a pooled-lineage
number and must not be quoted as a property of v90.** What survives the version cut
is the *shape* — early good, middle bad — not the level.

**Honest confound:** game length is an outcome, not a treatment. A game "ending at
r400 by core kill" is partly defined by the thing being measured. The hazard
framing (§1, second table) is the confound-resistant form, because it conditions
*on* a kill having happened and asks only whose — a question the outcome cannot
answer by construction.

## 3. Our opening is a constant, and that invalidates the obvious analysis

Measuring builds in a **fixed early window** (r0-150) restricted to games that ran
past it (turns ≥ 300, n=678), so both teams were alive throughout the window:

| r0-150 build | WON: us | WON: them | LOST: us | LOST: them |
|---|---|---|---|---|
| harvesters | 5 | 3 | **5** | 5 |
| turrets | 3 | 4 | **3** | 5 |
| conveyors | 36 | 12 | **36** | 23 |
| builder bots | 6 | 6 | 7 | 6 |

**Our own numbers are identical in wins and losses** (means confirm it: harvesters
5.5 vs 5.8, conveyors 35.7 vs 35.9, sentinels 1.7 vs 1.6). **Everything that
differs is theirs.**

So the tempting table — *"paired harvester diff ≤ −3 → 19.4% win, ≥ +3 → 65.5%"*,
and the same monotone pattern for turrets and conveyors — **is not measuring a
lever we control.** It is measuring how much the opponent built, which is a proxy
for opponent strength. **A differential whose variance lives entirely on the other
side of the subtraction is an opponent thermometer, not a strategy dial.**

*This is the third instance today of the same error family — a statistic standing
in for a measurement of the thing you can actually change. I nearly relayed the
differential table as a finding.*

## 4. We are already the disengage-and-out-economy team

Recent lineage, r0-150, paired within game (n=63):

| r0-150 build | us | them | paired diff | we lead in |
|---|---|---|---|---|
| harvesters | 5 | 4 | **+1** | 61.9% |
| conveyors | 36 | 23 | **+16** | **81.0%** |
| builder bots | 7 | 6 | +2 | 68.3% |
| **turrets** | **3** | **5** | **−1** | **25.4%** |

And over all 1,230 paired games the same shape: conveyors +13 (we lead 71.7%),
turrets **−3 (we lead only 20.1%)**.

**We out-build the field on every economic category and under-build it on
turrets — and we are at 42.5% in the turns ≥ 300 stratum.**

> **AMENDMENT to my own tactics file, same day.** `2026-08-09-sweep-2.md` filed
> *"disengage and out-economy the static defence"* (Battlecode 2025 / The Kragle)
> as `transfers: yes` with a corpus query attached. **The query is now run and the
> hook is refuted as a change**: we already are that team, and it is our worst
> stratum. The tactic is not wrong about RTS generally; it is **already our status
> quo**, so it cannot be a lever. Amended in place.

## 5. The economy arithmetic — cost scaling never binds on harvesters

Harvester: 20 Ti base, 10 Ti per 4 rounds = **2.5 Ti/round → 8-round payback**.
"+5% each" is ambiguous between additive and multiplicative, so both are computed;
"destroying removes its contribution" means N is the count of **live** harvesters.

| N (simultaneous) | additive cost | payback | multiplicative cost | payback |
|---|---|---|---|---|
| 1 | 20 | 8 rounds | 20 | 8 rounds |
| 20 | 39 | 16 | 50 | 20 |
| 50 | 69 | 28 | 218 | 87 |
| 100 | 119 | 48 | 2504 | 1002 |

Break-even against the remaining clock: additive ~2,482 harvesters at r0;
**multiplicative — the harsh reading — ~100 at r0 and still ~68 with 200 rounds
left.** A 30×30 map is 900 tiles; you would need >11% of the map to be ore.

**Where inflation actually bites is the +20% categories**, which produce no revenue
at all. Under the multiplicative reading the **20th builder bot costs 958 Ti** and
the 20th gunner 638 — **so `MAX_TEAM_UNITS = 50` is not our real ceiling, the cost
curve is.** If "when to stop expanding" has an answer here, it is about builder
bots and turrets, not harvesters. *(Sweep 4's arithmetic; the additive/
multiplicative fork is bounded on both sides, so the conclusion holds either way.)*

## 6. Verified: spending cannot cost us the primary tiebreak

The sweep flagged this as its least confident claim and it is load-bearing, so I
measured it rather than reasoning about it. Across **6,454 team-games** in
`econ.tsv`:

- `ti_collected` is **non-decreasing across round bands in 6,453 / 6,454
  (99.9845%)**. The single exception is a *local battery* file
  (`eider_s1_a_hsd.replay26`), not a ladder replay.
- `ti_end` (stored) **decreases at some point in 56.9%** of team-games.

**They are different counters. Stored falls when we spend; delivered never does.**
So converting titanium to ammunition is **free with respect to tiebreak key #1**,
and our measured over-banking is not conservative play — it is dead weight that
pays off only at tiebreak **3**, reached only when delivered *and* live-harvester
counts are both exactly tied.

**Corollary worth its own line: tiebreak 2 is harvesters *alive* — a snapshot at
r1000, not a stream.** A harvester built at r990 delivers ~12 Ti and is worthless
on key 1, but counts fully on key 2, and **does not even need a conveyor
connection.** Late surplus titanium converted into harvesters on any reachable ore
is a direct, cheap purchase of the second tiebreak. Given 353 of our 1,230 games
reach r1000, this is the cheapest untested idea in this document.

## 7. What I would do with this

1. **Do not open an economy programme.** §1 and §3 both say the economy is not the
   binding constraint and our own economic inputs barely vary.
2. **The middle-game hazard is the target**, and it is the same band the builder's
   home-defence advantage lives in. **Everything in this document points back at
   the work already in flight**, which is the outcome I would least have predicted
   when I picked topic 8.
3. **Cheap and independent of all of the above**: a late-game harvester-spam branch
   for tiebreak 2, and an ammo-conversion floor sized to one volley
   (`10×sentinels + 4×gunners`) so the float becomes explicit. Both are conditionals,
   not subsystems.
4. **Retire paired-differential tables as evidence about us** unless our own side
   of the subtraction is shown to vary first (§3).

## 8. Limits

- `THEM` is our ladder opponents, mostly 1500-1700; the archive is dominated by our
  own games (corpus-howto trap #4).
- §1's length buckets are outcome-defined; the hazard table is the defensible form.
- §3-§4 are correlational. The fixed-window design closes the reverse-causal path
  (an outcome at r600 cannot change r0-150 builds) but does not randomise anything.
- The recent-lineage cuts are n=63-120. Shape only; do not quote levels.
- §5's multiplicative branch is the *harsh* reading and may not be the engine's; the
  conclusion is stated so that it holds under either.
