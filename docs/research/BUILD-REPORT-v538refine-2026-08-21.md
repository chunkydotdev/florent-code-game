# BUILD REPORT — `bots/_v538refine` (v538), s52, 2026-08-21

**ONE PLANK: THE v537 SOCKET CLAIM STANDS DOWN ON BOARDS THE FERRY-SIEGE
REFUSES.** Parent `bots/_v537socket`, md5-frozen at `04:00:33Z` and re-verified
byte-unchanged at `04:24:11Z` (`scratchpad/s52_v538_build/PARENT_FREEZE.md5`,
`PARENT_REFREEZE.md5`). The change is the exact `bots/_v535cornergate` pattern —
gate a map-invariant plank by the map verdict the siege gate already computes —
applied to a second consumer.

This build wrote to `bots/_v538refine`, `docs/research/` and
`scratchpad/s52_v538_build/` only. No `tools/*` edit. `bots/_v488beltbreak2` is
mode-444 and was read, never written. Wall clock from `date -u` in the same
shell call each time: context read `03:59:01Z`, tree copy + parent freeze
`04:00:33Z`, doctrine block `04:01:05Z`, code `04:01-04:03Z`, predicate
instruments `04:03:57-04:05:15Z`, identity battery `04:07:15-04:08:54Z`,
mechanism run 1 `04:10:04-04:17:02Z`, twin control `04:17:51-04:22:34Z`,
mechanism run 2 (arm order reversed) `04:24:42-04:31:21Z`, direct dose probe
`04:23:28Z`, midgard cell `04:32:59-04:35:01Z`, parent re-freeze `04:24:11Z`.

**1,870 local games, 0 tracebacks, across five fixtures.**

---

## ⛔ TOP LINE — SIX SENTENCES

1. **THE ARCHIPELAGO BACKFIRE IS REVERSED AND IT REPLICATES ACROSS TWO RUNS
   WITH THE ARM ORDER FLIPPED: v537socket 20/120 (16.67 %) → v538refine
   61/120 (50.83 %), +34.17 pp, paired McNemar z = −5.34, 50 discordant one way
   against 9 the other.** The stated prediction was "recovers toward v536's
   35/60"; measured against `v536trustport` in the *same interleaved cells*,
   v538 lands at **parity with it** (57/120 vs 61/120, z = −0.53). §4.
2. **THE FALSIFIER HOLDS. The socket plank's gains on siege-active boards are
   fully retained**: against `v536trustport` on the two RUNNING maps pooled,
   v538 keeps **+33.33 pp (z = −7.56)**, and against v537socket it is
   **+7.50 pp (z = −1.78), i.e. not a cost**. §4.2.
3. ⭐⭐ **THE SURPRISE, WRITTEN BEFORE IT IS EXPLAINED: THE TWO RUNNING-MAP
   CELLS MOVED IN RUN 1 ON BOARDS WHERE THE GATE PROVABLY CANNOT ACT — and the
   two runs then DISAGREED IN SIGN on glacierkeep (+20.0 pp, then −13.3 pp).**
   That forced a control this build did not plan: **two byte-identical copies of
   the parent, run as separate arms on the identical grid**, which read
   **−11.67 pp on glacierkeep and +8.33 pp on archipelago at n = 60.** §5. The
   fixture's own same-bot swing is what those cells were showing.
4. ⚠ **AND ONE RESIDUAL IS NOT EXPLAINED BY THAT: yulerune reads +11.67 pp in
   BOTH runs (z = −2.56 pooled) on a board where the two trees are proved
   row-identical under NOISE_OFF.** Arm order was reversed between the runs and
   did not move it. No explanation is offered. §5.2.
5. **FLAG-OFF IS `bots/_v537socket`, FOUR WAYS, and the dose and its SCOPE come
   out of the same table: `FS_V538_CLAIM_GATE = False` is row-identical to the
   parent on 50 of 50 NOISE_OFF cells, while the gate ON differs on
   20 of 20 REFUSING cells and 0 of 30 RUNNING cells.** §6.
6. ⚠ **NO CURRENCY CLAIM.** Every win column here is at n = 60 or n = 120 per
   cell on a 4-map, one-opponent LOCAL fixture whose own same-bot swing this
   build measured at up to ±20 pp. **The powered screen is the builder's.**

---

## 1. THE PLANK AS BUILT

Four files, `raid.py` **md5-identical** to the frozen parent. The whole
changeset is **additive except three lines of `_fs_gate`, which are an
extraction** (§2).

| file | +lines | −lines | **+ executable (non-comment, non-docstring)** | what those lines are |
|---|---|---|---|---|
| `doctrine.py` | 69 | 0 | **3** | `LOKI_FS_V538`, `FS_V538_CLAIM_GATE`, `FS_V538_LOG`. The other 66 are the doctrine block — the defect, the mechanism story, the midgard trade stated as a cost, the map-robustness reason there is no map list. House convention (v524/v530/v534/v537 blocks are the same shape). |
| `eco.py` | 48 | 0 | **13** | `_v538_claim_on` (11 statements) + the single call site (2). |
| `siege.py` | 89 | 3 | **~30** | `_fs_enemy_anchor` (**9**, an *extraction*) + `_v535_map_refuses` (**~19**) + `_fs_gate` rewired to call the extraction (−3 / +1). |
| `main.py` | 9 | 0 | **2** | `self.v535_refuse = None`, `self.v538_claim_gated = 0`. |
| `raid.py` | 0 | 0 | 0 | untouched, md5-identical |

⇒ **≈48 executable lines across three functions.** The remaining ~170 are
doctrine prose and docstrings.

| flag | value | meaning |
|---|---|---|
| `LOKI_FS_V538` | `True` | master. `False` == `bots/_v537socket` unchanged, and the siege reader is never called at all |
| `FS_V538_CLAIM_GATE` | `True` | the gate: the v537 socket claim stands down on boards the ferry-siege REFUSES |
| `FS_V538_LOG` | `False` | stderr tape for the refusal verdict; off in competition |

### 1.1 Two design decisions, each with the reason it is not the other thing

**(a) THE GATE IS ASKED INSIDE THE WINDOW, NOT AT THE main.py RUNG.**
`_v537_socket_claim` early-returns on `rnd > FS_V537_BY_ROUND` **before** calling
`_v538_claim_on`, so the verdict costs a handful of calls per body per game and
nothing at all after r4. Gating at the rung would have re-asked it every round
for 1,000 rounds. **A side effect worth having: `main.py`'s dispatch is
untouched, so the only `main.py` change in the whole build is two `__init__`
lines.**

**(b) BOTH REFUSING BOARDS ARE GATED — NO MAP LIST, ON PURPOSE, AND IT COSTS
SOMETHING.** The commission flagged that v537's screen read midgard 37/60
(a gain over v536's 36) and that gating it gives that up. The alternative is a
named-map list, which the map-robustness policy (F3) forbids and which cannot
generalise to a board we have not seen. **So the principled predicate was
shipped and the midgard cell was then MEASURED rather than accepted on faith:
+6.67 pp, z = −0.76 — no detectable cost. §4.3.**

---

## 2. THE PLUMBING — ported what, called what

**The v535 corner-gate machinery is NOT on this lineage.** v537socket descends
`_v536trustport` ← `_v529merge`; `_v535cornergate` is a separate branch off
`_v534maptrust`. Checked on the trees, not assumed: `bots/_v537socket` contains
`_fs_map_gated` and **neither** `_fs_enemy_anchor` **nor** `_v535_map_refuses`.

**PORTED (two functions, from `bots/_v535cornergate/siege.py`):**

* **`_fs_enemy_anchor`** — an **extraction**, not new logic. The eight anchor
  lines stood inline in `_fs_gate`; they now live in one function that `_fs_gate`
  and the new reader both call. **Not flag-gated, deliberately**: a flag here
  would make the two paths differ under `FS_V538_CLAIM_GATE = False`, which is
  the exact property flag-off exists to rule out.
* **`_v535_map_refuses`** — the reader. **Kept under its v535 name**: it is the
  same object doing the same job (publishing the siege's map verdict to a
  non-siege plank), and renaming per consumer is the first step back toward two
  predicates. Its consumer here is the socket claim; v535's was the corner
  barriers, which are **not** gated on this tree.

**CALLED, NEVER RE-DERIVED (D21d).** `_fs_map_gated` — the existing verified
function — is unmodified and is the single definition of "this board refuses".
What is local to the reader is **the cache and the sign flip, nothing else.**

**A PORT INHERITS THE ORIGINAL'S DESIGN, NOT ITS VERIFICATION**, so all three
v535 checks were re-run against **this** tree
(`test_called.py`, `OUT_called.txt`, **PASS**):

1. **STRUCTURAL (AST).** `_v535_map_refuses`'s body, docstring stripped (prose
   must not score), **calls** `_fs_map_gated` and `_fs_enemy_anchor` and contains
   **none** of the ten tokens a re-derivation needs (`FS_MAP_SKIP`,
   `FS_V525_MIN_MAP_DIM`, `FS_V525_MIN_CORE_DSQ`, the cripple lists,
   `known_map_for`, `distance_squared`, `read_store`, `enemy_core_for`,
   `unpack_pos`, `SLOT_ENEMY_CORE`). ⛔ **Driven the other way**: the same
   scanner on `_fs_map_gated` and `_fs_enemy_anchor` **must** find those tokens,
   or "0 leaked" would be a report about an empty function. It does. Full call
   set: `['_fs_enemy_anchor', '_fs_map_gated', 'get_current_round', 'get_id',
   'print']`.
2. **THE EXTRACTION IS BEHAVIOUR-PRESERVING.** The rewired `_fs_gate` is
   compared against the **frozen parent's** `_fs_gate` over the whole map pool ×
   both seats × **all three anchor states** the extraction spans (own
   `self.enemy` / only `SLOT_ENEMY_CORE` published / neither, the mirror
   fallback) — **204 cells, 0 mismatches, and the comparison saw BOTH
   verdicts.** ⛔ Driven the other way by a stub anchor returning a bogus core on
   **nordkap** — a board asserted to RUN first, because a mutant sited on a board
   that already gives the target verdict demonstrates nothing.
3. **THE READER AGREES WITH THE ORIGINAL.** `_v535_map_refuses(ct) ==
   not _fs_gate(ct)` on all 68 pool cells, **with both verdicts occurring.**

And on the ENGINE: §6's NOISE_OFF grid has `masteroff_off` (`LOKI_FS_V538 =
False`, so `_fs_gate` runs through the extraction while the gate is dead)
row-identical to the un-refactored parent on **50 of 50 cells**.

---

## 3. WHERE THE GATE BINDS — BOTH VERDICTS, WHOLE POOL

`gatemap.py` drives the **shipped** predicate end-to-end on a real `Player` for
every `maps/*.map26` from **both seats** — 68 cells
(`OUT_gatemap.txt`; `--selftest` PASS at `04:03:57Z`, 8 mutants incl. the two
geometric floors, a grid-confirmed skip, a signature-with-wrong-grid, both flag
mutants, and a cache-cost check).

```
CELLS 68 | refuse 16 | run 52 | GATED-OFF 16 | SEAT-ASYMMETRIC: none
```

| class | maps | why |
|---|---|---|
| **REFUSE (8)** | archipelago, heart, lighthouse, moonrise, saga, snowflake | `FS_MAP_SKIP`, **grid-confirmed** (v534 F2) |
| | midgard | `FS_V525_CRIPPLE_MAPS`, **grid-confirmed** (v524 ch.1) |
| | inv_tiny8 | 8×8, under `FS_V525_MIN_MAP_DIM = 10` |
| **RUN (26)** | antler, atoll, auroraveil, drakkarfjord, drumlin, eider, fjordgate, frostgate, glacierkeep, hive, icefloe, inv_duel16, inv_hsym16, inv_large30, inv_mid20, inv_pierce16, inv_small12, inv_vsym16, inv_wide30x14, jackpot, meander, nordkap, ragnarok, royale, valkyrie, yulerune | |

**Digit-for-digit identical to the v535 build's enumeration**, independently
re-derived here on a different tree — which is the check that the port did not
change the verdict.

**Intersected with the live 15-map pool** (`tools/overnight_pool26.sh:129`):
the gate fires on exactly **{archipelago, midgard}**, the commission's set,
**as a measurement rather than a definition** — it moves if the pool or the
floors move.

### 3.1 THE DIRECT ENGINE-SIDE DOSE READ, both verdicts, four cells

`logprobe.sh` / `OUT_logprobe.txt`, `04:23:28Z`. The tape is **stderr from live
games**, not our own replay stdout (CLAUDE.md: `print()` is stripped from
platform replays; locally stderr is real). Opponent `bots/_x3r0v169mjolnir`.

| map | arm | `V538GATE` lines | first verdict | **`V537 SOCKET` claims** |
|---|---|---|---|---|
| **archipelago** *(REFUSES)* | parent | 0 | — | **2** |
| **archipelago** | **v538** | 4 | `refuse=1` | **0** |
| **nordkap** *(RUNS)* | parent | 0 | — | **2** |
| **nordkap** | **v538** | 4 | `refuse=0` | **2** |

⇒ The gate reaches the engine, prints **both** verdicts, and suppresses the
claim on exactly one of the two boards.

---

## 4. THE MECHANISM TEST — the three decisive cells, with predictions stated

`scratchpad/s52_v538_build/mech/` (`04:10:04-04:17:02Z`) and `mech2/`
(`04:24:42-04:31:21Z`). **Three arms INTERLEAVED** by `run_battery.py` (all arms
of a cell adjacent, sharing one wall-clock slice — v518 finding 2 measured a
4.6 pp false positive from pooling non-time-adjacent local fixtures), in blocks
of five seeds. Opponent `bots/_x3r0v169mjolnir`, the live holder tree.
**3 maps × 30 seeds × 2 seats × 3 arms = 540 games per run**, `PAR=4`,
**0 tracebacks in 1,080 games**.

⭐ **RUN 2 IS THE SAME GRID WITH THE ARM ORDER REVERSED** (`v538refine` first in
run 1, last in run 2). That is a control on the interleaving itself, and it is
what makes §5's glacierkeep sign-flip readable.

**DEFF:** local screens are balanced-by-construction and read pair-weighted
DEFF = 0.98 (s39 audit), so naive intervals are used and are marginally
conservative. Both contrasts share every (run, map, seed, seat) cell, so the
test is **paired McNemar**, and pooling across runs pairs **within** a run only
(`pool.py`, `--selftest` PASS).

### 4.1 THE THREE CELLS, POOLED OVER BOTH RUNS (n = 120 per arm per cell)

| cell | prediction | v536trust | v537socket | **v538refine** | v537→v538 McNemar | **verdict** |
|---|---|---|---|---|---|---|
| **archipelago** *(GATED)* | recovers toward v536 | 57/120 · 47.50 % | 20/120 · **16.67 %** | **61/120 · 50.83 %** | 50 / 9 discordant, **z = −5.34**, **+34.17 pp** | ⭐ **MET, and to PARITY with v536** (z = −0.53 vs v536) |
| **yulerune** *(runs — falsifier)* | gains must HOLD | 11/120 · 9.17 % | 44/120 · 36.67 % | **58/120 · 48.33 %** | 22 / 8, z = −2.56, **+11.67 pp** | **HELD** (and see §5.2 — this one is a surprise) |
| **glacierkeep** *(runs — falsifier)* | gains must HOLD | 23/120 · 19.17 % | 52/120 · 43.33 % | **56/120 · 46.67 %** | 38 / 34, **z = −0.47**, +3.33 pp | **HELD — and correctly NULL** |

Per-cell 95 % half-width at n = 120 is **±8.95 pp**; at n = 60 it is ±12.65 pp.

### 4.2 THE FALSIFIER, STATED AS THE COMMISSION STATED IT

> *"if gating refusing-map claims costs siege-active cells, the story is wrong."*

| cut | v536trust | v537socket | **v538refine** | v537→v538 |
|---|---|---|---|---|
| **RUNNING maps pooled** (glacierkeep + yulerune, n = 240/arm) | 34 · 14.17 % | 96 · 40.00 % | **114 · 47.50 %** | 60 / 42 discordant, **z = −1.78, +7.50 pp** |
| v538 vs v536trust on the same cut | — | — | — | 96 / 16, **z = −7.56, +33.33 pp** |

⇒ **The gate costs the siege-active cells NOTHING that this fixture can see**, and
**the socket plank's whole gain over `v536trustport` on those boards survives
the gate.** The falsifier does not fire.

### 4.3 THE MIDGARD CELL — the trade the commission named, measured

`scratchpad/s52_v538_build/midg/`, `04:32:59-04:35:01Z`, same three arms, same
opponent, 30 seeds × 2 seats = **60 games/arm**.

| | v536trust | v537socket | **v538refine** |
|---|---|---|---|
| wins | 34/60 · 56.67 % | 35/60 · 58.33 % | **39/60 · 65.00 %** |
| v537→v538 McNemar | — | — | 16 / 12, **z = −0.76, +6.67 pp** |
| timely-kill rate (primary) | 36.67 % | **48.33 %** | 40.00 % |
| median kill round (diagnostic) | r236 | **r205** | r281.5 |

⇒ **The feared midgard cost does not appear on wins** — the point estimate is a
non-significant *gain*. ⚠ **But its timely-kill rate falls 48.33 % → 40.00 % and
its median kill round moves r205 → r281.5**, which is the one number in this
build that moves the wrong way for the programme bar. At n = 60 (hw ±12.6 pp)
neither is resolved; **it is reported, not resolved.**

### 4.4 THE KILL-ROUND BAR, all four cells pooled

`PROGRAMME.md`'s primary is the **timely-kill rate: the share of ALL games
ending in a core-kill by r300.**

| cut | v536trust | v537socket | **v538refine** |
|---|---|---|---|
| **timely-kill rate, 3-map pool (n = 360/arm)** | 9.44 % | 8.06 % | **16.67 %** |
| games ending at r1000, 3-map pool | 45 | **28** | 36 |
| timely-kill rate, archipelago alone | 25.83 % | 7.50 % | **25.83 %** |
| timely-kill rate, midgard alone | 36.67 % | **48.33 %** | 40.00 % |

⇒ **The primary RISES sharply on the pool this build measures (+8.61 pp vs the
parent) — the plank is not off-programme on the bar as written.** The r1000 tail
grows slightly against v537socket (28 → 36 of 360) and shrinks hard against
v536trust (45 → 36). ⚠ **This is a 4-map, one-opponent, local cut; the kill-round
verdict is the builder's powered screen, not this build's.**

---

## 5. ⭐⭐ THE SURPRISE — cells moved where the gate cannot act

**Written down before it is explained.** Run 1 read v538refine **above**
v537socket on **glacierkeep (+20.0 pp, z = −2.06)** and **yulerune (+11.7 pp,
z = −1.70)**. **The gate returns claim-ON on both of those boards** — §3's
predicate table, and §6's NOISE_OFF grid proves the two trees are **row-identical
on all 30 running-map cells**. A gate that cannot fire cannot have caused it.

That forced a control this build did not plan.

### 5.1 THE SAME-BOT SWING — two byte-identical copies of the parent

`scratchpad/s52_v538_build/twin/`, `04:17:51-04:22:34Z`. `twinA` and `twinB` are
**byte-identical copies of `bots/_v537socket`** (verified: the md5 of the md5s of
their five files match), run as two separate arms on the identical grid, same
opponent, 30 seeds × 2 seats. **360 games, 0 tracebacks.** The arms are
NOISE_ON, and `NOISE_ON` resolves to `random.Random().randrange(97)` — an
**unseeded** draw (`main.py:1184`), so every game draws a fresh spawn salt.

| map | twinA | twinB | **Δ (same bot!)** | z |
|---|---|---|---|---|
| archipelago | 10/60 · 16.67 % | 5/60 · 8.33 % | **+8.33 pp** | +1.39 |
| glacierkeep | 22/60 · 36.67 % | 29/60 · 48.33 % | **−11.67 pp** | −1.30 |
| yulerune | 27/60 · 45.00 % | 23/60 · 38.33 % | **+6.67 pp** | +0.94 |
| **POOL** | 59/180 · 32.78 % | 57/180 · 31.67 % | +1.11 pp | +0.26 |

⇒ **This fixture's own per-map swing at n = 60 is up to ±11.7 pp with |z| up to
1.4, on code that is provably the same.**

### 5.2 AND THE SECOND RUN SETTLED IT — for one cell, not the other

| cell | run 1 (v538 first) | run 2 (v538 last) | pooled | reading |
|---|---|---|---|---|
| **archipelago** | +30.00 pp | **+38.33 pp** | **+34.17 pp, z = −5.34** | **replicates, and far outside the twin swing** |
| **glacierkeep** | +20.00 pp | **−13.33 pp** | +3.33 pp, z = −0.47 | ⭐ **SIGN FLIPS — it was the fixture, exactly as the twin control implied** |
| **yulerune** | +11.67 pp | **+11.67 pp** | +11.67 pp, z = −2.56 | ⚠ **UNEXPLAINED** |
| RUNNING pooled | +15.83 pp | −0.83 pp | +7.50 pp, z = −1.78 | consistent with the null |

⚠ **YULERUNE IS THE RESIDUAL AND NO EXPLANATION IS OFFERED.** It reads the same
delta twice, in runs whose arm order was reversed, on a board where §6 proves the
two trees row-identical under NOISE_OFF and where the gate returns claim-ON. Arm
order was the candidate and it was tested by reversing it; it did not move the
cell. The remaining candidates — a CPU-budget interaction from the extra
gate-verdict call at r1, or a 1-in-100 draw — are **not measured here**. Filed in
§8 as the first thing to test, not as a story.

⇒ **The honest reading of the running-map cells is the POOLED one: +7.50 pp,
z = −1.78, consistent with the null the mechanism requires** — with a residual
that is named rather than absorbed.

---

## 6. FLAG-OFF IS `bots/_v537socket` — FOUR WAYS

### 6.1 Static (`test_flagoff.py`, `OUT_flagoff.txt`, **PASS**)

| check | result |
|---|---|
| `raid.py` md5-identical to the frozen parent | **yes** |
| exactly the four intended files differ | `doctrine.py, eco.py, main.py, siege.py` |
| every v538 read site is **inside a function body** | **3 of 3** — `eco.py:645` (×2), `siege.py:577` |
| all three v538 names are read somewhere | **yes** |
| module-level defaults deriving from a v538 flag (the v515 finding-3 hazard) | **0 across the whole tree** |

**Every guard driven to both verdicts.** ⛔ **THE DEAD-FLAG POSITIVE CONTROL:** a
read-site scanner that cannot say *"nobody reads this"* cannot certify
*"everybody reads this in a body"*. v535's control flag (`FS_V530_MOUTH_SEATS`)
**does not exist on this lineage** — v537 descends v536trustport ← v529merge,
which never carried the home package — so a live dead flag was **found by
enumeration** (every `FS_*`/`LOKI_*` definition minus every `Load` site;
7 candidates) rather than assumed: **`FS_V525_LOG`, defined in `doctrine.py`,
read nowhere. The scanner returns 0 sites for it and >0 for `FS_V537_SOCKET`,
and the flag is asserted to be actually DEFINED so that "0 sites" cannot mean
"misspelled name".**

### 6.2 Predicate-level, whole pool

With `FS_V538_CLAIM_GATE = False` the predicate returns **exactly
`FS_V537_SOCKET` on all 68 pool cells**, including the 16 where flag-on
deliberately differs; **gate-ON differs on 16 of 68.** And gate-off **never
calls** the siege helper — proved by monkeypatching it to raise. ⛔ **The trap is
a `BaseException`, not an `Exception`**, because `_v538_claim_on` deliberately
catches `Exception` ("unreadable gate ⇒ parent behaviour") and would swallow the
control; **and the same trap is re-armed with the gate ON and MUST fire**, or the
first half only proves the trap was never armed. Both come out right.

### 6.3 Behavioural — 250 local NOISE_OFF games

`scratchpad/s52_v538_build/ident/`, `04:07:15-04:08:54Z`. **Every bot in the
fixture is NOISE_OFF, including the opponent** (`opp_off` =
`bots/_v488beltbreak2` with `NOISE_ON = False`). Maps **archipelago, midgard**
(REFUSING) + **glacierkeep, yulerune, nordkap** (RUNNING); seeds 1-5; both seats
= **50 cells per arm**. Compared on every column except `tag`, `arm` and
`winner` — ⛔ `winner` carries the winning bot's **directory name** and would
differ for identical outcomes; `ours` (US/OPP/NONE) carries the same outcome
team-neutrally and **is** compared, as are `cond`, `turn`, `tracebacks`,
`ours_mined`, `opp_mined`.

| arm | what it is |
|---|---|
| `par_off` | `_v537socket`, NOISE_OFF |
| `par_twin` | a **byte-identical copy** of `par_off` — the fixture's determinism control |
| `v538_off` | `_v538refine`, NOISE_OFF, gate **ON** |
| `flagoff_off` | `_v538refine`, NOISE_OFF, `FS_V538_CLAIM_GATE = False` |
| `masteroff_off` | `_v538refine`, NOISE_OFF, `LOKI_FS_V538 = False` |

| pair | shared cells | rows differing | **REFUSE cells** | **RUN cells** |
|---|---|---|---|---|
| `par_off` vs `par_twin` *(determinism control)* | 50 | **0** | 0 / 20 | 0 / 30 |
| `par_off` vs **`flagoff_off`** | 50 | **0** | 0 / 20 | 0 / 30 |
| `par_off` vs **`masteroff_off`** | 50 | **0** | 0 / 20 | 0 / 30 |
| `flagoff_off` vs `masteroff_off` | 50 | **0** | 0 / 20 | 0 / 30 |
| **`par_off` vs `v538_off`** | 50 | **20** | **20 / 20** | **0 / 30** |

⭐ **THAT LAST ROW IS THE DOSE AND ITS SCOPE IN ONE LINE: the gate changes every
single cell of the boards it fires on and not one cell of the boards it does
not.** `rowdiff.py --selftest` **PASS**: the comparator was driven the other way
by corrupting one side of a pair that currently reads 0, and both mutants
(`turn +1`, `ours` flipped) moved **exactly 1** row.

⚠ **AND ONE HONEST PROPERTY OF THIS FIXTURE: THE SEED IS INERT UNDER NOISE_OFF.**
Measured on the tape — for every (arm, map) bucket of 10 games the number of
distinct (seat, outcome) signatures is **2**, i.e. one per seat. `NOISE_ON` is
the only randomness these bots have, so 50 cells per arm are **5 maps × 2 seats
of distinct play**, repeated. That does not weaken an identity claim (identity is
asserted cell-by-cell, and a repeated cell still has to match) but it does mean
**this fixture is a determinism-and-dose instrument, not a sample.**

### 6.4 Arm construction

Every flag substitution is applied **at the definition site**, never appended
(`mkarm.sh`), and each arm's flag lines are printed and banked
(`OUT_arms.txt`) — **exit code is not the health signal, the flag line is.**
⭐ **Two real defects were fixed in this build's copy of `mkarm.sh`, both of
which the v537 report deferred (§9.2 item 7):** the **mode-444 hazard** now
`chmod -R u+w`s *before* the first write **and on the pre-existing destination**,
because `rm -rf` cannot remove a read-only tree either; and the flag-echo used
`$K[...]`, which **zsh parses as an array subscript**. `tools/*` was still not
touched — the fix lives in the scratch copy.

---

## 7. FAILURE / WATCH REEL — D16

All under `scratchpad/s52_v538_build/`; each row is a **paired cell** — same map,
same seed, same seat, same opponent — so the two files differ only by the plank.

| # | what to watch | treatment | control |
|---|---|---|---|
| 1 | ⭐ **THE RECOVERY, AND IT IS ALSO A TIMELY KILL.** The claim is not made, the r1 builder turn goes back to the raid, and the core dies at r174 instead of ours dying at r481. | `mech/rep/v538refine_archipelago_s1_A` — **WIN r174**, core kill | `mech/rep/v537socket_archipelago_s1_A` — **LOSS r481** |
| 2 | **THE TIEBREAK ESCAPE.** The control never closes and loses the r1000 tiebreak on `titanium_collected`; the gated arm kills. | `mech/rep/v538refine_archipelago_s16_B` — **WIN r393** | `mech/rep/v537socket_archipelago_s16_B` — **LOSS r1000, tiebreak** |
| 3 | ⚠ **THE COST CELL, and there are 5 of them in run 1's 60** (against 23 the other way). The gate stands the claim down and we lose a game the claim would have won. | `mech/rep/v538refine_archipelago_s10_A` — LOSS r325 | `mech/rep/v537socket_archipelago_s10_A` — **WIN r453** |
| 4 | ⭐ **THE SINGLE-VARIABLE VIEW, NOISE_OFF BOTH SIDES.** midgard, the *other* gated board: same fixture, gate the only difference, kill lands **118 rounds earlier**. | `ident/rep/v538_off_midgard_s1_B` — **WIN r152** | `ident/rep/par_off_midgard_s1_B` — WIN r270 |
| 5 | **THE NO-OP, which is the point of the gate.** A RUNNING board under NOISE_OFF: the two arms are byte-for-byte the same game. | `ident/rep/v538_off_glacierkeep_s1_A` — WIN **r121** | `ident/rep/par_off_glacierkeep_s1_A` — WIN **r121** |

**Re-run recipe for any mechanism cell:**
```
.venv/bin/fcode run bots/_v538refine bots/_x3r0v169mjolnir \
    maps/<map>.map26 --seed <n> --tle 10 --replay <path>
```
(swap the two bot arguments for a seat-B cell; `bots/_v537socket` for the
control arm.)

---

## 8. MANIFEST + WHAT THIS BUILD DID **NOT** DO

### 8.1 Instruments — all under `scratchpad/s52_v538_build/`

Five of the nine are **copies** of the v535 build's instruments, re-pointed at
the v538 predicate; the originals were never edited in place.

| instrument | what it establishes | tape | selftest drives the other way |
|---|---|---|---|
| `harness.py` | the unit harness; a real `Player`, a fake `Controller` over a real terrain grid | — | the fixture must be able to LIE (corrupted grid reads corrupted); off-map raises; the parent tree must lack the predicate |
| `gatemap.py` | §3 — where the gate binds, 68 cells | `OUT_gatemap.txt` | 8 mutants incl. both geometric floors, grid-confirmed skip, signature-with-wrong-grid, both flag mutants, cache cost |
| `test_called.py` | §2 — CALLED not re-derived, on **this** tree | `OUT_called.txt` | scanner must FIND the tokens in the originals; bogus anchor must flip `_fs_gate` on a board asserted to RUN |
| `test_flagoff.py` | §6.1-6.2 — bytes, AST, read sites, predicate identity | `OUT_flagoff.txt` | ⭐ dead-flag control found by enumeration; `BaseException` trap armed both ways |
| `rowdiff.py` | §6.3 — game-row identity, split REFUSE vs RUN | `OUT_rowdiff.txt` | corrupts a **0-difference** pair; 2 mutants each move exactly 1 row |
| `wintab.py` | §4 — per-map table + paired McNemar + the timely-kill primary | `OUT_wintab*.txt` | perfect flip / identical arms / all-win / all-loss / a late kill that must NOT count / a NOWINNER row |
| `pool.py` | §4.1, §5.2 — pools the two runs, pairing **within** run | `OUT_pool.txt` | two runs that add; two runs that cancel; the key must not cross-pair |
| `logprobe.sh` | §3.1 — the direct engine-side dose read | `OUT_logprobe.txt` | both maps × both arms, i.e. both verdicts by construction |
| `mkarm.sh` | the arms; prints every flag line rather than trusting `$?` | `OUT_arms.txt` | — |

Drivers: `ident_drive.sh`, `mech_drive.sh`, `mech2_drive.sh`, `twin_drive.sh`,
`midg_drive.sh`. Freezes: `PARENT_FREEZE.md5`, `PARENT_REFREEZE.md5`.

⛔ **ONE INSTRUMENT DEFECT WORTH RECORDING, because it failed silently in the
"everything is fine" direction:** the first `mech_drive.sh` built its seed list
with `seq -s, $a $b`. **BSD `seq` APPENDS the separator after the last element**
(`1,2,3,4,5,`), which `run_battery.py` parses as an empty seed and dies on
`int('')` — and the driver then printed all six blocks *"done"* in under one
second and `MECH DONE`. **A log line saying the work finished is not evidence the
work happened; the row count is.** Caught by `wc -l` on the tape, not by the log.

### 8.2 Deferred — named, not hidden

1. ⛔ **ANY CURRENCY READ.** Every win column here is n = 60 or 120 per cell on a
   4-map, one-opponent local fixture whose same-bot swing §5.1 measures at up to
   ±11.7 pp. **The full-pool powered screen against `bots/_x3r0v169mjolnir` is
   the builder's.**
2. ⚠ **THE YULERUNE RESIDUAL (§5.2)** — +11.67 pp twice on a board where the gate
   cannot act and the trees are proved row-identical under NOISE_OFF. **The
   first thing to test**, and the cheapest test is a twin control *on yulerune
   specifically* at larger n, plus a CPU read of the r1 builder turn with and
   without the gate call.
3. ⛔ **ANY CPU / TLE MEASUREMENT.** The gate adds one `_fs_map_gated` call per
   body per game, cached, inside a four-round window. Not measured against the
   10 ms budget; no CPU claim is made — **and item 2 is exactly why that
   omission is not free.**
4. ⚠ **THE OTHER SIX REFUSING BOARDS ARE UNMEASURED.** The gate fires on eight
   maps pool-wide; only archipelago and midgard are in the live 15-map pool and
   only those two were played. heart, lighthouse, moonrise, saga, snowflake and
   inv_tiny8 are gated on geometry alone.
5. ⛔ **THE v535 CORNER GATE IS STILL NOT ON THIS LINEAGE.** This build ported the
   *reader*, not the corner plank's gate. Whether `FS_V535_CORNER_GATE` also pays
   on the v537 chassis is untested, and the machinery is now sitting there for it.
6. ⛔ **v537's OWN DEFERRED LIST IS INHERITED UNTOUCHED** — the `_pick` anchor
   asymmetry, the glacierkeep residual (we claim at r1 and still deliver nothing
   in 57 % of glacierkeep games), no re-claim after destruction, and MOUTH not
   ported. None of them is this build's plank.
7. ⛔ **`tools/*` UNTOUCHED AGAIN.** The two `mkarm.sh` defects fixed in §6.4 were
   fixed in the **scratch copy**; the repo's own arm-builder still carries them.
   Three builds old now.

---

## 9. HONEST LIMITS

* **Four maps, one opponent version, and one of the four is the treatment
  board.** The right four for this question — both gated boards plus the two
  siege-active cells the falsifier names — and the wrong denominator for a
  release verdict.
* **n = 60 per (map, arm, run) cell ⇒ ±12.65 pp; n = 120 pooled ⇒ ±8.95 pp.**
  Only archipelago (z = −5.34) clears this fixture's own noise by a margin that
  is not arguable. glacierkeep's run-1 result did not, and flipped sign.
* **The identity fixture's seed is inert** (§6.3): 50 cells per arm are 10
  distinct game shapes repeated. It proves determinism and dose, not rate.
* **The gate's verdict is the siege's verdict, so this build inherits every
  hedge on `_fs_map_gated`** — including that the refusing set is a property of
  the current floors and the current pool, re-measured here and not fixed.
* **All local.** Per directive point 6 this **prioritises** the road; it retires
  nothing. No live-team leg was fired.
* **`_v535_map_refuses` is a port, and §2 re-verified it structurally,
  behaviourally in the harness, and on the engine — but a port carries the
  original's design decisions too**, including that the reader keeps a cache
  separate from `fs_gate_ok`. If that separation is ever wrong, it is now wrong
  in two trees.
