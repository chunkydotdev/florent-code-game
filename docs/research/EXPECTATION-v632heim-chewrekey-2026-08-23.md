# REGISTERED EXPECTATION — v632heim CHEW-CLOCK RE-KEY (SK_CHEW_REKEY)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition. All terms are in-engine mechanics; the
attack verb is the engine's documented builder action against an opposing
bot's in-game structures.**

**PROVENANCE:** typed by BUILDER s57, committed BEFORE the build agent runs.
Inputs: the diag431_* diagnostic (census instrument byte-inert, driven both
ways via two mutation controls; 2,980 pooled held-post rounds with an
adjacent enemy building, decliner table with anchors), the adopted-NS
baseline t_ns_* [alive 54 / deaths 50 / wins 34 / kills 22 / eco 38.27 /
harv 216].

**DEFECT TARGETED (measured, anchored):** `melee_tile`/`melee_since`
(`_clear_tile` sk_roles.py:6426-6430) is a ONE-SLOT memo keyed on TILE
only: (a) it never re-arms when a NEW enemy building occupies the same tile
(the 149-round jotunheim span: old barrier pecked dead r182, new barrier
bid=54 planted, clock stale from r218, 8-HP target held 124 rounds with
bank up to 53 and can_fire TRUE); (b) one slot means tiles evict each
other. `_demolish_budget_ok` (:9079) already re-keys on occupant id — the
verb's clock does not. Chew-clock declines measured: **142 F1 / 464 F2 /
131 F3 = 737 pooled (24.7%)**, stable 22-33% on all fixtures.

**KILLED FROM THE DIAGNOSTIC'S RECOMMENDATIONS (consumption receipt):**
rec (ii) — demolish rung targeting adjacent enemy BUILDER BOTS — is
refuted by the banked engine probe (bots/_probe_bvb_a/b: 990/990
can_fire=False on enemy builders; fire raises GameError). No plank may be
built on that road. Rec (iii) (SK_SEAT_CLEAR re-price) is routed as its
own queue row, not folded in here.

**DESIGN CONSTRAINTS (registered):** the clock becomes per-(tile, occupant
building id) with a bounded dict (the ban-dict hygiene precedents); the
GIVEUP semantics for cage walkers are UNCHANGED — a walker still abandons
a hard tile at 20 rounds; the only behavioural change is that a NEW
occupant re-arms the clock and that independent tiles carry independent
clocks. NO keeper exemption from the giveup in this flag (that is a
second, separately-registerable arm if dose falls short). Dict growth
bounded and disclosed.

## Registered lines (arm `cr` = SK_CHEW_REKEY=True vs t_ns_* baseline)

**C1 identity:** OFF ≡ t_ns_* 30/30 ×3. *Falsifier: divergence ⇒ leak; halt.*

**C2 mechanism (deterministic trace, the jotunheim specimen):** on
jotunheim_seatA F1 ON, the re-planted barrier's clock re-arms (traced) and
the specimen tile's post-r218 idle span shortens materially; the pecks land.
*Falsifier: clock still stale on a new occupant ⇒ weld; halt.*

**C3 DOSE (the census instrument, control values measured):** chew-clock
decline rounds fall vs **142 / 464 / 131** on ≥2 fixtures with the pooled
sum ≤ −50% (the defect class should mostly vanish — a re-keyed clock only
declines a genuinely-hard SAME occupant past 20 rounds); held-post
adjacent-enemy rounds vs **431 / 2,123 / 426** reported (they will not
vanish — bank poverty and the healing race are separate classes); pecks
landed (`_clear_tile` YES-fired count vs F1 3,092 pooled baseline) reported.

**C4 GUARDS:** alive-sum within −2 of **54**; death-sum within +4 of **50**;
eco-sum within −12% of **38.27**; harv within −10% of **216**;
titanium-spend sanity (the diagnostic's turn-vs-titanium substitution
note: F1 median bank is 1 — the extra pecks must not starve spawns; global
resources trajectory reported); wins/kills informational (34/22;
per-fixture 10/9/15).

**C5 tracebacks:** 0 expected.

## Adoption rule (pre-registered)

Adopts if C1, C2 pass, C3 meets the pooled bar, C4 holds. If C3's dose
lands but a C4 econ guard trips on F1 only (the bank-1 fixture), a
bank-floor rider on the re-keyed clock is a legitimate pre-registered
follow-up, not a silent amendment.

## VERDICT — REFUSED per the pre-registered adoption rule, BUILDER s57

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

C1 pass. **C2 FAIL — specimen misdiagnosed:** the trace shows the OFF memo
ALSO read since=196 on the (3,4) span; the 124 declines were the GIVE-UP
BINDING ON THE SAME OCCUPANT (r218−196=22>20), not a stale re-key — the
diag431 causal claim for that span is CORRECTED here (the true occupant
re-key class is ≤66 events tape-wide). **C3 FAIL, WRONG DIRECTION:**
chew-declines +259%, pecks −17.7%. **C4 TRIP:** F1 alive@300 −3 (bar −2),
wins 10→7, ≤r300 kills 6→3.

**THE FINDING THAT OUTLIVES THE REFUSAL:** `SK_CAGE_MELEE_GIVEUP=20` has
NEVER been in force — the one-slot memo is evicted by any chew on another
tile, so the shipped tree chews nearly indefinitely by thrash. Enforcing
the clock honestly is a MEASURED COST; the accidental persistence is
load-bearing. Directional evidence: in the measured range, MORE chewing =
more pecks = more wins. The code stays built, OFF, as the honest-clock
reference implementation.
