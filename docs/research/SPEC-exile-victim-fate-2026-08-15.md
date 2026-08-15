# SPEC — EXILE victim fate in `throws.tsv`, and the field lethality of a border throw

**Written 2026-08-15T04:34Z (`date`).** Decoder change + corpus read, zero games
played. Builder-arm subagent task.

---

## 1. THE DEFECT

`tools/corpus/replay_throws.py` populated `life` / `core_atk` / `any_atk` /
`reached` for `kind == "INSERT"` only. One line did it: records entered the
`active` dict under `if kind == "INSERT"`, and only `active` records ever had
`close()` called. Measured on the live 580,697-row `corpus/throws.tsv`:

| kind | n | rows with `life != -1` | distinct `life` values |
|---|---|---|---|
| INSERT | 114,972 | **100.0%** | 990 |
| **EXILE** | **243,790** | **0.0%** | **1** |
| RETREAT | 39,455 | 0.0% | 1 |
| UNATTRIB | 1,783 | 0.0% | 1 |

⛔ **For an EXILE row `-1/0/0/0` means NOT APPLICABLE, not "measured zero".** The
constant column reads as a clean negative on exactly the question the
launcher-kidnap plank asks. A finding was published off it on 2026-08-14 and was
wrong.

**Why the asymmetry existed, and it is the thing a successor should watch for:
the victim of an EXILE is the ENEMY'S unit.** The INSERT machinery is written
around *our ferried raider* — `core_atk` and `reached` are own-team-forward
semantics — and the victim never had a home in it. `border` was always measured
for every kind and always varied; that half was sound.

## 2. THE CHANGE

Three appended columns, populated for **every** kind:

| column | meaning |
|---|---|
| `vfate` | `UNTRACKED` \| `TRUNCATED` \| `DIED` \| `RETHROWN` \| `ALIVE_END` |
| `vlife` | rounds from **this** throw to that fate event; `-1` **iff** untracked |
| `vhp` | `UpdateHp` events naming this bot inside the tracked window; `-1` iff untracked |

Mechanism reuse, not reinvention: a `vclose(rec, rnd, fate)` twin of `close()`,
and a **separate `vtrack` dict**. The separation is load-bearing — `active`
closes only on a re-INSERT or a removal, `vtrack` closes on a throw **of any
kind** or a removal, so folding victims into `active` would silently change
`life` on INSERT rows, i.e. a regression dressed as an extension.

⛔ **`UNTRACKED` and `ALIVE_END` render differently on purpose.** "We followed
this bot to the end of the replay and it never died" and "we could not follow
this bot" collapse to the same `-1` under any single-sentinel scheme, and that
collapse is what made the old column unauditable.

⛔ **`TRUNCATED` exists because `fields()` slices `buf[i:i+length]` and Python
truncates silently.** A half-written replay yields a short turn list with no
error; every open window would then read `ALIVE_END` and every post-break death
would be invisible — **the flattering direction for "the throw did not kill
it".** `check_framing()` is imported from `tools/wincond_backfill.py` (one
implementation, one place a wire-format change lands). The file is **not**
refused, because refusing would change the INSERT rows this decoder has always
emitted; its victim columns are marked instead.

`vhp` is the discriminator without which the plank cannot be priced: a victim on
a border tile can die because its own off-map query raised (the plank) or because
the landing tile sat in a turret line (geometry). **`DIED` with `vhp == 0` is
"removed with no HP event in the window at all"** — the same signature
`tools/crash_census.py` uses. ⚠ It **conflates an uncaught exception with
`self_destruct()`**, exactly as `crash_census`'s own header says; that caveat
travels with every number below.

**Domain invariant verified, not assumed:** `RemoveEntity` carries only field 1
— 2,662 of 2,662 messages across an 80-replay stride, histogram `{(1,0): 2662}`
— so the decoder's ungated `for rn, _rw, rv in fields(ubuf)` is exact.

**`OPEN` is an internal state and raises if it reaches the TSV.** A registered
record that no path closed would emit `vlife == -1` with a tracked-looking
`vfate` — indistinguishable from `UNTRACKED`, re-creating the ambiguity this
change removes.

## 3. CONTROLS

**POSITIVE — INSERT output is byte-identical.** 846 replays (stride sample of
the 44,852-file archive), old decoder from `git show HEAD:` vs new:
**13,268 rows, `cut -f1-21` projections `cmp`-identical, 0 errors both sides.**
Runtime 21.25 s → 22.08 s (**+3.9%**).

**SELFTEST — synthetic replays through the shipped `census()` path.** A ~40-line
protobuf writer builds real `.replay26` bytes; a dict fixture would test a
parallel implementation and could not catch a wire-level defect. Every cell is a
pair differing by **one fact**: removal present/absent flips `DIED`/`ALIVE_END`;
one throw/two throws flips `ALIVE_END`/`RETHROWN`; HP events present/absent
moves `vhp` 0↔2; the same bytes intact/truncated flips `ALIVE_END`/`TRUNCATED`.

**NEGATIVE — mutation-tested, three mutants, all caught:**

| mutant | change | result |
|---|---|---|
| `m_overfire` | a re-throw closes as `DIED` | 2 cells fail, incl. the 152-throw fixture (`DIED 151`) |
| `m_noreg` | victims registered only for INSERT (**the original defect**) | 14 cells fail; fixture reads `UNTRACKED`, **0% populated — visibly different from 100% zero** |
| `m_nohp` | `vhp` never increments | 2 cells fail |

**⭐ REAL FIXTURE, and it is a NEGATIVE one on purpose.**
`77d7e100-6cb3-4c49-85cc-e91192caf8cd_game_1` vs 0033 v57: one enemy builder
(bot 5) thrown **152 times, r241→r996, all 152 landings on a border tile** of a
10x10 map. A bot still being thrown at r996 of a 1000-round game demonstrably did
not die, so the fixture can only be passed by a decoder that reports survival.
Decoded: **rows 152 · border 152 · RETHROWN 151 · ALIVE_END 1 · DIED 0.**
It runs inside `--selftest`.

**HAND-READ OF ONE CLAIMED KILL, off the wire, with no use of the tracker.**
`19dd8e1d-…_game_1`, bot 85:

```
r59 MOVE   id=85 -> (3, 6)      one tile per round: it is walking
r60 MOVE   id=85 -> (3, 5)
r61 MOVE   id=85 -> (3, 4)
r62 MOVE   id=85 -> (2, 4)
r63 MOVE   id=85 -> (0, 9)      5-tile displacement: a throw, to a CORNER
r63 REMOVE id=85                same round
UpdateHp events naming bot 85 over the WHOLE game: NONE
```

## 4. THE READ

**Population:** all 9,141 archived games with `us_side ∈ {a, b}`, re-decoded
single-process, **0 file errors**, 139,200 throw rows. Of those, **39,932 are OUR
EXILE throws** (`tteam == us`, victim is the enemy's builder) across **2,421
games**, **16,006 landing on a border tile (40.1%)**, **1,803 on a corner**,
**2,063 distinct victims**, **984 games**.

**All four kinds now track 100.0%** (`INSERT` 19,146 · `EXILE` 111,606 ·
`RETREAT` 6,771 · `UNATTRIB` 1,677), against `life != -1` at 100.0% / 0.0% /
0.0% / 0.0%.

### 4.1 The estimator, and why it is not per-throw

**A crash can happen to a bot at most once** — the engine destroys it
permanently — so the unit is the **victim**, not the throw. Per-throw rates are
also wildly over-precise: the fixture above supplies 152 throws of which 151 are
"survived" by construction. The clean cell is **each victim's FIRST landing of a
class**, with the matched control being each victim's first *interior* landing.
Censoring: a `RETHROWN`/`ALIVE_END` window shorter than *k* is neither a death
nor an observed survival and is dropped; a `DIED` on the replay's last round is
engine cleanup, not a kill (6 of 1,793, 0.3%).

`vhp == 0` is genuinely rare among deaths — **42 of 1,793 = 2.3%** — so the
engine does emit HP events for combat kills and the signature is not vacuous.

### 4.2 Does the victim die?

Per victim, first landing of each class, death within 1 round:

| landing | victims | died ≤1r | **crash signature (died ≤1r AND `vhp == 0`)** |
|---|---|---|---|
| **BORDER** | 2,060 | 22 = 1.068% | **6 = 0.291%** [0.134%, 0.634%] |
| INTERIOR | 3,736 | 15 = 0.401% | 1 = 0.027% [0.005%, 0.151%] |

RR 10.9x, **Fisher 2-sided p = 0.0098**. Any-cause: RR 2.66x, p = 3.1e-03.

**Dose-response on the mechanism's own axis — off-map neighbour count:**

| landing | off-map neighbours | victims | crash signature |
|---|---|---|---|
| interior | 0 | 3,736 | 0.027% |
| edge | 1 | 1,794 | 0.056% |
| **corner** | **2** | **307** | **1.629%** [0.698%, 3.755%] |

### 4.3 ⛔ AND THEN IT COLLAPSES INTO ONE ARM

| cut | first-border victims | died ≤1r | crash signature |
|---|---|---|---|
| **our v107** | 74 | 7 (9.46%) | **6 = 8.11%** |
| every other version | 1,986 | 15 (0.755%) | **0 = 0.00%** [0, 0.193%] |

v107 is the LOKI-14 kidnap arm. **All six crash-signature kills are v107's**, and
all six land against **exactly four opponents — S, Ship Happens, Troupe, vjg —
the four teams LOKI-14 was aimed at**, in **non-ladder** games.

**⭐ WITHIN-ARM CONTROL (same bot, same throw logic, different opponents):**

| v107 vs | first-border victims | crash signature |
|---|---|---|
| its 4 targets | 14 | **6 = 42.9%** [21.4%, 67.4%] |
| everyone else it met (CtrlAltDefeat, I Stone, The Bisons, gsxWins) | 60 | **0 = 0.0%** [0, 6.0%] |

**⛔ DECONFOUNDED: drop v107 and the dose-response vanishes.** Non-v107 arms put
**274 distinct enemy builders on a CORNER tile across 31 opponents** and killed
**0** by the crash signature; **1,753 on an edge**, also **0**. Pooled
**0 / 2,027**, 95% CI **[0, 0.189%]**.

v107 both *aimed at corners* and *met the vulnerable four*, so inside that arm
dose and target are collinear and neither can be credited. The deconfounded read
says the corner-vs-edge gradient in §4.2 is **entirely v107's target selection**,
not a property of corners.

### 4.4 Field vulnerability rate

**Per opponent — the number `#17` could not price:**

| exposure floor | opponents | vulnerable | rate |
|---|---|---|---|
| ≥1 first-border victim | 42 | 4 | **9.5%** [3.8%, 22.1%] |
| ≥5 | 33 | 2 | 6.1% |
| ≥10 | 29 | **0** | 0.0% |
| ≥30 | 17 | **0** | 0.0% |
| ≥100 | 7 | **0** | 0.0% |

The four vulnerable teams received **6, 1, 2 and 5** first-border victims
respectively. **Every opponent we hit more than nine times is immune.**

**Per victim:** 6/2,060 = **0.291%** overall; **0/2,027 = 0%** [0, 0.189%]
excluding v107; **0/930 = 0%** [0, 0.411%] on the **rated ladder**, where the
entire positive result is absent.

⚠ **Both directions of bias are live and they do not cancel.** 9.5% is biased
**up** — those four were *chosen* by LOKI-14, plausibly for suspected
vulnerability, so they are not a random draw. The ≥10 row is biased **down** for
the four, who never received that much dose. The honest sentence is the
conditional one: **vulnerability is real, concentrated in the weakest teams, and
absent from every opponent with meaningful border exposure.**

Against the caller's prior bound of ≤4.24% of the admissible population: the
**per-victim** rate is far below it (0.29%, and 0% off the LOKI-14 arm); the
**per-opponent** rate of 9.5% exceeds it but on a selected sample of four teams
totalling 14 victims.

## 5. WHAT THIS DOES NOT SAY

* `vhp == 0` cannot separate an uncaught exception from `self_destruct()`. The
  interior baseline (1/3,736) bounds that background at ~0.03%, which is why the
  six events are not plausibly baseline self-destructs — but "crash" is an
  inference, not a read.
* n = 14 carries the entire positive finding.
* Version and opponent are **perfectly collinear** for those four teams (only
  v107 ever met them at a border). This is the documented Bisons-v4 hazard: *our
  arm is better* and *their bot is worse* fit identically.
* Rule 6: this is corpus statistics. It may **prioritise** a live leg. It may not
  **close** the road.

## 6. COST

Full archive re-decode, **single process**: 44,852 replays at 846 / 22.2 s ≈
**19.6 minutes** (+3.9% over the previous decoder). The 9,141-game our-side
subset used here: ~4 minutes. The keeper daemon owns `corpus/throws.tsv`; this
work decoded to scratchpad and never wrote it, so the file picks the columns up
on its next scheduled rebuild.
