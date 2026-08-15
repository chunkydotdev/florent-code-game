# SPEC — `wincond` / `turns` backfill onto a full-coverage surface

**Item:** `QUEUE.md` row **#34**.
**Built:** 2026-08-15T03:5xZ (`date -u`, same shell as the runs below).
**Tool:** `tools/wincond_backfill.py` · **Output:** `corpus/wincond.tsv` (gitignored
by `corpus/.gitignore:2 *.tsv` — regenerable in 24 s, correctly not committed).

**THIS IS A TOOL, NOT A LEG.** It plays no games, creates no matches, and touches
nothing under `bots/`. It reads bytes already on disk. A pre-registration for a
corpus backfill would be ceremony: there is no treatment, no opponent, no arm,
and the verification is not a bar to clear but an EXACT agreement check against a
second, independent source (see CONTROLS). No `SCREEN-` doc is owed.

---

## 1. WHY — `R1000_IS_DEFEAT` makes this a defect, not a convenience

`PROGRAMME.md` carries `R1000_IS_DEFEAT: yes`, UNCONDITIONAL: a round-1000 game
is a defeat **even when we win it**. "How did this game end" is therefore a
**defeat-condition**, and a fixture that cannot report it cannot score itself.

`tools/panel_read.py:121` — the reader every unrated panel goes through — joins on
`corpus/meta_join.tsv`. That surface has **24 columns and none of them is an end
condition**. So every unrated leg this project has ever read was blind to the one
distinction that decides whether a win counts.

## 2. MEASURED COVERAGE, PER SURFACE

`tools/wincond_backfill.py --report`, 2026-08-15T03:54:55Z. ⚠ The corpus keeper
daemon writes to `corpus/` continuously; row counts drifted **+40 rows in
meta_join and +10 in our-games between two reads eight minutes apart** during this
work. Every count below is a snapshot, and no conclusion here turns on ±40 rows.

| population | n | `join.tsv` | `throws.tsv` | either | **BLIND** |
|---|---|---|---|---|---|
| OUR games (all) | 9,101 | 41.0% | 55.3% | 71.0% | **29.0%** |
| **OUR unrated** | **5,361** | **0.0%** | 51.0% | 51.0% | **49.0%** |
| OUR rated (ladder) | 3,740 | 99.7% | 61.6% | 99.8% | 0.2% |
| ALL archived (any team) | 44,230 | 8.4% | 32.6% | 35.8% | **64.2%** |

Why each surface falls short:

* **`corpus/ladder_games.tsv`** — has `cond` + `turns`, and is **rated-only by
  construction**: `tools/corpus/ladder_meta.py` walks
  `fcode match list --mine --type ladder`. 5,040 rows. Structurally cannot reach
  an unrated game.
* **`corpus/join.tsv`** — has `cond` + `turns`, but is the JOIN of decoded replays
  against `ladder_games.tsv`, so it inherits rated-only. 3,735 rows = exactly our
  ladder game count. **Unrated coverage 0 of 5,361.**
* **`corpus/meta_join.tsv`** — 44,230 rows, best platform coverage, **zero
  end-condition columns**.
* **`corpus/league_matches.tsv`** — MATCH-level (scores, versions, elo deltas).
  No per-game condition at all.
* **`corpus/throws.tsv`** — *does* carry `wincond` and `rounds`
  (`tools/corpus/replay_throws.py:43`), but emits **one row per THROW**, so it
  covers 14,586 of 44,431 files. ⛔ **It is selection-biased for this purpose:
  conditioning a win-condition read on "this game had a launcher throw" conditions
  on the treatment in every kidnap leg.** It is not a substitute and this spec
  does not treat it as one.
* **Shard tapes, `scratchpad/overnight*/**/*.tsv`** — **NOT blind. 169 tapes,
  ~583k data rows, `cond` + `turns` present BY NAME in 167; the other 2 have no
  header row at all** (`DEST14B.tsv`, `SENT41.tsv` — pre-existing, unfixed) and are
  reported as an **unnamed-schema class rather than indexed positionally**.
  0 unreadable. 8 tapes carry `# FIXTURE` lines, skipped leading and mid-file.
  **The gap is entirely a PLATFORM-surface gap.**

### 2a. ⚠ THE RELAYED "63% OF UNRATED FILES" DOES NOT SURVIVE CHECKING AS STATED

The queue row says *"63% of unrated files cannot be read for it"*. Measured:

* **Of OUR UNRATED files: 100% blind** on the surface panel reads use
  (`meta_join`), **49.0% blind** if the selection-biased `throws.tsv` is allowed
  to count.
* **64.2%** is the blind share of **ALL ARCHIVED files (any team)** — the number
  closest to 63, attached to a different population.

⇒ **The row's number describes the whole archive, not unrated files.** The row's
*claim* — that most of our free fixture is blind to the deciding distinction — is
**correct and if anything understated** (0%, not 37%, on the surface actually
read). Fixed here rather than argued: the number now carries its population.

## 3. IS IT RECOVERABLE? YES — FOR EVERY ERA, WITH ONE NAMED EXCEPTION

`Replay { Map map = 1; repeated Turn turns = 3; optional Team winner = 4;
string winCondition = 6; }`. `turns[i]` IS round `i`, so the count of
length-delimited field-3 occurrences is `turnsPlayed`.

* **Every blind file is on disk.** Of the 2,629 blind unrated files, **2,629
  (100.0%) are present in `replay_archive/`.** 0 of our 9,101 archived game rows
  are missing their replay.
* **No era is lost.** The oldest archived replays parse on the same path as the
  newest; the whole-archive scan returned **0 framing errors in 44,431 files**.
* ⛔ **THE ONE GENUINELY UNRECOVERABLE CLASS: the 25 `cond=error` / `turns=0` rows
  in `ladder_games.tsv` HAVE NO REPLAY.** Their `s3` replay key is the empty
  string — the platform never produced a file. They can be read from
  `ladder_games.tsv` (which is where they already are) and can **never** appear in
  a replay-derived backfill. **This is why `ABORTED` is a first-class klass rather
  than an absence: a joiner that finds no `wincond.tsv` row for such a match must
  not read that as "unclassified".**

## 4. THE METHOD — KEY ON `turns`, NEVER ON THE `cond` STRING

`klass` is a pure function of `turns`:

```
turns == 1000        -> R1000       (the defeat condition)
0 < turns < 1000     -> DECISIVE
turns == 0           -> ABORTED     (the cond=error class, its own bucket)
unreadable           -> UNREADABLE   (turns written as -1; NOT a summable count)
```

`wincond` is carried as a payload column and is **never** consulted to decide
`klass`. The reason is measured, not stylistic — **28 of 44,431 archived replays
have a `cond` string that disagrees with their turn count**:

| `wincond` | klass | n |
|---|---|---|
| core_destroyed | DECISIVE | 35,797 |
| titanium_collected | R1000 | 8,077 |
| harvesters | R1000 | 419 |
| titanium_stored | R1000 | 107 |
| **titanium_collected** | **DECISIVE** | **18** |
| **titanium_stored** | **DECISIVE** | **5** |
| **core_destroyed** | **R1000** | **4** |
| **coinflip** | **R1000** | **3** |
| **harvesters** | **DECISIVE** | **1** |

Two things fall out of that table:

1. **`coinflip` exists and is not in `ladder_games.tsv`'s vocabulary at all.**
   Three games were decided on the tiebreak ladder's 4th key. Any code
   enumerating win conditions from the rated surface has an incomplete domain.
2. ⚠ **`core_destroyed` AT `turns == 1000` (4 games) is a genuine ambiguity, and
   this spec does not resolve it unilaterally.** Rounds are 0-based, so 1000 turn
   buffers with a destroyed core means **a kill landing on the very last round**.
   `klass` follows the audit's mandated rule and calls it `R1000`; both columns are
   written so the lane can rule differently in a join. **It touches nothing today:
   all 4 — and all 3 `coinflip` games — are `us_side=none`, i.e. other teams'
   games. 0 of our 9,101 games are in the ambiguous class.**

## 5. CONTROLS — ALL DRIVEN, IN BOTH DIRECTIONS

`.venv/bin/python tools/wincond_backfill.py --selftest` → **SELFTEST PASS, exit 0**
(**23 checks, 0 FAIL**). The load-bearing ones:

| control | fixture | must be | drove |
|---|---|---|---|
| **POS-SYN** | 1000 turns, `cond="core_destroyed"` | R1000 | R1000 |
| **NEG-SYN** | 500 turns, `cond="titanium_collected"` | NOT R1000 | DECISIVE |
| **POS-REAL** | real archived file, platform says turns=1000 | R1000 | R1000 |
| **NEG-REAL** | real archived file, `cond=titanium_collected` **at turns=146** | NOT R1000 | DECISIVE |
| **ABORT-SYN** | 0 turn buffers | ABORTED, and asserted ≠ R1000, ≠ DECISIVE, ≠ UNREADABLE | ABORTED |
| **OVER-SYN** | 1001 turn buffers | REFUSED (raises) | `ReplayDomainError` |
| **ERR-TRUNC** | cut mid-field | UNREADABLE | `TruncatedReplayError` |
| **ERR-TAIL** | field 6 dropped, framing still valid | UNREADABLE | `TruncatedReplayError` |
| **ERR-WIRE** | illegal wire type | UNREADABLE | `TruncatedReplayError` |
| **ERR-ABSENT** | nonexistent path | UNREADABLE | `FileNotFoundError` |
| **DISCRIMINATOR** | 4 broken + 1 clean file in one batch | `R1000=0`, `UNREADABLE=4`, `ok=1` as **three separate facts** | as stated |
| **XVAL** | 3,735 real files vs the platform | exact agreement | **0 mismatches on `turns`, 0 on `cond`** |

The synthetic arms are deliberately built with the `cond` string set to the
**opposite** of what a cond-keyed rule would conclude, so a regression to
cond-keying fails POS-SYN and NEG-SYN immediately. **NEG-REAL is the sharpest:
it is a real game a cond-keyed tool misfiles.**

### 5a. XVAL is a POSITIVE CONTROL AGAINST AN INDEPENDENT SOURCE

`join.tsv`'s `cond`/`turns` come from `fcode match list` / `match info`
(`tools/corpus/ladder_meta.py:74`) — the platform's own bookkeeping, which never
touches the replay bytes this tool parses. **3,735 of 3,735 files agree exactly on
both columns, offset 0 in every one.** That is not a bar that was cleared; it is
two independent instruments returning identical values on every overlapping row.

### 5b. ⛔ TWO DEFECTS THE SELFTEST CAUGHT IN THIS TOOL, RECORDED BECAUSE THEY ARE THE POINT

1. **The first corruption fixture was a no-op.** It flipped the file's last byte —
   which landed inside the `winCondition` string payload and changed nothing the
   parser could notice. The check printed `[ok] status=ok`: *a corruption control
   the parser survives validates nothing.* Both replacement fixtures were
   mutation-tested to flip the verdict, and the clean bytes are asserted to still
   parse (so the fixture is not merely always-fail).
2. **That failure exposed a real hazard: truncation parses silently.**
   `fields()` reads a length-delimited field as `buf[i:i+length]`, and Python
   slicing truncates without complaint — so a half-written replay would have
   yielded a SHORT turn count with `status=ok`. **That fails in the flattering
   direction: it invents fast kills and deflates the r1000 rate, the exact
   quantity this table exists to measure.** Now guarded by `check_framing()`
   (bounds-checked walk) plus the empty-`wincond` tail guard.
   ⚠ **KNOWN LIMIT, stated rather than papered over:** a truncation landing on a
   field boundary *inside* the turn list — losing turns but keeping field 6 — is
   invisible to both guards. Nothing in the replay declares its own turn count, so
   there is no third check to add. Bounded by the XVAL result: 0 such cases among
   the 3,735 files where an independent source can check the count.

### 5c. AND A DEFECT THE GUARD CAUGHT IN AN AD-HOC SAMPLE

An early hand-rolled sample reported **1,030 of 6,000 files unparseable (17%)**.
The tool was right and the sample was wrong: `os.listdir()` had fed it the
**8,919 `.meta.json` files and 6 diagnostic subdirectories** that also live in
`replay_archive/` (53,357 entries, only 44,431 of them `.replay26`). The shipped
`build()` filters on the suffix. **Recorded because the error path produced a loud,
specific, countable signal instead of a quiet wrong number — which is the whole
design rule.**

## 6. NO-OP / ERROR-PATH DISCIPLINE

* **No bare `except: pass` and no `except: continue` anywhere.** Every per-file
  failure produces a ROW with `status=err:<Type>:<msg>` and `klass=UNREADABLE`.
* **`turns` is written as `-1` for unreadable rows** so a naive `sum()` cannot
  quietly absorb them as zero-round games.
* **`--build` exits 2 if any file was unreadable**, and prints the count on its
  own line above the class tally. *"0 R1000"* and *"couldn't read anything"* can
  never be the same output.
* **`ReplayDomainError` is deliberately re-raised**, not bucketed: a turn count
  above `MAX_TURNS` means the decoder is wrong, not that the file is damaged, and
  `UNREADABLE` already has a benign explanation available.
* **Every corpus read is by COLUMN NAME**, via `_need()`, which raises on a
  zero-row surface *and* on a missing column. (`era_guard` returned an empty list
  for `throws.tsv` on a surface where a real zero had just been established —
  that shape is why a zero-row read is an ALARM here, not a 0%.)
* **`_tsv()` skips `#` lines** — leading `# FIXTURE` and mid-file
  `# FIXTURE-RESUME` alike, matching `tools/overnight_read.py:111` and
  `tools/effective_n.py:72` — and the selftest drives that with a fixture carrying
  both.

## 7. RESULT

```
--build : 44,431 replays, 24.0 s, one process
          readable 44,431 · UNREADABLE 0 · R1000 8,610 · DECISIVE 35,821 · ABORTED 0
--validate : compared 3,735 · turns mismatches 0 · wincond mismatches 0 · PASS
```

**Coverage of OUR games goes 41.0% → 100.0% (9,101 of 9,101).** And the number the
row was actually about, previously unmeasurable:

| fixture | n | **R1000 rate** | our wins at r1000 (**defeats under `PROGRAMME`**) | decisive wins |
|---|---|---|---|---|
| **OUR UNRATED** | 5,361 | **6.2%** (332) | **124** | 2,415 |
| OUR RATED (ladder) | 3,740 | **14.6%** (547) | 289 | 1,595 |

⚠ **Read the fixture gap carefully — it is a comparison across two surfaces and
`CLAUDE.md`'s two-fixture form applies** (`DEFF_u/n_u + DEFF_r/n_r`, 1.833/1.529
pooled). It is also **confounded by design**: unrated pools PROTOTYPES and ladder
pools SHIPPED BOTS, against different opponent mixes. **The 8.4pp gap is stated as
a measured difference between two fixtures, not as an effect of anything.**

**The actionable half needs no such care: 124 unrated games we currently bank as
wins are defeats under `R1000_IS_DEFEAT`, and until now nothing could see them.**

## 8. COST AND OPERATION

* **24 s** for the full 44,431-file archive, **single process** (local screens own
  the cores), ~12 GB of reads. ~0.3 ms/file warm.
* Idempotent: `--build` rewrites the whole table via a `.tmp` + atomic `replace()`.
  Re-run it after the keeper adds replays; there is no incremental mode and at 24 s
  there does not need to be one.
* Writes only `corpus/wincond.tsv`, a NEW filename the keeper daemon never opens.
  Everything else in `corpus/` was read-only during this work.

## 9. FOLLOW-UPS NOT DONE HERE (deliberately out of scope)

1. **Join `wincond.tsv` into `panel_read.py` / `overnight_read.py`** so unrated leg
   reads report kill-vs-tiebreak natively. That edits lane-owned readers and is the
   lane's call.
2. **Have the keeper refresh `wincond.tsv`** after each decode pass.
3. **Rule on `core_destroyed` @ turns=1000** (§4, item 2). 4 games, none ours.
4. **Add `coinflip` to any hardcoded win-condition domain** (§4, item 1).
