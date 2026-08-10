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

---

> ### ⚠ CAVEAT ADDED 2026-08-10 (research arm) — **`THE FORWARD ROAD IS CLOSED` IS DEMOTED. DO NOT REASON DOWNSTREAM OF IT AS SETTLED.**
>
> This file treats that conclusion as established. **Two things have happened to it
> and neither had propagated here:**
>
> 1. **Its evidentiary floor did not reproduce.** `INDEX.md` records that the
>    `+11.4 / +16.6 / +22.3pp` home-defence advantage — the floor under the
>    conclusion — **does not reproduce on v102**: Eir home 78.3% vs field 62.0%
>    (+16.3pp) but **v102 71.5% (n=439) vs 81.5% (n=520) = -10.0pp**, and paired
>    within opponent the gap **narrows or flips in 5 of 8**. The index's own words:
>    **"n=439 supports 'does not reproduce', NOT 'refuted'"**.
> 2. **A field-wide cut now runs against it.** `../bisons-fast-kill-2026-08-10.md`:
>    **2+ forward in-range sentinels standing by r45 takes core-kill-by-r100 from
>    3.6% to 23.1% across the field (n=17,235/804, p=1.9e-12)**, with a powered
>    placebo firing null. The Bisons reach that position in **42.3%** of games and
>    convert **47.5%**. **The forward road is demonstrably open for other teams.**
>
> **The defensible statement is narrower than the one in this file: OUR forward road
> was closed on OUR instruments, in the Eir era.** That is not "the forward road is
> closed", and the two were being used interchangeably.
>
> **Under D12** (Magnus, 2026-08-10 - *"test everything in unrated games before we
> refute them"*) **an archive-sourced closure cannot retire a road at all.** This one
> goes to the **bottom of the queue, not off it.**
