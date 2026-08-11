---
tactic: Make the push RESUMABLE by watching a live count of the one asset it depends on and rebuilding the instant it hits zero — and the counter must be able to fall
source: https://battlecode.org/assets/files/postmortem-2025-om-nom.pdf
origin: Battlecode 2025 / om nom (finalists)
evidence: documented
transfers: yes
---

## WHAT IT IS — arm D: the field's answer to "how do you make an attack resumable rather than restartable"

om nom list it as improvement #3 in a numbered list of what they changed, and
they lead with the failure rather than the fix:

> *"We need to be robust to losing Paint Towers"*
> *"Losing a Paint Tower at the beginning of the game was devastating, because
> if you didn’t rebuild it, you would never make paint again and so all your
> units would die and you were basically guaranteed to lose. This was one of the
> reasons why rush was so effective."*

The fix is four words of policy and one line of bookkeeping:

> *"To combat this, we found a trick for computing the number of Paint Towers.
> Whenever our estimated number of Paint Towers hit 0, we would just build
> another one."*

**Referent check.** "This" in *"To combat this"* refers to the devastation of
losing a Paint Tower described in the previous sentence, not to rush in general —
the rush sentence is a subordinate observation about *why* the vulnerability
mattered. "Estimated" is theirs and load-bearing: they could not directly count
the towers, so the whole plank rests on **maintaining a count that tracks
reality, including downward.**

**Why this is the arm-D answer.** Arm D asked what it costs to have an attack
stopped and have to remount it. om nom's answer is that the cost is unbounded —
*"you would never make paint again"* — **not because the attack was stopped but
because a prerequisite silently went to zero and nothing was watching.** The
remedy is not a bigger reserve or a faster remount. It is a **liveness invariant
on the single asset the whole plan is a function of.**

The same document supplies the companion finding on the other side of the same
coin, already filed as
[`finish-the-task-before-you-withdraw`](finish-the-task-before-you-withdraw.md):
> *"the soldiers went home unconditionally at around 50 paint to refuel. This
> would lead to disastrous scenarios where we would barely get to a tower and
> then retreat without using roughly 10 attacks!"*
Together they are one doctrine: **do not abandon work you have paid for, and do
not fail to notice that the thing you depend on has died.**

## WHY IT MIGHT TRANSFER — and ⭐ WE HAVE THIS BUG, IN ITS THIRD INSTANCE

Our tree has hit om nom's failure mode **three separate times**, has fixed it
twice, and the third is live.

`bots/_v148ferryfirst/doctrine.py` documents the pattern by name:

* **`SLOT_FWD_GUN` — FIXED (LOKI-2b).** The comment at `doctrine.py:1222` is
  explicit: *"is written ONLY as `read + 1` (raid.py) and is never decremented
  … it counts every forward sentinel we have EVER built, alive or dead. Three
  destroyed turrets close the forward-sentinel arm PERMANENTLY for the rest of
  the match."* The fix is exactly om nom's — a **live census**
  (`raid.py:450 _live_fwd_guns`, `LOKI2B_LIVE_CAP_ON = True`), with the
  instrument-blindness case handled correctly: it *"Returns None when this unit
  cannot see the siege band at all, so the caller falls back to the monotone
  store rather than reading a census of zero as"* `"the cap is free"` — the
  inner quote marks are the source's, rendered as code so the outer quotation
  stays intact.
* **`SLOT_LAUNCHER` — FIXED (LOKI-6).** `doctrine.py:1427`: *"cleared ONLY on a
  failed build -- never on death. Lose the launcher and `_try_build_launcher`
  returns False forever … Same shape as the SLOT_FWD_GUN rubble counter that
  LOKI-2b had to fix."* Fixed by `LOKI6_LAUNCHER_RELEASE`.
* **`SLOT_HARVESTERS` — NOT FIXED.** `doctrine.py:381` states it plainly:
  *"SLOT_HARVESTERS is a monotone high-water mark of harvesters BUILT"*, and
  `eco.py:381-382` is a one-way ratchet:
  ```python
  if live > ct.read_store(SLOT_HARVESTERS):
      ct.write_store(SLOT_HARVESTERS, live)
  ```
  **`live` is already computed on that line and then discarded whenever it is
  smaller.** The slot can rise and can never fall, so it can never reach zero,
  so om nom's trigger cannot fire on it.

**This is our Paint Tower.** Our whole forward arm gates on it —
`raid.py:409` refuses the siege while `read_store(SLOT_HARVESTERS) <
LOKI_FWD_MIN_HARV`, and `main.py:606` and `eco.py:773` branch on it too. The
failure is the mirror image of the SLOT_FWD_GUN one: that counter got stuck HIGH
and closed an arm; this one gets stuck high and **holds an arm open on an economy
that has died**, while nothing anywhere triggers a harvester rebuild on loss.
And `CLAUDE.md` makes the underlying asset load-bearing in the other direction
too: *a harvester with no route home is worth zero on key 1, forever*.

**EFFECT ON MEDIAN KILL ROUND: NEUTRAL-TO-EARLIER, and that is testable rather
than assumed.** This is not a defensive purchase — it buys no HP and no
screening. It replaces a *stale belief* with a *true one*. It should make the
kill EARLIER in games where our economy was silently dead and we kept
siege-gating off a phantom (the siege opens on a real economy, sooner);
it can make it LATER only in games where the phantom count was accidentally
carrying us past a gate we would otherwise fail. **Both directions are real and
this is exactly why it needs the bar rather than an argument.**

## WHAT WOULD KILL IT

* **The readers were written against a monotone counter and may depend on it.**
  Flipping `SLOT_HARVESTERS` to a live count would let a harvester death slam
  `raid.py:409` shut mid-siege — turning a fixed instrument into a new way to
  stop trying, which is the exact failure `doctrine.py:1436` warns about
  (*"They remove three ways it stops being allowed to try"*). **The plank is the
  rebuild trigger, NOT the slot rewrite.** Any version that changes the published
  slot must be treated as a different, riskier plank.
* **Our harvesters may not be the binding asset.** Sweep 8 concluded the economy
  is not our constraint; `R1000_IS_DEFEAT` makes economy instrumental. If
  harvester loss is rare in our games, the trigger never fires and this is a
  correctness fix with no currency — a cheap null, but a null.
* **A blind unit reading a live count as zero is the known hazard**, and
  `_live_fwd_guns` shows we already know its shape. A rebuild trigger keyed to a
  census computed by a unit that cannot see the ore field would spam harvesters.

## BUILDER HOOK — smallest thing that would test it, and it needs NO new store slot

The 16-slot store is fully bound (`doctrine.py:931-961`, remapped `:1166-1170`),
so a plank needing a new slot is not buildable as written. **This one does not
need one.**

`eco.py:381` already computes `live` — the true count of harvesters this unit can
see — and throws it away on the downward branch. The minimal change is to use
that **local** value as a rebuild trigger, while continuing to publish only the
monotone high-water mark to the slot so no existing reader changes behaviour:

> if `live` is not None **and** `live == 0` **and** `read_store(SLOT_HARVESTERS) >= 1`
> — i.e. *we once had harvesters and this unit can see that they are gone* —
> then promote harvester rebuild to the top of this builder's action priority.

Zero new slots, zero changed readers, one new branch. **Guard it the way
`_live_fwd_guns` is guarded:** return early unless the unit is close enough to
the ore field for a zero to mean *absence* rather than *blindness*. That guard is
the whole plank — without it this is an alarm that cannot tell it is blind, which
is the failure mode `CLAUDE.md` names for `ship_watch`.

Pre-register **median kill round** alongside delivered-Ti so the neutral-to-earlier
prediction above is falsifiable in both directions.
