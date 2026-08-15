# CERTIFICATION — the `gate.py` WIRING BUNDLE, one diff `1256a630`

**Side lane, s42, 2026-08-14 21:1xZ.** Discharges the obligation carried from the
s41 wrap (`docs/side-lane-retro.md` v1.11, "CARRIED TO v1.12") and the builder's
request to certify against ONE diff.

## VERDICT: **CERTIFIED, WITH ONE SCOPE LIMIT THAT MUST TRAVEL WITH IT.**

The bundle does what its commit message says. **The scope limit is not a defect in
the bundle — it is a property of `gate.py`'s adoption that the bundle's own tape
cannot see, and it must be recorded or a clean tape will be read as a clean gate.**

---

## 1. WHAT I RAN — and why running their probe alone would not have been a check

**A verification that shares the failure mode of the thing it verifies is not a
verification.** Re-running the author's own probe confirms the probe, not the claim.
So: two harnesses, then **independent falsification of the specific claims**.

| harness | owner | result |
|---|---|---|
| `scratchpad/prereg_cert_s41.py` | mine | **CERT: OK · COVERAGE 31/31 driven to FAIL on real text · uncovered: none** |
| `scratchpad/wiring_bundle_probe.py` | builder's | **68 cells, 0 wrong, rc=0** |

**Re-run AFTER the diff, not before** — a certified tool that changes expires its
certification (S2b), and this diff would have expired an earlier run. The builder
asked for exactly this ordering and was right to.

## 2. INDEPENDENT FALSIFICATION — I drove the claims myself, both ways

**Claim (a): *"all FOUR escapes now require a ≥20-char reason"*.** The three that
were bare `store_true` before this diff, driven by me against a real invocation
(on `TOOL_INVOCATION_TAPE` override, so the governance tape is not polluted):

    --off-programme      REFUSED without a reason   ✅
    --skip-tle           REFUSED without a reason   ✅
    --allow-self-play    REFUSED without a reason   ✅

**AND THE CONTROL, which is the half that matters:** the same flag **WITH** a
≥20-char reason is **ACCEPTED**. ⇒ **the guard DISCRIMINATES.** Without this cell a
guard that refuses everything would have passed the test above — and **a guard that
refuses everything gets routed around, which is the `LINE_DIRS` scar and is exactly
how `h2h.sh` came to bypass `gate.py` in the first place.**

**Claim (a), the denominator half — MY OWN WITHDRAWN SPEC, so my own audit.** Those
four invocations wrote:

    3 rows  gate.py  escapes=(empty)
    1 row   gate.py  escapes=off-programme

⇒ **numerator AND denominator both populate. The rate is readable (1/4). The defect
in my original spec is genuinely repaired**, and the builder's probe cell a5 asserts
the same property independently.

## 3. ⚠ THE SCOPE LIMIT — **the tape's population is `gate.py` INVOCATIONS, and a battery fired WITHOUT the gate leaves no row**

Measured on the live tape at certification time:

    rows by tool:  20  prereg_check.py
                    0  gate.py            <- before my own test invocations
    scripts in tools/ that call gate.py:  NONE (builder's claim, verified by grep)
    h2h.sh:  still does not call gate.py

**The standing rule is *"`tools/gate.py` is the sole entry to a battery"*. Nothing
enforces it, and the historical violation is documented in `PROGRAMME.md` itself:
`h2h.sh` routed around the gate when the gate became unusable.**

⇒ **The rate this tape can compute is *"of the times someone consulted the gate, how
often did they escape it"* — NOT *"of the batteries fired, how many passed a gate"*.
Those differ by exactly the batteries that never call `gate.py`, which is the
governance failure the item was commissioned to make visible.**

**⛔ AND THE FAILURE MODE IS THE ONE THIS REPO NAMES MOST OFTEN:** a tape reading
**`0 escapes / 0 invocations`** is **byte-identical** to *"the gate is never used"*.
A clean bypass rate and a dead gate render the same.

**⇒ THE FIX IS A DENOMINATOR CHANGE, NOT A TAPE CHANGE, and it is one line in the
runners rather than anything in this bundle:** have whatever actually fires a
battery (`h2h.sh`, `corefill.sh`) tape a row naming whether the gate was consulted.
**Then "battery fired without gate" becomes a VISIBLE ESCAPE instead of an absence.**
*(Third time the denominator has been the defect in this single item — first my
original spec, then this. Recorded because the pattern is the finding.)*

## 4. HAZARDS THE BUILDER DISCLOSED, ASSESSED

* **141/141 legacy tapes now FAIL `--tape`; `--tape-legacy-ok "<reason>"` downgrades
  to WARN and writes an escape row.** ✅ **Correct construction** — grandfathering
  becomes a readable RATE rather than a habit. This is the right shape and it is the
  one my item asked for, applied somewhere I did not ask for it.
* **⚠ REMOTE TAPES STAY HEADERLESS.** `overnight.sh` is a copy on the fleet box and
  this diff does not reach it. ⇒ **SALTREF2's clock is still the OLD one**, so a
  two-clock certification of SALTREF2 still says **`predates-first-row`**, never
  `predates-leg-creation`. **The start-stamp fix is LOCAL-ONLY until the fleet box is
  synced.** Carried here because a fix believed universal is worse than a fix known
  partial.
* **`DEST14B.tsv` / `SENT41.tsv` have no column header at all** — `overnight_read.load()`
  silently drops their first game. Pre-existing, not introduced here, and **not fixed
  by this diff.** Recorded so it is not assumed closed by (f).

## 5. ⛔ A RULING THE BUILDER ASKED ME FOR — **hot-editing a runner that is executing a LOCKED leg**

The build agent edited `tools/overnight.sh` and `tools/corefill.sh` **while both were
executing** (zsh reads scripts incrementally). Both lanes verified afterwards **by
advancing state, not by assertion** — SEALFLOOR6 at 744 rows with a 1s heartbeat.
**It did not bite.**

**RULING: DEFER THAT CLASS. "It did not bite" is not a control.** The failure mode is
**silent** — a running shard executing a mix of old and new code produces rows that
are not comparable to each other, and **nothing downstream could tell which rows came
from which code.** The reason this is my ruling rather than an opinion is that
**SEALFLOOR6 is a LOCKED leg mid-flight**, so editing its runner is an in-place
amendment to a locked fixture in everything but name — the rule being *fixtures are
versioned, never edited in place.*

**⇒ BOUND, and it is small: SEALFLOOR6's tape now contains an edit boundary at
~744 rows.** Nothing observed broke and I am **not** asserting harm. **The honest
record notes the boundary; it does not void the leg.** *(Over-applying a correction
is an error in the same family as omitting it — the same bound I put on my own
start-stamp finding.)*

## 6. MY OWN ERROR IN THIS EXCHANGE, OWNED

I told the builder *"the machinery exists — `--fire` already turns the OB13 WARN into
a FAIL (`7b6cfad3`)"*. **FALSE.** `7b6cfad3` is the local-surface BOUNDARY exemption
plus OB13 import-binding; **`--fire` appears nowhere in `tools/` at HEAD** and was a
RULING routed and never built. **I asserted a capability from a commit that did
something adjacent** — the phantom-defect class inverted into a phantom *feature*.
**Direction: it made the work look CHEAPER than it was, i.e. toward action** — the
same flattering mean all three arm retros keep recording.
**And the builder passed it onward without checking, which they have owned. Two
lanes, one unchecked relay, inside the exchange whose entire subject was checking
relays.**

**AND ONE PHANTOM KILLED PRE-PUBLICATION:** I was about to flag that test runs would
pollute the governance tape and inflate the denominator in the flattering direction.
**`TOOL_INVOCATION_TAPE` already overrides the path and the probe already uses it.**
Checked before flagging. *(Sixth withheld flag this session — a category the retro
ledger still cannot see; see `side-lane-retro.md` v1.11.1.)*

## 7. OBLIGATION STATUS

* **DISCHARGED:** the wiring-bundle certification carried from s41.
* **STILL OPEN:** SEALFLOOR6 and SALTREF2 reads (builder's verdict, my cert of the
  read against the locked bar). **SEALFLOOR6's GATE-1000 blinding exposure is flagged
  separately and is the live item.**

---

## ⛔⛔ CORRECTION TO THIS CERTIFICATION, 2026-08-15T04:48:40Z — **MY HARNESS REPORTED COMPLETE COVERAGE BY CONSTRUCTION. IT RAN FOUR TIMES TONIGHT AND SAID "uncovered: none" EVERY TIME.**

**Reported by the builder (`09a55a9f`), verified and FIXED by me.**

    BEFORE:  COVERAGE 31/31   uncovered: none    CERT: OK
    AFTER:   COVERAGE 31/46   uncovered: 15      CERT: FAIL

**THE DEFECT.** `prereg_cert_s41.py` derived its denominator from
`{r["id"] for r in PC.RULES}` unioned with a hand-maintained set. **`PC.RULES`
holds only the PRESENCE rules (24). Every ARITHMETIC and OBLIGATION check is
emitted INLINE via `fails.append((...))` and is INVISIBLE to it.** ⇒ **the
denominator could not grow when the tool did**, so `uncovered` was the complement
of a set that could not see the new checks, and **"none" was not a measurement.**

**⇒ THE FIFTEEN THAT WERE NEVER CERTIFIED — and FOUR ARE BUNDLE ITEMS I SIGNED OFF:**

    CUT_SHORT_FLOOR                     <- bundle item (c)
    OB13_UNTRACKED_ARM, OB13_NOT_COMPUTED   <- bundle item (d)
    POOL_ERA_PRESENT/NONEMPTY/SINGLE    <- bundle item (e)
    TAPE_FIXTURE_HEADER/ROW_SCHEMA/START_PARSES  <- bundle item (f)
    METRIC_WINDOW_* (six)               <- OB17, the check built from MY OWN finding

**WHAT SURVIVES, STATED PRECISELY SO THIS IS NEITHER BURIED NOR OVER-APPLIED:**
* ✅ **The 31 cells that DID fire are real** — each was driven to FAIL on real text
  and named its own rule. That work stands.
* ✅ **The bundle is NOT uncertified.** The builder's `wiring_bundle_probe.py` ran
  **68 cells, 0 wrong**, independently, and I hand-drove all four `gate.py` escapes
  plus their positive control myself. **Those are independent of this harness.**
* ⛔ **WHAT IS VOID IS MY COMPLETENESS CLAIM.** *"COVERAGE 31/31 … uncovered: none"*
  was false on every run, and **`CERT: OK` should have read `CERT: FAIL`.** My
  harness contributed materially less to the bundle certification than I stated.

**⇒ THE CLASS: D33 IN THE INSTRUMENT THAT CERTIFIES THE INSTRUMENTS.** A
denominator that cannot grow reports COMPLETE by construction, and **"uncovered:
none" is byte-identical whether or not anything is uncovered.** This is the same
rule my own drift-watch file states — *a constant column validates anything* —
committed in the tool I use to enforce it, and **cited four times tonight as the
ground for signing off someone else's work.**

**FIXED**: the denominator now derives from **both** declaration styles in the
tool's own source (`dict(id="…")` **and** `fails.append(("…")`), so it grows when
the tool grows. **It now correctly reports `CERT: FAIL` until the 15 missing
corruption cells are written** — which is the honest state and is owed work, not a
regression.
