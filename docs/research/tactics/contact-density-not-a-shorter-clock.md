---
tactic: (D) WHAT DESIGNERS ACTUALLY ADJUSTED — Halite III shrank the board and RAISED the minimum turn count, and cut a ship-capture mechanic it had already built; the lever was contact density, never a shorter clock
source: https://raw.githubusercontent.com/HaliteChallenge/Halite-III/28b2119/website/learn-programming-challenge/game-overview.md
origin: Halite III (2018), organisers, pinned at commits 28b2119 / 0b3aa29 / a91510c
evidence: documented
transfers: partial
---
WHAT IT IS — Halite III's rules page changed twice in ten days of pre-launch beta.
Both changes are verbatim-quotable at pinned commits, so the before/after is
reproducible rather than remembered.

**Change 1 — a conversion mechanic was built and then deleted.** At `28b2119`
(2018-09-11) the interaction paragraph read, in part:

> *"A ship can be captured and change owners if it is flanked by an opposing
> player’s ships."*

Referent: it is the third of three ship-interaction sentences (collide-and-sink,
inspiration, then capture). At `0b3aa29`, three days later, the word `capture` does
not occur on the page at all (2 occurrences → 0), and it never returns. **A
mechanic that turns a local numerical advantage directly into a permanent swing —
the definition of converting a winning position — was playtested and cut before the
competition opened.**

**Change 2 — the board shrank and the clock got LONGER.** At `a91510c`
(2018-09-21), against `28b2119`:

| | before | after |
| --- | --- | --- |
| map | *"The map is a 2d grid (32x32, 48x48, 64x64, or 80x80)"* | *"The map is a 2d grid (32x32, 40x40, 48x48, 56x56, or 64x64)"* |
| turns | *"The game continues for 300 to 500 turns, depending on the game map size."* | *"The game continues for 400 to 500 turns, depending on the game map size."* |

The 80×80 map was deleted, the ceiling dropped to 64×64, two intermediate sizes
were inserted — and the **floor on game length rose from 300 to 400 turns.** More
turns, on a smaller board.

WHY IT MATTERS HERE — Two independent leagues now say the same counter-intuitive
thing about clocks, and this library was leaning the other way.

Battlecode 2021 halved its round limit and a top competitor reports the kill
condition became unreachable
([`shortening-the-clock-suppressed-the-kill`](shortening-the-clock-suppressed-the-kill.md)).
Halite III's designers, tuning for interaction, moved the clock in the **opposite**
direction from the intuitive one — they lengthened it — and did their real work on
the **map**. That converges with the Battlecode map-pool evidence
([`the-designers-lever-was-the-map-pool`](the-designers-lever-was-the-map-pool.md)):
across three leagues, the instrument designers reach for is **where the game is
played**, not how long it lasts.

Restated as a claim about mechanism: what drives games to a decision is
**contact**, not urgency. That is exactly the shape of our own measured surprise —
sweep 15 found our build production is a near-constant (CV 0.09) and that
**CONTACT is what varies** between our kill and no-kill games. Halite III's
organisers reached the same conclusion from the design side and acted on it by
shrinking the board.

The capture deletion carries a caution rather than a tactic. It is the one
mechanic in this sweep that would have made conversion cheap, and the people who
designed it decided against shipping it. **No rationale is recorded** — the commit
removes the sentence without comment — so any story about *why* is inference. What
is sourced is that Halite III shipped with no way to destroy an opponent on
purpose.

WHAT WOULD KILL IT — Neither change comes with a stated reason. The map and turn
edits are a diff, not an explanation, and reading "they were tuning contact
density" into them is inference — mine, from the direction of the changes. Halite
III is also a **collection race with no kill condition at all**, so calling
anything in it a decisiveness lever is already a stretch; the honest framing is
that these are *interaction* levers in a game where interaction was the design
worry.

And the direction does not automatically import. Our maps are 8×8 to 30×30 —
already at or below Halite III's *smallest* board — so "shrink the map to force
contact" has no headroom here. If contact is our binding variable, it has to be
bought with behaviour, not geometry.

BUILDER HOOK — none in the bot. It sharpens the corpus cut already queued in
[`the-map-decides-whether-anyone-can-win`](the-map-decides-whether-anyone-can-win.md):
cut core-kill incidence by map **area** first, since that is the axis three
independent design teams treated as the live one. If our smallest maps are not
markedly more decisive than our largest, the contact hypothesis is in trouble on
our own data and should be said so.
