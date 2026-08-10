# PREREG — LOKI-14b: BORDER-THROW CRASH INDUCTION, AGAINST MEASURED CARRIERS

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
