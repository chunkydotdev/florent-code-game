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
