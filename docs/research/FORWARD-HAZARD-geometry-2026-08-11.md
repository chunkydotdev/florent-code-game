# THE FORWARD HAZARD IS PER-ROUND, NOT PER-TILE — AND THAT BOUNDS THE ROUTING PLANK

**Research arm, s30, 2026-08-11, answering the builder's post-LOKI-25 design brief
(*"the version worth building REPLACES the station rather than taxing it"*).
Instrument: `scratchpad/ring_cover.py` + inline decodes over `replay_archive/`,
our games, v104-era. Gunner ray model: facing ray, r² ≤ 13, **stopping at the
first occupied tile**, which is itself covered.**

## 1. THE ENEMY CORE RING IS NOT DEFENDED BY GUNNERS

Sampled every 10th round, 205 of our games that had a forward presence:

| zone | tiles | **covered by an enemy gunner ray** |
|---|---:|---:|
| enemy core RING (d² ≤ 8) | 31.3 | **2.57%** |
| approach ANNULUS (d² 9–32) | 59.6 | **2.95%** |

**Ratio 1.1×. There is no lethal ring and no lethal annulus.** Share of sampled
rounds with **zero** free ring tile: **0.0%**.

## 2. THE DEATHS ARE THERE REGARDLESS

Our 9,227 forward builder deaths, by distance from the **enemy** core:

| d² from enemy core | deaths | share |
|---|---:|---:|
| **≤ 8 (on the ring)** | 2,678 | **29.0%** |
| **9–32 (the approach)** | 4,653 | **50.4%** |
| 33–100 | 1,665 | 18.0% |
| 101–400 | 231 | 2.5% |
| > 400 | 0 | 0.0% |

**79.4% inside d² ≤ 32.**

## 3. OUR TILE SELECTION IS ONLY MILDLY BAD — AND THAT IS THE CEILING

Over **22,676 forward builder-rounds**, our builders stand on a gunner-covered
tile **2.04%** of the time against a whole-map baseline of **1.34%** — **1.53×
chance.**

**⇒ A PERFECT ROUTING PLANK CAN CUT EXPOSURE BY AT MOST 34% (2.04 → 1.34), and
only with flawless tile choice.** That is the entire size of the prize, measured
before a build.

## 4. ⭐ WHY LOKI-25 DIED, WITHOUT BLAMING ITS IMPLEMENTATION

The hazard is **~2% per forward round and it accumulates** — a raider standing
forward 50 rounds is odds-on to enter a firing line at some point. **If death risk
is proportional to forward rounds, cutting forward rounds cuts deaths
proportionally and buys nothing per unit of work.**

LOKI-25 measured exactly that identity: **deaths −24%, forward presence −23%,
deaths per forward build −2.3%.**

**LOKI-25 did not fail for penalising instead of proposing. It failed because the
quantity it moved was rounds-exposed, and the hazard is per-round.**

⇒ **The lever is not WHERE a raider stands but HOW MANY ROUNDS IT STANDS THERE PER
UNIT OF WORK.** A plank that gets the same forward builds from fewer forward
builder-rounds beats both arms. A plank that only re-picks tiles is capped at 34%
of a hazard already only 1.53× chance.

## 5. ⛔ ONE CONTROL IN THIS CUT IS INVALID AND IS NOT USED

I also measured **their** forward builders standing in **our** gunner lines:
**1.01%**. **That is not evidence they route better.** We build **1.29
gunners/game against the field's 6.1** — they are exposed to fewer guns, not
better at dodging. **Same population error as this morning's `FIELD_vsUS`
pooling, caught before publication this time.** The valid contrast is our 2.04%
against the 1.34% map baseline, internal to the same games.

## 6. WHAT IS NOT MEASURED

**Dwell time per forward build** — the quantity all three results converge on.
Not measured here and not guessed. Also: the ray model assumes facing is current
at the sampled round and ignores rotation between samples; sampling every 5th or
10th round can miss a transient line-of-fire, so **2.04% is a lower bound on
exposure** — which makes the 1.53× a lower bound and the 34% ceiling an upper one.
