# Handover — 2026-08-08, after session 7 (candidate endgame, tag `ladder1`)

Start here, then [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md) → [docs/opponents.md](docs/opponents.md).

## Naming, because the platform has overtaken us

**The platform's submission `v45` is x3r0's `florent-v63`, not ours** — vendored locally as
`bots/opp_v45`. Our own artifact directories (`bots/_pkg45`, `bots/_pkg45b`) were named before
that landed and are kept only because every row in `results.tsv` references those names. **Do not
call our challenger "v45" anywhere durable.** It is *the `ladder1` candidate*; the platform
assigns its number at upload.

## The decision on the table: the honest answer is a base switch

**The `ladder1` candidate is assembled, fully gated, crash-free, and a large clean improvement on
our own line — and it is not the team's strongest bot, and cannot be made into one from here.**

| gate (480 matches: 15 maps × 16 seeds × both orderings, `--tle 10`; rush runs 240) | result |
| --- | --- |
| **vs `bots/opp_v45` (PRIMARY GATE — x3r0's active "florent-v63")** | **22.1% [18.6%, 26.0%] — fails badly** |
| vs `bots/opp_v44` (previous teammate bot, now a reference) | 44.8% [40.4%, 49.3%] — fails |
| vs `bots/aug7` (`3cfa588`, pinned incumbent) — the facing change alone | **58.5% [54.1%, 62.9%] — accept** |
| **vs `bots/_incumbent` = submission `v40`, what our line last put on the ladder** | **67.1% [62.8%, 71.1%]** |
| no-collapse vs `bots/starter` | 83.5% [80.0%, 86.6%] |
| no-collapse vs `bots/opp_v39` | 73.1% [69.0%, 76.9%] |
| rush stress vs `bots/rush_probe_fast` (the real instrument) | 62.1% [55.8%, 68.0%] — **below `aug7`'s 68.3%** |
| rush stress vs `bots/rush_probe` (the weak one) | 93.8% [91.2%, 95.6%] |
| `jackpot` mirror probe, seat A, 32 matches | **0/32 → 15/32 = 46.9% [31%, 64%]** |
| **crashes, our side, every run above** | **0** |

**Recommendation: do not activate the candidate. Switch bases to `florent-v63` and carry our
findings across, not our code.** Three independent measurements say the same thing:

1. **The gap is not closable by economy work.** `opp_v45` beats `aug7` 80.0% and our candidate
   78/22. Our whole session's accepted change moved that matchup by about **2 points**
   (20.0% → 22.1%).
2. **Their economy is already better than ours, so our accepted fix has nothing to give them.**
   A 20-replay census: their conditional delivery rate is **86.2% against our 70.0%**, and they
   collect **14% more titanium while building 42% fewer structures** (651 vs 1,115; conveyors
   552 vs 1,038). They do not have the facing defect we spent the session repairing.
3. **The decisive gap is combat, and it is stark.** Of their 15 wins over us in that census,
   **11 were Core kills. Our Core died 11 times in 20 matches; theirs died zero times.** Their
   first Sentinel lands at **median round 24 against our 51**, and they field Gunners (59 built,
   18 surviving) where we build none.

**What we can still contribute to the team's strongest bot** — these are real and worth more than
our lineage is:

- **A reproducible economy failure in `florent-v63` itself: on `heart`, seated as team B, it
  builds ZERO harvesters and collects zero titanium** — 2 of 2 seeds, and we sweep `heart` 4-0
  because of it. Same *class* of bug as our own (0,0)-Core defect. **Report this to x3r0 first;
  it is the highest-value thing in this handover.**
- **`fjordgate`, and small maps generally.** Their line disables its vision-triggered battery
  below a map-area threshold; we take `fjordgate` **26/32** against v63 and took it **32/32**
  against v44. Whatever base wins, that gate should go.
- **The (0,0)-Core store fix**, if their line still writes raw coordinates (check the v58→v63
  catalogue in [opponents.md](docs/opponents.md)).
- **The instruments**: `tools/replay_census.py`, `tools/arena.py`, and `results.tsv` as the
  append-only tape. The delivery census above took twenty minutes because those already existed.

If the team wants the artifact on the platform anyway — it costs nothing and preserves the work:

```bash
# Magnus only — bots/v* is write-protected for agents:
cp -r bots/_pkg45 bots/v5          # v5 is the next free LOCAL freeze slot (v1..v4 exist)
.venv/bin/fcode submit bots/v5 --name ladder1-trail-facing
.venv/bin/fcode submission list    # note the version number it is assigned
# Do NOT activate it: fcode submission activate <n> would replace a bot that beats it 78/22.
```

## What is in the candidate, and what each piece bought

Two changes over `bots/aug7` (`3cfa588`), each measured separately.

**1. Trail-linked conveyor facing** (`_try_move`, `NEAR_CORE_FACING_DIST_SQ = 18`). A builder
walking *outward* faces each new trail conveyor **back at the tile it came from** — an exact
link that survives bends, staircases and detours — but only beyond dist² 18 from the Core.
Inside that radius `aug7`'s "dominant axis toward the Core" rule is kept byte-for-byte.
**58.5% [54.1%, 62.9%] over 480 vs `aug7`**, above half on 12 of 15 maps, largest margin
`heart` 26/32 — the map where zero-delivery was first observed.

**2. The (0,0)-Core store fix** (the five-liner that has been waiting on a decision since
session 6). It ships on a **correctness** argument, not a pooled win rate: those two slots have
**exactly one writer and one reader**, so the patch is **provably inert on every map whose Core
is not at (0, 0)** — `jackpot` alone in this rotation — where it takes seat A from 0/32 to
15/32 and from "exactly zero titanium, every game" to a normal economy.

## The finding that matters more than the win rate: facing is a *global* problem

**The first implementation of change 1 was refuted at the screen — 11.1% [6.1%, 19.3%], losing
on all 15 maps** — and diagnosing it produced the session's real result. It faced every outward
conveyor back down its own trail, everywhere. A 30-replay census
(`tools/replay_census.py`, plus a purpose-built cycle-detecting graph walk):

- **931 of its 2,133 non-delivering conveyors (43.6%) sat in closed cycles. `aug7` had zero.**
  Two builders crossing the same corridor in opposite directions point at each other, and
  **84% of those cycles were within Chebyshev distance 5 of the Core**, where trails converge.
- `aug7`'s rule cannot produce a cycle *by construction*: "point at the Core" is a global
  potential field and every arrow descends it. A per-builder local rule has no such guarantee.
- Secondary and as predicted: dangling heads landed on a builder's own **spawn tile 23.6%** of
  the time (`aug7`: 4.8%) — the first trail tile points back at a tile that never gets a conveyor.

**The transferable rule: a local facing rule is only safe when anchored to a global one.** That
is exactly what the near-Core zone does in the shipped version, and the census confirms it —
**0 cycles in 1,891 non-delivering conveyors.**

## Three corrections to things we believed yesterday

1. **The rush probe is weak, and one number was relayed inverted.** `aug7` beats `rush_probe`
   **96.2% [93.0%, 98.0%]**; the defense-carrying `ladder1` scored **94.2% [90.4%, 96.5%]** —
   overlapping, if anything *worse*. The belief that reactive defense had "inverted a 95/5 rush
   matchup" came from reading the defender's win rate as the rusher's. **Standing rule now:
   every metric report names both sides — "X beats Y at N%", never "the baseline is N%".**
   `arena.py` reports the **first-named** bot's rate.
2. **The reactive-defense port's "violently bimodal per map" split was never its own.** The
   candidate carries no defense change and collapses on the *same* maps against v44 (`atoll`
   1/32, `hive` 4/32, `jackpot` 6, `drumlin` 6, `meander` 9) while winning the same ones
   (`fjordgate` 32/32, `archipelago` 28/32, `heart` 22/32). **It is a property of the
   aug7-lineage-vs-v44 matchup.** The ore-starvation story was explaining a pattern that was
   already there.
3. **Mechanism metrics and win rates keep coming apart, three times today.** The shipped facing
   change leaves the end-of-game conditional delivery rate statistically *unchanged* (52.9% vs
   `aug7`'s 53.1% head-to-head) while winning 58.5% — what moved was volume, **+29% titanium,
   +19% harvesters**. The discarded tie-break did the opposite: conditional rate **28.3% →
   74.0%**, terminal dangling conveyors **175 → 10**, and a **dead 50.0%** win rate.
   **End-of-game `chain_dir` is a snapshot; it cannot see time-to-first-delivery.** Measuring
   the round of each team's first delivery is now the highest-value instrument change.

## What is deliberately NOT in the candidate

- **The reactive home-defense port — now RETIRED, not pending.** `bots/_defense_port` has been
  measured on every instrument we own and has never once been positive: **40.6% vs `opp_v44`**
  against a 40.8% baseline; **94.2% vs the weak `rush_probe`** against `aug7`'s 96.2%; and now
  **61.3% [55.0%, 67.2%] vs `rush_probe_fast`** — the competent Launcher-insertion probe built
  specifically to test it — against **`aug7`'s 68.3% [62.2%, 73.9%]**. Intervals overlap
  everywhere, so nothing here is a proven regression, but three instruments pointing the same
  way is a verdict. **The mechanism (threat detection decoupled from our own economy) may still
  be right; this implementation is not.** Keep the directory as a reference, stop gating it.
- **The deterministic trail-aware tie-break** (`bots/_tiebreak1`, and assembled as
  `bots/_pkg45b`). Screen 50.0% [39.9%, 60.1%], confirm **52.9% [48.4%, 57.3%]** — no verdict,
  therefore discard. It leans positive and its mechanism evidence is the strongest we have;
  resolving a ~3-point effect needs on the order of 1,900 matches. **Top of the next candidate's queue.**
- **Tuned constants.** A full CEM sweep of `MAX_BUILDERS` / `TARGET_HARVESTERS` / `AMMO_BUFFER`
  against v44 confirmed at **40.8% — identical to untuned `aug7`.** The gap is structural, not
  tuning. Directionally the elite distribution drifted `TARGET_HARVESTERS` 3→4 and `AMMO_BUFFER`
  20→~14. **Re-tune after the delivery economy changes, not before:**
  `.venv/bin/python tools/tune.py _pkg45 opp_v44 --guards starter opp_v39`.
- **BFS pathfinding** — still discarded, code in `bots/_dev_bfs` (see session 6's entry).

## Known residual weaknesses

- **`atoll` 1/32 and `hive` 4/32 against `opp_v44`, and 0/32 on both against `opp_v45`** — the two lowest-ore maps in the pool. Single
  matches are unambiguous about the mechanism: on `hive` we finish with **125 buildings to their
  16** while collecting **400 to their 1,190**, and lose the Core at round 262. **We are
  out-delivered while spending more.** Every walked tile lays a conveyor, at +1% category scale
  each, whether or not that trail ever carries anything. A conveyor budget, a cap, or laying only
  where a trail already reaches a harvester are all cheap and untested. **This is the top
  economy lane for the next candidate.**
- **The near-Core dangling spike is unexplained.** The candidate still shows ~3× `aug7`'s dangling-head
  count at Chebyshev distance 1-2 — in a zone where its code is byte-identical to `aug7`. The
  far-zone topology is feeding the near zone differently and nobody has said how. Most likely
  place another chunk of delivery is hiding.
- **Small maps: `fjordgate` is our best map against v44 (32/32) for a reason that is theirs, not
  ours** — v44 gates its vision-triggered battery on `w*h > 120`, so on the 10×10 it is
  disabled. The hole read out of its source last session is real and total. **Do not copy that
  gate**, and do not read our 32/32 as small-map strength of our own.
- **Mirror equivariance: still unfixed, still unmeasured this session.** Six of the 15 maps
  mirror; `cardinal_toward` is equivariant, and the new trail rule is defined relative to the
  walk (so it is equivariant under rotation *and* both reflections by construction), but no
  per-map mirror seat table was re-run for the candidate. `jackpot` is now repaired; `heart`, `lighthouse`
  and `atoll` seat asymmetries remain open.
- **`archipelago`'s seat advantage is an engine fact** (team A's Nth builder always gets the
  lower unit id, so A resolves first), not something the candidate changes.

## The next queue, ranked — assuming the base switch

**On `florent-v63` as the base:**

1. **Tell x3r0 about the `heart` seat-B zero-harvester failure** and help fix it. Reproducible,
   costs them a whole map, and it is the same class of bug as the (0,0)-Core defect we fixed.
2. **Remove the small-map area gate on their vision-triggered battery.** We beat v44 32/32 and
   v63 26/32 on `fjordgate` largely because of it.
3. **Census their delivery on the maps where it is weakest** (`atoll` 68.8% conditional against
   our 100% there) — that is the one place our facing work may still transfer.
4. **Re-run the per-map mirror seat table on the new base.** Six of fifteen maps mirror; nobody
   has checked whether their line is equivariant.

**If the team keeps our lineage alive anyway** (as a second submission, or for the learning):

5. **Combat, not economy.** 11 of 15 losses to v63 are Core kills; our Core died 11/20, theirs
   0/20. Enemy-Core tracking, `ct.fire()` sabotage, and Gunners are all still unbuilt, and their
   first Sentinel lands at round 24 against our 51.
6. **Instrument time-to-first-delivery** and re-read every facing result against it — the
   end-of-game snapshot demonstrably cannot see what our accepted changes are buying.
7. **Conveyor spend per delivered titanium.** We build 1,115 structures to v63's 651 and collect
   14% less. Every walked tile lays a conveyor whether or not that trail will ever carry
   anything.
8. **The tie-break** (`bots/_tiebreak1`), at resolving power or on the correctness argument.

## Operating notes for the next session

- **The submission-watcher monitor does not survive this session.** It was a persistent monitor
  attached to the main session and dies with it. **Re-arm it** if you want submission/activation
  changes noticed automatically; nothing on the platform side reports them to us.
- **Standing norm: the team slot follows arena measurement.** A candidate that beats `opp_v44`
  takes the slot, with the numbers attached. This candidate does not, so it does not.
- **Date labels still run one day ahead of wall clock.** Every commit here is authored
  `Thu Aug 6 2026`; the log labels sessions 5-7 as `2026-08-07`/`08`. **Three logged "days" are
  one calendar day.** Left deliberately rather than silently renumbered.
- **Never reset `bots/ladder1` while an agent is measuring it** — still true, and it shaped this
  session's sequencing (the corrected variant was built in `bots/_facing_v2` precisely so a
  running census agent kept a stable artifact).
- Protected from edits: `tools/arena.py`, `tools/make_map.py`, `maps/`, `bots/starter`,
  `bots/v*`, `bots/probe_*`, `bots/rush_probe*`, `bots/opp_*`, `program.md`. Platform *write*
  commands (submit / activate / rename) are Magnus-only.
- `results.tsv` is the append-only tape and stays untracked; every run above is a row in it.
  Still no `git remote`.

## Where things live

| path | what it is |
| --- | --- |
| **`bots/_pkg45`** | **the candidate.** `bots/ladder1` is a byte-identical copy |
| `bots/_facing_v2` | the candidate minus the (0,0) fix — the artifact the accept was measured on |
| `bots/_pkg45b`, `bots/_tiebreak1` | the discarded tie-break, packaged and standalone |
| `bots/_defense_port` | the reactive home-defense port, preserved, awaiting `rush_probe_fast` |
| `bots/aug7` (`3cfa588`) | pinned incumbent |
| `bots/_incumbent` (`a9d81a1`) | submission **v40** — what the ladder last ran from our line |
| `bots/opp_v45` | **x3r0's new active bot** (platform submission v45, "florent-v63") — the primary gate |
| `bots/opp_v44`, `bots/opp_v39` | the previous teammate bot (secondary reference) and the older guard |
| `bots/rush_probe`, `bots/rush_probe_fast` | the weak walked rush, and the Launcher-insertion probe |
| `bots/_fix_core00`, `bots/_dev_bfs`, `bots/_facing_v3` | superseded / discarded, kept for reference |
| safe to delete | `bots/_tune_*`, `bots/_diag_*`, `bots/_probe_*`, `bots/aug7_h1..h4` |

## Traps

All previous ones still apply — `python3` is 3.14 so use `.venv/bin/`; always `--tle 10`;
`print()` goes to the replay, use stderr; `random` is not seeded by `--seed`; never single-seat
or pooled-only evaluation; `ct.get_cpu_time_elapsed()` is inert under `fcode run`; the validator
rejects `try`/`finally`; tile queries raise outside vision; the comms store cannot represent a
zero; a pooled win rate cannot see a single-map defect. New this session:

- **`arena.py` reports the FIRST-NAMED bot's win rate.** A bare percentage in prose is a coin
  flip. Name both sides, every time.
- **A cross-tab that contradicts the headline is a defect to resolve before relaying**, not
  colour to relay alongside it. Both times the rush number went wrong, the contradicting
  cross-tab was in the same file.
- **A screen that fails uniformly across all 15 maps is a mechanism defect, not a refuted
  hypothesis.** 11.1% on every map meant "this breaks delivery everywhere", and the fix took one
  iteration once the census named cycles. A hypothesis refutation looks patchy; a broken
  mechanism looks flat.
- **Any facing/routing rule computed per builder can create cycles.** The census's cycle count is
  the diagnostic; it is not part of `replay_census.py`, it was a throwaway graph walk over its
  parsed output. Rebuild it before trusting the next routing change.
- **In zsh here, `set -- $var` inside a loop does not populate `$1`.** Cost two failed
  diagnostic runs; write the arguments out explicitly.
