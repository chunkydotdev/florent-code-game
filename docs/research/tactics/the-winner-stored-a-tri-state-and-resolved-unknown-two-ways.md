---
tactic: (A) THE ANSWER TO SUB-QUESTION (A) — the Battlecode 2023 WINNER kept UNKNOWN as a first-class third value, one char per tile, and shipped TWO readers that resolve UNKNOWN in opposite directions so each caller picks its own risk appetite
source: https://raw.githubusercontent.com/awesomelemonade/Battlecode2023/2e231f31a4622909b0dfd34a68c9b634dde1c803/src/finalBot/util/PassabilityCache.java
origin: "Producing Perfection" (Lawrence Chen, Jason Lee) — **Battlecode 2023 overall winner**, confirmed on https://battlecode.org/past.html: *"Winner: [Producing Perfection] Lawrence Chen, Jason Lee"*. Repo `awesomelemonade/Battlecode2023`, commit `2e231f31a4622909b0dfd34a68c9b634dde1c803`
evidence: documented
transfers: yes
---
WHAT IT IS — the winning bot's terrain memory is one flat 3600-char buffer, one char per
tile, holding a **three-valued** cell. Verbatim, `src/finalBot/util/PassabilityCache.java`
lines 41-47:

```java
    public static final char UNKNOWN = '\u0000';
    public static final char UNPASSABLE = '\u0001';
    public static final char PASSABLE = '\u0002';
    // we gotta save bytecodes - so we return int instead of enum
    public static char isPassable(MapLocation location) {
        return data.charAt(location.x * Constants.MAX_MAP_SIZE + location.y);
    }
```

**And it never collapses UNKNOWN at the storage layer — it collapses it at the READ, twice,
in opposite directions.** Lines 33-39:

```java
    public static boolean isPassableOrFalse(MapLocation location) {
        return isPassable(location) == PASSABLE;
    }

    public static boolean isPassableOrTrue(MapLocation location) {
        return isPassable(location) != UNPASSABLE;
    }
```

**What it refuses to store: anything that changes.** The cell is written exactly once per
tile, on first sight, and never revisited — `src/finalBot/pathfinder/BFSVision.java` lines
46-50 guard the write on the cell still being `UNKNOWN`:

```java
                        if (PassabilityCache.data.charAt(index) == PassabilityCache.UNKNOWN) {
```

So the memory holds only the **permanent** layer (terrain), and everything mutable —
robots, resources — is re-sensed. There is no timestamp, no "last seen round", no staleness
field anywhere in the class. Two independent Battlecode postmortems describe the same
choice at bit resolution: **"Gone Fishin'" (2nd, 2023)** — *"Each robot (including HQ) has a
MapRecorder that records all the tiles that this robot has seen. Each location is
represented by a char (8 bits):"*, whose first bullet is *"SEEN BIT: whether this tile has
been recorded before. This is also useful to avoid repeatedly scouting the same tile."*
(`postmortem-2023-gone-fishin.pdf`); and **"SPAARK" (HS 1st, 2025)** — *"We stored an array
of 60 longs to keep track of explored tiles (each long can be used as 60 bits, so we
effectively have a 2d array but more bytecode efficient)"* (`postmortem-2025-spaark.pdf`).

WHY IT MIGHT TRANSFER — this is the representation our map-walking code needs, and the
two-reader trick is the part worth stealing.

- **Our terrain layer is permanent too.** `Environment.WALL` / `EMPTY` / `ORE_TITANIUM`
  never change during a match. So the same "write once on first sight, never re-check"
  rule applies exactly, and a per-unit terrain memory is sound *by the same argument they
  used*, with no staleness reasoning required.
- **The two readers map straight onto our two callers.** A route-planner asking "could a
  conveyor line go here" wants `isPassableOrTrue` (optimistic — don't refuse to plan through
  fog). A build-site chooser about to spend titanium wants `isPassableOrFalse` (pessimistic
  — never commit on a guess). **Today we have one predicate and it silently picks one of
  these.** Making the choice explicit at each call site is a small, testable change.
- **It says exactly what NOT to remember.** Our measured hazard is that
  [an entity id stops resolving the moment it leaves vision](an-entity-id-is-not-a-durable-handle.md);
  the winner's answer is to not keep mutable state at all. That is a cheaper discipline than
  building a staleness model we cannot validate.

WHAT WOULD KILL IT —

- **Their memory is per-robot and so is ours, but they had a far bigger channel to
  reconcile it through.** Battlecode 2023's shared array is 64 values of 16 bits
  (`battlecode23/engine/.../GameConstants.java:63` `SHARED_ARRAY_LENGTH = 64` and `:67`
  `MAX_SHARED_ARRAY_VALUE = (1 << 16) - 1`; the spec says *"shared array of 64 non-negative
  integers strictly less than $2^{16}$"*). Ours is 16 values with a one-round write lag. On an 8x8 map we have 64 tiles and ~4-8 builders;
  on 30x30 we have 900 tiles and the duplication is 900 entries per builder. Cheap on CPU
  (not our binding constraint) but it means **every new builder starts blind**, and there is
  no way to hand it the map — see
  [`the-sixteen-ints-really-are-the-only-channel`](the-sixteen-ints-really-are-the-only-channel.md).
- **Bytecode-efficiency is their headline and must not be ours.** Their comment
  *"we gotta save bytecodes - so we return int instead of enum"* and SPAARK's
  *"but more bytecode efficient"* are optimisations for a constraint we measured ourselves
  as non-binding (15.6 us median against a 10,000 us budget). **Copy the tri-state, not the
  bit-packing.** A dict of `Position -> Environment` is fine here and the packed-longs
  version would be pure complexity.
- **It is an enabler, not a plank.** It buys core-kill share only through the plank it
  carries ([symmetry](symmetry-is-the-only-free-information-about-the-unseen-map.md)).

BUILDER HOOK — one dict on the `Player` instance, `self.terrain: dict[Position, Environment]`,
written once per tile from `get_nearby_tiles()` each turn, never overwritten. Two readers,
`passable_or_true(p)` and `passable_or_false(p)`, and a rule that every call site names one.
The test is a null-hypothesis one: run the standing unrated leg with the memory built but
**read by nobody** — it must be exactly Elo-neutral. If it is not, the memory is being read
somewhere by accident and the instrument is lying.
