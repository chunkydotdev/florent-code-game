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
| D1 | a plank built outside the Loki lineage dirs, or any edit to the frozen incumbent beyond rollback | `LINE: loki`, `INCUMBENT_FROZEN: yes` |
| D2 | a battery or verdict measured against Eir (or any non-Loki baseline) instead of the previous Loki iteration | `COMPARE_AGAINST: previous_line_iteration` |
| D3 | a verdict argued from win rate | `WIN_RATE_IS_VERDICT: no`; currencies are `core_kill_share` + `time_to_core_kill` |
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

| D18 | **A BEFORE/AFTER CUT ON *OUR* VERSION IS UNINTERPRETABLE UNLESS THE OPPONENT'S VERSION IS HELD CONSTANT OR SHOWN TO HAVE MOVED.** Fired TWICE on 2026-08-10 within four hours, on two different opponents, by two different lanes: the Ouroboros "frozen hard counter" (retracted — matchup improving once their version era was controlled) and this lane's Bisons "climb-band regression" (−31.4pp, p=0.0027 — killed: their v4 first appears **2026-08-09T19:22**, our v102's first ladder game **18:42**, **forty minutes apart and perfectly collinear** — all 7 v102+ matches vs their v4, none of the 13 earlier ones). **We control our own version scrupulously — every leg pins `ourver`, asserts the holder, verifies `teamAVersion` on the platform — and nothing anywhere pins, or even reads, the OPPONENT's version at analysis time.** Sub-finding, and it is why the gap survived: **`ladder_games.tsv.oppver` is NULL for all 100 Bisons games, and a null column reads as "no version change" to any cut that trusts it** — a constant column validating anything, in the one field that would have caught this. **Check form: before reporting any our-version before/after delta, join the opponent's version timeline (`league_matches.tsv` carries it; `ladder_games.tsv` does not) and report their boundary alongside ours. If the two are collinear, the delta is unattributable and must be written as such.** | research's formulation after killing this lane's finding, 2026-08-10; two independent firings the same day |

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
