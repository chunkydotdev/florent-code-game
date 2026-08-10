---
tactic: (D) THE ANSWER TO SUB-QUESTION (D) — two documented cases, and the sharper one is a team that lost its qualifying match because a unit reasoned about a tile OUTSIDE ITS VISION, concluded it was safe to shoot there, and splash-killed its own castle
source: https://github.com/programjames/BC19Bot/blob/master/Battlecode%202019%20Postmortem/Battlecode%202019%20Postmortem.md
origin: team "Double J" (Battlecode 2019, 17th) and "Gone Fishin'" (Battlecode 2023, 2nd)
evidence: documented
transfers: partial
---
WHAT IT IS — the cleanest documented case of a wrong model of the unseen map costing a
match, in the team's own words. Verbatim, from the Double J 2019 postmortem
(raw file `Battlecode 2019 Postmortem.md`, whitespace-flattened; the placing is stated in
the same paragraph, quoted through so the number travels with the story):

> *"In the end though, we lost to **Chicken** due to a sad bug in our code. Our preachers would sometimes fire when they couldn't see any enemies. They chose the place that would deal the least damage to our own units, so normally it was alright. However, in this unfortunate map, our castle happened to be barely outside our preacher's vision radius. Thinking it was safe to shoot there, our preacher splash-damaged our own castle, killing it off and causing us to lose the match. We ended up placing 17*th*, barely missing the final tournament"*

**Note the exact mechanism, because it is not the obvious one.** The bot did not crash and
it did not query illegally. It ran a *minimisation over friendly damage* across candidate
target tiles, and the tile it chose scored best **because the friendly unit standing there
was invisible and therefore contributed zero to the objective**. Unseen was scored as empty,
and empty scored as safe.

The second case is a wrong *symmetry* assumption, from "Gone Fishin'" (2nd, 2023):

> *"Before Sprint 1, we assumed a rotational symmetry, as all three maps up for scrimmages were rotationally symmetrical. This decision was due to time constraints and eventually backfired quite heavily in Sprint 1. We immediately implemented a MapRecorder after Sprint 1."*

SPAARK (HS 1st, 2025) reports the same class of bug surviving undetected because nothing
consumed it — *"Up until Sprint 2, symmetry detection was actually broken, but we didn't use
symmetry info so it didn't matter."*

WHY IT MIGHT TRANSFER —

- **We have the exact same objective-function shape, and worse blast geometry.** Loki's
  offensive planks pick tiles by scoring. Any scoring loop written as
  `sum(damage_to_friendlies(t) for t in candidates)` over tiles it cannot see returns 0 for
  the fog and therefore *prefers* the fog. **The bug is not in the query, it is in the
  aggregate**, so every guard in this sweep — the mask, the catch-all, the tri-state — would
  have passed it clean.
- **The Gone Fishin' case is the pre-mortem for our own symmetry plank.** It is the same
  team, in the same document, that then built the MapRecorder; the sequence was *assume,
  lose, then measure*. Our [symmetry plank](symmetry-is-the-only-free-information-about-the-unseen-map.md)
  proposes an assumption about our map pool that nobody has enumerated yet. **This is the
  documented price of skipping that enumeration.**
- **The SPAARK line is the argument for our standing instrument rule in someone else's
  words.** A symmetry detector nothing reads is a constant column; it validated nothing for
  two sprints and they said so.

WHAT WOULD KILL IT —

- **Our units have no splash damage.** A builder's attack is 2 damage to one orthogonally
  adjacent building; gunners and sentinels fire lines. So the *literal* Double J failure —
  area damage landing on an unseen friendly — cannot happen to us in that form. What
  transfers is the **scoring-over-fog** pattern, not the weapon.
- **Sentinels are the place it could bite, and that is inference, not documented.** A
  sentinel's line shot *"ignores obstacles"* at r²=32, which exceeds a builder's r²=20
  vision. **A sentinel can therefore hit tiles no builder of ours has ever seen.** Whether
  our line-of-fire scoring already accounts for friendlies in that band is a question about
  our code, not about this source, and I have not checked it. Marked as my inference.
- **Both cases are single anecdotes with no counterfactual.** Double J's own framing is
  *"a sad bug"*, not a strategic finding. Do not price it.

BUILDER HOOK — a falsifier, not a feature. Add one counter to the standing unrated leg:
**friendly-fire and self-damage events, and separately, actions whose chosen target tile was
NOT in the acting unit's vision at decision time.** If the second counter is not zero, we
already have this bug and did not know. That is a strictly cheaper test than reasoning about
whether we have it, and it produces a number either way.
