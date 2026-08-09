# Heal cancellation on a besieged core: it is not a map-width effect, and we invert under concentration

> # ⛔ TWO CORRECTIONS (third lane, same session). THE HEADLINE IS BAND-SPECIFIC, AND ONE CONSTANT WAS WRONG.
>
> **(1) My "FIELD" is `join.tsv`-scoped, which means OUR OPPONENTS — not the league.**
> The broad field does **not** scale its guard: **no-us games cancel 34.6% at 3+
> attackers, and TOP (≥1750) cancels 31.5% — both WORSE than our 39.4%.**
>
> **So "their cancellation rises with pressure while ours falls" is true only of the
> 1500-1650 band we actually play.** It is not a property of strong play, and it is
> not a property of the league. **A scoped population presented as "the field" —
> which is a selection rule I failed to state, the same error class as the five-row
> table.**
>
> *It also flips the offensive read pleasantly: a multi-shooter chain against most of
> the ladder faces a defence that does **not** scale back.*
>
> **(2) The heal cap on a CORE is 32 HP/round, not 16.** A 2×2 core has **8**
> orthogonal ring tiles, not 4 — a geometric invariant that held in 5,470/5,470
> sides. **The 16 HP/round figure is correct only for a 1×1 building.** Every place
> below where I reasoned about the core against a 16 HP/round ceiling is wrong by a
> factor of two, and the "adjacency cap saturates at one attacker" mechanism has
> twice the headroom I claimed.
>
> **(3) And the verdict on the confound is neither of my two alternatives.** The
> third lane's cut refutes *both*: **"already lost" is dead** (5.02 live builders,
> 0.9% zero-builder rounds) **and "mispositioned" is dead** — **our adjacency 2.68
> BEATS the field's 2.49 and TOP's 1.99**, discriminator fraction 12.5% against the
> field's 40.6%, and at *fixed adjacency and fixed damage* our per-builder
> cancellation equals or beats every population.
>
> **What survives is DETAIL SIZE AGAINST A HEAVIER LOAD:** our 23.05 dmg/round needs
> **~5.8 adjacent healers** for full cancellation; we run **2.68, at 85% of its own
> cap**, with ≥1 spare live builder in 91.3% of those rounds. **And round-matched,
> our detail equals our opponents' before r250 (2.24 vs 2.30) — the entire gap opens
> at r251-500** (they grow to 3.53, we hold 2.46), **the same window as the
> forward-posture collapse.**
>
> **So my framing — "the resource is present and unspent" — is wrong in its second
> half.** We apply it about as well as anyone; **the load is heavier and the detail
> does not grow after r250.** Corrected here rather than left for a successor.

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
  are dead.

> ## ✅ CONFOUND CLOSED (same session)
>
> Live builder count reconstructed from `tl.tsv` as running builds minus deaths, per
> team per round, on the same damage-landing rounds:
>
> | attackers | who | dmg-rounds | cancel% | **mean live builders** |
> |---|---|---|---|---|
> | 1 | US | 93,710 | 65.2% | **5.62** |
> | 1 | FIELD | 77,845 | 46.4% | 5.32 |
> | 2 | US | 26,106 | 51.0% | **5.06** |
> | 2 | FIELD | 23,071 | 66.8% | 5.36 |
> | 3+ | US | 6,749 | **38.9%** | **5.02** |
> | 3+ | FIELD | 6,093 | **68.6%** | 5.06 |
>
> **At 3+ attackers we have 5.02 live builders — statistically the same as at one
> attacker (5.62), and the same as the field's 5.06.** The "our builders were
> already dead" alternative is **refuted**. We have the builders. We do not apply
> them.
>
> **So "our heal detail does not scale with the threat" survives its main
> confound**, and it is now the strongest single characterisation of our defensive
> failure: *the resource is present and unspent.*
>
> Residual: this is live builder **count**, not **adjacency to the besieged core** —
> a builder alive across the map cannot heal. The stronger version still needs
> per-round positions, which neither corpus carries.
