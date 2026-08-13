# SIX-ROADS STATUS — moved verbatim from CLAUDE.md 2026-08-13

**TAGS: incumbent v123 `bots/_v187saltidle_f` at move time. Moved by the meta
lane (boot-load audit cut 5, Magnus 'apply your fixes'): volatile per-road
status does not belong in the auto-loaded file. Update THIS file when a road
moves; CLAUDE.md carries only the pointer.**

**THE SIX ROADS BELOW ARE A QUEUE ORDER, PENDING LIVE TESTS — NOT A STATUS.**
Re-anchored 2026-08-10 after an audit found **not one of the six rested on a leg
where we deployed the trick against a live team**; under the standard above,
REOPEN / REPRICE / CLOSED are all still archive verdicts and none of them has
retired or revived anything on its own authority. Audited
2026-08-10 (`docs/research/AUDIT-the-six-refuted-roads-2026-08-10.md`): **not one
of the six rested on a leg where we deployed the trick against a live team** —
the bases are our own engine probes, archive statistics, and in one case a
measurement whose result was never reported. The block as first written also
contradicted itself, listing spawn-tile denial as open two lines above closing
two of its three forms. **Every entry now says WHAT was refuted (mechanism or
price) and on what basis:**

| road | status |
|---|---|
| **siphon** | **CLOSED** — off-currency by construction. Stays closed. |
| **partial spawn starvation** | **ALREADY IMPLEMENTED, not a road.** Discovered 2026-08-10 by trying to BUILD it: our incumbent already puts a body on the enemy 12-tile ring in **68.8% of rounds** (**⚠ s28: THIS SPECIFIC NUMBER IS UNREPRODUCIBLE — it came from a 480-game LOCAL battery against our own `*_probe` bots and that battery's script is not in `tools/` or `tools/corpus/`. The LIVE figure over 165 games is 0.586 game-mean / 0.636 round-weighted. The reclassification below still stands on the live number; the 68.8% does not, and the two must never share a sentence without this caveat**), arriving ~r22, and both arms of the test already exceed the prescription's ONE body (~2.3 simultaneous). **The open margin is RETENTION, not presence** — `_raid_station` walks the body OFF a corner exactly when that corner becomes pure body-denial. That is LOKI-16. Original entry read: **REOPEN.** What was refuted is *"partial occupancy is a LOCK"* — a rules fact (the core needs exactly one free tile). The hostile treatment was **never dosed**: max ever seen on an *enemy* ring is 6 of 12, four times in 2,710 sides, and the source table is teams walling **themselves** in. **⛔ CORRECTED s31, 2026-08-11 (Magnus authorised). This row previously asserted that a hostile body on the ring "DOUBLES the 25-round core-death hazard, 2.24%→4.77%" — a summary that had lost its own source's hedges.** **The ~2× figure is an ASSOCIATION and is MARKER-DOMINANT, not causal: a core's OWN healers on its OWN ring, which cannot damage it, reproduce ×2.02 of it.** ⇒ **Do not size a plank on it; do not pre-register LOKI-16 against core-death hazard.** **Full derivation, all five controls, the dose and duration curves and every scope restriction live in `docs/coordination.md:16649`** — the original, which itself said *"treat 2.1× as an UPPER BOUND, not an effect size"* — **and `docs/research/RING-HAZARD-VERIFICATION-2026-08-11.md`** (s31, 19,178 replays, 16.0M core-rounds). **This entry is a POINTER, not a summary, per D22: a promoted claim carries its hedges or it carries a pointer, and if the hedges do not fit, it is a pointer.** **⭐ RULES-LEVEL AND UNAFFECTED — the bar to use if this road is ever run: 0 spawns in 2,405,604 body ring-tile-rounds.** **The road stays at the BOTTOM of the queue, not off it (D12):** the `US_ATTACK` cell alone flips in the causal direction, us-only and observational, and **only a live leg randomising the tile — raider held on the ring vs stepped one tile off — separates the stories.** |
| **barrier-form spawn lock** | **NEVER TESTED as a lock.** The s22 probe was FRIENDLY bodies only; three maps produced no enemy contact. Its "they defend for free" inference was overturned in-repo by our own s24 probe (a parked body makes the tile unspawnable for its owner too). |
| **CPU denial** | **REOPEN on evidence** — the only statement of the refutation in the repo is one clause in a wrap, with no number, denominator, n, or script output; the 201,469 rows sit in an untracked scratch dir. **Separately, CPU-timeout *induction* is HELD ON NORMS, not evidence** — Magnus owes the organisers one question first. Do not merge the two. |
| **ore poisoning** | **REPRICE.** The mechanism is engine-confirmed with a control; what died was a PRICE (throughput vs redundancy) computed under the retired currency. Clearing a 3 Ti barrier costs them ~30 Ti and 15 builder-turns — a tempo weapon nobody priced as one. A carve-out both primaries preserved was dropped here: *"barrier an ore tile a forward gun already covers"* remains unmeasured. |
| **heal-idle staffing** | **REOPENED 2026-08-11.** Was *"off-programme under `PLAY_DEFENCE: never`"* — **that field no longer says that** (see the defence clause above). Now admissible IF it clears `DEFENCE_ADMISSION_BAR: kill_round_non_regression`. ⚠ **And grep the incumbent FIRST: we already ship `_heal_core`, `_heal_adjacent`, `heal_seats` and a `SLOT_UNDER` under-attack latch — the adjacent plank died 2026-08-11 to two minutes of grep.** |

**AND A ROAD CAN BE "UNTESTED" ONLY BECAUSE NOBODY READ OUR OWN CODE.** The
spawn-starvation entry above was audited from the evidence, nominated as an
untested lever, and turned out to be **something we already do** — found only by
going to build it. **An audit of the literature is not an audit of the codebase,
and this queue is a list of things to CHANGE, not things to KNOW.** Before
pre-registering any plank, grep the incumbent for the behaviour: the cheapest
possible null is a leg that tests a feature we already shipped.

**A price refutation computed under the retired currency is void even if the
fixture was clean.** So is any survival/screening refutation resolved on
`orizon`/`cad` — see the fixture warning in point 3 above.
