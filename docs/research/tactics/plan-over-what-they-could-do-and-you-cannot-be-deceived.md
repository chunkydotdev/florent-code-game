---
tactic: (D) The immune opponent, with its mechanism named — one that plans over what you COULD do rather than what you WILL do
source: https://github.com/rooklift/halite2_rush_theory
origin: Halite II 2017 / rooklift (fohristiwhirl), "rush theory"; corroborating decay evidence from CodinGame "Ocean of Code" 2020 / pb4
evidence: documented
transfers: partial
---
WHAT IT IS — **Sweep question (D) has a clean answer, and it is not "a bot that is smarter". It is
a bot that uses a different decision rule.** rooklift, analysing early-game ship combat in Halite
II, describes placing ships in positions where every enemy response is at worst a neutral trade,
then states the property that follows:

> *"It's worth noting that this approach uses no prediction at all. We prepare for what the enemy
> could do, not what we think he will do. Therefore, it cannot really be exploited"*

(The referent of *"this approach"* is the "sweet spot" placement described immediately before —
positions computed from the *threat ranges* of the enemy ships, i.e. from the enemy's action set,
not from any forecast of which action he picks. *"it"* = that approach.) **A bot that evaluates
against the opponent's whole option set has no branch to trigger, because it never committed to a
belief about which option is coming. There is nothing to falsify, so there is nothing to fake.**

**This is the general form of the immunity we found separately in Battlecode.** The one successful
cross-team deception in that corpus worked because Steam Locomotive's units held a *durable belief
about a fact* — where their own HQ was — and The High Ground was immune purely because their
constants differed
([`the-only-cross-team-spoof-was-a-replayed-message`](the-only-cross-team-spoof-was-a-replayed-message.md)).
**Deception needs a stored belief to corrupt. Purely reactive, option-set-based logic stores
nothing.**

**And where a whole game was built on hiding, the hiding decayed.** Ocean of Code (CodinGame 2020)
is a hidden-movement game — a submarine whose position the opponent must infer. pb4, one of its
strongest competitors, on how the value of pure stealth moved over the contest:

> *"By this time, moving with the sole objective to stay stealthy was a declining strategy as most
> players started to use mines efficiently."*

(*"By this time"* refers to the later stage of pb4's own iteration, described in the preceding
sentences; *"declining"* is about the strategy's value as the field adapted, not about pb4's
rating.) **Even in a game explicitly about concealment, concealment-as-an-end depreciated as the
field learned to probe instead of guess.**

WHY IT MIGHT TRANSFER — **as a diagnostic that costs zero games and should gate the whole
family.** Before building any provocation, the question to ask about each of the five opponents
holding our rating deficit is not "are they strong" but **"do they branch on a stored belief, or do
they re-derive from what they can see each round?"** Our own corpus can answer this: a bot that
stores a belief shows *hysteresis* — behaviour that persists after the triggering observation
disappears — and one that re-derives does not. That is precisely the signature 5 Musketeers
described from the inside when their own recall logic *lacked* hysteresis and oscillated
([`defence-recall-oscillation`](defence-recall-oscillation.md)).

**The inverse also matters and is on-programme in a way defence never is.** rooklift's rule is a
statement about *our* decision layer too: a Loki that commits to a plan based on a prediction is
exploitable, and this library has repeatedly found that the winning representation stores no plan
([`the-modal-winning-representation-is-no-stored-plan`](the-modal-winning-representation-is-no-stored-plan.md)).
**We are, by that account, already close to un-deceivable — which is the same fact as "we have
little to gain from being deceived less", so it is not a plank, it is a reason not to spend on
counter-deception.**

WHAT WOULD KILL IT — **the transfer is weaker than the quote sounds, and the reason is our
geometry.** rooklift's claim is about a *simultaneous-move, continuous-space* collision game where
"what the enemy could do" is a small, enumerable disc around each ship. Our engine is sequential
with a measured id-ascending turn order, builder bots move only cardinally, and the enemy's option
set over 1000 rounds is not enumerable in 10 ms. **"Plan over their whole option set" is a
tractable rule in Halite II and an intractable one here** — so this file supplies a *diagnostic*
and a *warning*, not a decision procedure we can implement. Also note rooklift's own hedge: *"cannot
really be exploited"*, not "cannot be exploited". And pb4's decay observation is one competitor's
retrospective on one contest, with no numbers attached.

BUILDER HOOK — **a corpus cut, no games:** for each of the five opponents in
`docs/research/dirty-tricks-shortlist-2026-08-09.md`, measure **hysteresis** — after one of our
units leaves their sensing range, how many rounds does their altered behaviour persist? **Zero
rounds means they re-derive and are rooklift-immune: no feint we build will ever pay against them,
and the deception family should be closed for that opponent specifically.** A persistence tail
means a stored belief exists, and only then is there a surface worth
[`a-feint-only-pays-when-the-victim-overreacts`](a-feint-only-pays-when-the-victim-overreacts.md).
