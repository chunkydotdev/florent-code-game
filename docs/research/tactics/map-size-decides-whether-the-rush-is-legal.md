---
tactic: Map size and passability decide whether a rush can work at all — make the commit a runtime toggle
source: https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
origin: Battlecode 2021 / Isaac Liao (wololo) — the most rigorous published account of a pure-rush bot; corroborated by BC2020 The High Ground, BC2023 don't @ me, BC2025 The Kragle
evidence: documented
transfers: yes
---
WHAT IT IS — wololo built the deepest pure-rush bot in the Battlecode record and
then reports, in his own postmortem, that it stopped working — and exactly where:

> *"Other teams like monky began to fortify and improve their politician defenses,
> to the point that they could defeat my rush every time on medium to large size
> maps and any maps with lots of high-passability tiles."*

He also states the economic verdict against a defender who stops over-spending:

> *"the economic theory suggested my rush could have no winning response at all"*

Referent: "my rush" is his muckraker rush; the sentence describes opponents
(BattlePath) who saved conviction instead of pouring it into defence. The fix he
shipped was **not a better rush**:

> *"I let my ECs dynamically transition between rushing and turtling depending on
> context"* … *"betting that I'd be nimble enough to still overwhelm the opponent
> with my rush on small maps, and yet turtle harder than my opponent on larger
> maps"*

and it worked:

> *"my new dynamic strategy stood firmly against several turtling teams which had
> dominated my pure rushing strategy in the past"*

**Three other years say the same thing about map size, independently.** BC2023
don't @ me: *"whichever team won the beginning launcher duel would go on to win
the whole match. This was also bolstered due to the small map sizes"*. BC2020 The
High Ground: *"the devs indirectly nerfed rush through large and hard-to-path maps
in the seeding tournament. Some very strong rush teams were knocked out pretty
early"*. BC2025 The Kragle, as advice to future teams: Teh Devs *"have historically
shown favoritism to teams that prioritize economy-based gameplans (as opposed to
rush/attack based gameplans) by making maps in the finals tournament larger and
slower"*.

WHY IT MIGHT TRANSFER — Our maps run 8x8 to 30x30. That is a **14x area range and
a 3.75x linear range** — a wider spread than the BC seasons above, and it is
already known to matter to us: the library's topic-9 finding is that *"an opening
unconditional on MAP GEOMETRY is a documented failure mode, and our own width
gradient is it."* This file is the cross-league corroboration of that, aimed
directly at the Loki commit decision. `get_map_width()` and `get_map_height()`
are free, available on round 0, need no scouting and no store slot. If Loki
commits at all, the commit should be conditioned on them.

There is a second, sharper reason here than in wololo's game: **our attacker's
arrival cost is superlinear in map size while the defender's is zero.** A builder
bot moves one cardinal step per move-cooldown and cannot move diagonally, so a
diagonal crossing of a 30x30 map is ~58 moves, not 30. The defender pays nothing
to be at home.

WHAT WOULD KILL IT — (a) If our ladder map pool is in fact concentrated at the
small end, the toggle is inert and a constant is fine; that is a corpus query.
(b) A toggle is two strategies to maintain and wololo had a whole season to build
the turtle half — we already have the turtle half (Eir, and `INCUMBENT_FROZEN:
bots/_v115dodge`), but PROGRAMME forbids porting between lines, so Loki would
have to grow its own. (c) The Kragle quote is a warning about **tournament map
pools**, not the ladder — if Florent's organisers do the same thing, a bot tuned
to ladder map sizes is tuned to the wrong distribution at the moment it matters.

BUILDER HOOK — Corpus query, no bot change, and it is the highest-value single
query this sweep suggests: **split our existing core-kill share and time-to-kill
by map area**. If kill share falls with area (it almost certainly does), the
programme's 250-round target is achievable on a sub-population and the number to
report is *the area threshold*, not a global rate. That reframes every subsequent
LOKI verdict.
