---
tactic: When a forward unit is about to be killed, spend it — convert it into a structure on the tile it is standing on rather than walking it home
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
origin: Battlecode 2020, Bagger288 (reported by The High Ground); Battlecode 2020 Bowl of Chowder
evidence: documented
transfers: partial
---

## WHAT IT IS

The High Ground's shout-out section records two teams that answered "this forward
unit is about to die" with a **conversion** rather than a retreat:

> *"who implemented a strategy where their landscapers would self-destruct and be replaced with net guns if they detected they were soon going to get crunched on"*

**Referent check.** The sentence opens *"A final shoutout goes to Bagger288,"* —
"their landscapers" are Bagger288's forward units on the turtle wall; "crunched
on" refers to the drone crunch described earlier in the same document. The High
Ground's assessment follows immediately: *"This would have been a fantastic
counter to us if we hadn't implemented our last-minute turtling."*

The same paragraph records a second, structurally identical trick from a
different team:

> *"who was the only team to successfully implement self-destruction of landscapers in order to create islands to build net guns to break drone walls"*

(referent: *"One more shoutout goes to Bowl of Chowder,"*). Both convert a mobile
unit's remaining value into an immobile emplacement **at the forward position**,
on an event trigger, with no travel.

## WHY IT MIGHT TRANSFER — the ANALOGUE is stronger here, and the LITERAL move is worthless

**The literal move does not port.** Our `self_destruct()` **deals no damage** and
leaves nothing behind; it is a pure deletion. There is no build-on-death.

**The analogue ports and is cheap.** A builder that expects to die this round or
next can spend its action on a **build** instead of a move: a barrier (3 Ti base,
30 HP) or, if the bank allows, a gunner or sentinel on an orthogonally adjacent
tile. The exchange is favourable in a way that is specific to our cost rules:

* The builder's own destruction **refunds its +20%** contribution to the single
  global additive scale, while the structure it leaves adds only **+1%** (barrier)
  or **+20%** (turret). A raider that converts to a barrier and dies has *lowered*
  our scale by 19 points net while leaving a body on the tile.
* A **barrier on an enemy spawn-ring tile is a body that does not need a unit**,
  and it costs 3 Ti at scale 1.0. `CLAUDE.md` records the retention problem
  directly: *"The open margin is RETENTION, not presence."* **A structure retains
  by construction.**
* Under `R1000_IS_DEFEAT`, a forward turret left behind is a lane opener, which is
  the only justification the programme accepts for buying a turret at all.

## WHAT WOULD KILL IT

* **Predicting "about to die" is the hard half, and Bagger288's detector is not
  described** — "if they detected they were soon going to get crunched on" is all
  the source says, reported second-hand by an opponent. `evidence: documented`
  for the tactic, **nothing at all for the predicate.** The nearest usable proxy
  we have is the HP-delta arming in
  [`arm-the-flee-on-an-hp-delta-and-disarm-it-on-absence`](arm-the-flee-on-an-hp-delta-and-disarm-it-on-absence.md).
* **Demolishing enemy buildings lowers THEIR scale**, and by the same rule our own
  forward barrier raises OURS by 1% for as long as it lives. Small, but it is a
  real cost and the +1% applies to every subsequent build of every type.
* A barrier on a tile our own raiders need to walk through blocks **us** —
  builders cannot pass buildings, and this library already holds the
  self-interference case
  ([`the-blockade-blanks-your-own-guns`](the-blockade-blanks-your-own-guns.md)).

## BUILDER HOOK

On the round a raider registers an HP drop while standing on a tile of denial
value, build a barrier on the *adjacent* tile the enemy needs rather than moving.
One condition, one build call, no new state. **Falsifier: if the barrier is
cleared within a handful of rounds it is a 3 Ti tempo tax on us, not on them —
measure rounds-until-cleared before sizing anything on it.**
