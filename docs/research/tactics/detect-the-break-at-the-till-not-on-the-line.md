---
tactic: (C) THE ANSWER TO THE DETECTION QUESTION — nobody inspects the infrastructure. They watch the INCOME, and a halving against a moving average is the alarm
source: https://raw.githubusercontent.com/openttdcoop/ai-cluelessplus/master/connection.nut
origin: CluelessPlus (Zuu), OpenTTD NoAI competitive AI; corroborated from the opposite direction by the Factorio wiki (https://wiki.factorio.com/Tutorial:Main_bus) and Mindustry's own in-game stat disclaimer
evidence: documented
transfers: yes
---

WHAT IT IS — sub-question (C) was the one my brief said I *"most want and least
expect"*. It has an answer, it is in a competitive AI, and it is eleven lines.

**CluelessPlus never asks whether its road is still connected.** It asks whether
the route is still earning, and if the answer is no it runs the full repair
pathfinder:

> *"// Try to repair road connections from time to time"*

> *"mean_income < 30 ||"*

> *"(long_time_mean_income > 0 && income < (long_time_mean_income / 2)) ||"*

> *"// Repair the connection if it is broken"*

The baseline it compares against is an exponential moving average maintained on
the same route:

> *"this.long_time_mean_income = (this.long_time_mean_income * 9 + income) / 10;"*

**Two guards stop the alarm oscillating**, and both are as important as the trigger.
A rate limiter:

> *"this.last_repair_route + 30 * 3 > AIDate.GetCurrentDate(); // repaired in the last 3 months"*

and a deliberate damping of the baseline after a successful repair, so the alarm
cannot immediately re-fire against a memory of the healthy past:

> *"this.long_time_mean_income = this.long_time_mean_income * 7 / 10; // Fake a reduction of long time mean in order to prevent or make management hell less likely to happen."*

**And the corroboration from the other side is the reason the "at the till" framing
matters rather than "somewhere downstream".** The Factorio wiki states outright
that inspecting the line is not a test — the referent of *"this"* is the "fake"-bus
described in the preceding sentence, which is quoted here so the demonstrative is
anchored:

> *"When one doesn't have enough production to saturate a belt (or splits it into more) then this can be called a "fake"-bus as it can not be saturated."*

> *"This is especially deceiving when the item isn't moving and all belts have filled up as these belts can't carry the amount they lead one to believe they can."*

**A full belt and a working belt look identical.** Mindustry declines to give a
trustworthy throughput number at all — *"stat.itemsmoved.info = Throughput is often
not linear and tied to FPS/TPS."* And Factorio, which ships **17** named alert
types including `train_no_path` and `pipeline_overextended`, ships **none** for
belts:

> *"Available alert types are: entity_destroyed, entity_under_attack, not_enough_construction_robots, no_material_for_construction, not_enough_repair_packs, platform_tile_building_blocked, turret_out_of_ammo, turret_fire, custom, no_storage, train_out_of_fuel, train_no_path, no_platform_storage, collector_path_blocked, unclaimed_cargo, no_roboport_storage, and pipeline_overextended."*

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **The observable is our first tiebreak key.** Titanium delivered to the core is
  what decides ~94% of round-1000 games, and it is the exact quantity a break
  suppresses. **We are already required to care about the number that is also the
  diagnostic.**
- **It fits the store.** An EMA of delivered titanium is one small non-negative
  integer, updated by one writer (the core), read a round later by everyone. Every
  measured hazard of our 16-slot store — last-writer-wins, one-round buffer, the
  negative-write raise — is harmless for that.
- **It is the only detector in this sweep that needs no map walk, no vision, and no
  per-tile bookkeeping**, which is why it survives our 10 ms budget where the
  structural checks are borderline.
- **The two guards translate directly.** Our version of *"repaired in the last 3
  months"* is a round-count cooldown; our version of the baseline damping is
  mandatory, because after a repair the EMA still remembers a healthy economy and
  would re-trigger every round.

WHAT WOULD KILL IT —

- **⚠ Income falls for reasons other than breakage, and the author says so in his
  own code**: *"If no action is taken, this will lead to the AI thinking that the
  connection might be broken as the mean income will dip."* For us the confounders
  are worse and constant: an enemy killing a harvester, ore exhausting, our own
  spending, and the passive 10 Ti every 4 rounds. **This detector fires on "the
  economy got worse", not on "the network broke", and it cannot distinguish them.**
  Its response has to be something that is safe to do when the diagnosis is wrong.
- **It is slow by construction.** An EMA with weight 9:10 needs many rounds to
  halve. A corked line stalls immediately and stays stalled; the alarm arrives long
  after the damage. **It is a good backstop and a poor first line** — pair it with a
  local check, do not use it alone.
- **One AI in seven had it.** Leg 1 examined seven OpenTTD AIs and only CluelessPlus
  detects breakage economically; PathZilla — the graph-theoretic networking AI you
  would most expect to — has **no post-build breakage detection at all**. So this is
  one author's idea, not a field consensus.
- **The competition table is suggestive and nothing more.** In a solo, one-seed
  benchmark (*"They were all competing alone"*), CluelessPlus v37 finished with
  *"356/ 356 100%"* served stations against NoCAB v499's *"1,022/2,145 48%"* on
  *"392,145"* road pieces. **The organiser's own caveat is attached:** *"The x value
  is probably artificially inflated for some AIs."* One seed, one run, no controls,
  versions differing in far more than their detection logic. **Do not read it as
  evidence that the detector caused the difference.**

BUILDER HOOK — free, and it is an instrument before it is a plank: have the core
maintain an EMA of delivered titanium per N rounds in one store slot and `print()`
it. **Then look at the replays of games we lose on the tiebreak and see whether the
break is visible in that series before round 1000.** If it is not visible, this
whole idea is dead for us and we have learned it for the price of a log line.
