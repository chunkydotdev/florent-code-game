# ⚠ CROSS-HOST DISPERSION EXCEEDS THE BINOMIAL — and the per-host cert cannot see it
*(builder s43, 2026-08-15. Found while banking the GUNAXABL/SENTTHR remote replications.)*

## THE OBSERVATION
Three comparisons have now been run on BOTH the local box and a fleet box, same
arms, same 15-map pool, differing only in the per-host seed offset. **95% band on
a local-vs-remote difference at n=5400 each is ±1.87pp.**

| pair | local | remote | diff | vs the ±1.87pp band |
|---|---|---|---|---|
| SEALREPAIR | 59.30 | 56.77 | **+2.53** | **EXCEEDS** |
| GUNAXABL | 48.69 | 50.61 | **−1.92** | **EXCEEDS** |
| SENTTHR | 49.80 | 48.30 | +1.50 | within |

**Two of three exceed the band.** ⚠ **Directions are MIXED (+, −, +), so this is
NOT a consistent host bias** — it is consistent with **excess dispersion across
hosts beyond the binomial**, i.e. the true uncertainty on a 5400-row shard is
wider than the ±1.33pp we quote.

## WHY THE EXISTING GUARD CANNOT CATCH IT
Each host runs a `NULLHOST` certification cell — byte-identical trees, accepted at
**45–55% on n≥400**. At n=400 the half-width is **±4.9pp**. **A ~2pp host term
sits entirely inside that acceptance window**, so a host can certify clean and
still carry it. The cert was designed to catch a *bent* host (wall-clock `--tle 10`
means a faster or slower core changes WHICH TURNS TIME OUT); it is not powered for
a small one.

## WHAT THIS DOES AND DOES NOT CHANGE
* ⛔ **It does NOT change any verdict banked tonight.** `GUNAXABL` and `SENTTHR`
  were both read on the **LOCAL shard alone**, as their preregs registered
  (`PLANNED n: 5400`, `BOUNDARY: 5400 shard rows`), and both landed in the DROP
  band. The remote rows were reported separately and deliberately not pooled.
* ⚠ **It DOES mean cross-host pooling needs a variance term.** Any future prereg
  that registers pooling local + remote rows into one bar should either measure
  the host term first or inflate its interval for it. **Pooling them naively
  treats 10,800 rows as one draw when they are two draws that disagree by more
  than the binomial allows.**
* ⚠ **And it raises the bar on the "independent draws that POOL" claim** in
  `orchestrate.sh`'s header. The seed partition makes the GAMES independent; it
  does not make the HOSTS exchangeable.

## STATUS — PRIORITISING, NOT CLOSING
n=3 pairs. This **prioritises** a measurement; it does not establish a constant.
The cheap next step is a **NULLHOST at n≥5400 on each host** (byte-identical
trees, so any deviation from 50 is pure host term) — that is the same instrument
already in place, run long enough to resolve what it was never sized to see.

---

# ⚠ HOW THIN THIS IS — THE 2-OF-3 COUNT HINGES ON 0.053pp
*(side lane, verified by the builder. Recorded because the NULLHOST measurement
below is being commissioned on the strength of this count.)*

```
SEALREPAIR  +2.53   margin over the +-1.867pp threshold   +0.663pp
GUNAXABL    -1.92   margin                                +0.053pp   <- a hair
SENTTHR     +1.50   margin                                -0.367pp
```
**And the significance flips on that hair:**
```
P(>=2 of 3 exceed | null) = 0.0073     <- the reading above
P(>=1 of 3 exceed | null) = 0.1426     <- if GUNAXABL had landed 0.05pp the other way
```
⇒ **p = 0.007 and p = 0.14 are separated by five hundredths of a point on one
shard.** This does not change the conclusion — the status line already said
*"prioritises a measurement, does not establish a constant"* — **it prices how
thin the evidence under it is, and the price is: one game.**

# ⭐ AND IT DENTS A BOOTED EXEMPTION — ROUTED TO MAGNUS, NOT EDITED
`CLAUDE.md:663-666` exempts local screens from the platform design effects:
*"Local corefill/arena screens are a balanced-by-construction fixture and read
pair-weighted DEFF = 0.98 (ρ = −0.020) across 124 shards … applying the platform
constants to them would widen local intervals 24-35% for correlation that is not
there."*
**That exemption does not distinguish WITHIN-HOST from CROSS-HOST pooling.** If a
host term exists:
* **within-host bars** — 0.98 plausibly still holds and the exemption is right;
* **cross-host pooled bars** — **not covered by that measurement at all.**

⇒ **A booted rule currently reads more broadly than its evidence supports** —
the class this repo names as *a fact true of the case it was measured on and read
as general*. **`CLAUDE.md` is edited only on Magnus's directive, so this is routed
to him rather than changed.**

# THE OPERATIONAL FORM, which needs no edit and binds now
**Any prereg registering LOCAL+REMOTE pooling must measure or register the host
term FIRST.** The seed partition makes the GAMES independent; **it does not make
the HOSTS exchangeable.**

# THE MEASUREMENT, COMMISSIONED
`NULL5400` — the certified byte-identical pair (`_v146null` vs `_v146gunaxis`,
**all four files md5-identical, verified**) at **n=5400 per host**. Any deviation
from 50.0 is a pure host term; half-width ±1.33pp per host and ±1.87pp on the
difference. **Run it BEFORE any prereg registers cross-host pooling, not after.**
