# SIDE-LANE RETRO — instance s33, 2026-08-12

**Instrument: `docs/side-lane-retro.md` v1.2.1. FIRINGS: 3** (s29, s32, s33).
**Run at Magnus's wrap call, answered from the day's artefacts — commits, the
ship tape, the worklist, peer messages — not from memory.**

---

## Q1. CONSUMPTION — were flags ACTED ON, or filed?

**~30 flags raised. 24 changed an outcome. 0 ignored.** Named, with what changed:

| flag | outcome it changed |
|---|---|
| `target_value.py` crashing on **every** entry point but `--selftest` | the mandated pre-prereg gate restored, + entry-point cells |
| destructive-`argv` in **4** decoders (1 guarded, 3 not) | `guard_out()` as a class, one definition, driven both ways |
| `GREP: TODO` satisfying the admission gate | promise-values rejected as a **class**, 3 cells |
| `queue_check` undercounting **8 vs 11** | status made structural; `#25`/`#26` correctly excluded |
| leg-name collisions (LOKI-30, LOKI-31) | `tools/leg_name.py` + `LEG-REGISTRY.md`, 3-way selftest |
| `effective_n` ceiling-pinned at low k | projection retracted, `CEILING` verdict added |
| crash-channel **pooled** cut wrong aggregation | per-opponent cut → road closed **harder**, team `S` found |
| `LAUNCH0` conflating EXILE + INSERT | the launcher **2×2** |
| between-arm MDE on that 2×2 | resolvability **pre-registered** |
| `DELVSDEF` fixture asymmetry, then the challenger-vs-incumbent bias | both recorded **before readout** |
| `kidnap_fate` gate ignoring `ok0` | D24(b) live defect fixed; count derived from the cell list |
| LOKI-48 missing its family history | `QUEUE.md #27`, a **family row** (better than my pairwise ask) |
| `target_value` reading cached ratings silently | freshness header + drift warning |
| `cores_idle` docstring vs shipped predicate | fixed + 6 forced-answer cells |
| *(+10 more: ship-gate specs, D11 GUNBORDER relabel, `replay_throws` fallback & selftest, EXILE0's ferry half, hook exit-code conflation, HANDOVER data-loss omission, control census, …)* | |

**Consumption was ~100% and same-hour.** The reason is unchanged from s32 and it
is not goodwill: **every flag carried a buildable fix.**

## Q2. LATENCY — did the flag beat the decision?

**Ahead in 22 of 24.** The three that mattered most:
* **`target_value` outage** — flagged ~10 min after the commit, **before any
  prereg quoted it**; fixed in 4 min.
* **GUNBORDER D11** — raised at **2% shard completion**, so it cost a relabel
  and not a re-run.
* **`DELVSDEF` biases** — both **before readout**, which is the only time a bias
  note is worth anything.

**Two arrived late and both were mine to be late on:** the **v115 holder change**
(5.5 h stale, §Q3) and the `GUNBLANK` pooling argument, which arrived after the
no-ship call and was wrong anyway.

## Q3. ⚠ INFERENCE PUBLISHED AS FACT — this lane's characteristic failure

**THIRTEEN.** The worst count recorded, and the count is the wrong headline —
**the mechanism collapsed to one shape and it is not s32's shape.**

**s32 was *"inferred from an artefact instead of opening the primary"* (4/4).
s33 is `A PROXY IS NOT THE CLAIM` — I measured something CORRELATED with the
claim instead of the claim (promoted as D25 mid-session, then broken again twice
after promoting it):**

| # | claim | proxy I used |
|---|---|---|
| 1 | is `queue_check` tested? | grep for cell calls → **0**, it asserts **23** |
| 2 | is `elo_logger` tested? | grep for an *in-file* selftest → **0**, 4 cells live in `tests/` |
| 3 | are `PROGRAMME.md` fields unique? | an awk pipeline that mangled the names |
| 4 | which fields are declared? | a **digit-excluding** regex; silently dropped `R1000_IS_DEFEAT` |
| 5 | does `target_value.py` run? | **the exit code**; called a usage message a crash |
| 6 | is the live holder's code present? | **a name pattern** (`bots/*116*`); it is `_v169launchlate160` |
| 7 | what does the sentinel target? | **an assumption**; `raid.py:415` says `core_tiles(E)` |

**Plus six of the older shape:** the invented `elo_logger` double-count hazard
(reasoned from the READER's arithmetic, never opened the writer) · `GUNBLANK`
pooling (ignored selection-on-result) · SURCH core-time (read **win rate**, not
the kill-round axis the programme specifies) · the defence "bracket" overreach ·
the 11+ harvester confound (refuted by the test I asked for) · **v114 asserted as
"the live incumbent" for 5.5 hours.**

**⭐ DIRECTION — and this is the finding, because v1.2 got it wrong.** s32 was
**4/4 comfortable** and v1.2 advised *"check that side first."* **s33 is MIXED:**
comfortable (#2 made a lane's work look worthless; the defence bracket) and
**dramatic** (#5 called a working tool crashed; the invented stop-loss hazard;
#7 predicted 1–2 early kills where the mechanism cannot produce a death event).
⇒ **v1.2's direction advice is retracted, already recorded as v1.2.1. The
MECHANISM replicates; the DIRECTION does not.**

## Q4. DID MY OWN WATCH CATCH MY OWN WORK?

**6 of 13 self-caught; 7 caught externally** — worse than s32's 4-of-5, and the
denominator tripled.

**The mechanism that caught all six is unchanged and is still not diligence:
GOING TO *USE* THE NUMBER.** #1 and #2 fell out while deciding whether to build
the cell; #5 while driving the entry points; the double-count hazard while
opening the writer to implement it.

**⛔ THE ONE THAT MATTERS MOST WAS CAUGHT BY NOBODY FOR 5.5 HOURS, AND MY OWN
INSTRUMENT WAS REPORTING IT.** `ship_watch` printed `v115` and `net_act_src=env`
from **09:17:53Z**; `lg_age_min` — the freshness column **I added this morning
for exactly this hazard** — climbed **39.6 → 464.9 minutes** in every row.
**I read neither, and I added four freshness columns today.** Promoted as **D28**:
*a live, correct gate that nobody reads is D20's mirror and the more dangerous
direction.*

## Q5. FALSE POSITIVES — what did flagging cheaply cost?

**5 wrong. TWO CAUSED HARM — the first time this lane has caused rather than
nearly caused.**

* **⛔ CAUSED: the MAGAZINE BURST misdirection.** I framed the effect as *"against
  builders 1–2 kills, against a core noise"* **without opening the targeting
  code.** The verification followed my framing, counted **enemy builder deaths**
  for a plank aimed at **cores**, and the plank was cancelled on it. **Cost: two
  cancellations and a re-queue under fresh shard names.** Magnus caught it.
* **⛔ CAUSED: SURCH30 cancelled.** My *"~7 core-hours on a settled question"*
  read the win-rate axis and not `DEFENCE_ADMISSION_BAR`'s kill-round axis. **The
  kill-round cell was the only unresolved one** (+17, CI [−2,+41]) and it died
  ~2 minutes before my correction landed. Rows kept; the number was not.
* **NEARLY CAUSED: the `GUNBLANK` pooling argument** — would have shipped a
  winner's-curse estimate. Refuted by the builder's simulation.
* Two harmless: the 11+ harvester confound (refuted by the test it prompted,
  which *strengthened* the row) and the invented double-count hazard.

**The policy still survives, and the reason is measurable: 24 outcome-changing
flags against 2 harms.** But *"a wrong flag costs a one-line reply"* is now
**false as written** and should not be quoted unqualified.

## Q6. FAIRNESS — conduct claims about another lane

**ZERO. Fourth consecutive quiet run.** The v1.2 sunset clause — *any question
with zero firings after three runs is struck at the next bump* — **is met.**
**⇒ RECOMMEND STRIKING Q6 at v1.3**, and the reason is information about the
lane, not failure of the question: **since the s28 rule (*"the bar for a conduct
claim is what they DID, verified"*), this lane has made none.**
**⚠ One adjacent instance to record before it goes:** I repeated *"0 built arms"*
about research's lane for **two sessions** without re-deriving it, and it was
**false** (seven tactics converted). **That is not a conduct claim — it is a
relayed NUMBER about a colleague's output — and it did the damage a conduct claim
would.** ⇒ **Q6's replacement, if any, should cover relayed figures about another
lane, not just characterisations of their behaviour.**

## Q7. WHAT DID I DECLINE, and was declining right?

**Seven. All held.**
1. **`.claude/settings.json`** on a peer's flag — harness config; **held even
   though I proposed the change and believed it right.** Magnus authorised it
   separately. *(Research declined for the same reason, stated the same way —
   neither of us being able to close it was the correct outcome.)*
2. **`HANDOVER.md`**, **`bots/`**, **`tools/` under another lane's active edit** —
   routed instead; the `target_value` fix landed in 4 minutes without a collision.
3. **The locked LOKI-42 prereg** — flagged for a new dated amendment, not edited.
4. **Every ship/rollback verdict** on v114/v115/v116.
5. **⭐ Offering further mechanism priors after the MAGAZINE BURST error** — told
   research explicitly *"if you want a read on either premise, ask and I will read
   the targeting code first this time."* **The one decline prompted by a
   measured failure of my own.**

## Q8. MECHANISATION — did any flag become a SCRIPT?

**TEN.** s32 was 6, s28 was 3.

`tools/slot_denoms.py` (30 cells) · `ship_watch`'s `dd_z`/`resolvable_k`/`p_null`/
`sd_pm`/`net_act_src`/`lg_age_min` + 7 cells · `cores_idle`'s pure predicate +
6 cells · `tools/leg_name.py` + registry · `queue_check`'s `STATUS:` vocabulary
and grep-promise class · `target_value`'s entry-point cells **and** freshness
header · `replay_throws`' `--selftest` + `guard_out()` across 4 decoders ·
`kidnap_fate`'s landing-capture cell + derived gate · `effective_n`'s `CEILING`
verdict · `arena.py` row persistence.

**The practice is unchanged from s32 and it is the whole explanation: FLAG THE
DEFECT WITH ITS FIX.** Every one arrived with a buildable replacement.
**s33 adds a second condition, learned from the two harms: THE FIX MUST NAME
WHAT IT WAS VERIFIED AGAINST.** My two harmful flags carried fixes too — they
just carried an *unverified premise* underneath.

---

## THE LEDGER

> **Prevented: 24. Caused: 2. Nearly caused: 1.**

**Prevented, largest first:** the mandated pre-prereg gate restored before any
prereg quoted it · a data-destroying `argv` signature closed across 3 unguarded
decoders · the crash-channel road closed on the right aggregation (and team `S`
surfaced) · LOKI-43's shard declined before burning ~3.5 machine-hours ·
`kidnap_fate`'s silent-null path controlled · the queue floor made honest twice.

**Caused: 2** — MAGAZINE BURST's misdirected measurement, SURCH30's cancellation.
**Both from asserting a premise I had not verified, inside a flag that otherwise
followed every rule this lane has.**
