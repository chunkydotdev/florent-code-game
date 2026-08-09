---
tactic: (A) THE ANSWER FOR A 16-INT BUFFERED STORE — do not transmit a plan, transmit an index into a plan table that every unit already holds because it is in the same source file
source: https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/AIJ99.pdf
origin: RoboCup Simulation League — Peter Stone & Manuela Veloso, CMUnited-97 (4th of 29, RoboCup-97) / CMUnited-98 (world champion); *Artificial Intelligence* 110(2):241-273, June 1999
evidence: documented
transfers: yes
---

## WHAT IT IS

The paper is titled *"Task Decomposition, Dynamic Role Assignment, and Low-Bandwidth
Communication for Real-Time Strategic Teamwork"*, and it is the only source any sweep in
this library has found that solves **our exact constraint set** rather than an analogue of
it: autonomous agents, no shared memory, a single low-bandwidth unreliable channel, and a
hard real-time budget.

Its own summary of what it contributes lists the object we want by name:

> *"a method for using roles to define pre-compiled multi-step, multi-agent plans"*

**Referent check.** That phrase sits in the contributions list in section 2; the full
sentence enumerates *"the introduction of the concepts of PTS domains and locker-room
agreements; the definition of a general team member agent architecture structure for
defining a flexible teamwork structure; the facilitation of smooth transitions among roles
and entire formations; a method for using roles to define pre-compiled multi-step,
multi-agent plans; and techniques for dealing with the obstacles to inter-agent
communication during the low-communication periods of PTS domains with single-channel,
low-bandwidth, unreliable communication during the "on-line" periods."* So *"pre-compiled
multi-step, multi-agent plans"* is the authors' own description of their set-play mechanism,
not a reader's gloss.

**The mechanism is that the plan is not communicated at all.** It is agreed before the game
and stored identically in every agent:

> *"The locker-room agreement is set by the team when it is able to privately synchronize."*

> *"The set-plays are defined in the locker-room agreement so that they are known to all
> agents on the team."*

And the problem it is solving is stated in the same words we would use:

> *"since the agents are autonomous and do not share memory, they could easily become
> uncoordinated"*

**Referent check.** That clause is item 3 of a list of open problems the architecture must
answer — *"how to ensure that all agents are using the same formation; and how to ensure
that all roles in a formation are filled: since the agents are autonomous and do not share
memory, they could easily become uncoordinated."* The subject is the team's own agents, not
the opponent's.

**The runtime channel then carries only an index.** In their protocol the live message
fields for a strategy switch are `<Formation-number>` and `<Formation-set-time>` — a number
naming which pre-agreed plan is active, and when it was chosen.

## WHY IT MIGHT TRANSFER

This is the single most load-bearing structural result in sweep 18 for our engine, and the
reason is that **our version of the locker-room agreement is free.**

- Every unit on our team runs the same `Player` class from the same `main.py`. A table of
  plans written as a module-level constant is **already shared by every unit, at zero
  bandwidth, with zero latency, and with no possibility of disagreement about its
  contents.** Stone & Veloso had to arrange a synchronisation opportunity to establish
  theirs; ours is established by the zip file.
- Our 16 unsigned integers then have to carry **one small number**, not a plan.
  `SLOT_MODE = <index into PLANS>` plus `SLOT_MODE_SINCE = <round it was set>` is the exact
  pair of fields their protocol uses, and it fits in two slots.
- **Every hazard the library has measured in our store disappears when the payload is an
  index.** Last-writer-wins is harmless if all writers are computing the same index from the
  same world state. The one-round buffer costs one round of latency on a mode switch, which
  is two orders of magnitude better than the 3.4-second average propagation Stone measured
  over a lossy broadcast (see
  [`one-writer-names-the-mode-and-the-rest-obey`](one-writer-names-the-mode-and-the-rest-obey.md)).
  A small nonnegative index can never trip the negative-write raise that permanently
  destroys a unit.
- It answers 17A's structural finding directly. 17A established that **an
  economically-correct evaluator never finishes**, because every step of an assault has a
  negative immediate return. A pre-compiled plan does not price its steps at all — it
  executes an index. The suspension of per-step pricing is the *point* of the
  representation, not a side effect.

## WHAT WOULD KILL IT

- **A plan table is a fixed opening by another name.** Sweep 9 already established that
  fixed openings are the league norm and that our constant is defensible, **with one
  documented failure mode: an opening unconditional on MAP GEOMETRY.** A plan table indexed
  only by game phase and not by map width/ore layout reproduces exactly the error our own
  width gradient already is. The trigger conditions must read geometry.
- **Stone's agents have real memory between decisions; ours have 16 ints.** The paper's
  agents also keep an *internal state* per agent (*"the agent's role within a team behavior
  could be stored as part of the internal state"*). We can hold per-unit state on the
  `Player` instance keyed by `ct.get_id()` — this works, and
  [`the-goal-stack-beats-the-mode-flag`](the-goal-stack-beats-the-mode-flag.md) already
  documents it — but it is **not** durable across a unit's death and cannot be read by
  another unit. Anything two units must agree on still has to go through the index.
- **No claim here that the plan table wins.** The measured evidence that set-plays paid is
  in [`set-plays-were-ablated-and-set-plays-won`](set-plays-were-ablated-and-set-plays-won.md);
  it is a soccer result over 38 ten-minute games, in a game with mobile attackers and no
  healing. It licenses the *representation*, not the *content*.
- **RoboCup's medium is worse than ours in one way and better in another.** Their channel is
  lossy and shared with the opponent; ours is private and reliable. But their agents get
  *continuous* sensing of teammates' positions, and ours are vision-limited (builder
  r²=20). A plan that assumes units can see each other executing it will not run here.

## BUILDER HOOK

Smallest test, and it changes no behaviour on the first plank: define `PLANS` as a
module-level tuple of named modes that the bot **already** has (whatever the current
build-priority branches are), have exactly one designated unit — the core, which is id 1 or
2 and therefore always acts first in the round — write the chosen index to a store slot each
round, and have every other unit *read* the index and assert (via `print()` to the replay)
that the branch it would have picked locally matches it. **Parity is required: behaviour
must be byte-identical.** Then read the disagreement rate off the replay text. If units
already agree with the core almost always, a shared mode index costs one slot and buys
nothing; if they disagree often, the disagreement is the thing worth building against, and
you have found it for the price of one store slot and one print.

## SOURCES QUOTED IN THIS FILE

- https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/AIJ99.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text (`pdftotext` → strip markup → decode entities → flatten whitespace including `\f\r` →
`grep -F`) during tactics sweep 18 (2026-08-09).
