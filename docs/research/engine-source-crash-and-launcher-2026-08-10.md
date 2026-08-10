# ENGINE SOURCE: the destruction path, the crash surface, and the launcher

Read from the shipped engine binary (`.venv/lib/python3.*/site-packages/fcode/`)
by disassembly, **two independent toolchains (`objdump` and `otool -tV`) with
separate parsers, results intersected**. This is the PRIMARY. Where it disagrees
with `docs/reference/official-docs.md` or with `CLAUDE.md`, it wins.

Caveat carried from the agent and not laundered: this is the **local** `.so`.
The platform may ship a different build. Items flagged LOCAL-ONLY below.

## 1. THE DESTRUCTION PATH — confirmed, and narrower than we wrote

Three distinct failure sites, resolved by their `eprintln!` format strings
(an earlier attribution by address alone was wrong — all three drop a `PyErr`):

| site | what failed |
|---|---|
| `0x19d40` | `[runner] unit {} failed to init` — Player instantiation |
| `0x1a640` | `[runner] unit {} turn setup failed` — Controller construction, before `run()` |
| **`0x1ac5c`** | **the uncaught exception escaping `run()`** |

All route to the same `Game::destroy_entity` used by death-by-damage. **Per
unit, real destruction, indistinguishable in the replay from a normal death
except that no damage precedes it** — which is exactly the signature
`tools/crash_census.py` keys on.

**THE EXEMPTIONS ARE EXACTLY TWO:**

    1a95c  PyErr_GivenExceptionMatches(exc, PyExc_KeyboardInterrupt) -> no destroy
    1a9dc  PyErr_GivenExceptionMatches(exc, PyExc_SystemExit)        -> no destroy,
           else fall through to 1ab5c -> 0x1ac5c destroy_entity

**`SystemExit` and `KeyboardInterrupt` only. An escaping `GameError` DESTROYS
THE UNIT.** The TLE "interrupted" flag (`w28`) is ANDed with the turn-timeout
config and written to the replay as a bool — **it is NOT routed to destroy**, so
a CPU timeout does not kill the unit while any other escaping exception does.
That is the distinction `CLAUDE.md` asserts, now confirmed on the binary.

*Honest limit:* the agent could not find the timeout INJECTION mechanism —
`Watchdog::arm/disarm` make no Python C-API calls and the import table has no
`PyThreadState_SetAsyncExc`, `Py_AddPendingCall`, or `PyEval_SetTrace`.
"SystemExit is the timeout signal" is **inference from the exemption logic, not
disassembly fact.**

## 2. THE CRASH SURFACE — what actually raises

**A third guard nobody had listed:** `get_nearby_tiles`, `get_nearby_entities`,
`get_nearby_buildings`, `get_nearby_units` raise **`"dist_sq exceeds vision
radius"`** when passed an explicit `dist_sq` larger than the CALLER's radius
(str ref `0x4d30` in `get_nearby_tiles @ 0x4b0c`; the other three funnel
through it).

**This is a live self-inflicted risk for us, not only an attack surface.** A
launcher scanning at its own r²=26 is legal; **a builder bot passing 26 is not**
(builder r²=20). Any code that shares a radius constant across unit types is one
refactor away from deleting its own units.

**Vision-error strings, corrected** (`assert_entity_in_vision @ 0xbaec`):
* `"Position out of vision range"` @ `0xbce8` — the single-tile path, i.e.
  **every entity except the core**.
* `"Entity out of vision range"` @ `0xbf20` — **the core only** (enum tag 5),
  tested as a 3x3 block of nine `is_in_vision_unchecked` calls, raising only if
  all nine miss.

So `get_hp(enemy_gunner)` raises "Position…", `get_hp(enemy_core)` raises
"Entity…". Same membership, different labels — the labels were previously
recorded the wrong way round.

`launch()` and `fire()` also raise **`"Unknown id"`**, as do `can_act`,
`get_gunner_target`, `get_move_cooldown`, `get_action_cooldown`,
`get_attackable_tiles`.

## 3. THE LAUNCHER — no vision guard, no team check

**`can_launch`, `can_fire`, `can_fire_from`, `can_move`, `can_heal`,
`can_destroy`, `can_spawn` and all seven `can_build_*` have ZERO vision
guards** — no string reference, no `is_in_vision_unchecked` call.

Mechanics as read:
* **pickup ring d² <= 2** (so orthogonal AND diagonal neighbours of the launcher)
* **throw range 1 <= d² <= 26, measured FROM THE LAUNCHER**
* **no team check on the picked-up builder** — enemy bodies are legal targets
* **costs 0 ammo; launcher cooldown += 1**
* **position-only mutation** of the thrown unit

That last one is the interesting one for a trick: the engine changes the
victim's POSITION and nothing else, so the victim's own cached state (previous
position, path, "the tile I was about to build on") silently goes stale. **Our
own `eco.py` carries a guard for exactly this because a throw made OUR builder
raise** — which is direct evidence that a naive bot's cached position state does
not survive being thrown.

Separately: **`ct.can_fire()` on a launcher raises `"Use can_launch() for
launchers, not can_fire()"`** — a different guard from the vision one, and it
deletes any launcher swept up in a generic turret loop.

## 4. LOCAL-ONLY: `get_cpu_time_elapsed()` is hardcoded to 0 in this build

    14970  ldr xzr, [x8, #0x258]   ; CPU_DEADLINE_NS -> discarded
    14978  ldr xzr, [x8, #0x250]   ; CPU_START_NS    -> discarded
    14980  mov x0, #0x0

`CPU_DEADLINE_NS` is loaded at the top of 112 Controller methods and the
destination is `xzr` in **113 of 113 sites** — nothing branches on it. The
per-call deadline check is compiled out here.

**CONSEQUENCE FOR OUR BOT:** every `self._cpu_exhausted(ct)` guard in the Loki
tree is a **no-op locally**, so local runs cannot exercise our CPU backstops at
all. Corroborates the existing note at `docs/coordination.md:37`.
**Unverified remotely — do not conclude the platform behaves this way.**

## 5. Sandbox facts worth knowing before designing a trick

* **AST validation runs per MATCH, not at submission** (`validate_bot_ast @
  0x1c114`, executed via `Python::run` from `runner::run` after
  `read_py_sources_from_disk`). Failures surface as
  `"Bot A failed validation: …"`. Whitelist is 69 names. **`finally:` is banned
  outright**, as is bare `except:` and any non-plain-name handler type.
* **The clock is frozen.** `time.time/monotonic/perf_counter/process_time/
  clock_gettime` and `datetime.now/today` are pinned to constants
  (2076-03-16 14:00 UTC). The in-source comment names the exploit it blocks:
  bots detecting submission age to play a real strategy only for the first N
  minutes. **That road is closed by construction — do not spend a leg on it.**
* `builtins.open` and `memoryview` are deleted; `Player` is renamed to a random
  32-hex string at load.

## What this licenses, and what it does not

**LICENSED:** launcher kidnap of enemy builders as a denial/displacement tool
(no vision guard, no team check, free, d²<=2 pickup, d²<=26 throw). Whether
throwing a victim makes ITS bot raise is **not established here** — the engine
only guarantees the position changes; the raise depends on the victim's own
code, which is why `crash_census.py` measuring opponents at 2,451 unexplained
removals against our 0 is the relevant prior, not proof.

**NOT LICENSED:** any claim that we can reliably crash a specific opponent.
That needs a live leg with a pre-registered mechanism counter.
