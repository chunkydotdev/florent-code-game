# The communication store: four assumptions, now measured

**Research arm, session 23, 2026-08-09.** Two local deterministic probes,
`--tle 0`, seed 1, `maps/fjordgate.map26`, idle opponent. Probe sources in the s23
scratchpad, **not in `bots/`**. Zero arena, zero downloads, zero bot edits.
**Version tag:** live **v90** = `bots/_v104latch`, ladder 1568 @ 505, #30.

Commissioned by tactics sweep 7 (topic 7), which flagged that **our bot depends on
last-writer-wins and that this is an assumption, not a measured fact**, and that
several slots depend on it.

---

## 0. The four answers

| # | question | answer |
|---|---|---|
| Q1 | Is a write visible in the same turn? | **No — buffered, as documented.** `read_store` after `write_store` returns the OLD value. |
| Q2 | Two units write the same slot in one round — who wins? | **LAST WRITER WINS.** |
| Q3 | Does the read-increment-write ticket idiom survive a collision? | **NO. It is broken, and silently.** |
| Q4 | What values does a slot accept? | **Unsigned 32-bit: `[0, 2³²−1]`. Negatives RAISE `OverflowError`.** |

---

## 1. Q1/Q2 — buffering and last-writer-wins

Five builders (ids 3-7) each wrote their own id to slot 15 in round 30, then read
it back in round 31:

```
[r30] id=3: slot15 before write=0  after write=0  -> buffered (not visible)
[r30] id=4: slot15 before write=0  after write=0  -> buffered
[r30] id=5..7: same
[r31] CORE and all five builders read: slot15 = 7      <- the LAST writer
```

**Confirmed on both counts.** And an independent witness ran in the same match:
slot 12 accumulated `read*10 + id%10`. Under same-turn visibility it would have
reached `34567`; under buffering every writer reads 0 and writes its own digit, so
the final value should be the last writer's digit alone.

```
slot12 = 7          (not 34567)
```

**So an accumulate-across-units idiom does not merely lose precision — it collapses
to a single writer's contribution.**

## 2. Q3 — the ticket bug, demonstrated rather than argued

Sweep 7 flagged this as a latent single-point failure. It reproduces exactly:

```
[r30] id=3: read ticket=0, wrote 1  -> believes it is unit #0
[r30] id=4: read ticket=0, wrote 1  -> believes it is unit #0
[r30] id=5: read ticket=0, wrote 1  -> believes it is unit #0
[r30] id=6: read ticket=0, wrote 1  -> believes it is unit #0
[r30] id=7: read ticket=0, wrote 1  -> believes it is unit #0
[r31] slot14 = 1                    <- five writers, counter advanced by ONE
```

**All five units believe they are unit #0, and there is no error of any kind.**

Our `SLOT_ROLE_N` (`main.py:902`, `write_store(SLOT_ROLE_N, n + 1)`) is this idiom.
**It is currently safe only because the core spawns at most one builder bot per
turn**, so at most one unit runs its first-turn init in any round. That is a rule
of the game holding up a bot invariant by luck, not by design.

**What would break it**, all plausible: a launcher-thrown bot re-initialising, any
change that lets two units take a ticket in the same round, a second spawner, or
turrets taking tickets. The failure is silent role collapse — two units doing the
same job and one job undone.

**Sweep 7's fix is two lines and provably collision-free: make the CORE own the
counter** (it increments on a successful `spawn_builder()`, the newborn reads it on
its first turn). Single writer, and it survives any future change to who
initialises when.

## 3. Q4 — the store is unsigned 32-bit, and negatives are a crash hazard

A value ladder, one write per round:

```
0            ACCEPTED        2**31-1  ACCEPTED
1            ACCEPTED        2**31    ACCEPTED
-1           RAISED OverflowError     2**32-1  ACCEPTED
-2           RAISED OverflowError     2**32    RAISED OverflowError
2**15..2**16 ACCEPTED        2**63-1 and above  RAISED OverflowError
```

**Range is exactly `[0, 2**32 - 1]`.**

Two consequences:

**1. Good news for packing.** **32 usable bits per slot, 16 slots = 512 bits
total.** That is *wider* than Battlecode's own shared arrays, which have run 10-16
bits per entry across the years sweep 7 surveyed — so every packing scheme in that
sweep fits comfortably, and the round-stamp-plus-position layout it recommends is
cheap here.

**2. A real crash hazard for future code.** `write_store` with a negative value
raises `OverflowError`, and **an uncaught exception permanently destroys that unit
for the rest of the match.** Any computed store value that can go negative — a
difference, a decrement, a countdown — is a unit-kill waiting to happen.

### Audit of the live bot: clean

I checked every `write_store` call site in `bots/_v104latch/main.py` (39 of them).
**All are non-negative by construction**: `pack_pos(...)` of an in-bounds position,
integer literals, `get_current_round()` or `round + 1`, `read_store(...) + 1`
counters, and `income_ti * K_HEAL_RATE_PCT // 100`. **No live negative-write
hazard.** Recording the audit rather than only the rule, so the next person knows
it was checked and when.

*Note the monotone counters (`SLOT_HOME_GUN`, `SLOT_HARVESTERS`, `SLOT_DROPPED`)
are bounded by build counts over 1000 rounds and come nowhere near 2³², so overflow
is not a concern from that direction either.*

## 4. Limits

- One map, one seed. These are engine rules and should not be map-dependent, but
  they were not replicated across maps.
- Q2's "last writer" is last **in unit execution order**, which the probe observed
  as ascending entity id in this match. **I did not test whether execution order is
  guaranteed to be id-ascending**, and a design that depends on *which* writer wins
  (rather than merely that one does) should not rest on this.
- The collision test used builder bots only; turrets and the core were not tested
  as competing writers.
- Q4's ladder is powers of two plus neighbours; the exact bound is inferred from
  `2**32-1` accepted and `2**32` raised, which is unambiguous, but intermediate
  values were not swept.
