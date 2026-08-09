---
tactic: THE META MOVED FROM COLLECTION TO DENIAL — the decisive lever was stopping the opponent's income, not destroying his base; and the counter to denial was escorting, which produced an escalation the field never exited
source: adamslay.md — GitHub README, "LUX AI Season 2 Rule-based Agent (top 25 solution)", 23rd of 637 (local raw fetch; the canonical repo URL does NOT appear in the local bytes and is deliberately not invented here)
origin: Lux AI Challenge Season 2 (2023) / a 23rd-place rule-based agent, describing the field's meta evolution
evidence: documented
transfers: partial
---
WHAT IT IS — A competitor's account of how the S2 field's meta moved, in three
stages. The quote carries the demonstrative *"This trend"*, so the sentence
establishing the referent is quoted with it, as the library's second rule requires:

> *"However, as the competition progressed, it became clear that the most successful agents would not only focus on resource collection, but also on resource denial. This trend started with agents that would sacrifice all but one of their factories in order to devote all of their energy to destroying the opponent's robots, thus denying them the ability to collect resources and keep their factories alive."*

Referent: *"This trend"* is **the shift from resource-collection-focused agents to
denial-focused ones**, stated in the immediately preceding sentence and quoted above.
Without it the "in order to devote all of their energy" clause reads as if it were
about a single agent's design rather than a field-wide movement, which is the error
this rule exists to prevent.

*(Source note for re-grepping: the raw markdown is hard-wrapped, and there is a
trailing space after `resources` before the line break. A whitespace-flattened grep
finds it; a raw grep on the full sentence will not. The apostrophe in
`opponent's` is **ASCII** in this file — see the per-string glyph warning in the
summary.)*

**And the third stage matters as much as the second**, because it is where the field
stopped:

> *"Once this strategy became popular, it was quickly countered by agents that would defend their factories by deploying robots to antagonize the robots that were sent to antagonize them."*

Denial → escort → escort-the-escort. The author's own summary is that the meta
*"escalated quickly"* into a cat-and-mouse over robot survival. **Nobody in this
account ever went back to pure collection, and nobody found a denial that could not
be escorted.**

WHY IT MIGHT TRANSFER — This is the one Lux finding with a genuine mechanical
counterpart here, and the counterpart is **the tiebreak table**, not the core.

Our tiebreak keys are *"most titanium collected, then most harvesters, then most
titanium stored"*. Two of the three are **directly attackable**:

- **Key 2, harvesters alive, is a physical object with 30 HP on a known tile.** A
  sentinel (18 dmg, r²=32, line ignores obstacles) removes one in two shots. A
  builder bot's attack — 2 Ti for 2 dmg on an orthogonally adjacent tile — removes
  one for 30 Ti and 15 turns, which is a bad price but a legal one.
- **Key 1, titanium collected, is a rate you can suppress** by killing harvesters
  and by cutting conveyor lines, both of which are buildings and therefore legal
  builder targets.

That is a real road, and it is *not* the same road as the core kill. It is the
tiebreak version of adamslay's meta: **do not fight their army, reduce their
ledger.** It also sits well with our measured strengths — the library's standing
finding is that we win the clock (57.2% at r1000) and die in the middle game.
Suppressing their key-1 rate widens the margin on the road we already win, instead of
opening a sixth doctrine road on the one we lose.

The escalation half transfers as a **warning**, and it is a sharper warning here than
it was there. Their counter to denial was escorting robots with robots. Our escort is
**strictly stronger**: builder attacks cannot touch builder bots, so a healing detail
standing on a harvester tile is untouchable except by turrets, and one heal repairs
both the bot and the building on that tile (8.00 HP/Ti stacked). **A competent
opponent's counter to harvester denial costs them almost nothing and beats a builder-
borne raid outright.** Only turrets break it — which puts us back in the forward-
placement problem the library calls closed.

WHAT WOULD KILL IT — Three things, and the first is decisive:

1. **Their denial killed; ours only slows.** See
   [`the-kill-mechanism-was-starvation-not-hp`](the-kill-mechanism-was-starvation-not-hp.md).
   Lux S2 factories die of thirst, so denial *is* the win condition there. Here it is
   a tiebreak adjustment, worth a fraction of a key rather than a game.
2. **Key 1 is cumulative.** Titanium already collected cannot be taken back. Denial
   only suppresses the *forward* rate, so its value scales with the rounds remaining
   at the moment it starts working — which makes it an early-game tactic exactly where
   the library says early contact is costly, and worth almost nothing after r700.
3. **It is untested against the escort.** No file in this library measures a raid on
   an enemy harvester defended by a healing builder. If that exchange is worse than
   2.2:1 — and the stacked-heal arithmetic says it is — the tactic loses titanium
   faster than it denies it, which would make this a `no`.

BUILDER HOOK — Corpus first, no bot change: **cut our 353 r1000 games by which
tiebreak key decided them** (17A already queued this), and then **cut the enemy
harvester count at r1000 in games we lost the tiebreak against games we won it.** If
key 2 never decides anything, the whole harvester-denial road is worth nothing here
regardless of how cheap it is, and this file should be downgraded to `no` on the
strength of that cut alone. That is a cheaper test than building the raid.
