---
tactic: Infer the enemy's bank from their observed spending, and strike in the window where the counter is unaffordable
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf
origin: Battlecode 2020, Java Best Waifu (top-ranked lattice bot; the team that broke the 2020 rush meta)
evidence: documented
transfers: yes
---

## WHAT IT IS

Java Best Waifu's attacking unit (the Delivery Drone) had a hard counter (the Net Gun),
and they observed that opponents built the counter *reactively* — the moment they saw a
drone. Rather than scouting for the counter, they inferred the opponent's **cash
position** from the opponent's **observed expenditure**, and committed only in the window
where the counter was unaffordable:

> *"we decided to spawn Drones only if the enemy has spawned a unit or built a building
> recently (this way we assume they wouldn’t have the soup for a Net Gun)"*

**Referent check.** "they" = the enemy team; "the soup" = soup, the 2020 resource; "a Net
Gun" = the anti-drone building. The surrounding sentences are explicit about the causal
chain: *"We realized that most of the teams would build a Net Gun right after we spawn our
first Drone, so we decided to spawn Drones only if the enemy has spawned a unit or built a
building recently"*

The same section carries the reactive-production rule the trigger sits inside — a
`RushManager` that fires on a sensed condition, not a clock:

> *"create a RushManager class that would take care of the unit production if we sense we
> are being rushed"*

> *"we would spawn one Drone for each Landscaper that the enemy spawns, otherwise we would
> spawn one Landscaper for each Landscaper that the enemy has +1"*

And the documented failure of the inference, in the same paragraph — an opponent who
**banked** instead of spending broke it:

> *"Our games against Kryptonite depended almost uniquely if our initial drone was able to
> repel or capture their rush miner or not."*
> (verified in sweep 14; the preceding sentences state Kryptonite *"rushed relatively
> late"* and *"stacked a lot of soup in between"*.)

## WHY IT MIGHT TRANSFER

This is the cleanest published answer to *"what was in the trigger?"* — and it is the one
trigger shape that **costs no scouting**, because the evidence is the opponent's own
buildings appearing in vision, not a reconnaissance mission.

Our ruleset makes the inference *sharper* than theirs, in three specific ways:

1. **Their counter to a forward plant is a turret, and turrets cannot fire without ammo,
   and ammo has exactly one source.** Teams start at **0 ammo**, there is **no passive ammo
   income**, and the only source is `convert_ammo` at the core, 1:1 from titanium, at most
   once per team per turn. So an enemy who has spent their titanium on buildings has, at
   that instant, *no way to buy the shots that would clear our plant* — the conversion
   competes with the build for the same pool.
2. **Build costs scale.** Every enemy build raises their own next cost by 1-20% depending
   on category. Observed builds are therefore evidence about their *future* prices as well
   as their present bank.
3. **Their spending is visible without a dedicated scout.** `get_nearby_buildings()` inside
   a builder's r²=20 or the core's r²=36 returns ids; `get_entity_type(id)` classifies
   them. A builder doing economic work near the midline sees new enemy structures appear as
   a side effect of standing there.

The measured convergence is what makes this worth a plank. Our own core-kill incidence cut
(`docs/research/core-kill-incidence-cut-2026-08-09.md`) found the largest single
discriminator on the enemy side is **`THEM_ti_collected_end_w50`, AUC 0.32, "their economy
did not come up"** — an *economic state* read, not an aggression read — with the
runtime-readable proxy being **their conveyor count (70.1% of their early conveyors sit
inside one builder's r²=20 of their own core)**. Java Best Waifu's trigger is the same
construct measured a different way: *read their economy, commit when it is weak.*

## WHAT WOULD KILL IT

- **The banking counter-strategy, which is documented and named.** Kryptonite defeated this
  exact inference by not spending — accumulating and then buying the counter in one turn on
  arrival. Any opponent who holds titanium looks, to this trigger, exactly like an opponent
  who has none. Our library already records that *we* are the banking archetype
  (*"We bank and do not spend"*), so an opponent running this trigger on us would misread us
  the same way.
- **Ammo is invisible.** There is no `Controller` getter for the enemy's titanium or ammo —
  `get_global_resources()` and `get_global_ammo()` are this team's. The inference is
  strictly indirect and cannot be validated at runtime.
- **The 2.2:1 heal edge does not care about their bank.** An enemy with zero titanium can
  still out-repair sub-threshold damage using titanium they earn during the fight. The
  window this trigger opens is a *purchasing* window, not a defence-free window.
- **One-round staleness.** A build we see this round was paid for last round; they may have
  converted ammo in the same turn (conversion does not consume the core's action cooldown).

## BUILDER HOOK

Smallest test: a **core-side counter of enemy build events seen in the core's r²=36**,
maintained in core instance state (no store slot needed — one writer, and the core never
moves). Define `their_recent_spend = builds observed in the last K rounds`. Gate the
existing forward commitment on `their_recent_spend > 0` in the previous ~5 rounds, and
measure `core_kill_share` against LOKI-(N−1) per `PROGRAMME.md`.

Cheaper still, and closer to what our own cut actually measured: gate on **their conveyor
count inside a builder's vision** rather than on spend events, published to one store slot
by a **single** writer (last-writer-wins is then safe; the value is a count so it is never
negative — a negative write raises and permanently destroys the unit).

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
