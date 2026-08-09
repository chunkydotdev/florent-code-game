---
tactic: The blockade should be made of the cheapest legal object, not the best unit
source: https://battlecode.org/assets/files/postmortem-2021-musketeers.pdf
origin: Battlecode 2021 3 Musketeers (blockade rush); same principle in Battlecode 2021 Wololo's "burier" role
evidence: documented
transfers: yes
---

WHAT IT IS — 3 Musketeers started their enemy-base blockade with *strong* units
and discovered the unit's stats were irrelevant, because a blockading unit never
fights — it only occupies. They rewrote the sizing rule:

> *"Eventually, we realized that increasing our number of muckrakers spawned
> would allow us to overwhelm the enemy regardless of how big the muckrakers
> were, so we switched to spawning small 1-influence muckrakers."*

That is the whole tactic: **a body used as terrain should cost the minimum the
rules allow.** They had been paying 50 influence per blockader; they dropped to
1, the floor.

WHY IT MIGHT TRANSFER — **it transfers as a correction, and it points away from
the material every existing denial file in this library implicitly assumes.**

Our two candidate blockading objects are priced very differently, and the
*scaling* term matters more than the sticker:

| object | cost | scale hit | HP | blocks build? | blocks `can_spawn`? | mobile? |
|---|---:|---:|---:|---|---|---|
| **barrier** | **3 Ti** | **+1%** (joint-cheapest in the game) | 30 | yes | yes (building ⇒ not passable) | no |
| builder bot | 30 Ti | **+20%** | 40 | yes | yes (bots mutually impassable) | yes |

**A blockade made of builder bots costs 10× the titanium and 20× the scale
increment of one made of barriers** — and the +20% is charged against *every
future builder, gunner and sentinel we buy for the rest of the match*. Twelve
barriers seal the whole 12-tile spawn ring for ~36 Ti and +12% on the
cheapest-scaling category. Twelve builder bots would cost 360 Ti at base and
would roughly triple our own builder price.

**The removal arithmetic is what makes the barrier the right body here, and it is
the nastiest exchange rate in this game:**

- `destroy()` is **allied-only** (engine type stubs, per [[spawn-smothering]]) —
  they cannot delete our barrier cheaply at all.
- A builder attack is **2 damage for 2 Ti**, so a 30 HP barrier costs them
  **15 builder-turns and 30 Ti** to remove. **10:1 in titanium and 15:1 in
  turns, against an object we placed in one turn.**
- Shooting it costs **5 gunner shots = 20 Ti of ammo** from a pool with **no
  passive income**.

WHAT WOULD KILL IT — three real limits, and the first is the one that decides it:

1. **A barrier cannot be placed where a body already stands, and cannot follow.**
   Build legality is strictly stronger than `is_tile_empty` — the s24 probe
   (`bots/_probe_prison`) found `can_build_barrier = False` on a tile holding a
   standing bot even with `is_tile_empty = True`. So barriers can only take
   *vacant* ring tiles, and a defender who parks its own bodies on its ring
   denies us the cheap material and forces the expensive one.
2. **Placement adjacency is the real cost.** Each barrier needs our builder
   **orthogonally adjacent** to the target tile, one per turn, standing inside
   the enemy's turret coverage. The 3 Ti is not the price; **12 builder-turns
   under fire** is the price.
3. **The mobility we give up is not free.** A barrier cannot re-block a tile the
   defender clears. 3 Musketeers' muckrakers could re-form; our barriers cannot.
   Wololo's burier role solved exactly this by *re-recruiting into gaps* — with
   barriers we must re-walk a builder to the gap.

BUILDER HOOK — **the builder arm reached the same 36 Ti number
independently from the engine constant on 2026-08-09 — their probe note prices a
spawn-lock at 12 barriers ≈ 36 Ti rather than ≈120 (coordination 08:52) — **so the arithmetic is
settled and the open question is delivery, not price.** Beyond that,
this file mostly changes a number in tactics we already have,
so the hook is a sizing audit, not a build.** Anywhere in the Loki tree where a
denial/blockade idea is costed in **builder bots**, re-cost it in **barriers**
and re-check whether it clears. Concretely: the spawn-ring seal is a **~36 Ti,
12-builder-turn** proposition, not a 360 Ti one — which moves it from "obviously
unaffordable" into the range of a 500 Ti opening bank.

Related: [[spawn-smothering]] · [[press-them-onto-their-own-spawn]] ·
[[ore-tile-denial]] · [[the-blockade-blanks-your-own-guns]]
