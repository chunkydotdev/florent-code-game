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

## ⛔ CAVEAT APPENDED 2026-08-11 (s32, research arm) — THIS FILE REASONS ON A RETIRED PROGRAMME FIELD
This file cites **`PLAY_DEFENCE: never`**. That field was amended the same day and now reads
**`PLAY_DEFENCE: not_at_the_kill_s_expense`** with **`DEFENCE_ADMISSION_BAR: kill_round_non_regression`**
(`PROGRAMME.md:19-20`). **A defensive tactic is now ADMISSIBLE IFF it does not slow the kill** — it carries a
kill-round non-regression bar beside its survival bar, and is off-programme only if MEDIAN KILL ROUND RISES.
**"Defensive, therefore off-programme" is no longer a valid closure reason.**
**Scope, unchanged:** this licenses surviving the **r150-250 window so our own kill lands** (median kill 174,
median death 187, core dies in 46.3% of games). It does **NOT** license surviving to r1000 —
**`R1000_IS_DEFEAT: yes` still governs.**
**WHAT THIS DOES AND DOES NOT DO TO THIS FILE:** Line 44's heading claims the relief/impossible
framing is chosen because "it is the only framing on this list that survives `PLAY_DEFENCE:
never`" — implying every other withdrawal framing in the sweep (survival-based ones) was
excluded by category. That exclusivity is void: a survival-based withdrawal framing is no
longer automatically off-programme, only conditionally admissible via the new bar. This does not
undercut the file's own BUILDER HOOK (add a completion-test disjunct, remove the round-count
give-up) — that recommendation was independently argued from allocation logic ("the unit leaves
because its forward output has gone to zero"), not from the exclusivity claim.
**STATUS:** RESTRICTION NARROWED — this is no longer necessarily "the only" admissible
withdrawal framing; other framings (e.g. survival-based) may now also be tested, subject to the
kill-round bar.
**NOT REOPENED BY THIS CAVEAT.** Voiding a closure reason does not revive the road; it returns it to the queue
for a live test. Under `docs/research/PROGRAMME-drift-watch-2026-08-09.md` D12 an archive-sourced closure cannot
retire a road, and this caveat cannot restore one.
