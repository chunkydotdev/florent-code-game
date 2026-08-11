---
tactic: A cheap enough rebuild REPLACES defence — the BC2025 runner-up disabled his defensive structures outright because a destroy-and-rebuild loop made losing one nearly free
source: https://battlecode.org/assets/files/postmortem-2025-confused.pdf
origin: Battlecode 2025 confused (2nd, top seed into finals); loop originated by team Gone Whalin
evidence: documented
transfers: partial
---

## WHAT IT IS

Arm D asked for investments that serve two roles. **The runner-up found a third option:
an economic mechanism that made the defensive role UNNECESSARY.**

The loop itself, learned from Gone Whalin, exploits that BC2025 towers spawn with a fixed
paint reserve, so demolishing and rebuilding one converts the expensive currency into the
scarce one:

> *"they used the fact that all towers spawned with 500 paint to continuously destroy and
> rebuild their tower to convert 1000 chips to 500 paint"*

**The defensive consequence, which is the part arm D wants, is stated as a bullet:**

> *"Enemy soldier aggression becomes less relevant as you can simply build a new tower on
> the destroyed tower, replenishing your paint supply."*

**And then the deletion, explicit:**

> *"This also meant that defense towers were no longer necessary to my strategy since I
> wanted to destroy my own towers, so I disabled them."*

**⚠ REFERENT DISCIPLINE, because the adjacent number invites a false claim.** The same
paragraph reports *"Introducing tower flickering dramatically improved my bot’s
performance, resulting in a 70%+ win rate against my submission for qualifiers."* **That
70% is attributed to TOWER FLICKERING as a whole. It is NOT a measurement of disabling
defence towers**, which is reported as a consequence, unmeasured. Anyone quoting the two
together must keep them apart.

## WHY IT MIGHT TRANSFER — against our ruleset

**The primitive is not merely present here, it is cheaper than theirs.** `destroy()` on an
allied building from an orthogonally adjacent tile is **free, no cooldown, unlimited per
turn**. And the global additive scale factor works the same way in reverse: *destruction
removes the contribution*, so a demolished barrier returns its +1% and a demolished
harvester its +5%. **A rebuild is therefore priced at raw titanium plus builder-turns,
with the scale externality netting to zero.**

**Where the argument transfers, and it is narrower than it first looks:**

* **Barriers.** 3 Ti, 30 HP, +1%. Losing one to an enemy builder's 2-damage attack takes
  15 of their builder-turns and 30 Ti of their attack cost, against 3 Ti and one turn of
  ours to replace. **The rebuild is already so cheap relative to the demolition that
  defending a barrier with anything is a mispricing** — this is
  [`ore-tile-denial`](ore-tile-denial.md)'s arithmetic pointed at our own structures.
* **Conveyor line.** 3 Ti, +1%, and our binding failure mode is breakage. **A cheap
  rebuild loop is the correct answer to a broken belt and is a strictly better use of the
  same builder-turn than a turret guarding it.**

**Where it does NOT transfer:**

* **The CORE cannot be rebuilt.** Their towers were fungible; our core is the win
  condition and has 500 HP and no replacement. **No rebuild loop makes core loss cheap,
  and our core dies in 46.3% of games.** The substitution argument therefore covers
  peripheral structures only and says nothing about the thing our defence actually
  protects.
* **Harvesters are 20 Ti and +5%** and sit on fixed ore tiles the enemy can re-attack.
  Rebuilding under sustained pressure is a losing rate race, not a free loop.
* **There is no currency conversion to harvest.** Their loop PAID (chips → paint). Ours
  merely restores; the economic engine that made theirs a strategy rather than a repair is
  absent.

## HOW IT MEETS `DEFENCE_ADMISSION_BAR: kill_round_non_regression`

**This is the one item in the sweep that clears the bar by DELETING defence rather than
adding it, which makes it the cheapest thing here to test.**

* The intervention is a removal, so it cannot add titanium cost, cannot add scale, and
  cannot displace a forward action. **Its kill-round cost is bounded below by zero.**
* Its risk is entirely on the survival side: if the structures we stop defending were
  load-bearing, core-death rate rises.

**What would show it slowed the kill:** essentially nothing can, mechanically — which is
why the bar to watch on this plank is the SURVIVAL bar, inverted. **The correct
pre-registration is: kill round non-inferior (expected: unchanged or better) AND
core-death rate non-inferior.** If core-death rises, the deletion failed on its own terms.

**⚠ And the prior is against a naive version.** s30 measured `barrier-seal-off` at
399/1024 — removing our barrier seal COST us. **So "stop defending structures" is already
partially refuted in our own record and this plank must be scoped to *rebuild instead of
defend*, not to *neither*.** Those are different arms and pooling them would reproduce
exactly the s30 result.

## WHAT WOULD KILL IT

* **The 70% number does not belong to this claim** (see the referent note above). This
  file rests on an unmeasured consequence reported by one competitor.
* **Their rebuild was free of an opportunity cost ours is not.** A BC2025 tower rebuilds
  itself from stored resources; ours needs a **builder standing orthogonally adjacent**,
  and that builder acts XOR moves. **Every rebuild is a forward action foregone**, which
  is the same tempo currency every other file in this sweep is denominated in. A rebuild
  loop that runs continuously is a builder pinned at home — the failure mode of
  [`the-recall-to-defend-was-deleted-for-costing-time`](the-recall-to-defend-was-deleted-for-costing-time.md)
  arriving by a different door.
* **Cross-reference:** the converter mechanism itself is already filed as
  [`destroy-rebuild-converter`](destroy-rebuild-converter.md). **This file adds only the
  defensive-substitution consequence**, which that file does not carry.

## BUILDER HOOK

**Smallest test: a repair-versus-defend switch on peripheral structures only.** When one
of our conveyors or barriers is destroyed and a builder is within a small radius, rebuild
it immediately rather than routing anything defensive to the site. Explicitly EXCLUDE the
core's own ring, which is where s30's `barrier-seal-off` negative lives.

**Diagnostic to run first, off the corpus, no bot change:** how many of our destroyed
peripheral structures are ever rebuilt at all, and after how many rounds? **If the median
is "never", we are already paying the full cost of loss with none of the cheap-rebuild
mitigation, and the plank is a correctness fix before it is a strategy.**
