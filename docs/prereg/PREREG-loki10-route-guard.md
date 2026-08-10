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

---

## ADDENDUM — PRE-LEG, NO LEG HAS FIRED. Three bars change and one is a programme problem.

Research's pre-leg check on the **v102** population (125 our-side ladder games,
not the ~75 either of us estimated). Written before any leg exists.

### 1. THE MOTIVATION NUMBERS IN THIS FILE ARE EIR NUMBERS. Superseded.
**Do not quote 13.2% or 11.1% for v102.** They are Eir figures on an Eir
denominator, and v102 moves in **opposite directions depending on the
denominator**: **38% HIGHER per game** (0.424 vs 0.307) but **2.7x LOWER as a
share of turret builds** (1.95% vs 5.36%), because **v102 builds 3.8x more
turrets and barriers** (21.70/game vs 5.72).
**Quote 0.42 builds/game and 53 events.** Sixth denominator-as-view catch
tonight, and it is on my own motivating figure.

### 2. THE n=0 TRAP DOES NOT APPLY — the leg can fire.
53 events across 125 games; a 60-game control arm expects **25.4**, P(zero)
~7e-8. The did-it-fire bar stands as written.

### 3. BUT THE VERDICT CHANNEL IS STRUCTURALLY CLOSED, AND THAT IS A PROGRAMME
### PROBLEM RATHER THAN A DESIGN FLAW.
**Only 8 of 115 attributed v102 games reach round 1000. 93.0% end in
`core_destroyed`**, against 73.3% for every other version — independently
reproduced from a different filter and a pinned snapshot (93.3% vs the Eir era's
67.6%). **The motivating 11.1% mass figure is round-1000-only, so the instrument
that produced it is structurally unavailable for v102**, and **titanium decides
roughly one v102 game in fourteen.**

**⇒ THE VERY PROPERTY THAT MAKES LOKI-8 GOOD — it ends games decisively — CLOSES
THE CHANNEL AN ECONOMIC FIX COULD SHOW UP IN.**

So `core_kill_share` **cannot** move on this treatment at any feasible n, and
**PROGRAMME.md is explicit that a mechanism metric never substitutes for the
currency.** The honest consequence, stated now rather than discovered in a null:

* **THIS PLANK CANNOT BE BANKED AS A PROGRAMME GAIN.** It is a CORRECTNESS FIX —
  we spend our own titanium corking our own lines — and it will be reported as
  one. **No currency claim will be made for it, in either direction.**
* **The bar is the MECHANISM COUNTER ALONE: control ~25 events, treatment 0.**
* **A flat `core_kill_share` is NOT evidence against the plank** and must not be
  written up as a null. The channel is closed; a closed channel reports nothing.
* The leg's remaining value is a **safety check** — that the refusal costs
  nothing measurable — which is cheap and worth having.

### 4. AND THE REFUSAL COVERS ONLY PART OF THE MECHANISM.
The reverse case — **a conveyor built LATER, aimed at an existing friendly
turret** — is **23 events against this treatment's 53 in v102, so the refusal
reaches ~70%**; pooled across the archive it is **607 vs 658, barely 52%**.
**This treatment cannot falsify "our own turrets cork our lines". It can only
falsify "we build turrets onto lines."** Stated so a null is not over-read.

### 5. VARIANCE, for whoever reads the arm.
**76.0% of v102 games contain ZERO such builds** (95 of 125); dispersion index
2.01, twice Poisson. **Any per-game outcome metric is dominated by games where
the treatment was inert.** Report the event counter, not a per-game average.

---

## ADDENDUM 2 — PRE-LEG, still no leg fired. THE PLANK COVERS 35% OF ITS CLASS, NOT 70%.

**Corrected coverage.** The 70% I recorded in addendum 1 was split by **EVENT
COUNT**. By **TITANIUM it inverts**: the **35 reverse pairs** — a conveyor built
LATER and aimed at an EXISTING friendly turret — carry **66 Ti/game**, against
the **64 forward pairs' 36 Ti/game** that this plank actually catches.
**So LOKI-10 as built reaches ~35% of the self-block mass, not 70%.** Ninth
denominator-as-view correction of the session and it is on my own plank's
coverage claim.

**Class-4 (self-blocking) costed over 210 v102 games: 102 Ti/game defect, fix
cost 0, return infinite, 35/210 games affected, 593 Ti per affected game.**

### THE MIRROR PREDICATE — SPECIFIED, NOT BUILT
Symmetric to `_feeds_tile`: **before building a CONVEYOR with facing `f` on tile
`T`, refuse if the tile `T.add(f)` holds a friendly TURRET or BARRIER.** Same
four-neighbour cost class, same pure-refusal shape, and it needs no new state.

**I am NOT building it tonight and the reason is on the record rather than
implied:** the conveyor build path is in `eco.py`, which I have not read, and
this session has produced **four instruments broken IN THE FIXING — none of them
by carelessness.** A symmetric-looking change into an unread file at 03:30 is
exactly that pattern. **Whoever picks it up: build both predicates, re-run the
gate, and the plank goes from a third of its class to all of it.**

### AND THE 421 Ti CALIBRATION POINT DOES NOT APPLY HERE
It measures **build spend on excess forward turrets**; this plank measures
**delivery loss from turrets corking routes**. Different quantities. The
comparable figure is **593 Ti/affected game**, and its similarity to 421 is
**coincidence**. Recorded because an instruction to reconcile the two would have
propagated a category error into a plank.
