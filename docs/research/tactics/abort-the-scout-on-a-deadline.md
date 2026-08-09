---
tactic: Put a stop-loss deadline on the reconnaissance itself, and return the scout to economic work
source: https://battlecode.org/assets/files/postmortem-2020-confused.pdf
origin: Battlecode 2020, confused (2nd in the high school bracket, 6th on the scrimmage server)
evidence: documented
transfers: yes
---

## WHAT IT IS

confused's rush was carried by their **first spawned miner**, i.e. an economic unit
seconded to reconnaissance. The rule that made that affordable was a hard deadline on the
reconnaissance, after which the unit **stops scouting and rejoins the economy**:

> *"If after 180 rounds it still doesn't see the enemy HQ, it gives up on the rush and
> joins the rest of the miners and do normal miner stuff."*

**Referent check.** "it" is the rusher miner — the surrounding text reads *"We assign our
first spawned miner as the "rusher", which will do the following things"* followed by a
numbered list of which this is item 5. The deadline is on the *search*, not on the attack.

The same list carries a second, complementary rule — a **reactive counter-build at the
forward plant**, triggered by seeing the counter-unit's producer rather than by a clock:

> *"If the design school has already been built and it spots a drone or a drone factory, it
> builds a net gun."*

And, separately, the exchange logic that made their commitment unconditional once it was
running (this half was already recorded in sweep 14 as the "rush cost" price gate):

> *"We also noticed that in a battle of rush vs. rush, it was mostly better to not defend,
> since defense meant that you couldn't spend more on offense."*

## WHY IT MIGHT TRANSFER

This is the missing safety rail on every trigger in this sweep. Each of them says *commit
when you observe X*. None of them says what to do when **X is never observed** — and in our
ruleset the cost of waiting for X is paid in the most expensive currency we have: builder
rounds, which are also build rounds.

Our numbers make the deadline concrete rather than arbitrary:

- A builder that spends 180 of our 1000 rounds searching has forgone up to 180 builds. Our
  own opening spends **5 builder bots and 3 harvesters by r50** (corpus medians), so one
  builder is ~20% of the early workforce.
- Our engine has no fog-of-war memory to fall back on: `is_in_vision(pos)` is per-unit and
  per-round. A search that fails leaves nothing behind unless the searcher wrote to a store
  slot.
- The deadline is trivially cheap: `ct.get_current_round()` is free, and the builder's
  fallback behaviour (build/harvest) already exists.

The design principle worth taking is narrower than "add a timeout": **the abort returns the
unit to a productive role rather than to idle or to a suicide attack.** confused's rusher
becomes a miner. Our equivalent is a builder that has been walking toward the enemy half and
now turns around and builds conveyors on the way home — a route it is already on.

## WHAT WOULD KILL IT

- **180 is their number, not ours.** Their map scale and 3000-round game are not ours; the
  transferable object is *a deadline exists and the abort is to economy*, not the constant.
  Our own tape says we go 277-148 before r200 and 164-363 after, so a deadline that expires
  after r200 is expiring into the part of the game we lose.
- **It is a stop-loss, not a trigger.** It cannot make a commitment happen; it only bounds
  the cost of one that never became possible. Filing it as a tactic on its own risks it
  being mistaken for the answer to (A). It is the answer to *"what if (A) never fires"*.
- **Our builders cannot fight on the way home.** A builder attack is 2 Ti for 2 dmg and
  **cannot target enemy builder bots at all**, so an aborting scout has no consolation
  damage available — the abort really must be to economy.

## BUILDER HOOK

If any Loki iteration ships a builder whose job is to observe the enemy half, give it a
round-number stop-loss and a named fallback role, and **log which branch it took**. The
per-game split (fired / expired) is the cheapest possible instrument for whether the
trigger in `the-trigger-rides-on-a-unit-already-going-there.md` is live at all on our map
pool — and it costs one integer in the replay's `print()` output.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2020-confused.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
