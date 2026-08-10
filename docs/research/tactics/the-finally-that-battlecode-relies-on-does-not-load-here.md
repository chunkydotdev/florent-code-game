---
tactic: The canonical Battlecode guard block is `try` / `catch` / `finally` — and our loader HARD-REJECTS `finally`, bare `except:` and `except BaseException` at load time. Copying the ancestor's shape verbatim fails validation before round 0
source: https://raw.githubusercontent.com/battlecode/battlecode22-scaffold/main/src/examplefuncsplayer/RobotPlayer.java
origin: MIT Battlecode 2022 starter kit (repo `battlecode/battlecode22-scaffold`, branch `main`) vs. the Florent Code League engine loader (`fcode` 2.3.6, `fcode_engine.cpython-313-darwin.so`)
evidence: documented
transfers: partial
---
WHAT IT IS — Battlecode's starter kit ends its per-turn guard block with a `finally`
that yields the turn, so the turn is always ended no matter which handler ran
(`RobotPlayer.java:93-96`, verbatim source lines):

```java
            } finally {
                // Signify we've done everything we want to do, thereby ending our turn.
                // This will make our code wait until the next turn, and then perform this loop again.
                Clock.yield();
```

**Our engine will not load that.** The loader runs an `ast` pass over every module in the
zip before the match. Its source is recoverable verbatim from the shipped engine binary
(`strings -n 4 .venv/lib/python3.13/site-packages/fcode/fcode_engine.cpython-313-darwin.so`):

```python
        if isinstance(node, ast.Try) and node.finalbody:
            raise ValueError(f'{fpath}:{node.finalbody[0].lineno}: `finally` blocks are not allowed')
```

```python
        if ty is None:
            raise ValueError(f'{fpath}:{lineno}: bare `except:` is not allowed; use a specific exception type')
```

```python
        for name in names:
            if name not in ALLOWED:
                raise ValueError(f'{fpath}:{lineno}: `{name}` is not an allowed exception type')
```

**Confirmed live, four arms, one map, one seed** (`.venv/bin/fcode run … maps/eider.map26 --seed 1`):

| bot body | engine response |
| --- | --- |
| `try: pass / except Exception: pass / finally: pass` | `ValueError: <bot>/main.py:8: \`finally\` blocks are not allowed` |
| `try: pass / except: pass` | `ValueError: <bot>/main.py:5: bare \`except:\` is not allowed; use a specific exception type` |
| `try: pass / except BaseException: pass` | `ValueError: <bot>/main.py:5: \`BaseException\` is not an allowed exception type` |
| `try: pass / except (GameError, Exception): pass` | **`Completed turn 0` … match runs** |

The fourth row is the negative control: the same harness that rejects the other three
loads this one and plays the match, so the three rejections are the check firing, not the
harness being broken.

The `ALLOWED` set recovered from the binary contains `'Exception'` and `'GameError'` and
does **not** contain `BaseException`. `ArithmeticError`, `AttributeError`, `IndexError`,
`KeyError`, `OverflowError`, `TypeError`, `ValueError`, `ZeroDivisionError` are all on it.

WHY IT MIGHT TRANSFER — it does not "transfer"; it **constrains** the tactic that does.
Read it as the errata attached to
[`catch-everything-at-the-top-of-run`](catch-everything-at-the-top-of-run.md):

- **Take the `try`/`except Exception`, drop the `finally`.** Python does not need it — our
  `run()` ends the turn by returning, so there is no `Clock.yield()` obligation to
  guarantee. The `finally` is load-fatal and buys nothing here.
- **The ban on `BaseException` is a feature, not an obstacle.** Battlecode arrived at the
  same width deliberately from the other direction — see
  [`the-death-signal-must-outrank-your-blanket-catch`](the-death-signal-must-outrank-your-blanket-catch.md).
- **A `finally` anywhere in the zip kills the whole submission, not one unit.** This is a
  whole-team, round-negative-one failure. Any future agent that "helpfully" adds a cleanup
  block to `eco.py`, `raid.py` or `doctrine.py` bricks the submission. `tools/submit_clean.py`
  should be the place this is caught.

WHAT WOULD KILL IT — nothing about the engine finding; it is measured on the shipped
engine at the version in `.venv`. What could invalidate it is **an engine version bump**:
the `ALLOWED` set and the two structural bans are engine-side and could change. Re-probe
after any `fcode` upgrade. Also note the loader message `store index 16 out of range (0..16)`
is itself off-by-one — index 16 raises, so the usable range is 0..15 — which is evidence
the engine's own error strings are not a reliable specification.

BUILDER HOOK — add three lines to `tools/submit_clean.py` (or `tools/preflight.py`): an
`ast` walk that rejects `node.finalbody`, bare `ExceptHandler` with `type is None`, and
any handler name outside the allowed set, over every `.py` in the bot directory. The
fixtures above are the four test cases, and the fourth is the one that must pass.

> **⚠ BROKEN LINK (research arm, 2026-08-10):** this file links to
> `the-death-signal-must-outrank-your-blanket-catch.md`, which **does not exist**
> (confirmed by `ls`). Pre-existing, not introduced by sweep 21. The link target was
> never written; do not infer its content from the citing sentence.
