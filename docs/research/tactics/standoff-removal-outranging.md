---
tactic: Standoff removal — shoot the planted turret from outside its reply range
source: https://battlecode.org/assets/files/postmortem-2025-confused.pdf
origin: Battlecode 2025 / confused
evidence: documented (the principle) + arithmetic by tactics sweep 9
transfers: partial
---

WHAT IT IS — the plainest statement of the principle I found in any postmortem,
about attacking an immobile defensive structure:

> "Splashers can hit the tower indirectly by sitting just outside their range."

A structure that cannot move has a fixed reply envelope. Anything that outranges
it removes it **for free in risk terms**, however slowly.

**The same principle is the textbook counter to a cannon rush, and it is stated
as a placement rule rather than a targeting one.** Liquipedia's Protoss counters:

> "Once scouted, the defending player should immediately build their own
> [[Forge]] and immediately start building defensive Cannons slightly out of
> range of the opponent's Cannons. The aim is to use defensive Cannons to prevent
> the attacking player from building Cannons within range of any important
> structures."

*(raw wikitext, brackets as in source; liquipedia.net/starcraft2/Photon_Cannon_Rush
— community wiki.)* And Jay Scott gives the same move with an explicit **count
discipline** attached, which is the part worth stealing:

> "Zerg can commonly stop encroachment by building 1 sunken as close to the
> cannons as possible while out of range. **Only make more than 1 if absolutely
> necessary.**"

*(emphasis mine.)* The standoff counter-turret is a *single* structure whose job
is to stop the plant advancing, not a second defensive line.

**And in Terminal the standoff is written into the official starter kit as a
worked strategy** — one where *cheap structures are built specifically to hold
the attacker at the standoff distance*. From Correlation One's own
`python-algo/algo_strategy.py`:

> "Build a line of the cheapest stationary unit so our demolisher can attack from
> long range."

> "Now let's build out a line of stationary units. This will prevent our
> demolisher from running into the enemy base. Instead they will stay at the
> perfect distance to attack the front two rows of the enemy base."

A Terminal competitor states the underlying range fact the same way:
"the demolisher has a range of 4.5 units, which is longer than the range of
turrets (2.5 units, 3.5 when upgraded). So 1 possible strategy would have been to
spawn demolisher(s), build a row of walls to keep the demolisher from advancing
into the range of enemy turrets, and take out the turrets from far."
*(github.com/wowthecoder/citadel-terminal-ai — competitor writeup.)*

**Read across: the standoff is a placement problem, not a targeting one.** Our
sentinel cannot rotate and cannot move, so the "row of walls that holds the
shooter at the right distance" has no direct analogue — but the principle that
you *spend cheap structures to preserve a range advantage* is the same spend
argued in [[funnel-not-seal]].

WHY IT MIGHT TRANSFER — the range table hands us the standoff outright, and it is
the one place our own turret arsenal has a strict dominance relation:

| | vision r² | attack r² |
|---|---:|---:|
| **sentinel** (ours) | 32 | **32** |
| **gunner** (theirs, the measured killer) | 13 | 13 |

A sentinel bearing on a planted gunner at d² between 14 and 32 **cannot be
answered and cannot even be seen** — the gunner's vision radius is its attack
radius. And the sentinel's shot **ignores obstacles** (probed s23: 18 damage
landed through our own builder bot *and* our own barrier), so the escort cannot
body-block it either. This is the cleanest zero-risk removal in the ruleset, and
it sits on top of a measured strength: our home turrets survive better than
anyone's in the corpus.

It is also, specifically, an answer aimed at the **41.4% of enemy plants that
survive to the end of the game** — a tail that by definition nothing else we
currently do is reaching.

WHAT WOULD KILL IT — and this is where it stops being a free lunch:

1. **Standoff removes RISK, not the heal deficit.** Against a 25 HP gunner with
   *k* escorting healers (+4 HP/round each for 1 Ti/round), the sentinel's
   6.0–9.0 HP/round at 3.3–5.0 Ti/round of ammo **beats one healer narrowly and
   loses to two.** The ranking in [[sustained-plant-removal-race]] stands; this
   file only says that *if* you remove, remove from outside. Note the drain runs
   the wrong way even when we win: we spend 3.3–5.0 Ti/round of ammo to force
   1–2 Ti/round of healing.
2. **Sentinels cannot rotate at all** (`machinery-audit`). The standoff shot has
   to have been aimed correctly **before the plant existed**, and plants land at a
   median round of 154 spread p10 11 → p90 547. A mis-aimed sentinel can only be
   destroyed and rebuilt — at +20% scale.
3. The shot is a **single-tile-wide line**. The planted gunner must be exactly on
   that ray, not merely inside r²=32. That is a much smaller target set than the
   radius suggests, and it is the real reason this is not simply "build a
   sentinel".
4. Ammo is the line we are already worst at: we hold more titanium than Ouroboros
   through r200–300 while buying a twelfth as much ammunition. A standoff duel is
   an ammo commitment, which is the resource we have repeatedly failed to spend.
5. It is worth **nothing** against a planted *sentinel* (r²=32 vs our 32 — no
   standoff exists) — but planted sentinels beyond gunner reach are only 7.7% of
   our home builder deaths, so the tactic covers the shape of the problem we
   actually have.

BUILDER HOOK — **not a new build; a targeting rule for sentinels we already own.**

> When a friendly sentinel's action cooldown is 0 and an enemy **gunner** lies on
> its firing line at d² > 13 from itself, fire on the gunner in preference to any
> other target.

That costs one condition in the sentinel branch and no titanium, and it is
directly measurable: enemy-turret lifetime inside our band (currently median 14
rounds for the 58.6% that die, 41.4% surviving to end).

The **count discipline** from Jay Scott transfers unchanged and costs nothing to
adopt: **one** standoff sentinel per planted gunner, not an arc. At +20% scale
per sentinel that discipline is worth more here than it was in Brood War.

The **siting** consequence is the expensive half and should not be taken on this
file's evidence alone: it argues for placing home sentinels so their fixed ray
sweeps the d² 13–29 plant band (the p25–p75 of measured plant distance to our
core) rather than pointing at the enemy core. That is a doctrine change, and it
trades against [[runtime-density-siting]]'s objection that permanent turrets
should not be aimed on transient evidence.

Related: [[sustained-plant-removal-race]] · [[sentinel-file-stacking]] ·
[[gunner-line-blinding]] ·
[turret line blocking probe](../turret-line-blocking-2026-08-09.md)
