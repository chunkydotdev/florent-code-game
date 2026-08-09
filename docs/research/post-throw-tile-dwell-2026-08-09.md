# Post-throw tile dwell: how long does a thrown builder bot sit where it lands?

**Built 2026-08-09T14:22Z (session 24, research arm), answering Q1 from the builder arm.**

**Version tag**
- Live slot **v94 = `bots/_v115dodge`**, tree hash `6ae6871c`.
- Corpus git sha **`7418e13`**, manifest `built_utc 2026-08-09T14:08:17Z`,
  `archive_replays = 6233`.
- **Frozen input list**, snapshotted before the first read so the keeper's ~10-min
  auto-sync could not move it under the run:
  - **6,233 replay paths** = every path under `replay_archive/` whose basename
    appears in `corpus/decoded.txt` (6,193 unique basenames; **35 basenames exist
    at two paths** under the `diag_ad_*` subdirectories, and both copies are read —
    see Validation, this cost one whole pass to find).
  - `corpus/join.tsv` snapshot — 1,445 data rows.
  - `corpus/throws.tsv` snapshot — 97,995 data rows.
- Decoder: `docs/research/scripts/post-throw-dwell-2026-08-09/throw_dwell.py`
  (reuses `tools/replay_census.py` helpers and the throw-detection rule of
  `tools/corpus/replay_throws.py`; no new replay parser was written).
- Scan cost: **31 seconds wall** over 6,233 files at `-j 8`, 0 file errors.

---

## THE ANSWER, FIRST

**The modal post-throw dwell is 1 round, and for the case the kidnap plank
actually cares about — a launcher throwing an ENEMY builder bot — 96.4% of
victims are off the landing tile within one round** (and 97.5% when *we* are the
thrower).

**Kidnap-into-ray must be priced as DISPLACEMENT plus at most one shot, not as a
kill.**

Against a 40 HP builder bot, from the spec arithmetic the builder already
established (gunner 7 dmg / 6 shots / ~11 rounds; sentinel 18 dmg / 3 shots /
~7 rounds), the archive says:

| ray exposure needed | gunner kill (11 rounds) | sentinel kill (7 rounds) |
| --- | --- | --- |
| share of enemy-victim throws that stay that long | **0.42%** | **0.61%** |
| share of *our* throws of an enemy bot that stay that long | **0.46%** | **0.75%** |

So the kill outcome happens in roughly **1 throw in 200**. The realistic yield is
**one gunner shot (7 HP, 17.5% of the bot) or one sentinel shot (18 HP, 45%)**,
and about a third of the time the victim steps off in the *same round* it lands,
so even that one shot is not guaranteed — it depends on whether the turret's unit
turn precedes the victim's.

---

## Question

After a launcher throw, how many rounds does the thrown builder bot remain on its
**landing tile**? Distribution, not median; split by who threw (us vs them) and by
whether the victim was the thrower's own bot or the opponent's.

Sub-question: does landing **reset or penalise the victim's move cooldown**? The
official rules are silent (`docs/reference/official-docs.md` was grepped by the
builder and says nothing), so this has to be inferred from the dwell shape.

## Method

**Throw detection** is the rule from corpus-howto trap 3, unchanged, so the throw
sets are directly comparable to `corpus/throws.tsv`: a throw is a
`moveBuilderBot` (Update field 2) whose destination is **more than one tile
(manhattan)** from the bot's previous position; the thrower is a launcher alive at
**d² ≤ 2 of the pre-throw tile**, diagonals included; if launchers of both teams
are in range the throw is `UNATTRIB` and is never guessed.

**Dwell** is read off the same event stream:

```
dwell = (round of the first later event that puts the bot on a tile != T) - r0
```

`moveBuilderBot` is the only positional event a builder bot emits, so this is
exact rather than inferred. **`dwell` can be 0**: the launcher acts on its own
unit turn, and the victim's `run()` may come later in the *same* round buffer, in
which case the victim never sits on `T` at a round boundary at all. That case is
kept, not clamped — it turns out to carry the answer to the cooldown question.

**Exit reasons** are tracked separately and censored groups are never folded into
the moved-off distribution:

| exit | meaning | count |
| --- | --- | --- |
| `step` | left `T` under its own power (next move ≤ 1 tile) | 91,560 |
| `rethrow` | next positional event was another throw | 5,450 |
| `died` | removed while still on `T` — **right-censored**, and this is the kill outcome | 492 |
| `end` | game ended with the bot still on `T` — **right-censored** | 497 |

**Populations.** `corpus/join.tsv` maps a replay file to which team index is US.
It covers **1,445 of 6,233 files**; every throw in a file outside it, and every
`UNATTRIB` throw inside it, is reported as **UNATTRIBUTED** — not guessed, not
dropped. Population Ns are stated on every row of every table below.

Reproduce:

```bash
.venv/bin/python docs/research/scripts/post-throw-dwell-2026-08-09/throw_dwell.py \
    scan --files <frozen-file-list> -j 8 > dwell.tsv
.venv/bin/python docs/research/scripts/post-throw-dwell-2026-08-09/throw_dwell.py \
    report dwell.tsv --join corpus/join.tsv --throws corpus/throws.tsv
```

---

## VALIDATION

A number is not a result until it has been checked.

**Reconciliation against `corpus/throws.tsv` on `(file, rnd, bot)`:**

```
mine        96,185 distinct keys  (97,999 throw rows; 1,814 keys carry two throws
                                   of the same bot in the same round)
throws.tsv  96,181 distinct keys  (97,995 rows)
agree       96,181 — 100.0000% of throws.tsv, 99.9958% of mine
mine only        4
theirs only      0
```

**Every row in `throws.tsv` is reproduced.** The 4 extra keys are all in
`7526e216-…_game_5.replay26`, a file that is listed in `corpus/decoded.txt` but
contributes **zero** rows to the `throws.tsv` snapshot I froze — i.e. the keeper
folded that file in between my `throws.tsv` copy and my `decoded.txt` copy. To
rule out a parser disagreement I ran the **reference decoder**
`tools/corpus/replay_throws.py` directly on that file: it emits exactly those
same 4 throws (r47 bot 9 INSERT, r130/r135/r142 bots 281/286 EXILE). So the gap
is a snapshot seam of my own making, not a decode difference. **Effective
agreement: 96,185/96,185.**

**The 35-duplicate-basename trap (new, worth recording).** My first pass keyed
the frozen list by basename and reconciled at only **99.65%** — 337 throws in
`throws.tsv` that I could not see, concentrated in 23 files with names like
`archipelago_s1_a_ad.replay26`. Cause: `replay_archive/` holds **two different
games under the same basename**, in `diag_ad_flips_2026-08-08/` and
`diag_ad_kladde_2026-08-08/`. `corpus/decoded.txt` records 6,193 *basenames* while
the corpus decoder actually reads 6,233 *paths*. Any decoder that builds its file
list as `{basename: path}` silently drops one game of each pair. The script's
`--files` argument therefore takes explicit paths, and the frozen list expands
each decoded basename to **all** of its paths.

**`dwell ≤ life` sanity check.** `throws.tsv.life` (rounds the bot stayed alive
after the throw) is only populated for `INSERT` rows. Over the 24,085 INSERT rows
present in both tables: **24,085 / 24,085 satisfy `dwell ≤ life`, 0 violations.**

**Zero-check.** No cell in the headline distributions is an exact zero, and the
two groups that are small (`died` n=492, `end` n=497) are small because they are
genuinely rare exits, not because a branch never fires — both are populated across
all four thrower/victim splits.

---

## Dwell distribution — UNCENSORED (bot left the tile alive)

Percent of that population, by rounds spent on the landing tile.

| population | N | 0 | 1 | 2 | 3 | 4 | 5 | 6-10 | 11+ | median | mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all | 97,010 | 32.5% | 59.4% | 5.4% | 1.0% | 0.3% | 0.2% | 0.4% | 0.8% | 1 | 1.14 |
| thrower **US** | 12,576 | 44.3% | 52.6% | 1.6% | 0.2% | 0.2% | 0.1% | 0.4% | 0.6% | 1 | 0.78 |
| thrower **THEM** | 19,735 | 41.0% | 54.1% | 3.5% | 0.7% | 0.1% | 0.2% | 0.2% | 0.2% | 1 | 0.73 |
| thrower **UNATTRIB** | 64,699 | 27.6% | 62.3% | 6.7% | 1.3% | 0.4% | 0.2% | 0.5% | 1.0% | 1 | 1.34 |
| victim = thrower's **own** bot | 32,338 | 21.8% | 60.5% | 12.3% | 2.1% | 0.5% | 0.3% | 0.8% | 1.8% | 1 | 1.85 |
| victim = **enemy** bot | 63,699 | 37.7% | 58.9% | 2.0% | 0.5% | 0.3% | 0.1% | 0.3% | 0.3% | 1 | 0.78 |
| victim unattrib | 973 | 49.2% | 49.1% | 0.5% | 0.2% | 0.2% | 0.1% | 0.2% | 0.4% | 1 | 1.21 |
| **US throws own bot** | 547 | 8.2% | 73.1% | 9.0% | 0.9% | 0.9% | 0.4% | 0.9% | 6.6% | 1 | 3.22 |
| **US throws enemy bot** | 12,029 | 46.0% | 51.6% | 1.2% | 0.2% | 0.1% | 0.1% | 0.4% | 0.3% | 1 | 0.67 |
| **THEM throws own bot** | 3,311 | 26.2% | 60.6% | 8.8% | 2.7% | 0.3% | 0.6% | 0.3% | 0.5% | 1 | 1.07 |
| **THEM throws enemy bot** | 16,424 | 43.9% | 52.8% | 2.5% | 0.3% | 0.1% | 0.1% | 0.2% | 0.1% | 1 | 0.66 |

## Dwell distribution — ALL THROWS (censored counted at their censoring time)

For `died` the value is the *exact* time on the tile (the bot never left). For
`end` it is a lower bound only in the counterfactual sense that the game stopped.

| population | N | 0 | 1 | 2 | 3 | 4 | 5 | 6-10 | 11+ | median | mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all throws | 97,999 | 32.4% | 58.8% | 5.4% | 1.0% | 0.4% | 0.2% | 0.5% | 1.2% | 1 | 1.97 |
| thrower US | 12,653 | 44.2% | 52.3% | 1.5% | 0.3% | 0.2% | 0.2% | 0.5% | 0.9% | 1 | 1.49 |
| thrower THEM | 19,969 | 40.8% | 53.6% | 3.7% | 0.7% | 0.3% | 0.2% | 0.3% | 0.4% | 1 | 1.43 |
| thrower UNATTRIB | 65,377 | 27.6% | 61.7% | 6.7% | 1.3% | 0.5% | 0.2% | 0.6% | 1.5% | 1 | 2.22 |
| US throws own bot | 589 | 8.0% | 67.9% | 8.5% | 1.7% | 1.2% | 1.4% | 2.2% | 9.2% | 1 | 6.99 |
| **US throws enemy bot** | 12,064 | 46.0% | 51.5% | 1.2% | 0.2% | 0.1% | 0.1% | 0.4% | 0.5% | 1 | 1.22 |
| THEM throws own bot | 3,500 | 25.8% | 57.9% | 9.6% | 2.7% | 1.3% | 0.8% | 0.6% | 1.2% | 1 | 2.53 |
| THEM throws enemy bot | 16,469 | 43.9% | 52.7% | 2.5% | 0.3% | 0.1% | 0.1% | 0.2% | 0.2% | 1 | 1.19 |

## Ray-exposure survival — the table the plank should be priced off

`P(bot is still on the landing tile at least k rounds after the throw)`, all
throws, censored ones included at their true on-tile time.

| k rounds | all **enemy-victim** throws (N=63,966) | **US throws enemy bot** (N=12,064) | all **own-bot** throws (N=33,054) |
| ---: | ---: | ---: | ---: |
| 1 | 62.27% | 54.04% | 78.39% |
| 2 | 3.57% | 2.54% | 19.07% |
| 3 | 1.62% | 1.33% | 6.84% |
| 4 | 1.13% | 1.14% | 4.69% |
| 5 | 0.87% | 0.99% | 4.02% |
| 6 | 0.72% | 0.88% | 3.64% |
| **7** (sentinel kill) | **0.61%** | **0.75%** | 3.30% |
| 8 | 0.55% | 0.70% | 3.04% |
| 9 | 0.50% | 0.58% | 2.89% |
| 10 | 0.45% | 0.52% | 2.78% |
| **11** (gunner kill) | **0.42%** | **0.46%** | 2.67% |

The cliff is between k=1 and k=2: **96.4% of enemy-victim throws are off the tile
by the second round.** Nothing about turret DPS matters after that.

## Censored group 1 — DIED on the landing tile (the kill outcome)

**N = 492 of 97,999 throws (0.50%).**

| population | N | 0 | 1 | 2 | 3 | 4 | 5 | 6-10 | 11+ | median | mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all | 492 | 20.1% | 6.7% | 12.8% | 4.3% | 13.4% | 8.7% | 13.8% | 20.1% | 4 | 19.50 |
| thrower US | 36 | 11.1% | 0.0% | 2.8% | 13.9% | 5.6% | 16.7% | 25.0% | 25.0% | 6 | 16.72 |
| thrower THEM | 188 | 21.8% | 12.2% | 23.9% | 3.7% | 19.1% | 4.3% | 6.9% | 8.0% | 2 | 9.55 |
| thrower UNATTRIB | 268 | 20.1% | 3.7% | 6.3% | 3.4% | 10.4% | 10.8% | 17.2% | 28.0% | 5 | 26.85 |
| victim own bot | 421 | 12.1% | 6.9% | 14.7% | 5.0% | 15.2% | 8.6% | 15.2% | 22.3% | 4 | 22.33 |
| **victim enemy bot** | **69** | **69.6%** | 5.8% | 1.4% | 0.0% | 2.9% | 8.7% | 4.3% | 7.2% | 0 | 2.64 |
| US throws own bot | 32 | 6.2% | 0.0% | 3.1% | 15.6% | 6.2% | 18.8% | 25.0% | 25.0% | 6 | 17.56 |
| **US throws enemy bot** | **4** | 50.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 25.0% | 25.0% | 9 | 10.00 |
| THEM throws own bot | 179 | 19.6% | 12.8% | 25.1% | 3.9% | 20.1% | 3.4% | 6.7% | 8.4% | 2 | 9.94 |
| THEM throws enemy bot | 9 | 66.7% | 0.0% | 0.0% | 0.0% | 0.0% | 22.2% | 11.1% | 0.0% | 0 | 1.89 |

Death-on-landing-tile **rate** per population:

| population | throws | died on T | rate |
| --- | ---: | ---: | ---: |
| all | 97,999 | 492 | 0.50% |
| thrower US | 12,653 | 36 | 0.28% |
| thrower THEM | 19,969 | 188 | 0.94% |
| thrower UNATTRIB | 65,377 | 268 | 0.41% |
| US throws **own** bot | 589 | 32 | **5.43%** |
| US throws **enemy** bot | 12,064 | 4 | **0.03%** |
| THEM throws **own** bot | 3,500 | 179 | **5.11%** |
| THEM throws **enemy** bot | 16,469 | 9 | **0.05%** |

Read this carefully, because it is the sharpest thing in the document. **A bot
dying where it lands is ~100x more likely when it is the thrower's OWN bot
(5.1-5.4%) than when it is the enemy's (0.03-0.05%).** That is not a property of
turret coverage — it is the raider dying at the end of an insertion. The
enemy-victim death-on-tile rate, which is the plank's actual target metric, is
**4 events in 12,064 across the entire archive** for our own throws. And when an
enemy victim *does* die on its landing tile, 69.6% of the time it dies at
`dwell = 0` — the same round it lands — which is not a turret grinding it down
over 11 rounds; it is a bot that was already nearly dead, or one destroyed by
adjacent builder attacks.

## Censored group 2 — GAME ENDED with the bot still on the tile

**N = 497 of 97,999 throws (0.51%).** 58.6% of these sat for 11+ rounds, median
31 — unsurprising, since these are overwhelmingly late-game bots that stopped
being driven at all (bot destroyed by an uncaught exception, or a stalled
opponent). They are excluded from the uncensored table and reported here so they
cannot inflate the dwell tail.

| population | N | 0 | 1 | 2 | 3 | 4 | 5 | 6-10 | 11+ | median | mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all | 497 | 31.4% | 3.8% | 1.4% | 0.6% | 0.6% | 0.4% | 3.2% | 58.6% | 31 | 145.32 |
| thrower US | 41 | 34.1% | 4.9% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 61.0% | 56 | 204.73 |
| thrower THEM | 46 | 37.0% | 2.2% | 0.0% | 0.0% | 2.2% | 0.0% | 0.0% | 58.7% | 81 | 266.26 |
| thrower UNATTRIB | 410 | 30.5% | 3.9% | 1.7% | 0.7% | 0.5% | 0.5% | 3.9% | 58.3% | 28 | 125.81 |
| victim own bot | 295 | 18.0% | 3.4% | 1.4% | 1.0% | 0.3% | 0.7% | 4.4% | 70.8% | 54 | 160.13 |
| victim enemy bot | 198 | 51.5% | 4.5% | 1.5% | 0.0% | 1.0% | 0.0% | 1.5% | 39.9% | 0 | 121.70 |

## Censored group 3 — RETHROW

**N = 5,450 (5.56%).** The bot left `T` but by someone's launcher rather than its
own legs. Included in the uncensored table (it did leave the tile); broken out
here because for the plank it is not the same event — a rethrow can put the victim
*back* onto a ray. Enemy-victim rethrows are 1,166; own-bot rethrows are 4,284,
i.e. **most rethrow chains are a team bucket-brigading its own raider forward**,
not a duel over one bot.

---

## Does landing impose a move cooldown? — INFERENCE, and it is a strong one

**Inference: no. Landing does not set or extend the victim's move cooldown. The
victim can step off at its very next unit turn, including the same round it was
thrown.**

Evidence, in order of strength:

1. **`dwell = 0` happens 32.4% of the time (31,757 of 97,999 throws), and 29,884
   of those exit by `step`, not by rethrow or death.** A `step` exit means the
   next `moveBuilderBot` for that bot was ≤ 1 tile — an ordinary self-move — and
   it occurred *in the same turn buffer as the throw*. If landing set even a
   1-round move cooldown, `dwell = 0` would be structurally impossible. It is a
   third of the corpus. **This alone settles it.**
2. **Hand-verified on the raw event stream**, three independent cases, to rule out
   a two-part throw emission (jump + adjust) masquerading as a same-round step:
   - `01a5778f-…_game_1.replay26`, bot 311: moves to (6,8) at r156 → thrown to
     (8,12) at r157 → steps to (8,11) **later in r157** → (8,10) at r158.
   - `01a5778f-…_game_2.replay26`, bot 367: (6,18) at r236 → thrown to (8,13) at
     r237 → (8,14) **in r237** → (8,15) at r238.
   - `00523979-…_game_5.replay26`, bot 17: thrown to (10,13) at r7 → (9,13) **in
     r7** → (9,12) at r8.
   In each case the victim keeps a **1 move per round cadence straight through the
   throw**. The throw did not consume the victim's move, did not delay it, and did
   not cost it a turn.
3. **The 0/1 split is explained by unit turn order, not by cooldown.** 32.4% at
   `dwell = 0` plus 58.8% at `dwell = 1` = **91.2% of all throws leave at the
   earliest opportunity the engine allows** — same round if the victim's `run()`
   comes after the launcher's, next round otherwise. That is exactly the shape a
   *no-penalty* rule predicts and nothing else predicts as cleanly.

**Strength: strong.** n = 97,999 throws over 6,233 games and 3 hand-verified raw
traces; the falsifying observation (`dwell = 0`) is not merely present but modal-
adjacent. **What it does NOT establish:** whether the *thrower* pays anything, and
whether an **action** cooldown (as opposed to move) is imposed on the victim —
this pass measures movement only, and a bot that is action-locked but move-free
would look identical here. If the plank ever depends on the victim being unable to
*build or attack* on landing, that is a separate measurement.

---

## Sub-question: are landing tiles ever non-empty? — YES, and the earlier count undercounts

Answered in the same pass at no extra cost, because occupancy was already being
maintained for entity tracking.

**33.48% of all throws (32,812 of 97,999) land the bot on a tile that already
holds another entity.**

| co-occupant of the landing tile | throws | share |
| --- | ---: | ---: |
| *(none — tile empty)* | 65,187 | 66.52% |
| conveyor, same team as the victim | 27,826 | 28.39% |
| conveyor, opposing team to the victim | 4,985 | 5.09% |
| splitter, opposing team | 1 | 0.001% |
| anything else (turret, harvester, barrier, core, another bot) | **0** | **0%** |

So the throw-target legality rule is **`is_tile_passable`, not `is_tile_empty`** —
and a builder bot may stand on a conveyor or splitter of *either* team, but never
on a turret, harvester, barrier, core, or another bot. The exact-zero for "another
bot" is expected here rather than suspicious: it is the one exclusion the engine
must enforce for two bots to have distinct tiles at all, and the non-zero conveyor
rows prove the occupancy bookkeeping is live rather than dead.

**Consequence for the earlier research note:** a gunner-covered-landing-tile count
that only counted **empty** tiles undercounts the eligible target set by roughly
**half as many again** — conveyor and splitter tiles are legal landing spots and
they are 33.5% of what actually gets used in practice. Conveyor tiles are also
exactly where an economy sits, so a ray aimed along a conveyor run covers more
throwable tiles than an empty-tile census suggests. That raises the *hit surface*
of the plank; it does not change the dwell arithmetic above.

---

## NON-COVERAGE / LIMITS

1. **Trap 3 undercount, unfixed and unfixable from this data.** A throw that lands
   the bot exactly one tile from where it stood is byte-identical to an ordinary
   step and is invisible to every decoder in this repo, including this one. All
   counts here are of throws of ≥ 2 tiles. There is no reason to expect the dwell
   *distribution* of 1-tile throws to differ, but it is an assumption, not a
   measurement.
2. **`join.tsv` covers 1,445 of 6,233 files.** 65,377 of 97,999 throws (66.7%) are
   `UNATTRIB` — either the file is not one of our ladder games, or launchers of
   both teams were within d² ≤ 2 of the pre-throw tile so the thrower could not be
   named. These are reported as their own population and never folded into US or
   THEM. The US and THEM populations are 12,653 and 19,969 throws respectively;
   both are large, but they are **our ladder games only**, so "THEM" means "the
   opponents we have played", not "the field".
3. **The archive is not a random sample of the field** (corpus-howto trap 4). It
   is dominated by our own games. Per-opponent behaviour is not broken out here.
4. **`US throws own bot` is only 589 throws** and `US throws enemy bot` death-on-
   tile is **4 events**. Any statement about *our* kill rate from throws rests on
   single-digit counts; the enemy-victim dwell distribution (12,064 throws) is the
   solid one.
5. **Move cooldown only.** Action cooldown on landing is not measured (see the
   inference section).
6. **`end`-censored dwells are true on-tile times within the recorded game**, but
   the game stopping is not the bot choosing to stay. They are 0.51% of throws and
   are excluded from the uncensored table.
7. **Ray coverage is not measured here at all.** This document answers "how long
   is the victim there"; it does not answer "can a gunner we own actually see that
   tile". The two must be multiplied before the plank is priced.
8. **Turn-order within a round is inferred, not read.** The `dwell = 0` group
   proves the victim sometimes acts after the launcher in the same round; this
   pass does not establish the ordering rule (presumably entity id), so the
   expected number of turret shots landing on a `dwell = 0` victim is somewhere in
   [0, 1] and is not pinned down.

---

---

# FOLLOW-UP PASS — 2026-08-09T14:29Z: is `dwell = 0` CONTROLLABLE?

**Second pass, same session, same frozen file list (6,233 paths, corpus sha
`7418e13`), so every number below is commensurable with the tables above.** The
decoder gained one column, `tid` = the thrower launcher's entity id, recorded
**only when exactly one launcher was in range** (`amb == "one"`); with two
candidate launchers the id would be a guess and a guessed id makes this test
worthless. Everything else is unchanged.

## The answer

**Yes. It separates, and it separates hard: turn order is entity-id ascending,
and `dwell = 0` is not a coin — it is `launcher_id < victim_id`.**

| all attributed throws (unique launcher), N = 95,900 | N | `dwell = 0` | rate |
| --- | ---: | ---: | ---: |
| `launcher_id < victim_id` (launcher acts first) | 35,345 | 29,740 | **84.14%** |
| `launcher_id > victim_id` (victim already acted) | 60,555 | 1,106 | **1.83%** |

And the 1.83% is almost entirely **not** the victim escaping. Of those 1,106
same-round exits, **933 were a rethrow by a second launcher, 149 were the game
ending, 20 were the bot dying, and only 4 were the victim stepping off under its
own power** — 4 in 60,555, **0.0066%**.

**For our own throws it is exactly zero.** US, `launcher_id > victim_id`,
N = 6,685: 22 `dwell = 0` events, of which `end` 14, `rethrow` 7, `died` 1,
**`step` 0**. Across the entire archive, a builder bot has never once been seen to
step off its landing tile in the same round when our launcher's id was the higher
one.

## Cross-tab by population

| population | N | 0 | 1 | 2 | 3 | 4 | 5 | 6-10 | 11+ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| US throws **enemy** bot, `L < V` | 5,886 | 93.8% | 4.4% | 0.5% | 0.2% | 0.1% | 0.1% | 0.4% | 0.5% |
| **US throws enemy bot, `L > V`** | **6,177** | **0.4%** | **96.4%** | 1.8% | 0.2% | 0.2% | 0.1% | 0.4% | 0.5% |
| US throws own bot, `L < V` | 80 | 58.8% | 3.8% | 1.2% | 5.0% | 3.8% | 6.2% | 6.2% | 15.0% |
| US throws own bot, `L > V` | 508 | 0.0% | 78.0% | 9.6% | 1.2% | 0.8% | 0.6% | 1.6% | 8.3% |
| THEM throws enemy bot, `L < V` | 7,338 | 92.1% | 5.7% | 1.4% | 0.3% | 0.1% | 0.1% | 0.2% | 0.1% |
| THEM throws enemy bot, `L > V` | 8,670 | 2.2% | 93.4% | 3.4% | 0.3% | 0.1% | 0.1% | 0.1% | 0.3% |
| THEM throws own bot, `L < V` | 2,081 | 39.0% | 49.3% | 6.3% | 1.9% | 1.9% | 0.3% | 0.4% | 0.9% |
| THEM throws own bot, `L > V` | 1,159 | 0.9% | 71.4% | 17.3% | 4.7% | 0.6% | 1.7% | 1.1% | 2.2% |

**US throws enemy bot with `launcher_id > victim_id`, N = 6,177:**
`P(on tile ≥ 1 round) = 99.64%`, `≥ 2 = 3.24%`, `≥ 3 = 1.39%`, `≥ 7 = 0.71%`,
`≥ 11 = 0.47%`.

**So the plank's yield becomes exactly one round of ray exposure, reliably** —
one gunner shot (7 HP) or one sentinel shot (18 HP), at 99.6%, instead of the
54/46 coin in the headline tables. It does **not** become a kill: the `≥ 7` and
`≥ 11` tails are unchanged (0.71% / 0.47%), because whether the victim *keeps*
moving after round 1 has nothing to do with turn order.

## Does the own/enemy asymmetry vanish under conditioning? — PARTLY. Say so.

The prediction was that the raw 8.0% (US throws own bot) vs 46.0% (US throws
enemy bot) `dwell = 0` gap should disappear once conditioned on id order.

| | US throws own bot | US throws enemy bot |
| --- | ---: | ---: |
| raw `dwell = 0` rate | 8.0% | 46.0% |
| **exposure**: share with `L < V` | **13.61%** (N=588) | **48.79%** (N=12,063) |
| `dwell = 0` given `L > V` | **0.0%** | **0.4%** |
| `dwell = 0` given `L < V` | **58.8%** | **93.8%** |

- **On the `L > V` side the asymmetry vanishes completely** (0.0% vs 0.4%) — as
  predicted, and that is the confirming half.
- **Most of the raw gap is exposure**, not behaviour: own-bot throws land on the
  `L < V` side only 13.6% of the time against 48.8% for enemy-bot throws. That is
  itself an id fact — a team's own launcher is usually built *after* the raider
  bots it ferries, so `L > V` by construction.
- **A residual survives on the `L < V` side: 58.8% vs 93.8%, and the id hypothesis
  does not explain it.** The honest reading is that id order governs whether the
  victim *gets a turn* after the throw, not what it does with it. An enemy victim
  handed a turn walks off 93.8% of the time; a bot thrown by its **own** team was
  put where it wanted to be, and 41% of the time it spends that turn on something
  else — plausibly building or attacking, which are mutually exclusive with moving.
  **That is a behavioural explanation, offered as a hypothesis and not tested
  here.** The id rule is complete for "can it move"; it is silent on "will it".

## Sign distribution — is this already free, or is it a change?

Attributed throws with a unique launcher:

| | `launcher_id < victim_id` (bad: victim escapes same round) | `launcher_id > victim_id` (good: one guaranteed round) |
| --- | ---: | ---: |
| **US, all throws** (N=12,651) | 47.16% | 52.84% |
| **US, enemy victims** (N=12,063) | **48.79%** | **51.21%** |
| US, own-bot throws (N=588) | 13.61% | 86.39% |
| THEM, all throws (N=19,248) | 48.93% | 51.07% |
| THEM, enemy victims (N=16,008) | 45.84% | 54.16% |

**This is a change, not something we already get for free.** Just under half
(48.79%) of the enemy bots we currently throw are on the losing side of the id
comparison, and every one of those escapes the same round with ~94% probability.
Filtering targets to `victim_id < ct.get_id()` converts that half from ~0 shots
to 1 shot — **roughly a 2× improvement on the plank's only remaining value**, at
the cost of declining about half the throws.

Both ids are readable at runtime: `ct.get_id()` for the launcher, and the victim's
id comes straight out of `get_nearby_units()` / `get_tile_builder_bot_id(pos)`.
The rule is a single integer comparison, not a model.

## Corollary — ids are a global creation-order counter, so this is a build-timing lever

Verified directly, not assumed: over the **first 300 files of the frozen list**,
taking every pair of consecutively-created entities that were created in
*different* rounds, **26,078 pairs, 0 with a non-increasing id (0.0000%)**; of
those, **8,802 were cross-team pairs, also 0 inversions.** Entity ids come from a
**single global counter shared by both teams**, assigned in creation order.

Therefore `victim_id < launcher_id` means exactly **"this enemy bot existed before
we built this launcher"**, and it follows that:

- A kidnap launcher built **late** has a high id and so is favourably ordered
  against every enemy bot already on the map.
- A launcher built **early** is unfavourably ordered against every enemy bot
  spawned afterwards — and the enemy spawns bots continuously, so an early
  launcher's favourable pool only shrinks.

That corollary follows from the counter behaviour plus the turn-order law; it is
**not separately measured against build round**, and should be treated as a
prediction to check rather than a result.

## Validation of this pass

- **Row-for-row identical to the first pass.** Adding the `tid` column changed
  nothing else: 97,999 throw rows, 96,185 distinct `(file, rnd, bot)` keys,
  **100.0000% of `corpus/throws.tsv`'s 96,181 keys reproduced**, same 4 known
  extras, `dwell ≤ life` 24,085/24,085.
- **N stated everywhere; the excluded set is stated too.** 2,099 of 97,999 throws
  (2.14%) have no unique launcher id and are dropped from this section only:
  1,120 `same_team` (two friendly launchers in range) and 979 `both_teams`. They
  are not guessed at.
- **The finding is not an artefact of the exclusion**: the `both_teams` rows were
  already `UNATTRIB` in the headline tables, and the `same_team` rows are 1.1% of
  the corpus.
- **No exact zero was accepted without a cause.** The 0.0% cell (US throws own
  bot, `L > V`, `dwell = 0`, N=508) and the `step`-count of 0 in the US `L > V`
  exception set are both *predicted* by the id law rather than surprising, and the
  neighbouring populations are non-zero (4 self-steps do exist across all
  attributed `L > V` throws), so the branch demonstrably fires.

## Limits specific to this pass

1. **`amb == "one"` only.** The id test needs an unambiguous thrower; 2.14% of
   throws are excluded.
2. **Within-round ordering among entities created in the same round is untested** —
   the corollary check deliberately skipped same-round pairs. It does not affect
   the turn-order law, which is tested on the ids themselves.
3. **The `L < V` residual (58.8% vs 93.8%) is unexplained by ids.** A behavioural
   hypothesis is offered; it is not measured. Do not price anything off it.
4. **The 1-round yield does not become a kill.** `P(≥ 7)` and `P(≥ 11)` are
   unchanged by conditioning. Everything in the first pass's LIMITS section still
   applies, in particular the trap-3 one-tile-throw undercount and the `join.tsv`
   coverage limit.

---

## Files

- Decoder: `docs/research/scripts/post-throw-dwell-2026-08-09/throw_dwell.py`
- Inputs (frozen): 6,233 `replay_archive/**/*.replay26` paths, `corpus/join.tsv`
  (1,445 rows), `corpus/throws.tsv` (97,995 rows), `corpus/decoded.txt`
  (6,193 basenames), corpus git sha `7418e13`.
- Intermediate table: 97,999 rows, one per throw, columns
  `file rounds rnd bot bteam tteam tid amb rel lx ly occ occ_what dwell exit
  d2_before d2_after`. Regenerable in 31 seconds by the command in Method.
  (`tid` = thrower launcher entity id, `-1` unless exactly one launcher was in
  range; added by the 14:29Z follow-up pass, which re-ran the same frozen list and
  reproduced the first pass row-for-row.)
