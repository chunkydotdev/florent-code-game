# LEG RECORD — PANEL-2 CALIBRATION (s28, 2026-08-10)

Prereg: `docs/prereg/PREREG-panel2-calibration-2026-08-10.md`, git author time
**14:27:30 CEST** (commit `a8ec673`), ~35 min before this arm's first match.
Platform-`createdAt` half of the two-clock standard is owed at read-out.

Runner: `tools/panel2_cal.sh`. **Activates nothing** — v104 is both the live
incumbent and the bot being calibrated — so zero rated exposure and zero holder
risk, unlike `fanout.sh`, which HANDOVER forbids running unattended.

---

## 1. HOLDER-ASSERT GUARD — MUTATION-TESTED, BOTH BRANCHES

`panel2_cal.sh` is a COPY of `fanout.sh`'s s27 D28 fix. The mutation test done on
the original does not cover the copy (side-lane flag, s28: *discipline attaches
to labels, not function*). Both branches were therefore exercised directly:

**ABORT branch** — `INCUMBENT=999 OUT=scratchpad/arm_panel2_MUTTEST.txt zsh tools/panel2_cal.sh 1`

```
13:06:51Z PANEL2: ABORT -- expected v999, holder is 'v104 (Loki v2)'. Firing nothing.
exit=1
corpus/FANOUT_ABORT: 13:06:51Z panel2 aborted: holder v999 expected, saw "v104 (Loki v2)"
scratchpad/arm_panel2_MUTTEST.txt: does not exist  <-- nothing fired
```

Pre-state: `corpus/FANOUT_ABORT` absent. Post-state: written. **The artifact was
then deleted** so a live monitor would not read a test as a real alert — which is
why the file is absent on disk and why this record exists instead. The claim in
the script's header comment was committed ahead of this record; that ordering was
the defect the side lane flagged, and it is corrected here rather than defended.

**PASS branch** — the live arm, holder `v104`, fired and banked challenges
(3 in cycle 1, continuing). A guard that only ever aborts is not a guard.

**RATE-LIMIT branch** (new in the rewrite) — exercised live at
`13:08:51Z PANEL2: rate-limited on bfbb9a68, waiting 330s (attempt 1)`, i.e. it
**waited for the window and retried the same cell** instead of dropping it.

---

## 2. THE RATE LIMIT IS 20 MINUTES, NOT 10 — AND IT SILENTLY STARVES THE TAIL

Measured on the CLI, verbatim:

```
Error: Rate limit exceeded: max 5 test/unrated matches per 20 minutes
```

`CLAUDE.md` and `fanout.sh` both encoded **10 minutes**; `fanout.sh` sleeps 620 s.
Both corrected.

**Evidence it CHANGED rather than always having been 20:** every s27 arm filled
its five panel cells uniformly — control v104 `7/7/7/6/6`, loki15 `7/7/6/6/6`,
confirm `4/4/4/4/4`, loki16 and loki14 `3/3/3/3/3` — on a 620 s inter-arm cadence.
Under a 20-minute window that is impossible: the tail of the id list would starve
every window. **So the s27 legs are not retroactively damaged by this.**

**The failure mode it creates going forward is silent and biased.** `fanout.sh`'s
`fire()` retries a rejected challenge 3× at 25 s, gives up, prints `fired 3/5`,
and moves on. Under a window it cannot outwait, the drop is **systematic and
always lands on the same cells**. It is not hypothetical: **this leg's own cycle 1
fired 3/5, and the two dropped cells were exactly the two RETAINED controls**
(I Stone `bfbb9a68`, gsxWins `ebd8d82a`) — the cells that link panel-2 back to
panel-1. A calibration leg had begun starving its own linkage.

Fixed in `panel2_cal.sh` two ways: **wait out the window and retry the same
cell**, and **rotate the starting cell each cycle** so a residual drop cannot
keep landing on one opponent. `fanout.sh` is patched to the 20-minute cadence but
**still drops on retry exhaustion — fix that before the rotation is restarted.**

---

## 3. REGIME SPLIT — FOR THE READ-OUT, SO NOBODY INVENTS AN OPPONENT EFFECT

This leg spans two instrument regimes and the read-out must say so:

* **Cycle 1** (13:0x Z): old cadence, no backoff, tail-drop. Banked 1 challenge
  each for `f61d19c1`, `48340ad8`, `0774b1b2`; **0** for `bfbb9a68`, `ebd8d82a`.
* **Cycles 2+** (from 13:08Z): rewritten runner, resumed with **`START=3`** so
  the rotation begins at the two starved cells and closes the deficit first.

Any per-window structure in the results has this in front of it.

---

## 4. WHAT THIS LEG DOES AND DOES NOT LICENCE

Per the prereg: **no plank is tested here and no plank result may be derived from
it.** Admission band `[0.20, 0.80]` on `core_kill_share`, n=25/cell. The
falsifier for the exercise itself stands: if all five cells land inside the band,
**the panel was never the problem** and that gets written.
