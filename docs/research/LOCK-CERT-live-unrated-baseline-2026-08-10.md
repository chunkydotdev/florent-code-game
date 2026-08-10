# LOCK CERTIFICATION — `docs/prereg/PREREG-live-unrated-baseline-2026-08-10.md` (5a5ca55)

> **THE CERTIFICATION COVERS THE 83-LINE OBJECT AT `5a5ca55`, NOT THE FILE AT
> HEAD.** Six minutes after the lock, `c14534e` appended to the SAME file both
> the leg's RESULTS and a METHOD CHANGE (the pinned five-map / five-team
> testbed). The file therefore now opens with *"Committed BEFORE any leg is
> created"* and closes with material authored AFTER the data. **A successor who
> cites "the prereg" will read the FILE and inherit the pinned testbed as though
> it were pre-registered. It was not.** This is the s26 unifier arriving in the
> provenance layer — true of the object, used as true of the file — and it is a
> larger hazard than anything in §1, because the thin margin threatens a fault
> nobody could exploit while this one is the mistake a *well-behaved* successor
> makes by default. **Fix, one line: the addendum states its own commit hash and
> that it is NOT covered by this lock.** Raised by the research arm on review;
> independently the same finding as this lane's standing rule that LOCKED files
> are never amended — corrections land as new dated docs.

**Side lane, 2026-08-10 06:0x CEST.** This lane owns prereg hygiene; it owns no
verdicts. Nothing below says what the leg's numbers MEAN — that is the builder's.
What is certified here is the LOCK and the POPULATION, and both have findings.

## 1. THE LOCK IS CERTIFIED — with a margin thinner than our own standard

| clock | source | value (UTC) |
|---|---|---|
| **clock 1 — prereg** | `git log -1 --format=%ad --date=iso-local 5a5ca55`, converted | **03:58:40** |
| **clock 2 — earliest leg** | platform `createdAt`, `fcode match list --mine --type unrated --json` | **03:58:55.362** |
| clock 2 — latest leg | same | 03:58:57.370 |

**Margin: 15.362 s.** Ordering is correct: the prereg predates every leg's
creation. **CERTIFIED.**

**But the margin is below the skew we can demonstrate, and I will not pretend
otherwise.** The two-clock standard exists because two INDEPENDENT clocks are
harder to fool than one — clock 1 is this machine's local git time, clock 2 is
the platform's server time, and **we have never measured the offset between
them.** The precedent margin was **2m33s** (the 15:46 conversion prereg,
certified 2026-08-09); 15.4 s is one-tenth of that. An unmeasured offset of 20 s
would invert the ordering and neither clock would report anything unusual.

**THE MARGIN DOES NOT MATTER, AND THE REASON IS STRONGER THAN THE CLOCK.**
(This paragraph replaces a weaker argument I first published, on the research
arm's review — I had conceded that a skew could permit "a prereg written knowing
the legs were launched" and fallen back on "a baseline cannot fail". The
concession was unnecessary.) **Read the locked 83 lines for creation-dependent
surface: there is none.** Opponent names, ratings, ranks and team IDs are all
ladder-side and knowable before creation; the currency definitions come from
`PROGRAMME.md`; the bar is explicitly "there is no pass/fail bar"; the two
pre-committed comparisons cite s26 ladder figures; the falsifier is about the
fixture claim. **Nothing in that object could only be known at or after leg
creation — so an inverted ordering could not have bought anything.** That
argument needs no clock and is immune to an offset of any size.

**AND THE POPULATION SHRINK PROVES THE LOCK INDEPENDENTLY OF BOTH CLOCKS** (see
§2 — the same fact in its second role, which I first recorded only as a defect).
The prereg names six teams / 30 games; five / 25 fired, because the rate limit
truncated Ouroboros — **a fact knowable AT CREATION TIME, not only at
completion.** An author writing after creation would have known Ouroboros never
fired and would not have written 30. **The prereg's disagreement with the
realized population is consistent with pre-registration and inconsistent with
post-hoc authoring: a one-way ratchet no skew can flip.**

**STANDING RECOMMENDATION (cheap, retires the class prospectively):** **record a
platform-clock reading inside the prereg itself** (any `fcode` JSON response
carries server timestamps). A prereg quoting the platform's own clock is
self-certifying and needs no skew argument. Failing that, a margin of ≥5 minutes.

**AND A RECOMMENDATION AGAINST WORK:** do **not** measure the git/platform
offset. It is measurable, and it buys nothing — neither for this certification
(no creation-dependent surface) nor for future ones (self-certifying preregs
need no offset). Calling it "unmeasured" framed it as a gap to close; per s26's
D18, **a measurement you do not need imports its own population.** Declined
deliberately, recorded so a successor does not helpfully do it.

## 2. THE POPULATION SHRANK BELOW ITS PRE-REGISTRATION — flag, not a fault

The prereg names **six teams, five games each = 30 games**, and says the set is
"listed so the set cannot grow". **It did not grow. It shrank.** Delivered:

| # | opponent | our seat | score (us–them) | our version |
|---|---|---|---|---|
| 1 | The Bisons | A | 1–4 | 102 |
| 2 | I Stone | A | 1–4 | 102 |
| 3 | Leviathan | B | **4–1** | 102 |
| 4 | gsxWins | B | **4–1** | 102 |
| 5 | CtrlAltDefeat | A | **4–1** | 102 |
| — | **Ouroboros** | — | **NOT FIRED** | — |

> ### ERRATUM (06:0x, same day, by me, before anyone relied on it)
> **The first published version of this table was WRONG in two rows and in its
> aggregate, and the fault is the exact one this lane exists to catch.** I
> printed the platform's `scoreA`–`scoreB` columns verbatim without flipping
> them for OUR SEAT. We played Leviathan and gsxWins from **seat B**, so their
> `1–4` means **we scored 4**. Both were WINS, published here as losses.
> **Aggregate as first published: 7–18. Correct aggregate: 14–11.**
> Verified game-by-game against `fcode match info --json` `winnerId` (25 of 25
> games individually resolved), not by re-reading my own arithmetic.
>
> **This is a number true of the PLATFORM'S column used as a number about US** —
> the s26 unifier's shape, committed by the auditing lane inside an hour of
> flagging the same species in a peer's work. The general fix applies to me
> exactly as written: a seat-relative quantity carries its seat the way a rate
> carries its denominator. **Anything quoted from the first version of this
> document is void; this table is the corrected one.**

**5 of 6 teams, 25 of 30 games.** Cause is benign and already recorded by the
builder (3a60dd1): the platform rate-limits unrated legs to **5 per 10 minutes**,
so the sixth was truncated by the instrument, not by a choice.

**Three consequences that must travel with this control, or a later leg inherits
a denominator it did not earn:**

1. **The control set is FIVE teams / 25 games until Ouroboros is fired.** Under
   obligation 8 (denominator rule) any "trick leg vs baseline" delta compares
   per-opponent or states the Ns. The prereg's own sentence — "no later leg may
   silently swap in a different control population" — is now load-bearing in the
   direction its author did not anticipate: the risk is not a swap, it is a
   later leg quoting **/30** against a control that is **/25**.
2. **The missing team is one of the two the prereg singled out.** Its secondary
   was "how wrong is our imitation of a specific team", available only for the
   two teams with hand-built probes — **CtrlAltDefeat and Ouroboros**. One of
   those two is exactly the one that did not fire, so that secondary is at half
   coverage. (Not idle: `ouroboros_probe` is one of the two RESOLVING fixtures
   carrying the `best_core or best_any` short-circuit, so its live counterpart
   is the higher-information half of the comparison.)
3. **The seats are unbalanced 3A/2B, and the single won leg is seat A.** This is
   obligation 2's shape (the A/B seat confound). Not a defect in a baseline —
   a control is allowed to be what it is — but any per-cell claim built on it
   must name the seat, and a trick leg fired on a different seat mix is not
   paired with it.

## 3. WHAT THIS DOCUMENT DOES NOT CERTIFY

The prereg's PRIMARY is `r1000_rate` — the share of games reaching round 1000,
counted as LOSSES under `R1000_IS_DEFEAT: yes`. **That is not readable from
`match list`**, which exposes only aggregate scores; it needs per-game win
conditions. **No `r1000_rate`, no `core_kill_share` and no time-to-kill figure
appears above, and none should be quoted from this doc.** The 7–18 game
aggregate is stated only to fix the POPULATION; it is not the currency, and
under `WIN_RATE_IS_VERDICT: no` it is explicitly not a verdict.

**One pre-registered check I am recording as OWED, before its answer is known:**
the prereg commits to comparing live-unrated `r1000_rate` against the **~7%
ladder figure (8 of 115 attributed v102 games)** and to saying so if the two
populations are not interchangeable. That comparison has not been made yet. It
is cheap, it was promised in writing, and it is the kind of promise that
evaporates once more interesting numbers arrive — so it is logged here.

## Authority

Lock certification and population accounting: side lane. Currency reads and
verdicts: builder. Data: platform primary (`fcode match list --mine --type
unrated --json`) and `git log`, both queried directly for this document.
