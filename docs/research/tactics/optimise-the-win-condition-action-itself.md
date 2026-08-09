---
tactic: THE WIN-CONDITION ACTION GETS ITS OWN MICRO — the field's conversion gains came from beating the objective's cooldown and beating congestion from FRIENDLY units, not from winning more fights
source: https://battlecode.org/assets/files/postmortem-2024-cout-for-clout.pdf
origin: Battlecode 2024 / cout for clout (finalist), crediting the technique to Wololo
evidence: documented
transfers: partial
---
WHAT IT IS — BC2024's win condition required physically carrying an enemy flag
back to your own spawn. cout for clout's conversion improvement was not a combat
change at all; it was an optimisation of the *carry*, and the two things it beat
are worth naming exactly:

> *"The movement cooldown for holding a flag is 20."*

> *"A large weakness of bugNav is dealing with multiple robots, leading the flag
> carrier to be blocked by other friendly ducks. Flag passing significantly reduces
> this issue since the flag holder would not need to bugNav through all the ducks;
> it can just pass the flag instead."*

Referent: "this issue" is the friendly-blocking described in the sentence
immediately before — their **own** units obstructing their **own** objective
carrier. The trick works because the game charged the cooldown to the *holder*,
so handing the objective to a different unit reset the effective clock: dropping
and re-picking gave *"a maximum travel distance of 2sqrt(2) as opposed to the
normal sqrt(2) distance"*.

Two general lessons sit under the specific trick. **(1) The bottleneck on
converting was a cooldown attached to a specific unit, and the answer was to
change which unit was doing it.** **(2) A large part of the friction was
self-inflicted** — the attacker's own units in the way.

WHY IT MIGHT TRANSFER — The literal mechanic does not: nothing is carried here,
and there is no objective to hand off. What transfers is that both bottlenecks
exist in our ruleset in measured form, and neither is currently engineered.

**Self-inflicted congestion is real and asymmetric here.** The s23 probes measured
that a **gunner's line is blocked by our own bots and buildings**, while a
**sentinel's line passes through them** (18 dmg landed through a friendly bot *and*
a friendly barrier), and that `get_attackable_tiles()` **ignores occupancy** and
reports the target as attackable in both cases. So a siege built of gunners is
partly blinded by the very bodies that
[the crunch](the-crunch-is-a-rate-race-not-a-damage-race.md) needs on the target's
adjacent tiles, and the bot cannot tell from the API that this has happened. The
existing file [`the-blockade-blanks-your-own-guns`](the-blockade-blanks-your-own-guns.md)
holds the defensive half of this; the offensive half is that **a crunch must be
sentinel-based or it fights itself.**

**The cooldown lesson has a sharper counterpart than it looks.** Our within-round
ordering is fixed by entity id, and ids are assigned by creation order — so *we
choose which of our units acts first by choosing when we build them*. The library
measured the extreme case: post-throw `dwell = 0` in **84.14%** of throws where
`launcher_id < victim_id` against **1.83%** where `launcher_id > victim_id`. That
is BC2024's lesson in our engine's idiom — **who acts first is a build-order
decision, not luck** — and it applies to any within-round race in a crunch: whether
a healer we displaced gets back on the tile before our turret fires, whether our
builder occupies a vacated tile before theirs does.

WHAT WOULD KILL IT — Honesty about the size of the effect. The library's own
calibration on the id fact is that the edge is **real per-event and has never been
shown to accumulate into an outcome edge**: seat-based win rate and
`core_kill_share` are both null (p = 0.48 and p = 0.29,
`../per-opponent-gates-v102-2026-08-09.md`). **The earlier citation for this — 2,715
ladder games at p ≈ 0.37 / 0.80 — is WITHDRAWN (s26): it was computed off
`ladder_games.tsv`'s `seat` column, which holds the WINNER's side, not ours. The
conclusion is unchanged; only its evidence is replaced.** So "choose
your ids" is the right explanation for an individual race in a decode and a poor
justification for a plank. The congestion half is the load-bearing one; the
ordering half is a tie-break on implementation details, not a strategy.

The other limit: BC2024's carry had a **20-turn** cooldown, an enormous number
that made the optimisation worth a postmortem section. Our comparable numbers are
small (gunner reload 1, sentinel reload 2, builder action cooldown gated per turn).
A trick that pays 20-for-2 there may pay nothing here, and no measurement in this
library sizes it.

BUILDER HOOK — The cheap, testable half: when siting a siege turret against the
enemy core, prefer the **sentinel** wherever friendly bodies will occupy the line —
i.e. exactly where the crunch's clearance phase puts them — and never validate a
gunner placement with `get_attackable_tiles()` alone, since it ignores occupancy.
That is a change to a placement predicate, not a new subsystem.
