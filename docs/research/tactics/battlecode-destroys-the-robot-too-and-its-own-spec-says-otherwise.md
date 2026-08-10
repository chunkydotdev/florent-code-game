---
tactic: CORRECTION TO A PREMISE — our engine's "uncaught exception permanently destroys the unit" is NOT harsher than Battlecode. It is IDENTICAL to Battlecode 2022, 2023 and 2025, where the engine calls `destroyRobot()` on any escape from `run()`. And Battlecode's own published spec says "paralyze", which the engine contradicts
source: https://raw.githubusercontent.com/battlecode/battlecode22/master/engine/src/main/battlecode/world/GameWorld.java
origin: MIT Battlecode engine source, years 2021-2025 (repos `battlecode/battlecode21` … `battlecode25`, branch `master`)
evidence: documented
transfers: yes
---
WHAT IT IS — sweep 20B was briefed with "an uncaught exception PERMANENTLY DESTROYS that
unit … This is strictly harsher than Battlecode's equivalent". **It is not.** I read the
engine for five consecutive years. The relevant three lines are in
`engine/src/main/battlecode/world/GameWorld.java`, in `updateRobot()`, immediately after the
player code has run:

**battlecode22 (`GameWorld.java:142-146`) — and identical in battlecode23 (`:220-224`):**

```java
        // If the robot terminates but the death signal has not yet
        // been visited:
        if (this.controlProvider.getTerminated(robot) && objectInfo.getRobotByID(robot.getID()) != null)
            destroyRobot(robot.getID());
```

**battlecode25 (`GameWorld.java:357-363`)** guards on `robot.getLocation() != null` and then
calls `destroyRobot(robot.getID());` the same way.

**battlecode21 (`GameWorld.java:138-142`) is the outlier, and says so:**

```java
        if (this.controlProvider.getTerminated(robot) && objectInfo.getRobotByID(robot.getID()) != null)
            //destroyRobot(robot.getID());
            ; // Freeze robot instead of destroying it
```

**battlecode24 (`GameWorld.java:212-215`) is the other outlier** — it despawns rather than
destroys, and the comment records the change and the reason:

```java
        // NOTE: changed this from destroy to despawn; double check that this change is correct
        //allowing despawned robots to continue throwing errors may be cause of gc overhead errors
        if (this.controlProvider.getTerminated(robot) && objectInfo.getRobotByID(robot.getID()) != null && robot.getLocation() != null)
            despawnRobot(robot.getID());
```

**"Terminated" covers an uncaught exception.** In `SandboxedRobotPlayer`, the player thread
invokes `RobotPlayer.run` reflectively; an exception escaping it arrives as
`InvocationTargetException` and is reported, and the enclosing `finally` sets
`this.terminated = true;` unconditionally. A *normal* return is treated the same and the
engine prints (`SandboxedRobotPlayer.java:183-188`) `"froze in round "` … `" because it
returned from its run() method!"`.

**And Battlecode's published spec disagrees with its own engine.** The spec's
`## GameActionExceptions` section ends, verbatim in the 2022, 2023 and 2024 specs:

> *"Unhandled exceptions may paralyze your robot"*

*"Paralyze"* is accurate for **2021 only**. In 2022, 2023 and 2025 the engine destroys the
robot; in 2024 it despawns it. The starter kit, meanwhile, tells the truth twice —
*"Try/catch blocks stop unhandled exceptions, which cause your robot to explode."*

WHY IT MIGHT TRANSFER —

- **Directly: it removes an excuse.** If our severity were unique, one could argue the
  ancestor's practices under-invest in guarding. They do not. **The league whose starter kit
  wraps everything in try/catch has our exact penalty**, which makes
  [the catch-all](catch-everything-at-the-top-of-run.md) a like-for-like import rather than
  an adaptation.
- **The spec-versus-engine split is our own house pattern, in someone else's house.** Our
  `CLAUDE.md` already records that the organisers' primary doc is wrong about the tiebreak
  phrasing and about per-category cost scaling, both settled by probing the engine. Here the
  *same class* of error appears in Battlecode: the human-facing spec says "paralyze", the
  engine says `destroyRobot`. **Rule: for any league, the engine is the specification.**
- **It is also a caution about which YEAR you read.** A guard doctrine sourced from a 2021
  postmortem is sourced from the one year where the penalty was mild. Cite the year.

WHAT WOULD KILL IT —

- **I did not run a Battlecode match to confirm the code path**, unlike our own engine where
  the destruction is measured end-to-end (`bots/_probe_oov_raw`: `r=4 units=5` →
  `r=5 units=2`, permanently). The Battlecode claim is read from source across five repos,
  not executed. That is `evidence: documented` at source level, not at behaviour level.
- **One real difference remains, and it is architectural rather than severity.** Battlecode's
  `run()` is called **once per robot for its whole life**, with the turn loop inside player
  code; ours is called **once per unit per round**. So in Battlecode a *single* stray
  exception at any point in a 2000-turn lifetime ends the robot, whereas in principle our
  per-round call boundary could have been forgiving — **it is not**, but the two engines
  arrive at the same outcome by different routes, and that is worth stating precisely rather
  than as "same rule".

BUILDER HOOK — none. This is a premise correction for the research lead and for anyone
citing Battlecode practice: **name the year, and quote the engine, not the spec.**
