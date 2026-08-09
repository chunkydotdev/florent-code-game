---
tactic: Ore-tile denial — 3 Ti permanently blocks a 20 Ti harvester
source: https://battlecode.org/assets/files/postmortem-2019-smite.pdf
origin: Battlecode 2019 smite; field-wide by BC 2020; Lux AI resource denial
evidence: documented
transfers: yes
---
WHAT IT IS — occupy or block the opponent's resource sites rather than fighting
their army. smite: "if we can control even one resource cluster on the enemy side
of the map, that creates an asymmetry in resource incomes that should, with
optimal play, lead to a win" — they sent harassers by turn 4-6 and **halted their
own castle production for a turn** to afford them early enough. By BC 2020 it was
universal: "every top team, no matter what their strategy, now had a drone
harass."

WHY IT MIGHT TRANSFER — harvesters can ONLY be built on ore tiles, and ore is a
small fixed set (hive: 12 tiles, exactly symmetric). A 3 Ti barrier on an
enemy-side ore tile denies a 20 Ti harvester plus its whole delivery stream, and
because `destroy()` is allied-only they must chew 30 HP at 2 dmg/2 Ti to clear
it. Denying harvesters also holds their cost scale down less than it holds their
income down.

WHAT WOULD KILL IT — reachability. If their ore sits inside their turret
coverage, the builder that plants the barrier dies on the way, and our own
measurement says a bot in enemy territory after r150 lives ~6 rounds. **This is
an EARLY tactic on our timeline, not a late one.**

BUILDER HOOK — we already know every map's ore layout from the bot's own map
book (`known_map_for`). Cost the walk: which enemy-side ore tiles are reachable
before r150 on each map?
