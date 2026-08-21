# BUILD REPORT — `bots/_v542wave` (THE CONVERSION-WAVE MERGE), s52, 2026-08-21

**The three-way UNION of `bots/_v538refine`, `bots/_v539resilience` and
`bots/_v541quiet`, all three forked from `bots/_v537socket`.** No new mechanism,
no new flag, no new constant, **no value changed** — every flag in the merged
tree carries its sibling's shipped value, verified by reading all 32 of them
side by side (§5).

**This build's only question is COMPOSITION**, and it answers the STRUCTURAL half
of that question, not the value half. **⛔ THE MERGED TREE'S VALUE IS UNMEASURED
AND IS NOT CLAIMED ANYWHERE BELOW.** It gets ONE powered read — the builder's
battery — after this. What is settled here is that each plank's mechanism
survives the union and that turning any one of them off reproduces the merge of
the other two, exactly.

Wall clock from `date -u` in the same shell call: freeze `09:28:17Z`, merge
`09:01:32Z → 09:07Z`, battery 1 `09:11:05Z → 09:18:54Z`, battery 2 `09:27:11Z → 09:45:10Z`.
**2,700 games on ws1, 0 tracebacks, 0 timeouts.** **ZERO local `fcode`
runs** — `scratchpad/overnight/V537POOL.tsv` was mid-fill for the whole build
phase (4,583 rows at boot, target 5,400, `COMPLETE` at `09:23:26Z`) and the
NEWPOOL-BASELINE shard takes the box after it, so every engine game in this
report ran on `work-server-1` via `tools/remote_battery.py`.

---

## ⛔ TOP LINE — FOUR SENTENCES

1. **ONE textual conflict, and it is a position conflict, not a semantic one.**
   All three planks append their constant block at `doctrine.py`'s EOF at the
   identical anchor, so `git merge-file` conflicts on every pair. Resolved by
   `doctrine_union.py` under seven proofs (P1–P7, self-tested both ways) — and
   the resolution is **order-independent in meaning**: all 601 module-level
   bindings of `doctrine.py` are identical under all three append orders, and
   `eco/main/raid/siege` are byte-identical under every order. **The other four
   files merged with zero conflicts.**
2. **All four ablation identities read 0 on BOTH batteries, and none is a
   pass-by-default.** With any one master off the merged tree is row-for-row
   identical to the merge of the other two; with all three off it is row-for-row
   identical to `_v537socket` — **0 of 120 and 0 of 180 rows differ** — and in
   the SAME tape each ablated plank is shown to have moved something
   (24/12/12 cells on `_v488beltbreak2`, 12/6/1 on `_x3r0v168mjolnir`), so the
   zeros are not vacuous. §2.
3. **Each plank's own dose reproduces ON THE MERGED TREE**, measured with that
   plank's own instrument copied from its own build directory: v538's gate binds
   on **midgard alone** over the rotated 15-map pool and the r1–r4 socket claim
   still runs on the other 14; v539 declares famine and rebuilds in **9 of 9**
   harness cells where the parent declares in 0; v541's finisher acts in
   **midgard seat B**, the one cell its own build named. §3.
4. **⭐ THE PLANKS SHARE GROUND ON MIDGARD, AND THE THREE COMPOSITIONS MEASURED
   THERE COME OUT THREE DIFFERENT WAYS.** **v538 × v541** on kill round vs
   `_v488beltbreak2` is **exactly additive** (parent r270; v541 alone −2, v538
   alone −118, together −120). **v538 × v539** on the famine harness's rebuild
   round is **sub-additive by 3** (−7 alone, −16 alone, −20 together against an
   additive prediction of −23). **v538 × v541 vs the baseline opponent is
   degenerate** — v538 carries the whole r375-loss→r629-win flip and v541
   contributes nothing. **v539 × v541 was not measured on either surface and is
   named as deferred, with a structural argument that it is NEGATIVE
   (§4.3).** ⛔ **None of this is a value claim, and no additivity banner is
   raised.**

---

## 1. THE MERGE — THE CONFLICTS, AND WHAT RESOLVED THEM

### 1.1 The common base needed no construction

Unlike v529merge (whose siblings parented on a *configured* `_v526transit` and
needed a `base_arm` built first), all three planks here fork **`bots/_v537socket`
verbatim**. Confirmed by `doctrine_union.py`'s P1 on all three: each child's
`doctrine.py` is EXACTLY `_v537socket`'s bytes followed by a tail — **not one
byte of the shared region is touched by any plank**.

### 1.2 File-by-file editor map — and why a per-file copy would have been wrong

| file | v538 | v539 | v541 | editors |
|---|:--:|:--:|:--:|:--:|
| `doctrine.py` | ✔ | ✔ | ✔ | **3** |
| `eco.py` | ✔ | ✔ | — | 2 |
| `main.py` | ✔ | ✔ | ✔ | **3** |
| `siege.py` | ✔ | ✔ | ✔ | **3** |
| `raid.py` | — | — | ✔ | 1 |

⛔ **v529merge could resolve its merge by TAKING WHOLE FILES** (`eco.py` =
v528's, `main.py`+`siege.py` = v527's) because every file there had at most one
editor. **Three of five files here have three editors each**, so a per-file copy
would silently drop two planks. `mkmerge.sh` therefore does a real three-way
merge per file with `git merge-file` — chosen because it **conflicts loudly**
instead of picking a side. A merge that cannot fail has not been seen to merge.

### 1.3 ⛔ CONFLICT 1 (the only one) — `doctrine.py`, all three planks, EOF

```
MERGE ok        _v542wave/doctrine.py  <- _v538refine
MERGE CONFLICT  _v542wave/doctrine.py  <- _v539resilience
MERGE CONFLICT  _v542wave/doctrine.py  <- _v541quiet
_v542wave/doctrine.py:5497:<<<<<<< merged     ...  :6084:>>>>>>> _v541quiet
```

**WHAT IT IS.** All three planks append at the file's END, at the identical
anchor line. A both-added-at-EOF hunk has no trailing context to order by, so
`git merge-file` cannot resolve it and correctly refuses. **The conflict is
POSITION ONLY** — the three blocks assign 3, 16 and 13 names with zero overlap.

⛔ **AND THE EXIT CODE DID NOT CATCH IT.** The first `mkmerge.sh` run was piped
through `tee`, so `$?` read **0** while the script had exited 2. What caught it
was the artefact assertion — an explicit `grep` for conflict markers in the
produced `.py` files. *(CLAUDE.md: exit code is not a health signal. It was not
one here either.)*

**HOW IT IS RESOLVED — `doctrine_union.py`, seven proofs, not a concatenation:**

```
P1  each side is EXACTLY base ++ tail (no side edits the shared region)
       v538  4,271 bytes /  3 assigns · v539 13,475 / 16 · v541 20,799 / 13
P2  each tail is module-level ASSIGNMENTS ONLY (a def/if/import would make
    ORDER load-bearing and invalidate this whole resolution)
P3  the three tails' names are PAIRWISE DISJOINT
P4  no tail SHADOWS a name already bound in the base
P5  union bytes == base ++ tail538 ++ tail539 ++ tail541
P6  union AST == base ++ tails, statement for statement (599 statements)
P7  every name carries ITS OWN SIDE'S value node (559 base + 32 tail names)
```

⭐ **P7 IS THE ONE THAT MATTERS AND P3 DOES NOT IMPLY IT.** Disjoint names say
no side overwrites another's constant; P7 says the union actually CARRIES each
side's value rather than the base's or a sibling's.

**Selftest — every guard driven to its other verdict** (`OUT_doctrine_union_selftest.txt`):

```
HONEST base+s1+s2                             PASS
P1 side edits a base line          -> FAIL    P1 side shorter than base  -> FAIL
P2 tail carries a def              -> FAIL    P2 tail carries an import  -> FAIL
P3 two tails assign X              -> FAIL    P4 tail shadows base A     -> FAIL
P6 writer drops a statement        -> FAIL    P7 union value != side's   -> FAIL
HONEST again (patches reverted)               PASS      0 wrong verdicts
```

**ORDER-INDEPENDENCE, PROVED RATHER THAN ARGUED** (`OUT_order_independence.txt`).
The union was rebuilt under two other append orders and compared:

```
eco / main / raid / siege     BYTE-IDENTICAL under all three orders
doctrine.py bytes             DIFFER (comment-block layout only)
doctrine.py AST namespace     591 Assign names, 0 differ, under both orders
doctrine.py EXECUTED module   601 bindings, 0 differ, under both orders
CONTROL one constant mutated  1 binding differs   -> the check CAN fail
CONTROL one function mutated  1 binding differs   -> functions really compared
```

⛔ **AND THE CONTROL EARNED ITS KEEP.** The first version of that comparison
reported **3 spurious differences** (`fs_crew_on`, `fs_crew_seat`,
`fs_muster_wait`) — they are FUNCTIONS, and `repr()` of a function carries its
memory address, which differs between imports. The AST pass read 0 at the same
moment. **A naive `repr` compare would have reported a merge defect that does
not exist**; the comparator now compares function SOURCE and both controls fire.

### 1.4 CONFLICT 2 — there isn't one. The other four files merged clean

```
eco.py    <- v538 ok  <- v539 ok                    (v541 does not touch it)
main.py   <- v538 ok  <- v539 ok  <- v541 ok
siege.py  <- v538 ok  <- v539 ok  <- v541 ok
raid.py                           <- v541 ok        (only editor)
```

The hunks are disjoint by REGION even where they share a file:

| file | v538's region | v539's region | v541's region |
|---|---|---|---|
| `main.py` | `__init__` @178 (2 fields) | `__init__` @172 (3 fields) + roster @1343 + release @1431 + crew-seat @1562 | `__init__` @194 (3 fields) |
| `siege.py` | `_fs_gate` @483 → extract `_fs_enemy_anchor`, add `_v535_map_refuses` | `_fs_eco_publish` @215 + the `_v539_*` family @255 | sealer rung 5 @3462, support rung 5 @3541, the `_v541_*` family @4006 |
| `eco.py` | `_v538_claim_on` + `_v537_socket_claim` @610 | `_eco_spendable` @490 + `_sync_harvesters` @815 | — |

**Digest chain** (frozen `09:28:17Z`, `TREE_FINAL.md5`):

```
PARENT  _v537socket       doctrine 64f68421  eco 68732db4  main 8cce089a  raid 3b3a0456  siege 15daf5a0
v538    _v538refine       doctrine d562d0d5  eco 31dbcf5a  main dba8b635  raid 3b3a0456  siege 71b5d177
v539    _v539resilience   doctrine 8dd7507e  eco 486de3aa  main 5c0fadd2  raid 3b3a0456  siege 7596eb5a
v541    _v541quiet        doctrine 39e11bf3  eco 68732db4  main 55af88de  raid e0e74d83  siege 046aee1b
UNION   _v542wave         doctrine 20848e53  eco c954b674  main fe037a69  raid e0e74d83  siege a798cb53
                                   ^^merged   ^^538+539     ^^all three   ^^= v541's    ^^all three
```

`raid.py` is **byte-identical to `_v541quiet`'s** — the expected result when one
plank is a file's only editor, and a check that the merge did not silently
re-derive it.

### 1.5 ⭐ THE MERGE-SPECIFIC STATIC QUESTION NO PLANK BUILD COULD ASK

A plank build proves one family is dominated by one master. A merge has to ask
**whether the three families touch each other at all** — because if plank A's
code reads plank B's flag, "A off" is not an ablation of A and every table in §2
is measuring something other than what it names.

`crossref.py` (self-tested, 10 cases, every scan driven both ways) on
`bots/_v542wave`:

```
POPULATION  71 flag reads · 28 family calls · 2,013 self-attr sites
            v538:  3 flag reads,  1 call   v539: 47 reads, 11 calls   v541: 21 reads, 16 calls
X1 CROSS-FAMILY FLAG READS   (must be empty)  0
X2 CROSS-FAMILY CALLS        (must be empty)  0
X3 SHARED CALL SITES         (enumerated)     0   <- no single function reaches two families
X4 SHARED PER-UNIT STATE     (enumerated)     0   <- no self.<attr> written by one family, read by another
RESULT: PASS
```

⚠ **X3 = 0 AND X4 = 0 DO NOT MEAN "NO INTERACTION"** and this report does not
read them that way. They mean the three planks are wired into three **disjoint
call sites** and share no Python-level state. They interact through the **engine
and the shared parent state** (`self.role`, `SLOT_HARVESTERS`, `FS_ECO_SLOT`, the
bank, the belt) — §4 enumerates those and two of them are measured.

**Presence check** — all ten plank methods appear **exactly once** in the union
and **zero times** in the parent: `_fs_enemy_anchor`, `_v535_map_refuses`,
`_v538_claim_on`, `_v539_famine_bits`, `_v539_famine_state`, `_v539_lifeline`,
`_v541_corefirst`, `_v541_core_attack`, `_v541_idle_ok`, `_v541_finishable`.

**Derived-default AST scan** (`flagoff_ast.py`, v515 finding-3 hazard) over all
five merged files, every inherited flag set v518–v528: **0 hits, RESULT PASS**.
`flagoff_audit.py` (v541's R1/R2/R3, self-tested 10 cases / 3 rules) on the
merged tree: **CLEAN, master `FS_V541_COREPECK`, 12 subordinate flags**.

---

## 2. THE ABLATION-IDENTITY PROOFS — THE CORE DELIVERABLE

**Four claims, and three of them cannot be stated against the parent at all.**
A flag-off arm only shows a plank stands *down*. What a merge needs is that the
union **with one plank live reproduces the merge of the other two, exactly** — so
that any later v542-vs-sibling gap is interaction between live planks and cannot
be a merge defect. (v529merge §2's A3/A4, generalised from two planks to three.)

**THE REFERENCE TREES ARE BUILT, NOT ASSERTED.** Three pairwise unions were
constructed by the same `mkmerge.sh` from the same parent:
`ref_no538 = merge(v539,v541)`, `ref_no539 = merge(v538,v541)`,
`ref_no541 = merge(v538,v539)`.

**FIXTURE.** `tools/remote_battery.py` on ws1. **`NOISE_ON = False` on EVERY tree
in the battery — all nine arms AND the opponent** (v541 §0's rule: a paired
battery in this repo is paired only if every tree has it off on disk; without it
the frozen parent reproduces itself on only 3 of 180 rows). Every arm's flags
were verified by READING THEM off disk (`OUT_flagtable.txt`), never by `$?`.
Rows compared cell-by-cell on `(map, seed, seat)` over every column except `tag`,
`arm` and `winner` (`winner` carries the bot DIRECTORY NAME and differs by name
alone; `ours` carries the same outcome team-neutrally and IS compared).

### 2.1 BATTERY 1 — `_v488beltbreak2`, 5 maps × 12 seeds × 2 seats, 1,080 games

```
                                                      cells   differ  where
--- THE FOUR IDENTITY CLAIMS (each must read 0) ---
v542[LOKI_FS_V538=False]     == merge(v539,v541)        120        0  -
v542[LOKI_FS_V539=False]     == merge(v538,v541)        120        0  -
v542[FS_V541_COREPECK=False] == merge(v538,v539)        120        0  -
v542[ALL THREE OFF]          == _v537socket             120        0  -
--- THE NEGATIVE CONTROLS (each must read > 0) ---
v542 vs v542[LOKI_FS_V538=False]     (v538 acted?)      120       24  midgard/A:12 midgard/B:12
v542 vs v542[LOKI_FS_V539=False]     (v539 acted?)      120       12  valkyrie/B:12
v542 vs v542[FS_V541_COREPECK=False] (v541 acted?)      120       12  midgard/B:12
v542 vs _v537socket                  (merge acted?)     120       36  midgard/A:12 midgard/B:12 valkyrie/B:12

IDENTITIES PASS   CONTROLS PASS   TRACEBACKS 0
```

⭐ **THE CONTROLS ARE NOT DECORATION.** v529merge §2 records an identity arm
passing *by default* because no cell in its sample made the plank fire. `abl.py`
makes that a FAIL condition rather than a memory: every identity row is paired
with the row proving the ablated plank moved something in the **same tape**, and
the verdict is FAIL if any control reads 0. The selftest drives exactly that case
(*"no plank acts → identities PASS but controls FAIL"*).

### 2.2 BATTERY 2 — `_x3r0v168mjolnir` (the current baseline), the FULL rotated 15-map pool

**A SECOND OPPONENT AND EVERY MAP THE LADDER CAN PAIR US ON.** 15 maps × 6 seeds
× 2 seats = 180 cells/arm, 1,620 games.

```
                                                      cells   differ  where
--- THE FOUR IDENTITY CLAIMS (each must read 0) ---
v542[LOKI_FS_V538=False]     == merge(v539,v541)        180        0  -
v542[LOKI_FS_V539=False]     == merge(v538,v541)        180        0  -
v542[FS_V541_COREPECK=False] == merge(v538,v539)        180        0  -
v542[ALL THREE OFF]          == _v537socket             180        0  -
--- THE NEGATIVE CONTROLS (each must read > 0) ---
v542 vs v542[LOKI_FS_V538=False]     (v538 acted?)      180       12  midgard/A:6 midgard/B:6
v542 vs v542[LOKI_FS_V539=False]     (v539 acted?)      180        6  helheim/B:6
v542 vs v542[FS_V541_COREPECK=False] (v541 acted?)      180        1  midgard/B:1
v542 vs _v537socket                  (merge acted?)     180       18  helheim/B:6 midgard/A:6 midgard/B:6

IDENTITIES PASS   CONTROLS PASS   TRACEBACKS 0
```

⭐ **AND THIS BATTERY CONFIRMS §3.1 ON THE ENGINE ACROSS THE WHOLE LIVE POOL.**
`poolbind.py` predicts, from the predicate alone, that v538's gate binds on
**midgard and nothing else** in the rotated 15-map pool. Over all 15 maps and
both seats, the arm that differs by `LOKI_FS_V538` differs on **midgard only —
12 of 12 midgard cells, 0 of 168 elsewhere.** A prediction from a static
predicate, met by 180 engine games.

⚠ **v541's DOSE IS THIN AGAINST THIS OPPONENT — 1 cell of 180**, and that is
consistent with `_v541quiet`'s own report, which read a **zero** finisher dose on
its mjolnir cell (§4.3 row 4 there). It is reported as a thin dose, not as a
null: the identity claim above does not depend on its size, only on its being
nonzero.

### 2.3 The whole pairwise reference structure (battery 1, context)

```
_v537socket vs merge(v539,v541)                   24  midgard/B:12 valkyrie/B:12
_v537socket vs merge(v538,v541)                   24  midgard/A:12 midgard/B:12
_v537socket vs merge(v538,v539)                   36  midgard/A:12 midgard/B:12 valkyrie/B:12
merge(v538,v539) vs v542  (= v541 added last)     12  midgard/B:12
merge(v538,v541) vs v542  (= v539 added last)     12  valkyrie/B:12
merge(v539,v541) vs v542  (= v538 added last)     24  midgard/A:12 midgard/B:12
```

Every row is consistent with the identity table: **adding plank *i* to the merge
of the other two changes exactly the cells plank *i* acts in, and no others** —
v541 → `midgard/B`, v539 → `valkyrie/B`, v538 → `midgard/A` + `midgard/B`.
And the union of the three single-plank cell sets is exactly the 36 cells that
separate `v542` from the parent, with `midgard/B` counted once because **v538
and v541 both act there** (§4.2).

---

## 3. PER-PLANK DOSE REPRODUCTION ON THE MERGED TREE

⛔ **EACH PLANK'S OWN INSTRUMENT, COPIED FROM ITS OWN BUILD DIRECTORY AND
RE-POINTED — NEVER EDITED WHERE IT LIVES.** That is the house convention
(v538's `harness.py` header, verbatim: *"COPIED … (never edited in place) and
re-pointed"*), and it exists so the plank builds' banked outputs stay
reproducible from the files that produced them. `repoint.py` (self-tested, 5
guards both ways) performs the copy as a **mechanical token substitution with
every changed site enumerated and the line count asserted unchanged** — a
hand-edit that also "improves" a probe turns a dose REPRODUCTION into a new
measurement wearing a reproduction's name.

| instrument | source | sites re-pointed |
|---|---|---|
| `p538/harness.py`, `p538/gatemap.py`, `p538/test_flagoff.py`, `p538/test_called.py` | `s52_v538_build/` | `_v538refine` → `_v542wave` (2, 4, 1, 1) |
| `p539/harness.py`, `p539/consumers.py`, `p539/agg.py` | `s52_v539_build/` | `_v539resilience` → `_v542wave` (24, 3, 1) |
| `p541/harness.py`, `p541/flagoff_audit.py` | `s52_v541_build/` | `bots/_v541quiet` → `bots/_v542wave` (1, 2) |
| `p538/pool.py`, `p538/wintab.py`, `p538/rowdiff.py`, `p541/paired.py`, `p541/summarise.py`, `p541/diverge.py` | as above | **copied verbatim** — they take arms on the CLI, so `repoint.py` correctly REFUSED them ("token not found … the copy would be a no-op") |

One further substitution was needed and is enumerated for the same reason:
`parents[2]` → `parents[3]` in four files, because the copies sit one directory
deeper than the originals and `REPO` is derived from `__file__`.

**⭐ ALL THREE RE-POINTED HARNESSES PASS THEIR OWN SELFTESTS AGAINST THE MERGED
TREE** — which is already a per-plank mechanism-preservation result, since each
selftest drives every one of that plank's gates to BOTH verdicts on
`bots/_v542wave` (`OUT_harness_selftests.txt`; v538 8 assertions, v539 11 groups,
v541 41 assertions incl. the harm check's two positive controls).

### 3.1 v538 — the claim gate binds on **midgard alone** over the LIVE pool

`p538/gatemap.py` drives the shipped predicate end-to-end on a real `Player` for
every `maps/*.map26`, both seats — now **88 cells** (44 maps; the pool rotation
added ten). `--selftest` PASS, 8 mutants incl. both geometric floors, a
grid-confirmed skip, a signature-with-wrong-grid, both flag mutants and the
cache-cost check.

```
CELLS 88 | refuse 16 | run 72 | GATED-OFF 16 | SEAT-ASYMMETRIC: none
REFUSING (8): archipelago, heart, inv_tiny8, lighthouse, midgard, moonrise, saga, snowflake
```

**Digit-for-digit identical to `_v538refine`'s own enumeration** — the check that
the merge did not change the verdict.

⛔ **AND THE POOL MOVED UNDER THIS PLANK BETWEEN ITS BUILD AND THIS ONE.**
v538's report intersected its refusal set with the pool as it stood at
`06:0xZ` (its own §3, `tools/overnight_pool26.sh`) and got **{archipelago, midgard}**. The organisers rotated the pool
again the same morning (`tools/overnight.sh`, commit `99b692150`, `08:04Z`) and
**archipelago left the pool**. `poolbind.py` (self-tested, 9 guards both ways,
including the trap of matching the commented-out OLD pool line) reads the pool
from **the line that executes it**:

```
LIVE POOL (tools/overnight.sh): 15 maps
⇒ ON THE LIVE POOL THE GATE BINDS ON 1 MAP: midgard
⇒ THE r1-r4 SOCKET CLAIM STILL RUNS ON 14: auroraveil, bifrost, fimbulwinter,
  glacierkeep, helheim, holmgang, icefloe, jotunheim, longhouse, paths, skald,
  stavkirke, valkyrie, yggdrasil
```

**Confirmed on the ENGINE, not only in the predicate**: battery 1's v538 control
differs from the merge on **midgard and nowhere else** (24 of 24 midgard cells,
0 of 96 elsewhere), and battery 2 puts that over all 15 pool maps (§2.2).

### 3.2 v539 — famine declared and the rebuild bought, 9 of 9 harness cells

`p539/harness.py --endgame`, the plank's own famine fixture (stub engine, wipe
round is the cell key), merged tree vs frozen parent, 3 maps × 3 wipe rounds:

| map | wipe | `famine_rnd` par → v542 | `first_rebuild_rnd` par → v542 | `final_harvesters` par → v542 |
|---|---|---|---|---|
| atoll | 100 | **−1 → 121** | 252 → **132** | 2 → 2 |
| atoll | 140 | **−1 → 161** | 276 → **162** | 2 → 2 |
| atoll | 180 | **−1 → 201** | **−1 (never) → 228** | **0 → 2** |
| glacierkeep | 100 | −1 → 121 | 244 → **132** | 3 → 3 |
| glacierkeep | 140 | −1 → 161 | 268 → **162** | 3 → 3 |
| glacierkeep | 180 | −1 → 201 | 252 → **224** | 3 → 3 |
| midgard | 100 | −1 → 121 | 144 → **124** | 2 → **3** |
| midgard | 140 | −1 → 161 | 180 → **168** | 2 → **3** |
| midgard | 180 | −1 → 201 | 221 → **208** | 1 → **3** |

**Famine declared in 9 of 9 cells at exactly wipe+21; parent declares in 0 of 9.
Rebuild strictly earlier in 9 of 9.** The atoll/180 row is the headline case:
the parent **never rebuilds** and finishes with **0 harvesters**; the merged tree
rebuilds at r228 with 2.

**⚠ AND v539's OWN §6 RISK REPRODUCES IN THE MERGE, so it is reported here
rather than left in its parent report.** `afford_sentinel_rounds` — the count of
rounds the bank could have paid for a sentinel — falls in **8 of 9 cells** and
ties in 1 (midgard 132→70, 116→60, 104→39; glacierkeep 32→23, 32→23, 36→19;
atoll 57→40, 45→28, 41→41). ⚠ **DO NOT READ THAT AS PURE HARM WITHOUT THE
ATTRIBUTION IN §4.2**: on midgard the fall is attributable to **v538**, not
v539, and on two midgard cells the tree also built MORE turrets. The
conservative arm `FS_V539_RESERVE_FLOOR` ships **False**, exactly as
`_v539resilience` shipped it; nothing here re-prices it.

### 3.3 v541 — the finisher acts in midgard seat B, its own build's cell

`p541/harness.py --report` on the merged tree:

```
DOSE (per single call, arrived body, collar closed, 500 bank):
  FS_V541_COREPECK=True  (shipped) fired=True  core_hp=-2 ti=-2 pecks=1
  FS_V541_COREPECK=False (parent)  fired=False core_hp=+0 ti=+0 pecks=0
HARM CHECK (parent's own _fs_walk vs the child's idle gate): 5/5 boards agree,
  both positive controls fire (a board that makes the parent WALK exists, and a
  board that opens the idle gate exists — otherwise "no conflict" is vacuous)
```

**On the engine**, battery 1's v541 control differs from the merge in
**12 cells, all `midgard` seat B** — v541's own report §8 REEL 1 names exactly
that cell (*"the only cell the plank acts in: `midgard`, seat B, vs
`_v488beltbreak2`"*). The finisher's dose is **reproduced on the merged tree in
the cell its own build identified**, and the additive clause `FS_V541_IDLEPECK`
remains **False** (§5).

---

## 4. THE INTERACTION SURFACE — WHERE TWO PLANKS SHARE GROUND

⛔ **THE v531 §6 LESSON IS THAT TWO PLANKS TOUCHING THE SAME GROUND IS WHERE
MERGES BREAK.** §1.5 shows they share no Python-level state; that is necessary
and not sufficient. Four shared surfaces were enumerated by reading both
mechanisms; two are measured, two are bounded and named as unmeasured.

### 4.1 INTERACTION A — v538's claim gate vs v539's famine SENSOR (identified, bounded)

v539's detector is a **delivery drought on the Core's own mouth** — a friendly
conveyor/splitter orthogonally adjacent to our 2×2 footprint (`_fs_eco_mouth`,
v514) — and it arms only after `FS_ECO_BIT_DELIV` latches, i.e. after the first
sighting of a stack on that mouth. **v537's socket claim BUILDS exactly such a
mouth conveyor at r1–r4**, and v538's gate stands that claim down on refusing
boards. **So on midgard the merged tree does not pre-claim the mouth, and the
round at which v539's detector arms is a v538-dependent quantity.**

**BOUNDED, and the bound is why this is not a defect:** `_fs_eco_mouth` accepts
ANY friendly conveyor adjacent to the core and the normal belt terminates there,
so the mouth still appears — later, not never. And **delivery is required for the
economy to exist at all** (CLAUDE.md's own engine probe: a harvester with no
route home collected 0 over 998 rounds), so a tree that never arms the detector
is a tree with no economy to lose. v539 also cannot declare before
`FS_V539_MIN_RND = 60`, four to five rungs after v538's r1–r4 window closes.
**No temporal overlap between the two mechanisms' windows.**

⚠ **UNMEASURED:** the arming-round delay itself. Naming it as deferred rather
than claiming it is small.

### 4.2 ⭐ INTERACTION B — MIDGARD, MEASURED BOTH WAYS, AND IT SPLITS

**ON THE ENGINE it is exactly additive.** `midgard` seat B vs `_v488beltbreak2`,
NOISE_OFF, all 12 seeds returning the identical pair:

| arm | `ours` | kill round | mined (ours/opp) |
|---|---|---|---|
| `_v537socket` (parent) | US | **270** | 2050 / 1600 |
| merge(v539,v541) — **v538 off** | US | **268** | 2030 / 1580 |
| merge(v538,v539) — **v541 off** | US | **152** | 1230 / 550 |
| merge(v538,v541) — v539 off | US | 150 | 1200 / 550 |
| **`_v542wave` (all three)** | US | **150** | 1200 / 550 |

⇒ **v541 alone buys −2 rounds; v538 alone buys −118; together −120. The
composition on this cell is the SUM OF THE PARTS, to the round.** That is the
answer to the question the prompt raised about v541's raid clause meeting the
rest of the merge on the one board where both act, and it is a measurement, not
an argument.

**ON THE HARNESS the same board is NOT additive.** `p539/harness.py --endgame`,
five arms, midgard, wipe r100:

| arm | `famine_rnd` | `first_rebuild_rnd` | `conv_built_pre` | `final_harvesters` | `afford_sentinel_rounds` |
|---|---|---|---|---|---|
| parent | −1 | 144 | 14 | 2 | 132 |
| merge(v539,v541) — v538 off | 121 | **137** | 14 | 2 | 132 |
| merge(v538,v541) — v539 off | −1 | **128** | 16 | 3 | 70 |
| merge(v538,v539) — v541 off | 121 | **124** | 16 | 3 | 70 |
| **`_v542wave`** | 121 | **124** | 16 | 3 | 70 |

⇒ v539 alone buys 144→137 (**−7**). v538 alone buys 144→128 (**−16**). Additivity
would predict 144 − 23 = **121**. **The measured value together is 124 (−20).**
**SUB-ADDITIVE by 3 rounds on the rebuild clock, on the one board where both
planks act** — the two planks are pulling on the same rebuild and partly buy the
same rounds, which is what a shared-ground interaction looks like when it is
benign.

⚠ **AND THE ENGINE ROW AND THE HARNESS ROW ARE NOT IN CONFLICT, BECAUSE THEY ARE
ABOUT DIFFERENT PAIRS.** The engine cell measures **v538 × v541** on kill round
(exactly additive); the harness cell measures **v538 × v539** on rebuild round
(sub-additive by 3). Only one pair of the three has been measured on each
surface, and **v539 × v541 has been measured on neither** — that is §4.3.

On `glacierkeep` — a board v538's gate does not touch — the same table shows v539
carrying the effect **alone** and `merge(v539,v541) == v542` on every column,
which is the control that makes the midgard row readable.

**AND THE SAME MIDGARD BOARD AGAINST THE BASELINE OPPONENT SHOWS THE THIRD
PATTERN — one plank doing all of it.** `midgard` seat B vs `_x3r0v168mjolnir`,
6 of 6 seeds: parent **OPP @ r375**; `merge(v539,v541)` (v538 off) **OPP @ r375**
— v541 does not act on this cell against this opponent; `merge(v538,v541)`,
`merge(v538,v539)` and `_v542wave` all **US @ r629**. **v538 carries the whole
movement and the other two contribute exactly nothing.** A composition that is
additive, one that is sub-additive and one that is degenerate, all on the same
board — which is why this report reports cells rather than a coefficient.

### 4.3 ⭐ INTERACTION C — v539's DRAFT REMOVES BODIES FROM v541's POPULATION (structural, directional, unmeasured)

**This is the one the prompt asked to look for and it is real.** The dispatch in
`main.py` is:

```python
if self.fs_raider and not self.fs_off:  self._fs_turn(ct)   # siege — v541 rung 5
elif self.role == "raid":               self._raid(ct)      # raid  — v541 clause 6.5 / 8
elif self.role == "defend":             self._defend(ct)
else:                                   self._expand(ct)    # ECONOMY — no v541 clause
```

v539's rung B does **two** things to a body during famine: it sets
`self.role = "expand"` at the roster block, and — at the third site the v539
harness found — it sets `take = None` so the body cannot take a ferry-siege crew
seat. **Both branches that carry a v541 clause are therefore closed for every
body v539 drafts.** ⇒ **During a famine episode the merged tree's v541 dose is
strictly ≤ the un-drafted tree's.**

**BOUNDED:** it touches only bodies whose role is assigned **while** famine holds
(never an established raider — the T4_BLEED rule), the draft releases itself the
round delivery resumes, and famine is capped at `FS_V539_MAX_EPISODES = 3` ×
`FS_V539_MAX_RNDS = 120`.

⚠ **UNMEASURED, AND DELIBERATELY NOT ESTIMATED HERE.** Battery 1's v539 cell
(valkyrie/B) and v541 cell (midgard/B) are **disjoint**, so this fixture contains
no game in which both fire — which is exactly why the interaction could not be
priced. It is named as **deferred work with a stated design** (§9), not
hand-waved as small.

### 4.4 INTERACTION D — one bank, three claimants (identified, bounded, unmeasured)

v539's lifeline waives the collar and siege reserves for an EXPANDER's eco spend
during famine (`ti >= cost` only); v541's peck is junior to the whole remaining
collar plus a whole sentinel plus `FS_V541_TI_FLOOR = 8`, **and** to the
ammunition clause. Both draw the one bank. The ordering is safe by construction
in both directions — v541 re-reads the bank every call and simply refuses more
often when it is low; v539's waiver never drops the bank below the item's own
cost. **The s50 belt-lastlink deadlock (two reserves never checked against each
other) cannot recur here because neither claim is a LATCH.** ⚠ Magnitude
unmeasured; `FS_V541_MAX_PECKS = 60` caps one body's lifetime draw at 120 Ti.

### 4.5 ⚠ THE FIXTURE DIAGNOSTIC — AND IT IS **NOT** A VALUE READ

Printed because a reader will compute it anyway, and because leaving it out
would be the flattering choice. `OUT_diag_bb2.txt`, `OUT_diag_mjol.txt`.

| | wins | **kill ≤ r300** | kill ≤ r200 | median kill |
|---|---|---|---|---|
| **bb2** parent / all v538-off arms | 84 | **48** | 36 | 270 |
| **bb2** `v542` / all v538-live arms | 84 | **48** | 48 | **170.5** |
| **mjolnir** parent / all v538-off arms | 102 | **48** | 18 | 289 |
| **mjolnir** `v542` / all v538-live arms | **107** | **48** | 12 | 298 |

⭐ **THE PROGRAMME PRIMARY — timely-kill ≤ r300 — READS 48 IN EVERY ARM ON BOTH
BATTERIES.** No arm regresses it, and no arm improves it. Everything that moves
is BELOW that bar: on `_v488beltbreak2` the merge is faster (kill ≤ r200 36 → 48,
median 270 → 170.5); on `_x3r0v168mjolnir` it is slower (18 → 12, median
289 → 298) while converting five losses into wins.

⛔ **ALL FOUR MOVEMENTS ARE ATTRIBUTABLE TO v538 ALONE** — every arm with
`LOKI_FS_V538` live reads one row and every arm without it reads the other, on
both batteries.

⛔⛔ **AND THIS TABLE CANNOT BE A VERDICT, FOR A REASON THAT IS ARITHMETIC AND
NOT MODESTY.** Battery 1's whole signal lives in **3 `(map, seat)` cells**,
battery 2's in **3**, and inside each cell all 6–12 seeds return ONE unique
outcome (ρ ≈ 1). **Effective n is three cells per battery, not 120 or 180
games.** The direction is also **opponent-dependent and opposite** between the
two. That is exactly the shape v541's own §4.4 flags as void for game-level
p-values, and none is quoted here.

---

## 5. FLAG STATUS — NOTHING WAS RE-PRICED BY THIS BUILD

All 32 plank flags read off `bots/_v542wave/doctrine.py` beside their sibling
trees (`OUT_flagtable.txt`). **Every value matches its sibling's shipped value;
this build changed none of them.**

| family | ON as fired | **shipped OFF, deliberately** |
|---|---|---|
| v538 | `LOKI_FS_V538`, `FS_V538_CLAIM_GATE` | `FS_V538_LOG` |
| v539 | `LOKI_FS_V539`, `FS_V539_REEST`, `FS_V539_DRAFT`, `FS_V539_SEAT3_HOLD`, `FS_V539_LIFELINE` (+ constants 60 / 25 / 40 / 120 / 3) | **`FS_V539_RESERVE_FLOOR`** (v539.1 conservative arm), **`FS_V539_HONEST_SLOT`** (the commission's ratchet reset — the consumer enumeration says it CLOSES the forward-sentinel gate), `FS_V539_LOG` |
| v541 | `FS_V541_COREPECK`, `FS_V541_COREFIRST`, `FS_V541_FINISH_ON` (HP 120), `FS_V541_KEEP_SENT`, `FS_V541_AMMO_AWARE` (min 120), `FS_V541_RAID_ON` (+ TI_FLOOR 8, MAX_PECKS 60) | **`FS_V541_IDLEPECK`** (the additive clause), **`FS_V541_NEED_SENTINEL`**, `FS_V541_LOG` |
| chassis | `NOISE_ON = True`, `LOKI_QUIET_ON = True`, `FS_V537_SOCKET = True` — all unchanged from the parent | |

⛔ **`LOKI_QUIET_ON` STAYS TRUE.** v541 is a target-priority redirect at core
adjacency, not an un-silencing of builder melee; the −10.83 v527 precedent
against wholesale un-silencing is untested here and stands.

---

## 6. SURPRISES — WRITTEN BEFORE THEY WERE EXPLAINED

1. **⭐ v538'S CLAIM GATE MAKES THE TREE BUILD *MORE* CONVEYORS, NOT FEWER.**
   On midgard the harness reads `conv_built_pre` **14 for the parent and 16
   whenever v538 is live**. The gate's whole action is to SUPPRESS two conveyor
   builds at r1–r4. *(Explanation offered afterwards and not measured: the two
   freed builder turns go back into the normal belt/expansion path, which lays
   more than two links by r100. The number is the datum; that sentence is a
   hypothesis.)*
2. **⭐ THE SAME GATE TAKES MIDGARD SEAT A FROM A r365 LOSS TO A r629 LOSS**
   (vs `_v488beltbreak2`). 12 of 12 cells, `ours = OPP` on both sides. **Not a
   win — a loss that arrives 264 rounds later.** Under `R1000_IS_DEFEAT` that is
   worth nothing directly; it is reported because it is the largest single
   movement in that tape and because a reader scanning "midgard: 24 cells
   changed" would otherwise assume they all went our way. Half did (seat B,
   r270→r150 wins) and half did not.
3. **⚠ v539's ONLY ACTING CELL IN BATTERY 1 MAKES OUR LOSS ARRIVE *SOONER*.**
   `valkyrie` seat B: parent loses at r474, every v539-live arm loses at **r373**,
   with opponent mining dropping 3650→2210. 12 of 12 seeds. No win/loss flip
   either way. **Inconvenient, unexplained, and reported.** ⚠ This is ONE
   (map, seat) cell with ρ ≈ 1 inside it — effective n is 1 cell, not 12 games —
   so it is a flag for the builder's battery, not a finding.
   **⭐ AND BATTERY 2 POINTS THE OTHER WAY**, which is why it is a flag and not a
   negative: v539's only acting cell there (`helheim` seat B) moves a loss from
   **r275 to r297** — 22 rounds LATER. Two cells, two opponents, opposite signs.
4. **⛔⛔ v538'S TWO ACTING CELLS AGAINST THE BASELINE OPPONENT MOVE IN OPPOSITE
   DIRECTIONS, AND ONE OF THEM COSTS A FAST KILL.** `_x3r0v168mjolnir`, 6 of 6
   seeds each:
   * `midgard` seat A: **we WIN at r156 without v538 and at r298 WITH it.**
     Still a timely kill — but **142 rounds slower and 2 rounds off the r300
     bar.**
   * `midgard` seat B: **parent LOSES at r375; with v538 we WIN — at r629.**
     A loss→win flip that pays **nothing** on the r300 primary and is a
     `R1000_IS_DEFEAT`-adjacent outcome.
   ⇒ **The v538 plank's engine-side effect is not one-signed**, and the report
   says so rather than quoting only the `_v488beltbreak2` cell where it buys
   −118 rounds. *(v538's own build screened it on a different pool against a
   different mjolnir build; this is not a contradiction of that screen, it is a
   different fixture. Neither is powered.)*
5. **⚠ v541's DOSE COLLAPSES BETWEEN THE TWO FIXTURES — 12 cells of 120 vs
   `_v488beltbreak2`, 1 cell of 180 vs `_x3r0v168mjolnir`.** Not a merge defect
   (the identity claim needs it nonzero, not large) and consistent with
   `_v541quiet`'s own zero-dose mjolnir cell — but it means **the merged tree's
   v541 contribution is close to unobservable against the current baseline
   opponent**, and a builder battery that pairs only against mjolnir will not be
   able to see it at all.
6. **⛔ A NAIVE `repr()` COMPARISON REPORTED THREE MERGE DEFECTS THAT DO NOT
   EXIST.** §1.3. Functions `repr()` with a memory address. The instrument was
   corrected and given a control that mutates a function BODY, so it now really
   compares functions rather than their identities.
7. **⛔ `tee` SWALLOWED THE MERGE SCRIPT'S EXIT CODE 2 AND THE RUN READ AS
   CLEAN.** §1.3. The conflict was caught by the artefact assertion (a `grep`
   for conflict markers), which is the only reason this report has a §1.3 at all.

---

## 7. INSTRUMENTS — ALL SELF-TESTED, EVERY GUARD DRIVEN BOTH WAYS

| instrument | new/copied | guards driven to both verdicts |
|---|---|---|
| `doctrine_union.py` | **new** | 8 mutants + 2 honest passes (P1×2, P2×2, P3, P4, P6, P7); `OUT_doctrine_union_selftest.txt` |
| `crossref.py` | **new** | 9 cases; every scan (X1–X4) fired and stayed silent; incl. "population non-empty so the zeros are not vacuous" |
| `poolbind.py` | **new** | 9 cases incl. the commented-OLD-pool trap, a constant column, and a pool where the gate binds on nothing (must PASS, not error) |
| `abl.py` | **new** | 7 cases; **incl. the pass-by-default case** (no plank acts → identities PASS, controls FAIL) |
| `repoint.py` | **new** | 5 cases; refuses a no-op copy, a surviving stale token, a line-count change |
| `mkmerge.sh` | **new** | artefact-asserted (conflict-marker grep + `ast.parse` per file), not exit-code-gated |
| `p538/gatemap.py` | copied+re-pointed | 8 mutants incl. both flag mutants and the cache-cost check — **PASS on the merged tree** |
| `p538/harness.py`, `p539/harness.py`, `p541/harness.py` | copied+re-pointed | plank selftests, **all PASS on the merged tree** |
| `p538/rowdiff.py` | copied verbatim | selftest corrupts a zero-difference pair (turn +1, `ours` flipped) |
| `p541/flagoff_audit.py` | copied+re-pointed | 10 cases / 3 rules — **CLEAN on the merged tree** |
| `flagoff_ast.py` | copied verbatim | positive control (`FERRY_HOME_ON` reads `FS_CREW_ON`) fires; merged tree reads 0 |

---

## 8. MANIFEST

**Tree:** `bots/_v542wave/`. Changed vs `bots/_v537socket`: all five files.
Frozen: `scratchpad/s52_v542_build/TREE_FINAL.md5` (`09:28:17Z`, 8 trees ×
5 files).

**Reference trees** (`scratchpad/s52_v542_build/ref/`):
`ref_no538 = merge(v539,v541)` · `ref_no539 = merge(v538,v541)` ·
`ref_no541 = merge(v538,v539)` · `order_A`, `order_B` (the two alternative
doctrine append orders, §1.3).

**Arms** (`scratchpad/s52_v542_build/arms/`), every one built by `mkarm.sh`
(in-place at the definition site, never appended) and verified by reading its
flags:

| arm | configuration |
|---|---|
| `parent` | `bots/_v537socket` + `NOISE_ON=False` |
| `v542` | merged tree as fired + `NOISE_ON=False` |
| `v542_538off` / `v542_539off` / `v542_541off` | + one master `False` |
| `v542_alloff` | + all three masters `False` |
| `ref_no538` / `ref_no539` / `ref_no541` | the pairwise unions + `NOISE_ON=False` |
| `opp_bb2` / `opp_mjol` | `_v488beltbreak2` / `_x3r0v168mjolnir` + `NOISE_ON=False` |

**Tapes:**

| dir | fixture | rows |
|---|---|---|
| `ident_bb2/` (+ `ident_bb2_combined.tsv`) | ws1, NOISE_OFF, `_v488beltbreak2`, 5 maps × 12 seeds × 2 seats | 9 × 120 |
| `ident_mjol/` (+ `ident_mjol_combined.tsv`) | ws1, NOISE_OFF, `_x3r0v168mjolnir`, full rotated 15-map pool × 6 seeds × 2 seats | 9 × 180 |

**Outputs:** `OUT_doctrine_union_selftest.txt`, `OUT_repoint_selftest.txt`,
`OUT_crossref_selftest.txt`, `OUT_crossref_v542.txt`, `OUT_poolbind_selftest.txt`,
`OUT_poolbind.txt`, `OUT_abl_selftest.txt`, `OUT_abl_bb2.txt`, `OUT_abl_mjol.txt`,
`OUT_abl_table.txt`, `OUT_rowdiff_bb2.txt`, `OUT_cell_detail.txt`,
`OUT_diag_bb2.txt`, `OUT_diag_mjol.txt`, `OUT_refstruct_bb2.txt`,
`OUT_refstruct_mjol.txt`, `OUT_order_independence.txt`, `OUT_flagtable.txt`,
`OUT_harness_selftests.txt`, `OUT_p538_gatemap.txt`,
`OUT_p538_gatemap_selftest.txt`, `OUT_p539_endgame.tsv`,
`OUT_p539_endgame_attrib.tsv`, `OUT_p539_identity.txt`, `OUT_p541_report.txt`.
**Logs:** `logs/mkmerge_v542.log`, `logs/mkmerge_refs.log`, `logs/arms.log`,
`logs/ident_bb2.log`, `logs/ident_mjol.log`.

---

## 9. REEL / MANIFEST (D16) — WHAT TO WATCH, AND WHAT THERE IS TO WATCH IT WITH

⛔ **THERE ARE NO REPLAYS, AND THAT IS A LIMIT RATHER THAN A STYLE CHOICE.**
This build made **zero local `fcode` runs** (V537POOL was mid-fill for its whole
duration, then NEWPOOL-BASELINE takes the box), and `tools/remote_battery.py`
runs `--replay /dev/null` and returns the run_grid **tape**, not replays.
**So the reel is a deterministic re-run recipe** — worth something only because
the fixture is provably reproducible: every tree in it, arms **and opponent**,
carries `NOISE_ON = False` on disk, and the four identity rows reading exactly
0/120 and 0/180 are themselves the determinism certificate (nine arms, two
opponents, four zero-difference pairs).

### REEL 1 — ⭐ THE CELL WHERE TWO PLANKS MEET: `midgard`, seat B, vs `_v488beltbreak2`

```
.venv/bin/python tools/remote_battery.py \
  --arm parent=scratchpad/s52_v542_build/arms/parent \
  --arm v542=scratchpad/s52_v542_build/arms/v542 \
  --arm ref_no538=scratchpad/s52_v542_build/arms/ref_no538 \
  --arm ref_no541=scratchpad/s52_v542_build/arms/ref_no541 \
  --opp scratchpad/s52_v542_build/arms/opp_bb2 \
  --maps midgard --seeds 1-12 --block-size 3 --par 1 \
  --hosts work-server-1 --out /tmp/reel1
```
**WHAT TO WATCH:** seat B, every seed. `parent` kills at **270**; `ref_no538`
(v538 off) at **268**; `ref_no541` (v541 off) at **152**; `v542` at **150**.
Twelve seeds return one unique quadruple — **effective n is ONE CELL, not 12
games**, and the report says so wherever the number appears.
**WHAT WOULD FALSIFY THE MERGE:** any arm reading a value not in that set, or
`v542 ≠ 150`.

### REEL 2 — THE FOUR IDENTITY CERTIFICATES (both tapes, nine arms each)

```
.venv/bin/python scratchpad/s52_v542_build/abl.py \
    scratchpad/s52_v542_build/ident_bb2_combined.tsv
.venv/bin/python scratchpad/s52_v542_build/abl.py \
    scratchpad/s52_v542_build/ident_mjol_combined.tsv
```
**Expect the four identity rows at 0 on both, and the control rows at
24/12/12/36 (bb2) and 12/6/1/18 (mjolnir).** `abl.py` FAILS if any control reads
0 — that is the pass-by-default guard, and its selftest drives exactly that
case. To rebuild the tapes from scratch, the two `tools/remote_battery.py`
invocations are the last two `LAUNCHED` lines of `logs/ident_bb2.log` and
`logs/ident_mjol.log`, with the nine `--arm` paths listed in §8.

### REEL 2b — ⭐ THE POOL PREDICTION MET BY 180 GAMES

```
.venv/bin/python scratchpad/s52_v542_build/p538/gatemap.py > /tmp/gm.txt
.venv/bin/python scratchpad/s52_v542_build/poolbind.py /tmp/gm.txt
```
prints `BINDS ON 1 MAP: midgard` from the predicate alone. The mjolnir tape's
v538 control then differs on **midgard only, 12 of 12 midgard cells, 0 of 168
elsewhere**, over all fifteen pool maps. **A static prediction and an engine
measurement that agree is the strongest single row in this report.**

### REEL 3 — ⛔ THERE IS NO REEL FOR THE HARNESS TABLES, AND WHY

§3.2 and §4.2's harness rows come from `tools/stub_engine.py`, which has a 1×1
Core, no resource-stack physics and no opponent. **They can say which BRANCH the
real shipped code takes on a scripted board; they cannot say a game was won.**
Re-run with `p539/harness.py --endgame --maps midgard,glacierkeep --wipe-at
100,180 --rounds 400 --arms _v537socket,_v542wave,<the three refs>` — it is
deterministic (NOISE off in `load_tree`) and reproduces the tables verbatim.

---

## 10. HONEST LIMITS, AND WHAT IS DEFERRED

1. **⛔⛔ THE MERGED TREE'S VALUE IS NOT MEASURED IN THIS REPORT AND MUST NOT BE
   READ OUT OF IT.** §2's batteries are ABLATION-IDENTITY fixtures: nine arms
   chosen to prove structure, on two opponents, with the arms' differences
   concentrated in a handful of `(map, seat)` cells. **The composition's worth
   gets ONE powered read — the builder's battery — and this build asserts no
   additivity banner.**
2. **EFFECTIVE n IS CELLS, NOT GAMES.** Battery 1's entire signal lives in three
   `(map, seat)` cells, each returning one unique outcome across all 12 seeds
   (ρ ≈ 1 inside the stratum). Any p-value computed on 120 games from this tape
   would be void, which is why none is quoted.
3. **THE INTERACTION IN §4.3 IS UNPRICED.** v539's draft and v541's clauses never
   co-fired in either battery (disjoint cells). **Deferred design:** a fixture
   that forces a famine on a board where v541's finisher also acts — e.g. a
   midgard cell against a belt-cutting opponent with the wipe scripted — and then
   the v541 dose counter read with `FS_V541_LOG = True` on a LOCAL run (platform
   replays carry `stdout` empty in 30,664 of 30,664 events, so this must be
   local).
4. **§4.1's arming-round delay is unmeasured**, and §4.4's bank contention is
   bounded but unquantified.
5. **`_x3r0v168mjolnir` is the CURRENT baseline** (Magnus's s52 directive,
   commit `99b692150`); `_v488beltbreak2` is the standing screen opponent and is
   the fixture v541's own dose cell was measured on. Neither is the ladder.
6. **THE POOL ROTATED THIS MORNING** and could rotate again. §3.1's
   "binds on midgard alone" is a **measurement of the pool at `09:45Z`**, not a
   property of the gate. `poolbind.py` re-derives it from
   `tools/overnight.sh`'s live `MAPS=(...)` line in one command.
7. **v541's DOSE AGAINST THE CURRENT BASELINE IS 1 CELL IN 180.** The identity
   proof does not depend on its size, but any downstream battery that pairs only
   against `_x3r0v168mjolnir` will be measuring v538 and v539 with v541 along for
   the ride. **Include `_v488beltbreak2` (or another belt-cutting opponent) if the
   v541 contribution is meant to be visible.**
8. **NOT DONE:** an engine-side stderr dose tape (`FS_V538_LOG` / `FS_V539_LOG` /
   `FS_V541_LOG`) for the merged tree. It needs local `fcode` runs with stderr
   kept, and the box was gated for this build's whole duration. v538's own build
   has that tape for its plank (`OUT_logprobe.txt`); the merged tree does not.

---

## BUILDER VERDICT LINES (s52)

* **MERGE: STRUCTURALLY CLEAN.** One conflict (doctrine EOF, three-way,
  position-only), resolved under seven proofs and shown order-independent in
  meaning. Four files merged with zero conflicts. Zero cross-plank flag reads,
  calls or shared state.
* **ABLATION IDENTITY: 4/4 PASS ON BOTH BATTERIES — 0 of 120 and 0 of 180 rows
  differing; controls 24/12/12/36 and 12/6/1/18, none vacuous; 0 tracebacks in
  2,700 games across two opponents and the full rotated 15-map pool.**
* **DOSE: 3/3 planks reproduce their own build's dose on the merged tree**, each
  with that plank's own instrument copied and mechanically re-pointed.
* **INTERACTIONS: 4 enumerated, 2 measured (v538×v541 additive, v538×v539
  sub-additive by 3), 2 named as unpriced — one of them (v539's draft removing
  bodies from v541's dispatch branches) argued STRUCTURALLY NEGATIVE and never
  co-fired in either fixture.**
* **VALUE: UNMEASURED, AND NOT INFERABLE FROM §4.5. Hand to the builder's
  battery — and include a belt-cutting opponent, or v541 is invisible in it.**
