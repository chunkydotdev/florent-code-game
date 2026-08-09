# The gunner-plant tiles do not repeat: HANDOVER queue #1's premise is false

**Research arm, session 24, 2026-08-09 12:3x CEST.**
**Version tag:** live **v91 "Eir 9c hivethaw"** = `bots/_v100hf`, tree `4558be91`,
single-file. Corpus synced at boot: archive **5081** replays, **5041** decoded,
**0 new**; reconciliation **1325/1325 = 100.0000%**.
**Sources: `corpus/events.tsv`, `corpus/builds.tsv`, `corpus/join.tsv` only.
Zero replay downloads. No bot edited, no arena run.**

---

## The claim being tested, and why it needed testing

`HANDOVER.md`, s24 boot block, queue item #1:

> **THE GUNNER-PLANT TILES.** The only item with a MEASURED TARGET rather than a
> hypothesis, and it is **enumerable, not behavioural**: name the >=5-kill tiles
> per map/seat and cover them (3 Ti barriers or a turret arc). One tile produced
> 45 kills. Specification, not doctrine.

The underlying measurement
(`builder-death-attribution-2026-08-09.md`) is not in dispute and I did not
re-derive it. What it establishes is that **within a game**, a few tiles do most
of the killing: 4,254 US home deaths from 1,559 distinct **(game, side, shooter
tile)** killers, tiles with >=5 kills carrying 47.3%.

**That grain is per-game.** "Name the tiles per map/seat and cover them" requires
something the attribution never measured and cannot measure at that grain: **that
the tile set REPEATS across different games on the same map and seat.** If it does
not, a shipped table is a fitted constant.

I tested the premise before anyone builds on it.

---

## Method

> **AMENDMENT, 2026-08-09 12:3x CEST, by the author.** As first published, this
> document twice asserted that the kill-grain decoder `dc_decode.py` "died with the
> third lane's scratchpad". **That is wrong.** The builder arm corrected me: it is
> preserved at `docs/research/scripts/side-lane-2026-08-09/dc_decode.py` (commit
> `1966026`), together with `rx_decode.py`, `bb_decode.py` and a README recording
> each one's validation. I have verified the files exist. **The claim was mine, it
> was checkable in one `ls`, and I did not check it before publishing.** The
> corrected statements are marked below. Nothing else in this document depends on
> it — every figure here comes from the committed corpus — but the practical
> conclusion changes: **the kill-grain follow-up is cheap, not blocked**, and I am
> running it rather than deferring it.

Enemy turret **plants** are already a first-class corpus row, so this needed no
decoder rebuild and no replay downloads. Confirmed against
`tools/corpus/replay_builds.py:84-92` and `replay_events.py`:

* `d2_own` = squared distance from the build tile to the **builder's own** core
  (NW corner of the 2x2 — same convention as the attribution doc).
* `d2_enemy` = squared distance to the **opposing** core.

So for a build by the opponent, `d2_enemy` is the distance **to our core**, and
`d2_enemy <= 32` reproduces the attribution doc's HOME band exactly.

`join.tsv` supplies `map` and `our_team`, giving the (map, seat) cell. Population:
**1,325 attributed games**, **6,515 enemy turret plants inside our home band**
(5,027 gunner, 1,380 sentinel, 108 launcher). 30 (map, seat) cells with >=20
plants.

Scripts (scratchpad, will die with this session; each is ~60 lines of
`csv.DictReader` over the committed corpus and is trivially rebuildable from this
document): `plant_repeat.py`, `plant_overlap.py`, `plant_order.py`,
`plant_table.py`.

---

## 1. The tiles repeat — and the repetition carries no information

Per (map, seat), enemy gunner plants land on **14 to 63 distinct tiles**, and
75–97% of plants land on a tile used in **>=2 different games**. Taken alone that
reads like strong repetition, and it is how a table would get justified.

**It does not survive a held-out test.** Split each cell's games in half, learn the
tile set on the first half, score coverage of plants in the second half, against
a null of *the same number of tiles drawn at random from the tiles anyone ever
plants on in that cell*:

| | mean over 30 (map, seat) cells |
| --- | ---: |
| coverage of held-out plants by the learned tile set | **70.4%** |
| coverage by a same-size RANDOM subset of the band | **66.6%** |
| **lift** | **+3.8pp** |

Worse, when the set is filtered to the tiles that are actually *shippable* — the
ones the enemy plants on and **we** essentially never build on — the lift is
**negative at every threshold tested**:

| filter (max share of games in which we build there) | tiles | cost | held-out cover | **lift vs random-in-band** | games with a conflict |
| --- | ---: | ---: | ---: | ---: | ---: |
| <=5% | 4.0 | 12 Ti | 4.8% | **−3.0pp** | 17.3% |
| <=20% | 8.6 | 26 Ti | 14.2% | **−3.0pp** | 44.1% |
| no filter (cover everything) | 38.5 | 116 Ti | 76.9% | **−2.1pp** | **99.9%** |

**Reading it plainly: knowing which tiles killed us before tells you nothing about
which tile will be used next, beyond the fact that it will be somewhere in the
home band.** The apparent repetition is an artefact of a small universe — the
d²<=32 band holds at most ~45 in-bounds tiles minus the 2x2 footprint, walls and
ore, so a training set naturally names most of it. Selecting *within* the band by
observed kill frequency is at best free and at worst actively worse than
arbitrary, because the tiles we never contest are the low-traffic ones.

**Honest note on the null.** It is the stringent one: it draws from the observed
plant universe (which includes held-out tiles), not from raw map geometry. Against
a knowledge-free geometric null the table would look excellent. I chose the
stringent null because it is the one that answers the actual decision — *is a
ranked table better than just naming the band?* — and the answer is no.

## 2. Geometry does not rescue it either

If tiles are unpredictable, a runtime rule keyed on distance might still work.
It does not: plants are spread flat across every ring of the band, and their
density tracks our own construction density (ratio of plant share to our-build
share stays in 0.61–1.74 with no trend).

| d² | 1 | 2 | 4 | 5 | 8 | 9 | 10 | 13 | 16 | 17 | 18 | 20 | 25 | 26 | 29 | 32 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| % of enemy plants | 4.4 | 5.1 | 10.3 | 11.2 | 4.9 | 5.7 | 7.7 | 6.6 | 5.8 | 6.6 | 3.4 | 3.8 | 11.8 | 6.3 | 3.6 | 2.6 |
| plant share ÷ our-build share | 0.96 | 0.73 | 1.47 | 0.79 | 0.84 | 1.33 | 0.82 | 0.77 | 1.73 | 0.94 | 1.00 | 0.61 | 1.74 | 1.14 | 0.70 | 1.62 |

There is no ring to defend. **50% of plants land inside d²<=10 and 50% outside** —
they are simply where buildable ground is.

## 3. The band is our own conveyor network, so occupying it is a trade

Across the corpus, **97.2% of the tiles the enemy plants on are tiles we also
build on**, and what we build there is overwhelmingly conveyor:

```
conveyor 30,004   sentinel 1,882   harvester 1,592   gunner 1,222   launcher 728   barrier 184
```

Per game, **35.4% of plants (2,309/6,515) land on a tile we build on in that same
game**, and **53.4% of games (624/1,168)** contain at least one such collision.
Blanket-covering the band is therefore **not** a free 116 Ti — it is 116 Ti plus a
fight with our own economy in 99.9% of games. (It also blocks our own builders'
movement, since a bot may co-occupy only a conveyor, splitter, or the allied core
— s23 probe result, carried forward, not re-verified here.)

## 4. But two thirds of plants land on ground we never touch

The same cut, from the other side, is the one genuinely encouraging number here:

| where the plant landed | n | share |
| --- | ---: | ---: |
| a tile we **never** build on in that game | 4,206 | **64.6%** |
| we built there **before** the plant | 1,156 | 17.7% |
| we built there only **after** the plant | 1,153 | 17.7% |
| same round | 0 | 0.0% |

**In 100% of the 1,156 "we were there first" cases, one of our buildings died on
that tile between our build and their plant.** So on the minority where we do
occupy, the blocker gets removed before the plant — median **202 rounds** between
our build and their plant, so this is a slow grind, not a clear-and-plant tempo
play.

**LIMIT, stated rather than inferred across:** the corpus `DEATH` row cannot
distinguish an enemy kill from our own free `destroy()` — both emit
`removeEntity`. So "they cleared our building" is *one* reading of that 100%, and
"we removed our own building and they took the vacancy" is another. **This
document does not choose between them, and neither should the builder.**

## 5. Timing, and a first look at removal

Plants are a whole-game phenomenon, not an opening: median round **154**, p10 11,
p90 547. **26.3% land by r50, 38.3% by r100, 49.2% by r150, 74.0% by r300.** Any
pre-placed cover must be down early to catch even a quarter of them.

> **AMENDMENT 2, 2026-08-09, by the author — THE SENTENCE BELOW IS WRONG AND THE
> TABLE IS CENSORED.** Follow-up analysis
> (`in-base-plant-survival-tail-2026-08-09.md`) shows (a) the 41.4% is roughly 40%
> **right-censoring artifact** — 57.5% of "survivors" had under 100 rounds of game
> left, and the honest censored tail is **~25%**, not 41.4%; and (b) **"not obviously
> worse than the field's" does not survive the censoring fix.** Matched at a fixed
> horizon, enemy plants in our band survive **25.2%** (n=3,179) against our plants in
> theirs at **20.3%** (n=1,590) — **+4.9pp, z=3.77, p=1.6e-4**, and **MH odds ratio
> 1.31 across 482 same-replay both-sides comparisons.** **We remove enemy plants
> modestly WORSE than the field removes ours, at every horizon tested.** The raw
> table is retained below only so the correction is legible; **use the follow-up
> document's numbers, not these.**

Removal is already happening and is ~~**not obviously worse than the field's**~~
**worse than the field's once censoring is handled — see Amendment 2**:

| | n | died in game | survived to end | median lifetime of those that died |
| --- | ---: | ---: | ---: | ---: |
| **enemy** turret planted inside **our** band | 6,407 | 58.6% | **41.4%** | 14 rounds |
| **our** turret planted inside **their** band | 2,610 | 65.1% | 34.9% | 12 rounds |

**This is the one place I would spend the next effort, and I am labelling it a
lead, not a finding.** *(It was spent — see Amendment 2 and the follow-up doc; the
lead was right about where to look and wrong about the size and the sign.)* The
problem is visibly in the ~~41.4%~~ **~25% censored** tail, not in mean
removal speed — and the 45-kill tile from the attribution doc is by construction a
member of that tail. What separates a planted gunner that dies in 14 rounds from
one that lives to round 1000 is not answerable from the plant/death grain alone;
it needs the kill-attribution decoder — ~~which died with the third lane's
scratchpad and would have to be rebuilt~~ **which is preserved and runnable at
`docs/research/scripts/side-lane-2026-08-09/dc_decode.py` (see the amendment at the
top). The follow-up is cheap and is in flight.**

---

## What this changes

1. **Queue #1 as written is refuted.** "Enumerable, not behavioural" is false: the
   ≥5-kill tile list does not transfer across games, and a shipped per-map/seat
   table would carry **+3.8pp of information at best and −3.0pp at the sizes worth
   shipping.** It is a fitted constant.
2. **The band, not the tile, is the only thing that transfers** — and the band is
   16–72 tiles, 48–216 Ti of cover, jointly occupied by our own conveyor network
   in 99.9% of games. That is a real strategic trade, and it deserves to be
   evaluated as one rather than smuggled in as a 3 Ti fix.
3. **The 64.6% of plants on ground we never touch is the affordable part** of that
   trade and the only version of "cover the tiles" I would price at all. It is
   still a doctrine change (pave the dead ground early), not a specification.
4. **The remaining lever is reactive removal against the 41.4% tail**, which is
   where the grinding tiles live. Unmeasured here.
5. **Nothing above says the attribution doc was wrong.** Its within-game
   concentration is real. What is wrong is the inference from within-game
   concentration to a cross-game table — the same shape as this lane's s23 failure
   family, *a statistic standing in for a measurement*.

## Provenance

Corpus at `manifest.json` of 2026-08-09 12:15 CEST. All five tables above are
reproducible from `corpus/events.tsv`, `corpus/builds.tsv` and `corpus/join.tsv`
with the column semantics stated in the Method section. Nothing here consumes the
kill-grain attribution beyond quoting its published figures.

**One correction has been applied to this document since first publication** — see
the amendment block in the Method section. It was my error, caught by the builder
arm, and it is recorded rather than silently edited.
