# hive decode — the map halves our economy and leaves theirs intact

**Research arm, session 20, 2026-08-08 23:1x CEST.**
**Version tag:** live version is **v86 "Z2 fastfacing"** (x3r0, activated 22:15
CEST; a 128-line diff from `bots/opp_v76`, so v77–v84 are reverted). Replays
decoded span **our v72–v84**. The hive defect is measured on both sides of that
fork and is flat across it, so it applies to v86.
**Sources:** 34 hive replays + 60 non-hive core-kill-loss replays + a 305-replay
per-map sample, all from `replay_archive/`, parsed with `tools/replay_census.py`.
**DOWNLOAD BUDGET: 25 granted, 0 SPENT.** All 34 hive games were already
archived; the entire decode was free.
**Commissioned by:** builder, with pre-registration required. Hypotheses H1–H4
and their refuters were written into the coordination channel *before* any
replay was opened.

---

## Verdicts on the pre-registered hypotheses

| | hypothesis | verdict |
|---|---|---|
| **H1** | terrain/opening — hive breaks our opening build | **real, but NOT the cause** |
| **H2** | ore topology — hive starves our economy | **CONFIRMED — this is the mechanism** |
| **H3** | chokepoint siege — their turrets set up outside our rays | **NOT TESTED** (declared, not refuted) |
| **H4** | not hive-specific — generic pattern showing up on our most-drawn map | **REFUTED** |

H4 is the one I said I most expected to survive. It did not, and the test that
killed it is the one worth trusting most (below).

---

## 1. H2 — the mechanism

**hive is the worst economy map we have, by a clear margin.** Our titanium
collected per round, median, across all 15 maps:

```
hive          3.02   <<< LOWEST OF 15
heart         4.48
nordkap       4.53
saga          4.77
jackpot       4.92
...
drumlin      10.47
archipelago  11.85
snowflake    14.24
```

### The test that controls the obvious confound

"Losing depresses economy" would produce exactly this if hive games were simply
games we lose. So compare **losses to losses** — hive core-kill losses against
core-kill losses on every other map:

```
hive core-kill LOSSES        n=23   our ti/round median 2.72
other-map core-kill LOSSES   n=57   our ti/round median 5.32
Mann-Whitney z=-3.52  p=0.00043
```

Both cohorts are games we lost by core destruction. **Hive still halves our
economy.** That is H4 refuted: the pattern is not the generic shape of a loss.

Within hive, economy tracks the outcome:

```
hive WINS    n=5    our ti/round median 5.76
hive LOSSES  n=27   our ti/round median 2.64
Mann-Whitney z=+2.36  p=0.018
```

n=5 on wins — suggestive, not settled, and flagged as such.

### It is asymmetric — the map does not do this to them

```
                    OUR ti/round    THEIR ti/round    ratio
hive                    2.76             7.22          0.42
other-map kill loss     5.10            10.19          0.59
```

They lose ~29% of their economy on hive; we lose ~46%. **The deficit is ours.**

## 2. What the starvation actually consists of

End-of-game counts, medians:

| cohort | our harvesters | our *connected* | our conveyors | their harv | their conn |
|---|---|---|---|---|---|
| hive (all 34) | 3 | 1 | 18 | 6 | 4 |
| hive core-kill losses | **2** | **1** | 18 | **6** | **4** |
| other-map kill losses | 4 | 2 | 28 | 7 | 5 |

On hive we finish with **two harvesters and one working road**, while the
opponent finishes with six and four — which is what they get on other maps too.
**hive halves our harvester economy and leaves theirs untouched.**

And it is not a slow start:

```
                  OURS: 1st harvester r6, 1st conveyor r8     } identical
other maps        OURS: 1st harvester r6, 1st conveyor r8     } on both
hive             THEIRS: 1st harvester r5, 1st conveyor r4
other maps       THEIRS: 1st harvester r6, 1st conveyor r6
```

We open on time. **We just never scale.** (Their conveyor is 4 rounds earlier on
hive than elsewhere — small, but it points the same way.)

**Limit, stated plainly:** these are end-of-game snapshots. They cannot
distinguish *"we built few harvesters"* from *"we built enough and lost them."*
That distinction decides whether the fix is a build-policy change or a defence
change, and resolving it needs per-round entity tracking, which
`replay_census.py` does not do. **This is the single most valuable next
measurement and it is still free — the replays are already local.**

## 3. H1 — real, and not the cause

Our first sentinel arrives **round 28 on hive against round 15 elsewhere**:

```
our 1st sentinel round   hive n=34  median 28  mean 33.3   built in 100% of games
                      control n=57  median 15  mean 19.5   built in  95%
Mann-Whitney z=+5.23  p<0.00001
```

And it is **ours specifically** — the map does not delay theirs:

```
their 1st sentinel round  hive median 41   control median 36
Mann-Whitney z=+1.24  p=0.216   (not significant)
```

So H1 is a real, large, asymmetric, our-side property, and its pre-registered
refuter ("our r0–r30 build sequence matches other maps") did not fire.

**But it does not explain the losses**, and I am not going to let it ride on
plausibility:

```
our 1st sentinel, hive WINS   n=5   median 29
our 1st sentinel, hive LOSSES n=29  median 28
Mann-Whitney z=+0.24  p=0.808     -> no separation at all
```

The delay is identical in the games we win. And the per-map table refutes the
general form of the claim outright: **saga has a later first sentinel than hive
(median 43 vs 28) and we win 52% there.** Late sentinels do not lose games.

**H1 is a true description of hive and a false explanation of the hive defect.**
Anything built to pull our sentinel forward on hive is optimising a variable
measured not to move the outcome.

## 4. H3 — not tested, and I am not letting it lose by default

H3 (their turrets set up outside our firing rays) required extracting turret
positions and facings and testing ray coverage. `replay_census.py` reports
first-build round and end-of-game counts, not geometry. **I did not test it and
I am not reporting it as refuted.** It remains the live alternative to H2, and
it is not exclusive with H2 — a siege that shuts down our harvester field would
produce exactly the economy signature in section 1.

## 5. What I would measure next, in order

1. **Per-round harvester count on hive, ours vs theirs** — separates "never
   built" from "built and killed". Decides the entire shape of the fix. Free:
   replays are local; needs a per-round pass over `Update.placeEntity` /
   `removeEntity` that the current census does not do.
2. **H3 ray coverage** — the untested hypothesis, same replays, same zero cost.
3. **Ore-tile geometry of hive itself** — how much ore, how far from each core,
   and is it contested ground. `tools/make_map.py` recovered the map schema, so
   the tile grid is readable directly out of any hive replay without a game at
   all. This is the cheapest test in the list and I did not get to it.

## 6. Standing caveats

- **v72–v84 pooled.** The hive killed-rate is flat across the v86 fork (75%
  before, 75% after, strong opposition), which is why this transfers to the live
  bot — but the *mechanism* measurements here are not individually
  fork-controlled.
- **Opponent spread respected:** the 25-game hive loss pool is ≤5 per opponent
  (KCM 5, Memtrace 4, Lunds 3, CAD/Focalground/Powerpuff/Ouroboros 2 each), so
  this is not one opponent's habits.
- **`chain_dir` is an end-state snapshot** and says nothing about whether a road
  ever worked mid-game (noted in the census tool's own docstring).
- **Wins on hive are n=5.** Every within-hive win/loss contrast in this document
  rests on that and should be read as suggestive.

---

# ADDENDUM (23:2x) — two instruments agree on hive and disagree on why

The builder's 720-match local battery (both binaries vs `kladde_probe`, 15 maps
x 12 seeds x 2, uniform draw by construction) independently found hive to be the
worst core-kill cell on the board — bottom-ranked in **both** legs, the only map
that is. That is a second refutation of H4 from a direction I could not have
reached: game share cannot explain a collapse in an arena that draws every map
24 times.

**But the two instruments report opposite signatures, and the difference
matters.**

```
                     median turns    grind share    we are killed
PRODUCTION hive          284             12%            74%
PRODUCTION other maps    388             30%            37%

LOCAL leg hive        501-595          (n/a)          12-46% kill rate
LOCAL leg average     133-243
```

In production hive games are **shorter** than the field, grind **less**, and end
with our core destroyed three times as often. Locally they are 2–4x longer with
a low kill rate. Same map, inverted.

### The reconciliation is opponent strength, and it makes both true

A broken economy produces different failures depending on whether the opponent
can punish it:

- **`kladde_probe` cannot** — we beat it 87%. Starved economy against an
  opponent that will not kill you is a stalemate: we cannot build enough to
  close either. That is the 501–595 turns.
- **Ladder opponents can** — they convert the same starvation into a core kill
  by turn 284. That is the 74%.

One mechanism, two surface phenomena. **The practical consequence: a hive fix
validated on the local instrument would be scored on "did the grind shorten,"
which is not the failure mode production has.** Score hive work on **our
ti/round and harvester count** — the one variable both instruments agree on —
not on game length or kill conversion, where they disagree.

### And hive breaks the strength split

Every other map obeys the strong/weak split from the parent document. hive does
not:

```
                        n     win     killed    r1000
hive  vs STRONG >=1550  24     12%      75%      12%
hive  vs WEAK  <1550    10     20%      70%      10%
other vs STRONG        326     41%      44%      33%
other vs WEAK          140     75%      21%      24%
```

**On every other map a weak opponent is a 75% win. On hive they are a 20% win
and they kill us 70% of the time.** hive is the only cell that is absolutely
bad rather than conditionally bad — it is not explained by "we lose to strong
teams." The weak cell is n=10 and should be held loosely, but it points the same
way as every other measurement in this document.

---

# ADDENDUM 2 (23:4x) — #3 and #1, both run. It is BUILD POLICY, not defence.

Builder picked #3 first then #1, on the reasoning that ore geometry might
half-predict the harvester answer. It did exactly that. **Still zero downloads.**

## #3 — hive is the most ore-poor map on the board

Ore geometry read straight out of the `Map` message (no game required), all 15
maps:

```
map            dims     ore   density   d_median_own   contested
meander       25x15      24    0.064        6.0           42%
saga          24x24      36    0.062        8.1           39%
eider         28x20      32    0.057        4.5           12%
archipelago   26x26      38    0.056        6.0           16%
...
drumlin       25x25      30    0.048        8.6           40%
atoll         18x18       8    0.025        7.1           50%
hive          25x25      12    0.019        8.6           33%   <<< LOWEST
```

**hive has 12 ore tiles on a 25×25 board — a 0.019 density against a field of
0.042–0.064.** drumlin is the same dimensions with 30. And hive's ore is far:
median distance 8.6 from a core, tied-second-worst.

So hive imposes a hard cap of roughly six harvesters per side, and puts them at
arm's length. **That alone is not the defect** — the cap is symmetric, the map
is mirror-symmetric, and it applies to the opponent identically.

## #1 — we never build them. They do not die.

Per-round harvester tracking over `placeEntity` / `removeEntity`, medians:

```
cohort                    built  lost  peak   @r50  @r100  @r200   end
hive OURS   (kill-loss)     3.0   0.0   3.0    3.0    3.0    3.0   2.0
hive THEIRS (kill-loss)     6.0   0.0   6.0    3.0    4.0    5.0   6.0
other-map OURS   (loss)     6.0   1.0   6.0    3.0    4.0    5.0   4.5
other-map THEIRS (loss)     7.0   0.0   7.0    3.0    4.0    5.0   7.0
```

**The discriminator the builder asked for, answered:**

```
OF THE HARVESTERS WE BUILT, WHAT FRACTION DIED?
  hive, our kill-losses    OURS  0% died (n=25)
  other-map losses         OURS  9% died (n=59)
```

**Zero. Our hive harvesters do not die — we never build them.** This is a
build-policy defect, not a defence defect. H3 (siege) cannot be the mechanism
for the economy signature, because there is nothing being destroyed.

### The shape of the failure, in one line

Both sides sit at 3 harvesters at round 50. Then:

```
             r50    r100   r200   end
  OURS        3       3      3      2      <- flat forever
  THEIRS      3       4      5      6      <- keeps expanding
```

**We plateau at three by round 50 and never add another one for the rest of the
game. They keep expanding into the same scarce ore field and finish with
double.** On every other map our own policy reaches 6 — so this is not a
global build cap, it is something specific to hive that stops us at 3.

Peak saturation against the ~6/side cap:

```
hive, our kill-losses:   OUR peak 3.0/6 = 50%    THEIR peak 6.0/6 = 100%
```

And several opponents exceed six — Lunds 8, KCM 8, Powerpuff 9 — which means
**they are taking the contested ore (33% of hive's tiles are roughly
equidistant) and we are not contesting it.** hive is a race for twelve tiles
and we stop running at three.

## What this changes

- **The fix is build-policy, not defence.** Whatever gate stops our harvester
  expansion at 3 on hive is the target. Candidates worth a code-read: a
  distance/reachability cutoff (hive's ore is at median 8.6, the joint-worst),
  an ore-tiles-in-vision predicate, or a builder-count/economy gate that never
  fires because our economy is already starved — which would be a self-
  reinforcing loop and would explain the flat line from r50.
- **H3 is now refuted as the mechanism for the economy signature**, not merely
  untested — 0% harvester mortality leaves nothing for a siege to explain. It
  could still be a *separate* contributor to the core kills themselves.
- **H1's sentinel delay gets a plausible common cause.** A starved economy that
  plateaus at r50 would also delay a 30-Ti sentinel. That would make H1 a
  *symptom* of H2 rather than an independent property — consistent with H1
  showing no win/loss separation. Not tested; offered as the reading that fits.

**Caveat carried:** "built" counts first-placement per entity id (rotation
re-emit guarded). Medians over n=25 hive kill-losses. The per-game table shows
real spread — Ouroboros 7 built / 2 lost, one Powerpuff game 8 built / 7 lost —
so the flat-at-3 median is the central tendency of a distribution with tails,
not a law.
