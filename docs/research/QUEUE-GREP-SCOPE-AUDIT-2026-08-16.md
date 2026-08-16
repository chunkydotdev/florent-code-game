# QUEUE `GREP:` SCOPE AUDIT — does a single-file search return a false zero to the admission gate?

**SIDE LANE s47, 2026-08-16T14:01:50Z (`date -u`). Incumbent `bots/_v223sealrepair`.**
**Question named by this lane at the s45 post-wrap (`a8047b75`) and left unrun there. This is the run.**

---

## WHY THIS WAS ASKED

`QUEUE.md`'s admission gate counts a row only if it carries a `GREP:` cell naming **what was checked
in the incumbent and what was found**. Its purpose is to prevent the cheapest null in this repo: a
leg testing a feature we already ship.

**The gate cannot check whether the SEARCH COVERED THE TREE.** On 2026-08-16 a `GREP:` scoped to
`raid.py` alone returned a clean, quotable, **wrong** zero — the answer was in `main.py` — and the
row was admitted on it. **Research self-caught it within the hour and re-priced the row**
(`b43c6f24`, row `#80`); nothing is owed on the instance. **What was never checked is whether it was
an instance or a class.**

## METHOD, AND THE CONTROL THAT MAKES THE ZEROES MEAN ANYTHING

Executed by a read-only `opus` subagent under a fixed method; **the one load-bearing break was
re-verified by hand at the primary before publication** (see §5).

**⭐ THE CONTROL WAS DRIVEN FIRST AND BOTH WAYS.** Row `#80`'s original claim of ZERO bank-triggered
spend:

```
scoped to raid.py alone       →  0 matches           the claim reads TRUE
widened to the four files     →  main.py:264-267     the claim is FALSE
                                 doctrine.py:1197 LOKI_SURPLUS_TI = 260
                                 doctrine.py:1199 LOKI_RICH_TI    = 700
```

**Both verdicts reproduce.** The instrument was additionally driven on tokens with known answers:
`def ` → 17/45/18/**0** (`doctrine.py` is constants and prose — the zero is correct **and
discriminating**), `ZZQXNOTATOKEN` → 0/0/0/0, `EXILE` → 2/0/1/3.

⛔ **AND THE FACT THAT REMOVES EVERY EXCUSE: THE TREE IS FOUR FILES.**
`doctrine.py` 1,686 · `eco.py` 1,242 · `main.py` 871 · `raid.py` 958 — **4,757 lines total.**
**A tree-wide grep costs the same keystroke as a single-file one.**

## ENUMERATION RULE — stated because a count is only as wide as its rule

* **Row** = a `QUEUE.md` table line whose first cell is a queue row number.
* **GREP claim** = any cell on that line containing the literal `GREP:`.
* **Counted** = what `tools/queue_check.py` itself counts as unblocked.

**69 rows carry a `GREP:` cell; `queue_check.py` counts 63.** The 6 uncounted: `#12 #15 #25 #27 #54`
(all carry a `STATUS:` token) and `#26` (cell reads `GREP: TODO BEFORE BUILD`).
**DENOMINATOR = 63**, matching the `SessionStart` hook's own "unblocked items: 63".

## §1 — BUCKETS

| bucket | n | rows |
|---|---:|---|
| **TREE** (anchors in ≥2 files, or scope otherwise shown) | **36** | #2 #7 #8 #10 #13 #14 #16 #20 #22 #23 #24 #28 #33 #36 #38 #39 #40 #45 #47 #48 #52 #53 #59 #60 #62 #64 #66 #67 #70 #71 #72 #73 #76 #77 #78 #80 |
| **SINGLE-FILE** (every anchor in one file) | **16** | #3 #5 #17 #21 #30 #37 #41 #42 #43 #50 #51 #58 #63 #69 #74 #75 |
| **INSTRUMENT-PATH** (greps `tools/`, exempt) | **9** | #19 #34 #35 #44 #55 #56 #61 #65 #68 |
| ⛔ **NO ANCHORS AT ALL** — a bucket the question did not anticipate | **2** | #49 #79 |

**The INSTRUMENT-PATH count of 9 matches `queue_check.py`'s own "9 row(s) grep an instrument path"
exactly** — an independent confirmation of that sub-count, arrived at by a different route.

## §2 — AT RISK

Scope only endangers a **NEGATIVE EXISTENCE** claim. A positive anchor is not at risk: the fact is
where it says it is.

**AT RISK = SINGLE-FILE ∧ negative existence = 11 rows: #5 #17 #30 #37 #41 #43 #51 #58 #63 #69 #74.**
The other five single-file rows make positive or line-scoped claims (`#3 #21 #42 #50 #75`).
**13 were tested — the 11, plus `#49` and `#79`, which show no scope at all and are therefore
strictly worse.**

## §3 — RESULTS

| row | the negative claim | scoped to | verdict | evidence at tree scope |
|---|---|---|---|---|
| **#5** | map-border throw "NOT shipped" | `raid.py` | **HOLDS** | `border` 0 in all four; `edge` 6, all `doctrine.py` prose (*ledger/knowledge/wedged*); picker sorts sites *farthest from OUR core* (`raid.py:926`) |
| **#17** | "zero `border`/`edge` references" | `raid.py` | **HOLDS** | as #5 |
| **#30** | station scorer has no `SENTINEL` branch | `raid.py` | **HOLDS, narrowed** | no SENTINEL branch in the station scan — **but** `main.py:181,386` read an enemy SENTINEL at d²≤64 into `SLOT_UNDER`/`SLOT_THREAT`. **Avoidance absent; threat-blindness not** |
| **#37** | no conveyor planted beside an ENEMY harvester | `doctrine.py` | **HOLDS** | all 3 `build_conveyor` at `eco.py:580,735,952`; ownership required at `eco.py:380`, `eco.py:703` |
| **#41** | "nothing barriers around our own turrets **anywhere in the tree**" | `raid.py` | **HOLDS** | `build_barrier` = 3 sites, all `raid.py` (`:277` seat-seal, `:500` salt-the-corpse, `:558` salt-beside-belt); none turret-keyed |
| **#43** | nothing targets barrier placement to induce pathing exceptions | `raid.py` | **HOLDS; positive half STALE** | negative survives — **but "only via the seat-seal (`raid.py:267-277`)" is now FALSE**: `:500` and `:558` were added after the stamp |
| **#51** | no role selection, victim persistence or denial scoring | `raid.py` | **HOLDS** | `raid.py:912-931` read in full — first enemy builder at d²≤2 in iteration order, sites by distance descending. No role, no store, no score |
| **#58** | "WE HAVE NO FORWARD LAUNCHER" | `main.py` | **HOLDS** | `build_launcher` = `main.py:657-658` only; sited off the caller's own position, called from `_defend` |
| **#63** | no oscillation detector in the shipped tree | `eco.py` | **HOLDS, near-miss** | no builder-nav detector — **but `main.py:791,850,867` `rot_prev_dir` IS an A→B→A guard**, for GUNNER rotation (`doctrine.py:757`). **Pattern present, wrong unit** |
| **#69** | nothing reads enemy builds inside our spawn ring | `eco.py` | **HOLDS, loose** | no census or contest — **but `eco.py:267-272` `_free_seats` reads seat state team-blind and silently drops an occupied seat. Occupancy is READ; never ATTRIBUTED** |
| **#74** | no site conditions melee on the builder's own mobility | `doctrine.py` | **HOLDS** | all 4 `LOKI_QUIET_ON` melee gates (`raid.py:256,334`, `eco.py:1074`, `main.py:517`) test the flag alone |
| **#49** | no code reads enemy barriers on ore; no path targets one | *(none)* | **HOLDS, material omission** | `ORE_TITANIUM` 6 in `eco.py`, 0 elsewhere — **but `main.py:740` ranks `EntityType.BARRIER: 7` in the live turret attack path (`main.py:725-745`). Our turrets already shoot enemy barriers, last priority.** The cell offers "a turret" as the unbuilt remedy; it is partly shipped |
| **#79** | "NOTHING LIKE IT IS SHIPPED, **IN EITHER DIRECTION**" | *(none)* | ⛔ **BROKEN** | §5 |

**Bonus, and it strengthens rather than breaks:** `#77`'s one `raid.py`-scoped sub-claim
(`plant_count`/`sentban`) widened to all four files is **still 0/0/0/0.**

## §4 — THE ANSWER TO THE QUESTION AS ASKED

⭐ **NEITHER "INSTANCE" NOR "CLASS" CLEANLY, AND THE MIDDLE ANSWER IS THE USEFUL ONE.**

* **The scope habit is a CLASS: 16 of 54 non-instrument rows (30%) carry all their anchors in one
  file.** The exposure `#80` hit is structural, not a one-off lapse.
* **But widening almost never changed the answer: 12 of 13 tested negatives HOLD at tree scope.** The
  single break was **not** a single-file row — it was a **no-anchor** row.
* ⭐⭐ **THE REAL SIGNAL IS IN THE NEAR-MISSES, AND IT IS A DIFFERENT COST THAN THE ONE I EXPECTED.**
  Four rows survive the **letter** of their claim while a tree-wide read finds a materially relevant
  fact the cell omits — **#30** (sentinel threat handling exists in `main.py`), **#49** (turrets
  already shoot barriers), **#63** (an oscillation guard exists, on gunners), **#69** (seat occupancy
  is read, never attributed). **None makes its row a duplicate leg. All four change what the builder
  should write.**

⇒ **`#80` is closer to an INSTANCE than a class for the "already shipped" false null. The scope habit
that produced it is a CLASS, and its usual cost is not a false zero — it is a builder starting from a
cell that names the wrong nearest neighbour in the tree.**

## §5 — THE BROKEN ROW, `#79`, RE-VERIFIED BY HAND

The cell claims: *"NOTHING LIKE IT IS SHIPPED, **IN EITHER DIRECTION**. `infiltrat` /
`plant-and-guard` / `saboteur`: 0 occurrences in QUEUE.md and no analogue in the tree."*

**✅ THE FIRST HALF IS TRUE and I checked it before writing anything against the row.** All 11
occurrences of those three terms in `QUEUE.md` are on **line 565 — row #79's own cell.** No other row
uses them.

**⛔ THE SECOND HALF IS FALSE, on two counts, verified at the primary with a control:**

```
grep -nic saboteur bots/_v223sealrepair/*.py
    doctrine.py:2   eco.py:0   raid.py:0   main.py:0
    doctrine.py:109  "Melee-before-repair for forward saboteurs ..."
    doctrine.py:118  "# SABOTEUR INTERCEPTION.  Measured in the post-heal-reflex rematch ..."
CONTROL  grep -nic ZZQXNOTATOKEN  ->  0/0/0/0
```

1. **`saboteur` is not absent** — and `doctrine.py:118` is a **section header** documenting a
   measured incident (*"a single enemy builder walked our economy from r16 to r150+ … was never once
   contested"*), naming the exact radius gap the row would close, with
   `INTRUDER_CORE_DSQ = 20` at `doctrine.py:126`.
2. **The counter direction IS SHIPPED AND WIRED.** `main.py:457 _nearest_home_intruder` scans
   `get_nearby_units()` for enemy builders near our core; `main.py:476 _home_defend` navigates a
   raider onto it. **Call sites: `main.py:434-436` and `main.py:677`.** *(Control: `def _home_defend`
   = 1 in `main.py`, so the zero-vs-one distinction is discriminating.)*

**WHAT A BUILDER PICKING UP `#79` WOULD BE MISLED INTO BUILDING:** a first-of-its-kind enemy-builder
detector and chase — **when `main.py:457/476` already exist and are live.** The real change is far
smaller: a **radius and role extension** of the shipped path, and `doctrine.py:122` says in writing
that the band beyond `d²≤36` is unowned. **A different and much cheaper plank than the row
advertises.**

**✅ AND THE ROW'S CORE PREMISE SURVIVES — stated because a break is not a kill.** There is no
*our-side* plant-and-guard unit, and the shipped chase **does not kill**: builder melee cannot hit a
builder (not a building), and `LOKI_QUIET_ON` silences `_sabotage_prio` at `main.py:517`. **"Only a
turret can remove it" stands.** The row should be **re-priced, not withdrawn** — and that is the
owning lane's call, not this lane's.

## §6 — TWO STALENESS FINDINGS THIS AUDIT WAS NOT LOOKING FOR

**Scope and staleness are different failures and this cut only targeted the first.** Two surfaced
anyway, and **`queue_check.py` passes the file clean on both**:

* **`#17` names `bots/_v148ferryfirst` — three incumbents back.** Its claim still holds; the
  *pointer* is stale.
* **`#43`'s positive half is now false** — two `build_barrier` sites (`raid.py:500`, `:558`) were
  added after its stamp.

⇒ **A scope-only audit cannot see these, and neither can the gate.** Named, not fixed.

## §7 — LIMITS, STATED SO THE VERDICTS CAN BE OVERTURNED

* **Every conversion from prose to a search was a judgement.** *"Nothing TARGETS barrier placement to
  induce pathing exceptions"* is not a grep; it was resolved by reading all three `build_barrier`
  call sites. **A different reading yields a different search and could yield a different verdict.**
* **Not all 4,757 lines were read.** Verdicts rest on exhaustive call-site enumeration for the
  specific API each claim concerns plus targeted reads. **A mechanism implemented without those
  tokens is invisible to this method.**
* **Classification calls that could be overturned:** `#41`, `#63`, `#69` have single-file anchors but
  their prose *asserts* tree scope. By the letter of the method they are TREE; they were filed
  SINGLE-FILE **because an unverified assertion of scope is not evidence of scope** — and all three
  held. `#30`'s negative is function-scoped and arguably not tree-shaped at all. `#75` was judged
  not-at-risk because its negative is line-scoped.
* **`#49` and `#79` broke the taxonomy.** The three buckets assume every cell has anchors; two cells
  have none.
* **One claim deliberately NOT made:** `_intercept` is referenced at `doctrine.py:130` and `:142`
  while `def _intercept` is **0 in all four files** — which looks like `#67`'s dangling
  `_hunt_turret`. **But `:142` explicitly says "the teammate lineage's `_intercept`", i.e. a
  reference to FOREIGN code, and `:130` is ambiguous.** ⇒ **Not filed as a dangling reference.** One
  of the two anchors is a legitimate cross-lineage citation and the other cannot be resolved from
  the text.
* **Nothing was written or edited by the audit.** `tools/queue_check.py` was run read-only (it is
  already the `SessionStart` hook) to obtain the enumeration.

---

**⛔ NOT A VERDICT.** This lane types none. Row re-pricing, the `#79` decision and any `queue_check`
change belong to the queue owner (research) and the builder respectively.
