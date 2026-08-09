---
tactic: COUNTERWEIGHT — a team built the expensive emplacement because it was the only thing left to spend on, not because it was good
source: https://battlecode.org/assets/files/postmortem-2022-5-musketeers.pdf
origin: Battlecode 2022, 5 Musketeers
evidence: documented
transfers: yes
---

## WHAT IT IS

This sweep was told to actively look for the reading in which an observed structure mix
is a **consequence** rather than a **cause**. This is the cleanest published instance of
it, and the team states it themselves without apparently noticing what they are saying.

BC2022 capped how much resource a team could spend per turn — one soldier per Archon —
and 5 Musketeers coined a word for being above the cap:

> *"This year, though, the most lead you could spend per turn was 300, one soldier per
> Archon. Too much more than that, and you were certainly obese. When obese, we wanted to
> be making more builders. This is because the builders can use that excess lead to build
> watchtowers."*

**The watchtower — the season's expensive static structure — appears in their build not
as a doctrine but as a DRAIN for resources their unit production was rate-capped from
absorbing.** The same document says elsewhere that *"It still wasn't worth it to build
anything expensive"* and that *"The games were won and lost with soldiers."* Both
statements are true simultaneously, and the reconciliation is: **you build the expensive
static thing with the money you could not spend on the cheap good thing.**

## WHY IT MIGHT TRANSFER — and it is close to exact

**We have the same rate cap, and it is harder than theirs.** Our core spawns **at most one
builder bot per turn**, and each builder adds +20% to the single global cost scale. Turns
are not purchasable (sweep 14 established this as the structural reason our field's
anti-rush is not available to us). Meanwhile passive income arrives unconditionally at 10
Ti every 4 rounds and harvesters deliver on their own schedule.

**So the condition that produced 5 Musketeers' watchtowers — income exceeding the rate at
which the good unit can absorb it — is our permanent state, and we have measured it:**
*we bank and do not spend; we end r200-300 holding more titanium than Ouroboros while
buying a twelfth as much ammunition* (INDEX standing context).

**This cuts two ways and both are useful:**

1. **As a warning about the sweep's own subject.** If the top tier's gunner-heavy mix is
   partly **what a rich, rate-capped bot spends on** (my paraphrase of the mechanism, not a
   quotation from anyone), then the mix is a
   spending-sink artefact, and copying the ratio buys nothing. This is a second,
   independent route to the marker reading in
   [`a-gunner-kill-is-a-clear-line-not-a-doctrine`](a-gunner-kill-is-a-clear-line-not-a-doctrine.md).
2. **As a genuine, cheap lever for us specifically.** We are the ones with the idle bank.
   5 Musketeers' answer to obesity was to convert surplus into the expensive static
   structure. **Ours already exists and is not a structure: `convert_ammo()`.** It is the
   only sink in our ruleset that costs no action cooldown, no adjacency, no tile and no
   scale — and it is precisely the one we under-use.

## WHAT WOULD KILL IT

- **Their cap was on spend; ours is on unit production only.** We can spend arbitrarily
  much titanium per turn on structures and ammunition — a builder bot can build once per
  turn but many builders build in parallel. So "obese" is not a rule of our engine; it is
  a description of our *measured behaviour*. That distinction matters: theirs was forced,
  ours is a choice we keep making.
- **The quote proves the motive for one team in one season.** It does not establish that
  any other team's static-defence count was a spending sink, and it must not be cited as
  though it did.
- If our banked titanium turns out to be reserved deliberately (e.g. for rebuild
  reserves), the "idle sink" reading is wrong and this file's second limb dies.

## BUILDER HOOK

The smallest test is not a structure at all: **a surplus rule on the core.** If banked
titanium exceeds what the next N rounds of planned builds require, convert the excess to
ammunition — a sink that is never rate-capped, never blocked by adjacency, and never
raises the cost scale. The measurement that would justify it: our median titanium balance
by round, against the median ammunition balance, ours vs the field. If the first curve is
high and flat while the second is near zero, the obesity is real and it is ours.
