---
tactic: The withdrawal predicate is a CONJUNCTION and the clause everyone forgets is "a destination exists"
source: https://battlecode.org/assets/files/postmortem-2023-dont-at-me.pdf
origin: Battlecode 2023, don't @ me (US Qualifier finalist)
evidence: documented
transfers: partial
---

## WHAT IT IS

don't @ me's forward unit leaves on a three-clause conjunction, stated as a
single sentence in their strategy list:

> *"A launcher's state is set to fallback if it is not in combat, if they are less than half health, and if they have a fallback island."*

**Referent check.** "A launcher" is their main combat unit; "fallback island" is
defined in the immediately following bullet:

> *"A fallback island is the closest captured island to the given launcher."*

The three clauses do three different jobs:

1. **`not in combat`** — the task check. A unit currently doing forward work does
   not evaluate the withdrawal at all. (Same shape as
   [`finish-the-task-before-you-withdraw`](finish-the-task-before-you-withdraw.md).)
2. **`< half health`** — the danger check, and it is the *weakest* of the three.
3. **`has a fallback island`** — **the destination check.** No destination, no
   withdrawal. A unit with nowhere to go stays and keeps working.

And the same team, in the same document, records that they **cut this feature
entirely in Sprint 2** and only reinstated it after the organisers changed the
healing numbers:

> *"we decided that the value we were getting from the island heal was too low and we would rather have the map presence that the launcher presente, even if it was low health."*

**So the same team, on the same mechanic, went both ways within one season — and
the deciding variable was the exchange rate between HP restored and map presence
forgone, not a doctrine.**

## WHY IT MIGHT TRANSFER — clause 3 is the one that ports; clause 2 mostly does not

**Clause 3 is directly implementable and we probably violate it.** A round-count
give-up (`GIVEUP_RND`) fires whether or not there is anywhere better for the unit
to be. don't @ me's structure says: **compute the destination first, and if the
best destination is the tile you are standing on, the withdrawal is a no-op.**
That single change converts a clock into a comparison, and it composes with
[`the-idle-forward-unit-gets-a-destination-not-a-recall`](the-idle-forward-unit-gets-a-destination-not-a-recall.md).

**Clause 2 does not port cleanly**, because their fallback island *heals* and our
home does not — see
[`every-withdrawal-trigger-in-the-field-is-a-resupply-trigger`](every-withdrawal-trigger-in-the-field-is-a-resupply-trigger.md).
Their own Sprint-2 deletion is the evidence for that: when the heal was worth
little, they preferred the map presence. **On our ruleset the heal at home is
worth exactly nothing, because there is no heal at home — so their Sprint-2
position, not their final one, is the one that matches our exchange rate.**

## WHAT WOULD KILL IT

* The reinstated version won them games on **island-heavy Qualifier maps**, i.e.
  the destination was cheap and abundant. Ours is not: there is no captured
  intermediate position to fall back to, only our own core.
* Treating "our core" as the destination makes clause 3 trivially true always,
  which silently deletes the clause. **If it is implemented, the destination set
  must be forward positions, not home.**

## BUILDER HOOK

Replace the raid give-up with: *pick the best next act-target anywhere I can
reach; if it is behind me, walk back; if there is none, hold.* The withdrawal
then falls out of target selection and no clock is needed. **Falsifier: if the
"best target is behind me" branch fires in a large majority of raider-rounds, the
raid target list is the defect and this change is cosmetic.**
