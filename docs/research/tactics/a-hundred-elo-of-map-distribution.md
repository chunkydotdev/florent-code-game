---
tactic: A rating gap can be a map-distribution artefact — one bot moved ~100 Elo with no code change
source: https://battlecode.org/assets/files/postmortem-2025-om-nom.pdf
origin: Battlecode 2025 / om nom (US Qualifiers winner, finalist); corroborated by BC2023 don't @ me and BC2020 The High Ground
evidence: documented
transfers: partial
---
WHAT IT IS — om nom report a rating move of about 100 Elo caused entirely by which maps the
ladder was running, with their submission held fixed. They set up the control themselves:

> *"Indeed, we did not re-upload a bot until the next Thursday, and our bot’s elo was relatively
> static. However, when they uploaded the tournament maps our bot jumped about 100 ELO reaching
> the 2000s for the first time."*

(*"they"* is the organisers, who added the tournament map pool to the ladder; the subject of the
100-Elo jump is om nom's own unchanged bot.) They had already noticed the same effect in the
tournament itself: *"We won with much larger margins then we had been winning in scrims"*, which
they attribute to favourable maps — *"complex pathing, large rush distance"*.

**Two independent corroborations that a map-pool change moves rating without a code change.**
BC2023 don't @ me: *"These maps had more variance than the original three maps, allowing our bot
to climb rating without any adjustments."* BC2020 The High Ground, on the organisers doing it
deliberately: *"the devs indirectly nerfed rush through large and hard-to-path maps in the
seeding tournament. Some very strong rush teams were knocked out pretty early"*.

WHY IT MIGHT TRANSFER — **It is a calibration on the number this whole sweep is aimed at.** We are
reasoning about a 360-500 Elo gap as if it were a pure strength difference. This source says that
in a comparable league, **~100 Elo of one bot's apparent strength was the map distribution
interacting with that bot's shape** — an amount that is a fifth to a quarter of our gap, from a
single environmental variable. It does not make the gap illusory; it says a meaningful slice of
any rating difference is a *fit between bot and map pool*, and that slice is addressable by
conditioning on map properties rather than by getting stronger. That is the same lever
[`generality-saturates-and-then-stops-paying`](generality-saturates-and-then-stops-paying.md)
arrives at from the opposite direction, and INDEX already names our width gradient as an
unconditional-opening failure.

WHAT WOULD KILL IT — **Our ladder's map pool is presumably stable**, so there is no event to
observe and the finding cannot be replicated as an experiment — only inferred cross-sectionally
by comparing our performance across map types, which is confounded by everything else that varies
with map size. More fundamentally, **om nom's 100 Elo is a claim about their bot on that pool,
not a general constant**; copying the number to our league would be precisely the "a number
carries a subject" error INDEX documents. The honest transfer is the *category* — map fit is a
component of rating — not the magnitude.

BUILDER HOOK — Same query as
[`upset-them-where-they-are-overfitted`](upset-them-where-they-are-overfitted.md), so run it once
and read it twice: win rate and `core_kill_share` against the top band, bucketed by map width,
height, symmetry and ore count. Here the question is not "where can we ambush them" but **"how
much of our deficit is map fit"** — i.e. how wide is the spread across buckets. A large spread
says a geometry branch is worth real money; a flat profile says the gap is strength and this file
is closed.
