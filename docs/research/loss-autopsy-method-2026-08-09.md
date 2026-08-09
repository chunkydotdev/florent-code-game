# The loss-autopsy loop: what killed us, would another trick have won, would a combination have turned it

**Side lane, 2026-08-09 15:2x CEST, on Magnus's directive: after the unrated
games, check what killed us — would another trick have won, would a
combination have changed the tide. This is the repeatable method, prototyped
NOW on already-decoded rated losses so it runs the moment unrated replays
land. Zero downloads; the decoders are warm.**

## The loop (runs on any batch of our losses — rated or unrated replays)

For each game we lost, four questions in order, each answerable from the
decoders we already have:

**1. WHAT killed us** (`dc_deaths` + `bb_rows` + the shooter table):
- **Core killed by turret siege** — split gunner (point-blank, d²≤13) vs
  sentinel (stand-off, ignores obstacles). This is 99% of early losses.
- **Out-economied to a tiebreak loss** — core survived, we lost on delivered
  titanium / harvesters. (Rare for us — we win 57% of tiebreaks.)
- **Builder attrition → economic collapse** — no single core event.
- **Crash / no-damage removal** — 0 for us historically; watch it on new bots.

**2. COUNTERFACTUAL: would surviving have won?** (`bb_rows` core HP + economy
state at death). This is the question that decides whether the answer is a
*tempo/defensive* trick or an *economic/offensive* one:
- If we were **ahead on delivered titanium** (or would win the r1000 tiebreak)
  at the moment our core died → **surviving = winning**, so the indicated trick
  is whatever buys survival or kills first. Do NOT add economy; we had it.
- If we were **behind** → a survival trick only extends a loss; the indicated
  trick has to change the economic or kill race itself.

**3. WHICH trick targets that cause** (map to `offensive-catalog` A-list):
- sentinel siege → **A1 (rush: kill before their line matures)** — it can't be
  tile-denied (obstacle-ignoring), so out-tempo is the only lever.
- gunner siege (point-blank) → **A1 or A3 (spawn-ring: contest the tiles)** —
  point-blank IS tile-contestable.
- out-economied → **A7 (tiebreak key-1 pressure)** / **A8 (heal uptime)**.
- never-rotating-gunner defender → **A4 (off-axis flank)**.

**4. COMBINATION: is one trick enough, or does the cause require composing?**
The key question Magnus named. A cause that a single trick can't answer flags a
*combination*: e.g. a sentinel-vs-sentinel race — a gunner-only rush loses it,
so the indicated answer is **A1 (our sentinel rush) + A3 (spawn-ring to
suppress their heal while we race)**, which compose because they don't compete
for tiles (sentinel fires through the collar). One trick is insufficient
whenever the loss cause is itself two-piece.

## Worked example — the 47 CAD losses we've already decoded

Ran the loop on our decoded CAD core-kill losses:

| autopsy field | result |
| --- | --- |
| WHAT killed us | 47/47 turret siege; **18 sentinel-dominant, 29 gunner-dominant** |
| timing | 11 died ≤r250 (fast rush), 36 died >r250 (grind) |
| COUNTERFACTUAL | **all 47 counterfactually winnable** — we're 16-4 vs CAD at the r1000 tiebreak, so for every core-kill loss "would surviving have won?" is YES by base rate. The economy edge is already ours. |
| INDICATED trick | survive-or-kill-first, never add-economy → **A1 rush** (29 gunner losses also open to A3 spawn-ring) |
| COMBINATION | **18/47 need A1+A3 together** — against a sentinel-dominant siege a gunner-only rush loses the race; our own sentinel rush + the spawn-ring collar compose and neither alone wins the sentinel-vs-sentinel race |

**The answer to Magnus's three questions, for CAD:** what killed us = a
two-piece turret siege, sentinel-led in 38% of losses; would another trick have
won = yes, because we already win these games if we survive to r1000, so *any*
survival/tempo trick converts them; would a combination have turned it = **for
the 18 sentinel-led losses, yes and only a combination** — A1+A3, because the
loss cause is itself two-piece and no single trick answers both halves.

## Running it on the unrated batch (the live use)

When the unrated fixture games land (docs/research/unrated-fixture-hard-teams),
the pipeline is mechanical:
1. Archive the unrated replays (they enter `replay_archive/` like any game).
2. Decode with the warm decoders (`dc`/`rx`/`bb`, ~2s/50 games).
3. Run the four-question loop per loss → a per-loss trick indication.
4. **The output is a ranked "next trick to add" list**, per opponent, with the
   combination flags — which is exactly the build queue for the following
   unrated round. Loss → mechanism → candidate trick → test → repeat.

This closes Magnus's loop: we don't guess which trick to build next, we read it
off how we actually died, and we test the indicated trick (or combination) in
the next free unrated cycle. The autopsy makes the free tool *directed* instead
of a fishing trip.

## Honest limits

- The counterfactual is an **indication, not a simulation** — we cannot replay
  the game with trick X inserted (no local engine that mutates a live game).
  "Would trick X have won" is answered as "trick X targets the measured cause
  of death and the economy state says survival converts," which is a testable
  hypothesis, not a proof. The test is the next unrated cycle.
- Combination claims inherit that limit doubled — "A1+A3 would have won 18
  games" means both target the two-piece cause, not that we simulated it.
- Small per-opponent n on unrated (47% power at n=10) — the autopsy tells you
  *what to try*, the ladder confirms *whether it worked*.

## Provenance

Prototype: `cadpass/games.tsv` + `cadpass/shooters.tsv` (75 CAD replays,
decoded this session). Autopsy logic grounded in the verified 16-4 tiebreak
fact (cad-core-kill-2026-08-09) and the trick map from
offensive-catalog-2026-08-09. Method is decoder-agnostic — same four questions
run on any loss batch.
