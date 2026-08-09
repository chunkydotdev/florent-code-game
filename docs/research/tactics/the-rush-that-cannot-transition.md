---
tactic: FAILURE MODE — the rush that does damage, does not kill, and has no economy behind it
source: https://battlecode.org/assets/files/postmortem-2019-smite.pdf
origin: Battlecode 2019 / smite (finalists); independently BC2021 3 Musketeers and BC2025 The Kragle
evidence: documented
transfers: yes
---
WHAT IT IS — The most-repeated failure in the whole Battlecode record, sighted
three times in three different years by three teams that all finished high.

**BC2019 smite** — they added a preacher rush an hour before a deadline:
> *"So we'd do significant damage with our rush, but we never transitioned out of
> it, and eventually lost."*
and their own verdict on the resulting bot:
> *"we had succeeded in our attempt to build a do-nothing bot"*
Referent: the sentence before establishes the cause — one pilgrim was left behind
to mine karbonite and mined fuel instead, so the economy never restarted after
the attackers left. They also record the cost:
> *"All but one of the map losses we experienced in the seeding tournament"* …
> *"was due to a bug in the rush"*

**BC2025 The Kragle**, on their own conditional rush:
> *"we never had good logic for what to do after a rush completed"*
— and they were relying on *"the rush being disruptive enough to give us a
massive lead that we couldn't fumble."*

**BC2021 3 Musketeers** are the only team in the record with a *fix*: they
repurposed the failed attackers instead of discarding them.
> *"our failed rush politicians (which had a significant amount of influence),
> would turn into what we called Golem Politicians"* …
> *"These politicians would patrol the base they were assigned, waiting to kill
> big enemies that approached it."*

WHY IT MATTERS HERE — This is the failure mode most likely to kill the Loki plank,
because our ruleset makes the drawdown **unrecoverable in a way theirs was not**.
Every titanium spent on ammo is gone: there is no refund, no salvage, and no
passive ammo income to rebuild from. Titanium spent on a forward sentinel is
recoverable only in the sense that `destroy()` removes its +20% scale
contribution — the 30-51 Ti is not returned. And the cost curve punishes the
retry: gunners and sentinels scale **+20% each**, so a second attempt after a
failed first is bought at inflated prices while the defender's heal stays at
4.00 HP/Ti forever.

Worse, our tiebreak chain makes a failed rush a **double** loss. Key #1 is
cumulative titanium *delivered*, an integral over the whole game. Rounds spent
attacking are rounds not delivering, so the failed attack does not merely fail to
win — it forfeits the fallback we currently win (353 games reached r1000; we won
57.2%).

WHAT THE FIX LOOKS LIKE — The Golem shape is the transferable one, and our version
is unusually good: an attacking builder bot that survives a failed strike is a
**full-price builder bot standing in enemy territory**, and it can `build`,
`heal`, or `destroy` on any orthogonally adjacent tile. It does not have to walk
home to be worth 30 Ti. The two non-suicidal terminal states are (a) plant
barriers/harvester-denial on enemy-side ore — `ore-tile-denial.md` — or (b) walk
back and join the home heal screen at 4.00 HP/Ti, which is our measured asset.
What it must NOT do is `self_destruct()`, which deals no damage and hands the
enemy a free cost-scale refund on nothing.

BUILDER HOOK — Before any Loki strike plank ships, define its **terminal state**
in code, not in prose: on abort, every surviving strike unit gets an explicit
role reassignment. Then measure the thing smite measured — *delivered titanium in
the 100 rounds after an aborted strike* — and compare against games where no
strike was attempted. If it does not recover, the abort logic is the plank, not
the strike.
