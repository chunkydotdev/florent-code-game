# Are our titanium lines stalling? — the stalled-stack cut

**Research arm, session 27. Decoded 2026-08-10 (brief written 2026-08-09; filename keeps the brief's date).**
**Population: 8,399 archived replays → 16,798 team-sides. No downloads. No bot, arena or prereg touched.**

---

## 1. The discriminator's answer, stated first

The brief pre-registered:

> If OUR stall rate is materially above the third-party rate → live bug, mechanical cause.
> If our stall rate matches the field's → the shortfall is genuinely economic.

**Our stall rate matches the field's. By the pre-registered rule the shortfall is economic, not a
line-alignment bug.**

| measure, round-1000 games | US (n=576 team-sides) | third-party field (n=2,905) | ratio |
| --- | --- | --- | --- |
| carrier-residency episodes with dwell ≥33 rounds | 0.541% | 0.409% | 1.32 |
| carrier-residency episodes with dwell ≥129 rounds | 0.313% | 0.226% | 1.39 |
| carriers whose max dwell ever reached 32 rounds | 20.71% of built | 17.66% | 1.17 |
| stacks still sitting on a carrier at round 1000 | 2.51% of emitted | 2.50% | 1.00 |
| **titanium stranded on carriers at round 1000** | **279 Ti/game** | 154 Ti/game | 1.81 |

We are 1.2–1.4× the field on the *rate*, and the *ratio* is the wrong number to look at, because the
quantity it multiplies is tiny. **Median titanium stranded on a carrier at round 1000, in the 273
round-1000 games we lost on `titanium_collected`: 150 Ti. Median losing margin in those same games:
5,780 Ti.** The stranded-stack mechanism accounts for **2.6%** of the gap it was proposed to explain.

Counterfactuals on those 273 losses, computed per game rather than on medians:

| give us, for free… | losses that flip |
| --- | --- |
| zero stranded stacks — every line terminates correctly | **8 / 273 (2.9%)** |
| zero in-transit loss of any kind (stranded + destroyed + fed to the enemy core) | **19 / 273 (7.0%)** |
| harvesters that never back up (100% of theoretical emission delivered) | **163 / 273 (59.7%)** |

**The diagonal-terminus bug is real, is present, and is not where the 5,000 Ti went.**

---

## 2. But the shortfall DOES have a mechanical cause — one pipe segment upstream

The brief looked for stalls in the conveyor line. The stall is in the **harvester**, and it is nine
times larger.

Per round-1000 game, US:

```
  theoretical emission (harvester-rounds ÷ 4, +1 on build)   18,918 Ti
  actually left a harvester                                  11,118 Ti   <- 7,800 Ti (41%) never emitted
  delivered to our core                                      10,236 Ti   <-   882 Ti lost in transit
     of which fed into the ENEMY core                           509 Ti
     of which destroyed in transit                                93 Ti
     of which stranded on a carrier at r1000                     279 Ti
```

In the 273 round-1000 titanium losses, medians, us against the winner of the same game:

| | US | THEM (winner) |
| --- | --- | --- |
| harvesters built | 10 | 10 |
| core-entry tiles used | 3 | 3 |
| harvester-rounds alive | 5,444 | 6,322 |
| theoretical emission | 13,730 Ti | 15,870 Ti |
| **actually emitted** | **6,830 Ti** | **12,120 Ti** |
| delivered | 5,660 Ti | 11,720 Ti |
| **harvester-stall share** | **48.8%** | **24.6%** |
| in-transit loss share | 5.81% | 2.70% |
| stranded at r1000 | 150 Ti | 260 Ti |
| steady-state delivery, r500-999 | 0.500 stacks/round | 1.250 stacks/round |

We build the same number of harvesters, onto the same number of core entry tiles, and get **43% of
the throughput.** Our median in-harvester loss in those games is **6,210 Ti — larger than the entire
5,780 Ti median losing margin.**

### The mechanism, with its control

For every long-lived harvester (life ≥ 200 rounds) I reconstructed its 4-round emission schedule and
asked, at each *missed* slot, whether the tile it normally emits into was already holding a stack the
round before.

```
  US, 150 round-1000 losses, 2,323 harvesters, 731,023 missed emission slots
    missed slots with the output tile occupied at r-1 : 94.1%
    HIT   slots with the output tile occupied at r-1 : 24.7%   <- the control
    separation                                       : +69.4 pp   DISCRIMINATING
```

The complement was computed before the number was believed (method rule 3 — this is the exact shape
that made TRAP 8's `deliveries` column "prove" a hypothesis). The field shows the same mechanism:
98.2% vs 24.5%, +73.8 pp, on 1,299 harvesters in 150 third-party round-1000 games.

**Harvesters are not idle. They are blocked by their own output conveyor still holding the previous
stack.** This is back-pressure from the delivery network, and it is universal — which is precisely
why our rate matching the field's does not make it a doctrine question.

---

## 3. Calibrating "normal" — the dwell distribution the brief asked for

Per file × team, over every contiguous residency of one stack id on one conveyor / splitter /
harvester tile. Dwell = departure round − arrival round.

**US (n=576 team-sides, 4,136,624 episodes) / FIELD (n=2,905, 12,231,712 episodes)**

| dwell (rounds) | US share | US cumulative | FIELD share | FIELD cumulative |
| --- | --- | --- | --- | --- |
| 1 | 87.173% | 87.173% | 83.135% | 83.135% |
| 2 | 7.173% | 94.346% | 8.442% | 91.577% |
| 3 | 1.185% | 95.532% | 2.174% | 93.751% |
| 4 | 1.567% | 97.098% | 2.497% | 96.248% |
| 5–6 | 0.771% | 97.869% | 1.231% | 97.479% |
| 7–8 | 0.744% | 98.613% | 1.100% | 98.579% |
| 9–12 | 0.314% | 98.927% | 0.425% | 99.004% |
| 13–16 | 0.266% | 99.193% | 0.335% | 99.339% |
| 17–24 | 0.155% | 99.349% | 0.138% | 99.477% |
| 25–32 | 0.110% | 99.459% | 0.114% | 99.591% |
| 33–48 | 0.087% | 99.546% | 0.081% | 99.672% |
| 49–64 | 0.053% | 99.598% | 0.039% | 99.712% |
| 65–96 | 0.056% | 99.655% | 0.040% | 99.752% |
| 97–128 | 0.033% | 99.687% | 0.023% | 99.774% |
| 129–192 | 0.039% | 99.726% | 0.022% | 99.796% |
| 193–256 | 0.027% | 99.753% | 0.015% | 99.811% |
| 257–384 | 0.043% | 99.796% | 0.021% | 99.832% |
| 385–512 | 0.035% | 99.831% | 0.017% | 99.849% |
| 513–1000 | **0.169%** | 100% | **0.151%** | 100% |

The brief's calibration is confirmed at the head: **87% of residencies last exactly one round.** The
shape is not two clean modes but three:

1. a dominant spike at 1–2 rounds (94.3% of US episodes) — a healthy line;
2. a shoulder at 3–8 rounds (4.1%) — a line that hitches but recovers;
3. a **terminal mode at 513–1000 rounds** which is *larger* than either of the two buckets below it
   (0.169% vs 0.035% and 0.043%). That is the true pathology: a stack that arrives and never leaves.

### Choosing N from this distribution, not from the brief

- **N = 17** is the 99.35th percentile of US dwell and is 4× the harvester emission period, so it
  cannot be produced by ordinary emission cadence.
- **N = 33** is the 99.46th percentile and the point where the US and field curves cross in the same
  direction they stay in (ratio 1.32 and rising).
- **N = 513** isolates the terminal mode — a stack resident for more than half the match.

Share of a team's **built** carriers whose max dwell ever reached N (denominator = every conveyor,
splitter and harvester the team ever built, so a carrier that never receives anything counts against
the team rather than vanishing from the denominator):

| N | US | FIELD |
| --- | --- | --- |
| 2 | 41.30% | 37.21% |
| 4 | 28.59% | 26.91% |
| 8 | 24.87% | 22.77% |
| 16 | 22.61% | 19.65% |
| 32 | 20.71% | 17.66% |
| 64 | 18.58% | 15.78% |
| 128 | 16.40% | 14.03% |
| 256 | 13.81% | 12.35% |

**One in six of our conveyors holds a single stack for more than 128 consecutive rounds at some point
in the game.** That is a real, elevated defect rate. It is also worth ~279 Ti/game. Both statements
are true and the second one is the one that decides.

A separate, cheaper indictment of the same network: **only 50.2% of the carriers we build ever hold a
stack at all** (field: 51.4%). We build a median of 116 carriers per round-1000 game; roughly 58 of
them never carry anything.

---

## 4. Per-team spread — the field figure is a mixture, and quoting its mean would be wrong

63 third-party teams have ≥8 round-1000 team-sides. Their per-team median harvester-stall shares:

```
  min 0.0   q1 23.3   median 39.5   q3 49.6   max 100.0
```

Extremes: `Cookie` 100.0% (n=86) and `TKB` 99.6% (n=138) build harvesters that emit essentially
nothing; `Kleos` 0.0% (n=81) and `Powered by SmartFridge` 0.0% (n=69) are at the floor. **The band
mean averages incompatible doctrines** — method rule 6, and it bites here.

**Our 39.8% median sits at the 52nd percentile of the 63 field teams.** That is the discriminator's
answer in one number.

But the 0% teams are not the frontier — they are small economies whose few harvesters are perfectly
fed. The frontier is the teams that run a large economy *and* convert it:

| team | n | harv-rounds | theoretical | emitted | **collected** | carriers built |
| --- | --- | --- | --- | --- | --- | --- |
| **US OpenSverige** | 576 | 6,420 | 16,105 | 9,925 | **9,465** | **116** |
| Jacobs Code | 19 | 7,728 | 19,400 | 14,450 | **13,740** | 77 |
| PromptNPray | 98 | 8,846 | 22,205 | 12,790 | **11,625** | 82 |
| Bean counters | 122 | 8,495 | 21,290 | 12,450 | **11,275** | 97 |
| Git Glam | 94 | 6,420 | 16,285 | 11,125 | **10,385** | 72 |
| Viktor5776 | 83 | 4,917 | 12,320 | 9,940 | **9,800** | **34** |
| Kleos | 81 | 3,193 | 8,000 | 7,340 | 7,290 | 25 |
| Powered by SmartFridge | 69 | 1,955 | 4,900 | 3,540 | 3,540 | 24 |

(medians per round-1000 team-side; `theoretical`/`emitted`/`collected` in Ti)

**Viktor5776 collects more titanium than we do from 23% fewer harvester-rounds using 34 conveyors
against our 116.** Git Glam has *identical* harvester-rounds to ours (6,420) and delivers 10% more
from 62% of the carriers. Our network is the largest in the top of the field and the least
productive per tile. That is the shape of the problem: not misalignment, not stalling — **conveyor
mass that does not convert into throughput.**

---

## 5. A hard engine ceiling that nobody had measured

Deliveries into a core arrive from tiles orthogonally adjacent to its 2×2 footprint. Counting
distinct such tiles per team-side and comparing to steady-state delivery in rounds 500–999:

```
  team-sides exceeding entry_tiles x 1 stack/round : 0 / 3,582
  deliveries per entry tile per round: median 0.250   p99 1.000   max 1.000
```

**One stack per core-entry tile per round is a hard cap, hit exactly and never exceeded in 3,582
team-sides.** And the median team — ours and the field alike — runs those tiles at **25.0–25.1% of
capacity**, i.e. exactly one harvester's 4-round cadence per entry tile.

Median steady-state delivery by entry-tile count is almost perfectly linear at 0.25/tile:

| entry tiles | US median stacks/round (n) | FIELD median (n) |
| --- | --- | --- |
| 1 | 0.250 (35) | 0.250 (670) |
| 2 | 0.500 (106) | 0.500 (822) |
| 3 | 0.748 (121) | 0.750 (562) |
| 4 | 1.227 (146) | 1.000 (262) |
| 5+ | 1.690 (163) | 1.725 (134) |

Harvester stall rises monotonically with demand-over-capacity, and **our curve and the field's are the
same curve** — further evidence for "shared structural constraint", not "our bug":

| harvester demand ÷ core entry capacity | US harv-stall | FIELD harv-stall |
| --- | --- | --- |
| 0.00–0.25 | 16.4% | 11.7% |
| 0.25–0.50 | 26.2% | 29.2% |
| 0.50–0.75 | 39.9% | 42.3% |
| 0.75–1.00 | 48.1% | 50.2% |
| ≥1.00 | 54.5% | 58.9% |

The headroom implied by 25% utilisation is 4×. Whether it is reachable depends on the network's
internal merge structure, which I did not measure (§8).

---

## 6. Brief question 4 — does stalled-conveyor count predict the emitted-vs-collected gap?

The emitted side **is** exactly reconstructible, and better than the brief's formula. Every stack has
a unique id and its first appearance in `distributeResources` is its emission, with the `from` tile
identifying the emitting harvester: **births_from_harvester = births in 16,798/16,798 team-sides —
100.0%, zero births from any other tile kind.** So `emitted Ti = births × 10` is measured, not
estimated.

| | US (n=576) | FIELD (n=2,864) |
| --- | --- | --- |
| Spearman(stalled carriers ≥32, **in-transit** gap Ti) | +0.662 | +0.614 |
| Spearman(stalled carriers ≥32, **in-harvester** gap Ti) | +0.666 | +0.583 |
| median in-transit gap | 380 Ti | 100 Ti |
| median in-harvester gap | **5,950 Ti** | 2,745 Ti |

**Yes, stalled conveyors predict the gap — ρ ≈ +0.66 — and the gap they predict is 380 Ti.** They
predict the in-harvester gap equally well, which tells you the two are downstream of one common
cause (a congested network) rather than one causing the other. Correlation strength was never the
question; the magnitude of the quantity was.

---

## 7. Instrument validation — teeth, per guard, per branch

**Two guards run on every team-side and both can fail.**

| guard | clean archive | under injected corruption |
| --- | --- | --- |
| `ti_ok`: core deliveries × 10 == `Player.titaniumCollected` | **16,798 / 16,798 pass** | 21/60 FAIL when the resource stream is silenced after r200; 6/60 FAIL when two carrier tiles are frozen |
| `cons_ok`: births == delivered + destroyed + stranded | **16,798 / 16,798 pass** | (holds by construction; verified non-trivially — it caught a cross-team attribution bug during development, `lost = ±3`) |

**Injected-stall test (the alarm must fire).** Freezing the two busiest carrier tiles of each team
from round 100 in 30 replays — the exact signature of a chain that terminates where it cannot
deliver:

```
  stacks alive at end   562 -> 1,803   (3.2x)  PASS
  episodes dwell>=128   282 -> 1,103   (3.9x)  PASS
  deliveries         10,761 -> 9,660           PASS (delivery collapses)
  ti_ok               60/60 -> 54/60           PASS (the guard detects the lie)
```

**Destroyed-with-carrier guard is load-bearing, not decorative.** Disabling it moves 156 stacks from
`destroyed` into `alive_end` and inflates the ≥128-round tail by 35% (282 → 382). Without it, every
conveyor blown up while holding a stack would have been reported as an 800-round stall.

**Both branches of the ours/field partition were tested (method rule 2).** Swapping the seat
assignment changes the answer materially — median harvesters built in "our" losses goes 10 → 4 and
entry tiles 3 → 2 — so the seat variable carries real signal and is not near-constant. The seat comes
from `meta_join.us_side`, which `meta_attrib.py` derives from `meta.json`'s `teamAId == <our GUID>`,
**not** from `winnerSide` — so TRAP 7's circularity does not apply here. `related != 'none'`
(opensverige – plan B) is excluded from both arms.

**Emission-clock model validated before it was used.** The theoretical-emission denominator assumes
one stack per harvester per 4 rounds, +1 on build. Measured across 120 replays:

```
  inter-emission gaps: 94.53% are exactly 4 rounds   (median 4, mean 4.65)
  first emission after build: mode 0 and 2 rounds
  life ÷ emissions, long-lived harvesters (n=514): min 3.93, p05 3.98, median 4.03
```

The 4-round ceiling is not theoretical — 5% of long-lived harvesters achieve it to within 0.5%.

---

## 8. What I could not measure

1. **Why the output conveyor is still full.** I proved the harvester is blocked by its own output
   tile (94.1% vs 24.7% control) but not *which* downstream tile is the binding constraint — merge
   point, trunk head, or core entry. Core entry runs at 25% utilisation, so the constraint is
   *inside* the network. **This is the single biggest unmeasured thing and it is the one that turns
   this document into a build change.** It needs a per-round flow-graph decode: for each blocked
   conveyor, walk its output chain to the first tile that did not move, and histogram what that tile
   is. Feasible from the same stream; roughly one more decoder.
2. **A harvester that never emits at all is invisible to the move stream.** A stack that never moves
   generates no `ResourceMove`, so a fully blocked harvester is unobservable directly. I bounded it
   from the entity side: we build 12.18 harvesters/game and 1.21 of them never emit once,
   contributing 210 harvester-rounds/game of pure zero. Small, but it is a floor, not a measurement.
3. **`deliv_entry_tiles` counts distinct tiles used over the whole game, not concurrent capacity.**
   A line rebuilt into a different core face inflates it. `max_deliv_1round` (US median 3.0) is the
   conservative concurrent bound. Every entry-tile claim in §5 should be read as an upper bound on
   capacity and therefore a *lower* bound on the utilisation shortfall.
4. **Round-1000 games only.** 576 US team-sides of 2,243 attributed. Games ending in a core kill are
   excluded entirely — nothing here says anything about economies in short games.
5. **Archive composition.** The third-party arm is 2,905 round-1000 team-sides across 63 teams with
   ≥8 games, but the archive is still dominated by our own matches; per-team field coverage runs
   8–149. Small-n teams in the §4 table are indicative only.

---

## 9. Two things this settles that were open elsewhere

**TRAP 8's unresolved question is now answered.** `corpus-howto.md` records as STILL UNRESOLVED
whether `titanium_collected` includes passive income (~2,500/game) or only delivered titanium.
**It counts only core deliveries.** Core-footprint deliveries × 10 equals `Player.titaniumCollected`
exactly in **16,798 of 16,798 team-sides**, over full and partial games, winners and losers. Passive
income is not in the tiebreak key. (The schema doc had this at 56 team-sides; it now holds at 300×
that scale, and the guard demonstrably fails under corruption, so it is a test rather than a claim.)

**A number in the brief does not reproduce.** The brief cites *212 round-1000 losses on
`titanium_collected`, median losing margin 5,035 Ti*. On `meta_join` + in-replay `winCondition` I get
**273 losses, median margin 5,780 Ti** (mean 6,517), from 577 such games (273 L / 304 W). Neither
figure changes any conclusion here — the margin is ~5–6k either way and the stranded-stack
contribution is 150 Ti — but the populations differ by 29% and one of them is wrong.

---

## Appendix — reproducing this

Decoder and analysis scripts are session-scratch and will die with the session; they are ~250 lines
against `tools/replay_census.fields`. The load-bearing design decisions, so the next analyst does not
re-derive them:

- **Stack ids are resource ids from the same global counter as entity ids** (TRAP 1). Only *identity*
  and *ordering* are used here; no magnitude comparison anywhere.
- **`ResourceMove.resourceId` is present in 100% of moves** (22,114/22,114 in the first probe). The
  whole analysis rests on this; it is not optional in practice despite being `optional` in the schema.
- **`Conveyor.stored` is never populated on `placeEntity`**, and conveyors are placed exactly once
  (only gunners re-emit — TRAP 3, confirmed: 6 gunners placed >1 time, 0 of every other kind). So
  occupancy is only recoverable by integrating the move stream. There is no snapshot.
- **A stack's first appearance is its emission**, and its `from` tile is the emitting harvester —
  true in 100% of births archive-wide.
- **A carrier destroyed while holding a stack must terminate that stack's episode**, or it reads as a
  multi-hundred-round stall. This guard alone accounts for 35% of the long tail.
