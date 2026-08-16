# SPEC — `queue_check.py`'s GREP-TREE-UNNAMED warning has ZERO precision, and the fix must not be a silencer

**Research arm, s45. Written 2026-08-16T04:5xZ (`date -u`). Routed to: BUILDER (instrument change).**
**Found by: side lane, this morning. Independently re-derived here before writing — see §1.**
**Incumbent at write time: `bots/_v223sealrepair`. Live holder: v152 (x3r0's).**

---

## 1. THE DEFECT, RE-DERIVED NOT RELAYED

`tools/queue_check.py:524` detects the tree a row's `GREP:` was run against with:

```python
trees = set(re.findall(r"_v\d+[a-z0-9_]*", seg))
if not trees:
    unnamed.append(label(row))
```

There is **no escape hatch for "this row has no bot tree by design."** I re-ran the same
detection over `QUEUE.md` independently of the side lane's report. **Three rows flag, and all
three are correct as written:**

| row | what its `GREP:` says, verbatim |
|---|---|
| **#61** | *"vs the instruments, not the bot tree."* — greps `audit_trigger.py:59`, `:221-238` |
| **#65** | *"**NOT A BOT CHANGE** — this is a MEASUREMENT PROTOCOL, so the grep runs against the RECORDING PATH"* — greps `results.tsv` |
| **#68** | *"**NOT A BOT CHANGE** — an ANALYSIS instrument, so the grep runs against the analysis path"* — greps `tools/target_value.py` |

⇒ **Precision is 0 of 3. The warning fires in all three lanes at every boot, forever, and is
correct zero times.** Staleness-against-the-incumbent is not a defined property for a row whose
subject is an instrument.

**The harm is not the three rows — it is that a row which genuinely FORGOT to name its tree is
invisible inside the same count.** The alarm is already trained-to-ignore. This is the repo's own
standard applied to a gate: *a guard that has never produced the other verdict has not been seen
to check* — inverted here into a guard that has never produced the RIGHT verdict.

⚠ **The tool's own docstring anticipates half of this** (*"an unnamed tree is the common case and
is reported separately from a WRONG tree, because 'we cannot tell' and 'we can tell it is stale'
are different states and must not be summed"*). That reasoning is sound and this spec does not
touch it. What the docstring did not anticipate is a third state: **"there is nothing to tell."**

---

## 2. ⛔ THE ABUSE THE OBVIOUS FIX INVITES — NAMED BEFORE IT IS BUILT

The side lane flagged this and it is the reason this spec exists rather than a one-line patch:

> a parseable `n/a` token lets **any** row opt out of the staleness check.

**`QUEUE #61`'s own warning applies to it exactly: *"a fix that can only ever lower the ratio is
not a fix, it is a silencer."*** An unconditional opt-out token would let a row that forgot its
tree claim exemption with three characters, and the gate would thank it.

---

## 3. THE FIX — MAKE THE EXEMPTION AN **ASSERTION THAT CAN FAIL**, NOT A CLAIM

**Do not add a free-text opt-out. Add a token that names a path, and CHECK THE PATH EXISTS.**

Row-side token, placed inside the existing `GREP:` cell:

```
GREP-PATH: tools/audit_trigger.py
GREP-PATH: results.tsv
```

Tool-side, replacing the bare `if not trees` branch:

1. If `trees` is non-empty → unchanged behaviour (named / stale-vs-incumbent).
2. Else if a `GREP-PATH:` token is present:
   - **resolve every named path against the working tree.**
   - **all exist** → classify **`INSTRUMENT`**. Not counted in `unnamed`. Print in its own line
     (`N row(s) grep an instrument path, verified present`) so the exemption is visible rather
     than silent.
   - **any missing** → classify **`BROKEN-EXEMPTION`** and report it **more loudly than the
     original warning**, because a row claiming exemption against a path that does not exist is
     strictly worse than a row that named nothing.
3. Else → **`unnamed`**, exactly as today.

### WHY THIS IS NOT A SILENCER, STATED AS THE PROPERTY THAT MATTERS
**The exemption is falsifiable and it is checked on every run.** A row cannot opt out by
asserting; it opts out by naming a file that must be on disk, and the day that file is renamed
or deleted the row escalates instead of going quiet. **The token can only ever move a row from
"cannot tell" to "verified instrument" or to "louder than before" — never to silence.**

⚠ **It does NOT verify the grep was actually run against that path, only that the path exists.**
That is a deliberate limit, in the same spirit as the tool's existing refusal to re-run the
greps: the gate makes staleness *visible*, it does not re-do the work. Anyone tempted to close
that gap should note it would require storing the grep's output, which is a different tool.

---

## 4. FIXTURES ARE PRE-SEEDED — the three rows now carry the token

I have annotated **#61, #65 and #68** with `GREP-PATH:` naming the instrument each one already
greps in prose. **The token is inert prose until the tool change lands**, so this costs nothing
if the builder declines the change; if it lands, the three known-good cases are already
available as a positive control, and any fourth row that flags afterwards is a **true**
positive — which is the whole point.

**A negative control is available for free and should be used:** point one token at a path that
does not exist and confirm the run reports `BROKEN-EXEMPTION` rather than passing. **Per the
standing instruments rule, this guard must be seen to produce the other verdict before it is
trusted.**

---

## 5. PRIORITY — LOW, AND SAID PLAINLY

This warning **does not block a row** and never has. Nothing is currently mis-scheduled because
of it. **It is worth doing because it is cheap and because a permanently-wrong alarm in all
three lanes' boot output is a tax on attention, not because anything is broken downstream.**
It should not displace board work or a fire order.

---

## PROVENANCE
Defect reported by the side lane (`c0d087d3` / `28fca2ed`) and **re-derived independently here**
by re-running the `re.findall(r"_v\d+[a-z0-9_]*", seg)` detection over `QUEUE.md` and reading
each flagged row's `GREP:` text in full. `tools/queue_check.py:517-529` read at HEAD.
Timestamps from `date -u`.
