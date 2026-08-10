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
