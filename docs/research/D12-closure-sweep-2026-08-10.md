# D12 SWEEP — every closure in the repo, classified by evidence basis

**Side lane, 2026-08-10 07:1x CEST.** Sonnet subagent, read-only. Applying
Magnus's live-evidence standard (D12) to the whole corpus, not just the docs this
lane happened to remember.

**Coverage, stated before the findings:** `CLAUDE.md`, `PROGRAMME.md`,
`game-model.md`, `builder-method.md` read in full or near-full; `HANDOVER.md`
(2,106 lines) sampled ~250 lines across highest-signal blocks; `coordination.md`
(26,117 lines) — 1,236 headers skimmed, **123 `REFUTED` hits**, 12 read in depth;
`docs/research/tactics/` — **31 of ~244 files (~13%)**; `docs/research/` —
**32 of ~191 `.md` files (~17%)**, ranked by hit-density. **Closure-keyword hits
total: coordination 786, tactics 207, research 1,038.** This is a
**high-signal sample, not a census**, and the agent said so unprompted.

**Instrument note:** positive controls (`grep -c -i titanium`) run before every
sweep, all non-zero. **The agent hit the zsh unquoted-variable trap itself** — a
multi-path `$TARGETS` collapsed to one non-existent path and silently returned 0
for every keyword — **and caught it with the control.** Third instance of that
failure mode tonight, first one caught by a guard rather than by surprise.

## TALLY

| verdict | count | meaning |
|---|---|---|
| **EXEMPT** | **7** (+1 partial) | rules-level engine facts, no behavioural premise, premises quoted |
| **UNCLEAR** | ~15 | basis undeterminable from the document |
| **DEMOTE** | ~50 | must be relabelled hypothesis, sent to the bottom of the queue |

**Essentially ZERO of the sampled DEMOTE rows cite a fresh `fcode match unrated`
run against a real opponent to test the claim.** That is the same pattern the
six-roads audit found, reproduced across the whole corpus.

## THE EXEMPT SEVEN — these survive D12 and should not be re-tested

Sandbox freezes `time.*`/`datetime.now` to a constant · `self_destruct` deals 0
damage · cost-scale tracks LIVE entities so churn is not a weapon · the comms
store is private per team, closing jamming and spoofing · builder bots cannot
damage enemy builder bots **at all** (so worker-pull cannot exist here) ·
`destroy()` targets allied *buildings* and a builder bot is the one unit that is
not a building · a 3 Ti barrier on an empty ore tile vetoes a 20 Ti harvester
(probe with a restore control).

## THE FINDING THAT IS BIGGER THAN THE ONE I BRIEFED

**"THE FORWARD ROAD IS CLOSED" is asserted as settled fact in at least SEVEN
tactic files** — `when-the-plan-aborts-say-where-its-units-go.md:93`,
`manner-pylon-and-what-the-rules-permit.md:98`,
`the-scout-that-pays-for-itself.md:74`, `pay-a-positional-price-to-deny.md:83`,
`spawn-the-attack-at-the-target-not-a-march.md:41`,
`defenders-advantage-has-exactly-two-mechanisms.md:104-105`, and one more.

**Its evidentiary floor already collapsed, in the index those files should have
been checked against.** `tactics/INDEX.md:1076-1081`: *"the +11.4/+16.6/+22.3pp
home-defence advantage… DOES NOT REPRODUCE… n=439 supports 'does not reproduce',
NOT 'refuted'."* **None of the seven carry the caveat.** This is the largest
blast radius in the corpus and it is a propagation failure, not a measurement
failure — the correction exists and never travelled.

**Same shape, three more files:** `worker-fortified-turret-cell.md:87`,
`fortify-on-idle.md:43`, `defence-production-pegged-to-economy.md:106` each
assert turret production was *"already refuted four ways"* with **zero evidence
cited in any of the three**.

## STALE COPIES OF THE SIX ROADS STILL LIVE OUTSIDE `CLAUDE.md`

`CLAUDE.md` was corrected today. **Two other docs still assert the same six flat:**
- **`docs/builder-method.md:24`** — *"imprisonment (refuted)"*, unhedged.
- **`HANDOVER.md:137-139`** — the origin of the claim, still flat.

**A session reading `builder-method.md` first inherits the stale version of a
claim the flagship doc has already walked back.** Correcting one copy of a claim
is not correcting the claim.

## THE WEAKEST CLOSURE IN THE REPO

**`HANDOVER.md:130-136`** kills suicide-builder rush, cheap-builder swarm,
infinite-heal blob and two-sentinel one-shot **by analogy to the patch notes of a
DIFFERENT GAME** (Cambridge Battlecode 2026), with the document's own caveat
*"Values do NOT transfer… intent does."* **Zero evidence from our engine or from
any game we have played.** Weaker than self-play, and the cheapest possible thing
to actually test.

## A BROKEN CITATION

`a-gunner-kill-is-a-clear-line-not-a-doctrine.md` and
`the-tower-heavy-mix-was-an-artefact-not-a-doctrine.md` both cite
`copying-the-top-tier-is-not-free.md` for a *"garrison refuted 40% vs 60%"* claim.
**That file was read in full and contains no garrison content at all.**

## MY OWN DOC IS ON THE LIST, CORRECTLY

`league-fast-kill-mechanism-2026-08-10.md` is flagged as *"a plank RETIRED ON n=4
that the same document says should be REOPENED — an internally-flagged textbook
violation."* **Accurate.** It is labelled that way deliberately, but the agent is
right that a document containing both the retirement and its own refutation is
not a resolved state.

## THE FIVE WORTH TESTING LIVE FIRST (agent's ranking, adopted)

1. **`HANDOVER.md:130-136`** — four tactics closed on another game's patch notes.
   Cheapest to test, highest chance of surprise, literally never tried here.
2. **The "turret production refuted four ways"** cluster — asserted, uncited, 3 files.
3. **The "FORWARD ROAD IS CLOSED" cluster** — 7 files resting on a floor that
   INDEX.md already walked back.
4. **Imprisonment / barrier-lock** — the probe's own text says the enemy case was
   never tested; already reopened in `CLAUDE.md` and already nominated as the
   first live leg.
5. **"Plant closer"**, retired on n=4 by its own document's admission.

## WHAT THIS DOES NOT ESTABLISH

**It is a sample, not a census** — 13% of tactics files, 17% of research files.
**A DEMOTE verdict means "not established as closed", never "the road works".**
And under D12's own bottom-of-queue clause, **none of these fifty items jump the
queue; they cease to be reasons NOT to look.**
