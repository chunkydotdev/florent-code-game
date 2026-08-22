# COMMISSION — FIRST-CONTACT MECHANISM DECODE (Skalman rc v180: reach, first-damage, fidelity vs the field)

Commissioned by: RESEARCH s54, 2026-08-22 ~09:4xZ. Corpus synced (the 13 first-contact matches are decoded).
PROVENANCE (inputs — read these; open every anchor):
- The 13 matches (wire-verified ids, all ours v180 unless noted): MIRROR vs Bean counters v68 pinned:
  4bc7ed13, e46e55fd, 0e5b63ea, 5ee3afec (08:24Z; 0-5,0-5,0-5,1-4). PIVOT v249 pinned: ab068a0d,
  e200bcab, 919000f0, 64a8beb6 (0-5 ×4). KLADDE v173: 82a03bfd, b6ec7f91, d18b7d7b (1-4), 0de59936,
  abd8f4fc (0-5 ×4 + the 1-4). Replays in replay_archive/<id>_game_N.replay26; corpus tables synced.
- `docs/research/FIDELITY-READ-v602-2026-08-21.md` + the builder's later fidelity reads — the mechanism
  column set Skalman is graded on (answer-latency is a standing column since ~07:43Z).
- `docs/research/REPLAY-STUDY-kladde-v173-2026-08-22.md` — the kladde bars: REACH (do our turrets ever
  cover their sentinel's approach/siting tiles) and FIRST-DAMAGE-ROUND on their core (their beaters: 83%
  of games ≥1 damage; us historically 31%). Reuse `scratchpad/s54_klad_lib.py` decoders where applicable.
- `docs/research/PLAYBOOK-beancounters-2026-08-21.md` §6 COPY 1-9 — the mirror fidelity checklist.
- `docs/research/CUT-116-beltgun-answer-2026-08-21.md` — belt-gun siting geometry (BC removes 75.9%).
- **Q3d labels:** the cell scores above are wire facts I verified; every mechanism claim about v180's
  TREE is UNVERIFIED from here — read behavior off the REPLAYS, not off any bots/ source, and do not
  open bots/ trees at all (the replay is the evidence surface; tree attribution is the builder's).

## QUESTIONS (per cell, all decode-only)
1. **KLADDE CELL (the amended bar):** per game — our REACH (any v180 turret whose attack pattern ever
   covers the tile their killer sentinel fires from, or its approach path), their sentinel's siting round
   + our answer latency if any, our FIRST-DAMAGE-ROUND on their core (vs their beaters' benchmark), and
   what killed us + at what round. The 1-4 game (d18b7d7b) gets a round-by-round arc: what did the taken
   game differently?
2. **MIRROR CELL:** fidelity in contact — which COPY verbs executed under BC's real pressure vs the
   NOISE_OFF fixture (cage/ring barriers placed? drip converts? nest sited in-band? belt survival rounds)?
   Where does the real BC kill us relative to the benchmark copy (round, mechanism)? The 1-4 game
   (5ee3afec) arc: what landed?
3. **PIVOT CELL:** kill mechanism + round; did their belt-gun shape (the #116 finding) appear against us?
4. **CROSS-CELL:** first-damage-round table (ours-on-them / theirs-on-us) for all 13 matches; turret
   reach coverage summary; any exception-death of OUR units (0 expected — flag any).

## METHOD BARS
Known-cell validation first (reproduce the 13 match scores/turns/cond from your decode path — they are
in unrated_games.tsv and above). n=65 games on 3 opponents: counts and per-game lists over intervals;
if you quote an interval, DEFF-caveat it. INFERENCE inline on causal sentences. No queue/coordination/
bots/tools edits, no commits.

## DELIVERABLE
`docs/research/DECODE-firstcontact-v180-2026-08-22.md`. Final text = data return: the kladde-bar table
(reach / first-damage / answer-latency), the mirror fidelity-in-contact summary, kill mechanisms per cell,
the two 1-4 arcs' answer, validation result, anything that refutes a commission premise.
