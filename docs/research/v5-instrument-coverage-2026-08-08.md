# v5 — Where Elo actually bleeds, vs. where we have a valid instrument

Research arm, 2026-08-08 s19. Archive-only (176 rated matches with Elo deltas),
zero downloads. Inherits tonight's probe-fidelity verdicts rather than assuming
the fleet is sound.

## 1. Where the bleed is

Net Elo across all archived rated matches is **+8** — but that nets a **−493
gross bleed** against a matching gain. The bleed is extraordinarily concentrated:

| opponent | matches | net Elo | share of bleed | games | cum |
|---|--:|--:|--:|---|--:|
| Lunds Stallions | 17 | −135.5 | 27.5% | 21-64 | 27% |
| Ouroboros | 12 | −123.6 | 25.0% | 10-50 | 53% |
| Kings College Munich | 14 | −88.4 | 17.9% | 21-49 | 70% |
| CtrlAltDefeat | 14 | −57.0 | 11.6% | 24-46 | 82% |
| arsonist duck | 2 | −28.3 | 5.7% | 1-9 | 88% |
| Powerpuff Girls | 12 | −26.9 | 5.5% | 27-33 | 93% |
| kladde | 2 | −15.4 | 3.1% | 1-9 | 96% |
| Focalground / Clankers / Bisons | 6 | −18.4 | 3.7% | — | 100% |

**Four opponents carry 82% of all Elo we have ever lost.**

## 2. Instrument coverage against that bleed

Fidelity status from tonight's audits (`probe-fidelity-guards`,
`probe-fidelity-orizon-flotte`, `probe-fleet-staleness`):

| bleed source | share | frozen instrument | fidelity verdict |
|---|--:|---|---|
| **Lunds Stallions** | 27.5% | — | **NONE EXISTS** |
| **Ouroboros** | 25.0% | `ouroboros_probe` | **RETIRED** (drop-probe; behavioural fidelity ≠ predictive fidelity, twice measured) |
| **Kings College Munich** | 17.9% | — | **NONE EXISTS** |
| CtrlAltDefeat | 11.6% | `cad_probe` | **DISCLAIMED** (P6-widened: wild v117 fields no launcher, no forward sentinels — gate-map cells are matchup artefacts) |
| arsonist duck | 5.7% | — | none exists |
| Powerpuff Girls | 5.5% | — | none exists |
| kladde | 3.1% | `kladde_probe` | **INVALID** — ~70pt calibration gap; turret composition never faithful (33% gunner vs wild 62–70%) |

**Coverage of the bleed by a currently-valid instrument: 0.0%.**

Not "thin" — **zero**. Every probe that maps onto a real bleed source is
retired, disclaimed, or invalid. The two instruments that ARE valid point at
opponents we beat:

| valid instrument | its opponent | our record there |
|---|---|---|
| `orizon_probe` (class-valid; +11.6 discounts to ≈+6-8) | Orizon | **+4.8 Elo, 12-8** |
| `band_probe` (valid, RUSH MODE ONLY) | Banminary | **+78.7 Elo, 27-8** |

## 3. What this means

The local instrument stack is **aimed almost exactly away from where we lose**.
Every gate we have run tonight — every "guards green", every class-weighted
battery — was scored against opponents that contribute ~0% of our bleed, using
replicas of opponents we beat.

This is a sharper answer to the gate/ladder divergence question than
"underpowered". An instrument can be perfectly powered and still uninformative
if it measures a population that is not the one costing us. **Both are true
here: n=120 gives 19% power (v1), and the thing being measured at 19% power is
the wrong population (this study).**

It also re-reads the probe-fleet problem. The fleet is not merely stale — it was
**built against the teams we were already beating or could most easily
replicate**, and the three hardest bleed sources (Lunds 27.5%, KCM 17.9%,
arsonist duck 5.7% — 51% of bleed combined) have never had an instrument at all.

## 4. Consequences, ordered

1. **Building a Lunds instrument is worth more than any plank in the queue.**
   27.5% of all bleed, 0 match wins in 17, and tonight's decode (`lunds-switch-decode`)
   already names two mechanisms — their absolutely-oriented r3 launcher insertion,
   and our own `hive_magazine`.
2. **KCM at 17.9% is entirely undecoded** — no probe, no first-read, no decode
   document. It is the largest completely-unexamined bleed source we have.
3. **Ouroboros at 25.0% is instrument-blocked by a measured law**, not by
   neglect: the probe was retired because behavioural fidelity did not predict.
   Re-freezing it would repeat a refuted approach; that one needs a different
   method, not a fresh extraction.
4. Do NOT read "guards green" as field evidence. Guards are `kladde_probe`
   (invalid) and `band_probe` (valid but rush-only, and its wild counterpart is
   one we beat by +78.7).

## 5. Limits

Elo deltas are per-match and noisy (per-match sd ≈9.25); opponent totals over
1–17 matches carry wide intervals, and the tail rows (n≤4) should be read as
"present" not "measured". The concentration in the top four (57 matches) is
robust to that; the ordering within the tail is not. This study also says
nothing about whether a valid instrument would have *predicted* ladder outcomes
— that is v2, which remains unrunnable as specified (regression dilution, 4
joinable ships).
