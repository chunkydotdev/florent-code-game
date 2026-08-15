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
