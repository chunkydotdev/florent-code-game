# SPEC — `tools/nav_lock_census.py` (the `#54` nav-limit-cycle census)

**2026-08-14T21:26:48Z (`date -u`) · head `dc471638` · builder lane, rebuild agent**
**Supersedes the lost `nav_limit_cycle_census.py`.  A rule that should be a
script is now a script, and this is its dated spec.**

---

## 0. WHY THIS EXISTS AT ALL

`nav_limit_cycle_census.py` measured how often our builder bots end up in a
two-tile navigation limit cycle.  It is simultaneously the **dose instrument**,
the **mechanism metric** and the **retirement predicate** for four queue rows —
`#54` (the cycle), `#63` (long-approach arrival), `#64` (spawnpocket) and the
`RETIRE60` plank — and two pre-registrations banked their pre-launch dose
through it.

**It has been lost twice.**  It never entered git; it lived in a session
scratchpad, was recovered once from two dying scratchpad dirs, and is now gone
for good along with both of its outputs (`census_v125.withmap.jsonl`,
`census_v125.jsonl`).  `/private/tmp/claude-501/...` held 86 session
directories on 2026-08-14 and holds **7** now — the purge that
`docs/coordination.md`'s own persistence note warned was coming.  This rebuild
is committed so there is no third time.

**Nothing of the original survived except prose.**  Everything below marked
INFERENCE was reconstructed from `QUEUE.md:139`,
`docs/research/HOME-LOCK-MECHANISM-2026-08-14.md` and
`docs/coordination.md:45586,45660`, then verified against the published figures.

---

## 1. THE ALGORITHM

### 1.1 Track construction

Per replay, for **our** builder bots only, decoded straight off the
`.replay26` wire — wire helpers imported from `tools/replay_census.py`, never
re-rolled (`tools/replay_schema.md` is the schema of record):

* `placeEntity` carrying `Entity.builderBot` (field 10) with our team byte →
  the bot's **spawn**.  The FIRST such record for an id is the spawn; later ones
  are state re-emits and must not restart the track (the rotation-re-emit guard
  in `replay_census.py` generalises).
* `moveBuilderBot` → position update.
* `removeEntity` → death.
* At the END of every round, every living bot appends its current position.

So `track[i]` is the bot's position at the end of its `i`-th living round, and
its absolute round is `spawn + i`.  **A bot's builder-rounds = `len(track)`**,
and the population's builder-rounds is the sum over bots.

### 1.2 The lock predicate

A window of consecutive track indices `[l..r]` **qualifies** iff

| # | condition | parameter | provenance |
|---|---|---|---|
| 1 | `r - l + 1 >= MIN_SPAN` | `MIN_SPAN = 50` | **RECORDED** (name and value) |
| 2 | at most `MAX_TILES` distinct positions in the window | `MAX_TILES = 2` | **INFERENCE** |
| 3 | every maximal run of identical consecutive positions inside the window — boundary runs included, truncated by the window edges — is at most `MAX_DWELL` rounds | `MAX_DWELL = 2` | **RECORDED** (name and value); the *reading* is inference |

**STRICT** (the headline metric) = a qualifying window that runs to the bot's
last living round: a *permanent* lock, never escaped.  `onset` is the earliest
index from which the tail qualifies; `strict_rounds = len(track) - onset`.

**SOFT** = the union of every qualifying window anywhere in the track (maximal
windows, merged where they overlap or abut so no round is double counted).

### 1.3 Other definitions

* **never acted** — no `builderBuild` (16), `builderHeal` (15) or
  `builderAttack` (13) update ever carried this bot's id.  ⚠ `destroy` and
  `self_destruct` surface as an *unattributed* `removeEntity`, so they are
  invisible here; "never acted" means "never built, healed or attacked".
* **map** — exact `(width, height, tile grid)` match against `maps/*.map26`;
  failing that, a `(width, height, coreA, coreB)` layout signature, reported
  with a `*` suffix; failing that, `UNKNOWN`.  midgard and ragnarok share dims
  AND core positions, so the signature stage refuses to guess when more than one
  map matches.
* **population** — `corpus/meta_join.tsv`, `ourver` derived per game as
  `teamAVersion` or `teamBVersion` according to `us_side`, with the standing
  `a→0, b→1` team mapping.

---

## 2. WHAT I HAD TO GUESS, STATED AS GUESSES

**(a) `MAX_DWELL` is a TIME, not a tile count.**  This is the whole ball game.
Read as "at most 2 distinct tiles", the v125 rate comes out **41.47%** instead
of 11.58%, because every parked builder counts as locked.  The correction is
`HOME-LOCK-MECHANISM-2026-08-14.md:150`, which says in passing that a pocket
produces *"either a stall (long dwell — **excluded by the detector's
MAX_DWELL = 2**) or a 2-cycle"*.  Dwell is therefore consecutive rounds on one
tile, and §2 of that same doc confirms the scale — *"dwell is exactly 1 in every
window"* — which is only meaningful for a time.

**(b) `MAX_TILES = 2` is not recorded anywhere.**  Only `MIN_SPAN` and
`MAX_DWELL` were.  It is inferred from the row's own vocabulary ("two-tile
lock", "≥50-round two-tile lock per bot per game") and is a separate named
constant so it can be swept.

**(c) STRICT = "the window reaches the bot's last living round".**  The row
distinguishes *"STRICT: 183,489/1,584,948 ... spent in permanent locks"* from
*"SOFT (any ≥50-round window): 19.29%"*, which fixes SOFT exactly and leaves
"permanent" to be read.  "Runs to the end of the bot's life" reproduces both
numbers; "alive at game end" does not (182,237 / 953 bots).

**(d) The window's LEADING run is bound by `MAX_DWELL` too.**  This is the one
genuinely unresolved edge and it is discussed in §5 — the alternative (leading
run exempt, i.e. an arrival stall counts as part of the lock) is measurably
*further* from the published figures, so the stricter reading is used.

**(e) The 1,160-game population is the 1,160 OLDEST v125 games by
`completedAt`.**  The archive now holds 1,185; the headline was taken at 1,160.
This is not a guess any more — see §4.1, it is confirmed to the digit.

---

## 3. HOW TO DRIVE IT

```bash
.venv/bin/python tools/nav_lock_census.py --selftest      # 30 unit checks
.venv/bin/python tools/nav_lock_census.py --controls      # positive + 5 negative
.venv/bin/python tools/nav_lock_census.py --ourver 125 --limit 1160 \
    --report --jsonl census_v125.jsonl
.venv/bin/python tools/nav_lock_census.py --game <replay> --team 1
```

Sweeps are flags, not edits: `--min-span`, `--max-tiles`, `--max-dwell`.

**Cost: 18.6 s wall clock for the full 1,160-game run** (~16 ms/game,
single-threaded, cold). The 1,185-game superset is 19.2 s.  `--limit` exists
for snapshot reproduction, not for speed — nothing here needs it.

The JSONL supersedes the original's two-file split: every record carries the
map name **and** the core positions, so map cuts and d² cuts no longer need a
join between two incompatible snapshots.  Per-bot fields: `id, spawn, life,
acts, strict, onset, strict_rounds, soft_rounds, lock_tiles, max_d2_own,
lock_d2_own`.  `lock_d2_own` and `max_d2_own` are new and exist for
`RETIRE60`'s clause-(c) carve-out, which needs "is this locked bot parked on our
spawn ring?" answerable without a second decode.

---

## 4. REPRODUCTION GATE

Population: `ourver = 125`, 1,160 oldest archived games, **0 parse errors,
100% coverage**.

### 4.1 The population is confirmed exactly

| cut | builder-rounds |
|---|---|
| 1,159 oldest | 1,584,123 |
| **1,160 oldest** | **1,584,948** ← published denominator, exact |
| 1,161 oldest | 1,586,241 |

A 7-digit exact hit, with neighbouring cuts ~1,000 away.  The population and the
track-construction rule (§1.1) are therefore both settled, and the whole residual
below lives in the numerator.

### 4.2 The eight gate figures

| # | figure | published | this rebuild | delta |
|---|---|---|---|---|
| 1 | locked builder-rounds | **183,489 / 1,584,948 = 11.58%** | 184,537 / 1,584,948 = **11.64%** | +0.06pp (+0.57% rel) |
| 2 | locked bots | **962** | **972** | +10 (+1.0%) |
| 3 | games with ≥1 locked builder | **47.6%** (552) | **47.8%** (555) | +0.2pp |
| 4 | locked bots that never acted | **39.81%** | **39.81%** (387/972) | **exact** |
| 5 | median onset round | **68** | **67** | −1 |
| 6 | midgard | **35.6%** | **35.8%** | +0.2pp |
| 7 | ragnarok | **14.1%** | **14.2%** | +0.1pp |
| 8 | valkyrie | **12.8%** | **12.8%** | **exact** |

### 4.3 Figures beyond the eight, all published, none tuned against

| figure | published | rebuild |
|---|---|---|
| drakkarfjord | 11.0% | **11.0%** exact |
| fjordgate | 8.0% | **8.0%** exact |
| icefloe | 3.2% | **3.2%** exact |
| archipelago | 15.8% | 16.0% |
| glacierkeep (the 64 "UNKNOWN" games) | 6.25% | 6.3% |
| SOFT (any ≥50-round window) | 19.29% | 19.46% |
| sensitivity `min_span=100`, rounds | 9.69% | 9.73% |
| sensitivity `min_span=100`, games | 27.6% | 27.8% |
| valkyrie lock tiles (25,14)↔(25,15) | 19 games | **19** exact |
| valkyrie mirror (4,14)↔(4,15) | 18 games | **18** exact |
| HOME-LOCK §2 trajectory table | 20 bots, tile pairs + maps | **20/20 exact** |

### 4.4 Controls — both recorded ones reproduce

**POSITIVE — 11/11 on `483b5bcd` g1, including all six hand-traced ids.**
Reproduced: 11 of 11 of our builders read locked, ids `[4, 6, 8, 11, 13, 18,
394, 435, 627, 724, 760]` ⊇ `{4, 11, 18, 435, 724, 760}`.

**NEGATIVE — 1/6.**  The original published only the bare string
`negative control 1/6`; **how that group was built was recorded nowhere.**  It
was recovered by enumeration: **game 2 of the same match, our own side, reads
exactly 1/6** and is the only cell in the match that does (g1 11/11, g2 **1/6**,
g3 0/6, g4 1/7, g5 1/5; opponent side 0/8, 0/9, 0/11, 0/8, 0/29).
**This control is load-bearing, not garnish: under the wrong (tiles-only)
reading of `MAX_DWELL` the same cell reads 3/6.**  It discriminates between the
two candidate predicates on its own.

Three further mutation controls ship in `--controls`, each driving a specific
clause to the other verdict on real wire data:

| control | what it mutates | result |
|---|---|---|
| N1 | team byte only, same replay | opponent side **0/8** vs our **11/11** |
| N2 | splice a 3rd tile into each traced bot's window | **6/6** flip to UNLOCKED (`MAX_TILES`) |
| N3 | cut each window to `MIN_SPAN − 1` rounds | **6/6** flip to UNLOCKED (`MIN_SPAN`) |
| N4 | replace each window with a stall on one lock tile | **6/6** flip to UNLOCKED (`MAX_DWELL`) |

N4 is the one that matters most: a detector passing N1–N3 but failing N4 is
precisely the detector that reports 41.5%.

`--selftest` adds 30 unit checks, including a 300-track × 9-parameter
randomised agreement test between the O(n) two-pointer and a naive O(n²)
reference, and drives the map identifier to all four of its verdicts (exact,
signature, ambiguous-refusal, unknown).

---

## 5. WHAT DID NOT REPRODUCE, AND THE DIAGNOSIS

**The residual is +0.57% on locked rounds and +1.0% on locked bots, with the
denominator exact and both controls exact.**  Reported rather than tuned away.

**What it is not.**  A parameter sweep over `min_span ∈ 47..54` ×
`max_dwell ∈ 1..3` (24 cells) contains **no cell** that reproduces
(962 bots, 183,489 rounds).  The two nearest cells bracket it and each misses on
the other axis:

| cell | rounds | bots |
|---|---|---|
| `min_span >= 50` (shipped) | 184,537 (11.64%) | 972 |
| **published** | **183,489 (11.58%)** | **962** |
| `min_span > 50` | 183,537 (11.58%) | 952 |

The `> 50` variant reproduces the *percentage* exactly and misses the bot count
by 10 in the other direction.  **No parameter choice satisfies both, which is
the evidence that the shipped constants were not fitted to the target.**

**What it most likely is — the left window edge (guess (d) in §2).**  The one
place the rebuild is known to disagree with a recorded artefact is bot 760 of
the positive control: the s39 hand tracer recorded a **606**-round window, this
detector reports **602**.  The bot arrives at (22,21) at index 22, sits there
**six** rounds, and only then begins the (22,21)↔(23,21) cycle.  The tracer
charged that arrival stall to the lock; this detector's `MAX_DWELL` clause cuts
into it.  So the leading run's treatment is genuinely ambiguous — and it was
measured both ways rather than assumed:

| leading-run rule | rounds | bots | games |
|---|---|---|---|
| bounded by `MAX_DWELL` (shipped) | 184,537 (11.64%) | 972 | 47.8% |
| exempt (arrival stall counts) | 189,469 (11.95%) | 1,008 | 49.1% |
| only the final run bounded | 194,123 (12.25%) | 1,030 | 50.2% |

**The published figure sits just BELOW the strictest of the three**, so the
original was at least as strict as this rebuild at that edge and possibly
stricter in some way I could not identify without fitting.  The exempt variant
is the one that matches the tracer's 606 — and it is measurably *further* from
the census figures, which is itself evidence that the tracer and the census were
different instruments (they were: `six_bot_oscillation.py` ran first, with a
parity window and no dwell clause).  ⚠ **`QUEUE.md:139` reports both scripts'
outputs in one sentence; the six window lengths are the TRACER's, the 11.58% is
the CENSUS's, and they are not the same detector.**

**Direction of the error.**  The rebuild is *biased slightly high*: it will over-
state the lock rate by roughly 1% relative.  For `#54`'s purpose (sizing a
workforce tax and reading a treatment/control ratio) this is immaterial, and it
fails in the conservative direction for a fix arm — a fix measured with this
instrument has a marginally *harder* bar to clear, not an easier one.
**It is not immaterial for a claim of the form "the rate is exactly X"**, and
any such claim should quote 11.6% ± the residual rather than 11.58%.

**Second-order item, `median onset 67 vs 68`.**  A one-round difference on an
integer median over 972 values is what the +10 bots produce; it is a consequence
of the residual above, not an independent defect.

---

## 6. TWO CORPUS FACTS FOUND ON THE WAY, BOTH LOAD-BEARING

**(1) The map files postdate the census, and two grids were reshipped.**
`maps/{valkyrie,glacierkeep,midgard,ragnarok,drakkarfjord,auroraveil,frostgate,
icefloe,royale,yulerune}.map26` were **first committed in `f9fda96a`,
2026-08-14 22:07:52 +0200** — after the s39 census ran.  The valkyrie and
glacierkeep grids the platform served for the v125 games differ from those
committed copies by **10 and 9 tiles** respectively.  Exact-grid matching alone
therefore leaves 144 of 1,160 v125 games unnamed (80 valkyrie + 64 glacierkeep),
which is the origin of the original's "64 UNKNOWN games ... verified by
dims+cores (14,2)/(14,26)" note.  The two-stage identifier resolves both and
flags them with `*` so a re-grid is never laundered into an exact match.
⇒ **Any per-map cut on valkyrie or glacierkeep is measured under the OLD grid
and must say so** — which is exactly the caveat `#54` already carries.

**(2) Every lock is an orthogonally adjacent tile pair.**  Tested as a candidate
extra clause: requiring the two lock tiles to be orthogonally adjacent drops
**0 of 972** bots.  So no lock in the v125 population is an artefact of a
launcher throw teleporting a bot between two distant tiles, and adjacency is not
worth spending a clause on.

---

## 7. CAVEATS THAT TRAVEL WITH ANY NUMBER OUT OF THIS TOOL

1. **us-only, `ourver = 125` archived replays.**  Not a field statistic.
2. **`ourver` is derived from `meta_join.tsv`'s per-match version fields**, not
   from the poll-time `elo_history.tsv` tag.  That is the better of the two, but
   a version boundary inside a match still lands wherever the platform stamped
   it — treat boundary cells as approximate.
3. **The population pools rated ladder with unrated challenge games** (300/860
   at the time of the original; 305/880 now).  Correct here, because the question
   is a property of our own code — but **any win-rate denominator taken off this
   population would breach the standing `meta_join` rule.**
4. **`a→0, b→1`** is inherited from the recovered script and is not
   independently re-verified.  It is however consistent with the positive
   control: `us_side='b'` on `483b5bcd` and team 1 is the side with the 11
   locked builders.
5. **DEFF.** Any interval on a cut of these games must enumerate its clusters
   per `CLAUDE.md` — MATCH and OPPONENT both live here, since a v125 cell holds
   several games from the same match and several matches against the same
   opponent.  The unrated pooled constant (1.833) is the starting point, not the
   answer; enumerate rather than look up.
