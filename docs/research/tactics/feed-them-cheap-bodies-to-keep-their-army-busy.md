---
tactic: Pin an opponent who prefers fighting to expanding by feeding him cheap units to kill, then land the real attack elsewhere
source: https://bencbartlett.com/blog/screeps-3-state-of-the-automated-union/
origin: Screeps 2018-03-12 / Ben Bartlett (author of the Overmind AI), describing a live PvP engagement
evidence: anecdotal
transfers: partial
---
WHAT IT IS — **The closest thing to a deliberate, offensive decoy that any bot league in this
sweep produced, and the exploited heuristic is named outright.** Bartlett, describing a sustained
PvP fight against a neighbouring player's AI:

> *"His combat creeps put up a good fight, frequently beating mine in equally-sized conflicts with
> what was clearly very polished kiting code. However, his AI seemed to prioritize fighting over
> expanding, and he kept pumping out fighters at the cost of under-saturating his own room's
> sources. Since I had far more resources at my disposal, I kept sending my comparatively dumb
> creeps to die to keep him occupied, and, in the end, I ended up taking out his RCL4 room with a
> pair of boosted destroyers."*

(Referents: *"his AI"* and *"his combat creeps"* are the opposing player's automated bot;
*"under-saturating his own room's sources"* means his energy harvesting fell below capacity because
the units that should have been mining were being built as fighters; the *"pair of boosted
destroyers"* is the real attack, distinct from the *"comparatively dumb creeps"* used as bait.)

**Note the exact structure, which is not the structure people imagine when they say "decoy".** The
bait units were *real* and *died*; nothing was faked. The exploited property was a **standing
production bias** — an opponent whose build priority responded to the presence of a fight — and the
payoff was **his economy**, not his position. Bartlett was not hiding anything; he was buying the
opponent's attention at a price he could afford and the opponent could not.

WHY IT MIGHT TRANSFER — **it is the one bot-league instance where the mechanism is offensive,
economic, and asymmetric in the attacker's favour**, and all three properties survive our ruleset
in principle:

- **The trigger is a production heuristic, not a percept.** We do not need the opponent to believe
  anything false; we need them to spend on combat while we spend on the core kill. That is a much
  weaker requirement than a feint, and it is the same shape as wololo's tax
  ([`their-defensive-reflex-fires-unconditionally`](their-defensive-reflex-fires-unconditionally.md)).
- **Our bait is unusually cheap and theirs is unusually expensive.** A barrier is 3 Ti at +1%
  scale; a sentinel shot costs them **10 ammo bought 1:1 from the same titanium that pays for
  buildings**, with no passive ammo income at all. That exchange rate is already the basis of
  [`ammo-drain-baiting`](ammo-drain-baiting.md), and Bartlett's account is independent
  corroboration from a second league that "feed cheap bodies to occupy them" is a real, winning
  line rather than a theory.

WHAT WOULD KILL IT — **four, and the first two are severe.**

1. **It is a single anecdote from one engagement, with no number.** The author's own summary is
   *"It seems that room quarantining was a very effective strategy here"* — a hedge, about the
   quarantine rather than about the bait, and *"here"* means that one neighbour.
2. **The asymmetry that made it work was resources, not cleverness** — *"Since I had far more
   resources at my disposal"*. Bartlett was the richer player spending surplus. **Loki's premise is
   the opposite: we want a kill before an economy differential exists.** A bait line that requires
   us to be ahead is not an opening, and this programme has no use for a tactic that only works
   from in front.
3. **Screeps is a persistent, asymmetric, multi-week MMO with no unit cap and no global cost
   scale.** We have `MAX_TEAM_UNITS = 50`, one global additive cost factor, and 1000 rounds.
   **Every bait body we build permanently inflates the price of the sentinels that do the killing**
   unless it comes from the +1% class
   ([`the-decoy-is-not-priced-in-titanium-it-is-priced-in-builder-turns`](the-decoy-is-not-priced-in-titanium-it-is-priced-in-builder-turns.md)),
   and a builder bot used as bait is the worst possible choice at **+20% each**.
4. **Our only mobile unit is the builder bot, at 40 HP and 30 Ti.** There is no cheap mobile
   throwaway in this game — the cheap things (barrier, conveyor) are immobile and the mobile thing
   is expensive. **Bartlett's "dumb creeps" have no direct analogue here**, which is why this file
   is `partial` and not `yes`.

BUILDER HOOK — **the bait must be immobile, or it is not cheap.** The smallest test uses a barrier
rather than a body: place one barrier inside a known enemy turret's line and count **ammo spent and
builder-turns diverted** in the following 20 rounds, against the 3 Ti it cost. This is the same
provocation read that
[`manner-pylon-and-what-the-rules-permit`](manner-pylon-and-what-the-rules-permit.md) already
specifies, so it should be **one leg, not two** — what this file adds is the second league's
independent evidence that the mechanism is real, and the explicit warning that Bartlett's version
was funded by a lead we will not have.
