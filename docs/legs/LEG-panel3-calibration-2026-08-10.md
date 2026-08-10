# LEG RECORD — PANEL-3 CALIBRATION (s28)

Prereg `docs/prereg/PREREG-panel3-reachable-band-2026-08-10.md`. Runner
`tools/panel3_cal.sh`. **Activates nothing** — v104 is the live incumbent and the
bot under calibration — so zero rated exposure, zero holder risk, and it is the
one arm safe to leave running unattended.

## 1. HOLDER-ASSERT GUARD — MUTATION-TESTED **ON THIS FILE**

`panel3_cal.sh` is the **third** copy of the s27 D28 holder guard. The first two
records cover `fanout.sh` and `panel2_cal.sh`; **this file's header originally
cited PANEL-2's 13:06:51Z run**, i.e. it inherited a citation instead of carrying
a test. Side-lane flag, upheld — *discipline attaches to labels, not function* —
and it matters more here than for the earlier copies, because **this is the arm
nominated to run unattended**: for an attended arm a broken assert costs one
noticed abort; for an 8-hour unattended arm it is the only thing standing between
a version mix-up and a night of contaminated data nobody sees until 06:00.

**ABORT branch**, run at **15:46:09Z** — exit code captured **without a pipe**,
because a piped `$?` returns `head`'s status and that trap has already caught two
lanes today:

```
$ INCUMBENT=999 OUT=/tmp/p3_mut.txt zsh tools/panel3_cal.sh 1
exit=1
15:46:09Z PANEL3: ABORT -- expected v999, holder is 'v104 (Loki v2)'. Firing nothing.
corpus/FANOUT_ABORT: 15:46:09Z panel3 aborted: holder v999 expected, saw "v104 (Loki v2)"
/tmp/p3_mut.txt: No such file or directory        <-- ZERO challenges fired
```

Artifact deleted afterwards so a live monitor cannot read a test as a real alert;
**this record is its trace.**

**PASS branch** — the live arm, holder `v104`, fired and banked 4 challenges at
15:43–15:44Z. **RATE-LIMIT branch** — `rate-limited on eceb8455, waiting 330s`,
i.e. it waited for the window and retried rather than dropping the cell. **The
live arm was unaffected by the mutation run** (still running, still 4 banked).

## 2. THE DEFECT THIS RECORD EXISTS TO CORRECT IS MINE, AND IT IS THE THIRD TODAY

The test was **run** before the commit; what was missing was the **record**, and
the commit message asserted *"abort branch mutation-tested on the copy"* while
the file header pointed at another file's timestamp. **A reader could not tell
the two apart, which makes the claim unverifiable, which makes it a claim.**

**Third instance in one session** — `panel2_cal.sh`'s header (§1 of that leg
doc), the deficit-first count predicate (§5), and now this. **The standing rule
is that the record IS the test, and I have now broken it three times in the same
day while enforcing it on others.** The pattern is specific: *I run the check,
see it pass, and treat the passing as the artefact.*

## 3. Cells and what the leg produces

Six reachable-band cells (`us−80…us+125`): SmartFridge +5 · Askar City +18 ·
The Bisons +32 · farming_200s +35 · 0033 +111 · Lunds Stallions −30.
**n=25/cell**, admission = **in band AND `[0.20, 0.80]` inclusive**, no cell
inherits a verdict. **The Bisons re-derives D22's floor**, two-way pre-committed.

**The artefact this leg exists to produce is the admitted-cell set**, which every
subsequent leg passes to `leg_read.py --live-cells` — the input that stops a leg
deriving its own live-cell denominator from its own outcomes.
