# REGISTERED EXPECTATION — survival family: SK_WALK_GUARDS + SK_LEASH_DUTY

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**PROVENANCE:** BUILDER s58, committed while the build agent runs. Baseline
= t_so [alive 53 / deaths 54 / wins 31 / kills 14 / eco 35.47 / harv 208].
Two separate single-flag arms in one chain (never composed). The campaign
context: four rotation arms froze at wins 31-34; alive-sum 53 caps the
touchable population; these are the queue's survival planks.

## Registered lines (each arm)

**S1 identity:** flags-off ≡ t_so 30/30 ×3.
**S2 liveness:** ≥5/30 divergent per fixture (both planks fire on
conditional states; the SO precedent read 6/6/11).

**ARM A dose (walk guards):** zero-action runs ≥50 rounds by our builders,
three-fixture total rounds, ≤ **−25%** vs baseline (measured same-readout;
long-freeze class only — the ≥20r crawl class is #131's, excluded by the
run-length; the three guarded sites are the audit's named freeze shapes).
Conditional seen-firing: escape-fires > 0 required only in cells where a
guarded deadlock state occurs; the state count is a registered column.

**ARM B dose (leash duty):** in cells with ≥1 leashed-no-target round
(registered column), duty_holds > 0 and the keeper reaches core-adjacency;
the banked degenerate class (0-eco 400+-round cells) absent. Eco builds in
formerly-degenerate shapes reported.

**Guards (both):** alive-sum within −2 of 53 (any RISE reported against
the campaign arithmetic — each +1 alive-cell raises the win ceiling);
deaths +4 of 54; eco −12%; harv −10%; wins/kills informational.

## Pre-registered decision
Per arm, SO-precedent bug-fix grade: dose + guards → ADOPT. Dose
conditional-vacuous (no deadlock/no-target states occur) → adopt-eligible
only as identity-preserving hardening IF guards hold and the state columns
are honestly zero — disclosed, not silent. Guard breach → one redesign
then park, standing rules.

**PRE-TAPE DISPOSITIONS (blind held — no tape of either arm exists):**
**ARM B WITHDRAWN** on the build agent's premise measurement: the existing
fall-through (`tgt = self.core` + the core-ring goal branch) already
delivers the keeper to core-adjacency in the leashed-no-target state (610
rounds traced, zero stuck away; 4 of 7 dosed smoke cells byte-identical to
OFF). The plank is near-identity by design; taping it spends a window on
nothing. THE REAL RESIDUAL, measured and routed to the queue as its own
candidate: LEASHED-ECONOMY STARVATION — that keeper laid 1 conveyor in 849
leashed rounds; the treatment is leashed WORK (core-adjacent belt/apron
tiles as in-range targets), not a better walk. The smoke's one win→r1000
regression on B's divergent cells is banked with the withdrawal.
**ARM A AMENDED to the terminating form** (the same smoke-mechanism
amendment class as RO-P/mesh/p10): `_walk_escape` gains a short per-site
tile ban after an executed escape (precedents: `_escape`'s ban,
`SK_CURSOR_GIVEUP`, `_t4_chase_ok`), so the walk re-targets elsewhere
instead of oscillating. Bars unchanged (−25% on ≥50r freeze rounds;
conditional seen-firing with state columns) — with the honest note that
the ≥50r mass at these sites may already be small post-SO; a
vacuous-with-disclosure outcome adopts as hardening per the registered
rule.

**ARM A DOSE BAR RE-FORMED PRE-TAPE (blind held; the 4.2 smoke's paradox
is the provenance):** the global ≥50r freeze-round pool is DOMINATED by the
#131 crawl class these sites never touch (jotunheim's 1,475-round parked
body alone), and the escape-only form SCORED BETTER on it by shuttling —
the instrument rewards the dishonest fix. The bar re-forms to the
mechanism's terms: (i) conditional seen-firing (escapes execute where
deadlock states occur — unchanged); (ii) NO POST-ESCAPE OSCILLATION — after
each executed escape, the body's next 20 rounds visit ≥3 distinct tiles or
the walk target changes (the smoke's 64%→16% top-2-share is the shape);
(iii) freeze rounds ON THE GUARDED STATE-TILES ONLY → reduced-or-zero
where states occur. Global freeze pool reported, never gated. Adoption =
hardening grade (correctness plank); any alive-sum rise reported against
the campaign arithmetic as a bonus, never required.

## VERDICT — ARM A ADOPTED (hardening grade), typed by BUILDER s57 2026-08-23

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

Against the re-formed mechanism-terms bar (readout e46wg_*, diagnostic diagwg_*):
- **(i) seen-firing: PASS.** Escapes execute where states occur (bifrost def 4/
  deny 1 traced round-by-round; F3 early-termination share 0.082→0.149, p90
  117→93). State column is an upper-bound proxy, disclosed.
- **(ii) no-oscillation: MARGINAL PASS with a named defect.** At the one traced
  SITE-3 firing the body visits ≥3 tiles and leaves within 20r (bar met), but
  only after re-fires: **the per-(site,tile) ban is invisible to sibling
  walks** — the DEF decline falls through to _deny_target, which steps back
  onto the banned tile. Bounded (116r freeze → 8r oscillation → gone), real,
  routed below.
- **(iii) guarded-tile freezes: PASS on the registered form.** The F1 21→724
  ore-freeze regression contains ZERO rounds on guard paths (frozen body 237:
  wg counters 0/0/0, ban {} for its whole life, never adjacent to a banned
  tile, no BASE counterpart) — it is an **unguarded nav-stall**
  (_deny_target→_nav→step_to produces no step, no verb, body NOT boxed: two
  free neighbours) inside a divergence-shuffled game whose root WAS a
  legitimate guard firing (r63, audit row 30's exact tile). Where guard states
  occurred, freezes went to zero.
- **Guards: ALL PASS.** alive-sum 53(+0), deaths 53(−1), eco +0.4%, harv
  +0.5%. Informational: wins 31→32, kills 14→18, **F3 13→15 wins** (one from
  the 16/30 victory bar), F3 freeze mass −37.4%, global pool −18.0%.

**NEW BASELINE:** t_wg_* sums [alive 53 / deaths 53 / wins 32 / kills 18 /
eco 36.00 / harv 209]. F1 8, F2 9, F3 15 wins.

**ROUTED RESIDUALS (the diagnostic's two live findings):**
1. **Cross-site ban blindness** — a declined walk's fall-through sibling
   re-targets the banned tile. Candidate fix: same-tile bans visible to all
   sites, or the decline carries the tile into the fall-through's exclusions.
2. **The nav-stall class is the measured dominant residual freeze mechanism**
   (bifrost bot 237: 686r with free neighbours; bifrost bot 3: 979r keeper
   nav-stall; midgard bot 3: the ban-comment's own oscillation still live at
   an unguarded site). Class signature: a walk returns a target, step_to
   yields no step, the role falls through with NO VERB, silently, for
   hundreds of rounds. This is the #131 family with fresh anchors — the next
   survival plank is a stall detector at the WALK EXECUTOR level (all walks,
   not three sites).
