# TLE-FIXTURE EXPOSURE RETRO — work-server-1, WORKERS=40 on ncpu=16

**Research arm, s42. 2026-08-14. Retrospective fixture audit, read-only. Nothing here retires,
revises or retracts a banked number** — per point 6 a corpus statistic prioritises a road, it never
closes one. The output for an exposed number is *"re-run on the fixed fixture"*.

---

## RULING

**The banked set IS exposed, the signed prediction HELD where it could be tested — and its
corollary is WRONG for two of the four positives, in the direction that matters.** A wall-clock
watchdog is confirmed at the engine level (`std::time::Instant::now` → `clock_gettime(8 =
CLOCK_UPTIME_RAW)`, armed inside `battlecode_titan::runner::watchdog::Watchdog::arm`), so
contention really does fire spurious TLEs and really does penalise whichever side spends more
wall-clock per turn. The one leg that straddles the 13:47:33Z bump shows exactly that: SEALREPAIRR
reads **60.51% pre-bump vs 56.38% post-bump (Δ +4.13pp, SE 2.26, p = 0.067)**, while **three
same-shape controls read ≈ 0** (local twin at the identical index split +0.55pp p = 0.81; remote
SEALFLOOR0R, never bumped, −0.24pp p = 0.92; cross-host at the un-degraded head +0.51pp p = 0.87).
**But "degraded nulls are suspect, degraded positives are conservative" only holds when the
TREATMENT is the heavier arm.** On V140VS142 and V140VS143 the control is x3r0's router —
**9,215 / 9,216 source lines carrying two complete policy trees, against our 4,757** — so the bias
runs **against the control and flatters our treatment.** Those are the two legs that fired the
v140 reactivation rule. **SEALFLOOR0R is not exposed at all** (all 5,347 rows completed
13:36:18Z, eleven minutes *before* the bump; the brief's leg list is wrong on this one). **No
decision flips**: margins are 3.7–8.1 SE against bars, and the largest bias this audit can measure
is ~4pp. **The one banked item that does not survive as written is an INFERENCE, not a number** —
`results.tsv:367`'s *"CROSS-HOST … REAL heterogeneity, so quote the verdict PER-HOST"*: the host
gap is absent pre-bump (+0.51pp, p = 0.87) and present only post-bump (−2.85pp, p = 0.004), and a
whole shard run at WORKERS=10 on both hosts (SEALFLOOR0) shows no host gap (−1.13pp, p = 0.24).
That is a *window* effect wearing a *host* label, and it needs re-deriving on the fixed fixture.
**Finally: the fixture leaves almost no footprint we record** — game length, tiebreak rate and
NOWINNER rate are all flat or move the wrong way, and our replays carry no CPU or TLE telemetry at
all. The only two instruments that saw anything were the outcome itself and the row timestamps.

---

## 0b. ⛔⛔ AMENDMENT TO THE RULING — **THE "NO DECISION FLIPS" CLAUSE WAS ARGUED IN THE WRONG UNITS**

**Added 2026-08-14T20:0xZ after a side-lane flag, against this document's own ruling. The
MEASUREMENTS below are untouched; the RULING's safety clause is not.**

The ruling says the margins are **3.7–8.1 SE** against their bars and that the largest bias
this audit can measure is **~4pp**. ⛔ **Those are different units in the same clause.**
**SE answers a SAMPLING question. The exposure is a SYSTEMATIC BIAS. An 8-SE margin gives
ZERO protection against a 6pp bias.** Restated in the currency that actually binds — pp
against pp:

| leg | share | bar | **MARGIN** | flips if bias exceeds | proxy bias | **cushion** |
|---|---|---|---|---|---|---|
| V140VS142 | 56.80 | 51.0 | **5.80pp** | 5.80pp | 4.13pp | **1.40×** |
| V140VS143 | 57.06 | 51.0 | **6.06pp** | 6.06pp | 4.13pp | **1.47×** |

⛔ **AND THE PROXY DOES NOT TRANSFER, WHICH IS THE SHARPER HALF OF THE FLAG.** The 4.13pp
comes from the SEALREPAIRR straddle — but **SEALREPAIRR's arms are `_v223sealrepair` vs
`_v218mapfix`, 4,757 vs 4,522 lines: asymmetry 1.05×, i.e. essentially SYMMETRIC.** The two
reactivation legs run **4,757 vs 9,215 lines: asymmetry 1.94×**, and per §5 **V140VS143 was
additionally co-resident at ~5× oversubscription.** *(All four line counts re-derived by
this lane rather than relayed.)*

**Compute asymmetry IS the mechanism this document identified. A bias measured where the
mechanism is nearly absent is not a bound on that bias where the mechanism is strong.**
That is a number true SOMEWHERE used SOMEWHERE ELSE.

⇒ **CORRECTED DISPOSITION FOR THESE TWO LEGS: EXPOSED-AND-UNRESOLVED, not
exposed-and-safe.** The magnitude at 1.94× asymmetry is **UNMEASURED**, and a 1.40× cushion
over an untransferable estimate is thin rather than comfortable. **The measured direction
still says contention FLATTERED us on both** — so the untested possibility is that we held
the slot against better bots.

**WHAT BOUNDS THE URGENCY, and it is why this is an amendment rather than an alarm: THE
EXPOSURE IS HISTORICAL, NOT LIVE.** v142 and v143 are off the slot; the live question is
v145, and **V140VS145B is already re-firing at WORKERS=10 on the fixed fixture.**
⇒ **nobody needs to undo anything, and the number governing the CURRENT slot is being
produced correctly.** ⚠ **But the conditional is worth writing down now while it is cheap:
if v145's clean read comes in BELOW 51.0, the v142/v143 pattern stops being historical and
becomes a live question about whether we have been systematically holding the slot against
better bots.** If it comes in above, the historical question is moot.

*(Raised by the side lane; the flag was possible only because §3 had already labelled the
compute-asymmetry column as INFERENCE FROM SOURCE STRUCTURE, NOT MEASUREMENT — a caveat
this document wrote about itself and then did not apply to its own ruling one section
later. Same class as the two self-corrections in the CAL-8 read.)*

---

## 1. THE FIXTURE, ESTABLISHED FROM THE RECORD

| fact | value | source |
|---|---|---|
| box | `worker@work-server-1`, **ncpu = 16** (recorded as 48) | Magnus → builder; `worker.log` ncpu=16 workers=40 load_ceil=20 from ≥ 15:49:25Z |
| bump | `WORKERS` 10 → 40 at **2026-08-14T13:47:33Z** (executed 13:46:12Z) | `docs/coordination.md:47703` |
| pre-bump setting | WORKERS=10, worker restarted 13:26:43Z | `docs/coordination.md:47507`, `:46303` |
| box lifetime | first row 11:24:29Z; nothing on this host predates it | `overnight-remote/worker@work-server-1/NULLHOST.tsv` |
| TLE | `--tle 10`, hardcoded and non-optional in the runner | `tools/vps/worker.sh:271-282` |
| local box | **ncpu = 10**, `corefill.sh` MAX_SHARDS=8, LOAD_CEIL=11.0, one game at a time per shard | `sysctl hw.ncpu`; `tools/corefill.sh:62,66`; `tools/overnight.sh:99-110` |

**Oversubscription ladder (games per core):** remote pre-bump **0.63×** (10/16) · local **≈ 0.8×**
(≤8 concurrent on 10 cores) · remote post-bump **2.5×** (40/16) · **remote post-bump with a second
shard co-resident ≈ 5×** (see §5).

### 1a. The TLE is wall-clock — measured on the engine, not assumed

`docs/coordination.md:47703` states, in the bump note itself, *"The 10ms budget is CPU time, mostly
contention-immune"*. `tools/vps/worker.sh:71` states the opposite. **The engine settles it.**
Disassembly of `fcode_engine.cpython-313-darwin.so` (fcode 2.3.6, the pinned version):

```
__RNvMNtCsaLOjE9VYtxK_3std4timeNtB2_7Instant3now:
  5f958  mov  w0, #0x8                      ; clockid 8 = CLOCK_UPTIME_RAW (macOS) — WALL CLOCK
  5f95c  b    std::sys::pal::unix::time::Timespec::now   ->  clock_gettime
```
and the sole call site of `Instant::now` in the whole binary is at `0x33b90`, inside
**`battlecode_titan::runner::watchdog::Watchdog::arm`**, which takes the TLE as a float in `d0`.
Rust `std` exposes no CPU-time clock at all. ⇒ **the turn budget is a wall-clock watchdog.**
*(Measured on the darwin build present in this repo. The remote box runs the manylinux wheel of the
same pinned 2.3.6; on Linux `Instant::now` is `CLOCK_MONOTONIC`, also wall-clock. Labelled
INFERENCE for the Linux build; the mechanism is identical Rust source.)*
**The builder's 13:47:33Z parenthetical is the one that is wrong, and it is the reason the bump was
executed with only a straddle guard rather than a hold.**

### 1b. Our own timestamps confirm ncpu ≈ 16 independently

SEALREPAIRR throughput, same bots, same map cycle, same shard, split at the bump:

| segment | WORKERS | games | wall | **games/min** |
|---|---|---|---|---|
| pre-bump | 10 | 509 | 10.8 min | **47.2** |
| post-bump | 40 | 4,885 | 142.8 min | **34.2** |
| post-bump, sole-occupant stretch 14:45–14:50 | 40 | ~200 | 5 min | ~40 |

**Quadrupling the worker count LOWERED throughput by 28%.** On a 48-core box that is impossible;
on a 16-core box with `LOAD_CEIL=20` (which a 40-wide run exceeds permanently, forcing the worker's
own 30 s holds) it is exactly what you expect. **This is independent corroboration of the ncpu fact
from data we already had on disk, and it was legible at 13:50Z.**

---

## 2. THE SIGNATURE HUNT

### 2a. What DID show — the straddle, with three controls

Command: split each shard's rows on `ts` at the bump, and on `game` index at 509 (the row the bump
landed on) for shards that were never bumped. DEFF 0.98 (local balanced-by-construction fixture)
applied throughout; platform DEFFs deliberately NOT used.

| test | segments | Δ | SE | z | p |
|---|---|---|---|---|---|
| **A. SEALREPAIRR, pre vs post bump** | 60.51 (n=509) vs 56.38 (n=4,885) | **+4.13pp** | 2.26 | +1.83 | **0.067** |
| B. control — LOCAL twin, same idx split, no bump | 59.80 (n=505) vs 59.25 (n=4,891) | +0.55pp | 2.27 | +0.24 | 0.81 |
| C. control — SEALFLOOR0R, same idx split, all WORKERS=10 | 53.44 (n=509) vs 53.68 (n=4,838) | −0.24pp | 2.30 | −0.10 | 0.92 |
| **D. cross-host, idx-matched HEAD (neither degraded)** | R 60.31 vs L 59.80 | **+0.51pp** | 3.05 | +0.17 | 0.87 |
| **E. cross-host, idx-matched TAIL (remote degraded)** | R 56.40 vs L 59.25 | **−2.85pp** | 0.99 | −2.89 | **0.0039** |
| F. control — SEALFLOOR0 whole shard, remote all WORKERS=10 | R 53.66 vs L 54.78 | −1.13pp | 0.95 | −1.18 | 0.24 |

**Read D and E together: the cross-host gap that `results.tsv:367` banked as host heterogeneity is
zero in the pre-bump half of the same shard and −2.85pp (p = 0.004) in the post-bump half.** F says
the same thing from a different shard: a full 5,400-row remote screen run entirely at WORKERS=10
shows no significant host gap. **Test A alone is p = 0.067 and would not carry a claim; A + B + C +
D + E + F is a pattern with one positive cell and five nulls arranged exactly where the mechanism
predicts.** Labelled: A is the direct test, B/C/F are pre-specifiable controls, D/E is the
decomposition of an already-banked anomaly.

### 2b. What did NOT show — report the negatives

Three candidate footprints were checked and **none of them works as a detector**:

| candidate | pre-bump | post-bump | local (un-degraded) | verdict |
|---|---|---|---|---|
| mean game length (turns) | 291.1 | 299.5 | 298.6 | **no signal** — local matches POST, not PRE |
| tiebreak rate | 5.30% | 6.39% | 6.52% | **no signal** — same |
| NOWINNER rate (`timeout 120` kills) | 0/509 | 6/4,891 = 0.12% | 4/5,400 = 0.07% | **WRONG WAY at shard level**: SEALFLOOR0R at WORKERS=10 has the highest rate in the whole corpus, 53/5,400 = 0.98% |

**⇒ If you did not already know the bump time, you could not find it in the shard rows.** The
outcome column and the timestamp column are the only two instruments that saw anything, and the
outcome column only works because we happen to hold an un-degraded twin of the same shard.

### 2c. Seat, for completeness

Seat asymmetry is large everywhere and is balanced by construction (treatment takes seat A on even
idx, B on odd), so it cancels out of every headline share. SEALREPAIRR A−B goes +2.60pp (pre,
n=509) → +9.31pp (post); local twin +6.00pp; SALTREF +9.85pp; NULLHOST +3.00 / +5.00. The pre→post
move is z = 1.47 on a thin pre-segment — **not resolvable, recorded so the next reader does not
re-derive it.**

---

## 3. COMPUTE SYMMETRY OF THE ARMS — THE PART THAT FLIPS THE SIGN

`diff -rq` on the two trees of each leg, plus total non-`__pycache__` Python lines:

| leg | treatment | control | LOC T vs C | heavier arm | bias runs |
|---|---|---|---|---|---|
| SEALREPAIR / SEALREPAIRR | `_v223sealrepair` | `_v218mapfix` | 4,757 vs 4,522 (2 files differ) | **treatment** | against treatment |
| SALTREF | `_v231saltref` | `_v223sealrepair` | 4,774 vs 4,757 (2 files differ) | **treatment**, marginally | against treatment |
| SEALFLOOR0R | `_v219sealfloor0` | `_v197mapcode` | 4,522 vs 4,522 (1 file differs) | ~symmetric | ~none |
| **V140VS142** | `_v223sealrepair` | `_x3r0v142` | **4,757 vs 9,215** | **CONTROL** | **against control ⇒ flatters us** |
| **V140VS143** | `_v223sealrepair` | `_x3r0v143` | **4,757 vs 9,216** | **CONTROL** | **against control ⇒ flatters us** |
| V140VS145 (voided) | `_v223sealrepair` | `_x3r0v145` | **4,757 vs 110,184** | **CONTROL, extremely** | against control ⇒ flatters us |
| NULLHOST | `_v146null` | `_v146gunaxis` | **md5-identical, all four .py files** | neither | none possible |

x3r0's v142/v143 are *routers*: each ships a `p_`/`n_`-prefixed complete second policy tree
alongside a dispatcher. v145 ships roughly twenty-three of them.

**⚠ MEASUREMENT ATTEMPTED AND IT DID NOT RESOLVE — stated because the brief said measurement beats
reasoning, and here it did not deliver.** Two probes were run:
1. **Replay CPU telemetry: DOES NOT EXIST LOCALLY.** Decoding `botOutput` (field 9) events out of
   locally-generated replays at both `--tle 0` and `--tle 10`, the only sub-fields present are
   **field 1 (entity id)** and occasionally **field 2 (stdout string)**. There is **no `execTimeUs`
   and no timed-out flag** in engine 2.3.6's local replay output. (`CLAUDE.md`'s `execTimeUs` note
   describes PLATFORM replays.) 12 games decoded, 0 exec-time records.
2. **Wall-clock self-play regression** (each bot vs itself, 4 maps, `--tle 0`, µs per unit-turn
   fitted against unit-turn count): **the fit is noise** — it returns a *negative* slope for
   `_v223sealrepair` and an intercept of 10 s. Single-seed games on a laptop cannot separate a
   1–2 s process/import constant from a per-turn cost. Ratio-of-totals ranks
   `_x3r0v145` (455 µs/unit-turn) > `_x3r0v142` (361) > `_v223sealrepair` (297) >
   `_v231saltref` (227) > `_v218mapfix` (211), which is directionally consistent with the LOC
   table, but the same statistic ranks `_x3r0v143` at 200 — i.e. it disagrees with itself on the
   two nearly-identical x3r0 builds. **Do not cite these numbers as a compute measurement.**
   **The compute-asymmetry column above is INFERENCE from source structure, not measurement.**

---

## 4. NULLHOST IS NOT AN IMMUNITY CERTIFICATE — VERIFIED, NOT INHERITED

The claim under audit: *"NULLHOST certifications are immune because they run identical trees and
are therefore symmetric."* **Checked three ways; the claim is true and it is also useless.**

1. **The arms really are byte-identical.** `md5` of `main.py`, `doctrine.py`, `eco.py`, `raid.py` is
   pairwise equal between `_v146null` and `_v146gunaxis`; the concatenated digest matches
   (`e39f0c97…`). So NULLHOST's expected T-share is 50% under **any** fixture, degraded or not.
2. **Which is exactly why it has ZERO POWER against this failure mode.** A detector whose expected
   value is 50% whatever the contention is cannot report contention. **NULLHOST is a positive
   control for the scoring harness and the map/engine pin. `worker.sh:66-75` advertises it as the
   instrument that "catches a bent ruler … the specific mechanism is WALL-CLOCK TLE PARITY" —
   that advertisement is wrong for the asymmetric case.** It catches a host that is broken for both
   arms; it is blind to a host that is unfair between arms, and unfairness between arms is the only
   thing that moves a screen. Seat is balanced by construction too, so it cannot even catch a
   seat-directional effect.
3. **And on work-server-1 it never sampled the degraded regime anyway.** NULLHOST completed at
   **11:29:21Z at WORKERS=10** — 2h18m before the bump. Every WORKERS=40 row on that box is
   certified by a null that was run under a different fixture. The worker's NULLHOST-first ordering
   is per-HOST, not per-CONFIGURATION, so a `WORKERS` change re-fixtures the box without
   re-triggering the cert.

**Re-derived numbers, since the brief asked (mine, not inherited):**

| cert | host | fixture | T-share | SE | **95% CI** | consistent with 50? |
|---|---|---|---|---|---|---|
| NULLHOST | work-server-1 | ncpu 16, WORKERS=10, pre-bump | 49.00% (196/400) | 2.50 | **[44.10, 53.90]** | yes |
| NULLHOST | work-server-2 | ncpu 6, WORKERS=4 | 52.00% (208/400) | 2.50 | **[47.10, 56.90]** | **yes** |

⛔ **Erratum on an input handed to me:** the server-2 cert was relayed as *"52.0%, 95% CI
[45.1, 54.9]"*. **[45.1, 54.9] is not a CI around 52.0 — it is 50.0 ± 4.9, i.e. the reader's
45–55% ACCEPTANCE BAND.** The actual 95% CI around 52.0 at n=400 is **[47.1, 56.9]**. The
conclusion is unchanged (52.0 is 0.80 SE from 50 and the band is cleared), but a band quoted as a
CI will eventually be read as one, and this one is *narrower* than the true CI — it flatters.

---

## 5. THE CONCURRENCY FINDING — V140VS143 IS WORSE OFF THAN THE OTHERS

Per-minute row counts on work-server-1 (`ts` truncated to the minute, all shards):

* **14:52–15:15 — V140VS142 ran ALONE.** SEALREPAIRR drops to 0 rows/min for the entire window and
  resumes at 15:16. Exposure = 40 workers / 16 cores = **2.5×**.
* **15:49–16:10 — V140VS143 ran CONCURRENTLY with SEALREPAIRR**, both emitting 20–40 rows/min in
  the same minutes; and **16:10–16:19 concurrently with SALTREF**. Exposure ≈ **80 concurrent
  games / 16 cores ≈ 5×**.

`docs/coordination.md:48913` records the intent as *"SEALREPAIRR resumes after it"* — which is what
happened for v142 and is **not** what happened for v143. **So the leg with the biggest margin
(6.06pp, 3.91 SE) is also the one run on the worst fixture, and its only un-degraded corroboration
is a 118-game local stub.** Same window re-exposes SEALREPAIRR's tail (idx ~4,800–5,400) and
SALTREF's first ~400 rows.

---

## 6. EXPOSURE TABLE

Host/WORKERS derived from row timestamps against the 13:47:33Z bump, not from the leg's label.
SE uses DEFF 0.98 (local balanced-by-construction fixture — platform DEFFs 1.529/1.833 deliberately
NOT applied). "bar" is the leg's own registered bar (GATE-1000 = 51.0 per Magnus `c62f90c`;
O'Brien-Fleming final band upper edge = 51.34).

| leg | date (UTC) | host | WORKERS | n | share | bar | margin | SE | **margin/SE** | direction of bias | **verdict** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **V140VS142** | 14:51–15:16 | work-server-1 | **40** (sole occupant, 2.5×) | 1,000 | 56.80 | 51.0 | +5.80pp | 1.55 | **+3.74** | **flatters us** (control is 2× our LOC) | **EXPOSED — anti-conservative; decision survives** |
| **V140VS143** | 15:49–16:19 | work-server-1 | **40 + co-resident shard (≈5×)** | 999 | 57.06 | 51.0 | +6.06pp | 1.55 | **+3.91** | **flatters us** | **EXPOSED — anti-conservative, worst fixture; decision survives** |
| **SALTREF** | 16:10–18:17 | work-server-1 | **40** (2.5×; first ~400 rows ≈5×) | 5,400 | 49.11 | 51.0 | −1.89pp | 0.67 | **−2.80** | against treatment (masks a real effect) | **EXPOSED — the suspect class; bounded by a local replication, see below** |
| **SEALREPAIRR** | 13:36–16:10 | work-server-1 | **10 → 40 at row ~509** | 5,394 | 56.77 | 51.34 | +5.43pp | 0.67 | **+8.13** | against treatment (conservative) | **ROBUST on the verdict; its CROSS-HOST inference is EXPOSED** |
| **SEALFLOOR0R** | 11:29–13:36 | work-server-1 | **10 (never bumped)** | 5,347 | 53.66 | 51.34 | +2.32pp | 0.68 | **+3.43** | ~symmetric arms anyway | **ROBUST — NOT EXPOSED; the brief's leg list is wrong here** |
| SEALREPAIR (local twin) | 09:32–16:01 | local mac | ≤8 on 10 cores | 5,396 | 59.30 | 51.34 | +7.96pp | 0.66 | +12.03 | none | ROBUST |
| V140VS145 | 19:23–19:36 | work-server-1 | 40 | 480 | 50.42 | 51.0 | −0.58pp | 2.26 | −0.26 | flatters us | **already VOIDED by the builder — correctly** |
| NULLHOST (s1) | 11:24–11:29 | work-server-1 | 10 | 400 | 49.00 | band 45–55 | — | 2.50 | — | none possible | ROBUST but **does not certify the WORKERS=40 fixture** |
| NULLHOST (s2) | 19:28–19:37 | work-server-2 | 4 on ncpu 6 | 400 | 52.00 | band 45–55 | — | 2.50 | — | none possible | ROBUST, CI [47.1, 56.9] |
| V140VS145B | 19:36– | work-server-1 | **10** | 40 (running) | 42.50 | 51.0 | — | 7.82 | — | none | UNREADABLE at n=40 — the un-degraded re-fire, let it finish |

**UNPLACEABLE: none.** Every leg in the brief was placed from its own row timestamps against the
bump; nothing had to be guessed. The two things I could NOT establish from the record are (i) the
per-arm CPU cost (§3 — no telemetry exists) and (ii) whether `LOAD_CEIL=20` holds were interleaving
during specific blocks (throughput dips at idx 3,200–3,599 and 4,800–5,199 are consistent with
either holds or co-residency).

### "Margins were mostly > 3 SE" — the actual number

**5 of the 6 readable screens clear ±3 SE (3.43, 3.74, 3.91, 8.13, 12.03).** The sixth is
**SALTREF at −2.80 SE, and it is the one that fails the bar** — i.e. **the only leg that does not
have a 3-SE cushion is precisely the leg whose verdict the bias could have manufactured.** The
reassurance is true and it lands everywhere except where it was needed.

### Survival under the measured bias

The largest bias this audit can put a number on is the SEALREPAIRR straddle, **4.13pp ± 2.26**
(95%: roughly −0.3 to +8.6pp). Applying it as a flat shift:

* **V140VS142**: 56.80 − 2.40 (its own measured remote-vs-local gap, +2.40pp, p = 0.28) = **54.40**;
  still > 51. Even at the full 4.13pp it is 52.67 > 51. **Decision holds.**
* **V140VS143**: 57.06 − 4.13 = **52.93** > 51. At the pessimistic 8.6pp upper edge it would be
  48.5 and the decision would flip — but that edge is unsupported and its local twin (n=118) reads
  57.63, Δ −0.57pp. **Decision holds; corroboration is thin.**
* **SALTREF**: 49.11 + 4.13 = **53.24**, which would clear the 51 bar. **This is the one arithmetic
  that changes an answer.** Against it: the arms differ by ~17 LOC (vs 235 for SEALREPAIR), and the
  **pre-migration LOCAL stub at n=1,025 reads 49.95 (Δ −0.84pp vs remote, SE 1.69, p = 0.62)** on
  a fixture at ≤0.8× oversubscription. That bounds the plausible SALTREF bias well under 4pp.
  **Verdict: EXPOSED, re-run before the #48b rung is cited as measured — but the local stub says a
  verdict flip is unlikely, not merely undecided.**

### What must be re-derived rather than re-run

`results.tsv:367` reads *"CROSS-HOST: local 59.30 vs remote 56.77, delta 2.53pp z~2.7 — REAL
heterogeneity, so per the audit D26 rule the verdict is quoted PER-HOST"*. **The heterogeneity is
real; the attribution to HOST is not supported.** Pre-bump the two hosts agree (+0.51pp, p = 0.87)
and a whole WORKERS=10 shard pair agrees (−1.13pp, p = 0.24). **This costs nothing to fix — the
rows already on disk carry the answer — and it should be re-derived, not re-run.** Note the
D26 per-host quoting rule stays useful; it is the *diagnosis* that was wrong, and quoting per-host
happens to have been the safe response to it.

### Note on the straddle guard, because it nearly worked

The builder pre-committed the guard **before** any affected final and executed it: SEALREPAIRR's
boundary was bracketed [390, 470] and the two segment deltas reported as **+2.66pp@390 / +4.01pp@470,
direction noted as "observation only"**. My timestamp split gives **+4.13pp** — the guard measured
the right thing, to within noise, and then licensed the pool because a 4pp gap on a 509-row head
segment (SE 2.17) is not resolvable. **The guard's design was right and its decision rule was
underpowered by construction**: a boundary at row 509 of 5,400 can never resolve a bias of the size
that matters. A guard placed at a bump should either bracket at the MIDPOINT of the shard or
declare in advance that it can only detect ≥ ~6pp.

---

## 7. WHAT WE FAIL TO RECORD — the answer to "what would we have to start recording"

**Not one of the five facts needed to audit a shard is in the shard's own file.** `ts / shard /
game / map / seed / seat / winner / cond / turns` is the entire row schema
(`tools/vps/worker.sh:280-320`, `tools/overnight.sh:99-130`). Host is inferable only from the
directory the file was pulled into. WORKERS, ncpu, load ceiling and engine version exist only as
prose in `docs/coordination.md`, and the ncpu value there was wrong for the whole day.

**Cheapest fixes, in order of value per line of code:**

1. **A shard HEADER row: `# host=<h> ncpu=<n> workers=<w> load_ceil=<c> engine=<v> started=<ts>`,
   and re-emit it whenever any of those change mid-shard.** This alone would have made the bump a
   visible column instead of a forensic exercise, and it is ~3 lines in `worker.sh`. **A shard that
   cannot state its own fixture cannot be audited, and today two of them changed fixture
   mid-flight.**
2. **Per-row wall duration.** `ts` is the game's COMPLETION time only; start time is discarded, so
   per-game latency is unrecoverable and contention is only visible as batch-level throughput.
   One `date +%s` before the run. **This is the direct observable for the failure mode and it is
   free.**
3. **Per-team TLE counts per game.** This is the actual quantity in question and **we cannot get
   it**: engine 2.3.6's local replays carry no `execTimeUs` and no timed-out flag (§3). Either ask
   the organisers for a local-replay timing field, or accept that TLE incidence is permanently
   unobservable on our own fixture and rely on (1) + (2) as proxies. **Recording this as a known
   blind spot is itself the deliverable — the current situation is that we believed we could read
   it.**
4. **Re-run NULLHOST on every FIXTURE change, not every HOST change** — and stop describing it as
   the instrument that catches wall-clock TLE unfairness (`worker.sh:66-75`), because §4 shows it
   provably cannot. The instrument that *would* work is a **deliberately asymmetric null**: the
   same bot against itself with one arm wrapped in a fixed per-turn busy-loop, run at the live
   WORKERS setting. That has non-zero power against exactly this failure and costs one cheap shard.

---

## 8. DID THE SIGNED PREDICTION HOLD?

**The mechanism: YES.** Wall-clock TLE confirmed at the engine; the one within-fixture test
(SEALREPAIRR straddle) moved 4.13pp in the predicted direction with three controls at zero and the
cross-host anomaly decomposing cleanly onto the bump.

**The corollary as stated in the brief — "nulls suspect, positives conservative": NO, and the
exception is not a technicality.** The sign attaches to *compute weight*, not to the *treatment
label*. Two of the four "conservative" positives (V140VS142, V140VS143) have the heavy arm on the
CONTROL side, so contention flatters our number — and those two are the ones that fired ship
decisions under `X3R0_SLOT_RULE`. **A rule of thumb keyed to "treatment" would have marked exactly
the wrong two legs as safe.** The durable form: **check which tree is bigger, every time; the arm
label carries no information about compute.**

**And one leg in the brief's list was never exposed at all** (SEALFLOOR0R, complete 11 minutes
before the bump), which is the ordinary reason to place every leg from its own rows rather than
from the list you were handed.
