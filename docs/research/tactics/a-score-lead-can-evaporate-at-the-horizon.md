---
tactic: A SCORE LEAD IS NOT BANKED — a 2nd-place bot repeatedly held a 4x score lead at 90% of the clock and finished at zero, because the scored substance was removable right up to the final turn
source: https://www.kaggle.com/competitions/lux-ai-season-2/writeups/tigga-yet-another-logic-bot
origin: Lux AI Challenge Season 2 (2023) / Tigga, 2nd place
evidence: documented
transfers: partial
---
⚠ **TIER 2.** Read through a text proxy, **not diffed against Kaggle's original
HTML**. The strings verify verbatim against the local bytes.

⚠ **FILED CORRECTLY, AND THE FILING IS THE POINT.** This is **not** a kill failure
and must not be read as one. It is a **score lead evaporating at the horizon** — a
different phenomenon from
[`it-walked-away-from-a-kill-it-had-won`](it-walked-away-from-a-kill-it-had-won.md),
which is from the same author and the same list of self-criticisms. Merging them
would manufacture a claim neither source makes.

WHAT IT IS — Tigga's own account, in his list of weaknesses. The bullet is headed by
his diagnosis — *"Countering late game heavy lichen blitzing. Seems I lose a lot of
games to this. Have to figure out a way to indentify it and combat the blitzers."*
(his typo, preserved) — and the magnitude is stated in the same bullet:

> *"Many games I lose despite being 4x lichen up at step 900 and basically dropping to zero by step 1000."*

**Four times ahead, at 90% of the clock, to zero.** The mechanism is available in the
S2 spec and is not inference: lichen is the scored substance, and
*"any addition of rubble onto a tile with [Lichen](#lichen) on it will automatically
remove all of the lichen on that tile."* A heavy robot self-destructing or digging
adds rubble. So an opponent with no economy left can spend his last hundred turns
**deleting the scoreboard** rather than building his own — and the score is a *stock*
that can be driven to zero, not a ledger.

WHY IT MIGHT TRANSFER — Only partly, and the partition is the finding, because our
three tiebreak keys behave completely differently under this attack.

- **Key 1, `most titanium collected`, is CUMULATIVE and therefore immune.** Titanium
  already delivered cannot be removed by anything an opponent does. This is a
  structural protection Tigga did not have, and it is a large part of why our
  economy-first bot wins **57.2% of the 353 games that reach r1000**.
- **Key 2, `most harvesters`, is a live count of 30 HP buildings and is fully
  exposed.** A sentinel kills a harvester in two shots. At r990 an opponent can
  reduce our key-2 standing with no economic consequence to himself whatsoever,
  because there is no future left for the titanium he is spending.
- **Key 3, `most titanium stored`, is a stock and is exposed in the other direction**
  — it falls whenever we spend, so end-game spending trades key 3 away.

So the transferable statement is precise: **our score is only immune at key 1, and
key 1 is only decisive when the key-1 margin is non-zero.** In any game that reaches
r1000 with the collected-titanium totals close, the decision passes to a key that
**can be attacked in the last ten rounds at zero opportunity cost.**

That is a real and unexamined exposure. It is also a symmetric opportunity: the same
arithmetic says a late harvester raid against an opponent whose key-1 margin is thin
is one of the cheapest interventions available to us, because damage dealt at r990
costs the attacker nothing he will miss.

WHAT WOULD KILL IT — **One corpus cut kills or confirms the whole file: which
tiebreak key actually decided our 353 r1000 games.** 17A already queued exactly this
measurement and it has never been run. If key 1 decides ~all of them, our score is
effectively banked, Tigga's failure mode does not exist here, and this drops to
`transfers: no` — a clean and valuable negative. If key 2 decides a meaningful share,
we have both an exposure to defend and a lever to use, and it is the cheapest lever
in this sweep because it fires in rounds where nothing else we could buy will pay off.

It is also killed by the possibility that opponents simply never do this. Nothing in
our corpus has been checked for late harvester raids, and Lux's blitzers existed
because their scored substance was deletable *in bulk by one action*. Ours is not:
removing a harvester takes two sentinel shots, not one dig.

BUILDER HOOK — Run the queued cut first. If key 2 matters, the defensive hook is
smaller than the offensive one and should come first: **from r950, treat any friendly
harvester below half HP as a heal priority over every economic action.** Healing is
4.00 HP/Ti, the titanium has no remaining use, and key 2 is decided by the count
alive at the horizon rather than by anything cumulative.
