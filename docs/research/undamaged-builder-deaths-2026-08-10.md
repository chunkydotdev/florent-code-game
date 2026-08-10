# Are our builder bots leaving the game undamaged? — the exception-kill census

**Research arm, session 28, decoded 2026-08-10. Read-only cut. No bot, arena, prereg or
coordination file touched.**

---

## 0. The answer in six lines

**ZERO. 0 of 539 builder-bot removals on our side across 235 v102 ladder games — 0.00 per
game — left the game with positive HP.** Not one. No exclusion filter was even needed: the
count is zero before *and* after dropping final-round removals.

**The control fires, hard.** The identical classifier on 4,870 third-party ladder games
finds **2,636 undamaged mid-game builder removals out of 25,466 (10.35%)**, in **610 of
4,870 games (12.53%)**. **The instrument can see the category.**

**And the instrument was shown to fire on OUR rows specifically**: with negative HP deltas
stripped from our own tapes, our count goes 0 → **539 / 539 (100%)**. The zero is a
property of the data, not of the classifier's reach.

**The pre-stated expectation was zero and zero is what came back.** But the reason is not
the one the brief hoped for, and §6 says so plainly: **we are at zero because `run()` wraps
everything in a blanket `try/except Exception`, not because our paths are vision-safe.**
That distinction changes what the null licenses.

---

## 1. THE TABLE

**Subject: builder-bot removals. Unit: one removal. Fixture: LADDER, no downloads.**

| arm | population | games | builder removals | **undamaged, mid-game** | rate | per game |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| **US** | our v102 side | **235** | **539** | **0** | **0.00%** | **0.00** |
| OPP | opponents, *same 235 games* | 235 | 396 | 3 | 0.76% | 0.013 |
| **FIELD control** | third-party ladder, both sides | **4,870** | **25,466** | **2,636** | **10.35%** | **0.541** |

**Denominators.** Our arm also rests on **1,677 builder spawns** in those 235 games (32.1%
of our builders die at all). The three OPP events all sit in **one match**
(`36b09df5-d7b2-…`, opponent version 8), two games, rounds 275/278/304 — so the same-games
control is a 1-opponent, 1-match phenomenon and is *not* the load-bearing control. §3 is.

**Concentration tails, control arm (n = 2,636):**

| basis | top-1 | top-3 | top-5 | distinct |
| --- | ---: | ---: | ---: | ---: |
| per game | 0.6% | 1.6% | 2.6% | 610 |
| **per team** | **57.5%** | **81.5%** | **94.7%** | **13** |

**Read the per-team tail before anything else.** The category is flat across games and
extremely concentrated in *teams*. It is a bot-design property, not an event.

**Round shape, control arm:** median round **57** (q1 21, q3 169, min 1, max 985); median
unit lifetime at removal **46 rounds**. So had ours been nonzero, the expected shape is an
early-to-mid cluster, not an end-of-game artefact.

### Our zero in the field's terms

| | teams |
| --- | ---: |
| field teams with ≥200 builder removals | **43** |
| …of which sit at **exactly zero** undamaged removals | **33 (77%)** |
| …of which carry the category | 10 |

Top carriers: `vjg` **96.13%** (1,517/1,578), `S` 89.06% (293/329), `Ship Happens` 87.40%
(229/262), `Troupe` 84.92% (338/398), `Cookie` 50.21% (119/237), `Ouroboros` 17.91%,
`not adgato` 5.60%, `LingLing40` 1.32%, `I Stone` 0.62%, `farming_200s` 0.23%.

**Our 0 is the modal team outcome, not a distinction.** Saying "we are clean" is true and
says less than it sounds like: three quarters of the measurable field is also at zero.

### Power

Rule of three on 0/539: **95% upper bound = 0.56% of removals** (per game: 0/235 → **1.28%
of games**, against the field's 12.53%).

| if our true rate were… | P(observing 0 in 539) |
| --- | ---: |
| the pooled field 10.35% | ≈ e^−59 |
| 1% | 0.0044 |
| 0.5% | 0.067 |

**A rate at or above 1% is excluded at p < 0.005. A rate below 0.5% is NOT excluded.** In
per-game terms the strongest honest statement is: fewer than one silent builder loss per
178 games.

---

## 2. What the classifier actually is

Per builder bot, from the raw `.replay26` update stream (no corpus table used — `events.tsv`
carries no HP):

```
  hp_at_removal = spawn_hp + Σ(every UpdateHp delta for that id, whole game, r ≤ removal)
  UNDAMAGED-ALIVE removal  :=  hp_at_removal > 0  AND  removal round < last round
```

Two decisions carry it:

- **The ledger is summed over the WHOLE game, not the removal round.** That is what
  neutralises the `FireTurret`-emitted-after-`removeEntity` ordering trap
  (`tools/replay_schema.md`, S1): a lethal delta emitted out of order is still counted.
- **`UpdateHp.delta` is a two's-complement 64-bit varint**, sign-extended for negatives —
  decoded via `sint()`, not read as an unsigned int.

Guards applied: **rotation re-emits suppressed** (a build is the FIRST `placeEntity`
carrying an id — TRAP 3); **entity ids treated as orderless** (shared counter with resource
stacks); **`ladder_games.tsv:seat` and `econ.tsv:deliveries` never touched** (TRAPs 7, 8).

**Seat, independently verified behaviourally.** Seat and version come from
`replay_archive/*.meta.json` (`teamAId`/`teamAVersion`), never from `winnerSide`. The
independent check: **`builderAttack` = 0 on our side across all 235 games (0 games with
any), against 13,164 on the opponents'.** LOKI-8's silenced melee identifies our seat from
the bot's own fingerprint.

**Population, frozen before any headline was computed.** `pop_v102.tsv`, sha256
`178a5ddc67335730` — 235 games / 47 matches, `triggeredBy == ladder`, our team version 102,
`opensverige - plan B` excluded from both arms. Seat split 100 A / 135 B. Median game 156
rounds (min 59, max 456). Control population `pop_field.tsv`, sha256 `27f6584e0c2a2cb5` —
4,870 games / 974 matches / 70 distinct teams, neither side us, neither side plan B.

**Decode completeness: 235/235 and 4,870/4,870 files, zero errors.** An incomplete run
would have had no number.

---

## 3. Proving the control fires — three independent ways, because one was not enough

### 3.1 Synthetic ground truth: I built the bug and measured it

Two local matches, same map (`hive`), same opponent, differing in **one line** of the
builder branch:

| arm | builder does at r30 | builders | removals | **detected undamaged** |
| --- | --- | ---: | ---: | ---: |
| `bot_crash` | `ct.get_tile_env(<tile outside vision>)`, **uncaught** | 96 | 96 | **96 / 96 (100%)** |
| `bot_suicide` | `ct.self_destruct()` | 96 | 96 | **96 / 96 (100%)** |
| `bot_idle` | `return` | 3 | **0** | **0** |

Every detected removal reads `hp_at_removal = 40`, `ever_neg = False`. **The positive
control fires at 100% and the negative control is clean at 0.** This also confirms the
premise the whole question rests on: **an out-of-vision `get_tile_env()` raises, escapes,
and the engine removes the unit** — observed, not assumed.

### 3.2 The field arm, at scale

**2,636 undamaged mid-game removals in 4,870 real third-party games**, spread over 610
games and 13 teams (§1). A classifier returning 2,636 on real tapes is not a dead column.

### 3.3 Corruption arms — the alarm flips in both directions

| arm | US | OPP |
| --- | ---: | ---: |
| **clean** | **0 / 539 (0.00%)** | 3 / 396 (0.76%) |
| `inject` — add a lethal delta before every undamaged removal | 0 / 539 | **3 → 0** |
| `strip_hp` — drop every negative delta | **0 → 539 / 539 (100%)** | 396 / 396 (100%) |

**`strip_hp` is the load-bearing one and it is aimed precisely at the constant-column
trap.** It proves the classifier is not structurally incapable of emitting on *our* rows:
feed our own 539 removals an undamaged signal and all 539 fire. `inject` proves the
converse — corrupt the input toward "damaged" and the three real OPP alarms go silent.

### 3.4 An independent decoder reproduces the denominator

`tools/field_deaths.py` — written for a different question, sharing only the low-level
`fields()`/`parse_entity()` primitives — run over the identical 235-game list returns
**US deaths = 539, spawns = 1,677**. My decoder: **539**. Exact.

---

## 4. GUARD 4, AND IT IS THE MOST IMPORTANT PARAGRAPH IN THIS DOCUMENT

**An uncaught-exception kill and `self_destruct()` are INDISTINGUISHABLE in the replay —
not "hard to tell apart", literally byte-identical.**

```
  cmp cal_crash.replay26 cal_suicide.replay26   ->  identical, 1000/1000 turns, 0 differing
```

The two matches in §3.1 differ in exactly one source line and produce **the same file
bytes**. Per-round update histograms around the death round agree exactly
(r30: `{botOutput: 8, removeEntity: 3, updatePlayers: 1}` in both). And critically:
**the traceback does NOT reach the replay.** `BotOutput.stdout` on the death round is
`b''` and `tled = 0` in both arms. The engine prints the traceback to its own stderr; the
tape keeps nothing.

**So the honest position is: from replays alone, this question is unanswerable.** The tape
gives you the *count of undamaged removals* and cannot split it.

**It becomes answerable for US, and only for US, from a source fact:**

> The shipped v102 tree — `bots/_v124loki8`, treehash **`2dad5a2a`**, matching
> `HANDOVER.md:11` — contains **zero call sites** for `self_destruct()`, `destroy()` or
> `resign()` across all four shipped files (`main.py`, `doctrine.py`, `eco.py`, `raid.py`).
> The nine textual hits on "destroy" in `doctrine.py` are comments.

Given zero voluntary-exit call sites, any undamaged builder removal on our side would have
had to be an exception kill. There were none, so the point is moot — **but the reasoning
chain is source→tape, and a future version that adds `self_destruct()` breaks this
instrument permanently.** Note that for the FIELD arm no such source is available, so
**the 2,636 control events are "undamaged removals" and must NOT be reported as crashes.**

---

## 5. The other ways a builder can leave the game — ruled out, or named as unexcluded

**1. `destroy()` on a builder bot — RULED OUT MECHANICALLY, probed not assumed.** A local
probe crowded four friendly builders orthogonally adjacent and called `can_destroy()` on
every neighbour tile holding a friendly builder, every round from r30:
**`can_destroy = False` on every tile, every round, without exception.** `destroy()` targets
allied *buildings*; a builder bot is the one unit that is not a building. **It cannot
produce this signature for either side.**

**2. `self_destruct()` — indistinguishable in tape (§4); ruled out for US by source.**

**3. A lethal delta I mis-bucketed — RULED OUT on four checks.**
 - The ledger sums the whole game, so the ordering trap cannot hide one.
 - The delta alphabet across **14,583 field builders** is exactly
   `{−7: 21,000, +4: 6,692, −18: 3,521, +3: 1,232, +2: 381, +1: 84}` — gunner, sentinel,
   and heals (the engine emits the **clamped** heal, +1/+2/+3, not a flat +4).
 - **Reconstructed HP never exceeds `max_hp` (40) at any ledger point — 0 overflow events
   in 14,583 builders.** This is the check that matters: if heals were emitted unclamped,
   the ledger would drift high and *manufacture* false "removed while alive" rows. It does
   not drift.
 - **No delta of −2 exists anywhere**, independently reproducing the s-lane finding that a
   builder attack (2 dmg) can never touch a builder bot.

**4. CPU timeout (TLE) — RULED OUT on the real tape, not on a local probe.** In 900
third-party games, **877 builders had at least one `tled = 1` turn and 778 of them (88.7%)
were never removed at all.** Among undamaged removals only **0.74% ever TLEd** — *lower*
than among damaged removals (**2.70%**). A TLE interrupts a turn; it does not remove a
unit. **And our own side carries 0 TLE events in all 235 v102 games** (opponents: 2,809, in
15 games). *Caveat: my local `--tle 10` arm never set the flag, so the local runner did not
enforce the limit and that arm is inconclusive by itself — the real-tape figures above are
what carries this row.*

**5. Launched off the map / thrown to death — 1 event, NOT EXCLUDED.** Exactly **1 of the
2,640 raw control removals (0.04%)** fell on a round the victim was displaced by more than
one tile. I did not chase it. **0 on our side**, so it changes nothing here.

**6. End-of-round cleanup / mass removal at game end — RULED OUT.** The engine does not
sweep units when the core dies: only **4 of 2,640** raw undamaged control removals landed
in the final round. They are excluded anyway, and our count is 0 with or without the filter.

**7. Replay truncation — RULED OUT.** 5,105 files decoded, 0 errors, and the denominator
reproduces an independent decoder exactly (§3.4).

### Unexcluded, stated as such

- **Engine parity.** All calibration in §3.1/§4/§5.1 ran against the **local** `fcode`
  engine. If the platform engine differs — most consequentially, if it writes the traceback
  into `BotOutput.stdout` — then "byte-identical" is a local claim and the platform tape
  might carry a discriminator I did not look for. I found no traceback text in any archived
  `botOutput`, but I did not search exhaustively.
- **Non-builder units.** Our turrets, launchers and core are not measured here. An exception
  kill hits any unit type, and for buildings the discriminator is weaker because `destroy()`
  *is* legal on them. The nearest existing evidence is
  `repair-class-costing-2026-08-10.md` §4: 0 undamaged carrier removals on our side against
  122 on the opponents'. **A rate below 0.5% is not excluded for builders either (§1).**

---

## 6. Why the null happened, and why it does NOT license what it looks like it licenses

**`v102` catches everything.** `bots/_v124loki8/main.py:116`:

```python
def run(self, ct):
    try:
        self._dispatch(ct)
    except Exception:
        if not self.reported_error:
            self.reported_error = True
            import sys, traceback
            traceback.print_exc(file=sys.stderr)
```

`self.reported_error` is initialised at `main.py:110`, so the handler itself does not
raise on its first use.

**This is the mechanism behind the zero, and it is a different fact from "our paths are
vision-safe."** The brief's framing — *"we have a constraint the current bot happens to
respect, which is exactly what a new graph walk would violate"* — **is the part of the
brief I think is wrong.** A new graph walk placed under `_dispatch` would *also* measure
zero undamaged removals, because the same blanket handler swallows its `GameError` too.

**The real hazard the sibling cut is pointing at is not unit loss. It is TURN loss, and
turn loss is invisible in the tape.** An exception at any depth costs that unit its entire
round — every action it would have taken, silently, with no removal, no HP delta, no
`botOutput` marker, and a stderr line printed **once per unit lifetime** (`reported_error`
latches) that platform games never show us. A unit burning turns to a repeating
out-of-vision query looks, in the replay, exactly like a unit that decided to idle.

**So the correct conclusion is narrower than "vision-safe":** *no shipped path is losing us
units*, and *the tape cannot tell us whether shipped paths are losing us turns.* The
per-builder build budget the brief worries about is **safe from the unit-loss failure mode**
— no builder silently vanishes from a per-builder census — **and is not protected against
the turn-loss one**, which would depress that budget without leaving any trace this
instrument can read.

Two residual escape hatches in the guard itself, neither observed and both cheap to note:
`except Exception` does not catch `BaseException` subclasses, and an exception raised inside
the handler (the `import`/`print_exc` path) would still escape.

---

## 7. What I would measure next, and what I deliberately did not

**Next (and it is a different instrument, not an extension of this one): the turn-loss
census.** It cannot be done from the replay alone — the discriminator has to come from a
local fixture instrumented to count handler entries, or from a shipped build that writes a
crash counter into an unused comms-store slot. That is a builder decision, not a research
one, and it is the only way §6's open half gets closed.

**Not measured, on purpose (a measurement the question does not turn on imports its own
population):** per-opponent breakdown of the 3 OPP events; the field's undamaged removals
by opponent version; non-builder undamaged removals on our side; anything about win rate.

---

## Appendix — reproducing this

Scripts are session-scratch and die with the session: `decode.py` (raw `.replay26` →
per-builder HP ledger, removal, throw and `botOutput` records; ~230 lines against
`tools/replay_census.fields`/`parse_entity`), `run.py` / `run_field.py` (population drivers
and corruption arms), plus four calibration bots `bot_crash` / `bot_suicide` / `bot_idle` /
`bot_destroy`. Frozen populations `pop_v102.tsv` (`178a5ddc67335730`) and `pop_field.tsv`
(`27f6584e0c2a2cb5`).

Load-bearing decisions, in the order they would break the result:

1. **The HP ledger is summed over the whole game**, defeating the S1 ordering trap.
2. **`UpdateHp.delta` decoded as a sign-extended 64-bit varint.** Read unsigned, every
   negative delta becomes ~1.8e19 and the whole census inverts.
3. **`strip_hp` was run before the headline was written.** A zero with no proof the
   classifier can fire on that arm's own rows is the constant-column trap, and this
   document's null would have been worthless without it.
4. **Seat from `.meta.json`, confirmed behaviourally by `builderAttack` = 0 vs 13,164.**
5. **Rotation `placeEntity` re-emits suppressed** (first-id-wins), per TRAP 3.
6. **`can_destroy()` on a builder tile was probed, not inferred from the API docs.**
7. **The crash-vs-suicide indistinguishability was established by byte-comparing two
   replays**, not by reasoning about the schema.
