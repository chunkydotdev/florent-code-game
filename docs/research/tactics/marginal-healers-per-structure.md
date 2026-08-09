---
tactic: "Marginal repairers needed" — size the repair detail from incoming DPS, not from a role quota
source: https://liquipedia.net/starcraft/SCV
origin: Liquipedia StarCraft Brood War (community wiki), "SCV" article, §Repair Details; corroborated by the same wiki's "Bunker" article
evidence: documented
transfers: yes
---

WHAT IT IS — Brood War's Terran doctrine does not ask "how many SCVs should
repair?" as a role-budget question. It computes a **break-even count** from the
attacker's DPS and the defender's repair rate, and the wiki tabulates it as a
column called *Marginal SCVs Needed*.

The rate is a stated formula:

> "…the SCV Repair Rate is affected by the total health of the unit it is
> repairing, as well as the build time of the unit. Additionally, there's a flat
> 90% modification across all rates. The formula is as follows: Repair Rate =
> 0.9 \* (total health / build time denominated in seconds)."

*(the sentence opens "®Please note that the SCV Repair Rate…" in the source
wikitext — the stray glyph and the lead-in are elided, nothing else)*

and the decision rule is stated as a ratio:

> "When you're reading the table, the Marginal SCVs Needed column is the most
> useful data, which is the Effective DPS / Bunker Marginal Repair Rate."

with worked breakpoints:

> "If a dragoon is attacking a bunker, one SCV is sufficient to exceed the
> dragoon's dps; however, eventually your SCV will completely repair the bunker
> and stop repairing. Likewise, one SCV is sufficient to exceed the dps of two
> marines."

The point is that the answer is *small and integral*. A single worker holds a
bunker against a dragoon; the table's whole Marginal-SCVs column runs from 0.26
to 1.32. Repair is also cheap relative to replacement — "This costs roughly a
third of the repaired's total cost in minerals and gas, while the repair duration
is roughly a third of the unit's build time."

WHY IT MIGHT TRANSFER — **because our numbers are integral and small too, and
nobody here has ever computed them.** Every input exists in the official docs
(`docs/reference/official-docs.md`):

| channel | per round | per round in Ti |
|---|---|---|
| builder **heal** | **+4 HP** on one adjacent tile | 1 Ti |
| enemy builder **attack** | −2 HP | 2 Ti (theirs) |
| enemy **gunner** ("18 every 2 rounds against 7 every round") | −7 HP | 4 Ti (theirs, as ammo) |
| enemy **sentinel** (same line) | −9 HP | 5 Ti (theirs, as ammo) |

Builder action cooldown is **1 round** (official-docs L1142-3), the same
convention under which a gunner with "Reload | 1 round" fires "7 every round" —
so a builder heals **every** round. That makes the marginal-healer table:

| incoming | HP/round | **healers needed** | our Ti/rd | their Ti/rd | exchange |
|---|---|---|---|---|---|
| 1 enemy builder | 2 | 0.5 | 0.5 | 2 | 4:1 us |
| 2 enemy builders | 4 | **1** | 1 | 4 | 4:1 us |
| 1 gunner | 7 | **2** | 2 | 4 | 2:1 us |
| 1 sentinel | 9 | **3** | 3 | 5 | 1.7:1 us |
| gunner + sentinel | 16 | **4** | 4 | 9 | 2.3:1 us |

Two results fall straight out and both are checkable:

1. **A 1×1 turret has exactly four orthogonal neighbours, and healers and enemy
   attackers compete for the same four tiles.** With `k` healers, the enemy can
   field at most `4−k` chippers: heal `4k` vs damage `2(4−k)`. That resolves at
   `k ≥ 4/3`. **Two builders holding two of the four tiles make a turret
   un-chippable by builder attacks, permanently** — and since builder attacks
   cannot damage builder bots, the enemy cannot remove the healers either.
2. **Two healers (8 HP/rd) strictly out-heal one enemy gunner (7 HP/rd).** A lone
   gunner cannot kill a doubly-healed building at all, at a cost to us of 2 Ti/rd
   against their 4 Ti/rd of ammunition.

This is the same shape as the existing 2.2:1 heal-arithmetic result, but stated
as *how many bodies* rather than *how many titanium* — which is the form a
builder can actually branch on.

WHAT WOULD KILL IT — four things, one of which is an instrument bug we should fix
regardless:

1. **`docs/v79-analysis.md` line 360 states "a gunner is ~3.5/rd and a sentinel
   is ~9/rd".** The official docs say the gunner fires *"7 every round"*. If the
   internal number is the stale one, every medic/escort predicate sized against
   it is under-provisioned by 2×. **This needs an engine probe before any of the
   table above is shipped** — it is the single load-bearing input.
2. **HP caps make overflow worthless.** A gunner is 25 HP; two healers restore
   8/rd into a 25 HP ceiling. Healing a full-HP building is a wasted turn and 1
   wasted Ti, so the rule must be `hp < max_hp` gated, exactly as the wiki notes
   ("eventually your SCV will completely repair the bunker and stop repairing").
3. **Opportunity cost is the whole objection.** Two builders pinned to a turret
   for 300 rounds is 600 Ti of heal plus two bodies at 30 Ti × scale (+20% each)
   that are not delivering titanium — and tiebreak #1 is cumulative titanium
   delivered. Brood War's SCV returns to mining the moment the bunker is full;
   ours must too. See [[heal-cap-and-timeout]].
4. **Brood War repair is a continuous rate; ours is a discrete 4 HP tick that
   costs the builder's entire turn and blocks its move that round.** A healer
   cannot reposition and heal in the same round, so a two-healer cell is
   genuinely static in a way an SCV detail is not.

BUILDER HOOK — the smallest test is a **predicate, not a strategy**: before
committing a builder to heal a building under fire, compute
`needed = ceil(incoming_hp_per_round / 4)` from the enemy turrets whose
`get_attackable_tiles_from(...)` covers the target plus the count of adjacent
enemy builders, and **refuse to heal at all if we cannot field `needed`
healers** — a lone healer against a sentinel is 4 HP/rd into 9 HP/rd of damage
and is pure titanium burn.

The corpus instrument that decides whether this is already costing us: **of our
heal actions on a building that was under enemy turret fire, what fraction were
delivered by a detail too small to break even?** If that fraction is high, our
1.11:1 damage-to-repair ratio is partly *wasted* repair rather than defensive
repair, and this predicate is free Elo.

Related: [[worker-fortified-turret-cell]] · [[heal-cap-and-timeout]] ·
[heal arithmetic](../heal-arithmetic-2026-08-09.md)
