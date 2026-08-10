---
tactic: (PLANK) FOUR independent Battlecode teams — including the 2023 WINNER and the 2023 runner-up — spend their scarce shared channel on ONE thing: which map symmetry is still possible. It is the only way to know where the enemy base is before anything has walked there, and it is priced in exactly our currency (time-to-core-kill)
source: https://raw.githubusercontent.com/awesomelemonade/Battlecode2023/2e231f31a4622909b0dfd34a68c9b634dde1c803/src/finalBot/util/EnemyHqGuesser.java
origin: "Producing Perfection" (**Battlecode 2023 winner**), "Gone Fishin'" (**2023, 2nd**), "no thoughts head empty" (2023, Newbie 2nd), "SPAARK" (**2025, HS 1st**) — placings from https://battlecode.org/past.html
evidence: documented
transfers: yes
---
WHAT IT IS — Battlecode maps, like ours, are symmetric. Every one of these four teams turns
that into a *prediction of where the enemy base is* from the moment they see their own, and
then narrows it by elimination.

**The winner generates all three candidate reflections of a known friendly HQ in five lines**
(`src/finalBot/util/EnemyHqGuesser.java:46-54`, verbatim):

```java
    public static void guessEnemyHeadquartersLocations(MapLocation location, int hqIndex) {
        int x = location.x;
        int y = location.y;
        int symX = Constants.MAP_WIDTH - x - 1;
        int symY = Constants.MAP_HEIGHT - y - 1;
        predictions[hqIndex * NUM_POSSIBLE_SYMMETRIES] = new MapLocation(x, symY);
        predictions[hqIndex * NUM_POSSIBLE_SYMMETRIES + 1] = new MapLocation(symX, y);
        predictions[hqIndex * NUM_POSSIBLE_SYMMETRIES + 2] = new MapLocation(symX, symY);
    }
```

**A prediction is only falsified when it becomes legally sensable** — never on a guess
(`EnemyHqGuesser.java:145-153`):

```java
        // traverse and remove any that are visible and not there
        for (int i = predictions.length; --i >= 0; ) {
            if (isInvalidatedPrediction(i)) {
                continue;
            }
            MapLocation prediction = predictions[i];
            if (rc.canSenseLocation(prediction)) {
                try {
                    RobotInfo robot = rc.senseRobotAtLocation(prediction);
```

and the array is declared with the unknown case named in the comment
(`EnemyHqGuesser.java:20`):

```java
    public static MapLocation[] enemyHeadquartersLocations; // may include null (for unknown enemy headquarters)
```

**Three more teams, same idea, three different encodings, all of them in the SHARED array:**

- **"Gone Fishin'" (2nd, 2023)** — *"Each map must fit either of 3 symmetry types: rotational,
  vertical, or horizontal."* and *"If the symmetry is not confirmed, all units will check if
  a newly seen tile eliminates an existing symmetry."*
- **"no thoughts head empty" (Newbie 2nd, 2023)** — *"Since maps could be either horizontally,
  vertically, or rotationally symmetrical, amplifiers tested each newly found location
  against known locations to exclude possible symmetries until they settled on one confirmed
  symmetry. This symmetry would then be stored in the shared array."*
- **"SPAARK" (HS 1st, 2025)** — *"We also stored the map symmetry using 3 bits, with each bit
  representing if the symmetry is valid or not."* and, listing its comms layout,
  *"Bits 1-3: Ruled out symmetries (horizontal, vertical, rotational)"*.

**The whole thing costs THREE BITS.**

WHY IT MIGHT TRANSFER — this is the one finding in the sweep that is a plank rather than an
enabler, and it is a plank in the programme's own currency.

- **Our maps are symmetric by construction.** Our own rules state the grid is *"symmetric by
  reflection or rotation"*. So the candidate-generation code above is directly portable,
  with `MAP_WIDTH`/`MAP_HEIGHT` from `get_map_width()`/`get_map_height()` and the friendly
  core position from round 0.
- **It buys `time_to_core_kill` directly, which is our SECONDARY currency, and it is the
  only lever in this sweep that touches the primary one.** Loki's mandate is *"destroy the
  enemy core"* inside 250 rounds. Everything else in sweep 20B is correctness work that stops
  us dying to our own code. This is the one that makes a raid start walking toward the right
  quadrant on round 1 instead of after a scout returns.
- **Three bits fit our channel with room to spare.** We have 16 ints. SPAARK's entire
  symmetry model is 3 bits; the winner's is a set of candidate `MapLocation`s that each unit
  regenerates locally from its own core position — **no comms needed at all for
  generation**, only for elimination. Given that
  [module state is not shared between our units](the-sixteen-ints-really-are-the-only-channel.md),
  the regenerate-locally half is the part that works unchanged, and it is the bigger half.
- **The elimination rule is exactly the guard doctrine from the rest of this sweep.**
  `if (rc.canSenseLocation(prediction))` is our `if ct.is_in_vision(p)`. A candidate is
  never falsified by an unsensable tile — which is also what protects it from the
  exception. Same line does both jobs.

WHAT WOULD KILL IT —

- **Our maps are 8x8 to 30x30 and often small.** On an 8x8 map the enemy core is inside a
  builder's r²=20 within a handful of moves and the prediction saves almost nothing. The
  payoff scales with map size, so this must be measured *per map-size band*, not pooled —
  and `docs/research/tactics/a-hundred-elo-of-map-distribution.md` and
  `map-size-decides-whether-the-rush-is-legal.md` are the existing evidence that pooling
  across our map pool hides exactly this kind of effect.
- **Their maps had 3 symmetry classes and I have NOT verified how many ours has.** Our
  rules say *"symmetric by reflection or rotation"* without enumerating the axes. **If our
  pool is single-class (say, always horizontal), the prediction is free and unique and this
  gets stronger; if it has classes we have not enumerated, the elimination logic is wrong in
  a way that fails silently.** `maps/` is checked into the repo and this is a one-script
  question — do it before building anything.
- **A wrong symmetry assumption is a documented, expensive failure**, by the team that made
  it: see [`the-model-of-the-unseen-map-killed-its-own-core`](the-model-of-the-unseen-map-killed-its-own-core.md).

BUILDER HOOK — smallest possible test, no comms, no elimination, one map-size band:
at round 0 every unit computes the three reflections of its own core position and picks the
one on the far side of the map's long axis; the raid heads there instead of toward its
current target. **Pre-register the falsifier as `time_to_core_kill` on the maps where the
enemy core is NOT within r²=20 of the direct path** — on the rest it must be a no-op, and if
it moves those too, the leg is measuring something else. First, though, run the one-script
check over `maps/*.map26` and write down how many symmetry classes our pool actually has.
