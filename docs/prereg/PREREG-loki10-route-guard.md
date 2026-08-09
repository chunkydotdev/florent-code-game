# PREREG — LOKI-10, don't build onto our own conveyor route

**Committed BEFORE the build and before any leg.** Line `loki`; comparator
**LOKI-8 = `bots/_v124loki8`** (previous line iteration, per PROGRAMME.md).

## The defect

Research's binding-tile cut (all 8,519 replays, 1,798,862 blocked
harvester-rounds): **85.2% of our binding tiles have no directed path to our
core**, and **13.2% of them are a conveyor line pointing at a TURRET OR
BARRIER**. We build our own emplacements onto the tile our own line delivers
into. Cost **11.1%** of the blockage — **more than the enemy inflicts (6.1%)**.

Verified in this tree: the counterbattery build-site filter
(`_v124loki8/main.py:556-566`) excludes heal seats and nothing else. **No build
path anywhere checks whether a friendly conveyor points into the candidate
tile.** The defect is present by construction.

## The treatment — a refusal, not a mechanism

Before building a turret or barrier on tile `T`, reject `T` if any orthogonally
adjacent friendly **conveyor** faces `T`. Four `get_direction` reads, inside the
existing `_cpu_exhausted` guard. **Nothing new is built, nothing is re-sited,
nothing moves** — a candidate site is removed from consideration. This is the
only shape that has ever gained on this line.

## Bars, stated before the leg

* **DID-IT-FIRE (mechanism, NOT the verdict):** count of our own turret/barrier
  builds landing on a tile a friendly conveyor faces. LOKI-8 control arm > 0;
  **LOKI-10 must be 0.** Decoded from the leg's own replays. A guard that never
  had an opportunity to fire is not evidence — **if the control arm is also 0 on
  this fixture, the leg answered nothing** and must be re-run on a fixture where
  it occurs.
* **VERDICT (PRIMARY_CURRENCY): `core_kill_share` vs LOKI-8**, paired, with its
  interval. **SECONDARY:** titanium delivered (`titanium_collected`), which is
  the quantity the defect actually damages — reported, and NOT substituted for
  the currency.
* **FIXTURE, stated because tonight established it matters as much as
  population:** this is an ECONOMIC defect. `razer_probe` does not make it
  arena-testable. The arena can show the guard FIRES; only the ladder can price
  it. Expect a mechanism result locally and a currency result slowly.

## Falsifier

**Guard fires and `core_kill_share` does not move -> LABELLED NULL**, and I will
write the word. **Guard does not fire -> the leg answered nothing** (D7 shape),
not evidence against the idea. **Delivered titanium rises while
`core_kill_share` is flat -> an OFF-PREDICTION result, labelled, not banked** —
PROGRAMME is explicit that a secondary-only headline is not a pass.

## What this does NOT attempt

The other 74% of the mass — unterminated lines 33.4%, destroyed segments 23.9%,
facing coherence 15.8% — is larger and needs real routing logic. **This is the
smallest shippable slice**, chosen because it is a pure refusal and because it
is the one item where **we cost ourselves more than the enemy costs us.**
