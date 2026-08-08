# Opponent constants under v80: the re-seeding block does not hold, and the Lunds fixture can proceed

**Research arm, session 20, 2026-08-09 03:0x CEST.** Live **v80 "Eir 9b"**,
window n=9/20, ladder 1588 @ 450 #28. **Zero downloads** — 125 archived replays
across Lunds/KCM/Ouroboros, plus `match list` metadata. Queue item 3.

Answers the block I myself placed on the builder's Lunds fixture at ~22:4x:
*"deterministic opponents re-seed on OUR version, and we went v84→v86→v80, so
constants extracted under v83 are suspect."*

**That block is not supported by the data, and I am lifting it.**

---

## 1. The tooling trap that had to be cleared first

`fcode match info --json` returns the **opponent's version as `null`** on every
row — a known defect already in tooling.md. Joining on it silently gives you
"their version: None" for every match and makes the opponent look static.

**`match list` carries both versions.** Every result below is joined from
`match list`, not `match info`.

## 2. The experiment is cleaner than expected: their version was already fixed

```
Lunds Stallions   their v44 throughout   seen 07:26 .. 21:35 today
Ouroboros         their v8  throughout   seen 06:16 .. 20:56
Kings College     their v1 -> v8         v1: 06:56..10:36   v8: 13:17..20:47
```

**Lunds and Ouroboros held one version all day while we shipped v74→v86.** That
is exactly the experiment the re-seeding claim needs: their code fixed, ours
varying.

## 3. Result: opponent opening constants are INVARIANT to our version

Permutation test on between-our-version spread, their version held fixed,
5,000 shuffles per test:

```
Lunds Stallions (their v44, n=40)
  launcher    p=0.247   medians by our v74..v81: 1, 1, 1, 1, 1, 1
  gunner      p=0.385   16, 26, 12, 8, 12.5, 16
  harvester   p=0.457   9, 10, 8.5, 8, 10, 9
  conveyor    p=0.466   11, 12, 10.5, 10, 12, 11
  sentinel    p=0.714

Ouroboros (their v8, n=35)
  gunner      p=0.300   21, 9, 23, 29, 21, 23
  harvester   p=0.259   4, 7, 5, 5, 4, 4
  conveyor    p=0.683   3, 6, 3, 3, 3.5, 3
```

Bonferroni over 10 tests requires p < 0.005. **Nothing comes close.**

The strongest single result is not a null at all: **Lunds builds its launcher on
round 1 in 40 of 40 games across six of our versions — zero variance.** That is
an exact invariant, not a failure to detect a difference.

## 4. The KCM "signal" was their ship, not ours

The first cut of this analysis found KCM opening dramatically faster under our
v80 — harvester r2 vs r7, surviving a map-mix control on 5 of 6 overlapping
maps. **It is entirely explained by KCM shipping v1→v8 at midday:**

```
KCM v1  (our v74-76):  harvester r8, conveyor r8, launcher in 14/15 games
KCM v8  (our v79-82):  harvester r3, conveyor r7, launcher in  9/20 games
```

Our version has nothing to do with it. **This is the finding restated as a
warning: "opponent behaviour changed across our versions" is almost always
"the opponent shipped", and `match info` cannot see that because it nulls their
version.**

## 5. What this does to the re-seeding rule — a re-scoping, not a deletion

The protocol rule says deterministic opponents re-seed on our version and their
constants need re-extraction after our ships. **For opening constants that is
mechanically implausible and empirically unsupported**: a build on round 1
happens before either side has seen the other, so our code cannot be an input to
it.

Re-scoped, the rule survives in a narrower and more useful form:

> **Constants describing behaviour BEFORE first contact cannot depend on our
> version — only on theirs. Constants describing behaviour AFTER contact
> (denial tiles, target selection, insertion targets) can.**
> **The staleness axis that actually matters is THEIR ship, not ours.**

## 6. Consequence: the Lunds fixture is unblocked

The fixture targets Lunds's **absolutely-oriented r3 launcher insertion**. Split
into its two halves:

- **The launcher's existence and build round: VERIFIED STABLE.** r1, 40/40,
  across our v74–v81, with Lunds on v44 the whole time. Nothing about our
  v84→v86→v80 churn touches it.
- **The insertion tile itself: still unverified.** A throw is a post-contact
  event and is exactly the class §5 says can depend on us. It is also not
  extractable from `replay_census.py`, which reports builds, not launches.

**So the block is lifted on the half that the fixture is built around, and
narrowed to the half that a fixture would have to measure anyway.** Building it
no longer risks discovering that the launcher moved — it cannot have.

**The real watch item is a Lunds ship.** They have been v44 all day; if that
number changes, every Lunds constant is stale at once, and `match list` is
where to see it.

## 7. Caveats

- **Power.** 5–10 games per version cell over 6 cells. This test would not
  detect a modest shift; it is evidence against a *large* dependence, not proof
  of none. The launcher invariant (zero variance, 40/40) is the only result here
  strong enough to stand alone.
- **Rule 6 applied to myself:** the treatment *was* in the pool — v74→v81 spans
  the E-family bundle, the hive fix and PIECE MAG, so our versions genuinely
  differed. This is not a null from an empty bucket.
- Sentinel cells for Lunds are sparse and erratic (medians 16.5 to 228.5) —
  that is games where no sentinel was built until very late, not a constant.
- KCM v8's launcher rate (9/20) is not a timing constant but a **frequency**;
  whether that is map-driven is untested.
