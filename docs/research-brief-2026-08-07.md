# Research brief — session 12 parallel fan-out (2026-08-07)

For the researcher session: read this file top to bottom, then execute it. Magnus
runs the lead on Fable/xhigh; subagent tiering guidance is in the mission block.

---

You are a parallel RESEARCH SESSION for the Florent Code League repo at
/Users/junghard/Projects/Work/florent-code-game. The measuring session (main
session) is running concurrently — Fable, session 12. You read everything and
measure nothing. Magnus has authorized a wide fan-out: spawn as many parallel
subagents as the threads below warrant (the last research session ran 19+;
match or exceed that where the work supports it). Suggested tiering: Opus for
code-read/synthesis threads, Sonnet for mechanical replay decoding; you hold
all verdict-quality judgment yourself.

ORIENT FIRST (in this order): HANDOVER.md (all of it, including FINAL
ADDENDUM), docs/spitball.md (all of it — your predecessor's findings and the
external-meta scavenge are there), docs/game-model.md, the Traps section of
HANDOVER.md. The project CLAUDE.md is the organisers' doc with known errors —
game-model.md wins on any conflict.

HARD RULES (the measuring session's discipline depends on these):

- NO arena runs, NO fcode submit/activate/rename, NO unrated or test
  challenges (the rate limit is shared), NO edits to any file under bots/,
  and no writes to results.tsv, elo_history.tsv, HANDOVER.md, or docs/ EXCEPT
  appending to docs/spitball.md.
- Platform reads (match list/info/replay downloads) are allowed — pace them,
  stagger your subagents' downloads a few seconds apart, and share one replay
  cache directory in your scratchpad so nothing is downloaded twice.
- Use .venv/bin/python everywhere (system python3 is 3.14, unsupported).
- Replay tooling: tools/replay_census.py + tools/replay_schema.md are the
  reference decoders; derived scripts from past sessions are gone — have ONE
  subagent regenerate a shared decode toolkit first (~10 min) and give it to
  the others, rather than 19 agents each rebuilding it.
- Findings go to docs/spitball.md as appended bullets (date + author tag),
  with file:line or replay/match ids on EVERY claim. Verdicts (KEEP/REFUTED/
  PARKED) belong to the measuring session — never write them. Anything HOT
  (changes what the measuring session should build TODAY) should also be
  messaged to the main session directly.
- CORRECTIONS to existing spitball claims are first-class results — the v82
  attribution correction was the most valuable line of the last cycle. Verify
  before you extend.

ALREADY CLAIMED by the measuring session — do not duplicate: Ouroboros decode,
seat-B builder-death role breakdown, the siege-solvency build (_v74e4) and all
its screening, cad_probe re-freeze. You may still THEORIZE around their edges
(e.g. eider throughput is explicitly yours, hive solvency is not).

MEASURING-SESSION UPDATE (2026-08-07 ~12:20, fold into your priors): the
siege-solvency package screened production-flat on hive vs kladde_probe (0/32
identical to baseline 0/32, all titanium_collected, zero core deaths either
leg). The hive loss mode for the CURRENT line is farm death r63-390 followed
by 10:1 economy starvation, NOT core death — the decoded core_destroyed@787
replay was the v55-era shape. This RAISES the value of threads 2 (lane math)
and 4 (tiebreak margins): the grind front is now known to be economy-bound on
both of its maps.

## THREADS, tier 1 (decisive and cheap — run these first)

1. DETERMINISM FALSIFIER. If a (map, opponent-version) pairing replays
   identically, every repeated rated loss is the same lost game re-lost, and a
   ~10-line decision-noise injection converts guaranteed losses to coin flips
   at +3.2 Elo/game. Find pairs of our rated matches vs the same opponent
   version on the same map (match-list JSON has versions), decode both, diff
   round-by-round. Deliverable: identical-or-not with evidence, and a count of
   how many of our ~230 rated games were exact repeats — that count is the
   prize pool.
2. LANE-SATURATION AUDIT vs ECO_CAP=18. Known math: one conveyor lane moves 10
   Ti/round = exactly 4 harvesters' output; the 2x2 core has 8 orthogonal
   input tiles = 80 Ti/round ceiling. Decode our economy-race games (eider
   losses to kladde especially — 16 enemy builders vs our 5-12, both cores
   near full HP at r1000; hive now belongs in this bucket too, see the update
   above): how many distinct input lanes do we actually wire, at what round
   does marginal harvester N stop adding DELIVERED titanium, how much capital
   sits stranded on belts at the bell? Deliverable: the real throughput
   bottleneck (lanes vs hands vs cap) with numbers per map.
3. KLADDE v62 FRESH DECODE. kladde shipped v62 (~1811); kladde_probe was
   frozen from their older build and is stale. Download recent kladde v62
   games — INCLUDING their matches vs third-party teams, not just vs us —
   and characterize what changed: strike composition, timing, raider count,
   economy curve. Deliverable: a probe-refresh spec the measuring session can
   freeze from (exact behaviors + a representative replay id list).
4. TIEBREAK-MARGIN FLIP CANDIDATES. Two-thirds of games end at r1000 on
   tiebreak #1 (titanium delivered). Sweep our rated losses: for every
   2-3 match and every r1000 game we lost, extract the margin (Ti delivered
   delta, harvester-count delta, stored delta). Atoll was once lost by 190 Ti
   = 8 rounds of one wired harvester. Deliverable: the ranked list of losses
   within reach of (a) an endgame spend-switch at ~r960 (dump bank into
   harvesters + ammo), (b) the harvester-adjacent conveyor splice, (c) one
   more delivered stack — this prices three queued builds at once.

## THREADS, tier 2 (exploit discovery — "play the players")

5. TURRET-TARGETING IDIOM CENSUS. get_attackable_tiles() enumerates row-major
   in absolute coords, so any tutorial-idiom "first occupied tile on my ray"
   loop makes N/NE/NW/W-facing turrets engage the FARTHEST target and
   E/SE/S/SW the nearest. From existing replays, find moments where an enemy
   turret had 2+ candidates on its ray and record which it shot, per nemesis
   (Lunds, CAD, kladde, Flotte, Powerpuff). Deliverable: per-team, per-facing
   verdict on the bias — each confirmed team makes a 3-Ti bait barrier a
   permanent turret blind.
6. BARRIER SIEGE-RING GEOMETRY. For each pool map and each core spawn,
   enumerate the plantable tiles in the chip-siege band (core-dsq 10-41,
   empty/non-wall/reachable), compute the minimal deny-set and its cost
   (claim to check: ~40-60 Ti structurally removes the chip class), and
   cross-check against where Lunds/kladde actually planted in decoded losses.
   Include the predictive trigger spec: gate on "a tile an enemy builder
   could reach next turn", never on "we are under attack".
7. LANDERS + ORIZON AUDITS. The two near-rating nemeses (E≈0.5, best
   Elo/effort) never decoded. Same protocol as the completed Lunds/CAD
   audits: 4-6 losses each, class assignment (rush/chip/grind/other), timing
   signatures, which of our systems failed to engage and why.
8. TOP-8 SINGLE-GAME THEFT PREP. Game-share Elo makes one stolen game vs
   E<0.20 net-positive. Scout Flotte (and optionally Pivot/team lazy) via
   their matches against OTHER top teams: which maps do they drop, to whom,
   by what mechanism? Deliverable: the single most stealable (opponent, map)
   pair and what the winning bot did — the "Flotte-meander-only line of
   study" made concrete.

## THREADS, tier 3 (design specs that feed builds)

9. B8 PORT SPEC. What owns archipelago is v79's top sensing tier
   (gun_sense=100/b_sense=36, fires on area>=650 and mw==mh — archipelago +
   snowflake in this pool); ours is flat 64/16 everywhere. Read
   bots/opp_v58/main.py end-to-end and write the port spec for the Eir
   architecture: state needed, CPU cost vs the 8000us budget, expected
   behavior delta. We are 0/32 on archipelago vs opp_v50-class bots.
10. DESTROY()/WALK-AWAY DOCTRINE. destroy() is free, unlimited, refunds
    nothing but REMOVES the entity's cost-scale contribution — and appears
    zero times in any bot of ours. Quantify from replays: orphaned relays
    (prior measurement: 18 of 40 surviving relays connect to nothing), scale
    inflation from rebuild churn (meander: 201 conveyor builds), and the
    defense bill (we have paid 819/708/905 consecutive rounds of one
    builder's actions defending a single 3-Ti conveyor). Spec: when to
    destroy a doomed relay, reroute short, and walk away; where hysteresis
    (1.75x abandonment penalty / 3x switch threshold) belongs in our target
    selection (_pick and friends in bots/_v72e2/main.py).
11. SEAT TIME-TO-FIRST-DELIVERY. The surviving seat-asymmetry lead on
    atoll/heart/lighthouse (~28-31% seat-B): decode per-seat time to first
    delivered stack, spawn-to-first-harvester, and first contested tile.
    The sign crosses the symmetry-class line, so orientation bugs are dead;
    if seat B's first delivery lags structurally, the counter is an opening
    reorder, not combat.
12. AMMO-SPIKE TRIGGER PRE-MORTEM. We end games with 2,782-3,031 Ti banked
    having fired 13 shots; convert_ammo is uncapped, same-turn, cooldown-free
    — the whole bank converts the round a target appears. From our losses:
    when did convertible targets actually appear vs our ammo level at that
    round? Spec the trigger that would have fired, and what it would have
    killed.

## OPTIONAL, Magnus's call (bends the no-local-runs rule)

The HARVESTER-ADJACENT CONVEYOR SPLICE mechanics probe — two toy bots on an
invented map to test whether our conveyor placed cardinally adjacent to THEIR
harvester captures its output stream. Ten minutes, no shared resources, kills
or confirms a double tiebreak swing. If run: maps/ is permission-locked, so
put the invented map in your scratchpad and pass its path positionally to
fcode run.

## CLOSE-OUT

Append everything to docs/spitball.md under a dated session header, one bullet
per finding, ids on every claim, HOT items messaged to the main session
directly. End with a completeness pass: which threads did NOT run or NOT
converge, stated explicitly — silence must not read as coverage.
