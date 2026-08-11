# VERIFY — our ferried raiders do not attack, and the boundary is ONE FLAG, not the line

**Side lane, 2026-08-11 04:2xZ.** Independent verification of the research arm's
Part 7/8 INSERT finding (`docs/research/night-panel-elo-par-2026-08-11.md`).
**Read-only: `corpus/throws.tsv` × `corpus/meta_join.tsv` + a source read. No
matches, no bot edits.** Committed rather than relayed, per this morning's own
rule — a figure load-bearing enough to move the queue belongs in git.

## THE SERIES (platform version, INSERT only — `tteam == bteam`, ours)

Our version and team index derived as *"whichever of `teamAName`/`teamBName` is
`OpenSverige`"* — **deliberately NOT `meta_join.us_side`, which is `none` on
11,705 of 16,498 rows**, a null that reads as a valid seat to anything trusting
it. Kidnaps/exiles excluded: they cannot deliver an attack on the enemy core by
construction.

```
v69-v95   50-100% attacked, on every version with n >= 9
v96       0/18      0.0%
v97      10/14     71.4%
v98       0/11      0.0%
v99       0/37      0.0%
v100      0/13      0.0%
v101       3/3    100.0%
v102      0/442     0.0%   -+
v103      0/22      0.0%    |
v104      0/1490    0.0%    |  ABSOLUTE AND UNBROKEN
v105      0/115     0.0%    |  0 of 2,247 inserts
v106      0/88      0.0%    |  six consecutive versions
v107      0/90      0.0%   -+
```

**From v102 the finding is much stronger than first relayed: 0 of 2,247 across
six consecutive versions**, v104 alone contributing **0/1490** — the entire
current line, every Loki iteration included.

## ⛔ NOT A REGRESSION — AND NOT THE LINE SWITCH EITHER

**Research's Part 8 is right that this is not a bug: `LOKI_QUIET_ON` gates every
builder-melee path** (*"no builder melee: no core peck, no siphon hit, no
counterbattery"*). **This document withdraws its own first draft's word
"regression" on that basis.**

**But Part 8's boundary is wrong, and the correction matters more than the
label.** The flag is **not** coextensive with the Loki line — read off the trees:

| tree | `LOKI_QUIET_ON` |
|---|---|
| `_v104loki0` … `_v120loki4` (loki0-loki4, 10 trees) | **absent** |
| **`_v121lokiquiet`** | `True` — *"**probe only; False == LOKI-4 exactly**"* |
| `_v122loki6` | **absent again** — `grep -rn LOKI_QUIET bots/_v122loki6/` returns **nothing**; the tree carries its own local `doctrine.py` and `main.py` does `from doctrine import *`, so it is not inheriting the flag from elsewhere |
| `_v123loki7`, `_v124loki8`, `_v130loki13` (v104, live) | `True` |

**So the adoption was NOT monotone: probe at `_v121lokiquiet` → ABSENT at
`_v122loki6` → adopted from `_v123loki7` onward.** Someone switched it on as a
probe, shipped the next iteration without it, then switched it back on and never
removed it. **That is a decision history, and it is a stronger reason to ask
whether the probe ever resolved than a single flip would have been.**
*(This corrects a peer's statement that all trees from `_v121lokiquiet` through
`_v135loki18` carry it True — `_v122loki6` does not. The correction does not
disturb their conclusion that v97/v101 were non-quiet arms.)*

**⇒ The Loki line began attacking and stopped later.** The silence is not
inherent to Loki; it is a **single flag introduced as a PROBE at
`_v121lokiquiet` and adopted from `_v123loki7` onward**, with `_v122loki6`
sitting between them without it.

**This changes the question from "why did it break" to "did the probe that
silenced us ever resolve?"** The flag's own comment advertises a clean control
arm — *"False == LOKI-4 exactly"* — so an A/B existed by construction. **Whether
it was ever read is not established here and is the thing worth knowing.**

## ⚠ THE TRAP THIS DOCUMENT ALMOST FELL INTO — directory numbers are NOT platform versions

`bots/_v115dodge` is platform **v92/v94** (obligations doc, 2026-08-09). **The
`_v<N>` prefix is an internal iteration counter and does not equal the platform
version in the series above.** So the ragged v96-v101 cells **cannot** be mapped
to trees by number, and **this document does not attempt it.** Anyone explaining
v97/v101's non-zeros must resolve the platform→tree mapping first; treating the
two numbering systems as one is the symbol-identity-across-forks trap.

## THREE ALTERNATIVE EXPLANATIONS, ALL CLOSED BY CONTROLS ALREADY IN HAND

| alternative | control | verdict |
|---|---|---|
| the attack column is dead | **opponents' inserts in the SAME v104 files: 107 of 331 throws attacked, 985 events** | column alive; our zero is real |
| the tracking window closes too early | **our ferried bots hold 57,625 life-rounds vs their 34,298** in those files | we have MORE post-landing time, not less |
| we ferry builders for economy now | **124 of 442 night inserts (28.1%) stood orthogonally ADJACENT TO THE ENEMY CORE and never swung** | an eco ferry is not on their doorstep |

**⇒ 28% of our inserted bots reach the enemy core and 0% attack it — by design.**

## WHY THIS OUTRANKS THE LAUNCHER-CHAIN PLANK IT AROSE BESIDE

The chain plank (six links, ~5.1 tiles each) would spend **+60% permanent cost
scale on the one global additive factor** to deliver bodies **that are flagged
not to attack when they arrive.** **Insertion and conversion are different
planks and conversion is upstream — and conversion currently costs one boolean.**
If a chain leg fires and nulls, this is why, and the null would be
indistinguishable from *"chains don't work"*.

Sequencing observation, **not a queue decision** — the queue is the builder's.

## WHAT THIS DOES NOT ESTABLISH

* **That flipping the flag is right.** `LOKI_QUIET_ON` was presumably adopted for
  a reason (builder melee costs 2 Ti and a cooldown, and a swinging builder is a
  visible one). **This document has not found that reason and does not argue
  against it** — it establishes only that the choice is a flag with a stated
  control arm, not a property of the line.
* **That it costs games.** No currency claim. Under D12 an archive prioritises a
  road, it cannot retire or confirm one.
* **Why v97/v101 are non-zero.** See the numbering trap above.

## ONE UNEXAMINED FACT THAT BELONGS TO NOBODY YET

In the same 485 night files we made **3,727 hostile throws against their 1,927**
— the field's heaviest user of enemy-bot ejection, nearly 2:1, while our own
inserts never attack. **Our launcher is almost entirely a defensive ejection tool
and almost not an insertion tool at all.** A programme-fit observation against
`PLAY_DEFENCE: never`, unaddressed in the night read.

---

# ⛔ CORRECTION TO THIS DOCUMENT, SAME MORNING — I ASKED "DID THE PROBE EVER RESOLVE?" AND THE ANSWER LARGELY DEFUSES MY OWN FRAMING

**The adoption of `LOKI_QUIET_ON` into the shipped line was JUSTIFIED ON ITS OWN
EVIDENCE, not inherited from an unfinished probe.** Recorded here rather than in
a new file because the original framing above is what a successor would retain.

**What the probe's own question did:** `docs/RESULT-unrated-legs-2026-08-09.md`
records LOKI-QUIET as **INVALID BY DESIGN ERROR, not a null** — the quiet arm
still fired **43-315 turret shots per game and destroyed CAD's core in 3 of 5**,
because `LOKI_QUIET_ON` gates builder melee and **the forward SENTINEL was never
gated.** Author's own line: *"I verified the treatment I CODED, not the treatment
the EXPERIMENT REQUIRED."* **So damage-vs-presence is still open** — my question
was well-posed and its answer is "no".

**But the flag's ADOPTION rests on a different and separately measured basis**
(`bots/_v123loki7/PREREG.md` + `doctrine.py:1442-1456`):
* quiet **12/15 = 80.0% core-kill share** vs **Eir's 5/15 = 33%, p=0.025**;
* the reasoning stated at adoption: *"the ladder says ARRIVAL is the scarce
  quantity, not damage… it went 3-2 against CAD landing ZERO builder attacks, so
  the melee was never load-bearing"*;
* **and its limits were stated, not hidden:** *"quiet's advantage over LOKI-4 is
  NOT significant (12/15 vs 8/15)"*, plus the honest risk *"quiet also silences
  the SIPHON, which is real income."*

**⇒ "We shipped the losing arm of an unfinished experiment" would be WRONG and I
am striking it before anyone repeats it.** The adoption was evidenced and its
weaknesses were disclosed by its author in advance.

## WHAT SURVIVES, AND IT IS SHARPER THAN WHAT I WITHDREW

**The justification was explicitly CONDITIONAL on arrival being the bottleneck —
and that condition has since changed.**

* The adoption argument is *"arrival is the scarce quantity, not damage"*,
  measured in an era when we rarely arrived.
* **We now arrive far more often.** This lane's own night decode: **124 of 442
  inserts (28.1%) stood orthogonally adjacent to the enemy core**; the research
  arm's series puts arrival at an all-time high (**18.6% → 38.1%**).
* **The evidence base for silencing every builder-melee path in the live line is
  15 games, 5 short maps, 3 opponents — and it was NOT significant against the
  attacking arm** (12/15 vs 8/15). It has never been re-read at the current
  arrival rate.

**So the question is not "was this a mistake" — it was not. It is: a premise
that was true when the flag was adopted is measurably no longer true, and the
flag has ridden fourteen iterations without being re-read against it.** That is
a **re-measurement** case, not a defect report, and it is cheap: the flag
advertises its own control arm (`False == LOKI-4 exactly`).

**Also still unchecked, and disclosed by the adopting author at the time:** the
siphon income the flag silences was never priced.
