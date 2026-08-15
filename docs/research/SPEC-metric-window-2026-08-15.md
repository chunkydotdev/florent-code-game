# SPEC — `METRIC WINDOW`: the round window a mechanism metric is observed in, asserted against the tree's round gates

**Written 2026-08-15T04:41:37Z (`date -u`), builder subagent. Enforced by
`tools/prereg_check.py` (rows `METRIC_WINDOW_*`). Research owns the vocabulary;
the tool owns the enforcement — same split as `SPEC-prereg-check-2026-08-14.md`.**

**Source of the obligation:** `docs/research/AUDIT-closures-bad-build-vs-bad-idea-2026-08-15.md`
§3, which ROUTED it as *"PROPOSED OBLIGATION 17 — not yet written into the
numbered series"*. **This spec does not admit it to the numbered series either —
that is research's call.** It specifies the token and what the checker does with
it, so the routing has a machine behind it rather than a paragraph.

---

## 1. THE DEFECT

A prereg names its mechanism metric's `file:line`, asserts the intersection with
the treatment diff, and **satisfies OBLIGATION 13 in full** — while observing the
metric in a round window where the mechanism is **gated off by a constant in the
tree, in BOTH arms.**

| row | metric observed at | gate that voids it | verdict |
|---|---|---|---|
| **#60** | `get_scale_percent()` at r50 / r100 / r150 | `LAUNCHER_MIN_RND = 160` (`doctrine.py:1536`) | no launcher exists at any of those rounds, either arm |
| **#67** | living entities at r75 | `HUNT_MIN_RND = 120` (`doctrine.py:416`) | the hunt cannot fire before r120 |
| **#54** | `stuck >= 5` | `main.py:400` resets `stuck` on ANY position change | a 2-cycle is made of SUCCESSFUL moves; the counter never reaches 5 |

**OB13 says nothing about WHEN the metric is observed.** All three pass it.
**An inert metric produces a null that looks like a refutation** — each of those
legs would have failed IDENTICALLY had the idea been good.

---

## 2. WHAT THE CHECK CATCHES — AND WHAT IT DOES NOT

**CAUGHT: #60 and #67.** Both are round windows against round gates and both are
rebuilt as forced-fail selftest cells **against the real shipped v140 tree**
(`bots/_v223sealrepair`), not against a synthetic constant.

⛔ **NOT CAUGHT: #54.** It is **not a round window** — it is **counter
reachability**, which needs a reaching-definitions analysis over a mutable
counter (an increment site and a reset site in different files). Nothing in this
check looks at it, and no wording here should be read as covering it. **Two of
three, and the third is named.** A check that claimed all three and caught two
would be worse than this one.

---

## 3. THE TOKEN

```
METRIC WINDOW: r<a>-r<b>. GATING CONSTANTS: <NAME>=<value> … . MECHANISM CAN OCCUR IN WINDOW: yes/no.
```

* **`METRIC WINDOW:`** accepts `r50-r150`, `r75`, `r50 / r100 / r150`,
  `rounds 120-250`, `r0..r1000`. The window is the **MIN and MAX of every round
  named** — a list of observation points and a range are the same object for this
  test. Rounds outside `0..1000` (`GameConstants.MAX_TURNS`) are ignored.
* **`GATING CONSTANTS:`** zero or more `NAME=value` pairs. A name containing
  `MIN` is a FLOOR gate (mechanism only at `round >= value`); `MAX` is a CEILING.
* **`MECHANISM CAN OCCUR IN WINDOW:`** `yes` / `no`. **`no` is a FAIL** — the same
  consequence OB13 attaches to `INTERSECTION: no`.
* **The one legal refusal** is explicit and reasoned:
  `METRIC WINDOW: N/A — <why this metric is not round-scoped>` (≥12 chars).
  A bare `N/A` FAILs. A placeholder (`TBD`) FAILs.
* **Not applicable at all** when the leg declares `MECHANISM METRIC READS: N/A`
  (a calibration panel, a pinning leg). The trigger is OB13's own N/A-by-shape
  spelling, so the two obligations cannot disagree about whether a document has a
  mechanism.

---

## 4. THE FIVE VERDICTS AND THE DESIGN DECISION BEHIND EACH

| id | fires when | tier |
|---|---|---|
| `METRIC_WINDOW_PRESENT` | no `METRIC WINDOW:` line | **WARN at lock, FAIL under `--fire`** |
| `METRIC_WINDOW_PARSE` | declared but names no round, or a bare `N/A` | FAIL |
| `METRIC_WINDOW_DECLARED_INERT` | the prereg itself declares `CAN OCCUR IN WINDOW: no` | FAIL |
| `METRIC_WINDOW_INERT` | the window lies **entirely** on the closed side of a **binding** gate | FAIL |
| `METRIC_WINDOW_GATE_STALE` | a declared `NAME=value` disagrees with the tree | FAIL |
| `METRIC_WINDOW_NOT_COMPUTED` | window declared, metric file unresolvable, no declared gate | **CANNOT-COMPUTE row + WARN at lock, FAIL under `--fire`** |

**(1) MISSING FIELD = WARN AT LOCK, FAIL UNDER `--fire`.** A new required field
is a cost, and the two failure modes are opposite: FAIL-on-missing retroactively
reds every locked prereg in the repo (including a currently RUNNING screen);
silence makes the obligation decoration. **This is the escalation
`prereg_check.py` already uses for OB13's non-computable diff**, for the same
reason — at lock time a document may legitimately predate the machinery; at FIRE
time the leg is about to spend games and a declaration nobody made is a check
nobody ran. **Measured consequence: 0 of 96 documents change verdict at lock
time; 0 flip OK→FAIL even under `--fire`** (§6).

**(2) GATES COME FROM TWO SOURCES AND THEY ARE NOT THE SAME EVIDENCE.**
* **DECLARED** (`GATING CONSTANTS:`) is the author's arithmetic. Always
  assertable, even with no tree on disk.
* **DISCOVERED** — grepped out of the tree — **is the half that catches #60 and
  #67**, because an author who knew about `LAUNCHER_MIN_RND = 160` would not have
  registered r50/r100/r150. Names matching
  `*_MIN_RND|*_MAX_RND|*_MIN_ROUND|*_MAX_ROUND|*_RND_MIN|…` that are **referenced
  by the metric file** are collected; each value is resolved narrowest-first —
  the metric file itself, then modules it imports from the same directory
  (`from doctrine import *` is how every arm tree binds its constants), then any
  `.py` in that directory.

**(3) DISCOVERED GATES ARE TIERED BY SCOPE, and one tier would be wrong either
way.** A gate referenced **inside the metric's own `def` block** ⇒ **FAIL**. A
gate referenced **elsewhere in the metric file** ⇒ **WARN**. File-scope alone
over-fires (a 2,000-line `eco.py` references four unrelated round gates);
function-scope alone misses a metric read one call deep. **The tiers are named in
the output** so a reader can see which one fired.

**(4) THE RESOLVED PATH IS PRINTED, NOT ONLY USED.** A gate value read out of the
WRONG arm tree (a stale `PROVENANCE` line pointing at last week's bot) is
indistinguishable from the right one unless the tool says which file it opened.
Resolution order: `TREATMENT TREE` → `TREATMENT DIFF TOUCHES` → `TREATMENT DIFF
REFS` → `PROVENANCE`.

**(5) CANNOT-COMPUTE IS ITS OWN VERDICT WITH ITS OWN STRING.** *"The metric file
is not on disk"* and *"no gate constrains this window"* are opposite facts. The
selftest asserts **the two strings DIFFER**, not merely that a line was printed —
this project's signature defect is a guard that reports SUCCESS on a NO-OP.
**Ambiguity is also a can't-tell:** a gate name binding to two distinct values in
one tree is reported as CANNOT-COMPUTE for that name, never silently resolved.

**PARTIAL WINDOWS ARE A WARN, NOT A FAIL.** `r100-r200` across
`HUNT_MIN_RND = 120` is not inert — but rounds r100–r119 cannot contain the
mechanism, and the warn says so. Emitted only for **binding** gates; one per
file-scope gate turned an `r0-r1000` window into four lines of noise, and a warn
channel nobody reads is the same failure as no warn at all.

---

## 5. FORCED-FAIL EVIDENCE

17 selftest cells, in `prereg_check.py --selftest` under
`OBLIGATION 17 — metric window vs round gates`. **Every branch driven to the
verdict it must NOT give as well as the one it must:**

* **#67 rebuilt** — metric `eco.py:233` (enclosing function guarded by
  `HUNT_MIN_RND`, tree value 120), window `r75` ⇒ **FAIL**; window `r200-r400` ⇒ **OK**.
* **#60 rebuilt** — metric `main.py:613` (`LAUNCHER_MIN_RND`, tree value 160),
  window `r50 / r100 / r150` ⇒ **FAIL**; window `r160-r400` ⇒ **OK**.
* declared-gate-alone with an unresolvable tree ⇒ **FAIL**; partial overlap ⇒ **OK**+WARN;
  stale declared value ⇒ **FAIL**, agreeing value ⇒ **OK**;
  `CAN OCCUR: no` ⇒ **FAIL**; `TBD` ⇒ **FAIL**, reasoned `N/A` ⇒ **OK**;
  missing field at lock ⇒ **OK**, same doc under `--fire` ⇒ **FAIL**, and
  `--fire` on a leg with **no mechanism** ⇒ **OK**;
  unresolvable metric at lock ⇒ **OK**+WARN, under `--fire` ⇒ **FAIL**.

⭐ **THE TWO INERT CELLS READ THE REAL SHIPPED TREE.** If either constant moves,
the cell reports the WRONG verdict loudly rather than passing on a fixture that
stopped meaning anything.

---

## 6. BLAST RADIUS, MEASURED BEFORE LANDING

96 documents — `docs/prereg/*.md` + `docs/research/{PREREG,SCREEN,LEG}-*.md` —
run through **both** the committed checker and the modified one, with the real
git-diff resolution path, in both modes:

| mode | verdict flips | new failure id on an already-FAIL doc |
|---|---|---|
| default (lock time) | **0** | **0** |
| `--fire` | **0** | **15** (`METRIC_WINDOW_PRESENT`) |

**No locked prereg changes verdict.** All 15 `--fire` documents were **already
FAIL under `--fire`** before this change, counted: **8 on `OB13_NOT_COMPUTED`
alone** (juustopin, bodyaware, crashdrive, finishhp, gunaxabl, seatscan,
sentthreat, wirehold), **1 on `OB13_INTERSECTION` alone** (sealfloor6), and
**6 older documents already failing 16–21 presence ids each** (loki16b, loki19,
loki20, loki25, collarmedic, the obligations doc itself).
`SCREEN-bodyaware-2026-08-14.md` — the **currently RUNNING**
screen — reads **OK before and OK after** at lock time; under `--fire` it was
already red on `OB13_NOT_COMPUTED` and now carries a second id.

**No prereg was edited to suit the checker.**

---

## 7. KNOWN LIMITS, STATED RATHER THAN DISCOVERED LATER

1. **#54's class (counter reachability) is not covered.** §2.
2. **The check is only as good as the declaration.** A leg that omits
   `METRIC WINDOW:` and is never run with `--fire` gets a WARN and nothing else.
   The obligation binds at fire time by design; **it does not bind a leg nobody
   runs the checker on.**
3. **Function-scope is a proxy for "gates the metric".** A metric read one call
   deeper than its own `def` drops to the WARN tier; a gate in the metric's
   function that governs unrelated code FAILs a leg that is fine. **Both
   directions are possible and the tier is printed so the reader can tell.**
4. **Gate discovery is name-shaped, not semantic.** A round gate that is not
   named `*_MIN_RND`-ish (e.g. a literal `if ct.get_current_round() < 160:`) is
   invisible to it. Declaring it in `GATING CONSTANTS:` is the covering move.
5. **`scratchpad/prereg_cert_s41.py` (the side lane's independent certification)
   still passes 31/31 — but its coverage denominator is a HARDCODED set of 8
   arithmetic ids**, so it reports `uncovered: none` while covering none of the
   five new `METRIC_WINDOW_*` ids (it already omits `CUT_SHORT_FLOOR` and the
   `POOL_ERA_*` family for the same reason). **A coverage denominator that is a
   hand-maintained list under-reports by construction.** Not patched here — that
   file belongs to the side lane.

---

# ⛔ ADDENDUM (builder, on landing): THE `--fire` TIER IS NOT WIRED, SO THIS CHECK IS ADVISORY TODAY

The agent flagged this as its first uncertainty and it is worse than it looks,
because it is **not specific to OBLIGATION 17**.

**Verified:** `grep -rn -- "--fire" tools/` returns **nothing in any firing path**.
`tools/overnight.sh` — the runner — mentions `prereg_check` **only inside a
comment** (`:95`). `tools/corefill.sh` never calls it. **So every check in the
`--fire` escalation tier binds only when a human types the flag by hand:**

* `OB13_UNTRACKED_ARM` (shipped earlier tonight — an untracked arm tree FAILs)
* `OB13_NOT_COMPUTED` → FAIL at fire time
* `METRIC_WINDOW_PRESENT` / `METRIC_WINDOW_NOT_COMPUTED` (this obligation)

**All of them are the enforceable half of their own rule, and none of them is
enforced.** I typed `--fire` by hand several times on 2026-08-14; that is
attention, which is precisely what this project's own finding says does not last.

**THE DURABLE FIX, owed and NOT done here:** `corefill.sh` refuses to launch a
shard whose prereg fails `prereg_check --fire`. That is the point where a leg
stops being a document and starts spending cores, and it is the only place the
tier can bind without a human.

**WHY IT IS DEFERRED RATHER THAN DONE:** `BODYAWR` is a **live screen** and
`corefill.sh` is its runner. Editing a runner mid-leg is what the versioned-
fixtures rule forbids, and the side lane's ruling on hot-editing a runner
(accepted 2026-08-14) applies exactly. **It goes in at the next quiet fixture.**
⚠ Until then, treat every `--fire`-tier check as ADVISORY and say so when citing
one — an unenforced gate that reads like an enforced one is the same class this
whole obligation exists to catch.
