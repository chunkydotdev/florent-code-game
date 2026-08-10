---
tactic: (B) HOW THE WINNER ACTUALLY WROTE IT — mask FIRST, try/catch as backstop, and a third layer that RE-THROWS in the dev build and silently swallows in the tournament build, flipped by one boolean constant
source: https://raw.githubusercontent.com/awesomelemonade/Battlecode2023/2e231f31a4622909b0dfd34a68c9b634dde1c803/src/finalBot/util/HasAdjacentUnpassableCache.java
origin: "Producing Perfection" — **Battlecode 2023 overall winner** (https://battlecode.org/past.html). Repo `awesomelemonade/Battlecode2023`, commit `2e231f31a4622909b0dfd34a68c9b634dde1c803`
evidence: documented
transfers: yes
---
WHAT IT IS — the sweep asked whether winners guarded every call site, wrapped in try/catch,
precomputed a legality mask, or restructured so the illegal call is unreachable. **The 2023
winner did the first three at once, in seventeen lines**, and the ordering is the finding.
`src/finalBot/util/HasAdjacentUnpassableCache.java:21-38`, verbatim:

```java
    public static boolean isPassable(MapLocation location) {
        try {
            if (rc.canSenseLocation(location)) {
                return rc.sensePassability(location);
            } else {
                if (Util.onTheMap(location)) {
                    // locations outside of map are not passable
                    return false;
                } else {
                    becauseOfCloud = true;
                    // because of cloud
                    return false; // assume false
                }
            }
        } catch (GameActionException ex) {
            Debug.failFast(ex);
        }
        return false;
    }
```

Three layers, in this order:

1. **The mask decides.** `rc.canSenseLocation(location)` gates the only call that can throw.
2. **The fog is CLASSIFIED, not just refused.** Both branches return `false`, but they set
   `becauseOfCloud` differently — so the caller can tell "off-map" from "obscured". (Line 19
   labels that field verbatim: `private static boolean becauseOfCloud = false; // ugly hack`.
   As a raw observation: the comment `// locations outside of map are not passable` sits in
   the `Util.onTheMap(location)` **true** branch, which reads as misplaced; both branches
   return `false` regardless, so it does not change behaviour. `Util.onTheMap` is a
   one-line pass-through to `rc.onTheMap`, `Util.java:444-446`.)
3. **The catch is a backstop that changes behaviour between builds.** `Debug.java:11-15`:

```java
    public static void failFast(GameActionException ex) {
        if (Constants.DEBUG_FAIL_FAST) {
            throw new IllegalStateException(ex);
        }
    }
```

and in the shipped final bot, `Constants.java:9` reads `public static final boolean
DEBUG_FAIL_FAST = false;`. **So in the tournament build the exception is silently swallowed;
in the dev build the same line re-throws and kills the robot loudly.** The same pattern is
used on their symmetry-elimination sense
(`EnemyHqGuesser.java:160-161`: `} catch (GameActionException ex) { Debug.failFast(ex); }`).

WHY IT MIGHT TRANSFER — it resolves the tension between the two guards this sweep produces.

- **[The catch-all](catch-everything-at-the-top-of-run.md) and
  [the mask](the-legality-mask-is-a-total-function.md) are not alternatives, and the winner
  shows the composition.** The mask handles the anticipated case and returns *information*
  (`false`, plus a reason). The catch exists only for the case the mask author did not
  anticipate. **Anything reaching the catch is a bug**, which is why it is wired to a
  fail-fast in development.
- **The dev/tournament split is the answer to the objection that a catch-all hides bugs.**
  We can have both: `except Exception` that re-raises when a module-level `DEBUG` flag is on
  and prints-and-returns when it is off. Our engine allows this — the ban is on `finally`,
  bare `except:` and `BaseException`, not on conditional re-raise
  ([measured](the-finally-that-battlecode-relies-on-does-not-load-here.md)).
- **Classifying the fog rather than collapsing it is what
  [Double J's preachers failed to do](the-model-of-the-unseen-map-killed-its-own-core.md).**
  `becauseOfCloud` is a two-line version of that discipline from the team that won.

WHAT WOULD KILL IT —

- **In the shipped build layer 3 is a silent swallow, and that is exactly the failure mode
  our own doctrine warns about.** A bot that swallows quietly for 1000 rounds looks alive.
  The winner's mitigation is that the flag exists at all and they used it locally; ours must
  be a counter written to the store or a `print()` to the replay, not nothing. **Do not copy
  the `false` branch without copying a way to notice it fired.**
- **Their fail-fast throws `IllegalStateException` — i.e. it deliberately kills the robot to
  surface the bug.** On our engine that is not a debugging aid but the production failure
  mode, so the dev-build branch must be exercised only in local `fcode run`, never in a
  submitted zip. `tools/submit_clean.py` should assert the flag is off.
- **Enabler, not a plank.** No core-kill share. Priced in "bugs found in development", which
  the programme does not score.

BUILDER HOOK — the smallest version, three lines, that gives us both builds:

```python
DEBUG = False
...
        except Exception as exc:
            if DEBUG:
                raise
            print(f"guard {ct.get_id()} {type(exc).__name__}: {exc}")
```

Then run the existing local battery once with `DEBUG = True`. **Any unit that dies in that
run is a bug we are currently shipping and hiding.** That single run is the whole test, and
it costs one match.
