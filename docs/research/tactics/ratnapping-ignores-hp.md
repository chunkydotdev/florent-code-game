---
tactic: Kidnapping is HP-independent — so the counter is information, not durability
source: https://battlecode.org/assets/files/postmortem-2026-generalized-strokes-theorem.pdf
origin: Battlecode 2026 Generalized Strokes Theorem
evidence: documented
transfers: yes
---

WHAT IT IS — Battlecode 2026's "ratnap" (pick up an enemy unit) has the property
that makes theft structurally different from damage, and the 2026 team states it
as the reason they rebuilt their micro:

> *"enemies behind you or to the side of you can ratnap you regardless of health"*

A full-HP unit is exactly as stealable as a dying one. Every defensive instinct
built around HP — retreat when low, heal, tank with the healthy unit — is
therefore **the wrong instinct against a grabber.** They ranked it above the
map's environmental hazard:

> *"so preventing enemies from ratnapping you was a higher priority for us than
> avoiding the cat path"*

**And their answer was not armour or positioning-by-HP — it was information.**

> *"squeak maximization: every turn in Micro, every Baby Rat would squeak their
> health, nearest enemy health, nearest enemy direction, and nearest enemy
> location."*

They spent their whole per-unit communication budget on **knowing where the
grabbers were**, because that is the only defence against a threat that does not
care how healthy you are.

**AND THIS IS THE ONLY PRIOR ART THAT EXISTS.** Sweep 11 searched Screeps, Terminal,
Halite III, Lux AI S1/S2 and BattleSnake for any involuntary unit-displacement
primitive and found **none**: Screeps' only candidate, `Creep.pull`, returns
`ERR_NOT_OWNER` on a foreign creep and requires the *target* to call `move()`
itself — *"Help another creep to follow this creep"* (docs.screeps.com/api) — and
`steal|capture|take control|push|pull|displace` returns zero hits across the Lux
S1/S2 specs, the Halite III rules, Terminal's `game-configs.json` and the
BattleSnake rules. **Battlecode 2026 is the only comparable league that lets you
move an enemy unit, and it is one season old.** Anything we learn about the
launcher we are learning first-hand.

WHY IT MIGHT TRANSFER — **our launcher has exactly this property and neither side
of this league appears to have priced it.**

`launch(bot_pos, target)` picks up an adjacent builder bot **from either team**
and there is no HP term anywhere in it. Two consequences, in opposite directions:

**Offensively — grab priority must never key on HP.** Any targeting rule of the
shape *throw the weakest enemy builder* is importing a damage intuition into a
theft mechanic. The right key is **what that builder is doing** (is it adjacent
to one of our buildings? is it standing on a tile we want? is it their healer?)
and **where we can put it**. Their healer at 40/40 HP is the single best grab on
the board — our own arithmetic says a defender's heal is **4.00 HP/Ti** against
our best damage at **1.80 HP/Ti**, so **removing the healer from the tile is
worth more than any damage we could do to it**, and costs 0 ammo.

**Defensively — the same is true of us, and we have measured the exposure.**
Enemy builders reach our door: **7.5% of their builder deaths are at d²≤2 from
our core and 27.4% within d²≤8**, against 7.6% for us at theirs
([[launcher-defensive-interception]]). Any enemy launcher within r²=26 of one of
our builders can move that builder anywhere passable, at any HP, for free. Our
healers standing on core footprint tiles — the **8.00 HP/Ti stacked-tile seat**
that the whole heal arithmetic rests on — are the highest-value grab targets on
the board **and they are stationary by design.**

**The 2026 counter is available to us and cheap.** We have 16 integer slots and
they are not saturated. A single slot carrying "an enemy launcher is standing at
(x,y)" is enough for every builder to avoid ending a turn within r²=26 of it —
which is the direct analogue of squeak maximization at a fraction of the cost,
because our store is team-global rather than per-unit broadcast.

WHAT WOULD KILL IT — 

1. **Does the field field launchers at all?** If enemy launcher counts are near
   zero, the defensive half is worthless. **This is a corpus count, not a
   battery**, and it must be run before any store slot is spent. We know at least
   one opponent (Albert And Einstein, ~1307) builds a launcher on turn 1 — but
   for **rush delivery of their own scout**, not for grabbing ours
   (`docs/opponents.md:110-125`).
2. **Avoidance may be unaffordable.** Telling builders to keep r²>26 from an
   enemy launcher could evacuate exactly the tiles our economy and our heal seats
   need. **Avoidance that costs a heal seat is worse than being grabbed**, given
   the seat is worth 8.00 HP/Ti.
3. **Unmeasured engine facts gate the offensive half**, and they are the same
   three that gate every launcher tactic: is `can_launch` adjacency 4-way or
   8-way; must the target be reachable or merely passable; does being thrown
   alter the thrown bot's cooldowns. **If a throw does not cost the victim its
   turn, half the value evaporates.**

BUILDER HOOK — **two cheap things, neither of which is a bot change:**

1. **Corpus count:** launchers built per game per opponent, and how many of our
   builder-bot position discontinuities (a move of more than one tile in a round)
   are enemy throws of *our* units. If that number is above zero we are already
   being kidnapped and do not know it.
2. **Then, and only then**, one probe: `can_launch` on a **full-HP** enemy
   builder, to confirm the HP-independence holds in this engine as it does in
   Battlecode 2026.

Related: [[score-the-throw-destination]] · [[launcher-defensive-interception]] ·
[[displace-dont-kill]] · [[throw-into-prebuilt-cell]] ·
[heal arithmetic](../heal-arithmetic-2026-08-09.md)
