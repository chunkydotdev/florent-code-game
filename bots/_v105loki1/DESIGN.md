# LOKI-1 (v105) — the collar

**Doctrine in one line: don't break the door, jam the lock.**

## What raises the kill rate

A builder heals +4 HP for 1 Ti from any of the **8 tiles orthogonally adjacent
to the enemy 2×2 footprint** — 0.25 Ti/HP against ~0.56 for any attacker. Net HP
to kill a Core is a stable 500–512 but the raw hits landed range 28 → 1206
(14 decoded games): the 43× spread *is* the defender's heal line. Those same 8
tiles are also the only tiles a conveyor can deliver into a Core from, and 8 of
its 12 spawn tiles. One chokepoint for healing, income and reinforcement.

A **barrier is 3 Ti / 30 HP** and bot-impassable. Breaking one costs 15 pecks at
2 Ti = **30 Ti, a 10:1 exchange**, and every round spent pecking is a round not
spent healing. A raider on one of the **4 diagonal ring tiles** is orthogonally
adjacent to exactly the two seats flanking it, so four corner raiders seal all
eight. Sealed, every point of damage we land is permanent.

Damage then comes from a **forward Sentinel** — forced, not preferred: barriers
block LOS so a Gunner ray would die on our own collar, while the Sentinel line
ignores obstacles and shoots *through* it. 18 dmg / 2-round reload = 6 HP/round
against a defender who can no longer repair.

## Re-aim after the mid-build evidence

Built first against "remove the r180 cutoff, target r200-300". That premise was
refuted mid-build (ablation 49.4%, n=180; 11,895 throws show median raider life
collapsing 43 → 6 rounds at r150; only 2.34% of r200+ throws ever land one
attack). What survived: of 528 raiders that *did* attack, 25 produced half of
all 40,114 attacks and **319 were on the winning team**. The scarce resource is
**survival at the destination**.

So the two are now separated (`raid.py`, `_raid_open`):

- **Cold insertion** — a fresh body walking at intact defences — is open only
  until `LOKI_COLD_INSERT_RND = 150`.
- **Foothold reinforcement** — any round a raider is still acting at the ring,
  published as a heartbeat in `SLOT_RAID_LIVE` — has **no cutoff**. That is
  exactly the state the winning 319 were in.

## Survival package (the answer to defender-exile)

Defensive disposal is ~70% of all launcher activity in the field, so a lone
raider beside a defended Core is food. Six answers, all in `raid.py`:

1. **Value outlives the body** — the first action after landing is a barrier;
   an exile does not un-build it.
2. **The collar is also cover** — barriers block LOS, so Gunner rays cannot
   reach a raider standing behind its own wall.
3. **Numbers** — 12 stations, deterministically preassigned by raid slot, so
   raiders arrive spread instead of one-at-a-time (the incumbent staged one).
4. **Site choice** — a station within d²≤2 of a visible enemy Launcher is
   scored down by `LOKI_EXILE_PENALTY`; a raider that detects a teleport bans
   that station and re-enters elsewhere instead of walking back into the pickup.
5. **Buddy heal** — +4 HP/1 Ti onto an adjacent wounded raider cancels a
   Gunner's 3.5 HP/round.
6. **A building, not a body** — the forward Sentinel keeps firing after every
   raider is dead.

The raider **never waits** for a launcher (the incumbent's `launchwait` role is
gone): it walks, and the ferry throws it forward only if the walk happens to
cross the pickup ring.

## Kept vs rebuilt

**Ported verbatim from `_v103split` (`eco.py`)** — harvester bootstrap, trunk
chain planner, pave trail, BFS nav, heal-seat reservation, siphon hygiene, chain
medic, multi-healer convergence; `doctrine.py` copied whole. **Rebuilt** — roles,
Core spawn/ammo policy, home defence, the whole raid layer. **Dropped** — every
per-map special case (hive/snowflake/nordkap/atoll), the siege planner, the
`launchwait` role and its four gates.

`raid.py` is ablatable: delete its four call sites in `main.py` and what remains
is a plain economy bot.

## Known weak points

- The full 4-corner collar is a *model*, never observed holding. Measured games
  end with 1–3 barriers alive, not 8.
- Cold-insert seats are few before r150 (seat 0, then seat 3 after the harvester
  shell); "arriving in numbers" depends on a surplus bank that may come late.
- `LOKI_SURPLUS_TI`/`LOKI_RICH_TI` population lifts are unmeasured guesses.
- Barriers are +1% team cost scale each; 8 of them is +8% on everything after.
