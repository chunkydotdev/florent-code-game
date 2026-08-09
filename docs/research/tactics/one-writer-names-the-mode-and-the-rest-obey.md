---
tactic: (A)+(B) THE MEASURED COST OF SWITCHING A WHOLE TEAM ONTO ONE PLAN THROUGH A LOSSY ONE-WAY CHANNEL — one designated decision-maker, a mode number plus a timestamp, and 50 trials showing the team converges in 3.4 seconds even when fewer than half hear the message
source: https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/AIJ99.pdf
origin: RoboCup Simulation League — Stone & Veloso, CMUnited-97; *Artificial Intelligence* 110(2):241-273, June 1999
evidence: documented
transfers: yes
---

## WHAT IT IS

Stone & Veloso's protocol carries a strategy switch in two fields — `<Formation-number>` and
`<Formation-set-time>`, i.e. **which plan and when it was chosen** — and they measured how long
a whole team takes to converge on it when the channel is unreliable, single-channel and
shared with the opponent.

> *"We ran two different experiments, each consisting of 50 formation changes."*

The design: **one player is given the power to toggle the team's formation**, announces it
once, and the rest of the team must either hear the original message or learn it second-hand.
Two conditions — the announcement made by a midfielder (heard by most teammates) and by the
goaltender at the far end of the field (heard by fewer).

> *"Even when the decision-making agent is at the edge of the field (goaltender) so that fewer
> than half of teammates can hear the single message indicating the switch, the team is
> completely coordinated after an average of 3.4 seconds."*

The published table gives, for the goaltender condition: min 0.0 s, **max 23.8 s**, avg
**3.4 s**, variance 17.8, with **46.6%** hearing it from the decision-maker; and for the
midfielder condition: min 0.0, max 7.9, avg **1.3 s**, variance 2.8, **80.6%** hearing it
directly.

**And the reason a single number suffices is that the plans themselves are pre-agreed:**

> *"locker-room agreements are remembered identically by all agents and allow them to
> coordinate efficiently"*

**The switch conditions are themselves pre-agreed and keyed to the score.** CMUnited-97 used a
4-4-2 formation in general,

> *"switching to an 8-2-0 formation if winning near the end of the game, or a 3-3-4 formation
> if losing. The triggers for these formation switches were defined as part of the
> locker-room agreement."*

**Referent check.** The 8-2-0 is the defensive formation — the same paper's formation
round-robin concludes *"The results show that the defensive formation (8-2-0) does the best."*
So the rule is: **if winning near the end, switch to the defensive formation.**

## ⚠ THIS CORRECTS A RESIDUAL NEGATIVE IN SWEEP 17A

17A recorded, after searching Battlecode, Halite, CodinGame, Terminal and the StarCraft bot
codebases (**internal library quotation, from `2026-08-09-sweep-17a.md`, not a source**):
*"nobody, in any league or any codebase read here, wrote a rule in the *other* direction — an
explicit gate that **stops attacking and plays for the tiebreak score**. Every positive decides
whether to start or continue a fight."*

**Here is one.** A pre-agreed trigger that switches the whole team to the most defensive
available configuration **on the condition of being ahead near the end**. The negative was
true of the corpora 17A searched; it is not true of RoboCup, which 17A explicitly listed as
unswept.

## WHY IT MIGHT TRANSFER

**Our store is strictly better than the medium this was measured on, and the comparison is
worth making concrete.**

| | RoboCup 1997 say-hear channel | our 16-integer store |
|---|---|---|
| delivery | lossy; **46.6%** heard the announcement | **lossless** |
| latency to full team agreement | **3.4 s average, 23.8 s worst case** | **exactly 1 round**, every unit, always |
| adversary access | shared channel, opponent can hear and mimic | **private per team** |
| payload | a formation number + a timestamp | 16 unsigned 32-bit slots |

- **Everything that made their protocol complicated — encoded stamps against spoofing, gossip
  to reach the unreached, a set-time field to resolve stale messages — we get for free.** What
  remains is the part that carries the value: **one designated writer, a mode number, and the
  round it was set.**
- **The designated writer is obvious and free here.** The library measured that **cores are
  always id 1 (team A) and id 2 (team B) in every replay**, and turn order is global entity-id
  ascending with 0 inversions over 1,842,445 ordered pairs. **Our core is guaranteed to act
  before every other unit on our team, every round.** It is the natural single writer, and
  making it the only writer of a mode slot eliminates last-writer-wins entirely.
- **The `<Formation-set-time>` field has a direct use here that is not about staleness.** A
  mode-set round lets every unit compute "how long have we been in this mode", which is the
  input to the progress timeout in
  [`abandon-the-plan-on-a-progress-timeout`](abandon-the-plan-on-a-progress-timeout.md) and to
  the minimum-dwell rule in
  [`add-a-constant-to-the-incumbents-score`](add-a-constant-to-the-incumbents-score.md) — **two
  slots buying three mechanisms.**

## WHAT WOULD KILL IT

- **The measurement is of a communication protocol, not of a strategy.** 3.4 seconds is how
  fast their team agreed, not evidence that agreeing helped. The evidence that the plan content
  paid is separate — see
  [`set-plays-were-ablated-and-set-plays-won`](set-plays-were-ablated-and-set-plays-won.md).
- **Our vision limit is the constraint their channel was.** Their goaltender could *see* the
  whole field; our core sees r²=36 and a builder r²=20. **The designated writer may be the one
  unit least able to observe what the mode should be.** That is a real inversion of their
  setup and it is not solved by the store.
- **Their trigger keys on a score they can read exactly.** Ours would key on tiebreak position
  — cumulative titanium delivered — and **there is no getter for the enemy's.** "If winning
  near the end" is not directly computable here; it must be inferred, and the library's
  standing warning is that a paired differential whose variance lives on the opponent's side
  is an opponent thermometer, not a dial.
- **17A's residual negative is corrected in existence, not in strength.** One 1997 soccer team
  wrote a play-for-the-score rule. That is a precedent, not a recommendation, and our own
  measured tiebreak advantage flips sign with opponent strength (+9.8pp against 1550-1649,
  −7.5pp against <1450, and **≥1750 is empty**).

## BUILDER HOOK

Two slots and no behaviour change: have the core — and only the core — write `SLOT_MODE` and
`SLOT_MODE_SINCE` each round, computed from whatever branch logic already exists. Every other
unit reads both and `print()`s whether its own locally-computed branch matches. **The
disagreement rate is the deliverable.** If it is near zero, our units already agree and a mode
channel buys nothing; if it is high, the disagreements are the bug, and one designated writer
fixes them at a cost of one round of latency — against the 3.4 seconds the field paid.

## SOURCES QUOTED IN THIS FILE

- https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/AIJ99.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09); Table 7's numbers were additionally re-read from
`pdftotext -layout` output.
