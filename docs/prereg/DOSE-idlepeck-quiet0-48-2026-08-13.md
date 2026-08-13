# PREREG — #48 rungs: IDLEPECK (surgical) + QUIET0 (doctrine ablation)

**Committed before any dose game or shard heartbeat (two-clock per readout).**
Builder s37, 2026-08-13. Basis: research's #48 full-width cut (10.68% of ALL
v125 builder-rounds parked, median onset r47; 54/110 recent games; camp/heal
teams park us hardest) + the 4b039a9c autopsy lever + research's rung ranking
(QUIET's LOKI-5 basis: 12/15 at n=15, short-map, would not clear today's
bars). Research's two riders adopted verbatim below.

## The arms (both single-diff vs `_v197mapcode`)

* **`bots/_v208idlepeck`** — ladder step 8: a raider with
  `LOKI_IDLE_PECK_RNDS=8` consecutive actionless rounds, adjacent to the
  enemy core, pecks it. Quiet doctrine untouched for active raiders. Idle
  clock resets only on non-idle-peck actions (call-site bookkeeping).
  Tag `IDLEPECK48`.
* **`bots/_v209quiet0`** — `LOKI_QUIET_ON` True→False, one constant: the
  doctrine test (reopens core peck, siphon hit, counterbattery wholesale).
  No tag needed: the contrast is behavioural and read by the detector +
  builderAttack counts in replays.

## Dose (IDLEPECK only; QUIET0 goes straight to screen — its mechanism is
## the removal of a gate, visible in builderAttack counts, not a new path)

Fixture `bots/_probe_sitter` (a sitter reproduces the park: raiders arrive,
ladder empties — no seal targets die, no wounded, no belts to salt). 6 games
× {midgard, frostgate}, seeds 995001-6, kept replays.

1. **VALIDITY (pre-treatment):** control (`_v197mapcode` vs sitter) shows ≥1
   parked raider per research's PINNED detector (`scratchpad/parked_raider.py`
   — their definition governs, not the autopsy agent's) in ≥4 of 6 games per
   map. If the sitter fails to reproduce the park, the dose is FIXTURE-INVALID
   and moves to a camp-shaped fixture, not to a verdict.
2. **DOSE BAR:** in treatment games with a parked-eligible raider (same
   detector, on the pre-peck rounds), `IDLEPECK48` fires in ≥half; **kill
   round strictly falls vs the paired control cell in ≥half of matched
   (map,seed) cells** (the peck arithmetic predicts large drops — a parked
   bot adds 2 dmg/round to a 500 HP core). FALSIFIER: 0 IDLEPECK48 across
   all valid games ⇒ the clock or adjacency test is wrong — instrument
   first, plank second.
3. **OFF-BRANCH (2 games):** `LOKI_IDLE_PECK=False` copy, tag present:
   0 IDLEPECK48, parks still present per detector (exposure denominator).

## Screens (corefill, both queued at commit time)

* `IDLEPECK` vs `_v197mapcode`, n=5400, seed base 230000.
* `QUIET0` vs `_v197mapcode`, n=5400, seed base 231000.
* **D26 replication rules, declared now:** each replicated iff final
  |share−50| ≥ 2.0pp; second shards at seed bases 232000/233000, scored
  alone, pool only on same-side finals.
* **Rider 1 (research): the screens read HARM ONLY.** Self-play incumbent
  does not heal-camp; peck economics (1.0 dmg/Ti vs 4 HP/Ti heal) can lose
  exactly where parks are worst. The VALUE read is a pinned live leg vs the
  camp class (Leviathan/I Stone) with its own prereg — neither screen
  licenses a ship.
* **Rider 2 (research): terminal-idle SEAT RELEASE is orthogonal, not
  competing** — queued as the next build, not raced tonight; the pair prices
  spend-vs-redeploy when both have screens.

## Kill-round bars

Both arms carry kill-round non-regression at their screens (paired-seed
estimator per the UNDERECO decomposition — matched (map,seed) cells, median
per-cell diff ≤ 0 expected; IDLEPECK's mechanism PREDICTS faster kills, so a
kill-round RISE in either arm is a red flag, not a nuance).

---

## AMENDMENT 1 (ADD-only, pre-treatment-data; clock = this commit's git
## author time): FIXTURE-INVALID fallback taken, as pre-registered

Bar 1's control read: **parks 0 in 12/12 sitter games — and the cause is
structural, not behavioural: v125 kills the sitter at r63-90, so a ≥100-round
park cannot exist in the game** (rounds verified on two replays). Per bar 1's
own text the dose moves to a camp-shaped fixture: **`bots/_probe_camper`**
(new: builders heal the core every round +4/1Ti, barrier ring; lie direction
stated — perfect heal uptime overstates the camp, making parks EASIER, which
is against the treatment's interest at bar 2's kill-round clause). Validity
bar unchanged in form: ≥1 park per the pinned detector in ≥4 of 6 control
games per map, now vs the camper; additionally the control game must reach
r300+ (else the fixture still fails to stall and no cell is read). Seeds and
all other bars unchanged.

---

## AMENDMENT 2 (ADD-only; committed with ZERO treatment games run — every
## input below is control/fixture data; clock = this commit's git author time)

**Validity as registered FAILED on both fixtures, both runs disclosed:**
sitter 0/12 (structural — kills r63-90); camper v1 5/12 parks (2/6 midgard,
3/6 frostgate, onsets r25-68, games r110-210); a strengthened camper v2 was
tried and read WORSE (4/12, faster kills — extra builders inflate the
fixture's own cost scale) and is REVERTED to the committed v1. **The pinned
100-round park definition cannot live inside games v125 ends by r220 — that
is a fact about the fixture class, not the plank.** Iterating the fixture
further toward the bar would be fixture-shopping; stopped.

**RE-SCOPED BARS (pre-treatment, control-data-driven):**
* **Bar 2a (local, mechanism):** vs camper v1, seeds unchanged: `IDLEPECK48`
  fires in ≥half of games, and the paired-cell kill round DROPS in ≥half of
  matched cells (unchanged). The step's own precondition (8 actionless
  rounds adjacent to the core) replaces the 100-round corpus definition as
  the local exposure test.
* **Bar 2b (live, the #48-definition read):** moves to the pinned camp-class
  leg research already required — readable on the WIRE with by-construction
  attribution: **v125 produces ZERO builder-attacks-on-core (QUIET_ON since
  v102 origin; autopsy: 0 in all four Jython losses), so ANY builder-core-
  attack event in a treatment leg is treatment-caused.** Same class as
  iteration 4's r<160 eviction attribution.
* Validity 5/12 at the pinned definition is DISCLOSED as the fixture's
  ceiling, not cured.
