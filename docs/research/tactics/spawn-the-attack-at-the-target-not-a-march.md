---
tactic: Plant production next to the enemy base and spawn the attack there — the march is the part that fails
source: https://battlecode.org/assets/files/postmortem-2020-confused.pdf
origin: Battlecode 2020 / Battlegaode (dominant rush), reported independently by confused, The High Ground and Java Best Waifu
evidence: documented
transfers: partial
---
WHAT IT IS — The one rush shape that actually broke bases in BC2020 did not walk
an army across the map. It walked **one cheap scout**, built a **factory next to
the enemy HQ**, and produced the attackers on site. Three independent teams
describe the same thing.

confused, on Battlegaode:
> *"they would make a miner run to the three possible enemy HQ locations due to
> symmetry, and when it found the HQ, it built a design school right next to it,
> which immediately spawned landscapers and buried it"*

Java Best Waifu, describing the same team's mechanism from the receiving end:
> *"in our third game their miner successfully built a Design School next to our
> base"* — and that was the game they lost of three.

The High Ground list it as one of the two strategies of the year: run a miner to
the HQ, build a Design School and perhaps Net Gun, then bury.

WHY IT MIGHT TRANSFER — The transferable idea is not "factory" but **the
attacking asset's cost of arrival must be paid once, in scout-moves, not per
attacker**. Every league in this sweep that killed a base early did it by
converting cheap travel into on-site production; every one that failed (see
`the-attack-that-arrives-too-late-or-at-nothing`) failed in transit. Our version
is the **forward turret plant**: one builder bot walks, and a sentinel built
in place then produces 9 HP/round of damage forever without ever travelling.
`escorted-forward-plant.md` and `runtime-density-siting.md` already carry the
placement half; this file supplies the *why*.

WHAT WOULD KILL IT — And this is the reason it is `partial`, not `yes`. Their
forward building **made units**. Ours cannot: only the core spawns builder bots,
at most one per turn, on its own 12-tile Chebyshev-1 ring. A forward sentinel is
a 40 HP immobile building sitting inside the enemy's kill zone with **no ability
to replace itself or its escort**. Everything the enemy loses to it, they replace
from a core that is right there; everything we lose, we replace across the whole
map. That asymmetry is precisely what `THE FORWARD ROAD IS CLOSED` measured on
three instruments — this file does not reopen it, it explains what the field's
working version had that ours lacks.

Second killer: their scout found the base by testing three symmetries. Ours is
cheaper — the map is symmetric by reflection or rotation, so the core location is
largely computable — but The High Ground record that even a *good* symmetry
routine cost them: *"our rush miner would first run to the middle of the map in an
attempt to determine which of 3 possible symmetries the map was"*, which they call
out as making their rush **worse** when a guess would have been right.

BUILDER HOOK — None new. The prerequisite is already filed: if a forward plant is
ever tried again it must be measured as *damage delivered per builder-round spent
travelling*, and compared against the same builder standing at home healing at
4.00 HP/Ti. If a forward sentinel does not clear that bar it is a donation.
