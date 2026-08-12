# SIDE-LANE RETRO — instance s34, 2026-08-12

**Instrument: `docs/side-lane-retro.md` v1.3.4. FIRINGS: 4** (s29, s32, s33, s34).
**Run at Magnus's wrap call, answered from the day's artefacts — 29 commits, the
peer message traffic, the drift monitor's event stream — not from memory.**
**Session: 17:24Z boot → 21:1xZ wrap, ~4 hours.**

---

## Q1. CONSUMPTION — were flags ACTED ON, or filed?

**~24 flags raised. 21 changed an outcome. 0 ignored. 3 correctly refused.**
Consumption was again ~100% and same-hour, and the reason is unchanged from
s33: **every flag carried a buildable fix.**

| flag | outcome it changed |
|---|---|
| two stale v114-pinned monitor loops | killed; the racing `ship_watch_state.json` pinned |
| ship gate had **no calibration cell on its own contrast** | `_v169null` built md5-identical, `SHIPGATENULL` queued **before the shards read out** |
| the cell was **invisible to `_cal`** (prefix match) | selector rewritten to match by control tree |
| …and **still** invisible (identification stayed name-based) | rewritten again to **byte-identity**, which cannot rot |
| calibration gap is **general** — 4 control trees, 1 cell | per-contrast calibration + `BORROWED` banner on every run |
| `PROGRAMME.md:8` stale across three holders | **Magnus updated it** (v112 → v116, my hand, his directive) |
| `raid.py` station scorer has no enemy-SENTINEL term | **`QUEUE #30`** |
| `#29` points 9 and 10 target disjoint tiles | row re-priced to the **leaf** payoff |
| `#29`'s 8-seat structural bound | trunk case closed; **saved research a per-opponent query** |
| belt curve: *"monotonically"* false on its own table | **claim withdrawn by its author** |
| `#30`'s 4.6× is a **share** ratio, not a payoff ratio | **D46**; row re-sized to 0.32/game; **queue re-ranked** |
| `#32`'s *"~3× per build"* is a median ratio | corrected to 2.0×; *"ONLY survival"* withdrawn |
| `#31`'s scale surcharge, priced at ~12 Ti | one line in the row; **reported as SMALL** |
| GUNBLOCK overlaps shipped LOKI-25 | non-additivity risk declared **before** the shard |
| gsxWins fails the **band** gate (not payout) | the mandated gate line written **before the cells fired** |
| **`bots/starter` control uses unseeded `random`** | **retraction: the engine is DETERMINISTIC; `check_control_equivalence` SURVIVES** |
| `#32`/`#33` renumber left a stale use here | superseded; **relay-a-pointer-not-a-copy** rule |
| new uniqueness alarm fired **3:1 wolf** on first run | tombstones excluded; **D48** |
| the ship-gate early stop | licensed line added to `HANDOVER` |
| v116 duplicate: seat- and map-matched | strongest fixture-resolution measurement in the repo |
| Leviathan 4-1 doesn't survive its primaries | flattering read retired before it was banked |

## Q2. LATENCY — did the flag beat the decision it bore on?

**Ahead in 22 of 24.** The three that mattered:
* **`SHIPGATENULL`** — raised **before the gate shards read out**; the band on
  the ship decision is now measured rather than borrowed.
* **The `starter` control** — raised **~90 seconds before** a guard would have
  been retired, and the guard was the one its own author had named as catching
  the day's biggest defect.
* **gsxWins** — the gate line written **before the cells fired**; afterwards it
  is a defence.

**Two arrived late and both were mine:** the `#32` estimator flag reached the
wrong lane (a collided row number, §Q5), and my overnight-readiness check ran
**after** both peers had wrapped rather than before.

## Q3. ⚠ INFERENCE PUBLISHED AS FACT — this lane's characteristic failure

**FOUR published. Down from s33's thirteen, and the mechanism is unchanged.**

| # | claim | the substitution |
|---|---|---|
| 1 | *"`SENTINEL` → nothing"* in `raid.py` | grepped **one function**, published it as a property of the **file** (`:366` gives `GUNNER`/`SENTINEL` `pr=3`) |
| 2 | *"local self-play UNDERSTATES `#30`"* | cited `#23`'s **turret-share** over the **top-6** to argue about **sentinel counts** on a **five-opponent panel** |
| 3 | *"not established anywhere I can find"* (the API default) | a claim about **where I looked**, wearing a claim about **the repo** |
| 4 | *"the session-level explanation is better"* | accepted a generalisation at **n=4 within one session** — the exact fault v1.2.1 retracted, while holding the retraction |

**⭐ DIRECTION: 4 of 4 ran toward the row I was supporting or auditing** — and
**#2 was committed inside the message flagging the builder for a pooled
denominator.** I enforced the rule and broke it in the same paragraph.

**⛔ AND THE UNIFIER IS SHARPER THAN THE COUNT: three of the four are the SAME
SUBSTITUTION — a claim about the SCOPE OF MY SEARCH published as a claim about
THE WORLD.** #1 (one function → the file), #3 (my search → the repo), and #2
(one population → the field). **That is one fault with three costumes.**

## Q4. DID MY OWN WATCH CATCH MY OWN WORK?

**5 of 9 self-caught — worse than s33's 6 of 13 by rate, and the four external
catches were all on the SAME artefact.**

**Self-caught (5), and the mechanism is unchanged and is still not diligence —
it is GOING TO USE THE THING:** the fabricated commit hash (caught while
committing) · the digit-excluding field regex (caught because 17 was followed by
19) · the self-play direction, before publishing (caught by opening the primary
instead of the commit subject) · the map-identity item I left open and closed
myself · **and the overnight-readiness check, whose three alarms were ALL FALSE
and which I caught by running a second instrument before publishing.**

**Peer-caught (4):** `SENTINEL → nothing` · the understatement direction ·
`SHIPGATENULL`'s fix, **twice**.

**⛔ THE ONE THAT IS THE PUREST INSTANCE OF THE AUDITOR'S BLIND SPOT: I PRINTED
MY OWN EXECUTION GUARD AND RAN THE TOOL IN THE SAME COMMAND**, so the guard's
result was never consumed — **the exact defect I had flagged in three other
instruments that day.** Not a wrong correction; a check I performed and did not
act on. **Corrected on the next execution by inspecting the call site first and
clearing it deliberately.**

## Q5. FALSE POSITIVES — what did flagging cheaply cost?

**3 wrong. ZERO caused harm — against s33's two.**
* **The overnight alarm: 3 false in one check** (stale heartbeats on *completed*
  shards; "nothing running" from a `pgrep` that masked its own failure; a 95%
  disk that is the machine's, not ours — our whole footprint is 9.3 GiB with
  91 GiB free). **Caught before publishing.**
* **`SENTINEL → nothing`** — wrong as stated; **the corrected form is stronger**,
  so the flag improved the row it nearly weakened.
* **The understatement direction** — reversed; **the builder's split produced a
  better fixture position than either of us started with.**

**⭐ THE POLICY'S PRICE IS BACK TO ~ZERO AND THE REASON IS STRUCTURAL: every
flag this session carried BOTH BRANCHES AND A DISCRIMINATING TEST.** The
`starter` flag named the exact experiment that would vindicate the author —
**and it did**, in the opposite direction from my suspicion, within a minute.

## Q6′. CLAIMS ABOUT ANOTHER LANE — including relayed FIGURES

**~8 claims about peers' work. ZERO wrong, and this is the question's first
clean run since it replaced Q6.**
Every relayed figure carried its owner and window: the builder's 2.17→0.73 and
research's 3.03→0.93 were **named as two different cuts and reconciled** rather
than pooled; the `pid`/`etime` figures I gave research were **labelled as mine
with my clock**; and when the builder caught the v118 seat-B confound
concurrently, **I recorded it as concurrent rather than relayed so the ledger
was right.**
**Conduct claims: zero, fifth consecutive run** — the s28 rule continues to hold
after the question that measured it was struck.

## Q7. WHAT DID I DECLINE, and was declining right?

**Six. All held.**
1. **Running the retro on a PEER'S RELAY that Magnus had called the wrap** —
   *"a relayed directive is not a directive to me"*, the s28 precedent where the
   builder refused on my relay and was right. **Held until Magnus said it here.**
2. **Editing `PROGRAMME.md` on my own initiative** — flagged the stale
   `INCUMBENT` and the retired-1650 prose, edited **only** on his direct word.
3. **Running `target_value.py`, `gate.py`, `audit_trigger.py`** — all trip the
   execution guard; **computed the gsxWins verdict from the constants by READING
   the source instead.**
4. **Clearing the 595 undecoded replays** — research declined for the same
   reason and I would have too: 8 shards running, and the ceiling exists to
   protect their timings.
5. **Every verdict**, including the ship call.
6. **⭐ ADVISING AGAINST A QUERY: I told research NOT to run the per-opponent
   group-by they offered** — the 8-seat structure is opponent-independent, so no
   timing cut could reopen the trunk case. **Declining to consume someone else's
   work is a decline this question had not seen before.**

## Q8. MECHANISATION — did any flag become a SCRIPT?

**FIVE.** (s28: 3 · s32: 6 · s33: 10 · s34: 5 in a half-length session.)
* **`overnight_read.py` — calibration PER CONTRAST**, selecting by control tree,
  then by **byte-identity**; `BORROWED` banner naming the arm count.
* **`overnight_read.py` — the `SHIPGATENULL`-not-reachable case as a permanent
  cell**, the failure itself turned into a test.
* **`tools/leg_record.py` (NEW)** — fixture fingerprint per leg cell: seat, dims
  **and core geometry by trilateration**, with the **dims-collision case asserted
  to FAIL to pair**. **It also added a case I missed: same maps in a DIFFERENT
  ORDER must not pair.**
* **`queue_check.py` — unique row numbers**, scanning **table rows AND section
  headings** (the real collision was one of each), with a regression cell.
* **`queue_check.py` — tombstones do not collide**, from the alarm's 3:1 first
  live run.

**The practice is unchanged and is the whole explanation: FLAG THE DEFECT WITH
ITS FIX.** s34 adds the condition s33 learned: **the fix must name what it was
verified against** — and §Q9 shows what happens when it does not.

## Q9 (NEW, adopted from research's v1.7) — DID MY CORRECTIONS NEED CORRECTING?

**THREE of my corrections were themselves corrected, and ALL THREE by peers.**
1. **`SHIPGATENULL` — wrong twice.** Specified a cell without opening its
   consumer; then the fix I proposed (control-tree matching) **still** left it
   unreadable because identification stayed name-based.
2. **The self-play direction** — my correction of the row ran the wrong way.
3. **The session-level explanation** — I corrected my own lane-level account
   toward it, and its next data point falsified it.

**⭐⭐ THE PATTERN, AND IT IS THIS INSTANCE'S HEADLINE: I WAS RIGHT THAT SOMETHING
WAS WRONG, AND WRONG ABOUT WHAT WOULD FIX IT — EVERY TIME.** Detection was sound
in all three; the **prescription** failed. ⇒ **DETECTION and PRESCRIPTION are
different accuracies and this lane is visibly better at the first.**
**A flag that names a fix carries the authority of the detection into a claim
that has not earned it** — and research's companion mechanism explains why nobody
catches it: **a correction inherits the authority of having been careful; the
diligence is the disguise.**
**⇒ THE DERIVED CHECK, mechanical, adopted: when you correct a number, RE-RUN THE
ORIGINAL OBJECTION AGAINST THE CORRECTED NUMBER before publishing.** My second
`SHIPGATENULL` fix failed the *same question* my first one did — *"can the
consumer read this?"* — and I never re-asked it.

---

## THE LEDGER

> **Prevented: 21. Caused: 0. Nearly caused: 1.**

**Prevented, largest first:** a guard retired on a control that shared its fault
(`check_control_equivalence`, ~90 s before it went) · the ship gate's band
measured on its own contrast instead of borrowed · a rated 0-5 by the live holder
surfaced from raw replays after the corpus never ingested it · `#30` re-sized 4.6×
→ 1.4× and the queue re-ranked on it · `#29`'s trunk case closed on an 8-seat
structural bound before any games · a flattering Leviathan read retired · the
mandated target gate written before the cells fired.

**Nearly caused: 1** — the `SENTINEL → nothing` overstatement, which would have
let a naive grep contest `QUEUE #30`. **Caught by research; the corrected form is
stronger than mine.**

**Caused: 0.** *(s33 caused two. The difference is not care — it is that every
flag this session shipped with both branches and a discriminating test, so the
wrong ones cost a reply instead of a plank.)*

---

## THE ONE THING I WOULD TELL MY SUCCESSOR

**Your detection is trustworthy and your prescriptions are not.** Three times
today the defect was real and the fix I named was wrong — twice on the same
artefact. **When you have found something, say what is broken and what test
would settle it; say what would FIX it only after you have opened the thing that
must consume the fix.** The cheapest version of this rule: **a fix is specified
against the CONSUMER, not against the artefact.**
