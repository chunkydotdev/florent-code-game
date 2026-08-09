# Heal cancellation on a besieged core: it is not a map-width effect, and we invert under concentration

**Research arm, session 23, 2026-08-09.** Cross-lane: commissioned by the third
research lane, which had cut this by map **width** as a proxy and asked for the real
axis. Their per-round table (`tl.tsv`, 388 MB, streamed) supplies core damage/heal
per round; **exact per-file core separation comes from our corpus** — a core DEATH
row carries `d2_own = 0` and `d2_enemy` = the squared distance between core anchors,
so it *is* `d²_cores`. **2,777,394 rows streamed; 1,849 files had a known
separation.**

Semantics that are easy to get wrong and are handled explicitly: `coredmg_taken` /
`coreheal_taken` are for **that row's own core**, while `atkers_on_enemy_core` is
that team's attackers on the **opponent's** core — so for a defender, the attacker
count is the *other* team's column at the same `(file, round)`.

---

## 1. Core separation is NOT the axis. Attacker count is.

Damage-landing rounds only (the third lane's denominator):

| band | 1 attacker | 2 attackers | 3+ attackers |
|---|---|---|---|
| narrow ≤81 | 45.2% | 41.6% | **31.6%** |
| mid 128-144 | 43.5% | 41.3% | **33.2%** |
| wide 288-392 | 43.2% | 38.6% | **33.8%** |
| hive 650 | 42.0% | 43.4% | 25.4% *(n=988)* |

**At one attacker, cancellation is 42-45% in every band. At 3+, it is 25-34% in
every band.** The spread *across* separations at fixed attacker count is ~3pp; the
spread *across* attacker counts at fixed separation is ~10-12pp.

**So the third lane's "on wide maps cancellation falls to 37% at 3+ attackers" is
real as an observation but mis-attributed: it is a concentration effect that exists
at every width, not a width effect.** Their revised conclusion — *concentration
pays, "concentration never pays" is dead* — **is strengthened**, and it should drop
the map-width qualifier. Net damage per damage-round rises 4.83 → 7.93 → 13.50 on
narrow maps and 5.96 → 10.54 → 16.16 on wide ones: **the same ~2.7× multiplier from
1 to 3+ attackers regardless of separation.**

## 2. The bigger finding: our heal response inverts under concentration

Splitting by **whose core is under siege**:

| band | atkers | **OUR core cancels** | **FIELD core cancels** |
|---|---|---|---|
| narrow ≤81 | 1 | **65.5%** | 32.3% |
| narrow ≤81 | 2 | 53.4% | 34.8% |
| narrow ≤81 | 3+ | **32.9%** | **50.3%** |
| mid 128-144 | 1 | **65.2%** | 32.1% |
| mid 128-144 | 2 | 45.5% | 51.8% |
| mid 128-144 | 3+ | **30.7%** | **63.0%** |
| wide 288-392 | 1 | **57.2%** | 34.0% |
| wide 288-392 | 2 | 42.6% | 43.9% |
| wide 288-392 | 3+ | **27.5%** | **64.6%** |
| hive 650 | 1 | **61.2%** | 35.7% |

**Against ONE attacker we cancel roughly TWICE what the field cancels — 57-66%
against 32-36%, in every band.** That is the strongest quantification yet of *"home
defence is our measured strength"*.

**Against THREE OR MORE it completely inverts: we collapse to 27-33% while the field
rises to 50-65%.** Their cancellation *increases* with pressure; ours *decreases*.

**The mechanism is almost certainly the adjacency cap.** At most four builders fit
orthogonally around a tile, so heal throughput on one tile is capped near 16
HP/round. **A fixed small heal detail saturates at one attacker and cannot scale to
three.** The field evidently scales its detail with the threat; we do not.

**This is the same shape as everything else measured today** — excellent in the easy
regime, collapsing in the hard one — and it is the *defensive* twin of the turret
finding (`turret-mix-and-map-width-2026-08-09.md`): best-in-corpus home turret
survival, worst-in-corpus forward survival.

## 3. What it means

- **For the third lane's S4 (healer-screen priority):** the target is not heal
  *volume* but heal *scaling*. The gap opens at 2 attackers and is decisive at 3+.
- **For the builder's home-defence work:** our single-attacker absorption is already
  the best in the corpus and does not need improving. **The whole deficit is
  multi-attacker response.**
- **It also re-frames the 2.2:1 heal-vs-damage arithmetic**: that ratio is a *rate*
  comparison, and it holds only while the defender can actually apply the heal.
  Above the adjacency cap the attacker's damage keeps scaling and the defender's
  heal does not — which is exactly the crack tactics sweep 2 identified from the
  literature (*"a linear-law resource facing a concentrable one"*), now measured on
  our own games.

## 4. Limits

- **1,849 of the third lane's files had a known core separation** (their attributed
  set is broader than our joined set); the US/FIELD split rests on `join.tsv`, a
  further subset.
- `atkers_on_enemy_core` is the third lane's decoded column; **I trust their
  semantics and did not re-derive it.** The pairing logic is mine.
- Damage-landing rounds only, so this says nothing about rounds where nothing lands.
- **Correlational.** "We cancel less at 3+ attackers" could mean our heal detail is
  too small, or that games reaching 3+ attackers are already lost and our builders
  are dead. **Those are distinguishable** — count *live builders adjacent to the
  core* at the moment of a 3+-attacker round — and that measurement has not been
  run.
