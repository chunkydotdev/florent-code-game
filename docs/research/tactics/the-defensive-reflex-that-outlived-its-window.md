---
tactic: FAILURE MODE (arm C) — a spawn-on-sight defensive reflex bought the early window and then ate the whole game's offence, and the author's own diagnosis names all three costs
source: https://battlecode.org/assets/files/postmortem-2019-smite.pdf
origin: Battlecode 2019 smite (3rd in qualifiers; the season's dominant economic bot)
evidence: documented
transfers: yes
---

## WHAT IT IS

The single most complete account in the corpus of a defensive investment that was
correct in its window and catastrophic outside it — written by the team that shipped it.

**The purchase, and it is exactly our r150–250 case:**

> *"While our economy-focused bot won on unit health at the end of the game, it was still
> vulnerable to early game attacks. To mitigate this problem, we added emergency defense
> code to all of our churc inhes and castles."*

*(The `churc inhes` is a `pdftotext` artefact of the source layout, quoted as extracted.)*

**The mechanism — spawn a counter-unit on sight, unconditionally:**

> *"When these units saw enemy units, they would immediately spawn crusaders, prophets,
> or preachers (depending on the type and distance of the enemies)."*

**The verdict, and note that the sentence contains BOTH halves of our admission bar:**

> *"This code allowed us to survive early in the game but had a major unintended
> consequence."*

> *"Especially later in the game, defensive units would be overproduced, either being fed
> into enemy lines, wasting resources and stalling global production, or simply using so
> much fuel to be produced that they could no longer attack."*

**Three distinct costs, and they are three distinct mechanisms:** units *fed into enemy
lines* (bad trades), *stalling global production* (the queue is occupied), and *so much
fuel* that the offence was unaffordable (the resource is gone). **The reflex did not
merely fail to help — it converted the team's economic advantage into nothing.**

## THE TELL, AND THEY CAUGHT IT DURING THE SEASON

Arm C asked specifically whether anyone diagnosed this while it mattered. **smite did,
and the tell was an OPPONENT, not a statistic.**

> *"DOS used a very aggressive, sustained preacher attack strategy, draining our
> resources with emergency defense until we eventually lost castles."*

The referent is the qualifying tournament, where smite lost to DOS twice and placed
third. **The diagnostic signature is specific and reproducible: a single opponent that
loses the material exchange every time and still wins, because the exchange is not what
they are farming.** DOS was not killing smite's army; DOS was making smite build it.

**And the response is the part worth stealing, because it is the opposite of the
instinct:**

> *"instead of tuning to be more defensive against rush bots like DOS, we decided to send
> one prophet scout"*

*(Full clause, for the referent: they sent it on 1v1 maps to sit outside the enemy
castle's attack range and shoot at what it saw — an OFFENSIVE answer to a defensive
leak.)*

## WHY IT MIGHT TRANSFER — against our ruleset

**Our incumbent has this exact shape.** We ship `_heal_core`, `_heal_adjacent`,
`heal_seats` and a `SLOT_UNDER` under-attack latch. Every one of those is a
spawn-on-sight-class reflex: a condition observed at the core diverts a builder-turn to a
defensive action. **The BC2019 failure is not that such a reflex is wrong — smite says
plainly that it worked early — it is that the reflex had no upper bound and no window.**

**Two of smite's three costs have direct analogues and one does not:**

* **The *"stalling global production"* cost transfers hardest.** Our core spawns ≤1 builder per turn
  and a builder acts XOR moves. A defensive action is a turn a raider did not spend
  forward. This is the same currency as the previous file's tempo price.
* **The *"using so much fuel to be produced that they could no longer attack"* cost transfers with an extra sting.** Ours is
  one global titanium pool paying for builds, builder attacks (2 Ti each) AND ammo
  (`convert_ammo` 1:1). A defensive drawdown does not merely compete with the attack; it
  competes with the **ammunition the attack fires**, and we start at 0 ammo with no
  passive income.
* **The *"either being fed into enemy lines"* cost transfers WEAKLY and the difference matters.** Their defensive
  units could be killed in bad trades. Our defensive *builds* are static and our defensive
  *builders* can be killed — but the biggest analogue is worse than a bad trade: every
  gunner or sentinel we build adds **+0.20 to the global additive scale factor
  permanently**, and destroying it does not help the enemy's economy — it lowers OUR OWN
  contribution back. The overproduction tax here is a price increase on everything, not a
  unit loss.

**⚠ The attacker-side reading of this same passage is already in the library**
([`their-defensive-reflex-fires-unconditionally`](their-defensive-reflex-fires-unconditionally.md),
and a partial quote in [`2026-08-09-sweep-1.md`](2026-08-09-sweep-1.md) §3). **This file is
the SELF-directed reading: not "bait theirs", but "we ship one".** They do not overlap and
both should stand.

**⚠ Correction to the existing library, found by this sweep's grep:**
`2026-08-09-sweep-1.md` renders the quote as *"defensive units to be overproduced… wasting
resources and stalling global production"*. The source reads *"defensive units **would
be** overproduced"*. Inside quotation marks, that is a paraphrase — small, but exactly the
class the INDEX's method block exists to catch.

## HOW IT MEETS `DEFENCE_ADMISSION_BAR: kill_round_non_regression`

**It fails it, loudly, and that is why it is filed.** smite's own sentence — *"using so
much fuel to be produced that they could no longer attack"* — is a kill-round regression
reported in words. **A reflex of this class clears the bar only if it carries a CAP and a
WINDOW**, and smite's carried neither.

**The two guards this failure prescribes:**

1. **A hard count cap on defensive responses per game or per contact episode** — the same
   answer BC2025's winners reached independently with *"we have less than 2 defense
   towers"*.
2. **An event terminus that disarms on absence**, per
   [`the-window-purchase-terminates-on-an-event-not-a-round-number`](the-window-purchase-terminates-on-an-event-not-a-round-number.md).

**What would show it slowed the kill, on our instruments:** median kill round rising
*together with* a rise in defensive actions per game. **And the DOS signature is the
cheap early-warning: an opponent against whom our defensive-action count is far above our
median and our win rate is below it.** That is computable off `ladder_games.tsv` joined
to the replay corpus, per opponent, with no bot change — and unlike a kill-round
regression it can be seen in a single matchup rather than needing a panel.

## WHAT WOULD KILL IT

* **BC2019's economy had a fuel cost per SHOT and a unit-health tiebreak.** Both are
  absent here, and both amplified the failure there. The mechanism transfers; the
  severity is not portable.
* **It is a postmortem narrative with no counterfactual.** smite never ran the ablation —
  we have their word that the reflex helped early and hurt late, and no number for either.
* **Our reflexes may already be capped.** `SLOT_UNDER` is a latch, and a latch with a
  release is not the unbounded version. **Grep before pre-registering** — the cheapest
  null available is a leg testing a guard we already ship.

## BUILDER HOOK

**Do not start with a bot change. Start with the DOS detector**, because it is free and
it is the thing smite lacked:

> Per opponent, over our archived games: **defensive actions per game** (heals + home
> builds + barrier placements) against **game share**. Flag any opponent in the top
> quartile of the former and the bottom quartile of the latter.

**A non-empty flag list is a live instance of this failure in our own record.** An empty
one is the other verdict, and the check has then been seen to check. Only after that is a
cap worth tuning.
