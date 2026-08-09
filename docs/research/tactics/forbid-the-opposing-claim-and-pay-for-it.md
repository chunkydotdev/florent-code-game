---
tactic: (D) A DIRECTIONAL RESERVATION on each tile makes head-to-head structurally impossible — a real guarantee, with a published price tag of 30 points of success rate
source: https://jiaoyangli.me/files/2021-ICAPS.pdf
origin: Christian Wälter's CPR approach (Flatland 2019), described and benchmarked by the 2020 Flatland Challenge winners — Li, Chen, Zheng et al., "Scalable Rail Planning and Replanning: Winning the 2020 Flatland Challenge", ICAPS 2021
evidence: documented
transfers: partial
---

WHAT IT IS — the only mechanism found anywhere in this sweep that makes our
`HEAD_TO_HEAD` class **impossible by construction** rather than merely rarer. The
winners describe it — the referent of *"Its"* is CPR, the approach the paragraph
introduces:

> *"Its main idea is that, after it plans a path for a train, it reserves the directions of the cells on the path so that future trains cannot traverse these cells in the opposite directions. This rule prevents any two trains from traversing a single-track corridor in opposite directions and thus guarantees deadlock-freeness."*

**And they benchmarked it against their own winning approach on a named fixture:**

> *"For example, for instances in Test 33 (which contains 1,006 trains), our approach obtained a mean reward of 0.649 with a success rate of 96% on our server, while CPR obtained a mean reward of 0.406 with a success rate of 66%."*

> *"We therefore did not pursue CPR."*

**The same trade appears independently in the other winner's writeup.** Andreica
tried strict time-separation instead of strict direction-reservation and reports
both the win and the cost, on the official 250 tests:

> *"Implementing this approach indeed avoided deadlocks in all the cases and I could tune it to get an average of ~97.5%(*) of agents reaching their destinations."*

> *"The problem was that now the agents were spaced too far apart in time, reducing the available “throughput”."*

**A caveat that must travel with those two percentages**, in his own words — the
`(*)` markers are his:

> *"it’s possible that the scores reported here are also affected by a similar 0.7% difference (so a 96.5% score should in fact be 97.2%, and a 97.5% score should in fact be 98.2%)."*

His earlier detect-and-abandon version scored *"96.5%(*)"* on the same fixture, so
**avoid beat detect by about one point, with a systematic offset that does not
change the ordering.**

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **Our head-to-head rate is 9.94% of blocked mass against a field 1.57% — 6x.**
  The binding-tile cut calls it *"close to a live bug"* and *"ours specifically"*.
  This is the mechanism that removes it categorically.
- **Our version is cheaper than theirs, because our reservation is already stored
  in the world.** CPR must maintain a reservation table. **A conveyor's facing IS
  the reservation** — `get_direction(id)` reads it back for free. So our invariant
  is a *local read*, not a table: **before building a conveyor at `pos` facing `d`,
  check the tile at `pos.add(d)`; if it holds a friendly conveyor whose own facing
  points back at `pos`, refuse.** One `get_tile_building_id` and one `get_direction`.
- **Our resource is static and theirs is not, which favours us.** CPR's cost comes
  from *permanently* denying a corridor to future trains that only need it for a few
  timesteps. **A conveyor's facing is genuinely permanent and genuinely
  single-purpose** — a tile that carries titanium east is not also needed to carry
  it west. The throughput CPR sacrifices is throughput we do not have to sacrifice.
- **And our engine has the escape hatch CPR lacks:** `destroy()` is free, costs no
  action cooldown, is unlimited per turn, and per the organisers' reference
  *"returns any resources currently in transit on that tile to your team's
  balance."* **So a reservation here is revocable at zero cost**, which is precisely
  the property whose absence made CPR expensive.

WHAT WOULD KILL IT —

- **⚠ THE PRICE IS PUBLISHED AND IT IS LARGE.** 96% → 66% success at 1,006 agents.
  The people who measured it declined to use it. **Anyone proposing a hard
  no-opposing-claim rule here must say why our version escapes that cost**, and the
  three arguments above are *arguments*, not measurements. **They could be wrong.**
- **The blind spot is not covered by this rule.** CPR forbids a *future* train
  claiming an opposing direction. It does nothing about two claims made in the
  *same* step — see
  [`the-symmetric-claim-is-the-blind-spot`](the-symmetric-claim-is-the-blind-spot.md),
  which is very likely where our 6x actually comes from.
- **Flatland is single-team.** Nothing here addresses an enemy conveyor, and our
  `ENEMY_NET` class (0.74%) is small enough that it does not matter — but the rule
  must check `get_team` before refusing, or an enemy conveyor pointing at us
  becomes a self-imposed veto on our own construction.

BUILDER HOOK — the refusal is four lines and it is the *cheapest* plank in sweep 19:
before `build_conveyor(pos, d)`, look at `pos.add(d)`; if it holds a **friendly**
conveyor or splitter whose facing output tile is `pos`, refuse and pick another
facing. Gate on the mechanism counter — **head-to-head pairs created per game,
control versus treatment** — exactly as the LOKI-10 prereg gates its turret refusal,
and for the same reason: the outcome channel is closed in 93% of our games, so Elo
cannot resolve it.
