# The heal channel is NOT the constraint. It is 18% used, and the ceiling is 2.1× their peak.

**Research arm, session 24, 2026-08-09.** The CAD core-kill read's follow-up item **(b)**
— *"per-round heal-throughput ceiling arithmetic vs measured CAD DPS curves (free, rule
arithmetic — S1 before anything)"* — taken on the builder's ask because it is **the one
item on the board that could refute an entire class of response at the spec level.**

**It does not. The class survives, and the binding constraint turns out to be something
neither of us had named.**

**Version tag:** live **v92** = `bots/_v115dodge`, submission `7b1d8d73`. **No corpus
query, no decode, no replay downloads** — this is rule arithmetic against already-published
measurements, which is why it took minutes rather than a session.

---

## 0. The rules it rests on, each read from the installed engine rather than remembered

`.venv/lib/python3.13/site-packages/fcode/_types.py`, verbatim:

* `heal()`: *"Heal all friendly entities on an orthogonally adjacent tile (not diagonal,
  not this builder bot's own tile) by 4 HP. If both a friendly builder bot and a friendly
  building are on the target tile, both are healed. **Costs 1 titanium and one action
  cooldown.**"*
* `GameConstants`: `HEAL_AMOUNT = 4`, `BUILDER_BOT_HEAL_COST = 1`, `GUNNER_DAMAGE = 7`,
  `GUNNER_FIRE_COOLDOWN = 1`, `GUNNER_AMMO_COST = 4`, `SENTINEL_DAMAGE = 18`,
  `SENTINEL_FIRE_COOLDOWN = 2`, `SENTINEL_AMMO_COST = 10`.

**"One action cooldown" resolves to one heal per builder per round.** The same constant
family gives `GUNNER_FIRE_COOLDOWN = 1` for a turret the official docs describe as *"7
every round"*, so cooldown *N* means *acts once every N rounds*. **A healer heals every
round.** This was the one assumption that could have halved the whole answer, so it was
checked rather than inherited.

## 1. The geometric cap on the heal channel

The core is a **2×2, four tiles, ONE entity** — so healing *any* footprint tile heals the
core. The tiles from which a footprint tile is orthogonally adjacent:

| position | count | note |
| --- | ---: | --- |
| **outside the footprint** (the "seats") | **8** | the classic ring |
| **on the footprint itself** | **4** | a builder may co-occupy the allied core; it cannot heal its *own* tile but can heal the adjacent footprint tile |
| **HARD CAP** | **12** | **= 48 HP/round, for 12 Ti/round** |

**The 4 on-footprint healers rest on the s23 co-occupation probe** (a bot may co-occupy
only a conveyor, splitter, or the allied core) — **which is a prior-session result of my
own lane, and the lane call authorising those probes is still open with Magnus.** So I
state the conclusion **both ways**, and it does not depend on them:

* **12 healers → 48 HP/round** (with on-footprint co-occupation)
* **8 healers → 32 HP/round** (seats only — safe under any reading)

## 2. CAD's damage, nominal and measured

**Nominal** — every core-shooting turret firing every available round, at CAD's measured
mix of 189 gunners : 144 sentinels (57/43):

| population | core-shooters/game | nominal DPS | vs 48 ceiling | vs 32 seats-only |
| --- | ---: | ---: | --- | --- |
| our wins | 1.9 | 14.9 HP/rd | under | under |
| tiebreaks | 2.9 | 22.8 HP/rd | under | under |
| all games (median) | 4.0 | 31.5 HP/rd | under | at the line |
| **loss games** | **5.6** | **44.0 HP/rd** | **under** | over |

**Even the loss-game nominal maximum — every turret firing every round, which never
happens — sits under the 48 HP/round ceiling.**

**Measured** is far below nominal, and this is the number that matters. CAD loss games:
**2,117 damage/game against 1,613 healed (ratio 0.76)**, over a window running from the
first gunner planted (median r172) to core death (median r361) — **~189 rounds**:

| quantity | HP/round | in healers |
| --- | ---: | ---: |
| **mean incoming damage** | **11.20** | — |
| **mean healing we actually deliver** | **8.53** | **2.1 healers** |
| **peak siege DPS ever measured** (`_v100hf:554`, two decode corpora) | **23.22** | 5.8 healers |
| **ceiling (12 seats)** | **48.00** | 12 |
| **ceiling (8 seats only)** | **32.00** | 8 |

## 3. THE ANSWER

**The defensive class is NOT refuted at the spec level, and it is not close.**

* The ceiling is **2.1× the highest siege DPS ever measured against us** (48 vs 23.22),
  and **1.4× it even counting only the 8 safe seats.**
* We are running the channel at **2.1 healers of 12 — 18% utilisation** — in exactly the
  games we lose.
* Matching the *peak* ever measured needs **5.8 healers**, under half the seats.
* And the titanium exchange is in our favour throughout: **0.556–0.571 Ti per HP dealt for
  them against 0.250 Ti per HP healed for us — a 2.22:1 to 2.29:1 defender edge**, which
  re-derives the standing 2.2:1 fact from a different direction.
* To sustain the mean measured incoming, **they pay 6.2 Ti/round and we pay 2.8 Ti/round.**

**The heal channel is not the bottleneck. We simply do not staff it.**

## 4. SO WHY DID ESCALATE FAIL AT −7.8pp? — and this is the actual finding

The measured refutation of *"scale the heal detail"* and this arithmetic are both correct,
and reconciling them names the real constraint.

**It is not titanium and it is not geometry. It is BUILDER-TURNS.**

A healing builder costs **1 Ti** — trivial against a bank we are documented to sit on. What
it actually costs is **its action that round**: acting and moving are mutually exclusive
for a builder, so a healer is a builder not building, not harvesting, not linking, and not
walking anywhere. **The 12 Ti/round ceiling price is a rounding error; the 12
builder-turns/round is the whole cost.** ESCALATE measured that cost and it exceeded what
the defence saved. **The Ti arithmetic never priced it, which is why the channel looks free
and is not.**

**Three independent lines now converge on the same conclusion**, which is why I am
confident enough to state it as a recommendation rather than an option:

1. **This arithmetic**: the channel has 82% headroom and costs almost no titanium.
2. **ESCALATE, −7.8pp**: paying for it with *scheduled* builder-turns loses more than it
   saves.
3. **Tactics sweep 10** (`fortify-on-idle`, Overmind/Screeps): the field's rule is to
   fortify **only on idle time** — *"a strictly-dominated-time change costing zero
   scheduled builder-turns"*.

**⇒ Staff the heal channel from IDLE builder-turns only.** That is the one form that takes
the 82% headroom without paying the price ESCALATE measured. It is not "more healers"; it
is "healers when the builder had nothing else to do", which is a scheduling change rather
than an economic diversion.

## 5. What this does NOT say

* **It does not say a heal-detail build will work.** It says the *channel* is not the
  refutation, so a failure would be a failure of the *response*, not of the class. That
  distinction is what item (b) existed to establish.
* **It does not touch the sentinel geometry problem.** 65% of CAD's core damage is
  stand-off sentinels at median d²=26, 28% planted outside our home band. Healing answers
  the *damage*; it does nothing about the *source*, and tile denial cannot reach d²=26.
  **The two pieces are independent and a response must price both** — that was the CAD
  read's own warning and this result does not weaken it.
* **It does not establish that we CAN staff 12 seats.** `MAX_TEAM_UNITS = 50`, and builder
  cost scales **+20% each** — the 12th builder alone costs **30 × 1.2¹¹ = 223 Ti** to
  field. Whether the bodies exist at the moment they are needed is an empirical question
  this arithmetic cannot answer.
* **The 4 on-footprint seats are inference from an engine probe, not from a rule I can
  quote.** Everything above holds on the 8 outside seats alone.

## 6. The cheapest thing that would sharpen it

**A per-round census of how many core seats we actually staff, and when.** The 2.1-healer
figure here is derived from a game total divided by an assumed 189-round window — it is an
*average over the window*, and the core dies to *sustained* DPS, not average. `bb_decode.py`
already tracks core-ring adjacency and heal attribution, so the distribution of staffed
seats per round is one decoder pass away. **If staffing is 2.1 flat, the headroom is real;
if it is 6 during the siege and 0 otherwise, this whole document is measuring the wrong
thing.** I would not build a heal response before that cut.

## Provenance

Arithmetic only. Inputs: `docs/research/cad-core-kill-2026-08-09.md` (2,117 / 1,613 / 0.76;
189 gunners : 144 sentinels; 5.6 / 2.9 / 1.9 core-shooters per game; r172 → r361 window),
`bots/_v100hf/main.py:554` (peak measured siege DPS 23.22), and `fcode/_types.py`
(constants and the `heal()` docstring, read directly from the installed engine). No number
here is new measurement; the contribution is the ceiling, the utilisation, and the
reconciliation with ESCALATE.
