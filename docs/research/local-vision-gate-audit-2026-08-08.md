# The "team fact from local vision" defect class — audit and a sharper definition

Research arm, 2026-08-08 s19. Source: `bots/_v97e11/main.py` (LIVE v83, md5
56b9d178). Triggered by the builder's observation that three defects tonight
shared a root. **The class is real. It is also narrower than "team-level facts
inferred from local vision", and the file already contains the correct idiom —
which makes the fix cheaper than a new store-publish mechanism.**

## The sharper definition

33 `get_nearby_*` scan sites exist across 27 functions. Nearly all are fine:
reading local state to make a local decision is what the API is for. The defect
requires a **conjunction**:

> **A DURABLE decision (persisting beyond this round) gated on an UNGUARDED
> local-vision sample, where the caller's position is not constrained relative
> to the thing being sensed.**

Drop either conjunct and it stops being a bug.

## The four-way classification

| site | durable? | caller position guarded? | verdict |
|---|---|---|---|
| `hive_freeze` via `_live_home_gun` (:3222-3229 dispatch, freeze at the `_expand` head) | **YES — permanent for the match** | **NO** — `_expand` is the dispatch DEFAULT branch, so the caller is whoever fell through | **THE BUG** |
| `_c1b_supply` heal-line gate (PIECE E1b) | held across rounds via the claim | **NO** — helper may sit at `C1B_SUPPLY_HOME_DSQ`=64 while vision is r²=20, so it can be inside the band and structurally unable to see the heal seats | **SAME DEFECT, conservative direction** |
| `_sync_harvesters` | writes `SLOT_HARVESTERS` (durable) | **YES** — `if p.distance_squared(self.core) > 64: return`, **plus** a monotone floor (`if live > stored`) so a partial view can only ever RAISE the count | **CORRECT — this is the idiom** |
| `_core_shelled` | per-round only | vision-bounded, returns False out of vision | acceptable; failure is one round of conservatism |

## Why this matters for the fix

The builder's proposal was to publish team facts through the store (slot 5 is
verified free). That works, but `_sync_harvesters` shows the file already solves
this **without spending a slot**, using two cheap guards:

1. **Constrain the caller** — refuse to answer unless within a stated distance
   of the subject (`> 64: return`).
2. **Make partial views monotone** — a limited view may only move the estimate
   in the safe direction, never erase a better one.

Applied to `hive_freeze`, monotonicity would help — but **a distance guard would
NOT, and my first draft of this doc was wrong to say it would.** See the
correction below.

## CORRECTION (same session): for `hive_freeze` no position guard can work

Two facts, both verified at source after the builder corrected the latch claim:

1. **The freeze does not latch.** The block persists nothing — its only
   statement is `return`; `CB_OVER_HEAL_ON = True` (:800) routes the arm through
   `_live_home_gun`, a fresh per-unit scan recomputed every call. The
   "rest of the match" phrasing in three tape rows (including my own
   `hive-freeze-live-defect`) was quoted from a **stale comment** describing the
   pre-Piece-J form that read the monotone `SLOT_HOME_GUN` (4 increments, 0
   decrements — verified). The measured effect sizes stand; the mechanism
   description does not.
2. **The sensor is smaller than the question.** `HUNT_BAND_DSQ = 41` (≈6.4
   tiles) is the band `_live_home_gun` is asked about; builder vision is r²=20
   (≈4.47 tiles). **A unit standing exactly on the Core cannot see the outer
   band at all** — roughly half the band's radius-squared range is unobservable
   from the best possible position.

So this predicate is not merely position-*dependent*; it is **structurally
incapable of answering its own question from any position**. A distance guard
constrains where the caller stands, which cannot help when no standing point
covers the band. That makes `hive_freeze` a member of the second fix class, not
the first: it genuinely needs a **store-published arming signal** (slot 5 is
verified free), and the position-guard idiom is the wrong prescription here.

The four-way table above still holds for the other members; only the `hive_freeze`
prescription changes.

**Store-publish is still the right answer where the fact is genuinely global and
no single unit can ever be positioned to observe it** (the deny-silence target,
where the siphoned harvester may be 8-15 tiles from every builder we own — there
is no position guard that helps, because no eligible unit is ever near it).

## The item I own

`_c1b_supply`'s heal-line gate is mine, built this session, and it has the
defect. It fails conservative (a helper who cannot see healers refuses to leave
the line), so it is not urgent — but its measured effect (the kladde tax
recovering 70.0 → 75.0) was attributed to the RULE when part of it may be
attributable to WHERE THE HELPER HAPPENED TO STAND. That attribution is now
caveated; the plank is not withdrawn.

## What this does NOT establish

Whether any of these gates is costing measurable Elo. This is a code audit, not
a measurement — every claim above is about reachability and construction, and
the only measured member of the class is `hive_freeze` (arms vs opp_v63, silent
vs ouroboros_probe, tape row `hive-arm-positional`).
