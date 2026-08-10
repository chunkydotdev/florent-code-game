---
tactic: Plant a cheap building in their base — the AIIDE rules whitelist it by name, and the payoff is their overreaction
source: https://davechurchill.ca/starcraft/aiide/
origin: AIIDE StarCraft AI Competition official rules (2026 edition, Dave Churchill); Jay Scott's Starcraft AI blog on Steamhammer and Locutus
evidence: documented
transfers: yes
---

WHAT IT IS — **the question "has any league ruled on this" has a precise answer,
and it is more permissive than anyone here has assumed.** The AIIDE StarCraft AI
Competition maintains an explicit whitelist, and it names the canonical
plant-in-their-base trick:

> *"The following StarCraft bugs/tricks are permitted: Plague on interceptor,
> Units pressed through, Drops to defuse mines, Mineral walk, Manner Pylon,
> Lurker hold position, Observer over turret, Stacking air units."*

A *Manner Pylon* is a cheap building placed inside the opponent's worker line to
obstruct mining and pin workers. **It is expressly legal.** (Liquipedia's article
on it is the standard reference; I could not re-fetch it — liquipedia.net
rate-limited this session with HTTP 429 — so **no wording from it is quoted
here.**)

The forbidden list is where the real line sits:

> *"All other bugs/exploits are forbidden. Bots caught attempted these exploits
> will be disqualified. This includes but is not limit to: Flying drones and
> templars, Terran sliding buildings, Stacking ground units, Allied mines, Gas
> walk to get through blocked entrances or ramps"*

*(the typos "attempted" and "is not limit to" are the source's.)*

**Read the two lists together and the principle is unmistakable: placing an
object to block the opponent is legitimate play; using an engine bug to phase
*through* a legitimate block is a disqualification.** Note also that *"Allied
mines"* — friendly-fire exploitation — sits on the forbidden side, which is a
useful calibration for how far [[blind-their-gun-with-their-own-body]] should be
pushed if our organisers ever weigh in.

**And the payoff is not the object. It is what the object makes them do.** Jay
Scott, on Steamhammer's gas steal — a bot-implemented denial building:

> *"The point of stealing gas is to channel your opponent’s play into a direction
> that you can exploit."*

made nearly free by the same author:

> *"The SCV leaves the refinery not quite finished, so that it can be canceled
> before it is destroyed, getting most of the mineral cost back."*

on Locutus, a competition bot with an opponent-specific denial feature:

> *"It’s called “pylon harassment” and in this version it is hardcoded to happen
> only against Iron."*

> *"Those that pull workers to defend against proxy buildings might pull too many
> workers and stop mining, for example."*

and the thesis stated outright:

> *"The bot 5 Pool exploited the fact that most opponents either didn’t react and
> lost, or overreacted and fell behind."*

> *"it is much easier to overreact to the rush and be safe for the moment than to
> react with exactly enough defense"*

WHY IT MIGHT TRANSFER — **this is Magnus's "play the players" mandate with a
sourced mechanism, and we already own the instrument that measures the
reaction function.**

1. **The object is nearly free here too.** A barrier is **3 Ti at +1% scale**,
   the joint-cheapest scaling increment in the game
   ([[minimum-cost-blockading-body]]). And our version of Steamhammer's
   cancel-refund is better than theirs: **`destroy()` is free, costs no action
   cooldown and is unlimited per turn**, and a destroyed entity **stops
   contributing to cost scale** — so a denial barrier that has done its job can
   be un-bought on the scale side at zero cost (see
   [[destroy-rebuild-converter]]).
2. **The forbidden list does not touch anything we can do.** There is no
   phase-through, no collision bug, no ally-damage primitive we could abuse
   accidentally. **Everything in the denial family here is on the permitted side
   of AIIDE's line as a matter of engine capability, not restraint.**
3. **We already measure the reaction function.**
   `docs/research/opponent-reaction-atlas-2026-08-09.md` (2,735 attributed
   replays, 495/495 winner-field validated, 5,470/5,470 shot-count reconciled)
   carries per-opponent **defensive-build response rates and median reaction
   latencies** — e.g. Ouroboros at **79.3% heal response, median latency 8
   rounds**, defensive-build rate ratio **1.2**. **Jay Scott's claim is that the
   money is in the tail of that distribution: the opponents who over-pull.** We
   have the atlas; what we have never done is *provoke* it and re-read it.

WHAT WOULD KILL IT — 

1. **Our organisers have not ruled, and AIIDE is not our organiser.** This file
   is evidence about *norms in the field*, not permission. **It should not be
   cited as authority.** The one thing it does settle is that denial-by-object
   is normal competitive practice rather than an exploit.
2. **The forward road is closed on three of our own instruments.** Planting in
   their base is the tactic our own measurement most consistently refutes: a
   raider in enemy territory after r150 lives ~6 rounds, and **2.34% of forward
   throws at r200+ ever land a single attack on the enemy core**. **This is an
   opening-window tactic here or it is nothing** — which happens to match the
   250-round programme, and does not match anything later.
3. **Hardcoding to one opponent is now regulated elsewhere.** AIIDE's 2026
   rules add: *"Please do not attempt to identify bots through other means or
   previously learned behavior."* Locutus's Iron-only feature is exactly the
   practice that rule targets. **A general trigger ages better than a named
   one**, and would survive an equivalent ruling here.
4. **The reaction we want may not exist.** Ouroboros' median heal latency of 8
   rounds is *slow*, which suggests under-reaction rather than over-reaction —
   the failure mode Jay Scott says loses, but not the one that pays us.

BUILDER HOOK — **a provocation read, not a plank, and the atlas already has the
baseline.** Plant one barrier inside the enemy's economy in the opening window
and re-run the reaction-atlas cuts on those games alone:

- **builders diverted per barrier** (how many enemy builder-turns go to removal
  at 2 dmg / 2 Ti against our 3 Ti object),
- **change in their harvester and turret build rate in the following 30 rounds.**

Overreaction shows up as diverted builder-turns exceeding the 15 the barrier
strictly demands. **If the ratio is ≤1, they react correctly and this whole road
is a tempo loss** — which is a clean, cheap kill criterion.

Related: [[minimum-cost-blockading-body]] · [[ore-tile-denial]] ·
[[escorted-forward-plant]] · [[blind-their-gun-with-their-own-body]] ·
[[no-league-bans-inducing-an-opponent-timeout]] · [[destroy-rebuild-converter]]

---

> ### ⚠ CAVEAT ADDED 2026-08-10 (research arm) — **`THE FORWARD ROAD IS CLOSED` IS DEMOTED. DO NOT REASON DOWNSTREAM OF IT AS SETTLED.**
>
> This file treats that conclusion as established. **Two things have happened to it
> and neither had propagated here:**
>
> 1. **Its evidentiary floor did not reproduce.** `INDEX.md` records that the
>    `+11.4 / +16.6 / +22.3pp` home-defence advantage — the floor under the
>    conclusion — **does not reproduce on v102**: Eir home 78.3% vs field 62.0%
>    (+16.3pp) but **v102 71.5% (n=439) vs 81.5% (n=520) = -10.0pp**, and paired
>    within opponent the gap **narrows or flips in 5 of 8**. The index's own words:
>    **"n=439 supports 'does not reproduce', NOT 'refuted'"**.
> 2. **A field-wide cut now runs against it.** `../bisons-fast-kill-2026-08-10.md`:
>    **2+ forward in-range sentinels standing by r45 takes core-kill-by-r100 from
>    3.6% to 23.1% across the field (n=17,235/804, p=1.9e-12)**, with a powered
>    placebo firing null. The Bisons reach that position in **42.3%** of games and
>    convert **47.5%**. **The forward road is demonstrably open for other teams.**
>
> **The defensible statement is narrower than the one in this file: OUR forward road
> was closed on OUR instruments, in the Eir era.** That is not "the forward road is
> closed", and the two were being used interchangeably.
>
> **Under D12** (Magnus, 2026-08-10 - *"test everything in unrated games before we
> refute them"*) **an archive-sourced closure cannot retire a road at all.** This one
> goes to the **bottom of the queue, not off it.**
