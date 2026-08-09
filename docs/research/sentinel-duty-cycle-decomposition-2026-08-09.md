# Why our sentinels are silent: NO TARGET / WRONG FACING / OTHER

**Research arm, 2026-08-09.** The brief: *our sentinels fire at 13.5% of their
reload ceiling — decompose that idle time.* A build decision is blocked on it.
**ZERO replay downloads** — every byte read was already on disk.

> ## THE THREE SHARES
>
> **Population: OpenSverige's own sentinels, 2,218 clean side-games,
> 5,456 sentinel emplacements, 1,188,099 idle sentinel-rounds.**
> Denominator: every round a living sentinel of ours did **not** fire.
>
> | | share of idle sentinel-rounds |
> | --- | ---: |
> | **(a) NO TARGET** — no enemy entity anywhere within r²=32 | **22.0%** |
> | **(b) WRONG FACING** — enemy in r²=32, none on the fixed facing line | **64.4%** |
> | **(c) OTHER** — enemy *was* on the line and it still did not fire | **13.6%** |
>
> **(c) decomposes completely and holds no mystery:** reload-blocked **6.5%**,
> team ammunition below 10 **6.4%**, TLE **0.00%**, `run()` never invoked
> **0.02%**, **unexplained 0.7%**.
>
> **`(b)`-DOMINANT.** By the coordinator's own pre-registration that means the
> plank is **redirected, not killed**: from *"put sentinels forward"* to
> *"choose the facing deliberately at build time."*
>
> **But the redirect has a sharper form than the pre-registration anticipated,
> and §4 is the load-bearing section:** siting and facing are **not two planks**.
> Forward siting works *because* it makes facing stop mattering. Our own forward
> sentinels already prove it, and there is a cheaper version of the same lever
> that moves nothing.

---

## 0. VERSION TAG AND FROZEN INPUTS

| | |
| --- | --- |
| repo git sha at run | `935a375` |
| `replay_archive/` at run | **9,705** `.replay26` |
| files decoded | **7,829** (`meta_join` ∩ on disk ∩ `related == none`) |
| our side-games in it | **2,218** (446 matches) · third-party side-games **5,611** (70 named teams) |
| scripts | session scratchpad `sdc/` — **not committed** (see §7) |

The keeper daemon appends to `corpus/` every ~10 min, so `meta_join.tsv` was
**frozen into the scratchpad before any use** and every number below is read
from the freeze.

| artifact | rows | md5 |
| --- | ---: | --- |
| `meta_join.frozen.tsv` | 7,954 | `4fc955a3` |
| `full4.tsv` (**new decoder** `sentinel_duty2.py`, one row per sentinel emplacement) | **25,210** | `317c8be5` |

**Decoder ran with 0 errors on all 7,829 files.**

### Which side is us — TRAP 7 does not apply here

`corpus-howto.md` TRAP 7 warns that `ladder_games.seat`, `meta_join.us_side`,
`join.our_team` and `ladder_games.won` all descend from `winnerSide`. **For
`us_side` that is not true and I checked at source.** `tools/corpus/meta_attrib.py:275`
derives it from the **team id**:

```python
if meta.get("teamAId") == OURS:  us = "a"
elif meta.get("teamBId") == OURS: us = "b"
else: us = "none"
```

Independently confirmed against the team **name** across the whole frozen table:
`us_side == ("a" if teamAName=="OpenSverige" else "b" if teamBName=="OpenSverige" else "none")`
on **7,874 / 7,874 rows, 0 mismatches**. No winner-derived field is on the path.

### Populations, and the label each one carries

- **`US (OpenSverige)`** — our side in our 2,218 clean games.
- **`TP <band>`** — clean third-party side-games, banded on **that side's own**
  at-match `ratingBefore`. The clean field.
- **`FIELD-IN-OUR-GAMES`** — the opponent's side in our own games. **Not a field
  figure**; confounded by our matchmaking band. Shown once, labelled.

---

## 1. THE RULESET CLAIM, VERIFIED AGAINST THE PRIMARY

The brief asked me to check its own discriminator rather than trust it. I did.
**The load-bearing half is sourced; a second half is not, and the brief inherited
that from an earlier document.**

> **`docs/reference/official-docs.md:257`** — *"Sentinels hit a single tile-wide
> line along their facing direction, just like a Gunner's shot — but the line
> reaches much further (vision/attack r²=32 vs. Gunner's 13) and, unlike a
> Gunner's, **is never blocked by walls or units in the way**. … **Facing is fixed
> at build time; Sentinels cannot rotate.**"*
>
> **`official-docs.md:282`** — *"Rotation costs exactly 10 Ti and triggers a
> 1-round action cooldown. **Sentinels and Launchers have no rotate()** — their
> orientation (or lack of one) is fixed for their lifetime."*
>
> **`official-docs.md:1392`** — `Sentinel | 40 | 30 | 32 | 32 | 18 | 10 | 2`

✅ single-tile-wide line · ✅ fixed facing direction · ✅ r²=32 · ✅ ignores
obstacles · ✅ cannot rotate, ever. **The premise that makes this question
decision-relevant is sound.**

**NOT sourced — flagged, not repeated.** The brief states the sentinel's shot
*"passes through friendly bots and barriers and does not harm them"*. `:257` says
only *"never blocked"*. **Blocking and damaging are different claims and the
primary is silent on the second.** `gunner-vs-sentinel-pricing-2026-08-09.md` §2.3
raised exactly this and §2.4 settled it *indirectly* (18 × shots reconstructs
observed damage to 0.02%). **My instrument does not depend on it either way** —
I never model damage — so nothing below rests on the unsourced half.

**Line geometry, derived and then measured.** Line = `pos + k·delta(dir)` for
`k = 1,2,…` while `|k·delta|² ≤ 32` → **5 tiles cardinal, 4 tiles diagonal**, no
occlusion. §2 shows that **all 452,496 sentinel `fireTurret` events in the archive
land on that computed line (rate = 1.000000)**, which confirms the line length,
the `Direction` enum → `(dx,dy)`
mapping, and the north-is-`(0,−1)` convention simultaneously.

---

## 2. TEETH — FOUR GUARDS, BOTH POPULATION BRANCHES, EVERY CLASSIFIER BRANCH

Method rule 1: *an instrument that has never been observed to fail is a claim.*
Method rule 2: *prove teeth per guard, per branch.* Every guard was run
separately on **400 clean ours** and **400 clean third-party** files, TRUE and
under each of four corruptions.

### 2.1 The statistic that carries the whole decomposition

**A fire is ground truth that a target was on the line.** So the direct test of
the (a) and (b) predicates is to run them on the **fired** branch and count how
often they would have said "no target" / "wrong facing" anyway. That
false-negative rate is the error rate of the buckets I am reporting.

### 2.2 Results

| branch | statistic | TRUE | CORRUPT `facing` | CORRUPT `team` | CORRUPT `live` | CORRUPT `offset` |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| **ours** | **T1** fire lands on computed line | **1.00000** | **0.00000** | 1.00000 | 1.00000 | 1.00000 |
| ours | **T2** fire target is an enemy tile | 0.90238 | 0.90238 | **0.03501** | 0.99350 | 0.90238 |
| ours | **T3** classifier FN on fired rounds | **0.01327** | **0.59626** | **0.65287** | 0.00011 | **0.05662** |
| ours | T3a — … falsely as **(a)** | 0.00071 | 0.00071 | **0.01988** | 0.00000 | 0.00331 |
| ours | T3b — … falsely as **(b)** | 0.01256 | **0.59555** | **0.63299** | 0.00011 | **0.05331** |
| ours | **T4** **(a)** share on the idle branch | 0.18016 | 0.18016 | **0.00859** | **0.03714** | 0.17962 |
| ours | **(b)** share on the idle branch | 0.56333 | 0.58667 | 0.29161 | **0.10700** | 0.55770 |
| ours | **(c)** share on the idle branch | 0.25651 | 0.23317 | **0.69980** | **0.85586** | 0.26268 |
| **third-party** | **T1** | **1.00000** | **0.00000** | 1.00000 | 1.00000 | 1.00000 |
| third-party | **T2** | 0.83835 | 0.83835 | **0.00605** | 0.97118 | 0.83835 |
| third-party | **T3** | **0.03993** | **0.67644** | **0.63432** | 0.02473 | **0.06760** |
| third-party | T3a — falsely **(a)** | 0.00054 | 0.00054 | **0.01062** | 0.00044 | 0.00149 |
| third-party | T3b — falsely **(b)** | 0.03939 | **0.67589** | **0.62370** | 0.02430 | **0.06611** |
| third-party | **T4** **(a)** share | 0.19837 | 0.19837 | **0.00703** | **0.07655** | 0.19796 |
| third-party | **(b)** share | 0.45537 | 0.58531 | 0.45291 | **0.17249** | 0.45160 |
| third-party | **(c)** share | 0.34626 | 0.21632 | **0.54006** | **0.75096** | 0.35044 |

*(Teeth sample = 400 + 400 files, so its TRUE shares differ from the full-archive
figures in §3. That is the sample, not a disagreement.)*

**Every branch is covered.**
- **(b)** — `facing` rotates every sentinel 90°: T1 **1.00000 → 0.00000**, T3b
  **0.013 → 0.596** (ours) and **0.040 → 0.676** (third-party).
- **(a)** — `live` stops honouring `removeEntity` so occupancy never shrinks:
  the (a) share collapses **0.180 → 0.037** (ours), **0.198 → 0.077** (tp).
- **(a) + (b)** — `team` classifies against the sentinel's own team: T2 collapses
  **0.902 → 0.035** / **0.838 → 0.006**, T3 blows up to 0.65 / 0.63.
- **(c)** — `offset` reads the fire ledger one round late: T3 **0.013 → 0.057** /
  **0.040 → 0.068**, and (c) shifts. The reload sub-bucket is anchored separately
  in §2.4.

### 2.3 G5 — census grain against an independently written, shipped decoder

Per-file × per-team **sentinel counts** from my decoder against
`tools/corpus/replay_builds.py`'s shipped `corpus/builds.tsv`, over the **6,123
files in common**, requiring **exact** agreement:

```
TRUE       12,246 / 12,246 = 100.000000%
TEAM-FLIP   1,212 / 12,246 =   9.897109%
```

### 2.4 Two model parameters anchored by measurement, not assumption

- **Reload = 2 is measured.** Minimum observed gap between consecutive fires by
  the same sentinel: **≥ 2 in 25,210 / 25,210 emplacements; 0 with a gap < 2.**
  The reload sub-bucket in (c) is therefore not a modelling choice.
- **`Direction` = CENTRE never occurs.** 0 of 25,210 sentinels. No sentinel has a
  degenerate empty line, so no bucket is inflated by one.

### 2.5 The residual error, named, bounded, and its mechanism identified

T2 is 0.90 and not 1.00; T3 is 0.013 and not 0.000. **Both come from the same
place and it is not a bug in the ledger.** Unit turn order is global entity-id
ascending, so a builder bot can step onto the line, be shot, and be removed —
all inside one round. It is then absent from **both** my start-of-round and
end-of-round snapshots.

**The `live` corruption proves the mechanism rather than merely bounding it:**
disabling `removeEntity` — i.e. letting killed entities persist — lifts T2 from
**0.902 → 0.9935** (ours) and **0.838 → 0.971** (third-party). The missing
targets are exactly the ones that died that round.

**Bound: (b) is over-counted by at most 1.3% of fired rounds (ours) / 3.9%
(third-party).** Against a (b) share of 64.4% this cannot change the ranking.
Both readings are printed side by side in §3 so the sensitivity is visible
rather than asserted.

---

## 3. THE DECOMPOSITION

**Headline rule = UNION**: an enemy occupied a tile at the **start or the end** of
the round. This is the *"could this sentinel have hit something this round"*
quantity method rule 5 asks for, and it is deliberately **generous to (c)** and
**conservative about (a) and (b)** — it can only shrink the buckets I am claiming
are large.

### 3.1 Per band, never pooled

| population | N sent | idle sent-rnds | % of reload ceiling | **(a) NO TARGET** | **(b) WRONG FACING** | **(c) OTHER** | — c reload | — c other | % fwd | med d²_own |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TP <1550 | 5,427 | 1,578,748 | 13.8% | 32.0% | 43.2% | 24.8% | 5.1% | 19.6% | 44.8% | 26 |
| TP 1550-1699 | 3,232 | 335,164 | 25.1% | 9.2% | 52.4% | 38.5% | 13.5% | 25.0% | 69.4% | 116 |
| TP 1700-1799 | 4,211 | 476,878 | 22.1% | 5.6% | 45.6% | 48.8% | 11.7% | 37.1% | 62.6% | 85 |
| TP 1800-1899 | 718 | 67,513 | 30.5% | 9.6% | 31.3% | 59.2% | 17.3% | 41.9% | 75.6% | 130 |
| **TP ≥1900** | **2,330** | **305,637** | **23.5%** | **6.6%** | **61.7%** | **31.6%** | 12.5% | 19.1% | 70.1% | 100 |
| TP ≥1700 | 7,259 | 850,028 | 23.3% | 6.3% | 50.3% | 43.4% | 12.4% | 31.0% | 66.3% | 97 |
| *FIELD-IN-OUR-GAMES* | *3,836* | *507,896* | *29.6%* | *18.0%* | *46.0%* | *35.9%* | *16.8%* | *19.1%* | *70.3%* | *121* |
| **US (OpenSverige)** | **5,456** | **1,188,099** | **13.6%** | **22.0%** | **64.4%** | **13.6%** | **6.5%** | **7.1%** | **30.9%** | **18** |

**START-of-round sensitivity** (the conservative reading, §2.5): US
**22.6 / 64.8 / 12.6**; TP ≥1900 **6.8 / 62.0 / 31.2**. **The ordering is
identical in every population.** Nothing below depends on which rule is used.

### 3.2 Reproduction of the prior cut, on an independent decoder

`gunner-vs-sentinel-pricing-2026-08-09.md` is reproduced without being consulted
during the decode:

| quantity | prior doc | this decoder |
| --- | ---: | ---: |
| US sentinel % of reload ceiling | 13.5% | **13.6%** |
| US sentinel median d²_own | 18 | **18** |
| US sentinel % forward | 30.7% | **30.9%** |
| TP ≥1900 sentinel % forward | 70.1% | **70.1%** |
| Clankers % forward | 74.4% | **74.1%** |
| Clankers % of reload ceiling | 46.4% | **48.1%** |

### 3.3 (c) is fully accounted for — and the brief's ammunition assumption is wrong

The brief pre-cleared ammo — *"already ruled out (we end games holding 150.5
unspent ammo)"*. **That is an end-of-game aggregate and it does not survive a
per-round read.** Bucket assignment uses the engine's own `updatePlayers`
ammunition balance; `< 10` means the team could not have afforded one more
sentinel shot.

| population | idle rnds | (c) total | reload | **ammo < 10** | TLE | `run()` never invoked | **unexplained** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TP 1700-1799 | 476,878 | 48.8% | 11.7% | **33.2%** | 0.00% | 0.06% | 3.8% |
| TP 1800-1899 | 67,513 | 59.2% | 17.3% | **41.0%** | 0.00% | 0.06% | 0.8% |
| TP ≥1900 | 305,637 | 31.6% | 12.5% | **10.7%** | 0.00% | 0.02% | 8.4% |
| TP ≥1700 | 850,028 | 43.4% | 12.4% | **25.7%** | 0.00% | 0.05% | 5.2% |
| **US** | **1,188,099** | **13.6%** | **6.5%** | **6.4%** | **0.00%** | **0.02%** | **0.7%** |
| **US, forward-sited only** | **86,030** | **68.4%** | **40.2%** | **27.7%** | 0.00% | 0.20% | **0.3%** |
| Clankers | 31,685 | 74.0% | 30.7% | **37.5%** | — | — | — |

> **Ammunition is not ruled out — it is the price of the plank.** Our *home*
> sentinels are ammo-blocked in 4.7% of idle rounds; our *forward* sentinels in
> **27.7%**, Clankers in **37.5%**, 0033 in **53.6%**. **Ammunition is what binds
> once duty cycle is high, and we are already hitting it on the third of our
> sentinels that fire.** A forward-siting or facing change without an ammunition
> policy converts a facing problem into an ammunition problem.
>
> Two good pieces of news. **TLE is 0.00% of idle sentinel-rounds in every
> population** — the 10 ms budget is not what silences a sentinel — and the
> `run()`-never-invoked bucket is **0.02%**, so no sentinel is sitting there
> permanently disabled by an uncaught exception. And our **unexplained residual is
> 0.7%**: when a target is on our line, we are off cooldown and we can pay for the
> shot, we take it. **Our firing logic is not the problem.**

---

## 4. THE COMPARISON ARM — AND THE INTERACTION THE BRIEF ASKED ABOUT

The brief pre-stated the discriminator: *"If their (b) share is similar to ours
and only their (a) share differs, siting is the whole story. If their (b) is much
lower, they are choosing facings better."*

**It returns different answers at the band level and the doctrine level, and per
method rule 6 the band level is the one that must not be trusted.**

| population | rating | N sent | % of ceiling | **(a)** | **(b)** | **(c)** | % fwd | med d²_own |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **US** | 1604 | 5,456 | **13.6%** | **22.0%** | **64.4%** | 13.6% | 30.9% | 18 |
| **TP ≥1900 (the band)** | — | 2,330 | 23.5% | **6.6%** | **61.7%** | 31.6% | 70.1% | 100 |
| **sporks** | **2079** | 1,146 | **11.9%** | 9.4% | **80.1%** | 10.5% | 63.7% | 90 |
| Pantheon | 2002 | 500 | 22.3% | 5.6% | 46.3% | 48.1% | 67.0% | 121 |
| **Clankers** | **1989** | 499 | **48.1%** | **1.8%** | **24.2%** | 74.0% | 74.1% | 137 |
| The Flotte Experience | 1890 | 231 | 69.6% | 0.0% | 3.4% | 96.6% | 86.1% | 181 |
| not adgato | 1920 | 151 | 67.1% | 0.0% | 0.4% | 99.6% | 92.7% | 113 |
| 0033 | 1753 | 785 | 38.0% | 1.5% | 17.7% | 80.7% | 74.5% | 173 |
| Big O | 1786 | 359 | 53.2% | 1.6% | 11.3% | 87.1% | 73.0% | 89 |

**Against the ≥1900 band**: their (b) is 61.7% and ours is 64.4% — *the same* —
while their (a) is 6.6% against our 22.0%. **By the brief's rule that reads
"siting is the whole story."**

**Against Clankers**: (b) **24.2%** against our 64.4%. **By the same rule that
reads "they choose facings better."**

The ≥1900 band is the mixture the prior session already flagged. **sporks at 2079
has a (b) of 80.1% — worse than ours — and fires at 11.9% of its reload ceiling,
which is *below* our 13.6%.** Averaging sporks's 80.1% with Clankers's 24.2%
produces 61.7%, a number describing neither.

### 4.1 The population test that settles it — 41 third-party teams, ≥100 sentinels each

| correlation | value |
| --- | ---: |
| corr(rating, % of reload ceiling) | **+0.270** |
| **corr(rating, (a) NO TARGET share)** | **−0.402** |
| **corr(rating, (b) WRONG FACING share)** | **+0.067** |
| corr(rating, (c) OTHER share) | +0.135 |
| corr(rating, actual-vs-best facing ratio) | +0.138 |

> **Rating tracks (a) and does not track (b).** Strong teams are not teams that
> aim better — they are teams whose sentinels have *something in range at all*.
> **(a) NO TARGET is the only bucket that carries information about strength**,
> and it is our smallest bucket at 22.0%.
>
> **And duty cycle itself is a weak marker: r = +0.270, with the #1 team below
> us.** The 13.5%-of-ceiling figure that motivated this brief is a mechanism
> reading, not a defect.

### 4.2 THE INTERACTION — a random-facing baseline separates "aimed well" from "sited where everything works"

This is the measurement that makes the two candidate planks comparable. For every
sentinel I compute, per round, which of the **8** facings *would* have had an
enemy on the line from that same tile. Position is held fixed; only facing varies.

| population | N sent | % of ceiling | **RANDOM facing** on-line | **ACTUAL facing** on-line | **BEST of 8** on-line | **actual − random** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **US — all** | 5,456 | 13.6% | 16.6% | 19.4% | 62.5% | **+2.7 pp** |
| **US — home-sited (69.1%)** | 3,768 | 8.9% | 14.2% | **13.2%** | 58.6% | **−0.9 pp** |
| **US — forward-sited (30.9%)** | 1,688 | **58.5%** | 40.0% | **77.6%** | 98.9% | **+37.5 pp** |
| TP ≥1900 | 2,330 | 23.5% | 29.6% | 39.6% | 84.1% | +10.0 pp |
| **sporks** (2079) | 1,146 | 11.9% | 25.0% | **15.7%** | 77.4% | **−9.3 pp** |
| Pantheon (2002) | 500 | 22.3% | 26.6% | 53.8% | 84.6% | +27.2 pp |
| **Clankers** (1989) | 499 | **48.1%** | 41.1% | **80.3%** | 95.8% | **+39.1 pp** |

> **Our home sentinels aim worse than chance.** 13.2% actual against a 14.2%
> random-facing baseline — **−0.9 pp**. A coin flip over the eight directions
> would do marginally better than the predicate we ship.
>
> **Clankers's advantage is roughly half siting and half aim.** Their random
> baseline is 41.1% (ours at home is 14.2%) — **siting alone, before any aiming,
> is worth ~27 pp** — and their aim then adds a further **+39.1 pp**.
>
> **Our own forward-sited sentinels already reach +37.5 pp and 77.6% on-line —
> Clankers-class.** Our forward code path is not broken. **We have two sentinel
> doctrines in one bot, and the broken one owns **92.8% of our idle sentinel-rounds** (90.5% of live ones).**

### 4.3 The two doctrines inside our own bot, and the selection caveat stated up front

| US slice | N | med build round | med lifetime | % destroyed | idle rnds | % of ceiling | (a) | (b) | (c) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **home-sited** | 3,768 | r93 | **175** | 37.0% | **1,102,069** | **8.9%** | 23.8% | 66.9% | 9.3% |
| **forward-sited** | 1,688 | r30 | **22** | **64.8%** | 86,030 | **58.5%** | **0.0%** | **31.6%** | 68.4% |
| US — d²_own > 120 | 1,010 | — | — | — | 39,333 | **77.4%** | 0.0% | 1.1% | 98.9% |

> **THIS IS NOT A TREATMENT EFFECT AND I AM NOT PRESENTING IT AS ONE.** Our
> forward sentinels are built at round 30 into a target-saturated early rush,
> live **22** rounds against the home path's **175**, and **64.8%** of them are
> destroyed. They are a different regime, not the same sentinels moved. The
> honest reading is *"forward positions have targets in every direction"*
> (best-of-8 **98.9%** forward vs **58.6%** at home), **not** *"moving a home
> sentinel forward yields 58.5%."*

**The interaction the brief asked me to name, stated plainly:**

> **(a) and (b) are not independent, and the dependence runs one way.** Moving a
> sentinel forward does not merely delete (a); it collapses (b) as a side effect,
> because a forward tile has enemy entities on *almost every* ray. Best-of-8 rises
> from 58.6% (home) to 98.9% (forward) in our own data and from 77.4% (sporks,
> mid-field) to 95.8% (Clankers, deep). **Forward siting is not a way of finding
> targets; it is a way of making the facing decision stop mattering.**
>
> The converse does **not** hold: choosing a better facing at home cannot create
> (a)-rounds' worth of targets. **Ceiling on facing-only at our current
> positions: best-of-8 = 58.6% of home rounds, against 13.2% today.**

### 4.4 Is an empty line a *deterred* line? — the alternative, tested

A sentinel line that is never occupied could mean enemies route around a covered
corridor. That would make (b) a virtue, not a defect. **It does not rescue our
home path**, because there is no deterrence story for a sentinel aimed at your
own base:

| population | N sent | faces **exactly at our own core** | within 45° of our own core | ≥135° **away** from the enemy core | line **never** held an enemy in its whole life |
| --- | ---: | ---: | ---: | ---: | ---: |
| **US — home-sited** | 3,768 | **11.4%** | **39.8%** | **17.5%** | **13.7%** |
| US — forward-sited | 1,688 | 3.0% | 9.7% | 2.5% | 1.8% |
| TP ≥1900 | 2,330 | 5.5% | 23.8% | 5.8% | **1.1%** |
| sporks (2079) | 1,146 | 6.5% | 26.1% | 10.6% | **0.3%** |
| Clankers (1989) | 499 | 10.0% | 35.9% | 2.2% | 0.6% |

**13.7% of our home sentinels never had a single enemy entity on their line in a
median 175-round life**, against 1.1% at ≥1900 and **0.3% for sporks** — and ours
live *longer*, so lifetime cannot explain it. **11.4% point exactly at our own
core.** That is not deterrence.

*(Deterrence remains a live and untestable alternative for the **residual** (b),
and specifically for sporks, whose lines are eventually occupied 99.7% of the time
while its instantaneous on-line rate is 15.7%. See §7.)*

---

## 5. THE SMALLEST BUILDABLE THING THIS LICENSES

Since **facing is fixed at build time forever**, the change is a **build-time
predicate**, not a runtime behaviour. I priced the simplest one that exists —
*face the compass bearing from the build tile to the enemy core* — against the
same rounds, holding position and everything else fixed.

| population | N sent | RANDOM facing | **ACTUAL (shipped)** | **"face the enemy core"** | BEST of 8 | actual facing already == that bearing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **US — home-sited** | 3,768 | 14.2% | **13.2%** | **32.7%** | 58.6% | **38.6%** |
| US — forward-sited | 1,688 | 40.0% | 77.6% | 95.9% | 98.9% | 89.3% |
| US — all | 5,456 | 16.6% | 19.4% | **38.7%** | 62.5% | 54.3% |
| TP ≥1900 | 2,330 | 29.6% | 39.6% | 61.6% | 84.1% | 59.2% |
| sporks (2079) | 1,146 | 25.0% | 15.7% | 49.9% | 77.4% | 38.0% |
| Clankers (1989) | 499 | 41.1% | 80.3% | 85.8% | 95.8% | **83.0%** |

> ### **One predicate. Nothing moves. 2.5×.**
>
> **`build_sentinel(pos, pos.direction_to(enemy_core))`** — on our home path,
> **61.4% of our sentinels currently violate it**, and applying it lifts
> target-on-line from **13.2% → 32.7%** of live sentinel-rounds at **zero**
> change to siting, build count, build order, titanium, or mortality exposure.
> Clankers already satisfies it 83.0% of the time; we satisfy it 38.6%.
>
> **Why this is strictly cheaper than the forward-siting plank as written:** the
> prior document's own guard rail was that our cost-to-destroy (1,588 damage
> points vs the ≥1700 tier's 1,031) must not fall — *"sentinels moved forward are
> sentinels not defending."* **A facing change moves nothing, so that guard rail
> cannot be tripped at all.** It is also the change the brief's own fear applies
> least to: nothing is newly exposed to fire.
>
> **The ceiling on it is 58.6%** (best-of-8 at our existing tiles), so this
> captures roughly **half** the available facing headroom. The other half needs
> siting — and §3.3 says siting then needs ammunition.

**Falsifier, pre-stated.** Sentinel target-on-line rate must rise from **13.2% →
~32%** on the home path and duty cycle from **8.9% → ~18%** of reload ceiling
(reload and ammunition cap the conversion; do not expect 32%). **If on-line rate
rises and duty cycle does not, the binding constraint is ammunition (§3.3) and
the next plank is the ammunition policy, not siting.** Both are now directly
measurable per replay by this decoder.

---

## 6. THE ANSWER TO THE QUESTION THAT WAS ASKED

> **(b)-dominant at 64.4%** (N = 5,456 sentinels / 1,188,099 idle sentinel-rounds,
> OpenSverige only). Per the coordinator's pre-registration: **the plank is
> redirected, not killed.**
>
> **But the pre-registered reading needs one correction.** *"(b)-dominant ⇒
> siting alone does not fix it"* is right about the mechanism and wrong about the
> direction of the fix. **Siting does fix (b)** — that is precisely what our own
> forward path and Clankers demonstrate — because a forward tile makes every
> facing a hit. What siting cannot do is fix (b) *cheaply*, and what the facing
> predicate cannot do is reach past 58.6%.
>
> **And the premise underneath the whole brief does not survive.** *"13.5% of
> reload ceiling"* was treated as the defect. **sporks — #1 on the ladder at 2079
> — fires at 11.9%**, and across 41 third-party teams `corr(rating, duty cycle) =
> +0.270` while `corr(rating, (b)) = +0.067`. **Duty cycle is a mechanism reading,
> not a currency.** The bucket that actually tracks rating is **(a)**, at
> **−0.402** — and it is our smallest.
>
> **The one thing that is unambiguously broken and unambiguously ours:** our home
> sentinels' chosen facing performs **0.9 pp worse than a random draw over the
> eight directions**, 11.4% of them point exactly at our own core, and 13.7% of
> them never see an enemy on their line in a median 175-round life.

---

## 7. WHAT I COULD NOT MEASURE

- **No causal estimate exists here.** §4.3's home-vs-forward contrast is
  observational and the two slices differ in build round (r93 vs r30), lifetime
  (175 vs 22) and mortality (37.0% vs 64.8%). **It bounds a mechanism; it does not
  forecast a treatment effect.** The §5 facing counterfactual is cleaner — it
  holds position, round, and the enemy's realised movement fixed — but it still
  assumes **the enemy would have moved identically**. A bot that routes around
  known sentinel lines would degrade it, and nothing observational can separate
  that.
- **Deterrence is untested for the residual (b).** §4.4 kills it for the
  own-core-facing portion of our home path. It remains a live explanation for
  sporks (lines eventually occupied 99.7% of the time, instantaneous on-line rate
  15.7%) and for some of the rest of our (b).
- **Within-round ordering leaves 1.3% (ours) / 3.9% (tp) of fired rounds
  misclassified as (b)** — §2.5, mechanism identified, direction known
  (over-counts (b)), too small to move the ranking.
- **"Targetable" was taken as "any enemy entity."** `:242` defines the *gunner's*
  targetable set as *"a builder bot or a building"*; the primary never restates it
  for the sentinel. If some entity type is not a legal `fire` target, (b) is
  slightly over-counted. **T1 at 1.00000 over 452,496 fire events constrains the
  geometry but not the target-type set.**
- **The ammunition bucket uses the END-of-round team balance.** A team that dipped
  below 10 mid-round and recovered is under-counted as ammo-blocked; one that
  spent down after the sentinel's turn is over-counted. It is also a **team**
  balance — with several turrets competing, "the pool could not afford one more
  shot" is not the same as "this sentinel specifically was starved."
- **The engine was not probed.** `docs/two-session-protocol.md:138` reserves that
  for the builder arm. Reload=2, the direction enum mapping and the r²=32 line
  length are all measured from replay bytes (T1 = 1.00000, n = 452,496) rather
  than confirmed against the engine. **A five-minute builder-arm probe of
  `get_attackable_tiles_from()` would settle the line geometry to certainty.**
- **Third-party coverage is what the archiver happened to download**, not a random
  sample of the league. Per-team N is stated on every row; §4.1's correlations
  rest on 41 teams and the pattern across them, not on any single row.
- **I did not measure whether a better facing converts to `core_kill_share`.**
  Everything here is priced in target-on-line and duty cycle, which are mechanism
  currencies. §5's falsifier is stated in those currencies deliberately; the
  programme currency reading has to come from the ladder.
- **Scripts live in the session scratchpad and were not committed**, per the
  one-file constraint. `sentinel_duty2.py`'s grain — one row per sentinel
  emplacement with per-round idle classification, the 8-facing counterfactual, and
  the ammo/TLE ledgers — **is new and worth promoting into `tools/corpus/`.
  Filing that as the adjacent issue rather than doing it here.**
- **I did not run the arena, submit, activate, probe the engine, or edit anything
  under `bots/` or `tools/`. No git commit.**

---

# 8. ADDENDUM — IS THE `PREREG-loki9-facing` TREATMENT REACHABLE? (LOKI-8 / `v102` ONLY)

**Added after the main deliverable, on the coordinator's follow-up.** The
question: the treatment prefers, *among facings the existing gate already
permits*, the one pointing at the enemy core. If the gate
(`can_fire_from(bp, facing, turret_type, SLOT_THREAT)`) typically fires on a
raider **inside our own collar**, the permitted set could be near-disjoint from
the enemy-core direction and the fallback would trigger almost every time.

**Population: LOKI-8 (`v102`) ONLY — 75 our-side games, 15 matches. Not pooled
with the archive.** LOKI-8's chosen facing satisfies the gate *by construction*,
so the observed facing is a readout of where `SLOT_THREAT` was.

## 8.1 THE ANSWER: the gate is ALIGNED with the enemy-core direction, not opposed to it

Angle between the **chosen build-time facing** and the **bearing to the enemy
core**, our side only, first-`placeEntity` per entity id (TRAP 2 guarded):

| population | N builds | games | matches | 0° | 45° | 90° | 135° | **180°** | **within 45°** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **HOME turrets (gunner + sentinel) — the bar's population** | **207** | 51 | 15 | 35.7% | 25.6% | 18.8% | 12.6% | **7.2%** | **61.4%** |
| — home sentinels only | 133 | 46 | 15 | 47.4% | 23.3% | 18.0% | 5.3% | **6.0%** | **70.7%** |
| — home gunners only | 74 | 33 | 15 | 14.9% | 29.7% | 20.3% | 25.7% | **9.5%** | **44.6%** |
| FORWARD turrets | 280 | 58 | 15 | 90.4% | 6.4% | 1.1% | 1.1% | 1.1% | 96.8% |
| ALL facing turrets | 487 | 71 | 15 | 67.1% | 14.6% | 8.6% | 6.0% | 3.7% | 81.7% |
| *random draw over 8 facings* | — | — | — | *12.5%* | *25.0%* | *25.0%* | *25.0%* | *12.5%* | *37.5%* |

> ### `REFUTED` — the hypothesis that the gate points inward.
>
> The distribution is **monotone decreasing in angle** and mass-loaded at **0°**.
> Home turrets sit at **35.7% dead-on against a 12.5% random expectation (2.9×)**
> and at **7.2% at 180° against a 12.5% expectation (0.6×)**. Mean angle **58.4°**
> against **90.0°** under a random draw.
>
> **The gate-permitted set is not disjoint from the enemy-core direction; it is
> positively correlated with it.** The threat the gate fires on is, more often
> than not, already roughly *between* the turret and the enemy core.
> **The treatment is reachable. It will be permitted, not fall through to
> fallback.**

## 8.2 BUT THE SECOND THING YOU ASKED ABOUT BITES — AND IT IS WORSE THAN THE FIRST

The control-arm baseline is **already high**, and the `+30pp` bar has to fit
underneath 100%.

| bar population, as it could legitimately be read | baseline within 45° | 95% CI (cluster-bootstrap by match, n=15) | **`+30pp` bar requires** | verdict |
| --- | ---: | --- | ---: | --- |
| **home sentinels only** | **70.7%** | [56.7%, 85.1%] | **100.7%** | **ARITHMETICALLY IMPOSSIBLE** |
| **home gunner + sentinel** (as written: "turrets") | **61.4%** | [50.7%, 74.6%] | **91.4%** | reachable only at near-total compliance |
| home turrets **including the 83 home launchers** as non-compliant | **43.8%** | — | 73.8% | comfortably reachable |

> ### **THE DENOMINATOR DECIDES THE LEG, AND IT IS NOT PINNED DOWN.**
>
> LOKI-8 plants **83 home launchers** alongside 133 home sentinels and 74 home
> gunners. **A Launcher has no facing at all** (`official-docs.md:227` — *"The
> Launcher has no facing direction at all"*). Whether the bar's *"newly-built
> home turrets"* denominator includes them changes the baseline from **43.8% to
> 61.4%**, and restricting to sentinels moves it to **70.7%** — **three defensible
> readings of the bar's own wording, giving "easy", "marginal", and
> "impossible".** This must be fixed in writing **before** the leg, not
> adjudicated from the results afterwards.
>
> **And the interval is wide enough to swallow the bar on its own.** At n=15
> matches the baseline CI on the written population is **[50.7%, 74.6%]**. If the
> leg's own control arm lands at the top of that, `+30pp` is unreachable **even
> for the gunner+sentinel reading**. Max reachable rise from the observed
> baseline: **+25.4pp to +49.3pp**.

**A numerical collision worth naming before it causes an error.** The prereg
correctly labels the archive's **61.4% violation** figure as a different subject
and context only. **v102's home-turret within-45° *compliance* is also 61.4%.**
Two different statistics, two different populations, same digits, one of them a
violation rate and the other its complement's cousin. **Do not let those meet in
a results table.**

## 8.3 Does the archive figure transfer to LOKI-8? — permutation test

The prereg demotes the corpus figures because *"OpenSverige is not one bot"*.
**Correct in principle; on this particular statistic it does not bite.** Drawing
200 random 75-file samples from our 2,218 our-side games and recomputing the
home-**sentinel** within-45° share:

```
random 75-file draws : median 68.4%, 2.5-97.5% [58.6%, 78.7%]
v102 (LOKI-8) TRUE   : 70.7%
```

**LOKI-8 is statistically indistinguishable from the archive average on facing
compliance.** So the caution was right to take but the archive was, here, a fair
proxy — and that is itself bad news for the leg, because it means the ceiling is
not an artefact of a small v102 sample.

## 8.4 GUARDS — including the new, previously untested v102 selector branch

| guard | statistic | TRUE | CORRUPTED | verdict |
| --- | --- | ---: | ---: | --- |
| **G-V1** version selector | **our** builder attacks in the selected files | **0** | median **15,116** over 200 random 75-file draws (min 8,442); **0 / 200 draws reach zero** | **PASS** |
| G-V1b contrast | *their* builder attacks, same files | **5,185** | — | selector is not just selecting quiet games |
| **G-V2** version selector | our **forward gunner** plants | **5** | median **77** (min 48); **0 / 200 draws ≤ 5** | **PASS** |
| **G-B1** TRAP-2 rotation re-emit guard | our-side facing-turret builds | **487** | **855** (guard removed) | **PASS** (1.76× inflation) |
| **G-B2** facing ledger | home within-45° share | **61.4%** | **30.4%** (facings rotated 90°) | **PASS** |

The v102 selector is the new filter and therefore the untested one, so it gets
**two independent behavioural fingerprints**, neither derived from `winnerSide`:
LOKI-8's silenced melee (`batk = 0` on our side, against 5,185 on theirs in the
same files) and its near-absent forward-gunner path.

**One small correction to the prereg while I am here.** It states LOKI-8 *"plants
zero forward gunners"* from a code reading. The tape says **5 across 75 games**
(0.07/game, against a 0.66/game archive average) — consistent with a rare path or
with a midfield gunner tipping over the `d²_enemy < d²_own` boundary that defines
FORWARD. **Not a contradiction of the argument** (a leg filtering on forward
gunners would still be hopeless at n=5), but "zero" is now "5" and the sibling
prereg's n=0 claim should say so.

## 8.5 WHAT I WOULD DO WITH THIS

1. **Fix the bar's denominator in writing first** — my recommendation: **home
   gunner + sentinel, launchers excluded and said so**, baseline **61.4%**.
2. **Re-cut the bar as a relative closure, not an absolute `+30pp`.** *"Close
   ≥60% of the gap to 100%"* is scale-free, cannot become arithmetically
   impossible, and at the 61.4% baseline demands ~76.8% — a real bar that the
   fallback cannot cheaply satisfy.
3. **If `+30pp` is kept, keep it only on the gunner+sentinel population and
   record now that it is unreachable on sentinels alone.** Otherwise the leg can
   fail its own mechanism bar while the diff works perfectly, which is exactly
   the D7 misread the prereg is trying to avoid.

**Limits of this addendum.** n = 75 games / **15 matches**, and matches are the
independent unit — every interval above is quoted from a match-clustered
bootstrap for that reason. `SLOT_THREAT` is inferred from the *observed* facing
under the assumption that LOKI-8's gate is the only thing setting it; if any
other code path sets a facing, that path is silently folded in. And 8.1 measures
where the gate *pointed*, not whether the enemy-core facing would also have
**passed** the gate in the same round — that needs the round's full occupancy at
build time against `can_fire_from`, which I did not compute.
