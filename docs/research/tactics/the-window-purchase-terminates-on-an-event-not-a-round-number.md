---
tactic: Every defensive purchase in the field terminates on an EVENT, never on a round number — and the one bot that used a round number used it only as an OR-clause backstop
source: https://battlecode.org/assets/files/postmortem-2020-confused.pdf
origin: Battlecode 2020 confused; Battlecode 2025 Just Woke Up (winners); Jay Scott (Steamhammer); Terminal 2023 Lostkids (3rd, APAC)
evidence: documented
transfers: yes
---

## WHAT IT IS

Sweep 24 asked arm A as: what did they buy, and for how long? **The "how long" half
came back with one shape across four independent leagues: the defensive purchase is
scoped by an EVENT that ends it, and the event is an artefact you can see.**

| source | what was bought | terminated by |
|---|---|---|
| Jay Scott / Brood War | one sunken colony | *"a sunken to tide yourself over until your spire finishes"* — **the tech building completing** |
| Just Woke Up (BC2025) | tower spawns moppers instead of expanding | *"whenever they sensed enemy soldiers in range"* — **the enemy leaving the sensor** |
| confused (BC2020) | nothing — the reverse: a surcharge SUPPRESSING defence | *"our rush miner signals that the rush is over when our design school is destroyed"* — **the forward building dying** |
| Lostkids (Terminal) | the wall entrances closed | *"depending on whether the algorithm is attacking and whether the enemy is attacking"* — **two live booleans, re-evaluated every turn** |
| confused (BC2025) | a rebuilt defence tower on an attacked site | *"only happen if there were still"* … *"enemy units around"* — **a current look, after a remembered-attack rule overbuilt** |

**The single round-number in the whole set is confused's, and it is an OR-clause, not the
condition:** *"if it's still before round 250 and the rush isn't over"*. The round number
is a **backstop on a state that is otherwise event-driven** — and note it bounds the
suppression of defence, not the purchase of it.

**The failure mode when the terminus is a memory instead of a look is documented in the
same corpus, by the runner-up, who caught it mid-season.** confused (BC2025) built a
marking system so that a destroyed tower's site would be rebuilt as a defence tower:
*"Then if this tower was destroyed, a soldier would come to it and see the mark and build
a defense tower, and this implementation was able to build defense towers in previously
attacked areas."* The rule keyed on a REMEMBERED attack. His fix added a present-tense
condition — the flattened PDF injects a page number and a figure caption into the middle
of the sentence (*"if there were still 8 Figure 10: Tower marks enemy units around"*), so
the two halves are quoted separately: *"Eventually I changed it so that this would only
happen if there were still"* … *"enemy units around, as defense towers were being
overbuilt. This change helped a lot when the center area was very contested."*

## WHY IT MIGHT TRANSFER — against our ruleset

**Our programme's window is stated as a round range (r150–250) and the field says that is
the wrong variable to branch on.** The library already carries the general form twice —
[`branch-on-a-milestone-not-a-round-number`](branch-on-a-milestone-not-a-round-number.md)
and [`retract-the-target-only-on-a-look-not-on-a-clock`](retract-the-target-only-on-a-look-not-on-a-clock.md)
— and this is the third independent arrival, now specifically about DEFENSIVE spend. The
convergence is strong enough to treat as the default shape.

**The events available to us are cheap and already in the Controller.**

* **`get_hp()` on the core, sampled by the core itself.** A drop since last round is the
  only zero-cost proof of an attacker in contact. `bots/_v135loki18/main.py:176-178`
  already computes an HP delta, but the block is marked core-only
  (`# --- Core-only accounting ---`, `:95`), so it is a CORE arming signal and is not
  available to a raider.
* **`get_nearby_units(dist_sq)` filtered by `get_team()`** — a live look, no memory.
* **One store slot holding "our forward plant is alive"**, written by whichever unit can
  see it. Last-writer-wins, one-round buffer, no read-increment-write — the one idiom
  `store-semantics-2026-08-09.md` shows survives our buffered store.

**The disarm condition is the part that matters and the part we would get wrong.** All
five field cases disarm on the ABSENCE of the trigger, not on a timer running out.
`arm-and-disarm-on-different-thresholds.md` is the hysteresis fix that keeps that from
thrashing; `defence-recall-oscillation.md` is what happens without it.

## HOW IT MEETS `DEFENCE_ADMISSION_BAR: kill_round_non_regression`

**This is the mechanism that makes the bar SATISFIABLE rather than merely testable.** A
defensive behaviour armed on a round range is live for 100 rounds whether or not anything
is attacking us, and every round of it that fires with no attacker present is pure
kill-round regression with no survival return. **An event-armed version is off by
construction whenever there is nothing to defend against, so its expected cost to the kill
is bounded by the frequency of the event.**

**What would show it slowed the kill anyway:** the treatment's median kill round rising
despite the arming rate being low — which would mean the DISARM is broken (we latch on and
never let go), not the arm. **The diagnostic to print beside the bar is therefore
`fraction of rounds the defensive branch was armed`.** If that number is high and the kill
round moved, the terminus is the bug; if the number is low and the kill round moved, the
plank itself is expensive.

## WHAT WOULD KILL IT

* **`confused`'s round 250 is not our 250.** Theirs bounds a rush-priority surcharge in
  a BC2020 game that ran far past it — their own postmortem discusses behaviour *"after
  round 2700"* — so their 250 is an EARLY-GAME marker; ours is the whole kill window. **Coincidence of integers is not
  evidence and must not be quoted as such.**
* **An event terminus needs the event to be OBSERVABLE, and ours is fog-limited.** Our
  core's vision is r²=36. An attacker that damages a forward structure outside every
  friendly unit's vision produces no event at all, and the plank silently never arms.
  A round-range fallback may be needed *precisely* as confused used one — as an OR, not
  as the condition.
* **Five cases, four leagues, all anecdotal.** No one A/B-tested event-arming against
  round-arming. Under `PROGRAMME.md` point 6 this prioritises a shape and retires nothing.

## BUILDER HOOK

**Smallest test, and it is a diagnostic before it is a plank:** instrument the incumbent
to record, per round, (a) whether any enemy unit is within the core's vision and (b)
whether any defensive build was made that round. **Cross-tabulate.** The cell
"defensive build made, no enemy visible" is the volume an event terminus would delete,
and its size decides whether this is worth a leg at all. Zero bot behaviour change, one
counter, readable off our existing corpus.
