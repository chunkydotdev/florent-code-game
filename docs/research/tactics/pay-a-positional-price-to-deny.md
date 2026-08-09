---
tactic: PAY A POSITIONAL PRICE TO DENY — choose a deliberately suboptimal base placement to sit on the opponent's resource, then win the endurance contest; and the documented counter is an opponent who reroutes flexibly
source: https://www.kaggle.com/competitions/lux-ai-season-2/discussion/407982
origin: Lux AI Challenge Season 2 (2023) / ry_andy_, 1st of 646
evidence: documented
transfers: partial
---
⚠ **TIER 2.** This source was read through a text proxy (the local artifact carries
the proxy's `Title:` / `URL Source:` / `Markdown Content:` header) and was **not
diffed against Kaggle's original HTML**. Every string below verifies verbatim against
the local bytes; what is *not* established is that the local bytes are byte-identical
to what Kaggle served. Treat as strong but one step removed from a primary.

⚠ **GLYPH NOTE, and it is the per-string trap in the flesh.** In the first quote
below, `opponent’s` uses a **CURLY** apostrophe, while other apostrophes in the same
file are ASCII. An ASCII-apostrophe grep of that sentence returns a clean, confident
FAIL. Checking glyphs per *document* rather than per *string* would have cut a true
quote from the winner's own writeup.

WHAT IT IS — The winner of Lux S2 (646 teams) chose where to put his base by asking
what it would deny rather than what it would produce:

> *"I figured it might be worth purposely choosing an otherwise suboptimal factory spawn position if it meant I was well-positioned to deny ice to an opponent’s factory, while using light water transporters to outlast them."*

The strategy is named *"ice conflicts"* in the source. He implemented it by weighting
placement toward proximity to the ice around an **opponent's** factory, added
*"a pair of light \"blockade\" units to block opponent water transporters"*, and
reports it won sprint 2 outright.

**Two things make this more than "deny the enemy resources".** First, the price is
paid **up front and in position**, not in units — he accepts a worse economy
permanently in exchange for a permanent claim on the contested tile. Second, the plan
has an explicit **endurance clause**: *"while using light water transporters to
outlast them"*. Denial without a plan to survive the shortage you have created is not
this tactic; the transporters are what make the suboptimal position survivable.

**AND HIS OWN CONVERSION FAILURE IS PART OF THE FINDING.** The quote carries the
demonstrative *"This"*, so the sentence establishing its referent is quoted with it:

> *"Interestingly, this did not work at all against flg, who tended to use heavies to flexibly move ice around the map wherever it was needed. This resulted in very few factory kills, and I just had to live with the otherwise suboptimal factory placements."*

Referent: *"This"* is **his ice-conflict strategy failing against flg, an opponent who
rerouted resources flexibly**, stated in the preceding sentence. He adds
*"This weak matchup really hurt my final score."* So the winner of the competition
records that his denial strategy, against a flexible opponent, produced **the
positional cost with none of the benefit** — he paid for a bad base and got no kills
for it.

WHY IT MIGHT TRANSFER — The **shape** transfers cleanly and the *mechanism* does not.

Shape: we make one irreversible, high-leverage placement decision early — where our
first harvesters and forward turrets go — and the library records that we currently
make it on economic grounds alone, siting sentinels at median **d²=18 from our own
core, 30.7% forward**, against comparable builders at **d²_own 53–181, 63–93%
forward**. ry_andy_'s claim is that on a symmetric map the *contested* tile is worth
more than the *productive* one, and that you should knowingly buy the worse economy
to get it. On our maps — symmetric by reflection or rotation, 8×8 to 30×30 — there is
always a mirrored contested ore cluster, and it is always equidistant.

Mechanism: it does **not** transfer, because his denial killed factories and ours
cannot kill anything (see
[`the-kill-mechanism-was-starvation-not-hp`](the-kill-mechanism-was-starvation-not-hp.md)).
Our version buys tiebreak key 1 suppression and key 2 attrition, not a win.

The failure half transfers *better than the success half*, and this is the part
worth carrying forward. **Denial fails against an opponent who can reroute.** Our
opponents reroute trivially: conveyor networks are rebuildable at 3 Ti a tile, ore
clusters are plural on most maps, and a builder bot can re-site a harvester in a few
rounds. So the flg-shaped counter is the *default* here, not the exception. That is a
strong prior that positional denial underperforms against a competent field — from
the winner's own account of the games he lost.

WHAT WOULD KILL IT — Three things:

1. **Map class.** On a map with one contested ore cluster the tactic is live; with
   three or more, flg's counter is free. The library already flags that incidence
   experiments must be blocked on map class or they measure the map. **This tactic is
   more map-sensitive than most and should never be A/B'd unblocked.**
2. **Our cost scale is ONE GLOBAL ADDITIVE FACTOR.** A denial emplacement is not just
   a worse harvester; every builder and turret it needs raises the price of everything
   we build afterwards. ry_andy_'s cost was a worse spawn tile. Ours is a worse spawn
   tile **plus a permanent tax on the rest of the game.**
3. The measured fact that **our forward road is closed** on three instruments. A
   contested-cluster claim is a forward emplacement by another name, and it inherits
   every reason forward emplacements fail for us.

BUILDER HOOK — Corpus, not bot: **in our own replays, cut core-kill incidence and
r1000 tiebreak margin by the number of distinct ore clusters on the map.** If the
single-cluster class exists and behaves differently, the tactic has a home and the
gate is map-shaped. If incidence is flat across cluster count, contested-tile
placement is buying nothing here and this file drops to `no`.
