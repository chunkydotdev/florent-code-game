# ⭐ GENERATOR BRIEF — THE KNOB-TURN BUDGET, AND THE NON-KNOB CANDIDATES

**Research arm, s31, 2026-08-11. Written on Magnus's direct instruction widening
this lane to generation:** *"you who have all the research might be the better
suited to generate ideas that are NOT knob-turns and tweaks, however some
knob-turns might be good, but that needs to be tested, although a reasonable
amount, set a limit for the amount of versions a knob-turn can be tested."*

---

# PART 1 — THE KNOB-TURN LIMIT, DERIVED RATHER THAN PICKED

## The arithmetic it comes from

**Budget** (side lane, `9209e3e`): v104 went 646 → 749 rated matches in 29.5 h ≈
**84/day ⇒ ~420 rated matches left in the game.** Convergence takes ~100 matches
⇒ **~4 ship-and-converge cycles remain.**
**Conversion:** near 50%, **+1pp true game share ≈ +7 Elo of equilibrium rating.**

**What a self-play screen can actually resolve** (two arms, game share,
`SE(diff) = √(2·0.25/n)`, MDE at 80% power two-sided = 2.8·SE):

| n per arm | games | wall clock¹ | MDE | in Elo |
|---:|---:|---:|---:|---:|
| 1,024 | 2,048 | ~12 min | **6.2 pp** | ~+43 |
| **4,096** | **8,192** | **~50 min** | **3.1 pp** | **~+22** |
| 16,384 | 32,768 | ~3.3 h | 1.5 pp | ~+11 |

¹ measured: the s30 8×1024 battery ran 8,192 games in ~50 min on 8 parallel shards.

**⇒ A knob-turn worth +2.3pp (~+15 Elo) needs ~7,400 games/arm to see at 80% power.
Anything smaller is invisible at every n we can afford this week.** That is the
same wall the screens hit all day: **big effects resolve cheaply, small ones cannot
be seen at all.**

## THE LIMIT

> **ONE screen per knob, at n = 4,096/arm.**
> **A knob that lands inside the band is DEAD. It does not get a second version.**
>
> **ONE exception, pre-registered or it does not count: if a DOSE CHECK shows the
> mechanism did not fire, the knob gets exactly ONE re-test at corrected dose.**
>
> ⇒ **HARD LIMIT: 2 versions per knob** (screen + at most one dose-corrected retest).
> ⇒ **PORTFOLIO LIMIT: 6 knob-turn versions total for the remainder of the game**
> — about 5 hours of compute, leaving the bulk of the clock for non-knob work.

**Why "inside the band" ends it rather than earning a retest.** At n=4,096 the band
already excludes everything worth less than ~+22 Elo. Re-screening a knob that
landed inside it is fishing, and it is D61 run backwards: **D61's lesson was that
"inside the band" is NO INFORMATION and returns a plank to the pool — not that it
earns more games.** The pool is where it goes; the queue is not where it goes.

**Why the dose exception is not a loophole.** It separates *"the knob does not
help"* from *"the knob was never turned"*, which is a different claim. **s30 D64 is
the case: the `K_HEAL_RATE_PCT` 5→1 arm was the joint top performer and the dose
check found it healing 461.5/game against the control's 132.8 — 3.5× MORE.** Without
a dose check that ships a bot doing the opposite of what the plank claims.

**Why 6 total.** **s30 spent 19 arm trees on knob-turns and shipped zero.** Even a
knob that *clears* at n=4,096 is worth ~+22 Elo against LOKI-13's ~+120. With ~4
ship-and-converge cycles left, **spending more than one on knobs is bad expected
value**, and 6 versions ≈ one cycle's worth of compute.

---

# PART 2 — NON-KNOB CANDIDATES

**A knob-turn changes a constant. These change what the bot DOES.** Ranked by
(measured effect × confidence it survives contact × fit to a five-day clock).
**Every effect size is labelled by its evidential status. I am naming mechanisms,
not writing diffs.**

## C1 — RING RETENTION: hold the enemy spawn ring instead of walking off it

**Not a knob:** `_raid_station` walks the body **off** a corner exactly when that
corner becomes pure body-denial. The change is to the behaviour, not to a number.

**Claimed effect — ⚠ INHERITED, UNDER VERIFICATION AS OF THIS WRITING:** one
hostile body on the ring **doubles the 25-round core-death hazard, 2.24% → 4.77%,
CIs disjoint.** *(`CLAUDE.md`, from a prior session's primary, never independently
re-derived. I have an agent re-deriving it now with a dose-response curve, a
duration curve, third-party separation, and — the part that decides it — a
**marker-vs-cause** analysis with a lead-lag placebo. **I will not promote this
candidate on the inherited number.**)*

**Dose is guaranteed:** we already hold a body on the enemy 12-tile ring in
**59–64% of rounds**, arriving ~r22. **The open margin is RETENTION, not presence.**

**The risk, stated first:** a body on the enemy ring is a plausible **marker** of a
winning attack rather than a cause. If the verification says marker, **this
candidate dies and I will say so.**

## C2 — LAUNCHER DELIVERY: arrive without traversing

**Not a knob:** a new use of a unit we already build.

**Grounded in today's measurement:** forward hazard is a **flat ~3.5× multiplier in
every round band** (ours 2.1–3.8 per 1k forward builder-rounds, theirs 0.70–0.93),
so **fewer traverse rounds means proportionally fewer deaths.**

**⭐ AND IT IS THE ONE FORM THAT ESCAPES THE LOKI-25 TRAP.** LOKI-25 died because it
moved numerator and denominator together — deaths −24%, forward presence −23%,
ratio −2.3%. **Launcher delivery cuts the rounds spent getting there while
PRESERVING the arrival**, so it cuts the numerator without cutting the denominator.
That is the distinguishing property and it is why this is not just "go forward
less".

**Engine facts (read off the binary, `docs/research/engine-source-…`):** pickup
d² ≤ 2, throw 1 ≤ d² ≤ 26 measured from the launcher, **0 ammo**, cooldown += 1,
position-only mutation, **no team check and no vision guard**.

**⛔ THE ASSUMPTION THAT COULD KILL IT, NAMED UP FRONT: the traverse-vs-destination
split of the hazard is ASSUMED, NOT MEASURED.** If our builders die *at* the
forward site rather than *on the way*, delivery buys nothing. **`events.tsv` carries
death round and position and `builder-death-attribution` splits shooter type — this
is a ~1 hour cut and it should precede any build.**

## C3 — CRASH INDUCTION AT SCALE: the highest ceiling on the board, and it has sat at the bottom of the queue for weeks

**Not a knob: it is a weapon.** Kidnap an enemy builder with a launcher (no team
check, no vision guard) and throw it to a legal **map-border** tile, where that
bot's own code queries an off-map neighbour, raises, and **the engine permanently
destroys that unit for the rest of the match.** We spend 0 ammo and one throw.

**The field-level fact that makes this a scale weapon, not a trick:**
`tools/crash_census.py` measures **2,451 unexplained unit removals by opponents
across 1,855 of our games, against 0 by us.** **The field crashes constantly on its
own, unaided.** We patched our own instance of exactly this bug in `eco.py`; most
teams have not.

**Status: APPROVED CLASS — Magnus asked the organisers and crash-induction is
approved. No norms question is owed. It is BUILT (`bots/_v131loki14`).**

**⛔ WHY IT HAS NEVER BEEN RESOLVED, and it is an instrument failure rather than a
negative result:** the LOKI-14 leg planned to read its own arm tag out of the live
replay, and **`print()` is stripped from platform-downloaded replays — 30,664
`BotOutput` events, stdout empty in 30,664 of 30,664.** The leg decoded **314
kidnaps** off the wire and the mechanism fired; **the method as written was not
executable and the weapon was never scored on the currency.**

**⇒ THIS IS THE ONE I WOULD SPEND A CYCLE ON.** Highest ceiling, approved, already
built, dose already demonstrated at 314 throws, and **its only failure to date was
a read-out that no longer has to be attempted that way** — read arms from
engine-side facts (throw destinations, entity removals), never from our own stdout.

## C4 — ORE-BARRIER CARVE-OUT: barrier an ore tile a forward gun already covers

**Not a knob.** Both primaries preserved this carve-out and **it has never been
measured.** Clearing a 3 Ti barrier costs them **~30 Ti and 15 builder-turns** — a
tempo weapon nobody priced as one, and the price refutation that killed the parent
idea was computed under the **retired** currency, so it is void.

**Cheap, but lower ceiling than C1–C3.** Queue behind them.

## C5 — ENEMY-HARVESTER TAP — **I AM LISTING THIS TO RULE IT OUT, NOT TO PROPOSE IT**

Engine-verified and genuinely open: **harvester round-robin is team-blind**, an
enemy conveyor adjacent to a harvester is a **full-rank acceptor** (measured 49/49),
and titanium is credited to whoever owns the **destination** core. So a conveyor
built beside their harvester, routed home, takes ~half its output.

**⛔ It is off-currency. `R1000_IS_DEFEAT: yes` makes `titanium_collected`
instrumental only, and its real value — starving their build — is slow.** On a
five-day clock with a kill-round focus, **this is not worth a cycle and I am saying
so rather than padding the list.**

---

# WHAT I AM NOT DOING

* **Not writing diffs.** Mechanisms and constants named; the intervention is the
  builder's.
* **Not promoting C1 until its number is re-derived**, including the confound that
  could kill it.
* **Not proposing the `econ.tsv` header fix, the three-way state split, or the
  forward-efficiency 880-game run** — all sound, all wrong for this clock.
