---
tactic: Removal loses to sustain — why a screened turret is not worth shooting
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf
origin: Battlecode 2020 / Java Best Waifu (WINNER), on the "cookie" turtle; corroborated from the attacking side by The High Ground
evidence: documented (the analogue) + arithmetic by tactics sweep 9
transfers: yes — as a NEGATIVE that prices every other answer
---

WHAT IT IS — the canonical statement of what happens when an immobile turret is
surrounded by units that repair it. Java Best Waifu, describing the endgame
turtle they could not break:

> "there was no way of penetrating it: a full army of landscapers would keep the
> Net Guns alive, and we could not drown their Landscapers because of the Net
> Guns."

and, in their game-design reflection at the end of the same document:

> "if several landscapers were surrounding a net gun it was almost impossible to
> destroy unless you crunch it with Drones."

The High Ground record the identical lock from the *attacking* side of a forward
plant — Kryptonite "prioritized surrounding their own net gun over destroying
our HQ, which often led to extended standoffs as we were unable to build drones
and unable to bury their net gun."

**Note the structure**: the turret protects the repairers and the repairers
protect the turret. BC2020's only documented exit was a **displacement** unit —
the drone — that removed the repairers without fighting them.

**Two other leagues state the same rule as an explicit programming requirement.**
Screeps' community combat wiki, on when to shoot at all with a tower:

> "Generally you only want to shoot enemy creeps with towers, if they will damage
> them. Creeps with high heal, damage resistance or support healers, may be able
> to out-heal your towers depending on range. As such, its important to have logic
> in place to account for the damage you can do, vs the healing the enemy creep
> will do in a given tick."

*(wiki.screepspl.us/index.php/Combat — community wiki, not official.)* And Jay
Scott, on the commonest bot failure against an entrenched structure:

> "Don't throw units away against the cannons; build up until you can take them
> out. This is the most basic thing, and yet most bots do it wrong, including
> Steamhammer."

*(http://satirist.org/ai/starcraft/blog/archives/748-cannon-rush-reactions.html —
the author names his own bot as an offender.)* **Three independent fields
converged on "check the damage against the heal before firing, and do not fire
below threshold."** That is the alpha-strike discipline already in
[sweep 2](2026-08-09-sweep-2.md), arriving from a third direction.

**A fourth field states the ranking outright.** Terminal's whole meta is placed
structures, and its community's verdict on the entrenched formation is a single
sentence — kkroep, on beating "maze algos":

> "Successfully setting up a structure like that is a win condition: once it is up
> you win almost guaranteed. Easier to prevent the maze from going up than to
> combat a full maze."

*(forum.c1games.com/t/tips-on-beating-maze-algos/532, via Wayback.)* See
[[funnel-not-seal]] for the rest of that league's answer.

WHY IT MIGHT TRANSFER — because our numbers reproduce the lock exactly, and this
time **we are the attacker**, so the library's 2.2:1 defensive edge runs against
us. Against a planted 25 HP gunner escorted by *k* orthogonally adjacent enemy
builders healing it (+4 HP for 1 Ti, so **4k HP/round for k Ti/round**):

| our removal tool | damage/round | Ti/round | HP/Ti |
|---|---:|---:|---:|
| builder attack (each) | 2 | 2 | 1.00 |
| gunner (dmg 7, reload 1) | 3.5 | 2.0 | 1.75 |
| sentinel (dmg 18, reload 2) | 6.0 – 9.0 | 3.3 – 5.0 | 1.80 |

*(The sentinel range is the standing library ambiguity on whether "reload 2"
fires every 2nd or every 3rd round; both bounds are given rather than picked.)*

**One escorting healer — 4 HP/round for 1 Ti/round — cancels two of our
builder-attackers (4 Ti/round) or roughly a whole sentinel's throughput
(3.3–5.0 Ti/round of ammo).** Two healers beat any single turret we own. There
is no titanium price at which we win this cleanly, because the heal is 4.00 HP/Ti
and our best damage is 1.80 HP/Ti.

And the tail predicted by "removal is a race you win in the first few rounds or
never" is **exactly what the corpus shows**: of the 6,407 enemy gunner/sentinel plants inside
our home band, **58.6% die with a median lifetime of 14 rounds and 41.4% survive
to the end of the game.** That distribution is bimodal, not spread — which is the
signature of a threshold race, not of a grind.

**The consequence is a ranking, not a tactic:**

> Denial and interdiction are priced in **one-off titanium**. Removal is priced
> in a **per-round ammo stream** running against a **per-round heal stream that
> is 2.2× more efficient**. So anything that prevents the plant outvalues
> anything that answers it, and any answer must land **before the escort
> arrives** — which the 14-round median says is the window that already works.

This is also why [[gunner-line-blinding]] is the interesting reactive option and
shooting is not: blinding does not have to out-pace a heal, because a barrier in
the lane is not in a damage race with anything.

**One removal window that other leagues have and WE DO NOT.** Liquipedia's
cannon-rush counters are all priced against a *construction* window — "It takes
one [[Zealot]] or three [[Probe]]s to destroy a Cannon that is being built, if
the Cannon is attacked immediately after it is warped in", and the attacker's
matching discipline "any that are near death should be cancelled to recoup 75% of
the mineral cost of construction" *(raw wikitext, brackets as in source)*. **Our
buildings complete instantly and there is no cancel and no refund.** So the
cheapest removal window in the canonical source does not exist here at all: a
planted gunner is at full 25 HP from the round it appears. This is a genuine
disanalogy and it pushes the answer further toward denial — there is no moment of
weakness to exploit, only a moment of *absence* before the plant.

WHAT WOULD KILL IT — squarely: **if enemy plants are typically UNescorted, the
whole ranking is wrong**, removal is cheap, and shooting the tail is the correct
spend. That is measurable and it is **not measured** — the corpus carries plants
and deaths but nobody has counted enemy builders adjacent to a plant afterwards.
Two secondary caveats: our home turrets are already sited when a plant lands, so
if a plant falls inside an existing arc, removal costs only ammo we would not
otherwise spend; and 58.6% of plants *do* die, so removal manifestly works
somewhere — the question is whether it works on the tail.

BUILDER HOOK — **none as a change; this is a pricing result.** It shares its one
measurement with [[escorted-forward-plant]]:

> For each enemy turret planted in our band, count enemy builder bots
> orthogonally adjacent to it over the 20 rounds after the plant, and cross that
> against survive-to-end. **If escorted plants are the 41.4% tail, denial is
> confirmed as the correct spend and this ranking ships as doctrine. If the tail
> is unescorted, the tail is a siting failure of our own turrets and the answer
> is a turret arc, not a barrier.**

Two hypotheses, one measurement, opposite builds. That is the best shape a
research item can have and it should jump the queue on that ground alone.

Related: [[escorted-forward-plant]] · [[gunner-line-blinding]] ·
[[sentinel-file-stacking]] · [heal arithmetic](../heal-arithmetic-2026-08-09.md)
