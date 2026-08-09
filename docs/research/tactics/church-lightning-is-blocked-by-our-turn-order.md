---
tactic: TRANSFERS: NO — Battlecode 2019's named stalemate-breaker was a build-chain that exploited same-round activation of newly-created units; our engine is measured to forbid exactly that
source: https://battlecode.org/assets/files/postmortem-2019-big-red-battlecode.pdf
origin: Battlecode 2019 / Big Red Battlecode (describing the technique's effect on the meta)
evidence: documented
transfers: no
---
WHAT IT IS — BC2019's metagame reached the state ours is in: games that neither
side could finish, settled on a health tiebreak. The technique that broke it was
called **church lightning** — a pilgrim builds a chain of alternating
church-pilgrim-church-pilgrim structures reaching across the map, terminating in
an attacking unit next to the enemy castle.

> *"Church lightning very easily broke stalemates that focused on winning by unit
> health"*

The mechanism is stated explicitly, and it is a **turn-order exploit**:

> *"This aptly used the turn timer (as newly completed units had the next turn and
> could thus go right after the preceding unit, and so the church lightning chain
> steps could be completed almost instantly given enough resources."*

Referent: "the turn timer" is BC2019's within-round unit activation order; "the
preceding unit" is the previous link in the chain. The whole chain therefore
resolves inside effectively one round, which is why the defender cannot respond.

And note what it actually won — not always an annihilation:

> *"was able to allow teams to win by having more castles (even if complete castle
> annihilation wasn’t possible)"*

i.e. it converted by improving the **tiebreak key**, one rung up from unit health,
rather than by finishing the enemy off.

WHY IT DOES NOT TRANSFER — Our engine has been measured on precisely this point,
twice, independently, and the answer is the opposite of BC2019's:

- **A unit created mid-round does not act that round.** 24,045 new entities,
  0 acted (s25 research; independently confirmed by the builder arm over 205
  replays, 1,842,445 ordered pairs, 0 inversions). A core-spawned builder first
  acts the *following* round.
- Turn order is **global entity-id ascending**, and ids come from a single
  creation-order counter — so a newly built entity always holds the *highest* id
  and therefore acts *last*, if it acts at all.

So a chain cannot cascade within a round here. Each link costs at minimum a full
round, and the chain is visible and attackable for every one of them. Worse, our
chain could not terminate the way BC2019's did: **builder bots are spawned only by
the core, at most one per turn, on the 12-tile Chebyshev-1 spawn ring.** A builder
cannot build another builder. The only things we can extend forward are buildings
— and a newly built turret does not fire the round it is built.

The tiebreak-key half of the technique does not import either. BC2019's key was
castle count, which the chain could directly manufacture. Our keys are titanium
delivered, harvesters alive, titanium stored — none of which a forward structure
chain produces. A forward conveyor line into *their* territory feeds nothing of
ours.

WHAT WOULD KILL THE "NO" — Only an engine change. If the ordering fact were ever
found to have an exception — a class of entity that acts on its creation round —
the whole family reopens, and it would reopen loudly, because a same-round cascade
is the one thing that defeats a rate-capped defence outright. The measurement is
strong enough (0 in 24,045, plus two causal tests that never look at log ordering)
that this should be treated as settled rather than re-probed.

BUILDER HOOK — none, and that is the point of the file: it exists so the next
session does not spend a sweep rediscovering a stalemate-breaker our engine
already forbids. The transferable residue is the *framing* — BC2019's field broke
its stalemate by attacking a **tiebreak key** rather than the enemy base — and for
us the only key that is attackable at all is **harvesters alive**, which is key 2.
That is a different tactic and is not sourced here.
