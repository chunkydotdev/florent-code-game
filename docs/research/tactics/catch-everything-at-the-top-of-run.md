---
tactic: The direct ancestor's starter kit answers (B) with the crudest option — one catch-all around the WHOLE per-turn body, not per-call-site guards — and it says so in a comment
source: https://raw.githubusercontent.com/battlecode/battlecode22-scaffold/main/src/examplefuncsplayer/RobotPlayer.java
origin: MIT Battlecode 2022, official `examplefuncsplayer` starter kit (repo `battlecode/battlecode22-scaffold`, branch `main`)
evidence: documented
transfers: yes
---
WHAT IT IS — Battlecode is the league where sensing outside vision throws
`GameActionException`, and the organisers' own starter kit does **not** guard call
sites. It wraps the entire per-turn dispatch in `try` / `catch (GameActionException)`
/ `catch (Exception)`, and states the stake in a comment on the `try` line
(`RobotPlayer.java:65-66`, verbatim, two consecutive lines):

```java
            // Try/catch blocks stop unhandled exceptions, which cause your robot to explode.
            try {
```

and again inside the handler (`RobotPlayer.java:82-83`; these are two comment lines,
so the sentence is split by a `//` in the raw file — reproduced here with its own
line breaks rather than joined):

```java
                // handle GameActionExceptions judiciously, in case unexpected events occur in the game
                // world. Remember, uncaught exceptions cause your robot to explode!
```

The method contract is stated twice more, at `RobotPlayer.java:42` —
*"It is like the main function for your robot. If this method returns, the robot dies!"*
— and at `RobotPlayer.java:59` —
*"If we ever leave this loop and return from run(), the robot dies!"*

The organisers' spec gives the doctrine in one sentence
(`battlecode22/specs/specs.md.html`, whitespace-flattened, verified verbatim):

> *"Thus, you must write your player defensively and handle `GameActionException`s judiciously."*

**The referent matters and is stated in the two sentences that precede it in the same
`## GameActionExceptions` section:** *"`GameActionException`s are thrown when something
cannot be done. It is often the result of illegal actions such as moving onto another
robot, or an unexpected round change in your code."* So "defensively" is about the
league's illegal-action exception, not about a defensive game strategy.

WHY IT MIGHT TRANSFER — this is our exact hazard, in the league our engine is modelled
on, and the winners' league answer is the cheapest possible one.

- **The shape maps one-for-one.** Battlecode's `run()` is called once per robot for its
  whole life and contains the turn loop; ours is called once per unit per round. Their
  catch-all sits immediately inside the loop; ours sits immediately inside `run()`. The
  unit of protection is identical: **one turn's worth of work, and nothing escapes it.**
- **Measured on our engine, in one match, with a matched control arm**
  (`bots/_probe_oov_raw` vs `bots/_probe_oov_guard`, `maps/eider.map26`, seed 1): both
  arms have every builder call `get_tile_env(Position(w-1, h-1))` from round 4. The
  unguarded team goes `r=4 units=5` → `r=5 units=2` and **stays at 2 for the rest of the
  match** — every builder is destroyed the first round it makes the call, including every
  replacement. The guarded team, running the identical query with `except GameError`
  around it, reaches 6 units and holds. Same map, same seed, same round, one line of
  difference.
- **`except Exception` — not `except GameError` — is the right width, and that is also
  measured.** `write_store(0, -5)` and `write_store(0, 2**62)` raise **`OverflowError`,
  not `GameError`** (`bots/_probe_oov_surface`, r3). A handler narrowed to `GameError`
  would let that one through and destroy the core. `Exception` is on the engine's
  allowed-handler list (below).

WHAT WOULD KILL IT —

- **`finally` is a load-time rejection on our engine, and the Battlecode kit's structure
  depends on one.** Their per-turn body ends `finally { Clock.yield(); }`. Copying the
  block wholesale does not run here — see
  [`the-finally-that-battlecode-relies-on-does-not-load-here`](the-finally-that-battlecode-relies-on-does-not-load-here.md).
  Take the `try`/`except`, drop the `finally`.
- **A catch-all converts a fatal bug into a silent no-op turn.** Battlecode's kit prints
  and stack-traces inside both handlers rather than swallowing. If we swallow silently we
  will ship a bot that quietly does nothing for 1000 rounds and looks alive. The handler
  must `print()` (captured to the replay) or write a counter to the store.
- **This is an ENABLER, not a plank.** It buys zero core-kill share on its own. It only
  makes it safe to write the map-walking code that does. Nothing here should be priced in
  `core_kill_share`; its currency is "units not lost to our own code", which the programme
  does not score.

BUILDER HOOK — the smallest test: take the current Loki `main.py`, move the entire body
of `run()` into `_turn(ct)`, and make `run()` exactly
`try: self._turn(ct)` / `except Exception as exc: print(...)`. Then re-run the standing
unrated leg and compare **units-destroyed-with-full-HP** against
`docs/research/undamaged-builder-deaths-2026-08-10.md`. If that count does not move, we
were never dying this way and the enabler is free insurance; if it drops, we have been
paying for it.
