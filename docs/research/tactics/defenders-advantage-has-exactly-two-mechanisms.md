---
tactic: The defender's advantage decomposes into exactly two mechanisms — and the only documented way to cancel it is production AT the target, which cancels only one of them
source: http://web.archive.org/web/20230716050510/https://liquipedia.net/starcraft2/Defender%27s_Advantage
origin: RTS theory — Liquipedia StarCraft II, "Defender's Advantage" (via Wayback; the live site rate-limits)
evidence: documented
transfers: partial
---

## WHAT IT IS

This library's single most load-bearing standing fact is that **the defender wins any
titanium-symmetric attrition race 2.2:1 (4.4:1 on a stacked tile)**, and every sweep since has
been read against the question *"how does anyone break that."* RTS theory has a canonical
decomposition of the same axiom, and it names **two** mechanisms and no others:

> *"refers to the well-known idea that a player is defending an attack at his/her base is at an
> inherent advantage stemming from the fact that the attack is occurring at a minimal distance
> from the defender's production facilities and that the defender has additional time to produce
> units (due to map attack distances)."*

**Referent check.** The quote begins mid-sentence because the article's bolded subject term
*"Defender's Advantage"* immediately precedes *"refers"*. The grammatical error (*"a player is
defending"*) is in the original. The two mechanisms are therefore: **(i) reinforcement travel
distance**, and **(ii) production time bought by that distance.**

**The condition under which it weakens is named, and it removes only one of the two:**

> *"the defender's advantage is somewhat mitigated if both armies are maxed (200/200 supply),
> but this does not change the fact that the distance needed for reinforcements to arrive is
> reduced."*

**Referent check.** The preceding word is *"Of course,"*; the following sentence adds *"In
addition, even when supplies are maxed, proximity to static defense, such as fighting near a
planetary fortress or near a shield battery, can provide an additional form of defender's
advantage."* So at a unit cap the **production** half disappears and the **travel** half does
not.

**And the one documented cancellation in the whole article is production placed AT the target:**

> *"As Day(9) says, there is always a defender's advantage, but indeed there is one exception."*

> *"This close warp in cancels the notion of the Defender's Advantage (when it comes to
> reinforcements). The advantage based on fortifications and structures remains."*

**Referent check.** *"This close warp in"* is the sentence before: *"Protoss, after the Warp
Gate tech has been researched, have the ability to warp in at a proxy pylon close to the
defenders base."* *"one exception"* is stated as the **sole** documented case. The cancellation
is explicitly **partial** — reinforcement edge voided, fortification edge intact.

## WHY IT MIGHT TRANSFER

**It corroborates sweep 14's precondition #3 from a completely independent evidence path.**
Sweep 14 found that every BC2020 rush that killed bases produced its attackers **at the target**
rather than marching them, and filed that as
[`spawn-the-attack-at-the-target-not-a-march`](spawn-the-attack-at-the-target-not-a-march.md) —
*"This is the precondition we structurally lack."* Liquipedia, from RTS theory rather than
Battlecode, independently names forward production as **the one exception** to defender's
advantage. Two fields, one answer. That materially raises confidence in a finding this library
had from a single season.

The decomposition also sharpens what our own arithmetic is measuring, because **our two
mechanisms are not the same two**:

| their mechanism | our analogue | is it live for us? |
| --- | --- | --- |
| reinforcement **travel distance** | a builder walking home, 1 cardinal step/round, and moving is mutually exclusive with acting | **yes, and it is severe** |
| **production time** bought by that distance | the core spawns **≤1 builder/turn** on its 12-tile ring, with +20% scaling per builder | **yes, but rate-capped — turns are not purchasable** |
| — | **healing**, 4.00 HP/Ti (8.00 stacked), adjacency-capped at ~16 HP/round per tile | **this is ours and has no analogue in the source** |

That third row is the important one. Our defender's edge is **not** primarily either of
Liquipedia's mechanisms — it is a repair rate the source game does not have. So the maxed-supply
nuance transfers only partially: `MAX_TEAM_UNITS = 50` is our supply cap and would kill the
production half, but it would leave both the travel half **and** the heal rate untouched. **Our
defender's advantage is more robust than the canonical one, not less** — which is consistent
with everything the library has measured and is the honest reading.

The genuinely actionable line is the **partial** cancellation. Forward production voids
reinforcement, *"The advantage based on fortifications and structures remains."* In our terms: a
forward plant does nothing about the enemy's turrets or their heal ring. It only removes their
travel-and-production edge — which, per the table above, is the part of their advantage we were
least blocked by.

## WHAT WOULD KILL IT

- **We cannot produce at the target.** Only the core spawns builders, ≤1/turn, on its own
  Chebyshev-1 ring. The one documented exception to defender's advantage is **structurally
  unavailable to us**, and no amount of forward building creates it — a forward plant produces
  nothing. This is the same wall sweep 14 hit, restated by a second field.
- **The nearest thing we have is the launcher**, which *displaces* rather than produces — and
  our own measurement caps what that buys: **post-throw dwell is one round**, 96.4% of enemy
  victims are off the landing tile within one round, and the share of throws lasting the 11
  rounds a gunner needs is **0.42%**. Throwing is not warp-in.
- **Liquipedia is a wiki, not a measurement.** *"the well-known idea"* and *"As Day(9) says"* are
  appeals to authority; no number in the article is measured. It is doctrine, correctly labelled
  `documented` because the *doctrine* is documented — not the effect.
- **The 200/200 supply nuance may invert here.** At `MAX_TEAM_UNITS`, our builders cannot be
  replaced, so a defender at the cap loses the production half exactly as the source says — but
  our own corpus has never shown us near the cap in a contested game, so the condition may never
  bind.

## BUILDER HOOK

None new, and that is the finding. This file's value is **corroborative**: it independently
confirms that the road sweep 14 identified as closed (production at the target) is the one road
RTS theory also names as the only one, and it explains *why* the forward road stays closed here
while it opened in BC2020 and BC2023. Anyone proposing a forward doctrine should be able to say
which of the two mechanisms it cancels — and if the answer is "neither", it is not a
defender's-advantage argument at all.

## SOURCES QUOTED IN THIS FILE

- http://web.archive.org/web/20230716050510/https://liquipedia.net/starcraft2/Defender%27s_Advantage

All five quoted strings were verified verbatim by me, by literal grep against the tag-stripped
raw Wayback HTML, during tactics sweep 15 (2026-08-09). Apostrophes are ASCII `'` (U+0027)
throughout, consistent with the rest of Liquipedia. **The live Liquipedia site rate-limits every
request; this URL is the Wayback capture and is the one that was fetched.**

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
