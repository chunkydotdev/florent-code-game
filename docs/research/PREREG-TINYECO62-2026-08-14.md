# PREREG — **TINYECO (`QUEUE #62`)**: the opening's builder count becomes a function of map area (research s40, 2026-08-14)

**STATUS: committed BEFORE the arm tree exists and before any row is filled**
(two-clock standard; side lane certifies against the first shard row).
Research designs; **the BUILDER builds and executes**; the verdict sentence is
theirs.

**Control: `bots/_v223sealrepair` (v140)**, the live holder — reactivated
16:21:36Z after the v143 displacement.

---

## THE MECHANISM, MEASURED AND VERIFIED TWICE

**We spawn EXACTLY 5 builders before the first harvester whether the map is 100
tiles or 900.** Research-verified independently of the book that raised it,
`ourver` ≥ 125, archived:

| area class | n | median first-harvester round | **median builders before it** |
|---|---|---|---|
| tiny <300 | 252 | r5 | **5.0** |
| 400 | 574 | r7 | **5.0** |
| mid 500-676 | 351 | r6 | **5.0** |
| 900 | 611 | r8 | **5.0** |

**⇒ The harvester TIMING adapts to distance; the builder COUNT does not.** A
constant where a map-aware bot would vary.

**GREP (`_v223sealrepair`): the opening has NO MAP TERM.** Spawn path
`main.py:285-302` sorts candidates by a salted key and spawns; the only gates
before harvester #1 are `SLOT_HARVESTERS`-keyed (`main.py:202`, `:548`, `:639`);
the eco caps are **absolute integers** — `ECO_CAP = 18` (`doctrine.py:30`),
`SURGE_ECO_CAP = 24` (`:405`). `mw`/`mh` are read only for geometry bookkeeping.
**The count cannot vary with area, and it does not.**

## THE TREATMENT
**One constant, one gate: on maps with area < 300, cap builders spawned before
the first harvester at 3 (from 5). Everything else unchanged; off-segment
behaviour byte-identical.**
*(3 is a 40% cut and is chosen as the FIRST dose, not as an optimum. If the arm
pays, the sweep is 2/3/4 and belongs in a second leg.)*

## ⛔ OBLIGATION 15a — SEGMENT AND DIRECTION
**MAP SEGMENT (primary): TINY, area < 300 — `fjordgate` 100 · `moonrise` 168 ·
`antler` 252.**
**EXPECTED DIRECTION: POSITIVE on-segment, ~ZERO off-segment.**
⭐ **The direction is inherited from a MECHANISM, not from a sweep hit — this is a
genuine prediction, not a replication test.** *(Contrast the three segment-sweep
candidates, whose directions came from their discovery.)*
**Exactly ONE primary segment (15b). No secondary segment is declared.**

## ⛔⛔ THE SCREEN MUST RUN ON THE TINY SET, AND THIS IS NOT A PREFERENCE
**The change is INERT by construction on ~88% of the pool** (3 of 25 maps are
area < 300). **A pooled screen would therefore dilute a real effect to near
zero — the exact dilution arithmetic Obligation 15 was written for (+6pp on 5 of
15 maps pools to +0.67pp).** ⇒ **the screen fires on the TINY MAP SET ONLY, and
a pooled number from it must never be quoted as this arm's effect.**
**Off-segment non-regression is established by CONSTRUCTION (byte-identical code
path), not by a screen — the builder should assert the diff shows no
off-segment change rather than spend rows proving it.**

## METRICS — the dose dial first, and it gates everything
1. **DOSE (must move before ANY effect is read): median builders before the
   first harvester on the tiny set must go 5.0 → ~3.0.** ⛔ **If the dose does
   not move, the arm is inert and the outcome is uninterpretable — report the
   dose and stop.** *(Two arms today read a small-n zero that turned out to be a
   broken hook rather than an inert mechanism; the dose is checked first for
   that reason.)*
2. **PRIMARY: game share on the tiny set** vs control.
3. **MECHANISM (must move in the predicted direction or the story is wrong even
   if the share moves): first-DELIVERY round** (collected = delivery to core) and
   **`get_scale_percent()` at r50** — fewer early builders is −40% of a +20%
   contribution each, so the scale curve should visibly flatten.
4. **RIDER: kill-round non-regression** (`DEFENCE_ADMISSION_BAR`), stated as an
   EXCLUSION per `CLAUDE.md`: the CI must exclude a kill-round rise, not merely
   fail to show one.

## OBLIGATION 12 — RESOLUTION AT THE COMMITTED n
**Local screens are a balanced-by-construction fixture measured at DEFF = 0.98
(ρ = −0.020, 124 shards), so naive bars are correct here — the platform
constants must NOT be applied.** At **n = 2,700 tiny-set rows**, the 95%
half-width on a share near 50% is **±1.9pp**.
⇒ **BAR: ≥ 52.0 at n = 2,700 continues; < 50.0 drops (futility).** The band
50.0–52.0 is **UNRESOLVED and carries to a second leg — it is not a pass.**
⚠ **And the standing open-condition: `GATE-1000 < 48` discards a true-50 arm
10.3% of the time.** That is accepted, and named so the drop is read correctly.

## FALSIFIER
**If the dose moves 5.0 → ~3.0 and the tiny-set share does NOT rise above 50.0,
the "map-blind opening costs us on tiny maps" story is refuted** — the count is
map-blind (measured, certain) but that blindness is not what the tiny-map deficit
is made of, and `#62` closes. **The deficit itself would then belong entirely to
`#63`'s and the book's other mechanisms.**

## TARGET-VALUE LINE
Local screen: **zero rated exposure, zero submits, zero unrated budget.** Payout
gate N/A until a live leg is proposed; **band re-read before any live leg is
sized**, and the tiny segment's live n is small (fjordgate + antler ≈ 13% of
pairings), so a live confirmation will be slow by construction — **state that
before anyone expects one this week.**

## SCRIPT NAMING (banking rule clause v)
The verification behind this prereg is a ~20-line cut over `corpus/events.tsv` +
`corpus/meta_join.tsv` (builds of kind `harvester`/`builder_bot` per file, first
harvester round, builders before it, classed by `mw*mh` from `events.tsv`),
run inline in the s40 research session. **Reproducible from that description in
under ten minutes; no scratch file to recover.**
