# PREREG — LOKI-14b: BORDER-THROW CRASH INDUCTION, AGAINST MEASURED CARRIERS

**PROVENANCE: corpus/archive cut** — the bimodal border-hazard census
(`docs/research/crash-induction-targeting-2026-08-10.md`), which found four teams
carrying 2,401 undamaged border removals against ZERO off-border — **plus an
engine binary read** for `can_launch`'s absent team check and absent vision guard
(`docs/research/engine-source-crash-and-launcher-2026-08-10.md`).
**Nothing in `docs/research/tactics/` spoke to this plank.**

*(Field added on Magnus's ruling, 2026-08-10: "they need to state where the idea
came from." ADD-only, so it is a legitimate amendment to an unfired prereg, and
this is deliberately the first carrier of the field so it models the format.
**The honest negative is written on its first use** — that is the clause the
field exists for. The audit that motivated it could only discover "0 of 13
preregs cite a tactics file" by counting three days later; a field that records
the MISS makes the gap visible at the moment it happens.)*

## LOCK CERT — READ THIS BEFORE CERTIFYING THIS DOCUMENT

**Each section is certified by the commit that ADDED IT, not by the file's
latest touch.**

| section | commit | git author time | what it fixed |
|---|---|---|---|
| body (panel, bars, falsifiers) | `ce12795` | **2026-08-10T15:29:57+02:00** | the bars |
| Amendment 1 (carrier admission) | `6463741` | **2026-08-10T15:38:30+02:00** | the admission rule |

Platform `createdAt` of the first challenge is the second clock and is owed at
read-out. **The leg is unfired as of both commits, so both are blind.**

**WHY THIS BLOCK EXISTS — a side-lane flag on this very file (s28), and it is
about a MECHANISM, not about this document.** An in-place amendment makes a
mechanical cert ambiguous: `git log -1` returns **15:38:30**, and a naive
`--lockcert` would certify the WHOLE document — original bars included —
against that later time. Harmless here because both commits predate any data.
**The mechanism is not harmless: a genuinely post-hoc edit to a prereg would
silently re-date the original bars and still certify clean, which is precisely
what the two-clock standard exists to make impossible.**

**CONVENTION SETTLED HERE, before `--lockcert` is written, because whatever is
picked becomes what it implements:**
1. **The body is certified at `git log --diff-filter=A`** — the commit that
   created the file — never at its latest touch.
2. **Every amendment carries its own hash and author time in its header**, so it
   self-certifies independently of the file's mtime.
3. **An amendment may only ADD a constraint or fix a rule whose inputs do not
   yet exist.** Anything that loosens, retargets or reinterprets an existing bar
   is **not an amendment** — it is a new pre-registration, and it says so.

**THE BOT DOES NOT CHANGE. THE FIXTURE DOES.** Treatment is `v107` =
`bots/_v131loki14`, byte-identical to the build that fired LOKI-14. This is the
discriminating follow-up to a null whose scope was pre-committed as *"a null
about OUR panel"* — so the correct next move varies the panel and holds the bot
fixed. Anything else confounds the two.

## What LOKI-14 established, and what it did not

**Established:** across 15 matches / 75 games, **0 undamaged enemy builder-bot
removals from 150 border throws** (bar was ≥45), with a **clean placebo**
(interior arm 0/164) and the mechanism bar met **7.5×** (314 kidnaps decoded).
The prereg's structural escape did not apply — every map produced border throws,
launcher edge-margin ≤4 for 278/314 — so **the null cannot be attributed to
under-dosing.**

**Not established:** that border-throw crash induction fails against the field.
The motivating census is **bimodal**, and our five-team panel sits entirely in
the immune half.

| team | undamaged removals | hazard on border /10k | hazard OFF border /10k | verdict |
|---|---:|---:|---:|---|
| vjg | 1,517 | **450.71** | **0.000** (0 / 560,750) | boundary-gated |
| Troupe | 345 | **146.43** | **0.000** (0 / 688,735) | boundary-gated |
| Ship Happens | 246 | **111.55** | **0.000** (0 / 441,970) | boundary-gated |
| S | 293 | **105.06** | **0.000** (0 / 642,562) | boundary-gated |

**Pooled: 2,401 undamaged removals in 107,159 border builder-rounds (224.06/10k)
against ZERO in 2,334,017 non-border builder-rounds.** Rule-of-three 95% upper
bound on the off-border hazard 0.0129/10k; **hazard-ratio lower bound ≥17,432×**.
**Every one of the 2,401 was standing on a border tile** — 1,517/1,517 vjg,
345/345 Troupe, 293/293 S, 246/246 Ship Happens.

**None of these four is on the panel LOKI-14 was fired at.** That is the entire
reason this leg exists.

## Panel

| team | id |
|---|---|
| vjg | `4a7f4c9a-6bbd-4883-891c-cf095331b592` |
| Troupe | `43a1e488-543d-4d51-a066-4f9bf039d1fb` |
| S | `a6273fb2-53e4-45dc-bcb1-d4067dd34f2e` |
| Ship Happens | `05686428-b33b-4e07-a619-13a35a9782f2` |

Ids resolved from `corpus/league_matches.tsv` (`teamAId`/`teamBId` joined on
name); **each name resolved to exactly one id, no ambiguity.** Same five pinned
maps as every other leg.

**Target: 25 matches (125 games), ~6 per carrier.** Pooling is the default now,
not a luxury.

## PRIMARY BAR — and it is a mechanism count, not a currency

**Undamaged enemy BUILDER-BOT removals within 3 rounds of a BORDER throw**,
decoded from the wire by `tools/crash_census.py`, with the **within-leg INTERIOR
throw arm as placebo**. Identical estimator to LOKI-14; **no estimator may be
selected after the data is seen** (D33).

**Expected dose:** LOKI-14 delivered 150 border throws in 15 matches, so 25
matches projects to **~250 border throws**. At the carriers' pooled border hazard
of 224.06/10k and a deliberately conservative **one-round-exposure floor**,
that is **λ ≈ 5.6**, i.e. **P(0 | carriers behave as measured) ≈ 0.4%.**

* **CONFIRMED** if border-arm undamaged removals **≥ 5** with the interior arm
  at ~0. That is roughly the point estimate the census predicts and it is
  comfortably separated from the interior arm's observed 0/164.
* **REFUTED** if border-arm removals **= 0** with **≥150 border throws
  delivered**, a clean interior arm, AND the natural-crash control below showing
  the carriers still crash. **That combination closes the road for real** — not
  for our panel, for the mechanism.
* **ANSWERED NOTHING** if fewer than 150 border throws land. I will write that
  sentence rather than read a contrast out of an undosed leg.

## THE CONTROL THIS LEG HAS AND LOKI-14 DID NOT: NATURAL BORDER CRASHES

The carriers' hazard was measured on **archived ladder replays**. A team may have
**patched the bug since**. Absent a control, a zero would be uninterpretable —
mechanism failure and opponent-patched look identical.

**So the same replays are decoded for the carriers' own border crashes NOT caused
by our throws** — their builders that walk onto a border themselves and vanish
undamaged. This is free: same decode, different filter.

| natural crashes | thrown crashes | reading |
|---|---|---|
| **> 0** | 0 | **the mechanism genuinely fails on thrown bots** — a real refutation, and it implies the throw does not reproduce the state their own pathing does |
| **0** | 0 | **the carrier has PATCHED.** The leg is uninformative about the exploit; it re-dates the census, and it must not be written up as a refutation |
| > 0 | > 0 | confirmation, with a rate comparison available for free |

**This is the check whose absence made LOKI-14's zero ambiguous, and it is
cheap.** Pre-committing it because a zero is the likeliest single outcome and
this is what decides how it may be written.

## Falsifiers for the instrument, not the plank

1. **Interior placebo > 0** ⇒ the instrument is talking, not the exploit.
   Reported FIRST, before any other number, exactly as in LOKI-14.
2. **`crash_census.py --selftest` must PASS and be reported before any number it
   produces** (positive control fires, negative control silent).
3. **Throws are attributed from the wire**, never from our own
   `LOKI14 KIDNAP arm=` print stream — **that stream does not exist in platform
   replays** (stdout empty in 30,664/30,664; `CLAUDE.md` corrected s28, D35).
4. **Our team is established per match from `meta.json`, never from seat.**

## Cost, stated in advance

Unlike PANEL2-CAL, this leg **requires activating v107**, so it costs holder time
and whatever ladder pairings land inside the window. Measured precedent: v103,
v104 and v107 each played **zero** rated ladder matches across their legs.
Protocol: serve the rate-limit wait with **v104 live**, activate only in the
instant before firing, roll back and **VERIFY THE HOLDER** (`fcode status`
`Active bot:` field — never the exit code, s27 D26).

**Rate limit is 5 test/unrated matches per 20 MINUTES** (corrected s28 off the
CLI). 25 matches ⇒ ~5 windows ⇒ ~100 minutes of wall clock. **This leg does not
start until PANEL2-CAL has finished spending that budget.**

## What this leg cannot do

It cannot resolve anything in the primary currency. `core_kill_share` against
four unfamiliar teams at n=125 has an MDE well above any plausible effect
(`tools/leg_read.py` now prints it), and **the currency reading is explicitly not
the bar.** If someone later quotes a win rate or a kill share off this leg, they
are quoting a number this document pre-committed to ignoring.

---

# AMENDMENT 1 — CARRIER ADMISSION, PRE-COMMITTED BEFORE THE RECENCY DATA EXISTS

**SELF-CERT: commit `6463741`, git author time `2026-08-10T15:38:30+02:00`,
committed BEFORE the research arm's per-carrier recency table existed.** That
ordering is the whole point of this amendment, so it is stamped here rather than
inferred from the file.

## Why this is being written now and not after

The body above puts the "has the carrier PATCHED?" question in the read-out, via
the natural-crash control. **The research arm pointed out it is answerable NOW,
for free, from the growing replay archive — before we spend holder time.** They
are right, and it is strictly better sequencing: a patched carrier buys an
**uninterpretable zero by construction**, and we would learn that only after
paying for the leg.

**But moving a check earlier converts it from a read-out into a PANEL SELECTION,
and panel selection after seeing the numbers is exactly the trap that built the
current five-cell panel** (`PREREG-panel2-calibration`: *"selecting a fixture
from a pooled-era number builds an instrument that cannot move"*). If I wait for
the recency table and then decide who stays, I am choosing cells on the data.

**So the rule is fixed here, in advance, and the arithmetic is done before the
inputs are known.**

## The rule

Each carrier's exclusion threshold is derived from **its own** measured border
hazard, at λ ≥ 3 (so P(0 events | the old hazard still holds) ≤ 4.98%):

| carrier | measured hazard /10k | border builder-rounds since its last undamaged border removal that would EXCLUDE it |
|---|---:|---:|
| vjg | 450.71 | **67** |
| Troupe | 146.43 | **205** |
| Ship Happens | 111.55 | **269** |
| S | 105.06 | **286** |

Three outcomes, decided by the table and not by judgement:

1. **ADMITTED** — the carrier has ≥1 undamaged border removal in the archive at
   any point, AND has NOT since accumulated its threshold of border
   builder-rounds with zero events. The measured hazard still stands.
2. **EXCLUDED — PATCHED** — the carrier has accumulated **at or above its
   threshold** of border builder-rounds since its last event, with zero events.
   At 95% confidence the old hazard no longer describes it. **It comes off the
   panel BEFORE the leg fires, and that exclusion is a FINDING** (a team fixed
   the bug), reported as such — not a quiet substitution.
3. **HELD — INSUFFICIENT RECENT EXPOSURE** — zero recent events but **below**
   the threshold. **This is NOT the same as patched and must not be merged with
   it.** The carrier stays on the panel; its games are read but a zero from it
   carries the caveat that we could not have detected non-zero either.

**If fewer than two carriers are ADMITTED, the leg does not fire.** A one-cell
fixture cannot support the conclusion this leg exists to reach, and firing it
anyway would repeat D22 with a denominator of one.

## What this amendment does NOT license

It does not permit swapping in replacement opponents chosen from the same
recency scan. **Adding a cell selected on the statistic being measured is panel
selection on the data no matter which direction it runs.** If admissions fall
below two, the correct response is a new pre-registration, not a substitution.

## The fidelity gate on the incoming numbers

The research arm's decoder must **reproduce the four per-carrier hazards in the
table above** before its recency split is used for anything. **A mismatch is the
headline, not a detail to reconcile quietly** — the hazards are the entire basis
for this leg's target selection, and a decoder that cannot re-derive them is not
measuring what the census measured.

---

# AMENDMENT 2 — HOW PRIOR ART MAY AND MAY NOT TOUCH THIS LEG

**SELF-CERT: commit `3d1c691`, git author time `2026-08-10T15:44:57+02:00`,
committed BEFORE any library-mining output was read** — the mining agents were
in flight when it was written.

*(First draft of this header said the hash was "recoverable via `git log`",
which is honest and verifiable and still WRONG under clause 2 of this file's own
convention: it defers precisely the lookup a self-cert exists to prevent. Caught
by the side lane on the convention's second-ever application. A section can only
carry its own hash via a follow-up commit, which is how Amendment 1 got its
stamp too — the pattern, not an exception.)*

**This amendment only ADDS constraints, which is the only thing the convention
in the lock-cert block permits an amendment to do.** It is that clause's first
live test, and it arrived within the hour of the clause being written.

Prior art (a mined library, an archived analysis, an external write-up) is
**more admissible than our own inference because it is external and pre-existing
— but it is not exempt from the rules that govern any other input.**

1. **Prior art MAY add a constraint**: exclude a carrier, raise a dose floor,
   add a control, tighten a bar. Legitimate, self-certified as above.
2. **Prior art MAY NOT loosen, retarget or reinterpret an existing bar.** If the
   library says border crashes are rarer than the census implies and the
   **≥5 CONFIRMED** bar starts to look unreachable, **that is a NEW
   pre-registration, not an amendment.** The temptation is precisely the case
   the rule exists for: an unreachable bar is exactly when moving it feels most
   reasonable.
3. **If prior art recommends a PANEL change, the rule for acting on it is fixed
   BEFORE its output is read** — the same structure as Amendment 1 and the
   recency table. Recorded now even if the mining returns nothing, because the
   window in which a pre-commitment is possible closes the moment the output is
   readable.
4. **A library file is not live-game backing** (`CLAUDE.md` point 6 / D12).
   Prior art may re-order the queue and move confidence; **it cannot retire this
   road or substitute for the leg. A mined corroboration is not a result.**

---

# AMENDMENT 3 — ESTIMATOR ARITHMETIC, AND THE LIMIT ON HOW A ZERO MAY BE WRITTEN

**Committed BEFORE the leg's first challenge.** Hash and author time stamped by
the follow-up commit named at the end of this section, per clause 2.
**Both clauses below TIGHTEN. Neither moves the ≥5 CONFIRMED bar** — stated
explicitly because Amendment 2 clause 2 forbids an amendment that loosens one,
and an unreachable-looking bar is exactly when moving it feels reasonable.

## 3a. The body's expected-dose arithmetic cites a rate its own estimator will not produce

There are **two definitions of "undamaged" in this repo** and they differ by
**91 events (3.8%)**:

* **LOOSE** — reconstructed HP at removal > 0, so a builder damaged earlier and
  healed back still counts. **2,401 events, 224.06/10k.** This is the census
  doc's rule and it is what the body's panel table and dose arithmetic quote.
* **STRICT** — never had an `updateHp` event at all. **2,310 events,
  215.57/10k.** This is `tools/crash_census.py`, i.e. **the pre-registered leg
  estimator.**

The 91-event gap reproduces the census's own §1 note exactly (52 of vjg's
1,517 carry a negative delta somewhere in life; 1,517 − 1,465 = 52).

**CORRECTED EXPECTATION, on the estimator the leg will actually run:** at 250
border throws and the one-round-exposure floor, **λ ≈ 5.4, P(0) ≈ 0.45%**
(the body says 5.6 / 0.4%). **The ≥5 CONFIRMED bar is UNCHANGED.**

## 3b. AN UNDAMAGED REMOVAL IS INDISTINGUISHABLE FROM `self_destruct()` ON THE WIRE

**This is the load-bearing caveat on the whole control and it constrains the
write-up, not the measurement.** The natural-crash control establishes that the
carriers' **border-locked removal PHENOMENON is live today**. It does **NOT**
establish that the cause is an uncaught exception.

**So if the leg returns 0 with natural crashes > 0:**

* **LICENSED:** *"the throw does not reproduce the state their own pathing
  does."*
* **NOT LICENSED:** *"their bot crashes."*

Those are different sentences and the second is supported by nothing we can
decode. **Any read-out that writes the second one is wrong on this
pre-registration's own terms.**

## 3c. Denominator heterogeneity — read event counts, not rates

Border builder-rounds are dominated by games where a builder **parks** on a
border for hundreds of rounds; one that steps on and vanishes contributes ~1.
That is why S reads 20 events in 403 recent border-rounds against 293 in 27,888
historically — **a shift in how much parking is in the denominator, not a change
in the mechanism.** **Robust statistics for the read-out: event counts and the
fraction of games with ≥1 event. The /10k figures are the census's metric
reproduced, not a stable rate.**

## Carrier admission verdict under Amendment 1 — ALL FOUR ADMITTED

Fidelity gate **PASSED to the digit** (all four rows' events, hazards and both
denominators reproduced independently; population rebuilt from
`corpus/meta_join.tsv` and matched the census's game counts before any event was
decoded; 990 files, 0 errors).

| carrier | last natural border event | border b-rounds since | trailing-20 exposure vs threshold | verdict |
|---|---|---:|---:|---|
| vjg | 12:59:17Z | 0 | 1,216 vs 67 = **18×** | **ADMITTED** |
| Troupe | 12:59:17Z | 0 | 3,421 vs 205 = **16×** | **ADMITTED** |
| S | 12:59:56Z | 0 | 403 vs 286 = **1.4×** | **ADMITTED** |
| Ship Happens | 13:25:28Z | 0 | 3,789 vs 269 = **13.6×** | **ADMITTED** |

**Every carrier's last natural border crash sits in its most recently archived
match**, 20–46 minutes before the analysis. **The INSUFFICIENT branch never had
to arbitrate — no cell rests on an occurrence-zero**, and the two-carrier floor
clears with margin. **Version column flat for all four** (vjg v4, Troupe v1,
S v2, Ship Happens v1) against **56 of 72 teams changing version in the same
window** — so the flatness is a signal, not a dead column. **vjg's hazard is
RISING** (recent-20 ~1,060/10k vs 450 historical): highest-yield cell.

---

# AMENDMENT 4 — WHAT A **CONFIRMED** MAY AND MAY NOT BE WRITTEN TO MEAN

**Committed BEFORE the leg's first ACCEPTED challenge** (cycle 1 was rejected on
the rate limit and banked nothing; cycle 2 is due 14:10:34Z). ADD-only: it
constrains the write-up and **does not touch the ≥5 bar**.

**Prompted by Magnus asking "what's vjg? I can't see that team."** He could not
see it because **it is near the bottom of the ladder.** Ratings pulled LIVE from
the platform by the builder (per-team `match list`, latest match 13:32:59Z), not
from the ~22h-stale corpus snapshot the research arm flagged as its own caveat:

| team | live rating | version | gap to us |
|---|---:|---|---:|
| **us (OpenSverige)** | **1658** | v104 | — |
| S | 1106.8 | v2 | **−551** |
| Ship Happens | 1048.1 | v1 | **−610** |
| Troupe | 1023.4 | v1 | **−635** |
| **vjg** | **806.5** | v4 | **−852** |

## The problem this creates, stated plainly

**We selected this panel on a VULNERABILITY, and it resolved into a panel
selected on WEAKNESS.** A bot that walks its own builders onto map borders and
deletes them is a bot that loses, so the border-crash signature is plausibly a
**marker of low bot quality** rather than an independent vulnerability. That
would explain the census's bimodality directly: the carriers are carriers
because they are unpolished.

**This is the fixture trap again in new clothes — selecting cells on a property
that correlates with the outcome** — and it is the same "rich downward, empty
upward" asymmetry the tactics sweeps found from an unrelated direction.

## What is and is not affected

* **The leg is NOT stopped and its bars are NOT touched.** The mechanism
  question is real, unanswered, cheap, and worth knowing regardless of whom it
  fires on: **does a FORCED border placement reproduce what their own pathing
  does?**
* **What a CONFIRMED BUYS is what changes.** A confirmation here is a
  confirmation **against four teams rated 806–1107 while we are 1658**, and the
  entire top of the ladder (2102 / 2040 / 2000 / 1977 / 1966) is in the census's
  immune half by construction.

## Binding constraints on the read-out

1. **A CONFIRMED MUST CARRY ITS RATING RANGE IN THE SAME SENTENCE.** The
   permitted form is *"the exploit fires against teams rated 806–1107, we are
   1658"*. **The bare sentence "the exploit works" is forbidden by this
   pre-registration**, exactly as LOKI-14's null was forbidden from being
   written as "crash-induction is refuted". **If a null had to carry its scope,
   a confirmation carries its own.**
2. **A CONFIRMED DOES NOT LICENSE SHIPPING BORDER-THROWING INTO THE LIVE BOT.**
   Under `R1000_IS_DEFEAT` and a ladder currency, **an exploit that only fires
   downward is close to worthless for ranking** — we already beat these four
   comfortably. Shipping requires a separate question answered first (below).
3. **The separate question, and it is now the more interesting one:** *is there
   any opponent AT OR ABOVE our rating that carries this signature?* The census
   classified six teams as clean and **left four UNCLASSIFIED rather than calling
   them immune. That unclassified four is the set worth decoding now, not the
   carriers.** Queued as its own item; it is an archive cut and costs no
   holder time.

**Method note carried from the research arm and confirmed by the builder's own
pull:** their figures came from the most recent `rating*Before` in the corpus
(~22h stale, pre-match snapshots) and they said so rather than presenting them
as a leaderboard read. The live pull moved vjg from 855 to **806.5** — same
ordering, same conclusion, and the gap is far too large to be a staleness
artefact either way.

---

# AMENDMENT 5 — WHAT THE LIBRARY PASS ADDS, BEFORE THE FIRST ACCEPTED CHALLENGE

**Committed before any challenge was accepted** (cycle 1 rejected on the rate
limit, banked 0; cycle 2 due 14:10:34Z). **ADD-only throughout: every clause
narrows what a result may be written to mean. The ≥5 bar is untouched.**

Source: the library-consumption pass Magnus ordered. **It earned its keep on
first use, which is the answer to my own audit** — I read a 1.8% citation rate as
evidence the input was worthless; it was evidence the consumption step had never
been built. (The pass also corrects my number: **the true rate is ZERO** — 0 of
252 tactics files are referenced from any file in `docs/prereg/` or `bots/`.)

## 5a. ⭐ A CANDIDATE MECHANISM FOR LOKI-14's 0/150 — NOT A RESTATEMENT OF IT

`the-legality-mask-is-a-total-function.md` (BC2025 `RobotController.java`
javadoc, plus our own probe `bots/_probe_oov_surface` with a boundary positive
control) reports that **`is_in_vision()` and the whole `can_*` family are TOTAL —
they never raise — and `get_nearby_tiles()` with no argument returns only
in-bounds tiles.**

**If that holds, a bot that enumerates neighbours the idiomatic way is
border-immune without having written one line of anti-crash code**, and only
hand-constructed `Position.add(dir)` → `get_tile_*` is vulnerable.
**Vulnerability would then be a CODE-STYLE property** — which would explain, in
one stroke, why the census is bimodal, why it tracks the weak tail, and why our
five-team panel returned a clean zero.

**STATUS: adopted as the leading EXPLANATION, not as an established fact.**
`CLAUDE.md` independently records `is_in_vision(pos)` returning False rather than
raising, which is consistent; the generalisation to the entire `can_*` family
rests on the research arm's probe and I have not re-run it myself. **It changes
no bar here and it must be verified before it is quoted as settled.**

## 5b. THE TRIGGER IS NOT THE KIDNAP — DO NOT READ ONE AS THE OTHER

`displace-dont-kill.md` supplies the arithmetic: **killing an enemy builder
REFUNDS their +20% cost scale and frees a unit slot; throwing refunds nothing.**
So **LOKI-14's 0/150 is a null on the CRASH TRIGGER, not on kidnap.** A read-out
that treats them as one thing over-reads, and this pre-registration forbids it.
*(That file's CodinGame quotes are NOT in the INDEX quote-audit table and must
not be cited as verified; the arithmetic is ours and stands.)*

## 5c. A NONZERO INTERIOR ARM IS A CONFIRMATION, NOT A REFUTATION

Under the D17 class ruling, border-throw and stale-plan displacement are **the
same approved mechanism with different triggers.** Therefore:

**A nonzero interior arm reads as "the border TRIGGER is refuted AND a second
trigger in the same approved class is CONFIRMED" — never as "the mechanism is
refuted."**

This supersedes the reading in `bots/_v131loki14/doctrine.py:1558-1560`, which
currently says the opposite. **Note this does NOT weaken the placebo:** a
nonzero interior arm still invalidates the border-vs-interior CONTRAST, and
falsifier 1 in the body still fires first and is still reported first. It
changes only what the *interior* number itself may be written to mean.

## 5d. SCORE THE TRICK ON THE WINDOW BEFORE IT IS ANSWERED

`probing-the-target-teaches-the-target.md`: BC2020 *confused* tested a counter by
requesting many scrimmages; **the target watched the replays and shipped the
counter-counter before the deadline.** Cory Li's BC2009 crash exploit died the
same way — opponents noticed robots "mysteriously exploding" and patched before
finals. **This is the only recorded operational cost of crash induction in 252
files and it is exactly our shape: 125 games of a named exploit at four named
teams.**

**The file's own open question — whether opponents can request games against us
at will — is settled against us in our own repo:** `docs/opponents.md:356-361`
records **70 unrated matches on our account, 63 initiated by Pivot, none by us.**
**The channel is two-way and they can watch every replay.**

**BINDING: any value claim from this leg is scored on the WINDOW BEFORE IT IS
ANSWERED, never as a steady-state rate, and no chassis may be built that depends
on these four teams staying unpatched.** *(Honest counter-cut, recorded: a
rolling ladder has no deadline, so there is no last-mover advantage against us
either.)*

## 5e. The follow-on this makes urgent

Combined with Amendment 4, the addressable population is now doubly narrowed:
**teams that both (a) hand-construct off-map positions and (b) sit far below us.**
**The question that decides whether any of this is worth shipping is unchanged
and unanswered: is there any opponent AT OR ABOVE our rating carrying this
signature?** The census left **four teams UNCLASSIFIED rather than immune**, and
that set — not the carriers — is now the decisive cut. Archive work, no holder
time.

---

# AMENDMENT 6 — STOP RULE, ON MAGNUS'S CLIMBING RULING

**Committed before the first accepted challenge.** Magnus, 2026-08-10, verbatim:
*"I guess a vulnerability is not relevant if it's too far below our ELO, we care
about climbing, killing the teams above us helps us a lot."*

That is a **prioritisation directive on the currency**, and it lands on this leg
mid-flight: the carriers are **806–1107 against our 1658**.

## The decision, and it is the builder's

**The leg CONTINUES, but only far enough to buy the EXISTENCE PROOF, and then it
releases the rate budget.**

**Why not stop outright.** LOKI-14's null is ambiguous between *"the mechanism is
dead"* and *"our panel was immune"*, and **that ambiguity is the only thing this
leg exists to resolve.** Left unresolved it sits in the record permanently and
every future exploit decision inherits it. The most valuable single outcome is
arguably the **negative** one: a zero **with natural crashes present** closes the
road for real and stops us spending on it — which serves the climbing currency
directly, by deleting a seam rather than mining it.

**Why not run it to n=25.** Under the ruling, additional precision about a
downward-only exploit buys nothing for climbing, and **the rate budget is the
binding constraint on everything** — 5 per 20 minutes, shared, and PANEL2-CAL
(which repairs the instrument every currency verdict depends on) is paused at
13/25 waiting for it.

## The rule, and why it is not a loosening

**Run until the leg's OWN PRE-REGISTERED DOSE GATE is met — ≥150 border throws —
then stop and hand the budget back to PANEL2-CAL.**

The body already makes 150 the gate (*"ANSWERED NOTHING if fewer than 150 border
throws land"*). **The "25 matches" figure was a PROJECTION for reaching that
gate, never a bar.** LOKI-14 produced 150 border throws in 15 matches (~10/match),
so **4 cycles × 4 carriers = 16 matches ≈ 160 throws.** Concretely: **stop after
cycle 4, decode, and extend ONLY if the throw count is under 150.**

**This does not loosen anything** — the **≥5 CONFIRMED bar is unchanged**, the
dose gate is unchanged, and the placebo is unchanged. Stopping at the gate makes
the leg *less* likely to confirm, not more, so it cannot flatter the result.
**It is a stop rule fixed before any data, which is the only kind worth having.**

## What the ruling makes decisive, and it is not this leg

**Does ANY team at or above our ~1658 carry a nonzero border hazard?**
Archive-only, costs no holder time, and it does not wait for the leg. **If the
answer is none, the road is structurally irrelevant to climbing WHATEVER 14b
returns** — and it is then deprioritised on Magnus's currency rather than on the
mechanism. If some strong team does carry it, **that team was always the
interesting panel and these four never were.** The census left **four teams
UNCLASSIFIED rather than immune**; that set is the cut.

**Programme-level question, surfaced to Magnus and NOT decided here:** if
vulnerabilities are systematically discoverable *downward* — the "rich downward,
empty upward" asymmetry the tactics sweeps found independently — then the exploit
hunt may be mining a seam that does not pay for climbing. **That is a question
about the LOKI line's premise and it is Magnus's to answer, not a lane's.**

---

# AMENDMENT 7 — THE INTERPRETATION AT THE STOPPED DOSE. **THE BAR DOES NOT MOVE.**

**Committed before the first accepted challenge decodes.** ADD-only: it forbids
sentences, it does not touch the **≥5 CONFIRMED** bar, which stands exactly as
written.

Amendment 6 cut the dose. **I did not compute what that does to the evidence
behind the bars, and it changes it a lot.** Re-derived by the builder at the
STRICT rate (215.57/10k, Amendment 3) with the one-round-exposure floor:

| throws | λ | P(0) | P(≥1) | P(≥3) | **P(≥5)** | mode |
|---:|---:|---:|---:|---:|---:|---:|
| 250 (body's projection) | 5.39 | **0.46%** | 99.5% | 90.5% | **62.5%** | 5 |
| 150 (Amendment 6's gate) | 3.23 | **3.94%** | 96.1% | 62.7% | **22.5%** | **3** |
| 160 (4 cycles, expected) | 3.45 | 3.18% | 96.8% | 67.0% | 26.5% | **3** |

## 7a. A zero is an **8.6× weaker** refutation than the body advertised

**The read-out must quote P(0) = 3.94% at the delivered dose and must NOT
inherit the body's 0.46%.** The bars are unchanged; **the evidence behind them
is not**, and that distinction is exactly what made the MDE finding matter this
afternoon. A number that was true at one dose, quoted at another, is the same
fault in a new place.

## 7b. ⚠ THE ≥5 BAR IS ACTIVELY MISLEADING AT THIS DOSE — AND THE FIX IS A WORD, NOT A THRESHOLD

**At λ≈3.2–3.5 the MODAL outcome is 3.** So the single most likely result, *even
if the mechanism works exactly as the census measured it*, is **1–4 removals:
below the pre-registered bar, while being overwhelming evidence the mechanism
EXISTS** (P(≥1 | working) = 96%; and against a dead mechanism the interior arm's
0/164 makes P(≥3) ≈ 0).

**Writing that as "not confirmed" would be the D23 failure — a plank nulling on
its own resolution floor rather than on the plank — committed KNOWINGLY, with
the arithmetic in hand beforehand.** This project catalogued D23 this morning;
repeating it after computing the numbers would be worse than the original.

**BINDING INTERPRETATION, fixed before any result exists:**

| result | how it MUST be written |
|---|---|
| **0** | the **only** outcome licensing refutation language — and still only in the scoped form Amendments 3b/4 require |
| **1–4** | **"MECHANISM DEMONSTRATED; pre-registered bar not met at the delivered dose."** The phrase **"not confirmed" is FORBIDDEN** for this range |
| **≥5** | CONFIRMED, carrying its rating range per Amendment 4, and **not a ship licence** |

**Why this is an ADD and not a loosening:** the ≥5 bar keeps its full force —
nothing below it may be called CONFIRMED. What is forbidden is the *opposite*
error: reporting a 96%-likely-under-the-hypothesis result as though it were
evidence against the mechanism. **A bar constrains what you may CLAIM; it was
never a licence to mis-describe what you SAW.**

**Credit and process note:** flagged by the side lane, arithmetic re-derived
independently by the builder before adoption. **The cut that made this necessary
was mine (Amendment 6), and I made it without computing its effect on the
evidence** — the same class of omission as quoting an MDE from the wrong
denominator, caught by another lane on the same day I catalogued it.
