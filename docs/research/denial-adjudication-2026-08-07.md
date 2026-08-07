# Denial Adjudication — Ouroboros eider/meander first-gunner (2026-08-07)

Read-only. Resolved entirely from local data already on disk — zero downloads,
zero `fcode` calls. Total spend: two local replay decodes (already-archived
files) run through the existing `decode.py` + `siege_geometry.py` toolkit.

## Verdict

**Not a definitional collision, not Ouroboros-version drift — it's an
our-own-version-era sample mismatch, plus one small classification bug in the
denial book's meander row.**

1. Both sources measure the *same* tile-concept: Ouroboros's literal
   first-built gunner (the "home picket," station 0 of its build queue), with
   dsq computed to **our** core in both cases. Session-12's "phase-2 creep to
   dsq 1-9" is a later stage of the *same* games, not a different definition
   of "first-gunner." Confirmed directly: `session12-decoders/decode.py`
   (the actual tool behind the session-12 numbers) prints
   `dsq_to_ourcore = min_dsq_to_footprint(pos, r.core_fp[1])` — footprint
   index 1 is always the defender (us) — for exactly the first-build-per-kind
   entry. No creep-vs-picket mixup on either side.
2. Ouroboros's own version is **not** the variable. `thread1_determinism.md`
   tags match `89114461-4764-4636-bcac-6526e9bfcd3c` — one of the five match
   prefixes `bots/ouroboros_probe/main.py`'s docstring cites as session-12's
   13-replay source — as `Ouroboros oppv8, atoll, ourv53`. Today's local
   archive (`bab61537…meta.json`, `22f55a05…meta.json`) is also Ouroboros
   **v8**. Stable throughout.
3. **Our own version is the variable, and it's a big one.** Session-12/the
   probe decoded matches from our **v53/55/59** era (the `ourv53` tag above,
   plus `spitball.md:289`'s own "our versions 53/55/59"). The book's local
   archive is fresh **today**, our **v64** (`bab61537.meta.json`:
   `teamBVersion: 64`, `completedAt: 2026-08-07T11:31:55Z` — the "Eir 4"
   ship-battery leg `HANDOVER.md:48-49` names explicitly). Ouroboros's
   build-queue timing is **already established as opponent-perturbable** by
   the book's own drumlin/atoll rows (§1: "aim-POLICY not a fixed
   coordinate" — builder-death timing shifts the landing tile/round). Our
   bot changed enormously between v53-59 and v64 (pieces C/D, Eir 3/4) —
   easily enough to shift when *our* builders die to Ouroboros fire, exactly
   the perturbation input the book documented. Independent corroboration:
   `HANDOVER.md:80-82` — `ouroboros_probe` (built from session-12's exact
   numbers) was already measured **"gentler than wild (4/8 vs their
   14/15) — verdicts understate real pressure"**, i.e. flagged stale by a
   fully independent battery before this adjudication even started.
4. **Bonus finding, a real bug**: the book's meander "1st CORE-THREAT" pick,
   `r6@(12,6)`, isn't actually reachable by a gunner. `(12,6)` has
   `fp_dsq=16`, clearing `sentinel_threat` (r²≤32) but **failing
   `gunner_threat`** (r²≤13) — and Ouroboros is confirmed gunner-only (book
   §1). The book's §8 method note says it scanned with
   `sentinel_threat/gunner_threat`; the broader set leaked into this one row.
   Corrected first true `gunner_threat` tile: `r46@(13,8)`, `fp_dsq=5`.
   Eider's `r50@(16,10)` pick has no such bug — confirmed `gunner_threat=True`
   directly.

Figures below come from re-decoding the exact files the book cites
(`bab61537-2315-4121-9286-d9447197afc2_game_1/_2.replay26`) with `decode.py`,
cross-checked against `siege_geometry.py`'s BFS margin model — which
reproduces the book's own stated margins exactly (r4@(13,6)→1, r6@(12,6)→3,
r12@(12,9)→6, r50@(16,10)→48) before the correction below is applied.

## Corrected constants — Ouroboros eider + meander

dsq is always squared distance from the tile to the nearest tile of **our**
2×2 core footprint (never Ouroboros's own core).

| map | role | round | tile | dsq→our core | Ouroboros ver | our ver | source |
|---|---|---|---|---|---|---|---|
| eider | home picket (station 0, NOT core-threatening) | r12 | (12,9) | 49 | v8 | v64 | `bab61537` g1, today |
| eider | **core-threat creep** (`gunner_threat=True`, confirmed) | r50 | (16,10) | 9 | v8 | v64 | `bab61537` g1, today |
| eider | *retired* old-sample station-0 | r32 | (14,10) | 25 | v8 | v53-59 | `ouroboros_probe` prov. (match 89114461 family) |
| meander | home picket (station 0, NOT core-threatening) | r4 | (13,6) | 17 | v8 | v64 | `bab61537` g2, today |
| meander | book's stated "core-threat" — **wrong, sentinel-only reach** | r6 | (12,6) | 16 | v8 | v64 | denial-book §1 (needs correction) |
| meander | **corrected core-threat creep** (`gunner_threat=True`) | r46 | (13,8) | 5 | v8 | v64 | `bab61537` g2, today (this pass) |
| meander | *retired* old-sample station-0 | r6 | (10,7) | 10 | v8 | v53-59 | session-12 / `ouroboros_probe` |

Note: tile `(10,7)`/dsq10 (session-12's meander number) exists in today's
replay too — but as a later, non-aligned, non-threatening addition first
built r104, not station 0. Same lattice point, different role across eras —
the clearest single illustration of the perturbation mechanism.

## GO / NO-GO for hardcoding into Loki denial

- **Eider `r50@(16,10)`, dsq9, margin 48 — GO.** Version-pin to Ouroboros
  v8 / our v64+; re-verify after any ship that measurably changes
  early-game builder survival (piece D-class changes) — that's the
  demonstrated perturbation input, not a calendar deadline.
- **Meander `r46@(13,8)`, dsq5, margin 45 — GO, with a doc fix.** Same
  version-pin/re-verify condition. File the correction against
  `denial-book-2026-08-07.md` §1's meander row (`r6@(12,6)` → `r46@(13,8)`) —
  its margin-3 "genuinely contested" call was an artifact of the wrong test.
- **Both maps' literal home-picket tiles (`(12,9)`, `(13,6)`) — NO-GO,
  regardless of source.** Confirmed non-core-threatening
  (`gunner_threat=False`); denying them doesn't stop the siege, per the
  book's own §0.5 reframe.
- **Session-12/`ouroboros_probe`'s original eider/meander numbers
  (`r32@(14,10)`, `r6@(10,7)`) — RETIRE.** Stale (our v53-59 era), not
  reproduced against current v64 code, independently flagged understrength
  (`ouroboros_probe` 4/8 vs wild 14/15, `HANDOVER.md:80-82`). Do not
  hand-code them or use them to gate future build verdicts.

**Single-sample caveat, honestly stated:** both corrected core-threat tiles
are n=1 (one replay each, today's era) — same standard the book itself
already flagged as its weakest point for these two maps. The large margins
(45, 48) make exact-tile precision less load-bearing than on a tight map, but
it hasn't been confirmed a second time the way drumlin/atoll were (2
independent series, tile drift ≤2 tiles, round drift 0). **What would settle
it further:** one more eider and one more meander game against our current
code, ideally a different match than `bab61537` — ordinary output of the
unrated portfolio sweep already running per `HANDOVER.md`'s "continue the
sweep" instruction, so no dedicated download budget is needed; just re-run
this file's method against the next arrivals in `replay_archive/`.
