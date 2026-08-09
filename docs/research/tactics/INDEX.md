# Tactics library — ideas mined from comparable games, for the builder

**Standing mandate (Magnus, 2026-08-09):** the research arm is permanently
data-hungry and continuously mines strategies, tactics and ideas from comparable
games, converting them into things the builder can use. Boot instructions live in
`.claude/commands/research.md`. **Subagents are pre-authorised — no per-session
permission needed.**

This index exists so successive sessions **do not re-research the same ground.**
Update it in the same commit as any findings.

## ✅ QUOTE AUDIT — 2026-08-09, and the method matters as much as the result

**Why it happened:** one sweep agent disclosed that an earlier draft of its own report
contained **fabricated quotes attributed to eight named teams**. That draft was never
delivered and nothing from it was published — but **every sweep in this library was
produced by agents of the same class**, so the library had to be checked rather than
trusted.

**Result: 16 of 16 load-bearing quotes verified VERBATIM against primary sources.**

| sweep | claim checked | verdict |
|---|---|---|
| 2 | Kragle *"the counter to static defense is to disengage…"* | ✅ verbatim |
| 2 | 5 Musketeers tiebreak passage (full, ~90 words) | ✅ verbatim |
| 3 | High Ground *"every top team… now had a drone harass"* | ✅ verbatim |
| 3 | High Ground *"pick up and drown their rushing miner"* | ✅ verbatim |
| 3 | Smite *"10:1 or more… to guarantee a successful attack"* | ✅ verbatim |
| 3 | Smite *"as soon as a drone sees the gun, its dead"* | ✅ verbatim |
| 5 | Gone Fishin' *"140 bits: a total of 10 enemies…"* | ✅ verbatim |
| 6 | Gone Fishin' *"wins about 2/3 of the game…"* | ✅ verbatim |
| 6 | Tavares single-choice **28.1%** / reply-last **60.9%** | ✅ both present |
| 7 | SPAARK disintegrate-after-**30 turns**; **sqrt(35)** build condition | ✅ verbatim |
| 8 | Agade tower/mine formulas + *"4.25 queen HP… way too high"* | ✅ verbatim |
| 8 | robostac *"hitpoints / 10 … encourage aggressive tower placement"* | ✅ verbatim |
| 8 | ryandy Lux `ice_conflict_bonus` **500** above `ice1_bonus` **300** | ✅ verbatim |

### THE METHOD — and the trap that nearly produced two false retractions

**Do NOT ask a model whether a string is present.** My first check of the SPAARK
quote was a `WebFetch` summarisation of the PDF; it reported that **neither phrase
appears.** Both appear verbatim.

**And do not grep raw `pdftotext` output either.** My first pass over four Battlecode
PDFs returned **zero hits on three quotes that are all genuine** — because PDF
extraction breaks sentences across lines.

```bash
curl -sL "<url>" -o x.pdf && pdftotext x.pdf x.txt
tr -s ' \n\t\f\r' ' ' < x.txt > x.flat     # <-- THE STEP THAT MATTERS
grep -o "phrase.\{0,120\}" x.flat
```

**METHOD BUG FOUND AND FIXED IN SWEEP 14 (s25):** the command as previously written
here flattened only space/newline/tab and **left `\f` (form feed) in place**.
`pdftotext` emits `\f` at every page break, so **any quote straddling a page boundary
still failed the literal grep** — the exact false negative this procedure exists to
prevent, hiding inside the fix for it. The `\f\r` above is the correction. **A guard
that has a blind spot is more dangerous than no guard**, because a "not found" from it
reads as a verified absence.

**Two false negatives in one audit, in opposite tools.** A quote check that returns
"not found" is not a result until whitespace has been normalised and a second method
has agreed.

### THE RULE, promoted from observation on the THIRD sighting (s24, builder's suggestion)

**A plausible sentence near the right passage survives everything except a verbatim
grep.** Three independent cases now, and the failure is *not* "models invent sources":

| # | case | why it looked fine |
| --- | --- | --- |
| 1 | s23 — an agent disclosed fabricated quotes attributed to eight named teams in an undelivered draft | right league, right era, plausible teams |
| 2 | s24 sweep 9 — a `WebFetch` summariser produced a **Screeps tower falloff formula absent from the raw page** | right document, right topic, formula-shaped |
| 3 | s24 sweep 10 — a drafted *"SCVs are used to repair tanks and draw fire"* actually reads *"**They** are also used to repair tanks and draw fire"*, where **"They" refers to Supply Depots** in the preceding sentence | **right document, right topic, adjacent sentence, WRONG SUBJECT** |

**Case 3 is the instructive one because nothing about it looks wrong.** The source
says something very like it, on that page, about that mechanic. Only the literal
string check catches it.

**THE SPECIFIC FAILURE IS PARAPHRASE-INTO-UNMARKED-TEXT**, not invention — a near-miss
gets smoothed into quotation marks. **THE FIX IS MECHANICAL AND NON-NEGOTIABLE:**
extract → **flatten whitespace** → grep the **literal** string. Never ask a model
whether a string is present; never grep raw `pdftotext` output. If it does not verify
**verbatim**, cut it or label it an explicit paraphrase — those are the only two
outcomes.

### THE SECOND RULE — verbatim is necessary and NOT sufficient (s24, and it defeated the first rule)

**A correctly-copied sentence can still be pointed at the wrong object, and the quote
audit cannot see that.**

Sweep 13 found that `cpu-timeout-induction.md`'s headline — *"deliberately inducing an
opponent's compute overrun is banned by name in at least two comparable leagues"* — is
**not supported by the sources it cites.** The BASIL quote is genuine and **passed the
16/16 quote audit**. Read in full context, *"this timeout"* is the **30-minute real-time
GAME limit** and the banned act is stalling *"to avoid losing"* — nothing to do with an
opponent's per-turn compute budget. **The string was right; the referent was invented by
the reader.**

**So the checklist grows by one step, and it is a different step:**

| check | catches | misses |
| --- | --- | --- |
| extract → flatten → grep the literal | fabrication, paraphrase-as-quote, wrong subject | **a true quote about a different thing** |
| **quote the sentences AROUND it and state the referent explicitly** | scope errors | — |

**Rule: when a quote carries a demonstrative — "this timeout", "that rule", "such bots" —
the referent must be quoted too, or the claim is not sourced.** This is the same family
as the project's standing failure — *the arithmetic was right, what it was taken to MEAN
was wrong* — arriving in the citation layer instead of the statistics layer.

**And the standing caution it does NOT relax:** a tactic no other league bans is **not
thereby permitted here**. Our organisers' rules govern. `cpu-timeout-induction` remains
**HELD pending an organiser ruling** — the correction narrows a claim, it does not open a
road.

**Convention on minor edits:** sweeps silently correct source typos when quoting
(Smite's *"suppourt"*, robostac's *"priortised"*, Agade's *"to more"*). That is
acceptable and now stated; **anything beyond a typo must be marked as a paraphrase.**

## How a sweep runs

1. Pick the next **unswept** or **stale** row from the wheel below.
2. Launch a background subagent (or several narrow ones) with an explicit brief:
   the ruleset summary, the question, and the demand for sources.
3. When it returns, write one file per usable tactic into this directory, mark
   the wheel row, and **relay to the builder** — subagent results die with the
   session.

Sweeps run **at boot**, **whenever the queue drains** (watch state is a sweep,
never an idle), and **after any measured surprise** that contradicts doctrine.

## File format

```markdown
---
tactic: <short name>
source: <URL>
origin: <competition / year / team, or "RTS theory">
evidence: documented | anecdotal | inference
transfers: yes | partial | no
---
WHAT IT IS — two or three sentences.
WHY IT MIGHT TRANSFER — against OUR ruleset specifically.
WHAT WOULD KILL IT — the rule or measurement that makes it inapplicable here.
BUILDER HOOK — the smallest thing that would test it, or "none yet".
```

**Rules.** Never invent a tactic or attribute one to a team that did not use it.
An untransferable tactic recorded as `transfers: no` **is a useful result** and
should be filed, not discarded — it stops the next session chasing it. A
plausible-sounding tactic with no source is pollution; mark it
`evidence: inference` and say whose inference.

## Our ruleset, for briefing subagents

Two teams, symmetric grid 8x8..30x30. Core 500 HP / 2x2. Builder bots (40 HP, the
only mobile unit; build/attack/heal/destroy on an orthogonally adjacent tile).
Turrets: gunner r²=13 dmg 7 / 4 ammo; sentinel r²=32 dmg 18, **ignores obstacles**
/ 10 ammo; launcher r²=26, throws a builder bot **from either team** to a passable
tile. One resource (titanium), moved physically by conveyors/splitters/harvesters
into the core; **core converts titanium→ammo 1:1, no passive ammo income**.
Build costs **scale up** per category as you build more. 16-slot integer team
comms store, writes visible next round. 1000 rounds; win by core kill, else
tiebreak on titanium delivered → harvesters alive → titanium stored. **10 ms CPU
per unit per turn; exceeding it silently discards that unit's turn.** An uncaught
exception permanently destroys that unit for the match.

## The wheel

| # | topic | status | swept | files |
|---|---|---|---|---|
| 1 | Battlecode postmortems: late-game conversion, breaking stalemates | **SWEPT** — 23 official PDFs 2019-2026 read in full. **Produced the heal-arithmetic finding.** | 2026-08-09 | [heal-arithmetic](../heal-arithmetic-2026-08-09.md), [sweep 1](2026-08-09-sweep-1.md) |
| 2 | Cross-league trickster/asymmetric play (steering deterministic opponents, denial, baiting, body-blocking, tiebreak manipulation) | **SWEPT** | 2026-08-09 | [sweep 1](2026-08-09-sweep-1.md), [spawn-smothering](spawn-smothering.md), [ore-tile-denial](ore-tile-denial.md), [ammo-drain-baiting](ammo-drain-baiting.md), [destroy-rebuild](destroy-rebuild-converter.md) |
| 3 | Engine/rule-edge exploits + post-hoc rule patches (best index of what worked) | **SWEPT** (8 Battlecode postmortem PDFs read in full) | 2026-08-09 | [sweep 1](2026-08-09-sweep-1.md) §3, §6 |
| 4 | CPU/time-limit exploitation — inducing opponent timeouts | **SWEPT.** Effect is real & tournament-deciding (StarCraft natural experiment); deliberate induction **BANNED BY NAME in BASIL and SC2 AI Arena** — held pending an organiser ruling | 2026-08-09 | [cpu-timeout-induction](cpu-timeout-induction.md) |
| 5 | Turret/tower placement doctrine and advancing a firing line | **SWEPT**, then **RE-AIMED** at the measured turret-survival flip. Its leading hypothesis (survival = avoidance) is **falsified by our own data**; its subsidiary findings are the most buildable material any sweep has produced — **the ablative barrier screen is ~8× HP/Ti and is SENTINEL-ONLY** | 2026-08-09 | [lanchester-commit-gate](lanchester-commit-gate.md), [sweep 1](2026-08-09-sweep-1.md), [sweep 7](2026-08-09-sweep-7.md) |
| 6 | Cost-inflation attacks (making the opponent's buildings dearer) | **SWEPT** — and inverted: killing an enemy builder REFUNDS their scale; imprison instead | 2026-08-09 | [exchange-rates](../exchange-rates-2026-08-09.md) §6 |
| 7 | Limited-bandwidth team coordination (our 16 ints) | **SWEPT** — 15 BC postmortems 2019-2026. **Produced a probe that found a latent bug**: the read-increment-write ticket idiom collapses silently under our buffered store, and `SLOT_ROLE_N` is safe only because the core spawns ≤1 builder/turn | 2026-08-09 | [sweep 5](2026-08-09-sweep-5.md), [store semantics](../store-semantics-2026-08-09.md) |
| 8 | Economy: harvest saturation, expansion timing, when to stop expanding | **SWEPT** — and it turned into a negative: **cost scaling never binds on harvesters** (break-even beyond any map's ore supply under both readings); it binds on the **+20% categories**. The corpus hooks then showed **the economy is not our constraint at all** | 2026-08-09 | [sweep 4](2026-08-09-sweep-4.md), [middle-game hazard](../middle-game-hazard-and-economy-2026-08-09.md) |
| 9 | Opening theory and build-order steering in symmetric-map games | **SWEPT** — **our constant is DEFENSIBLE** (fixed openings are the league norm; the anti-constant result needs cross-game memory the engine forbids). **The one qualification — an opening unconditional on MAP GEOMETRY — is a documented failure mode, and our own width gradient is it.** | 2026-08-09 | [sweep 6](2026-08-09-sweep-6.md) |
| 10 | Endgame/tiebreak play when the win condition is a score, not a kill | **SWEPT** (BC 2019 do-nothing, BC 2022 one-gold, Halite endgame flag, Spring'21 score+banked/3) | 2026-08-09 | [sweep 1](2026-08-09-sweep-1.md) §4 |
| 11 | Anti-rush and defensive-line theory — **re-aimed at "how does anyone break a 2.2:1 defensive edge?"** | **SWEPT** — 8 BC postmortem PDFs read in full + Screeps/Terminal/RTS theory. **Answer: mostly you don't, you win on economy; every league converged there independently.** | 2026-08-09 | [sweep 2](2026-08-09-sweep-2.md), [sentinel-file](sentinel-file-stacking.md) |
| 12 | Unit-displacement mechanics elsewhere (our launcher throws EITHER team's bots) | **SWEPT — and it INVERTS our current use.** BC2020's Delivery Drone has our Launcher's exact verb signature; that field converged on grabbing the **enemy's** unit defensively, never on ferrying their own forward | 2026-08-09 | [sweep 3](2026-08-09-sweep-3.md), [defensive-interception](launcher-defensive-interception.md), [displace-dont-kill](displace-dont-kill.md), [throw-into-prebuilt-cell](throw-into-prebuilt-cell.md) |

| **13** | **DIRTY TRICKS — denial/smothering, imprisonment, resource poisoning, friendly-fire manipulation, unit theft** (the PROGRAMME `loki` re-aim: enemy core dead inside r250) | **SWEPT** (s24). **12 files, 75 quoted strings, 0 unverified.** Produced the **library correction** above. | 2026-08-09 | [blind-their-gun-with-their-own-body](blind-their-gun-with-their-own-body.md), [ratnapping-ignores-hp](ratnapping-ignores-hp.md), [press-them-onto-their-own-spawn](press-them-onto-their-own-spawn.md), [import-a-hazard-into-their-base](import-a-hazard-into-their-base.md), [score-the-throw-destination](score-the-throw-destination.md), [pin-against-terrain](pin-against-terrain.md), [minimum-cost-blockading-body](minimum-cost-blockading-body.md), [the-blockade-blanks-your-own-guns](the-blockade-blanks-your-own-guns.md), [comms-jamming-and-spoofing](comms-jamming-and-spoofing.md), [body-blocking-was-patched-out-elsewhere](body-blocking-was-patched-out-elsewhere.md), [manner-pylon-and-what-the-rules-permit](manner-pylon-and-what-the-rules-permit.md), [no-league-bans-inducing-an-opponent-timeout](no-league-bans-inducing-an-opponent-timeout.md) |

| **14** | **RE-AIM of topics 1 + 11 at the PROGRAMME's own tension** — `KILL_WINDOW_RND: 250` demands the one thing every prior sweep concluded you mostly cannot do. *What CONVERTED a deadline attack into a dead base elsewhere, and what KILLED the ones that failed?* | **SWEPT** (s25). 16 files + summary. **97 strings verified verbatim, 4 near-misses corrected, 2 claims CUT unverified.** **Corrects sweep 2's clock claim** (see standing context) and **found a bug in this library's own quote-verification command** (see method block above). | 2026-08-09 | [sweep 14](2026-08-09-sweep-14.md), [rush-as-fallback-when-the-opening-is-denied](rush-as-fallback-when-the-opening-is-denied.md), [the-all-in-is-a-counter-strategy-not-a-strategy](the-all-in-is-a-counter-strategy-not-a-strategy.md), [the-rush-cost-budget-gate](the-rush-cost-budget-gate.md), [one-cheap-interceptor-decides-the-matchup](one-cheap-interceptor-decides-the-matchup.md), [reactive-spawn-is-the-sufficient-anti-rush](reactive-spawn-is-the-sufficient-anti-rush.md), [the-rush-that-cannot-transition](the-rush-that-cannot-transition.md), [the-attack-that-arrives-too-late-or-at-nothing](the-attack-that-arrives-too-late-or-at-nothing.md), [spawn-the-attack-at-the-target-not-a-march](spawn-the-attack-at-the-target-not-a-march.md), [map-size-decides-whether-the-rush-is-legal](map-size-decides-whether-the-rush-is-legal.md), [late-rush-beats-the-anti-rush-reflex](late-rush-beats-the-anti-rush-reflex.md), [no-lose-engagement-geometry](no-lose-engagement-geometry.md), [the-defenders-reserve-and-what-defeats-it](the-defenders-reserve-and-what-defeats-it.md), [retreat-and-return-under-the-counter-unit](retreat-and-return-under-the-counter-unit.md), [wall-off-the-forward-plant-and-leave-a-rebuild-gap](wall-off-the-forward-plant-and-leave-a-rebuild-gap.md) |

### Sweep 14 (s25) — the one sentence a builder should take from it

**Every deadline attack that converted elsewhere fired as a CONDITIONAL FALLBACK keyed
to a scouting trigger — never as an unconditional plan.** BC2025 The Kragle rushed only
when scouting found the economic opening denied; BC2020 confused encoded commitment as a
**price, not a mode** — a virtual surcharge on all non-rush spending before a deadline,
abortable by a store signal. **Both are cheap in our ruleset.** The matching structural
opening: the field's documented-as-sufficient anti-rush is **reactive unit production**,
and our engine rate-caps that at **≤1 builder per turn with +20% scaling** — turns are
not purchasable. Bounded by the fact that our field's real counter is *healing*, which is
not rate-capped.

**The strongest failure mode, and we should assume opponents can run it on us:** one
cheap mobile interceptor decides the matchup. Java Best Waifu: *"Our games against
Kryptonite depended almost uniquely if our initial drone was able to repel or capture
their rush miner or not."* **Our field's version of that interceptor is the LAUNCHER** —
20 Ti, +10% scale, no ammo, facing-independent, grabs either team's builder — and
sweep 12 independently found the field already prefers it defensively.

**Why topic 4 is not merely academic:** we measured (2026-08-09,
`docs/research/ammo-and-cpu-2026-08-09.md`) that Ouroboros discards **26,356
unit-turns across 85 games** — median 0 per game, mean 310, **max 3,508**, firing
in 44% of games. Leviathan 4.40%, The Bisons 4.65%. Every 1800+ team and we
ourselves sit at 0.00%. A conditional compute blow-up in three opponents is the
most exploitable shape a weakness can have, and we do not yet know the trigger.

**SWEEP 8 (objective functions for static defence)** is the most decision-relevant
of the set and **contradicts what we shipped**: four independent winners/podium
finishers encode static-defence value with **forward-ness POSITIVE** and **survival
absent as a term**. See [sweep 8](2026-08-09-sweep-8.md) — and read its **provenance
block first**, because its author disclosed fabricated quotes in an undelivered
draft and I re-verified four load-bearing claims against primaries before publishing.

| 5b | **RE-AIM of topic 5 at the in-base plant surprise** — how leagues both PLANT structures in enemy territory and DENY/REMOVE them, on both sides | **SWEPT** (s24). BC2020 (3 postmortems), BC2024, BC2025 (2), Terminal (starter-kit code + Wayback forum + 3 competitor writeups), Screeps docs/wiki, Jay Scott, Liquipedia SC2. **10 files.** Quotes re-verified by the research arm on the load-bearing source. | 2026-08-09 | [escorted-forward-plant](escorted-forward-plant.md), [turret-threat-field](turret-threat-field.md), [gunner-line-blinding](gunner-line-blinding.md), [sustained-plant-removal-race](sustained-plant-removal-race.md), [runtime-density-siting](runtime-density-siting.md), [preemptive-escort-turret-premortem](preemptive-escort-turret-premortem.md), [retake-the-vacated-tile](retake-the-vacated-tile.md), [standoff-removal-outranging](standoff-removal-outranging.md), [yield-and-reroute](yield-and-reroute.md), [funnel-not-seal](funnel-not-seal.md) |

### Sweep 9 (topic 5b) — what it settles, and one correction it makes to this library

**It arrived at the constructive answer to a refutation made the same session.**
`docs/research/cover-and-dodge-cuts-2026-08-09.md` killed the per-map/seat killer-tile
table (−3.9pp at k=8 out of sample, negative at every k). Sweep 9 independently found
that **the 2020 Battlecode winner solved the same problem with a RUNTIME field, not a
table** — a ±1 coverage grid maintained per unit, with covered tiles treated as
**binary obstacles**. Verified verbatim by the research arm against the primary PDF:

> *"every time a Net Gun is reported they would add +1 to all cells at distance 15 or
> less, and every time a Net Gun is destroyed they would add −1 …"* and
> *"A Drone considers all locations with value > 0 as obstacles"*

That is the same shape as the builder's live code fact (`_v100hf/main.py:4525`,
`_bfs_direction` already puts turret tiles in `blocked` with **no** range or
line-of-fire term) — **so we have half of the winner's mechanism already and are
missing the coverage half.** BC2024 supplies the same idea for *siting*: score
placements from **live** enemy density rather than a fitted map table.

**CORRECTION MADE BY THIS SWEEP, and it is the kind this library exists to catch:**
*"attack the builder, not the structure"* is **NOT sourced doctrine** as the counter
to a cannon/proxy rush. Liquipedia calls a single worker sent after the probe
*responding too lightly*; Jay Scott says chasing it *"will be hard to catch"*.
**Grepped: this library does not currently assert it.** If any future note does, it
must be labelled inference. Recorded so the claim cannot enter by repetition.

**Non-coverage, stated rather than implied:** Halite, Lux AI, CodinGame and AI
Challenge were **not** searched for this topic — the sweep stopped after BC2020 and
Terminal proved far richer on it. **Terminal's official rules page is unretrievable**
(302 live and in every Wayback capture; `docs.c1games.com` is DNS-dead), so every
Terminal *rules* claim rests on Correlation One's own starter-kit source, and
engine-side enforcement is inference. **A WebFetch summariser fabricated a Screeps
tower falloff formula that is absent from the raw page; it was caught and not used** —
the same failure mode as the documented incident above, now observed twice.

| 8b | **RE-AIM of topic 8 (economy) at the builder-exposure split** — how leagues allocate WORKER TIME between economy upkeep and defence upkeep | **SWEPT** (s24). BC2020 (3), BC2022, Liquipedia BW/SC2, Screeps docs + Overmind, Halite II. **6 files, 38 quote-strings all verified.** | 2026-08-09 | [worker-fortified-turret-cell](worker-fortified-turret-cell.md), [marginal-healers-per-structure](marginal-healers-per-structure.md), [heal-cap-and-timeout](heal-cap-and-timeout.md), [fortify-on-idle](fortify-on-idle.md), [defence-production-pegged-to-economy](defence-production-pegged-to-economy.md), [worker-pull-does-not-exist-here](worker-pull-does-not-exist-here.md) |

### Sweep 10 (topic 8b) — it explains the field's 5.04 lift, and it found a stale number

**The measured surprise it was sent at:** the field's home builders die next to *their
own turrets* (32.3%, lift **5.04**) where ours do so 2.7% of the time (lift 1.00) —
their exposed workers service **defence**, ours service **economy**.

**The sweep's answer is that the field's number is the signature of a mutual-protection
cell**, and it closes *harder* in our ruleset than in the games it came from, because
**builder attacks cannot touch builder bots at all** — so workers holding a turret's
orthogonal tiles out-repair the chip while the turret kills the only thing that could
remove the workers. `worker-pull-does-not-exist-here` is the control that makes the
reading forced rather than one of two: the canonical RTS answer to *"when does a worker
switch to defence"* is **it starts shooting**, which is impossible here — so the
field's turret-adjacent deaths **cannot** be a worker pull.

**And the counter-evidence is filed beside it, not buried:** BC2022's 5 Musketeers ran
our exact heal arithmetic and watched the repair queue pull *"nearly a dozen soldiers
out of commission"* and lose *"the clash in the middle"* — **and the middle game is
exactly where we die.** Anyone building toward the 5.04 must read
`heal-cap-and-timeout` first.

**A STALE NUMBER FOUND, CHECKED IN THE BOT, AND CORRECTED.** `docs/v79-analysis.md`
(proposal B0b) said *"a gunner is ~3.5/rd and a sentinel ~9/rd"*. The gunner figure is
**2× low**: `docs/reference/official-docs.md:257` says *"18 every 2 rounds against 7
every round"*, so a gunner is **7/rd**. **Before flagging it I checked whether it sized
anything shipped — it did not.** `MEDIC_TI_FLOOR/MIN_RND/EARLY_MIN_DMG/TYPES` carry no
damage-rate, and the heal-seat arithmetic at `_v100hf/main.py:550-560` uses a
**measured** siege DPS (max 23.22) instead. **The error is latent, not live — it would
have become live the moment anyone built B0b.** It doubles the healer count that
proposal implies: one healer (4 HP/rd) does **not** out-heal a gunner; two do.
Corrected in place at the source line.

**Non-coverage and negatives, stated:** **no league instruments the economy-vs-defence
worker-time split** — every rule found is a build-order ratio or a trigger, and not one
source reports realised worker-rounds by task. **No published repair-vs-rebuild return
measurement exists anywhere**; our 4.00 HP/Ti comparison appears to be original. Lux
(S1/S2) and Halite III gave nothing quantified. Terminal was dropped rather than
transferred — **it has no workers at all**, so its repair economics are a resource
decision, not a worker-time one. One CodinGame claim was found only as a search snippet
and **is in no file** because it could not be verified on-page.

**Quote discipline, recorded because it is the third data point on this failure mode:**
one drafted quote — *"SCVs are used to repair tanks and draw fire"* — turned out to
read *"They are also used to repair tanks and draw fire"* with **"They" referring to
Supply Depots**. Wrong subject, not verbatim. **Cut, not paraphrased into unmarked
text**, and replaced with a labelled paraphrase.

**THE WHEEL IS NOW FULLY SWEPT (all 12 topics, 2026-08-09).** Successive sessions
should re-sweep STALE rows rather than pick unswept ones — and prefer re-aiming a
topic at a specific measured surprise, which is what produced the best results here
(topic 11 re-aimed at the 2.2:1 edge; topic 9 re-aimed at "our opening is a
constant").

## Model rule for sweeps

**Every subagent gets an explicit `model:` — `opus` or `sonnet`, never `fable`,
never omitted** (Magnus 2026-08-09, restating the 2026-08-08 s18 directive after
it drifted a second time). Sonnet for mechanical sweeps with a validated method;
Opus for anything that must grade its own sources — which is most tactics work,
since the whole value is in the evidence labels.

## Standing context a sweep should know

- **The field does not rush.** Only 12% of top-tier kills land by r100; median
  kill round r296.
- **Everything about us breaks at r150.** Five independent instruments agree:
  conversion ratio, raider survival (43→6 rounds), turret production, forward
  placement, ammo conversion.
- **Late offensive insertion is refuted for us** (`late-game-doctrine-2026-08-09.md`):
  2.34% of forward throws at r200+ ever land a single attack on the enemy core.
- **We bank and do not spend.** We end r200-300 holding more titanium than
  Ouroboros while buying a twelfth as much ammunition.
- **THE UNIFYING FACT (2026-08-09, `heal-arithmetic-2026-08-09.md`): healing is
  4.00 HP/Ti and the best damage source is 1.80 HP/Ti, so the defender wins any
  titanium-symmetric attrition race 2.2:1 — and builder attacks cannot touch
  enemy BUILDERS, so only turrets clear a healing screen.** We run a
  damage-to-repair ratio of 1.11:1 against the field's 2.79:1. Every sweep
  should be read against this: the question is never "how do we do more damage"
  but "how does anyone break a 2.2:1 defensive edge".
  **AMENDED 2026-08-09 (s23), from engine source:** one heal repairs *both* a
  friendly builder bot and a friendly building on the same tile for 1 Ti, and a
  bot may co-occupy only a **conveyor, splitter, or the allied core**. So the
  stack caps at 2 entities = **8.00 HP/Ti → 4.4:1 on a stacked tile**, and the
  load-bearing case is **a builder standing on a core footprint tile.** The
  defender's edge is larger than the headline, not smaller.
- **THE SENTINEL FILE IS LEGAL BUT NOT A CAP-BREAKER (2026-08-09, s23).** Probed:
  a sentinel's shot lands through friendly entities and **does not harm them**. But
  the economics shrink the claim — **N=6 against a maxed 2×2 core (32 HP/round) is a
  5.4:1 exchange AGAINST the attacker**, ammo dominating. **Against the measured
  field detail of 2.68 healers, N=2 suffices.** It beats the defence opponents
  actually field, not the defence the rules permit.
- **THE ANSWER TO THE STANDING QUESTION, from sweep 2:** *mostly you don't break
  it — you win on economy.* Every league swept converged there independently, and
  each one that reached a defence-dominant equilibrium was rescued by **a clock,
  not a tactic.**
  **QUALIFIED BY SWEEP 14 (s25) — the second clause is FALSE across Battlecode
  seasons.** BC2020 and BC2023 were **offence-dominant seasons in this engine's own
  family**; BC2023 don't @ me report launcher rushing *"often deciding the fate of the
  game in less than 200 rounds"*, and what ended BC2020's rush era was a defensive
  counter-unit plus organiser map choices — **a tactic and a map pool, not a clock.**
  So a deadline attack CAN be dominant here-adjacent. **The precondition both seasons
  had and we lack: cheap, mobile, continuously-producible damage.** Our only mobile
  unit deals 2 dmg for 2 Ti and **cannot target enemy builders at all**; all real
  damage is immobile, must be paid for, placed inside the enemy kill zone, and cannot
  retreat. This does not contradict `THE FORWARD ROAD IS CLOSED` — **it explains it.** Our clock is round 1000 and our first tiebreak key is
  cumulative titanium delivered. **The crack that does exist is that our
  defender's heal is adjacency-capped at ~16 HP/round per tile while the
  attacker's damage on that tile is capped only by titanium** — concentration,
  not more damage.
- **MEASURED ENGINE FACTS (2026-08-09, s23 probes — stop assuming these).**
  **Store**: writes are buffered to next round; **last writer wins**; the
  read-increment-write ticket idiom **collapses silently** (5 writers → counter +1,
  all five believe they are unit #0); slot range is **unsigned 32-bit `[0, 2³²−1]`
  and a negative write RAISES**, which permanently destroys the unit.
  **Turret lines**: a **gunner** line is blocked by our own bots and buildings; a
  **sentinel** line passes through them (18 dmg landed through a friendly bot *and*
  a friendly barrier). `get_attackable_tiles()` **ignores occupancy** and reports
  the target as attackable in both cases.
  **Build legality** is strictly stronger than `is_tile_empty`; **spawn ring is the
  12-tile Chebyshev-1 ring** (`CORE_SPAWNING_RADIUS_SQ = 2`, not the r²=8 action
  radius).
- **UNIT TURN ORDER IS GLOBAL ENTITY-ID ASCENDING (2026-08-09, s25, research —
  measured, and it is documented NOWHERE in `official-docs.md`).** 26,078 ordered
  pairs, **0 inversions**; ids come from a single global creation-order counter.
  **This is a lever, not trivia: we choose our units' ids by choosing when we build
  them.** Demonstrated consequence — whether a thrown builder escapes its landing
  tile in the *same round* is decided entirely by this: `dwell = 0` in **84.14%** of
  throws where `launcher_id < victim_id` versus **1.83%** where `launcher_id >
  victim_id` (only **4 self-steps in 60,555** on the favourable side, and **0 in
  6,685** of our own). Any within-round race — who reaches a tile first, whether a
  turret fires before a bot steps away — is decided by id, so it is **reproducible by
  build order rather than luck.** Source: `../post-throw-tile-dwell-2026-08-09.md`.
- **POST-THROW DWELL IS ONE ROUND (2026-08-09, s25).** 97,999 throws over 6,233
  games: modal dwell **1**, and **96.4% of enemy victims are off the landing tile
  within one round**. Landing imposes **no move cooldown** (three hand-verified raw
  traces; a victim keeps its 1-move-per-round cadence straight through the throw).
  Share of throws lasting the **11 rounds a gunner needs: 0.42%**; the **7 a sentinel
  needs: 0.61%**. **Throwing an enemy into your own turret's ray is DISPLACEMENT plus
  at most one shot — never a kill** (~1 throw in 200). Also: **33.5% of throws land
  on an OCCUPIED tile** — always a conveyor or splitter, either team, never a turret
  or bot — so any "empty landing tiles only" count undercounts by about half again.
- **THE MIDDLE GAME IS THE TARGET, NOT THE ECONOMY (2026-08-09, s23).** Conditional
  on a core kill, the chance it is **ours** rises monotonically **29% → 55% → 72% →
  76%** across r0-150 / r151-300 / r301-600 / r601-999 — but **353 games reached
  r1000 and we won 57.2%**. We win the opening and we win the clock; we die in the
  middle. **`disengage and out-economy` (sweep 2) is REFUTED as a change**: paired,
  we already out-build the field on conveyors (+13) and under-build turrets (−3,
  leading in only 20.1% of games). It is our status quo, not a lever.
- **METHOD WARNING from the same work: our opening is a near-constant** — r0-150
  build medians are *identical* in wins and losses; all the variance is the
  opponent's. **A paired differential whose variance lives on the other side of the
  subtraction is an opponent thermometer, not a strategy dial.**
- **THE FORWARD ROAD IS CLOSED (builder, 2026-08-09 09:05)** on three
  instruments, and sweep 3 corroborates it from an independent evidence path.
  Research amended the magnitude of one of those instruments — see
  [`loki3-anchor-and-fargun-recheck`](../loki3-anchor-and-fargun-recheck-2026-08-09.md)
  — without disturbing the verdict. **Home defence is the measured asset**
  (+11.4 / +16.6 / +22.3pp over the field), and the launcher tactics above are
  the ones that reinforce it rather than opening a sixth doctrine road.
