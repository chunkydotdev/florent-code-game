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

| **15** | **RE-AIM at the incidence cut's surprise** — our build PRODUCTION is a constant (17/30 r0-50 medians identical between kill and no-kill games; CV **0.09** vs the field's **0.26**) and **CONTACT is what varies**. *(A) What was IN the trigger? (B) Did anyone ever separate contact-as-CAUSE from contact-as-MARKER? (C) Among fixed-opening bots, what varied after the opening and on what signal?* | **SWEPT** (s25). **19 files. 128 external verbatim + 7 internal, 8 near-misses corrected, 2 claims CUT.** **(B) is a clean measured negative.** | 2026-08-09 | [sweep 15](2026-08-09-sweep-15.md), [nobody-separated-cause-from-marker](nobody-separated-cause-from-marker.md), [self-play-inflates-the-effect-by-about-2x](self-play-inflates-the-effect-by-about-2x.md), [self-play-ab-has-the-wrong-population](self-play-ab-has-the-wrong-population.md), [branch-on-a-milestone-not-a-round-number](branch-on-a-milestone-not-a-round-number.md), [the-field-warns-against-early-contact](the-field-warns-against-early-contact.md), [infer-their-bank-from-their-spending](infer-their-bank-from-their-spending.md), [the-scout-that-pays-for-itself](the-scout-that-pays-for-itself.md), [the-trigger-rides-on-a-unit-already-going-there](the-trigger-rides-on-a-unit-already-going-there.md), [local-force-count-is-the-engage-gate](local-force-count-is-the-engage-gate.md), [arm-and-disarm-on-different-thresholds](arm-and-disarm-on-different-thresholds.md), [the-goal-stack-beats-the-mode-flag](the-goal-stack-beats-the-mode-flag.md), [defenders-advantage-has-exactly-two-mechanisms](defenders-advantage-has-exactly-two-mechanisms.md) |

| **16** | **RE-AIM at Magnus's asymmetry question — "we are rich downward and empty upward."** We sit at **1603.6**; our whole evidence base is against teams at or below us, while the top runs **2102 / 2040 / 2000 / 1977 / 1966**. *(A) How did competitors beat opponents STRONGER than themselves? (B) Did a league's top tier separate itself by doing MORE of the same, or something DIFFERENT IN KIND? (C) What did teams do when their own test pool was too weak?* | **SWEPT** (s25). **21 files. 150 verbatim, 18 near-misses corrected, 2 cut/held.** **(C)'s expected negative is REFUTED.** | 2026-08-09 | [sweep 16](2026-08-09-sweep-16.md) |

| **17A** | **RE-AIM at the incidence cut** — `KILL_WINDOW_RND: 250` is **not** our binding constraint (74.4% of our core-kill wins already land inside it). *What raised the SHARE OF DECISIVE GAMES elsewhere; what separates a bot that converts from one that grinds; the commit/abort decision; and did organisers change rules to raise decisiveness?* | **SWEPT** (s26). **23 files. 176 strings verbatim, 0 unverified, 0 cut.** **Falsifies sweep 15's round-number claim.** Queued one measurement which I then ran — see below. | 2026-08-09 | [sweep 17A](2026-08-09-sweep-17a.md), [pay-for-the-capture-with-no-economic-return](pay-for-the-capture-with-no-economic-return.md) |
| **17B** | **RE-AIM of topics 5 + 8 at the weapon-mix inversion** — ≥1700 cores die to gunner 53.1 / sentinel 44.4 / melee 2.5; ours is 22.7 / 69.2 / 8.1. *Cheap-close vs expensive-far; what decided the mix; superlinear costs; friendly line-blocking; and **is the top tier's gunner share a mechanism or a marker?*** | **SWEPT** (s26). **21 files + summary. 92/94 spans verbatim** (2 are quotations of the brief, labelled); **summary separately audited, 1 corrected.** **Verdict: mostly MARKER** — independently agreeing with the corpus-side pricing deliverable. **Corrects sweep 8.** | 2026-08-09 | [sweep 17B](2026-08-09-sweep-17b.md), [the-turret-mix-is-not-a-cost-decision](the-turret-mix-is-not-a-cost-decision.md) |

| **18** | **MULTI-STEP PLAN COMPOSITION — the first genuinely NEW row in a fully-swept wheel.** Magnus's oldest unanswered ask (*"bigger plans than that, more steps that might make a bad tactic actually a good tactic"*), which is the **converse** of 17A's *an economically-correct evaluator never finishes*. *(A) representation (B) commit/abort (C) did it beat reactive play, measured (D) where planning LOST* | **SWEPT** (s26). **25 files. 292 spans, 288 verbatim over 61 primary documents; summary audited separately (61/63).** **(C) IS A SURPRISE — the ablation exists.** 19 `yes` / 5 `partial` / 1 `no`. | 2026-08-09 | [sweep 18](2026-08-09-sweep-18.md) |

| **19** | **NETWORK CORRECTNESS AND REPAIR** — aimed at *"85.2% of our binding tiles have no directed path to our core; we are BREAKAGE-bound where every big-economy team is SATURATION-bound."* *(A) build-time connectivity invariants (B) repair vs rebuild (C) how does anyone DETECT silent breakage (D) self-interference* | **SWEPT** (s26). **24 files + summary. 228 strings verbatim, 0 unverified.** **My "nobody solved this" prediction is REFUTED** — and it found an **arithmetic fault in the parent cut's regrouped table.** | 2026-08-10 | [sweep 19](2026-08-10-sweep-19.md) |

| **20** | **PARTIAL OBSERVABILITY — acting on what a unit cannot see.** Re-aimed at the `WHAT LOKI IS` block (never play defence; a r1000 game is a defeat). Three arms: **20A** deception under fog (manufacturing a FALSE belief in an opponent who cannot see us) · **20B** our own fog + the illegal-query hazard (briefed as an ENABLER, not a plank) · **20C** committing to a stale belief. | **SWEPT** (s27). **20A: 41/41 verbatim, 1 cut, 3 near-misses corrected. 20C: 66/66 verbatim, 6 near-misses, 1 self-gloss cut.** **BOTH ARMS REFUTED THEIR OWN LEAD HYPOTHESIS.** Produced a **library correction** (see below). | 2026-08-10 | [20A files](hallucinate-a-target-to-steer-your-own-units.md) · [20C files](retract-the-target-only-on-a-look-not-on-a-clock.md) |

### Sweep 20A (s27) — **THE SEAM IS EMPTY, AND THAT IS THE FINDING**

**My pre-stated expectation was that deception under fog is a rich underexploited
seam. It is refuted QUANTITATIVELY.** Across **22 Battlecode postmortems / 123,745
words**: `decoy` **0** · `feint` **0** · `deceiv` **0** · `bluff` **0** · `mislead`
**0** · `disguis` **0** · `fake` **0**. `bait` = 1 (and it is a SELF-bait). `trick`
= 8, of which **exactly one is opponent-directed.** The IEEE ToG 2018 survey of a
decade of StarCraft AI competition carries **zero deception vocabulary.**

**Jay Scott states the law, and note the hedge — dropping it converts it into a
universal, which is one of the near-misses this sweep corrected:**
> *"**Most** forms of deception do not work against bots, because bots are not smart
> enough to fall for them. Exploitation of overreactions is a form of deception that
> often does work, at least against bots that react at all."*

**AND THE ONE BENCHMARK THAT MEASURES A FEINT SCORES OUR DREAM PLAY AT ZERO.**
HLSMAC scenario `dhls` — *"A small group of our units lures the enemy forces away.
Our main force attacks the enemy base."* — sits in the EXCLUDED set, and the
exclusion rule is *"scenarios where all algorithms achieved zero win rates."*
**All 21 algorithms scored zero, against a victim SCRIPTED to fall for it.**
(That `dhls` = 0.00 is inferred from caption + exclusion rule, not printed — labelled
`evidence: inference` in-file.) The other feint scenario `sdjx` is bimodal: **14/21
at exactly 0.00**, five at 0.72-0.89.

**⇒ FOR THE PROGRAMME: "manipulation" as an OPPONENT-DIRECTED play has no
precedent and one measured null. The transferable form is INWARD** —
[`hallucinate-a-target-to-steer-your-own-units`](hallucinate-a-target-to-steer-your-own-units.md):
BC2023 baited its OWN launchers by writing a synthetic enemy into its own comms so
existing reactive rules produced the behaviour, **with no new mode**. One store slot.
Its authors never measured it. **Immunity condition is named** (rooklift, Halite II):
*"We prepare for what the enemy could do, not what we think he will do. Therefore, it
cannot really be exploited"* — **deception needs a stored belief to corrupt.**
**Second prior refuted:** the global cost scale does NOT price decoys out —
`floor(scale x base)` means the first 34 barriers each cost 3 Ti. **The decoy is
priced in BUILDER-TURNS, not titanium** (act XOR move), which moves it into tempo.

### Sweep 20C (s27) — **SYMMETRY DOES NOT PIN THE CORE, AND DECAY IS A NULL WITH A MECHANISM**

**⛔ LIBRARY CORRECTION — [`2026-08-09-sweep-5.md`](2026-08-09-sweep-5.md) asserts the
map is *"symmetric, fully queryable"*. IT IS NOT.** Out-of-vision terrain queries
**RAISE** (`get_tile_env` / `is_tile_passable` / `get_tile_building_id`), and an
uncaught raise permanently destroys the unit. This materially changes the economics
of symmetry elimination: **the cost is WALKING, not CPU.** Independently agrees with
`../predicate-feasibility-2026-08-10.md` (CPU 15.6 us median vs a 10,000 us budget).

**Round-0 knowledge NEVER pins the enemy core — measured, not asserted.** 1,129
replays parsed, deduped to **20 unique maps** (population: this repo's archive, not
the organisers' generator):
| | result |
|---|---|
| true enemy core in {Hrefl, Vrefl, Rot180} | **20/20 (100%)** |
| distinct candidates = 3 / = 2 / **= 1** | 15/20 · 5/20 · **0/20** |
| `Rot180` correct | **17/20 (85%)** (Vrefl 25%, Hrefl 15%) |
| guard: true core shifted by (+3,+5) | **0/20** still among candidates — **the check produces the other verdict** |
**A WRONG GUESS COSTS ABOUT A SECOND FULL TRAVERSE** — max spread between candidates
median **24** vs true distance median **24**, equal in 17/18 on a second pass.
**~24+ rounds of a 250-round window, paid at the FAR end.** Shape: default `Rot180`
(85% free), walk it, disambiguate en route because the centre is the midpoint anyway.

**DECAY IS A NULL, AND ITS MECHANISM IS WHY.** Decay rules exist elsewhere and their
tuning parameter is **target mobility** (BC2026 lorem ipsum: *"Cats had 5 rounds, rats
had 0 (has to be this round), kings have 10"*; BC2023 4 Musketeers: *"since enemies
move, we reset that information every 100 ... rounds"*). **Run that against our entity
list: every target we can ATTACK is an immobile building, so N = infinity for all of
them.** Builder attacks hit buildings only; turrets fire from live vision.
**⇒ Do not spend store slots on information ageing.** The replacement rule is
[`retract-the-target-only-on-a-look-not-on-a-clock`](retract-the-target-only-on-a-look-not-on-a-clock.md)
— Steamhammer and PurpleWave independently retract a remembered enemy **only when the
tile is currently visible and it is not there**, no age term. PurpleWave: *"Buildings
that can't move are either in the same place or dead"*, default survival `Forever()`.

**And a measured warning against the obvious "verify before you commit" reflex:**
BC2020 The High Ground reported the scouting detour NEGATIVE on the majority branch —
*"This made our rush worse in cases when we would have guessed the right symmetry
anyway, but more consistent overall."* **Consistency is not our currency.**

### Sweep 19 (s26) — the negative is real and my prediction of it was still wrong, and (C) has a concrete answer

**(A) IS NOT THIN — four distinct patterns, all in competitive code.** **AdmiralAI dry-runs
the entire route under `AITestMode()` before laying a tile**, and logs *"pathfinding was ok,
building failed"* as its own outcome. **Overmind returns on `ret.incomplete` and enforces it
STRUCTURALLY** — the placement loop reads only from a map written on success, so a partial
route cannot leak. **NoNoCAB builds and then RE-WALKS the tile list**, treating *"built but not
connected"* as failure, **because its API has no reachability query, only adjacency — the
IDENTICAL gap our `Controller` has.** Mindustry and the Factorio Learning Environment deleted
hand-routing entirely.

**(C) — THE SUB-QUESTION I EXPECTED TO BE EMPTY HAS THE SHARPEST ANSWER: NOBODY DETECTS A
BROKEN NETWORK BY LOOKING AT IT.** **CluelessPlus never asks whether its road is connected** —
it fires the repair pathfinder when **a route's income falls below half its EMA**, with a rate
limiter and a deliberate post-repair damping of the baseline. **Factorio's wiki states the
reason from the other side: a full belt and a working belt are visually identical.** Three
cheaper detectors exist (stuck counter with reset-on-change, precondition timeout, model-based
prediction). **And the expectation-setting finding: in Overmind, ChooChoo and FLE the exact
check we want was WRITTEN, PRICED AND COMMENTED OUT** — Overmind's
`// TODO: repath if you are not on expected next position` is still live in the file.

**STRONGEST TRANSFERABLE ITEM — Overmind's `roadCoverage`: infrastructure completeness as ONE
PERSISTED SCALAR that a DIFFERENT subsystem branches on.** **It compresses to one small
non-negative integer — the single thing our 16-slot store is provably safe for** (all writers
agree, one-round buffer is fine for a level, negative-write raise cannot fire). **We currently
have no way to express "the network is broken" at all.**

**THE BREADTH NEGATIVE IS REAL AND LARGER THAN EXPECTED — and my prediction was still wrong.**
**Battlecode (all seasons), Halite I-III, Lux S1/S2, Terminal and CodinGame's 94-game catalogue
contain NO player-built directed breakable transport.** Battlecode contributed nothing, as
predicted. **But *"nobody solved this"* is REFUTED: OpenTTD NoAI is a real competitive league
that answers all four sub-questions, and it has never appeared in eighteen prior sweeps.**
**⚠ The field here is TWO LEAGUES WIDE — treat every convergence as a good SHAPE, not a
distribution.**

**⚠ AND IT FOUND AN ARITHMETIC FAULT IN THE PARENT CUT, IN EXACTLY THE ROWS THIS LIBRARY AND
THE BUILDER QUOTED.** `binding-tile-cut-2026-08-10.md`'s **§1 class table is exact** (sums to
100.000%, 7,767 Ti). **Its REGROUPED table sums to 120.5%**, and its note that the first three
are sub-classes of the two `DEAD_END_*` rows cannot hold: **33.4 + 23.9 + 11.1 = 68.4% against
a parent of 52.76%.** Three rows reconcile exactly (fix-facings, no-output, saturation);
**all four over-counted rows are precisely the ones quoted as the prescription ranking — 39.6
and 33.4, 23.9, and 11.1. They claim 74.5pp where their parents hold 53.50pp, a factor of
1.393.** **The qualitative finding is untouched. The RELATIVE PRIORITY is not established at
that precision and nothing should be sized on those numbers.**
**Three further qualifications:** **39.6% is not all build-time** — the source splits it into
never-built and destroyed; **the 74.3% opponent figure needs the 55.2% third-party number
beside it**, without which it reads as a capability statement rather than a selection one; and
**the 41% and 116-vs-34 figures come from the PARENT cut, with the 41% resting on the
single-output-tile instrument the binding-tile cut explicitly supersedes.**

**Three new method traps, each producing a false FAIL:** **ligature loss in old LaTeX PDFs**
(`efficiency` → `eciency`), **page furniture injected mid-sentence** (the `\f` fix does not
cover it), and hard-wrapped markdown. **The audit's first pass flagged 45 spans, of which 7
were the sweep's OWN paraphrases sitting inside quotation marks — the library's recurring
failure, in its drafts, in the same session it re-read the rule.**

**Gaps: the Battlecode negative is LEG-REPORTED, not first-hand** (every spec URL 404'd, and
one reported population looks short); **`tt-forums.net` is behind a bot wall so ~38 OpenTTD
threads are unread; no corpus cut was run.**

### Sweep 18 (s26) — the answer to Magnus's ask is 27 years old, it fits our exact constraints, and my pre-stated expectation was wrong in a way that changes the plank

**(C) THE EXPECTED NEGATIVE IS REFUTED, AND THE REASON IS A FINDING ABOUT THIS LIBRARY'S OWN
METHOD.** I pre-registered *"expect not to find a published planner-vs-reactive-ablation;
these leagues essentially never separate cause from marker."* **Wrong.** **Stone & Veloso,
RoboCup 1999, ran one with populations: teams *"otherwise identical"*, 38 games of 10
minutes, set-plays alone → 28 wins to 5, 187 goals to 108** — and they entered their own
ablation in a live tournament and beat it **6-0**.

**⇒ SWEEP 15'S HARD NEGATIVE MUST BE RE-SCOPED. It is true of GAME COMPETITIONS and false of
the adjacent ACADEMIC literature — which sat in an unswept row (RoboCup) this whole time.**
The library was searching where the negative is real. **Battlecode remains a clean negative;
the generalisation to "nobody, anywhere" does not survive.**
**Boundary that must travel with the result: the baseline is RIGID-SCRIPTED, not reactive.
The claim is *stored plans beat NO stored plans*, not *deliberation beats reaction*.**

**(A) THE REPRESENTATION THAT FITS OUR CONSTRAINTS IS ROBOCUP'S "LOCKER-ROOM AGREEMENT",
AND IT IS FREE FOR US.** **The plan is never transmitted.** It is pre-agreed and **identical
in every agent**; the channel carries only a **formation index and a timestamp**.
**We already have the whole mechanism: the same `main.py` runs in every unit, so a
module-level mode table is shared at ZERO bandwidth.** The 16-int store then needs to carry
**one small nonnegative int** — at which point **every measured hazard of that store becomes
harmless**: last-writer-wins is fine when all writers agree, the one-round buffer is fine for
a mode index, and the negative-write raise cannot fire.
**And plans must name ROLES, NOT UNITS** — our ids are one global counter shared with
resource stacks, and raider lifetime at r150 is **6 rounds**.

**The modal WINNING representation elsewhere is no stored plan at all** — Halite III's 1st/
6th/7th recompute a score per unit × tile every turn, Lux S1's winner is a stateless net,
PurpleWave rebuilds its production timeline every tick. **Commitment is bought with a shaped
score or ONE CONSTANT**, not with a queue.

**(B) "A CHEAP ABORT PREDICATE" IS THREE PREDICATES DOING THREE JOBS**, and the third is the
one we lack:
- **VALIDITY** — Overmind splits it in two: `isValidTask` (about the actor) vs
  `isValidTarget` (about the world). **Ours is `can_build_*`.**
- **PROGRESS** — Steamhammer's `ProductionJamFrameLimit = 360`; PurpleWave's is
  state-conditional (45 s before the plan pays, 90 s absolute).
- **GRANULARITY** — **replanning from scratch on every disruption produced an INFINITE
  RESTART LOOP and lost the matchup; classifying disruptions and patching in place won it.**
**Commitment itself is one constant added to last round's answer** — Steamhammer `+= 13/11/4`
under a comment reading `// Hysteresis.`, PurpleWave 1.5×, UAlbertaBot's asymmetric 100-frame
lockout, Stardust's 120-frame belief dwell. **Cheapest item in the sweep: `goToState` vs
`goToStateTemporary`, one line apart — a resumable interrupt with no stack.**

**(D) AND THE NEGATIVE IS BRUTAL, WHICH IS WHY THE SHAPE MATTERS MORE THAN THE IDEA.**
MicroRTS 10-agent round robin, 60 starting positions per matchup, **100 ms/cycle — 10× our
budget**: the **AHTN planner scores 24.0**, NaïveMCTS **13.3, last of ten**, against
LightRush's **55.3** — and **three separate hand-coded scripts each beat the HTN planner
100.0%, 60 of 60.** Runner-up: **PurpleWave deleted 8,596 lines / 221 files of declarative
gameplan DSL in two days** and went 82.29% → 82.95%. Deepest: Steamhammer's maintainer calls
plan latency a **design** defect, not an implementation one.

**⇒ THE SYNTHESIS, AND IT DECIDES WHAT THE NEXT PLANK BUILDS.** **What lost everywhere is a
SEQUENCE. What won is a MODE.** My own brief drew the line as *"a committed mode rather than
a plan representation"* — **that is wrong: a mode table IS the plan representation, just not
the one people picture.** The two literatures converge independently. **So: build a table of
indices, not a queue.**

**⚠ AND THE LIMIT, STATED BY THE SWEEP ITSELF: none of this answers whether such a mode
converts games HERE. It licenses the SHAPE, not the content.**

**THREE MORE METHOD TRAPS, each of which produced a FALSE FAIL in this sweep:** JSDoc `` * ``
continuation markers survive whitespace flattening; `pdftotext` emits `\x0f` bullet controls
**inside** sentences; inline `<code>` injects spaces into surrounding prose. **Plus a data
trap: MicroRTS tables must be read with `pdftotext -layout` — the default extraction reorders
them column-wise and yields real numbers attached to the WRONG AGENT.**
**Nine near-misses caught in the sweep's own drafts**, including **three of its own phrasings
written inside quotation marks** — the recurring one.

**Gaps:** the AI Magazine MicroRTS competition paper is unfetchable (4 routes); Kaggle
writeups are SPA-only (Lux S2 sourced from code, not prose); **Halite I unsearched**; two
MIT-hosted Battlecode postmortems 500 on every attempt; **RoboCup is now only PARTLY swept**.
**No corpus cut was run.**

### Sweeps 17A + 17B (s26) — the weapon-mix question is answered MARKER by two independent paths, and the incidence question turns structural

**⚠ FIRST, THE CORRECTION THAT REACHES BACKWARDS INTO THIS INDEX.** The **53.1 / 44.4 / 2.5**
figure that aimed 17B — from `../upward-pricing-top-tier-2026-08-09.md`, **my own s25
deliverable** — **is a MIXTURE ARTIFACT.** Across 53 third-party teams,
`corr(rating, gunner kill share) = −0.025` and **exactly 1 of 22 teams lands within 5 points
of the pooled 53%**: the tier contains incompatible doctrines that average to it (**Pivot
100% gunner at 1956; Clankers 99.8% sentinel at 1984**). **What tracks rating is core-kill
rate itself, r = +0.767.** The source doc is amended in place.
**⇒ Any earlier claim in this library premised on "the top tier prefers gunners" does not
survive. Doctrine-conditional claims — what a Clankers-like sentinel doctrine does forward —
do.**

**AND THE SENTINEL IS THE CHEAPER WEAPON, three ways.** The organisers' primary says it
outright — *"per point of damage a Sentinel is slightly cheaper to run than a Gunner"*
(`../reference/official-docs.md`, verified verbatim). Realised lifetime output over **2,228
sentinels / 8,205 gunners**: **0.652 vs 0.678 Ti per damage point, cheaper in every band
including ≥1900.** And 17B's independent arithmetic: **ammo 0.5714 vs 0.5556 Ti/damage — a
2.9% gap**, with the **sentinel the higher-DPS unit at 9/round against 7** (*"18 every 2
rounds against 7 every round"*). **Build cost for equal firepower: 9 gunners 324 Ti vs 7
sentinels 336 Ti.** Everything is within ~10% and the two biggest gaps point opposite ways.
**⇒ If the gunner mix is a mechanism it is GEOMETRIC, not economic.**

**THE ONE SURVIVING MECHANISM, and it is a siting predicate rather than a quota.** A
gunner's line *"stops at the first targetable tile (a builder bot or a building) in its
facing direction"* and reaches **3 tiles cardinally** — so a gunner core-kill **requires a
≤3-tile stand with a totally clear axis.** It measures the approach, not the weapon.
**At ≤3 tiles with a clear line, the sentinel's premium is property you are not using.**

**WHAT WE ARE ACTUALLY WRONG ABOUT IS SITING, and the numbers are not close.** Our sentinels
sit at median **d²=18 from our own core, 30.7% forward, firing at 13.5% of reload ceiling**;
comparable builders site them at **d²_own 53-181, 63-93% forward**; **Clankers runs 74.4%
forward at 46.4% of ceiling.** And the under-build story dies on one row: **`sporks`, #1 at
2082, builds 1.99 gunners per side-game — we build 1.95.**

**(D) FRIENDLY LINE-BLOCKING IS A CLEAN NEGATIVE IN EVERY COMPETITIVE LEAGUE** — Screeps,
Terminal, Code Royale, 22 Battlecode postmortems, the RTS canon. The only two precedents are
colony sims (Dwarf Fortress staggering 3×3 siege engines; RimWorld's wall/barricade mix).
**⇒ Our gunner's self-blocking is close to unique, and the transferable consequence is
blunt: two gunners in file are one gunner and one 20 Ti barrier.**

**(C) NOBODY PRICES THE Nth STRUCTURE HIGHER** — Screeps uses per-RCL count caps with flat
towers, Terminal is flat, Battlecode uses spend caps or upgrade tiers. **One new build idea
falls out of our own rule instead:** our scale *"decreases again when an entity is
destroyed"*, so **demolish before you build** — a replacement sentinel prices at
`floor(1.8×30) = 54` instead of `60`, and the discount applies to **every** build in the
window. **⚠ Rests on one unprobed fact: whether `destroy()` updates scale within the same
round.** Builder probe, not a library claim.

**(B) FOUR DECIDING VARIABLES, AND RANGE IS NOT ONE.** Lanchester (AIIDE-15): *"the squared
law has nothing to do with range – what is really important is the rate of acquiring new
targets."* Its default α = dmg × HP gives **gunner 175, sentinel 360 — the sentinel 1.37×
better per titanium, CONDITIONAL ON BOTH FIRING**, which is exactly the condition our 13.5%
duty cycle fails.

**17A'S STRUCTURAL FINDING, and it is the deepest thing either sweep produced.**
**AN ECONOMICALLY-CORRECT EVALUATOR NEVER FINISHES.** Jay Scott adds *"a small bonus in the
move generator for captures of enemy planets… to allow it to take 0-growth enemies if
nothing else beckons"*; Steamhammer's scourge are hard-coded not to waste themselves on
floating buildings — **correct efficiency, and exactly what blocked the kill.**
**This lands on our ruleset mechanically: killing the enemy core returns no titanium, no
harvester and no tiebreak key, and a failed attack is a 2.2:1 donation. A return-priced bot
is CORRECT to never commit.** The documented converter is a **discrete mode switch that
REPLACES the economy policy** (Steamhammer's `enemySeemsToBeDead()` short-circuits the whole
tech planner; BC2020's "crunch" is the same structure sized as a rate) — **and the
documented failure is doing it as a weight.**

**SWEEP 15'S "NO WINNING BOT BRANCHES ON A ROUND NUMBER" IS FALSIFIED.** robostac, 1st in
Code Royale: *"For the last 40 turns spend gold as fast as possible"*, *"For the first 50
turns just send knights"*. **What survives is narrower and better: a clock is a poor ARMING
trigger and a good DEADLINE/DISARM trigger.**

**DESIGNERS REACH FOR THE MAP, NEVER A SHORTER CLOCK.** BC2020 deleted the score fallback
outright; **Halite III deleted its 80×80 map while RAISING the turn floor 300→400**; Halite
II's organisers **vetoed** proposed elimination timers — *"I veto any change related to this.
Survival is part of the meta"*.

**AND THE FINDING THAT ARGUES AGAINST OUR OWN PROGRAMME, FILED RATHER THAN BURIED.**
SSCAIT's tiebreak pays for razings; **ours pays for economy.** Slin took 3rd in Planet Wars
by **deliberately never finishing**. *"Krasi0 was ahead in points, on average, in the games
that it lost"* — **so every natural proxy for an offensive change is a trap.** Measured on
our own tape the same evening: **our r1000 tiebreak win rate beats our decisive-game win
rate by +9.8pp against 1550-1649 opponents and trails it by −7.5pp against <1450 — the sign
flips monotonically with opponent strength.** **Bounded: selection is the leading
alternative** (reaching r1000 against a stronger opponent already selects for games we were
not losing) — **`UNSEPARATED`** — and **≥1750 is EMPTY: we have never played a game to r1000
against the tier we must beat.**

**A CORRECTION 17B MAKES TO SWEEP 8, which this INDEX calls "the most decision-relevant of
the set".** Sweep 8 presents **Agade's** site-scoring formulas as the encoding of his
doctrine. The formulas are genuine and re-verified — **but they sorted WHICH SITES, and that
branch was *"very often this was overridden"* by a "Knight danger" fallback that could only
build towers**, which Shingy (9th) wrote counters to (*"This was mainly for Agade's strategy
of covering the map with towers."*). **"Forward-ness positive" stands as a site-choice
weight; it must NOT be upgraded into why his bot was tower-heavy.** Sweep 8's other sources
are untouched.

**THREE NEW METHOD TRAPS — the quote procedure needs two more steps.**
1. **The glyph trap is per-STRING, not per-document.** JWU's BC2025 PDF has ASCII `'` in
   *"that's"* and curly `’` in *"wasn't"* **in the same file.**
2. **Markup inside numerals defeats the literal grep even after whitespace flattening** —
   CodinGame writes *size `<const>1</const>` tree*; the Screeps wiki stores *'centered'* as
   `&#x27;`. **The procedure is now: extract → strip markup → decode entities → flatten
   `\f\r` → grep the literal.**
3. **JSON-escaped punctuation is a third variant** — Wayback's Kore capture escapes every `+`.
Plus two auditor artifacts: text between two *adjacent* inline code spans reads as a quote,
and **two blockquotes with no blank `>` between them concatenate into a string that can never
match** — indistinguishable from a real failure until inspected.

**GAPS, STATED RATHER THAN PASSED OFF AS COVERAGE.** **Liquipedia produced ZERO verified
strings in 17A** (HTTP 429 across 6 attempts, 4 user agents, both curl and WebFetch) — **no
Liquipedia quote appears anywhere in 17A.** **Terminal remains unverifiable** (Cloudflare;
and its shipped config and the engine's hardcoded fallback are **two different balance
patches, both live at HEAD**). **RoboCup, Warcraft III tower doctrine, and CodinGame's wider
catalogue were not swept.** **17B ran NO corpus cut** — the decisive test (distance and
line-clearance of the killing turret at the killing shot, ours vs theirs) **is not run and
is not claimed.** Halite III's map/turn edits **carry no stated rationale**; "tuning contact
density" is 17A's inference and is labelled as such.

### Sweep 16 (s25) — at a 400-Elo gap, opponent modelling bought nothing and only variance scored

**(A) THE RESULT, and it is the sharpest single data point the library holds on our actual
situation.** AIIDE 2020: **Microwave finished #6 at 54.47% overall and scored 1% against
#1 Stardust.** Its published opening table was re-parsed by the sweep itself — **47
openings, 150 games, exactly ONE nonzero row: `3HatchLingBust 9 11%`, an all-in.** Its
most-tried opening went `3HatchMuta 36 0%`.

**And the obvious alternative explanation dies in the same source: Microwave predicted
Stardust correctly in 127 of 150 games — *"Not that it helped."*** So at a 400+ Elo gap,
**perfect opponent modelling bought nothing and only maximum variance scored anything at
all.** We are 400-500 Elo below our own top tier, which makes this the closest documented
analogue to our position that any sweep has found.

**The counterweight is filed beside it, not buried:** Jay Scott traded upset-proneness for
strength **deliberately** and rose. So variance is the *underdog's* instrument, not a
strategy — it buys single games against a wall, and it costs you the games you should win.

**(B) IS ANSWERED BOTH WAYS, and both readings are published with the disagreement
stated.** This matters because our own measurement says our defence is *more of the same*
(collar 66.5% against a field 53.2%) while the top tier is **thinner** (40.6% at ≥1900) —
see [`../upward-pricing-top-tier-2026-08-09.md`](../upward-pricing-top-tier-2026-08-09.md).

**(C) THE EXPECTED NEGATIVE IS REFUTED — five leagues solved it explicitly.** The brief
held open *"if nobody solved it, that is a bound on what local testing can tell us."*
**Nobody's problem; they solved it:**
- **wololo, in our exact position** — *"my new strategy demolished the locally ranked
  competition"* — *"had to test purely by requesting scrimmages against high-ranked teams."*
- **BC2026's 2nd place got its magic numbers by reverse-engineering replays of teams above
  it**, corroborated independently in Halite III and CodinGame.
- **VirtualAtom replaced one aggregate win-rate with FIVE NAMED OPPONENTS and per-opponent
  gates.** That is the directly buildable one for us.
- **And the errors have a direction:** training data *"overestimated Microwave's success"*
  against stronger opponents — i.e. a weak pool does not merely add noise, **it biases
  optimistic**, which is the same sign as sweep 15's ~2× self-play inflation.

**METHOD FINDING, and it is a guard gap in this library's own process:** of 18 near-misses
corrected, **14 were compressions in the SUMMARY document — which had never been
machine-audited before.** Per-tactic files were being verbatim-checked; the summary that
most readers actually read was not. **Audit the summary, not only the files.**

**A CORRECTION THE SWEEP MADE TO ITS OWN BRIEF:** *"the ladder is the field instrument"*
is **not in this INDEX** — it is a session-memory directive (Magnus, 2026-08-08) that was
being cited as though it were library standing context. Recorded so it is not quoted from
here.

### Sweep 15 (s25) — the negative is the finding, and it bounds this whole library

**(B) NOBODY, ANYWHERE, SEPARATED CAUSE FROM MARKER — and that is measured, not asserted.**
Across all **22 official Battlecode postmortems 2019-2026**, these strings appear **zero
times in every document**: `correlat`, `causal`, `confound`, `ablat`, `regression`,
`hypothes`, `sample size`, `noise`, `misleading`, `coincidence`, `p-value`, `random seed`,
`number of games`. Halite, Lux, CodinGame and Terminal return the same negative
independently. **The question is not answered badly — it is not asked.**

**⇒ THE LIBRARY'S EVIDENCE CLASS IS NOW BOUNDED, and this is the most important line in
the index.** Every "what converted a rush" finding in sweep 14 and every finding in sweep
15 rests on **winners describing their own winning games.** Since nobody ever separated
cause from marker, **the library cannot adjudicate that question for us. The arena is the
only instrument — and that is now a SOURCED conclusion rather than a default.**

**What the field has instead is a literature on the LIMITS OF SELF-PLAY A/B, and it is
directly load-bearing on how we test.** The **BC2025 winner overrode its own A/B twice and
won**, on the stated ground that *"our bot wasn't super aggressive, and we believed that
this, in theory, SHOULD be better against the teams that we have the worst matchups
against."* **That defect is exactly ours** — the self-play pool does not contain the
opponent behaviour the feature is designed to read, and our own opening is a near-constant
(CV 0.09) in a pool we dominate 87-90%. And one competitor **published the same feature
measured on both instruments**: *"Locally, in self-play, amputating this opponent modelling
causes a loss of ~30% in winrate"* against *"~15% seen with CGBench"* — **roughly 2×
inflation, same sign**, with a usable mitigation (amputate, during the self-play leg, the
module whose accuracy is inflated by the opponent being a copy of you). Halite II's winner
independently: local testing *"became increasingly inaccurate and pointless over time."*

**Three qualifications to standing context, all narrowing rather than reversing:**
1. **Sweep 14's trigger is filled in, and it is ECONOMIC.** Our own corpus cut says the
   enemy-side signal is *their economy failing*; Java Best Waifu and Shummie independently
   keyed on **enemy economic state**. *"Commit when their economy has not come up"* is
   **doubly sourced**; *"rush when they look aggressive"* is sourced by **nobody**.
2. **`KILL_WINDOW_RND: 250` is a round number, and NO winning bot in this sweep branches
   on a round number.** Every branch found is on an achievement, a structure count, a
   resource threshold, or map geometry. **This does not contradict the PROGRAMME — the
   window is a target, not a trigger — but the IMPLEMENTATION of a commitment should
   probably not be a clock.**
3. **The RTS leg landed after the summary was written and only the re-verifiable part was
   published. HOLDING IT WAS RIGHT, AND THE HELD CLAIM TURNED OUT TO BE WRONG.** The
   unpublished item was *"PurpleWave branches at ~1:32 off a single enemy
   building-completion timestamp"*, which would have **superseded** the earliest branch
   point published under (C). **Its own author then corrected it before anyone published
   it: the strings verify but the framing did not. `1:32` is a REFERENCE CONSTANT recording
   the fastest-observed 4-pool, not a decision boundary.** The threshold the fingerprint
   actually tests is **1:55** (derived as `NinePool_PoolCompleteBy` 1:58 minus 3 s), and the
   earliest window opening anywhere in the fetched code is **1:30**, on a *negative-evidence*
   "Main empty" rule. **And what the fingerprint switches TO is unverified** — it sets a
   label; the consequent lives in gameplan code never fetched. **This is the strongest
   argument in the library for the hold-what-you-cannot-re-verify rule: the held claim was
   a true string with an invented referent, and holding it is the only reason it never
   entered.** **New URL trap: BW `liquipedia.net/starcraft/Rush` is a PLAYER PROFILE, not
   the strategy article.**

**OUTSTANDING FROM SWEEP 15 — relayed to me but NOT verified by me, therefore claims and
not findings.** The RTS leg's full packet (24 re-verified strings) could not be routed
peer-to-peer and reached me only as a summary. Recorded so the next session can close it
rather than re-derive it:
- **Question (B)'s hard negative is reported to SURVIVE two challenges** — a "Microwave
  confounder" that is about *scouting* and self-hedged, and a "Facebook control run" that
  controls **build-order switching on/off, not aggression**. A 49-paper grep is reported to
  find nothing on attack-timing causality. **If true this strengthens (B); I have not seen
  the strings.**
- **No FORCE-RATIO threshold for first contact is reported to exist anywhere in the RTS
  corpus** — the closest being UAlbertaBot's `bool retreat = score < 0;`, *a simulated
  outcome, not a ratio*. **Note this does NOT conflict with
  [`local-force-count-is-the-engage-gate`](local-force-count-is-the-engage-gate.md)**, which
  documents a **signed count**, not a ratio — if the UAlbertaBot string verifies it is a
  *fifth* league independently converging on a **sign**, which would strengthen that file.
- **A GLYPH TRAP for anyone re-grepping these sources:** Liquipedia and source code use
  **ASCII `'`**; satirist.org and PDF-extracted text use **curly `’`**. Combined with the
  `\f` flatten fix above, a literal grep needs the right apostrophe *and* collapsed
  whitespace. Two Liquipedia quotes (Rush, Cheese) are **truncated mid-sentence because
  `scouting`/`All-In` are inline hyperlinks**, so the full sentences will never grep.

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

## ⛔ PREREQUISITE — **OUR ARENA POOL CANNOT MEASURE A DEFENSIVE PLANK AT ALL** (2026-08-10, builder's LOKI-10 sizing; read this BEFORE proposing any defensive tactic)

**Not one of our forward sentinels takes a single point of damage in 480 arena games.
Survival is 100.0% at +10 / +20 / +30 / +50 rounds.** The cause is the opponent list:
**the probe family fires 54,264 shots and 99.83% of them target our CORE.** They are
single-target core-rushers.

**THIS IS A THIRD KIND OF SATURATION AND IT IS THE WORST ONE.** The library already tracks
*"the bar is too high to resolve"* (win rate 93-97% on clanker/ouroboros). **This is
different: THE MECHANISM NEVER OCCURS.** Every **survivability, healing, screening, repair or
ablative** plank measured against `cad_probe` / `orizon_probe` / the probe family is
**measuring a treatment on an event that does not happen**, and **would return a clean null
that means nothing.**

**⇒ A BUILDING-ATTACKING OPPONENT IN THE POOL IS A PREREQUISITE FOR THAT WHOLE CLASS OF WORK,
NOT AN IMPROVEMENT TO IT.**

> **⚠ AMENDED 2026-08-10 (s26, research) — THIS BLOCK OVERSTATED THE PROBLEM IN TWO WAYS, AND
> WE AUTHORED THE SCARCITY OURSELVES.**
>
> **1. The 99.83%-at-core is OUR OWN CODE, not a property of the field.**
> `grep -l "best_core or best_any" bots/*/main.py` returns **five of nine** opponent-imitation
> probes. **It is a copy-pasted target-selection shortcut in the probes WE wrote** — never a
> measurement of how opponents behave. **The league is the opposite: over 67 third-party
> teams, the non-core share of enemy-directed attack events runs min 0.0% / p25 40.4% /
> median 59.1% / p90 91.8% / max 100.0%, and 44 of 67 attack BUILDINGS MORE THAN CORES.**
> **66 of 67 sit above the probe family's 0.17% floor.**
>
> **2. "Nine items are gated" is too strong. They were unmeasurable IN THE ARENA; a live
> field instrument already existed.** **We lose 46.9% of every turret we build on the
> platform — 5,599 of 11,947 across 2,313 games.** The ladder was measuring these treatments
> the whole time. **The correct statement is: the ARENA cannot see them; the LADDER can, more
> slowly and without a controlled arm.**
>
> **3. And the replacement fixture is MIS-CALIBRATED IN THE DIRECTION THAT FLATTERS THE
> TREATMENTS IT EXISTS TO TEST.** `razer_probe` sits at **p93 on attack volume (339/game) but
> only p58 on kills (13/game)** — **26 attack events per building destroyed, against a league
> range of 3.4-37.4 and a median near 10.** **A repair line easily out-paces an attacker
> needing 26 swings per kill** (heal is 1 Ti for +4 HP; a builder attack is 2 Ti for 2 damage)
> — and would be overwhelmed by **Ouroboros at 4.0**, live on the ladder, which beats us 83%
> of the time. **Trust it for "does the treatment do anything", never for "how much".**
> Source: [`../building-attackers-2026-08-10.md`](../building-attackers-2026-08-10.md).

**Library items this gates — they are not wrong, they are UNTESTABLE HERE until the pool
changes:** [`sentinel-file-stacking`](sentinel-file-stacking.md) · the **ablative barrier
screen** (~8× HP/Ti, sentinel-only) · [`worker-fortified-turret-cell`](worker-fortified-turret-cell.md) ·
[`marginal-healers-per-structure`](marginal-healers-per-structure.md) ·
[`heal-cap-and-timeout`](heal-cap-and-timeout.md) · [`fortify-on-idle`](fortify-on-idle.md) ·
[`preemptive-escort-turret-premortem`](preemptive-escort-turret-premortem.md) ·
[`sustained-plant-removal-race`](sustained-plant-removal-race.md) ·
[`the-defenders-reserve-and-what-defeats-it`](the-defenders-reserve-and-what-defeats-it.md).

**AND THE FIXTURE DISTINCTION IS THE POINT, because it was conflated once already:**
forward-ordnance survival is *"the sharpest number in the corpus"* — **in the LADDER corpus,
against real opponents. It is UNMEASURABLE in our arena.** **Those are different fixtures.
Any survival, heal or screening figure must name which one it came from.**

**TWO MORE FIXTURE-SPECIFIC FACTS FROM THE SAME CUT:**
- **`builderAttack` is emitted 0 times by EITHER side in the 480-game LOKI-9 battery set.**
  **So the behavioural seat fingerprint — *"our `batk` = 0 against theirs = 5,185"*, which is
  LADDER-valid — cannot discriminate there: both sides are zero and it fails silently.**
  **⚠ NARROWED 2026-08-10 (s26): this is BATTERY-SET-specific, NOT "the arena" generally.**
  A different 24-file arena population carries **13,056 `builderAttack` events**, because it
  includes `razer_probe` runs which emit hundreds each. **The original phrasing — mine, from
  the builder's number — generalised one battery to a whole fixture class.** **The safe rule
  is the general one: a behavioural fingerprint is only valid in a population where the
  behaviour it keys on actually varies — check that before using it, in every new set.**
- **⚠ THE "OUR HEAL IS DEAD CODE" FINDING IS FULLY REFUTED (2026-08-10, s26). Recorded here in
  its final form because it was published, propagated and corrected three times in one night,
  and the CORRECTION IS MORE USEFUL THAN THE ORIGINAL CLAIM.**
  **What was reported:** *"0 of 87,169 heals land on anything but our own core"* in a 480-game
  arena battery, attributed to **priority ordering** (`_heal_core` outranking `_heal_adjacent`)
  and filed as removal-shaped dead code.
  **What is true:** **the heal was never dead — it had nothing to repair.** The battery
  inflicted **zero** building damage, so *"0 heals on buildings"* was **the only possible
  observation**, and it looked exactly like a code defect.
  **Measured where damage exists:** on the platform, v102 heals **29.3%** of incoming damage to
  its non-core buildings back (30,037 of 102,614 HP; 8,870 of 23,772 heal events land on a tile
  holding a non-core building). **In the razer fixture, 47.9%** (10,660 of 22,238 HP).
  **The mechanism, and it means intent cannot answer the question:** `heal(position)` repairs
  **EVERY** friendly entity on the tile, so heals aimed at a builder standing on a conveyor lane
  **repair the lane as a side effect.** **Intent is core-only; effect is not.** ⇒ *"Does our bot
  repair its buildings"* **is not answerable from code reading at all — only from effect.**
  **THE GENERAL LESSON, which is why this entry is long: a bug was diagnosed from a fixture
  STRUCTURALLY INCAPABLE of exhibiting the behaviour that would have disproved it** — the 0a
  failure consuming a finding written one hour after 0a itself. **Before attributing an absence
  to a defect, ask whether the fixture could have shown the alternative.**
  **AND IT IS THE MEASURED FORM OF THE THREAT-MODEL ARGUMENT ABOVE:** a defender repairing
  **~48%** of an attacker's output is exactly what **1 Ti/+4 HP against 2 Ti/2 damage**
  predicts. **A builder-only attacker cannot threaten a repairing defender.** **⇒ The
  turret-bearing second fixture is a STANDING PREREQUISITE before any repair plank is trusted,
  not an option.**

## ⚙ THE ONE STRUCTURAL FIX — **MEASURE INSIDE THE ARM YOU ARE TESTING. NEVER SIZE ANYTHING ON A STORED FIGURE.** (2026-08-10, s26)

**Nine distinct failures across two lanes in one session turned out to be one fault wearing
different clothes.** Every one of them was a number that was true **somewhere** and got used
**somewhere else**:

| what it was measured on | what it got used as |
| --- | --- |
| a **view** (join-mapped subset, n=212) | the **population** (true n=273) |
| an **assumed capacity** (1 stack/tile) | a measured **utilisation** (25%) |
| an **assumed game length** (1000 turns) | a per-turn **rate** |
| a **battery** (480 arena files) | a **fixture class** ("the arena") |
| a **three-line window** | a **file** ("byte-identical") |
| **turret + builder events** pooled | a **builder-only** benchmark |
| an **Eir-era archive** (92% of games) | the **current line** |
| one **vivid probe observation** | a **rate** |
| a **denominator** chosen after seeing the split | a **comparison** (same claim flips sign) |

**AND THE FIX IS THE SAME IN ALL NINE CASES, which is why it is worth stating once instead of
nine times: MEASURE BOTH SIDES OF YOUR COMPARISON INSIDE THE THING YOU ARE TESTING.**

- A **paired within-arm control** is immune to era drift **by construction** — both arms are
  the same bot on the same day, so it does not matter what the archive is made of.
- A **control arm in the same fixture** is immune to fixture contamination — a probe that
  cannot see your buildings cannot see them for either arm.
- A **rate with both numerator and denominator from the same population** cannot be a view.
- **Measuring both arms** removes the need to divide by an assumed constant at all.

**THE DEMONSTRATION, and it is the reason this block exists.** Three planks were sized in one
evening. **Two died of era drift before they ever fired** — a forward-gunner plank motivated by
`57.2% dead inside 30 rounds` (Eir tape; the current line plants ~5 forward gunners in 75
games), and a facing plank motivated by `13.2%` on-line and `61.4%` violation (Eir). **The
third survived — and NOT because anyone foresaw the era problem.** It survived because its
pre-registration **pinned every bar to a paired within-leg control** and **pre-declared its
currency channel closed**. **The discipline that saved it was subject-and-population hygiene,
applied for unrelated reasons, and it turned out to be the same defence.**

**⇒ PRACTICAL RULE FOR A SUCCESSOR: before using ANY figure from this library, from `HANDOVER`,
or from any deliverable to size a plank — ASK WHICH BOT, WHICH POPULATION, AND WHICH FIXTURE IT
WAS MEASURED ON. If the answer is not "the arm I am about to run", do not size on it. Use it to
choose WHAT to test, never HOW MUCH to expect.**

### ⚙ AND ONE THAT IS ABOUT THE NOTIFICATION CHANNEL, NOT THE ANALYSIS: **PRE-WRITE THE ESCALATION, INCLUDING ITS FIRST LINE**

**A stop-loss fired twice in one session, and both times the push to the project lead read
*"no action needed unless overruling"* — correctly, because a conjunction governed the actual
decision and only one of its two terms was satisfied.**

**⇒ THE READER HAS NOW BEEN TRAINED TWICE THAT THIS NOTIFICATION MEANS NOTHING TO DO.** A third
arriving in the same channel, from the same sender, about the same subject **is the textbook
setup for alarm fatigue** — and it is the one that would matter.

**THE FIX IS THE PRE-COMMITMENT STRUCTURE APPLIED TO THE MESSAGE ITSELF: compose the
decision-required escalation BEFORE the event, verbatim, with only live numbers appended at
send time.** **Composed under the alarm, it will read like the two that preceded it — because
the person writing it is the person who has just written those two.**

**AND FIX THE FIRST LINE, NOT ONLY THE BODY.** A phone notification is read as **sender +
opening words + nothing else.** **The category must be legible before the content**: *"DECISION
REQUIRED — v102 below its replacement"* is a different object from a status line that happens
to contain a decision three sentences in.

**Generalises past this project: any alarm that can fire in both a "note it" and an "act now"
mode needs the two messages written at different times — the routine one whenever, the
decisive one in advance.**

### ⚙ WHY THESE ARE RULES AND NOT ADVICE — read this before concluding the answer is "be careful"

**All eleven failures in the session that produced this file were committed by people APPLYING
THE STANDARD AT THE TIME.** Four instruments were broken **in the fixing**. A stop-loss whose
author had written *"a stop-loss that cannot fire is worse than none"* in its own docstring
reintroduced the fault in its segmentation. A selftest's fixture was one the broken design also
passed. **Not one of these was carelessness, so "be more careful" is not available as a fix.**

**And the reason judgement fails here specifically: the correct action often FEELS LIKE A
FAILURE IN THE MOMENT.** The builder arm, on declining to write a four-neighbour refusal into
an unread file at 03:30 — **"it did not feel like discipline at the time, it felt like stopping
short."** **That is exactly why it needs a rule behind it rather than a judgement**: a
judgement made under that feeling reliably goes the other way.

**Same shape across the session: retracting a number that flatters you, reporting an estimate
at the n where it looks smallest, declining to loosen a rule at the moment it binds, and
specifying rather than building. Every one of them feels like giving something up while you do
it.** **The rules exist to make the right move survive that feeling.**

**AND THE COUNT BELONGS TO THE BOUNDARY, NOT TO EITHER LANE.** Across both arms, **not one
retraction came from an author re-reading their own work.** Every one came from a peer with the
primary open, or from an agent explicitly briefed to disagree. **⇒ Structure caught eleven
things that care would not have — which is the argument for the two-lane protocol and for
briefing agents to challenge their own brief, stated as a measurement rather than a
preference.**

### ⚙ AND THE INVERSE RULE, which is the only one here that says to measure LESS: **A MEASUREMENT YOU DO NOT NEED IMPORTS ITS POPULATION**

**Every other rule in this file says check your number. This one says notice when you do not
need one.**

**The case.** A graph walk over conveyor topology needed a visited set. The argument offered
was a frequency one — *"two conveyors pointing at each other is 9.9% of our binding tiles, so
cycles are common"* — and **that 9.9% is a share of BINDING TILES while the claim required
CYCLE-REACHABLE-UPSTREAM-FROM-A-DEAD-END. Different populations.**

**But the correct argument required no measurement at all.** **A visited set is justified by
ASYMMETRIC PAYOFF: three lines and a set lookup, against an infinite loop inside a 10 ms budget
that discards the unit's turn SILENTLY.** **No reachability rate could make omitting it
correct — not 9.9%, not 0.1%.**

**⇒ A BOUNDED-COST / UNBOUNDED-RISK DECISION WAS DRESSED IN A FREQUENCY ARGUMENT THAT DID NOT
APPLY. Reaching for a measurement you do not need is NOT FREE: it imports that measurement's
population, and the borrowed population was wrong.** **The stronger case was the simpler one.**

**PRACTICAL FORM: before citing a rate in support of a decision, ask whether the decision turns
on the rate at all. If the cost is bounded and the downside is unbounded, the rate is
decoration — and decoration carries a denominator.**
**Corollary worth keeping separate: "settled for the build" and "settled as a measurement" are
different states.** The reachability rate here is still unmeasured and still worth knowing —
**it says how often the naive version would have failed** — but it is off the critical path,
and conflating the two would either block a correct build or bank an unearned number.

### ⚙ AND A SECOND RULE OF THE SAME CLASS: **COST THE FIX, NOT ONLY THE DEFECT**

**Every ranking this project used before 2026-08-10 priced the DEFECT and never the FIX** —
including the one a shipped plank was selected from. **When the four titanium-delivery repair
classes were finally costed on both sides, the top class changed sign:**

| | defect | fix | **net** | return |
| --- | ---: | ---: | ---: | ---: |
| finish unterminated lines, **aimed** (walk upstream; finish only if the chain reaches a harvester) | 464 | 38 | **+411** | 11.9× |
| finish unterminated lines, **as an unconditional invariant** | 464 | **681** | **−223** | 0.7× |

**Same idea, opposite sign, and the entire difference is ONE UPSTREAM WALK.**
**⇒ *"Finish unterminated lines"* is a GOOD PLANK and a BAD RULE — a distinction that cannot
exist in a defect-only ranking, because the defect is identical in both rows.**

**And the ordering itself is not stable across the two ways of pricing:** by **net titanium**
the four classes rank 411 / 182 / 130 / 102; by **return on spend** they rank **∞ / 95× / 38× /
11.9×** — **exactly reversed.** **Neither ordering is wrong; they answer different questions,
and a ranking that does not say which one it is answering has not ranked anything.**

**PRACTICAL FORM: before proposing a fix, price the fix at the LIVE scale, and report NET and
RETURN separately. A defect size is a reason to look; it is not a reason to build.**

### ⚠ TWO FAILURES THE ABOVE FIX DOES **NOT** CATCH — added at the end of the same session, from cases it missed

**The nine above are all "a number true somewhere, used somewhere else", and measuring both
sides inside your own arm defeats every one of them. These two are different in kind and the
same fix does nothing for either.**

**A. A SYMBOL ASSUMED SHARED BY TWO FORKS THAT DO NOT SHARE IT.** A comparison of the Eir and
Loki trees was run through `self.forward_guns` — **which does not exist in the Loki tree at
all** (zero references, all files; that tree gates through `_live_fwd_guns` /
`LOKI_FWD_GUN_CAP`). The search was correct, the measurement was correct, the report was
honest — **and the question was addressed to a name only one of the two trees has.**
**⇒ A GREP RETURNING NOTHING IN ONE FORK IS AMBIGUOUS BETWEEN "THE BEHAVIOUR IS ABSENT" AND
"THE NAME IS." Verify the identifier exists in both before comparing behaviour through it.**
**Measuring both sides of the comparison would not have helped — both sides were measured, and
one of them was measured through a symbol it does not have.**

**B. A PER-UNIT RATE REASONED INTO AN AGGREGATE WITHOUT ASKING HOW MANY UNITS.** *"Nothing kills
a 40 HP sentinel in two rounds — a gunner does 7/round"* was used to rule out enemy fire and
infer a self-`destroy()` loop. **The replay shows seven `−7` deltas from five distinct enemy
firing tiles: seven gunners × 7 = 49 ≥ 40.** **The premise failed on MULTIPLICITY, not on
mechanics.**
**⇒ AND THE ANSWER WAS ALREADY IN THIS FILE.** The standing context states the crack in the
defender's edge is **"concentration, not more damage"** — **the reasoning ran straight past a
line in the library it was reasoning from.**
**⇒ BEFORE RULING SOMETHING OUT ON A UNIT RATE, ASK HOW MANY UNITS. A per-unit constant is a
statement about one unit and nothing else.**

**The honest summary of the pair: the "measure inside your own arm" rule is the highest-yield
single fix available and it is not complete. Two of eleven failures in one session were
outside it — one in the SYMBOL layer and one in the ARITHMETIC-OF-AGGREGATION layer, neither
of which is a population question.**

## ⛔⛔ READ FIRST — **MOST OF THE STANDING CONTEXT BELOW DESCRIBES EIR, NOT THE LIVE BOT** (2026-08-10, s26, `prior-tracing-2026-08-10.md`)

**This is ONE fact, not seven separate caveats: the section below was built on an archive that
is ~92% Eir (`join.tsv`: 1,580 Eir games against 130 LOKI-8), and FOUR of its own instruments
INVERT when re-run on the v102 subset.**

| standing claim | Eir (as published) | **v102, same instrument** |
| --- | --- | --- |
| *"Everything about us breaks at r150"* — ammo Ti/100 rounds by band | 212 → **156 → 130** → 140 | **209 → 300 → 253 → 135 — converts 43% MORE after r150** |
| *"We under-build turrets"* — turrets built r200-300 | us 0.64 / field 2.22 | **us 2.15 / field 1.18 — we now OUT-BUILD them** |
| *"We bank and do not spend"* — Ti held at end of r200-300 | us 506 / field 348 | **us 96 / field 210 — INVERTED** |
| *"353 games reached r1000 and we won 57.2%"* | 30.2% reach r1000 (n=477) | **6.9% — 1 of 9. The clock claim has no current denominator at all.** |

**And the 57.2% figure's own source document says it must not be quoted as a property of the
current bot. This INDEX quotes it without that sentence.**

**⇒ Treat every item below as EIR-ERA unless it has been re-run on v102. The library's oldest
standing complaint — *"we bank and do not spend"* — is FALSE OF THE LIVE BOT, which now holds
less titanium than the field.**

**SECOND EXPOSURE, and it sits under a bigger conclusion: the `+11.4 / +16.6 / +22.3pp`
home-defence advantage — the evidentiary floor under `THE FORWARD ROAD IS CLOSED` — DOES NOT
REPRODUCE.** Same instrument (BUILD→DEATH, 50-round horizon, censored dropped): **Eir home
78.3% vs field 62.0% = +16.3pp; v102 71.5% (n=439) vs 81.5% (n=520) = −10.0pp.** Paired within
opponent (n≥20 both eras) the gap **narrows or flips in 5 of 8**, holds in 1, 2 saturated.
**n=439 supports "does not reproduce", NOT "refuted" — but the floor under a headline
conclusion is no longer standing on its published number.**

**THIRD: both "resolving" fixtures were certified by audits that never tested target
selection.** `probe-fidelity-orizon-flotte` declared orizon *"CLASS-VALID… usable as a field
instrument"* and `probe-fidelity-guards` declared band *"USABLE AS A GUARD"* — **every
predicate in both is opening / turret-type / geometry / lane-fraction.** The guard document
states its own purpose as *"does a change break our repair line, our harvester defence…"* —
**exactly what the targeting shortcut makes unreachable.** **Prior art existed and was not
consumed: `cad-probe-refreeze-spec` documented the build-site half of the same blindness two
days earlier.**

**Bucket counts over 34 traced priors: CLEAN 18 · ERA-DRIFT 7 · PROBE-CONTAMINATED 4 ·
FIXTURE-BLIND 2 · UNTRACEABLE 3.** **The majority is clean and that is the honest headline.**
**But two of the four probe-contaminated items are the fixture CERTIFICATIONS themselves — so
it is one bad instrument, not four bad documents, and a zero-retraction verdict audit is NOT
the same as the probe problem being small.**

## Standing context a sweep should know

- ~~**The field does not rush.** Only 12% of top-tier kills land by r100; median
  kill round r296.~~
  **⚠ INVERTS AGAINST THE CURRENT BOT (2026-08-10).** Strong-band kills landed **on us**:
  median **r316 → r202**, by-r100 **7.5% → 20.7%** (n=478 Eir / 58 v102, p=0.0009, two
  classifiers agreeing). **Caveat kept: the instrument measures "they kill US", so this is a
  MATCHUP property, not a new fact about the field.**
- ~~**Everything about us breaks at r150.** Five independent instruments agree:
  conversion ratio, raider survival (43→6 rounds), turret production, forward
  placement, ammo conversion.~~
  **⛔ THIS CLAIM NOW HAS ZERO OF ITS FIVE INSTRUMENTS ON v102 (2026-08-10).** Three fell in
  `prior-tracing`; the other two in `standing-context-rederived`. **Forward placement does not
  merely weaken — it REVERSES: after r150 v102 plants turrets FORWARD (55.6% → 70.6% →
  83.3%) while the field pulls them HOME (65.8% → 22.6% → 40.9%). Eir did the exact opposite
  in both roles.** **This reads directly on `THE FORWARD ROAD IS CLOSED` below: v102 is doing
  the closed thing at 83%, and losing those turrets at 11.6% 50-round survival.**
- **Late offensive insertion is refuted** (`late-game-doctrine-2026-08-09.md`):
  2.34% of forward throws at r200+ ever land a single attack on the enemy core.
  **⚠ SUBJECT CORRECTED 2026-08-10 — this was published as "refuted FOR US" and it is not a
  claim about us at all.** The figure is **archive-wide over ALL teams' throws** (§1's whole
  four-band table is field-wide). **Splitting it by our version is a category error.** Our own
  r200+ inserts number **41 in the entire Eir era**, and on our own throws there is **no r150
  cliff at all** (73 → 75 → 7 → 9) — **our collapse is at r200, on n=17.**
  **Same family as the `2.68 healers` error: a field figure relabelled as ours.**
  **Archive drift on the published level, separate from the subject error: 2.34% → 1.11% on
  25,357 throws, because the archive has tripled since publication.**
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
  5.4:1 exchange AGAINST the attacker**, ammo dominating. ~~**Against the measured
  field detail of 2.68 healers, N=2 suffices.**~~ It beats the defence opponents
  actually field, not the defence the rules permit.
  **⚠ CORRECTED 2026-08-09 (s25) — `2.68` WAS OUR OWN NUMBER, RELABELLED "FIELD" BY
  THIS ENTRY.** Its source, `../besieged-core-confound-2026-08-09.md:28,119,131`, reads
  *"**Our** detail on 3+ rounds is **2.68** adjacent builders"* and states the field
  figure in the same sentence: **FIELD 2.49, TOP 1.99.** The sentinel-file economics were
  therefore sized against **our own defensive detail** while claiming to be sized against
  the opponent's. **Third-party re-derivation (s25): 2.13 at 3+ attackers, 1.57 at 1,
  N=28,277.** Direction of the error: it made the attack look **harder** than it is —
  **N=2 sentinels net +9.5 HP/round, not +7.3.** Conservative by luck, not by design.
  **This is the citation-failure family in the NUMBERS layer rather than the quote layer**
  — a true figure attached to the wrong referent, which is exactly what the "verbatim is
  necessary and not sufficient" rule above was written about. **A number carries a subject;
  copy the subject with it.**
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
  **INDEPENDENTLY CONFIRMED by the builder arm the same day, and NOT provisional:**
  **1,842,445 ordered pairs over 205 replays, 0 inversions**, cross-team ordering
  included — plus **two causal tests that never look at log ordering** (so the finding
  cannot be an artifact of how the replay writer sorts): **41,613 vacate-then-enter
  pairs, lower id always the vacater, 0 inversions**; and **1,961/1,961 victims of a
  higher-id launcher unable to move that round.** Four consequences it established, all
  build-relevant:
  - **A unit created MID-ROUND does not act that round** (24,045 new entities, 0 acted).
    A core-spawned builder first acts the FOLLOWING round and, holding the highest id,
    **acts LAST among our units**.
  - **A unit killed earlier in the round loses its turn entirely** (1,470/1,470).
    **Killing with a LOWER-id unit denies the victim's turn.**
  - **Cores are always id 1 (team A) and id 2 (team B) in every replay** — so **team A's
    core acts first in every round of every game.**
    **DO NOT CHASE THIS AS AN EDGE — MEASURED NULL (research, s25).** It was flagged as
    "a free seat asymmetry nobody has exploited"; it does not reach the scoreboard.
    ~~Over **2,715 ladder games**: win rate **seat a 50.6% (n=1,392) vs seat b 52.3%
    (n=1,323), z = −0.90, p ≈ 0.37**; **`core_kill_share` 30.2% vs 30.7%, z = −0.25,
    p ≈ 0.80**.~~
    **⚠ THAT EVIDENCE IS INVALID — WITHDRAWN 2026-08-09 (s26, research). THE CONCLUSION
    SURVIVES ON REPLACEMENT EVIDENCE; THE NUMBERS ABOVE DO NOT.** `ladder_games.tsv`'s
    column named **`seat` is not our seat — it is the WINNER's side**
    (`tools/corpus/ladder_meta.py`: `seat=(g.get("winnerSide") or "")`, read at source).
    So *"win rate by seat"* computed off it is **near-circular**: on a loss the column
    names the **opponent's** side, so the statistic is close to *"how often are we team
    A"*, which is ~50% by construction and cannot measure a seat effect at all.
    **Replacement evidence, on a seat variable established against the in-replay
    `DEATH`/`core` team index rather than `winnerSide`: still no seat effect, p = 0.48
    and p = 0.29** (`../per-opponent-gates-v102-2026-08-09.md`). **So "do not chase it"
    stands — it was right for the wrong reason for a day.**
    **The trap is live for anyone else reading that column** and the same deliverable
    shows it manufacturing *"v102 seat B 87.5% vs seat A 26.9%, p = 1.7e-05"* out of
    nothing. Whatever the one-turn head
    start is worth mechanically, **it is not worth build effort.** Two descriptive
    asymmetries, untested and not claimed: they kill our core slightly more often when we
    are seat a (33.3% vs 29.9%), and our own kills come faster in seat a (median r139 vs
    r163.5) — both consistent with seat-a games simply being more decisive.
    **CALIBRATION — do not over-rotate on that null (side lane, s25).** The null is about
    **AGGREGATE OUTCOMES**; the id-ordering fact stays **real and load-bearing at the
    MICRO level** — the r74 autopsy's r4 body-block was genuinely id-decided. **The joint
    reading: the edge exists per-event, and the events do not accumulate into any outcome
    edge anyone has found.** So *"do not chase it"* is right for **planks**, and the fact
    remains the correct explanation for **individual race outcomes in decodes** — which is
    also why "was this luck or reproducible?" is answerable at all.
  - **Ids are ONE GLOBAL COUNTER SHARED WITH RESOURCE STACKS** (97,455 of the gaps are
    stack ids). **Id MAGNITUDE is meaningless** — dominated by titanium churn — and only
    **ordering** carries information. Anyone inferring "how recently was this built" from
    an id delta is wrong.
  **Two decoder traps from the same work, for anyone writing a parser:** `botOutput` is
  emitted at the **END** of a unit's turn, after its actions — assuming otherwise
  manufactured **689,520 phantom displacements against 2,672 real throws** in an
  intermediate pass; and gunners re-emit `placeEntity` for an **existing** id (4,990
  times, from `rotate()`), so a parser treating every `placeEntity` as a creation invents
  entities.
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
