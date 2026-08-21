# BUILD REPORT — `bots/_v536trustport` (v536), s52, 2026-08-21

**THE MAPTRUST CHANGESET, RE-SITED ONTO THE 72.57 CHASSIS, WITH THE HOME
PACKAGE LEFT BEHIND.** v534 built MAPTRUST on `bots/_v533home` — i.e. on top of
the v530-v533 home package, which `V529POOL` has since priced at **−6.13pp**
(`docs/coordination.md`, `2026-08-21T02:33:15Z`: v529merge pooled **72.57
[71.38, 73.76]**, vs HOMEPOOL +6.13 excluding 0, and **release bar (2) MET by
`bots/_v529merge`**). This build takes the MAPTRUST diff — and nothing else —
and applies it to `_v529merge`.

**THE LOAD-BEARING CLAIM OF THIS BUILD IS NOT "THE FIX WORKS". v534 established
that. IT IS "THE CODE IS THE SAME CODE, ON A DIFFERENT CHASSIS."** So the first
instrument is a port checker, and every one of v534's verification suites was
then re-run **on the new tree** rather than cited from the old report.

Parent `bots/_v529merge`, md5-frozen at `02:34:38Z` and re-verified byte-
unchanged at `02:42:50Z` (`scratchpad/s52_v536_build/PARENT_FREEZE.md5`). This
build wrote to `bots/_v536trustport`, `docs/research/` and
`scratchpad/s52_v536_build/` only. `bots/_v488beltbreak2` is mode-444 and was
read, never written (§7.4). Wall clock, from `date -u` in the same shell call
each time: context read `02:33:49Z`, tree copy + parent freeze `02:34:38Z`,
patch application `02:35-02:37Z`, unit harness `02:38:13Z`, arms
`02:38:50-02:39:31Z`, local battery `02:40:18-02:41:38Z`, rowdiff + census
`02:41:56-02:42:50Z`, parent re-freeze `02:42:50Z`.

---

## ⛔ TOP LINE — FIVE SENTENCES

1. **EVERY CODE HUNK APPLIED AT IDENTICAL CONTEXT. NOTHING WAS RE-SITED
   EXCEPT PROSE.** `eco.py` and `siege.py`'s added/removed lines are
   **byte-identical to v534's**, and `doctrine.py`'s block is
   **executable-identical** (16 executable lines both sides) with four
   deliberately re-worded comment passages, enumerated in §2.2.
2. **THE MECHANISM, NOT LUCK:** `siege.py` is byte-frozen since v529, and the
   two parents' `eco.py` **first diverge at line 704** while the MAPTRUST hunks
   attach at **122 and 130** — 574 lines above the seam. `doctrine.py`'s hunk is a
   pure EOF append, which has no context to lose. `main.py` and `raid.py` are
   byte-identical to `_v529merge`.
3. **THE FULL v534 SUITE RE-RUN ON THE NEW TREE REPRODUCES v534's NUMBERS
   DIGIT FOR DIGIT:** 15 pool maps **0 regressions in 2,092 stance-cells**, 10
   other catalogued maps **0 in 1,120**, colliding boards **parent adopts 8/8 /
   v536 returns `None` 8/8**, skip-collisions **parent refuses 4/4 / v536 runs
   4/4**, **eider SKIP→RUN**, flag-off **0 differences in 1,958 cells** while
   flag-on differs in 22 (0 real-map `known_map_for` / 2 eider / 20 synthetic).
4. **GAME-LEVEL IDENTITY IS EXACT AND THE DOSE IS PROVEN DELIVERED: 250 local
   NOISE_OFF games, 5 arms.** `par_off` vs `v536_off` **0 of 50 rows differ**,
   `flagoff_off` vs `par_off` **0 of 50**, the byte-identical `par_twin`
   determinism control **0 of 50** — while `mut_off` (one integer changed,
   `FS_V534_MIN_TILES 8 → 100000`) moves **50 of 50**. **0 tracebacks in all
   250 games.**
5. ⚠ **NO CURRENCY CLAIM AND NO CPU CLAIM IS MADE HERE.** The pricing read is
   the builder's; §5.1's cost table counts **engine calls**, not microseconds.

⚠ **WRITTEN DOWN BEFORE IT IS EXPLAINED AWAY (§7):** the doctrine block v534
shipped contains a paragraph describing a **memo that v534 deliberately removed**
— its own `eco.py` header and build report §7.1 say so. It was found by re-siting
and is corrected in v536; **v534 still carries it.** And the stray `mut_off`
win-share observation v534 recorded "because it was observed" **reverses sign on
this chassis** (§7.2).

---

## 1. WHAT THE PORT HAD TO CROSS

The two parents are not close. Measured with `difflib`, first differing line:

| file | `_v529merge` | `_v533home` | first divergence between the parents | MAPTRUST patch context (old numbering) |
|---|---|---|---|---|
| `doctrine.py` | 5,280 lines | 5,701 | **line 5,281** (i.e. only past `_v529merge`'s EOF) | EOF append |
| `eco.py` | 2,419 | 2,939 | **line 704** | **122 and 130** |
| `siege.py` | 6,120 | 6,120 | **none — byte-identical** | 65 and 504 |
| `main.py` | 2,483 | 2,608 | line 91 | *(untouched)* |
| `raid.py` | 1,382 | 1,382 | none | *(untouched)* |

In the finished tree the added code sits at `eco.py:125-213` and `:222-223`,
`siege.py:68-88` and `:527-560`, `doctrine.py:5,281-5,409`.

**THE HAZARD THE BRIEF NAMED WAS REAL AND IT MISSED BY 574 LINES.** `eco.py`
does differ between the parents — by 520 lines — but the home package's
additions are all **downstream** of `known_map_for`. That is why the eco patch
applied at exact context rather than needing hand re-siting, and it is a fact
about *where* the home package edits eco, not a guarantee that any future port
will be so lucky.

---

## 2. THE HUNK-BY-HUNK RE-SITING TABLE

Derived by diffing `_v533home` → `_v534maptrust` (that diff **is** MAPTRUST,
nothing else) and applying it with `patch -F0` (zero fuzz) to the copy of
`_v529merge`.

| # | file | hunk | v534 site | v536 site | applied |
|---|---|---|---|---|---|
| 1 | `eco.py` | `_maptrust_pick` + its header comment (89 lines) | before `known_map_for`, :122 | **:122** | **CLEAN, zero offset, zero fuzz** |
| 2 | `eco.py` | the 2-line guarded call inside `known_map_for` | :130 | **:130** | **CLEAN** |
| 3 | `siege.py` | `_FS_V534_SKIP_GRIDS` + `_fs_v534_skip_grids()` (20 lines) | :65 | **:65** | **CLEAN** (file byte-identical across parents) |
| 4 | `siege.py` | `FS_MAP_SKIP` grid-confirm in `_fs_map_gated` (+34/−1) | :504 | **:504** | **CLEAN** |
| 5 | `doctrine.py` | the `LOKI-V534 "MAPTRUST"` flag/constant block | append after `FS_V532_WEAVE` (:5,699) | **append after `LOKI_FS_V528` (:5,280)** | ⚠ **RE-SITED — see §2.1** |

**4 of 5 hunks applied clean at identical line numbers. 1 was re-sited.**

### 2.1 The one re-sited hunk

`patch` rejected hunk 5 (`No such line 5698 in input file`) because its context
is three v530/v532 lines that do not exist on this chassis. The hunk is a **pure
append with no dependency on that context**: it defines 3 flags, 6 map-code
string constants and one dict, and reads nothing above it. Re-sited by appending
the same block at `_v529merge`'s EOF. **`portcheck.py` is what makes "the same
block" checkable rather than asserted** (§3).

### 2.2 The four prose adaptations, enumerated

The block's own text names its parent and its sibling flag blocks, so shipping
it verbatim would have put **false statements** in the tree. Four passages
changed; **no constant, no flag value and no code line differs from v534**:

| # | v534 text | v536 text | why |
|---|---|---|---|
| a | *(none)* | a 10-line **PORT HEADER** naming `_v529merge`, the home package left behind, and this report | provenance must be in the tree, not only in a doc |
| b | *"Refutations are memoised per (w, h, anchor)… ONLY refutations taken on a building-free tile are stored"* | **"⛔ NOTHING IS MEMOISED"** + the account of why the memo was cut | ⭐ **the v534 text was STALE — §7.1** |
| c | *"same convention as the v524/v530/v532 blocks… reproduces `_v533home` byte-for-byte. `flagoff_ast.py` asserts it."* | *"the v524/v528 blocks… reproduces `_v529merge` byte-for-byte. The v536 flag-off audit asserts it."* | v530/v532 do not exist here; the named asserting instrument does not exist under that name |
| d | `# master.  False == bots/_v533home unchanged` | `# master.  False == bots/_v529merge unchanged` | the flag-off claim must name the actual parent |

Also: `# THE CODES BELOW ARE NOT RETYPED` gained *"and v536 did not retype them
either — they are the v534 block's own bytes, diff-verified"*, keeping the
pointer to `scratchpad/s52_v534_build/gen_doctrine_block.py` as the original
provenance.

---

## 3. INSTRUMENT #1 — `portcheck.py`: THE PORT IS THE SAME CHANGESET

```
changeset(_v533home -> _v534maptrust)  ==  changeset(_v529merge -> _v536trustport)
```

| file | mode | detail | verdict |
|---|---|---|---|
| `main.py` | UNTOUCHED | byte-identical to `_v529merge` | **OK** |
| `raid.py` | UNTOUCHED | byte-identical to `_v529merge` | **OK** |
| `eco.py` | **EXACT** | +91/−0 added-removed lines both sides, byte for byte | **OK** |
| `siege.py` | **EXACT** | +54/−1 both sides, byte for byte | **OK** |
| `doctrine.py` | **CODE-ONLY** | **16 executable added lines both sides** (112 raw v534 / 129 raw v536) | **OK** |

**WHY TWO MODES AND WHY NEITHER STANDS IN FOR THE OTHER.** `eco.py`/`siege.py`
were ported byte-for-byte, so EXACT is the right and strictest test. `doctrine.py`
was deliberately re-worded (§2.2), so it is compared on **executable content
only** — comments and blank lines stripped **with the tokenizer, not a regex**,
because a regex would mangle a `#` inside one of the six base-27 map code
strings and the tokenizer cannot confuse a STRING with a COMMENT. Applying the
CODE-ONLY mode to eco/siege would have silently licensed a comment drift there;
applying EXACT to doctrine would have failed the honest re-wording.

**DRIVEN TO BOTH VERDICTS, PER GUARD** (`--selftest`, tape `OUT_portcheck.txt`):

| mutant | expected | got |
|---|---|---|
| unmutated trees | PASS | **PASS** |
| doctrine **CODE** line mutated (`FS_V534_MIN_TILES 8 → 9`) | FAIL | **FAIL** |
| doctrine **COMMENT** line reworded | PASS *(must be tolerated)* | **PASS** |
| `eco.py` added **CODE** line mutated (`<` → `<=`) | FAIL | **FAIL** |
| `eco.py` added **COMMENT** line reworded | FAIL *(EXACT mode)* | **FAIL** |

⚠ **The comment-rewording mutants are the ones that make this a checker rather
than a hash.** A checker that failed on (3) would forbid the port's honest
re-wording; a checker that passed on (2) or (4) would not be checking anything.

**And the first draft of `code_only()` failed exactly there:** it dropped
comment-ONLY lines but kept trailing comments, so `FS_V534_MAPTRUST = True
# … _v533home unchanged` vs `… _v529merge unchanged` read as an executable
difference. Fixed to cut at the tokenizer's comment start column.

---

## 4. THE v534 SUITE, RE-RUN ON THE NEW TREE

Every table below is this build's own run against `bots/_v536trustport`, not a
quotation from the v534 report. **All figures reproduce v534's exactly.**

### 4.1 F1 — `known_map_for` (`OUT_f1.txt`)

| population | cells | min tiles verified | **regressions** | pre-existing wrong picks |
|---|---|---|---|---|
| **15 current-pool maps** | **2,092** | 22 | **0** | 2 |
| 10 other catalogued maps | **1,120** | 22 | **0** | 0 |

`FS_V534_MIN_TILES = 8` never binds — the sparsest legal stance on any of the 25
boards still verified **22** tiles. The **2 pre-existing wrong picks are not
charged to this build**: on yulerune from stance (0,9) at builder vision the
visible window does not separate yulerune from frostgate (shared
`(20,20,(2,9),(16,9))`) and **both trees pick frostgate**. F1 cannot fix that —
both candidates verify.

**Positive control — colliding boards** (real terrain cropped from a *different*
real map, relabelled with a catalogued signature's dims and anchors, both core
footprints cleared):

| fixture | parent adopts | parent's grid correct | **v536 → `None`** |
|---|---|---|---|
| SINGLETON (20,26) nordkap sig, valkyrie terrain | 2/2 | 0/2 | **2/2** |
| SINGLETON (16,16) lighthouse sig, valkyrie terrain | 2/2 | 0/2 | **2/2** |
| PAIR (30,30) midgard/ragnarok sig, glacierkeep terrain | 2/2 | 0/2 | **2/2** |
| PAIR (26,26) snowflake/archi sig, drakkarfjord terrain | 2/2 | 0/2 | **2/2** |

The middle column is the fixture's own control: had the parent's adopted grid
*matched* the board, the fixture would not be a collision at all.

**Three guards, each driven the other way:**

| guard | parent | v536 |
|---|---|---|
| mismatch on a **building-free** tile | — | **refutes → `None`** |
| same tile, **building on it** | — | **does not refute → grid kept** |
| degenerate ask (`vision_sq = 0`) | adopts a grid | **`None`** |
| `ct = None` | adopts a grid | **`None`** |

**Residual, measured** (nordkap, single flipped tile vs d² from the core anchor,
core vision r²=36):

| d² | 1 | 4 | 9 | 16 | 25 | 36 | **49** | **64** |
|---|---|---|---|---|---|---|---|---|
| caught | 4/4 | 4/4 | 4/4 | 4/4 | 12/12 | 4/4 | **0/3** | **0/3** |

**100% inside the vision window, 0% outside it.** This narrows the hazard; it
does not close it.

### 4.2 F2 — `FS_MAP_SKIP` (`OUT_f2.txt`)

| case | parent | v536 |
|---|---|---|
| **invariant**: every `FS_MAP_SKIP` signature has registered grids | — | 5 sigs, 5 registered, 0 unregistered, 0 orphan |
| lighthouse / saga / moonrise / heart / snowflake / archipelago, both seats | `False` 12/12 | **`False` 12/12** |
| drakkarfjord / glacierkeep / nordkap / royale | `True` 4/4 | **`True` 4/4** |
| **colliding** boards on 4 skip signatures | **`False` 4/4** *(the exposure)* | **`True` 4/4** |
| archipelago with `self.map_grid` pre-set (the no-`ct` path) | — | `False` |
| ⭐ **eider, both seats** | **`False` (stood down)** | **`True` (runs)** |

The **eider flip is carried forward unchanged and stays declared**: eider shares
heart's `(28,20,(7,9),(19,9))` signature exactly, while
`docs/research/BELT-ON-SEATS-SURVEY-2026-08-17.md` classifies it *Marginal*
(5.7-8.8), not *SKIP*. **It is free on the current pool** — eider is not among
the live 15, and archipelago is the only `FS_MAP_SKIP` map that is, with its
shared entry registering **both** snowflake's and archipelago's grids so that
deliberate shared treatment is preserved exactly.

### 4.3 Exposure census + engine-call cost (`OUT_census.txt`)

**78 catalogued `(w,h,anchor)` keys, 70 of them SINGLETONS** — the surface F1
covers. Of the 9 authored `maps/invented/*` boards, **0** collide. ⚠ **A floor,
not a rate.**

| case | `get_tile_env` | `get_tile_building_id` | verdict |
|---|---|---|---|
| VERIFY nordkap, core r²=36 | 113 | 0 | grid |
| VERIFY nordkap, builder r²=20 | 69 | 0 | grid |
| VERIFY midgard, core | 63 | 1 | grid |
| VERIFY archipelago, core | 111 | 1 | grid |
| **REJECT** (30,30) midgard sig / glacierkeep terrain | **1** | 1 | `None` |
| **REJECT** (26,26) snowflake sig / drakkarfjord terrain | **5** | 2 | `None` |
| **REJECT** (20,26) nordkap sig / valkyrie terrain | **13** | 1 | `None` |

⛔ **ENGINE CALLS, NOT MICROSECONDS. No CPU or TLE claim is made** (§8.2).

---

## 5. FLAG-OFF IS `_v529merge` — FOUR WAYS

`OUT_flagoff.txt`, plus §6's game arm.

1. **BYTES.** `raid.py` and `main.py` md5-identical to `_v529merge`
   (`3b3a0456…`, `93a85f57…`).
2. **AST.** **0** module-level defaults anywhere in the tree derive from a v534
   flag (the v515 finding-3 hazard, which would make an arm override silently
   not reach the code). **The scanner is driven both ways on a synthetic
   module: offender → 1 hit, cleaned → 0.** The 6 hits in the data-constant
   class (`FS_V534_SKIP_CODES` reading the six code strings at `doctrine.py`
   :5,403) are the **v524 precedent**, reclassified rather than suppressed.
3. **READ SITES.** All 4 flag reads — `eco.py:207,222`, `siege.py:547,552` —
   are inside function bodies.
4. **BEHAVIOUR** (`FS_V534_MAPTRUST = False` applied **at the definition site**
   by `mkarm.sh`, never appended):

| sweep | real maps (`known_map_for`) | real maps (gate) | synthetic collisions | total |
|---|---|---|---|---|
| parent vs **FLAG-OFF** | 0 | 0 | 0 | **0 / 1,958** |
| parent vs **FLAG-ON** | **0** | 2 *(= eider, both seats)* | 20 | 22 / 1,958 |

**The breakdown is the point, not the total** — a single "22 differences" number
cannot tell a fix from a regression.

---

## 6. GAME-LEVEL: 250 NOISE_OFF IDENTITY GAMES

`tools/remote_battery.py --hosts local --par 4 --block-size 1`, run
`02:40:18-02:41:38Z` (80 s). **Every bot in the fixture is NOISE_OFF, including
the opponent** — `opp_off` = `bots/_v488beltbreak2` with `NOISE_ON = False`.
Maps `archipelago, midgard, nordkap, yulerune, drakkarfjord`, seeds 1-5, both
seats = **50 cells per arm, 5 arms, 250 games**.

| arm | what it is |
|---|---|
| `par_off` | `_v529merge`, NOISE_OFF |
| `par_twin` | a **byte-identical copy** of `par_off` — the fixture's own determinism control |
| `v536_off` | `_v536trustport`, NOISE_OFF, **flag ON** |
| `flagoff_off` | `_v536trustport`, NOISE_OFF, **`FS_V534_MAPTRUST = False`** |
| `mut_off` | `v536_off` with **one integer changed**: `FS_V534_MIN_TILES 8 → 100000` |

Compared on every column except `tag`, `arm` and `winner`. ⛔ **`winner` is
excluded because it carries the winning bot's DIRECTORY NAME**, so it reads
`par_off` in one arm and `v536_off` in the other for the identical outcome;
`ours` (US/OPP/NONE) carries the same outcome team-neutrally and **is** compared,
as are `cond`, `turn`, `tracebacks`, `ours_mined`, `opp_mined`.

| pair | shared cells | **rows differing** |
|---|---|---|
| `par_off` vs **`par_twin`** *(determinism control)* | 50 | **0** |
| `par_off` vs **`v536_off`** | 50 | **0** |
| `par_off` vs **`flagoff_off`** | 50 | **0** |
| `par_twin` vs `v536_off` / `flagoff_off` vs `v536_off` | 50 | **0** |
| **`mut_off`** vs each of the other four | 50 | **50** |

**`mut_off` IS THE DOSE-DELIVERED PROOF.** It differs from `v536_off` in one
integer on one line, a constant read **only** inside `_maptrust_pick`, which
forces `known_map_for` to return `None` on every board. It moves **50 of 50
rows**. A flag that never executed in-game could not do that, so the 0/50 above
is the fix running and agreeing, not the fix being absent.

**Tracebacks: 0 in all 250 games**, all five arms.

**The comparator is driven the other way** (`rowdiff.py --selftest`): it corrupts
a pair that currently reads **0** — here `flagoff_off` vs `par_off` — and both
mutants (`turn +1`, `ours` flipped) move exactly **1** row.

⚠ **NOT A CURRENCY READ — AND SEE §7.2 BEFORE QUOTING ANY OF IT.** For the
record only: `par_off`/`par_twin`/`v536_off`/`flagoff_off` each won **35 of 50**
with 5 r1000 games; `mut_off` won **25 of 50** with 0. n=50, one opponent, one
NOISE_OFF fixture that is not the shipped configuration, 5 maps, no DEFF, no
pre-registration.

---

## 7. ⚠ SURPRISES — WRITTEN DOWN BEFORE THEY ARE EXPLAINED AWAY

### 7.1 v534's doctrine block documents a memo v534 deliberately deleted

The `F1 — THE FIX` paragraph in `bots/_v534maptrust/doctrine.py` reads
*"Refutations are memoised per (w, h, anchor) … ONLY refutations taken on a
building-free tile are stored"*. **There is no memo.** `_maptrust_pick` has
none, `bots/_v534maptrust/eco.py`'s own header opens with **"⛔ THERE IS
DELIBERATELY NO MEMO HERE, AND THE FIRST DRAFT OF THIS FIX HAD ONE"**, and the
v534 build report §7.1 gives the full account of why it was cut (the key
`(w, h, anchor)` is precisely the thing that does not identify a map — a cache on
it reintroduces the collision bug inside the collision fix). **The doctrine
paragraph is the one place in v534 that was never updated to match the shipped
code**, and it is the paragraph a future reader is most likely to trust, because
it sits beside the flag it describes.

Corrected in v536 (§2.2b). **Not explained:** whether this was an editing miss or
a deliberate ordering the v534 build ran out of clock on. `bots/_v534maptrust`
still carries the stale text; **fixing it there is out of this build's scope and
is listed in §8.4.** This is the same failure class the always-loaded CLAUDE.md
names — *a fact recorded in one place and contradicted in another is a fact
nobody has* — arriving inside a single tree.

### 7.2 The stray `mut_off` win-share observation reverses on this chassis

v534's §6 recorded, disclaimed but recorded, that `mut_off` — the always-live-
sensing posture — won **30 of 50** against the parent's **25 of 50**. On the
v529 chassis, same fixture design, same opponent, same maps and seeds, it is
**25 of 50 against 35 of 50** — the opposite sign, and a larger gap. **Neither
number is a currency read and neither should be quoted as one.** The point is
narrower and it is about method: a number recorded "because it was observed"
inherited a chassis, and swapping the chassis flipped it. **Expected the two to
at least agree in direction; they did not.** No explanation is offered and none
is needed for this build's claims, all of which are identity claims.

### 7.3 The port needed no code re-siting at all, and that was not the prior

The brief flagged `eco.py` as the hazard — correctly, the two parents' eco files
differ by 520 lines — and every eco anchor was re-read before patching. **The
patch then applied at zero offset and zero fuzz**, because the home package's
eco additions begin at line 704 and `known_map_for` lives at 122-219. The
re-siting that *was* required turned out to be entirely in `doctrine.py`, the
file the brief did not flag, and entirely prose. **The check earned its keep
anyway** — without it, "the diff applied" would have been the whole claim, and
`portcheck.py` is what turns that into a checkable statement.

### 7.4 `bots/_v488beltbreak2` is mode-444 and it broke `mkarm.sh`

The frozen opponent fixture ships read-only (`-r--r--r--`, and its `__pycache__`
likewise). `mkarm.sh` does `cp -R` then `rm -rf $DEST/__pycache__`, which fails
with `Permission denied` under `set -e` — **so the script exits before applying
the flag substitution and leaves an arm that silently still reads
`NOISE_ON = True`.** Caught by printing every arm's flag values rather than
trusting the script's exit (**exit code is not a health signal**, and here the
health signal is the flag line itself). Worked around in-build with an explicit
`chmod -R u+w` after the copy. **No `tools/*` edit was made** (brief constraint);
filed in §8.4.

---

## 8. FAILURE REEL + MANIFEST

### 8.1 FAILURE REEL — ⛔ THERE IS NONE, AND HERE IS WHY

**No replay in this build exists to be reeled.** `tools/remote_battery.py` runs
every game with `--replay /dev/null` — including under `--hosts local`, verified
in `ps` on the live driver — so the house convention (earliest our-core-death per
map, capped at 5) cannot be applied. It is recorded as **not executed**, not as
"no deaths".

**And it would carry nothing if it existed.** The 50 cells for `v536_off` and for
`flagoff_off` are **row-identical to the parent's**: any death in those arms is
`_v529merge`'s death, at the same turn, in the same game. The informative arm is
`mut_off`, and what it demonstrates is a *constant* being read, not a tactical
failure.

**Exact re-run recipe for anyone who wants the replays:**
```
.venv/bin/fcode run scratchpad/s52_v536_build/arms/v536_off \
    scratchpad/s52_v536_build/arms/opp_off maps/archipelago.map26 \
    --seed 1 --tle 10 --replay <path>
```
(swap the two bot arguments for a seat-B cell; `par_off` / `par_twin` /
`flagoff_off` / `mut_off` for the other arms; seeds 1-5; maps archipelago,
midgard, nordkap, yulerune, drakkarfjord). ⚠ Reproducible **only** with every
bot in the fixture NOISE_OFF — the v534 lesson (its first battery was void
because the opponent was left noisy).

### 8.2 MANIFEST — the instruments

All under `scratchpad/s52_v536_build/` (not committed, per the v534 precedent).
Every instrument has a `--help`; every selftest is driven to **both** verdicts.

| instrument | what it establishes | tape | selftest drives the other way |
|---|---|---|---|
| **`portcheck.py`** *(new for v536)* | §3, changeset(v533→v534) == changeset(v529→v536) | `OUT_portcheck.txt` | code mutation → FAIL; comment rewording → PASS in CODE-ONLY mode and FAIL in EXACT mode; unmutated → PASS |
| `harness.py` | the fake Controller reproduces real terrain, **can lie**, and raises off-map like the engine | `OUT_harness.txt` | corrupted fixture reads WALL; `(-1,0)` raises; parent has no `FS_V534_MAPTRUST`, child has it True |
| `test_f1.py` | §4.1, 3,212 real-map cells + 8 colliding cells + 4 guards + the residual cut | `OUT_f1.txt` | parent adopts / v536 rejects on every collision; parent adopts / v536 refuses on both degenerate guards |
| `test_f2.py` | §4.2, 12 skip cells + 8 non-skip + 8 colliding + eider + the pre-set-grid path | `OUT_f2.txt` | parent refuses / v536 runs on all 4 collisions |
| `test_flagoff.py` | §5, md5 + AST + read-sites + 1,958-cell behavioural sweep | `OUT_flagoff.txt` | synthetic module-level offender → 1 hit, cleaned → 0; flag-on differs in 22 while flag-off differs in 0 |
| `census.py` | §4.3 exposure census + engine-call cost | `OUT_census.txt` | — *(descriptive; no verdict to invert)* |
| `rowdiff.py` | §6 row identity across arms | `OUT_rowdiff.txt` | corrupts a **0-difference** pair; both mutants move exactly 1 row |

Supporting artifacts: `PARENT_FREEZE.md5` (frozen `02:34:38Z`, re-verified
`02:42:50Z`), `DIFF_{doctrine,eco,siege}.py.txt` (the v534 changeset as
extracted), `doctrine_v534_block.py` / `doctrine_v536_block.py` (the appended
block before and after the four prose adaptations), `mkarm.sh`, `arms/`,
`grid/` (5 per-arm tapes + `ALL.tsv`), `grid.log`, `PIDS`.

**Fixture provenance:** the colliding boards are **not synthetic noise** — each
is real terrain cropped from a *different* real pool map and relabelled with a
catalogued signature's dims and core anchors, with both core footprints cleared
(`crop_from()` in `test_f1.py`). **No `.map26` files were authored.**

### 8.3 The battery

| tape | when (`date -u`) | arms | opponent | cells/arm | status |
|---|---|---|---|---|---|
| **`grid/`** | **02:40:18-02:41:38Z** | 5 (`par_off`, `par_twin`, `v536_off`, `flagoff_off`, `mut_off`) | `arms/opp_off` **(NOISE_OFF)** | **50** | **LIVE — §6** |

`--hosts local --par 4 --block-size 1`, 250 games in 80 s, driver cleaned after
the run. **ws1 was not used** (it returns ~04:00Z and this ran at 02:40Z); ws2
was not needed. Map choice, as a rule rather than a taste: archipelago is the
only `FS_MAP_SKIP` map in the live pool (F2's only on-pool surface); midgard and
yulerune are the two collision pairs that also feed the v524 cripple gate;
nordkap is a plain singleton; drakkarfjord touches neither mechanism.

### 8.4 WHAT THIS BUILD DID **NOT** DO — deferred

1. ⛔ **ANY CURRENCY READ.** Deliberate, per brief. §6's 35/35/35/35/25 split is
   an artefact of an identity fixture and is explicitly disclaimed. **The
   pricing read is the builder's** — and the honest statement of what this build
   can and cannot support is in §9.
2. ⛔ **ANY CPU / TLE MEASUREMENT.** §4.3 counts engine calls. The added
   first-turn cost on a *verifying* board (up to 113 `get_tile_env` on the core,
   ~69 on a builder) has not been measured against the 10 ms budget. Unchanged
   from v534 and inherited by v536 without new evidence.
3. ⛔ **A GAME-LEVEL DEMO ON A COLLIDING MAP.** `tools/remote_battery.py` ships
   maps by name from `maps/` and refuses if the map is not present there, so a
   custom colliding board would have to be committed into the repo's shared
   `maps/`. Not done. The mechanism is established at unit level (§4.1, §4.2).
4. ⛔ **AN ENGINE PROBE OF `get_tile_env` UNDER A BUILDING.** The building guard
   exists precisely because this is assumed, not verified. A 3-line probe bot
   would settle it.
5. ⛔ **FIXING THE STALE PARAGRAPH IN `bots/_v534maptrust`** (§7.1). v536 is
   correct; v534 still is not. A one-paragraph edit to a banked tree is a
   separate decision.
6. ⛔ **FIXING `mkarm.sh` FOR READ-ONLY SOURCE TREES** (§7.4). `tools/*` edits
   were out of scope for this build; the fix is a `chmod -R u+w "$DEST"` after
   the `cp -R`.
7. ⛔ **THE GENERALISATION BATTERY** the map-hardcoding audit's F3 asks for
   (head vs incumbent on the 9 rotated-out era-1 maps + `maps/invented/`).
   Still the number that would price the overfit.

---

## 9. HONEST LIMITS

* **This build measured IDENTITY, not VALUE.** Everything in §4-§6 says the
  ported code is the same code and behaves like the parent everywhere the
  current pool can reach. **Whether `_v536trustport` prices at or above
  `_v529merge`'s 72.57 is a question only a powered full-pool read can answer,
  and it is the builder's.** The insurance argument — MAPTRUST costs nothing on
  boards we know and saves us on boards we do not — is *supported* by 0/2,092
  and 0/50, and is *not established* by them, because no unseen finals board was
  in either fixture.
* **Verification is partial by construction.** A colliding board that also
  agrees with the catalogue across the whole visible window is still adopted.
  Measured boundary: 100% caught inside r²=36, 0% outside (§4.1).
* **F1 cannot disambiguate an indistinguishable pair.** The yulerune/frostgate
  cell picks the wrong member from one stance under **both** trees. Pre-existing,
  unchanged, out of this fix's reach.
* **The census is a floor, not a rate** — it counts how many boards *we happen
  to hold* collide, not how likely an unannounced finals board is to (§4.3).
* **The unit harness is a fake Controller.** It makes no claim about play, tempo
  or outcome — only about which grid a lookup returns for given visible terrain.
* **n = 50 cells per arm on 5 maps against 1 opponent** in §6. That is an
  identity check, which needs to be exact, not powered — **not** a performance
  sample, and no interval is quoted for it. The 5 games of a cell block are not
  independent in the platform sense either; **no DEFF is applied because no
  inferential claim is made**.
* **eider's flip is a judgement, not a measurement**, inherited from v534. It
  follows the closure survey's own classification; if the builder disagrees, the
  remedy is eider's **own** entry with eider's **own** grid — never a signature
  standing in for two maps.
* **`portcheck.py` proves the changeset is the same; it cannot prove the
  changeset is CORRECT on this chassis.** That is what §4's re-run on the new
  tree is for, and §4 is bounded by the maps we hold.
