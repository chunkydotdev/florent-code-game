# Why we cannot kill a healer: four verified defects that form one chain

**Research arm, 2026-08-09 (session 22).** Magnus's trickster tasking, axis C
(machinery we own, pointed wrong). Read-only audit of `bots/_v103split/`
(main.py 3,994 lines + doctrine.py 1,141), cross-checked against the engine type
stubs. **Every claim below re-verified by me against source before relay.**

**Version tag:** live **v90 "Heimdall 1"** = `bots/_v104latch`, tree `2c6dbc17`.
Audited chassis is `_v103split` (the det-proved doctrine split of `_v100hf`).

---

## THE CHAIN

`heal-arithmetic-2026-08-09.md` established from the ruleset that healing is
4.00 HP/Ti against a best damage source of 1.80, that **builder attacks damage
buildings only** so builders cannot attack enemy builders, and therefore that
**only a turret or a launcher can remove a healer.** This audit is why ours
cannot.

### 1. We field Sentinels, and Sentinels can never be re-aimed

`PRIMARY_SENTINEL = True` (doctrine.py:950); both `_plan_siege` and
`_try_counterbattery` prefer Sentinel. **Verified in the engine stub:**
`can_rotate` reads *"Return True if this **gunner** can rotate to a different
compass direction this turn."* **Gunner-only.** A Sentinel's facing is fixed for
its entire life.

### 2. The only re-aim mechanism is `destroy()` + rebuild, and we have ZERO call sites

`grep` over the live chassis: `destroy` / `can_destroy` / `self_destruct` appear
**nowhere** in 5,100 lines. The engine contract (`_types.py:594-601`) is
*"Destroy the allied building at building_pos. Does not cost action cooldown."* —
free, unlimited per turn, and it removes the entity's cost-scale contribution.

**A home Sentinel that the siege walks around is permanently inert, and the fix
is a capability we own and have never called.** Our own files spec the doctrine
three times without building it: `main.py:3541`, `doctrine.py:511`,
`docs/research-brief-2026-08-07.md:130`.

### 3. Our turrets deprioritise builders everywhere except one map and one seat

Verified at `main.py:3620-3624` / `:3653-3668`:

```python
healer_focus = (map is 26x26 and enemy_anchor == (5,5))   # snowflake seat B ONLY
if healer_focus: prio = {BUILDER_BOT: 0, CORE: 1, ...}
else:            prio = {CORE: 0, SENTINEL: 1, GUNNER: 2, BUILDER_BOT: 3, ...}
```

**The one table in the file that shoots healers first is map-locked to a single
seat of a single map.** Everywhere else our primary weapon shoots enemy turrets
before enemy builders.

**Sub-finding 3b:** the tie-break is `if prio < best_prio` — a strict first-wins
scan over `get_attackable_tiles()`, whose enumeration `docs/game-model.md:283-290`
measured as **absolutely oriented** (N/NE/NW/W turrets engage the farthest enemy
on the line; E/SE/S/SW the nearest). **Two enemy builders on the same Sentinel
line are resolved by our own facing.** Documented-and-unfixed in the shipped
file; the fix is a `(prio, dsq)` tuple compare.

### 4. And we could not afford the kill anyway

`AMMO_FLOOR = 16` (doctrine.py:949); magazine is
`max(16 | 24 under siege, min(48, 4 * weapons))` (main.py:594-606).

**A 40-HP builder takes 3 Sentinel shots = 30 ammo. Our standing peacetime
magazine is 16.** The `4 * weapons` term is priced at 4 = **one GUNNER shot** —
the comment on main.py:603 says so explicitly — while we fire Sentinels at 10.

**`doctrine.py:1025-1029` already contains this exact criticism**, written about
the *disabled* `SPORKS_AMMO_ON` block: *"we are sentinel-heavy at 10, so a cap of
60 is six sentinel shots."* Nobody wrote the note on the live block. The
`atoll → 32` and `hive → 256` magazine hacks are hand-patches around this
constant.

**Sequencing (the audit's recommendation, endorsed): 4 → 3 → launcher exile is
ONE leg with three ablatable flags.** Fixing what the guns shoot without fixing
what they can afford just wastes shots.

---

## TWO MORE

### 5. `_link_path`'s undecoded-map fallback has no team test

Verified. The decoded branch is correct — `elif ct.get_team(eid) != self.team:
blocked.add(key)` (main.py:2986-2991). The fallback branch (main.py:3073-3082)
checks entity **type** only. **On any map absent from the map book, our trunk
chain can be planned terminating into the enemy network.**
`doctrine.py:1083-1088` records five of fifteen rotation maps undecoded as
recently as 2026-08-06.

**Candidate mechanism for the 36.5 stacks/game we push onto enemy networks**
(`flow.tsv`, vs their 25.7). Two-line fix mirroring the decoded branch.

### 6. We measured the offensive siphon ourselves and never used it

`doctrine.py:846-873`, a constructed 10x10 probe: *"the engine's output rule is
ROUND-ROBIN LEAST-RECENTLY-USED over the four cardinal neighbours and it DOES NOT
LOOK AT TEAM"*; *"one acceptor per team → strict 50/50 alternation over 800
rounds, zero exceptions"*; *"Final credit 990 (us) / 1470 (them) off that single
harvester."* Confirmed at `docs/game-model.md:331-337`.

So one 3-Ti conveyor adjacent to one of **their** harvesters, wired into our
chain, takes **50%** of its output. We have `_find_siphon` and `_siphon_deny`,
both purely defensive.

**The refutation is in our own notes and is serious:** a dead-end stub delivers
zero (`doctrine.py:876-884`), so the tap needs a completed chain home across the
map, destructible along its length. **The cheap variant exists only where their
farm sits near our chain — and `play-the-players-2026-08-09.md` §3 measured that
by r150, 34% of their new harvesters are nearer OUR core than theirs.**

---

## DEAD INVENTORY

| item | state | note |
|---|---|---|
| `LAUNCHER_RESERVE = 80` | read nowhere | delete |
| `self.forward_barriers` | written once, never read | dead state named for a feature that does not exist |
| `B8_ON = False` | hides a pure CPU win | the `_try_counterbattery` reach test (main.py:2235-2238) is gated behind it and is unrelated to B8's sensing change; without it every defender turn burns a ~128-256-call scan on out-of-reach threats. **Worth splitting out.** |
| `SPORKS_AMMO_ON`, `HIVE_FREEZE_ON`, `HS_SEAT_BAN_CONVEYORS` | False | all measured-refuted, correctly off |

## NEGATIVES — so nobody re-chases them

- The either-team launcher pickup is **already correct** (`main.py:3937-3943`,
  `dist_sq <= 2` matches the measured 8-neighbour ring).
- **Builders genuinely cannot attack builders** — `fire()` *"only damage[s] the
  building on it"*. This is why 1-4 are one cluster, not four ideas.
- Feeding titanium into the enemy core has **no offensive flip**; it is a gift,
  and our conveyor facing is correctly one-directional.
- `can_spawn` is **Core-only** and cannot be asked about the enemy core.
- **Splitters are never built and there is no arithmetic case for them.** Zero
  call sites for `build_splitter`. Do not spend a slot.
