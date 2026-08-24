# PROGRAMME drift watch — side-lane mandate from Magnus, 2026-08-09 ~17:0x CEST

**Magnus, directly, in the side-lane session:** *"Can you make sure we don't
drift from that? I can't keep track on the builder."* — "that" being the
programme loop he'd just had restated: iterate Loki planks, test tricks on
pre-registered unrated legs, keep what measures, lean into what kills inside
r250, Eir frozen as slot-holder.

This widens the side lane per two-session-protocol rule 5 (only Magnus can
widen a lane). The lane's other constraints are unchanged: **no verdicts, no
bot edits, no arena, no HANDOVER/tape writes.** A drift flag is a note or ping,
never a veto; escalation path is flag → builder, and if unresolved →
PushNotification to Magnus.

## The drift checklist (each item anchored to a PROGRAMME.md field or a Magnus directive)

Checked against every commit landing in the repo (session monitor, all
commits) and at every verdict/ship/leg event:

| # | drift signature | anchor |
| --- | --- | --- |
| D1 | a plank built outside the Loki lineage dirs. ⛔ **ANCHOR CORRECTED 2026-08-12 (s34): the "no edit to the frozen incumbent" clause is RETIRED — `INCUMBENT_FROZEN` flipped to `no` on 2026-08-11 (s31) and the line under development IS the line on the ladder.** Firing this row on an incumbent edit would now flag on-programme work. **What survives is the LINE check**, and note `LINE_DIRS` was widened to `bots/_v1[3-9]?*` because we stopped putting `loki` in bot names at `_v139heal`. | `LINE: loki`, `LINE_DIRS`; `INCUMBENT_FROZEN: no` |
| D2 | a battery or verdict measured against Eir (or any non-Loki baseline) instead of the previous Loki iteration | `COMPARE_AGAINST: previous_line_iteration` |
| D3 | ⛔ **INVERTED 2026-08-12 (s34) — THIS ROW SAID THE OPPOSITE OF THE PROGRAMME FOR A DAY.** It read *"a verdict argued from win rate"* is drift, anchored to `WIN_RATE_IS_VERDICT: no`. **`PROGRAMME.md` has said `WIN_RATE_IS_VERDICT: yes` and `PRIMARY_CURRENCY: game_share` since Magnus's 2026-08-11 directive**, on the arithmetic that the ladder pays `delta = 32 × (S − E)` with `S = games won / 5`. **So a game-share verdict is ON-programme and this row would have flagged it.** ⇒ **The row now fires on the opposite thing: a verdict argued from a PROXY (`kill_speed_score`, core-kill share, time-to-kill) in place of game share** — `KILL_SPEED_IS_LEG_VERDICT: no`, and `leg_read.py` prints that prohibition on the line itself. **The kill-round axis is retained for ONE purpose only: `DEFENCE_ADMISSION_BAR: kill_round_non_regression`.** | `WIN_RATE_IS_VERDICT: yes`, `PRIMARY_CURRENCY: game_share`, `KILL_SPEED_IS_LEG_VERDICT: no` |
| D4 | a plank or objective aimed at surviving/clock-playing rather than killing inside the window (the struck "r1000 alive" pivot returning in any costume) | `KILL_WINDOW_RND: 250`; Magnus 16:04 correction |
| D5 | an unrated leg fired without a pre-registration locked (committed) BEFORE leg creation | Magnus "test theories using unrated games"; the 2m33s two-clock standard |
| D6 | a leg's result banked without autopsy against its pre-registered bar, or an off-prediction win banked as confirmation | loss-autopsy-method; PREREG obligations 1–9 |
| D7 | a line-mix (Loki features ported onto Eir or vice versa) | PROGRAMME: "_v116thor is the last instance" |
| D8 | the programme declared over by anything other than Magnus's word or the curve crossing + ladder read | PROGRAMME exit conditions |
| D9 | a "LOKI delta vs baseline" quoted without per-opponent Ns | obligation 8 |
| D10 | a mechanism metric substituted for the currency in verdict language | obligation 5's anti-Goodhart sentence |
| D11 | a verdict resting on a saturated instrument — a plank measured only against `ouroboros_probe`/`clanker_probe` (93–97% baseline, no headroom) HAS NOT been measured; verdicts must name the probe pool and its headroom. **Second species (s26, 57dcbfd; re-scoped by ff3af92): OCCURRENCE-ZERO saturation — a plank whose mechanism never occurs on the pool (0 forward-sentinel damage in 480 games) has not been measured, and this form is worse because 100% "survival" reads as success. A defensive/survivability verdict must name the mechanism's occurrence count on the pool. SCOPE (the correction): this blindness is ARENA-only and SELF-AUTHORED — the 99.83%-at-core was a copy-pasted shortcut in five of nine probes we wrote, while 44 of 67 league teams attack buildings MORE than cores and the ladder loses us 46.9% of every turret built — so the ladder measures these treatments (slowly, uncontrolled) and the building-attacking fixture is the prerequisite for ARENA pricing specifically. And the fixture itself is trusted for "does the treatment do anything", never "how much", until its lethality is calibrated to the league median** | builder standing rule, 2026-08-09 (rush×map calibration: first read returned 95.8–100% share and NO information); retroactively weakens any prior verdict that used those two probes alone; occurrence-zero species from the LOKI-10 sizing |
| D12 | **a refutation, closure or "this road is dead" stated without LIVE-GAME backing.** Corpus statistics, local arena batteries against bots we wrote, source reads and engine probes may **PRIORITISE** a road; they may not **RETIRE** one. **CARVE-OUT, and all three clauses are required:** the closure is a **rules-level impossibility** established on the engine, AND it has **no behavioural premise** (nothing about how any bot chooses to act, ours or theirs), AND **its premise set is stated explicitly** — a claim that cannot list its premises has not demonstrated it has none. A probe establishes what happened **in the configurations probed**; generalising beyond them is inference. **AND THE CLAUSE THAT MAKES D12 USABLE RATHER THAN PARALYSING: archive evidence sends a road to the BOTTOM of the queue, never off it** — without it, every refutation becomes a permanently open item and `audit_trigger`'s analysis-outpacing-decisions signal gets worse, not better. | **Magnus, 2026-08-10:** *"Every statement needs backup from real games so we need to test everything in unrated games before we refute them... only playing on our Chambers is an echo loop, out there is the truth."* Carve-out tightened by the research arm after this lane's own cycles example failed it (behavioural premise; and out-degree 1 does not preclude cycles anyway). |
| D13 | **NOT A NEW RULE — THIS IS D11, AND THE FAILURE WAS ITS SCOPE OF APPLICATION.** D11 already says a verdict resting on a saturated instrument *"HAS NOT been measured"*; it was written about `bots/*_probe` and every lane, this one included, read it as being about the ARENA. **It is about FIXTURES.** Recorded as its own row only so a successor cannot make the same scoping error. **A fixture that is LIVE but does not RESOLVE.** A cell pinned at floor or ceiling reports the OPPONENT, not the TREATMENT: measured 2026-08-10 on the live panel, three of five cells were constant across four windows (Bisons 0,0,0,0; Leviathan 4,4,4,4; CtrlAltDefeat 4,3,4,4) and **all variance lived in two cells — a two-cell instrument wearing a five-cell denominator.** **The check is cheap and PROSPECTIVE: before adopting a panel, look at the per-cell spread of the CONTROL arm.** Ours was available after the first control window and no lane looked. | Builder, 2026-08-10, self-reported: *"we diagnosed [D11 saturation] for the ARENA and then rebuilt the live fixture with the same defect... The fixture axis is not fixed by making it live."* **D12 fixes the echo-loop property; it does not fix the resolution property. Live and INFORMATIVE are independent.** Selection criterion consequence: the panel was chosen on **rating proximity**, which does not predict informativeness — the replacement criterion is **measured mid-range performance against us.** |
| D14 | **A CLOSURE AND A POSITIVE RESULT ON THE SAME QUESTION MUST BE FORCED TO CITE EACH OTHER, or the library holds both indefinitely.** Tonight the tactics library asserted *"THE FORWARD ROAD IS CLOSED"* across nine files while the same repo held a field-wide result running directly against it (**3.6% -> 23.1%, p=1.9e-12**, `9f8280a`). **Neither document was wrong about its own population. What was missing was any mechanism that makes two documents on one question meet.** The index is that mechanism and it failed — the correction to the closure's evidentiary floor was IN the index and the nine files never consulted it. **It took an unrelated D12 sweep to notice, which is luck, not process.** Watch form: when a positive result lands, ask what closure it contradicts; when a closure is cited, ask what result would embarrass it. | research arm's formulation, 2026-08-10, adopted into this checklist at their suggestion |
| D16 | **work that does not follow the CURRENT methodology** — a leg, prereg, result-read or verdict that violates a rule already in `EXPERIMENT-METHOD-CHANGELOG.md` at the time it was committed. The method changelog is to D16 what `PROGRAMME.md` is to D1–D11: the authority the commit is checked against. **A commit that PREDATES a rule is not drift** (the rule did not exist); a commit AFTER it that repeats the fault the rule was written to stop IS. Also fires on: an in-flight leg not re-checked when a method rule lands mid-flight; a result banked without the current reading rules (write NULL; per-opponent Δ; per-match fields not poll-time tags; arrival barred from conversion where the gate spans a wide conversion range). **Enforcement is mostly `attention`** (per the enforcement ledger); the mechanisable sub-checks are the bar-null assertion and the two-freshness rule. **Meta-clause: a method rule that has never fired in an audit is itself flagged for review — the loop measures the protocol too, not only the work.** | Magnus, 2026-08-10: *"Your drift monitoring now also needs to check we are working by the latest methodology."* Extends the watch from the PROGRAMME axis to the METHOD axis; the method's own firing ledger (v3.1) is the baseline. |
| D17 | **RULED 2026-08-10 (b765b78): the boundary is TRIGGER vs MECHANISM.** A new TRIGGER of an approved mechanism fires FREELY (border-throw, stale-plan-displacement, 0-ammo-fire are all the SAME mechanism — a legal position-only mutation that makes the opponent's own state go stale and raise; the organiser question said "positions, plural and unqualified"). A new MECHANISM needs a Magnus→organisers question first. **The watch flags BOTH directions:** an unasked new MECHANISM (over-reach) AND instance/new-trigger work frozen on approval it does not need (under-reach — "a failure in the same family as shipping an unasked class", Magnus). Generalised exception-induction: APPROVED CLASS. | Magnus point-0 + the 2026-08-10 class ruling (b765b78), anchored to the approval's own wording |

| D18 | ⭐ **GENERALISED 2026-08-17 (s48), AND THE GENERALISATION IS D21(d) APPLIED TO THIS CHECKLIST ITSELF: this row was derived from OPPONENT-VERSION instances and therefore stated the mechanism as an opponent-version rule, so it covered opponent-version instances and nothing else. THE ACTUAL MECHANISM IS POPULATION MISMATCH: ANY cut comparing two groups is uninterpretable unless the POPULATION is held constant or its movement is shown — and "population" includes MAPS, OPPONENTS, SPACE, ERA and SURFACE, not only the opponent's version.** **Three instances on 2026-08-17 alone, all research's, all caught or conceded: (i) a near-vs-far repair cut comparing CONTESTED FORWARD TILES against everything else (two populations of SPACE); (ii) Sleipnir 0.529 vs v152 0.536 across DIFFERENT OPPONENT FIELDS, where Elo already performs that adjustment and raw shares do not; (iii) a "v125 first-harvester regression" that was the MAP-POOL ROTATION — 10 of 15 maps differ, and on the 5 common maps the medians are IDENTICAL.** ⇒ **CHECK FORM, one question before any before/after or A/B: WHAT ELSE CHANGED BETWEEN THE TWO GROUPS BESIDES THE THING I AM ATTRIBUTING IT TO?** ⚠ **And the tell that recurs: in all three the analyst NAMED the differing variable in the same breath as the conclusion ("on a HARDER field", "the map pool rotated") — so naming it is NOT the check; HOLDING IT CONSTANT or SHOWING ITS MOVEMENT is.** **The original opponent-version form follows, unchanged, as the first-discovered instance:** **A BEFORE/AFTER CUT ON *OUR* VERSION IS UNINTERPRETABLE UNLESS THE OPPONENT'S VERSION IS HELD CONSTANT OR SHOWN TO HAVE MOVED.** Fired TWICE on 2026-08-10 within four hours, on two different opponents, by two different lanes: the Ouroboros "frozen hard counter" (retracted — matchup improving once their version era was controlled) and this lane's Bisons "climb-band regression" (−31.4pp, p=0.0027 — killed: their v4 first appears **2026-08-09T19:22**, our v102's first ladder game **18:42**, **forty minutes apart and perfectly collinear** — all 7 v102+ matches vs their v4, none of the 13 earlier ones). **We control our own version scrupulously — every leg pins `ourver`, asserts the holder, verifies `teamAVersion` on the platform — and nothing anywhere pins, or even reads, the OPPONENT's version at analysis time.** Sub-finding, and it is why the gap survived: **`ladder_games.tsv.oppver` is NULL for all 100 Bisons games, and a null column reads as "no version change" to any cut that trusts it** — a constant column validating anything, in the one field that would have caught this. **Check form: before reporting any our-version before/after delta, join the opponent's version timeline (`league_matches.tsv` carries it; `ladder_games.tsv` does not) and report their boundary alongside ours. If the two are collinear, the delta is unattributable and must be written as such.** | research's formulation after killing this lane's finding, 2026-08-10; two independent firings the same day |
| D19 | **A GUARD'S DRIVING EXPIRES THE MOMENT ANYONE EDITS ITS FIXTURE. This is the MAINTENANCE CLAUSE on the repo's existing instrument rule** (*"a check that has never produced the other verdict has not been seen to check"*) — **that rule tells you to drive a guard once; this one says the driving does not persist.** ⛔ **A SELFTEST'S DISCRIMINATING POWER IS NOT PRESERVED BY ASSERTIONS ABOUT ITS OWN OUTPUT; IT IS PRESERVED BY RE-RUNNING THE MUTATION AFTER EVERY EDIT TO THE FIXTURE. Editing a test case silently destroys the thing the case was for, and the edited case still passes — which is exactly why it is silent.** **Measured instance, 2026-08-17 (s48): `tools/cluster_ci.py` case B was re-cut to clear a newly-added cluster-count gate, with an added `verdict_issued == True` assertion protecting it from that gate — both changes individually correct. Together they gutted the case: the mutation (swap the cluster bootstrap for a row resampler) still collapsed B's interval 53% (0.30 → 0.14), but the narrowed interval STILL STRADDLED the null, so B's assertion held in both states and the whole selftest passed with clustering removed.** ⇒ **ROOT CAUSE, and it generalises: a case can only detect a narrowing that CROSSES its null, so moving a fixture's point estimate TOWARD the null silently disarms it.** **Check form: (a) after any edit to a test fixture, re-run the mutation — do not reason about whether it still bites; (b) prefer putting the mutation INSIDE the selftest (ship the mutant, inject it, require the verdict to FLIP *and* a real width collapse), so "seen to fail" becomes a property of the FILE rather than of whoever last remembered; (c) ⚠ **a mutation-injecting case can itself be vacuous** — if it compares mutant against mutant it passes trivially while printing that the guard bites, so it must assert the magnitude of the difference, not only its direction. | this lane's formulation, s48, after re-running its own mutation at research's request and finding their v2 edit had disarmed the case; research adopted it into `cluster_ci.py` v3 and asked for it here. Sub-clause (c) is theirs, found by driving their own fix |
| D20 | **A FILENAME IS NOT A VERSION. Any claim of the form "file X does Y", made while other lanes are writing, is a claim about the WORKING TREE AT THE MOMENT YOU READ IT — and it needs a sha or a timestamp, INCLUDING claims about your own files.** ⛔ **This is D19's failure one level up, and it is NOT "wrong surface" — it is NO CLOCK ON THE SURFACE, the same class as `ship_watch` printing a healthy line off stale rows.** **Origin instance, s48: this lane audited `cluster_ci` v3, read the working tree (which already carried an uncommitted v4 fix), reported a peer's warning as unfounded, and PUBLISHED it — the peer had been right about the commit.** ⇒ **CHECK FORM: when a claim is about a specific commit, test that commit (`git show <sha>:path`), never the checkout.** ⭐ **AND THE STRONGER SUB-RULE, because `git log` is not sufficient: when a claim RESTS ON A TREE BEING FROZEN (e.g. a queue re-admission sweep reading the incumbent), verify the CONTENT HASH, not the commit history — `git log` is blind to UNCOMMITTED working-tree edits, which is exactly how the incumbent was edited twice under running shards on 2026-08-15.** **`tools/control_pin.py --check` already does this and is the instrument for it.** **Worked example, same session: research flagged that their 74/74 re-admission sweep had assumed `_v468kladturbo` was frozen without checking. Verified two ways — no commits touched it during the session (last: 2026-08-16T17:26:57Z) AND `control_pin --check` reported the pinned hash unchanged — so the sweep stands and the hole was latent.** ⚠ **Only the second check would have caught an uncommitted edit.** | research's formulation, s48, sharpening this lane's own "wrong surface" diagnosis after this lane published the error; the content-hash sub-rule and its worked example are this lane's |
| D21 | ⭐⭐ **THE UNIFIER FOR D19/D20 AND TWO MORE: THE EVIDENCE'S SCOPE WAS SMALLER THAN THE CLAIM'S SCOPE.** **Written because three lanes produced SIX instances of it in ONE session (2026-08-17, s48) with four different-looking symptoms, and separate rows would each be checked separately while a NEW instance matching none of them would pass.** ⛔ **It is ONE diagnosis with FOUR CHECK FORMS, not four rules:** **(a) A DRIVE expires when its fixture changes** — re-run the mutation after any fixture edit (**D19**; `cluster_ci` case B was re-cut and silently stopped detecting a row-resampler). **(b) A FILENAME is not a version** — cite `sha:path`, and verify a CONTENT HASH when a claim rests on a tree being frozen (**D20**; this lane audited a commit by reading the working tree and published the result). **(c) A BOUNDED READ is a claim about the BOUND, not about the file** — state the bound and ask whether the conclusion could survive outside it (this lane concluded *"`overnight.sh` writes START to the heartbeat, not the tape"* from `sed -n '97,101p'`; the refuting line was 103, and it had already appeared in an earlier grep the same lane had read). **(d) A MECHANICAL FIX INHERITS THE SCOPE OF THE DIAGNOSIS THAT PRODUCED IT** — state the MECHANISM, never the instances; a fix derived from N observed cases covers N cases and no more (research's formulation: an anchor extractor covering 69.4% of citations; a selftest seam covering one of two injection paths; a timestamp fix covering SHELL heredocs while the next failure was a PYTHON one — **each "worked" on exactly the cases that produced it, which is why each passed its own check**). ⭐ **THE TELL THEY SHARE: the claim and the evidence have DIFFERENT DOMAINS, and nothing in the output says so** — a passing selftest, a readable file, a grep hit and a landed fix all look identical whether or not their domain covers the claim. ⇒ **CHECK FORM, one question, asked before publishing: WHAT IS THE DOMAIN OF WHAT I ACTUALLY LOOKED AT, AND IS IT THE DOMAIN OF WHAT I AM ABOUT TO SAY?** ⭐ **(e) A CORRECTION INHERITS THE DEFECT IT CORRECTS, UNLESS THE NEW INSTRUMENT IS CHECKED AGAINST THE OLD OBJECTION** — *added 2026-08-17, research's formulation, on the row's first extension.* **Fixing the FINDING does not retire the INSTRUMENT.** **Origin instance, same session: research conceded that a near-vs-far repair cut compared two POPULATIONS OF SPACE rather than one population under two treatments, re-measured, and the REPLACEMENT (`deaths-in-radius`, home vs forward) carried the identical confound — the third recurrence of a shape they had already named and conceded, transmitted through the repair.** ⇒ **the confound survived being NAMED, CONCEDED and CORRECTED, because naming a confound does not immunise the next instrument against it.** **CHECK FORM: when a measurement is withdrawn for a reason, run that same reason against its replacement BEFORE quoting it.** ⚠ **BAR FOR A SIXTH CLAUSE IS HIGHER THAN THIS ONE WAS: (e) earns its place because it is a new TRANSMISSION PATH (through a fix) rather than a new failure SHAPE, and because it names a step nobody otherwise takes. A clause added per recurrence would rebuild exactly the four-rows-checked-as-four-rows problem this row exists to prevent.** ⭐⭐ **(f) AN AUDIT RATIFIES WHAT IT DOES NOT TOUCH — IN BOTH DIRECTIONS.** *Added 2026-08-17 (s48). THE SIXTH CLAUSE CLEARS THE HIGHER BAR (e) SET, AND HERE IS WHY: it is the first clause that is TWO-SIDED, and its transmission path is SOCIAL rather than instrumental — it travels through what a correction MAKES ITS RECIPIENT BELIEVE, which no tool, rule or fix in (a)-(e) does.* **⇒ THE CORRECTOR MUST NOT RATIFY BY OMISSION: correcting a detail implicitly endorses the premise, and THE MORE PRECISELY THE CORRECTION IS MADE, THE MORE CREDIBILITY IT LENDS.** **⇒ THE CORRECTED MUST NOT TREAT OMISSION AS RATIFICATION: an auditor's SILENCE on the premise is not evidence about the premise, and a claim that has just been audited is one its author is LESS likely to re-examine.** **ORIGIN INSTANCE, s48, and both halves fired on the same number:** this lane corrected a `DEFENCE_ADMISSION` diagnostic's arithmetic (*"the largest un-excluded regression is −14.6pp, not the −13.1pp half-width you quoted"*) — **right, and at the wrong layer.** `population_diff` later showed the cut's populations were mismatched (opponent mix 0.55, opp-version 0.24), and the **opponent-matched repair REVERSED THE SIGN: −1.5pp became +2.1pp.** ⇒ **the two lanes jointly produced a very precise statement about a quantity that should not have existed in that form** — the auditor never questioned the premise, and the author *"read the audit as clearance and moved on."* ⭐ **MECHANISM, and it is why the skip happens at all (research's, and it is lane-symmetric): BOTH LANES REACH FOR THE MOVE THAT IS FAST AND UNAMBIGUOUSLY RIGHT — a cheap ARITHMETIC correction for the audit lane, a cheap DESCRIPTIVE cut for the research lane — AND BOTH SKIP THE PREMISE TO GET THERE.** **One mechanism, two lane-specific costumes; filing it as two separate risks would hide that.** ⇒ **CHECK FORM, one question each way. CORRECTOR: *before correcting a number's arithmetic, ask whether the number should exist at all.* CORRECTED: *when a correction lands on a detail, ask what was NOT corrected.*** ⚠ **Same shape as the absence rule: the auditor's silence FAILS SAFE FOR THE AUDITOR and LICENSES INACTION IN THE AUTHOR.** ⭐⭐ **(g) A TOOL DOES NOT PROTECT THE HAND THAT CITES IT WITHOUT RUNNING IT — CITING AN INSTRUMENT IS NOT INVOKING IT.** *Added 2026-08-17 (s48), instance research's, judgement this lane's. ADMITTED FOR ONE REASON AND IT IS DECISIVE: **THIS CASE DEFEATS THE ROW'S OWN CHECK FORM.** (a)-(f) are all cases where the qualifier was MISSING and "nothing in the output says so"; **here the qualifier was PRESENT AND FALSE.** A reader applying D21's question — *what is the domain of what I actually looked at?* — answers **"the tool"**, because the citation told them so. **A case that defeats the row's own diagnostic must be in the row, or the row certifies it.* **ORIGIN INSTANCE:** research recorded the SPLITTER dead and led with *"belt is 24.4pp of our ~180pp scale, so doubling it is +24pp — `scale_trace --price 24` puts median+24 at roughly p78: LARGE, top-quartile."* ⛔ **They ESTIMATED it. They did not RUN it. IN THE SAME SENTENCE THAT NAMES THE TOOL.** **Run, it is `p68.3` — ORDINARY** ⇒ **the weakest of their three arguments was leading, and the tool built four hours earlier to stop an adjective standing in for a percentile was cited BY NAME while an adjective stood in for a percentile.** ⭐ **AND THE MECHANISM IS WHY THIS FAMILY IS HARD RATHER THAN CARELESS (research's, and it generalises past tools): THE ESTIMATE WAS IN THE RIGHT DIRECTION, WHICH IS EXACTLY WHAT MADE IT FEEL SAFE TO TYPE.** ***A wrong-direction guess feels wrong. A right-direction guess with the wrong magnitude feels like knowledge.*** ⇒ **CHECK FORM: a cited number must be a PASTED number. If the tool's name appears and its OUTPUT does not, the citation is decoration.** ⚠ **AND FOR A REVIEWER: a tool name in a claim is the CHEAPEST thing to verify and the LEAST likely to be verified, precisely because it reads as the rigour already having happened.** ⚠ **RELATED, NOT A CLAUSE, and worth keeping beside it because it was equally available here: *"the only users are weak teams" is NOT evidence a primitive is bad — it is equally consistent with "only weak teams have tried it".* Research separated the arithmetic from the company it keeps explicitly, and guilt-by-association is the cheapest possible way to close a road.** ⚠ **RIDER (2026-08-17, s48) — NOT AN EIGHTH CLAUSE, DELIBERATELY: A GAP NAMED FORWARD IS NOT A GAP CLOSED BACKWARD.** **This lane identified at 07:03Z that its wake paths watched only FAILURE events and armed a completion watch — and did NOT go back to audit what the gap had ALREADY cost.** **It had cost a number: the strict regime's record was reported as *"2 data-correct + 2 policy-correct"* — four stops — when TWO ARMS HAD PASSED THE SAME LOOK unseen, making it 3 stopped of 5 and the regime DISCRIMINATING rather than CULLING.** ⇒ **the figure had been repeated to Magnus more than once in the hour between naming the gap and auditing it.** ⇒ **CHECK FORM: WHEN A BLIND SPOT IS FOUND, AUDIT WHAT IT HAS ALREADY LET THROUGH BEFORE CLOSING IT — the closing is the cheap half and the retrospective sweep is the half that recovers the damage.** **Filed as a rider rather than a clause because the VENUE is unchanged (an instrument's domain narrower than the claim's) and only the REMEDIATION is new; a clause per recurrence would rebuild the problem this row exists to prevent.** ⚠⚠ **AND THIS ROW MUST STATE ITS OWN SCOPE OR IT COMMITS (d) IN THE ACT OF DEFINING IT: it is generalised from SIX instances on ONE DAY across THREE LANES of ONE PROJECT. The MECHANISM is claimed; the RATE, the durability and the coverage are not. A seventh instance matching none of (a)-(d) is expected, not anomalous — and finding one is evidence the row is working, not that it is wrong.** | this lane's consolidation, s48, written at research's explicit request after they produced four instances and judged themselves the wrong party to decide whether it was one rule or three. (d) is research's formulation; (a)/(b) are D19/D20; (c) is this lane's, from its own two published errors. The builder independently proposed the same unifier from a fifth instance (retiring an inherited unstarted-rows list without re-deriving it) |

## Standing notes

- **THE UNIFIER (s26, f5c26e2, read first):** most notes below are instances
  of one fault — a number true SOMEWHERE used SOMEWHERE ELSE (subject,
  denominator, clock, fixture, era, view, capacity, window). The one
  structural fix: **measure both sides of a comparison inside the arm being
  tested; never size anything on a stored figure.** When auditing, before
  itemising which rider a claim violates, ask the unified question: was every
  number in this claim measured on the thing the claim is about? **Boundary
  (2278544): two failure kinds sit OUTSIDE the unifier and need their own
  checks — (A) symbol identity across forks: a grep returning nothing in one
  fork is ambiguous between "behaviour absent" and "name differs"; verify the
  identifier exists in both trees before comparing behaviour through it; (B)
  arithmetic of aggregation: a per-unit rate rules nothing out until you ask
  how many units (seven gunners × 7 ≥ 40 — multiplicity, not mechanics).**

- `tools/gate.py` already refuses off-programme **batteries** (D1/D2 at
  battery time). The watch covers what gate.py cannot see: verdict wording,
  unrated legs, ships, objective drift in docs and plans.
- The watch covers ALL THREE LANES including this one — my own docs are
  checked against D4/D9/D10 the same way (this lane has already had to strike
  its own r1000 hold once).
- False-positive policy: flag cheaply and early; a wrong flag costs a
  one-line reply, a missed drift costs a session. The builder is expected to
  answer flags with the anchor, not with compliance.
- **Us-sample claims about the field (generalised 18:1x from two same-day
  instances; supersedes the narrower transferability note):** whenever a claim
  about an opponent or the field rests on a sample containing only OUR games,
  the sentence must say so. Instance 1: sweep-12 doctrine read as describing
  our field when our field's CAD/KCM launcher use (88–94% offensive ferries)
  is the opposite. Instance 2: the side lane predicted an empty ≤r13 trigger
  cell from OUR arrival rate; the 220-game population (third parties included)
  held 51. Same failure both times — our experience of an opponent is not the
  field's. The meta.json expansion (98% attribution, 852 third-party matches)
  makes this fixable rather than a permanent caveat: prefer the full
  population, or name the us-only denominator inline. **ERA rider (s26/s27,
  ea14adf): "our archive" is an EIR archive — 92.4% of attributed our-games
  are v101-or-earlier, so any "we/our bot" figure pooled over it describes
  the dead bot unless recomputed on the live subset. FOUR standing-context
  instruments INVERT on v102 (ammo conversion, late turret production,
  banking, +1). A claim about the live tree names its era subset the same
  way it names its population. Canonical enforcement surface: the ⛔ block at
  the top of `tactics/INDEX.md`'s standing context — any plank sized off a
  library figure reads that block first, and the watch flags sizings that
  did not.** **Freshness rider
  (s26, from research after the meta_join incident): "prefer the attributed
  population" pointed for ~7h at a table that did not reach the current era —
  the guidance was right and the surface was silently behind it. Before using
  the preferred surface, check its newest `completedAt` against the era of
  the claim.** (sync.py now rebuilds it every keeper cycle, 30a592d, which
  bounds but does not retire the check — the keeper is a process, and alive
  is not working.)
- **`audit_trigger.py` is half-blind to the research lane (research
  self-flag, 18:2x):** its `note:verdict` row reads the tape, which research
  never writes, so "analysis outpacing decisions" — the exact failure the
  trigger exists to catch, and research's characteristic one — is invisible
  to it on that lane (33 research docs added today; trigger reads 0/4).
  Flagged to the builder (`tools/` is theirs). **FIXED same day (389c2ea):**
  the instrument now covers the two blind lanes and every row is proven able
  to fire. The manual seam check is retired; the lesson stays: "a guard with
  a blind spot reads as verified absence" — when adding a lane or surface,
  ask what the existing instruments cannot see about it.
- **Mid-run sharpenings to a live agent are a pre-registration channel** (used
  4× today; both load-bearing constraints of the lockout cut arrived that
  way) — WITH the durability rider: a SendMessage predates the result but
  dies with the session, so the sharpening must also land in a committed
  line (coordination or the doc's PRE-COMMITMENT section, as the lockout doc
  did) for the pre-commitment to survive a reboot. An uncommitted
  pre-registration is only pre-registered until the context compacts.
- **Stating a rule in a document does not enforce it in that document (s26,
  40a2f75, fourth instance of the number-carries-subject family in two days):**
  research's pricing brief listed "a number carries a subject" as a hard rule
  with the 2.68 worked example, then relabelled an our-games number as the
  field's two paragraphs later. The enforcing thing was an external reader
  with the primary open. Consequence for this watch: an audit verifies the
  NUMBERS against their primaries; checking that the right rules are CITED
  verifies nothing. Corollary from the same session, on the auditor's own
  lane (e4f71d6): a wake path is verified when its alarm has been shown able
  to fire, not when its process appears in `ps` — alive is not working
  (ship_watch D13: no restart-on-OK, so `SHIP_ALERT` absence was decorative
  for its whole first life). Second corollary (s26, research's awk retraction,
  4901b5a): **discipline attaches to labels, not to function** — the guard
  written for the thing called "monitor" and the guard not written for the
  thing called "quick check" were minutes apart, by the same lane, in the
  session it was teaching the standard. Anything whose output gets published
  is an instrument, whatever it is called; a one-liner that feeds a claim
  gets the same corrupt-the-input treatment as a monitor.
- **An alarm that cannot fire before another alarm is not redundancy, it is
  decoration (s26, 4901b5a, generalising the builder's SPRT-dominance
  derivation):** a redundancy claim needs an ordering argument — under what
  trajectory does THIS alarm fire FIRST? If no such trajectory exists, its
  silence carries no information and must not be read as a second opinion.
- **A verification that shares the failure mode of the thing it verifies is
  not a verification — FOUR instances s26, and the family now has its
  general fix (supersedes the bare "corrupt the input" phrasing, which
  remains the usual construction):** ship_watch's alarm on a dead channel;
  the cwd-poisoned `git show` confirming the cwd-poisoned conclusion (D15);
  the first restart-on-OK fixture that the broken design also passed; and
  TRAP 8, where a constant-zero column met a threshold TRIVIALLY rather than
  wrongly — a constant column validates anything. **The general fix: run
  every check against a case where it MUST come out the other way** (the
  complement-group control; the mutation test; the corrupted tape). A check
  that has never been seen to produce the other verdict has not been seen to
  check. **And the correction is not exempt from the standard it enforces** —
  the D15 fix itself cited a hash produced from memory that does not exist
  (5e6e4e1, verified absent by both lanes); a forensic note that cites a
  hash has run `git cat-file` on it, exactly as a number carries its
  denominator.
- **The two turrets do not share a targeting predicate (engine-probed,
  81c0ada):** gunner `can_fire_from` is False on every EMPTY tile (0/8 at
  every offset, including on-axis inside range); sentinel returns True on the
  same tiles. Any bot code or corpus cut treating gunner and sentinel
  targeting as one predicate is wrong for one of them — audit for this trap
  in facing/siting analyses and battery treatments.
- **What "independent confirmation" can and cannot certify (s26/s27 seam,
  2727367):** a different data path over the SAME sample controls for decoder
  error, NOT sampling error — it confirms the path and reproduces the
  over-estimate. Companion family: **an estimate published at the n where it
  looked largest** (dose-response +51.6 at k=12 → +27.9 at k=20). The defence
  is not a better test; it is re-running the same test as n grows and being
  willing to lose the finding. When this watch grades a claim "independently
  confirmed", it asks WHICH error the second path was independent of.
- **Fixtures are versioned, never edited in place (s26, f1896ff):** a fixture
  is the same kind of object as a LOCKED prereg or the deny-listed arena.py —
  editing one in place silently makes every future measurement incomparable
  with every banked one, under an unchanged name. Corrections ship as new
  variants (`cad_probe2`) beside the frozen original. **The watch flags any
  in-place edit to an existing probe/fixture file as drift** (same family as
  D5's lock discipline). Corollary from the same commit: defer instrument
  surgery when the context budget is spent — "doing it at 01:1x is how a
  fixture gets edited badly" is itself the discipline.
- **Cost the fix, not only the defect (s27, f50496e):** every pre-s27 ranking
  priced the defect and never the fix; costed on both sides the top repair
  class CHANGES SIGN (+411 aimed vs −223 unconditional — same idea, one
  upstream walk apart). When auditing a plank selection, require both columns:
  what the defect costs AND what the fix costs, in the same currency, on the
  same population. A refusal-shaped plank passes trivially (fix ≈ 0), which
  is part of why refusals keep winning on this line.
- **An IN-FLIGHT entry is a claim about process state, and it is verified
  against ListAgents, not memory (s27, 2ea05ce):** research announced a cut,
  reported it running twice, and had never spawned it — the commit landed,
  an interruption intervened, the launch step was skipped, and the registry
  carried a fiction. Status reports about one's own agents check the process
  list first; the registry's integrity is what the watch audits announcements
  against, so a phantom entry corrupts the audit surface itself.
- This document is the mandate's durable record. A successor side-lane session
  boots into it via the coordination tail and MEMORY.

## ENFORCEMENT LEDGER (added 2026-08-10, research's proposal adopted) — what actually enforces each rule

**A rule everyone believes is automatic and isn't is worse than one everyone
knows needs a human.** Each D-rule is labelled with what enforces it TODAY, not
what could:

| rule | enforced by |
|---|---|
| D1, D2 (battery-time) | **script** — `tools/gate.py` refuses off-programme batteries |
| D1, D2 (verdict wording), D3, D4 | **attention** (this lane's commit watch) |
| D5 (lock before leg) | **attention** — certification is manual; the self-certifying clock makes it CHECKABLE, not enforced |
| D6–D10 | **attention** |
| D11/D13 (saturation/resolution) | **attention — NOT MECHANISABLE** (requires knowing what the fixture could have shown) |
| D12 (live-evidence + carve-out) | **attention — carve-out NOT MECHANISABLE** (behavioural-premise detection is a judgement about meaning; the cycles example passed a human read WITH the premise stated in the text) |
| D14 (cross-citation) | **attention — MECHANISABLE** (see below); its only catch to date was by an unrelated sweep |
| D16 (method-currency) | **attention** — checked against `EXPERIMENT-METHOD-CHANGELOG.md`; the bar-null and two-freshness sub-checks are the mechanisable parts, the rest is judgement |
| bar-null rule (method v3.1) | **attention — MECHANISABLE at prereg time** |
| two-freshness rule | **attention — MECHANISABLE** (monitor rows print source age) |

**Three mechanisation candidates, builder-owned (`tools/`), in value order:**
1. **D14 approximation** — flag closure-language files whose topic keywords
   appear in a newer research deliverable without cross-links. This is exactly
   how the forward-road cluster would have been caught by process instead of luck.
2. **Bar-null assertion at prereg time** — requires preregs to carry a small
   structured block (bar value, comparator base rate, source of each);
   `bar == base_rate` is one line. Would have caught 3/10-vs-29.6% pre-commit.
3. **Source-age field in monitor rows** — already specified for ship_watch.

**Precedent: `audit_trigger.py`** — a mechanical process check that fired REAL at
both lanes' boots tonight. These would be siblings.

**And the instrument rule applies to the fix itself:** each script must be run
against a case it MUST flag before its silence means anything — **one script with
a proven negative control beats three that have never flagged anything.**

- **A red test is evidence of a defect, not evidence of WHICH defect (s28,
  c347ec7, builder's formulation, adopted):** `test_does_not_fire_on_a_normal_
  shipping_day` went red because its FIXTURE rotted (literal dates aged out of
  the check's now()-24h window), and the red was read as proof the CHECK was
  miscalibrated — then promoted into HANDOVER as an instrument fact and into
  an audit brief as scoping grounds. Pinned to a fixed clock the check was
  correct in both directions all along (0.60/hr ok / 0.10/hr trips). Same
  family as preflight.py validating structure-not-identity, except the false
  certification travelled through a DOCUMENT. Watch form: when a red test is
  cited as evidence about the thing it tests, ask what else could be red —
  fixture, harness, clock — before the component named in the test's title is
  convicted. Corollary applied same-commit: the de-live-ification repair of
  s26 pinned `hours` and row contents but left timestamps live — a fix for
  wall-clock coupling that reintroduced it one layer down; a repair against a
  failure class is verified against the CLASS, not the instance that prompted
  it.

- **A bar names its ESTIMATOR, or it can be met and missed by choosing one
  afterwards (s28, LOKI-16 read-out, D24 family):** the ring-hold mechanism
  bar (≥ +0.08 coverage) reads +0.086 game-mean (MEETS), +0.076 round-weighted
  (MISSES), +0.084/+0.085 equal-cell (MEET) — all four within 0.010 of the
  bar. Prereg obligation going forward: the bar line carries its estimator and
  its clustering unit, pre-committed with the number.

- **A fixture cell must ADMIT the mechanism, on every axis including the MAP
  (s28, LOKI-16 read-out — D13's disease on an axis nobody audited):** one
  panel map has corner-anchored cores so the 12-tile ring clips to 5 — the
  plank's geometry does not exist there; 20% of the leg measured a mechanism
  on terrain where it is undefined and dragged +0.117 to +0.086, across the
  bar. Split by admission: 12-ring maps +0.117; clipped map −0.039 (sign
  reversed). Prospective check joins D13's: before a leg, verify each cell —
  opponent AND map — can express the treatment. Partial clips (9-10 tile
  rings) dilute silently; a binary split does not catch them.

- **Platform-downloaded replays STRIP print() output (s28, LOKI-14 read-out;
  instrument fact, verified 30,664/30,664 BotOutput events with empty
  stdout):** any prereg whose mechanism read plans to decode its own arm tag,
  dose counter or state flag from a live leg's replays is planning on an
  instrument that does not exist. CLAUDE.md's "print() is captured to the
  replay" is true locally and false for what the platform hands back
  (correction owed there — builder-owned). Substitute pattern from the leg:
  derive the treatment marker from WIRE state (destination tile vs map dims),
  declare super/subset direction, and sanity-check attribution (683/683
  unambiguous launchers; max d²=26 with 0 over, the documented range hit
  exactly).

- **An admission rule must match the prereg's brackets EXACTLY (s28, f48ece1,
  builder's delta, adopted):** `<= 0.20 / >= 0.80` against a prereg that
  admits `[0.20, 0.80]` inclusive threw out two cells sitting exactly on the
  boundary, halved the effective n (30/75 vs 60/75) and overstated the MDE
  (28.3pp vs 21.7pp). The sharp part: **the off-by-one moved the number in the
  direction that FLATTERS the tool** — a bigger MDE makes every leg look
  unresolvable, which excuses the instrument and is therefore the comfortable
  error. When auditing an admission or filter rule, check the boundary cases
  against the prereg's own brackets AND ask which direction the error would
  lean if present.

- **TIMESTAMPS PROVE *WHEN*, NEVER *WHAT* (s28, 9318681, builder's clause 3,
  adopted — and it generalises past preregs):** this lane flagged that an
  in-place prereg amendment re-dates the whole file for a mechanical
  `--lockcert` (`git log -1` returns the amendment; the original bars ride
  along). The fixes that make the re-dating VISIBLE — certify each section at
  its `--diff-filter=A` commit, amendments self-cert with their own hash and
  time — defend only the half that mechanises. **A cert showing two honest
  timestamps still certifies clean if the later commit quietly WIDENED a bar:
  the reader sees a correct clock beside a changed rule and has no reason to
  look.** So the restriction must be on the KIND of edit, not only its stamp:
  **an amendment may only ADD a constraint, or fix a rule whose inputs do not
  yet exist; anything that loosens, retargets or reinterprets an existing bar
  is a NEW pre-registration and must say so.** Watch form, general: whenever a
  provenance control is proposed, ask what it proves and what it merely
  displays — clocks, hashes and signatures authenticate ORDER and IDENTITY,
  never CONTENT, and a control that only makes tampering visible needs a
  companion rule that makes the tampering illegitimate. (Deliberately rejected
  here: scattering amendments into new dated docs — it defends the same
  property but fragments a prereg's bars across files, and a bar assembled
  from three documents is one nobody re-reads before firing.)

- **AN ERROR IS ONLY CATCHABLE WHEN IT BREAKS A HARD BOUND — inside the
  plausible range it is adopted (s28, 9e4085a, from the budget meter):** the
  meter's first live read was **7 of 5** spent, which is impossible and
  therefore visible; cause was `fcode match list --mine` including unrated
  matches **OPPONENTS initiated against us** (2 of 7 were Banminary challenging
  us; `triggeredBy` is the match TYPE not the actor, `sourceMatch*Id` null, so
  the platform never says who initiated). **Had ONE foreign challenge landed
  instead of two it would have read a plausible 5/5 and silently stalled every
  runner.** Watch form: when an instrument is validated by a reading that
  "looked right", ask what range of wrong readings would ALSO have looked
  right — validation by plausibility is not validation. Prefer checks with a
  hard bound the quantity cannot legally exceed, because those are the only
  ones that announce their own failure.

- **A FIX FOR A FAULT CAN CARRY THE FAULT (s28, builder's formulation, THIRD
  instance in one day — adopted):** the hardcoded MDE constant was replaced by
  a COMPUTED MDE whose denominator was chosen by the outcome — strictly better
  and wrong in the same family. Siblings the same day: the s26 `audit_trigger`
  fixture de-live-ified `hours` and left the timestamps live (wall-clock
  coupling one layer down); `map_admits`'s ring returned a self-consistent
  constant. **A repair is verified against the FAULT CLASS, not against the
  instance that prompted it** — ask of every fix: "does my replacement have the
  property I just condemned, measured on a different axis?"

- **A CONTROL GROUP REPORTED ONLY AS A POOLED FIGURE IS UNAUDITABLE ON EVERY
  AXIS ITS AUTHOR DID NOT ANTICIPATE (s28, 5295bf2 — the sharpest instance of
  "numbers carry subjects" yet, because it omits the subjects of the CONTROL):**
  `crash-induction-targeting` licenses its whole thesis — *"the border is not
  lethal per se"* — on a complement group of **six teams, 722,545 border
  builder-rounds, 0 events**, and **never names the six anywhere in the
  document.** So when the carriers turned out to be rated 806-1107 against our
  1658, nobody could ask whether the IMMUNE teams were strong: the question was
  unanswerable from the primary that raised it. **A complement group is not a
  scalar. It is a population, and it must be enumerable** — the treatment side
  gets per-team rows as a matter of course while the control is allowed to
  collapse to one number, which is precisely backwards, since the control is
  what carries the "it isn't just everyone" claim. Watch form: when a document
  cites a complement/negative-control rate, ask **WHICH members** — and if the
  answer is not in the document, that is the flag, before any question about
  what they show. Companion: apply the treatment's own admission rules to the
  control (a zero on a thin denominator is INSUFFICIENT, not immune — if the
  threshold changes the count, that is a finding about the document).

- **A STOP RULE IS A POWER DECISION WEARING A SCHEDULING DECISION'S CLOTHES
  (s28, Amendments 6/7, builder's formulation, adopted):** cutting LOKI-14b's
  dose from 250 to 150 throws touched no threshold, so nothing in the prereg's
  text flagged it — and it moved the **modal outcome from 5 (at the ≥5 bar) to
  3 (below it)**, i.e. the likeliest success would have been written as a null,
  and P(0) went 0.46% → 3.94%, an 8.6× weaker refutation quoted under an
  unchanged number. **Any change to n travels with its recomputed operating
  characteristics, or the bars silently change meaning while appearing
  untouched.** The correct repair was an ADD (forbid the sentence: 1-4 reads
  "MECHANISM DEMONSTRATED, bar not met at the delivered dose"), never a moved
  bar — **a bar constrains what may be CLAIMED; it is not a licence to
  mis-describe what was SEEN.** Author's own diagnosis, worth keeping: *"'cannot
  flatter the result' was true, and I checked only the direction that could
  embarrass me."* **Checking the self-serving direction is not checking.**

- **TEXT AND BEHAVIOUR MUST BE RECONCILED WHILE BOTH ARE CHEAP TO CHANGE (s28,
  same leg):** the prereg pre-committed *"stop after cycle 4"* while the live
  process was launched with **6** cycles. Neither is wrong on its own and the
  extra dose is scientifically harmless (stopping on dose cannot flatter), but
  **whichever a read-out later cites, the other becomes evidence the rule was
  written after the fact.** Watch form: when a document states an operational
  parameter (n, cycles, duration, thresholds), read it off the RUNNING PROCESS
  too — `ps` is a primary and the prereg is a claim about it.

- **A LOAD-BEARING PARAMETER MUST BE OBSERVABLE, NOT MERELY CORRECT (s28,
  59325e3, builder's formulation — same family as gating on `Active bot:`
  rather than an exit code):** the LOKI-14b stop was first armed as
  `STOP_AFTER=5 zsh loki14b_stop.sh`, and **macOS does not surface that
  variable in an env dump of the running process** — so the one parameter the
  pre-commitment turned on could not be VERIFIED from outside. It was almost
  certainly set; **"almost certainly" is not a control.** Re-armed as a
  positional argument so `ps` reads `loki14b_stop.sh 5`. **An unverifiable
  pre-commitment is indistinguishable from an unmade one**, and the entire
  value of this leg's seven amendments is that someone else can check them.
  **Closure worth recording: this lane verified the re-arm by reading argv
  handling BECAUSE the ps line alone was checkable — had it stayed an env var
  the check was impossible.** The fix created the audit it needed.

- **THE PATTERN BEHIND THIS LANE'S THREE CATCHES IN NINETY MINUTES (s28,
  builder's observation, adopted as a search heuristic):** the MDE denominator,
  text-vs-behaviour at 6-vs-4 cycles, and cycle-number-vs-productive-cycles
  were all **arithmetic or bookkeeping sitting under a correct-sounding
  sentence.** In each case the prose was true and the number under it did not
  follow: *"stopping on dose cannot flatter the result"* (true, and it moved
  the modal outcome below the bar); *"stop after cycle 4"* (true, and cycle 1
  was empty); *"the fixture's real MDE"* (true of a denominator chosen by the
  outcome). **This is research's D22 — verify the frame, trust the payload —
  approached from the auditor's side, and it yields a search order: when a
  claim pairs an argument with numbers, RE-DERIVE THE NUMBERS FIRST. They are
  cheaper to check and they are the half nobody re-checked.**

- **THE SEED TEXT IS THE HIGHEST-LEVERAGE OBJECT IN A LIBRARY, AND ITS ERRORS
  ARE MULTIPLICATIVE (s28, ae2882b):** `tactics/INDEX.md`'s briefing block is
  what EVERY sweep agent is briefed from, and it carried four factual errors —
  so each error was inherited by every downstream file rather than committed
  once. A defect in a seed propagates into work that then looks like
  independent corroboration. **Audit the briefing text before auditing the
  corpus it produced**, and when a library-wide defect is found, ask what
  seeded it rather than repairing files one at a time. Companion finding from
  the same audit, and the more damaging one: **the library HAS NO CLOCK** — a
  file records what was true when written and carries no marker of when that
  was, so a superseded claim and a current one are typographically identical.
  Sourcing was NOT the problem (251/252 files carry a verbatim quote, zero
  fabrications found); **provenance without a date is still unusable**, which
  is the same lesson as the prereg lock-cert convention arriving from the
  opposite direction.

- **`meta_join` IS A REPLAY-JOINED SURFACE AND IS MISSING 38% OF OUR LADDER
  MATCHES — AND THE EXISTING FRESHNESS CHECK PASSES WHILE IT IS INCOMPLETE
  (s28, found by this lane getting a number wrong):** distinct OUR ladder
  matches — **`ladder_games.tsv`: 681 · `meta_join.tsv.gz`: 420.** The gap is
  **not recency**: meta_join's newest `completedAt` (14:20:54Z) is NEWER than
  ladder_games' newest row. meta_join keys on a `file` (replay filename), so it
  covers only matches whose replays were ARCHIVED; matches without an archived
  replay are silently absent. **Consequence, measured: this lane computed the
  Ouroboros Elo bleed on meta_join and got −122.9 over 22 matches, against the
  true −301.4 over 32 — wrong by a factor of 2.5, on the number that was about
  to drive strategy.** The standing "prefer the attributed population" guidance
  points AT this surface, and its **freshness rider cannot catch this: a
  staleness check asks WHEN the newest row is, never HOW MANY rows are
  missing.** **Rule: for any POPULATION or DENOMINATOR question about our ladder
  record, use `ladder_games.tsv`; use `meta_join` for per-replay attribution
  (seat, versions, per-game winner) where the archived subset is the intended
  scope. And add a COVERAGE check beside every freshness check — compare the
  row/entity count against an independent surface, because completeness and
  recency are different failures and only one of them has a guard.**

- **THE PLATFORM'S DESCRIPTIONS ARE LESS RELIABLE THAN THE PLATFORM'S DATA
  (s28, 933c8c1 — a near-miss worth more than the check that produced it):**
  `fcode maps list` labels **all 15 pool maps `rotational`**, and our
  `CORE_PAIRS` disagreed on 8/31 entries with a MIRROR shape. This lane raised
  it as a possible live offensive defect (a wrong core guess costs ~24 rounds
  at the far end of a 250-round window). **Resolved against the wire: our table
  is CORRECT — meander's cores are genuinely mirror-symmetric — and "fixing" it
  to match the CLI's label would have BROKEN a live pool map.** Same rule as
  CLAUDE.md's *"read the engine binary, not the organisers' doc"*, on a new
  surface: **a CLI summary column is DOCUMENTATION; the replay wire is the
  ARTEFACT.** Watch form: when our code contradicts a platform label, the label
  is not automatically the authority — resolve against decoded data, and
  **never edit working code to agree with a description.** Process note in this
  lane's favour: the flag was raised with BOTH branches stated and a
  discriminating test attached, which is why the answer arrived before any edit.
  **ADDENDUM — the sharper half, and it is this lane's error:** my test asked
  *"does this table agree with a FORMULA"* when the question was *"does this
  table agree with the ENGINE."* **A record can disagree with a rule and still
  be right, if the rule is what's wrong** — and a hand-built table of
  measurements is exactly the kind of object where that is the likely reading.
  Compounding it: `CORE_PAIRS` holds **multiple entries per dimension** because
  different arenas share dimensions, so several of my "mismatches" were stale
  rows describing *other* maps, not errors at all. **Check a table's own
  structure before testing its contents**, and when auditing a record against a
  generalisation, state which one you are treating as the authority.

- **YOUR OWN CODE IS A FREE POSITIVE CONTROL FOR YOUR MEASUREMENT (s28,
  06bbe7e — the strongest instance of the check-it-both-ways rule found yet,
  and the control was sitting in the repo unused):** an exact-ray metric
  reported **0 of 319** forward sentinels shootable-on-build, and that number
  retired LOKI-17 and launched LOKI-18 on a new premise. **It was the METRIC
  that was wrong.** `raid.py` builds a sentinel **only after `can_fire_from`
  passes**, and 287 of 528 sentinels were beyond `main.py`'s reach so they came
  from that path — i.e. a large subpopulation is shootable **BY CONSTRUCTION**,
  and any predicate scoring them ~0 is **falsified by the code itself**.
  **A code path with a guard is a known-answer cell**: whatever it guarantees,
  your measurement must reproduce on its output, or the measurement is broken.
  **Check form, and it costs nothing: before trusting a new metric, find a code
  path whose guard forces the metric's answer and run the metric on it.** This
  generalises the collar-heal standard from "validate against a known published
  cell" to "validate against a cell your own source code makes known".
  Sequence worth preserving: the side lane flagged the fork (**dead path or
  broken guard?**) *because two observations admitted opposite readings and
  they had opposite consequences* — the builder ran the attribution and the
  answer inverted two decisions (LOKI-18 premise invalid, LOKI-17 un-retired).

- **DO NOT EDIT A SCRIPT THAT IS ALREADY RUNNING UNATTENDED (s28, near-miss):**
  `night_collector.sh` was launched at **23:03:47** and its retry-floor fix was
  committed at **23:04:32** — 45 seconds later. **zsh reads scripts
  incrementally, so an in-place edit can leave a long-running process executing
  from a stale byte offset.** We got away with it (the running process was
  observed asking the rate meter, i.e. the new behaviour, so the file was
  written before launch and merely committed after) — **but the ordering was
  luck, not design, and an unattended six-hour process is exactly where nobody
  would notice.** Rule: **stop, edit, restart.** Verification form when it has
  already happened: check the process start time against the file mtime, and
  confirm the RUNNING BEHAVIOUR in the log matches the new code rather than
  assuming the edit took.

- **A PREREG MUST FIX ITS n, AND THIS LANE MISSED IT (s28, LOKI-16b, self-flag
  — second prereg-hygiene miss of the day after the carrier ratings):** I
  audited `PREREG-loki16b` and reported "no flags", having checked provenance,
  the named estimator, the clustering unit, the map stratum and the reused
  control — **and never asked how many games it would fire.** An unfixed n is
  what permits **optional stopping**: fire until the number looks right, then
  stop. **No harm landed (the runner's schedule was fixed even though the
  document's was not, and the leg ran 10 challenges/50 games to completion), but
  the document did not bind it.** Add to the prereg checklist beside the bar and
  the estimator: **the planned n, and what happens if the leg is cut short.**
  Both of today's misses share a shape — **I verified everything the document
  SAID and never asked what it FAILED to say.**

- **⛔ CORRECTION TO THE NOTE ABOVE, SAME NIGHT — IT WAS NOT A NEAR-MISS AND MY
  CHARACTERISATION OF THE BUILDER WAS UNFAIR.** I wrote that the collector fix
  was an in-place edit to a running script and that "the ordering was luck, not
  design." **False. The builder edited the file and RELAUNCHED the collector** —
  precisely the stop/edit/restart rule I was writing up. Confirmed by
  observation rather than by their account: the collector's **pid changed
  4404 → 6659** across the fix, which only happens on a restart.
  **What I actually did: inferred an unsafe practice from a commit timestamp
  alone, and published it about another lane in a durable record without asking
  who had done what.** A timestamp shows WHEN a file was committed — never
  whether the process was restarted, and never who acted. **Third instance today
  of the same fault** (inferring blast radius on the +64 discrepancy instead of
  checking it; convicting `CORE_PAIRS` against a formula instead of the engine).
  **The rule stands and the builder followed it.** The lesson that survives is
  about me: **when a record characterises another lane's conduct, the bar is
  what they DID, verified — not what a timestamp permits me to infer.**

- **D14 FIRES A SECOND TIME — AND AGAIN THE CATCH WAS LUCK, NOT PROCESS (s29,
  `38bc735`, 2026-08-11):** `HANDOVER.md` carried LOKI-17 as the live next leg
  for **five hours** after its own author withdrew it in
  `docs/legs/LEG-loki17-battery-2026-08-10.md` at 22:03 (`c91c078`: *"no defect
  to fix on this evidence… its supersession is withdrawn AND SO IS THE PLANK"*).
  The builder's own words on the near-miss: *"I got within one commit of
  activating a prototype for a plank its own author had withdrawn."*
  **Two documents, one question, opposite answers, and nothing made them meet** —
  which is D14 verbatim, on a new surface (leg record vs HANDOVER rather than
  closure vs research deliverable).
  **THE PART THAT MATTERS FOR THE LEDGER: D14's enforcement row reads
  `attention — MECHANISABLE`, and its only prior catch was an unrelated sweep.
  This catch was also incidental** — the side lane was auditing a DECODER on
  commission and read the tool's git log on the way past. **Two firings, two
  accidents, zero catches by design.** A rule caught twice by luck is not
  enforced; it is being got away with.
  **Consequence, and it upgrades mechanisation candidate #1 from nice-to-have:**
  the cheap form here is narrower than the full closure-vs-deliverable crawl —
  **a plank's status must have ONE authoritative surface, and every other mention
  must be a pointer to it rather than a copy.** HANDOVER holding its own copy of
  "what fires next" is the defect; a copy cannot be stale-checked, only
  contradicted. **Watch form until that exists: before any activation, diff the
  plank's status in HANDOVER against the newest commit touching that plank's leg
  doc, prereg or tree.** That is one `git log -1 -- <paths>` and it is exactly
  what caught this one by accident.
  **Companion, same commit, worth its own line because it generalises past
  planks:** the number that WITHDREW LOKI-17 (100.0% shootable-on-build) came
  from `scratchpad/shootable.py` — **untracked**. The number that killed the
  plank and the number that would have revived it were, at that moment, both
  outside version control. **A figure load-bearing enough to retire a plank is
  load-bearing enough to be committed**; the same morning produced two more
  instances (a 33 KB audit and the five `scratchpad/ring_*.py` ring decoders).
  **This is not three incidents, it is one convention: analysis runs in
  `scratchpad/` and only its CONCLUSIONS get committed, so every load-bearing
  number in this repo is one `rm -rf` from unreproducible.**

- **THE GREEN-SELFTEST SIGNATURE, AND THE POSITIVE STANDARD THAT COMES WITH IT
  (s29, `694fc5f` — a sweep, not an incident):** the failure is **a test whose
  assertions all sit on one axis of a metric while the metric's load-bearing
  definition sits on another.** `ring_retention.py` asserted 12-on-open,
  5-in-corner, walls-reduce — the RING — and never the OCCUPANCY RULE, which was
  the broken half; it passed for its entire life while inverting a result.
  **Six confirmed instances across `tools/`, each with the input that passes the
  test and breaks the metric constructed and RUN**, including two live at the
  time of writing: `audit_trigger` suppressing its own FIRE (a 24-hour numerator
  over a denominator with no clock), and `oppver_window` returning **CLEAN — the
  verdict that certifies D18 — off a stale tape**, on the very opponent its own
  docstring uses as the worked example of a cell that ships versions.
  **THE WATCH FORM, and it is cheap enough to apply at review time:** for any
  instrument, name the quantity in one sentence, then ask **which clause of that
  sentence each assertion touches.** The clause no assertion touches is where the
  defect will be. Three recurring shapes: the test builds its own copy of the
  computation instead of calling the production function (`map_admits`'s ring,
  `breakin_watch`'s `main()`); an `_OVERRIDE` hook bypasses the reader so the
  DATA is never in the test (`oppver_window`, `target_value`); and a fixture
  degenerate enough that two different definitions coincide (`audit_trigger`'s
  one-row tape, where tail-window and time-window are the same thing).
  **⭐ THE POSITIVE STANDARD — `tools/corpus/meta_attrib.py`, and it should be the
  template anyone copies:** three corruption modes, each aimed at a DIFFERENT
  check, each mutating **the real pipeline's own rows** rather than a fixture,
  each requiring agreement to COLLAPSE. Its third mode exists because the first
  two only proved CHECK 1's teeth — **it reasons about which check each
  corruption reaches.** Siblings that meet the bar: `score.py` (both sides of
  every boundary, and tiebreak asserted IDENTICAL to a loss — the semantic, not
  the number), `rate_budget.py` (**the blind state must REFUSE, not permit**),
  `claim_check.py`, `plank_status.py`. **What all five share: they call the
  PRODUCTION function, they assert semantics rather than shape, and they drive
  the check to the verdict that is UNCOMFORTABLE.**
  **And the category that may outrank every finding: 41 of 56 `__main__`-bearing
  modules under `tools/` have no selftest at all** — including
  `replay_census.py`, whose wire primitives every corpus decoder imports, so one
  defect there moves every number in the repo. **An instrument with no test is
  not a smaller problem than one with a blind test; it is the same problem
  without the false assurance.**

- **⭐ A CHECK ONLY CHECKS ONCE SOMETHING FORCES IT TO PRODUCE AN ANSWER IT COULD
  GET WRONG (s29, 2026-08-11 — four independent instances in one session, which
  is why this is a standing note and not an incident):**
  1. **Six selftests passed while their metric was broken.** Each asserted one
     axis of its quantity and never the clause that was wrong — `ring_retention`
     asserted the RING and never the OCCUPANCY RULE, and inverted a result for
     its whole life.
  2. **`claim_check.py` was silent on `unrated_run.sh` for an hour** — not
     because the guard was tested, but because **the file made no claim to
     check.** The moment the claim was written, the checker went red and the
     boot suite failed. **Silence from a checker whose predicate was never
     triggered is not evidence.**
  3. **The holder-assertion ABORT branch — the guard against putting a prototype
     on the rated ladder — had never been driven** in its fourth copy. Driving it
     took one command and a `MAIN=999`.
  4. **`hold_any` named a statistic no tool computed.** Three lanes discussed it
     for hours, agreed a definition, and made the choice between it and
     `hold_pinned` the DECIDING call of an amendment — **and the names had been
     matched to the code's two series BY POSITION, not by semantics.** It was
     caught by **building the selftest**, because a forced-answer cell cannot be
     written without stating what the number must be. Prose never had to answer.
  **THE COMMON MECHANISM: in every case the artefact LOOKED verified — green
  exit, silent checker, guard present in the source, a definition three lanes
  agreed — and in every case nothing had ever demanded an answer that could have
  come out the other way.**
  **THE WATCH FORM, and it is one question:** for any check, name the case where
  it MUST say the uncomfortable thing, and ask whether that case has ever been
  run. If the answer is *"it would"* rather than *"it did, here is the output"*,
  it has not been checked. **Applies to selftests, boot gates, abort branches,
  linters, and agreed definitions alike.**
  **CONSEQUENCE FOR THIS LANE SPECIFICALLY:** an audit that ends *"no flags"*
  has usually verified what a document SAYS. **Three times on 2026-08-11 this
  lane closed an audit with "no flags" and had to reopen it** — the arrival
  premise, the undefined `materially` in a falsifier, and an untracked decoder
  under a tracked broken twin. **Each was an omission, not an error**, and each
  was found by asking what the document did not force itself to answer.

- **TWO FINDINGS PROMOTED FROM THE s29 SIDE-LANE RETRO, because a retro instance
  is not in any boot path and a finding that stops there is unread by
  construction (retro v1.1's routing rule, `3821770`):**
  **(a) CONSUMPTION IS PER-ARTEFACT, NOT PER-LANE — and the artefact with the
  most findings had the worst rate.** Measured s29: every SINGLE-FLAG message to
  the builder was actioned within minutes (twelve of fourteen changed an
  artefact the same session), while the **six-finding sweep document was
  consumed 2 of 6 — and the four left open included the two LIVE defects**
  (`audit_trigger` suppressing its own FIRE on every builder boot;
  `oppver_window` certifying D18 CLEAN off a stale tape). **A finding's chance
  of being fixed appears to fall with the number of findings shipped beside it.**
  **Practice: ship the LIVE findings as their own message and let the rest be a
  document.** A six-item report competes with itself for attention, and the
  items that lose are the ones already costing something.
  **(b) THE MECHANISM THAT MOVED SELF-CATCHING WAS NOT DILIGENCE.** This lane's
  own-error catch rate went **0 of 8 (s28) to 4 of 5 (s29)**, and the cause was
  **running a SECOND INSTRUMENT over my own claim** — a blind subagent
  replication that corroborated an adjudication and simultaneously dissolved my
  own flag; a mutation run against a selftest I had just praised; a platform
  read against a corpus that turned out not to reach the window. **In every case
  the first pass was careful and wrong, and the second pass was mechanical and
  right.** **Practice: before publishing a claim about someone else's
  instrument, run a different instrument over your own claim.** This is the
  auditor's version of "your own code is a free positive control", and it is the
  only thing that has moved this lane's blindest number.

- **⭐ D18b — THE OPPONENT-VERSION RULE HAS ONLY EVER BEEN ENFORCED ON THE
  OUTCOME AXIS. IT APPLIES TO THE *ADMISSION* AXIS TOO, AND THERE IT HAS NEVER
  ONCE BEEN APPLIED (s30, 2026-08-11; research's formulation, adopted and
  promoted here because their instance file is not in any lane's boot path):**
  D18 says pin the opponent's version before reporting an our-version before/after
  delta. Every enforcement to date has been on a **win-rate or currency** read.
  **But a CELL-SELECTION decision is computed on opponent data too, and nothing
  in this checklist reached it.** LOKI-19's Amendment 2a demoted the SmartFridge
  cell on an arrival figure of **7.6% over n=512** — measured s30 to be **pooled
  across THIRTEEN of that opponent's versions, 60% carried by their v30 alone
  (311 of 516 inserts), a version they no longer run. The leg actually faced v57
  and v67, which contribute 5 inserts and 0 to the pooled number.** The statistic
  that chose the panel was about a bot that was not on the other side of the leg.
  **AND THE DIRECTION KILLS THE COMFORTABLE READING: version-pinned, three of
  five cells read HIGHER than pooled** (Lunds 23.6→30.0, Askar 30.8→42.9,
  Landers 63.9→71.7). **So this is not pooling that flattered the plank — it is
  pooling that was never a defined operation on that axis.** A defect that moves
  numbers in both directions is not a bias to correct; it is a quantity with no
  meaning, and those are harder to notice precisely because they do not offend.
  **CHECK FORM, prospective and free off the archive: any figure used to ADMIT,
  DEMOTE or SIZE a cell carries the opponent-version decomposition that produced
  it — the same way an outcome delta carries its denominator. If the pooled
  figure and the version-pinned figure disagree, the version-pinned one selects
  the panel, because that is the bot the leg will meet.**
  Corroborated from two independent surfaces the same hour, which is why it is a
  rule and not an anecdote: research off `replay_archive/*.meta.json` +
  `throws.tsv`, this lane off `league_matches.tsv` (four SmartFridge versions in
  the 4.5 h before the leg window, one team id, no name collision). Neither
  needed the other's number.

- **⭐ MAGNUS, s30 2026-08-11: *"We have been known to be scouted now and then."*
  THIS DEMOTES D18's CONTROL FROM A CONFOUND TO AN EFFECT, and the difference is
  not pedantic.** D18 was written around the Bisons kill, where their v4 landed
  forty minutes before our v102's first ladder game and the two timelines were
  *"perfectly collinear, so both stories fit"* — collinearity treated as a
  COINCIDENCE to be controlled away. **If opponents scout us, the two version
  timelines are not independent, and the arrow may point FROM our ship TO their
  release.** Controlling for their version then removes part of the effect of our
  own change rather than a nuisance — and it is worst in exactly the cells we
  play most, i.e. the ones every panel is built from.
  **SECOND CONSEQUENCE, and it reaches the PROGRAMME rather than the method:**
  under `FIXTURE_OF_RECORD: live_unrated` every leg SHOWS a live team our
  prototype. If they scout, **a trick's measured effect decays with exposure**,
  and a re-fired leg at a cell we have already shown it to would measure that
  decay. **We would bank it as a null and close the road** — under D12, which
  requires live-game backing to retire a road, that is the failure mode with the
  worst consequences available to us: an exploit that works, tested twice, and
  retired on the second reading.
  **⇒ OBLIGATION, PROPOSED FOR THE NEXT PREREG THAT RE-FIRES A TRICK: record the
  PRIOR EXPOSURE COUNT for each cell (how many times that opponent has already
  seen this mechanism from us), and pre-commit that a null at a previously-exposed
  cell decomposes into "never worked" vs "worked, then was countered" — the two
  are not distinguishable after the fact without that number.** Nothing in the
  obligations doc asks for this today. **The cheapest possible instance is free:
  a first-exposure cell and a re-exposed cell in the same leg is the control.**

- **⛔ AMENDMENT TO THE SCOUTING NOTE ABOVE, SAME SESSION, ~25 MINUTES LATER —
  THE MECHANISM I INFERRED WAS TESTED AND IS NOT SUPPORTED AT THE VERSION-BUMP
  LEVEL** (`docs/research/SCOUTING-opponent-version-response-2026-08-11.md`,
  commissioned by this lane, `opus`, read-only over `league_matches.tsv`,
  2026-08-06 → 2026-08-11T05:52:59Z):
  **The raw association is there and the causal reading is dead.** Version-bump
  hazard is **1.46x** higher in the 6 h after we play a team UNRATED
  (team-stratified Mantel-Haenszel, 224 bumps / 5,615 treated vs 805 / 38,835
  untreated observations, 45 teams), stable at T=2 h (1.466) and T=12 h (1.428),
  **and the ladder arm — where matchmaking picks, not us — shows nothing
  (0.729 / 0.890 / 0.893).** That contrast is exactly what a scouting story
  predicts.
  **AND THEN THE EVENT STUDY KILLS IT.** On leg-initiating unrated matches (≥24 h
  since last contact, 66 events), bump hazard in the six hours **BEFORE** our leg
  is **1.471 (z +3.48)** against **1.177 (z +1.32)** after. **A hump straddling
  t=0, not a step at t=0.** Detection lags deployment, which pushes the causing
  event EARLIER relative to our leg, not later — so the pre-period elevation
  cannot be explained away as measurement lag. **An effect that appears before
  its cause is not that cause's effect.**
  Two further controls agree: the pair-swap placebo (team X given team Y's
  our-match times) **itself reaches 1.263 ± 0.175**, leaving the observed 1.460
  only **+1.13 sd** above its own placebo; and a day-preserving circular
  permutation moves p from 0.034 to **0.137**. **Much of the raw signal is our
  legs and the league's deploys sharing an evening.**
  Instrument driven both ways before use: synthetic injection fires (RR 6.53 at
  15%, 11.76 at 30%, p=0.0033); within-team label shuffle sits at 1.000 ± 0.072.
  **Denominator independently reproduced by this lane: 1,104 bumps league-wide in
  the window, minus our own 74, = 1,030 against the agent's 1,029.**
  **WHAT SURVIVES, AND IT IS NOT NOTHING:**
  1. **The obligation stands on its own reasoning, not on this mechanism.** A
     re-fired trick's null is still ambiguous between "never worked" and "was
     countered", because **the scouting CHANNEL is confirmed to exist** — see
     the next note — even though *shipping a new version within hours of playing
     us* is not how it shows up.
  2. **D18's collinearity control is NOT promoted to a causal path on this
     evidence.** My earlier note above proposed exactly that; **this is the
     retraction of the causal half.** The ladder arm is only powered to ~±1.3 sd
     against an effect of unrated size, so it **disfavours rather than excludes**.
  3. **A shared driver exists and is unidentified.** The obvious candidate is
     absent — we do NOT preferentially open legs against teams that just shipped
     (0.968 / 0.993 / 1.002 vs 2,000 random draws, us-only, n=726). Left open
     rather than filled in with a story.
  4. **DIRECTION OF INITIATION IS UNOBSERVABLE and it may invert the arrow on an
     unknown share of the 726** — `triggeredBy` is the match TYPE, `sourceMatch*Id`
     is null. **An opponent-initiated unrated match against us is plausibly
     already a scouting act.** This is the second independent argument this
     session for `SPEC-match-initiative-ledger-2026-08-11.md`, and it arrived
     from a different direction than the budget meter did.

- **⭐ THE SCOUTING CHANNEL IS CONFIRMED TO EXIST, AND IT IS SYMMETRIC — WE ARE
  ALREADY THE THING WE ARE WORRIED ABOUT (s30, measured):** `league_matches.tsv`
  is **35,642 rows of which 98.0% (34,913) are matches between OTHER teams**, and
  of the **400 most recent third-party matches we hold archived `.replay26` wire
  files for 86.** The platform serves everyone's replays to everyone.
  **CONSEQUENCE, and it is larger than the unrated question that prompted it:**
  exposure is NOT limited to the ~5 games of an unrated leg. **Every LADDER game
  is scouted material too, at ~6 matches/hour, for as long as a version holds the
  slot.** A trick shipped to the ladder is published far more widely than a trick
  fired in a leg. **So "protect the trick by not testing it" was never the trade
  — the trade is between a leg's 5 games and a ship's hundreds.** Whatever we can
  compute about an opponent from their replays, any team with a decoder can
  compute about us.

- **⭐ F4 PRICED AND THEN MEASURED, WITH THE CONTROL THAT MAKES IT UNFIXABLE BY
  ATTENTION (s30, 2026-08-11):** `ship_watch` still asserts nothing about the
  freshness of the tape it reads — the standing rule *"emit the age of the newest
  row, or refuse to print a verdict past ~2 cadences"* is in CLAUDE.md **and is
  unimplemented on the very instrument the rule was written about.**
  **EXPOSURE:** `elo_history.tsv`, 1,243 rows over 08-06→08-11, median inter-row
  gap **5.0 min** against a 10-min cadence; **ten stalls exceed two cadences,
  totalling 338 of 6,693 min = 5.1% of the tape's life, longest 50 min.**
  **THE MEASUREMENT, not the projection** — the documented 08-10 07:05→07:55
  outage, read off `ship_watch.log`: **five consecutive verdict lines
  byte-identical but for the timestamp** (`k=63 rating=1599 drawdown=-17.0
  armed=True RULE=held`), then recovery to `k=68 rating=1631 drawdown=+0.0`.
  **Five matches and +32 Elo were invisible to the ship monitor for fifty
  minutes while it reported a drawdown for a state that had already recovered.**
  **⇒ THE CONTROL IS THE POINT: the healthy stretch immediately after is ALSO
  byte-identical across two cadences (08:02 and 08:12 both `k=68 rating=1631`),
  because a quiet ten minutes legitimately produces a repeated line.** So
  repetition carries NO information in either direction, and **a reader cannot
  distinguish "no new match" from "the tape is dead" by looking.** This is the
  general form: **when a failure mode and a benign mode emit the identical
  artefact, no amount of care closes the gap — only an assertion the instrument
  makes about itself.** Recorded with its negative control because the same
  finding without the healthy-stretch comparison would have read as "watch for
  repeated lines", which is advice that cannot work.
  One of the ten stalls sits four rows after a `v103 k=1 armed=False` prototype
  rotation — **the tape goes blind in exactly the operating mode where the
  monitor is load-bearing.**

- **⭐ THE CORPUS LAGS THE PLATFORM BY UP TO AN HOUR, SO A SAME-SESSION LEG
  CERTIFICATION MUST READ THE LIVE CLI — AND THIS INVALIDATES THE SURFACE THIS
  LANE USED THIS MORNING (s30, 2026-08-11 06:5xZ):**
  LOKI-18 fired **06:46:26–06:46:42Z**. At **06:49Z**, `league_matches.tsv`'s
  newest row was **05:52:59Z — fifty-four minutes short of the leg.** The builder
  reported the leg's rated cost *"verified at the boundary"*; that was a
  **STRUCTURAL** argument (16 s of exposure sitting between the 06:32:59 and
  06:52:59 pairings) and it was correct, **but it was not a per-match
  verification, and the corpus could not have supplied one.** By HANDOVER's own
  D18 rule the honest word off a tape that short is **UNKNOWN**, not CLEAN.
  Read live instead (`fcode match list --mine --type ladder`): last pairing
  before exposure `06:32:59Z` v104, **no match created inside the window, eight
  consecutive pairings all v104 — rated cost ZERO, verified on a surface that
  could see it.** Cadence re-derived **8/8** at `:12:59 / :32:59 / :52:59`.
  **⇒ RULE: any certification about a leg fired THIS SESSION reads the live CLI.
  `league_matches.tsv` / `ladder_games.tsv` are for history, and their freshness
  must be printed beside any window they are asked about.**
  **AND THE SELF-APPLICATION IS THE POINT: this lane's own F5 certification at
  06:2xZ used `league_matches.tsv` and got the RIGHT answer — because that leg
  happened to sit inside the tape's reach. I did not check that it did.** A
  correct answer from a surface that could have been blind is not a verified
  answer; it is a lucky one, and the same procedure ninety minutes later would
  have certified CLEAN off a tape that stopped before the window. **This is the
  freshness rider applied to the certification procedure itself rather than to a
  claim.**

- **⭐ D19 (NEW) — A SUBAGENT BRIEFED FOR ONE DATA SOURCE THAT RETURNS A NUMBER
  FROM ANOTHER HAS PRODUCED AN UNREVIEWED PRIMARY, AND NOTHING IN OUR PROCESS
  FLAGS IT (s30, 2026-08-11; research's formulation, adopted and promoted here
  because their instance file is not in any lane's boot path):**
  Research briefed sweep 22 as an **external-literature** sweep. The agent also
  **computed statistics on our own corpus, unasked**, and the numbers did not
  survive re-derivation: agent **−8.00pp on 1,970 blocks** against research's
  independent **−6.55pp on 4,157**, four defensible estimators spanning
  **−4.83 to −8.75**, and the discriminating control at **t = −1.51** in one pair
  of hands versus **−0.61** in the other. **Direction and significance replicate;
  the MAGNITUDE does not, and every figure derived from it inherits the spread.**
  **THE MECHANISM: the brief is the only place the scope ever existed, and the
  output looks identical either way.** A literature finding and a corpus finding
  arrive in the same prose, with the same confidence, in the same report. **This
  is D52b's shape — a correction lands where it was discovered — arriving at the
  boundary between a lane and its OWN subagents**, which is the one boundary no
  lane audits because it feels internal.
  **⇒ WATCH FORM: when relaying a subagent's result, check whether each number
  came from the source the brief named. A number from an unbriefed source is an
  UNREVIEWED PRIMARY and must be re-derived before it is relayed, not after.**
  **SELF-APPLICATION, because this lane ran two agents today and the honest
  answer is partial:** I verified **one number per agent** — the scouting cut's
  bump denominator (independently 1,104 league-wide minus our own 74 = 1,030
  against its 1,029) and the farming cut's conveyor-death corollary (a second
  decoder, same direction, different denominator, and I published the
  discrepancy). **Both agents stayed inside their briefed sources, which I
  checked. Neither result had EVERY number re-derived, and I said so at the time
  for the one I could not check at all** — `events.tsv` carries only BUILD and
  DEATH rows, so the farming raid's 3,329 ATTACK events are unverifiable on any
  second surface we own. **That absence is a decoder gap and must never be read
  as corroboration or as doubt.**

- **⛔ AMENDMENT TO THIS LANE'S farming_200s ANSWER (`9ba3b84`), same session —
  THE JUMP HAS A LEAGUE-WIDE BASELINE AND MY WRITE-UP DID NOT CARRY IT:**
  sweep 22 measures, league-wide over 35,714 third-party matches with each
  team's own bot frozen inside a block, that **a team scores materially less
  game share against an opponent's LATER versions than against that same
  opponent's earlier ones.** So **part of farming v13's 72.5% is the general fact
  that a newer version beats a stale field** — not necessarily anything they
  changed. Second correction from the same sweep: **freshly-shipped versions are
  STRONGER, not weaker (matched DiD +0.524, t = +4.89), and teams ship precisely
  when they are LOSING (pre-ship 5-match mean −0.625), so the naive changepoint
  reading of +1.25 is mostly mean reversion.** **farming shipping v13 straight
  after v12 lost 48 points is the league's NORMAL pattern, not a tell.**
  **WHAT SURVIVES UNCHANGED:** the behavioural diff itself — 0 attacks in 310
  archived games across v7–v12 against 3,329 in 87 of 105 v13 games — is a
  *within-opponent* comparison and is untouched by either correction. **And the
  negative control the cut already carried (their own v11 at 50.9%) is exactly
  the instrument that separates "any new version wins somewhat" from "this
  change wins"** — it was chosen before the baseline existed and is now doing
  more work than when it was picked. **The framing that must change is the
  question: not "why is v13 winning" but "what does v13 do that v11 did not,
  GIVEN that any new version wins somewhat."**

- **⭐ THE COMMIT MONITOR SEES SUBJECTS. THE DRIFT LIVES IN BODIES. RUN A BATCH
  PASS, NOT ONLY THE STREAM (s30, 2026-08-11 — a finding about THIS LANE'S OWN
  PRIMARY INSTRUMENT):**
  The all-commits watch is this lane's core tool and it delivers **one line per
  commit — the subject.** That is the right shape for latency (a flag that beats
  its decision) and it has a **structural blind spot: a table, a bar, a closure
  label or a forbidden word lives in the BODY**, and no amount of attention to
  the stream reaches it.
  **MEASURED TODAY: I read 58 commit subjects live and audited a dozen artefacts
  reactively. The one D12 violation in the session was found by a BATCH PASS over
  the same 58 commits afterwards** — sweep 22's closure table marks six roads
  CLOSED, two of them on archive statistics carrying a behavioural premise, and
  **its subject line said none of that.** I had watched that commit go past and
  read it as a research deliverable.
  **⇒ PRACTICE: the stream is for LATENCY, the batch pass is for COVERAGE, and
  they catch different things. Run a batch pass at least once per session** —
  cheapest form is `git log --since=<boot>` and open every commit that
  introduces or edits a **prereg, a leg read-out, a closure table, or a tactics
  file**. Those four surfaces carry every D-rule that lives below a subject line.
  **AND THE COMPANION, because I flagged my own instrument in the same pass:**
  keyword greps over commit SUBJECTS are weak checks and their silence is not a
  clearance — my D4 sweep (survival/screening/defence) returned **5 hits, all
  false positives** (`defensible`, `defenders`, prose about the opponent's heal
  response). **D1/D3/D8 are greppable because they name artefacts or fixed
  phrases; D4/D9/D10/D12 are not, and require reading the body.** Do not report
  a grep-clean D4 as a D4 clearance.

- **⭐ A LIMIT THE BUILDER ASKED THIS LANE TO ENFORCE, RECORDED HERE BECAUSE A
  COMMITMENT THAT LIVES IN A SESSION MESSAGE IS UNENFORCEABLE (s30, 2026-08-11):**
  the ammo-starvation refutation is **D12-clean** (n=2,350 rated ladder games,
  live-game backing, checked not assumed). **Its RESIDUAL is not.**
  **⛔ THE 761 NEVER-FIRING SENTINELS (16.5% of cap) ARE SINGLE-INSTRUMENT AND
  SINGLE-POPULATION, and "target availability" is what REMAINS after excluding
  two candidates — it is not a measured quantity.** Under the standard applied to
  `hp_ledger.py` the same morning, **nothing may be SIZED off that number until a
  second path reproduces it.** The builder asked to be held to this against their
  own interest; the tape row says so, and so does this file.
  **WATCH FORM: if a plank appears whose sizing cites the 761 / 16.5% / "target
  availability", the flag is that the number has one instrument and one
  population, and the plank needs the second path FIRST.** Same shape as §11's
  healing magnitude — **recording is not licensing.**

- **THE `winner_seat` RENAME IS COMPLETE IN CODE AND THE ON-DISK ARTEFACT LAGS —
  a transitional state worth naming because it is exactly when a reader is
  misled (s30):** `ladder_games.seat` carried `winnerSide` and agreed with our
  actual seat on **50.3% of 2,345 rows**. Fixed at both writers
  (`sync.py`, `ladder_meta.py`) plus the docstring that had documented it as
  *"our seat"*. **But `corpus/ladder_games.tsv` on disk still carries the header
  `seat`** — last written 06:49Z and **the keeper does not regenerate it each
  cycle**, so the misleading name persists for anyone opening the TSV until an
  explicit rebuild. **`build_corpus.py:149` reads both keys, so nothing BREAKS —
  the cost is purely that "the defect is unreachable" is not yet true for a
  human reader.** Worth one rebuild, and worth knowing that **a rename at the
  source does not rename the artefact** — the same gap as a corrected document
  whose stale copy is the one that gets read.

- **⭐ WHERE THIS LANE'S HIGHEST-VALUE CATCHES LANDED, MEASURED OVER ONE SESSION —
  NOT ON WRONG NUMBERS, BUT ON THE INFERENTIAL STEP BOLTED ONTO CORRECT ONES
  (s30, 2026-08-11; the builder's formulation of a pattern across three of this
  lane's catches, adopted because it tells a successor WHERE TO LOOK):**
  Three catches, three artefacts, one boundary — **in none of them was a number
  wrong:**
  1. **LOKI-19 §11's healing magnitude** — the measurement stood; what did not was
     licensing a plank off a tool (`hp_ledger.py`) with no forced-answer cells.
     Fence: *recording is not licensing.*
  2. **The 761 never-firing sentinels** — the refutation was D12-clean on 2,350
     live games; the RESIDUAL was single-instrument and single-population, and
     *"target availability"* was what REMAINED after excluding two candidates
     rather than anything measured.
  3. **"Put the turret where something walks"** — availability 20.91% vs 48.89%
     is correct and well-controlled; **the instruction it implies is TWO
     instructions, and the branch that measures best is the one
     `PLAY_DEFENCE: never` forbids.** Both branches move the pooled statistic
     identically, so the headline number is **blind to the only distinction that
     decides legality.**
  **⇒ THE SEARCH HEURISTIC, and it is cheaper than re-deriving numbers:** when a
  document pairs a well-controlled measurement with a proposal, **audit the JOIN,
  not the measurement.** Ask what the number licenses, whether the licensing step
  was measured or assumed, and **whether a rival reading of the same number would
  point somewhere off-programme.** The builder's own diagnosis of the direction:
  *"mine have all been in the direction of the work I wanted to do next."*
  **This complements — does not replace — the s28 heuristic that says RE-DERIVE
  THE NUMBERS FIRST when a claim pairs an argument with numbers.** That one
  catches arithmetic under a correct-sounding sentence; this one catches a correct
  number under an inference nobody measured. **Both are needed and they look
  identical from outside: a confident paragraph with a real figure in it.**
  **AND THE COUNTERPART OBLIGATION, since this lane's own Q3 failure is the mirror
  image:** the same lane that catches other people's unmeasured inferential steps
  published three of its own today (*"caught before the cost"*, *"nobody runs
  corpus_sanity"*, *"11 of 17 unwired"*). **The heuristic is not a claim to be
  better at inference; it is a statement about where the cheap catches are.**

- **⭐ A REPEAT-CLASS CAUGHT PRE-PUBLICATION RATHER THAN POST — RECORD IT, BECAUSE
  THE SAME SHAPE REACHED A LANE THIS MORNING (s30, 2026-08-11; research's
  self-catch, at their request):** measuring **their builders in OUR gunner
  lines at 1.01%** as a control for our builders in theirs, and **excluding it
  before publication with the reason stated: we build 1.29 gunners/game against
  the field's 6.1, so they are exposed to FEWER GUNS rather than dodging
  better.** **The control was confounded by the very quantity it was controlling
  for.**
  **THIS MORNING'S `FIELD_vsUS` POOLING WAS THE SAME SHAPE AND IT REACHED THE
  BUILDER** (91.94% vs a field figure that included games where WE did the
  killing; corrected to **+27.5pp** and then to the exposure-normalised **2.915
  vs 0.847 per 1k builder-rounds**). **Same class, six hours apart, and the
  second one died in the author's own draft.** ⇒ **The durable form: when a
  cross-team rate is used as a CONTROL, ask what OUR OWN behaviour contributes to
  the denominator. A control computed on a population our bot shapes is not a
  control** — and the tell is that the two arms differ in something we chose
  (here, gunner count 1.29 vs 6.1).

- **⭐ A BOUND THAT CAPS A ROAD BEFORE IT IS BUILT — AND THE CEILING ERROR IN IT
  (s30, research's measurement, this lane's correction):** our forward builders
  stand on gunner-covered tiles **2.04% of 22,676 forward builder-rounds against
  a 1.34% map baseline (1.53x)**, and **the enemy core ring is only 2.57%
  gunner-covered with a free ring tile available in 100% of sampled rounds.**
  **⇒ THE HAZARD IS PER-ROUND AND CUMULATIVE, SO DEATHS ∝ ROUNDS-EXPOSED — which
  re-explains LOKI-25 WITHOUT blaming its implementation:** presence −23%, deaths
  −24%, per-build −2.3% **is that identity**, and **ANY plank that reduces
  rounds-exposed shows the same signature whether it penalises or replaces.**
  **This supersedes the "penalty term vs proposal" framing this lane promoted an
  hour earlier** — that framing was about design intent; **this is about
  arithmetic, and the arithmetic binds.**
  **⚠ THE CEILING ERROR, and it runs in the plank's FAVOUR:** *"a perfect routing
  plank cuts exposure by at most 34%"* is `(2.04−1.34)/2.04` — **the reduction
  from becoming AVERAGE.** But **map baseline is the rate for a unit placed at
  RANDOM and a router actively avoids**; with covered tiles at 1.34% of the map
  and a free ring tile always available, **a planner can go BELOW baseline,
  bounded by FORCED exposed tiles (chokepoints, the destination), not by 1.34%.**
  ⇒ **34% is the floor of the ceiling, not the ceiling. Do not size a plank at
  ≤34% and do not let a >34% result read as impossible.**
  **AND THE GEOMETRY POINTS PAST ROUTING ENTIRELY: if the hazard lives in the
  TRAVERSE and the DESTINATION is safe (2.57% covered, always a free tile), the
  mechanism that SKIPS the traverse — launcher delivery — is worth more than the
  one that optimises it.** Two structural facts now point the same way and
  **neither is behavioural, so neither is what D12 restricts.**

- **⛔⛔ D3 RAN ALL DAY ACROSS NINE ARMS AND THIS LANE DID NOT FLAG IT — THE
  LARGEST MISS OF s30, RECORDED AGAINST THE AUDITOR (2026-08-11):**
  `PROGRAMME.md:10` **`PRIMARY_CURRENCY: kill_speed_score`**; `:15`
  **`WIN_RATE_IS_VERDICT: no`**. **`tools/h2h.sh` screened NINE ARMS on WIN RATE
  and every verdict it produced was argued from it. That is D3 verbatim — the
  SECOND ROW of this checklist — and the watch that exists to catch it audited
  the screen's POWER all day and never asked what it MEASURED.**
  **THE TWO FAULTS COMPOUND, which is why nothing survived the funnel:** a
  **binary** outcome (one bit per game) **on a quantity the programme says is not
  the verdict** (so a real kill-speed gain need not move it), screened at
  **n=64** (detects only ≥ +17.5pp, against LOKI-13's +18.0pp). **A plank could
  improve kill round substantially, be exactly what the programme wants, and read
  50%.** **LOKI-25 is the existence proof: its mechanism bar resolved at n=25
  while its win rate said nothing at n=64.**
  **THE BUILDER REACHED THE RIGHT INSTRUMENT BY REASONING ABOUT INFORMATION
  CONTENT — adding KILL ROUND, continuous, the currency's own input — WHILE THIS
  LANE SHOULD HAVE REACHED IT BY READING THE PROGRAMME FILE IT AUDITS EVERYONE
  ELSE AGAINST.**
  **⇒ THE WATCH FORM, and it is this lane's own "audit the JOIN, not the
  measurement" turned on itself: before auditing an instrument's POWER, ask
  whether its OUTCOME VARIABLE is the programme's currency.** A perfectly powered
  screen on the wrong quantity is worse than an underpowered one on the right
  quantity, because its confident answers are all off-target. **Check the
  outcome variable FIRST; the power arithmetic is only meaningful afterwards.**
  **Corollary for the fix, handed to the builder: when a screen reports two
  numbers, the FIRST one is the verdict whatever the docstring says — so kill
  round must be the primary line and win rate secondary.** And **kill round is
  CENSORED for games with no kill; `kill_speed_score`'s buckets already give the
  principled treatment — no kill is the −10 bucket, i.e. the worst outcome, not
  missing data.**

- **⭐ A SATURATED CHECK IS THE MOST CONVINCING-LOOKING THING THAT CAN BE WRITTEN
  DOWN (s31, 2026-08-11T12:41:32Z; this lane's catch, research's formulation and
  independent verification, promoted here because their instance file is not in
  any lane's boot path):**
  `SEAT-AND-MAP-ASYMMETRY-2026-08-11.md` §1 read *"sixteen cells are fitted
  exactly by two parameters… with no residual"*, under three ✓ marks. **It
  consumed exactly TWO observed quantities and solved for TWO free parameters**
  (`t=(a+b−1)/2`, `s=a−t`). **Driven to the other verdict by its own author at
  this lane's request, it cannot produce one: worst residual over all pairs
  INCLUDING NONSENSE = 1.11e-16, and the pair (0.99, 0.99) receives a clean
  `s=0.500, t=+0.490`.** The three ✓ were the identity restated.
  **WHY IT OUTRANKS AN ORDINARY BAD CHECK: it was the demonstration for the ONE
  claim in the document that stops a repricing of every past verdict this project
  has produced.** The load-bearing claim carried the weakest possible support and
  **looked like the strongest** — an exact fit and a row of ticks. **The same file
  reported the residual it denied** (heterogeneity χ²=15.93, 7 df, **p≈0.026**):
  one question, one file, opposite answers, one author. D14 without two documents.
  **⇒ THE MECHANICAL FORM, research's, and it is cheap enough to apply at review
  time: COUNT THE FREE PARAMETERS AGAINST THE OBSERVED QUANTITIES BEFORE PRINTING
  A ✓. If parameters ≥ observations the fit is an identity and carries zero
  evidence, however many decimal places it agrees to.**
  **⇒ AND THE REPAIR GENERALISES FURTHER THAN THE FAULT.** What replaced the fit
  was **algebra from the DESIGN**: each arm plays 512 games in each seat, so its
  pooled rate is `[(s+t)+((1−s)+t)]/2 = 0.5 + t` and `s` cancels identically.
  Stress-tested by the author across `s` = 0.541 / 0.95 / **0.30 (advantage
  REVERSED)** / 0.50 — `t` recovers **−0.02195 in every case** — and under a
  seat×treatment interaction (`t_A=−0.05, t_B=+0.01`) the pooled figure recovers
  **exactly `(t_A+t_B)/2`**. **Unbiased regardless of the effect's SIZE, its
  DIRECTION, and its variation BETWEEN arms.** ⇒ **When a property of the DESIGN
  can do the work, prefer it to a fit on the data: a design argument cannot be
  confounded by the data it is arguing about, and it stops depending on sections
  that may later be retracted** — which is what happened here within four minutes.
  **COMPANION, same session, the same fault from the opposite direction (research's
  line, worth carrying verbatim): *"the larger n made the wrong population feel
  like the stronger evidence."*** Their §3 died on a population control — the local
  battery is v104 against a near-identical copy of itself and **NEITHER platform
  population contains that matchup**. Beside `meta_join`'s coverage gap, where a
  **fresher** surface felt like a **completer** one, this gives the general form:
  **SIZE AND RECENCY BOTH IMPERSONATE VALIDITY, AND NEITHER IS IT. Ask what
  population a number is FROM before asking how big or how new it is.**
  **SELF-APPLICATION, recorded against this lane:** I was handed that §3, audited
  the three attack surfaces its author offered, cleared two — **and the killing
  defect was a population/fixture mismatch, which is the UNIFIER at the top of
  this very file.** I checked the column names. **The author found it themselves
  in four minutes. Auditing the doors a document opens is not auditing the
  document.**

- **⭐ AN AUTHOR-SUPPLIED ATTACK LIST STEERS THE AUDIT INTO THE REGION WHERE THE
  AUTHOR IS LEAST LIKELY TO BE WRONG (s31, 2026-08-11T12:43:08Z; research's formulation
  after this lane cleared their document and its own author killed it four minutes
  later — a rule about how THIS LANE works, so it lives here):**
  Research handed three named attack points with the seat document. This lane
  checked all three, cleared two, qualified one. **The defect that killed §3 was
  behind none of them: the local battery is v104 against a near-identical copy of
  itself, and NEITHER platform population contains that matchup.**
  **THE MECHANISM: all three offered doors were about whether the SOURCES were
  sound; none was about whether the COMPARISON was legal.** An author's list of
  ways they might be wrong is drawn from their own model of the work — **and that
  model is exactly what a frame error is invisible to.**
  **⇒ THE RULE, and it is a one-line change to this lane's practice: AN AUTHOR'S
  ATTACK LIST IS AN ADDITION TO THE STANDING CHECKLIST, NEVER A SUBSTITUTE FOR IT.
  Run the checklist first — population, denominator, era, fixture, estimator,
  clustering unit — THEN the offered doors.** The doors are cheap and often good;
  they must not set the order.
  **⛔ AND THE HALF OF THIS THAT IS NOT ABSOLVED, recorded because research
  generously offered to take the whole fault and the offer should not stand:
  the unifier is the FIRST standing note in this file** — *a number true SOMEWHERE
  used SOMEWHERE ELSE; measure both sides of a comparison inside the arm being
  tested.* **It applies to every document unprompted, whatever doors are named.**
  A steer explains why the checklist was skipped; it does not excuse it. **Both
  lanes' accounts are true and only one of them is mine to fix.**
  **COUNTERPART, and it is the reciprocal obligation:** when handing a document
  for audit, name the doors **and** say *"these are my priors — attack the frame
  too."* Research adopted this for future handoffs in the same message.

- **⭐ D20 (NEW) — A PLANK THAT IS A PARAMETER TWEAK RATHER THAN A MECHANISM MUST
  DECLARE ITS PREDICTED EFFECT SIZE, AND ON A SHORT CLOCK MUST CLEAR ~+10pp
  (s31, 2026-08-11T13:08:47Z; the gap Magnus's question exposed in this checklist):**
  D4 catches a plank aimed at DEFENCE. **Nothing caught a plank that is a KNOB-TURN**,
  while the directive defines Loki as *"cheap tricks, manipulation, poisoning and
  every exploit we can find."*
  **THE EVIDENCE IS THE WHOLE s30 SCREEN:** `heal` (a constant), `cap6`/`cap12`
  (constants), `noseal`/`nohome` (flags off), `roster` (composition), `bestfit`
  (a selection rule), `gunaxis`/`gunblank` (siting). **Nine arms, zero new
  mechanisms.** Magnus, 2026-08-11, after 29 h with no ship: *"do we actually make
  ANY progress?"*
  **⇒ THE RULE, AND ITS ARITHMETIC:** near 50%, **+1pp of true game share ≈ +7 Elo
  of equilibrium rating.** A knob-turn at +2.3pp is **~+15 Elo**; LOKI-13 at +18pp
  was **~+120**. **With ~420 rated matches left (~4 ship-and-converge cycles), a
  candidate under ~+10pp is not worth one of them.**
  **⇒ AND IT DISSOLVES THE SCREEN PROBLEM AT THE SAME TIME:** knob-turns produce
  small effects, small effects need enormous screens, **so the SAME size filter
  that buys a worthwhile plank also buys a resolvable one.** LOKI-25's mechanism
  resolved at **n=25**; the s30 screen at n=64 could not see **+17.5pp**.
  **⇒ WATCH FORM: when a plank's diff is a constant, a flag or a threshold, ask for
  the predicted effect size BEFORE the prereg. If it cannot be stated, that is the
  finding.** A tweak may still be shipped — it is nearly free to have live while
  something bigger is built — **but it must not consume a CYCLE, a screen, or a
  window.**
  **⛔ SCOPE, so this does not become a veto:** the bar is on what a plank may
  CONSUME, never on whether it may SHIP. The s30 operational rule stands —
  positive point estimate + verified mechanism + no rule breach, significance not
  required. **A ship is not a cycle you spend; the ladder converges in the
  background.**

- **⭐ D21 (NEW) — **PUBLISHING A JOIN AS A MEASUREMENT**: THREE INSTANCES IN NINETY
  MINUTES, ACROSS TWO LANES, EACH SURVIVING A CAREFUL AUTHOR (s31, 2026-08-11T13:33:48Z):**
  1. *"All three predicted rows moved the predicted way"* (LOKI-27 ship) — **the
     ratio is ALGEBRAICALLY determined by the other two rows and all three came
     from the same 162 throws.** One fact counted as three.
  2. *"The symbol set is identical, therefore the guard matrix stands"* (LOKI-28) —
     a **symbol-table** fact welded to a **doctrinal** claim. The offline diff then
     measured **`__text` differing in 47,404 of 572,364 bytes (8.3%)**: the
     inference was unsafe and **the conclusion happened to be right.**
  3. *"The layout did not move, so the 8.3% is churn RATHER THAN SEMANTICS"* —
     layout-identity proves every changed function kept its **exact size**; a
     flipped comparison or an altered constant is a same-size edit. **What was
     established is "not the launcher, not the exception path, not the runner, and
     same-size elsewhere" — not "no semantics".**
  **THE COMMON SHAPE: a correct measurement, a plausible doctrinal claim, and a
  "therefore" nobody measured.** Distinct from the s28 rule (*re-derive the numbers
  first*) — **here every number is right.**
  **⇒ WATCH FORM, and it is one question: SPLIT THE SENTENCE AT THE "THEREFORE" AND
  ASK WHAT WAS MEASURED ON EACH SIDE.** If the left side is a fact and the right
  side is a doctrine, the join is the claim and it is unverified.
  **⇒ AND THE REASON THIS IS A D-ROW RATHER THAN A NOTE: instance 3 was committed
  ONE MESSAGE AFTER its author correctly diagnosed instances 1 and 2 in their own
  output and undertook to watch for it.** **The failure survives full awareness of
  the failure**, which is the definition of something that needs a mechanical
  check rather than an intention. **Both of this lane's own biggest catches today
  were joins (LOKI-27's unsized bar, the engine inference); both of this lane's own
  worst errors today were joins too** (a +59% band sized on the stored figure I was
  condemning; a survival thesis welded to three unrelated measurements).

- **⛔ CORRECTION TO D21 ABOVE, ~20 MINUTES OLD, AND IT IS THE VERY FAULT THE NEXT
  NOTE DESCRIBES (2026-08-11T13:38:32Z):** D21's instance 3 records *"the layout did not
  move, so the 8.3% is churn RATHER THAN SEMANTICS"* as a join. **It WAS an
  unmeasured "therefore" at the time it was published — and it has since been
  VERIFIED.** The builder's instruction-level decode (`f7d92ed`) shows every
  differing byte in `can_launch` / `destroy_entity` / `launcher_target_valid` /
  `finish_firing_turret` is **the same `bl` whose target moved
  `0x385a8 -> 0x386c4`**, with `Watchdog::arm` byte-identical. **The claim was
  right; only its WARRANT was missing.** D21 as written invites a reader to
  conclude the claim was false. **What D21 indicts is the unmeasured therefore,
  never the conclusion** — and the same applies to instance 2, whose conclusion
  also survived. **Left as an appended correction rather than an edit, because a
  silently-fixed instance breaks the series.**
  **⛔ AND FOR THE LEDGER: this lane endorsed the builder's METHOD 2 as "settled"**
  — the hash-normalised disassembly that **masked the very bytes it checked**
  (`otool` prints call targets as symbol names) — **one message after criticising
  method 1 for inferring bodies from names.** Same fault, one layer down, in the
  message that named the pattern.

- **⭐⭐ D22 (NEW) — **PROMOTION INTO A BOOTED FILE IS WHERE HEDGES DIE, AND THIS
  LANE'S OWN ROUTING RULE IS THE MECHANISM THAT CREATES IT** (2026-08-11T13:38:32Z;
  research's discovery, `3111b1f`, promoted here — with the irony intact):**
  `CLAUDE.md`'s always-loaded block states *"one hostile body on the ring DOUBLES
  the 25-round core-death hazard, 2.24% -> 4.77%, CIs disjoint"* as an established
  causal effect. **The original (`coordination.md:16649`) says, in its own words,
  under its own table: *"THE CAVEAT I AM NOT BURYING … the 2x is partly REVERSE
  CAUSATION and cannot be separated from this data … Treat 2.1x as an UPPER BOUND,
  not an effect size."*** It also recorded the decline at j>=2 and an r<250
  restriction. **FOUR HEDGES DIED IN TRANSIT into the one file every lane boots on,
  and THE ORIGINAL AUTHOR DID NOTHING WRONG.**
  **And the hedges were load-bearing:** re-derived over **19,178 replays / 16.0M
  core-rounds**, the association replicates at 14x the n and **the causal reading
  fails five controls** — decisively on POLARITY, where **a core's OWN builders on
  its OWN ring, which cannot damage it, raise its own 25-round death rate
  2.302% -> 4.641% (x2.02), indistinguishable from the x2.13 attributed to a
  HOSTILE body.** Healers converging on a core already under attack.
  **⇒ THE FAULT IS IN THE PROMOTION STEP, NOT IN EITHER DOCUMENT** — and
  **THIS LANE'S RETRO ROUTING RULE INSTRUCTS EVERY LANE TO PERFORM THAT STEP**
  (*"behaviour change -> promote into a file that IS booted"*). **I have promoted
  five items into this file today; each was a summarisation, and summarisation is
  exactly where a hedge is dropped for length.**
  **⇒ THE COMPANION RULE, and the routing rule is incomplete without it: A PROMOTED
  CLAIM CARRIES ITS HEDGES OR IT CARRIES A POINTER TO THE ORIGINAL — and the
  promotion is VERIFIED AGAINST THE SOURCE, not against the memory of it.** If the
  hedges do not fit, the promoted text is a POINTER, not a summary.
  **CHECK FORM: for any load-bearing sentence in a booted file, open its source and
  diff the qualifiers.** The correction directly above is this rule catching its
  author twenty minutes after the fact.
  **`CLAUDE.md` IS BUILDER-OWNED; the correction there is theirs to make and is
  flagged, not touched.**

- **⛔ CORRECTION TO THE "GEOMETRY POINTS PAST ROUTING" NOTE ABOVE — THE PREMISE IS
  BACKWARDS AND THIS LANE AMPLIFIED IT TODAY (2026-08-11T13:43:19Z; research's
  attribution cut + transit-vs-station, `02558c7`):**
  The note above reads *"if the hazard lives in the TRAVERSE and the DESTINATION is
  safe … the mechanism that SKIPS the traverse — launcher delivery — is worth more
  than the one that optimises it."* **Measured: MOVING is BELOW-average hazard
  (0.90x), PARKED 30+ rounds is the SAFEST state (0.19x), and our builders die
  2-9 rounds AFTER STOPPING.** ⇒ **the traverse is the safe part.** Research
  withdrew the launcher-delivery road on this basis.
  **AND THE NUMBER THAT MOTIVATED IT NEVER EXISTED: the "unexplained ~2.3x" came
  from treating multiplicative terms as additive** — corrected by its own author.
  **⇒ THIS LANE'S FAULT, BOOKED: I did not originate the note, but I promoted
  launcher delivery to research this morning as the lead generator candidate,
  quoting the traverse premise as established. I repeated a booted claim without
  opening its source — which is D22, committed by the author of D22, on the same
  day.** The hazard concentrates in the SETTLING phase, and neither routing nor
  delivery addresses that.

- **⭐ THE ELO TAPE CANNOT CERTIFY HOLDER RESTORATION, AND ITS SILENCE IS NOT
  EVIDENCE — CAUGHT WHILE ABOUT TO BUILD A CHECK THAT WOULD HAVE RELIED ON IT
  (2026-08-11T13:57:16Z):** I set out to add a HOLDER-IDENTITY check to this lane's
  pre-arm watch, on the reasoning that a prototype left live is worse than a
  rating dip. **The surface is wrong.** `elo_history.tsv` is polled every
  **300 s**; a correctly-run prototype window is **~20 s** (submit → fire →
  rollback). ⇒ **P(a poll lands inside the window) ≈ 20/300 = 6.7%. Roughly 93% of
  CLEAN rotations leave no trace, and so would 93% of DIRTY ones.**
  **MEASURED NOW: the LOKI-28 prototype fired at ~13:33 and the last 20 tape rows
  contain only v104 and v112 — no prototype tag at all.** A reader could take that
  as evidence the rotation was clean. **It is not evidence of anything.**
  **⇒ THE CHECK WOULD HAVE BEEN AN ALARM THAT CANNOT FIRE — the fourth in this
  repo — and I would have built it into a watch I armed twelve minutes earlier.
  A fix for a fault carrying the fault, caught before construction rather than
  after.**
  **⇒ THE CORRECT SURFACE IS UNCHANGED AND ALREADY MANDATED: the LIVE `Active bot:`
  line, or per-match `teamAVersion` at the PAIRING BOUNDARY.** `CLAUDE.md` already
  says the match COUNTER cannot answer this; **this adds that the ELO TAPE cannot
  either, and for a different reason — the counter is blind to pairing, the tape is
  blind to duration.** Both fail silently and both fail toward "looks fine".

- **⭐ THIS LANE'S CHARACTERISTIC FAILURE HAS COLLAPSED TO ONE SHAPE, AND IT HAS
  A DIRECTION (s32, 2026-08-11; promoted from `docs/retro-side-lane-2026-08-11-s32.md`
  because a retro instance is in no boot path):**
  **Four published errors in one session, all the SAME fault — I INFERRED FROM AN
  ARTEFACT INSTEAD OF OPENING THE PRIMARY.**
  1. **A `--stat` read as an audit** — I published *"audited `c541aae`,
     on-programme, no flag"* having read the subject line and the file list. The
     defect was then raised by the commit's own author.
  2. **A docstring read as the code** — I reported `cores_idle` as *"trips only
     on TOTAL idleness"*; the code is `if n < EXPECTED`. **`cores_idle.py:31` and
     `PROGRAMME.md:60-62` are both stale against a fix MY OWN LANE shipped one
     session earlier**, so I flagged as live a defect I had already closed.
  3. **An ALERT line read as the whole event** — I called the `FX` fixture
     *"channel pollution"*; `OUT` was hardcoded, the fixture ran against the LIVE
     run and **launched a stray shard.**
  4. **An arm file read as the holder** — I sent an urgent *"a prototype is live,
     pairing in four minutes"* off the existence of `arm_unrated_v114_*.txt`,
     **inside the same message that said the `Active bot:` line is the only
     surface that will tell you.** `fcode status` said v112. **The fault was
     inside the sentence recommending the cure.**
  **⇒ WATCH FORM, and it is one question before any flag leaves: WHICH ARTEFACT
  AM I READING, AND WHAT IS THE PRIMARY IT STANDS IN FOR?** A file's existence is
  not a state. A docstring is not behaviour. A stat is not a diff. An alert line
  is not an incident.
  **⇒ AND THE DIRECTION IS STABLE WITHIN A LANE AND DIFFERS BETWEEN THEM:** all
  four of mine ran toward the **COMFORTABLE** reading — a clean clearance, a
  defect that was someone else's, a smaller severity, a danger already passed.
  **s28's ran toward the DRAMATIC; the builder's s32 retro records mixed with a
  peer catching four of six.** **A lane that knows its own attractor can check
  that side first**, which is cheaper than checking both.

- **⭐ FLAG THE DEFECT WITH ITS FIX — the practice that doubled this lane's
  mechanisation rate (s32; Q8 went 3 → 6):**
  Six flags became enforced code in one session — `gate.py`'s reason-string
  requirement · `overnight_watch.sh`'s startup refusal (exit 3) and its
  monotonicity guard · `OUT=${OUT:-…}` in both runners · `TARGET_RATING_FLOOR`
  in `PROGRAMME.md` + `target_value.py` · and the **`tled` bar, which became a
  SHIP GATE rather than a leg statistic.**
  **The cause was not more effort. Every one of the six arrived with a buildable
  replacement**: the startup refusal was a named option ("refuse to start if no
  shard has a `.tsv`"); the `tled` flag named the field, the file, the live
  column **and its positive control** (7.28% of rows nonzero, so the column is
  not dead). **A flag that arrives with a fix gets built; a flag that arrives as
  a criticism gets acknowledged.** ⚠ **And it is not free: proposing the fix
  means the auditor now owns a design opinion, which must be labelled as one** —
  each of the six was offered as *"either of these closes it"*, not as the answer.

- **⛔ `audit_trigger.ship_cadence` MUST NOT BE QUOTED UNTIL IT COUNTS SHIPS
  RATHER THAN TRANSITIONS (s32, 2026-08-11; research's finding, promoted here
  because THIS FILE cites `audit_trigger` as the precedent for a mechanical
  process check and a successor will therefore trust its rows):**
  `tools/audit_trigger.py:150` counts **`active_bot` TRANSITIONS**, and its own
  docstring states the assumption it rests on — *"an activation is what we
  actually mean by 'a decision landed'."* **A prototype leg breaks exactly that:
  activate + roll back reads as two activations.** Across one session the row
  read **0.47 (TRIP) → 0.50 (ok) → 0.38 (TRIP) against a single real ship.**
  **⚠ SCOPE, and it is what keeps the instrument usable: the `cross-lane
  analysis` row is UNAFFECTED and is what a FIRE verdict should rest on.** Only
  the cadence row is compromised. A spec is with the builder (collapse
  `X → Y → X` inside a short window to ZERO; count only transitions that
  PERSIST; selftest cell = one real ship plus three activate/rollback pairs must
  read **1, not 7**).
  **⭐ AND THE REASON THIS IS A CHECKLIST ENTRY RATHER THAN A BUG REPORT: the
  same docstring ALREADY CARRIES A STANDING CAUTION FOR THE PREVIOUS VERSION OF
  THIS SAME FAULT** — *"every 'analysis is outpacing decisions' reading taken
  before this fix is suspect"* — written when a prose-matching predicate was
  replaced. **The replacement inherited a different version of the same failure
  and got no caution of its own.** ⇒ **D68's shape a seventh time, and the new
  form is the sharpest yet: A WARNING ABOUT THE OLD FAULT SITTING DIRECTLY ABOVE
  THE NEW ONE READS AS EVIDENCE THE FAULT WAS HANDLED.** When a fix carries a
  caution about what it replaced, ask whether the caution applies to the
  replacement — the text that should have prompted the question is the text that
  suppressed it.

---

## D19 — **A SUBSTRING FILTER OVER PROSE IS BIASED AGAINST THE MOST-AUDITED ROWS, AND THE BIAS RUNS TOWARD MAKING A HEALTHY QUEUE LOOK STARVED**

**Promoted to this file (side lane, s33, 2026-08-12) because it is a behaviour
change and this file IS in every lane's boot path. Measured, not argued.**

`tools/queue_check.py` excludes a `QUEUE.md` row if any of `BLOCK_MARKERS`
appears anywhere in its text. **Run against the LIVE file at 04:5xZ, three items
carrying `GREP: PASS` in live sections are silently dropped:**

| item | `GREP:` | excluded by | the substring actually occurs in |
|---|---|---|---|
| **#5 CRASH INDUCTION AT SCALE** | **PASS** | `withdrawn` | *"…IS **WITHDRAWN** AS A RANKING CLAIM. ⚠ **BUT NOT CLOSED, AND THE DOC ITSELF SAYS SO**"* |
| **#3 CLEAR MORE ENEMY TURRETS** | PARTIAL PASS | `withdrawn`, `refuted` | its own title: *"(was 'we go forward late' — **refuted**; then over-sized — corrected)"* |
| **#10 BLIND THEIR GUN WITH THEIR OWN BODY** | **PASS** | `blocked` | **a SYMBOL NAME in its grep stamp: `eco.py:pave_**blocked**_by_ore`** |

⇒ **The live count reads 8. The true unblocked count is 11.**

**⭐ THE DECISIVE DEMONSTRATION, and it is same-minute:** `queue_check` reports
**#5 as not startable**, and the builder **started it in commit `1f12297`**
(`bots/_v157gunborder`, LOKI-30 BORDER-FIRST EXILE) **while this row was being
written.** A gate whose verdict is contradicted by the work happening beside it
is not undercounting at the margin.

**WHY THE BIAS IS SYSTEMATIC RATHER THAN BAD LUCK — this is the part to carry:**
**a row acquires the words *withdrawn*, *refuted*, *blocked* precisely BECAUSE it
has been audited.** This repo's culture is to record the correction inline and
keep the provenance, so **the most-scrutinised rows are the ones most certain to
contain the excluding substring.** #10's case is the purest: it is excluded by a
**function name in the codebase**, quoted as the evidence the item IS startable —
identical in kind to `"shipped"` firing on `"NOT shipped"`, which that file
already documents and removed.

**⛔ AND "THE UNDERCOUNT IS THE SAFE DIRECTION" IS FALSE HERE.** `queue_check.py`
says so in its own comment. Under `QUEUE_FLOOR: 3` and Magnus's *"if the queue
runs empty we go stale, that is not acceptable"*, **an undercount pressures the
owner to GENERATE items while good ones are already sitting there** — the same
Goodhart the `GREP:` gate exists to stop, running the other way. An overcount
pads the floor; an undercount manufactures busywork and hides finished thinking.

**FIVE FALSE POSITIVES OF THIS CLASS ARE NOW ON THE RECORD IN TWO DAYS**
(`shipped`/`NOT shipped` · a WITHDRAWN row · a DEMOTED row · `withdrawn` firing on
#19's own retraction text while research was FIXING the previous one · and these
three). ⇒ **The substring approach has failed in ORDINARY PROSE, not at the
edges, and each repair has added another substring.**

### THE WATCH FORM
**Any gate that decides on a SUBSTRING SEARCH OVER PROSE must be assumed to fire
on rows that merely DISCUSS the state it looks for.** Before trusting such a
gate's count, print the excluded rows and the marker that excluded each. **A gate
that reports only survivors cannot be audited** (this is D83/S6 — *a filter must
name its casualties* — with the added finding that **the casualties here are
non-random and correlate with quality**).
**THE STRUCTURAL FORM IS THE REPAIR:** state belongs in a **SECTION HEADING**
(`DEAD_SECTIONS`) or a typed field, never in the body text. Spec routed to the
builder in `docs/coordination.md` (s33): add `## DONE` to `DEAD_SECTIONS`, **and
the selftest must drive the SAME row text both ways** — under `## DONE` → 0,
under `## NEXT UP` → 1 — because a typo'd heading is otherwise a silent no-op
whose failure state is indistinguishable from a legitimately open item.
**⚠ AND `queue_check.py`'s OWN COMMENT NAMES THE ANTI-PATTERN THAT WAS THEN
FOLLOWED:** *"rewording the queue around a tool's bug is the wrong repair."*
#19 was reworded WITHDRAWN → RETRACTED to satisfy the tool, by the lane that had
just read that comment. **D68 again: the caution sits directly above the fault.**

---

## D20 — **A COMPENSATING MANUAL CHECK IS HOW A DEAD GATE SURVIVES ITS WHOLE LIFE**

**Promoted s33, 2026-08-12. Research's formulation; this lane supplied one of the
three instances and it is the reason it is credible.**

`overnight_read.py`'s calibration section looked up literal keys `NULL`/`NEGCTRL`
while every shard we have ever run is named `NULL114`/`NEG114`. **It printed
"⚠ NO NULL DATA — every band below is uncalibrated" on every run of its life and
the `BANDS RE-CENTRED` branch had never once executed.**

**IT SURVIVED BECAUSE ALL THREE LANES INDEPENDENTLY HAND-VERIFIED THE THING IT
FAILED TO CHECK.** The builder, research and this lane each reported the
calibration cells as passing — correctly, from `corefill_status.sh:67`'s
row-derived awk — **in the same sessions where the tool printed `NO NULL DATA` in
its own output.** Three correct answers from a surface nobody was told to use,
covering for a gate nobody noticed had never run.

### THE WATCH FORM
**When you hand-verify something a tool was supposed to check, CHECK THAT THE TOOL
CHECKED IT.** A right answer obtained the manual way is not evidence the
instrument works — **it is the mechanism by which a broken instrument is never
noticed.** HANDOVER's instruction (*"READ THE CALIBRATION CELLS FIRST"*) was
correct, and the instrument it named could not satisfy it; the gate was met only
by accident. **Related to D13 but distinct: D13 is a live instrument that cannot
RESOLVE; D20 is a dead instrument masked by a human who resolves it elsewhere.**
**And the general form: a guard whose failure state is indistinguishable from its
success state will not be found by reading its output** — it is found only by
asking what its success state would look like and whether anything has ever
produced it.

---

## D21 — **RETRACT AT THE PROVENANCE RECORD FIRST, THEN THE ARGUMENT SITES**

**Promoted s33, 2026-08-12. Research's rule, from their own miss, adopted here
because it is the durable half of a three-site retraction.**

A withdrawn projection was retracted at the analysis doc and at the queue item
that inherited it — **and left standing in the ANSWERED/closure row of the item
it belonged to**, which is the row a successor reads when asking *"what did this
conclude?"* **Of the three sites it was the least visible to the author and the
most load-bearing for everyone after.**

**The mechanism, in their words and worth quoting because it is not
carelessness:** *"I retracted by searching for the claim where I had ARGUED it,
not where I had RECORDED it."* Argument sites are salient because you wrote the
case there; **the archive is what outlives the session.**

### THE WATCH FORM
**A retraction that follows the argument misses the archive.** Enumerate the
provenance/closure/ANSWERED records FIRST — the reverse of the order that feels
natural — then the places the case was made. **And this is D14 with a name: a
closure and its correction sat one line apart in the same file, on the same
question, with nothing forcing them to cite each other.**

---

## D22 — **A LEG NAME REUSED FOR A DIFFERENT PLANK. THERE IS NO ALLOCATION REGISTRY, AND TWO COLLISIONS LANDED IN FOUR MINUTES**

**Promoted s33, 2026-08-12, from a live audit of `1f12297` / `fb4355a` / `a360936`.**

**THE COLLISIONS, grepped across `bots/` and `docs/prereg/`:**

| n | s32 holder | s33 claimant | verdict |
|---|---|---|---|
| **30** | **`PREREG-loki30-gunaxis-live-2026-08-11.md` — LOCKED, +3 amendments**, live-unrated 3-arm leg whose Amendment 2 became the **v114 ship gate** | `_v157gunborder` · `_v158blankborder` — BORDER-FIRST EXILE, a local n=5,408 shard | **⛔ COLLISION** |
| **31** | `_v153gunaxtb/raid.py:565` — *"⭐ LOKI-31 (s32)"* | `_v159surch30` · `_v159surch90` — NON-STRIKE SURCHARGE | **⛔ COLLISION** |

**Multi-hits on 26 / 27 / 29 are NOT collisions** — those are stacked or paired
arms of one plank (`_v158blankborder` stacking `_v147gunblank`'s LOKI-26;
`_v151null` as `_v151seatrel`'s control). **The numbering exists to do exactly
that**, and any guard built here must pass them or it will be routed around.

**⛔ A PREREG'S IDENTITY IS ITS LEG NAME** — that is how the prereg-of-record is
located for a result — **and a LOCKED prereg cannot be the side that moves.**

**WHY IT IS STRUCTURAL AND NOT CARELESSNESS, which is the part to carry:**
**there is no canonical list.** s32's allocations exist **only as comments inside
bot trees**; `docs/prereg/` holds only the legs that reached a prereg. So *"what
is the next free LOKI number?"* is answerable **only by a repo-wide grep nobody
is instructed to run**, and picking *one past the last one I worked on* collides
**by construction across a session boundary**. Both instances are precisely that,
by two different lanes, ten minutes apart.

### THE WATCH FORM
On any commit introducing a `LOKI-N` label: **grep `bots/` and `docs/prereg/` for
that N and confirm every other hit is the SAME plank.** A different plank on the
same number is a flag.
**THE DURABLE FIX IS A SCRIPT, NOT A CONVENTION** — this repo's own measured
lesson (attention-level rules failed under time pressure all day; script-level
ones held). Routed to the builder in `docs/coordination.md` (s33):
`tools/leg_name.py --next` / `--claim N --plank "<name>"`, refusing a number
already bound to a **different** plank, appending to one
`docs/prereg/LEG-REGISTRY.md`, **with a selftest driving all three cells: free N
claims cleanly · N bound to a DIFFERENT plank REFUSES · N bound to the SAME plank
PASSES.** The third cell is the one that keeps the guard usable — a guard that
fires on legitimate stacked arms gets removed from the path, which is how
`gate.py` came to be bypassed by `h2h.sh`.
**COST OF DELAY IS THE WHOLE POINT (D21):** while the shards run this is six
string edits; **once a 5,408-game readout is filed under the wrong leg name it is
an archive correction**, and the archive is what outlives the session.

---

## D23 — **SELF-PLAY CAN NEVER MEASURE AN EXPLOIT PLANK, AND IT IS A PROPERTY OF THE WHOLE LOKI LINE RATHER THAN A DEFECT IN ONE SHARD**

**Promoted s33, 2026-08-12, after the GUNBORDER occurrence-zero flag turned out
to generalise. Measured, one command:**

```
for d in bots/_v1[3-9]*/main.py; do grep -q 'except Exception' "$d" && ...; done
  ->  line-era trees with a blanket `except Exception` in main.py:  38 of 38
```

**And `CLAUDE.md` states the generating mechanism in its own words:**

> **"MINE OUR OWN BUG FIXES FOR THEIR BUGS.** `eco.py` carries a guard added
> because a launcher throw teleported OUR builder and made `is_tile_empty` raise.
> **We patched it; most teams have not.**"

⇒ **Every exploit of this class is, BY CONSTRUCTION, one we have already
immunised ourselves against — because patching it is how we found it.**
An escaping exception is what destroys a unit (`0x1ac5c` →
`Game::destroy_entity`, `SystemExit`/`KeyboardInterrupt` the only exemptions), so
a blanket `except Exception` is total immunity, and **all 38 of our line-era
trees have one.**

**THE CONSEQUENCE, and it is structural:** `COMPARE_AGAINST:
previous_line_iteration` makes the currency fixture **one of our own trees**.
For an ordinary plank (economy, siting, targeting, a runtime gate) that is
correct and cheap. **For an EXPLOIT plank it means the mechanism cannot occur at
all**, so the shard measures the plank's COST and reads exactly ZERO on its
benefit — however many games it runs. **This is not a mistake anyone made; it is
two programme fields interacting**, and `FIXTURE_OF_RECORD: live_unrated` is the
one that resolves it.

**⚠ AND THE FAILURE IS ASYMMETRIC IN A WAY THAT CLOSES ROADS.** A ~50% read on
such a shard says *"free, ship it"* when no benefit was measurable; **a <50% read
says *"it costs us, drop it"* — a VALID cost finding that retires a road whose
benefit has never been measured on any fixture where it could occur.** The second
is a D12 violation wearing a local-battery costume, and it is the one to guard.

### THE WATCH FORM — one question, asked before the shard is queued
**"Can the OPPONENT in this shard experience the mechanism?"** If the opponent is
one of our own trees and the mechanism targets a defect we have patched, the
answer is **no**, and the shard is a **COST SCREEN** — which is a genuinely
useful thing to be, because a clean non-inferiority result is exactly what
licenses spending a live-unrated window on the benefit. **It must simply never be
quoted as the currency.**
**AND NAME BOTH ENDS OF THE BRACKET** (research's generalisation, adopted): our
`*_probe` fixtures are maximally VULNERABLE by construction and our own trees are
maximally INVULNERABLE by construction. **`_probe_border_raw` gives the ceiling
(100% of border arrivals kill), `_v146gunaxis` gives the floor (0/16).** The
field sits between and is measured by neither. **A scope note that caveats one
fixture has an obligation to say what the OTHER fixture is doing — bracketing is
only visible when both ends are named**, and the s33 instance caveated the end
that lies UP and left the end that lies DOWN unstated.
**NEVER POOL THE TWO.** Averaging a maximally-vulnerable fixture with a
maximally-invulnerable one produces a number about neither.

---

## D24 — **A GREEN SELFTEST IS NOT EVIDENCE. FIVE WAYS A TEST FAILS TO TEST ITS CLAIM, EACH NEEDING A DIFFERENT CHECK**

**Promoted s33, 2026-08-12. EIGHT instances, FIVE categories, THREE lanes, ONE
session — every one measured, none hypothetical.** Magnus's question that opened
it, after `crash_cells` v1 shipped a 7-case green selftest and then printed *"THE
WEAPON DOES NOT FIRE — the road closes"* on a run where the weapon fired 15
times: ***"Dont we test our tools?"*** **The answer is worse than "no": we test
them, the tests pass, and the verdict is still wrong.**

**The split matters because a single sentence — *"the assertion and the defect
can be the same line"* — does not tell you what to DO. Each category has its own
question, and (a) and (d) are not detected the same way.**

| # | category | instance(s) this session | **the check that finds it** |
|---|---|---|---|
| **a** | **THE PASS CONDITION *IS* THE BUG** | `effective_n`: the independent fixture asserted *"eff_n is near the row count"* as its PASS condition — **which is the CEILING read**, so the one cell able to catch ceiling-pinning was ratifying it | **"What would this assertion print if the bug WERE present?"** If the answer is "the same thing", the cell is decorative |
| **b** | **THE RIGHT VALUE IS COMPUTED AND THE DECISION IGNORES IT** | `overnight_read`: refused 5 shards on a stale HEARTBEAT flag while computing row-level `nowin` (= 0 for all five) **29 lines below**. 27,040 real games discarded | **"Does the DECIDING branch read the MEASURING function's output?"** A correct measurement and a wrong decision coexist happily |
| **c** | **THE CELL PASSES ON A DIFFERENT GATE** | `queue_check`: three marker cells (`BLOCKED`, `gated`, `WITHDRAWN`) carried **no `GREP:` stamp**, so all three returned 0 because of the missing grep — **they would have passed with the marker code deleted** | **"Delete the code under test. Does the cell still pass?"** If yes, it was never testing that code |
| **d** | **THERE IS NO CELL AT ALL** | `cores_idle`: **zero cells for its predicate**, which is how the docstring said `n == 0` for a whole session while the code said `n < expected` and `--selftest` stayed green · `replay_throws`: shipped a published-output instrument with no selftest | **"Which branch does each cell touch?"** Enumerate branches, not cells — a suite can be green and untouched |
| **e** | **THE CELL DRIVES A PARALLEL IMPLEMENTATION** | `replay_throws` first draft: extracted `is_border()` **for the test** and left the decoder's inline copy in place — the test would have passed forever against code that does not ship. **Self-caught before push** | **"Is the line the test calls the line that SHIPS?"** `ship_watch`'s own docstring already states it: *"anything you retype is a second implementation, and the second implementation is the one nobody tests"* |

**⭐ THE INSTANCE THAT MAKES THIS A CHECKLIST ENTRY RATHER THAN AN OBSERVATION:
category (e) was committed INSIDE THE COMMIT THAT ADDED THE TEST FOR CATEGORY
(d), by the lane that had just catalogued (a)–(c).** Knowing the taxonomy did not
prevent the fault; **asking the question did** — *"what is this cell actually
touching?"* is what caught it, and it is the same question that found the other
four. **That is D68's shape and it is why the CHECK column exists: the categories
are for diagnosis, the questions are the instrument.**

### THE WATCH FORM
**A green `--selftest` may not be cited as evidence that a tool is correct.** It
is evidence only that the cells present were driven. Before trusting an
instrument whose output gets published, run the five questions above **per
guard, per branch** — and prefer the cheapest one first: **(d) is answered by
counting, (c) by deleting a line, (e) by grepping for a second definition.**
**AND THE POSITIVE OBLIGATION, which is the standing repo rule this row
operationalises:** a cell must have been **seen to produce the OTHER verdict**.
The gold standard shipped today is `replay_throws`' size trap — **`(13,1)` reads
BORDER on antler 14×18 and INTERIOR on 26×26, the same coordinate, changing only
the map** — so any regression to an assumed size fails loudly rather than
silently confirming the null.

*Attribution: the eight instances came from all three lanes; the side lane split
them into categories and supplied (d)'s second instance and the questions; the
research arm supplied (a)–(c), then produced (e) by committing and catching it.*

### ⭐ D23 REFINEMENT, added the same day by the finding that would have been BLOCKED by D23 as first written

**D23 asks *"can the OPPONENT experience the mechanism?"* and routes a `no` to
COST SCREEN. Read carelessly that says immune fixtures are only ever a
consolation prize. THAT IS WRONG, and the counter-example landed within the
hour** (`8db6390`).

**AN IMMUNE FIXTURE IS THE *CORRECT* INSTRUMENT FOR MEASURING DOSE.** The
builder's dose counter detected a launch as a Chebyshev jump in the victim's own
position log — **and a crashed victim stops logging**, so **the denominator
shrank exactly when the treatment succeeded.** Immortal-time selection with the
sign pointing at the treatment: the same shape that reversed the s32 kidnap
closure. **It surfaced not by inspection but from a 7× swing on an UNCHANGED arm**
(1.17 vs 8.06 throws/game, same tree, same probe, same maps, different seed
block) — *a 7× swing on an unchanged arm is not variance, it is a fixture
measuring something other than what it names.*

**The fix was to measure dose against `_probe_border_guard`**, and the reasoning
is the general rule: **dose is a property of OUR bot, not of the victim, so
measuring it against an immune target is not a compromise — it is the correct
fixture**, because immunity removes the feedback loop by construction.
Re-measured, 32 games/arm, zero crashes both sides, exposure within 3%: **5.8×
the border dose per exposed round, border share 25.0% → 80.0%** (the earlier
"4×" was measured on the biased counter and UNDERSTATED it).

⇒ **THE RULE, stated so D23 cannot be misapplied: MATCH THE FIXTURE TO THE
QUANTITY, not to the plank.**

| quantity | correct fixture | why |
|---|---|---|
| **DOSE** (how often do we deliver it?) | **IMMUNE** | a property of OUR bot; immunity removes the outcome→exposure feedback |
| **LETHALITY** (does it kill when delivered?) | **VULNERABLE** | needs the mechanism to be able to occur |
| **CURRENCY** (does it pay?) | **LIVE UNRATED** | needs the FIELD's guard rate, which neither of our fixtures has |

**AND THE SECOND FIX IS THE GENERALISABLE ONE:** report the dose **per EXPOSED
VICTIM-ROUND**, not per game, so any residual difference in observation time
cannot masquerade as a difference in rate. **Any per-game rate whose denominator
can be shortened by the outcome needs an exposure denominator instead** — that is
the risk-set correction, arrived at independently in a second instrument on the
same day.

---

## D25 — **A PROXY IS NOT THE CLAIM. FIVE INSTANCES IN ONE SESSION, ALL FROM THE LANE THAT AUDITS**

**Promoted s33, 2026-08-12, on an evidence base that is entirely this lane's own
errors. Cheaper than D24 and it catches a superset of D24(c).**

**THE RULE: when the claim is *"does X hold"*, RUN X AND READ ITS OUTPUT.** Never
substitute a signal that merely correlates with X — a grep hit, a cell count, an
exit code, the presence of a harness.

| # | the claim I was making | the PROXY I measured | what it cost |
|---|---|---|---|
| 1 | *is `queue_check` tested?* | grep for `^\s*check(` | reported **0 cells**; it asserts **23** |
| 2 | *is `elo_logger` tested?* | grep for an **in-file** `--selftest` | reported **0**; four cross-implementation cells live in `tests/`. **Published a fleet table whose headline was false and which REALLOCATED ANOTHER LANE'S WORK** |
| 3 | *are `PROGRAMME.md`'s fields unique?* | an awk pipeline over the field names | mangled them into `DUPLICATE x20` — **garbage, not a verdict** |
| 4 | *which fields are declared?* | `grep -E '^    [A-Z_]+:'` | **silently dropped `R1000_IS_DEFEAT`** — the character class excluded digits |
| 5 | *does `target_value.py` run?* | **the exit code** | reported no-args as `** CRASHES **`; it prints a **clean usage message with zero tracebacks** and exits non-zero by design |

**⛔ AND #5 IS A RULE THIS REPO ALREADY HAS, APPLIED TO THE WRONG TARGET.**
`CLAUDE.md` states **"EXIT CODE IS NOT A HEALTH SIGNAL ON THIS PLATFORM"** and
prescribes gating on the **presence of the load-bearing field**. That was written
about `fcode`; **I applied an exit code as a health signal to OUR OWN TOOL, hours
after quoting the rule at another lane.** A rule scoped to one surface does not
generalise itself.

**ALL FIVE WERE SELF-CAUGHT, FOUR OF THEM WITHIN MINUTES — AND THAT IS NOT A
DEFENCE.** #2 stood long enough to move a lane's plan. **The mechanism that caught
each one was the same: going to USE the number for something.** Not diligence,
not review — the second instrument was always *"now do the thing the number was
for"*.

### THE WATCH FORM
Before publishing any audit figure, name the **claim** and the **measurement** in
one sentence and ask whether they are the same thing. *"Is it tested"* measured by
*"does the file contain the string `selftest`"* is two different sentences.
**Three cheap habits close most of it:** run the thing rather than grepping for
it · **read the OUTPUT, not the return code** · and when a count is the claim,
derive it from the same list the code uses rather than re-deriving it externally.
**RELATED BUT DISTINCT, and it needs its own check:** the `elo_logger`
double-count hazard I invented came from reasoning about the **reader's**
arithmetic and never opening the **writer** — that is D24's *open the primary*,
not a proxy failure. **Proxy failures mis-MEASURE; artefact-inference
mis-LOCATES.**

---

## D26 — **REPLICATE ON A RULE, NOT ON A RESULT. A SELECTED FIRST RUN MAY NOT BE POOLED WITH ITS REPLICATION**

**Promoted s33, 2026-08-12, from a flag OF MINE THAT WAS WRONG. Research's
correction; the mechanism is the third instance of one bias family in one
session.**

**WHAT I CLAIMED:** `GUNBLANK` read **52.11%** and its replication **50.30%**;
the runs do not differ significantly (`z=1.88`), so under this repo's own
*"pooling is the default, not a luxury"* the pooled read is **51.20% ± 0.94,
excluding 50** — and *"does not replicate"* was the wrong reason for a no-ship.

**WHY IT IS WRONG, and I verified the premise in the primary before conceding:**
**`GUNBLANKREP` is the ONLY replication in the entire worklist.** Thirteen arms
ran; exactly one was replicated, **and it was the highest reader of the set**
(52.11 > GUNSEAT 51.04 > GUNPEN16 50.72 > GUNFERRY 50.20 > CAP6B 49.00 …).

⇒ **REPLICATION WAS SELECTED ON THE FIRST RESULT. That makes the first run a
WINNER'S-CURSE estimate — `E[first | selected for replication] > true` — and
pooling a selected estimate with an unselected one INHERITS the upward bias.**
**The replication alone is the unbiased estimate: 50.30%, inside its band.**
Research's corrected phrasing — *"the unbiased estimate does not clear 50"* — is
right and is a **stronger** statement than the one it replaced.

**⭐ AND IT IS THE SAME BIAS FAMILY AS THE OTHER TWO TODAY, WHICH IS WHY IT GETS
A ROW:** the kidnap estimator (the thrown arm conditioned on having survived to
be thrown) · the dose counter (denominator shrinks exactly when the treatment
succeeds) · **and now, which arms get a second run conditioned on how the first
one read.** **Three instruments, three lanes, one shape: SELECTION ON THE
OUTCOME.** The first two were caught in the estimator; this one lives in the
EXPERIMENT SCHEDULE, where no estimator can see it.

### THE WATCH FORM
**Ask what selected this sample, and whether the thing that selected it is
correlated with the thing being measured.** For a replication the question is
concrete: **was this arm replicated because of a RULE (every arm · a pre-declared
subset · a fixed cadence) or because of its RESULT?**
* **Selected on a result ⇒ THE REPLICATION IS THE READ.** Do not pool; the first
  run is a discovery, the second is the estimate.
* **Selected by a rule ⇒ POOL**, per the standing pooling doctrine, which remains
  correct for unselected windows and is what `CLAUDE.md` is talking about.
**⚠ THE TWO RULES GIVE OPPOSITE ANSWERS ON THE SAME NUMBERS, so which one applies
must be fixed BEFORE the replication is ordered, never after both are read** —
otherwise the choice of rule is itself selected on the outcome, one level up.
**Cheapest fix: declare the replication trigger when the first shard is queued.**

### ⛔ D26 AMENDED SAME DAY — attribution corrected, the pattern is TWO instances, and it reaches the SHIPPED INCUMBENT

**1. THE CREDIT WAS WRONG AND IT RUNS THE OTHER WAY.** I wrote this row crediting
the research arm. **The winner's-curse counter-argument is the BUILDER's, produced
with its own simulation.** **BOTH review lanes — research and this one —
independently made the SAME pooling error, and the lane whose plank was under
review talked both of us out of it.** That is the direction credit rarely runs
and the row must record it accurately: **promoted from flags of both review
lanes that were wrong, corrected by the builder.**

**2. THE PATTERN IS TWO INSTANCES, NOT ONE — which strengthens the row.** My
*"only replication in the worklist"* was true as scoped and understated
unscoped. **`GUNAXREP` also exists** (earlier worklist, `scratchpad/overnight/`,
**verified by me: 52.31%, n=5,408**), replicating **GUNAXIS at 51.94%** — again
a high reader. ⇒ **Across both worklists, replications have gone to high readers
TWICE and to nothing else.** A schedule-level selection pattern, not a one-off.

**3. ⭐ IT APPLIES RETROACTIVELY TO THE LIVE INCUMBENT, AND THE ANSWER DOES NOT
CHANGE.** **v114 shipped on GUNAXIS 51.94% replicated at 52.31%.** Under rule 1
of this row, if `GUNAXREP` was ordered *because* GUNAXIS read high, then
**51.94% is itself a selected estimate and 52.31% is the unbiased read.**
**52.31% ± 1.33 = [50.98, 53.64] — it clears.** ⇒ **The incumbent's evidence is
UNHARMED; it should simply be stated on the REPLICATION ALONE rather than on the
pair.** *(Note the replication read HIGHER than the original — a winner's-curse
estimate usually regresses down, so this is consistent with a true rate near 52%
and the first run being an unremarkable draw, not with an inflated discovery.)*
**Nothing here reopens the ship**; the rule is applied to it because a successor
will ask whether it was, and the answer should be on the record before they do.

---

## D27 — **PRICE THE EXPECTED EFFECT BEFORE QUEUEING. AN ARM WHOSE PREDICTED SIZE IS BELOW THE BAND IS A SHARD SPENT ON A NUMBER INDISTINGUISHABLE FROM ZERO**

**Promoted s33, 2026-08-12, from LOKI-43 `LAUNCHRENT` — withdrawn BEFORE FIRING,
which is the outcome this row exists to make repeatable.**

The four-part queue admission already demands *"a fixture that can resolve it"*.
**Nobody was checking the other half: whether the EXPECTED EFFECT clears the
fixture's resolution.** LOKI-43 had a real mechanism, a legal API, a clean
design and a queued shard — and its predicted size was **~24 Ti on a ~568 Ti
build-out**, far below what **±1.33pp at n=5,408** can resolve. **A shard spent
there buys a number indistinguishable from zero, and 5,408 games is ~3.5 hours
of the machine under `ALWAYS_BE_RUNNING`.**

**HOW IT WAS PRICED — three lanes, each supplying a term, none of them right
alone:**
```
rent  = (n_cycles - 1) x 20 x S        saving = 0.10 x remaining base cost
side lane   supplied the FORM, and the caveat that n is bounded by GEOMETRY not throws
research    instantiated it: n=5, 169 Ti  ->  240 vs 17 Ti, "14x short"
builder     attacked 169 -> measured 260 Ti (moves 54% TOWARD the plank)
builder     then measured the decisive term nobody had: 0.62 launcher deaths/game, NOT 5
            (self-destruct fires only on the EXILE branch; rebuild needs the Core to
             lose sight of a launcher -- cycles bounded by geometry, exactly as flagged)
CORRECTED   rent 25-50 Ti vs saving 26 Ti  ->  NET +1 to -24 Ti, roughly BREAK-EVEN
```
**Both review lanes were wrong in OPPOSITE directions and the plank's own author
corrected both** — the same credit direction as D26, twice in one session.

**⭐ THE FINDING IS THE SYMMETRY, and it generalises past this plank:** *the rent
cycle fires rarely, which caps the cost — and caps the benefit with it.*
**The property that made it look safe is the property that makes it worthless.**
Watch for it wherever a plank's risk is bounded by a rate: **the same rate bounds
the payoff, and a mechanism that cannot hurt you often usually cannot help you
often either.**

### THE WATCH FORM
**Before a shard is queued, state the expected effect in the units the shard
reports, and compare it to the band.** Three outcomes:
* **predicted >> band** → run it;
* **predicted ≈ band** → run it only if the direction alone is worth the cores;
* **predicted << band** → **do not run it.** A null there is uninformative by
  construction and reads as evidence of absence to everyone downstream.
**MECHANISM CONFIRMED IS NOT MAGNITUDE.** LOKI-43's mechanism is engine-real and
was measured (**0.62 launcher deaths/game against the control's 0.00** — the
self-destruct and the rebuild both work). **Record that, then decline the shard.**
Same shape as **E-22.3**, which died the same way; **the two now cite each other,
which is D14 satisfied prospectively rather than after a rediscovery.**

**⛔ D27 SCOPE, added by its author within the hour, because as first written it
could be used to refuse work the programme owner asked for.** Magnus's standing
directive today is *"Today is experimentation day, we focus on building bots and
load them."* **D27 is a DEFAULT for choosing between candidate arms when cores
are the binding constraint. It is NOT a veto, and it does not outrank a
directive.** A checklist row promoted by a review lane cannot override the person
whose programme it is — **and a successor quoting D27 at a "load them all"
instruction would be using my row to do exactly that.**
**The compatible reading, and it is the one intended:** when Magnus says load
them, load them; **D27 governs which arm to queue NEXT when the queue is longer
than the cores**, and it governs whether to write *"no effect"* or *"below the
band"* when the result lands. **LOKI-43 was declined on D27 grounds by the
plank's own author, not imposed on them by a reviewer** — that is the intended
mode of use and the row should be read through it.

---

## ⛔⛔ D28 — **THE INSTRUMENT WAS RIGHT AND THREE LANES DID NOT READ IT. THE SIDE LANE ASSERTED A STALE HOLDER FOR FIVE AND A HALF HOURS**

**This row is a correction of MY OWN work and it is the worst error of s33.**

**THE TIMELINE, from `corpus/ship_watch.log`:**
```
08:57:53Z  v114  k=41   <- last v114 row
09:17:53Z  v115  k=1    <- teammate x3r0's ship, live on OUR slot
```
**My last read of that tape was 08:55:44Z.** I did not read it again for **five
and a half hours**, and in that window I:
* **committed a drift-watch amendment headed *"IT APPLIES RETROACTIVELY TO THE
  LIVE INCUMBENT"* about v114 — at 10:55Z, ~1h40m after v114 stopped being the
  incumbent.** ⇒ **CORRECTED HERE: every reference to v114 as "the live
  incumbent" in the D26 amendment means "the incumbent AT THE TIME OF THAT
  SHIP". The live holder since 09:17:53Z is v115.** The D26 reasoning about
  GUNAXIS/GUNAXREP is unaffected — it is about how v114's evidence was read —
  **only the word "live" was false.**
* **reported "v114 stable" in a state summary at ~14:26Z.**

**⭐ AND THE INSTRUMENT WAS NOT AT FAULT — IT REPORTED THE CHANGE IN TWO COLUMNS.**
`ship_watch` printed `v115` from 09:17:53Z, **and `net_act_src=env`** — the
derived-baseline column I added this morning correctly failing over, because a
brand-new holder has no `ladder_games` rows to derive from. **The monitor
signalled the handover twice and I read neither.** The builder reports the same:
*"ship_watch has been printing v115 since at least 11:57Z and I read that log
twice today without noticing the version column had changed."*

**⇒ THIS IS D20's MIRROR AND IT IS THE MORE DANGEROUS DIRECTION.** D20 is a DEAD
gate masked by humans checking manually. **D28 is a LIVE, CORRECT gate that
nobody reads** — no amount of instrument-hardening fixes it, and today four
instruments gained freshness columns while the one column that had already
changed went unread by three lanes.

**⚠ AND IT NEARLY COST A TEAMMATE THEIR SHIP.** The builder was one command from
firing a live leg with a rollback target **hardcoded to v114**, which would have
submitted a prototype over x3r0's live ship and then "restored" the wrong
version, leaving their bot off the ladder. **`submit_clean.py` reads the holder
before submitting and would have prevented it; the script bypassed it by passing
`--activate` with a hardcoded 114.** Caught by near-miss, not by process.

### THE WATCH FORM
**A state claim has a clock. Re-read the primary before asserting live state, and
quote the row's timestamp with the claim** — *"v114 stable"* with no timestamp is
the same defect as a drawdown with no n. **Concretely for this lane: the holder
version is the FIRST thing to re-check at every state report, not the last, and
`HANDOVER.md` naming a holder is a CACHE, not a source.**
**AND FOR ANY SCRIPT THAT SUBMITS: never hardcode a rollback target. Read the
`Active bot:` line at fire time** — `submit_clean.py` already does this and must
not be bypassed with `--activate` plus a literal version.

---

## D29 — **A SPARSE, CASE-SENSITIVE COLUMN RETURNS A CLEAN ZERO TO ANY CUT THAT DOES NOT CHECK. `meta_join.tsv` BIT THREE TIMES IN ONE DAY**

**Promoted s33, 2026-08-12. Research's finding, from their own three misses.
`CLAUDE.md` already warns about this surface for a NARROWER reason — *"NEVER
`meta_join` for a win-rate denominator"* — and that rule does not cover what
happened twice more today.**

**THE THREE INSTANCES:**
1. **Morning, target selection:** `our_won` is **empty in 18,575 of 24,203 rows
   (77%)**; counting blanks as losses turned a **118W-62L** record into
   *"23.4% share"* and set the wrong leg target. *(Caught before lock.)*
2. **Pooled the wrong population:** `throws.tsv` carries **every** throw by both
   teams; an unfiltered cut read **median insert r301, 31% before r160** —
   flatly contradicting the truth.
3. **⭐ THE SILENT ONE:** filtering `us_side == "A"` returned **ZERO of our
   throws** — because the column holds **lowercase `"a"`/`"b"`**. **A
   case-mismatched comparison matches nothing rather than erroring.** And
   `us_side` is **`"none"` in 20,678 of 26,501 rows (78%)** — the same sparsity
   that made `our_won` unusable in instance 1.

**Correct answer, once the cut was right: n=3,913 inserts over 1,915 attributable
games, median insert r82, median FIRST insert per game r27, 74.6% before r160.**
*(This is the number that confirmed the DELVSDEF fixture asymmetry — the ferry
does deliver early, so that flag rests on a measurement rather than an
inference.)*

⇒ **THE GENERAL FORM, which is what earns a row: a column that is MOSTLY EMPTY
and CASE-SENSITIVE is indistinguishable, to any filter, from a column where your
predicate is simply false.** An empty result set is the same shape as a real
zero. **The failure is silent, it errors nowhere, and it produces a
publication-ready number.**

### THE WATCH FORM
**Before filtering on any column, check its FILL RATE and its VALUE DOMAIN**
(`sort | uniq -c` on a sample beats an assumption; both defects were one command
away). **And run the POSITIVE CONTROL IN THE SAME COMMAND as the real cut** —
research's own D82 from this morning, and the thing that caught instance 3:
**a cut returning 0 of our throws, when we demonstrably throw thousands, indicts
the harness and not the corpus.** A zero that is *impossible* is the cheapest
alarm available and it fired here for the third time today.
**SCOPE EXTENSION:** `CLAUDE.md`'s existing rule bans `meta_join` for **win-rate
denominators**. **That is too narrow — the hazard is any filter on any sparse
column of that surface**, and two of today's three instances were not
denominators at all.

### ⛔ D27 REFINEMENT 2 — **PRICE AGAINST THE OUTCOME THE MECHANISM ACTUALLY TARGETS, VERIFIED IN THE CODE. I PRICED LOKI-44 AGAINST THE WRONG ONE AND HELPED CANCEL IT.**

**LOKI-44 was cancelled twice on two different wrong reasons and re-queued on
Magnus's catch. I contributed to the first one.**

**MY FLAG SAID:** *"~2 extra volleys, ~36 damage… **against builders at 40 HP
that is 1–2 early kills; against a 500 HP core it is noise.** Which of those it
is decides whether the plank clears ±1.33pp."* **The verification that followed
counted ENEMY BUILDER DEATHS in r13–20 and found the window empty.**

**⛔ THE SENTINEL IS NOT AIMED AT BUILDERS.** `raid.py:415` sets
`tiles = core_tiles(E)` — **it is aimed at the CORE, and core damage produces NO
DEATH EVENT until the core falls.** ⇒ **Nothing that cut counted could ever have
shown the effect.** I offered the builder framing as the live possibility
**without opening the targeting code**, and the measurement followed the framing.

⇒ **REFINEMENT: D27 says price the expected effect. That is only safe once you
have VERIFIED WHAT THE MECHANISM ACTS ON.** Pricing against an assumed target
produces a confident number and a measurement aimed at the wrong outcome —
**worse than not pricing at all, because it looks like diligence.** The check is
one grep of the targeting line.

**AND THE SECOND WRONG REASON IS WORTH RECORDING BECAUSE IT INVERTS:** the plank
was then cancelled on *"their core heals ~16 HP/round against our 6, so the
damage is refunded"*. **A builder gets ONE ACTION PER TURN and acting is
MUTUALLY EXCLUSIVE WITH MOVING** — so four healers cost the enemy **4 Ti AND four
builder-actions per round, pinned in place**, against ~5 Ti/round of ammo on our
side. **THE ABSORPTION IS THE WEAPON, not evidence the mechanism failed.** If the
sentinel's job is **PINNING** rather than killing, filling its magazine sooner
pins sooner, and the value is not bounded by whether the damage survives the heal
line.

**⭐ AND THE CORRECT USE OF D27 SURVIVED BOTH ERRORS**, declared before the data:
**game share at n=5,408 resolves 1.33pp, while the quantity that tests the pin is
ENEMY BUILDER-ACTIONS DENIED per round — which the replays can measure and a
win-rate shard cannot.** ⇒ **A null here means "under 1.33pp", never "the pin
does not work."** That is D27 used to SCOPE a conclusion rather than to cancel a
run, which is the mode the first scope note already said was intended.

- **⭐ THERE IS A THIRD TIER OF API AUTHORITY AND NOBODY HAD NAMED IT (s34,
  2026-08-12, side lane + research within twenty minutes, on `#23`'s premise):**
  `CLAUDE.md` says *read the engine binary, not the organisers' doc*, which
  presents a two-tier world — the `.so` (authoritative, expensive) and
  `official-docs.md` (cheap, known-wrong). **There is a cheap middle tier and it
  is already installed: `.venv/lib/python3.13/site-packages/fcode/_types.py`,
  shipped BY the organisers with `py.typed` beside it.** It carries **per-method**
  contracts on the method's own docstring line — `get_nearby_buildings` reads
  *"Return ids of all buildings within dist_sq (defaults to vision radius)"*, and
  `get_nearby_tiles` carries a second sentence the others do not (*"dist_sq must
  not exceed the vision radius"*) which **corroborates the binary's own
  `dist_sq exceeds vision radius` guard string** (`engine-source-crash-and-
  launcher-2026-08-10.md:46-50`).
  **WHY IT EARNS A NOTE RATHER THAN A FOOTNOTE: the failure it prevents is
  READING ACROSS ROWS.** `#23`'s premise — that a no-argument
  `get_nearby_buildings()` defaults to vision — was taken from the **neighbouring
  `get_nearby_tiles` row** of a summary table, because that is the only row
  carrying the parenthetical. **A table invites the read-across; a per-method
  docstring cannot be read across.** Both lanes independently searched
  `official-docs.md`, found nothing, and one of them published *"not established
  anywhere I can find"* — **which was a claim about where they had looked,
  wearing the clothes of a claim about the repo.**
  **⚠ AND THE TIER HAS A CEILING THAT MUST TRAVEL WITH IT: the bodies are `...`.**
  `_types.py` is a STUB, so this is a **docstring, not an implementation** — and
  *"a docstring read as the code"* is one of the four recorded instances of this
  lane's characteristic failure. ⇒ **RANKING, and it is the usable output:
  `.so` probe > `_types.py` (cite WITH the stub caveat) > `official-docs.md` /
  `CLAUDE.md` tables (never read across rows).** **`_types.py` demotes a probe
  from BLOCKING to LOW PRIORITY; it never retires one.**
  **Dead end recorded so nobody re-walks it:** the `.so` carries **no
  docstrings** and `fcode_engine` exposes only `run_game` — `Controller` is not
  importable, so the top tier is a BUILDER-OWNED behavioural probe
  (`get_cpu_time_elapsed`-style call loop), not introspection.
  **⭐ OUTCOME, SAME HOUR (`0686fdc`): THE TOP TIER WAS RUN AND THE MIDDLE TIER
  HELD.** The builder built `bots/_probe_nearby_default` and executed it:
  **`D == V` in 100% of informative rows over 9 games, never wider**, so the
  no-argument default IS the caller's vision radius and research's premise (and
  `_types.py`) are confirmed **on the engine**. ⇒ **The ranking above did its job
  rather than merely being stated: `_types.py` correctly demoted the probe from
  blocking to low-priority, the probe was still run, and it agreed.** Worth
  copying as a probe design: the decision rule is pre-registered with **all
  three** outcomes including a **SKIP for non-evidence**, and it carries the
  control that makes a MATCH mean something — `D == V` is informative only if
  buildings exist beyond the caller's vision, so the probe measures that too and
  **refuses rather than printing a clean PASS** when they do not.

- **⭐ `INSIDE-BAND ⇒ NO SHIP` IS UNBIASED PER DECISION AND BIASED IN AGGREGATE
  (s34, 2026-08-12, side lane, from the builder's NEG-cell judgement):** the ship
  gate's three branches were checked and the reasoning is sound — **both OUTSIDE
  branches are power-independent in INTERPRETATION** (once a value is outside the
  band, power governed the *probability* of getting there, not what it means),
  **and the inside-band branch maps to NO SHIP under both the "no effect" and the
  "no power" reading.** So a missing negative control does not corrupt any single
  gate decision.
  **⛔ AND THAT IS EXACTLY WHY THE AGGREGATE FAILURE IS INVISIBLE: a fixture that
  lacks power lands inside-band SYSTEMATICALLY, and inside-band always resolves
  for the INCUMBENT.** A power deficit therefore does not produce random
  no-ships — **it produces a standing preference for the bot already on the
  slot**, recurring at every gate, with every individual decision looking
  correctly reasoned. **This is research's D32 shape one level up** (they flagged
  that `DELVSDEF`'s null was both the weaker branch and the status-quo-preserving
  one; the same collision is built into the ship RULE, not just that leg).
  ⇒ **WATCH FORM: `inside-band ⇒ NO SHIP` may not be applied on a contrast with
  no NEG cell.** The rule silently converts *"we could not measure"* into *"the
  incumbent keeps the slot"*, and with **~420 rated matches left in the whole
  game** that is the expensive direction to be wrong in. **A NEG cell is the
  price of reading a null as a decision rather than as a non-result.**
  *(Companion, same session: a NEG cell also licenses the inside-band branch's
  WORDING — "the arm cannot separate from the holder" is a claim about the ARM,
  while without NEG the honest sentence is "this fixture could not resolve a
  difference", which is a claim about the FIXTURE.)*

- **⛔⛔ D30 — `ALWAYS_BE_RUNNING` STRUCTURALLY BLINDS THE INSTRUMENT THAT READS
  THE ONLY EVIDENCE THIS PROGRAMME ACCEPTS AS AUTHORITATIVE. TWO PROGRAMME FIELDS
  IN DIRECT CONFLICT, and neither document knows about the other (s34,
  2026-08-12; builder's measurement, side lane's framing).**
  `tools/corpus/keeper.py:57` sets `LOAD_CEILING = 6.0` and `:212` defers the
  **decode** above it. **`PROGRAMME.md` carries `ALWAYS_BE_RUNNING: yes` — idle
  cores are a DEFECT — so a fully-loaded box is the NORMAL state, not an
  exception.** Measured this session: **every keeper cycle deferred at load
  9–15**, and the live 1-minute average read **16.25 against the 6.0 ceiling**.
  ⇒ **The decode does not defer occasionally. It defers essentially always, BY
  CONSTRUCTION, and it will keep doing so exactly as long as we honour the core
  value.**
  **THE COST IS NOT HYPOTHETICAL AND IT LANDED TODAY:** `95e14c55` — a **RATED
  0-5 loss by the LIVE HOLDER v116** — sat on disk with **0 rows in
  `corpus/events.tsv`** for over an hour, invisible to all three lanes. It was
  read only because **Magnus asked about a replay** and this lane decoded it
  straight off `replay_archive/`. **The most informative rated match of the day
  was unreadable while every lane had instruments pointed at the corpus.**
  **⭐ WHY THIS IS A PROGRAMME ROW AND NOT AN OPS TICKET: the conflict is with
  `FIXTURE_OF_RECORD: live_unrated` and D12** (*a refutation without live-game
  backing is a hypothesis*). **This programme makes LIVE evidence the authority
  and then runs a machine configuration under which live evidence is the one
  thing that does not get ingested.** The busier we are — i.e. the better we obey
  the core value — **the blinder we get about what the ladder is doing to us.**
  **ROUTED (builder owns `tools/`), and the asymmetry is the fix:** our own rated
  matches are **a handful of files a day**, not the 27k-replay archive the ceiling
  was written to protect. ⇒ **decode OUR RATED matches at a much higher ceiling
  (or unconditionally, or triggered after a leg), and keep the ceiling for the
  bulk archive.** **The ceiling is correct for what it was written about and is
  being applied to a population a thousand times smaller.**
  **WATCH FORM:** when a monitor reports a deferral, ask **what fraction of
  cycles defer** — a guard that skips 100% of the time is not a throttle, it is
  an OFF switch that reports as a throttle. *(Same family as an alarm that cannot
  fire and an alarm that cannot tell it is blind; this is the third species: a
  throttle whose precondition is guaranteed by policy.)*

- **⭐⭐ D31 — AN EXPECTATION-SHAPED QUERY RETURNS SOMETHING PLAUSIBLE, AND THE
  PLAUSIBLE RETURN IS WHAT STOPS THE SECOND LOOK. THE ONLY RELIABLE CATCH IS A
  DOMAIN VIOLATION, NOT A VALUE CHECK (s35, 2026-08-13; research's formulation in
  the second half, this lane's instances in the first; promoted here because all
  THREE lanes committed it within one hour and it is not in any booted file).**
  **THE SESSION'S INSTANCES, and the uniformity is the finding:**
  1. **Side lane** — extracted a commit stamp with `awk '{print $4}'`; `%an` is
     three words, so field 4 was **an author's middle name**. Printed `MISMATCH`
     against a healthy instrument.
  2. **Side lane** — read `throws.tsv` column **20** as `wincond`; column 20 is
     `winner`. Returned a clean **`0 / 1`** — *a publication-ready wrong answer.*
  3. **Side lane** — ran a cumulative-Elo ledger with an arbitrary `--since`,
     returning **−49.61 over 26 matches**, which reads as *"the trigger would have
     rolled back v116 last night."* Since-activation is **−17.50** and does not
     trip. A chosen tail wearing the holder's name.
  4. **Builder** — pre-registered *"cumulative net Elo <= -21 (**the standing
     slot-swap rule**)"* on a live ship. The standing rule is a **rolling
     five-match slope** (`slot_rule.py:129`). They reached for the rule's NAME
     instead of opening it.
  5. **Research** — ran a header dump for `wincond` and read `winner` off the
     same output; and separately a `meta_join` filter on a case-sensitive column
     returning **zero of our own throws**.
  **⛔ THE MECHANISM, and it is not carelessness — every one of these was done BY
  someone actively being careful:** *the query was shaped by what the author
  expected, so it consulted the author's expectation and was called consulting
  the source.* **Research's asymmetry is the operative half: an
  expectation-shaped query USUALLY RETURNS SOMETHING, and a plausible return is
  what stops the second look.**
  **⭐ THE CATCH THAT WORKED, IN EVERY CASE WHERE THERE WAS ONE, WAS A DOMAIN
  VIOLATION AND NEVER A VALUE CHECK.** `0/1` is not a plausible DOMAIN for a win
  condition (instance 2, caught). A zero is not a plausible domain for *our own*
  throws when we demonstrably throw thousands (instance 5, caught — D29). **7 of
  5** spent is not a legal value for a rate meter (s28, caught). By contrast
  instances 1, 3 and 4 produced values INSIDE their plausible range and were
  caught only by an external reader or by going to use the artefact — **i.e. by
  luck or by cost, not by the check.**
  ⇒ **THE WATCH FORM, one question, applicable before the result is read:**
  **"what values could this query return that would be ILLEGAL rather than merely
  surprising — and does my result sit inside that legal range for the wrong
  reason?"** A quantity with a hard bound announces its own failure; a quantity
  without one does not, and for those the only defence is that the RETURN ITSELF
  was never the check — open the primary, or run the tool at the boundary it is
  actually defined for.
  **COROLLARY FOR THIS LANE SPECIFICALLY, measured s35: ad-hoc field indexing was
  wrong 3 times out of 3** and is this lane's single most error-prone operation.
  **Count the header; never trust a remembered column number.** This is the s28
  *"validation by plausibility is not validation"* note arriving from the
  operator's side rather than the instrument's.

- **⭐ D32 — LINE POSITION IN A HUMAN-MAINTAINED TEXT FILE SILENTLY BECOMES
  PRIORITY, AND NOTHING IN THE FILE DECLARES IT (s35, 2026-08-13; builder's
  phrasing, side lane's third instance; promoted because two of the three were
  found INDEPENDENTLY on the same day and the pattern is what makes the fourth
  cheap to catch).**
  **Builder, `326a6a9`: *"a priority decision made accidentally by a text file."***
  **THREE INSTANCES:**
  1. **`tools/monitors/cores_idle.py:84`** — `next_queue_item()` returns
     `rows[0]` in FILE ORDER, while `QUEUE.md`'s own fire-order block declares
     *"THIS BLOCK SUPERSEDES POSITIONAL ORDER IN THE SECTIONS BELOW."* **The alarm
     whose design virtue is naming the next plank hands out whatever sits highest
     in the file.** *(Side lane, s35 boot. Still open.)*
  2. **`corefill` launches in worklist ORDER**, so a head-to-head Magnus asked for
     **twice** sat queued behind two attribution arms **purely by line position.**
     *(Builder, s35.)*
  3. **`fanout.sh` — ALREADY IN `CLAUDE.md` FOR DAYS AND NEVER CONNECTED TO THE
     OTHERS.** Its `fire()` retries three times then gives up; under a rate-limit
     window it cannot outwait, **the drop is systematic and always lands on the
     SAME cells — the tail of the id list.** The doc's own prescription is
     *"rotate its starting cell"*; `panel2_cal.sh` does it, **`fanout.sh` is still
     unpatched on that half.**
  **⇒ WHAT MAKES IT A CLASS RATHER THAN THREE BUGS: in all three the file has NO
  FIELD EXPRESSING INTENT.** The ordering is emergent from how the READER
  iterates, so it is invisible in the file and gets edited by people who do not
  know it is load-bearing. **The tell is a reader that takes `[0]`, or iterates
  without a sort key, over a human-maintained list.**
  **⇒ THE CHECK, prospective and cheap: for every human-maintained list a tool
  reads, ask what happens to the LAST ROW — and whether any field in the file
  expresses the intended order.** If nothing expresses it, **the file's line order
  IS the policy.** Sibling of D31: both are cases where the artefact returns
  something usable and therefore never announces that it was never asked the right
  question.

- **⭐⭐ THE UNIT OF THE CLAIM, NOT THE UNIT OF THE DATA (s39, 2026-08-14;
  research's formulation at the end of the removal-discriminator chain,
  promoted here because it unifies the day and the day proved it three
  ways):** an interval is only a guard when it is denominated in the unit
  the CLAIM is about. Turret-level intervals answer "what share of their
  turrets did we remove"; the claim was about GAMES — and the discriminator
  survived a turret-level restatement (+12.2pp "just separate") only to
  dissolve at the game level with match clustering (NO cell separates).
  Same fault, same day, two levels up: games treated as independent inside
  MATCHES (the DEFF finding, now in CLAUDE.md), and CAL-2's ± carrying no
  unit at all. **Watch form, cheap and prospective: before any interval is
  banked, ask two questions — what unit is the CLAIM about, and is the
  interval's denominator that unit?** A mismatch is not a smaller interval;
  it is an answer to a different question. Chain record: three restatements
  (51-vs-14 → +12.2pp → resolved-in-none), each smaller, each found by a
  peer, none by the author, and the surviving evidence (the round-band
  split) is precisely the contrast that lives WITHIN the claim's unit.
  Companion instrument note: `era_guard`'s selftest failed on healthy
  corpus growth within an hour of shipping (hardcoded row counts) and was
  rewritten to surface-derived INVARIANTS, mutation-tested — invariants
  catch logic errors, snapshots catch appends; a selftest that fails on
  growth is one that gets ignored.

- **⭐ A LAGGED COUNT IS BIASED IN ONE DIRECTION, AND THE DIRECTION FAVOURS
  SLEEP (s39, 2026-08-14; research's formulation after the v140-era k
  reconciliation, promoted same hour):** three reads of one era's match count
  — k=7, k=8, and the true 9 — were EACH CORRECT AT THEIR OWN CLOCK and none
  carried its clock, so the newest document under-read a THRESHOLD decision
  (`SHIP_SIT_MIN_K: 8`) as "one match off the gate" when the gate had armed.
  The structure, not the instance: **a count off a lagged surface can only be
  too LOW; a too-low count always reads "not yet" against a threshold; and
  being under a threshold is the unremarkable state, so the error never
  announces itself — it feels like caution and behaves like a silent
  deferral.** (Family: the s29 724→724 pairing-boundary blindness; R1's
  same-hour-counts-from-the-live-CLI — broken here by R1's own author one day
  after promoting it.) **Watch form: any count compared against a threshold
  carries its CLOCK and its surface's LAG in the same sentence; where the
  count sits within lag-distance of the threshold, the verdict is typed only
  after a live-CLI re-read.** Companion discipline from the same incident,
  kept because it is the half that resists misuse: the gate arming at 62.2%
  over 45 games is PROCEDURAL — the DEFF-corrected interval [~45, ~79] still
  contains 50, so "gate armed" may not do work the interval cannot support.

- **⭐⭐ A PRESCRIPTION THAT CITES A NUMBER RE-DERIVES THAT NUMBER FIRST (s40,
  2026-08-14; side lane's own defect, routed here from the arm retro because a
  finding that stops in a retro instance is unread by construction):** the
  relayed-figure fault and the wrong-prescription fault are separately recorded
  in this repo and they CHAIN. Measured instance: a peer's note said CAL-8 stood
  at *"16 accepts (80 games, floor met)"*; the true state was **8 accepts / 40
  games** (the count had summed ATTEMPTS including rate-limit rejections —
  discarding the accept/reject split, the one distinction the runner exists to
  make). This lane consumed the figure without re-deriving it, **certified a
  comparative read as legal on it**, and then issued a PRESCRIPTION — *"name a
  registered ground for the seal"* — which the builder correctly acted on,
  **hardening the false number into a false GROUND in a commit.** The
  re-derivation was one `awk` over one column.
  **⇒ THE STRUCTURE, and it is why this is not just "check your numbers": a
  relayed number sitting in a note is one lane's error, and the same number
  inside a PRESCRIPTION acquires the authority of the detection and travels into
  another lane's artefact.** The existing rule (*a fix is specified against the
  CONSUMER*) was satisfied here — the builder could and did act on it. **The
  missing half: a fix is also specified against its own NUMBERS.**
  **WATCH FORM, prospective and cheap: before a flag's FIX clause cites any
  quantity — an n, a threshold, a count, a rate — derive it from the primary in
  the same action that writes the flag.** Detection may proceed on a relayed
  figure (flagging cheaply and early is still correct); **prescription may not.**
  *(Companion, same session and same class one level down: three lanes each
  described a check they had not run — an attempt-count read as accepts, a
  whole-directory scan actually of the newest 12 files, and an eyeballed listing
  published as a count — all within twenty minutes, each caught by a peer, none
  by its author. The uniformity is the finding: "I checked" is the sentence
  least likely to have been checked.)*

- **⭐⭐ D33 — A GUARD THAT REPORTS SUCCESS ON A NO-OP. SIX INSTANCES IN ONE
  SESSION, ACROSS ALL THREE LANES, EVERY ONE COMMITTED BY A LANE AUDITING THE
  SAME CLASS (s42, 2026-08-14; converged on independently by the builder and
  this lane within minutes; promoted here because the instances are the
  evidence and the CLASS is the finding).**
  **THE GENERALISATION, and it is what makes this one item rather than six
  bugs: EVERY INSTANCE IS AN ERROR PATH THAT RETURNS THE SAME VALUE AS A CLEAN
  NEGATIVE RESULT.** Not *"the check was missing"* — **the check RAN, swallowed
  its own failure, and emitted the SHAPE OF A REAL ANSWER.**
  **THE SIX:**
  1. **side lane** — a `scipy` branch falling through to a normal
     approximation **silently**, producing an **illegal negative proportion**
     (`[-0.5%, 10.5%]`) that was published to another lane.
  2. **`target_value.py`** — `try/except: pass` around the live `fcode status`
     read, **falling back to the CACHED rating** with no indication which path
     supplied the number every prereg's gap is measured from.
  3. **`worker.sh`** — a heartbeat whose last written content is the literal
     string `RUNNING`, so **a sleeping worker and a dead one are byte-identical
     in CONTENT**; only the mtime discriminates and nothing read it. *(This
     lane declared a LOCKED leg dead on it. The instrument finding was right
     and the conclusion was wrong.)*
  4. **`cores_idle.py`** — `EXPECTED_GAMES` defaulting to `1`, i.e. the
     **retired `n == 0` predicate operationally restored by a default**, in the
     alarm whose own docstring retires it citing this lane's s31 audit.
  5. **builder** — `git add -A <path> 2>/dev/null` swallowing a failure →
     empty index → `commit` no-ops → **`push` still echoes PUSHED.**
  6. **builder (their instance, attributed, not re-derived by me)** —
     `era_guard` returning an **EMPTY LIST** for `throws.tsv` because
     `int(r["team"])` raised `KeyError` inside a bare `except: continue`, on a
     surface where **v140 genuinely makes zero rated throws**. **A blind zero
     and a real zero, byte-identical on the same table, inside the tool built
     to keep era claims honest.**
  **⇒ THE WATCH FORM, one question, applicable to any guard or tool before its
  silence is trusted: WHAT DOES THIS RETURN WHEN IT FAILS — and is that value
  DISTINGUISHABLE from a legitimate negative result?** If a swallowed exception,
  a missing key, a stale cache or an empty match yields `0`, `[]`, `OK`,
  `RUNNING` or `PUSHED`, **the guard cannot tell you it is blind and its silence
  carries no information.**
  **PRESCRIPTION: an error path must return a value OUTSIDE the legal domain of
  a real answer, or announce itself.** `CANNOT-COMPUTE` as a distinct string
  (the s42 OB13 fix) is the shape that works; `except: pass` is the shape that
  does not.
  ⚠ **AND THE REASON THIS IS A DRIFT ROW RATHER THAN AN ENGINEERING NOTE: all
  six were committed by lanes actively auditing this exact class, on the same
  night, while quoting the rule at each other.** Knowing the defect does not
  prevent committing it — **only a forced question at the moment of writing
  does.** (D31's asymmetry from the writer's side rather than the reader's:
  prefer error paths that produce ILLEGAL values, because those are the only
  ones that announce themselves.)

  **⭐⭐ D33 ADDENDUM, 2026-08-14T23:06:29Z — THE AUTHOR COMMITTED IT THREE TIMES IN FOUR
  MINUTES, INSIDE THE CHECKS VERIFYING D33 ON HIMSELF. This is not an anecdote;
  it is the closing clause's proof.**
  Applying the promoter's-first-use rule deliberately, I checked whether my own
  drift watch was alive — because its silence admits two readings (*no new
  commits* / *monitor dead*), which is D33 exactly. **The check itself failed
  the check, three ways:**
  1. `ps -o ... -p <pid> | cut -c1-90 || echo GONE` — **`cut` exits 0 even when
     `ps` finds nothing**, so the `||` branch never fires and **a dead process
     prints as a blank line: indistinguishable from a live one whose output was
     trimmed.**
  2. **Wrong subject.** The pid I checked (93898) was the *gate-2700 watch*,
     which had **exited CORRECTLY after firing** — so even a working check would
     have reported a healthy exit as a death.
  3. **The "safe" rewrite reproduced the class exactly:**
     `pgrep -fc '<pat>' 2>/dev/null || echo 0` **returned 0 while three matching
     processes existed.** `-c` is not a count flag in macOS `pgrep`; it is a
     **usage error**, and **`|| echo 0` is `except: pass` returning zero** —
     an error path emitting the exact value a legitimate negative emits.
  **⇒ WHAT CAUGHT IT WAS NOT CARE.** A `pgrep -fl` listing added for DISPLAY
  sat beside the count and **contradicted it: 0 processes while 3 were listed is
  an ILLEGAL PAIR, not a surprising one.** **A second instrument over my own
  claim** (Q4's recorded mechanism) **producing a domain violation** (D31's).
  **Neither vigilance nor knowing the rule played any part — I had promoted the
  rule minutes earlier.**
  **⇒ THE PRESCRIPTION SHARPENS: do not ask "is this guard correct?" — ask
  "print the EVIDENCE beside the VERDICT and check they agree."** A count next
  to its listing, a share next to its numerator and denominator, a status next
  to its timestamp. **The contradiction is visible even when the reasoning that
  produced it is not.**
  *(Truth, for the record: the watch was ALIVE — pids 21664 (s41) and 22570
  (s42). The wake path was never broken. **Three failed checks, and the
  underlying fact was fine the whole time** — which is why the failures were
  invisible: every wrong answer was also PLAUSIBLE.)*

- **⛔ D29 COMPANION, 2026-08-15T04:04:35Z (s42) — `corpus/throws.tsv` PRODUCED TWO FALSE HEADLINES IN ONE HOUR, BOTH HANDED TO THE PRINCIPAL. Three enumerated traps; treat this surface like `meta_join`.**
  **The builder's enumeration, adopted verbatim because they did the join and I did not:**
  1. **`life` / `core_atk` / `any_atk` / `reached` are populated for `INSERT` ONLY and read as a
     CONSTANT for `EXILE`.** Measured: INSERT has `life != -1` in **100.0% of 114,972 rows** with
     990 distinct values; EXILE in **0.0% of 243,790 rows**, ONE distinct value. **`-1/0/0/0` means
     NOT APPLICABLE and reads as a clean measured outcome.**
  2. **THERE IS NO VERSION COLUMN** (21 columns; `file … kind … winner wincond`). **Every version
     claim needs a `file → version` join, and the raw surface POOLS RATED WITH UNRATED.**
  3. **`join.tsv` covers ~3,735 files against `meta_join`'s ~44,230**, so a cut built on it
     **understates throw counts ~10× and silently misses the largest games.**
  **THE TWO FAILURES, both in one hour:** *"it NEVER died / never attacked anything"* (trap 1 — a
  constant column), and *"v140 makes ZERO exile throws across 115 rated games"* (trap 2 — no join).
  **The truth: 200 rated games / 193 EXILE throws. The UNRATED half reproduced the relayed number
  EXACTLY and the RATED half was a SIGN FLIP** — which is the pooling trap producing a plausible
  wrong answer rather than an obvious one.
  ⭐ **AND THE CORRECTED NUMBER IS SHARPER THAN THE FALSE ONE, so the conclusion SURVIVES:** the
  throws occur in **3 of 200 rated games (1.5%)** and **ONE game carries 176 of the 193 (91%)** — the
  same pathological signature as the 152-throw and 548-throw games: **a launcher latching onto ONE
  victim and cycling it, not a weapon delivered across the field.** ⇒ **#51's kill stands** (aiming a
  loop that fires in 1.5% of rated games buys nothing). **"Zero" was a STRONGER and FALSER claim
  than "1.5%".**
  **⇒ WATCH FORM: before any `throws.tsv` claim leaves a lane — name the `kind` the outcome columns
  are valid for, state the join that supplied the version, and state which file set the cut covers.**
  **A claim off this table that names none of the three has not been checked.**
  ⚠ **THIS LANE'S HALF: I REPEATED the zero-throws figure back to its originator without
  re-deriving it** (Q6′), flagged it as an unverified relay **only** because I noticed the missing
  version column — **and my "low harm, I relayed it to its own originator" assessment was luck, not
  reasoning: the same figure had already been handed to Magnus as a headline and put in the #38
  brief as a load-bearing fact.** **A relayed figure's harm is not bounded by who I said it to.**

- **⭐⭐ D34 — A FIX COMMITTED TO A SCRIPT THAT IS ALREADY RUNNING IS NOT DEPLOYED, AND EVERY
  ARTEFACT THAT PROCESS EMITS AFTERWARD STILL CARRIES THE OLD BEHAVIOUR.** *(2026-08-15T06:10:23Z,
  s43/s44. **Found by the BUILDER on their own instrument and offered to this lane for the
  checklist** — their words: "I think this generalises past this one field". Recorded with their
  attribution because a promoted finding carries whose it is.)*

  **THE INSTANCE, measured:** the corefill FIXTURE header's `workers=` field reads the constant
  `workers=1` on **5 of 5 filler-launched shards**, while the filler was launched 8-wide with 1-3
  running. **It is not a code bug.** `WORKERS=$MAX_SHARDS` landed in `1256a630` at **21:08:41Z**;
  the filler process had started at **20:25:57Z — 43 minutes earlier**. The commit is correct, the
  test would pass, `git log` shows the fix, and **the running process never read it.**

  **WHY IT BELONGS ON THIS CHECKLIST RATHER THAN IN A BUG LOG:** it defeats every verification
  this repo trusts at once. **The code is right on disk. The selftest passes. The diff is in
  version control. The commit timestamp PRECEDES the artefact.** ⇒ **a `git log` check
  "confirming" a fix was live at the time an artefact was produced is INVALID unless the process
  was restarted after the commit** — and that ordering is the natural, wrong check to run.

  **⚠ AND IT IS LOAD-BEARING RIGHT NOW, which is why it is D-numbered rather than noted:**
  `workers=` is the fleet-width field, and **SALTREF2 has just made fleet width worth 2.67pp**
  (ws1 n=5400: 49.11% → 51.78% against A1's locked [47.24, 50.98], the single change being the
  `WORKERS=40→10` fixture defect). **A constant `workers=` column cannot distinguish the widths
  whose difference is the finding** — the D19/`CLAUDE.md` "a constant column validates anything"
  failure, in the field that currently prices a live result.

  **THE WATCH FORM, three questions, cheap:**
  1. **When a fix lands in a script, ask whether an instance of that script is RUNNING.**
     `pgrep -f <script>` beside the commit; if a process predates the commit, the fix is **not
     deployed to it**.
  2. **When an artefact is dated after a fix, do NOT infer the fix was active.** Compare the
     artefact's clock to the **PROCESS START TIME** (`ps -o lstart`), never to the commit time.
  3. **A long-running monitor or runner is a DEPLOYMENT TARGET, not just a file.** Restarting it
     is part of landing the fix, and "committed and pushed" does not discharge that.

  **⛔ THE SCOPE, so this does not become a demand to restart everything:** it binds where the
  running process **EMITS A RECORD SOMEONE WILL READ AS EVIDENCE** — fixture headers, tape rows,
  monitor verdicts, heartbeat content. A cosmetic fix to a running script's log formatting is not
  a drift risk. **The trigger is: does this process write a field a later cut will trust?**

  **SIBLING OF D28** (the instrument was right and nobody read it) **and its exact inverse: there
  the artefact was correct and unread; here the artefact is read and stale.** Both are the gap
  between a fix EXISTING and a fix BEING IN FORCE.

- **⭐⭐ D35 — `HANDOVER.md` IS READ BY ONE LANE OF THREE, SO ITS CONTENT REACHES THE OTHER TWO ONLY
  THROUGH LOSSY CHANNELS — AND BOTH LOST THE SAME SCOPING, INDEPENDENTLY, INSIDE ONE HOUR.**
  *(2026-08-15T06:15:53Z, s43. Self-caught after publishing and retracting my own instance,
  `6409c3a0`; research's instance was self-reported in the same exchange.)*

  **THE STRUCTURE, verified rather than asserted:** `grep -c HANDOVER` over the three command
  files returns **builder 5, research 1, side lane 1** — and the single mention in each of the two
  non-builder charters is a **write PROHIBITION** (*"NO HANDOVER/tape writes"*), not a read step.
  **`HANDOVER.md` is step 1 of the BUILDER's boot and is in no other lane's boot sequence at all.**

  **THE TWO INSTANCES, same hour, same lost scoping:**
  * **Mine:** I met `d449720c` as a line in my drift watch and quoted its **COMMIT SUBJECT** —
    *"target_value gets it wrong in the ADMITTING direction"*, flat and unscoped — then "corrected"
    it as an over-generalisation. **The file's body scopes it to one case and states the
    bidirectionality one line down** (*"also wrong, the other way… three ratings, three verdicts"*).
  * **Research's, self-reported:** *"I had adopted the admitting-direction framing from the
    builder's RELAY this morning."* **Same content, different lossy channel, same lost scope.**

  ⇒ **NEITHER OF US READ THE FILE, AND THE STRUCTURE IS WHY.** A commit subject must flatten; a
  relay must compress. **The two lanes that never open `HANDOVER.md` both received it through a
  channel that cannot carry a caveat**, and both then acted on the flattened version.

  **⛔ AND IT COST AN HOUR OF REDERIVATION ON A LINE THAT WAS ALREADY WRITTEN.** `d449720c`
  prescribes, verbatim: *"Re-derive from `fcode team search` on **BOTH sides** before firing —
  never from `target_value`'s cached opponent column."* **Research and I independently converged on
  exactly that third surface over ~1 hour, each presenting it as a finding.** **D28's shape — the
  instrument was right and nobody read it — with the aggravating detail that the s42 wrap had
  already called `HANDOVER.md` *"the artefact most likely to be picked up cold."***

  **THE WATCH FORM:**
  1. **When a drift-watch line makes you want to correct a claim, OPEN THE FILE THE COMMIT TOUCHED.**
     A commit subject is an index entry, never the claim. **A correction sourced from a subject line
     is not a correction.**
  2. **Before publishing a fix, grep `HANDOVER.md` for the thing you are about to prescribe.** It is
     where the previous session's prescriptions live and it is the file your charter does not open.
  3. **A relayed rule carries its scope or it is not the rule** — the compression happens in the
     relay, so the relayer owns restating the caveat, not the recipient.

  **⚠ STANDING ASK, OUTSIDE THIS LANE'S WRITE SURFACE (Magnus's, as `.claude/commands/*` always
  is): the side-lane and research boot sequences should READ `HANDOVER.md`'s top block, not merely
  be forbidden from writing it.** Recorded here because routing is the only mechanism available to
  this lane — **the identical constraint is already on record at `side-lane-retro.md` v1.1 about the
  same file**, which is itself evidence that a standing ask with no route gets re-made rather than
  resolved.

- **⚠ D35 — AMENDED 2026-08-15T06:25:xxZ, TWENTY MINUTES AFTER IT WAS WRITTEN, AND THE AMENDMENT
  MAKES IT STRONGER AND MY OWN ACCOUNT IN IT WRONG.**

  **D35 as written says: *"I met `d449720c` as a line in my drift watch and quoted its COMMIT
  SUBJECT."* THAT IS NOT WHERE I GOT IT.** The research arm corrected their own provenance first
  (*"I said I'd adopted it from the builder's relay. I didn't"*) and the correction applies to me
  identically: **`d449720c`'s subject is in the `gitStatus` preamble of this session's boot
  context**, under `Recent commits:`, verbatim and flattened. **It was in front of me from message
  one — before my drift watch was armed at 05:58:16Z, and before any peer messaged me.**

  ⇒ **RESEARCH'S FORMULATION IS THE RIGHT ONE AND I ADOPT IT: THE COMMIT SUBJECT LINE IS A
  BOOT-CONTEXT SURFACE, AND IT IS THE ONE SURFACE WITH NO ROOM FOR A QUALIFIER.**

  **THIS STRENGTHENS D35 RATHER THAN REPLACING IT, because the two halves compose into something
  worse than either:**
  * **The FLATTENED version is delivered automatically, to every lane, at boot** (`gitStatus`
    preamble — no action required, no way to decline it).
  * **The SCOPED version requires a deliberate read of a file two of three lanes do not boot.**
  ⇒ **THE DEFAULT PATH DELIVERS THE LOSSY VERSION AND THE CORRECT ONE IS OPT-IN.** That is why two
  lanes committed the same error independently within one morning, with no contact between them —
  **it is not two mistakes, it is one surface.**

  **⭐ AND THE WATCH FORM GENERALISES PAST COMMITS ENTIRELY — third instance, same session:** the
  builder's `v140vs146` tape row cited `SCREEN-v140vs146:74` and reported the superiority bar, while
  **`:74-79` carries an explicit ⛔ saying that object is not the decision rule.** Subject vs body ·
  subject vs body · **line vs paragraph.** ⇒ **THE RULE IS "OPEN THE PARAGRAPH, NOT THE LINE",
  and it supersedes the surface-specific wording in D35's original watch form.** A citation with a
  line number is the shape most likely to have stopped at the line.

  **⚠ RECORDED AGAINST MYSELF: I published a checklist item whose worked example was my own error,
  and got the mechanism of my own error wrong inside it.** The detection was right and the
  provenance was not — and the provenance was the part that made it a *structural* finding rather
  than a personal one. **Q9: a correction of mine that needed correcting, caught by a peer's
  correction of themselves rather than by me.**

- **⭐⭐ D36 — REPRODUCING A NUMBER IDENTIFIES *A* PATH, NEVER *THE* PATH. TWO DISTINCT ERRORS LANDED
  0.07pp APART AND THE MATCH NEARLY CERTIFIED A WRONG ACCOUNT OF A COLLEAGUE'S MISTAKE.**
  *(2026-08-15T06:29:xxZ, s43. **My error, caught by its subject** — the research arm — not by me.)*

  **WHAT I DID.** Research published a retrospective interval of **±29.6pp** on a 5/15 cell while
  citing **DEFF 1.366**. I recomputed, found 1.366 gives **27.9** and **1.529 gives 29.5**, and
  published: *"your ±29.6 is computed at DEFF ≈1.529, not the 1.366 you cite."*

  **WHAT HAPPENED.** They had used **the correct DEFF 1.366 with `p = 0.5` hardcoded** instead of the
  observed `p = 0.333`. That path gives **29.57**.

      p=0.500, DEFF 1.366  ->  29.57   <- what they actually did
      p=0.333, DEFF 1.529  ->  29.50   <- what I inferred they did
      p=0.333, DEFF 1.366  ->  27.88   <- correct, and now adopted

  ⇒ **TWO DIFFERENT ERRORS, 0.07pp APART.** My reconstruction matched to the second decimal and was
  **the wrong story about their method**: *"used the pooled DEFF on a single-opponent cell"* is a
  **methodological** error they did not make; *"defaulted to p=0.5"* is an **arithmetic default**
  they did. **Different errors, different fixes, and only one of them belonged to them.**

  **THE RULE, and it is narrow enough to apply: WHEN AUDITING A FIGURE, REPRODUCING IT SUPPORTS THE
  ARITHMETIC AND IDENTIFIES NOTHING ABOUT THE AUTHOR'S PATH.** Under-determination is the normal
  case, not the exception — every interval has ≥2 free parameters, so a target number is typically
  reachable by several wrong routes. ⇒
  1. **State the discrepancy, not the cause:** *"I get 27.9 where you report 29.6"* is verified.
     *"You used X"* is a claim about their code and requires **reading their code or asking them.**
  2. **A reconstruction that matches to high precision is EVIDENCE OF UNDER-DETERMINATION, not of
     identification** — the closer the match, the more paths are within noise of it.
  3. **This is a Q6′ object.** It is a claim about another lane's WORK, and the standing bar is
     *what they DID, verified* — never what an artefact permits me to infer. **I inferred.**

  **⚠ AND THE ASYMMETRY THAT MAKES IT WORSE THAN A NORMAL WRONG GUESS:** the number was right, so the
  correction would have been ACCEPTED, and the false account of the cause would have entered the
  record **attached to a true correction**. **A wrong cause riding a right number is not self-
  correcting** — it is the diligence-as-disguise mechanism (Q9) pointed at a colleague.
  **They checked instead of accepting the relay, which is the only reason the record is right.**

- **⭐ D35 RIDER, 2026-08-15T07:50:xxZ — A CORRECT SENTENCE THAT RELIABLY MISLEADS HAS NO ERROR ANYONE CAN POINT AT.**
  *(Research arm's formulation, s43, on `CLAUDE.md:71`. Recorded as a RIDER and not a new D-number
  deliberately: this lane's measured cost is volume, and the shape belongs under D35's "how a fact
  reaches a lane in lossy form" rather than beside it.)*

  **THE INSTANCE.** `CLAUDE.md:71` glosses `is_tile_passable(pos)` as *"A friendly builder bot could
  stand there."* **That is TRUE** — a tile holding any bot is not passable for a friendly bot either.
  **And it reliably produces the team-scoped misreading**, because naming *friendly* in a
  description of a team-BLIND predicate implies a contrast that does not exist. The engine settles
  it: **`Tile::is_bot_passable@0x2eabc` returns false for ANY tile holding a live builder bot**
  (`engine-guard-matrix-exploit-hunt-2026-08-10.md:171`, disassembly).

  **⇒ WHY IT IS ITS OWN SHAPE AND NOT JUST "THE DOC IS WRONG":** a wrong doc can be corrected and
  the correction is checkable. **A correct-but-misleading gloss has no defect to file** — every
  reader who is burned by it was, strictly, careless, and the sentence survives every audit that
  asks *"is this true?"* ⇒ **it fails the only test we routinely apply, and keeps failing readers.**

  **THE PRACTICE, and it is one line: CITE THE ADDRESS, NEVER THE GLOSS.** Where an engine fact has
  been read off the binary, the checklist, the prereg and the queue row quote **the symbol and
  offset**, not the organisers' description of it — **including when the description is accurate.**
  **The test is not "is the gloss true" but "can the gloss be read the wrong way by someone who has
  not seen the disassembly."**

## ⭐⭐ D26 REFINEMENT 2 — **THE FOURTH SITE OF SELECTION-ON-THE-OUTCOME IS THE PRIMARY METRIC'S OWN DENOMINATOR, AND D26's WATCH FORM CANNOT SEE IT**

**Promoted side lane s44, 2026-08-16, from a PRE-FIRE catch on `FIRE ORDER #1`
(`docs/coordination.md`, `a80c27ce`; research's amendment `3a1504f5`). Filed as a
REFINEMENT and not as D30 deliberately: D26 already declares this family in its
own text — *"Three instruments, three lanes, one shape: SELECTION ON THE
OUTCOME"* — and splitting one mechanism across two rows is how a checklist stops
being usable (D14).**

**THE THREE SITES D26 NAMES:** the ESTIMATOR (the kidnap arm conditioned on
having survived to be thrown) · the SCHEDULE (which arm gets replicated) · the
DOSE COUNTER (denominator shrinks when the treatment succeeds).
**THE FOURTH, AND IT IS THE BEST HIDDEN: THE DEFINITION OF THE PRIMARY METRIC.**

**THE CASE.** A live leg pre-registered **"median kill round censored at
`KILL_WINDOW_RND`"** as PRIMARY. The censoring point was chosen impeccably — it
is `PROGRAMME.md`'s own constant, so it cannot be tuned after the fact — and the
sizing was correct arithmetic. **But "kill round" is only defined on games we
WON BY CORE KILL**, and the sizing said so in passing (*"our kill-wins = 49% of
games, inflation applied"*). ⇒ **the treatment decides which games enter its own
denominator.**
**The plank on the leg (`bodyaware`) moves win share +3.7pp, so it necessarily
moves the subset**, and the board already showed the signature: leaders reading
*win more AND kill later* (232 vs 209). **A treatment converting marginal slow
LOSSES into slow WINS adds slow kills to the numerator and reads as a kill-round
regression having caused none.**

**⛔ WHY D26's WATCH FORM MISSES IT, WHICH IS THE ENTIRE REASON THIS IS WRITTEN
DOWN.** D26 asks *"what SELECTED this sample, and is the selector correlated with
what is measured?"* **Here nothing selected the sample.** The metric is applied
identically and blindly to both arms, by a definition committed in advance, with
no per-arm choice anywhere. **The conditioning is a property of the QUANTITY, not
of any act — so a lane looking for a selection STEP finds none and passes it.**
That is what let it clear a prereg, a pricing pass, and a relay to two lanes.

### THE WATCH FORM — one question, asked of every PRIMARY before a leg is locked
**NAME THE DENOMINATOR. THEN ASK: IS MEMBERSHIP IN IT DECIDED AFTER
RANDOMISATION?** If a game's inclusion depends on anything the treatment could
have changed — won / killed / survived / reached a round / built a thing — the
contrast is not the causal one, however clean the arithmetic on top.
* **The tell is a metric that is UNDEFINED on some games.** "Kill round" has no
  value on a loss. **Wherever a metric is undefined, a selection is hiding**, and
  the sizing line that inflates for it (*"49% of games"*) is where it is visible.
* **THE FIX IS ALMOST ALWAYS AN ITT FORM: give the undefined games a defined
  value from the programme's own constants** (here: no kill inside the window
  scores the window, 250). Every randomised game contributes; nothing is
  conditioned on outcome.
* ⭐⭐ **AND PRICE IT BEFORE ASSUMING IT COSTS MORE — IT WAS 2.26x CHEAPER.**
  Measured on the live rated population (520 games / 104 matches): win-conditioned
  sd 56.4 with **DEFF 1.265**, ITT sd 53.7 with **DEFF 1.185** ⇒ at ±15 rounds,
  **539 games/arm against 238.** The collider inflates the DESIGN EFFECT as well
  as biasing the estimate, because conditioning on winning correlates games within
  a match (a 5-0 contributes five kill rounds, a 0-5 contributes none).
  **The unbiased form was the cheap one. Nobody had checked.**
* ⭐ **BEST OUTCOME: IT MAY FACTORISE, IN WHICH CASE NOBODY HAS TO CHOOSE.**
  Research's amendment: `RMST_250 = 250 − P(kill inside 250) × E[250−T | kill]`,
  **verified residual 0.0000000000**. Pre-register all three — combined primary,
  rate, conditional speed — and they multiply back, so a reader always sees which
  factor moved. **Prefer a factorisation to a definitional ruling.**

**⚠ AND THE MEASUREMENT CAVEAT THAT TRAVELS WITH THOSE CONSTANTS:** they are from
the RATED tape and the leg fires UNRATED. Any cross-fixture number is a
**PROJECTION**, and the projection itself rests on untested assumptions
(multiplicative fixture effect; a ratio measured on PROPORTIONS transferring to a
CONTINUOUS outcome). **Label it `PLANNING` and carry re-measurement as an
obligation** — this is `CLAUDE.md`'s own count-metric debt, one level up.

## STANDING NOTE (s44, 2026-08-16) — **PUBLISH THE ARITHMETIC, NOT THE VERDICT. A CONCLUSION IS AGREEABLE; ONLY WORKING IS FALSIFIABLE.**

**Formulation joint with research, from the same incident.** `FIRE ORDER #1`'s
CONCLUSION — *"win share is infeasible on the live fixture, kill round is the
cheap question"* — **survived the audit completely intact.** What died was the
ESTIMATOR, and **the defect lived in the sizing arithmetic**, in a parenthetical
about the inflation factor.

⇒ **A fire order, prereg or verdict that states only its conclusion is
UNAUDITABLE NO MATTER HOW MANY LANES READ IT.** A peer given a conclusion can
only agree or disagree; a peer given the working can falsify it. **The review
worked because the sizing was written down, not because a second lane read it.**
⇒ **When this watch grades an artefact, grade whether its load-bearing numbers
are RECONSTRUCTIBLE from what it published** — that property, not the number of
readers, is what made a wrong primary die before it fired rather than after.

## ⭐⭐ D30 — **A REPRODUCTION IS NOT A VALIDATION. AGREEMENT BETWEEN IMPLEMENTATIONS CERTIFIES THE COMPUTATION, NEVER THE ESTIMATOR.**

**Promoted side lane s44, 2026-08-16. Formulated by the BUILDER from their own error and sharpened
by RESEARCH; recorded here with attribution because both were in-channel and messages die with
sessions.** Routed to this file rather than to a retro because it is an AUDITING rule, not a
lane-specific lesson — it governs what this watch may conclude from a confirmation.

### THE INCIDENT

`RMST-ESTIMATOR-2026-08-16.md` published per-arm RMST₃₀₀ differences with 95% intervals. **THREE
LANES REPRODUCED THE POINT ESTIMATES DIGIT-FOR-DIGIT** — research computed them, the builder's
subagent recomputed them for the board, and this lane recomputed them independently (BODYAWR −6.84,
AWRLNCH −6.43, NULL114 +0.42, NEG114 +33.27). **All three agreed. All three were right. And the
INTERVALS WERE ~18% TOO NARROW ON EVERY ARM**, because the estimator was PAIRED (both arms play the
same games, `corr ≈ −0.40`) and had been computed two-sample.

**⛔ THE AGREEMENT CARRIED NO INFORMATION ABOUT THE DEFECT.** The point estimate is
`mean(T) − mean(C)` under either variance assumption — **so reproducing it could not have detected
the error, and three independent confirmations felt like verification while certifying only the
arithmetic.** The builder's own words: *"the point estimates were never wrong, so three lanes
reproducing them digit-for-digit validated nothing about the interval."*

**WHAT ACTUALLY CAUGHT IT: a FOURTH implementation asking a DIFFERENT QUESTION** — computing
`d_i = T_i − C_i` per game rather than two arm means, which makes the pairing structural and the
variance form unavoidable. **Not a fourth confirmation. A different construction.**

### THE WATCH FORM — one question, asked whenever this lane grades a claim "independently confirmed"

**ASK WHAT THE AGREEING IMPLEMENTATIONS SHARE.** They agree about whatever they hold in common and
are silent about the rest.
* **Same estimator, different code ⇒ the agreement certifies the ARITHMETIC only.** Variance form,
  clustering, denominator choice, conditioning and population are all UNTESTED by it.
* **Different estimator, same answer ⇒ that is a real replication**, and it is the only kind that
  reaches the modelling assumptions.
⇒ **A confirmation count is not a strength unless the implementations DIFFER IN CONSTRUCTION. "Three
lanes agree" and "three lanes ran the same recipe" are the same sentence until someone checks.**

**⭐ THIS SHARPENS THE s26/s27 NOTE IT SITS BESIDE, RATHER THAN REPEATING IT.** That note says *"a
different data path over the SAME sample controls for decoder error, NOT sampling error — it
confirms the path and reproduces the over-estimate."* **D30 is the same fault one layer up: a
different CODE PATH over the same ESTIMATOR confirms the computation and reproduces the modelling
error.** Sample → path → estimator; the question *"independent of WHAT?"* is the same question at
each level and this repo has now been bitten at two of the three.

⚠ **AND THE HAZARD IN THE RULE ITSELF, so it is not over-applied: DEMANDING A DIFFERENT
CONSTRUCTION FOR EVERY CHECK WOULD STOP THE CHEAP CONFIRMATIONS THAT DO WORK.** Reproducing a
number IS the right check for a transcription error, a wrong column, a stale file, a bad join —
this lane caught real defects that way today. ⇒ **the rule is not "reproductions are worthless", it
is "name which failure class your reproduction can see."** A reproduction sees the computation. It
cannot see the choice.

## ⭐⭐⭐ D31 — **A CHECK THAT DEPENDS ON A LANE BEING PRESENT IS NOT A CHECK. MECHANISE IT OR IT DOES NOT EXIST.**

**MAGNUS, 2026-08-16, verbatim: *"this should always be the case actually"*** — said of a side-lane
verification that had just stopped being load-bearing because the builder folded it into the
scheduler. **Recorded verbatim because it is a directive, and promoted here rather than to
`PROGRAMME.md` because this file is the side lane's mandate and `PROGRAMME.md` is
edit-on-his-directive-only through the builder.**
⚠ **MY READING, STATED SO IT CAN BE CORRECTED:** *a manual check performed by a lane is a
PLACEHOLDER for a mechanism, and the lane's job is finished only when the check no longer needs the
lane.* If he meant something narrower, this row is wrong and should be struck rather than reworded.

### WHY IT IS A ROW AND NOT A PREFERENCE — ONE SESSION'S EVIDENCE, BOTH DIRECTIONS

**EVERY durable win of 2026-08-16 was a lane observation converted into a mechanism:**

    clear-from-empty on the -40 halt   -> BLIND + printed age + 3-strike, in the gate
    silent unpin fall-through          -> UNPINNED_OK abort, in the runner
    starting-cell rotation             -> (k-1 mod 10), in the scheduler
    per-flip leak verification (MINE)  -> id-keyed platform read that HALTS, in the scheduler
    queue title truncation             -> ellipsis-only-when-cut, in queue_check
    gate.py's zero test coverage       -> 13-cell fixture selftest, mutation-driven
    silent rate-window wait            -> "wait Ns — same-cell retry, never advances" heartbeat

**EVERY failure of the same day was an attention-level rule that did not fire when it mattered:**
* **D28** — *"a reboot state's holder line comes from `fcode status`, never a poller"* — **committed
  by the lane that promoted it, in its own closing artefact**, having cited it twice that day.
* **D3** — *"the interpreter is part of the guard"* — **committed by me ~19 hours after the builder
  logged it**, in a monitor I armed *specifically* to close a hole in my own watch.
* **The promoter's-first-use rule fired three times**, on three lanes, on rules written that day.
⇒ **The pattern is not that people are careless. It is that a rule lives in attention and a
mechanism lives in the repository.** `PROGRAMME.md` already carries the observation —
*"attention-level rules failed under time pressure all day; script-level ones held"* — **D31 makes
it an obligation instead of a lesson.**

### THE WATCH FORM

**When this lane produces a check, ask the same question of it that it asks of everything else:
WHAT HAPPENS TO THIS CHECK WHEN NOBODY IS LOOKING?**
1. **Name the mechanism the check should become.** *"I verified the flip"* is a placeholder for
   *"the scheduler verifies the flip and halts."*
2. **Route it with the defect** — the flag arrives with its fix AND with what the fix was verified
   against (Q8's two conditions), because a flag that becomes a script is the only output that
   outlives the session.
3. **A check that CANNOT be mechanised is stated as such**, with the reason, so nobody inherits it
   as covered. **An unmechanisable check is a standing cost and must be visible as one.**
⇒ **AND THE MEASURE OF THIS LANE IS THE COUNT OF ITS CHECKS THAT NO LONGER NEED IT.** A lane whose
value depends on its own presence has built nothing; **the session's own best outcome was the
moment a peer made my verification redundant, and that is the target rather than a concession.**

⚠ **THE HAZARD, NAMED SO THE ROW IS NOT OVER-APPLIED:** *mechanise it* is not *mechanise it NOW*.
**A guard built mid-flight on a firing leg is a change to a running experiment** — today the
correct sequence was HALT → patch → selftest both ways → resume, twice. **The obligation is that
the mechanism EXISTS before the check is relied upon again, not that it exists before the current
run finishes.** And a mechanism landed without being driven to both verdicts is not a mechanism, it
is a second thing to audit — **which is the whole of D24 and the reason this row does not shorten
the path.**

## ⛔⛔ D31 — **ATTRIBUTION RETRACTED WITHIN THREE MINUTES. THE DIRECTIVE WAS ABOUT THE WRAP RULE, NOT ABOUT MECHANISATION. The ROW's CONTENT SURVIVES AS THIS LANE'S OBSERVATION; THE "MAGNUS SAID" DOES NOT.**

**Retracted 2026-08-16T07:3xZ, at the provenance record first (D21), by the lane that wrote it.**

**WHAT I DID.** Magnus wrote *"wrap when builder wraps"*, I acknowledged, and he then wrote **"this
should always be the case actually."** **Arriving immediately after my own paragraph about a
verification becoming redundant, I read "this" as THAT** — and encoded a mechanisation obligation
as **D31, attributed to him VERBATIM, in a file every side-lane session boots.**

**WHAT IT ACTUALLY WAS.** The research arm was **asked directly whether the wrap rule was a
one-off** and received the same sentence in answer. ⇒ **"this should always be the case" = the
BUILDER-WRAPS-THEN-YOU-WRAP RULE IS STANDING.** They have the disambiguating exchange and I do not.
**Their reading is almost certainly right and mine is almost certainly wrong.**

**⇒ THE ATTRIBUTION IS STRUCK. D31 IS NOT A MAGNUS DIRECTIVE.** Anything downstream that cites it as
one is citing a misread. **The `⭐⭐⭐` and the verbatim quote are withdrawn.**

### ✅ WHAT SURVIVES, AND WHY IT IS KEPT RATHER THAN DELETED

**The row's CONTENT was never his; it was the session's evidence, and that evidence is unchanged:**
every durable win of 2026-08-16 was a lane observation converted into a mechanism, and every
failure was an attention-level rule that did not fire — **D28 committed by its own promoter, D3
committed by me nineteen hours after it was logged, promoter's-first-use firing three times on
three lanes.** ⇒ **it stands as A SIDE-LANE OBSERVATION, at ordinary weight, with no directive
authority.** ⛔ **A rule can be right and its provenance false, and the provenance is the half that
was load-bearing here** — a booted file carrying *"Magnus said"* is quoted differently from one
carrying *"the side lane noticed"*. **If he wants it as a directive he can say so; until then it is
mine and it is weaker.**

### ⛔ AND THE MECHANISM IS THE ONE I HAVE NAMED SIX TIMES TODAY, NOW AT ITS WORST PLACEMENT

**I read ONE SURFACE — a pronoun, against the paragraph nearest to it — and reported a property of
the world: what Magnus meant.** Seventh instance, and the worst-sited: **not a number in a note but
a DIRECTIVE ATTRIBUTION in a booted checklist**, which is the highest-authority object this lane
can write.
⚠ **The one thing that limited it: I flagged the ambiguity in the row itself** — *"MY READING,
STATED SO IT CAN BE CORRECTED… if he meant something narrower, this row is wrong and should be
struck"* — **which is why the correction cost three minutes instead of a session.** ⇒ **stating a
reading as a reading is not a substitute for asking, and it is the difference between a retraction
and an inherited falsehood.**
⭐ **THE PRACTICE THIS EARNS, and it is narrow enough to follow: A DIRECTIVE IS NEVER ENCODED FROM A
PRONOUN. If the instruction's SUBJECT is supplied by context rather than stated, confirm the subject
before writing it down — the cost of asking is one message and the cost of guessing is a false
attribution in a file nobody re-derives.**

### ⭐ D30 RIDER — **AGREEMENT IS NOT REPLICATION WHEN THE SUBJECT IS A PERSON, EITHER**

**Added side lane s44, 2026-08-16. The re-derivation is mine; the observation of what it
demonstrated is research's, and they asked for it here under my name because this is the file I
boot. Split recorded because the halves are separable and a joint credit would hide that.**

**THE INSTANCE.** I published six retractions in a session. Research characterised them as *"six
SELF-CAUGHT instances — an instrument with a detection rate."* **I re-derived it from the actual
buckets: 3 caught pre-publication, 5 published, and of those 5 only 3 were self-caught — TWO NEEDED
A PEER.** ⇒ **their agreement with my self-assessment certified nothing, because it reproduced my
judgement rather than testing it.** What tested it was going back to the buckets.

⇒ **D30 GENERALISES OFF NUMBERS: "same estimator, different code ⇒ certifies the arithmetic only"
has a human form — SAME IMPRESSION, DIFFERENT PERSON ⇒ CERTIFIES NOTHING.** Two people agreeing
about a third person's error rate, a lane's reliability, or whose work caused what are **sharing an
impression, not replicating a measurement.** ⛔ **And this direction is the more dangerous one,
because agreement about a PERSON arrives as generosity and is socially expensive to test.** The
flattering version is the one nobody re-derives.
⚠ **Concrete guard, since the general form is easy to nod at: a claim about a lane's conduct or
output — including a favourable one, including your own — is checked against the LEDGER, not
against whether a colleague concurs.** This lane put *"0 built arms"* into three artefacts on a
figure it never re-derived; **the failure mode does not require anyone to be wrong on purpose.**

### ⭐ RIDER TO THE D31 RETRACTION — **A CORRECTION INHERITS THE AMBIGUITY OF THE THING IT CORRECTS**

**Formulated by RESEARCH, 2026-08-16, from watching me do it. Recorded with their attribution.**

**THE SHAPE, in one sequence:** Magnus's *"this should always be the case actually"* followed
*"wrap when builder wraps"*. **I OVER-READ it** as a mechanisation directive and encoded it as a
verbatim Magnus row. **Struck that correctly on research's evidence — and then drew from the strike
that *"my wrap still waits on Magnus's word, not the builder's"*, which is an UNDER-READ: he had
already given me the word, directly, in the instruction the retraction was about.**

⇒ **The correction resolved the SAME PRONOUN against a different nearby paragraph and got it wrong
from the other side.** ⛔ **A retraction feels like a checked object because it cost something to
make — and that feeling is the disguise.** *(Q9's mechanism, one level up: v1.4 already records that
"a correction inherits the authority of having been careful"; this adds that it also inherits the
AMBIGUITY, which the earlier form did not say.)*

**⇒ THE PRACTICE, and it is narrow enough to actually follow: after retracting a reading, state the
NEW reading as a separate claim and check it against the SAME primary — never treat "I have just
been careful" as coverage for what the care produced.** Here the primary was one line of Magnus's
own text, re-readable in seconds, and neither the over-read nor the under-read consulted it.
**Both errors were free to prevent and neither was prevented by diligence.**

---

## ⭐⭐ D32 — **ROUTING DEBT: THE FINDING IS SOUND, THE SURFACE CANNOT FIRE IT, AND NOBODY NOTICES BECAUSE THE ARTEFACT LOOKS COMPLETE.**

*(Added 2026-08-16T08:27:11Z. Name coined by the RESEARCH lane; definition theirs, the two additions below mine;
written by THIS lane at their explicit request — **"my lane produced two of the three instances, and
a failure mode written up by its principal offender is weaker evidence than the same text written by
the lane that caught it"**. Provenance recorded because it is doing real work here.)*

**⛔ THE TELL IS THAT THE ARTEFACT IS COMPLETE AND CORRECT.** Routing debt has **no defect to
find** — a reviewer reads the note and finds nothing wrong, **because nothing is wrong with the
note.** It survives review by being right. **That is why every other row in this checklist misses
it: they all ask whether a claim is TRUE.**

**⇒ THE CHECK, and it is the whole of the row:**
> **NOT *"is this right?"* — but *"WHAT HAS TO READ THIS FOR IT TO FIRE, AND DOES THAT THING
> EXIST?"***

**⭐ IT IS THE DUAL OF D31, NOT AN INSTANCE OF IT — state this or a successor will collapse them.**
* **D31:** a check that needs a LANE PRESENT is not a check.
* **D32:** a check that needs NO LANE and **still** cannot fire, because it was written to a surface
  **with no reader.**
**Same family, opposite mechanism.**

**FOUR INSTANCES, all 2026-08-16, across two lanes and one directive:**

| # | the correct thing | the surface that could not fire it |
|---|---|---|
| 1 | `AGENTS.md`'s regeneration rule | **an HTML comment INSIDE the generated file** — fires only if a `CLAUDE.md` editor happens to open the twin. Held 3× (`14770691`, `21a74414`, `f0eebd2e`), **lapsed across 8 commits / 4 days**, and **nothing in `tools/`, `.claude/` or `.github/` references the file at all.** |
| 2 | *"the fieldcal tape carries a number that looks like a fired falsifier"* | **a `coordination.md` note** — but **the TAPE is what a successor opens FIRST** when a number looks alarming. Fires only if the note is read before the thing it warns about. |
| 3 | **Magnus's 70% aiming point** (verbatim, 08:24:10Z) | **a 62,000-line append-only channel no lane's boot sequence opens.** Every lane is said to *"inherit"* it; **the inheritance mechanism is a successor scrolling far enough.** |
| 4 | my `AGENTS.md` drift flag naming `RMST₃₀₀` as missing from the twin | **the twin STRUCTURALLY CANNOT CARRY IT** — `RMST` is 0× in `CLAUDE.md`; it lives in `PROGRAMME.md`, which has no twin. Correct finding, aimed at a surface that could never hold the fix. |

**⚠ THE SUNSET CLAUSE APPLIES TO THIS ROW TOO, AND IT WAS THE CONDITION OF WRITING IT** (research,
verbatim): ***"the write-up must itself be routed, or it is an instance of its own subject."*** A
dated spec under `docs/research/` naming three instances **is exactly the artefact shape that reads
complete and fires for nobody.** ⇒ **It is here, in the file this lane's boot sequence opens at step
3, and not in a spec.** **If two successive runs cite it and change no behaviour, strike it.**

---

## ⭐ D33 — **A NUMBER IMPROVED RATHER THAN A THING FIXED. A WARNING COUNT THAT FALLS WITHOUT A TOOL CHANGE IS A SILENCING, AND IT WILL LOOK LIKE HOUSEKEEPING.**

*(Added 2026-08-16T08:27:11Z. Same family as D32 and D19; the live case is `queue_check`'s grep-tree gate.)*

**THE LIVE CASE, measured 2026-08-16:** `tools/queue_check.py` warns `GREP TREE UNNAMED (3 of 58)`.
**Those three rows — `#61`, `#65`, `#68` — have no bot tree BY DESIGN**; their subjects are
`tools/audit_trigger.py`, `results.tsv` and `tools/target_value.py`. ⇒ **The warning CANNOT clear
and MUST NOT until the tool learns the exemption.**

**⛔ AND THE GATE IS ALREADY KNOWN TO BE SILENCEABLE BY PROSE** (research, `4b6614aa`, driven on a
three-cell matrix): the incumbent token is matched **anywhere** in the GREP segment with no
requirement that its sentence assert a grep, **so a row reading *"`_v223sealrepair` is NOT the
relevant tree"* scores as CHECKED and drops out of the warning.** ⚠ **Its own author produced that
wording by accident while writing an HONEST disclaimer, and the count went to 0 of 3.**

**⇒ THE ROW: if a warning count FALLS and no TOOL CHANGE explains it, treat the fall as the
finding.** The silencing edit is **indistinguishable from diligence** — it reads as a row being more
carefully documented — **so a good-faith author will do it, repeatedly, and nobody will notice.**
**A guard whose bypass looks like good practice is bypassed by the people trying hardest to comply.**

**⚠ AND THE STATED LIMIT OF THE ONLY CUT RUN SO FAR, so nobody quotes it as clearance:** this lane
checked how many of the 58 rows are silenced TODAY and found **none** — but the detector was a
**negation-proximity heuristic over prose**, i.e. **the same instrument class the defect exploits**,
and only the 11 rows it surfaced were read. ⇒ **The honest form is *"no silencer found by a crude
detector"*, never *"none exists"*.** **The durable fix is structural — a `GREP-TREE:` field whose
wrong answer is MALFORMED rather than PLAUSIBLE — not a better prose filter.**

---

## ⭐⭐ D34 — **A NUMBER GETS AUDITED WHEN SOMEBODY DISLIKES IT. DIRECTION, NOT MAGNITUDE, DECIDES WHETHER IT IS EVER CHECKED — AND BOTH DIRECTIONS ARE UNGUARDED.**

*(Added 2026-08-16T08:40:39Z. First half is the RESEARCH lane's finding and their sentence; the corollary and the
worked harm are this lane's, demonstrated the same hour. Routed here at their request.)*

**RESEARCH'S HALF, measured 2026-08-16:** the repo quoted **53.50%** as the board leader's shipping
value for a full day. It assumes **τ = 0**, which **Q = 787 on 58 df falsifies**. The correct
empirical-Bayes value is **~54.9%**. ⇒ **A REPO-WIDE NUMBER DRIFTED FOR A DAY IN THE PESSIMISTIC
DIRECTION AND NOBODY CHECKED.** Their formulation: **pessimistic numbers do not get audited.**

**⭐ THE COROLLARY, AND IT IS WHY THIS IS A ROW RATHER THAN AN ANECDOTE: OPTIMISTIC CORRECTIONS ARE
AUDITED BY NOBODY EITHER.** An audit arrives when a number is DISPUTED, and **a number is not
disputed by the person it flatters.** ⇒ **A pessimistic number sits unchecked because nobody wants
to argue it up; a favourable correction sits unchecked because nobody wants to argue it down. The
unguarded set is BOTH TAILS, and the middle — the number someone resents — is the only part that
gets read carefully.**

**WORKED HARM, same hour, and it is why the corollary earns its place:** this lane audited the
**favourable** correction on purpose, precisely because it was favourable. **The arithmetic was
right** — independently re-derived at EB weight `τ²/(τ²+SE²)` = 0.9305, shrinkage **+0.30pp**
against research's +0.29. **The USE was wrong.** The correction gives a **replication-expected**
value, while Magnus's bar is a **MEASUREMENT** (*"It must MEASURE at least 60 +-2pp"*). ⇒ quoting
*"the gap is +5.2pp"* beside the bar **puts an EB posterior where a screen read belongs**, and
pairing a shrunken point with a naive ±1.31pp would understate the precision term of a bar that
HAS one. **Nothing in the arithmetic would have caught that, and nobody checks a number that moves
in their favour.**

**⇒ THE ROW, and it is a habit rather than a tool:** **when a number MOVES, ask which direction it
moved before deciding whether to check it — and then check it BECAUSE of the direction, not despite
it.** A correction that helps us is the one with the fewest natural auditors. ⚠ **Note this is the
same asymmetry `CLAUDE.md`'s DEFF direction clause already encodes for intervals** (*"a
fail-to-exclude claim must first be restated as an exclusion"*): **the flattering direction is the
one the machinery does not police.** **D34 generalises it from intervals to every number the repo
quotes.**

---

### ⭐⭐ D26 REFINEMENT 3 — **THE FIFTH SITE IS A CLAIM ABOUT OUR OWN ERRORS. EVERY ERROR SET IS A *CAUGHT* SET, AND CATCHING IS NOT INDEPENDENT OF THE PROPERTY BEING CLAIMED.**

*(Added 2026-08-16T09:06:55Z, side lane s45, from a live dispute resolved the same hour. Filed as a
REFINEMENT and NOT as a new D-number for the reason refinement 2 gives: **splitting one mechanism
across rows is how a checklist stops being usable (D14).** ⭐ **The COUNT is the finding — five sites
now, and the fifth is the one that inspects the inspectors.**)*

**THE INSTANCE.** The research lane claimed, of a three-hour window: *"every error caught today ran
in the flattering direction… the bias has a sign."* **Withdrawn in full within the hour, on three
grounds; the decisive one is D26's.**

**⛔ THE SET WAS SELECTED ON BEING CAUGHT, AND THE SELECTOR IS THE MECHANISM UNDER TEST.** D34 —
written the same morning, and cited BY THE CLAIM IN ITS OWN SUPPORT — says a favourable number has
**no natural auditor**. ⇒ **flattering errors are HARDER to catch, so a CAUGHT set must
UNDER-represent them.** **The rule was cited as evidence for a claim it predicts the opposite of.**
**The denominator that would settle it — the errors nobody caught — is by construction unobservable.**

**AND THE SUB-SELECTOR NOBODY OWNED:** the sample was *"errors that reached a PUBLISHED surface"*.
**Two errors that ran toward the ALARMING were absent only because the side lane killed them
PRE-PUBLICATION** (a subagent's *"CAL418's lock statement was never signed"* — it was; and
*"`PROGRAMME.md` declares a retired estimator to a machine"* — it does not). ⇒ **the publication
filter is itself correlated with direction, and it was invisible to the lane assembling the set
because that lane did not perform the filtering.**

**⛔ AND THE PRIOR MEASUREMENT EXISTED, ONE SESSION OLD, SAYING THE OPPOSITE.**
`docs/side-lane-retro.md` **v1.13 BANS direction models**, because the s44 instance measured
**"5 of 8 ran toward the alarming, 3 toward the comfortable."** ⇒ **A property of our error
distribution was asserted without checking whether it had been measured. It had, it was one session
old, it disagreed, and it was one grep away.**

**⇒ THE WATCH FORM, and it is a question to ask BEFORE the claim, not after:**
> **STATE THE RULE BY WHICH THE SET WAS ASSEMBLED, BEFORE CLAIMING A PROPERTY OF IT.** *(Research's
> formulation, kept as theirs.)* **Then ask D26's question of that rule: is the selector correlated
> with the property?** For any set of our own mistakes the answer is **always yes**, because the
> selector is *"we noticed"*.

⭐ **THE REPLACEMENT THAT NEEDS NO DIRECTION MODEL, banked in its place:** *"every correction today
came from a PEER or from a RECOMPUTATION, and none from an author re-reading their own work."*
**A claim about MECHANISM rather than SIGN — it argues for the three-lane protocol whichever way the
direction runs, and unlike the withdrawn form it is TESTABLE NEXT SESSION.**
⚠ **The withdrawn claim survives only as a DESCRIPTION OF FOUR ITEMS. It is not banked and is
deliberately absent from this checklist as a finding.**

---

## ⭐⭐ D35 — **BOTH-WAYS IS NECESSARY AND NOT SUFFICIENT. A DRIVE THAT A PLAUSIBLE WRONG IMPLEMENTATION ALSO PASSES HAS NOT SEPARATED THE MECHANISM FROM ITS LOOKALIKE.**

*(Added 2026-08-16T09:32:12Z. Found by the RESEARCH lane against THIS lane's own specified cells, mid-build.
⚠ **Recorded as a ROW rather than folded in as a rider — and the distinction is deliberate, because
I declined a row two entries ago on volume grounds: an INSTANCE folds in; a change to a STANDING
RULE gets a row.** This modifies the most-cited rule in the repo.*)

**THE STANDING RULE, `CLAUDE.md`:** *"Before trusting one, run it against a case where it MUST come
out the other way. A check that has never produced the other verdict has not been seen to check."*
**Correct, and this lane has applied it all session.**

**THE INSTANCE.** I specified two fixture cells for the fieldcal reader's falsifier guard:
**(a) today's tape (n=260) must REFUSE; (b) a synthetic pooled read at n≥800 must COMPARE.**
Both ways, both reachable, and the guard ships driven. ⛔ **Research's objection: BOTH CELLS ARE
SATISFIED BY `if n < 800: warn`** — a plain sample-size threshold, which is **NOT the registered
rule.** The registered rule is CATEGORICAL: **a per-CELL read never fires the falsifier at ANY n**,
because a cell is a different statistic from the pooled one.

⇒ **Their third cell is what separates them: a synthetic PER-CELL line at n ≥ 600/arm MUST STILL
CARRY THE REFUSAL.** Under the correct rule it refuses; under `if n < 800` it clears.
**Cells (a) and (b) agree on both implementations. Only (c) disagrees.**

**⇒ THE ROW:** **name the PLAUSIBLE WRONG IMPLEMENTATION before choosing the cells, and add the cell
on which it DISAGREES with the right one.** ⛔ **"It passed both ways" is compatible with having
tested a lookalike.** The dangerous lookalike is never absurd — **it is the one a competent
implementer would write from the same brief**, which here is a threshold on n, and it fails silently
**at exactly the moment the leg gets big and the guard starts to matter.**

**⚠ AND THE SELF-AUDIT, because this is the FOURTH instance of one shape from this lane in a single
session:** RMST (answered a narrower question than the finding needed) · the carry idiom (asked
*"is it stale?"* not *"is it classified right?"*) · the verb-list clearance (tested one member,
reported the class clear) · **and now this (specified cells that verify the OUTPUT and not the
MECHANISM).** ⇒ **All four published a correct answer to a question smaller than the one on the
table.** **The 09:22Z correction — *name the members tested and not tested in the same sentence as
the clearance* — would NOT have caught this one**, because the gap was not in the members, it was
in **what the members could discriminate.**
**⇒ The correction is extended: name the members tested, AND name the wrong implementation the
tested members would fail to detect.**

### ⭐⭐ D32 RIDER — **THE FAMILY IS WIDER THAN SITING: A GUARD THAT IS COMPLETE, CORRECT, AND UNABLE TO FIRE. THREE MEMBERS, THREE MECHANISMS, ONE DAY.**

*(Added 2026-08-16T10:09:15Z. Family identified by the RESEARCH lane; the third member and the general form are this
lane's; the sharpening below is theirs verbatim. ⚠ **A RIDER AND NOT A NEW D-NUMBER, deliberately —
this is the same object D32 already names, seen from two more angles, and the CURATION is the
finding.** Sixth checklist action today; I have declined two rows on volume grounds and this one adds
no number.)*

**D32 as written covers SITING — the surface has no reader. The family has at least three
mechanisms, and only the first was named:**

| # | mechanism | instance (2026-08-16) |
|---|---|---|
| 1 | **SITING** — the surface has no reader | `AGENTS.md`'s regeneration rule in an HTML comment inside the generated file; Magnus's 70% in a 62k-line channel; the fieldcal falsifier warning in a note rather than the tape |
| 2 | **ORDERING** — the guard is reached only when it cannot matter | `queue_check`'s `if claimed (prose) … elif gp (structured)`: six rows carried a verified token that was **never consulted**, so adding tokens was INERT |
| 3 | **EXPIRY** — the guard reads correct and the ground moved | `E3`'s NOWINNER-RATE exclusion: 8.33% and 10.83% today, **0.59% and 0.48% once the same shards resume** — same contamination, same rule, silently admitted |

**⭐ THE GENERAL FORM (this lane):** **a CONTAMINATION RATE is a property of the DENOMINATOR, so any
rule keyed to it expires as soon as the denominator grows.** The contamination did not change; **the
rule's ability to see it did.**

**⭐⭐ AND THE SHARPENING THAT EARNS THE FAMILY ITS OWN NAME (research, verbatim):**
> ***a wrong threshold is visible on inspection; an EXPIRED one reads correct forever.***

⇒ **They fail differently and only the second is invisible to review.** **Every member of this family
shares that property — the artefact passes inspection, which is exactly why nobody looks twice.**
**D32's original tell holds across all three: the tell is that it is COMPLETE AND CORRECT.**

**⇒ THE CHECK, extended from D32's:** *"what has to READ this for it to fire, and does that thing
exist?"* **plus** *"is it REACHED before it can matter?"* **plus** *"does anything it is keyed to
GROW?"*

**⚠ BOUNDED, so the row is not read as an alarm:** research swept their published cuts and **E3 is
the ONLY rate-keyed exclusion** — `E5`/`E4`/the fieldcal 40-per-arm floor are COUNTS, the kladde
exclusions are IDENTITY, and **counts and identities do not expire when the denominator grows.**
⭐ **That distinction is what made the sweep quick, and it is the durable diagnostic: RATES expire,
COUNTS and IDENTITIES do not.**
**Also bounded: both corrupt shards POST-DATE the 08:31:10Z reachability read and are not among its
59 arms. No published number moves.** **What expires is the RULE on any re-run — the dangerous case,
because a successor re-running the same script tomorrow gets a silently different population.**

**⭐⭐ WHY THIS FAMILY DOMINATES — added 2026-08-16T11:37:51Z, and it is the reason D32 is worth its length.**
*(Research lane's formulation, kept as theirs; the corollary is this lane's. Appended to the existing
rider rather than filed as a new row — it changes how the family is PRIORITISED, which is
decision-relevant, and it adds no number.)*

> ***A WRONG FACT IS THE CHEAP ERROR. A MIS-ROUTED CORRECT FACT SURVIVES INDEFINITELY, BECAUSE
> NOTHING CONTRADICTS IT.***

**Measured on one day, two lanes:** research's seven errors were **six correct-but-mis-sited or
correct-but-mis-compared, and ONE false.** ⛔ **The false one died to a single measurement in
minutes** (their map-skew hypothesis, refuted on both shards). **The other six needed a peer to
notice where they were sitting.**

**⭐ AND THE COROLLARY, WHICH IS WHY D32'S CHECK IS THE ONLY DETECTOR THERE IS: a mis-sited CORRECT
claim has NO EMPIRICAL DETECTOR.** **Data cannot refute it, because it is not wrong.** Re-running the
analysis confirms it. Checking the arithmetic confirms it. **Every instrument this repo owns returns
PASS.** ⇒ **The only thing that catches it is an audit of SITING — *what has to read this for it to
fire, and does that thing exist?*** **That is not one check among several; for this class it is the
check, and there is no second opinion available.**

⚠ **PRIORITISATION CONSEQUENCE, stated so the row changes behaviour rather than describing it:
when triaging a batch of findings, the CORRECT ones are the ones to audit for siting.** **The wrong
ones will be found by the work; the right ones will not be found at all.**

---

## ⭐⭐ D36 — **A RULE INVOKED AGAINST ANOTHER LANE'S CLAIM IS NOT THEREBY APPLIED TO YOUR OWN. THE INVOCATION FEELS LIKE THE APPLICATION.**

*(Added 2026-08-16T11:53:51Z. Mechanism and formulation by the RESEARCH lane, about themselves; **written by this
lane at the standard they set when they handed me D32 — a failure mode written up by its principal
offender is weaker evidence than the same text written by the lane that caught it.** Filed as a NEW
number, not a rider: it is not D32 (siting), not D26 (selection), not D35 (lookalike cells). **New
mechanism, mechanical fix.**)*

**THE INSTANCE, 2026-08-16 ~11:5xZ.** Research corrected the builder for *"gate-1 clearance implies
probable gate-2 victory"* — **naming the non-transitivity rule, citing 's discordant pair and
** — **and then committed the same composition in their own headline, in the same message,
about the same two numbers**: *"the 60-bar decodes to beat the live holder by ~3pp, and nothing we
hold is even as good as what is live."*

**⛔ THE MECHANISM: HAVING JUST DEMONSTRATED THAT YOU KNOW THE RULE IS THE STRONGEST POSSIBLE REASON
NOT TO RE-CHECK YOURSELF AGAINST IT.** The invocation supplies the FEELING of compliance. ⇒ **This is
the class that survives review BY ITS OWN AUTHOR, and it is not the same as forgetting** — the rule
was held, cited, and correctly applied one paragraph earlier.
⚠ **Sharper still: the anchor was THEIR OWN LANE'S DOCUMENT**
(`docs/research/SCREEN-PREDICTIVE-VALIDITY-2026-08-14.md:47`,
*"these two coincide only under transitivity"*). **Not a rule they forgot — a rule they wrote.**

**⛔⛔ AND D36 CLAIMED ITS AUTHOR IN THE COMMIT THAT WROTE IT — logged here rather than in the
channel, because a row this shape is worth more with its own instance attached.** The citation above
was **destroyed on first write**: I used an unquoted heredoc, zsh executed the backticked path as a
command, and the anchor was replaced by an empty string — **leaving a row about checkable rules with
no checkable anchor.** ⚠ **I made the IDENTICAL error at 09:17Z, corrected it, and wrote up the
correction.** ⇒ **I fixed the INSTANCE and not the PRACTICE, then invoked D36 against another lane
while committing D36's own shape.** **The mechanical fix I prescribed for them is the one I owed
myself: quoted heredoc always, timestamp interpolated separately — which I had already applied
correctly in the SAME shell call, to a different file.**

**⭐⭐ AND THE ROW CARRIES TWO INSTANCES AT DIFFERENT DISTANCES FROM CARE, WHICH IS WHY IT IS A ROW
AND NOT A NOTE-TO-SELF** *(re-ranking by the research lane, against this lane's own ordering — I
called mine the duller of the two and they argued the reverse, correctly):*
* **RESEARCH'S:** a rule **held and cited**, not applied one paragraph later. ⇒ *a rule can be held
  and not applied.* **One mechanical habit closes it.**
* **THIS LANE'S:** a rule **held, caught, WRITTEN UP, and BANKED that same morning** — then broken
  two hours later, **in the same shell call where the correct form was applied to a different file.**
  ⇒ *a rule can be held, **documented**, and still not applied.*
⛔ **The second is the one that justifies a checklist row at all: it shows that WRITING THE RULE DOWN
IS NOT THE FIX.** **If documentation closed this class, my instance could not exist.** ⇒ **the fix
must be mechanical and must fire at the moment of writing — the citation, or the heredoc — never at
the moment of remembering.**

**⭐⭐ THIRD INSTANCE, AND IT MAKES THE ROW A GRADIENT RATHER THAN TWO ANECDOTES.** Research banked at
~11:1xZ: *"a count is only as wide as its enumeration rule, and neither number is quotable without
it."* **They then gave a count of their own errors WITHOUT ENUMERATING — stating seven against
categories summing to eight.** Resolved from the commit log at their own hand: **the total was
wrong, the categories right, it is EIGHT.**

| # | how actively the rule was held | gap | closed by care? |
|---|---|---|---|
| 1 | held and CITED against a peer | one paragraph | no |
| 2 | held and CITED IN A COMMIT MESSAGE the same day | hours | no |
| 3 | held, CAUGHT, WRITTEN UP and BANKED that morning | hours, with the correct form applied 5 lines away | no |

⛔ **THE GRADIENT IS THE FINDING: the class does not attenuate as the rule is held more actively.**
**Each instance is further from "forgot" and none is closed by attention.**
⚠ **AND INSTANCE 2 CARRIES THE WARNING THE OTHER TWO DO NOT: it landed on A COUNT THAT WOULD HAVE
BEEN QUOTED IN A RETRO AS EVIDENCE OF RIGOUR.** *"A wrong error-count in a document about
error-handling"* — **and nothing about the number looked wrong; it looked like diligence.**
⇒ **Audit your own counts first: enumeration is mechanical, so it is exactly where the mechanical
fix is cheapest.**

**⇒ THE FIX IS MECHANICAL, NOT ATTENTIONAL, AND THAT IS THE WHOLE VALUE OF THE ROW** (their words,
and they are right that more care does not reach this): **when you cite a rule against someone
else's claim, RE-READ YOUR OWN TEXT IN THE SAME ACTION, against that rule.** **The trigger is the
citation itself.** ⛔ **"I was careful" cannot catch this, because the author WAS careful — that is
the precondition.**

⭐ **AND IT GENERALISES PAST LANES: the same shape is a reviewer applying a standard to a diff and
not to their own review, or a prereg registering a guard it then violates in its own analysis
section.** **Anywhere a rule is INVOKED, the invoker is the least-audited reader of it.**

---

### ⭐⭐ D35 RIDER — **NAME THE ALTERNATIVE READING BEFORE WRITING A BRANCH AS DECISIVE. FOR ANY SOFT OR PERMISSIVE KNOB, THE ALTERNATIVE IS ALWAYS "THE KNOB NEVER BOUND."**

*(Added 2026-08-16. Research lane's formulation, after this lane broke their branch. Filed as a
RIDER to D35 and not a new number — **D35 says name the plausible wrong IMPLEMENTATION before
choosing cells; this says name the plausible alternative READING before choosing a branch. Same
shape, one object over.**)*

**THE INSTANCE.** `#78`'s conversion route registered: *"#23 flat or negative ⇒ #78's prize does not
convert and the row should not be built."* ⛔ **`LOKI_FWD_GUN_CAP` is a SOFT, MONOTONE cap
(`raid.py:654` — `>= CAP` ⇒ decline to build): raising it PERMITS more turrets and never FORCES
them.** ⇒ **a flat read is ambiguous between *the dose does not pay* and *the cap never bound*, and
the branch was written as decisive over both.**

**⇒ THE FIX IS FREE AND OFF THE ARM'S OWN TAPE: A MANIPULATION CHECK.** *Did the arm actually
produce more of the thing the knob permits, versus control?* **Flat WITH a confirmed dose is
decisive. Flat WITHOUT one is an inert flag, not a null.**

**⭐ THE GENERAL FORM, research's words kept as theirs:** ***"The cost of a strong claim is the
obligation to enumerate its alternatives, and I took the first without the second."***
⇒ **Writing a branch as DECISIVE is not free — it converts *"what else could produce this reading?"*
from good practice into a PREREQUISITE.** ⚠ **A softer wording would not have needed the check at
all, which is the honest trade: strength buys bindingness and costs an enumeration.**

**⛔ AND THE STANDING SPECIAL CASE, because it recurs and the answer is always the same: FOR A SOFT OR
PERMISSIVE KNOB — a cap, a ceiling, an `if allowed` — THE ALTERNATIVE EXPLANATION FOR ANY NULL IS
"IT NEVER BOUND."** **Not a judgement call, and checkable mechanically from the arm's own rows.**
⭐ **Already registered once, one row over, by the lane that then did not carry it across:** `SENTBAN`'s
*"K=2 is a DOSE, not the mechanism — a K=2 null does not refute attrition memory."* **Same morning,
next soft knob, rule not re-applied — which is D36's shape and is why these two rows sit together.**

## ⭐⭐ D37 — **A REVERT THAT RESTORES THE PINNED STATE ALSO DESTROYS THE EVIDENCE THAT WOULD CERTIFY THE EXPOSED WINDOW. QUARANTINE, DON'T REVERT — AND THE PRESCRIPTION THAT GOT THIS WRONG WAS THIS LANE'S.**

**Written 2026-08-17T07:25:06Z, against this lane's own prescription in the 07:16Z control-tree incident.**

The incumbent/control tree `bots/_v468kladturbo` was edited **uncommitted** while three certified
arms wrote against it. `corefill`'s guard refused at 07:16:27Z; `control_pin --check` showed
`pinned a9228ccb → now 955ec186`. **This lane flagged it correctly and fast (~1 min), and quoted the
tool's own prescription — *"revert, then `--pin` again; DO NOT JUST RE-PIN TO SILENCE THIS."*
Then it added a fix of its own: `git checkout -- bots/_v468kladturbo/`.**

⛔ **THAT FIX WOULD HAVE BEEN A DISASTER OF A PARTICULAR AND NON-OBVIOUS KIND. It restores the pinned
bytes exactly — and in doing so it deletes the only copy of the edits, which are the ONLY thing that
can answer the question the incident actually poses: *were the rows written during the window
contaminated, and by how much?*** The builder instead **stashed** (`s48-wrapfix-control-tree-edits-QUARANTINED`),
which restored the identical bytes AND kept the diff — and the diff is what certified the window.

⭐ **THE CERTIFICATION, verified INDEPENDENTLY by this lane rather than taken on relay** (peer claims
get checked against primaries): a **stripped-AST** comparison — docstrings removed, because comments
never reach the AST but docstrings DO, which is why a naive `ast.dump` flags a comment-only edit —
returns `bytes_identical=False, stripped_AST_identical=True` for **both** `eco.py` and `raid.py`.
**Instrument driven BOTH ways before use: a real change reads DIFFER, a comment-only change reads SAME.**
⇒ **The edits were comment/docstring-only. NO ROW WAS CONTAMINATED. The window is CLEAN — certified, not assumed.**

⇒ **THE GENERAL RULE. When a pinned artefact moves under a live fixture, the state and the evidence are
TWO different things and the obvious repair conflates them:**
* **RESTORE the bytes** (so the fixture stops drifting) — **and PRESERVE the diff** (so the exposed
  window can be certified rather than excised). `git stash` does both; `git checkout --` does only the first.
* **Excision is the fallback you pay when the evidence is gone.** Here it cost nothing because the
  evidence survived — **by the builder's choice, not this lane's.**

⚠ **AND THE HONEST SCORE, because it is this lane's recurring failure mode and it recurred:** the s34
retro's headline — *"right that something was wrong, wrong about what would fix it, every time"* —
**landed again, and this time the mechanism is nameable rather than just tallied: a one-line
prescription optimises for restoring STATE, while the value of the incident is in the EVIDENCE.**
**This is the argument for the rescoped charter's *"name the defect, hand the fix to the owning lane"*
— the defect call was right, the fix call was wrong, and the split is exactly where the charter puts it.**

## ⛔⛔ D38 — **BEHAVIOURAL IDENTITY: THE SHIPPED BOT'S ACTUAL PLAY IS AUDITED AGAINST THE DECLARED DOCTRINE, PER ADOPTION AND PER WRAP. PROCEDURALLY-PERFECT VERDICTS CAN AGGREGATE INTO DOCTRINE DRIFT, AND ONLY A BEHAVIOURAL DECODE SEES IT.**

**Commissioned by Magnus 2026-08-23/24 night (his question, verbatim: "isn't the side lane
supposed to make sure we follow the directives? Is it sleeping?") — adopted into this checklist
by the lane it indicts, with the incident stated in full.**

**THE INCIDENT.** Across s57/s58's campaign this lane certified ~40 verdicts, every one
procedurally clean (blind bars, unmoved rulers, honest refusals) — and the AGGREGATE drifted:
seven hardening adoptions, zero identity planks shipped. Every identity-carrying plank
(dispatch, rotation, push, hammer) was refused by screens vs OUR OWN SIBLING FIXTURES, while
hardening passed — local screens against siblings can only converge to a polished chassis.
The live leg then delivered the field's ruling: Jython v266 swept us 5-0 playing THE DECLARED
SKALMAN DOCTRINE ITSELF. **The drift lived in the verdict layer's objective function, and the
encoding-level audit (verbatim faithful, bars unmoved) could not see it by construction.**

**⛔ AND THE CHECKLIST ALREADY HELD THE CONCEPT: D23 (self-play cannot measure an exploit
plank — a property of the whole line) IS this finding, scoped to exploit planks. The auditor
had the row and did not fire it at the verdict AGGREGATE — the D36 class (a rule invoked
against single instances is not thereby applied to the stack of them).**

### THE WATCH FORM
1. **Per ADOPTION and per WRAP: decode the shipped/adopted tree's ACTUAL PLAY** — rush check
   (forward bodies pre-latch?), box check (does the box fire?), phase check (does the flip/
   burst happen?), identity-verb census (which declared doctrine verbs executed ≥once per
   game at what rate) — and DIFF against the declared identity in PROGRAMME.md. The play-it-
   well rule's execution ledger is the instrument; the diff is this row's product.
2. **Per REFUSAL of an identity-carrying plank: ask WHICH fixture class refused it.** A
   sibling-fixture refusal of an identity plank is D23's class and is REPORTED AS
   EXECUTION-DEBUGGER INFORMATION, never certified as an identity verdict (the IDENTITY
   INVERSION, PROGRAMME 2026-08-23/24: screens debug execution; the field judges identity).
3. **The adoption-count diagnostic: at every wrap, count adoptions by class
   (identity-verb vs hardening).** A run of N hardening adoptions with zero identity
   adoptions is a FIRING CONDITION of this row, not a neutral fact.

**Retroactive first firing: run against the s57/s58 adoption set (below, this date).**

## ⛔⛔ D39 — **A VERSION-KEYED GUARD OUTLIVES ITS SUBJECT SILENTLY, THEN FIRES ON EVERYTHING. EVERY ACTIVATION SWEEPS RUNNING MONITORS FOR KEYS NAMING THE DISPLACED VERSION.**

**Added 2026-08-24 (s58 wrap, side lane; routed from retro v1.25). Earned by TWO instances
inside one hour, one of them the auditor's own:** after the v213→v215 ship, the builder's
v213-keyed slot guard (pid-level `ver != "v213"` pipeline) was still running beside the new
v215 guard — on the next elo-tape row it would have printed HOLDER CHANGED perpetually,
devaluing the exact alarm words the live guard uses (the fires-on-everything-asserts-nothing
class, D4-of-the-builder's-wrap inverted). **And this lane's OWN independent tape monitor
carried the identical stale key** — found in the same sweep, stopped and re-armed before
either instrument fired once.

**THE WATCH FORM:** at every activation/restore (ship, rollback, window open/close), enumerate
RUNNING monitors (`ps` for the guard pipelines, the session's own Monitor tasks) and check
each fire-condition for a literal version string naming the DISPLACED version. A guard keyed
to a version is an instrument whose fixture just changed — D19's expiry clause applied to the
guard itself. The sweep includes the auditor's own instruments: the second instance was mine,
and only the habit of sweeping MY keys alongside theirs caught it pre-fire.

*(Game context: in-game Florent Code League instruments.)*
