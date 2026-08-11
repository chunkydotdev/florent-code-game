---
tactic: NEGATIVE — the one league where a top tier adopted a dedicated defensive structure did so because the DESIGNERS made it pay income. Our turrets pay nothing and consume the currency that buys the kill, so their adoption story does not transfer.
source: https://battlecode.org/assets/files/postmortem-2025-confused.pdf
origin: Battlecode 2025 — confused (2nd), Just Woke Up (winners), om nom (3rd)
evidence: documented
transfers: no
---

## WHAT IT IS

Arm D asked who had dual-purpose defensive units. **The clearest case in the corpus is
dual-purpose by DESIGNER FIAT rather than by player ingenuity, and reading it as a
tactic would be a mistake.** BC2025's defensive structure earns money for defending:

> confused (2nd): *"Defense Tower: High damage output, generates chips upon attacking
> enemy units."*

> Just Woke Up (winners), in their own unit list, *"Defense Tower"* / *"Shoots enemies to
> earn money"* (a bullet glyph and a zero-width space separate the two in the source), and in the loss they learned it from: *"defense towers gain money when they
> destroy enemy units"*

**So in BC2025 a defensive emplacement is not a pure tempo loss — it is an economic
structure that happens to shoot, and its opportunity cost against a money tower is a
difference of income rates rather than income versus nothing.**

**And that is precisely the axis on which the field decided against it anyway.** The
baseline across the top tier was ZERO:

> om nom (3rd): *"There are also Defense Towers, which we did not use (but maybe should
> have)."*

> om nom again, on why their income solver worked: *"(not building Defense Towers helped)"*

> confused (2nd), after his rebuild loop made structure loss cheap: *"This also meant that
> defense towers were no longer necessary to my strategy since I wanted to destroy my own
> towers, so I disabled them."*

**Only Just Woke Up shipped them, under three simultaneous conditions with a hard cap of
two** — filed as
[`cap-the-expensive-emplacement-and-gate-it-on-a-choke`](cap-the-expensive-emplacement-and-gate-it-on-a-choke.md).
**Even WITH a designed income channel, the equilibrium in a strong field was two of them,
gated, or none.**

## WHY IT DOES NOT TRANSFER — and this is the load-bearing part

**Run our entity list against theirs and the second channel is simply absent.**

* **Our gunner and sentinel produce no titanium, no ammunition and no units.** They are
  buildings that consume.
* **They consume the SAME pool the kill is paid from.** There is one resource. A gunner
  fires 4 ammo per shot and a sentinel 10, and the only source of ammunition is the core
  converting global titanium 1:1 — the same titanium that buys builders, conveyors,
  harvesters and the raid's own barriers. **We start at 0 ammo with no passive ammo
  income.** So a home turret is a standing claim on the offence's budget every time it
  fires.
* **They also tax every future build.** Each gunner or sentinel adds **+0.20 to the single
  global additive team scale factor**, inflating the cost of every subsequent build of
  every type — including the harvester line. **A BC2025 defense tower's opportunity cost
  was one money tower's income; ours is a permanent multiplier on everything.**
* **And the one channel that might have paid is closed by the engine.** Destroying enemy
  buildings **lowers their scale**, i.e. helps them
  (`engine-guard-matrix-exploit-hunt-2026-08-10.md`), and pushing resources into the enemy
  core **credits them**. There is no defensive structure in our ruleset with a second
  positive channel of any kind.

**⇒ The BC2025 adoption story is unavailable to us. Any argument of the form "the winners
used defensive structures, so we should" imports a unit that paid for itself and lands it
on a unit that cannot.** The transferable part of BC2025 is the GATING RULE, already
filed; the adoption itself is not evidence about our ruleset.

## HOW IT MEETS `DEFENCE_ADMISSION_BAR: kill_round_non_regression`

**It fails, and it identifies the precise reason a home turret is the hardest defensive
plank to clear the bar with.** Three separate kill-round channels, none of which a short
measurement window will see:

1. the titanium spent on the build,
2. the titanium converted to ammunition for every shot it takes,
3. **the +20% scale, which raises the price of every later build for the rest of the
   game** — a cost that grows with how long the game runs and is therefore *largest
   exactly in the games we most want to shorten*.

**What would show it slowed the kill:** median kill round with `get_scale_percent()` at
r150 / r250 and cumulative `convert_ammo` volume printed beside it. **If a turret arm's
scale is higher at equal harvester count, the tempo cost is already proven and the kill
round is a lagging confirmation.**

**⚠ This does NOT contradict s30's `home-turrets-off` result (433/1024).** That measured
REMOVING what we already ship and it came back a real negative — our current turrets are
paying. **This file is about the ARGUMENT FOR MORE, and it says the BC2025 evidence
cannot supply one.** The two are compatible: a dose can be simultaneously worth keeping
and not worth increasing, which is the whole content of Jay Scott's "1 sunken, not 5"
(see [`static-defence-must-name-what-the-safety-bought`](static-defence-must-name-what-the-safety-bought.md)).

## WHAT WOULD KILL IT

* **A second channel we have not noticed.** The claim rests on our turrets having no
  positive externality. `get_attackable_tiles`, `can_fire_from` and the launcher's
  no-team-check throw are the places to look for one — **the launcher in particular is a
  defensive structure with an OFFENSIVE second channel (kidnap), and it costs +10% rather
  than +20%.** That is a genuinely dual-purpose unit in our ruleset and this file's
  argument does not reach it.
* **If ammunition ever became free or passive**, channel 2 disappears and the arithmetic
  changes materially. It is currently 0 passive by rule.

## BUILDER HOOK

**None for the negative.** The forward-looking hook is the exception it names: **the
LAUNCHER is our only defensive-by-position structure with a second channel** — r²=26,
0 ammo, +10% scale, and `can_launch` has no team check and no vision guard. **Any
"dual-purpose defence" work should start there and not on gunners**, and the library
already carries the offensive half
([`launcher-defensive-interception`](launcher-defensive-interception.md),
[`displace-dont-kill`](displace-dont-kill.md),
[`throw-into-prebuilt-cell`](throw-into-prebuilt-cell.md)). What is unwritten is the
defensive half: **a launcher sited to cover our own core's approach throws an incoming
enemy builder backwards for 0 ammo and 1 cooldown — defence and the crash-induction
exploit in the same action.**
