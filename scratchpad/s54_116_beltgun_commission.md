# COMMISSION — QUEUE #116: DO BEAN COUNTERS ANSWER A GUN ON THEIR OWN BELT? (decode-only)

Commissioned by: RESEARCH s54, 2026-08-21 ~16:5xZ.
PROVENANCE (the draft agent's input files, verbatim — read these, nothing else is assumed):
- `QUEUE.md` row #116 (line ~722) — the admitted row this cut discharges.
- `docs/research/PLAYBOOK-beancounters-2026-08-21.md` — §8 caveat 6 is the named gap; §2-§5 for context. **Q3d label: the row's framing ("no removal loop for a belt shooter", n=2) is the ROW's claim sourced from this book — verify the caveat says what the row says before building on it.**
- `docs/research/REPLAY-STUDY-beancounters-v47v68-2026-08-21.md` — the banked base study (the 79.7%±2.2 home-CORE-half forward-turret clearance figure lives here; it is the comparison cell).
- `docs/research/corpus-howto.md` — query the corpus, do not hand-roll a decoder.
- `scratchpad/s53_bean_*` and `scratchpad/s53_beanwatch*` — the s53 instruments. **UNVERIFIED premise, labeled per Q3c: the queue row claims the BUILD/DEATH+position join in these probes "computes exactly this". I verified the FILES EXIST (listed 16:52Z); I did NOT verify they compute the belt-gun stimulus/response join. Verify before reuse; adapt or extend rather than trusting the claim.**
- `scratchpad/s53_bean_meta_join.frozen.tsv` — prefer the frozen join for population stability (the live corpus moves under you).

## THE QUESTION (verbatim intent from the row)
Per-game, at population scale, over ALL archived Bean counters games with the stimulus present:
when an enemy turret (gunner or sentinel) stands within ITS OWN firing range of a BC belt tile
(conveyor/splitter on BC's delivery network), do BC ever attack/remove it? At what latency?
Split v47 / v68 (their doctrine eras — era boundaries are in the base study; do not average across eras).
Contrast cell: their 79.7%±2.2 clearance of forward turrets in their home CORE half (base study).
The finding either way is the split between "defends the castle" and "defends the supply line".

## METHOD DISCIPLINE (non-negotiable)
1. **Validate against a known cell FIRST** (collar-heal standard): before trusting any new number,
   reproduce at least one PUBLISHED figure from the base study on the same pipeline (e.g. the 79.7%±2.2
   clearance, or the 80.3% ore-cap with its 1.0% placebo) and show the reproduction in the deliverable.
   A pipeline that has never produced a known-correct number has not been seen to work.
2. **Placebo/control**: a stimulus definition needs a control that MUST come out the other way —
   e.g. same-window turrets NOT in range of any belt tile (their answer rate = the castle/base rate),
   or a same-shape placebo like the base study's different-tile control. Drive it; do not assert it.
3. **Denominators and subjects inline**: every rate carries n, the population (which games, which era,
   rated/unrated mix), and the clock. BC's pool is ~90% unrated per the base study — internal ratios only.
4. **Cluster caveat**: games cluster by match and opponent; carry the DEFF caveat (CLAUDE.md's measured
   constants) on any interval, or present counts without intervals and say so.
5. **Effects vs causes**: causal sentences carry INFERENCE inline or do not ship. A latency distribution
   is an effect; "they cannot see belt guns" is an inference.
6. **Anchors**: every file:line or figure you cite, you opened. Anything relayed unopened is labeled
   RELAYED-UNVERIFIED.

## DELIVERABLE
`docs/research/CUT-116-beltgun-answer-2026-08-21.md`:
- The known-cell reproduction (method validation) up top.
- The main table: belt-gun answer rate + removal latency, split v47/v68, with stimulus definition
  (range geometry used, belt-tile definition), placebo cell, ns everywhere.
- The castle-vs-supply-line contrast against 79.7%±2.2, stated as a comparison of THEIR cells.
- Limits: what the stimulus definition cannot see (e.g. turrets that died before firing, our own
  attribution blind spots).
- NO ship verdicts, NO queue edits — return the findings; the commissioning lane routes them.

Your final text is the return value: give the headline numbers + deliverable path + any premise
you refuted (a refuted premise of this brief is a first-class finding — say it plainly).
