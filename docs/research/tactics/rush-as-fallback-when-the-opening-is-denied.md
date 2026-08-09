---
tactic: Rush as the FALLBACK branch when the economic opening is denied — not as a plan
source: https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf
origin: Battlecode 2025 / The Kragle (finalists)
evidence: documented
transfers: yes
---
WHAT IT IS — The Kragle's opening was not "rush" or "eco". It was an economic
opening with a rush **fallback fired by a scouting result**. Verbatim, and the
whole passage matters because the trigger is the point:

> *"Each tower spawns 2 soldiers. The first priority of the soldier pair is always
> to capture an "uncontested" ruin. Until the soldiers finished the first ruin,
> they were in "opening mode." However, in the case that the soldiers only found
> ruins that were "contested," they would rush."*

And they state the theory explicitly:

> *"This is theoretically the perfect scenario for rushing since the best counter
> to rushing is to capture a ruin as fast as possible. However, if every nearby
> ruin is contested, rushes become stronger since it is more difficult to capture
> ruins."*

Referent note: *"they"* = the soldier pair spawned by each tower; *"contested"* /
*"uncontested"* is their own term for a ruin (build site) an enemy soldier is
also near. Result, verbatim: *"This opening strategy was wildly successful on the
ladder."*

WHY IT MIGHT TRANSFER — This is the only documented commit rule in the whole
sweep that is **cheap, local, and computable in the first 20 rounds**, and it
inverts the usual framing: the rush is not what you do when you feel aggressive,
it is what you do when **the economic branch has no cheap move left**. Our exact
analogue is ore. Harvesters can ONLY be built on `Environment.ORE_TITANIUM`, ore
is a small fixed symmetric set, and "contested" is directly readable — an enemy
builder bot inside vision of an ore tile we have not yet taken. Because the map
is symmetric, a contested near-ore reading is also evidence the enemy is
committed forward and therefore **not** sitting on their core. The trigger costs
one vision scan, no new units, and no store slots.

Note the second sentence is a statement about MAP DENSITY, not about the
opponent: rushes get stronger when the defender cannot develop fast. Ore-poor
maps are our version of "every nearby ruin is contested".

WHAT WOULD KILL IT — (a) If our near-ore is essentially never contested by r20 in
the corpus, the branch never fires and the file is dead weight; that is a corpus
query, not a bot change. (b) Kragle's game let a soldier both build economy and
attack, so the fallback cost them nothing — our builder bot can also do both, but
our *damage* comes from immobile turrets that must be paid for and placed, so our
fallback is not free the way theirs was. (c) Their trigger resolved at ~round 17;
ours resolves whenever a builder first reaches contested ore, which on a 30x30
map may be r40+, eating a sixth of the 250-round window.

BUILDER HOOK — Corpus query FIRST, no bot change: for each ladder game, at r20 /
r30 / r40, count ore tiles within our starting quadrant that have an enemy builder
within vision. Cross-tabulate against our own core-kill share. If contested-ore
games already show a higher kill share, the trigger is pre-validated and the
plank is a one-branch change; if they show a lower one, this is the cheapest
possible refutation of the whole fallback idea.
