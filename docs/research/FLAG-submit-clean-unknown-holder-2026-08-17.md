# FLAG — `submit_clean.py`'s holder restore is disarmed by an unreadable holder

**Side lane, s48, 2026-08-17T04:26:37Z.** Found while auditing the ship chain during a live
`fcode status` outage. **Reported to the builder at 04:24:5xZ and ACCEPTED** (fail-closed fix on
their wrap debt list, this state table as the spec; a standing no-`submit_clean` constraint adopted
for the session in the meantime).

**Version tag:** holder `v155` "Sleipnir v1" (Moonfarm, 2026-08-16T19:38:40.236Z);
`INCUMBENT: bots/_v468kladturbo`; `SLOT_STOP_LOSS: off`. Tool as of `5a1e652c`.

**Anchors:** `CLAUDE.md` — *"SUBMITTING **IS** SHIPPING. `fcode submit` AUTO-ACTIVATES WHAT IT
UPLOADS"*; the measured **−24.67 Elo across 3 leaked rated matches** (~−8/match); and the script's
own `_holder()` docstring.

---

## THE DEFECT

`tools/submit_clean.py:473`, with its `elif` at `:497`:

```python
if holder_after and holder_before and holder_after != holder_before:
    ...restore...
elif holder_after == holder_before:
    print("holder unchanged by submit.")
return 0
```

`_holder()` returns `None` when the `Active bot:` line is absent from `fcode status`.
**`None == None` is `True`.** So a submit whose before- and after-reads both fail prints
**`"holder unchanged by submit."`** and exits **`0`**.

⛔ **`_holder()`'s own docstring states the invariant the code breaks**, verbatim:

> *"Returns None if it cannot be read — and None is treated as UNKNOWN, never as 'unchanged'."*

**The docstring is right. The branch does the opposite.** This is a documentation/behaviour
inversion in a guard, which is the shape that survives review longest — a reader who checks the
docstring is told the correct thing.

## DRIVEN, NOT REASONED

The branch was replicated verbatim over the holder-read state space in a throwaway interpreter —
**read-only: nothing imported, nothing submitted, no platform contact.** Since `fcode submit`
ALWAYS auto-activates, "no restore attempted" always means "the prototype is the live holder".

| `holder_before` | `holder_after` | outcome | safe? |
|---|---|---|---|
| readable | readable-prototype | **RESTORE ATTEMPTED** | ✅ YES |
| readable | readable-same | `"holder unchanged by submit."` → 0 | n/a (submit did not take) |
| readable | **UNREADABLE** | falls through silently → 0 | ⛔ **NO — PROTOTYPE STAYS LIVE** |
| **UNREADABLE** | readable-prototype | falls through silently → 0 | ⛔ **NO — PROTOTYPE STAYS LIVE** |
| **UNREADABLE** | readable-same | falls through silently → 0 | ⛔ **NO — PROTOTYPE STAYS LIVE** |
| **UNREADABLE** | **UNREADABLE** | `"holder unchanged by submit."` → 0 | ⛔ **NO — PROTOTYPE STAYS LIVE** |

**4 of 6 states leave an unmeasured prototype on the RATED ladder and report success.**

* ⛔ **Row 4 is the worst: the tool CAN SEE the prototype is live** (`holder_after` reads fine) **and
  still does nothing**, because `holder_before` is `None`. The information needed to act is in hand
  and the branch cannot reach it.
* ⛔ **Row 6 is the most dangerous to a reader**, because it does not merely fail silently — it
  prints an actively false sentence. *"holder unchanged by submit"* is the one claim that cannot be
  true after an auto-activating submit.
* ⛔ **`--leg` mode lives INSIDE the restore branch**, so in a blind window the leg hold and its
  `LEG_TIMEOUT_S` auto-restore never arm either. **The timeout is not a backstop for this.**
* ✅ **`--activate` is UNAFFECTED** — it returns earlier. **This bites the DEFAULT path**, i.e. the
  prototype-leg path the restore was written for. The ship path is fine; the *"submit is not
  shipping"* path is the broken one.

## WHY IT IS REACHABLE TODAY, NOT HYPOTHETICALLY

The triggering state was **live while this was written**. `fcode status` was flapping between three
distinct response states (see the boot note and the correction below), with `Active bot:` absent for
23 consecutive `holder_watch` polls between 03:12:06Z and 03:56:16Z alone.

⇒ **A prototype leg fired in that window would have leaked onto the rated ladder for as long as
nobody looked, with the tool's own exit code and final line both reporting success.**

## THE FIX — named, not written (tools are the builder's)

The chain needs an arm for `holder_before is None or holder_after is None` that **fails loud**
(non-zero exit, "HOLDER UNKNOWN — VERIFY AND RESTORE BY HAND NOW") *before* the equality test.

**⭐ THE DURABLE RULE, which is worth more than the diff: FAIL CLOSED ON UNKNOWN; NEVER FOLD UNKNOWN
INTO UNCHANGED.** `None == None` is the specific idiom that folds them, and it will read as correct
to anyone who does not have the three-valued case in mind. **Two values are being represented in a
type that has no room for the third.**

---

## ⚠ A CORRECTION TO THIS LANE'S OWN BOOT NOTE, 20 MINUTES AFTER PUBLISHING IT

The boot note (`a2bb7b2a`) gave the degradation signature as *"`fcode status` returns `Error: True` +
`Could not fetch live data`"*. **`Error: True` IS NOT A DEGRADATION SIGNAL — it prints on fully good
reads too.** Measured 04:23:19Z: one sample carried `Error: True` **and** `Rating: 1803` **and**
`Active bot: v155 (Sleipnir v1)`; four further samples in the same two seconds carried `Error: True`
alone. **Amended here rather than silently.**

⭐ **THE REPLACEMENT IS MORE USEFUL THAN THE THING IT CORRECTS — THERE ARE THREE RESPONSE STATES,
NOT TWO:**

| state | carries | holder readable? |
|---|---|---|
| **FULL** | rating + rank + `Active bot:` | ✅ yes |
| **PARTIAL** | rating + rank, **no `Active bot:`** | ⛔ **no — THE HAZARD** |
| **EMPTY** | neither | ⛔ no (and obvious) |

**PARTIAL verified at 04:22:41Z:** the text block printed `Rating: 1803 (Emerald) — 1156 matches
played`, `Rank: #19 of 126`, `Team: OpenSverige (?)` — **and no `Active bot:` line at all.** The
`--json` path in the same second returned only
`{"user":…,"team":…,"error":"could_not_fetch_live_data"}`.

⇒ ⛔ **READING RATING / RANK / MATCHES OFF `fcode status` DOES NOT VERIFY THE HOLDER.** In PARTIAL a
reader gets three live-looking numbers and no holder. **EMPTY is safe because it is obvious; PARTIAL
is dangerous because it looks like FULL to anyone not grepping the holder line specifically.**

✅ **AND THIS VINDICATES `tools/now.py` RATHER THAN INDICTING IT.** `now.py` gates on
`active_submission` — the load-bearing field `CLAUDE.md` mandates — so **in PARTIAL it is the only
one of the two instruments that can tell FULL from PARTIAL.** Its selftest asserts *"degraded fcode
→ says BLIND"* and *"it must NOT fall back to a poller."*
⇒ **The real gap is that it does not RETRY** — the flap is sub-second (5 samples spanned 2 s and 1
was FULL), so one retry loop converts most BLINDs into reads.
⛔ **RETRY; DO NOT RELAX THE GATE.** Relaxing it — falling back to the text block or a poller —
would remove the D28 protection and break a guard the tool's own selftest asserts. **Accepted by the
builder, who is wording their wrap-debt entry so a successor cannot read it the other way.**

## ⚠ AND A PROCESS NOTE ON HOW THIS WAS FOUND, BECAUSE IT WAS NOT DILIGENCE

This came out of **checking a peer's commit message claim** (*"now.py BLIND = instrument debt"*)
rather than from auditing the ship chain on a schedule. **Q4's mechanism for a fifth run: going to
USE the thing, not re-reading what was written.** The audit of `submit_clean` happened only because
establishing whether `now.py` or the platform was at fault required reading what else consumes the
`Active bot:` line — and `submit_clean` and `ship_ledger` are what came back.

⚠ **The builder's verification itself was SOUND** (their read contained the literal `v155` block, so
they had a FULL read) — **the flag was on the DIAGNOSIS, not the verification, and a flag on a
diagnosis is what found the defect.** A correct conclusion reached through a wrong model of the
instrument still leaves the wrong model in the tree for the next reader.
