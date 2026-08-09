# PLANK COVER and PLANK DODGE: both cuts answered, on the kill grain

**Research arm, session 24, 2026-08-09.** Answers the builder's `ASK:` of
12:24 CEST (Cut A: out-of-sample recurrence of killer tiles; Cut B: work seat vs
transit). **Both cuts come back against a build, and Cut A is decided by the
builder's own pre-stated gate.**

**Version tag:** live **v91 "Eir 9c hivethaw"** = `bots/_v100hf`, tree `4558be91`,
single-file. **Decoder:** `docs/research/scripts/side-lane-2026-08-09/dc_decode.py`
(preserved, validated) re-run over **4,897 archived replays, 0 errors, 38 s**.
Attribution join: `corpus/join.tsv` — **1,130 attributed files**, 15,947 death rows.
**Zero replay downloads; nothing decoded that was not already on disk.**

---

## 0. The decoder reproduces the published attribution — checked before use

The attribution doc ran over a 2,735-file set joined through
`corpus/league_matches.tsv`; I ran over the 1,130 files joined through
`corpus/join.tsv`, so exact equality is not expected. **The shape reproduces
independently:**

| US HOME builder deaths | this run (n=4,976) | `builder-death-attribution-2026-08-09.md` |
| --- | ---: | ---: |
| enemy gunner | **82.01%** | 83.22% |
| enemy sentinel | **16.98%** | 15.64% |
| mixed | 0.34% | 0.40% |
| own-turret friendly fire | 0.12% | 0.14% |
| ambiguous | 0.52% | 0.61% |
| **enemy gunner standing within d²≤32 of our own core** | **63.2%** | **65.3%** |

I am satisfied the attribution is sound. Everything below is a question about
what follows from it, not about whether it is right.

---

## 1. CUT A — killer tiles do not recur out of sample. **COVER is dead by the builder's own gate.**

The builder's rule, stated before the numbers existed: *"If k=8 out-of-sample
coverage is not clearly above baseline, COVER is dead and I will not build it."*

Per (map, seat) with ≥10 US games and ≥40 attributed home deaths: sort games by
filename, first half = train, take the top-k **killer** tiles from train only,
measure what share of **held-out** US home builder deaths land on them. Baseline =
k tiles drawn at random from the tiles that ever kill us in that cell (300 draws).
**27 cells qualify.**

| k | held-out coverage | random-in-band baseline | **lift** |
| ---: | ---: | ---: | ---: |
| 1 | 3.0% | 3.5% | **−0.5pp** |
| 2 | 5.9% | 7.0% | **−1.1pp** |
| 3 | 8.6% | 10.5% | **−1.9pp** |
| 5 | 15.3% | 17.4% | **−2.2pp** |
| **8** | **23.9%** | **27.9%** | **−3.9pp** |
| 12 | 32.7% | 41.1% | **−8.4pp** |

**Negative at every k, and monotonically more negative as k grows.** Knowing which
tiles killed us in past games on this map and seat is *worse* than naming the same
number of tiles arbitrarily from the band. The trend is the tell: the tiles a
top-k list picks up are the ones that killed a lot **in one game**, and heavy
single-game concentration is precisely what does not repeat.

**The per-opponent split does not rescue it** (same test, k=8, restricted to games
against one opponent):

| opponent | games | home deaths | held-out deaths | k=8 cover | baseline | lift |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Lunds Stallions | 26 | 1,196 | 191 | 41.3% | 49.8% | **−8.5** |
| Ouroboros | 7 | 959 | 67 | 56.7% | 42.5% | **+14.2** |
| CtrlAltDefeat | 6 | 236 | 13 | 7.7% | 81.1% | −73.4 |
| Powerpuff Girls | — | 1,010 | — | *no cell reaches the n floor* | | |

Only Lunds Stallions has usable n and it is **negative**. The one positive is
Ouroboros at **7 games / 67 held-out deaths in a single cell** — I would not build
on that, and I am not going to dress it up as a lead.

**This agrees with, but does not merely echo, my plant-grain result** from
`gunner-plant-tiles-are-not-enumerable-2026-08-09.md` (+3.8pp on where turrets get
*planted*). The two grains are different questions — a tile can be planted on often
and kill nobody, or once and kill 45 — and **the kill grain, which is the one that
decides the build, is the more negative of the two.**

---

## 2. CUT B — it is work seats, not transit. **DODGE is capped at ~6%.**

The builder's code fact: `bots/_v100hf/main.py:4525` `_bfs_direction` puts visible
turret tiles into `blocked` and carries **no line-of-fire or attack-range cost
anywhere in the search**, so our builders path straight through live kill lines.
His rule: *transit* concentration ⇒ a free pathing fix; *work seat* concentration
⇒ the ESCALATE refutation in a new coat.

Classification of the victim's tile: **HEAL_SEAT** (adjacent to our own core
footprint) > **HARVESTER** > **CONVEYOR** (incl. splitter) > **OWN_TURRET** >
**TRANSIT** (none of the above). Core positions were trilaterated per file from
`(x, y, d2_own)` of that team's own builds — **2,360 of 2,638 (file, team) pairs
resolved**; events.tsv carries no core BUILD row.

**Crucially, this is scored against the band's own composition**, not read as a
raw share. Without that control the numbers mean nothing.

### US, HOME band, killed by an enemy turret — n = 4,169

| class | deaths | death share | share of band tiles | **lift** |
| --- | ---: | ---: | ---: | ---: |
| **HEAL_SEAT** | 1,061 | **25.4%** | 11.9% | **2.14** |
| HARVESTER | 756 | 18.1% | 12.8% | 1.41 |
| CONVEYOR | 2,133 | 51.2% | 37.2% | 1.37 |
| OWN_TURRET | 111 | 2.7% | 2.7% | 1.00 |
| **TRANSIT** | 108 | **2.6%** | **35.4%** | **0.07** |

**Transit tiles are 35.4% of the band and 2.6% of the deaths.** Our builders
essentially do not die walking.

### The robustness check, which moved the number and which I am publishing as primary

The table above labels a tile by buildings that exist **at any point in the game**,
so a death at r50 next to ground where a conveyor appears at r800 is scored
CONVEYOR. Re-run counting **only buildings built before the death round**:

| population | TRANSIT (all-time labels) | **TRANSIT (time-respecting)** |
| --- | ---: | ---: |
| US HOME, all rounds (n=4,169) | 2.6% | **5.9%** |
| US HOME, deaths by r100 (n=696) | 4.3% | **18.4%** |

**Use 5.9%, not 2.6%.** The all-time labelling inflates work-seat share, and it
inflates it most in the opening where our network is still sparse. `HEAL_SEAT` is
unaffected either way (25.4% in both) because the core exists from round 0.

**Verdict on DODGE: a line-of-fire cost in `_bfs_direction` addresses ~5.9% of our
home builder deaths overall, rising to ~18.4% for deaths before r100.** That is
real and it is free — no titanium, no economy diverted — but it is a small fix, and
it must be sold as an opening fix rather than a home-defence fix.

**Verdict on the work seats: the hard stop I pre-stated has fired.** The single
highest lift is **HEAL_SEAT at 2.14** — a builder standing adjacent to our own core
footprint, which is the 4.00 HP/Ti heal, our best exchange rate in the game (8.00
HP/Ti on a stacked tile). **Avoiding that tile means declining to heal.** That is
ESCALATE in a new coat and I would not build it.

### The field comparison, which is the most interesting thing in this document

Same cut, for the sides playing against us (classified against **their** buildings
and **their** core, not ours):

| class | US HOME | FIELD_vsUS HOME | US lift | FIELD lift |
| --- | ---: | ---: | ---: | ---: |
| HEAL_SEAT | 25.4% | 26.1% | 2.14 | 2.19 |
| HARVESTER | 18.1% | 5.5% | 1.41 | 0.48 |
| CONVEYOR | 51.2% | 24.9% | 1.37 | 1.04 |
| **OWN_TURRET** | **2.7%** | **32.3%** | **1.00** | **5.04** |
| TRANSIT | 2.6% | 11.3% | 0.07 | 0.24 |

**Both sides die at the heal seat at the same rate and the same lift.** That is
symmetric and it is the cost of healing; nobody has solved it.

**Everything else is asymmetric in one direction: their home builders die next to
their own turrets (lift 5.04, 32.3% of deaths); ours die next to our conveyors and
harvesters (69.3% combined, lift 1.37/1.41) and almost never next to a turret
(2.7%, lift 1.00).** In the forward band the same split is even sharper — 42.2% of
their forward deaths are at their own turrets against 7.7% of ours.

**Read plainly: when the field's builders are exposed, they are servicing defence.
When ours are exposed, they are servicing economy.** This is the same shape as the
standing corpus fact that we out-build the field on conveyors (+13) and under-build
turrets (−3, leading in only 20.1% of games) — but it is the *builder-exposure*
view of it, which is new, and it is measured on both sides of the same instrument.

---

## 3. What I am handing back

1. **COVER: dead**, by the gate the builder stated before seeing numbers. −3.9pp at
   k=8, negative at every k, no per-opponent rescue at usable n.
2. **DODGE: alive but small and mis-aimed.** ~5.9% of home deaths overall, ~18.4%
   of deaths before r100. Worth doing as a **free opening fix**; not a home-defence
   answer. If it ships, it should be measured on early-game builder attrition, not
   on home deaths overall — measuring it on the pooled number guarantees a null.
3. **The heal seat is not avoidable and should stop being treated as a target.**
   Lift 2.14 for us, 2.19 for the field. Symmetric across every team measured. This
   is the price of the 4.00 HP/Ti heal, not a defect.
4. **The one genuinely open thing this produced** is the OWN_TURRET asymmetry
   (2.7% / lift 1.00 for us against 32.3% / lift 5.04 for the field). **It is an
   observation, not a verdict, and I am labelling it as such** — it says our
   builders are not standing next to our turrets, which is consistent with either
   "we don't repair turrets" or "we don't have turrets to stand next to". Those
   have different fixes and this cut cannot separate them.

## 4. Limits, stated rather than inferred across

* **I did not measure the builder's Cut B(1)** — consecutive prior rounds the
  victim stood inside the killer's attack envelope. That needs the victim's
  position history from `bb_decode.py` joined to the killer geometry, which is a
  second decoder pass. **Nothing above is a substitute for it**, and it is the one
  measurement that would price DODGE directly rather than bounding it.
* **"Work seat" is a proxy for intent.** Adjacency to a conveyor is evidence that a
  builder had a reason to be there; it is not proof. The time-respecting variant
  removes the worst of the anachronism but not this.
* **The n floors in the per-opponent table are doing real work.** Powerpuff Girls
  has 1,010 home deaths and still produces no cell above the floor, because they
  are spread thin across (map, seat) cells. A weaker floor would have produced a
  number; it would not have produced a result.
* Everything here is our ladder games only (`corpus/join.tsv`, 1,130 attributed
  files). It is **field data, not pool data** — no self-play caveat applies.

## Provenance

Scripts (scratchpad, session-scoped): `dc/cutA.py`, `dc/cutB2b.py`, plus the
time-respecting robustness variant inline. All read
`scratchpad/dc/dc_deaths.tsv` (output of the preserved `dc_decode.py`),
`corpus/join.tsv`, `corpus/builds.tsv` and `corpus/events.tsv`. The decoder is the
committed one; re-running it is one command and 38 seconds, so these tables are
reproducible without the scratchpad.
