---
tactic: Pull the forward worker out when something else can do its job, or when the job has become impossible — never because it is in danger
source: https://raw.githubusercontent.com/kant2002/steamhammer/master/Steamhammer/Source/ScoutManager.cpp
origin: Steamhammer (Jay Scott), Brood War AI — `ScoutManager::releaseScoutEarly`
evidence: documented
transfers: yes
---

## WHAT IT IS

Steamhammer's forward unit is **a worker in the enemy base** — the closest
structural analogue to our raiding builder in any league this library has swept.
Its *release* decision (as distinct from its flee decision) is not a survival
test at all. The function is commented with its own doctrine:

> ```
> // Should we release the worker scout early?
> // Check for nearby friendly units that can keep watch, or for nearby enemy static defense
> // that indicates we won't be able to see anything more this early in the game.
> // If we see enemy units, we probably want to keep an eye on them until our combat units arrive.
> ```

**Referent check.** "the worker scout" is `_workerScout`, the single worker sent
into the enemy base; "release" means hand it back to the worker manager for
mining. The three clauses in the comment are the three branches of the function
body, in order, and the call site says the same thing in one line:

> ```
> // Release the worker if it can no longer help: We have combat units to keep watch.
> ```

Two guard clauses precede the test and both are about *work done*, not danger:

* `// We're still close to where we started from.` — returns false inside
  `24 * 32` pixels of our own front. **A unit that has not yet arrived cannot be
  released.**
* If no enemy unit type has been seen beyond the starting set, it returns false —
  **the errand is not finished, so it stays.**

The positive test is a proximity search for either a friendly non-worker combat
unit (**relief has arrived**) or a completed enemy Bunker/Photon Cannon
(**static defence makes further forward work impossible**).

## WHY IT MIGHT TRANSFER — and it is the only framing on this list that survives `PLAY_DEFENCE: never`

Every other withdrawal doctrine in the sweep is framed as preservation. This one
is framed as **allocation**: the unit leaves because its forward output has gone
to zero, either because someone else is producing it or because the tile can no
longer produce it. That is a reason to move a unit that our programme accepts.

Both clauses are directly expressible:

* **Relief.** A friendly gunner/sentinel already standing forward and covering the
  area is our "combat unit keeping watch". A raider whose remaining errand is
  covered by a turret we already built is producing nothing.
* **Impossible.** `get_attackable_tiles_from(position, direction, turret_type)`
  and `can_fire_from(...)` let us compute, from *outside*, whether an enemy
  turret's pattern covers the tiles we still need to act on. If every remaining
  build target is inside a live enemy turret's pattern, the errand is the
  Photon Cannon case: **leave, because the work cannot be done, not because we
  might die.**

Note the asymmetry Steamhammer does not have and we do: **an enemy builder bot
cannot attack our builder at all** (builder attacks target buildings only). Our
"static defence" set is exactly the enemy turrets, which are **immobile** and
**ammo-gated with no passive ammo income** — so the impossible-set is small,
fixed and cheap to compute.

## WHAT WOULD KILL IT

* If we never build forward turrets, the *relief* clause has no object and only
  the *impossible* clause is live.
* `is_in_vision(pos)` returns False rather than raising, but `get_tile_env` and
  friends **raise off-map and out of vision**, and an escaping exception
  permanently destroys the unit. Any implementation of the impossible-test must
  be built from remembered turret sightings plus `is_in_vision`, not from
  speculative terrain queries.
* Our cost scale is one global additive factor, so a released builder that gets
  destroyed **refunds its +20%** — the accounting for "release vs let it die"
  is not the same as Brood War's.

## BUILDER HOOK

Smallest test: add **one** disjunct to whatever currently ends a raid errand —
every remaining build target on the raider's list is inside a known enemy
turret's attack pattern — and remove the round-count give-up in the same arm. That
swaps a clock for a completion test without adding a mode.
