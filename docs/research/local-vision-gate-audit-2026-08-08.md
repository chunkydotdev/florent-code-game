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

Applied to `hive_freeze`, either guard alone kills the positional accident: a
distance guard makes the arm depend on the board rather than on where a builder
wandered; monotonicity makes a "no gun visible" reading unable to un-arm or arm
a permanent state.

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
