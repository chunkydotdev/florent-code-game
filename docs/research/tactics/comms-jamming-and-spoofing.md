---
tactic: Jam or spoof the enemy's communication channel — REFUTED for our ruleset
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
origin: Battlecode 2020 — The High Ground (4th) names both attacks; confused prices the counter
evidence: documented (the tactic) / documented (our refutation, from the engine)
transfers: no
---

WHAT IT IS — Battlecode 2020's communication channel was **shared by both teams
and rate-limited**, which makes it attackable:

> *"units could bid soup to send messages, and the top 7 per round were published
> anonymously to both teams"*

The High Ground names the two attacks it invites, and the second is the nastier
one:

> *"it was possible to mess up your opponent by either spending a lot of soup to
> spam messages and prevent them from communicating, or mess up their
> communication by sending messages they would interpret as their own"*

**Bandwidth denial and identity spoofing, on a channel with a fixed number of
slots per round and no sender authentication.**

And the field priced it honestly rather than romanticising it — confused, on why
nobody actually ran the jam:

> *"This made message spamming highly unprofitable until at least mid game"*

> *"since it could also potentially block their own messages"*

**A shared channel is a shared liability: the jam costs the jammer the same
bandwidth it costs the victim.**

WHY IT DOES NOT TRANSFER — **our store is private, and that single word closes
both attacks.** Our 16 integer slots are *"private per team, shared by all of a
team's units"*. There is no bidding, no shared queue, no anonymity, and no
cross-team read or write primitive anywhere in the Controller API — `read_store`
and `write_store` take an index and nothing else. Concretely:

| the BC2020 attack | why it is impossible here |
|---|---|
| flood the channel to deny bandwidth | our 16 slots are ours alone; nothing an opponent does can consume them |
| spoof a message they read as their own | we cannot write into their store at all |
| read their coordination | we cannot read their store at all |

**Filed as `transfers: no` because it will be re-proposed.** "16 shared integer
slots" reads like a shared bus, and the phrase *global communication store* in
the rules invites exactly the misreading The High Ground's paragraph would then
seem to license. It is not shared. Anyone who writes a plank premised on
touching the opponent's store has misread the API.

**The one real lesson that does survive** is the *self*-inflicted half of
confused's note — a channel can be jammed by its own owner. Our store is
buffered with **last-writer-wins**, and the s23 probes measured the failure:
five writers doing read-increment-write leave the counter at +1 with **all five
believing they are unit #0**. **We cannot be jammed by them; we can very easily
jam ourselves**, and that is a live bug class rather than a tactic. See
`docs/research/store-semantics-2026-08-09.md`.

WHAT WOULD REVIVE IT — one thing only: a rules change making any part of the
store cross-team readable or writable. That would resurrect both attacks
immediately and would be worth re-reading this file on the day it happened.
Nothing short of that does.

BUILDER HOOK — none, and that is the point. **Do not spend a probe on this.**

Related: [[cpu-timeout-induction]] · [store semantics](../store-semantics-2026-08-09.md) ·
[sweep 5](2026-08-09-sweep-5.md)
