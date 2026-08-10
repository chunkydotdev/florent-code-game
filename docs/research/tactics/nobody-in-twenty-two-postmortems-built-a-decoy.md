---
tactic: SURVEY / NEGATIVE — deception of the *opponent* is essentially absent from the Battlecode corpus
source: https://battlecode.org/past
origin: Battlecode 2019-2026 — all 22 official postmortems, machine-searched 2026-08-10
evidence: documented
transfers: no
---
WHAT IT IS — **The denominator for sweep 20A, and it is close to zero.** All 22 official
Battlecode postmortems (2019-2026) were downloaded, `pdftotext`-extracted and flattened
(`tr -s ' \n\t\f\r' ' '`) to defeat the page-break trap, giving **123,745 words** of
first-person competitor writing from the league whose engine ours is a derivative of. Literal
case-insensitive greps over that corpus:

| term | hits | files |
|---|---:|---:|
| `decoy` | **0** | 0 |
| `feint` | **0** | 0 |
| `deceiv` | **0** | 0 |
| `bluff` | **0** | 0 |
| `mislead` | **0** | 0 |
| `disguis` | **0** | 0 |
| `fake` | **0** | 0 |
| `camouflage` | 5 | 1 |
| `bait` | **1** | 1 |
| `trick` | 8 | 6 |

**Every one of those non-zero hits reduces to something other than deceiving an opponent, with
exactly one exception.**

- `camouflage` ×5 — all in wololo 2021, and all describe a **game-provided mechanic**, not a
  player tactic:

  > *"If a slanderer existed for 300 turns, it then "camouflaged" and became a politician"*

  (The subject is the Battlecode 2021 unit type, and the transformation is automatic on a turn
  counter — no player chooses it.) wololo discusses it purely
  as economics (conviction retention, unit-count sacrifice). **Nobody in the corpus writes about
  exploiting the resulting ambiguity** — the one league mechanic that made two unit types
  indistinguishable to an opponent was mined for income, not for lies.
- `bait` ×1 — no thoughts head empty 2023, and it is a team baiting **its own** units. See
  [`hallucinate-a-target-to-steer-your-own-units`](hallucinate-a-target-to-steer-your-own-units.md).
- `trick` ×8 — seven are engineering idioms ("their trick they had come up with for going
  through sensed locations in a bytecode-efficient manner", "tricks like flag passing", a trick
  for counting Paint Towers, an SRP-placement trick, and The Kragle offering *"tricks for other
  aspiring teams"*). **The eighth is the only cross-team deception in the corpus** — Prasici
  replaying Steam Locomotive's own message back at them, filed separately as
  [`the-only-cross-team-spoof-was-a-replayed-message`](the-only-cross-team-spoof-was-a-replayed-message.md).

**So: one instance of opponent-directed deception in eight years of the closest comparable
league, and it was a comms replay attack, not a decoy.** Nobody built a fake expansion. Nobody
sent a sacrificial unit to draw a defence. Nobody hid a real build behind a false one.

WHY THIS MATTERS FOR US — **it answers sweep question (C) flatly: nobody measured the payoff of
deception because almost nobody attempted deception.** Every "the enemy reacted wrongly" result
in this corpus comes from the opponent's own unconditional reflexes being *taxed by a real
attack* (wololo — [`their-defensive-reflex-fires-unconditionally`](their-defensive-reflex-fires-unconditionally.md))
or from a *bug* in their reaction logic (5 Musketeers' distress oscillation —
[`defence-recall-oscillation`](defence-recall-oscillation.md)), never from a manufactured false
belief. **The competitive precedent is: attack them for real in the place their reflex
overreacts, rather than pretending to.**

Read the absence carefully before treating it as a market gap. Two readings are live and this
survey cannot separate them: (i) deception is underexplored and therefore cheap alpha, or
(ii) deception loses to bots, because a bot's reaction is cheap, local and instantly revised —
it does not tilt, does not commit, and re-senses next turn. **Reading (ii) has one concrete
supporting datum in the corpus:** the single successful spoof worked on the *communication
layer* (a persistent belief, written to a shared array and acted on for many turns), not on the
*sensing* layer. Nothing in the corpus shows a bot holding a false belief that came from its own
eyes.

WHAT WOULD KILL IT — nothing about our engine; this is a survey result, not a mechanic. What
would *change* it is a source outside Battlecode showing a measured decoy payoff. The other two
lanes of this sweep were tasked with exactly that; anything they find belongs beside this file,
not instead of it. Note also that our corpus is competitor *self-report*: a team that ran a
decoy and did not write it up is invisible here. The 0-hit columns are strong evidence about
what teams thought was worth explaining, and weaker evidence about what every bot did.

BUILDER HOOK — none, and deliberately. **Do not spend a leg building a decoy on the strength of
"nobody has tried it".** The buildable output of this sweep is
[`hallucinate-a-target-to-steer-your-own-units`](hallucinate-a-target-to-steer-your-own-units.md),
which is the opposite mechanism.

Reproduction: `curl -sL https://battlecode.org/past`, extract the 22
`assets/files/postmortem-*.pdf` links, `pdftotext` each, flatten with
`tr -s ' \n\t\f\r' ' '`, then `grep -oi '<term>' *.flat | wc -l`.
