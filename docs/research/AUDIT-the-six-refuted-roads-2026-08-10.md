# AUDIT — the six "already refuted" roads in `CLAUDE.md`

**Side lane, 2026-08-10 06:1x CEST.** Opus subagent, read-only, ~60 tool calls of
archaeology. **No verdicts on planks** — reopening a road is a statement about
EVIDENCE, not a recommendation to build. Builds are the builder's.

**Target:** `CLAUDE.md:280-281`, added in `4f4c402` (05:57:36 +0200):
> *"**Already refuted, do not re-derive:** ore poisoning, partial spawn starvation,
> siphon, barrier-form spawn lock, CPU denial, heal-idle staffing."*

Ancestor: `HANDOVER.md:137-139` (`24580a2`, 2026-08-09 16:01), the s24 builder wrap.

---

## THE HEADLINE

**ZERO of the six rest on a leg where we deployed the trick against a live team.**
Evidence bases: 2× our own engine probe, 3× archive/corpus statistics, 1× a
measurement whose result was **never reported**.

**The block sits FIFTEEN LINES BELOW its own bullet 3** (`CLAUDE.md:264-272`):
*"PROTOTYPES GO AT LIVE TEAMS, NOT AT OUR OWN PROBES."* **It states the rule and
violates it inside the same block.** This is the s26 standing note exactly —
*stating a rule in a document does not enforce it in that document* — now in the
always-loaded file.

**Three structural defects in the block, independent of the six verdicts:**
1. **No anchors.** Six class names, no file, no line, no commit, in the doc every
   session loads. Establishing what each rests on cost ~60 tool calls. **A closure
   a lane cannot check is a closure a lane must take on faith.**
2. **It contradicts its own paragraph.** `CLAUDE.md:277-279` lists **spawn-tile
   denial** as *"never balance-changed, therefore still open"*. Two lines later,
   **two of the three forms of spawn-tile denial are closed.** Open and closed in
   the same paragraph.
3. **Two of the six are not Loki roads at all.** Heal-idle staffing is
   heal-uptime; siphon is economy. Both are already retired by the directive's own
   consequences 1 and 2. **Listing them makes the arsenal look six-times-searched
   when only three of the six were ever core-kill questions.**

---

## SCORECARD

| class | evidence base | live-team? | mechanism or price | verdict |
|---|---|---|---|---|
| ore poisoning | archive + engine probe *confirming* the mechanism | **no** | **price** | **REPRICE** + carve-out NEVER TESTED |
| **partial spawn starvation** | archive, **treatment never dosed** | **no** | neither — undosed null | **REOPEN ← strongest** |
| siphon | archive + arithmetic | **no** | price, *already in the new currency* | **STAYS CLOSED** (weak bucket fit) |
| barrier-form spawn lock | engine fact — **friendly bodies only** — then inference | **no** | mechanism, of a *different* proposition | **NEVER TESTED** as a lock |
| CPU denial | archive, **result never reported** | **no** | unresolvable | **REOPEN** |
| heal-idle staffing | archive, us-only, Eir-era, one opponent | **no** | supply | REOPEN on evidence, **off-programme** |

---

## 1. PARTIAL SPAWN STARVATION — **REOPEN. The strongest finding in the audit.**

**`CLAUDE.md` closes a road that its own primary source measures POSITIVE on
`core_kill_share` inside r250, two pages earlier in the same document.**

The refutation (`loki-arsenal-pricing-2026-08-09.md:546-550`) rests on blocking
4-of-12 halving the spawn rate "but the curve is non-monotone above 6". **The doc
names its own confounder** (`:538-542`): *"heavy blocking is mostly a team's OWN
mature infrastructure and correlates with a rich economy, which raises spawn
rate."* **So the table carrying the refutation is a table of teams walling
THEMSELVES in.** The hostile dose Loki would apply has essentially never occurred
(`:181-183`): *"the most bodies any team has ever had on an enemy ring is 6 of 12,
four times in 2,710 sides."*

**And the hostile form is measured POSITIVE in the same document** (`:318-328`,
539k exposed builder-rounds, rounds <250):
> *"One hostile body on the ring **doubles** the 25-round core-death hazard
> (2.24% → 4.77%, CIs disjoint)."*

Prescription already written (`:653-654`): *"Ring-parking: get ONE body there,
EARLY, and keep it."* **Bodies 2–12 have no support; body 1 does.**

**What is correctly closed:** "partial occupancy is a LOCK" — a rules fact, since
the core needs exactly one free ring tile. **What is wrongly closed:** hostile
ring-body denial as a lever.

## 2. BARRIER-FORM SPAWN LOCK — **NEVER TESTED as a lock**

The probe (`bots/_probe_prison`) established one engine fact: `can_build_barrier`
is False on a tile holding a builder bot, **build legality being strictly stricter
than `is_tile_empty`**. **Its own scope label** (`coordination.md:16360-16363`):
*"tested with FRIENDLY bodies only — three maps produced no enemy contact — so the
enemy case is formally untested."*

The leap to the class refutation is an **inference**: they defend for free by
standing a builder on each tile. **That premise was CORRECTED IN-REPO the next
day** (`coordination.md:16416-16434`, s24 `_probe_victim` vs `_probe_jail`, 1,000
rounds):
> *"the parked body itself makes the tile unspawnable. The dilemma is total: ring
> left free → we occupy it → they cannot spawn; ring parked by their own bodies →
> **they** cannot spawn."* — and stepping off costs that builder its action for
> the round, since move and act are mutually exclusive.

**`CLAUDE.md` restates the pre-correction version.** Cost model was one-sided in
exactly the shape the standing "cost the fix, not only the defect" rule forbids:
s22 priced our lock's failure, never the defender's cost of defeating it.
`minimum-cost-blockading-body.md:28-49` prices a 12-tile seal at **~36 Ti**,
arithmetic independently derived twice.

## 3. ORE POISONING — **REPRICE, and `CLAUDE.md` dropped the carve-out**

Mechanism is **engine-CONFIRMED with a control** (`coordination.md:10209-10217`):
`can_build_harvester` True → barrier placed → **False** → we destroy our own
barrier → **True restored**. *"ORE DENIAL IS LEGAL AND IT WORKS. The Q4 restore is
the control."* What was refuted is **throughput against redundancy** (median 5
tiles used, 11 spare, top-1 worth 25%) — a **price**, not a mechanism.

**Both primaries explicitly preserve a carve-out that `CLAUDE.md` silently drops**
(`loki-arsenal-pricing:509-511`): *"this refutes generic and pre-emptive denial. It
does **not** touch 'barrier an ore tile a forward gun already covers', which
remains unmeasured."* Same carve-out in `play-the-players-2026-08-09.md:47-48`.

**And the exchange rate was never netted against the refutation**
(`coordination.md:10222-10225`): clearing our 3 Ti barrier costs them *"15 attacks,
30 Ti and 15 builder-turns… ~10:1 in titanium, ~15:1 in builder-turns."* **Under a
dead-core-by-r250 currency a 15-builder-turn tax is a TEMPO weapon, and nobody
priced it as one.**

## 4. CPU DENIAL — **REOPEN, bordering NEVER TESTED, plus a name collision**

**The only statement of this refutation anywhere in the repo is one clause in a
wrap summary** (`coordination.md:17078-17080`): *"CPU denial as a lever (no
temporal precedence, placebo leads equal the lags)"*. **No number, no denominator,
no n, no population, no effect size, no analysis doc, no committed script, no
output table.** `git log -S "placebo leads"` returns exactly one commit — the wrap.

The measurement DID happen: `tools/cpu_lag_probe.py` exists, and
`scratchpad/cpu_lag.tsv` holds **201,469 rows** — **in a directory the repo's own
wrap calls disposable and untracked.** Under our own standing rule (*numbers carry
subjects*), a bare "refuted, no temporal precedence" **is not a citable
refutation**.

**The strongest REAL evidence argues a ceiling, not impossibility**
(`ammo-and-cpu-2026-08-09.md:99-101`): Ouroboros discards 26,356 unit-turns across
85 games **and beats us anyway**. That doc's own limit: us-only, n=85.

> **NAME COLLISION, AND IT NEEDS MAGNUS.** "CPU denial" is not the same object as
> **CPU-timeout induction**, which `HANDOVER.md:140-142` holds on **NORMS, not
> evidence** — and `HANDOVER.md:477-478`: *"**Magnus owes the organisers one
> question** before anyone builds CPU exhaustion: sibling leagues ban it by name;
> ours is silent."* (Our own earlier ban claim was retracted — the quoted rule
> turned out to be about a 30-minute game clock.) **`CLAUDE.md` merges an
> unreported measurement and an open norms question into the single word
> "refuted".**

## 5. SIPHON — **STAYS CLOSED**, but flag the bucket fit honestly

No rules impossibility and no live-team evidence, so it does not meet the bucket's
stated bar. **But it is the one refutation already computed against
`core_kill_share` @ r250** — it predates the directive and already scored r1000
economy at zero. *"The median opponent banks 1,160 Ti before r250 and the
programme's currency is a dead core, not their bank balance."* **Leave it closed;
do not cite it as impossible.**

## 6. HEAL-IDLE STAFFING — REOPEN on evidence quality, **off-programme; do not spend a leg**

Us-only, one opponent family (CAD loss games, 19,393 siege-rounds over 54 games),
Eir-era — and the metric has since **moved**: our builder idle rate went 11.4–21.6%
across thirteen versions to **25.78% on v102** (+12.9pp). So the evidence would not
survive its own audit. **But heal-uptime is retired by the directive.** Reopening
costs nothing and gains nothing. **Its presence on the list is the real defect: it
inflates the appearance of a searched arsenal.**

---

## THE DISTORTIONS, VERIFIED RATHER THAN ASSUMED

- **Probe short-circuit:** `grep -rn "best_core or best_any" bots/*/main.py`
  returns exactly five — `band_probe`, `cad_probe`, `flotte_probe`, `kladde_probe`,
  `orizon_probe`. **None of the six refutations rests on an arena battery**, so
  this distortion does not bite them directly. It is still why bullet 3 exists,
  and it makes the block's silence on live-team evidence more glaring.
- **Era:** 1,580 of 1,710 attributed ladder games are v101-or-earlier — **92.4%
  Eir / 7.6% v102**. Bites classes 5 and 6 directly and classes 1–3's US controls.

---

## THE UNCLOSED ROAD NOBODY LISTED — **harvester round-robin is TEAM-BLIND**

`game-model.md:331-338`, verified on our engine: **an enemy conveyor adjacent to
your harvester is a full-rank acceptor.** An unwired harvester beside an enemy belt
gives **~half its output away**, and wiring your own belt only *halves* the drain.
Measured **49/49** sole-enemy-acceptor; strict 50/50 with one acceptor per team
over 800 rounds. **This is a live theft mechanic, distinct from the refuted siphon,
and no doc closes it.** Related engine fact from the arsenal doc: **the engine
credits titanium to whoever owns the DESTINATION core**, and **41.03% of our sides
already push ≥1 hop onto the enemy network by accident.**

## OTHER VERIFIED-AND-OPEN ITEMS FOUND DURING THE SWEEP

- **KIDNAP-ADJACENT PLACEMENT — the arsenal doc's own "the one to build":**
  **20.65%** of enemy-builder-rounds <r250 have a buildable launcher site, 16.03%
  persist a round, **0 of 1,355 games have none** — and we build 0.64
  launchers/game, **none forward**.
- **Launcher ranges measured for the first time**, 31,569 real throws, zero
  exceptions: pickup Chebyshev-1 (d²≤2), throw reaches d²≤26.
- **Seat-A turn-order advantage on contested-ore maps: 62 vs 27 harvesters (2.3×)**
  over 5 instrumented matches on archipelago.
- **Cheapest unprobed item in the library**, by its own file: does an enemy body
  block an enemy gunner? *"Assumed by symmetry, never shown."*
- **A correction that never propagated:** `sentinel-file-stacking.md` still prints
  "2.68 healers" as *the MEASURED field detail* when `INDEX.md` records it as **our
  own** number relabelled as the field's. The correction lives in INDEX.md and was
  never patched into the tactic file.

---

## RECOMMENDATIONS (evidence statements; builds are the builder's)

1. **Ring-body denial deserves the first live-unrated trick leg.** It is the only
   closed road whose own primary measures it positive on the primary currency
   inside the window, with the prescription already written: **one body, early,
   keep it.** It is also unambiguously *offensive* — denying spawns while raising
   their core-death hazard — so it does not brush `PLAY_DEFENCE: never`.
2. **Re-anchor the `CLAUDE.md` block or delete it.** Minimum fix: every item
   carries `file:line` and the word MECHANISM or PRICE. As written it closes six
   roads on no live evidence, contradicts its own paragraph, and drops a carve-out
   its sources preserved.
3. **Bank the CPU-lag result or strike the claim.** 201,469 rows sit in a
   directory the repo calls disposable, as the only trace of a refutation stated
   with no denominator. **And CPU-timeout induction is a question Magnus owes the
   organisers — a norms decision, not a research finding.**

---

## ADDENDUM 2026-08-10 10:5x — CORRECTION to the ring-body verdict (this audit's own #1 recommendation)

This audit's #1 recommendation was: *"ring-body denial deserves the first
live-unrated trick leg — the one reopened road whose own primary measures it
positive on the currency (2.24%→4.77% at j=1)."* **Building it corrected that.**
Per LOKI-16's prereg (2755aca), **our incumbent ALREADY places >1 body on the
enemy ring — "both arms already exceed the prescription's ONE body."** So the
one-body lever the observational evidence measured is **not an untested reopened
road; it is already implemented.** The 2.24%→4.77% finding describes something
our bot already does, not a new thing to add.

**Reclassify:** ring-body (one body) → **ALREADY-IMPLEMENTED**, not REOPEN. The
open margin is **RETENTION** (hold a body vs trade it for a barrier), which is a
different mechanism and is what LOKI-16 (E-27.6) actually tests. **Method note:
"reopen this road" was itself an archive-sourced claim (D12) — and the way it got
checked was by building it and finding the bot already did it, which is the
live-evidence standard working: the prescription met reality and reality already
had it.** The other five roads' verdicts stand; this is the one where
construction, not analysis, delivered the correction.
